#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private ExplorationSearchDefinition explorationSearchDefinition;

        public TestOnlySharedWorldPolicy EnableExplorationSearch()
        {
            if (initializationStarted || explorationSearchDefinition != null || SelectedSchema != Snapshot.ObservationSchema
                || observationAlgorithmVersion != ObservationAlgorithmVersion.ExactPathIntervalsV2)
                throw new InvalidOperationException("Select ordinary Search on the independent exact-observation host before initialization.");
            var d = new ExplorationSearchDefinition(ExplorationSearchDefinition.Source, ExplorationSearchDefinition.Director,
                ExplorationSearchDefinition.VisibleFringe, TestOnlyPolicy.CompanionId, TestOnlyPolicy.ActorId,
                new ExplorationSearchCell(3, 3), new ExplorationSearchCell(1, 0), new ExplorationSearchCell(2, 2),
                new ExplorationSearchCell(2, 1));
            explorationSearchDefinition = d;
            ContentFingerprint = ExplorationSearchDefinition.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                d.SourceRevision, d.DirectorId, d.CueId, d.SearcherId, d.ConcealedActorId, d.Anchor, d.CueCandidate,
                d.Sign, d.Occlusion, "existing-whole-ordinary-interval|exact-end|private-visual-fringe"));
            return this;
        }

        private static ObservationPoint SearchPoint(ExplorationSearchCell cell)
            => new ObservationPoint(new RuleQuantity(cell.X), new RuleQuantity(cell.Y));

        private void InitializeExplorationSearch(Snapshot state)
        {
            var d = explorationSearchDefinition;
            if (d == null) return;
            if (!ObservationGeometry.SupportsAnchorAt(state, d.Anchor.X, d.Anchor.Y)
                || !ObservationGeometry.SupportsAnchorAt(state, d.CueCandidate.X, d.CueCandidate.Y)
                || !ObservationGeometry.SupportsAnchorAt(state, d.Sign.X, d.Sign.Y)
                || observationFixture.Cell(d.Occlusion.X, d.Occlusion.Y)?.BlocksSight != true
                || !ObservationGeometry.GeometricSight(state, d.SearcherId, SearchPoint(d.Anchor), SearchPoint(d.Sign))
                || ObservationGeometry.GeometricSight(state, d.SearcherId, SearchPoint(d.Anchor), SearchPoint(d.CueCandidate)))
                throw new InvalidOperationException("Ordinary Search requires its authored visible near-side fringe and occluded recess.");
            state.ExplorationSearch = new ExplorationSearchRecord(d);
        }

        private static bool AtSearchPoint(Snapshot state, string actor, ExplorationSearchCell cell)
        {
            var position = ObservationGeometry.Position(state, actor);
            return position.X == new RuleQuantity(cell.X) && position.Y == new RuleQuantity(cell.Y);
        }

        private static bool SearcherCapable(Snapshot state, string actor)
            => ActorLifeRules.CanAct(state, actor) && !View(state, actor).BlocksSight && Permissions(state, actor).Action;

        private static bool InvalidExplorationSearchPayload(Command command)
            => command.Inventory != null || command.Combat != null || command.Advancement != null || command.Ranged != null
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null || command.OverwatchRider != OverwatchRider.None;

        private string AssessExplorationSearch(Snapshot state, Command command, out WorldActivityIntervalRecord activity)
        {
            activity = null;
            var search = state.ExplorationSearch;
            if (search == null || state.InventoryCombat) return "OrdinarySearchUnavailable";
            if (ConnectedObservationStageClosed(state)) return "ConnectedObservationStageClosed";
            var d = search.Definition;
            if (command.Actor != d.SearcherId || !IsOffCalendarActivity(state, command.Actor)) return "OrdinarySearchActorUnavailable";
            if (InvalidExplorationSearchPayload(command) || command.X < 0 || command.Y < 0
                || command.X >= state.ObservationMapWidth || command.Y >= state.ObservationMapHeight)
                return "InvalidOrdinarySearchRequest";
            if (search.Pending != null || PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state))
                return "OrdinarySearchDecisionPending";
            if (!SearcherCapable(state, d.SearcherId)) return "OrdinarySearchVisualCapabilityUnavailable";
            if (!AtSearchPoint(state, d.SearcherId, d.Anchor) || state.WorldTraversals.Any(x => x.ActorId == d.SearcherId))
                return "OrdinarySearchRequiresStationaryAnchor";

            activity = ActivityInterval(state, d.SearcherId);
            if (command.Target != ExplorationSearchRecord.Marker(activity.CalendarId, activity.IntervalIndex))
                return "WrongOrdinaryActivityInterval";
            var start = WorldActivityIntervalRecord.StartAt(state.WorldSchedule, activity.IntervalIndex);
            var end = WorldActivityIntervalRecord.EndAt(state.WorldSchedule, activity.IntervalIndex);
            if (state.RuleClock != start) return "OrdinarySearchRequiresIntervalStart";
            if (activity.Action != WorldActionCommitment.None) return "OffCalendarActionAlreadySpent";
            if (WorldActivityValidation.HasActiveLabor(state, d.SearcherId, start, end)
                || state.RestIntervals.Any(x => x.ActorId == d.SearcherId && x.Status == RestIntervalStatus.Active)
                || OrdinaryInventory.Busy(state, d.SearcherId))
                return "OrdinarySearchActorBusy";
            if (search.Attempts.Count == ExplorationSearchRecord.MaxAttempts || state.ObservationActions.Length >= ObservationValidation.MaxAttempts)
                return "ObservationHistoryCapacityReached";
            var profile = state.ObservationProfiles.Single(x => x.ActorId == d.SearcherId);
            return WithinRange(SearchPoint(d.Anchor), SearchPoint(new ExplorationSearchCell(command.X, command.Y)), profile.SearchRangeFeet)
                ? null : "SearchCellOutOfRange";
        }

        private string BeginExplorationSearch(Snapshot state, Command command)
        {
            var failure = AssessExplorationSearch(state, command, out var activity);
            if (failure != null) return failure;
            var attempt = new ExplorationSearchAttempt(state.Revision + 1, command.Id, activity.IntervalIndex,
                state.RuleClock, WorldActivityIntervalRecord.EndAt(state.WorldSchedule, activity.IntervalIndex),
                new ExplorationSearchCell(command.X, command.Y));
            SetActivityInterval(state, activity.PaySearch(command.Id, state.Revision + 1));
            state.ExplorationSearch = state.ExplorationSearch.Start(attempt);
            return null;
        }

        private static string AssessCancelExplorationSearch(Snapshot state, Command command)
        {
            var search = state.ExplorationSearch;
            if (search?.Pending == null || command.Actor != search.Definition.SearcherId || command.Target != search.Pending.Id)
                return "NoPendingOrdinarySearch";
            if (command.X != 0 || command.Y != 0 || InvalidExplorationSearchPayload(command)) return "InvalidOrdinarySearchCancellation";
            if (state.ManufacturingAdvance != null || PendingCalendarChoice(state)) return "OrdinarySearchDecisionPending";
            return null;
        }

        private static string CancelExplorationSearch(Snapshot state, Command command)
        {
            var failure = AssessCancelExplorationSearch(state, command);
            if (failure != null) return failure;
            FinishExplorationSearch(state, command, ExplorationSearchStatus.Cancelled);
            return null;
        }

        private static void FinishExplorationSearch(Snapshot state, Command cause, ExplorationSearchStatus status,
            ExplorationSearchInterruption interruption = ExplorationSearchInterruption.None, string resultId = "",
            string cueId = "", string hideId = "")
        {
            state.ExplorationSearch = state.ExplorationSearch.Finish(new ExplorationSearchEnd(status,
                interruption, state.Revision + 1, cause.Id, state.RuleClock, resultId, cueId, hideId));
        }

        private static ExplorationSearchInterruption SearchInterruption(Snapshot state, ExplorationSearchDefinition d)
        {
            if (state.InventoryCombat) return ExplorationSearchInterruption.TacticalControlEntered;
            if (!AtSearchPoint(state, d.SearcherId, d.Anchor)) return ExplorationSearchInterruption.SearcherDisplaced;
            return SearcherCapable(state, d.SearcherId) ? ExplorationSearchInterruption.None
                : ExplorationSearchInterruption.VisualCapabilityLost;
        }

        private static ObservationActionRecord QualifyingSearchHide(Snapshot state, ExplorationSearchDefinition d,
            ExplorationSearchCell candidate)
        {
            if (!candidate.Equals(d.CueCandidate) || !AtSearchPoint(state, d.ConcealedActorId, candidate)
                || !ActorLifeRules.CanAct(state, d.ConcealedActorId)
                || !ObservationRules.HiddenTo(state, d.SearcherId, d.ConcealedActorId)
                || !ObservationGeometry.GeometricSight(state, d.SearcherId, SearchPoint(d.Anchor), SearchPoint(d.Sign)))
                return null;
            return ActiveSearchHide(state, d.SearcherId, d.ConcealedActorId);
        }

        private static bool ReconcileExplorationSearch(Snapshot state, Command cause)
        {
            var search = state.ExplorationSearch;
            var pending = search?.Pending;
            if (pending == null || cause == null) return false;
            var d = search.Definition;
            var interruption = SearchInterruption(state, d);
            if (interruption != ExplorationSearchInterruption.None) {
                FinishExplorationSearch(state, cause, ExplorationSearchStatus.Interrupted, interruption);
                return true;
            }
            if (state.RuleClock != pending.DueAt || state.ManufacturingAdvance != null || PendingCalendarChoice(state))
                return false;

            var hide = QualifyingSearchHide(state, d, pending.Candidate);
            var result = RecordSearchResult(state, d.SearcherId, SearchPoint(pending.Candidate), hide);
            FinishExplorationSearch(state, cause, ExplorationSearchStatus.Completed, resultId: result.Id,
                cueId: hide == null ? "" : d.CueId, hideId: hide?.Id ?? "");
            return true;
        }

        private bool FinishSearchAtAdvanceBoundary(Snapshot state, Command cause)
        {
            var search = state.ExplorationSearch;
            var pending = search?.Pending;
            if (pending == null || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state)
                || state.RuleClock != pending.DueAt
                    && SearchInterruption(state, search.Definition) == ExplorationSearchInterruption.None)
                return false;

            TestOnlyClubAttackPolicy.AdvanceConditions(state, ".clock-final");
            if (!ReconcileExplorationSearch(state, cause)) return false;
            RefreshActivityIntervals(state);
            return true;
        }

        private static string SearchActivityConflict(Snapshot state, Command command)
        {
            var search = state.ExplorationSearch;
            if (search?.Definition.SearcherId != command.Actor) return null;
            bool activeWork = StartsOrResumesActivityWork(command);
            if (search.Pending != null && (activeWork || command.Kind == CommandKind.BeginWorldStep
                || command.Kind == CommandKind.ResumeWorldStep || command.Kind == CommandKind.HandleInventory
                || command.Kind == CommandKind.HandleVessel || command.Kind == CommandKind.StartIntake))
                return "OrdinarySearchInProgress";
            if (activeWork && ActivityInterval(state, command.Actor).Action == WorldActionCommitment.Search)
                return "OffCalendarActionAlreadySpent";
            return null;
        }
    }
}
#endif
