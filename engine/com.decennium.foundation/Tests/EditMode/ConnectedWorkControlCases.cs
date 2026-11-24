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
        private static ConnectedExpeditionSession NewWorkControlExpedition()
            => ConnectedExpeditionSession.StartWithConnectedWorkControl(ClericInitialSelection.AuthoredExample(),
                ClericRepertoireSelection.AuthoredExample(), ClericMilestoneDeclaration.AuthoredExample(), BishopEntryRecord.Announced());

        private static void AddConnectedWorkControlCases(Dictionary<string, Action> cases, string directory)
        {
            foreach(bool nativeAdvance in new[] { false, true }) {
                bool advance = nativeAdvance;
                cases.Add("mgt02_work_control_model_mining_pending_" + (advance ? "native_advance" : "explicit_resume"), () => {
                    // WC-PENDING-01: this policy truthfully authors condition events. It is NOT
                    // the connected work-control profile or evidence of host reachability.
                    var initial = TestOnlySharedWorldPolicy.WithMining(new SharedMiningFixture()).Initial();
                    uint seed = MiningSeedFor(TaskDegree.Success, MiningModifier(initial));
                    var conditions = new ConditionCombatFixture(new[] {
                        CCApply("work-pending-stun", "Stunned", MiningWorker),
                        CCGrant("work-pending-ward", MiningWorker, new ConditionStamp(new RuleTime(1800)), "Stunned"),
                        new ConditionFixtureEvent(MiningWorker, ConditionOperation.Cure("event.work-pending-cure",
                            new ConditionStamp(new RuleTime(1801)), "Stunned"))
                    });
                    var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed), conditions: conditions)
                        .EnableMining(new SharedMiningFixture());
                    var sim = World(policy); var host = TestOnlySharedWorldPolicy.Host();
                    CCDispatch(sim, "work-pending-stun", MiningWorker);
                    CCDispatch(sim, "work-pending-ward", MiningWorker);
                    MiningCommit(sim, MiningCommand(sim, CommandKind.StartMining, SharedMiningFixture.DepositId,
                        MiningSelection(SharedMiningFixture.CategoryA)));
                    uint rng = sim.Capture().RandomState;
                    WorldAdvance(sim, 1800);
                    var pending = sim.Capture(); var job = pending.MiningAttempts.Single();
                    Require(job.Status == MiningAttemptStatus.AwaitingCheck && job.WorkDone == new RuleTime(1800)
                        && pending.RandomState == rng && !job.ResolvedAt.HasValue
                        && pending.MiningUnits.Single(x => x.Id == SharedMiningFixture.UnitA).ReceivedLotId == "",
                        "Due immunity expiry did not retain fully worked mining without drawing or producing output.");
                    var before = Bytes(sim); var denied = MiningCommand(sim, CommandKind.ResumeMining, job.Id);
                    Require(!sim.QueryCommand(host, denied).Admissible
                        && sim.QueryCommand(host, denied).Code == "MiningWorkerIncapable"
                        && sim.Execute(host, denied).Code == "MiningWorkerIncapable"
                        && before.SequenceEqual(Bytes(sim)), "Ineligible pending mining query/execute changed state.");
                    string path = Path.Combine(directory, "model-mining-pending-" + advance + ".ddsave");
                    var store = new FileSaveStore(); store.Save(path, sim.Capture());
                    var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                    foreach(var run in new[] { sim, restored }) {
                        WorldAdvance(run, 1);
                        Require(run.Capture().RandomState == rng
                            && run.Capture().MiningAttempts.Single().Status == MiningAttemptStatus.AwaitingCheck,
                            "Native advancement resolved while the worker remained incapable.");
                        CCDispatch(run, "work-pending-cure", MiningWorker);
                        Require(run.Capture().RandomState == rng
                            && run.Capture().MiningAttempts.Single().Status == MiningAttemptStatus.AwaitingCheck,
                            "Cure alone resolved the pending extraction.");
                        before = Bytes(run);
                        var resume = MiningCommand(run, CommandKind.ResumeMining, job.Id);
                        Require(run.QueryCommand(host, resume).Admissible && before.SequenceEqual(Bytes(run)),
                            "Eligible pending query changed state or was rejected.");
                        var resolve = advance ? IC(run, CommandKind.AdvanceClock, x: 1, y: 2) : resume;
                        MiningCommit(run, resolve);
                        var final = run.Capture(); var completed = final.MiningAttempts.Single();
                        var draw = PlaytestDice.RollD20(rng);
                        Require(completed.Status == MiningAttemptStatus.Success && completed.WorkDone == new RuleTime(1800)
                            && completed.RandomBefore == rng && completed.RandomAfter == draw.NextRandomState
                            && completed.Natural == draw.Natural && final.RandomState == draw.NextRandomState
                            && final.MiningUnits.Single(x => x.Id == SharedMiningFixture.UnitA).Status == MiningUnitStatus.Extracted
                            && final.Work.Reservations.Where(x => x.JobId == job.Id).All(x => x.Status != ReservationStatus.Reserved),
                            "Pending extraction did not settle exactly one native check without extra labor.");
                        before = Bytes(run);
                        Require(run.Execute(host, resolve).Outcome == Outcome.Duplicate && before.SequenceEqual(Bytes(run)),
                            "Repeated pending resolution mutated state.");
                    }
                    Require(Bytes(sim).SequenceEqual(Bytes(restored)), "Pending mining changed across strict save/restore replay.");
                    store.Save(path + ".complete", sim.Capture());
                    File.WriteAllText(path + ".scope.txt", "MODEL_ONLY own declared condition fixture; no connected-profile host reachability claim.\n");
                });
            }
            cases.Add("mgt02_work_control_existing_haven_transaction_query_grant", () => {
                var session = NewWorkControlExpedition();
                foreach(var command in QualityWalkthrough().Take(26))CommitVialRoute(session, command);
                Require(session.View(ExpeditionSeat.Player).Revision == 26, "Transaction regression did not reach its genuine prefix.");
                var commandToSell = new Command("work-control.haven-query", ConnectedExpeditionSession.Companion, 26,
                    CommandKind.StartHavenSale, TestOnlyHavenSaleProfile.OfferVersionId);
                string path = Path.Combine(directory, "haven-query-before.ddsave"); session.Save(path);
                var before = File.ReadAllBytes(path);
                Require(session.QueryCommand(ExpeditionSeat.Player, commandToSell).Admissible
                    && session.DiscoverCommands(ExpeditionSeat.Player, ConnectedExpeditionSession.Companion)
                        .Any(x => x.Command.Kind == CommandKind.StartHavenSale && x.Query.Admissible),
                    "Query/discovery omitted the narrowly selected transaction grant used by submission.");
                session.Save(path + ".after-reads");
                Require(before.SequenceEqual(File.ReadAllBytes(path + ".after-reads")), "Transaction queries mutated the campaign.");
                Require(session.Submit(ExpeditionSeat.Player, commandToSell).Response == ExpeditionResponse.Committed,
                    "Admitted existing sale failed submission.");
                session.SetSeatEnabled(ExpeditionSeat.Player, false);
                Require(session.QueryCommand(ExpeditionSeat.Player, commandToSell).Code == "NotAuthorized"
                    && session.Submit(ExpeditionSeat.Player, commandToSell).Response == ExpeditionResponse.NotAuthorized,
                    "Transaction selection bypassed revoked seat authority.");
            });
            cases.Add("mgt02_work_control_native_fill_record_and_booking_caps", () => {
                var session = NewWorkControlExpedition(); var store = new FileSaveStore(); var codec = new SnapshotCodec();
                string path = Path.Combine(directory, "fill-record-cap.ddsave"), actor = ConnectedExpeditionSession.Companion;
                Snapshot Capture() { session.Save(path); return store.Load(path); }
                void Commit(Command command) {
                    var query = session.QueryCommand(ExpeditionSeat.Player, command);
                    Require(query.Admissible, "Capacity witness query failed: " + command.Kind + "/" + query.Code);
                    Require(session.Submit(ExpeditionSeat.Player, command).Response == ExpeditionResponse.Committed,
                        "Capacity witness submission disagreed: " + command.Kind);
                }
                void Clock(int n, int d) {
                    var s = Capture(); Require(session.SubmitSessionCommand(new Command("cap-clock." + s.Revision,
                        ConnectedExpeditionSession.Hero, s.Revision, CommandKind.AdvanceClock, x: n, y: d)).Response == ExpeditionResponse.Committed,
                        "Capacity witness clock failed.");
                }
                Command Start(Snapshot s) => new Command("cap-start." + s.Revision, actor, s.Revision, CommandKind.StartWaterFill,
                    TestOnlyFillingPolicy.SupplyId, inventory: new InventoryRequest(new RuleQuantity(1, 2), TestOnlyFillingPolicy.CompanionSkinId));
                for(int i = 0; i < 32; i++) {
                    Commit(Start(Capture())); var s = Capture();
                    Commit(new Command("cap-cancel." + i, actor, s.Revision, CommandKind.CancelWaterFill, s.WaterFills.Single(x => x.Pending).Id));
                    Clock(6, 1);
                }
                var full = Capture(); var bytes = codec.Encode(full); var denied = Start(full);
                Require(full.WaterFills.Length == 32 && full.Work.Reservations.Count == 32 && full.Work.WorkerIntervals.Count == 0
                    && session.QueryCommand(ExpeditionSeat.Player, denied).Code == "FillRecordCapacityReached"
                    && session.Submit(ExpeditionSeat.Player, denied).Response == ExpeditionResponse.Unavailable
                    && bytes.SequenceEqual(codec.Encode(Capture())), "Record33 was advertised/admitted or history was evicted.");

                session = NewWorkControlExpedition(); path = Path.Combine(directory, "fill-booking-cap.ddsave");
                Commit(Start(Capture())); string job = Capture().WaterFills.Single().Id;
                for(int i = 0; i < Snapshot.MaxCropWorkRecords; i++) {
                    Clock(1, 1000); var s = Capture();
                    Commit(new Command("cap-pause." + i, actor, s.Revision, CommandKind.PauseWaterFill, job));
                    if(i + 1 < Snapshot.MaxCropWorkRecords)
                        Commit(new Command("cap-resume." + i, actor, Capture().Revision, CommandKind.ResumeWaterFill, job));
                }
                full = Capture(); bytes = codec.Encode(full);
                denied = new Command("cap-resume-overflow", actor, full.Revision, CommandKind.ResumeWaterFill, job);
                Require(full.Work.WorkerIntervals.Count == 128 && full.WaterFills.Single().Progress == new RuleTime(16, 125)
                    && session.QueryCommand(ExpeditionSeat.Player, denied).Code == "WorkBookingCapacityReached"
                    && session.Submit(ExpeditionSeat.Player, denied).Response == ExpeditionResponse.Unavailable
                    && bytes.SequenceEqual(codec.Encode(Capture())), "Booking129 was advertised/admitted or retained labor changed.");
            });
            cases.Add("mgt02_work_control_reservation_cap_mechanical_assessment", () => {
                // Explicit model-level boundary arrangement, NOT a causally reachable host save or
                // gameplay witness. Keep the genuine genesis fingerprint; never import this clone.
                var session = NewWorkControlExpedition(); var store = new FileSaveStore();
                string path = Path.Combine(directory, "reservation-cap-genuine-genesis.ddsave"); session.Save(path);
                var state = store.Load(path); var source = state.Work.Lots.Single(x => x.Id == TestOnlyFillingPolicy.SupplyId);
                var claims = Enumerable.Range(0, 128).Select(i => new ResourceReservation("mechanical-cap.claim." + i,
                    "mechanical-cap.job." + i, source.Id, new RuleQuantity(1), released: new RuleQuantity(1))).ToArray();
                state.Work = new WorkLedger(state.Work.Lots, state.Work.WorkerIntervals, claims);
                var ledger = state.Work; var fills = state.WaterFills; var rng = state.RandomState;
                var command = new Command("mechanical-cap.start", ConnectedExpeditionSession.Companion, state.Revision,
                    CommandKind.StartWaterFill, source.Id, inventory: new InventoryRequest(new RuleQuantity(1, 2), TestOnlyFillingPolicy.CompanionSkinId));
                Require(new TestOnlyFillingPolicy().Resolve(state, command) == "WorkReservationCapacityReached"
                    && ReferenceEquals(ledger, state.Work) && ReferenceEquals(fills, state.WaterFills) && state.RandomState == rng,
                    "Shared pure family admission failed the effective128 reservation boundary.");
                File.WriteAllText(Path.Combine(directory, "reservation-cap-scope.txt"),
                    "PASS: mechanical model assessment only.128 released claims arranged on a detached genuine-genesis clone; not restored or submitted as host history. No genuine campaign reachability claim.\n");
            });
            cases.Add("mgt02_work_control_fresh_identity_strict_restore_and_legacy_boundary", () => {
                var session = NewWorkControlExpedition();
                var original = NewOrdinaryMagicExpedition();
                var store = new FileSaveStore(); var codec = new SnapshotCodec();
                string freshPath = Path.Combine(directory, "work-control-genesis.ddsave");
                string oldPath = Path.Combine(directory, "ordinary116-genesis.ddsave");
                session.Save(freshPath); original.Save(oldPath);
                var fresh = store.Load(freshPath); var old = store.Load(oldPath);
                Require(fresh.WireSchemaVersion == 116 && old.WireSchemaVersion == 116
                    && fresh.ContentFingerprint.Length == 90 && fresh.ContentFingerprint != old.ContentFingerprint
                    && fresh.OrdinaryMagic.PredecessorFingerprint == old.OrdinaryMagic.PredecessorFingerprint,
                    "Work control changed its wire or deeper source declaration.");
                var normalized = fresh.Copy(); normalized.ContentFingerprint = old.ContentFingerprint;
                Require(codec.Encode(normalized).SequenceEqual(codec.Encode(old)),
                    "Opt-in host selection invented authoritative genesis work, resources or calendar events.");

                void RejectRestore(ConnectedExpeditionSession target, string path, string beforePath)
                {
                    target.Save(beforePath); var before = File.ReadAllBytes(beforePath);
                    bool rejected = false;
                    try { target.Restore(path); }
                    catch (Exception e) when (e is ArgumentException || e is InvalidDataException) { rejected = true; }
                    target.Save(beforePath + ".after");
                    Require(rejected && before.SequenceEqual(File.ReadAllBytes(beforePath + ".after")),
                        "Mixed-profile restore adopted a predecessor or changed the live session.");
                }
                RejectRestore(session, oldPath, Path.Combine(directory, "new-before-rejected-old.ddsave"));
                RejectRestore(original, freshPath, Path.Combine(directory, "old-before-rejected-new.ddsave"));

                Require(session.Submit(ExpeditionSeat.Player, new Command("work-control.first-step",
                    ConnectedExpeditionSession.Hero, 0, CommandKind.BeginWorldStep, "walk", 1, 0)).Response == ExpeditionResponse.Committed,
                    "Fresh host could not start its ordinary connected traversal.");
                string activePath = Path.Combine(directory, "work-control-active-traversal.ddsave");
                session.Save(activePath); var restored = NewWorkControlExpedition(); restored.Restore(activePath);
                var advance = new Command("work-control.first-clock", ConnectedExpeditionSession.Hero, 1,
                    CommandKind.AdvanceClock, x: 1, y: 1);
                foreach (var run in new[] { session, restored })
                    Require(run.SubmitSessionCommand(advance).Response == ExpeditionResponse.Committed,
                        "Genuine restored host failed the same continuation.");
                string left = Path.Combine(directory, "work-control-continued.ddsave"), right = Path.Combine(directory, "work-control-restored-continued.ddsave");
                session.Save(left); restored.Save(right);
                Require(File.ReadAllBytes(left).SequenceEqual(File.ReadAllBytes(right)),
                    "Opt-in work identity changed deterministic restored continuation.");
            });
            cases.Add("mgt02_work_control_fractional_fill_pause_resume_completion_and_retry", () => {
                var session = NewWorkControlExpedition(); var store = new FileSaveStore(); var codec = new SnapshotCodec();
                string path = Path.Combine(directory, "fractional-fill.ddsave");
                Snapshot Capture() { session.Save(path); return store.Load(path); }
                void Commit(Command command)
                {
                    AssertNativeInitialAssessmentV1(CastingSimulation(session),command,HavenSaleHost());
                    var before = codec.Encode(Capture());
                    var query = session.QueryCommand(ExpeditionSeat.Player, command);
                    Require(query.Supported && query.Admissible && before.SequenceEqual(codec.Encode(Capture())),
                        "Fill query denied a lawful command or mutated authoritative state: " + command.Kind + "/" + command.Id + "/" + query.Code);
                    Require(session.Submit(ExpeditionSeat.Player, command).Response == ExpeditionResponse.Committed,
                        "Fill execution disagreed with the admitted query.");
                }
                void Advance(int numerator, int denominator)
                {
                    var state = Capture();
                    Require(session.SubmitSessionCommand(new Command("fill-clock." + state.Revision,
                        ConnectedExpeditionSession.Hero, state.Revision, CommandKind.AdvanceClock,
                        x: numerator, y: denominator)).Response == ExpeditionResponse.Committed, "Fill clock failed.");
                }
                var initial = Capture(); uint rng = initial.RandomState;
                var contaminated = new Command("fill-contaminated", ConnectedExpeditionSession.Companion, 0, CommandKind.StartWaterFill,
                    TestOnlyFillingPolicy.SupplyId, inventory: new InventoryRequest(new RuleQuantity(1, 2), TestOnlyFillingPolicy.FlaskId));
                Require(session.QueryCommand(ExpeditionSeat.Player, contaminated).Code == "ContaminationPropagationUnsupported"
                    && session.Submit(ExpeditionSeat.Player, contaminated).Response == ExpeditionResponse.Unavailable
                    && codec.Encode(initial).SequenceEqual(codec.Encode(Capture())),
                    "The authored contaminated flask was treated as an ordinary clean fill target.");
                var start = new Command("fill-start", ConnectedExpeditionSession.Companion, 0, CommandKind.StartWaterFill,
                    TestOnlyFillingPolicy.SupplyId, inventory: new InventoryRequest(new RuleQuantity(1, 2), TestOnlyFillingPolicy.CompanionSkinId));
                Require(!session.QueryCommand(ExpeditionSeat.FirstOpponent, start).Admissible,
                    "Opponent acquired authority over the player's water.");
                Commit(start); Advance(1, 2);
                var working = Capture(); var job = working.WaterFills.Single();
                var workView = session.ObserveWork(ExpeditionSeat.Player, job.WorkerId).Jobs.Single();
                Require(workView.Labor == new RuleTime(1, 2) && workView.Retained == workView.Labor
                    && workView.Remaining == new RuleTime(119, 2) && workView.OpeningInUse
                    && workView.Bookings.Single().IncludesFutureTime && workView.Bookings.Single().End == new RuleTime(60)
                    && workView.Claims.Single().Remaining == new RuleQuantity(1, 2)
                    && workView.ReservedCapacityPints == new RuleQuantity(1, 2)
                    && workView.Controls.Select(x => x.Command.Kind).SequenceEqual(new[] { CommandKind.PauseWaterFill, CommandKind.CancelWaterFill }),
                    "Work observation confused productive labor, future booking or quantity/capacity claims.");
                Require(job.Progress == new RuleTime(1, 2) && job.Status == WaterFillStatus.Working,
                    "A fractional fill changed the fixed60-second work rate.");
                Commit(new Command("fill-pause", job.WorkerId, working.Revision, CommandKind.PauseWaterFill, job.Id));
                Advance(1, 1);
                var paused = Capture();
                var pausedView = session.ObserveWork(ExpeditionSeat.Player, job.WorkerId).Jobs.Single();
                Require(pausedView.Labor == new RuleTime(1, 2) && !pausedView.OpeningInUse
                    && pausedView.Bookings.All(x => !x.IncludesFutureTime) && pausedView.ReservedCapacityPints == new RuleQuantity(1, 2)
                    && workView.OpeningInUse && workView.Bookings.Single().IncludesFutureTime,
                    "Paused views lost retained claims or mutated an already-returned observation.");
                Require(paused.WaterFills.Single().Progress == new RuleTime(1, 2)
                    && paused.Work.AvailableAmount(TestOnlyFillingPolicy.SupplyId) == new RuleQuantity(63, 2),
                    "Paused filling lost its progress or reserved source quantity.");
                var early = new Command("fill-resume-too-early", job.WorkerId, paused.Revision, CommandKind.ResumeWaterFill, job.Id);
                Require(session.QueryCommand(ExpeditionSeat.Player, early).Code == "OffCalendarActionAlreadySpent"
                    && session.Submit(ExpeditionSeat.Player, early).Response == ExpeditionResponse.Unavailable
                    && codec.Encode(paused).SequenceEqual(codec.Encode(Capture())),
                    "A delayed same-interval resume invented another off-calendar work allowance.");
                Advance(9, 2); // Reach the next existing six-second activity interval at t=6.
                var resume = new Command("fill-resume", job.WorkerId, Capture().Revision, CommandKind.ResumeWaterFill, job.Id);
                Commit(resume); Advance(119, 2);
                var completed = Capture(); var filled = completed.WaterFills.Single();
                Require(filled.Status == WaterFillStatus.Complete && filled.Progress == new RuleTime(60)
                    && completed.RuleClock == new RuleTime(131, 2) && completed.RandomState == rng
                    && completed.Work.Lots.Single(x => x.Id == filled.OutputLotId).Amount == new RuleQuantity(1, 2)
                    && completed.Work.Lots.Single(x => x.Id == TestOnlyFillingPolicy.SupplyId).Amount == new RuleQuantity(63, 2),
                    "Fill completion lost exact time, quantity or RNG conservation.");
                var bytes = codec.Encode(completed);
                Require(session.ObserveWork(ExpeditionSeat.Player, job.WorkerId).Jobs.Single().Controls.Count == 0
                    && session.ObserveWork(ExpeditionSeat.Player, job.WorkerId).Jobs.Single().ReservedCapacityPints == default(RuleQuantity)
                    && session.QueryCommand(ExpeditionSeat.Player, resume).Code == "AlreadyCommitted",
                    "Completed work exposed an active continuation or lost receipt classification.");
                Require(session.Submit(ExpeditionSeat.Player, resume).Response == ExpeditionResponse.Duplicate
                    && bytes.SequenceEqual(codec.Encode(Capture())), "Completed-job receipt retry repeated fill effects.");
            });
            cases.Add("mgt02_work_control_reads_discovery_and_revoked_authority", () => {
                var session = NewWorkControlExpedition(); var codec = new SnapshotCodec(); var store = new FileSaveStore();
                string path = Path.Combine(directory, "work-read-purity.ddsave");
                Snapshot Capture() { session.Save(path); return store.Load(path); }
                var before = Capture(); var bytes = codec.Encode(before);
                string actor = ConnectedExpeditionSession.Companion;
                var observation = session.ObserveWork(ExpeditionSeat.Player, actor);
                var pair = observation.Filling.Single(x => x.SourceId == TestOnlyFillingPolicy.SupplyId && x.DestinationId == TestOnlyFillingPolicy.CompanionSkinId);
                Require(pair.StockCapacityBound == new RuleQuantity(4) && pair.RequiredActiveTime == new RuleTime(60)
                    && pair.ExampleAmounts.SequenceEqual(new[] { new RuleQuantity(1, 2), new RuleQuantity(1), new RuleQuantity(4) }),
                    "Filling descriptor lost exact non-exhaustive quantities or fixed duration.");
                var first = session.DiscoverCommands(ExpeditionSeat.Player, actor);
                var second = session.DiscoverCastingCommands(ExpeditionSeat.Player, actor);
                Require(first.Select(x => x.Command.Id).SequenceEqual(second.Select(x => x.Command.Id))
                    && first.Select(x => x.Command.Id).Distinct().Count() == first.Count, "Discovery aliases changed stable option identities.");
                foreach(var option in first) {
                    var query = session.QueryCommand(ExpeditionSeat.Player, option.Command);
                    Require(query.Code == option.Query.Code && query.Admissible == option.Query.Admissible,
                        "Discovery/query disagreement for " + option.Command.Kind);
                }
                var fill = first.Single(x => x.Command.Kind == CommandKind.StartWaterFill && x.Command.Target == pair.SourceId
                    && x.Command.Inventory.Destination == pair.DestinationId && x.Command.Inventory.Amount == new RuleQuantity(1, 2));
                Require(fill.Query.Admissible && bytes.SequenceEqual(codec.Encode(Capture())), "Read/discovery altered state or failed lawful filling.");
                Require(!session.ObserveWork(ExpeditionSeat.FirstOpponent, actor).Enabled
                    && session.ObserveWork(ExpeditionSeat.FirstOpponent, actor).Filling.Count == 0
                    && session.DiscoverCommands(ExpeditionSeat.FirstOpponent, actor).Count == 0,
                    "A foreign seat received worker or inventory details.");
                Require(session.Submit(ExpeditionSeat.Player, fill.Command).Response == ExpeditionResponse.Committed, "Discovered fill failed submission.");
                session.SetSeatEnabled(ExpeditionSeat.Player, false);
                Require(session.QueryCommand(ExpeditionSeat.Player, fill.Command).Code == "NotAuthorized"
                    && session.Submit(ExpeditionSeat.Player, fill.Command).Response == ExpeditionResponse.NotAuthorized
                    && !session.ObserveWork(ExpeditionSeat.Player, actor).Enabled
                    && session.DiscoverCommands(ExpeditionSeat.Player, actor).Count == 0,
                    "Revoked authority was bypassed by a receipt or observation.");
                session.SetSeatEnabled(ExpeditionSeat.Player, true);
                Require(session.QueryCommand(ExpeditionSeat.Player, fill.Command).Code == "AlreadyCommitted",
                    "Reenabled authority could not inspect its exact committed receipt.");
            });
            cases.Add("mgt02_work_control_fill_retry_after_source_leaves_range", () => {
                var session = NewWorkControlExpedition(); var store = new FileSaveStore(); var codec = new SnapshotCodec();
                string path = Path.Combine(directory, "fill-retry-out-of-range.ddsave"), actor = ConnectedExpeditionSession.Companion;
                Snapshot Capture() { session.Save(path); return store.Load(path); }
                void Commit(Command command) { Require(session.Submit(ExpeditionSeat.Player, command).Response == ExpeditionResponse.Committed,
                    "Retry setup command failed: " + command.Kind); }
                void Clock(int seconds) { var s = Capture(); Require(session.SubmitSessionCommand(new Command("retry-clock." + s.Revision,
                    ConnectedExpeditionSession.Hero, s.Revision, CommandKind.AdvanceClock, x: seconds, y: 1)).Response == ExpeditionResponse.Committed,
                    "Retry setup clock failed."); }
                var start = new Command("retry-original-fill", actor, 0, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId,
                    inventory: new InventoryRequest(new RuleQuantity(1, 2), TestOnlyFillingPolicy.CompanionSkinId));
                Commit(start); var begun = Capture();
                Commit(new Command("retry-cancel", actor, begun.Revision, CommandKind.CancelWaterFill, begun.WaterFills.Single().Id));
                Clock(6);
                for(int i = 0; i < 2; i++) {
                    var s = Capture(); Commit(new Command("retry-walk." + i, actor, s.Revision, CommandKind.BeginWorldStep, "walk", 1, 0)); Clock(3);
                }
                var final = Capture(); var bytes = codec.Encode(final);
                Require(!session.ObserveWork(ExpeditionSeat.Player, actor).Filling.Any(x => x.SourceId == start.Target),
                    "Retry witness did not actually leave source range.");
                Require(session.QueryCommand(ExpeditionSeat.Player, start).Code == "AlreadyCommitted"
                    && session.QueryCastingCommand(ExpeditionSeat.Player, start).Code == "AlreadyCommitted"
                    && session.Submit(ExpeditionSeat.Player, start).Response == ExpeditionResponse.Duplicate,
                    "Lost sight/range changed the classification of an exact authorized retry.");
                var conflict = new Command(start.Id, actor, start.ExpectedRevision, start.Kind, start.Target,
                    inventory: new InventoryRequest(new RuleQuantity(3, 4), TestOnlyFillingPolicy.CompanionSkinId));
                Require(session.QueryCommand(ExpeditionSeat.Player, conflict).Code == "CommandIdConflict"
                    && session.Submit(ExpeditionSeat.Player, conflict).Response == ExpeditionResponse.CommandIdConflict,
                    "Lost range concealed a conflicting committed command ID.");
                var fresh = new Command("retry-fresh-unseen", actor, final.Revision, start.Kind, start.Target, inventory: start.Inventory);
                Require(!session.QueryCommand(ExpeditionSeat.Player, fresh).Supported
                    && session.Submit(ExpeditionSeat.Player, fresh).Response == ExpeditionResponse.Unavailable
                    && bytes.SequenceEqual(codec.Encode(Capture())), "Fresh unseen work bypassed visibility or retry reads changed state.");
            });
        }
    }
}
#endif
