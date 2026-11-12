param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$PredecessorRoot,
    [Parameter(Mandatory)][string]$OutputRoot
)
$ErrorActionPreference = 'Stop'
$research = Join-Path $PSScriptRoot '../2026-11-12-mgt09-connected-formula-research'
& (Join-Path $research 'Verify-ConnectedResearchCompatibility.ps1') -AssemblyRoot $AssemblyRoot -OutputRoot $OutputRoot
$reportPath = Join-Path $OutputRoot 'results.json'
$report = Get-Content -LiteralPath $reportPath -Raw | ConvertFrom-Json -AsHashtable
$origins = Get-Content -LiteralPath (Join-Path $PredecessorRoot 'origin.json') -Raw | ConvertFrom-Json -AsHashtable
$bindings = Get-Content -LiteralPath (Join-Path $research 'BINDINGS.json') -Raw | ConvertFrom-Json -AsHashtable
if ($origins.sourceCommit -cne $bindings.implementationCommit) { throw 'Wrong predecessor assembly source' }
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$t = [Decennium.Foundation.Tests.FoundationCases]
$f = [Reflection.BindingFlags]'NonPublic,Static'
$profile = [Decennium.Foundation.ExecutionProfile]::Laboratory
$argsIn = [object[]]::new(1)
$argsIn[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$originalResearch = $t.GetMethod('ConnectedObservationPolicy',$f).Invoke($null,$argsIn).EnableConnectedFormulaResearch()
$specimenPolicy = $t.GetMethod('ConnectedObservationPolicy',$f).Invoke($null,$argsIn).EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen()
$shared = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]
function Hash([byte[]]$Data) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Data)).ToLowerInvariant()
}
function Restore-Old($Path,$Digest,$Wire,$Base,$Policy) {
    $bytes = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $Path).Path)
    if ((Hash $bytes) -cne $Digest -or [BitConverter]::ToInt32($bytes,4) -ne $Wire) {
        throw "Wrong authentic byte digest or wire: $Path"
    }
    $run = [Decennium.Foundation.Simulation]::new($Policy,$codec.Decode($bytes),$profile)
    $s = $run.Capture()
    if ($s.WireSchemaVersion -ne $Wire -or $s.SchemaVersion -ne $Base -or (Hash ($codec.Encode($s))) -cne $Digest -or $s.BloodSpecimen) {
        throw "Authentic round trip changed: $Path"
    }
    try {
        $null = [Decennium.Foundation.Simulation]::new($specimenPolicy,$codec.Decode($bytes),$profile)
        throw "Authentic old save accepted under specimen policy: $Path"
    } catch { if ($_.Exception.GetBaseException() -isnot [ArgumentException]) { throw } }
    return $run
}
foreach ($origin in $origins.saves) {
    $name = $origin.name
    $policy = switch ($name) {
        'wire75-mid-treatment' { $shared::WithHarvestPreservationTreatment([Decennium.Foundation.Laboratory.SharedHarvestFixture]::new(),[uint32]$origin.seed) }
        'wire76-clean-open' { $shared::WithHarvestPreservationExposure([Decennium.Foundation.Laboratory.SharedHarvestFixture]::new(),[uint32]$origin.seed) }
        'wire18-recipe14' { $t.GetMethod('Recipe14ManufacturePolicy',$f).Invoke($null,@([uint32]$origin.seed,$null,$null)) }
        default { throw "Unexpected predecessor $name" }
    }
    $run = Restore-Old (Join-Path $PredecessorRoot "$name.ddsave") $origin.sha256 $origin.wire $origin.base $policy
    $old = $run.Capture()
    $advance = switch ($origin.wire) { 75 { 1200 } 76 { 30 } 18 { 60 } }
    $null = $t.GetMethod('WorldAdvance',$f).Invoke($null,@($run,$advance,1))
    $next = $run.Capture()
    if ($origin.wire -eq 75 -and $next.HarvestPreservationTreatmentAttempts[0].Status.ToString() -cne 'Success') {
        throw 'Original fish treatment failed to finish after restore.'
    }
    if ($origin.wire -eq 76 -and (
        ![Decennium.Foundation.HarvestPreservationRules]::IsProtectedAt($old,$origin.target,$old.RuleClock) -or
        [Decennium.Foundation.HarvestPreservationRules]::IsProtectedAt($next,$origin.target,$next.RuleClock))) {
        throw 'Original fish opening did not expire at its actual boundary.'
    }
    if ($origin.wire -eq 18 -and $policy.BloodUnprotectedAge($next,'recipe-14',0).ToString() -cne '11644/1') {
        throw 'Original recipe-14 blood age changed.'
    }
    $report.authenticSaves += $origin + @{continuedAt=$next.RuleClock.ToString();continuedRevision=$next.Revision;wire94Rejected=$true}
}
foreach ($name in 'first-window-paused','continued') {
    $relative = "focused/saves/mgt09-connected-research-$name.ddsave"
    $run = Restore-Old (Join-Path $research $relative) $bindings.artifacts[$relative].sha256 93 90 $originalResearch
    $s = $run.Capture()
    if ($name -eq 'first-window-paused') {
        $control = $t.GetMethod('ResearchCommand',$f).Invoke($null,
            @($run,[Decennium.Foundation.CommandKind]::ResumeFormulaWork,$s.FormulaWork[0].Id,0,
                [Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId,'recipe-4'))
        $null = $t.GetMethod('LaterCommit',$f).Invoke($null,@($run,$control))
        $null = $t.GetMethod('WorldAdvance',$f).Invoke($null,@($run,11584,1))
        if ($run.Capture().FormulaWork[0].Status.ToString() -cne 'Success') { throw 'Authentic paused research failed to finish.' }
    }
    $report.authenticSaves += [ordered]@{path=$relative;wire=93;base=90;sha256=$bindings.artifacts[$relative].sha256
        time=$s.RuleClock.ToString();revision=$s.Revision;continuedAt=$run.Capture().RuleClock.ToString();wire94Rejected=$true}
}
$report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $reportPath -Encoding utf8
