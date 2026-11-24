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
            => ShortRestAccessConstraintV1(state, active)?.NativeCode;

        private NativeCommandConstraintV1 ShortRestAccessConstraintV1(Snapshot state, ShortRestRecord active)
        {
            const string actor = ShortRestBerth.Actor;
            if (active == null && state.InventoryCombat || ShortRestEncounter(state))
                return new NativeCommandConstraintV1("ShortRestRequiresOrdinaryExploration", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 25);
            var body = state.Actors.Single(x => x.Id == actor);
            if (body.X != ShortRestBerth.X || body.Y != ShortRestBerth.Y
                || !WorldWalkable(state, ShortRestBerth.X, ShortRestBerth.Y)
                || state.WorldTraversals.Any(x => x.ActorId == actor))
                return new NativeCommandConstraintV1("ShortRestRequiresStationaryBerthAccess", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 30);
            if (state.Actors.Any(x => x.Id != actor && x.X == ShortRestBerth.X && x.Y == ShortRestBerth.Y))
                return new NativeCommandConstraintV1("ShortRestBerthOccupied", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 32);
            if (state.Lives.Single(x => x.ActorId == actor).Dead) return new NativeCommandConstraintV1("ShortRestActorDead", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 33);
            if (state.Work.WorkerIntervals.Any(x => x.JobId != active?.Id && x.WorkerId == actor
                    && x.Start <= state.RuleClock && x.End > state.RuleClock)
                || WorldActivityProjection.CurrentWork(state).Any(x => x.ActorId == actor && x.Id != active?.Id))
                return new NativeCommandConstraintV1("ShortRestActorOccupied", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 37);
            return null;
        }

        private NativeCommandConstraintV1 ShortRestOpeningConstraintV1(Snapshot state, Command command)
        {
            if (!state.ConnectedShortRest || command.Actor != ShortRestBerth.Actor) return new NativeCommandConstraintV1("ShortRestUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 43);
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null)
                return new NativeCommandConstraintV1("UnsupportedShortRestSelection", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 49);
            if (PendingCalendarChoice(state) || ManufacturingChoicePending(state) || HasPendingRecoveryOffer(state)
                || state.ManufacturingAdvance != null) return new NativeCommandConstraintV1("ShortRestPendingChoice", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 51);
            var active = ShortRestBerth.Active(state);
            if (command.Kind == CommandKind.InterruptShortRest) {
                if (active == null || command.Target != active.Id) return new NativeCommandConstraintV1("NoMatchingActiveShortRest", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 54);
                return null;
            }
            bool mutation = command.Kind == CommandKind.BeginMutationShortRest;
            if (mutation) {
                var failure = MutationRestConstraintV1(state, command.Target);
                if (failure != null) return failure;
            } else if (command.Target != ShortRestBerth.Id) return new NativeCommandConstraintV1("ShortRestSiteUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 62);
            if (active != null) return new NativeCommandConstraintV1("ShortRestAlreadyActive", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 63);
            var access = ShortRestAccessConstraintV1(state, null);
            if (access != null) return access;
            if (state.ShortRests.Length == ShortRestBerth.MaxAttempts) return new NativeCommandConstraintV1("ShortRestHistoryCapacityReached", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 66);
            return null;
        }

        private static NativeCommandConstraintV1 ShortRestWindowConstraintV1(Snapshot state, string actor, RuleTime startedAt)
        {
            // Same lazy arithmetic as ShortRestRecord.DueAt inside the native overlap predicate.
            return state.Work.WorkerIntervals.Any(x => x.WorkerId == actor
                && x.Start < startedAt.AddSeconds(ShortRestBerth.DurationSeconds) && x.End > startedAt)
                ? new NativeCommandConstraintV1("ShortRestActorOccupied", "engine/com.decennium.foundation/Laboratory/Model/SharedShortRest.cs", 69) : null;
        }

        private NativeCommandConstraintV1 ShortRestConstraintV1(Snapshot state, Command command)
        {
            var failure = ShortRestOpeningConstraintV1(state, command);
            return failure != null || command.Kind == CommandKind.InterruptShortRest ? failure
                : ShortRestWindowConstraintV1(state, command.Actor, state.RuleClock);
        }

        private string ResolveShortRest(Snapshot state, Command command)
        {
            var failure = ShortRestOpeningConstraintV1(state, command);
            if (failure != null) return failure.NativeCode;
            if (command.Kind == CommandKind.InterruptShortRest) {
                EndShortRest(state, ShortRestBerth.Active(state), command, ShortRestInterruption.Explicit);
                return null;
            }
            bool mutation = command.Kind == CommandKind.BeginMutationShortRest;
            var rest = new ShortRestRecord(state.ShortRests.Length, command.Id, state.Revision + 1, state.RuleClock);
            var window = ShortRestWindowConstraintV1(state, command.Actor, rest.StartedAt);
            if (window != null) return window.NativeCode;
            state.Work = state.Work.Reserve(rest.Id, new[] {
                new WorkerInterval(ShortRestBerth.OccupancyId(rest.Id), rest.Id, command.Actor, rest.StartedAt, rest.DueAt)
            }, Array.Empty<ResourceReservation>());
            state.ShortRests = state.ShortRests.Append(rest).ToArray();
            if (mutation) AddMutationRestChoice(state, rest, command.Target);
            return null;
        }

        private void ReconcileShortRest(Snapshot state, Command command)
        {
            var rest = ShortRestBerth.Active(state);
            if (rest == null) return;
            var choice = FleshWardenProfile.Choice(state, rest.Id);
            if (ShortRestAccess(state, rest) != null || choice != null && MutationRestAccess(state, choice.MutationId) != null) {
                EndShortRest(state, rest, command, ShortRestEncounter(state)
                    ? ShortRestInterruption.Encounter : ShortRestInterruption.AccessLost);
                return;
            }
            if (state.RuleClock == rest.DueAt) EndShortRest(state, rest, command, ShortRestInterruption.None);
        }

        private static bool ShortRestEncounter(Snapshot state)
            // Ordinary exploration retains its sparse calendar and roster after tactical exit.
            => state.InventoryCombat && (state.Encounter == null || state.Encounter.Order.Contains(ShortRestBerth.Actor));

        private static void EndShortRest(Snapshot state, ShortRestRecord rest, Command command, ShortRestInterruption interruption)
        {
            bool completed = interruption == ShortRestInterruption.None;
            var benefit = !completed ? ShortRestBenefit.NotCompleted : ShortRestBerth.BenefitsUsed(state) < ShortRestBerth.InitialBenefits
                ? ShortRestBenefit.Eligible : ShortRestBenefit.Ineligible;
            if (!completed) state.Work = state.Work.CancelFutureWork(rest.Id, state.RuleClock);
            var ended = new ShortRestRecord(rest.Sequence, rest.StartCommandId, rest.StartRevision, rest.StartedAt,
                completed ? ShortRestOutcome.Completed : ShortRestOutcome.Interrupted, benefit, interruption,
                command.Id, state.Revision + 1, state.RuleClock);
            if (completed) CompleteMutationRest(state, ended);
            state.ShortRests = state.ShortRests.Select(x => x.Id == rest.Id ? ended : x).ToArray();
        }
    }
}
#endif
