using System;
using System.Linq;
using System.Collections.Generic;

namespace Decennium.Foundation
{
    public enum CharterAttemptEventKind
    {
        Admitted = 1, OutboundStarted, OutboundArrived, Observed, ReturnStarted, Returned,
        Suspended, Continued, Aborted, Expired, Withdrawn, ScopeLeft
    }

    public enum CharterAttemptOutcome { Open, ReturnedComplete, ReturnedIncomplete, EndedAtStaging, AwaitingLawfulReturn }

    public sealed class CharterAttemptAuthority
    {
        public string VersionId { get; }
        public string DepartureMandateId { get; }
        public string SiteId { get; }
        public string SiteScopeEvidenceId { get; }
        public string ControllerId { get; }
        public string ControllerAuthorityId { get; }
        public string HeroId { get; }
        public int StageX { get; }
        public int StageY { get; }
        public int ApproachX { get; }
        public int ApproachY { get; }
        public string VisibilityEvidenceId { get; }
        public string FatigueEvidenceId { get; }
        public string RestScheduleId { get; }
        public RestWatchSlot OpeningRestWatch => RestWatchSlot.Evening;
        public RuleTime Epoch { get; }
        public int OpeningStrain { get; }
        public bool OpeningRestDebt { get; }
        public RuleTime FatigueUntil { get; }
        public string EgressPermissionId { get; }
        public string EgressEvidenceId { get; }
        public RuleTime EgressFrom { get; }
        public RuleTime EgressUntil { get; }

        public CharterAttemptAuthority(string versionId, string departureMandateId, string siteId, string siteScopeEvidenceId,
            string controllerId, string controllerAuthorityId, string heroId, int stageX, int stageY, int approachX, int approachY,
            string visibilityEvidenceId, string fatigueEvidenceId, string restScheduleId, RuleTime epoch, int openingStrain,
            bool openingRestDebt, RuleTime fatigueUntil, string egressPermissionId, string egressEvidenceId, RuleTime egressFrom,
            RuleTime egressUntil)
        {
            if (new[] { versionId, departureMandateId, siteId, siteScopeEvidenceId, controllerId, controllerAuthorityId, heroId,
                    visibilityEvidenceId, fatigueEvidenceId, restScheduleId, egressPermissionId, egressEvidenceId }
                .Any(x => !Validation.ValidId(x))
                || stageX < 0 || stageY < 0 || approachX < 0 || approachY < 0
                || Math.Abs((long)stageX - approachX) + Math.Abs((long)stageY - approachY) != 1
                || openingStrain < 0 || openingStrain > 6 || fatigueUntil <= epoch
                || egressFrom < epoch || egressUntil <= egressFrom || egressUntil > fatigueUntil)
                throw new ArgumentException("Invalid charter-attempt authority.");
            VersionId = versionId;
            DepartureMandateId = departureMandateId;
            SiteId = siteId;
            SiteScopeEvidenceId = siteScopeEvidenceId;
            ControllerId = controllerId;
            ControllerAuthorityId = controllerAuthorityId;
            HeroId = heroId;
            StageX = stageX;
            StageY = stageY;
            ApproachX = approachX;
            ApproachY = approachY;
            VisibilityEvidenceId = visibilityEvidenceId;
            FatigueEvidenceId = fatigueEvidenceId;
            RestScheduleId = restScheduleId;
            Epoch = epoch;
            OpeningStrain = openingStrain;
            OpeningRestDebt = openingRestDebt;
            FatigueUntil = fatigueUntil;
            EgressPermissionId = egressPermissionId;
            EgressEvidenceId = egressEvidenceId;
            EgressFrom = egressFrom;
            EgressUntil = egressUntil;
        }

        public bool Matches(NextCharterAgreementTerms agreement) => HeroId == agreement.ParticipantId
            && agreement.AccessPermission != null && ControllerId == agreement.AccessPermission.IssuerId
            && ControllerAuthorityId == agreement.AccessPermission.IssuerAuthorityId
            && StageX == agreement.PlanTerms.StageX && StageY == agreement.PlanTerms.StageY
            && ApproachX == agreement.PlanTerms.ApproachX && ApproachY == agreement.PlanTerms.ApproachY
            && EgressFrom <= agreement.ValidFrom && EgressUntil > agreement.ValidUntil;

        public bool EgressAt(RuleTime time) => EgressFrom <= time && time < EgressUntil;

