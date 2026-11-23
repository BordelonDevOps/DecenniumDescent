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
                Require(job.Progress == new RuleTime(1, 2) && job.Status == WaterFillStatus.Working,
                    "A fractional fill changed the fixed60-second work rate.");
                Commit(new Command("fill-pause", job.WorkerId, working.Revision, CommandKind.PauseWaterFill, job.Id));
                Advance(1, 1);
                var paused = Capture();
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
                Require(session.Submit(ExpeditionSeat.Player, resume).Response == ExpeditionResponse.Duplicate
                    && bytes.SequenceEqual(codec.Encode(Capture())), "Completed-job receipt retry repeated fill effects.");
            });
        }
    }
}
#endif
