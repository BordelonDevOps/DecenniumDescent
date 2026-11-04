using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Exact phase accounting. The selected rule supplies phase lengths and interruption
    /// policy; elapsed world time is not itself permission to credit labor.</summary>
    public sealed class ActiveWorkProgress
    {
        public const int MaxPhases = 64;
        public IReadOnlyList<RuleTime> Phases { get; }
        public int CompletedPhases { get; }
        public RuleTime Partial { get; }
        public RuleTime Labor { get; }
        public bool Complete => CompletedPhases == Phases.Count;
        public RuleTime Retained => Sum(Phases.Take(CompletedPhases).Concat(new[] { Partial }));
        public RuleTime Required => Sum(Phases);
        public RuleTime Remaining => Subtract(Required, Retained);
        public ActiveWorkProgress(IEnumerable<RuleTime> phases, int completedPhases = 0, RuleTime partial = default, RuleTime labor = default)
        {
            if (phases == null) throw new ArgumentNullException(nameof(phases));
            var values = phases.ToArray();
            if (values.Length < 1 || values.Length > MaxPhases || values.Any(x => x == default)
                || completedPhases < 0 || completedPhases > values.Length
                || (completedPhases == values.Length ? partial != default : partial >= values[completedPhases]))
                throw new ArgumentException("Invalid active work phase position.");
            Phases = Array.AsReadOnly(values); CompletedPhases = completedPhases; Partial = partial; Labor = labor;
            if (Labor < Retained) throw new ArgumentException("Retained work exceeds actual labor.");
        }
        public ActiveWorkProgress Credit(RuleTime duration)
        {
            if (duration == default || duration > Remaining) throw new ArgumentException("Invalid active work credit.");
            int count = CompletedPhases; RuleTime partial = Partial, left = duration;
            while (left > default(RuleTime)) {
                var need = Subtract(Phases[count], partial);
                if (left < need) { partial = Add(partial, left); break; }
                left = Subtract(left, need); count++; partial = default;
            }
            return new ActiveWorkProgress(Phases, count, partial, Add(Labor, duration));
        }
        public ActiveWorkProgress Interrupt(bool discardUnfinishedPhase)
            => discardUnfinishedPhase && Partial != default ? new ActiveWorkProgress(Phases, CompletedPhases, default, Labor) : this;
        private static RuleTime Sum(IEnumerable<RuleTime> values)
        {
            var q = RuleQuantity.Sum(values.Select(x => new RuleQuantity(x.Numerator, x.Denominator)));
            return new RuleTime(q.Numerator, q.Denominator);
        }
        private static RuleTime Add(RuleTime a, RuleTime b) => Sum(new[] { a, b });
        private static RuleTime Subtract(RuleTime a, RuleTime b)
        {
            var q = new RuleQuantity(a.Numerator, a.Denominator) - new RuleQuantity(b.Numerator, b.Denominator);
            return new RuleTime(q.Numerator, q.Denominator);
        }
    }
}
