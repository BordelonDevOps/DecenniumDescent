using System;
using System.Linq;
using System.Collections.ObjectModel;

namespace Decennium.Foundation
{
    public enum PortablePlacement { Carried, Worn, Contained, Attached, Ground }
    public enum PortableLinkKind { None, InventoryLot, WaterVessel, SupplyEquipment }
    public enum PortableMassBasis { Fixed, FoodPounds, WaterPints }
    public enum PortableOperation { Pickup, Drop, Retrieve, Stow, Handover, Wear, Remove, Open, Close }

    /// <summary>One actual test-fixture item or quantity already tracked in another component.
    /// Weight estimates and container fit facts remain explicit and schema-versioned.</summary>
    public sealed class PortableEquipmentRecord
    {
        public string Id { get; }
        public string ProfileId { get; }
        public string OwnerId { get; }
        public string CustodianId { get; }
        public string ParentId { get; }
        public PortablePlacement Placement { get; }
        public PortableLinkKind LinkKind { get; }
        public string LinkedId { get; }
        public PortableMassBasis MassBasis { get; }
        public RuleQuantity? SourceWeightLb { get; }
        public RuleQuantity? OperationalWeightLb { get; }
        public RuleQuantity? PrintedLoad { get; }
        public RuleQuantity? CapacityPounds { get; }
        public RuleQuantity? CapacityCubicFeet { get; }
        public bool Wearable { get; }
        public bool Open { get; }
        public string FitRuleId { get; }
        private readonly string[] fitMemberIds;
        public ReadOnlyCollection<string> FitMemberIds { get; }
        public int GroundX { get; }
        public int GroundY { get; }

        public PortableEquipmentRecord(string id,string profileId,string ownerId,string custodianId,string parentId,
            PortablePlacement placement,PortableLinkKind linkKind,string linkedId,PortableMassBasis massBasis,
            RuleQuantity? sourceWeightLb,RuleQuantity? operationalWeightLb,RuleQuantity? printedLoad=null,
            RuleQuantity? capacityPounds=null,RuleQuantity? capacityCubicFeet=null,bool wearable=false,bool open=false,
            string fitRuleId="",string[] fitMemberIds=null,int groundX=0,int groundY=0)
        {
            var members=fitMemberIds??Array.Empty<string>();
            if(!Validation.ValidId(id)||!Validation.ValidId(profileId)||!Validation.ValidId(ownerId)||!Validation.ValidId(custodianId)
                ||parentId==null||(parentId!=""&&!Validation.ValidId(parentId))||!Enum.IsDefined(typeof(PortablePlacement),placement)
                ||!Enum.IsDefined(typeof(PortableLinkKind),linkKind)||!Enum.IsDefined(typeof(PortableMassBasis),massBasis)
                ||linkedId==null||(linkedId!=""&&!Validation.ValidId(linkedId))||((linkKind==PortableLinkKind.None)!=(linkedId==""))
                ||(linkKind==PortableLinkKind.InventoryLot)!=(massBasis==PortableMassBasis.FoodPounds||massBasis==PortableMassBasis.WaterPints)
                ||(massBasis==PortableMassBasis.Fixed)!=operationalWeightLb.HasValue
                ||(sourceWeightLb.HasValue&&sourceWeightLb.Value<default(RuleQuantity))||(operationalWeightLb.HasValue&&operationalWeightLb.Value<default(RuleQuantity))
                ||(printedLoad.HasValue&&printedLoad.Value<default(RuleQuantity))||(capacityPounds.HasValue&&capacityPounds.Value<default(RuleQuantity))
                ||(capacityCubicFeet.HasValue&&capacityCubicFeet.Value<default(RuleQuantity))||(capacityPounds.HasValue!=capacityCubicFeet.HasValue)
                ||(wearable&&placement!=PortablePlacement.Worn&&profileId!="adventuring-gear.backpack")
                ||(placement==PortablePlacement.Worn&&!wearable)
                ||((placement==PortablePlacement.Contained||placement==PortablePlacement.Attached)!=(parentId!=""))
                ||(placement==PortablePlacement.Ground?(groundX<0||groundY<0):(groundX!=0||groundY!=0))
                ||fitRuleId==null||(fitRuleId!=""&&!Validation.ValidId(fitRuleId))||members.Length>32
                ||members.Any(x=>!Validation.ValidId(x)||x==id)||members.Distinct(StringComparer.Ordinal).Count()!=members.Length
                ||((fitRuleId!="")!=(members.Length!=0))||open&&(capacityPounds==null))
                throw new ArgumentException("Invalid portable equipment record.");
            Id=id;ProfileId=profileId;OwnerId=ownerId;CustodianId=custodianId;ParentId=parentId;Placement=placement;
            LinkKind=linkKind;LinkedId=linkedId;MassBasis=massBasis;SourceWeightLb=sourceWeightLb;OperationalWeightLb=operationalWeightLb;
            PrintedLoad=printedLoad;CapacityPounds=capacityPounds;CapacityCubicFeet=capacityCubicFeet;Wearable=wearable;Open=open;
            FitRuleId=fitRuleId;this.fitMemberIds=members.ToArray();FitMemberIds=Array.AsReadOnly(this.fitMemberIds);GroundX=groundX;GroundY=groundY;
        }
        public PortableEquipmentRecord With(string custodianId=null,string parentId=null,PortablePlacement? placement=null,
            bool? open=null,int? groundX=null,int? groundY=null)
            =>new PortableEquipmentRecord(Id,ProfileId,OwnerId,custodianId??CustodianId,parentId??ParentId,placement??Placement,
                LinkKind,LinkedId,MassBasis,SourceWeightLb,OperationalWeightLb,PrintedLoad,CapacityPounds,CapacityCubicFeet,
                Wearable,open??Open,FitRuleId,fitMemberIds,groundX??GroundX,groundY??GroundY);
    }

