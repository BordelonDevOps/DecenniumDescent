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
        private const string ProspectingWorker = TestOnlyPolicy.CompanionId;

        private static Command ProspectingCommand(Simulation simulation, CommandKind kind, string target,
            ProspectingExposureRequest exposure = null, string actor = ProspectingWorker, string id = null)
        {
            var state = simulation.Capture();
            return new Command(id ?? "prospecting.command." + (state.Revision + 1), actor, state.Revision, kind,
                target, prospectingExposure: exposure);
        }

        private static void ProspectingCommit(Simulation simulation, Command command)
        {
            var result = simulation.Execute(TestOnlySharedWorldPolicy.Host(), command);
            Require(result.Outcome == Outcome.Committed, command.Kind + " rejected: " + result.Code);
        }

        private static ProspectingPatchFixtureContent ProspectingPatchWithChange(string key, int x, int y,
            ProspectingSignSeverity signs, string firstFact, string changedFact)
        {
            string owner = ProspectingWorker;
            string patchId = "TEST_ONLY.prospecting." + key + ".patch";
            string firstExposure = "TEST_ONLY.prospecting." + key + ".exposure.v1";
            string renamedExposure = "TEST_ONLY.prospecting." + key + ".exposure.renamed";
            string changedExposure = "TEST_ONLY.prospecting." + key + ".exposure.v2";
            string firstFinding = "TEST_ONLY.prospecting." + key + ".finding.v1";
            string changedFinding = "TEST_ONLY.prospecting." + key + ".finding.v2";
            var first = new ProspectingObservationProfile(firstFinding, ProspectingObservationKind.MineralSign, firstFact);
            var changed = new ProspectingObservationProfile(changedFinding, ProspectingObservationKind.MineralSign, changedFact);
            var initial = new ProspectingExposureProfile(firstExposure, patchId, 75, true, true, signs,
                ProspectingMethodKind.VisualInspection, 0, "TEST_ONLY.prospecting.hazard.none", Array.Empty<string>(), new[] { firstFinding });
            var renamed = new ProspectingExposureProfile(renamedExposure, patchId, 75, true, true, signs,
                ProspectingMethodKind.VisualInspection, 0, "TEST_ONLY.prospecting.hazard.none", Array.Empty<string>(), new[] { firstFinding });
            var next = new ProspectingExposureProfile(changedExposure, patchId, 75, true, true, ProspectingSignSeverity.Obscured,
                ProspectingMethodKind.VisualInspection, 0, "TEST_ONLY.prospecting.hazard.none", Array.Empty<string>(), new[] { changedFinding });
            var patch = new ProspectingPatchRecord(patchId, owner, "TEST_ONLY.prospecting." + key + ".site", x, y, firstExposure);
            return new ProspectingPatchFixtureContent(patch, firstExposure, new[] { initial, renamed, next }, new[] { first, changed });
        }

        private static int ProspectingModifier(Snapshot state)
        {
            var character = state.Characters.Single(x => x.ActorId == ProspectingWorker);
            var skill = state.SkillTraining.SingleOrDefault(x => x.ActorId == ProspectingWorker && x.SkillId == "mining-tools");
            return checked(PlaytestCharacters.AbilityModifier(character.Abilities[4])
                + (skill == null ? 0 : PlaytestCharacters.ProficiencyBonus(character.Levels.Count) * (skill.ProficiencyRank == 2 ? 2 : 1)));
        }

        private static uint ProspectingSeed(TaskDegree degree, int modifier, int dc, int disadvantageSources = 0)
        {
            for (uint seed = 1; seed < 1000000; seed++) {
                var roll = PlaytestDice.RollD20(seed, disadvantageSources: disadvantageSources);
                if (PlaytestRolls.TaskCheck(roll.Natural, modifier, dc).Degree == degree) return seed;
            }
            throw new Exception("No deterministic prospecting seed for " + degree + ".");
        }

        private static void AddProspectingCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("prospecting_uses_authored_dc_and_success_degrees_reveal_only_observable_facts", () => {
                string fact = "A narrow dark green streak is visible across the exposed stone.";
                var clear = SharedProspectingFixture.Patch("clear", 3, 3, ProspectingSignSeverity.Clear,
                    new[] { new ProspectingObservationProfile("TEST_ONLY.prospecting.clear.sign", ProspectingObservationKind.MineralSign, fact) });
                var severe = SharedProspectingFixture.Patch("severe", 4, 3, ProspectingSignSeverity.SevereFeasible,
                    new[] { new ProspectingObservationProfile("TEST_ONLY.prospecting.severe.sign", ProspectingObservationKind.MineralSign, fact) });
                var renamedPatch = SharedProspectingFixture.Patch("renamed-clear", 3, 3, ProspectingSignSeverity.Clear,
                    new[] { new ProspectingObservationProfile("TEST_ONLY.prospecting.renamed-clear.sign", ProspectingObservationKind.MineralSign, fact) });
                Throws<ArgumentException>(()=>new SharedProspectingFixture(new[]{clear,renamedPatch}));
                foreach (var profile in new[] { clear, severe }) {
                    int dc = profile.Exposures.Single().Signs == ProspectingSignSeverity.Clear ? 12 : 18;
                    var fixture = new SharedProspectingFixture(new[] { profile }, trained: true, wisdom: 18);
                    var unseeded = TestOnlySharedWorldPolicy.WithProspecting(fixture);
                    int modifier = ProspectingModifier(unseeded.Initial());
                    TaskDegree targetDegree = profile == clear ? TaskDegree.Success : TaskDegree.CriticalSuccess;
                    uint seed = ProspectingSeed(targetDegree, modifier, dc);
                    var policy = TestOnlySharedWorldPolicy.WithProspecting(fixture, seed);
                    var simulation = World(policy); var before = simulation.Capture();
                    var start = simulation.DiscoverCommands(host, ProspectingWorker).Single(x => x.Command.Kind == CommandKind.StartProspecting
                        && x.Command.Target == profile.Patch.Id);
                    Require(start.Query.Admissible && start.Query.Costs.Any(x => x.Kind == "work-seconds" && x.Amount == 600)
                        && before.SchemaVersion == Snapshot.ProspectingSchema,
                        "The discovered prospecting job did not expose its ten-minute authored opportunity and schema44 state.");
                    var command = start.Command;
                    ProspectingCommit(simulation, command);
                    var open = simulation.Capture().ProspectingAttempts.Single();
                    Require(open.Status == ProspectingAttemptStatus.Working && open.CheckDc == dc && open.WisdomModifier == 4
                        && open.ProficiencyBonus == 2 && simulation.Capture().RandomState == before.RandomState
                        && simulation.Capture().MiningDeposits.Length == 0 && simulation.Capture().MiningUnits.Length == 0,
                        "Prospecting rolled early, used the wrong DC/ability, or created a mineral deposit.");
                    WorldAdvance(simulation, 599);
                    Require(simulation.Capture().ProspectingAttempts.Single().Status == ProspectingAttemptStatus.Working
                        && simulation.Capture().ProspectingAttempts.Single().WorkDone == new RuleTime(599),
                        "Prospecting completed before ten active minutes.");
                    WorldAdvance(simulation, 1);
                    var state = simulation.Capture(); var attempt = state.ProspectingAttempts.Single();
                    var observations = policy.ObservationsFor(state, ProspectingWorker);
                    Require((attempt.Status == ProspectingAttemptStatus.Success || attempt.Status == ProspectingAttemptStatus.CriticalSuccess)
                        && attempt.Status.ToString() == targetDegree.ToString()
                        && attempt.WorkDone == new RuleTime(600) && attempt.ResolvedAt == new RuleTime(600)
                        && attempt.FindingIds.SequenceEqual(profile.Exposures.Single().FindingIds)
                        && observations.Count == 1 && observations[0].ObservableFact == fact
                        && observations[0].Kind == ProspectingObservationKind.MineralSign
                        && policy.ObservationsFor(state, TestOnlyPolicy.ActorId).Count == 0
                        && state.MiningDeposits.Length == 0 && state.MiningCategories.Length == 0 && state.MiningUnits.Length == 0,
                        "Success and Critical Success must reveal the same authored observation to the lead only, without producing hidden geology.");
                    byte[] saved = Bytes(simulation);
                    simulation = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
                    Require(saved.SequenceEqual(Bytes(simulation)), "Prospecting check or observation ownership changed through save/restore.");
                    var duplicate = simulation.Execute(host, command);
                    Require(duplicate.Outcome == Outcome.Duplicate && saved.SequenceEqual(Bytes(simulation)),
                        "Duplicate prospecting start replay repeated the check or finding.");
                }
            });

            cases.Add("prospecting_untrained_disadvantage_and_failed_checks_reveal_no_reliable_finding", () => {
                var fact = new ProspectingObservationProfile("TEST_ONLY.prospecting.outcome.fact",
                    ProspectingObservationKind.MineralSign, "A pale line of mineral stain crosses the rock face.");
                var profile = SharedProspectingFixture.Patch("outcome", 3, 3, ProspectingSignSeverity.Clear, new[] { fact });
                foreach (TaskDegree degree in new[] { TaskDegree.Failure, TaskDegree.CriticalFailure }) {
                    var fixture = new SharedProspectingFixture(new[] { profile }, trained: false, wisdom: 18);
                    var unseeded = TestOnlySharedWorldPolicy.WithProspecting(fixture);
                    uint seed = ProspectingSeed(degree, ProspectingModifier(unseeded.Initial()), 12, disadvantageSources: 1);
                    var policy = TestOnlySharedWorldPolicy.WithProspecting(fixture, seed); var simulation = World(policy);
                    ProspectingCommit(simulation, ProspectingCommand(simulation, CommandKind.StartProspecting, profile.Patch.Id));
                    var started = simulation.Capture().ProspectingAttempts.Single();
                    Require(started.ProficiencyRank == 0 && started.ProficiencyBonus == 0 && started.WisdomModifier == 4,
                        "Untrained prospecting added a Mining-tools proficiency contribution.");
                    WorldAdvance(simulation, 600); var state = simulation.Capture(); var attempt = state.ProspectingAttempts.Single();
                    var expected = degree == TaskDegree.Failure ? ProspectingAttemptStatus.Failure : ProspectingAttemptStatus.CriticalFailure;
                    Require(attempt.Status == expected && attempt.DiceSelection == MiningDiceSelection.Disadvantage
                        && attempt.FirstDie >= 1 && attempt.SecondDie >= 1 && attempt.RandomBefore != attempt.RandomAfter
                        && attempt.FindingIds.Length == 0 && policy.ObservationsFor(state, ProspectingWorker).Count == 0
                        && state.MiningDeposits.Length == 0 && state.ProspectingExposures.Single().HazardDeclarationId == "TEST_ONLY.prospecting.hazard.none",
                        "A failed prospecting check revealed a reliable finding or applied an undeclared/implicit hazard.");
                }
            });

            cases.Add("prospecting_pause_save_resume_and_repeat_prevention_preserve_shared_labor", () => {
                var fact = new ProspectingObservationProfile("TEST_ONLY.prospecting.pause.fact",
                    ProspectingObservationKind.PossibleAccess, "A shallow opening remains visible from the exposed patch.");
                var profile = SharedProspectingFixture.Patch("pause", 3, 3, ProspectingSignSeverity.Obscured, new[] { fact });
                var fixture = new SharedProspectingFixture(new[] { profile }, trained: true, wisdom: 18);
                var unseeded = TestOnlySharedWorldPolicy.WithProspecting(fixture);
                uint seed = ProspectingSeed(TaskDegree.Success, ProspectingModifier(unseeded.Initial()), 15);
                var policy = TestOnlySharedWorldPolicy.WithProspecting(fixture, seed); var simulation = World(policy);
                var start = ProspectingCommand(simulation, CommandKind.StartProspecting, profile.Patch.Id);
                ProspectingCommit(simulation, start); WorldAdvance(simulation, 237);
                var attempt = simulation.Capture().ProspectingAttempts.Single();
                ProspectingCommit(simulation, ProspectingCommand(simulation, CommandKind.PauseProspecting, attempt.Id));
                var paused = simulation.Capture().ProspectingAttempts.Single();
                Require(paused.Status == ProspectingAttemptStatus.Paused && paused.WorkDone == new RuleTime(237)
                    && !simulation.Capture().Work.WorkerIntervals.Any(x => x.JobId == attempt.Id && x.Start <= simulation.Capture().RuleClock && x.End > simulation.Capture().RuleClock),
                    "Pausing did not retain prospecting labor and release its active shared worker interval.");
                string path = Path.Combine(directory, "prospecting-paused.bin"); new FileSaveStore().Save(path, simulation.Capture());
                simulation = new Simulation(policy, new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                var reconstructed = CommandHistory.Read(simulation.Capture().Receipts.Single(x => x.Id == start.Id));
                Require(reconstructed.Kind == CommandKind.StartProspecting && reconstructed.Target == profile.Patch.Id,
                    "Saved command history did not reconstruct the prospecting start request.");
                ProspectingCommit(simulation, ProspectingCommand(simulation, CommandKind.ResumeProspecting, attempt.Id));
                WorldAdvance(simulation, 363); var state = simulation.Capture();
                Require(state.ProspectingAttempts.Single().Status == ProspectingAttemptStatus.Success
                    && state.ProspectingAttempts.Single().WorkDone == new RuleTime(600)
                    && state.ProspectingAttempts.Single().ResolvedAt == new RuleTime(600),
                    "Save/resume did not complete exactly the retained remaining prospecting labor.");
                byte[] saved = Bytes(simulation);
                var replay = simulation.Execute(host, start);
                Require(replay.Outcome == Outcome.Duplicate && saved.SequenceEqual(Bytes(simulation)),
                    "Saved duplicate replay repeated a prospecting check.");
                RejectUnchanged(simulation, host, ProspectingCommand(simulation, CommandKind.StartProspecting, profile.Patch.Id,
                    actor: TestOnlyPolicy.ActorId), "ProspectingOpportunityAlreadyAttempted");
            });

            cases.Add("prospecting_new_exposure_requires_new_facts_and_invalidates_open_work_without_a_check", () => {
                var profile = ProspectingPatchWithChange("change", 3, 3, ProspectingSignSeverity.Clear,
                    "A thin gray vein is visible beneath the loose surface layer.",
                    "Fresh orange staining is visible along the newly exposed edge.");
                var fixture = new SharedProspectingFixture(new[] { profile }, trained: true, wisdom: 18);
                var unseeded = TestOnlySharedWorldPolicy.WithProspecting(fixture);
                uint seed = ProspectingSeed(TaskDegree.Success, ProspectingModifier(unseeded.Initial()), 15);
                var policy = TestOnlySharedWorldPolicy.WithProspecting(fixture, seed); var simulation = World(policy);
                var start = ProspectingCommand(simulation, CommandKind.StartProspecting, profile.Patch.Id);
                ProspectingCommit(simulation, start); WorldAdvance(simulation, 180);
                var inProgress = simulation.Capture().ProspectingAttempts.Single();
                var unchanged = ProspectingCommand(simulation, CommandKind.RecordProspectingExposure, profile.Patch.Id,
                    new ProspectingExposureRequest("TEST_ONLY.prospecting.change.exposure.renamed", "world.event.rename"));
                RejectUnchanged(simulation, host, unchanged, "ProspectingEvidenceUnchanged");
                var change = ProspectingCommand(simulation, CommandKind.RecordProspectingExposure, profile.Patch.Id,
                    new ProspectingExposureRequest("TEST_ONLY.prospecting.change.exposure.v2", "world.event.erosion.1"));
                var changeResult = simulation.Execute(host, change);
                Require(changeResult.Outcome == Outcome.Committed, "New authored exposure was rejected: " + changeResult.Code);
                var invalidatedState = simulation.Capture(); var invalidated = invalidatedState.ProspectingAttempts.Single();
                Require(invalidated.Status == ProspectingAttemptStatus.InvalidatedWithoutCheck
                    && invalidated.WorkDone == inProgress.WorkDone && invalidated.InvalidationCauseId == "world.event.erosion.1"
                    && !invalidated.RandomBefore.Equals(invalidatedState.RandomState) && invalidated.FirstDie == 0
                    && invalidated.FindingIds.Length == 0 && invalidated.ClosedAt == invalidatedState.RuleClock
                    && invalidatedState.ProspectingPatches.Single().CurrentExposureId == "TEST_ONLY.prospecting.change.exposure.v2"
                    && invalidatedState.MiningDeposits.Length == 0,
                    "Exposure replacement did not preserve labor, close the old attempt without a check, and record its cause.");
                ProspectingCommit(simulation, ProspectingCommand(simulation, CommandKind.StartProspecting, profile.Patch.Id));
                WorldAdvance(simulation, 600);
                var complete = simulation.Capture();
                var observations = policy.ObservationsFor(complete, ProspectingWorker);
                Require(complete.ProspectingAttempts.Length == 2
                    && complete.ProspectingAttempts.Single(x => x.ExposureId == "TEST_ONLY.prospecting.change.exposure.v2").CheckDc == 15
                    && observations.Count == 1 && observations[0].ObservableFact == "Fresh orange staining is visible along the newly exposed edge."
                    && !observations.Any(x => x.ObservableFact == "A thin gray vein is visible beneath the loose surface layer."),
                    "The new exposure did not support a separate observation or the invalidated attempt leaked findings.");
                byte[] saved = Bytes(simulation); simulation = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(simulation)), "Exposure cause, history or invalidation changed through save/restore.");
                var receipt = simulation.Capture().Receipts.Single(x => x.Id == change.Id);
                var reconstructed = CommandHistory.Read(receipt);
                Require(reconstructed.ProspectingExposure.ExposureId == "TEST_ONLY.prospecting.change.exposure.v2"
                    && reconstructed.ProspectingExposure.CauseId == "world.event.erosion.1",
                    "The trusted exposure-change event could not be reconstructed from its durable receipt.");
                var duplicate = simulation.Execute(host, reconstructed);
                Require(duplicate.Outcome == Outcome.Duplicate && saved.SequenceEqual(Bytes(simulation)),
                    "Duplicate exposure-event replay changed the evidence history or prospecting outcome.");
            });

            cases.Add("prospecting_requires_actual_authored_implements_and_method_hands", () => {
                const string patchId = "TEST_ONLY.prospecting.tools.patch";
                const string exposureId = "TEST_ONLY.prospecting.tools.exposure.v1";
                const string itemId = "TEST_ONLY.prospecting.tools.measurement-kit";
                var observation = new ProspectingObservationProfile("TEST_ONLY.prospecting.tools.fact",
                    ProspectingObservationKind.MineralSign, "Parallel green traces cross the exposed stone.");
                var exposure = new ProspectingExposureProfile(exposureId, patchId, 20, true, true, ProspectingSignSeverity.Clear,
                    ProspectingMethodKind.Measurement, 2, "TEST_ONLY.prospecting.hazard.none", new[] { itemId }, new[] { observation.Id });
                var patch = new ProspectingPatchRecord(patchId, ProspectingWorker, "TEST_ONLY.prospecting.tools.site", 3, 3, exposureId);
                var kit = new PortableEquipmentRecord(itemId, "TEST_ONLY.prospecting.measurement-kit", ProspectingWorker, ProspectingWorker, "",
                    PortablePlacement.Ground, PortableLinkKind.None, "", PortableMassBasis.Fixed, new RuleQuantity(1), new RuleQuantity(1), groundX: 3, groundY: 3);
                var profile = new ProspectingPatchFixtureContent(patch, exposureId, new[] { exposure }, new[] { observation }, new[] { kit });
                var policy = TestOnlySharedWorldPolicy.WithProspecting(new SharedProspectingFixture(new[] { profile }, trained: true));
                var simulation = World(policy);
                var option = simulation.DiscoverCommands(host, ProspectingWorker).Single(x => x.Command.Kind == CommandKind.StartProspecting
                    && x.Command.Target == patchId);
                Require(option.Query.Admissible && option.Query.Costs.Any(x => x.Kind == "work-seconds" && x.Amount == 600),
                    "Prospecting method did not validate its actual item and two-hand requirement through the shared command query.");
                ProspectingCommit(simulation, option.Command);

                var misplaced = new PortableEquipmentRecord(itemId, "TEST_ONLY.prospecting.measurement-kit", ProspectingWorker, ProspectingWorker, "",
                    PortablePlacement.Ground, PortableLinkKind.None, "", PortableMassBasis.Fixed, new RuleQuantity(1), new RuleQuantity(1), groundX: 4, groundY: 3);
                var blockedProfile = new ProspectingPatchFixtureContent(patch, exposureId, new[] { exposure }, new[] { observation }, new[] { misplaced });
                var blocked = World(TestOnlySharedWorldPolicy.WithProspecting(new SharedProspectingFixture(new[] { blockedProfile }, trained: true)));
                RejectUnchanged(blocked, host, ProspectingCommand(blocked, CommandKind.StartProspecting, patchId), "ProspectingAccessUnavailable");
            });
        }
    }
}
#endif
