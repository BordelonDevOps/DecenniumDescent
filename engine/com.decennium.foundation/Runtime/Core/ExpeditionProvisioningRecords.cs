using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ExpeditionStrainEndpoint { None, OrdinaryDeath }
    public enum ExpeditionStrainCauseKind { DailyProvisioning, RestDebtDeadline, RestMissedWhileIndebted, WoundTreatmentCriticalFailure }

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
        public ExpeditionStrainCauseKind CauseKind { get; }
        public string CauseId { get; }
        public int GainSequence { get; }
        /// <summary>Schema62 compatibility view. Non-daily causes have no settlement identity.</summary>
        public string SettlementId => CauseKind == ExpeditionStrainCauseKind.DailyProvisioning ? CauseId : "";
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
            : this(id, pointId, ExpeditionStrainCauseKind.DailyProvisioning, settlementId, 0, actorId,
                sourceId, trackId, at, revision, levelBefore, attemptedAmount, addedAmount,
                ordinaryRemovable, removalGateMet, endpoint)
        { }

        public ExpeditionStrainGainRecord(string id, string pointId, ExpeditionStrainCauseKind causeKind,
            string causeId, int gainSequence, string actorId, string sourceId, string trackId, RuleTime at,
            long revision, int levelBefore, int attemptedAmount, int addedAmount, bool? ordinaryRemovable,
            bool? removalGateMet, ExpeditionStrainEndpoint endpoint)
        {
            if (!Validation.ValidId(id) || (pointId != "" && !Validation.ValidId(pointId))
                || !Enum.IsDefined(typeof(ExpeditionStrainCauseKind), causeKind) || !Validation.ValidId(causeId)
                || gainSequence < 0 || !Validation.ValidId(actorId)
                || !Validation.ValidId(sourceId) || trackId != "expedition.strain"
                || revision < 1 || levelBefore < 0 || levelBefore > 6 || attemptedAmount < 1 || attemptedAmount > 6
                || addedAmount < 0 || addedAmount > 6 || levelBefore + addedAmount > 6
                || (addedAmount > 0) != (pointId != "")
                || !Enum.IsDefined(typeof(ExpeditionStrainEndpoint), endpoint))
                throw new ArgumentException("Invalid Expedition Strain gain history.");
            Id = id; PointId = pointId; CauseKind = causeKind; CauseId = causeId; GainSequence = gainSequence;
            ActorId = actorId; SourceId = sourceId;
            TrackId = trackId; At = at; Revision = revision; LevelBefore = levelBefore;
            AttemptedAmount = attemptedAmount; AddedAmount = addedAmount;
            OrdinaryRemovable = ordinaryRemovable; RemovalGateMet = removalGateMet; Endpoint = endpoint;
        }
    }

    public enum RestWatchSlot { Morning, Afternoon, Evening }
    public enum RestIntervalStatus { Active, Completed, Interrupted, Unqualified }
    public enum RestWatchOutcomeKind { Rested, Missed }
    public enum RestDebtEventKind { Opened, UnpaidDeadline, MissedWhileIndebted, Cleared }

    /// <summary>Prospective per-actor schedule change. Absence of a row means the sourced Evening default.</summary>
    public sealed class RestWatchScheduleRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public long DayOrdinal { get; }
        public RestWatchSlot Slot { get; }
        public RuleTime At { get; }
        public long Revision { get; }

        public RestWatchScheduleRecord(string id, string actorId, long dayOrdinal, RestWatchSlot slot,
            RuleTime at, long revision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || dayOrdinal < 0
                || !Enum.IsDefined(typeof(RestWatchSlot), slot) || revision < 1)
                throw new ArgumentException("Invalid Rest Watch schedule change.");
            Id = id; ActorId = actorId; DayOrdinal = dayOrdinal; Slot = slot; At = at; Revision = revision;
        }
    }

    /// <summary>One actual attempt at a continuous eight-hour Rest. Site eligibility is bound by the
    /// TEST_ONLY host profile; worker reservations and shared travel remain the activity authorities.</summary>
    public sealed class RestIntervalRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string SiteId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime ScheduledEnd { get; }
        public RuleTime? EndedAt { get; }
        public RestIntervalStatus Status { get; }
        public long Revision { get; }

        public RestIntervalRecord(string id, string actorId, string siteId, RuleTime startedAt,
            RuleTime scheduledEnd, RuleTime? endedAt, RestIntervalStatus status, long revision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Validation.ValidId(siteId)
                || scheduledEnd != startedAt.AddSeconds(8 * 60 * 60)
                || !Enum.IsDefined(typeof(RestIntervalStatus), status) || revision < 1
                || status == RestIntervalStatus.Active && endedAt.HasValue
                || status != RestIntervalStatus.Active && !endedAt.HasValue
                || endedAt.HasValue && (endedAt.Value < startedAt || endedAt.Value > scheduledEnd)
                || status == RestIntervalStatus.Completed && endedAt.Value != scheduledEnd
                || status == RestIntervalStatus.Interrupted && endedAt.Value >= scheduledEnd)
                throw new ArgumentException("Invalid actual Rest interval.");
            Id = id; ActorId = actorId; SiteId = siteId; StartedAt = startedAt; ScheduledEnd = scheduledEnd;
            EndedAt = endedAt; Status = status; Revision = revision;
        }
    }

    /// <summary>Once-only outcome for one actor's scheduled Watch. A completed Rest interval is
    /// linked only when it spans the entire canonical Rest Watch.</summary>
    public sealed class RestWatchOutcomeRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public long DayOrdinal { get; }
        public RestWatchSlot Slot { get; }
        public RuleTime Start { get; }
        public RuleTime End { get; }
        public RestWatchOutcomeKind Outcome { get; }
        public string RestIntervalId { get; }
        public long Revision { get; }

        public RestWatchOutcomeRecord(string id, string actorId, long dayOrdinal, RestWatchSlot slot,
            RuleTime start, RuleTime end, RestWatchOutcomeKind outcome, string restIntervalId, long revision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || dayOrdinal < 0
                || !Enum.IsDefined(typeof(RestWatchSlot), slot) || end <= start
                || !Enum.IsDefined(typeof(RestWatchOutcomeKind), outcome) || restIntervalId == null
                || (restIntervalId != "" && !Validation.ValidId(restIntervalId))
                || (outcome == RestWatchOutcomeKind.Rested) != (restIntervalId != "") || revision < 1)
                throw new ArgumentException("Invalid Rest Watch outcome.");
            Id = id; ActorId = actorId; DayOrdinal = dayOrdinal; Slot = slot; Start = start; End = end;
            Outcome = outcome; RestIntervalId = restIntervalId; Revision = revision;
        }
    }

    /// <summary>Append-only Rest Debt transition. Current debt is projected from this one history.
    /// Strain gains link to the exact UnpaidDeadline or MissedWhileIndebted event.</summary>
    public sealed class RestDebtEventRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public RestDebtEventKind Kind { get; }
        public RuleTime At { get; }
        public long Revision { get; }
        public int EventSequence { get; }
        public string EpisodeId { get; }
        public string EvidenceId { get; }
        public RuleTime DeadlineBefore { get; }
        public RuleTime DeadlineAfter { get; }
        public string StrainGainId { get; }

        public RestDebtEventRecord(string id, string actorId, RestDebtEventKind kind, RuleTime at,
            long revision, int eventSequence, string episodeId, string evidenceId, RuleTime deadlineBefore,
            RuleTime deadlineAfter, string strainGainId)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId)
                || !Enum.IsDefined(typeof(RestDebtEventKind), kind) || revision < 1
                || eventSequence < 0
                || !Validation.ValidId(episodeId) || !Validation.ValidId(evidenceId)
                || strainGainId == null || (strainGainId != "" && !Validation.ValidId(strainGainId)))
                throw new ArgumentException("Invalid Rest Debt event.");
            if (kind == RestDebtEventKind.Opened && (deadlineBefore != default(RuleTime)
                    || deadlineAfter != at.AddSeconds(16 * 60 * 60) || strainGainId != "")
                || kind == RestDebtEventKind.UnpaidDeadline && (deadlineBefore != at || deadlineAfter != at || strainGainId == "")
                || kind == RestDebtEventKind.MissedWhileIndebted && (deadlineAfter != at.AddSeconds(16 * 60 * 60) || strainGainId == "")
                || kind == RestDebtEventKind.Cleared && (deadlineAfter != default(RuleTime) || strainGainId != ""))
                throw new ArgumentException("Invalid Rest Debt event transition.");
            Id = id; ActorId = actorId; Kind = kind; At = at; Revision = revision; EventSequence = eventSequence;
            EpisodeId = episodeId; EvidenceId = evidenceId; DeadlineBefore = deadlineBefore;
            DeadlineAfter = deadlineAfter; StrainGainId = strainGainId;
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
        public const int MaxRestWatchSchedules = 4096;
        public const int MaxRestIntervals = 4096;
        public const int MaxRestWatchOutcomes = 16384;
        public const int MaxRestDebtEvents = 16384;
        public const int MaxStrainRecoveryGateUpdates = 32768;
        public const int MaxBeneficialRests = 4096;
        public const int MaxStrainRecoveryOffers = 4096;
        public const int MaxStrainRemovals = 8192;
        public const int MaxMoraleRestIntervals = 4096;
        public const int MaxMoraleRestBenefits = 4096;
        public const int MaxHavenCareIntervals = 4096;
        public const int MaxHavenCareAssessments = 4096;

        public static void Validate(Snapshot s)
        {
            if (s.DailyProvisioningSettlements == null || s.DailyProvisioningConsumption == null
                || s.ExpeditionStrainGains == null || s.ExpeditionDashLocks == null
                || s.DailyProvisioningSettlements.Length > MaxSettlements
                || s.DailyProvisioningConsumption.Length > MaxConsumptionEvidence
                || s.ExpeditionStrainGains.Length > MaxStrainGains
                || s.ExpeditionDashLocks.Length > MaxDashLocks
                || s.RestWatchSchedules == null || s.RestWatchSchedules.Length > MaxRestWatchSchedules
                || s.RestIntervals == null || s.RestIntervals.Length > MaxRestIntervals
                || s.RestWatchOutcomes == null || s.RestWatchOutcomes.Length > MaxRestWatchOutcomes
                || s.RestDebtEvents == null || s.RestDebtEvents.Length > MaxRestDebtEvents
                || s.ExpeditionStrainRecoveryGateUpdates == null || s.ExpeditionStrainRecoveryGateUpdates.Length > MaxStrainRecoveryGateUpdates
                || s.ExpeditionBeneficialRests == null || s.ExpeditionBeneficialRests.Length > MaxBeneficialRests
                || s.ExpeditionStrainRecoveryOffers == null || s.ExpeditionStrainRecoveryOffers.Length > MaxStrainRecoveryOffers
                || s.ExpeditionStrainRemovals == null || s.ExpeditionStrainRemovals.Length > MaxStrainRemovals
                || s.ExpeditionMoraleRestIntervals == null || s.ExpeditionMoraleRestIntervals.Length > MaxMoraleRestIntervals
                || s.ExpeditionMoraleRestBenefits == null || s.ExpeditionMoraleRestBenefits.Length > MaxMoraleRestBenefits
                || s.ExpeditionHavenCareIntervals == null || s.ExpeditionHavenCareIntervals.Length > MaxHavenCareIntervals
                || s.ExpeditionHavenCareAssessments == null || s.ExpeditionHavenCareAssessments.Length > MaxHavenCareAssessments
                || s.DailyProvisioningSettlements.Any(x => x == null)
                || s.DailyProvisioningConsumption.Any(x => x == null)
                || s.ExpeditionStrainGains.Any(x => x == null)
                || s.ExpeditionDashLocks.Any(x => x == null)
                || s.RestWatchSchedules.Any(x => x == null) || s.RestIntervals.Any(x => x == null)
                || s.RestWatchOutcomes.Any(x => x == null) || s.RestDebtEvents.Any(x => x == null)
                || s.ExpeditionStrainRecoveryGateUpdates.Any(x => x == null) || s.ExpeditionBeneficialRests.Any(x => x == null)
                || s.ExpeditionStrainRecoveryOffers.Any(x => x == null) || s.ExpeditionStrainRemovals.Any(x => x == null)
                || s.ExpeditionMoraleRestIntervals.Any(x => x == null) || s.ExpeditionMoraleRestBenefits.Any(x => x == null)
                || s.ExpeditionHavenCareIntervals.Any(x => x == null) || s.ExpeditionHavenCareAssessments.Any(x => x == null))
                throw new ArgumentException("Invalid Expedition provisioning or Strain collections.");

            if (s.SchemaVersion < Snapshot.DailyProvisioningSchema)
            {
                if (s.DailyProvisioningSettlements.Length != 0 || s.DailyProvisioningConsumption.Length != 0
                    || s.ExpeditionStrainGains.Length != 0 || s.ExpeditionDashLocks.Length != 0
                    || s.RestWatchSchedules.Length != 0 || s.RestIntervals.Length != 0
                    || s.RestWatchOutcomes.Length != 0 || s.RestDebtEvents.Length != 0
                    || s.ExpeditionStrainRecoveryGateUpdates.Length != 0 || s.ExpeditionBeneficialRests.Length != 0
                    || s.ExpeditionStrainRecoveryOffers.Length != 0 || s.ExpeditionStrainRemovals.Length != 0
                    || s.ExpeditionMoraleRestIntervals.Length != 0 || s.ExpeditionMoraleRestBenefits.Length != 0
                    || s.ExpeditionHavenCareIntervals.Length != 0 || s.ExpeditionHavenCareAssessments.Length != 0)
                    throw new ArgumentException("Daily provisioning state requires schema62.");
                return;
            }
            if (s.SchemaVersion < Snapshot.RestDebtSchema
                && (s.RestWatchSchedules.Length != 0 || s.RestIntervals.Length != 0
                    || s.RestWatchOutcomes.Length != 0 || s.RestDebtEvents.Length != 0
                    || s.ExpeditionStrainGains.Any(x => x.CauseKind != ExpeditionStrainCauseKind.DailyProvisioning || x.GainSequence != 0)))
                throw new ArgumentException("Rest Debt state requires schema63.");
            if (s.SchemaVersion < Snapshot.ExpeditionStrainRecoverySchema
                && (s.ExpeditionStrainRecoveryGateUpdates.Length != 0 || s.ExpeditionBeneficialRests.Length != 0
                    || s.ExpeditionStrainRecoveryOffers.Length != 0 || s.ExpeditionStrainRemovals.Length != 0))
                throw new ArgumentException("Expedition Strain recovery state requires schema64.");
            if (s.SchemaVersion < Snapshot.MoraleRestSchema
                && (s.ExpeditionMoraleRestIntervals.Length != 0 || s.ExpeditionMoraleRestBenefits.Length != 0))
                throw new ArgumentException("Morale Rest state requires schema65.");
            if (s.SchemaVersion < Snapshot.HavenCareSchema
                && (s.ExpeditionHavenCareIntervals.Length != 0 || s.ExpeditionHavenCareAssessments.Length != 0
                    || s.ExpeditionStrainRemovals.Any(x => x.RecoveryKind == ExpeditionRecoveryKind.HavenCare)))
                throw new ArgumentException("Haven-care state requires schema66.");
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
                    if (gain == null || gain.CauseKind != ExpeditionStrainCauseKind.DailyProvisioning
                        || gain.CauseId != settlement.Id || gain.ActorId != settlement.ActorId
                        || gain.At != settlement.End || gain.Revision != settlement.Revision)
                        throw new ArgumentException("Daily settlement has no matching Strain gain.");
                }
            }

            if (s.ExpeditionStrainGains.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionStrainGains.Length
                || s.ExpeditionStrainGains.Select(x => x.PointId).Where(x => x != "").Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainGains.Count(x => x.PointId != "")
                || s.ExpeditionStrainGains.Any(x => !Actor(x.ActorId) || x.Revision > s.Revision || x.At > s.RuleClock
                    || x.CauseKind == ExpeditionStrainCauseKind.DailyProvisioning && !Settlement(x.CauseId)
                    || x.CauseKind != ExpeditionStrainCauseKind.DailyProvisioning && s.SchemaVersion < Snapshot.RestDebtSchema
                    || x.AddedAmount == 0 && (x.LevelBefore < 6 || x.Endpoint != ExpeditionStrainEndpoint.OrdinaryDeath)
                    || x.AddedAmount > 0 && x.LevelAfter == 6 && x.Endpoint != ExpeditionStrainEndpoint.OrdinaryDeath
                    || x.LevelAfter < 6 && x.Endpoint != ExpeditionStrainEndpoint.None))
                throw new ArgumentException("Invalid source-qualified Expedition Strain history.");
            foreach (var group in s.ExpeditionStrainGains.GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                if (s.SchemaVersion >= Snapshot.RestDebtSchema
                    && group.GroupBy(x => x.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + "|"
                        + x.GainSequence.ToString(System.Globalization.CultureInfo.InvariantCulture), StringComparer.Ordinal).Any(x => x.Count() > 1))
                    throw new ArgumentException("Expedition Strain gain sequence is not unique within the command.");
                var ordered = s.SchemaVersion >= Snapshot.RestDebtSchema
                    ? group.OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.GainSequence).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray()
                    : group.OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
                if (s.SchemaVersion < Snapshot.ExpeditionStrainRecoverySchema)
                {
                    int level = 0;
                    foreach (var gain in ordered)
                    {
                        if (gain.LevelBefore != level || gain.AttemptedAmount != 1
                            || gain.AddedAmount != Math.Min(1, 6 - level))
                            throw new ArgumentException("Expedition Strain point history is not cumulative.");
                        level = gain.LevelAfter;
                    }
                }
            }

            if (s.SchemaVersion >= Snapshot.RestDebtSchema)
                ValidateRestDebtReferences(s, Actor);
            if (s.SchemaVersion >= Snapshot.ExpeditionStrainRecoverySchema)
                ValidateRecoveryReferences(s, Actor, Settlement);

            if (s.ExpeditionDashLocks.Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionDashLocks.Length
                || s.ExpeditionDashLocks.Any(x => !Actor(x.ActorId) || x.AppliedRevision > s.Revision
                    || x.AppliedAt > s.RuleClock || x.Deadline <= x.AppliedAt))
                throw new ArgumentException("Invalid current Expedition Dash lock.");
        }

        private static void ValidateRestDebtReferences(Snapshot s, Func<string, bool> actorExists)
        {
            if (s.RestWatchSchedules.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.RestWatchSchedules.Length
                || s.RestWatchSchedules.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision || x.At > s.RuleClock))
                throw new ArgumentException("Invalid Rest Watch schedule history.");
            if (s.RestIntervals.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.RestIntervals.Length
                || s.RestIntervals.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.StartedAt > s.RuleClock || x.EndedAt.HasValue && x.EndedAt.Value > s.RuleClock
                    || x.Status == RestIntervalStatus.Active && x.ScheduledEnd <= s.RuleClock))
                throw new ArgumentException("Invalid actual Rest interval history.");
            if (s.RestWatchOutcomes.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.RestWatchOutcomes.Length
                || s.RestWatchOutcomes.Select(x => x.ActorId + "|" + x.DayOrdinal.ToString(System.Globalization.CultureInfo.InvariantCulture))
                    .Distinct(StringComparer.Ordinal).Count() != s.RestWatchOutcomes.Length
                || s.RestWatchOutcomes.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision || x.End > s.RuleClock
                    || x.RestIntervalId != "" && !s.RestIntervals.Any(r => r.Id == x.RestIntervalId && r.ActorId == x.ActorId
                        && r.Status == RestIntervalStatus.Completed && r.StartedAt == x.Start && r.ScheduledEnd == x.End)))
                throw new ArgumentException("Invalid Rest Watch outcome references.");
            if (s.RestDebtEvents.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.RestDebtEvents.Length
                || s.RestDebtEvents.GroupBy(x => x.ActorId + "|" + x.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture)
                    + "|" + x.EventSequence.ToString(System.Globalization.CultureInfo.InvariantCulture), StringComparer.Ordinal).Any(x => x.Count() > 1)
                || s.RestDebtEvents.Where(x => x.Kind == RestDebtEventKind.Opened)
                    .Select(x => x.ActorId + "|" + x.EpisodeId).Distinct(StringComparer.Ordinal).Count()
                    != s.RestDebtEvents.Count(x => x.Kind == RestDebtEventKind.Opened)
                || s.RestDebtEvents.Where(x => x.Kind == RestDebtEventKind.UnpaidDeadline)
                    .Select(x => x.ActorId + "|" + x.EpisodeId + "|" + x.At.Numerator.ToString(System.Globalization.CultureInfo.InvariantCulture)
                        + "/" + x.At.Denominator.ToString(System.Globalization.CultureInfo.InvariantCulture))
                    .Distinct(StringComparer.Ordinal).Count() != s.RestDebtEvents.Count(x => x.Kind == RestDebtEventKind.UnpaidDeadline)
                || s.RestDebtEvents.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision || x.At > s.RuleClock))
                throw new ArgumentException("Invalid Rest Debt event history.");

            foreach (var group in s.RestDebtEvents.GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                string episode = "";
                RuleTime deadline = default;
                var orderedEvents = group.OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.EventSequence)
                    .ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
                foreach (var debtEvent in orderedEvents)
                {
                    if (debtEvent.Kind == RestDebtEventKind.Opened || debtEvent.Kind == RestDebtEventKind.MissedWhileIndebted)
                    {
                        var outcome = s.RestWatchOutcomes.SingleOrDefault(x => x.Id == debtEvent.EvidenceId);
                        if (outcome == null || outcome.ActorId != debtEvent.ActorId || outcome.Outcome != RestWatchOutcomeKind.Missed
                            || outcome.End != debtEvent.At)
                            throw new ArgumentException("Rest Debt miss has no matching missed Watch outcome.");
                    }
                    if (debtEvent.Kind == RestDebtEventKind.Cleared)
                    {
                        var interval = s.RestIntervals.SingleOrDefault(x => x.Id == debtEvent.EvidenceId);
                        if (interval == null || interval.ActorId != debtEvent.ActorId
                            || interval.Status != RestIntervalStatus.Completed || interval.EndedAt != debtEvent.At)
                            throw new ArgumentException("Rest Debt clearance has no matching completed Rest interval.");
                    }
                    if (debtEvent.Kind == RestDebtEventKind.UnpaidDeadline || debtEvent.Kind == RestDebtEventKind.MissedWhileIndebted)
                    {
                        var gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.Id == debtEvent.StrainGainId);
                        var expectedKind = debtEvent.Kind == RestDebtEventKind.UnpaidDeadline
                            ? ExpeditionStrainCauseKind.RestDebtDeadline : ExpeditionStrainCauseKind.RestMissedWhileIndebted;
                        if (gain == null || gain.CauseKind != expectedKind || gain.CauseId != debtEvent.Id
                            || gain.ActorId != debtEvent.ActorId || gain.At != debtEvent.At || gain.Revision != debtEvent.Revision)
                            throw new ArgumentException("Rest Debt Strain gain is not linked to its exact cause event.");
                    }

                    switch (debtEvent.Kind)
                    {
                        case RestDebtEventKind.Opened:
                            if (episode != "" || debtEvent.DeadlineBefore != default(RuleTime))
                                throw new ArgumentException("Rest Debt opened while an episode was already owed.");
                            episode = debtEvent.EpisodeId; deadline = debtEvent.DeadlineAfter;
                            break;
                        case RestDebtEventKind.UnpaidDeadline:
                            if (episode == "" || debtEvent.EpisodeId != episode || debtEvent.DeadlineBefore != deadline
                                || debtEvent.At != deadline || debtEvent.EvidenceId != episode)
                                throw new ArgumentException("Rest Debt deadline does not match the current episode.");
                            break;
                        case RestDebtEventKind.MissedWhileIndebted:
                            if (episode == "" || debtEvent.EpisodeId != episode || debtEvent.DeadlineBefore != deadline)
                                throw new ArgumentException("Rest Debt miss does not match the current episode.");
                            deadline = debtEvent.DeadlineAfter;
                            break;
                        case RestDebtEventKind.Cleared:
                            if (episode == "" || debtEvent.EpisodeId != episode || debtEvent.DeadlineBefore != deadline)
                                throw new ArgumentException("Rest Debt clearance does not match the current episode.");
                            episode = ""; deadline = default;
                            break;
                    }
                }
            }
            if (s.ExpeditionStrainGains.Any(x => (x.CauseKind == ExpeditionStrainCauseKind.RestDebtDeadline
                || x.CauseKind == ExpeditionStrainCauseKind.RestMissedWhileIndebted) && !s.RestDebtEvents.Any(e => e.Id == x.CauseId && e.StrainGainId == x.Id)))
                throw new ArgumentException("Rest Debt Strain gain has no unique causal event.");
        }

        private static void ValidateRecoveryReferences(Snapshot s, Func<string, bool> actorExists,
            Func<string, bool> settlementExists)
        {
            if (s.SchemaVersion >= Snapshot.MoraleRestSchema)
            {
                ValidateSchema65RecoveryReferences(s, actorExists, settlementExists);
                return;
            }
            if (s.ExpeditionStrainRecoveryGateUpdates.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryGateUpdates.Length
                || s.ExpeditionStrainRecoveryGateUpdates.Select(x => x.PointId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryGateUpdates.Length
                || s.ExpeditionStrainRecoveryGateUpdates.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.At > s.RuleClock || !settlementExists(x.SettlementId)))
                throw new ArgumentException("Invalid Expedition Strain recovery gate history.");

            foreach (var update in s.ExpeditionStrainRecoveryGateUpdates)
            {
                var settlement = s.DailyProvisioningSettlements.Single(x => x.Id == update.SettlementId);
                var gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.PointId == update.PointId);
                if (settlement.ActorId != update.ActorId || settlement.HasShortfall || settlement.End != update.At
                    || settlement.Revision != update.Revision || gain == null || gain.ActorId != update.ActorId
                    || gain.CauseKind != ExpeditionStrainCauseKind.DailyProvisioning || gain.OrdinaryRemovable != true
                    || gain.RemovalGateMet != false || gain.At >= update.At
                    || s.DailyProvisioningSettlements.Single(x => x.Id == gain.CauseId).DayOrdinal >= settlement.DayOrdinal)
                    throw new ArgumentException("Recovery gate update is not proven by a later supported day.");
            }

            if (s.ExpeditionBeneficialRests.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionBeneficialRests.Length
                || s.ExpeditionBeneficialRests.Select(x => x.RestIntervalId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionBeneficialRests.Length
                || s.ExpeditionBeneficialRests.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.CompletedAt > s.RuleClock || x.RecoveryOfferId == null
                    || x.RecoveryOfferId != "" && !Validation.ValidId(x.RecoveryOfferId)))
                throw new ArgumentException("Invalid beneficial Long Rest history.");
            foreach (var group in s.ExpeditionBeneficialRests.GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                var ordered = group.OrderBy(x => x.CompletedAt).ThenBy(x => x.Revision).ToArray();
                for (int i = 0; i < ordered.Length; i++)
                {
                    var benefit = ordered[i];
                    var interval = s.RestIntervals.SingleOrDefault(x => x.Id == benefit.RestIntervalId);
                    if (interval == null || interval.ActorId != benefit.ActorId || interval.Status != RestIntervalStatus.Completed
                        || interval.EndedAt != benefit.CompletedAt || benefit.Revision < interval.Revision
                        || interval.SiteId == "" || interval.ScheduledEnd != benefit.CompletedAt)
                        throw new ArgumentException("Beneficial Long Rest has no exact completed interval.");
                    if (i > 0 && benefit.CompletedAt < ordered[i - 1].CompletedAt.AddSeconds(24 * 60 * 60))
                        throw new ArgumentException("Beneficial Long Rest limit is less than 24 elapsed hours.");
                    var linkedOffer = s.ExpeditionStrainRecoveryOffers.SingleOrDefault(x =>
                        x.RestIntervalId == benefit.RestIntervalId);
                    if (benefit.RecoveryOfferId == "" ? linkedOffer != null
                        : linkedOffer == null || linkedOffer.Id != benefit.RecoveryOfferId
                            || linkedOffer.ActorId != benefit.ActorId || linkedOffer.CompletedAt != benefit.CompletedAt)
                        throw new ArgumentException("Beneficial Long Rest offer link is invalid.");
                }
            }

            if (s.ExpeditionStrainRecoveryOffers.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryOffers.Length
                || s.ExpeditionStrainRecoveryOffers.Select(x => x.RestIntervalId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryOffers.Length
                || s.ExpeditionStrainRecoveryOffers.Where(x => x.Pending).Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryOffers.Count(x => x.Pending)
                || s.ExpeditionStrainRecoveryOffers.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.CompletedAt > s.RuleClock || x.Pending && x.CompletedAt != s.RuleClock
                    || !s.Receipts.Any(r => r.Id == x.InitiatingCommandId && r.Revision == x.Revision)
                    || !x.Pending && (x.ResolvedRevision > s.Revision || x.ResolvedRevision <= x.Revision)))
                throw new ArgumentException("Invalid pending Expedition Strain recovery offer.");
            foreach (var offer in s.ExpeditionStrainRecoveryOffers)
            {
                var interval = s.RestIntervals.SingleOrDefault(x => x.Id == offer.RestIntervalId);
                if (interval == null || interval.ActorId != offer.ActorId || interval.Status != RestIntervalStatus.Completed
                    || interval.EndedAt != offer.CompletedAt)
                    throw new ArgumentException("Recovery offer has no exact completed Rest.");
                var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.RestIntervalId == offer.RestIntervalId);
                bool legacyPending = offer.Pending && benefit == null;
                if (!legacyPending && (benefit == null || benefit.RecoveryOfferId != offer.Id || benefit.ActorId != offer.ActorId
                    || benefit.CompletedAt != offer.CompletedAt
                    || benefit.Revision != offer.Revision && benefit.Revision != offer.ResolvedRevision))
                    throw new ArgumentException("Recovery offer has no matching beneficial Rest record.");
                var latestSettlement = s.DailyProvisioningSettlements.Where(x => x.ActorId == offer.ActorId && x.End <= offer.CompletedAt)
                    .OrderByDescending(x => x.End).FirstOrDefault();
                if (offer.Pending && latestSettlement != null && latestSettlement.HasShortfall)
                    throw new ArgumentException("A recovery offer remains open while the actor provisioning block is active.");
                foreach (string pointId in offer.PointIds)
                {
                    var gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.PointId == pointId);
                    bool gateMet = gain != null && (gain.RemovalGateMet == true
                        || s.ExpeditionStrainRecoveryGateUpdates.Any(x => x.PointId == pointId
                            && x.At <= offer.CompletedAt && x.Revision <= offer.Revision));
                    bool activeAtCompletion = gain != null && gain.At <= offer.CompletedAt && gain.Revision <= offer.Revision
                        && !s.ExpeditionStrainRemovals.Any(x => x.ActorId == offer.ActorId && x.PointId == pointId
                            && x.At <= offer.CompletedAt && x.Revision <= offer.Revision);
                    if (gain == null || gain.ActorId != offer.ActorId || gain.AddedAmount != 1
                        || gain.OrdinaryRemovable != true || !gateMet || !activeAtCompletion)
                        throw new ArgumentException("Recovery offer contains an unclassified or unqualified point.");
                    if (!offer.Pending && offer.ChosenPointId == pointId
                        && !s.ExpeditionStrainRemovals.Any(x => x.BeneficialRestId == benefit.Id && x.PointId == pointId))
                        throw new ArgumentException("Chosen recovery point has no matching removal event.");
                }
                if (offer.Pending && benefit != null
                    && s.ExpeditionStrainRemovals.Any(x => x.BeneficialRestId == benefit.Id))
                    throw new ArgumentException("Pending recovery offer already removed a Strain point.");
            }

            if (s.ExpeditionStrainRemovals.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRemovals.Length
                || s.ExpeditionStrainRemovals.Select(x => x.PointId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRemovals.Length
                || s.ExpeditionStrainRemovals.Select(x => x.BeneficialRestId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRemovals.Length
                || s.ExpeditionStrainRemovals.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.At > s.RuleClock))
                throw new ArgumentException("Invalid Expedition Strain point-removal history.");
            foreach (var removal in s.ExpeditionStrainRemovals)
            {
                var gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.Id == removal.GainId);
                var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.Id == removal.BeneficialRestId);
                var offer = benefit == null ? null : s.ExpeditionStrainRecoveryOffers.SingleOrDefault(x =>
                    x.RestIntervalId == benefit.RestIntervalId);
                if (gain == null || gain.ActorId != removal.ActorId || gain.PointId != removal.PointId
                    || gain.AddedAmount != 1 || gain.OrdinaryRemovable != true || benefit == null
                    || benefit.ActorId != removal.ActorId || benefit.CompletedAt != removal.At
                    || benefit.Revision > removal.Revision || offer == null || offer.Pending
                    || benefit.RecoveryOfferId != offer.Id || offer.ChosenPointId != removal.PointId
                    || offer.ResolvedRevision != removal.Revision)
                    throw new ArgumentException("Strain removal is not linked to one eligible point and its Rest.");
            }

            // Schema64 orders gains and removals in one actor-local event stream. Gain records
            // retain their original causes; removal events only change whether a point is active.
            foreach (string actor in s.ExpeditionStrainGains.Select(x => x.ActorId)
                .Concat(s.ExpeditionStrainRemovals.Select(x => x.ActorId)).Distinct(StringComparer.Ordinal))
            {
                var events = s.ExpeditionStrainGains.Where(x => x.ActorId == actor).Select(x => new StrainEvent(
                        x.At, x.Revision, x.GainSequence, x, null))
                    .Concat(s.ExpeditionStrainRemovals.Where(x => x.ActorId == actor).Select(x => new StrainEvent(
                        x.At, x.Revision, x.MutationSequence, null, x)))
                    .OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.Sequence).ToArray();
                if (events.GroupBy(x => x.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + "|"
                    + x.Sequence.ToString(System.Globalization.CultureInfo.InvariantCulture), StringComparer.Ordinal).Any(x => x.Count() > 1))
                    throw new ArgumentException("Expedition Strain mutation sequence is not unique within the command.");
                int level = 0;
                var activePoints = new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal);
                foreach (var item in events)
                {
                    if (item.Gain != null)
                    {
                        var gain = item.Gain;
                        if (gain.LevelBefore != level || gain.AttemptedAmount != 1
                            || gain.AddedAmount != Math.Min(1, 6 - level))
                            throw new ArgumentException("Expedition Strain active-point history is not cumulative.");
                        if (gain.AddedAmount > 0) { activePoints.Add(gain.PointId); level++; }
                    }
                    else
                    {
                        if (!activePoints.Remove(item.Removal.PointId) || level <= 0)
                            throw new ArgumentException("Expedition Strain removal targets an inactive or absent point.");
                        level--;
                    }
                }
            }
        }

        private static void ValidateSchema65RecoveryReferences(Snapshot s, Func<string, bool> actorExists,
            Func<string, bool> settlementExists)
        {
            if (s.ExpeditionStrainRecoveryGateUpdates.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryGateUpdates.Length
                || s.ExpeditionStrainRecoveryGateUpdates.Select(x => x.PointId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryGateUpdates.Length
                || s.ExpeditionStrainRecoveryGateUpdates.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.At > s.RuleClock || !settlementExists(x.SettlementId)))
                throw new ArgumentException("Invalid Expedition Strain recovery gate history.");
            foreach (var update in s.ExpeditionStrainRecoveryGateUpdates)
            {
                var settlement = s.DailyProvisioningSettlements.Single(x => x.Id == update.SettlementId);
                var gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.PointId == update.PointId);
                if (settlement.ActorId != update.ActorId || settlement.HasShortfall || settlement.End != update.At
                    || settlement.Revision != update.Revision || gain == null || gain.ActorId != update.ActorId
                    || gain.CauseKind != ExpeditionStrainCauseKind.DailyProvisioning || gain.OrdinaryRemovable != true
                    || gain.RemovalGateMet != false || gain.At >= update.At
                    || s.DailyProvisioningSettlements.Single(x => x.Id == gain.CauseId).DayOrdinal >= settlement.DayOrdinal)
                    throw new ArgumentException("Recovery gate update is not proven by a later supported day.");
            }

            if (s.ExpeditionBeneficialRests.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionBeneficialRests.Length
                || s.ExpeditionBeneficialRests.Select(x => x.RestIntervalId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionBeneficialRests.Length
                || s.ExpeditionBeneficialRests.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.CompletedAt > s.RuleClock || x.RecoveryOfferId == null
                    || x.RecoveryOfferId != "" && !Validation.ValidId(x.RecoveryOfferId)))
                throw new ArgumentException("Invalid beneficial Long Rest history.");
            foreach (var group in s.ExpeditionBeneficialRests.GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                var ordered = group.OrderBy(x => x.CompletedAt).ThenBy(x => x.Revision).ToArray();
                for (int i = 0; i < ordered.Length; i++)
                {
                    var benefit = ordered[i];
                    var interval = s.RestIntervals.SingleOrDefault(x => x.Id == benefit.RestIntervalId);
                    if (interval == null || interval.ActorId != benefit.ActorId || interval.Status != RestIntervalStatus.Completed
                        || interval.EndedAt != benefit.CompletedAt || benefit.Revision < interval.Revision
                        || interval.SiteId == "" || interval.ScheduledEnd != benefit.CompletedAt)
                        throw new ArgumentException("Beneficial Long Rest has no exact completed interval.");
                    if (i > 0 && benefit.CompletedAt < ordered[i - 1].CompletedAt.AddSeconds(24 * 60 * 60))
                        throw new ArgumentException("Beneficial Long Rest limit is less than 24 elapsed hours.");
                    var linkedOffer = s.ExpeditionStrainRecoveryOffers.SingleOrDefault(x =>
                        x.RecoveryKind == ExpeditionRecoveryKind.SecureLongRest && x.ActivityIntervalId == benefit.RestIntervalId);
                    if (benefit.RecoveryOfferId == "" ? linkedOffer != null
                        : linkedOffer == null || linkedOffer.Id != benefit.RecoveryOfferId
                            || linkedOffer.RecoveryCompletionId != benefit.Id || linkedOffer.ActorId != benefit.ActorId
                            || linkedOffer.CompletedAt != benefit.CompletedAt)
                        throw new ArgumentException("Beneficial Long Rest offer link is invalid.");
                }
            }

            if (s.ExpeditionMoraleRestIntervals.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionMoraleRestIntervals.Length
                || s.ExpeditionMoraleRestIntervals.Any(x => !actorExists(x.ActorId) || x.StartRevision > s.Revision
                    || x.EndRevision > s.Revision || x.StartedAt > s.RuleClock || x.EndedAt.HasValue && x.EndedAt.Value > s.RuleClock
                    || !s.Receipts.Any(r => r.Id == x.StartCommandId && r.Revision == x.StartRevision
                        && CommandHistory.Read(r).Kind == CommandKind.BeginMoraleRest)
                    || x.Status == MoraleRestIntervalStatus.Active && (x.EndedAt.HasValue || x.EndCommandId != ""
                        || x.EndRevision != 0 || x.ScheduledEnd <= s.RuleClock)
                    || x.Status == MoraleRestIntervalStatus.Completed && x.EndedAt != x.ScheduledEnd
                    || x.Status == MoraleRestIntervalStatus.Interrupted && (!x.EndedAt.HasValue || x.EndedAt.Value > x.ScheduledEnd)
                    || x.Status != MoraleRestIntervalStatus.Active && !s.Receipts.Any(r => r.Id == x.EndCommandId
                        && r.Revision == x.EndRevision && (x.Status == MoraleRestIntervalStatus.Completed
                            || x.Status == MoraleRestIntervalStatus.Interrupted
                                && (CommandHistory.Read(r).Kind == CommandKind.InterruptMoraleRest
                                    && x.EndedAt.Value < x.ScheduledEnd
                                    || CommandHistory.Read(r).Kind == CommandKind.AdvanceClock
                                        && x.EndedAt.Value <= x.ScheduledEnd)))))
                throw new ArgumentException("Invalid Morale Rest interval history.");
            foreach (var interval in s.ExpeditionMoraleRestIntervals)
                if (interval.ScheduledEnd != interval.StartedAt.AddSeconds(4 * 60 * 60))
                    throw new ArgumentException("Morale Rest interval is not four consecutive hours.");

            if (s.ExpeditionMoraleRestBenefits.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionMoraleRestBenefits.Length
                || s.ExpeditionMoraleRestBenefits.Select(x => x.IntervalId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionMoraleRestBenefits.Length
                || s.ExpeditionMoraleRestBenefits.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.CompletedAt > s.RuleClock || x.RecoveryOfferId == null
                    || x.RecoveryOfferId != "" && !Validation.ValidId(x.RecoveryOfferId)))
                throw new ArgumentException("Invalid Morale Rest benefit history.");
            foreach (var group in s.ExpeditionMoraleRestBenefits.GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                var ordered = group.OrderBy(x => x.CompletedAt).ThenBy(x => x.Revision).ToArray();
                for (int i = 0; i < ordered.Length; i++)
                {
                    var benefit = ordered[i];
                    var interval = s.ExpeditionMoraleRestIntervals.SingleOrDefault(x => x.Id == benefit.IntervalId);
                    if (interval == null || interval.ActorId != benefit.ActorId
                        || interval.Status != MoraleRestIntervalStatus.Completed || interval.EndedAt != benefit.CompletedAt
                        || benefit.Revision < interval.EndRevision)
                        throw new ArgumentException("Morale Rest benefit has no exact completed interval.");
                    if (i > 0 && benefit.CompletedAt < ordered[i - 1].CompletedAt.AddSeconds(24 * 60 * 60))
                        throw new ArgumentException("Morale Rest benefit limit is less than 24 elapsed hours.");
                    var offer = s.ExpeditionStrainRecoveryOffers.SingleOrDefault(x =>
                        x.RecoveryKind == ExpeditionRecoveryKind.MoraleRest && x.RecoveryCompletionId == benefit.Id);
                    if (benefit.RecoveryOfferId == "" ? offer != null
                        : offer == null || offer.Id != benefit.RecoveryOfferId || offer.ActorId != benefit.ActorId
                            || offer.CompletedAt != benefit.CompletedAt || offer.ActivityIntervalId != interval.Id)
                        throw new ArgumentException("Morale Rest benefit offer link is invalid.");
                }
            }
            foreach (var group in s.ExpeditionMoraleRestIntervals.Where(x => x.Status == MoraleRestIntervalStatus.Completed)
                .GroupBy(x => x.ActorId, StringComparer.Ordinal))
            {
                RuleTime? lastBenefit = null;
                foreach (var interval in group.OrderBy(x => x.EndedAt).ThenBy(x => x.EndRevision))
                {
                    bool shouldConsume = !lastBenefit.HasValue
                        || interval.EndedAt.Value >= lastBenefit.Value.AddSeconds(24 * 60 * 60);
                    var benefit = s.ExpeditionMoraleRestBenefits.SingleOrDefault(x => x.IntervalId == interval.Id);
                    if (shouldConsume != (benefit != null))
                        throw new ArgumentException("Morale Rest completion does not match the independent allowance.");
                    if (benefit != null) lastBenefit = benefit.CompletedAt;
                }
            }

            if (s.ExpeditionStrainRecoveryOffers.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryOffers.Length
                || s.ExpeditionStrainRecoveryOffers.Select(x => ((int)x.RecoveryKind).ToString(
                    System.Globalization.CultureInfo.InvariantCulture) + "|" + x.RecoveryCompletionId)
                    .Distinct(StringComparer.Ordinal).Count() != s.ExpeditionStrainRecoveryOffers.Length
                || s.ExpeditionStrainRecoveryOffers.Where(x => x.Pending).Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRecoveryOffers.Count(x => x.Pending)
                || s.ExpeditionStrainRecoveryOffers.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.CompletedAt > s.RuleClock || x.Pending && x.CompletedAt != s.RuleClock
                    || !Validation.ValidId(x.RecoveryCompletionId) || !Validation.ValidId(x.ActivityIntervalId)
                    || !s.Receipts.Any(r => r.Id == x.InitiatingCommandId && r.Revision == x.Revision)
                    || !x.Pending && (x.ResolvedRevision > s.Revision || x.ResolvedRevision <= x.Revision)))
                throw new ArgumentException("Invalid pending typed Expedition Strain recovery offer.");
            foreach (var offer in s.ExpeditionStrainRecoveryOffers)
            {
                bool hasBenefit;
                if (offer.RecoveryKind == ExpeditionRecoveryKind.SecureLongRest)
                {
                    if (offer.RestIntervalId != offer.ActivityIntervalId)
                        throw new ArgumentException("Secure Long Rest offer lost its interval identity.");
                    var interval = s.RestIntervals.SingleOrDefault(x => x.Id == offer.ActivityIntervalId);
                    var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.Id == offer.RecoveryCompletionId
                        && x.RestIntervalId == offer.ActivityIntervalId);
                    hasBenefit = benefit != null && benefit.ActorId == offer.ActorId
                        && benefit.CompletedAt == offer.CompletedAt && benefit.RecoveryOfferId == offer.Id
                        && (benefit.Revision == offer.Revision || benefit.Revision == offer.ResolvedRevision);
                    if (interval == null || interval.ActorId != offer.ActorId || interval.Status != RestIntervalStatus.Completed
                        || interval.EndedAt != offer.CompletedAt || !hasBenefit)
                        throw new ArgumentException("Secure Long Rest offer has no exact completion.");
                }
                else if (offer.RecoveryKind == ExpeditionRecoveryKind.MoraleRest)
                {
                    var interval = s.ExpeditionMoraleRestIntervals.SingleOrDefault(x => x.Id == offer.ActivityIntervalId);
                    var benefit = s.ExpeditionMoraleRestBenefits.SingleOrDefault(x => x.Id == offer.RecoveryCompletionId
                        && x.IntervalId == offer.ActivityIntervalId);
                    hasBenefit = benefit != null && benefit.ActorId == offer.ActorId
                        && benefit.CompletedAt == offer.CompletedAt && benefit.RecoveryOfferId == offer.Id
                        && (benefit.Revision == offer.Revision || benefit.Revision == offer.ResolvedRevision);
                    if (interval == null || interval.ActorId != offer.ActorId
                        || interval.Status != MoraleRestIntervalStatus.Completed || interval.EndedAt != offer.CompletedAt
                        || !hasBenefit)
                        throw new ArgumentException("Morale Rest offer has no exact completion.");
                }
                else throw new ArgumentException("Unknown Expedition Strain recovery kind.");

                var latestSettlement = s.DailyProvisioningSettlements.Where(x => x.ActorId == offer.ActorId
                        && x.End <= offer.CompletedAt).OrderByDescending(x => x.End).FirstOrDefault();
                if (latestSettlement != null && latestSettlement.HasShortfall)
                    throw new ArgumentException("A recovery offer remains open while provisioning is blocked.");
                foreach (string pointId in offer.PointIds)
                {
                    var gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.PointId == pointId);
                    bool gateMet = gain != null && (gain.RemovalGateMet == true
                        || s.ExpeditionStrainRecoveryGateUpdates.Any(x => x.PointId == pointId
                            && x.At <= offer.CompletedAt && x.Revision <= offer.Revision));
                    bool activeAtCompletion = gain != null && gain.At <= offer.CompletedAt && gain.Revision <= offer.Revision
                        && !s.ExpeditionStrainRemovals.Any(x => x.ActorId == offer.ActorId && x.PointId == pointId
                            && x.At <= offer.CompletedAt && x.Revision <= offer.Revision);
                    if (gain == null || gain.ActorId != offer.ActorId || gain.AddedAmount != 1
                        || gain.OrdinaryRemovable != true || !gateMet || !activeAtCompletion)
                        throw new ArgumentException("Recovery offer contains an unclassified or unqualified point.");
                    if (!offer.Pending && offer.ChosenPointId == pointId
                        && !s.ExpeditionStrainRemovals.Any(x => x.RecoveryKind == offer.RecoveryKind
                            && x.RecoveryCompletionId == offer.RecoveryCompletionId && x.PointId == pointId))
                        throw new ArgumentException("Chosen recovery point has no matching removal event.");
                }
                if (offer.Pending && s.ExpeditionStrainRemovals.Any(x => x.RecoveryKind == offer.RecoveryKind
                    && x.RecoveryCompletionId == offer.RecoveryCompletionId))
                    throw new ArgumentException("Pending recovery offer already removed a Strain point.");
            }

            if (s.ExpeditionStrainRemovals.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRemovals.Length
                || s.ExpeditionStrainRemovals.Select(x => x.PointId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionStrainRemovals.Length
                || s.ExpeditionStrainRemovals.GroupBy(x => ((int)x.RecoveryKind).ToString(
                    System.Globalization.CultureInfo.InvariantCulture) + "|" + x.RecoveryCompletionId,
                    StringComparer.Ordinal).Any(x => x.Count() > 1
                        && x.First().RecoveryKind != ExpeditionRecoveryKind.HavenCare)
                || s.ExpeditionStrainRemovals.Any(x => !actorExists(x.ActorId) || x.Revision > s.Revision
                    || x.At > s.RuleClock || !Validation.ValidId(x.RecoveryCompletionId)))
                throw new ArgumentException("Invalid typed Expedition Strain point-removal history.");
            foreach (var removal in s.ExpeditionStrainRemovals)
            {
                var gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.Id == removal.GainId);
                var offer = s.ExpeditionStrainRecoveryOffers.SingleOrDefault(x =>
                    x.RecoveryKind == removal.RecoveryKind && x.RecoveryCompletionId == removal.RecoveryCompletionId);
                var havenAssessment = removal.RecoveryKind == ExpeditionRecoveryKind.HavenCare
                    ? s.ExpeditionHavenCareAssessments.SingleOrDefault(x => x.Id == removal.RecoveryCompletionId) : null;
                bool completionMatches = removal.RecoveryKind == ExpeditionRecoveryKind.SecureLongRest
                    ? s.ExpeditionBeneficialRests.Any(x => x.Id == removal.RecoveryCompletionId
                        && x.ActorId == removal.ActorId && x.CompletedAt == removal.At && x.Revision <= removal.Revision)
                    : removal.RecoveryKind == ExpeditionRecoveryKind.MoraleRest
                        && s.ExpeditionMoraleRestBenefits.Any(x => x.Id == removal.RecoveryCompletionId
                            && x.ActorId == removal.ActorId && x.CompletedAt == removal.At && x.Revision <= removal.Revision)
                        || removal.RecoveryKind == ExpeditionRecoveryKind.HavenCare
                            && havenAssessment != null && havenAssessment.ActorId == removal.ActorId
                            && havenAssessment.CompletedAt == removal.At && havenAssessment.Revision == removal.Revision
                            && havenAssessment.EligiblePointIds.Contains(removal.PointId, StringComparer.Ordinal);
                bool offerMatches = removal.RecoveryKind == ExpeditionRecoveryKind.HavenCare
                    ? offer == null
                    : offer != null && !offer.Pending && offer.ChosenPointId == removal.PointId
                        && offer.ResolvedRevision == removal.Revision && offer.ActorId == removal.ActorId
                        && offer.CompletedAt == removal.At;
                if (gain == null || gain.ActorId != removal.ActorId || gain.PointId != removal.PointId
                    || gain.AddedAmount != 1 || gain.OrdinaryRemovable != true || !completionMatches
                    || !offerMatches)
                    throw new ArgumentException("Strain removal is not linked to one eligible point and typed completion.");
            }

            ValidateHavenCareHistory(s, actorExists);

            ValidateStrainMutationOrder(s);
        }

        private static void ValidateHavenCareHistory(Snapshot s, Func<string, bool> actorExists)
        {
            if (s.SchemaVersion < Snapshot.HavenCareSchema)
            {
                if (s.ExpeditionHavenCareIntervals.Length != 0 || s.ExpeditionHavenCareAssessments.Length != 0
                    || s.ExpeditionStrainRemovals.Any(x => x.RecoveryKind == ExpeditionRecoveryKind.HavenCare))
                    throw new ArgumentException("Haven-care history requires schema66.");
                return;
            }

            if (s.ExpeditionHavenCareIntervals.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionHavenCareIntervals.Length
                || s.ExpeditionHavenCareAssessments.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionHavenCareAssessments.Length
                || s.ExpeditionHavenCareAssessments.Select(x => x.IntervalId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionHavenCareAssessments.Length
                || s.ExpeditionHavenCareIntervals.Count(x => x.Status == HavenCareIntervalStatus.Active) > 1
                || s.ExpeditionHavenCareIntervals.Any(x => !actorExists(x.ActorId) || x.StartRevision > s.Revision
                    || x.StartedAt > s.RuleClock || x.ScheduledEnd != x.StartedAt.AddSeconds(86400)
                    || !s.Receipts.Any(r => r.Id == x.StartCommandId && r.Revision == x.StartRevision
                        && CommandHistory.Read(r).Kind == CommandKind.BeginHavenCare)
                    || x.Status == HavenCareIntervalStatus.Active && (x.ScheduledEnd <= s.RuleClock
                        || x.EndedAt.HasValue || x.EndCommandId != ""
                        || x.EndCommandRevision != 0 || x.EndRevision != 0)
                    || x.Status == HavenCareIntervalStatus.Completed && x.EndedAt != x.ScheduledEnd
                    || x.EndedAt.HasValue && (x.EndedAt.Value > s.RuleClock || x.EndRevision > s.Revision
                        || x.EndCommandRevision > x.EndRevision
                        || !s.Receipts.Any(r => r.Id == x.EndCommandId && r.Revision == x.EndCommandRevision
                            && (CommandHistory.Read(r).Kind == CommandKind.AdvanceClock
                                || CommandHistory.Read(r).Kind == CommandKind.InterruptHavenCare
                                || CommandHistory.Read(r).Kind == CommandKind.BeginFixedEncounter
                                || CommandHistory.Read(r).Kind == CommandKind.BeginWorldStep
                                || CommandHistory.Read(r).Kind == CommandKind.EnterInventoryCombat
                                || CommandHistory.Read(r).Kind == CommandKind.DispatchConditionEvent)))))
                throw new ArgumentException("Invalid Haven-care interval history.");

            foreach (var interval in s.ExpeditionHavenCareIntervals)
            {
                bool hasAssessment = s.ExpeditionHavenCareAssessments.Any(x => x.IntervalId == interval.Id);
                if ((interval.Status == HavenCareIntervalStatus.Completed) != hasAssessment
                    || interval.Status == HavenCareIntervalStatus.Active && hasAssessment)
                    throw new ArgumentException("Haven-care completion assessment does not match its interval status.");
                if (s.ExpeditionHavenCareIntervals.Any(x => x.Id != interval.Id
                    && x.StartedAt < (interval.EndedAt ?? interval.ScheduledEnd)
                    && interval.StartedAt < (x.EndedAt ?? x.ScheduledEnd)))
                    throw new ArgumentException("The single Haven-care patient slot overlaps two intervals.");
            }

            foreach (var assessment in s.ExpeditionHavenCareAssessments)
            {
                var interval = s.ExpeditionHavenCareIntervals.SingleOrDefault(x => x.Id == assessment.IntervalId);
                if (interval == null || interval.Status != HavenCareIntervalStatus.Completed
                    || interval.ActorId != assessment.ActorId || interval.EndedAt != assessment.CompletedAt
                    || interval.EndCommandId == "" || interval.EndRevision != assessment.Revision
                    || assessment.Revision > s.Revision || assessment.CompletedAt > s.RuleClock
                    || assessment.IntakeIds.Any(id => !s.Intakes.Any(x => x.Id == id && x.ActorId == assessment.ActorId)))
                    throw new ArgumentException("Haven-care assessment has no exact completed interval or support evidence.");

                string[] removals = s.ExpeditionStrainRemovals.Where(x =>
                        x.RecoveryKind == ExpeditionRecoveryKind.HavenCare
                        && x.RecoveryCompletionId == assessment.Id && x.ActorId == assessment.ActorId
                        && x.At == assessment.CompletedAt && x.Revision == assessment.Revision)
                    .OrderBy(x => x.MutationSequence).Select(x => x.PointId).ToArray();
                if (!removals.SequenceEqual(assessment.EligiblePointIds, StringComparer.Ordinal))
                    throw new ArgumentException("Haven-care Strain removals do not match the complete eligible batch.");
            }
        }

        private static void ValidateStrainMutationOrder(Snapshot s)
        {
            foreach (string actor in s.ExpeditionStrainGains.Select(x => x.ActorId)
                .Concat(s.ExpeditionStrainRemovals.Select(x => x.ActorId)).Distinct(StringComparer.Ordinal))
            {
                var events = s.ExpeditionStrainGains.Where(x => x.ActorId == actor).Select(x => new StrainEvent(
                        x.At, x.Revision, x.GainSequence, x, null))
                    .Concat(s.ExpeditionStrainRemovals.Where(x => x.ActorId == actor).Select(x => new StrainEvent(
                        x.At, x.Revision, x.MutationSequence, null, x)))
                    .OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.Sequence).ToArray();
                if (events.GroupBy(x => x.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + "|"
                    + x.Sequence.ToString(System.Globalization.CultureInfo.InvariantCulture), StringComparer.Ordinal).Any(x => x.Count() > 1))
                    throw new ArgumentException("Expedition Strain mutation sequence is not unique within the command.");
                int level = 0;
                var activePoints = new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal);
                foreach (var item in events)
                {
                    if (item.Gain != null)
                    {
                        var gain = item.Gain;
                        if (gain.LevelBefore != level || gain.AttemptedAmount != 1
                            || gain.AddedAmount != Math.Min(1, 6 - level))
                            throw new ArgumentException("Expedition Strain active-point history is not cumulative.");
                        if (gain.AddedAmount > 0) { activePoints.Add(gain.PointId); level++; }
                    }
                    else if (!activePoints.Remove(item.Removal.PointId) || level <= 0)
                        throw new ArgumentException("Expedition Strain removal targets an inactive or absent point.");
                    else level--;
                }
            }
        }

        private sealed class StrainEvent
        {
            public RuleTime At { get; }
            public long Revision { get; }
            public int Sequence { get; }
            public ExpeditionStrainGainRecord Gain { get; }
            public ExpeditionStrainRemovalRecord Removal { get; }
            public StrainEvent(RuleTime at, long revision, int sequence, ExpeditionStrainGainRecord gain,
                ExpeditionStrainRemovalRecord removal)
            { At = at; Revision = revision; Sequence = sequence; Gain = gain; Removal = removal; }
        }
    }
}
