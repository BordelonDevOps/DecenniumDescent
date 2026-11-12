param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputRoot
)
$ErrorActionPreference = 'Stop'
$searchRoot = Join-Path $PSScriptRoot '../2026-11-11-exp04-exploration-search'
& (Join-Path $searchRoot 'Verify-ExplorationSearchCompatibility.ps1') -AssemblyRoot $AssemblyRoot -OutputRoot $OutputRoot
$reportPath = Join-Path $OutputRoot 'results.json'
$report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json -AsHashtable
$manifest = Get-Content -LiteralPath (Join-Path $searchRoot 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$flags = [Reflection.BindingFlags]'Static,NonPublic'
$fixture = [Decennium.Foundation.Tests.FoundationCases].GetMethod('ExplorationSearchPolicy',$flags)
$events = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$policy = $fixture.Invoke($null,@($true,5,$events))
$paths = @('focused/saves/exp04-search-wire91-control.ddsave','focused/saves/exp04-search-paid-pending.ddsave')
foreach ($name in $paths) {
    $path = Join-Path $searchRoot $name
    $raw = [IO.File]::ReadAllBytes($path)
    $sha = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($raw)).ToLowerInvariant()
    if ($sha -cne $manifest.artifacts[$name].sha256 -or [BitConverter]::ToInt32($raw,4) -ne 91) {
        throw "Published wire91 bytes changed: $name"
    }
    $simulation = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($raw),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $s = $simulation.Capture()
    $encoded = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($s))).ToLowerInvariant()
    if ($encoded -cne $sha -or $s.WireSchemaVersion -ne 91 -or $s.SchemaVersion -ne 51 -or $s.ExplorationHide) {
        throw "Authentic wire91 did not roundtrip under the predecessor policy: $name"
    }
    $entry = [ordered]@{path=$name;wire=91;base=51;sha256=$sha;bytes=$raw.Length;time=$s.RuleClock.ToString();revision=$s.Revision}
    if ($s.ExplorationSearch.Pending) {
        $fixtureTests = [Decennium.Foundation.Tests.FoundationCases]
        $advance = $fixtureTests.GetMethod('SearchAdvance',$flags).Invoke($null,@($simulation,12,1))
        $after = $simulation.Capture()
        $search = $after.ObservationActions[-1]
        if ($advance.ReachedClock.ToString() -cne '36/1' -or $search.Natural -ne 6 -or $search.WordsConsumed -ne 1 -or
            $search.Outcome.ToString() -cne 'SearchNoFinding' -or $after.ExplorationSearch.Pending) {
            throw 'The authentic pending predecessor Search did not continue through its original rules.'
        }
        $entry.continued = [ordered]@{at=$after.RuleClock.ToString();revision=$after.Revision;natural=$search.Natural
            words=$search.WordsConsumed;outcome=$search.Outcome.ToString()}
    }
    $report.authenticSaves += $entry
}
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $reportPath -Encoding utf8
