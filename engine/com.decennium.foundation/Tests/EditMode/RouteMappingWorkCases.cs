#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlyExpeditionRouteMappingWorkFixture RouteMappingWorkProfile(
            TestOnlyExpeditionRouteFixture routes, int tier = 1,
            params TestOnlyRouteMappingSkillFact[] skills)
            => new TestOnlyExpeditionRouteMappingWorkFixture(routes,
                new[] { new TestOnlyRouteMappingTaskProfile(RouteTravelId, tier) }, skills);

        private static Command RouteMappingWorkCommand(Simulation simulation, CommandKind kind,
            string target, string id, string actor = TestOnlyPolicy.ActorId,
            IEnumerable<string> assistants = null)
        {
            var request = kind == CommandKind.StartRouteMappingWork
                ? new RouteMappingWorkRequest(assistants ?? Array.Empty<string>()) : null;
            return new Command(id, actor, simulation.Capture().Revision, kind, target,
                routeMappingWork: request);
        }

        private static uint SeedForD20(int natural)
        {
            for (uint seed = 1; seed < 10000; seed++)
                if (RuleDice.RollD20(seed).Natural == natural) return seed;
            throw new Exception("No seed found for requested d20 natural.");
        }

        private static uint SeedForDisadvantage(int first, int second)
        {
            for (uint seed = 1; seed < 100000; seed++)
            {
                var roll = RuleDice.RollD20(seed, disadvantageSources: 1);
                if (roll.First == first && roll.Second == second) return seed;
            }
            throw new Exception("No seed found for requested disadvantage dice.");
        }

        private static RuleTime RouteMappingConditionStartAt => new RuleTime(9, 2);
        private static RuleTime RouteMappingConditionCompletionAt => new RuleTime(57609, 2);

        private static Simulation RouteMappingConditionWorld(TestOnlyExpeditionRouteFixture routes,
            uint seed, ConditionFixtureEvent condition)
        {
            var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(),
                new SharedCombatFixture(seed: seed), new SupplyCacheFixture(),
                conditions: new ConditionCombatFixture(condition))
                .EnableExpeditionRouteTravel(routes)
                .EnableRouteMappingWork(RouteMappingWorkProfile(routes));
            var simulation = World(policy);
            RouteTravelReachSource(simulation);
            Require(simulation.Capture().RuleClock == RouteMappingConditionStartAt,
                "Condition fixture start marker no longer matches the authored route-approach duration.");
            return simulation;
        }

        private static void AddRouteMappingWorkCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();

            cases.Add("route_mapping_work_check_rejects_negative_condition_prefix", () => {
                Throws<ArgumentException>(() => new ExpeditionRouteMappingWorkCheckRecord(
                    "route.map.negative-prefix", 1, default(RuleTime), 0, 0, 0, 0, 12, -1,
                    false, 10, 0, 10, 10, ExpeditionRouteMappingResultDegree.Success,
                    1, 2, 1, ExpeditionRouteMapping.Unknown, ExpeditionRouteMapping.Unknown, 0, 0, 0));
            });

            cases.Add("route_mapping_work_uses_reserved_team_time_rng_and_persists", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                uint seed = SeedForD20(20);
                var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(),
                    new SharedCombatFixture(seed: seed), new SupplyCacheFixture())
                    .EnableExpeditionRouteTravel(routes)
                    .EnableRouteMappingWork(RouteMappingWorkProfile(routes, 1,
                        new TestOnlyRouteMappingSkillFact(TestOnlyPolicy.CompanionId, 1)));
                var simulation = World(policy);
                Snapshot replayStart = simulation.Capture();
                RouteTravelReachSource(simulation);

                // The companion works from the adjacent 5-foot map cell. The lead is untrained;
                // this proves lead training is not silently made a start requirement.
                WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, -1, 0, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, 0, 1, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, -1, 0, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, -1, 0, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                var positioned = simulation.Capture();
                Require(positioned.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && positioned.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2
                    && positioned.Actors.Single(x => x.Id == TestOnlyPolicy.CompanionId).X == 0
                    && positioned.Actors.Single(x => x.Id == TestOnlyPolicy.CompanionId).Y == 2,
                    "Test team was not placed at the authored route mouth.");

                var discovered = simulation.DiscoverCommands(host, TestOnlyPolicy.ActorId)
                    .Where(x => x.Command.Kind == CommandKind.StartRouteMappingWork
                        && x.Command.Target == RouteTravelId).ToArray();
                var assistantOptions = discovered.Where(x => x.Command.RouteMappingWork.AssistantIds
                    .SequenceEqual(new[] { TestOnlyPolicy.CompanionId }, StringComparer.Ordinal)).ToArray();
                Require(assistantOptions.Length == 1, "Command discovery omitted the trained adjacent assistant: "
                    + string.Join(";", discovered.Select(x => x.Command.Target + "/"
                        + string.Join(",", x.Command.RouteMappingWork.AssistantIds))));
                var selected = assistantOptions.Single().Command;
                var beforeQuery = Bytes(simulation);
                var query = simulation.QueryCommand(host, selected);
                Require(query.Supported && query.Admissible && query.Costs.Count == 1
                    && query.Costs[0].Kind == "active-work-seconds"
                    && query.Costs[0].ResourceId == RouteTravelId
                    && query.Costs[0].Amount == TestOnlyExpeditionRouteMappingWorkFixture.RequiredWorkSeconds
                    && beforeQuery.SequenceEqual(Bytes(simulation)),
                    "Start query was not pure or omitted the full 480-minute team-work cost.");
                RejectUnchanged(simulation, host, RouteMappingWorkCommand(simulation,
                    CommandKind.StartRouteMappingWork, RouteTravelId, "route.map.self-assist",
                    TestOnlyPolicy.ActorId, new[] { TestOnlyPolicy.ActorId }), "RouteMappingLeadCannotAssist");
                Throws<ArgumentException>(() => new RouteMappingWorkRequest(new[] {
                    "assistant.one", "assistant.two", "assistant.three", "assistant.four" }));
                WorldCommit(simulation, selected);
                var started = simulation.Capture();
                var attempt = started.RouteMappingWorkAttempts.Single();
                Require(started.SchemaVersion == Snapshot.RouteMappingWorkSchema
                    && attempt.Status == ExpeditionRouteMappingWorkStatus.Working
                    && attempt.WorkDone == default && attempt.WorkRequired == new RuleTime(28800)
                    && started.Work.WorkerIntervals.Count(x => x.JobId == attempt.Id) == 2
                    && WorldActivityProjection.CurrentWork(started).Count == 2,
                    "Map Route did not reserve both real participants or project their shared work.");

                WorldAdvance(simulation, 120);
                WorldCommit(simulation, RouteMappingWorkCommand(simulation, CommandKind.PauseRouteMappingWork,
                    attempt.Id, "route.map.pause"));
                var paused = simulation.Capture().RouteMappingWorkAttempts.Single();
                Require(paused.Status == ExpeditionRouteMappingWorkStatus.Paused && paused.WorkDone == new RuleTime(120)
                    && paused.Check == null && !simulation.Capture().Work.WorkerIntervals.Any(x => x.JobId == attempt.Id
                        && x.Start <= simulation.Capture().RuleClock && x.End > simulation.Capture().RuleClock),
                    "Pause did not retain the 120 active seconds and release future participant intervals.");
                RejectUnchanged(simulation, host, RouteMappingWorkCommand(simulation, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "route.map.second-open"), "RouteMappingTaskAlreadyOpen");
                WorldAdvance(simulation, 100);
                Require(simulation.Capture().RouteMappingWorkAttempts.Single().WorkDone == new RuleTime(120),
                    "Paused route work accrued passive time.");

                byte[] checkpoint = Bytes(simulation);
                simulation = new Simulation(policy, new SnapshotCodec().Decode(checkpoint), ExecutionProfile.Laboratory);
                Require(checkpoint.SequenceEqual(Bytes(simulation)), "Paused schema59 route work changed through save/restore.");
                var resume = RouteMappingWorkCommand(simulation, CommandKind.ResumeRouteMappingWork,
                    attempt.Id, "route.map.resume");
                var resumeQuery = simulation.QueryCommand(host, resume);
                Require(resumeQuery.Admissible && resumeQuery.Costs.Count == 1
                    && resumeQuery.Costs[0].Amount == 28680,
                    "Resume failed to expose only retained-work remainder.");
                WorldCommit(simulation, resume);
                WorldAdvance(simulation, 28680);
                var completed = simulation.Capture();
                var resolved = completed.RouteMappingWorkAttempts.Single();
                var check = resolved.Check;
                var knowledge = ExpeditionRouteMappingRules.Current(completed, RouteTravelId,
                    ExpeditionRouteMapping.Unknown);
                Require(resolved.Status == ExpeditionRouteMappingWorkStatus.Resolved
                    && resolved.WorkDone == new RuleTime(28800) && check != null
                    && check.AppliedRevision == completed.Revision && check.Natural == 20
                    && check.ProficiencyRank == 0 && check.ProficiencyBonus == 0 && check.AssistantBonus == 1
                    && !check.Disadvantage && check.FirstRoll == 20 && check.SecondRoll == 0
                    && check.Dc == 12 && check.Degree == ExpeditionRouteMappingResultDegree.CriticalSuccess
                    && check.RandomBefore != check.RandomAfter && check.WordsConsumed > 0
                    && knowledge.Mapping == ExpeditionRouteMapping.Sketched && knowledge.UnspentMarks == 1,
                    "Completed work check mismatch: status=" + resolved.Status + " work=" + resolved.WorkDone
                    + " check=" + (check == null ? "null" : "natural=" + check.Natural + ",modifier=" + check.LeadModifier
                        + ",rank=" + check.ProficiencyRank + ",pb=" + check.ProficiencyBonus + ",assistant=" + check.AssistantBonus
                        + ",dc=" + check.Dc + ",total=" + check.Total + ",degree=" + check.Degree
                        + ",mapping=" + check.MappingBefore + "->" + check.MappingAfter + ",marks=" + check.MarksGranted + "/" + check.MarksAfter)
                    + " current=" + knowledge.Mapping + "/" + knowledge.UnspentMarks);
                RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "route.map.unknown-travel"), "RouteRequiresReconnaissance");
                var finalBytes = Bytes(simulation);
                Require(finalBytes.SequenceEqual(Bytes(new Simulation(policy, new SnapshotCodec().Decode(finalBytes),
                        ExecutionProfile.Laboratory))), "Resolved schema59 check changed through save/restore.");

                var replay = new Simulation(policy, replayStart, ExecutionProfile.Laboratory);
                foreach (var receipt in completed.Receipts.OrderBy(x => x.Revision))
                {
                    var replayed = replay.Execute(host, CommandHistory.Read(receipt));
                    Require(replayed.Outcome == Outcome.Committed,
                        "Saved route mapping history did not replay at revision " + receipt.Revision + ".");
                }
                Require(finalBytes.SequenceEqual(Bytes(replay)),
                    "Route mapping work/check replay changed the canonical snapshot or RNG stream.");
            });

            cases.Add("route_mapping_work_applies_poisoned_disadvantage_and_persists_both_dice", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                uint seed = SeedForDisadvantage(18, 3);
                var simulation = RouteMappingConditionWorld(routes, seed, CCApply("route-map-poison", "Poisoned",
                    TestOnlyPolicy.ActorId, expires: new ConditionStamp(RouteMappingConditionCompletionAt.AddSeconds(1)),
                    at: new ConditionStamp(RouteMappingConditionStartAt)));
                Snapshot replayStart = simulation.Capture();
                WorldCommit(simulation, CCCommand(simulation, "route-map-poison"));
                WorldCommit(simulation, RouteMappingWorkCommand(simulation, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "route.map.poison.start"));
                WorldAdvance(simulation, 28800);
                var completed = simulation.Capture();
                var attempt = completed.RouteMappingWorkAttempts.Single();
                var check = attempt.Check;
                Require(attempt.Status == ExpeditionRouteMappingWorkStatus.Resolved && check != null
                    && check.Disadvantage && check.FirstRoll == 18 && check.SecondRoll == 3
                    && check.Natural == 3 && check.WordsConsumed == 2
                    && check.RandomBefore != check.RandomAfter
                    && ExpeditionRouteMappingRules.Current(completed, RouteTravelId,
                        ExpeditionRouteMapping.Unknown).Mapping == ExpeditionRouteMapping.Unknown,
                    "Poisoned did not select and preserve the disadvantage roll trace.");
                var codec = new SnapshotCodec();
                byte[] bytes = codec.Encode(completed);
                Require(bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),
                    "Poisoned Map Route check dice changed through save/restore.");
                var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(),
                    new SharedCombatFixture(seed: seed), new SupplyCacheFixture(),
                    conditions: new ConditionCombatFixture(CCApply("route-map-poison", "Poisoned",
                        TestOnlyPolicy.ActorId, expires: new ConditionStamp(RouteMappingConditionCompletionAt.AddSeconds(1)),
                        at: new ConditionStamp(RouteMappingConditionStartAt))))
                    .EnableExpeditionRouteTravel(routes)
                    .EnableRouteMappingWork(RouteMappingWorkProfile(routes));
                var replay = new Simulation(policy, replayStart, ExecutionProfile.Laboratory);
                foreach (var receipt in completed.Receipts.Where(x => x.Revision > replayStart.Revision)
                    .OrderBy(x => x.Revision))
                {
                    var replayed = replay.Execute(TestOnlySharedWorldPolicy.Host(), CommandHistory.Read(receipt));
                    Require(replayed.Outcome == Outcome.Committed,
                        "Poisoned route mapping replay failed at revision " + receipt.Revision
                        + " with outcome " + replayed.Outcome + " and code " + replayed.Code + ".");
                }
                Require(bytes.SequenceEqual(codec.Encode(replay.Capture())),
                    "Poisoned route mapping replay changed the check result or RNG state.");
            });

            cases.Add("route_mapping_work_uses_post_boundary_condition_state_at_completion", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                uint seed = SeedForDisadvantage(18, 3);
                var condition = CCApply("route-map-poison-expires", "Poisoned", TestOnlyPolicy.ActorId,
                    expires: new ConditionStamp(RouteMappingConditionCompletionAt),
                    at: new ConditionStamp(RouteMappingConditionStartAt));
                var simulation = RouteMappingConditionWorld(routes, seed, condition);
                WorldCommit(simulation, CCCommand(simulation, "route-map-poison-expires"));
                WorldCommit(simulation, RouteMappingWorkCommand(simulation, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "route.map.poison-expiring.start"));
                WorldAdvance(simulation, 28800);
                var state = simulation.Capture();
                var check = state.RouteMappingWorkAttempts.Single().Check;
                Require(check != null && !check.Disadvantage && check.FirstRoll == 18 && check.SecondRoll == 0
                    && check.Natural == 18 && check.WordsConsumed == 1
                    && !TestOnlyClubAttackPolicy.ConditionsFor(state, TestOnlyPolicy.ActorId).View().Has(ConditionKind.Poisoned),
                    "A condition expiring at the task boundary still altered its completed check.");
            });

            cases.Add("route_mapping_work_check_uses_condition_history_at_its_causal_point", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var condition = CCApply("route-map-poison-after-check", "Poisoned", TestOnlyPolicy.ActorId,
                    expires: new ConditionStamp(RouteMappingConditionCompletionAt.AddSeconds(1)),
                    at: new ConditionStamp(RouteMappingConditionCompletionAt));
                uint seed = SeedForD20(20);
                var simulation = RouteMappingConditionWorld(routes, seed, condition);
                Snapshot replayStart = simulation.Capture();
                var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(),
                    new SharedCombatFixture(seed: seed), new SupplyCacheFixture(),
                    conditions: new ConditionCombatFixture(condition))
                    .EnableExpeditionRouteTravel(routes)
                    .EnableRouteMappingWork(RouteMappingWorkProfile(routes));
                WorldCommit(simulation, RouteMappingWorkCommand(simulation, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "route.map.causal-check.start"));
                WorldAdvance(simulation, 28800);
                var check = simulation.Capture().RouteMappingWorkAttempts.Single().Check;
                Require(check != null && !check.Disadvantage && check.Natural == 20,
                    "The check did not resolve normally before the later same-time Poisoned event.");
                var poisonAfterCheck = simulation.Execute(TestOnlySharedWorldPolicy.Host(),
                    CCCommand(simulation, "route-map-poison-after-check"));
                Require(poisonAfterCheck.Outcome == Outcome.Committed,
                    "A later same-clock condition event was rejected with " + poisonAfterCheck.Code + ".");
                var conditioned = simulation.Capture();
                var retained = conditioned.RouteMappingWorkAttempts.Single().Check;
                Require(retained != null && retained.AppliedRevision < conditioned.Revision
                    && !retained.Disadvantage && retained.Natural == 20
                    && retained.ConditionOperationCount < conditioned.Conditions.Single(x => x.Target == TestOnlyPolicy.ActorId).Operations.Count
                    && TestOnlyClubAttackPolicy.ConditionsFor(conditioned, TestOnlyPolicy.ActorId)
                        .View().Has(ConditionKind.Poisoned),
                    "A later same-clock condition rewrote the earlier Map Route check.");
                byte[] bytes = Bytes(simulation);
                var codec = new SnapshotCodec();
                Require(bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),
                    "Causal condition evidence changed through save/restore.");
                var replay = new Simulation(policy, replayStart, ExecutionProfile.Laboratory);
                foreach (var receipt in conditioned.Receipts.Where(x => x.Revision > replayStart.Revision)
                    .OrderBy(x => x.Revision))
                    Require(replay.Execute(TestOnlySharedWorldPolicy.Host(), CommandHistory.Read(receipt)).Outcome == Outcome.Committed,
                        "Causal condition replay failed at revision " + receipt.Revision + ".");
                Require(bytes.SequenceEqual(Bytes(replay)),
                    "Causal condition check/replay changed the final snapshot.");
            });

            cases.Add("route_mapping_work_synchronous_handling_cannot_cross_fractional_completion", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var policy = RouteTravelPolicy(routes).EnableRouteMappingWork(RouteMappingWorkProfile(routes));
                var simulation = World(policy);
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteMappingWorkCommand(simulation, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "route.map.handling-boundary.start"));
                WorldAdvance(simulation, 57599, 2);
                Require(simulation.Capture().RuleClock == new RuleTime(28804),
                    "Fixture did not reach exactly one-half second before Map Route completion.");
                RejectUnchanged(simulation, TestOnlySharedWorldPolicy.Host(),
                    IC(simulation, CommandKind.HandleInventory, TestOnlyInventoryPolicy.FoodId,
                        new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Stow),
                        TestOnlyPolicy.CompanionId), "TimedHandlingBoundaryUnsupported");
                WorldAdvance(simulation, 1, 2);
                var completed = simulation.Capture().RouteMappingWorkAttempts.Single();
                Require(simulation.Capture().RuleClock == new RuleTime(57609, 2)
                    && completed.Status == ExpeditionRouteMappingWorkStatus.Resolved
                    && completed.WorkDone == completed.WorkRequired
                    && completed.Check != null && completed.Check.At == simulation.Capture().RuleClock,
                    "The shared clock did not resolve Map Route exactly at its fractional boundary.");
            });

            cases.Add("route_mapping_work_does_not_stop_an_unrelated_route_traveler", () => {
                var routes = RouteTravelFixture();
                var policy = RouteTravelPolicy(routes)
                    .EnableRouteMappingWork(RouteMappingWorkProfile(routes));
                var simulation = World(policy);
                RouteTravelReachSource(simulation);
                WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, -1, 0, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, 0, 1, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, -1, 0, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, -1, 0, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId); WorldAdvance(simulation, 3, 2);
                var traveller = RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "route.map.traveller-start");
                var travelQuery = simulation.QueryCommand(host, traveller);
                Require(travelQuery.Admissible, "Baseline unrelated route traveler could not start: " + travelQuery.Code);
                WorldCommit(simulation, traveller);

                var start = RouteMappingWorkCommand(simulation, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "route.map.parallel-start", TestOnlyPolicy.CompanionId);
                var workQuery = simulation.QueryCommand(host, start);
                Require(workQuery.Admissible, "Stationary route task was blocked by another actor's route travel: " + workQuery.Code);
                WorldCommit(simulation, start);
                WorldAdvance(simulation, 300);
                var concurrent = simulation.Capture();
                Require(concurrent.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Moving
                    && concurrent.RouteTravels.Single().Progress > default(RuleQuantity)
                    && concurrent.RouteMappingWorkAttempts.Single().WorkDone == new RuleTime(300),
                    "The unrelated route traveler stopped or route work failed to accrue beside it.");
                WorldAdvance(simulation, 28500);
                var remainingTravel = simulation.Capture().RouteTravels.Single();
                RuleTime effortRemaining = RuleTime.FromFraction(
                    (BigInteger)ExpeditionRouteTravelRules.NominalSegmentSeconds * remainingTravel.NominalEffort.Denominator
                        - remainingTravel.NominalEffort.Numerator,
                    remainingTravel.NominalEffort.Denominator);
                RuleTime actualTravelRemaining = ExpeditionRouteTravelRules.ActualMovingTime(effortRemaining,
                    TestOnlyClubAttackPolicy.WalkingSpeed(simulation.Capture(), TestOnlyPolicy.ActorId),
                    routes.Routes.Single().Quality);
                Require(actualTravelRemaining.Denominator == 1 && actualTravelRemaining.Numerator > 0,
                    "The authored route fixture did not produce a whole-second remaining travel interval.");
                WorldAdvance(simulation, checked((int)actualTravelRemaining.Numerator));
                var completed = simulation.Capture();
                var finalTravel = completed.RouteTravels.Single();
                var finalWork = completed.RouteMappingWorkAttempts.Single();
                Require(finalTravel.Status == ExpeditionRouteTravelStatus.SegmentComplete
                    && finalWork.Status == ExpeditionRouteMappingWorkStatus.Resolved,
                    "Parallel result mismatch: travel=" + finalTravel.Status + " progress=" + finalTravel.Progress
                    + "/" + finalTravel.SegmentStartProgress + "+" + finalTravel.SegmentProgressAward
                    + " work=" + finalWork.Status + " done=" + finalWork.WorkDone + " clock=" + completed.RuleClock);
            });

            cases.Add("failed_route_mapping_retry_requires_a_fresh_480_minutes", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(),
                    new SharedCombatFixture(seed: SeedForD20(1)), new SupplyCacheFixture())
                    .EnableExpeditionRouteTravel(routes)
                    .EnableRouteMappingWork(RouteMappingWorkProfile(routes, tier: 6));
                var simulation = World(policy);
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteMappingWorkCommand(simulation, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "route.map.fail.first"));
                WorldAdvance(simulation, 28800);
                var first = simulation.Capture().RouteMappingWorkAttempts.Single();
                Require(first.Status == ExpeditionRouteMappingWorkStatus.Resolved && first.Check.Natural == 1
                    && (first.Check.Degree == ExpeditionRouteMappingResultDegree.Failure
                        || first.Check.Degree == ExpeditionRouteMappingResultDegree.CriticalFailure)
                    && first.WorkDone == new RuleTime(28800)
                    && ExpeditionRouteMappingRules.Current(simulation.Capture(), RouteTravelId,
                        ExpeditionRouteMapping.Unknown).Mapping == ExpeditionRouteMapping.Unknown,
                    "Failed attempt reused or applied route mapping progress.");
                var retry = RouteMappingWorkCommand(simulation, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "route.map.fail.retry");
                var query = simulation.QueryCommand(host, retry);
                Require(query.Admissible && query.Costs.Single().Amount == 28800,
                    "Failed attempt did not require a new complete 480-minute labor booking.");
                WorldCommit(simulation, retry);
                Require(simulation.Capture().RouteMappingWorkAttempts.Length == 2
                    && simulation.Capture().RouteMappingWorkAttempts[1].WorkDone == default,
                    "Retry inherited labor or check evidence from the immutable failure.");
                WorldAdvance(simulation, 28799);
                var beforeRetryBoundary = simulation.Capture().RouteMappingWorkAttempts.OrderBy(x => x.StartedRevision).Last();
                Require(beforeRetryBoundary.Status == ExpeditionRouteMappingWorkStatus.Working
                    && beforeRetryBoundary.Check == null && beforeRetryBoundary.WorkDone == new RuleTime(28799),
                    "Retry resolved before its complete active-work duration.");
                WorldAdvance(simulation, 1);
                var result = simulation.Capture();
                Require(result.RouteMappingWorkAttempts.All(x => x.Status == ExpeditionRouteMappingWorkStatus.Resolved)
                    && result.RouteMappingWorkAttempts.All(x => x.WorkDone == new RuleTime(28800))
                    && result.RouteMappingWorkAttempts.Select(x => x.StartedRevision).Distinct().Count() == 2
                    && result.RouteMappingWorkAttempts.Select(x => x.Check.AppliedRevision).Distinct().Count() == 2,
                    "Retry history reused a prior task, receipt, labor interval, or roll.");
            });
        }
    }
}
#endif
