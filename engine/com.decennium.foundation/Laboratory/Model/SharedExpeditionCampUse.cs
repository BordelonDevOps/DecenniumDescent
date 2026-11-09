#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Finite TEST_ONLY FL-07 camp facts, bound to one exact authored route checkpoint.
    /// This profile grants no construction, storage, safety, recovery, discovery, or Haven behavior.</summary>
    public sealed class TestOnlyExpeditionCampSiteFixture
    {
        public string Id { get; }
        public string RouteId { get; }
        public RuleQuantity RouteProgress { get; }
        public int FootprintWidthFeet { get; }
        public int FootprintHeightFeet { get; }
        public bool LegalAccess { get; }
        public bool Stable { get; }
        public bool Drainage { get; }
        public bool WeatherProtection { get; }
        public bool InhabitantSpace { get; }
        public bool GearSpace { get; }
        public bool Exposed { get; }
        public bool KnownToEnemies { get; }
        public bool Concealed { get; }
        public string Fingerprint { get; }

        public TestOnlyExpeditionCampSiteFixture(string id, string routeId, RuleQuantity routeProgress,
            bool legalAccess = true, bool stable = true, bool drainage = true, bool weatherProtection = true,
            bool inhabitantSpace = true, bool gearSpace = true, bool exposed = false,
            bool knownToEnemies = false, bool concealed = false,
            int footprintWidthFeet = 20, int footprintHeightFeet = 20)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(routeId) || routeProgress < default(RuleQuantity)
                || footprintWidthFeet != 20 || footprintHeightFeet != 20)
                throw new ArgumentException("Invalid TEST_ONLY camp site profile.");
            Id = id; RouteId = routeId; RouteProgress = routeProgress;
            LegalAccess = legalAccess; Stable = stable; Drainage = drainage; WeatherProtection = weatherProtection;
            InhabitantSpace = inhabitantSpace; GearSpace = gearSpace; Exposed = exposed;
            KnownToEnemies = knownToEnemies; Concealed = concealed;
            FootprintWidthFeet = footprintWidthFeet; FootprintHeightFeet = footprintHeightFeet;
            Fingerprint = "TEST_ONLY.camp-site-v1-" + Hash(Canonical);
        }

        internal string Canonical => string.Join("|", new[] {
            "MGT-03", "FL-07", "exact-paused-route-checkpoint-v1", Id, RouteId, RouteProgress.ToString(),
            FootprintWidthFeet.ToString(CultureInfo.InvariantCulture), FootprintHeightFeet.ToString(CultureInfo.InvariantCulture),
            Bit(LegalAccess), Bit(Stable), Bit(Drainage), Bit(WeatherProtection), Bit(InhabitantSpace), Bit(GearSpace),
            Bit(Exposed), Bit(KnownToEnemies), Bit(Concealed), "no-construction:no-storage:no-recovery:no-haven"
        });

        internal string BindFingerprint(string prior)
            => "TEST_ONLY.camp-world-v1-" + Hash(prior + "|" + Fingerprint);

        internal string ValidateRoute(TestOnlyExpeditionRouteFixture routes)
        {
            var route = routes?.Find(RouteId);
            if (route == null) return "CampSiteRouteUnknown";
            var binding = route.PositionAt(RouteProgress);
            return binding == null || binding.Progress != RouteProgress
                ? "CampSiteRequiresExactAuthoredRouteCheckpoint" : null;
        }

        private static string Bit(bool value) => value ? "1" : "0";
        private static string Hash(string value)
        {
            using (var sha = SHA256.Create())
                return string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(value))
                    .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionCampSiteFixture expeditionCampSiteProfile;

        /// <summary>Opt into the bounded TEST_ONLY FL-07 camp-use/Pressure link. Requires the
        /// existing fixed-cohort Pressure and route fixtures; it adds no construction procedure.</summary>
        public TestOnlySharedWorldPolicy EnableExpeditionCampUse(TestOnlyExpeditionCampSiteFixture fixture)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (fixture == null || expeditionCampSiteProfile != null)
                throw new ArgumentException("Supply one explicit camp-site fixture.");
            if (expeditionPressureProfile == null || routeTravelFixture == null)
                throw new InvalidOperationException("CampUseRequiresExpeditionPressureAndRouteTravel");
            string error = fixture.ValidateRoute(routeTravelFixture);
            if (error != null) throw new InvalidOperationException(error);
            expeditionCampSiteProfile = fixture;
            ContentFingerprint = fixture.BindFingerprint(ContentFingerprint);
            return this;
        }

        private void InitializeExpeditionCampUse(Snapshot s)
        {
            if (expeditionCampSiteProfile == null) return;
            var route = routeTravelFixture.Find(expeditionCampSiteProfile.RouteId);
            var position = route.PositionAt(expeditionCampSiteProfile.RouteProgress);
            s.ExpeditionCampSites = new[] { new ExpeditionCampSiteRecord(
                expeditionCampSiteProfile.Id, expeditionPressureProfile.CohortId, route.Id,
                expeditionCampSiteProfile.RouteProgress, routeTravelFixture.Fingerprint,
                expeditionCampSiteProfile.Fingerprint, position.X, position.Y,
                expeditionCampSiteProfile.FootprintWidthFeet, expeditionCampSiteProfile.FootprintHeightFeet,
                expeditionCampSiteProfile.LegalAccess, expeditionCampSiteProfile.Stable,
                expeditionCampSiteProfile.Drainage, expeditionCampSiteProfile.WeatherProtection,
                expeditionCampSiteProfile.InhabitantSpace, expeditionCampSiteProfile.GearSpace,
                expeditionCampSiteProfile.Exposed, expeditionCampSiteProfile.KnownToEnemies,
                expeditionCampSiteProfile.Concealed) };
            s.ExpeditionCampActivities = Array.Empty<ExpeditionCampActivityRecord>();
        }

        private string ValidateExpeditionCampFixtureState(Snapshot s)
        {
            if (expeditionCampSiteProfile == null)
                return s.ExpeditionCampSites.Length + s.ExpeditionCampActivities.Length == 0
                    ? null : "CampSiteFixtureMissing";
            if (expeditionPressureProfile == null || routeTravelFixture == null
                || s.SchemaVersion != Snapshot.ExpeditionCampUseSchema || s.ExpeditionCampSites.Length != 1)
                return "CampSiteProfileMismatch";
            string error = expeditionCampSiteProfile.ValidateRoute(routeTravelFixture);
            if (error != null) return error;
            var route = routeTravelFixture.Find(expeditionCampSiteProfile.RouteId);
            var position = route.PositionAt(expeditionCampSiteProfile.RouteProgress);
            var expected = new ExpeditionCampSiteRecord(expeditionCampSiteProfile.Id,
                expeditionPressureProfile.CohortId, route.Id, expeditionCampSiteProfile.RouteProgress,
                routeTravelFixture.Fingerprint, expeditionCampSiteProfile.Fingerprint,
                position.X, position.Y, expeditionCampSiteProfile.FootprintWidthFeet,
                expeditionCampSiteProfile.FootprintHeightFeet, expeditionCampSiteProfile.LegalAccess,
                expeditionCampSiteProfile.Stable, expeditionCampSiteProfile.Drainage,
                expeditionCampSiteProfile.WeatherProtection, expeditionCampSiteProfile.InhabitantSpace,
                expeditionCampSiteProfile.GearSpace, expeditionCampSiteProfile.Exposed,
                expeditionCampSiteProfile.KnownToEnemies, expeditionCampSiteProfile.Concealed);
            return s.ExpeditionCampSites[0].SameAs(expected) ? null : "CampSiteProfileMismatch";
        }

        private static bool IsExpeditionCampUseCommand(CommandKind kind)
            => kind == CommandKind.BeginCampUse || kind == CommandKind.EndCampUse
                || kind == CommandKind.BeginLyingLow || kind == CommandKind.EndLyingLow;

        private CommandQueryResult QueryExpeditionCampUse(Snapshot s, Command c)
        {
            if (expeditionCampSiteProfile == null)
                return new CommandQueryResult(false, false, "UnsupportedOperation", s.Revision);
            string error = ResolveExpeditionCampUse(s.Copy(), c);
            return new CommandQueryResult(true, error == null, error ?? "Available", s.Revision);
        }

        private string ResolveExpeditionCampUse(Snapshot s, Command c)
        {
            if (expeditionCampSiteProfile == null || s.SchemaVersion != Snapshot.ExpeditionCampUseSchema)
                return "CampUseNotSelected";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.SuppressionFire != null || c.DefensiveFormation != null || c.ExpeditionAssignment != null
                || c.HarvestSelection != null || c.MiningSelection != null || c.ProspectingExposure != null
                || c.RouteMappingWork != null || c.OverwatchRider != OverwatchRider.None
                || c.Target != expeditionCampSiteProfile.Id || c.X != 0 || c.Y != 0)
                return "InvalidCampUseCommand";
            if (c.Actor != expeditionPressureProfile.MemberId) return "CampUseCohortMemberRequired";
            var site = s.ExpeditionCampSites.SingleOrDefault(x => x.Id == expeditionCampSiteProfile.Id
                && x.CohortId == expeditionPressureProfile.CohortId);
            if (site == null) return "CampSiteProfileMismatch";
            var activities = s.ExpeditionCampActivities;
            var activeUse = activities.SingleOrDefault(x => x.Kind == ExpeditionCampActivityKind.Use
                && x.CohortId == site.CohortId && x.Active);
            var activeLow = activities.SingleOrDefault(x => x.Kind == ExpeditionCampActivityKind.LyingLow
                && x.CohortId == site.CohortId && x.Active);

            if (c.Kind == CommandKind.BeginCampUse)
            {
                if (!site.SupportsUse) return "CampSiteAccessBlockedOrUnsuitable";
                string locationError = CampCheckpointFailure(s, site);
                if (locationError != null) return locationError;
                if (s.InventoryCombat) return "CampUseRequiresExploration";
                if (activeUse != null) return "CampUseAlreadyActive";
                if (s.ExpeditionCampActivities.Length >= ExpeditionCampValidation.MaxActivities)
                    return "CampActivityHistoryCapacityReached";
                var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.CohortId == site.CohortId
                    && x.RouteId == site.RouteId && !x.EndedAt.HasValue);
                if (exposure == null || exposure.StartedAt > s.RuleClock) return "CampUseRequiresActiveRouteExposure";
                string id = CampActivityId(ExpeditionCampActivityKind.Use, site.Id, s.Revision + 1);
                s.ExpeditionCampActivities = activities.Concat(new[] { new ExpeditionCampActivityRecord(id,
                    site.CohortId, exposure.Id, site.Id, ExpeditionCampActivityKind.Use, "", s.RuleClock,
                    s.Revision + 1, c.Id) }).ToArray();
                return null;
            }

            if (c.Kind == CommandKind.EndCampUse)
            {
                if (activeUse == null) return "CampUseNotActive";
                s.ExpeditionCampActivities = activities.Select(x => x.Id == activeUse.Id || activeLow != null && x.Id == activeLow.Id
                    ? x.End(s.RuleClock, s.Revision + 1, c.Id, ExpeditionCampActivityEndReason.Command) : x).ToArray();
                return null;
            }

            if (c.Kind == CommandKind.BeginLyingLow)
            {
                if (s.InventoryCombat) return "LyingLowUnavailableDuringCombat";
                if (activeUse == null) return "LyingLowRequiresActiveCampUse";
                if (!site.Concealed) return "LyingLowRequiresConcealedSite";
                if (activeLow != null) return "LyingLowAlreadyActive";
                if (s.Work.WorkerIntervals.Any(x => x.WorkerId == c.Actor && x.Start <= s.RuleClock && x.End > s.RuleClock))
                    return "LyingLowConflictsWithActiveWork";
                if (s.RestIntervals.Any(x => x.ActorId == c.Actor && x.StartedAt <= s.RuleClock
                    && x.ScheduledEnd > s.RuleClock)) return "LyingLowConflictsWithRest";
                if (s.ExpeditionCampActivities.Length >= ExpeditionCampValidation.MaxActivities)
                    return "CampActivityHistoryCapacityReached";
                string id = CampActivityId(ExpeditionCampActivityKind.LyingLow, site.Id, s.Revision + 1);
                s.ExpeditionCampActivities = activities.Concat(new[] { new ExpeditionCampActivityRecord(id,
                    site.CohortId, activeUse.ExposureId, site.Id, ExpeditionCampActivityKind.LyingLow,
                    activeUse.Id, s.RuleClock, s.Revision + 1, c.Id) }).ToArray();
                return null;
            }

            if (c.Kind == CommandKind.EndLyingLow)
            {
                if (activeLow == null) return "LyingLowNotActive";
                s.ExpeditionCampActivities = activities.Select(x => x.Id == activeLow.Id
                    ? x.End(s.RuleClock, s.Revision + 1, c.Id, ExpeditionCampActivityEndReason.Command) : x).ToArray();
                return null;
            }
            return "InvalidCampUseCommand";
        }

        private string CampCheckpointFailure(Snapshot s, ExpeditionCampSiteRecord site)
        {
            string member = expeditionPressureProfile.MemberId;
            if (s.WorldTraversals.Length != 0) return "CampUseBlockedByPendingTraversal";
            var travel = s.RouteTravels.SingleOrDefault(x => x.RouteId == site.RouteId && x.TravelerId == member
                && (x.Status == ExpeditionRouteTravelStatus.Moving || x.Status == ExpeditionRouteTravelStatus.Paused));
            if (travel == null || travel.Status != ExpeditionRouteTravelStatus.Paused
                || travel.Progress != site.RouteProgress) return "CampUseRequiresPausedAuthoredCheckpoint";
            var spatial = s.RouteTravelSpatial.SingleOrDefault(x => x.RouteId == site.RouteId
                && x.TravelerId == member);
            bool detached = s.RouteTravelSpatial.Any(x => x.RouteId == site.RouteId
                && x.TravelerId == member && x.Detached);
            var physical = WorldPositionResolver.Position(s, member);
            var actor = s.Actors.Single(x => x.Id == member);
            if (detached || spatial != null && (spatial.X != new RuleQuantity(site.RouteX)
                    || spatial.Y != new RuleQuantity(site.RouteY))
                || physical.X != new RuleQuantity(site.RouteX) || physical.Y != new RuleQuantity(site.RouteY)
                || actor.X != site.RouteX || actor.Y != site.RouteY)
                return "CampUseRequiresPhysicalCheckpointPresence";
            if (!TestOnlyPolicy.Walkable(site.RouteX, site.RouteY)
                || WorldSpatialQueries.Occupied(s, member, site.RouteX, site.RouteY))
                return "CampSiteAccessBlockedOrOccupied";
            return null;
        }

        private void ApplyExpeditionCampTransitions(Snapshot s, Command c)
        {
            if (expeditionCampSiteProfile == null) return;
            string cohort = expeditionPressureProfile.CohortId;
            string member = expeditionPressureProfile.MemberId;
            ExpeditionCampActivityEndReason? interruption = null;
            bool endUse = false;
            if (c.Kind == CommandKind.BeginFixedEncounter || c.Kind == CommandKind.EnterInventoryCombat)
                interruption = ExpeditionCampActivityEndReason.Combat;
            if (c.Actor == member && (c.Kind == CommandKind.BeginWorldStep || c.Kind == CommandKind.ResumeWorldStep
                || c.Kind == CommandKind.StartRouteTravel || c.Kind == CommandKind.ResumeRouteTravel)
                )
            {
                interruption = ExpeditionCampActivityEndReason.Travel;
                endUse = true;
            }
            if (c.Kind == CommandKind.TacticalStep || c.Kind == CommandKind.TacticalRepositionStep)
            {
                var site = s.ExpeditionCampSites.Single(x => x.Id == expeditionCampSiteProfile.Id);
                var actor = s.Actors.Single(x => x.Id == member);
                if (actor.X != site.RouteX || actor.Y != site.RouteY)
                {
                    interruption = ExpeditionCampActivityEndReason.Travel;
                    endUse = true;
                }
            }
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == member && x.Start == s.RuleClock && x.End > x.Start))
                interruption = ExpeditionCampActivityEndReason.Work;
            if (!interruption.HasValue) return;
            s.ExpeditionCampActivities = s.ExpeditionCampActivities.Select(x =>
                x.CohortId == cohort && x.Active && (x.Kind == ExpeditionCampActivityKind.LyingLow
                    || endUse && x.Kind == ExpeditionCampActivityKind.Use)
                    ? x.End(s.RuleClock, s.Revision + 1, c.Id, interruption.Value) : x).ToArray();
        }

        private RuleTime? NextCampUseBoundary(Snapshot s)
        {
            if (expeditionCampSiteProfile == null) return null;
            var activeLow = s.ExpeditionCampActivities.Where(x => x.Kind == ExpeditionCampActivityKind.LyingLow && x.Active).ToArray();
            if (activeLow.Length == 0) return null;
            string[] members = activeLow.Select(x => x.CohortId).Distinct(StringComparer.Ordinal)
                .SelectMany(id => s.ExpeditionPressureCohorts.Single(x => x.Id == id).Members).ToArray();
            return s.Work.WorkerIntervals.Where(x => members.Contains(x.WorkerId, StringComparer.Ordinal)
                    && x.Start > s.RuleClock)
                .Select(x => (RuleTime?)x.Start).OrderBy(x => x.Value).FirstOrDefault();
        }

        private string RecordCampPressureEvidence(Snapshot s, ExpeditionPressureExposureRecord exposure,
            long watch, RuleTime at)
        {
            if (expeditionCampSiteProfile == null) return null;
            var site = s.ExpeditionCampSites.Single(x => x.Id == expeditionCampSiteProfile.Id);
            RuleTime watchStart = new RuleTime(checked(watch * ExpeditionPressureRules.WatchSeconds));
            RuleTime watchEnd = watchStart.AddSeconds(ExpeditionPressureRules.WatchSeconds);
            bool campKnownForPressure = site.Exposed || site.KnownToEnemies;
            foreach (var use in s.ExpeditionCampActivities.Where(x => x.CohortId == exposure.CohortId
                && x.ExposureId == exposure.Id && x.CampId == site.Id && x.Kind == ExpeditionCampActivityKind.Use))
            {
                if (!campKnownForPressure) continue;
                RuleTime start = use.StartedAt > watchStart ? use.StartedAt : watchStart;
                if (exposure.StartedAt > start) start = exposure.StartedAt;
                RuleTime end = at < watchEnd ? at : watchEnd;
                if (use.EndedAt.HasValue && use.EndedAt.Value < end) end = use.EndedAt.Value;
                if (exposure.EndedAt.HasValue && exposure.EndedAt.Value < end) end = exposure.EndedAt.Value;
                if (end <= start) continue;
                string error = AddCampPressureEvidence(s, exposure, ExpeditionPressureChangeKind.ExposedCampUse,
                    use, watch, start);
                if (error != null) return error;
            }

            foreach (var low in s.ExpeditionCampActivities.Where(x => x.CohortId == exposure.CohortId
                && x.ExposureId == exposure.Id && x.CampId == site.Id && x.Kind == ExpeditionCampActivityKind.LyingLow))
            {
                if (!site.Concealed || !ExpeditionCampValidation.CoversWatch(low, watch)
                    || exposure.StartedAt > watchStart
                    || exposure.EndedAt.HasValue && exposure.EndedAt.Value < watchEnd)
                    continue;
                var parent = s.ExpeditionCampActivities.SingleOrDefault(x => x.Id == low.ParentUseId
                    && x.Kind == ExpeditionCampActivityKind.Use && x.CohortId == low.CohortId
                    && x.CampId == low.CampId && x.ExposureId == low.ExposureId);
                if (parent == null || !ExpeditionCampValidation.CoversWatch(parent, watch)) continue;
                string error = AddCampPressureEvidence(s, exposure, ExpeditionPressureChangeKind.FullWatchLyingLow,
                    low, watch, watchEnd);
                if (error != null) return error;
            }
            return null;
        }

        private static string AddCampPressureEvidence(Snapshot s, ExpeditionPressureExposureRecord exposure,
            ExpeditionPressureChangeKind kind, ExpeditionCampActivityRecord activity, long watch, RuleTime at)
        {
            string id = CampPressureEvidenceId(kind, activity.Id, watch);
            if (s.ExpeditionPressureChanges.Any(x => x.Id == id)) return null;
            if (s.ExpeditionPressureChanges.Length >= ExpeditionPressureValidation.MaxChanges)
                return "ExpeditionPressureChangeCapacityReached";
            var change = new ExpeditionPressureChangeRecord(id, exposure.CohortId, exposure.Id,
                exposure.RouteId, watch, kind, activity.Id, activity.StartedRevision, at);
            s.ExpeditionPressureChanges = s.ExpeditionPressureChanges.Concat(new[] { change }).ToArray();
            return null;
        }

        private static string CampPressureEvidenceId(ExpeditionPressureChangeKind kind, string sourceId, long watch)
        {
            using (var sha = SHA256.Create())
            {
                string canonical = ((int)kind).ToString(CultureInfo.InvariantCulture) + "|"
                    + watch.ToString(CultureInfo.InvariantCulture) + "|" + sourceId;
                string hash = string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(canonical))
                    .Take(24).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
                return "camp-pressure-" + hash;
            }
        }

        private static string CampActivityId(ExpeditionCampActivityKind kind, string siteId, long revision)
        {
            using (var sha = SHA256.Create())
            {
                string canonical = ((int)kind).ToString(CultureInfo.InvariantCulture) + "|" + siteId
                    + "|" + revision.ToString(CultureInfo.InvariantCulture);
                string hash = string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(canonical))
                    .Take(24).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
                return "camp-activity-" + hash;
            }
        }

        private void ProcessCampUseBoundary(Snapshot s, Command initiating)
        {
            if (expeditionCampSiteProfile == null || initiating == null) return;
            string member = expeditionPressureProfile.MemberId;
            bool workStarts = s.Work.WorkerIntervals.Any(x => x.WorkerId == member
                && x.Start == s.RuleClock && x.End > x.Start);
            var closedRoute = s.ExpeditionPressureCheckpoints.Any(x => x.CohortId == expeditionPressureProfile.CohortId
                && x.At == s.RuleClock && x.CommandId == initiating.Id
                && x.Consequence == ExpeditionPressureConsequenceKind.RouteClosure);
            if (!workStarts && !closedRoute) return;
            var reason = closedRoute ? ExpeditionCampActivityEndReason.PressureClosure
                : ExpeditionCampActivityEndReason.Work;
            s.ExpeditionCampActivities = s.ExpeditionCampActivities.Select(x =>
                x.CohortId == expeditionPressureProfile.CohortId && x.Active
                    && (x.Kind == ExpeditionCampActivityKind.LyingLow || closedRoute && x.Kind == ExpeditionCampActivityKind.Use)
                    ? x.End(s.RuleClock, s.Revision + 1, initiating.Id, reason) : x).ToArray();
        }

        private System.Collections.Generic.IEnumerable<Command> DiscoverExpeditionCampUseCommands(Snapshot s, string actor)
        {
            if (expeditionCampSiteProfile == null || actor != expeditionPressureProfile.MemberId
                || s.InventoryCombat) yield break;
            var site = s.ExpeditionCampSites.SingleOrDefault(x => x.Id == expeditionCampSiteProfile.Id);
            if (site == null) yield break;
            string prefix = "option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".camp.";
            var activeUse = s.ExpeditionCampActivities.SingleOrDefault(x => x.Kind == ExpeditionCampActivityKind.Use
                && x.CohortId == site.CohortId && x.Active);
            var activeLow = s.ExpeditionCampActivities.SingleOrDefault(x => x.Kind == ExpeditionCampActivityKind.LyingLow
                && x.CohortId == site.CohortId && x.Active);
            if (activeLow != null)
                yield return new Command(prefix + "lying-low.end", actor, s.Revision,
                    CommandKind.EndLyingLow, site.Id);
            else if (activeUse != null && site.Concealed)
                yield return new Command(prefix + "lying-low.begin", actor, s.Revision,
                    CommandKind.BeginLyingLow, site.Id);
            if (activeUse != null)
                yield return new Command(prefix + "use.end", actor, s.Revision,
                    CommandKind.EndCampUse, site.Id);
            else
                yield return new Command(prefix + "use.begin", actor, s.Revision,
                    CommandKind.BeginCampUse, site.Id);
        }
    }
}
#endif
