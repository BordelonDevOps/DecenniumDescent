param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Save,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Save=(Resolve-Path -LiteralPath $Save).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh evidence export directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$report=[ordered]@{status='FAIL';scope='Read-only structural evidence export of the separately verified actual final save; no gameplay execution or additional replay claim';assemblies=@()}
try {
    foreach($name in 'Core','Persistence'){
        $path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path
        $report.assemblies+=@{name=$name;sha256=(Digest $path)}
    }
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Export-FerryContinuation.executed.ps1')
    $report.input=@{path=$Save;sha256=(Digest $Save)}
    $codec=[Decennium.Foundation.SnapshotCodec]::new();$bytes=[IO.File]::ReadAllBytes($Save);$state=$codec.Decode($bytes)
    if([Convert]::ToBase64String($bytes)-cne[Convert]::ToBase64String($codec.Encode($state))){throw 'Structural decode/encode changed the input.'}
    $all=@($state.Receipts|ForEach-Object {[ordered]@{receipt=$_;command=[Decennium.Foundation.CommandHistory]::Read($_)}})
    $all|ConvertTo-Json -Depth 70|Set-Content -LiteralPath (Join-Path $Run 'all-command-receipts.json') -Encoding utf8
    @($all|Where-Object {$_.receipt.Revision-gt365})|ConvertTo-Json -Depth 70|Set-Content -LiteralPath (Join-Path $Run 'selected-continuation-commands.json') -Encoding utf8
    [ordered]@{actors=$state.Actors;lives=$state.Lives;rp=$state.ResonancePools;ferry=$state.FerryWraith;closures=$state.ClosedEncounters;knownSpells=$state.KnownSpells;typedDamage=$state.TypedDamage;healingRites=$state.HealingRites;worldIntervals=$state.WorldIntervals;worldActivities=$state.WorldActivityIntervals;clubs=$state.Clubs}|ConvertTo-Json -Depth 70|Set-Content -LiteralPath (Join-Path $Run 'final-private-evidence.json') -Encoding utf8
    if($state.Revision-ne462-or$all.Count-ne462-or@($all|Where-Object {$_.receipt.Revision-gt365}).Count-ne97){throw 'Unexpected actual continuation history length.'}
    if((Digest $Save)-cne$report.input.sha256){throw 'Read-only export changed the save.'}
    $report.finalRevision=$state.Revision;$report.allCommands=$all.Count;$report.selectedCommands=97
    $report.status='PASS_READ_ONLY_ACTUAL_CONTINUATION_EXPORT'
} catch {$report.error=$_.Exception.ToString()}
$report|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
