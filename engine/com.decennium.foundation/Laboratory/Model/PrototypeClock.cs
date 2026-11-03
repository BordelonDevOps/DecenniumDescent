#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
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

    public enum InitialSlotBoundaryKind { End, Start }
    public sealed class InitialSlotBoundary
    {
        public string ActorId { get; }
        public RuleTime At { get; }
        public InitialSlotBoundaryKind Kind { get; }
        internal InitialSlotBoundary(string actorId,RuleTime at,InitialSlotBoundaryKind kind)
        { ActorId=actorId;At=at;Kind=kind; }
    }
    public sealed class InitialInitiativeSlot
    {
        public string ActorId { get; }
        public RuleTime Start { get; }
        public RuleTime End { get; }
        internal InitialInitiativeSlot(string actorId,RuleTime start,RuleTime end)
        { ActorId=actorId;Start=start;End=end; }
    }
    /// <summary>
    /// Owner-approved initial allocation only: the caller supplies already resolved initiative
    /// order, including player/Director tie choices. No membership-change or reorder policy.
    /// Immutable absolute checkpoints cannot rewrite existing effect deadline records.
    /// </summary>
    public sealed class PrototypeInitialInitiative
    {
        public IReadOnlyList<InitialInitiativeSlot> Slots { get; }
        public IReadOnlyList<InitialSlotBoundary> Boundaries { get; }
        public PrototypeInitialInitiative(RuleTime encounterStart,IEnumerable<string> orderedActorIds)
        {
            if(orderedActorIds==null) throw new ArgumentNullException(nameof(orderedActorIds));
            var ids=orderedActorIds.ToArray();
            if(ids.Length<1 || ids.Length>64 || ids.Any(id=>!Validation.ValidId(id))
                || ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length)
                throw new ArgumentException("Supply1-64 distinct actors in explicitly resolved initiative order.");
            RuleTime Checkpoint(int index) => RuleTime.FromFraction((BigInteger)encounterStart.Numerator*ids.Length
                +(BigInteger)6*index*encounterStart.Denominator,(BigInteger)encounterStart.Denominator*ids.Length);
            var slots=ids.Select((id,index)=>new InitialInitiativeSlot(id,Checkpoint(index),Checkpoint(index+1))).ToArray();
            Slots=Array.AsReadOnly(slots);
            Boundaries=Array.AsReadOnly(slots.SelectMany(slot=>new[]{
                new InitialSlotBoundary(slot.ActorId,slot.Start,InitialSlotBoundaryKind.Start),
                new InitialSlotBoundary(slot.ActorId,slot.End,InitialSlotBoundaryKind.End)})
                .OrderBy(boundary=>boundary.At).ThenBy(boundary=>boundary.Kind).ToArray());
        }
    }
}
#endif
