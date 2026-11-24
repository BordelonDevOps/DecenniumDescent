using System;
using System.Collections.Generic;

namespace Decennium.Foundation
{
    /// <summary>Trusted native guard identity. Never a player diagnostic or persisted field.
    /// Coordinates identify the unchanged guard in the accepted 67f3d201b contract baseline.</summary>
    public sealed class NativeCommandConstraintV1
    {
        public string NativeCode { get; }
        public string SourcePath { get; }
        public int SourceLine { get; }
        public NativeCommandConstraintV1(string nativeCode, string sourcePath, int sourceLine)
        {
            if (string.IsNullOrEmpty(nativeCode) || string.IsNullOrEmpty(sourcePath) || sourceLine < 1)
                throw new ArgumentException("A native constraint needs its exact originating guard.");
            NativeCode = nativeCode; SourcePath = sourcePath; SourceLine = sourceLine;
        }
    }

    public enum NativeAssessmentStatusV1
    {
        Available, Unavailable, AlreadyCommitted, Rejected, Unsupported,
        StaleObservation, VerificationUnavailable, ProjectionUnavailable
    }

    /// <summary>Immutable native result for the trusted host. Public player projections must
    /// apply their registered per-field and per-origin disclosure rules.</summary>
    public sealed class NativeCommandAssessmentV1
    {
        public NativeAssessmentStatusV1 Status { get; }
        public bool Supported => Status != NativeAssessmentStatusV1.Unsupported;
        public bool Admissible => Status == NativeAssessmentStatusV1.Available;
        public long ObservedRevision { get; }
        public long? MatchingReceiptRevision { get; }
        public bool? InitialEligibility { get; }
        public bool? CommitFeasibility { get; }
        public NativeCommandConstraintV1 Constraint { get; }
        public IReadOnlyList<int> ProhibitedCallAttempts { get; }

        public NativeCommandAssessmentV1(long revision, bool initialEligibility, bool? commitFeasibility,
            NativeCommandConstraintV1 constraint = null)
            : this(initialEligibility && commitFeasibility != false ? NativeAssessmentStatusV1.Available
                : NativeAssessmentStatusV1.Unavailable, revision, constraint, null, initialEligibility, commitFeasibility)
        {
            if (Admissible && constraint != null || !Admissible && constraint == null)
                throw new ArgumentException("Native eligibility and its constraint disagree.");
        }

        internal NativeCommandAssessmentV1(NativeAssessmentStatusV1 status, long revision,
            NativeCommandConstraintV1 constraint = null, long? matchingReceiptRevision = null,
            bool? initialEligibility = null, bool? commitFeasibility = null, int[] attempts = null)
        {
            if (revision < 0) throw new ArgumentOutOfRangeException(nameof(revision));
            Status = status; ObservedRevision = revision; Constraint = constraint;
            MatchingReceiptRevision = matchingReceiptRevision; InitialEligibility = initialEligibility;
            CommitFeasibility = commitFeasibility;
            ProhibitedCallAttempts = Array.AsReadOnly((int[])(attempts ?? new int[NativeReadInspectionV1.OperationCount]).Clone());
        }

        internal NativeCommandAssessmentV1 WithAudit(int[] attempts)
            => new NativeCommandAssessmentV1(Status, ObservedRevision, Constraint, MatchingReceiptRevision,
                InitialEligibility, CommitFeasibility, attempts);
    }

    public interface ICommandAssessmentFactsPolicyV1
    {
        bool SupportsAssessment(CommandKind kind);
        bool RequiresVerifiedAssessment(CommandKind kind);
        NativeCommandAssessmentV1 AssessFacts(NativeReadContextV1 readContext, Snapshot current,
            Authority authority, Command command);
    }

    public interface IVerifiedCommandAssessmentV1
    {
        NativeCommandAssessmentV1 AssessFacts(VerifiedSimulationOrigin origin, NativeReadContextV1 readContext,
            Snapshot current, Authority authority, Command command);
    }

    public sealed partial class Simulation
    {
        /// <summary>Trusted native assessment. Does not expose the owning read capability.
        /// The connected host separately applies its endpoint, exposure and target boundaries.</summary>
        public NativeCommandAssessmentV1 AssessCommandFactsV1(Authority authority, Command command,
            long expectedObservationRevision)
        {
            RequireOwnerEntryV1();
            long revision = state.Revision;
            using (var inspection = NativeReadInspectionV1.Enter()) {
                NativeCommandAssessmentV1 Result(NativeAssessmentStatusV1 status,
                    NativeCommandConstraintV1 constraint = null, long? receipt = null)
                    => new NativeCommandAssessmentV1(inspection.HasViolation ? NativeAssessmentStatusV1.ProjectionUnavailable : status,
                        revision, inspection.HasViolation ? null : constraint, inspection.HasViolation ? null : receipt,
                        attempts: inspection.Attempts());
                try {
                    if (!(policy is ICommandAssessmentFactsPolicyV1 assessor) || command == null
                        || !assessor.SupportsAssessment(command.Kind)) return Result(NativeAssessmentStatusV1.Unsupported);
                    var authorityFailure = AssessCommandAndAuthorityV1(authority, command);
                    if (authorityFailure != null) return Result(NativeAssessmentStatusV1.Rejected, authorityFailure);
                    if (expectedObservationRevision != revision) return Result(NativeAssessmentStatusV1.StaleObservation);
                    var failure = AssessCommandAfterAuthorityV1(authority, command, out var previous);
                    if (failure != null) return Result(NativeAssessmentStatusV1.Rejected, failure);
                    if (previous != null) return Result(NativeAssessmentStatusV1.AlreadyCommitted, receipt: previous.Revision);
                    var captured = state.Copy();
                    var context = CurrentReadContextV1(captured);
                    if (context == null) return Result(NativeAssessmentStatusV1.ProjectionUnavailable);
                    NativeCommandAssessmentV1 assessed;
                    if (assessor.RequiresVerifiedAssessment(command.Kind)) {
                        if (verificationOrigin == null || !(checkpoint is IVerifiedCommandAssessmentV1 verified))
                            return Result(NativeAssessmentStatusV1.VerificationUnavailable);
                        assessed = verified.AssessFacts(verificationOrigin, context, captured, authority, command);
                    } else assessed = assessor.AssessFacts(context, captured, authority, command);
                    if (inspection.HasViolation || assessed == null || assessed.ObservedRevision != revision
                        || !context.IsBoundTo(captured)) return Result(NativeAssessmentStatusV1.ProjectionUnavailable);
                    return assessed.WithAudit(inspection.Attempts());
                }
                catch (Exception)
                { return Result(NativeAssessmentStatusV1.ProjectionUnavailable); }
            }
        }
    }
}
