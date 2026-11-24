#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyCharterAttemptProfile
    {
        public bool DepartureAuthorized { get; }
        public bool ControlledLocalSite { get; }
        public bool CurrentFatigueHistoryEstablished { get; }
        public bool EgressIssued { get; }
        public bool DirectViewEstablished { get; }
        public bool ConflictingLocalRestriction { get; }
        public RuleTime FatigueUntil { get; }
        public RuleTime EgressUntil { get; }

        public TestOnlyCharterAttemptProfile(bool departureAuthorized = true, bool controlledLocalSite = true,
            bool currentFatigueHistoryEstablished = true, bool egressIssued = true, bool directViewEstablished = true,
            bool conflictingLocalRestriction = false, int fatigueUntil = 28800, int egressUntil = 24500)
        {
            if (fatigueUntil > ExpeditionPressureRules.WatchSeconds)
                throw new ArgumentOutOfRangeException(nameof(fatigueUntil));
            DepartureAuthorized = departureAuthorized;
            ControlledLocalSite = controlledLocalSite;
            CurrentFatigueHistoryEstablished = currentFatigueHistoryEstablished;
            EgressIssued = egressIssued;
            DirectViewEstablished = directViewEstablished;
            ConflictingLocalRestriction = conflictingLocalRestriction;
            FatigueUntil = new RuleTime(fatigueUntil);
            EgressUntil = new RuleTime(egressUntil);
        }

        internal CharterAttemptAuthority Bind(NextCharterAgreementTerms agreement)
        {
            var plan = agreement.PlanTerms;
            return new CharterAttemptAuthority("TEST_ONLY.local-charter-attempt.v1", "TEST_ONLY.local-departure-mandate.v1",
                "TEST_ONLY.haven-controlled-approach", "TEST_ONLY.controlled-edge-outside-route-and-camp.v1",
                TestOnlyNextCharterAgreementProfile.SiteControllerId, TestOnlyNextCharterAgreementProfile.SiteControlAuthorityId,
                agreement.ParticipantId, plan.StageX, plan.StageY, plan.ApproachX, plan.ApproachY,
                "TEST_ONLY.daylight-direct-local-view.v1", "TEST_ONLY.hero-opening-fatigue-and-debt.v1",
                "TEST_ONLY.epoch-zero-evening-rest-schedule.v1", default, 0, false, FatigueUntil,
                "TEST_ONLY.haven-approach-egress.v1", "TEST_ONLY.site-controller-egress-grant.v1",
                agreement.ValidFrom, EgressUntil);
        }

        internal string Key => string.Join("|", "FL03-FL08-FL26-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4",
            DepartureAuthorized, ControlledLocalSite, CurrentFatigueHistoryEstablished, EgressIssued,
            DirectViewEstablished, ConflictingLocalRestriction, "finish-entered-edge-and-return-only");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyCharterAttemptProfile charterAttemptProfile;
        private CharterAttemptAuthority charterAttemptAuthority;

        public TestOnlySharedWorldPolicy EnableCharterAttempt(TestOnlyCharterAttemptProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || charterAttemptProfile != null || SelectedSchema != Snapshot.NextCharterAgreementSchema)
                throw new InvalidOperationException("Select one local attempt on the accepted charter host before initialization.");
            charterAttemptAuthority = profile.Bind(nextCharterAgreementTerms);
            charterAttemptProfile = profile;
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.charter-attempt-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(
                    ContentFingerprint + "|" + charterAttemptAuthority.BindingKey + "|" + profile.Key))
                    .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private static bool IsCharterAttemptCommand(CommandKind kind) => kind == CommandKind.StartCharterAttempt
            || kind == CommandKind.ObserveCharterApproach || kind == CommandKind.AbortCharterAttempt || kind == CommandKind.InspectCharterAttempt;

        private IEnumerable<Command> DiscoverCharterAttempt(Snapshot state, string actor)
        {
            if (charterAttemptProfile == null || actor != charterAttemptAuthority.HeroId || state.NextCharterAgreement == null) yield break;
            Command Option(CommandKind kind, string target) => new Command("option."
                + state.Revision.ToString(CultureInfo.InvariantCulture) + ".local-attempt." + kind, actor, state.Revision, kind, target);
            var attempt = state.CharterAttempt;
            if (attempt == null) {
                yield return Option(CommandKind.StartCharterAttempt, state.NextCharterAgreement.Terms.CharterId);
                yield break;
            }
            yield return Option(CommandKind.InspectCharterAttempt, attempt.Id);
            if (!attempt.ObjectiveOpen) yield break;
            yield return Option(CommandKind.AbortCharterAttempt, attempt.Id);
            if (attempt.OutboundArrived != null && attempt.Observed == null && attempt.ReturnStarted == null)
                yield return Option(CommandKind.ObserveCharterApproach, attempt.Id);
        }

        private string CharterLocalScopeFailure(Snapshot state)
            => CharterLocalScopeFailureConstraintV1(state)?.NativeCode;

        private NativeCommandConstraintV1 CharterLocalScopeFailureConstraintV1(Snapshot state)
        {
            var authority = charterAttemptAuthority;
            if (!charterAttemptProfile.ControlledLocalSite) return new NativeCommandConstraintV1("CharterLocalSiteScopeMissing", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 98);
            var cohorts = state.ExpeditionPressureCohorts.Where(x => x.Members.Contains(authority.HeroId))
                .Select(x => x.Id).ToHashSet(StringComparer.Ordinal);
            if (charterAttemptProfile.ConflictingLocalRestriction
                || state.ExpeditionPressureExposures.Any(x => cohorts.Contains(x.CohortId) && !x.EndedAt.HasValue)
                || state.ExpeditionCampActivities.Any(x => cohorts.Contains(x.CohortId) && x.Active)
                || state.RouteTravels.Any(x => x.TravelerId == authority.HeroId
                    && (x.Status == ExpeditionRouteTravelStatus.Moving || x.Status == ExpeditionRouteTravelStatus.Paused)))
                return new NativeCommandConstraintV1("CharterLocalSiteScopeContradicted", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 106);
            return null;
        }

        private string CharterFatigueFailure(Snapshot state, out int strain, out bool debt)
            => CharterFatigueFailureConstraintV1(state, out strain, out debt)?.NativeCode;

        private NativeCommandConstraintV1 CharterFatigueFailureConstraintV1(Snapshot state, out int strain, out bool debt)
        {
            strain = default;
            debt = default;
            var authority = charterAttemptAuthority;
            var actor = authority.HeroId;
            if (!charterAttemptProfile.CurrentFatigueHistoryEstablished || state.WorldSchedule.Origin != authority.Epoch
                || state.RuleClock < authority.Epoch || state.RuleClock >= authority.FatigueUntil)
                return new NativeCommandConstraintV1("CharterCurrentFatigueBasisUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 118);
            if (state.RestWatchOutcomes.Any(x => x.ActorId == actor) && restDebtProfile == null)
                return new NativeCommandConstraintV1("CharterCurrentFatigueBasisContradicted", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 120);
            if (restDebtProfile != null || state.RestDebtEvents.Any(x => x.ActorId == actor)) {
                var represented = DebtFor(state, actor);
                if (represented.Owed && represented.Deadline <= state.RuleClock)
                    return new NativeCommandConstraintV1("CharterCurrentDebtDeadlineUnresolved", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 124);
                debt = represented.Owed;
            } else debt = authority.OpeningRestDebt;
            strain = authority.OpeningStrain + ExpeditionStrainRules.Current(state, actor).Level;
            return strain <= 6 ? null : new NativeCommandConstraintV1("CharterCurrentFatigueBasisContradicted", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 128);
        }

        private string CharterObjectiveAuthorityFailure(Snapshot state)
            => CharterObjectiveAuthorityFailureConstraintV1(state)?.NativeCode;

        private NativeCommandConstraintV1 CharterObjectiveAuthorityFailureConstraintV1(Snapshot state)
        {
            var agreement = state.NextCharterAgreement;
            if (agreement == null) return new NativeCommandConstraintV1("CharterAcceptedAgreementRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 134);
            if (agreement.StatusAt(state.RuleClock) != NextCharterAgreementStatus.AcceptedConditional)
                return new NativeCommandConstraintV1("CharterAgreementOutOfForce", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 136);
            if (!charterAttemptProfile.DepartureAuthorized) return new NativeCommandConstraintV1("CharterDepartureMandateMissing", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 137);
            if (!charterAttemptProfile.EgressIssued || !charterAttemptAuthority.Matches(agreement.Terms))
                return new NativeCommandConstraintV1("CharterEgressAuthorityMissing", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 139);
            return CharterLocalScopeFailureConstraintV1(state) ?? NextCharterAgreementAuthorityFailureConstraintV1();
        }

        private string CharterObjectiveReadiness(Snapshot state, bool requireStaging, out CharterAttemptReadiness readiness)
            => CharterObjectiveReadinessConstraintV1(state, requireStaging, out readiness)?.NativeCode;

        private NativeCommandConstraintV1 CharterObjectiveReadinessConstraintV1(Snapshot state, bool requireStaging, out CharterAttemptReadiness readiness)
        {
            readiness = null;
            var failure= CharterObjectiveAuthorityFailureConstraintV1(state);
            if (failure != null) return failure;
            failure = CharterFatigueFailureConstraintV1(state, out int strain, out bool debt);
            if (failure != null) return failure;
            var authority = charterAttemptAuthority;
            string actor = authority.HeroId;
            var current = ObserveNextCharterPlan(state, state.Revision);
            readiness = new CharterAttemptReadiness(current, strain, debt);
            if (state.InventoryCombat || PendingCalendarChoice(state) || ManufacturingChoicePending(state)
                || state.Encounter != null && !ResolvedConflict(state) || current.TacticalTransition)
                return new NativeCommandConstraintV1("CharterTacticalTransitionRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 156);
            if (current.CanCarry != true) return new NativeCommandConstraintV1("CharterHardCarryingLimit", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 157);
            if (!current.ScoutCapable || !CanDecideNextCharter(state, actor)) return new NativeCommandConstraintV1("CharterActorIncapable", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 158);
            if (requireStaging && !current.ScoutAtStage) return new NativeCommandConstraintV1("CharterStationaryStagingRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 159);
            if (OrdinaryInventory.Busy(state, actor)) return new NativeCommandConstraintV1("CharterActorBusy", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 160);
            if (current.ApproachAccess == false) return new NativeCommandConstraintV1("CharterAccessContradicted", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 161);
            if (!current.Walkable || current.Occupied || current.PathReserved) return new NativeCommandConstraintV1("CharterPassageObstructed", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 162);
            if (!charterAttemptProfile.DirectViewEstablished || View(state, actor).BlocksSight) return new NativeCommandConstraintV1("CharterDirectObservationUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 163);
            return current.Supplies.All(x => x.ReadyAvailable >= x.Required) ? null : new NativeCommandConstraintV1("CharterReadySupportInsufficient", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 164);
        }

        private string CharterEgressFailure(Snapshot state, int fromX, int fromY, int toX, int toY)
        {
            var authority = charterAttemptAuthority;
            string scope = CharterLocalScopeFailure(state);
            if (scope != null) return scope;
            if (!charterAttemptProfile.EgressIssued || !authority.EgressAt(state.RuleClock)) return "CharterEgressPermissionUnavailable";
            if (state.InventoryCombat || PendingCalendarChoice(state) || ManufacturingChoicePending(state)
                || WorldStepWouldStartEncounter(state, authority.HeroId, fromX, fromY, toX, toY))
                return "CharterEgressTacticalTransitionRequired";
            string actor = authority.HeroId;
            if (!CapableWorker(state, actor) || !Permissions(state, actor).VoluntarySpeed || Speed(state, actor) == 0)
                return "CharterEgressActorIncapable";
            if (OrdinaryInventory.Busy(state, actor)) return "CharterEgressActorBusy";
            var burden = PortableEquipmentRules.CarriedBurden(state, actor);
            if (PlaytestCarrying.CanCarry(PlaytestCarrying.Limits(CarrierSize.Medium, 10), burden) != true)
                return "CharterEgressHardCarryingLimit";
            return WorldSpatialQueries.Step(state, actor, fromX, fromY, toX, toY, false, false, (x, y) => WorldWalkable(state, x, y))
                    == SpatialStepFailure.None && !RoutePathReserved(state, actor, toX, toY)
                ? null : "CharterEgressPassageObstructed";
        }

        private string AssessCharterAttempt(Snapshot state, Command command, out CharterAttemptReadiness readiness,
            out CharterAttemptAssessment assessment)
            => AssessCharterAttemptConstraintV1(state, command, out readiness, out assessment)?.NativeCode;

        private NativeCommandConstraintV1 AssessCharterAttemptConstraintV1(Snapshot state, Command command, out CharterAttemptReadiness readiness,
            out CharterAttemptAssessment assessment)
        {
            readiness = null;
            assessment = null;
            if (charterAttemptProfile == null || state.SchemaVersion < Snapshot.CharterAttemptSchema)
                return new NativeCommandConstraintV1("CharterAttemptNotSelected", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 194);
            string actor = charterAttemptAuthority.HeroId;
            if (command.Actor != actor) return new NativeCommandConstraintV1("CharterAttemptActorUnauthorized", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 196);
            if (!NextCharterCommandPayloadValid(command)) return new NativeCommandConstraintV1("InvalidCharterAttemptPayload", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 197);
            var attempt = state.CharterAttempt;
            if (command.Kind == CommandKind.StartCharterAttempt) {
                if (state.NextCharterAgreement == null) return new NativeCommandConstraintV1("CharterAcceptedAgreementRequired", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 200);
                if (command.Target != state.NextCharterAgreement.Terms.CharterId) return new NativeCommandConstraintV1("CharterAttemptAgreementUnknown", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 201);
                if (attempt != null) return new NativeCommandConstraintV1("CharterAttemptAlreadyAdmitted", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 202);
                return CharterObjectiveReadinessConstraintV1(state, true, out readiness);
            }
            if (attempt == null || command.Target != attempt.Id) return new NativeCommandConstraintV1("CharterAttemptUnknown", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 205);
            if (command.Kind == CommandKind.InspectCharterAttempt) {
                var position = WorldPositionResolver.Position(state, actor);
                var edge = state.WorldTraversals.SingleOrDefault(x => x.ActorId == actor);
                string objective = attempt.ObjectiveOpen ? CharterObjectiveReadiness(state, attempt.OutboundStarted == null, out _) : "CharterObjectiveEnded";
                string egress = null;
                if (attempt.Returned == null && attempt.OutboundStarted != null) {
                    var authority = attempt.Authority;
                    if (edge != null && IsCharterEdge(attempt, edge))
                        egress = CharterEgressFailure(state, edge.FromX, edge.FromY, edge.ToX, edge.ToY);
                    else if (AtSalePosition(state, actor, authority.ApproachX, authority.ApproachY))
                        egress = CharterEgressFailure(state, authority.ApproachX, authority.ApproachY, authority.StageX, authority.StageY);
                    else egress = "CharterEgressRequiresBoundPosition";
                }
                assessment = new CharterAttemptAssessment(attempt, state.RuleClock, state.Revision, position.X, position.Y, edge, objective, egress);
                return null;
            }
            if (!attempt.ObjectiveOpen) return new NativeCommandConstraintV1("CharterObjectiveEnded", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 222);
            if (command.Kind == CommandKind.AbortCharterAttempt)
                return CanDecideNextCharter(state, actor) ? null : new NativeCommandConstraintV1("CharterActorIncapable", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 224);
            if (attempt.Observed != null) return new NativeCommandConstraintV1("CharterApproachAlreadyObserved", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 225);
            if (attempt.OutboundArrived == null || attempt.ReturnStarted != null
                || !AtSalePosition(state, actor, attempt.Authority.ApproachX, attempt.Authority.ApproachY))
                return new NativeCommandConstraintV1("CharterObservationRequiresStationaryArrival", "engine/com.decennium.foundation/Laboratory/Model/SharedCharterAttempt.cs", 228);
            return CharterObjectiveReadinessConstraintV1(state, false, out readiness);
        }

        private static CharterAttemptEvent AttemptEvent(Snapshot state, Command cause, CharterAttemptEventKind kind, string reason)
            => new CharterAttemptEvent(kind, cause.Id, state.Revision + 1, state.RuleClock, reason);

        private static bool IsCharterEdge(CharterAttemptRecord attempt, WorldTraversalRecord edge)
            => edge.ActorId == attempt.Authority.HeroId
                && (edge.StartedRevision == attempt.OutboundStarted?.Revision || edge.StartedRevision == attempt.ReturnStarted?.Revision);

        private static void SuspendCharterTraversal(Snapshot state, CharterAttemptRecord attempt)
        {
            var edge = state.WorldTraversals.SingleOrDefault(x => IsCharterEdge(attempt, x));
            if (edge != null && edge.Status != WorldTraversalStatus.Suspended)
                SetEdge(state, edge.With(edge.DistanceFeet, WorldTraversalStatus.Suspended));
        }

        private static void StopCharterObjective(Snapshot state, Command cause, CharterAttemptEventKind kind, string reason)
        {
            var attempt = state.CharterAttempt;
            if (!attempt.ObjectiveOpen) return;
            SuspendCharterTraversal(state, attempt);
            state.CharterAttempt = attempt.Append(AttemptEvent(state, cause, kind, reason));
        }

        private static void ContinueCharterAttempt(Snapshot state, Command cause)
        {
            var attempt = state.CharterAttempt;
            if (attempt.Interrupted)
                state.CharterAttempt = attempt.Append(AttemptEvent(state, cause, CharterAttemptEventKind.Continued, "CharterExplicitContinuation"));
        }

        private string ResolveCharterAttempt(Snapshot state, Command command)
        {
            string failure = AssessCharterAttempt(state, command, out var readiness, out _);
            if (failure != null) return failure;
            var attempt = state.CharterAttempt;
            switch (command.Kind) {
                case CommandKind.StartCharterAttempt:
                    var agreement = state.NextCharterAgreement;
                    var admission = AttemptEvent(state, command, CharterAttemptEventKind.Admitted, "CharterAttemptAdmitted");
                    state.CharterAttempt = new CharterAttemptRecord("charter.attempt." + admission.Revision.ToString(CultureInfo.InvariantCulture),
                        agreement.Terms.CharterId, agreement.AcceptedRevision, agreement.PlanId, agreement.PriorCloseRevision,
                        charterAttemptAuthority, readiness, new[] { admission });
                    return null;
                case CommandKind.AbortCharterAttempt:
                    StopCharterObjective(state, command, CharterAttemptEventKind.Aborted, "CharterExplicitAbort");
                    return null;
                case CommandKind.ObserveCharterApproach:
                    ContinueCharterAttempt(state, command);
                    var authority = attempt.Authority;
                    var observation = new CharterApproachObservation(authority.ApproachX, authority.ApproachY,
                        WorldWalkable(state, authority.StageX, authority.StageY), WorldWalkable(state, authority.ApproachX, authority.ApproachY),
                        state.NextCharterAgreement.Terms.AccessPermission.VersionId);
                    state.CharterAttempt = state.CharterAttempt.Append(
                        AttemptEvent(state, command, CharterAttemptEventKind.Observed, "CharterDirectSurfaceObserved"), observation: observation);
                    return null;
                default: return "CharterAttemptReadOnly";
            }
        }

        private bool IsCharterOutwardStep(Snapshot state, CharterAttemptRecord attempt, Command command, WorldStepFacts facts)
        {
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            return attempt.ObjectiveOpen && attempt.OutboundStarted == null && command.Target == "walk"
                && attempt.Authority.Outbound(actor.X, actor.Y, facts.ToX, facts.ToY);
        }

        private static bool IsCharterReturnStep(Snapshot state, CharterAttemptRecord attempt, Command command, WorldStepFacts facts)
        {
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            return attempt.OutboundArrived != null && attempt.ReturnStarted == null
                && attempt.Authority.Return(actor.X, actor.Y, facts.ToX, facts.ToY);
        }

        private string AssessCharterWorldStep(Snapshot state, Command command, WorldStepFacts facts)
        {
            var attempt = state.CharterAttempt;
            if (attempt == null || attempt.Authority.HeroId != command.Actor || attempt.Returned != null) return null;
            if (IsCharterOutwardStep(state, attempt, command, facts)) {
                string failure = CharterObjectiveReadiness(state, true, out var readiness);
                facts.CharterDeparture = readiness;
                return failure;
            }
            if (!IsCharterReturnStep(state, attempt, command, facts)) return null;
            if (command.Target != "walk") return "CharterReturnRequiresOrdinaryWalk";
            if (attempt.ObjectiveOpen && attempt.Observed != null) return CharterObjectiveReadiness(state, false, out _);
            var authority = attempt.Authority;
            return CharterEgressFailure(state, authority.ApproachX, authority.ApproachY, authority.StageX, authority.StageY);
        }

        private void AttachCharterWorldStep(Snapshot state, Command command, WorldTraversalRecord edge, CharterAttemptReadiness departure)
        {
            var attempt = state.CharterAttempt;
            if (attempt == null || attempt.Authority.HeroId != edge.ActorId || attempt.Returned != null) return;
            var authority = attempt.Authority;
            if (attempt.ObjectiveOpen && attempt.OutboundStarted == null && !edge.Running
                && authority.Outbound(edge.FromX, edge.FromY, edge.ToX, edge.ToY)) {
                ContinueCharterAttempt(state, command);
                state.CharterAttempt = state.CharterAttempt.Append(AttemptEvent(state, command,
                    CharterAttemptEventKind.OutboundStarted, "CharterActualOutbound"), departure: departure);
                return;
            }
            if (attempt.OutboundArrived != null && attempt.ReturnStarted == null && !edge.Running
                && authority.Return(edge.FromX, edge.FromY, edge.ToX, edge.ToY)) {
                if (attempt.Observed == null) StopCharterObjective(state, command, CharterAttemptEventKind.Aborted, "CharterReturnedWithoutObservation");
                ContinueCharterAttempt(state, command);
                state.CharterAttempt = state.CharterAttempt.Append(AttemptEvent(state, command,
                    CharterAttemptEventKind.ReturnStarted, "CharterActualReturnStarted"));
                return;
            }
            if (attempt.ObjectiveOpen)
                StopCharterObjective(state, command, CharterAttemptEventKind.ScopeLeft, "CharterUnrelatedOrdinaryMovement");
        }

        private string AssessCharterTraversalResume(Snapshot state, WorldTraversalRecord edge)
        {
            var attempt = state.CharterAttempt;
            if (attempt == null || !IsCharterEdge(attempt, edge)) return null;
            return attempt.ObjectiveOpen ? CharterObjectiveReadiness(state, false, out _)
                : CharterEgressFailure(state, edge.FromX, edge.FromY, edge.ToX, edge.ToY);
        }

        private static void ResumeCharterTraversal(Snapshot state, Command cause, WorldTraversalRecord edge)
        {
            var attempt = state.CharterAttempt;
            if (attempt == null || !IsCharterEdge(attempt, edge)) return;
            if (attempt.ObjectiveOpen) ContinueCharterAttempt(state, cause);
            else state.CharterAttempt = attempt.Append(AttemptEvent(state, cause, CharterAttemptEventKind.Continued,
                "CharterExplicitEgressContinuation"));
        }

        private static void CreditCharterMovement(Snapshot state, WorldTraversalRecord edge, RuleTime elapsed)
        {
            var attempt = state.CharterAttempt;
            if (attempt == null || !IsCharterEdge(attempt, edge)) return;
            bool returning = attempt.ReturnStarted?.Revision == edge.StartedRevision;
            state.CharterAttempt = attempt.WithMovementTimes(
                returning ? attempt.OutboundMovingTime : CampGreens.Add(attempt.OutboundMovingTime, elapsed),
                returning ? CampGreens.Add(attempt.ReturnMovingTime, elapsed) : attempt.ReturnMovingTime);
        }

        private static RuleTime? NextCharterAttemptBoundary(Snapshot state)
        {
            var attempt = state.CharterAttempt;
            if (attempt == null || attempt.Returned != null || !attempt.ObjectiveOpen
                && !state.WorldTraversals.Any(x => IsCharterEdge(attempt, x) && x.Status != WorldTraversalStatus.Suspended)) return null;
            RuleTime deadline = attempt.ObjectiveOpen ? state.NextCharterAgreement.Terms.ValidUntil : attempt.Authority.EgressUntil;
            return deadline > state.RuleClock ? deadline : (RuleTime?)null;
        }

        private void ReconcileCharterAttempt(Snapshot state, Command cause, WorldTraversalRecord completedEdge = null)
        {
            var attempt = state.CharterAttempt;
            if (attempt == null || attempt.Returned != null || cause == null) return;
            var agreement = state.NextCharterAgreement;
            bool arrived = completedEdge != null && IsCharterEdge(attempt, completedEdge);
            bool returning = arrived && completedEdge.StartedRevision == attempt.ReturnStarted?.Revision;
            if (attempt.ObjectiveOpen) {
                if (agreement.Withdrawal != null)
                    StopCharterObjective(state, cause, CharterAttemptEventKind.Withdrawn, "CharterAgreementWithdrawn");
                else if (state.RuleClock >= agreement.Terms.ValidUntil)
                    StopCharterObjective(state, cause, CharterAttemptEventKind.Expired, "CharterAgreementExpired");
                else {
                    string authorityFailure = CharterObjectiveAuthorityFailure(state);
                    string blocker = authorityFailure ?? CharterObjectiveReadiness(state, false, out _);
                    if (authorityFailure != null || blocker == "CharterTacticalTransitionRequired" || blocker == "CharterAccessContradicted"
                        || returning && blocker != null)
                        StopCharterObjective(state, cause, CharterAttemptEventKind.Aborted, blocker);
                    else if (attempt.OutboundStarted != null) {
                        var edge = state.WorldTraversals.SingleOrDefault(x => IsCharterEdge(attempt, x));
                        if (blocker != null || edge?.Status == WorldTraversalStatus.Suspended) {
                            SuspendCharterTraversal(state, attempt);
                            if (!attempt.Interrupted)
                                state.CharterAttempt = attempt.Append(AttemptEvent(state, cause, CharterAttemptEventKind.Suspended,
                                    blocker ?? "CharterTraversalSuspended"));
                        }
                    }
                }
            } else {
                var edge = state.WorldTraversals.SingleOrDefault(x => IsCharterEdge(attempt, x));
                if (edge != null && CharterEgressFailure(state, edge.FromX, edge.FromY, edge.ToX, edge.ToY) != null)
                    SuspendCharterTraversal(state, attempt);
            }
            if (arrived) {
                var actor = state.Actors.Single(x => x.Id == completedEdge.ActorId);
                if (actor.X != completedEdge.ToX || actor.Y != completedEdge.ToY) return;
                state.CharterAttempt = state.CharterAttempt.Append(AttemptEvent(state, cause,
                    returning ? CharterAttemptEventKind.Returned : CharterAttemptEventKind.OutboundArrived,
                    returning ? "CharterPhysicalReturn" : "CharterPhysicalOutboundArrival"));
            }
        }
    }
}
#endif
