#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;

namespace Decennium.Foundation.Laboratory
{
    public enum RuleD20Selection { Normal, Advantage, Disadvantage }

    /// <summary>One explicit d20 draw selection and its deterministic random-state trace.</summary>
    public readonly struct RuleD20Roll
    {
        public RuleD20Selection Selection { get; }
        public int First { get; }
        public int? Second { get; }
        public int Natural { get; }
        public uint NextRandomState { get; }
        public long WordsConsumed { get; }

        internal RuleD20Roll(RuleD20Selection selection, int first, int? second, int natural,
            uint nextRandomState, long wordsConsumed)
        {
            Selection = selection;
            First = first;
            Second = second;
            Natural = natural;
            NextRandomState = nextRandomState;
            WordsConsumed = wordsConsumed;
        }
    }

    /// <summary>Shared d20 selection policy. Callers supply eligible modifier sources.</summary>
    public static class RuleDice
    {
        public static RuleD20Selection SelectD20(int advantageSources, int disadvantageSources)
        {
            if (advantageSources < 0 || disadvantageSources < 0)
                throw new ArgumentOutOfRangeException(nameof(advantageSources));
            if ((advantageSources == 0) == (disadvantageSources == 0)) return RuleD20Selection.Normal;
            return advantageSources > 0 ? RuleD20Selection.Advantage : RuleD20Selection.Disadvantage;
        }

        public static RuleD20Roll RollD20(uint initialState, int advantageSources = 0, int disadvantageSources = 0)
        {
            RuleD20Selection selection = SelectD20(advantageSources, disadvantageSources);
            BoundedDraw first = DiceStream.Draw(initialState, 20);
            if (selection == RuleD20Selection.Normal)
                return new RuleD20Roll(selection, first.Value + 1, null, first.Value + 1,
                    first.NextState, first.WordsConsumed);

            BoundedDraw second = DiceStream.Draw(first.NextState, 20);
            int a = first.Value + 1;
            int b = second.Value + 1;
            int selected = selection == RuleD20Selection.Advantage ? Math.Max(a, b) : Math.Min(a, b);
            return new RuleD20Roll(selection, a, b, selected, second.NextState,
                checked(first.WordsConsumed + second.WordsConsumed));
        }
    }

    public enum RuleTaskDegree { CriticalFailure, Failure, Success, CriticalSuccess }

    public readonly struct RuleTaskCheckResult
    {
        public long Total { get; }
        public RuleTaskDegree Degree { get; }
        public bool Success => Degree >= RuleTaskDegree.Success;

        internal RuleTaskCheckResult(long total, RuleTaskDegree degree)
        { Total = total; Degree = degree; }
    }

    public readonly struct RuleAttackRollResult
    {
        public long Total { get; }
        public bool Hit { get; }
        public bool Critical { get; }

        internal RuleAttackRollResult(long total, bool hit, bool critical)
        { Total = total; Hit = hit; Critical = critical; }
    }

    public readonly struct RuleSavingThrowResult
    {
        public long Total { get; }
        public bool Success { get; }
        public long FailureMargin { get; }

        internal RuleSavingThrowResult(long total, bool success, long failureMargin)
        { Total = total; Success = success; FailureMargin = failureMargin; }
    }

    public readonly struct RuleOpposedCheckResult
    {
        public long ActorTotal { get; }
        public long DefenderTotal { get; }
        public bool ChangesState => ActorTotal > DefenderTotal;

        internal RuleOpposedCheckResult(long actorTotal, long defenderTotal)
        { ActorTotal = actorTotal; DefenderTotal = defenderTotal; }
    }

    /// <summary>Shared source-bound arithmetic for task, attack, save, and opposed rolls.
    /// Modifiers, legality, consequences, and record persistence remain caller-owned.</summary>
    public static class RuleResolution
    {
        public static RuleTaskCheckResult TaskCheck(int natural, int modifier, int dc)
        {
            long total = RollTotal(natural, modifier, nameof(natural));
            Nonnegative(dc, nameof(dc));
            RuleTaskDegree degree = total >= (long)dc + 10 ? RuleTaskDegree.CriticalSuccess
                : total >= dc ? RuleTaskDegree.Success
                : total <= (long)dc - 10 ? RuleTaskDegree.CriticalFailure : RuleTaskDegree.Failure;
            if (natural == 20 && degree < RuleTaskDegree.CriticalSuccess) degree++;
            else if (natural == 1 && degree > RuleTaskDegree.CriticalFailure) degree--;
            return new RuleTaskCheckResult(total, degree);
        }

        public static RuleAttackRollResult AttackRoll(int natural, int modifier, int armorClass, int criticalThreshold = 20)
        {
            long total = RollTotal(natural, modifier, nameof(natural));
            Nonnegative(armorClass, nameof(armorClass));
            if (criticalThreshold < 2 || criticalThreshold > 20)
                throw new ArgumentOutOfRangeException(nameof(criticalThreshold));
            bool hit = natural != 1 && (natural == 20 || total >= armorClass);
            return new RuleAttackRollResult(total, hit, hit && natural >= criticalThreshold);
        }

        public static RuleSavingThrowResult SavingThrow(int natural, int modifier, int dc)
        {
            long total = RollTotal(natural, modifier, nameof(natural));
            Nonnegative(dc, nameof(dc));
            return new RuleSavingThrowResult(total, total >= dc, Math.Max(0L, (long)dc - total));
        }

        public static RuleOpposedCheckResult OpposedCheck(int actorNatural, int actorModifier,
            int defenderNatural, int defenderModifier)
        {
            long actor = RollTotal(actorNatural, actorModifier, nameof(actorNatural));
            long defender = RollTotal(defenderNatural, defenderModifier, nameof(defenderNatural));
            return new RuleOpposedCheckResult(actor, defender);
        }

        private static long RollTotal(int natural, int modifier, string parameter)
        {
            if (natural < 1 || natural > 20) throw new ArgumentOutOfRangeException(parameter);
            return (long)natural + modifier;
        }

        private static void Nonnegative(int value, string parameter)
        { if (value < 0) throw new ArgumentOutOfRangeException(parameter); }
    }
}
#endif
