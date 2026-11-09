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
        private static string StartStorageFill(Simulation simulation,RuleQuantity amount,string destination)
        {
            var state=simulation.Capture();
            var command=new Command("mgt01.fill."+(state.Revision+1).ToString(System.Globalization.CultureInfo.InvariantCulture),
                TestOnlyPolicy.CompanionId,state.Revision,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,
                inventory:new InventoryRequest(amount,destination));
            var result=simulation.Execute(TestOnlySharedWorldPolicy.Host(),command);
            Require(result.Outcome==Outcome.Committed,"MGT-01 water fill did not start: "+result.Code);
            return simulation.Capture().WaterFills.Single(x=>x.StartedAt==state.RuleClock&&x.WorkerId==TestOnlyPolicy.CompanionId
                &&x.DestinationId==destination&&x.Status==WaterFillStatus.Working).Id;
        }

        private static void ResolveStorageCheckpointCombat(Simulation simulation)
        {
            WorldCommit(simulation,IC(simulation,CommandKind.BeginFixedEncounter));
            var encounter=simulation.Capture();
            Require(encounter.InventoryCombat&&encounter.RouteTravels.Single().Status==ExpeditionRouteTravelStatus.Paused,
                "Exploration checkpoint did not transfer into the existing tactical encounter authority.");
            for(int skipped=0;simulation.Capture().Encounter.CurrentActor!=TestOnlyPolicy.ActorId;skipped++) {
                Require(skipped<encounter.Encounter.Order.Count,"Tactical initiative did not reach the exploring character.");
                ConnectedEnd(simulation);
            }
            // The active pressure cohort deliberately restricts its explorer's tactical movement.
            // Use the established pressure combat trace: the hostile approaches and attacks, then
            // the explorer resolves the encounter from the preserved route checkpoint.
            PressureMoveHostileAdjacent(simulation);
            DefeatConnectedEnemy(simulation);
            WorldCommit(simulation,Tac(simulation,CommandKind.EndFixedEncounter));
            Require(!simulation.Capture().InventoryCombat
                &&simulation.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).X==1
                &&simulation.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId).Y==3,
                "Combat exit did not return the explorer to the saved camp checkpoint.");
        }

        private static void FinishStorageCamp(Simulation simulation)
        {
            for(int attempt=0;attempt<20&&!TemporaryCampConstructionValidation.HasTemporaryCamp(simulation.Capture(),PressureCampId);attempt++) {
                CampConstructionCommit(simulation,CommandKind.StartTemporaryCampConstruction,PressureCampId,"mgt01.start."+attempt);
                WorldAdvance(simulation,checked((int)TestOnlyExpeditionCampConstructionFixture.RequiredWorkSeconds));
            }
            Require(TemporaryCampConstructionValidation.HasTemporaryCamp(simulation.Capture(),PressureCampId),
                "The bounded deterministic camp construction attempts did not install the storage root.");
        }

        private static Snapshot AddContainedTestItems(Snapshot source,int count,RuleQuantity pounds,RuleQuantity? printedLoad)
        {
            var copy=source.Copy();
            var root=copy.PortableEquipment.Single(x=>x.Id==TestOnlyExpeditionCampConstructionFixture.PackLotId);
            var additions=Enumerable.Range(0,count).Select(i=>new PortableEquipmentRecord(
                "TEST_ONLY.capacity-item-"+i.ToString(System.Globalization.CultureInfo.InvariantCulture),
                "adventuring-gear.waterskin",TestOnlyPolicy.ActorId,root.CustodianId,root.Id,PortablePlacement.Contained,
                PortableLinkKind.None,"",PortableMassBasis.Fixed,pounds,pounds,printedLoad));
            copy.PortableEquipment=copy.PortableEquipment.Concat(additions).ToArray();
            return copy;
        }

        private static PortableEquipmentRecord[] PortableStorageDescendants(Snapshot snapshot,string rootId)
        {
            var found=new List<PortableEquipmentRecord>();var pending=new Queue<string>();pending.Enqueue(rootId);
            while(pending.Count!=0) {
                string parent=pending.Dequeue();
                foreach(var child in snapshot.PortableEquipment.Where(x=>x.ParentId==parent)) {
                    found.Add(child);pending.Enqueue(child.Id);
                }
            }
            return found.ToArray();
        }

        private static void AddPortableStorageCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("mgt01_portable_storage_connected_loop_save_restore_capacity_and_rejections",()=>{
                var seed=CampConstructionSeed(success:true);
                var simulation=CampConstructionAtCheckpoint(seed,storage:true);
                ResolveStorageCheckpointCombat(simulation);
                string foodLot=CampConstructionPrepareCompanionFood(simulation,new RuleQuantity(2));
                var foodBefore=simulation.Capture().InventoryLots.Single(x=>x.LotId==foodLot);
                Require(simulation.Capture().Work.Lots.Single(x=>x.Id==foodLot).Amount==new RuleQuantity(2)
                    &&foodBefore.OwnerId==TestOnlyPolicy.ActorId&&foodBefore.FreshUntil.HasValue,
                    "The cache path did not supply the real, fresh, owner-bound two-pound food lot.");

                // A live water-fill claim protects its physical vessel and descendant tree.
                string fullSkin=TestOnlyFillingPolicy.CompanionSkinId;
                var openCamp=Portable(simulation,CommandKind.OpenPortableContainer,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId);
                PortableCommit(simulation,openCamp);
                string fill=StartStorageFill(simulation,new RuleQuantity(4),fullSkin);
                var dropDuringFill=Portable(simulation,CommandKind.HandlePortableEquipment,fullSkin,
                    handling:HandlingKind.Drop,actor:TestOnlyPolicy.CompanionId);
                RejectUnchanged(simulation,host,dropDuringFill,"WorkerBusy");
                WorldAdvance(simulation,60);
                var filled=simulation.Capture();
                var waterLot=filled.VesselContents.Single(x=>x.VesselId==fullSkin).LotId;
                Require(filled.WaterFills.Single(x=>x.Id==fill).Status==WaterFillStatus.Complete
                    &&filled.Work.Lots.Single(x=>x.Id==waterLot).Amount==new RuleQuantity(4)
                    &&filled.PortableEquipment.Single(x=>x.Id==fullSkin).SourceWeightLb==new RuleQuantity(1),
                    "A four-pint physical waterskin did not preserve its one-pound tare plus actual water contents.");

                // Open is a distinct ordinary handling operation; capacity does not exist as storage until install.
                var beforeUninstalled=Bytes(simulation);
                var earlyStow=Portable(simulation,CommandKind.HandlePortableEquipment,foodLot,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId,HandlingKind.Stow,TestOnlyPolicy.CompanionId);
                var earlyQuery=simulation.QueryCommand(host,earlyStow);
                Require(earlyQuery.Supported&&!earlyQuery.Admissible&&earlyQuery.Code=="TemporaryCampStorageNotInstalled"
                    &&beforeUninstalled.SequenceEqual(Bytes(simulation)),
                    "The fitting pack accepted storage before a successful Temporary Camp installation.");
                var closeBeforeBuild=Portable(simulation,CommandKind.ClosePortableContainer,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId);
                PortableCommit(simulation,closeBeforeBuild);
                FinishStorageCamp(simulation);
                var installed=simulation.Capture();
                Require(TemporaryCampConstructionValidation.StorageCapacity(installed,PressureCampId).Load==20
                    &&installed.TemporaryCampInstallations.Any(x=>x.LotId==TestOnlyExpeditionCampConstructionFixture.PackLotId),
                    "Camp storage was not derived from the actual installed fitting-pack claim.");

                // Independent exact capacity checks: exact Load succeeds; weight, Load, and volume fail separately.
                var exactLoad=AddContainedTestItems(installed,1,new RuleQuantity(1),new RuleQuantity(20));
                PortableEquipmentValidation.Validate(exactLoad);
                Throws<ArgumentException>(()=>PortableEquipmentValidation.Validate(
                    AddContainedTestItems(installed,1,new RuleQuantity(201),new RuleQuantity(20))));
                Throws<ArgumentException>(()=>PortableEquipmentValidation.Validate(
                    AddContainedTestItems(installed,1,new RuleQuantity(1),new RuleQuantity(201,10))));
                PortableEquipmentValidation.Validate(AddContainedTestItems(installed,100,new RuleQuantity(1),default));
                Throws<ArgumentException>(()=>PortableEquipmentValidation.Validate(
                    AddContainedTestItems(installed,101,new RuleQuantity(1),default)));
                var cycle=installed.Copy();
                var rations=cycle.PortableEquipment.Single(x=>x.Id==PortableKitFixture.Rations);
                var selfContained=new PortableEquipmentRecord(rations.Id,rations.ProfileId,rations.OwnerId,rations.CustodianId,
                    rations.Id,PortablePlacement.Contained,rations.LinkKind,rations.LinkedId,rations.MassBasis,
                    rations.SourceWeightLb,rations.OperationalWeightLb,rations.PrintedLoad,new RuleQuantity(1),new RuleQuantity(1),
                    rations.Wearable,rations.Open,rations.FitRuleId,rations.FitMemberIds.ToArray(),rations.GroundX,rations.GroundY,rations.HeldHands);
                cycle.PortableEquipment=cycle.PortableEquipment.Select(x=>x.Id==rations.Id?selfContained:x).ToArray();
                cycle.Work=new WorkLedger(cycle.Work.Lots.Select(x=>x.Id==rations.LinkedId
                    ?new ResourceLot(x.Id,x.UnitId,x.Amount,rations.Id,x.CustodianId):x),cycle.Work.WorkerIntervals,cycle.Work.Reservations);
                Throws<ArgumentException>(()=>PortableEquipmentValidation.Validate(cycle));

                // Closed and out-of-reach checks happen before any transfer or clock debit.
                var closedStow=Portable(simulation,CommandKind.HandlePortableEquipment,foodLot,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId,HandlingKind.Stow,TestOnlyPolicy.CompanionId);
                RejectUnchanged(simulation,host,closedStow,"PortableContainerOutOfReach");
                var openAfterInstall=Portable(simulation,CommandKind.OpenPortableContainer,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId);
                var openQuery=simulation.QueryCommand(host,openAfterInstall);
                Require(openQuery.Supported&&openQuery.Admissible,"Installed camp storage could not be opened separately.");
                PortableCommit(simulation,openAfterInstall);
                var skinStow=Portable(simulation,CommandKind.HandlePortableEquipment,fullSkin,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId,HandlingKind.Stow,TestOnlyPolicy.CompanionId);
                var skinQuery=simulation.QueryCommand(host,skinStow);
                Require(skinQuery.Supported&&skinQuery.Admissible,"The camp pack did not admit its authored full waterskin profile.");
                PortableCommit(simulation,skinStow);
                var incompatible=Portable(simulation,CommandKind.HandlePortableEquipment,PortableKitFixture.MessKit,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId,HandlingKind.Stow);
                RejectUnchanged(simulation,host,incompatible,"ContainerFitNotEstablished");
                // Portion the actual acquired food, then use the same profile resolver for camp and ordinary crate.
                var portionCommand=new Command("mgt01.food.portion",TestOnlyPolicy.CompanionId,simulation.Capture().Revision,
                    CommandKind.PortionInventory,foodLot,inventory:new InventoryRequest(new RuleQuantity(1),handling:HandlingKind.Pickup));
                WorldCommit(simulation,portionCommand);
                var portion=simulation.Capture().InventoryLots.Single(x=>x.ParentId==foodLot);
                var primaryStow=Portable(simulation,CommandKind.HandlePortableEquipment,foodLot,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId,HandlingKind.Stow,TestOnlyPolicy.CompanionId);
                var primaryQuery=simulation.QueryCommand(host,primaryStow);
                Require(primaryQuery.Supported&&primaryQuery.Admissible&&primaryQuery.Costs.Count==1
                    &&primaryQuery.Costs[0].Kind=="work-seconds"&&primaryQuery.Costs[0].Amount==1,
                    "Portable destination query and ordinary handling cost did not admit the same compatible camp deposit.");
                byte[] beforeStow=Bytes(simulation);
                PortableCommit(simulation,primaryStow);
                var portionStow=Portable(simulation,CommandKind.HandlePortableEquipment,portion.LotId,
                    TestOnlyExpeditionCampConstructionFixture.PackLotId,HandlingKind.Stow,TestOnlyPolicy.CompanionId);
                var portionQuery=simulation.QueryCommand(host,portionStow);
                Require(portionQuery.Supported&&portionQuery.Admissible,
                    "A same-profile food portion was rejected by the camp destination assessment.");
                PortableCommit(simulation,portionStow);
                var stored=simulation.Capture();
                var campContents=stored.PortableEquipment.Where(x=>x.ParentId==TestOnlyExpeditionCampConstructionFixture.PackLotId
                    &&x.Placement==PortablePlacement.Contained).ToArray();
                var campPounds=RuleQuantity.Sum(campContents.Select(x=>PortableEquipmentValidation.Mass(stored,x))
                    .Concat(campContents.SelectMany(x=>PortableStorageDescendants(stored,x.Id))
                        .Select(x=>PortableEquipmentValidation.Mass(stored,x))));
                var campLoad=RuleQuantity.Sum(campContents.Select(x=>PortableStorageProfileValidation.Load(stored,x))
                    .Concat(campContents.SelectMany(x=>PortableStorageDescendants(stored,x.Id))
                        .Select(x=>PortableStorageProfileValidation.Load(stored,x))));
                Require(campPounds==new RuleQuantity(7)&&campLoad==new RuleQuantity(7,10)
                    &&PortableStorageProfileValidation.ContentsVolume(stored,stored.PortableEquipment.Single(
                        x=>x.Id==TestOnlyExpeditionCampConstructionFixture.PackLotId))
                        ==new RuleQuantity(22,100),
                    "Two pounds of food plus a full one-pound-tare/four-pound-water skin did not count as seven pounds and 0.7 Load exactly once: "
                    +campPounds+" lb, "+campLoad+" Load, "+PortableStorageProfileValidation.ContentsVolume(stored,stored.PortableEquipment.Single(
                        x=>x.Id==TestOnlyExpeditionCampConstructionFixture.PackLotId))+" ft3; direct="
                    +string.Join(",",campContents.Select(x=>x.Id+"="+PortableEquipmentValidation.Mass(stored,x))));
                Require(stored.PortableEquipment.Single(x=>x.Id==fullSkin).ParentId==TestOnlyExpeditionCampConstructionFixture.PackLotId
                    &&stored.PortableEquipment.Single(x=>x.Id==fullSkin).CustodianId==TestOnlyPolicy.ActorId
                    &&stored.PortableEquipment.Single(x=>x.Id==fullSkin).OwnerId==TestOnlyPolicy.CompanionId
                    &&stored.Vessels.Single(x=>x.Id==fullSkin).LocationId==TestOnlyExpeditionCampConstructionFixture.PackLotId
                    &&stored.Vessels.Single(x=>x.Id==fullSkin).CustodianId==TestOnlyPolicy.ActorId
                    &&stored.Work.Lots.Single(x=>x.Id==waterLot).LocationId==fullSkin
                    &&stored.VesselContents.Any(x=>x.VesselId==fullSkin&&x.LotId==waterLot)
                    &&stored.InventoryLots.Single(x=>x.LotId==waterLot).CreatedAt==filled.InventoryLots.Single(x=>x.LotId==waterLot).CreatedAt
                    &&stored.InventoryLots.Single(x=>x.LotId==waterLot).OwnerId==filled.InventoryLots.Single(x=>x.LotId==waterLot).OwnerId
                    &&stored.InventoryLots.Single(x=>x.LotId==foodLot).FreshUntil==foodBefore.FreshUntil
                    &&stored.InventoryLots.Single(x=>x.LotId==foodLot).OwnerId==foodBefore.OwnerId,
                    "Deposit failed to preserve original ownership/freshness/provenance, vessel contents or synchronized physical links.");

                var foodInCamp=Portable(simulation,CommandKind.HandlePortableEquipment,portion.LotId,
                    handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId);
                PortableCommit(simulation,foodInCamp);
                var foodToCrate=Portable(simulation,CommandKind.HandlePortableEquipment,portion.LotId,
                    TestOnlyPortableStorageFixture.CrateId,HandlingKind.Stow,TestOnlyPolicy.ActorId);
                var crateQuery=simulation.QueryCommand(host,foodToCrate);
                Require(crateQuery.Supported&&crateQuery.Admissible,
                    "The ordinary portable crate did not use the shared destination assessment.");
                byte[] beforeCrateStow=Bytes(simulation);
                PortableCommit(simulation,foodToCrate);
                byte[] afterStow=Bytes(simulation);
                Require(simulation.Execute(host,foodToCrate).Outcome==Outcome.Duplicate
                    &&afterStow.SequenceEqual(Bytes(simulation))&&beforeCrateStow.SequenceEqual(afterStow)==false
                    &&simulation.Capture().PortableEquipment.Single(x=>x.Id==portion.LotId).ParentId==TestOnlyPortableStorageFixture.CrateId,
                    "Crate deposit was not an idempotent one-second physical custody transaction.");

                // Active companion work is independent of these nested goods and survives save/restore.
                WorldAdvance(simulation,6); // Roll into a fresh off-calendar activity interval after prior handling work.
                string activeFill=StartStorageFill(simulation,new RuleQuantity(1,2),TestOnlyFillingPolicy.FlaskId);
                var checkpoint=simulation.Capture();
                Require(checkpoint.WaterFills.Single(x=>x.Id==activeFill).Status==WaterFillStatus.Working
                    &&checkpoint.Work.Reservations.Any(x=>x.JobId==activeFill&&x.RemainingAmount==new RuleQuantity(1,2))
                    &&checkpoint.PortableEquipment.Any(x=>x.ParentId==TestOnlyExpeditionCampConstructionFixture.PackLotId)
                    &&checkpoint.PortableEquipment.Any(x=>x.ParentId==TestOnlyPortableStorageFixture.CrateId),
                    "The saved management checkpoint did not retain nested goods plus compatible companion work.");
                byte[] checkpointBytes=Bytes(simulation);
                Directory.CreateDirectory(directory);
                File.WriteAllBytes(Path.Combine(directory,"mgt01_portable_storage_nested_work_checkpoint.sav"),checkpointBytes);
                var left=new Simulation(CampConstructionPolicy(seed,storage:true),codec.Decode(checkpointBytes),ExecutionProfile.Laboratory);
                var right=new Simulation(CampConstructionPolicy(seed,storage:true),codec.Decode(checkpointBytes),ExecutionProfile.Laboratory);
                Require(checkpointBytes.SequenceEqual(Bytes(left))&&codec.Encode(codec.Decode(checkpointBytes)).SequenceEqual(checkpointBytes),
                    "Schema71 profile facts, nested goods and active work did not round-trip canonically.");

                // Compare an uninterrupted active-fill clock advance with a split, disk-restored advance.
                var wholeClock=new Simulation(CampConstructionPolicy(seed,storage:true),codec.Decode(checkpointBytes),ExecutionProfile.Laboratory);
                var splitClock=new Simulation(CampConstructionPolicy(seed,storage:true),codec.Decode(checkpointBytes),ExecutionProfile.Laboratory);
                WorldAdvance(wholeClock,60);
                WorldAdvance(splitClock,30);
                byte[] halfwayBytes=Bytes(splitClock);
                File.WriteAllBytes(Path.Combine(directory,"mgt01_split_fill_halfway.sav"),halfwayBytes);
                splitClock=new Simulation(CampConstructionPolicy(seed,storage:true),codec.Decode(halfwayBytes),ExecutionProfile.Laboratory);
                Require(halfwayBytes.SequenceEqual(Bytes(splitClock))
                    &&splitClock.Capture().WaterFills.Single(x=>x.Id==activeFill).Status==WaterFillStatus.Working
                    &&splitClock.Capture().WaterFills.Single(x=>x.Id==activeFill).Progress==new RuleTime(30)
                    &&splitClock.Capture().Work.Reservations.Any(x=>x.JobId==activeFill
                        &&x.RemainingAmount==new RuleQuantity(1,2)),
                    "The split water-fill save did not retain its exact half-work reservation and remainder.");
                WorldAdvance(splitClock,30);
                var wholeClockState=wholeClock.Capture();var splitClockState=splitClock.Capture();
                var wholeClockFill=wholeClockState.WaterFills.Single(x=>x.Id==activeFill);
                var splitClockFill=splitClockState.WaterFills.Single(x=>x.Id==activeFill);
                Require(wholeClockState.RuleClock==splitClockState.RuleClock
                    &&wholeClockState.RandomState==splitClockState.RandomState
                    &&wholeClockFill.Status==WaterFillStatus.Complete&&splitClockFill.Status==wholeClockFill.Status
                    &&splitClockFill.Progress==wholeClockFill.Progress&&splitClockFill.OutputLotId==wholeClockFill.OutputLotId
                    &&wholeClockState.Work.Lots.OrderBy(x=>x.Id,StringComparer.Ordinal).Select(x=>new {x.Id,x.Amount,x.LocationId,x.CustodianId})
                        .SequenceEqual(splitClockState.Work.Lots.OrderBy(x=>x.Id,StringComparer.Ordinal)
                            .Select(x=>new {x.Id,x.Amount,x.LocationId,x.CustodianId})),
                    "Uninterrupted and split/restored clock advancement changed active work, water settlement, or RNG state.");

                WorldAdvance(left,60);WorldAdvance(right,60);
                var leftSkin=Portable(left,CommandKind.HandlePortableEquipment,fullSkin,handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId);
                var rightSkin=Portable(right,CommandKind.HandlePortableEquipment,fullSkin,handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId);
                WorldCommit(left,leftSkin);WorldCommit(right,rightSkin);
                var leftHandover=Portable(left,CommandKind.HandlePortableEquipment,fullSkin,TestOnlyPolicy.CompanionId,
                    HandlingKind.Handover,TestOnlyPolicy.ActorId);
                var rightHandover=Portable(right,CommandKind.HandlePortableEquipment,fullSkin,TestOnlyPolicy.CompanionId,
                    HandlingKind.Handover,TestOnlyPolicy.ActorId);
                WorldCommit(left,leftHandover);WorldCommit(right,rightHandover);
                var leftFood=Portable(left,CommandKind.HandlePortableEquipment,foodLot,handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId);
                var rightFood=Portable(right,CommandKind.HandlePortableEquipment,foodLot,handling:HandlingKind.Retrieve,actor:TestOnlyPolicy.ActorId);
                WorldCommit(left,leftFood);WorldCommit(right,rightFood);
                WorldCommit(left,Portable(left,CommandKind.HandlePortableEquipment,foodLot,TestOnlyPolicy.CompanionId,
                    HandlingKind.Handover,TestOnlyPolicy.ActorId));
                WorldCommit(right,Portable(right,CommandKind.HandlePortableEquipment,foodLot,TestOnlyPolicy.CompanionId,
                    HandlingKind.Handover,TestOnlyPolicy.ActorId));
                var lf=left.Capture();
                Require(Bytes(left).SequenceEqual(Bytes(right))
                    &&lf.PortableEquipment.Single(x=>x.Id==fullSkin).CustodianId==TestOnlyPolicy.CompanionId
                    &&lf.PortableEquipment.Single(x=>x.Id==foodLot).CustodianId==TestOnlyPolicy.CompanionId
                    &&lf.PortableEquipment.Single(x=>x.Id==waterLot).CustodianId==TestOnlyPolicy.CompanionId
                    &&lf.Vessels.Single(x=>x.Id==fullSkin).LocationId==TestOnlyPolicy.CompanionId
                    &&lf.InventoryLots.Single(x=>x.LotId==waterLot).OwnerId==TestOnlyPolicy.CompanionId
                    &&lf.InventoryLots.Single(x=>x.LotId==foodLot).OwnerId==TestOnlyPolicy.ActorId,
                    "Restore/replay changed final custody, ownership or synchronized vessel/lot records.");

                foreach(var simulationCopy in new[]{left,right}) {
                    WorldAdvance(simulationCopy,6); // The companion begins a fresh ordinary work interval after the restore steps.
                    var eat=new Command("mgt01.intake.food",TestOnlyPolicy.CompanionId,simulationCopy.Capture().Revision,
                        CommandKind.StartIntake,foodLot,inventory:new InventoryRequest(new RuleQuantity(2,3)));
                    WorldCommit(simulationCopy,eat);WorldAdvance(simulationCopy,600);
                    var drink=new Command("mgt01.intake.water",TestOnlyPolicy.CompanionId,simulationCopy.Capture().Revision,
                        CommandKind.StartIntake,waterLot,inventory:new InventoryRequest(new RuleQuantity(1)));
                    WorldCommit(simulationCopy,drink);WorldAdvance(simulationCopy,60);
                    WorldAdvance(simulationCopy,6);
                    WorldStep(simulationCopy,0,-1,actor:TestOnlyPolicy.CompanionId);
                    WorldAdvance(simulationCopy,3,2);
                    Require(simulationCopy.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.CompanionId).X==2
                        &&simulationCopy.Capture().Actors.Single(x=>x.Id==TestOnlyPolicy.CompanionId).Y==2,
                        "The companion did not clear the mapped route cell after completing management work.");
                    var unreachableStow=Portable(simulationCopy,CommandKind.HandlePortableEquipment,foodLot,
                        TestOnlyExpeditionCampConstructionFixture.PackLotId,HandlingKind.Stow,TestOnlyPolicy.CompanionId);
                    RejectUnchanged(simulationCopy,host,unreachableStow,"PortableContainerOutOfReach");
                    WorldCommit(simulationCopy,RouteTravelCommand(simulationCopy,CommandKind.ResumeRouteTravel,"mgt01.route.continue"));
                    WorldAdvance(simulationCopy,10800);
                }
                var finalLeft=left.Capture();var finalRight=right.Capture();
                Require(Bytes(left).SequenceEqual(Bytes(right))
                    &&finalLeft.Intakes.Count(x=>x.Status==IntakeStatus.Complete)==2
                    &&finalLeft.RouteTravels.Single().Progress>checkpoint.RouteTravels.Single().Progress
                    &&finalLeft.Work.Lots.Single(x=>x.Id==waterLot).Amount==new RuleQuantity(3)
                    &&finalLeft.InventoryLots.Single(x=>x.LotId==foodLot).FreshUntil==foodBefore.FreshUntil
                    &&finalLeft.TemporaryCampInstallations.Any(x=>x.LotId==TestOnlyExpeditionCampConstructionFixture.PackLotId&&x.SiteId==PressureCampId)
                    &&finalRight.TemporaryCampInstallations.Any(x=>x.LotId==TestOnlyExpeditionCampConstructionFixture.PackLotId&&x.SiteId==PressureCampId),
                    "Identical restored histories diverged during real intake and route continuation: bytes="
                    +Bytes(left).SequenceEqual(Bytes(right))+", intakes="+finalLeft.Intakes.Count(x=>x.Status==IntakeStatus.Complete)
                    +", route="+finalLeft.RouteTravels.Single().Progress+">"+checkpoint.RouteTravels.Single().Progress
                    +", water="+finalLeft.Work.Lots.Single(x=>x.Id==waterLot).Amount+", freshness="
                    +(finalLeft.InventoryLots.Single(x=>x.LotId==foodLot).FreshUntil==foodBefore.FreshUntil)
                    +", installations="+finalLeft.TemporaryCampInstallations.Length+"/"+finalRight.TemporaryCampInstallations.Length);

                // The schema70 content profile remains independently loadable with its original fingerprint and layout.
                var historicalPolicy=CampConstructionPolicy(CampConstructionSeed(success:true));
                var historical=historicalPolicy.Initial();var historicalBytes=codec.Encode(historical);
                Require(historical.SchemaVersion==Snapshot.TemporaryCampConstructionSchema
                    &&historicalBytes.SequenceEqual(codec.Encode(codec.Decode(historicalBytes)))
                    &&Bytes(new Simulation(historicalPolicy,codec.Decode(historicalBytes),ExecutionProfile.Laboratory))
                        .SequenceEqual(historicalBytes),
                    "Adding schema71 changed historical schema70 save bytes or restore behavior.");
            });
        }
    }
}
#endif
