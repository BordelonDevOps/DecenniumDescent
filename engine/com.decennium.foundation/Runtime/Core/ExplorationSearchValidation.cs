using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static class ExplorationSearchValidation
    {
        public static bool RetainsPaidIntervalAtBoundary(Snapshot state, WorldActivityIntervalRecord interval)
        {
            var search = state.ExplorationSearch;
            var pending = search?.Pending;
            return pending != null && interval.ActorId == search.Definition.SearcherId
                && interval.IntervalIndex == pending.IntervalIndex && state.RuleClock == pending.DueAt
                && state.ManufacturingAdvance != null;
        }

        public static void ValidateCommitment(Snapshot state, WorldActivityIntervalRecord interval)
        {
            var search = state.ExplorationSearch;
            if (search == null || state.WireSchemaVersion != Snapshot.ExplorationSearchSchema
                && state.WireSchemaVersion != Snapshot.ExplorationHideSchema
                && state.WireSchemaVersion != Snapshot.ConnectedExplorationObservationSchema)
                throw new ArgumentException("Search activity requires a selected ordinary Search profile.");
            if (interval.ActorId != search.Definition.SearcherId || !search.Attempts.Any(x => x.IntervalIndex == interval.IntervalIndex
                && x.CommandId == interval.ActionReference && x.Revision == interval.ActionReferenceRevision))
                throw new ArgumentException("Search activity lacks its originating payment.");
        }

        public static void Validate(Snapshot state)
        {
            var search = state.ExplorationSearch;
            bool connected = ConnectedExplorationObservation.IsSelected(state);
            bool selected = connected || state.ContentFingerprint.StartsWith(ExplorationSearchDefinition.FingerprintPrefix, StringComparison.Ordinal)
                || state.ContentFingerprint.StartsWith(ExplorationHideDefinition.FingerprintPrefix, StringComparison.Ordinal);
            if ((search != null) != selected)
                throw new ArgumentException("Ordinary Search fingerprint and private component must agree.");
            if (search == null) return;
            var d = search.Definition;
            if (connected) ConnectedExplorationObservation.ValidateLayout(state, d);
            else if (!state.TestOnly || state.SchemaVersion != Snapshot.ObservationSchema || state.WorldSchedule == null
                || state.ObservationMapWidth == 0 || state.LaterEncounter != null || state.CharterAttempt != null
                || state.Retreat != null || state.Reengagement != null || state.SurpriseEntry != null
                || d.DirectorId != ExplorationSearchDefinition.Director)
                throw new ArgumentException("Invalid independent ordinary observation layout.");
            if (!state.Actors.Any(x => x.Id == d.SearcherId) || !state.Actors.Any(x => x.Id == d.ConcealedActorId)
                || WorldTiming.ForActor(state, d.SearcherId) != null
                || new[] { d.Anchor, d.CueCandidate, d.Sign, d.Occlusion }.Any(x => !InMap(state, x))
                || !state.ObservationCells.Any(x => x.X == d.Occlusion.X && x.Y == d.Occlusion.Y && x.BlocksSight))
                throw new ArgumentException("Ordinary Search source does not bind the selected actor and geometry.");

            foreach (var attempt in search.Attempts) {
                var cause = ReadReceipt(state, attempt.Revision, attempt.CommandId);
                if (cause?.Kind != CommandKind.Search || cause.Actor != d.SearcherId
                    || cause.Target != ExplorationSearchRecord.Marker(state.WorldSchedule.Id, attempt.IntervalIndex)
                    || cause.X != attempt.Candidate.X || cause.Y != attempt.Candidate.Y || !InMap(state, attempt.Candidate)
                    || attempt.StartedAt != WorldActivityIntervalRecord.StartAt(state.WorldSchedule, attempt.IntervalIndex)
                    || attempt.DueAt != WorldActivityIntervalRecord.EndAt(state.WorldSchedule, attempt.IntervalIndex)
                    || attempt.StartedAt > state.RuleClock)
                    throw new ArgumentException("Ordinary Search declaration or interval lacks its committed provenance.");
                if (connected) ConnectedExplorationObservation.ValidateDeclaration(state, attempt.Revision, attempt.StartedAt);
                var end = attempt.End;
                if (end != null) {
                    if (connected) ConnectedExplorationObservation.ValidateTerminal(state, end.Revision, end.CommandId, end.At,
                        end.Interruption == ExplorationSearchInterruption.TacticalControlEntered);
                    if (ReadReceipt(state, end.Revision, end.CommandId) == null || end.At > state.RuleClock)
                        throw new ArgumentException("Ordinary Search terminal receipt is invalid.");
                    ValidateEnd(state, d, attempt, end);
                }
            }

            var current = state.WorldActivityIntervals.Single(x => x.ActorId == d.SearcherId);
            var currentAttempt = search.Attempts.LastOrDefault(x => x.IntervalIndex == current.IntervalIndex);
            if (currentAttempt != null && (current.Action != WorldActionCommitment.Search
                || current.ActionReference != currentAttempt.CommandId || current.ActionReferenceRevision != currentAttempt.Revision))
                throw new ArgumentException("Ordinary Search lost its paid Action before the authorized refresh.");
            var pending = search.Pending;
            if (pending != null) {
                var pos = WorldPositionResolver.Position(state, d.SearcherId);
                if (state.InventoryCombat || connected && !ConnectedExplorationObservation.StageOpen(state)
                    || state.RuleClock > pending.DueAt || currentAttempt != pending
                    || state.RuleClock == pending.DueAt && state.ManufacturingAdvance == null
                    || state.WorldTraversals.Any(x => x.ActorId == d.SearcherId)
                    || pos.X != new RuleQuantity(d.Anchor.X) || pos.Y != new RuleQuantity(d.Anchor.Y))
                    throw new ArgumentException("Pending ordinary Search lost its stationary paid interval.");
            }
        }

        private static bool InMap(Snapshot state, ExplorationSearchCell cell)
            => cell.X < state.ObservationMapWidth && cell.Y < state.ObservationMapHeight;

        private static Command ReadReceipt(Snapshot state, long revision, string id)
        {
            var receipt = state.Receipts.SingleOrDefault(x => x.Revision == revision && x.Id == id);
            return receipt == null ? null : CommandHistory.Read(receipt);
        }

        private static void ValidateEnd(Snapshot state, ExplorationSearchDefinition d, ExplorationSearchAttempt attempt,
            ExplorationSearchEnd end)
        {
            if (end.Status == ExplorationSearchStatus.Cancelled) {
                var cancel = ReadReceipt(state, end.Revision, end.CommandId);
                if (cancel.Kind != CommandKind.CancelExplorationSearch || cancel.Actor != d.SearcherId || cancel.Target != attempt.Id)
                    throw new ArgumentException("Invalid ordinary Search cancellation authority.");
            }
            if (end.Status != ExplorationSearchStatus.Completed) {
                if (state.ObservationActions.Any(x => x.Kind == ObservationActionKind.Search && x.ActorId == d.SearcherId
                    && x.Revision == end.Revision))
                    throw new ArgumentException("Unfinished ordinary Search cannot have an observation result.");
                return;
            }

            var result = state.ObservationActions.SingleOrDefault(x => x.Id == end.ObservationId);
            if (result?.Kind != ObservationActionKind.Search || result.ActorId != d.SearcherId || result.Revision != end.Revision
                || result.At != end.At || result.X != new RuleQuantity(attempt.Candidate.X) || result.Y != new RuleQuantity(attempt.Candidate.Y)
                || result.TargetId != "" && result.TargetId != d.ConcealedActorId
                || (end.CueId == "") != (result.WordsConsumed == 0))
                throw new ArgumentException("Ordinary Search result does not bind its actual completion.");
            if (end.CueId == "") return;
            var hide = state.ObservationActions.SingleOrDefault(x => x.Id == end.HideId);
            if (end.CueId != d.CueId || !attempt.Candidate.Equals(d.CueCandidate)
                || hide?.Kind != ObservationActionKind.Hide || hide.ActorId != d.ConcealedActorId || hide.Revision > end.Revision
                || hide.Revision == end.Revision && !ExplorationHideValidation.PrecedesSearchAtSameBoundary(state, hide, attempt)
                || !state.ObservationHideResults.Any(x => x.AttemptId == end.HideId && x.ObserverId == d.SearcherId && x.HiddenEstablished))
                throw new ArgumentException("Ordinary Search has no genuine cue and observer-specific Hide reference.");
        }
    }

    public enum ExplorationSearchViewStatus { Pending, NoFinding, Found, Cancelled, Interrupted }

    public sealed class ExplorationSearchView
    {
        public string AttemptId { get; }
        public ExplorationSearchViewStatus Status { get; }
        public RuleTime StartedAt { get; }
        public RuleTime DueAt { get; }
        public RuleTime? EndedAt { get; }
        public ExplorationSearchCell? FoundLocation { get; }

        internal ExplorationSearchView(ExplorationSearchAttempt attempt, ObservationActionRecord result)
        {
            AttemptId = attempt.Id;
            StartedAt = attempt.StartedAt;
            DueAt = attempt.DueAt;
            EndedAt = attempt.End?.At;
            switch (attempt.Status) {
                case ExplorationSearchStatus.Pending: Status = ExplorationSearchViewStatus.Pending; break;
                case ExplorationSearchStatus.Cancelled: Status = ExplorationSearchViewStatus.Cancelled; break;
                case ExplorationSearchStatus.Interrupted: Status = ExplorationSearchViewStatus.Interrupted; break;
                default:
                    if (result.Outcome == ObservationActionOutcome.SearchFound) {
                        Status = ExplorationSearchViewStatus.Found;
                        FoundLocation = attempt.Candidate;
                    } else {
                        Status = ExplorationSearchViewStatus.NoFinding;
                    }
                    break;
            }
        }
    }
}
