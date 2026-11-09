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

                // An adjacent companion can operate the stationary installed container without moving its anchor.
                var installedPack=installed.PortableEquipment.Single(x=>x.Id==TestOnlyExpeditionCampConstructionFixture.PackLotId);
                var companionPosition=installed.Actors.Single(x=>x.Id==TestOnlyPolicy.CompanionId);
                int anchoredX=installedPack.GroundX,anchoredY=installedPack.GroundY;
                Require(Math.Abs((long)companionPosition.X-anchoredX)+Math.Abs((long)companionPosition.Y-anchoredY)==1,
                    "The storage fixture no longer places its companion adjacent to the installed container.");
                var adjacentStorage=new Simulation(CampConstructionPolicy(seed,storage:true),codec.Decode(Bytes(simulation)),
                    ExecutionProfile.Laboratory);
                var adjacentOpen=Portable(adjacentStorage,CommandKind.OpenPortableContainer,installedPack.Id,actor:TestOnlyPolicy.CompanionId);
                var adjacentOpenQuery=adjacentStorage.QueryCommand(host,adjacentOpen);
                Require(adjacentOpenQuery.Supported&&adjacentOpenQuery.Admissible,
                    "An adjacent companion could not query opening the installed camp container.");
                PortableCommit(adjacentStorage,adjacentOpen);
                var adjacentOpened=adjacentStorage.Capture();
                var openedPack=adjacentOpened.PortableEquipment.Single(x=>x.Id==installedPack.Id);
                Require(openedPack.Open&&openedPack.GroundX==anchoredX&&openedPack.GroundY==anchoredY
                    &&PortableEquipmentValidation.GroundLocation(openedPack)==adjacentOpened.Work.Lots.Single(x=>x.Id==installedPack.Id).LocationId
                    &&adjacentOpened.TemporaryCampInstallations.Any(x=>x.LotId==installedPack.Id&&x.SiteId==PressureCampId),
                    "Adjacent schema71 Open relocated the installed container or desynchronized its anchored lot.");
                var adjacentClose=Portable(adjacentStorage,CommandKind.ClosePortableContainer,installedPack.Id,actor:TestOnlyPolicy.CompanionId);
                var adjacentCloseQuery=adjacentStorage.QueryCommand(host,adjacentClose);
                Require(adjacentCloseQuery.Supported&&adjacentCloseQuery.Admissible,
                    "An adjacent companion could not query closing the installed camp container.");
                PortableCommit(adjacentStorage,adjacentClose);
                var adjacentClosed=adjacentStorage.Capture();
                var closedPack=adjacentClosed.PortableEquipment.Single(x=>x.Id==installedPack.Id);
                Require(!closedPack.Open&&closedPack.GroundX==anchoredX&&closedPack.GroundY==anchoredY
                    &&PortableEquipmentValidation.GroundLocation(closedPack)==adjacentClosed.Work.Lots.Single(x=>x.Id==installedPack.Id).LocationId
                    &&adjacentClosed.TemporaryCampInstallations.Any(x=>x.LotId==installedPack.Id&&x.SiteId==PressureCampId),
                    "Adjacent schema71 Close relocated the installed container or desynchronized its anchored lot.");

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
                Require(skinQuery.Supported&&skinQuery.Admissible,"The camp pack did not admit its authored full waterskin profile: "+skinQuery.Code+".");
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

                // The TEST_ONLY crate remains an ordinary movable container: custody and ground placement are
                // mutable handling state, while its authored identity, mass, capacity and contents are preserved.
                byte[] crateStartBytes=Bytes(simulation);
                var cratePolicy=CampConstructionPolicy(seed,storage:true);
                var crateLeft=new Simulation(cratePolicy,codec.Decode(crateStartBytes),ExecutionProfile.Laboratory);
                var crateRight=new Simulation(cratePolicy,codec.Decode(crateStartBytes),ExecutionProfile.Laboratory);
                var crateStart=crateLeft.Capture();
                var crateItem=crateStart.PortableEquipment.Single(x=>x.Id==TestOnlyPortableStorageFixture.CrateId);
                var crateContents=PortableStorageDescendants(crateStart,crateItem.Id);
                var crateMass=RuleQuantity.Sum(new[]{PortableEquipmentValidation.Mass(crateStart,crateItem)}
                    .Concat(crateContents.Select(x=>PortableEquipmentValidation.Mass(crateStart,x))));
                var crateLoad=RuleQuantity.Sum(new[]{PortableStorageProfileValidation.Load(crateStart,crateItem)}
                    .Concat(crateContents.Select(x=>PortableStorageProfileValidation.Load(crateStart,x))));
                var actorBurdenBefore=PortableEquipmentRules.CarriedBurden(crateStart,TestOnlyPolicy.ActorId);
                var companionBurdenBefore=PortableEquipmentRules.CarriedBurden(crateStart,TestOnlyPolicy.CompanionId);
                Require(actorBurdenBefore.Pounds.HasValue&&actorBurdenBefore.Load.HasValue
                    &&companionBurdenBefore.Pounds.HasValue&&companionBurdenBefore.Load.HasValue,
                    "The admitted TEST_ONLY roster did not have known baseline carrying totals.");
                var cratePickup=Portable(crateLeft,CommandKind.HandlePortableEquipment,crateItem.Id,
                    handling:HandlingKind.Pickup,actor:TestOnlyPolicy.ActorId);
                var cratePickupQuery=crateLeft.QueryCommand(host,cratePickup);
                Require(cratePickupQuery.Supported&&cratePickupQuery.Admissible,
                    "The shared portable query rejected pickup of the admitted ordinary crate.");
                PortableCommit(crateLeft,cratePickup);
                var pickedCrate=crateLeft.Capture();
                var pickedRoot=pickedCrate.PortableEquipment.Single(x=>x.Id==crateItem.Id);
                var pickedContents=PortableStorageDescendants(pickedCrate,crateItem.Id);
                var actorBurdenWithCrate=PortableEquipmentRules.CarriedBurden(pickedCrate,TestOnlyPolicy.ActorId);
                Require(actorBurdenWithCrate.Pounds.HasValue&&actorBurdenWithCrate.Load.HasValue
                    &&pickedRoot.Placement==PortablePlacement.Carried&&pickedRoot.CustodianId==TestOnlyPolicy.ActorId
                    &&pickedContents.Length==crateContents.Length&&pickedContents.All(x=>x.CustodianId==TestOnlyPolicy.ActorId)
                    &&pickedContents.All(x=>crateContents.Single(y=>y.Id==x.Id).OwnerId==x.OwnerId)
                    &&actorBurdenWithCrate.Pounds.Value==RuleQuantity.Sum(new[]{actorBurdenBefore.Pounds.Value,crateMass})
                    &&actorBurdenWithCrate.Load.Value==RuleQuantity.Sum(new[]{actorBurdenBefore.Load.Value,crateLoad}),
                    "Crate pickup changed its contents/ownership or failed to add the whole nested burden exactly once.");
                var crateHandover=Portable(crateLeft,CommandKind.HandlePortableEquipment,crateItem.Id,
                    TestOnlyPolicy.CompanionId,HandlingKind.Handover,TestOnlyPolicy.ActorId);
                var crateHandoverQuery=crateLeft.QueryCommand(host,crateHandover);
                Require(crateHandoverQuery.Supported&&crateHandoverQuery.Admissible,
                    "The shared portable query rejected handover of the carried crate to the adjacent companion.");
                PortableCommit(crateLeft,crateHandover);
                var handoverState=crateLeft.Capture();
                var handedRoot=handoverState.PortableEquipment.Single(x=>x.Id==crateItem.Id);
                var handedContents=PortableStorageDescendants(handoverState,crateItem.Id);
                var companionBurdenWithCrate=PortableEquipmentRules.CarriedBurden(handoverState,TestOnlyPolicy.CompanionId);
                var actorBurdenAfterHandover=PortableEquipmentRules.CarriedBurden(handoverState,TestOnlyPolicy.ActorId);
                Require(companionBurdenWithCrate.Pounds.HasValue&&companionBurdenWithCrate.Load.HasValue
                    &&actorBurdenAfterHandover.Pounds==actorBurdenBefore.Pounds&&actorBurdenAfterHandover.Load==actorBurdenBefore.Load
                    &&handedRoot.Placement==PortablePlacement.Carried&&handedRoot.CustodianId==TestOnlyPolicy.CompanionId
                    &&handedRoot.OwnerId==crateItem.OwnerId&&handedContents.All(x=>x.CustodianId==TestOnlyPolicy.CompanionId)
                    &&handedContents.All(x=>crateContents.Single(y=>y.Id==x.Id).OwnerId==x.OwnerId)
                    &&companionBurdenWithCrate.Pounds.Value==RuleQuantity.Sum(new[]{companionBurdenBefore.Pounds.Value,crateMass})
                    &&companionBurdenWithCrate.Load.Value==RuleQuantity.Sum(new[]{companionBurdenBefore.Load.Value,crateLoad}),
                    "Crate handover lost custody/ownership/contents or failed to transfer the nested carrying burden.");
                Directory.CreateDirectory(directory);
                byte[] crateHandoverBytes=Bytes(crateLeft);
                File.WriteAllBytes(Path.Combine(directory,"mgt01_crate_handover_checkpoint.sav"),crateHandoverBytes);
                crateLeft=new Simulation(cratePolicy,codec.Decode(crateHandoverBytes),ExecutionProfile.Laboratory);
                crateRight=new Simulation(cratePolicy,codec.Decode(crateHandoverBytes),ExecutionProfile.Laboratory);
                Require(crateHandoverBytes.SequenceEqual(Bytes(crateLeft))&&crateHandoverBytes.SequenceEqual(Bytes(crateRight))
                    &&codec.Encode(codec.Decode(crateHandoverBytes)).SequenceEqual(crateHandoverBytes),
                    "The handed-over crate and its nested contents did not survive canonical save/restore.");
                var crateDropLeft=Portable(crateLeft,CommandKind.HandlePortableEquipment,crateItem.Id,
                    handling:HandlingKind.Drop,actor:TestOnlyPolicy.CompanionId);
                var crateDropRight=Portable(crateRight,CommandKind.HandlePortableEquipment,crateItem.Id,
                    handling:HandlingKind.Drop,actor:TestOnlyPolicy.CompanionId);
                var crateDropQuery=crateLeft.QueryCommand(host,crateDropLeft);
                Require(crateDropQuery.Supported&&crateDropQuery.Admissible,
                    "The shared portable query rejected dropping the restored crate.");
                Require(crateRight.QueryCommand(host,crateDropRight).Admissible,
                    "An identical restored crate branch disagreed about drop admissibility.");
                PortableCommit(crateLeft,crateDropLeft);PortableCommit(crateRight,crateDropRight);
                var droppedCrate=crateLeft.Capture();
                var droppedRoot=droppedCrate.PortableEquipment.Single(x=>x.Id==crateItem.Id);
                var droppedContents=PortableStorageDescendants(droppedCrate,crateItem.Id);
                var companionBurdenAfterDrop=PortableEquipmentRules.CarriedBurden(droppedCrate,TestOnlyPolicy.CompanionId);
                Require(companionBurdenAfterDrop.Pounds==companionBurdenBefore.Pounds
                    &&companionBurdenAfterDrop.Load==companionBurdenBefore.Load
                    &&Bytes(crateLeft).SequenceEqual(Bytes(crateRight))&&droppedRoot.Placement==PortablePlacement.Ground
                    &&droppedRoot.CustodianId==TestOnlyPolicy.CompanionId&&droppedRoot.GroundX==companionPosition.X
                    &&droppedRoot.GroundY==companionPosition.Y&&droppedContents.Length==crateContents.Length
                    &&droppedContents.All(x=>x.ParentId==crateItem.Id&&x.CustodianId==TestOnlyPolicy.CompanionId)
                    &&droppedContents.All(x=>crateContents.Single(y=>y.Id==x.Id).OwnerId==x.OwnerId),
                    "Restored crate drop changed its nested goods/owner, position or deterministic carrying burden.");

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

                // Decode bytes retained in the accepted pre-storage schema70 tree, then continue the paused work
                // through two identical current-code restore branches. This proves actual historical compatibility.
                byte[] historicalBytes=PortableStorageHistoricalSchema70Fixture.Read();
                var historicalSnapshot=codec.Decode(historicalBytes);
                var historicalPolicy=CampConstructionPolicy(CampConstructionSeed(success:true));
                var historicalRestored=new Simulation(historicalPolicy,historicalSnapshot,ExecutionProfile.Laboratory);
                Require(historicalSnapshot.SchemaVersion==Snapshot.TemporaryCampConstructionSchema
                    &&historicalSnapshot.PortableStorageProfiles.Length==0
                    &&historicalBytes.SequenceEqual(codec.Encode(historicalSnapshot))
                    &&historicalBytes.SequenceEqual(Bytes(historicalRestored)),
                    "Authentic pre-MGT-01 schema70 bytes did not decode, re-encode and restore exactly.");
                Directory.CreateDirectory(directory);
                File.WriteAllBytes(Path.Combine(directory,"mgt01_schema70_pre_storage_source.sav"),historicalBytes);
                File.WriteAllBytes(Path.Combine(directory,"mgt01_schema70_current_reencoded.sav"),codec.Encode(historicalRestored.Capture()));
                var historicalLeft=new Simulation(historicalPolicy,codec.Decode(historicalBytes),ExecutionProfile.Laboratory);
                var historicalRight=new Simulation(historicalPolicy,codec.Decode(historicalBytes),ExecutionProfile.Laboratory);
                string historicalAttempt=historicalLeft.Capture().TemporaryCampConstructionAttempts.Single().Id;
                var historicalResume=CampConstructionCommand(historicalLeft,CommandKind.ResumeTemporaryCampConstruction,
                    historicalAttempt,"mgt01.schema70.resume");
                Require(historicalLeft.QueryCommand(host,historicalResume).Admissible,
                    "The current code could not query continuation of the authentic paused schema70 save.");
                WorldCommit(historicalLeft,historicalResume);
                WorldCommit(historicalRight,CampConstructionCommand(historicalRight,CommandKind.ResumeTemporaryCampConstruction,
                    historicalAttempt,"mgt01.schema70.resume"));
                WorldCommit(historicalLeft,IC(historicalLeft,CommandKind.AdvanceClock,x:14400,y:1,id:"mgt01.schema70.finish"));
                WorldCommit(historicalRight,IC(historicalRight,CommandKind.AdvanceClock,x:14400,y:1,id:"mgt01.schema70.finish"));
                var historicalContinued=historicalLeft.Capture();
                Require(Bytes(historicalLeft).SequenceEqual(Bytes(historicalRight))
                    &&historicalContinued.SchemaVersion==Snapshot.TemporaryCampConstructionSchema
                    &&historicalContinued.PortableStorageProfiles.Length==0
                    &&historicalContinued.TemporaryCampConstructionAttempts.Single().Status==TemporaryCampConstructionStatus.Resolved
                    &&TemporaryCampConstructionValidation.HasTemporaryCamp(historicalContinued,PressureCampId),
                    "The authentic schema70 save did not continue deterministically through camp installation under current code.");
                File.WriteAllBytes(Path.Combine(directory,"mgt01_schema70_current_continuation.sav"),Bytes(historicalLeft));
            });
        }
    }
}
#endif
