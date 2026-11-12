param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$PaidSearchSave,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference='Stop'
$assemblies = @(foreach ($n in 'Core','Persistence','LabModel','HeadlessTests') {
    $path = Join-Path $AssemblyRoot "Decennium.Foundation.$n.dll"
    Add-Type -Path $path
    [ordered]@{name=Split-Path -Leaf $path;sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
})
$t=[Decennium.Foundation.Tests.FoundationCases]
$f=[Reflection.BindingFlags]'NonPublic,Static'
function Call([string]$Name,[object[]]$ArgsIn) {
 try { $t.GetMethod($Name,$f).Invoke($null,$ArgsIn) } catch { throw $_.Exception.GetBaseException() }
}
$argsForFixture=[object[]]::new(1)
$argsForFixture[0]=[Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$p=Call 'ConnectedObservationPolicy' $argsForFixture
$c=[Decennium.Foundation.SnapshotCodec]::new()
$raw=[IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $PaidSearchSave).Path)
$run=[Decennium.Foundation.Simulation]::new($p,$c.Decode($raw),[Decennium.Foundation.ExecutionProfile]::Laboratory)
$null=Call 'SearchAdvance' @($run,18,1)
$null=Call 'PlanWalk' @($run,0,1,[Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId)
$null=Call 'StageReinforcingCompanion' @($run)
$null=Call 'ReturnToConnectedApproach' @($run)
$entry=Call 'EnterLater' @($run)
$command=Call 'ReinforcementCommand' @($run,[Decennium.Foundation.CommandKind]::BeginReinforcementApproach,[Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId)
$null=Call 'LaterCommit' @($run,$command)
$first = Call 'EndReinforcementTurn' @($run,[Decennium.Foundation.CombatStance]::Guarded)
$afterFirst = $run.Capture()
$reason = ''
try { $null = Call 'EndReinforcementTurn' @($run,[Decennium.Foundation.CombatStance]::Guarded) }
catch { $reason = $_.Exception.Message }
$afterSecond = $run.Capture()
if ($reason -cne 'EndRegularTurn failed: InvalidResult' -or $afterSecond.Reinforcement.Admission -or
    $afterFirst.RuleClock.ToString() -cne '23353/2' -or $afterSecond.RuleClock -ne $afterFirst.RuleClock) {
    throw "The exact rejected admission was not reproduced: $reason"
}
[ordered]@{status='REPRODUCED';source='2b12ec6fcd1cef4e520d93f4ad2440b26abdf4bf';assemblies=$assemblies
    savedInput=(Get-FileHash -LiteralPath $PaidSearchSave).Hash.ToLowerInvariant()
    genuineEntry=$entry.Epoch.Origin.ToString();firstEnd=$first.Id;afterFirst=$afterFirst.RuleClock.ToString()
    secondEnd=$reason;afterSecond=$afterSecond.RuleClock.ToString();admissionCommitted=$false} |
    ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputFile -Encoding utf8