    /// <summary>Append-only record of a completed ordinary handling or container operation.</summary>
    public sealed class PortableHandlingRecord
    {
        public string Id { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public string ItemId { get; }
        public string FromParentId { get; }
        public string ToParentId { get; }
        public string RecipientId { get; }
        public PortableOperation Operation { get; }
        public PortablePlacement Before { get; }
        public PortablePlacement After { get; }
        public RuleTime StartedAt { get; }
        public RuleTime EndedAt { get; }
        public bool Tactical { get; }
        public PortableHandlingRecord(string id,long revision,string actorId,string itemId,string fromParentId,string toParentId,
            string recipientId,PortableOperation operation,PortablePlacement before,PortablePlacement after,RuleTime startedAt,RuleTime endedAt,bool tactical)
        {
            if(!Validation.ValidId(id)||revision<1||!Validation.ValidId(actorId)||!Validation.ValidId(itemId)
                ||fromParentId==null||(fromParentId!=""&&!Validation.ValidId(fromParentId))
                ||toParentId==null||(toParentId!=""&&!Validation.ValidId(toParentId))
                ||recipientId==null||(recipientId!=""&&!Validation.ValidId(recipientId))
                ||!Enum.IsDefined(typeof(PortableOperation),operation)||!Enum.IsDefined(typeof(PortablePlacement),before)
                ||!Enum.IsDefined(typeof(PortablePlacement),after)||endedAt<startedAt)
                throw new ArgumentException("Invalid portable handling record.");
            Id=id;Revision=revision;ActorId=actorId;ItemId=itemId;FromParentId=fromParentId;ToParentId=toParentId;RecipientId=recipientId;
            Operation=operation;Before=before;After=after;StartedAt=startedAt;EndedAt=endedAt;Tactical=tactical;
        }
    }

