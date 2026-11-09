#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy CampConstructionPolicy(uint seed, bool concealed = false,
            HuntingTrapFixture traps = null)
        {
            var routes = RouteTravelCheckpointFixture();
            var site = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                new RuleQuantity(1), exposed: !concealed, concealed: concealed);
            var skillFacts = new TestOnlyExpeditionRouteMappingWorkFixture(routes,
                new[] { new TestOnlyRouteMappingTaskProfile(RouteTravelId, 1) },
                new[] { new TestOnlyRouteMappingSkillFact(TestOnlyPolicy.ActorId, 1),
                    new TestOnlyRouteMappingSkillFact(TestOnlyPolicy.CompanionId, 1) });
            var policy = PressurePolicy(initialPressure: 0, seed: seed, routes: routes)
                .EnableRouteMappingWork(skillFacts)
                .EnableExpeditionCampUse(site)
                .EnableExpeditionCampConstruction(new TestOnlyExpeditionCampConstructionFixture(1,
                    TestOnlyPolicy.ActorId, new[] { TestOnlyPolicy.CompanionId }, CharacterAbility.Strength));
            if (traps != null) policy.EnableHuntingTraps(traps);
            return policy;
        }

        private static Simulation CampConstructionAtCheckpoint(uint seed, bool concealed = false)
        {
            var policy = CampConstructionPolicy(seed, concealed);
            var initial = policy.Initial();
            Require(CharacterSkillTrainingFacts.IsTrained(initial, TestOnlyPolicy.ActorId,
                    TestOnlyExpeditionCampConstructionFixture.SkillId)
                && CharacterSkillTrainingFacts.IsTrained(initial, TestOnlyPolicy.CompanionId,
                    TestOnlyExpeditionCampConstructionFixture.SkillId)
                && initial.SkillTraining.Count(x => x.SkillId == TestOnlyExpeditionCampConstructionFixture.SkillId) == 2,
                "The shared character snapshot did not expose the two explicitly fingerprinted Survival training facts.");
            var simulation = new Simulation(policy, initial, ExecutionProfile.Laboratory);
            WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId);
            WorldAdvance(simulation, 1);
            PortableCommit(simulation, Portable(simulation, CommandKind.RemovePortableItem, PortableKitFixture.Pack));
            PortableCommit(simulation, Portable(simulation, CommandKind.HandlePortableEquipment,
                PortableKitFixture.Pack, handling: HandlingKind.Drop));
            RouteTravelReachSource(simulation);
            WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                "camp-build.route.start"));
            WorldAdvance(simulation, 10800);
            PressurePauseActiveRouteIfMoving(simulation, "camp-build.route.pause");
            // Put the trained remote assistant on the adjacent tile. The route lead remains at its
            // exact paused checkpoint and the pair is physically co-located for the fixed fixture.
            WorldStep(simulation, 0, 1, actor: TestOnlyPolicy.CompanionId);
            WorldAdvance(simulation, 1);
            WorldStep(simulation, -1, 0, actor: TestOnlyPolicy.CompanionId);
            WorldAdvance(simulation, 1);
            var state = simulation.Capture();
            Require(state.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                && state.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                && state.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                && state.Actors.Single(x => x.Id == TestOnlyPolicy.CompanionId).X == 2
                && state.Actors.Single(x => x.Id == TestOnlyPolicy.CompanionId).Y == 3,
                "Construction preparation failed to preserve the paused exploration checkpoint and adjacent assistant.");
            return simulation;
        }

        private static Command CampConstructionCommand(Simulation simulation, CommandKind kind, string target,
            string suffix)
            => new Command("camp-build." + suffix + "." + simulation.Capture().Revision.ToString(
                    System.Globalization.CultureInfo.InvariantCulture), TestOnlyPolicy.ActorId,
                simulation.Capture().Revision, kind, target);

        private static void CampConstructionCommit(Simulation simulation, CommandKind kind, string target,
            string suffix)
            => WorldCommit(simulation, CampConstructionCommand(simulation, kind, target, suffix));

        private static uint CampConstructionSeed(bool success)
        {
            for (uint seed = 1; seed < 10000; seed++)
            {
                var policy = CampConstructionPolicy(seed);
                var initial = policy.Initial();
                var modifier = AbilityCheckRules.Derive(initial, TestOnlyPolicy.ActorId,
                    TestOnlyExpeditionCampConstructionFixture.SkillId, CharacterAbility.Strength).Total + 1;
                int natural = RuleDice.RollD20(initial.RandomState).Natural;
                bool predicted = RuleResolution.TaskCheck(natural, modifier,
                    TemporaryCampConstructionValidation.TierDc(1)).Success;
                if (predicted == success) return seed;
            }
            throw new Exception("Could not find a deterministic TEST_ONLY camp check seed.");
        }

        private static void AddTemporaryCampConstructionCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            var codec = new SnapshotCodec();
            cases.Add("temporary_camp_support_mark_projection_uses_saved_result_degree", () => {
                var snapshot = CampConstructionPolicy(CampConstructionSeed(success: true)).Initial();
                TemporaryCampConstructionCheckRecord Check(string id, TemporaryCampConstructionResult result)
                    => new TemporaryCampConstructionCheckRecord(id + ".check", 1, default(RuleTime),
                        0, 0, 0, 0, 0, 0, TemporaryCampConstructionValidation.TierDc(1),
                        0, false, Array.Empty<int>(), 10, 0, 10, 10, result, 1, 2, 1);
                TemporaryCampConstructionAttemptRecord Attempt(string id, TemporaryCampConstructionResult result)
                    => new TemporaryCampConstructionAttemptRecord(id, PressureCampId, RouteTravelId, 1,
                        "TEST_ONLY.mark-projection", TestOnlyPolicy.ActorId,
                        TestOnlyExpeditionCampConstructionFixture.SkillId, CharacterAbility.Strength,
                        id + ".tent", id + ".pack", Array.Empty<string>(), 1, default(RuleTime),
                        default(RuleTime), new RuleTime(28800), new RuleTime(28800),
                        TemporaryCampConstructionStatus.Resolved, Check(id, result));
                snapshot.TemporaryCampConstructionAttempts = new[] {
                    Attempt("mark.success", TemporaryCampConstructionResult.Success),
                    Attempt("mark.critical", TemporaryCampConstructionResult.CriticalSuccess),
                    Attempt("mark.failure", TemporaryCampConstructionResult.Failure)
                };
                Require(TemporaryCampConstructionValidation.SupportMarks(snapshot, PressureCampId) == 3
                    && TemporaryCampConstructionValidation.SupportMarks(snapshot, "other-site") == 0,
                    "Saved Success/Critical Success/Failure degrees did not project to one/two/zero Support marks by site.");
            });
            cases.Add("temporary_camp_construction_composes_with_hunting_traps", () => {
                var traps = new HuntingTrapFixture(new HuntingTrapDefinition("TEST_ONLY.camp-composition-trap",
                    TestOnlyPolicy.ActorId, 1, 0, new[] { TestOnlyPolicy.ActorId }));
                var policy = CampConstructionPolicy(CampConstructionSeed(success: true), traps: traps);
                var initial = policy.Initial();
                var simulation = new Simulation(policy, initial, ExecutionProfile.Laboratory);
                Require(simulation.Capture().SchemaVersion == Snapshot.TemporaryCampConstructionSchema
                    && simulation.Capture().PortableEquipment.Any(x => x.Id == "TEST_ONLY.camp-composition-trap")
                    && simulation.Capture().ExpeditionCampSites.Any(x => x.Id == PressureCampId),
                    "Schema70 camp construction rejected or lost the existing hunting-trap composition.");
            });
            cases.Add("temporary_camp_construction_schema70_save_resume_replay_and_pressure", () => {
                uint seed = CampConstructionSeed(success: true);
                var simulation = CampConstructionAtCheckpoint(seed);
                var state = simulation.Capture();
                var start = CampConstructionCommand(simulation, CommandKind.StartTemporaryCampConstruction,
                    PressureCampId, "start");
                byte[] beforeQuery = Bytes(simulation);
                var query = simulation.QueryCommand(host, start);
                Require(query.Supported && query.Admissible && query.Costs.Count == 1
                    && query.Costs[0].Kind == "active-work-seconds"
                    && query.Costs[0].Amount == TestOnlyExpeditionCampConstructionFixture.RequiredWorkSeconds
                    && Bytes(simulation).SequenceEqual(beforeQuery),
                    "Construction discovery/query did not report the fixed labor requirement without mutating state.");
                CampConstructionCommit(simulation, CommandKind.StartTemporaryCampConstruction, PressureCampId, "start");
                state = simulation.Capture();
                var attempt = state.TemporaryCampConstructionAttempts.Single();
                Require(state.SchemaVersion == Snapshot.TemporaryCampConstructionSchema
                    && attempt.Status == TemporaryCampConstructionStatus.Working
                    && attempt.WorkDone == default(RuleTime)
                    && state.Work.Reservations.Count(x => x.JobId == attempt.Id && x.RemainingAmount == new RuleQuantity(20)) == 2
                    && state.Work.AvailableAmount(attempt.TentLotId) == default(RuleQuantity)
                    && state.Work.AvailableAmount(attempt.PackLotId) == default(RuleQuantity)
                    && state.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.ExposedCampUse) == 0,
                    "Start did not atomically reserve the two physical lots without granting progress or a camp-use Pressure cause.");
                Throws<ArgumentException>(() => state.Work.Reserve("camp-build.competitor", Array.Empty<WorkerInterval>(),
                    new[] { new ResourceReservation("camp-build.competitor.claim", "camp-build.competitor",
                        attempt.TentLotId, new RuleQuantity(1)) }));

                WorldAdvance(simulation, 14400);
                Require(simulation.Capture().TemporaryCampConstructionAttempts.Single().WorkDone == new RuleTime(14400),
                    "The first four active hours were not credited from the shared simulation clock.");
                CampConstructionCommit(simulation, CommandKind.PauseTemporaryCampConstruction, attempt.Id, "pause");
                var paused = simulation.Capture();
                Require(paused.TemporaryCampConstructionAttempts.Single().Status == TemporaryCampConstructionStatus.Paused
                    && paused.TemporaryCampConstructionAttempts.Single().WorkDone == new RuleTime(14400),
                    "Pause did not preserve exactly the completed active work.");
                byte[] pausedBytes = Bytes(simulation);
                var pickup = Portable(simulation, CommandKind.HandlePortableEquipment,
                    TestOnlyExpeditionCampConstructionFixture.TentLotId, handling: HandlingKind.Pickup);
                var blockedPickup = simulation.Execute(host, pickup);
                Require(blockedPickup.Outcome == Outcome.Rejected && blockedPickup.Code == "PortableItemHasPendingWork"
                    && Bytes(simulation).SequenceEqual(pausedBytes),
                    "A paused installation claim did not continue to protect the physical tent from ordinary pickup: "
                    + blockedPickup.Outcome + "/" + blockedPickup.Code + ".");
                WorldAdvance(simulation, 3600);
                Require(simulation.Capture().TemporaryCampConstructionAttempts.Single().WorkDone == new RuleTime(14400),
                    "Paused construction received work from elapsed world time.");

                string path = Path.Combine(directory, "temporary-camp-construction-paused.ddsave");
                var store = new FileSaveStore(); store.Save(path, simulation.Capture());
                byte[] saved = File.ReadAllBytes(path);
                var restoredSnapshot = store.Load(path);
                var restored = new Simulation(CampConstructionPolicy(seed), restoredSnapshot, ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(restored))
                    && codec.Encode(codec.Decode(saved)).SequenceEqual(saved),
                    "Paused schema70 construction did not survive canonical save/restore.");

                var left = new Simulation(CampConstructionPolicy(seed), codec.Decode(saved), ExecutionProfile.Laboratory);
                var right = new Simulation(CampConstructionPolicy(seed), codec.Decode(saved), ExecutionProfile.Laboratory);
                string activeId = left.Capture().TemporaryCampConstructionAttempts.Single().Id;
                var resume = CampConstructionCommand(left, CommandKind.ResumeTemporaryCampConstruction, activeId, "resume");
                Require(left.QueryCommand(host, resume).Admissible,
                    "A restored attempt with both original claims and trained crew was not resumable.");
                WorldCommit(left, resume);
                var sameResume = CampConstructionCommand(right, CommandKind.ResumeTemporaryCampConstruction, activeId, "resume");
                WorldCommit(right, sameResume);
                var completionLeft = IC(left, CommandKind.AdvanceClock, x: 14400, y: 1, id: "camp-build.finish");
                var completionRight = IC(right, CommandKind.AdvanceClock, x: 14400, y: 1, id: "camp-build.finish");
                WorldCommit(left, completionLeft);
                WorldCommit(right, completionRight);
                Require(Bytes(left).SequenceEqual(Bytes(right)),
                    "Two identical resumed command histories from the same save produced different serialized state.");
                var completed = left.Capture();
                attempt = completed.TemporaryCampConstructionAttempts.Single();
                Require(attempt.Status == TemporaryCampConstructionStatus.Resolved
                    && attempt.Check != null && attempt.Check.Result >= TemporaryCampConstructionResult.Success
                    && attempt.Check.Dc == TemporaryCampConstructionValidation.TierDc(1)
                    && attempt.Check.AssistantBonus == 1
                    && TemporaryCampConstructionValidation.SupportMarks(completed, PressureCampId)
                        == (attempt.Check.Result == TemporaryCampConstructionResult.CriticalSuccess ? 2 : 1)
                    && completed.TemporaryCampInstallations.Count(x => x.AttemptId == attempt.Id) == 2
                    && TemporaryCampConstructionValidation.HasTemporaryCamp(completed, PressureCampId)
                    && completed.Work.Lots.Single(x => x.Id == attempt.TentLotId).Amount == new RuleQuantity(20)
                    && completed.Work.Lots.Single(x => x.Id == attempt.PackLotId).Amount == new RuleQuantity(20),
                    "A successful shared check did not install both unconsumed physical lots exactly once.");
                var capacity = TemporaryCampConstructionValidation.StorageCapacity(completed, PressureCampId);
                Require(capacity.Load == 20 && capacity.Pounds == new RuleQuantity(200)
                    && capacity.CubicFeet == new RuleQuantity(20),
                    "Installed fixture did not expose its derived bounded storage capacity.");
                var afterDuplicateBytes = Bytes(left);
                var duplicate = left.Execute(host, completionLeft);
                Require(duplicate.Outcome == Outcome.Duplicate && Bytes(left).SequenceEqual(afterDuplicateBytes),
                    "Repeated completion command changed the resolved check or installed items.");

                // The installation does not alter the pre-existing exposure facts. Actual camp use
                // remains the only source of its existing exposed-site Pressure increment.
                var site = completed.ExpeditionCampSites.Single();
                Require(site.Exposed && !site.Concealed, "Construction rewrote the authored site exposure profile.");
                CampConstructionCommit(left, CommandKind.BeginCampUse, PressureCampId, "camp-use.begin");
                PressureAdvanceTo(left, new RuleTime(ExpeditionPressureRules.WatchSeconds * 2));
                var pressure = left.Capture();
                var secondWatch = pressure.ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 1);
                var exposedUseCause = pressure.ExpeditionPressureChanges.SingleOrDefault(x =>
                    x.Kind == ExpeditionPressureChangeKind.ExposedCampUse && x.WatchIndex == 1);
                Require(exposedUseCause != null && secondWatch.Context == ExpeditionPressureCheckpointContext.Camp
                    && secondWatch.CauseIds.Contains(exposedUseCause.Id, StringComparer.Ordinal)
                    && pressure.ExpeditionCampSites.Single().Exposed,
                    "After construction, the existing exposed camp-use Pressure rule did not remain authoritative: "
                    + string.Join(",", pressure.ExpeditionPressureChanges.Select(x => x.Kind + "@" + x.WatchIndex))
                    + "; uses=" + string.Join(",", pressure.ExpeditionCampActivities.Where(x => x.Kind == ExpeditionCampActivityKind.Use)
                        .Select(x => x.StartedAt + "-" + (x.EndedAt?.ToString() ?? "active")))
                    + "; checkpoints=" + string.Join(",", pressure.ExpeditionPressureCheckpoints.Select(x => x.WatchIndex + ":" + x.At))
                    + "; clock=" + pressure.RuleClock + ".");

                var uninterrupted = CampConstructionAtCheckpoint(seed);
                CampConstructionCommit(uninterrupted, CommandKind.StartTemporaryCampConstruction, PressureCampId, "start");
                var wholeClock = IC(uninterrupted, CommandKind.AdvanceClock, x: 28800, y: 1, id: "camp-build.whole.finish");
                WorldCommit(uninterrupted, wholeClock);
                var whole = uninterrupted.Capture();
                var split = left.Capture();
                var wholeAttempt = whole.TemporaryCampConstructionAttempts.Single();
                var splitAttempt = split.TemporaryCampConstructionAttempts.Single();
                Require(wholeAttempt.WorkDone == splitAttempt.WorkDone && wholeAttempt.Check.Result >= TemporaryCampConstructionResult.Success
                    && splitAttempt.Check.Result >= TemporaryCampConstructionResult.Success
                    && whole.TemporaryCampInstallations.Select(x => new { x.Kind, x.SiteId, x.LotId })
                        .OrderBy(x => x.Kind).ThenBy(x => x.LotId, StringComparer.Ordinal)
                        .SequenceEqual(split.TemporaryCampInstallations.Select(x => new { x.Kind, x.SiteId, x.LotId })
                            .OrderBy(x => x.Kind).ThenBy(x => x.LotId, StringComparer.Ordinal)),
                    "Uninterrupted and paused/resumed construction did not produce semantically equivalent work and installations.");
            });

            cases.Add("temporary_camp_construction_failure_releases_claims_and_retries_fresh", () => {
                uint seed = CampConstructionSeed(success: false);
                var simulation = CampConstructionAtCheckpoint(seed);
                CampConstructionCommit(simulation, CommandKind.StartTemporaryCampConstruction, PressureCampId, "fail.start");
                var finish = IC(simulation, CommandKind.AdvanceClock, x: 28800, y: 1, id: "camp-build.fail.finish");
                WorldCommit(simulation, finish);
                var state = simulation.Capture(); var attempt = state.TemporaryCampConstructionAttempts.Single();
                Require(attempt.Status == TemporaryCampConstructionStatus.Resolved
                    && attempt.Check.Result < TemporaryCampConstructionResult.Success
                    && TemporaryCampConstructionValidation.SupportMarks(state, PressureCampId) == 0
                    && !TemporaryCampConstructionValidation.HasTemporaryCamp(state, PressureCampId)
                    && state.TemporaryCampInstallations.Length == 0
                    && state.Work.Lots.Single(x => x.Id == attempt.TentLotId).Amount == new RuleQuantity(20)
                    && state.Work.Lots.Single(x => x.Id == attempt.PackLotId).Amount == new RuleQuantity(20)
                    && state.Work.Reservations.Count(x => x.JobId == attempt.Id
                        && x.ReleasedAmount == new RuleQuantity(20) && x.RemainingAmount == default(RuleQuantity)) == 2,
                    "Failed construction damaged a fixture, installed an item, or retained an active material claim.");
                byte[] resolved = Bytes(simulation);
                var duplicate = simulation.Execute(host, finish);
                Require(duplicate.Outcome == Outcome.Duplicate && Bytes(simulation).SequenceEqual(resolved),
                    "Duplicated failure completion rerolled or settled claims twice.");
                var retry = CampConstructionCommand(simulation, CommandKind.StartTemporaryCampConstruction,
                    PressureCampId, "retry");
                Require(simulation.QueryCommand(host, retry).Admissible,
                    "A resolved failed attempt did not allow a fresh full-duration retry.");
                WorldCommit(simulation, retry);
                var retried = simulation.Capture().TemporaryCampConstructionAttempts.OrderBy(x => x.StartedRevision).Last();
                Require(retried.WorkDone == default(RuleTime) && retried.Status == TemporaryCampConstructionStatus.Working
                    && retried.StartedAt == simulation.Capture().RuleClock
                    && simulation.Capture().Work.Reservations.Count(x => x.JobId == retried.Id
                        && x.RemainingAmount == new RuleQuantity(20)) == 2,
                    "Retry inherited prior labor or claim settlement instead of beginning a fresh attempt.");
            });

            cases.Add("temporary_camp_construction_and_lying_low_exclude_each_other", () => {
                var simulation = CampConstructionAtCheckpoint(seed: 1, concealed: true);
                CampConstructionCommit(simulation, CommandKind.BeginCampUse, PressureCampId, "low.use.begin");
                CampConstructionCommit(simulation, CommandKind.BeginLyingLow, PressureCampId, "low.begin");
                var start = CampConstructionCommand(simulation, CommandKind.StartTemporaryCampConstruction,
                    PressureCampId, "low.blocked-start");
                var blocked = simulation.QueryCommand(host, start);
                Require(blocked.Supported && !blocked.Admissible
                    && blocked.Code == "TemporaryCampConstructionConflictsWithLyingLow",
                    "A live lying-low interval did not block construction with the documented reason.");
                RejectUnchanged(simulation, host, start, "TemporaryCampConstructionConflictsWithLyingLow");
                CampConstructionCommit(simulation, CommandKind.EndLyingLow, PressureCampId, "low.end");
                CampConstructionCommit(simulation, CommandKind.EndCampUse, PressureCampId, "low.use.end");
                CampConstructionCommit(simulation, CommandKind.StartTemporaryCampConstruction, PressureCampId, "low.start");
                CampConstructionCommit(simulation, CommandKind.BeginCampUse, PressureCampId, "low.work.use.begin");
                var lieDown = CampConstructionCommand(simulation, CommandKind.BeginLyingLow, PressureCampId, "low.work.blocked");
                var query = simulation.QueryCommand(host, lieDown);
                Require(query.Supported && !query.Admissible && query.Code == "LyingLowConflictsWithActiveWork",
                    "Lying-low began while the same lead held active construction work.");
                RejectUnchanged(simulation, host, lieDown, "LyingLowConflictsWithActiveWork");
            });
        }
    }
}
#endif
