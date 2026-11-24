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
        public ConditionHistory(string target, EffectClockMarker origin = default, bool relationships = false)
            : this(new ConditionJournal(relationships ? ConditionJournal.RelationshipPolicyId : PolicyId, target, Stamp(origin)),
                  new ConditionLedger(target, origin)) { }
        public static ConditionHistory Restore(ConditionJournal journal)
        {
            ConditionResolutionScope.RequireLifecycleAllowed();
            if (journal == null) throw new ArgumentNullException(nameof(journal));
            bool relationships = journal.PolicyId == ConditionJournal.RelationshipPolicyId;
            if (journal.PolicyId != PolicyId && !relationships) throw new ArgumentException("Unsupported condition interpretation policy.");
            var ledger = new ConditionLedger(journal.Target, Marker(journal.Origin));
            foreach (var operation in journal.Operations) ledger = Resolve(ledger, operation, relationships).State;
            return new ConditionHistory(journal, ledger);
        }
        public ConditionHistoryTransition Append(ConditionOperation operation)
        {
            ConditionResolutionScope.RequireLifecycleAllowed();
            // Validate chronology, identity and capacity before returning any new state.
            var journal = Journal.Append(operation);
            var transition = Resolve(Ledger, operation, Journal.PolicyId == ConditionJournal.RelationshipPolicyId);
            return new ConditionHistoryTransition(new ConditionHistory(journal, transition.State), transition);
        }
        public static ConditionStamp Stamp(EffectClockMarker marker) => new ConditionStamp(marker.Time, marker.Phase);
        private static EffectClockMarker Marker(ConditionStamp stamp) => new EffectClockMarker(stamp.Time, stamp.Phase);
        private static EffectClockMarker? Marker(ConditionStamp? stamp) => stamp.HasValue ? Marker(stamp.Value) : (EffectClockMarker?)null;
        private static ConditionKind Kind(string name, bool relationships)
        {
            if (!Enum.TryParse(name, false, out ConditionKind kind) || !Enum.IsDefined(typeof(ConditionKind), kind) || kind.ToString() != name
                || !relationships && kind == ConditionKind.Frightened)
                throw new ArgumentException("Unsupported condition identity in journal.");
            return kind;
        }
        private static ConditionTransition Resolve(ConditionLedger ledger, ConditionOperation operation, bool relationships)
        {
            var at = Marker(operation.At);
            if (operation.Kind != ConditionOperationKind.Advance && !at.Equals(ledger.Now))
                throw new ArgumentException("Condition history clock mismatch.");
            switch (operation.Kind) {
                case ConditionOperationKind.Apply:
                    var a = operation.Application;
                    if (!relationships && a.Fear != null) throw new ArgumentException("Legacy policy does not admit relationships.");
                    return ledger.Apply(new ConditionApplication(a.Id, a.Owner, a.Source, ledger.Target, Kind(a.Kind, relationships), at,
                        Marker(a.Expires), a.EndingMethod, a.GenericCureAllowed, a.ApplyingDc, a.Magnitude, a.InheritedCureAllowed, a.Fear), operation.Subject);
                case ConditionOperationKind.GrantImmunity:
                    var g = operation.Immunity;
                    return ledger.GrantImmunity(new ConditionImmunity(g.Id, g.Owner, g.Source, ledger.Target,
                        g.Kinds.Select(x => Kind(x, relationships)), at, Marker(g.Expires), g.EndingMethod, relationships));
                case ConditionOperationKind.Suppress: return ledger.SuppressApplication(operation.Subject, operation.Suppressed);
                case ConditionOperationKind.EndApplication: return ledger.EndApplication(operation.Subject, operation.Reason);
                case ConditionOperationKind.EndImmunity: return ledger.EndImmunity(operation.Subject, operation.Reason);
                case ConditionOperationKind.Cure: return ledger.Cure(Kind(operation.Subject, relationships));
                case ConditionOperationKind.Advance: return ledger.AdvanceTo(at);
                default: throw new ArgumentException("Unsupported condition history operation.");
            }
        }
    }

    /// <summary>Reuses immutable condition calculations only inside one synchronous resolver pass.</summary>
    internal sealed class ConditionResolutionScope : IDisposable
    {
        [ThreadStatic] private static ConditionResolutionScope current;
        private readonly ConditionResolutionScope previous;
        private readonly Dictionary<ConditionJournal, Entry> entries;
        private readonly NativeReadContextV1 readContext;
        private readonly Snapshot readSnapshot;
        private readonly CurrentConditionProjectionV1 readProjection;
        private bool readDisposed;

        private ConditionResolutionScope(bool reuse)
        {
            if (current?.readContext != null)
                throw new InvalidOperationException("A V1 condition read cannot enter a lifecycle resolution scope.");
            previous = current;
            if (reuse) entries = new Dictionary<ConditionJournal, Entry>(JournalIdentity.Instance);
            current = reuse ? this : null;
        }

        internal static ConditionResolutionScope Enter(bool reuse)
            => reuse || current != null ? new ConditionResolutionScope(reuse) : null;

        private ConditionResolutionScope(NativeReadContextV1 context, Snapshot snapshot)
        {
            if (context?.IsBoundTo(snapshot) != true || !(context.Projection is CurrentConditionProjectionV1 projection)
                || !projection.Covers(snapshot))
                throw new InvalidOperationException("A current owning condition projection is required.");
            previous = current;
            readContext = context;
            readSnapshot = snapshot;
            readProjection = projection;
            current = this;
        }

        internal static ConditionResolutionScope EnterRead(NativeReadContextV1 context, Snapshot snapshot)
            => new ConditionResolutionScope(context, snapshot);

        internal static void RequireReadSnapshot(Snapshot snapshot)
        {
            if (current?.readContext != null && (current.readContext.IsBoundTo(snapshot) != true
                || !current.readProjection.Covers(snapshot)))
                throw new InvalidOperationException("A condition read belongs to a different snapshot or generation.");
        }

        internal static void RequireLifecycleAllowed()
        {
            NativeReadInspectionV1.RequireExecution(NativeReadOperationV1.ConditionLifecycle);
            if (current?.readContext != null)
                throw new InvalidOperationException("Condition lifecycle execution is forbidden during a V1 read.");
        }

        private void RequireCurrentRead()
        {
            if (!readContext.IsBoundTo(readSnapshot) || !readProjection.Covers(readSnapshot))
                throw new InvalidOperationException("The owning condition read context is unavailable.");
        }

        public void Dispose()
        {
            if (readContext != null && readDisposed) return;
            if ((readContext != null || current?.readContext != null) && !ReferenceEquals(current, this))
                throw new InvalidOperationException("V1 condition scopes must be disposed in nesting order.");
            if (readContext != null) readDisposed = true;
            current = previous;
            entries?.Clear();
        }

        internal static ConditionHistory Read(ConditionJournal journal)
        {
            if (current?.readContext != null) {
                current.RequireCurrentRead();
                return current.readProjection.Read(journal);
            }
            return current == null || journal == null ? ConditionHistory.Restore(journal) : current.Get(journal).History;
        }

        internal static ConditionLedger Project(ConditionJournal journal, bool project, EffectClockMarker marker)
        {
            if (current?.readContext != null) {
                current.RequireCurrentRead();
                return current.readProjection.Project(journal, project, marker);
            }
            if (!project) return Read(journal).Ledger;
            if (current == null || journal == null) return At(ConditionHistory.Restore(journal).Ledger, marker);
            var entry = current.Get(journal);
            if (entry.Projection == null || !entry.Marker.Equals(marker)) {
                entry.Projection = At(entry.History.Ledger, marker);
                entry.Marker = marker;
            }
            return entry.Projection;
        }

        private static ConditionLedger At(ConditionLedger ledger, EffectClockMarker marker)
            => ledger.Now.CompareTo(marker) < 0 ? ledger.AdvanceTo(marker).State : ledger;

        private Entry Get(ConditionJournal journal)
        {
            if (entries.TryGetValue(journal, out var entry)) return entry;
            entry = new Entry(ConditionHistory.Restore(journal));
            // Keep the scope bounded even if a command produces many replacement journals.
            if (entries.Count == 32) entries.Clear();
            entries.Add(journal, entry);
            return entry;
        }

        private sealed class Entry
        {
            internal readonly ConditionHistory History;
            internal EffectClockMarker Marker;
            internal ConditionLedger Projection;

            internal Entry(ConditionHistory history) { History = history; }
        }

        private sealed class JournalIdentity : IEqualityComparer<ConditionJournal>
        {
            internal static readonly JournalIdentity Instance = new JournalIdentity();
            public bool Equals(ConditionJournal first, ConditionJournal second) => ReferenceEquals(first, second);
            public int GetHashCode(ConditionJournal journal) => System.Runtime.CompilerServices.RuntimeHelpers.GetHashCode(journal);
        }
    }
}
#endif
