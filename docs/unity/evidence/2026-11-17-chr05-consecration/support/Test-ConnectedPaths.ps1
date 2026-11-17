param([string]$AssemblyRoot,[string]$FinalSource,[string]$Run,[ValidateSet('Export','ConsoleUninterrupted','ConsoleRestored','TypedUninterrupted','TypedRestored','ReceiptReplay')][string]$Mode)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
. (Join-Path $PSScriptRoot 'TypedCommand.ps1')
. (Join-Path $PSScriptRoot 'TraceCommand.ps1')
$Run=[IO.Path]::GetFullPath($Run);$FinalSource=(Resolve-Path $FinalSource).Path
$null=New-Item -ItemType Directory -Force $Run
$final=[Decennium.Foundation.FileSaveStore]::new().Load($FinalSource)
function Require($ok,$message){if(!$ok){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
Require ($final.WireSchemaVersion-eq115-and$final.Revision-eq428-and!$final.InventoryCombat) 'Wrong genuine completed lineage.'
$marks=@(0,80,150,200,231,250,344,346,352,353,360,361,375,428)
$seats=@('Player','FirstOpponent','RecoveryOpponent','FerryOpponent')
if($Mode-eq'Export'){
    $trace=[Collections.Generic.List[object]]::new()
    function Mark($revision){if($revision-in$marks){
        $path='r'+$revision.ToString('D3')+'.ddsave';$trace.Add(@{op='save';path=$path})
        foreach($seat in $seats){foreach($op in 'view','terrain','terrain-healing'){$trace.Add(@{op=$op;seat=$seat;actor='TEST_ONLY.companion';evidence=($path+'.'+$seat+'.'+$op+'.json')})}}
        $trace.Add(@{op='save';path=($path+'.after-read.ddsave')});$trace.Add(@{op='load';path=$path})
    }}
    Mark 0
    foreach($receipt in $final.Receipts){$trace.Add((ConvertTo-ConsecrationRequest $receipt));Mark $receipt.Revision}
    $trace|ForEach-Object{ConvertTo-Json -InputObject $_ -Depth 12 -Compress}|Set-Content (Join-Path $Run 'inputs.jsonl') -Encoding utf8
    @{source=$FinalSource;sha256=(Digest $FinalSource);revision=$final.Revision;marks=$marks;seats=$seats;scope='Trace export only; not gameplay execution'}|ConvertTo-Json -Depth 5|Set-Content (Join-Path $Run 'trace.json')
    return
}
$folder=Join-Path $Run $Mode
Require (!(Test-Path $folder)) 'Use a fresh path folder.'
$null=New-Item -ItemType Directory $folder
$trace=@(Get-Content (Join-Path $Run 'inputs.jsonl')|ForEach-Object{ConvertFrom-Json -AsHashtable $_}|Where-Object{$Mode.EndsWith('Restored')-or$_.op-ne'load'})
function New-Session{[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConsecration([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())}
function Dispatch($session,$command,$r){switch($r.op){
    'auto'{$session.AdvanceAutomaticDefender()}
    'clock'{$session.SubmitSessionCommand($command)}
    'close'{$session.SubmitSessionCommand($command)}
    'defender-presence'{$session.SubmitDefenderIntimidatingPresence([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
    'defender-sanctuary'{$session.SubmitDefenderSanctuary([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
    default{$session.Submit($r.seat,$command)}
}}
function Read-Projection($session,$r){
    $value=switch($r.op){
        'view'{$v=$session.View($r.seat);$targets=[ordered]@{};foreach($t in $v.KnownTargets.GetEnumerator()){$targets[$t.Key.ToString()]=$t.Value};$v=$v|Select-Object -Property * -ExcludeProperty KnownTargets,FleshWarden,ShortRest;$v|Add-Member -NotePropertyName KnownTargets -NotePropertyValue $targets;$v}
        'terrain'{,@($session.ObserveConsecration($r.seat,$r.actor))}
        'terrain-healing'{,@($session.ObserveConsecrationHealing($r.seat,$r.actor))}
    }
    ConvertTo-Json -InputObject $value -Depth 8 -Compress -EnumsAsStrings
}
$report=[ordered]@{status='FAIL';mode=$Mode;commands=0;sourceSha256=(Digest $FinalSource);startedUtc=[DateTime]::UtcNow.ToString('o')}
try{
    if($Mode.StartsWith('Console')){
        $inputPath=Join-Path $folder 'inputs.jsonl';$trace|ForEach-Object{ConvertTo-Json -InputObject $_ -Depth 12 -Compress}|Set-Content $inputPath -Encoding utf8
        $launcher=(Resolve-Path (Join-Path $PSScriptRoot '../../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
        Push-Location $folder
        try{& $launcher -Consecration -AssemblyRoot $AssemblyRoot -InputPath $inputPath|Set-Content (Join-Path $folder 'responses.jsonl') -Encoding utf8}finally{Pop-Location}
        $lines=@(Get-Content (Join-Path $folder 'responses.jsonl'));Require ($lines.Count-eq$trace.Count) 'Console response count.'
        for($i=0;$i-lt$trace.Count;$i++){$r=$trace[$i];$v=ConvertFrom-Json $lines[$i] -NoEnumerate
            if($r.evidence){[IO.File]::WriteAllText((Join-Path $folder $r.evidence),$lines[$i]);continue}
            $want=switch($r.op){'save'{'Saved'}'load'{'Restored'}default{$report.commands++;'Committed'}}
            Require ($v.Response-ceq$want) "Console $i expected $want, got $($v.Response)"
            if($want-eq'Committed'){Require ($v.Revision-eq$report.commands) "Console revision $i"}
        }
    }else{
        $session=New-Session
        foreach($r in $trace){
            if($r.evidence){[IO.File]::WriteAllText((Join-Path $folder $r.evidence),(Read-Projection $session $r));continue}
            if($r.op-eq'save'){$session.Save((Join-Path $folder $r.path));continue}
            if($r.op-eq'load'){$session=New-Session;$session.Restore((Join-Path $folder $r.path));continue}
            $command=if($Mode-eq'ReceiptReplay'){[Decennium.Foundation.CommandHistory]::Read($final.Receipts[$report.commands])}else{New-TypedCommand $r}
            $response=Dispatch $session $command $r;$report.commands++
            Require ($response.Response-eq'Committed'-and$response.Revision-eq$report.commands) "$Mode command $($report.commands) failed: $($response.Response)"
        }
    }
    Require ($report.commands-eq428) 'Incomplete command path.'
    Require ((Digest (Join-Path $folder 'r428.ddsave'))-ceq$report.sourceSha256) 'Final canonical bytes differ.'
    foreach($n in $marks){$p=Join-Path $folder ('r'+$n.ToString('D3')+'.ddsave');Require ((Digest $p)-ceq(Digest ($p+'.after-read.ddsave'))) 'Read mutated snapshot.'}
    $report.status='PASS';$report.checkpoints=$marks.Count;$report.seats=$seats;$report.files=@(Get-ChildItem $folder -File|Where-Object Name -notin 'responses.jsonl','inputs.jsonl'|ForEach-Object{@{name=$_.Name;sha256=(Digest $_.FullName)}})
}catch{$report.error=$_.Exception.ToString()}
finally{$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 8|Set-Content (Join-Path $folder 'result.json')}
if($report.status-ne'PASS'){throw $report.error}
Write-Output "$Mode PASS: 428 commands, 14 checkpoints, four seat views and terrain/healing projections. Cross-path equality requires separate comparison."
