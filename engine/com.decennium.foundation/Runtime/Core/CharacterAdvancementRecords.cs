using System;
using System.Linq;
using System.Collections.ObjectModel;

namespace Decennium.Foundation
{
    public static class CharacterAdvancementProfileIds
    {
        public const string TestOnlySoldierLevel1="TEST_ONLY.soldier-level1";
        public const string TestOnlySoldierLevel1WithInitialCards="TEST_ONLY.soldier-level1-initial-cards";
        public const string TestOnlySoldierLevel1InitialBuild="TEST_ONLY.soldier-level1-initial-build";
    }

    public static class CharacterFeatureIds
    {
        public const string DefensivePositioning="soldier.base.defensive-positioning";
        public const string TacticalReposition="soldier.base.tactical-reposition";
        public const string Overwatch="soldier.base.overwatch";
        public const string WarningShot="soldier.base.warning-shot";
        public const string ShieldTrained="soldier.base.shield-trained";
        public const string CoveringFire="soldier.base.covering-fire";
        public const string CommandStep="soldier.arch.command-step";
        public const string TacticalAssessment="soldier.arch.tactical-assessment";
        public const string SuppressionFire="soldier.arch.suppression-fire";
        public const string DefensiveFormation="soldier.arch.defensive-formation";
    }
    public enum CharacterFeatureGrantOrigin { SelectedCard, AutomaticClassFeature, InitialClassSelection }
    public enum HitPointGainMethod { FixedAverage }

    /// <summary>Explicit map marker for a solid feature or cover that qualifies for this one passive.</summary>
    public sealed class TacticalCoverRecord
    {
        public string Id { get; }
        public int X { get; }
        public int Y { get; }
        public TacticalCoverRecord(string id,int x,int y)
        {if(!Validation.ValidId(id))throw new ArgumentException("Invalid tactical cover identity.");Id=id;X=x;Y=y;}
    }

