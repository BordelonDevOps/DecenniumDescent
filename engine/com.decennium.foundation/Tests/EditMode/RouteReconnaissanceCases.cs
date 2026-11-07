#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlyExpeditionRouteReconnaissanceFixture RouteReconnaissanceProfile(
            TestOnlyExpeditionRouteFixture routes, int tier = 1,
            params TestOnlyRouteReconnaissanceSkillFact[] skills)
        {
            var route = routes.Routes.Single(x => x.Id == RouteTravelId);
            var endpoint = route.Positions.Single(x => x.Progress == route.LengthProgress);
            var inspection = new TestOnlyRouteReconnaissanceInspectionProfile(
                "inspection.route-cache-to-plot", route.Id, endpoint.X, endpoint.Y);
            return new TestOnlyExpeditionRouteReconnaissanceFixture(routes,
                new[] { new TestOnlyRouteReconnaissanceTaskProfile(RouteTravelId, tier, inspection) }, skills);
        }

        private static TestOnlySharedWorldPolicy RouteReconnaissancePolicy(
            TestOnlyExpeditionRouteFixture routes, uint seed, int tier = 1,
            ConditionCombatFixture conditions = null,
            params TestOnlyRouteReconnaissanceSkillFact[] skills)
            => new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(seed: seed),
                new SupplyCacheFixture(), conditions: conditions)
                .EnableRouteObservationIntegration(routes, RouteTravelMotionFixture(routes), RouteTravelObservationFixture())
                .EnableRouteReconnaissance(RouteReconnaissanceProfile(routes, tier, skills));

        private static ObservationFixture RouteReconnaissanceBlockedSightFixture()
            => new ObservationFixture(5, 5, new[] { new ObservationGridCell(2, 2, true, false, false) }, new[] {
                new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
            });

        private static Command RouteReconnaissanceCommand(Simulation s, CommandKind kind,
            string target, string id, string actor = TestOnlyPolicy.ActorId)
            => new Command(id, actor, s.Capture().Revision, kind, target);

        private static void AddRouteReconnaissanceCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("unknown_route_requires_scoped_reconnaissance_then_shared_travel", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var policy = RouteReconnaissancePolicy(routes, SeedForD20(20), 1, null,
                    new TestOnlyRouteReconnaissanceSkillFact(TestOnlyPolicy.ActorId, 1));
                var simulation = World(policy);
                Snapshot replayStart = simulation.Capture();
                RouteTravelReachSource(simulation);

                var routeStart = RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "route.recon.no-bypass.before-check");
                RejectUnchanged(simulation, host, routeStart, "RouteRequiresReconnaissance");
                var begin = RouteReconnaissanceCommand(simulation, CommandKind.StartRouteReconnaissance,
                    RouteTravelId, "route.recon.start");
                var beginQuery = simulation.QueryCommand(host, begin);
                Require(beginQuery.Admissible && beginQuery.Costs.Single().Kind == "active-work-seconds"
                    && beginQuery.Costs.Single().Amount == TestOnlyExpeditionRouteReconnaissanceFixture.RequiredWorkSeconds,
                    "Reconnaissance did not quote the source-derived full active-work interval.");
                WorldCommit(simulation, begin);
                var attemptId = simulation.Capture().RouteReconnaissanceAttempts.Single().Id;
                WorldAdvance(simulation, 120);
                var after120 = simulation.Capture();
                var after120Attempt = after120.RouteReconnaissanceAttempts.Single();
                Require(after120Attempt.Status == ExpeditionRouteReconnaissanceStatus.Working,
                    "Reconnaissance did not remain active after 120 seconds: status=" + after120Attempt.Status
                    + " work=" + after120Attempt.WorkDone + " actor="
                    + after120.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X + ","
                    + after120.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y
                    + " clock=" + after120.RuleClock + " traversals=" + after120.WorldTraversals.Length
                    + " routes=" + after120.RouteTravels.Length + " procedures="
                    + string.Join(",", WorldActivityProjection.CurrentWork(after120).Select(x => x.Id + ":" + x.ActorId)));
                WorldCommit(simulation, RouteReconnaissanceCommand(simulation,
                    CommandKind.PauseRouteReconnaissance, attemptId, "route.recon.pause"));
                var pausedBytes = Bytes(simulation);
                simulation = new Simulation(policy, new SnapshotCodec().Decode(pausedBytes), ExecutionProfile.Laboratory);
                Require(pausedBytes.SequenceEqual(Bytes(simulation)),
                    "Paused reconnaissance work did not preserve canonical save bytes.");
                var resume = RouteReconnaissanceCommand(simulation, CommandKind.ResumeRouteReconnaissance,
                    attemptId, "route.recon.resume");
                var resumeQuery = simulation.QueryCommand(host, resume);
                Require(resumeQuery.Admissible && resumeQuery.Costs.Single().Amount == 28680,
                    "Resume did not retain exactly the work already completed.");
                WorldCommit(simulation, resume);
                WorldAdvance(simulation, 28679);
                var beforeBoundary = simulation.Capture().RouteReconnaissanceAttempts.Single();
                Require(beforeBoundary.Status == ExpeditionRouteReconnaissanceStatus.Working
                    && beforeBoundary.WorkDone == new RuleTime(28799) && beforeBoundary.Check == null,
                    "Reconnaissance resolved before its final active-work second.");
                WorldAdvance(simulation, 1);
                var feasible = simulation.Capture();
                var segment = feasible.RouteSegments.Single();
                var attempt = feasible.RouteReconnaissanceAttempts.Single();
                Require(attempt.Status == ExpeditionRouteReconnaissanceStatus.Resolved
                    && attempt.WorkDone == new RuleTime(28800) && attempt.Check != null
                    && attempt.Check.Natural == 20 && attempt.Check.ProficiencyRank == 1
                    && attempt.Check.Dc == 12 && attempt.Check.Degree == ExpeditionRouteReconnaissanceDegree.CriticalSuccess
                    && attempt.InspectionProfileId == RouteReconnaissanceProfile(routes).Tasks.Single().Inspection.Id
                    && attempt.InspectionProfileFingerprint == RouteReconnaissanceProfile(routes).Tasks.Single().Inspection.Fingerprint
                    && segment.Status == ExpeditionRouteSegmentStatus.Feasible
                    && segment.FeasibilityAttemptId == attempt.Id && segment.ProgressAward == new RuleQuantity(2)
                    && segment.PressureReductionBlockedAtFloor
                    && routes.Routes.Single().Mapping == ExpeditionRouteMapping.Unknown
                    && feasible.RouteMappingResults.Length == 0,
                    "The resolved check did not establish one scoped Unknown-route segment and critical benefit.");

                var allowedTravel = RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "route.recon.travel.start");
                var travelQuery = simulation.QueryCommand(host, allowedTravel);
                Require(travelQuery.Admissible, "Successful reconnaissance did not authorize its exact segment: " + travelQuery.Code);
                WorldCommit(simulation, allowedTravel);
                Require(simulation.Capture().RouteSegments.Single().Status == ExpeditionRouteSegmentStatus.Traveling,
                    "Starting passage did not consume feasibility into a traveling segment.");
                long travelSpeed = TestOnlyClubAttackPolicy.WalkingSpeed(simulation.Capture(), TestOnlyPolicy.ActorId);
                RuleTime actualTravelTime = ExpeditionRouteTravelRules.ActualMovingTime(
                    new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds), travelSpeed,
                    ExpeditionRouteQuality.Secured);
                WorldAdvance(simulation, checked((int)actualTravelTime.Numerator),
                    checked((int)actualTravelTime.Denominator));
                var completed = simulation.Capture();
                var settledTravel = completed.RouteTravels.Single();
                var settledSegment = completed.RouteSegments.Single();
                var settledActor = completed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                Require(settledTravel.Status == ExpeditionRouteTravelStatus.SegmentComplete
                    && settledTravel.StartingMapping == ExpeditionRouteMapping.Unknown
                    && settledTravel.SegmentProgressAward == new RuleQuantity(2)
                    && settledTravel.Progress == new RuleQuantity(2)
                    && settledSegment.Status == ExpeditionRouteSegmentStatus.Complete
                    && settledActor.X == 2 && settledActor.Y == 3,
                    "The authorized passage did not settle through the shared route movement and clock records: travel="
                    + settledTravel.Status + " mapping=" + settledTravel.StartingMapping + " award="
                    + settledTravel.SegmentProgressAward + " progress=" + settledTravel.Progress
                    + " segment=" + settledSegment.Status + " travel-rev=" + settledSegment.TravelStartedRevision
                    + " done-rev=" + settledSegment.TravelCompletedRevision + " actor=" + settledActor.X + "," + settledActor.Y
                    + " clock=" + completed.RuleClock);
                byte[] finalBytes = Bytes(simulation);
                Require(finalBytes.SequenceEqual(Bytes(new Simulation(policy, new SnapshotCodec().Decode(finalBytes),
                    ExecutionProfile.Laboratory))), "Schema60 reconnaissance and travel changed on save/restore.");
                var replay = new Simulation(policy, replayStart, ExecutionProfile.Laboratory);
                foreach (var receipt in completed.Receipts.OrderBy(x => x.Revision))
                {
                    var replayed = replay.Execute(host, CommandHistory.Read(receipt));
                    Require(replayed.Outcome == Outcome.Committed,
                        "Reconnaissance and travel history failed to replay at revision " + receipt.Revision + ".");
                }
                Require(finalBytes.SequenceEqual(Bytes(replay)),
                    "Reconnaissance and route travel replay changed the canonical state or RNG stream.");
            });

            cases.Add("failed_route_reconnaissance_keeps_work_but_retry_rebooks_all_eight_hours", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var policy = RouteReconnaissancePolicy(routes, SeedForD20(1), tier: 6);
                var simulation = World(policy);
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteReconnaissanceCommand(simulation,
                    CommandKind.StartRouteReconnaissance, RouteTravelId, "route.recon.fail.start"));
                WorldAdvance(simulation, 28800);
                var failed = simulation.Capture();
                Require(failed.RouteReconnaissanceAttempts.Single().Status == ExpeditionRouteReconnaissanceStatus.Resolved
                    && failed.RouteReconnaissanceAttempts.Single().WorkDone == new RuleTime(28800)
                    && failed.RouteReconnaissanceAttempts.Single().Check.Degree == ExpeditionRouteReconnaissanceDegree.CriticalFailure
                    && failed.RouteSegments.Single().Status == ExpeditionRouteSegmentStatus.ReconnaissanceRequired
                    && failed.RouteSegments.Single().FeasibilityAttemptId == "",
                    "A failed check granted route feasibility or lost its spent work.");
                RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "route.recon.failed.no-travel"), "RouteRequiresReconnaissance");
                var retry = RouteReconnaissanceCommand(simulation, CommandKind.StartRouteReconnaissance,
                    RouteTravelId, "route.recon.fail.retry");
                var retryQuery = simulation.QueryCommand(host, retry);
                Require(retryQuery.Admissible && retryQuery.Costs.Single().Amount == 28800,
                    "Failure did not require a fresh full reconnaissance work interval.");
                WorldCommit(simulation, retry);
                WorldAdvance(simulation, 28799);
                var last = simulation.Capture().RouteReconnaissanceAttempts.OrderBy(x => x.StartedRevision).Last();
                Require(last.Status == ExpeditionRouteReconnaissanceStatus.Working
                    && last.WorkDone == new RuleTime(28799) && last.Check == null
                    && simulation.Capture().RouteSegments.Single().FeasibilityAttemptId == "",
                    "Retry inherited the prior attempt's work or feasibility.");
            });

            cases.Add("route_reconnaissance_requires_and_pauses_on_inspection_access_loss", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var blindEvent = CCApply("recon-blind", "Blinded", at: new ConditionStamp(new RuleTime(249, 2)));
                var policy = RouteReconnaissancePolicy(routes, SeedForD20(20), 1,
                    new ConditionCombatFixture(blindEvent),
                    new TestOnlyRouteReconnaissanceSkillFact(TestOnlyPolicy.ActorId, 1));
                var simulation = World(policy);
                RouteTravelReachSource(simulation);
                var start = RouteReconnaissanceCommand(simulation, CommandKind.StartRouteReconnaissance,
                    RouteTravelId, "route.recon.sight.start");
                WorldCommit(simulation, start);
                WorldAdvance(simulation, 120);
                var beforeBlind = simulation.Capture();
                var dispatch = new Command("route.recon.sight.dispatch", TestOnlyPolicy.ActorId,
                    beforeBlind.Revision, CommandKind.DispatchConditionEvent, "event.recon-blind");
                WorldCommit(simulation, dispatch);
                var blinded = simulation.Capture();
                var attempt = blinded.RouteReconnaissanceAttempts.Single();
                Require(attempt.Status == ExpeditionRouteReconnaissanceStatus.Paused
                    && attempt.WorkDone == new RuleTime(120)
                    && attempt.InspectionProfileId == "inspection.route-cache-to-plot"
                    && attempt.InspectionProfileFingerprint == RouteReconnaissanceProfile(routes).Tasks.Single().Inspection.Fingerprint,
                    "Losing visual access did not pause the bound inspection attempt at its credited-work boundary.");
                WorldAdvance(simulation, 600);
                Require(simulation.Capture().RouteReconnaissanceAttempts.Single().WorkDone == new RuleTime(120),
                    "The reconnaissance task earned work while its required inspection capability was unavailable.");
                RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "route.recon.sight.no-feasibility"), "RouteRequiresReconnaissance");

                var blockedRoutes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var blockedPolicy = new TestOnlySharedWorldPolicy(new PortableKitFixture(),
                    new SharedCombatFixture(seed: SeedForD20(20)), new SupplyCacheFixture())
                    .EnableRouteObservationIntegration(blockedRoutes, RouteTravelMotionFixture(blockedRoutes),
                        RouteReconnaissanceBlockedSightFixture())
                    .EnableRouteReconnaissance(RouteReconnaissanceProfile(blockedRoutes));
                var blockedSight = World(blockedPolicy);
                RouteTravelReachSource(blockedSight);
                RejectUnchanged(blockedSight, host, RouteReconnaissanceCommand(blockedSight,
                    CommandKind.StartRouteReconnaissance, RouteTravelId, "route.recon.sight.blocked"),
                    "RouteReconnaissanceInspectionAccessUnavailable");
            });
        }
    }
}
#endif
