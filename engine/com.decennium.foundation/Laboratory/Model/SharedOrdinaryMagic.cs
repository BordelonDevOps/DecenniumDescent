#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private MagicalActivityCalendarRecord ordinaryMagicDeclaration;
        internal TestOnlySharedWorldPolicy EnableOrdinaryMagicalActivity()
        {
            if (initializationStarted || consecrationDeclaration == null || ordinaryMagicDeclaration != null)
                throw new InvalidOperationException("Select ordinary magical activity once on a fresh Consecration expedition.");
            ordinaryMagicDeclaration = new MagicalActivityCalendarRecord(ContentFingerprint);
            ContentFingerprint = OrdinaryMagicProfile.BindFingerprint(ContentFingerprint);
            return this;
        }
        private static SpellTurnIdentity CurrentMagicalActionOrigin(Snapshot s, string actor)
            => s.OrdinaryMagic == null ? CurrentCastingTurn(s, actor)
                : actor == ClericRpProfile.Actor ? s.OrdinaryMagic.Current?.Origin : null;

        private static string AssessMagicalActivityContext(Snapshot s, string actor)
        {
            string failure = OrdinaryMagicProfile.ContextFailure(s, actor);
            if (failure != null) return failure;
            var record = s.OrdinaryMagic;
            return record.Activities.Count >= SpellCastingProfile.MaxActivities
                || record.Segments.Count >= MagicalActivityCalendarRecord.MaxRows - 4
                || record.Settlements.Count >= MagicalActivityCalendarRecord.MaxRows - 4
                || record.Transitions.Count >= MagicalActivityCalendarRecord.MaxRows - 4
                || record.ZeroIdleRanges.Count >= MagicalActivityCalendarRecord.MaxRows - 4 ? "MagicalAccountingHistoryFull" : null;
        }
        private static void CloseMagicalSegment(Snapshot s, Command cause, RuleTime at)
        {
            var record = s.OrdinaryMagic;
            if (record?.Current == null) return;
            var current = record.Segments.Single(x => x.Ordinal == record.Current.SegmentOrdinal);
            s.OrdinaryMagic = record.With(record.NextOrdinal, record.Current, segments: record.Segments.Select(x =>
                x == current ? current.Close(cause.Id, s.Revision + 1, at) : x));
        }
        private static void ChangeMagicalContext(Snapshot s, WorldScheduleRecord epoch, bool initiative, Command cause)
        {
            if (s.OrdinaryMagic == null || !OrdinaryMagicProfile.SupportedEpoch(s, epoch?.Id)) return;
            var old = s.OrdinaryMagic.Current;
            if (old != null && old.ContextEpoch == epoch.Id && old.InInitiative == initiative) return;
            if (cause == null) throw new ArgumentException("Magical context requires its actual transition command.");
            var carried = Interval(s, ClericRpProfile.Actor);
            bool bonus = s.BonusActions.Single(x => x.ActorId == ClericRpProfile.Actor).Available;
            CloseMagicalSegment(s, cause, s.RuleClock);
            var record = s.OrdinaryMagic;
            long ordinal = record.NextOrdinal;
            var transition = new MagicalTransitionRecord(ordinal, cause.Id, s.Revision + 1, s.RuleClock,
                old?.Origin, old?.ContextEpoch ?? "", epoch.Id, old?.InInitiative ?? false, initiative, old?.Consumed ?? true,
                old?.ContextEpoch == epoch.Id ? null : new ReinforcementCarry(carried, bonus));
            var segment = new MagicalSegmentRecord(ordinal + 1, old?.Origin, epoch.Id, initiative,
                old?.Consumed ?? true, cause.Id, s.Revision + 1, s.RuleClock);
            var current = new MagicalAllowanceRecord(old?.Origin, old?.OriginAt ?? default, old?.Deadline ?? default,
                epoch.Id, initiative, old?.Consumed ?? true, segment.Ordinal);
            s.OrdinaryMagic = record.With(ordinal + 2, current, segments: record.Segments.Append(segment),
                transitions: record.Transitions.Append(transition));
        }
        private static void SettleMagicalOpportunity(Snapshot s, Command cause, RuleTime at, MagicalSettlementReason reason)
        {
            var record = s.OrdinaryMagic;
            var current = record?.Current;
            if (current?.Origin == null || current.Consumed) return;
            if (cause == null) throw new ArgumentException("Magical settlement requires its actual advancing command.");
            var activities = record.Activities.Where(x => x.Origin.SameAs(current.Origin)).ToArray();
            bool magic = activities.Any(x => x.Kind != CastingActivityKind.Grounding);
            bool grounding = activities.Any(x => x.Kind == CastingActivityKind.Grounding);
            bool idle = reason != MagicalSettlementReason.ReplacementStartPartial;
            int pb = CharacterRuleFacts.ForActor(s, ClericRpProfile.Actor).ProficiencyBonus;
            var before = s.CastingStrain.Single(x => x.ActorId == ClericRpProfile.Actor);
            var after = before.ReduceAtSettledEnd(magic ? 0 : grounding ? pb : idle ? 1 : 0);
            var settlement = new MagicalSettlementRecord(record.NextOrdinal, current.Origin, current.SegmentOrdinal,
                current.ContextEpoch, cause.Id, s.Revision + 1, at, reason, idle, magic, grounding, pb, before.Dissonance, after.Dissonance);
            s.CastingStrain = s.CastingStrain.Select(x => x == before ? after : x).ToArray();
            s.OrdinaryMagic = record.With(record.NextOrdinal + 1, current.SetConsumed(), settlements: record.Settlements.Append(settlement));
        }
        private static void SettleOrdinaryMagicTime(Snapshot s, RuleTime from, RuleTime to, Command cause)
        {
            var current = s.OrdinaryMagic?.Current;
            if (current?.Origin == null || current.Consumed) return;
            var originEpoch = WorldTiming.FindEpoch(s, current.Origin.EpochId);
            var segment = s.OrdinaryMagic.Segments.Single(x => x.Ordinal == current.SegmentOrdinal);
            var end = originEpoch.Start(current.Origin.LocalStart + 1);
            if (current.InInitiative && current.ContextEpoch == originEpoch.Id && segment.At < end && end > from && end <= to) {
                SettleMagicalOpportunity(s, cause, end, MagicalSettlementReason.RegularEnd);
                return;
            }
            if (current.Deadline <= to) {
                if (current.Deadline < from) throw new InvalidOperationException("Unprocessed magical deadline.");
                SettleMagicalOpportunity(s, cause, current.Deadline, MagicalSettlementReason.OutsideDeadline);
            }
        }
        private static RuleTime? NextOrdinaryMagicBoundary(Snapshot s)
        {
            var record = s.OrdinaryMagic;
            var current = record?.Current;
            if (current == null) return null;
            var epoch = WorldTiming.FindEpoch(s, current.ContextEpoch);
            bool carried = current.Origin == null || current.Origin.EpochId != current.ContextEpoch;
            RuleTime? due = null;
            if (carried) {
                long first = OrdinaryMagicProfile.FirstOwnerStart(epoch);
                if (OrdinaryMagicProfile.IsSkippedStart(s, epoch, first)) first += epoch.Order.Count;
                var start = epoch.Start(first);
                if (start > s.RuleClock) due = start;
            }
            if (current.Origin == null) return due;
            if (current.Consumed) {
                // Consumption ends this opportunity, not future idle accounting. A nonzero
                // remainder must visit the next real supply before empty-range compression.
                if (!carried && s.CastingStrain.Single(x => x.ActorId == ClericRpProfile.Actor).Dissonance != 0) {
                    long next = checked(current.Origin.LocalStart + epoch.Order.Count);
                    if (OrdinaryMagicProfile.IsSkippedStart(s, epoch, next)) next += epoch.Order.Count;
                    var start = epoch.Start(next);
                    if (start > s.RuleClock && (!due.HasValue || start < due.Value)) due = start;
                }
                return due;
            }
            bool meaningful = s.CastingStrain.Single(x => x.ActorId == ClericRpProfile.Actor).Dissonance != 0
                || record.Activities.Any(x => x.Origin.SameAs(current.Origin));
            if (!carried && !current.InInitiative && !meaningful) return due;
            var boundary = current.Deadline;
            if (current.InInitiative && !carried) {
                var end = epoch.Start(current.Origin.LocalStart + 1);
                var segment = record.Segments.Single(x => x.Ordinal == current.SegmentOrdinal);
                if (end > s.RuleClock && segment.At < end) boundary = end;
            }
            if (boundary > s.RuleClock && (!due.HasValue || boundary < due.Value)) due = boundary;
            return due;
        }
        private static void RecordZeroIdleRange(Snapshot s, WorldScheduleRecord epoch, long first, long last, Command cause)
        {
            if (last < first) return;
            if (s.CastingStrain.Single(x => x.ActorId == ClericRpProfile.Actor).Dissonance != 0)
                throw new InvalidOperationException("Sparse magical range cannot hide nonzero Dissonance.");
            var phase = s.Reinforcement?.Admission?.Phase;
            var exit = s.Retreat?.SuccessfulExit;
            long skipped = epoch.Id == phase?.Epoch.Id && exit != null ? exit.EndTurn + 1L - phase.FirstTurn : -1;
            if (skipped >= first && skipped <= last && OrdinaryMagicProfile.IsSkippedStart(s, epoch, skipped)) {
                RecordZeroIdleRange(s, epoch, first, skipped - epoch.Order.Count, cause);
                RecordZeroIdleRange(s, epoch, skipped + epoch.Order.Count, last, cause);
                return;
            }
            var record = s.OrdinaryMagic;
            var range = new MagicalZeroIdleRange(record.NextOrdinal, epoch.Id, first, last,
                (last - first) / epoch.Order.Count + 1, cause.Id, s.Revision + 1, epoch.Start(last).AddSeconds(6));
            s.OrdinaryMagic = record.With(record.NextOrdinal + 1, record.Current, ranges: record.ZeroIdleRanges.Append(range));
        }
        private static void BeforeMagicalOwnerStart(Snapshot s, WorldScheduleRecord epoch, long local, Command cause, bool initiative)
        {
            if (s.OrdinaryMagic == null || epoch.Order[(int)(local % epoch.Order.Count)] != ClericRpProfile.Actor
                || !OrdinaryMagicProfile.SupportedEpoch(s, epoch.Id)) return;
            if (cause == null) throw new ArgumentException("Owner Start requires its actual advancing command.");
            var current = s.OrdinaryMagic.Current;
            if (current == null) throw new InvalidOperationException("Owner Start has no actual admission context.");
            var origin = OrdinaryMagicProfile.OriginAt(s, epoch, local);
            if (origin.SameAs(current.Origin)) return;
            if (OrdinaryMagicProfile.IsSkippedStart(s, epoch, local)) throw new InvalidOperationException("A skipped Start cannot refresh magic.");
            var at = epoch.Start(local);
            if (current.Origin != null && !current.Consumed) SettleMagicalOpportunity(s, cause,
                current.Deadline <= at ? current.Deadline : at, current.Deadline <= at
                    ? MagicalSettlementReason.OutsideDeadline : MagicalSettlementReason.ReplacementStartPartial);
            current = s.OrdinaryMagic.Current;
            bool sameEpoch = current.Origin?.EpochId == epoch.Id;
            long firstNew = sameEpoch ? checked(current.Origin.LocalStart + epoch.Order.Count) : OrdinaryMagicProfile.FirstOwnerStart(epoch);
            if (OrdinaryMagicProfile.IsSkippedStart(s, epoch, firstNew)) firstNew += epoch.Order.Count;
            if (firstNew > local || !sameEpoch && firstNew != local)
                throw new InvalidOperationException("Carried first owner Start was not processed at its actual boundary.");
            CloseMagicalSegment(s, cause, epoch.Start(firstNew));
            if (sameEpoch && local > firstNew) {
                if (current.InInitiative) throw new InvalidOperationException("Initiative cannot skip magical regular Ends.");
                RecordZeroIdleRange(s, epoch, firstNew, local - epoch.Order.Count, cause);
            }
            var record = s.OrdinaryMagic;
            var segment = new MagicalSegmentRecord(record.NextOrdinal, origin, epoch.Id, initiative, false, cause.Id, s.Revision + 1, at);
            s.OrdinaryMagic = record.With(record.NextOrdinal + 1,
                new MagicalAllowanceRecord(origin, at, at.AddSeconds(6), epoch.Id, initiative, false, segment.Ordinal),
                segments: record.Segments.Append(segment));
        }
        private static void RecordMagicalActivityContext(Snapshot s, Command c, CastingActivityKind kind)
        {
            if (s.OrdinaryMagic == null) return;
            var record = s.OrdinaryMagic;
            var current = record.Current;
            var row = new MagicalActivityContextRecord(record.NextOrdinal, c.Id, s.Revision + 1, s.RuleClock,
                current.Origin, current.SegmentOrdinal, current.ContextEpoch, current.InInitiative, current.Consumed, kind);
            s.OrdinaryMagic = record.With(record.NextOrdinal + 1, current, activities: record.Activities.Append(row));
        }
        private static bool OrdinaryMagicOldDisposition(Snapshot s, string epoch)
            => s.OrdinaryMagic?.Current?.ContextEpoch == epoch && (s.OrdinaryMagic.Current.Consumed || s.OrdinaryMagic.Current.Deadline > s.RuleClock);
    }
}
#endif
