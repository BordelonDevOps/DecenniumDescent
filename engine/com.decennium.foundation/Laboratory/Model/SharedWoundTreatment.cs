#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedWoundTreatment;

        internal TestOnlySharedWorldPolicy EnableConnectedWoundTreatment()
        {
            EnableConnectedCompanionStabilization();
            connectedWoundTreatment = true;
            ContentFingerprint = WoundTreatmentStation.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                "fixed-kit-1,2|patient-1,3|consent-stable-or-positive|tier1-dc12|elapsed-28800|sealed-two-baskets|packed-at-0"));
            return this;
        }

        private void InitializeWoundTreatment(Snapshot state)
        {
            if (!connectedWoundTreatment) return;
            state.ConnectedWoundTreatment = true;
            state.ConnectedConsumeDecay = connectedConsumeDecay;
            state.ConnectedShortRest = connectedShortRest;
            InitializeFleshWarden(state);
            var stock = new[] { WoundTreatmentStation.Kit }.Concat(
                Enumerable.Range(0, WoundTreatmentStation.BasketCount).SelectMany(WoundTreatmentStation.Stock)).ToArray();
            state.Work = new WorkLedger(state.Work.Lots.Concat(stock), state.Work.WorkerIntervals, state.Work.Reservations);
            state.InventoryLots = state.InventoryLots.Concat(stock.Select(WoundTreatmentStation.Provenance)).ToArray();
        }

        private string WoundTreatmentAccess(Snapshot state, WoundTreatmentRecord active)
            => WoundTreatmentAccessConstraintV1(state, active)?.NativeCode;

        private NativeCommandConstraintV1 WoundTreatmentAccessConstraintV1(Snapshot state, WoundTreatmentRecord active)
        {
            const string healer = WoundTreatmentStation.Healer;
            const string patient = WoundTreatmentStation.Patient;
            if (state.InventoryCombat || state.Encounter != null || !state.ClosedEncounters.Any(x => x.Encounter.Id == state.Reinforcement?.Definition.EncounterId))
                return new NativeCommandConstraintV1("WoundTreatmentRequiresOrdinaryStation", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 38);
            var worker = state.Actors.Single(x => x.Id == healer);
            var recipient = state.Actors.Single(x => x.Id == patient);
            if (worker.X != 1 || worker.Y != 2 || recipient.X != 1 || recipient.Y != 3
                || state.WorldTraversals.Any(x => x.ActorId == healer || x.ActorId == patient)
                || !ObservationGeometry.LineOfEffectClear(state, healer, patient))
                return new NativeCommandConstraintV1("WoundTreatmentRequiresStationaryAccess", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 44);
            if (!CapableWorker(state, healer) || !Permissions(state, healer).Action || AvailableHands(state, healer) < 1)
                return new NativeCommandConstraintV1("WoundTreatmentHealerIncapable", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 46);
            var life = state.Lives.Single(x => x.ActorId == patient);
            if (life.Dead || (life.Hp == 0 && !life.Stable) || life.LinkedInjuries.Count != 1
                || active != null && life.LinkedInjuries[0] != active.LinkedInjury)
                return new NativeCommandConstraintV1("WoundTreatmentPatientIneligible", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 50);
            if (state.Work.WorkerIntervals.Any(x => x.JobId != active?.Id && (x.WorkerId == healer || x.WorkerId == patient)
                    && x.Start <= state.RuleClock && x.End > state.RuleClock)
                || WorldActivityProjection.CurrentWork(state).Any(x => (x.ActorId == healer || x.ActorId == patient) && x.Id != active?.Id))
                return new NativeCommandConstraintV1("WoundTreatmentParticipantOccupied", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 54);
            return null;
        }

        private NativeCommandConstraintV1 WoundTreatmentOpeningConstraintV1(Snapshot state, Command command)
        {
            if (!state.ConnectedWoundTreatment || command.Actor != WoundTreatmentStation.Healer || command.Target != WoundTreatmentStation.Patient)
                return new NativeCommandConstraintV1("WoundTreatmentUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 61);
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null)
                return new NativeCommandConstraintV1("InvalidWoundTreatmentRequest", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 67);
            var active = WoundTreatmentStation.Active(state);
            if (command.Kind == CommandKind.InterruptWoundTreatment) {
                if (active == null) return new NativeCommandConstraintV1("NoActiveWoundTreatment", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 70);
                return null;
            }
            if (active != null) return new NativeCommandConstraintV1("WoundTreatmentAlreadyActive", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 74);
            var access = WoundTreatmentAccessConstraintV1(state, null);
            if (access != null) return access;
            if (state.WoundTreatments.Length == WoundTreatmentStation.BasketCount || state.RuleClock >= WoundTreatmentStation.ExpiresAt)
                return new NativeCommandConstraintV1("WoundTreatmentSupplyUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 78);
            return null;
        }

        private static NativeCommandConstraintV1 WoundTreatmentSupplyConstraintV1(Snapshot state, int basket, out ResourceLot[] inputs)
        {
            inputs = new[] { WoundTreatmentStation.Kit }.Concat(WoundTreatmentStation.Stock(basket)).ToArray();
            if (inputs.Any(x => !state.Work.Lots.Any(lot => lot.Id == x.Id && lot.CustodianId == x.CustodianId
                && lot.LocationId == x.LocationId && lot.UnitId == x.UnitId) || state.Work.AvailableAmount(x.Id) != x.Amount))
                return new NativeCommandConstraintV1("WoundTreatmentSupplyOrKitUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 85);
            return null;
        }

        private static NativeCommandConstraintV1 WoundTreatmentWindowConstraintV1(Snapshot state, Command command, RuleTime startedAt)
        {
            // Same lazy arithmetic as WoundTreatmentRecord.DueAt; no candidate job or claims.
            return state.Work.WorkerIntervals.Any(x => (x.WorkerId == command.Actor || x.WorkerId == command.Target)
                && x.Start < startedAt.AddSeconds(WoundTreatmentStation.DurationSeconds) && x.End > startedAt)
                ? new NativeCommandConstraintV1("WoundTreatmentParticipantOccupied", "engine/com.decennium.foundation/Laboratory/Model/SharedWoundTreatment.cs", 88) : null;
        }

        private NativeCommandConstraintV1 WoundTreatmentConstraintV1(Snapshot state, Command command)
        {
            var failure = WoundTreatmentOpeningConstraintV1(state, command);
            if (failure != null || command.Kind == CommandKind.InterruptWoundTreatment) return failure;
            return WoundTreatmentSupplyConstraintV1(state, state.WoundTreatments.Length, out _)
                ?? WoundTreatmentWindowConstraintV1(state, command, state.RuleClock);
        }

        private string ResolveWoundTreatment(Snapshot state, Command command)
        {
            var failure = WoundTreatmentOpeningConstraintV1(state, command);
            if (failure != null) return failure.NativeCode;
            if (command.Kind == CommandKind.InterruptWoundTreatment) {
                EndWoundTreatment(state, WoundTreatmentStation.Active(state), command, WoundTreatmentOutcome.Interrupted);
                return null;
            }
            var patient = state.Lives.Single(x => x.ActorId == WoundTreatmentStation.Patient);
            var job = new WoundTreatmentRecord(state.WoundTreatments.Length, command.Id, state.Revision + 1,
                state.RuleClock, patient.LinkedInjuries[0]);
            var supply = WoundTreatmentSupplyConstraintV1(state, job.Basket, out var inputs);
            if (supply != null) return supply.NativeCode;
            var window = WoundTreatmentWindowConstraintV1(state, command, job.StartedAt);
            if (window != null) return window.NativeCode;
            var intervals = new[] { command.Actor, command.Target }.Select(actor => new WorkerInterval(
                WoundTreatmentStation.IntervalId(job.Id, actor), job.Id, actor, job.StartedAt, job.DueAt));
            var claims = inputs.Select((lot, index) => new ResourceReservation(
                WoundTreatmentStation.ClaimId(job.Id, index), job.Id, lot.Id, lot.Amount)).ToArray();
            var work = state.Work.Reserve(job.Id, intervals, claims);
            foreach (var claim in claims.Skip(1)) work = work.Consume(job.Id, claim.Id);
            state.Work = work;
            state.WoundTreatments = state.WoundTreatments.Append(job).ToArray();
            return null;
        }

        private void ReconcileWoundTreatment(Snapshot state, Command command)
        {
            var job = WoundTreatmentStation.Active(state);
            if (job == null) return;
            if (WoundTreatmentAccess(state, job) != null
                || !state.Work.Reservations.Any(x => x.Id == WoundTreatmentStation.ClaimId(job.Id, 0)
                    && x.Status == ReservationStatus.Reserved)) {
                EndWoundTreatment(state, job, command, WoundTreatmentOutcome.Interrupted);
                return;
            }
            if (state.RuleClock != job.DueAt) return;

            const string healer = WoundTreatmentStation.Healer;
            const string patient = WoundTreatmentStation.Patient;
            long revision = state.Revision + 1;
            int modifier = CharacterStateFacts.ForActor(state, healer, "medicine").TotalWithInjury(CharacterAbility.Wisdom);
            bool disadvantage = View(state, healer).Has(ConditionKind.Poisoned)
                || ExpeditionStrainRules.Current(state, healer).ExpeditionCheckDisadvantage;
            var roll = PlaytestDice.RollD20(state.RandomState, disadvantageSources: disadvantage ? 1 : 0);
            var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, WoundTreatmentStation.Difficulty);
            var outcome = (WoundTreatmentOutcome)((int)WoundTreatmentOutcome.CriticalFailure + (int)check.Degree);
            if (check.Success) {
                var before = state.Lives.Single(x => x.ActorId == patient);
                var after = new ActorLifeRecord(before.ActorId, before.MaximumHp, before.Hp, before.TemporaryHp, Array.Empty<int>(),
                    before.Stable, before.Dead, before.UsesDeathSaves, before.DeathSuccesses, before.DeathFailures,
                    before.StableUntil, before.LastDeathTurn, before.Prone, before.HeldItems);
                state.Lives = state.Lives.Select(x => x.ActorId == patient ? after : x).ToArray();
            } else if (outcome == WoundTreatmentOutcome.CriticalFailure) {
                string gainId = job.Id + ".gain";
                var gain = new ExpeditionStrainGainRecord(gainId, gainId + ".point",
                    ExpeditionStrainCauseKind.WoundTreatmentCriticalFailure, job.Id,
                    ExpeditionStrainRules.NextGainSequence(state, patient, revision), patient,
                    WoundTreatmentStation.Prefix + "medicine", "expedition.strain", state.RuleClock, revision,
                    ExpeditionStrainRules.Project(state, patient, state.RuleClock, revision).Level,
                    1, 1, null, null, ExpeditionStrainEndpoint.None);
                AppendStrainGain(state, gain);
            }
            EndWoundTreatment(state, job, command, outcome, roll, modifier);
            state.RandomState = roll.NextRandomState;
        }

        private static void EndWoundTreatment(Snapshot state, WoundTreatmentRecord job, Command command,
            WoundTreatmentOutcome outcome, D20Roll roll = null, int modifier = 0)
        {
            state.Work = state.Work.Release(job.Id, WoundTreatmentStation.ClaimId(job.Id, 0));
            if (outcome == WoundTreatmentOutcome.Interrupted)
                state.Work = state.Work.CancelFutureWork(job.Id, state.RuleClock);
            var ended = new WoundTreatmentRecord(job.Basket, job.StartCommandId, job.StartRevision, job.StartedAt, job.LinkedInjury,
                outcome, command.Id, state.Revision + 1, state.RuleClock, roll?.First ?? 0, roll?.Second ?? 0,
                roll?.Natural ?? 0, modifier, roll == null ? 0 : state.RandomState, roll?.NextRandomState ?? 0, roll?.WordsConsumed ?? 0);
            state.WoundTreatments = state.WoundTreatments.Select(x => x.Id == job.Id ? ended : x).ToArray();
        }
    }
}
#endif
