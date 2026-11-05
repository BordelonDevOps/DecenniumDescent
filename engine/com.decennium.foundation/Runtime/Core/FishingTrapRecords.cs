using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum FishingTrapAttemptStatus { SettingUp, Paused, Soaking, Resolved, Cancelled, Abandoned, CheckMissed, RetrievedBeforeCheck, NoResponse }
    public enum FishingTrapCheckOutcome { None, NoCatch, CapturedInTrap }
    public enum FishingTrapDiceSelection { None, Normal, Disadvantage }
    public enum FishingTrapCheckDegree { None, CriticalFailure, Failure, Success, CriticalSuccess }
    public enum FishingOpportunityStatus { Available, Reserved, Spent }
    public enum FishingCreatureLifeState { Alive, Dead }
    public enum FishingTrapPhysicalStatus { Staged, Deployed, Retrieved, Abandoned, Reserved }
    public enum FishingTrapRetrievalStatus { Working, Paused, Complete, Cancelled }

    /// <summary>Persisted state for one bounded unattended fishing-trap operation. This record
    /// does not create a creature inventory lot: a successful catch remains inside the deployed trap.</summary>
    public sealed class FishingTrapAttemptRecord
    {
        public string Id { get; }
        public string SetterId { get; }
        public string ResponsibleHolderId { get; }
        public string TrapId { get; }
        public string OpportunityId { get; }
        public string CreatureId { get; }
        public string CapturedCreatureId { get; }
        public string SiteId { get; }
        public string BaitLotId { get; }
        public string BaitReservationId { get; }
        public RuleTime? BaitExposedAt { get; }
        public RuleTime StartedAt { get; }
        public RuleTime SetupLabor { get; }
        public RuleTime? SetupCompletedAt { get; }
        public RuleTime? CheckDueAt { get; }
        public RuleTime? CheckResolvedAt { get; }
        public RuleTime? AbandonedAt { get; }
        public FishingTrapAttemptStatus Status { get; }
        public bool OpportunityCommitted { get; }
        public int WisdomModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public FishingTrapDiceSelection DiceSelection { get; }
        public int FirstDie { get; }
        public int SecondDie { get; }
        public int Natural { get; }
        public int CheckModifier { get; }
        public int CheckDc { get; }
        public FishingTrapCheckDegree CheckDegree { get; }
        public FishingTrapCheckOutcome CheckOutcome { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }

        public FishingTrapAttemptRecord(string id,string setterId,string responsibleHolderId,string trapId,string opportunityId,
            string creatureId,string capturedCreatureId,string siteId,RuleTime startedAt,RuleTime setupLabor,
            RuleTime? setupCompletedAt,RuleTime? checkDueAt,RuleTime? checkResolvedAt,RuleTime? abandonedAt,
            FishingTrapAttemptStatus status,bool opportunityCommitted,int wisdomModifier,int proficiencyRank,int proficiencyBonus,
            FishingTrapDiceSelection diceSelection,int firstDie,int secondDie,int natural,int checkModifier,int checkDc,
            FishingTrapCheckDegree checkDegree,FishingTrapCheckOutcome checkOutcome,uint randomBefore,uint randomAfter,long wordsConsumed,
            string baitLotId,string baitReservationId,RuleTime? baitExposedAt)
        {
            foreach(string value in new[]{id,setterId,responsibleHolderId,trapId,opportunityId,creatureId,siteId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid fishing-trap identity.");
            bool legacyWithoutBait=baitLotId==""&&baitReservationId=="";
            if(baitLotId==null||baitReservationId==null||!legacyWithoutBait&&(!Validation.ValidId(baitLotId)||!Validation.ValidId(baitReservationId)))
                throw new ArgumentException("Invalid fishing-trap bait identity.");
            if(capturedCreatureId==null||capturedCreatureId!=""&&!Validation.ValidId(capturedCreatureId)
                ||!Enum.IsDefined(typeof(FishingTrapAttemptStatus),status)||!Enum.IsDefined(typeof(FishingTrapDiceSelection),diceSelection)
                ||!Enum.IsDefined(typeof(FishingTrapCheckDegree),checkDegree)||!Enum.IsDefined(typeof(FishingTrapCheckOutcome),checkOutcome)
                ||setupLabor<default(RuleTime)||setupLabor>new RuleTime(300)||wisdomModifier< -20||wisdomModifier>20
                ||proficiencyRank<0||proficiencyRank>2||proficiencyBonus<0||proficiencyBonus>40
                ||firstDie<0||firstDie>20||secondDie<0||secondDie>20||natural<0||natural>20
                ||checkModifier< -100||checkModifier>100||checkDc<0||checkDc>100||randomBefore==0&&randomAfter!=0
                ||randomBefore!=0&&randomAfter==0||wordsConsumed<0||status==FishingTrapAttemptStatus.SettingUp&&setupLabor>=new RuleTime(300)
                ||status==FishingTrapAttemptStatus.Paused&&setupLabor>=new RuleTime(300)
                ||setupCompletedAt.HasValue!=(setupLabor==new RuleTime(300))
                ||(legacyWithoutBait
                    ?setupCompletedAt.HasValue&&(!checkDueAt.HasValue||checkDueAt.Value!=setupCompletedAt.Value.AddSeconds(3000))
                        ||!setupCompletedAt.HasValue&&checkDueAt.HasValue
                    :!checkDueAt.HasValue||checkDueAt.Value!=startedAt.AddSeconds(3300))
                ||legacyWithoutBait&&baitExposedAt.HasValue
                ||!legacyWithoutBait&&setupCompletedAt.HasValue!=baitExposedAt.HasValue
                ||baitExposedAt.HasValue&&baitExposedAt.Value!=setupCompletedAt.Value
                ||opportunityCommitted!=setupCompletedAt.HasValue
                ||setupCompletedAt.HasValue&&setupCompletedAt.Value<startedAt
                ||status==FishingTrapAttemptStatus.Soaking&&(!setupCompletedAt.HasValue||checkResolvedAt.HasValue||abandonedAt.HasValue)
                ||status==FishingTrapAttemptStatus.SettingUp&&(setupCompletedAt.HasValue||abandonedAt.HasValue)
                ||status==FishingTrapAttemptStatus.Paused&&(setupCompletedAt.HasValue||abandonedAt.HasValue)
                ||status==FishingTrapAttemptStatus.Cancelled&&(opportunityCommitted||abandonedAt.HasValue||checkResolvedAt.HasValue)
                ||status==FishingTrapAttemptStatus.Resolved&&(!checkResolvedAt.HasValue||!checkDueAt.HasValue||checkResolvedAt.Value!=checkDueAt.Value||abandonedAt.HasValue)
                ||status==FishingTrapAttemptStatus.CheckMissed&&(!checkResolvedAt.HasValue||!checkDueAt.HasValue||checkResolvedAt.Value!=checkDueAt.Value||abandonedAt.HasValue)
                ||status==FishingTrapAttemptStatus.NoResponse&&(!setupCompletedAt.HasValue||!opportunityCommitted
                    ||checkResolvedAt.HasValue||checkOutcome!=FishingTrapCheckOutcome.None||abandonedAt.HasValue)
                ||status==FishingTrapAttemptStatus.RetrievedBeforeCheck&&(!setupCompletedAt.HasValue||!opportunityCommitted
                    ||checkResolvedAt.HasValue||abandonedAt.HasValue||checkOutcome!=FishingTrapCheckOutcome.None)
                ||status==FishingTrapAttemptStatus.Abandoned&&!abandonedAt.HasValue
                ||status!=FishingTrapAttemptStatus.Abandoned&&abandonedAt.HasValue
                ||checkResolvedAt.HasValue&&(!checkDueAt.HasValue||checkResolvedAt.Value!=checkDueAt.Value
                    ||!setupCompletedAt.HasValue&&status!=FishingTrapAttemptStatus.CheckMissed&&!(status==FishingTrapAttemptStatus.Abandoned&&checkOutcome==FishingTrapCheckOutcome.None))
                ||checkOutcome==FishingTrapCheckOutcome.None&&(checkResolvedAt.HasValue&&status!=FishingTrapAttemptStatus.CheckMissed
                    &&!(status==FishingTrapAttemptStatus.Abandoned&&checkResolvedAt.HasValue)||diceSelection!=FishingTrapDiceSelection.None
                    ||firstDie!=0||secondDie!=0||natural!=0||checkModifier!=0||checkDc!=0||checkDegree!=FishingTrapCheckDegree.None
                    ||randomBefore!=0||randomAfter!=0||wordsConsumed!=0||capturedCreatureId!="")
                ||checkOutcome!=FishingTrapCheckOutcome.None&&(!checkResolvedAt.HasValue||diceSelection==FishingTrapDiceSelection.None
                    ||firstDie<1||natural<1||checkDc<1||checkDegree==FishingTrapCheckDegree.None||randomBefore==0||randomAfter==0
                    ||wordsConsumed!=(diceSelection==FishingTrapDiceSelection.Normal?1:2)
                    ||(diceSelection==FishingTrapDiceSelection.Normal?secondDie!=0:secondDie<1)
                    ||(checkOutcome==FishingTrapCheckOutcome.CapturedInTrap)!=(checkDegree>=FishingTrapCheckDegree.Success)
                    ||(checkOutcome==FishingTrapCheckOutcome.CapturedInTrap?capturedCreatureId!=creatureId:capturedCreatureId!=""))
                ||status==FishingTrapAttemptStatus.Resolved&&checkOutcome==FishingTrapCheckOutcome.None
                ||(status==FishingTrapAttemptStatus.SettingUp||status==FishingTrapAttemptStatus.Paused)&&checkOutcome!=FishingTrapCheckOutcome.None
                ||status==FishingTrapAttemptStatus.Soaking&&checkOutcome!=FishingTrapCheckOutcome.None
                ||status==FishingTrapAttemptStatus.Cancelled&&checkOutcome!=FishingTrapCheckOutcome.None
                ||status==FishingTrapAttemptStatus.Abandoned&&abandonedAt.Value<startedAt
                ||status==FishingTrapAttemptStatus.Abandoned&&checkResolvedAt.HasValue&&abandonedAt.Value<checkResolvedAt.Value
                ||checkOutcome!=FishingTrapCheckOutcome.None&&checkModifier!=wisdomModifier+proficiencyBonus
                ||checkOutcome!=FishingTrapCheckOutcome.None&&natural!=(diceSelection==FishingTrapDiceSelection.Normal?firstDie:Math.Min(firstDie,secondDie)))
                throw new ArgumentException("Invalid fishing-trap attempt.");
            Id=id;SetterId=setterId;ResponsibleHolderId=responsibleHolderId;TrapId=trapId;OpportunityId=opportunityId;
            CreatureId=creatureId;CapturedCreatureId=capturedCreatureId;SiteId=siteId;StartedAt=startedAt;SetupLabor=setupLabor;
            BaitLotId=baitLotId;BaitReservationId=baitReservationId;BaitExposedAt=baitExposedAt;
            SetupCompletedAt=setupCompletedAt;CheckDueAt=checkDueAt;CheckResolvedAt=checkResolvedAt;AbandonedAt=abandonedAt;
            Status=status;OpportunityCommitted=opportunityCommitted;WisdomModifier=wisdomModifier;ProficiencyRank=proficiencyRank;
            ProficiencyBonus=proficiencyBonus;DiceSelection=diceSelection;FirstDie=firstDie;SecondDie=secondDie;Natural=natural;
            CheckModifier=checkModifier;CheckDc=checkDc;CheckDegree=checkDegree;CheckOutcome=checkOutcome;
            RandomBefore=randomBefore;RandomAfter=randomAfter;WordsConsumed=wordsConsumed;
        }
    }

    /// <summary>One finite site opportunity with one authored candidate in the bounded schema37 fixture.</summary>
    public sealed class FishingOpportunityRecord
    {
        public string Id { get; }
        public string SiteId { get; }
        public string StockVersionId { get; }
        public string CandidateCreatureId { get; }
        public FishingOpportunityStatus Status { get; }
        public string ReservedByAttemptId { get; }
        public RuleTime? ReservedAt { get; }
        public string CommittedByAttemptId { get; }
        public RuleTime? CommittedAt { get; }
        public string LastReleasedAttemptId { get; }
        public RuleTime? LastReleasedAt { get; }
        public FishingOpportunityRecord(string id,string siteId,string stockVersionId,string candidateCreatureId,
            FishingOpportunityStatus status,string reservedByAttemptId,RuleTime? reservedAt,string committedByAttemptId,
            RuleTime? committedAt,string lastReleasedAttemptId,RuleTime? lastReleasedAt)
        {
            foreach(string value in new[]{id,siteId,stockVersionId,candidateCreatureId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid fishing-opportunity identity.");
            if(reservedByAttemptId==null||reservedByAttemptId!=""&&!Validation.ValidId(reservedByAttemptId)
                ||committedByAttemptId==null||committedByAttemptId!=""&&!Validation.ValidId(committedByAttemptId)
                ||lastReleasedAttemptId==null||lastReleasedAttemptId!=""&&!Validation.ValidId(lastReleasedAttemptId)
                ||!Enum.IsDefined(typeof(FishingOpportunityStatus),status)
                ||(status==FishingOpportunityStatus.Available&&(reservedByAttemptId!=""||reservedAt.HasValue||committedByAttemptId!=""||committedAt.HasValue))
                ||(status==FishingOpportunityStatus.Reserved&&(!Validation.ValidId(reservedByAttemptId)||!reservedAt.HasValue
                    ||committedByAttemptId!=""||committedAt.HasValue))
                ||(status==FishingOpportunityStatus.Spent&&(reservedByAttemptId!=""||!reservedAt.HasValue
                    ||!Validation.ValidId(committedByAttemptId)||!committedAt.HasValue))
                ||lastReleasedAttemptId!=""!=lastReleasedAt.HasValue
                ||reservedAt.HasValue&&committedAt.HasValue&&committedAt.Value<reservedAt.Value
                ||reservedAt.HasValue&&lastReleasedAt.HasValue&&lastReleasedAt.Value<reservedAt.Value)
                throw new ArgumentException("Invalid fishing-opportunity reservation state.");
            Id=id;SiteId=siteId;StockVersionId=stockVersionId;CandidateCreatureId=candidateCreatureId;Status=status;
            ReservedByAttemptId=reservedByAttemptId;ReservedAt=reservedAt;CommittedByAttemptId=committedByAttemptId;
            CommittedAt=committedAt;LastReleasedAttemptId=lastReleasedAttemptId;LastReleasedAt=lastReleasedAt;
        }
        public FishingOpportunityRecord Reserve(string attemptId,RuleTime at)
        {
            if(Status!=FishingOpportunityStatus.Available)throw new ArgumentException("Fishing opportunity is unavailable.");
            return new FishingOpportunityRecord(Id,SiteId,StockVersionId,CandidateCreatureId,FishingOpportunityStatus.Reserved,
                attemptId,at,"",null,LastReleasedAttemptId,LastReleasedAt);
        }
        public FishingOpportunityRecord Release(RuleTime at)
        {
            if(Status!=FishingOpportunityStatus.Reserved)throw new ArgumentException("Fishing opportunity is not reserved.");
            return new FishingOpportunityRecord(Id,SiteId,StockVersionId,CandidateCreatureId,FishingOpportunityStatus.Available,
                "",null,"",null,ReservedByAttemptId,at);
        }
        public FishingOpportunityRecord Commit(RuleTime at)
        {
            if(Status!=FishingOpportunityStatus.Reserved)throw new ArgumentException("Fishing opportunity is not reserved.");
            return new FishingOpportunityRecord(Id,SiteId,StockVersionId,CandidateCreatureId,FishingOpportunityStatus.Spent,
                "",ReservedAt,ReservedByAttemptId,at,LastReleasedAttemptId,LastReleasedAt);
        }
    }

    /// <summary>A versioned finite set of actual physical stock members for one shared stock pool.
    /// Labels identify records; membership and applicability are authoritative.</summary>
    public sealed class FishingStockManifestRecord
    {
        private readonly string[] physicalMemberIds;
        public string Id { get; }
        public string SharedStockId { get; }
        public string VersionId { get; }
        public RuleTime EffectiveFrom { get; }
        public RuleTime? EffectiveUntil { get; }
        public string[] PhysicalMemberIds=>(string[])physicalMemberIds.Clone();

        public FishingStockManifestRecord(string id,string sharedStockId,string versionId,RuleTime effectiveFrom,
            RuleTime? effectiveUntil,string[] physicalMemberIds)
        {
            foreach(string value in new[]{id,sharedStockId,versionId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid fishing-stock manifest identity.");
            if(effectiveFrom<default(RuleTime)||effectiveUntil.HasValue&&effectiveUntil.Value<=effectiveFrom
                ||physicalMemberIds==null||physicalMemberIds.Length<1||physicalMemberIds.Length>FishingTrapValidation.MaxAttempts
                ||physicalMemberIds.Any(x=>!Validation.ValidId(x))
                ||physicalMemberIds.Distinct(StringComparer.Ordinal).Count()!=physicalMemberIds.Length)
                throw new ArgumentException("Invalid finite fishing-stock manifest.");
            Id=id;SharedStockId=sharedStockId;VersionId=versionId;EffectiveFrom=effectiveFrom;EffectiveUntil=effectiveUntil;
            this.physicalMemberIds=physicalMemberIds.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
        }

        public bool AppliesAt(RuleTime at)=>EffectiveFrom<=at&&(!EffectiveUntil.HasValue||at<EffectiveUntil.Value);
    }

    /// <summary>An opportunity's explicit allocation from the manifest's physical members. The partition
    /// label never substitutes for the member list; whole-pool allocations must enumerate every member.</summary>
    public sealed class FishingStockAllocationRecord
    {
        private readonly string[] physicalMemberIds;
        public string Id { get; }
        public string ManifestId { get; }
        public string OpportunityId { get; }
        public bool WholePool { get; }
        public string[] PhysicalMemberIds=>(string[])physicalMemberIds.Clone();

        public FishingStockAllocationRecord(string id,string manifestId,string opportunityId,bool wholePool,string[] physicalMemberIds)
        {
            foreach(string value in new[]{id,manifestId,opportunityId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid fishing-stock allocation identity.");
            if(physicalMemberIds==null||physicalMemberIds.Length<1||physicalMemberIds.Length>FishingTrapValidation.MaxAttempts
                ||physicalMemberIds.Any(x=>!Validation.ValidId(x))
                ||physicalMemberIds.Distinct(StringComparer.Ordinal).Count()!=physicalMemberIds.Length)
                throw new ArgumentException("Invalid fishing-stock allocation membership.");
            Id=id;ManifestId=manifestId;OpportunityId=opportunityId;WholePool=wholePool;
            this.physicalMemberIds=physicalMemberIds.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
        }
    }

    /// <summary>One actual physical body referenced by one or more finite opportunity profiles. ActiveResponseAttemptId
    /// reserves it once across those profiles. Containment is authoritative; a contained creature is never copied into inventory.</summary>
    public sealed class FishingCreatureBodyRecord
    {
        public string Id { get; }
        public string ProfileId { get; }
        public string OriginId { get; }
        public string SiteId { get; }
        public string LocationId { get; }
        public string ContainerId { get; }
        public string CustodianId { get; }
        public FishingCreatureLifeState LifeState { get; }
        public RuleQuantity MassPounds { get; }
        public RuleQuantity VolumeCubicFeet { get; }
        public string ActiveResponseAttemptId { get; }
        public string LastResponseAttemptId { get; }
        public string CapturedByAttemptId { get; }
        public RuleTime? RecoveryEvaluatedAt { get; }
        public int RecoveryExtraUnits { get; }
        public FishingCreatureBodyRecord(string id,string profileId,string originId,string siteId,string locationId,string containerId,
            string custodianId,FishingCreatureLifeState lifeState,RuleQuantity massPounds,RuleQuantity volumeCubicFeet,
            string activeResponseAttemptId,string lastResponseAttemptId,string capturedByAttemptId,
            RuleTime? recoveryEvaluatedAt,int recoveryExtraUnits)
        {
            foreach(string value in new[]{id,profileId,originId,siteId,locationId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid fishing-creature identity.");
            foreach(string value in new[]{containerId,custodianId,activeResponseAttemptId,lastResponseAttemptId,capturedByAttemptId})
                if(value==null||value!=""&&!Validation.ValidId(value))throw new ArgumentException("Invalid fishing-creature custody identity.");
            if(!Enum.IsDefined(typeof(FishingCreatureLifeState),lifeState)||massPounds<=default(RuleQuantity)
                ||volumeCubicFeet<=default(RuleQuantity)||recoveryExtraUnits<0||recoveryExtraUnits>3
                ||containerId!=""&&locationId!=containerId
                ||containerId!=""&&capturedByAttemptId==""
                ||(recoveryEvaluatedAt.HasValue!=(capturedByAttemptId!=""))
                ||!recoveryEvaluatedAt.HasValue&&recoveryExtraUnits!=0)
                throw new ArgumentException("Invalid fishing-creature physical state.");
            Id=id;ProfileId=profileId;OriginId=originId;SiteId=siteId;LocationId=locationId;ContainerId=containerId;
            CustodianId=custodianId;LifeState=lifeState;MassPounds=massPounds;VolumeCubicFeet=volumeCubicFeet;
            ActiveResponseAttemptId=activeResponseAttemptId;LastResponseAttemptId=lastResponseAttemptId;
            CapturedByAttemptId=capturedByAttemptId;RecoveryEvaluatedAt=recoveryEvaluatedAt;RecoveryExtraUnits=recoveryExtraUnits;
        }
        public FishingCreatureBodyRecord Reserve(string attemptId)
        {
            if(ActiveResponseAttemptId!=""||ContainerId!=""||LifeState!=FishingCreatureLifeState.Alive)
                throw new ArgumentException("Fishing creature is already allocated or unavailable.");
            return new FishingCreatureBodyRecord(Id,ProfileId,OriginId,SiteId,LocationId,ContainerId,CustodianId,LifeState,
                MassPounds,VolumeCubicFeet,attemptId,LastResponseAttemptId,"",null,0);
        }
        public FishingCreatureBodyRecord Release(string attemptId)
        {
            if(ActiveResponseAttemptId!=attemptId)throw new ArgumentException("Fishing creature allocation mismatch.");
            return new FishingCreatureBodyRecord(Id,ProfileId,OriginId,SiteId,LocationId,ContainerId,CustodianId,LifeState,
                MassPounds,VolumeCubicFeet,"",attemptId,"",null,0);
        }
        public FishingCreatureBodyRecord Capture(string attemptId,string trapId,RuleTime at)
        {
            if(ActiveResponseAttemptId!=attemptId||ContainerId!=""||LifeState!=FishingCreatureLifeState.Alive||RecoveryEvaluatedAt.HasValue)
                throw new ArgumentException("Fishing creature cannot be secured by this attempt.");
            return new FishingCreatureBodyRecord(Id,ProfileId,OriginId,SiteId,trapId,trapId,trapId,LifeState,
                MassPounds,VolumeCubicFeet,"",attemptId,attemptId,at,0);
        }
        public FishingCreatureBodyRecord RetrieveFromTrap(string attemptId,string locationId,string custodianId)
        {
            if(CapturedByAttemptId!=attemptId||ContainerId==""||LocationId!=ContainerId||!RecoveryEvaluatedAt.HasValue)
                throw new ArgumentException("Fishing creature is not secured by this retrieval.");
            return new FishingCreatureBodyRecord(Id,ProfileId,OriginId,SiteId,locationId,"",custodianId,LifeState,
                MassPounds,VolumeCubicFeet,"",LastResponseAttemptId,CapturedByAttemptId,RecoveryEvaluatedAt,RecoveryExtraUnits);
        }
        public FishingCreatureBodyRecord WithMassPounds(RuleQuantity massPounds)
        {
            if(LifeState!=FishingCreatureLifeState.Dead||massPounds<=default(RuleQuantity)||massPounds>MassPounds
                ||ActiveResponseAttemptId!=""||CapturedByAttemptId!="")throw new ArgumentException("Only remaining dead remains can lose material mass.");
            return new FishingCreatureBodyRecord(Id,ProfileId,OriginId,SiteId,LocationId,ContainerId,CustodianId,LifeState,
                massPounds,VolumeCubicFeet,ActiveResponseAttemptId,LastResponseAttemptId,CapturedByAttemptId,RecoveryEvaluatedAt,RecoveryExtraUnits);
        }
    }

    public sealed class FishingTrapPhysicalRecord
    {
        public string TrapId { get; }
        public string SiteId { get; }
        public string SupportId { get; }
        public FishingTrapPhysicalStatus Status { get; }
        public string AttemptId { get; }
        public string LatestRetrievalId { get; }
        public string ReceivingLocationId { get; }
        public RuleTime? RetrievedAt { get; }
        public int StructuralAc { get; }
        public long CatchCapacityPounds { get; }
        public RuleQuantity CatchCapacityCubicFeet { get; }
        public RuleQuantity BodyVolumeCubicFeet { get; }
        public int RecoveryCordFeet { get; }
        public int X { get; }
        public int Y { get; }
        public FishingTrapPhysicalRecord(string trapId,string siteId,string supportId,FishingTrapPhysicalStatus status,
            string attemptId,string latestRetrievalId,string receivingLocationId,RuleTime? retrievedAt,int structuralAc,
            long catchCapacityPounds,RuleQuantity catchCapacityCubicFeet,RuleQuantity bodyVolumeCubicFeet,int recoveryCordFeet,int x=0,int y=0)
        {
            foreach(string value in new[]{trapId,siteId,supportId})if(!Validation.ValidId(value))throw new ArgumentException("Invalid fishing Trap body identity.");
            foreach(string value in new[]{attemptId,latestRetrievalId,receivingLocationId})
                if(value==null||value!=""&&!Validation.ValidId(value))throw new ArgumentException("Invalid fishing Trap disposition identity.");
            if(!Enum.IsDefined(typeof(FishingTrapPhysicalStatus),status)||structuralAc<1||structuralAc>30
                ||catchCapacityPounds<1||catchCapacityCubicFeet<=default(RuleQuantity)||bodyVolumeCubicFeet<=default(RuleQuantity)
                ||recoveryCordFeet<1||recoveryCordFeet>100
                ||x<0||y<0
                ||(status==FishingTrapPhysicalStatus.Staged&&(attemptId!=""||retrievedAt.HasValue||receivingLocationId!=""))
                ||(status==FishingTrapPhysicalStatus.Reserved&&(!Validation.ValidId(attemptId)||retrievedAt.HasValue||receivingLocationId!=""))
                ||(status==FishingTrapPhysicalStatus.Deployed&&(!Validation.ValidId(attemptId)||retrievedAt.HasValue||receivingLocationId!=""))
                ||(status==FishingTrapPhysicalStatus.Abandoned&&(!Validation.ValidId(attemptId)||retrievedAt.HasValue||receivingLocationId!=""))
                ||(status==FishingTrapPhysicalStatus.Retrieved&&(!Validation.ValidId(attemptId)||!retrievedAt.HasValue||!Validation.ValidId(receivingLocationId))))
                throw new ArgumentException("Invalid fishing Trap physical state.");
            TrapId=trapId;SiteId=siteId;SupportId=supportId;Status=status;AttemptId=attemptId;LatestRetrievalId=latestRetrievalId;
            ReceivingLocationId=receivingLocationId;RetrievedAt=retrievedAt;StructuralAc=structuralAc;
            CatchCapacityPounds=catchCapacityPounds;CatchCapacityCubicFeet=catchCapacityCubicFeet;BodyVolumeCubicFeet=bodyVolumeCubicFeet;
            RecoveryCordFeet=recoveryCordFeet;X=x;Y=y;
        }
        public FishingTrapPhysicalRecord WithStatus(FishingTrapPhysicalStatus status,string attemptId)
            =>new FishingTrapPhysicalRecord(TrapId,SiteId,SupportId,status,attemptId,LatestRetrievalId,"",null,
                StructuralAc,CatchCapacityPounds,CatchCapacityCubicFeet,BodyVolumeCubicFeet,RecoveryCordFeet,X,Y);
        public FishingTrapPhysicalRecord WithRetrieved(string retrievalId,string destination,RuleTime at,int x,int y)
            =>new FishingTrapPhysicalRecord(TrapId,SiteId,SupportId,FishingTrapPhysicalStatus.Retrieved,AttemptId,
                retrievalId,destination,at,StructuralAc,CatchCapacityPounds,CatchCapacityCubicFeet,BodyVolumeCubicFeet,RecoveryCordFeet,x,y);
    }

    public sealed class FishingReceiveLocationRecord
    {
        public string Id { get; }
        public string SiteId { get; }
        public string SupportId { get; }
        public int X { get; }
        public int Y { get; }
        public RuleQuantity CapacityPounds { get; }
        public RuleQuantity CapacityCubicFeet { get; }
        public int RecoveryPathFeet { get; }
        public string ReservedByRetrievalId { get; }
        public FishingReceiveLocationRecord(string id,string siteId,string supportId,int x,int y,RuleQuantity capacityPounds,
            RuleQuantity capacityCubicFeet,string reservedByRetrievalId,int recoveryPathFeet=0)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(siteId)||!Validation.ValidId(supportId)||x<0||y<0
                ||capacityPounds<=default(RuleQuantity)||capacityCubicFeet<=default(RuleQuantity)
                ||reservedByRetrievalId==null||reservedByRetrievalId!=""&&!Validation.ValidId(reservedByRetrievalId)
                ||recoveryPathFeet<0||recoveryPathFeet>1000)
                throw new ArgumentException("Invalid fishing receiving location.");
            Id=id;SiteId=siteId;SupportId=supportId;X=x;Y=y;CapacityPounds=capacityPounds;CapacityCubicFeet=capacityCubicFeet;
            ReservedByRetrievalId=reservedByRetrievalId;RecoveryPathFeet=recoveryPathFeet;
        }
        public FishingReceiveLocationRecord Reserve(string retrievalId)
        {if(ReservedByRetrievalId!="")throw new ArgumentException("Receiving location is already reserved.");
            return new FishingReceiveLocationRecord(Id,SiteId,SupportId,X,Y,CapacityPounds,CapacityCubicFeet,retrievalId,RecoveryPathFeet);}
        public FishingReceiveLocationRecord Release(string retrievalId)
        {if(ReservedByRetrievalId!=retrievalId)throw new ArgumentException("Receiving location reservation mismatch.");
            return new FishingReceiveLocationRecord(Id,SiteId,SupportId,X,Y,CapacityPounds,CapacityCubicFeet,"",RecoveryPathFeet);}
    }

    public sealed class FishingTrapRetrievalRecord
    {
        public string Id { get; }
        public string AttemptId { get; }
        public string TrapId { get; }
        public string WorkerId { get; }
        public string DestinationId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime WorkDone { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime? CompletedAt { get; }
        public FishingTrapRetrievalStatus Status { get; }
        public FishingTrapRetrievalRecord(string id,string attemptId,string trapId,string workerId,string destinationId,
            RuleTime startedAt,RuleTime workDone,RuleTime updatedAt,RuleTime? completedAt,FishingTrapRetrievalStatus status)
        {
            foreach(string value in new[]{id,attemptId,trapId,workerId,destinationId})if(!Validation.ValidId(value))throw new ArgumentException("Invalid Trap retrieval identity.");
            if(!Enum.IsDefined(typeof(FishingTrapRetrievalStatus),status)||startedAt>updatedAt||workDone<default(RuleTime)
                ||workDone>new RuleTime(300)||completedAt.HasValue!=(status==FishingTrapRetrievalStatus.Complete)
                ||completedAt.HasValue&&(completedAt.Value!=updatedAt||workDone!=new RuleTime(300)))
                throw new ArgumentException("Invalid Trap retrieval work state.");
            Id=id;AttemptId=attemptId;TrapId=trapId;WorkerId=workerId;DestinationId=destinationId;StartedAt=startedAt;
            WorkDone=workDone;UpdatedAt=updatedAt;CompletedAt=completedAt;Status=status;
        }
        public FishingTrapRetrievalRecord WithWork(RuleTime workDone,RuleTime updatedAt)
            =>new FishingTrapRetrievalRecord(Id,AttemptId,TrapId,WorkerId,DestinationId,StartedAt,workDone,updatedAt,null,FishingTrapRetrievalStatus.Working);
        public FishingTrapRetrievalRecord WithPaused(RuleTime updatedAt)
            =>new FishingTrapRetrievalRecord(Id,AttemptId,TrapId,WorkerId,DestinationId,StartedAt,WorkDone,updatedAt,null,FishingTrapRetrievalStatus.Paused);
        public FishingTrapRetrievalRecord WithWorker(string workerId,RuleTime updatedAt)
            =>new FishingTrapRetrievalRecord(Id,AttemptId,TrapId,workerId,DestinationId,StartedAt,WorkDone,updatedAt,null,FishingTrapRetrievalStatus.Paused);
        public FishingTrapRetrievalRecord WithCompleted(RuleTime at)
            =>new FishingTrapRetrievalRecord(Id,AttemptId,TrapId,WorkerId,DestinationId,StartedAt,new RuleTime(300),at,at,FishingTrapRetrievalStatus.Complete);
        public FishingTrapRetrievalRecord WithCancelled(RuleTime at)
            =>new FishingTrapRetrievalRecord(Id,AttemptId,TrapId,WorkerId,DestinationId,StartedAt,WorkDone,at,null,FishingTrapRetrievalStatus.Cancelled);
    }

    public static class FishingTrapValidation
    {
        public const int MaxAttempts=32;
        public static void Validate(Snapshot s)
        {
            if(s.FishingTrapAttempts==null||s.FishingTrapAttempts.Length>MaxAttempts||s.FishingTrapAttempts.Any(x=>x==null)
                ||s.FishingOpportunities==null||s.FishingCreatures==null||s.FishingTraps==null||s.FishingReceiveLocations==null||s.FishingTrapRetrievals==null
                ||new[]{s.FishingOpportunities.Length,s.FishingCreatures.Length,s.FishingTraps.Length,s.FishingReceiveLocations.Length,s.FishingTrapRetrievals.Length}.Any(x=>x>MaxAttempts)
                ||s.FishingOpportunities.Any(x=>x==null)||s.FishingCreatures.Any(x=>x==null)||s.FishingTraps.Any(x=>x==null)
                ||s.FishingReceiveLocations.Any(x=>x==null)||s.FishingTrapRetrievals.Any(x=>x==null))
                throw new ArgumentException("Invalid fishing-trap collection.");
            if(s.SchemaVersion<Snapshot.FishingTrapSchema&&(s.FishingOpportunities.Length!=0||s.FishingCreatures.Length!=0
                ||s.FishingTraps.Length!=0||s.FishingReceiveLocations.Length!=0||s.FishingTrapRetrievals.Length!=0))
                throw new ArgumentException("Physical Trap state requires schema37.");
            if(s.SchemaVersion<Snapshot.FishingTrapLegacySchema) {
                if(s.FishingTrapAttempts.Length!=0)throw new ArgumentException("Fishing-trap state requires schema35.");
                return;
            }
            if(s.FishingTrapAttempts.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.FishingTrapAttempts.Length
                ||s.FishingTrapAttempts.GroupBy(x=>x.TrapId,StringComparer.Ordinal).Any(g=>g.Count(x=>x.Status!=FishingTrapAttemptStatus.Cancelled
                    &&x.Status!=FishingTrapAttemptStatus.Abandoned&&!(x.Status==FishingTrapAttemptStatus.CheckMissed&&!x.OpportunityCommitted))>1)
                ||s.FishingTrapAttempts.GroupBy(x=>x.OpportunityId,StringComparer.Ordinal).Any(g=>g.Count(x=>x.OpportunityCommitted)>1))
                throw new ArgumentException("Duplicate or unresolved fishing-trap state.");
            foreach(var attempt in s.FishingTrapAttempts) {
                if(!s.Actors.Any(x=>x.Id==attempt.SetterId)||!s.Actors.Any(x=>x.Id==attempt.ResponsibleHolderId))
                    throw new ArgumentException("Fishing-trap actor is missing.");
                if(s.SchemaVersion>=Snapshot.FishingTrapBaitSchema) {
                    var baitLot=s.Work.Lots.SingleOrDefault(x=>x.Id==attempt.BaitLotId);
                    var baitInventory=s.InventoryLots.SingleOrDefault(x=>x.LotId==attempt.BaitLotId);
                    var bait=s.Work.Reservations.SingleOrDefault(x=>x.Id==attempt.BaitReservationId);
                    if(baitLot==null||baitInventory==null||baitLot.UnitId!="ordinary-angling-bait-0.10lb"
                        ||baitLot.LocationId!=attempt.TrapId+".bait-holder"||baitLot.CustodianId!=attempt.SetterId
                        ||baitInventory.OwnerId!=attempt.SetterId||baitInventory.Nutrition!=NutritionKind.None
                        ||baitInventory.Access!=InventoryAccess.Ready||bait==null||bait.JobId!=attempt.Id
                        ||bait.LotId!=attempt.BaitLotId||bait.Amount!=new RuleQuantity(1)
                        ||(attempt.BaitExposedAt.HasValue?bait.Status!=ReservationStatus.Consumed
                            :(attempt.Status==FishingTrapAttemptStatus.Cancelled
                                ||attempt.Status==FishingTrapAttemptStatus.Abandoned||attempt.Status==FishingTrapAttemptStatus.CheckMissed)
                                ?bait.Status!=ReservationStatus.Released
                                :bait.Status!=ReservationStatus.Reserved))
                        throw new ArgumentException("Fishing-trap bait is missing, unreserved, or settled at the wrong phase.");
                } else if(attempt.BaitLotId!=""||attempt.BaitReservationId!=""||attempt.BaitExposedAt.HasValue)
                    throw new ArgumentException("Schema35 fishing-trap state cannot contain schema36 bait data.");
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==attempt.Id).OrderBy(x=>x.Start).ToArray();
                if(intervals.Any(x=>x.WorkerId!=attempt.SetterId))throw new ArgumentException("Fishing-trap setup has another worker.");
                RuleQuantity booked=RuleQuantity.Sum(intervals.Where(x=>x.Start<s.RuleClock).Select(x=>{
                    RuleTime end=x.End<s.RuleClock?x.End:s.RuleClock;
                    return RuleQuantity.FromFraction((System.Numerics.BigInteger)end.Numerator*x.Start.Denominator
                        -(System.Numerics.BigInteger)x.Start.Numerator*end.Denominator,
                        (System.Numerics.BigInteger)end.Denominator*x.Start.Denominator);
                }));
                if(booked!=new RuleQuantity(attempt.SetupLabor.Numerator,attempt.SetupLabor.Denominator))
                    throw new ArgumentException("Fishing-trap setup labor does not match its worker intervals.");
                bool active=attempt.Status==FishingTrapAttemptStatus.SettingUp;
                var current=intervals.SingleOrDefault(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock);
                if(active) {
                    RuleTime expectedEnd=RuleTime.FromFraction((System.Numerics.BigInteger)s.RuleClock.Numerator*attempt.SetupLabor.Denominator
                        +(System.Numerics.BigInteger)(300*attempt.SetupLabor.Denominator-attempt.SetupLabor.Numerator)*s.RuleClock.Denominator,
                        (System.Numerics.BigInteger)s.RuleClock.Denominator*attempt.SetupLabor.Denominator);
                    if(current==null||current.End!=expectedEnd)throw new ArgumentException("Active fishing-trap interval mismatch.");
                } else if(current!=null)throw new ArgumentException("Inactive fishing-trap attempt holds worker time.");
                if(attempt.Status==FishingTrapAttemptStatus.Soaking||attempt.Status==FishingTrapAttemptStatus.Resolved
                    ||attempt.Status==FishingTrapAttemptStatus.Abandoned&&attempt.SetupCompletedAt.HasValue) {
                    if(attempt.SetupCompletedAt==null||attempt.SetupLabor!=new RuleTime(300))throw new ArgumentException("Fishing-trap setup is incomplete.");
                }
                if(attempt.Status==FishingTrapAttemptStatus.Soaking&&attempt.CheckDueAt.Value<=s.RuleClock
                    ||attempt.Status==FishingTrapAttemptStatus.Resolved&&attempt.CheckResolvedAt.Value>s.RuleClock
                    ||attempt.Status==FishingTrapAttemptStatus.CheckMissed&&attempt.CheckResolvedAt.Value>s.RuleClock
                    ||attempt.Status==FishingTrapAttemptStatus.SettingUp&&attempt.SetupCompletedAt.HasValue
                    ||attempt.Status==FishingTrapAttemptStatus.Paused&&attempt.SetupCompletedAt.HasValue)
                    throw new ArgumentException("Fishing-trap timeline mismatch.");
            }
            if(s.SchemaVersion<Snapshot.FishingTrapSchema)return;
            if(s.FishingOpportunities.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.FishingOpportunities.Length
                ||s.FishingCreatures.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.FishingCreatures.Length
                ||s.FishingTraps.Select(x=>x.TrapId).Distinct(StringComparer.Ordinal).Count()!=s.FishingTraps.Length
                ||s.FishingReceiveLocations.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.FishingReceiveLocations.Length
                ||s.FishingTrapRetrievals.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.FishingTrapRetrievals.Length
                ||s.FishingTrapRetrievals.Where(x=>x.Status!=FishingTrapRetrievalStatus.Cancelled).Select(x=>x.AttemptId)
                    .Distinct(StringComparer.Ordinal).Count()!=s.FishingTrapRetrievals.Count(x=>x.Status!=FishingTrapRetrievalStatus.Cancelled))
                throw new ArgumentException("Duplicate physical fishing identity.");
            if(s.SchemaVersion<Snapshot.FishingStockSchema) {
                if(s.FishingStockManifests.Length!=0||s.FishingStockAllocations.Length!=0)
                    throw new ArgumentException("Legacy fishing schema cannot carry stock manifests or allocations.");
            } else {
                if(s.FishingStockManifests.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.FishingStockManifests.Length
                    ||s.FishingStockManifests.Select(x=>x.SharedStockId+"|"+x.VersionId).Distinct(StringComparer.Ordinal).Count()!=s.FishingStockManifests.Length
                    ||s.FishingStockAllocations.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.FishingStockAllocations.Length
                    ||s.FishingStockAllocations.Select(x=>x.OpportunityId).Distinct(StringComparer.Ordinal).Count()!=s.FishingStockAllocations.Length
                    ||s.FishingStockAllocations.Length!=s.FishingOpportunities.Length)
                    throw new ArgumentException("Fishing stock manifest or allocation identities are duplicated or incomplete.");
                foreach(var manifest in s.FishingStockManifests) {
                    if(manifest.PhysicalMemberIds.Any(id=>!s.FishingCreatures.Any(creature=>creature.Id==id)))
                        throw new ArgumentException("Fishing stock manifest references a missing physical creature.");
                }
                for(int i=0;i<s.FishingStockManifests.Length;i++)for(int j=i+1;j<s.FishingStockManifests.Length;j++) {
                    var first=s.FishingStockManifests[i];var second=s.FishingStockManifests[j];
                    bool overlaps=first.SharedStockId==second.SharedStockId
                        &&(!first.EffectiveUntil.HasValue||second.EffectiveFrom<first.EffectiveUntil.Value)
                        &&(!second.EffectiveUntil.HasValue||first.EffectiveFrom<second.EffectiveUntil.Value);
                    if(overlaps&&!first.PhysicalMemberIds.SequenceEqual(second.PhysicalMemberIds,StringComparer.Ordinal))
                        throw new ArgumentException("Overlapping versions of one shared stock pool disagree about physical membership.");
                }
                foreach(var allocation in s.FishingStockAllocations) {
                    var manifest=s.FishingStockManifests.SingleOrDefault(x=>x.Id==allocation.ManifestId);
                    var opportunity=s.FishingOpportunities.SingleOrDefault(x=>x.Id==allocation.OpportunityId);
                    if(manifest==null||opportunity==null||opportunity.StockVersionId!=manifest.VersionId
                        ||allocation.PhysicalMemberIds.Any(id=>!manifest.PhysicalMemberIds.Contains(id,StringComparer.Ordinal))
                        ||allocation.WholePool!=allocation.PhysicalMemberIds.SequenceEqual(manifest.PhysicalMemberIds,StringComparer.Ordinal)
                        ||!allocation.PhysicalMemberIds.Contains(opportunity.CandidateCreatureId,StringComparer.Ordinal))
                        throw new ArgumentException("Fishing allocation does not match its actual versioned stock membership.");
                }
            }
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            ObjectStructureRecord Structure(string id)=>s.Structures.SingleOrDefault(x=>x.Id==id);
            foreach(var opportunity in s.FishingOpportunities) {
                var creature=s.FishingCreatures.SingleOrDefault(x=>x.Id==opportunity.CandidateCreatureId);
                if(creature==null||creature.SiteId!=opportunity.SiteId)throw new ArgumentException("Fishing opportunity has no physical stock member.");
                if(opportunity.Status==FishingOpportunityStatus.Available&&opportunity.ReservedByAttemptId!="")
                    throw new ArgumentException("Available fishing opportunity remains reserved.");
                if(opportunity.Status==FishingOpportunityStatus.Reserved) {
                    var attempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==opportunity.ReservedByAttemptId);
                    if(attempt==null||attempt.OpportunityId!=opportunity.Id||attempt.OpportunityCommitted
                        ||attempt.Status!=FishingTrapAttemptStatus.SettingUp&&attempt.Status!=FishingTrapAttemptStatus.Paused)
                        throw new ArgumentException("Fishing opportunity reservation has no live setup.");
                }
                if(opportunity.Status==FishingOpportunityStatus.Spent) {
                    var attempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==opportunity.CommittedByAttemptId);
                    if(attempt==null||attempt.OpportunityId!=opportunity.Id||!attempt.OpportunityCommitted)
                        throw new ArgumentException("Spent fishing opportunity has no committed attempt.");
                }
            }
            foreach(var creature in s.FishingCreatures) {
                if(creature.ActiveResponseAttemptId!="") {
                    var attempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==creature.ActiveResponseAttemptId);
                    if(attempt==null||attempt.CreatureId!=creature.Id||!attempt.OpportunityCommitted
                        ||attempt.Status!=FishingTrapAttemptStatus.Soaking)
                        throw new ArgumentException("Fishing creature response allocation has no live attempt.");
                }
                if(creature.CapturedByAttemptId!="") {
                    var attempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==creature.CapturedByAttemptId);
                    if(attempt==null||attempt.CreatureId!=creature.Id||attempt.CheckOutcome!=FishingTrapCheckOutcome.CapturedInTrap
                        ||creature.RecoveryEvaluatedAt!=attempt.CheckResolvedAt||creature.RecoveryExtraUnits!=0)
                        throw new ArgumentException("Fishing capture identity or recovery evaluation mismatch.");
                    if(creature.ContainerId!=""&&creature.ContainerId!=attempt.TrapId)
                        throw new ArgumentException("Captured creature is held by an unrelated container.");
                }
            }
            foreach(var trap in s.FishingTraps) {
                var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==trap.TrapId);
                var body=Structure(trap.TrapId);var support=Structure(trap.SupportId);
                if(item==null||body==null||support==null||body.MassPounds!=item.OperationalWeightLb
                    ||item.Placement!=PortablePlacement.Ground||item.GroundX!=trap.X||item.GroundY!=trap.Y)
                    throw new ArgumentException("Fishing Trap is missing its actual physical body, support, or location.");
                if(trap.Status==FishingTrapPhysicalStatus.Staged&&trap.AttemptId!=""
                    ||trap.Status!=FishingTrapPhysicalStatus.Staged&&trap.Status!=FishingTrapPhysicalStatus.Retrieved&&trap.AttemptId=="")
                    throw new ArgumentException("Fishing Trap attempt link does not match its physical state.");
                if(trap.Status==FishingTrapPhysicalStatus.Reserved) {
                    var attempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==trap.AttemptId);
                    if(attempt==null||attempt.TrapId!=trap.TrapId||attempt.OpportunityCommitted
                        ||attempt.Status!=FishingTrapAttemptStatus.SettingUp&&attempt.Status!=FishingTrapAttemptStatus.Paused)
                        throw new ArgumentException("Reserved Trap body has no matching setup.");
                } else if(trap.Status==FishingTrapPhysicalStatus.Deployed||trap.Status==FishingTrapPhysicalStatus.Abandoned) {
                    var attempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==trap.AttemptId);
                    if(attempt==null||attempt.TrapId!=trap.TrapId||!attempt.OpportunityCommitted)
                        throw new ArgumentException("Deployed Trap body has no committed attempt.");
                } else if(trap.Status==FishingTrapPhysicalStatus.Retrieved) {
                    var retrieval=s.FishingTrapRetrievals.SingleOrDefault(x=>x.Id==trap.LatestRetrievalId);
                    if(retrieval==null||retrieval.TrapId!=trap.TrapId||retrieval.DestinationId!=trap.ReceivingLocationId
                        ||retrieval.Status!=FishingTrapRetrievalStatus.Complete||retrieval.CompletedAt!=trap.RetrievedAt)
                        throw new ArgumentException("Retrieved Trap body has no completed retrieval.");
                }
                if(trap.Status!=FishingTrapPhysicalStatus.Retrieved&&body.Broken)
                    throw new ArgumentException("Broken Trap body remains deployed or reserved.");
            }
            foreach(var receiver in s.FishingReceiveLocations) {
                if(Structure(receiver.SupportId)==null||!s.FishingOpportunities.Any(x=>x.SiteId==receiver.SiteId)
                    ||receiver.ReservedByRetrievalId!=""&&!s.FishingTrapRetrievals.Any(x=>x.Id==receiver.ReservedByRetrievalId
                        &&x.DestinationId==receiver.Id&&(x.Status==FishingTrapRetrievalStatus.Working||x.Status==FishingTrapRetrievalStatus.Paused)))
                    throw new ArgumentException("Fishing receiving location has no physical support or valid reservation.");
            }
            foreach(var retrieval in s.FishingTrapRetrievals) {
                var attempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==retrieval.AttemptId);
                var trap=s.FishingTraps.SingleOrDefault(x=>x.TrapId==retrieval.TrapId);
                var receiver=s.FishingReceiveLocations.SingleOrDefault(x=>x.Id==retrieval.DestinationId);
                if(attempt==null||trap==null||receiver==null||attempt.TrapId!=retrieval.TrapId||receiver.SiteId!=trap.SiteId
                    ||!Actor(retrieval.WorkerId)||retrieval.StartedAt>s.RuleClock||retrieval.UpdatedAt>s.RuleClock
                    ||receiver.RecoveryPathFeet>trap.RecoveryCordFeet)
                    throw new ArgumentException("Fishing retrieval has an invalid actor, body, destination or route.");
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==retrieval.Id).OrderBy(x=>x.Start).ToArray();
                if(intervals.Any(x=>x.WorkerId!=retrieval.WorkerId))throw new ArgumentException("Fishing retrieval has another worker's labor.");
                RuleQuantity booked=RuleQuantity.Sum(intervals.Where(x=>x.Start<s.RuleClock).Select(x=>{
                    RuleTime end=x.End<s.RuleClock?x.End:s.RuleClock;
                    return RuleQuantity.FromFraction((System.Numerics.BigInteger)end.Numerator*x.Start.Denominator
                        -(System.Numerics.BigInteger)x.Start.Numerator*end.Denominator,
                        (System.Numerics.BigInteger)end.Denominator*x.Start.Denominator);
                }));
                if(booked!=new RuleQuantity(retrieval.WorkDone.Numerator,retrieval.WorkDone.Denominator))
                    throw new ArgumentException("Fishing retrieval labor does not match its worker intervals.");
                var current=intervals.SingleOrDefault(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock);
                if(retrieval.Status==FishingTrapRetrievalStatus.Working) {
                    RuleTime expectedEnd=RuleTime.FromFraction((System.Numerics.BigInteger)s.RuleClock.Numerator*retrieval.WorkDone.Denominator
                        +(System.Numerics.BigInteger)(300*retrieval.WorkDone.Denominator-retrieval.WorkDone.Numerator)*s.RuleClock.Denominator,
                        (System.Numerics.BigInteger)s.RuleClock.Denominator*retrieval.WorkDone.Denominator);
                    if(retrieval.WorkDone>=new RuleTime(300)||current==null||current.End!=expectedEnd
                        ||receiver.ReservedByRetrievalId!=retrieval.Id)
                        throw new ArgumentException("Active fishing retrieval interval is inconsistent.");
                } else if(current!=null)throw new ArgumentException("Inactive fishing retrieval holds worker time.");
                if(retrieval.Status==FishingTrapRetrievalStatus.Paused&&receiver.ReservedByRetrievalId!=retrieval.Id
                    ||retrieval.Status==FishingTrapRetrievalStatus.Complete&&(retrieval.CompletedAt.Value>s.RuleClock
                        ||receiver.ReservedByRetrievalId==retrieval.Id||trap.Status!=FishingTrapPhysicalStatus.Retrieved)
                    ||retrieval.Status==FishingTrapRetrievalStatus.Cancelled&&receiver.ReservedByRetrievalId==retrieval.Id)
                    throw new ArgumentException("Fishing retrieval completion or reservation is inconsistent.");
                if(retrieval.Status!=FishingTrapRetrievalStatus.Complete&&retrieval.Status!=FishingTrapRetrievalStatus.Cancelled
                    &&trap.Status!=FishingTrapPhysicalStatus.Deployed
                    &&trap.Status!=FishingTrapPhysicalStatus.Abandoned)
                    throw new ArgumentException("Open fishing retrieval has no deployed Trap.");
            }
            foreach(var attempt in s.FishingTrapAttempts) {
                var opportunity=s.FishingOpportunities.SingleOrDefault(x=>x.Id==attempt.OpportunityId);
                var trap=s.FishingTraps.SingleOrDefault(x=>x.TrapId==attempt.TrapId);
                var creature=s.FishingCreatures.SingleOrDefault(x=>x.Id==attempt.CreatureId);
                if(opportunity==null||trap==null||creature==null||opportunity.SiteId!=attempt.SiteId||trap.SiteId!=attempt.SiteId
                    ||opportunity.CandidateCreatureId!=attempt.CreatureId||creature.MassPounds>new RuleQuantity(trap.CatchCapacityPounds)
                    ||creature.VolumeCubicFeet>trap.CatchCapacityCubicFeet)
                    throw new ArgumentException("Fishing attempt exceeds its actual opportunity, assembly or prey profile.");
                if(attempt.OpportunityCommitted!=(opportunity.Status==FishingOpportunityStatus.Spent)
                    &&!(attempt.Status==FishingTrapAttemptStatus.Cancelled||attempt.Status==FishingTrapAttemptStatus.CheckMissed
                        ||attempt.Status==FishingTrapAttemptStatus.Abandoned&&!attempt.OpportunityCommitted))
                    throw new ArgumentException("Fishing attempt and opportunity commitment disagree.");
                if(attempt.OpportunityCommitted&&opportunity.CommittedByAttemptId!=attempt.Id)
                    throw new ArgumentException("Fishing attempt committed another opportunity owner.");
                if(s.SchemaVersion>=Snapshot.FishingStockSchema&&attempt.OpportunityCommitted) {
                    var allocation=s.FishingStockAllocations.Single(x=>x.OpportunityId==opportunity.Id);
                    var manifest=s.FishingStockManifests.Single(x=>x.Id==allocation.ManifestId);
                    if(!manifest.AppliesAt(attempt.SetupCompletedAt.Value))
                        throw new ArgumentException("Fishing stock version was not applicable at response allocation.");
                }
                if(attempt.Status==FishingTrapAttemptStatus.SettingUp||attempt.Status==FishingTrapAttemptStatus.Paused) {
                    if(trap.Status!=FishingTrapPhysicalStatus.Reserved||trap.AttemptId!=attempt.Id
                        ||opportunity.Status!=FishingOpportunityStatus.Reserved||opportunity.ReservedByAttemptId!=attempt.Id)
                        throw new ArgumentException("Setup attempt does not reserve its actual opportunity and Trap.");
                }
                if(attempt.OpportunityCommitted&&trap.Status==FishingTrapPhysicalStatus.Reserved)
                    throw new ArgumentException("Committed attempt still has a staged Trap.");
                if(attempt.CheckOutcome==FishingTrapCheckOutcome.CapturedInTrap&&creature.CapturedByAttemptId!=attempt.Id
                    &&!s.FishingTrapRetrievals.Any(x=>x.AttemptId==attempt.Id&&x.Status==FishingTrapRetrievalStatus.Complete))
                    throw new ArgumentException("Successful catch is not the same persistent creature body.");
                if(attempt.Status==FishingTrapAttemptStatus.RetrievedBeforeCheck
                    &&(!s.FishingTrapRetrievals.Any(x=>x.AttemptId==attempt.Id&&x.Status==FishingTrapRetrievalStatus.Complete)
                        ||attempt.CheckResolvedAt.HasValue||attempt.CheckOutcome!=FishingTrapCheckOutcome.None))
                    throw new ArgumentException("Early Trap retrieval did not close without a catch.");
            }
        }
    }
}
