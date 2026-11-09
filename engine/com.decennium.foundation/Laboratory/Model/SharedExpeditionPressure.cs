#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Numerics;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Finite TEST_ONLY binding for the source-backed FL-08/FL-09 pressure slice.
    /// Route geometry, quality, Risk, mapping and capacity remain owned by the existing route fixture.</summary>
    public sealed class TestOnlyExpeditionPressureFixture
    {
        private readonly string[] safeHavenLocations;
        public string CohortId { get; }
        public string MemberId { get; }
        public int InitialPressure { get; }
        public IReadOnlyList<string> SafeHavenLocations { get; }
        public string Fingerprint { get; }

        public TestOnlyExpeditionPressureFixture(string cohortId, string memberId, int initialPressure,
            IEnumerable<string> safeHavenLocationIds)
        {
            safeHavenLocations = (safeHavenLocationIds ?? Array.Empty<string>()).OrderBy(x => x, StringComparer.Ordinal).ToArray();
            if (!Validation.ValidId(cohortId) || !Validation.ValidId(memberId) || initialPressure < 0 || initialPressure > 6
                || safeHavenLocations.Length == 0 || safeHavenLocations.Length > 32
                || safeHavenLocations.Any(x => !Validation.ValidId(x))
                || safeHavenLocations.Distinct(StringComparer.Ordinal).Count() != safeHavenLocations.Length)
                throw new ArgumentException("Invalid fixed-cohort TEST_ONLY expedition-pressure fixture.");
            CohortId = cohortId; MemberId = memberId; InitialPressure = initialPressure;
            SafeHavenLocations = Array.AsReadOnly(safeHavenLocations);
            Fingerprint = Hash("test-only-expedition-pressure-v1|FL-08|FL-09|TR-13|" + cohortId + "|" + memberId + "|"
                + initialPressure.ToString(CultureInfo.InvariantCulture) + "|" + string.Join(";", safeHavenLocations));
        }

        internal string ValidateRoutes(TestOnlyExpeditionRouteFixture routes)
        {
            if (routes == null) return "PressureRouteFixtureRequired";
            if (!routes.Routes.Any(x => safeHavenLocations.Contains(x.ToLocationId, StringComparer.Ordinal)))
                return "PressureSafeHavenRouteRequired";
            return null;
        }

        internal bool IsSafeHaven(TestOnlyExpeditionRoute route)
            => route != null && safeHavenLocations.Contains(route.ToLocationId, StringComparer.Ordinal);

        internal string BindFingerprint(string worldFingerprint, TestOnlyExpeditionRouteFixture routes)
            => "TEST_ONLY.pressure-world-v1-" + Hash(worldFingerprint + "|" + routes.Fingerprint + "|" + Fingerprint);

        private static string Hash(string value)
        {
            using (var sha = SHA256.Create())
                return string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(value)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionPressureFixture expeditionPressureProfile;

        /// <summary>Opt into the bounded TEST_ONLY FL-08/FL-09 integration on the existing shared
        /// route, attack, clock, RNG and persistence authorities. This first profile supports one
        /// fixed traveler, base route travel, committed melee/ranged attacks, secured-route entry,
        /// finite route obstruction/closure, and authored safe-Haven endpoints.</summary>
        public TestOnlySharedWorldPolicy EnableExpeditionPressure(TestOnlyExpeditionPressureFixture fixture)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (fixture == null || expeditionPressureProfile != null) throw new ArgumentException("Supply one explicit pressure fixture.");
            if (routeTravelFixture == null) throw new InvalidOperationException("ExpeditionPressureRequiresRouteTravel");
            if (routeMotionFixture != null || observationFixture != null || routeReconnaissanceFixture != null
                || routeMappingFixture != null || routeMappingWorkFixture != null)
                throw new InvalidOperationException("ExpeditionPressureRouteCompositionUnsupported");
            if (havenCareProfile != null || moraleRestProfile != null || strainRecoveryProfile != null
                || restDebtProfile != null || dailyProvisioning != null)
                throw new InvalidOperationException("ExpeditionPressureRecoveryCompositionUnsupported");
            string error = fixture.ValidateRoutes(routeTravelFixture);
            if (error != null) throw new InvalidOperationException(error);
            expeditionPressureProfile = fixture;
            bodies.ConfigurePressureMovement(AssessExpeditionPressureMovement,
                IsPressureRetreatDeparture, CompletePressureRetreat);
            ContentFingerprint = fixture.BindFingerprint(ContentFingerprint, routeTravelFixture);
            return this;
        }

        private void InitializeExpeditionPressure(Snapshot s)
        {
            if (expeditionPressureProfile == null) return;
            if (!s.Actors.Any(x => x.Id == expeditionPressureProfile.MemberId))
                throw new InvalidOperationException("PressureCohortMemberMissing");
            s.ExpeditionPressureCohorts = new[] { new ExpeditionPressureCohortRecord(
                expeditionPressureProfile.CohortId, s.ContentFingerprint, routeTravelFixture.Fingerprint,
                expeditionPressureProfile.InitialPressure, new[] { expeditionPressureProfile.MemberId }) };
            s.ExpeditionPressureExposures = Array.Empty<ExpeditionPressureExposureRecord>();
            s.ExpeditionPressureChanges = Array.Empty<ExpeditionPressureChangeRecord>();
            s.ExpeditionPressureCheckpoints = Array.Empty<ExpeditionPressureCheckpointRecord>();
        }

        private string ValidateExpeditionPressureFixtureState(Snapshot s)
        {
            if (expeditionPressureProfile == null)
                return s.ExpeditionPressureCohorts.Length + s.ExpeditionPressureExposures.Length
                    + s.ExpeditionPressureChanges.Length + s.ExpeditionPressureCheckpoints.Length == 0
                    ? null : "PressureFixtureMissing";
            if ((s.SchemaVersion != Snapshot.ExpeditionPressureSchema
                    && s.SchemaVersion != Snapshot.ExpeditionPressureLifecycleSchema
                    && s.SchemaVersion != Snapshot.ExpeditionCampUseSchema
                    && s.SchemaVersion != Snapshot.TemporaryCampConstructionSchema)
                || s.ExpeditionPressureCohorts.Length != 1
                || !s.ExpeditionPressureCohorts[0].SameAs(new ExpeditionPressureCohortRecord(
                    expeditionPressureProfile.CohortId, s.ContentFingerprint, routeTravelFixture.Fingerprint,
                    expeditionPressureProfile.InitialPressure, new[] { expeditionPressureProfile.MemberId })))
                return "PressureProfileMismatch";
            string error = expeditionPressureProfile.ValidateRoutes(routeTravelFixture);
            if (error != null) return error;

            foreach (var exposure in s.ExpeditionPressureExposures)
            {
                var route = routeTravelFixture.Find(exposure.RouteId);
                if (route == null || route.Quality == ExpeditionRouteQuality.Collapsed || route.Risk > 6
                    || route.Mapping == ExpeditionRouteMapping.Unknown) return "InvalidPressureRouteExposure";
            }
            foreach (var checkpoint in s.ExpeditionPressureCheckpoints)
            {
                var route = routeTravelFixture.Find(checkpoint.RouteId);
                if (route == null || checkpoint.RouteFingerprint != routeTravelFixture.Fingerprint
                    || checkpoint.ProfileFingerprint != s.ContentFingerprint
                    || checkpoint.RouteQuality != route.Quality
                    || checkpoint.RiskFloor != (route.Quality == ExpeditionRouteQuality.Secured ? 0 : route.Risk)
                    || checkpoint.RouteProgress > route.LengthProgress
                    || checkpoint.Consequence == ExpeditionPressureConsequenceKind.RouteClosure
                        && checkpoint.RetreatRouteId != route.Id)
                    return "InvalidPressureCheckpointRouteBinding";
            }
            if (s.SchemaVersion == Snapshot.ExpeditionPressureSchema
                && s.ExpeditionPressureExposures.Any(x => x.EndKind == ExpeditionPressureExposureEndKind.RetreatCompleted))
                return "RetreatCompletionRequiresPressureLifecycleSchema";

            if (s.SchemaVersion >= Snapshot.ExpeditionPressureLifecycleSchema)
            {
                var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                    && !x.EndedAt.HasValue);
                if (exposure != null)
                {
                    var route = routeTravelFixture.Find(exposure.RouteId);
                    var actor = s.Actors.Single(x => x.Id == expeditionPressureProfile.MemberId);
                    var closure = ActivePressureRouteClosure(s, exposure);
                    if (closure != null && (!route.Positions.Any(x => x.Progress <= closure.RouteProgress
                        && x.X == actor.X && x.Y == actor.Y)
                        || actor.X == route.ToSiteX && actor.Y == route.ToSiteY))
                        return "InvalidPressureRetreatPosition";
                    var pending = PendingPressureHavenArrival(s, exposure);
                    if (pending != null)
                    {
                        RuleTime? deadline = PendingPressureHavenAdmissionAt(s, exposure);
                        var gate = route.PositionAt(pending.RouteProgress);
                        bool movementSource = gate != null && s.Receipts.Where(r => r.Revision < pending.AppliedRevision)
                            .Any(r => {
                                try {
                                    var command = CommandHistory.Read(r);
                                    return command.Kind == CommandKind.BeginWorldStep
                                        && command.Actor == expeditionPressureProfile.MemberId
                                        && (command.Target == "walk" || command.Target == "run")
                                        && gate.X + command.X == route.ToSiteX && gate.Y + command.Y == route.ToSiteY;
                                } catch (ArgumentException) { return false; }
                            });
                        if (!deadline.HasValue || deadline.Value <= s.RuleClock || gate == null
                            || actor.X != gate.X || actor.Y != gate.Y || !movementSource)
                            return "InvalidPendingPressureHavenArrival";
                    }
                    else if (expeditionPressureProfile.IsSafeHaven(route)
                        && actor.X == route.ToSiteX && actor.Y == route.ToSiteY)
                        return "PressureArrivalMustCloseExposure";
                }
            }

            foreach (var routeGroup in s.RouteTravels.GroupBy(x => x.RouteId, StringComparer.Ordinal))
            {
                var route = routeTravelFixture.Find(routeGroup.Key);
                if (route == null) return "InvalidPressureRouteTravel";
                if (route.Risk > 6) return "PressureRiskFloorUnsupported";
            }
            return null;
        }

        private void RecordPressureRouteStart(Snapshot s, TestOnlyExpeditionRoute route, Command command)
        {
            if (expeditionPressureProfile == null || command.Actor != expeditionPressureProfile.MemberId) return;
            var active = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && !x.EndedAt.HasValue);
            if (active != null && active.RouteId == route.Id) return;
            if (active != null) SetPressureExposure(s, active.End(s.RuleClock, s.Revision + 1,
                ExpeditionPressureExposureEndKind.RouteTransition));
            long watch = EventWatchIndex(s.RuleClock);
            string exposureId = "pressure-exposure-" + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
            var exposure = new ExpeditionPressureExposureRecord(exposureId, expeditionPressureProfile.CohortId,
                route.Id, s.Revision + 1, s.RuleClock);
            s.ExpeditionPressureExposures = s.ExpeditionPressureExposures.Concat(new[] { exposure }).ToArray();
            if (route.Quality == ExpeditionRouteQuality.Secured)
            {
                int existingReductions = s.ExpeditionPressureChanges.Count(x => x.CohortId == exposure.CohortId
                    && x.WatchIndex == watch && x.Kind == ExpeditionPressureChangeKind.SecuredRouteEntry);
                if (existingReductions < 2)
                {
                    var receipt = s.Receipts.SingleOrDefault(x => x.Revision == command.ExpectedRevision + 1);
                    string sourceId = receipt?.Id ?? command.Id;
                    AddPressureChange(s, exposure, ExpeditionPressureChangeKind.SecuredRouteEntry,
                        sourceId, command.ExpectedRevision + 1, s.RuleClock, watch);
                }
            }
        }

        private string PressureRouteStartFailure(Snapshot s, TestOnlyExpeditionRoute route)
        {
            if (expeditionPressureProfile == null) return null;
            var active = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && !x.EndedAt.HasValue);
            if (active != null && active.RouteId == route.Id) return null;
            long watch = EventWatchIndex(s.RuleClock);
            if (s.ExpeditionPressureCheckpoints.Any(x => x.CohortId == expeditionPressureProfile.CohortId
                && x.WatchIndex == watch)) return "ExpeditionPressureSameWatchRouteReentryUnsupported";
            return s.ExpeditionPressureExposures.Any(x => x.RouteId == route.Id
                && x.CohortId == expeditionPressureProfile.CohortId && EventWatchIndex(x.StartedAt) == watch)
                ? "ExpeditionPressureSameWatchRouteReentryUnsupported" : null;
        }

        private static string PressureRouteAccessFailure(Snapshot s, TestOnlyExpeditionRoute route)
        {
            var latest = s.ExpeditionPressureCheckpoints.Where(x => x.AffectedRouteId == route.Id)
                .OrderByDescending(x => x.AppliedRevision).FirstOrDefault();
            if (latest?.Consequence == ExpeditionPressureConsequenceKind.RouteClosure) return "RouteClosedByPressure";
            if (latest?.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction
                && latest.ConsequenceEndsAt > s.RuleClock) return "RouteObstructedByPressure";
            return null;
        }

        private void RecordPressureCombatSources(Snapshot s, string[] oldMelee, string[] oldRanged)
        {
            if (expeditionPressureProfile == null) return;
            var members = new HashSet<string>(new[] { expeditionPressureProfile.MemberId }, StringComparer.Ordinal);
            long resolvingRevision = s.Revision + 1;
            var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && (!x.EndedAt.HasValue || x.EndRevision == resolvingRevision && x.EndedAt.Value == s.RuleClock
                    && x.EndKind == ExpeditionPressureExposureEndKind.RetreatCompleted));
            if (exposure == null) return;
            var attacks = s.MeleeAttacks.Where(x => !oldMelee.Contains(x.Id, StringComparer.Ordinal))
                .Select(x => new { x.Id, x.Revision, x.AttackerId, x.TargetId, x.At, x.Opportunity })
                .Concat(s.RangedAttacks.Where(x => !oldRanged.Contains(x.Id, StringComparer.Ordinal))
                    .Select(x => new { x.Id, x.Revision, x.AttackerId, x.TargetId, x.At, Opportunity = false }))
                .OrderBy(x => x.Revision).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            foreach (var attack in attacks)
            {
                if (!members.Contains(attack.AttackerId) && !members.Contains(attack.TargetId)) continue;
                if (!ExpeditionPressureRules.AttackWithinExposure(s, exposure, attack.AttackerId,
                    attack.TargetId, attack.Revision, attack.At, attack.Opportunity)) continue;
                if (s.ExpeditionPressureChanges.Any(x => x.Kind == ExpeditionPressureChangeKind.OpenCombat
                    && x.SourceId == attack.Id)) continue;
                AddPressureChange(s, exposure, ExpeditionPressureChangeKind.OpenCombat, attack.Id,
                    attack.Revision, attack.At, EventWatchIndex(attack.At));
            }
        }

        private static long EventWatchIndex(RuleTime at)
            => checked((long)(new BigInteger(at.Numerator) / at.Denominator / ExpeditionPressureRules.WatchSeconds));

        private static void AddPressureChange(Snapshot s, ExpeditionPressureExposureRecord exposure,
            ExpeditionPressureChangeKind kind, string sourceId, long sourceRevision, RuleTime at, long watch)
        {
            string id = PressureChangeId(kind, sourceId);
            if (s.ExpeditionPressureChanges.Any(x => x.Id == id)) return;
            var change = new ExpeditionPressureChangeRecord(id, exposure.CohortId, exposure.Id, exposure.RouteId,
                watch, kind, sourceId, sourceRevision, at);
            s.ExpeditionPressureChanges = s.ExpeditionPressureChanges.Concat(new[] { change }).ToArray();
        }

        private static string PressureChangeId(ExpeditionPressureChangeKind kind, string sourceId)
        {
            using (var sha = SHA256.Create())
                return "pressure-change-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(((int)kind).ToString(CultureInfo.InvariantCulture)
                    + "|" + sourceId)).Take(24).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }

        private static void SetPressureExposure(Snapshot s, ExpeditionPressureExposureRecord value)
            => s.ExpeditionPressureExposures = s.ExpeditionPressureExposures.Select(x => x.Id == value.Id ? value : x).ToArray();

        private ExpeditionPressureCheckpointRecord PendingPressureHavenArrival(Snapshot s,
            ExpeditionPressureExposureRecord exposure)
        {
            if (s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema || exposure == null) return null;
            var arrival = s.ExpeditionPressureCheckpoints.Where(x => x.CohortId == exposure.CohortId
                && x.RouteId == exposure.RouteId
                && (x.Reason == ExpeditionPressureSettlementReason.HavenArrival
                    || x.Reason == ExpeditionPressureSettlementReason.HavenArrivalAtWatchEnd)
                && x.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction)
                .OrderByDescending(x => x.AppliedRevision).FirstOrDefault();
            if (arrival == null || s.ExpeditionPressureCheckpoints.Any(x => x.CohortId == exposure.CohortId
                && x.RouteId == exposure.RouteId && x.AppliedRevision > arrival.AppliedRevision
                && x.Consequence == ExpeditionPressureConsequenceKind.RouteClosure)) return null;
            return arrival;
        }

        private RuleTime? PendingPressureHavenAdmissionAt(Snapshot s, ExpeditionPressureExposureRecord exposure)
        {
            var arrival = PendingPressureHavenArrival(s, exposure);
            if (arrival == null) return null;
            return s.ExpeditionPressureCheckpoints.Where(x => x.CohortId == exposure.CohortId
                    && x.RouteId == exposure.RouteId && x.AppliedRevision >= arrival.AppliedRevision
                    && x.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction
                    && x.ConsequenceEndsAt.HasValue)
                .OrderByDescending(x => x.ConsequenceEndsAt.Value).Select(x => x.ConsequenceEndsAt).First();
        }

        private ExpeditionPressureCheckpointRecord ActivePressureRouteClosure(Snapshot s,
            ExpeditionPressureExposureRecord exposure)
            => exposure == null ? null : s.ExpeditionPressureCheckpoints.Where(x => x.CohortId == exposure.CohortId
                && x.RouteId == exposure.RouteId && x.AppliedRevision >= exposure.StartedRevision
                && x.Consequence == ExpeditionPressureConsequenceKind.RouteClosure)
                .OrderByDescending(x => x.AppliedRevision).FirstOrDefault();

        private bool IsPressureHavenArrival(Snapshot s, WorldTraversalRecord edge)
        {
            if (s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema || expeditionPressureProfile == null
                || edge == null || edge.ActorId != expeditionPressureProfile.MemberId) return false;
            var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && !x.EndedAt.HasValue);
            var route = exposure == null ? null : routeTravelFixture.Find(exposure.RouteId);
            return route != null && expeditionPressureProfile.IsSafeHaven(route)
                && edge.ToX == route.ToSiteX && edge.ToY == route.ToSiteY;
        }

        private bool IsPressureRetreatDeparture(Snapshot s, string actorId, int fromX, int fromY, int toX, int toY)
        {
            if (s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema || expeditionPressureProfile == null
                || actorId != expeditionPressureProfile.MemberId) return false;
            var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && !x.EndedAt.HasValue);
            var closure = ActivePressureRouteClosure(s, exposure);
            var route = closure == null ? null : routeTravelFixture.Find(closure.RouteId);
            return route != null && fromX == route.FromX && fromY == route.FromY
                && !route.Positions.Any(x => x.X == toX && x.Y == toY)
                && !(toX == route.ToSiteX && toY == route.ToSiteY);
        }

        private void CompletePressureRetreat(Snapshot s, string actorId, RuleTime at, long revision)
        {
            if (expeditionPressureProfile == null || actorId != expeditionPressureProfile.MemberId
                || s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema) return;
            var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && !x.EndedAt.HasValue);
            if (exposure != null)
                SetPressureExposure(s, exposure.End(at, revision, ExpeditionPressureExposureEndKind.RetreatCompleted));
        }

        private RuleTime? NextExpeditionPressureBoundary(Snapshot s)
        {
            var exposure = expeditionPressureProfile == null ? null
                : s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                    && !x.EndedAt.HasValue);
            if (exposure == null) return null;
            BigInteger denominator = new BigInteger(s.RuleClock.Denominator);
            BigInteger watchUnits = denominator * ExpeditionPressureRules.WatchSeconds;
            BigInteger index = new BigInteger(s.RuleClock.Numerator) / watchUnits;
            BigInteger boundaryNumerator = (index + BigInteger.One) * watchUnits;
            if (boundaryNumerator > long.MaxValue) throw new OverflowException("Expedition pressure Watch boundary overflowed.");
            RuleTime boundary = new RuleTime((long)boundaryNumerator, s.RuleClock.Denominator);
            var admission = PendingPressureHavenAdmissionAt(s, exposure);
            return admission.HasValue && admission.Value > s.RuleClock && admission.Value < boundary
                ? admission : boundary;
        }

        private static bool IsPressureWatchEnd(RuleTime at)
            => new BigInteger(at.Numerator) % (new BigInteger(at.Denominator) * ExpeditionPressureRules.WatchSeconds) == 0;

        private static long PressureWatchAtEnd(RuleTime at)
        {
            BigInteger units = new BigInteger(at.Numerator) / (new BigInteger(at.Denominator) * ExpeditionPressureRules.WatchSeconds);
            return checked((long)(units - BigInteger.One));
        }

        private string ProcessExpeditionPressureBoundary(Snapshot s, RuleTime at, Command initiating,
            WorldTraversalRecord stagedArrival = null, bool completedRetreat = false)
        {
            if (expeditionPressureProfile == null) return null;
            if (s.RuleClock != at) throw new InvalidOperationException("PressureBoundaryMustUseSharedClock.");
            var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && !x.EndedAt.HasValue);
            if (exposure == null) return null;
            var route = routeTravelFixture.Find(exposure.RouteId);
            var actor = s.Actors.Single(x => x.Id == expeditionPressureProfile.MemberId);
            bool stagedHavenArrival = IsPressureHavenArrival(s, stagedArrival);
            bool safeArrival = stagedHavenArrival || expeditionPressureProfile.IsSafeHaven(route)
                && actor.X == route.ToSiteX && actor.Y == route.ToSiteY;
            var pendingAdmission = PendingPressureHavenAdmissionAt(s, exposure);
            bool pendingAdmissionDue = s.SchemaVersion >= Snapshot.ExpeditionPressureLifecycleSchema
                && pendingAdmission.HasValue && pendingAdmission.Value <= at;
            bool watchEnd = IsPressureWatchEnd(at);
            long watch = watchEnd ? PressureWatchAtEnd(at) : EventWatchIndex(at);
            if (safeArrival || watchEnd)
            {
                if (exposure.StartedAt < at && (stagedHavenArrival || watchEnd || s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema)
                    && !s.ExpeditionPressureCheckpoints.Any(x => x.CohortId == exposure.CohortId
                    && x.WatchIndex == watch))
                {
                    bool havenArrivalSettlement = stagedHavenArrival
                        || s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema && safeArrival;
                    var reason = havenArrivalSettlement
                        ? watchEnd ? ExpeditionPressureSettlementReason.HavenArrivalAtWatchEnd
                            : ExpeditionPressureSettlementReason.HavenArrival
                        : watchEnd ? ExpeditionPressureSettlementReason.WatchEnd
                            : ExpeditionPressureSettlementReason.HavenArrival;
                    string error = ResolveExpeditionPressureCheckpoint(s, exposure, route, watch, at, reason, initiating);
                    if (error != null) return error;
                }
                if (s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema && safeArrival)
                {
                    var current = s.ExpeditionPressureExposures.SingleOrDefault(x => x.Id == exposure.Id);
                    if (current != null && !current.EndedAt.HasValue)
                        SetPressureExposure(s, current.End(at, s.Revision + 1,
                            ExpeditionPressureExposureEndKind.SafeHavenArrival));
                }
            }
            if (s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema) return null;
            exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.Id == exposure.Id && !x.EndedAt.HasValue);
            if (exposure == null) return null;
            if (completedRetreat)
            {
                CompletePressureRetreat(s, expeditionPressureProfile.MemberId, at, s.Revision + 1);
                return null;
            }
            if (!safeArrival && !pendingAdmissionDue) return null;
            if (ActivePressureRouteClosure(s, exposure) != null) return null;
            pendingAdmission = PendingPressureHavenAdmissionAt(s, exposure);
            if (pendingAdmission.HasValue && pendingAdmission.Value > at) return null;
            if (safeArrival || pendingAdmissionDue)
            {
                actor.X = route.ToSiteX; actor.Y = route.ToSiteY;
                s.Clubs = s.Clubs.Select(c => c.HeldBy == actor.Id
                    ? new ClubInstance(c.Id, c.ProfileId, c.OwnerId, c.CustodianId, c.HeldBy, actor.X, actor.Y) : c).ToArray();
                SetPressureExposure(s, exposure.End(at, s.Revision + 1,
                    ExpeditionPressureExposureEndKind.SafeHavenArrival));
            }
            return null;
        }

        private string ResolveExpeditionPressureCheckpoint(Snapshot s, ExpeditionPressureExposureRecord exposure,
            TestOnlyExpeditionRoute route, long watch, RuleTime at, ExpeditionPressureSettlementReason reason, Command initiating)
        {
            if (initiating == null || route == null) return "PressureCheckpointContextUnsupported";
            var travel = LatestRouteTravel(s, route.Id, expeditionPressureProfile.MemberId);
            if (travel == null) return "PressureRouteProgressMissing";
            string campEvidenceError = RecordCampPressureEvidence(s, exposure, watch, at);
            if (campEvidenceError != null) return campEvidenceError;
            int before = ExpeditionPressureRules.CurrentAt(s, exposure.CohortId, s.Revision + 1, at);
            var causes = s.ExpeditionPressureChanges.Where(x => x.CohortId == exposure.CohortId
                && x.WatchIndex == watch && (x.Kind == ExpeditionPressureChangeKind.OpenCombat
                    || s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema
                        && x.Kind == ExpeditionPressureChangeKind.ExposedCampUse)
                && x.SourceRevision <= s.Revision + 1 && x.At <= at)
                .OrderBy(x => x.SourceRevision).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            var reductions = s.ExpeditionPressureChanges.Where(x => x.CohortId == exposure.CohortId
                && x.WatchIndex == watch && (x.Kind == ExpeditionPressureChangeKind.SecuredRouteEntry
                    || s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema
                        && x.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow)
                && x.SourceRevision <= s.Revision + 1 && x.At <= at)
                .OrderBy(x => x.SourceRevision).ThenBy(x => x.Id, StringComparer.Ordinal).Take(2).ToArray();
            int floor = route.Quality == ExpeditionRouteQuality.Secured ? 0 : route.Risk;
            int stored = ExpeditionPressureRules.Settle(before,
                ExpeditionPressureRules.IncreaseCategoryCount(causes), reductions.Length, floor);
            bool watchEnd = IsPressureWatchEnd(at);
            bool campCheckpoint = s.SchemaVersion >= Snapshot.ExpeditionCampUseSchema && watchEnd
                && s.ExpeditionCampActivities.Any(x => x.CohortId == exposure.CohortId
                    && x.Kind == ExpeditionCampActivityKind.Use && x.StartedAt < at
                    && (!x.EndedAt.HasValue || x.EndedAt.Value >= at)
                    && x.ExposureId == exposure.Id && x.CampId == expeditionCampSiteProfile.Id
                    && (!exposure.EndedAt.HasValue || exposure.EndedAt.Value >= at));
            var context = campCheckpoint ? ExpeditionPressureCheckpointContext.Camp
                : ExpeditionPressureCheckpointContext.Route;
            int effective = ExpeditionPressureRules.EffectiveForCheckpoint(stored, route.Quality, context);
            uint randomBefore = s.RandomState, randomAfter = randomBefore;
            long words = 0; int natural = 0, total = 0;
            if (effective > 0 && effective < 6)
            {
                var draw = DiceStream.Draw(randomBefore, 6);
                natural = total = draw.Value + 1; randomAfter = draw.NextState; words = draw.WordsConsumed;
                s.RandomState = randomAfter;
            }
            var outcome = ExpeditionPressureRules.Classify(effective, natural, total, false);
            var consequence = outcome == ExpeditionPressureOutcome.None ? ExpeditionPressureConsequenceKind.None
                : outcome == ExpeditionPressureOutcome.Severe ? ExpeditionPressureConsequenceKind.RouteClosure
                : ExpeditionPressureConsequenceKind.TimedRouteObstruction;
            RuleTime? ends = outcome == ExpeditionPressureOutcome.Minor ? CampGreens.Add(at, new RuleTime(900))
                : outcome == ExpeditionPressureOutcome.Standard ? CampGreens.Add(at, new RuleTime(3600)) : (RuleTime?)null;
            var checkpoint = new ExpeditionPressureCheckpointRecord("pressure-check-" + watch.ToString(CultureInfo.InvariantCulture),
                exposure.CohortId, watch, at, reason, route.Id, routeTravelFixture.Fingerprint, s.ContentFingerprint,
                route.Quality, floor, before, stored, effective, causes.Select(x => x.Id), reductions.Select(x => x.Id),
                natural, total, false, randomBefore, randomAfter, words, outcome, consequence,
                consequence == ExpeditionPressureConsequenceKind.None ? "" : route.Id,
                consequence == ExpeditionPressureConsequenceKind.RouteClosure ? route.Id : "",
                travel.Progress, ends, initiating.Id, s.Revision + 1, context);
            s.ExpeditionPressureCheckpoints = s.ExpeditionPressureCheckpoints.Concat(new[] { checkpoint }).ToArray();
            if (consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction)
            {
                var activeTravel = s.RouteTravels.SingleOrDefault(x => x.StartedRevision == travel.StartedRevision
                    && (x.Status == ExpeditionRouteTravelStatus.Moving || x.Status == ExpeditionRouteTravelStatus.Paused));
                if (activeTravel?.Status == ExpeditionRouteTravelStatus.Moving)
                    SetRouteTravel(s, activeTravel.With(activeTravel.NominalEffort, ExpeditionRouteTravelStatus.Paused));
            }
            else if (consequence == ExpeditionPressureConsequenceKind.RouteClosure)
            {
                var activeTravel = s.RouteTravels.SingleOrDefault(x => x.StartedRevision == travel.StartedRevision
                    && (x.Status == ExpeditionRouteTravelStatus.Moving || x.Status == ExpeditionRouteTravelStatus.Paused));
                if (activeTravel != null)
                {
                    SetRouteTravel(s, activeTravel.With(activeTravel.NominalEffort, ExpeditionRouteTravelStatus.Terminated));
                    s.RouteTravelSpatial = s.RouteTravelSpatial.Where(x => x.TravelStartedRevision != activeTravel.StartedRevision).ToArray();
                }
                if (s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema)
                {
                    var current = s.ExpeditionPressureExposures.SingleOrDefault(x => x.Id == exposure.Id);
                    if (current != null && !current.EndedAt.HasValue)
                        SetPressureExposure(s, current.End(at, s.Revision + 1, ExpeditionPressureExposureEndKind.SevereClosure));
                }
            }
            return null;
        }

        private string AssessLegacyExpeditionPressureWorldStep(Snapshot s, string actorId, int toX, int toY)
        {
            if (expeditionPressureProfile == null || actorId != expeditionPressureProfile.MemberId) return null;
            var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && !x.EndedAt.HasValue);
            if (exposure != null)
            {
                var route = routeTravelFixture.Find(exposure.RouteId);
                return expeditionPressureProfile.IsSafeHaven(route) && toX == route.ToSiteX && toY == route.ToSiteY
                    ? null : "ExpeditionPressureRouteDepartureUnsupported";
            }
            var closure = s.ExpeditionPressureCheckpoints.Where(x => x.CohortId == expeditionPressureProfile.CohortId
                && x.Consequence == ExpeditionPressureConsequenceKind.RouteClosure)
                .OrderByDescending(x => x.AppliedRevision).FirstOrDefault();
            if (closure == null) return null;
            var closedRoute = routeTravelFixture.Find(closure.AffectedRouteId);
            if (closedRoute == null) return "PressureRetreatRouteMissing";
            var actor = s.Actors.Single(x => x.Id == actorId);
            if (actor.X == closedRoute.FromX && actor.Y == closedRoute.FromY) return null;
            var current = closedRoute.Positions.Where(x => x.Progress <= closure.RouteProgress
                && x.X == actor.X && x.Y == actor.Y).OrderBy(x => x.Progress).LastOrDefault();
            if (current == null) return "PressureRetreatPositionUnsupported";
            var previous = closedRoute.Positions.Where(x => x.Progress < current.Progress).OrderBy(x => x.Progress).LastOrDefault();
            if (previous == null) return "PressureRetreatPositionUnsupported";
            return toX == previous.X && toY == previous.Y ? null : "PressureRetreatMustFollowClosedRoute";
        }

        private bool IsClosedPressureRouteCell(TestOnlyExpeditionRoute route, int x, int y)
            => route.Positions.Any(p => p.X == x && p.Y == y) || route.ToSiteX == x && route.ToSiteY == y;

        private string AssessExpeditionPressureMovement(Snapshot s, string actorId, int fromX, int fromY,
            int toX, int toY, bool tactical)
        {
            if (expeditionPressureProfile == null || actorId != expeditionPressureProfile.MemberId) return null;
            if (s.SchemaVersion < Snapshot.ExpeditionPressureLifecycleSchema)
                return tactical ? null : AssessLegacyExpeditionPressureWorldStep(s, actorId, toX, toY);
            var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == expeditionPressureProfile.CohortId
                && !x.EndedAt.HasValue);
            if (exposure == null) return null;
            var route = routeTravelFixture.Find(exposure.RouteId);
            var closure = ActivePressureRouteClosure(s, exposure);
            if (closure != null)
            {
                var closedRoute = routeTravelFixture.Find(closure.RouteId);
                if (closedRoute == null) return "PressureRetreatRouteMissing";
                if (fromX == closedRoute.FromX && fromY == closedRoute.FromY)
                    return IsClosedPressureRouteCell(closedRoute, toX, toY)
                        ? "PressureRetreatMustFollowClosedRoute" : null;
                var current = closedRoute.Positions.Where(x => x.Progress <= closure.RouteProgress
                    && x.X == fromX && x.Y == fromY).OrderBy(x => x.Progress).LastOrDefault();
                if (current == null) return "PressureRetreatPositionUnsupported";
                var previous = closedRoute.Positions.Where(x => x.Progress < current.Progress)
                    .OrderBy(x => x.Progress).LastOrDefault();
                if (previous == null) return "PressureRetreatPositionUnsupported";
                return toX == previous.X && toY == previous.Y ? null : "PressureRetreatMustFollowClosedRoute";
            }
            if (tactical) return "PressureTacticalMovementUnsupported";
            if (!expeditionPressureProfile.IsSafeHaven(route) || toX != route.ToSiteX || toY != route.ToSiteY)
                return "ExpeditionPressureRouteDepartureUnsupported";
            return PendingPressureHavenArrival(s, exposure) == null ? null : "PressureHavenAdmissionPending";
        }
    }

}
#endif
