#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public static class ManufacturingRules
    {
        public static CraftQuality Quality(int natural, int modifier, int dc, bool takeTen = false)
        {
            if (natural < 1 || natural > 20 || takeTen && natural != 10) throw new ArgumentException("Invalid crafting die.");
            long margin = (long)natural + modifier - dc;
            return !takeTen && natural == 1 || margin <= -10 ? CraftQuality.Mishap : margin < -4 ? CraftQuality.Failed
                : margin < 0 ? CraftQuality.Flawed : margin < 5 ? CraftQuality.Standard : margin < 10 ? CraftQuality.Exceptional : CraftQuality.Masterwork;
        }
        public static bool Eligible(int tradeLevel, int skill, bool toolTrained, bool hasFormula, bool formulaRequired)
        {
            if (tradeLevel < 0 || tradeLevel > 20 || skill < 1 || skill > 20) throw new ArgumentException("Invalid trade level.");
            int effective = toolTrained ? tradeLevel : 0;
            return skill <= (effective == 0 ? 4 : Math.Max(4, effective)) && (!formulaRequired || hasFormula);
        }
        public static bool CanTakeTen(int tradeLevel, int skill, bool trained, bool safeSuitableWorkshop, bool disadvantage)
            => trained && tradeLevel - skill >= 5 && safeSuitableWorkshop && !disadvantage;
        public static int Yield(CraftQuality quality, int standard, CraftQualityChoice choice)
        {
            if (standard < 1 || !Enum.IsDefined(typeof(CraftQuality),quality) || quality == CraftQuality.None || !Enum.IsDefined(typeof(CraftQualityChoice),choice)) throw new ArgumentException("Invalid crafting yield.");
            if (quality == CraftQuality.Mishap || quality == CraftQuality.Failed) return 0;
            if (quality == CraftQuality.Flawed) return standard >= 2 ? standard / 2 : 0; // Caller must supply a reviewed singleton flaw profile.
            return choice == CraftQualityChoice.FullYield ? quality == CraftQuality.Masterwork ? checked((int)((long)standard * 3 / 2))
                : quality == CraftQuality.Exceptional ? checked((int)((long)standard * 5 / 4)) : standard : standard;
        }
        public static RuleQuantity FailureRecovery(RuleQuantity amount, bool consumed, bool catalyst, bool divisible)
        {
            if (!consumed) return amount;
            if (catalyst) return default;
            long scale = divisible ? 100 : 1;
            var units = ((BigInteger)amount.Numerator * scale) / ((BigInteger)amount.Denominator * 4);
            return RuleQuantity.FromFraction(units, scale);
        }
        public static int TradeAward(CraftQuality quality, int level, int recipeSkill, int trivialAt, bool trained,
            bool priorSuccess, bool priorFindingAtLevel, bool realInputsAndLabor, bool usableFinding, int mishap)
        {
            if (!trained || level >= trivialAt) return 0;
            if (quality >= CraftQuality.Standard) return priorSuccess ? 2 : 4;
            return quality != CraftQuality.None && recipeSkill >= level && !priorFindingAtLevel && realInputsAndLabor && usableFinding && mishap != 6 ? 1 : 0;
        }
        public static (int Level, int Xp) AdvanceTrade(int level, int xp, int award)
        {
            if (level < 1 || level > 20 || xp < 0 || award < 0) throw new ArgumentException("Invalid trade progression.");
            xp = checked(xp + award);
            while (level < 20 && xp >= 10 + level) { xp -= 10 + level; level++; }
            return (level, xp);
        }
        // Exact public recipe-4 component occurrences, not a name-only substitute registry.
        public static readonly System.Collections.Generic.IReadOnlyList<string> Recipe4Components = Array.AsReadOnly(new[] { "ing-4-0-alchemical_catalyst", "ing-4-1-crystal_vial", "ing-4-2-alchemical_base", "drop-black_blood_sample" });
        public static readonly System.Collections.Generic.IReadOnlyList<int> Recipe4Amounts = Array.AsReadOnly(new[] { 5, 5, 5, 1 });
        public static RuleQuantity Recipe4Mass(int component) => component == 3 ? new RuleQuantity(38,100) : new RuleQuantity(1,10);
        public static bool Recipe4Catalyst(int component) => component == 0 || component == 3;
        public static bool Recipe4Divisible(int component) => component != 1;
        public static RuleQuantity Recipe4CompoundMass(int retainedCatalyst)
            => new RuleQuantity(138,100) - (retainedCatalyst < 0 ? default : Recipe4Mass(retainedCatalyst));
        public static bool Recipe4CanYield(CraftQuality quality, int reservedExtraVials, int retainedCatalyst)
        {
            int yield = Yield(quality, 5, CraftQualityChoice.FullYield);
            return yield <= 5 + reservedExtraVials && new RuleQuantity(yield,10) <= Recipe4CompoundMass(retainedCatalyst);
        }
    }
}
#endif