        public bool Outbound(int fromX, int fromY, int toX, int toY)
            => fromX == StageX && fromY == StageY && toX == ApproachX && toY == ApproachY;

        public bool Return(int fromX, int fromY, int toX, int toY) => Outbound(toX, toY, fromX, fromY);

        public string BindingKey => string.Join("|", VersionId, DepartureMandateId, SiteId, SiteScopeEvidenceId, ControllerId,
            ControllerAuthorityId, HeroId, FormattableString.Invariant($"{StageX},{StageY},{ApproachX},{ApproachY}"),
            VisibilityEvidenceId, FatigueEvidenceId, RestScheduleId, Epoch,
            FormattableString.Invariant($"{OpeningStrain}"), OpeningRestDebt, FatigueUntil, EgressPermissionId,
            EgressEvidenceId, EgressFrom, EgressUntil);
    }

    public sealed class CharterAttemptReadiness
    {
        public NextCharterPlanObservation Physical { get; }
        public int Strain { get; }
        public bool RestDebtOwed { get; }
        public bool RoutePressureApplicable => false;

        public CharterAttemptReadiness(NextCharterPlanObservation physical, int strain, bool restDebtOwed)
        {
            if (physical == null || strain < 0 || strain > 6)
                throw new ArgumentException("Invalid charter-attempt readiness.");
            Physical = physical;
            Strain = strain;
            RestDebtOwed = restDebtOwed;
        }
    }

    public sealed class CharterAttemptEvent
    {
        public CharterAttemptEventKind Kind { get; }
        public string CommandId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public string Reason { get; }

        public CharterAttemptEvent(CharterAttemptEventKind kind, string commandId, long revision, RuleTime at, string reason)
        {
            if (!Enum.IsDefined(typeof(CharterAttemptEventKind), kind) || !Validation.ValidId(commandId) || revision < 1
                || !Validation.ValidId(reason)) throw new ArgumentException("Invalid charter-attempt event.");
            Kind = kind;
            CommandId = commandId;
            Revision = revision;
            At = at;
            Reason = reason;
        }
    }

    public sealed class CharterApproachObservation
    {
        public const string DirectVisibleSurface = "direct-visible-local-surface";
        public string MethodId => DirectVisibleSurface;
        public int X { get; }
        public int Y { get; }
        public bool StageSurfaceWalkable { get; }
        public bool ApproachSurfaceWalkable { get; }
        public string PermissionVersionId { get; }
        public bool HiddenConditionsEstablished => false;
        public bool FuturePassageEstablished => false;

        public CharterApproachObservation(int x, int y, bool stageSurfaceWalkable, bool approachSurfaceWalkable, string permissionVersionId)
        {
            if (x < 0 || y < 0 || !Validation.ValidId(permissionVersionId))
                throw new ArgumentException("Invalid local approach observation.");
            X = x;
            Y = y;
            StageSurfaceWalkable = stageSurfaceWalkable;
            ApproachSurfaceWalkable = approachSurfaceWalkable;
            PermissionVersionId = permissionVersionId;
        }
    }

    public sealed class CharterAttemptRecord
    {
        public const int MaxEvents = 2 * Validation.MaxReceipts;
        public string Id { get; }
        public string CharterId { get; }
        public long AgreementRevision { get; }
        public string PlanId { get; }
        public long CloseRevision { get; }
        public CharterAttemptAuthority Authority { get; }
        public CharterAttemptReadiness Admission { get; }
        public CharterAttemptReadiness Departure { get; }
        public CharterApproachObservation Observation { get; }
        public RuleTime OutboundMovingTime { get; }
        public RuleTime ReturnMovingTime { get; }
        public IReadOnlyList<CharterAttemptEvent> Events { get; }

        public CharterAttemptEvent Admitted => Events[0];
        public CharterAttemptEvent OutboundStarted => Find(CharterAttemptEventKind.OutboundStarted);
        public CharterAttemptEvent OutboundArrived => Find(CharterAttemptEventKind.OutboundArrived);
        public CharterAttemptEvent Observed => Find(CharterAttemptEventKind.Observed);
        public CharterAttemptEvent ReturnStarted => Find(CharterAttemptEventKind.ReturnStarted);
        public CharterAttemptEvent Returned => Find(CharterAttemptEventKind.Returned);
        public CharterAttemptEvent Stop => Events.SingleOrDefault(x => IsStop(x.Kind));
        public bool Interrupted => Events.LastOrDefault(x => x.Kind == CharterAttemptEventKind.Suspended
            || x.Kind == CharterAttemptEventKind.Continued)?.Kind == CharterAttemptEventKind.Suspended;
        public bool ObjectiveOpen => Stop == null && Returned == null;

