using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ExpeditionStrainEndpoint { None, OrdinaryDeath }

    /// <summary>Actual consumption attribution for one recipient's closed provisioning day.
    /// It references physical inventory and consumption reservations; it creates no stock.</summary>
    public sealed class DailyProvisioningConsumptionRecord
    {
        public string SettlementId { get; }
        public string IntakeId { get; }
        public string ActorId { get; }
        public string LotId { get; }
        public string ReservationId { get; }
        public NutritionKind Nutrition { get; }
        public RuleQuantity Amount { get; }

        public DailyProvisioningConsumptionRecord(string settlementId, string intakeId, string actorId,
            string lotId, string reservationId, NutritionKind nutrition, RuleQuantity amount)
        {
            if (!Validation.ValidId(settlementId) || !Validation.ValidId(intakeId) || !Validation.ValidId(actorId)
                || !Validation.ValidId(lotId) || !Validation.ValidId(reservationId)
                || nutrition != NutritionKind.FoodPounds && nutrition != NutritionKind.WaterPints
                || amount <= default(RuleQuantity))
                throw new ArgumentException("Invalid daily provisioning consumption evidence.");
            SettlementId = settlementId; IntakeId = intakeId; ActorId = actorId; LotId = lotId;
            ReservationId = reservationId; Nutrition = nutrition; Amount = amount;
        }
    }

    /// <summary>Once-only accounting for one fixed recipient and half-open canonical day.
    /// Food and water shortages are retained separately but resolve to one Strain gain.</summary>
    public sealed class DailyProvisioningSettlementRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public long DayOrdinal { get; }
        public RuleTime Start { get; }
        public RuleTime End { get; }
        public RuleQuantity FoodRequired { get; }
        public RuleQuantity WaterRequired { get; }
        public RuleQuantity FoodConsumed { get; }
        public RuleQuantity WaterConsumed { get; }
        public bool RecipientLivingBeforeGain { get; }
        public string StrainGainId { get; }
        public long Revision { get; }

        public DailyProvisioningSettlementRecord(string id, string actorId, long dayOrdinal, RuleTime start,
            RuleTime end, RuleQuantity foodRequired, RuleQuantity waterRequired, RuleQuantity foodConsumed,
            RuleQuantity waterConsumed, bool recipientLivingBeforeGain, string strainGainId, long revision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || dayOrdinal < 0 || end <= start
                || foodRequired <= default(RuleQuantity) || waterRequired <= default(RuleQuantity)
                || foodConsumed < default(RuleQuantity) || waterConsumed < default(RuleQuantity)
                || strainGainId == null || (strainGainId != "" && !Validation.ValidId(strainGainId)) || revision < 1)
                throw new ArgumentException("Invalid daily provisioning settlement.");
            Id = id; ActorId = actorId; DayOrdinal = dayOrdinal; Start = start; End = end;
            FoodRequired = foodRequired; WaterRequired = waterRequired; FoodConsumed = foodConsumed;
            WaterConsumed = waterConsumed; RecipientLivingBeforeGain = recipientLivingBeforeGain;
            StrainGainId = strainGainId; Revision = revision;
        }
        public bool FoodShortfall => FoodConsumed < FoodRequired;
        public bool WaterShortfall => WaterConsumed < WaterRequired;
        public bool HasShortfall => FoodShortfall || WaterShortfall;
    }

    /// <summary>Immutable source-qualified point/gain history. A null removability flag means the
    /// source-bound recovery procedure has not yet classified it; it does not make the point inactive.</summary>
    public sealed class ExpeditionStrainGainRecord
    {
        public string Id { get; }
        public string PointId { get; }
        public string SettlementId { get; }
        public string ActorId { get; }
        public string SourceId { get; }
        public string TrackId { get; }
        public RuleTime At { get; }
        public long Revision { get; }
        public int LevelBefore { get; }
        public int AttemptedAmount { get; }
        public int AddedAmount { get; }
        public bool? OrdinaryRemovable { get; }
        public bool? RemovalGateMet { get; }
        public ExpeditionStrainEndpoint Endpoint { get; }
        public int LevelAfter => checked(LevelBefore + AddedAmount);

        public ExpeditionStrainGainRecord(string id, string pointId, string settlementId, string actorId,
            string sourceId, string trackId, RuleTime at, long revision, int levelBefore, int attemptedAmount,
            int addedAmount, bool? ordinaryRemovable, bool? removalGateMet, ExpeditionStrainEndpoint endpoint)
        {
            if (!Validation.ValidId(id) || (pointId != "" && !Validation.ValidId(pointId))
                || !Validation.ValidId(settlementId) || !Validation.ValidId(actorId)
                || !Validation.ValidId(sourceId) || trackId != "expedition.strain"
                || revision < 1 || levelBefore < 0 || levelBefore > 6 || attemptedAmount < 1 || attemptedAmount > 6
                || addedAmount < 0 || addedAmount > 6 || levelBefore + addedAmount > 6
                || (addedAmount > 0) != (pointId != "")
                || !Enum.IsDefined(typeof(ExpeditionStrainEndpoint), endpoint))
                throw new ArgumentException("Invalid Expedition Strain gain history.");
            Id = id; PointId = pointId; SettlementId = settlementId; ActorId = actorId; SourceId = sourceId;
            TrackId = trackId; At = at; Revision = revision; LevelBefore = levelBefore;
            AttemptedAmount = attemptedAmount; AddedAmount = addedAmount;
            OrdinaryRemovable = ordinaryRemovable; RemovalGateMet = removalGateMet; Endpoint = endpoint;
        }
    }

    /// <summary>Current source-anchored Dash restriction. Deadline is absolute so entering or leaving
    /// initiative cannot convert, restart, or rephase an already-recorded lock.</summary>
    public sealed class ExpeditionDashLockRecord
    {
        public string ActorId { get; }
        public long AppliedRevision { get; }
        public RuleTime AppliedAt { get; }
        public RuleTime Deadline { get; }
        public string EncounterId { get; }
        public RuleTime MarkerPhase { get; }
        public bool InitiativeAnchored => EncounterId != "";

        public ExpeditionDashLockRecord(string actorId, long appliedRevision, RuleTime appliedAt,
            RuleTime deadline, string encounterId = "", RuleTime markerPhase = default)
        {
            if (!Validation.ValidId(actorId) || appliedRevision < 1 || deadline <= appliedAt
                || encounterId == null || (encounterId != "" && !Validation.ValidId(encounterId)))
                throw new ArgumentException("Invalid Expedition Strain Dash lock.");
            if (encounterId == "" && markerPhase != default)
                throw new ArgumentException("Out-of-initiative Dash locks have no marker phase.");
            ActorId = actorId; AppliedRevision = appliedRevision; AppliedAt = appliedAt;
            Deadline = deadline; EncounterId = encounterId; MarkerPhase = markerPhase;
        }
    }

    public static class ExpeditionProvisioningValidation
    {
        public const int MaxSettlements = 8192;
        public const int MaxConsumptionEvidence = 65536;
        public const int MaxStrainGains = 8192;
        public const int MaxDashLocks = 64;

        public static void Validate(Snapshot s)
        {
            if (s.DailyProvisioningSettlements == null || s.DailyProvisioningConsumption == null
                || s.ExpeditionStrainGains == null || s.ExpeditionDashLocks == null
                || s.DailyProvisioningSettlements.Length > MaxSettlements
                || s.DailyProvisioningConsumption.Length > MaxConsumptionEvidence
                || s.ExpeditionStrainGains.Length > MaxStrainGains
                || s.ExpeditionDashLocks.Length > MaxDashLocks
                || s.DailyProvisioningSettlements.Any(x => x == null)
                || s.DailyProvisioningConsumption.Any(x => x == null)
                || s.ExpeditionStrainGains.Any(x => x == null)
                || s.ExpeditionDashLocks.Any(x => x == null))
                throw new ArgumentException("Invalid Expedition provisioning or Strain collections.");

            if (s.SchemaVersion < Snapshot.DailyProvisioningSchema)
            {
                if (s.DailyProvisioningSettlements.Length != 0 || s.DailyProvisioningConsumption.Length != 0
                    || s.ExpeditionStrainGains.Length != 0 || s.ExpeditionDashLocks.Length != 0)
                    throw new ArgumentException("Daily provisioning state requires schema62.");
                return;
            }
            if (!s.TestOnly) throw new ArgumentException("Expedition provisioning is TEST_ONLY.");

            bool Actor(string id) => s.Actors.Any(x => x.Id == id);
            bool Settlement(string id) => s.DailyProvisioningSettlements.Any(x => x.Id == id);
            if (s.DailyProvisioningSettlements.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.DailyProvisioningSettlements.Length
                || s.DailyProvisioningSettlements.Select(x => x.ActorId + "|" + x.DayOrdinal.ToString(System.Globalization.CultureInfo.InvariantCulture))
                    .Distinct(StringComparer.Ordinal).Count() != s.DailyProvisioningSettlements.Length
                || s.DailyProvisioningSettlements.Any(x => !Actor(x.ActorId) || x.Revision > s.Revision || x.End > s.RuleClock))
                throw new ArgumentException("Invalid daily provisioning settlement identity or time.");

            if (s.DailyProvisioningConsumption.Any(x => !Settlement(x.SettlementId)
                || !Actor(x.ActorId) || !s.Intakes.Any(i => i.Id == x.IntakeId && i.ActorId == x.ActorId
                    && i.LotId == x.LotId && i.ReservationId == x.ReservationId)
                || !s.InventoryLots.Any(l => l.LotId == x.LotId && l.Nutrition == x.Nutrition))
                || s.DailyProvisioningConsumption.GroupBy(x => x.SettlementId + "|" + x.IntakeId, StringComparer.Ordinal)
                    .Any(g => g.Count() > 1))
                throw new ArgumentException("Invalid daily consumption evidence references.");

            foreach (var settlement in s.DailyProvisioningSettlements)
            {
                var evidence = s.DailyProvisioningConsumption.Where(x => x.SettlementId == settlement.Id).ToArray();
                if (RuleQuantity.Sum(evidence.Where(x => x.Nutrition == NutritionKind.FoodPounds).Select(x => x.Amount))
                        != settlement.FoodConsumed
                    || RuleQuantity.Sum(evidence.Where(x => x.Nutrition == NutritionKind.WaterPints).Select(x => x.Amount))
                        != settlement.WaterConsumed
                    || settlement.HasShortfall != (settlement.StrainGainId != ""))
                    throw new ArgumentException("Daily settlement does not match its evidence or point outcome.");
                if (settlement.StrainGainId != "")
                {
                    var gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.Id == settlement.StrainGainId);
                    if (gain == null || gain.SettlementId != settlement.Id || gain.ActorId != settlement.ActorId
                        || gain.At != settlement.End || gain.Revision != settlement.Revision)
                        throw new ArgumentException("Daily settlement has no matching Strain gain.");
                }
            }

            if (s.ExpeditionStrainGains.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionStrainGains.Length
                || s.ExpeditionStrainGains.Select(x => x.PointId).Where(x => x != "").Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainGains.Count(x => x.PointId != "")
                || s.ExpeditionStrainGains.Any(x => !Actor(x.ActorId) || x.Revision > s.Revision || x.At > s.RuleClock
                    || !Settlement(x.SettlementId) || x.AddedAmount == 0 && (x.LevelBefore < 6 || x.Endpoint != ExpeditionStrainEndpoint.OrdinaryDeath)
                    || x.AddedAmount > 0 && x.LevelAfter == 6 && x.Endpoint != ExpeditionStrainEndpoint.OrdinaryDeath
                    || x.LevelAfter < 6 && x.Endpoint != ExpeditionStrainEndpoint.None))
                throw new ArgumentException("Invalid source-qualified Expedition Strain history.");
            foreach (var group in s.ExpeditionStrainGains.GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                var ordered = group.OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
                int level = 0;
                foreach (var gain in ordered)
                {
                    if (gain.LevelBefore != level || gain.AttemptedAmount != 1
                        || gain.AddedAmount != Math.Min(1, 6 - level))
                        throw new ArgumentException("Expedition Strain point history is not cumulative.");
                    level = gain.LevelAfter;
                }
            }

            if (s.ExpeditionDashLocks.Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionDashLocks.Length
                || s.ExpeditionDashLocks.Any(x => !Actor(x.ActorId) || x.AppliedRevision > s.Revision
                    || x.AppliedAt > s.RuleClock || x.Deadline <= x.AppliedAt))
                throw new ArgumentException("Invalid current Expedition Dash lock.");
        }
    }
}
