using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ExpeditionWorkProcedure { ToolRepair = 1, FishingTrapRetrieval = 2, MiningExtraction = 3 }
    public enum ExpeditionAssignmentStatus { Travelling = 1, Ready = 2, Started = 3, Cancelled = 4 }

    /// <summary>Explicit assignment intent. The selected fixture derives the physical work site;
    /// this payload supplies neither site authority nor procedure qualifications.</summary>
    public sealed class ExpeditionAssignmentRequest
    {
        public ExpeditionWorkProcedure Procedure { get; }
        public string TargetId { get; }
        public string DestinationId { get; }
        public MiningSelectionRequest MiningSelection { get; }
        internal string Fingerprint => ((int)Procedure).ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + TargetId + "|" + DestinationId;
        public ExpeditionAssignmentRequest(ExpeditionWorkProcedure procedure, string targetId, string destinationId = "",
            MiningSelectionRequest miningSelection = null)
        {
            if (!Enum.IsDefined(typeof(ExpeditionWorkProcedure), procedure) || !Validation.ValidId(targetId)
                || destinationId == null || destinationId != "" && !Validation.ValidId(destinationId)
                || procedure == ExpeditionWorkProcedure.ToolRepair && destinationId != ""
                || procedure == ExpeditionWorkProcedure.FishingTrapRetrieval && destinationId == ""
                || procedure == ExpeditionWorkProcedure.MiningExtraction && (destinationId != "" || miningSelection == null)
                || procedure != ExpeditionWorkProcedure.MiningExtraction && miningSelection != null)
                throw new ArgumentException("Invalid expedition work assignment request.");
            Procedure = procedure; TargetId = targetId; DestinationId = destinationId; MiningSelection = miningSelection;
        }
    }

    public sealed class ExpeditionWorkAssignmentRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public ExpeditionWorkProcedure Procedure { get; }
        public string TargetId { get; }
        public string DestinationId { get; }
        public int SiteX { get; }
        public int SiteY { get; }
        public RuleTime AssignedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ExpeditionAssignmentStatus Status { get; }
        public string WorkId { get; }
        public MiningSelectionRequest MiningSelection { get; }
        public bool Open => Status == ExpeditionAssignmentStatus.Travelling || Status == ExpeditionAssignmentStatus.Ready;

        public ExpeditionWorkAssignmentRecord(string id, string workerId, ExpeditionWorkProcedure procedure, string targetId,
            string destinationId, int siteX, int siteY, RuleTime assignedAt, RuleTime updatedAt,
            ExpeditionAssignmentStatus status, string workId = "", MiningSelectionRequest miningSelection = null)
        {
            foreach (string value in new[] { id, workerId, targetId })
                if (!Validation.ValidId(value)) throw new ArgumentException("Invalid expedition assignment identity.");
            if (!Enum.IsDefined(typeof(ExpeditionWorkProcedure), procedure)
                || !Enum.IsDefined(typeof(ExpeditionAssignmentStatus), status)
                || destinationId == null || destinationId != "" && !Validation.ValidId(destinationId)
                || procedure == ExpeditionWorkProcedure.ToolRepair && destinationId != ""
                || procedure == ExpeditionWorkProcedure.FishingTrapRetrieval && destinationId == ""
                || procedure == ExpeditionWorkProcedure.MiningExtraction && (destinationId != "" || miningSelection == null)
                || procedure != ExpeditionWorkProcedure.MiningExtraction && miningSelection != null
                || siteX < 0 || siteY < 0 || assignedAt > updatedAt
                || workId == null || workId != "" && !Validation.ValidId(workId)
                || (status == ExpeditionAssignmentStatus.Started) != (workId != ""))
                throw new ArgumentException("Invalid expedition assignment state.");
            Id = id; WorkerId = workerId; Procedure = procedure; TargetId = targetId; DestinationId = destinationId;
            SiteX = siteX; SiteY = siteY; AssignedAt = assignedAt; UpdatedAt = updatedAt; Status = status; WorkId = workId;
            MiningSelection = miningSelection;
        }

        public ExpeditionWorkAssignmentRecord With(ExpeditionAssignmentStatus status, RuleTime at, string workId = "")
            => new ExpeditionWorkAssignmentRecord(Id, WorkerId, Procedure, TargetId, DestinationId, SiteX, SiteY,
                AssignedAt, at, status, workId, MiningSelection);
    }

    public static class ExpeditionAssignmentValidation
    {
        public const int MaxAssignments = 64;
        public static bool HasCapacity(Snapshot s)
            => s != null && s.ExpeditionAssignments != null && s.ExpeditionAssignments.Length < MaxAssignments;
        public static void Validate(Snapshot s)
        {
            if (s.ExpeditionAssignments == null || s.ExpeditionAssignments.Length > MaxAssignments
                || s.ExpeditionAssignments.Any(x => x == null)) throw new ArgumentException("Invalid expedition assignments.");
            if (s.SchemaVersion < Snapshot.ExpeditionAssignmentSchema && s.ExpeditionAssignments.Length != 0)
                throw new ArgumentException("Expedition assignments require their snapshot schema.");
            if (s.SchemaVersion < Snapshot.MiningExpeditionAssignmentSchema
                && s.ExpeditionAssignments.Any(x => x.Procedure == ExpeditionWorkProcedure.MiningExtraction))
                throw new ArgumentException("Mining assignments require schema47.");
            if (s.ExpeditionAssignments.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionAssignments.Length
                || s.ExpeditionAssignments.Where(x => x.Open).Select(x => x.WorkerId).Distinct(StringComparer.Ordinal).Count()
                    != s.ExpeditionAssignments.Count(x => x.Open))
                throw new ArgumentException("Duplicate or overlapping expedition assignments.");
            foreach (var assignment in s.ExpeditionAssignments)
            {
                if (!s.Actors.Any(x => x.Id == assignment.WorkerId) || assignment.AssignedAt > s.RuleClock
                    || assignment.UpdatedAt > s.RuleClock) throw new ArgumentException("Unknown worker or future expedition assignment time.");
                if (assignment.Status == ExpeditionAssignmentStatus.Ready)
                {
                    var worker = s.Actors.Single(x => x.Id == assignment.WorkerId);
                    if (worker.X != assignment.SiteX || worker.Y != assignment.SiteY
                        || s.WorldTraversals.Any(x => x.ActorId == worker.Id))
                        throw new ArgumentException("Ready expedition assignment is not at its work site.");
                }
                if (assignment.Procedure == ExpeditionWorkProcedure.MiningExtraction) {
                    var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==assignment.TargetId)
                        ??throw new ArgumentException("Mining assignment references an unknown deposit.");
                    var selection=assignment.MiningSelection;
                    if(selection.DepositVersionId!=deposit.VersionId||assignment.SiteX!=deposit.SiteX||assignment.SiteY!=deposit.SiteY
                        ||selection.CategoryIds.Any(id=>!s.MiningCategories.Any(x=>x.Id==id&&x.DepositId==deposit.Id&&x.Accessible)))
                        throw new ArgumentException("Mining assignment does not match its exposed deposit and selected categories.");
                }
                if (assignment.Status == ExpeditionAssignmentStatus.Started)
                {
                    bool linked = assignment.Procedure == ExpeditionWorkProcedure.ToolRepair
                        ? s.RepairWork.Any(x => x.Id == assignment.WorkId && x.WorkerId == assignment.WorkerId && x.TargetId == assignment.TargetId)
                        : assignment.Procedure == ExpeditionWorkProcedure.FishingTrapRetrieval
                            ? s.FishingTrapRetrievals.Any(x => x.Id == assignment.WorkId && x.WorkerId == assignment.WorkerId
                                && x.TrapId == assignment.TargetId && x.DestinationId == assignment.DestinationId)
                            : s.MiningAttempts.Any(x => x.Id == assignment.WorkId && x.WorkerId == assignment.WorkerId
                                && x.DepositId == assignment.TargetId && x.DepositVersionId == assignment.MiningSelection.DepositVersionId
                                && x.SelectedCategoryIds.SequenceEqual(assignment.MiningSelection.CategoryIds)
                                && x.Ability == assignment.MiningSelection.Ability && x.Hurried == assignment.MiningSelection.Hurried
                                && x.FailureVictimPreference == assignment.MiningSelection.FailureVictimPreference
                                && x.CriticalRecoveryPreference == assignment.MiningSelection.CriticalRecoveryPreference);
                    if (!linked) throw new ArgumentException("Started expedition assignment has no matching procedure record.");
                }
            }
        }
    }
}
