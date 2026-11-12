param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
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
$hero = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::ActorId
$companion = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId
$enemy = [Decennium.Foundation.Laboratory.AdditionalTacticalActor]::Id
$buyer = 'TEST_ONLY.haven-copper-buyer'
$defender = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::LaterDefenderId
$ids = @($hero,$companion,$enemy,$buyer,$defender)
$profiles = [Decennium.Foundation.Laboratory.ObservationSightProfile[]]@($ids | ForEach-Object {
    [Decennium.Foundation.Laboratory.ObservationSightProfile]::new($_,30,30)
})
$cells = [Decennium.Foundation.Laboratory.ObservationGridCell[]]@(
    [Decennium.Foundation.Laboratory.ObservationGridCell]::new(2,1,$true,$false,$false,$false))
$map = [Decennium.Foundation.Laboratory.ObservationFixture]::new(5,5,$cells,$profiles)
$codec = [Decennium.Foundation.SnapshotCodec]::new()
function Call([string]$Name,[object[]]$Arguments) {
    try { $tests.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
function Require([bool]$Condition,[string]$Message) { if (-not $Condition) { throw $Message } }
function Hash([byte[]]$Data) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Data)).ToLowerInvariant() }
function Walk($Simulation,[string]$Actor,[int]$X,[int]$Y) { $null = Call 'PlanWalk' @($Simulation,$X,$Y,$Actor) }
function Where-Is($State,[string]$Actor) {
    $position = $State.Actors | Where-Object Id -CEQ $Actor
    @($position.X,$position.Y)
}
function Sees($State,[string]$Observer,[string]$Target) {
    [Decennium.Foundation.Laboratory.ObservationRules]::CanSee($State,$Observer,$Target)
}
function Hidden-To($State,[string]$Observer,[string]$Target) {
    [Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($State,$Observer,$Target)
}
function Actor-At($State,[string]$Actor,[int]$X,[int]$Y) {
    ($State.Actors | Where-Object Id -CEQ $Actor | Where-Object {$_.X -eq $X -and $_.Y -eq $Y}).Count -eq 1
}

$policy = Call 'SurprisePolicy' @([Decennium.Foundation.SurpriseAwareness]::Warned,$null)
$null = $policy.EnableObservation($map)
$gate = ''
try { $null = $policy.EnableExplorationSearch() }
catch [InvalidOperationException] { $gate = $_.Exception.GetBaseException().Message }
Require ($gate -ceq 'Select ordinary Search on the independent exact-observation host before initialization.') 'Expected composition gate was not observed.'

$sim = Call 'LaterPrepared' @($policy)
$prepared = $sim.Capture()
Require ($prepared.WireSchemaVersion -eq 90 -and $prepared.SchemaVersion -eq 90 -and $prepared.ObservationMapWidth -eq 5 -and
    $prepared.ObservationActions.Count -eq 0 -and -not $prepared.ExplorationSearch -and -not $prepared.ExplorationHide -and
    $prepared.CharterAttempt.Outcome.ToString() -ceq 'ReturnedComplete' -and $prepared.LaterEncounter.FirstExit -and
    $prepared.LaterEncounter.FirstExit.ClosedAt.ToString() -ceq '15/1' -and $prepared.HavenSales[0].Status.ToString() -ceq 'Paid' -and
    $prepared.HavenMealPurchases.Count -eq 1 -and $prepared.ExpeditionBills[0].Status.ToString() -ceq 'Reconciled' -and
    -not $prepared.LaterEncounter.Entry -and -not $prepared.SurpriseEntry.Decision) 'The accepted connected preparation did not run.'

Walk $sim $companion -1 0
Walk $sim $companion 0 -1
Walk $sim $hero 0 -1
Walk $sim $hero 0 -1
Walk $sim $hero 0 -1
$null = Call 'WorldAdvance' @($sim,2,1)
$window = $sim.Capture()
$schedule = $window.WorldSchedule
$scheduled = $window.WorldIntervals | Where-Object ActorId -CEQ $hero
$activity = $window.WorldActivityIntervals | Where-Object ActorId -CEQ $companion
$due = $schedule.Start($scheduled.LastStart + $schedule.Order.Count)
Require ((Actor-At $window $hero 1 0) -and (Actor-At $window $companion 3 2) -and (Actor-At $window $buyer 2 4) -and
    -not (Sees $window $companion $hero) -and (Sees $window $buyer $hero) -and
    -not (Hidden-To $window $companion $hero) -and -not (Hidden-To $window $buyer $hero) -and
    -not $scheduled.ActionSpent -and $scheduled.LastStart -eq 3870 -and
    $activity.Action.ToString() -ceq 'None' -and $activity.IntervalIndex -eq 1935 -and
    $window.RuleClock.ToString() -ceq '11610/1' -and $due.ToString() -ceq '11616/1' -and
    $schedule.Start($scheduled.LastStart) -eq $window.RuleClock -and
    [Decennium.Foundation.WorldActivityIntervalRecord]::StartAt($schedule,$activity.IntervalIndex) -eq $window.RuleClock) 'The actual ordinary window lost its geometry or two original Action owners.'

$geometry = [Decennium.Foundation.Laboratory.ObservationGeometry].GetMethod('GeometricSight',$flags)
$point = $geometry.GetParameters()[2].ParameterType.GetConstructors([Reflection.BindingFlags]'Instance,NonPublic')[0]
function Grid-Point([int]$X,[int]$Y) {
    $point.Invoke(@([Decennium.Foundation.RuleQuantity]::new($X,1),[Decennium.Foundation.RuleQuantity]::new($Y,1)))
}
$cueVisible = $geometry.Invoke($null,@($window,$companion,(Grid-Point 3 2),(Grid-Point 3 1)))
Require $cueVisible 'The selected visual fringe is not actually visible from the companion anchor.'

$readyBytes = $codec.Encode($window)
$restored = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($readyBytes),[Decennium.Foundation.ExecutionProfile]::Laboratory)
Require ((Hash ($codec.Encode($restored.Capture()))) -ceq (Hash $readyBytes)) 'The observation-enabled predecessor does not restore exactly.'
Walk $restored $hero 1 0
$alternate = $restored.Capture()
Require ((Actor-At $alternate $hero 2 0) -and -not (Sees $alternate $companion $hero) -and
    -not (Sees $alternate $buyer $hero) -and $alternate.RandomState -eq $window.RandomState) 'Actual movement did not reach the alternate hiding position outside both sight lines.'
