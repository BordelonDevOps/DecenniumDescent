#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy : IReadStateProjectionPolicyV1
    {
        IReadStateProjectionV1 IReadStateProjectionPolicyV1.CreateReadProjection(ReadStateStampV1 stamp, Snapshot current)
            => new CurrentConditionProjectionV1(stamp, current);
    }

    /// <summary>Derived immutable ledgers, established only by the owning Simulation publisher.</summary>
    internal sealed class CurrentConditionProjectionV1 : IReadStateProjectionV1
    {
        private readonly Entry[] entries;
        private readonly EffectClockMarker currentMarker;
        public ReadStateStampV1 Stamp { get; }

        internal CurrentConditionProjectionV1(ReadStateStampV1 stamp, Snapshot current)
        {
            Stamp = stamp ?? throw new ArgumentNullException(nameof(stamp));
            currentMarker = new EffectClockMarker(current.RuleClock);
            // Consume only complete immutable journals, schema and exact clock. Other snapshot
            // children are neither materialized nor cached as permissions, life or inventory rights.
            entries = current.Conditions.Select(journal => {
                var history = ConditionHistory.Restore(journal);
                var projected = current.SchemaVersion >= Snapshot.ExpeditionRouteSchema
                    && history.Ledger.Now.CompareTo(currentMarker) < 0
                        ? history.Ledger.AdvanceTo(currentMarker).State : history.Ledger;
                return new Entry(journal, history, projected);
            }).ToArray();
        }

        internal bool Covers(Snapshot current)
            => current != null && current.Revision == Stamp.Revision && current.SchemaVersion == Stamp.SchemaVersion
                && current.WireSchemaVersion == Stamp.WireSchemaVersion && current.RuleClock == Stamp.RuleClock
                && current.ContentFingerprint == Stamp.ContentFingerprint && current.TestOnly == Stamp.TestOnly
                && current.Conditions.Length == entries.Length
                && current.Conditions.Select((journal, index) => ReferenceEquals(journal, entries[index].Journal)).All(x => x);

        internal ConditionHistory Read(ConditionJournal journal)
            => Find(journal).History;

        internal ConditionLedger Project(ConditionJournal journal, bool project, EffectClockMarker marker)
        {
            var entry = Find(journal);
            if (!project) return entry.History.Ledger;
            if (!marker.Equals(currentMarker) || Stamp.SchemaVersion < Snapshot.ExpeditionRouteSchema)
                throw new InvalidOperationException("The owning condition projection does not cover this marker or mode.");
            return entry.Projected;
        }

        private Entry Find(ConditionJournal journal)
            => entries.SingleOrDefault(x => ReferenceEquals(x.Journal, journal))
                ?? throw new InvalidOperationException("The owning condition projection does not cover this journal.");

        private sealed class Entry
        {
            internal readonly ConditionJournal Journal;
            internal readonly ConditionHistory History;
            internal readonly ConditionLedger Projected;
            internal Entry(ConditionJournal journal, ConditionHistory history, ConditionLedger projected)
            { Journal = journal; History = history; Projected = projected; }
        }
    }
}
#endif
