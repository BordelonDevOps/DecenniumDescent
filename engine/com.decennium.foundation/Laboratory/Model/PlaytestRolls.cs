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
            RuleTaskCheckResult result = RuleResolution.TaskCheck(natural, modifier, dc);
            return new TaskCheckResult(result.Total, (TaskDegree)result.Degree);
        }

        public static AttackRollResult AttackRoll(int natural, int modifier, int armorClass, int criticalThreshold = 20)
        {
            RuleAttackRollResult result = RuleResolution.AttackRoll(natural, modifier, armorClass, criticalThreshold);
            return new AttackRollResult(result.Total, result.Hit, result.Critical);
        }

        public static SavingThrowResult SavingThrow(int natural, int modifier, int dc)
        {
            RuleSavingThrowResult result = RuleResolution.SavingThrow(natural, modifier, dc);
            return new SavingThrowResult(result.Total, result.Success, result.FailureMargin);
        }

        public static OpposedCheckResult OpposedCheck(int actorNatural, int actorModifier, int defenderNatural, int defenderModifier)
        {
            RuleOpposedCheckResult result = RuleResolution.OpposedCheck(actorNatural, actorModifier,
                defenderNatural, defenderModifier);
            return new OpposedCheckResult(result.ActorTotal, result.DefenderTotal);
        }
    }
}
#endif
