using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static partial class OrdinaryMagicProfile
    {
        private static long AfterSkipped(Snapshot s, WorldScheduleRecord epoch, long local)
            => IsSkippedStart(s, epoch, local) ? checked(local + epoch.Order.Count) : local;

        // Prove complete coverage, not just the internal validity of rows that survived.
        // Actual context changes split segments; only unchanged zero-idle intervals may
        // occupy the gap between consecutive explicitly represented owner Starts.
        private static void ValidateCoverage(Snapshot s)
        {
            var record = s.OrdinaryMagic;
            var segments = record.Segments.OrderBy(x => x.Ordinal).ToArray();
            var events = record.Segments.Select(x => (ordinal: x.Ordinal, at: x.At, revision: x.Revision))
                .Concat(record.Activities.Select(x => (ordinal: x.Ordinal, at: x.At, revision: x.Revision)))
                .Concat(record.Settlements.Select(x => (ordinal: x.Ordinal, at: x.At, revision: x.Revision)))
                .Concat(record.ZeroIdleRanges.Select(x => (ordinal: x.Ordinal, at: x.Through, revision: x.Revision)))
                .Concat(record.Transitions.Select(x => (ordinal: x.Ordinal, at: x.At, revision: x.Revision)))
                .OrderBy(x => x.ordinal).ToArray();
            if (events.Skip(1).Where((x, i) => x.at < events[i].at || x.revision < events[i].revision).Any())
                throw new ArgumentException("Magical event order contradicts actual time or command order.");
            long SegmentLimit(long ordinal) => record.Segments.Select(x => x.Ordinal)
                .Concat(record.Transitions.Select(x => x.Ordinal)).Concat(record.ZeroIdleRanges.Select(x => x.Ordinal))
                .Where(x => x > ordinal).DefaultIfEmpty(record.NextOrdinal).Min();
            if (record.Activities.Any(x => x.Ordinal >= SegmentLimit(x.SegmentOrdinal))
                || record.Settlements.Any(x => x.Ordinal >= SegmentLimit(x.SegmentOrdinal)))
                throw new ArgumentException("Magical event follows its segment's actual closing phase.");
            var usedRanges = new System.Collections.Generic.HashSet<long>();
            for (int i = 0; i < segments.Length; i++) {
                var segment = segments[i];
                var previous = i == 0 ? null : segments[i - 1];
                var transition = record.Transitions.SingleOrDefault(x => x.Ordinal == segment.Ordinal - 1);
                if (transition != null) {
                    if (!SameOrigin(segment.Origin, transition.Origin) || segment.ContextEpoch != transition.ToEpoch
                        || segment.InInitiative != transition.ToInitiative || segment.ConsumedAtOpen != transition.Consumed
                        || segment.CauseId != transition.CauseId || segment.Revision != transition.Revision || segment.At != transition.At
                        || previous != null && (!previous.Closed || previous.CloseAt != segment.At
                            || previous.CloseRevision != segment.Revision || previous.CloseCauseId != segment.CauseId))
                        throw new ArgumentException("Magical context segment changed its carried allowance.");
                } else {
                    if (previous == null || !previous.Closed || segment.Origin == null || SameOrigin(previous.Origin, segment.Origin)
                        || segment.ContextEpoch != previous.ContextEpoch || segment.InInitiative != previous.InInitiative
                        || segment.Origin.EpochId != segment.ContextEpoch || segment.ConsumedAtOpen
                        || segment.CauseId != previous.CloseCauseId || segment.Revision != previous.CloseRevision)
                        throw new ArgumentException("Magical Start has no contiguous predecessor.");
                    var epoch = WorldTiming.FindEpoch(s, segment.ContextEpoch);
                    bool sameEpoch = previous.Origin?.EpochId == epoch.Id;
                    long first = AfterSkipped(s, epoch, sameEpoch
                        ? checked(previous.Origin.LocalStart + epoch.Order.Count) : FirstOwnerStart(epoch));
                    if (segment.At != epoch.Start(segment.Origin.LocalStart) || previous.CloseAt != epoch.Start(first)
                        || first > segment.Origin.LocalStart || !sameEpoch && first != segment.Origin.LocalStart)
                        throw new ArgumentException("Magical Start skipped its actual replacement boundary.");
                    var ranges = record.ZeroIdleRanges.Where(x => x.Ordinal > previous.Ordinal && x.Ordinal < segment.Ordinal)
                        .OrderBy(x => x.Ordinal).ToArray();
                    long expected = first;
                    foreach (var range in ranges) {
                        if (previous.InInitiative || range.EpochId != epoch.Id || range.FirstLocalStart != expected
                            || range.LastLocalStart >= segment.Origin.LocalStart || range.CauseId != segment.CauseId
                            || range.Revision != segment.Revision || !usedRanges.Add(range.Ordinal))
                            throw new ArgumentException("Magical zero-idle range leaves a gap or crosses a Start.");
                        expected = AfterSkipped(s, epoch, checked(range.LastLocalStart + epoch.Order.Count));
                    }
                    if (expected != segment.Origin.LocalStart)
                        throw new ArgumentException("Missing actual owner-Start coverage.");
                    if (previous.Origin != null && !record.Settlements.Any(x => x.Origin.SameAs(previous.Origin)
                        && x.Ordinal < segment.Ordinal && x.At <= segment.At))
                        throw new ArgumentException("Replaced magical opportunity has no settlement.");
                }
                if (i == 0 && (transition == null || transition.Ordinal != 1 || segment.Origin != null))
                    throw new ArgumentException("Magical history lacks its actual bootstrap context.");
                if (segment.Origin != null) {
                    bool consumedBefore = record.Settlements.Any(x => x.Origin.SameAs(segment.Origin) && x.Ordinal < segment.Ordinal);
                    if (segment.ConsumedAtOpen != consumedBefore) throw new ArgumentException("Magical segment openness differs from history.");
                }
            }
            if (usedRanges.Count != record.ZeroIdleRanges.Count) throw new ArgumentException("Unattached magical zero-idle range.");

            var current = record.Current;
            var currentEpoch = WorldTiming.FindEpoch(s, current.ContextEpoch);
            long last = currentEpoch.LatestStart(ClericRpProfile.Actor, currentEpoch.ProcessedSlot);
            if (IsSkippedStart(s, currentEpoch, last)) last -= currentEpoch.Order.Count;
            if (last >= 0 ? current.Origin == null || current.Origin.EpochId != currentEpoch.Id || current.Origin.LocalStart != last
                : current.Origin?.EpochId == currentEpoch.Id)
                throw new ArgumentException("Magical current origin is not the latest actual processed supply.");

            foreach (var settlement in record.Settlements) {
                var segment = segments.Single(x => x.Ordinal == settlement.SegmentOrdinal);
                if (settlement.At < segment.At || settlement.Revision < segment.Revision
                    || segment.Closed && (settlement.At > segment.CloseAt || settlement.Revision > segment.CloseRevision))
                    throw new ArgumentException("Magical settlement lies outside its real segment.");
            }

            var mutations = s.SpellCasts.Select(x => (at: x.At, revision: x.Revision, after: x.DissonanceAfter, phase: 0))
                .Concat(record.Settlements.Select(x => (at: x.At, revision: x.Revision, after: x.After, phase: 0)))
                .Concat(BishopProfile.Invocations(s).Select(x => (at: x.At, revision: x.Revision, after: x.DissonanceAfter, phase: 0)))
                .Concat(s.ClericLongRestSettlements.Select(x => (at: x.At, revision: x.Revision, after: x.DissonanceAfter, phase: 1)))
                .OrderBy(x => x.at).ThenBy(x => x.revision).ThenBy(x => x.phase).ToArray();
            foreach (var range in record.ZeroIdleRanges) {
                var start = WorldTiming.FindEpoch(s, range.EpochId).Start(range.FirstLocalStart);
                var prior = mutations.Where(x => x.at <= start && x.revision <= range.Revision).ToArray();
                if (prior.Length != 0 && prior.Last().after != 0 || mutations.Any(x => x.at > start && x.at < range.Through))
                    throw new ArgumentException("Zero-idle range hides nonzero strain or an intervening mutation.");
            }
        }
    }
}
