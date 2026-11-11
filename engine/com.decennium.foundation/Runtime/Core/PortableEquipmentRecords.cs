using System;
using System.Linq;
using System.Collections.ObjectModel;
using System.Numerics;

namespace Decennium.Foundation
{
    public enum PortablePlacement { Carried, Worn, Contained, Attached, Ground }
    public enum PortableLinkKind { None, InventoryLot, WaterVessel, SupplyEquipment }
    public enum PortableMassBasis { Fixed, FoodPounds, WaterPints, GenericPounds, Unmodeled, CountedQuantity }
    public enum PortableOperation { Pickup, Drop, Retrieve, Stow, Handover, Wear, Remove, Open, Close, ShieldDoff }

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
        /// <summary>Hands occupied while carried. Currently authored only for a held Soldier shield.</summary>
        public int HeldHands { get; }

        public PortableEquipmentRecord(string id,string profileId,string ownerId,string custodianId,string parentId,
            PortablePlacement placement,PortableLinkKind linkKind,string linkedId,PortableMassBasis massBasis,
            RuleQuantity? sourceWeightLb,RuleQuantity? operationalWeightLb,RuleQuantity? printedLoad=null,
            RuleQuantity? capacityPounds=null,RuleQuantity? capacityCubicFeet=null,bool wearable=false,bool open=false,
            string fitRuleId="",string[] fitMemberIds=null,int groundX=0,int groundY=0,int heldHands=0)
        {
            var members=fitMemberIds??Array.Empty<string>();
            if(!Validation.ValidId(id)||!Validation.ValidId(profileId)||!Validation.ValidId(ownerId)||!Validation.ValidId(custodianId)
                ||parentId==null||(parentId!=""&&!Validation.ValidId(parentId))||!Enum.IsDefined(typeof(PortablePlacement),placement)
                ||!Enum.IsDefined(typeof(PortableLinkKind),linkKind)||!Enum.IsDefined(typeof(PortableMassBasis),massBasis)
                ||linkedId==null||(linkedId!=""&&!Validation.ValidId(linkedId))||((linkKind==PortableLinkKind.None)!=(linkedId==""))
                ||(linkKind==PortableLinkKind.InventoryLot)!=(massBasis==PortableMassBasis.FoodPounds||massBasis==PortableMassBasis.WaterPints
                    ||massBasis==PortableMassBasis.GenericPounds||massBasis==PortableMassBasis.CountedQuantity)
                ||(massBasis==PortableMassBasis.Fixed)!=operationalWeightLb.HasValue
                ||massBasis==PortableMassBasis.CountedQuantity&&(sourceWeightLb.HasValue||operationalWeightLb.HasValue)
                ||massBasis==PortableMassBasis.Unmodeled&&(sourceWeightLb.HasValue||operationalWeightLb.HasValue||linkKind!=PortableLinkKind.None)
                ||(sourceWeightLb.HasValue&&sourceWeightLb.Value<default(RuleQuantity))||(operationalWeightLb.HasValue&&operationalWeightLb.Value<default(RuleQuantity))
                ||(printedLoad.HasValue&&printedLoad.Value<default(RuleQuantity))||(capacityPounds.HasValue&&capacityPounds.Value<default(RuleQuantity))
                ||(capacityCubicFeet.HasValue&&capacityCubicFeet.Value<default(RuleQuantity))||(capacityPounds.HasValue!=capacityCubicFeet.HasValue)
                ||(placement==PortablePlacement.Worn&&!wearable)
                ||((placement==PortablePlacement.Contained||placement==PortablePlacement.Attached)!=(parentId!=""))
                ||(placement==PortablePlacement.Ground?(groundX<0||groundY<0):(groundX!=0||groundY!=0))
                ||fitRuleId==null||(fitRuleId!=""&&!Validation.ValidId(fitRuleId))||members.Length>32
                ||members.Any(x=>!Validation.ValidId(x)||x==id)||members.Distinct(StringComparer.Ordinal).Count()!=members.Length
                ||((fitRuleId!="")!=(members.Length!=0))||open&&(capacityPounds==null)
                ||heldHands<0||heldHands>2||heldHands>0&&(profileId!="armor-and-shields.shield"||placement!=PortablePlacement.Carried
                    ||parentId!=""||!wearable)
                ||(wearable&&placement!=PortablePlacement.Worn&&profileId!="adventuring-gear.backpack"&&profileId!="armor-and-shields.shield"))
                throw new ArgumentException("Invalid portable equipment record.");
            Id=id;ProfileId=profileId;OwnerId=ownerId;CustodianId=custodianId;ParentId=parentId;Placement=placement;
            LinkKind=linkKind;LinkedId=linkedId;MassBasis=massBasis;SourceWeightLb=sourceWeightLb;OperationalWeightLb=operationalWeightLb;
            PrintedLoad=printedLoad;CapacityPounds=capacityPounds;CapacityCubicFeet=capacityCubicFeet;Wearable=wearable;Open=open;
            FitRuleId=fitRuleId;this.fitMemberIds=members.ToArray();FitMemberIds=Array.AsReadOnly(this.fitMemberIds);GroundX=groundX;GroundY=groundY;HeldHands=heldHands;
        }
        public PortableEquipmentRecord With(string custodianId=null,string parentId=null,PortablePlacement? placement=null,
            bool? open=null,int? groundX=null,int? groundY=null,int? heldHands=null)
            =>new PortableEquipmentRecord(Id,ProfileId,OwnerId,custodianId??CustodianId,parentId??ParentId,placement??Placement,
                LinkKind,LinkedId,MassBasis,SourceWeightLb,OperationalWeightLb,PrintedLoad,CapacityPounds,CapacityCubicFeet,
                Wearable,open??Open,FitRuleId,fitMemberIds,groundX??GroundX,groundY??GroundY,heldHands??HeldHands);
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

