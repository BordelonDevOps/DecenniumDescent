#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy RangedPolicy(uint seed=1,long hp=26,RepeatingCrossbowFixture fixture=null,ConditionCombatFixture conditions=null)
            =>new TestOnlySharedWorldPolicy(fixture??new RepeatingCrossbowFixture(),new SharedCombatFixture(hp,seed),conditions:conditions);
        private static Command RangedCommand(Simulation s,CommandKind kind,string target="",int amount=0,string ammo=RepeatingCrossbowFixture.AmmunitionId)
        {
            var v=s.Capture();string actor=v.Encounter?.CurrentActor??TestOnlyPolicy.ActorId;
            string turn=v.Encounter?.CurrentTurnId??"world.unstarted-turn";
            return new Command("ranged."+(v.Revision+1),actor,v.Revision,kind,target,
                ranged:new RangedRequest(turn,RepeatingCrossbowFixture.WeaponId,kind==CommandKind.ReloadRepeatingCrossbow?ammo:"",amount));
        }
        private static void RangedCommit(Simulation s,Command c)=>WorldCommit(s,c);
        private static void PrepareRangedActorTurn(Simulation s)
        {
            BeginEncounter(s);
            RangedCommit(s,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:1));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
            WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
            WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
        }
        private static uint SeedForNatural(int natural)
        {
            for(uint seed=1;seed<1_000_000;seed++)if(PlaytestDice.RollD20(seed).Natural==natural)return seed;
            throw new Exception("Could not find deterministic ranged seed.");
        }
        private static void AddRangedCrossbowCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("repeating_crossbow_fixture_persists_custody_training_mass_and_empty_magazine",()=>{
                var p=RangedPolicy();var s=World(p);var v=s.Capture();var weapon=v.RepeatingCrossbows.Single();
                Require(v.SchemaVersion==Snapshot.RepeatingCrossbowSchema&&weapon.HeldBy==TestOnlyPolicy.ActorId&&weapon.GripHands==2
                    &&weapon.LoadedBoltLots.Count==0&&v.AmmunitionLots.Single().AvailableQuantity==20
                    &&v.RangedCombatants.Single().CrossbowProficient&&v.RangedCombatants.Single().TrainingId==RepeatingCrossbowFixture.TrainingId
                    &&v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).HeldItems.SequenceEqual(new[]{RepeatingCrossbowFixture.WeaponId})
                    &&v.Clubs.Single(x=>x.Id==TestOnlyClubAttackPolicy.ActorClub).HeldBy==""
                    &&PortableEquipmentRules.CarriedBurden(v,TestOnlyPolicy.ActorId).Pounds==Q(43,2),"Source-bound weapon, kit, training, hands or mass was not initialized exactly once.");
                var path=Path.Combine(directory,"ranged-crossbow-initial.ddsave");new FileSaveStore().Save(path,v);
                Require(Bytes(s).SequenceEqual(Bytes(new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory))),"Initial ranged equipment failed save/restore.");
            });
            cases.Add("repeating_reload_moves_exact_bolts_pays_action_and_replays_after_restore",()=>{
                var p=RangedPolicy();var s=World(p);BeginEncounter(s);uint before=s.Capture().RandomState;
                var reload=RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:5);RangedCommit(s,reload);var v=s.Capture();
                Require(v.RepeatingCrossbows.Single().LoadedBoltLots.SequenceEqual(Enumerable.Repeat(RepeatingCrossbowFixture.AmmunitionId,5))
                    &&v.RepeatingCrossbows.Single().GripHands==1&&v.AmmunitionLots.Single().AvailableQuantity==15
                    &&v.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent&&v.RandomState==before&&v.RuleClock==default,
                    "Reload created, lost, retimed ammunition, or failed to pay Action/release one grip.");
                RejectUnchanged(s,host,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:1),"ActionAlreadySpent");
                var restored=new Simulation(p,codec.Decode(Bytes(s)),ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(restored))&&restored.Execute(host,reload).Outcome==Outcome.Duplicate,
                    "Reload save/restore or idempotency failed.");
                Require(PortableEquipmentRules.CarriedBurden(v,TestOnlyPolicy.ActorId).Pounds==Q(43,2),"Loading changed total carried mass.");
            });
            cases.Add("repeating_crossbow_attack_uses_shared_action_critical_d10_damage_and_one_bolt",()=>{
                var p=RangedPolicy(SeedForNatural(20));var s=World(p);PrepareRangedActorTurn(s);var before=s.Capture();
                var attack=RangedCommand(s,CommandKind.AttackRepeatingCrossbow,AdditionalTacticalActor.Id);RangedCommit(s,attack);var v=s.Capture();
                var result=v.RangedAttacks.Single();var life=v.Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id);
                Require(result.Attack.Critical&&result.Attack.Hit&&result.Attack.Modifier==2&&result.Damage.Dice.Count==2
                    &&result.Damage.Total==result.Damage.Dice.Sum()+2&&result.Damage.AfterDefense==result.Damage.Total
                    &&v.RepeatingCrossbows.Single().LoadedBoltLots.Count==0&&v.RepeatingCrossbows.Single().GripHands==2
                    &&v.AmmunitionLots.Single().AvailableQuantity==19&&life.Hp<26
                    &&v.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent&&v.RuleClock==before.RuleClock
                    &&v.Presses.Length==0&&v.RandomState==result.Damage.FinalRandom,
                    "Ranged attack omitted the shared Action, critical d10 dice, magazine expenditure or settled damage.");
                RejectUnchanged(s,host,RangedCommand(s,CommandKind.AttackRepeatingCrossbow,AdditionalTacticalActor.Id),"ActionAlreadySpent");
                var path=Path.Combine(directory,"ranged-crossbow-critical.ddsave");new FileSaveStore().Save(path,v);
                var restored=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(restored)),"Ranged outcome, ammunition provenance or damage did not survive save/restore.");
            });
            cases.Add("repeating_crossbow_attack_uses_character_facts_after_stale_cache_save_restore_and_replay",()=>{
                var p=RangedPolicy(SeedForNatural(20),fixture:new RepeatingCrossbowFixture(legacyProficiencyBonusProjection:0));
                var s=World(p);PrepareRangedActorTurn(s);
                var initial=s.Capture();var cached=initial.RangedCombatants.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                Require(cached.ProficiencyBonus==0,"The test fixture did not initialize a stale compatibility projection.");
                byte[] before=Bytes(s);var restoredBefore=new Simulation(p,codec.Decode(before),ExecutionProfile.Laboratory);
                Require(before.SequenceEqual(Bytes(restoredBefore))&&restoredBefore.Capture().RangedCombatants.Single(x=>x.ActorId==cached.ActorId).ProficiencyBonus==0,
                    "The historical ranged numeric cache did not survive byte-for-byte save/restore.");
                var replay=new Simulation(p,codec.Decode(before),ExecutionProfile.Laboratory);
                var attack=RangedCommand(restoredBefore,CommandKind.AttackRepeatingCrossbow,AdditionalTacticalActor.Id);
                var first=restoredBefore.Execute(host,attack);var second=replay.Execute(host,attack);
                var facts=CharacterRuleFacts.ForActor(restoredBefore.Capture(),TestOnlyPolicy.ActorId);
                int expected=checked(facts.AbilityModifier(CharacterAbility.Dexterity)
                    +(cached.CrossbowProficient?facts.ProficiencyBonus:0));
                Require(first.Outcome==Outcome.Committed&&second.Outcome==Outcome.Committed
                    &&restoredBefore.Capture().RangedAttacks.Single().Attack.Modifier==expected&&expected!=cached.ProficiencyBonus
                    &&Bytes(restoredBefore).SequenceEqual(Bytes(replay)),
                    "Attack resolution reused stale cached proficiency instead of the restored authoritative character record.");
                byte[] after=Bytes(restoredBefore);var restoredAfter=new Simulation(p,codec.Decode(after),ExecutionProfile.Laboratory);
                Require(after.SequenceEqual(Bytes(restoredAfter))&&restoredAfter.Execute(host,attack).Outcome==Outcome.Duplicate
                    &&after.SequenceEqual(Bytes(restoredAfter)),"Post-attack save/restore or deterministic command replay changed the authoritative result.");
            });
            cases.Add("repeating_crossbow_rejects_empty_ammo_and_blocked_unknown_or_total_cover_before_roll",()=>{
                foreach(var item in new[]{
                    new{Fixture=new RepeatingCrossbowFixture(targetLocationKnown:false),Failure="RangedAttackUnknownTargetLocation"},
                    new{Fixture=new RepeatingCrossbowFixture(lineOfFireClear:false),Failure="RangedAttackBlockedLineOfFire"},
                    new{Fixture=new RepeatingCrossbowFixture(targetCover:CombatCover.Total),Failure="RangedAttackTotalCover"}}) {
                    var p=RangedPolicy(fixture:item.Fixture);var s=World(p);PrepareRangedActorTurn(s);
                    RejectUnchanged(s,host,RangedCommand(s,CommandKind.AttackRepeatingCrossbow,AdditionalTacticalActor.Id),item.Failure);
                }
                var emptyPolicy=RangedPolicy();var empty=World(emptyPolicy);BeginEncounter(empty);
                WorldCommit(empty,Tac(empty,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                RejectUnchanged(empty,host,RangedCommand(empty,CommandKind.AttackRepeatingCrossbow,AdditionalTacticalActor.Id),"NoAmmunition");
            });
            cases.Add("repeating_crossbow_query_discovers_costs_without_mutating_rng_or_authoritative_state",()=>{
                var p=RangedPolicy();var s=World(p);BeginEncounter(s);var before=Bytes(s);uint random=s.Capture().RandomState;
                var options=s.DiscoverCommands(host,TestOnlyPolicy.ActorId);
                var reloads=options.Where(x=>x.Command.Kind==CommandKind.ReloadRepeatingCrossbow).OrderBy(x=>x.Command.Ranged.Amount).ToArray();
                var attack=options.Single(x=>x.Command.Kind==CommandKind.AttackRepeatingCrossbow);
                Require(reloads.Length==5&&reloads.All(x=>x.Query.Supported&&x.Query.Admissible&&x.Query.Code=="Available")
                    &&reloads.Select(x=>x.Command.Ranged.Amount).SequenceEqual(new[]{1,2,3,4,5}),"Discovery did not expose exactly the finite legal reload quantities.");
                Require(reloads[0].Query.Costs.Count==2&&reloads[0].Query.Costs[0].Kind=="action"
                    &&reloads[0].Query.Costs[1].ResourceId==RepeatingCrossbowFixture.AmmunitionId&&reloads[0].Query.Costs[1].Amount==1,
                    "Read-only query omitted the admitted action and ammunition costs.");
                Require(!attack.Query.Admissible&&attack.Query.Code=="NoAmmunition"&&attack.Query.Costs.Count==0,
                    "An empty-magazine attack was not explained as inadmissible without claiming spendable costs.");
                for(int i=0;i<3;i++)s.QueryCommand(host,reloads[0].Command);
                Require(Bytes(s).SequenceEqual(before)&&s.Capture().RandomState==random,"Repeated query/discovery changed authoritative bytes or RNG.");
                var stale=new Command("query.stale",reloads[0].Command.Actor,reloads[0].Command.ExpectedRevision-1,
                    CommandKind.ReloadRepeatingCrossbow,ranged:reloads[0].Command.Ranged);
                Require(s.QueryCommand(host,stale).Code=="StaleRevision","Query accepted a stale command revision.");
                var revoked=new Authority("TEST_ONLY.query-revoked",new[]{TestOnlyPolicy.ActorId});
                Require(s.QueryCommand(revoked,reloads[0].Command).Code=="InventoryNotAuthorized","Query ignored revoked inventory permission.");
                var unsupported=new Command("query.unsupported",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.Move);
                Require(!s.QueryCommand(host,unsupported).Supported,"Unsupported operations were presented as queryable.");
                var pending=OverwatchTrigger(OverwatchExecutionPolicy(SeedForNatural(10)));var pendingView=pending.Capture();var pendingBytes=Bytes(pending);
                var pendingAttack=new Command("query.pending",TestOnlyPolicy.ActorId,pendingView.Revision,CommandKind.AttackRepeatingCrossbow,
                    AdditionalTacticalActor.Id,ranged:new RangedRequest(pendingView.Encounter.CurrentTurnId,
                        RepeatingCrossbowFixture.WeaponId,"",0));
                Require(pending.QueryCommand(host,pendingAttack).Code=="TacticalChoicePending"&&Bytes(pending).SequenceEqual(pendingBytes),
                    "Query bypassed an unresolved tactical response/choice.");
                Require(Bytes(s).SequenceEqual(before),"Rejected queries changed authoritative state.");
            });
            cases.Add("repeating_crossbow_headless_controller_submits_normal_reload_and_attack_commands",()=>{
                var p=RangedPolicy();var s=World(p);BeginEncounter(s);var controller=new RepeatingCrossbowHeadlessController();
                var reload=controller.Act(s,host,TestOnlyPolicy.ActorId);var loaded=s.Capture();
                Require(reload!=null&&reload.Outcome==Outcome.Committed&&loaded.RepeatingCrossbows.Single().LoadedBoltLots.Count==5
                    &&loaded.AmmunitionLots.Single().AvailableQuantity==15&&loaded.Receipts.Any(x=>x.Revision==reload.Revision
                        &&x.Id.StartsWith("option.",StringComparison.Ordinal)),
                    "Headless controller failed to submit the largest admissible reload through normal command execution.");
                var restored=new Simulation(p,codec.Decode(Bytes(s)),ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(restored)),"Headless reload did not survive snapshot save/restore.");s=restored;
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Guarded));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                var attack=controller.Act(s,host,TestOnlyPolicy.ActorId);var final=s.Capture();
                Require(attack!=null&&attack.Outcome==Outcome.Committed&&final.RangedAttacks.Length==1
                    &&final.RepeatingCrossbows.Single().LoadedBoltLots.Count==4&&final.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,
                    "Headless controller did not select and execute an admissible attack through the ordinary command path.");
            });
            cases.Add("repeating_crossbow_discovery_retains_known_unseen_attack_targets",()=>{
                var p=RangedPolicy(fixture:new RepeatingCrossbowFixture(targetVisible:false));var s=World(p);PrepareRangedActorTurn(s);
                var option=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Single(x=>x.Command.Kind==CommandKind.AttackRepeatingCrossbow);
                Require(option.Query.Admissible&&option.Query.Code=="Available",
                    "A known but unseen location was incorrectly hidden from attack discovery instead of retaining the existing disadvantage rule.");
            });
            cases.Add("repeating_crossbow_proficiency_is_explicit_and_untrained_possession_adds_no_bonus",()=>{
                var p=RangedPolicy(fixture:new RepeatingCrossbowFixture(proficient:false));var s=World(p);PrepareRangedActorTurn(s);
                RangedCommit(s,RangedCommand(s,CommandKind.AttackRepeatingCrossbow,AdditionalTacticalActor.Id));
                Require(s.Capture().RangedCombatants.Single().TrainingId==""&&!s.Capture().RangedCombatants.Single().CrossbowProficient
                    &&s.Capture().RangedAttacks.Single().Attack.Modifier==0,"Possession inferred martial proficiency.");
            });
            cases.Add("repeating_crossbow_drop_on_unconsciousness_preserves_loaded_bolt_and_title",()=>{
                var facts=new RepeatingCrossbowFixture(shooterIsAdditional:true);
                var conditions=new ConditionCombatFixture(CCApply("crossbow-sleep","Unconscious",AdditionalTacticalActor.Id,at:new ConditionStamp(T(3))));
                var p=RangedPolicy(fixture:facts,conditions:conditions);var s=World(p);BeginEncounter(s);
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                RangedCommit(s,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:1));
                CCDispatch(s,"crossbow-sleep",AdditionalTacticalActor.Id);var v=s.Capture();var xbow=v.RepeatingCrossbows.Single();
                Require(xbow.HeldBy==""&&xbow.CellX==4&&xbow.CellY==0&&xbow.LoadedBoltLots.SequenceEqual(new[]{RepeatingCrossbowFixture.AmmunitionId})
                    &&xbow.OwnerId==AdditionalTacticalActor.Id&&xbow.CustodianId==AdditionalTacticalActor.Id
                    &&v.Lives.Single(l=>l.ActorId==AdditionalTacticalActor.Id).HeldItems.Count==0
                    &&TestOnlyClubAttackPolicy.ConditionsFor(v,AdditionalTacticalActor.Id).View().Has(ConditionKind.Unconscious),
                    "Condition-caused drop destroyed loaded ammunition, changed ownership or left the weapon held.");
                Require(Bytes(s).SequenceEqual(Bytes(new Simulation(p,codec.Decode(Bytes(s)),ExecutionProfile.Laboratory))),"Dropped loaded crossbow failed replay restore.");
            });
        }
    }
}
#endif
