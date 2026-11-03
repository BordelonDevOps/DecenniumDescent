#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    [Flags]
    public enum SoloPause { None=0, Explicit=1, Menu=2, Dialogue=4, TacticalDecision=8 }

    /// <summary>
    /// Owner-approved prototype clock arithmetic. The caller supplies elapsed time, selected
    /// activities and the next pending milestone; this code never reads wall time or runs jobs.
    /// All subsystems observe the returned single time. No cooperative policy is inferred.
    /// </summary>
    public static class PrototypeClock
    {
        private const SoloPause AllPauses=SoloPause.Explicit|SoloPause.Menu|SoloPause.Dialogue|SoloPause.TacticalDecision;
        public static RuleTime Exploration(RuleTime now,RuleTime liveElapsed,SoloPause pause,RuleTime? nextMilestone=null)
        {
            ValidatePause(pause);
            ValidateMilestone(now,nextMilestone);
            if(pause!=SoloPause.None) return now;
            BigInteger numerator=(BigInteger)now.Numerator*liveElapsed.Denominator
                +(BigInteger)liveElapsed.Numerator*now.Denominator;
            BigInteger denominator=(BigInteger)now.Denominator*liveElapsed.Denominator;
            // Bound before converting to Int64 components: a reachable earlier deadline can
            // be representable even when the unbounded requested endpoint would overflow.
            if(nextMilestone.HasValue && numerator*nextMilestone.Value.Denominator
                >= (BigInteger)nextMilestone.Value.Numerator*denominator) return nextMilestone.Value;
            return RuleTime.FromFraction(numerator,denominator);
        }
        /// <summary>Explicitly selected wait/rest/activity target; caller resolves all intervening milestones.</summary>
        public static RuleTime DeclaredActivity(RuleTime now,RuleTime desiredEnd,RuleTime? nextMilestone=null)
            => StopAtMilestone(now,desiredEnd,nextMilestone);
        /// <summary>Application absence supplies no elapsed game time.</summary>
        public static RuleTime RestoreAfterOffline(RuleTime savedTime) => savedTime;
        internal static void ValidatePause(SoloPause pause)
        {
            if((pause & ~AllPauses)!=0) throw new ArgumentException("Unsupported solo pause reason.");
        }
        private static void ValidateMilestone(RuleTime now,RuleTime? milestone)
        {
            if(milestone.HasValue && milestone.Value<now) throw new ArgumentException("Resolve overdue milestones before advancing.");
        }
        internal static RuleTime StopAtMilestone(RuleTime now,RuleTime target,RuleTime? milestone)
        {
            if(target<now) throw new ArgumentException("Time cannot reverse.");
            ValidateMilestone(now,milestone);
            return milestone.HasValue && milestone.Value<target?milestone.Value:target;
        }
    }

    /// <summary>
    /// One ordinary round's absolute six-second window. Explicit checkpoints do not allocate
    /// initial initiative phases. Reaching End twice adds no time; actors and extra turns cannot
    /// enlarge this window. The future session scheduler must persist/own round identity.
    /// </summary>
    public sealed class PrototypeRoundWindow
    {
        public RuleTime Start { get; }
        public RuleTime Current { get; }
        public RuleTime End { get; }
        public bool Complete => Current==End;
        public PrototypeRoundWindow(RuleTime start,RuleTime current)
        {
            Start=start;End=start.AddSeconds(6);
            if(current<start || current>End) throw new ArgumentException("Current time is outside this round.");
            Current=current;
        }
        public PrototypeRoundWindow AdvanceTo(RuleTime checkpoint,SoloPause pause,RuleTime? nextMilestone=null)
        {
            PrototypeClock.ValidatePause(pause);
            if(checkpoint<Current || checkpoint>End) throw new ArgumentException("Checkpoint is outside remaining round.");
            RuleTime bounded=PrototypeClock.StopAtMilestone(Current,checkpoint,nextMilestone);
            return pause==SoloPause.None?new PrototypeRoundWindow(Start,bounded):this;
        }
    }
}
#endif
