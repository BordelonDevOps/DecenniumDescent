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
        private const string HarvestWorker=TestOnlyPolicy.CompanionId;

        private static Command HarvestCommand(Simulation s,CommandKind kind,string target="",string actor=HarvestWorker)
        {
            var state=s.Capture();
            return new Command("harvest.command."+(state.Revision+1),actor,state.Revision,kind,target);
        }

        private static Command HarvestRequirementCommand(Simulation s,CommandKind kind,string target,InventoryRequest request=null)
        {
            var state=s.Capture();
            return new Command("mgt05a.requirement."+(state.Revision+1),HarvestWorker,state.Revision,kind,target,inventory:request);
        }

        private static void HarvestCommit(Simulation s,Command command)
        {
            var result=s.Execute(TestOnlySharedWorldPolicy.Host(),command);
            Require(result.Outcome==Outcome.Committed,command.Kind+" rejected: "+result.Code);
        }

        private static uint HarvestSeedFor(TaskDegree degree,int modifier,bool disadvantage=false)
        {
            for(uint seed=1;seed<uint.MaxValue;seed++)
                if(PlaytestRolls.TaskCheck(PlaytestDice.RollD20(seed,disadvantageSources:disadvantage?1:0).Natural,modifier,12).Degree==degree)return seed;
            throw new Exception("No deterministic harvest check seed for "+degree+".");
        }

        private static int HarvestModifier(Snapshot state)
        {
            var worker=state.Characters.Single(x=>x.ActorId==HarvestWorker);
            var training=state.SkillTraining.SingleOrDefault(x=>x.ActorId==HarvestWorker&&x.SkillId=="fishing-tackle");
            return checked(PlaytestCharacters.AbilityModifier(worker.Abilities[3])
                +(training==null?0:PlaytestCharacters.ProficiencyBonus(worker.Levels.Count)*(training.ProficiencyRank==2?2:1)));
        }

        private static uint HarvestSmallSeedFor(TaskDegree degree,int modifier,bool disadvantage=false)
        {
            for(uint seed=1;seed<uint.MaxValue;seed++) {
                var yield=HarvestYieldRules.Roll(HarvestSize.Small,seed);
                if(yield.Units!=2)continue;
                if(PlaytestRolls.TaskCheck(PlaytestDice.RollD20(yield.RandomAfter,disadvantageSources:disadvantage?1:0).Natural,modifier,12).Degree==degree)
                    return seed;
            }
            throw new Exception("No deterministic two-unit Small harvest seed for "+degree+".");
        }

        private static Command HarvestBatchCommand(Simulation simulation,string[] categories,string failurePreference="",string criticalPreference="",
            string actor=HarvestWorker,string commandId=null)
        {
            var state=simulation.Capture();
            var selection=new HarvestSelectionRequest("TEST_ONLY.small-river-fish-anatomy-v1",categories,failurePreference,criticalPreference);
            return new Command(commandId??"harvest.batch."+(state.Revision+1),actor,state.Revision,CommandKind.StartHarvest,
                SharedHarvestFixture.ManifestId,harvestSelection:selection);
        }

        private static Command HarvestPreservationSourceCommand(Simulation simulation)
        {
            var state=simulation.Capture();var manifest=state.HarvestManifests.Single();
            return new Command("mgt05a.harvest."+(state.Revision+1),HarvestWorker,state.Revision,CommandKind.StartHarvest,
                manifest.Id,harvestSelection:new HarvestSelectionRequest(manifest.AnatomyVersionId,
                    new[]{SharedHarvestFixture.CategoryRecordId}));
        }

        private static void AddHarvestCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("harvest_fixture_is_finite_dead_source_and_preserves_unknown_food_identity",()=>{
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture());var simulation=World(policy);
                var state=simulation.Capture();
                Require(state.SchemaVersion==Snapshot.HarvestSchema&&state.TestOnly&&!state.InventoryCombat
                    &&state.HarvestDonors.Length==1&&state.HarvestManifests.Length==1&&state.HarvestCategories.Length==1
                    &&state.HarvestUnits.Length==1&&state.HarvestAttempts.Length==0,
                    "Harvest fixture did not establish one explicitly bounded finite source.");
                var body=state.FishingCreatures.Single(x=>x.Id==SharedHarvestFixture.CreatureId);
                var donor=state.HarvestDonors.Single();var unit=state.HarvestUnits.Single();
                Require(body.LifeState==FishingCreatureLifeState.Dead&&body.ActiveResponseAttemptId==""
                    &&body.ContainerId==""&&donor.CreatureId==body.Id&&donor.DeathAt==default
                    &&donor.OriginalMassPounds==new RuleQuantity(1)&&unit.Status==HarvestUnitStatus.Available
                    &&unit.ValueCopper==null&&unit.MassPounds==RuleQuantity.FromFraction(1,4)
                    &&!state.InventoryLots.Any(x=>x.LotId==unit.Id)&&!state.Work.Lots.Any(x=>x.Id==unit.Id),
                    "Initial source was created as inventory, had a fabricated sale value, or lacked physical remains.");
                Throws<InvalidOperationException>(()=>new Simulation(policy,policy.Initial(),ExecutionProfile.Release));
                var encoded=new SnapshotCodec().Encode(state);var restored=new SnapshotCodec().Decode(encoded);
                Require(encoded.SequenceEqual(new SnapshotCodec().Encode(restored))&&restored.HarvestDonors.Single().LifecycleEventId==donor.LifecycleEventId,
                    "Finite source provenance changed through a save round trip.");
            });

            cases.Add("harvest_success_spends_exact_work_and_settles_same_finite_unit",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture());
                int modifier=HarvestModifier(unseeded.Initial());uint seed=HarvestSeedFor(TaskDegree.Success,modifier);
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(),seed);var simulation=World(policy);
                var initial=simulation.Capture();var unit=initial.HarvestUnits.Single();var donor=initial.HarvestDonors.Single();
                var start=HarvestCommand(simulation,CommandKind.StartHarvest,SharedHarvestFixture.CategoryRecordId);
                HarvestCommit(simulation,start);var attempt=simulation.Capture().HarvestAttempts.Single();
                Require(attempt.Status==HarvestAttemptStatus.Working&&attempt.Duration==new RuleTime(600)
                    &&attempt.CheckDc==12&&attempt.WorkDone==default&&simulation.Capture().RandomState==initial.RandomState,
                    "Starting extraction rolled early or used a duration/DC outside the fixed profile.");
                WorldAdvance(simulation,300);
                string save=Path.Combine(directory,"harvest-active.bin");new FileSaveStore().Save(save,simulation.Capture());
                simulation=new Simulation(policy,new FileSaveStore().Load(save),ExecutionProfile.Laboratory);
                Require(simulation.Capture().HarvestAttempts.Single().WorkDone==new RuleTime(300)
                    &&simulation.Capture().HarvestAttempts.Single().Status==HarvestAttemptStatus.Working,
                    "Active extraction progress did not survive restoration at the exact halfway point.");
                WorldAdvance(simulation,300);var state=simulation.Capture();attempt=state.HarvestAttempts.Single();
                var body=state.FishingCreatures.Single(x=>x.Id==donor.CreatureId);
                var inventory=state.InventoryLots.Single(x=>x.LotId==unit.Id);var physical=state.PortableEquipment.Single(x=>x.Id==unit.Id);
                var lot=state.Work.Lots.Single(x=>x.Id==unit.Id);
                Require(attempt.Status==HarvestAttemptStatus.Success&&attempt.CompletedAt==new RuleTime(600)
                    &&attempt.Degree==HarvestCheckDegree.Success&&attempt.Natural==PlaytestDice.RollD20(initial.RandomState).Natural
                    &&attempt.ProficiencyRank==1&&attempt.ProficiencyBonus==PlaytestCharacters.ProficiencyBonus(initial.Characters.Single(x=>x.ActorId==HarvestWorker).Levels.Count)
                    &&attempt.DiceSelection==HarvestDiceSelection.Normal&&attempt.SecondDie==0
                    &&unit.Id==inventory.LotId&&inventory.OwnerId==donor.OwnerId&&inventory.Nutrition==NutritionKind.None
                    &&inventory.FreshUntil==unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds)
                    &&unit.PreservationAt(unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds))==HarvestPreservationState.Degraded
                    &&unit.PreservationAt(unit.OriginAt.AddSeconds(2*unit.PreservationIntervalSeconds))==HarvestPreservationState.Spoiled
                    &&lot.Id==unit.Id&&lot.UnitId==SharedHarvestFixture.MaterialUnit&&lot.Amount==unit.MassPounds
                    &&physical.LinkedId==unit.Id&&physical.MassBasis==PortableMassBasis.GenericPounds
                    &&body.MassPounds==donor.OriginalMassPounds-unit.MassPounds&&body.LifeState==FishingCreatureLifeState.Dead
                    &&state.HarvestUnits.Single().Status==HarvestUnitStatus.Extracted,
                    "Successful extraction failed to settle the precommitted unit into the existing inventory while conserving remains mass.");
                var bytes=new SnapshotCodec().Encode(state);var restored=new Simulation(policy,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(new SnapshotCodec().Encode(restored.Capture())),"Settled harvest output changed through save/restore.");
                var split=state.Copy();OrdinaryInventory.Descendant(split,unit.Id,"harvest.portion.1",RuleQuantity.FromFraction(1,10),
                    SharedHarvestFixture.ContainerId,donor.OwnerId,InventoryAccess.Stowed);
                Validation.Snapshot(split);
                Require(split.InventoryLots.Single(x=>x.LotId=="harvest.portion.1").FreshUntil==inventory.FreshUntil
                    &&split.Work.Lots.Single(x=>x.Id==unit.Id).Amount==RuleQuantity.FromFraction(3,20)
                    &&split.PortableEquipment.Single(x=>x.Id=="harvest.portion.1").MassBasis==PortableMassBasis.GenericPounds,
                    "A descendant resource lot lost its source freshness, mass, or portable cargo identity.");
                var replay=simulation.Execute(host,start);
                Require(replay.Outcome==Outcome.Duplicate&&bytes.SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "Duplicate start command repeated or altered the completed extraction.");
                var retry=HarvestCommand(simulation,CommandKind.StartHarvest,SharedHarvestFixture.CategoryRecordId);
                RejectUnchanged(simulation,host,retry,"HarvestSelectionExhausted");
            });

            cases.Add("mgt05a_harvest_mass_preservation_work_deadline_save_restore_and_replay",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvestPreservation(new SharedHarvestFixture());
                int modifier=HarvestModifier(unseeded.Initial());uint seed=HarvestSeedFor(TaskDegree.Success,modifier);
                var policy=TestOnlySharedWorldPolicy.WithHarvestPreservation(new SharedHarvestFixture(),seed);
                var simulation=World(policy);var initial=simulation.Capture();var source=initial.HarvestUnits.Single();
                HarvestCommit(simulation,HarvestPreservationSourceCommand(simulation));
                WorldAdvance(simulation,600);
                var harvested=simulation.Capture();var extracted=harvested.HarvestUnits.Single(x=>x.Id==source.Id);
                Require(extracted.Status==HarvestUnitStatus.Extracted&&extracted.ValueCopper==null
                    &&HarvestPreservationRules.TryProject(harvested,source.Id,out var freshRoot)
                    &&freshRoot.State==HarvestPreservationState.Fresh&&freshRoot.ValueMultiplier==new RuleQuantity(1),
                    "Actual finite harvest output was not recognized as fresh physical mass with its original unknown value.");

                var portion=IC(simulation,CommandKind.PortionInventory,source.Id,
                    new InventoryRequest(RuleQuantity.FromFraction(1,10),"",HandlingKind.Pickup),HarvestWorker);
                HarvestCommit(simulation,portion);
                var split=simulation.Capture();var child=split.InventoryLots.Single(x=>x.ParentId==source.Id);
                var rootAmount=split.Work.Lots.Single(x=>x.Id==source.Id).Amount;
                var childAmount=split.Work.Lots.Single(x=>x.Id==child.LotId).Amount;
                Require(rootAmount+childAmount==source.MassPounds&&child.OwnerId==split.InventoryLots.Single(x=>x.LotId==source.Id).OwnerId
                    &&child.FreshUntil==split.InventoryLots.Single(x=>x.LotId==source.Id).FreshUntil
                    &&split.PortableEquipment.Single(x=>x.Id==child.LotId).MassBasis==PortableMassBasis.GenericPounds,
                    "The physical mass split changed origin, freshness, ownership, or portable identity.");
                var freshness=child.FreshUntil;

                PortableCommit(simulation,Portable(simulation,CommandKind.HandlePortableEquipment,child.LotId,
                    handling:HandlingKind.Retrieve,actor:HarvestWorker));
                var retrieved=simulation.Capture();var carried=retrieved.PortableEquipment.Single(x=>x.Id==child.LotId);
                Require(carried.ParentId==""&&carried.Placement==PortablePlacement.Carried&&carried.CustodianId==HarvestWorker
                    &&retrieved.InventoryLots.Single(x=>x.LotId==child.LotId).OwnerId==child.OwnerId
                    &&retrieved.Work.Lots.Single(x=>x.Id==child.LotId).LocationId==HarvestWorker
                    &&retrieved.InventoryLots.Single(x=>x.LotId==child.LotId).FreshUntil==freshness,
                    "Retrieval failed to move custody through the portable authority while retaining owner and source freshness.");

                var unit=retrieved.HarvestUnits.Single(x=>x.Id==source.Id);
                RuleTime b1=unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds);
                Require(b1.Denominator==1&&retrieved.RuleClock.Denominator==1&&b1>retrieved.RuleClock,
                    "Fixture no longer leaves a bounded integral interval before B1.");
                RuleTime remaining=new RuleTime(b1.Numerator-retrieved.RuleClock.Numerator);
                Require(remaining.Numerator>10,"Fixture no longer leaves a bounded interval before B1.");
                WorldAdvance(simulation,checked((int)remaining.Numerator-10));
                Require(simulation.DiscoverCommands(host,HarvestWorker).Any(x=>x.Command.Kind==CommandKind.StartHarvestRequirementWork
                    &&x.Command.Target==child.LotId&&x.Query.Admissible),"Fresh extracted mass did not produce a discoverable bound-work option.");
                var start=HarvestRequirementCommand(simulation,CommandKind.StartHarvestRequirementWork,child.LotId,
                    new InventoryRequest(childAmount,"",HandlingKind.Pickup));
                byte[] beforeQuery=Bytes(simulation);var startQuery=simulation.QueryCommand(host,start);
                Require(startQuery.Supported&&startQuery.Admissible&&startQuery.Costs.Any(x=>x.Kind=="work-seconds"
                    &&x.Amount==checked(unit.PreservationIntervalSeconds*2L))&&beforeQuery.SequenceEqual(Bytes(simulation)),
                    "Pure command query did not expose the bounded adapter work while preserving authoritative state.");
                var startResult=simulation.Execute(host,start);
                if(startResult.Outcome!=Outcome.Committed) {
                    var diagnostic=simulation.Capture();string resolver=policy.Resolve(diagnostic,start);
                    string snapshotError="";try { Validation.Snapshot(diagnostic); } catch(Exception ex) { snapshotError=ex.Message; }
                    string policyError=policy.ValidateState(diagnostic);
                    throw new Exception("Fresh adapter start rejected: "+startResult.Code+"; resolver="+resolver
                        +"; snapshot="+snapshotError+"; policy="+policyError);
                }
                var work=simulation.Capture().HarvestRequirementWorks.Single();
                Require(work.Status==HarvestRequirementWorkStatus.Working&&work.Requirement==HarvestIngredientRequirement.Fresh
                    &&simulation.Capture().Work.Reservations.Single(x=>x.Id==work.ReservationId).RemainingAmount==childAmount,
                    "Fresh-required adapter work failed to reserve the existing physical portion.");
                WorldAdvance(simulation,2);
                HarvestCommit(simulation,HarvestRequirementCommand(simulation,CommandKind.PauseHarvestRequirementWork,work.Id));
                var paused=simulation.Capture();work=paused.HarvestRequirementWorks.Single();
                Require(work.Status==HarvestRequirementWorkStatus.Paused&&work.Work.Labor==new RuleTime(2)
                    &&work.Work.Retained==work.Work.Labor&&paused.Work.Reservations.Single(x=>x.Id==work.ReservationId).RemainingAmount==childAmount,
                    "Explicit pause lost credited work or released the input reservation.");

                string pausedPath=Path.Combine(directory,"mgt05a-paused.ddsave");var store=new FileSaveStore();store.Save(pausedPath,paused);
                var codec=new SnapshotCodec();byte[] pausedBytes=codec.Encode(paused);
                simulation=new Simulation(policy,store.Load(pausedPath),ExecutionProfile.Laboratory);
                Require(pausedBytes.SequenceEqual(Bytes(simulation)),"Paused adapter state changed through the supported save/restore path.");
                var resume=HarvestRequirementCommand(simulation,CommandKind.ResumeHarvestRequirementWork,work.Id);
                var replayA=new Simulation(policy,codec.Decode(pausedBytes),ExecutionProfile.Laboratory);
                var replayB=new Simulation(policy,codec.Decode(pausedBytes),ExecutionProfile.Laboratory);
                HarvestCommit(replayA,resume);HarvestCommit(replayB,resume);
                WorldAdvance(replayA,8);WorldAdvance(replayB,8);
                Require(Bytes(replayA).SequenceEqual(Bytes(replayB)),"Identical resume and clock commands did not deterministically replay from the same save.");

                var splitAdvance=new Simulation(policy,codec.Decode(pausedBytes),ExecutionProfile.Laboratory);
                HarvestCommit(splitAdvance,HarvestRequirementCommand(splitAdvance,CommandKind.ResumeHarvestRequirementWork,work.Id));
                WorldAdvance(splitAdvance,4);
                string workingPath=Path.Combine(directory,"mgt05a-working.ddsave");store.Save(workingPath,splitAdvance.Capture());
                splitAdvance=new Simulation(policy,store.Load(workingPath),ExecutionProfile.Laboratory);
                var finalAdvance=IC(splitAdvance,CommandKind.AdvanceClock,x:4,y:1);var finalResult=splitAdvance.Execute(host,finalAdvance);
                if(finalResult.Outcome!=Outcome.Committed) {
                    var diagnostic=splitAdvance.Capture();string resolver=policy.Resolve(diagnostic,finalAdvance);
                    string snapshotError="";try { Validation.Snapshot(diagnostic); } catch(Exception ex) { snapshotError=ex.Message; }
                    throw new Exception("Split B1 advance rejected: "+finalResult.Code+"; resolver="+resolver+"; snapshot="+snapshotError
                        +"; policy="+policy.ValidateState(diagnostic));
                }

                var atB1=replayA.Capture();var atB1Split=splitAdvance.Capture();
                var first=atB1.HarvestRequirementWorks.Single();var splitWork=atB1Split.HarvestRequirementWorks.Single();
                Require(atB1.RuleClock==b1&&atB1Split.RuleClock==b1
                    &&first.Status==HarvestRequirementWorkStatus.Paused&&first.PauseReason==HarvestRequirementPauseReason.IngredientNotFresh
                    &&first.Work.Labor==new RuleTime(10)&&splitWork.Work.Labor==first.Work.Labor
                    &&atB1.Work.Reservations.Single(x=>x.Id==first.ReservationId).RemainingAmount==childAmount
                    &&atB1.Work.Reservations.Single(x=>x.Id==first.ReservationId).ConsumedAmount==default
                    &&HarvestPreservationRules.TryProject(atB1,child.LotId,out var degraded)
                    &&degraded.State==HarvestPreservationState.Degraded&&degraded.ValueMultiplier==new RuleQuantity(1,2)
                    &&degraded.HarvestUnitId==source.Id&&atB1.InventoryLots.Single(x=>x.LotId==child.LotId).FreshUntil==freshness,
                    "Whole and split clock advancement did not stop at exact B1 with identical credit, retained reservation, and derived half-value degradation.");
                var resumeAtB1=HarvestRequirementCommand(replayA,CommandKind.ResumeHarvestRequirementWork,first.Id);
                byte[] beforeDeniedQuery=Bytes(replayA);var denied=replayA.QueryCommand(host,resumeAtB1);
                Require(denied.Supported&&!denied.Admissible&&denied.Code=="FreshIngredientRequired"
                    &&beforeDeniedQuery.SequenceEqual(Bytes(replayA)),"B1 Fresh-only resume was not denied by a pure query.");

                WorldAdvance(replayA,unit.PreservationIntervalSeconds);
                var atB2=replayA.Capture();
                Require(HarvestPreservationRules.TryProject(atB2,child.LotId,out var spoiled)
                    &&spoiled.State==HarvestPreservationState.Spoiled&&spoiled.ValueMultiplier==default
                    &&atB2.HarvestRequirementWorks.Single().Status==HarvestRequirementWorkStatus.Paused
                    &&atB2.Work.Reservations.Single(x=>x.Id==first.ReservationId).RemainingAmount==childAmount,
                    "The second sourced interval failed to derive Spoiled/zero multiplier while retaining unfinished reservation state.");
            });

            cases.Add("mgt05a_rejects_unbound_generic_mass_and_schema73_preservation_split",()=>{
                var policy=TestOnlySharedWorldPolicy.WithHarvestPreservation(new SharedHarvestFixture(),seed:17);
                var simulation=World(policy);HarvestCommit(simulation,HarvestPreservationSourceCommand(simulation));
                WorldAdvance(simulation,600);var harvested=simulation.Capture();
                string unrelated="TEST_ONLY.unbound-generic-pound";var unrelatedState=harvested.Copy();
                unrelatedState.Work=new WorkLedger(unrelatedState.Work.Lots.Concat(new[]{new ResourceLot(unrelated,SharedHarvestFixture.MaterialUnit,
                    RuleQuantity.FromFraction(1,10),HarvestWorker,HarvestWorker)}),unrelatedState.Work.WorkerIntervals,unrelatedState.Work.Reservations);
                unrelatedState.InventoryLots=unrelatedState.InventoryLots.Concat(new[]{new InventoryLotRecord(unrelated,"",HarvestWorker,
                    RuleQuantity.FromFraction(1,10),unrelatedState.RuleClock,NutritionKind.None,null,InventoryAccess.Ready)}).ToArray();
                unrelatedState.PortableEquipment=unrelatedState.PortableEquipment.Concat(new[]{new PortableEquipmentRecord(unrelated,
                    "prototype.generic-pound-lot",HarvestWorker,HarvestWorker,"",PortablePlacement.Carried,PortableLinkKind.InventoryLot,
                    unrelated,PortableMassBasis.GenericPounds,RuleQuantity.FromFraction(1,10),null)}).ToArray();
                Validation.Snapshot(unrelatedState);
                var badPortion=new Command("mgt05a.unbound-portion",HarvestWorker,unrelatedState.Revision,CommandKind.PortionInventory,
                    unrelated,inventory:new InventoryRequest(RuleQuantity.FromFraction(1,20),"",HandlingKind.Pickup));
                byte[] unrelatedBefore=new SnapshotCodec().Encode(unrelatedState);
                string unrelatedResult=new TestOnlyInventoryPolicy().Resolve(unrelatedState,badPortion);
                Require(unrelatedResult=="UnsupportedInventoryProfile"&&unrelatedBefore.SequenceEqual(new SnapshotCodec().Encode(unrelatedState)),
                    "Unbound generic mass was accepted or mutated by the schema74 inventory handler.");

                var schema73=harvested.Copy();schema73.SchemaVersion=Snapshot.PortableCountedLotSchema;
                schema73.HarvestRequirementWorks=Array.Empty<HarvestRequirementWorkRecord>();Validation.Snapshot(schema73);
                var unsupported=IC(simulation,CommandKind.PortionInventory,harvested.HarvestUnits.Single().Id,
                    new InventoryRequest(RuleQuantity.FromFraction(1,10),"",HandlingKind.Pickup),HarvestWorker);
                byte[] before=new SnapshotCodec().Encode(schema73);
                string result=new TestOnlyInventoryPolicy().Resolve(schema73,unsupported);
                Require(result=="UnsupportedInventoryProfile"&&before.SequenceEqual(new SnapshotCodec().Encode(schema73)),
                    "Schema73 preservation split result="+result+" bytesStable="
                    +before.SequenceEqual(new SnapshotCodec().Encode(schema73))+"; schema74 lineage behavior must remain unsupported.");
            });

            cases.Add("harvest_critical_failure_records_trade_accident_and_applies_life_damage",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture());
                int modifier=HarvestModifier(unseeded.Initial());uint seed=HarvestSeedFor(TaskDegree.CriticalFailure,modifier);
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(),seed);var simulation=World(policy);
                var before=simulation.Capture();var start=HarvestCommand(simulation,CommandKind.StartHarvest,SharedHarvestFixture.CategoryRecordId);
                HarvestCommit(simulation,start);WorldAdvance(simulation,600);var state=simulation.Capture();
                var attempt=state.HarvestAttempts.Single();var life=state.Lives.Single(x=>x.ActorId==HarvestWorker);
                Require(attempt.Status==HarvestAttemptStatus.CriticalFailure&&attempt.Degree==HarvestCheckDegree.CriticalFailure
                    &&attempt.D4Rolled>=1&&attempt.D4Rolled<=4&&attempt.AccidentDamageType=="piercing"
                    &&attempt.DamageApplied==attempt.D4Rolled&&life.Hp==ActorLifeRules.Read(before.Lives.Single(x=>x.ActorId==HarvestWorker)).Hp-attempt.DamageApplied
                    &&state.HarvestUnits.Single().Status==HarvestUnitStatus.Ruined
                    &&state.FishingCreatures.Single().MassPounds==before.FishingCreatures.Single().MassPounds,
                    "Critical failure did not record the fishing-trade piercing accident, apply life damage, and preserve donor remains.");
                var bytes=new SnapshotCodec().Encode(state);var restored=new Simulation(policy,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(new SnapshotCodec().Encode(restored.Capture()))
                    &&restored.Capture().HarvestAttempts.Single().AccidentDamageType=="piercing",
                    "Critical-failure damage type or audit changed through save/restore.");
            });

            cases.Add("harvest_failure_ruins_only_selected_unit_and_cannot_be_retried",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture());
                int modifier=HarvestModifier(unseeded.Initial());uint seed=HarvestSeedFor(TaskDegree.Failure,modifier);
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(),seed);var simulation=World(policy);
                var initial=simulation.Capture();var start=HarvestCommand(simulation,CommandKind.StartHarvest,SharedHarvestFixture.CategoryRecordId);
                HarvestCommit(simulation,start);WorldAdvance(simulation,600);var state=simulation.Capture();
                var attempt=state.HarvestAttempts.Single();var unit=state.HarvestUnits.Single();
                Require(attempt.Status==HarvestAttemptStatus.Failure&&attempt.Degree==HarvestCheckDegree.Failure
                    &&unit.Status==HarvestUnitStatus.Ruined&&state.FishingCreatures.Single().MassPounds==initial.FishingCreatures.Single().MassPounds
                    &&!state.InventoryLots.Any(x=>x.LotId==unit.Id)&&!state.Work.Lots.Any(x=>x.Id==unit.Id)
                    &&state.RandomState!=initial.RandomState,
                    "Failed extraction awarded material, consumed the full donor, or failed to record its check.");
                RejectUnchanged(simulation,host,HarvestCommand(simulation,CommandKind.StartHarvest,SharedHarvestFixture.CategoryRecordId),"HarvestSelectionExhausted");
            });

            cases.Add("harvest_pause_resume_and_tactical_entry_preserve_credit_without_overlap",()=>{
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(),seed:23);var simulation=World(policy);
                HarvestCommit(simulation,HarvestCommand(simulation,CommandKind.StartHarvest,SharedHarvestFixture.CategoryRecordId));
                string attemptId=simulation.Capture().HarvestAttempts.Single().Id;WorldAdvance(simulation,100);
                HarvestCommit(simulation,HarvestCommand(simulation,CommandKind.PauseHarvest,attemptId));
                var paused=simulation.Capture().HarvestAttempts.Single();
                Require(paused.Status==HarvestAttemptStatus.Paused&&paused.WorkDone==new RuleTime(100)
                    &&!simulation.Capture().Work.WorkerIntervals.Any(x=>x.JobId==attemptId&&x.Start<=simulation.Capture().RuleClock&&x.End>simulation.Capture().RuleClock),
                    "Manual pause released neither active labor nor exact earned progress.");
                string path=Path.Combine(directory,"harvest-paused.bin");new FileSaveStore().Save(path,simulation.Capture());
                simulation=new Simulation(policy,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                HarvestCommit(simulation,HarvestCommand(simulation,CommandKind.ResumeHarvest,attemptId));WorldAdvance(simulation,100);
                Require(simulation.Capture().HarvestAttempts.Single().WorkDone==new RuleTime(200),
                    "Resumed work discarded or duplicated progress.");
                HarvestCommit(simulation,IC(simulation,CommandKind.BeginFixedEncounter));var combat=simulation.Capture();
                Require(combat.InventoryCombat&&combat.HarvestAttempts.Single().Status==HarvestAttemptStatus.Paused
                    &&combat.HarvestAttempts.Single().WorkDone==new RuleTime(200)
                    &&!combat.Work.WorkerIntervals.Any(x=>x.JobId==attemptId&&x.Start<=combat.RuleClock&&x.End>combat.RuleClock),
                    "Entering tactical control failed to pause off-calendar extraction at the shared clock boundary.");
                RejectUnchanged(simulation,host,HarvestCommand(simulation,CommandKind.ResumeHarvest,attemptId),"HarvestingRequiresExploration");
            });

            cases.Add("harvest_untrained_generic_attempt_uses_wisdom_zero_proficiency_and_disadvantage",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(trained:false));
                var initial=unseeded.Initial();int wisdom=PlaytestCharacters.AbilityModifier(initial.Characters.Single(x=>x.ActorId==HarvestWorker).Abilities[3]);
                uint seed=HarvestSeedFor(TaskDegree.Success,wisdom,disadvantage:true);
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(trained:false),seed);var simulation=World(policy);
                var before=simulation.Capture();
                var start=HarvestCommand(simulation,CommandKind.StartHarvest,SharedHarvestFixture.CategoryRecordId);
                HarvestCommit(simulation,start);var working=simulation.Capture().HarvestAttempts.Single();
                Require(working.ProficiencyRank==0&&working.ProficiencyBonus==0&&working.AbilityModifier==wisdom
                    &&!simulation.Capture().SkillTraining.Any(x=>x.ActorId==HarvestWorker&&x.SkillId=="fishing-tackle"),
                    "Untrained generic harvesting was blocked or received a proficiency contribution.");
                WorldAdvance(simulation,600);var attempt=simulation.Capture().HarvestAttempts.Single();
                var expected=PlaytestDice.RollD20(before.RandomState,disadvantageSources:1);
                Require(attempt.Status==HarvestAttemptStatus.Success&&attempt.DiceSelection==HarvestDiceSelection.Disadvantage
                    &&attempt.FirstDie==expected.First&&attempt.SecondDie==expected.Second&&attempt.Natural==expected.Natural
                    &&attempt.CheckModifier==wisdom&&attempt.Degree==HarvestCheckDegree.Success,
                    "Untrained generic harvesting did not use Wisdom, zero proficiency and the shared disadvantage roll.");
            });

            cases.Add("harvest_rejects_missing_tools_and_prohibited_origin_without_cost",()=>{
                foreach(var fixture in new[]{new SharedHarvestFixture(hasToolkit:false),
                    new SharedHarvestFixture(originRestriction:HarvestOriginRestriction.Prohibited)}) {
                    var simulation=World(TestOnlySharedWorldPolicy.WithHarvest(fixture));var before=simulation.Capture();
                    string expected=!fixture.HasToolkit?"FishingToolkitUnavailable":"HarvestOriginProhibited";
                    RejectUnchanged(simulation,host,HarvestCommand(simulation,CommandKind.StartHarvest,SharedHarvestFixture.CategoryRecordId),expected);
                    Require(new SnapshotCodec().Encode(before).SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                        "Rejected harvest mutated time, source state, or RNG.");
                }
                var malformed=World(TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture())).Capture();
                malformed.FishingCreatures=malformed.FishingCreatures.Select(x=>x.WithMassPounds(RuleQuantity.FromFraction(3,4))).ToArray();
                Throws<ArgumentException>(()=>Validation.Snapshot(malformed));
            });

            cases.Add("harvest_schema42_rolls_small_yield_once_and_roundtrips_batch_selection",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed:2);
                var initial=unseeded.Initial();var manifest=initial.HarvestManifests.Single();
                var yield=HarvestYieldRules.Roll(HarvestSize.Small,2);
                Require(initial.SchemaVersion==Snapshot.HarvestManifestSchema&&manifest.Size==HarvestSize.Small
                    &&initial.HarvestDonors.Single().AnatomyProfileId==manifest.AnatomyVersionId
                    &&manifest.FullTimeSeconds==20*60&&manifest.BaseYieldUnits==2&&manifest.BaseYieldDice.SequenceEqual(new[]{2})
                    &&manifest.YieldRandomBefore==2&&manifest.YieldRandomAfter==initial.RandomState
                    &&manifest.YieldWordsConsumed==yield.WordsConsumed&&manifest.BaseYieldUnits==yield.Units,
                    "Small finite yield was not resolved once from its source-sized dice at manifest creation.");
                var bytes=new SnapshotCodec().Encode(initial);var restored=new SnapshotCodec().Decode(bytes);
                Require(bytes.SequenceEqual(new SnapshotCodec().Encode(restored))
                    &&restored.HarvestManifests.Single().BaseYieldDice.SequenceEqual(new[]{2})
                    &&restored.RandomState==initial.RandomState,"The finite yield receipt changed through schema42 save/load.");
            });

            cases.Add("harvest_schema42_full_two_category_selection_uses_one_check_and_replays",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed:2);
                int modifier=HarvestModifier(unseeded.Initial());uint seed=HarvestSmallSeedFor(TaskDegree.Success,modifier);
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed);var simulation=World(policy);
                var before=simulation.Capture();
                var wrongVersion=new Command("harvest.batch.wrong-version",HarvestWorker,before.Revision,CommandKind.StartHarvest,
                    SharedHarvestFixture.ManifestId,harvestSelection:new HarvestSelectionRequest("TEST_ONLY.wrong-river-fish-anatomy-v1",
                        new[]{SharedHarvestFixture.CategoryRecordId}));
                RejectUnchanged(simulation,host,wrongVersion,"HarvestManifestVersionMismatch");
                Require(new SnapshotCodec().Encode(before).SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "A mismatched anatomy version changed time, RNG, or selection state.");
                var command=HarvestBatchCommand(simulation,new[]{SharedHarvestFixture.CategoryRecordId,SharedHarvestFixture.CategoryRecordId2},
                    criticalPreference:SharedHarvestFixture.RecoveryUnitId,commandId:"harvest.batch.full");
                HarvestCommit(simulation,command);var attempt=simulation.Capture().HarvestAttempts.Single();
                Require(attempt.Duration==new RuleTime(20*60)&&attempt.SelectedCategoryIds.Length==2
                    &&attempt.SelectedUnitIds.Length==3&&simulation.Capture().RandomState==before.RandomState,
                    "Full Small allocation did not book twenty minutes and one shared check without rolling early.");
                var receipt=simulation.Capture().Receipts.Single(x=>x.Id==command.Id);
                var reconstructed=CommandHistory.Read(receipt);
                Require(reconstructed.MatchesReceipt(receipt)&&reconstructed.HarvestSelection.CategoryIds.Length==2
                    &&reconstructed.HarvestSelection.CriticalRecoveryPreference==SharedHarvestFixture.RecoveryUnitId,
                    "Batch category and conditional choice were not reconstructible from the canonical command receipt.");
                string path=Path.Combine(directory,"harvest-schema42-active.bin");new FileSaveStore().Save(path,simulation.Capture());
                simulation=new Simulation(policy,new FileSaveStore().Load(path),ExecutionProfile.Laboratory);
                WorldAdvance(simulation,20*60);var state=simulation.Capture();attempt=state.HarvestAttempts.Single();
                Require(attempt.Status==HarvestAttemptStatus.Success&&attempt.SelectedUnitIds.Length==3
                    &&state.HarvestUnits.Count(x=>x.Status==HarvestUnitStatus.Extracted)==2
                    &&state.HarvestUnits.Single(x=>x.Id==SharedHarvestFixture.RecoveryUnitId).Status==HarvestUnitStatus.Available
                    &&state.FishingCreatures.Single().MassPounds==RuleQuantity.FromFraction(1,2)
                    &&state.InventoryLots.Count(x=>x.LotId==SharedHarvestFixture.UnitId||x.LotId==SharedHarvestFixture.UnitId2)==2,
                    "One successful full-manifest check did not extract both baseline units atomically.");
                var settled=new SnapshotCodec().Encode(state);var restored=new Simulation(policy,new SnapshotCodec().Decode(settled),ExecutionProfile.Laboratory);
                Require(settled.SequenceEqual(new SnapshotCodec().Encode(restored.Capture()))
                    &&restored.Execute(host,reconstructed).Outcome==Outcome.Duplicate,
                    "Batch outcome or duplicate command replay changed after save/load.");
            });

            cases.Add("harvest_schema42_partial_category_costs_half_time_and_forfeits_unselected_pool",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed:2);
                uint seed=HarvestSmallSeedFor(TaskDegree.Success,HarvestModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed);var simulation=World(policy);
                HarvestCommit(simulation,HarvestBatchCommand(simulation,new[]{SharedHarvestFixture.CategoryRecordId}));
                var attempt=simulation.Capture().HarvestAttempts.Single();
                Require(attempt.Duration==new RuleTime(10*60)&&attempt.SelectedUnitIds.SequenceEqual(new[]{SharedHarvestFixture.UnitId}),
                    "One of two anatomy categories did not use half the full work time.");
                WorldAdvance(simulation,10*60);var state=simulation.Capture();
                Require(state.HarvestUnits.Single(x=>x.Id==SharedHarvestFixture.UnitId).Status==HarvestUnitStatus.Extracted
                    &&state.HarvestUnits.Where(x=>x.Id==SharedHarvestFixture.UnitId2||x.Id==SharedHarvestFixture.RecoveryUnitId)
                        .All(x=>x.Status==HarvestUnitStatus.Forfeited),
                    "First positive labor did not permanently forfeit the unselected category allocation.");
            });

            cases.Add("harvest_schema42_one_category_attempts_every_allocated_unit_with_one_check",()=>{
                var fixture=new SharedHarvestFixture(smallFinitePool:true,singleCategoryMultipleUnits:true);
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(fixture,seed:2);
                uint seed=HarvestSmallSeedFor(TaskDegree.Success,HarvestModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithHarvest(fixture,seed);var simulation=World(policy);
                HarvestCommit(simulation,HarvestBatchCommand(simulation,new[]{SharedHarvestFixture.CategoryRecordId},
                    criticalPreference:SharedHarvestFixture.RecoveryUnitId));
                var attempt=simulation.Capture().HarvestAttempts.Single();
                Require(attempt.Duration==new RuleTime(20*60)&&attempt.SelectedUnitIds.Length==3,
                    "A selected category with multiple anatomy units was split into separate attempts or mis-timed.");
                WorldAdvance(simulation,20*60);var state=simulation.Capture();
                Require(state.HarvestAttempts.Length==1&&state.HarvestAttempts[0].Status==HarvestAttemptStatus.Success
                    &&state.HarvestUnits.Count(x=>x.Status==HarvestUnitStatus.Extracted)==2,
                    "A category-level check did not settle every allocated intact unit together.");
            });

            cases.Add("harvest_schema42_failure_ruins_unique_highest_value_and_exhausts_other_selected_tissue",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed:2);
                uint seed=HarvestSmallSeedFor(TaskDegree.Failure,HarvestModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed);var simulation=World(policy);
                HarvestCommit(simulation,HarvestBatchCommand(simulation,new[]{SharedHarvestFixture.CategoryRecordId,SharedHarvestFixture.CategoryRecordId2}));
                WorldAdvance(simulation,20*60);var state=simulation.Capture();
                Require(state.HarvestUnits.Single(x=>x.Id==SharedHarvestFixture.UnitId2).Status==HarvestUnitStatus.Ruined
                    &&state.HarvestUnits.Single(x=>x.Id==SharedHarvestFixture.UnitId).Status==HarvestUnitStatus.Exhausted
                    &&!state.Work.Lots.Any(x=>x.Id==SharedHarvestFixture.UnitId||x.Id==SharedHarvestFixture.UnitId2),
                    "Failure did not ruin only the uniquely highest-value selected unit and exhaust the remaining claimed allocation.");
            });

            cases.Add("harvest_schema42_tied_failure_requires_and_records_player_choice",()=>{
                var fixture=new SharedHarvestFixture(smallFinitePool:true,equalFailureValues:true);
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(fixture,seed:2);
                uint seed=HarvestSmallSeedFor(TaskDegree.Failure,HarvestModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithHarvest(fixture,seed);var simulation=World(policy);var before=simulation.Capture();
                RejectUnchanged(simulation,host,HarvestBatchCommand(simulation,new[]{SharedHarvestFixture.CategoryRecordId,SharedHarvestFixture.CategoryRecordId2}),
                    "HarvestFailureTieChoiceRequired");
                Require(new SnapshotCodec().Encode(before).SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "Missing tied-value victim choice changed clock, RNG, or selection state.");
                HarvestCommit(simulation,HarvestBatchCommand(simulation,new[]{SharedHarvestFixture.CategoryRecordId,SharedHarvestFixture.CategoryRecordId2},
                    failurePreference:SharedHarvestFixture.UnitId));
                WorldAdvance(simulation,20*60);var state=simulation.Capture();
                Require(state.HarvestUnits.Single(x=>x.Id==SharedHarvestFixture.UnitId).Status==HarvestUnitStatus.Ruined
                    &&state.HarvestAttempts.Single().FailureVictimPreference==SharedHarvestFixture.UnitId,
                    "The selected tied highest-value failure victim was not honored and persisted.");
            });

            cases.Add("harvest_schema42_unknown_failure_values_reject_before_work",()=>{
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true,unknownFailureValues:true),seed:2);
                var simulation=World(policy);var before=simulation.Capture();
                RejectUnchanged(simulation,host,HarvestBatchCommand(simulation,
                    new[]{SharedHarvestFixture.CategoryRecordId,SharedHarvestFixture.CategoryRecordId2}),"HarvestFailureValueUnranked");
                Require(new SnapshotCodec().Encode(before).SequenceEqual(new SnapshotCodec().Encode(simulation.Capture())),
                    "Unrankable unknown values were not rejected before labor and RNG.");
            });

            cases.Add("harvest_schema42_critical_success_recovers_one_selected_damaged_unit",()=>{
                var unseeded=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed:2);
                uint seed=HarvestSmallSeedFor(TaskDegree.CriticalSuccess,HarvestModifier(unseeded.Initial()));
                var policy=TestOnlySharedWorldPolicy.WithHarvest(new SharedHarvestFixture(smallFinitePool:true),seed);var simulation=World(policy);
                HarvestCommit(simulation,HarvestBatchCommand(simulation,new[]{SharedHarvestFixture.CategoryRecordId2},
                    criticalPreference:SharedHarvestFixture.RecoveryUnitId));
                WorldAdvance(simulation,10*60);var state=simulation.Capture();
                Require(state.HarvestAttempts.Single().Status==HarvestAttemptStatus.CriticalSuccess
                    &&state.HarvestUnits.Single(x=>x.Id==SharedHarvestFixture.UnitId2).Status==HarvestUnitStatus.Extracted
                    &&state.HarvestUnits.Single(x=>x.Id==SharedHarvestFixture.RecoveryUnitId).Status==HarvestUnitStatus.Extracted
                    &&state.FishingCreatures.Single().MassPounds==RuleQuantity.FromFraction(1,2),
                    "Critical success did not add exactly one preselected eligible damaged unit to the baseline extraction.");
            });
        }
    }
}
#endif
