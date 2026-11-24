#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyNextCharterAgreementProfile
    {
        public const string OfferId = "TEST_ONLY.haven-approach-charter-offer.v1";
        public const string CharterId = "TEST_ONLY.haven-approach-charter";
        public const string CharterVersionId = "TEST_ONLY.haven-approach-charter.v1";
        public const string SiteControllerId = "TEST_ONLY.haven-approach-site-controller";
        public const string SiteControlAuthorityId = "TEST_ONLY.haven-approach-site-control-assignment.v1";
        public const string PermissionId = "TEST_ONLY.haven-approach-walk-permission.v1";
        public const string PermissionEvidenceId = "TEST_ONLY.haven-approach-walk-grant.v1";
        public const string RestrictionsId = "TEST_ONLY.haven-approach-walk-observe-only";
        public const string ParticipantId = TestOnlyNextCharterPlanProfile.PlannerId;

        public RuleTime ValidFrom { get; }
        public RuleTime ValidUntil { get; }
        public NextCharterAccessPermission AccessPermission { get; }
        public bool AssentAuthorized { get; }
        public bool RecordsAccessible { get; }
        public bool ResourceUseAuthorized { get; }
        public bool ConflictingRestriction { get; }
        public string ResourceOwnerId { get; }

        public TestOnlyNextCharterAgreementProfile(int validFrom = 11000, int validUntil = 24000, bool assentAuthorized = true,
            bool recordsAccessible = true, bool resourceUseAuthorized = true, bool conflictingRestriction = false,
            bool accessIssued = true, NextCharterAccessPermission accessPermission = null, string resourceOwnerId = ParticipantId)
        {
            ValidFrom = new RuleTime(validFrom);
            ValidUntil = new RuleTime(validUntil);
            AssentAuthorized = assentAuthorized;
            RecordsAccessible = recordsAccessible;
            ResourceUseAuthorized = resourceUseAuthorized;
            ConflictingRestriction = conflictingRestriction;
            ResourceOwnerId = resourceOwnerId;
            AccessPermission = accessIssued ? accessPermission ?? IssueAccess(validFrom, validUntil) : null;
        }

        // The selected scenario establishes control of these two locations and the edge by the named site office.
        // The existing grant authorizes both directions and the limited observation for the named beneficiary.
        public static NextCharterAccessPermission IssueAccess(int validFrom = 11000, int validUntil = 24000,
            string issuerId = SiteControllerId, string authorityId = SiteControlAuthorityId, string beneficiaryId = ParticipantId,
            int approachX = 3, int approachY = 3, NextCharterPassageDirections directions = NextCharterPassageDirections.RoundTrip)
            => new NextCharterAccessPermission(PermissionId, PermissionEvidenceId, issuerId, authorityId, beneficiaryId,
                TestOnlyHavenAppraisalProfile.SiteX, TestOnlyHavenAppraisalProfile.SiteY, approachX, approachY,
                directions, NextCharterAccessPermission.WalkAndObserve, new RuleTime(validFrom), new RuleTime(validUntil), 0, RestrictionsId);

        internal NextCharterAgreementTerms Bind(NextCharterPlanTerms plan)
            => new NextCharterAgreementTerms(OfferId, CharterId, CharterVersionId, "TEST_ONLY.next-charter-assent-mandate.v1",
                "TEST_ONLY.next-charter-assent-records-access.v1", "TEST_ONLY.hero-own-stock-use.haven-approach.v1",
                ResourceOwnerId, NextCharterOffice.All, plan, AccessPermission, ValidFrom, ValidUntil);

        internal string Key => string.Join("|", "FL02-FL26-SO01-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4",
            AssentAuthorized, RecordsAccessible, ResourceUseAuthorized, ConflictingRestriction, "unreserved-own-designations");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyNextCharterAgreementProfile nextCharterAgreementProfile;
        private NextCharterAgreementTerms nextCharterAgreementTerms;

        public TestOnlySharedWorldPolicy EnableNextCharterAgreement(TestOnlyNextCharterAgreementProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || nextCharterAgreementProfile != null || SelectedSchema != Snapshot.NextCharterPlanSchema)
                throw new InvalidOperationException("Select one prospective agreement on the accepted planning host before initialization.");
            nextCharterAgreementTerms = profile.Bind(nextCharterPlanProfile.Terms);
            nextCharterAgreementProfile = profile;
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.charter-assent-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(
                    ContentFingerprint + "|" + nextCharterAgreementTerms.BindingKey + "|" + profile.Key))
                    .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private static bool IsNextCharterAgreementCommand(CommandKind kind)
            => kind == CommandKind.AcceptNextCharter || kind == CommandKind.WithdrawNextCharter || kind == CommandKind.InspectNextCharterAgreement;

        private IEnumerable<Command> DiscoverNextCharterAgreement(Snapshot state, string actor)
        {
            if (nextCharterAgreementProfile == null || actor != nextCharterAgreementTerms.ParticipantId) yield break;
            Command Option(CommandKind kind, string target) => new Command("option."
                + state.Revision.ToString(CultureInfo.InvariantCulture) + ".charter-assent." + kind, actor, state.Revision, kind, target);
            var agreement = state.NextCharterAgreement;
            if (agreement == null) {
                if (state.NextCharterPlans.Any(x => x.Report != null))
                    yield return Option(CommandKind.AcceptNextCharter, nextCharterAgreementTerms.OfferId);
                yield break;
            }
            yield return Option(CommandKind.InspectNextCharterAgreement, agreement.Terms.CharterId);
            if (agreement.StatusAt(state.RuleClock) == NextCharterAgreementStatus.AcceptedConditional)
                yield return Option(CommandKind.WithdrawNextCharter, agreement.Terms.CharterId);
        }

        private string NextCharterAgreementAuthorityFailure()
            => NextCharterAgreementAuthorityFailureConstraintV1()?.NativeCode;

        private NativeCommandConstraintV1 NextCharterAgreementAuthorityFailureConstraintV1()
        {
            var profile = nextCharterAgreementProfile;
            var terms = nextCharterAgreementTerms;
            if (!profile.AssentAuthorized) return new NativeCommandConstraintV1("NextCharterAssentMandateMissing", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 106);
            if (!profile.RecordsAccessible) return new NativeCommandConstraintV1("NextCharterAssentRecordsUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 107);
            if (!profile.ResourceUseAuthorized || terms.ResourceOwnerId != terms.ParticipantId)
                return new NativeCommandConstraintV1("NextCharterAssentResourceUseUnauthorized", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 109);
            var permission = terms.AccessPermission;
            if (permission == null) return new NativeCommandConstraintV1("NextCharterAssentPermissionMissing", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 111);
            if (permission.VersionId != TestOnlyNextCharterAgreementProfile.PermissionId
                || permission.EvidenceId != TestOnlyNextCharterAgreementProfile.PermissionEvidenceId
                || permission.IssuerId != TestOnlyNextCharterAgreementProfile.SiteControllerId
                || permission.IssuerAuthorityId != TestOnlyNextCharterAgreementProfile.SiteControlAuthorityId
                || permission.RestrictionsId != TestOnlyNextCharterAgreementProfile.RestrictionsId)
                return new NativeCommandConstraintV1("NextCharterAssentPermissionIssuerUnestablished", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 117);
            if (!terms.PermissionCoversWindow) return new NativeCommandConstraintV1("NextCharterAssentPermissionScopeOrValidity", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 118);
            return profile.ConflictingRestriction ? new NativeCommandConstraintV1("NextCharterAssentApplicableRestriction", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 119) : null;
        }

        private static bool CanDecideNextCharter(Snapshot state, string actor)
        {
            var view = View(state, actor);
            return ActorLifeRules.CanAct(state, actor) && !view.Unaware && !view.Clauses.Incapacitated
                && !ExpeditionStrainRules.Current(state, actor).Incapacitated;
        }

        private string NextCharterAgreementPhysicalFailure(Snapshot state, NextCharterPlanObservation current)
            => NextCharterAgreementPhysicalFailureConstraintV1(state, current)?.NativeCode;

        private NativeCommandConstraintV1 NextCharterAgreementPhysicalFailureConstraintV1(Snapshot state, NextCharterPlanObservation current)
        {
            string actor = nextCharterAgreementTerms.ParticipantId;
            if (state.InventoryCombat || PendingCalendarChoice(state) || ManufacturingChoicePending(state)
                || state.Encounter != null && !ResolvedConflict(state))
                return new NativeCommandConstraintV1("NextCharterAssentStableBoundaryRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 134);
            if (current.CanCarry != true) return new NativeCommandConstraintV1("NextCharterAssentCarryingCapacity", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 135);
            if (!current.ScoutCapable || !CanDecideNextCharter(state, actor)) return new NativeCommandConstraintV1("NextCharterAssentActorIncapable", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 136);
            if (!current.ScoutAtStage) return new NativeCommandConstraintV1("NextCharterAssentStationaryStagingRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 137);
            if (OrdinaryInventory.Busy(state, actor)) return new NativeCommandConstraintV1("NextCharterAssentWorkerBusy", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 138);
            if (current.ApproachAccess == false) return new NativeCommandConstraintV1("NextCharterAssentPermissionContradicted", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 139);
            if (!current.Walkable || current.Occupied || current.PathReserved || current.TacticalTransition)
                return new NativeCommandConstraintV1("NextCharterAssentPassageUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 141);
            return current.Supplies.All(x => x.ReadyAvailable >= x.Required) ? null : new NativeCommandConstraintV1("NextCharterAssentReadyReservesInsufficient", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 142);
        }

        private string AssessNextCharterAgreementCommand(Snapshot state, Command command, out NextCharterPlanRecord plan,
            out NextCharterAgreementAssessment assessment)
            => AssessNextCharterAgreementCommandConstraintV1(state, command, out plan, out assessment)?.NativeCode;

        private NativeCommandConstraintV1 AssessNextCharterAgreementCommandConstraintV1(Snapshot state, Command command, out NextCharterPlanRecord plan,
            out NextCharterAgreementAssessment assessment)
        {
            plan = null;
            assessment = null;
            var terms = nextCharterAgreementTerms;
            if (nextCharterAgreementProfile == null || state.SchemaVersion < Snapshot.NextCharterAgreementSchema)
                return new NativeCommandConstraintV1("NextCharterAssentNotSelected", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 152);
            if (command.Actor != terms.ParticipantId) return new NativeCommandConstraintV1("NextCharterAssentActorUnauthorized", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 153);
            if (!NextCharterCommandPayloadValid(command)) return new NativeCommandConstraintV1("InvalidNextCharterAssentPayload", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 154);
            var agreement = state.NextCharterAgreement;
            if (command.Kind != CommandKind.AcceptNextCharter) {
                if (agreement == null || command.Target != agreement.Terms.CharterId) return new NativeCommandConstraintV1("NextCharterAgreementUnknown", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 157);
                if (!nextCharterAgreementProfile.RecordsAccessible) return new NativeCommandConstraintV1("NextCharterAssentRecordsUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 158);
                if (command.Kind == CommandKind.WithdrawNextCharter) {
                    if (agreement.Withdrawal != null) return new NativeCommandConstraintV1("NextCharterAlreadyWithdrawn", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 160);
                    if (!terms.InWindow(state.RuleClock)) return new NativeCommandConstraintV1("NextCharterAgreementExpired", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 161);
                    if (PendingCalendarChoice(state) || ManufacturingChoicePending(state)) return new NativeCommandConstraintV1("NextCharterAssentStableBoundaryRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 162);
                    return CanDecideNextCharter(state, command.Actor) ? null : new NativeCommandConstraintV1("NextCharterAssentActorIncapable", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 163);
                }
                var current = ObserveNextCharterPlan(state, state.Revision);
                assessment = new NextCharterAgreementAssessment(terms, agreement, current, state.RuleClock, state.Revision,
                    NextCharterAgreementAuthorityFailure() ?? NextCharterAgreementPhysicalFailure(state, current));
                return null;
            }

            if (command.Target != terms.OfferId) return new NativeCommandConstraintV1("NextCharterOfferUnknown", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 171);
            if (agreement != null) return new NativeCommandConstraintV1("NextCharterOfferAlreadyAccepted", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 172);
            var authorityFailure= NextCharterAgreementAuthorityFailureConstraintV1();
            if (authorityFailure != null) return authorityFailure;
            if (!terms.InWindow(state.RuleClock)) return new NativeCommandConstraintV1("NextCharterAssentOfferOutsideWindow", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 175);
            var close = state.ExpeditionEpisodeClose;
            if (close == null || close.EpisodeId != terms.PlanTerms.EpisodeId || close.CharterVersionId != terms.PlanTerms.CharterVersionId)
                return new NativeCommandConstraintV1("NextCharterAssentPriorCloseRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 178);
            plan = state.NextCharterPlans.SingleOrDefault(x => x.Report != null);
            if (plan == null || plan.Terms.BindingKey != terms.PlanTerms.BindingKey || plan.PriorCloseRevision != close.CloseRevision)
                return new NativeCommandConstraintV1("NextCharterAssentCompletedPlanRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedNextCharterAgreement.cs", 181);

            var observation = ObserveNextCharterPlan(state, state.Revision);
            var physicalFailure= NextCharterAgreementPhysicalFailureConstraintV1(state, observation);
            assessment = new NextCharterAgreementAssessment(terms, null, observation, state.RuleClock, state.Revision, physicalFailure?.NativeCode);
            return physicalFailure;
        }

        private string ResolveNextCharterAgreement(Snapshot state, Command command)
        {
            string failure = AssessNextCharterAgreementCommand(state, command, out var plan, out var assessment);
            if (failure != null) return failure;
            if (command.Kind == CommandKind.InspectNextCharterAgreement) return "NextCharterAgreementReadOnly";
            if (command.Kind == CommandKind.WithdrawNextCharter) {
                state.NextCharterAgreement = state.NextCharterAgreement.WithWithdrawal(
                    new NextCharterWithdrawal(command.Id, state.Revision + 1, state.RuleClock));
                return null;
            }
            state.NextCharterAgreement = new NextCharterAgreementRecord(nextCharterAgreementTerms, plan.Id, plan.Report.Revision,
                plan.PriorCloseRevision, command.Id, state.Revision + 1, assessment.CurrentObservation);
            return null;
        }
    }
}
#endif
