#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedShortRest;

        internal TestOnlySharedWorldPolicy EnableConnectedShortRest()
        {
            EnableConnectedConsumeDecay();
            connectedShortRest = true;
            ContentFingerprint = ShortRestBerth.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                ShortRestBerth.SourceRevision, ShortRestBerth.Id, ShortRestBerth.Actor,
                "sheltered-0,1|fixed-owner|no-fee|one-occupant|ordinary-only|elapsed-3600|zero-dice|two-initial-benefits|warrior-strain-zero|no-owned-rest-refresh|no-reset"));
            return this;
        }

        private string ShortRestAccess(Snapshot state, ShortRestRecord active)
        {
            const string actor = ShortRestBerth.Actor;
            if (active == null && (state.InventoryCombat || state.Encounter != null) || ShortRestEncounter(state))
                return "ShortRestRequiresOrdinaryExploration";
            var body = state.Actors.Single(x => x.Id == actor);
            if (body.X != ShortRestBerth.X || body.Y != ShortRestBerth.Y
                || !WorldWalkable(state, ShortRestBerth.X, ShortRestBerth.Y)
                || state.WorldTraversals.Any(x => x.ActorId == actor))
                return "ShortRestRequiresStationaryBerthAccess";
            if (state.Actors.Any(x => x.Id != actor && x.X == ShortRestBerth.X && x.Y == ShortRestBerth.Y))
                return "ShortRestBerthOccupied";
            if (state.Lives.Single(x => x.ActorId == actor).Dead) return "ShortRestActorDead";
            if (state.Work.WorkerIntervals.Any(x => x.JobId != active?.Id && x.WorkerId == actor
                    && x.Start <= state.RuleClock && x.End > state.RuleClock)
                || WorldActivityProjection.CurrentWork(state).Any(x => x.ActorId == actor && x.Id != active?.Id))
                return "ShortRestActorOccupied";
            return null;
        }

        private string ResolveShortRest(Snapshot state, Command command)
        {
            if (!state.ConnectedShortRest || command.Actor != ShortRestBerth.Actor) return "ShortRestUnavailable";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null)
                return "UnsupportedShortRestSelection";
            if (PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state)
                || state.ManufacturingAdvance != null) return "ShortRestPendingChoice";
            var active = ShortRestBerth.Active(state);
            if (command.Kind == CommandKind.InterruptShortRest) {
                if (active == null || command.Target != active.Id) return "NoMatchingActiveShortRest";
                EndShortRest(state, active, command, ShortRestInterruption.Explicit);
                return null;
            }
            if (command.Target != ShortRestBerth.Id) return "ShortRestSiteUnavailable";
            if (active != null) return "ShortRestAlreadyActive";
            string access = ShortRestAccess(state, null);
            if (access != null) return access;
            if (state.ShortRests.Length == ShortRestBerth.MaxAttempts) return "ShortRestHistoryCapacityReached";
            var rest = new ShortRestRecord(state.ShortRests.Length, command.Id, state.Revision + 1, state.RuleClock);
            if (state.Work.WorkerIntervals.Any(x => x.WorkerId == command.Actor && x.Start < rest.DueAt && x.End > rest.StartedAt))
                return "ShortRestActorOccupied";
            state.Work = state.Work.Reserve(rest.Id, new[] {
                new WorkerInterval(ShortRestBerth.OccupancyId(rest.Id), rest.Id, command.Actor, rest.StartedAt, rest.DueAt)
            }, Array.Empty<ResourceReservation>());
            state.ShortRests = state.ShortRests.Append(rest).ToArray();
            return null;
        }

        private void ReconcileShortRest(Snapshot state, Command command)
        {
            var rest = ShortRestBerth.Active(state);
            if (rest == null) return;
            if (ShortRestAccess(state, rest) != null) {
                EndShortRest(state, rest, command, ShortRestEncounter(state)
                    ? ShortRestInterruption.Encounter : ShortRestInterruption.AccessLost);
                return;
            }
            if (state.RuleClock == rest.DueAt) EndShortRest(state, rest, command, ShortRestInterruption.None);
        }

        private static bool ShortRestEncounter(Snapshot state)
            => state.Encounter?.Order.Contains(ShortRestBerth.Actor) == true || state.InventoryCombat && state.Encounter == null;

        private static void EndShortRest(Snapshot state, ShortRestRecord rest, Command command, ShortRestInterruption interruption)
        {
            bool completed = interruption == ShortRestInterruption.None;
            var benefit = !completed ? ShortRestBenefit.NotCompleted : ShortRestBerth.BenefitsUsed(state) < ShortRestBerth.InitialBenefits
                ? ShortRestBenefit.Eligible : ShortRestBenefit.Ineligible;
            if (!completed) state.Work = state.Work.CancelFutureWork(rest.Id, state.RuleClock);
            var ended = new ShortRestRecord(rest.Sequence, rest.StartCommandId, rest.StartRevision, rest.StartedAt,
                completed ? ShortRestOutcome.Completed : ShortRestOutcome.Interrupted, benefit, interruption,
                command.Id, state.Revision + 1, state.RuleClock);
            state.ShortRests = state.ShortRests.Select(x => x.Id == rest.Id ? ended : x).ToArray();
        }
    }
}
#endif