Walk $restored $hero -1 0
$returned = $restored.Capture()
Require ((Actor-At $returned $hero 1 0) -and -not (Sees $returned $companion $hero) -and
    (Sees $returned $buyer $hero) -and -not (Hidden-To $returned $companion $hero)) 'The actual return did not restore the authored sight relationships.'
foreach ($y in 1..3) { Walk $restored $hero 0 1 }
$beforeApproach = $restored.Capture()
$approachActivity = $beforeApproach.WorldActivityIntervals | Where-Object ActorId -CEQ $companion
$approachDue = [Decennium.Foundation.WorldActivityIntervalRecord]::EndAt($beforeApproach.WorldSchedule,$approachActivity.IntervalIndex)
$entry = Call 'EnterLater' @($restored)
$entered = $restored.Capture()
Require ((Actor-At $beforeApproach $hero 1 3) -and (Actor-At $entered $hero 0 3) -and $entered.InventoryCombat -and
    $approachActivity.Action.ToString() -ceq 'None' -and $beforeApproach.RuleClock.ToString() -ceq '11640/1' -and
    $approachDue.ToString() -ceq '11646/1' -and $entry.Epoch.Origin -lt $approachDue -and
    $entered.SurpriseEntry.Binding.Outcome.ToString() -ceq 'Warned' -and $entered.SurpriseEntry.Decision -and
    -not $entered.SurpriseEntry.SurprisePending -and $entry.Epoch.Id -ceq 'TEST_ONLY.later-calendar' -and
    $companion -cnotin $entry.Epoch.Order -and (Sees $entered $hero $defender) -and (Sees $entered $defender $hero)) 'The actual later entry lost the independent Warned authority, sight or roster.'
