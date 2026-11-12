param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputRoot
)
$ErrorActionPreference = 'Stop'
$observation = Join-Path $PSScriptRoot '../2026-11-11-exp04-connected-observation'
& (Join-Path $observation 'Verify-ConnectedObservationCompatibility.ps1') -AssemblyRoot $AssemblyRoot -OutputRoot $OutputRoot
$reportPath = Join-Path $OutputRoot 'results.json'
$report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json -AsHashtable
$bindings = Get-Content -LiteralPath (Join-Path $observation 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
$t = [Decennium.Foundation.Tests.FoundationCases]
$f = [Reflection.BindingFlags]'NonPublic,Static'
$arguments = [object[]]::new(1)
$arguments[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$original = $t.GetMethod('ConnectedObservationPolicy',$f).Invoke($null,$arguments)
$selected = $t.GetMethod('ConnectedObservationPolicy',$f).Invoke($null,$arguments).EnableConnectedFormulaResearch()
$authority = $t.GetMethod('LaterHost',$f).Invoke($null,@())
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$profile = [Decennium.Foundation.ExecutionProfile]::Laboratory
function Hash([byte[]]$Data) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Data)).ToLowerInvariant()
}
foreach ($name in 'before-observation','actual-later-entry') {
    $relative = "focused/saves/exp04-connected-observation-$name.ddsave"
    $path = Join-Path $observation $relative
    $bytes = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $path).Path)
    $digest = Hash $bytes
    if ($digest -cne $bindings.artifacts[$relative].sha256) { throw "Authentic wire93 bytes changed: $name" }
    $run = [Decennium.Foundation.Simulation]::new($original,$codec.Decode($bytes),$profile)
    $s = $run.Capture()
    if ((Hash ($codec.Encode($s))) -cne $digest -or $s.WireSchemaVersion -ne 93 -or $s.SchemaVersion -ne 90) {
        throw "Original wire93 compatibility failed: $name"
    }
    $rejected = $false
    try {
        $null = [Decennium.Foundation.Simulation]::new($selected,$codec.Decode($bytes),$profile)
    } catch {
        if ($_.Exception.GetBaseException() -isnot [ArgumentException]) { throw }
        $rejected = $true
    }
    if (!$rejected) { throw "Original wire93 was incorrectly accepted by the research selection: $name" }
    $command = [Decennium.Foundation.Command]::new('old-wire93.research',[Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId,
        $s.Revision,[Decennium.Foundation.CommandKind]::StartFormulaResearch,[Decennium.Foundation.Laboratory.SharedResearchFixture]::Evidence)
    $denial = $run.Execute($authority,$command)
    if ($denial.Code -ne 'FormulaWorkNotSelected' -or (Hash ($codec.Encode($run.Capture()))) -cne $digest) {
        throw "Authentic wire93 acquired research behavior: $name"
    }
    $report.authenticSaves += [ordered]@{path=$relative;wire=93;base=90;sha256=$digest;bytes=$bytes.Length;time=$s.RuleClock.ToString()
        revision=$s.Revision;selectedProfileRejected=$rejected;originalResearchCommand=$denial.Code}
}
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $reportPath -Encoding utf8
