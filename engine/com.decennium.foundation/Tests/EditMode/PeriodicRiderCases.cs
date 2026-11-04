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
        private static ActorLifeRecord PeriodicHeroLife(long hp=10)=>new ActorLifeRecord(TestOnlyPolicy.ActorId,10,hp,0,Array.Empty<int>(),
            false,false,true,0,0,null,0,false,new[]{TestOnlyClubAttackPolicy.ActorClub});
        private static PeriodicRiderApplicationFact PeriodicApp(string eventId="bleed.event.one",string riderId="bleed.record.one",
            string owner=AdditionalTacticalActor.Id,string target=TestOnlyPolicy.ActorId,int dc=10,RuleTime at=default)
            =>new PeriodicRiderApplicationFact(eventId,riderId,owner,target,dc,at);
        private static PeriodicRiderFixture PeriodicFixture(PeriodicRiderApplicationFact[] apps,PeriodicHealingFact healing=null,int medicineRank=2,
            PeriodicRiderRecord[] initialRiders=null)
            =>new PeriodicRiderFixture(apps,new[]{new PeriodicMedicineFact(TestOnlyPolicy.ActorId,medicineRank)},healing,initialRiders);
        private static TestOnlySharedWorldPolicy PeriodicPolicy(PeriodicRiderFixture fixture,uint seed=1,long heroHp=10,SharedResearchFixture research=null)
        {
            var advancement=new CharacterAdvancementFixture(PeriodicHeroLife(heroHp));var combat=new SharedCombatFixture(seed:seed);
            return research==null?new TestOnlySharedWorldPolicy(fixture,advancement,combat)
                :new TestOnlySharedWorldPolicy(fixture,advancement,combat,research);
        }
        private static void PeriodicBegin(Simulation s)=>WorldCommit(s,IC(s,CommandKind.BeginFixedEncounter));
        private static void PeriodicApply(Simulation s,PeriodicRiderApplicationFact fact)
            =>WorldCommit(s,Tac(s,CommandKind.DispatchFixturePeriodicRider,fact.EventId,actor:fact.OwnerId));
        private static void PeriodicEndTurn(Simulation s)=>ConnectedEnd(s);
        private static void PeriodicAdvanceToTargetStart(Simulation s){PeriodicEndTurn(s);PeriodicEndTurn(s);}
        private static uint PeriodicSeed(Func<D20Roll,bool> predicate)
        {
            for(uint seed=1;seed<100000;seed++)if(predicate(PlaytestDice.RollD20(seed)))return seed;
            throw new Exception("No deterministic Medicine test seed found.");
        }
        private static void AddPeriodicRiderCases(Dictionary<string,Action> cases,string directory)
        {
            var codec=new SnapshotCodec();
            cases.Add("periodic_rider_schema23_registered_profile_roundtrips_without_unity",()=>{
                var p=PeriodicPolicy(PeriodicFixture(new[]{PeriodicApp()}));var s=World(p);var v=s.Capture();var encoded=codec.Encode(v);
                Require(v.SchemaVersion==Snapshot.PeriodicRiderSchema&&v.PeriodicRiders.Length==0&&v.SkillTraining.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ProficiencyRank==2
                    &&encoded.SequenceEqual(codec.Encode(codec.Decode(encoded))),"Schema23 registration, explicit Medicine training or canonical save encoding failed.");
                Throws<InvalidOperationException>(()=>new Simulation(p,v,ExecutionProfile.Release));
            });
            cases.Add("periodic_rider_tick_uses_next_target_start_and_survives_save_replay",()=>{
                var p=PeriodicPolicy(PeriodicFixture(new[]{PeriodicApp()}));var s=World(p);PeriodicBegin(s);PeriodicApply(s,PeriodicApp());
                var before=s.Capture();var restored=new Simulation(p,codec.Decode(Bytes(s)),ExecutionProfile.Laboratory);
                Require(before.PeriodicRiders.Single().NextStartSlot==2&&before.PeriodicRiders.Single().RemainingTicks==1,
                    "Application did not capture the next regular target Start.");
                PeriodicAdvanceToTargetStart(s);PeriodicAdvanceToTargetStart(restored);
                var after=s.Capture();var tick=after.PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Tick);
                Require(Bytes(s).SequenceEqual(Bytes(restored))&&after.RuleClock==new RuleTime(6)&&after.WorldSchedule.ProcessedSlot==2
                    &&tick.At==new RuleTime(6)&&tick.WorldSlot==2&&tick.Outcome==PeriodicRiderOutcome.Damage&&tick.Die>=1&&tick.Die<=4
                    &&after.PeriodicRiders.Single().EndedAt==new RuleTime(6)&&after.PeriodicRiders.Single().EndingMethod=="tick"
                    &&after.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Hp==10-tick.Amount,
                    "Periodic damage, actual life state, marker identity or reload continuation diverged.");
            });
            cases.Add("periodic_rider_outside_encounter_due_start_runs_one_life_save_before_tick",()=>{
                var app=PeriodicApp("bleed.event.outside-dying","bleed.record.future-outside-dying",owner:AdditionalTacticalActor.Id);
                const long slot=2;string target=TestOnlyPolicy.ActorId;
                var rider=new PeriodicRiderRecord("bleed.record.outside-dying",PeriodicRiderFixture.ProfileId,PeriodicRiderFixture.FamilyId,
                    app.OwnerId,PeriodicRiderFixture.SourceId,target,app.EventId,"piercing",app.ApplyingDc,0,default,slot,1);
                var fixture=PeriodicFixture(new[]{app},initialRiders:new[]{rider});
                var p=PeriodicPolicy(fixture,seed:1,heroHp:0);var s=World(p);var initial=s.Capture();var schedule=initial.WorldSchedule;
                var due=schedule.Start(slot);WorldAdvance(s,checked((int)due.Numerator),checked((int)due.Denominator));var after=s.Capture();
                var saves=after.LifeEvents.Where(x=>x.ActorId==target&&x.Kind==LifeEventKind.DeathSave&&x.At==due).ToArray();
                var tick=after.PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Tick);
                Require(saves.Length==1&&after.WorldLifeMarkers.Count(x=>x.ActorId==target&&x.CalendarId==schedule.Id&&x.Ordinal==slot)==1
                    &&tick.WorldSlot==slot&&tick.At==due&&tick.Outcome==PeriodicRiderOutcome.Damage,
                    "Outside-encounter rider handling repeated the regular-start death save or ran Bleed before life processing.");
            });
            cases.Add("periodic_rider_same_owner_source_refreshes_without_extra_dice",()=>{
                var first=PeriodicApp("bleed.event.first","bleed.record.first",dc:10);
                var refresh=PeriodicApp("bleed.event.refresh","bleed.record.refresh",dc:15);
                var p=PeriodicPolicy(PeriodicFixture(new[]{first,refresh}));var s=World(p);PeriodicBegin(s);uint random=s.Capture().RandomState;
                PeriodicApply(s,first);PeriodicApply(s,refresh);var v=s.Capture();
                var refreshEvent=v.PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Refreshed);
                Require(v.PeriodicRiders.Length==1&&v.PeriodicRiders[0].Id==first.RiderId&&v.PeriodicRiders[0].NextStartSlot==2
                    &&v.PeriodicRiders[0].ApplyingDc==10&&v.PeriodicRiders[0].OriginEventId==first.EventId
                    &&refreshEvent.Dc==15&&refreshEvent.RiderId==first.RiderId
                    &&v.PeriodicRiderEvents.Select(x=>x.Kind).SequenceEqual(new[]{PeriodicRiderEventKind.Applied,PeriodicRiderEventKind.Refreshed})
                    &&v.RandomState==random,"Refresh stacked a second die, lost the later cure DC or changed random state.");
            });
            cases.Add("periodic_rider_same_owner_source_can_affect_distinct_targets",()=>{
                var first=PeriodicApp("bleed.event.target-one","bleed.record.target-one",owner:TestOnlyPolicy.ActorId,target:TestOnlyPolicy.ActorId,dc:10);
                var second=PeriodicApp("bleed.event.target-two","bleed.record.target-two",owner:TestOnlyPolicy.ActorId,target:AdditionalTacticalActor.Id,dc:14);
                var p=PeriodicPolicy(PeriodicFixture(new[]{first,second}));var s=World(p);PeriodicBegin(s);PeriodicApply(s,first);PeriodicApply(s,second);
                var v=s.Capture();
                Require(v.PeriodicRiders.Length==2&&v.PeriodicRiders.Single(x=>x.TargetId==TestOnlyPolicy.ActorId).ApplyingDc==10
                    &&v.PeriodicRiders.Single(x=>x.TargetId==AdditionalTacticalActor.Id).ApplyingDc==14
                    &&v.PeriodicRiders.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()==2
                    &&v.PeriodicRiderEvents.Count(x=>x.Kind==PeriodicRiderEventKind.Applied)==2,
                    "The owner/source group incorrectly treated distinct target markers as one global effect.");
            });
            cases.Add("periodic_rider_family_arbitration_rolls_winner_then_consumes_loser",()=>{
                var first=PeriodicApp("bleed.event.owner-one","bleed.record.owner-one",owner:TestOnlyPolicy.ActorId);
                var second=PeriodicApp("bleed.event.owner-two","bleed.record.owner-two",owner:AdditionalTacticalActor.Id);
                var p=PeriodicPolicy(PeriodicFixture(new[]{first,second}));var s=World(p);PeriodicBegin(s);PeriodicApply(s,first);PeriodicApply(s,second);
                PeriodicAdvanceToTargetStart(s);var v=s.Capture();var ticks=v.PeriodicRiderEvents.Where(x=>x.Kind==PeriodicRiderEventKind.Tick).OrderBy(x=>x.EventId,StringComparer.Ordinal).ToArray();
                Require(ticks.Length==2&&ticks.Single(x=>x.RiderId==first.RiderId).Outcome==PeriodicRiderOutcome.Damage
                    &&ticks.Single(x=>x.RiderId==first.RiderId).Die>=1&&ticks.Single(x=>x.RiderId==second.RiderId).Outcome==PeriodicRiderOutcome.FamilyLost
                    &&ticks.Single(x=>x.RiderId==second.RiderId).Die==0&&v.PeriodicRiders.All(x=>x.RemainingTicks==0),
                    "The tied earliest application did not win, or the losing application banked its tick.");
            });
            cases.Add("periodic_rider_family_immunity_prevents_application_and_suppresses_due_tick",()=>{
                var app=PeriodicApp();var p=PeriodicPolicy(PeriodicFixture(new[]{app}));var s=World(p);PeriodicBegin(s);
                WorldCommit(s,Tac(s,CommandKind.SetPeriodicFamilyImmunity,TestOnlyPolicy.ActorId,actor:TestOnlyPolicy.ActorId,x:1));PeriodicApply(s,app);
                Require(s.Capture().PeriodicRiders.Length==0&&s.Capture().PeriodicRiderEvents.Single(x=>x.EventId==app.EventId).Outcome==PeriodicRiderOutcome.Immune,
                    "Family immunity failed to prevent initial registered application.");
                var p2=PeriodicPolicy(PeriodicFixture(new[]{app}));var later=World(p2);PeriodicBegin(later);PeriodicApply(later,app);
                WorldCommit(later,Tac(later,CommandKind.SetPeriodicFamilyImmunity,TestOnlyPolicy.ActorId,actor:TestOnlyPolicy.ActorId,x:1));
                uint random=later.Capture().RandomState;PeriodicAdvanceToTargetStart(later);var tick=later.Capture().PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Tick);
                Require(tick.Outcome==PeriodicRiderOutcome.Immune&&tick.Die==0&&tick.RandomBefore==random&&tick.RandomAfter==random
                    &&later.Capture().PeriodicRiders.Single().RemainingTicks==0,"Later immunity did not suppress and consume the due tick.");
            });
            cases.Add("periodic_rider_suppression_consumes_due_tick_without_drawing_damage",()=>{
                var app=PeriodicApp();var p=PeriodicPolicy(PeriodicFixture(new[]{app}));var s=World(p);PeriodicBegin(s);PeriodicApply(s,app);
                WorldCommit(s,Tac(s,CommandKind.SetPeriodicRiderSuppression,app.RiderId,actor:app.OwnerId,x:1));uint random=s.Capture().RandomState;
                PeriodicAdvanceToTargetStart(s);var tick=s.Capture().PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Tick);
                Require(tick.Outcome==PeriodicRiderOutcome.Suppressed&&tick.Die==0&&tick.RandomBefore==random&&tick.RandomAfter==random
                    &&s.Capture().PeriodicRiders.Single().RemainingTicks==0,"Suppression banked the tick or consumed an unneeded die roll.");
            });
            cases.Add("periodic_rider_medicine_uses_wis_training_shared_action_and_selected_record",()=>{
                var first=PeriodicApp("bleed.event.medicine-one","bleed.record.medicine-one",owner:AdditionalTacticalActor.Id,dc:10);
                var second=PeriodicApp("bleed.event.medicine-two","bleed.record.medicine-two",owner:TestOnlyPolicy.ActorId,dc:10);
                uint seed=PeriodicSeed(x=>x.Natural+4>=10);var p=PeriodicPolicy(PeriodicFixture(new[]{first,second}),seed);var s=World(p);PeriodicBegin(s);
                PeriodicApply(s,first);PeriodicApply(s,second);WorldCommit(s,Tac(s,CommandKind.CurePeriodicRider,first.RiderId,actor:TestOnlyPolicy.ActorId));
                var v=s.Capture();var eventRecord=v.PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Medicine);
                Require(eventRecord.Outcome==PeriodicRiderOutcome.MedicineSuccess&&eventRecord.Modifier==4&&eventRecord.Dc==10
                    &&v.PeriodicRiders.Single(x=>x.Id==first.RiderId).EndingMethod=="medicine"
                    &&v.PeriodicRiders.Single(x=>x.Id==second.RiderId).Present&&v.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,
                    "Medicine did not roll recorded WIS/proficiency, spend the shared Action and cure only the selected present record.");
            });
            cases.Add("periodic_rider_medicine_failure_spends_action_and_records_rng",()=>{
                var app=PeriodicApp(dc:30);uint seed=PeriodicSeed(x=>x.Natural==1);var p=PeriodicPolicy(PeriodicFixture(new[]{app},medicineRank:0),seed);var s=World(p);
                PeriodicBegin(s);PeriodicApply(s,app);var before=s.Capture().RandomState;WorldCommit(s,Tac(s,CommandKind.CurePeriodicRider,app.RiderId,actor:TestOnlyPolicy.ActorId));
                var v=s.Capture();var result=v.PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Medicine);
                Require(result.Outcome==PeriodicRiderOutcome.MedicineFailure&&result.Natural==1&&result.RandomBefore==before&&result.RandomAfter==v.RandomState
                    &&v.PeriodicRiders.Single().Present&&v.WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,
                    "Failed Medicine refunded its Action, ended the rider or lost the recorded roll.");
            });
            cases.Add("periodic_rider_medicine_natural_twenty_uses_shared_task_degree",()=>{
                var app=PeriodicApp(dc:25);uint seed=PeriodicSeed(x=>x.Natural==20);var p=PeriodicPolicy(PeriodicFixture(new[]{app},medicineRank:0),seed);var s=World(p);
                PeriodicBegin(s);PeriodicApply(s,app);WorldCommit(s,Tac(s,CommandKind.CurePeriodicRider,app.RiderId,actor:TestOnlyPolicy.ActorId));
                var v=s.Capture();var record=v.PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Medicine);
                var task=PlaytestRolls.TaskCheck(record.Natural,record.Modifier,record.Dc);
                var restored=new Simulation(p,codec.Decode(Bytes(s)),ExecutionProfile.Laboratory);
                Require(record.Natural==20&&task.Total<record.Dc&&task.Degree==TaskDegree.Success
                    &&record.CheckDegree==PeriodicRiderCheckDegree.Success
                    &&record.CheckTotal==task.Total&&record.Outcome==PeriodicRiderOutcome.MedicineSuccess
                    &&v.PeriodicRiders.Single().EndingMethod=="medicine"&&Bytes(s).SequenceEqual(Bytes(restored)),
                    "A natural 20 that upgrades a below-DC Medicine check did not resolve as a recorded successful cure or did not survive save/replay.");
            });
            cases.Add("periodic_rider_medicine_natural_one_downgrades_raw_success",()=>{
                var app=PeriodicApp(dc:5);uint seed=PeriodicSeed(x=>x.Natural==1);var p=PeriodicPolicy(PeriodicFixture(new[]{app},medicineRank:2),seed);var s=World(p);
                PeriodicBegin(s);PeriodicApply(s,app);WorldCommit(s,Tac(s,CommandKind.CurePeriodicRider,app.RiderId,actor:TestOnlyPolicy.ActorId));
                var v=s.Capture();var record=v.PeriodicRiderEvents.Single(x=>x.Kind==PeriodicRiderEventKind.Medicine);
                var task=PlaytestRolls.TaskCheck(record.Natural,record.Modifier,record.Dc);
                Require(record.Natural==1&&record.CheckTotal>=record.Dc&&task.Degree==TaskDegree.Failure
                    &&record.CheckDegree==PeriodicRiderCheckDegree.Failure
                    &&record.CheckTotal==task.Total&&record.Outcome==PeriodicRiderOutcome.MedicineFailure
                    &&v.PeriodicRiders.Single().Present&&v.PeriodicRiders.Single().EndingMethod=="",
                    "A natural 1 that downgrades a raw successful Medicine check cured Bleed.");
            });
            cases.Add("periodic_rider_positive_potential_healing_cures_at_full_hp_without_hp_gain",()=>{
                var app=PeriodicApp();var healing=new PeriodicHealingFact("fixture.heal.once",AdditionalTacticalActor.Id,TestOnlyPolicy.ActorId,4);
                var p=PeriodicPolicy(PeriodicFixture(new[]{app},healing));var s=World(p);PeriodicBegin(s);PeriodicApply(s,app);
                WorldCommit(s,Tac(s,CommandKind.ApplyFixtureMagicalHealing,TestOnlyPolicy.ActorId,actor:AdditionalTacticalActor.Id));var v=s.Capture();
                var eventRecord=v.PeriodicRiderEvents.Single(x=>x.EventId==healing.EventId);
                Require(v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Hp==10&&eventRecord.HitPointGain==0&&eventRecord.Flag
                    &&eventRecord.Outcome==PeriodicRiderOutcome.HealingCure&&v.PeriodicRiders.Single().EndingMethod=="healing",
                    "A source-qualified positive-potential healing event required actual HP gain or failed to end the present rider.");
            });
            cases.Add("periodic_rider_companion_research_and_tick_share_one_clock",()=>{
                var app=PeriodicApp();var research=new SharedResearchFixture();var p=PeriodicPolicy(PeriodicFixture(new[]{app}),seed:1,research:research);var s=World(p);
                ResearchStart(s);PeriodicBegin(s);PeriodicApply(s,app);PeriodicAdvanceToTargetStart(s);var v=s.Capture();
                Require(v.RuleClock==new RuleTime(6)&&v.PeriodicRiderEvents.Any(x=>x.Kind==PeriodicRiderEventKind.Tick&&x.At==new RuleTime(6))
                    &&v.FormulaWork.Single().Work.Labor==new RuleTime(6)&&v.FormulaWork.Single().Status==FormulaWorkStatus.Working,
                    "Companion work and periodic combat consequences did not progress on the same shared simulation clock.");
            });
        }
    }
}
#endif
