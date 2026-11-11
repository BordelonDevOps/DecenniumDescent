using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public enum NextCharterPlanStatus { Working = 1, Paused, PendingCompletion, CompletedConditional, Cancelled, Expired, Invalidated }

    [Flags]
    public enum NextCharterAbortCondition
    {
        AccessUnavailable = 1, PassageBlockedOrTactical = 2, ScoutIncapable = 4, SupportInsufficient = 8, ObligationPreventsUse = 16,
        Required = AccessUnavailable | PassageBlockedOrTactical | ScoutIncapable | SupportInsufficient | ObligationPreventsUse
    }

    public sealed class NextCharterPlanTerms
    {
        public string VersionId { get; }
        public string EpisodeId { get; }
        public string CharterVersionId { get; }
        public string PlannerId { get; }
        public string ScoutId => PlannerId;
        public string MandateId { get; }
        public string EvidenceAuthorityId { get; }
        public string DeskId { get; }
        public string ObjectiveId { get; }
        public string PassageWitnessId { get; }
        public int StageX { get; }
        public int StageY { get; }
        public int ApproachX { get; }
        public int ApproachY { get; }
        public string RationRoot { get; }
        public string WaterRoot { get; }
        public string WaterVessel { get; }
        public string ReserveWaterRoot { get; }
        public string ReserveWaterVessel { get; }
        public RuleTime ValidFrom { get; }
        public RuleTime AuthorizationUntil { get; }
        public RuleQuantity IntendedFood => new RuleQuantity(2);
        public RuleQuantity ReserveFood => new RuleQuantity(2);
        public RuleQuantity WaterPerVessel => new RuleQuantity(4);
        public long NewCashLimitCopper => 0;
        public bool SupportProposedCarried => true;
        public bool SupportCommitted => false;
        public NextCharterAbortCondition AbortConditions => NextCharterAbortCondition.Required;
        public bool DistinctWaterSources => WaterRoot != ReserveWaterRoot && WaterVessel != ReserveWaterVessel;

        public NextCharterPlanTerms(string versionId, string episodeId, string charterVersionId, string plannerId, string mandateId,
            string evidenceAuthorityId, string deskId, string objectiveId, string passageWitnessId, int stageX, int stageY,
            int approachX, int approachY, string rationRoot, string waterRoot, string waterVessel, string reserveWaterRoot,
            string reserveWaterVessel, RuleTime validFrom, RuleTime authorizationUntil)
        {
            if (new[] { versionId, episodeId, charterVersionId, plannerId, mandateId, evidenceAuthorityId, deskId, objectiveId,
                passageWitnessId, rationRoot, waterRoot, waterVessel, reserveWaterRoot, reserveWaterVessel }.Any(x => !Validation.ValidId(x))
                || stageX < 0 || stageY < 0 || approachX < 0 || approachY < 0
                || Math.Abs((long)stageX - approachX) + Math.Abs((long)stageY - approachY) != 1 || authorizationUntil <= validFrom
                || rationRoot == waterRoot || rationRoot == reserveWaterRoot || plannerId == passageWitnessId)
                throw new ArgumentException("Invalid next-charter planning terms.");
            VersionId = versionId;
            EpisodeId = episodeId;
            CharterVersionId = charterVersionId;
            PlannerId = plannerId;
            MandateId = mandateId;
            EvidenceAuthorityId = evidenceAuthorityId;
            DeskId = deskId;
            ObjectiveId = objectiveId;
            PassageWitnessId = passageWitnessId;
            StageX = stageX;
            StageY = stageY;
            ApproachX = approachX;
            ApproachY = approachY;
            RationRoot = rationRoot;
            WaterRoot = waterRoot;
            WaterVessel = waterVessel;
            ReserveWaterRoot = reserveWaterRoot;
            ReserveWaterVessel = reserveWaterVessel;
            ValidFrom = validFrom;
            AuthorizationUntil = authorizationUntil;
        }

        public bool AuthorizedAt(RuleTime time) => ValidFrom <= time && time < AuthorizationUntil;
        public string BindingKey => string.Join("|", VersionId, EpisodeId, CharterVersionId, PlannerId, MandateId,
            EvidenceAuthorityId, DeskId, ObjectiveId, PassageWitnessId, RationRoot, WaterRoot, WaterVessel,
            ReserveWaterRoot, ReserveWaterVessel, ValidFrom, AuthorizationUntil,
            StageX.ToString(CultureInfo.InvariantCulture), StageY.ToString(CultureInfo.InvariantCulture),
            ApproachX.ToString(CultureInfo.InvariantCulture), ApproachY.ToString(CultureInfo.InvariantCulture),
            IntendedFood, ReserveFood, WaterPerVessel, AbortConditions, "walk-out-and-back", "new-cash-0");
    }

    public sealed class NextCharterStockObservation
    {
        public string LotId { get; }
        public string OwnerId { get; }
        public string CustodianId { get; }
        public string LocationId { get; }
        public RuleQuantity PhysicalAmount { get; }
        public RuleQuantity UnreservedAmount { get; }
        public bool UseAuthorized { get; }
        public bool CorrectCustody { get; }
        public bool Carried { get; }
        public bool Suitable { get; }
        public bool Accessible { get; }
        public bool Ready { get; }
        public bool Eligible => UseAuthorized && CorrectCustody && Carried && Suitable;

        public NextCharterStockObservation(string lotId, string ownerId, string custodianId, string locationId,
            RuleQuantity physicalAmount, RuleQuantity unreservedAmount, bool useAuthorized, bool correctCustody,
            bool carried, bool suitable, bool accessible, bool ready)
        {
            if (new[] { lotId, ownerId, custodianId, locationId }.Any(x => !Validation.ValidId(x))
                || unreservedAmount > physicalAmount || ready && (!carried || !accessible))
                throw new ArgumentException("Invalid next-charter stock observation.");
            LotId = lotId;
            OwnerId = ownerId;
            CustodianId = custodianId;
            LocationId = locationId;
            PhysicalAmount = physicalAmount;
            UnreservedAmount = unreservedAmount;
            UseAuthorized = useAuthorized;
            CorrectCustody = correctCustody;
            Carried = carried;
            Suitable = suitable;
            Accessible = accessible;
            Ready = ready;
        }
    }

    public sealed class NextCharterSupplyObservation
    {
        public string RootId { get; }
        public string VesselId { get; }
        public RuleQuantity? VesselCapacity { get; }
        public string VesselOwnerId { get; }
        public string VesselCustodianId { get; }
        public string VesselLocationId { get; }
        public RuleQuantity Required { get; }
        public IReadOnlyList<NextCharterStockObservation> Lots { get; }
        public RuleQuantity EligibleAvailable => RuleQuantity.Sum(Lots.Where(x => x.Eligible).Select(x => x.UnreservedAmount));
        public RuleQuantity AccessibleAvailable => RuleQuantity.Sum(Lots.Where(x => x.Eligible && x.Accessible).Select(x => x.UnreservedAmount));
        public RuleQuantity ReadyAvailable => RuleQuantity.Sum(Lots.Where(x => x.Eligible && x.Ready).Select(x => x.UnreservedAmount));
        public RuleQuantity Deficit => EligibleAvailable >= Required ? default : Required - EligibleAvailable;
        public bool RequiresPreparation => ReadyAvailable < Required;

        public NextCharterSupplyObservation(string rootId, string vesselId, RuleQuantity? vesselCapacity, string vesselOwnerId,
            string vesselCustodianId, string vesselLocationId, RuleQuantity required, IEnumerable<NextCharterStockObservation> lots)
        {
            if (!Validation.ValidId(rootId) || vesselId == null || required == default
                || (vesselId != "") != vesselCapacity.HasValue
                || vesselCapacity.HasValue && (!Validation.ValidId(vesselId)
                    || new[] { vesselOwnerId, vesselCustodianId, vesselLocationId }.Any(x => !Validation.ValidId(x)))
                || vesselId == "" && (vesselOwnerId != "" || vesselCustodianId != "" || vesselLocationId != ""))
                throw new ArgumentException("Invalid next-charter supply observation.");
            RootId = rootId;
            VesselId = vesselId;
            VesselCapacity = vesselCapacity;
            VesselOwnerId = vesselOwnerId;
            VesselCustodianId = vesselCustodianId;
            VesselLocationId = vesselLocationId;
            Required = required;
            Lots = Array.AsReadOnly(ExpeditionEpisodeCloseRecord.Freeze(lots, 128, x => x.LotId)
                .OrderBy(x => x.LotId, StringComparer.Ordinal).ToArray());
            if (!Lots.Any(x => x.LotId == rootId)) throw new ArgumentException("Missing observed supply root.");
        }
    }

    public sealed class NextCharterPlanObservation
    {
        public RuleTime At { get; }
        public long Revision { get; }
        public bool Walkable { get; }
        public bool Occupied { get; }
        public bool PathReserved { get; }
        public bool TacticalTransition { get; }
        public bool? ApproachAccess { get; }
        public bool ScoutCapable { get; }
        public bool ScoutAtStage { get; }
        public RuleQuantity? ActualPounds { get; }
        public RuleQuantity? ActualLoad { get; }
        public bool? CanCarry { get; }
        public bool? Burdened { get; }
        public int? Pressure { get; }
        public int? Strain { get; }
        public bool? RestDebt { get; }
        public bool WiderObligationsResolved => false;
        public bool HazardSafetyEstablished => false;
        public bool CharterAccepted => false;
        public bool DeparturePermitted => false;
        public bool AccessibilityCheckPerformed => false;
        public IReadOnlyList<NextCharterSupplyObservation> Supplies { get; }

        public NextCharterPlanObservation(RuleTime at, long revision, bool walkable, bool occupied, bool pathReserved,
            bool tacticalTransition, bool? approachAccess, bool scoutCapable, bool scoutAtStage, RuleQuantity? actualPounds,
            RuleQuantity? actualLoad, bool? canCarry, bool? burdened, int? pressure, int? strain, bool? restDebt,
            IEnumerable<NextCharterSupplyObservation> supplies)
        {
            if (revision < 0 || pressure < 0 || pressure > 6 || strain < 0 || strain > 6)
                throw new ArgumentException("Invalid next-charter observation.");
            At = at;
            Revision = revision;
            Walkable = walkable;
            Occupied = occupied;
            PathReserved = pathReserved;
            TacticalTransition = tacticalTransition;
            ApproachAccess = approachAccess;
            ScoutCapable = scoutCapable;
            ScoutAtStage = scoutAtStage;
            ActualPounds = actualPounds;
            ActualLoad = actualLoad;
            CanCarry = canCarry;
            Burdened = burdened;
            Pressure = pressure;
            Strain = strain;
            RestDebt = restDebt;
            Supplies = Array.AsReadOnly(ExpeditionEpisodeCloseRecord.Freeze(supplies, 3, x => x.RootId).ToArray());
            if (Supplies.Count != 3) throw new ArgumentException("Incomplete planning support observations.");
        }

        public bool Matches(NextCharterPlanTerms terms)
            => Supplies[0].RootId == terms.RationRoot && Supplies[0].VesselId == ""
                && Supplies[0].Required == terms.IntendedFood + terms.ReserveFood
                && Supplies[1].RootId == terms.WaterRoot && Supplies[1].VesselId == terms.WaterVessel
                && Supplies[1].Required == terms.WaterPerVessel
                && Supplies[2].RootId == terms.ReserveWaterRoot && Supplies[2].VesselId == terms.ReserveWaterVessel
                && Supplies[2].Required == terms.WaterPerVessel;
    }

    public sealed class NextCharterPlanRecord
    {
        public const int RequiredSeconds = 3600;
        public string Id { get; }
        public string WorkerId => Terms.PlannerId;
        public NextCharterPlanTerms Terms { get; }
        public long PriorCloseRevision { get; }
        public long PassageRevision { get; }
        public long StartRevision { get; }
        public long UpdatedRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }
        public NextCharterPlanStatus Status { get; }
        public string Reason { get; }
        public NextCharterPlanObservation Report { get; }
        public bool Open => Status == NextCharterPlanStatus.Working || Status == NextCharterPlanStatus.Paused
            || Status == NextCharterPlanStatus.PendingCompletion;

        public NextCharterPlanRecord(string id, NextCharterPlanTerms terms, long priorCloseRevision, long passageRevision,
            long startRevision, long updatedRevision, RuleTime startedAt, RuleTime updatedAt, RuleTime labor,
            NextCharterPlanStatus status, string reason, NextCharterPlanObservation report = null)
        {
            var required = new RuleTime(RequiredSeconds);
            if (!Validation.ValidId(id) || terms == null || !terms.DistinctWaterSources || !Validation.ValidId(reason)
                || passageRevision < 1 || passageRevision >= priorCloseRevision || priorCloseRevision >= startRevision
                || updatedRevision < startRevision || updatedAt < startedAt || !terms.AuthorizedAt(startedAt) || labor > required
                || !Enum.IsDefined(typeof(NextCharterPlanStatus), status)
                || (status == NextCharterPlanStatus.CompletedConditional) != (report != null)
                || (status == NextCharterPlanStatus.Working || status == NextCharterPlanStatus.Paused) && labor == required
                || (status == NextCharterPlanStatus.CompletedConditional || status == NextCharterPlanStatus.PendingCompletion) && labor != required
                || status == NextCharterPlanStatus.Expired && updatedAt != terms.AuthorizationUntil
                || report != null && (report.At != updatedAt || report.Revision != updatedRevision
                    || !terms.AuthorizedAt(updatedAt) || !report.Matches(terms)))
                throw new ArgumentException("Invalid next-charter planning record.");
            Id = id;
            Terms = terms;
            PriorCloseRevision = priorCloseRevision;
            PassageRevision = passageRevision;
            StartRevision = startRevision;
            UpdatedRevision = updatedRevision;
            StartedAt = startedAt;
            UpdatedAt = updatedAt;
            Work = new ActiveWorkProgress(new[] { required });
            if (labor != default) Work = Work.Credit(labor);
            Status = status;
            Reason = reason;
            Report = report;
        }

        public NextCharterPlanRecord With(Snapshot state, RuleTime labor, NextCharterPlanStatus status, string reason,
            NextCharterPlanObservation report = null)
            => new NextCharterPlanRecord(Id, Terms, PriorCloseRevision, PassageRevision, StartRevision, state.Revision + 1,
                StartedAt, state.RuleClock, labor, status, reason, report);
    }

    public static class NextCharterPlanValidation
    {
        public const int MaxAttempts = 8;

        public static void Validate(Snapshot state)
        {
            var jobs = state.NextCharterPlans;
            if (jobs == null || jobs.Length > MaxAttempts || jobs.Any(x => x == null)
                || jobs.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != jobs.Length
                || jobs.Count(x => x.Open || x.Report != null) > 1
                || state.SchemaVersion != Snapshot.NextCharterPlanSchema && jobs.Length != 0
                || state.SchemaVersion == Snapshot.NextCharterPlanSchema && !state.TestOnly)
                throw new ArgumentException("Invalid next-charter planning history.");
            foreach (var job in jobs) ValidateJob(state, job);
        }

        private static void ValidateJob(Snapshot state, NextCharterPlanRecord job)
        {
            var close = state.ExpeditionEpisodeClose;
            var terms = job.Terms;
            var witness = close?.Members.SingleOrDefault(x => x.ActorId == terms.PassageWitnessId);
            var start = state.Receipts.SingleOrDefault(x => x.Revision == job.StartRevision);
            var update = state.Receipts.SingleOrDefault(x => x.Revision == job.UpdatedRevision);
            var passage = state.Receipts.SingleOrDefault(x => x.Revision == job.PassageRevision);
            if (close == null || close.CloseRevision != job.PriorCloseRevision || close.EpisodeId != terms.EpisodeId
                || close.CharterVersionId != terms.CharterVersionId || close.ClosedAt > job.StartedAt
                || witness == null || job.PassageRevision > close.SourceRevision
                || start == null || update == null || passage == null || job.UpdatedAt > state.RuleClock
                || job.Open && !terms.AuthorizedAt(state.RuleClock) || state.Work.Reservations.Any(x => x.JobId == job.Id))
                throw new ArgumentException("Invalid next-charter planning provenance.");
            var walked = CommandHistory.Read(passage);
            if (walked.Kind != CommandKind.BeginWorldStep || walked.Actor != terms.PassageWitnessId || walked.Target != "walk"
                || walked.X != terms.ApproachX - terms.StageX || walked.Y != terms.ApproachY - terms.StageY)
                throw new ArgumentException("Invalid prior passage evidence.");
            var admitted = CommandHistory.Read(start);
            if (admitted.Kind != CommandKind.StartNextCharterPlan || admitted.Actor != job.WorkerId || admitted.Target != terms.VersionId
                || job.Id != "next-charter.plan." + job.StartRevision.ToString(CultureInfo.InvariantCulture))
                throw new ArgumentException("Invalid next-charter plan admission receipt.");
            var intervals = state.Work.WorkerIntervals.Where(x => x.JobId == job.Id).ToArray();
            if (intervals.Any(x => x.WorkerId != job.WorkerId || x.Start < job.StartedAt || x.Start > job.UpdatedAt
                || x.End >= terms.AuthorizationUntil || job.Status != NextCharterPlanStatus.Working && x.End > job.UpdatedAt)
                || intervals.Count(x => x.End > state.RuleClock) != (job.Status == NextCharterPlanStatus.Working ? 1 : 0))
                throw new ArgumentException("Invalid next-charter work intervals.");
            foreach (var interval in intervals) ValidateBookingReceipt(state, job, interval);
            var active = intervals.SingleOrDefault(x => x.End > state.RuleClock);
            if (active != null && Seconds(active.End) - Seconds(state.RuleClock) != Seconds(job.Work.Remaining))
                throw new ArgumentException("Invalid next-charter remaining booking.");
            var elapsed = RuleQuantity.Sum(intervals.Select(x => Seconds(x.End < state.RuleClock ? x.End : state.RuleClock) - Seconds(x.Start)));
            if (elapsed != Seconds(job.Work.Labor)) throw new ArgumentException("Next-charter labor differs from its ledger.");
            if (job.Report != null && intervals.Max(x => x.End) < job.UpdatedAt) {
                var command = CommandHistory.Read(update);
                if (command.Kind != CommandKind.FinalizeNextCharterPlan || command.Actor != job.WorkerId || command.Target != job.Id)
                    throw new ArgumentException("Delayed next-charter report lacks a finalization receipt.");
            }
        }

        private static void ValidateBookingReceipt(Snapshot state, NextCharterPlanRecord job, WorkerInterval interval)
        {
            string prefix = job.Id + ".labor.";
            if (!interval.Id.StartsWith(prefix, StringComparison.Ordinal)
                || !long.TryParse(interval.Id.Substring(prefix.Length), NumberStyles.None, CultureInfo.InvariantCulture, out long revision)
                || revision < job.StartRevision || revision > job.UpdatedRevision)
                throw new ArgumentException("Invalid next-charter planning booking identity.");
            if (revision == job.StartRevision) {
                if (interval.Start != job.StartedAt) throw new ArgumentException("Invalid initial next-charter booking start.");
                return;
            }
            var receipt = state.Receipts.SingleOrDefault(x => x.Revision == revision);
            if (receipt == null) throw new ArgumentException("Next-charter booking lacks a resume receipt.");
            var command = CommandHistory.Read(receipt);
            if (command.Kind != CommandKind.ResumeNextCharterPlan || command.Actor != job.WorkerId || command.Target != job.Id)
                throw new ArgumentException("Invalid next-charter planning resume receipt.");
        }

        private static RuleQuantity Seconds(RuleTime value) => new RuleQuantity(value.Numerator, value.Denominator);
    }
}
