#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>TEST_ONLY authoring bundle for an already-existing, physically present sample lot.
    /// No sample inventory is inferred or created by an assay profile.</summary>
    public sealed class MiningAssaySampleFixture
    {
        public MiningAssaySampleRecord Sample { get; }
        public ResourceLot PhysicalStock { get; }
        public InventoryLotRecord Provenance { get; }
        public PortableEquipmentRecord PhysicalItem { get; }

        public MiningAssaySampleFixture(MiningAssaySampleRecord sample, ResourceLot physicalStock,
            InventoryLotRecord provenance, PortableEquipmentRecord physicalItem)
        {
            Sample = sample ?? throw new ArgumentNullException(nameof(sample));
            PhysicalStock = physicalStock ?? throw new ArgumentNullException(nameof(physicalStock));
            Provenance = provenance ?? throw new ArgumentNullException(nameof(provenance));
            PhysicalItem = physicalItem ?? throw new ArgumentNullException(nameof(physicalItem));
            if (PhysicalStock.Id != Sample.InventoryLotId || PhysicalStock.UnitId != "mass-pound"
                || PhysicalStock.Amount != Sample.Amount || Provenance.LotId != Sample.InventoryLotId
                || Provenance.CreatedAmount != Sample.Amount || Provenance.Nutrition != NutritionKind.None
                || PhysicalItem.Id != Sample.Id || PhysicalItem.LinkKind != PortableLinkKind.InventoryLot
                || PhysicalItem.LinkedId != Sample.InventoryLotId || PhysicalItem.MassBasis != PortableMassBasis.GenericPounds)
                throw new ArgumentException("TEST_ONLY assay sample content must bind one exact physical inventory lot.");
        }

        internal string Key => string.Join("|", new[] { Sample.Id, Sample.DepositId, Sample.DepositVersionId,
            Sample.CategoryId, Sample.InventoryLotId, Sample.Amount.ToString(),
            string.Join(",", Sample.CompatibleMethodProfileIds.OrderBy(x=>x,StringComparer.Ordinal)), PhysicalStock.Id, PhysicalStock.UnitId,
            PhysicalStock.LocationId, PhysicalStock.CustodianId, PhysicalStock.Amount.ToString(), Provenance.OwnerId,
            Provenance.ParentId, Provenance.CreatedAt.ToString(), ((int)Provenance.Access).ToString(CultureInfo.InvariantCulture),
            PhysicalItem.Id, PhysicalItem.ProfileId, PhysicalItem.OwnerId, PhysicalItem.CustodianId,
            PhysicalItem.ParentId, ((int)PhysicalItem.Placement).ToString(CultureInfo.InvariantCulture),
            PhysicalItem.GroundX.ToString(CultureInfo.InvariantCulture), PhysicalItem.GroundY.ToString(CultureInfo.InvariantCulture) });
    }

    /// <summary>Versioned source and operational-policy identity included in assay-bearing save content.</summary>
    internal static class MiningAssayContentBinding
    {
        public const string Identity = "MGT-07.ASSAY.PROTOTYPE.2026-11-06.v1"
            + "|source-revision=46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
            + "|mining-guide-sha256=726cb84a1104901f5b05b412039b458af5bb5168e4482fb9e9844b1b42b697c3"
            + "|gathering-guide-sha256=9b1e4defcd18569ad8d8305552ad740e62be1faea3e1de448e364bd7536215bc"
            + "|policy-json-sha256=3b39253d850ffebd752c452ddbdefb7f4e7b25d6dda5d49046755d4ddead555f";
    }

    internal static class MiningToolContentBinding
    {
        public const string Identity="MGT-07.RECIPE-347.USE-PROTOTYPE.2026-11-06.v1"
            +"|source-revision=46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4"
            +"|mining-guide-sha256=726cb84a1104901f5b05b412039b458af5bb5168e4482fb9e9844b1b42b697c3"
            +"|gathering-guide-sha256=9b1e4defcd18569ad8d8305552ad740e62be1faea3e1de448e364bd7536215bc"
            +"|body-catalogue-sha256=23fb5db0282881499abcddaa3cd259bab4262a34c884e5a80c1de8a894c5dd99"
            +"|recipe-cards-sha256=c83b14b7df8475a1bdba05a69785e90dabcec5a12bb81cb722fa7737ab444a12"
            +"|public-data-sha256=121a396e18e7e294e26a469a42e434f70c24816659bc05c77f094fcbd9e06510";
    }

    /// <summary>One explicitly authored TEST_ONLY mining definition. These records are fixture
    /// inputs; the shared mining handler resolves them without content-specific identities.</summary>
    public sealed class MiningDepositFixtureContent
    {
        private readonly MiningCategoryRecord[] categories;
        private readonly MiningMaterialUnitRecord[] units;
        private readonly PortableEquipmentRecord[] physicalItems;
        private readonly ObjectStructureRecord[] workSurfaces;
        public MiningDepositRecord Deposit { get; }
        public MiningCategoryRecord[] Categories=>categories.ToArray();
        public MiningMaterialUnitRecord[] Units=>units.ToArray();
        public PortableEquipmentRecord[] PhysicalItems=>physicalItems.ToArray();
        public ObjectStructureRecord[] WorkSurfaces=>workSurfaces.ToArray();

        public MiningDepositFixtureContent(MiningDepositRecord deposit,MiningCategoryRecord[] categories,
            MiningMaterialUnitRecord[] units,PortableEquipmentRecord[] physicalItems,ObjectStructureRecord[] workSurfaces)
        {
            Deposit=deposit??throw new ArgumentNullException(nameof(deposit));
            if(categories==null||units==null||physicalItems==null||workSurfaces==null
                ||categories.Any(x=>x==null)||units.Any(x=>x==null)||physicalItems.Any(x=>x==null)||workSurfaces.Any(x=>x==null))
                throw new ArgumentException("Mining fixture content must contain initialized record arrays.");
            this.categories=categories.ToArray();this.units=units.ToArray();this.physicalItems=physicalItems.ToArray();this.workSurfaces=workSurfaces.ToArray();
            if(this.categories.Any(x=>x.DepositId!=deposit.Id)||this.units.Any(x=>x.DepositId!=deposit.Id)
                ||this.categories.SelectMany(x=>x.UnitIds).Distinct(StringComparer.Ordinal).Count()!=this.units.Length
                ||!this.categories.SelectMany(x=>x.UnitIds).OrderBy(x=>x,StringComparer.Ordinal)
                    .SequenceEqual(this.units.Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal))
                ||this.units.Any(x=>!this.categories.Any(c=>c.Id==x.CategoryId&&c.UnitIds.Contains(x.Id,StringComparer.Ordinal)))
                ||this.categories.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=this.categories.Length
                ||this.units.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=this.units.Length
                ||this.physicalItems.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=this.physicalItems.Length
                ||this.workSurfaces.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=this.workSurfaces.Length)
                throw new ArgumentException("Mining fixture records do not form one consistent authored deposit.");
        }

        internal string Key
        {
            get
            {
                var b=new StringBuilder();
                b.Append("deposit|").Append(Deposit.Id).Append('|').Append(Deposit.VersionId).Append('|').Append(Deposit.SiteId).Append('|')
                    .Append(Deposit.OwnerId).Append('|').Append(Deposit.SiteX).Append('|').Append(Deposit.SiteY).Append('|')
                    .Append(Deposit.MiningToolsId).Append('|').Append(Deposit.PickId).Append('|').Append(Deposit.ReceiverId).Append('|')
                    .Append(Deposit.WorkSurfaceId).Append('|').Append(Deposit.ExactCheckDc?.ToString(CultureInfo.InvariantCulture)??"-")
                    .Append('|').Append(Deposit.HurryFeasible);
                foreach(var x in categories.OrderBy(x=>x.Id,StringComparer.Ordinal))
                    b.Append("|category|").Append(x.Id).Append('|').Append(x.DepositId).Append('|').Append(x.MaterialId).Append('|')
                        .Append(x.Tier).Append('|').Append(x.Accessible).Append('|').Append(string.Join(",",x.UnitIds.OrderBy(v=>v,StringComparer.Ordinal)));
                foreach(var x in units.OrderBy(x=>x.Id,StringComparer.Ordinal))
                    b.Append("|unit|").Append(x.Id).Append('|').Append(x.DepositId).Append('|').Append(x.CategoryId).Append('|')
                        .Append(x.MassPounds).Append('|').Append(x.VolumeCubicFeet).Append('|')
                        .Append(x.ValueCopper?.ToString(CultureInfo.InvariantCulture)??"-").Append('|').Append((int)x.Condition).Append('|')
                        .Append((int)x.Status).Append('|').Append(x.ReceivedLotId).Append('|').Append(x.ReceivedContainerId);
                foreach(var x in physicalItems.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                    b.Append("|item|").Append(x.Id).Append('|').Append(x.ProfileId).Append('|').Append(x.OwnerId).Append('|').Append(x.CustodianId)
                        .Append('|').Append(x.ParentId).Append('|').Append((int)x.Placement).Append('|').Append((int)x.LinkKind).Append('|')
                        .Append(x.LinkedId).Append('|').Append((int)x.MassBasis).Append('|').Append(Q(x.SourceWeightLb)).Append('|')
                        .Append(Q(x.OperationalWeightLb)).Append('|').Append(Q(x.PrintedLoad)).Append('|').Append(Q(x.CapacityPounds)).Append('|')
                        .Append(Q(x.CapacityCubicFeet)).Append('|').Append(x.Wearable).Append('|').Append(x.Open).Append('|').Append(x.FitRuleId)
                        .Append('|').Append(string.Join(",",x.FitMemberIds.OrderBy(v=>v,StringComparer.Ordinal))).Append('|')
                        .Append(x.GroundX).Append('|').Append(x.GroundY).Append('|').Append(x.HeldHands);
                }
                foreach(var x in workSurfaces.OrderBy(x=>x.Id,StringComparer.Ordinal))
                    b.Append("|surface|").Append(x.Id).Append('|').Append(x.ProfileId).Append('|').Append(x.OwnerId).Append('|')
                        .Append(x.CustodianId).Append('|').Append(x.LocationId).Append('|').Append((int)x.Material).Append('|')
                        .Append(x.MaximumHp).Append('|').Append(x.Hp).Append('|').Append(x.BaselineCopper).Append('|').Append(x.MassPounds);
                return b.ToString();
            }
        }
        private static string Q(RuleQuantity? value)=>value.HasValue?value.Value.ToString():"-";
    }

    /// <summary>Authored TEST_ONLY exposed mineral content. It never generates geology or stock.</summary>
    public sealed class SharedMiningFixture
    {
        private readonly MiningDepositFixtureContent[] deposits;
        private readonly MiningAssayProfileRecord[] assayProfiles;
        private readonly MiningAssaySampleFixture[] assaySamples;
        private readonly DestructiveMiningAssayProfileRecord[] destructiveAssayProfiles;
        private readonly MineralPreparationProfileRecord[] mineralPreparationProfiles;
        private readonly MiningToolCandidateProfileRecord[] miningToolCandidateProfiles;
        private readonly MiningToolInstanceStateRecord[] miningToolInstanceStates;
        private readonly ObjectStructureRecord[] miningToolStructures;
        private readonly PortableEquipmentRecord[] miningToolItems;
        public const string DepositId="TEST_ONLY.mining.deposit";
        public const string DepositVersionId="TEST_ONLY.mining.deposit-v1";
        public const string SiteId="TEST_ONLY.mining.site";
        public const string OwnerId=TestOnlyPolicy.CompanionId;
        public const string CategoryA="TEST_ONLY.mining.category.iron";
        public const string CategoryB="TEST_ONLY.mining.category.copper";
        public const string UnitA="TEST_ONLY.mining.unit.iron";
        public const string UnitB="TEST_ONLY.mining.unit.copper";
        public const string MiningToolsId="TEST_ONLY.mining.tools";
        public const string PickId="TEST_ONLY.mining.pick";
        public const string ReceiverId="TEST_ONLY.mining.receiver";
        public const string SurfaceId="TEST_ONLY.mining.surface";
        public const string FitRuleId="TEST_ONLY.mining.receiver-fit-v1";
        public readonly bool Trained,HasMiningTools,HasPick,HasReceiver,HasWorkSurface,HurryFeasible;
        public readonly MiningUnitCondition UnitBCondition;
        public readonly int SiteX,SiteY;
        public MiningDepositFixtureContent[] Deposits=>deposits.ToArray();
        public MiningAssayProfileRecord[] AssayProfiles=>assayProfiles.ToArray();
        public MiningAssaySampleFixture[] AssaySamples=>assaySamples.ToArray();
        public DestructiveMiningAssayProfileRecord[] DestructiveAssayProfiles=>destructiveAssayProfiles.ToArray();
        public MineralPreparationProfileRecord[] MineralPreparationProfiles=>mineralPreparationProfiles.ToArray();
        public MiningToolCandidateProfileRecord[] MiningToolCandidateProfiles=>miningToolCandidateProfiles.ToArray();
        public MiningToolInstanceStateRecord[] MiningToolInstanceStates=>miningToolInstanceStates.ToArray();
        public ObjectStructureRecord[] MiningToolStructures=>miningToolStructures.ToArray();
        public PortableEquipmentRecord[] MiningToolItems=>miningToolItems.ToArray();
        public readonly int? Intelligence,Wisdom;
        private readonly string[] trainedWorkerIds;
        public bool HasExplicitTrainingRoster => trainedWorkerIds != null;
        public string[] TrainedWorkerIds => trainedWorkerIds?.ToArray();
        public SharedMiningFixture(bool trained=true,bool hasMiningTools=true,bool hasPick=true,bool hasReceiver=true,
            bool hasWorkSurface=true,bool hurryFeasible=false,int siteX=3,int siteY=3,
            MiningUnitCondition unitBCondition=MiningUnitCondition.Intact,int? intelligence=null,int? wisdom=null,
            MiningAssayProfileRecord[] assayProfiles=null, MiningAssaySampleFixture[] assaySamples=null,
            DestructiveMiningAssayProfileRecord[] destructiveAssayProfiles=null,
            MineralPreparationProfileRecord[] mineralPreparationProfiles=null,
            MiningToolCandidateProfileRecord[] miningToolCandidateProfiles=null,
            MiningToolInstanceStateRecord[] miningToolInstanceStates=null,ObjectStructureRecord[] miningToolStructures=null,
            PortableEquipmentRecord[] miningToolItems=null,string[] trainedWorkerIds=null)
        {
            if(siteX<0||siteY<0||!Enum.IsDefined(typeof(MiningUnitCondition),unitBCondition)
                ||intelligence.HasValue&&(intelligence.Value<1||intelligence.Value>30)
                ||wisdom.HasValue&&(wisdom.Value<1||wisdom.Value>30)
                ||trainedWorkerIds!=null&&(!trained||trainedWorkerIds.Any(x=>!Validation.ValidId(x))
                    ||trainedWorkerIds.Distinct(StringComparer.Ordinal).Count()!=trainedWorkerIds.Length))throw new ArgumentOutOfRangeException(nameof(siteX));
            Trained=trained;HasMiningTools=hasMiningTools;HasPick=hasPick;HasReceiver=hasReceiver;
            HasWorkSurface=hasWorkSurface;HurryFeasible=hurryFeasible;SiteX=siteX;SiteY=siteY;UnitBCondition=unitBCondition;
            Intelligence=intelligence;Wisdom=wisdom;this.trainedWorkerIds=trainedWorkerIds?.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            deposits=new[]{DefaultContent(siteX,siteY,hasMiningTools,hasPick,hasReceiver,hasWorkSurface,hurryFeasible,unitBCondition)};
            this.assayProfiles=ValidateAssayProfiles(assayProfiles);
            this.assaySamples=ValidateAssaySamples(assaySamples);
            this.destructiveAssayProfiles=ValidateDestructiveAssayProfiles(destructiveAssayProfiles);
            this.mineralPreparationProfiles=ValidateMineralPreparationProfiles(mineralPreparationProfiles);
            this.miningToolStructures=ValidateMiningToolStructures(miningToolStructures);
            this.miningToolItems=ValidateMiningToolItems(miningToolItems);
            this.miningToolCandidateProfiles=ValidateMiningToolCandidateProfiles(miningToolCandidateProfiles);
            this.miningToolInstanceStates=ValidateMiningToolInstanceStates(miningToolInstanceStates);
            ValidateAssayProfileIdentity();
        }
        public SharedMiningFixture(IEnumerable<MiningDepositFixtureContent> deposits,bool trained=true,int? intelligence=null,int? wisdom=null,
            MiningAssayProfileRecord[] assayProfiles=null, MiningAssaySampleFixture[] assaySamples=null,
            DestructiveMiningAssayProfileRecord[] destructiveAssayProfiles=null,
            MineralPreparationProfileRecord[] mineralPreparationProfiles=null,
            MiningToolCandidateProfileRecord[] miningToolCandidateProfiles=null,
            MiningToolInstanceStateRecord[] miningToolInstanceStates=null,ObjectStructureRecord[] miningToolStructures=null,
            PortableEquipmentRecord[] miningToolItems=null,string[] trainedWorkerIds=null)
        {
            if(deposits==null)throw new ArgumentNullException(nameof(deposits));
            var authored=deposits.ToArray();
            if(authored.Length<1||authored.Any(x=>x==null)||authored.Select(x=>x.Deposit.Id).Distinct(StringComparer.Ordinal).Count()!=authored.Length
                ||authored.SelectMany(x=>x.Categories).Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=authored.SelectMany(x=>x.Categories).Count()
                ||authored.SelectMany(x=>x.Units).Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=authored.SelectMany(x=>x.Units).Count()
                ||authored.SelectMany(x=>x.PhysicalItems).Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=authored.SelectMany(x=>x.PhysicalItems).Count()
                ||authored.SelectMany(x=>x.WorkSurfaces).Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=authored.SelectMany(x=>x.WorkSurfaces).Count()
                ||intelligence.HasValue&&(intelligence.Value<1||intelligence.Value>30)
                ||wisdom.HasValue&&(wisdom.Value<1||wisdom.Value>30)
                ||trainedWorkerIds!=null&&(!trained||trainedWorkerIds.Any(x=>!Validation.ValidId(x))
                    ||trainedWorkerIds.Distinct(StringComparer.Ordinal).Count()!=trainedWorkerIds.Length))throw new ArgumentException("Invalid authored mining fixture set.",nameof(deposits));
            this.deposits=authored;
            Trained=trained;HasMiningTools=authored.All(x=>x.PhysicalItems.Any(i=>i.Id==x.Deposit.MiningToolsId));
            HasPick=authored.All(x=>x.PhysicalItems.Any(i=>i.Id==x.Deposit.PickId));
            HasReceiver=authored.All(x=>x.PhysicalItems.Any(i=>i.Id==x.Deposit.ReceiverId));
            HasWorkSurface=authored.All(x=>x.WorkSurfaces.Any(i=>i.Id==x.Deposit.WorkSurfaceId));
            HurryFeasible=authored.Any(x=>x.Deposit.HurryFeasible);UnitBCondition=authored.SelectMany(x=>x.Units)
                .SingleOrDefault(x=>x.Id==UnitB)?.Condition??MiningUnitCondition.Intact;
            SiteX=authored[0].Deposit.SiteX;SiteY=authored[0].Deposit.SiteY;
            Intelligence=intelligence;Wisdom=wisdom;this.trainedWorkerIds=trainedWorkerIds?.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            this.assayProfiles=ValidateAssayProfiles(assayProfiles);
            this.assaySamples=ValidateAssaySamples(assaySamples);
            this.destructiveAssayProfiles=ValidateDestructiveAssayProfiles(destructiveAssayProfiles);
            this.mineralPreparationProfiles=ValidateMineralPreparationProfiles(mineralPreparationProfiles);
            this.miningToolStructures=ValidateMiningToolStructures(miningToolStructures);
            this.miningToolItems=ValidateMiningToolItems(miningToolItems);
            this.miningToolCandidateProfiles=ValidateMiningToolCandidateProfiles(miningToolCandidateProfiles);
            this.miningToolInstanceStates=ValidateMiningToolInstanceStates(miningToolInstanceStates);
            ValidateAssayProfileIdentity();
        }
        internal string Key=>"TEST_ONLY.exposed-minerals-v1|"+Trained+"|"+HasMiningTools+"|"+HasPick+"|"+HasReceiver
            +"|"+HasWorkSurface+"|"+HurryFeasible+"|"+SiteX.ToString(CultureInfo.InvariantCulture)+","+SiteY.ToString(CultureInfo.InvariantCulture)
            +"|"+((int)UnitBCondition).ToString(CultureInfo.InvariantCulture)+"|"+(Intelligence?.ToString(CultureInfo.InvariantCulture)??"-")
            +"|"+(Wisdom?.ToString(CultureInfo.InvariantCulture)??"-")+"|"+string.Join("||",deposits.OrderBy(x=>x.Deposit.Id,StringComparer.Ordinal).Select(x=>x.Key))
            +(assayProfiles.Length==0?"":"|assay|"+string.Join("||",assayProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal).Select(AssayProfileKey)))
            +(assaySamples.Length==0?"":"|assay-samples|"+string.Join("||",assaySamples.OrderBy(x=>x.Sample.Id,StringComparer.Ordinal).Select(x=>x.Key)))
            +(destructiveAssayProfiles.Length==0?"":"|destructive-assay|"+string.Join("||",destructiveAssayProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal)
                .Select(x=>x.Id+"|"+x.SampleId+"|"+x.MethodProfileId+"|"+x.SampleAmount)))
            +(mineralPreparationProfiles.Length==0?"":"|mineral-preparation|"+string.Join("||",mineralPreparationProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal)
                .Select(x=>x.Id+"|"+x.UnitId+"|"+x.GangueWastePounds+"|"+x.DressedItemProfileId+"|"+x.GangueItemProfileId)))
            +(miningToolCandidateProfiles.Length==0?"":"|mining-tool-profile|"+MiningToolContentBinding.Identity+"|"+string.Join("||",miningToolCandidateProfiles.OrderBy(x=>x.Id,StringComparer.Ordinal)
                .Select(x=>x.Id+"|"+x.DepositId+"|"+x.ToolItemId+"|"+x.ToolItemProfileId+"|"+x.StructureId+"|"+x.StructureProfileId
                    +"|"+x.PreparationProfileId+"|"+x.PreparationUnitId+"|"+x.ReserveUnitId)))
            +(miningToolInstanceStates.Length==0?"":"|mining-tool-state|"+string.Join("||",miningToolInstanceStates.OrderBy(x=>x.ProfileId,StringComparer.Ordinal)
                .Select(x=>x.ProfileId+"|"+x.ToolItemId+"|"+string.Join(",",x.MissingMemberIds)+"|"+x.Suppressed+"|"+x.Melded)))
            +(miningToolStructures.Length==0?"":"|mining-tool-structure|"+string.Join("||",miningToolStructures.OrderBy(x=>x.Id,StringComparer.Ordinal)
                .Select(x=>x.Id+"|"+x.ProfileId+"|"+x.OwnerId+"|"+x.CustodianId+"|"+x.LocationId+"|"+((int)x.Material).ToString(CultureInfo.InvariantCulture)
                    +"|"+x.MaximumHp.ToString(CultureInfo.InvariantCulture)+"|"+x.Hp.ToString(CultureInfo.InvariantCulture)+"|"+x.MassPounds)))
            +(miningToolItems.Length==0?"":"|mining-tool-item|"+string.Join("||",miningToolItems.OrderBy(x=>x.Id,StringComparer.Ordinal)
                .Select(x=>x.Id+"|"+x.ProfileId+"|"+x.OwnerId+"|"+x.CustodianId+"|"+x.GroundX.ToString(CultureInfo.InvariantCulture)
                    +"|"+x.GroundY.ToString(CultureInfo.InvariantCulture)+"|"+Q(x.SourceWeightLb)+"|"+Q(x.OperationalWeightLb))))
            +(assayProfiles.Length+assaySamples.Length+destructiveAssayProfiles.Length==0?"":"|assay-source-policy|"+MiningAssayContentBinding.Identity)
            +(trainedWorkerIds==null?"":"|trained-workers|"+string.Join(";",trainedWorkerIds));
        private static string Q(RuleQuantity? value)=>value.HasValue?value.Value.ToString():"-";

        private void ValidateAssayProfileIdentity()
        {
            string[] ids=assayProfiles.Select(x=>x.Id).Concat(destructiveAssayProfiles.Select(x=>x.Id)).ToArray();
            if(ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length)
                throw new ArgumentException("Nondestructive and destructive assay profile IDs must be globally unique.");
        }

        private static string AssayProfileKey(MiningAssayProfileRecord x)
            =>string.Join("|",new[]{x.Id,x.DepositId,x.DepositVersionId,x.ExactSourceDc?.ToString(CultureInfo.InvariantCulture)??"-",
                x.RequiredHands.ToString(CultureInfo.InvariantCulture),string.Join(",",x.AssessedCategoryIds),string.Join(",",x.RequiredImplementIds),
                string.Join("||",x.Findings.OrderBy(f=>f.Id,StringComparer.Ordinal).Select(f=>string.Join("|",new[]{f.Id,f.CategoryId,
                    ((int)f.Kind).ToString(CultureInfo.InvariantCulture),f.Fact}))) });

        private MiningAssayProfileRecord[] ValidateAssayProfiles(MiningAssayProfileRecord[] profiles)
        {
            var values=profiles??Array.Empty<MiningAssayProfileRecord>();
            if(values.Any(x=>x==null)||values.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=values.Length)
                throw new ArgumentException("Invalid mining assay profiles.",nameof(profiles));
            foreach(var profile in values) {
                var content=deposits.SingleOrDefault(x=>x.Deposit.Id==profile.DepositId&&x.Deposit.VersionId==profile.DepositVersionId);
                if(content==null||profile.AssessedCategoryIds.Any(id=>!content.Categories.Any(x=>x.Id==id&&x.Accessible))
                    ||profile.RequiredImplementIds.Any(id=>!content.PhysicalItems.Any(x=>x.Id==id)))
                    throw new ArgumentException("Mining assay profile does not bind to its authored manifest.",nameof(profiles));
                int[] tiers=content.Categories.Where(x=>profile.AssessedCategoryIds.Contains(x.Id,StringComparer.Ordinal)).Select(x=>x.Tier).ToArray();
                if(!profile.ExactSourceDc.HasValue&&tiers.Any(x=>x<1))
                    throw new ArgumentException("An exact source DC is required when the assay profile includes an unknown tier.",nameof(profiles));
            }
            return values.OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray();
        }

        private MiningAssaySampleFixture[] ValidateAssaySamples(MiningAssaySampleFixture[] samples)
        {
            var values=samples??Array.Empty<MiningAssaySampleFixture>();
            if(values.Any(x=>x==null)||values.Select(x=>x.Sample.Id).Distinct(StringComparer.Ordinal).Count()!=values.Length
                ||values.Select(x=>x.Sample.InventoryLotId).Distinct(StringComparer.Ordinal).Count()!=values.Length)
                throw new ArgumentException("Invalid authored physical assay samples.",nameof(samples));
            foreach(var value in values) {
                var deposit=deposits.SingleOrDefault(x=>x.Deposit.Id==value.Sample.DepositId&&x.Deposit.VersionId==value.Sample.DepositVersionId);
                if(deposit==null||!deposit.Categories.Any(x=>x.Id==value.Sample.CategoryId&&x.Accessible)
                    ||value.Provenance.OwnerId!=deposit.Deposit.OwnerId||value.PhysicalStock.CustodianId!=deposit.Deposit.OwnerId
                    ||value.PhysicalItem.OwnerId!=deposit.Deposit.OwnerId||value.PhysicalItem.CustodianId!=deposit.Deposit.OwnerId
                    ||value.PhysicalItem.Placement!=PortablePlacement.Ground
                    ||value.PhysicalItem.GroundX!=deposit.Deposit.SiteX||value.PhysicalItem.GroundY!=deposit.Deposit.SiteY
                    ||value.PhysicalStock.LocationId!="ground."+deposit.Deposit.SiteX.ToString(CultureInfo.InvariantCulture)+"."+deposit.Deposit.SiteY.ToString(CultureInfo.InvariantCulture))
                    throw new ArgumentException("TEST_ONLY sample does not physically match its authored deposit.",nameof(samples));
                foreach(string methodId in value.Sample.CompatibleMethodProfileIds) {
                    var method=assayProfiles.SingleOrDefault(x=>x.Id==methodId);
                    if(method==null||method.DepositId!=deposit.Deposit.Id||method.DepositVersionId!=deposit.Deposit.VersionId
                        ||!method.AssessedCategoryIds.Contains(value.Sample.CategoryId,StringComparer.Ordinal))
                        throw new ArgumentException("TEST_ONLY sample compatibility does not match an authored assay method.",nameof(samples));
                }
            }
            return values.OrderBy(x=>x.Sample.Id,StringComparer.Ordinal).ToArray();
        }

        private DestructiveMiningAssayProfileRecord[] ValidateDestructiveAssayProfiles(DestructiveMiningAssayProfileRecord[] profiles)
        {
            var values=profiles??Array.Empty<DestructiveMiningAssayProfileRecord>();
            if(values.Any(x=>x==null)||values.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=values.Length)
                throw new ArgumentException("Invalid destructive assay profiles.",nameof(profiles));
            foreach(var profile in values) {
                var sample=assaySamples.SingleOrDefault(x=>x.Sample.Id==profile.SampleId)?.Sample;
                var method=assayProfiles.SingleOrDefault(x=>x.Id==profile.MethodProfileId);
                if(sample==null||method==null||profile.SampleAmount!=sample.Amount
                    ||!sample.CompatibleMethodProfileIds.Contains(method.Id,StringComparer.Ordinal))
                    throw new ArgumentException("Destructive assay profile lacks an explicitly sufficient compatible sample.",nameof(profiles));
            }
            return values.OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray();
        }

        private MineralPreparationProfileRecord[] ValidateMineralPreparationProfiles(MineralPreparationProfileRecord[] profiles)
        {
            var values=profiles??Array.Empty<MineralPreparationProfileRecord>();
            if(values.Any(x=>x==null)||values.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=values.Length
                ||values.Select(x=>x.UnitId).Distinct(StringComparer.Ordinal).Count()!=values.Length)
                throw new ArgumentException("Invalid mineral preparation profiles.",nameof(profiles));
            foreach(var profile in values) {
                var unit=deposits.SelectMany(x=>x.Units).SingleOrDefault(x=>x.Id==profile.UnitId);
                if(unit==null||unit.Condition!=MiningUnitCondition.Intact||unit.MassPounds>new RuleQuantity(1)
                    ||profile.GangueWastePounds>=unit.MassPounds)
                    throw new ArgumentException("Mineral preparation content must bind an ordinary intact unit no heavier than one pound and conserve positive retained mass.",nameof(profiles));
            }
            return values.OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray();
        }

        private ObjectStructureRecord[] ValidateMiningToolStructures(ObjectStructureRecord[] structures)
        {
            var values=structures??Array.Empty<ObjectStructureRecord>();
            if(values.Any(x=>x==null)||values.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=values.Length)
                throw new ArgumentException("Invalid mining-tool structures.",nameof(structures));
            return values.OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray();
        }

        private PortableEquipmentRecord[] ValidateMiningToolItems(PortableEquipmentRecord[] items)
        {
            var values=items??Array.Empty<PortableEquipmentRecord>();
            if(values.Any(x=>x==null)||values.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=values.Length
                ||values.Any(x=>x.Placement!=PortablePlacement.Ground||x.ParentId!=""||x.LinkKind!=PortableLinkKind.None))
                throw new ArgumentException("Mining-tool candidate fixtures must be distinct actual ground equipment bodies.",nameof(items));
            return values.OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray();
        }

        private MiningToolCandidateProfileRecord[] ValidateMiningToolCandidateProfiles(MiningToolCandidateProfileRecord[] profiles)
        {
            var values=profiles??Array.Empty<MiningToolCandidateProfileRecord>();
            if(values.Any(x=>x==null)||values.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=values.Length
                ||values.Select(x=>x.DepositId).Distinct(StringComparer.Ordinal).Count()!=values.Length)
                throw new ArgumentException("Invalid mining-tool candidate profiles.",nameof(profiles));
            foreach(var profile in values) {
                var content=deposits.SingleOrDefault(x=>x.Deposit.Id==profile.DepositId);
                var item=content==null?null:content.PhysicalItems.Concat(miningToolItems).SingleOrDefault(x=>x.Id==profile.ToolItemId);
                var structure=miningToolStructures.SingleOrDefault(x=>x.Id==profile.StructureId);
                if(content==null||item!=null&&item.ProfileId!=profile.ToolItemProfileId
                    ||structure!=null&&structure.ProfileId!=profile.StructureProfileId
                    ||profile.ReserveUnitId!=""&&(!content.Units.Any(x=>x.Id==profile.ReserveUnitId&&x.Condition==MiningUnitCondition.Intact)
                        ||!content.Categories.Any(c=>c.Accessible&&c.UnitIds.Contains(profile.ReserveUnitId,StringComparer.Ordinal)))
                    ||profile.PreparationProfileId!=""&&(!mineralPreparationProfiles.Any(x=>x.Id==profile.PreparationProfileId
                        &&x.UnitId==profile.PreparationUnitId)||!content.Units.Any(x=>x.Id==profile.PreparationUnitId)))
                    throw new ArgumentException("Mining-tool profile does not bind to an actual authored body, mineral unit and preparation profile.",nameof(profiles));
            }
            return values.OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray();
        }

        private MiningToolInstanceStateRecord[] ValidateMiningToolInstanceStates(MiningToolInstanceStateRecord[] states)
        {
            var values=states??miningToolCandidateProfiles.Select(x=>new MiningToolInstanceStateRecord(x.Id,x.ToolItemId)).ToArray();
            if(values.Any(x=>x==null)||values.Select(x=>x.ProfileId).Distinct(StringComparer.Ordinal).Count()!=values.Length
                ||values.Any(x=>{
                    var profile=miningToolCandidateProfiles.SingleOrDefault(p=>p.Id==x.ProfileId);
                    return profile==null||profile.ToolItemId!=x.ToolItemId
                        ||x.MissingMemberIds.Any(m=>!profile.RequiredMemberIds.Concat(profile.OptionalMemberIds).Contains(m,StringComparer.Ordinal));
                }))
                throw new ArgumentException("Mining-tool instance state does not match an authored candidate profile.",nameof(states));
            return values.OrderBy(x=>x.ProfileId,StringComparer.Ordinal).ToArray();
        }

        private static MiningDepositFixtureContent DefaultContent(int x,int y,bool hasTools,bool hasPick,bool hasReceiver,bool hasSurface,
            bool hurryFeasible,MiningUnitCondition unitBCondition)
        {
            string owner=OwnerId;var iron=new RuleQuantity(1);var copper=new RuleQuantity(1);
            var deposit=new MiningDepositRecord(DepositId,DepositVersionId,SiteId,owner,x,y,MiningToolsId,PickId,ReceiverId,SurfaceId,null,hurryFeasible);
            var categories=new[]{new MiningCategoryRecord(CategoryA,DepositId,"TEST_ONLY.mineral.iron-ore",1,true,new[]{UnitA}),
                new MiningCategoryRecord(CategoryB,DepositId,"TEST_ONLY.mineral.copper-ore",2,true,new[]{UnitB})};
            var units=new[]{new MiningMaterialUnitRecord(UnitA,DepositId,CategoryA,iron,RuleQuantity.FromFraction(1,50),10,
                    MiningUnitCondition.Intact,MiningUnitStatus.Available),
                new MiningMaterialUnitRecord(UnitB,DepositId,CategoryB,copper,RuleQuantity.FromFraction(1,40),20,
                    unitBCondition,MiningUnitStatus.Available)};
            var items=new List<PortableEquipmentRecord>{RawUnit(UnitA,owner,x,y,iron),RawUnit(UnitB,owner,x,y,copper)};
            if(hasTools)items.Add(GroundItem(MiningToolsId,"TEST_ONLY.mining.screen-and-tray",owner,x,y,new RuleQuantity(3)));
            if(hasPick)items.Add(GroundItem(PickId,"TEST_ONLY.mining-pick",owner,x,y,new RuleQuantity(10)));
            if(hasReceiver)items.Add(new PortableEquipmentRecord(ReceiverId,"TEST_ONLY.mining-receiver",owner,owner,"",PortablePlacement.Ground,
                PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(2),new RuleQuantity(2),capacityPounds:new RuleQuantity(50),
                capacityCubicFeet:new RuleQuantity(1),open:true,fitRuleId:FitRuleId,fitMemberIds:new[]{UnitA,UnitB},groundX:x,groundY:y));
            var surfaces=hasSurface?new[]{new ObjectStructureRecord(SurfaceId,"TEST_ONLY.stable-mining-work-surface",owner,owner,SiteId,
                ObjectMaterial.Stone,100,100,0,new RuleQuantity(20))}:Array.Empty<ObjectStructureRecord>();
            return new MiningDepositFixtureContent(deposit,categories,units,items.ToArray(),surfaces);
        }
        private static PortableEquipmentRecord RawUnit(string id,string owner,int x,int y,RuleQuantity amount)
            =>new PortableEquipmentRecord(id,"TEST_ONLY.mining.raw-unit",owner,owner,"",PortablePlacement.Ground,PortableLinkKind.InventoryLot,
                id,PortableMassBasis.GenericPounds,amount,null,groundX:x,groundY:y);
        private static PortableEquipmentRecord GroundItem(string id,string profile,string owner,int x,int y,RuleQuantity pounds)
            =>new PortableEquipmentRecord(id,profile,owner,owner,"",PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,
                pounds,pounds,groundX:x,groundY:y);
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private SharedMiningFixture miningFixture;
        private string MiningOwnerId=>OffCalendarWorkerId;
        private string[] MiningWorkerIds=>worldConfiguration?.Actors.Select(x=>x.Id).ToArray()??new[]{TestOnlyPolicy.CompanionId};
        private string[] MiningTrainingWorkerIds=>miningFixture==null||!miningFixture.Trained?Array.Empty<string>()
            :miningFixture.HasExplicitTrainingRoster?miningFixture.TrainedWorkerIds:MiningWorkerIds;
        private bool IsMiningWorker(string id)=>assignmentBindingProfile!=null
            ?assignmentBindingProfile.WorkerIds.Contains(id,StringComparer.Ordinal)
            :worldConfiguration==null?id==TestOnlyPolicy.CompanionId:worldConfiguration.Actors.Any(x=>x.Id==id);

        public static TestOnlySharedWorldPolicy WithMining(SharedMiningFixture fixture,uint seed=1,long enemyHp=26)
        {
            if(fixture==null)throw new ArgumentNullException(nameof(fixture));
            var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(enemyHp,seed),walkingSpeed:30);
            policy.miningFixture=fixture;
            using(var sha=SHA256.Create())policy.ContentFingerprint="TEST_ONLY.mining-v1-"+string.Concat(sha.ComputeHash(
                Encoding.UTF8.GetBytes(policy.ContentFingerprint+"|"+fixture.Key+"|seed="+seed.ToString(CultureInfo.InvariantCulture)))
                    .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
            return policy;
        }

        private void InitializeMining(Snapshot s)
        {
            if(miningFixture==null)return;
            s.MiningAssayProfiles=miningFixture.AssayProfiles;
            s.MiningAssaySamples=miningFixture.AssaySamples.Select(x=>x.Sample).ToArray();
            s.DestructiveMiningAssayProfiles=miningFixture.DestructiveAssayProfiles;
            s.MineralPreparationProfiles=miningFixture.MineralPreparationProfiles;
            s.MineralPreparationAttempts=Array.Empty<MineralPreparationAttemptRecord>();
            s.MiningToolCandidateProfiles=miningFixture.MiningToolCandidateProfiles;
            s.MiningToolInstanceStates=miningFixture.MiningToolInstanceStates;
            s.MiningToolUses=Array.Empty<MiningToolUseRecord>();
            if(miningFixture.Intelligence.HasValue||miningFixture.Wisdom.HasValue) {
                s.Characters=s.Characters.Select(x=>{
                    if(x.ActorId!=MiningOwnerId)return x;
                    int[] scores=x.Abilities.ToArray();if(miningFixture.Intelligence.HasValue)scores[3]=miningFixture.Intelligence.Value;
                    if(miningFixture.Wisdom.HasValue)scores[4]=miningFixture.Wisdom.Value;
                    return new ActorCharacterRecord(x.ActorId,x.ProfileId,scores,x.Levels);
                }).ToArray();
            }
            var trainedWorkers=MiningTrainingWorkerIds;
            if(trainedWorkers.Any(id=>!s.Actors.Any(a=>a.Id==id)))throw new InvalidOperationException("MiningTrainingWorkerNotControlled");
            s.SkillTraining=s.SkillTraining.Concat(trainedWorkers
                .Where(id=>!s.SkillTraining.Any(x=>x.ActorId==id&&x.SkillId=="mining-tools"))
                .Select(id=>new SkillTrainingRecord(id,"mining-tools",1))).ToArray();
            var authored=miningFixture.Deposits;
            var deposits=authored.Select(x=>x.Deposit).ToArray();
            var categories=authored.SelectMany(x=>x.Categories).ToArray();
            var units=authored.SelectMany(x=>x.Units).ToArray();
            var physical=authored.SelectMany(x=>x.PhysicalItems).ToArray();
            var surfaces=authored.SelectMany(x=>x.WorkSurfaces).ToArray();
            var depositById=deposits.ToDictionary(x=>x.Id,StringComparer.Ordinal);
            var lots=units.Select(x=>{
                var deposit=depositById[x.DepositId];
                string ground=GroundId(deposit.SiteX,deposit.SiteY);
                return new ResourceLot(x.Id,"mass-pound",x.MassPounds,ground,deposit.OwnerId);
            }).ToArray();
            var assayStock=miningFixture.AssaySamples.Select(x=>x.PhysicalStock).ToArray();
            s.Work=new WorkLedger(s.Work.Lots.Concat(lots).Concat(assayStock),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Concat(units.Select(x=>{
                var deposit=depositById[x.DepositId];
                return new InventoryLotRecord(x.Id,"",deposit.OwnerId,x.MassPounds,s.RuleClock,NutritionKind.None,null,InventoryAccess.Ground);
            })).Concat(miningFixture.AssaySamples.Select(x=>x.Provenance)).ToArray();
            s.MiningDeposits=s.MiningDeposits.Concat(deposits).ToArray();
            s.MiningCategories=s.MiningCategories.Concat(categories).ToArray();
            s.MiningUnits=s.MiningUnits.Concat(units).ToArray();
            s.PortableEquipment=s.PortableEquipment.Concat(physical).Concat(miningFixture.MiningToolItems)
                .Concat(miningFixture.AssaySamples.Select(x=>x.PhysicalItem)).ToArray();
            s.DestructiveMiningAssayAttempts=Array.Empty<DestructiveMiningAssayAttemptRecord>();
            s.Structures=s.Structures.Concat(surfaces).Concat(miningFixture.MiningToolStructures).ToArray();
        }

        private static string GroundId(int x,int y)=>"ground."+x.ToString(CultureInfo.InvariantCulture)+"."+y.ToString(CultureInfo.InvariantCulture);

        private static void PutMiningAttempt(Snapshot s,MiningAttemptRecord value)
            =>s.MiningAttempts=s.MiningAttempts.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void PutMiningUnit(Snapshot s,MiningMaterialUnitRecord value)
            =>s.MiningUnits=s.MiningUnits.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void PutMiningToolUse(Snapshot s,MiningToolUseRecord value)
            =>s.MiningToolUses=s.MiningToolUses.Select(x=>x.Id==value.Id?value:x).ToArray();
        private bool IsMiningCommand(Command c)=>miningFixture!=null&&(c.Kind==CommandKind.StartMining
            ||c.Kind==CommandKind.PauseMining||c.Kind==CommandKind.ResumeMining);
        private static RuleTime AddMiningTime(RuleTime first,RuleTime second)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)first.Numerator*second.Denominator
                +(System.Numerics.BigInteger)second.Numerator*first.Denominator,(System.Numerics.BigInteger)first.Denominator*second.Denominator);
        private static RuleTime MiningOverlap(RuleTime from,RuleTime to,RuleTime start,RuleTime end)
        {
            RuleTime left=from>start?from:start,right=to<end?to:end;
            return right>left?SubtractMiningTime(right,left):default;
        }
        private static RuleTime SubtractMiningTime(RuleTime first,RuleTime second)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)first.Numerator*second.Denominator
                -(System.Numerics.BigInteger)second.Numerator*first.Denominator,(System.Numerics.BigInteger)first.Denominator*second.Denominator);
        private static string MiningWorkId(long revision)=>"mining.extraction."+revision.ToString(CultureInfo.InvariantCulture);

        private static bool MiningWorkerBusy(Snapshot s,string actor,string exceptJob="")
            =>s.Work.WorkerIntervals.Any(x=>x.WorkerId==actor&&x.JobId!=exceptJob&&x.Start<=s.RuleClock&&x.End>s.RuleClock)
                ||WorldActivityProjection.CurrentWork(s).Any(x=>x.ActorId==actor&&x.Id!=exceptJob);

        private string MiningAccess(Snapshot s,string actor,MiningDepositRecord deposit,string exceptJob="",string[] selectedUnitIds=null)
        {
            if(miningFixture==null)return "MiningNotSelected";
            if(s.InventoryCombat&&s.WorldSchedule.Order.Contains(actor))return "MiningRequiresExploration";
            if(!IsMiningWorker(actor))return "MiningWorkerUnsupported";
            if(!CapableWorker(s,actor))return "MiningWorkerIncapable";
            if(s.WorldTraversals.Any(x=>x.ActorId==actor))return "MiningWorkerMoving";
            if(MiningWorkerBusy(s,actor,exceptJob))return "WorkerBusy";
            if(AvailableHands(s,actor)<2)return "TwoHandsRequired";
            var worker=s.Actors.Single(x=>x.Id==actor);
            if(!WorldSpatialQueries.WithinCardinalRange(worker.X,worker.Y,deposit.SiteX,deposit.SiteY,1))return "MiningWorksiteOutOfReach";
            PortableEquipmentRecord accessible(string id)=>s.PortableEquipment.SingleOrDefault(x=>x.Id==id
                &&x.CustodianId==deposit.OwnerId&&x.Placement==PortablePlacement.Ground&&x.GroundX==deposit.SiteX&&x.GroundY==deposit.SiteY
                &&PortableEquipmentRules.Accessible(s,actor,x));
            if(accessible(deposit.MiningToolsId)==null)return "MiningToolsUnavailable";
            if(accessible(deposit.PickId)==null)return "MiningPickUnavailable";
            var surface=s.Structures.SingleOrDefault(x=>x.Id==deposit.WorkSurfaceId&&x.LocationId==deposit.SiteId&&!x.Broken);
            if(surface==null)return "MiningWorkSurfaceUnavailable";
            var receiver=accessible(deposit.ReceiverId);
            if(receiver==null||!receiver.Open||!receiver.CapacityPounds.HasValue||!receiver.CapacityCubicFeet.HasValue
                ||receiver.FitRuleId=="")return "MiningReceiverUnavailable";
            string[] selected=selectedUnitIds??Array.Empty<string>();
            if(exceptJob!=""&&s.SchemaVersion>=Snapshot.MiningToolCandidateSchema) {
                var use=s.MiningToolUses.SingleOrDefault(x=>x.MiningAttemptId==exceptJob);
                if(use!=null&&use.ReservedUnitId!="")selected=selected.Concat(new[]{use.ReservedUnitId}).Distinct(StringComparer.Ordinal).ToArray();
            }
            var units=s.MiningUnits.Where(x=>x.DepositId==deposit.Id&&selected.Contains(x.Id,StringComparer.Ordinal)).ToArray();
            if(units.Length!=selected.Distinct(StringComparer.Ordinal).Count())return "MiningSelectionInvalid";
            foreach(var unit in units) {
                var body=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id);
                if(body==null||body.OwnerId!=deposit.OwnerId||body.CustodianId!=deposit.OwnerId
                    ||!PortableEquipmentValidation.FitsAuthoredMember(s,receiver,body))return "MiningReceiverFitUnavailable";
            }
            var existing=s.MiningUnits.Where(x=>x.Status==MiningUnitStatus.Extracted&&x.ReceivedContainerId==receiver.Id).ToArray();
            if(RuleQuantity.Sum(existing.Select(x=>x.MassPounds).Concat(units.Select(x=>x.MassPounds)))>receiver.CapacityPounds.Value)
                return "MiningReceiverCapacityInsufficient";
            if(RuleQuantity.Sum(existing.Select(x=>x.VolumeCubicFeet).Concat(units.Select(x=>x.VolumeCubicFeet)))>receiver.CapacityCubicFeet.Value)
                return "MiningReceiverVolumeInsufficient";
            if(!TestOnlyClubAttackPolicy.DamageConditionCapacity(s,actor))return "MiningConsequenceCapacityReached";
            return null;
        }

        private void BookMining(Snapshot s,MiningAttemptRecord attempt)
        {
            RuleTime remaining=SubtractMiningTime(new RuleTime(attempt.DurationSeconds),attempt.WorkDone);
            RuleTime end=AddMiningTime(s.RuleClock,remaining);
            int interval=s.Work.WorkerIntervals.Count(x=>x.JobId==attempt.Id);
            string intervalId=attempt.Id+".labor."+interval.ToString(CultureInfo.InvariantCulture);
            var intervals=new[]{new WorkerInterval(intervalId,attempt.Id,attempt.WorkerId,s.RuleClock,end)};
            var claims=attempt.SelectedUnitIds.Select((id,index)=>new ResourceReservation(MiningIds.Reservation(attempt.Id,index),
                attempt.Id,id,s.MiningUnits.Single(x=>x.Id==id).MassPounds)).ToArray();
            var use=s.SchemaVersion>=Snapshot.MiningToolCandidateSchema?s.MiningToolUses.SingleOrDefault(x=>x.MiningAttemptId==attempt.Id):null;
            if(use!=null&&use.ReservedUnitId!="")claims=claims.Concat(new[]{new ResourceReservation(MiningIds.ToolReserveReservation(attempt.Id),
                attempt.Id,use.ReservedUnitId,s.MiningUnits.Single(x=>x.Id==use.ReservedUnitId).MassPounds)}).ToArray();
            bool claimsExist=s.Work.Reservations.Any(x=>x.JobId==attempt.Id);
            s.Work=s.Work.Reserve(attempt.Id,intervals,claimsExist?Array.Empty<ResourceReservation>():claims);
        }

        private static void PauseMining(Snapshot s,MiningAttemptRecord attempt)
        {
            if(attempt.Status!=MiningAttemptStatus.Working)return;
            s.Work=s.Work.CancelFutureWork(attempt.Id,s.RuleClock);
            PutMiningAttempt(s,attempt.WithWork(s.RuleClock,attempt.WorkDone,MiningAttemptStatus.Paused,attempt.CommittedAt));
        }

        private void PauseIncompatibleMining(Snapshot s)
        {
            foreach(var attempt in s.MiningAttempts.Where(x=>x.Status==MiningAttemptStatus.Working).ToArray()) {
                var deposit=s.MiningDeposits.Single(x=>x.Id==attempt.DepositId);
                if(MiningAccess(s,attempt.WorkerId,deposit,attempt.Id,attempt.SelectedUnitIds)!=null)PauseMining(s,attempt);
            }
        }

        private static RuleTime? NextMiningBoundary(Snapshot s)
        {
            var boundaries=new List<RuleTime>();
            foreach(var attempt in s.MiningAttempts.Where(x=>x.Status==MiningAttemptStatus.Working)) {
                boundaries.Add(s.Work.WorkerIntervals.Single(w=>w.JobId==attempt.Id&&w.Start<=s.RuleClock&&w.End>s.RuleClock).End);
                if(s.SchemaVersion<Snapshot.MiningToolCandidateSchema)continue;
                var use=s.MiningToolUses.SingleOrDefault(x=>x.MiningAttemptId==attempt.Id);
                if(use==null||use.PreparedUnitId==""||attempt.RemovalSeconds<MineralPreparationValidation.WorkSeconds)continue;
                RuleTime preparationEnd=new RuleTime(checked(attempt.SetupSeconds+attempt.RemovalSeconds));
                if(attempt.WorkDone<preparationEnd)
                    boundaries.Add(AddMiningTime(s.RuleClock,SubtractMiningTime(preparationEnd,attempt.WorkDone)));
            }
            return boundaries.Count==0?(RuleTime?)null:boundaries.Min();
        }

        private void CreditMiningWork(Snapshot s,RuleTime elapsed)
        {
            foreach(var attempt in s.MiningAttempts.Where(x=>x.Status==MiningAttemptStatus.Working).ToArray()) {
                if(!s.Work.WorkerIntervals.Any(w=>w.JobId==attempt.Id&&w.Start<=attempt.UpdatedAt&&w.End>=s.RuleClock))continue;
                RuleTime work=AddMiningTime(attempt.WorkDone,elapsed);RuleTime? committedAt=attempt.CommittedAt;
                if(!committedAt.HasValue&&attempt.WorkDone<=new RuleTime(attempt.SetupSeconds)&&work>new RuleTime(attempt.SetupSeconds)) {
                    RuleTime untilRemoval=SubtractMiningTime(new RuleTime(attempt.SetupSeconds),attempt.WorkDone);
                    committedAt=AddMiningTime(attempt.UpdatedAt,untilRemoval);
                    var reserved=s.SchemaVersion>=Snapshot.MiningToolCandidateSchema
                        ?s.MiningToolUses.SingleOrDefault(x=>x.MiningAttemptId==attempt.Id)?.ReservedUnitId:"";
                    var unselected=s.MiningCategories.Where(x=>x.DepositId==attempt.DepositId&&x.Accessible
                        &&!attempt.SelectedCategoryIds.Contains(x.Id,StringComparer.Ordinal)).SelectMany(x=>x.UnitIds)
                        .Where(id=>id!=reserved);
                    foreach(string unitId in unselected) {
                        var unit=s.MiningUnits.Single(x=>x.Id==unitId);
                        if(unit.Status==MiningUnitStatus.Available)PutMiningUnit(s,unit.WithStatus(MiningUnitStatus.Forfeited));
                    }
                }
                if(work>=new RuleTime(attempt.DurationSeconds))PutMiningAttempt(s,attempt.WithWork(s.RuleClock,new RuleTime(attempt.DurationSeconds),MiningAttemptStatus.AwaitingCheck,committedAt));
                else PutMiningAttempt(s,attempt.WithWork(s.RuleClock,work,MiningAttemptStatus.Working,committedAt));
                if(s.SchemaVersion>=Snapshot.MiningToolCandidateSchema) {
                    var use=s.MiningToolUses.SingleOrDefault(x=>x.MiningAttemptId==attempt.Id);
                    if(use!=null) {
                        var profile=s.MiningToolCandidateProfiles.Single(x=>x.Id==use.ProfileId);
                        var instance=s.MiningToolInstanceStates.SingleOrDefault(x=>x.ProfileId==profile.Id);
                        string[] covered=attempt.SelectedUnitIds.Concat(use.ReservedUnitId==""?Array.Empty<string>():new[]{use.ReservedUnitId}).ToArray();
                        bool physical=MiningToolCandidateRules.PhysicallyEligible(s,profile,instance,attempt.WorkerId,covered);
                        RuleTime toolWork=use.ToolWorkDone,preparationWork=use.PreparationWorkDone;
                        RuleTime removalStart=new RuleTime(attempt.SetupSeconds);
                        RuleTime removalEnd=new RuleTime(checked(attempt.SetupSeconds+attempt.RemovalSeconds));
                        if(physical)toolWork=AddMiningTime(toolWork,MiningOverlap(attempt.WorkDone,work,removalStart,removalEnd));
                        bool targetBound=use.PreparedUnitId!=""&&attempt.RemovalSeconds>=MineralPreparationValidation.WorkSeconds;
                        RuleTime prepEnd=removalEnd;
                        RuleTime prepStart=SubtractMiningTime(prepEnd,new RuleTime(MineralPreparationValidation.WorkSeconds));
                        if(physical&&targetBound)preparationWork=AddMiningTime(preparationWork,
                            MiningOverlap(attempt.WorkDone,work,prepStart,prepEnd));
                        var progressed=use.WithWork(toolWork,preparationWork);PutMiningToolUse(s,progressed);
                        if(targetBound&&preparationWork>=new RuleTime(MineralPreparationValidation.WorkSeconds)
                            &&!progressed.PreparationCompletedAt.HasValue)
                            CompleteMiningToolPreparation(s,attempt,progressed,profile);
                    }
                }
            }
        }

        private static void CompleteMiningToolPreparation(Snapshot s,MiningAttemptRecord attempt,
            MiningToolUseRecord use,MiningToolCandidateProfileRecord candidate)
        {
            var preparation=s.MineralPreparationProfiles.Single(x=>x.Id==candidate.PreparationProfileId);
            var unit=s.MiningUnits.Single(x=>x.Id==use.PreparedUnitId);
            var deposit=s.MiningDeposits.Single(x=>x.Id==attempt.DepositId);
            if(unit.Status!=MiningUnitStatus.Available||!attempt.SelectedUnitIds.Contains(unit.Id,StringComparer.Ordinal)
                ||unit.Condition!=MiningUnitCondition.Intact||unit.MassPounds>new RuleQuantity(1)
                ||attempt.RemovalSeconds<MineralPreparationValidation.WorkSeconds)
                throw new InvalidOperationException("Mining-tool preparation target ceased to match its committed extraction.");
            int index=Array.IndexOf(attempt.SelectedUnitIds,unit.Id);
            string inputReservation=MiningIds.Reservation(attempt.Id,index);
            if(s.Work.Reservations.Single(x=>x.Id==inputReservation).Status==ReservationStatus.Reserved)
                s.Work=s.Work.Release(attempt.Id,inputReservation);
            string retainedId=use.Id+".retained";
            string gangueId=preparation.GangueWastePounds>default(RuleQuantity)?use.Id+".gangue":"";
            string ground=GroundId(deposit.SiteX,deposit.SiteY);
            RuleQuantity retainedMass=unit.MassPounds-preparation.GangueWastePounds;
            OrdinaryInventory.Descendant(s,unit.Id,retainedId,retainedMass,ground,deposit.OwnerId,InventoryAccess.Ground);
            if(gangueId!="")OrdinaryInventory.Descendant(s,unit.Id,gangueId,preparation.GangueWastePounds,
                ground,deposit.OwnerId,InventoryAccess.Ground);
            var original=s.PortableEquipment.Single(x=>x.Id==unit.Id);
            var retainedItem=new PortableEquipmentRecord(unit.Id,original.ProfileId,deposit.OwnerId,deposit.OwnerId,"",
                PortablePlacement.Ground,PortableLinkKind.InventoryLot,retainedId,PortableMassBasis.GenericPounds,retainedMass,null,
                groundX:deposit.SiteX,groundY:deposit.SiteY);
            var items=s.PortableEquipment.Where(x=>x.Id!=unit.Id&&x.Id!=retainedId&&x.Id!=gangueId).ToList();
            items.Add(retainedItem);
            if(gangueId!="")items.Add(new PortableEquipmentRecord(gangueId,preparation.GangueItemProfileId,
                deposit.OwnerId,deposit.OwnerId,"",PortablePlacement.Ground,PortableLinkKind.InventoryLot,gangueId,
                PortableMassBasis.GenericPounds,preparation.GangueWastePounds,null,groundX:deposit.SiteX,groundY:deposit.SiteY));
            s.PortableEquipment=items.ToArray();
            PutMiningToolUse(s,use.CompletePreparation(s.RuleClock,retainedId,gangueId));
        }

        private void ResolveReadyMining(Snapshot s)
        {
            var ready=s.MiningAttempts.Where(x=>x.Status==MiningAttemptStatus.AwaitingCheck).ToArray();
            if(ready.Length>0)TestOnlyClubAttackPolicy.AdvanceConditions(s,".mining-ready",true);
            foreach(var attempt in ready) {
                var deposit=s.MiningDeposits.Single(x=>x.Id==attempt.DepositId);
                if(MiningAccess(s,attempt.WorkerId,deposit,attempt.Id,attempt.SelectedUnitIds)==null)FinishMiningCheck(s,attempt);
            }
        }

        private void FinishMiningCheck(Snapshot s,MiningAttemptRecord prior)
        {
            var actorFacts=CharacterStateFacts.ForActor(s,prior.WorkerId,"mining-tools");
            var toolUse=s.SchemaVersion>=Snapshot.MiningToolCandidateSchema
                ?s.MiningToolUses.SingleOrDefault(x=>x.MiningAttemptId==prior.Id):null;
            var toolProfile=toolUse==null?null:s.MiningToolCandidateProfiles.Single(x=>x.Id==toolUse.ProfileId);
            var toolInstance=toolProfile==null?null:s.MiningToolInstanceStates.SingleOrDefault(x=>x.ProfileId==toolProfile.Id);
            bool toolQualified=toolUse!=null&&MiningToolCandidateRules.Qualifies(s,toolProfile,toolInstance,toolUse,
                prior.WorkerId,prior.SelectedUnitIds);
            CharacterAbility ability=prior.Ability==MiningAbilityChoice.Strength?CharacterAbility.Strength:CharacterAbility.Wisdom;
            int injury=actorFacts.InjuryPenalty(ability,toolCheck:true);
            int modifier=checked(prior.AbilityModifier+prior.ProficiencyBonus+injury+(toolQualified?MiningToolCandidateProfileRecord.CheckBonus:0));
            int disadvantage=(prior.ProficiencyRank==0?1:0)+(prior.Hurried?1:0)
                +(TestOnlyClubAttackPolicy.ConditionsFor(s,prior.WorkerId).View().Has(ConditionKind.Poisoned)?1:0);
            uint randomBefore=s.RandomState;
            var roll=PlaytestDice.RollD20(randomBefore,disadvantageSources:disadvantage);
            var check=PlaytestRolls.TaskCheck(roll.Natural,modifier,prior.CheckDc);
            s.RandomState=roll.NextRandomState;
            MiningAttemptStatus status=check.Degree==TaskDegree.CriticalSuccess?MiningAttemptStatus.CriticalSuccess
                :check.Degree==TaskDegree.Success?MiningAttemptStatus.Success
                :check.Degree==TaskDegree.Failure?MiningAttemptStatus.Failure:MiningAttemptStatus.CriticalFailure;
            int d4=0,wound=0,injuryRoll=0;long damage=0,words=roll.WordsConsumed;
            if(status==MiningAttemptStatus.CriticalFailure) {
                var draw=DiceStream.Draw(s.RandomState,4);d4=checked((int)draw.Value+1);damage=d4;
                damage=CharacterAdvancementRules.ReduceIncomingDamage(s,prior.WorkerId,damage);
                if(TestOnlyClubAttackPolicy.ConditionsFor(s,prior.WorkerId).View().Has(ConditionKind.Petrified))damage=PlaytestConditions.PetrifiedDamage(damage);
                int constitution=checked(actorFacts.Rules.AbilityModifier(CharacterAbility.Constitution)
                    +CharacterAdvancementRules.SaveProficiencyBonus(s,prior.WorkerId,"CON"));
                var life=actorFacts.Life;
                var injuryResult=PlaytestDamageDice.Resolve(ActorLifeRules.Read(life),damage,s.RuleClock,draw.NextState,constitution);
                s.RandomState=injuryResult.NextRandomState;words=checked(words+draw.WordsConsumed+injuryResult.WordsConsumed);
                wound=injuryResult.WoundRoll?.Natural??0;injuryRoll=injuryResult.InjuryD6??0;
                TestOnlyClubAttackPolicy.ApplyLife(s,life,injuryResult.Outcome.State);
            }
            var selected=prior.SelectedUnitIds.Select(id=>s.MiningUnits.Single(x=>x.Id==id)).ToArray();
            string[] outputIds=Array.Empty<string>();
            if(status==MiningAttemptStatus.Success||status==MiningAttemptStatus.CriticalSuccess) {
                var output=selected.Where(x=>x.Condition==MiningUnitCondition.Intact).Select(x=>x.Id).ToList();
                if(status==MiningAttemptStatus.CriticalSuccess) {
                    var damaged=selected.Where(x=>x.Condition==MiningUnitCondition.DamagedPotentiallyRecoverable).ToArray();
                    if(damaged.Length>0)output.Add(damaged.SingleOrDefault(x=>x.Id==prior.CriticalRecoveryPreference)?.Id??damaged.OrderBy(x=>x.Id,StringComparer.Ordinal).First().Id);
                }
                outputIds=output.Distinct(StringComparer.Ordinal).ToArray();
            }
            string reserveAwarded=status==MiningAttemptStatus.CriticalSuccess&&toolQualified&&toolUse.ReservedUnitId!=""
                ?toolUse.ReservedUnitId:"";
            bool dressedAwarded=(status==MiningAttemptStatus.Success||status==MiningAttemptStatus.CriticalSuccess)
                &&toolQualified&&toolUse.PreparedUnitId!=""&&toolUse.PreparationCompletedAt.HasValue
                &&outputIds.Contains(toolUse.PreparedUnitId,StringComparer.Ordinal);
            string failedUnit="";
            if(status==MiningAttemptStatus.Failure) {
                if(selected.Any(x=>!x.ValueCopper.HasValue))failedUnit=selected.OrderBy(x=>x.Id,StringComparer.Ordinal).First().Id;
                else {
                    long highest=selected.Max(x=>x.ValueCopper.Value);
                    var top=selected.Where(x=>x.ValueCopper.Value==highest).ToArray();
                    failedUnit=(top.SingleOrDefault(x=>x.Id==prior.FailureVictimPreference)??top.OrderBy(x=>x.Id,StringComparer.Ordinal).First()).Id;
                }
            }
            string receiverId=s.MiningDeposits.Single(x=>x.Id==prior.DepositId).ReceiverId;
            foreach(var unit in selected) {
                bool received=outputIds.Contains(unit.Id,StringComparer.Ordinal);
                if(received) {
                    if(toolUse!=null&&toolUse.PreparedUnitId==unit.Id&&toolUse.PreparationCompletedAt.HasValue) {
                        ReceivePreparedMiningUnit(s,unit,toolUse,toolProfile,receiverId,dressedAwarded);
                        continue;
                    }
                    var lot=s.Work.Lots.Single(x=>x.Id==unit.Id);
                    var lots=s.Work.Lots.Select(x=>x.Id==unit.Id?new ResourceLot(x.Id,x.UnitId,x.Amount,receiverId,x.CustodianId):x).ToArray();
                    var portable=s.PortableEquipment.Single(x=>x.Id==unit.Id);
                    var receiver=s.PortableEquipment.Single(x=>x.Id==receiverId);
                    var body=new PortableEquipmentRecord(unit.Id,portable.ProfileId,portable.OwnerId,receiver.CustodianId,receiverId,
                        PortablePlacement.Contained,PortableLinkKind.InventoryLot,unit.Id,PortableMassBasis.GenericPounds,unit.MassPounds,null);
                    s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==unit.Id?body:x).ToArray();
                    var provenance=s.InventoryLots.Single(x=>x.LotId==unit.Id);
                    s.InventoryLots=s.InventoryLots.Select(x=>x.LotId==unit.Id?new InventoryLotRecord(x.LotId,x.ParentId,x.OwnerId,
                        x.CreatedAmount,x.CreatedAt,x.Nutrition,x.FreshUntil,InventoryAccess.Stowed):x).ToArray();
                    PutMiningUnit(s,unit.WithStatus(MiningUnitStatus.Extracted,unit.Id,receiverId));
                    // The item remains the same physical lot; only its location changes.
                    if(lot.Amount!=unit.MassPounds||provenance.OwnerId!=body.OwnerId)throw new InvalidOperationException("Mining receipt lost its source unit.");
                    s.Work=new WorkLedger(lots,s.Work.WorkerIntervals,s.Work.Reservations);
                } else {
                    MiningUnitStatus disposition=status==MiningAttemptStatus.CriticalFailure||unit.Id==failedUnit
                        ?MiningUnitStatus.Ruined:MiningUnitStatus.Spent;
                    PutMiningUnit(s,unit.WithStatus(disposition));
                }
            }
            if(reserveAwarded!="") {
                var reserve=s.MiningUnits.Single(x=>x.Id==reserveAwarded);
                ReceiveMiningUnit(s,reserve,receiverId);
            }
            // Reservations are claims on identified physical units; resolution closes each claim.
            foreach(string unitId in prior.SelectedUnitIds) {
                int index=Array.IndexOf(prior.SelectedUnitIds,unitId);string reservationId=MiningIds.Reservation(prior.Id,index);
                if(s.Work.Reservations.Any(x=>x.Id==reservationId&&x.RemainingAmount!=default))s.Work=s.Work.Release(prior.Id,reservationId);
            }
            if(toolUse!=null&&toolUse.ReservedUnitId!="") {
                string reservationId=MiningIds.ToolReserveReservation(prior.Id);
                if(s.Work.Reservations.Any(x=>x.Id==reservationId&&x.RemainingAmount!=default))s.Work=s.Work.Release(prior.Id,reservationId);
            }
            MiningCheckDegree degree=check.Degree==TaskDegree.CriticalFailure?MiningCheckDegree.CriticalFailure
                :check.Degree==TaskDegree.Failure?MiningCheckDegree.Failure
                :check.Degree==TaskDegree.Success?MiningCheckDegree.Success:MiningCheckDegree.CriticalSuccess;
            PutMiningAttempt(s,prior.WithResult(s.RuleClock,status,degree,
                roll.Selection==D20Selection.Normal?MiningDiceSelection.Normal:roll.Selection==D20Selection.Advantage?MiningDiceSelection.Advantage:MiningDiceSelection.Disadvantage,
                roll.First,roll.Second??0,roll.Natural,modifier,d4,damage,d4==0?"":"bludgeoning",wound,injuryRoll,
                randomBefore,s.RandomState,words));
            if(toolUse!=null)PutMiningToolUse(s,toolUse.WithOutcome(toolQualified,reserveAwarded,dressedAwarded));
            ReconcileDyingCadences(s);PauseIncompatibleWork(s);
        }

        private static void ReceivePreparedMiningUnit(Snapshot s,MiningMaterialUnitRecord unit,MiningToolUseRecord use,
            MiningToolCandidateProfileRecord candidate,string receiverId,bool dressed)
        {
            var profile=s.MineralPreparationProfiles.Single(x=>x.Id==candidate.PreparationProfileId);
            var deposit=s.MiningDeposits.Single(x=>x.Id==unit.DepositId);
            RuleQuantity mass=unit.MassPounds-profile.GangueWastePounds;
            var lot=s.Work.Lots.Single(x=>x.Id==use.RetainedLotId);
            var lots=s.Work.Lots.Select(x=>x.Id==use.RetainedLotId
                ?new ResourceLot(x.Id,x.UnitId,x.Amount,receiverId,x.CustodianId):x).ToArray();
            var provenance=s.InventoryLots.Single(x=>x.LotId==use.RetainedLotId);
            s.InventoryLots=s.InventoryLots.Select(x=>x.LotId==use.RetainedLotId
                ?new InventoryLotRecord(x.LotId,x.ParentId,x.OwnerId,x.CreatedAmount,x.CreatedAt,x.Nutrition,x.FreshUntil,InventoryAccess.Stowed):x).ToArray();
            var receiver=s.PortableEquipment.Single(x=>x.Id==receiverId);
            var body=new PortableEquipmentRecord(unit.Id,dressed?profile.DressedItemProfileId:"TEST_ONLY.mining.raw-unit",
                deposit.OwnerId,receiver.CustodianId,receiverId,PortablePlacement.Contained,PortableLinkKind.InventoryLot,
                use.RetainedLotId,PortableMassBasis.GenericPounds,mass,null);
            s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==unit.Id?body:x).ToArray();
            PutMiningUnit(s,unit.WithStatus(MiningUnitStatus.Extracted,use.RetainedLotId,receiverId));
            if(lot.Amount!=mass||provenance.OwnerId!=body.OwnerId||body.LinkedId!=use.RetainedLotId)
                throw new InvalidOperationException("Prepared mining receipt lost its physical descendant.");
            s.Work=new WorkLedger(lots,s.Work.WorkerIntervals,s.Work.Reservations);
        }

        private static void ReceiveMiningUnit(Snapshot s,MiningMaterialUnitRecord unit,string receiverId)
        {
            var lot=s.Work.Lots.Single(x=>x.Id==unit.Id);
            var lots=s.Work.Lots.Select(x=>x.Id==unit.Id?new ResourceLot(x.Id,x.UnitId,x.Amount,receiverId,x.CustodianId):x).ToArray();
            var portable=s.PortableEquipment.Single(x=>x.Id==unit.Id);
            var receiver=s.PortableEquipment.Single(x=>x.Id==receiverId);
            var body=new PortableEquipmentRecord(unit.Id,portable.ProfileId,portable.OwnerId,receiver.CustodianId,receiverId,
                PortablePlacement.Contained,PortableLinkKind.InventoryLot,unit.Id,PortableMassBasis.GenericPounds,unit.MassPounds,null);
            s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==unit.Id?body:x).ToArray();
            var provenance=s.InventoryLots.Single(x=>x.LotId==unit.Id);
            s.InventoryLots=s.InventoryLots.Select(x=>x.LotId==unit.Id?new InventoryLotRecord(x.LotId,x.ParentId,x.OwnerId,
                x.CreatedAmount,x.CreatedAt,x.Nutrition,x.FreshUntil,InventoryAccess.Stowed):x).ToArray();
            PutMiningUnit(s,unit.WithStatus(MiningUnitStatus.Extracted,unit.Id,receiverId));
            if(lot.Amount!=unit.MassPounds||provenance.OwnerId!=body.OwnerId)
                throw new InvalidOperationException("Mining receipt lost its source unit.");
            s.Work=new WorkLedger(lots,s.Work.WorkerIntervals,s.Work.Reservations);
        }

        private sealed class MiningAssessment
        {
            public MiningDepositRecord Deposit;
            public MiningCategoryRecord[] Categories;
            public MiningMaterialUnitRecord[] Units;
            public MiningAttemptRecord Current;
            public MiningToolCandidateProfileRecord ToolProfile;
            public string ToolPreparedUnitId,ToolReservedUnitId;
            public string[] CategoryIds,UnitIds;
            public string FailurePreference,CriticalPreference;
            public int Duration,AbilityModifier,ProficiencyRank,ProficiencyBonus,CheckDc;
        }

        private string AssessMiningCommand(Snapshot s,Command c,out MiningAssessment facts)
        {
            facts=null;
            // Mining's records are carried forward unchanged by later snapshot schemas.
            // Expedition assignment (schema47) delegates into this resolver, so equality
            // with schema43 would incorrectly disable the shared extraction transaction.
            if(miningFixture==null||s.SchemaVersion<Snapshot.MiningSchema)return "MiningNotSelected";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.OverwatchRider!=OverwatchRider.None
                ||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.ExpeditionAssignment!=null||c.HarvestSelection!=null||c.X!=0||c.Y!=0)
                return "InvalidMiningCommand";
            if(IsOffCalendarActivity(s,c.Actor)&&StartsOrResumesActivityWork(c)) {
                var activity=ActivityInterval(s,c.Actor);
                if(activity.Action==WorldActionCommitment.Dash
                    ||activity.Action==WorldActionCommitment.ActiveLabor&&!CanContinueActivityLabor(s,c.Actor))return "OffCalendarActionAlreadySpent";
            }
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Kind==CommandKind.StartMining) {
                if(c.MiningSelection==null)return "MiningSelectionRequired";
                var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==c.Target);
                if(deposit==null)return "UnknownMiningDeposit";
                if(c.MiningSelection.DepositVersionId!=deposit.VersionId)return "MiningDepositVersionMismatch";
                string[] requested=c.MiningSelection.CategoryIds;
                var categories=s.MiningCategories.Where(x=>x.DepositId==deposit.Id&&requested.Contains(x.Id,StringComparer.Ordinal)).ToArray();
                if(categories.Length!=requested.Length)return "UnknownMiningCategory";
                var accessible=s.MiningCategories.Where(x=>x.DepositId==deposit.Id&&x.Accessible).ToArray();
                if(categories.Any(x=>!x.Accessible))return "MiningCategoryInaccessible";
                if(s.MiningAttempts.Any(x=>x.DepositId==deposit.Id))return "MiningDepositClaimClosed";
                var units=categories.SelectMany(x=>x.UnitIds).Select(id=>s.MiningUnits.Single(x=>x.Id==id)).ToArray();
                if(units.Length==0||units.Any(x=>x.Status!=MiningUnitStatus.Available))return "MiningSelectionUnavailable";
                string[] categoryIds=categories.Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
                string[] unitIds=units.Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
                var damaged=units.Where(x=>x.Condition==MiningUnitCondition.DamagedPotentiallyRecoverable).ToArray();
                string failurePreference=c.MiningSelection.FailureVictimPreference;
                if(units.Any(x=>!x.ValueCopper.HasValue)) {
                    if(failurePreference!="")return "MiningUnknownValueUsesNeutralOrder";
                } else {
                    long highest=units.Max(x=>x.ValueCopper.Value);var top=units.Where(x=>x.ValueCopper.Value==highest).ToArray();
                    if(top.Length>1&&(failurePreference==""||!top.Any(x=>x.Id==failurePreference)))return "MiningFailureTieChoiceRequired";
                    if(failurePreference!=""&&!top.Any(x=>x.Id==failurePreference))return "InvalidMiningFailurePreference";
                }
                string criticalPreference=c.MiningSelection.CriticalRecoveryPreference;
                if(damaged.Length>1&&(criticalPreference==""||!damaged.Any(x=>x.Id==criticalPreference)))return "MiningCriticalRecoveryChoiceRequired";
                if(criticalPreference!=""&&!damaged.Any(x=>x.Id==criticalPreference))return "InvalidMiningCriticalRecoveryPreference";
                if(c.MiningSelection.Hurried&&!deposit.HurryFeasible)return "MiningHurryNotFeasible";
                string access=MiningAccess(s,c.Actor,deposit,selectedUnitIds:unitIds);if(access!=null)return access;
                CharacterAbility ability=c.MiningSelection.Ability==MiningAbilityChoice.Strength?CharacterAbility.Strength:CharacterAbility.Wisdom;
                var check=AbilityCheckRules.Derive(s,c.Actor,"mining-tools",ability);
                int dc;
                if(deposit.ExactCheckDc.HasValue)dc=deposit.ExactCheckDc.Value;
                else if(categories.Any(x=>x.Tier==0))return "MiningUnknownTierRequiresExactDc";
                else dc=MiningExtractionRules.TierDc(categories.Max(x=>x.Tier));
                int duration=MiningExtractionRules.DurationSeconds(accessible.Length,categories.Length,c.MiningSelection.Hurried);
                MiningToolCandidateProfileRecord toolProfile=null;string preparedUnitId="",reservedUnitId="";
                if(s.SchemaVersion>=Snapshot.MiningToolCandidateSchema) {
                    toolProfile=s.MiningToolCandidateProfiles.SingleOrDefault(x=>x.DepositId==deposit.Id);
                    var instance=toolProfile==null?null:s.MiningToolInstanceStates.SingleOrDefault(x=>x.ProfileId==toolProfile.Id);
                    if(toolProfile==null||!MiningToolCandidateRules.PhysicallyEligible(s,toolProfile,instance,c.Actor,unitIds))toolProfile=null;
                    if(toolProfile!=null) {
                        MiningExtractionRules.StagePlan(duration,out _,out int removal,out _);
                        if(toolProfile.PreparationUnitId!=""&&unitIds.Contains(toolProfile.PreparationUnitId,StringComparer.Ordinal)
                            &&removal>=MineralPreparationValidation.WorkSeconds)
                            preparedUnitId=toolProfile.PreparationUnitId;
                        string reserve=toolProfile.ReserveUnitId;
                        if(reserve!=""&&!unitIds.Contains(reserve,StringComparer.Ordinal)) {
                            var reserveUnit=s.MiningUnits.Single(x=>x.Id==reserve);
                            string[] allocation=unitIds.Concat(new[]{reserve}).ToArray();
                            if(reserveUnit.Status==MiningUnitStatus.Available&&s.Work.AvailableAmount(reserve)==reserveUnit.MassPounds
                                &&MiningToolCandidateRules.PhysicallyEligible(s,toolProfile,instance,c.Actor,allocation)
                                &&MiningAccess(s,c.Actor,deposit,selectedUnitIds:allocation)==null)
                                reservedUnitId=reserve;
                        }
                    }
                }
                facts=new MiningAssessment { Deposit=deposit,Categories=categories,Units=units,CategoryIds=categoryIds,UnitIds=unitIds,
                    FailurePreference=failurePreference,CriticalPreference=criticalPreference,
                    Duration=duration,ToolProfile=toolProfile,ToolPreparedUnitId=preparedUnitId,ToolReservedUnitId=reservedUnitId,
                    AbilityModifier=check.AbilityModifier,ProficiencyRank=check.ProficiencyRank,
                    ProficiencyBonus=check.ProficiencyBonus,CheckDc=dc };
                return null;
            }
            var current=s.MiningAttempts.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
            if(current==null)return "UnknownMiningAttempt";
            if(c.MiningSelection!=null)return "InvalidMiningCommand";
            if(c.Kind==CommandKind.PauseMining) {
                if(current.Status!=MiningAttemptStatus.Working)return "MiningNotWorking";
                facts=new MiningAssessment { Current=current };return null;
            }
            if(c.Kind!=CommandKind.ResumeMining)return "InvalidMiningCommand";
            if(current.Status!=MiningAttemptStatus.Paused&&current.Status!=MiningAttemptStatus.AwaitingCheck)return "MiningNotPaused";
            var depositToResume=s.MiningDeposits.Single(x=>x.Id==current.DepositId);
            string resumeAccess=MiningAccess(s,c.Actor,depositToResume,current.Id,current.SelectedUnitIds);if(resumeAccess!=null)return resumeAccess;
            facts=new MiningAssessment { Current=current,Deposit=depositToResume };
            return null;
        }

        private string ResolveMining(Snapshot s,Command c)
        {
            string error=AssessMiningCommand(s,c,out var facts);if(error!=null)return error;
            if(c.Kind==CommandKind.StartMining) {
                MiningExtractionRules.StagePlan(facts.Duration,out int setup,out int removal,out int sorting);
                string id=MiningWorkId(s.Revision+1);
                var attempt=new MiningAttemptRecord(id,c.Actor,facts.Deposit.Id,facts.Deposit.VersionId,
                    s.MiningCategories.Count(x=>x.DepositId==facts.Deposit.Id&&x.Accessible),c.MiningSelection.Ability,c.MiningSelection.Hurried,
                    facts.CategoryIds,facts.UnitIds,facts.FailurePreference,s.RuleClock,s.RuleClock,facts.Duration,setup,removal,sorting,default,null,
                    MiningAttemptStatus.Working,facts.AbilityModifier,facts.ProficiencyRank,facts.ProficiencyBonus,facts.CheckDc,null,null,
                    MiningCheckDegree.None,MiningDiceSelection.None,0,0,0,0,0,0,"",0,0,0,0,0,facts.CriticalPreference);
                if(facts.ToolProfile!=null) {
                    s.MiningToolUses=s.MiningToolUses.Concat(new[]{new MiningToolUseRecord(id+".tool-use",id,facts.ToolProfile.Id,
                        c.Actor,facts.ToolPreparedUnitId,facts.ToolReservedUnitId,default,default,null,"","",false,"",false)}).ToArray();
                }
                BookMining(s,attempt);s.MiningAttempts=s.MiningAttempts.Concat(new[]{attempt}).ToArray();return null;
            }
            var current=facts.Current;
            if(c.Kind==CommandKind.PauseMining){PauseMining(s,current);return null;}
            if(current.Status==MiningAttemptStatus.AwaitingCheck){FinishMiningCheck(s,current);return null;}
            BookMining(s,current);
            PutMiningAttempt(s,current.WithWork(s.RuleClock,current.WorkDone,MiningAttemptStatus.Working,current.CommittedAt));return null;
        }

        private bool IsMineralPreparationCommand(Command c)=>miningFixture!=null&&miningFixture.MineralPreparationProfiles.Length>0
            &&(c.Kind==CommandKind.StartMineralPreparation||c.Kind==CommandKind.PauseMineralPreparation
                ||c.Kind==CommandKind.ResumeMineralPreparation);

        private static void PutMineralPreparation(Snapshot s,MineralPreparationAttemptRecord value)
            =>s.MineralPreparationAttempts=s.MineralPreparationAttempts.Select(x=>x.Id==value.Id?value:x).ToArray();

        private string MineralPreparationAccess(Snapshot s,string actor,MineralPreparationProfileRecord profile,
            MiningMaterialUnitRecord unit,string exceptJob="")
        {
            if(miningFixture==null||s.SchemaVersion<Snapshot.MineralPreparationSchema||profile==null||unit==null)return "MineralPreparationNotSelected";
            if(s.InventoryCombat&&s.WorldSchedule.Order.Contains(actor))return "MineralPreparationRequiresExploration";
            if(!IsMiningWorker(actor))return "MineralPreparationWorkerUnsupported";
            if(!CapableWorker(s,actor)||s.WorldTraversals.Any(x=>x.ActorId==actor))return "MineralPreparationWorkerUnavailable";
            if(MiningWorkerBusy(s,actor,exceptJob))return "WorkerBusy";
            if(AvailableHands(s,actor)<2)return "TwoHandsRequired";
            var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==unit.DepositId);
            if(deposit==null||profile.UnitId!=unit.Id||unit.Condition!=MiningUnitCondition.Intact||unit.MassPounds>new RuleQuantity(1))
                return "MineralPreparationUnitIneligible";
            if(unit.Status!=MiningUnitStatus.Extracted||unit.ReceivedContainerId!=deposit.ReceiverId)return "MineralPreparationRequiresExtractedUnit";
            var worker=s.Actors.Single(x=>x.Id==actor);
            if(!WorldSpatialQueries.WithinCardinalRange(worker.X,worker.Y,deposit.SiteX,deposit.SiteY,1))return "MineralPreparationWorksiteOutOfReach";
            var surface=s.Structures.SingleOrDefault(x=>x.Id==deposit.WorkSurfaceId&&x.LocationId==deposit.SiteId&&!x.Broken);
            if(surface==null)return "MineralPreparationStableSurfaceUnavailable";
            var tools=s.PortableEquipment.SingleOrDefault(x=>x.Id==deposit.MiningToolsId&&x.OwnerId==deposit.OwnerId
                &&x.CustodianId==deposit.OwnerId&&x.Placement==PortablePlacement.Ground&&x.GroundX==deposit.SiteX&&x.GroundY==deposit.SiteY);
            if(tools==null||!PortableEquipmentRules.Accessible(s,actor,tools))return "MineralPreparationToolsUnavailable";
            var receiver=s.PortableEquipment.SingleOrDefault(x=>x.Id==deposit.ReceiverId&&x.OwnerId==deposit.OwnerId
                &&x.CustodianId==deposit.OwnerId&&x.Placement==PortablePlacement.Ground&&x.GroundX==deposit.SiteX&&x.GroundY==deposit.SiteY
                &&x.Open&&x.CapacityPounds.HasValue&&x.CapacityCubicFeet.HasValue&&x.FitRuleId!="");
            if(receiver==null||!PortableEquipmentRules.Accessible(s,actor,receiver))return "MineralPreparationReceiverUnavailable";
            var body=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id&&x.LinkKind==PortableLinkKind.InventoryLot
                &&x.LinkedId==unit.ReceivedLotId&&x.ParentId==receiver.Id&&x.Placement==PortablePlacement.Contained
                &&x.CustodianId==deposit.OwnerId&&x.OwnerId==deposit.OwnerId);
            if(body==null||!PortableEquipmentRules.Accessible(s,actor,body))return "MineralPreparationUnitUnavailable";
            var ownClaim=s.Work.Reservations.SingleOrDefault(x=>x.JobId==exceptJob&&x.LotId==unit.Id&&x.RemainingAmount>default(RuleQuantity));
            if(!s.Work.Lots.Any(x=>x.Id==unit.Id&&x.Amount==unit.MassPounds)
                ||s.Work.AvailableAmount(unit.Id)+(ownClaim?.RemainingAmount??default(RuleQuantity))!=unit.MassPounds)
                return "MineralPreparationUnitReserved";
            var structure=s.Structures.SingleOrDefault(x=>x.Id==deposit.WorkSurfaceId);
            if(structure==null||structure.Broken)return "MineralPreparationStableSurfaceUnavailable";
            return null;
        }

        private void PauseMineralPreparation(Snapshot s,MineralPreparationAttemptRecord attempt)
        {
            if(attempt.Status!=MineralPreparationStatus.Working)return;
            s.Work=s.Work.CancelFutureWork(attempt.Id,s.RuleClock);
            PutMineralPreparation(s,attempt.WithWork(s.RuleClock,attempt.WorkDone,MineralPreparationStatus.Paused));
        }

        private void PauseIncompatibleMineralPreparation(Snapshot s)
        {
            foreach(var attempt in s.MineralPreparationAttempts.Where(x=>x.Status==MineralPreparationStatus.Working).ToArray()) {
                var profile=s.MineralPreparationProfiles.Single(x=>x.Id==attempt.ProfileId);
                var unit=s.MiningUnits.Single(x=>x.Id==attempt.UnitId);
                if(MineralPreparationAccess(s,attempt.WorkerId,profile,unit,attempt.Id)!=null)PauseMineralPreparation(s,attempt);
            }
        }

        private static RuleTime? NextMineralPreparationBoundary(Snapshot s)
        {
            var ends=s.MineralPreparationAttempts.Where(x=>x.Status==MineralPreparationStatus.Working)
                .Select(x=>s.Work.WorkerIntervals.Single(w=>w.JobId==x.Id&&w.Start<=s.RuleClock&&w.End>s.RuleClock).End).ToArray();
            return ends.Length==0?(RuleTime?)null:ends.Min();
        }

        private static void CreditMineralPreparationWork(Snapshot s,RuleTime elapsed)
        {
            foreach(var attempt in s.MineralPreparationAttempts.Where(x=>x.Status==MineralPreparationStatus.Working).ToArray()) {
                if(!s.Work.WorkerIntervals.Any(w=>w.JobId==attempt.Id&&w.Start<=attempt.UpdatedAt&&w.End>=s.RuleClock))continue;
                RuleTime work=AddMiningTime(attempt.WorkDone,elapsed);
                PutMineralPreparation(s,work>=new RuleTime(MineralPreparationValidation.WorkSeconds)
                    ?attempt.WithWork(s.RuleClock,new RuleTime(MineralPreparationValidation.WorkSeconds),MineralPreparationStatus.AwaitingCompletion)
                    :attempt.WithWork(s.RuleClock,work,MineralPreparationStatus.Working));
            }
        }

        private void ResolveReadyMineralPreparations(Snapshot s)
        {
            foreach(var attempt in s.MineralPreparationAttempts.Where(x=>x.Status==MineralPreparationStatus.AwaitingCompletion).ToArray()) {
                var profile=s.MineralPreparationProfiles.Single(x=>x.Id==attempt.ProfileId);
                var unit=s.MiningUnits.Single(x=>x.Id==attempt.UnitId);
                if(MineralPreparationAccess(s,attempt.WorkerId,profile,unit,attempt.Id)==null)
                    CompleteMineralPreparation(s,attempt,profile,unit);
            }
        }

        private static void CompleteMineralPreparation(Snapshot s,MineralPreparationAttemptRecord prior,
            MineralPreparationProfileRecord profile,MiningMaterialUnitRecord unit)
        {
            var deposit=s.MiningDeposits.Single(x=>x.Id==unit.DepositId);
            s.Work=s.Work.Release(prior.Id,prior.ReservationId);
            string retainedId=MineralPreparationIds.RetainedLot(prior.Id);
            string gangueId=prior.GangueWastePounds>default(RuleQuantity)?MineralPreparationIds.GangueLot(prior.Id):"";
            OrdinaryInventory.Descendant(s,prior.SourceLotId,retainedId,prior.RetainedMassPounds,deposit.ReceiverId,deposit.OwnerId,InventoryAccess.Stowed);
            if(gangueId!="")OrdinaryInventory.Descendant(s,prior.SourceLotId,gangueId,prior.GangueWastePounds,
                GroundId(deposit.SiteX,deposit.SiteY),deposit.OwnerId,InventoryAccess.Ground);
            var receiver=s.PortableEquipment.Single(x=>x.Id==deposit.ReceiverId);
            var body=new PortableEquipmentRecord(unit.Id,profile.DressedItemProfileId,deposit.OwnerId,receiver.CustodianId,receiver.Id,
                PortablePlacement.Contained,PortableLinkKind.InventoryLot,retainedId,PortableMassBasis.GenericPounds,
                prior.RetainedMassPounds,null);
            var gangueBody=gangueId==""?null:new PortableEquipmentRecord(gangueId,profile.GangueItemProfileId,deposit.OwnerId,deposit.OwnerId,"",
                PortablePlacement.Ground,PortableLinkKind.InventoryLot,gangueId,PortableMassBasis.GenericPounds,
                prior.GangueWastePounds,null,groundX:deposit.SiteX,groundY:deposit.SiteY);
            s.PortableEquipment=s.PortableEquipment.Where(x=>x.Id!=retainedId).Select(x=>x.Id==unit.Id?body:x)
                .Concat(gangueBody==null?Array.Empty<PortableEquipmentRecord>():new[]{gangueBody}).ToArray();
            PutMiningUnit(s,unit.WithStatus(MiningUnitStatus.Extracted,retainedId,deposit.ReceiverId));
            PutMineralPreparation(s,prior.Complete(s.RuleClock,retainedId,gangueId));
        }

        private sealed class MineralPreparationAssessment
        {
            public MineralPreparationProfileRecord Profile;
            public MiningMaterialUnitRecord Unit;
            public MineralPreparationAttemptRecord Current;
        }

        private string AssessMineralPreparationCommand(Snapshot s,Command c,out MineralPreparationAssessment facts)
        {
            facts=null;
            if(miningFixture==null||miningFixture.MineralPreparationProfiles.Length==0||s.SchemaVersion<Snapshot.MineralPreparationSchema)
                return "MineralPreparationNotSelected";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.OverwatchRider!=OverwatchRider.None
                ||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.ExpeditionAssignment!=null||c.MiningSelection!=null
                ||c.HarvestSelection!=null||c.ProspectingExposure!=null||c.X!=0||c.Y!=0)return "InvalidMineralPreparationCommand";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Kind==CommandKind.StartMineralPreparation) {
                var profile=s.MineralPreparationProfiles.SingleOrDefault(x=>x.UnitId==c.Target);
                if(profile==null)return "MineralPreparationProfileUnavailable";
                if(s.MineralPreparationAttempts.Any(x=>x.UnitId==profile.UnitId))return "MineralPreparationAlreadyAttempted";
                var unit=s.MiningUnits.SingleOrDefault(x=>x.Id==profile.UnitId);
                if(unit==null)return "MineralPreparationUnitIneligible";
                string access=MineralPreparationAccess(s,c.Actor,profile,unit);if(access!=null)return access;
                facts=new MineralPreparationAssessment{Profile=profile,Unit=unit};return null;
            }
            var current=s.MineralPreparationAttempts.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
            if(current==null)return "UnknownMineralPreparationAttempt";
            var currentProfile=s.MineralPreparationProfiles.Single(x=>x.Id==current.ProfileId);
            var currentUnit=s.MiningUnits.Single(x=>x.Id==current.UnitId);
            if(c.Kind==CommandKind.PauseMineralPreparation) {
                if(current.Status!=MineralPreparationStatus.Working)return "MineralPreparationNotWorking";
            } else if(c.Kind==CommandKind.ResumeMineralPreparation) {
                if(current.Status!=MineralPreparationStatus.Paused&&current.Status!=MineralPreparationStatus.AwaitingCompletion)
                    return "MineralPreparationNotPaused";
                string access=MineralPreparationAccess(s,c.Actor,currentProfile,currentUnit,current.Id);if(access!=null)return access;
            } else return "InvalidMineralPreparationCommand";
            facts=new MineralPreparationAssessment{Profile=currentProfile,Unit=currentUnit,Current=current};return null;
        }

        private string ResolveMineralPreparation(Snapshot s,Command c)
        {
            string error=AssessMineralPreparationCommand(s,c,out var facts);if(error!=null)return error;
            if(c.Kind==CommandKind.StartMineralPreparation) {
                string id="mineral.preparation."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
                string reservation=MineralPreparationIds.Reservation(id);
                var profile=facts.Profile;var unit=facts.Unit;
                var attempt=new MineralPreparationAttemptRecord(id,c.Actor,profile.Id,unit.Id,unit.Id,reservation,unit.MassPounds,
                    profile.GangueWastePounds,unit.MassPounds-profile.GangueWastePounds,s.RuleClock,s.RuleClock,default,
                    MineralPreparationStatus.Working);
                BookMineralPreparation(s,attempt,true);s.MineralPreparationAttempts=s.MineralPreparationAttempts.Concat(new[]{attempt}).ToArray();
                return null;
            }
            var current=facts.Current;
            if(c.Kind==CommandKind.PauseMineralPreparation){PauseMineralPreparation(s,current);return null;}
            if(current.Status==MineralPreparationStatus.AwaitingCompletion) {
                CompleteMineralPreparation(s,current,facts.Profile,facts.Unit);return null;
            }
            BookMineralPreparation(s,current,false);
            PutMineralPreparation(s,current.WithWork(s.RuleClock,current.WorkDone,MineralPreparationStatus.Working));return null;
        }

        private static void BookMineralPreparation(Snapshot s,MineralPreparationAttemptRecord attempt,bool reserveInput)
        {
            RuleTime remaining=SubtractMiningTime(new RuleTime(MineralPreparationValidation.WorkSeconds),attempt.WorkDone);
            RuleTime end=AddMiningTime(s.RuleClock,remaining);
            int index=s.Work.WorkerIntervals.Count(x=>x.JobId==attempt.Id);
            var intervals=new[]{new WorkerInterval(attempt.Id+".labor."+index.ToString(CultureInfo.InvariantCulture),
                attempt.Id,attempt.WorkerId,s.RuleClock,end)};
            var claims=reserveInput?new[]{new ResourceReservation(attempt.ReservationId,attempt.Id,attempt.SourceLotId,attempt.InputMassPounds)}
                :Array.Empty<ResourceReservation>();
            s.Work=s.Work.Reserve(attempt.Id,intervals,claims);
        }
    }
}
#endif
