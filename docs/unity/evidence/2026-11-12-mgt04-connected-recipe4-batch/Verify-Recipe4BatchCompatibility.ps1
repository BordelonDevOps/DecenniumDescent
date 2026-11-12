param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$PredecessorRoot,
    [Parameter(Mandatory)][string]$OutputRoot
)
$ErrorActionPreference = 'Stop'
$old = Join-Path $PSScriptRoot '../2026-11-12-mgt05-black-blood-handoff'
& (Join-Path $old 'Verify-BloodSpecimenCompatibility.ps1') -AssemblyRoot $AssemblyRoot `
    -PredecessorRoot (Join-Path $old 'legacy-saves/inputs') -OutputRoot $OutputRoot
$reportPath = Join-Path $OutputRoot 'results.json'
$report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json -AsHashtable
$bindings = Get-Content -LiteralPath (Join-Path $old 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
$origins = Get-Content -LiteralPath (Join-Path $PredecessorRoot 'origin.json') -Raw | ConvertFrom-Json -AsHashtable
if ($origins.sourceCommit -cne $bindings.implementationCommit) { throw 'Unexpected authentic save origin.' }
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$profile = [Decennium.Foundation.ExecutionProfile]::Laboratory
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
function Call-Test([string]$Name,[object[]]$Arguments) {
    try { $tests.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
$arguments = [object[]]::new(1)
$arguments[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$wire94 = (Call-Test 'ConnectedObservationPolicy' $arguments).EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen()
$wire95 = (Call-Test 'ConnectedObservationPolicy' $arguments).EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen().EnableConnectedRecipe4Batch()
function Digest([byte[]]$bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}
function Restore([string]$File,[string]$Hash,[int]$Wire,$Policy) {
    $bytes = [IO.File]::ReadAllBytes($File)
    if ((Digest $bytes) -cne $Hash -or [BitConverter]::ToInt32($bytes,4) -ne $Wire) { throw "Incorrect authentic save $File" }
    $sim = [Decennium.Foundation.Simulation]::new($Policy,$codec.Decode($bytes),$profile)
    $state = $sim.Capture()
    if ($state.ConnectedBatch -or (Digest ($codec.Encode($state))) -cne $Hash) { throw "Prior save changed $File" }
    try {
        $null = [Decennium.Foundation.Simulation]::new($wire95,$codec.Decode($bytes),$profile)
        throw "Wire 95 accepted predecessor $File"
    } catch { if ($_.Exception.GetBaseException() -isnot [ArgumentException]) { throw } }
    return $sim
}
foreach ($origin in $origins.saves) {
    $seed = [uint32]$origin.seed
    $policy = if ($origin.wire -eq 18) { Call-Test 'ManufacturePolicy' @($seed,$null,$null,$null) }
        else { Call-Test 'ResolvedPolicy' @($seed) }
    $sim = Restore (Join-Path $PredecessorRoot $origin.file) $origin.sha256 $origin.wire $policy
    $null = Call-Test 'WorldAdvance' @($sim,13200,1)
    if ($sim.Capture().ManufacturingOrders[0].Status.ToString() -cne 'AwaitingChoice') { throw 'Prior live quality check changed.' }
    $null = Call-Test 'ManufactureChoice' @($sim,[Decennium.Foundation.CraftQualityChoice]::Durability,-1)
    $next = $sim.Capture()
    if ($next.AlchemyDoses.Length -ne 5 -or $next.ManufacturingOrders[0].Natural -ne 12 -or $next.WireSchemaVersion -ne $origin.wire) {
        throw 'Prior genuine batch output changed.'
    }
    $report.authenticSaves += $origin + @{continuedAt=$next.RuleClock.ToString();doses=$next.AlchemyDoses.Length;wire95Rejected=$true}
}
$wire94Saves = @($bindings.artifacts.Keys | Where-Object { $_ -clike 'focused/saves/*.ddsave' } | Sort-Object)
if ($wire94Saves.Count -ne 10) { throw 'The accepted wire 94 inventory must contain ten saves.' }
foreach ($relative in $wire94Saves) {
    $sim = Restore (Join-Path $old $relative) $bindings.artifacts[$relative].sha256 94 $wire94
    $state = $sim.Capture()
    if ($relative -clike '*-cutoff.ddsave') {
        $null = Call-Test 'WorldAdvance' @($sim,900,1)
        $specimen = $null
        $null = [Decennium.Foundation.HarvestPreservationRules]::TryProject($sim.Capture(),$state.BloodSpecimen.LotId,[ref]$specimen)
        if ($specimen.UnprotectedAge.ToString() -cne '14279/1' -or $sim.Capture().ManufacturingOrders.Length -ne 0) {
            throw 'The authentic wire 94 assessment-only handoff changed on continuation.'
        }
    }
    $report.authenticSaves += [ordered]@{path=$relative;wire=94;base=90;sha256=$bindings.artifacts[$relative].sha256
        time=$state.RuleClock.ToString();revision=$state.Revision;continuedAt=$sim.Capture().RuleClock.ToString();wire95Rejected=$true}
}
if ($report.authenticSaves.Count -ne 25) { throw 'Unexpected authentic save total.' }
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $reportPath -Encoding utf8
