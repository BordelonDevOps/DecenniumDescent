param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ResearchSave,
    [Parameter(Mandatory)][string]$Output
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$originalSave = Join-Path $PSScriptRoot '../2026-11-11-exp04-connected-observation/focused/saves/exp04-connected-observation-actual-later-entry.ddsave'
$t = [Decennium.Foundation.Tests.FoundationCases]
$f = [Reflection.BindingFlags]'NonPublic,Static'
$arguments = [object[]]::new(1)
$arguments[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$store = [Decennium.Foundation.FileSaveStore]::new()
$samples = foreach ($mode in 'accepted-wire93','connected-research') {
    $policy = $t.GetMethod('ConnectedObservationPolicy',$f).Invoke($null,$arguments)
    $path = $originalSave
    if ($mode -eq 'connected-research') {
        $null = $policy.EnableConnectedFormulaResearch()
        $path = $ResearchSave
    }
    $state = $store.Load($path)
    $sim = [Decennium.Foundation.Simulation]::new($policy,$state,[Decennium.Foundation.ExecutionProfile]::Laboratory)
    $kind = [Decennium.Foundation.CommandKind]::SelectCombatStance
    $knockout = [Decennium.Foundation.AttackKnockoutMode]::OrdinaryOutcome
    $press = [Decennium.Foundation.PressHitInstruction]::ArmOrReplace
    $command = $t.GetMethod('Tac',$f).Invoke($null,@($sim,$kind,$null,$null,0,0,'',$false,$knockout,1,$press))

    $timer = [Diagnostics.Stopwatch]::StartNew()
    [Decennium.Foundation.Validation]::Snapshot($state)
    $coreSeconds = $timer.Elapsed.TotalSeconds
    $timer.Restart()
    $validation = $policy.ValidateState($state)
    $policySeconds = $timer.Elapsed.TotalSeconds
    $timer.Restart()
    $resolution = $policy.Resolve($state.Copy(),$command)
    $resolveSeconds = $timer.Elapsed.TotalSeconds
    if ($validation -or $resolution) { throw "Validation or stance failed: $validation $resolution" }
    [ordered]@{profile=$mode;clock=$state.RuleClock.ToString();receipts=$state.Receipts.Length
        coreValidationSeconds=$coreSeconds;policyValidationSeconds=$policySeconds;stanceResolutionSeconds=$resolveSeconds
        saveSha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
}
[ordered]@{
    scope='Two single wall-clock samples while the headless regression was running. No controlled benchmark.'
    mechanism='The existing shared-world policy reconstructs Initial, replays all receipts, and compares canonical snapshot bytes during validation.'
    samples=@($samples)
} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $Output -Encoding utf8
