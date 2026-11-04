#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    // Only the clause families used by these projections; not the complete28-condition catalog.
    public enum ConditionClause { Blinded, Dazed, Frightened, Grappled, Incapacitated, Invisible, Paralyzed,
        Petrified, Poisoned, Prone, Restrained, Staggered, Stunned, Unconscious }
    public enum ConditionAttackKind { Melee, Ranged }
    public enum HpRestorationKind { HealingEffect, DeathNaturalTwenty, StableRecovery }
    /// <summary>Projection clauses. The public constructor retains the legacy parent-component
    /// inference contract. The condition lifecycle supplies already resolved components through
    /// FromResolved, so named component immunity is never undone by that legacy inference.</summary>
    public sealed class ConditionClauses
    {
        public IReadOnlyList<ConditionClause> Active { get; }
        private readonly bool inferInherited;
        public ConditionClauses(params ConditionClause[] active) : this(true,active) { }
        private ConditionClauses(bool infer,ConditionClause[] active)
        {
            if(active==null||active.Any(x=>!Enum.IsDefined(typeof(ConditionClause),x)))throw new ArgumentException("Unknown condition projection clause.");
            Active=Array.AsReadOnly(active.Distinct().OrderBy(x=>x).ToArray());
            inferInherited=infer;
        }
        internal static ConditionClauses FromResolved(IEnumerable<ConditionClause> active)=>new ConditionClauses(false,active.ToArray());
        public bool Has(ConditionClause c)=>Active.Contains(c);
        internal bool Incapacitated=>Has(ConditionClause.Incapacitated)||inferInherited&&(Has(ConditionClause.Paralyzed)||Has(ConditionClause.Petrified)||Has(ConditionClause.Stunned)||Has(ConditionClause.Unconscious));
        internal bool Immobile=>Has(ConditionClause.Paralyzed)||Has(ConditionClause.Petrified)||Has(ConditionClause.Stunned)||Has(ConditionClause.Unconscious);
    }
    public readonly struct ConditionPermissions
    {
        public bool Action { get; }
        public bool BonusAction { get; }
        public bool Reaction { get; }
        public bool VoluntarySpeed { get; }
        public bool Dash { get; }
        public bool ConcentrationMayContinue { get; }
        public bool MustChooseActionOrMovement { get; }
        internal ConditionPermissions(bool action,bool bonus,bool reaction,bool move,bool dash,bool concentration,bool choose)
        {Action=action;BonusAction=bonus;Reaction=reaction;VoluntarySpeed=move;Dash=dash;ConcentrationMayContinue=concentration;MustChooseActionOrMovement=choose;}
    }
    public readonly struct ConditionAttackModifiers
    {
        public bool AdvantagePresent { get; }
        public bool DisadvantagePresent { get; }
        public D20Selection RollMode=>PlaytestDice.Selection(AdvantagePresent?1:0,DisadvantagePresent?1:0);
        public bool CriticalIfHit { get; }
        public bool AttackerNotIncapacitated { get; }
        internal ConditionAttackModifiers(bool advantage,bool disadvantage,bool critical,bool able)
        {AdvantagePresent=advantage;DisadvantagePresent=disadvantage;CriticalIfHit=critical;AttackerNotIncapacitated=able;}
    }
    /// <summary>Source-bound condition calculations, not application legality or authoritative condition
    /// state. Callers supply exact active clauses, visibility facts and legal events after specific rules.
    /// Returned permissions are condition constraints only; they grant no Action, Speed, target or die.</summary>
    public static class PlaytestConditions
    {
        private static void Level(int exhaustion){if(exhaustion<0||exhaustion>6)throw new ArgumentOutOfRangeException(nameof(exhaustion));}
        private static void Clauses(ConditionClauses conditions){if(conditions==null)throw new ArgumentNullException(nameof(conditions));}
        public static long ExhaustionMaximum(long otherwiseMaximum,int level)
        {Level(level);return PlaytestMaximumHp.SystemicMaximum(otherwiseMaximum,exhaustion:level);}
        // Exhaustion-only capacity projection. A combined systemic-factor ledger must multiply its
        // compatible rational factors before rounding; do not chain separately rounded modifiers.
        public static LifeState RecomputeExhaustionCapacity(LifeState state,long otherwiseMaximum,int level)
        {
            if(state==null)throw new ArgumentNullException(nameof(state));long max=ExhaustionMaximum(otherwiseMaximum,level);
            return PlaytestMaximumHp.ApplyCapacity(state,max);
        }
        // Resolve an actual admitted track change, without survival replacements. Numerical capacity
        // recalculation or repeating an existing level6 is not a new lethal transition.
        public static LifeState ChangeExhaustion(LifeState state,long otherwiseMaximum,int previousLevel,int level)
        {
            Level(previousLevel);var next=RecomputeExhaustionCapacity(state,otherwiseMaximum,level);
            if(previousLevel==6||level!=6)return next;
            return new LifeState(next.MaximumHp,0,next.TemporaryHp,next.Wounds,dead:true,deathSuccesses:next.DeathSuccesses,
                deathFailures:next.DeathFailures,usesDeathSaves:next.UsesDeathSaves,lastDeathTurn:next.LastDeathTurn);
        }
        public static long EffectiveSpeed(long baseSpeed,long flatAdjustment,ConditionClauses conditions,int exhaustion=0)
        {
            Clauses(conditions);Level(exhaustion);if(baseSpeed<0)throw new ArgumentOutOfRangeException(nameof(baseSpeed));
            if(exhaustion>=5||conditions.Immobile||conditions.Has(ConditionClause.Grappled)||conditions.Has(ConditionClause.Restrained))return 0;
            // Widen before adding; halving may bring an intermediate sum back into the supported range.
            BigInteger speed=BigInteger.Max(0,(BigInteger)baseSpeed+flatAdjustment);if(exhaustion>=2)speed/=2;
            if(speed>long.MaxValue)throw new OverflowException("Effective Speed exceeds supported range.");return (long)speed;
        }
        public static ConditionPermissions Permissions(ConditionClauses conditions,long actionsTaken=0,long voluntarySpeedSpent=0)
        {
            Clauses(conditions);if(actionsTaken<0||voluntarySpeedSpent<0)throw new ArgumentException("Invalid prior turn spending.");
            bool incap=conditions.Incapacitated,dazed=conditions.Has(ConditionClause.Dazed);
            bool action=!incap&&(!dazed||actionsTaken==0&&voluntarySpeedSpent==0);
            return new ConditionPermissions(action,!incap&&!dazed,!incap&&!conditions.Has(ConditionClause.Staggered),
                !conditions.Immobile&&(!dazed||actionsTaken==0),action&&!dazed,!incap,dazed&&!incap&&actionsTaken==0&&voluntarySpeedSpent==0);
        }
        public static ConditionAttackModifiers Attack(ConditionClauses attacker,ConditionClauses target,long distanceFeet=5,
            ConditionAttackKind kind=ConditionAttackKind.Melee,int attackerExhaustion=0,bool attackerInvisibleLocationKnown=false,
            bool targetInvisibleLocationKnown=false,bool targetSeesInvisibleAttacker=false,bool attackerSeesInvisibleTarget=false,
            bool frightenedSourceVisible=false,bool otherAdvantage=false,bool otherDisadvantage=false)
        {
            Clauses(attacker);Clauses(target);Level(attackerExhaustion);
            if(distanceFeet<0||!Enum.IsDefined(typeof(ConditionAttackKind),kind))throw new ArgumentException("Invalid attack geometry/kind.");
            bool adv=otherAdvantage,dis=otherDisadvantage;
            dis|=attacker.Has(ConditionClause.Blinded)||attacker.Has(ConditionClause.Poisoned)||attacker.Has(ConditionClause.Prone)||attacker.Has(ConditionClause.Restrained)||attackerExhaustion>=3;
            dis|=attacker.Has(ConditionClause.Frightened)&&frightenedSourceVisible;
            adv|=target.Has(ConditionClause.Blinded)||target.Has(ConditionClause.Paralyzed)||target.Has(ConditionClause.Petrified)
                ||target.Has(ConditionClause.Restrained)||target.Has(ConditionClause.Stunned)||target.Has(ConditionClause.Unconscious);
            if(target.Has(ConditionClause.Prone)){adv|=kind==ConditionAttackKind.Melee&&distanceFeet<=5;dis|=kind==ConditionAttackKind.Ranged||distanceFeet>5;}
            // Known location is not sight. Invisible-specific bonuses end without restoring sight-target legality.
            // Do not also pass generic unseen bonuses caused solely by this same Invisible condition.
            adv|=attacker.Has(ConditionClause.Invisible)&&!attackerInvisibleLocationKnown&&!targetSeesInvisibleAttacker;
            dis|=target.Has(ConditionClause.Invisible)&&!targetInvisibleLocationKnown&&!attackerSeesInvisibleTarget;
            bool critical=(target.Has(ConditionClause.Paralyzed)||target.Has(ConditionClause.Unconscious))&&distanceFeet<=5;
            return new ConditionAttackModifiers(adv,dis,critical,!attacker.Incapacitated);
        }
        public static long HpRestorationAmount(long potential,bool corrupted,HpRestorationKind kind=HpRestorationKind.HealingEffect)
        {
            if(potential<0||!Enum.IsDefined(typeof(HpRestorationKind),kind)||kind!=HpRestorationKind.HealingEffect&&potential!=1)throw new ArgumentException("Invalid restoration amount/kind.");
            return corrupted&&kind==HpRestorationKind.HealingEffect?potential/2:potential;
        }
        // Input is already after flat reductions/saves; do not halve this result again for another resistance.
        public static long PetrifiedDamage(long damage,bool corruptionDamage=false,bool explicitCorruptionResistance=false,bool immune=false)
        {
            if(damage<0)throw new ArgumentOutOfRangeException(nameof(damage));
            return immune?0:!corruptionDamage||explicitCorruptionResistance?damage/2:damage;
        }
    }
}
#endif
