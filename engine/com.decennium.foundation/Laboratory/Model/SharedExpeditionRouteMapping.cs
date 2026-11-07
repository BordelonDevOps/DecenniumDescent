#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>A synthetic, pre-resolved Map Route outcome for a TEST_ONLY profile. It does
    /// not claim that a check was run, that work elapsed, or that route passage was surveyed.</summary>
    public sealed class TestOnlyExpeditionRouteMappingResult
    {
        public string RouteId { get; }
        public string ResultId { get; }
        public string ActorId { get; }
        public string EvidenceId { get; }
        public RuleTime CompletedAt { get; }
        public ExpeditionRouteMappingResultDegree Degree { get; }

        public TestOnlyExpeditionRouteMappingResult(string routeId, string resultId, string actorId,
            string evidenceId, RuleTime completedAt, ExpeditionRouteMappingResultDegree degree)
        {
            if (!Validation.ValidId(routeId) || !Validation.ValidId(resultId) || !Validation.ValidId(actorId)
                || !Validation.ValidId(evidenceId) || completedAt < default(RuleTime)
                || !Enum.IsDefined(typeof(ExpeditionRouteMappingResultDegree), degree))
                throw new ArgumentException("Invalid synthetic route-mapping result fixture.");
            RouteId = routeId; ResultId = resultId; ActorId = actorId; EvidenceId = evidenceId;
            CompletedAt = completedAt; Degree = degree;
        }

        internal string Canonical => RouteId + "|" + ResultId + "|" + ActorId + "|" + EvidenceId + "|"
            + CompletedAt.Numerator.ToString(CultureInfo.InvariantCulture) + "/"
            + CompletedAt.Denominator.ToString(CultureInfo.InvariantCulture) + "|" + (int)Degree;
    }

    /// <summary>Finite, fingerprinted test outcomes attached to authored route content. These
    /// outcomes exercise persistence and accounting only; production Map Route checks remain gated.</summary>
    public sealed class TestOnlyExpeditionRouteMappingResultFixture
    {
        private const string PlayerBookSha256 = "4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480";
        private readonly TestOnlyExpeditionRouteMappingResult[] results;
        public string RouteFingerprint { get; }
        public string Fingerprint { get; }
        public System.Collections.Generic.IReadOnlyList<TestOnlyExpeditionRouteMappingResult> Results { get; }

        public TestOnlyExpeditionRouteMappingResultFixture(TestOnlyExpeditionRouteFixture routes,
            params TestOnlyExpeditionRouteMappingResult[] results)
        {
            if (routes == null || results == null || results.Length < 1
                || results.Length > ExpeditionRouteMappingRules.MaxResults || results.Any(x => x == null)
                || results.Select(x => x.ResultId).Distinct(StringComparer.Ordinal).Count() != results.Length
                || results.Any(x => routes.Routes.All(route => route.Id != x.RouteId)))
                throw new ArgumentException("Invalid TEST_ONLY route-mapping result fixture set.");
            RouteFingerprint = routes.Fingerprint;
            this.results = results.OrderBy(x => x.ResultId, StringComparer.Ordinal).ToArray();
            Results = Array.AsReadOnly(this.results);
            string key = "ex58-exact-2026-10-11|FL-10|TR-13|player-book-sha256=" + PlayerBookSha256
                + "|synthetic-pre-resolved-outcomes-v1|no-check-no-labor-no-passage-feasibility|"
                + RouteFingerprint + "|" + string.Join(";", this.results.Select(x => x.Canonical));
            using (var sha = SHA256.Create()) Fingerprint = "TEST_ONLY.route-map-results-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }

        internal TestOnlyExpeditionRouteMappingResult Find(string id) => results.SingleOrDefault(x => x.ResultId == id);

        internal string ValidateRoutes(TestOnlyExpeditionRouteFixture routes)
            => routes != null && routes.Fingerprint == RouteFingerprint
                && results.All(x => routes.Routes.Any(route => route.Id == x.RouteId))
                ? null : "RouteMappingFixtureMismatch";
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionRouteMappingResultFixture routeMappingFixture;

        /// <summary>Adds a schema54-only synthetic mapping-result harness to a selected route
        /// profile. It never upgrades authored route Mapping or enables Unknown-route passage.</summary>
        public TestOnlySharedWorldPolicy EnableTestOnlyRouteMappingResults(
            TestOnlyExpeditionRouteMappingResultFixture fixture)
        {
            if (initializationStarted) throw new InvalidOperationException("World initialization has already started.");
            if (routeTravelFixture == null || fixture == null || routeMappingFixture != null)
                throw new ArgumentException("Route mapping results require one selected route profile and one finite result fixture.");
            string error = fixture.ValidateRoutes(routeTravelFixture);
            if (error != null) throw new ArgumentException(error, nameof(fixture));
            routeMappingFixture = fixture;
            using (var sha = SHA256.Create()) ContentFingerprint = "TEST_ONLY.route-map-world-v1-"
                + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(ContentFingerprint + "|" + fixture.Fingerprint))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private static bool RouteMappingResultCommand(CommandKind kind)
            => kind == CommandKind.ConsumeTestOnlyRouteMappingResult;

        private string AssessRouteMappingResultCommand(Snapshot s, Command c,
            out TestOnlyExpeditionRouteMappingResult result, out TestOnlyExpeditionRoute route)
        {
            result = null; route = null;
            if (routeMappingFixture == null || routeTravelFixture == null) return "RouteMappingResultsNotEnabled";
            if (!RouteMappingSchemaActive(s) || c.Target == "" || !Validation.ValidId(c.Target)
                || c.X != 0 || c.Y != 0 || c.Inventory != null || c.Combat != null || c.Advancement != null
                || c.Ranged != null || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null
                || c.DefensiveFormation != null || c.ExpeditionAssignment != null || c.HarvestSelection != null
                || c.MiningSelection != null || c.ProspectingExposure != null)
                return "InvalidRouteMappingResultRequest";
            result = routeMappingFixture.Find(c.Target);
            if (result == null) return "UnknownTestOnlyRouteMappingResult";
            if (result.ActorId != c.Actor) return "RouteMappingResultActorMismatch";
            route = routeTravelFixture.Find(result.RouteId);
            if (route == null) return "RouteMappingDefinitionMissing";
            if (result.CompletedAt > s.RuleClock) return "RouteMappingResultNotComplete";
            string resultId = result.ResultId;
            if (s.RouteMappingResults.Any(x => x.ResultId == resultId)) return "RouteMappingResultAlreadyConsumed";
            if (s.RouteMappingResults.Length >= ExpeditionRouteMappingRules.MaxResults) return "RouteMappingHistoryCapacityReached";
            return null;
        }

        private string ResolveRouteMappingResultCommand(Snapshot s, Command c)
        {
            string failure = AssessRouteMappingResultCommand(s, c, out var result, out var route);
            if (failure != null) return failure;
            var before = ExpeditionRouteMappingRules.Current(s, route.Id, route.Mapping);
            var after = ExpeditionRouteMappingRules.Apply(before, route.Risk, result.Degree, out int marksGranted);
            s.RouteMappingResults = s.RouteMappingResults.Concat(new[] {
                new ExpeditionRouteMappingResultRecord(route.Id, result.ResultId, result.ActorId, c.Id,
                    ExpeditionRouteMappingRules.MapRouteOperationId, result.EvidenceId, routeMappingFixture.Fingerprint,
                    s.Revision + 1, result.CompletedAt, result.Degree, before.Mapping, after.Mapping,
                    before.UnspentMarks, marksGranted, after.UnspentMarks, synthetic: true)
            }).ToArray();
            return null;
        }

        private CommandQueryResult QueryRouteMappingResultCommand(Snapshot s, Command c)
        {
            string failure = AssessRouteMappingResultCommand(s, c, out _, out _);
            return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision,
                Array.Empty<CommandCost>());
        }

        private string ValidateRouteMappingResultState(Snapshot s)
        {
            if (routeMappingFixture == null)
                return s.RouteMappingResults.Length == 0 && s.SchemaVersion != Snapshot.RouteMappingSchema
                    ? null : "RouteMappingResultFixtureMissing";
            if (!RouteMappingSchemaActive(s) || routeTravelFixture == null
                || routeMappingFixture.ValidateRoutes(routeTravelFixture) != null)
                return "RouteMappingSchemaOrFixtureMismatch";
            foreach (var group in s.RouteMappingResults.GroupBy(x => x.RouteId, StringComparer.Ordinal))
            {
                var route = routeTravelFixture.Find(group.Key);
                if (route == null) return "RouteMappingDefinitionMissing";
                var current = new ExpeditionRouteMappingKnowledge(route.Mapping, 0);
                foreach (var record in group.OrderBy(x => x.AppliedRevision))
                {
                    var profile = routeMappingFixture.Find(record.ResultId);
                    var receipt = s.Receipts.SingleOrDefault(x => x.Revision == record.AppliedRevision);
                    if (profile == null || profile.RouteId != record.RouteId || profile.ActorId != record.ActorId
                        || profile.EvidenceId != record.EvidenceId || profile.CompletedAt != record.CompletedAt
                        || profile.Degree != record.Degree || record.OperationId != ExpeditionRouteMappingRules.MapRouteOperationId
                        || record.ResultProfileFingerprint != routeMappingFixture.Fingerprint || !record.Synthetic
                        || receipt == null || receipt.Id != record.CommandId)
                        return "InvalidRouteMappingResultEvidence";
                    Command command;
                    try { command = CommandHistory.Read(receipt); }
                    catch (ArgumentException) { return "InvalidRouteMappingResultCommand"; }
                    if (command.Kind != CommandKind.ConsumeTestOnlyRouteMappingResult
                        || command.Actor != record.ActorId || command.Target != record.ResultId
                        || command.ExpectedRevision + 1 != record.AppliedRevision
                        || profile.CompletedAt > s.RuleClock)
                        return "InvalidRouteMappingResultCommand";
                    var next = ExpeditionRouteMappingRules.Apply(current, route.Risk, record.Degree, out int marksGranted);
                    if (record.MappingBefore != current.Mapping || record.MarksBefore != current.UnspentMarks
                        || record.MappingAfter != next.Mapping || record.MarksGranted != marksGranted
                        || record.MarksAfter != next.UnspentMarks)
                        return "InvalidRouteMappingResultTransition";
                    current = next;
                }
            }
            return null;
        }

        private bool RouteMappingSchemaActive(Snapshot s)
            => s.SchemaVersion == Snapshot.RouteMappingSchema
                || huntingTrapFixture != null && s.SchemaVersion == Snapshot.HuntingTrapSchema;

    }
}
#endif
