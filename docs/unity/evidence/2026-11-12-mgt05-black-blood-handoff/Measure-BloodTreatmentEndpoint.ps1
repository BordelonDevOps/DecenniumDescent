param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$worker = [Decennium.Foundation.ConnectedBloodSpecimen]::Worker
$ruleTime = [Decennium.Foundation.RuleTime]
$stamp = [Decennium.Foundation.ConditionStamp]
$kind = [Decennium.Foundation.CommandKind]
$codec = [Decennium.Foundation.SnapshotCodec]::new()
function Call-Test([string]$Name,[object[]]$Arguments) {
    try { $tests.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
$runs = @(foreach ($expiry in 13379,13380) {
    $poison = Call-Test 'CCApply' @('blood-endpoint-poison','Poisoned',$worker,$stamp::new($ruleTime::new($expiry),0),
        $stamp::new($ruleTime::new(11578),0),$null)
    $argsIn = [object[]]::new(1)
    $argsIn[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@($poison)
    $policy = (Call-Test 'ConnectedObservationPolicy' $argsIn).EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen()
    $simulation = Call-Test 'LaterPrepared' @($policy)
    if ($simulation.Capture().RuleClock -ne $ruleTime::new(11578)) { throw 'Unexpected ordinary preparation clock.' }
    $null = Call-Test 'LaterCommit' @($simulation,(Call-Test 'CCCommand' @($simulation,'blood-endpoint-poison',$worker)))
    $null = Call-Test 'LaterCommit' @($simulation,(Call-Test 'BloodVesselCommand' @($simulation,$kind::OpenPortableContainer,$null)))
    $null = Call-Test 'LaterCommit' @($simulation,(Call-Test 'BloodTreatmentCommand' @($simulation)))
    $before = $simulation.Capture()
    $null = Call-Test 'WorldAdvance' @($simulation,1800,1)
    $after = $simulation.Capture()
    $attempt = $after.HarvestPreservationTreatmentAttempts[0]
    $first = [Decennium.Foundation.DiceStream]::Draw($before.RandomState,20)
    $second = [Decennium.Foundation.DiceStream]::Draw($first.NextState,20)
    $withDisadvantage = $expiry -gt 13379
    $natural = if ($withDisadvantage) { [Math]::Min($first.Value,$second.Value) + 1 } else { $first.Value + 1 }
    $words = if ($withDisadvantage) { $first.WordsConsumed + $second.WordsConsumed } else { $first.WordsConsumed }
    $next = if ($withDisadvantage) { $second.NextState } else { $first.NextState }
    if ($after.RuleClock -ne $ruleTime::new(13379) -or $attempt.Natural -ne $natural -or
        $attempt.RandomWordsConsumed -ne $words -or $after.RandomState -ne $next -or
        $attempt.Work.Labor -ne $ruleTime::new(1800)) { throw 'Treatment check did not use endpoint condition state.' }
    $bytes = $codec.Encode($after)
    $roundTrip = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($bytes),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $digest = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
    $replayed = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($roundTrip.Capture()))).ToLowerInvariant()
    if ($digest -cne $replayed) { throw 'Endpoint result changed on restore.' }
    [ordered]@{poisonExpiry=$expiry; starts=$before.RuleClock.ToString(); completes=$after.RuleClock.ToString()
        disadvantage=$withDisadvantage; natural=$attempt.Natural; status=$attempt.Status.ToString()
        rngBefore=$attempt.RandomBefore; rngAfter=$attempt.RandomAfter; consumedWords=$attempt.RandomWordsConsumed; replaySha256=$digest}
})
@{status='PASS'; endpoint=$runs} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding utf8
