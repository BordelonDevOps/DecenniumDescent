param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run,[switch]$Worker,
    [string]$SourcesRoot='',[string]$Role='Current')
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh continuation directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$executionSourceBinding=Start-GeometryExecutionBinding $Run @($PSCommandPath,(Join-Path $PSScriptRoot '../../2026-11-16-chr03-bishop-runtime/support/Bishop-ViewProjection.ps1'))
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($value,$message){if(!$value){throw $message}}
if(!$Worker){
    $prior=Join-Path $repository 'docs/unity/evidence/2026-11-16-chr03-bishop-runtime'
    $old=(New-Item -ItemType Directory -Path (Join-Path $Run 'accepted-assemblies')).FullName
    Expand-Archive -LiteralPath (Join-Path $prior 'discovery-correction/execution-assemblies.zip') -DestinationPath $old
    $launch=Get-Content -LiteralPath (Join-Path $repository 'engine/artifacts/bishop-entry/regression-discovery/launch.json') -Raw|ConvertFrom-Json -AsHashtable
    foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){
        $dll="Decennium.Foundation.$part.dll";Require ((Digest (Join-Path $old $dll))-ceq$launch.assemblies[$dll]) "Accepted assembly changed: $dll"
    }
    $SourcesRoot=(New-Item -ItemType Directory -Path (Join-Path $Run 'sources')).FullName
    $archive=Join-Path $prior 'qualification-evidence.zip';if((Digest $archive)-cne'3c07ef37de6d7be2ee7da3da633f95c6ed4348ea7a5f2c8c93fcb81c52453649'){throw 'Accepted112 archive changed'};$zip=[IO.Compression.ZipFile]::OpenRead($archive)
    try{
        $entry=$zip.GetEntry('qualification/reference/manifest.json');$reader=[IO.StreamReader]::new($entry.Open())
        try{$manifest=$reader.ReadToEnd()|ConvertFrom-Json -AsHashtable}finally{$reader.Dispose()}
        foreach($mark in $manifest.marks){
            Require ([IO.Path]::GetFileName($mark.name)-ceq$mark.name) 'Unsafe checkpoint name.'
            $entry=$zip.GetEntry('qualification/reference/'+$mark.name);Require ($null-ne$entry) 'Authentic checkpoint absent.'
            $stream=$entry.Open();$destination=[IO.File]::Create((Join-Path $SourcesRoot $mark.name))
            try{$stream.CopyTo($destination)}finally{$destination.Dispose();$stream.Dispose()}
            Require ((Digest (Join-Path $SourcesRoot $mark.name))-ceq$mark.sha256) "Authentic checkpoint hash differs: $($mark.name)"
        }
        $manifest.marks|Sort-Object revision|ConvertTo-Json -Depth 16|Set-Content -LiteralPath (Join-Path $SourcesRoot 'marks.json') -Encoding utf8
    }finally{$zip.Dispose()}
    foreach($mode in 'Accepted112','Current'){
        $selected=if($mode-eq'Accepted112'){$old}else{$AssemblyRoot}
        & pwsh -NoProfile -File $PSCommandPath -Worker -Role $mode -AssemblyRoot $selected -SourcesRoot $SourcesRoot -Run (Join-Path $Run $mode)
        if($LASTEXITCODE-ne0){throw "$mode wire112 execution failed."}
    }
    $accepted=Get-Content -LiteralPath (Join-Path $Run 'Accepted112/results.json') -Raw|ConvertFrom-Json -AsHashtable
    $current=Get-Content -LiteralPath (Join-Path $Run 'Current/results.json') -Raw|ConvertFrom-Json -AsHashtable
    Require ($accepted.status-eq'PASS'-and$current.status-eq'PASS') 'Both actual runs must pass.'
    foreach($key in $accepted.artifacts.Keys){Require ($accepted.artifacts[$key]-ceq$current.artifacts[$key]) "Authentic predecessor parity differs: $key"}
    [ordered]@{status='PASS';sourceArchiveSha256=(Digest $archive);authenticCheckpoints=$accepted.checkpoints;
        actualContinuationCommandsPerRole=$accepted.commands;comparedCanonicalAndViews=$accepted.artifacts.Count;
        oldPid=$accepted.pid;currentPid=$current.pid;oldAssemblies=$accepted.assemblies;currentAssemblies=$current.assemblies;
        newProfileRejections=$current.newProfileRejections;artifacts=$current.artifacts}
        |ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
    Write-Output "PASS: $($accepted.checkpoints) authentic wire112 checkpoints; $($accepted.commands) continuation commands per role; $($accepted.artifacts.Count) exact canonical/view comparisons."
    Complete-GeometryExecutionBinding $Run $executionSourceBinding
    exit
}
. (Join-Path $PSScriptRoot '../../2026-11-16-chr03-bishop-runtime/support/Bishop-ViewProjection.ps1')
$SourcesRoot=(Resolve-Path -LiteralPath $SourcesRoot).Path
$loaded=[ordered]@{}
foreach($part in 'Core','Persistence','LabModel'){
    $file=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";$assembly=[Reflection.Assembly]::LoadFrom($file)
    $loaded[$part]=@{sha256=(Digest $file);moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
$marks=@(Get-Content -LiteralPath (Join-Path $SourcesRoot 'marks.json') -Raw|ConvertFrom-Json -AsHashtable)
$store=[Decennium.Foundation.FileSaveStore]::new();$artifacts=[ordered]@{};$count=0
$report=[ordered]@{status='FAIL';role=$Role;pid=$PID;startedUtc=[DateTime]::UtcNow.ToString('o');assemblies=$loaded}
function Start-OldSession {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithBishopEntry(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
}
function Capture-Views($session,$prefix){
    foreach($seat in 'Player','FirstOpponent','RecoveryOpponent'){
        $name=$prefix+'.'+$seat+'.view.json';$json=Get-BishopViewJson $session $seat
        [IO.File]::WriteAllText((Join-Path $Run $name),$json);$artifacts[$name]=Digest (Join-Path $Run $name)
    }
}
try{
    for($i=0;$i-lt$marks.Count;$i++){
        $mark=$marks[$i];$source=Join-Path $SourcesRoot $mark.name;$snapshot=$store.Load($source)
        Require ($snapshot.WireSchemaVersion-eq112-and$snapshot.Revision-eq$mark.revision) 'Authentic wire112 identity differs.'
        $session=Start-OldSession;$session.Restore($source)
        $name=$mark.name+'.roundtrip.ddsave';$session.Save((Join-Path $Run $name));$artifacts[$name]=Digest (Join-Path $Run $name)
        Require ($artifacts[$name]-ceq$mark.sha256) "Wire112 roundtrip differs: $($mark.name)"
        Capture-Views $session $mark.name
        if($i+1-lt$marks.Count){
            $next=$marks[$i+1];$final=$store.Load((Join-Path $SourcesRoot $next.name))
            foreach($receipt in $final.Receipts|Where-Object Revision -gt $snapshot.Revision){
                $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
                if($receipt.Principal-eq'TEST_ONLY.tac10-later-defender.v1'-and$command.Id.StartsWith('tac10.')){$result=$session.AdvanceAutomaticDefender()}
                elseif($command.Kind-in'AdvanceClock','EndFixedEncounter'){$result=$session.SubmitSessionCommand($command)}
                elseif($command.Kind-eq'UseIntimidatingPresence'-and$command.Actor-eq'TEST_ONLY.later-defender'){$result=$session.SubmitDefenderIntimidatingPresence([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
                elseif($command.Kind-eq'RespondSanctuary'-and$receipt.Principal-eq'TEST_ONLY.tac10-later-defender.v1'){$result=$session.SubmitDefenderSanctuary([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)}
                else{$seat=if($command.Actor-eq'TEST_ONLY.third-combatant'){'FirstOpponent'}elseif($command.Actor-eq'TEST_ONLY.recovery-defender'){'RecoveryOpponent'}else{'Player'};$result=$session.Submit($seat,$command)}
                Require ($result.Response-eq'Committed'-and$result.Revision-eq$receipt.Revision) "Wire112 continuation failed: $($receipt.Revision)"
                $count++
            }
            $name=$next.name+'.continued.ddsave';$session.Save((Join-Path $Run $name));$artifacts[$name]=Digest (Join-Path $Run $name)
            Require ($artifacts[$name]-ceq$next.sha256) "Wire112 continued state differs: $($next.name)"
            Capture-Views $session ($next.name+'.continued')
        }
        [ordered]@{role=$Role;checkpoints=$i+1;commands=$count}|ConvertTo-Json -Compress|Set-Content -LiteralPath (Join-Path $Run 'progress.json') -Encoding utf8
    }
    $rejected=0
    if($Role-eq'Current'){
        $bishop=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithDeclaredGeometry(
            [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
            [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
        $bishop.Save((Join-Path $Run 'bishop-before.ddsave'))
        foreach($mark in $marks){$failed=$false;try{$bishop.Restore((Join-Path $SourcesRoot $mark.name))}catch{$failed=$true};Require $failed 'Bishop silently upgraded wire112.';$rejected++}
        $bishop.Save((Join-Path $Run 'bishop-after.ddsave'))
        Require ((Digest (Join-Path $Run 'bishop-before.ddsave'))-ceq(Digest (Join-Path $Run 'bishop-after.ddsave'))) 'Cross-profile restore changed Bishop state.'
    }
    $report.status='PASS';$report.checkpoints=$marks.Count;$report.commands=$count;$report.artifacts=$artifacts;$report.newProfileRejections=$rejected
}catch{$report.error=$_.ToString()}
finally{Complete-GeometryExecutionBinding $Run $executionSourceBinding;$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
