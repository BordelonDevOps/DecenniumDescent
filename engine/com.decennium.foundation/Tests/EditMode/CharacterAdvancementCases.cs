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
        }
    }
}
#endif
