using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum RepairWorkStatus { Working, Paused, AwaitingCheck, Success, Failure, Cancelled }
    public sealed class RepairWorkRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public string TargetId { get; }
        public string ToolkitId { get; }
        public string MaterialsId { get; }
        public RepairWorkStatus Status { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public bool Open => Status == RepairWorkStatus.Working || Status == RepairWorkStatus.Paused || Status == RepairWorkStatus.AwaitingCheck;
        public RepairWorkRecord(string id, string worker, string target, string toolkit, string materials, RepairWorkStatus status,
            RuleTime start, RuleTime updated, ActiveWorkProgress work, int first = 0, int second = 0, int natural = 0)
        {
            if (new[] { id, worker, target, toolkit, materials }.Any(x => !Validation.ValidId(x)) || target == toolkit
                || !Enum.IsDefined(typeof(RepairWorkStatus), status) || work == null || updated < start || first < 0 || first > 20 || second < 0 || second > 20 || natural < 0 || natural > 20)
                throw new ArgumentException("Invalid repair work.");
            bool resolved = status == RepairWorkStatus.Success || status == RepairWorkStatus.Failure;
            if (status != RepairWorkStatus.Cancelled && (resolved || status == RepairWorkStatus.AwaitingCheck) != work.Complete
                || (resolved ? first == 0 || natural == 0 || natural != first && natural != second : first != 0 || second != 0 || natural != 0)) throw new ArgumentException("Invalid repair result.");
            Id = id; WorkerId = worker; TargetId = target; ToolkitId = toolkit; MaterialsId = materials; Status = status;
            StartedAt = start; UpdatedAt = updated; Work = work; First = first; Second = second; Natural = natural;
        }
    }
    public static class RepairWorkValidation
    {
        public const int MaxRecords = 32;
        public static void Validate(Snapshot s)
        {
            if (s.RepairWork == null || s.RepairWork.Length > MaxRecords || s.RepairWork.Any(x => x == null) || s.SchemaVersion < Snapshot.RepairWorkSchema && s.RepairWork.Length != 0
                || s.RepairWork.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.RepairWork.Length) throw new ArgumentException("Invalid repair collection.");
            if (s.RepairWork.Where(x => x.Open).GroupBy(x => x.TargetId).Any(x => x.Count() > 1)) throw new ArgumentException("Overlapping target repair claims.");
            foreach (var job in s.RepairWork) {
                if (!s.Actors.Any(x => x.Id == job.WorkerId) || !s.Structures.Any(x => x.Id == job.TargetId) || !s.Structures.Any(x => x.Id == job.ToolkitId)
                    || !s.Work.Lots.Any(x => x.Id == job.MaterialsId) || job.UpdatedAt > s.RuleClock) throw new ArgumentException("Invalid repair references.");
                var elapsed = new RuleQuantity(job.UpdatedAt.Numerator, job.UpdatedAt.Denominator) - new RuleQuantity(job.StartedAt.Numerator, job.StartedAt.Denominator);
                if (new RuleQuantity(job.Work.Labor.Numerator, job.Work.Labor.Denominator) > elapsed) throw new ArgumentException("Repair labor exceeds elapsed time.");
            }
        }
    }
}
