param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputRoot
)
$ErrorActionPreference = 'Stop'
$hideRoot = Join-Path $PSScriptRoot '../2026-11-11-exp04-exploration-hide'
& (Join-Path $hideRoot 'Verify-ExplorationHideCompatibility.ps1') -AssemblyRoot $AssemblyRoot -OutputRoot $OutputRoot
$reportPath = Join-Path $OutputRoot 'results.json'
$report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json -AsHashtable
$hideManifest = Get-Content -LiteralPath (Join-Path $hideRoot 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$tests = [Decennium.Foundation.Tests.FoundationCases]
function Hash([byte[]]$Data) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Data)).ToLowerInvariant() }
function Restore-Old([string]$Path,[string]$Digest,[int]$Wire,[int]$Base,$Policy) {
    $raw = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $Path).Path)
    if ((Hash $raw) -cne $Digest -or [BitConverter]::ToInt32($raw,4) -ne $Wire) { throw "Authentic bytes differ: $Path" }
    $run = [Decennium.Foundation.Simulation]::new($Policy,$codec.Decode($raw),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $s = $run.Capture()
    if ($s.WireSchemaVersion -ne $Wire -or $s.SchemaVersion -ne $Base -or (Hash ($codec.Encode($s))) -cne $Digest) {
        throw "The authentic predecessor no longer roundtrips exactly: $Path"
    }
    [ordered]@{run=$run;entry=[ordered]@{path=$Path;wire=$Wire;base=$Base;sha256=$Digest;bytes=$raw.Length
        time=$s.RuleClock.ToString();revision=$s.Revision}}
}

$laterPath = 'docs/unity/evidence/2026-11-11-exp07-later-encounter/focused/run-20261111T175357019Z-a31272fd/saves/exp07_later_encounter_connected_arrival_and_fractional_replay/exp07-later-before-entry.ddsave'
$oldLater = $tests.GetMethod('LaterPolicy',$flags).Invoke($null,@($null,$null))
$legacy = Restore-Old $laterPath '325db7684c31094979cd3e543388abf0f1b17dbfdf105b8027e904b63541b921' 86 86 $oldLater
if ($legacy.run.Capture().ExplorationHide -or $legacy.run.Capture().ExplorationSearch) { throw 'Wire86 acquired ordinary observation.' }
$report.authenticSaves += $legacy.entry

$oldHide = $tests.GetMethod('ExplorationHidePolicy',$flags).Invoke($null,
    @([uint32]2,$false,5,[Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()))
$hideRelative = 'focused/saves/exp04-hide-restore-partial.ddsave'
$wire92 = Restore-Old (Join-Path $hideRoot $hideRelative) $hideManifest.artifacts[$hideRelative].sha256 92 51 $oldHide
if (-not $wire92.run.Capture().ExplorationHide.Pending) { throw 'The authentic Hide was not pending after restore.' }
$advance = $tests.GetMethod('SearchAdvance',$flags).Invoke($null,@($wire92.run,18,1))
$after = $wire92.run.Capture()
$actual = $after.ObservationActions[-1]
if ($advance.ReachedClock.ToString() -cne '36/1' -or $actual.Kind.ToString() -cne 'Hide' -or
    $actual.Natural -ne 6 -or $actual.WordsConsumed -ne 1 -or $after.ExplorationHide.Pending) {
    throw 'Authentic pending wire92 Hide failed to continue through the original ordinary window.'
}
$wire92.entry.continued = [ordered]@{at=$after.RuleClock.ToString();revision=$after.Revision;natural=$actual.Natural
    words=$actual.WordsConsumed;kind=$actual.Kind.ToString()}
$report.authenticSaves += $wire92.entry
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $reportPath -Encoding utf8
