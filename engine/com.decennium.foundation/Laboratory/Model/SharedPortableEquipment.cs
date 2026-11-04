#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private readonly PortableKitFixture portableKit;
        private static bool PortableCommand(CommandKind kind)=>kind==CommandKind.HandlePortableEquipment||kind==CommandKind.EquipPortableItem
            ||kind==CommandKind.RemovePortableItem||kind==CommandKind.OpenPortableContainer||kind==CommandKind.ClosePortableContainer;
        private void InitializePortableEquipment(Snapshot s)
        {
            if(portableKit==null)return;
            PortableEquipmentRules.Initialize(s);
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
        private string ResolvePortableEquipment(Snapshot s,Command c)
        {
            if(portableKit==null)return "PortableEquipmentNotSelected";
            bool transfer=c.Kind==CommandKind.HandlePortableEquipment;
            if(transfer!=(c.Inventory!=null)||c.Combat!=null||c.X!=0||c.Y!=0)return "InvalidPortableRequest";
            if(transfer&&c.Inventory.Amount!=new RuleQuantity(1))return "PortableItemsAreIndivisible";
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==c.Target);if(item==null)return "UnknownPortableItem";
            if(!PortableEquipmentRules.Accessible(s,c.Actor,item))return "PortableItemOutOfReach";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(!CapableWorker(s,c.Actor))return "WorkerCannotPerformTask";
            if(AvailableHands(s,c.Actor)<1)return "HandlingHandRequired";
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
                            if(item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Carried||to!=PortableKitFixture.Pack)
                                return "InvalidPortableStow";
                            var pack=s.PortableEquipment.Single(x=>x.Id==to);
                            if(!PortableEquipmentRules.Accessible(s,c.Actor,pack)||!pack.Open)return "PortableContainerOutOfReach";
                            if(!PortableEquipmentValidation.FitsAuthoredMember(s,pack,item))return "ContainerFitNotEstablished";
                            if(PortableEquipmentRules.HasPendingClaim(s,item))return "PortableItemHasPendingWork";
                            after=PortablePlacement.Contained;break;
                        case HandlingKind.Handover:
                            operation=PortableOperation.Handover;recipient=c.Inventory.Destination;
                            if(item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Carried||recipient==c.Actor
                                ||!s.Actors.Any(a=>a.Id==recipient)||!NearPortable(s.Actors.Single(a=>a.Id==c.Actor),s.Actors.Single(a=>a.Id==recipient)))return "InvalidPortableHandover";
                            if(AvailableHands(s,recipient)<1||OrdinaryInventory.Busy(s,recipient))return "RecipientHandsUnavailable";
                            if(s.WorldTraversals.Any(x=>x.ActorId==recipient))return "RecipientTraversalInProgress";
                            if(PortableEquipmentRules.HasPendingClaim(s,item))return "PortableItemHasPendingWork";
                            after=PortablePlacement.Carried;break;
                        default:return "InvalidPortableHandling";
                    }
                    break;
                case CommandKind.EquipPortableItem:
                    operation=PortableOperation.Wear;
                    if(c.Inventory!=null||!item.Wearable||item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Carried)return "CannotWearPortableItem";
                    after=PortablePlacement.Worn;break;
                case CommandKind.RemovePortableItem:
                    operation=PortableOperation.Remove;
                    if(c.Inventory!=null||!item.Wearable||item.ParentId!=""||item.CustodianId!=c.Actor||item.Placement!=PortablePlacement.Worn)return "PortableItemNotWorn";
                    after=PortablePlacement.Carried;break;
                case CommandKind.OpenPortableContainer:
                    operation=PortableOperation.Open;
                    if(c.Inventory!=null||!item.CapacityPounds.HasValue||item.Open)return "PortableContainerCannotOpen";
                    break;
                case CommandKind.ClosePortableContainer:
                    operation=PortableOperation.Close;
                    if(c.Inventory!=null||!item.CapacityPounds.HasValue||!item.Open)return "PortableContainerNotOpen";
                    if(PortableEquipmentRules.HasPendingClaim(s,item))return "PortableItemHasPendingWork";
                    break;
                default:return "PortableEquipmentNotImplemented";
            }
            if((operation==PortableOperation.Pickup||operation==PortableOperation.Drop||operation==PortableOperation.Retrieve||operation==PortableOperation.Stow
                ||operation==PortableOperation.Handover||operation==PortableOperation.Remove||operation==PortableOperation.Close)
                &&PortableEquipmentRules.HasPendingClaim(s,item))return "PortableItemHasPendingWork";
            Snapshot projected=s.Copy();var projectedItem=projected.PortableEquipment.Single(x=>x.Id==item.Id);
            bool ground=after==PortablePlacement.Ground;
            string newCustodian=operation==PortableOperation.Handover?recipient
                :operation==PortableOperation.Pickup||operation==PortableOperation.Retrieve?c.Actor:projectedItem.CustodianId;
            string newParent=operation==PortableOperation.Stow?to
                :operation==PortableOperation.Retrieve||operation==PortableOperation.Pickup||operation==PortableOperation.Drop||operation==PortableOperation.Handover?"":projectedItem.ParentId;
            var changed=projectedItem.With(custodianId:newCustodian,
                parentId:newParent,placement:after,open:operation==PortableOperation.Open?true:operation==PortableOperation.Close?false:null,
                groundX:ground?projected.Actors.Single(x=>x.Id==c.Actor).X:0,groundY:ground?projected.Actors.Single(x=>x.Id==c.Actor).Y:0);
            SetPortable(projected,changed);
            if(newCustodian!=item.CustodianId)foreach(var child in PortableEquipmentRules.Descendants(projected,item.Id))SetPortable(projected,child.With(custodianId:newCustodian));
            PortableEquipmentRules.SynchronizeLinks(projected);
            string projectionError=CheckPortableProjectedState(projected);if(projectionError!=null)return projectionError;
            bool tactical=s.InventoryCombat;
            RuleTime operationStart=s.RuleClock;
            if(tactical) {
                if(connectedCombat==null||s.Encounter==null||s.Encounter.CurrentActor!=c.Actor||PendingCalendarChoice(s))return "TacticalChoicePending";
                var interval=Interval(s,c.Actor);
                if(interval.Interactions!=s.InventoryInteractions||interval.Interactions>=2)return "InteractionBudgetUnavailable";
                if(interval.Interactions==1&&interval.ActionSpent)return "ActionAlreadySpent";
                if(interval.Interactions==1&&!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
                var spent=interval.SpendInteraction();SetInterval(s,spent);s.InventoryInteractions=spent.Interactions;
            } else {
                RuleTime start=s.RuleClock,end=start.AddSeconds(1);
                var condition=NextConditionDeadline(s);if(condition.HasValue&&condition.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var formula=NextFormulaBoundary(s);if(formula.HasValue&&formula.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var dying=NextDyingMarker(s);if(dying.HasValue&&dying.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var remedy=NextRemedyBoundary(s);if(remedy.HasValue&&remedy.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var repairBoundary=NextRepairBoundary(s);if(repairBoundary.HasValue&&repairBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                var manufacturingBoundary=NextManufacturingBoundary(s);if(manufacturingBoundary.HasValue&&manufacturingBoundary.Value<=end)return "TimedHandlingBoundaryUnsupported";
                string id=OrdinaryInventory.Identity(s,"portable");
                s.Work=s.Work.Reserve(id,new[]{new WorkerInterval(id+".labor",id,c.Actor,start,end)},Array.Empty<ResourceReservation>());
                AdvanceTo(s,end,initiating:c);
            }
            // The action and any shared-time work finish before physical custody changes.
            item=s.PortableEquipment.Single(x=>x.Id==c.Target);
            newParent=operation==PortableOperation.Stow?to
                :operation==PortableOperation.Retrieve||operation==PortableOperation.Pickup||operation==PortableOperation.Drop||operation==PortableOperation.Handover?"":item.ParentId;
            changed=item.With(custodianId:newCustodian,
                parentId:newParent,placement:after,open:operation==PortableOperation.Open?true:operation==PortableOperation.Close?false:null,
                groundX:ground?s.Actors.Single(x=>x.Id==c.Actor).X:0,groundY:ground?s.Actors.Single(x=>x.Id==c.Actor).Y:0);
            SetPortable(s,changed);
            if(newCustodian!=item.CustodianId)foreach(var child in PortableEquipmentRules.Descendants(s,item.Id))SetPortable(s,child.With(custodianId:newCustodian));
            PortableEquipmentRules.SynchronizeLinks(s);
            string eventId=OrdinaryInventory.Identity(s,"portable");
            var record=new PortableHandlingRecord(eventId,s.Revision+1,c.Actor,item.Id,from,operation==PortableOperation.Stow?to:"",recipient,
                operation,before,after,operationStart,s.RuleClock,tactical);
            s.PortableHandling=s.PortableHandling.Concat(new[]{record}).ToArray();
            return null;
        }
    }
}
#endif
