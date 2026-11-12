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
$witness = 'TEST_ONLY.search-witness'
$kind = [Decennium.Foundation.CommandKind]
$ordinary = [Decennium.Foundation.AttackKnockoutMode]::OrdinaryOutcome
$press = [Decennium.Foundation.PressHitInstruction]::ArmOrReplace
$fixture = Call 'ObservationObserverIsolatedGapFixture' @()
$seedPolicy = Call 'ConnectedPolicy' @(26,[uint32]1,$null)
$null = $seedPolicy.EnableObservation($fixture)
$seed = Call 'ObservationTwoObserverHideSeed' @($seedPolicy.Initial())
$profiles = [Decennium.Foundation.Laboratory.ObservationSightProfile[]]@($fixture.Profiles | ForEach-Object {$_})
$profiles += [Decennium.Foundation.Laboratory.ObservationSightProfile]::new($witness,30,30)
$cells = @($fixture.Cells | ForEach-Object {$_})
$cells += [Decennium.Foundation.Laboratory.ObservationGridCell]::new(2,1,$true,$false,$true,$false)
$map = [Decennium.Foundation.Laboratory.ObservationFixture]::new(8,8,
    [Decennium.Foundation.Laboratory.ObservationGridCell[]]$cells,[Decennium.Foundation.Laboratory.ObservationSightProfile[]]$profiles)
$instances = [Decennium.Foundation.Laboratory.SharedActorInstanceDefinition[]]@(
    [Decennium.Foundation.Laboratory.SharedActorInstanceDefinition]::new($witness,'profile.numeric-warrior3',1,4))
$actorDefinitions = [Decennium.Foundation.Laboratory.SharedActorDefinition[]]@(
    [Decennium.Foundation.Laboratory.SharedActorDefinition]::new('profile.numeric-warrior3','TEST_ONLY.numeric-warrior3',30))
$siteDefinitions = [Decennium.Foundation.Laboratory.SharedSiteDefinition[]]@(
    [Decennium.Foundation.Laboratory.SharedSiteDefinition]::new('profile.tool-repair','tool-repair'))
$site = [Decennium.Foundation.Laboratory.SharedSiteInstanceDefinition]::new('TEST_ONLY.search-unused-site','profile.tool-repair',4,4)
$config = [Decennium.Foundation.Laboratory.SharedWorldConfiguration]::new('TEST_ONLY.search-source-baseline',
    $actorDefinitions,$instances,$siteDefinitions,$site,'TEST_ONLY.search-unused-lot')
$combat = [Decennium.Foundation.Laboratory.SharedCombatFixture]::new(1,$seed,26)
$crafting = [Decennium.Foundation.Laboratory.SharedCraftingFixture]::new(26,26,5,$false,
    [Decennium.Foundation.Laboratory.CraftingMishapFact[]]@())
$repair = [Decennium.Foundation.Laboratory.SharedRepairFixture]::new($true,$true,$true,$true,$true,4,4)
$event = Call 'CCApply' @('observation-exit-blind','Blinded',$opponent,$null,[Decennium.Foundation.ConditionStamp]::new([Decennium.Foundation.RuleTime]::new(0,1),0),$null)
$conditions = [Decennium.Foundation.Laboratory.ConditionCombatFixture]::new([Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@($event))
$terrain = [Decennium.Foundation.Laboratory.TacticalTerrainCell[]]@()
$policy = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::new($config,$combat,$null,$crafting,$repair,$null,$null,30,$conditions,$terrain)
$null = $policy.EnableObservation($map)
$null = $policy.EnableExplorationSearch()
$sim = Call 'World' @($policy)
function Commit($Command) { $null = Call 'WorldCommit' @($sim,$Command) }
function Tac([Decennium.Foundation.CommandKind]$Kind,[int]$X=0,[int]$Y=0,[int]$Stance=0) {
    Call 'Tac' @($sim,$Kind,$null,$null,$X,$Y,'',$false,$ordinary,$Stance,$press)
}
$stance = [int][Decennium.Foundation.CombatStance]::Aggressive
$null = Call 'CCDispatch' @($sim,'observation-exit-blind',$opponent)
$null = Call 'WorldStep' @($sim,1,0,$false,$hero)
$null = Call 'WorldAdvance' @($sim,1,1)
Commit (Call 'IC' @($sim,$kind::BeginFixedEncounter,'',$null,$hero,0,0,'search.baseline.begin'))
Commit (Tac $kind::SelectCombatStance 0 0 $stance)
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
Require (-not $ordinaryState.InventoryCombat -and $ordinaryState.LaterEncounter -eq $null) 'The actual tactical exit did not return to ordinary exploration.'
$ready = $sim.Capture()
$ledger = $ready.WorldIntervals | Where-Object ActorId -CEQ $hero
$calendar = $ready.WorldSchedule
$start = $calendar.Start($ledger.LastStart)
$next = $calendar.Start($ledger.LastStart + $calendar.Order.Count)
Require ($ready.WireSchemaVersion -eq 91 -and $ready.SchemaVersion -eq 51 -and $ready.ObservationActions.Count -eq 0 -and
    -not $ledger.ActionSpent -and $ready.RuleClock -eq $start) 'The selected world did not reach a genuine unspent ordinary Hide window.'
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$before = $codec.Encode($ready)
$sha = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($before)).ToLowerInvariant()
$authority = $policy.HostAuthority()
$hide = Call 'IC' @($sim,$kind::Hide,$calendar.MarkerId($ledger.LastStart),$null,$hero,0,0,'hide.baseline.ordinary')
$query = $sim.QueryCommand($authority,$hide)
$rejected = $sim.Execute($authority,$hide)
Require (-not $query.Supported -and $query.Code -ceq 'UnsupportedOperation' -and
    $rejected.Outcome.ToString() -ceq 'Rejected' -and $rejected.Code -ceq 'ObservationActionRequiresTacticalCombat') 'The ordinary Hide gap changed.'
