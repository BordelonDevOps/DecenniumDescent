#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private PortableKitFixture portableKit;
        private static bool PortableCommand(CommandKind kind)=>kind==CommandKind.HandlePortableEquipment||kind==CommandKind.EquipPortableItem
            ||kind==CommandKind.RemovePortableItem||kind==CommandKind.DoffPortableShield||kind==CommandKind.OpenPortableContainer||kind==CommandKind.ClosePortableContainer;
        private void InitializePortableEquipment(Snapshot s)
        {
            if(portableKit==null)return;
            PortableEquipmentRules.Initialize(s);
        }
        private static void InitializeSoldierPortableEquipment(Snapshot s)
        {
            if(s.SchemaVersion<Snapshot.SoldierInitialBuildSchema||s.PortableEquipment.Length!=0)
                throw new ArgumentException("Soldier starting equipment requires a clean schema28 physical-equipment ledger.");
            string actor=TestOnlyPolicy.ActorId;RuleQuantity Q(long value)=>new RuleQuantity(value);
            const string fitRule=SoldierInitialEquipmentIds.PackFitRule;
            var fitMembers=new[]{SoldierInitialEquipmentIds.Rations,SoldierInitialEquipmentIds.Waterskin,SoldierInitialEquipmentIds.Water,
                SoldierInitialEquipmentIds.Pitons,SoldierInitialEquipmentIds.Tinderbox};
            var rations=SoldierInitialEquipmentIds.Rations;var skin=SoldierInitialEquipmentIds.Waterskin;var water=SoldierInitialEquipmentIds.Water;
            var replacedStock=new[]{TestOnlyInventoryPolicy.FoodId,TestOnlyInventoryPolicy.WaterId};
            bool inheritedActorSkin=s.Vessels.Any(x=>x.Id==TestOnlyFillingPolicy.ActorSkinId&&x.OwnerId==actor&&x.CustodianId==actor)
                &&s.VesselContents.Count(x=>x.VesselId==TestOnlyFillingPolicy.ActorSkinId&&x.LotId==TestOnlyInventoryPolicy.WaterId)==1;
            if(s.Work.Reservations.Any(x=>replacedStock.Contains(x.LotId))
                ||s.InventoryLots.Any(x=>x.ParentId!=""&&replacedStock.Contains(x.ParentId))
                ||s.VesselContents.Any(x=>replacedStock.Contains(x.LotId)
                    &&!(x.LotId==TestOnlyInventoryPolicy.WaterId&&x.VesselId==TestOnlyFillingPolicy.ActorSkinId))
                ||s.VesselContents.Any(x=>x.VesselId==TestOnlyFillingPolicy.ActorSkinId&&x.LotId!=TestOnlyInventoryPolicy.WaterId)
                ||s.WaterFills.Any(x=>x.SourceLotId==TestOnlyInventoryPolicy.WaterId||x.DestinationId==TestOnlyFillingPolicy.ActorSkinId)
                ||s.VesselMoves.Any(x=>x.VesselId==TestOnlyFillingPolicy.ActorSkinId))
                throw new ArgumentException("Soldier starter stores cannot replace stock with active descendants, reservations or vessel assignments.");
            if(!inheritedActorSkin)throw new ArgumentException("Soldier starter stores require the inherited, unmodified actor waterskin fixture.");
            s.Work=new WorkLedger(s.Work.Lots.Where(x=>!replacedStock.Contains(x.Id)).Concat(new[]{
                new ResourceLot(rations,TestOnlyInventoryPolicy.FoodUnit,Q(20),SoldierInitialEquipmentIds.Pack,actor),
                new ResourceLot(water,TestOnlyInventoryPolicy.WaterUnit,Q(4),skin,actor)
            }),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Where(x=>!replacedStock.Contains(x.LotId)).Concat(new[]{
                new InventoryLotRecord(rations,"",actor,Q(20),s.RuleClock,NutritionKind.FoodPounds,new RuleTime(2592000),InventoryAccess.Stowed),
                new InventoryLotRecord(water,"",actor,Q(4),s.RuleClock,NutritionKind.WaterPints,null,InventoryAccess.Stowed)
            }).ToArray();
            s.Vessels=s.Vessels.Where(x=>x.Id!=TestOnlyFillingPolicy.ActorSkinId)
                .Concat(new[]{new WaterVesselRecord(skin,WaterVesselProfile.Waterskin,actor,SoldierInitialEquipmentIds.Pack,actor)}).ToArray();
            s.VesselContents=s.VesselContents.Where(x=>x.VesselId!=TestOnlyFillingPolicy.ActorSkinId&&!replacedStock.Contains(x.LotId))
                .Concat(new[]{new VesselContentRecord(water,skin)}).ToArray();
            PortableEquipmentRecord Fixed(string id,string profile,string parent,PortablePlacement placement,long weight)
                =>FixedQ(id,profile,parent,placement,Q(weight));
            PortableEquipmentRecord FixedQ(string id,string profile,string parent,PortablePlacement placement,RuleQuantity weight)
                =>new PortableEquipmentRecord(id,profile,actor,actor,parent,placement,PortableLinkKind.None,"",PortableMassBasis.Fixed,weight,weight);
            var items=new[]{
                new PortableEquipmentRecord(SoldierInitialEquipmentIds.ChainMail,"armor-and-shields.chain-mail",actor,actor,"",PortablePlacement.Worn,
                    PortableLinkKind.None,"",PortableMassBasis.Fixed,Q(55),Q(55),wearable:true),
                new PortableEquipmentRecord(SoldierInitialEquipmentIds.Shield,"armor-and-shields.shield",actor,actor,"",PortablePlacement.Worn,
                    PortableLinkKind.None,"",PortableMassBasis.Fixed,Q(6),Q(6),wearable:true),
                Fixed(SoldierInitialEquipmentIds.Dagger,"simple-melee-weapons.dagger","",PortablePlacement.Carried,1),
                new PortableEquipmentRecord(SoldierInitialEquipmentIds.Pack,"adventuring-gear.backpack",actor,actor,"",PortablePlacement.Ground,
                    PortableLinkKind.None,"",PortableMassBasis.Fixed,Q(5),Q(5),capacityPounds:Q(30),capacityCubicFeet:Q(1),
                    wearable:true,open:true,fitRuleId:fitRule,fitMemberIds:fitMembers,groundX:0,groundY:0),
                new PortableEquipmentRecord(rations,"adventuring-gear.rations-1-day",actor,actor,SoldierInitialEquipmentIds.Pack,
                    PortablePlacement.Contained,PortableLinkKind.InventoryLot,rations,PortableMassBasis.FoodPounds,Q(20),null),
                new PortableEquipmentRecord(skin,"adventuring-gear.waterskin",actor,actor,SoldierInitialEquipmentIds.Pack,
                    PortablePlacement.Contained,PortableLinkKind.WaterVessel,skin,PortableMassBasis.Fixed,Q(5),Q(1)),
                new PortableEquipmentRecord(water,"prototype.potable-water.pint",actor,actor,skin,PortablePlacement.Contained,
                    PortableLinkKind.InventoryLot,water,PortableMassBasis.WaterPints,Q(4),null),
                Fixed(SoldierInitialEquipmentIds.Tinderbox,"adventuring-gear.tinderbox",SoldierInitialEquipmentIds.Pack,PortablePlacement.Contained,1),
                FixedQ(SoldierInitialEquipmentIds.Pitons,"adventuring-gear.piton",SoldierInitialEquipmentIds.Pack,PortablePlacement.Contained,Q(5).Scale(1,2)),
                Fixed(SoldierInitialEquipmentIds.Crowbar,"adventuring-gear.crowbar",SoldierInitialEquipmentIds.Pack,PortablePlacement.Attached,5),
                Fixed(SoldierInitialEquipmentIds.Hammer,"adventuring-gear.hammer",SoldierInitialEquipmentIds.Pack,PortablePlacement.Attached,3),
                Fixed(SoldierInitialEquipmentIds.Torches,"adventuring-gear.torch",SoldierInitialEquipmentIds.Pack,PortablePlacement.Attached,10),
                Fixed(SoldierInitialEquipmentIds.Rope,"adventuring-gear.rope-hempen-50-feet",SoldierInitialEquipmentIds.Pack,PortablePlacement.Attached,10)
            };
            s.PortableEquipment=items.Concat(new[]{new PortableEquipmentRecord(TestOnlyFillingPolicy.CompanionSkinId,"adventuring-gear.waterskin",
                TestOnlyPolicy.CompanionId,TestOnlyPolicy.CompanionId,"",PortablePlacement.Carried,PortableLinkKind.WaterVessel,
                TestOnlyFillingPolicy.CompanionSkinId,PortableMassBasis.Fixed,Q(5),Q(1))}).ToArray();
        }
        private static void SetPortable(Snapshot s,PortableEquipmentRecord value)
            =>s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static bool NearPortable(ActorState a,ActorState b)=>Math.Abs((long)a.X-b.X)+Math.Abs((long)a.Y-b.Y)<=1;
        private static string PendingPackOrItem(Snapshot s,PortableEquipmentRecord item)
        {
            if(PortableEquipmentRules.HasPendingClaim(s,item))return "PortableItemHasPendingWork";
            return null;
        }
        private static string CheckPortableProjectedState(Snapshot projected)
        {
            try {
                PortableEquipmentValidation.Validate(projected);
                PortableEquipmentRules.ValidateFixture(projected);
                if(projected.Actors.Any(a=>!PortableEquipmentRules.FitsCarrier(projected,a.Id)))return "CarryingCapacityExceeded";
                return null;
            } catch(ArgumentException ex) {
                if(ex.Message.Contains("fit",StringComparison.OrdinalIgnoreCase))return "ContainerFitNotEstablished";
                if(ex.Message.Contains("capacity",StringComparison.OrdinalIgnoreCase))return "ContainerCapacityExceeded";
                return "InvalidPortableTransition";
            }
        }
        private string AssessPortableShieldDoff(Snapshot s,Command c,out PortableEquipmentRecord shield,out RepeatingCrossbowRecord crossbow)
        {
            shield=null;crossbow=null;
            if(s.SchemaVersion<Snapshot.SoldierInitialBuildSchema)return "FeatureRequiresSchema28";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.X!=0||c.Y!=0)return "InvalidPortableRequest";
            if(!s.InventoryCombat||connectedCombat==null||s.Encounter==null)return "ShieldDoffRequiresTacticalCombat";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Actor!=s.Encounter.CurrentActor)return "WrongRegularTurn";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(!CapableWorker(s,c.Actor)||!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(s.WorldTraversals.Any(x=>x.ActorId==c.Actor))return "TraversalRequiresStationaryInteraction";
            var build=s.InitialCharacterLoadouts.SingleOrDefault(x=>x.ActorId==c.Actor);
            if(build==null||c.Target!=build.ShieldId)return "ShieldDoffUnavailable";
            shield=s.PortableEquipment.SingleOrDefault(x=>x.Id==build.ShieldId);
            if(shield==null||shield.ProfileId!="armor-and-shields.shield"||!shield.Wearable||shield.CustodianId!=c.Actor
                ||shield.ParentId!=""||shield.Placement!=PortablePlacement.Worn||shield.HeldHands!=0)return "ShieldNotWorn";
            if(!CharacterAdvancementRules.ShieldTrainedCrossbowException(s,c.Actor))return "ShieldTrainedRequired";
            crossbow=s.RepeatingCrossbows.SingleOrDefault(x=>x.Id==build.CrossbowId);
            if(crossbow==null||crossbow.HeldBy!=c.Actor||crossbow.CustodianId!=c.Actor||crossbow.GripHands!=2
                ||!s.Lives.Single(x=>x.ActorId==c.Actor).HeldItems.Contains(crossbow.Id))return "CrossbowMustBeHeldTwoHanded";
            var interval=Interval(s,c.Actor);
            if(interval.Interactions!=s.InventoryInteractions)return "TacticalInteractionLedgerMismatch";
            if(interval.ActionSpent)return "ActionAlreadySpent";
            return null;
        }
        private string ResolvePortableEquipment(Snapshot s,Command c)
        {
            if(portableKit==null&&soldierCharacterBuild==null&&harvestFixture==null&&ordinaryReceptacles==null&&huntingTrapFixture==null)return "PortableEquipmentNotSelected";
            bool transfer=c.Kind==CommandKind.HandlePortableEquipment;
            if(transfer!=(c.Inventory!=null)||c.Combat!=null||c.X!=0||c.Y!=0)return "InvalidPortableRequest";
            if(transfer&&c.Inventory.Amount!=new RuleQuantity(1))return "PortableItemsAreIndivisible";
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==c.Target);if(item==null)return "UnknownPortableItem";
            bool vial = item.LinkKind == PortableLinkKind.AlchemyDose;
            bool selectedStow = vial && s.ConnectedStowedVial && transfer && c.Inventory.Handling == HandlingKind.Stow
                && c.Inventory.Destination == ConnectedVialRules.PackId && item.Placement == PortablePlacement.Carried
                && item.CustodianId == c.Actor && item.HeldHands == 1;
            bool selectedRetrieve = vial && s.ConnectedStowedVial && transfer && c.Inventory.Handling == HandlingKind.Retrieve
                && item.ParentId == ConnectedVialRules.PackId && item.Placement == PortablePlacement.Contained;
            if (vial && (s.InventoryCombat || c.Actor != ConnectedVialRules.CarrierId || !transfer
                || (c.Inventory.Handling != HandlingKind.Pickup && !selectedStow && !selectedRetrieve)))
                return "ConnectedVialHandlingUnsupported";
            if (s.ConnectedStowedVial && item.Id == ConnectedVialRules.PackId
                && s.PortableEquipment.Any(x => x.LinkKind == PortableLinkKind.AlchemyDose && x.ParentId == item.Id)
                && (s.InventoryCombat || c.Kind != CommandKind.OpenPortableContainer && c.Kind != CommandKind.ClosePortableContainer))
                return "ConnectedVialPackHandlingUnsupported";
            bool installedCampStorageRoot=portableStorageFixture!=null
                &&item.Id==TestOnlyExpeditionCampConstructionFixture.PackLotId
                &&s.TemporaryCampInstallations.Any(x=>x.LotId==item.Id&&x.Kind==TemporaryCampFixtureKind.FittingPack);
            if(huntingTrapFixture?.Find(item.Id)!=null&&s.HuntingTrapDeployments.Any(x=>x.TrapItemId==item.Id)
                ||huntingTrapFixture?.Find(item.Id)!=null&&s.HuntingTrapActions.Any(x=>x.TrapItemId==item.Id&&x.Status==HuntingTrapActionStatus.Working))
                return "HuntingTrapDeviceInUse";
            if(!PortableEquipmentRules.Accessible(s,c.Actor,item))return "PortableItemOutOfReach";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(!CapableWorker(s,c.Actor))return "WorkerCannotPerformTask";
            bool doffShield=c.Kind==CommandKind.DoffPortableShield;
            bool dropsHeldItem=transfer&&c.Inventory.Handling==HandlingKind.Drop&&item.HeldHands>0;
            if(AvailableHands(s,c.Actor)<1&&!doffShield&&!dropsHeldItem&&!selectedStow)return "HandlingHandRequired";
            if(s.WorldTraversals.Any(x=>x.ActorId==c.Actor))return "TraversalRequiresStationaryInteraction";
            var before=item.Placement;string from=item.ParentId,to="",recipient="";var after=before;PortableOperation operation;
            switch(c.Kind) {
                case CommandKind.HandlePortableEquipment:
                    switch(c.Inventory.Handling) {
                        case HandlingKind.Pickup:
                            operation=PortableOperation.Pickup;
                            if(c.Inventory.Destination!=""||item.ParentId!=""||item.Placement!=PortablePlacement.Ground)return "InvalidPortablePickup";
                            after=PortablePlacement.Carried;break;
                        case HandlingKind.Drop:
                            operation=PortableOperation.Drop;
                            if(c.Inventory.Destination!=""||item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Carried)
                                return item.Placement==PortablePlacement.Worn?"RemoveWornContainerFirst":"InvalidPortableDrop";
                            after=PortablePlacement.Ground;break;
                        case HandlingKind.Retrieve:
                            operation=PortableOperation.Retrieve;
                            if(c.Inventory.Destination!=""||item.ParentId==""||(item.Placement!=PortablePlacement.Contained&&item.Placement!=PortablePlacement.Attached))return "InvalidPortableRetrieval";
                            if(PortableEquipmentRules.HasPendingClaim(s,item))return "PortableItemHasPendingWork";
                            after=PortablePlacement.Carried;to="";break;
                        case HandlingKind.Stow:
                            operation=PortableOperation.Stow;to=c.Inventory.Destination;
                            if(item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Carried
                                ||to==""||!s.PortableEquipment.Any(x=>x.Id==to))
                                return "InvalidPortableStow";
                            var pack=s.PortableEquipment.Single(x=>x.Id==to);
                            if(!PortableEquipmentRules.Accessible(s,c.Actor,pack)||!pack.Open)return "PortableContainerOutOfReach";
                            var destinationProfile=PortableStorageProfileValidation.Find(s,pack.ProfileId);
                            if(destinationProfile!=null&&destinationProfile.AllowedContainedProfileIds.Count!=0) {
                                string destinationFailure=PortableStorageProfileValidation.StorageDestinationFailure(s,pack,item);
                                if(destinationFailure!=null)return destinationFailure;
                            } else if(!PortableEquipmentValidation.FitsAuthoredMember(s,pack,item))return "ContainerFitNotEstablished";
                            if(PortableEquipmentRules.HasPendingClaim(s,item))return "PortableItemHasPendingWork";
                            after=PortablePlacement.Contained;break;
                        case HandlingKind.Handover:
                            operation=PortableOperation.Handover;recipient=c.Inventory.Destination;
                            if(item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Carried||recipient==c.Actor
                                ||!s.Actors.Any(a=>a.Id==recipient)||!NearPortable(s.Actors.Single(a=>a.Id==c.Actor),s.Actors.Single(a=>a.Id==recipient)))return "InvalidPortableHandover";
                            if(AvailableHands(s,recipient)<1||OrdinaryInventory.Busy(s,recipient))return "RecipientHandsUnavailable";
                            if(s.WorldTraversals.Any(x=>x.ActorId==recipient))return "RecipientTraversalInProgress";
                            if(PortableEquipmentRules.HasPendingClaim(s,item,installedCampStorageRoot))return "PortableItemHasPendingWork";
                            after=PortablePlacement.Carried;break;
                        default:return "InvalidPortableHandling";
                    }
                    break;
                case CommandKind.EquipPortableItem:
                    // The source assigns ten minutes to don heavy armor and an Action to don a
                    // shield. This narrow handler only implements ordinary one-second handling;
                    // do not route distinct donning procedures through that cost.
                    if(soldierCharacterBuild!=null)return "EquipmentDonDoffProcedureUnsupported";
                    operation=PortableOperation.Wear;
                    if(c.Inventory!=null||!item.Wearable||item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Carried)return "CannotWearPortableItem";
                    after=PortablePlacement.Worn;break;
                case CommandKind.RemovePortableItem:
                    if(soldierCharacterBuild!=null)return "EquipmentDonDoffProcedureUnsupported";
                    operation=PortableOperation.Remove;
                    if(c.Inventory!=null||!item.Wearable||item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Worn)return "PortableItemNotWorn";
                    after=PortablePlacement.Carried;break;
                case CommandKind.DoffPortableShield:
                    operation=PortableOperation.ShieldDoff;
                    string doffFailure=AssessPortableShieldDoff(s,c,out _,out _);
                    if(doffFailure!=null)return doffFailure;
                    if(item.Id!=c.Target)return "ShieldDoffUnavailable";
                    after=PortablePlacement.Carried;break;
                case CommandKind.OpenPortableContainer:
                    operation=PortableOperation.Open;
                    if(c.Inventory!=null||!item.CapacityPounds.HasValue||item.Open)return "PortableContainerCannotOpen";
                    if(s.OrdinaryReceptacleLocks.Any(x=>x.ContainerId==item.Id&&x.Locked))return "PortableContainerLocked";
                    break;
                case CommandKind.ClosePortableContainer:
                    operation=PortableOperation.Close;
                    if(c.Inventory!=null||!item.CapacityPounds.HasValue||!item.Open)return "PortableContainerNotOpen";
                    break;
                default:return "PortableEquipmentNotImplemented";
            }
            bool physicalMove=operation==PortableOperation.Pickup||operation==PortableOperation.Drop||operation==PortableOperation.Retrieve
                ||operation==PortableOperation.Stow||operation==PortableOperation.Handover||operation==PortableOperation.Remove;
            if((physicalMove||operation==PortableOperation.Close)
                &&PortableEquipmentRules.HasPendingClaim(s,item,installedCampStorageRoot&&(physicalMove||operation==PortableOperation.Close)))
                return "PortableItemHasPendingWork";
            if(installedCampStorageRoot&&physicalMove)return "InstalledTemporaryCampCannotMove";
            Snapshot projected=s.Copy();var projectedItem=projected.PortableEquipment.Single(x=>x.Id==item.Id);
            bool ground=after==PortablePlacement.Ground;
            bool stationaryProfileAccess=(operation==PortableOperation.Open||operation==PortableOperation.Close)
                &&PortableStorageProfileValidation.Find(s,item.ProfileId)!=null;
            string newCustodian=operation==PortableOperation.Handover?recipient
                :operation==PortableOperation.Stow?projected.PortableEquipment.Single(x=>x.Id==to).CustodianId
                :operation==PortableOperation.Pickup||operation==PortableOperation.Retrieve?c.Actor:projectedItem.CustodianId;
            string newParent=operation==PortableOperation.Stow?to
                :operation==PortableOperation.Retrieve||operation==PortableOperation.Pickup||operation==PortableOperation.Drop||operation==PortableOperation.Handover?"":projectedItem.ParentId;
            var changed=projectedItem.With(custodianId:newCustodian,
                parentId:newParent,placement:after,open:operation==PortableOperation.Open?true:operation==PortableOperation.Close?false:null,
                groundX:ground?(stationaryProfileAccess?projectedItem.GroundX:projected.Actors.Single(x=>x.Id==c.Actor).X):0,
                groundY:ground?(stationaryProfileAccess?projectedItem.GroundY:projected.Actors.Single(x=>x.Id==c.Actor).Y):0,
                heldHands:after==PortablePlacement.Carried?(operation==PortableOperation.ShieldDoff||vial?1:projectedItem.HeldHands):0);
            SetPortable(projected,changed);
            if(operation==PortableOperation.ShieldDoff) {
                var loadout=projected.InitialCharacterLoadouts.Single(x=>x.ActorId==c.Actor);
                projected.RepeatingCrossbows=projected.RepeatingCrossbows.Select(x=>x.Id==loadout.CrossbowId?x.WithGrip(1):x).ToArray();
            }
            if(newCustodian!=item.CustodianId)foreach(var child in PortableEquipmentRules.Descendants(projected,item.Id))SetPortable(projected,child.With(custodianId:newCustodian));
            SynchronizeMiningToolStructureLocation(projected,projected.PortableEquipment.Single(x=>x.Id==item.Id));
            PortableEquipmentRules.SynchronizeLinks(projected);
            string projectionError=CheckPortableProjectedState(projected);if(projectionError!=null)return projectionError;
            bool tactical=s.InventoryCombat;
            RuleTime operationStart=s.RuleClock;
            if(tactical) {
                if(operation==PortableOperation.ShieldDoff) {
                    var interval=Interval(s,c.Actor);
                    SetInterval(s,interval.PayAction());
                } else {
                if(connectedCombat==null||s.Encounter==null||s.Encounter.CurrentActor!=c.Actor||PendingCalendarChoice(s))return "TacticalChoicePending";
                var interval=Interval(s,c.Actor);
                if(interval.Interactions!=s.InventoryInteractions||interval.Interactions>=2)return "InteractionBudgetUnavailable";
                if(interval.Interactions==1&&interval.ActionSpent)return "ActionAlreadySpent";
                if(interval.Interactions==1&&!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
                var spent=interval.SpendInteraction();SetInterval(s,spent);s.InventoryInteractions=spent.Interactions;
                }
            } else {
                RuleTime start=s.RuleClock,end=start.AddSeconds(1);
                var condition=NextConditionDeadline(s);if(condition.HasValue&&condition.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var formula=NextFormulaBoundary(s);if(formula.HasValue&&formula.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var dying=NextDyingMarker(s);if(dying.HasValue&&dying.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var remedy=NextRemedyBoundary(s);if(remedy.HasValue&&remedy.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var repairBoundary=NextRepairBoundary(s);if(repairBoundary.HasValue&&repairBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var manufacturingBoundary=NextManufacturingBoundary(s);if(manufacturingBoundary.HasValue&&manufacturingBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var recipe347Boundary=NextRecipe347Boundary(s);if(recipe347Boundary.HasValue&&recipe347Boundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var pressureBoundary=NextExpeditionPressureBoundary(s);if(pressureBoundary.HasValue&&pressureBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                string id=OrdinaryInventory.Identity(s,"portable");
                s.Work=s.Work.Reserve(id,new[]{new WorkerInterval(id+".labor",id,c.Actor,start,end)},Array.Empty<ResourceReservation>());
                string timeFailure=AdvanceTo(s,end,initiating:c);if(timeFailure!=null)return timeFailure;
            }
            // The action and any shared-time work finish before physical custody changes.
            item=s.PortableEquipment.Single(x=>x.Id==c.Target);
            newParent=operation==PortableOperation.Stow?to
                :operation==PortableOperation.Retrieve||operation==PortableOperation.Pickup||operation==PortableOperation.Drop||operation==PortableOperation.Handover?"":item.ParentId;
            changed=item.With(custodianId:newCustodian,
                parentId:newParent,placement:after,open:operation==PortableOperation.Open?true:operation==PortableOperation.Close?false:null,
                groundX:ground?(stationaryProfileAccess?item.GroundX:s.Actors.Single(x=>x.Id==c.Actor).X):0,
                groundY:ground?(stationaryProfileAccess?item.GroundY:s.Actors.Single(x=>x.Id==c.Actor).Y):0,
                heldHands:after==PortablePlacement.Carried?(operation==PortableOperation.ShieldDoff||vial?1:item.HeldHands):0);
            SetPortable(s,changed);
            if(operation==PortableOperation.ShieldDoff) {
                var loadout=s.InitialCharacterLoadouts.Single(x=>x.ActorId==c.Actor);
                s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==loadout.CrossbowId?x.WithGrip(1):x).ToArray();
            }
            if(newCustodian!=item.CustodianId)foreach(var child in PortableEquipmentRules.Descendants(s,item.Id))SetPortable(s,child.With(custodianId:newCustodian));
            SynchronizeMiningToolStructureLocation(s,s.PortableEquipment.Single(x=>x.Id==item.Id));
            PortableEquipmentRules.SynchronizeLinks(s);
            string eventId=OrdinaryInventory.Identity(s,"portable");
            var record=new PortableHandlingRecord(eventId,s.Revision+1,c.Actor,item.Id,from,operation==PortableOperation.Stow?to:"",recipient,
                operation,before,after,operationStart,s.RuleClock,tactical);
            s.PortableHandling=s.PortableHandling.Concat(new[]{record}).ToArray();
            return null;
        }

        private void SynchronizeMiningToolStructureLocation(Snapshot s,PortableEquipmentRecord item)
        {
            if(s.SchemaVersion<Snapshot.MiningToolCandidateSchema)return;
            var profiles=s.MiningToolCandidateProfiles.Where(x=>x.ToolItemId==item.Id).ToArray();
            var structureIds=profiles.Select(x=>x.StructureId).ToList();
            if(recipe347Fixture!=null) {
                if(item.Id==TestOnlyRecipe347Fixture.BodyItemId)structureIds.Add(TestOnlyRecipe347Fixture.BodyStructureId);
                if(item.Id==TestOnlyRecipe347Fixture.MiningToolsItemId)structureIds.Add(TestOnlyRecipe347Fixture.MiningToolsStructureId);
                if(item.Id==TestOnlyRecipe347Fixture.AssayKitId)structureIds.Add(TestOnlyRecipe347Fixture.AssayKitStructureId);
            }
            structureIds=structureIds.Distinct(StringComparer.Ordinal).ToList();
            if(structureIds.Count==0)return;
            string location;
            if(item.Placement==PortablePlacement.Ground) {
                var deposit=s.MiningDeposits.SingleOrDefault(x=>x.SiteX==item.GroundX&&x.SiteY==item.GroundY
                    &&profiles.Any(p=>p.DepositId==x.Id));
                location=deposit?.SiteId??"ground."+item.GroundX.ToString(CultureInfo.InvariantCulture)
                    +"."+item.GroundY.ToString(CultureInfo.InvariantCulture);
            } else location=item.ParentId!=""?item.ParentId:item.CustodianId;
            foreach(string structureId in structureIds) {
                var structure=s.Structures.SingleOrDefault(x=>x.Id==structureId);
                if(structure!=null&&(structure.LocationId!=location||structure.CustodianId!=item.CustodianId))
                    s.Structures=s.Structures.Select(x=>x.Id==structureId?x.WithLocationAndCustodian(location,item.CustodianId):x).ToArray();
            }
        }
    }
}
#endif
