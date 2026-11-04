#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;

namespace Decennium.Foundation.Laboratory
{
    public enum RangedAttackFailure
    {
        None,
        UnknownTargetLocation,
        BlockedLineOfFire,
        TotalCover,
        OutOfRange
    }

    /// <summary>Caller-supplied, already-authored facts for resolving one ranged attack roll.
    /// This query does not validate a weapon, hands, ammunition, Action/Reaction authority, creature
    /// state, or geometry; those remain with the command and spatial policies.</summary>
    public readonly struct RangedAttackRequest
    {
        public long DistanceFeet { get; }
        public long NormalRangeFeet { get; }
        public long MaximumRangeFeet { get; }
        public int TargetArmorClass { get; }
        public int DexterityModifier { get; }
        public int ProficiencyBonus { get; }
        public bool Proficient { get; }
        public int FlatAttackModifier { get; }
        public CombatCover TargetCover { get; }
        public bool TargetLocationKnown { get; }
        public bool TargetVisible { get; }
        public bool LineOfFireClear { get; }
        public bool AttackerUnseen { get; }
        public bool CloseHostileEligible { get; }
        public ConditionClauses AttackerConditions { get; }
        public ConditionClauses TargetConditions { get; }
        public int AttackerExhaustion { get; }
        public bool AttackerInvisibleLocationKnown { get; }
        public bool TargetInvisibleLocationKnown { get; }
        public bool TargetSeesInvisibleAttacker { get; }
        public bool AttackerSeesInvisibleTarget { get; }
        public bool FrightenedSourceVisible { get; }
        public int AdditionalAdvantageSources { get; }
        public int AdditionalDisadvantageSources { get; }

        public RangedAttackRequest(long distanceFeet,long normalRangeFeet,long maximumRangeFeet,int targetArmorClass,
            int dexterityModifier,int proficiencyBonus,bool proficient,int flatAttackModifier,CombatCover targetCover,
            bool targetLocationKnown,bool targetVisible,bool lineOfFireClear,bool attackerUnseen,bool closeHostileEligible,
            ConditionClauses attackerConditions,ConditionClauses targetConditions,int attackerExhaustion=0,
            bool attackerInvisibleLocationKnown=false,bool targetInvisibleLocationKnown=false,
            bool targetSeesInvisibleAttacker=false,bool attackerSeesInvisibleTarget=false,bool frightenedSourceVisible=false,
            int additionalAdvantageSources=0,int additionalDisadvantageSources=0)
        {
            DistanceFeet=distanceFeet;NormalRangeFeet=normalRangeFeet;MaximumRangeFeet=maximumRangeFeet;
            TargetArmorClass=targetArmorClass;DexterityModifier=dexterityModifier;ProficiencyBonus=proficiencyBonus;
            Proficient=proficient;FlatAttackModifier=flatAttackModifier;TargetCover=targetCover;
            TargetLocationKnown=targetLocationKnown;TargetVisible=targetVisible;LineOfFireClear=lineOfFireClear;
            AttackerUnseen=attackerUnseen;CloseHostileEligible=closeHostileEligible;
            AttackerConditions=attackerConditions;TargetConditions=targetConditions;AttackerExhaustion=attackerExhaustion;
            AttackerInvisibleLocationKnown=attackerInvisibleLocationKnown;TargetInvisibleLocationKnown=targetInvisibleLocationKnown;
            TargetSeesInvisibleAttacker=targetSeesInvisibleAttacker;AttackerSeesInvisibleTarget=attackerSeesInvisibleTarget;
            FrightenedSourceVisible=frightenedSourceVisible;AdditionalAdvantageSources=additionalAdvantageSources;
            AdditionalDisadvantageSources=additionalDisadvantageSources;
        }
    }

