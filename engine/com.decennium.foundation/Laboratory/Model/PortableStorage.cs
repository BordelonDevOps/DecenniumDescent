#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Finite TEST_ONLY physical fit and packed-volume facts for MGT-01. These authored
    /// dimensions admit only the selected camp, crate, food and water profiles.</summary>
    public sealed class TestOnlyPortableStorageFixture
    {
        public const string CrateId = "TEST_ONLY.storage-crate";
        public const string CrateProfileId = "TEST_ONLY.storage-crate";
        private const string ItemUnit = "item";
        private const string CampPackProfileId = TestOnlyExpeditionCampConstructionFixture.PackProfileId;

        private static PortableStorageProfileRecord[] Definitions() => new[] {
            new PortableStorageProfileRecord(CampPackProfileId, "mass-pound", null,
                new[]{"adventuring-gear.rations-1-day","adventuring-gear.waterskin","prototype.food-lot"}, true),
            new PortableStorageProfileRecord(CrateProfileId, ItemUnit, null,
                new[]{"adventuring-gear.rations-1-day","prototype.food-lot"}),
            new PortableStorageProfileRecord("adventuring-gear.rations-1-day", TestOnlyInventoryPolicy.FoodUnit,
                new RuleQuantity(1,100)),
            new PortableStorageProfileRecord("adventuring-gear.waterskin", ItemUnit,
                new RuleQuantity(1,5), new[]{TestOnlyInventoryPolicy.WaterUnit}),
            new PortableStorageProfileRecord("prototype.food-lot", TestOnlyInventoryPolicy.FoodUnit,
                new RuleQuantity(1,100)),
            new PortableStorageProfileRecord(TestOnlyInventoryPolicy.WaterUnit, TestOnlyInventoryPolicy.WaterUnit,
                new RuleQuantity(1,100))
        };

        private static PortableStorageProfileRecord[] Recipe347Definitions()
        {
            var baseProfiles=Definitions();
            var componentProfiles=Enumerable.Range(0,TestOnlyRecipe347Fixture.ComponentLotIds.Length).Select(i=>
                new PortableStorageProfileRecord(CountedProfileId(TestOnlyRecipe347Fixture.ComponentUnitIds[i]),
                    TestOnlyRecipe347Fixture.ComponentUnitIds[i],TestOnlyRecipe347Fixture.ComponentVolumes[i],
                    massPerUnitLb:TestOnlyRecipe347Fixture.ComponentMasses[i]));
            var fixedAndBodyProfiles=new[]{
                new PortableStorageProfileRecord(TestOnlyRecipe347Fixture.BodyProfileId,"mass-pound",new RuleQuantity(1,25)),
                new PortableStorageProfileRecord("tools.miners-supplies","item",new RuleQuantity(1,2)),
                new PortableStorageProfileRecord("tools.assayers-supplies","item",new RuleQuantity(1,5)),
                new PortableStorageProfileRecord("TEST_ONLY.mining-pick","item",new RuleQuantity(3,10))
            };
            string[] additions=componentProfiles.Select(x=>x.ProfileId).Concat(fixedAndBodyProfiles.Select(x=>x.ProfileId)).ToArray();
            var crate=baseProfiles.Single(x=>x.ProfileId==CrateProfileId);
            var expandedCrate=new PortableStorageProfileRecord(crate.ProfileId,crate.QuantityUnitId,crate.PackedVolumePerUnitCubicFeet,
                crate.AllowedContainedProfileIds.Concat(additions).ToArray(),crate.RequiresInstalledTemporaryCamp);
            return baseProfiles.Select(x=>x.ProfileId==CrateProfileId?expandedCrate:x)
                .Concat(componentProfiles).Concat(fixedAndBodyProfiles).ToArray();
        }

        internal static string CountedProfileId(string unitId)=>"TEST_ONLY.recipe347.profile."+unitId;

        internal static void AppendRecipe347Profiles(Snapshot s)
        {
            if(s.SchemaVersion!=Snapshot.PortableCountedLotSchema)
                throw new ArgumentException("Counted portable stock requires schema73.");
            if(s.PortableStorageProfiles.Any(x=>x.MassPerUnitLb.HasValue))
                throw new ArgumentException("Counted portable profiles are already installed.");
            s.PortableStorageProfiles=Recipe347Definitions();
        }

        internal string Canonical => "MGT-01|schema71|source=46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|"
            + "FL-05|FL-07|BODY_EQUIPMENT_PLAYTEST|EQUIPMENT_ACQUISITION_PLAYTEST|"
            + "explicit-test-only-profile-volumes|camp=20-load-200lb-20ft3|"
            + "crate=50lb-2ft3|food=0.01ft3-per-pound|waterskin=0.2ft3-per-item|"
            + "water=0.01ft3-per-pint|printed-load-then-known-pounds-divided-by-ten|"
            + string.Join(";", Definitions().OrderBy(x=>x.ProfileId,StringComparer.Ordinal).Select(ProfileKey));

        internal string BindFingerprint(string prior)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.portable-storage-v1-"
                +string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+Canonical))
                    .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }

        internal void Initialize(Snapshot s)
        {
            if((s.SchemaVersion<Snapshot.PortableStorageSchema||s.SchemaVersion>Snapshot.PortableCountedLotSchema)||s.ExpeditionCampSites.Length!=1
                ||s.PortableEquipment.Any(x=>x.Id==CrateId))
                throw new ArgumentException("Portable storage requires the selected schema71 camp fixture.");
            var site=s.ExpeditionCampSites.Single();
            string actor=TestOnlyPolicy.ActorId;
            s.PortableStorageProfiles=Definitions();
            s.PortableEquipment=s.PortableEquipment.Concat(new[]{new PortableEquipmentRecord(CrateId,CrateProfileId,
                actor,actor,"",PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,
                new RuleQuantity(5),new RuleQuantity(5),capacityPounds:new RuleQuantity(50),
                capacityCubicFeet:new RuleQuantity(2),open:true,groundX:site.RouteX,groundY:site.RouteY)}).ToArray();
        }

        internal string ValidateSnapshot(Snapshot s)
        {
            var definitions=s.SchemaVersion>=Snapshot.PortableCountedLotSchema?Recipe347Definitions():Definitions();
            if((s.SchemaVersion<Snapshot.PortableStorageSchema||s.SchemaVersion>Snapshot.PortableCountedLotSchema)||!s.TestOnly
                ||!s.PortableStorageProfiles.Select(ProfileKey).OrderBy(x=>x,StringComparer.Ordinal)
                    .SequenceEqual(definitions.Select(ProfileKey).OrderBy(x=>x,StringComparer.Ordinal),StringComparer.Ordinal))
                return "PortableStorageProfileMismatch";
            var site=s.ExpeditionCampSites.SingleOrDefault();
            var crate=s.PortableEquipment.SingleOrDefault(x=>x.Id==CrateId);
            var crateCustodians=new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId};
            if(site==null||crate==null||crate.ProfileId!=CrateProfileId||crate.OwnerId!=TestOnlyPolicy.ActorId
                ||!crateCustodians.Contains(crate.CustodianId,StringComparer.Ordinal)||crate.ParentId!=""
                ||crate.Placement!=PortablePlacement.Ground&&crate.Placement!=PortablePlacement.Carried
                ||crate.LinkKind!=PortableLinkKind.None||crate.MassBasis!=PortableMassBasis.Fixed
                ||crate.SourceWeightLb!=new RuleQuantity(5)||crate.OperationalWeightLb!=new RuleQuantity(5)
                ||crate.CapacityPounds!=new RuleQuantity(50)||crate.CapacityCubicFeet!=new RuleQuantity(2))
                return "PortableStorageCrateFixtureMismatch";
            return null;
        }

        private static string ProfileKey(PortableStorageProfileRecord x)
            =>x.ProfileId+"|"+x.QuantityUnitId+"|"+(x.PackedVolumePerUnitCubicFeet.HasValue
                    ?x.PackedVolumePerUnitCubicFeet.Value.Numerator.ToString(CultureInfo.InvariantCulture)+"/"
                        +x.PackedVolumePerUnitCubicFeet.Value.Denominator.ToString(CultureInfo.InvariantCulture):"?")+"|"
                +string.Join(",",x.AllowedContainedProfileIds.OrderBy(id=>id,StringComparer.Ordinal))+"|"+x.RequiresInstalledTemporaryCamp
                +(x.MassPerUnitLb.HasValue?"|mass="+x.MassPerUnitLb.Value.Numerator.ToString(CultureInfo.InvariantCulture)+"/"
                    +x.MassPerUnitLb.Value.Denominator.ToString(CultureInfo.InvariantCulture):"");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyPortableStorageFixture portableStorageFixture;

        public TestOnlySharedWorldPolicy EnablePortableStorage(TestOnlyPortableStorageFixture fixture)
        {
            if(initializationStarted)throw new InvalidOperationException("World initialization has already started.");
            if(fixture==null||portableStorageFixture!=null)throw new ArgumentException("Supply one explicit portable-storage fixture.");
            if(portableKit==null||expeditionCampConstructionProfile==null||expeditionCampSiteProfile==null
                ||expeditionPressureProfile==null||routeTravelFixture==null)
                throw new InvalidOperationException("PortableStorageRequiresPortableKitAndTemporaryCampConstruction");
            portableStorageFixture=fixture;
            ContentFingerprint=fixture.BindFingerprint(ContentFingerprint);
            return this;
        }

        private void InitializePortableStorage(Snapshot s)
        {
            if(portableStorageFixture!=null)portableStorageFixture.Initialize(s);
        }

        private string ValidatePortableStorageState(Snapshot s)
            =>harvestPreservationTreatmentEnabled?ValidateHarvestPreservationTreatmentPortableProfiles(s)
                :harvestPreservationEnabled?ValidatePreservationPortableProfiles(s):portableStorageFixture==null
                ?s.PortableStorageProfiles.Length==0?null:"PortableStorageFixtureMissing"
                :portableStorageFixture.ValidateSnapshot(s);
    }
}
#endif
