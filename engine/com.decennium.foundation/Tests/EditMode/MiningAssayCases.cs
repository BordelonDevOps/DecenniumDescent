#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static MiningAssayProfileRecord MiningAssayProfile(string id, int? exactDc = null,
            string[] categories = null, MiningAssayFindingRecord[] findings = null)
        {
            categories = categories ?? new[] { SharedMiningFixture.CategoryA, SharedMiningFixture.CategoryB };
            findings = findings ?? new[] {
                new MiningAssayFindingRecord("TEST_ONLY.assay.finding.iron", SharedMiningFixture.CategoryA,
                    MiningAssayFindingKind.SupportedCategory, ""),
                new MiningAssayFindingRecord("TEST_ONLY.assay.finding.copper", SharedMiningFixture.CategoryB,
                    MiningAssayFindingKind.SupportedCategory, ""),
                new MiningAssayFindingRecord("TEST_ONLY.assay.finding.iron-use", SharedMiningFixture.CategoryA,
                    MiningAssayFindingKind.Suitability, "TEST_ONLY: suitable for the authored iron-use example."),
                new MiningAssayFindingRecord("TEST_ONLY.assay.finding.copper-handling", SharedMiningFixture.CategoryB,
                    MiningAssayFindingKind.HandlingRequirement, "TEST_ONLY: handle using the authored copper-handling example.")
            };
            return new MiningAssayProfileRecord(id, SharedMiningFixture.DepositId, SharedMiningFixture.DepositVersionId,
                exactDc, 1, categories, new[] { SharedMiningFixture.MiningToolsId }, findings);
        }

        private static uint MiningAssaySeed(TaskDegree degree, int modifier, int dc, int disadvantageSources = 0)
        {
            for (uint seed = 1; seed < 1000000; seed++) {
                var roll = PlaytestDice.RollD20(seed, disadvantageSources: disadvantageSources);
                if (PlaytestRolls.TaskCheck(roll.Natural, modifier, dc).Degree == degree) return seed;
            }
            throw new Exception("No deterministic assay seed for " + degree + ".");
        }

        private static Command MiningAssayCommand(Simulation simulation, CommandKind kind, string target,
            string actor = SharedMiningFixture.OwnerId, string id = null)
        {
            var state = simulation.Capture();
            return new Command(id ?? "mining-assay.command." + (state.Revision + 1), actor, state.Revision, kind, target);
        }

        private static void MiningAssayCommit(Simulation simulation, Command command)
        {
            var result = simulation.Execute(TestOnlySharedWorldPolicy.Host(), command);
            Require(result.Outcome == Outcome.Committed, command.Kind + " rejected: " + result.Code);
        }

        private static string[] MiningAssayStockSignature(Snapshot state)
        {
            var units = state.MiningUnits.Select(x => "unit|" + x.Id + "|" + x.DepositId + "|" + x.CategoryId + "|"
                + x.MassPounds + "|" + x.VolumeCubicFeet + "|" + (x.ValueCopper?.ToString() ?? "-") + "|"
                + (int)x.Condition + "|" + (int)x.Status + "|" + x.ReceivedLotId + "|" + x.ReceivedContainerId);
            var items = state.PortableEquipment.Select(x => "item|" + x.Id + "|" + x.CustodianId + "|" + x.ParentId + "|"
                + (int)x.Placement + "|" + (int)x.LinkKind + "|" + x.LinkedId + "|" + x.GroundX + "|" + x.GroundY + "|"
                + x.SourceWeightLb + "|" + x.OperationalWeightLb);
            var lots = state.Work.Lots.Select(x => "lot|" + x.Id + "|" + x.UnitId + "|" + x.Amount + "|" + x.LocationId + "|" + x.CustodianId);
            return units.Concat(items).Concat(lots).OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        private static SharedMiningFixture DestructiveAssayFixture(out MiningAssayProfileRecord method,
            out DestructiveMiningAssayProfileRecord destructiveProfile, out DestructiveMiningAssayProfileRecord equivalentProfile)
        {
            const string methodId = "TEST_ONLY.assay.method.prepared-sample";
            const string sampleId = "TEST_ONLY.assay.sample.prepared-iron";
            const string lotId = "TEST_ONLY.assay.lot.prepared-iron";
            var amount = RuleQuantity.FromFraction(1, 4);
            method = new MiningAssayProfileRecord(methodId, SharedMiningFixture.DepositId,
                SharedMiningFixture.DepositVersionId, null, 1, new[] { SharedMiningFixture.CategoryA },
                new[] { SharedMiningFixture.MiningToolsId }, new[] {
                    new MiningAssayFindingRecord("TEST_ONLY.assay.sample.iron-category", SharedMiningFixture.CategoryA,
                        MiningAssayFindingKind.SupportedCategory, ""),
                    new MiningAssayFindingRecord("TEST_ONLY.assay.sample.iron-use", SharedMiningFixture.CategoryA,
                        MiningAssayFindingKind.Suitability, "TEST_ONLY: prepared sample suitability.")
                });
            var sample = new MiningAssaySampleRecord(sampleId, SharedMiningFixture.DepositId,
                SharedMiningFixture.DepositVersionId, SharedMiningFixture.CategoryA, lotId, amount, new[] { methodId });
            var physical = new PortableEquipmentRecord(sampleId, "TEST_ONLY.prepared-mineral-sample",
                SharedMiningFixture.OwnerId, SharedMiningFixture.OwnerId, "", PortablePlacement.Ground,
                PortableLinkKind.InventoryLot, lotId, PortableMassBasis.GenericPounds, amount, null, groundX: 3, groundY: 3);
            var sampleFixture = new MiningAssaySampleFixture(sample,
                new ResourceLot(lotId, "mass-pound", amount, "ground.3.3", SharedMiningFixture.OwnerId),
                new InventoryLotRecord(lotId, "", SharedMiningFixture.OwnerId, amount, default,
                    NutritionKind.None, null, InventoryAccess.Ground), physical);
            destructiveProfile = new DestructiveMiningAssayProfileRecord("TEST_ONLY.assay.destructive.iron",
                sampleId, methodId, amount);
            equivalentProfile = new DestructiveMiningAssayProfileRecord("TEST_ONLY.assay.destructive.iron.renamed",
                sampleId, methodId, amount);
            return new SharedMiningFixture(assayProfiles: new[] { method }, assaySamples: new[] { sampleFixture },
                destructiveAssayProfiles: new[] { destructiveProfile, equivalentProfile });
        }

        private static int MiningAssayExactDcFlagOffset(byte[] bytes, string profileId)
        {
            byte[] text = Encoding.UTF8.GetBytes(profileId);
            byte[] needle = BitConverter.GetBytes(text.Length).Concat(text).ToArray();
            int offset = -1;
            for (int i = 0; i <= bytes.Length - needle.Length; i++) {
                bool match = true;
                for (int j = 0; j < needle.Length; j++) if (bytes[i + j] != needle[j]) { match = false; break; }
                if (match) { offset = i; break; }
            }
            if (offset < 0) throw new Exception("Mining assay profile was not found in the encoded fixture.");
            using (var stream = new MemoryStream(bytes, false)) using (var reader = new BinaryReader(stream, Encoding.UTF8, true)) {
                stream.Position = offset;
                void SkipText() { int length = reader.ReadInt32(); if (length < 0 || length > 512) throw new Exception("Invalid encoded assay text."); stream.Position += length; }
                SkipText(); SkipText(); SkipText();
                return checked((int)stream.Position);
            }
        }

        private static void AddMiningAssayCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("mining_assay_findings_are_scoped_to_the_successful_profile", () => {
                const string worker = "TEST_ONLY.assay.worker";
                const string findingId = "TEST_ONLY.assay.shared-finding-id";
                var learnedFact = new MiningAssayFindingRecord(findingId, "TEST_ONLY.assay.category.one",
                    MiningAssayFindingKind.SupportedCategory, "");
                var unrelatedFact = new MiningAssayFindingRecord(findingId, "TEST_ONLY.assay.category.two",
                    MiningAssayFindingKind.SupportedCategory, "");
                var learnedProfile = new MiningAssayProfileRecord("TEST_ONLY.assay.profile.one", "TEST_ONLY.assay.deposit.one",
                    "TEST_ONLY.assay.deposit.one.v1", 12, 0, new[] { learnedFact.CategoryId }, Array.Empty<string>(), new[] { learnedFact });
                var unrelatedProfile = new MiningAssayProfileRecord("TEST_ONLY.assay.profile.two", "TEST_ONLY.assay.deposit.two",
                    "TEST_ONLY.assay.deposit.two.v1", 12, 0, new[] { unrelatedFact.CategoryId }, Array.Empty<string>(), new[] { unrelatedFact });
                var attempt = new MiningAssayAttemptRecord("TEST_ONLY.assay.attempt.one", worker, learnedProfile.Id,
                    learnedProfile.DepositId, learnedProfile.DepositVersionId, default, new RuleTime(60), new RuleTime(60),
                    MiningAssayStatus.Success, 0, 1, 2, 12, new RuleTime(60), MiningCheckDegree.Success,
                    MiningDiceSelection.Normal, 12, 0, 12, 2, 1, 2, 1, new[] { findingId });
                var state = new Snapshot { RuleClock = new RuleTime(60), MiningAssayProfiles = new[] { learnedProfile, unrelatedProfile },
                    MiningAssayAttempts = new[] { attempt } };
                var learned = MiningAssayValidation.FindingsFor(state, worker);
                Require(learned.Length == 1 && learned[0].Id == findingId
                    && learned[0].CategoryId == learnedFact.CategoryId,
                    "A successful assay exposed a different profile's fact through a shared finding ID.");
            });
            cases.Add("mining_assay_uses_shared_work_save_resume_and_only_authored_findings", () => {
                var profile = MiningAssayProfile("TEST_ONLY.assay.profile.tier-fallback");
                var fixture = new SharedMiningFixture(assayProfiles: new[] { profile });
                var unseeded = TestOnlySharedWorldPolicy.WithMining(fixture);
                var initial = unseeded.Initial();
                Require(MiningAssayValidation.Difficulty(initial, profile) == 13,
                    "Assay DC fallback did not use the highest assessed tier.");
                uint seed = MiningAssaySeed(TaskDegree.Success, MiningModifier(initial), 13);
                var policy = TestOnlySharedWorldPolicy.WithMining(fixture, seed);
                var simulation = World(policy);
                var startingBytes = Bytes(simulation);
                var option = simulation.DiscoverCommands(host, SharedMiningFixture.OwnerId).Single(x =>
                    x.Command.Kind == CommandKind.StartMiningAssay && x.Command.Target == profile.Id);
                Require(option.Query.Admissible && option.Query.Costs.Any(x => x.Kind == "work-seconds" && x.Amount == 60)
                    && startingBytes.SequenceEqual(Bytes(simulation)),
                    "Assay discovery omitted its one-minute shared-work cost or mutated state.");

                var before = simulation.Capture();
                string[] stockBefore = MiningAssayStockSignature(before);
                var start = MiningAssayCommand(simulation, CommandKind.StartMiningAssay, profile.Id, id: "assay.start");
                MiningAssayCommit(simulation, start);
                var attempt = simulation.Capture().MiningAssayAttempts.Single();
                Require(attempt.Status == MiningAssayStatus.Working && attempt.CheckDc == 13
                    && attempt.ProficiencyRank == 1 && simulation.Capture().RandomState == before.RandomState
                    && simulation.Capture().Work.WorkerIntervals.Any(x => x.JobId == attempt.Id)
                    && !simulation.Capture().Work.Reservations.Any(x => x.JobId == attempt.Id),
                    "Starting assay rolled early, failed to book labor, or reserved nonexistent mineral stock.");

                WorldAdvance(simulation, 20);
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.PauseMiningAssay, attempt.Id));
                byte[] pausedSave = Bytes(simulation);
                simulation = new Simulation(policy, new SnapshotCodec().Decode(pausedSave), ExecutionProfile.Laboratory);
                Require(pausedSave.SequenceEqual(Bytes(simulation))
                    && simulation.Capture().MiningAssayAttempts.Single().Status == MiningAssayStatus.Paused
                    && simulation.Capture().MiningAssayAttempts.Single().WorkDone == new RuleTime(20),
                    "Partial assay work did not survive the schema45 save/restore round trip.");

                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.ResumeMiningAssay, attempt.Id));
                WorldAdvance(simulation, 40);
                var completed = simulation.Capture();
                attempt = completed.MiningAssayAttempts.Single();
                string[] expected = profile.Findings.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal).ToArray();
                var learned = MiningAssayValidation.FindingsFor(completed, SharedMiningFixture.OwnerId);
                Require((attempt.Status == MiningAssayStatus.Success || attempt.Status == MiningAssayStatus.CriticalSuccess)
                    && attempt.WorkDone == new RuleTime(60) && attempt.ResolvedAt == completed.RuleClock
                    && attempt.RandomBefore == seed && attempt.RandomAfter == completed.RandomState
                    && attempt.FindingIds.SequenceEqual(expected) && learned.Select(x => x.Id).SequenceEqual(expected)
                    && learned.Select(x => x.Fact).Contains("TEST_ONLY: suitable for the authored iron-use example.")
                    && learned.Select(x => x.Fact).Contains("TEST_ONLY: handle using the authored copper-handling example.")
                    && MiningAssayStockSignature(completed).SequenceEqual(stockBefore)
                    && completed.MiningAttempts.Length == before.MiningAttempts.Length,
                    "Completed assay revealed unsupported facts, changed source stock, or failed to resolve its one check.");
                byte[] settled = Bytes(simulation);
                var duplicate = simulation.Execute(host, start);
                Require(duplicate.Outcome == Outcome.Duplicate && settled.SequenceEqual(Bytes(simulation)),
                    "Replaying the durable assay command changed its findings or shared simulation state.");
            });

            cases.Add("mining_assay_uses_exact_source_dc_and_untrained_disadvantage_without_consumption", () => {
                var profile = MiningAssayProfile("TEST_ONLY.assay.profile.exact-untrained", exactDc: 18,
                    categories: new[] { SharedMiningFixture.CategoryA }, findings: new[] {
                        new MiningAssayFindingRecord("TEST_ONLY.assay.exact.supported", SharedMiningFixture.CategoryA,
                            MiningAssayFindingKind.SupportedCategory, ""),
                        new MiningAssayFindingRecord("TEST_ONLY.assay.exact.suitability", SharedMiningFixture.CategoryA,
                            MiningAssayFindingKind.Suitability, "TEST_ONLY: exact-profile suitability example.")
                    });
                var fixture = new SharedMiningFixture(trained: false, assayProfiles: new[] { profile });
                var unseeded = TestOnlySharedWorldPolicy.WithMining(fixture);
                var initial = unseeded.Initial();
                uint seed = MiningAssaySeed(TaskDegree.Failure, MiningModifier(initial), 18, disadvantageSources: 1);
                var policy = TestOnlySharedWorldPolicy.WithMining(fixture, seed);
                var simulation = World(policy);
                string[] stockBefore = MiningAssayStockSignature(simulation.Capture());
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.StartMiningAssay, profile.Id,
                    id: "assay.exact.start"));
                WorldAdvance(simulation, 60);
                var state = simulation.Capture(); var attempt = state.MiningAssayAttempts.Single();
                Require(MiningAssayValidation.Difficulty(state, profile) == 18 && attempt.CheckDc == 18
                    && attempt.ProficiencyRank == 0 && attempt.ProficiencyBonus == 0
                    && attempt.DiceSelection == MiningDiceSelection.Disadvantage
                    && (attempt.Status == MiningAssayStatus.Failure || attempt.Status == MiningAssayStatus.CriticalFailure)
                    && attempt.FindingIds.Length == 0
                    && MiningAssayValidation.FindingsFor(state, SharedMiningFixture.OwnerId).Length == 0
                    && MiningAssayStockSignature(state).SequenceEqual(stockBefore),
                    "Untrained assay did not use its exact DC/disadvantage or failure exposed facts/consumed stock.");
                RejectUnchanged(simulation, host, MiningAssayCommand(simulation, CommandKind.StartMiningAssay, profile.Id,
                    id: "assay.exact.repeat"), "MiningAssayEvidenceAlreadyAttempted");
            });

            cases.Add("mining_assay_codec_rejects_noncanonical_exact_dc_flag", () => {
                var profile = MiningAssayProfile("TEST_ONLY.assay.profile.codec");
                var policy = TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture(assayProfiles: new[] { profile }));
                byte[] bytes = new SnapshotCodec().Encode(policy.Initial());
                int flag = MiningAssayExactDcFlagOffset(bytes, profile.Id);
                Require(bytes[flag] == 0, "The fixture should encode an absent exact assay DC as false.");
                bytes[flag] = 2; Resign(bytes);
                Throws<InvalidDataException>(() => new SnapshotCodec().Decode(bytes));
            });

            cases.Add("mining_destructive_assay_consumes_one_authored_portion_at_first_work_and_resumes_from_save", () => {
                var fixture = DestructiveAssayFixture(out var method, out var profile, out var equivalent);
                var unseeded = TestOnlySharedWorldPolicy.WithMining(fixture);
                var initial = unseeded.Initial();
                int dc = MiningAssayValidation.Difficulty(initial, method);
                uint seed = MiningAssaySeed(TaskDegree.Success, MiningModifier(initial), dc);
                var policy = TestOnlySharedWorldPolicy.WithMining(fixture, seed);
                var simulation = World(policy);
                var sample = simulation.Capture().MiningAssaySamples.Single();
                var lotBefore = simulation.Capture().Work.Lots.Single(x => x.Id == sample.InventoryLotId);
                var start = simulation.DiscoverCommands(host, SharedMiningFixture.OwnerId).Single(x =>
                    x.Command.Kind == CommandKind.StartMiningAssay && x.Command.Target == profile.Id);
                byte[] beforeStart = Bytes(simulation);
                Require(start.Query.Admissible && start.Query.Costs.Any(x => x.Kind == "work-seconds" && x.Amount == 60)
                    && beforeStart.SequenceEqual(Bytes(simulation)), "Destructive assay discovery did not expose a pure one-minute start.");
                MiningAssayCommit(simulation, start.Command);
                var attempt = simulation.Capture().DestructiveMiningAssayAttempts.Single();
                var claim = simulation.Capture().Work.Reservations.Single(x => x.Id == attempt.ReservationId);
                Require(attempt.Status == MiningAssayStatus.Working && attempt.SampleAmount == sample.Amount
                    && claim.Amount == sample.Amount && claim.ConsumedAmount == default(RuleQuantity)
                    && simulation.Capture().Work.Lots.Single(x => x.Id == sample.InventoryLotId).Amount == lotBefore.Amount
                    && simulation.Capture().RandomState == seed,
                    "Starting assay did not reserve the exact physical sample without early debit or RNG use.");

                WorldAdvance(simulation, 20);
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.PauseMiningAssay, attempt.Id));
                var paused = simulation.Capture();
                claim = paused.Work.Reservations.Single(x => x.Id == attempt.ReservationId);
                Require(paused.DestructiveMiningAssayAttempts.Single().WorkDone == new RuleTime(20)
                    && paused.DestructiveMiningAssayAttempts.Single().Status == MiningAssayStatus.Paused
                    && paused.Work.Lots.Single(x => x.Id == sample.InventoryLotId).Amount == default(RuleQuantity)
                    && claim.ConsumedAmount == sample.Amount && claim.ReleasedAmount == default(RuleQuantity),
                    "First positive work did not consume the authored sample exactly once before pause.");
                byte[] pausedSave = Bytes(simulation);
                simulation = new Simulation(policy, new SnapshotCodec().Decode(pausedSave), ExecutionProfile.Laboratory);
                Require(pausedSave.SequenceEqual(Bytes(simulation)), "Schema46 assay sample, debit provenance or partial work changed on save/restore.");
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.ResumeMiningAssay, attempt.Id));
                WorldAdvance(simulation, 40);

                var completed = simulation.Capture();
                attempt = completed.DestructiveMiningAssayAttempts.Single();
                var findings = MiningAssayValidation.FindingsFor(completed, SharedMiningFixture.OwnerId);
                claim = completed.Work.Reservations.Single(x => x.Id == attempt.ReservationId);
                Require((attempt.Status == MiningAssayStatus.Success || attempt.Status == MiningAssayStatus.CriticalSuccess)
                    && attempt.WorkDone == new RuleTime(60) && attempt.ResolvedAt == completed.RuleClock
                    && attempt.EvidenceBasisId == sample.InventoryLotId && attempt.MethodProfileId == method.Id
                    && claim.ConsumedAmount == sample.Amount && completed.Work.Lots.Single(x => x.Id == sample.InventoryLotId).Amount == default(RuleQuantity)
                    && findings.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal)
                        .SequenceEqual(method.Findings.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal))
                    && completed.RandomState != seed,
                    "Resumed destructive assay did not resolve one authored finding set after exactly 60 seconds.");
                byte[] settled = Bytes(simulation);
                var duplicate = simulation.Execute(host, start.Command);
                Require(duplicate.Outcome == Outcome.Duplicate && settled.SequenceEqual(Bytes(simulation)),
                    "Duplicate destructive assay command changed its debit, check, or findings.");
                RejectUnchanged(simulation, host, MiningAssayCommand(simulation, CommandKind.StartMiningAssay,
                    equivalent.Id, id: "assay.same-evidence-method-repeat"), "MiningAssayEvidenceAlreadyAttempted");
            });

            cases.Add("mining_destructive_assay_cancellation_settles_prework_and_postwork_without_check_or_refund", () => {
                var fixture = DestructiveAssayFixture(out _, out var profile, out _);
                var policy = TestOnlySharedWorldPolicy.WithMining(fixture, seed: 17);
                var simulation = World(policy);
                uint randomBefore = simulation.Capture().RandomState;
                var sample = simulation.Capture().MiningAssaySamples.Single();
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.StartMiningAssay, profile.Id,
                    id: "assay.cancel.before.start"));
                var first = simulation.Capture().DestructiveMiningAssayAttempts.Last();
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.CancelMiningAssay, first.Id,
                    id: "assay.cancel.before.cancel"));
                var prework = simulation.Capture();
                var preClaim = prework.Work.Reservations.Single(x => x.Id == first.ReservationId);
                Require(prework.DestructiveMiningAssayAttempts.Single(x => x.Id == first.Id).Status == MiningAssayStatus.Cancelled
                    && prework.DestructiveMiningAssayAttempts.Single(x => x.Id == first.Id).WorkDone == default(RuleTime)
                    && preClaim.ConsumedAmount == default(RuleQuantity) && preClaim.ReleasedAmount == sample.Amount
                    && prework.Work.Lots.Single(x => x.Id == sample.InventoryLotId).Amount == sample.Amount
                    && prework.RandomState == randomBefore,
                    "Pre-work cancellation did not release the sample without debit or check.");

                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.StartMiningAssay, profile.Id,
                    id: "assay.cancel.after.start"));
                var second = simulation.Capture().DestructiveMiningAssayAttempts.Last();
                WorldAdvance(simulation, 1);
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.CancelMiningAssay, second.Id,
                    id: "assay.cancel.after.cancel"));
                var postwork = simulation.Capture();
                var postAttempt = postwork.DestructiveMiningAssayAttempts.Single(x => x.Id == second.Id);
                var postClaim = postwork.Work.Reservations.Single(x => x.Id == second.ReservationId);
                Require(postAttempt.Status == MiningAssayStatus.Cancelled && postAttempt.WorkDone == new RuleTime(1)
                    && !postAttempt.ResolvedAt.HasValue && postAttempt.FindingIds.Length == 0
                    && postClaim.ConsumedAmount == sample.Amount && postClaim.ReleasedAmount == default(RuleQuantity)
                    && postwork.Work.Lots.Single(x => x.Id == sample.InventoryLotId).Amount == default(RuleQuantity)
                    && postwork.RandomState == randomBefore,
                    "Post-work cancellation refunded consumed material, transferred labor, or resolved a check.");
                RejectUnchanged(simulation, host, MiningAssayCommand(simulation, CommandKind.StartMiningAssay,
                    profile.Id, id: "assay.consumed-sample-reuse"), "MiningAssaySampleUnavailable");
            });

            cases.Add("destructive_mining_assay_cancel_is_projected_as_an_activity_control", () => {
                var fixture = DestructiveAssayFixture(out _, out var profile, out _);
                var policy = TestOnlySharedWorldPolicy.WithMining(fixture);
                var simulation = World(policy);
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.StartMiningAssay, profile.Id));
                var state = simulation.Capture();
                var attempt = state.DestructiveMiningAssayAttempts.Single();
                var options = simulation.DiscoverCommands(host, attempt.WorkerId);
                var activity = WorldActivityProjection.OpenProcedures(state, options).Single(x => x.Id == attempt.Id);
                Require(activity.AvailableCommands.Any(x => x.Command.Kind == CommandKind.CancelMiningAssay
                    && x.Command.Target == attempt.Id && x.Query.Admissible),
                    "Destructive assay cancellation was discoverable but missing from the activity controls.");
            });

            cases.Add("mining_assay_projection_preserves_controls_for_all_open_procedure_kinds", () => {
                var assayFixture = DestructiveAssayFixture(out var method, out var destructiveProfile, out _);
                var fixture = new SharedMiningFixture(trained: true, assayProfiles: new[] { method },
                    assaySamples: assayFixture.AssaySamples, destructiveAssayProfiles: new[] { destructiveProfile });
                var policy = TestOnlySharedWorldPolicy.WithMining(fixture);
                var simulation = World(policy);
                string worker = SharedMiningFixture.OwnerId;
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.StartMiningAssay, method.Id,
                    actor: worker, id: "assay.mixed.normal.start"));
                var normal = simulation.Capture().MiningAssayAttempts.Single();
                WorldAdvance(simulation, 1);
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.PauseMiningAssay, normal.Id,
                    actor: worker, id: "assay.mixed.normal.pause"));
                MiningAssayCommit(simulation, MiningAssayCommand(simulation, CommandKind.StartMiningAssay, destructiveProfile.Id,
                    actor: worker, id: "assay.mixed.destructive.start"));

                var state = simulation.Capture();
                var options = simulation.DiscoverCommands(host, worker);
                var activities = WorldActivityProjection.OpenProcedures(state, options);
                var destructive = state.DestructiveMiningAssayAttempts.Single();
                var projected = activities.Single(x => x.Id == destructive.Id);
                Require(projected.AvailableCommands.Any(x => x.Command.Kind == CommandKind.PauseMiningAssay
                        && x.Command.Target == destructive.Id && x.Query.Admissible)
                    && projected.AvailableCommands.Any(x => x.Command.Kind == CommandKind.CancelMiningAssay
                        && x.Command.Target == destructive.Id && x.Query.Admissible),
                    "An open nondestructive assay suppressed the destructive assay's pause/cancel controls.");
            });

            cases.Add("mining_assay_profile_ids_are_unique_across_assay_kinds", () => {
                var fixture = DestructiveAssayFixture(out var method, out var destructiveProfile, out _);
                var colliding = new DestructiveMiningAssayProfileRecord(method.Id, destructiveProfile.SampleId,
                    method.Id, destructiveProfile.SampleAmount);
                Throws<ArgumentException>(() => {
                    var invalid = new SharedMiningFixture(trained: true, assayProfiles: new[] { method },
                        assaySamples: fixture.AssaySamples, destructiveAssayProfiles: new[] { colliding });
                    TestOnlySharedWorldPolicy.WithMining(invalid).Initial();
                });
            });

            cases.Add("destructive_assay_content_fingerprint_includes_source_and_policy_contract", () => {
                var fixture = DestructiveAssayFixture(out _, out _, out _);
                var policy = TestOnlySharedWorldPolicy.WithMining(fixture, seed: 17);
                Require(policy.ContentFingerprint == "TEST_ONLY.mining-v1-b03b365155f6cf0921fe84713d70a8cdfe7ce478397a6cd3886f9f44272f1030",
                    "Assay-bearing content no longer matches its source and policy contract fingerprint.");
            });
        }
    }
}
#endif
