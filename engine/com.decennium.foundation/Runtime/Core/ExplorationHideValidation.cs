using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static class ExplorationHideValidation
    {
        public static void Validate(Snapshot state)
        {
            var hide = state.ExplorationHide;
            bool selected = state.ContentFingerprint.StartsWith(ExplorationHideDefinition.FingerprintPrefix, StringComparison.Ordinal);
            if ((hide != null) != selected)
                throw new ArgumentException("Ordinary Hide fingerprint and private component must agree.");
            if (hide == null) {
                if (state.ExplorationSearch != null && state.Receipts.Any(x => CommandHistory.Read(x).Kind == CommandKind.CancelExplorationHide))
                    throw new ArgumentException("Ordinary Hide cancellation requires wire92.");
                return;
            }
            var search = state.ExplorationSearch;
            var d = hide.Definition;
            var schedule = state.WorldSchedule;
            if (search == null || !state.TestOnly || state.SchemaVersion != Snapshot.ObservationSchema
                || schedule == null || !schedule.Order.Contains(d.HiderId)
                || !state.ObservationProfiles.Any(x => x.ActorId == d.WitnessId)
                || d.WitnessId == search.Definition.SearcherId || d.HiderId != search.Definition.ConcealedActorId
                || !d.Recess.Equals(search.Definition.CueCandidate)
                || new[] { d.Recess, d.Alternate }.Any(x => x.X >= state.ObservationMapWidth || x.Y >= state.ObservationMapHeight
                    || state.ObservationCells.Any(c => c.X == x.X && c.Y == x.Y)))
                throw new ArgumentException("Invalid wire92 Hide authority or layout.");

            ValidateRelocation(state, d, hide.LatestRelocation);
            foreach (var attempt in hide.Attempts) {
                var cause = ReadReceipt(state, attempt.Revision, attempt.CommandId);
                if (cause?.Kind != CommandKind.Hide || cause.Actor != d.HiderId || cause.X != 0 || cause.Y != 0
                    || cause.Target != schedule.MarkerId(attempt.PaidStart) || attempt.CalendarId != schedule.Id
                    || schedule.LatestStart(d.HiderId, attempt.PaidStart) != attempt.PaidStart
                    || attempt.StartedAt != schedule.Start(attempt.PaidStart) || attempt.StartedAt > state.RuleClock
                    || attempt.DueAt != schedule.Start(checked(attempt.PaidStart + schedule.Order.Count))
                    || !d.Allows(attempt.Anchor))
                    throw new ArgumentException("Ordinary Hide declaration or scheduled payment lacks its committed provenance.");
                ValidateRelocation(state, d, attempt.Relocation);
                if (attempt.End != null) ValidateEnd(state, d, attempt);
            }

            var interval = state.WorldIntervals.Single(x => x.ActorId == d.HiderId);
            var livePayment = hide.Attempts.LastOrDefault(x => x.PaidStart == interval.LastStart);
            if (livePayment != null && (!interval.ActionSpent || interval.DashPaid))
                throw new ArgumentException("Ordinary Hide lost the paid scheduled Action before refresh.");
            var pending = hide.Pending;
            if (pending != null) {
                var position = WorldPositionResolver.Position(state, d.HiderId);
                if (state.InventoryCombat || state.RuleClock > pending.DueAt
                    || state.RuleClock == pending.DueAt && state.ManufacturingAdvance == null
                    || state.RuleClock < pending.DueAt && livePayment != pending
                    || state.WorldTraversals.Any(x => x.ActorId == d.HiderId)
                    || position.X != new RuleQuantity(pending.Anchor.X) || position.Y != new RuleQuantity(pending.Anchor.Y))
                    throw new ArgumentException("Pending ordinary Hide lost its stationary paid interval.");
            }
        }

        private static void ValidateRelocation(Snapshot state, ExplorationHideDefinition d, ExplorationHideRelocation relocation)
        {
            if (relocation == null) return;
            var departure = ReadReceipt(state, relocation.StartedRevision);
            var arrival = ReadReceipt(state, relocation.ArrivedRevision, relocation.ArrivalCommandId);
            if (!d.Allows(relocation.From) || !d.Allows(relocation.To) || relocation.At > state.RuleClock
                || departure?.Kind != CommandKind.BeginWorldStep || departure.Actor != d.HiderId
                || departure.Target != "walk" && departure.Target != "run"
                || departure.X != relocation.To.X - relocation.From.X || departure.Y != relocation.To.Y - relocation.From.Y
                || arrival?.Kind != CommandKind.AdvanceClock)
                throw new ArgumentException("Ordinary Hide has no actual alternate-position movement authority.");
        }

        private static Command ReadReceipt(Snapshot state, long revision, string id = null)
        {
            var receipt = state.Receipts.SingleOrDefault(x => x.Revision == revision && (id == null || x.Id == id));
            return receipt == null ? null : CommandHistory.Read(receipt);
        }

        public static ObservationActionRecord UnchangedFailure(Snapshot state, ExplorationHideAttempt attempt,
            string observer, long beforeRevision)
        {
            string hider = state.ExplorationHide.Definition.HiderId;
            var prior = state.ObservationActions.Where(x => x.ActorId == hider && x.Revision < beforeRevision
                    && x.Kind == ObservationActionKind.Hide && x.Outcome == ObservationActionOutcome.HideAttempted)
                .OrderByDescending(x => x.Revision)
                .Select(x => (Action: x, Comparison: state.ObservationHideResults
                    .SingleOrDefault(r => r.AttemptId == x.Id && r.ObserverId == observer)))
                .FirstOrDefault(x => x.Comparison != null);
            if (prior.Comparison == null || prior.Comparison.HiddenEstablished) return null;
            var move = attempt.Relocation;
            bool changed = move != null && move.StartedRevision > prior.Action.Revision && move.At > prior.Action.At
                && prior.Action.X == new RuleQuantity(move.From.X) && prior.Action.Y == new RuleQuantity(move.From.Y);
            return changed ? null : prior.Action;
        }

        private static void ValidateEnd(Snapshot state, ExplorationHideDefinition d, ExplorationHideAttempt attempt)
        {
            var end = attempt.End;
            var cause = ReadReceipt(state, end.Revision, end.CommandId);
            if (cause == null || end.At > state.RuleClock || end.Status == ExplorationHideStatus.Cancelled
                && (cause.Kind != CommandKind.CancelExplorationHide || cause.Actor != d.HiderId || cause.Target != attempt.Id))
                throw new ArgumentException("Ordinary Hide terminal receipt lacks its authority.");

            var recorded = state.ObservationActions.SingleOrDefault(x => x.Kind == ObservationActionKind.Hide
                && x.ActorId == d.HiderId && x.Revision == end.Revision);
            if (end.ObservationId == "") {
                if (recorded != null)
                    throw new ArgumentException("An unrolled ordinary Hide cannot have an observation check.");
            } else if (recorded == null || recorded.Id != end.ObservationId || recorded.At != end.At
                || recorded.X != new RuleQuantity(attempt.Anchor.X) || recorded.Y != new RuleQuantity(attempt.Anchor.Y)
                || recorded.Outcome != ObservationActionOutcome.HideAttempted) {
                throw new ArgumentException("Ordinary Hide result lacks its paid terminal provenance.");
            }

            string searcher = state.ExplorationSearch.Definition.SearcherId;
            var eligible = new[] { searcher, d.WitnessId }.Where(x => end.EligibleObservers.HasFlag(
                x == searcher ? ExplorationHideObservers.Searcher : ExplorationHideObservers.Witness)).ToArray();
            var failure = eligible.Select(x => (Observer: x, Prior: UnchangedFailure(state, attempt, x, end.Revision)))
                .Where(x => x.Prior != null).OrderBy(x => x.Observer, StringComparer.Ordinal).FirstOrDefault();
            if (end.NoRoll == ExplorationHideNoRoll.UnchangedFailure) {
                if (failure.Prior?.Id != end.PriorFailureId || failure.Observer != end.PriorFailureObserverId)
                    throw new ArgumentException("Ordinary Hide suppressed retry lacks its prior failed comparison.");
            } else if (failure.Prior != null) {
                throw new ArgumentException("Ordinary Hide rerolled a materially unchanged failed comparison.");
            }
            if (recorded == null) return;

            if (recorded.Selection != ObservationDieSelection.Normal && recorded.Selection != ObservationDieSelection.Disadvantage)
                throw new ArgumentException("Invalid ordinary Hide die selection.");
            var results = state.ObservationHideResults.Where(x => x.AttemptId == recorded.Id).ToArray();
            if (!eligible.OrderBy(x => x, StringComparer.Ordinal).SequenceEqual(results.Select(x => x.ObserverId).OrderBy(x => x, StringComparer.Ordinal)))
                throw new ArgumentException("Ordinary Hide results differ from their private eligibility.");

            var search = state.ExplorationSearch.Attempts.SingleOrDefault(x => x.End?.Revision == end.Revision
                && x.End.Status == ExplorationSearchStatus.Completed);
            if (search != null) {
                var found = state.ObservationActions.Single(x => x.Id == search.End.ObservationId);
                bool hideFirst = attempt.Revision < search.Revision;
                var first = hideFirst ? recorded : found;
                var second = hideFirst ? found : recorded;
                if (end.CommandId != search.End.CommandId || end.At != search.End.At
                    || first.RandomAfter != second.RandomBefore
                    || Array.IndexOf(state.ObservationActions, first) >= Array.IndexOf(state.ObservationActions, second))
                    throw new ArgumentException("Coincident ordinary Hide and Search must use declaration receipt order.");
            }
        }

        public static bool PrecedesSearchAtSameBoundary(Snapshot state, ObservationActionRecord hide, ExplorationSearchAttempt search)
        {
            var prior = state.ExplorationHide?.Attempts.SingleOrDefault(x => x.End?.ObservationId == hide.Id);
            if (prior == null || prior.Revision >= search.Revision || prior.End.Revision != search.End.Revision
                || prior.End.CommandId != search.End.CommandId || prior.End.At != search.End.At)
                return false;
            var result = state.ObservationActions.SingleOrDefault(x => x.Id == search.End.ObservationId);
            return result != null && result.RandomBefore == hide.RandomAfter;
        }
    }
}
