#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private ExplorationHideDefinition explorationHideDefinition;

        public TestOnlySharedWorldPolicy EnableExplorationHide()
        {
            if (initializationStarted || explorationSearchDefinition == null || explorationHideDefinition != null)
                throw new InvalidOperationException("Select ordinary Hide after selecting the independent ordinary Search profile.");
            var d = new ExplorationHideDefinition(ExplorationSearchDefinition.Source, ExplorationHideDefinition.Director,
                explorationSearchDefinition.ConcealedActorId, ExplorationHideDefinition.Witness,
                explorationSearchDefinition.CueCandidate, new ExplorationSearchCell(2, 0));
            explorationHideDefinition = d;
            ContentFingerprint = ExplorationHideDefinition.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                d.SourceRevision, d.DirectorId, d.HiderId, d.WitnessId, d.Recess, d.Alternate,
                "existing-personal-action|paid-stationary-interval|completed-alternate-relocation|receipt-ordered-boundary"));
            return this;
        }

        private void InitializeExplorationHide(Snapshot state)
        {
            var d = explorationHideDefinition;
            if (d == null) return;
            if (!state.WorldSchedule.Order.Contains(d.HiderId) || !state.Actors.Any(x => x.Id == d.WitnessId)
                || !ObservationGeometry.SupportsAnchorAt(state, d.Recess.X, d.Recess.Y)
                || !ObservationGeometry.SupportsAnchorAt(state, d.Alternate.X, d.Alternate.Y))
                throw new InvalidOperationException("Ordinary Hide requires its scheduled actor and authored anchors and witness.");
            state.ExplorationHide = new ExplorationHideRecord(d);
        }

        private static bool HiderCapable(Snapshot state, string actor)
        {
            var life = state.Lives.Single(x => x.ActorId == actor);
            return View(state, actor).PermissionsForLife(ActorLifeRules.Read(life)).Action;
        }

        private string AssessExplorationHide(Snapshot state, Command command, out WorldIntervalRecord interval,
            out ExplorationSearchCell anchor, out RuleTime due)
        {
            interval = null;
            anchor = default;
            due = default;
            var hide = state.ExplorationHide;
            if (hide == null || state.InventoryCombat) return "OrdinaryHideUnavailable";
            if (ConnectedObservationStageClosed(state)) return "ConnectedObservationStageClosed";
            var d = hide.Definition;
            if (command.Actor != d.HiderId || WorldTiming.ForActor(state, command.Actor)?.Id != state.WorldSchedule.Id)
                return "OrdinaryHideActorUnavailable";
            if (command.X != 0 || command.Y != 0 || InvalidExplorationSearchPayload(command)) return "InvalidOrdinaryHideRequest";
            if (hide.Pending != null || PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state))
                return "OrdinaryHideDecisionPending";
            if (!HiderCapable(state, d.HiderId)) return "OrdinaryHideActionCapabilityUnavailable";
            anchor = AtSearchPoint(state, d.HiderId, d.Recess) ? d.Recess : d.Alternate;
            if (!AtSearchPoint(state, d.HiderId, anchor) || state.WorldTraversals.Any(x => x.ActorId == d.HiderId))
                return "OrdinaryHideRequiresStationaryAnchor";

            interval = Interval(state, d.HiderId);
            var schedule = state.WorldSchedule;
            if (interval.LastStart < 0 || command.Target != schedule.MarkerId(interval.LastStart))
                return "WrongOrdinaryHideStart";
            if (state.RuleClock != schedule.Start(interval.LastStart)) return "OrdinaryHideRequiresOwnStart";
            if (interval.ActionSpent) return "ActionAlreadySpent";
            due = schedule.Start(checked(interval.LastStart + schedule.Order.Count));
            if (WorldActivityValidation.HasActiveLabor(state, d.HiderId, state.RuleClock, due)
                || state.RestIntervals.Any(x => x.ActorId == d.HiderId && x.Status == RestIntervalStatus.Active)
                || OrdinaryInventory.Busy(state, d.HiderId))
                return "OrdinaryHideActorBusy";
            // Reserve capacity for both selected procedures without exposing their private qualification.
            if (hide.Attempts.Count >= ExplorationHideRecord.MaxAttempts
                || state.ObservationActions.Length > ObservationValidation.MaxAttempts - 2
                || state.ObservationHideResults.Length > ObservationValidation.MaxHideResults - 2
                || state.ObserverKnowledge.Length > ObservationValidation.MaxKnowledgePairs - 2)
                return "ObservationHistoryCapacityReached";
            return null;
        }

        private string BeginExplorationHide(Snapshot state, Command command)
        {
            var error = AssessExplorationHide(state, command, out var interval, out var anchor, out var due);
            if (error != null) return error;
            var hide = state.ExplorationHide;
            var relocation = hide.LatestRelocation;
            var attempt = new ExplorationHideAttempt(state.Revision + 1, command.Id, state.WorldSchedule.Id,
                interval.LastStart, state.RuleClock, due, anchor, relocation?.To.Equals(anchor) == true ? relocation : null);
            SetInterval(state, interval.PayAction());
            state.ExplorationHide = hide.Start(attempt);
            return null;
        }

        private string AssessCancelExplorationHide(Snapshot state, Command command)
        {
            var hide = state.ExplorationHide;
            if (hide?.Pending == null || command.Actor != hide.Definition.HiderId || command.Target != hide.Pending.Id)
                return "NoPendingOrdinaryHide";
            if (command.X != 0 || command.Y != 0 || InvalidExplorationSearchPayload(command)) return "InvalidOrdinaryHideCancellation";
            return OrdinaryObservationChoicePending(state) ? "OrdinaryHideDecisionPending" : null;
        }

        private string CancelExplorationHide(Snapshot state, Command command)
        {
            var failure = AssessCancelExplorationHide(state, command);
            if (failure != null) return failure;
            FinishExplorationHide(state, command, ExplorationHideStatus.Cancelled);
            return null;
        }

        private CommandQueryResult QueryExplorationHide(Snapshot state, Command command)
        {
            if (command.Kind == CommandKind.CancelExplorationHide) {
                var cancellation = AssessCancelExplorationHide(state, command);
                return new CommandQueryResult(true, cancellation == null, cancellation ?? "Available", state.Revision);
            }
            var failure = AssessExplorationHide(state, command, out _, out _, out var due);
            var costs = failure == null
                ? new[] { new CommandCost("action", "", 1), new CommandCost("elapsed-seconds", "", CampGreens.Subtract(due, state.RuleClock).Numerator) }
                : Array.Empty<CommandCost>();
            return new CommandQueryResult(true, failure == null, failure ?? "Available", state.Revision, costs);
        }

        private IEnumerable<Command> DiscoverExplorationHide(Snapshot state, string actor)
        {
            var hide = state.ExplorationHide;
            if (state.InventoryCombat || hide?.Definition.HiderId != actor) yield break;
            var interval = Interval(state, actor);
            var pending = hide.Pending;
            if (pending == null && interval.LastStart < 0) yield break;
            var option = pending != null
                ? new Command("option." + Number(state.Revision) + ".cancel-ordinary-hide", actor, state.Revision,
                    CommandKind.CancelExplorationHide, pending.Id)
                : new Command("option." + Number(state.Revision) + ".ordinary-hide", actor, state.Revision,
                    CommandKind.Hide, state.WorldSchedule.MarkerId(interval.LastStart));
            if (QueryExplorationHide(state, option).Admissible) yield return option;
        }

        private static string HideActivityConflict(Snapshot state, Command command)
        {
            var hide = state.ExplorationHide;
            if (hide?.Pending == null || command.Actor != hide.Definition.HiderId) return null;
            return StartsOrResumesActivityWork(command) || command.Kind == CommandKind.BeginWorldStep
                || command.Kind == CommandKind.ResumeWorldStep || command.Kind == CommandKind.Move
                || command.Kind == CommandKind.Interact || command.Kind == CommandKind.BeginRest
                || command.Kind == CommandKind.BeginMoraleRest || command.Kind == CommandKind.BeginHavenCare
                ? "OrdinaryHideInProgress" : null;
        }

        private static void RecordHideRelocation(Snapshot state, WorldTraversalRecord edge, RuleTime at, Command cause)
        {
            var hide = state.ExplorationHide;
            if (hide == null || hide.Definition.HiderId != edge.ActorId || ConnectedObservationStageClosed(state)) return;
            var d = hide.Definition;
            var from = new ExplorationSearchCell(edge.FromX, edge.FromY);
            var to = new ExplorationSearchCell(edge.ToX, edge.ToY);
            var evidence = d.Allows(from) && d.Allows(to) && cause?.Kind == CommandKind.AdvanceClock
                ? new ExplorationHideRelocation(from, to, edge.StartedRevision, state.Revision + 1, cause.Id, at)
                : null;
            state.ExplorationHide = hide.WithRelocation(evidence);
        }

        private static void FinishExplorationHide(Snapshot state, Command cause, ExplorationHideStatus status,
            ExplorationHideInterruption interruption = ExplorationHideInterruption.None, string result = "",
            ExplorationHideNoRoll noRoll = ExplorationHideNoRoll.None, string failure = "", string observer = "",
            ExplorationHideObservers eligible = ExplorationHideObservers.None)
        {
            state.ExplorationHide = state.ExplorationHide.Finish(new ExplorationHideEnd(status, interruption,
                state.Revision + 1, cause.Id, state.RuleClock, result, noRoll, failure, observer, eligible));
        }

        private static ExplorationHideInterruption HideInterruption(Snapshot state, ExplorationHideAttempt pending)
        {
            if (state.InventoryCombat) return ExplorationHideInterruption.TacticalControlEntered;
            string hider = state.ExplorationHide.Definition.HiderId;
            if (!AtSearchPoint(state, hider, pending.Anchor)) return ExplorationHideInterruption.HiderDisplaced;
            return HiderCapable(state, hider) ? ExplorationHideInterruption.None : ExplorationHideInterruption.ActionCapabilityLost;
        }

        private static void CompleteExplorationHide(Snapshot state, Command cause)
        {
            var hide = state.ExplorationHide;
            var d = hide.Definition;
            var attempt = hide.Pending;
            var position = SearchPoint(attempt.Anchor);
            string[] observers = { state.ExplorationSearch.Definition.SearcherId, d.WitnessId };
            var eligible = observers.Where(actor => {
                var view = View(state, actor);
                var observerPosition = ObservationGeometry.Position(state, actor);
                var profile = state.ObservationProfiles.Single(x => x.ActorId == actor);
                return ActorLifeRules.CanAct(state, actor) && !view.Unaware && !view.BlocksSight
                    && WithinRange(observerPosition, position, profile.SightRangeFeet)
                    && !ObservationRules.DirectSightAt(state, actor, d.HiderId, observerPosition, position);
            }).OrderBy(x => x, StringComparer.Ordinal).ToArray();
            if (eligible.Length == 0) {
                FinishExplorationHide(state, cause, ExplorationHideStatus.Completed, noRoll: ExplorationHideNoRoll.NoEligibleObservers);
                return;
            }
            var eligibility = ExplorationHideObservers.None;
            if (eligible.Contains(observers[0])) eligibility |= ExplorationHideObservers.Searcher;
            if (eligible.Contains(observers[1])) eligibility |= ExplorationHideObservers.Witness;
            foreach (var observer in eligible) {
                var failed = ExplorationHideValidation.UnchangedFailure(state, attempt, observer, state.Revision + 1);
                if (failed == null) continue;
                FinishExplorationHide(state, cause, ExplorationHideStatus.Completed, noRoll: ExplorationHideNoRoll.UnchangedFailure,
                    failure: failed.Id, observer: observer, eligible: eligibility);
                return;
            }
            var result = RecordHideRoll(state, d.HiderId, position, HideObserverFacts(state, eligible),
                HideModifier(state, d.HiderId), HideDisadvantage(state, d.HiderId));
            FinishExplorationHide(state, cause, ExplorationHideStatus.Completed, result: result.Id, eligible: eligibility);
        }

        private static string ValidateExplorationHideRolls(Snapshot state)
        {
            if (state.ExplorationHide == null) return null;
            foreach (var attempt in state.ExplorationHide.Attempts.Where(x => !string.IsNullOrEmpty(x.End?.ObservationId))) {
                var recorded = state.ObservationActions.Single(x => x.Id == attempt.End.ObservationId);
                var dice = RuleDice.RollD20(recorded.RandomBefore, disadvantageSources:
                    recorded.Selection == ObservationDieSelection.Disadvantage ? 1 : 0);
                if (recorded.Natural != dice.Natural || recorded.First != dice.First || recorded.Second != (dice.Second ?? 0)
                    || recorded.RandomAfter != dice.NextRandomState || recorded.WordsConsumed != dice.WordsConsumed)
                    return "OrdinaryHideRngProvenanceMismatch";
                foreach (var result in state.ObservationHideResults.Where(x => x.AttemptId == recorded.Id)) {
                    var check = PlaytestRolls.TaskCheck(recorded.Natural, recorded.Modifier, result.Dc);
                    if (check.Success != result.HiddenEstablished || ObservationDegree(check.Degree) != result.Degree)
                        return "OrdinaryHideTaskDegreeMismatch";
                }
            }
            return null;
        }

        private bool OrdinaryObservationChoicePending(Snapshot state)
            => state.ManufacturingAdvance != null || PendingCalendarChoice(state) || ManufacturingChoicePending(state)
                || HasPendingRecoveryOffer(state);

        private bool ReconcileOrdinaryObservationActions(Snapshot state, Command cause)
        {
            if (state.ExplorationHide == null) return ReconcileExplorationSearch(state, cause);
            if (cause == null) return false;
            if (state.InventoryCombat && state.ExplorationHide.LatestRelocation != null)
                state.ExplorationHide = state.ExplorationHide.WithRelocation(null);
            var hide = state.ExplorationHide.Pending;
            var search = state.ExplorationSearch.Pending;
            bool settled = false;
            if (hide != null) {
                var interruption = HideInterruption(state, hide);
                if (interruption != ExplorationHideInterruption.None) {
                    FinishExplorationHide(state, cause, ExplorationHideStatus.Interrupted, interruption);
                    hide = null;
                    settled = true;
                }
            }
            if (search != null && SearchInterruption(state, state.ExplorationSearch.Definition) != ExplorationSearchInterruption.None) {
                settled |= ReconcileExplorationSearch(state, cause);
                search = null;
            }
            if (OrdinaryObservationChoicePending(state)) return settled;
            bool hideDue = hide?.DueAt == state.RuleClock;
            bool searchDue = search?.DueAt == state.RuleClock;
            if (hideDue && (!searchDue || hide.Revision < search.Revision)) {
                CompleteExplorationHide(state, cause);
                hideDue = false;
                settled = true;
            }
            if (searchDue) settled |= ReconcileExplorationSearch(state, cause);
            if (hideDue) {
                CompleteExplorationHide(state, cause);
                settled = true;
            }
            return settled;
        }

        private bool FinishOrdinaryObservationAtAdvanceBoundary(Snapshot state, Command cause)
        {
            if (state.ExplorationHide == null) return FinishSearchAtAdvanceBoundary(state, cause);
            var hide = state.ExplorationHide.Pending;
            var search = state.ExplorationSearch.Pending;
            if (hide == null && search == null) return false;
            if (hide != null && hide.DueAt == state.RuleClock || search != null && search.DueAt == state.RuleClock
                || hide != null && HideInterruption(state, hide) != ExplorationHideInterruption.None
                || search != null && SearchInterruption(state, state.ExplorationSearch.Definition) != ExplorationSearchInterruption.None) {
                TestOnlyClubAttackPolicy.AdvanceConditions(state, ".clock-final",
                    onlyAtExpiry: state.SchemaVersion >= Snapshot.ExpeditionRouteSchema);
                if (ReconcileOrdinaryObservationActions(state, cause)) {
                    string deferred = state.ExplorationSearch.Pending?.DueAt == state.RuleClock
                        ? state.ExplorationSearch.Definition.SearcherId : null;
                    RefreshActivityIntervals(state, deferred);
                    return !OrdinaryObservationChoicePending(state);
                }
            }
            return false;
        }
    }
}
#endif