        public CharterAttemptOutcome Outcome => Returned != null
            ? Stop == null && Observed != null ? CharterAttemptOutcome.ReturnedComplete : CharterAttemptOutcome.ReturnedIncomplete
            : Stop == null ? CharterAttemptOutcome.Open : OutboundStarted == null
                ? CharterAttemptOutcome.EndedAtStaging : CharterAttemptOutcome.AwaitingLawfulReturn;

        public CharterAttemptRecord(string id, string charterId, long agreementRevision, string planId, long closeRevision,
            CharterAttemptAuthority authority, CharterAttemptReadiness admission, IEnumerable<CharterAttemptEvent> events,
            CharterAttemptReadiness departure = null, CharterApproachObservation observation = null,
            RuleTime outboundMovingTime = default, RuleTime returnMovingTime = default)
        {
            var rows = events?.ToArray();
            if (!Validation.ValidId(id) || !Validation.ValidId(charterId) || !Validation.ValidId(planId) || closeRevision < 1
                || agreementRevision <= closeRevision || authority == null || admission == null
                || rows == null || rows.Length < 1 || rows.Length > MaxEvents || rows.Any(x => x == null)
                || rows[0].Kind != CharterAttemptEventKind.Admitted || rows[0].Revision <= agreementRevision
                || admission.Physical.At != rows[0].At || admission.Physical.Revision != rows[0].Revision - 1
                || rows.Skip(1).Where((row, index) => row.Revision < rows[index].Revision || row.At < rows[index].At).Any()
                || rows.GroupBy(x => x.Kind).Any(x => x.Key != CharterAttemptEventKind.Suspended && x.Key != CharterAttemptEventKind.Continued && x.Count() > 1)
                || rows.Count(x => IsStop(x.Kind)) > 1)
                throw new ArgumentException("Invalid charter-attempt history.");
            Id = id;
            CharterId = charterId;
            AgreementRevision = agreementRevision;
            PlanId = planId;
            CloseRevision = closeRevision;
            Authority = authority;
            Admission = admission;
            Departure = departure;
            Observation = observation;
            OutboundMovingTime = outboundMovingTime;
            ReturnMovingTime = returnMovingTime;
            Events = Array.AsReadOnly(rows);
            if (OutboundStarted == null && outboundMovingTime != default || ReturnStarted == null && returnMovingTime != default
                || (OutboundStarted != null) != (departure != null)
                || departure != null && (departure.Physical.At != OutboundStarted.At || departure.Physical.Revision != OutboundStarted.Revision - 1)
                || OutboundArrived != null && (OutboundStarted == null || OutboundArrived.Revision <= OutboundStarted.Revision)
                || (Observed != null) != (observation != null)
                || Observed != null && (OutboundArrived == null || Observed.Revision <= OutboundArrived.Revision
                    || observation.X != authority.ApproachX || observation.Y != authority.ApproachY)
                || ReturnStarted != null && (OutboundArrived == null || ReturnStarted.Revision <= OutboundArrived.Revision)
                || Returned != null && (ReturnStarted == null || Returned.Revision <= ReturnStarted.Revision
                    || Stop == null && (Observed == null || Observed.Revision >= ReturnStarted.Revision)))
                throw new ArgumentException("Invalid charter-attempt stage order.");
        }

        private CharterAttemptEvent Find(CharterAttemptEventKind kind) => Events.SingleOrDefault(x => x.Kind == kind);

        public static bool IsStop(CharterAttemptEventKind kind) => kind == CharterAttemptEventKind.Aborted
            || kind == CharterAttemptEventKind.Expired || kind == CharterAttemptEventKind.Withdrawn || kind == CharterAttemptEventKind.ScopeLeft;

        public CharterAttemptRecord Append(CharterAttemptEvent entry, CharterAttemptReadiness departure = null,
            CharterApproachObservation observation = null)
            => new CharterAttemptRecord(Id, CharterId, AgreementRevision, PlanId, CloseRevision, Authority,
                Admission, Events.Append(entry), departure ?? Departure, observation ?? Observation, OutboundMovingTime, ReturnMovingTime);

