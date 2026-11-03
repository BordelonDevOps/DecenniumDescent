#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>
    /// Explicit new schema-2 technical fixture. All stock, time, bookings and draws are
    /// synthetic; there is no fishing/crafting yield, actual labor credit or job completion.
    /// Shares the existing world fixture and the authoritative Simulation/FileSaveStore path.
    /// </summary>
    public sealed class TestOnlyWorkPolicy : ICommandPolicy
    {
        public const string JobId = "TEST_ONLY.work";
        public const string LotId = "TEST_ONLY.material";
        public const string ClaimId = "TEST_ONLY.reservation";
        private readonly TestOnlyPolicy world = new TestOnlyPolicy();
        public string ContentFingerprint => "TEST_ONLY.work-session-v1";
        public bool TestOnly => true;
        public Snapshot Initial()
        {
            var state = world.Initial();
            state.SchemaVersion = Snapshot.WorkSchema;
            state.ContentFingerprint = ContentFingerprint;
            state.Work = new WorkLedger(new[] { new ResourceLot(LotId, "TEST_ONLY.unit", 10,
                "TEST_ONLY.store", TestOnlyPolicy.CompanionId) });
            return state;
        }
        public string ValidateState(Snapshot state)
        {
            if (state.SchemaVersion != Snapshot.WorkSchema || state.Work == null) return "WrongFixtureSchema";
            string invalidWorld = TestOnlyPolicy.ValidateWorld(state);
            if (invalidWorld != null) return invalidWorld;
            var ledger = state.Work;
            if (ledger.Lots.Count != 1 || ledger.WorkerIntervals.Count > 1 || ledger.Reservations.Count > 1
                || ledger.WorkerIntervals.Count != ledger.Reservations.Count) return "InvalidFixtureWork";
            var claim = ledger.Reservations.SingleOrDefault();
            var work = ledger.WorkerIntervals.SingleOrDefault();
            if (claim != null && (claim.Id != ClaimId || claim.JobId != JobId || claim.LotId != LotId || claim.Quantity != 3))
                return "InvalidFixtureClaim";
            if (work != null && (work.Id != "TEST_ONLY.booking" || work.JobId != JobId
                || work.WorkerId != TestOnlyPolicy.CompanionId || work.Start > state.RuleClock
                || (BigInteger)work.End.Numerator * work.Start.Denominator
                    - (BigInteger)work.Start.Numerator * work.End.Denominator
                    != (BigInteger)work.Start.Denominator * work.End.Denominator)) return "InvalidFixtureBooking";
            var lot = ledger.Lots[0];
            if (lot.Id != LotId || lot.UnitId != "TEST_ONLY.unit" || lot.LocationId != "TEST_ONLY.store"
                || lot.CustodianId != TestOnlyPolicy.CompanionId
                || lot.Quantity != (claim != null && claim.Status == ReservationStatus.Consumed ? 7 : 10))
                return "InvalidFixtureStock";
            return null;
        }
        public string Resolve(Snapshot state, Command command)
        {
            if (command.Kind == CommandKind.AdvanceClock)
            {
                // Explicit fraction of a second requested by the harness, never frame time or a Watch.
                if (command.Target != "" || command.X < 1 || command.X > 10 || command.Y < 1 || command.Y > 10)
                    return "InvalidExactAdvance";
                state.RuleClock = RuleTime.FromFraction((BigInteger)state.RuleClock.Numerator * command.Y
                    + (BigInteger)command.X * state.RuleClock.Denominator, (BigInteger)state.RuleClock.Denominator * command.Y);
                return null;
            }
            if (command.Kind == CommandKind.Move || command.Kind == CommandKind.Interact) return world.Resolve(state, command);
            if (command.Actor != TestOnlyPolicy.CompanionId) return "WrongWorker";
            if (command.X != 0 || command.Y != 0) return "InvalidWorkRequest";
            if (command.Kind == CommandKind.ReserveWork)
            {
                if (command.Target != JobId) return "UnknownJob";
                if (state.Work.Reservations.Count != 0) return "AlreadyReserved";
                state.Work = state.Work.Reserve(JobId, new[] { new WorkerInterval("TEST_ONLY.booking", JobId,
                    command.Actor, state.RuleClock, state.RuleClock.AddSeconds(1)) },
                    new[] { new ResourceReservation(ClaimId, JobId, LotId, 3) });
                return null;
            }
            if (command.Kind == CommandKind.ConsumeReservation || command.Kind == CommandKind.ReleaseReservation)
            {
                if (command.Target != ClaimId) return "UnknownReservation";
                var claim = state.Work.Reservations.SingleOrDefault();
                if (claim == null) return "NotReserved";
                if (claim.Status != ReservationStatus.Reserved) return "AlreadySettled";
                if (command.Kind == CommandKind.ReleaseReservation) state.Work = state.Work.Release(JobId, ClaimId);
                else
                {
                    state.Work = state.Work.Consume(JobId, ClaimId);
                    // A synthetic draw verifies that debit, receipt and RNG commit together.
                    // It does not award anything or implement a Decennium outcome table.
                    state.RandomState = DiceStream.Draw(state.RandomState, 20).NextState;
                }
                return null;
            }
            return "UnsupportedCommand";
        }
    }
}
#endif
