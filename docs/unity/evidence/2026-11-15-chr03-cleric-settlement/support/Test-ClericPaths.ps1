param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$TraceRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$TraceRoot=(Resolve-Path -LiteralPath $TraceRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$launcher=(Resolve-Path -LiteralPath (Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1')).Path
function Require($test,$message){if(!$test){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$assemblies=@('Core','Persistence','LabModel')
foreach($part in $assemblies){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$manifest=Get-Content -LiteralPath (Join-Path $TraceRoot 'manifest.json') -Raw|ConvertFrom-Json
$inputs=@(Get-Content -LiteralPath (Join-Path $TraceRoot 'inputs.jsonl')|ForEach-Object{ConvertFrom-Json -AsHashtable $_})
function Start-Session {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericSettlement(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
}
function New-TypedCommand($request){
    # Independent constructor dispatch from retained typed JSON: no receipt reader,
    # snapshot reader, console parser or private rule resolver participates here.
    $inventory=$null;$combat=$null;$mining=$null;$presence=$null;$advancement=$null;$healingRite=$null
    if($request.inventory){$i=$request.inventory;$inventory=[Decennium.Foundation.InventoryRequest]::new(
        [Decennium.Foundation.RuleQuantity]::new($i.numerator,$i.denominator),$i.destination,$i.handling)}
    if($request.combat){$c=$request.combat;$combat=[Decennium.Foundation.CombatRequest]::new(
        $c.turn,$c.weapon,$c.stance,$c.knockout,$c.choice,$c.press)}
    if($request.mining){$m=$request.mining;$mining=[Decennium.Foundation.MiningSelectionRequest]::new(
        $m.version,[string[]]$m.categories,$m.ability,$m.hurried,$m.failureVictim,$m.criticalRecovery,$m.assistant)}
    if($request.intimidatingPresence){$presence=[Decennium.Foundation.IntimidatingPresenceRequest]::new([string[]]$request.intimidatingPresence.targets)}
    if($request.advancement){$a=$request.advancement;$advancement=[Decennium.Foundation.CharacterAdvancementRequest]::new([string[]]$a.features,$a.invocationPath,$a.earnedSpell)}
    if($request.healingRite){$healingRite=[Decennium.Foundation.HealingRiteRequest]::new($request.healingRite.curePreference)}
    [Decennium.Foundation.Command]::new($request.id,$request.actor,$request.revision,$request.kind,$request.target,$request.x,$request.y,
        $inventory,$combat,$advancement,$null,'None',$null,$null,$null,$null,$mining,$null,$null,$presence,$healingRite)
}
function Dispatch($session,$command,$operation,$seat){
    if($operation-in'clock','close'){$session.SubmitSessionCommand($command)}
    elseif($operation-eq'defender-presence'){$session.SubmitDefenderIntimidatingPresence([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
    else{$session.Submit(($seat ?? 'Player'),$command)}
}
function Check-Marks($folder){
    $hashes=[ordered]@{}
    foreach($mark in $manifest.marks){
        $hash=Digest (Join-Path $folder $mark.name)
        Require ($hash-ceq$mark.sha256) "Checkpoint differs: $folder/$($mark.name)"
        $hashes[$mark.name]=$hash
    }
    return $hashes
}
$report=[ordered]@{status='FAIL';scope='Connected reference checkpoint parity; support for CHR03 acceptance, not full module completion.';
    startedUtc=[DateTime]::UtcNow.ToString('o');traceRoot=$TraceRoot;traceSha256=(Digest (Join-Path $TraceRoot 'inputs.jsonl'));
    assemblies=@($assemblies|ForEach-Object{@{name=$_;sha256=(Digest (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll"))}});
    paths=[ordered]@{}}
try{
    foreach($mode in 'ConsoleUninterrupted','ConsoleRestored'){
        $folder=(New-Item -ItemType Directory -Path (Join-Path $Run $mode)).FullName
        $trace=@($inputs|Where-Object{$mode-eq'ConsoleRestored'-or$_.op-ne'load'})
        $trace|ForEach-Object{ConvertTo-Json $_ -Depth 8 -Compress}|Set-Content -LiteralPath (Join-Path $folder 'inputs.jsonl') -Encoding utf8
        Push-Location $folder
        try{& $launcher -ClericSettlement -AssemblyRoot $AssemblyRoot -InputPath (Join-Path $folder 'inputs.jsonl')|Set-Content -LiteralPath (Join-Path $folder 'responses.jsonl') -Encoding utf8}
        finally{Pop-Location}
        $responses=@(Get-Content -LiteralPath (Join-Path $folder 'responses.jsonl')|ConvertFrom-Json)
        Require ($responses.Count-eq$trace.Count) "$mode response count differs."
        $revision=0
        for($index=0;$index-lt$trace.Count;$index++){
            $request=$trace[$index];$response=$responses[$index]
            $expected=switch($request.op){'save'{'Saved'}'load'{'Restored'}default{$revision++;'Committed'}}
            Require ($response.Response-ceq$expected) "$mode input $index expected $expected; got $($response.Response)."
            if($request.op-notin'save','load'){Require ($response.Revision-eq$revision) "$mode input $index has wrong revision."}
        }
        Require ($revision-eq$manifest.revision) "$mode did not execute every committed command."
        $report.paths[$mode]=@{commands=$revision;inputs=$trace.Count;checkpoints=(Check-Marks $folder)}
        Write-Output "$mode passed $revision commands and $($manifest.marks.Count) exact checkpoints."
    }
    foreach($mode in 'TypedUninterrupted','TypedRestored'){
        $folder=(New-Item -ItemType Directory -Path (Join-Path $Run $mode)).FullName
        $trace=@($inputs|Where-Object{$mode-eq'TypedRestored'-or$_.op-ne'load'})
        $session=Start-Session;$revision=0;$results=[Collections.Generic.List[object]]::new()
        foreach($request in $trace){
            if($request.op-eq'save'){$session.Save((Join-Path $folder $request.path));continue}
            if($request.op-eq'load'){
                $session=Start-Session;$session.Restore((Join-Path $folder $request.path));continue
            }
            $result=if($request.op-eq'auto'){$session.AdvanceAutomaticDefender()}
                else{Dispatch $session (New-TypedCommand $request) $request.op $request.seat}
            $revision++
            Require ($result.Response-eq'Committed'-and$result.Revision-eq$revision) "$mode failed at revision $revision."
            $results.Add($result)
        }
        $results|ConvertTo-Json -Depth 5 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $folder 'responses.json') -Encoding utf8
        Require ($revision-eq$manifest.revision) "$mode did not execute every committed command."
        $report.paths[$mode]=@{commands=$revision;inputs=$trace.Count;checkpoints=(Check-Marks $folder)}
        Write-Output "$mode passed $revision commands and $($manifest.marks.Count) exact checkpoints."
    }
    $mode='ReceiptReplay';$folder=(New-Item -ItemType Directory -Path (Join-Path $Run $mode)).FullName
    $session=Start-Session
    function Save-ReceiptMarks([long]$revision){foreach($mark in $manifest.marks|Where-Object revision -eq $revision){$session.Save((Join-Path $folder $mark.name))}}
    Save-ReceiptMarks 0
    $final=[Decennium.Foundation.FileSaveStore]::new().Load($manifest.finalSource)
    Require ((Digest $manifest.finalSource)-ceq$manifest.finalSha256) 'The retained receipt source changed.'
    foreach($receipt in $final.Receipts){
        $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
        if($receipt.Principal-eq'TEST_ONLY.tac10-later-defender.v1'-and$command.Id.StartsWith('tac10.')){$result=$session.AdvanceAutomaticDefender()}
        else{
            $operation=if($command.Kind-eq'AdvanceClock'){'clock'}elseif($command.Kind-eq'EndFixedEncounter'){'close'}
                elseif($command.Kind-eq'UseIntimidatingPresence'){'defender-presence'}else{'submit'}
            $seat=if($command.Actor-eq'TEST_ONLY.third-combatant'){'FirstOpponent'}else{'Player'}
            $result=Dispatch $session $command $operation $seat
        }
        Require ($result.Response-eq'Committed'-and$result.Revision-eq$receipt.Revision) "Receipt replay failed at $($receipt.Revision)."
        Save-ReceiptMarks $receipt.Revision
    }
    $report.paths[$mode]=@{commands=$final.Revision;checkpoints=(Check-Marks $folder)}
    Write-Output "$mode passed $($final.Revision) commands and $($manifest.marks.Count) exact checkpoints."
    $report.status='PASS'
}catch{$report.error=$_.ToString()}
finally{
    $report.finishedUtc=[DateTime]::UtcNow.ToString('o')
    $report|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
}
if($report.status-ne'PASS'){throw $report.error}
