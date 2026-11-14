using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public enum WoundTreatmentOutcome { Active, Interrupted, CriticalFailure, Failure, Success, CriticalSuccess }

    /// <summary>A fixed vessel at the selected treatment station. Contents are held in WorkLedger.</summary>
    public sealed class WoundTreatmentVessel
    {
        public string Id { get; }
        public string LotId { get; }
        public int CapacityPints { get; }
        public RuleQuantity TarePounds { get; }
        public RuleQuantity ContentPoundsPerPint { get; }

        internal WoundTreatmentVessel(string id, string lotId, int capacity, RuleQuantity tare, RuleQuantity contentPoundsPerPint)
        {
            Id = id;
            LotId = lotId;
            CapacityPints = capacity;
            TarePounds = tare;
            ContentPoundsPerPint = contentPoundsPerPint;
        }

        public RuleQuantity GrossPounds(WorkLedger work)
            => TarePounds + work.Lots.Single(x => x.Id == LotId).Amount.Scale(
                ContentPoundsPerPint.Numerator, ContentPoundsPerPint.Denominator);
    }

    public sealed class WoundTreatmentRecord
    {
        public string Id => WoundTreatmentStation.Prefix + Basket.ToString(CultureInfo.InvariantCulture);
        public int Basket { get; }
        public string StartCommandId { get; }
        public long StartRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime DueAt => StartedAt.AddSeconds(WoundTreatmentStation.DurationSeconds);
        public int LinkedInjury { get; }
        public WoundTreatmentOutcome Outcome { get; }
        public string EndCommandId { get; }
        public long EndRevision { get; }
        public RuleTime? EndedAt { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }

        public WoundTreatmentRecord(int basket, string startCommandId, long startRevision, RuleTime startedAt, int linkedInjury,
            WoundTreatmentOutcome outcome = WoundTreatmentOutcome.Active, string endCommandId = "", long endRevision = 0,
            RuleTime? endedAt = null, int first = 0, int second = 0, int natural = 0, int modifier = 0,
            uint randomBefore = 0, uint randomAfter = 0, long wordsConsumed = 0)
        {
            bool active = outcome == WoundTreatmentOutcome.Active;
            bool checkedMedicine = outcome >= WoundTreatmentOutcome.CriticalFailure;
            if (basket < 0 || basket >= WoundTreatmentStation.BasketCount || !Validation.ValidId(startCommandId)
                || startRevision < 1 || startedAt < default(RuleTime) || linkedInjury < 0 || linkedInjury > 6
                || !Enum.IsDefined(typeof(WoundTreatmentOutcome), outcome)
                || (active ? endedAt.HasValue || endCommandId != "" || endRevision != 0
                    : !endedAt.HasValue || !Validation.ValidId(endCommandId) || endRevision <= startRevision
                        || endedAt.Value < startedAt || endedAt.Value > startedAt.AddSeconds(WoundTreatmentStation.DurationSeconds))
                || (checkedMedicine ? endedAt != startedAt.AddSeconds(WoundTreatmentStation.DurationSeconds)
                    || first < 1 || first > 20 || second < 0 || second > 20 || natural != (second == 0 ? first : Math.Min(first, second))
                    || randomBefore == 0 || randomAfter == 0 || wordsConsumed < (second == 0 ? 1 : 2)
                    : first != 0 || second != 0 || natural != 0 || modifier != 0
                        || randomBefore != 0 || randomAfter != 0 || wordsConsumed != 0))
                throw new ArgumentException("Invalid ordinary Wound treatment history.");
            Basket = basket;
            StartCommandId = startCommandId;
            StartRevision = startRevision;
            StartedAt = startedAt;
            LinkedInjury = linkedInjury;
            Outcome = outcome;
            EndCommandId = endCommandId;
            EndRevision = endRevision;
            EndedAt = endedAt;
            First = first;
            Second = second;
            Natural = natural;
            Modifier = modifier;
            RandomBefore = randomBefore;
            RandomAfter = randomAfter;
            WordsConsumed = wordsConsumed;
        }
    }

    /// <summary>The approved TEST_ONLY station and finite, sealed initial stocks.</summary>
    public static class WoundTreatmentStation
    {
        public const string FingerprintPrefix = "TEST_ONLY.wound-treatment-v1-";
        public const byte Marker = 6;
        public const string Prefix = "TEST_ONLY.wound-treatment.";
        public const string KitLot = Prefix + "kit";
        public const string Location = Prefix + "station";
        public const string Healer = ConnectedVialRules.CarrierId;
        public const string Patient = ConnectedVialRules.CompanionRecipientId;
        public const int BasketCount = 2;
        public const int DurationSeconds = 28800;
        public const int Difficulty = 12;
        public static readonly RuleTime PackedAt = new RuleTime(0);
        public static readonly RuleTime ExpiresAt = PackedAt.AddSeconds(30 * 86400);
        public static readonly ResourceLot Kit = new ResourceLot(KitLot, "medical-kit", 1, Location, Healer);

        public static IReadOnlyList<WoundTreatmentVessel> Vessels(int basket)
        {
            string id = BasketId(basket);
            return Array.AsReadOnly(new[] {
                new WoundTreatmentVessel(id + ".skin-a", id + ".water-a", 4, new RuleQuantity(1), new RuleQuantity(1)),
                new WoundTreatmentVessel(id + ".skin-b", id + ".water-b", 4, new RuleQuantity(1), new RuleQuantity(1)),
                new WoundTreatmentVessel(id + ".flask", id + ".oil", 1, new RuleQuantity(1, 4), new RuleQuantity(3, 4))
            });
        }

        public static IEnumerable<ResourceLot> Stock(int basket)
        {
            string id = BasketId(basket);
            var vessels = Vessels(basket);
            yield return new ResourceLot(id + ".food", "dry-ration-pounds", 2, Location, Healer);
            yield return new ResourceLot(vessels[0].LotId, "clean-water-pints", 4, vessels[0].Id, Healer);
            yield return new ResourceLot(vessels[1].LotId, "clean-water-pints", 4, vessels[1].Id, Healer);
            yield return new ResourceLot(vessels[2].LotId, "lamp-oil-pints", 1, vessels[2].Id, Healer);
            yield return new ResourceLot(id + ".sundries", "sundries-pounds", new RuleQuantity(1, 4), Location, Healer);
        }

        public static InventoryLotRecord Provenance(ResourceLot lot)
            => new InventoryLotRecord(lot.Id, "", Healer, lot.Amount, PackedAt, NutritionKind.None,
                lot.UnitId == "dry-ration-pounds" ? ExpiresAt : (RuleTime?)null, InventoryAccess.Ground);

        public static bool IsStationId(string id) => id != null && id.StartsWith(Prefix, StringComparison.Ordinal);

        private static string BasketId(int basket) => Prefix + basket.ToString(CultureInfo.InvariantCulture);
        public static string ClaimId(string job, int index) => job + ".claim-" + index.ToString(CultureInfo.InvariantCulture);
        public static string IntervalId(string job, string actor) => job + (actor == Healer ? ".healer" : ".patient");
        public static bool PatientOccupancy(Snapshot state, WorkerInterval interval)
            => state.ConnectedWoundTreatment && interval.WorkerId == Patient && interval.Id == IntervalId(interval.JobId, Patient)
                && interval.JobId.StartsWith(Prefix, StringComparison.Ordinal);

        public static bool SelectedFingerprint(string fingerprint) => fingerprint.StartsWith(FingerprintPrefix, StringComparison.Ordinal) || ConsumeDecaySite.SelectedFingerprint(fingerprint);
        public static WoundTreatmentRecord Active(Snapshot state)
            => state.ConnectedWoundTreatment ? state.WoundTreatments.SingleOrDefault(x => x.Outcome == WoundTreatmentOutcome.Active) : null;

        public static bool IsCommand(CommandKind kind)
            => kind == CommandKind.StartWoundTreatment || kind == CommandKind.InterruptWoundTreatment;

        internal static void Validate(Snapshot state)
        {
            var jobs = state.WoundTreatments;
            var gains = state.ExpeditionStrainGains.Where(x => x.CauseKind == ExpeditionStrainCauseKind.WoundTreatmentCriticalFailure).ToArray();
            if (jobs == null || jobs.Length > BasketCount || jobs.Any(x => x == null)
                || state.ConnectedWoundTreatment != SelectedFingerprint(state.ContentFingerprint)
                || !state.ConnectedWoundTreatment && (jobs.Length != 0 || gains.Length != 0
                    || state.Work?.Lots.Any(x => IsStationId(x.Id)) == true))
                throw new ArgumentException("Invalid Wound treatment envelope.");
            if (!state.ConnectedWoundTreatment) return;
            if (!state.TestOnly || !state.ConnectedCompanionStabilization || state.SchemaVersion != Snapshot.SurpriseEntrySchema)
                throw new ArgumentException("Wound treatment requires the selected stabilization history.");

            ValidateLot(state, Kit, Kit.Amount);
            long previous = 0;
            for (int basket = 0; basket < BasketCount; basket++) {
                var job = basket < jobs.Length ? jobs[basket] : null;
                var stock = Stock(basket).ToArray();
                foreach (var lot in stock) ValidateLot(state, lot, job == null ? lot.Amount : default);
                if (job == null) continue;
                bool active = job.Outcome == WoundTreatmentOutcome.Active;
                var priorExit = state.ClosedEncounters.FirstOrDefault(x => x.Encounter.Id == state.Reinforcement?.Definition.EncounterId);
                if (priorExit == null || priorExit.ClosedRevision >= job.StartRevision || priorExit.ClosedAt > job.StartedAt
                    || job.Basket != basket || job.StartRevision <= previous || job.StartRevision > state.Revision
                    || job.StartedAt >= ExpiresAt || job.StartedAt > state.RuleClock
                    || active && (basket != jobs.Length - 1 || job.DueAt <= state.RuleClock)
                    || job.EndRevision > state.Revision || job.EndedAt > state.RuleClock)
                    throw new ArgumentException("Invalid Wound treatment chronology.");
                previous = job.EndRevision;
                var start = new Command(job.StartCommandId, Healer, job.StartRevision - 1, CommandKind.StartWoundTreatment, Patient);
                if (!state.Receipts.Any(x => x.Revision == job.StartRevision && x.Principal == "TEST_ONLY.host" && start.MatchesReceipt(x)))
                    throw new ArgumentException("Wound treatment start requires its exact command receipt.");
                if (!active) ValidateEndReceipt(state, job);
                var expected = new[] { Kit }.Concat(stock).ToArray();
                var claims = state.Work.Reservations.Where(x => x.JobId == job.Id).ToDictionary(x => x.Id, StringComparer.Ordinal);
                if (claims.Count != expected.Length) throw new ArgumentException("Wound treatment requires its exact claims.");
                for (int index = 0; index < expected.Length; index++) {
                    var lot = expected[index];
                    var status = index == 0 ? (active ? ReservationStatus.Reserved : ReservationStatus.Released) : ReservationStatus.Consumed;
                    if (!claims.TryGetValue(ClaimId(job.Id, index), out var claim) || claim.LotId != lot.Id
                        || claim.Amount != lot.Amount || claim.Status != status)
                        throw new ArgumentException("Invalid Wound treatment stock settlement.");
                }
                RuleTime end = job.EndedAt ?? job.DueAt;
                var intervals = state.Work.WorkerIntervals.Where(x => x.JobId == job.Id).ToArray();
                if (end == job.StartedAt ? intervals.Length != 0 : intervals.Length != 2
                    || new[] { Healer, Patient }.Any(actor => !intervals.Any(x => x.Id == IntervalId(job.Id, actor)
                        && x.WorkerId == actor && x.Start == job.StartedAt && x.End == end)))
                    throw new ArgumentException("Invalid Wound treatment occupancy.");
            }
            if (state.Receipts.Count(x => x.Fingerprint.StartsWith(((int)CommandKind.StartWoundTreatment)
                    .ToString(CultureInfo.InvariantCulture) + "|", StringComparison.Ordinal)) != jobs.Length)
                throw new ArgumentException("Missing Wound treatment start evidence.");
            if (state.Work.Reservations.Any(x => (x.LotId.StartsWith(Prefix, StringComparison.Ordinal)
                    || x.JobId.StartsWith(Prefix, StringComparison.Ordinal)) && !jobs.Any(j => j.Id == x.JobId))
                || state.Work.WorkerIntervals.Any(x => x.JobId.StartsWith(Prefix, StringComparison.Ordinal) && !jobs.Any(j => j.Id == x.JobId)))
                throw new ArgumentException("Unknown Wound treatment ledger claim.");
            var criticalFailures = jobs.Where(x => x.Outcome == WoundTreatmentOutcome.CriticalFailure).ToArray();
            if (gains.Length != criticalFailures.Length) throw new ArgumentException("Missing Wound treatment Strain evidence.");
            for (int index = 0; index < criticalFailures.Length; index++) {
                var job = criticalFailures[index];
                string id = job.Id + ".gain";
                if (!gains.Any(x => x.CauseId == job.Id && x.ActorId == Patient && x.At == job.EndedAt
                    && x.Revision == job.EndRevision && x.Id == id && x.PointId == id + ".point"
                    && x.SourceId == Prefix + "medicine" && x.LevelBefore == index && x.GainSequence == 0
                    && x.AttemptedAmount == 1 && x.AddedAmount == 1 && x.Endpoint == ExpeditionStrainEndpoint.None
                    && !x.OrdinaryRemovable.HasValue && !x.RemovalGateMet.HasValue))
                    throw new ArgumentException("Invalid Wound treatment Strain evidence.");
            }
        }

        private static void ValidateLot(Snapshot state, ResourceLot expected, RuleQuantity amount)
        {
            var actual = state.Work.Lots.SingleOrDefault(x => x.Id == expected.Id);
            var provenance = state.InventoryLots.SingleOrDefault(x => x.LotId == expected.Id);
            var origin = Provenance(expected);
            if (actual == null || actual.LocationId != expected.LocationId || actual.CustodianId != Healer
                || actual.UnitId != expected.UnitId || actual.Amount != amount
                || provenance == null || provenance.ParentId != "" || provenance.OwnerId != Healer
                || provenance.CreatedAmount != expected.Amount || provenance.CreatedAt != origin.CreatedAt
                || provenance.Nutrition != NutritionKind.None || provenance.FreshUntil != origin.FreshUntil
                || provenance.Access != InventoryAccess.Ground || state.InventoryLots.Any(x => x.ParentId == expected.Id)
                || state.Intakes.Any(x => x.LotId == expected.Id))
                throw new ArgumentException("Invalid fixed Wound treatment stock.");
        }

        private static void ValidateEndReceipt(Snapshot state, WoundTreatmentRecord job)
        {
            var receipt = state.Receipts.SingleOrDefault(x => x.Revision == job.EndRevision);
            if (receipt == null || receipt.Id != job.EndCommandId) throw new ArgumentException("Missing Wound treatment end receipt.");
            if (job.Outcome == WoundTreatmentOutcome.Interrupted && receipt.Principal == "TEST_ONLY.host") {
                var command = new Command(job.EndCommandId, Healer, job.EndRevision - 1, CommandKind.InterruptWoundTreatment, Patient);
                if (command.MatchesReceipt(receipt)) return;
            }
            var clock = CommandHistory.Read(receipt);
            if (receipt.Principal != "TEST_ONLY.session-operator" || clock.Kind != CommandKind.AdvanceClock
                || clock.Actor != Healer || clock.Target != "" || clock.X < 1 || clock.Y < 1)
                throw new ArgumentException("Wound treatment end requires the authorized elapsed clock or interrupt.");
        }
    }
}
