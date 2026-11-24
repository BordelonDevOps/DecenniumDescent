#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        public string Resolve(Snapshot s, Command c) => Resolve(s, c, null);

        private string Resolve(Snapshot s, Command c, PlanningPassage? passage, bool verifiedExecution = false)
        {
            NativeReadInspectionV1.RequireExecution(NativeReadOperationV1.Resolver);
            using var conditions = ConditionResolutionScope.Enter(verifiedExecution && ReuseAdvanceConditions(s, c));
            Snapshot workWatchBefore=recipe347Fixture!=null&&Recipe347WorkStartCommand(c)?s.Copy():null;
            var pendingAdvance = s.ManufacturingAdvance;
            string error = ResolveCore(s, c, passage: passage);
            if (error == null) ReconcileClericLongRestAccess(s,c);
            if(error==null&&PendingSanctuary(s)!=null)return null;
            if (error == null) ReconcileShortRest(s, c);
            if (error == null && ActiveBloodTreatment(s) is HarvestPreservationTreatmentAttemptRecord treatment) {
                if (treatment.UpdatedAt < s.RuleClock) return "BloodTreatmentRequiresSharedAdvance";
                string access = BloodTreatmentAccess(s, treatment.WorkerId);
                if (access != null) return access;
            }
            if (IsCharterAttemptCommand(c.Kind)) return error;
            if (IsNextCharterAgreementCommand(c.Kind)) {
                if (error == null && c.Kind == CommandKind.WithdrawNextCharter) ReconcileCharterAttempt(s, c);
                return error;
            }
            if(error==null&&workWatchBefore!=null)
                error=Recipe347ProjectedWorkWatchFailure(workWatchBefore,s,c);
            if(error==null)ApplyExpeditionCampTransitions(s,c);
            if(error==null)ReconcileHavenAppraisal(s);
            if(error==null)ReconcileHavenSale(s);
            if(error==null)ReconcileExpeditionBill(s);
            if(error==null)ReconcileNextCharterPlan(s);
            if(error==null)ExpireReadyActionsAtStart(s,c);
            if(error==null&&s.InventoryCombat) {
                error=QueueCompletedTacticalHuntingTrapEntries(s);
                if(error==null)ResolveOrderedHuntingTrapTrigger(s,c);
            }
            if (error == null && ObservationRules.Enabled(s))
                ObservationRules.Refresh(s, s.RuleClock, s.Revision + 1);
            if (error == null) ReconcileCharterAttempt(s, c);
            if (error == null) ReconcileReinforcement(s, c);
            if (error == null && s.Retreat != null) {
                RecordLocalRetreatCombatSources(s);
                ReconcileRetreat(s, c);
            }
            if (error == null && s.SurpriseEntry != null) CompleteSurpriseFirstEnd(s, c, pendingAdvance);
            if (error == null && ReconcileOrdinaryObservationActions(s, c)) RefreshActivityIntervals(s);
            if (error == null) ReconcileClericLongRestAccess(s,c);
            return error;
        }

        private bool ReuseAdvanceConditions(Snapshot state, Command command)
            => verifiedPlanningPassage && command.Kind == CommandKind.AdvanceClock && !state.InventoryCombat
                && state.FormulaWork.Any(job => job.Kind == FormulaWorkKind.Research && job.Status == FormulaWorkStatus.Working);

        private string ResolveObservationAction(Snapshot s, Command c)
        {
            string failure = AssessObservationAction(s, c, out var interval);
            if (failure != null) return failure;
            ObservationPoint candidateCell = default;
            if (c.Kind == CommandKind.Search)
            {
                failure = AssessSearchRequest(s, c, out candidateCell);
                if (failure != null) return failure;
            }
            failure = c.Kind == CommandKind.Hide ? ResolveHide(s, c) : ResolveSearch(s, c, candidateCell);
            if (failure != null) return failure;
            SetInterval(s, interval.PayAction());
            PauseIncompatibleWork(s);
            return null;
        }

        private string AssessObservationAction(Snapshot s, Command c, out WorldIntervalRecord interval)
            => ObservationActionConstraintV1(s, c, out interval)?.NativeCode;

        private NativeCommandConstraintV1 ObservationActionConstraintV1(Snapshot s, Command c, out WorldIntervalRecord interval)
        {
            interval = null;
            if (observationFixture == null || s.SchemaVersion < Snapshot.ObservationSchema)
                return new NativeCommandConstraintV1("ObservationActionNotImplemented", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 83);
            if (s.Encounter == null || !s.InventoryCombat) return new NativeCommandConstraintV1("ObservationActionRequiresTacticalCombat", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 84);
            if (PendingCalendarChoice(s)) return new NativeCommandConstraintV1("TacticalChoicePending", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 85);
            if (c.Actor != s.Encounter.CurrentActor || c.Target != s.Encounter.CurrentTurnId)
                return new NativeCommandConstraintV1("WrongRegularTurn", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 87);
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.SuppressionFire != null || c.ExpeditionAssignment != null || c.HarvestSelection != null
                || c.MiningSelection != null || c.ProspectingExposure != null || c.OverwatchRider != OverwatchRider.None)
                return new NativeCommandConstraintV1("InvalidObservationActionPayload", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 91);
            if (!ActorLifeRules.CanAct(s, c.Actor)) return new NativeCommandConstraintV1("ActorCannotAct", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 92);
            if (!Permissions(s, c.Actor).Action) return new NativeCommandConstraintV1("ConditionPreventsAction", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 93);
            interval = Interval(s, c.Actor);
            if (interval.ActionSpent) return new NativeCommandConstraintV1("ActionAlreadySpent", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 95);
            if (s.ObservationActions.Length >= ObservationValidation.MaxAttempts)
                return new NativeCommandConstraintV1("ObservationHistoryCapacityReached", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 97);
            return null;
        }

        /// <summary>Pure public Search-request validation. Deliberately does not inspect Hidden
        /// targets, observer knowledge or a target's recorded Stealth result.</summary>
        private string AssessSearchRequest(Snapshot s, Command c, out ObservationPoint candidateCell)
            => SearchRequestConstraintV1(s, c, out candidateCell)?.NativeCode;

        private NativeCommandConstraintV1 SearchRequestConstraintV1(Snapshot s, Command c, out ObservationPoint candidateCell)
        {
            candidateCell = default;
            if (c.Target != s.Encounter.CurrentTurnId || c.X < 0 || c.Y < 0
                || c.X >= s.ObservationMapWidth || c.Y >= s.ObservationMapHeight) return new NativeCommandConstraintV1("InvalidSearchRequest", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 107);
            var profile = s.ObservationProfiles.Single(x => x.ActorId == c.Actor);
            var searcher = ObservationGeometry.Position(s, c.Actor);
            candidateCell = new ObservationPoint(new RuleQuantity(c.X), new RuleQuantity(c.Y));
            return WithinRange(searcher, candidateCell, profile.SearchRangeFeet) ? null : new NativeCommandConstraintV1("SearchCellOutOfRange", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 111);
        }

        private CommandQueryResult QueryObservationSearchCommand(Snapshot s, Command c)
        {
            if (c.Kind == CommandKind.CancelExplorationSearch) {
                var cancellationFailure = AssessCancelExplorationSearch(s, c);
                return new CommandQueryResult(true, cancellationFailure == null, cancellationFailure ?? "Available", s.Revision);
            }
            if (s.ExplorationSearch != null && !s.InventoryCombat) {
                var explorationFailure = AssessExplorationSearch(s, c, out var activity);
                var explorationCosts = Array.Empty<CommandCost>();
                if (explorationFailure == null) {
                    var start = WorldActivityIntervalRecord.StartAt(s.WorldSchedule, activity.IntervalIndex);
                    var end = WorldActivityIntervalRecord.EndAt(s.WorldSchedule, activity.IntervalIndex);
                    var elapsed = CampGreens.Subtract(end, start);
                    explorationCosts = new[] { new CommandCost("action", "", 1), new CommandCost("elapsed-seconds", "", elapsed.Numerator) };
                }
                return new CommandQueryResult(true, explorationFailure == null, explorationFailure ?? "Available",
                    s.Revision, explorationCosts);
            }
            string failure = AssessObservationAction(s, c, out _);
            if (failure == null) failure = AssessSearchRequest(s, c, out _);
            var costs = failure == null
                ? new[] { new CommandCost("action", "", 1) }
                : Array.Empty<CommandCost>();
            return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
        }

        private IEnumerable<Command> DiscoverObservationSearchCommands(Snapshot s, string actor)
        {
            if (observationFixture == null || s.SchemaVersion < Snapshot.ObservationSchema) yield break;
            string turnId;
            if (s.InventoryCombat) {
                if (s.Encounter == null || actor != s.Encounter.CurrentActor) yield break;
                turnId = s.Encounter.CurrentTurnId;
            } else {
                if (s.ExplorationSearch?.Definition.SearcherId != actor || ConnectedObservationStageClosed(s)) yield break;
                var pending = s.ExplorationSearch.Pending;
                if (pending != null) {
                    yield return new Command("option." + s.Revision + ".cancel-ordinary-search", actor,
                        s.Revision, CommandKind.CancelExplorationSearch, pending.Id);
                    yield break;
                }
                var activity = ActivityInterval(s, actor);
                turnId = ExplorationSearchRecord.Marker(activity.CalendarId, activity.IntervalIndex);
            }
            var profile = s.ObservationProfiles.SingleOrDefault(x => x.ActorId == actor);
            if (profile == null) yield break;
            var searcher = ObservationGeometry.Position(s, actor);
            for (int y = 0; y < s.ObservationMapHeight; y++)
            for (int x = 0; x < s.ObservationMapWidth; x++)
            {
                var candidateCell = new ObservationPoint(new RuleQuantity(x), new RuleQuantity(y));
                if (!WithinRange(searcher, candidateCell, profile.SearchRangeFeet)) continue;
                string id = "option." + s.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture)
                    + ".observation.search." + x.ToString(System.Globalization.CultureInfo.InvariantCulture)
                    + "." + y.ToString(System.Globalization.CultureInfo.InvariantCulture);
                yield return new Command(id, actor, s.Revision, CommandKind.Search, turnId, x, y);
            }
        }

        private NativeCommandConstraintV1 HideConstraintV1(Snapshot s, Command c, out ActorState selectedActor,
            out ObservationPoint selectedPosition, out ActorState[] selectedObservers, out int selectedModifier, out int selectedDisadvantage,
            out (string Actor, ObservationPoint Position, int Dc)[] selectedObserverFacts)
        {
            selectedActor=null; selectedPosition=default; selectedObservers=null; selectedModifier=0; selectedDisadvantage=0; selectedObserverFacts=null;
            if (c.Target != s.Encounter.CurrentTurnId || c.X != 0 || c.Y != 0) return new NativeCommandConstraintV1("InvalidHideRequest", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 175);
            var actor = s.Actors.Single(x => x.Id == c.Actor);
            var position = ObservationGeometry.Position(s, actor.Id);
            if (!IsGridCell(position.X) || !IsGridCell(position.Y)) return new NativeCommandConstraintV1("HideRequiresAuthoredGridCell", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 178);

            var observers = s.Actors.Where(x => x.Id != actor.Id && ActorLifeRules.CanAct(s, x.Id)
                    && !TestOnlyClubAttackPolicy.ConditionsFor(s, x.Id).View().Unaware
                    && WithinRange(ObservationGeometry.Position(s, x.Id), position,
                        s.ObservationProfiles.Single(p => p.ActorId == x.Id).SightRangeFeet))
                .OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            if (observers.Any(x => ObservationRules.DirectSightAt(s, x.Id, actor.Id,
                    ObservationGeometry.Position(s, x.Id), position))) return new NativeCommandConstraintV1("HideWhileClearlyObserved", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 186);
            if (s.ObservationHideResults.Length + observers.Length > ObservationValidation.MaxHideResults)
                return new NativeCommandConstraintV1("ObservationHideHistoryCapacityReached", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 188);
            if (s.ObserverKnowledge.Length + observers.Count(x => !s.ObserverKnowledge.Any(k => k.ObserverId == x.Id && k.TargetId == actor.Id))
                > ObservationValidation.MaxKnowledgePairs) return new NativeCommandConstraintV1("ObservationKnowledgeCapacityReached", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 190);

            selectedActor=actor; selectedPosition=position; selectedObservers=observers;
            if (observers.Length == 0) return null;

            int modifier = HideModifier(s, actor.Id);
            int disadvantage = HideDisadvantage(s, actor.Id);
            var selection = PlaytestDice.Selection(0, disadvantage);
            var observerFacts = HideObserverFacts(s, observers.Select(x => x.Id));
            var prior = s.ObservationActions.Where(x => x.ActorId == actor.Id && x.Kind == ObservationActionKind.Hide)
                .OrderByDescending(x => x.Revision).FirstOrDefault();
            if (prior != null && prior.Outcome == ObservationActionOutcome.HideAttempted
                && prior.X == position.X && prior.Y == position.Y && prior.Modifier-HistoricalGuidance(s,prior.Id) == modifier
                && prior.Selection == DieSelection(selection))
            {
                var priorResults = s.ObservationHideResults.Where(x => x.AttemptId == prior.Id)
                    .OrderBy(x => x.ObserverId, StringComparer.Ordinal).ToArray();
                bool unchanged = priorResults.Length == observerFacts.Length
                    && observerFacts.OrderBy(x => x.Actor, StringComparer.Ordinal).Select((x, i) =>
                        priorResults[i].ObserverId == x.Actor && priorResults[i].Dc == x.Dc
                            && priorResults[i].ObserverX == x.Position.X && priorResults[i].ObserverY == x.Position.Y).All(x => x);
                if (unchanged && priorResults.Any(x => !x.HiddenEstablished)) return new NativeCommandConstraintV1("HideAttemptUnchanged", "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 220);
            }
            selectedModifier=modifier; selectedDisadvantage=disadvantage; selectedObserverFacts=observerFacts;
            return null;
        }

        private string ResolveHide(Snapshot s, Command c, bool assessOnly=false)
        {
            var failure=HideConstraintV1(s,c,out var actor,out var position,out var observers,
                out var modifier,out var disadvantage,out var observerFacts);
            if(failure!=null)return failure.NativeCode;
            if(assessOnly)return null;
            long revision = s.Revision + 1;
            string attemptId = "observation." + revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".hide";
            RuleTime at = s.RuleClock;
            if (observers.Length == 0)
            {
                s.ObservationActions = s.ObservationActions.Concat(new[] { new ObservationActionRecord(attemptId, actor.Id, "",
                    ObservationActionKind.Hide, ObservationActionOutcome.NoEligibleObservers, at, revision, position.X, position.Y,
                    0, 0, 0, 0, 0, ObservationDieSelection.None, s.RandomState, s.RandomState, 0) }).ToArray();
                return null;
            }

            modifier=checked(modifier+ConsumeGuidance(s,c,attemptId,GuidanceCheckKind.Hide));
            RecordHideRoll(s, actor.Id, position, observerFacts, modifier, disadvantage);
            return null;
        }

        private static int HideModifier(Snapshot s, string actor)
            => CharacterStateFacts.ForActor(s, actor, "stealth").TotalWithInjury(CharacterAbility.Dexterity);

        private static int HideDisadvantage(Snapshot s, string actor)
            => View(s, actor).Has(ConditionKind.Poisoned) || FrightenedRules.VisibleSource(s, actor) ? 1 : 0;

        private static (string Actor, ObservationPoint Position, int Dc)[] HideObserverFacts(Snapshot s, IEnumerable<string> observers)
            => observers.Select(x => (x, ObservationGeometry.Position(s, x), PassivePerception(s, x))).ToArray();

        private static ObservationActionRecord RecordHideRoll(Snapshot s, string actor, ObservationPoint position,
            (string Actor, ObservationPoint Position, int Dc)[] observerFacts, int modifier, int disadvantage)
        {
            long revision = s.Revision + 1;
            string attemptId = "observation." + revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".hide";
            RuleTime at = s.RuleClock;
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var action = new ObservationActionRecord(attemptId, actor, "", ObservationActionKind.Hide,
                ObservationActionOutcome.HideAttempted, at, revision, position.X, position.Y, roll.First,
                roll.Second ?? 0, roll.Natural, modifier, roll.Natural + (long)modifier, DieSelection(roll.Selection),
                before, roll.NextRandomState, roll.WordsConsumed);
            var results = observerFacts.Select(fact =>
            {
                var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, fact.Dc);
                var degree = ObservationDegree(check.Degree);
                return new ObservationHideResultRecord(attemptId, fact.Actor, fact.Position.X, fact.Position.Y,
                    fact.Dc, degree, check.Success);
            }).ToArray();
            s.ObservationActions = s.ObservationActions.Concat(new[] { action }).ToArray();
            s.ObservationHideResults = s.ObservationHideResults.Concat(results).ToArray();
            s.RandomState = roll.NextRandomState;
            foreach (var result in results.Where(x => x.HiddenEstablished))
                ObservationRules.ApplyHide(s, result.ObserverId, actor, attemptId, at, revision);
            return action;
        }

        private NativeCommandConstraintV1 SearchCandidateConstraintV1(Snapshot s, Command c,
            ObservationPoint candidateCell, out ActorState[] targets)
        {
            targets = s.Actors.Where(x => x.Id != c.Actor && s.WorldSchedule.Order.Contains(x.Id)
                    && ObservationRules.HiddenTo(s, c.Actor, x.Id))
                .Where(x =>
                {
                    var point = ObservationGeometry.Position(s, x.Id);
                    return IsGridCell(point.X) && IsGridCell(point.Y) && point.X == candidateCell.X && point.Y == candidateCell.Y;
                }).OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            if (targets.Length > 1) return new NativeCommandConstraintV1("SearchCandidateAmbiguous",
                "engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs", 273);
            return null;
        }

        private string ResolveSearch(Snapshot s, Command c, ObservationPoint candidateCell)
        {
            var failure=SearchCandidateConstraintV1(s,c,candidateCell,out var targets);
            if(failure!=null)return failure.NativeCode;
            var hide = targets.Length == 0 ? null : ActiveSearchHide(s, c.Actor, targets[0].Id);
            RecordSearchResult(s, c.Actor, candidateCell, hide,c);
            return null;
        }

        private static ObservationActionRecord ActiveSearchHide(Snapshot state, string observer, string target)
        {
            var knowledge = state.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target);
            return state.ObservationActions.Single(x => x.Id == knowledge.HiddenAttemptId && x.Kind == ObservationActionKind.Hide);
        }

        private static ObservationActionRecord RecordSearchResult(Snapshot s, string actor, ObservationPoint candidateCell,
            ObservationActionRecord hide,Command command=null)
        {
            long revision = s.Revision + 1;
            string attemptId = "observation." + revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".search";
            RuleTime at = s.RuleClock;
            if (hide == null)
            {
                var noFinding = new ObservationActionRecord(attemptId, actor, "", ObservationActionKind.Search,
                    ObservationActionOutcome.SearchNoFinding, at, revision, candidateCell.X, candidateCell.Y,
                    0, 0, 0, 0, 0, ObservationDieSelection.None, s.RandomState, s.RandomState, 0);
                s.ObservationActions = s.ObservationActions.Append(noFinding).ToArray();
                return noFinding;
            }

            int dc = checked((int)hide.Total);
            var actorFacts = CharacterStateFacts.ForActor(s, actor, "perception");
            int modifier = checked(actorFacts.TotalWithInjury(CharacterAbility.Wisdom, perception: true)
                +ConsumeGuidance(s,command,attemptId,GuidanceCheckKind.Search));
            int disadvantage = TestOnlyClubAttackPolicy.ConditionsFor(s, actor).View().Has(ConditionKind.Poisoned)
                || FrightenedRules.VisibleSource(s, actor) ? 1 : 0;
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, dc);
            bool found = check.Success;
            var action = new ObservationActionRecord(attemptId, actor, found ? hide.ActorId : "", ObservationActionKind.Search,
                found ? ObservationActionOutcome.SearchFound : ObservationActionOutcome.SearchNoFinding, at, revision,
                candidateCell.X, candidateCell.Y, roll.First, roll.Second ?? 0, roll.Natural, modifier,
                roll.Natural + (long)modifier, DieSelection(roll.Selection), before, roll.NextRandomState, roll.WordsConsumed);
            s.ObservationActions = s.ObservationActions.Concat(new[] { action }).ToArray();
            s.RandomState = roll.NextRandomState;
            if (found) ObservationRules.DiscloseLocation(s, actor, hide.ActorId, ObservationEvidenceKind.Search, at, revision);
            return action;
        }

        private static bool IsGridCell(RuleQuantity x) => x.Denominator == 1;
        private static ObservationDieSelection DieSelection(D20Selection selection)
            => selection == D20Selection.Normal ? ObservationDieSelection.Normal
                : selection == D20Selection.Advantage ? ObservationDieSelection.Advantage : ObservationDieSelection.Disadvantage;
        private static ObservationTaskDegree ObservationDegree(TaskDegree degree)
            => degree == TaskDegree.CriticalSuccess ? ObservationTaskDegree.CriticalSuccess
                : degree == TaskDegree.Success ? ObservationTaskDegree.Success
                : degree == TaskDegree.Failure ? ObservationTaskDegree.Failure : ObservationTaskDegree.CriticalFailure;

        private static int PassivePerception(Snapshot s, string actor)
        {
            var check = AbilityCheckRules.Derive(s, actor, "perception", CharacterAbility.Wisdom);
            return checked(10 + check.Total);
        }

        private static bool WithinRange(ObservationPoint a, ObservationPoint b, long rangeFeet)
        {
            BigInteger dx = BigInteger.Abs((BigInteger)a.X.Numerator * b.X.Denominator
                - (BigInteger)b.X.Numerator * a.X.Denominator);
            BigInteger dxDenominator = (BigInteger)a.X.Denominator * b.X.Denominator;
            BigInteger dy = BigInteger.Abs((BigInteger)a.Y.Numerator * b.Y.Denominator
                - (BigInteger)b.Y.Numerator * a.Y.Denominator);
            BigInteger dyDenominator = (BigInteger)a.Y.Denominator * b.Y.Denominator;
            BigInteger limit = (BigInteger)rangeFeet;
            return dx * 5 <= limit * dxDenominator && dy * 5 <= limit * dyDenominator;
        }
    }
}
#endif