$null = Call 'FinishLaterFight' @($restored,$false)
Walk $restored $hero 1 0
$continued = $restored.Capture()
$ownerAfterExit = [Decennium.Foundation.WorldTiming]::ForActor($continued,$hero)
Require (-not $continued.InventoryCombat -and $continued.ClosedEncounters.Count -eq 2 -and
    $continued.ClosedEncounters[1].Encounter.Id -ceq $entered.LaterEncounter.Definition.EncounterId -and
    $ownerAfterExit.Id -ceq $entry.Epoch.Id -and -not [Decennium.Foundation.WorldTiming]::ForActor($continued,$companion) -and
    (Actor-At $continued $hero 1 3) -and (Actor-At $continued $companion 3 2) -and
    $continued.CharterAttempt.Outcome.ToString() -ceq 'ReturnedComplete' -and $continued.ObservationActions.Count -eq 0) 'Actual combat and ordinary continuation did not retain the same world and management history.'

$report = [ordered]@{status='PASS';authority='TEST_ONLY';assemblies=$assemblies;fingerprint=$window.ContentFingerprint
    base=$window.SchemaVersion;wire=$window.WireSchemaVersion;ordinaryProcedureGate=$gate
    earlier=[ordered]@{at=$prepared.LaterEncounter.FirstExit.ClosedAt.ToString();revision=$prepared.LaterEncounter.FirstExit.ClosedRevision
        soldLot=$prepared.HavenSales[0].Basis.GoodsLotId;payment=$prepared.HavenSales[0].PaymentCopper
        paidAt=$prepared.HavenSales[0].UpdatedAt.ToString();meal=$prepared.HavenMealPurchases[0].Id
        bill=$prepared.ExpeditionBills[0].Id;billAt=$prepared.ExpeditionBills[0].UpdatedAt.ToString()
        charter=$prepared.CharterAttempt.Outcome.ToString();returnedAt=$prepared.CharterAttempt.Returned.At.ToString()}
    window=[ordered]@{at=$window.RuleClock.ToString();revision=$window.Revision;readySha256=Hash $readyBytes
        hero=@(Where-Is $window $hero);companion=@(Where-Is $window $companion);buyer=@(Where-Is $window $buyer)
        actualSight=@((Sees $window $companion $hero),(Sees $window $buyer $hero));noneHidden=$true
        scheduledMarker=$schedule.MarkerId($scheduled.LastStart);actionSpent=$scheduled.ActionSpent
        activityMarker=[Decennium.Foundation.ExplorationSearchRecord]::Marker($activity.CalendarId,$activity.IntervalIndex)
        activityAction=$activity.Action.ToString();due=$due.ToString();rng=$window.RandomState
        sightBlocker=@(2,1);visualFringe=@(3,1);visibleFringe=$cueVisible}
    alternate=[ordered]@{at=$alternate.RuleClock.ToString();position=@(Where-Is $alternate $hero)
        actualSight=@((Sees $alternate $companion $hero),(Sees $alternate $buyer $hero));rng=$alternate.RandomState}
    realLaterEntry=[ordered]@{at=$entered.RuleClock.ToString();revision=$entered.Revision;receipt=$entry.ArrivalCommandId
        from=@(Where-Is $beforeApproach $hero);arrival=@(Where-Is $entered $hero);order=@($entry.Epoch.Order)
        declarationWindow=$beforeApproach.RuleClock.ToString();originalOffCalendarDeadline=$approachDue.ToString()
        calendar=$entry.Epoch.Id;director=$entered.SurpriseEntry.Binding.DirectorId;decision=$entered.SurpriseEntry.Binding.Outcome.ToString()}
    continuation=[ordered]@{at=$continued.RuleClock.ToString();revision=$continued.Revision
        closedAt=$continued.ClosedEncounters[1].ClosedAt.ToString();hero=@(Where-Is $continued $hero)
        companion=@(Where-Is $continued $companion);heroCalendar=$ownerAfterExit.Id;saveSha256=Hash ($codec.Encode($continued))}}
$report | ConvertTo-Json -Depth 13 | Set-Content -LiteralPath $OutputFile -Encoding utf8
