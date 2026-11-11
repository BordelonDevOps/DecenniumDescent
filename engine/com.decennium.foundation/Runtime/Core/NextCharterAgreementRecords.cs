using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    [Flags]
    public enum NextCharterOffice
    {
        Leader = 1, Quartermaster = 2, Routekeeper = 4, Surgeon = 8, ClaimantOfRecord = 16,
        All = Leader | Quartermaster | Routekeeper | Surgeon | ClaimantOfRecord
    }

    [Flags]
    public enum NextCharterPassageDirections { Outbound = 1, Return = 2, RoundTrip = Outbound | Return }

    public enum NextCharterAgreementStatus { Offered, AcceptedConditional, Withdrawn, Expired }

    public sealed class NextCharterAccessPermission
    {
        public const string WalkAndObserve = "ordinary-walking-accessibility-observation";
        public string VersionId { get; }
        public string EvidenceId { get; }
        public string IssuerId { get; }
        public string IssuerAuthorityId { get; }
        public string BeneficiaryId { get; }
        public int StageX { get; }
        public int StageY { get; }
        public int ApproachX { get; }
        public int ApproachY { get; }
        public NextCharterPassageDirections Directions { get; }
        public string MethodId { get; }
        public RuleTime ValidFrom { get; }
        public RuleTime ValidUntil { get; }
        public long ChargeCopper { get; }
        public string RestrictionsId { get; }

        public NextCharterAccessPermission(string versionId, string evidenceId, string issuerId, string issuerAuthorityId,
            string beneficiaryId, int stageX, int stageY, int approachX, int approachY, NextCharterPassageDirections directions,
            string methodId, RuleTime validFrom, RuleTime validUntil, long chargeCopper, string restrictionsId)
        {
            if (new[] { versionId, evidenceId, issuerId, issuerAuthorityId, beneficiaryId, methodId, restrictionsId }
                    .Any(x => !Validation.ValidId(x))
                || stageX < 0 || stageY < 0 || approachX < 0 || approachY < 0
                || Math.Abs((long)stageX - approachX) + Math.Abs((long)stageY - approachY) != 1
                || directions == 0 || (directions & ~NextCharterPassageDirections.RoundTrip) != 0
                || validUntil <= validFrom || chargeCopper < 0)
                throw new ArgumentException("Invalid next-charter access permission.");
            VersionId = versionId;
            EvidenceId = evidenceId;
            IssuerId = issuerId;
            IssuerAuthorityId = issuerAuthorityId;
            BeneficiaryId = beneficiaryId;
            StageX = stageX;
            StageY = stageY;
            ApproachX = approachX;
            ApproachY = approachY;
            Directions = directions;
            MethodId = methodId;
            ValidFrom = validFrom;
            ValidUntil = validUntil;
            ChargeCopper = chargeCopper;
            RestrictionsId = restrictionsId;
        }

        public bool Covers(NextCharterPlanTerms plan) => BeneficiaryId == plan.ScoutId
            && StageX == plan.StageX && StageY == plan.StageY && ApproachX == plan.ApproachX && ApproachY == plan.ApproachY
            && Directions == NextCharterPassageDirections.RoundTrip && MethodId == WalkAndObserve;

        public string BindingKey => string.Join("|", VersionId, EvidenceId, IssuerId, IssuerAuthorityId, BeneficiaryId,
            StageX.ToString(CultureInfo.InvariantCulture), StageY.ToString(CultureInfo.InvariantCulture),
            ApproachX.ToString(CultureInfo.InvariantCulture), ApproachY.ToString(CultureInfo.InvariantCulture),
            Directions, MethodId, ValidFrom, ValidUntil, ChargeCopper.ToString(CultureInfo.InvariantCulture), RestrictionsId);
    }

    public sealed class NextCharterAgreementTerms
    {
        public string OfferId { get; }
        public string CharterId { get; }
        public string CharterVersionId { get; }
        public string AssentAuthorityId { get; }
        public string RecordsAccessId { get; }
        public string ResourceUseAuthorityId { get; }
        public string ResourceOwnerId { get; }
        public NextCharterOffice SoloOffices { get; }
        public NextCharterPlanTerms PlanTerms { get; }
        public string ParticipantId => PlanTerms.PlannerId;
        public NextCharterAccessPermission AccessPermission { get; }
        public RuleTime ValidFrom { get; }
        public RuleTime ValidUntil { get; }
        public long NewCashLimitCopper => PlanTerms.NewCashLimitCopper;
        public bool ReservesDesignated => true;
        public bool ReservesExclusivelyCommitted => false;

        public NextCharterAgreementTerms(string offerId, string charterId, string charterVersionId, string assentAuthorityId,
            string recordsAccessId, string resourceUseAuthorityId, string resourceOwnerId, NextCharterOffice soloOffices,
            NextCharterPlanTerms planTerms, NextCharterAccessPermission accessPermission, RuleTime validFrom, RuleTime validUntil)
        {
            if (new[] { offerId, charterId, charterVersionId, assentAuthorityId, recordsAccessId, resourceUseAuthorityId,
                    resourceOwnerId }.Any(x => !Validation.ValidId(x))
                || planTerms == null || charterVersionId == planTerms.CharterVersionId || charterId == planTerms.EpisodeId
                || validUntil <= validFrom || (soloOffices & ~NextCharterOffice.All) != 0)
                throw new ArgumentException("Invalid prospective charter terms.");
            OfferId = offerId;
            CharterId = charterId;
            CharterVersionId = charterVersionId;
            AssentAuthorityId = assentAuthorityId;
            RecordsAccessId = recordsAccessId;
            ResourceUseAuthorityId = resourceUseAuthorityId;
            ResourceOwnerId = resourceOwnerId;
            SoloOffices = soloOffices;
            PlanTerms = planTerms;
            AccessPermission = accessPermission;
            ValidFrom = validFrom;
            ValidUntil = validUntil;
        }

        public bool InWindow(RuleTime at) => ValidFrom <= at && at < ValidUntil;

        public bool PermissionCoversWindow => AccessPermission != null && AccessPermission.Covers(PlanTerms)
            && AccessPermission.ValidFrom <= ValidFrom && ValidUntil <= AccessPermission.ValidUntil && AccessPermission.ChargeCopper == 0;

        public string BindingKey => string.Join("|", OfferId, CharterId, CharterVersionId, AssentAuthorityId, RecordsAccessId,
            ResourceUseAuthorityId, ResourceOwnerId, SoloOffices, PlanTerms.BindingKey, ValidFrom, ValidUntil, AccessPermission?.BindingKey);
    }

    public sealed class NextCharterWithdrawal
    {
        public string CommandId { get; }
        public long Revision { get; }
        public RuleTime At { get; }

        public NextCharterWithdrawal(string commandId, long revision, RuleTime at)
        {
            if (!Validation.ValidId(commandId) || revision < 1) throw new ArgumentException("Invalid charter withdrawal.");
            CommandId = commandId;
            Revision = revision;
            At = at;
        }
    }

    public sealed class NextCharterAgreementRecord
    {
        public NextCharterAgreementTerms Terms { get; }
        public string PlanId { get; }
        public long PlanReportRevision { get; }
        public long PriorCloseRevision { get; }
        public string CommandId { get; }
        public string ActorId => Terms.ParticipantId;
        public long SourceRevision => AcceptedRevision - 1;
        public long AcceptedRevision { get; }
        public RuleTime AcceptedAt => Observation.At;
        public NextCharterPlanObservation Observation { get; }
        public NextCharterWithdrawal Withdrawal { get; }

        public NextCharterAgreementRecord(NextCharterAgreementTerms terms, string planId, long planReportRevision,
            long priorCloseRevision, string commandId, long acceptedRevision, NextCharterPlanObservation observation,
            NextCharterWithdrawal withdrawal = null)
        {
            if (terms == null || terms.SoloOffices != NextCharterOffice.All || terms.ResourceOwnerId != terms.ParticipantId
                || !terms.PermissionCoversWindow || !terms.PlanTerms.DistinctWaterSources || !Validation.ValidId(planId)
                || !Validation.ValidId(commandId) || priorCloseRevision < 1 || planReportRevision <= priorCloseRevision
                || acceptedRevision <= planReportRevision || observation == null || observation.Revision != acceptedRevision - 1
                || !terms.InWindow(observation.At) || !observation.Matches(terms.PlanTerms) || !ReadyAtAssent(observation)
                || withdrawal != null && (withdrawal.Revision <= acceptedRevision || withdrawal.At < observation.At || !terms.InWindow(withdrawal.At)))
                throw new ArgumentException("Invalid prospective charter agreement.");
            Terms = terms;
            PlanId = planId;
            PlanReportRevision = planReportRevision;
            PriorCloseRevision = priorCloseRevision;
            CommandId = commandId;
            AcceptedRevision = acceptedRevision;
            Observation = observation;
            Withdrawal = withdrawal;
        }

        private static bool ReadyAtAssent(NextCharterPlanObservation observation) => observation.Walkable && !observation.Occupied
            && !observation.PathReserved && !observation.TacticalTransition && observation.ApproachAccess != false
            && observation.ScoutCapable && observation.ScoutAtStage && observation.CanCarry == true
            && observation.Supplies.All(x => x.ReadyAvailable >= x.Required);

        public NextCharterAgreementStatus StatusAt(RuleTime at)
            => at < AcceptedAt ? NextCharterAgreementStatus.Offered
                : Withdrawal != null && Withdrawal.At <= at ? NextCharterAgreementStatus.Withdrawn
                : at < Terms.ValidUntil ? NextCharterAgreementStatus.AcceptedConditional : NextCharterAgreementStatus.Expired;

        public NextCharterAgreementRecord WithWithdrawal(NextCharterWithdrawal withdrawal)
            => new NextCharterAgreementRecord(Terms, PlanId, PlanReportRevision, PriorCloseRevision, CommandId, AcceptedRevision,
                Observation, withdrawal ?? throw new ArgumentNullException(nameof(withdrawal)));
    }

    public sealed class NextCharterAgreementAssessment
    {
        public NextCharterAgreementTerms Terms { get; }
        public NextCharterAgreementRecord Agreement { get; }
        public NextCharterPlanObservation CurrentObservation { get; }
        public RuleTime At { get; }
        public long Revision { get; }
        public string CurrentPrerequisiteFailure { get; }
        public NextCharterAgreementStatus Status => Agreement?.StatusAt(At) ?? NextCharterAgreementStatus.Offered;
        public bool AgreementRecorded => Agreement != null;
        public bool InForce => Status == NextCharterAgreementStatus.AcceptedConditional;
        public bool DeparturePermitted => false;

        public NextCharterAgreementAssessment(NextCharterAgreementTerms terms, NextCharterAgreementRecord agreement,
            NextCharterPlanObservation currentObservation, RuleTime at, long revision, string currentPrerequisiteFailure)
        {
            Terms = terms;
            Agreement = agreement;
            CurrentObservation = currentObservation;
            At = at;
            Revision = revision;
            CurrentPrerequisiteFailure = currentPrerequisiteFailure;
        }
    }

    public static class NextCharterAgreementValidation
    {
        public static void Validate(Snapshot state)
        {
            var agreement = state.NextCharterAgreement;
            if (state.SchemaVersion == Snapshot.NextCharterAgreementSchema && !state.TestOnly)
                throw new ArgumentException("The prospective charter profile requires TEST_ONLY authority.");
            if (agreement == null) return;
            if (state.SchemaVersion != Snapshot.NextCharterAgreementSchema)
                throw new ArgumentException("Prospective charter history requires its own schema.");
            var plan = state.NextCharterPlans.SingleOrDefault(x => x.Id == agreement.PlanId);
            var close = state.ExpeditionEpisodeClose;
            if (plan?.Report == null || close == null || close.CloseRevision != agreement.PriorCloseRevision
                || plan.PriorCloseRevision != close.CloseRevision || plan.Report.Revision != agreement.PlanReportRevision
                || plan.Terms.BindingKey != agreement.Terms.PlanTerms.BindingKey || plan.Report.At > agreement.AcceptedAt
                || agreement.AcceptedAt > state.RuleClock)
                throw new ArgumentException("Invalid prospective charter predecessor.");
            VerifyReceipt(state, agreement.AcceptedRevision, agreement.CommandId, agreement.ActorId,
                CommandKind.AcceptNextCharter, agreement.Terms.OfferId);
            var withdrawal = agreement.Withdrawal;
            if (withdrawal == null) return;
            if (withdrawal.At > state.RuleClock) throw new ArgumentException("Invalid prospective charter withdrawal time.");
            VerifyReceipt(state, withdrawal.Revision, withdrawal.CommandId, agreement.ActorId,
                CommandKind.WithdrawNextCharter, agreement.Terms.CharterId);
        }

        private static void VerifyReceipt(Snapshot state, long revision, string commandId, string actor, CommandKind kind, string target)
        {
            var receipt = state.Receipts.SingleOrDefault(x => x.Revision == revision);
            if (receipt == null) throw new ArgumentException("Prospective charter history lacks its receipt.");
            var command = CommandHistory.Read(receipt);
            if (command.Id != commandId || command.Actor != actor || command.Kind != kind || command.Target != target
                || command.ExpectedRevision != revision - 1)
                throw new ArgumentException("Invalid prospective charter receipt.");
        }
    }
}
