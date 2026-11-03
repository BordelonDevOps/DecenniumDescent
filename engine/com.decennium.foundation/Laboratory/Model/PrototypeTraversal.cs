#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public enum OrdinaryTraversal { Walk, Climb, Swim }

    /// <summary>Owner-approved prototype limits, in exact half-feet; not collision or jump execution.</summary>
    public readonly struct PrototypeJumpLimits
    {
        public long HorizontalHalfFeet { get; }
        public long VerticalHalfFeet { get; }
        public decimal HorizontalFeet => HorizontalHalfFeet / 2m;
        public decimal VerticalFeet => VerticalHalfFeet / 2m;
        internal PrototypeJumpLimits(long horizontal,long vertical)
        { HorizontalHalfFeet=horizontal;VerticalHalfFeet=vertical; }
    }

    /// <summary>
    /// New prototype choices explicitly adopted by the owner on 2026-11-03.
    /// See docs/unity/PROTOTYPE_RULE_DECISIONS.md. Not recovered rules or release content.
    /// Route legality, continuous run-up validation, costs, body/tool access and interruption
    /// remain the authoritative caller's responsibility. These helpers grant no action or movement.
    /// </summary>
    public static class PrototypeTraversal
    {
        public const int RequiredRunUpFeet=10;
        public static PrototypeJumpLimits JumpLimits(int strengthScore,bool hasTenFootContinuousRunUp)
        {
            if(strengthScore<0) throw new ArgumentOutOfRangeException(nameof(strengthScore));
            long factor=hasTenFootContinuousRunUp?2:1;
            return new PrototypeJumpLimits(factor*strengthScore,
                factor*Math.Max(0L,3L+PlaytestCharacters.AbilityModifier(strengthScore)));
        }
        /// <summary>Ratio only. Caller supplies walking pace in its explicit unit and pays an ordinary Dash.</summary>
        public static decimal RunningPace(decimal walkingPace,bool ordinaryDashPaid)
        {
            if(walkingPace<0) throw new ArgumentOutOfRangeException(nameof(walkingPace));
            if(!ordinaryDashPaid) throw new ArgumentException("Running requires a paid ordinary Dash.");
            decimal doubled=checked(2m*walkingPace);
            // Decimal multiplication can round to fit its 96-bit coefficient even in a
            // checked context. No prototype rounding policy was adopted, so reject that.
            int[] before=decimal.GetBits(walkingPace),after=decimal.GetBits(doubled);
            if(Coefficient(after)*BigInteger.Pow(10,(before[3]>>16)&255)
                != 2*Coefficient(before)*BigInteger.Pow(10,(after[3]>>16)&255))
                throw new OverflowException("Exact doubled pace cannot be represented as decimal.");
            return doubled;
        }
        private static BigInteger Coefficient(int[] bits) => (BigInteger)(uint)bits[0]
            + ((BigInteger)(uint)bits[1]<<32) + ((BigInteger)(uint)bits[2]<<64);
        /// <summary>Whole-foot paths only; no fractional jump limit is rounded into a movement debit.</summary>
        public static long MovementCost(long distanceFeet,OrdinaryTraversal mode,bool hasDedicatedSpeed=false,
            TerrainCost terrain=TerrainCost.Normal,bool crawling=false,bool squeezing=false)
        {
            if(!Enum.IsDefined(typeof(OrdinaryTraversal),mode)) throw new ArgumentException("Unsupported traversal mode.");
            long baseCost=PlaytestCombatBudgets.MovementCost(distanceFeet,terrain,crawling,squeezing);
            return checked(baseCost+((mode!=OrdinaryTraversal.Walk && !hasDedicatedSpeed)?distanceFeet:0));
        }
    }
}
#endif
