#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One authored TEST_ONLY Explorer's Pack arrangement. Source weights are retained
    /// separately from the exact internal-fit fact; no item-volume inference is made.</summary>
    public sealed class PortableKitFixture
    {
        public const string Pack="TEST_ONLY.explorer-pack",Rations="TEST_ONLY.pack-rations",Skin="TEST_ONLY.pack-skin",Water="TEST_ONLY.pack-water";
        public const string Tools=SupplyCacheFixture.ToolsId,MessKit="TEST_ONLY.pack-mess-kit",Tinderbox="TEST_ONLY.pack-tinderbox";
        public const string Bedroll="TEST_ONLY.pack-bedroll",Torches="TEST_ONLY.pack-torches",Rope="TEST_ONLY.pack-rope";
        public const string ActorPouch="TEST_ONLY.actor-pouch",CompanionPouch="TEST_ONLY.companion-pouch";
        public const string FitRule="TEST_ONLY.explorer-pack-fit-v1";
        public static readonly System.Collections.ObjectModel.ReadOnlyCollection<string> FitMembers=Array.AsReadOnly(new[]{Rations,Skin,Water,Tools,MessKit,Tinderbox});
        internal string Key=>"portable-kit-schema20-v1|source-main-46a4d527|pack.explorer|interior=20lb-rations+5lb-full-skin+1lb-tools+1lb-mess-kit+1lb-tinderbox;exact-fixture-fit-28lb|external=7lb-bedroll+10lb-torches+10lb-rope-strapped|simple-unfastened-worn-open-pack|"+FitRule+"|"+string.Join(",",FitMembers);
    }

    /// <summary>Physical execution for the narrow reviewed pack fixture. This does not define a
    /// universal item catalog, volume model, body-size model or release equipment policy.</summary>
    public static class PortableEquipmentRules
    {
        private static string N(long value)=>value.ToString(CultureInfo.InvariantCulture);
        internal static string Fingerprint(string prior,PortableKitFixture facts)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.portable-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+facts.Key)).Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
        internal static void Initialize(Snapshot s)
        {
            string actor=TestOnlyPolicy.ActorId,companion=TestOnlyPolicy.CompanionId;
            if(s.SchemaVersion<Snapshot.PortableEquipmentSchema||s.SupplyCaches.Length!=1
                ||!s.SupplyCacheEquipment.Any(x=>x.Id==PortableKitFixture.Tools))throw new ArgumentException("Portable kit requires the selected cache and actual tools.");
            var pack=PortableKitFixture.Pack;
            s.Work=new WorkLedger(s.Work.Lots.Concat(new[]{
                new ResourceLot(PortableKitFixture.Rations,TestOnlyInventoryPolicy.FoodUnit,new RuleQuantity(20),pack,actor),
                new ResourceLot(PortableKitFixture.Water,TestOnlyInventoryPolicy.WaterUnit,new RuleQuantity(4),PortableKitFixture.Skin,actor)
            }),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Concat(new[]{
                new InventoryLotRecord(PortableKitFixture.Rations,"",actor,new RuleQuantity(20),s.RuleClock,NutritionKind.FoodPounds,
                    new RuleTime(2592000),InventoryAccess.Stowed),
                new InventoryLotRecord(PortableKitFixture.Water,"",actor,new RuleQuantity(4),s.RuleClock,NutritionKind.WaterPints,null,InventoryAccess.Stowed)
            }).ToArray();
            s.Vessels=s.Vessels.Concat(new[]{new WaterVesselRecord(PortableKitFixture.Skin,WaterVesselProfile.Waterskin,actor,pack,actor)}).ToArray();
            s.VesselContents=s.VesselContents.Concat(new[]{new VesselContentRecord(PortableKitFixture.Water,PortableKitFixture.Skin)}).ToArray();
            s.SupplyCacheEquipment=s.SupplyCacheEquipment.Select(x=>x.Id==PortableKitFixture.Tools
                ?new SupplyCacheEquipmentRecord(x.Id,x.Kind,x.OwnerId,pack,x.CustodianId):x).ToArray();
            RuleQuantity Q(long value)=>new RuleQuantity(value);
            PortableEquipmentRecord Fixed(string id,string profile,string owner,string parent,PortablePlacement place,long weight,bool? wearable=null,
                bool open=false,string fit="",string[] fitMembers=null,long? capacity=null,long? volume=null)
                =>new PortableEquipmentRecord(id,profile,owner,owner,parent,place,PortableLinkKind.None,"",PortableMassBasis.Fixed,Q(weight),Q(weight),
                    capacityPounds:capacity.HasValue?Q(capacity.Value):(RuleQuantity?)null,capacityCubicFeet:volume.HasValue?Q(volume.Value):(RuleQuantity?)null,
                    wearable:wearable??false,open:open,fitRuleId:fit,fitMemberIds:fitMembers,groundX:0,groundY:0);
            var items=new List<PortableEquipmentRecord>{
                new PortableEquipmentRecord(pack,"adventuring-gear.backpack",actor,actor,"",PortablePlacement.Worn,PortableLinkKind.None,"",PortableMassBasis.Fixed,
                    Q(5),Q(5),capacityPounds:Q(30),capacityCubicFeet:Q(1),wearable:true,open:true,fitRuleId:PortableKitFixture.FitRule,fitMemberIds:PortableKitFixture.FitMembers.ToArray()),
                new PortableEquipmentRecord(PortableKitFixture.Rations,"adventuring-gear.rations-1-day",actor,actor,pack,PortablePlacement.Contained,
                    PortableLinkKind.InventoryLot,PortableKitFixture.Rations,PortableMassBasis.FoodPounds,Q(20),null),
                new PortableEquipmentRecord(PortableKitFixture.Skin,"adventuring-gear.waterskin",actor,actor,pack,PortablePlacement.Contained,
                    PortableLinkKind.WaterVessel,PortableKitFixture.Skin,PortableMassBasis.Fixed,Q(5),Q(1)),
                new PortableEquipmentRecord(PortableKitFixture.Water,"prototype.potable-water.pint",actor,actor,PortableKitFixture.Skin,PortablePlacement.Contained,
                    PortableLinkKind.InventoryLot,PortableKitFixture.Water,PortableMassBasis.WaterPints,Q(4),null),
                new PortableEquipmentRecord(PortableKitFixture.Tools,"tools.thieves-tools",actor,actor,pack,PortablePlacement.Contained,
                    PortableLinkKind.SupplyEquipment,PortableKitFixture.Tools,PortableMassBasis.Fixed,Q(1),Q(1)),
                Fixed(PortableKitFixture.MessKit,"adventuring-gear.mess-kit",actor,pack,PortablePlacement.Contained,1),
                Fixed(PortableKitFixture.Tinderbox,"adventuring-gear.tinderbox",actor,pack,PortablePlacement.Contained,1),
                Fixed(PortableKitFixture.Bedroll,"adventuring-gear.bedroll",actor,pack,PortablePlacement.Attached,7),
                Fixed(PortableKitFixture.Torches,"adventuring-gear.torch",actor,pack,PortablePlacement.Attached,10),
                Fixed(PortableKitFixture.Rope,"adventuring-gear.rope-hempen-50-feet",actor,pack,PortablePlacement.Attached,10),
                Fixed(PortableKitFixture.ActorPouch,"adventuring-gear.pouch",actor,"",PortablePlacement.Carried,1),
                Fixed(PortableKitFixture.CompanionPouch,"adventuring-gear.pouch",companion,"",PortablePlacement.Carried,1),
                new PortableEquipmentRecord(TestOnlyFillingPolicy.CompanionSkinId,"adventuring-gear.waterskin",companion,companion,"",
                    PortablePlacement.Carried,PortableLinkKind.WaterVessel,TestOnlyFillingPolicy.CompanionSkinId,PortableMassBasis.Fixed,Q(1),Q(1))
            };
            s.PortableEquipment=items.ToArray();
        }
        internal static void ValidateFixture(Snapshot s)
        {
            foreach(var item in s.PortableEquipment.Where(x=>x.ParentId!=""&&x.MassBasis==PortableMassBasis.WaterPints)) {
                var parent=s.PortableEquipment.SingleOrDefault(x=>x.Id==item.ParentId);
                if(parent?.LinkKind!=PortableLinkKind.WaterVessel)continue;
                var vessel=s.Vessels.Single(x=>x.Id==parent.LinkedId);var contents=s.Work.Lots.Single(x=>x.Id==item.LinkedId);
                if(contents.Amount>WaterFilling.Capacity(vessel.Profile))throw new ArgumentException("Portable vessel content exceeds its selected prototype capacity.");
            }
        }

        public static BurdenTotals CarriedBurden(Snapshot s,string actor)
        {
            if(s==null||!s.Actors.Any(x=>x.Id==actor))throw new ArgumentException("Unknown carrying actor.");
            var records=s.PortableEquipment;
            var modeled=records.Where(item=>IsCarriedBy(s,actor,item)).ToArray();
            var burden=modeled.Select(x=>{
                if(x.MassBasis==PortableMassBasis.Unmodeled)return new BurdenItem(x.Id,x.ParentId==""?null:x.ParentId,null,null);
                var mass=PortableEquipmentValidation.Mass(s,x);
                // A missing source weight is retained as null; only its approved operational
                // Load fallback supplies estimated pounds for routine carrying.
                RuleQuantity? pounds=x.SourceWeightLb.HasValue?mass:(RuleQuantity?)null;
                RuleQuantity? load=x.PrintedLoad??(x.SourceWeightLb.HasValue?null:mass.Scale(1,10));
                return new BurdenItem(x.Id,x.ParentId==""?null:x.ParentId,pounds,load);
            }).ToList();
            foreach(var club in s.Clubs.Where(x=>x.HeldBy==actor))
                burden.Add(new BurdenItem(club.Id,null,new RuleQuantity(2),null));
            foreach(var crossbow in s.RepeatingCrossbows.Where(x=>x.CustodianId==actor&&x.HeldBy==actor))
                burden.Add(new BurdenItem(crossbow.Id,null,new RuleQuantity(20)+new RuleQuantity(3L*crossbow.LoadedBoltLots.Count,40),null));
            foreach(var lot in s.AmmunitionLots.Where(x=>x.CustodianId==actor))
                burden.Add(new BurdenItem(lot.Id,null,new RuleQuantity(3L*lot.AvailableQuantity,40),null));
            if(s.SchemaVersion>=Snapshot.ExpeditionStrainRecoverySchema) {
                // Schema64's TEST_ONLY inventory composition can have no PortableEquipment
                // records at all. Preserve its existing fixed-pouch fact and include legacy
                // carried lots/vessels that the portable projection does not own. Earlier
                // schemas retain their exact historical projection.
                if(!(s.SchemaVersion>=Snapshot.HavenSaleSchema&&actor==TestOnlyHavenSaleProfile.BuyerId)
                    &&!records.Any(x=>x.ProfileId=="adventuring-gear.pouch"&&x.OwnerId==actor))
                    burden.Add(new BurdenItem("TEST_ONLY.default-pouch."+actor,null,new RuleQuantity(1),new RuleQuantity(1,10)));
                var portableLots=new HashSet<string>(records.Where(x=>x.LinkKind==PortableLinkKind.InventoryLot)
                    .Select(x=>x.LinkedId),StringComparer.Ordinal);
                var carriedVesselIds=new HashSet<string>(s.Vessels.Where(v=>v.LocationId==actor&&v.CustodianId==actor)
                    .Select(v=>v.Id),StringComparer.Ordinal);
                var unlinkedVessels=s.Vessels.Where(v=>v.LocationId==actor&&v.CustodianId==actor
                    &&!records.Any(x=>x.LinkKind==PortableLinkKind.WaterVessel&&x.LinkedId==v.Id)).ToArray();
                var coveredUnlinkedContents=new HashSet<string>(StringComparer.Ordinal);
                foreach(var vessel in unlinkedVessels) {
                    var contents=s.VesselContents.Where(x=>x.VesselId==vessel.Id&&!portableLots.Contains(x.LotId))
                        .Select(x=>s.Work.Lots.Single(l=>l.Id==x.LotId)).ToArray();
                    string physicalId="TEST_ONLY.unlinked-vessel."+vessel.Id;
                    var mass=WaterFilling.Tare(vessel.Profile)+RuleQuantity.Sum(contents.Select(x=>x.Amount));
                    var contentIds=contents.Select(x=>x.Id).ToArray();
                    foreach(var id in contentIds)coveredUnlinkedContents.Add(id);
                    burden.Add(new BurdenItem(physicalId,null,mass,mass.Scale(1,10),contentIds,contentIds));
                    foreach(var content in contents)
                        burden.Add(new BurdenItem(content.Id,physicalId,content.Amount,content.Amount.Scale(1,10)));
                }
                foreach(var lot in s.Work.Lots.Where(x=>(x.LocationId==actor||carriedVesselIds.Contains(x.LocationId))
                    &&!portableLots.Contains(x.Id)&&!coveredUnlinkedContents.Contains(x.Id)))
                    burden.Add(new BurdenItem(lot.Id,null,lot.Amount,lot.Amount.Scale(1,10)));
            }
            return PlaytestCarrying.Total(burden);
        }
        internal static bool IsCarriedBy(Snapshot s, string actor, PortableEquipmentRecord item)
        {
            var current = item;
            var seen = new HashSet<string>(StringComparer.Ordinal);
            while (current.ParentId != "") {
                if (!seen.Add(current.ParentId)) return false;
                current = s.PortableEquipment.Single(x => x.Id == current.ParentId);
            }
            return current.CustodianId == actor && current.Placement != PortablePlacement.Ground;
        }

        public static bool IsBurdened(Snapshot s,string actor)
        {
            var burden=CarriedBurden(s,actor);if(!burden.Pounds.HasValue||!burden.Load.HasValue)throw new InvalidOperationException("Portable carrying evidence is incomplete.");
            return PlaytestCarrying.IsBurdened(burden.Load.Value,PlaytestCarrying.Limits(CarrierSize.Medium,10).Load);
        }
        internal static string[] Owners(Snapshot s,string itemId)
        {
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==itemId);if(item==null)return Array.Empty<string>();
            var ids=Descendants(s,itemId).Select(x=>x.OwnerId).Append(item.OwnerId).Distinct(StringComparer.Ordinal).ToArray();
            return ids;
        }
        internal static PortableEquipmentRecord[] Descendants(Snapshot s,string id)
        {
            var result=new List<PortableEquipmentRecord>();var pending=new Queue<string>();pending.Enqueue(id);
            while(pending.Count!=0){var parent=pending.Dequeue();foreach(var child in s.PortableEquipment.Where(x=>x.ParentId==parent)){result.Add(child);pending.Enqueue(child.Id);}}
            return result.ToArray();
        }
        internal static bool Accessible(Snapshot s,string actor,PortableEquipmentRecord item)
        {
            var current=item;var seen=new HashSet<string>(StringComparer.Ordinal);
            while(true) {
                if(current.Placement==PortablePlacement.Ground) {
                    var a=s.Actors.Single(x=>x.Id==actor);
                    return Math.Abs((long)a.X-current.GroundX)+Math.Abs((long)a.Y-current.GroundY)<=1;
                }
                if(current.ParentId=="")return current.CustodianId==actor;
                var parent=s.PortableEquipment.SingleOrDefault(x=>x.Id==current.ParentId);
                if(parent==null||!seen.Add(parent.Id))return false;
                if(current.Placement==PortablePlacement.Contained&&!parent.Open)return false;
                current=parent;
            }
        }
        internal static bool HasPendingClaim(Snapshot s,PortableEquipmentRecord item)
            =>HasPendingClaim(s,item,false);
        internal static bool HasPendingClaim(Snapshot s,PortableEquipmentRecord item,bool ignoreExactInstalledCampAnchor)
        {
            var ids=Descendants(s,item.Id).Select(x=>x.Id).Append(item.Id).ToHashSet(StringComparer.Ordinal);
            var lots=s.PortableEquipment.Where(x=>ids.Contains(x.Id)&&x.LinkKind==PortableLinkKind.InventoryLot).Select(x=>x.LinkedId).ToHashSet(StringComparer.Ordinal);
            var vessels=s.PortableEquipment.Where(x=>ids.Contains(x.Id)&&x.LinkKind==PortableLinkKind.WaterVessel).Select(x=>x.LinkedId).ToHashSet(StringComparer.Ordinal);
            var tools=s.PortableEquipment.Where(x=>ids.Contains(x.Id)&&x.LinkKind==PortableLinkKind.SupplyEquipment).Select(x=>x.LinkedId).ToHashSet(StringComparer.Ordinal);
            bool IsExactInstalledCampAnchor(ResourceReservation reservation)
            {
                if(!ignoreExactInstalledCampAnchor||reservation.LotId!=item.Id)return false;
                var installation=s.TemporaryCampInstallations.SingleOrDefault(x=>x.AttemptId==reservation.JobId
                    &&x.LotId==item.Id&&x.Kind==TemporaryCampFixtureKind.FittingPack);
                if(installation==null)return false;
                var attempt=s.TemporaryCampConstructionAttempts.SingleOrDefault(x=>x.Id==installation.AttemptId);
                return attempt!=null&&attempt.Status==TemporaryCampConstructionStatus.Resolved
                    &&attempt.Check!=null&&attempt.Check.Result>=TemporaryCampConstructionResult.Success;
            }
            return s.Work.Reservations.Any(x=>lots.Contains(x.LotId)&&x.RemainingAmount!=default&&!IsExactInstalledCampAnchor(x))
                ||s.Intakes.Any(x=>lots.Contains(x.LotId)&&x.Status==IntakeStatus.Working)
                ||s.WaterFills.Any(x=>x.Pending&&(vessels.Contains(x.DestinationId)||vessels.Contains(WaterFilling.SourceVessel(s,x.SourceLotId))))
                ||s.SupplyCacheAttempts.Any(x=>x.Status==SupplyCacheAttemptStatus.Working&&tools.Contains(x.EquipmentId))
                ||s.OrdinaryReceptacleAttempts.Any(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working&&ids.Contains(x.CredentialItemId))
                ||s.MiningAttempts.Where(x=>x.Status==MiningAttemptStatus.Working||x.Status==MiningAttemptStatus.Paused
                    ||x.Status==MiningAttemptStatus.AwaitingCheck).Any(x=>{
                        var deposit=s.MiningDeposits.SingleOrDefault(d=>d.Id==x.DepositId);
                        return deposit!=null&&(ids.Contains(deposit.MiningToolsId)||ids.Contains(deposit.PickId)||ids.Contains(deposit.ReceiverId)
                            ||x.SelectedUnitIds.Any(ids.Contains));
                    })
                ||s.SchemaVersion>=Snapshot.MiningToolCandidateSchema&&s.MiningToolUses.Any(use=>{
                    var profile=s.MiningToolCandidateProfiles.SingleOrDefault(p=>p.Id==use.ProfileId);
                    var attempt=s.MiningAttempts.SingleOrDefault(a=>a.Id==use.MiningAttemptId);
                    bool recipeProduced=profile!=null&&s.SchemaVersion>=Snapshot.Recipe347Schema
                        &&s.Recipe347MiningToolProfiles.Any(x=>x.ItemId==profile.ToolItemId);
                    return profile!=null&&attempt!=null&&ids.Contains(profile.ToolItemId)
                        &&(attempt.Status==MiningAttemptStatus.Working||!recipeProduced
                            &&(attempt.Status==MiningAttemptStatus.Paused||attempt.Status==MiningAttemptStatus.AwaitingCheck));
                })
                ||s.CacheExcavations.Any(x=>(x.Status==CacheExcavationStatus.Working||x.Status==CacheExcavationStatus.Paused)&&ids.Contains(x.ShovelId))
                ||s.MineralPreparationAttempts.Where(x=>x.Status==MineralPreparationStatus.Working||x.Status==MineralPreparationStatus.Paused
                    ||x.Status==MineralPreparationStatus.AwaitingCompletion).Any(x=>{
                        var unit=s.MiningUnits.SingleOrDefault(u=>u.Id==x.UnitId);
                        var deposit=unit==null?null:s.MiningDeposits.SingleOrDefault(d=>d.Id==unit.DepositId);
                        return ids.Contains(x.UnitId)||deposit!=null&&(ids.Contains(deposit.MiningToolsId)||ids.Contains(deposit.ReceiverId));
                    });
        }
        internal static bool InventoryAccessible(Snapshot s,string actor,string location)
        {
            var portable=s.PortableEquipment.SingleOrDefault(x=>x.Id==location&&x.CapacityPounds.HasValue);
            return portable!=null&&Accessible(s,actor,portable)&&portable.Open;
        }
        internal static void SynchronizeLinks(Snapshot s)
        {
            var lots=s.Work.Lots.ToDictionary(x=>x.Id,x=>x,StringComparer.Ordinal);
            var inventory=s.InventoryLots.ToDictionary(x=>x.LotId,x=>x,StringComparer.Ordinal);
            var vessels=s.Vessels.ToDictionary(x=>x.Id,x=>x,StringComparer.Ordinal);
            var tools=s.SupplyCacheEquipment.ToDictionary(x=>x.Id,x=>x,StringComparer.Ordinal);
            foreach(var item in s.PortableEquipment.Where(x=>x.LinkKind!=PortableLinkKind.None)) {
                string location=item.ParentId!=""?item.ParentId:item.Placement==PortablePlacement.Ground
                    ?PortableEquipmentValidation.GroundLocation(item):item.CustodianId;
                if(item.LinkKind==PortableLinkKind.InventoryLot) {
                    var lot=lots[item.LinkedId];lots[item.LinkedId]=new ResourceLot(lot.Id,lot.UnitId,lot.Amount,location,item.CustodianId);
                    var old=inventory[item.LinkedId];InventoryAccess access;
                    if(item.Placement==PortablePlacement.Ground)access=InventoryAccess.Ground;
                    else if(item.ParentId=="")access=InventoryAccess.Ready;
                    else {
                        var parent=s.PortableEquipment.Single(x=>x.Id==item.ParentId);
                        access=parent.LinkKind==PortableLinkKind.WaterVessel&&parent.ParentId==""&&parent.Placement!=PortablePlacement.Ground
                            ?InventoryAccess.Ready:InventoryAccess.Stowed;
                    }
                    inventory[item.LinkedId]=new InventoryLotRecord(old.LotId,old.ParentId,old.OwnerId,old.CreatedAmount,old.CreatedAt,old.Nutrition,old.FreshUntil,access);
                } else if(item.LinkKind==PortableLinkKind.WaterVessel) {
                    var vessel=vessels[item.LinkedId];vessels[item.LinkedId]=new WaterVesselRecord(vessel.Id,vessel.Profile,vessel.OwnerId,location,item.CustodianId);
                } else if(item.LinkKind==PortableLinkKind.SupplyEquipment) {
                    var tool=tools[item.LinkedId];tools[item.LinkedId]=new SupplyCacheEquipmentRecord(tool.Id,tool.Kind,tool.OwnerId,location,item.CustodianId);
                }
            }
            s.Work=new WorkLedger(s.Work.Lots.Select(x=>lots[x.Id]),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Select(x=>inventory[x.LotId]).ToArray();
            s.Vessels=s.Vessels.Select(x=>vessels[x.Id]).ToArray();
            s.SupplyCacheEquipment=s.SupplyCacheEquipment.Select(x=>tools[x.Id]).ToArray();
        }
        public static bool FixtureFitValid(Snapshot s,PortableEquipmentRecord pack)
        {
            if(pack.Id!=PortableKitFixture.Pack||pack.ProfileId!="adventuring-gear.backpack"||pack.FitRuleId!=PortableKitFixture.FitRule
                ||pack.CapacityPounds!=new RuleQuantity(30)||pack.CapacityCubicFeet!=new RuleQuantity(1)
                ||!pack.FitMemberIds.OrderBy(x=>x,StringComparer.Ordinal).SequenceEqual(PortableKitFixture.FitMembers.OrderBy(x=>x,StringComparer.Ordinal)))return false;
            return true;
        }
        internal static bool FitsCarrier(Snapshot s,string actor)
        {
            var burden=CarriedBurden(s,actor);return burden.Pounds.HasValue&&burden.Load.HasValue
                &&PlaytestCarrying.CanCarry(PlaytestCarrying.Limits(CarrierSize.Medium,10),burden)==true;
        }
        internal static void RegisterInventoryLot(Snapshot s,string lotId,string location,string custodian)
        {
            if(s.SchemaVersion<Snapshot.PortableEquipmentSchema||s.PortableEquipment.Any(x=>x.LinkedId==lotId))return;
            var item=s.InventoryLots.Single(x=>x.LotId==lotId);var lot=s.Work.Lots.Single(x=>x.Id==lotId);
            bool genericPounds=item.Nutrition==NutritionKind.None&&lot.UnitId=="mass-pound";
            var countedProfiles=item.Nutrition==NutritionKind.None
                ?s.PortableStorageProfiles.Where(x=>x.QuantityUnitId==lot.UnitId&&x.MassPerUnitLb.HasValue
                    &&(x.ProfileId!=ConnectedBloodSpecimen.MaterialProfile||s.BloodSpecimen?.LotId==lotId)).ToArray()
                :Array.Empty<PortableStorageProfileRecord>();
            if(countedProfiles.Length>1)throw new ArgumentException("Counted lot unit has ambiguous physical profiles.");
            bool counted=countedProfiles.Length==1;
            if(item.Nutrition==NutritionKind.None&&!genericPounds&&!counted)return;
            string parent="";PortablePlacement placement=PortablePlacement.Carried;
            if(location!=custodian) {
                var holder=s.PortableEquipment.SingleOrDefault(x=>x.Id==location&&(x.CapacityPounds.HasValue||x.LinkKind==PortableLinkKind.WaterVessel));
                if(holder==null)return;
                parent=holder.Id;placement=PortablePlacement.Contained;
            }
            var basis=counted?PortableMassBasis.CountedQuantity:genericPounds?PortableMassBasis.GenericPounds:item.Nutrition==NutritionKind.FoodPounds
                ?PortableMassBasis.FoodPounds:PortableMassBasis.WaterPints;
            string root=item.LotId;var lineage=new HashSet<string>(StringComparer.Ordinal);
            while(true) {
                var current=s.InventoryLots.Single(x=>x.LotId==root);
                if(current.ParentId=="")break;
                if(!lineage.Add(current.ParentId))throw new ArgumentException("Inventory portion cycle.");
                root=current.ParentId;
            }
            string profile=counted?countedProfiles[0].ProfileId:genericPounds?"prototype.generic-pound-lot":item.Nutrition==NutritionKind.WaterPints?"prototype.potable-water.pint"
                :root==PortableKitFixture.Rations?"adventuring-gear.rations-1-day":"prototype.food-lot";
            var physical=new PortableEquipmentRecord(lotId,profile,item.OwnerId,custodian,parent,placement,PortableLinkKind.InventoryLot,lotId,basis,
                counted?null:lot.Amount,null);
            s.PortableEquipment=s.PortableEquipment.Concat(new[]{physical}).ToArray();
        }
    }
}
#endif
