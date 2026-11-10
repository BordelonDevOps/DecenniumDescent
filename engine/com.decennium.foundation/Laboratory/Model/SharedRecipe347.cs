#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Numerics;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One explicit finite TEST_ONLY recipe-347 workshop and stock profile. It supplies
    /// no production formula acquisition, material generation, workshop catalog or advancement.</summary>
    public sealed class TestOnlyRecipe347Fixture
    {
        public const string RecipeId="recipe-347";
        public const string WorkshopId="TEST_ONLY.recipe347.workshop";
        public const string StationId="TEST_ONLY.recipe347.mine-face";
        public const string BodyItemId="TEST_ONLY.recipe347.mundane-body";
        public const string BodyStructureId="TEST_ONLY.recipe347.mundane-body.structure";
        public const string BodyProfileId="TEST_ONLY.mundane-mining-tool-body";
        public const string BodyLotId="TEST_ONLY.recipe347.mundane-body.lot";
        public const string MiningToolsItemId="TEST_ONLY.recipe347.mining-tools";
        public const string MiningToolsStructureId="TEST_ONLY.recipe347.mining-tools.structure";
        public const string AssayKitId="TEST_ONLY.recipe347.assay-kit";
        public const string AssayKitStructureId="TEST_ONLY.recipe347.assay-kit.structure";
        public const string FormulaAccessId="TEST_ONLY.recipe347.formula-access";
        public const string SpecialtyId="TEST_ONLY.recipe347.specialty";
        public const string FormulaSourceId="TEST_ONLY.recipe347.authored-formula";
        public const string SpecialtySourceId="TEST_ONLY.recipe347.authored-specialty";
        public static readonly string[] ComponentLotIds={
            "TEST_ONLY.recipe347.component.wooden-handle",
            "TEST_ONLY.recipe347.component.metal-head",
            "TEST_ONLY.recipe347.component.extraction-tools",
            "TEST_ONLY.recipe347.component.reinforced-grip",
            "TEST_ONLY.recipe347.component.silver-dragon-rib"};
        public static readonly string[] ComponentUnitIds={
            "ing-347-0-wooden_handle","ing-347-1-metal_head","ing-347-2-extraction_tools",
            "ing-347-3-reinforced_grip","drop-silver_dragon_rib"};
        public static readonly int[] ComponentAmounts={5,3,1,1,1};
        public static readonly RuleQuantity[] ComponentMasses={
            new RuleQuantity(1,10),new RuleQuantity(1),new RuleQuantity(1),new RuleQuantity(1,10),new RuleQuantity(49,100)};
        public static readonly RuleQuantity[] ComponentVolumes={
            new RuleQuantity(1,50),new RuleQuantity(1,100),new RuleQuantity(1,20),new RuleQuantity(1,1000),new RuleQuantity(1,20)};
        public static readonly bool[] ComponentConsumed={true,true,false,true,true};
        private readonly RuleTime[] phases={new RuleTime(900),new RuleTime(27900),new RuleTime(28800),new RuleTime(28800),new RuleTime(28800),new RuleTime(28800)};

        internal string Canonical=>"recipe347-test-only-v2|source=46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|"
            +"worker=companion|level=10|specialty=Mining:recipe-347:+1|formula=explicit-access|DC20|STR-or-WIS|"
            +"components=5x0.1+3x1+1x1-retained+1x0.1+1x0.49|body=mundane-3lb-HP5|"
            +"miners-tools=25gp-10lb-HP5-WoodLeather_TEST_ONLY|phases=900,27900,28800,28800,28800,28800|"
            +"workshop=proper-mine-face|two-watches-excluding-rest|shared-mining-candidate-v1|"
            +"default-preparation=unitA:600s:0.1lb-gangue_TEST_ONLY|default-reserve=unitB|"
            +"portable-counted-lots=schema73|volumes="+string.Join(",",ComponentVolumes.Select(x=>x.Numerator.ToString(CultureInfo.InvariantCulture)
                +"/"+x.Denominator.ToString(CultureInfo.InvariantCulture)))+"|body=1/25ft3-per-lb|miners=1/2ft3|assay=1/5ft3|pick=3/10ft3|"
            +string.Join(",",ComponentLotIds);

        internal void Initialize(Snapshot s)
        {
            if(s.SchemaVersion!=Snapshot.PortableCountedLotSchema||s.MiningDeposits.Length==0
                ||s.Recipe347Workshops.Length!=0||s.PortableEquipment.Any(x=>x.Id==BodyItemId||x.Id==AssayKitId)
                ||s.Structures.Any(x=>x.Id==BodyStructureId||x.Id==AssayKitStructureId||x.Id==MiningToolsStructureId)
                ||s.PortableEquipment.Any(x=>x.Id==MiningToolsItemId))
                throw new ArgumentException("Recipe-347 counted stock requires schema73, the selected Mining worksite and fresh fixture identities.");
            var deposit=s.MiningDeposits.OrderBy(x=>x.Id,StringComparer.Ordinal).First();
            string owner=deposit.OwnerId;
            var crate=s.PortableEquipment.SingleOrDefault(x=>x.Id==TestOnlyPortableStorageFixture.CrateId);
            if(crate==null||crate.Placement!=PortablePlacement.Ground
                ||crate.CapacityPounds!=new RuleQuantity(50)||crate.CapacityCubicFeet!=new RuleQuantity(2))
                throw new ArgumentException("Recipe-347 counted stock requires the authored physical storage crate.");
            crate=crate.With(custodianId:owner);
            s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==crate.Id?crate:x).ToArray();
            TestOnlyPortableStorageFixture.AppendRecipe347Profiles(s);
            string custodian=crate.CustodianId,storage=crate.Id;
            var lots=s.Work.Lots.ToList();var inventory=s.InventoryLots.ToList();
            var componentItems=new List<PortableEquipmentRecord>();
            for(int i=0;i<ComponentLotIds.Length;i++) {
                lots.Add(new ResourceLot(ComponentLotIds[i],ComponentUnitIds[i],ComponentAmounts[i],storage,custodian));
                inventory.Add(new InventoryLotRecord(ComponentLotIds[i],"",owner,new RuleQuantity(ComponentAmounts[i]),s.RuleClock,
                    NutritionKind.None,null,InventoryAccess.Stowed));
                componentItems.Add(new PortableEquipmentRecord(ComponentLotIds[i],TestOnlyPortableStorageFixture.CountedProfileId(ComponentUnitIds[i]),
                    owner,custodian,storage,PortablePlacement.Contained,PortableLinkKind.InventoryLot,ComponentLotIds[i],
                    PortableMassBasis.CountedQuantity,null,null));
            }
            lots.Add(new ResourceLot(BodyLotId,"mass-pound",new RuleQuantity(3),storage,custodian));
            inventory.Add(new InventoryLotRecord(BodyLotId,"",owner,new RuleQuantity(3),s.RuleClock,
                NutritionKind.None,null,InventoryAccess.Stowed));
            s.Work=new WorkLedger(lots,s.Work.WorkerIntervals,s.Work.Reservations);s.InventoryLots=inventory.ToArray();
            var body=new PortableEquipmentRecord(BodyItemId,BodyProfileId,owner,custodian,storage,
                PortablePlacement.Contained,PortableLinkKind.InventoryLot,BodyLotId,PortableMassBasis.GenericPounds,
                new RuleQuantity(3),null);
            var assayKit=new PortableEquipmentRecord(AssayKitId,"tools.assayers-supplies",owner,custodian,storage,
                PortablePlacement.Contained,PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(3),new RuleQuantity(3));
            var miningTools=new PortableEquipmentRecord(MiningToolsItemId,"tools.miners-supplies",owner,custodian,storage,
                PortablePlacement.Contained,PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(10),new RuleQuantity(10));
            var pick=s.PortableEquipment.SingleOrDefault(x=>x.Id==deposit.PickId);
            if(pick==null||pick.ProfileId!="TEST_ONLY.mining-pick"||pick.MassBasis!=PortableMassBasis.Fixed)
                throw new ArgumentException("Recipe-347 workshop requires the authored physical pick.");
            var storedPick=pick.With(custodianId:custodian,parentId:storage,placement:PortablePlacement.Contained,groundX:0,groundY:0);
            s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==deposit.PickId?storedPick:x)
                .Concat(componentItems).Concat(new[]{body,assayKit,miningTools}).ToArray();
            s.Structures=s.Structures.Concat(new[]{
                new ObjectStructureRecord(BodyStructureId,"TEST_ONLY.mundane-mining-tool-body",owner,custodian,storage,
                    ObjectMaterial.WoodLeather,5,5,500,new RuleQuantity(3)),
                new ObjectStructureRecord(AssayKitStructureId,"TEST_ONLY.assay-kit-structure",owner,custodian,storage,
                    ObjectMaterial.WoodLeather,5,5,0,new RuleQuantity(3)),
                new ObjectStructureRecord(MiningToolsStructureId,"tools.miners-supplies",owner,custodian,storage,
                    ObjectMaterial.WoodLeather,5,5,2500,new RuleQuantity(10))}).ToArray();
            s.Trades=s.Trades.Where(x=>x.WorkerId!=TestOnlyPolicy.CompanionId||x.TradeId!="Mining")
                .Concat(new[]{new TradeProgressRecord(TestOnlyPolicy.CompanionId,"Mining",10,0)}).ToArray();
            string[] implements={MiningToolsItemId,deposit.PickId,AssayKitId};
            s.Recipe347FormulaAccess=new[]{new TestOnlyRecipe347FormulaAccessRecord(FormulaAccessId,TestOnlyPolicy.CompanionId,RecipeId,FormulaSourceId)};
            s.Recipe347TradeSpecialties=new[]{new TestOnlyTradeSpecialtyRecord(SpecialtyId,TestOnlyPolicy.CompanionId,"Mining",RecipeId,SpecialtySourceId)};
            s.Recipe347Workshops=new[]{new TestOnlyRecipe347WorkshopRecord(WorkshopId,deposit.SiteId,deposit.SiteX,deposit.SiteY,
                StationId,deposit.WorkSurfaceId,Recipe347StationKind.MineFace,implements,true)};
        }

        internal string ValidateSnapshot(Snapshot s)
        {
            if(s.SchemaVersion!=Snapshot.PortableCountedLotSchema||s.Recipe347FormulaAccess.Length!=1
                ||s.Recipe347FormulaAccess[0].Id!=FormulaAccessId||s.Recipe347FormulaAccess[0].ActorId!=TestOnlyPolicy.CompanionId
                ||s.Recipe347TradeSpecialties.Length!=1||s.Recipe347TradeSpecialties[0].Id!=SpecialtyId
                ||s.Recipe347Workshops.Length!=1||s.Recipe347Workshops[0].Id!=WorkshopId
                ||s.Trades.Count(x=>x.TradeId=="Mining")!=1
                ||s.PortableEquipment.Count(x=>x.Id==BodyItemId)!=1||s.PortableEquipment.Count(x=>x.Id==AssayKitId)!=1
                ||s.PortableEquipment.Count(x=>x.Id==MiningToolsItemId)!=1
                ||s.Structures.Count(x=>x.Id==BodyStructureId)!=1||s.Structures.Count(x=>x.Id==AssayKitStructureId)!=1
                ||s.Structures.Count(x=>x.Id==MiningToolsStructureId)!=1)
                return "Recipe347FixtureMismatch";
            var miningKit=s.PortableEquipment.Single(x=>x.Id==MiningToolsItemId);
            var miningKitStructure=s.Structures.Single(x=>x.Id==MiningToolsStructureId);
            var deposit=s.MiningDeposits.OrderBy(x=>x.Id,StringComparer.Ordinal).First();
            var workshop=s.Recipe347Workshops.Single();
            var storedPick=s.PortableEquipment.SingleOrDefault(x=>x.Id==deposit.PickId);
            if(miningKit.ProfileId!="tools.miners-supplies"||miningKit.SourceWeightLb!=new RuleQuantity(10)
                ||miningKit.OperationalWeightLb!=new RuleQuantity(10)
                ||miningKitStructure.ProfileId!=miningKit.ProfileId||miningKitStructure.MaximumHp!=5
                ||miningKitStructure.Hp!=5||miningKitStructure.MassPounds!=new RuleQuantity(10)
                ||miningKitStructure.Material!=ObjectMaterial.WoodLeather
                ||storedPick==null||storedPick.ProfileId!="TEST_ONLY.mining-pick"
                ||!workshop.ImplementIds.SequenceEqual(new[]{MiningToolsItemId,deposit.PickId,AssayKitId},StringComparer.Ordinal))
                return "Recipe347MinerToolsFixtureMismatch";
            for(int i=0;i<ComponentLotIds.Length;i++) {
                var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==ComponentLotIds[i]);
                var inventory=s.InventoryLots.SingleOrDefault(x=>x.LotId==ComponentLotIds[i]);
                var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==ComponentLotIds[i]);
                var profile=PortableStorageProfileValidation.Find(s,TestOnlyPortableStorageFixture.CountedProfileId(ComponentUnitIds[i]));
                if(lot==null||lot.UnitId!=ComponentUnitIds[i]||inventory==null
                    ||inventory.CreatedAmount!=new RuleQuantity(ComponentAmounts[i])
                    ||item==null||inventory.OwnerId!=item.OwnerId||item.CustodianId!=lot.CustodianId
                    ||item.LinkedId!=lot.Id||item.LinkKind!=PortableLinkKind.InventoryLot
                    ||item.MassBasis!=PortableMassBasis.CountedQuantity||item.SourceWeightLb.HasValue||item.OperationalWeightLb.HasValue
                    ||profile==null||profile.QuantityUnitId!=ComponentUnitIds[i]
                    ||profile.MassPerUnitLb!=ComponentMasses[i]||profile.PackedVolumePerUnitCubicFeet!=ComponentVolumes[i])
                    return "Recipe347CountedStockFixtureMismatch";
            }
            return null;
        }

        internal void BindMiningCandidates(Snapshot s,Recipe347MiningToolProfileRecord recipeProfile)
        {
            var profiles=s.MiningToolCandidateProfiles.ToList();
            var states=s.MiningToolInstanceStates.ToList();
            int index=0;
            foreach(var deposit in s.MiningDeposits.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                var existing=profiles.SingleOrDefault(x=>x.DepositId==deposit.Id);
                if(existing!=null) {
                    if(existing.ToolItemId==recipeProfile.ItemId&&existing.StructureId==recipeProfile.StructureId
                        &&!states.Any(x=>x.ProfileId==existing.Id))
                        states.Add(new MiningToolInstanceStateRecord(existing.Id,existing.ToolItemId));
                    index++;continue;
                }
                var target=s.MiningUnits.SingleOrDefault(x=>x.Id==SharedMiningFixture.UnitA&&x.DepositId==deposit.Id
                    &&x.Condition==MiningUnitCondition.Intact&&x.MassPounds<=new RuleQuantity(1));
                var preparation=target==null?null:s.MineralPreparationProfiles.SingleOrDefault(x=>x.UnitId==target.Id);
                var reserve=s.MiningUnits.SingleOrDefault(x=>x.Id==SharedMiningFixture.UnitB&&x.DepositId==deposit.Id
                    &&x.Condition==MiningUnitCondition.Intact);
                string id=recipeProfile.Id+".candidate."+index.ToString(CultureInfo.InvariantCulture);
                var profile=new MiningToolCandidateProfileRecord(id,deposit.Id,recipeProfile.ItemId,BodyProfileId,
                    recipeProfile.StructureId,BodyProfileId,preparation?.Id??"",preparation?.UnitId??"",reserve?.Id??"");
                profiles.Add(profile);states.Add(new MiningToolInstanceStateRecord(id,recipeProfile.ItemId));index++;
            }
            s.MiningToolCandidateProfiles=profiles.ToArray();s.MiningToolInstanceStates=states.ToArray();
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyRecipe347Fixture recipe347Fixture;

        public TestOnlySharedWorldPolicy EnableRecipe347(TestOnlyRecipe347Fixture fixture)
        {
            if(initializationStarted)throw new InvalidOperationException("World initialization has already started.");
            if(fixture==null||recipe347Fixture!=null)throw new ArgumentException("Supply one explicit recipe-347 fixture.");
            if(miningFixture==null||portableStorageFixture==null||crafting==null)
                throw new InvalidOperationException("Recipe347RequiresMiningPortableStorageAndCraftingConsequences");
            var dressingTarget=miningFixture.Deposits.SelectMany(x=>x.Units)
                .SingleOrDefault(x=>x.Id==SharedMiningFixture.UnitA&&x.Condition==MiningUnitCondition.Intact
                    &&x.MassPounds>new RuleQuantity(1,10)&&x.MassPounds<=new RuleQuantity(1));
            if(dressingTarget!=null&&!miningFixture.MineralPreparationProfiles.Any(x=>x.UnitId==dressingTarget.Id))
                miningFixture=miningFixture.WithMineralPreparationProfile(new MineralPreparationProfileRecord(
                    "TEST_ONLY.recipe347.mineral-preparation",dressingTarget.Id,new RuleQuantity(1,10),
                    "TEST_ONLY.recipe347.dressed-mineral","TEST_ONLY.recipe347.gangue"));
            recipe347Fixture=fixture;
            using(var sha=SHA256.Create())ContentFingerprint="TEST_ONLY.recipe347-v1-"
                +string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(ContentFingerprint+"|"+fixture.Canonical))
                    .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
            return this;
        }

        private static bool Recipe347Command(CommandKind kind)=>kind==CommandKind.StartRecipe347||kind==CommandKind.PauseRecipe347
            ||kind==CommandKind.ResumeRecipe347||kind==CommandKind.CancelRecipe347||kind==CommandKind.ResolveRecipe347Quality;
        private static string Recipe347Claim(Recipe347WorkOrderRecord order,int index)
            =>order.Id+".component"+index.ToString(CultureInfo.InvariantCulture);
        private static void PutRecipe347Order(Snapshot s,Recipe347WorkOrderRecord value)
            =>s.Recipe347WorkOrders=s.Recipe347WorkOrders.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static RuleTime Recipe347Add(RuleTime a,RuleTime b)
            =>RuleTime.FromFraction((BigInteger)a.Numerator*b.Denominator+(BigInteger)b.Numerator*a.Denominator,
                (BigInteger)a.Denominator*b.Denominator);
        private static RuleTime Recipe347Subtract(RuleTime a,RuleTime b)
            =>RuleTime.FromFraction((BigInteger)a.Numerator*b.Denominator-(BigInteger)b.Numerator*a.Denominator,
                (BigInteger)a.Denominator*b.Denominator);
        private static long Recipe347Day(RuleTime at)
        {
            if(at<default(RuleTime))throw new ArgumentOutOfRangeException(nameof(at));
            return checked((long)(((BigInteger)at.Numerator/at.Denominator)/86400));
        }
        private static RestWatchSlot Recipe347Watch(Snapshot s,string actor,long day)
            =>s.RestWatchSchedules.Where(x=>x.ActorId==actor&&x.DayOrdinal==day&&x.At<=s.RuleClock)
                .OrderByDescending(x=>x.At).ThenByDescending(x=>x.Revision).ThenByDescending(x=>x.Id,StringComparer.Ordinal)
                .Select(x=>(RestWatchSlot?)x.Slot).FirstOrDefault()??RestWatchSlot.Evening;
        private static int Recipe347WatchIndex(RuleTime at)
        {
            long seconds=checked((long)((BigInteger)at.Numerator/at.Denominator));
            return checked((int)(seconds%86400/28800));
        }
        private static RuleTime Recipe347WatchStart(long day,int watch)=>new RuleTime(checked(day*86400L+watch*28800L));
        private static RuleTime Recipe347WatchEnd(RuleTime at)
        {
            long day=Recipe347Day(at);int watch=Recipe347WatchIndex(at);
            return Recipe347WatchStart(day,watch+1);
        }
        private static bool Recipe347AtWatchStart(RuleTime at)
            =>at==Recipe347WatchStart(Recipe347Day(at),Recipe347WatchIndex(at));

        private static bool Recipe347SourceQualifiedJob(Snapshot s,string jobId)
            =>s.Recipe347WorkOrders.Any(x=>x.Id==jobId)
                ||s.FormulaWork.Any(x=>x.Id==jobId)
                ||s.ManufacturingOrders.Any(x=>x.Id==jobId)
                ||s.MiningAttempts.Any(x=>x.Id==jobId)
                ||s.HarvestAttempts.Any(x=>x.Id==jobId)
                ||s.Crops.SelectMany(x=>x.Tasks).Any(x=>x.Id==jobId)
                ||s.CraftingIncidents.Any(x=>RemedyJobId(x)==jobId);
        private static bool Recipe347SourceQualifiedWorkInWatch(Snapshot s,string actor,long day,int watch)
        {
            var start=Recipe347WatchStart(day,watch);var end=Recipe347WatchStart(day,watch+1);
            return s.Work.WorkerIntervals.Any(x=>x.WorkerId==actor&&Recipe347SourceQualifiedJob(s,x.JobId)
                &&x.Start<end&&x.End>start);
        }
        private static int Recipe347UsedWatches(Snapshot s,string actor,long day)
            =>Enumerable.Range(0,3).Count(w=>(int)Recipe347Watch(s,actor,day)!=w
                &&Recipe347SourceQualifiedWorkInWatch(s,actor,day,w));
        private string Recipe347ProjectedWorkWatchFailure(Snapshot before,Snapshot after,Command command)
        {
            if(recipe347Fixture==null||!Recipe347WorkStartCommand(command))return null;
            var priorIds=new HashSet<string>(before.Work.WorkerIntervals.Select(x=>x.Id),StringComparer.Ordinal);
            var newlyBooked=after.Work.WorkerIntervals.Where(x=>!priorIds.Contains(x.Id)
                &&Recipe347SourceQualifiedJob(after,x.JobId)).ToArray();
            foreach(var interval in newlyBooked) {
                long firstDay=Recipe347Day(interval.Start),lastDay=Recipe347Day(interval.End);
                for(long day=firstDay;day<=lastDay;day++) {
                    bool overlaps=Enumerable.Range(0,3).Any(w=>interval.Start<Recipe347WatchStart(day,w+1)
                        &&interval.End>Recipe347WatchStart(day,w));
                    int restWatch=(int)Recipe347Watch(after,interval.WorkerId,day);
                    if(restWatch>=0&&restWatch<3&&interval.Start<Recipe347WatchStart(day,restWatch+1)
                        &&interval.End>Recipe347WatchStart(day,restWatch))return "Recipe347ScheduledRestWatch";
                    if(overlaps&&Recipe347UsedWatches(before,interval.WorkerId,day)<=2
                        &&Recipe347UsedWatches(after,interval.WorkerId,day)>2)
                        return "Recipe347TwoWorkWatchesExceeded";
                    if(day==long.MaxValue)break;
                }
            }
            return null;
        }
        private string Recipe347WatchAdmission(Snapshot s,string actor)
        {
            if(recipe347Fixture==null)return null;
            if(!Recipe347AtWatchStart(s.RuleClock))return "Recipe347WorkMustStartAtWatchBoundary";
            long day=Recipe347Day(s.RuleClock);int watch=Recipe347WatchIndex(s.RuleClock);
            if((int)Recipe347Watch(s,actor,day)==watch)return "Recipe347ScheduledRestWatch";
            bool alreadyBooked=Recipe347SourceQualifiedWorkInWatch(s,actor,day,watch);
            if(!alreadyBooked&&Recipe347UsedWatches(s,actor,day)>=2)return "Recipe347TwoWorkWatchesExceeded";
            return null;
        }
        private static bool Recipe347WorkStartCommand(Command c)
        {
            switch(c.Kind) {
                case CommandKind.StartRecipe347: case CommandKind.StartManufacturing: case CommandKind.StartFormulaResearch:
                case CommandKind.StartFormulaCopy: case CommandKind.StartHarvest: case CommandKind.PlantCrop:
                case CommandKind.TendCrop: case CommandKind.HarvestCrop: case CommandKind.StartCraftRemedy:
                case CommandKind.StartExpeditionWork: case CommandKind.StartMining:return true;
                case CommandKind.ResumeRecipe347: case CommandKind.ResumeManufacturing: case CommandKind.ResumeFormulaWork:
                case CommandKind.ResumeHarvest: case CommandKind.ResumeMining:return true;
                default:return false;
            }
        }
        private string Recipe347WorkWatchCommandFailure(Snapshot s,Command c)
        {
            if(recipe347Fixture==null||!Recipe347WorkStartCommand(c))return null;
            if(c.Kind==CommandKind.StartRecipe347)return Recipe347WatchAdmission(s,c.Actor);
            if(c.Kind==CommandKind.ResumeRecipe347) {
                var order=s.Recipe347WorkOrders.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
                return order!=null&&order.Status==Recipe347OrderStatus.Paused
                    ?Recipe347WatchAdmission(s,c.Actor):null;
            }
            // The exact-Watch-start rule belongs to this recipe profile only. Other source-bound
            // procedures are admitted at their own legal times, then their booked intervals are
            // checked against the shared two-Work-Watch ceiling after the command books them.
            return null;
        }

        private void InitializeRecipe347(Snapshot s)
        {
            if(recipe347Fixture!=null)recipe347Fixture.Initialize(s);
        }
        private string ValidateRecipe347State(Snapshot s)
            =>recipe347Fixture==null
                ?s.Recipe347FormulaAccess.Length+s.Recipe347TradeSpecialties.Length+s.Recipe347Workshops.Length
                    +s.Recipe347WorkOrders.Length+s.Recipe347Outputs.Length+s.Recipe347MiningToolProfiles.Length
                    +s.Recipe347MiningToolUseEvidence.Length+s.Recipe347MiningToolWorkSegments.Length==0?null:"Recipe347FixtureNotSelected"
                :recipe347Fixture.ValidateSnapshot(s);

        private string Recipe347Access(Snapshot s,string actor,CharacterAbility ability,string exceptJob="")
        {
            if(recipe347Fixture==null)return "Recipe347NotSelected";
            if(actor!=TestOnlyPolicy.CompanionId)return "Recipe347WorkerUnsupported";
            if(ability!=CharacterAbility.Strength&&ability!=CharacterAbility.Wisdom)return "InvalidRecipe347Ability";
            if(s.InventoryCombat&&s.WorldSchedule.Order.Contains(actor))return "Recipe347RequiresExploration";
            if(!CapableWorker(s,actor)||View(s,actor).BlocksSight||AvailableHands(s,actor)<2)return "Recipe347WorkerIncapable";
            if(s.WorldTraversals.Any(x=>x.ActorId==actor))return "Recipe347WorkerMoving";
            var workshop=s.Recipe347Workshops.SingleOrDefault(x=>x.Id==TestOnlyRecipe347Fixture.WorkshopId);
            if(workshop==null)return "Recipe347WorkshopUnavailable";
            var worker=s.Actors.Single(x=>x.Id==actor);
            if(!WorldSpatialQueries.WithinCardinalRange(worker.X,worker.Y,workshop.SiteX,workshop.SiteY,1))return "Recipe347WorkshopOutOfReach";
            var station=s.Structures.SingleOrDefault(x=>x.Id==workshop.StationStructureId&&x.LocationId==workshop.SiteId&&!x.Broken);
            if(station==null||!workshop.ProperWorkshop||CraftingRestrictions.NewOrderBlocked(s,actor,workshop.StationId,"Mining")
                ||CraftingRestrictions.CraftingCheckBlocked(s,TestOnlyRecipe347Fixture.MiningToolsStructureId))
                return "Recipe347WorkshopUnavailable";
            var access=s.Recipe347FormulaAccess.SingleOrDefault(x=>x.ActorId==actor&&x.RecipeId==TestOnlyRecipe347Fixture.RecipeId);
            if(access==null)return "Recipe347FormulaUnavailable";
            var trade=s.Trades.SingleOrDefault(x=>x.WorkerId==actor&&x.TradeId=="Mining");
            var specialty=s.Recipe347TradeSpecialties.SingleOrDefault(x=>x.ActorId==actor&&x.TradeId=="Mining"
                &&x.ScopeId==TestOnlyRecipe347Fixture.RecipeId);
            if(trade==null||trade.Level<10||specialty==null)return "Recipe347MiningSpecialtyRequired";
            if(!s.SkillTraining.Any(x=>x.ActorId==actor&&x.SkillId=="mining-tools"&&x.ProficiencyRank>0))return "Recipe347MiningToolsTrainingRequired";
            for(int i=0;i<TestOnlyRecipe347Fixture.ComponentLotIds.Length;i++) {
                string lotId=TestOnlyRecipe347Fixture.ComponentLotIds[i];
                var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==lotId);
                var physical=s.PortableEquipment.SingleOrDefault(x=>x.LinkKind==PortableLinkKind.InventoryLot&&x.LinkedId==lotId);
                if(lot==null||lot.UnitId!=TestOnlyRecipe347Fixture.ComponentUnitIds[i]||physical==null
                    ||!PortableEquipmentRules.Accessible(s,actor,physical))return "Recipe347ComponentsUnavailable";
            }
            var implements=workshop.ImplementIds.Select(id=>s.PortableEquipment.SingleOrDefault(x=>x.Id==id)).ToArray();
            if(implements.Length!=3||implements.Any(x=>x==null||x.CustodianId!=actor||x.Placement!=PortablePlacement.Ground
                ||x.GroundX!=workshop.SiteX||x.GroundY!=workshop.SiteY||!PortableEquipmentRules.Accessible(s,actor,x)))
                return "Recipe347RequiredImplementsUnavailable";
            if(s.PortableEquipment.SingleOrDefault(x=>x.Id==TestOnlyRecipe347Fixture.BodyItemId) is PortableEquipmentRecord body
                &&(body.Placement!=PortablePlacement.Ground||body.GroundX!=workshop.SiteX||body.GroundY!=workshop.SiteY))
                return "Recipe347MundaneBodyUnavailable";
            if(s.Work.WorkerIntervals.Any(x=>x.WorkerId==actor&&x.JobId!=exceptJob&&x.Start<=s.RuleClock&&x.End>s.RuleClock))return "WorkerBusy";
            return null;
        }
        private void PauseIncompatibleRecipe347(Snapshot s)
        {
            if(recipe347Fixture==null)return;
            foreach(var order in s.Recipe347WorkOrders.Where(x=>x.Status==Recipe347OrderStatus.Working).ToArray())
                if(Recipe347Access(s,order.WorkerId,order.Ability,order.Id)!=null) {
                    s.Work=s.Work.CancelFutureWork(order.Id,s.RuleClock);
                    PutRecipe347Order(s,order.WithWork(s.RuleClock,order.Work.Interrupt(true),Recipe347OrderStatus.Paused));
                }
        }
        private RuleTime Recipe347NextBookingEnd(Snapshot s,Recipe347WorkOrderRecord order)
        {
            long day=Recipe347Day(s.RuleClock);int watch=Recipe347WatchIndex(s.RuleClock);
            RuleTime watchEnd=Recipe347WatchStart(day,watch+1);
            RuleTime phaseEnd=Recipe347Add(s.RuleClock,Recipe347Subtract(order.Work.Phases[order.Work.CompletedPhases],order.Work.Partial));
            return phaseEnd<watchEnd?phaseEnd:watchEnd;
        }
        private bool Recipe347NextPhaseFitsCurrentWatch(Snapshot s,Recipe347WorkOrderRecord order)
        {
            if(order.Work.CompletedPhases>=order.Work.Phases.Count)return false;
            RuleTime watchEnd=Recipe347WatchStart(Recipe347Day(s.RuleClock),Recipe347WatchIndex(s.RuleClock)+1);
            RuleTime remaining=Recipe347Subtract(watchEnd,s.RuleClock);
            RuleTime phaseRemaining=Recipe347Subtract(order.Work.Phases[order.Work.CompletedPhases],order.Work.Partial);
            return phaseRemaining<=remaining;
        }
        private void BookRecipe347(Snapshot s,Recipe347WorkOrderRecord order,bool claims)
        {
            var end=Recipe347NextBookingEnd(s,order);
            if(end<=s.RuleClock)throw new InvalidOperationException("Recipe347NoWatchWorkAvailable");
            int index=s.Work.WorkerIntervals.Count(x=>x.JobId==order.Id);
            var interval=new WorkerInterval(order.Id+".labor."+index.ToString(CultureInfo.InvariantCulture),order.Id,order.WorkerId,s.RuleClock,end);
            if(claims) {
                var reservations=Enumerable.Range(0,5).Select(i=>new ResourceReservation(Recipe347Claim(order,i),order.Id,
                    order.ComponentLotIds[i],TestOnlyRecipe347Fixture.ComponentAmounts[i])).Concat(new[]{
                    new ResourceReservation(order.Id+".body",order.Id,order.BodyLotId,new RuleQuantity(3))}).ToArray();
                s.Work=s.Work.Reserve(order.Id,new[]{interval},reservations);
            } else s.Work=s.Work.Reserve(order.Id,new[]{interval},Array.Empty<ResourceReservation>());
        }
        private RuleTime? NextRecipe347Boundary(Snapshot s)
        {
            if(recipe347Fixture==null)return null;
            var ends=s.Recipe347WorkOrders.Where(x=>x.Status==Recipe347OrderStatus.Working).Select(j=>new[]{
                s.Work.WorkerIntervals.Single(x=>x.JobId==j.Id&&x.Start<=s.RuleClock&&x.End>s.RuleClock).End,
                Recipe347Add(s.RuleClock,Recipe347Subtract(j.Work.Phases[j.Work.CompletedPhases],j.Work.Partial))}).SelectMany(x=>x).ToArray();
            return ends.Length==0?(RuleTime?)null:ends.Min();
        }
        private void CreditRecipe347(Snapshot s,RuleTime elapsed,ICollection<string> ready)
        {
            if(recipe347Fixture==null)return;
            foreach(var order in s.Recipe347WorkOrders.Where(x=>x.Status==Recipe347OrderStatus.Working).ToArray()) {
                var work=order.Work.Credit(elapsed);var current=order.WithWork(s.RuleClock,work,Recipe347OrderStatus.Working);
                if(work.Complete) {PutRecipe347Order(s,current.WithWork(s.RuleClock,work,Recipe347OrderStatus.AwaitingCheck));ready.Add(order.Id);continue;}
                bool phaseEnded=work.CompletedPhases>order.Work.CompletedPhases;
                bool watchEnded=Recipe347AtWatchStart(s.RuleClock);
                bool intervalEnded=!s.Work.WorkerIntervals.Any(x=>x.JobId==order.Id&&x.Start<=s.RuleClock&&x.End>s.RuleClock);
                if(intervalEnded&&phaseEnded&&!watchEnded&&Recipe347NextPhaseFitsCurrentWatch(s,current)) {
                    PutRecipe347Order(s,current);BookRecipe347(s,current,false);continue;
                }
                if(intervalEnded||watchEnded) {
                    s.Work=s.Work.CancelFutureWork(order.Id,s.RuleClock);
                    PutRecipe347Order(s,current.WithWork(s.RuleClock,work.Interrupt(true),Recipe347OrderStatus.Paused));
                } else PutRecipe347Order(s,current);
            }
        }

        private string AssessRecipe347(Snapshot s,Command c,out Recipe347WorkOrderRecord order)
        {
            order=null;
            if(recipe347Fixture==null)return "Recipe347NotSelected";
            if(c.Inventory!=null||c.Combat!=null||c.MiningSelection!=null||c.Advancement!=null||c.X<0||c.Y<0)return "InvalidRecipe347Command";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Kind==CommandKind.StartRecipe347) {
                if(c.Target!=TestOnlyRecipe347Fixture.WorkshopId||c.Y!=0
                    ||c.X!=(int)CharacterAbility.Strength&&c.X!=(int)CharacterAbility.Wisdom)return "InvalidRecipe347Command";
                string failure=Recipe347Access(s,c.Actor,(CharacterAbility)c.X);if(failure!=null)return failure;
                failure=Recipe347WatchAdmission(s,c.Actor);if(failure!=null)return failure;
                if(s.Recipe347WorkOrders.Any(x=>x.Open))return "Recipe347WorkshopClaimed";
                for(int i=0;i<5;i++)if(s.Work.AvailableAmount(TestOnlyRecipe347Fixture.ComponentLotIds[i])
                    <new RuleQuantity(TestOnlyRecipe347Fixture.ComponentAmounts[i]))return "Recipe347ComponentsUnavailable";
                if(s.Work.AvailableAmount(TestOnlyRecipe347Fixture.BodyLotId)<new RuleQuantity(3))return "Recipe347MundaneBodyUnavailable";
                order=new Recipe347WorkOrderRecord("recipe347.order."+(s.Revision+1).ToString(CultureInfo.InvariantCulture),c.Actor,
                    TestOnlyRecipe347Fixture.RecipeId,(CharacterAbility)c.X,TestOnlyRecipe347Fixture.FormulaAccessId,
                    TestOnlyRecipe347Fixture.SpecialtyId,TestOnlyRecipe347Fixture.WorkshopId,TestOnlyRecipe347Fixture.BodyItemId,
                    TestOnlyRecipe347Fixture.BodyStructureId,TestOnlyRecipe347Fixture.BodyLotId,
                    TestOnlyRecipe347Fixture.ComponentLotIds,new[]{TestOnlyRecipe347Fixture.MiningToolsItemId,
                        s.MiningDeposits.OrderBy(x=>x.Id,StringComparer.Ordinal).First().PickId,TestOnlyRecipe347Fixture.AssayKitId},
                    Recipe347OrderStatus.Working,new ActiveWorkProgress(new[]{new RuleTime(900),new RuleTime(27900),new RuleTime(28800),
                        new RuleTime(28800),new RuleTime(28800),new RuleTime(28800)}),s.RuleClock,s.RuleClock);
                return null;
            }
            order=s.Recipe347WorkOrders.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
            if(order==null)return "UnknownRecipe347Order";
            if(!order.Open)return "Recipe347OrderClosed";
            if(c.Kind==CommandKind.ResolveRecipe347Quality) {
                if(order.Status!=Recipe347OrderStatus.AwaitingChoice||c.Y!=0
                    ||c.X!=(int)CraftQualityChoice.Durability&&c.X!=(int)CraftQualityChoice.FullYield)return "Recipe347QualityChoiceUnavailable";
                return null;
            }
            if(c.X!=0||c.Y!=0)return "InvalidRecipe347Command";
            if(c.Kind==CommandKind.PauseRecipe347)return order.Status==Recipe347OrderStatus.Working?null:"Recipe347NotWorking";
            if(c.Kind==CommandKind.CancelRecipe347)return order.Status==Recipe347OrderStatus.AwaitingChoice?"Recipe347ChoicePending":null;
            if(c.Kind!=CommandKind.ResumeRecipe347)return "InvalidRecipe347Command";
            if(order.Status==Recipe347OrderStatus.AwaitingCheck)return Recipe347Access(s,c.Actor,order.Ability);
            if(order.Status!=Recipe347OrderStatus.Paused)return "Recipe347NotPaused";
            string resume=Recipe347Access(s,c.Actor,order.Ability);if(resume!=null)return resume;
            return Recipe347WatchAdmission(s,c.Actor);
        }
        private static void SettleRecipe347Claim(Snapshot s,string job,string id,RuleQuantity consumed)
        {
            var claim=s.Work.Reservations.Single(x=>x.JobId==job&&x.Id==id);
            if(consumed>claim.ConsumedAmount)s.Work=s.Work.ConsumeThrough(job,id,consumed);
            claim=s.Work.Reservations.Single(x=>x.JobId==job&&x.Id==id);
            if(claim.RemainingAmount>default(RuleQuantity))s.Work=s.Work.Release(job,id);
        }
        private static long Recipe347MaximumHp(CraftQuality quality,CraftQualityChoice choice)
            =>quality==CraftQuality.Flawed?2:quality==CraftQuality.Exceptional&&choice==CraftQualityChoice.Durability?6
                :quality==CraftQuality.Masterwork&&choice==CraftQualityChoice.Durability?7:5;
        private void SettleRecipe347(Snapshot s,Recipe347WorkOrderRecord order,CraftQualityChoice choice,int mishap=0,string incidentId="")
        {
            bool failed=order.Quality==CraftQuality.Failed,misHap=order.Quality==CraftQuality.Mishap;
            for(int i=0;i<5;i++) {
                RuleQuantity consumed=TestOnlyRecipe347Fixture.ComponentConsumed[i]
                    ?misHap?new RuleQuantity(TestOnlyRecipe347Fixture.ComponentAmounts[i])
                        :failed?new RuleQuantity(TestOnlyRecipe347Fixture.ComponentAmounts[i])
                            -ManufacturingRules.FailureRecovery(new RuleQuantity(TestOnlyRecipe347Fixture.ComponentAmounts[i]),true,false,false)
                        :new RuleQuantity(TestOnlyRecipe347Fixture.ComponentAmounts[i])
                    :default;
                SettleRecipe347Claim(s,order.Id,Recipe347Claim(order,i),consumed);
            }
            SettleRecipe347Claim(s,order.Id,order.Id+".body",default);
            int xp=0;var trade=s.Trades.Single(x=>x.WorkerId==order.WorkerId&&x.TradeId=="Mining");
            if(!misHap&&!failed) {
                int training=AbilityCheckRules.Derive(s,order.WorkerId,"mining-tools",order.Ability).ProficiencyRank;
                string finding=TestOnlyRecipe347Fixture.RecipeId+".level"+trade.Level.ToString(CultureInfo.InvariantCulture);
                xp=ManufacturingRules.TradeAward(order.Quality,trade.Level,10,15,training>0,
                    trade.SuccessfulRecipes.Contains(TestOnlyRecipe347Fixture.RecipeId),trade.Findings.Contains(finding),true,false,0);
                var next=ManufacturingRules.AdvanceTrade(trade.Level,trade.Xp,xp);var successes=trade.SuccessfulRecipes.ToList();
                if(order.Quality>=CraftQuality.Standard&&!successes.Contains(TestOnlyRecipe347Fixture.RecipeId))successes.Add(TestOnlyRecipe347Fixture.RecipeId);
                s.Trades=s.Trades.Select(x=>x==trade?new TradeProgressRecord(trade.WorkerId,trade.TradeId,next.Level,next.Xp,successes,trade.Findings):x).ToArray();
            }
            string outputId="";Recipe347OrderStatus status=misHap?Recipe347OrderStatus.Mishap:failed?Recipe347OrderStatus.Failed:Recipe347OrderStatus.Complete;
            if(status==Recipe347OrderStatus.Complete) {
                outputId=order.Id+".output";var structure=s.Structures.Single(x=>x.Id==order.BodyStructureId);
                long maximum=Recipe347MaximumHp(order.Quality,choice),hp=Math.Max(0,maximum-(structure.MaximumHp-structure.Hp));
                s.Structures=s.Structures.Select(x=>x.Id==structure.Id?new ObjectStructureRecord(x.Id,x.ProfileId,x.OwnerId,x.CustodianId,
                    x.LocationId,x.Material,maximum,hp,x.BaselineCopper,x.MassPounds):x).ToArray();
                s.Recipe347Outputs=s.Recipe347Outputs.Concat(new[]{new Recipe347OutputProvenanceRecord(outputId,order.Id,
                    order.BodyItemId,order.BodyStructureId,s.RuleClock,s.Revision+1,order.Quality,choice,structure.MaximumHp,
                    structure.Hp,maximum,hp)}).ToArray();
                s.Recipe347MiningToolProfiles=s.Recipe347MiningToolProfiles.Concat(new[]{new Recipe347MiningToolProfileRecord(
                    order.Id+".mining-profile",outputId,order.BodyItemId,order.BodyStructureId,maximum)}).ToArray();
                recipe347Fixture.BindMiningCandidates(s,s.Recipe347MiningToolProfiles.Single(x=>x.ProvenanceId==outputId));
                SynchronizeMiningToolStructureLocation(s,s.PortableEquipment.Single(x=>x.Id==order.BodyItemId));
            }
            PutRecipe347Order(s,order.WithSettlement(s.RuleClock,status,choice,mishap,xp,incidentId,outputId));
        }
        private string FinishRecipe347Check(Snapshot s,Recipe347WorkOrderRecord order)
        {
            if(s.Receipts.Length>=511||s.Revision>=long.MaxValue-1)return "Recipe347SettlementReceiptCapacityReached";
            var facts=CharacterStateFacts.ForActor(s,order.WorkerId,"mining-tools");
            var ability=AbilityCheckRules.Derive(s,order.WorkerId,"mining-tools",order.Ability);
            int modifier=checked(ability.Total+facts.InjuryPenalty(order.Ability,toolCheck:true)+1);
            uint before=s.RandomState;var roll=PlaytestDice.RollD20(before,
                disadvantageSources:View(s,order.WorkerId).Has(ConditionKind.Poisoned)?1:0);s.RandomState=roll.NextRandomState;
            CraftQuality quality=ManufacturingRules.Quality(roll.Natural,modifier,20);
            order=order.WithCheck(s.RuleClock,modifier,roll.First,roll.Second??0,roll.Natural,before,roll.NextRandomState,
                roll.WordsConsumed,quality,quality==CraftQuality.Exceptional||quality==CraftQuality.Masterwork
                    ?Recipe347OrderStatus.AwaitingChoice:Recipe347OrderStatus.AwaitingSettlement);
            if(quality==CraftQuality.Exceptional||quality==CraftQuality.Masterwork){PutRecipe347Order(s,order);return null;}
            int mishap=0;string incident="";
            if(quality==CraftQuality.Mishap) {
                var d6=DiceStream.Draw(s.RandomState,6);s.RandomState=d6.NextState;mishap=d6.Value+1;
                incident=order.Id+".mishap";
                var fact=new CraftingMishapFact(incident,mishap,order.WorkerId,s.RuleClock,new[]{order.WorkerId},
                    TestOnlyRecipe347Fixture.MiningToolsStructureId,TestOnlyRecipe347Fixture.StationId,"Mining");
                string consequence=ApplyCraftingMishap(s,fact);if(consequence!=null)return consequence;
            }
            SettleRecipe347(s,order,CraftQualityChoice.StandardQuantity,mishap,incident);return null;
        }
        private string ResolveRecipe347(Snapshot s,Command c)
        {
            string failure=AssessRecipe347(s,c,out var order);if(failure!=null)return failure;
            if(c.Kind==CommandKind.StartRecipe347) {
                BookRecipe347(s,order,true);s.Recipe347WorkOrders=s.Recipe347WorkOrders.Concat(new[]{order}).ToArray();return null;
            }
            if(c.Kind==CommandKind.PauseRecipe347) {
                s.Work=s.Work.CancelFutureWork(order.Id,s.RuleClock);
                PutRecipe347Order(s,order.WithWork(s.RuleClock,order.Work.Interrupt(true),Recipe347OrderStatus.Paused));return null;
            }
            if(c.Kind==CommandKind.CancelRecipe347) {
                s.Work=s.Work.CancelFutureWork(order.Id,s.RuleClock);
                for(int i=0;i<5;i++)SettleRecipe347Claim(s,order.Id,Recipe347Claim(order,i),
                    order.Work.Labor>default(RuleTime)&&TestOnlyRecipe347Fixture.ComponentConsumed[i]
                        ?new RuleQuantity(TestOnlyRecipe347Fixture.ComponentAmounts[i]):default);
                SettleRecipe347Claim(s,order.Id,order.Id+".body",default);
                PutRecipe347Order(s,order.WithWork(s.RuleClock,order.Work.Interrupt(true),Recipe347OrderStatus.Cancelled));return null;
            }
            if(c.Kind==CommandKind.ResumeRecipe347) {
                if(order.Status==Recipe347OrderStatus.AwaitingCheck)return FinishRecipe347Check(s,order);
                BookRecipe347(s,order,false);PutRecipe347Order(s,order.WithWork(s.RuleClock,order.Work,Recipe347OrderStatus.Working));return null;
            }
            if(c.Kind==CommandKind.ResolveRecipe347Quality) {
                var choice=(CraftQualityChoice)c.X;SettleRecipe347(s,order,choice);
                return ResumeManufacturingAdvance(s,c);
            }
            return "InvalidRecipe347Command";
        }
    }
}
#endif
