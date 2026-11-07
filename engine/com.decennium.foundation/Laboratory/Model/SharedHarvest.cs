#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit authored TEST_ONLY remains and apparatus for the first ordinary fish
    /// harvest witness. The fixture supplies a pre-existing dead specimen; harvest commands never
    /// create a creature, decide death, or imply ownership.</summary>
    public sealed class SharedHarvestFixture
    {
        public const string CreatureId="TEST_ONLY.harvest.river-fish-remains";
        public const string SiteId="TEST_ONLY.harvest.river-shore";
        public const string ManifestId="TEST_ONLY.harvest.river-fish-manifest";
        public const string CategoryId="material.generic-fish-meat";
        public const string CategoryRecordId="TEST_ONLY.harvest.river-fish-category";
        public const string UnitId="TEST_ONLY.harvest.river-fish-meat-portion";
        public const string CategoryId2="TEST_ONLY.material.river-fish-offal";
        public const string CategoryRecordId2="TEST_ONLY.harvest.river-fish-offal-category";
        public const string UnitId2="TEST_ONLY.harvest.river-fish-offal-portion";
        public const string RecoveryUnitId="TEST_ONLY.harvest.river-fish-damaged-liver";
        public const string ToolkitId="TEST_ONLY.harvest.fishing-tackle";
        public const string KnifeId="TEST_ONLY.harvest.small-knife";
        public const string ContainerId="TEST_ONLY.harvest.receiving-tray";
        public const string WorkSurfaceId="TEST_ONLY.harvest.stable-surface";
        public const string MaterialUnit="mass-pound";
        public const string ContainerFitRule="TEST_ONLY.harvest-container-fit-v1";
        public bool Trained { get; }
        public bool HasToolkit { get; }
        public bool HasKnife { get; }
        public bool HasContainer { get; }
        public bool HasWorkSurface { get; }
        public HarvestOriginRestriction OriginRestriction { get; }
        public int SiteX { get; }
        public int SiteY { get; }
        public bool SmallFinitePool { get; }
        public bool EqualFailureValues { get; }
        public bool SingleCategoryMultipleUnits { get; }
        public bool UnknownFailureValues { get; }
        public int SchemaVersion=>SmallFinitePool?Snapshot.HarvestManifestSchema:Snapshot.HarvestSchema;
        public SharedHarvestFixture(bool trained=true,bool hasToolkit=true,bool hasKnife=true,bool hasContainer=true,
            bool hasWorkSurface=true,HarvestOriginRestriction originRestriction=HarvestOriginRestriction.Ordinary,int siteX=3,int siteY=3,
            bool smallFinitePool=false,bool equalFailureValues=false,bool singleCategoryMultipleUnits=false,bool unknownFailureValues=false)
        {
            if(!Enum.IsDefined(typeof(HarvestOriginRestriction),originRestriction)||siteX<0||siteY<0)
                throw new ArgumentException("Invalid ordinary fish harvest fixture.");
            Trained=trained;HasToolkit=hasToolkit;HasKnife=hasKnife;HasContainer=hasContainer;
            HasWorkSurface=hasWorkSurface;OriginRestriction=originRestriction;SiteX=siteX;SiteY=siteY;
            SmallFinitePool=smallFinitePool;EqualFailureValues=equalFailureValues;
            SingleCategoryMultipleUnits=singleCategoryMultipleUnits;UnknownFailureValues=unknownFailureValues;
        }
        internal string Key=>"harvest-schema41-v1|TEST_ONLY-preexisting-dead-river-fish|tiny|tier-I-dc12|one-unit|10m|generic-fish-meat-unknown-value|0.25lb-portion|8h-age-from-death|"
            +Trained+"|"+HasToolkit+"|"+HasKnife+"|"+HasContainer+"|"+HasWorkSurface+"|"+(int)OriginRestriction
            +(SiteX==3&&SiteY==3?"":"|site="+SiteX.ToString(CultureInfo.InvariantCulture)+","+SiteY.ToString(CultureInfo.InvariantCulture))
            +(SmallFinitePool?"|schema42-small-d2|single-category="+SingleCategoryMultipleUnits
                +"|equal-values="+EqualFailureValues+"|unknown-values="+UnknownFailureValues:"");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private SharedHarvestFixture harvestFixture;
        private bool IsHarvestWorker(string actorId) => worldConfiguration == null
            ? actorId == TestOnlyPolicy.CompanionId
            : worldConfiguration.Actors.Any(x => x.Id == actorId);

        public static TestOnlySharedWorldPolicy WithHarvest(SharedHarvestFixture fixture,uint seed=1)
        {
            if(fixture==null)throw new ArgumentNullException(nameof(fixture));
            var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:seed),walkingSpeed:30);
            policy.harvestFixture=fixture;
            using(var sha=SHA256.Create())policy.ContentFingerprint="TEST_ONLY.harvest-v1-"+string.Concat(sha.ComputeHash(
                Encoding.UTF8.GetBytes(policy.ContentFingerprint+"|"+fixture.Key+"|seed="+seed.ToString(CultureInfo.InvariantCulture)))
                    .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
            return policy;
        }

        private static HarvestManifestRecord Manifest(Snapshot s)=>s.HarvestManifests.Single(x=>x.Id==SharedHarvestFixture.ManifestId);
        private static void PutHarvestAttempt(Snapshot s,HarvestAttemptRecord value)
            =>s.HarvestAttempts=s.HarvestAttempts.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void PutHarvestUnit(Snapshot s,HarvestMaterialUnitRecord value)
            =>s.HarvestUnits=s.HarvestUnits.Select(x=>x.Id==value.Id?value:x).ToArray();

        private void InitializeHarvest(Snapshot s)
        {
            if(harvestFixture==null)return;
            string owner=OffCalendarWorkerId;
            if(harvestFixture.Trained) s.SkillTraining=s.SkillTraining.Concat(HarvestWorkerIds
                .Where(id=>!s.SkillTraining.Any(x=>x.ActorId==id&&x.SkillId=="fishing-tackle"))
                .Select(id=>new SkillTrainingRecord(id,"fishing-tackle",1))).ToArray();
            s.FishingCreatures=s.FishingCreatures.Concat(new[]{new FishingCreatureBodyRecord(SharedHarvestFixture.CreatureId,
                "TEST_ONLY.ordinary-river-fish.1lb",HarvestSiteId,HarvestSiteId,HarvestSiteId,
                "",owner,FishingCreatureLifeState.Dead,new RuleQuantity(1),RuleQuantity.FromFraction(1,10),"","","",null,0)}).ToArray();
            string anatomy=harvestFixture.SmallFinitePool?"TEST_ONLY.small-river-fish-anatomy-v1":"TEST_ONLY.ordinary-river-fish-anatomy-v1";
            s.HarvestDonors=new[]{new HarvestDonorRecord(SharedHarvestFixture.CreatureId,"TEST_ONLY.river-fish-death-event.0",default,
                harvestFixture.OriginRestriction,anatomy,owner,new RuleQuantity(1))};
            if(harvestFixture.SmallFinitePool) {
                HarvestYieldResolution yield=HarvestYieldRules.Roll(HarvestSize.Small,s.RandomState);
                if(yield.Units!=2)throw new InvalidOperationException("The TEST_ONLY Small manifest seed must resolve the sourced 1d2 yield to two units.");
                s.RandomState=yield.RandomAfter;
                s.HarvestManifests=new[]{new HarvestManifestRecord(SharedHarvestFixture.ManifestId,SharedHarvestFixture.CreatureId,
                    anatomy,HarvestSize.Small,s.RuleClock,12,HarvestYieldRules.FullTimeSeconds(HarvestSize.Small),yield.Units,HarvestSiteId,
                    SharedHarvestFixture.ToolkitId,SharedHarvestFixture.KnifeId,SharedHarvestFixture.ContainerId,SharedHarvestFixture.WorkSurfaceId,yield)};
                s.HarvestCategories=harvestFixture.SingleCategoryMultipleUnits
                    ?new[]{new HarvestCategoryRecord(SharedHarvestFixture.CategoryRecordId,SharedHarvestFixture.ManifestId,
                        SharedHarvestFixture.CategoryId,2,new[]{HarvestFiniteLotId,SharedHarvestFixture.UnitId2,SharedHarvestFixture.RecoveryUnitId})}
                    :new[]{
                        new HarvestCategoryRecord(SharedHarvestFixture.CategoryRecordId,SharedHarvestFixture.ManifestId,
                            SharedHarvestFixture.CategoryId,1,new[]{HarvestFiniteLotId}),
                        new HarvestCategoryRecord(SharedHarvestFixture.CategoryRecordId2,SharedHarvestFixture.ManifestId,
                            SharedHarvestFixture.CategoryId2,1,new[]{SharedHarvestFixture.UnitId2,SharedHarvestFixture.RecoveryUnitId})};
                long? firstValue=harvestFixture.UnknownFailureValues?null:(long?)(harvestFixture.EqualFailureValues?5:10);
                long? secondValue=harvestFixture.UnknownFailureValues?null:(long?)(harvestFixture.EqualFailureValues?5:20);
                string secondCategory=harvestFixture.SingleCategoryMultipleUnits?SharedHarvestFixture.CategoryId:SharedHarvestFixture.CategoryId2;
                s.HarvestUnits=new[]{
                    new HarvestMaterialUnitRecord(HarvestFiniteLotId,SharedHarvestFixture.ManifestId,SharedHarvestFixture.CategoryId,
                        "TEST_ONLY.material.river-fish-meat",1,RuleQuantity.FromFraction(1,4),firstValue,
                        HarvestUnitCondition.Intact,HarvestUnitStatus.Available,8*60*60,default),
                    new HarvestMaterialUnitRecord(SharedHarvestFixture.UnitId2,SharedHarvestFixture.ManifestId,secondCategory,
                        "TEST_ONLY.material.river-fish-offal",1,RuleQuantity.FromFraction(1,4),secondValue,
                        HarvestUnitCondition.Intact,HarvestUnitStatus.Available,8*60*60,default),
                    new HarvestMaterialUnitRecord(SharedHarvestFixture.RecoveryUnitId,SharedHarvestFixture.ManifestId,secondCategory,
                        "TEST_ONLY.material.damaged-fish-liver",1,RuleQuantity.FromFraction(1,4),5,
                        HarvestUnitCondition.DamagedPotentiallyRecoverable,HarvestUnitStatus.Available,8*60*60,default)};
            } else {
                s.HarvestManifests=new[]{new HarvestManifestRecord(SharedHarvestFixture.ManifestId,SharedHarvestFixture.CreatureId,
                    anatomy,HarvestSize.Tiny,s.RuleClock,12,600,1,HarvestSiteId,
                    SharedHarvestFixture.ToolkitId,SharedHarvestFixture.KnifeId,SharedHarvestFixture.ContainerId,SharedHarvestFixture.WorkSurfaceId)};
                s.HarvestCategories=new[]{new HarvestCategoryRecord(SharedHarvestFixture.CategoryRecordId,SharedHarvestFixture.ManifestId,
                    SharedHarvestFixture.CategoryId,1,new[]{HarvestFiniteLotId})};
                s.HarvestUnits=new[]{new HarvestMaterialUnitRecord(HarvestFiniteLotId,SharedHarvestFixture.ManifestId,
                    SharedHarvestFixture.CategoryId,"generic.ordinary-fish-meat",1,RuleQuantity.FromFraction(1,4),null,
                    HarvestUnitCondition.Intact,HarvestUnitStatus.Available,8*60*60,default)};
            }

            var physical=new System.Collections.Generic.List<PortableEquipmentRecord>();
            if(harvestFixture.HasToolkit)physical.Add(GroundTool(SharedHarvestFixture.ToolkitId,"fishing.fishing-tackle-kit",new RuleQuantity(4)));
            if(harvestFixture.HasKnife)physical.Add(GroundTool(SharedHarvestFixture.KnifeId,"adventuring-gear.small-knife",RuleQuantity.FromFraction(1,4)));
            if(harvestFixture.HasContainer)physical.Add(new PortableEquipmentRecord(SharedHarvestFixture.ContainerId,"TEST_ONLY.harvest-tray",
                owner,owner,"",PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(1),new RuleQuantity(1),
                capacityPounds:new RuleQuantity(2),capacityCubicFeet:RuleQuantity.FromFraction(1,10),open:true,
                fitRuleId:SharedHarvestFixture.ContainerFitRule,fitMemberIds:harvestFixture.SmallFinitePool
                    ?new[]{HarvestFiniteLotId,SharedHarvestFixture.UnitId2,SharedHarvestFixture.RecoveryUnitId}
                    :new[]{HarvestFiniteLotId},groundX:HarvestSiteX,groundY:HarvestSiteY));
            s.PortableEquipment=s.PortableEquipment.Concat(physical).ToArray();
            if(harvestFixture.HasWorkSurface)s.Structures=s.Structures.Concat(new[]{new ObjectStructureRecord(SharedHarvestFixture.WorkSurfaceId,
                "TEST_ONLY.stable-harvest-surface",owner,owner,HarvestSiteId,ObjectMaterial.Stone,100,100,0,new RuleQuantity(20))}).ToArray();
        }
        private PortableEquipmentRecord GroundTool(string id,string profile,RuleQuantity pounds)
            =>new PortableEquipmentRecord(id,profile,OffCalendarWorkerId,OffCalendarWorkerId,"",PortablePlacement.Ground,
                PortableLinkKind.None,"",PortableMassBasis.Fixed,pounds,pounds,groundX:HarvestSiteX,groundY:HarvestSiteY);

        private bool IsHarvestCommand(Command c)=>harvestFixture!=null&&c.Kind==CommandKind.StartHarvest
            ||harvestFixture!=null&&c.Kind==CommandKind.PauseHarvest||harvestFixture!=null&&c.Kind==CommandKind.ResumeHarvest;

        private static string HarvestWorkId(long revision)=>"harvest.work."+revision.ToString(CultureInfo.InvariantCulture);
        private static RuleTime AddHarvestTime(RuleTime first,RuleTime second)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)first.Numerator*second.Denominator
                +(System.Numerics.BigInteger)second.Numerator*first.Denominator,(System.Numerics.BigInteger)first.Denominator*second.Denominator);
        private static RuleTime SubtractHarvestTime(RuleTime first,RuleTime second)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)first.Numerator*second.Denominator
                -(System.Numerics.BigInteger)second.Numerator*first.Denominator,(System.Numerics.BigInteger)first.Denominator*second.Denominator);

        private static bool HarvestWorkerBusy(Snapshot s,string actor,string exceptJob="")
            =>s.Work.WorkerIntervals.Any(x=>x.WorkerId==actor&&x.JobId!=exceptJob&&x.Start<=s.RuleClock&&x.End>s.RuleClock);

        private string HarvestAccess(Snapshot s,string actor,HarvestManifestRecord manifest,string exceptJob="",string[] selectedUnitIds=null)
        {
            if(harvestFixture==null)return "HarvestingNotSelected";
            if(s.InventoryCombat)return "HarvestingRequiresExploration";
            var donor=s.HarvestDonors.SingleOrDefault(x=>x.CreatureId==manifest.CreatureId);
            var body=s.FishingCreatures.SingleOrDefault(x=>x.Id==manifest.CreatureId);
            if(donor==null||body==null||body.LifeState!=FishingCreatureLifeState.Dead||body.LocationId!=manifest.SiteId
                ||donor.OwnerId!=body.CustodianId)return "HarvestRemainsUnavailable";
            if(donor.OriginRestriction==HarvestOriginRestriction.Prohibited)return "HarvestOriginProhibited";
            if(donor.OriginRestriction==HarvestOriginRestriction.ConsentRequired)return "HarvestConsentNotRecorded";
            if(donor.OriginRestriction==HarvestOriginRestriction.AuthorityRequired)return "HarvestAuthorityNotRecorded";
            if(!IsHarvestWorker(actor))return "HarvestWorkerUnsupported";
            // Generic harvesting is open to an untrained worker. The actual tool/site gates
            // below still apply; training contributes proficiency and removes the untrained
            // disadvantage at resolution.
            if(!CapableWorker(s,actor))return "HarvestWorkerIncapable";
            if(s.WorldTraversals.Any(x=>x.ActorId==actor))return "HarvestWorkerMoving";
            if(HarvestWorkerBusy(s,actor,exceptJob))return "WorkerBusy";
            var worker=s.Actors.Single(x=>x.Id==actor);
            if(!WorldSpatialQueries.WithinCardinalRange(worker.X,worker.Y,HarvestSiteX,HarvestSiteY,1))
                return "HarvestWorksiteOutOfReach";
            PortableEquipmentRecord tool(string id)=>s.PortableEquipment.SingleOrDefault(x=>x.Id==id&&x.CustodianId==donor.OwnerId
                &&x.Placement==PortablePlacement.Ground&&PortableEquipmentRules.Accessible(s,actor,x));
            if(!harvestFixture.HasToolkit||tool(manifest.ToolkitId)==null)return "FishingToolkitUnavailable";
            if(!harvestFixture.HasKnife||tool(manifest.KnifeId)==null)return "HarvestKnifeUnavailable";
            if(!harvestFixture.HasWorkSurface||s.Structures.SingleOrDefault(x=>x.Id==manifest.WorkSurfaceId&&x.LocationId==manifest.SiteId&& !x.Broken)==null)
                return "HarvestWorkSurfaceUnavailable";
            var receiver=tool(manifest.ContainerId);
            string[] selected=selectedUnitIds??new[]{HarvestFiniteLotId};
            if(!harvestFixture.HasContainer||receiver==null||!receiver.Open||!receiver.CapacityPounds.HasValue
                ||!receiver.CapacityCubicFeet.HasValue||receiver.FitRuleId!=SharedHarvestFixture.ContainerFitRule
                ||selected.Any(id=>!receiver.FitMemberIds.Contains(id,StringComparer.Ordinal)))return "HarvestContainerUnavailable";
            var units=s.HarvestUnits.Where(x=>selected.Contains(x.Id,StringComparer.Ordinal)&&x.ManifestId==manifest.Id).ToArray();
            if(units.Length!=selected.Distinct(StringComparer.Ordinal).Count())return "HarvestSelectionInvalid";
            if(RuleQuantity.Sum(units.Select(x=>x.MassPounds))>receiver.CapacityPounds.Value)return "HarvestContainerCapacityInsufficient";
            if(TestOnlyClubAttackPolicy.DamageConditionCapacity(s,actor)==false)return "HarvestConsequenceCapacityReached";
            return null;
        }

        private void BookHarvest(Snapshot s,HarvestAttemptRecord attempt)
        {
            RuleTime remaining=SubtractHarvestTime(attempt.Duration,attempt.WorkDone);
            RuleTime end=AddHarvestTime(s.RuleClock,remaining);
            int interval=s.Work.WorkerIntervals.Count(x=>x.JobId==attempt.Id);
            string intervalId=attempt.Id+".labor."+interval.ToString(CultureInfo.InvariantCulture);
            s.Work=s.Work.Reserve(attempt.Id,new[]{new WorkerInterval(intervalId,attempt.Id,attempt.WorkerId,s.RuleClock,end)},Array.Empty<ResourceReservation>());
        }

        private static void PauseHarvest(Snapshot s,HarvestAttemptRecord attempt)
        {
            if(attempt.Status!=HarvestAttemptStatus.Working)return;
            s.Work=s.Work.CancelFutureWork(attempt.Id,s.RuleClock);
            PutHarvestAttempt(s,attempt.WithWork(s.RuleClock,attempt.WorkDone,HarvestAttemptStatus.Paused));
        }

        private void PauseIncompatibleHarvesting(Snapshot s)
        {
            foreach(var attempt in s.HarvestAttempts.Where(x=>x.Status==HarvestAttemptStatus.Working).ToArray()) {
                var manifest=s.HarvestManifests.Single(x=>x.Id==attempt.ManifestId);
                if(HarvestAccess(s,attempt.WorkerId,manifest,attempt.Id,attempt.SelectedUnitIds)!=null)PauseHarvest(s,attempt);
            }
        }

        private static RuleTime? NextHarvestBoundary(Snapshot s)
        {
            var ends=s.HarvestAttempts.Where(x=>x.Status==HarvestAttemptStatus.Working)
                .Select(x=>s.Work.WorkerIntervals.Single(w=>w.JobId==x.Id&&w.Start<=s.RuleClock&&w.End>s.RuleClock).End).ToArray();
            return ends.Length==0?(RuleTime?)null:ends.Min();
        }

        private void CreditHarvestWork(Snapshot s,RuleTime elapsed)
        {
            foreach(var attempt in s.HarvestAttempts.Where(x=>x.Status==HarvestAttemptStatus.Working).ToArray()) {
                if(!s.Work.WorkerIntervals.Any(w=>w.JobId==attempt.Id&&w.Start<=attempt.UpdatedAt&&w.End>=s.RuleClock))continue;
                RuleTime work=AddHarvestTime(attempt.WorkDone,elapsed);
                if(attempt.WorkDone==default&&elapsed>default(RuleTime)) {
                    var unselected=s.HarvestCategories.Where(x=>x.ManifestId==attempt.ManifestId&&!attempt.SelectedCategoryIds.Contains(x.Id,StringComparer.Ordinal))
                        .SelectMany(x=>x.UnitIds).ToHashSet(StringComparer.Ordinal);
                    foreach(string id in unselected) {
                        var unit=s.HarvestUnits.Single(x=>x.Id==id);
                        if(unit.Status==HarvestUnitStatus.Available)PutHarvestUnit(s,unit.WithStatus(HarvestUnitStatus.Forfeited));
                    }
                }
                if(work>=attempt.Duration)FinishHarvest(s,attempt,attempt.WithWork(s.RuleClock,attempt.Duration,HarvestAttemptStatus.Working));
                else PutHarvestAttempt(s,attempt.WithWork(s.RuleClock,work,HarvestAttemptStatus.Working));
            }
        }

        private void FinishHarvest(Snapshot s,HarvestAttemptRecord prior,HarvestAttemptRecord completed)
        {
            var actorFacts=CharacterStateFacts.ForActor(s,prior.WorkerId,"fishing-tackle");
            int injury=actorFacts.InjuryPenalty(CharacterAbility.Intelligence,toolCheck:true);
            int modifier=checked(prior.AbilityModifier+prior.ProficiencyBonus+injury);
            int disadvantage=(TestOnlyClubAttackPolicy.ConditionsFor(s,prior.WorkerId).View().Has(ConditionKind.Poisoned)?1:0)
                +(prior.ProficiencyRank==0?1:0);
            uint randomBefore=s.RandomState;
            var roll=PlaytestDice.RollD20(randomBefore,disadvantageSources:disadvantage);
            var check=PlaytestRolls.TaskCheck(roll.Natural,modifier,prior.CheckDc);
            s.RandomState=roll.NextRandomState;
            HarvestAttemptStatus status=check.Degree==TaskDegree.CriticalSuccess?HarvestAttemptStatus.CriticalSuccess
                :check.Degree==TaskDegree.Success?HarvestAttemptStatus.Success
                :check.Degree==TaskDegree.Failure?HarvestAttemptStatus.Failure:HarvestAttemptStatus.CriticalFailure;
            int d4=0,wound=0,injuryRoll=0;long damage=0,words=roll.WordsConsumed;
            if(status==HarvestAttemptStatus.CriticalFailure) {
                var draw=DiceStream.Draw(s.RandomState,4);d4=draw.Value+1;damage=d4;
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
            var manifest=s.HarvestManifests.Single(x=>x.Id==prior.ManifestId);
            var donor=s.HarvestDonors.Single(x=>x.CreatureId==manifest.CreatureId);
            var body=s.FishingCreatures.Single(x=>x.Id==manifest.CreatureId);
            var selectedUnits=prior.SelectedUnitIds.Select(id=>s.HarvestUnits.Single(x=>x.Id==id)).ToArray();
            var baseline=selectedUnits.Where(x=>x.Condition==HarvestUnitCondition.Intact).ToArray();
            var outputUnits=new System.Collections.Generic.List<HarvestMaterialUnitRecord>();
            if(status==HarvestAttemptStatus.Success||status==HarvestAttemptStatus.CriticalSuccess) {
                outputUnits.AddRange(baseline);
                if(status==HarvestAttemptStatus.CriticalSuccess) {
                    var damaged=selectedUnits.Where(x=>x.Condition==HarvestUnitCondition.DamagedPotentiallyRecoverable).ToArray();
                    if(damaged.Length>0)outputUnits.Add(damaged.SingleOrDefault(x=>x.Id==prior.CriticalRecoveryPreference)??damaged.Single());
                }
            }
            if(outputUnits.Count>0) {
                RuleQuantity extractedMass=RuleQuantity.Sum(outputUnits.Select(x=>x.MassPounds));
                if(body.MassPounds<extractedMass)throw new InvalidOperationException("Harvest exceeded the actual remains mass.");
                foreach(var unit in outputUnits) {
                    RuleTime freshUntil=unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds);
                    s.Work=new WorkLedger(s.Work.Lots.Concat(new[]{new ResourceLot(unit.Id,SharedHarvestFixture.MaterialUnit,
                        unit.MassPounds,manifest.ContainerId,donor.OwnerId)}),s.Work.WorkerIntervals,s.Work.Reservations);
                    s.InventoryLots=s.InventoryLots.Concat(new[]{new InventoryLotRecord(unit.Id,"",donor.OwnerId,unit.MassPounds,
                        s.RuleClock,NutritionKind.None,freshUntil,InventoryAccess.Stowed)}).ToArray();
                    var container=s.PortableEquipment.Single(x=>x.Id==manifest.ContainerId);
                    s.PortableEquipment=s.PortableEquipment.Concat(new[]{new PortableEquipmentRecord(unit.Id,
                        "prototype.generic-pound-lot",donor.OwnerId,donor.OwnerId,container.Id,PortablePlacement.Contained,
                        PortableLinkKind.InventoryLot,unit.Id,PortableMassBasis.GenericPounds,unit.MassPounds,null)}).ToArray();
                    PutHarvestUnit(s,unit.WithStatus(HarvestUnitStatus.Extracted));
                }
                s.FishingCreatures=s.FishingCreatures.Select(x=>x.Id==body.Id?x.WithMassPounds(x.MassPounds-extractedMass):x).ToArray();
            } else if(status==HarvestAttemptStatus.Failure) {
                if(s.SchemaVersion<Snapshot.HarvestManifestSchema) {
                    PutHarvestUnit(s,s.HarvestUnits.Single(x=>x.Id==prior.UnitId).WithStatus(HarvestUnitStatus.Ruined));
                } else {
                    long highest=baseline.Where(x=>x.ValueCopper.HasValue).Select(x=>x.ValueCopper.Value).DefaultIfEmpty(long.MinValue).Max();
                    var top=baseline.Where(x=>x.ValueCopper==highest).ToArray();
                    var victim=top.Length==1?top[0]:top.Single(x=>x.Id==prior.FailureVictimPreference);
                    foreach(var unit in baseline)PutHarvestUnit(s,unit.WithStatus(unit.Id==victim.Id?HarvestUnitStatus.Ruined:HarvestUnitStatus.Exhausted));
                }
            } else if(status==HarvestAttemptStatus.CriticalFailure) {
                foreach(var unit in baseline)PutHarvestUnit(s,unit.WithStatus(HarvestUnitStatus.Ruined));
            }
            HarvestCheckDegree degree=check.Degree==TaskDegree.CriticalFailure?HarvestCheckDegree.CriticalFailure
                :check.Degree==TaskDegree.Failure?HarvestCheckDegree.Failure
                :check.Degree==TaskDegree.Success?HarvestCheckDegree.Success:HarvestCheckDegree.CriticalSuccess;
            PutHarvestAttempt(s,completed.WithResult(s.RuleClock,status,
                degree,
                roll.Selection==D20Selection.Normal?HarvestDiceSelection.Normal:HarvestDiceSelection.Disadvantage,
                roll.First,roll.Second??0,roll.Natural,modifier,d4,damage,d4==0?"":"piercing",wound,injuryRoll,
                randomBefore,s.RandomState,words));
            ReconcileDyingCadences(s);PauseIncompatibleWork(s);
        }

        private sealed class HarvestAssessment
        {
            public HarvestManifestRecord Manifest;
            public HarvestCategoryRecord[] Categories;
            public HarvestMaterialUnitRecord[] Selected;
            public HarvestAttemptRecord Current;
            public string[] CategoryIds;
            public string[] UnitIds;
            public string FailurePreference;
            public string CriticalPreference;
            public RuleTime Duration;
            public int AbilityModifier;
            public int ProficiencyRank;
            public int ProficiencyBonus;
        }

        private string AssessHarvestCommand(Snapshot s,Command c,out HarvestAssessment facts)
        {
            facts=null;
            if(harvestFixture==null||s.SchemaVersion!=harvestFixture.SchemaVersion)return "HarvestingNotSelected";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.OverwatchRider!=OverwatchRider.None
                ||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.ExpeditionAssignment!=null||c.X!=0||c.Y!=0)
                return "InvalidHarvestCommand";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Kind==CommandKind.StartHarvest) {
                HarvestManifestRecord manifest;
                HarvestCategoryRecord[] categories;
                string failurePreference="",criticalPreference="";
                if(s.SchemaVersion>=Snapshot.HarvestManifestSchema) {
                    if(c.HarvestSelection==null)return "HarvestSelectionRequired";
                    manifest=s.HarvestManifests.SingleOrDefault(x=>x.Id==c.Target);
                    if(manifest==null)return "UnknownHarvestManifest";
                    if(c.HarvestSelection.ManifestVersionId!=manifest.AnatomyVersionId)return "HarvestManifestVersionMismatch";
                    string[] requested=c.HarvestSelection.CategoryIds;
                    categories=s.HarvestCategories.Where(x=>x.ManifestId==manifest.Id&&requested.Contains(x.Id,StringComparer.Ordinal)).ToArray();
                    if(categories.Length!=requested.Length)return "UnknownHarvestCategory";
                    failurePreference=c.HarvestSelection.FailureVictimPreference;
                    criticalPreference=c.HarvestSelection.CriticalRecoveryPreference;
                } else {
                    if(c.HarvestSelection!=null)return "InvalidHarvestCommand";
                    var category=s.HarvestCategories.SingleOrDefault(x=>x.Id==c.Target);
                    if(category==null)return "UnknownHarvestCategory";
                    manifest=s.HarvestManifests.Single(x=>x.Id==category.ManifestId);
                    categories=new[]{category};
                }
                var selected=s.HarvestUnits.Where(x=>categories.Any(ca=>ca.UnitIds.Contains(x.Id,StringComparer.Ordinal))).ToArray();
                if(categories.Any(x=>x.AllocationUnits<1)||selected.Length==0)return "HarvestSelectionInvalid";
                if(s.HarvestAttempts.Any(x=>x.ManifestId==manifest.Id))return "HarvestSelectionExhausted";
                var intact=selected.Where(x=>x.Condition==HarvestUnitCondition.Intact).ToArray();
                var damaged=selected.Where(x=>x.Condition==HarvestUnitCondition.DamagedPotentiallyRecoverable).ToArray();
                if(intact.Length==0||selected.Any(x=>x.Status!=HarvestUnitStatus.Available
                    &&(x.Condition==HarvestUnitCondition.Intact||x.Condition==HarvestUnitCondition.DamagedPotentiallyRecoverable)))return "HarvestUnitUnavailable";
                string[] categoryIds=categories.Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
                string[] unitIds=selected.Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
                if(s.SchemaVersion>=Snapshot.HarvestManifestSchema) {
                    if(intact.Length>1&&intact.Any(x=>!x.ValueCopper.HasValue))return "HarvestFailureValueUnranked";
                    long highest=intact.Where(x=>x.ValueCopper.HasValue).Select(x=>x.ValueCopper.Value).DefaultIfEmpty(long.MinValue).Max();
                    var highestUnits=intact.Where(x=>x.ValueCopper==highest).ToArray();
                    if(highestUnits.Length>1&&(failurePreference==""||!highestUnits.Any(x=>x.Id==failurePreference)))return "HarvestFailureTieChoiceRequired";
                    if(failurePreference!=""&&!highestUnits.Any(x=>x.Id==failurePreference))return "InvalidHarvestFailurePreference";
                    if(damaged.Length>1&&(criticalPreference==""||!damaged.Any(x=>x.Id==criticalPreference)))return "HarvestCriticalRecoveryChoiceRequired";
                    if(criticalPreference!=""&&!damaged.Any(x=>x.Id==criticalPreference))return "InvalidHarvestCriticalRecoveryPreference";
                }
                string access=HarvestAccess(s,c.Actor,manifest,selectedUnitIds:unitIds);if(access!=null)return access;
                var check=AbilityCheckRules.Derive(s,c.Actor,"fishing-tackle",CharacterAbility.Intelligence);
                facts=new HarvestAssessment { Manifest=manifest,Categories=categories,Selected=selected,CategoryIds=categoryIds,UnitIds=unitIds,
                    FailurePreference=failurePreference,CriticalPreference=criticalPreference,
                    Duration=HarvestValidation.Duration(manifest.FullTimeSeconds,s.HarvestCategories.Count(x=>x.ManifestId==manifest.Id),categories.Length),
                    AbilityModifier=check.AbilityModifier,ProficiencyRank=check.ProficiencyRank,ProficiencyBonus=check.ProficiencyBonus };
                return null;
            }
            var current=s.HarvestAttempts.SingleOrDefault(x=>x.Id==c.Target&&x.WorkerId==c.Actor);
            if(current==null)return "UnknownHarvestAttempt";
            if(c.HarvestSelection!=null)return "InvalidHarvestCommand";
            if(c.Kind==CommandKind.PauseHarvest) {
                if(current.Status!=HarvestAttemptStatus.Working)return "HarvestNotWorking";
                facts=new HarvestAssessment { Current=current };return null;
            }
            if(c.Kind!=CommandKind.ResumeHarvest)return "InvalidHarvestCommand";
            if(current.Status!=HarvestAttemptStatus.Paused)return "HarvestNotPaused";
            var manifestToResume=s.HarvestManifests.Single(x=>x.Id==current.ManifestId);
            string resumeAccess=HarvestAccess(s,c.Actor,manifestToResume,current.Id,current.SelectedUnitIds);if(resumeAccess!=null)return resumeAccess;
            facts=new HarvestAssessment { Current=current,Manifest=manifestToResume };
            return null;
        }

        private string ResolveHarvest(Snapshot s,Command c)
        {
            string error=AssessHarvestCommand(s,c,out var facts);if(error!=null)return error;
            if(c.Kind==CommandKind.StartHarvest) {
                var manifest=facts.Manifest;
                var primary=facts.Selected.Where(x=>x.Condition==HarvestUnitCondition.Intact).OrderBy(x=>x.Id,StringComparer.Ordinal).First();
                string id=HarvestWorkId(s.Revision+1);
                var attempt=new HarvestAttemptRecord(id,c.Actor,manifest.Id,facts.CategoryIds[0],primary.Id,s.RuleClock,s.RuleClock,facts.Duration,
                    default,HarvestAttemptStatus.Working,facts.AbilityModifier,
                    facts.ProficiencyRank,facts.ProficiencyBonus,manifest.RequiredDc,null,HarvestCheckDegree.None,HarvestDiceSelection.None,
                    0,0,0,0,0,0,"",0,0,0,0,0,facts.CategoryIds,facts.UnitIds,facts.FailurePreference,facts.CriticalPreference);
                BookHarvest(s,attempt);s.HarvestAttempts=s.HarvestAttempts.Concat(new[]{attempt}).ToArray();return null;
            }
            var current=facts.Current;
            if(c.Kind==CommandKind.PauseHarvest) {
                PauseHarvest(s,current);return null;
            }
            BookHarvest(s,current.WithWork(s.RuleClock,current.WorkDone,HarvestAttemptStatus.Working));
            PutHarvestAttempt(s,current.WithWork(s.RuleClock,current.WorkDone,HarvestAttemptStatus.Working));return null;
        }
    }
}
#endif
