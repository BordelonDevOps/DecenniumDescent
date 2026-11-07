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

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionRouteFixture routeTravelFixture;

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

        private void InitializeExpeditionRouteTravel(Snapshot s)
        {
            if (routeTravelFixture == null) return;
            if (observationFixture != null) throw new InvalidOperationException("RouteObservationIntegrationUnsupported");
            string error = routeTravelFixture.ValidateBindings(s, harvestFixture, worldConfiguration);
            if (error != null) throw new InvalidOperationException(error);
            s.RouteTravels = Array.Empty<ExpeditionRouteTravelRecord>();
        }

        private static bool RouteTravelCommand(CommandKind kind)
            => kind == CommandKind.StartRouteTravel || kind == CommandKind.PauseRouteTravel || kind == CommandKind.ResumeRouteTravel;

        private static ExpeditionRouteTravelRecord OpenRouteTravel(Snapshot s, string actor)
            => s.RouteTravels.Where(x => x.TravelerId == actor && x.Status != ExpeditionRouteTravelStatus.SegmentComplete)
                .SingleOrDefault();

        private static ExpeditionRouteTravelRecord LatestRouteTravel(Snapshot s, string routeId, string actor)
            => s.RouteTravels.Where(x => x.RouteId == routeId && x.TravelerId == actor)
                .OrderByDescending(x => x.StartedRevision).FirstOrDefault();

        private void SetRouteTravel(Snapshot s, ExpeditionRouteTravelRecord value)
            => s.RouteTravels = s.RouteTravels.Select(x => x.StartedRevision == value.StartedRevision ? value : x).ToArray();

        private string AssessRouteTravelCommand(Snapshot s, Command c, out TestOnlyExpeditionRoute route,
            out ExpeditionRouteTravelRecord current, out RuleQuantity startingProgress, out RuleQuantity segmentAward)
        {
            route = null; current = null; startingProgress = default; segmentAward = default;
            if (routeTravelFixture == null) return "RouteTravelNotEnabled";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.Target == "" || c.X != 0 || c.Y != 0 || !Validation.ValidId(c.Target)) return "InvalidRouteTravelRequest";
            route = routeTravelFixture.Find(c.Target);
            if (route == null) return "UnknownRoute";
            current = OpenRouteTravel(s, c.Actor);
            if (c.Kind == CommandKind.StartRouteTravel)
            {
                if (current != null) return "RouteTravelAlreadyOpen";
                if (s.InventoryCombat || s.Encounter != null) return "RouteTravelDuringTacticalControl";
                if (s.WorldTraversals.Length != 0) return "RouteTravelConflictsWithGridTraversal";
                if (s.RouteTravels.Count(x => x.Status == ExpeditionRouteTravelStatus.SegmentComplete) >= ExpeditionRouteTravelValidation.MaxRecords)
                    return "RouteTravelHistoryCapacityReached";
                if (s.RouteTravels.Any(x => x.Status == ExpeditionRouteTravelStatus.Moving)) return "ConcurrentRouteTravelUnsupported";
                if (route.Risk != 0) return "RouteRiskResolutionUnsupported";
                if (route.Quality != ExpeditionRouteQuality.Secured) return "RouteQualityConsequenceUnsupported";
                if (route.Mapping == ExpeditionRouteMapping.Unknown) return "RouteRequiresReconnaissance";
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
                segmentAward = ExpeditionRouteTravelRules.BaseProgress(route.Mapping);
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
            if (s.InventoryCombat || s.Encounter != null) return "RouteTravelDuringTacticalControl";
            if (!Permissions(s, c.Actor).VoluntarySpeed || Speed(s, c.Actor) <= 0) return "ConditionPreventsRouteTravel";
            if (s.WorldTraversals.Any(x => x.ActorId == c.Actor) || OrdinaryInventory.Busy(s, c.Actor)
                || WorldActivityValidation.HasActiveLabor(s, c.Actor, s.RuleClock, s.RuleClock.AddSeconds(1))) return "RouteTravelerBusy";
            var currentPosition = route.PositionAt(current.Progress); var currentActor = s.Actors.Single(x => x.Id == c.Actor);
            if (currentPosition == null || currentActor.X != currentPosition.X || currentActor.Y != currentPosition.Y)
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

        private string ResolveRouteTravelCommand(Snapshot s, Command c)
        {
            string failure = AssessRouteTravelCommand(s, c, out var route, out var current, out var start, out var award);
            if (failure != null) return failure;
            if (c.Kind == CommandKind.StartRouteTravel)
            {
                s.RouteTravels = s.RouteTravels.Concat(new[] { new ExpeditionRouteTravelRecord(route.Id, c.Actor,
                    s.Revision + 1, start, award, start, default, route.Mapping, ExpeditionRouteTravelStatus.Moving) }).ToArray();
                return null;
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
                if (s.InventoryCombat || s.Encounter != null || !Permissions(s, travel.TravelerId).VoluntarySpeed
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

        private void AdvanceRouteTravel(Snapshot s, RuleTime elapsed)
        {
            foreach (var travel in s.RouteTravels.Where(x => x.Status == ExpeditionRouteTravelStatus.Moving).ToArray())
            {
                var route = routeTravelFixture.Find(travel.RouteId);
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
                var position = route.PositionAt(updated.Progress);
                var actor = s.Actors.Single(x => x.Id == updated.TravelerId);
                if (position != null && (actor.X != position.X || actor.Y != position.Y))
                {
                    actor.X = position.X; actor.Y = position.Y;
                    s.Clubs = s.Clubs.Select(c => c.HeldBy == actor.Id
                        ? new ClubInstance(c.Id, c.ProfileId, c.OwnerId, c.CustodianId, c.HeldBy, actor.X, actor.Y) : c).ToArray();
                }
            }
        }

        private bool RouteTravelOpenForActor(Snapshot s, string actor)
            => routeTravelFixture != null && OpenRouteTravel(s, actor) != null;

        private string ValidateRouteTravelState(Snapshot s)
        {
            if (routeTravelFixture == null)
                return s.RouteTravels.Length == 0 ? null : "RouteTravelProfileMissing";
            if (s.SchemaVersion != Snapshot.ExpeditionRouteSchema) return "RouteTravelSchemaMismatch";
            if (ObservationRules.Enabled(s)) return "RouteObservationIntegrationUnsupported";
            string bindingError = routeTravelFixture.ValidateBindings(s, harvestFixture, worldConfiguration);
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
                    if (travel.SegmentStartProgress != expectedStart || travel.StartingMapping != route.Mapping
                        || route.Positions.All(x => x.Progress != travel.SegmentStartProgress + travel.SegmentProgressAward)
                        || travel.SegmentProgressAward != ExpeditionRouteTravelRules.BaseProgress(route.Mapping)
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
            foreach (var travel in s.RouteTravels.Where(x => x.Status != ExpeditionRouteTravelStatus.SegmentComplete))
            {
                var route = routeTravelFixture.Find(travel.RouteId);
                var binding = route?.PositionAt(travel.Progress);
                var actor = s.Actors.SingleOrDefault(x => x.Id == travel.TravelerId);
                if (binding == null || actor == null || travel.Status == ExpeditionRouteTravelStatus.Moving
                    && (actor.X != binding.X || actor.Y != binding.Y))
                    return "TravelerNotAtBoundRoutePosition";
            }
            return null;
        }

    }
}
#endif
