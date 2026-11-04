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
        private static TestOnlySharedWorldPolicy AdvancementPolicy(ActorLifeRecord life=null)
            =>new TestOnlySharedWorldPolicy(new CharacterAdvancementFixture(life),new SharedCombatFixture());
        private static Command AwardMilestone(Simulation s,string milestone="opening.milestone.soldier-2",string actor=null,string id="milestone.award")
            =>new Command(id,actor??TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AwardCharacterMilestone,milestone);
        private static Command AdvanceLevel(Simulation s,string milestone="opening.milestone.soldier-2",string one=CharacterAdvancementFixture.DefensivePositioning,
            string two=CharacterAdvancementFixture.TacticalReposition,string id="character.advance")
            =>new Command(id,TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,milestone,
                advancement:new CharacterAdvancementRequest(one,two));
        private static void AddCharacterAdvancementCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("character_advancement_schema21_starts_as_source_scoped_soldier1",()=>{
                var p=AdvancementPolicy();var s=new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);var v=s.Capture();
                Require(v.SchemaVersion==Snapshot.CharacterAdvancementSchema&&v.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Single().ClassName=="Soldier"
                    &&v.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Single().BaseHp==10
                    &&v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).MaximumHp==10&&v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Hp==4
                    &&v.CharacterHitDice.Single().DieSize==10&&!v.CharacterHitDice.Single().Spent&&v.CharacterFeatureGrants.Length==0
                    &&v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).HeldItems.SequenceEqual(new[]{TestOnlyClubAttackPolicy.ActorClub})
                    &&v.Clubs.Single(x=>x.Id==TestOnlyClubAttackPolicy.ActorClub).HeldBy==TestOnlyPolicy.ActorId,
                    "Initial progression facts are not the fixed Soldier 1 baseline.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),"Schema21 initial state did not roundtrip.");
            });
            cases.Add("character_advancement_rejects_missing_hit_dice_and_unknown_feature_grants",()=>{
                var p=AdvancementPolicy();var initial=World(p).Capture();var missingDice=initial.Copy();missingDice.CharacterHitDice=Array.Empty<CharacterHitDieRecord>();
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(missingDice));
                var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));var invalid=s.Capture();var grant=invalid.CharacterFeatureGrants[0];
                invalid.CharacterFeatureGrants[0]=new CharacterFeatureGrantRecord(grant.ActorId,"soldier.base.unimplemented",grant.ClassName,grant.ClassLevel,grant.MilestoneId,grant.GrantedRevision);
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(invalid));
                foreach(int schema in new[]{21,22,23}) {
                    invalid=s.Capture();invalid.SchemaVersion=schema;
                    invalid.CharacterFeatureGrants=invalid.CharacterFeatureGrants.Concat(new[]{new CharacterFeatureGrantRecord(TestOnlyPolicy.ActorId,
                        CharacterFeatureIds.Overwatch,"Soldier",1,"opening.milestone.soldier-2",invalid.CharacterAdvancements.Single().Revision)}).ToArray();
                    Throws<ArgumentException>(()=>new SnapshotCodec().Encode(invalid));
                }
            });
            cases.Add("character_advancement_requires_host_award_and_unique_milestone",()=>{
                var p=AdvancementPolicy();var s=World(p);var noHost=new Authority("observer",new[]{TestOnlyPolicy.ActorId});
                RejectUnchanged(s,noHost,AwardMilestone(s),"NotAuthorized");
                var emptyControlHost=new Authority("director",Array.Empty<string>(),canModifyWorld:true);
                var award=s.Execute(emptyControlHost,AwardMilestone(s));Require(award.Outcome==Outcome.Committed,"World authority could not award milestone to a non-controlled actor.");
                var before=Bytes(s);var duplicate=s.Execute(emptyControlHost,AwardMilestone(s,id:"milestone.award.again"));
                Require(duplicate.Outcome==Outcome.Rejected&&duplicate.Code=="MilestoneAlreadyAwarded"&&before.SequenceEqual(Bytes(s)),"Semantic duplicate milestone was not rejected unchanged.");
            });
            cases.Add("character_advancement_preserves_a_spent_prior_hit_die",()=>{
                var p=new TestOnlySharedWorldPolicy(new CharacterAdvancementFixture(null,startingHitDieSpent:true),new SharedCombatFixture());
                var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));
                var dice=s.Capture().CharacterHitDice.Where(x=>x.ActorId==TestOnlyPolicy.ActorId).OrderBy(x=>x.LevelOrdinal).ToArray();
                Require(dice.Length==2&&dice[0].Spent&&!dice[1].Spent,"Level gain refreshed a spent Hit Die or failed to add one unspent Hit Die.");
            });
            cases.Add("character_advancement_incomplete_and_unsupported_selections_are_atomic",()=>{
                var p=AdvancementPolicy();var s=World(p);WorldCommit(s,AwardMilestone(s));
                RejectUnchanged(s,host,AdvanceLevel(s,one:"",two:""),"IncompleteFeatureSelection");
                RejectUnchanged(s,host,AdvanceLevel(s,one:"soldier.base.unknown",two:CharacterAdvancementFixture.TacticalReposition,id:"character.advance.unsupported"),"UnsupportedFeatureSelection");
                Require(s.Capture().CharacterMilestones.Single().ConsumedRevision==0&&s.Capture().Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Levels.Count==1,
                    "Rejected selection consumed the entitlement or partially advanced the character.");
            });
            cases.Add("character_advancement_fixed_average_grants_cards_and_hit_die_without_healing",()=>{
                var p=AdvancementPolicy();var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));var v=s.Capture();
                var character=v.Characters.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);var life=v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                var result=v.CharacterAdvancements.Single();
                Require(v.SchemaVersion==21&&character.Levels.Count==2&&character.Levels[1].BaseHp==6&&life.MaximumHp==16&&life.Hp==4
                    &&v.CharacterHitDice.Count(x=>x.ActorId==TestOnlyPolicy.ActorId)==2&&!v.CharacterHitDice.Single(x=>x.LevelOrdinal==1).Spent
                    &&!v.CharacterHitDice.Single(x=>x.LevelOrdinal==2).Spent&&v.CharacterFeatureGrants.Select(x=>x.FeatureId).OrderBy(x=>x,StringComparer.Ordinal)
                        .SequenceEqual(new[]{CharacterAdvancementFixture.DefensivePositioning,CharacterAdvancementFixture.TacticalReposition}.OrderBy(x=>x,StringComparer.Ordinal))
                    &&v.CharacterMilestones.Single().ConsumedRevision==v.Revision&&result.HitPointMethod==HitPointGainMethod.FixedAverage
                    &&result.MaximumHpBefore==10&&result.MaximumHpAfter==16&&result.CurrentHpBefore==4&&result.CurrentHpAfter==4,
                    "Advancement did not preserve current HP while recording the sourced fixed-average increase and exact grants.");
                var bytes=Bytes(s);var restored=new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(restored)),"Advancement replay changed canonical save bytes.");
                var path=Path.Combine(directory,"soldier-level2.bin");new FileSaveStore().Save(path,v);
                Require(bytes.SequenceEqual(new SnapshotCodec().Encode(new FileSaveStore().Load(path))),"Schema21 advancement save did not persist.");
            });
            cases.Add("character_advancement_waits_for_traversal_and_tactical_control",()=>{
                var p=AdvancementPolicy();var s=World(p);WorldCommit(s,AwardMilestone(s));
                WorldCommit(s,new Command("level.traversal",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginWorldStep,"walk",1,0));
                RejectUnchanged(s,host,AdvanceLevel(s,id:"advance.during.traversal"),"CharacterBusy");
                s=World(AdvancementPolicy());WorldCommit(s,AwardMilestone(s));
                WorldCommit(s,new Command("level.begin.combat",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                RejectUnchanged(s,host,AdvanceLevel(s,id:"advance.during.tactical"),"TacticalControlActive");
            });
            cases.Add("character_advancement_preserves_down_state_and_temporary_resources",()=>{
                var initial=new ActorLifeRecord(TestOnlyPolicy.ActorId,10,0,3,new[]{2},true,false,true,3,1,new RuleTime(60),0,true,new[]{TestOnlyClubAttackPolicy.ActorClub});
                var p=AdvancementPolicy(initial);var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));var life=s.Capture().Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                Require(life.MaximumHp==16&&life.Hp==0&&life.TemporaryHp==3&&life.LinkedInjuries.SequenceEqual(new[]{2})&&life.Stable&&!life.Dead
                    &&life.UsesDeathSaves&&life.DeathSuccesses==3&&life.DeathFailures==1&&life.StableUntil==new RuleTime(60)&&life.Prone,
                    "Level advancement healed or rewrote incapacitated life state.");
            });
            cases.Add("soldier_features_apply_explicit_cover_and_tactical_reposition_preserves_press",()=>{
                uint seed=1;while(PlaytestDice.RollD20(seed).Natural<11||PlaytestDice.RollD20(seed).Natural==20)seed++;
                var life=new ActorLifeRecord(TestOnlyPolicy.ActorId,10,10,0,Array.Empty<int>(),false,false,true,0,0,null,0,false,new[]{TestOnlyClubAttackPolicy.ActorClub});
                var fixture=new CharacterAdvancementFixture(life,new TacticalCoverRecord("cover.stone-pillar",1,1));
                var p=new TestOnlySharedWorldPolicy(fixture,new SharedCombatFixture(seed:seed));var s=World(p);
                WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));WorldAdvance(s,3);
                WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);WorldAdvance(s,1);WorldStep(s,1,0);
                Require(s.Capture().InventoryCombat&&s.Capture().Encounter.CurrentActor==AdditionalTacticalActor.Id,
                    "The combat fixture did not enter on its authored initiative slot.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive,actor:AdditionalTacticalActor.Id));
                WorldCommit(s,Tac(s,CommandKind.TacticalStep,x:3,y:0,actor:AdditionalTacticalActor.Id));
                WorldCommit(s,Tac(s,CommandKind.AttackClub,target:TestOnlyPolicy.ActorId,actor:AdditionalTacticalActor.Id,weapon:AdditionalTacticalActor.ClubId));
                Require(s.Capture().MeleeAttacks.Single().Attack.ArmorClass==11&&s.Capture().Presses.Any(x=>x.ActorId==AdditionalTacticalActor.Id&&x.TargetId==TestOnlyPolicy.ActorId),
                    "Explicit qualifying cover did not grant +1 AC, or the source attack failed to arm Press.");
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                var feature=Tac(s,CommandKind.ActivateTacticalReposition);WorldCommit(s,feature);
                long ordinarySpent=WorldLedger(s).MovementSpent.Numerator;
                var runtime=s.Capture().CharacterFeatureRuntime.Single();
                Require(runtime.RepositionRechargeRemaining==2&&!runtime.BonusActionAvailable&&runtime.RepositionBudgetRemaining==15,
                    "Activation did not spend its Bonus Action or establish the half-Speed budget and Recharge 2.");
                WorldCommit(s,Tac(s,CommandKind.TacticalRepositionStep,x:1,y:0));
                var state=s.Capture();var offer=state.PressOffers.Single(x=>x.Status==PressOfferStatus.Pending);
                Require(state.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==1&&state.TacticalMoves.Last().Kind==TacticalMoveKind.TacticalReposition
                    &&state.TacticalMoves.Last().Reactors.Count==0&&state.MeleeAttacks.Length==1&&state.CharacterFeatureRuntime.Single().RepositionBudgetRemaining==10
                    &&WorldLedger(s).MovementSpent.Numerator==ordinarySpent&&offer.ActorId==AdditionalTacticalActor.Id,
                    "Reposition provoked an OA, spent ordinary movement, lost Press, or mispaid its special budget.");
                WorldCommit(s,Tac(s,CommandKind.RespondPress,target:offer.Id,actor:AdditionalTacticalActor.Id,choice:true));
                WorldCommit(s,Tac(s,CommandKind.TacticalRepositionStep,x:0,y:0));
                Require(s.Capture().TacticalMoves.Last().Kind==TacticalMoveKind.TacticalReposition&&s.Capture().CharacterFeatureRuntime.Single().RepositionBudgetRemaining==5
                    &&s.Capture().TacticalActors.Single(x=>x.ActorId==AdditionalTacticalActor.Id).PressConsumed,
                    "Accepted Press did not resolve before continuing the paid reposition budget.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                Require(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId&&s.Capture().CharacterFeatureRuntime.Single().RepositionRechargeRemaining==1
                    &&s.Capture().CharacterFeatureRuntime.Single().BonusActionAvailable,"Recharge did not advance on the Soldier's next regular start.");
                RejectUnchanged(s,host,Tac(s,CommandKind.ActivateTacticalReposition),"TacticalRepositionRecharging");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Aggressive));WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                Require(s.Capture().CharacterFeatureRuntime.Single().RepositionRechargeRemaining==0,"Recharge 2 did not become ready after two of the Soldier's regular starts.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),"Feature runtime did not survive canonical replay.");
            });
            cases.Add("overwatch_schema24_separates_automatic_grant_and_persists_shared_bonus_actions",()=>{
                var p=new TestOnlySharedWorldPolicy(new OverwatchFoundationFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);var v=s.Capture();var automatic=v.CharacterFeatureGrants.Single();
                Require(v.SchemaVersion==Snapshot.SharedBonusActionSchema&&v.BonusActions.Length==2
                    &&v.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).LastRegularStart==0
                    &&v.BonusActions.All(x=>x.Available)&&automatic.FeatureId==CharacterFeatureIds.Overwatch
                    &&automatic.Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature&&automatic.MilestoneId==""&&automatic.GrantedRevision==0
                    &&v.CharacterFeatureGrants.Count(x=>x.Origin==CharacterFeatureGrantOrigin.SelectedCard)==0,
                    "Schema24 did not model the shared interval budget and automatic Overwatch outside selected-card grants.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(v);var restored=codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(restored))&&restored.CharacterFeatureGrants.Single().Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature,
                    "Schema24 origin or action budget did not survive canonical save encoding.");
                var missing=v.Copy();missing.BonusActions=missing.BonusActions.Take(1).ToArray();Throws<ArgumentException>(()=>codec.Encode(missing));
                var stale=v.Copy();stale.BonusActions=stale.BonusActions.Select(x=>x.ActorId==TestOnlyPolicy.ActorId?new ActorBonusActionRecord(x.ActorId,-1):x).ToArray();
                Throws<ArgumentException>(()=>codec.Encode(stale));
            });
            cases.Add("overwatch_schema24_reposition_spends_shared_budget_and_regular_start_refills_it",()=>{
                var p=new TestOnlySharedWorldPolicy(new OverwatchFoundationFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);WorldCommit(s,AwardMilestone(s));WorldCommit(s,AdvanceLevel(s));
                WorldCommit(s,new Command("schema24.begin.combat",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.ActivateTacticalReposition));var after=s.Capture();
                Require(!after.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available
                    &&!after.CharacterFeatureRuntime.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).BonusActionAvailable,
                    "Tactical Reposition did not consume the common schema24 Bonus Action budget.");
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                var refreshed=s.Capture();Require(refreshed.Encounter.CurrentActor==TestOnlyPolicy.ActorId
                    &&refreshed.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available
                    &&refreshed.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).LastRegularStart==2
                    &&refreshed.CharacterFeatureRuntime.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).BonusActionAvailable
                    &&refreshed.CharacterFeatureRuntime.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).RepositionRechargeRemaining==1,
                    "The next regular start did not refill the shared Bonus Action budget and independently advance Reposition Recharge.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),
                    "Schema24 shared action budget did not survive command replay.");
            });
            cases.Add("overwatch_schema25_designation_spends_shared_bonus_action_and_persists_zone",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event","fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                var p=new TestOnlySharedWorldPolicy(new OverwatchDesignationFixture(),new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);Require(s.Capture().SchemaVersion==Snapshot.OverwatchSchema&&s.Capture().OverwatchIntervals.Single().ShotStatus==OverwatchShotStatus.Available,
                    "Schema25 did not initialize the interval-owned Overwatch entitlement.");
                WorldCommit(s,new Command("schema25.begin.combat",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                var designation=new Command("schema25.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:1,y:-1);
                WorldCommit(s,designation);var v=s.Capture();var zone=v.OverwatchDesignations.Single();
                Require(zone.Status==OverwatchDesignationStatus.Active&&zone.Contains(3,0)&&!zone.Contains(4,0)
                    &&v.OverwatchIntervals.Single().ShotStatus==OverwatchShotStatus.Available
                    &&!v.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                    "Designation did not persist its fixed 3-by-3 zone, preserve the interval shot, or spend the common Bonus Action.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(v);var restored=codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(restored))&&zone.SameAs(restored.OverwatchDesignations.Single()),
                    "Schema25 designation did not survive canonical save encoding.");
                var second=new Command("schema25.designate.again",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:1,y:-1);
                RejectUnchanged(s,host,second,"BonusActionUnavailable");
                Require(s.Capture().OverwatchDesignations.Single().Status==OverwatchDesignationStatus.Active,
                    "A rejected redeployment removed the previously active zone.");
            });
            cases.Add("overwatch_schema25_redeployment_replaces_zone_and_preserves_each_interval_shot_status",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event","fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                var p=new TestOnlySharedWorldPolicy(new OverwatchDesignationFixture(),new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var designated=World(p);WorldCommit(designated,new Command("schema25.replace.begin",TestOnlyPolicy.ActorId,designated.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(designated,Tac(designated,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(designated,new Command("schema25.replace.first",TestOnlyPolicy.ActorId,designated.Capture().Revision,CommandKind.DesignateOverwatch,
                    designated.Capture().Encounter.CurrentTurnId,x:1,y:-1));
                var baseState=designated.Capture();
                foreach(var status in new[]{OverwatchShotStatus.Available,OverwatchShotStatus.Spent,OverwatchShotStatus.Forfeited}) {
                    var seeded=baseState.Copy();
                    seeded.OverwatchIntervals=seeded.OverwatchIntervals.Select(x=>x.ActorId==TestOnlyPolicy.ActorId?x.WithStatus(status):x).ToArray();
                    seeded.BonusActions=seeded.BonusActions.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                        ?new ActorBonusActionRecord(x.ActorId,x.LastRegularStart,true):x).ToArray();
                    seeded.CharacterFeatureRuntime=seeded.CharacterFeatureRuntime.Select(x=>x.ActorId==TestOnlyPolicy.ActorId
                        ?x.WithBonusActionAvailable(true):x).ToArray();
                    // The current Base fixture has one Bonus Action per interval, so its normal
                    // command sequence cannot redeploy before the zone expires. Exercise the
                    // agreed replacement transition directly with a structurally valid available
                    // ledger; this does not add a second Bonus Action grant to the fixture.
                    var replacement=new Command("schema25.replace."+(int)status,TestOnlyPolicy.ActorId,seeded.Revision,
                        CommandKind.DesignateOverwatch,seeded.Encounter.CurrentTurnId,x:1,y:-1);
                    Require(p.Resolve(seeded,replacement)==null,"A valid available Bonus Action did not permit replacement.");
                    var after=seeded;var old=after.OverwatchDesignations.Single(x=>x.CreatedRevision==baseState.Revision);
                    var current=after.OverwatchDesignations.Single(x=>x.Status==OverwatchDesignationStatus.Active);
                    Require(old.Status==OverwatchDesignationStatus.Replaced&&current.Id!=old.Id&&current.LastRegularStart==old.LastRegularStart
                        &&after.OverwatchIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ShotStatus==status
                        &&!after.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                        "Redeployment failed to replace only the zone, preserve its interval endpoint/shot status, and spend the available shared Bonus Action.");
                }
            });
            cases.Add("overwatch_schema25_interval_history_compacts_after_sparse_long_world_advance",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event","fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                var p=new TestOnlySharedWorldPolicy(new OverwatchDesignationFixture(),new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);WorldAdvance(s,1000);var v=s.Capture();
                Require(v.OverwatchIntervals.Length<=2&&v.OverwatchIntervals.Where(x=>x.ActorId==TestOnlyPolicy.ActorId)
                    .OrderByDescending(x=>x.LastRegularStart).First().LastRegularStart>64,
                    "A large sparse calendar advance retained unbounded Overwatch interval history or failed to reach the new interval.");
            });
            cases.Add("overwatch_schema25_rejects_unknown_placement_and_invisible_zone_before_payment",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event", "fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                TestOnlySharedWorldPolicy Policy(OverwatchDesignationFixture fixture)=>new TestOnlySharedWorldPolicy(fixture,new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(Policy(new OverwatchDesignationFixture()));
                WorldCommit(s,new Command("schema25.invalid.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                RejectUnchanged(s,host,new Command("schema25.unknown.zone",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:2,y:-1),"UnsupportedOverwatchPlacement");
                var invisible=World(Policy(new OverwatchDesignationFixture(1,-1,false)));
                WorldCommit(invisible,new Command("schema25.invisible.begin",TestOnlyPolicy.ActorId,invisible.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(invisible,Tac(invisible,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                RejectUnchanged(invisible,host,new Command("schema25.invisible.zone",TestOnlyPolicy.ActorId,invisible.Capture().Revision,CommandKind.DesignateOverwatch,
                    invisible.Capture().Encounter.CurrentTurnId,x:1,y:-1),"OverwatchZoneNotVisible");
                Require(invisible.Capture().OverwatchDesignations.Length==0&&invisible.Capture().BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                    "An invisible-zone rejection mutated the designation or Bonus Action ledger.");
            });
            cases.Add("overwatch_schema25_zone_expires_and_interval_entitlement_refreshes_at_next_soldier_start",()=>{
                var periodic=new PeriodicRiderFixture(new[]{new PeriodicRiderApplicationFact("fixture.bleed.event","fixture.bleed",TestOnlyPolicy.ActorId,AdditionalTacticalActor.Id,10)});
                var p=new TestOnlySharedWorldPolicy(new OverwatchDesignationFixture(),new OverwatchFoundationFixture(),periodic,
                    new RepeatingCrossbowFixture(),new CharacterAdvancementFixture(),new SharedCombatFixture());
                var s=World(p);WorldCommit(s,new Command("schema25.expire.begin",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.BeginFixedEncounter));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,new Command("schema25.expire.designate",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.DesignateOverwatch,
                    s.Capture().Encounter.CurrentTurnId,x:1,y:-1));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn));
                WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,actor:AdditionalTacticalActor.Id,stance:(int)CombatStance.Aggressive));
                WorldCommit(s,Tac(s,CommandKind.EndRegularTurn,actor:AdditionalTacticalActor.Id));
                var v=s.Capture();var interval=v.OverwatchIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId&&x.LastRegularStart==2);
                Require(interval.ShotStatus==OverwatchShotStatus.Available&&v.OverwatchDesignations.Single().Status==OverwatchDesignationStatus.Expired
                    &&v.OverwatchDesignations.Single().EndedRevision==v.Revision
                    &&v.BonusActions.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Available,
                    "The previous zone survived the next regular start or the new interval did not refresh its shot and Bonus Action.");
                var bytes=Bytes(s);Require(bytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory))),
                    "Schema25 interval refresh did not survive command-history replay.");
            });
        }
    }
}
#endif
