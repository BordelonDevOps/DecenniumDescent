using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ExpeditionCloseField
    {
        Outcome, MembersAndLocations, LifeAndInjuries, Conditions, ProvisionsAndContainers, ResourcePools,
        Movement, NamedRouteTravel, Camps, Pressure, Pursuit, Heat, Strain, RestDebt, Companions, Devices,
        HostileDeath, CorpseHandling, CargoTitleAndCustody, MiningDispositions, HarvestAndSalvageClaims,
        QuotesAndPayments, WiderLiabilitiesAndProfit, Insurance, StandingAndRenown, FactionActions, RecordedAdvancement,
        UnadjudicatedEntitlements
    }

    public enum ExpeditionCloseKnowledge { KnownValue = 1, KnownNone, NotApplicable, Unresolved }
    public enum ExpeditionCloseMetric { RealizedNetExpedition = 1 }

    public sealed class ExpeditionCloseCoverage
    {
        public ExpeditionCloseField Field { get; }
        public ExpeditionCloseKnowledge Knowledge { get; }
        public string BasisId { get; }

        public ExpeditionCloseCoverage(ExpeditionCloseField field, ExpeditionCloseKnowledge knowledge, string basisId)
        {
            if (!Enum.IsDefined(typeof(ExpeditionCloseField), field) || !Enum.IsDefined(typeof(ExpeditionCloseKnowledge), knowledge)
                || !Validation.ValidId(basisId)) throw new ArgumentException("Invalid Expedition close coverage.");
            Field = field;
            Knowledge = knowledge;
            BasisId = basisId;
        }
    }

    public sealed class ExpeditionCloseCondition
    {
        public string ApplicationId { get; }
        public string Kind { get; }
        public bool Effective { get; }
        public bool Inherited { get; }
        public ConditionStamp? Expires { get; }

        public ExpeditionCloseCondition(string applicationId, string kind, bool effective, bool inherited, ConditionStamp? expires)
        {
            if (!Validation.ValidId(applicationId) || !Validation.ValidId(kind) || inherited && !effective)
                throw new ArgumentException("Invalid captured Expedition condition.");
            ApplicationId = applicationId;
            Kind = kind;
            Effective = effective;
            Inherited = inherited;
            Expires = expires;
        }
    }

    public sealed class ExpeditionCloseMember
    {
        public string ActorId => Life.ActorId;
        public ActorLifeRecord Life { get; }
        public RuleQuantity X { get; }
        public RuleQuantity Y { get; }
        public long LastMovementRevision { get; }
        public int AttainedLevels { get; }
        public IReadOnlyList<ExpeditionCloseCondition> Conditions { get; }

        public ExpeditionCloseMember(ActorLifeRecord life, RuleQuantity x, RuleQuantity y, long lastMovementRevision,
            int attainedLevels, IEnumerable<ExpeditionCloseCondition> conditions)
        {
            if (life == null || lastMovementRevision < 0 || attainedLevels < 1 || attainedLevels > 20)
                throw new ArgumentException("Invalid Expedition member closing facts.");
            Life = life;
            X = x;
            Y = y;
            LastMovementRevision = lastMovementRevision;
            AttainedLevels = attainedLevels;
            Conditions = Array.AsReadOnly(ExpeditionEpisodeCloseRecord.Freeze(conditions, 256, item => (item.ApplicationId, item.Kind))
                .OrderBy(item => item.ApplicationId, StringComparer.Ordinal).ThenBy(item => item.Kind, StringComparer.Ordinal).ToArray());
        }
    }

    public sealed class ExpeditionCloseStock
    {
        public InventoryLotRecord Provenance { get; }
        public ResourceLot Stock { get; }

        public ExpeditionCloseStock(InventoryLotRecord provenance, ResourceLot stock)
        {
            if (provenance == null || stock == null || provenance.LotId != stock.Id)
                throw new ArgumentException("Invalid Expedition stock closing facts.");
            Provenance = provenance;
            Stock = stock;
        }
    }

    public sealed class ExpeditionCloseMiningDisposition
    {
        public string UnitId { get; }
        public MiningUnitStatus Status { get; }
        public string ReceivedLotId { get; }

        public ExpeditionCloseMiningDisposition(string unitId, MiningUnitStatus status, string receivedLotId)
        {
            if (!Validation.ValidId(unitId) || !Enum.IsDefined(typeof(MiningUnitStatus), status)
                || status == MiningUnitStatus.Available || receivedLotId == null
                || (status == MiningUnitStatus.Extracted ? !Validation.ValidId(receivedLotId) : receivedLotId != ""))
                throw new ArgumentException("Invalid Expedition mining closing facts.");
            UnitId = unitId;
            Status = status;
            ReceivedLotId = receivedLotId;
        }
    }

    public sealed class ExpeditionCloseOutcome
    {
        public ExpeditionCloseMetric PrimaryMetric { get; }
        public long RealizedNetCopper { get; }
        public RuleQuantity NetTargetCopper { get; }
        public long RealizedGrossCopper { get; }
        public RuleQuantity GrossTargetCopper { get; }
        public RuleQuantity ProfitTargetCopper { get; }
        public bool PrimaryTargetMet => new RuleQuantity(RealizedNetCopper) >= NetTargetCopper;
        public bool GrossTargetMet => new RuleQuantity(RealizedGrossCopper) >= GrossTargetCopper;
        public bool? ProfitTargetMet => null;

        public ExpeditionCloseOutcome(ExpeditionCloseMetric primaryMetric, long realizedNetCopper, RuleQuantity netTargetCopper,
            long realizedGrossCopper, RuleQuantity grossTargetCopper, RuleQuantity profitTargetCopper)
        {
            if (primaryMetric != ExpeditionCloseMetric.RealizedNetExpedition || realizedNetCopper < 0 || realizedGrossCopper < 0)
                throw new ArgumentException("Invalid declared Expedition outcome.");
            PrimaryMetric = primaryMetric;
            RealizedNetCopper = realizedNetCopper;
            NetTargetCopper = netTargetCopper;
            RealizedGrossCopper = realizedGrossCopper;
            GrossTargetCopper = grossTargetCopper;
            ProfitTargetCopper = profitTargetCopper;
        }
    }

    /// <summary>Authoritative as-of projection, rebuilt from the historical command boundary by the selected policy.</summary>
    public sealed class ExpeditionEpisodeCloseRecord
    {
        public string EpisodeId { get; }
        public string CharterVersionId { get; }
        public string CloserId { get; }
        public string MandateId { get; }
        public string EvidenceAuthorityId { get; }
        public string CommandId { get; }
        public long SourceRevision { get; }
        public long CloseRevision => SourceRevision + 1;
        public RuleTime ClosedAt { get; }
        public string BillId { get; }
        public long BillReportRevision { get; }
        public string EncounterId { get; }
        public long EncounterExitRevision { get; }
        public string HostileId { get; }
        public RuleQuantity HostileX { get; }
        public RuleQuantity HostileY { get; }
        public string MiningAttemptId { get; }
        public string MealIntakeId { get; }
        public ExpeditionCloseOutcome Outcome { get; }
        public IReadOnlyList<ExpeditionCloseMember> Members { get; }
        public IReadOnlyList<ExpeditionCloseMiningDisposition> MiningDispositions { get; }
        public IReadOnlyList<ExpeditionCloseStock> Stock { get; }
        public IReadOnlyList<PortableEquipmentRecord> Equipment { get; }
        public IReadOnlyList<WaterVesselRecord> Vessels { get; }
        public IReadOnlyList<ExpeditionCloseCoverage> Coverage { get; }

        public ExpeditionEpisodeCloseRecord(string episodeId, string charterVersionId, string closerId, string mandateId,
            string evidenceAuthorityId, string commandId, long sourceRevision, RuleTime closedAt, string billId,
            long billReportRevision, string encounterId, long encounterExitRevision, string hostileId,
            RuleQuantity hostileX, RuleQuantity hostileY, string miningAttemptId, string mealIntakeId, ExpeditionCloseOutcome outcome,
            IEnumerable<ExpeditionCloseMember> members, IEnumerable<ExpeditionCloseMiningDisposition> miningDispositions,
            IEnumerable<ExpeditionCloseStock> stock, IEnumerable<PortableEquipmentRecord> equipment,
            IEnumerable<WaterVesselRecord> vessels, IEnumerable<ExpeditionCloseCoverage> coverage)
        {
            if (new[] { episodeId, charterVersionId, closerId, mandateId, evidenceAuthorityId, commandId, billId, encounterId,
                hostileId, miningAttemptId, mealIntakeId }.Any(id => !Validation.ValidId(id))
                || sourceRevision < 1 || sourceRevision == long.MaxValue || billReportRevision < 1 || billReportRevision > sourceRevision
                || encounterExitRevision < 1 || encounterExitRevision >= billReportRevision || outcome == null)
                throw new ArgumentException("Invalid Expedition episode close identity or chronology.");
            EpisodeId = episodeId;
            CharterVersionId = charterVersionId;
            CloserId = closerId;
            MandateId = mandateId;
            EvidenceAuthorityId = evidenceAuthorityId;
            CommandId = commandId;
            SourceRevision = sourceRevision;
            ClosedAt = closedAt;
            BillId = billId;
            BillReportRevision = billReportRevision;
            EncounterId = encounterId;
            EncounterExitRevision = encounterExitRevision;
            HostileId = hostileId;
            HostileX = hostileX;
            HostileY = hostileY;
            MiningAttemptId = miningAttemptId;
            MealIntakeId = mealIntakeId;
            Outcome = outcome;
            Members = Ordered(members, 12, x => x.ActorId);
            MiningDispositions = Ordered(miningDispositions, 32, x => x.UnitId);
            Stock = Ordered(stock, WorkLedger.MaxRecords, x => x.Stock.Id);
            Equipment = Ordered(equipment, 128, x => x.Id);
            Vessels = Ordered(vessels, 128, x => x.Id);
            int fields = Enum.GetValues(typeof(ExpeditionCloseField)).Length;
            var coverageRows = Freeze(coverage, fields, x => x.Field);
            if (coverageRows.Count != fields || Members.Count < 1 || !Members.Any(x => x.ActorId == closerId)
                || Members.Any(x => x.LastMovementRevision > sourceRevision) || Members.Any(x => x.ActorId == hostileId))
                throw new ArgumentException("Incomplete Expedition episode closing facts.");
            Coverage = Array.AsReadOnly(coverageRows.OrderBy(x => x.Field).ToArray());
        }

        public ExpeditionCloseCoverage StatusOf(ExpeditionCloseField field) => Coverage.Single(x => x.Field == field);

        private static IReadOnlyList<T> Ordered<T>(IEnumerable<T> rows, int max, Func<T, string> key) where T : class
            => Array.AsReadOnly(Freeze(rows, max, key).OrderBy(key, StringComparer.Ordinal).ToArray());

        internal static IReadOnlyList<T> Freeze<T, TKey>(IEnumerable<T> rows, int max, Func<T, TKey> key) where T : class
        {
            var values = rows?.Take(max + 1).ToArray();
            if (values == null || values.Length > max || values.Any(x => x == null)
                || values.Select(key).Distinct().Count() != values.Length)
                throw new ArgumentException("Invalid closing collection.");
            return values;
        }
    }

    public static class ExpeditionEpisodeCloseValidation
    {
        public static void Validate(Snapshot state)
        {
            var record = state.ExpeditionEpisodeClose;
            if (record == null) return;
            if (state.SchemaVersion != Snapshot.ExpeditionEpisodeCloseSchema || !state.TestOnly)
                throw new ArgumentException("Unexpected Expedition episode close.");
            var charter = state.ExpeditionBillCharter;
            var bill = state.ExpeditionBills.SingleOrDefault(x => x.Id == record.BillId && x.Status == ExpeditionBillStatus.Reconciled);
            var meal = state.HavenMealPurchases.SingleOrDefault(x => x.Id == bill?.Basis.MealId);
            var receipt = state.Receipts.SingleOrDefault(x => x.Revision == record.CloseRevision && x.Id == record.CommandId);
            var encounterExit = state.Receipts.SingleOrDefault(x => x.Revision == record.EncounterExitRevision);
            if (charter == null || bill == null || meal == null || receipt == null || encounterExit == null
                || record.ClosedAt > state.RuleClock || record.ClosedAt < bill.UpdatedAt || bill.UpdatedRevision != record.BillReportRevision
                || charter.EpisodeId != record.EpisodeId || charter.VersionId != record.CharterVersionId
                || !record.Members.Select(x => x.ActorId).SequenceEqual(charter.MemberIds.OrderBy(x => x, StringComparer.Ordinal))
                || record.Outcome.RealizedGrossCopper != bill.Basis.GrossSaleCopper || record.Outcome.RealizedNetCopper != bill.Basis.NetExpeditionCopper
                || record.Outcome.GrossTargetCopper != charter.GrossTargetCopper || record.Outcome.NetTargetCopper != charter.NetTargetCopper
                || record.Outcome.ProfitTargetCopper != charter.ProfitAfterReservesTargetCopper
                || !state.Intakes.Any(x => x.Id == record.MealIntakeId && x.Status == IntakeStatus.Complete
                    && x.ActorId == meal.Offer.CustomerId && x.LotId == meal.Offer.MealLotId && x.EndedAt <= record.ClosedAt)
                || !state.MiningAttempts.Any(x => x.Id == record.MiningAttemptId && x.ClosedAt.HasValue && x.ClosedAt.Value <= record.ClosedAt))
                throw new ArgumentException("Invalid Expedition close provenance.");
            var command = CommandHistory.Read(receipt);
            if (command.Kind != CommandKind.CloseExpeditionEpisode || command.Actor != record.CloserId
                || command.Target != record.EpisodeId || command.ExpectedRevision != record.SourceRevision
                || CommandHistory.Read(encounterExit).Kind != CommandKind.EndFixedEncounter)
                throw new ArgumentException("Expedition close receipt mismatch.");
        }
    }
}
