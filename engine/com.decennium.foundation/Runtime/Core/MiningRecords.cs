using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum MiningAbilityChoice { Strength, Wisdom }
    public enum MiningUnitCondition { Intact, DamagedPotentiallyRecoverable }
    public enum MiningUnitStatus { Available, Extracted, Ruined, Spent, Forfeited, Lost }
    public enum MiningAttemptStatus { Working, Paused, AwaitingCheck, Success, CriticalSuccess, Failure, CriticalFailure, TerminalNoCheck }
    public enum MiningCheckDegree { None, CriticalFailure, Failure, Success, CriticalSuccess }
    public enum MiningDiceSelection { None, Normal, Advantage, Disadvantage }
    public enum MiningWorkStage { Setup, Removal, SortingAndReceipt, AwaitingCheck, Resolved }

    /// <summary>One authored exposed mineral parcel. This is content and physical authority, not a
    /// generated geology rule. It references the actual worksite, implements and receiver.</summary>
    public sealed class MiningDepositRecord
    {
        public string Id { get; }
        public string VersionId { get; }
        public string SiteId { get; }
        public string OwnerId { get; }
        public int SiteX { get; }
        public int SiteY { get; }
        public string MiningToolsId { get; }
        public string PickId { get; }
        public string ReceiverId { get; }
        public string WorkSurfaceId { get; }
        public int? ExactCheckDc { get; }
        public bool HurryFeasible { get; }

        public MiningDepositRecord(string id,string versionId,string siteId,string ownerId,int siteX,int siteY,
            string miningToolsId,string pickId,string receiverId,string workSurfaceId,int? exactCheckDc=null,bool hurryFeasible=false)
        {
            foreach(string value in new[]{id,versionId,siteId,ownerId,miningToolsId,pickId,receiverId,workSurfaceId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid mining deposit identity.");
            if(siteX<0||siteY<0||exactCheckDc.HasValue&&(exactCheckDc.Value<1||exactCheckDc.Value>100))
                throw new ArgumentException("Invalid mining deposit profile.");
            Id=id;VersionId=versionId;SiteId=siteId;OwnerId=ownerId;SiteX=siteX;SiteY=siteY;
            MiningToolsId=miningToolsId;PickId=pickId;ReceiverId=receiverId;WorkSurfaceId=workSurfaceId;ExactCheckDc=exactCheckDc;HurryFeasible=hurryFeasible;
        }
    }

    /// <summary>A material category visible at one deposit. Tier zero means an exact source DC is required.</summary>
    public sealed class MiningCategoryRecord
    {
        private readonly string[] unitIds;
        public string Id { get; }
        public string DepositId { get; }
        public string MaterialId { get; }
        public int Tier { get; }
        public bool Accessible { get; }
        public string[] UnitIds=>unitIds.ToArray();
        public MiningCategoryRecord(string id,string depositId,string materialId,int tier,bool accessible,string[] unitIds)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(depositId)||!Validation.ValidId(materialId)
                ||tier<0||tier>6||unitIds==null||unitIds.Length<1||unitIds.Length>MiningValidation.MaxRecords
                ||unitIds.Any(x=>!Validation.ValidId(x))||unitIds.Distinct(StringComparer.Ordinal).Count()!=unitIds.Length)
                throw new ArgumentException("Invalid mining category.");
            Id=id;DepositId=depositId;MaterialId=materialId;Tier=tier;Accessible=accessible;
            this.unitIds=unitIds.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
        }
    }

    /// <summary>One actual finite physical mineral unit. Its mass and volume come from the authored node profile.</summary>
    public sealed class MiningMaterialUnitRecord
    {
        public string Id { get; }
        public string DepositId { get; }
        public string CategoryId { get; }
        public RuleQuantity MassPounds { get; }
        public RuleQuantity VolumeCubicFeet { get; }
        public long? ValueCopper { get; }
        public MiningUnitCondition Condition { get; }
        public MiningUnitStatus Status { get; }
        public string ReceivedLotId { get; }
        public string ReceivedContainerId { get; }
        public MiningMaterialUnitRecord(string id,string depositId,string categoryId,RuleQuantity massPounds,
            RuleQuantity volumeCubicFeet,long? valueCopper,MiningUnitCondition condition,MiningUnitStatus status,
            string receivedLotId="",string receivedContainerId="")
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(depositId)||!Validation.ValidId(categoryId)
                ||massPounds==default||volumeCubicFeet==default||valueCopper<0
                ||!Enum.IsDefined(typeof(MiningUnitCondition),condition)||!Enum.IsDefined(typeof(MiningUnitStatus),status)
                ||receivedLotId==null||receivedLotId!=""&&!Validation.ValidId(receivedLotId)
                ||receivedContainerId==null||receivedContainerId!=""&&!Validation.ValidId(receivedContainerId)
                ||(status==MiningUnitStatus.Extracted)!=(receivedLotId!="")
                ||(status==MiningUnitStatus.Extracted)!=(receivedContainerId!=""))
                throw new ArgumentException("Invalid mining material unit.");
            Id=id;DepositId=depositId;CategoryId=categoryId;MassPounds=massPounds;VolumeCubicFeet=volumeCubicFeet;
            ValueCopper=valueCopper;Condition=condition;Status=status;ReceivedLotId=receivedLotId;ReceivedContainerId=receivedContainerId;
        }
        public MiningMaterialUnitRecord WithStatus(MiningUnitStatus status,string receivedLotId="",string receivedContainerId="")
            =>new MiningMaterialUnitRecord(Id,DepositId,CategoryId,MassPounds,VolumeCubicFeet,ValueCopper,Condition,status,receivedLotId,receivedContainerId);
    }

    /// <summary>Authoritative resumable extraction job. Stage position is derived from WorkDone and
    /// its immutable persisted 1:10:1 plan; stage boundaries do not award separate checks or output.</summary>
    public sealed class MiningAttemptRecord
    {
        private readonly string[] selectedCategoryIds,selectedUnitIds;
        public string Id { get; }
        public string WorkerId { get; }
        public string DepositId { get; }
        public string DepositVersionId { get; }
        public int AccessibleCategoryCount { get; }
        public MiningAbilityChoice Ability { get; }
        public bool Hurried { get; }
        public string[] SelectedCategoryIds=>selectedCategoryIds.ToArray();
        public string[] SelectedUnitIds=>selectedUnitIds.ToArray();
        public string FailureVictimPreference { get; }
        public string CriticalRecoveryPreference { get; }
        public string AssistantId { get; }
        public int AssistantBonus { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public int DurationSeconds { get; }
        public int SetupSeconds { get; }
        public int RemovalSeconds { get; }
        public int SortingSeconds { get; }
        public RuleTime WorkDone { get; }
        public RuleTime? CommittedAt { get; }
        public MiningAttemptStatus Status { get; }
        public int AbilityModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int CheckDc { get; }
        public RuleTime? ResolvedAt { get; }
        public RuleTime? ClosedAt { get; }
        public MiningCheckDegree Degree { get; }
        public MiningDiceSelection DiceSelection { get; }
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

        public MiningAttemptRecord(string id,string workerId,string depositId,string depositVersionId,int accessibleCategoryCount,
            MiningAbilityChoice ability,bool hurried,string[] selectedCategoryIds,string[] selectedUnitIds,string failureVictimPreference,
            RuleTime startedAt,RuleTime updatedAt,int durationSeconds,int setupSeconds,int removalSeconds,int sortingSeconds,
            RuleTime workDone,RuleTime? committedAt,MiningAttemptStatus status,int abilityModifier,int proficiencyRank,
            int proficiencyBonus,int checkDc,RuleTime? resolvedAt,RuleTime? closedAt,MiningCheckDegree degree,
            MiningDiceSelection diceSelection,int firstDie,int secondDie,int natural,int checkModifier,int d4Rolled,
            long damageApplied,string accidentDamageType,int woundRoll,int injuryRoll,uint randomBefore,uint randomAfter,long wordsConsumed,
            string criticalRecoveryPreference="",string assistantId="",int assistantBonus=0)
        {
            foreach(string value in new[]{id,workerId,depositId,depositVersionId})if(!Validation.ValidId(value))throw new ArgumentException("Invalid mining attempt identity.");
            if(accessibleCategoryCount<1||!Enum.IsDefined(typeof(MiningAbilityChoice),ability)
                ||selectedCategoryIds==null||selectedUnitIds==null||selectedCategoryIds.Length<1
                ||selectedCategoryIds.Length>MiningValidation.MaxRecords||selectedUnitIds.Length<1||selectedUnitIds.Length>MiningValidation.MaxRecords
                ||selectedCategoryIds.Any(x=>!Validation.ValidId(x))||selectedUnitIds.Any(x=>!Validation.ValidId(x))
                ||selectedCategoryIds.Distinct(StringComparer.Ordinal).Count()!=selectedCategoryIds.Length
                ||selectedUnitIds.Distinct(StringComparer.Ordinal).Count()!=selectedUnitIds.Length
                ||failureVictimPreference==null||failureVictimPreference!=""&&!Validation.ValidId(failureVictimPreference)
                ||criticalRecoveryPreference==null||criticalRecoveryPreference!=""&&!Validation.ValidId(criticalRecoveryPreference)
                ||assistantId==null||assistantId!=""&&!Validation.ValidId(assistantId)
                ||startedAt>updatedAt||durationSeconds<60||durationSeconds%60!=0||setupSeconds<=0||removalSeconds<=0||sortingSeconds<=0
                ||checked(setupSeconds+removalSeconds+sortingSeconds)!=durationSeconds
                ||workDone<default(RuleTime)||workDone>new RuleTime(durationSeconds)
                ||committedAt.HasValue&&(committedAt.Value<startedAt||committedAt.Value>updatedAt)
                ||(workDone>new RuleTime(setupSeconds))!=committedAt.HasValue
                ||!Enum.IsDefined(typeof(MiningAttemptStatus),status)||!Enum.IsDefined(typeof(MiningCheckDegree),degree)
                ||!Enum.IsDefined(typeof(MiningDiceSelection),diceSelection)||proficiencyRank<0||proficiencyRank>2
                ||proficiencyBonus<0||proficiencyBonus>20||checkDc<1||checkDc>100
                ||firstDie<0||firstDie>20||secondDie<0||secondDie>20||natural<0||natural>20||d4Rolled<0||d4Rolled>4
                ||damageApplied<0||accidentDamageType==null||woundRoll<0||woundRoll>20||injuryRoll<0||injuryRoll>6||wordsConsumed<0)
                throw new ArgumentException("Invalid mining attempt.");
            bool resolved=status==MiningAttemptStatus.Success||status==MiningAttemptStatus.CriticalSuccess
                ||status==MiningAttemptStatus.Failure||status==MiningAttemptStatus.CriticalFailure;
            bool terminal=status==MiningAttemptStatus.TerminalNoCheck;
            if(assistantId==workerId||assistantBonus<0||assistantBonus>1
                ||assistantBonus!=(resolved&&assistantId!=""?1:0))
                throw new ArgumentException("Mining assistance evidence does not match its completed team check.");
            bool dieValid=diceSelection==MiningDiceSelection.Normal?secondDie==0&&natural==firstDie
                :diceSelection==MiningDiceSelection.Advantage?secondDie>=1&&natural==Math.Max(firstDie,secondDie)
                :diceSelection==MiningDiceSelection.Disadvantage&&secondDie>=1&&natural==Math.Min(firstDie,secondDie);
            if(resolved!=(resolvedAt.HasValue&&degree!=MiningCheckDegree.None&&diceSelection!=MiningDiceSelection.None
                    &&firstDie>=1&&natural>=1&&randomBefore!=0&&randomAfter!=0&&wordsConsumed>0)
                ||resolved&&!dieValid||resolved&&workDone!=new RuleTime(durationSeconds)
                ||resolved!=resolvedAt.HasValue||(resolved||terminal)!=closedAt.HasValue
                ||terminal&&(resolvedAt.HasValue||degree!=MiningCheckDegree.None||diceSelection!=MiningDiceSelection.None
                    ||firstDie!=0||secondDie!=0||natural!=0||randomBefore!=0||randomAfter!=0||wordsConsumed!=0)
                ||!resolved&&!terminal&&(resolvedAt.HasValue||closedAt.HasValue||degree!=MiningCheckDegree.None
                    ||diceSelection!=MiningDiceSelection.None||firstDie!=0||secondDie!=0||natural!=0||randomBefore!=0||randomAfter!=0||wordsConsumed!=0)
                ||resolved&&((status==MiningAttemptStatus.Success)!=(degree==MiningCheckDegree.Success)
                    ||(status==MiningAttemptStatus.CriticalSuccess)!=(degree==MiningCheckDegree.CriticalSuccess)
                    ||(status==MiningAttemptStatus.Failure)!=(degree==MiningCheckDegree.Failure)
                    ||(status==MiningAttemptStatus.CriticalFailure)!=(degree==MiningCheckDegree.CriticalFailure))
                ||(status==MiningAttemptStatus.CriticalFailure)!=(d4Rolled!=0)
                ||(d4Rolled==0&&(damageApplied!=0||accidentDamageType!=""||woundRoll!=0||injuryRoll!=0))
                ||(d4Rolled!=0&&accidentDamageType!="bludgeoning")
                ||closedAt.HasValue&&closedAt.Value!=updatedAt
                ||resolvedAt.HasValue&&resolvedAt.Value!=updatedAt)
                throw new ArgumentException("Mining attempt result does not match its persisted check.");
            Id=id;WorkerId=workerId;DepositId=depositId;DepositVersionId=depositVersionId;AccessibleCategoryCount=accessibleCategoryCount;
            Ability=ability;Hurried=hurried;this.selectedCategoryIds=selectedCategoryIds.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            this.selectedUnitIds=selectedUnitIds.OrderBy(x=>x,StringComparer.Ordinal).ToArray();FailureVictimPreference=failureVictimPreference;
            CriticalRecoveryPreference=criticalRecoveryPreference;
            AssistantId=assistantId;AssistantBonus=assistantBonus;
            StartedAt=startedAt;UpdatedAt=updatedAt;DurationSeconds=durationSeconds;SetupSeconds=setupSeconds;RemovalSeconds=removalSeconds;
            SortingSeconds=sortingSeconds;WorkDone=workDone;CommittedAt=committedAt;Status=status;AbilityModifier=abilityModifier;
            ProficiencyRank=proficiencyRank;ProficiencyBonus=proficiencyBonus;CheckDc=checkDc;ResolvedAt=resolvedAt;ClosedAt=closedAt;
            Degree=degree;DiceSelection=diceSelection;FirstDie=firstDie;SecondDie=secondDie;Natural=natural;CheckModifier=checkModifier;
            D4Rolled=d4Rolled;DamageApplied=damageApplied;AccidentDamageType=accidentDamageType;WoundRoll=woundRoll;InjuryRoll=injuryRoll;
            RandomBefore=randomBefore;RandomAfter=randomAfter;WordsConsumed=wordsConsumed;
        }

        public MiningAttemptRecord WithWork(RuleTime at,RuleTime work,MiningAttemptStatus status,RuleTime? committedAt)
            =>new MiningAttemptRecord(Id,WorkerId,DepositId,DepositVersionId,AccessibleCategoryCount,Ability,Hurried,
                selectedCategoryIds,selectedUnitIds,FailureVictimPreference,StartedAt,at,DurationSeconds,SetupSeconds,RemovalSeconds,
                SortingSeconds,work,committedAt,status,AbilityModifier,ProficiencyRank,ProficiencyBonus,CheckDc,null,null,
                MiningCheckDegree.None,MiningDiceSelection.None,0,0,0,0,0,0,"",0,0,0,0,0,CriticalRecoveryPreference,AssistantId);

        public MiningAttemptRecord WithResult(RuleTime at,MiningAttemptStatus status,MiningCheckDegree degree,
            MiningDiceSelection selection,int firstDie,int secondDie,int natural,int modifier,int d4,long damage,string damageType,
            int wound,int injury,uint randomBefore,uint randomAfter,long words,int assistantBonus=0)
            =>new MiningAttemptRecord(Id,WorkerId,DepositId,DepositVersionId,AccessibleCategoryCount,Ability,Hurried,
                selectedCategoryIds,selectedUnitIds,FailureVictimPreference,StartedAt,at,DurationSeconds,SetupSeconds,RemovalSeconds,
                SortingSeconds,new RuleTime(DurationSeconds),CommittedAt,status,AbilityModifier,ProficiencyRank,ProficiencyBonus,
                CheckDc,at,at,degree,selection,firstDie,secondDie,natural,modifier,d4,damage,damageType,wound,injury,randomBefore,randomAfter,words,
                CriticalRecoveryPreference,AssistantId,assistantBonus);

        public MiningAttemptRecord WithTerminalNoCheck(RuleTime at)
            =>new MiningAttemptRecord(Id,WorkerId,DepositId,DepositVersionId,AccessibleCategoryCount,Ability,Hurried,
                selectedCategoryIds,selectedUnitIds,FailureVictimPreference,StartedAt,at,DurationSeconds,SetupSeconds,RemovalSeconds,
                SortingSeconds,WorkDone,CommittedAt,MiningAttemptStatus.TerminalNoCheck,AbilityModifier,ProficiencyRank,
                ProficiencyBonus,CheckDc,null,at,MiningCheckDegree.None,MiningDiceSelection.None,0,0,0,0,0,0,"",0,0,0,0,0,
                CriticalRecoveryPreference,AssistantId);
    }

    /// <summary>Pure exposed-node calculations. These methods do not create deposits, units, tiers or output.</summary>
    public static class MiningExtractionRules
    {
        public static int DurationSeconds(int accessibleCategoryCount,int selectedCategoryCount,bool hurried)
        {
            if(accessibleCategoryCount<1||selectedCategoryCount<1||selectedCategoryCount>accessibleCategoryCount)
                throw new ArgumentOutOfRangeException(nameof(selectedCategoryCount));
            int numerator=checked(60*selectedCategoryCount);
            int minutes=checked((numerator+accessibleCategoryCount-1)/accessibleCategoryCount);
            if(minutes<1)minutes=1;
            if(hurried)minutes=checked((minutes+1)/2);
            return checked(minutes*60);
        }
        public static void StagePlan(int durationSeconds,out int setupSeconds,out int removalSeconds,out int sortingSeconds)
        {
            if(durationSeconds<60||durationSeconds%60!=0)throw new ArgumentOutOfRangeException(nameof(durationSeconds));
            setupSeconds=durationSeconds/12;
            removalSeconds=checked(durationSeconds-2*setupSeconds);
            sortingSeconds=setupSeconds;
        }
        public static int TierDc(int tier)
        {
            switch(tier) {
                case 1:return 12;case 2:return 13;case 3:return 15;case 4:return 16;case 5:return 18;case 6:return 19;
                default:throw new ArgumentOutOfRangeException(nameof(tier));
            }
        }
        public static MiningWorkStage Stage(MiningAttemptRecord attempt)
        {
            if(attempt==null)throw new ArgumentNullException(nameof(attempt));
            if(attempt.Status==MiningAttemptStatus.AwaitingCheck)return MiningWorkStage.AwaitingCheck;
            if(attempt.Status==MiningAttemptStatus.Success||attempt.Status==MiningAttemptStatus.CriticalSuccess
                ||attempt.Status==MiningAttemptStatus.Failure||attempt.Status==MiningAttemptStatus.CriticalFailure
                ||attempt.Status==MiningAttemptStatus.TerminalNoCheck)return MiningWorkStage.Resolved;
            if(attempt.WorkDone<new RuleTime(attempt.SetupSeconds))return MiningWorkStage.Setup;
            if(attempt.WorkDone<new RuleTime(checked(attempt.SetupSeconds+attempt.RemovalSeconds)))return MiningWorkStage.Removal;
            return MiningWorkStage.SortingAndReceipt;
        }
    }

    public static class MiningValidation
    {
        public const int MaxRecords=64;
        public static void Validate(Snapshot s)
        {
            if(s.MiningDeposits==null||s.MiningCategories==null||s.MiningUnits==null||s.MiningAttempts==null
                ||s.MineralPreparationProfiles==null||s.MineralPreparationAttempts==null
                ||s.MineralPreparationProfiles.Any(x=>x==null)||s.MineralPreparationAttempts.Any(x=>x==null)
                ||new[]{s.MiningDeposits.Length,s.MiningCategories.Length,s.MiningUnits.Length,s.MiningAttempts.Length}.Any(x=>x>MaxRecords)
                ||s.MiningDeposits.Any(x=>x==null)||s.MiningCategories.Any(x=>x==null)||s.MiningUnits.Any(x=>x==null)||s.MiningAttempts.Any(x=>x==null))
                throw new ArgumentException("Invalid mining collections.");
            if(s.SchemaVersion<Snapshot.MiningSchema) {
                if(s.MiningDeposits.Length+s.MiningCategories.Length+s.MiningUnits.Length+s.MiningAttempts.Length!=0)
                    throw new ArgumentException("Mining requires schema43.");
                return;
            }
            if(s.MiningDeposits.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.MiningDeposits.Length
                ||s.MiningCategories.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.MiningCategories.Length
                ||s.MiningUnits.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.MiningUnits.Length
                ||s.MiningAttempts.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.MiningAttempts.Length
                ||s.MiningAttempts.Select(x=>x.DepositId).Distinct(StringComparer.Ordinal).Count()!=s.MiningAttempts.Length)
                throw new ArgumentException("Duplicate mining identity or deposit claim.");
            foreach(var deposit in s.MiningDeposits) {
                if(!s.Actors.Any(x=>x.Id==deposit.OwnerId)||s.Structures.Any(x=>x.Id==deposit.WorkSurfaceId
                    &&(x.LocationId!=deposit.SiteId||x.OwnerId!=deposit.OwnerId)))
                    throw new ArgumentException("Mining deposit references an unknown owner or mismatched work surface.");
                if(s.MiningCategories.Count(x=>x.DepositId==deposit.Id)<1)throw new ArgumentException("Mining deposit has no material categories.");
                if(!deposit.ExactCheckDc.HasValue&&s.MiningCategories.Any(x=>x.DepositId==deposit.Id&&x.Tier==0))
                    throw new ArgumentException("Unknown mining tier requires an authored exact DC.");
            }
            foreach(var category in s.MiningCategories) {
                if(!s.MiningDeposits.Any(x=>x.Id==category.DepositId))throw new ArgumentException("Mining category references an unknown deposit.");
                if(category.UnitIds.Any(id=>!s.MiningUnits.Any(x=>x.Id==id&&x.CategoryId==category.Id&&x.DepositId==category.DepositId)))
                    throw new ArgumentException("Mining category/unit membership mismatch.");
            }
            foreach(var unit in s.MiningUnits) {
                if(!s.MiningCategories.Any(x=>x.Id==unit.CategoryId&&x.DepositId==unit.DepositId))throw new ArgumentException("Mining unit references an unknown category.");
                var source=s.Work.Lots.SingleOrDefault(x=>x.Id==unit.Id);
                var provenance=s.InventoryLots.SingleOrDefault(x=>x.LotId==unit.Id);
                bool wholeTransport=s.SchemaVersion>=Snapshot.HavenAppraisalSchema&&unit.Status==MiningUnitStatus.Extracted
                    &&unit.ReceivedLotId==unit.Id;
                if(source==null||source.UnitId!="mass-pound"||provenance==null||provenance.ParentId!=""
                    ||provenance.Nutrition!=NutritionKind.None||!wholeTransport&&provenance.OwnerId!=source.CustodianId
                    ||provenance.CreatedAmount!=unit.MassPounds)
                    throw new ArgumentException("Mining unit source inventory is invalid.");
                var integratedUse=s.SchemaVersion>=Snapshot.MiningToolCandidateSchema
                    ?s.MiningToolUses.SingleOrDefault(x=>x.PreparedUnitId==unit.Id&&x.PreparationCompletedAt.HasValue):null;
                if(unit.Status==MiningUnitStatus.Extracted) {
                    var preparation=s.MineralPreparationAttempts.SingleOrDefault(x=>x.UnitId==unit.Id&&x.Status==MineralPreparationStatus.Complete);
                    bool integratedPrepared=integratedUse!=null;
                    var output=s.InventoryLots.SingleOrDefault(x=>x.LotId==unit.ReceivedLotId);
                    var outputLot=s.Work.Lots.SingleOrDefault(x=>x.Id==unit.ReceivedLotId);
                    var body=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id);
                    bool prepared=preparation!=null||integratedPrepared;
                    string retainedId=preparation?.RetainedLotId??integratedUse?.RetainedLotId??unit.Id;
                    RuleQuantity retainedMass=preparation?.RetainedMassPounds??(integratedPrepared
                        ?unit.MassPounds-s.MineralPreparationProfiles.Single(x=>x.Id==s.MiningToolCandidateProfiles.Single(p=>p.Id==integratedUse.ProfileId).PreparationProfileId).GangueWastePounds
                        :unit.MassPounds);
                    string expectedProfile=preparation!=null?s.MineralPreparationProfiles.Single(x=>x.Id==preparation.ProfileId).DressedItemProfileId
                        :integratedPrepared&&integratedUse.DressedBenefitAwarded
                            ?s.MineralPreparationProfiles.Single(x=>x.Id==s.MiningToolCandidateProfiles.Single(p=>p.Id==integratedUse.ProfileId).PreparationProfileId).DressedItemProfileId
                            :body?.ProfileId??"";
                    if(unit.ReceivedLotId!=retainedId
                        ||(prepared?source.Amount!=default:source.Amount!=unit.MassPounds)
                        ||!wholeTransport&&!integratedPrepared&&source.LocationId!=unit.ReceivedContainerId
                        ||output==null||output.ParentId!=(prepared?unit.Id:"")
                        ||output.CreatedAmount!=retainedMass
                        ||output.OwnerId!=provenance.OwnerId||output.Nutrition!=NutritionKind.None||output.FreshUntil!=provenance.FreshUntil
                        ||!wholeTransport&&output.Access!=InventoryAccess.Stowed
                        ||outputLot==null||outputLot.UnitId!="mass-pound"||outputLot.Amount!=retainedMass
                        ||body==null||!wholeTransport&&(outputLot.LocationId!=unit.ReceivedContainerId
                            ||body.ParentId!=unit.ReceivedContainerId||body.Placement!=PortablePlacement.Contained)
                        ||wholeTransport&&(unit.ReceivedContainerId!=s.MiningDeposits.Single(x=>x.Id==unit.DepositId).ReceiverId
                            ||body.OwnerId!=provenance.OwnerId)
                        ||body.LinkedId!=unit.ReceivedLotId||body.LinkKind!=PortableLinkKind.InventoryLot
                        ||prepared&&body.ProfileId!=expectedProfile)
                        throw new ArgumentException("Mining receipt lost physical unit provenance.");
                } else if(integratedUse!=null) {
                    var deposit=s.MiningDeposits.Single(x=>x.Id==unit.DepositId);
                    var body=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id);
                    string ground="ground."+deposit.SiteX.ToString(System.Globalization.CultureInfo.InvariantCulture)+"."+
                        deposit.SiteY.ToString(System.Globalization.CultureInfo.InvariantCulture);
                    if(source.Amount!=default||source.LocationId!=ground
                        ||body==null||body.LinkedId!=integratedUse.RetainedLotId||body.ParentId!=""
                        ||body.Placement!=PortablePlacement.Ground||body.GroundX!=deposit.SiteX||body.GroundY!=deposit.SiteY)
                        throw new ArgumentException("Unawarded mining-tool preparation residue is not preserved at its worksite.");
                } else if(unit.Status==MiningUnitStatus.Lost) {
                    if(source.Amount!=default||s.PortableEquipment.Any(x=>x.Id==unit.Id))throw new ArgumentException("Lost mining unit remains physically available.");
                } else {
                    var body=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id);
                    var deposit=s.MiningDeposits.Single(x=>x.Id==unit.DepositId);
                    if(source.Amount!=unit.MassPounds||body==null||source.LocationId!=PortableEquipmentValidation.GroundLocation(body)
                        ||body.Placement!=PortablePlacement.Ground
                        ||body.ParentId!=""||body.LinkedId!=unit.Id||body.GroundX!=deposit.SiteX||body.GroundY!=deposit.SiteY)
                        throw new ArgumentException("Unreceived mining unit is not at its authored source.");
                }
            }
            if(s.MiningUnits.Any(x=>s.MiningCategories.Count(c=>c.UnitIds.Contains(x.Id,StringComparer.Ordinal))!=1))
                throw new ArgumentException("Mining unit must belong to exactly one category.");
            foreach(var deposit in s.MiningDeposits) {
                var categories=s.MiningCategories.Where(x=>x.DepositId==deposit.Id).ToArray();
                var units=s.MiningUnits.Where(x=>x.DepositId==deposit.Id).ToArray();
                if(RuleQuantity.Sum(units.Select(x=>x.MassPounds))>new RuleQuantity(50)
                    ||RuleQuantity.Sum(units.Select(x=>x.VolumeCubicFeet))>new RuleQuantity(1))
                    throw new ArgumentException("Mining parcel exceeds its exposed-node handling limits.");
                var tools=s.PortableEquipment.Where(x=>x.Id==deposit.MiningToolsId||x.Id==deposit.PickId||x.Id==deposit.ReceiverId).ToArray();
                if(tools.Any(x=>x.OwnerId!=deposit.OwnerId||x.CustodianId!=deposit.OwnerId))
                    throw new ArgumentException("Mining deposit equipment owner or custodian mismatch.");
                var receiver=tools.SingleOrDefault(x=>x.Id==deposit.ReceiverId);
                if(receiver!=null&&(!receiver.CapacityPounds.HasValue||!receiver.CapacityCubicFeet.HasValue||receiver.FitRuleId==""))
                    throw new ArgumentException("Mining receiver capacity and fit are required.");
                var extracted=receiver==null?Array.Empty<MiningMaterialUnitRecord>()
                    :units.Where(x=>x.Status==MiningUnitStatus.Extracted&&x.ReceivedContainerId==receiver.Id).ToArray();
                var reserved=s.MiningAttempts.Where(x=>x.DepositId==deposit.Id&&(x.Status==MiningAttemptStatus.Working
                    ||x.Status==MiningAttemptStatus.Paused||x.Status==MiningAttemptStatus.AwaitingCheck))
                    .SelectMany(x=>{
                        var use=s.SchemaVersion>=Snapshot.MiningToolCandidateSchema
                            ?s.MiningToolUses.SingleOrDefault(y=>y.MiningAttemptId==x.Id):null;
                        return x.SelectedUnitIds.Concat(use==null||use.ReservedUnitId==""
                            ?Array.Empty<string>():new[]{use.ReservedUnitId});
                    }).Select(id=>units.Single(u=>u.Id==id));
                if(extracted.Length>0&&receiver==null)throw new ArgumentException("Extracted mining units have no receiver.");
                if(receiver!=null&&(RuleQuantity.Sum(extracted.Select(x=>MineralPreparationValidation.ReceivedMass(s,x)).Concat(reserved.Select(x=>x.MassPounds)))>receiver.CapacityPounds.Value
                    ||RuleQuantity.Sum(extracted.Select(x=>x.VolumeCubicFeet).Concat(reserved.Select(x=>x.VolumeCubicFeet)))>receiver.CapacityCubicFeet.Value
                    ||extracted.Any(x=>!receiver.FitMemberIds.Contains(x.Id,StringComparer.Ordinal))
                    ||reserved.Any(x=>!receiver.FitMemberIds.Contains(x.Id,StringComparer.Ordinal))))
                    throw new ArgumentException("Mining receiver capacity or fit exceeded.");
                if(categories.Any(x=>x.UnitIds.Length==0))throw new ArgumentException("Mining category has no material units.");
            }
            foreach(var attempt in s.MiningAttempts)ValidateAttempt(s,attempt);
        }

        private static RuleTime Add(RuleTime first,RuleTime second)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)first.Numerator*second.Denominator
                +(System.Numerics.BigInteger)second.Numerator*first.Denominator,(System.Numerics.BigInteger)first.Denominator*second.Denominator);
        private static RuleTime Subtract(RuleTime first,RuleTime second)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)first.Numerator*second.Denominator
                -(System.Numerics.BigInteger)second.Numerator*first.Denominator,(System.Numerics.BigInteger)first.Denominator*second.Denominator);

        private static void ValidateAttempt(Snapshot s,MiningAttemptRecord attempt)
        {
            if(attempt.AssistantId!=""&&(s.SchemaVersion!=Snapshot.MiningAssistantSchema
                ||attempt.AssistantId==attempt.WorkerId||!s.Actors.Any(x=>x.Id==attempt.AssistantId)
                ||s.SkillTraining.Count(x=>x.ActorId==attempt.AssistantId&&x.SkillId=="mining-tools")!=1
                ||s.SkillTraining.Single(x=>x.ActorId==attempt.AssistantId&&x.SkillId=="mining-tools").ProficiencyRank<=0))
                throw new ArgumentException("Mining assistant binding is unsupported or untrained.");
            var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==attempt.DepositId)
                ??throw new ArgumentException("Mining attempt references an unknown deposit.");
            if(attempt.DepositVersionId!=deposit.VersionId)throw new ArgumentException("Mining attempt version mismatch.");
            var accessible=s.MiningCategories.Where(x=>x.DepositId==deposit.Id&&x.Accessible).OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray();
            var selected=attempt.SelectedCategoryIds.Select(id=>accessible.SingleOrDefault(x=>x.Id==id)
                ??throw new ArgumentException("Mining attempt selected an inaccessible category.")).ToArray();
            var selectedUnits=selected.SelectMany(x=>x.UnitIds).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            if(!selectedUnits.SequenceEqual(attempt.SelectedUnitIds.OrderBy(x=>x,StringComparer.Ordinal))
                ||attempt.AccessibleCategoryCount!=accessible.Length
                ||attempt.DurationSeconds!=MiningExtractionRules.DurationSeconds(accessible.Length,selected.Length,attempt.Hurried))
                throw new ArgumentException("Mining attempt duration or selection is inconsistent.");
            MiningExtractionRules.StagePlan(attempt.DurationSeconds,out int setup,out int removal,out int sorting);
            if(attempt.SetupSeconds!=setup||attempt.RemovalSeconds!=removal||attempt.SortingSeconds!=sorting)
                throw new ArgumentException("Mining attempt stage plan is not canonical.");
            var selectedMaterial=attempt.SelectedUnitIds.Select(id=>s.MiningUnits.Single(x=>x.Id==id)).ToArray();
            bool open=attempt.Status==MiningAttemptStatus.Working||attempt.Status==MiningAttemptStatus.Paused||attempt.Status==MiningAttemptStatus.AwaitingCheck;
            if(open&&selectedMaterial.Any(x=>x.Status!=MiningUnitStatus.Available))
                throw new ArgumentException("Open mining attempt selection is no longer available.");
            var damaged=selectedMaterial.Where(x=>x.Condition==MiningUnitCondition.DamagedPotentiallyRecoverable).ToArray();
            if(damaged.Length>1&&attempt.CriticalRecoveryPreference=="")
                throw new ArgumentException("Mining critical recovery choice was not persisted.");
            if(attempt.CriticalRecoveryPreference!=""&&!damaged.Any(x=>x.Id==attempt.CriticalRecoveryPreference))
                throw new ArgumentException("Mining critical recovery preference does not match its selected material.");
            if(selectedMaterial.Any(x=>!x.ValueCopper.HasValue)) {
                if(attempt.FailureVictimPreference!="")throw new ArgumentException("Mining unknown values require the stable neutral failure order.");
            } else {
                long highest=selectedMaterial.Max(x=>x.ValueCopper.Value);
                var top=selectedMaterial.Where(x=>x.ValueCopper.Value==highest).ToArray();
                if(top.Length>1&&attempt.FailureVictimPreference==""
                    ||attempt.FailureVictimPreference!=""&&!top.Any(x=>x.Id==attempt.FailureVictimPreference))
                    throw new ArgumentException("Mining failure victim choice is inconsistent with selected values.");
            }
            if(attempt.Hurried&&!deposit.HurryFeasible)
                throw new ArgumentException("Mining attempt claims an unauthored hurry allowance.");
            int expectedDc=deposit.ExactCheckDc??MiningExtractionRules.TierDc(selected.Max(x=>x.Tier));
            if(attempt.CheckDc!=expectedDc)throw new ArgumentException("Mining attempt difficulty does not match the selected tier.");
            var toolReserves=s.SchemaVersion>=Snapshot.MiningToolCandidateSchema?s.MiningToolUses
                .Where(x=>x.MiningAttemptId==attempt.Id&&x.ReservedUnitId!="").Select(x=>x.ReservedUnitId).ToArray():Array.Empty<string>();
            var unselectedUnits=s.MiningCategories.Where(x=>x.DepositId==deposit.Id&&x.Accessible
                &&!attempt.SelectedCategoryIds.Contains(x.Id,StringComparer.Ordinal)).SelectMany(x=>x.UnitIds)
                .Where(id=>!toolReserves.Contains(id,StringComparer.Ordinal))
                .Select(id=>s.MiningUnits.Single(x=>x.Id==id));
            bool committed=attempt.CommittedAt.HasValue;
            if(unselectedUnits.Any(x=>committed?x.Status!=MiningUnitStatus.Forfeited:x.Status==MiningUnitStatus.Forfeited))
                throw new ArgumentException("Mining partial-selection commitment is inconsistent.");
            var claims=attempt.SelectedUnitIds.Select((id,index)=>s.Work.Reservations.SingleOrDefault(r=>r.Id==MiningIds.Reservation(attempt.Id,index)))
                .ToArray();
            var toolUse=s.SchemaVersion>=Snapshot.MiningToolCandidateSchema?s.MiningToolUses.SingleOrDefault(x=>x.MiningAttemptId==attempt.Id):null;
            int expectedClaimCount=attempt.SelectedUnitIds.Length+(toolUse!=null&&toolUse.ReservedUnitId!=""?1:0);
            if(claims.Length!=attempt.SelectedUnitIds.Length||s.Work.Reservations.Count(r=>r.JobId==attempt.Id)!=expectedClaimCount
                ||claims.Any(x=>x==null||x.JobId!=attempt.Id)||attempt.SelectedUnitIds.Select((id,index)=>claims[index].LotId!=id
                ||claims[index].Amount!=s.MiningUnits.Single(x=>x.Id==id).MassPounds).Any(x=>x))
                throw new ArgumentException("Mining material reservation mismatch.");
            for(int i=0;i<claims.Length;i++) {
                bool split=toolUse!=null&&toolUse.PreparedUnitId==attempt.SelectedUnitIds[i]&&toolUse.PreparationCompletedAt.HasValue;
                if(open&&(split?claims[i].RemainingAmount!=default||claims[i].Status!=ReservationStatus.Released
                        :claims[i].RemainingAmount!=claims[i].Amount||claims[i].Status!=ReservationStatus.Reserved)
                    ||!open&&(claims[i].RemainingAmount!=default||claims[i].Status!=ReservationStatus.Released))
                    throw new ArgumentException("Mining reservation settlement does not match its attempt.");
            }
            var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==attempt.Id).OrderBy(x=>x.Start).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
            string[] workers=attempt.AssistantId==""?new[]{attempt.WorkerId}:new[]{attempt.WorkerId,attempt.AssistantId};
            if(intervals.Any(x=>!workers.Contains(x.WorkerId,StringComparer.Ordinal))||intervals.Length>0&&intervals[0].Start<attempt.StartedAt
                ||attempt.UpdatedAt>s.RuleClock||attempt.AssistantId!=""&&intervals.Any(x=>x.Start>s.RuleClock))
                throw new ArgumentException("Mining worker interval history is inconsistent.");
            foreach(var segment in intervals.GroupBy(x=>new{x.Start,x.End}))
                if(segment.Count()!=workers.Length||workers.Any(worker=>segment.Count(x=>x.WorkerId==worker)!=1))
                    throw new ArgumentException("Mining team labor intervals do not match.");
            if(attempt.Status==MiningAttemptStatus.Working) {
                var active=intervals.Where(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock).ToArray();
                var bookedRemaining=active.Length==workers.Length?new RuleQuantity(active[0].End.Numerator,active[0].End.Denominator)
                    -new RuleQuantity(s.RuleClock.Numerator,s.RuleClock.Denominator):default;
                var workRemaining=new RuleQuantity(attempt.DurationSeconds)-new RuleQuantity(attempt.WorkDone.Numerator,attempt.WorkDone.Denominator);
                if(active.Length!=workers.Length||workers.Any(worker=>active.Count(x=>x.WorkerId==worker)!=1)
                    ||active.Select(x=>x.End).Distinct().Count()!=1||bookedRemaining!=workRemaining)
                    throw new ArgumentException("Working mining job lacks its exact synchronized team interval.");
            } else if(intervals.Any(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock))
                throw new ArgumentException("Inactive mining job retains a live worker interval.");
            RuleTime credited=default;RuleTime? expectedCommit=null;
            foreach(var interval in intervals.Where(x=>x.WorkerId==attempt.WorkerId)) {
                if(interval.Start>=s.RuleClock)continue;
                RuleTime end=interval.End<s.RuleClock?interval.End:s.RuleClock;
                if(end<=interval.Start)continue;
                RuleTime span=Subtract(end,interval.Start);
                if(!expectedCommit.HasValue) {
                    RuleTime untilRemoval=Subtract(new RuleTime(attempt.SetupSeconds),credited);
                    if(span>untilRemoval)expectedCommit=Add(interval.Start,untilRemoval);
                }
                credited=Add(credited,span);
            }
            if(credited!=attempt.WorkDone||expectedCommit!=attempt.CommittedAt)
                throw new ArgumentException("Mining credited work or commitment time differs from booked labor.");
            if(attempt.Status==MiningAttemptStatus.AwaitingCheck&&attempt.WorkDone!=new RuleTime(attempt.DurationSeconds))
                throw new ArgumentException("Mining check awaits unfinished labor.");
            if(attempt.Status==MiningAttemptStatus.TerminalNoCheck&&attempt.SelectedUnitIds.Any(id=>s.MiningUnits.Single(x=>x.Id==id).Status!=MiningUnitStatus.Lost))
                throw new ArgumentException("Terminal mining claim still has selected material.");
            if(attempt.Status==MiningAttemptStatus.Success||attempt.Status==MiningAttemptStatus.CriticalSuccess) {
                var recoveredDamaged=attempt.Status==MiningAttemptStatus.CriticalSuccess&&damaged.Length>0
                    ?damaged.SingleOrDefault(x=>x.Id==attempt.CriticalRecoveryPreference)??damaged.OrderBy(x=>x.Id,StringComparer.Ordinal).First():null;
                foreach(var unit in selectedMaterial) {
                    bool eligible=unit.Condition==MiningUnitCondition.Intact||unit==recoveredDamaged;
                    if(eligible!=(unit.Status==MiningUnitStatus.Extracted))throw new ArgumentException("Mining success output does not match eligible baseline.");
                }
                for(int i=0;i<claims.Length;i++)
                    if(claims[i].Status!=ReservationStatus.Released)throw new ArgumentException("Mining success retained a mineral claim.");
            }
            if(attempt.Status==MiningAttemptStatus.Failure||attempt.Status==MiningAttemptStatus.CriticalFailure) {
                if(selectedMaterial.Any(x=>x.Status!=MiningUnitStatus.Ruined&&x.Status!=MiningUnitStatus.Spent))
                    throw new ArgumentException("Failed mining claim remains reusable.");
                if(claims.Any(x=>x.Status!=ReservationStatus.Released))throw new ArgumentException("Failed mining claim did not release material reservations.");
            }
        }
    }

    /// <summary>Stable identities for the mining procedure's shared-ledger resource claims.</summary>
    public static class MiningIds
    {
        public static string Reservation(string jobId,int index)
        {
            if(!Validation.ValidId(jobId)||index<0)throw new ArgumentException("Invalid mining claim identity.");
            return jobId+".claim."+index.ToString(System.Globalization.CultureInfo.InvariantCulture);
        }
        public static string ToolReserveReservation(string jobId)
        {
            if(!Validation.ValidId(jobId))throw new ArgumentException("Invalid mining-tool reserve claim identity.");
            return jobId+".tool-reserve";
        }
    }

    public enum MineralPreparationStatus { Working, Paused, AwaitingCompletion, Complete }

    /// <summary>Explicit TEST_ONLY mass measurement and identity mapping for one ordinary mineral unit.
    /// This is authored fixture data, not a general dressing loss formula.</summary>
    public sealed class MineralPreparationProfileRecord
    {
        public string Id { get; }
        public string UnitId { get; }
        public RuleQuantity GangueWastePounds { get; }
        public string DressedItemProfileId { get; }
        public string GangueItemProfileId { get; }

        public MineralPreparationProfileRecord(string id,string unitId,RuleQuantity gangueWastePounds,
            string dressedItemProfileId,string gangueItemProfileId)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(unitId)||gangueWastePounds<default(RuleQuantity)
                ||!Validation.ValidId(dressedItemProfileId)||!Validation.ValidId(gangueItemProfileId))
                throw new ArgumentException("Invalid mineral preparation profile.");
            Id=id;UnitId=unitId;GangueWastePounds=gangueWastePounds;
            DressedItemProfileId=dressedItemProfileId;GangueItemProfileId=gangueItemProfileId;
        }

        public bool HasSameContent(MineralPreparationProfileRecord other)
            =>other!=null&&Id==other.Id&&UnitId==other.UnitId&&GangueWastePounds==other.GangueWastePounds
                &&DressedItemProfileId==other.DressedItemProfileId&&GangueItemProfileId==other.GangueItemProfileId;
    }

    /// <summary>Append-only history for no-roll ten-minute mundane dressing. The mining unit remains
    /// the ingredient identity; retained material and gangue are conserved inventory descendants.</summary>
    public sealed class MineralPreparationAttemptRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public string ProfileId { get; }
        public string UnitId { get; }
        public string SourceLotId { get; }
        public string ReservationId { get; }
        public RuleQuantity InputMassPounds { get; }
        public RuleQuantity GangueWastePounds { get; }
        public RuleQuantity RetainedMassPounds { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime WorkDone { get; }
        public MineralPreparationStatus Status { get; }
        public string RetainedLotId { get; }
        public string GangueLotId { get; }

        public MineralPreparationAttemptRecord(string id,string workerId,string profileId,string unitId,string sourceLotId,
            string reservationId,RuleQuantity inputMassPounds,RuleQuantity gangueWastePounds,RuleQuantity retainedMassPounds,
            RuleTime startedAt,RuleTime updatedAt,RuleTime workDone,MineralPreparationStatus status,
            string retainedLotId="",string gangueLotId="")
        {
            bool complete=status==MineralPreparationStatus.Complete;
            if(!Validation.ValidId(id)||!Validation.ValidId(workerId)||!Validation.ValidId(profileId)||!Validation.ValidId(unitId)
                ||!Validation.ValidId(sourceLotId)||!Validation.ValidId(reservationId)||inputMassPounds<=default(RuleQuantity)
                ||gangueWastePounds<default(RuleQuantity)||retainedMassPounds<=default(RuleQuantity)
                ||gangueWastePounds+retainedMassPounds!=inputMassPounds||startedAt>updatedAt
                ||workDone<default(RuleTime)||workDone>new RuleTime(MineralPreparationValidation.WorkSeconds)
                ||!Enum.IsDefined(typeof(MineralPreparationStatus),status)||retainedLotId==null||gangueLotId==null
                ||(retainedLotId!=""&&!Validation.ValidId(retainedLotId))||(gangueLotId!=""&&!Validation.ValidId(gangueLotId))
                ||complete&&(workDone!=new RuleTime(MineralPreparationValidation.WorkSeconds)||retainedLotId==""
                    ||(gangueWastePounds==default)!=(gangueLotId==""))
                ||!complete&&(retainedLotId!=""||gangueLotId!="")
                ||(status==MineralPreparationStatus.Working||status==MineralPreparationStatus.Paused)
                    &&workDone>=new RuleTime(MineralPreparationValidation.WorkSeconds)
                ||status==MineralPreparationStatus.AwaitingCompletion&&workDone!=new RuleTime(MineralPreparationValidation.WorkSeconds))
                throw new ArgumentException("Invalid mineral preparation attempt.");
            Id=id;WorkerId=workerId;ProfileId=profileId;UnitId=unitId;SourceLotId=sourceLotId;ReservationId=reservationId;
            InputMassPounds=inputMassPounds;GangueWastePounds=gangueWastePounds;RetainedMassPounds=retainedMassPounds;
            StartedAt=startedAt;UpdatedAt=updatedAt;WorkDone=workDone;Status=status;RetainedLotId=retainedLotId;GangueLotId=gangueLotId;
        }

        public MineralPreparationAttemptRecord WithWork(RuleTime at,RuleTime work,MineralPreparationStatus status)
            =>new MineralPreparationAttemptRecord(Id,WorkerId,ProfileId,UnitId,SourceLotId,ReservationId,InputMassPounds,
                GangueWastePounds,RetainedMassPounds,StartedAt,at,work,status);

        public MineralPreparationAttemptRecord Complete(RuleTime at,string retainedLotId,string gangueLotId)
            =>new MineralPreparationAttemptRecord(Id,WorkerId,ProfileId,UnitId,SourceLotId,ReservationId,InputMassPounds,
                GangueWastePounds,RetainedMassPounds,StartedAt,at,new RuleTime(MineralPreparationValidation.WorkSeconds),
                MineralPreparationStatus.Complete,retainedLotId,gangueLotId);
    }

    public static class MineralPreparationValidation
    {
        public const int WorkSeconds=600;
        public const int MaxRecords=MiningValidation.MaxRecords;
        private static RuleTime Add(RuleTime a,RuleTime b)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator*b.Denominator
                +(System.Numerics.BigInteger)b.Numerator*a.Denominator,(System.Numerics.BigInteger)a.Denominator*b.Denominator);
        private static RuleTime Subtract(RuleTime a,RuleTime b)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator*b.Denominator
                -(System.Numerics.BigInteger)b.Numerator*a.Denominator,(System.Numerics.BigInteger)a.Denominator*b.Denominator);

        internal static RuleQuantity ReceivedMass(Snapshot s,MiningMaterialUnitRecord unit)
        {
            var preparation=s.MineralPreparationAttempts.SingleOrDefault(x=>x.UnitId==unit.Id&&x.Status==MineralPreparationStatus.Complete);
            if(preparation!=null)return preparation.RetainedMassPounds;
            var toolUse=s.SchemaVersion>=Snapshot.MiningToolCandidateSchema
                ?s.MiningToolUses.SingleOrDefault(x=>x.PreparedUnitId==unit.Id&&x.PreparationCompletedAt.HasValue):null;
            if(toolUse!=null) {
                var candidate=s.MiningToolCandidateProfiles.Single(x=>x.Id==toolUse.ProfileId);
                var profile=s.MineralPreparationProfiles.Single(x=>x.Id==candidate.PreparationProfileId);
                return unit.MassPounds-profile.GangueWastePounds;
            }
            return unit.MassPounds;
        }

        public static void Validate(Snapshot s)
        {
            if(s.MineralPreparationProfiles==null||s.MineralPreparationAttempts==null
                ||s.MineralPreparationProfiles.Length>MaxRecords||s.MineralPreparationAttempts.Length>MaxRecords
                ||s.MineralPreparationProfiles.Any(x=>x==null)||s.MineralPreparationAttempts.Any(x=>x==null))
                throw new ArgumentException("Invalid mineral preparation collections.");
            if(s.SchemaVersion<Snapshot.MineralPreparationSchema) {
                if(s.MineralPreparationProfiles.Length+s.MineralPreparationAttempts.Length!=0)
                    throw new ArgumentException("Mineral preparation requires schema48.");
                return;
            }
            if(s.MineralPreparationProfiles.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.MineralPreparationProfiles.Length
                ||s.MineralPreparationProfiles.Select(x=>x.UnitId).Distinct(StringComparer.Ordinal).Count()!=s.MineralPreparationProfiles.Length
                ||s.MineralPreparationAttempts.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.MineralPreparationAttempts.Length
                ||s.MineralPreparationAttempts.Select(x=>x.UnitId).Distinct(StringComparer.Ordinal).Count()!=s.MineralPreparationAttempts.Length)
                throw new ArgumentException("Duplicate mineral preparation profile, job or unit.");
            foreach(var profile in s.MineralPreparationProfiles) {
                var unit=s.MiningUnits.SingleOrDefault(x=>x.Id==profile.UnitId)
                    ??throw new ArgumentException("Mineral preparation profile references unknown material.");
                if(unit.Condition!=MiningUnitCondition.Intact||unit.MassPounds>new RuleQuantity(1)
                    ||profile.GangueWastePounds>=unit.MassPounds)
                    throw new ArgumentException("Mundane preparation only accepts an ordinary intact unit no heavier than one pound with positive retained mass.");
            }
            foreach(var attempt in s.MineralPreparationAttempts) ValidateAttempt(s,attempt);
        }

        private static void ValidateAttempt(Snapshot s,MineralPreparationAttemptRecord attempt)
        {
            var profile=s.MineralPreparationProfiles.SingleOrDefault(x=>x.Id==attempt.ProfileId)
                ??throw new ArgumentException("Mineral preparation attempt references unknown content.");
            var unit=s.MiningUnits.SingleOrDefault(x=>x.Id==attempt.UnitId)
                ??throw new ArgumentException("Mineral preparation attempt references unknown mineral.");
            var deposit=s.MiningDeposits.Single(x=>x.Id==unit.DepositId);
            var input=s.Work.Lots.SingleOrDefault(x=>x.Id==attempt.SourceLotId);
            var source=s.InventoryLots.SingleOrDefault(x=>x.LotId==attempt.SourceLotId);
            var claim=s.Work.Reservations.SingleOrDefault(x=>x.Id==attempt.ReservationId);
            bool complete=attempt.Status==MineralPreparationStatus.Complete;
            bool open=!complete;
            if(profile.UnitId!=unit.Id||unit.Condition!=MiningUnitCondition.Intact||unit.MassPounds>new RuleQuantity(1)
                ||profile.GangueWastePounds!=attempt.GangueWastePounds||attempt.InputMassPounds!=unit.MassPounds
                ||attempt.RetainedMassPounds!=attempt.InputMassPounds-attempt.GangueWastePounds
                ||attempt.SourceLotId!=unit.Id||attempt.ReservationId!=MineralPreparationIds.Reservation(attempt.Id)
                ||!s.Actors.Any(x=>x.Id==attempt.WorkerId)||attempt.StartedAt>attempt.UpdatedAt||attempt.UpdatedAt>s.RuleClock
                ||attempt.Status!=MineralPreparationStatus.Complete&&unit.Status!=MiningUnitStatus.Extracted
                ||input==null||source==null||source.ParentId!=""||input.UnitId!="mass-pound"
                ||claim==null||claim.JobId!=attempt.Id||claim.LotId!=attempt.SourceLotId||claim.Amount!=attempt.InputMassPounds)
                throw new ArgumentException("Mineral preparation source or profile binding is inconsistent.");
            if(open&&(unit.ReceivedContainerId!=deposit.ReceiverId||input.Amount!=attempt.InputMassPounds
                ||claim.RemainingAmount!=claim.Amount||claim.Status!=ReservationStatus.Reserved))
                throw new ArgumentException("Open mineral preparation lost its whole-unit reservation.");
            if(complete&&claim.Status!=ReservationStatus.Released)
                throw new ArgumentException("Completed preparation did not release the input reservation before subdivision.");
            var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==attempt.Id).OrderBy(x=>x.Start).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
            if(intervals.Any(x=>x.WorkerId!=attempt.WorkerId)||intervals.Length>0&&intervals[0].Start<attempt.StartedAt)
                throw new ArgumentException("Mineral preparation labor history is inconsistent.");
            if(attempt.Status==MineralPreparationStatus.Working) {
                var active=intervals.Where(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock).ToArray();
                var booked=active.Length==1?Subtract(active[0].End,s.RuleClock):default;
                var remaining=Subtract(new RuleTime(WorkSeconds),attempt.WorkDone);
                if(active.Length!=1||active[0].WorkerId!=attempt.WorkerId||booked!=remaining)
                    throw new ArgumentException("Working mineral preparation lacks its exact remaining interval.");
            } else if(intervals.Any(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock))
                throw new ArgumentException("Inactive mineral preparation retains a live worker interval.");
            RuleTime credited=default;
            foreach(var interval in intervals) {
                if(interval.Start>=s.RuleClock)continue;
                RuleTime end=interval.End<s.RuleClock?interval.End:s.RuleClock;
                if(end>interval.Start)credited=Add(credited,Subtract(end,interval.Start));
            }
            if(credited!=attempt.WorkDone)throw new ArgumentException("Mineral preparation work credit differs from booked labor.");
            if(complete) {
                var retained=s.InventoryLots.SingleOrDefault(x=>x.LotId==attempt.RetainedLotId);
                var retainedLot=s.Work.Lots.SingleOrDefault(x=>x.Id==attempt.RetainedLotId);
                var body=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id);
                var children=s.InventoryLots.Where(x=>x.ParentId==unit.Id).ToArray();
                bool wasteExpected=attempt.GangueWastePounds>default(RuleQuantity);
                var gangue=wasteExpected?s.InventoryLots.SingleOrDefault(x=>x.LotId==attempt.GangueLotId):null;
                var gangueLot=wasteExpected?s.Work.Lots.SingleOrDefault(x=>x.Id==attempt.GangueLotId):null;
                var gangueBody=wasteExpected?s.PortableEquipment.SingleOrDefault(x=>x.Id==attempt.GangueLotId):null;
                if(attempt.UpdatedAt>s.RuleClock||unit.Status!=MiningUnitStatus.Extracted||unit.ReceivedLotId!=attempt.RetainedLotId
                    ||unit.ReceivedContainerId!=deposit.ReceiverId||input.Amount!=default||input.LocationId!=deposit.ReceiverId
                    ||retained==null||retained.ParentId!=unit.Id||retained.CreatedAmount!=attempt.RetainedMassPounds
                    ||retained.OwnerId!=source.OwnerId||retained.Nutrition!=NutritionKind.None||retained.Access!=InventoryAccess.Stowed
                    ||retainedLot==null||retainedLot.UnitId!="mass-pound"||retainedLot.LocationId!=deposit.ReceiverId
                    ||body==null||body.ProfileId!=profile.DressedItemProfileId||body.LinkedId!=attempt.RetainedLotId
                    ||body.ParentId!=deposit.ReceiverId||body.Placement!=PortablePlacement.Contained
                    ||children.Length!=(wasteExpected?2:1)||!children.Any(x=>x.LotId==attempt.RetainedLotId)
                    ||wasteExpected&&(gangue==null||gangue.ParentId!=unit.Id||gangue.CreatedAmount!=attempt.GangueWastePounds
                        ||gangue.OwnerId!=source.OwnerId||gangue.Nutrition!=NutritionKind.None||gangue.CreatedAt!=attempt.UpdatedAt
                        ||gangueLot==null||gangueLot.UnitId!="mass-pound"
                        ||gangueBody==null||gangueBody.ProfileId!=profile.GangueItemProfileId||gangueBody.LinkedId!=attempt.GangueLotId))
                    throw new ArgumentException("Completed preparation did not conserve retained mineral and measured gangue lineage.");
            } else if(unit.ReceivedLotId!=unit.Id||input.LocationId!=deposit.ReceiverId)
                throw new ArgumentException("Open preparation no longer holds the extracted unit at its receiver.");
        }
    }

    public static class MineralPreparationIds
    {
        public static string Reservation(string jobId)=>jobId+".input";
        public static string RetainedLot(string jobId)=>jobId+".retained";
        public static string GangueLot(string jobId)=>jobId+".gangue";
    }

    /// <summary>One immutable, source-bound recipe-347 body/card profile. Its fixed measurements
    /// describe the reviewed Mining Tool; this record does not grant manufacturing, proficiency
    /// or acquisition. The preparation target and optional reserve are real authored unit IDs.</summary>
    public sealed class MiningToolCandidateProfileRecord
    {
        private readonly string[] requiredMemberIds,optionalMemberIds;
        public string Id { get; }
        public string DepositId { get; }
        public string ToolItemId { get; }
        public string ToolItemProfileId { get; }
        public string StructureId { get; }
        public string StructureProfileId { get; }
        public string PreparationProfileId { get; }
        public string PreparationUnitId { get; }
        public string ReserveUnitId { get; }
        public string[] RequiredMemberIds=>requiredMemberIds.ToArray();
        public string[] OptionalMemberIds=>optionalMemberIds.ToArray();
        public const string CardId="recipe-347";
        public const int CheckBonus=2,MaximumHp=5,StructuralAc=15;
        public const int WidthInches=12,DepthInches=12,HeightInches=4;
        public const int TrayWidthInches=10,TrayDepthInches=10,TrayHeightInches=2;
        public static readonly RuleQuantity EmptyMassPounds=new RuleQuantity(3);
        public static readonly RuleQuantity TrayCapacityPounds=new RuleQuantity(5);
        public static readonly RuleQuantity TrayCapacityCubicFeet=RuleQuantity.FromFraction(1,10);

        public MiningToolCandidateProfileRecord(string id,string depositId,string toolItemId,string toolItemProfileId,
            string structureId,string structureProfileId,string preparationProfileId="",string preparationUnitId="",string reserveUnitId="")
        {
            if(!Validation.ValidId(id)||id.Length>64||!Validation.ValidId(depositId)||!Validation.ValidId(toolItemId)
                ||!Validation.ValidId(toolItemProfileId)||!Validation.ValidId(structureId)||!Validation.ValidId(structureProfileId)
                ||preparationProfileId==null||preparationProfileId!=""&&!Validation.ValidId(preparationProfileId)
                ||preparationUnitId==null||preparationUnitId!=""&&!Validation.ValidId(preparationUnitId)
                ||reserveUnitId==null||reserveUnitId!=""&&!Validation.ValidId(reserveUnitId)
                ||(preparationProfileId=="")!=(preparationUnitId=="")
                ||preparationUnitId!=""&&preparationUnitId==reserveUnitId)
                throw new ArgumentException("Invalid recipe-347 mining-tool profile.");
            Id=id;DepositId=depositId;ToolItemId=toolItemId;ToolItemProfileId=toolItemProfileId;
            StructureId=structureId;StructureProfileId=structureProfileId;PreparationProfileId=preparationProfileId;
            PreparationUnitId=preparationUnitId;ReserveUnitId=reserveUnitId;
            requiredMemberIds=new[]{id+".member.frame",id+".member.principal-mesh",id+".member.tray"};
            optionalMemberIds=new[]{id+".member.brush",id+".member.minor-fittings"};
        }

        public bool HasSameContent(MiningToolCandidateProfileRecord other)
            =>other!=null&&Id==other.Id&&DepositId==other.DepositId&&ToolItemId==other.ToolItemId
                &&ToolItemProfileId==other.ToolItemProfileId&&StructureId==other.StructureId
                &&StructureProfileId==other.StructureProfileId&&PreparationProfileId==other.PreparationProfileId
                &&PreparationUnitId==other.PreparationUnitId&&ReserveUnitId==other.ReserveUnitId;
    }

    /// <summary>Persisted condition of one actual candidate body. Missing primary members,
    /// suppression or melding disable candidate effects even while structural HP remains positive.</summary>
    public sealed class MiningToolInstanceStateRecord
    {
        private readonly string[] missingMemberIds;
        public string ProfileId { get; }
        public string ToolItemId { get; }
        public string[] MissingMemberIds=>missingMemberIds.ToArray();
        public bool Suppressed { get; }
        public bool Melded { get; }
        public MiningToolInstanceStateRecord(string profileId,string toolItemId,string[] missingMemberIds=null,
            bool suppressed=false,bool melded=false)
        {
            var missing=missingMemberIds??Array.Empty<string>();
            if(!Validation.ValidId(profileId)||!Validation.ValidId(toolItemId)||missing.Length>8
                ||missing.Any(x=>!Validation.ValidId(x))||missing.Distinct(StringComparer.Ordinal).Count()!=missing.Length)
                throw new ArgumentException("Invalid mining-tool instance state.");
            ProfileId=profileId;ToolItemId=toolItemId;this.missingMemberIds=missing.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            Suppressed=suppressed;Melded=melded;
        }
    }

    /// <summary>One candidate's persisted participation and outcome audit, linked to the existing
    /// mining attempt. Work intervals remain owned by that attempt and WorkLedger.</summary>
    public sealed class MiningToolUseRecord
    {
        public string Id { get; }
        public string MiningAttemptId { get; }
        public string ProfileId { get; }
        public string WorkerId { get; }
        public string PreparedUnitId { get; }
        public string ReservedUnitId { get; }
        public RuleTime ToolWorkDone { get; }
        public RuleTime PreparationWorkDone { get; }
        public RuleTime? PreparationCompletedAt { get; }
        public string RetainedLotId { get; }
        public string GangueLotId { get; }
        public bool CheckBonusApplied { get; }
        public string CriticalReserveAwardedUnitId { get; }
        public bool DressedBenefitAwarded { get; }

        public MiningToolUseRecord(string id,string miningAttemptId,string profileId,string workerId,string preparedUnitId,string reservedUnitId,
            RuleTime toolWorkDone,RuleTime preparationWorkDone,RuleTime? preparationCompletedAt,string retainedLotId,
            string gangueLotId,bool checkBonusApplied,string criticalReserveAwardedUnitId,bool dressedBenefitAwarded)
        {
            bool completed=preparationCompletedAt.HasValue;
            if(!Validation.ValidId(id)||!Validation.ValidId(miningAttemptId)||!Validation.ValidId(profileId)||!Validation.ValidId(workerId)
                ||preparedUnitId==null||preparedUnitId!=""&&!Validation.ValidId(preparedUnitId)
                ||reservedUnitId==null||reservedUnitId!=""&&!Validation.ValidId(reservedUnitId)
                ||reservedUnitId!=""&&reservedUnitId==preparedUnitId
                ||toolWorkDone<default(RuleTime)||preparationWorkDone<default(RuleTime)
                ||preparationWorkDone>new RuleTime(MineralPreparationValidation.WorkSeconds)
                ||preparationCompletedAt.HasValue&&(preparationCompletedAt.Value<default(RuleTime))
                ||retainedLotId==null||retainedLotId!=""&&!Validation.ValidId(retainedLotId)
                ||gangueLotId==null||gangueLotId!=""&&!Validation.ValidId(gangueLotId)
                ||completed&&preparationWorkDone!=new RuleTime(MineralPreparationValidation.WorkSeconds)
                ||completed&&retainedLotId==""
                ||!completed&&(retainedLotId!=""||gangueLotId!="")
                ||(criticalReserveAwardedUnitId==null||criticalReserveAwardedUnitId!=""&&!Validation.ValidId(criticalReserveAwardedUnitId))
                ||dressedBenefitAwarded&&!completed
                ||checkBonusApplied&&(toolWorkDone<new RuleTime(60))
                ||criticalReserveAwardedUnitId!=""&&(toolWorkDone<new RuleTime(60))
                ||dressedBenefitAwarded&&(toolWorkDone<new RuleTime(60)))
                throw new ArgumentException("Invalid mining-tool use record.");
            Id=id;MiningAttemptId=miningAttemptId;ProfileId=profileId;WorkerId=workerId;PreparedUnitId=preparedUnitId;ReservedUnitId=reservedUnitId;
            ToolWorkDone=toolWorkDone;PreparationWorkDone=preparationWorkDone;PreparationCompletedAt=preparationCompletedAt;
            RetainedLotId=retainedLotId;GangueLotId=gangueLotId;CheckBonusApplied=checkBonusApplied;
            CriticalReserveAwardedUnitId=criticalReserveAwardedUnitId;DressedBenefitAwarded=dressedBenefitAwarded;
        }

        public MiningToolUseRecord WithWork(RuleTime toolWork,RuleTime preparationWork)
            =>new MiningToolUseRecord(Id,MiningAttemptId,ProfileId,WorkerId,PreparedUnitId,ReservedUnitId,toolWork,preparationWork,
                PreparationCompletedAt,RetainedLotId,GangueLotId,CheckBonusApplied,CriticalReserveAwardedUnitId,DressedBenefitAwarded);
        public MiningToolUseRecord CompletePreparation(RuleTime at,string retainedLotId,string gangueLotId)
            =>new MiningToolUseRecord(Id,MiningAttemptId,ProfileId,WorkerId,PreparedUnitId,ReservedUnitId,ToolWorkDone,
                new RuleTime(MineralPreparationValidation.WorkSeconds),at,retainedLotId,gangueLotId,
                CheckBonusApplied,CriticalReserveAwardedUnitId,DressedBenefitAwarded);
        public MiningToolUseRecord WithOutcome(bool checkBonusApplied,string reserveUnitId,bool dressedBenefitAwarded)
            =>new MiningToolUseRecord(Id,MiningAttemptId,ProfileId,WorkerId,PreparedUnitId,ReservedUnitId,ToolWorkDone,PreparationWorkDone,
                PreparationCompletedAt,RetainedLotId,GangueLotId,checkBonusApplied,reserveUnitId,dressedBenefitAwarded);
    }

    /// <summary>Pure physical qualification shared by command assessment, result resolution and
    /// snapshot validation. Only the reviewed on-site Mining Tool body is admitted here.</summary>
    public static class MiningToolCandidateRules
    {
        public static bool PhysicallyEligible(Snapshot s,MiningToolCandidateProfileRecord profile,
            MiningToolInstanceStateRecord instance,string actor,string[] selectedUnitIds)
        {
            if(s==null||profile==null||instance==null||selectedUnitIds==null||instance.ProfileId!=profile.Id
                ||instance.ToolItemId!=profile.ToolItemId||instance.Suppressed||instance.Melded
                ||profile.ToolItemId==""||selectedUnitIds.Length==0)return false;
            var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==profile.DepositId);
            var worker=s.Actors.SingleOrDefault(x=>x.Id==actor);
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==profile.ToolItemId);
            var structure=s.Structures.SingleOrDefault(x=>x.Id==profile.StructureId);
            var surface=deposit==null?null:s.Structures.SingleOrDefault(x=>x.Id==deposit.WorkSurfaceId);
            var receiver=deposit==null?null:s.PortableEquipment.SingleOrDefault(x=>x.Id==deposit.ReceiverId);
            var recipeTool=s.SchemaVersion>=Snapshot.Recipe347Schema
                ?s.Recipe347MiningToolProfiles.SingleOrDefault(x=>x.ItemId==profile.ToolItemId&&x.StructureId==profile.StructureId):null;
            bool recipeBody=recipeTool!=null&&structure!=null&&recipeTool.MaximumHp==structure.MaximumHp;
            bool validMass=recipeBody
                ?item!=null&&item.MassBasis==PortableMassBasis.GenericPounds&&item.SourceWeightLb==new RuleQuantity(3)
                    &&!item.OperationalWeightLb.HasValue
                :item!=null&&item.MassBasis==PortableMassBasis.Fixed
                    &&item.SourceWeightLb==MiningToolCandidateProfileRecord.EmptyMassPounds
                    &&item.OperationalWeightLb==MiningToolCandidateProfileRecord.EmptyMassPounds;
            bool validStructure=recipeBody
                ?structure!=null&&structure.ProfileId==profile.StructureProfileId&&structure.MaximumHp==recipeTool.MaximumHp
                    &&structure.MassPounds==new RuleQuantity(3)
                :structure!=null&&structure.ProfileId==profile.StructureProfileId
                    &&structure.MaximumHp==MiningToolCandidateProfileRecord.MaximumHp
                    &&structure.MassPounds==MiningToolCandidateProfileRecord.EmptyMassPounds;
            if(deposit==null||worker==null||item==null||structure==null||surface==null||receiver==null
                ||item.ProfileId!=profile.ToolItemProfileId
                ||item.OwnerId!=deposit.OwnerId||item.CustodianId!=deposit.OwnerId||item.Placement!=PortablePlacement.Ground
                ||item.GroundX!=deposit.SiteX||item.GroundY!=deposit.SiteY
                ||Math.Abs((long)worker.X-deposit.SiteX)+Math.Abs((long)worker.Y-deposit.SiteY)>1
                ||!validMass||structure.OwnerId!=deposit.OwnerId
                ||structure.CustodianId!=deposit.OwnerId||structure.LocationId!=deposit.SiteId
                ||!validStructure||structure.Hp<=0
                ||structure.Material!=ObjectMaterial.WoodLeather||surface.Broken||surface.LocationId!=deposit.SiteId
                ||receiver.Placement!=PortablePlacement.Ground||receiver.GroundX!=deposit.SiteX||receiver.GroundY!=deposit.SiteY
                ||!receiver.Open||!receiver.CapacityPounds.HasValue||!receiver.CapacityCubicFeet.HasValue||receiver.FitRuleId=="")return false;
            if(profile.RequiredMemberIds.Any(x=>instance.MissingMemberIds.Contains(x,StringComparer.Ordinal))
                ||instance.MissingMemberIds.Any(x=>!profile.RequiredMemberIds.Concat(profile.OptionalMemberIds).Contains(x,StringComparer.Ordinal)))return false;
            var units=selectedUnitIds.Select(id=>s.MiningUnits.SingleOrDefault(x=>x.Id==id)).ToArray();
            if(units.Any(x=>x==null)||RuleQuantity.Sum(units.Select(x=>x.MassPounds))>MiningToolCandidateProfileRecord.TrayCapacityPounds
                ||RuleQuantity.Sum(units.Select(x=>x.VolumeCubicFeet))>MiningToolCandidateProfileRecord.TrayCapacityCubicFeet)return false;
            return true;
        }

        public static bool Qualifies(Snapshot s,MiningToolCandidateProfileRecord profile,MiningToolInstanceStateRecord instance,
            MiningToolUseRecord use,string actor,string[] selectedUnitIds)
            =>use!=null&&use.ProfileId==profile?.Id&&use.WorkerId==actor&&use.ToolWorkDone>=new RuleTime(60)
                &&PhysicallyEligible(s,profile,instance,actor,selectedUnitIds.Concat(
                    use.ReservedUnitId==""?Array.Empty<string>():new[]{use.ReservedUnitId}).ToArray());
    }

    public static class MiningToolValidation
    {
        public const int MaxRecords=MiningValidation.MaxRecords;
        private static RuleTime Add(RuleTime a,RuleTime b)=>RuleTime.FromFraction(
            (System.Numerics.BigInteger)a.Numerator*b.Denominator+(System.Numerics.BigInteger)b.Numerator*a.Denominator,
            (System.Numerics.BigInteger)a.Denominator*b.Denominator);
        private static RuleTime Subtract(RuleTime a,RuleTime b)=>RuleTime.FromFraction(
            (System.Numerics.BigInteger)a.Numerator*b.Denominator-(System.Numerics.BigInteger)b.Numerator*a.Denominator,
            (System.Numerics.BigInteger)a.Denominator*b.Denominator);
        private static RuleTime WorkInStage(Snapshot s,MiningAttemptRecord attempt,RuleTime stageStart,RuleTime stageEnd)
        {
            RuleTime cursor=default,total=default;
            foreach(var interval in s.Work.WorkerIntervals.Where(x=>x.JobId==attempt.Id).OrderBy(x=>x.Start).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                if(interval.Start>=s.RuleClock)continue;
                RuleTime end=interval.End<s.RuleClock?interval.End:s.RuleClock;
                if(end<=interval.Start)continue;
                RuleTime span=Subtract(end,interval.Start),left=cursor>stageStart?cursor:stageStart;
                RuleTime right=Add(cursor,span)<stageEnd?Add(cursor,span):stageEnd;
                if(right>left)total=Add(total,Subtract(right,left));
                cursor=Add(cursor,span);
            }
            return total;
        }
        public static void Validate(Snapshot s)
        {
            if(s.MiningToolCandidateProfiles==null||s.MiningToolInstanceStates==null||s.MiningToolUses==null
                ||s.MiningToolCandidateProfiles.Length>MaxRecords||s.MiningToolInstanceStates.Length>MaxRecords||s.MiningToolUses.Length>MaxRecords
                ||s.MiningToolCandidateProfiles.Any(x=>x==null)||s.MiningToolInstanceStates.Any(x=>x==null)||s.MiningToolUses.Any(x=>x==null))
                throw new ArgumentException("Invalid mining-tool collections.");
            if(s.SchemaVersion<Snapshot.MiningToolCandidateSchema) {
                if(s.MiningToolCandidateProfiles.Length+s.MiningToolInstanceStates.Length+s.MiningToolUses.Length!=0)
                    throw new ArgumentException("Mining-tool candidates require schema49.");
                return;
            }
            if(s.MiningToolCandidateProfiles.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.MiningToolCandidateProfiles.Length
                ||s.MiningToolCandidateProfiles.Select(x=>x.DepositId).Distinct(StringComparer.Ordinal).Count()!=s.MiningToolCandidateProfiles.Length
                ||s.MiningToolInstanceStates.Select(x=>x.ProfileId).Distinct(StringComparer.Ordinal).Count()!=s.MiningToolInstanceStates.Length
                ||s.MiningToolUses.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.MiningToolUses.Length
                ||s.MiningToolUses.Select(x=>x.MiningAttemptId).Distinct(StringComparer.Ordinal).Count()!=s.MiningToolUses.Length)
                throw new ArgumentException("Duplicate mining-tool identity.");
            foreach(var profile in s.MiningToolCandidateProfiles) {
                var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==profile.DepositId)
                    ??throw new ArgumentException("Mining-tool profile references an unknown deposit.");
                var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==profile.ToolItemId);
                var structure=s.Structures.SingleOrDefault(x=>x.Id==profile.StructureId);
                var recipeTool=s.SchemaVersion>=Snapshot.Recipe347Schema
                    ?s.Recipe347MiningToolProfiles.SingleOrDefault(x=>x.ItemId==profile.ToolItemId&&x.StructureId==profile.StructureId):null;
                bool recipeBody=recipeTool!=null&&structure!=null&&recipeTool.MaximumHp==structure.MaximumHp;
                bool itemMismatch=item!=null&&(item.OwnerId!=deposit.OwnerId||item.CustodianId!=deposit.OwnerId
                    ||item.ProfileId!=profile.ToolItemProfileId
                    ||(recipeBody
                        ?item.MassBasis!=PortableMassBasis.GenericPounds||item.SourceWeightLb!=new RuleQuantity(3)
                            ||item.OperationalWeightLb.HasValue
                        :item.MassBasis!=PortableMassBasis.Fixed||item.SourceWeightLb!=MiningToolCandidateProfileRecord.EmptyMassPounds
                            ||item.OperationalWeightLb!=MiningToolCandidateProfileRecord.EmptyMassPounds));
                bool structureMismatch=structure!=null&&(structure.OwnerId!=deposit.OwnerId||structure.CustodianId!=deposit.OwnerId
                    ||structure.ProfileId!=profile.StructureProfileId
                    ||(recipeBody
                        ?structure.MaximumHp!=recipeTool.MaximumHp||structure.MassPounds!=new RuleQuantity(3)
                        :structure.MaximumHp!=MiningToolCandidateProfileRecord.MaximumHp
                            ||structure.MassPounds!=MiningToolCandidateProfileRecord.EmptyMassPounds)
                    ||structure.Material!=ObjectMaterial.WoodLeather);
                if(itemMismatch||structureMismatch)
                    throw new ArgumentException("Mining-tool physical records disagree with the reviewed body profile.");
                if(profile.ReserveUnitId!="") {
                    var reserve=s.MiningUnits.SingleOrDefault(x=>x.Id==profile.ReserveUnitId);
                    if(reserve==null||reserve.DepositId!=deposit.Id||reserve.Condition!=MiningUnitCondition.Intact
                        ||reserve.Id==profile.PreparationUnitId
                        ||!s.MiningCategories.Any(x=>x.Id==reserve.CategoryId&&x.DepositId==deposit.Id&&x.Accessible))
                        throw new ArgumentException("Mining-tool reserve is not a distinct accessible ordinary unit.");
                }
                if(profile.PreparationProfileId!="") {
                    var preparation=s.MineralPreparationProfiles.SingleOrDefault(x=>x.Id==profile.PreparationProfileId);
                    if(preparation==null||preparation.UnitId!=profile.PreparationUnitId
                        ||s.MiningUnits.Single(x=>x.Id==profile.PreparationUnitId).DepositId!=deposit.Id)
                        throw new ArgumentException("Mining-tool preparation target is not bound to its authored profile.");
                }
            }
            foreach(var instance in s.MiningToolInstanceStates) {
                var profile=s.MiningToolCandidateProfiles.SingleOrDefault(x=>x.Id==instance.ProfileId);
                if(profile==null||profile.ToolItemId!=instance.ToolItemId
                    ||instance.MissingMemberIds.Any(x=>!profile.RequiredMemberIds.Concat(profile.OptionalMemberIds).Contains(x,StringComparer.Ordinal)))
                    throw new ArgumentException("Mining-tool instance state does not match its body profile.");
            }
            foreach(var use in s.MiningToolUses)ValidateUse(s,use);
        }

        private static void ValidateUse(Snapshot s,MiningToolUseRecord use)
        {
            var attempt=s.MiningAttempts.SingleOrDefault(x=>x.Id==use.MiningAttemptId)
                ??throw new ArgumentException("Mining-tool use references an unknown extraction.");
            var profile=s.MiningToolCandidateProfiles.SingleOrDefault(x=>x.Id==use.ProfileId)
                ??throw new ArgumentException("Mining-tool use references unknown content.");
            var instance=s.MiningToolInstanceStates.SingleOrDefault(x=>x.ProfileId==profile.Id);
            if(instance==null||profile.DepositId!=attempt.DepositId||use.WorkerId!=attempt.WorkerId
                ||use.Id!=attempt.Id+".tool-use"||use.ToolWorkDone>new RuleTime(attempt.RemovalSeconds)
                ||use.PreparationWorkDone>new RuleTime(MineralPreparationValidation.WorkSeconds)
                ||use.ToolWorkDone>WorkInStage(s,attempt,new RuleTime(attempt.SetupSeconds),
                    new RuleTime(checked(attempt.SetupSeconds+attempt.RemovalSeconds)))
                ||use.PreparedUnitId!=""&&attempt.RemovalSeconds<MineralPreparationValidation.WorkSeconds
                ||use.PreparedUnitId!=""&&(use.PreparedUnitId!=profile.PreparationUnitId
                    ||!attempt.SelectedUnitIds.Contains(use.PreparedUnitId,StringComparer.Ordinal))
                ||use.ReservedUnitId!=""&&(use.ReservedUnitId!=profile.ReserveUnitId
                    ||attempt.SelectedUnitIds.Contains(use.ReservedUnitId,StringComparer.Ordinal)))
                throw new ArgumentException("Mining-tool use is not bound to its extraction or selected allocation.");
            RuleTime preparationEnd=new RuleTime(checked(attempt.SetupSeconds+attempt.RemovalSeconds));
            RuleTime preparationStart=Subtract(preparationEnd,new RuleTime(MineralPreparationValidation.WorkSeconds));
            if(use.PreparedUnitId==""&&use.PreparationWorkDone!=default
                ||use.PreparedUnitId!=""&&use.PreparationWorkDone>WorkInStage(s,attempt,preparationStart,preparationEnd))
                throw new ArgumentException("Mining-tool participation exceeds actual preparation work intervals.");
            if(use.ReservedUnitId!="") {
                var reserve=s.MiningUnits.SingleOrDefault(x=>x.Id==use.ReservedUnitId);
                var claim=s.Work.Reservations.SingleOrDefault(x=>x.Id==MiningIds.ToolReserveReservation(attempt.Id));
                bool open=attempt.Status==MiningAttemptStatus.Working||attempt.Status==MiningAttemptStatus.Paused
                    ||attempt.Status==MiningAttemptStatus.AwaitingCheck;
                if(reserve==null||reserve.DepositId!=attempt.DepositId||reserve.Condition!=MiningUnitCondition.Intact
                    ||reserve.Status!=MiningUnitStatus.Available&&!(use.CriticalReserveAwardedUnitId==reserve.Id
                        &&reserve.Status==MiningUnitStatus.Extracted)
                    ||claim==null||claim.JobId!=attempt.Id||claim.LotId!=reserve.Id||claim.Amount!=reserve.MassPounds
                    ||open&&(claim.Status!=ReservationStatus.Reserved||claim.RemainingAmount!=claim.Amount)
                    ||!open&&(claim.Status!=ReservationStatus.Released||claim.RemainingAmount!=default))
                    throw new ArgumentException("Mining-tool reserve lost its actual predeclared material claim.");
            }
            bool resolved=attempt.Status==MiningAttemptStatus.Success||attempt.Status==MiningAttemptStatus.CriticalSuccess
                ||attempt.Status==MiningAttemptStatus.Failure||attempt.Status==MiningAttemptStatus.CriticalFailure;
            // An unresolved use preserves measured work but is requalified against the tool's
            // current physical state when its check is actually resolved. Paused work may legally
            // release and relocate the recipe-produced body before that check. Only that versioned
            // recipe path may retain its completed result after later relocation; legacy schema49
            // candidate validation continues to derive qualification from its current body state.
            bool recipeProduced=s.SchemaVersion>=Snapshot.Recipe347Schema
                &&s.Recipe347MiningToolProfiles.Any(x=>x.ItemId==profile.ToolItemId);
            bool toolQualified=recipeProduced?resolved&&use.CheckBonusApplied
                :MiningToolCandidateRules.Qualifies(s,profile,instance,use,attempt.WorkerId,attempt.SelectedUnitIds);
            if(resolved&&use.CheckBonusApplied&&use.ToolWorkDone<new RuleTime(60))
                throw new ArgumentException("Mining-tool check bonus lacks the required actual participation.");
            bool expectedReserve=resolved&&attempt.Status==MiningAttemptStatus.CriticalSuccess&&toolQualified&&use.ReservedUnitId!="";
            bool successful=attempt.Status==MiningAttemptStatus.Success||attempt.Status==MiningAttemptStatus.CriticalSuccess;
            bool expectedDressed=successful&&toolQualified&&use.PreparedUnitId!=""&&use.PreparationCompletedAt.HasValue;
            if(!resolved&&(use.CheckBonusApplied||use.CriticalReserveAwardedUnitId!=""||use.DressedBenefitAwarded)
                ||resolved&&use.CheckBonusApplied!=toolQualified
                ||use.CriticalReserveAwardedUnitId!=(expectedReserve?use.ReservedUnitId:"")
                ||use.DressedBenefitAwarded!=expectedDressed)
                throw new ArgumentException("Mining-tool effect audit does not match eligibility and extraction outcome.");
            if(use.PreparationCompletedAt.HasValue)ValidateSplit(s,use,profile,attempt);
            else if(use.PreparationWorkDone==new RuleTime(MineralPreparationValidation.WorkSeconds))
                throw new ArgumentException("Completed preparation work is missing its physical split.");
            if(use.DressedBenefitAwarded&&(!use.CheckBonusApplied||attempt.Status!=MiningAttemptStatus.Success
                    &&attempt.Status!=MiningAttemptStatus.CriticalSuccess||use.PreparedUnitId==""
                    ||s.MiningUnits.Single(x=>x.Id==use.PreparedUnitId).ReceivedLotId!=use.RetainedLotId))
                throw new ArgumentException("Dressed recovery was awarded outside a successful eligible extraction.");
        }

        private static void ValidateSplit(Snapshot s,MiningToolUseRecord use,MiningToolCandidateProfileRecord profile,MiningAttemptRecord attempt)
        {
            var preparation=s.MineralPreparationProfiles.Single(x=>x.Id==profile.PreparationProfileId);
            var unit=s.MiningUnits.Single(x=>x.Id==use.PreparedUnitId);
            var deposit=s.MiningDeposits.Single(x=>x.Id==attempt.DepositId);
            var parent=s.InventoryLots.SingleOrDefault(x=>x.LotId==unit.Id);
            var source=s.Work.Lots.SingleOrDefault(x=>x.Id==unit.Id);
            var retained=s.InventoryLots.SingleOrDefault(x=>x.LotId==use.RetainedLotId);
            var retainedLot=s.Work.Lots.SingleOrDefault(x=>x.Id==use.RetainedLotId);
            var retainedItem=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id);
            var gangueWaste=preparation.GangueWastePounds;
            var retainedMass=unit.MassPounds-gangueWaste;
            var gangue=gangueWaste==default?null:s.InventoryLots.SingleOrDefault(x=>x.LotId==use.GangueLotId);
            var gangueLot=gangueWaste==default?null:s.Work.Lots.SingleOrDefault(x=>x.Id==use.GangueLotId);
            var gangueItem=gangueWaste==default?null:s.PortableEquipment.SingleOrDefault(x=>x.Id==use.GangueLotId);
            string location=use.DressedBenefitAwarded||unit.Status==MiningUnitStatus.Extracted?deposit.ReceiverId:"ground."
                +deposit.SiteX.ToString(System.Globalization.CultureInfo.InvariantCulture)+"."+deposit.SiteY.ToString(System.Globalization.CultureInfo.InvariantCulture);
            if(use.PreparedUnitId!=unit.Id||use.RetainedLotId!=use.Id+".retained"||gangueWaste!=default&&use.GangueLotId!=use.Id+".gangue"
                ||gangueWaste==default&&use.GangueLotId!=""||use.PreparationCompletedAt.Value>attempt.UpdatedAt
                ||parent==null||parent.ParentId!=""||source==null||source.Amount!=default||source.UnitId!="mass-pound"
                ||retained==null||retained.ParentId!=unit.Id||retained.CreatedAmount!=retainedMass||retained.CreatedAt!=use.PreparationCompletedAt
                ||retained.Nutrition!=NutritionKind.None||retained.Access!=(location==deposit.ReceiverId?InventoryAccess.Stowed:InventoryAccess.Ground)
                ||retainedLot==null||retainedLot.UnitId!="mass-pound"||retainedLot.Amount!=retainedMass||retainedLot.LocationId!=location
                ||retainedItem==null||retainedItem.LinkKind!=PortableLinkKind.InventoryLot||retainedItem.LinkedId!=use.RetainedLotId
                ||retainedItem.MassBasis!=PortableMassBasis.GenericPounds||retainedItem.SourceWeightLb!=retainedMass
                ||retainedItem.ProfileId!=(use.DressedBenefitAwarded?preparation.DressedItemProfileId:"TEST_ONLY.mining.raw-unit")
                ||retainedItem.ParentId!=(location==deposit.ReceiverId?deposit.ReceiverId:"")
                ||(location==deposit.ReceiverId)!=(retainedItem.Placement==PortablePlacement.Contained)
                )
                throw new ArgumentException("Mining-tool preparation did not conserve its retained material.");
            if(gangueWaste>default(RuleQuantity)&&(gangue==null||gangue.ParentId!=unit.Id||gangue.CreatedAmount!=gangueWaste
                ||gangue.CreatedAt!=use.PreparationCompletedAt||gangue.Nutrition!=NutritionKind.None
                ||gangue.Access!=InventoryAccess.Ground||gangueLot==null||gangueLot.UnitId!="mass-pound"
                ||gangueLot.Amount!=gangueWaste||gangueLot.LocationId!="ground."+deposit.SiteX.ToString(System.Globalization.CultureInfo.InvariantCulture)
                    +"."+deposit.SiteY.ToString(System.Globalization.CultureInfo.InvariantCulture)
                ||gangueItem==null||gangueItem.LinkedId!=use.GangueLotId||gangueItem.ProfileId!=preparation.GangueItemProfileId
                ||gangueItem.Placement!=PortablePlacement.Ground||gangueItem.GroundX!=deposit.SiteX||gangueItem.GroundY!=deposit.SiteY))
                throw new ArgumentException("Mining-tool preparation lost measured gangue.");
            if(unit.Status==MiningUnitStatus.Extracted&&(unit.ReceivedLotId!=use.RetainedLotId||unit.ReceivedContainerId!=deposit.ReceiverId)
                ||unit.Status!=MiningUnitStatus.Extracted&&retainedLot.LocationId!=PortableEquipmentValidation.GroundLocation(retainedItem))
                throw new ArgumentException("Mining-tool preparation output is not at its recorded disposition.");
        }
    }
}