    /// <summary>Level-gated feature resource state, kept separate from the ordinary Action/Reaction ledgers.</summary>
    public sealed class CharacterFeatureRuntimeRecord
    {
        public string ActorId { get; }
        public int LastRegularStart { get; }
        public bool BonusActionAvailable { get; }
        public int RepositionRechargeRemaining { get; }
        public int RepositionTurnOrdinal { get; }
        public long RepositionBudgetRemaining { get; }
        public int WarningShotRechargeRemaining { get; }
        public int CoveringFireRechargeRemaining { get; }
        public int TacticalAssessmentRechargeRemaining { get; }
        public int SuppressionFireRechargeRemaining { get; }
        public CharacterFeatureRuntimeRecord(string actorId,int lastRegularStart,bool bonusActionAvailable=true,int rechargeRemaining=0,
            int repositionTurnOrdinal=-1,long repositionBudgetRemaining=0,int warningShotRechargeRemaining=0,int coveringFireRechargeRemaining=0,
            int tacticalAssessmentRechargeRemaining=0,int suppressionFireRechargeRemaining=0)
        {
            if(!Validation.ValidId(actorId)||lastRegularStart< -1||rechargeRemaining<0||rechargeRemaining>2||repositionTurnOrdinal< -1
                ||repositionBudgetRemaining<0||repositionTurnOrdinal<0&&repositionBudgetRemaining!=0
                ||warningShotRechargeRemaining<0||warningShotRechargeRemaining>2||coveringFireRechargeRemaining<0||coveringFireRechargeRemaining>2
                ||tacticalAssessmentRechargeRemaining<0||tacticalAssessmentRechargeRemaining>3
                ||suppressionFireRechargeRemaining<0||suppressionFireRechargeRemaining>3)
                throw new ArgumentException("Invalid character feature runtime.");
            ActorId=actorId;LastRegularStart=lastRegularStart;BonusActionAvailable=bonusActionAvailable;RepositionRechargeRemaining=rechargeRemaining;
            RepositionTurnOrdinal=repositionTurnOrdinal;RepositionBudgetRemaining=repositionBudgetRemaining;
            WarningShotRechargeRemaining=warningShotRechargeRemaining;CoveringFireRechargeRemaining=coveringFireRechargeRemaining;
            TacticalAssessmentRechargeRemaining=tacticalAssessmentRechargeRemaining;
            SuppressionFireRechargeRemaining=suppressionFireRechargeRemaining;
        }
        public CharacterFeatureRuntimeRecord RegularStart(int ordinal,int regularStartsElapsed=1)
        {
            if(ordinal<=LastRegularStart||regularStartsElapsed<1)throw new ArgumentException("Feature regular start cannot repeat or go backward.");
            return new CharacterFeatureRuntimeRecord(ActorId,ordinal,true,Math.Max(0,RepositionRechargeRemaining-regularStartsElapsed),-1,0,
                Math.Max(0,WarningShotRechargeRemaining-regularStartsElapsed),Math.Max(0,CoveringFireRechargeRemaining-regularStartsElapsed),
                Math.Max(0,TacticalAssessmentRechargeRemaining-regularStartsElapsed),Math.Max(0,SuppressionFireRechargeRemaining-regularStartsElapsed));
        }
        public CharacterFeatureRuntimeRecord Activate(int ordinal,long budget)
        {
            if(ordinal<0||budget<1||!BonusActionAvailable||RepositionRechargeRemaining!=0)throw new ArgumentException("Tactical Reposition is unavailable.");
            return new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,false,2,ordinal,budget,WarningShotRechargeRemaining,CoveringFireRechargeRemaining,
                TacticalAssessmentRechargeRemaining,SuppressionFireRechargeRemaining);
        }
        public CharacterFeatureRuntimeRecord SpendReposition(long cost)
        {
            if(cost<0||cost>RepositionBudgetRemaining||RepositionTurnOrdinal<0)throw new ArgumentException("Invalid special movement expenditure.");
            return new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,BonusActionAvailable,RepositionRechargeRemaining,RepositionTurnOrdinal,
                RepositionBudgetRemaining-cost,WarningShotRechargeRemaining,CoveringFireRechargeRemaining,TacticalAssessmentRechargeRemaining,SuppressionFireRechargeRemaining);
        }
        public CharacterFeatureRuntimeRecord EndTacticalUse()=>new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,BonusActionAvailable,RepositionRechargeRemaining,-1,0,
            WarningShotRechargeRemaining,CoveringFireRechargeRemaining,TacticalAssessmentRechargeRemaining,SuppressionFireRechargeRemaining);
        public CharacterFeatureRuntimeRecord WithBonusActionAvailable(bool available)
            =>new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,available,RepositionRechargeRemaining,RepositionTurnOrdinal,RepositionBudgetRemaining,
                WarningShotRechargeRemaining,CoveringFireRechargeRemaining,TacticalAssessmentRechargeRemaining,SuppressionFireRechargeRemaining);
        public CharacterFeatureRuntimeRecord UseWarningShot()
        {
            if(WarningShotRechargeRemaining!=0)throw new ArgumentException("Warning Shot is recharging.");
            return new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,BonusActionAvailable,RepositionRechargeRemaining,RepositionTurnOrdinal,
                RepositionBudgetRemaining,2,CoveringFireRechargeRemaining,TacticalAssessmentRechargeRemaining,SuppressionFireRechargeRemaining);
        }
        public CharacterFeatureRuntimeRecord UseCoveringFire()
        {
            if(CoveringFireRechargeRemaining!=0)throw new ArgumentException("Covering Fire is recharging.");
            return new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,BonusActionAvailable,RepositionRechargeRemaining,RepositionTurnOrdinal,
                RepositionBudgetRemaining,WarningShotRechargeRemaining,2,TacticalAssessmentRechargeRemaining,SuppressionFireRechargeRemaining);
        }
        public CharacterFeatureRuntimeRecord UseTacticalAssessment()
        {
            if(TacticalAssessmentRechargeRemaining!=0)throw new ArgumentException("Tactical Assessment is recharging.");
            return new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,BonusActionAvailable,RepositionRechargeRemaining,RepositionTurnOrdinal,
                RepositionBudgetRemaining,WarningShotRechargeRemaining,CoveringFireRechargeRemaining,3,SuppressionFireRechargeRemaining);
        }
        public CharacterFeatureRuntimeRecord UseSuppressionFire()
        {
            if(SuppressionFireRechargeRemaining!=0)throw new ArgumentException("Suppression Fire is recharging.");
            return new CharacterFeatureRuntimeRecord(ActorId,LastRegularStart,BonusActionAvailable,RepositionRechargeRemaining,RepositionTurnOrdinal,
                RepositionBudgetRemaining,WarningShotRechargeRemaining,CoveringFireRechargeRemaining,TacticalAssessmentRechargeRemaining,3);
        }
    }

    /// <summary>Shared Bonus Action availability for one actor's current regular interval.</summary>
    public sealed class ActorBonusActionRecord
    {
        public string ActorId { get; }
        public int LastRegularStart { get; }
        public bool Available { get; }
        public ActorBonusActionRecord(string actorId,int lastRegularStart,bool available=true)
        {
            if(!Validation.ValidId(actorId)||lastRegularStart< -1)throw new ArgumentException("Invalid Bonus Action ledger.");
            ActorId=actorId;LastRegularStart=lastRegularStart;Available=available;
        }
        public ActorBonusActionRecord RegularStart(int ordinal)
        {
            if(ordinal<=LastRegularStart)throw new ArgumentException("Bonus Action regular start cannot repeat or go backward.");
            return new ActorBonusActionRecord(ActorId,ordinal,true);
        }
        public ActorBonusActionRecord Spend()
        {
            if(!Available)throw new ArgumentException("Bonus Action is unavailable.");
            return new ActorBonusActionRecord(ActorId,LastRegularStart,false);
        }
    }

    /// <summary>A host-authored entitlement tied to one actor. Consuming it is a separate command.</summary>
    public sealed class CharacterMilestoneRecord
    {
        public string MilestoneId { get; }
        public string ActorId { get; }
        public long AwardedRevision { get; }
        public long ConsumedRevision { get; }
        public CharacterMilestoneRecord(string milestoneId,string actorId,long awardedRevision,long consumedRevision=0)
        {
            if(!Validation.ValidId(milestoneId)||!Validation.ValidId(actorId)||awardedRevision<1||consumedRevision<0
                ||consumedRevision!=0&&consumedRevision<=awardedRevision)throw new ArgumentException("Invalid milestone entitlement.");
            MilestoneId=milestoneId;ActorId=actorId;AwardedRevision=awardedRevision;ConsumedRevision=consumedRevision;
        }
        public CharacterMilestoneRecord Consume(long revision)=>new CharacterMilestoneRecord(MilestoneId,ActorId,AwardedRevision,revision);
    }

    /// <summary>Per-level Hit Die availability, separate from the immutable attained-level count.</summary>
    public sealed class CharacterHitDieRecord
    {
        public string ActorId { get; }
        public int LevelOrdinal { get; }
        public string ClassName { get; }
        public int DieSize { get; }
        public bool Spent { get; }
        public CharacterHitDieRecord(string actorId,int levelOrdinal,string className,int dieSize,bool spent)
        {
            if(!Validation.ValidId(actorId)||levelOrdinal<1||levelOrdinal>20||string.IsNullOrEmpty(className)||className.Length>96
                ||className.Any(c=>c<32||c>126)||(dieSize!=6&&dieSize!=8&&dieSize!=10&&dieSize!=12))throw new ArgumentException("Invalid Hit Die record.");
            ActorId=actorId;LevelOrdinal=levelOrdinal;ClassName=className;DieSize=dieSize;Spent=spent;
        }
    }

    /// <summary>Origin-tagged feature entitlement; ownership is never inferred from class level alone.</summary>
    public sealed class CharacterFeatureGrantRecord
    {
        public string ActorId { get; }
        public string FeatureId { get; }
        public string ClassName { get; }
        public int ClassLevel { get; }
        public string MilestoneId { get; }
        public long GrantedRevision { get; }
        public CharacterFeatureGrantOrigin Origin { get; }
        public CharacterFeatureGrantRecord(string actorId,string featureId,string className,int classLevel,string milestoneId,long grantedRevision)
            :this(actorId,featureId,className,classLevel,milestoneId,grantedRevision,CharacterFeatureGrantOrigin.SelectedCard)
        { }
        public CharacterFeatureGrantRecord(string actorId,string featureId,string className,int classLevel,string milestoneId,long grantedRevision,
            CharacterFeatureGrantOrigin origin)
        {
            if(!Validation.ValidId(actorId)||!Validation.ValidId(featureId)||string.IsNullOrEmpty(className)||className.Length>96
                ||className.Any(c=>c<32||c>126)||classLevel<1||classLevel>20||!Enum.IsDefined(typeof(CharacterFeatureGrantOrigin),origin)
                ||origin==CharacterFeatureGrantOrigin.SelectedCard&&(!Validation.ValidId(milestoneId)||grantedRevision<1)
                ||origin==CharacterFeatureGrantOrigin.AutomaticClassFeature&&(milestoneId!=""||grantedRevision!=0)
                ||origin==CharacterFeatureGrantOrigin.InitialClassSelection&&(milestoneId!=""||grantedRevision!=0))
                throw new ArgumentException("Invalid feature grant.");
            ActorId=actorId;FeatureId=featureId;ClassName=className;ClassLevel=classLevel;MilestoneId=milestoneId;GrantedRevision=grantedRevision;Origin=origin;
        }
    }

    /// <summary>Immutable Level 1 class-card choices, separate from earned-level milestones.</summary>
    public sealed class CharacterInitialClassSelectionRecord
    {
        private readonly string[] selectedFeatureIds;
        public string ActorId { get; }
        public string ClassName { get; }
        public int ClassLevel { get; }
        public string SourceRevision { get; }
        public ReadOnlyCollection<string> SelectedFeatureIds { get; }
        public CharacterInitialClassSelectionRecord(string actorId,string className,int classLevel,string sourceRevision,string[] selectedFeatureIds)
        {
            var choices=selectedFeatureIds??Array.Empty<string>();
            if(!Validation.ValidId(actorId)||string.IsNullOrEmpty(className)||className.Length>96||className.Any(c=>c<32||c>126)
                ||classLevel<1||classLevel>20||!Validation.ValidId(sourceRevision)||choices.Length<1||choices.Length>16
                ||choices.Any(x=>!Validation.ValidId(x))||choices.Distinct(StringComparer.Ordinal).Count()!=choices.Length)
                throw new ArgumentException("Invalid initial class-card selection.");
            ActorId=actorId;ClassName=className;ClassLevel=classLevel;SourceRevision=sourceRevision;
            this.selectedFeatureIds=choices.OrderBy(x=>x,StringComparer.Ordinal).ToArray();SelectedFeatureIds=Array.AsReadOnly(this.selectedFeatureIds);
        }
    }

    public static class SoldierInitialEquipmentIds
    {
        public const string ChainMail="TEST_ONLY.soldier-chain-mail";
        public const string Shield="TEST_ONLY.soldier-shield";
        public const string Dagger="TEST_ONLY.soldier-dagger";
        public const string Pack="TEST_ONLY.soldier-dungeoneer-pack";
        public const string Rations="TEST_ONLY.soldier-pack-rations";
        public const string Waterskin="TEST_ONLY.soldier-pack-waterskin";
        public const string Water="TEST_ONLY.soldier-pack-water";
        public const string Crowbar="TEST_ONLY.soldier-pack-crowbar";
        public const string Hammer="TEST_ONLY.soldier-pack-hammer";
        public const string Pitons="TEST_ONLY.soldier-pack-pitons";
        public const string Torches="TEST_ONLY.soldier-pack-torches";
        public const string Tinderbox="TEST_ONLY.soldier-pack-tinderbox";
        public const string Rope="TEST_ONLY.soldier-pack-rope";
        public const string PackFitRule="TEST_ONLY.dungeoneer-pack-fit-v1";
    }

    /// <summary>Immutable TEST_ONLY acquisition provenance for one authored Soldier level-one
    /// build. It references physical runtime records; it is not a second inventory or resource ledger.</summary>
    public sealed class CharacterInitialLoadoutRecord
    {
        private readonly string[] selectedSkillIds;
        private readonly string[] savingThrowProficiencyIds;
        public string ActorId { get; }
        public string SourceRevision { get; }
        public int OptionalPointBuySpent { get; }
        public string SelectionProfileId { get; }
        public string ChainMailId { get; }
        public string ShieldId { get; }
        public string DaggerId { get; }
        public string PackId { get; }
        public string CrossbowId { get; }
        public string AmmunitionLotId { get; }
        public string RationsId { get; }
        public string WaterskinId { get; }
        public string WaterId { get; }
        public int InitialPackGroundX { get; }
        public int InitialPackGroundY { get; }
        public ReadOnlyCollection<string> SelectedSkillIds { get; }
        public ReadOnlyCollection<string> SavingThrowProficiencyIds { get; }
        public CharacterInitialLoadoutRecord(string actorId,string sourceRevision,int optionalPointBuySpent,string selectionProfileId,
            string[] selectedSkillIds,string[] savingThrowProficiencyIds,string chainMailId,string shieldId,string daggerId,string packId,
            string crossbowId,string ammunitionLotId,string rationsId,string waterskinId,string waterId,int initialPackGroundX,int initialPackGroundY)
        {
            var skills=selectedSkillIds??Array.Empty<string>();var saves=savingThrowProficiencyIds??Array.Empty<string>();
            if(!Validation.ValidId(actorId)||!Validation.ValidId(sourceRevision)||optionalPointBuySpent<0||optionalPointBuySpent>27
                ||!Validation.ValidId(selectionProfileId)||skills.Length!=2||skills.Any(x=>!Validation.ValidId(x))
                ||skills.Distinct(StringComparer.Ordinal).Count()!=skills.Length||saves.Length!=2||saves.Any(x=>!Validation.ValidId(x))
                ||saves.Distinct(StringComparer.Ordinal).Count()!=saves.Length||!Validation.ValidId(chainMailId)||!Validation.ValidId(shieldId)
                ||!Validation.ValidId(daggerId)||!Validation.ValidId(packId)||!Validation.ValidId(crossbowId)||!Validation.ValidId(ammunitionLotId)
                ||!Validation.ValidId(rationsId)||!Validation.ValidId(waterskinId)||!Validation.ValidId(waterId)
                ||initialPackGroundX<0||initialPackGroundY<0)
                throw new ArgumentException("Invalid initial character loadout provenance.");
            ActorId=actorId;SourceRevision=sourceRevision;OptionalPointBuySpent=optionalPointBuySpent;SelectionProfileId=selectionProfileId;
            this.selectedSkillIds=skills.OrderBy(x=>x,StringComparer.Ordinal).ToArray();SelectedSkillIds=Array.AsReadOnly(this.selectedSkillIds);
            this.savingThrowProficiencyIds=saves.OrderBy(x=>x,StringComparer.Ordinal).ToArray();SavingThrowProficiencyIds=Array.AsReadOnly(this.savingThrowProficiencyIds);
            ChainMailId=chainMailId;ShieldId=shieldId;DaggerId=daggerId;PackId=packId;CrossbowId=crossbowId;AmmunitionLotId=ammunitionLotId;
            RationsId=rationsId;WaterskinId=waterskinId;WaterId=waterId;InitialPackGroundX=initialPackGroundX;InitialPackGroundY=initialPackGroundY;
        }
    }

    /// <summary>Whether a Soldier with Shield Trained has traveled since its current regular start.</summary>
    public sealed class ShieldStationarityRecord
    {
        public string ActorId { get; }
        public int LastRegularStart { get; }
        public bool MovedSinceRegularStart { get; }
        public ShieldStationarityRecord(string actorId,int lastRegularStart,bool movedSinceRegularStart)
        {
            if(!Validation.ValidId(actorId)||lastRegularStart< -1||lastRegularStart<0&&movedSinceRegularStart)
                throw new ArgumentException("Invalid shield stationarity record.");
            ActorId=actorId;LastRegularStart=lastRegularStart;MovedSinceRegularStart=movedSinceRegularStart;
        }
        public ShieldStationarityRecord RegularStart(int ordinal)
        {
            if(ordinal<=LastRegularStart)throw new ArgumentException("Shield stationarity start cannot repeat or go backward.");
            return new ShieldStationarityRecord(ActorId,ordinal,false);
        }
        public ShieldStationarityRecord MarkMoved()=>MovedSinceRegularStart?this:new ShieldStationarityRecord(ActorId,LastRegularStart,true);
    }

    /// <summary>Auditable, replay-derived result for a single earned level.</summary>
    public sealed class CharacterAdvancementRecord
    {
        private readonly string[] selectedFeatureIds;
        private readonly CharacterAbility[] asiAbilityIncreases;
        private readonly int[] abilityScoresBefore;
        private readonly int[] abilityScoresAfter;
        public string ActorId { get; }
        public string MilestoneId { get; }
        public long Revision { get; }
        public int PreviousTotalLevel { get; }
        public int NewTotalLevel { get; }
        public string ClassName { get; }
        public int ClassLevel { get; }
        public int BaseHpGain { get; }
        public HitPointGainMethod HitPointMethod { get; }
        public long MaximumHpBefore { get; }
        public long MaximumHpAfter { get; }
        public long CurrentHpBefore { get; }
        public long CurrentHpAfter { get; }
        public string FeatureOne { get; }
        public string FeatureTwo { get; }
        public ReadOnlyCollection<string> SelectedFeatureIds { get; }
        public ReadOnlyCollection<CharacterAbility> AsiAbilityIncreases { get; }
        public ReadOnlyCollection<int> AbilityScoresBefore { get; }
        public ReadOnlyCollection<int> AbilityScoresAfter { get; }
        public CharacterAdvancementRecord(string actorId,string milestoneId,long revision,int previousTotalLevel,int newTotalLevel,
            string className,int classLevel,int baseHpGain,HitPointGainMethod method,long maximumBefore,long maximumAfter,
            long currentBefore,long currentAfter,string featureOne,string featureTwo)
            :this(actorId,milestoneId,revision,previousTotalLevel,newTotalLevel,className,classLevel,baseHpGain,method,maximumBefore,
                maximumAfter,currentBefore,currentAfter,new[]{featureOne,featureTwo},true,Array.Empty<CharacterAbility>(),
                Array.Empty<int>(),Array.Empty<int>())
        { }
        public CharacterAdvancementRecord(string actorId,string milestoneId,long revision,int previousTotalLevel,int newTotalLevel,
            string className,int classLevel,int baseHpGain,HitPointGainMethod method,long maximumBefore,long maximumAfter,
            long currentBefore,long currentAfter,string[] selectedFeatures)
            :this(actorId,milestoneId,revision,previousTotalLevel,newTotalLevel,className,classLevel,baseHpGain,method,maximumBefore,
                maximumAfter,currentBefore,currentAfter,selectedFeatures,false,Array.Empty<CharacterAbility>(),
                Array.Empty<int>(),Array.Empty<int>())
        { }
        public CharacterAdvancementRecord(string actorId,string milestoneId,long revision,int previousTotalLevel,int newTotalLevel,
            string className,int classLevel,int baseHpGain,HitPointGainMethod method,long maximumBefore,long maximumAfter,
            long currentBefore,long currentAfter,string[] selectedFeatures,CharacterAbility[] asiIncreases,
            int[] scoresBefore,int[] scoresAfter)
            :this(actorId,milestoneId,revision,previousTotalLevel,newTotalLevel,className,classLevel,baseHpGain,method,maximumBefore,
                maximumAfter,currentBefore,currentAfter,selectedFeatures,false,asiIncreases,scoresBefore,scoresAfter)
        { }
        private CharacterAdvancementRecord(string actorId,string milestoneId,long revision,int previousTotalLevel,int newTotalLevel,
            string className,int classLevel,int baseHpGain,HitPointGainMethod method,long maximumBefore,long maximumAfter,
            long currentBefore,long currentAfter,string[] selectedFeatures,bool legacyPair,CharacterAbility[] asiIncreases,
            int[] scoresBefore,int[] scoresAfter)
        {
            var asi=asiIncreases??Array.Empty<CharacterAbility>();
            var before= scoresBefore??Array.Empty<int>();var after=scoresAfter??Array.Empty<int>();
            if(!Validation.ValidId(actorId)||!Validation.ValidId(milestoneId)||revision<1||previousTotalLevel<1||newTotalLevel!=previousTotalLevel+1
                ||string.IsNullOrEmpty(className)||className.Length>96||className.Any(c=>c<32||c>126)||classLevel<1||classLevel>20
                ||baseHpGain<1||!Enum.IsDefined(typeof(HitPointGainMethod),method)||maximumBefore<1||maximumAfter<maximumBefore
                ||currentBefore<0||currentBefore>maximumBefore||currentAfter<0||currentAfter>maximumAfter||selectedFeatures==null
                ||legacyPair&&selectedFeatures.Length!=2||selectedFeatures.Length>4||selectedFeatures.Any(x=>!Validation.ValidId(x))
                ||selectedFeatures.Distinct(StringComparer.Ordinal).Count()!=selectedFeatures.Length
                ||asi.Length!=0&&asi.Length!=2||asi.Any(x=>!Enum.IsDefined(typeof(CharacterAbility),x))
                ||asi.Length==0&&(before.Length!=0||after.Length!=0)
                ||asi.Length==2&&(before.Length!=6||after.Length!=6||before.Any(x=>x<1)||after.Any(x=>x<1)))
                throw new ArgumentException("Invalid advancement result.");
            selectedFeatureIds=legacyPair?selectedFeatures.ToArray():selectedFeatures.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            asiAbilityIncreases=asi.ToArray();abilityScoresBefore=before.ToArray();abilityScoresAfter=after.ToArray();
            if(asi.Length==2) {
                var expected=before.ToArray();
                foreach(var ability in asi)expected[(int)ability]=checked(expected[(int)ability]+1);
                if(!expected.SequenceEqual(after)||asi.Any(x=>after[(int)x]>20))throw new ArgumentException("Invalid permanent ability-score increase audit.");
            }
            ActorId=actorId;MilestoneId=milestoneId;Revision=revision;PreviousTotalLevel=previousTotalLevel;NewTotalLevel=newTotalLevel;
            ClassName=className;ClassLevel=classLevel;BaseHpGain=baseHpGain;HitPointMethod=method;MaximumHpBefore=maximumBefore;
            MaximumHpAfter=maximumAfter;CurrentHpBefore=currentBefore;CurrentHpAfter=currentAfter;
            FeatureOne=selectedFeatureIds.Length>0?selectedFeatureIds[0]:"";FeatureTwo=selectedFeatureIds.Length>1?selectedFeatureIds[1]:"";
            SelectedFeatureIds=Array.AsReadOnly(selectedFeatureIds);
            AsiAbilityIncreases=Array.AsReadOnly(asiAbilityIncreases);AbilityScoresBefore=Array.AsReadOnly(abilityScoresBefore);
            AbilityScoresAfter=Array.AsReadOnly(abilityScoresAfter);
        }
    }

    /// <summary>Optional command payload. Empty fields are representable so the policy can reject an incomplete selection atomically.</summary>
    public sealed class CharacterAdvancementRequest
    {
        private readonly string[] featureIds;
        private readonly CharacterAbility[] asiAbilityIncreases;
        public ReadOnlyCollection<string> FeatureIds { get; }
        public bool UsesLegacyPairReceipt { get; }
        public ReadOnlyCollection<CharacterAbility> AsiAbilityIncreases { get; }
        public string FeatId { get; }
        public string FeatureOne { get; }
        public string FeatureTwo { get; }
        public CharacterAdvancementRequest(string featureOne="",string featureTwo="")
        {
            if(featureOne==null||featureTwo==null||featureOne!=""&&!Validation.ValidId(featureOne)||featureTwo!=""&&!Validation.ValidId(featureTwo))
                throw new ArgumentException("Invalid feature selection payload.");
            featureIds=new[]{featureOne,featureTwo};FeatureIds=Array.AsReadOnly(featureIds);
            asiAbilityIncreases=Array.Empty<CharacterAbility>();AsiAbilityIncreases=Array.AsReadOnly(asiAbilityIncreases);
            FeatId="";UsesLegacyPairReceipt=true;FeatureOne=featureOne;FeatureTwo=featureTwo;
        }
        public CharacterAdvancementRequest(string[] selectedFeatureIds)
        {
            if(selectedFeatureIds==null)throw new ArgumentNullException(nameof(selectedFeatureIds));
            var values=selectedFeatureIds.ToArray();
            if(values.Length>4||values.Any(x=>!Validation.ValidId(x)))throw new ArgumentException("Invalid class feature selection list.");
            featureIds=values.OrderBy(x=>x,StringComparer.Ordinal).ToArray();FeatureIds=Array.AsReadOnly(featureIds);
            asiAbilityIncreases=Array.Empty<CharacterAbility>();AsiAbilityIncreases=Array.AsReadOnly(asiAbilityIncreases);FeatId="";
            UsesLegacyPairReceipt=false;FeatureOne=featureIds.Length>0?featureIds[0]:"";FeatureTwo=featureIds.Length>1?featureIds[1]:"";
        }
        public CharacterAdvancementRequest(string[] selectedFeatureIds,CharacterAbility[] abilityScoreIncreases,string featId="")
        {
            if(selectedFeatureIds==null||abilityScoreIncreases==null||featId==null||selectedFeatureIds.Length>4
                ||abilityScoreIncreases.Length>4||selectedFeatureIds.Any(x=>!Validation.ValidId(x))
                ||abilityScoreIncreases.Any(x=>!Enum.IsDefined(typeof(CharacterAbility),x))
                ||featId!=""&&!Validation.ValidId(featId))throw new ArgumentException("Invalid advancement operation request.");
            featureIds=selectedFeatureIds.OrderBy(x=>x,StringComparer.Ordinal).ToArray();FeatureIds=Array.AsReadOnly(featureIds);
            asiAbilityIncreases=abilityScoreIncreases.ToArray();AsiAbilityIncreases=Array.AsReadOnly(asiAbilityIncreases);
            FeatId=featId;UsesLegacyPairReceipt=false;FeatureOne=featureIds.Length>0?featureIds[0]:"";
            FeatureTwo=featureIds.Length>1?featureIds[1]:"";
        }
    }

    public static class CharacterAdvancementValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.CharacterMilestones==null||s.CharacterHitDice==null||s.CharacterFeatureGrants==null||s.CharacterAdvancements==null
                ||s.CharacterFeatureRuntime==null||s.TacticalCovers==null||s.BonusActions==null
                ||s.InitialClassSelections==null||s.InitialClassSelections.Length>64||s.InitialClassSelections.Any(x=>x==null)
                ||s.InitialCharacterLoadouts==null||s.InitialCharacterLoadouts.Length>64||s.InitialCharacterLoadouts.Any(x=>x==null)
                ||s.ShieldStationarity==null||s.ShieldStationarity.Length>64||s.ShieldStationarity.Any(x=>x==null)
                ||s.CharacterMilestones.Length>256||s.CharacterHitDice.Length>1280||s.CharacterFeatureGrants.Length>256||s.CharacterAdvancements.Length>128
                ||s.CharacterFeatureRuntime.Length>64||s.TacticalCovers.Length>64||s.BonusActions.Length>64
                ||s.CharacterMilestones.Any(x=>x==null)||s.CharacterHitDice.Any(x=>x==null)||s.CharacterFeatureGrants.Any(x=>x==null)||s.CharacterAdvancements.Any(x=>x==null)
                ||s.CharacterFeatureRuntime.Any(x=>x==null)||s.TacticalCovers.Any(x=>x==null)||s.BonusActions.Any(x=>x==null))
                throw new ArgumentException("Invalid advancement collections.");
            if(s.SchemaVersion<Snapshot.CharacterAdvancementSchema) {
                if(s.CharacterMilestones.Length+s.CharacterHitDice.Length+s.CharacterFeatureGrants.Length+s.CharacterAdvancements.Length+s.CharacterFeatureRuntime.Length+s.TacticalCovers.Length+s.BonusActions.Length+s.InitialClassSelections.Length+s.InitialCharacterLoadouts.Length+s.ShieldStationarity.Length!=0)
                    throw new ArgumentException("Character progression requires schema21.");
                return;
            }
            bool Actor(string id)=>s.Characters.Any(c=>c.ActorId==id);
            if(s.TacticalCovers.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.TacticalCovers.Length
                ||s.TacticalCovers.Select(x=>x.X+","+x.Y).Distinct(StringComparer.Ordinal).Count()!=s.TacticalCovers.Length
                ||s.Characters.Where(c=>c.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1
                    ||s.CharacterHitDice.Any(d=>d.ActorId==c.ActorId)||s.CharacterMilestones.Any(m=>m.ActorId==c.ActorId)
                    ||s.CharacterFeatureGrants.Any(g=>g.ActorId==c.ActorId)||s.CharacterAdvancements.Any(a=>a.ActorId==c.ActorId)
                    ||s.CharacterFeatureRuntime.Any(r=>r.ActorId==c.ActorId)||s.InitialClassSelections.Any(r=>r.ActorId==c.ActorId))
                    .Any(c=>s.CharacterHitDice.Count(d=>d.ActorId==c.ActorId)!=c.Levels.Count)
                ||s.CharacterFeatureRuntime.Any(x=>!Actor(x.ActorId)||!s.CharacterFeatureGrants.Any(g=>g.ActorId==x.ActorId&&g.FeatureId==CharacterFeatureIds.TacticalReposition
                    &&(g.Origin==CharacterFeatureGrantOrigin.SelectedCard||g.Origin==CharacterFeatureGrantOrigin.InitialClassSelection))
                    ||x.LastRegularStart>=0&&s.WorldSchedule!=null&&x.LastRegularStart!=s.WorldSchedule.LatestStart(x.ActorId,s.WorldSchedule.ProcessedSlot)
                    ||x.RepositionTurnOrdinal>=0&&(!s.InventoryCombat||s.Encounter==null||x.RepositionTurnOrdinal!=s.Encounter.TurnOrdinal)
                    ||s.SchemaVersion>=Snapshot.SharedBonusActionSchema&&s.BonusActions.SingleOrDefault(b=>b.ActorId==x.ActorId)?.Available!=x.BonusActionAvailable)
                ||s.CharacterFeatureRuntime.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Count()!=s.CharacterFeatureRuntime.Length
                ||s.CharacterMilestones.Any(m=>!Actor(m.ActorId)||m.AwardedRevision>s.Revision||m.ConsumedRevision>s.Revision)
                ||s.CharacterMilestones.Select(m=>m.ActorId+"|"+m.MilestoneId).Distinct(StringComparer.Ordinal).Count()!=s.CharacterMilestones.Length
                ||s.CharacterHitDice.Any(d=>!Actor(d.ActorId)||d.LevelOrdinal>s.Characters.Single(c=>c.ActorId==d.ActorId).Levels.Count
                    ||d.ClassName!=s.Characters.Single(c=>c.ActorId==d.ActorId).Levels[d.LevelOrdinal-1].ClassName)
                ||s.CharacterHitDice.Select(d=>d.ActorId+"|"+d.LevelOrdinal).Distinct(StringComparer.Ordinal).Count()!=s.CharacterHitDice.Length
                ||s.CharacterFeatureGrants.Any(g=>!Actor(g.ActorId)||g.GrantedRevision>s.Revision
                    ||g.Origin==CharacterFeatureGrantOrigin.SelectedCard&&(!s.CharacterMilestones.Any(m=>m.ActorId==g.ActorId&&m.MilestoneId==g.MilestoneId&&m.ConsumedRevision==g.GrantedRevision)
                        ||g.ClassName!="Soldier"||!ValidSelectedGrant(s,g)
                        ||s.SchemaVersion>=Snapshot.CharacterAdvancementHistorySchema&&!s.CharacterAdvancements.Any(a=>a.ActorId==g.ActorId
                            &&a.Revision==g.GrantedRevision&&a.ClassName==g.ClassName&&a.ClassLevel==g.ClassLevel&&a.SelectedFeatureIds.Contains(g.FeatureId))
                        ||g.ClassLevel> s.Characters.Single(c=>c.ActorId==g.ActorId).Levels.Count(x=>x.ClassName==g.ClassName))
                    ||g.Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature&&(s.SchemaVersion<Snapshot.SharedBonusActionSchema||g.FeatureId!=CharacterFeatureIds.Overwatch
                        ||g.ClassName!="Soldier"||g.ClassLevel!=1||g.MilestoneId!=""||g.GrantedRevision!=0
                        ||(s.Characters.Single(c=>c.ActorId==g.ActorId).ProfileId!=CharacterAdvancementProfileIds.TestOnlySoldierLevel1
                            &&s.Characters.Single(c=>c.ActorId==g.ActorId).ProfileId!=CharacterAdvancementProfileIds.TestOnlySoldierLevel1WithInitialCards
                            &&s.Characters.Single(c=>c.ActorId==g.ActorId).ProfileId!=CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild))
                    ||g.ClassLevel>s.Characters.Single(c=>c.ActorId==g.ActorId).Levels.Count(x=>x.ClassName==g.ClassName))
                ||s.CharacterFeatureGrants.Select(g=>g.ActorId+"|"+g.FeatureId+"|"+(int)g.Origin).Distinct(StringComparer.Ordinal).Count()!=s.CharacterFeatureGrants.Length
                ||s.CharacterAdvancements.Any(a=>!Actor(a.ActorId)||a.Revision>s.Revision||!s.CharacterMilestones.Any(m=>m.ActorId==a.ActorId&&m.MilestoneId==a.MilestoneId&&m.ConsumedRevision==a.Revision)
                    ||!ValidAdvancementResult(s,a)
                    ||s.SchemaVersion<Snapshot.CharacterAdvancementHistorySchema&&a.NewTotalLevel!=s.Characters.Single(c=>c.ActorId==a.ActorId).Levels.Count
                    ||a.SelectedFeatureIds.Any(feature=>!s.CharacterFeatureGrants.Any(g=>g.ActorId==a.ActorId&&g.FeatureId==feature
                        &&g.Origin==CharacterFeatureGrantOrigin.SelectedCard&&g.ClassName==a.ClassName&&g.ClassLevel==a.ClassLevel&&g.GrantedRevision==a.Revision)))
                ||s.SchemaVersion>=Snapshot.CharacterAdvancementHistorySchema&&!ValidAdvancementHistory(s)
                ||s.CharacterAdvancements.Select(a=>a.ActorId+"|"+a.MilestoneId).Distinct(StringComparer.Ordinal).Count()!=s.CharacterAdvancements.Length
                ||s.CharacterMilestones.Any(m=>(m.ConsumedRevision!=0)!=s.CharacterAdvancements.Any(a=>a.ActorId==m.ActorId&&a.MilestoneId==m.MilestoneId)))
                throw new ArgumentException("Invalid advancement references or ledgers.");
            ValidateInitialClassSelections(s);
            ValidateInitialCharacterLoadouts(s);
            foreach(var actor in s.CharacterHitDice.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal)) {
                var dice=s.CharacterHitDice.Where(x=>x.ActorId==actor).OrderBy(x=>x.LevelOrdinal).ToArray();
                if(dice.Length!=s.Characters.Single(x=>x.ActorId==actor).Levels.Count
                    ||!dice.Select(x=>x.LevelOrdinal).SequenceEqual(Enumerable.Range(1,dice.Length)))throw new ArgumentException("Hit Dice must cover attained levels in order.");
            }
            if(s.SchemaVersion<Snapshot.SharedBonusActionSchema) {
                if(s.BonusActions.Length!=0)throw new ArgumentException("Shared Bonus Action ledger requires schema24.");
            } else {
                if(s.WorldSchedule==null||s.BonusActions.Length!=s.WorldSchedule.Order.Count
                    ||s.BonusActions.Any(b=>!Actor(b.ActorId)||!s.WorldSchedule.Order.Contains(b.ActorId)
                        ||b.LastRegularStart!=s.WorldIntervals.Single(x=>x.ActorId==b.ActorId).LastStart)
                    ||s.BonusActions.Select(b=>b.ActorId).Distinct(StringComparer.Ordinal).Count()!=s.BonusActions.Length)
                    throw new ArgumentException("Shared Bonus Action ledger must cover each calendar actor at the current regular start.");
                foreach(var soldier in s.Characters.Where(c=>c.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1
                    ||c.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1WithInitialCards
                    ||c.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild))
                    if(s.CharacterFeatureGrants.Count(g=>g.ActorId==soldier.ActorId&&g.FeatureId==CharacterFeatureIds.Overwatch
                        &&g.Origin==CharacterFeatureGrantOrigin.AutomaticClassFeature)!=1)
                        throw new ArgumentException("The schema24 Soldier fixture requires one automatic Overwatch entitlement, outside card selections.");
            }
        }

        private static bool ValidSelectedGrant(Snapshot s,CharacterFeatureGrantRecord grant)
        {
            if(grant.FeatureId==CharacterFeatureIds.Overwatch)
                return grant.ClassLevel==1&&s.SchemaVersion>=Snapshot.SharedBonusActionSchema;
            if(grant.ClassLevel==2)
                return grant.FeatureId==CharacterFeatureIds.DefensivePositioning||grant.FeatureId==CharacterFeatureIds.TacticalReposition;
            if(grant.ClassLevel==3&&s.SchemaVersion>=Snapshot.CommandStepSchema)
                return grant.FeatureId==CharacterFeatureIds.CommandStep||grant.FeatureId==CharacterFeatureIds.TacticalAssessment
                    ||s.SchemaVersion>=Snapshot.SuppressionFireSchema&&grant.FeatureId==CharacterFeatureIds.SuppressionFire
                    ||s.SchemaVersion>=Snapshot.DefensiveFormationSchema&&grant.FeatureId==CharacterFeatureIds.DefensiveFormation;
            if(grant.ClassLevel==4&&s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema)
                return grant.FeatureId==CharacterFeatureIds.DefensiveFormation;
            return false;
        }

        private static bool ValidAdvancementResult(Snapshot s,CharacterAdvancementRecord advancement)
        {
            if(advancement.ClassName!="Soldier"||advancement.BaseHpGain!=6||advancement.HitPointMethod!=HitPointGainMethod.FixedAverage)
                return false;
            if(s.SchemaVersion<Snapshot.CharacterAdvancementHistorySchema)
                return advancement.PreviousTotalLevel==1&&advancement.NewTotalLevel==2&&advancement.ClassLevel==2
                    &&advancement.MaximumHpBefore==10&&advancement.MaximumHpAfter==16
                    &&advancement.FeatureOne==CharacterFeatureIds.DefensivePositioning&&advancement.FeatureTwo==CharacterFeatureIds.TacticalReposition;
            if(s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema
                &&s.CharacterAdvancements.Any(x=>x.ActorId==advancement.ActorId&&(x.ClassLevel>=4||x.AsiAbilityIncreases.Count!=0))) {
                if(advancement.NewTotalLevel!=advancement.PreviousTotalLevel+1||advancement.ClassLevel!=advancement.NewTotalLevel
                    ||advancement.NewTotalLevel>s.Characters.Single(c=>c.ActorId==advancement.ActorId).Levels.Count
                    ||advancement.CurrentHpBefore>advancement.MaximumHpBefore
                    ||advancement.CurrentHpAfter!=Math.Min(advancement.CurrentHpBefore,advancement.MaximumHpAfter))return false;
                var extendedSelected=advancement.SelectedFeatureIds;
                if(advancement.ClassLevel==2)return advancement.AsiAbilityIncreases.Count==0
                    &&extendedSelected.SequenceEqual(new[]{CharacterFeatureIds.DefensivePositioning,CharacterFeatureIds.TacticalReposition});
                if(advancement.ClassLevel==3)return advancement.AsiAbilityIncreases.Count==0&&s.SchemaVersion>=Snapshot.CommandStepSchema&&(
                    extendedSelected.SequenceEqual(new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.TacticalAssessment})
                    ||s.SchemaVersion>=Snapshot.SuppressionFireSchema
                        &&extendedSelected.SequenceEqual(new[]{CharacterFeatureIds.SuppressionFire,CharacterFeatureIds.TacticalAssessment})
                    ||s.SchemaVersion>=Snapshot.DefensiveFormationSchema
                        &&extendedSelected.SequenceEqual(new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.DefensiveFormation}));
                return advancement.ClassLevel==4&&extendedSelected.SequenceEqual(new[]{CharacterFeatureIds.DefensiveFormation})
                    &&advancement.AsiAbilityIncreases.Count==2&&advancement.AbilityScoresBefore.Count==6
                    &&advancement.AbilityScoresAfter.Count==6;
            }
            var actor=s.Characters.Single(c=>c.ActorId==advancement.ActorId);
            bool supportedProfile=actor.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1
                ||s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema&&actor.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild;
            if(!supportedProfile||actor.Abilities[2]!=10||actor.Levels[0].BaseHp!=10
                ||advancement.NewTotalLevel!=advancement.PreviousTotalLevel+1||advancement.ClassLevel!=advancement.NewTotalLevel
                ||advancement.NewTotalLevel>actor.Levels.Count||actor.Levels[advancement.NewTotalLevel-1].ClassName!="Soldier"
                ||actor.Levels[advancement.NewTotalLevel-1].BaseHp!=advancement.BaseHpGain
                ||advancement.MaximumHpBefore!=10L+6L*(advancement.PreviousTotalLevel-1)
                ||advancement.MaximumHpAfter!=10L+6L*(advancement.NewTotalLevel-1)
                ||advancement.CurrentHpBefore>advancement.MaximumHpBefore
                ||advancement.CurrentHpAfter!=Math.Min(advancement.CurrentHpBefore,advancement.MaximumHpAfter)
                ||advancement.SelectedFeatureIds.Count!=2
                ||!advancement.SelectedFeatureIds.SequenceEqual(new[]{advancement.FeatureOne,advancement.FeatureTwo}))return false;
            var selected=advancement.SelectedFeatureIds;
            if(advancement.ClassLevel==2)
                return selected.SequenceEqual(new[]{CharacterFeatureIds.DefensivePositioning,CharacterFeatureIds.TacticalReposition});
            if(advancement.ClassLevel==3)
                return s.SchemaVersion>=Snapshot.CommandStepSchema&&(
                    selected.SequenceEqual(new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.TacticalAssessment})
                    ||s.SchemaVersion>=Snapshot.SuppressionFireSchema
                        &&selected.SequenceEqual(new[]{CharacterFeatureIds.SuppressionFire,CharacterFeatureIds.TacticalAssessment})
                    ||s.SchemaVersion>=Snapshot.DefensiveFormationSchema
                        &&selected.SequenceEqual(new[]{CharacterFeatureIds.CommandStep,CharacterFeatureIds.DefensiveFormation}));
            return false;
        }

        private static bool ValidAdvancementHistory(Snapshot s)
        {
            if(s.CharacterAdvancements.Select(x=>x.Revision).Distinct().Count()!=s.CharacterAdvancements.Length)return false;
            foreach(var actorId in s.CharacterAdvancements.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal)) {
                var actor=s.Characters.SingleOrDefault(x=>x.ActorId==actorId);
                var events=s.CharacterAdvancements.Where(x=>x.ActorId==actorId).OrderBy(x=>x.Revision).ToArray();
                if(actor==null||events.Length==0)return false;
                int total=1;
                bool supportedProfile=actor.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1
                    ||s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema&&actor.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild;
                var abilityEvents=events.Where(x=>x.AsiAbilityIncreases.Count!=0).OrderBy(x=>x.Revision).ToArray();
                if(actor.Levels.Count!=events.Length+total||!supportedProfile
                    ||actor.Levels[0].ClassName!="Soldier"||actor.Levels[0].BaseHp!=10
                    ||abilityEvents.Length==0&&actor.Abilities[2]!=10
                    ||abilityEvents.Length!=0&&!abilityEvents[abilityEvents.Length-1].AbilityScoresAfter.SequenceEqual(actor.Abilities))return false;
                int[] scores={10,10,10,10,10,10};
                var classLevels=actor.Levels.GroupBy(x=>x.ClassName,StringComparer.Ordinal)
                    .ToDictionary(g=>g.Key,g=>g.Count(),StringComparer.Ordinal);
                foreach(var entry in events.GroupBy(x=>x.ClassName,StringComparer.Ordinal)) {
                    if(!classLevels.ContainsKey(entry.Key))return false;
                    classLevels[entry.Key]-=entry.Count();
                    if(classLevels[entry.Key]<0)return false;
                }
                foreach(var advancement in events) {
                    if(advancement.PreviousTotalLevel!=total||advancement.NewTotalLevel!=total+1
                        ||advancement.NewTotalLevel>actor.Levels.Count
                        ||actor.Levels[advancement.NewTotalLevel-1].ClassName!=advancement.ClassName
                        ||!classLevels.ContainsKey(advancement.ClassName)
                        ||advancement.ClassLevel!=classLevels[advancement.ClassName]+1)return false;
                    if(advancement.AsiAbilityIncreases.Count!=0) {
                        if(!advancement.AbilityScoresBefore.SequenceEqual(scores))return false;
                        var after=scores.ToArray();
                        foreach(var ability in advancement.AsiAbilityIncreases)after[(int)ability]++;
                        if(!after.SequenceEqual(advancement.AbilityScoresAfter))return false;
                        scores=after;
                    } else if(advancement.AbilityScoresBefore.Count!=0||advancement.AbilityScoresAfter.Count!=0)return false;
                    total++;
                    classLevels[advancement.ClassName]++;
                }
                if(total!=actor.Levels.Count||!scores.SequenceEqual(actor.Abilities))return false;
            }
            return true;
        }

        private static void ValidateInitialClassSelections(Snapshot s)
        {
            const string sourceRevision="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
            var valid= new[]{CharacterFeatureIds.WarningShot,CharacterFeatureIds.TacticalReposition,CharacterFeatureIds.ShieldTrained,CharacterFeatureIds.CoveringFire};
            var selections=s.InitialClassSelections;
            var selectedProfiles=s.Characters.Where(c=>c.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1WithInitialCards
                ||s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema&&c.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild).ToArray();
            if(s.SchemaVersion<Snapshot.SoldierInitialLoadoutSchema) {
                if(selections.Length!=0||s.CharacterFeatureGrants.Any(g=>g.Origin==CharacterFeatureGrantOrigin.InitialClassSelection)
                    ||selectedProfiles.Length!=0)throw new ArgumentException("Initial class selections require schema27.");
                return;
            }
            if(s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema
                &&(selectedProfiles.Any(c=>c.ProfileId!=CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild)
                    ||selectedProfiles.Length!=s.InitialCharacterLoadouts.Length))
                throw new ArgumentException("Schema28 initial class selections require their matching Soldier build record.");
            if(selections.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Count()!=selections.Length
                ||selections.Length!=selectedProfiles.Length
                ||selections.Any(selection=>{
                    var character=s.Characters.SingleOrDefault(c=>c.ActorId==selection.ActorId);
                    bool correctProfile=character!=null&&(character.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1WithInitialCards
                        ||s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema&&character.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild);
                    return !correctProfile
                        ||selection.ClassName!="Soldier"||selection.ClassLevel!=1||selection.SourceRevision!=sourceRevision
                        ||character.Levels.Count<1||character.Levels[0].ClassName!="Soldier"
                        ||!s.CharacterFeatureRuntime.Any(runtime=>runtime.ActorId==selection.ActorId)
                        ||!selection.SelectedFeatureIds.OrderBy(x=>x,StringComparer.Ordinal).SequenceEqual(valid.OrderBy(x=>x,StringComparer.Ordinal),StringComparer.Ordinal)
                        ||valid.Any(feature=>s.CharacterFeatureGrants.Count(g=>g.ActorId==selection.ActorId&&g.FeatureId==feature
                            &&g.ClassName=="Soldier"&&g.ClassLevel==1&&g.MilestoneId==""&&g.GrantedRevision==0
                            &&g.Origin==CharacterFeatureGrantOrigin.InitialClassSelection)!=1);
                })||s.CharacterFeatureGrants.Any(g=>g.Origin==CharacterFeatureGrantOrigin.InitialClassSelection
                    &&!selections.Any(selection=>selection.ActorId==g.ActorId&&selection.SelectedFeatureIds.Contains(g.FeatureId)))
                ||selectedProfiles.Any(c=>!selections.Any(selection=>selection.ActorId==c.ActorId)))
                throw new ArgumentException("Invalid source-scoped Soldier initial class-card selection.");
        }

        private static void ValidateInitialCharacterLoadouts(Snapshot s)
        {
            if(s.SchemaVersion<Snapshot.SoldierInitialBuildSchema) {
                if(s.InitialCharacterLoadouts.Length!=0||s.ShieldStationarity.Length!=0)
                    throw new ArgumentException("Initial Soldier build provenance requires schema28.");
                return;
            }
            const string sourceRevision="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
            var allowedSkills=new[]{"athletics","intimidation","perception","survival"};
            var builds=s.InitialCharacterLoadouts;
            var buildActors=builds.Select(x=>x.ActorId).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            if(buildActors.Distinct(StringComparer.Ordinal).Count()!=buildActors.Length
                ||!buildActors.SequenceEqual(s.Characters.Where(c=>c.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild)
                    .Select(c=>c.ActorId).OrderBy(x=>x,StringComparer.Ordinal))
                ||!buildActors.SequenceEqual(s.ShieldStationarity.Select(x=>x.ActorId).OrderBy(x=>x,StringComparer.Ordinal))
                ||s.ShieldStationarity.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Count()!=s.ShieldStationarity.Length)
                throw new ArgumentException("Schema28 initial loadout and stationary-shield records must cover each Soldier build actor once.");
            foreach(var build in builds) {
                var character=s.Characters.Single(x=>x.ActorId==build.ActorId);
                var life=s.Lives.SingleOrDefault(x=>x.ActorId==build.ActorId);
                var selection=s.InitialClassSelections.SingleOrDefault(x=>x.ActorId==build.ActorId);
                var stationarity=s.ShieldStationarity.Single(x=>x.ActorId==build.ActorId);
                var hitDie=s.CharacterHitDice.SingleOrDefault(x=>x.ActorId==build.ActorId&&x.LevelOrdinal==1);
                var skills=s.SkillTraining.Where(x=>x.ActorId==build.ActorId&&build.SelectedSkillIds.Contains(x.SkillId)).ToArray();
                var chainMail=s.PortableEquipment.SingleOrDefault(x=>x.Id==build.ChainMailId);
                var shield=s.PortableEquipment.SingleOrDefault(x=>x.Id==build.ShieldId);
                var dagger=s.PortableEquipment.SingleOrDefault(x=>x.Id==build.DaggerId);
                var pack=s.PortableEquipment.SingleOrDefault(x=>x.Id==build.PackId);
                var rations=s.PortableEquipment.SingleOrDefault(x=>x.Id==build.RationsId);
                var skin=s.PortableEquipment.SingleOrDefault(x=>x.Id==build.WaterskinId);
                var water=s.PortableEquipment.SingleOrDefault(x=>x.Id==build.WaterId);
                var crossbow=s.RepeatingCrossbows.SingleOrDefault(x=>x.Id==build.CrossbowId);
                var ammunition=s.AmmunitionLots.SingleOrDefault(x=>x.Id==build.AmmunitionLotId);
                var lastAdvancement=s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema
                    ?s.CharacterAdvancements.Where(x=>x.ActorId==build.ActorId).OrderBy(x=>x.Revision).LastOrDefault():null;
                var lastAsi=s.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema
                    ?s.CharacterAdvancements.Where(x=>x.ActorId==build.ActorId&&x.AsiAbilityIncreases.Count!=0)
                        .OrderBy(x=>x.Revision).LastOrDefault():null;
                bool validAbilities=lastAsi==null?character.Abilities.SequenceEqual(new[]{10,10,10,10,10,10})
                    :lastAsi.AbilityScoresAfter.SequenceEqual(character.Abilities);
                long expectedMaximumHp=lastAdvancement?.MaximumHpAfter??10L+6L*(character.Levels.Count-1);
                bool validSkills=build.SelectedSkillIds.Count==2&&build.SelectedSkillIds.All(allowedSkills.Contains)
                    &&skills.Length==2&&skills.All(x=>x.ProficiencyRank==1)
                    &&build.SavingThrowProficiencyIds.SequenceEqual(new[]{"CON","STR"},StringComparer.Ordinal);
                bool validCharacter=character.ProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild
                    &&character.Levels.Count>=1&&character.Levels.All(x=>x.ClassName=="Soldier")&&character.Levels[0].BaseHp==10
                    &&validAbilities&&life!=null&&life.MaximumHp==expectedMaximumHp&&hitDie!=null
                    &&hitDie.ClassName=="Soldier"&&hitDie.DieSize==10&&!hitDie.Spent;
                var expectedPackMembers=new[]{SoldierInitialEquipmentIds.Rations,SoldierInitialEquipmentIds.Waterskin,
                    SoldierInitialEquipmentIds.Water,SoldierInitialEquipmentIds.Pitons,SoldierInitialEquipmentIds.Tinderbox};
                bool validEquipment=build.SourceRevision==sourceRevision&&build.OptionalPointBuySpent==12
                    &&build.SelectionProfileId==CharacterAdvancementProfileIds.TestOnlySoldierLevel1InitialBuild&&selection!=null
                    &&build.ChainMailId==SoldierInitialEquipmentIds.ChainMail&&chainMail?.ProfileId=="armor-and-shields.chain-mail"
                    &&chainMail.OwnerId==build.ActorId&&chainMail.MassBasis==PortableMassBasis.Fixed
                    &&chainMail.SourceWeightLb==new RuleQuantity(55)&&chainMail.OperationalWeightLb==new RuleQuantity(55)
                    &&build.ShieldId==SoldierInitialEquipmentIds.Shield&&shield?.ProfileId=="armor-and-shields.shield"
                    &&shield.OwnerId==build.ActorId&&shield.MassBasis==PortableMassBasis.Fixed
                    &&shield.SourceWeightLb==new RuleQuantity(6)&&shield.OperationalWeightLb==new RuleQuantity(6)
                    &&build.DaggerId==SoldierInitialEquipmentIds.Dagger&&dagger?.ProfileId=="simple-melee-weapons.dagger"
                    &&dagger.OwnerId==build.ActorId&&dagger.MassBasis==PortableMassBasis.Fixed
                    &&dagger.SourceWeightLb==new RuleQuantity(1)&&dagger.OperationalWeightLb==new RuleQuantity(1)
                    &&build.PackId==SoldierInitialEquipmentIds.Pack&&pack?.ProfileId=="adventuring-gear.backpack"
                    &&pack.OwnerId==build.ActorId&&pack.MassBasis==PortableMassBasis.Fixed&&pack.SourceWeightLb==new RuleQuantity(5)
                    &&pack.OperationalWeightLb==new RuleQuantity(5)&&pack.CapacityPounds==new RuleQuantity(30)
                    &&pack.CapacityCubicFeet==new RuleQuantity(1)&&pack.FitRuleId==SoldierInitialEquipmentIds.PackFitRule
                    &&pack.FitMemberIds.OrderBy(x=>x,StringComparer.Ordinal).SequenceEqual(expectedPackMembers.OrderBy(x=>x,StringComparer.Ordinal),StringComparer.Ordinal)
                    &&build.InitialPackGroundX==0&&build.InitialPackGroundY==0
                    &&build.RationsId==SoldierInitialEquipmentIds.Rations&&rations?.LinkKind==PortableLinkKind.InventoryLot
                    &&rations.LinkedId==build.RationsId&&rations.OwnerId==build.ActorId&&rations.SourceWeightLb==new RuleQuantity(20)
                    &&s.InventoryLots.SingleOrDefault(x=>x.LotId==build.RationsId)?.CreatedAmount==new RuleQuantity(20)
                    &&build.WaterskinId==SoldierInitialEquipmentIds.Waterskin&&skin?.ProfileId=="adventuring-gear.waterskin"
                    &&skin.OwnerId==build.ActorId&&skin.MassBasis==PortableMassBasis.Fixed&&skin.SourceWeightLb==new RuleQuantity(5)
                    &&skin.OperationalWeightLb==new RuleQuantity(1)
                    &&build.WaterId==SoldierInitialEquipmentIds.Water&&water?.LinkKind==PortableLinkKind.InventoryLot&&water.LinkedId==build.WaterId
                    &&water.OwnerId==build.ActorId&&water.SourceWeightLb==new RuleQuantity(4)
                    &&s.InventoryLots.SingleOrDefault(x=>x.LotId==build.WaterId)?.CreatedAmount==new RuleQuantity(4)
                    &&build.CrossbowId=="TEST_ONLY.actor-repeating-crossbow"&&crossbow!=null&&crossbow.OwnerId==build.ActorId
                    &&crossbow.ProfileId=="new.repeating-heavy-crossbow"
                    &&build.AmmunitionLotId=="TEST_ONLY.actor-crossbow-bolts"&&ammunition!=null&&ammunition.OwnerId==build.ActorId
                    &&ammunition.ProfileId=="ammunition.crossbow-bolts-20"&&ammunition.OriginalQuantity==20
                    &&s.PortableEquipment.Any(x=>x.Id==SoldierInitialEquipmentIds.Crowbar&&x.ProfileId=="adventuring-gear.crowbar"
                        &&x.OwnerId==build.ActorId&&x.SourceWeightLb==new RuleQuantity(5)&&x.OperationalWeightLb==new RuleQuantity(5))
                    &&s.PortableEquipment.Any(x=>x.Id==SoldierInitialEquipmentIds.Hammer&&x.ProfileId=="adventuring-gear.hammer"
                        &&x.OwnerId==build.ActorId&&x.SourceWeightLb==new RuleQuantity(3)&&x.OperationalWeightLb==new RuleQuantity(3))
                    &&s.PortableEquipment.Any(x=>x.Id==SoldierInitialEquipmentIds.Pitons&&x.ProfileId=="adventuring-gear.piton"
                        &&x.OwnerId==build.ActorId&&x.SourceWeightLb==new RuleQuantity(5,2)&&x.OperationalWeightLb==new RuleQuantity(5,2))
                    &&s.PortableEquipment.Any(x=>x.Id==SoldierInitialEquipmentIds.Torches&&x.ProfileId=="adventuring-gear.torch"
                        &&x.OwnerId==build.ActorId&&x.SourceWeightLb==new RuleQuantity(10)&&x.OperationalWeightLb==new RuleQuantity(10))
                    &&s.PortableEquipment.Any(x=>x.Id==SoldierInitialEquipmentIds.Tinderbox&&x.ProfileId=="adventuring-gear.tinderbox"
                        &&x.OwnerId==build.ActorId&&x.SourceWeightLb==new RuleQuantity(1)&&x.OperationalWeightLb==new RuleQuantity(1))
                    &&s.PortableEquipment.Any(x=>x.Id==SoldierInitialEquipmentIds.Rope&&x.ProfileId=="adventuring-gear.rope-hempen-50-feet"
                        &&x.OwnerId==build.ActorId&&x.SourceWeightLb==new RuleQuantity(10)&&x.OperationalWeightLb==new RuleQuantity(10));
                if(!validSkills||!validCharacter||!validEquipment||s.WorldSchedule==null
                    ||stationarity.LastRegularStart!=s.WorldSchedule.LatestStart(build.ActorId,s.WorldSchedule.ProcessedSlot))
                    throw new ArgumentException("Invalid source-scoped Soldier initial build provenance.");
            }
        }
    }
}