    public static class PortableEquipmentValidation
    {
        public const int MaxItems=128,MaxHandling=256;
        public static void Validate(Snapshot s)
        {
            if(s.PortableEquipment==null||s.PortableHandling==null||s.PortableEquipment.Length>MaxItems||s.PortableHandling.Length>MaxHandling
                ||s.PortableEquipment.Any(x=>x==null)||s.PortableHandling.Any(x=>x==null))throw new ArgumentException("Invalid portable equipment collections.");
            if(s.SchemaVersion<Snapshot.PortableEquipmentSchema) {
                if(s.PortableEquipment.Length!=0||s.PortableHandling.Length!=0)throw new ArgumentException("Portable equipment requires schema20.");
                return;
            }
            var items=s.PortableEquipment;
            if(items.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=items.Length
                ||items.Where(x=>x.LinkKind!=PortableLinkKind.None).Select(x=>x.LinkedId).Distinct(StringComparer.Ordinal).Count()!=items.Count(x=>x.LinkKind!=PortableLinkKind.None)
                ||s.PortableHandling.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.PortableHandling.Length
                ||s.PortableHandling.Select(x=>x.Revision).Distinct().Count()!=s.PortableHandling.Length
                ||s.PortableHandling.Any(x=>x.Revision>s.Revision||x.StartedAt>s.RuleClock||x.EndedAt>s.RuleClock))
                throw new ArgumentException("Duplicate or future portable equipment history.");
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            foreach(var item in items) {
                if(!Actor(item.OwnerId)||!Actor(item.CustodianId))throw new ArgumentException("Portable owner or custodian is not an actor.");
                if(item.ParentId!="") {
                    var parent=items.SingleOrDefault(x=>x.Id==item.ParentId);
                    bool recognizedVessel=parent!=null&&parent.LinkKind==PortableLinkKind.WaterVessel
                        &&item.LinkKind==PortableLinkKind.InventoryLot
                        &&item.MassBasis==PortableMassBasis.WaterPints;
                    if(parent==null||!parent.CapacityPounds.HasValue&&!recognizedVessel||item.CustodianId!=parent.CustodianId
                        ||item.Placement!=PortablePlacement.Contained&&item.Placement!=PortablePlacement.Attached)
                        throw new ArgumentException("Invalid portable containment or attachment.");
                    if(recognizedVessel) {
                        var vessel=s.Vessels.SingleOrDefault(x=>x.Id==parent.LinkedId);
                        var content=s.VesselContents.SingleOrDefault(x=>x.LotId==item.LinkedId&&x.VesselId==parent.LinkedId);
                        if(vessel==null||content==null)throw new ArgumentException("Portable vessel content link is invalid.");
                    }
                }
                var seen=new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal){item.Id};var current=item;
                while(current.ParentId!="") {
                    if(!seen.Add(current.ParentId))throw new ArgumentException("Portable containment cycle.");
                    current=items.Single(x=>x.Id==current.ParentId);
                }
                if(item.LinkKind!=PortableLinkKind.None) {
                    string location=item.ParentId!=""?item.ParentId:item.Placement==PortablePlacement.Ground?GroundLocation(item.GroundX,item.GroundY):item.CustodianId;
                    switch(item.LinkKind) {
                        case PortableLinkKind.InventoryLot:
                            var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==item.LinkedId);var inventory=s.InventoryLots.SingleOrDefault(x=>x.LotId==item.LinkedId);
                            if(lot==null||inventory==null||lot.LocationId!=location||lot.CustodianId!=item.CustodianId||inventory.OwnerId!=item.OwnerId
                                ||item.MassBasis==PortableMassBasis.FoodPounds&&inventory.Nutrition!=NutritionKind.FoodPounds
                                ||item.MassBasis==PortableMassBasis.WaterPints&&inventory.Nutrition!=NutritionKind.WaterPints)
                                throw new ArgumentException("Portable inventory link does not match its physical lot.");
                            break;
                        case PortableLinkKind.WaterVessel:
                            var vessel=s.Vessels.SingleOrDefault(x=>x.Id==item.LinkedId);
                            if(vessel==null||vessel.Profile!=WaterVesselProfile.Waterskin||vessel.LocationId!=location
                                ||vessel.CustodianId!=item.CustodianId||vessel.OwnerId!=item.OwnerId||item.MassBasis!=PortableMassBasis.Fixed)
                                throw new ArgumentException("Portable vessel link does not match its physical vessel.");
                            break;
                        case PortableLinkKind.SupplyEquipment:
                            var tool=s.SupplyCacheEquipment.SingleOrDefault(x=>x.Id==item.LinkedId);
                            if(tool==null||tool.LocationId!=location||tool.CustodianId!=item.CustodianId||tool.OwnerId!=item.OwnerId||item.MassBasis!=PortableMassBasis.Fixed)
                                throw new ArgumentException("Portable equipment link does not match its physical item.");
                            break;
                    }
                }
            }
            foreach(var container in items.Where(x=>x.CapacityPounds.HasValue)) {
                var contents=Descendants(items,container.Id).Where(x=>Inside(container.Id,x.Id,items)).ToArray();
                var placed=contents.Where(x=>EntirePathContained(container.Id,x,items)).ToArray();
                if(placed.Length!=0&&container.FitRuleId=="")throw new ArgumentException("Container fit is not established.");
                if(placed.Any(x=>!FitsAuthoredMember(s,container,x,items))&&container.FitRuleId!="")
                    throw new ArgumentException("Container fit is not established for every contained item.");
                var mass=RuleQuantity.Sum(placed.Select(x=>Mass(s,x)));
                if(mass>container.CapacityPounds.Value)throw new ArgumentException("Container weight capacity exceeded.");
            }
            foreach(var eventRecord in s.PortableHandling) {
                var item=items.SingleOrDefault(x=>x.Id==eventRecord.ItemId);
                if(item==null||!Actor(eventRecord.ActorId)||eventRecord.Id!="inventory."+eventRecord.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture)+".portable")
                    throw new ArgumentException("Invalid portable handling reference.");
                var work=s.Work.WorkerIntervals.Where(x=>x.JobId==eventRecord.Id).ToArray();
                if(eventRecord.Tactical?(eventRecord.StartedAt!=eventRecord.EndedAt||work.Length!=0)
                    :eventRecord.EndedAt!=eventRecord.StartedAt.AddSeconds(1)||work.Length!=1||work[0].WorkerId!=eventRecord.ActorId
                        ||work[0].Start!=eventRecord.StartedAt||work[0].End!=eventRecord.EndedAt)
                    throw new ArgumentException("Portable handling labor does not match its outcome.");
            }
            if(s.Work.WorkerIntervals.Any(w=>!s.Crops.SelectMany(c=>c.Tasks).Any(t=>t.Id==w.JobId)&&!s.Intakes.Any(j=>j.Id==w.JobId)
                &&!s.Handling.Any(j=>j.Id==w.JobId)&&!s.WaterFills.Any(j=>j.Id==w.JobId)&&!s.VesselMoves.Any(j=>j.Id==w.JobId)
                &&!s.SupplyCacheAttempts.Any(j=>j.Id==w.JobId)&&!s.PortableHandling.Any(j=>j.Id==w.JobId)))
                throw new ArgumentException("Unattributed portable handling labor.");
        }
        private static string GroundLocation(int x,int y)=>"ground."+x.ToString(System.Globalization.CultureInfo.InvariantCulture)+"."+y.ToString(System.Globalization.CultureInfo.InvariantCulture);
        public static string GroundLocation(PortableEquipmentRecord item)=>GroundLocation(item.GroundX,item.GroundY);
        private static PortableEquipmentRecord[] Descendants(PortableEquipmentRecord[] items,string id)=>items.Where(x=>Inside(id,x.Id,items)).ToArray();
        private static bool Inside(string parent,string child,PortableEquipmentRecord[] items) {
            var current=items.SingleOrDefault(x=>x.Id==child);var seen=new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal);
            while(current!=null&&current.ParentId!="") {if(current.ParentId==parent)return true;if(!seen.Add(current.ParentId))return false;current=items.SingleOrDefault(x=>x.Id==current.ParentId);}return false;
        }
        private static bool EntirePathContained(string parent,PortableEquipmentRecord child,PortableEquipmentRecord[] items) {
            var current=child;bool edge=false;
            while(current.ParentId!="") {var prior=current;current=items.Single(x=>x.Id==prior.ParentId);if(current.Id==parent)return edge||prior.Placement==PortablePlacement.Contained;
                if(prior.Placement==PortablePlacement.Attached)return false;edge=true;}return false;
        }
        public static bool FitsAuthoredMember(Snapshot s,PortableEquipmentRecord container,PortableEquipmentRecord item)
            =>FitsAuthoredMember(s,container,item,s.PortableEquipment);
        private static bool FitsAuthoredMember(Snapshot s,PortableEquipmentRecord container,PortableEquipmentRecord item,PortableEquipmentRecord[] items)
        {
            if(container.FitMemberIds.Contains(item.Id,StringComparer.Ordinal))return true;
            if(container.FitRuleId!="TEST_ONLY.explorer-pack-fit-v1"||item.LinkKind!=PortableLinkKind.InventoryLot)return false;
            var lot=s.InventoryLots.SingleOrDefault(x=>x.LotId==item.LinkedId);var seen=new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal);
            while(lot!=null&&lot.ParentId!="") {
                if(!seen.Add(lot.ParentId))return false;
                if(container.FitMemberIds.Contains(lot.ParentId,StringComparer.Ordinal)) {
                    var authored=items.SingleOrDefault(x=>x.Id==lot.ParentId&&x.LinkKind==PortableLinkKind.InventoryLot&&x.LinkedId==lot.ParentId);
                    // The split lot retains the authored source item's fit identity even after
                    // its remainder is retrieved. A subset cannot require the original stack to
                    // remain physically inside the same container.
                    return authored!=null;
                }
                lot=s.InventoryLots.SingleOrDefault(x=>x.LotId==lot.ParentId);
            }
            return false;
        }
        public static RuleQuantity Mass(Snapshot s,PortableEquipmentRecord item) {
            if(item.MassBasis==PortableMassBasis.Fixed)return item.OperationalWeightLb.Value;
            var lot=s.Work.Lots.Single(x=>x.Id==item.LinkedId);
            return item.MassBasis==PortableMassBasis.FoodPounds?lot.Amount:lot.Amount;
        }
    }
}