    /// <summary>Immutable selected-content facts for profile-based portable storage. A null
    /// packed volume means exterior volume is not established and cannot be stored directly in a
    /// profile-governed container.</summary>
    public sealed class PortableStorageProfileRecord
    {
        private readonly string[] allowedContainedProfileIds;
        public string ProfileId { get; }
        public string QuantityUnitId { get; }
        public RuleQuantity? PackedVolumePerUnitCubicFeet { get; }
        public RuleQuantity? MassPerUnitLb { get; }
        public ReadOnlyCollection<string> AllowedContainedProfileIds { get; }
        public bool RequiresInstalledTemporaryCamp { get; }

        public PortableStorageProfileRecord(string profileId,string quantityUnitId,RuleQuantity? packedVolumePerUnitCubicFeet,
            string[] allowedContainedProfileIds=null,bool requiresInstalledTemporaryCamp=false,RuleQuantity? massPerUnitLb=null)
        {
            if(!Validation.ValidId(profileId)||!Validation.ValidId(quantityUnitId)
                ||packedVolumePerUnitCubicFeet.HasValue&&packedVolumePerUnitCubicFeet.Value<default(RuleQuantity)
                ||massPerUnitLb.HasValue&&massPerUnitLb.Value<=default(RuleQuantity))
                throw new ArgumentException("Invalid portable storage profile.");
            var allowed=allowedContainedProfileIds??Array.Empty<string>();
            if(allowed.Length>64||allowed.Any(x=>!Validation.ValidId(x))
                ||allowed.Distinct(StringComparer.Ordinal).Count()!=allowed.Length
                ||requiresInstalledTemporaryCamp&&allowed.Length==0)
                throw new ArgumentException("Invalid portable storage profile admissions.");
            ProfileId=profileId;QuantityUnitId=quantityUnitId;PackedVolumePerUnitCubicFeet=packedVolumePerUnitCubicFeet;MassPerUnitLb=massPerUnitLb;
            this.allowedContainedProfileIds=allowed.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            AllowedContainedProfileIds=Array.AsReadOnly(this.allowedContainedProfileIds);
            RequiresInstalledTemporaryCamp=requiresInstalledTemporaryCamp;
        }
    }

    /// <summary>Provisional source rule for Load when an item has no separate printed Load.
    /// Known physical pounds divide by ten; this rule never derives volume.</summary>
    public static class CarryingLoadRules
    {
        public static RuleQuantity? FromPrintedLoadOrKnownWeight(RuleQuantity? printedLoad,RuleQuantity? knownPounds,
            bool allowWeightFallback=true)
            =>printedLoad??(allowWeightFallback?knownPounds?.Scale(1,10):(RuleQuantity?)null);
    }

