param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Saves,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
$assemblies = @(foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    $path = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $path
    [ordered]@{name=Split-Path -Leaf $path;sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
})
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$companion = [Decennium.Foundation.ConnectedExplorationObservation]::Searcher
function Call([string]$Name,[object[]]$Arguments) {
    try { $tests.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
function Hash([byte[]]$Data) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Data)).ToLowerInvariant() }
function Restore([string]$Name) {
    $path = Join-Path $Saves "exp04-connected-observation-$Name.ddsave"
    $bytes = [IO.File]::ReadAllBytes($path)
    $arguments = [object[]]::new(1)
    $arguments[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
    $policy = Call 'ConnectedObservationPolicy' $arguments
    $simulation = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($bytes),[Decennium.Foundation.ExecutionProfile]::Laboratory)
    if ((Hash ($codec.Encode($simulation.Capture()))) -cne (Hash $bytes)) { throw "Save changed during restore: $Name" }
    $simulation
}

$before = (Restore 'reinforcement-before-admission').Capture()
if ($before.Reinforcement.Admission -or -not ($before.WorldActivityIntervals | Where-Object ActorId -CEQ $companion)) {
    throw 'Negative control requires the existing lawful off-calendar allowance before admission.'
}
$before.WorldActivityIntervals = [Decennium.Foundation.WorldActivityIntervalRecord[]]@(
    $before.WorldActivityIntervals | Where-Object ActorId -CNE $companion)
$negative = ''
try { $null = $codec.Encode($before) } catch [ArgumentException] { $negative = $_.Exception.GetBaseException().Message }
if (-not $negative) { throw 'Unexplained removal of the current allowance was accepted.' }

$sim = Restore 'reinforcement-search-history-retained'
$replay = Restore 'reinforcement-search-history-retained'
$admitted = $sim.Capture()
$owner = [Decennium.Foundation.WorldTiming]::ForActor($admitted,$companion)
$phase = $admitted.Reinforcement.Admission.Phase
if ($owner.Id -cne $phase.Epoch.Id -or ($admitted.WorldActivityIntervals | Where-Object ActorId -CEQ $companion)) {
    throw 'The companion did not receive the actual new owner and retire its old row.'
}
$search = $admitted.ExplorationSearch.Attempts[0]
$receipt = $admitted.Receipts | Where-Object Revision -EQ $search.Revision
$paidMarker = [Decennium.Foundation.CommandHistory]::Read($receipt).Target
$finishedAttempt = $admitted.MiningAttempts[0]
$deposit = $admitted.MiningDeposits | Where-Object Id -CEQ $finishedAttempt.DepositId
$category = $admitted.MiningCategories | Where-Object {$_.DepositId -ceq $deposit.Id -and $_.Accessible} | Select-Object -First 1
$selection = [Decennium.Foundation.MiningSelectionRequest]::new($deposit.VersionId,[string[]]@($category.Id),
    [Decennium.Foundation.MiningAbilityChoice]::Wisdom,$false,'','','')
$hostAuthority = Call 'LaterHost' @()
foreach ($run in $sim,$replay) {
    $beforeQuery = Hash ($codec.Encode($run.Capture()))
    $command = Call 'MiningCommand' @($run,[Decennium.Foundation.CommandKind]::StartMining,$deposit.Id,$selection,$companion,$null)
    $query = $run.QueryCommand($hostAuthority,$command)
    $execution = $run.Execute($hostAuthority,$command)
    if (-not $query.Supported -or $query.Admissible -or $query.Code -cne 'MiningDepositClaimClosed' -or
        $execution.Outcome.ToString() -cne 'Rejected' -or $execution.Code -cne $query.Code -or
        (Hash ($codec.Encode($run.Capture()))) -cne $beforeQuery) {
        throw "Current work assessment did not reach the existing claimed-deposit rule: $($query.Code), $($execution.Code)"
    }
    $null = Call 'EndReinforcementTurn' @($run,[Decennium.Foundation.CombatStance]::Guarded)
}
$after = $sim.Capture()
$afterBytes = $codec.Encode($after)
if ($after.RuleClock -le $admitted.RuleClock -or (Hash $afterBytes) -cne (Hash ($codec.Encode($replay.Capture()))) -or
    $after.ExplorationSearch.Attempts[0].End.ObservationId -cne $search.End.ObservationId) {
    throw 'Replay after the roster change diverged or changed the historical Search.'
}
[ordered]@{status='PASS';assemblies=$assemblies;genuineAdmissionAt=$admitted.RuleClock.ToString();currentOwner=$owner.Id
    retiredOldRow=$true;historicalSearch=[ordered]@{declaration=$search.CommandId;paidMarker=$paidMarker;result=$search.End.ObservationId}
    currentWork=[ordered]@{actor=$companion;deposit=$deposit.Id;category=$category.Id;query=$query.Code;execution=$execution.Code}
    unexplainedMissingRowRejected=$negative
    identicalContinuation=[ordered]@{at=$after.RuleClock.ToString();revision=$after.Revision;sha256=Hash $afterBytes}} |
    ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputFile -Encoding utf8
