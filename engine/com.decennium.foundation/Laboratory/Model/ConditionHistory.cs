#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class ConditionHistoryTransition
    {
        public ConditionHistory State { get; }
        public IReadOnlyList<ConditionConsequence> Consequences { get; }
        public bool ApplicationPrevented { get; }
        internal ConditionHistoryTransition(ConditionHistory state, ConditionTransition transition)
        { State = state; Consequences = transition.Consequences; ApplicationPrevented = transition.ApplicationPrevented; }
    }

    /// <summary>Replay boundary for the provisional pure lifecycle. Restore reconstructs state,
    /// never returns historical consequences as pending work. The host must separately persist
    /// the world consequences and its command receipts in the same atomic snapshot.</summary>
    public sealed class ConditionHistory
    {
        public const string PolicyId = "TEST_ONLY.generic-conditions-v1";
        public ConditionJournal Journal { get; }
        public ConditionLedger Ledger { get; }
        private ConditionHistory(ConditionJournal journal, ConditionLedger ledger) { Journal = journal; Ledger = ledger; }
        public ConditionHistory(string target, EffectClockMarker origin = default)
            : this(new ConditionJournal(PolicyId, target, Stamp(origin)), new ConditionLedger(target, origin)) { }
        public static ConditionHistory Restore(ConditionJournal journal)
        {
            if (journal == null) throw new ArgumentNullException(nameof(journal));
            if (journal.PolicyId != PolicyId) throw new ArgumentException("Unsupported condition interpretation policy.");
            var ledger = new ConditionLedger(journal.Target, Marker(journal.Origin));
            foreach (var operation in journal.Operations) ledger = Resolve(ledger, operation).State;
            return new ConditionHistory(journal, ledger);
        }
        public ConditionHistoryTransition Append(ConditionOperation operation)
        {
            // Validate chronology, identity and capacity before returning any new state.
            var journal = Journal.Append(operation);
            var transition = Resolve(Ledger, operation);
            return new ConditionHistoryTransition(new ConditionHistory(journal, transition.State), transition);
        }
        public static ConditionStamp Stamp(EffectClockMarker marker) => new ConditionStamp(marker.Time, marker.Phase);
        private static EffectClockMarker Marker(ConditionStamp stamp) => new EffectClockMarker(stamp.Time, stamp.Phase);
        private static EffectClockMarker? Marker(ConditionStamp? stamp) => stamp.HasValue ? Marker(stamp.Value) : (EffectClockMarker?)null;
        private static ConditionKind Kind(string name)
        {
            if (!Enum.TryParse(name, false, out ConditionKind kind) || !Enum.IsDefined(typeof(ConditionKind), kind) || kind.ToString() != name)
                throw new ArgumentException("Unsupported condition identity in journal.");
            return kind;
        }
        private static ConditionTransition Resolve(ConditionLedger ledger, ConditionOperation operation)
        {
            var at = Marker(operation.At);
            if (operation.Kind != ConditionOperationKind.Advance && !at.Equals(ledger.Now))
                throw new ArgumentException("Condition history clock mismatch.");
            switch (operation.Kind) {
                case ConditionOperationKind.Apply:
                    var a = operation.Application;
                    return ledger.Apply(new ConditionApplication(a.Id, a.Owner, a.Source, ledger.Target, Kind(a.Kind), at,
                        Marker(a.Expires), a.EndingMethod, a.GenericCureAllowed, a.ApplyingDc, a.Magnitude, a.InheritedCureAllowed), operation.Subject);
                case ConditionOperationKind.GrantImmunity:
                    var g = operation.Immunity;
                    return ledger.GrantImmunity(new ConditionImmunity(g.Id, g.Owner, g.Source, ledger.Target, g.Kinds.Select(Kind), at, Marker(g.Expires), g.EndingMethod));
                case ConditionOperationKind.Suppress: return ledger.SuppressApplication(operation.Subject, operation.Suppressed);
                case ConditionOperationKind.EndApplication: return ledger.EndApplication(operation.Subject, operation.Reason);
                case ConditionOperationKind.EndImmunity: return ledger.EndImmunity(operation.Subject, operation.Reason);
                case ConditionOperationKind.Cure: return ledger.Cure(Kind(operation.Subject));
                case ConditionOperationKind.Advance: return ledger.AdvanceTo(at);
                default: throw new ArgumentException("Unsupported condition history operation.");
            }
        }
    }
}
#endif
