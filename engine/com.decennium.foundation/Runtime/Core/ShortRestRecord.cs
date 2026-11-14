using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ShortRestOutcome { Active, Interrupted, Completed }
    public enum ShortRestBenefit { NotCompleted, Eligible, Ineligible }
    public enum ShortRestInterruption { None, Explicit, Encounter, AccessLost }

    /// <summary>A receipt-bound elapsed rest. WorkLedger owns its exclusive occupancy.</summary>
    public sealed class ShortRestRecord
    {
        public int Sequence { get; }
        public string Id => ShortRestBerth.IntervalPrefix + Sequence.ToString(CultureInfo.InvariantCulture);
        public string ActorId => ShortRestBerth.Actor;
        public string SiteId => ShortRestBerth.Id;
        public string StartCommandId { get; }
        public long StartRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime DueAt => StartedAt.AddSeconds(ShortRestBerth.DurationSeconds);
        public ShortRestOutcome Outcome { get; }
        public ShortRestBenefit Benefit { get; }
        public ShortRestInterruption Interruption { get; }
        public string EndCommandId { get; }
        public long EndRevision { get; }
        public RuleTime? EndedAt { get; }
        public int HitDiceSpent => 0;
        public int Healing => 0;
        public int WarriorStrainBefore => ShortRestBerth.InitialWarriorStrain;
        public int WarriorStrainAfter => ShortRestBerth.InitialWarriorStrain;
        public ShortRestBenefit WarriorStrainReduction => Benefit;
        public int RewardRandomWords => 0;

        public ShortRestRecord(int sequence, string startCommandId, long startRevision, RuleTime startedAt,
            ShortRestOutcome outcome = ShortRestOutcome.Active, ShortRestBenefit benefit = ShortRestBenefit.NotCompleted,
            ShortRestInterruption interruption = ShortRestInterruption.None, string endCommandId = "", long endRevision = 0,
            RuleTime? endedAt = null)
        {
            bool active = outcome == ShortRestOutcome.Active;
            bool completed = outcome == ShortRestOutcome.Completed;
            if (sequence < 0 || sequence >= ShortRestBerth.MaxAttempts || !Validation.ValidId(startCommandId)
                || startRevision < 1 || startedAt < default(RuleTime)
                || !Enum.IsDefined(typeof(ShortRestOutcome), outcome) || !Enum.IsDefined(typeof(ShortRestBenefit), benefit)
                || !Enum.IsDefined(typeof(ShortRestInterruption), interruption)
                || (completed ? benefit == ShortRestBenefit.NotCompleted : benefit != ShortRestBenefit.NotCompleted)
                || (outcome == ShortRestOutcome.Interrupted ? interruption == ShortRestInterruption.None : interruption != ShortRestInterruption.None)
                || (active ? endedAt.HasValue || endCommandId != "" || endRevision != 0
                    : !endedAt.HasValue || !Validation.ValidId(endCommandId) || endRevision <= startRevision
                        || endedAt < startedAt || endedAt > startedAt.AddSeconds(ShortRestBerth.DurationSeconds))
                || completed && endedAt != startedAt.AddSeconds(ShortRestBerth.DurationSeconds))
                throw new ArgumentException("Invalid Short Rest interval or result.");
            Sequence = sequence;
            StartCommandId = startCommandId;
            StartRevision = startRevision;
            StartedAt = startedAt;
            Outcome = outcome;
            Benefit = benefit;
            Interruption = interruption;
            EndCommandId = endCommandId;
            EndRevision = endRevision;
            EndedAt = endedAt;
        }
    }

    /// <summary>Approved bounded TEST_ONLY facts; no Long Rest or mutation authority is implied.</summary>
    public static class ShortRestBerth
    {
        public const string FingerprintPrefix = "TEST_ONLY.short-rest-v1-";
        public const string Id = "TEST_ONLY.short-rest-berth";
        public const string Actor = ConnectedVialRules.CarrierId;
        public const string IntervalPrefix = "TEST_ONLY.short-rest.";
        public const byte Marker = 8;
        public const int X = 0;
        public const int Y = 1;
        public const int DurationSeconds = 3600;
        public const int InitialBenefits = 2;
        public const int InitialWarriorStrain = 0;
        public const int MaxAttempts = 1024; // Technical history capacity, not a rest-use rule.
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";

        public static bool SelectedFingerprint(string fingerprint) => fingerprint.StartsWith(FingerprintPrefix, StringComparison.Ordinal);
        public static bool IsCommand(CommandKind kind) => kind == CommandKind.BeginShortRest || kind == CommandKind.InterruptShortRest;
        public static ShortRestRecord Active(Snapshot state)
            => state.ConnectedShortRest ? state.ShortRests.SingleOrDefault(x => x.Outcome == ShortRestOutcome.Active) : null;
        public static int BenefitsUsed(Snapshot state) => state.ShortRests.Count(x => x.Benefit == ShortRestBenefit.Eligible);
        public static string OccupancyId(string interval) => interval + ".occupancy";
        public static bool RestOccupancy(Snapshot state, WorkerInterval interval)
            => state.ConnectedShortRest && interval.WorkerId == Actor && interval.Id == OccupancyId(interval.JobId)
                && state.ShortRests.Any(x => x.Id == interval.JobId);

        internal static void Validate(Snapshot state)
        {
            var rests = state.ShortRests;
            if (rests == null || rests.Length > MaxAttempts || rests.Any(x => x == null)
                || state.ConnectedShortRest != SelectedFingerprint(state.ContentFingerprint)
                || !state.ConnectedShortRest && rests.Length != 0)
                throw new ArgumentException("Invalid Short Rest envelope.");
            if (!state.ConnectedShortRest) return;
            if (!state.TestOnly || !state.ConnectedConsumeDecay || state.SchemaVersion != Snapshot.SurpriseEntrySchema)
                throw new ArgumentException("Short Rest requires its selected connected profile.");
            long previousRevision = 0;
            RuleTime previousEnd = default;
            int benefits = 0;
            for (int index = 0; index < rests.Length; index++) {
                var rest = rests[index];
                bool active = rest.Outcome == ShortRestOutcome.Active;
                if (rest.Sequence != index || rest.StartRevision <= previousRevision || rest.StartRevision > state.Revision
                    || rest.StartedAt < previousEnd || rest.StartedAt > state.RuleClock
                    || active && (index != rests.Length - 1 || rest.DueAt <= state.RuleClock)
                    || rest.EndRevision > state.Revision || rest.EndedAt > state.RuleClock)
                    throw new ArgumentException("Invalid Short Rest chronology.");
                var start = new Command(rest.StartCommandId, Actor, rest.StartRevision - 1, CommandKind.BeginShortRest, Id);
                if (!state.Receipts.Any(x => x.Revision == rest.StartRevision && x.Principal == "TEST_ONLY.host" && start.MatchesReceipt(x)))
                    throw new ArgumentException("Short Rest requires its exact start receipt.");
                if (!active) {
                    var terminal = state.Receipts.SingleOrDefault(x => x.Revision == rest.EndRevision);
                    if (terminal == null || terminal.Id != rest.EndCommandId)
                        throw new ArgumentException("Short Rest requires its terminal receipt.");
                    if (rest.Interruption == ShortRestInterruption.Explicit) {
                        var interrupt = new Command(rest.EndCommandId, Actor, rest.EndRevision - 1, CommandKind.InterruptShortRest, rest.Id);
                        if (terminal.Principal != "TEST_ONLY.host" || !interrupt.MatchesReceipt(terminal))
                            throw new ArgumentException("Invalid explicit Short Rest interruption receipt.");
                    }
                }
                if (rest.Outcome == ShortRestOutcome.Completed) {
                    var expected = benefits < InitialBenefits ? ShortRestBenefit.Eligible : ShortRestBenefit.Ineligible;
                    if (rest.Benefit != expected) throw new ArgumentException("Invalid Short Rest cadence or reward eligibility.");
                    if (rest.Benefit == ShortRestBenefit.Eligible) benefits++;
                }
                RuleTime end = rest.EndedAt ?? rest.DueAt;
                var occupancy = state.Work.WorkerIntervals.Where(x => x.JobId == rest.Id).ToArray();
                if (end == rest.StartedAt ? occupancy.Length != 0 : occupancy.Length != 1
                    || occupancy[0].Id != OccupancyId(rest.Id) || occupancy[0].WorkerId != Actor
                    || occupancy[0].Start != rest.StartedAt || occupancy[0].End != end)
                    throw new ArgumentException("Invalid Short Rest occupancy.");
                previousRevision = rest.EndRevision;
                previousEnd = end;
            }
            string startKind = ((int)CommandKind.BeginShortRest).ToString(CultureInfo.InvariantCulture) + "|";
            if (state.Receipts.Count(x => x.Fingerprint.StartsWith(startKind, StringComparison.Ordinal)) != rests.Length
                || state.Work.WorkerIntervals.Any(x => x.JobId.StartsWith(IntervalPrefix, StringComparison.Ordinal)
                    && !rests.Any(r => r.Id == x.JobId))
                || state.Work.Reservations.Any(x => x.JobId.StartsWith(IntervalPrefix, StringComparison.Ordinal)))
                throw new ArgumentException("Unattributed Short Rest history or resource claim.");
        }
    }
}