    /// <summary>Pure profile admission and capacity checks shared by Core validation and the
    /// selected TEST_ONLY handling resolver.</summary>
    public static class PortableStorageProfileValidation
    {
        public const int MaxProfiles=64;
        private const string ItemUnit="item";
        public static PortableStorageProfileRecord Find(Snapshot s,string profileId)
            =>s?.PortableStorageProfiles?.SingleOrDefault(x=>x.ProfileId==profileId);
        public static bool CanContain(Snapshot s,PortableEquipmentRecord container,PortableEquipmentRecord child)
        {
            if(s==null||container==null||child==null)return false;
            var profile=Find(s,container.ProfileId);var childProfile=Find(s,child.ProfileId);
            if(profile==null||profile.AllowedContainedProfileIds.Count==0||childProfile==null
                ||!profile.AllowedContainedProfileIds.Contains(child.ProfileId,StringComparer.Ordinal))return false;
            try { PackedVolume(s,child,childProfile);return true; }
            catch(ArgumentException) { return false; }
        }
        public static RuleQuantity PackedVolume(Snapshot s,PortableEquipmentRecord item)
        {
            var profile=Find(s,item?.ProfileId);
            if(profile==null)throw new ArgumentException("Portable storage profile is not established.");
            return PackedVolume(s,item,profile);
        }
        private static RuleQuantity PackedVolume(Snapshot s,PortableEquipmentRecord item,PortableStorageProfileRecord profile)
        {
            if(!profile.PackedVolumePerUnitCubicFeet.HasValue)
                throw new ArgumentException("Portable packed volume is not established.");
            RuleQuantity quantity;string unit;
            if(item.LinkKind==PortableLinkKind.InventoryLot) {
                var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==item.LinkedId);
                if(lot==null)throw new ArgumentException("Portable storage quantity is not established.");
                unit=lot.UnitId;quantity=lot.Amount;
            } else { unit=ItemUnit;quantity=new RuleQuantity(1); }
            if(unit!=profile.QuantityUnitId)throw new ArgumentException("Portable storage quantity unit is not established.");
            var perUnit=profile.PackedVolumePerUnitCubicFeet.Value;
            return RuleQuantity.FromFraction((BigInteger)perUnit.Numerator*quantity.Numerator,
                (BigInteger)perUnit.Denominator*quantity.Denominator);
        }
        public static RuleQuantity Load(Snapshot s,PortableEquipmentRecord item)
        {
            if(item.MassBasis==PortableMassBasis.Unmodeled)
                throw new ArgumentException("Portable item Load is not established.");
            var load=CarryingLoadRules.FromPrintedLoadOrKnownWeight(item.PrintedLoad,
                PortableEquipmentValidation.Mass(s,item));
            if(!load.HasValue)throw new ArgumentException("Portable item Load is not established.");
            return load.Value;
        }
        public static string StorageDestinationFailure(Snapshot s,PortableEquipmentRecord container,PortableEquipmentRecord child)
        {
            var profile=Find(s,container?.ProfileId);
            if(profile==null||profile.AllowedContainedProfileIds.Count==0)return "ContainerFitNotEstablished";
            if(profile.RequiresInstalledTemporaryCamp) {
                var installations=s.TemporaryCampInstallations.Where(x=>x.LotId==container.Id
                    &&x.Kind==TemporaryCampFixtureKind.FittingPack).ToArray();
                if(installations.Length>1)return "TemporaryCampStorageInstallationInvalid";
                var installation=installations.SingleOrDefault();
                if(installation==null||!TemporaryCampConstructionValidation.HasTemporaryCamp(s,installation.SiteId))
                    return "TemporaryCampStorageNotInstalled";
                var capacity=TemporaryCampConstructionValidation.StorageCapacity(s,installation.SiteId);
                if(container.CapacityPounds!=capacity.Pounds||container.CapacityCubicFeet!=capacity.CubicFeet)
                    return "TemporaryCampStorageCapacityMismatch";
            }
            return CanContain(s,container,child)?null:"ContainerFitNotEstablished";
        }
        public static RuleQuantity ContentsVolume(Snapshot s,PortableEquipmentRecord container)
        {
            var direct=s.PortableEquipment.Where(x=>x.ParentId==container.Id&&x.Placement==PortablePlacement.Contained).ToArray();
            return RuleQuantity.Sum(direct.Select(x=>PackedVolume(s,x)));
        }
        public static void ValidateSnapshot(Snapshot s)
        {
            if(s.PortableStorageProfiles==null||s.PortableStorageProfiles.Length>MaxProfiles
                ||s.PortableStorageProfiles.Any(x=>x==null))throw new ArgumentException("Invalid portable storage profile collection.");
            if(s.SchemaVersion<Snapshot.PortableStorageSchema) {
                if(s.PortableStorageProfiles.Length!=0)throw new ArgumentException("Portable storage profiles require schema71.");
                return;
            }
            if(s.SchemaVersion<Snapshot.PortableCountedLotSchema&&s.PortableStorageProfiles.Any(x=>x.MassPerUnitLb.HasValue))
                throw new ArgumentException("Per-unit portable mass requires schema73.");
            if((s.SchemaVersion==Snapshot.MiningAssistantSchema||s.SchemaVersion==Snapshot.HavenAppraisalSchema)
                &&s.TestOnly&&s.PortableStorageProfiles.Length==0)return;
            if(!s.TestOnly||s.PortableStorageProfiles.Length==0)
                throw new ArgumentException("Schema71 portable storage facts require a selected TEST_ONLY profile.");
            var profiles=s.PortableStorageProfiles;
            if(profiles.Select(x=>x.ProfileId).Distinct(StringComparer.Ordinal).Count()!=profiles.Length
                ||profiles.Any(x=>x.AllowedContainedProfileIds.Any(id=>!profiles.Any(p=>p.ProfileId==id))))
                throw new ArgumentException("Duplicate or unresolved portable storage profile.");
            foreach(var item in s.PortableEquipment) {
                if(item.ParentId==""||item.Placement!=PortablePlacement.Contained)continue;
                var parent=s.PortableEquipment.Single(x=>x.Id==item.ParentId);
                var parentProfile=Find(s,parent.ProfileId);
                if(parentProfile==null||parentProfile.AllowedContainedProfileIds.Count==0)continue;
                if(!CanContain(s,parent,item))throw new ArgumentException("Portable container profile fit is not established.");
            }
        }
        internal static void ValidateContainer(Snapshot s,PortableEquipmentRecord container,PortableEquipmentRecord[] placed)
        {
            var profile=Find(s,container.ProfileId);
            if(profile==null||profile.AllowedContainedProfileIds.Count==0)return;
            if(profile.RequiresInstalledTemporaryCamp) {
                var installations=s.TemporaryCampInstallations.Where(x=>x.LotId==container.Id
                    &&x.Kind==TemporaryCampFixtureKind.FittingPack).ToArray();
                if(installations.Length>1)throw new ArgumentException("Temporary Camp storage installation is duplicated.");
                var installation=installations.SingleOrDefault();
                if(installation==null) {
                    if(placed.Length!=0)throw new ArgumentException("Temporary Camp storage is not installed.");
                } else {
                    if(!TemporaryCampConstructionValidation.HasTemporaryCamp(s,installation.SiteId))
                        throw new ArgumentException("Temporary Camp storage is not installed.");
                    var capacity=TemporaryCampConstructionValidation.StorageCapacity(s,installation.SiteId);
                    if(container.CapacityPounds!=capacity.Pounds||container.CapacityCubicFeet!=capacity.CubicFeet)
                        throw new ArgumentException("Temporary Camp derived storage capacity mismatch.");
                    var load=RuleQuantity.Sum(placed.Select(x=>Load(s,x)));
                    if(load>new RuleQuantity(capacity.Load))throw new ArgumentException("Temporary Camp Load capacity exceeded.");
                }
            }
            var direct=s.PortableEquipment.Where(x=>x.ParentId==container.Id&&x.Placement==PortablePlacement.Contained).ToArray();
            if(direct.Any(x=>!CanContain(s,container,x)))throw new ArgumentException("Portable container profile fit is not established.");
            var volume=RuleQuantity.Sum(direct.Select(x=>PackedVolume(s,x)));
            if(!container.CapacityCubicFeet.HasValue||volume>container.CapacityCubicFeet.Value)
                throw new ArgumentException("Portable container volume capacity exceeded.");
        }
    }

    public static class PortableEquipmentValidation
    {
        public const int MaxItems=128,MaxHandling=256;
        public static void Validate(Snapshot s)
        {
            if(s.PortableEquipment==null||s.PortableHandling==null||s.PortableEquipment.Length>MaxItems||s.PortableHandling.Length>MaxHandling
                ||s.PortableEquipment.Any(x=>x==null)||s.PortableHandling.Any(x=>x==null))throw new ArgumentException("Invalid portable equipment collections.");
            PortableStorageProfileValidation.ValidateSnapshot(s);
            if(s.SchemaVersion<Snapshot.PortableEquipmentSchema) {
                if(s.PortableEquipment.Length!=0||s.PortableHandling.Length!=0)throw new ArgumentException("Portable equipment requires schema20.");
                return;
            }
            var items=s.PortableEquipment;
            if(s.SchemaVersion<Snapshot.SoldierInitialBuildSchema&&items.Any(x=>x.HeldHands!=0))
                throw new ArgumentException("Held portable equipment requires schema28.");
            if(items.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=items.Length
                ||items.Where(x=>x.LinkKind!=PortableLinkKind.None).Select(x=>x.LinkedId).Distinct(StringComparer.Ordinal).Count()!=items.Count(x=>x.LinkKind!=PortableLinkKind.None)
                ||s.PortableHandling.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.PortableHandling.Length
                ||s.PortableHandling.Select(x=>x.Revision).Distinct().Count()!=s.PortableHandling.Length
                ||s.PortableHandling.Any(x=>x.Revision>s.Revision||x.StartedAt>s.RuleClock||x.EndedAt>s.RuleClock))
                throw new ArgumentException("Duplicate or future portable equipment history.");
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            foreach(var item in items) {
                if(item.MassBasis==PortableMassBasis.Unmodeled&&s.SchemaVersion<Snapshot.OrdinaryReceptacleSchema)
                    throw new ArgumentException("Unmodeled mass requires schema50.");
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
                                ||item.MassBasis==PortableMassBasis.WaterPints&&inventory.Nutrition!=NutritionKind.WaterPints
                                ||item.MassBasis==PortableMassBasis.GenericPounds&&(inventory.Nutrition!=NutritionKind.None||lot.UnitId!="mass-pound")
                                ||item.MassBasis==PortableMassBasis.CountedQuantity&&(s.SchemaVersion<Snapshot.PortableCountedLotSchema
                                    ||inventory.Nutrition!=NutritionKind.None
                                    ||PortableStorageProfileValidation.Find(s,item.ProfileId) is not PortableStorageProfileRecord countedProfile
                                    ||countedProfile.QuantityUnitId!=lot.UnitId||!countedProfile.MassPerUnitLb.HasValue
                                    ||!countedProfile.PackedVolumePerUnitCubicFeet.HasValue
                                    ||lot.Amount.Denominator!=1
                                    ||countedProfile.PackedVolumePerUnitCubicFeet.Value<=default(RuleQuantity)))
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
                var storageProfile=PortableStorageProfileValidation.Find(s,container.ProfileId);
                bool profileContainer=storageProfile!=null&&storageProfile.AllowedContainedProfileIds.Count!=0;
                if(!profileContainer) {
                    if(placed.Length!=0&&container.FitRuleId=="")throw new ArgumentException("Container fit is not established.");
                    if(placed.Any(x=>!FitsAuthoredMember(s,container,x,items))&&container.FitRuleId!="")
                        throw new ArgumentException("Container fit is not established for every contained item.");
                }
                var mass=RuleQuantity.Sum(placed.Select(x=>Mass(s,x)));
                if(mass>container.CapacityPounds.Value)throw new ArgumentException("Container weight capacity exceeded.");
                PortableStorageProfileValidation.ValidateContainer(s,container,placed);
            }
            foreach(var eventRecord in s.PortableHandling) {
                var item=items.SingleOrDefault(x=>x.Id==eventRecord.ItemId);
                if(item==null||!Actor(eventRecord.ActorId)||eventRecord.Id!="inventory."+eventRecord.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture)+".portable")
                    throw new ArgumentException("Invalid portable handling reference.");
                if(eventRecord.Operation==PortableOperation.ShieldDoff&&(s.SchemaVersion<Snapshot.SoldierInitialBuildSchema||!eventRecord.Tactical
                    ||eventRecord.Before!=PortablePlacement.Worn||eventRecord.After!=PortablePlacement.Carried
                    ||item.ProfileId!="armor-and-shields.shield"||!item.Wearable
                    ||!s.InitialCharacterLoadouts.Any(x=>x.ActorId==eventRecord.ActorId&&x.ShieldId==item.Id)))
                    throw new ArgumentException("Invalid tactical shield-doff history.");
                var work=s.Work.WorkerIntervals.Where(x=>x.JobId==eventRecord.Id).ToArray();
                if(eventRecord.Tactical?(eventRecord.StartedAt!=eventRecord.EndedAt||work.Length!=0)
                    :eventRecord.EndedAt!=eventRecord.StartedAt.AddSeconds(1)||work.Length!=1||work[0].WorkerId!=eventRecord.ActorId
                        ||work[0].Start!=eventRecord.StartedAt||work[0].End!=eventRecord.EndedAt)
                    throw new ArgumentException("Portable handling labor does not match its outcome.");
            }
            if(s.Work.WorkerIntervals.Any(w=>!s.Crops.SelectMany(c=>c.Tasks).Any(t=>t.Id==w.JobId)&&!s.Intakes.Any(j=>j.Id==w.JobId)
                &&!s.Handling.Any(j=>j.Id==w.JobId)&&!s.WaterFills.Any(j=>j.Id==w.JobId)&&!s.VesselMoves.Any(j=>j.Id==w.JobId)
                &&!s.SupplyCacheAttempts.Any(j=>j.Id==w.JobId)&&!s.PortableHandling.Any(j=>j.Id==w.JobId)
                &&!s.FormulaWork.Any(j=>j.Id==w.JobId)&&!s.RepairWork.Any(j=>j.Id==w.JobId)&&!s.ManufacturingOrders.Any(j=>j.Id==w.JobId)
                &&!s.Recipe347WorkOrders.Any(j=>j.Id==w.JobId)
                &&!s.HarvestRequirementWorks.Any(j=>j.Id==w.JobId)
                &&!s.HarvestPreservationTreatmentAttempts.Any(j=>j.Id==w.JobId)
                &&!s.FishingTrapAttempts.Any(j=>j.Id==w.JobId)&&!s.FishingTrapRetrievals.Any(j=>j.Id==w.JobId)&&!s.HarvestAttempts.Any(j=>j.Id==w.JobId)
                &&!s.MiningAttempts.Any(j=>j.Id==w.JobId)
                &&!s.HavenAppraisals.Any(j=>j.Id==w.JobId)
                &&!s.ProspectingAttempts.Any(j=>j.Id==w.JobId)
                &&!s.MiningAssayAttempts.Any(j=>j.Id==w.JobId)
                &&!s.DestructiveMiningAssayAttempts.Any(j=>j.Id==w.JobId)
                &&!s.MineralPreparationAttempts.Any(j=>j.Id==w.JobId)
                &&!s.OrdinaryReceptacleAttempts.Any(j=>j.Id==w.JobId)
                &&!s.HuntingTrapActions.Any(j=>j.Id==w.JobId)
                &&!s.CacheExcavations.Any(j=>j.Id==w.JobId)
                &&!s.TemporaryCampConstructionAttempts.Any(j=>j.Id==w.JobId)
                &&!s.RouteMappingWorkAttempts.Any(j=>j.Id==w.JobId)
                &&!s.RouteReconnaissanceAttempts.Any(j=>j.Id==w.JobId)
                &&!s.CraftingIncidents.Any(j=>w.JobId=="craft.remedy."+j.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture))))
                throw new ArgumentException("Unattributed worker interval.");
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
            if(item.LinkKind!=PortableLinkKind.InventoryLot)return false;
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
            if(item.MassBasis==PortableMassBasis.Unmodeled)throw new InvalidOperationException("Portable item mass is not modeled.");
            var lot=s.Work.Lots.Single(x=>x.Id==item.LinkedId);
            if(item.MassBasis!=PortableMassBasis.CountedQuantity)return lot.Amount;
            var profile=PortableStorageProfileValidation.Find(s,item.ProfileId);
            if(profile==null||profile.QuantityUnitId!=lot.UnitId||!profile.MassPerUnitLb.HasValue)
                throw new InvalidOperationException("Counted portable item mass is not established.");
            var perUnit=profile.MassPerUnitLb.Value;
            return RuleQuantity.FromFraction((BigInteger)perUnit.Numerator*lot.Amount.Numerator,
                (BigInteger)perUnit.Denominator*lot.Amount.Denominator);
        }
    }
}
