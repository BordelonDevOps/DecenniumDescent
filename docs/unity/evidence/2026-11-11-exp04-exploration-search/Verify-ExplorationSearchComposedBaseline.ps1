param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
$assemblies = @(foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    $dll = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $dll
    [ordered]@{name=Split-Path -Leaf $dll;sha256=(Get-FileHash -LiteralPath $dll).Hash.ToLowerInvariant()}
})
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
function Call([string]$Name,[object[]]$Arguments) {
    try { $tests.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
function Require([bool]$Condition,[string]$Message) { if (-not $Condition) { throw $Message } }
$hero = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::ActorId
$searcher = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::CompanionId
$opponent = [Decennium.Foundation.Laboratory.AdditionalTacticalActor]::Id
$witness = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::LaterDefenderId
$kind = [Decennium.Foundation.CommandKind]
$ordinary = [Decennium.Foundation.AttackKnockoutMode]::OrdinaryOutcome
$press = [Decennium.Foundation.PressHitInstruction]::ArmOrReplace
$fixture = Call 'ObservationObserverIsolatedGapFixture' @()
$seedPolicy = Call 'ConnectedPolicy' @(26,[uint32]1,$null)
$null = $seedPolicy.EnableObservation($fixture)
$seed = Call 'ObservationTwoObserverHideSeed' @($seedPolicy.Initial())
$profiles = [Decennium.Foundation.Laboratory.ObservationSightProfile[]]@($fixture.Profiles | ForEach-Object {$_})
$profiles += [Decennium.Foundation.Laboratory.ObservationSightProfile]::new($witness,30,30)
$profiles += [Decennium.Foundation.Laboratory.ObservationSightProfile]::new('TEST_ONLY.haven-copper-buyer',30,30)
$cells = @($fixture.Cells | ForEach-Object {$_})
$cells += [Decennium.Foundation.Laboratory.ObservationGridCell]::new(2,1,$true,$false,$true,$false)
$map = [Decennium.Foundation.Laboratory.ObservationFixture]::new(8,8,
    [Decennium.Foundation.Laboratory.ObservationGridCell[]]$cells,[Decennium.Foundation.Laboratory.ObservationSightProfile[]]$profiles)
$event = Call 'CCApply' @('observation-exit-blind','Blinded',$opponent,$null,[Decennium.Foundation.ConditionStamp]::new([Decennium.Foundation.RuleTime]::new(0,1),0),$null)
$conditions = [Decennium.Foundation.Laboratory.ConditionCombatFixture]::new([Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@($event))
$terrain = [Decennium.Foundation.Laboratory.TacticalTerrainCell[]]@()
$policy = Call 'ReengagementPolicy' @($seed,$conditions,$true,$true)
$null = $policy.EnableSurpriseAwareEntry([Decennium.Foundation.SurpriseAwareness]::Warned)
$null = $policy.EnableObservation($map)
$sim = Call 'World' @($policy)
function Commit($Command) { $null = Call 'WorldCommit' @($sim,$Command) }
function Tac([Decennium.Foundation.CommandKind]$Kind,[int]$X=0,[int]$Y=0,[int]$Stance=0) {
    Call 'Tac' @($sim,$Kind,$null,$null,$X,$Y,'',$false,$ordinary,$Stance,$press)
}
$stance = [int][Decennium.Foundation.CombatStance]::Aggressive
$null = Call 'CCDispatch' @($sim,'observation-exit-blind',$opponent)
$null = Call 'WorldStep' @($sim,1,0,$false,$hero)
$null = Call 'WorldAdvance' @($sim,3,2)
Commit (Call 'IC' @($sim,$kind::BeginFixedEncounter,'',$null,$hero,0,0,'search.baseline.begin'))
Commit (Tac $kind::SelectCombatStance 0 0 $stance)
$hide = Call 'ObservationCommand' @($sim,$kind::Hide,$hero,0,0)
Commit $hide
$hidden = $sim.Capture()
Require ([Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($hidden,$searcher,$hero) -and
    [Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($hidden,$witness,$hero)) 'One actual Hide did not establish concealment for both live observers.'
Commit (Tac $kind::EndRegularTurn)
$route = @(@(4,1),@(4,2),@(3,2),@(2,2),@(2,3),@(1,3),@(0,3),@(0,2),@(0,1),@(0,0))
for ($i=0;$i -lt $route.Count;$i++) {
    if ($sim.Capture().Encounter.CurrentActor -cne $opponent) { $null = Call 'ConnectedEnd' @($sim) }
    $state = $sim.Capture()
    if (-not ($state.Stances | Where-Object {$_.ActorId -ceq $opponent -and $_.TurnOrdinal -eq $state.Encounter.TurnOrdinal})) {
        Commit (Tac $kind::SelectCombatStance 0 0 $stance)
    }
    Commit (Tac $kind::TacticalStep $route[$i][0] $route[$i][1])
    if ($i -eq 5 -or $i -eq $route.Count-1) { $null = Call 'ConnectedEnd' @($sim) }
}
$null = Call 'DefeatConnectedEnemy' @($sim)
$exit = Tac $kind::EndFixedEncounter
Commit $exit
$ordinaryState = $sim.Capture()
Require (-not $ordinaryState.InventoryCombat -and $ordinaryState.SurpriseEntry.Decision -eq $null) 'The actual tactical exit did not return to ordinary exploration.'
Require ([Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($ordinaryState,$searcher,$hero) -and
    [Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($ordinaryState,$witness,$hero)) 'Existing Hide did not survive the actual exit for both living observers.'
$calendar = $ordinaryState.WorldSchedule
$intervalIndex = [Decennium.Foundation.WorldActivityIntervalRecord]::IndexAt($calendar,$ordinaryState.RuleClock)
$intervalStart = [Decennium.Foundation.WorldActivityIntervalRecord]::StartAt($calendar,$intervalIndex)
if ($ordinaryState.RuleClock -ne $intervalStart) {
    $next = [Decennium.Foundation.WorldActivityIntervalRecord]::EndAt($calendar,$intervalIndex)
    Require ($next.Denominator -eq 1 -and $ordinaryState.RuleClock.Denominator -eq 1) 'Expected integral fixture timing.'
    $null = Call 'WorldAdvance' @($sim,[int]($next.Numerator-$ordinaryState.RuleClock.Numerator),1)
}
$ready = $sim.Capture()
$ledger = $ready.WorldActivityIntervals | Where-Object ActorId -CEQ $searcher
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$encoded = $codec.Encode($ready)
$sha = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($encoded)).ToLowerInvariant()
$hostAuthority = Call 'LaterHost' @()
$queryRows = @(foreach ($candidate in @(@(1,0),@(0,1))) {
    $command = Call 'IC' @($sim,$kind::Search,'',$null,$searcher,$candidate[0],$candidate[1],
        "search.baseline.$($candidate[0]).$($candidate[1])")
    $query = $sim.QueryCommand($hostAuthority,$command)
    $response = $sim.Execute($hostAuthority,$command)
    Require ($query.Supported -and $query.Code -ceq 'ObservationActionRequiresTacticalCombat' -and
        $response.Code -ceq $query.Code -and $response.Outcome.ToString() -ceq 'Rejected') 'Existing ordinary Search did not fail uniformly.'
    [ordered]@{x=$candidate[0];y=$candidate[1];query=$query.Code;execution=$response.Code;costs=@($query.Costs)}
})
Require ($sha -ceq [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($sim.Capture()))).ToLowerInvariant()) 'The unavailable command changed the exact state.'
$nextStart = [Decennium.Foundation.WorldActivityIntervalRecord]::EndAt($calendar,$ledger.IntervalIndex)
$knowledge = @(foreach ($observer in $searcher,$witness) {
    $evidence = $ready.ObserverKnowledge | Where-Object {$_.ObserverId -ceq $observer -and $_.TargetId -ceq $hero}
    Require ([Decennium.Foundation.Laboratory.ActorLifeRules]::CanAct($ready,$observer) -and
        [Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($ready,$observer,$hero) -and
        -not [Decennium.Foundation.Laboratory.ObservationRules]::CanSee($ready,$observer,$hero)) 'The ready witness lost live independent concealment.'
    $position = $ready.Actors | Where-Object Id -CEQ $observer
    [ordered]@{observer=$observer;position=@($position.X,$position.Y);hiddenAttempt=$evidence.HiddenAttemptId
        locationKnown=$evidence.CurrentLocationKnown;directSight=$false;living=$true}
})
$moving = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($encoded),[Decennium.Foundation.ExecutionProfile]::Laboratory)
$null = Call 'WorldStep' @($moving,1,0,$false,$hero)
$null = Call 'WorldAdvance' @($moving,3,4)
$partial = $moving.Capture()
$null = Call 'WorldAdvance' @($moving,3,4)
$moved = $moving.Capture()
$movedHero = $moved.Actors | Where-Object Id -CEQ $hero
foreach ($state in $partial,$moved) {
    foreach ($observer in $searcher,$witness) {
        Require ([Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($state,$observer,$hero) -and
            -not [Decennium.Foundation.Laboratory.ObservationRules]::CanSee($state,$observer,$hero)) 'The real relocation exposed the hider.'
    }
}
Require ($movedHero.X -eq 2 -and $movedHero.Y -eq 0 -and $partial.WorldTraversals.Count -eq 1 -and $moved.WorldTraversals.Count -eq 0 -and $moved.RandomState -eq $ready.RandomState) 'The actual move did not leave the candidate space as expected.'
[ordered]@{
    status='PASS';profile=$ready.ContentFingerprint;schema=$ready.SchemaVersion;seed=$seed;assemblies=$assemblies
    hide=[ordered]@{command=$hide.Id;at=$hidden.RuleClock.ToString();revision=$hidden.Revision
        check=$hidden.ObservationActions[-1].Id;natural=$hidden.ObservationActions[-1].Natural;total=$hidden.ObservationActions[-1].Total}
    exit=[ordered]@{command=$exit.Id;at=$ordinaryState.RuleClock.ToString();revision=$ordinaryState.Revision;tactical=$false}
    ready=[ordered]@{at=$ready.RuleClock.ToString();revision=$ready.Revision;rng=$ready.RandomState;target=$hero;candidate=@(1,0)
        searcher=$searcher;calendar=$calendar.Id;interval=$ledger.IntervalIndex;action=$ledger.Action.ToString()
        existingNextInterval=$nextStart.ToString();knowledge=$knowledge}
    ordinarySearchBaseline=$queryRows;unchangedSaveSha256=$sha
    actualUnseenRelocation=[ordered]@{partialAt=$partial.RuleClock.ToString();partialFeet=$partial.WorldTraversals[0].DistanceFeet.ToString()
        arrivedAt=$moved.RuleClock.ToString();newAnchor=@($movedHero.X,$movedHero.Y);bothStillHidden=$true}
} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputFile -Encoding utf8
