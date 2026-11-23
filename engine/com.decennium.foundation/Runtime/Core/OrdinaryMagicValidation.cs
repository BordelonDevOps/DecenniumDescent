using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static partial class OrdinaryMagicProfile
    {
        internal static void Validate(Snapshot s)
        {
            var record = s.OrdinaryMagic;
            if ((record != null) != SelectedFingerprint(s.ContentFingerprint)) throw new ArgumentException("Ordinary-magic envelope mismatch.");
            if (record == null) return;
            if (!s.TestOnly || s.Consecration == null || s.ContentFingerprint != BindFingerprint(record.PredecessorFingerprint)
                || record.PredecessorFingerprint != ConsecrationProfile.BindFingerprint(s.Consecration.PredecessorFingerprint)
                || s.CastingTurnEnds.Length != 0)
                throw new ArgumentException("Invalid ordinary-magic source composition or legacy End mixing.");
            var ordinals = record.Segments.Select(x => x.Ordinal).Concat(record.Activities.Select(x => x.Ordinal))
                .Concat(record.Settlements.Select(x => x.Ordinal)).Concat(record.ZeroIdleRanges.Select(x => x.Ordinal))
                .Concat(record.Transitions.Select(x => x.Ordinal)).ToArray();
            if (ordinals.Distinct().Count() != ordinals.Length || ordinals.Any(x => x >= record.NextOrdinal))
                throw new ArgumentException("Duplicate or unprocessed magical event ordinal.");
            if (record.NextOrdinal != ordinals.LongLength + 1 || ordinals.OrderBy(x => x).Where((x, i) => x != i + 1L).Any())
                throw new ArgumentException("Missing magical calendar event ordinal.");
            if (record.Current == null) {
                if (ordinals.Length != 0 || record.NextOrdinal != 1 || s.Reinforcement?.Admission != null)
                    throw new ArgumentException("Missing admitted magical allowance.");
                return;
            }
            var open = record.Segments.Where(x => !x.Closed).ToArray();
            var current = record.Current;
            if (open.Length != 1 || open[0].Ordinal != current.SegmentOrdinal || !SameOrigin(open[0].Origin, current.Origin)
                || open[0].ContextEpoch != current.ContextEpoch || open[0].InInitiative != current.InInitiative
                || current.ContextEpoch != WorldTiming.ForActor(s, ClericRpProfile.Actor)?.Id || current.InInitiative != s.InventoryCombat)
                throw new ArgumentException("Invalid current magical segment.");
            if (current.Origin != null) {
                var epoch = WorldTiming.FindEpoch(s, current.Origin.EpochId);
                var budget = s.WorldIntervals.Single(x => x.ActorId == ClericRpProfile.Actor);
                if (epoch == null || current.OriginAt != epoch.Start(current.Origin.LocalStart)
                    || budget.LastStart != (current.ContextEpoch == current.Origin.EpochId ? current.Origin.GlobalStart : -1)
                    || current.Consumed != record.Settlements.Any(x => x.Origin.SameAs(current.Origin))
                    || !current.Consumed && (current.Deadline <= s.RuleClock || open[0].ConsumedAtOpen))
                    throw new ArgumentException("Current magical allowance differs from its real budget or settlement.");
            }
            foreach (var segment in record.Segments) {
                Event(s, segment.CauseId, segment.Revision, segment.At);
                if (segment.Origin != null) {
                    ValidateOrigin(s, segment.Origin);
                    var epoch = WorldTiming.FindEpoch(s, segment.Origin.EpochId);
                    var end = epoch.Start(segment.Origin.LocalStart + 1);
                    bool ended = segment.InInitiative && segment.ContextEpoch == epoch.Id && segment.At < end
                        && (segment.Closed ? segment.CloseAt : s.RuleClock) >= end;
                    if (epoch.Start(segment.Origin.LocalStart) > segment.At
                        || segment.ConsumedAtOpen && !record.Settlements.Any(x => x.Origin.SameAs(segment.Origin) && x.Ordinal < segment.Ordinal)
                        || ended && !record.Settlements.Any(x => x.Origin.SameAs(segment.Origin) && x.At == end
                            && x.Reason == MagicalSettlementReason.RegularEnd))
                        throw new ArgumentException("Missing real End coverage or forged magical segment openness.");
                }
                if (segment.Closed) Event(s, segment.CloseCauseId, segment.CloseRevision, segment.CloseAt);
                var context = record.Transitions.Where(x => x.Ordinal < segment.Ordinal).OrderBy(x => x.Ordinal).LastOrDefault();
                if (context == null || context.ToEpoch != segment.ContextEpoch || context.ToInitiative != segment.InInitiative
                    || !SupportedEpoch(s, segment.ContextEpoch)) throw new ArgumentException("Magical segment lacks actual context provenance.");
            }
            if (record.Activities.Select(x => x.CommandId).Distinct(StringComparer.Ordinal).Count() != record.Activities.Count
                || record.Activities.Count != s.CastingActivities.Length)
                throw new ArgumentException("Magical command-context coverage differs.");
            foreach (var activity in record.Activities) {
                var command = Event(s, activity.CommandId, activity.Revision, activity.At);
                ValidateOrigin(s, activity.Origin);
                var source = s.CastingActivities.SingleOrDefault(x => x.CommandId == activity.CommandId);
                var segment = record.Segments.SingleOrDefault(x => x.Ordinal == activity.SegmentOrdinal);
                bool consumed = record.Settlements.Any(x => x.Origin.SameAs(activity.Origin) && x.Ordinal < activity.Ordinal);
                if (source == null || source.Revision != activity.Revision || source.At != activity.At || source.Kind != activity.Kind
                    || !source.Turn.SameAs(activity.Origin) || command.Actor != ClericRpProfile.Actor
                    || segment == null || !SameOrigin(segment.Origin, activity.Origin) || segment.ContextEpoch != activity.ContextEpoch
                    || segment.InInitiative != activity.InInitiative || segment.At > activity.At
                    || segment.Closed && (activity.At > segment.CloseAt || activity.Revision > segment.CloseRevision)
                    || consumed != activity.ConsumedAtUse)
                    throw new ArgumentException("Invalid paid activity attribution.");
                var epoch = WorldTiming.FindEpoch(s, activity.ContextEpoch);
                if (activity.InInitiative && (activity.Origin.EpochId != epoch.Id || epoch.SlotAt(activity.At) != activity.Origin.LocalStart))
                    throw new ArgumentException("Initiative magic is not its actual own turn.");
            }
            if (record.Settlements.Select(x => x.Origin.Binding).Distinct(StringComparer.Ordinal).Count() != record.Settlements.Count)
                throw new ArgumentException("Repeated magical settlement opportunity.");
            foreach (var settlement in record.Settlements) {
                Event(s, settlement.CauseId, settlement.Revision, settlement.At);
                ValidateOrigin(s, settlement.Origin);
                var epoch = WorldTiming.FindEpoch(s, settlement.Origin.EpochId);
                var segment = record.Segments.SingleOrDefault(x => x.Ordinal == settlement.SegmentOrdinal);
                var activities = record.Activities.Where(x => x.Origin.SameAs(settlement.Origin) && x.Ordinal < settlement.Ordinal).ToArray();
                var deadline = epoch.Start(settlement.Origin.LocalStart).AddSeconds(6);
                if (segment == null || !SameOrigin(segment.Origin, settlement.Origin) || segment.ContextEpoch != settlement.ContextEpoch
                    || settlement.Proficiency != 2 || settlement.MagicalActivity != activities.Any(x => x.Kind != CastingActivityKind.Grounding)
                    || settlement.Grounding != activities.Any(x => x.Kind == CastingActivityKind.Grounding)
                    || settlement.Reason == MagicalSettlementReason.RegularEnd && (!segment.InInitiative
                        || segment.ContextEpoch != epoch.Id || settlement.At != epoch.Start(settlement.Origin.LocalStart + 1))
                    || settlement.Reason == MagicalSettlementReason.OutsideDeadline && settlement.At != deadline
                    || settlement.Reason == MagicalSettlementReason.ReplacementStartPartial && (settlement.At >= deadline
                        || !record.Segments.Any(x => x.Ordinal > settlement.Ordinal && x.Origin != null
                            && x.Origin.EpochId == settlement.ContextEpoch && WorldTiming.FindEpoch(s, x.Origin.EpochId).Start(x.Origin.LocalStart) == settlement.At)))
                    throw new ArgumentException("Invalid magical settlement coverage or endpoint.");
            }
            foreach (var range in record.ZeroIdleRanges) {
                Event(s, range.CauseId, range.Revision, range.Through);
                var epoch = WorldTiming.FindEpoch(s, range.EpochId);
                if (epoch == null || !SupportedEpoch(s, epoch.Id) || epoch.LatestStart(ClericRpProfile.Actor, range.FirstLocalStart) != range.FirstLocalStart
                    || epoch.LatestStart(ClericRpProfile.Actor, range.LastLocalStart) != range.LastLocalStart
                    || range.Count != (range.LastLocalStart - range.FirstLocalStart) / epoch.Order.Count + 1
                    || range.Through != epoch.Start(range.LastLocalStart).AddSeconds(6)
                    || ConsecrationProfile.CountRechargeStarts(s, epoch, ClericRpProfile.Actor, range.FirstLocalStart - 1, range.LastLocalStart) != range.Count
                    || record.Segments.Any(x => InRange(x.Origin, range)) || record.Activities.Any(x => InRange(x.Origin, range))
                    || record.Settlements.Any(x => InRange(x.Origin, range))
                    || record.ZeroIdleRanges.Any(x => x != range && x.EpochId == range.EpochId
                        && x.FirstLocalStart <= range.LastLocalStart && range.FirstLocalStart <= x.LastLocalStart))
                    throw new ArgumentException("Invalid zero-idle coverage, overlap or skipped Start.");
                var context = record.Transitions.Where(x => x.Ordinal < range.Ordinal).OrderBy(x => x.Ordinal).LastOrDefault();
                if (context == null || context.ToInitiative || context.ToEpoch != range.EpochId
                    || context.At > epoch.Start(range.FirstLocalStart)) throw new ArgumentException("Zero-idle range crosses a context boundary.");
            }
            foreach (var transition in record.Transitions) {
                Event(s, transition.CauseId, transition.Revision, transition.At);
                if (!SupportedEpoch(s, transition.ToEpoch)) throw new ArgumentException("Unsupported magical transition calendar.");
                ValidateTransitionSource(s, transition);
                var previous = record.Segments.Where(x => x.Ordinal < transition.Ordinal).OrderBy(x => x.Ordinal).LastOrDefault();
                if (previous == null ? transition.Origin != null || transition.FromEpoch != "" || transition.AdmissionCarry?.Interval.LastStart != -1
                    : !SameOrigin(previous.Origin, transition.Origin) || previous.ContextEpoch != transition.FromEpoch
                        || previous.InInitiative != transition.FromInitiative || !previous.Closed || previous.CloseAt != transition.At
                        || previous.CloseRevision != transition.Revision || previous.CloseCauseId != transition.CauseId)
                    throw new ArgumentException("Transition replaced its actual carried origin.");
                if (transition.Consumed != (transition.Origin == null || record.Settlements.Any(x =>
                    x.Origin.SameAs(transition.Origin) && x.Ordinal < transition.Ordinal)))
                    throw new ArgumentException("Transition reset a consumed opportunity.");
            }
            ValidateCoverage(s);
        }
        private static bool InRange(SpellTurnIdentity origin, MagicalZeroIdleRange range) => origin != null
            && origin.EpochId == range.EpochId && origin.LocalStart >= range.FirstLocalStart && origin.LocalStart <= range.LastLocalStart;
        private static void ValidateOrigin(Snapshot s, SpellTurnIdentity origin)
        {
            RequireOrigin(origin);
            var epoch = WorldTiming.FindEpoch(s, origin.EpochId);
            if (epoch == null || !SupportedEpoch(s, epoch.Id) || origin.LocalStart > epoch.ProcessedSlot || IsSkippedStart(s, epoch, origin.LocalStart)
                || !SpellCastingProfile.ValidTurn(s, origin, epoch.Start(origin.LocalStart), true))
                throw new ArgumentException("Magical origin is not a supported real owner marker.");
        }
        private static Command Event(Snapshot s, string cause, long revision, RuleTime at)
        {
            var receipt = s.Receipts.SingleOrDefault(x => x.Id == cause && x.Revision == revision);
            if (receipt == null || revision > s.Revision || at > s.RuleClock) throw new ArgumentException("Unattributed magical calendar event.");
            return CommandHistory.Read(receipt);
        }
        private static void ValidateTransitionSource(Snapshot s, MagicalTransitionRecord row)
        {
            ReinforcementCarry carried = null;
            if (row.FromEpoch != row.ToEpoch) {
                if (row.ToEpoch == s.Reinforcement?.Admission?.Phase.Epoch.Id) {
                    var admission = s.Reinforcement.Events.Single(x => x.Kind == ReinforcementEventKind.Admitted);
                    if (row.FromEpoch != "" || row.Origin != null || row.Revision != admission.Revision
                        || row.CauseId != admission.CommandId || row.At != admission.At) throw new ArgumentException("Invalid bootstrap carry cause.");
                    carried = s.Reinforcement.Admission.Carried.Single(x => x.Interval.ActorId == ClericRpProfile.Actor);
                } else if (PostRecoveryProfile.IsEpoch(s, row.ToEpoch)) {
                    var entry = s.PostRecoveryEncounter.Entered;
                    if (row.Revision != entry.Revision || row.CauseId != entry.CommandId || row.At != entry.At
                        || row.FromEpoch != s.PostRecoveryEncounter.Admission.PreviousPartyEpochId) throw new ArgumentException("Invalid recovery carry cause.");
                    carried = s.PostRecoveryEncounter.Admission.PartyCarried.Single(x => x.Interval.ActorId == ClericRpProfile.Actor);
                } else if (FerryWraithProfile.IsEpoch(s, row.ToEpoch)) {
                    var entry = s.FerryWraith.Entered;
                    if (row.Revision != entry.Revision || row.CauseId != entry.CommandId || row.At != entry.At
                        || row.FromEpoch != s.FerryWraith.Admission.PreviousPartyEpochId) throw new ArgumentException("Invalid Ferry carry cause.");
                    carried = s.FerryWraith.Admission.PartyCarried.Single(x => x.Interval.ActorId == ClericRpProfile.Actor);
                }
                if (!row.ToInitiative || carried == null || row.AdmissionCarry == null || !SameBudget(row.AdmissionCarry.Interval, carried.Interval)
                    || row.AdmissionCarry.BonusActionAvailable != carried.BonusActionAvailable) throw new ArgumentException("Admission changed its actual carried budget.");
            } else if (row.ToInitiative) {
                var entry = s.Reengagement?.Entry;
                if (row.FromInitiative || entry == null || entry.ArrivalRevision != row.Revision
                    || entry.ArrivalCommandId != row.CauseId || entry.At != row.At) throw new ArgumentException("Invalid magical re-entry context.");
            } else if (!row.FromInitiative || !s.ClosedEncounters.Any(x => x.ClosedRevision == row.Revision && x.Reason == row.CauseId && x.ClosedAt == row.At))
                throw new ArgumentException("Magical outside context lacks actual closure.");
        }
        private static bool SameBudget(WorldIntervalRecord left, WorldIntervalRecord right)
            => left.ActorId == right.ActorId && left.LastStart == right.LastStart && left.MovementSpent == right.MovementSpent
                && left.ActionSpent == right.ActionSpent && left.DashPaid == right.DashPaid
                && left.ReactionAvailable == right.ReactionAvailable && left.Interactions == right.Interactions;
    }
}
