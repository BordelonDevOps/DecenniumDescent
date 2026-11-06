#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        public string Resolve(Snapshot s, Command c)
        {
            string error = ResolveCore(s, c);
            if (error == null && s.SchemaVersion >= Snapshot.ObservationSchema)
                ObservationRules.Refresh(s, s.RuleClock, s.Revision + 1);
            return error;
        }

        private string ResolveObservationAction(Snapshot s, Command c)
        {
            if (observationFixture == null || s.SchemaVersion < Snapshot.ObservationSchema)
                return "ObservationActionNotImplemented";
            if (s.Encounter == null || !s.InventoryCombat) return "ObservationActionRequiresTacticalCombat";
            if (PendingCalendarChoice(s)) return "TacticalChoicePending";
            if (c.Actor != s.Encounter.CurrentActor || c.Target != s.Encounter.CurrentTurnId)
                return "WrongRegularTurn";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.SuppressionFire != null || c.ExpeditionAssignment != null || c.HarvestSelection != null
                || c.MiningSelection != null || c.ProspectingExposure != null || c.OverwatchRider != OverwatchRider.None)
                return "InvalidObservationActionPayload";
            if (!ActorLifeRules.CanAct(s, c.Actor)) return "ActorCannotAct";
            if (!Permissions(s, c.Actor).Action) return "ConditionPreventsAction";
            var interval = Interval(s, c.Actor);
            if (interval.ActionSpent) return "ActionAlreadySpent";
            if (s.ObservationActions.Length >= ObservationValidation.MaxAttempts) return "ObservationHistoryCapacityReached";

            string failure = c.Kind == CommandKind.Hide ? ResolveHide(s, c) : ResolveSearch(s, c);
            if (failure != null) return failure;
            SetInterval(s, interval.PayAction());
            PauseIncompatibleWork(s);
            return null;
        }

        private string ResolveHide(Snapshot s, Command c)
        {
            if (c.Target != s.Encounter.CurrentTurnId || c.X != 0 || c.Y != 0) return "InvalidHideRequest";
            var actor = s.Actors.Single(x => x.Id == c.Actor);
            var position = ObservationGeometry.Position(s, actor.Id);
            if (!IsGridCell(position.X) || !IsGridCell(position.Y)) return "HideRequiresAuthoredGridCell";

            var observers = s.Actors.Where(x => x.Id != actor.Id && ActorLifeRules.CanAct(s, x.Id)
                    && !TestOnlyClubAttackPolicy.ConditionsFor(s, x.Id).View().Unaware
                    && WithinRange(ObservationGeometry.Position(s, x.Id), position,
                        s.ObservationProfiles.Single(p => p.ActorId == x.Id).SightRangeFeet))
                .OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            if (observers.Any(x => ObservationRules.DirectSightAt(s, x.Id, actor.Id,
                    ObservationGeometry.Position(s, x.Id), position))) return "HideWhileClearlyObserved";
            if (s.ObservationHideResults.Length + observers.Length > ObservationValidation.MaxHideResults)
                return "ObservationHideHistoryCapacityReached";
            if (s.ObserverKnowledge.Length + observers.Count(x => !s.ObserverKnowledge.Any(k => k.ObserverId == x.Id && k.TargetId == actor.Id))
                > ObservationValidation.MaxKnowledgePairs) return "ObservationKnowledgeCapacityReached";

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

            var character = s.Characters.Single(x => x.ActorId == actor.Id);
            var training = s.SkillTraining.SingleOrDefault(x => x.ActorId == actor.Id && x.SkillId == "stealth");
            int modifier = AbilityCheckRules.Derive(character, training, 1)
                .TotalWithInjury(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == actor.Id)));
            int disadvantage = TestOnlyClubAttackPolicy.ConditionsFor(s, actor.Id).View().Has(ConditionKind.Poisoned) ? 1 : 0;
            var selection = PlaytestDice.Selection(0, disadvantage);
            var observerFacts = observers.Select(observer => new
            {
                Actor = observer,
                Position = ObservationGeometry.Position(s, observer.Id),
                Dc = PassivePerception(s, observer.Id)
            }).ToArray();
            var prior = s.ObservationActions.Where(x => x.ActorId == actor.Id && x.Kind == ObservationActionKind.Hide)
                .OrderByDescending(x => x.Revision).FirstOrDefault();
            if (prior != null && prior.Outcome == ObservationActionOutcome.HideAttempted
                && prior.X == position.X && prior.Y == position.Y && prior.Modifier == modifier
                && prior.Selection == DieSelection(selection))
            {
                var priorResults = s.ObservationHideResults.Where(x => x.AttemptId == prior.Id)
                    .OrderBy(x => x.ObserverId, StringComparer.Ordinal).ToArray();
                bool unchanged = priorResults.Length == observerFacts.Length
                    && observerFacts.OrderBy(x => x.Actor.Id, StringComparer.Ordinal).Select((x, i) =>
                        priorResults[i].ObserverId == x.Actor.Id && priorResults[i].Dc == x.Dc
                            && priorResults[i].ObserverX == x.Position.X && priorResults[i].ObserverY == x.Position.Y).All(x => x);
                if (unchanged && priorResults.Any(x => !x.HiddenEstablished)) return "HideAttemptUnchanged";
            }
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var action = new ObservationActionRecord(attemptId, actor.Id, "", ObservationActionKind.Hide,
                ObservationActionOutcome.HideAttempted, at, revision, position.X, position.Y, roll.First,
                roll.Second ?? 0, roll.Natural, modifier, roll.Natural + (long)modifier, DieSelection(roll.Selection),
                before, roll.NextRandomState, roll.WordsConsumed);
            var results = observerFacts.Select(fact =>
            {
                var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, fact.Dc);
                var degree = ObservationDegree(check.Degree);
                return new ObservationHideResultRecord(attemptId, fact.Actor.Id, fact.Position.X, fact.Position.Y,
                    fact.Dc, degree, check.Success);
            }).ToArray();
            s.ObservationActions = s.ObservationActions.Concat(new[] { action }).ToArray();
            s.ObservationHideResults = s.ObservationHideResults.Concat(results).ToArray();
            s.RandomState = roll.NextRandomState;
            foreach (var result in results.Where(x => x.HiddenEstablished))
                ObservationRules.ApplyHide(s, result.ObserverId, actor.Id, attemptId, at, revision);
            return null;
        }

        private string ResolveSearch(Snapshot s, Command c)
        {
            if (c.Target != s.Encounter.CurrentTurnId || c.X < 0 || c.Y < 0
                || c.X >= s.ObservationMapWidth || c.Y >= s.ObservationMapHeight) return "InvalidSearchRequest";
            var profile = s.ObservationProfiles.Single(x => x.ActorId == c.Actor);
            var searcher = ObservationGeometry.Position(s, c.Actor);
            var candidateCell = new ObservationPoint(new RuleQuantity(c.X), new RuleQuantity(c.Y));
            if (!WithinRange(searcher, candidateCell, profile.SearchRangeFeet)) return "SearchCellOutOfRange";
            var targets = s.Actors.Where(x => x.Id != c.Actor && s.WorldSchedule.Order.Contains(x.Id)
                    && ObservationRules.HiddenTo(s, c.Actor, x.Id))
                .Where(x =>
                {
                    var point = ObservationGeometry.Position(s, x.Id);
                    return IsGridCell(point.X) && IsGridCell(point.Y) && point.X == candidateCell.X && point.Y == candidateCell.Y;
                }).OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            if (targets.Length > 1) return "SearchCandidateAmbiguous";
            long revision = s.Revision + 1;
            string attemptId = "observation." + revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".search";
            RuleTime at = s.RuleClock;
            if (targets.Length == 0)
            {
                s.ObservationActions = s.ObservationActions.Concat(new[] { new ObservationActionRecord(attemptId, c.Actor, "",
                    ObservationActionKind.Search, ObservationActionOutcome.SearchNoFinding, at, revision, candidateCell.X, candidateCell.Y,
                    0, 0, 0, 0, 0, ObservationDieSelection.None, s.RandomState, s.RandomState, 0) }).ToArray();
                return null;
            }

            var target = targets[0];
            var knowledge = s.ObserverKnowledge.Single(x => x.ObserverId == c.Actor && x.TargetId == target.Id);
            var hide = s.ObservationActions.Single(x => x.Id == knowledge.HiddenAttemptId && x.Kind == ObservationActionKind.Hide);
            int dc = checked((int)hide.Total);
            var character = s.Characters.Single(x => x.ActorId == c.Actor);
            var training = s.SkillTraining.SingleOrDefault(x => x.ActorId == c.Actor && x.SkillId == "perception");
            int modifier = AbilityCheckRules.Derive(character, training, 4)
                .TotalWithInjury(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == c.Actor)), perception: true);
            int disadvantage = TestOnlyClubAttackPolicy.ConditionsFor(s, c.Actor).View().Has(ConditionKind.Poisoned) ? 1 : 0;
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, dc);
            bool found = check.Success;
            var action = new ObservationActionRecord(attemptId, c.Actor, found ? target.Id : "", ObservationActionKind.Search,
                found ? ObservationActionOutcome.SearchFound : ObservationActionOutcome.SearchNoFinding, at, revision,
                candidateCell.X, candidateCell.Y, roll.First, roll.Second ?? 0, roll.Natural, modifier,
                roll.Natural + (long)modifier, DieSelection(roll.Selection), before, roll.NextRandomState, roll.WordsConsumed);
            s.ObservationActions = s.ObservationActions.Concat(new[] { action }).ToArray();
            s.RandomState = roll.NextRandomState;
            if (found) ObservationRules.DiscloseLocation(s, c.Actor, target.Id, ObservationEvidenceKind.Search, at, revision);
            return null;
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
            var character = s.Characters.Single(x => x.ActorId == actor);
            var training = s.SkillTraining.SingleOrDefault(x => x.ActorId == actor && x.SkillId == "perception");
            var check = AbilityCheckRules.Derive(character, training, 4);
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
