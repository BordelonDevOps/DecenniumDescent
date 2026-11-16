param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$TraceRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'Bishop-ViewProjection.ps1')
. (Join-Path $PSScriptRoot 'Bishop-TypedCommand.ps1')
. (Join-Path $PSScriptRoot 'Bishop-ReadProbes.ps1')
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$TraceRoot=(Resolve-Path -LiteralPath $TraceRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$launcher=(Resolve-Path -LiteralPath (Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1')).Path
function Require($test,$message){if(!$test){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$assemblies=@('Core','Persistence','LabModel')
foreach($part in $assemblies){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$manifest=Get-Content -LiteralPath (Join-Path $TraceRoot 'manifest.json') -Raw|ConvertFrom-Json -AsHashtable
$inputs=@(Get-Content -LiteralPath (Join-Path $TraceRoot 'inputs.jsonl')|ForEach-Object{ConvertFrom-Json -AsHashtable $_})
function Start-Session {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithBishopEntry(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
}
function Dispatch($session,$command,$operation,$seat){
    if($operation-in'clock','close'){$session.SubmitSessionCommand($command)}
    elseif($operation-eq'defender-presence'){$session.SubmitDefenderIntimidatingPresence([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
    elseif($operation-eq'defender-sanctuary'){$session.SubmitDefenderSanctuary([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
    else{$session.Submit(($seat ?? 'Player'),$command)}
}
function Check-Marks($folder){
    $hashes=[ordered]@{}
    foreach($mark in $manifest.marks){
        $hash=Digest (Join-Path $folder $mark.name)
        Require ($hash-ceq$mark.sha256) "Checkpoint differs: $folder/$($mark.name)"
        $hashes[$mark.name]=$hash
        Require ((Digest (Join-Path $folder ($mark.name+'.after-probes.ddsave')))-ceq$mark.sha256) "Read/denial probes mutated $($mark.name)."
        foreach($probe in $mark.probes){
            $actual=Digest (Join-Path $folder $probe.request.evidenceRead)
            Require ($actual-ceq$probe.sha256) "Read/denial behavior differs: $($probe.request.evidenceRead)"
            $hashes[$probe.request.evidenceRead]=$actual
        }
        foreach($seat in 'Player','FirstOpponent','RecoveryOpponent'){
            $view=$mark.views.$seat;$viewHash=Digest (Join-Path $folder $view.name)
            Require ($viewHash-ceq$view.sha256) "Filtered $seat view differs at $($mark.name)."
            $hashes[$view.name]=$viewHash
        }
    }
    return $hashes
}
$report=[ordered]@{status='FAIL';scope='Connected reference checkpoint parity; support for bounded Bishop acceptance, not full module completion.';
    startedUtc=[DateTime]::UtcNow.ToString('o');traceRoot=$TraceRoot;traceSha256=(Digest (Join-Path $TraceRoot 'inputs.jsonl'));
    assemblies=@($assemblies|ForEach-Object{@{name=$_;sha256=(Digest (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll"))}});
    paths=[ordered]@{}}
try{
    foreach($mode in 'ConsoleUninterrupted','ConsoleRestored'){
        $folder=(New-Item -ItemType Directory -Path (Join-Path $Run $mode)).FullName
        $trace=@($inputs|Where-Object{$mode-eq'ConsoleRestored'-or$_.op-ne'load'})
        $trace|ForEach-Object{ConvertTo-Json $_ -Depth 8 -Compress}|Set-Content -LiteralPath (Join-Path $folder 'inputs.jsonl') -Encoding utf8
        Push-Location $folder
        try{& $launcher -BishopEntry -AssemblyRoot $AssemblyRoot -InputPath (Join-Path $folder 'inputs.jsonl')|Set-Content -LiteralPath (Join-Path $folder 'responses.jsonl') -Encoding utf8}
        finally{Pop-Location}
        $responseLines=@(Get-Content -LiteralPath (Join-Path $folder 'responses.jsonl'))
        Require ($responseLines.Count-eq$trace.Count) "$mode response count differs."
        $revision=0
        for($index=0;$index-lt$trace.Count;$index++){
            $request=$trace[$index];$response=ConvertFrom-Json -InputObject $responseLines[$index] -NoEnumerate
            if($request.op-eq'view'){
                $responseLines[$index]|Set-Content -LiteralPath (Join-Path $folder $request.evidenceView) -Encoding utf8 -NoNewline
                continue
            }
            if($request.evidenceRead){
                $responseLines[$index]|Set-Content -LiteralPath (Join-Path $folder $request.evidenceRead) -Encoding utf8 -NoNewline
                continue
            }
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
            if($request.op-eq'view'){
                Get-BishopViewJson $session $request.seat|Set-Content -LiteralPath (Join-Path $folder $request.evidenceView) -Encoding utf8 -NoNewline
                continue
            }
            if($request.evidenceRead){
                Get-BishopProbeJson $session $request|Set-Content -LiteralPath (Join-Path $folder $request.evidenceRead) -Encoding utf8 -NoNewline
                continue
            }
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
    function Save-ReceiptMarks([long]$revision){
        foreach($mark in $manifest.marks|Where-Object revision -eq $revision){
            $session.Save((Join-Path $folder $mark.name))
            foreach($seat in 'Player','FirstOpponent','RecoveryOpponent'){
                Get-BishopViewJson $session $seat|Set-Content -LiteralPath (Join-Path $folder $mark.views.$seat.name) -Encoding utf8 -NoNewline
            }
            foreach($probe in $mark.probes){
                Get-BishopProbeJson $session $probe.request|Set-Content -LiteralPath (Join-Path $folder $probe.request.evidenceRead) -Encoding utf8 -NoNewline
            }
            $session.Save((Join-Path $folder ($mark.name+'.after-probes.ddsave')))
        }
    }
    Save-ReceiptMarks 0
    $final=[Decennium.Foundation.FileSaveStore]::new().Load($manifest.finalSource)
    Require ((Digest $manifest.finalSource)-ceq$manifest.finalSha256) 'The retained receipt source changed.'
    foreach($receipt in $final.Receipts){
        $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
        if($receipt.Principal-eq'TEST_ONLY.tac10-later-defender.v1'-and$command.Id.StartsWith('tac10.')){$result=$session.AdvanceAutomaticDefender()}
        else{
            $operation=if($command.Kind-eq'AdvanceClock'){'clock'}elseif($command.Kind-eq'EndFixedEncounter'){'close'}
                elseif($command.Kind-eq'UseIntimidatingPresence'-and$command.Actor-eq'TEST_ONLY.later-defender'){'defender-presence'}
                elseif($command.Kind-eq'RespondSanctuary'-and$receipt.Principal-eq'TEST_ONLY.tac10-later-defender.v1'){'defender-sanctuary'}else{'submit'}
            $seat=if($command.Actor-eq'TEST_ONLY.third-combatant'){'FirstOpponent'}elseif($command.Actor-eq'TEST_ONLY.recovery-defender'){'RecoveryOpponent'}else{'Player'}
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
