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
        private static TestOnlySharedWorldPolicy TacticalTechniquePolicy(uint seed=1,long enemyHp=26)
            =>new TestOnlySharedWorldPolicy(SoldierCharacterBuildFixture.ForTacticalTechniques(),new OverwatchFoundationFixture(),
                new CharacterAdvancementFixture(),new SharedCombatFixture(enemyHp,seed));

        private static TestOnlySharedWorldPolicy SuppressionTechniquePolicy(uint seed=1)
            =>new TestOnlySharedWorldPolicy(SoldierCharacterBuildFixture.ForTacticalTechniques(),new OverwatchFoundationFixture(),
                new CharacterAdvancementFixture(null,false,false,true,true,true),new SharedCombatFixture(seed:seed));

        private static uint SeedForSuppressionNatural(int natural)
        {
            for(uint seed=1;seed<1000000;seed++) {
                uint state=seed;for(int i=0;i<3;i++)state=DiceStream.Draw(state,6).NextState;
                if(PlaytestDice.RollD20(state).Natural==natural)return seed;
            }
            throw new InvalidOperationException("No deterministic seed found for Suppression Fire save.");
        }

        private static long NextScheduleSlot(Snapshot s,string actor)
        {
            long count=s.WorldSchedule.Order.Count;long candidate=Array.IndexOf(s.WorldSchedule.Order.ToArray(),actor);
            long current=s.WorldSchedule.ProcessedSlot;
            return candidate<=current?checked(candidate+checked(((current-candidate)/count+1)*count)):candidate;
        }

        private static void AdvanceSuppressionSoldierToLevelThree(Simulation s)
        {
            WorldCommit(s,AwardMilestone(s,"opening.milestone.soldier-2",id:"suppression.milestone.2"));
            WorldCommit(s,AdvanceLevel(s,"opening.milestone.soldier-2",id:"suppression.advance.2"));
            WorldCommit(s,AwardMilestone(s,"opening.milestone.soldier-3",id:"suppression.milestone.3"));
            WorldCommit(s,new Command("suppression.advance.3",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.AdvanceCharacterLevel,
                "opening.milestone.soldier-3",advancement:new CharacterAdvancementRequest(new[]{CharacterFeatureIds.SuppressionFire,
                    CharacterFeatureIds.TacticalAssessment})));
        }

        private static Command TacticalTechniqueCommand(Simulation s,CommandKind kind,string target="")
        {
            var v=s.Capture();string actor=v.Encounter?.CurrentActor??TestOnlyPolicy.ActorId;
            string turn=v.Encounter?.CurrentTurnId??"world.unstarted-turn";
            return new Command("soldier-technique."+(v.Revision+1).ToString(System.Globalization.CultureInfo.InvariantCulture),actor,v.Revision,kind,target,
                ranged:new RangedRequest(turn,RepeatingCrossbowFixture.WeaponId,"",0));
        }

        private static void PrepareSoldierTechniqueTurn(Simulation s)
        {
            BeginEncounter(s);
            var initial=s.Capture().InitialCharacterLoadouts.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
            var doff=new Command("soldier-technique.doff-shield",TestOnlyPolicy.ActorId,s.Capture().Revision,
                CommandKind.DoffPortableShield,initial.ShieldId);
            WorldCommit(s,doff);
            WorldCommit(s,Tac(s,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
            var drop=new Command("soldier-technique.drop-shield",TestOnlyPolicy.ActorId,s.Capture().Revision,
                CommandKind.HandlePortableEquipment,initial.ShieldId,
                inventory:new InventoryRequest(new RuleQuantity(1),"",HandlingKind.Drop));
            WorldCommit(s,drop);
            TacEnd(s);TacEnd(s);TacEnd(s);
            Require(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId
                &&s.Capture().PortableEquipment.Single(x=>x.Id==initial.ShieldId).Placement==PortablePlacement.Ground,
                "The Soldier did not complete the source-approved tactical shield doff and later free-hand drop before reloading.");
            WorldCommit(s,RangedCommand(s,CommandKind.ReloadRepeatingCrossbow,amount:5));
            TacEnd(s);TacEnd(s);TacEnd(s);
            Require(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId,"Three-actor schedule did not return to Soldier after reload.");
        }

        private static void AddSoldierTacticalTechniqueCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("soldier_suppression_fire_is_a_schema33_source_legal_level_three_pair",()=>{
                var p=SuppressionTechniquePolicy();var s=World(p);
                Require(s.Capture().SchemaVersion==Snapshot.SuppressionFireSchema,"The explicit Suppression Fire fixture did not select schema33.");
                AdvanceSuppressionSoldierToLevelThree(s);var v=s.Capture();var before=Bytes(s);
                Require(v.CharacterAdvancements.OrderBy(x=>x.ClassLevel).Select(x=>x.NewTotalLevel).SequenceEqual(new[]{2,3})
                    &&v.CharacterFeatureGrants.Where(x=>x.ClassLevel==3).Select(x=>x.FeatureId).OrderBy(x=>x,StringComparer.Ordinal)
                        .SequenceEqual(new[]{CharacterFeatureIds.SuppressionFire,CharacterFeatureIds.TacticalAssessment}.OrderBy(x=>x,StringComparer.Ordinal))
                    &&before.SequenceEqual(Bytes(new Simulation(p,codec.Decode(before),ExecutionProfile.Laboratory))),
                    "Schema33 did not atomically grant and replay the second legal Soldier level-three pair.");
            });
            cases.Add("soldier_suppression_fire_queries_action_and_three_bolts_without_mutation",()=>{
                var p=SuppressionTechniquePolicy();var s=World(p);AdvanceSuppressionSoldierToLevelThree(s);PrepareSoldierTechniqueTurn(s);
                var before=Bytes(s);uint random=s.Capture().RandomState;
                var commands=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Where(x=>x.Command.Kind==CommandKind.SuppressionFire).ToArray();
                Require(commands.Length==1,"The source-owned Suppression Fire option was not discovered in its authored target fixture.");
                var query=s.QueryCommand(host,commands[0].Command);
                Require(query.Supported&&query.Admissible&&query.Code=="Available"&&query.Costs.Count==2
                    &&query.Costs[0].Kind=="action"&&query.Costs[0].Amount==1&&query.Costs[1].Kind=="ammunition"
                    &&query.Costs[1].Amount==3&&query.Costs[1].ResourceId==RepeatingCrossbowFixture.AmmunitionId
                    &&Bytes(s).SequenceEqual(before)&&s.Capture().RandomState==random,
                    "Suppression Fire query did not expose exactly one Action and three loaded bolts without rolling or mutation.");
            });
            cases.Add("soldier_suppression_fire_records_one_shared_damage_roll_and_saves_then_expires_slow_at_soldier_end",()=>{
                var p=SuppressionTechniquePolicy(SeedForSuppressionNatural(1));var s=World(p);
                AdvanceSuppressionSoldierToLevelThree(s);PrepareSoldierTechniqueTurn(s);
                var command=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Single(x=>x.Command.Kind==CommandKind.SuppressionFire).Command;
                WorldCommit(s,command);var state=s.Capture();var volley=state.SuppressionFireVolleys.Single();var target=volley.Targets.Single();
                var slow=state.SuppressionSlows.Single();var enemy=state.Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id);
                Require(volley.ClassLevel==3&&volley.DamageDice.Length==3&&volley.DamageTotal==volley.DamageDice.Sum()
                    &&target.SaveNatural==1&&!target.SaveSucceeded&&target.Damage==volley.DamageTotal&&target.AfterDefense==target.Damage
                    &&state.RangedAttacks.Length==0&&state.RepeatingCrossbows.Single().LoadedBoltLots.Count==2
                    &&state.CharacterFeatureRuntime.Single().SuppressionFireRechargeRemaining==3
                    &&state.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent
                    &&enemy.Hp==26-target.AfterDefense&&slow.Status==SuppressionSlowStatus.Active
                    &&slow.ExpirySlot==NextScheduleSlot(state,TestOnlyPolicy.ActorId)
                    &&TestOnlyClubAttackPolicy.WalkingSpeed(state,AdditionalTacticalActor.Id)==20,
                    "Suppression Fire did not use one shared 3d6 roll, a full-damage failed save, three bolts, Action, Recharge 3, and a 10-foot slow.");
                var bytes=Bytes(s);s=new Simulation(p,codec.Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(s)),"Suppression Fire rolls, ammunition, recharge, or slow timing changed on save/restore.");
                while(s.Capture().WorldSchedule.ProcessedSlot<=slow.ExpirySlot)TacEnd(s);
                var expired=s.Capture().SuppressionSlows.Single();
                Require(expired.Status==SuppressionSlowStatus.Expired&&TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),AdditionalTacticalActor.Id)==30,
                    "The failed-save slow did not remain through the Soldier's next regular turn End.");
                Require(s.Capture().CharacterFeatureRuntime.Single().SuppressionFireRechargeRemaining==2,
                    "Suppression Fire Recharge did not tick once at the Soldier's next regular Start.");
                int rechargeAdvances=0;
                while(s.Capture().CharacterFeatureRuntime.Single().SuppressionFireRechargeRemaining>0&&rechargeAdvances<12) {
                    TacEnd(s);rechargeAdvances++;
                }
                Require(s.Capture().CharacterFeatureRuntime.Single().SuppressionFireRechargeRemaining==0,
                    "Suppression Fire Recharge did not reach zero after three subsequent Soldier starts.");
            });
            cases.Add("soldier_suppression_fire_success_halves_shared_damage_without_slow_or_attack_roll",()=>{
                var p=SuppressionTechniquePolicy(SeedForSuppressionNatural(20));var s=World(p);
                AdvanceSuppressionSoldierToLevelThree(s);PrepareSoldierTechniqueTurn(s);
                var command=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Single(x=>x.Command.Kind==CommandKind.SuppressionFire).Command;
                WorldCommit(s,command);var state=s.Capture();var volley=state.SuppressionFireVolleys.Single();var target=volley.Targets.Single();
                Require(target.SaveNatural==20&&target.SaveSucceeded&&target.Damage==volley.DamageTotal/2
                    &&state.SuppressionSlows.Length==0&&state.RangedAttacks.Length==0
                    &&state.Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Hp==26-target.AfterDefense,
                    "A successful Suppression Fire save did not halve rounded-down shared damage without a slow or attack roll.");
            });
            cases.Add("soldier_suppression_fire_rejects_an_unauthored_zone_before_cost_or_randomness",()=>{
                var p=SuppressionTechniquePolicy();var s=World(p);AdvanceSuppressionSoldierToLevelThree(s);PrepareSoldierTechniqueTurn(s);
                var invalid=new Command("suppression.invalid-zone",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.SuppressionFire,x:3,y:0,
                    suppressionFire:new SuppressionFireRequest(s.Capture().Encounter.CurrentTurnId,RepeatingCrossbowFixture.WeaponId,
                        new[]{AdditionalTacticalActor.Id}));
                RejectUnchanged(s,host,invalid,"SuppressionZoneOutsideAuthoredFixture");
            });
            cases.Add("soldier_schema29_is_explicit_opt_in_and_preserves_schema28_build_schedule",()=>{
                var legacyPolicy=new TestOnlySharedWorldPolicy(new SoldierCharacterBuildFixture(),new OverwatchFoundationFixture(),
                    new CharacterAdvancementFixture(),new SharedCombatFixture());
                var legacy=World(legacyPolicy);var sourcePolicy=TacticalTechniquePolicy();var source=World(sourcePolicy);
                Require(legacy.Capture().SchemaVersion==Snapshot.SoldierInitialBuildSchema
                    &&legacy.Capture().WorldSchedule.Order.Count==2&&legacy.Capture().TacticalAllies.Length==0
                    &&legacy.Capture().SoldierTacticalEffects.Length==0
                    &&source.Capture().SchemaVersion==Snapshot.SoldierTacticalTechniquesSchema
                    &&source.Capture().WorldSchedule.Order.SequenceEqual(new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId,AdditionalTacticalActor.Id})
                    &&source.Capture().TacticalAllies.Single().Includes(TestOnlyPolicy.ActorId)
                    &&source.Capture().TacticalAllies.Single().Other(TestOnlyPolicy.ActorId)==TestOnlyPolicy.CompanionId,
                    "Schema29 schedule/alliance leaked into the schema28 default or did not initialize through explicit opt-in.");
            });
            cases.Add("soldier_tactical_technique_queries_are_pure_and_report_one_action_one_loaded_bolt",()=>{
                var p=TacticalTechniquePolicy();var s=World(p);PrepareSoldierTechniqueTurn(s);var before=Bytes(s);uint random=s.Capture().RandomState;
                var discovered=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Where(x=>x.Command.Kind==CommandKind.WarningShot
                    ||x.Command.Kind==CommandKind.CoveringFire).ToArray();
                Require(discovered.Length==2,"Both selected Soldier ranged techniques were not discovered.");
                foreach(var option in discovered) {
                    var query=s.QueryCommand(host,option.Command);
                    Require(query.Supported&&query.Admissible&&query.Code=="Available"&&query.Costs.Count==2
                        &&query.Costs[0].Kind=="action"&&query.Costs[0].Amount==1&&query.Costs[1].Kind=="ammunition"
                        &&query.Costs[1].Amount==1&&query.Costs[1].ResourceId==s.Capture().RepeatingCrossbows.Single().LoadedBoltLots[0],
                        option.Command.Kind+" query did not expose its actual shared Action and loaded bolt costs.");
                    s.QueryCommand(host,option.Command);
                }
                Require(Bytes(s).SequenceEqual(before)&&s.Capture().RandomState==random,"Repeated tactical technique query changed state or RNG.");
            });
            cases.Add("soldier_warning_shot_critical_uses_weapon_dice_only_and_roundtrips_effect",()=>{
                var p=TacticalTechniquePolicy(SeedForNatural(20));var s=World(p);PrepareSoldierTechniqueTurn(s);
                var option=s.DiscoverCommands(host,TestOnlyPolicy.ActorId).Single(x=>x.Command.Kind==CommandKind.WarningShot);
                WorldCommit(s,option.Command);var v=s.Capture();var shot=v.RangedAttacks.Single();var effect=v.SoldierTacticalEffects.Single();
                Require(shot.Attack.Hit&&shot.Attack.Critical&&shot.Damage.Dice.Count==2&&shot.Damage.FlatModifier==0
                    &&shot.Damage.Total==shot.Damage.Dice.Sum()&&shot.TargetId==AdditionalTacticalActor.Id
                    &&v.RepeatingCrossbows.Single().LoadedBoltLots.Count==4
                    &&v.CharacterFeatureRuntime.Single().WarningShotRechargeRemaining==2
                    &&effect.Kind==SoldierTacticalEffectKind.WarningShot&&effect.Status==SoldierTacticalEffectStatus.Active
                    &&effect.OriginAttackId==shot.Id&&effect.ExpiryActorId==AdditionalTacticalActor.Id
                    &&effect.ExpiryPhase==SoldierTacticalEffectPhase.End,
                    "Critical Warning Shot did not spend one loaded bolt, use weapon dice only, start Recharge 2, and apply its next-attack rider.");
                var path=Path.Combine(directory,"soldier-warning-shot-active.ddsave");new FileSaveStore().Save(path,v);
                var restored=new Simulation(p,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(restored))&&restored.Capture().SoldierTacticalEffects.Single().SameAs(effect),
                    "Active Warning Shot, recharge, or timing marker changed on save/restore.");
            });
            cases.Add("soldier_warning_shot_miss_pays_action_ammunition_and_recharge_without_rider",()=>{
                var p=TacticalTechniquePolicy(SeedForNatural(1));var s=World(p);PrepareSoldierTechniqueTurn(s);
                WorldCommit(s,TacticalTechniqueCommand(s,CommandKind.WarningShot,AdditionalTacticalActor.Id));var v=s.Capture();
                Require(v.RangedAttacks.Single().Attack.Selected==1&&!v.RangedAttacks.Single().Attack.Hit
                    &&v.RangedAttacks.Single().Damage.Dice.Count==0&&v.RangedAttacks.Single().Damage.DiceWords==0
                    &&v.RepeatingCrossbows.Single().LoadedBoltLots.Count==4&&v.CharacterFeatureRuntime.Single().WarningShotRechargeRemaining==2
                    &&v.SoldierTacticalEffects.Length==0&&v.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,
                    "Legal Warning Shot miss refunded its Action/ammunition, rolled damage, or applied a rider.");
            });
            cases.Add("soldier_warning_shot_expires_at_target_end_and_recharge_ticks_on_owner_starts",()=>{
                var p=TacticalTechniquePolicy(SeedForNatural(20));var s=World(p);PrepareSoldierTechniqueTurn(s);
                WorldCommit(s,TacticalTechniqueCommand(s,CommandKind.WarningShot,AdditionalTacticalActor.Id));
                TacEnd(s);TacEnd(s);
                var targetStart=s.Capture();Require(targetStart.Encounter.CurrentActor==AdditionalTacticalActor.Id
                    &&targetStart.SoldierTacticalEffects.Single().Status==SoldierTacticalEffectStatus.Active,
                    "Warning Shot expired before the target completed its next future turn.");
                TacEnd(s);var afterTarget=s.Capture();
                Require(afterTarget.SoldierTacticalEffects.Single().Status==SoldierTacticalEffectStatus.Expired
                    &&afterTarget.CharacterFeatureRuntime.Single().WarningShotRechargeRemaining==1,
                    "Warning Shot did not expire at target End or its Recharge failed to tick at the Soldier's next Start.");
                TacEnd(s);TacEnd(s);TacEnd(s);
                Require(s.Capture().CharacterFeatureRuntime.Single().WarningShotRechargeRemaining==0,
                    "Recharge 2 did not become ready after exactly two later Soldier regular Starts.");
            });
            cases.Add("soldier_covering_fire_penalizes_ally_targeted_opportunity_attack_and_consumes_on_roll",()=>{
                var p=TacticalTechniquePolicy(SeedForNatural(20));var s=World(p);PrepareSoldierTechniqueTurn(s);
                WorldCommit(s,TacticalTechniqueCommand(s,CommandKind.CoveringFire,AdditionalTacticalActor.Id));
                var applied=s.Capture().SoldierTacticalEffects.Single();Require(applied.Kind==SoldierTacticalEffectKind.CoveringFire
                    &&applied.Status==SoldierTacticalEffectStatus.Active&&applied.ExpiryActorId==TestOnlyPolicy.ActorId
                    &&applied.ExpiryPhase==SoldierTacticalEffectPhase.Start,"Covering Fire did not capture its applying Soldier's next Start deadline.");
                var restored=new Simulation(p,codec.Decode(Bytes(s)),ExecutionProfile.Laboratory);Require(Bytes(s).SequenceEqual(Bytes(restored)),
                    "Covering Fire did not survive canonical persistence.");s=restored;
                TacEnd(s);
                WorldCommit(s,Tac(s,CommandKind.TacticalStep,actor:TestOnlyPolicy.CompanionId,x:4,y:3));
                WorldCommit(s,Tac(s,CommandKind.TacticalStep,actor:TestOnlyPolicy.CompanionId,x:4,y:2));
                WorldCommit(s,Tac(s,CommandKind.TacticalStep,actor:TestOnlyPolicy.CompanionId,x:4,y:1));
                WorldCommit(s,Tac(s,CommandKind.TacticalStep,actor:TestOnlyPolicy.CompanionId,x:3,y:2));
                var pending=TestOnlyClubAttackPolicy.PendingMove(s.Capture());
                Require(pending!=null&&pending.Reactors.SequenceEqual(new[]{AdditionalTacticalActor.Id}),
                    "Companion departure did not offer the marked enemy an opportunity attack before Covering Fire expiry.");
                CommitTac(s,Opportunity(s,true,AdditionalTacticalActor.ClubId));var v=s.Capture();
                var attack=v.MeleeAttacks.Single(x=>x.Opportunity);var effect=v.SoldierTacticalEffects.Single();
                var audit=v.TacticalAttackAudits.Single(x=>x.AttackId==attack.Id);
                Require(attack.AttackerId==AdditionalTacticalActor.Id&&attack.TargetId==TestOnlyPolicy.CompanionId
                    &&attack.Attack.Modifier==-2&&effect.Status==SoldierTacticalEffectStatus.Consumed&&effect.ResolutionId==attack.Id
                    &&audit.ConsumedEffectIds.Contains(effect.Id),
                    "Covering Fire did not apply -2 to the enemy's opportunity attack against the Soldier's ally or consume/audit that attempted roll.");
                var roundtrip=new Simulation(p,codec.Decode(Bytes(s)),ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(roundtrip)),"Consumed Covering Fire and its attack audit changed on save/restore.");
            });
        }
    }
}
#endif