    public sealed class RangedAttackResolution
    {
        public bool Legal=>Failure==RangedAttackFailure.None;
        public RangedAttackFailure Failure { get; }
        public bool RangeDisadvantage { get; }
        public int AttackModifier { get; }
        public int EffectiveArmorClass { get; }
        public D20Roll Roll { get; }
        public AttackRollResult Attack { get; }
        public bool Critical { get; }
        public uint RandomStateAfter { get; }

        internal RangedAttackResolution(RangedAttackFailure failure,uint initialState)
        {Failure=failure;RandomStateAfter=initialState;}
        internal RangedAttackResolution(bool rangeDisadvantage,int modifier,int armorClass,D20Roll roll,AttackRollResult attack,bool critical)
        {Failure=RangedAttackFailure.None;RangeDisadvantage=rangeDisadvantage;AttackModifier=modifier;EffectiveArmorClass=armorClass;
            Roll=roll;Attack=attack;Critical=critical;RandomStateAfter=roll.NextRandomState;}
    }

    /// <summary>Source-bound calculation for the ranged-attack roll only. Target selection, perception,
    /// line-of-fire facts, weapon legality, resource spending and hit damage are resolved by other layers.</summary>
    public static class RangedAttackRules
    {
        public static RangedAttackResolution Resolve(uint initialRandomState,RangedAttackRequest request)
        {
            if(request.DistanceFeet<0||request.NormalRangeFeet<0||request.MaximumRangeFeet<request.NormalRangeFeet
                ||request.TargetArmorClass<0||request.ProficiencyBonus<0||request.AttackerExhaustion<0||request.AttackerExhaustion>6
                ||request.AdditionalAdvantageSources<0||request.AdditionalDisadvantageSources<0
                ||request.AttackerConditions==null||request.TargetConditions==null
                ||!Enum.IsDefined(typeof(CombatCover),request.TargetCover))throw new ArgumentException("Invalid ranged-attack facts.",nameof(request));

            if(!request.TargetLocationKnown)return new RangedAttackResolution(RangedAttackFailure.UnknownTargetLocation,initialRandomState);
            if(!request.LineOfFireClear)return new RangedAttackResolution(RangedAttackFailure.BlockedLineOfFire,initialRandomState);
            var cover=PlanarCombatGeometry.BestCover(new[]{request.TargetCover});
            if(!cover.DirectTargetLegal)return new RangedAttackResolution(RangedAttackFailure.TotalCover,initialRandomState);
            var range=PlanarCombatGeometry.RangedRange(request.DistanceFeet,request.NormalRangeFeet,request.MaximumRangeFeet);
            if(!range.WithinMaximum)return new RangedAttackResolution(RangedAttackFailure.OutOfRange,initialRandomState);

            int modifier=checked(request.DexterityModifier+(request.Proficient?request.ProficiencyBonus:0)+request.FlatAttackModifier);
            int armorClass=checked(request.TargetArmorClass+cover.DefenseBonus.GetValueOrDefault());
            var conditions=PlaytestConditions.Attack(request.AttackerConditions,request.TargetConditions,request.DistanceFeet,
                ConditionAttackKind.Ranged,request.AttackerExhaustion,request.AttackerInvisibleLocationKnown,
                request.TargetInvisibleLocationKnown,request.TargetSeesInvisibleAttacker,request.AttackerSeesInvisibleTarget,
                request.FrightenedSourceVisible);
            bool advantage=conditions.AdvantagePresent||request.AttackerUnseen||request.AdditionalAdvantageSources>0;
            bool disadvantage=conditions.DisadvantagePresent||!request.TargetVisible||range.RangeDisadvantage
                ||request.CloseHostileEligible||request.AdditionalDisadvantageSources>0;
            var roll=PlaytestDice.RollD20(initialRandomState,advantage?1:0,disadvantage?1:0);
            var attack=PlaytestRolls.AttackRoll(roll.Natural,modifier,armorClass);
            return new RangedAttackResolution(range.RangeDisadvantage,modifier,armorClass,roll,attack,
                attack.Hit&&(attack.Critical||conditions.CriticalIfHit));
        }
    }
}
#endif
