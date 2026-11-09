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
    /// <summary>An exact route-progress to traversable exploration-cell binding. These points
    /// describe authored geometry; they do not create arbitrary walkable cells.</summary>
    public sealed class TestOnlyRoutePositionBinding
    {
        public RuleQuantity Progress { get; }
        public int X { get; }
        public int Y { get; }
        public TestOnlyRoutePositionBinding(RuleQuantity progress, int x, int y)
        { Progress = progress; X = x; Y = y; }
        internal string Canonical => Progress + "@" + X.ToString(CultureInfo.InvariantCulture) + "," + Y.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Immutable, explicitly authored TEST_ONLY route content. Source-derived quality,
    /// mapping, Risk, capacity and physical progress bindings remain independent fields.</summary>
    public sealed class TestOnlyExpeditionRoute
    {
        private readonly TestOnlyRoutePositionBinding[] positions;
        public string Id { get; }
        public string FromLocationId { get; }
        public string ToLocationId { get; }
        public int FromX { get; }
        public int FromY { get; }
        public int ToSiteX { get; }
        public int ToSiteY { get; }
        public RuleQuantity LengthProgress { get; }
        public ExpeditionRouteQuality Quality { get; }
        public int Risk { get; }
        public ExpeditionRouteMapping Mapping { get; }
        public RuleQuantity CapacityLoad { get; }
        public IReadOnlyList<TestOnlyRoutePositionBinding> Positions { get; }

        public TestOnlyExpeditionRoute(string id, string fromLocationId, string toLocationId,
            int fromX, int fromY, int toSiteX, int toSiteY, RuleQuantity lengthProgress,
            ExpeditionRouteQuality quality, int risk, ExpeditionRouteMapping mapping,
            RuleQuantity capacityLoad, IEnumerable<TestOnlyRoutePositionBinding> positions)
        {
            this.positions = (positions ?? Array.Empty<TestOnlyRoutePositionBinding>()).ToArray();
            if (!Validation.ValidId(id) || !Validation.ValidId(fromLocationId) || !Validation.ValidId(toLocationId)
                || fromX < 0 || fromY < 0 || toSiteX < 0 || toSiteY < 0 || lengthProgress == default
                || !Enum.IsDefined(typeof(ExpeditionRouteQuality), quality) || risk < 0
                || !Enum.IsDefined(typeof(ExpeditionRouteMapping), mapping) || capacityLoad == default
                || this.positions.Length < 2 || this.positions.Length > 128 || this.positions.Any(x => x == null)
                || this.positions.Select(x => x.Progress).Distinct().Count() != this.positions.Length
                || this.positions[0].Progress != default || this.positions[this.positions.Length - 1].Progress != lengthProgress
                || this.positions[0].X != fromX || this.positions[0].Y != fromY
                || WorldSpatialQueries.CardinalDistance(this.positions[this.positions.Length - 1].X,
                    this.positions[this.positions.Length - 1].Y, toSiteX, toSiteY) != 1
                || this.positions.Zip(this.positions.Skip(1), (a, b) => b.Progress > a.Progress
                    && WorldSpatialQueries.CardinalDistance(a.X, a.Y, b.X, b.Y) == 1).Any(ok => !ok))
                throw new ArgumentException("Invalid source-bound expedition route fixture.");
            Id = id; FromLocationId = fromLocationId; ToLocationId = toLocationId; FromX = fromX; FromY = fromY;
            ToSiteX = toSiteX; ToSiteY = toSiteY; LengthProgress = lengthProgress; Quality = quality;
            Risk = risk; Mapping = mapping; CapacityLoad = capacityLoad;
            Positions = Array.AsReadOnly(this.positions);
        }

        internal string Canonical => Id + "|" + FromLocationId + "|" + ToLocationId + "|" + FromX + "," + FromY
            + "|" + ToSiteX + "," + ToSiteY + "|" + LengthProgress + "|" + (int)Quality + "|" + Risk
            + "|" + (int)Mapping + "|" + CapacityLoad + "|" + string.Join(";", positions.Select(x => x.Canonical));

        internal TestOnlyRoutePositionBinding PositionAt(RuleQuantity progress)
            => positions.Where(x => x.Progress <= progress).OrderBy(x => x.Progress).LastOrDefault();
        internal TestOnlyRoutePositionBinding NextPositionAfter(RuleQuantity progress)
            => positions.Where(x => x.Progress > progress).OrderBy(x => x.Progress).FirstOrDefault();
    }

    /// <summary>Version-pinned TEST_ONLY route set. The expedition candidate remains unregistered
    /// for release and this fixture cannot create a Release simulation.</summary>
    public sealed class TestOnlyExpeditionRouteFixture
    {
        private const string PlayerBookSha256 = "4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480";
        private readonly TestOnlyExpeditionRoute[] routes;
        public IReadOnlyList<TestOnlyExpeditionRoute> Routes { get; }
        public string Fingerprint { get; }

        public TestOnlyExpeditionRouteFixture(params TestOnlyExpeditionRoute[] routes)
        {
            if (routes == null || routes.Length < 1 || routes.Length > 32 || routes.Any(x => x == null)
                || routes.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != routes.Length)
                throw new ArgumentException("Invalid TEST_ONLY route fixture set.");
            this.routes = routes.OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            Routes = Array.AsReadOnly(this.routes);
            string key = "ex58-exact-2026-10-11|FL-10|TR-13|player-book-sha256=" + PlayerBookSha256
                + "|source-candidate-not-release-registered|route-position-bindings-v1|"
                + string.Join(";", this.routes.Select(x => x.Canonical));
            using (var sha = SHA256.Create()) Fingerprint = "TEST_ONLY.expedition-routes-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }

        internal TestOnlyExpeditionRoute Find(string id) => routes.SingleOrDefault(x => x.Id == id);

        internal string ValidateBindings(Snapshot s, SharedHarvestFixture harvest, SharedWorldConfiguration config)
        {
            foreach (var route in routes)
            {
                if (route.Positions.Any(p => !TestOnlyPolicy.Walkable(p.X, p.Y))) return "RouteGeometryOutsideFixtureMap";
                RuleQuantity ordinaryAward = ExpeditionRouteTravelRules.BaseProgress(route.Mapping);
                if (ordinaryAward != default)
                {
                    BigInteger terminalNumerator = (BigInteger)route.LengthProgress.Numerator * ordinaryAward.Denominator;
                    BigInteger terminalDenominator = (BigInteger)route.LengthProgress.Denominator * ordinaryAward.Numerator;
                    if (terminalNumerator % terminalDenominator != 0) return "RouteTerminalProgressUnsupported";
                }
                bool LocationMatches(string id, int x, int y)
                    => harvest != null && id == SharedHarvestFixture.SiteId && x == harvest.SiteX && y == harvest.SiteY
                        || config != null && id == config.WorkSite.Id && x == config.WorkSite.X && y == config.WorkSite.Y
                        || s.Objects.Any(o => o.Id == id && o.X == x && o.Y == y)
                        || s.SupplyCaches.Any(o => o.Id == id && o.X == x && o.Y == y)
                        || s.FishingTraps.Any(o => o.TrapId == id && o.X == x && o.Y == y)
                        || s.FishingReceiveLocations.Any(o => o.Id == id && o.X == x && o.Y == y)
                        // The prepared-plot host fixes this fixture site at (3,3); bind by both
                        // its persisted plot identity and the existing host's authored position.
                        || id == TestOnlyCropPolicy.PlotId && x == 3 && y == 3 && s.CropPlots.Any(o => o.Id == id);
                if (!LocationMatches(route.FromLocationId, route.FromX, route.FromY)
                    || !LocationMatches(route.ToLocationId, route.ToSiteX, route.ToSiteY))
                    return "RouteEndpointNotBoundToExistingSite";
            }
            return null;
        }
    }

    /// <summary>An explicitly authored straight physical edge for one interval of route
    /// Progress. Linear interpolation is a fixture choice, never inferred for an arbitrary route.</summary>
    public sealed class TestOnlyRouteMotionLeg
    {
        public string RouteId { get; }
        public RuleQuantity StartProgress { get; }
        public RuleQuantity EndProgress { get; }
        public int FromX { get; }
        public int FromY { get; }
        public int ToX { get; }
        public int ToY { get; }

        public TestOnlyRouteMotionLeg(string routeId, RuleQuantity startProgress, RuleQuantity endProgress,
            int fromX, int fromY, int toX, int toY)
        {
            if (!Validation.ValidId(routeId) || startProgress < default(RuleQuantity) || endProgress <= startProgress
                || fromX < 0 || fromY < 0 || toX < 0 || toY < 0
                || WorldSpatialQueries.CardinalDistance(fromX, fromY, toX, toY) != 1)
                throw new ArgumentException("Invalid authored route-motion leg.");
            RouteId = routeId; StartProgress = startProgress; EndProgress = endProgress;
            FromX = fromX; FromY = fromY; ToX = toX; ToY = toY;
        }

        internal string Canonical => RouteId + "|" + StartProgress + ".." + EndProgress + "|"
            + FromX.ToString(CultureInfo.InvariantCulture) + "," + FromY.ToString(CultureInfo.InvariantCulture)
            + "->" + ToX.ToString(CultureInfo.InvariantCulture) + "," + ToY.ToString(CultureInfo.InvariantCulture);

        internal RuleQuantity ParameterAt(RuleQuantity progress)
        {
            RuleQuantity elapsed = progress - StartProgress;
            RuleQuantity duration = EndProgress - StartProgress;
            return RuleQuantity.FromFraction((BigInteger)elapsed.Numerator * duration.Denominator,
                (BigInteger)elapsed.Denominator * duration.Numerator);
        }

        internal ObservationPoint PositionAt(RuleQuantity progress)
        {
            RuleQuantity t = ParameterAt(progress);
            RuleQuantity Coordinate(int start, int end)
                => RuleQuantity.FromFraction((BigInteger)start * t.Denominator
                    + (BigInteger)(end - start) * t.Numerator, t.Denominator);
            return new ObservationPoint(Coordinate(FromX, ToX), Coordinate(FromY, ToY));
        }

        internal RuleQuantity DistanceFeetAt(RuleQuantity progress) => ParameterAt(progress).Scale(5);
    }

    /// <summary>Fingerprint-bound continuous physical paths for a TEST_ONLY route set. Every
    /// route edge must be explicitly authored; this fixture does not infer straight paths.</summary>
    public sealed class TestOnlyExpeditionRouteMotionFixture
    {
        private readonly TestOnlyRouteMotionLeg[] legs;
        public string RouteFingerprint { get; }
        public string Fingerprint { get; }

        public TestOnlyExpeditionRouteMotionFixture(TestOnlyExpeditionRouteFixture routes,
            params TestOnlyRouteMotionLeg[] legs)
        {
            if (routes == null || legs == null || legs.Length < 1 || legs.Length > 128 || legs.Any(x => x == null)
                || legs.Select(x => x.RouteId + "|" + x.StartProgress).Distinct(StringComparer.Ordinal).Count() != legs.Length)
                throw new ArgumentException("Invalid authored route-motion fixture.");
            RouteFingerprint = routes.Fingerprint;
            this.legs = legs.OrderBy(x => x.RouteId, StringComparer.Ordinal).ThenBy(x => x.StartProgress).ToArray();
            string error = ValidateRoutes(routes);
            if (error != null) throw new ArgumentException(error);
            string key = "route-motion-linear-cardinal-v1|" + RouteFingerprint + "|"
                + string.Join(";", this.legs.Select(x => x.Canonical));
            using (var sha = SHA256.Create()) Fingerprint = "TEST_ONLY.route-motion-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }

        internal string ValidateRoutes(TestOnlyExpeditionRouteFixture routes)
        {
            if (routes == null || routes.Fingerprint != RouteFingerprint) return "RouteMotionFixtureMismatch";
            foreach (var route in routes.Routes)
            {
                var routeLegs = legs.Where(x => x.RouteId == route.Id).ToArray();
                var expected = route.Positions.Zip(route.Positions.Skip(1), (a, b) => new {
                    Start = a, End = b
                }).ToArray();
                if (routeLegs.Length != expected.Length) return "RouteMotionBindingIncomplete";
                for (int i = 0; i < expected.Length; i++)
                    if (routeLegs[i].StartProgress != expected[i].Start.Progress
                        || routeLegs[i].EndProgress != expected[i].End.Progress
                        || routeLegs[i].FromX != expected[i].Start.X || routeLegs[i].FromY != expected[i].Start.Y
                        || routeLegs[i].ToX != expected[i].End.X || routeLegs[i].ToY != expected[i].End.Y)
                        return "RouteMotionBindingDoesNotMatchPositionCheckpoints";
            }
            if (legs.Any(x => routes.Routes.All(r => r.Id != x.RouteId))) return "RouteMotionDefinitionMissing";
            return null;
        }

        internal string ValidateBindings(Snapshot s, TestOnlyExpeditionRouteFixture routes,
            SharedHarvestFixture harvest, SharedWorldConfiguration config)
        {
            string error = ValidateRoutes(routes);
            if (error != null) return error;
            foreach (var leg in legs)
                if (!TestOnlyPolicy.Walkable(leg.FromX, leg.FromY) || !TestOnlyPolicy.Walkable(leg.ToX, leg.ToY)
                    || s.ObservationMapWidth < 1 || !ObservationGeometry.SupportsAnchorAt(s, leg.FromX, leg.FromY)
                    || !ObservationGeometry.SupportsAnchorAt(s, leg.ToX, leg.ToY))
                    return "RouteMotionGeometryOutsideObservationMap";
            return routes.ValidateBindings(s, harvest, config);
        }

        internal TestOnlyRouteMotionLeg LegAt(string routeId, RuleQuantity progress)
            => legs.Where(x => x.RouteId == routeId && x.StartProgress <= progress && progress < x.EndProgress)
                .OrderBy(x => x.StartProgress).FirstOrDefault()
                ?? legs.Where(x => x.RouteId == routeId && progress == x.EndProgress).OrderBy(x => x.StartProgress).LastOrDefault();

        internal ObservationPoint PositionAt(string routeId, RuleQuantity progress)
        {
            var leg = LegAt(routeId, progress);
            if (leg == null) return default;
            return leg.PositionAt(progress);
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionRouteFixture routeTravelFixture;
        private TestOnlyExpeditionRouteMotionFixture routeMotionFixture;

        /// <summary>Opt into the exact-candidate ordinary travel slice before Initial(). This
        /// changes the TEST_ONLY profile fingerprint and selects the append-only schema52 envelope.</summary>
        public TestOnlySharedWorldPolicy EnableExpeditionRouteTravel(TestOnlyExpeditionRouteFixture fixture)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (observationFixture != null) throw new InvalidOperationException("RouteObservationIntegrationUnsupported");
            if (fixture == null || routeTravelFixture != null) throw new ArgumentException("Supply one explicit route fixture.");
            routeTravelFixture = fixture;
            string value = ContentFingerprint + "|" + fixture.Fingerprint;
            using (var sha = SHA256.Create()) ContentFingerprint = "TEST_ONLY.route-world-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(value)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        /// <summary>Selects a new TEST_ONLY composed route-motion and observation profile. Route
        /// travel progress owns motion on explicitly authored cardinal legs. This is schema53;
        /// legacy route-only schema52 remains byte- and behavior-compatible.</summary>
        public TestOnlySharedWorldPolicy EnableRouteObservationIntegration(
            TestOnlyExpeditionRouteFixture routes, TestOnlyExpeditionRouteMotionFixture motion,
            ObservationFixture observation,
            ObservationAlgorithmVersion algorithmVersion = ObservationAlgorithmVersion.ExactPathIntervalsV2)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (routes == null || motion == null || observation == null)
                throw new ArgumentNullException("Composed route-observation profile requires route, motion, and observation content.");
            if (routeTravelFixture != null || observationFixture != null || routeMotionFixture != null)
                throw new InvalidOperationException("Route-observation content is already selected or conflicts with an existing profile.");
            if (algorithmVersion != ObservationAlgorithmVersion.LegacySampledV1
                && algorithmVersion != ObservationAlgorithmVersion.ExactPathIntervalsV2)
                throw new ArgumentOutOfRangeException(nameof(algorithmVersion));
            string error = motion.ValidateRoutes(routes);
            if (error != null) throw new InvalidOperationException(error);
            routeTravelFixture = routes; routeMotionFixture = motion;
            observationFixture = observation; observationAlgorithmVersion = algorithmVersion;
            ContentFingerprint = BindRouteMotionFingerprint(ContentFingerprint, routes, motion);
            ContentFingerprint = ObservationFixture.BindFingerprint(ContentFingerprint, observation, algorithmVersion);
            return this;
        }

        private static string BindRouteMotionFingerprint(string prior, TestOnlyExpeditionRouteFixture routes,
            TestOnlyExpeditionRouteMotionFixture motion)
        {
            using (var sha = SHA256.Create()) return "TEST_ONLY.route-observation-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior + "|" + routes.Fingerprint
                    + "|" + motion.Fingerprint)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }

        private void InitializeExpeditionRouteTravel(Snapshot s)
        {
            if (routeTravelFixture == null) return;
            if (routeMotionFixture == null && observationFixture != null)
                throw new InvalidOperationException("RouteObservationIntegrationUnsupported");
            string error = routeMotionFixture == null
                ? routeTravelFixture.ValidateBindings(s, harvestFixture, worldConfiguration)
                : routeMotionFixture.ValidateBindings(s, routeTravelFixture, harvestFixture, worldConfiguration);
            if (error != null) throw new InvalidOperationException(error);
            s.RouteTravels = Array.Empty<ExpeditionRouteTravelRecord>();
            s.RouteTravelSpatial = Array.Empty<ExpeditionRouteSpatialRecord>();
            s.RouteMappingResults = Array.Empty<ExpeditionRouteMappingResultRecord>();
        }

        private static bool RouteTravelCommand(CommandKind kind)
            => kind == CommandKind.StartRouteTravel || kind == CommandKind.PauseRouteTravel || kind == CommandKind.ResumeRouteTravel;

        private static ExpeditionRouteTravelRecord OpenRouteTravel(Snapshot s, string actor)
            => s.RouteTravels.Where(x => x.TravelerId == actor
                && (x.Status == ExpeditionRouteTravelStatus.Moving || x.Status == ExpeditionRouteTravelStatus.Paused))
                .SingleOrDefault();

        private static ExpeditionRouteTravelRecord LatestRouteTravel(Snapshot s, string routeId, string actor)
            => s.RouteTravels.Where(x => x.RouteId == routeId && x.TravelerId == actor)
                .OrderByDescending(x => x.StartedRevision).FirstOrDefault();

        private static ExpeditionRouteSpatialRecord RouteSpatial(Snapshot s, string actor)
            => s.RouteTravelSpatial.SingleOrDefault(x => x.TravelerId == actor);

        private void SetRouteTravel(Snapshot s, ExpeditionRouteTravelRecord value)
            => s.RouteTravels = s.RouteTravels.Select(x => x.StartedRevision == value.StartedRevision ? value : x).ToArray();

        private static void SetRouteSpatial(Snapshot s, ExpeditionRouteSpatialRecord value)
            => s.RouteTravelSpatial = s.RouteTravelSpatial.Select(x => x.TravelStartedRevision == value.TravelStartedRevision ? value : x).ToArray();

        private string AssessRouteTravelCommand(Snapshot s, Command c, out TestOnlyExpeditionRoute route,
            out ExpeditionRouteTravelRecord current, out RuleQuantity startingProgress, out RuleQuantity segmentAward)
        {
            route = null; current = null; startingProgress = default; segmentAward = default;
            if (routeTravelFixture == null) return "RouteTravelNotEnabled";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.Target == "" || c.X != 0 || c.Y != 0 || !Validation.ValidId(c.Target)) return "InvalidRouteTravelRequest";
            route = routeTravelFixture.Find(c.Target);
            if (route == null) return "UnknownRoute";
            if (expeditionPressureProfile != null)
            {
                if (c.Actor != expeditionPressureProfile.MemberId) return "PressureCohortTravelActorRequired";
                if (route.Quality == ExpeditionRouteQuality.Collapsed || route.Risk > 6)
                    return "PressureRouteProfileUnsupported";
                string pressureAccessFailure = PressureRouteAccessFailure(s, route);
                if (pressureAccessFailure != null) return pressureAccessFailure;
                if (c.Kind == CommandKind.StartRouteTravel)
                {
                    string reentryFailure = PressureRouteStartFailure(s, route);
                    if (reentryFailure != null) return reentryFailure;
                }
            }
            // Route commands are dispatched ahead of the shared manufacturing continuation
            // guard. Keep their query and execution path aligned with that guard explicitly.
            // This is schema53-only so schema52 command admission remains byte-for-byte in
            // its historical behavioral envelope.
            if (routeMotionFixture != null)
            {
                if (PendingCalendarChoice(s)) return "TacticalChoicePending";
                if (ManufacturingChoicePending(s) || s.ManufacturingAdvance != null)
                    return "ManufacturingChoicePending";
            }
            current = OpenRouteTravel(s, c.Actor);
            if (c.Kind == CommandKind.StartRouteTravel)
            {
                if (current != null) return "RouteTravelAlreadyOpen";
                if(HuntingTrapValidation.HasActiveTether(s,c.Actor))return "HuntingTrapTetherPreventsRouteTravel";
                string controlFailure = RouteTravelControlFailure(s);
                if (controlFailure != null) return controlFailure;
                if (s.WorldTraversals.Length != 0) return "RouteTravelConflictsWithGridTraversal";
                if (s.RouteTravels.Length >= ExpeditionRouteTravelValidation.MaxRecords)
                    return "RouteTravelHistoryCapacityReached";
                if (s.RouteTravels.Any(x => x.Status == ExpeditionRouteTravelStatus.Moving)) return "ConcurrentRouteTravelUnsupported";
                if (expeditionPressureProfile == null)
                {
                    if (route.Risk != 0) return "RouteRiskResolutionUnsupported";
                    if (route.Quality != ExpeditionRouteQuality.Secured) return "RouteQualityConsequenceUnsupported";
                }
                if (OrdinaryInventory.Busy(s, c.Actor) || WorldActivityValidation.HasActiveLabor(s, c.Actor, s.RuleClock, s.RuleClock.AddSeconds(1)))
                    return "RouteTravelerBusy";
                if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) <= 0) return "ConditionPreventsRouteTravel";
                var burden = PortableEquipmentRules.CarriedBurden(s, c.Actor);
                if (!burden.Load.HasValue) return "RouteLoadEvidenceIncomplete";
                if (burden.Load.Value > route.CapacityLoad) return "RouteCapacitySettlementUnsupported";
                var last = LatestRouteTravel(s, route.Id, c.Actor);
                if (last != null)
                {
                    if (last.Status != ExpeditionRouteTravelStatus.SegmentComplete) return "RouteTravelAlreadyOpen";
                    startingProgress = last.Progress;
                }
                if (startingProgress >= route.LengthProgress) return "RouteAlreadyComplete";
                var position = route.PositionAt(startingProgress);
                var actor = s.Actors.Single(x => x.Id == c.Actor);
                if (position == null || actor.X != position.X || actor.Y != position.Y) return "TravelerNotAtBoundRoutePosition";
                foreach (var binding in route.Positions)
                {
                    if (!WorldWalkable(s, binding.X, binding.Y)) return "RouteGeometryBlocked";
                    if (WorldSpatialQueries.Occupied(s, c.Actor, binding.X, binding.Y)) return "RouteGeometryOccupied";
                    bool hostileNear = s.WorldSchedule.Order.Where(id => id != c.Actor && !SoldierTacticalFeatures.IsAlly(s, c.Actor, id)
                        && s.Lives.Any(l => l.ActorId == id && !l.Dead)).Any(id => {
                            var other = s.Actors.Single(x => x.Id == id);
                            return WorldSpatialQueries.WithinRange(binding.X, binding.Y, other.X, other.Y, 1);
                        });
                    if (hostileNear) return "RoutePassesTacticalThreatBoundary";
                }
                if (route.Mapping == ExpeditionRouteMapping.Unknown)
                {
                    var segment = RouteSegment(s, route.Id, c.Actor, startingProgress);
                    if (!RouteReconnaissanceSelected(s) || segment == null
                        || segment.Status != ExpeditionRouteSegmentStatus.Feasible)
                        return "RouteRequiresReconnaissance";
                    segmentAward = segment.ProgressAward;
                }
                else segmentAward = ExpeditionRouteTravelRules.BaseProgress(route.Mapping);
                RuleQuantity remaining = route.LengthProgress - startingProgress;
                if (segmentAward == default || remaining < segmentAward) return "RouteTerminalProgressUnsupported";
                RuleQuantity segmentEndProgress = startingProgress + segmentAward;
                if (route.PositionAt(segmentEndProgress) == null
                    || route.NextPositionAfter(startingProgress) == null
                    || route.Positions.All(x => x.Progress != segmentEndProgress)) return "RouteSegmentEndpointUnbound";
                return null;
            }

            if (c.Kind != CommandKind.PauseRouteTravel && c.Kind != CommandKind.ResumeRouteTravel) return "InvalidRouteTravelRequest";
            if (current == null || current.RouteId != route.Id) return "NoMatchingRouteTravel";
            if (c.Kind == CommandKind.PauseRouteTravel)
                return current.Status == ExpeditionRouteTravelStatus.Moving ? null : "RouteTravelNotMoving";
            if (current.Status != ExpeditionRouteTravelStatus.Paused) return "RouteTravelNotPaused";
            if(HuntingTrapValidation.HasActiveTether(s,c.Actor))return "HuntingTrapTetherPreventsRouteTravel";
            string resumeControlFailure = RouteTravelControlFailure(s);
            if (resumeControlFailure != null) return resumeControlFailure;
            if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) <= 0) return "ConditionPreventsRouteTravel";
            bool detachedRejoin = routeMotionFixture != null && RouteSpatial(s, c.Actor)?.Detached == true;
            if (s.WorldTraversals.Any(x => x.ActorId != c.Actor)
                || s.WorldTraversals.Any(x => x.ActorId == c.Actor) && !detachedRejoin
                || OrdinaryInventory.Busy(s, c.Actor)
                || WorldActivityValidation.HasActiveLabor(s, c.Actor, s.RuleClock, s.RuleClock.AddSeconds(1))) return "RouteTravelerBusy";
            var currentPosition = route.PositionAt(current.Progress); var currentActor = s.Actors.Single(x => x.Id == c.Actor);
            var routeSpatial = RouteSpatial(s, c.Actor);
            if (routeMotionFixture != null)
            {
                if (routeSpatial == null || routeSpatial.RouteId != route.Id || routeSpatial.TravelStartedRevision != current.StartedRevision)
                    return "RoutePositionAuthorityMismatch";
                var expectedPose = routeMotionFixture.PositionAt(route.Id, current.Progress);
                if (routeSpatial.X != expectedPose.X || routeSpatial.Y != expectedPose.Y)
                    return "RoutePositionAuthorityMismatch";
                if (routeSpatial.Detached)
                {
                    var edge = s.WorldTraversals.SingleOrDefault(x => x.ActorId == c.Actor);
                    if (edge != null && edge.Status != WorldTraversalStatus.Suspended)
                        return "RouteRejoinRequiresSuspendedTraversal";
                    var actualPose = ObservationGeometry.Position(s, c.Actor);
                    if (actualPose.X != routeSpatial.X || actualPose.Y != routeSpatial.Y)
                        return "TravelerNotAtBoundRoutePosition";
                    if (edge == null && (routeSpatial.X.Denominator != 1 || routeSpatial.Y.Denominator != 1))
                        return "RouteRejoinTraversalRequired";
                }
                else if (currentActor.X != currentPosition.X || currentActor.Y != currentPosition.Y
                    || ObservationGeometry.Position(s, c.Actor).X != expectedPose.X
                    || ObservationGeometry.Position(s, c.Actor).Y != expectedPose.Y)
                    return "TravelerNotAtBoundRoutePosition";
            }
            else if (currentPosition == null || currentActor.X != currentPosition.X || currentActor.Y != currentPosition.Y)
                return "TravelerNotAtBoundRoutePosition";
            var resumeBurden = PortableEquipmentRules.CarriedBurden(s, c.Actor);
            if (!resumeBurden.Load.HasValue) return "RouteLoadEvidenceIncomplete";
            if (resumeBurden.Load.Value > route.CapacityLoad) return "RouteCapacitySettlementUnsupported";
            RuleQuantity segmentEnd = current.SegmentStartProgress + current.SegmentProgressAward;
            RuleQuantity resumeProgress = current.Progress;
            foreach (var binding in route.Positions.Where(x => x.Progress > resumeProgress && x.Progress <= segmentEnd))
            {
                if (!WorldWalkable(s, binding.X, binding.Y)) return "RouteGeometryBlocked";
                if (WorldSpatialQueries.Occupied(s, c.Actor, binding.X, binding.Y)) return "RouteGeometryOccupied";
                bool hostileNear = s.WorldSchedule.Order.Where(id => id != c.Actor && !SoldierTacticalFeatures.IsAlly(s, c.Actor, id)
                    && s.Lives.Any(l => l.ActorId == id && !l.Dead)).Any(id => {
                        var other = s.Actors.Single(x => x.Id == id);
                        return WorldSpatialQueries.WithinRange(binding.X, binding.Y, other.X, other.Y, 1);
                    });
                if (hostileNear) return "RoutePassesTacticalThreatBoundary";
            }
            return null;
        }

        private string RouteTravelControlFailure(Snapshot s)
        {
            // Preserve the original base-route rule for historical profiles. Schema 67's
            // pressure path may resume after a resolved encounter because combat pauses the
            // same route and the encounter record remains as canonical history.
            if (routeMotionFixture == null && s.SchemaVersion < Snapshot.ExpeditionPressureSchema)
                return s.InventoryCombat || s.Encounter != null ? "RouteTravelDuringTacticalControl" : null;
            // A completed conflict stays in the snapshot as history. Tactical control ends
            // only after the existing exit command has committed and the canonical conflict
            // record is resolved; retaining that record must not strand an admitted route.
            if (s.InventoryCombat || (s.Encounter != null && !ResolvedConflict(s)))
                return "RouteTravelDuringTacticalControl";
            return null;
        }

        private string ResolveRouteTravelCommand(Snapshot s, Command c)
        {
            string failure = AssessRouteTravelCommand(s, c, out var route, out var current, out var start, out var award);
            if (failure != null) return failure;
            if (c.Kind == CommandKind.StartRouteTravel)
            {
                s.RouteTravels = s.RouteTravels.Concat(new[] { new ExpeditionRouteTravelRecord(route.Id, c.Actor,
                    s.Revision + 1, start, award, start, default, route.Mapping, ExpeditionRouteTravelStatus.Moving,
                    route.Mapping == ExpeditionRouteMapping.Unknown) }).ToArray();
                if (route.Mapping == ExpeditionRouteMapping.Unknown)
                {
                    var segment = RouteSegment(s, route.Id, c.Actor, start);
                    if (segment == null || segment.Status != ExpeditionRouteSegmentStatus.Feasible)
                        throw new InvalidOperationException("RouteReconnaissanceFeasibilityDisappeared");
                    PutRouteSegment(s, segment.StartTravel(s.Revision + 1));
                }
                if (routeMotionFixture != null || huntingTrapFixture != null
                    || s.SchemaVersion >= Snapshot.RouteObservationSchema)
                {
                    var binding = route.PositionAt(start);
                    var poseX = routeMotionFixture == null ? new RuleQuantity(binding.X)
                        : routeMotionFixture.PositionAt(route.Id, start).X;
                    var poseY = routeMotionFixture == null ? new RuleQuantity(binding.Y)
                        : routeMotionFixture.PositionAt(route.Id, start).Y;
                    s.RouteTravelSpatial = s.RouteTravelSpatial.Concat(new[] { new ExpeditionRouteSpatialRecord(
                        route.Id, c.Actor, s.Revision + 1, poseX, poseY, false) }).ToArray();
                }
                RecordPressureRouteStart(s, route, c);
                return null;
            }
            if (c.Kind == CommandKind.ResumeRouteTravel && routeMotionFixture != null)
            {
                var spatial = RouteSpatial(s, c.Actor);
                if (spatial.Detached)
                {
                    var edge = s.WorldTraversals.SingleOrDefault(x => x.ActorId == c.Actor);
                    if (edge != null) s.WorldTraversals = s.WorldTraversals.Where(x => x.ActorId != c.Actor).ToArray();
                    var binding = route.PositionAt(current.Progress);
                    var actor = s.Actors.Single(x => x.Id == c.Actor);
                    actor.X = binding.X; actor.Y = binding.Y;
                    s.Clubs = s.Clubs.Select(x => x.HeldBy == actor.Id
                        ? new ClubInstance(x.Id, x.ProfileId, x.OwnerId, x.CustodianId, x.HeldBy, actor.X, actor.Y) : x).ToArray();
                    var pose = routeMotionFixture.PositionAt(route.Id, current.Progress);
                    SetRouteSpatial(s, spatial.With(pose.X, pose.Y, false));
                }
            }
            SetRouteTravel(s, current.With(current.NominalEffort,
                c.Kind == CommandKind.PauseRouteTravel ? ExpeditionRouteTravelStatus.Paused : ExpeditionRouteTravelStatus.Moving));
            return null;
        }

        private CommandQueryResult QueryRouteTravelCommand(Snapshot s, Command c)
        {
            string failure = AssessRouteTravelCommand(s, c, out _, out _, out _, out _);
            var costs = failure == null && c.Kind == CommandKind.StartRouteTravel
                ? new[] { new CommandCost("nominal-route-seconds", c.Target, ExpeditionRouteTravelRules.NominalSegmentSeconds) }
                : Array.Empty<CommandCost>();
            return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
        }

        private void ReconcileRouteTravel(Snapshot s)
        {
            foreach (var travel in s.RouteTravels.Where(x => x.Status == ExpeditionRouteTravelStatus.Moving).ToArray())
            {
                bool preserveEncounterBlock = routeMotionFixture == null
                    && s.SchemaVersion < Snapshot.ExpeditionPressureSchema;
                bool unresolvedTacticalControl = s.InventoryCombat
                    || (s.Encounter != null && (preserveEncounterBlock || !ResolvedConflict(s)));
                if (unresolvedTacticalControl || !Permissions(s, travel.TravelerId).VoluntarySpeed
                    || Speed(s, travel.TravelerId) <= 0)
                    SetRouteTravel(s, travel.With(travel.NominalEffort, ExpeditionRouteTravelStatus.Paused));
            }
        }

        private RuleTime? NextRouteTravelBoundary(Snapshot s)
        {
            RuleTime? result = null;
            foreach (var travel in s.RouteTravels.Where(x => x.Status == ExpeditionRouteTravelStatus.Moving))
            {
                var route = routeTravelFixture.Find(travel.RouteId);
                long speed = Speed(s, travel.TravelerId);
                if (speed <= 0) continue;
                RuleQuantity endProgress = travel.SegmentStartProgress + travel.SegmentProgressAward;
                var binding = route.NextPositionAfter(travel.Progress);
                RuleQuantity targetProgress = binding != null && binding.Progress < endProgress ? binding.Progress : endProgress;
                RuleTime targetEffort = ExpeditionRouteTravelRules.EffortAtProgress(travel.SegmentStartProgress,
                    travel.SegmentProgressAward, targetProgress);
                RuleTime remainingEffort = CampGreens.Subtract(targetEffort, travel.NominalEffort);
                if (remainingEffort == default) continue;
                RuleTime actual = ExpeditionRouteTravelRules.ActualMovingTime(remainingEffort, speed, route.Quality);
                RuleTime boundary = CampGreens.Add(s.RuleClock, actual);
                if (!result.HasValue || boundary < result.Value) result = boundary;
            }
            return result;
        }

        private string AdvanceRouteTravel(Snapshot s, RuleTime elapsed, RuleTime occurredAt)
        {
            foreach (var travel in s.RouteTravels.Where(x => x.Status == ExpeditionRouteTravelStatus.Moving).ToArray())
            {
                var route = routeTravelFixture.Find(travel.RouteId);
                var priorPosition = route.PositionAt(travel.Progress);
                long speed = Speed(s, travel.TravelerId);
                if (speed <= 0) continue;
                RuleTime earned = ExpeditionRouteTravelRules.EarnedNominalEffort(elapsed, speed, route.Quality);
                RuleTime effort = CampGreens.Add(travel.NominalEffort, earned);
                if (effort > new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds))
                    effort = new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds);
                var status = effort == new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds)
                    ? ExpeditionRouteTravelStatus.SegmentComplete : ExpeditionRouteTravelStatus.Moving;
                var updated = travel.With(effort, status);
                SetRouteTravel(s, updated);
                if (updated.Status == ExpeditionRouteTravelStatus.SegmentComplete)
                {
                    var segment = RouteSegmentForTravel(s, updated);
                    if (segment != null) PutRouteSegment(s, segment.CompleteTravel(s.Revision + 1));
                }
                var position = route.PositionAt(updated.Progress);
                var actor = s.Actors.Single(x => x.Id == updated.TravelerId);
                if (position != null && (actor.X != position.X || actor.Y != position.Y))
                {
                    actor.X = position.X; actor.Y = position.Y;
                    s.Clubs = s.Clubs.Select(c => c.HeldBy == actor.Id
                        ? new ClubInstance(c.Id, c.ProfileId, c.OwnerId, c.CustodianId, c.HeldBy, actor.X, actor.Y) : c).ToArray();
                }
                if(position!=null&&priorPosition!=null&&position.Progress==updated.Progress&&updated.Progress>travel.Progress
                    &&(priorPosition.X!=position.X||priorPosition.Y!=position.Y)) {
                    string entryId=HuntingTrapIdentity("route-entry|"+route.Id+"|"+updated.StartedRevision+"|"+position.Progress);
                    string trapError=QueueHuntingTrapEntry(s,updated.TravelerId,entryId,HuntingTrapEntryKind.RouteTravelCheckpoint,
                        position.X,position.Y,s.Revision+1,occurredAt,route.Id,updated.StartedRevision,position.Progress);
                    if(trapError!=null)return trapError;
                }
                if (routeMotionFixture != null)
                {
                    if (updated.Status == ExpeditionRouteTravelStatus.SegmentComplete)
                        s.RouteTravelSpatial = s.RouteTravelSpatial.Where(x => x.TravelStartedRevision != updated.StartedRevision).ToArray();
                    else
                    {
                        var pose = routeMotionFixture.PositionAt(route.Id, updated.Progress);
                        var spatial = RouteSpatial(s, updated.TravelerId);
                        if (spatial == null || spatial.Detached) throw new InvalidOperationException("MovingRouteSpatialAuthorityMissing");
                        SetRouteSpatial(s, spatial.With(pose.X, pose.Y, false));
                    }
                }
                else if (huntingTrapFixture != null || s.SchemaVersion >= Snapshot.RouteObservationSchema)
                {
                    if (updated.Status == ExpeditionRouteTravelStatus.SegmentComplete)
                        s.RouteTravelSpatial = s.RouteTravelSpatial.Where(x => x.TravelStartedRevision != updated.StartedRevision).ToArray();
                    else
                    {
                        if (position == null) throw new InvalidOperationException("MovingRoutePositionBindingMissing");
                        var spatial = RouteSpatial(s, updated.TravelerId);
                        if (spatial == null || spatial.Detached) throw new InvalidOperationException("MovingRouteSpatialAuthorityMissing");
                        SetRouteSpatial(s, spatial.With(new RuleQuantity(position.X), new RuleQuantity(position.Y), false));
                    }
                }
            }
            return null;
        }

        private List<ObservationMovementSegment> RouteObservationSegments(Snapshot s,
            IReadOnlyDictionary<long, RuleQuantity> progressBefore)
        {
            var result = new List<ObservationMovementSegment>();
            if (routeMotionFixture == null || observationFixture == null) return result;
            foreach (long startedRevision in progressBefore.Keys.OrderBy(x => x))
            {
                var travel = s.RouteTravels.SingleOrDefault(x => x.StartedRevision == startedRevision);
                if (travel == null || !progressBefore.TryGetValue(travel.StartedRevision, out var fromProgress)
                    || travel.Progress <= fromProgress) continue;
                var leg = routeMotionFixture.LegAt(travel.RouteId, fromProgress);
                if (leg == null || travel.Progress > leg.EndProgress)
                    throw new InvalidOperationException("RouteObservationSegmentCrossedAuthoredLeg");
                RuleQuantity fromDistance = leg.DistanceFeetAt(fromProgress);
                RuleQuantity toDistance = leg.DistanceFeetAt(travel.Progress);
                var edge = new WorldTraversalRecord(travel.TravelerId, travel.StartedRevision,
                    leg.FromX, leg.FromY, leg.ToX, leg.ToY, fromDistance, false, WorldTraversalStatus.Moving);
                result.Add(new ObservationMovementSegment(edge, fromDistance, toDistance));
            }
            return result;
        }

        private bool RouteTravelOpenForActor(Snapshot s, string actor)
            => routeTravelFixture != null && OpenRouteTravel(s, actor) != null;

        private string ValidateRouteTravelState(Snapshot s)
        {
            if (routeTravelFixture == null)
                return s.RouteTravels.Length == 0 ? null : "RouteTravelProfileMissing";
            int routeSchema = routeReconnaissanceFixture != null ? Snapshot.RouteReconnaissanceSchema
                : routeMappingWorkFixture != null ? Snapshot.RouteMappingWorkSchema
                : routeMappingFixture != null ? Snapshot.RouteMappingSchema
                : routeMotionFixture == null ? Snapshot.ExpeditionRouteSchema : Snapshot.RouteObservationSchema;
            if (s.SchemaVersion != routeSchema
                && !(expeditionPressureProfile != null && s.SchemaVersion >= Snapshot.ExpeditionPressureSchema
                    && s.SchemaVersion <= Snapshot.ExpeditionPressureLifecycleSchema
                    && routeSchema == Snapshot.ExpeditionRouteSchema)
                && !(characterAdvancement!=null&&characterAdvancement.LevelFourAdvancementEnabled
                    &&s.SchemaVersion==Snapshot.SharedCharacterAdvancementSchema&&routeSchema<Snapshot.SharedCharacterAdvancementSchema)
                && !(huntingTrapFixture != null && s.SchemaVersion == Snapshot.HuntingTrapSchema
                    && routeSchema < Snapshot.HuntingTrapSchema)
                && !(dodgeActionEnabled&&s.SchemaVersion==Snapshot.DodgeSchema&&routeSchema<Snapshot.DodgeSchema)
                && !(dailyProvisioning!=null&&s.SchemaVersion==Snapshot.DailyProvisioningSchema
                    &&routeSchema<Snapshot.DailyProvisioningSchema))
                return "RouteTravelSchemaMismatch";
            if (routeMotionFixture == null && ObservationRules.Enabled(s)) return "RouteObservationIntegrationUnsupported";
            string bindingError = routeMotionFixture == null
                ? routeTravelFixture.ValidateBindings(s, harvestFixture, worldConfiguration)
                : routeMotionFixture.ValidateBindings(s, routeTravelFixture, harvestFixture, worldConfiguration);
            if (bindingError != null) return bindingError;
            foreach (var group in s.RouteTravels.GroupBy(x => x.TravelerId + "|" + x.RouteId, StringComparer.Ordinal))
            {
                var history = group.OrderBy(x => x.StartedRevision).ToArray();
                var route = routeTravelFixture.Find(history[0].RouteId);
                if (route == null) return "RouteTravelDefinitionMissing";
                RuleQuantity expectedStart = default;
                foreach (var travel in history)
                {
                    var receipt = s.Receipts.SingleOrDefault(x => x.Revision == travel.StartedRevision);
                    var reconSegment = s.RouteSegments.SingleOrDefault(x => x.RouteId == travel.RouteId
                        && x.TravelerId == travel.TravelerId && x.StartingProgress == travel.SegmentStartProgress
                        && x.TravelStartedRevision == travel.StartedRevision);
                    RuleQuantity expectedAward = route.Mapping == ExpeditionRouteMapping.Unknown
                        ? reconSegment?.ProgressAward ?? default : ExpeditionRouteTravelRules.BaseProgress(route.Mapping);
                    if (travel.SegmentStartProgress != expectedStart || travel.StartingMapping != route.Mapping
                        || route.Positions.All(x => x.Progress != travel.SegmentStartProgress + travel.SegmentProgressAward)
                        || travel.SegmentProgressAward != expectedAward
                        || route.Mapping == ExpeditionRouteMapping.Unknown && (reconSegment == null
                            || reconSegment.FeasibilityAttemptId == ""
                            || reconSegment.Status != (travel.Status == ExpeditionRouteTravelStatus.SegmentComplete
                                ? ExpeditionRouteSegmentStatus.Complete : ExpeditionRouteSegmentStatus.Traveling))
                        || receipt == null) return "InvalidRouteTravelHistory";
                    Command command;
                    try { command = CommandHistory.Read(receipt); }
                    catch (ArgumentException) { return "InvalidRouteTravelHistory"; }
                    if (command.Kind != CommandKind.StartRouteTravel || command.Actor != travel.TravelerId || command.Target != travel.RouteId)
                        return "InvalidRouteTravelHistory";
                    expectedStart = travel.Progress;
                    if (travel != history[history.Length - 1] && travel.Status != ExpeditionRouteTravelStatus.SegmentComplete)
                        return "InvalidRouteTravelHistory";
                }
            }
            foreach (var travel in s.RouteTravels.Where(x => x.Status == ExpeditionRouteTravelStatus.Moving
                || x.Status == ExpeditionRouteTravelStatus.Paused))
            {
                var route = routeTravelFixture.Find(travel.RouteId);
                var binding = route?.PositionAt(travel.Progress);
                var actor = s.Actors.SingleOrDefault(x => x.Id == travel.TravelerId);
                var spatial = routeMotionFixture == null ? null : RouteSpatial(s, travel.TravelerId);
                if (binding == null || actor == null || travel.Status == ExpeditionRouteTravelStatus.Moving
                    && (actor.X != binding.X || actor.Y != binding.Y)
                    || routeMotionFixture != null && (spatial == null || spatial.RouteId != travel.RouteId
                        || spatial.TravelStartedRevision != travel.StartedRevision
                        || spatial.X != routeMotionFixture.PositionAt(route.Id, travel.Progress).X
                        || spatial.Y != routeMotionFixture.PositionAt(route.Id, travel.Progress).Y
                        || spatial.Detached && travel.Status != ExpeditionRouteTravelStatus.Paused
                        || !spatial.Detached && (actor.X != binding.X || actor.Y != binding.Y)))
                    return "TravelerNotAtBoundRoutePosition";
                if (routeMotionFixture == null
                    && (huntingTrapFixture != null || s.SchemaVersion >= Snapshot.RouteObservationSchema))
                {
                    var routeSpatial = RouteSpatial(s, travel.TravelerId);
                    if (routeSpatial == null || routeSpatial.Detached || routeSpatial.RouteId != travel.RouteId
                        || routeSpatial.TravelStartedRevision != travel.StartedRevision
                        || routeSpatial.X != new RuleQuantity(binding.X) || routeSpatial.Y != new RuleQuantity(binding.Y))
                        return "RouteTravelSpatialAuthorityMismatch";
                }
            }
            return null;
        }

    }
}
#endif
