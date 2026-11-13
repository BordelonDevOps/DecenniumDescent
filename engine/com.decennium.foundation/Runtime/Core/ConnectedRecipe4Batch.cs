using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ConnectedSpecimenDisposition { Uncharged, Charged, Returned, Consumed }

    /// <summary>The selected physical charging and settlement of one existing specimen.</summary>
    public sealed class ConnectedRecipe4Batch
    {
        public const string FingerprintPrefix = "TEST_ONLY.recipe4-batch-v1-";
        public const string RecipeId = "recipe-4";
        public const string Apparatus = "TEST_ONLY.recipe4.bench-apparatus.v1";
        public const string ApparatusProfile = "TEST_ONLY.recipe4.closed-processing.v1";
        public const string Fit = "TEST_ONLY.recipe4.one-batch-fit.v1";
        public const int BenchX = 3;
        public const int BenchY = 3;

        public string ApparatusId { get; }
        public string FitId { get; }
        public string ReturnVesselId { get; }
        public string OrderId { get; }
        public long ChargeRevision { get; }
        public long SettlementRevision { get; }
        public ConnectedSpecimenDisposition Disposition { get; }

        public ConnectedRecipe4Batch(string apparatusId, string fitId, string returnVesselId, string orderId,
            long chargeRevision, long settlementRevision, ConnectedSpecimenDisposition disposition)
        {
            if (apparatusId != Apparatus || fitId != Fit || returnVesselId != ConnectedBloodSpecimen.Vessel
                || !Enum.IsDefined(typeof(ConnectedSpecimenDisposition), disposition)
                || (disposition == ConnectedSpecimenDisposition.Uncharged
                    ? orderId != "" || chargeRevision != 0 || settlementRevision != 0
                    : chargeRevision < 1 || orderId != "manufacture.order." + chargeRevision.ToString(CultureInfo.InvariantCulture)
                        || (disposition == ConnectedSpecimenDisposition.Charged
                            ? settlementRevision != 0 : settlementRevision <= chargeRevision)))
                throw new ArgumentException("Invalid connected recipe-4 apparatus lifecycle.");
            ApparatusId = apparatusId;
            FitId = fitId;
            ReturnVesselId = returnVesselId;
            OrderId = orderId;
            ChargeRevision = chargeRevision;
            SettlementRevision = settlementRevision;
            Disposition = disposition;
        }

        public static ConnectedRecipe4Batch Selected()
            => new ConnectedRecipe4Batch(Apparatus, Fit, ConnectedBloodSpecimen.Vessel, "", 0, 0,
                ConnectedSpecimenDisposition.Uncharged);

        public ConnectedRecipe4Batch Charge(string orderId, long revision)
            => new ConnectedRecipe4Batch(ApparatusId, FitId, ReturnVesselId, orderId, revision, 0,
                ConnectedSpecimenDisposition.Charged);

        public ConnectedRecipe4Batch Settle(long revision, bool returned)
            => new ConnectedRecipe4Batch(ApparatusId, FitId, ReturnVesselId, OrderId, ChargeRevision, revision,
                returned ? ConnectedSpecimenDisposition.Returned : ConnectedSpecimenDisposition.Consumed);

        public bool UsesApparatus => Disposition == ConnectedSpecimenDisposition.Charged
            || Disposition == ConnectedSpecimenDisposition.Consumed;

        public static bool IsSelected(Snapshot s)
            => s.ContentFingerprint.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
                || s.ContentFingerprint.StartsWith(ConnectedVialRules.FingerprintPrefix, StringComparison.Ordinal)
                || s.ContentFingerprint.StartsWith(ConnectedVialRules.StowFingerprintPrefix, StringComparison.Ordinal)
                || s.ContentFingerprint.StartsWith(ConnectedVialRules.TacticalFingerprintPrefix, StringComparison.Ordinal)
                || s.ContentFingerprint.StartsWith(ConnectedVialRules.CompanionFingerprintPrefix, StringComparison.Ordinal)
                || s.ContentFingerprint.StartsWith(ConnectedVialRules.StabilizationFingerprintPrefix, StringComparison.Ordinal)
                || WoundTreatmentStation.SelectedFingerprint(s.ContentFingerprint);

        public static bool OnBench(PortableEquipmentRecord item)
            => item.Placement == PortablePlacement.Ground && item.GroundX == BenchX && item.GroundY == BenchY;

        internal static void Validate(Snapshot s)
        {
            var batch = s.ConnectedBatch;
            if ((batch != null) != IsSelected(s))
                throw new ArgumentException("Wire95 requires its exact connected batch composition.");
            if (batch == null) return;
            if (s.BloodSpecimen == null || s.SchemaVersion != Snapshot.SurpriseEntrySchema || !s.TestOnly
                || s.ExplorationSearch == null || s.ExplorationHide == null)
                throw new ArgumentException("Wire95 requires the selected specimen and both observation sections.");

            var apparatus = s.PortableEquipment.SingleOrDefault(x => x.Id == batch.ApparatusId);
            if (apparatus == null || apparatus.ProfileId != ApparatusProfile || !OnBench(apparatus)
                || apparatus.OwnerId != ConnectedBloodSpecimen.Worker || apparatus.CustodianId != apparatus.OwnerId
                || apparatus.LinkKind != PortableLinkKind.None || apparatus.MassBasis != PortableMassBasis.Unmodeled
                || apparatus.Open || apparatus.CapacityPounds.HasValue || apparatus.FitRuleId != batch.FitId
                || apparatus.FitMemberIds.Count != 1 || apparatus.FitMemberIds[0] != s.BloodSpecimen.LotId
                || s.PortableHandling.Any(x => x.ItemId == apparatus.Id))
                throw new ArgumentException("Invalid selected closed workshop apparatus.");

            if (batch.Disposition == ConnectedSpecimenDisposition.Uncharged) {
                if (s.ManufacturingOrders.Length != 0 || s.AlchemyDoses.Length != 0)
                    throw new ArgumentException("An uncharged specimen cannot have a batch or output.");
                return;
            }

            var order = s.ManufacturingOrders.Length == 1 ? s.ManufacturingOrders[0] : null;
            bool charged = batch.Disposition == ConnectedSpecimenDisposition.Charged;
            bool returned = batch.Disposition == ConnectedSpecimenDisposition.Returned;
            if (order == null || order.Id != batch.OrderId || order.RecipeId != RecipeId
                || order.WorkerId != ConnectedBloodSpecimen.Worker || order.MaterialSet != 0 || order.ExtraVials > 2
                || order.TakeTen || order.Open != charged || order.Work.Phases.Count != 2
                || order.Work.Phases[0] != new RuleTime(900) || order.Work.Phases[1] != new RuleTime(13500)
                || order.StabilizedAt.HasValue != (order.Work.CompletedPhases > 0)
                || !s.HarvestPreservationTreatmentAttempts.Any(x => x.Status == HarvestPreservationTreatmentStatus.Success)
                || HarvestPreservationRules.IsProtectedAtRevision(s, s.BloodSpecimen.LotId, order.StartedAt, batch.ChargeRevision - 1))
                throw new ArgumentException("Invalid connected recipe-4 order and stabilization history.");
            bool checkedQuality = order.Status == ManufacturingStatus.Complete || order.Status == ManufacturingStatus.AwaitingChoice;
            if (checkedQuality && (order.First < 1 || order.Natural !=
                    (order.Second == 0 ? order.First : Math.Min(order.First, order.Second)))
                || !checkedQuality && (order.First != 0 || order.Second != 0 || order.Natural != 0))
                throw new ArgumentException("Connected recipe-4 quality does not match its recorded dice.");
            ValidateLabor(s, order);

            var declaration = s.Receipts.SingleOrDefault(x => x.Revision == batch.ChargeRevision);
            if (declaration == null || !s.HarvestPreservationEvidence.Any(x => x.AppliedRevision < batch.ChargeRevision))
                throw new ArgumentException("The charged specimen lacks its actual workshop declaration.");
            var command = CommandHistory.Read(declaration);
            if (command.Kind != CommandKind.StartManufacturing || command.Actor != order.WorkerId
                || command.Target != RecipeId || command.X != 0 || command.Y != order.ExtraVials)
                throw new ArgumentException("The charged specimen declaration does not match its order.");

            if (charged) {
                var vessel = s.PortableEquipment.Single(x => x.Id == batch.ReturnVesselId);
                if (!vessel.Open || !OnBench(vessel) || s.InventoryCombat || s.AlchemyDoses.Length != 0)
                    throw new ArgumentException("The charged order requires its fixed open return vessel.");
            } else if (!s.Receipts.Any(x => x.Revision == batch.SettlementRevision)
                || returned != (order.Status == ManufacturingStatus.Cancelled && order.Work.Labor == default
                    || order.Status == ManufacturingStatus.Complete && order.Quality == CraftQuality.Masterwork && order.RetainedCatalyst == 3)) {
                throw new ArgumentException("The specimen's physical settlement does not match the terminal outcome.");
            }

            var claim = s.Work.Reservations.SingleOrDefault(x => x.JobId == order.Id && x.Id == order.Id + ".component3");
            var whole = new RuleQuantity(1);
            if (claim == null || claim.LotId != s.BloodSpecimen.LotId || claim.Amount != whole
                || claim.RemainingAmount != (charged ? whole : default)
                || claim.ReleasedAmount != (returned ? whole : default)
                || claim.ConsumedAmount != (!charged && !returned ? whole : default))
                throw new ArgumentException("Connected batch specimen claim does not conserve the selected whole lot.");

            var tool = s.Structures.SingleOrDefault(x => x.Id == s.BloodSpecimen.ToolId);
            if (s.AlchemyDoses.Any(x => order.Status != ManufacturingStatus.Complete || x.OrderId != order.Id
                || x.RecipeId != RecipeId || x.MakerId != order.WorkerId || x.OwnerId != order.WorkerId
                || x.CreatedAt != order.UpdatedAt || x.Id != ConnectedVialRules.SelectedId(s)
                    && (x.CustodianId != order.WorkerId || x.LocationId != tool?.LocationId)))
                throw new ArgumentException("Connected batch output lacks its actual settlement and custody.");
        }

        private static void ValidateLabor(Snapshot s, ManufacturingOrderRecord order)
        {
            var bookings = s.Work.WorkerIntervals.Where(x => x.JobId == order.Id).ToArray();
            RuleTime through = order.Open ? s.RuleClock : order.UpdatedAt;
            if (bookings.Any(x => x.WorkerId != order.WorkerId || x.Start < order.StartedAt || x.Start > through
                || !order.Open && x.End > through)
                || bookings.Count(x => x.End > s.RuleClock) != (order.Status == ManufacturingStatus.Working ? 1 : 0))
                throw new ArgumentException("Connected recipe-4 labor lacks its exclusive worker booking.");
            RuleQuantity labor = default;
            RuleTime? stabilization = null;
            foreach (var booking in bookings) {
                RuleTime end = booking.End < through ? booking.End : through;
                labor += Quantity(end) - Quantity(booking.Start);
                RuleTime phase = booking.Start.AddSeconds(order.Work.Phases[0].Numerator);
                if (!stabilization.HasValue && phase <= end
                    && HarvestPreservationRules.TryProjectAt(s, s.BloodSpecimen.LotId, phase, out var age)
                    && age.State != HarvestPreservationState.Spoiled)
                    stabilization = phase;
            }
            if (labor != Quantity(order.Work.Labor) || stabilization != order.StabilizedAt)
                throw new ArgumentException("Connected recipe-4 labor or stabilization disagrees with its actual bookings.");
        }

        private static RuleQuantity Quantity(RuleTime value) => new RuleQuantity(value.Numerator, value.Denominator);
    }
}
