#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;

namespace Decennium.Foundation.Laboratory
{
    public enum TaskDegree { CriticalFailure, Failure, Success, CriticalSuccess }

    public readonly struct TaskCheckResult
    {
        public long Total { get; }
        public TaskDegree Degree { get; }
        public bool Success => Degree >= TaskDegree.Success;
        internal TaskCheckResult(long total, TaskDegree degree) { Total = total; Degree = degree; }
    }

    public readonly struct AttackRollResult
    {
        public long Total { get; }
        public bool Hit { get; }
        public bool Critical { get; }
        internal AttackRollResult(long total, bool hit, bool critical)
        { Total = total; Hit = hit; Critical = critical; }
    }

    public readonly struct SavingThrowResult
    {
        public long Total { get; }
        public bool Success { get; }
        public long FailureMargin { get; }
        internal SavingThrowResult(long total, bool success, long failureMargin)
        { Total = total; Success = success; FailureMargin = failureMargin; }
    }

    public readonly struct OpposedCheckResult
    {
        public long ActorTotal { get; }
        public long DefenderTotal { get; }
        public bool ChangesState => ActorTotal > DefenderTotal;
        internal OpposedCheckResult(long actorTotal, long defenderTotal)
        { ActorTotal = actorTotal; DefenderTotal = defenderTotal; }
    }

    /// <summary>
    /// Provisional CORE_RESOLUTION_PLAYTEST.md, Rolls: declared legal d20 results only.
    /// Does not select dice, grant features, validate targets/actions, apply damage or mutate state.
    /// Source hashes and approval scope: docs/unity/evidence/2026-11-03-rolls/SOURCE_BINDINGS.json.
    /// </summary>
    public static class PlaytestRolls
    {
        public static TaskCheckResult TaskCheck(int natural, int modifier, int dc)
        {
            long total = RollTotal(natural, modifier, nameof(natural));
            Nonnegative(dc, nameof(dc));
            TaskDegree degree = total >= (long)dc + 10 ? TaskDegree.CriticalSuccess
                : total >= dc ? TaskDegree.Success
                : total <= (long)dc - 10 ? TaskDegree.CriticalFailure : TaskDegree.Failure;
            if (natural == 20 && degree < TaskDegree.CriticalSuccess) degree++;
            else if (natural == 1 && degree > TaskDegree.CriticalFailure) degree--;
            return new TaskCheckResult(total, degree);
        }

        public static AttackRollResult AttackRoll(int natural, int modifier, int armorClass, int criticalThreshold = 20)
        {
            long total = RollTotal(natural, modifier, nameof(natural));
            Nonnegative(armorClass, nameof(armorClass));
            if (criticalThreshold < 2 || criticalThreshold > 20)
                throw new ArgumentOutOfRangeException(nameof(criticalThreshold));
            bool hit = natural != 1 && (natural == 20 || total >= armorClass);
            return new AttackRollResult(total, hit, hit && natural >= criticalThreshold);
        }

        public static SavingThrowResult SavingThrow(int natural, int modifier, int dc)
        {
            long total = RollTotal(natural, modifier, nameof(natural));
            Nonnegative(dc, nameof(dc));
            return new SavingThrowResult(total, total >= dc, Math.Max(0L, (long)dc - total));
        }

        public static OpposedCheckResult OpposedCheck(int actorNatural, int actorModifier, int defenderNatural, int defenderModifier)
        {
            long actor = RollTotal(actorNatural, actorModifier, nameof(actorNatural));
            long defender = RollTotal(defenderNatural, defenderModifier, nameof(defenderNatural));
            return new OpposedCheckResult(actor, defender);
        }

        // Promote before arithmetic: all int modifiers/DCs are supported without wraparound.
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
