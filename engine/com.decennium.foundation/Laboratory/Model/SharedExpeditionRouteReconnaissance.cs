#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit TEST_ONLY evidence basis for a stationary route-mouth inspection. The
    /// authored facts and target are content, while sight, actor conditions and route geometry
    /// are checked against the live shared snapshot.</summary>
    public sealed class TestOnlyRouteReconnaissanceInspectionProfile
    {
        private const string VisualMethodId = "visual-route-mouth-survey";
        private const string ObservedFactsId = "visible-full-route-and-authored-tread";
        private const string BasisId = "clear-visible-walkable-path-establishes-feasibility";

        public string Id { get; }
        public string RouteId { get; }
        public string MethodId => VisualMethodId;
        public string AvailableFactsId => ObservedFactsId;
        public string FeasibilityBasisId => BasisId;
        public int TargetX { get; }
        public int TargetY { get; }
        public string Fingerprint { get; }

        public TestOnlyRouteReconnaissanceInspectionProfile(string id, string routeId, int targetX, int targetY)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(routeId) || targetX < 0 || targetY < 0)
                throw new ArgumentException("Invalid TEST_ONLY reconnaissance inspection profile.");
            Id = id; RouteId = routeId; TargetX = targetX; TargetY = targetY;
            string canonical = string.Join("|", new[] { Id, RouteId, MethodId, AvailableFactsId,
                FeasibilityBasisId, "requires-live-sight-and-walkable-authored-route-v1",
                TargetX.ToString(CultureInfo.InvariantCulture), TargetY.ToString(CultureInfo.InvariantCulture) });
            using (var sha = SHA256.Create()) Fingerprint = "TEST_ONLY.route-inspection-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(canonical))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }

        internal bool Matches(TestOnlyExpeditionRoute route)
        {
            var endpoint = route?.PositionAt(route.LengthProgress);
            return route != null && route.Id == RouteId && endpoint != null
                && endpoint.X == TargetX && endpoint.Y == TargetY;
        }

        internal string Canonical => string.Join("|", new[] { Id, RouteId, MethodId, AvailableFactsId,
            FeasibilityBasisId, TargetX.ToString(CultureInfo.InvariantCulture),
            TargetY.ToString(CultureInfo.InvariantCulture), Fingerprint });
    }

    /// <summary>Explicit TEST_ONLY route-tier DC. It supplies no route access or result.</summary>
    public sealed class TestOnlyRouteReconnaissanceTaskProfile
    {
        public string RouteId { get; }
        public int Tier { get; }
        public TestOnlyRouteReconnaissanceInspectionProfile Inspection { get; }
        public int Dc => StandardDc(Tier);

        public TestOnlyRouteReconnaissanceTaskProfile(string routeId, int tier,
            TestOnlyRouteReconnaissanceInspectionProfile inspection)
        {
            if (!Validation.ValidId(routeId) || tier < 1 || tier > 6 || inspection == null
                || inspection.RouteId != routeId)
                throw new ArgumentException("Invalid route-tier reconnaissance profile.");
            RouteId = routeId; Tier = tier; Inspection = inspection;
        }

        private static int StandardDc(int tier)
        {
            switch (tier)
            {
                case 1: return 12;
                case 2: return 13;
                case 3: return 15;
                case 4: return 16;
                case 5: return 18;
                case 6: return 19;
                default: throw new ArgumentOutOfRangeException(nameof(tier));
            }
        }

        internal string Canonical => RouteId + "|tier=" + Tier.ToString(CultureInfo.InvariantCulture)
            + "|dc=" + Dc.ToString(CultureInfo.InvariantCulture) + "|inspection=" + Inspection.Canonical;
    }

    /// <summary>TEST_ONLY character-sheet Survival training fact for a route task.</summary>
    public sealed class TestOnlyRouteReconnaissanceSkillFact
    {
        public string ActorId { get; }
        public int ProficiencyRank { get; }

        public TestOnlyRouteReconnaissanceSkillFact(string actorId, int proficiencyRank)
        {
            if (!Validation.ValidId(actorId) || proficiencyRank < 0 || proficiencyRank > 2)
                throw new ArgumentException("Invalid TEST_ONLY Survival training fact.");
            ActorId = actorId; ProficiencyRank = proficiencyRank;
        }

        internal string Canonical => ActorId + "|survival|" + ProficiencyRank.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>One finite, physically authored, risk-free unknown route per fixture. Recon is a
    /// stationary pre-travel task at the accessible route mouth; it is not FL-10's concurrent
    /// moving-scout procedure. The route remains inaccessible until the actual check succeeds.</summary>
    public sealed class TestOnlyExpeditionRouteReconnaissanceFixture
    {
        private const string PlayerBookSha256 = "4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480";
        private readonly TestOnlyRouteReconnaissanceTaskProfile[] tasks;
        private readonly TestOnlyRouteReconnaissanceSkillFact[] skills;
        public string RouteFingerprint { get; }
        public string Fingerprint { get; }
        public System.Collections.Generic.IReadOnlyList<TestOnlyRouteReconnaissanceTaskProfile> Tasks { get; }
        public System.Collections.Generic.IReadOnlyList<TestOnlyRouteReconnaissanceSkillFact> Skills { get; }
        public const int RequiredWorkSeconds = 480 * 60;
        public const string SkillId = "survival";
        public const int WisdomAbilityIndex = 4;

        public TestOnlyExpeditionRouteReconnaissanceFixture(TestOnlyExpeditionRouteFixture routes,
            System.Collections.Generic.IEnumerable<TestOnlyRouteReconnaissanceTaskProfile> tasks,
            System.Collections.Generic.IEnumerable<TestOnlyRouteReconnaissanceSkillFact> skills = null)
        {
            if (routes == null || tasks == null) throw new ArgumentNullException(routes == null ? nameof(routes) : nameof(tasks));
            this.tasks = tasks.ToArray();
            this.skills = (skills ?? Array.Empty<TestOnlyRouteReconnaissanceSkillFact>()).ToArray();
            if (this.tasks.Length < 1 || this.tasks.Length > ExpeditionRouteReconnaissanceValidation.MaxSegments
                || this.tasks.Any(x => x == null)
                || this.tasks.Select(x => x.RouteId).Distinct(StringComparer.Ordinal).Count() != this.tasks.Length
                || this.tasks.Any(x => !EligibleRoute(routes.Find(x.RouteId))
                    || !x.Inspection.Matches(routes.Find(x.RouteId)))
                || this.skills.Any(x => x == null)
                || this.skills.Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count() != this.skills.Length)
                throw new ArgumentException("Invalid finite route reconnaissance fixture.");
            RouteFingerprint = routes.Fingerprint;
            Array.Sort(this.tasks, (a, b) => StringComparer.Ordinal.Compare(a.RouteId, b.RouteId));
            Array.Sort(this.skills, (a, b) => StringComparer.Ordinal.Compare(a.ActorId, b.ActorId));
            Tasks = Array.AsReadOnly(this.tasks); Skills = Array.AsReadOnly(this.skills);
            string key = "ex60-exact-2026-11-07|FL-02/03/08/10|EX02-08|player-book-sha256=" + PlayerBookSha256
                + "|singleton-cohort|pretravel-stationary-mouth-task|480-active-minutes|wisdom-survival|route-tier-standard-dc"
                + "|success-unknown-base-one-plus-one-progress|critical-both-with-pressure-zero-floor|no-synthetic-mapping"
                + "|risk-zero-secured-route-only|visual-mouth-survey-requires-current-sight-and-walkable-route|"
                + "route-travel-remains-position-and-time-authority|no-moving-scout-convoy-overlap|"
                + RouteFingerprint + "|" + string.Join(";", this.tasks.Select(x => x.Canonical)) + "|"
                + string.Join(";", this.skills.Select(x => x.Canonical));
            using (var sha = SHA256.Create()) Fingerprint = "TEST_ONLY.route-recon-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }

        private static bool EligibleRoute(TestOnlyExpeditionRoute route)
            => route != null && route.Mapping == ExpeditionRouteMapping.Unknown && route.Risk == 0
                && route.Quality == ExpeditionRouteQuality.Secured && route.LengthProgress == new RuleQuantity(2)
                && route.PositionAt(default(RuleQuantity)) != null
                && route.PositionAt(default(RuleQuantity)).X == route.FromX
                && route.PositionAt(default(RuleQuantity)).Y == route.FromY
                && route.NextPositionAfter(default(RuleQuantity)) != null
                && route.PositionAt(new RuleQuantity(2)) != null;

        internal TestOnlyRouteReconnaissanceTaskProfile Find(string routeId)
            => tasks.SingleOrDefault(x => x.RouteId == routeId);

        internal string ValidateRoutes(TestOnlyExpeditionRouteFixture routes)
            => routes != null && routes.Fingerprint == RouteFingerprint
                && tasks.All(x => EligibleRoute(routes.Find(x.RouteId))
                    && x.Inspection.Matches(routes.Find(x.RouteId))) ? null : "RouteReconnaissanceFixtureMismatch";

        internal string ValidateBindings(Snapshot s)
            => s == null || skills.Any(x => !s.Actors.Any(a => a.Id == x.ActorId))
                ? "RouteReconnaissanceSkillActorMissing" : null;

        internal void Initialize(Snapshot s)
        {
            if (!s.TacticalAllies.Any(x => x.Includes(TestOnlyPolicy.ActorId)
                    && x.Other(TestOnlyPolicy.ActorId) == TestOnlyPolicy.CompanionId))
                s.TacticalAllies = s.TacticalAllies.Concat(new[] {
                    new TacticalAllyRecord(TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId) }).ToArray();
            var fixtureActors = new System.Collections.Generic.HashSet<string>(skills.Select(x => x.ActorId), StringComparer.Ordinal);
            s.SkillTraining = s.SkillTraining.Where(x => x.SkillId != SkillId || !fixtureActors.Contains(x.ActorId))
                .Concat(skills.Where(x => x.ProficiencyRank > 0)
                    .Select(x => new SkillTrainingRecord(x.ActorId, SkillId, x.ProficiencyRank))).ToArray();
            s.RouteSegments = Array.Empty<ExpeditionRouteSegmentRecord>();
            s.RouteReconnaissanceAttempts = Array.Empty<ExpeditionRouteReconnaissanceAttemptRecord>();
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionRouteReconnaissanceFixture routeReconnaissanceFixture;

        /// <summary>Opts a finite TEST_ONLY world into pre-travel reconnaissance. Route travel
        /// remains the sole authority for passage, position, effort and elapsed time.</summary>
        public TestOnlySharedWorldPolicy EnableRouteReconnaissance(TestOnlyExpeditionRouteReconnaissanceFixture fixture)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (routeTravelFixture == null || routeMotionFixture == null || observationFixture == null
                || fixture == null || routeReconnaissanceFixture != null
                || routeMappingFixture != null || routeMappingWorkFixture != null || readyActionEnabled
                || cacheExcavationEnabled || dodgeActionEnabled || huntingTrapFixture != null)
                throw new ArgumentException("Route reconnaissance requires one unlayered route-travel TEST_ONLY profile.");
            string error = fixture.ValidateRoutes(routeTravelFixture);
            if (error != null) throw new ArgumentException(error, nameof(fixture));
            routeReconnaissanceFixture = fixture;
            using (var sha = SHA256.Create()) ContentFingerprint = "TEST_ONLY.route-recon-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(ContentFingerprint + "|" + fixture.Fingerprint))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private static bool RouteReconnaissanceCommand(CommandKind kind)
            => kind == CommandKind.StartRouteReconnaissance || kind == CommandKind.PauseRouteReconnaissance
                || kind == CommandKind.ResumeRouteReconnaissance;

        private bool RouteReconnaissanceSelected(Snapshot s)
            => routeReconnaissanceFixture != null && s.SchemaVersion == Snapshot.RouteReconnaissanceSchema;

        private static ExpeditionRouteSegmentRecord RouteSegment(Snapshot s, string routeId, string travelerId,
            RuleQuantity startingProgress)
            => s.RouteSegments.SingleOrDefault(x => x.RouteId == routeId && x.TravelerId == travelerId
                && x.StartingProgress == startingProgress);

        private static ExpeditionRouteSegmentRecord RouteSegmentForTravel(Snapshot s, ExpeditionRouteTravelRecord travel)
            => s.RouteSegments.SingleOrDefault(x => x.RouteId == travel.RouteId && x.TravelerId == travel.TravelerId
                && x.StartingProgress == travel.SegmentStartProgress && x.TravelStartedRevision == travel.StartedRevision);

        private static void PutRouteSegment(Snapshot s, ExpeditionRouteSegmentRecord value)
            => s.RouteSegments = s.RouteSegments.Select(x => x.Id == value.Id ? value : x).ToArray();

        private static void PutRouteReconnaissanceAttempt(Snapshot s, ExpeditionRouteReconnaissanceAttemptRecord value)
            => s.RouteReconnaissanceAttempts = s.RouteReconnaissanceAttempts.Select(x => x.Id == value.Id ? value : x).ToArray();

        private void InitializeRouteReconnaissance(Snapshot s)
        {
            if (routeReconnaissanceFixture == null) return;
            string error = routeReconnaissanceFixture.ValidateBindings(s);
            if (error != null) throw new InvalidOperationException(error);
            routeReconnaissanceFixture.Initialize(s);
        }

        private string RouteReconnaissanceWorkerFailure(Snapshot s, string actorId,
            TestOnlyExpeditionRoute route, TestOnlyRouteReconnaissanceTaskProfile task,
            ExpeditionRouteReconnaissanceAttemptRecord current)
        {
            if (s.InventoryCombat || s.Encounter != null && !ResolvedConflict(s)) return "RouteReconnaissanceDuringTacticalControl";
            var actor = s.Actors.SingleOrDefault(x => x.Id == actorId);
            if (actor == null || actor.X != route.FromX || actor.Y != route.FromY
                || s.WorldTraversals.Any(x => x.ActorId == actorId)
                || s.RouteTravels.Any(x => x.TravelerId == actorId && x.Status != ExpeditionRouteTravelStatus.SegmentComplete))
                return "RouteReconnaissanceWorkerNotAtMouth";
            if (!CapableWorker(s, actorId)) return "RouteReconnaissanceWorkerIncapable";
            if (task == null || task.Inspection == null || !task.Inspection.Matches(route))
                return "RouteReconnaissanceInspectionProfileMissing";
            var view = View(s, actorId);
            if (route.Positions.Any(x => !WorldWalkable(s, x.X, x.Y))) return "RouteGeometryBlocked";
            if (view.BlocksSight || view.Unaware)
                return "RouteReconnaissanceInspectionAccessUnavailable";
            var target = new ObservationPoint(new RuleQuantity(task.Inspection.TargetX),
                new RuleQuantity(task.Inspection.TargetY));
            if (observationFixture == null || routeMotionFixture == null
                || !ObservationGeometry.GeometricSight(s, actorId, ObservationGeometry.Position(s, actorId), target))
                return "RouteReconnaissanceInspectionAccessUnavailable";
            RuleTime horizon = CampGreens.Add(s.RuleClock, new RuleTime(1));
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actorId && x.JobId != current?.Id
                    && x.Start < horizon && x.End > s.RuleClock)
                || WorldActivityProjection.CurrentWork(s).Any(x => x.ActorId == actorId && x.Id != current?.Id))
                return "RouteReconnaissanceWorkerBusy";
            return null;
        }

        private string AssessRouteReconnaissance(Snapshot s, Command c, out TestOnlyExpeditionRoute route,
            out TestOnlyRouteReconnaissanceTaskProfile task, out ExpeditionRouteSegmentRecord segment,
            out ExpeditionRouteReconnaissanceAttemptRecord current)
        {
            route = null; task = null; segment = null; current = null;
            if (!RouteReconnaissanceSelected(s) || routeTravelFixture == null) return "RouteReconnaissanceNotSelected";
            if (c.Target == "" || !Validation.ValidId(c.Target) || c.X != 0 || c.Y != 0
                || c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null || c.DefensiveFormation != null
                || c.ExpeditionAssignment != null || c.HarvestSelection != null || c.MiningSelection != null
                || c.ProspectingExposure != null || c.RouteMappingWork != null)
                return "InvalidRouteReconnaissanceRequest";
            if (s.RouteMappingResults.Length != 0) return "SyntheticRouteMappingResultsNotAllowed";
            if (c.Kind == CommandKind.StartRouteReconnaissance)
            {
                if (s.RouteReconnaissanceAttempts.Length >= ExpeditionRouteReconnaissanceValidation.MaxAttempts)
                    return "RouteReconnaissanceHistoryCapacityReached";
                route = routeTravelFixture.Find(c.Target);
                if (route == null) return "UnknownRoute";
                string requestedRouteId = route.Id;
                task = routeReconnaissanceFixture.Find(requestedRouteId);
                if (task == null) return "RouteReconnaissanceUnavailable";
                var last = LatestRouteTravel(s, route.Id, c.Actor);
                RuleQuantity startingProgress = last == null ? default : last.Progress;
                if (startingProgress != default || route.Mapping != ExpeditionRouteMapping.Unknown
                    || route.Risk != 0 || route.Quality != ExpeditionRouteQuality.Secured
                    || route.LengthProgress != new RuleQuantity(2)) return "UnsupportedRouteReconnaissanceProfile";
                if (s.RouteTravels.Any(x => x.Status != ExpeditionRouteTravelStatus.SegmentComplete))
                    return "RouteReconnaissanceConflictsWithRouteTravel";
                if (s.RouteReconnaissanceAttempts.Any(x => x.RouteId == requestedRouteId
                    && x.Status != ExpeditionRouteReconnaissanceStatus.Resolved))
                    return "RouteReconnaissanceAlreadyOpen";
                segment = RouteSegment(s, requestedRouteId, c.Actor, startingProgress);
                var sameRouteSegment = s.RouteSegments.SingleOrDefault(x => x.RouteId == requestedRouteId
                    && x.StartingProgress == startingProgress);
                if (sameRouteSegment != null && sameRouteSegment.TravelerId != c.Actor)
                    return "RouteSegmentBoundToDifferentCohort";
                string latestAttemptId = segment?.LatestAttemptId;
                if (segment != null && (segment.Status != ExpeditionRouteSegmentStatus.ReconnaissanceRequired
                    || latestAttemptId != "" && s.RouteReconnaissanceAttempts.Single(x => x.Id == latestAttemptId)
                        .Status != ExpeditionRouteReconnaissanceStatus.Resolved))
                    return "RouteSegmentNotAvailableForReconnaissance";
                string workerFailure = RouteReconnaissanceWorkerFailure(s, c.Actor, route, task, null);
                if (workerFailure != null) return workerFailure;
                if (route.Positions.Any(x => !WorldWalkable(s, x.X, x.Y))) return "RouteGeometryBlocked";
                RuleTime end = CampGreens.Add(s.RuleClock, new RuleTime(TestOnlyExpeditionRouteReconnaissanceFixture.RequiredWorkSeconds));
                if (s.Work.WorkerIntervals.Any(x => x.WorkerId == c.Actor && x.Start < end && x.End > s.RuleClock))
                    return "RouteReconnaissanceWorkerBusy";
                return null;
            }
            current = s.RouteReconnaissanceAttempts.SingleOrDefault(x => x.Id == c.Target && x.LeadId == c.Actor);
            if (current == null) return "UnknownRouteReconnaissance";
            route = routeTravelFixture.Find(current.RouteId);
            task = route == null ? null : routeReconnaissanceFixture.Find(route.Id);
            segment = RouteSegment(s, current.RouteId, c.Actor, default);
            if (route == null || task == null || segment == null) return "RouteReconnaissanceDefinitionMissing";
            if (c.Kind == CommandKind.PauseRouteReconnaissance)
                return current.Status == ExpeditionRouteReconnaissanceStatus.Working ? null : "RouteReconnaissanceNotWorking";
            if (c.Kind != CommandKind.ResumeRouteReconnaissance) return "InvalidRouteReconnaissanceRequest";
            string resumeFailure = RouteReconnaissanceWorkerFailure(s, current.LeadId, route, task, current);
            if (resumeFailure != null) return resumeFailure;
            if (current.Status == ExpeditionRouteReconnaissanceStatus.AwaitingCheck) return null;
            if (current.Status != ExpeditionRouteReconnaissanceStatus.Paused) return "RouteReconnaissanceNotPaused";
            RuleTime remaining = CampGreens.Subtract(current.WorkRequired, current.WorkDone);
            RuleTime endAt = CampGreens.Add(s.RuleClock, remaining);
            string currentLeadId = current.LeadId, currentId = current.Id;
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == currentLeadId && x.JobId != currentId
                && x.Start < endAt && x.End > s.RuleClock)) return "RouteReconnaissanceWorkerBusy";
            return null;
        }

        private string ResolveRouteReconnaissance(Snapshot s, Command c)
        {
            string failure = AssessRouteReconnaissance(s, c, out var route, out var task, out var segment, out var current);
            if (failure != null) return failure;
            if (c.Kind == CommandKind.StartRouteReconnaissance)
            {
                long revision = s.Revision + 1;
                string segmentId = segment?.Id ?? "route.recon.segment." + revision.ToString(CultureInfo.InvariantCulture);
                string attemptId = "route.recon.attempt." + revision.ToString(CultureInfo.InvariantCulture);
                segment = segment == null
                    ? new ExpeditionRouteSegmentRecord(segmentId, route.Id, c.Actor, revision, default,
                        ExpeditionRouteMapping.Unknown, attemptId, "", default,
                        ExpeditionRouteSegmentStatus.ReconnaissanceRequired, 0, 0, false)
                    : segment.WithLatestAttempt(attemptId);
                current = new ExpeditionRouteReconnaissanceAttemptRecord(attemptId, segmentId, route.Id,
                    c.Actor, task.Inspection.Id, task.Inspection.Fingerprint, revision, s.RuleClock, s.RuleClock, default,
                    new RuleTime(TestOnlyExpeditionRouteReconnaissanceFixture.RequiredWorkSeconds),
                    ExpeditionRouteReconnaissanceStatus.Working);
                BookRouteReconnaissanceWork(s, current);
                if (s.RouteSegments.Any(x => x.Id == segment.Id)) PutRouteSegment(s, segment);
                else s.RouteSegments = s.RouteSegments.Concat(new[] { segment }).ToArray();
                s.RouteReconnaissanceAttempts = s.RouteReconnaissanceAttempts.Concat(new[] { current }).ToArray();
                return null;
            }
            if (c.Kind == CommandKind.PauseRouteReconnaissance) PauseRouteReconnaissance(s, current);
            else if (current.Status == ExpeditionRouteReconnaissanceStatus.AwaitingCheck)
                FinishRouteReconnaissanceCheck(s, segment, current, c.Id, s.Revision + 1, task);
            else
            {
                var resumed = current.WithWork(s.RuleClock, current.WorkDone, ExpeditionRouteReconnaissanceStatus.Working);
                BookRouteReconnaissanceWork(s, resumed);
                PutRouteReconnaissanceAttempt(s, resumed);
            }
            return null;
        }

        private CommandQueryResult QueryRouteReconnaissance(Snapshot s, Command c)
        {
            string error = AssessRouteReconnaissance(s, c, out _, out _, out _, out var current);
            long cost = error != null || c.Kind == CommandKind.PauseRouteReconnaissance
                || current?.Status == ExpeditionRouteReconnaissanceStatus.AwaitingCheck ? 0
                : c.Kind == CommandKind.StartRouteReconnaissance ? TestOnlyExpeditionRouteReconnaissanceFixture.RequiredWorkSeconds
                : CampGreens.Subtract(current.WorkRequired, current.WorkDone).Numerator;
            var costs = error == null && cost > 0
                ? new[] { new CommandCost("active-work-seconds", c.Target, cost) }
                : Array.Empty<CommandCost>();
            return new CommandQueryResult(true, error == null, error ?? "Available", s.Revision, costs);
        }

        private static void BookRouteReconnaissanceWork(Snapshot s,
            ExpeditionRouteReconnaissanceAttemptRecord attempt)
        {
            RuleTime end = CampGreens.Add(s.RuleClock, CampGreens.Subtract(attempt.WorkRequired, attempt.WorkDone));
            string booking = (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
            var interval = new WorkerInterval(attempt.Id + ".labor." + attempt.LeadId + "." + booking,
                attempt.Id, attempt.LeadId, s.RuleClock, end);
            s.Work = s.Work.Reserve(attempt.Id, new[] { interval }, Array.Empty<ResourceReservation>());
        }

        private static void PauseRouteReconnaissance(Snapshot s, ExpeditionRouteReconnaissanceAttemptRecord attempt)
        {
            s.Work = s.Work.CancelFutureWork(attempt.Id, s.RuleClock);
            PutRouteReconnaissanceAttempt(s, attempt.WithWork(s.RuleClock, attempt.WorkDone,
                ExpeditionRouteReconnaissanceStatus.Paused));
        }

        private void PauseIncompatibleRouteReconnaissance(Snapshot s)
        {
            if (!RouteReconnaissanceSelected(s)) return;
            foreach (var attempt in s.RouteReconnaissanceAttempts
                .Where(x => x.Status == ExpeditionRouteReconnaissanceStatus.Working).ToArray())
            {
                var route = routeTravelFixture.Find(attempt.RouteId);
                var task = route == null ? null : routeReconnaissanceFixture.Find(route.Id);
                if (route == null || RouteReconnaissanceWorkerFailure(s, attempt.LeadId, route, task, attempt) != null)
                    PauseRouteReconnaissance(s, attempt);
            }
        }

        private RuleTime? NextRouteReconnaissanceBoundary(Snapshot s)
        {
            if (!RouteReconnaissanceSelected(s)) return null;
            var ends = s.RouteReconnaissanceAttempts.Where(x => x.Status == ExpeditionRouteReconnaissanceStatus.Working)
                .SelectMany(x => s.Work.WorkerIntervals.Where(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock)
                    .Select(w => w.End)).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }

        private void CreditRouteReconnaissance(Snapshot s, RuleTime elapsed,
            System.Collections.Generic.ICollection<string> readyChecks = null)
        {
            if (!RouteReconnaissanceSelected(s)) return;
            foreach (var attempt in s.RouteReconnaissanceAttempts
                .Where(x => x.Status == ExpeditionRouteReconnaissanceStatus.Working).ToArray())
            {
                if (!s.Work.WorkerIntervals.Any(w => w.JobId == attempt.Id && w.WorkerId == attempt.LeadId
                    && w.Start <= attempt.UpdatedAt && w.End >= s.RuleClock))
                    throw new InvalidOperationException("Route reconnaissance work interval is not reserved.");
                RuleTime progress = CampGreens.Add(attempt.WorkDone, elapsed);
                if (progress < attempt.WorkRequired)
                {
                    PutRouteReconnaissanceAttempt(s, attempt.WithWork(s.RuleClock, progress,
                        ExpeditionRouteReconnaissanceStatus.Working));
                    continue;
                }
                if (progress != attempt.WorkRequired)
                    throw new InvalidOperationException("Route reconnaissance crossed its work boundary without the clock boundary.");
                PutRouteReconnaissanceAttempt(s, attempt.AwaitCheck(s.RuleClock));
                readyChecks?.Add(attempt.Id);
            }
        }

        private void FinishRouteReconnaissanceCheck(Snapshot s, ExpeditionRouteSegmentRecord segment,
            ExpeditionRouteReconnaissanceAttemptRecord attempt, string commandId, long appliedRevision,
            TestOnlyRouteReconnaissanceTaskProfile task)
        {
            if (attempt.Status != ExpeditionRouteReconnaissanceStatus.AwaitingCheck || attempt.Check != null
                || attempt.WorkDone != attempt.WorkRequired)
                throw new InvalidOperationException("Route reconnaissance check is not awaiting resolution.");
            var route = routeTravelFixture.Find(attempt.RouteId);
            string workerFailure = route == null ? "RouteReconnaissanceDefinitionMissing"
                : RouteReconnaissanceWorkerFailure(s, attempt.LeadId, route, task, attempt);
            if (task == null || segment == null || workerFailure != null)
                throw new InvalidOperationException(workerFailure ?? "RouteReconnaissanceDefinitionMissing");
            var actorFacts = CharacterStateFacts.ForActor(s, attempt.LeadId, TestOnlyExpeditionRouteReconnaissanceFixture.SkillId);
            var modifier = actorFacts.DeriveCheck(CharacterAbility.Wisdom);
            int leadModifier = modifier.TotalWithInjury(actorFacts);
            int conditionOperationCount = s.Conditions.Single(x => x.Target == attempt.LeadId).Operations.Count;
            bool disadvantage = RouteMappingCheckDisadvantage(s, attempt.LeadId, s.RuleClock, conditionOperationCount);
            uint before = s.RandomState;
            RuleD20Roll roll = RuleDice.RollD20(before, disadvantageSources: disadvantage ? 1 : 0);
            var outcome = RuleResolution.TaskCheck(roll.Natural, leadModifier, task.Dc);
            var degree = outcome.Degree == RuleTaskDegree.CriticalFailure ? ExpeditionRouteReconnaissanceDegree.CriticalFailure
                : outcome.Degree == RuleTaskDegree.Failure ? ExpeditionRouteReconnaissanceDegree.Failure
                : outcome.Degree == RuleTaskDegree.Success ? ExpeditionRouteReconnaissanceDegree.Success
                : ExpeditionRouteReconnaissanceDegree.CriticalSuccess;
            s.RandomState = roll.NextRandomState;
            var check = new ExpeditionRouteReconnaissanceCheckRecord(commandId, appliedRevision, s.RuleClock,
                leadModifier, modifier.ProficiencyRank, modifier.ProficiencyBonus, task.Dc, conditionOperationCount,
                disadvantage, roll.First, roll.Second ?? 0, roll.Natural, outcome.Total, degree,
                before, roll.NextRandomState, roll.WordsConsumed);
            var resolved = attempt.Resolve(s.RuleClock, check);
            PutRouteReconnaissanceAttempt(s, resolved);
            if (degree == ExpeditionRouteReconnaissanceDegree.Success
                || degree == ExpeditionRouteReconnaissanceDegree.CriticalSuccess)
                PutRouteSegment(s, segment.MakeFeasible(attempt.Id,
                    degree == ExpeditionRouteReconnaissanceDegree.CriticalSuccess));
        }

        private void ResolveReadyRouteReconnaissanceChecks(Snapshot s,
            System.Collections.Generic.IEnumerable<string> attemptIds, Command initiating)
        {
            if (initiating == null || attemptIds == null) return;
            foreach (string id in attemptIds.Distinct(StringComparer.Ordinal))
            {
                var attempt = s.RouteReconnaissanceAttempts.SingleOrDefault(x => x.Id == id);
                if (attempt == null || attempt.Status != ExpeditionRouteReconnaissanceStatus.AwaitingCheck) continue;
                var route = routeTravelFixture.Find(attempt.RouteId);
                var segment = s.RouteSegments.SingleOrDefault(x => x.Id == attempt.SegmentId);
                var task = route == null ? null : routeReconnaissanceFixture.Find(route.Id);
                if (route != null && task != null
                    && attempt.InspectionProfileId == task.Inspection.Id
                    && attempt.InspectionProfileFingerprint == task.Inspection.Fingerprint
                    && RouteReconnaissanceWorkerFailure(s, attempt.LeadId, route, task, attempt) == null)
                    FinishRouteReconnaissanceCheck(s, segment, attempt, initiating.Id, s.Revision + 1, task);
            }
        }

        private string ValidateRouteReconnaissanceState(Snapshot s)
        {
            if (routeReconnaissanceFixture == null)
                return s.RouteSegments.Length == 0 && s.RouteReconnaissanceAttempts.Length == 0
                    && s.SchemaVersion != Snapshot.RouteReconnaissanceSchema ? null : "RouteReconnaissanceFixtureMissing";
            if (!RouteReconnaissanceSelected(s) || routeTravelFixture == null
                || routeReconnaissanceFixture.ValidateRoutes(routeTravelFixture) != null
                || routeReconnaissanceFixture.ValidateBindings(s) != null || s.RouteMappingResults.Length != 0)
                return "RouteReconnaissanceSchemaOrFixtureMismatch";
            foreach (var attempt in s.RouteReconnaissanceAttempts)
            {
                var route = routeTravelFixture.Find(attempt.RouteId);
                var task = route == null ? null : routeReconnaissanceFixture.Find(route.Id);
                var segment = s.RouteSegments.SingleOrDefault(x => x.Id == attempt.SegmentId);
                var startReceipt = s.Receipts.SingleOrDefault(x => x.Revision == attempt.StartedRevision);
                if (route == null || task == null || segment == null
                    || attempt.InspectionProfileId != task.Inspection.Id
                    || attempt.InspectionProfileFingerprint != task.Inspection.Fingerprint
                    || attempt.WorkRequired != new RuleTime(TestOnlyExpeditionRouteReconnaissanceFixture.RequiredWorkSeconds)
                    || segment.StartingMapping != ExpeditionRouteMapping.Unknown || segment.StartingProgress != default
                    || segment.RouteId != route.Id || segment.TravelerId != attempt.LeadId || startReceipt == null)
                    return "InvalidRouteReconnaissanceEvidence";
                Command start;
                try { start = CommandHistory.Read(startReceipt); }
                catch (ArgumentException) { return "InvalidRouteReconnaissanceStartCommand"; }
                if (start.Kind != CommandKind.StartRouteReconnaissance || start.Actor != attempt.LeadId
                    || start.Target != route.Id || attempt.StartedAt > s.RuleClock)
                    return "InvalidRouteReconnaissanceStartCommand";
                if (attempt.Check != null)
                {
                    var check = attempt.Check;
                    var checkReceipt = s.Receipts.SingleOrDefault(x => x.Revision == check.AppliedRevision);
                    if (checkReceipt == null) return "InvalidRouteReconnaissanceCheckCommand";
                    Command checkCommand;
                    try { checkCommand = CommandHistory.Read(checkReceipt); }
                    catch (ArgumentException) { return "InvalidRouteReconnaissanceCheckCommand"; }
                    var conditionJournal = s.Conditions.Single(x => x.Target == attempt.LeadId);
                    if (check.ConditionOperationCount < 0 || check.ConditionOperationCount > conditionJournal.Operations.Count
                        || conditionJournal.Operations.Take(check.ConditionOperationCount)
                            .Any(x => x.At.CompareTo(new ConditionStamp(check.At)) > 0))
                        return "InvalidRouteReconnaissanceConditionEvidence";
                    bool expectedDisadvantage = RouteMappingCheckDisadvantage(s, attempt.LeadId,
                        check.At, check.ConditionOperationCount);
                    RuleD20Roll replayedRoll = RuleDice.RollD20(check.RandomBefore,
                        disadvantageSources: check.Disadvantage ? 1 : 0);
                    if (checkReceipt.Id != check.CommandId || checkCommand.ExpectedRevision + 1 != check.AppliedRevision
                        || check.At < attempt.StartedAt || expectedDisadvantage != check.Disadvantage
                        || replayedRoll.Selection != (check.Disadvantage ? RuleD20Selection.Disadvantage : RuleD20Selection.Normal)
                        || replayedRoll.First != check.FirstRoll || replayedRoll.Second.GetValueOrDefault() != check.SecondRoll
                        || replayedRoll.Natural != check.Natural || replayedRoll.NextRandomState != check.RandomAfter
                        || replayedRoll.WordsConsumed != check.WordsConsumed)
                        return "InvalidRouteReconnaissanceRandomEvidence";
                    var actorFacts = CharacterStateFacts.ForActor(s, attempt.LeadId, TestOnlyExpeditionRouteReconnaissanceFixture.SkillId);
                    var modifier = actorFacts.DeriveCheck(CharacterAbility.Wisdom);
                    int leadModifier = modifier.TotalWithInjury(actorFacts);
                    var expected = RuleResolution.TaskCheck(check.Natural, leadModifier, task.Dc);
                    var expectedDegree = expected.Degree == RuleTaskDegree.CriticalFailure ? ExpeditionRouteReconnaissanceDegree.CriticalFailure
                        : expected.Degree == RuleTaskDegree.Failure ? ExpeditionRouteReconnaissanceDegree.Failure
                        : expected.Degree == RuleTaskDegree.Success ? ExpeditionRouteReconnaissanceDegree.Success
                        : ExpeditionRouteReconnaissanceDegree.CriticalSuccess;
                    if (check.LeadModifier != leadModifier || check.ProficiencyRank != modifier.ProficiencyRank
                        || check.ProficiencyBonus != modifier.ProficiencyBonus || check.Dc != task.Dc
                        || check.Total != expected.Total || check.Degree != expectedDegree)
                        return "InvalidRouteReconnaissanceCheck";
                }
                var intervals = s.Work.WorkerIntervals.Where(x => x.JobId == attempt.Id).ToArray();
                if (intervals.Length == 0 && attempt.Status == ExpeditionRouteReconnaissanceStatus.Paused
                    && attempt.WorkDone == default && attempt.Check == null) continue;
                if (intervals.Length == 0 || intervals.Any(x => x.WorkerId != attempt.LeadId))
                    return "InvalidRouteReconnaissanceReservations";
                RuleTime credited = default;
                foreach (var interval in intervals.OrderBy(x => x.Start))
                {
                    RuleTime end = interval.End < s.RuleClock ? interval.End : s.RuleClock;
                    if (end > interval.Start) credited = CampGreens.Add(credited, CampGreens.Subtract(end, interval.Start));
                }
                var leadIntervals = intervals.OrderBy(x => x.Start).ToArray();
                if (credited != attempt.WorkDone
                    || attempt.Status == ExpeditionRouteReconnaissanceStatus.AwaitingCheck
                        && (leadIntervals.Length == 0 || leadIntervals[leadIntervals.Length - 1].End != attempt.UpdatedAt)
                    || attempt.Status == ExpeditionRouteReconnaissanceStatus.Resolved
                        && (leadIntervals.Length == 0 || leadIntervals[leadIntervals.Length - 1].End > attempt.Check.At))
                    return "InvalidRouteReconnaissanceProgressEvidence";
                bool working = attempt.Status == ExpeditionRouteReconnaissanceStatus.Working;
                RuleTime expectedEnd = CampGreens.Add(s.RuleClock, CampGreens.Subtract(attempt.WorkRequired, attempt.WorkDone));
                int active = intervals.Count(x => x.Start <= s.RuleClock && x.End > s.RuleClock);
                if (active != (working ? 1 : 0)
                    || working && !intervals.Any(x => x.Start <= s.RuleClock && x.End == expectedEnd))
                    return "InvalidRouteReconnaissanceReservationStatus";
            }
            return null;
        }
    }
}
#endif
