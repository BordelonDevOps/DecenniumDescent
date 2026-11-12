param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$OutputFile
)
$ErrorActionPreference = 'Stop'
$assemblies = @(foreach ($name in 'Core', 'Persistence', 'LabModel', 'HeadlessTests') {
    $path = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $path
    [ordered]@{ name = (Split-Path -Leaf $path); sha256 = (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
})
$t = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
function Call([string]$Name,[object[]]$Arguments){
    try { $t.GetMethod($Name,$flags).Invoke($null,$Arguments) }
    catch { throw $_.Exception.GetBaseException() }
}
function Assert-True([bool]$Condition,[string]$Failure) {
    if(-not $Condition) { throw $Failure }
}
$policy = Call 'ReengagementPolicy' @($null,$null,$true,$true)
$sim = Call 'LaterPrepared' @($policy)
$before = $sim.Capture()
$def = $before.LaterEncounter.Definition
$hostAuthority = Call 'LaterHost' @()
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$kinds = [Decennium.Foundation.CommandKind]
$guard = [Decennium.Foundation.CombatStance]::Guarded
$ordinary = [Decennium.Foundation.AttackKnockoutMode]::OrdinaryOutcome
$press = [Decennium.Foundation.PressHitInstruction]::KeepExisting
function State($s) {
    [ordered]@{ at = $s.RuleClock.ToString(); revision = $s.Revision; rng = $s.RandomState; tactical = $s.InventoryCombat
        turn = if ($s.Encounter) { $s.Encounter.CurrentTurnId }; actor = if ($s.Encounter) { $s.Encounter.CurrentActor }
        currentObservations = if ($s.Encounter) { @($s.Encounter.ObservedOrdinals) }
        participants = @(foreach($id in $def.HeroId,$def.DefenderId){
            $life=$s.Lives | Where-Object ActorId -CEQ $id
            $interval=$s.WorldIntervals | Where-Object ActorId -CEQ $id
            $pos=[Decennium.Foundation.WorldPositionResolver]::Position($s,$id)
            [ordered]@{id=$id;position=@($pos.Item1.ToString(),$pos.Item2.ToString());hp=$life.Hp
                held=@($life.HeldItems);lastStart=$interval.LastStart;actionSpent=$interval.ActionSpent
                reaction=$interval.ReactionAvailable;movement=if($interval){$interval.MovementSpent.ToString()} }
        })
    }
}
function Tac([Decennium.Foundation.CommandKind]$Kind,[string]$Target=$null,[int]$X=0,[int]$Y=0,[string]$Weapon='') {
    Call 'Tac' @($sim,$Kind,$Target,$null,$X,$Y,$Weapon,$false,$ordinary,0,$press)
}
function Step([int]$X,[int]$Y) {
    Call 'LaterCommit' @($sim,(Tac $kinds::TacticalStep $sim.Capture().Encounter.CurrentTurnId $X $Y))
}
$approach=Call 'LaterApproach' @($sim)
$null=Call 'LaterCommit' @($sim,$approach)
$null=Call 'LaterCommit' @($sim,(Call 'LaterAdvance' @($sim,1,2)))
$partial=$sim.Capture()
Assert-True ($partial.WorldTraversals.Count -eq 1 -and -not $partial.InventoryCombat) 'Actual fractional approach absent'
$arrival=Call 'LaterAdvance' @($sim,12,1)
$transition=Call 'LaterCommit' @($sim,$arrival)
$entry=$sim.Capture()
Assert-True ($entry.Encounter.CurrentActor -eq $def.DefenderId -and $entry.Encounter.TurnOrdinal -eq 0 -and $transition.TacticalDecisionAt -eq $entry.RuleClock) 'Expected genuine defender-first entry'
$null=Call 'LaterStance' @($sim,$guard)
$null=Step 1 4
$adjacent=$sim.Capture()
Assert-True (-not [Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::PendingMove($adjacent)) 'Adjacent lateral step created an offer'
$null=Step 2 3
$leaving=$sim.Capture()
$offer=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::PendingMove($leaving)
Assert-True ($offer -and $offer.Reactors -ccontains $def.HeroId) 'The aware hero did not receive the real before-first-Start opportunity'
$decline=Call 'Opportunity' @($sim,$false,'',$ordinary,[Decennium.Foundation.PressHitInstruction]::ArmOrReplace)
$null=Call 'LaterCommit' @($sim,$decline)
$null=Step 1 4
$null=Call 'EndReinforcementTurn' @($sim,$guard)
$hero=$sim.Capture()
Assert-True ($hero.Encounter.CurrentActor -eq $def.HeroId -and $hero.Encounter.TurnOrdinal -eq 1) 'The genuine hero first Start is absent'
$null=Call 'LaterStance' @($sim,$guard)
$attack=Tac $kinds::AttackClub $def.DefenderId 0 0 ([Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ActorClub)
$null=Call 'LaterCommit' @($sim,$attack)
$paid=$sim.Capture()
Assert-True ($paid.MeleeAttacks[-1].AttackerId -eq $def.HeroId -and ($paid.WorldIntervals | Where-Object ActorId -EQ $def.HeroId).ActionSpent) 'Aware first-turn Club action did not pay through shared combat'
$null=Call 'EndReinforcementTurn' @($sim,$guard)
$ended=$sim.Capture()

$sidePolicy=Call 'ReengagementPolicy' @($null,$null,$true,$true)
$sim=[Decennium.Foundation.Simulation]::new($sidePolicy,$hero,[Decennium.Foundation.ExecutionProfile]::Laboratory)
$null=Call 'LaterStance' @($sim,$guard)
$vessel='TEST_ONLY.pack-skin'
$handling=[Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1),'',[Decennium.Foundation.HandlingKind]::Drop)
$handle=Call 'IC' @($sim,$kinds::HandlePortableEquipment,$vessel,$handling,$def.HeroId,0,0,'surprise.baseline.simple-handling')
$freeResult=$sim.Execute($hostAuthority,$handle)
$free=$sim.Capture()
$freeInterval=$free.WorldIntervals | Where-Object ActorId -EQ $def.HeroId
Assert-True ($freeResult.Outcome.ToString() -eq 'Committed' -and $freeInterval.Interactions -eq 1 -and -not $freeInterval.ActionSpent -and $free.RuleClock -eq $hero.RuleClock) "The known simple handling did not use a free interaction: $($freeResult.Code)"
$secondHandling=[Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1),'',[Decennium.Foundation.HandlingKind]::Pickup)
$second=Call 'IC' @($sim,$kinds::HandlePortableEquipment,$vessel,$secondHandling,$def.HeroId,0,0,'surprise.baseline.second-handling')
$null=Call 'LaterCommit' @($sim,$second)
$used=$sim.Capture()
$usedInterval=$used.WorldIntervals | Where-Object ActorId -EQ $def.HeroId
Assert-True ($usedInterval.Interactions -eq 2 -and $usedInterval.ActionSpent -and $used.RuleClock -eq $hero.RuleClock) 'The real second handling did not pay the ordinary Action'

$reactionPolicy=Call 'ReengagementPolicy' @($null,$null,$true,$true)
$sim=[Decennium.Foundation.Simulation]::new($reactionPolicy,$hero,[Decennium.Foundation.ExecutionProfile]::Laboratory)
$null=Call 'EndReinforcementTurn' @($sim,$guard)
$null=Call 'LaterStance' @($sim,$guard)
$null=Step 2 3
$nextOffer=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::PendingMove($sim.Capture())
Assert-True ($nextOffer -and $nextOffer.Reactors -ccontains $def.HeroId) 'Expected the same leave-reach event after the genuine first End'
$react=Call 'Opportunity' @($sim,$true,([Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ActorClub),$ordinary,[Decennium.Foundation.PressHitInstruction]::ArmOrReplace)
$null=Call 'LaterCommit' @($sim,$react)
$reaction=$sim.Capture()
Assert-True ($reaction.MeleeAttacks[-1].Opportunity -and -not ($reaction.WorldIntervals | Where-Object ActorId -EQ $def.HeroId).ReactionAvailable) 'The existing Reaction did not pay for the real later attack'

[ordered]@{status='PASS';authority='Exact schema 89 aware predecessor, surprise integration absent';
    earlierCharter=$entry.CharterAttempt.Outcome.ToString();approach=$approach.Id;approachRevision=$approach.ExpectedRevision+1
    partialFeet=$partial.WorldTraversals[0].DistanceFeet.ToString();arrival=$arrival.Id;entryDraws=@($entry.LaterEncounter.Entry.Draws | ForEach-Object {
        [ordered]@{actor=$_.ActorId;natural=$_.Natural;total=$_.Total} });
    before=(State $before);partial=(State $partial);entry=(State $entry);adjacent=(State $adjacent);
    actualAwareOpportunity=[ordered]@{id=$offer.Id;reactors=@($offer.Reactors);decline=$decline.Id;positionBeforeDecline=(State $leaving)};
    heroFirstStart=(State $hero);paidAttack=$paid.MeleeAttacks[-1].Id;afterPaidAttack=(State $paid);heroFirstEnd=(State $ended);
    realInteractions=[ordered]@{first=$handle.Id;firstState=(State $free);second=$second.Id;secondState=(State $used)};
    afterFirstEndReaction=[ordered]@{offer=$nextOffer.Id;command=$react.Id;attack=$reaction.MeleeAttacks[-1].Id;state=(State $reaction)};
    finalSaveSha256=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($codec.Encode($ended))).ToLowerInvariant();assemblies=$assemblies} |
    ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutputFile -Encoding utf8