Require ($sha -ceq [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($sim.Capture()))).ToLowerInvariant()) 'The rejected ordinary Hide changed exact state.'
function Observer-Rows($State) {
    foreach ($id in $searcher,$witness) {
        $canSee = [Decennium.Foundation.Laboratory.ObservationRules]::CanSee($State,$id,$hero)
        $hidden = [Decennium.Foundation.Laboratory.ObservationRules]::HiddenTo($State,$id,$hero)
        $live = [Decennium.Foundation.Laboratory.ActorLifeRules]::CanAct($State,$id)
        Require ($live -and -not $canSee -and -not $hidden) 'The live observer or concealment baseline unexpectedly changed.'
        $actor = $State.Actors | Where-Object Id -CEQ $id
        [ordered]@{actor=$id;anchor=@($actor.X,$actor.Y);living=$live;directSight=$canSee;hidden=$hidden}
    }
}

$targetMove = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($before),[Decennium.Foundation.ExecutionProfile]::Laboratory)
$null = Call 'WorldStep' @($targetMove,1,0,$false,$hero)
$null = Call 'WorldAdvance' @($targetMove,1,2)
$partial = $targetMove.Capture()
$null = Call 'WorldAdvance' @($targetMove,1,2)
$otherAnchor = $targetMove.Capture()
$actualHero = $otherAnchor.Actors | Where-Object Id -CEQ $hero
Require ($actualHero.X -eq 2 -and $actualHero.Y -eq 0 -and $partial.WorldTraversals[0].DistanceFeet.ToString() -ceq '5/2') 'Paid movement did not establish the actual second concealment position.'
$null = @(Observer-Rows $partial)
$otherObservers = @(Observer-Rows $otherAnchor)

$searchControl = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($before),[Decennium.Foundation.ExecutionProfile]::Laboratory)
$search = Call 'ExplorationSearchCommand' @($searchControl,1,0,'hide.baseline.search-without-hide')
$null = Call 'WorldCommit' @($searchControl,$search)
$finish = Call 'SearchAdvance' @($searchControl,12,1)
$searched = $searchControl.Capture()
$searchResult = $searched.ObservationActions[-1]
Require ($finish.ReachedClock -eq $next -and $searchResult.Outcome.ToString() -ceq 'SearchNoFinding' -and
    $searchResult.WordsConsumed -eq 0 -and $searched.RandomState -eq $ready.RandomState) 'Occlusion alone incorrectly supplied a Searchable Hide result.'
[ordered]@{
    status='PASS';profile=$ready.ContentFingerprint;wire=$ready.WireSchemaVersion;base=$ready.SchemaVersion;seed=$seed;assemblies=$assemblies
    resolvedCombat=[ordered]@{at=$ordinaryState.RuleClock.ToString();revision=$ordinaryState.Revision;exit=$exit.Id;noPreviousHide=$true}
    firstOrdinaryWindow=[ordered]@{at=$start.ToString();nextOwnStart=$next.ToString();ordinal=$ledger.LastStart
        marker=$calendar.MarkerId($ledger.LastStart);calendar=$calendar.Id;actionSpent=$ledger.ActionSpent;hider=@(1,0)
        rng=$ready.RandomState;observers=@(Observer-Rows $ready)}
    ordinaryHide=[ordered]@{query=$query.Code;execution=$rejected.Code;unchangedSha256=$sha}
    actualChangeOfHidingPosition=[ordered]@{partialAt=$partial.RuleClock.ToString();partialFeet=$partial.WorldTraversals[0].DistanceFeet.ToString()
        at=$otherAnchor.RuleClock.ToString();position=@($actualHero.X,$actualHero.Y);observers=$otherObservers}
    paidSearchWithoutHide=[ordered]@{reached=$finish.ReachedClock.ToString();status=$searchResult.Outcome.ToString()
        wordsConsumed=$searchResult.WordsConsumed;rngAfter=$searched.RandomState}
} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputFile -Encoding utf8