        public CharterAttemptRecord WithMovementTimes(RuleTime outbound, RuleTime returning)
            => new CharterAttemptRecord(Id, CharterId, AgreementRevision, PlanId, CloseRevision, Authority,
                Admission, Events, Departure, Observation, outbound, returning);
    }

    public sealed class CharterAttemptAssessment
    {
        public CharterAttemptRecord Attempt { get; }
        public RuleTime At { get; }
        public long Revision { get; }
        public RuleQuantity X { get; }
        public RuleQuantity Y { get; }
        public WorldTraversalRecord Traversal { get; }
        public string ObjectiveBlocker { get; }
        public string EgressBlocker { get; }

        public CharterAttemptAssessment(CharterAttemptRecord attempt, RuleTime at, long revision, RuleQuantity x, RuleQuantity y,
            WorldTraversalRecord traversal, string objectiveBlocker, string egressBlocker)
        {
            Attempt = attempt;
            At = at;
            Revision = revision;
            X = x;
            Y = y;
            Traversal = traversal;
            ObjectiveBlocker = objectiveBlocker;
            EgressBlocker = egressBlocker;
        }
    }

    public static class CharterAttemptValidation
    {
        public static void Validate(Snapshot state)
        {
            if (state.SchemaVersion >= Snapshot.CharterAttemptSchema && !state.TestOnly)
                throw new ArgumentException("Charter-bound local attempts require TEST_ONLY authority.");
            var attempt = state.CharterAttempt;
            if (attempt == null) return;
            var agreement = state.NextCharterAgreement;
            if (state.SchemaVersion < Snapshot.CharterAttemptSchema || agreement == null || attempt.CharterId != agreement.Terms.CharterId
                || attempt.AgreementRevision != agreement.AcceptedRevision || attempt.PlanId != agreement.PlanId
                || attempt.CloseRevision != agreement.PriorCloseRevision || !attempt.Authority.Matches(agreement.Terms)
                || !attempt.Admission.Physical.Matches(agreement.Terms.PlanTerms)
                || attempt.Departure != null && !attempt.Departure.Physical.Matches(agreement.Terms.PlanTerms)
                || attempt.Observation != null && attempt.Observation.PermissionVersionId != agreement.Terms.AccessPermission.VersionId
                || attempt.Id != "charter.attempt." + attempt.Admitted.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture))
                throw new ArgumentException("Invalid charter-attempt agreement binding.");

            foreach (var entry in attempt.Events) {
                var receipt = state.Receipts.SingleOrDefault(x => x.Revision == entry.Revision);
                if (receipt == null || receipt.Id != entry.CommandId || entry.At > state.RuleClock)
                    throw new ArgumentException("Invalid charter-attempt receipt provenance.");
                var command = CommandHistory.Read(receipt);
                switch (entry.Kind) {
                    case CharterAttemptEventKind.Admitted:
                        if (command.Kind != CommandKind.StartCharterAttempt || command.Actor != attempt.Authority.HeroId
                            || command.Target != attempt.CharterId) throw new ArgumentException("Invalid charter-attempt admission receipt.");
                        break;
                    case CharterAttemptEventKind.OutboundStarted:
                    case CharterAttemptEventKind.ReturnStarted:
                        int sign = entry.Kind == CharterAttemptEventKind.OutboundStarted ? 1 : -1;
                        if (command.Kind != CommandKind.BeginWorldStep || command.Actor != attempt.Authority.HeroId || command.Target != "walk"
                            || command.X != sign * (attempt.Authority.ApproachX - attempt.Authority.StageX)
                            || command.Y != sign * (attempt.Authority.ApproachY - attempt.Authority.StageY))
                            throw new ArgumentException("Invalid charter-attempt traversal receipt.");
                        break;
                    case CharterAttemptEventKind.Observed:
                        if (command.Kind != CommandKind.ObserveCharterApproach || command.Actor != attempt.Authority.HeroId
                            || command.Target != attempt.Id) throw new ArgumentException("Invalid charter-attempt observation receipt.");
                        break;
                    case CharterAttemptEventKind.Withdrawn:
                        if (agreement.Withdrawal?.Revision != entry.Revision || agreement.Withdrawal.At != entry.At)
                            throw new ArgumentException("Invalid charter-attempt withdrawal receipt.");
                        break;
                }
            }
        }
    }
}
