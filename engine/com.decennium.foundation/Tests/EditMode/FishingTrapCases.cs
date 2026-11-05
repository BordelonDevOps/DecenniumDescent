#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static Command TrapOp(Simulation s,FishingTrapInteraction operation,string id=null,string actor=TestOnlyPolicy.CompanionId,
            string target=SharedFishingTrapFixture.TrapId)
            =>IC(s,CommandKind.Interact,target,actor:actor,x:(int)operation,id:id);
        private static Command TrapRetrieve(Simulation s,string actor=TestOnlyPolicy.CompanionId,
            string destination="TEST_ONLY.riverbank.receiving-location",string id=null,string target=SharedFishingTrapFixture.TrapId)
            =>IC(s,CommandKind.Interact,target,
                new InventoryRequest(default,destination,HandlingKind.Retrieve),actor,(int)FishingTrapInteraction.Retrieve,0,id);
        private static Simulation TrapWorld(SharedFishingTrapFixture fixture,uint seed=1)
        {var p=TestOnlySharedWorldPolicy.WithFishingTrap(fixture,seed);return new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);}
        private static Simulation LegacyTrapWorld(SharedFishingTrapFixture fixture,uint seed=1)
        {var p=TestOnlySharedWorldPolicy.WithLegacyFishingTrap(fixture,seed);return new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);}
        private static void TrapCommit(Simulation s,FishingTrapInteraction operation,string id=null)
            =>WorldCommit(s,TrapOp(s,operation,id));
        private static int TrapModifier(Snapshot s,int rank,string actorId=TestOnlyPolicy.CompanionId)
        {
            var character=s.Characters.Single(x=>x.ActorId==actorId);
            int pb=rank==0?0:PlaytestCharacters.ProficiencyBonus(character.Levels.Count)*(rank==2?2:1);
            return PlaytestCharacters.AbilityModifier(character.Abilities[3])+pb;
        }
        private static FishingTrapCheckDegree TrapDegree(TaskDegree degree)
            =>degree==TaskDegree.CriticalFailure?FishingTrapCheckDegree.CriticalFailure
                :degree==TaskDegree.Failure?FishingTrapCheckDegree.Failure
                :degree==TaskDegree.Success?FishingTrapCheckDegree.Success:FishingTrapCheckDegree.CriticalSuccess;
        private static uint TrapSeedForDegree(SharedFishingTrapFixture fixture,TaskDegree requested)
        {
            for(uint seed=1;seed<10000;seed++) {
                var p=TestOnlySharedWorldPolicy.WithFishingTrap(fixture,seed);var s=p.Initial();
                int disadvantage=fixture.ProficiencyRank==0?1:0;
                var roll=PlaytestDice.RollD20(s.RandomState,disadvantageSources:disadvantage);
                if(PlaytestRolls.TaskCheck(roll.Natural,TrapModifier(s,fixture.ProficiencyRank,fixture.SetterId),fixture.CatchDc).Degree==requested)return seed;
            }
            throw new Exception("Could not find a deterministic seed for " + requested + ".");
        }
        private static void AddFishingTrapCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("fishing_trap_schema35_wire_shape_roundtrips_and_replays",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);var policy=TestOnlySharedWorldPolicy.WithLegacyFishingTrap(fixture);
                var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);var codec=new SnapshotCodec();
                Require(s.Capture().SchemaVersion==Snapshot.FishingTrapLegacySchema
                    &&s.Capture().Work.Lots.All(x=>x.Id!=SharedFishingTrapFixture.BaitLotId),
                    "Legacy schema35 fixture unexpectedly acquired new bait state.");
                TrapCommit(s,FishingTrapInteraction.Set,"legacy-set");WorldAdvance(s,120);
                var bytes=codec.Encode(s.Capture());var decoded=codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(decoded))&&decoded.FishingTrapAttempts.Single().BaitLotId=="",
                    "Legacy schema35 save format did not retain its original record shape.");
                s=new Simulation(policy,decoded,ExecutionProfile.Laboratory);WorldAdvance(s,180);
                var completed=s.Capture().FishingTrapAttempts.Single();
                Require(completed.Status==FishingTrapAttemptStatus.Soaking&&completed.OpportunityCommitted
                    &&completed.BaitLotId==""&&s.Capture().SchemaVersion==Snapshot.FishingTrapLegacySchema,
                    "Legacy schema35 history did not resume with its original timing semantics.");
            });
            cases.Add("fishing_trap_schema36_bait_wire_shape_roundtrips_and_replays",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);var policy=TestOnlySharedWorldPolicy.WithBaitOnlyFishingTrap(fixture);
                var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);var codec=new SnapshotCodec();
                Require(s.Capture().SchemaVersion==Snapshot.FishingTrapBaitSchema&&s.Capture().FishingTraps.Length==0,
                    "Historical schema36 fixture unexpectedly acquired schema37 physical state.");
                TrapCommit(s,FishingTrapInteraction.Set,"schema36-set");WorldAdvance(s,120);
                var bytes=codec.Encode(s.Capture());var decoded=codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(decoded))&&decoded.FishingTrapAttempts.Single().BaitLotId==fixture.BaitLotIdentity,
                    "Schema36 bait snapshot changed its historical wire projection.");
                s=new Simulation(policy,decoded,ExecutionProfile.Laboratory);WorldAdvance(s,180);
                var completed=s.Capture().FishingTrapAttempts.Single();
                Require(completed.Status==FishingTrapAttemptStatus.Soaking&&completed.BaitExposedAt==completed.SetupCompletedAt
                    &&completed.OpportunityCommitted&&s.Capture().SchemaVersion==Snapshot.FishingTrapBaitSchema
                    &&s.Capture().FishingTraps.Length==0,
                    "Schema36 setup replay did not preserve the bait/timing-only model.");
            });
            cases.Add("fishing_trap_setup_pause_resume_and_save_replay",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);var s=TrapWorld(fixture);
                var initial=s.Capture();Require(initial.SchemaVersion==Snapshot.FishingTrapSchema
                    &&initial.SkillTraining.Single(x=>x.ActorId==TestOnlyPolicy.CompanionId&&x.SkillId=="fishing-tackle").ProficiencyRank==1,
                    "Trap fixture did not select its source-bound skill profile.");
                TrapCommit(s,FishingTrapInteraction.Set,"trap-set");WorldAdvance(s,120);
                var attempt=s.Capture().FishingTrapAttempts.Single();Require(attempt.Status==FishingTrapAttemptStatus.SettingUp
                    &&attempt.SetupLabor==new RuleTime(120)
                    &&s.Capture().Work.Reservations.Single(x=>x.Id==attempt.BaitReservationId).Status==ReservationStatus.Reserved,
                    "Setup did not accrue 120 seconds or retain its pre-setup bait reservation.");
                byte[] beforeDiscovery=Bytes(s);var setupOptions=s.DiscoverCommands(TestOnlySharedWorldPolicy.Host(),fixture.SetterId);
                var setupActivity=WorldActivityProjection.CurrentWork(s.Capture(),setupOptions).Single(x=>x.Id==attempt.Id);
                Require(Bytes(s).SequenceEqual(beforeDiscovery)&&setupActivity.Status==attempt.Status.ToString()
                    &&setupActivity.RecordedWorkDone==attempt.SetupLabor&&setupActivity.ResourceReservations.Any(x=>x.Id==attempt.BaitReservationId)
                    &&setupActivity.AvailableCommands.Any(x=>x.Command.Kind==CommandKind.Interact&&x.Command.Target==fixture.TrapIdentity
                        &&x.Command.X==(int)FishingTrapInteraction.Pause&&x.Query.Admissible)
                    &&setupActivity.AvailableCommands.Any(x=>x.Command.Kind==CommandKind.Interact&&x.Command.Target==fixture.TrapIdentity
                        &&x.Command.X==(int)FishingTrapInteraction.Cancel&&x.Query.Admissible),
                    "Setup activity did not expose its existing discovered pause/cancel operations and linked bait reservation without mutation.");
                TrapCommit(s,FishingTrapInteraction.Pause,"trap-pause");WorldAdvance(s,60);
                var pausedSetup=s.Capture().FishingTrapAttempts.Single();
                var pausedOptions=s.DiscoverCommands(TestOnlySharedWorldPolicy.Host(),fixture.SetterId);
                Require(pausedSetup.SetupLabor==new RuleTime(120)&&pausedOptions.Any(x=>x.Command.Kind==CommandKind.Interact
                    &&x.Command.Target==fixture.TrapIdentity&&x.Command.X==(int)FishingTrapInteraction.Resume&&x.Query.Admissible),
                    "Paused setup accrued labor or failed to discover its existing resume operation.");
                TrapCommit(s,FishingTrapInteraction.Resume,"trap-resume");WorldAdvance(s,179);
                attempt=s.Capture().FishingTrapAttempts.Single();Require(attempt.Status==FishingTrapAttemptStatus.SettingUp
                    &&attempt.SetupLabor==new RuleTime(299),"Resumed setup did not retain exact prior labor.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(s.Capture());
                s=new Simulation(TestOnlySharedWorldPolicy.WithFishingTrap(fixture),codec.Decode(bytes),ExecutionProfile.Laboratory);
                WorldAdvance(s,1);attempt=s.Capture().FishingTrapAttempts.Single();
                Require(attempt.Status==FishingTrapAttemptStatus.Soaking&&attempt.SetupLabor==new RuleTime(300)
                    &&attempt.SetupCompletedAt==s.Capture().RuleClock&&attempt.CheckDueAt==attempt.StartedAt.AddSeconds(3300)
                    &&attempt.OpportunityCommitted&&attempt.WisdomModifier==PlaytestCharacters.AbilityModifier(
                        s.Capture().Characters.Single(x=>x.ActorId==TestOnlyPolicy.CompanionId).Abilities[3])
                    &&attempt.ProficiencyRank==1&&attempt.ProficiencyBonus==PlaytestCharacters.ProficiencyBonus(1)
                    &&attempt.BaitExposedAt==attempt.SetupCompletedAt
                    &&s.Capture().Work.Reservations.Single(x=>x.Id==attempt.BaitReservationId).Status==ReservationStatus.Consumed
                    &&s.Capture().Work.Lots.Single(x=>x.Id==attempt.BaitLotId).Amount==default,
                    "Setup completion did not expose reserved bait, snapshot the setter facts and schedule the check.");
                uint random=s.Capture().RandomState;WorldAdvance(s,2940);attempt=s.Capture().FishingTrapAttempts.Single();
                Require(attempt.Status==FishingTrapAttemptStatus.CheckMissed&&attempt.CheckResolvedAt==attempt.CheckDueAt
                    &&attempt.CheckOutcome==FishingTrapCheckOutcome.None&&attempt.DiceSelection==FishingTrapDiceSelection.None
                    &&s.Capture().RandomState==random,
                    "Delayed setup restarted the attempt clock or rolled without fifty continuous deployed minutes.");
            });
            cases.Add("fishing_trap_resume_query_matches_off_calendar_action_gate",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);
                var policy=TestOnlySharedWorldPolicy.WithFishingTrapAndRepair(fixture,new SharedRepairFixture()).EnableOffCalendarActivity();
                var snapshot=policy.Initial();
                var interval=snapshot.WorldActivityIntervals.Single(x=>x.ActorId==TestOnlyPolicy.CompanionId);
                snapshot.WorldActivityIntervals=snapshot.WorldActivityIntervals.Select(x=>x.ActorId==interval.ActorId
                    ?interval.PayDash("trap-resume-prior-dash",1):x).ToArray();
                snapshot.InventoryCombat=true;
                var command=new Command("trap-resume-after-dash",TestOnlyPolicy.CompanionId,snapshot.Revision,
                    CommandKind.Interact,fixture.TrapIdentity,(int)FishingTrapInteraction.Resume);
                var query=policy.QueryCommand(snapshot,TestOnlySharedWorldPolicy.Host(),command);
                string execution=policy.Resolve(snapshot,command);
                Require(query.Supported&&!query.Admissible&&query.Code=="OffCalendarActionAlreadySpent"
                    &&execution==query.Code,
                    "Trap resume query and execution did not apply the shared off-calendar Action gate before the exploration-only check.");
            });
            cases.Add("fishing_trap_resolves_each_check_degree_once_without_inventory_award",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);var codec=new SnapshotCodec();
                foreach(TaskDegree expectedDegree in Enum.GetValues(typeof(TaskDegree))) {
                    uint seed=TrapSeedForDegree(fixture,expectedDegree);var s=TrapWorld(fixture,seed);var start=s.Capture();
                    TrapCommit(s,FishingTrapInteraction.Set,"set");WorldAdvance(s,300);var beforeCheck=s.Capture();
                    var attemptBefore=beforeCheck.FishingTrapAttempts.Single();
                    Require(attemptBefore.BaitExposedAt==beforeCheck.RuleClock
                        &&beforeCheck.Work.Reservations.Single(x=>x.Id==attemptBefore.BaitReservationId).Status==ReservationStatus.Consumed,
                        "Trap did not debit and expose its reserved ordinary bait at first deployment.");
                    var advance=IC(s,CommandKind.AdvanceClock,x:3000,y:1);
                    WorldCommit(s,advance);var v=s.Capture();var attempt=v.FishingTrapAttempts.Single();
                    int modifier=TrapModifier(start,fixture.ProficiencyRank,fixture.SetterId);var roll=PlaytestDice.RollD20(start.RandomState);
                    var expected=PlaytestRolls.TaskCheck(roll.Natural,modifier,fixture.CatchDc);
                    Require(attempt.Status==FishingTrapAttemptStatus.Resolved&&attempt.CheckResolvedAt==attempt.CheckDueAt
                        &&attempt.CheckDegree==TrapDegree(expectedDegree)&&attempt.CheckDegree==TrapDegree(expected.Degree)
                        &&attempt.Natural==roll.Natural&&attempt.CheckModifier==modifier&&attempt.RandomBefore==start.RandomState
                        &&attempt.RandomAfter==roll.NextRandomState&&attempt.WordsConsumed==roll.WordsConsumed
                        &&v.RandomState==roll.NextRandomState,"Trap check result, degree mapping, or random ledger differs.");
                    Require((attempt.CheckOutcome==FishingTrapCheckOutcome.CapturedInTrap)==expected.Success
                        &&(attempt.CapturedCreatureId==SharedFishingTrapFixture.CreatureId)==expected.Success
                        &&v.Work.Lots.Select(x=>x.Id+"|"+x.Amount).SequenceEqual(beforeCheck.Work.Lots.Select(x=>x.Id+"|"+x.Amount))
                        &&v.InventoryLots.Length==beforeCheck.InventoryLots.Length,
                        "Trap catch was not retained in place or created an inventory lot.");
                    byte[] resolved=codec.Encode(v);var duplicate=s.Execute(TestOnlySharedWorldPolicy.Host(),advance);
                    Require(duplicate.Outcome==Outcome.Duplicate&&resolved.SequenceEqual(codec.Encode(s.Capture()))
                        &&s.Capture().FishingTrapAttempts.Length==1,"Repeating the due command resolved the trap twice.");
                }
            });
            cases.Add("fishing_trap_untrained_check_uses_and_records_disadvantage",()=>{
                var fixture=new SharedFishingTrapFixture(12,0);uint seed=TrapSeedForDegree(fixture,TaskDegree.Failure);
                var s=TrapWorld(fixture,seed);var initial=s.Capture();TrapCommit(s,FishingTrapInteraction.Set,"set-untrained");
                WorldAdvance(s,3300);var attempt=s.Capture().FishingTrapAttempts.Single();
                var roll=PlaytestDice.RollD20(initial.RandomState,disadvantageSources:1);
                Require(attempt.ProficiencyRank==0&&attempt.ProficiencyBonus==0
                    &&attempt.DiceSelection==FishingTrapDiceSelection.Disadvantage&&attempt.FirstDie==roll.First
                    &&attempt.SecondDie==roll.Second.Value&&attempt.Natural==roll.Natural&&attempt.WordsConsumed==2
                    &&attempt.RandomAfter==roll.NextRandomState&&attempt.CheckModifier==attempt.WisdomModifier,
                    "Untrained Trap check did not apply WIS alone with one auditable disadvantage roll.");
            });
            cases.Add("fishing_trap_retrieval_moves_the_same_catch_after_saved_partial_work",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);uint seed=TrapSeedForDegree(fixture,TaskDegree.Success);
                var policy=TestOnlySharedWorldPolicy.WithFishingTrap(fixture,seed);var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                TrapCommit(s,FishingTrapInteraction.Set,"retrieve-capture-set");WorldAdvance(s,3300);
                var caught=s.Capture();var attempt=caught.FishingTrapAttempts.Single();var body=caught.FishingCreatures.Single();
                Require(attempt.CheckOutcome==FishingTrapCheckOutcome.CapturedInTrap&&body.Id==attempt.CreatureId
                    &&body.ContainerId==fixture.TrapIdentity&&body.CapturedByAttemptId==attempt.Id,
                    "The successful check did not retain the same creature body inside the Trap.");
                WorldCommit(s,TrapRetrieve(s,id:"retrieve-start"));var active=s.Capture();var job=active.FishingTrapRetrievals.Single();
                Require(job.Status==FishingTrapRetrievalStatus.Working&&job.WorkDone==default
                    &&active.FishingReceiveLocations.Single().ReservedByRetrievalId==job.Id,
                    "Retrieval did not reserve its supported receiving location before work.");
                byte[] beforeDiscovery=Bytes(s);var retrievalOptions=s.DiscoverCommands(TestOnlySharedWorldPolicy.Host(),job.WorkerId);
                var retrievalActivity=WorldActivityProjection.CurrentWork(s.Capture(),retrievalOptions).Single(x=>x.Id==job.Id);
                Require(Bytes(s).SequenceEqual(beforeDiscovery)&&retrievalActivity.Status==job.Status.ToString()
                    &&retrievalActivity.WorkerIntervals.Any(x=>x.JobId==job.Id&&x.WorkerId==job.WorkerId)
                    &&retrievalActivity.AvailableCommands.Any(x=>x.Command.Kind==CommandKind.Interact&&x.Command.Target==fixture.TrapIdentity
                        &&x.Command.X==(int)FishingTrapInteraction.PauseRetrieval&&x.Query.Admissible),
                    "Retrieval activity did not expose its existing discovered pause operation or linked worker claim without mutation.");
                WorldAdvance(s,299);TrapCommit(s,FishingTrapInteraction.PauseRetrieval,"retrieve-pause");
                var paused=s.Capture();job=paused.FishingTrapRetrievals.Single();
                Require(job.Status==FishingTrapRetrievalStatus.Paused&&job.WorkDone==new RuleTime(299)
                    &&paused.FishingReceiveLocations.Single().ReservedByRetrievalId==job.Id,
                    "Paused retrieval did not preserve its partial labor and destination reservation.");
                var pausedRetrievalOptions=s.DiscoverCommands(TestOnlySharedWorldPolicy.Host(),job.WorkerId);
                Require(pausedRetrievalOptions.Any(x=>x.Command.Kind==CommandKind.Interact&&x.Command.Target==fixture.TrapIdentity
                    &&x.Command.X==(int)FishingTrapInteraction.ResumeRetrieval&&x.Query.Admissible),
                    "Paused retrieval did not discover its existing resume operation.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(paused);var restored=new Simulation(policy,codec.Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(codec.Encode(restored.Capture())),"Paused retrieval save changed its physical or labor state.");
                TrapCommit(restored,FishingTrapInteraction.ResumeRetrieval,"retrieve-resume");WorldAdvance(restored,1);
                var complete=restored.Capture();job=complete.FishingTrapRetrievals.Single();attempt=complete.FishingTrapAttempts.Single();
                body=complete.FishingCreatures.Single();var trap=complete.FishingTraps.Single();
                var item=complete.PortableEquipment.Single(x=>x.Id==fixture.TrapIdentity);
                Require(job.Status==FishingTrapRetrievalStatus.Complete&&job.WorkDone==new RuleTime(300)
                    &&job.CompletedAt==complete.RuleClock&&trap.Status==FishingTrapPhysicalStatus.Retrieved
                    &&trap.ReceivingLocationId==fixture.ReceiverIdentity&&trap.RetrievedAt==complete.RuleClock
                    &&item.Placement==PortablePlacement.Ground&&item.GroundX==fixture.ReceiverX&&item.GroundY==fixture.ReceiverY
                    &&item.CustodianId==TestOnlyPolicy.CompanionId&&body.Id==attempt.CreatureId&&body.ContainerId==""
                    &&body.LocationId==fixture.ReceiverIdentity&&body.CustodianId==TestOnlyPolicy.CompanionId
                    &&body.CapturedByAttemptId==attempt.Id&&body.RecoveryEvaluatedAt==attempt.CheckResolvedAt
                    &&complete.FishingReceiveLocations.Single().ReservedByRetrievalId==""
                    &&complete.FishingCreatures.Length==1&&complete.InventoryLots.Length==paused.InventoryLots.Length,
                    "Completed retrieval did not move the same Trap and captured creature into the receiver exactly once.");
                var completedBytes=codec.Encode(complete);var roundtrip=codec.Decode(completedBytes);
                Require(completedBytes.SequenceEqual(codec.Encode(roundtrip))
                    &&roundtrip.FishingTrapRetrievals.Single().Status==FishingTrapRetrievalStatus.Complete
                    &&roundtrip.FishingCreatures.Length==1&&roundtrip.PortableEquipment.Single(x=>x.Id==fixture.TrapIdentity).Id==fixture.TrapIdentity,
                    "Completed retrieval save did not preserve the settled catch and Trap exactly.");
            });
            cases.Add("fishing_trap_early_retrieval_spends_deployed_inputs_without_a_check",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);var policy=TestOnlySharedWorldPolicy.WithFishingTrap(fixture,17);
                var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);TrapCommit(s,FishingTrapInteraction.Set,"early-retrieve-set");
                WorldAdvance(s,300);WorldCommit(s,TrapRetrieve(s,id:"early-retrieve-start"));WorldAdvance(s,300);
                var v=s.Capture();var attempt=v.FishingTrapAttempts.Single();var opportunity=v.FishingOpportunities.Single();
                var creature=v.FishingCreatures.Single();var job=v.FishingTrapRetrievals.Single();
                Require(attempt.Status==FishingTrapAttemptStatus.RetrievedBeforeCheck&&!attempt.CheckResolvedAt.HasValue
                    &&attempt.CheckOutcome==FishingTrapCheckOutcome.None&&opportunity.Status==FishingOpportunityStatus.Spent
                    &&v.Work.Lots.Single(x=>x.Id==fixture.BaitLotIdentity).Amount==default
                    &&creature.LifeState==FishingCreatureLifeState.Alive&&creature.CapturedByAttemptId==""
                    &&creature.ContainerId==""&&job.Status==FishingTrapRetrievalStatus.Complete
                    &&v.RandomState==policy.Initial().RandomState
                    &&v.FishingTraps.Single().Status==FishingTrapPhysicalStatus.Retrieved,
                    "Early retrieval rolled a check, restored spent bait or opportunity, or failed to recover the live body.");
            });
            cases.Add("fishing_trap_check_resolves_before_retrieval_on_exact_tie",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);uint seed=TrapSeedForDegree(fixture,TaskDegree.Success);
                var policy=TestOnlySharedWorldPolicy.WithFishingTrap(fixture,seed);var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                TrapCommit(s,FishingTrapInteraction.Set,"tied-retrieve-set");WorldAdvance(s,3000);
                WorldCommit(s,TrapRetrieve(s,id:"tied-retrieve-start"));WorldAdvance(s,300);
                var v=s.Capture();var attempt=v.FishingTrapAttempts.Single();var retrieval=v.FishingTrapRetrievals.Single();
                var fish=v.FishingCreatures.Single();
                Require(attempt.CheckOutcome==FishingTrapCheckOutcome.CapturedInTrap&&attempt.CheckResolvedAt==attempt.CheckDueAt
                    &&retrieval.CompletedAt==attempt.CheckDueAt&&retrieval.Status==FishingTrapRetrievalStatus.Complete
                    &&fish.CapturedByAttemptId==attempt.Id&&fish.LocationId==fixture.ReceiverIdentity&&fish.ContainerId==""
                    &&v.FishingTraps.Single().Status==FishingTrapPhysicalStatus.Retrieved,
                    "Retrieval completion was processed before the coincident scheduled fishing check.");
            });
            cases.Add("fishing_trap_abandonment_pauses_retrieval_and_keeps_its_receiver_reserved",()=>{
                var fixture=new SharedFishingTrapFixture(12,1);uint seed=TrapSeedForDegree(fixture,TaskDegree.Success);
                var policy=TestOnlySharedWorldPolicy.WithFishingTrap(fixture,seed);var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                TrapCommit(s,FishingTrapInteraction.Set,"abandon-retrieval-set");WorldAdvance(s,3300);
                WorldCommit(s,TrapRetrieve(s,id:"abandon-retrieval-start"));WorldAdvance(s,120);
                TrapCommit(s,FishingTrapInteraction.Abandon,"abandon-during-retrieval");var paused=s.Capture();
                var job=paused.FishingTrapRetrievals.Single();var receiver=paused.FishingReceiveLocations.Single();
                Require(paused.FishingTraps.Single().Status==FishingTrapPhysicalStatus.Abandoned
                    &&job.Status==FishingTrapRetrievalStatus.Paused&&job.WorkDone==new RuleTime(120)
                    &&receiver.ReservedByRetrievalId==job.Id,
                    "Abandonment did not suspend retrieval while preserving its route reservation and labor.");
                TrapCommit(s,FishingTrapInteraction.ResumeRetrieval,"resume-abandoned-retrieval");WorldAdvance(s,180);
                var recovered=s.Capture();
                Require(recovered.FishingTrapRetrievals.Single().Status==FishingTrapRetrievalStatus.Complete
                    &&recovered.FishingTraps.Single().Status==FishingTrapPhysicalStatus.Retrieved
                    &&recovered.FishingTrapAttempts.Single().Status==FishingTrapAttemptStatus.Abandoned
                    &&recovered.FishingCreatures.Single().LocationId==fixture.ReceiverIdentity
                    &&recovered.FishingReceiveLocations.Single().ReservedByRetrievalId=="",
                    "A paused retrieval could not resume and recover the abandoned Trap and same catch.");
            });
            cases.Add("fishing_trap_retrieval_rejects_excess_path_and_remote_worker",()=>{
                var longRoute=new SharedFishingTrapFixture(12,1,recoveryPathFeet:21);
                var p=TestOnlySharedWorldPolicy.WithFishingTrap(longRoute);var s=new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);
                TrapCommit(s,FishingTrapInteraction.Set,"long-route-set");WorldAdvance(s,300);
                RejectUnchanged(s,TestOnlySharedWorldPolicy.Host(),TrapRetrieve(s,destination:longRoute.ReceiverIdentity,id:"too-long-route"),
                    "FishingReceiveCapacityOrPathUnavailable");
                var fixture=new SharedFishingTrapFixture(12,1);s=TrapWorld(fixture);TrapCommit(s,FishingTrapInteraction.Set,"remote-worker-set");
                WorldAdvance(s,300);
                RejectUnchanged(s,TestOnlySharedWorldPolicy.Host(),TrapRetrieve(s,actor:TestOnlyPolicy.ActorId,id:"remote-worker-retrieve"),
                    "FishingTrapOutOfReach");
            });
            cases.Add("fishing_trap_another_capable_adjacent_worker_can_retrieve",()=>{
                var fixture=new SharedFishingTrapFixture(12,1,identity:"alternate-worker",trapX:4,trapY:1,receiverX:4,receiverY:2,
                    setterId:AdditionalTacticalActor.Id);
                uint seed=TrapSeedForDegree(fixture,TaskDegree.Success);var policy=TestOnlySharedWorldPolicy.WithFishingTrap(fixture,seed);
                var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                WorldCommit(s,TrapOp(s,FishingTrapInteraction.Set,"alternate-worker-set",actor:AdditionalTacticalActor.Id,target:fixture.TrapIdentity));
                WorldStep(s,0,-1,actor:TestOnlyPolicy.CompanionId);WorldAdvance(s,2,5);
                byte[] travelBytes=Bytes(s);var traveling=new Simulation(policy,new SnapshotCodec().Decode(travelBytes),ExecutionProfile.Laboratory);
                Require(travelBytes.SequenceEqual(Bytes(traveling))&&traveling.Capture().WorldTraversals.Single().ActorId==TestOnlyPolicy.CompanionId,
                    "Off-calendar alternate retriever did not persist its actual journey.");
                s=traveling;WorldAdvance(s,3,5);WorldStep(s,1,0,actor:TestOnlyPolicy.CompanionId);WorldAdvance(s,1);
                WorldAdvance(s,3298);var checkedTrap=s.Capture();
                Require(checkedTrap.FishingTrapAttempts.Single().CheckOutcome==FishingTrapCheckOutcome.CapturedInTrap,
                    "A traveling alternate worker changed the Trap's scheduled capture.");
                var retrieve=TrapRetrieve(s,actor:TestOnlyPolicy.CompanionId,destination:fixture.ReceiverIdentity,
                    id:"alternate-worker-retrieve",target:fixture.TrapIdentity);var outcome=s.Execute(TestOnlySharedWorldPolicy.Host(),retrieve);
                var beforeRetrieve=s.Capture();var actorState=beforeRetrieve.Actors.Single(x=>x.Id==TestOnlyPolicy.CompanionId);
                var physical=beforeRetrieve.FishingTraps.Single(x=>x.TrapId==fixture.TrapIdentity);
                Require(outcome.Outcome==Outcome.Committed,"Alternate retrieval rejected "+outcome.Code+" at actor "+actorState.X+","+actorState.Y
                    +" and Trap "+physical.X+","+physical.Y+".");WorldAdvance(s,300);
                var v=s.Capture();var job=v.FishingTrapRetrievals.Single();var item=v.PortableEquipment.Single(x=>x.Id==fixture.TrapIdentity);
                var fish=v.FishingCreatures.Single();
                Require(job.Status==FishingTrapRetrievalStatus.Complete&&job.WorkerId==TestOnlyPolicy.CompanionId
                    &&item.CustodianId==TestOnlyPolicy.CompanionId&&fish.CustodianId==TestOnlyPolicy.CompanionId
                    &&fish.LocationId==fixture.ReceiverIdentity&&v.FishingTrapAttempts.Single().SetterId==fixture.SetterId
                    &&v.FishingTraps.Single().Status==FishingTrapPhysicalStatus.Retrieved,
                    "A different capable adjacent worker could not recover and receive the actual Trap catch.");
            });
            cases.Add("fishing_trap_setter_identity_and_check_profile_are_world_supplied",()=>{
                var fixture=new SharedFishingTrapFixture(12,1,identity:"third-setter",setterId:AdditionalTacticalActor.Id);
                uint seed=TrapSeedForDegree(fixture,TaskDegree.Success);var policy=TestOnlySharedWorldPolicy.WithFishingTrap(fixture,seed);
                var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                for(int step=0;step<4;step++){WorldStep(s,0,1,actor:fixture.SetterId);WorldAdvance(s,1);}
                WorldCommit(s,TrapOp(s,FishingTrapInteraction.Set,"third-setter-set",actor:fixture.SetterId,target:fixture.TrapIdentity));
                WorldAdvance(s,3300);
                var attempt=s.Capture().FishingTrapAttempts.Single();var setter=s.Capture().Characters.Single(x=>x.ActorId==fixture.SetterId);
                Require(attempt.SetterId==fixture.SetterId&&attempt.WisdomModifier==PlaytestCharacters.AbilityModifier(setter.Abilities[3])
                    &&attempt.ProficiencyRank==fixture.ProficiencyRank&&attempt.CheckDc==fixture.CatchDc
                    &&attempt.CheckOutcome==FishingTrapCheckOutcome.CapturedInTrap,
                    "The configured setter's own WIS and fishing-tackle profile did not resolve the supplied site opportunity.");
                var receive=TrapRetrieve(s,actor:TestOnlyPolicy.CompanionId,destination:fixture.ReceiverIdentity,
                    id:"third-setter-other-retriever",target:fixture.TrapIdentity);
                WorldCommit(s,receive);WorldAdvance(s,300);
                var state=s.Capture();var retrieval=state.FishingTrapRetrievals.Single();var body=state.FishingCreatures.Single();
                Require(retrieval.Status==FishingTrapRetrievalStatus.Complete&&retrieval.WorkerId==TestOnlyPolicy.CompanionId
                    &&retrieval.WorkerId!=attempt.SetterId&&body.LocationId==fixture.ReceiverIdentity
                    &&state.FishingTraps.Single().SiteId==fixture.SiteIdentity,
                    "Trap rules did not preserve supplied site/setter identities across a different capable retriever.");
            });
            cases.Add("fishing_trap_multiple_world_profiles_persist_and_resolve_independently",()=>{
                var river=new SharedFishingTrapFixture(12,1,identity:"riverbank",setterId:TestOnlyPolicy.CompanionId);
                var upper=new SharedFishingTrapFixture(15,2,identity:"upper-bank",trapX:4,trapY:1,receiverX:4,receiverY:2,
                    setterId:AdditionalTacticalActor.Id);
                var policy=TestOnlySharedWorldPolicy.WithFishingTraps(new[]{river,upper},seed:19);
                var reordered=TestOnlySharedWorldPolicy.WithFishingTraps(new[]{upper,river},seed:19);
                Require(policy.ContentFingerprint==reordered.ContentFingerprint,
                    "World-profile order changed the content fingerprint.");
                var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                var initial=s.Capture();
                Require(initial.FishingTraps.Length==2&&initial.FishingOpportunities.Length==2
                    &&initial.FishingCreatures.Length==2&&initial.FishingReceiveLocations.Length==2
                    &&initial.SkillTraining.Count(x=>x.SkillId=="fishing-tackle")==2,
                    "The supplied world profiles did not initialize distinct physical opportunities, stock and setters.");
                WorldCommit(s,TrapOp(s,FishingTrapInteraction.Set,"multi-river-set",actor:river.SetterId,target:river.TrapIdentity));
                WorldAdvance(s,3300);
                var firstOnly=s.Capture().FishingTrapAttempts.Single();
                Require(firstOnly.Status==FishingTrapAttemptStatus.Resolved&&firstOnly.SetterId==river.SetterId
                    &&firstOnly.CheckDc==river.CatchDc&&firstOnly.SiteId==river.SiteIdentity,
                    "The first supplied site did not use its own setter and check profile.");
                WorldCommit(s,TrapRetrieve(s,actor:river.SetterId,destination:river.ReceiverIdentity,
                    id:"multi-river-retrieve",target:river.TrapIdentity));
                WorldAdvance(s,300);
                Require(s.Capture().FishingTraps.Single(x=>x.TrapId==river.TrapIdentity).Status==FishingTrapPhysicalStatus.Retrieved
                    &&s.Capture().FishingTraps.Single(x=>x.TrapId==upper.TrapIdentity).Status==FishingTrapPhysicalStatus.Staged,
                    "Resolving the first profile changed another site's staged Trap.");
                WorldCommit(s,TrapOp(s,FishingTrapInteraction.Set,"multi-upper-set",actor:upper.SetterId,target:upper.TrapIdentity));
                WorldAdvance(s,3300);
                var checkedState=s.Capture();
                var first=checkedState.FishingTrapAttempts.Single(x=>x.TrapId==river.TrapIdentity);
                var second=checkedState.FishingTrapAttempts.Single(x=>x.TrapId==upper.TrapIdentity);
                Require(checkedState.FishingTrapAttempts.Length==2&&first.Status==FishingTrapAttemptStatus.Resolved
                    &&second.Status==FishingTrapAttemptStatus.Resolved&&first.SetterId==river.SetterId
                    &&second.SetterId==upper.SetterId&&first.CheckDc==river.CatchDc&&second.CheckDc==upper.CatchDc
                    &&first.OpportunityId==river.OpportunityIdentity&&second.OpportunityId==upper.OpportunityIdentity
                    &&first.CreatureId==river.CreatureIdentity&&second.CreatureId==upper.CreatureIdentity
                    &&checkedState.Work.Reservations.Single(x=>x.Id==first.BaitReservationId).Status==ReservationStatus.Consumed
                    &&checkedState.Work.Reservations.Single(x=>x.Id==second.BaitReservationId).Status==ReservationStatus.Consumed,
                    "A supplied site's setter, DC, stock or bait was resolved through another Trap profile.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(checkedState);
                s=new Simulation(policy,codec.Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(codec.Encode(s.Capture())),"Multiple physical Trap profiles changed across save/load.");
                WorldCommit(s,TrapRetrieve(s,actor:upper.SetterId,destination:upper.ReceiverIdentity,
                    id:"multi-upper-retrieve",target:upper.TrapIdentity));
                WorldAdvance(s,300);
                var after=s.Capture();
                Require(after.FishingTraps.Single(x=>x.TrapId==upper.TrapIdentity).Status==FishingTrapPhysicalStatus.Retrieved
                    &&after.FishingTraps.Single(x=>x.TrapId==river.TrapIdentity).Status==FishingTrapPhysicalStatus.Retrieved
                    &&after.FishingTrapRetrievals.Length==2
                    &&after.FishingTrapRetrievals.Single(x=>x.TrapId==upper.TrapIdentity).WorkerId==upper.SetterId,
                    "Retrieving one world Trap altered the other Trap's physical lifecycle.");
                bool duplicateRejected=false,rankConflictRejected=false;
                try{TestOnlySharedWorldPolicy.WithFishingTraps(new[]{river,new SharedFishingTrapFixture(identity:"riverbank")});}
                catch(ArgumentException){duplicateRejected=true;}
                try{TestOnlySharedWorldPolicy.WithFishingTraps(new[]{
                    new SharedFishingTrapFixture(12,1,identity:"same-setter-a",setterId:AdditionalTacticalActor.Id),
                    new SharedFishingTrapFixture(12,2,identity:"same-setter-b",setterId:AdditionalTacticalActor.Id)});}
                catch(ArgumentException){rankConflictRejected=true;}
                Require(duplicateRejected&&rankConflictRejected,
                    "The fixture accepted duplicate physical identities or conflicting skill ranks for one setter.");
            });
            cases.Add("fishing_trap_shared_physical_candidate_is_allocated_once_across_profiles",()=>{
                const string sharedSite="TEST_ONLY.shared-river-site",sharedCreature="TEST_ONLY.shared-river-fish",
                    sharedStock="TEST_ONLY.shared-river-stock";
                var firstProfile=new SharedFishingTrapFixture(12,1,identity:"shared-bank-a",setterId:TestOnlyPolicy.CompanionId,
                    sharedSiteIdentity:sharedSite,sharedCreatureIdentity:sharedCreature,sharedStockIdentity:sharedStock);
                var secondProfile=new SharedFishingTrapFixture(15,1,identity:"shared-bank-b",trapX:4,trapY:1,receiverX:4,receiverY:2,
                    setterId:AdditionalTacticalActor.Id,
                    sharedSiteIdentity:sharedSite,sharedCreatureIdentity:sharedCreature,sharedStockIdentity:sharedStock);
                var policy=TestOnlySharedWorldPolicy.WithFishingTraps(new[]{firstProfile,secondProfile},seed:31);
                Require(firstProfile.StockVersionIdentity!=secondProfile.StockVersionIdentity
                    &&firstProfile.OpportunityIdentity!=secondProfile.OpportunityIdentity,
                    "The contention witness must use distinct opportunity/allocation labels over one physical member.");
                var s=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                Require(s.Capture().SchemaVersion==Snapshot.FishingStockSchema&&s.Capture().FishingCreatures.Length==1
                    &&s.Capture().FishingOpportunities.Length==2&&s.Capture().FishingStockManifests.Length==2
                    &&s.Capture().FishingStockManifests.All(x=>x.SharedStockId==sharedStock&&x.PhysicalMemberIds.SequenceEqual(new[]{sharedCreature}))
                    &&s.Capture().FishingStockAllocations.All(x=>x.PhysicalMemberIds.SequenceEqual(new[]{sharedCreature})),
                    "Overlapping opportunities duplicated the same physical creature record.");
                for(int i=0;i<8;i++)WorldAdvance(s,1);
                uint randomBeforeExposure=s.Capture().RandomState;
                WorldCommit(s,TrapOp(s,FishingTrapInteraction.Set,"shared-stock-first",actor:firstProfile.SetterId,target:firstProfile.TrapIdentity));
                WorldCommit(s,TrapOp(s,FishingTrapInteraction.Set,"shared-stock-second",actor:secondProfile.SetterId,target:secondProfile.TrapIdentity));
                var pending=s.Capture();var commandOrder=pending.FishingTrapAttempts.OrderBy(x=>x.StartedAt)
                    .ThenBy(x=>long.Parse(x.Id.Substring("fishing.trap.".Length),CultureInfo.InvariantCulture)).ToArray();
                var codec=new SnapshotCodec();var pendingBytes=codec.Encode(pending);
                var restoredPending=codec.Decode(pendingBytes);
                Require(commandOrder[0].Id.EndsWith(".9",StringComparison.Ordinal)&&commandOrder[1].Id.EndsWith(".10",StringComparison.Ordinal)
                    &&restoredPending.FishingTrapAttempts[0].Id==commandOrder[1].Id,
                    "The contention witness did not exercise numeric command order against lexical save order.");
                s=new Simulation(policy,restoredPending,ExecutionProfile.Laboratory);
                WorldAdvance(s,300);
                var exposed=s.Capture();
                var first=exposed.FishingTrapAttempts.Single(x=>x.TrapId==firstProfile.TrapIdentity);
                var second=exposed.FishingTrapAttempts.Single(x=>x.TrapId==secondProfile.TrapIdentity);
                var baitReservations=exposed.Work.Reservations.Where(x=>x.Id==first.BaitReservationId||x.Id==second.BaitReservationId).ToArray();
                Require(first.Status==FishingTrapAttemptStatus.Soaking&&second.Status==FishingTrapAttemptStatus.NoResponse
                    &&first.OpportunityCommitted&&second.OpportunityCommitted
                    &&exposed.FishingOpportunities.All(x=>x.Status==FishingOpportunityStatus.Spent)
                    &&baitReservations.Length==2&&baitReservations.All(x=>x.Status==ReservationStatus.Consumed)
                    &&exposed.RandomState==randomBeforeExposure
                    &&exposed.FishingCreatures.Single().ActiveResponseAttemptId==first.Id
                    &&exposed.FishingTraps.All(x=>x.Status==FishingTrapPhysicalStatus.Deployed),
                    "Distinct allocation labels allocated the same physical response twice or refunded committed inputs.");
                var invalidVersion=exposed.Copy();
                invalidVersion.FishingStockManifests=invalidVersion.FishingStockManifests.Select(x=>new FishingStockManifestRecord(
                    x.Id,x.SharedStockId,x.VersionId,first.SetupCompletedAt.Value.AddSeconds(1),x.EffectiveUntil,x.PhysicalMemberIds)).ToArray();
                bool inapplicableVersionRejected=false;try{Validation.Snapshot(invalidVersion);}catch(ArgumentException){inapplicableVersionRejected=true;}
                Require(inapplicableVersionRejected,
                    "A committed response allocation accepted a stock version that became applicable only after exposure.");
                var bytes=codec.Encode(exposed);
                s=new Simulation(policy,codec.Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(codec.Encode(s.Capture())),"Shared-member allocation changed across save/restore.");
                WorldCommit(s,TrapRetrieve(s,actor:secondProfile.SetterId,destination:secondProfile.ReceiverIdentity,
                    id:"shared-stock-empty-trap-retrieval",target:secondProfile.TrapIdentity));
                WorldAdvance(s,300);
                var afterEmptyRetrieval=s.Capture();
                Require(afterEmptyRetrieval.FishingTraps.Single(x=>x.TrapId==secondProfile.TrapIdentity).Status==FishingTrapPhysicalStatus.Retrieved
                    &&afterEmptyRetrieval.FishingTraps.Single(x=>x.TrapId==firstProfile.TrapIdentity).Status==FishingTrapPhysicalStatus.Deployed
                    &&afterEmptyRetrieval.FishingCreatures.Single().ActiveResponseAttemptId==first.Id,
                    "Retrieving the no-response Trap removed or duplicated the other deployment's physical member.");
                WorldAdvance(s,2700);
                var resolved=s.Capture();first=resolved.FishingTrapAttempts.Single(x=>x.Id==first.Id);
                second=resolved.FishingTrapAttempts.Single(x=>x.Id==second.Id);
                var body=resolved.FishingCreatures.Single();
                Require(first.Status==FishingTrapAttemptStatus.Resolved&&first.WordsConsumed>0
                    &&second.Status==FishingTrapAttemptStatus.NoResponse&&second.WordsConsumed==0
                    &&body.CapturedByAttemptId!=second.Id&&body.ActiveResponseAttemptId=="",
                    "The shared physical candidate produced more than one response or the empty opportunity rolled a replacement.");
            });
            cases.Add("fishing_stock_manifest_membership_and_allocation_roundtrip",()=>{
                const string sharedSite="TEST_ONLY.partitioned-river-site",sharedStock="TEST_ONLY.partitioned-river-stock";
                var firstProfile=new SharedFishingTrapFixture(12,1,identity:"partition-a",setterId:TestOnlyPolicy.CompanionId,
                    sharedSiteIdentity:sharedSite,sharedStockIdentity:sharedStock);
                var secondProfile=new SharedFishingTrapFixture(15,1,identity:"partition-b",setterId:AdditionalTacticalActor.Id,
                    sharedSiteIdentity:sharedSite,sharedStockIdentity:sharedStock);
                var policy=TestOnlySharedWorldPolicy.WithFishingTraps(new[]{firstProfile,secondProfile},seed:37);
                var state=policy.Initial();
                Require(state.FishingStockManifests.Length==2&&state.FishingStockManifests.All(x=>x.SharedStockId==sharedStock
                    &&x.PhysicalMemberIds.OrderBy(id=>id,StringComparer.Ordinal).SequenceEqual(new[]{firstProfile.CreatureIdentity,secondProfile.CreatureIdentity}
                        .OrderBy(id=>id,StringComparer.Ordinal),StringComparer.Ordinal))
                    &&state.FishingStockAllocations.Length==2&&state.FishingStockAllocations.All(x=>!x.WholePool&&x.PhysicalMemberIds.Length==1),
                    "The finite stock manifest or physical-member partitions were inferred from labels instead of supplied identities.");
                var exposedMembers=state.FishingStockManifests[0].PhysicalMemberIds;exposedMembers[0]="TEST_ONLY.mutated-copy";
                Require(!state.FishingStockManifests.Any(x=>x.PhysicalMemberIds.Contains("TEST_ONLY.mutated-copy",StringComparer.Ordinal)),
                    "A caller mutated authoritative stock membership through an exposed array.");
                var codec=new SnapshotCodec();var bytes=codec.Encode(state);var restored=codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(restored))&&restored.FishingStockManifests.Length==2
                    &&restored.FishingStockAllocations.SelectMany(x=>x.PhysicalMemberIds).Distinct(StringComparer.Ordinal).Count()==2,
                    "Versioned finite membership or disjoint physical allocations changed across save/restore.");

                var invalidWholePool=restored.Copy();
                var allocation=invalidWholePool.FishingStockAllocations[0];
                invalidWholePool.FishingStockAllocations[0]=new FishingStockAllocationRecord(allocation.Id,allocation.ManifestId,
                    allocation.OpportunityId,true,allocation.PhysicalMemberIds);
                bool wholePoolRejected=false;try{Validation.Snapshot(invalidWholePool);}catch(ArgumentException){wholePoolRejected=true;}
                var invalidCandidate=restored.Copy();var opportunity=invalidCandidate.FishingOpportunities[0];
                invalidCandidate.FishingOpportunities[0]=new FishingOpportunityRecord(opportunity.Id,opportunity.SiteId,
                    opportunity.StockVersionId,secondProfile.CreatureIdentity,opportunity.Status,opportunity.ReservedByAttemptId,
                    opportunity.ReservedAt,opportunity.CommittedByAttemptId,opportunity.CommittedAt,opportunity.LastReleasedAttemptId,
                    opportunity.LastReleasedAt);
                bool nonmemberRejected=false;try{Validation.Snapshot(invalidCandidate);}catch(ArgumentException){nonmemberRejected=true;}
                Require(wholePoolRejected&&nonmemberRejected,
                    "The stock validator accepted an incomplete whole-pool allocation or a candidate outside its actual allocation.");
            });
            cases.Add("fishing_trap_cancel_before_exposure_and_abandonment_preserve_opportunity",()=>{
                var s=TrapWorld(new SharedFishingTrapFixture(12,1));TrapCommit(s,FishingTrapInteraction.Set,"set-first");
                WorldAdvance(s,299);TrapCommit(s,FishingTrapInteraction.Cancel,"cancel-first");
                Require(s.Capture().FishingTrapAttempts.Single().Status==FishingTrapAttemptStatus.Cancelled
                    &&!s.Capture().FishingTrapAttempts.Single().OpportunityCommitted
                    &&s.Capture().Work.Reservations.Single(x=>x.Id==s.Capture().FishingTrapAttempts.Single().BaitReservationId).Status==ReservationStatus.Released
                    &&s.Capture().Work.Lots.Single(x=>x.Id==SharedFishingTrapFixture.BaitLotId).Amount==new RuleQuantity(1),
                    "Pre-exposure cancellation committed the opportunity or spent its reserved bait.");
                TrapCommit(s,FishingTrapInteraction.Set,"set-second");WorldAdvance(s,300);
                var soaking=s.Capture().FishingTrapAttempts.Single(x=>x.Status==FishingTrapAttemptStatus.Soaking);
                TrapCommit(s,FishingTrapInteraction.Abandon,"abandon-second");var abandoned=s.Capture().FishingTrapAttempts.Single(x=>x.Id==soaking.Id);
                uint random=s.Capture().RandomState;WorldAdvance(s,3000);var after=s.Capture();
                abandoned=after.FishingTrapAttempts.Single(x=>x.Id==soaking.Id);
                Require(abandoned.Status==FishingTrapAttemptStatus.Abandoned&&abandoned.CheckOutcome==FishingTrapCheckOutcome.None
                    &&abandoned.OpportunityCommitted&&after.RandomState==random,
                    "Abandonment did not preserve the deployed trap/opportunity while suppressing the unattended check.");
                RejectUnchanged(s,TestOnlySharedWorldPolicy.Host(),TrapOp(s,FishingTrapInteraction.Resume,"bad-resume"),"FishingTrapDeploymentUnavailable");
            });
            cases.Add("fishing_trap_deployment_requires_compatible_bait_stock",()=>{
                var s=TrapWorld(new SharedFishingTrapFixture(12,1,hasBait:false));var initial=s.Capture();
                RejectUnchanged(s,TestOnlySharedWorldPolicy.Host(),TrapOp(s,FishingTrapInteraction.Set,"without-bait"),"FishingTrapBaitUnavailable");
                Require(s.Capture().FishingTrapAttempts.Length==0
                    &&s.Capture().Work.Lots.Single(x=>x.Id==SharedFishingTrapFixture.BaitLotId).Amount==default
                    &&s.Capture().Revision==initial.Revision,"Missing bait created a Trap deployment or changed state.");
            });
        }
    }
}
#endif
