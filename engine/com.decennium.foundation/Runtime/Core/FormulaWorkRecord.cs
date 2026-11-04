using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum FormulaWorkKind { Research, Copy }
    public enum FormulaWorkStatus { Working, Paused, Success, Failure, Cancelled, AwaitingCheck }
    /// <summary>Persistent knowledge-work facts. Definition, access, retry and cost authority are
    /// supplied by the command policy, never inferred from these identities or a successful roll.</summary>
    public sealed class FormulaWorkRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public string RecipeId { get; }
        public string EvidenceId { get; }
        public string MethodId { get; }
        public string PreviousAttemptId { get; }
        public FormulaWorkKind Kind { get; }
        public FormulaWorkStatus Status { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public FormulaWorkRecord(string id, string workerId, string recipeId, string evidenceId, string methodId,
            FormulaWorkKind kind, FormulaWorkStatus status, RuleTime startedAt, RuleTime updatedAt,
            ActiveWorkProgress work, int first = 0, int second = 0, int natural = 0, string previousAttemptId = "")
        {
            if (new[] { id, workerId, recipeId, evidenceId, methodId }.Any(x => !Validation.ValidId(x))
                || !Enum.IsDefined(typeof(FormulaWorkKind), kind) || !Enum.IsDefined(typeof(FormulaWorkStatus), status)
                || previousAttemptId == null || (previousAttemptId != "" && !Validation.ValidId(previousAttemptId))
                || work == null || updatedAt < startedAt || first < 0 || first > 20 || second < 0 || second > 20 || natural < 0 || natural > 20)
                throw new ArgumentException("Invalid formula work record.");
            bool resolved = status == FormulaWorkStatus.Success || status == FormulaWorkStatus.Failure;
            if ((status != FormulaWorkStatus.Cancelled && (resolved || status == FormulaWorkStatus.AwaitingCheck) != work.Complete) || (kind == FormulaWorkKind.Copy && (status == FormulaWorkStatus.Failure || status == FormulaWorkStatus.AwaitingCheck))
                || (resolved && kind == FormulaWorkKind.Research ? first == 0 || natural == 0 || (natural != first && natural != second) : first != 0 || second != 0 || natural != 0))
                throw new ArgumentException("Invalid formula work result.");
            Id = id; WorkerId = workerId; RecipeId = recipeId; EvidenceId = evidenceId; MethodId = methodId;
            PreviousAttemptId = previousAttemptId;
            Kind = kind; Status = status; StartedAt = startedAt; UpdatedAt = updatedAt; Work = work;
            First = first; Second = second; Natural = natural;
        }
    }
    public static class FormulaWorkValidation
    {
        public const int MaxRecords = 32;
        public static void Validate(Snapshot s)
        {
            if (s.FormulaWork == null || s.FormulaWork.Length > MaxRecords || s.FormulaWork.Any(x => x == null)
                || (s.SchemaVersion < Snapshot.FormulaWorkSchema && s.FormulaWork.Length != 0)
                || s.FormulaWork.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.FormulaWork.Length)
                throw new ArgumentException("Invalid formula work collection or schema.");
            foreach (var job in s.FormulaWork) {
                if (!s.Actors.Any(x => x.Id == job.WorkerId) || job.UpdatedAt > s.RuleClock)
                    throw new ArgumentException("Invalid formula worker or timestamp.");
                var elapsed = new RuleQuantity(job.UpdatedAt.Numerator, job.UpdatedAt.Denominator) - new RuleQuantity(job.StartedAt.Numerator, job.StartedAt.Denominator);
                if (new RuleQuantity(job.Work.Labor.Numerator, job.Work.Labor.Denominator) > elapsed)
                    throw new ArgumentException("Formula labor exceeds elapsed time.");
            }
        }
    }
}
