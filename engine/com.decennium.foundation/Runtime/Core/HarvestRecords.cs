using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    public enum HarvestOriginRestriction { Ordinary, ConsentRequired, AuthorityRequired, Prohibited }
    public enum HarvestSize { Tiny, Small, Medium, Large, Huge, Gargantuan }
    public enum HarvestUnitCondition { Intact, DamagedPotentiallyRecoverable, DamagedUnavailable, Unavailable }
    public enum HarvestPreservationState { Fresh, Degraded, Spoiled }
    public enum HarvestUnitStatus { Available, Forfeited, Ruined, Extracted, Exhausted }
    public enum HarvestAttemptStatus { Working, Paused, Success, CriticalSuccess, Failure, CriticalFailure, Cancelled }
    public enum HarvestCheckDegree { None, CriticalFailure, Failure, Success, CriticalSuccess }
    public enum HarvestDiceSelection { None, Normal, Disadvantage }

    /// <summary>One immutable source-size yield roll, resolved when a finite manifest is made.</summary>
    public sealed class HarvestYieldResolution
    {
        private readonly int[] diceFaces;
        public HarvestSize Size { get; }
        public int Units { get; }
        public int[] DiceFaces => diceFaces.ToArray();
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public HarvestYieldResolution(HarvestSize size,int units,int[] diceFaces,uint randomBefore,uint randomAfter,long wordsConsumed)
        {
            this.diceFaces=(diceFaces??Array.Empty<int>()).ToArray();
            if(!Enum.IsDefined(typeof(HarvestSize),size)||units<1||units>32||wordsConsumed<0)
                throw new ArgumentException("Invalid harvest yield resolution.");
            Size=size;Units=units;RandomBefore=randomBefore;RandomAfter=randomAfter;WordsConsumed=wordsConsumed;
        }
    }

    /// <summary>Source-bound size timing and once-only finite base-yield dice.</summary>
    public static class HarvestYieldRules
    {
        public static int FullTimeSeconds(HarvestSize size)
        {
            switch(size) {
                case HarvestSize.Tiny:return 10*60;
                case HarvestSize.Small:return 20*60;
                case HarvestSize.Medium:return 30*60;
                case HarvestSize.Large:return 60*60;
                case HarvestSize.Huge:return 2*60*60;
                case HarvestSize.Gargantuan:return 4*60*60;
                default:throw new ArgumentOutOfRangeException(nameof(size));
            }
        }
        public static int DiceCount(HarvestSize size)
        {
            switch(size) {
                case HarvestSize.Tiny:return 0;
                case HarvestSize.Small:case HarvestSize.Medium:return 1;
                case HarvestSize.Large:return 2;
                case HarvestSize.Huge:return 4;
                case HarvestSize.Gargantuan:return 8;
                default:throw new ArgumentOutOfRangeException(nameof(size));
            }
        }
        public static int DieSides(HarvestSize size)
        {
            switch(size) {
                case HarvestSize.Small:return 2;
                case HarvestSize.Medium:case HarvestSize.Large:case HarvestSize.Huge:case HarvestSize.Gargantuan:return 4;
                case HarvestSize.Tiny:return 0;
                default:throw new ArgumentOutOfRangeException(nameof(size));
            }
        }
        public static HarvestYieldResolution Roll(HarvestSize size,uint randomBefore)
        {
            int dice=DiceCount(size),sides=DieSides(size);
            if(dice==0)return new HarvestYieldResolution(size,1,Array.Empty<int>(),0,0,0);
            if(randomBefore==0)throw new ArgumentException("A variable harvest yield requires a nonzero RNG state.",nameof(randomBefore));
            uint state=randomBefore;long words=0;var faces=new int[dice];int total=0;
            for(int i=0;i<dice;i++) {
                var draw=DiceStream.Draw(state,sides);faces[i]=draw.Value+1;total=checked(total+faces[i]);
                state=draw.NextState;words=checked(words+draw.WordsConsumed);
            }
            return new HarvestYieldResolution(size,total,faces,randomBefore,state,words);
        }
        public static bool Matches(HarvestManifestRecord manifest)
        {
            if(manifest==null||manifest.FullTimeSeconds!=FullTimeSeconds(manifest.Size))return false;
            try {
                var expected=Roll(manifest.Size,manifest.YieldRandomBefore);
                return expected.Units==manifest.BaseYieldUnits&&expected.DiceFaces.SequenceEqual(manifest.BaseYieldDice)
                    &&expected.RandomBefore==manifest.YieldRandomBefore&&expected.RandomAfter==manifest.YieldRandomAfter
                    &&expected.WordsConsumed==manifest.YieldWordsConsumed;
            } catch(ArgumentException) { return false; }
        }
    }

    /// <summary>Provenance for actual remains. Creature identity, current mass, physical location,
    /// custody and life state remain on the linked FishingCreatureBodyRecord.</summary>
    public sealed class HarvestDonorRecord
    {
        public string CreatureId { get; }
        public string LifecycleEventId { get; }
        public RuleTime DeathAt { get; }
        public HarvestOriginRestriction OriginRestriction { get; }
        public string AnatomyProfileId { get; }
        public string OwnerId { get; }
        public RuleQuantity OriginalMassPounds { get; }
        public HarvestDonorRecord(string creatureId,string lifecycleEventId,RuleTime deathAt,
            HarvestOriginRestriction originRestriction,string anatomyProfileId,string ownerId,RuleQuantity originalMassPounds)
        {
            foreach(string value in new[]{creatureId,lifecycleEventId,anatomyProfileId,ownerId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid harvest donor provenance identity.");
            if(!Enum.IsDefined(typeof(HarvestOriginRestriction),originRestriction)||originalMassPounds<=default(RuleQuantity))
                throw new ArgumentException("Invalid harvest donor provenance.");
            CreatureId=creatureId;LifecycleEventId=lifecycleEventId;DeathAt=deathAt;OriginRestriction=originRestriction;
            AnatomyProfileId=anatomyProfileId;OwnerId=ownerId;OriginalMassPounds=originalMassPounds;
        }
    }

    /// <summary>A precommitted finite manifest. Yield is resolved once before any check; this
    /// record stores the resolved count and the authored full-duration profile.</summary>
    public sealed class HarvestManifestRecord
    {
        private readonly int[] baseYieldDice;
        public string Id { get; }
        public string CreatureId { get; }
        public string AnatomyVersionId { get; }
        public HarvestSize Size { get; }
        public RuleTime CreatedAt { get; }
        public int RequiredDc { get; }
        public int FullTimeSeconds { get; }
        public int BaseYieldUnits { get; }
        public int[] BaseYieldDice=>baseYieldDice.ToArray();
        public uint YieldRandomBefore { get; }
        public uint YieldRandomAfter { get; }
        public long YieldWordsConsumed { get; }
        public string SiteId { get; }
        public string ToolkitId { get; }
        public string KnifeId { get; }
        public string ContainerId { get; }
        public string WorkSurfaceId { get; }
        public HarvestManifestRecord(string id,string creatureId,string anatomyVersionId,HarvestSize size,RuleTime createdAt,
            int requiredDc,int fullTimeSeconds,int baseYieldUnits,string siteId,string toolkitId,string knifeId,string containerId,string workSurfaceId)
            :this(id,creatureId,anatomyVersionId,size,createdAt,requiredDc,fullTimeSeconds,baseYieldUnits,siteId,toolkitId,
                knifeId,containerId,workSurfaceId,null)
        { }
        public HarvestManifestRecord(string id,string creatureId,string anatomyVersionId,HarvestSize size,RuleTime createdAt,
            int requiredDc,int fullTimeSeconds,int baseYieldUnits,string siteId,string toolkitId,string knifeId,string containerId,
            string workSurfaceId,HarvestYieldResolution yield)
        {
            foreach(string value in new[]{id,creatureId,anatomyVersionId,siteId,toolkitId,knifeId,containerId,workSurfaceId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid harvest manifest identity.");
            if(!Enum.IsDefined(typeof(HarvestSize),size)||requiredDc<1||requiredDc>100||fullTimeSeconds<1||fullTimeSeconds>14400
                ||baseYieldUnits<1||baseYieldUnits>128)throw new ArgumentException("Invalid finite harvest manifest.");
            Id=id;CreatureId=creatureId;AnatomyVersionId=anatomyVersionId;Size=size;CreatedAt=createdAt;
            RequiredDc=requiredDc;FullTimeSeconds=fullTimeSeconds;BaseYieldUnits=baseYieldUnits;SiteId=siteId;
            ToolkitId=toolkitId;KnifeId=knifeId;ContainerId=containerId;WorkSurfaceId=workSurfaceId;
            if(yield!=null&&(yield.Size!=size||yield.Units!=baseYieldUnits))throw new ArgumentException("Harvest yield does not match its manifest.");
            baseYieldDice=yield?.DiceFaces??Array.Empty<int>();YieldRandomBefore=yield?.RandomBefore??0;
            YieldRandomAfter=yield?.RandomAfter??0;YieldWordsConsumed=yield?.WordsConsumed??0;
        }
    }

    /// <summary>A real category and its fixed unit allocation inside one finite manifest.</summary>
    public sealed class HarvestCategoryRecord
    {
        private readonly string[] unitIds;
        public string Id { get; }
        public string ManifestId { get; }
        public string CategoryId { get; }
        public int AllocationUnits { get; }
        public string[] UnitIds=>unitIds.ToArray();
        public HarvestCategoryRecord(string id,string manifestId,string categoryId,int allocationUnits,string[] unitIds)
        {
            var rows=unitIds??Array.Empty<string>();
            if(!Validation.ValidId(id)||!Validation.ValidId(manifestId)||!Validation.ValidId(categoryId)
                ||allocationUnits<1||allocationUnits>128||rows.Length<1||rows.Length>128
                ||rows.Any(x=>!Validation.ValidId(x))||rows.Distinct(StringComparer.Ordinal).Count()!=rows.Length)
                throw new ArgumentException("Invalid harvest category allocation.");
            Id=id;ManifestId=manifestId;CategoryId=categoryId;AllocationUnits=allocationUnits;this.unitIds=rows.ToArray();
        }
    }

    /// <summary>Finite anatomy unit. A successful extraction settles the existing unit identity
    /// into an ordinary ResourceLot/InventoryLotRecord with the same ID; no parallel inventory is made.</summary>
    public sealed class HarvestMaterialUnitRecord
    {
        public string Id { get; }
        public string ManifestId { get; }
        public string CategoryId { get; }
        public string MaterialId { get; }
        public int Tier { get; }
        public RuleQuantity MassPounds { get; }
        public long? ValueCopper { get; }
        public HarvestUnitCondition Condition { get; }
        public HarvestUnitStatus Status { get; }
        public int PreservationIntervalSeconds { get; }
        public RuleTime OriginAt { get; }
        public HarvestMaterialUnitRecord(string id,string manifestId,string categoryId,string materialId,int tier,
            RuleQuantity massPounds,long? valueCopper,HarvestUnitCondition condition,HarvestUnitStatus status,
            int preservationIntervalSeconds,RuleTime originAt)
        {
            foreach(string value in new[]{id,manifestId,categoryId,materialId})if(!Validation.ValidId(value))throw new ArgumentException("Invalid harvest material identity.");
            if(tier<1||tier>6||massPounds<=default(RuleQuantity)||valueCopper<0
                ||!Enum.IsDefined(typeof(HarvestUnitCondition),condition)||!Enum.IsDefined(typeof(HarvestUnitStatus),status)
                ||preservationIntervalSeconds<1||preservationIntervalSeconds>31536000)
                throw new ArgumentException("Invalid harvest material unit.");
            Id=id;ManifestId=manifestId;CategoryId=categoryId;MaterialId=materialId;Tier=tier;MassPounds=massPounds;
            ValueCopper=valueCopper;Condition=condition;Status=status;PreservationIntervalSeconds=preservationIntervalSeconds;OriginAt=originAt;
        }
        public HarvestMaterialUnitRecord WithStatus(HarvestUnitStatus status)
            =>new HarvestMaterialUnitRecord(Id,ManifestId,CategoryId,MaterialId,Tier,MassPounds,ValueCopper,Condition,status,
                PreservationIntervalSeconds,OriginAt);
        public HarvestPreservationState PreservationAt(RuleTime at)
        {
            RuleTime degradedAt=OriginAt.AddSeconds(PreservationIntervalSeconds);
            RuleTime spoiledAt=OriginAt.AddSeconds(checked(PreservationIntervalSeconds*2));
            return at<degradedAt?HarvestPreservationState.Fresh:at<spoiledAt?HarvestPreservationState.Degraded:HarvestPreservationState.Spoiled;
        }
    }

    /// <summary>One extraction attempt with the exact skill, duration, roll and consequence receipt.</summary>
    public sealed class HarvestAttemptRecord
    {
        private readonly string[] selectedCategoryIds;
        private readonly string[] selectedUnitIds;
        public string Id { get; }
        public string WorkerId { get; }
        public string ManifestId { get; }
        public string CategoryId { get; }
        public string UnitId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime Duration { get; }
        public RuleTime WorkDone { get; }
        public HarvestAttemptStatus Status { get; }
        public int AbilityModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int CheckDc { get; }
        public RuleTime? CompletedAt { get; }
        public HarvestCheckDegree Degree { get; }
        public HarvestDiceSelection DiceSelection { get; }
        public int FirstDie { get; }
        public int SecondDie { get; }
        public int Natural { get; }
        public int CheckModifier { get; }
        public int D4Rolled { get; }
        public long DamageApplied { get; }
        public string AccidentDamageType { get; }
        public int WoundRoll { get; }
        public int InjuryRoll { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public string[] SelectedCategoryIds=>selectedCategoryIds.ToArray();
        public string[] SelectedUnitIds=>selectedUnitIds.ToArray();
        public string FailureVictimPreference { get; }
        public string CriticalRecoveryPreference { get; }
        public HarvestAttemptRecord(string id,string workerId,string manifestId,string categoryId,string unitId,
            RuleTime startedAt,RuleTime updatedAt,RuleTime duration,RuleTime workDone,HarvestAttemptStatus status,
            int abilityModifier,int proficiencyRank,int proficiencyBonus,int checkDc,RuleTime? completedAt,
            HarvestCheckDegree degree,HarvestDiceSelection diceSelection,int firstDie,int secondDie,int natural,
            int checkModifier,int d4Rolled,long damageApplied,string accidentDamageType,int woundRoll,int injuryRoll,uint randomBefore,uint randomAfter,long wordsConsumed,
            string[] selectedCategoryIds=null,string[] selectedUnitIds=null,string failureVictimPreference="",string criticalRecoveryPreference="")
        {
            foreach(string value in new[]{id,workerId,manifestId,categoryId,unitId})if(!Validation.ValidId(value))throw new ArgumentException("Invalid harvest attempt identity.");
            if(!Enum.IsDefined(typeof(HarvestAttemptStatus),status)||!Enum.IsDefined(typeof(HarvestCheckDegree),degree)
                ||!Enum.IsDefined(typeof(HarvestDiceSelection),diceSelection)||startedAt>updatedAt||duration<=default(RuleTime)
                ||workDone<default(RuleTime)||workDone>duration||proficiencyRank<0||proficiencyRank>2
                ||proficiencyBonus<0||proficiencyBonus>20||checkDc<1||checkDc>100||firstDie<0||firstDie>20||secondDie<0||secondDie>20
                ||natural<0||natural>20||d4Rolled<0||d4Rolled>4||damageApplied<0||woundRoll<0||woundRoll>20
                ||injuryRoll<0||injuryRoll>6||wordsConsumed<0||accidentDamageType==null
                ||failureVictimPreference==null||criticalRecoveryPreference==null
                ||failureVictimPreference!=""&&!Validation.ValidId(failureVictimPreference)
                ||criticalRecoveryPreference!=""&&!Validation.ValidId(criticalRecoveryPreference)
                ||(d4Rolled==0)!=(accidentDamageType=="")||d4Rolled!=0&&accidentDamageType!="piercing")
                throw new ArgumentException("Invalid harvest attempt.");
            var categories=(selectedCategoryIds??new[]{categoryId}).ToArray();
            var units=(selectedUnitIds??new[]{unitId}).ToArray();
            if(categories.Length<1||categories.Length>HarvestValidation.MaxRecords||units.Length<1||units.Length>HarvestValidation.MaxRecords
                ||categories.Any(x=>!Validation.ValidId(x))||units.Any(x=>!Validation.ValidId(x))
                ||categories.Distinct(StringComparer.Ordinal).Count()!=categories.Length
                ||units.Distinct(StringComparer.Ordinal).Count()!=units.Length
                ||!categories.Contains(categoryId,StringComparer.Ordinal)||!units.Contains(unitId,StringComparer.Ordinal))
                throw new ArgumentException("Invalid harvest selection receipt.");
            bool resolved=status==HarvestAttemptStatus.Success||status==HarvestAttemptStatus.CriticalSuccess
                ||status==HarvestAttemptStatus.Failure||status==HarvestAttemptStatus.CriticalFailure;
            bool diceValid=resolved&&(diceSelection==HarvestDiceSelection.Normal?secondDie==0&&natural==firstDie
                :diceSelection==HarvestDiceSelection.Disadvantage&&secondDie>=1&&natural==Math.Min(firstDie,secondDie));
            if(resolved!=(completedAt.HasValue&&degree!=HarvestCheckDegree.None&&diceSelection!=HarvestDiceSelection.None
                &&firstDie>=1&&natural>=1&&randomBefore!=0&&randomAfter!=0&&wordsConsumed>0)
                ||resolved&&!diceValid
                ||!resolved&&(completedAt.HasValue||degree!=HarvestCheckDegree.None||diceSelection!=HarvestDiceSelection.None
                    ||firstDie!=0||secondDie!=0||natural!=0||checkModifier!=0||randomBefore!=0||randomAfter!=0||wordsConsumed!=0)
                ||completedAt.HasValue&&(completedAt.Value!=updatedAt||workDone!=duration)
                ||resolved&&((status==HarvestAttemptStatus.Success)!=(degree==HarvestCheckDegree.Success)
                    ||(status==HarvestAttemptStatus.CriticalSuccess)!=(degree==HarvestCheckDegree.CriticalSuccess)
                    ||(status==HarvestAttemptStatus.Failure)!=(degree==HarvestCheckDegree.Failure)
                    ||(status==HarvestAttemptStatus.CriticalFailure)!=(degree==HarvestCheckDegree.CriticalFailure))
                ||(status==HarvestAttemptStatus.CriticalFailure)!=(d4Rolled!=0)
                ||(d4Rolled==0&&(damageApplied!=0||woundRoll!=0||injuryRoll!=0)))
                throw new ArgumentException("Harvest result does not match its persisted check.");
            Id=id;WorkerId=workerId;ManifestId=manifestId;CategoryId=categoryId;UnitId=unitId;StartedAt=startedAt;UpdatedAt=updatedAt;
            Duration=duration;WorkDone=workDone;Status=status;AbilityModifier=abilityModifier;ProficiencyRank=proficiencyRank;
            ProficiencyBonus=proficiencyBonus;CheckDc=checkDc;CompletedAt=completedAt;Degree=degree;DiceSelection=diceSelection;
            FirstDie=firstDie;SecondDie=secondDie;Natural=natural;CheckModifier=checkModifier;D4Rolled=d4Rolled;
            DamageApplied=damageApplied;AccidentDamageType=accidentDamageType;WoundRoll=woundRoll;InjuryRoll=injuryRoll;RandomBefore=randomBefore;RandomAfter=randomAfter;WordsConsumed=wordsConsumed;
            this.selectedCategoryIds=categories.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            this.selectedUnitIds=units.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            FailureVictimPreference=failureVictimPreference;CriticalRecoveryPreference=criticalRecoveryPreference;
        }
        public HarvestAttemptRecord WithWork(RuleTime at,RuleTime work,HarvestAttemptStatus status)
            =>new HarvestAttemptRecord(Id,WorkerId,ManifestId,CategoryId,UnitId,StartedAt,at,Duration,work,status,
                AbilityModifier,ProficiencyRank,ProficiencyBonus,CheckDc,null,HarvestCheckDegree.None,HarvestDiceSelection.None,
                0,0,0,0,0,0,"",0,0,0,0,0,selectedCategoryIds,selectedUnitIds,FailureVictimPreference,CriticalRecoveryPreference);
        public HarvestAttemptRecord WithResult(RuleTime at,HarvestAttemptStatus status,HarvestCheckDegree degree,
            HarvestDiceSelection selection,int first,int second,int natural,int modifier,int d4,long damage,string damageType,int wound,int injury,
            uint randomBefore,uint randomAfter,long words)
            =>new HarvestAttemptRecord(Id,WorkerId,ManifestId,CategoryId,UnitId,StartedAt,at,Duration,Duration,status,
                AbilityModifier,ProficiencyRank,ProficiencyBonus,CheckDc,at,degree,selection,first,second,natural,modifier,
                d4,damage,damageType,wound,injury,randomBefore,randomAfter,words,selectedCategoryIds,selectedUnitIds,FailureVictimPreference,CriticalRecoveryPreference);
        public HarvestAttemptRecord WithCancelled(RuleTime at)
            =>new HarvestAttemptRecord(Id,WorkerId,ManifestId,CategoryId,UnitId,StartedAt,at,Duration,WorkDone,
                HarvestAttemptStatus.Cancelled,AbilityModifier,ProficiencyRank,ProficiencyBonus,CheckDc,null,
                HarvestCheckDegree.None,HarvestDiceSelection.None,0,0,0,0,0,0,"",0,0,0,0,0,selectedCategoryIds,selectedUnitIds,FailureVictimPreference,CriticalRecoveryPreference);
    }

    public static class HarvestValidation
    {
        public const int MaxRecords=32;
        private static HarvestCheckDegree Grade(int natural,int modifier,int dc)
        {
            long total=(long)natural+modifier;
            HarvestCheckDegree degree=total>=((long)dc+10)?HarvestCheckDegree.CriticalSuccess
                :total>=dc?HarvestCheckDegree.Success:total<=((long)dc-10)?HarvestCheckDegree.CriticalFailure:HarvestCheckDegree.Failure;
            if(natural==20&&degree<HarvestCheckDegree.CriticalSuccess)degree=(HarvestCheckDegree)((int)degree+1);
            else if(natural==1&&degree>HarvestCheckDegree.CriticalFailure)degree=(HarvestCheckDegree)((int)degree-1);
            return degree;
        }
        public static void Validate(Snapshot s)
        {
            if(s.HarvestDonors==null||s.HarvestManifests==null||s.HarvestCategories==null||s.HarvestUnits==null||s.HarvestAttempts==null
                ||new[]{s.HarvestDonors.Length,s.HarvestManifests.Length,s.HarvestCategories.Length,s.HarvestUnits.Length,s.HarvestAttempts.Length}.Any(x=>x>MaxRecords)
                ||s.HarvestDonors.Any(x=>x==null)||s.HarvestManifests.Any(x=>x==null)||s.HarvestCategories.Any(x=>x==null)
                ||s.HarvestUnits.Any(x=>x==null)||s.HarvestAttempts.Any(x=>x==null))throw new ArgumentException("Invalid finite-harvest collections.");
            if(s.SchemaVersion<Snapshot.HarvestSchema) {
                if(s.HarvestDonors.Length+s.HarvestManifests.Length+s.HarvestCategories.Length+s.HarvestUnits.Length+s.HarvestAttempts.Length!=0)
                    throw new ArgumentException("Harvesting requires schema41.");
                return;
            }
            if(s.HarvestDonors.Select(x=>x.CreatureId).Distinct(StringComparer.Ordinal).Count()!=s.HarvestDonors.Length
                ||s.HarvestManifests.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.HarvestManifests.Length
                ||s.HarvestManifests.Select(x=>x.CreatureId).Distinct(StringComparer.Ordinal).Count()!=s.HarvestManifests.Length
                ||s.HarvestCategories.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.HarvestCategories.Length
                ||s.HarvestUnits.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.HarvestUnits.Length
                ||s.HarvestAttempts.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.HarvestAttempts.Length
                ||s.HarvestAttempts.Select(x=>x.ManifestId).Distinct(StringComparer.Ordinal).Count()!=s.HarvestAttempts.Length)
                throw new ArgumentException("Duplicate finite-harvest identity.");
            foreach(var donor in s.HarvestDonors) {
                var body=s.FishingCreatures.SingleOrDefault(x=>x.Id==donor.CreatureId);
                if(body==null||body.LifeState!=FishingCreatureLifeState.Dead||body.ActiveResponseAttemptId!=""
                    ||body.CapturedByAttemptId!=""||body.ContainerId!=""||body.CustodianId!=donor.OwnerId
                    ||body.MassPounds>donor.OriginalMassPounds||donor.DeathAt>s.RuleClock
                    ||!s.Actors.Any(x=>x.Id==donor.OwnerId))throw new ArgumentException("Harvest donor has no actual eligible dead body or stable custody.");
                var units=s.HarvestUnits.Where(x=>x.ManifestId!=null&&s.HarvestManifests.Any(m=>m.Id==x.ManifestId&&m.CreatureId==donor.CreatureId)).ToArray();
                RuleQuantity extracted=RuleQuantity.Sum(units.Where(x=>x.Status==HarvestUnitStatus.Extracted).Select(x=>x.MassPounds));
                if(body.MassPounds+extracted!=donor.OriginalMassPounds)throw new ArgumentException("Harvest donor mass conservation failed.");
            }
            foreach(var manifest in s.HarvestManifests) {
                var donor=s.HarvestDonors.SingleOrDefault(x=>x.CreatureId==manifest.CreatureId);
                var body=s.FishingCreatures.SingleOrDefault(x=>x.Id==manifest.CreatureId);
                var categories=s.HarvestCategories.Where(x=>x.ManifestId==manifest.Id).ToArray();
                var units=s.HarvestUnits.Where(x=>x.ManifestId==manifest.Id).ToArray();
                bool validProfile=s.SchemaVersion==Snapshot.HarvestSchema
                    ?manifest.Size==HarvestSize.Tiny&&manifest.FullTimeSeconds==600&&manifest.BaseYieldUnits==1
                    :s.SchemaVersion>=Snapshot.HarvestManifestSchema&&HarvestYieldRules.Matches(manifest);
                if(donor==null||body==null||manifest.CreatedAt<donor.DeathAt||manifest.CreatedAt>s.RuleClock||categories.Length<1
                    ||!validProfile
                    ||manifest.RequiredDc!=12||manifest.SiteId!=body.SiteId||donor.AnatomyProfileId!=manifest.AnatomyVersionId
                    ||units.Length<1||units.Length>manifest.BaseYieldUnits+MaxRecords
                    ||categories.SelectMany(x=>x.UnitIds).Distinct(StringComparer.Ordinal).Count()!=units.Length
                    ||categories.SelectMany(x=>x.UnitIds).Any(id=>!units.Any(u=>u.Id==id))
                    ||categories.Any(x=>x.ManifestId!=manifest.Id)
                    ||categories.Sum(x=>x.AllocationUnits)!=manifest.BaseYieldUnits
                    ||units.Any(x=>x.ManifestId!=manifest.Id||x.OriginAt!=donor.DeathAt)
                    ||RuleQuantity.Sum(units.Select(x=>x.MassPounds))>donor.OriginalMassPounds)
                    throw new ArgumentException("Harvest manifest exceeds its actual donor anatomy or fixed allocation.");
            }
            foreach(var category in s.HarvestCategories) {
                var manifest=s.HarvestManifests.SingleOrDefault(x=>x.Id==category.ManifestId);
                var rows=s.HarvestUnits.Where(x=>x.ManifestId==category.ManifestId&&x.CategoryId==category.CategoryId).ToArray();
                if(manifest==null||category.UnitIds.Length!=rows.Length||!category.UnitIds.OrderBy(x=>x,StringComparer.Ordinal)
                    .SequenceEqual(rows.Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal)))throw new ArgumentException("Harvest category allocation is not finite or exact.");
                int baseline=rows.Count(x=>x.Condition==HarvestUnitCondition.Intact);
                if(category.AllocationUnits!=baseline)throw new ArgumentException("Harvest allocation does not match its preregistered ordinary units.");
            }
            foreach(var unit in s.HarvestUnits) {
                var category=s.HarvestCategories.SingleOrDefault(x=>x.ManifestId==unit.ManifestId&&x.CategoryId==unit.CategoryId);
                var attempt=s.HarvestAttempts.SingleOrDefault(x=>x.SelectedUnitIds.Contains(unit.Id,StringComparer.Ordinal));
                var output=s.InventoryLots.SingleOrDefault(x=>x.LotId==unit.Id);
                var physical=s.Work.Lots.SingleOrDefault(x=>x.Id==unit.Id);
                var physicalItem=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id);
                if(category==null||!category.UnitIds.Contains(unit.Id,StringComparer.Ordinal))throw new ArgumentException("Harvest unit has no unique category allocation.");
                if(unit.Status==HarvestUnitStatus.Extracted) {
                    var donor=s.HarvestDonors.Single(x=>x.CreatureId==s.HarvestManifests.Single(m=>m.Id==unit.ManifestId).CreatureId);
                    if(attempt==null||attempt.Status!=HarvestAttemptStatus.Success&&attempt.Status!=HarvestAttemptStatus.CriticalSuccess
                        ||output==null||physical==null||physicalItem==null||physical.UnitId!="mass-pound"
                        ||output.ParentId!=""||output.OwnerId!=donor.OwnerId||output.CreatedAmount!=unit.MassPounds
                        ||physicalItem.LinkKind!=PortableLinkKind.InventoryLot||physicalItem.LinkedId!=unit.Id
                        ||physicalItem.MassBasis!=PortableMassBasis.GenericPounds||physicalItem.OwnerId!=donor.OwnerId
                        ||output.Nutrition!=NutritionKind.None||output.FreshUntil!=unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds))
                        throw new ArgumentException("Extracted material is not settled into its real inventory lot.");
                } else if(output!=null||physical!=null)throw new ArgumentException("Unextracted harvest unit has a phantom inventory lot.");
                if(unit.Status==HarvestUnitStatus.Ruined&&(attempt==null||attempt.Status!=HarvestAttemptStatus.Failure
                    &&attempt.Status!=HarvestAttemptStatus.CriticalFailure))throw new ArgumentException("Ruined harvest unit has no failed attempt.");
                if(unit.Status==HarvestUnitStatus.Exhausted&&(attempt==null||attempt.Status!=HarvestAttemptStatus.Failure
                    ||!attempt.SelectedUnitIds.Contains(unit.Id,StringComparer.Ordinal)))throw new ArgumentException("Exhausted harvest tissue has no claimed failed attempt.");
            }
            foreach(var attempt in s.HarvestAttempts) {
                var manifest=s.HarvestManifests.SingleOrDefault(x=>x.Id==attempt.ManifestId);
                var selectedCategories=s.HarvestCategories.Where(x=>attempt.SelectedCategoryIds.Contains(x.Id,StringComparer.Ordinal)).ToArray();
                var selectedUnits=s.HarvestUnits.Where(x=>attempt.SelectedUnitIds.Contains(x.Id,StringComparer.Ordinal)).ToArray();
                var category=s.HarvestCategories.SingleOrDefault(x=>x.Id==attempt.CategoryId&&x.ManifestId==attempt.ManifestId);
                var unit=s.HarvestUnits.SingleOrDefault(x=>x.Id==attempt.UnitId&&x.ManifestId==attempt.ManifestId);
                bool outputExpected=attempt.Status==HarvestAttemptStatus.Success||attempt.Status==HarvestAttemptStatus.CriticalSuccess;
                bool ruinedExpected=attempt.Status==HarvestAttemptStatus.Failure||attempt.Status==HarvestAttemptStatus.CriticalFailure;
                if(manifest==null||category==null||unit==null||!s.Actors.Any(x=>x.Id==attempt.WorkerId)
                    ||selectedCategories.Length!=attempt.SelectedCategoryIds.Length||selectedUnits.Length!=attempt.SelectedUnitIds.Length
                    ||selectedCategories.Any(x=>x.ManifestId!=manifest.Id)||selectedUnits.Any(x=>x.ManifestId!=manifest.Id)
                    ||selectedCategories.SelectMany(x=>x.UnitIds).Distinct(StringComparer.Ordinal).Count()!=selectedUnits.Length
                    ||!selectedCategories.SelectMany(x=>x.UnitIds).OrderBy(x=>x,StringComparer.Ordinal)
                        .SequenceEqual(attempt.SelectedUnitIds.OrderBy(x=>x,StringComparer.Ordinal))
                    ||!selectedCategories.Any(x=>x.Id==attempt.CategoryId)||!selectedUnits.Any(x=>x.Id==attempt.UnitId)
                    ||!selectedUnits.Any(x=>x.Id==attempt.UnitId&&x.Condition==HarvestUnitCondition.Intact)
                    ||attempt.StartedAt<manifest.CreatedAt||attempt.UpdatedAt>s.RuleClock
                    ||attempt.CheckDc!=manifest.RequiredDc||attempt.Duration!=Duration(manifest.FullTimeSeconds,
                        categories:s.HarvestCategories.Count(x=>x.ManifestId==manifest.Id),selected:selectedCategories.Length)
                    ||outputExpected&&selectedUnits.Where(x=>x.Condition==HarvestUnitCondition.Intact).Any(x=>x.Status!=HarvestUnitStatus.Extracted)
                    ||outputExpected&&attempt.Status==HarvestAttemptStatus.Success&&selectedUnits.Any(x=>x.Condition==HarvestUnitCondition.DamagedPotentiallyRecoverable&&x.Status==HarvestUnitStatus.Extracted)
                    ||ruinedExpected&&attempt.Status==HarvestAttemptStatus.CriticalFailure&&selectedUnits.Where(x=>x.Condition==HarvestUnitCondition.Intact).Any(x=>x.Status!=HarvestUnitStatus.Ruined)
                    ||ruinedExpected&&attempt.Status==HarvestAttemptStatus.Failure&&!selectedUnits.Any(x=>x.Status==HarvestUnitStatus.Ruined)
                    ||!outputExpected&&!ruinedExpected&&selectedUnits.Any(x=>x.Status==HarvestUnitStatus.Extracted||x.Status==HarvestUnitStatus.Ruined||x.Status==HarvestUnitStatus.Exhausted))
                    throw new ArgumentException("Harvest attempt is inconsistent with its fixed selection or settlement.");
                if(s.SchemaVersion>=Snapshot.HarvestManifestSchema) {
                    var intact=selectedUnits.Where(x=>x.Condition==HarvestUnitCondition.Intact).ToArray();
                    var damaged=selectedUnits.Where(x=>x.Condition==HarvestUnitCondition.DamagedPotentiallyRecoverable).ToArray();
                    var maxValue=intact.Length==0?0:intact.Max(x=>x.ValueCopper??long.MinValue);
                    var top=intact.Where(x=>x.ValueCopper==maxValue).ToArray();
                    if(intact.Length==0||intact.Length>1&&intact.Any(x=>!x.ValueCopper.HasValue)
                        ||top.Length>1&&!top.Any(x=>x.Id==attempt.FailureVictimPreference)
                        ||attempt.FailureVictimPreference!=""&&!top.Any(x=>x.Id==attempt.FailureVictimPreference)
                        ||damaged.Length>1&&!damaged.Any(x=>x.Id==attempt.CriticalRecoveryPreference)
                        ||attempt.CriticalRecoveryPreference!=""&&!damaged.Any(x=>x.Id==attempt.CriticalRecoveryPreference)
                        ||attempt.Status==HarvestAttemptStatus.Failure&&!selectedUnits.Any(x=>x.Id==attempt.FailureVictimPreference||top.Length==1&&x.Id==top[0].Id)
                        ||attempt.Status==HarvestAttemptStatus.CriticalSuccess&&damaged.Length>0
                            &&!selectedUnits.Any(x=>x.Id==attempt.CriticalRecoveryPreference||damaged.Length==1&&x.Id==damaged[0].Id&&x.Status==HarvestUnitStatus.Extracted))
                        throw new ArgumentException("Harvest conditional outcome choices do not match the selected allocation.");
                }
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==attempt.Id).OrderBy(x=>x.Start).ToArray();
                if(intervals.Any(x=>x.WorkerId!=attempt.WorkerId))throw new ArgumentException("Harvest labor has another worker.");
                RuleQuantity booked=RuleQuantity.Sum(intervals.Where(x=>x.Start<s.RuleClock).Select(x=>{
                    RuleTime end=x.End<s.RuleClock?x.End:s.RuleClock;
                    return RuleQuantity.FromFraction((BigInteger)end.Numerator*x.Start.Denominator
                        -(BigInteger)x.Start.Numerator*end.Denominator,(BigInteger)end.Denominator*x.Start.Denominator);
                }));
                if(booked!=new RuleQuantity(attempt.WorkDone.Numerator,attempt.WorkDone.Denominator))
                    throw new ArgumentException("Harvest work does not match its exact worker intervals.");
                bool active=attempt.Status==HarvestAttemptStatus.Working;
                var current=intervals.SingleOrDefault(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock);
                if(active) {
                    RuleTime remaining=RuleTime.FromFraction((BigInteger)attempt.Duration.Numerator*attempt.WorkDone.Denominator
                        -(BigInteger)attempt.WorkDone.Numerator*attempt.Duration.Denominator,
                        (BigInteger)attempt.Duration.Denominator*attempt.WorkDone.Denominator);
                    RuleTime expectedEnd=RuleTime.FromFraction((BigInteger)s.RuleClock.Numerator*remaining.Denominator
                        +(BigInteger)remaining.Numerator*s.RuleClock.Denominator,(BigInteger)s.RuleClock.Denominator*remaining.Denominator);
                    if(current==null||current.End!=expectedEnd)throw new ArgumentException("Active harvest interval mismatch.");
                } else if(current!=null)throw new ArgumentException("Inactive harvest attempt holds worker time.");
                bool resolved=attempt.Status==HarvestAttemptStatus.Success||attempt.Status==HarvestAttemptStatus.CriticalSuccess
                    ||attempt.Status==HarvestAttemptStatus.Failure||attempt.Status==HarvestAttemptStatus.CriticalFailure;
                if(attempt.ProficiencyRank==0&&attempt.ProficiencyBonus!=0||attempt.ProficiencyRank>0&&attempt.ProficiencyBonus==0
                    ||resolved&&(attempt.CompletedAt!=attempt.UpdatedAt||attempt.WorkDone!=attempt.Duration
                        ||attempt.Degree!=Grade(attempt.Natural,attempt.CheckModifier,attempt.CheckDc))
                    ||attempt.Status==HarvestAttemptStatus.Paused&&attempt.WorkDone==attempt.Duration)
                    throw new ArgumentException("Harvest attempt timeline mismatch.");
            }
        }
        public static RuleTime Duration(int fullSeconds,int categories,int selected)
        {
            if(fullSeconds<1||categories<1||selected<1||selected>categories)throw new ArgumentException("Invalid selected harvest duration.");
            BigInteger numerator=(BigInteger)fullSeconds*selected,denominator=(BigInteger)categories*60;
            BigInteger minutes=(numerator+denominator-1)/denominator;
            if(minutes<1)minutes=1;
            return new RuleTime(checked((long)(minutes*60)));
        }
    }
}
