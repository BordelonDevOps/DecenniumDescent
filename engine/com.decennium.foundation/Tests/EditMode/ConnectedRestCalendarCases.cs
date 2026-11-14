#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddConnectedRestCalendarCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("mgt03_short_rest_retained_calendar_and_live_combat_boundary", () =>
            {
                const string hero = ShortRestBerth.Actor;
                const ExpeditionSeat player = ExpeditionSeat.Player;
                var session = StartVialScenario(ConnectedExpeditionSession.StartWithShortRest());
                var policy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession)
                    .GetField("policy", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(session);
                var codec = new SnapshotCodec();
                Snapshot Capture() => ShortRestCapture(session);
                string FileAt(string name) => Path.Combine(directory, "rest-calendar-" + name + ".ddsave");
                void Commit(string id, CommandKind kind, string target = "", int x = 0, int y = 0, InventoryRequest inventory = null)
                    => CommitVialRoute(session, new Command(id, hero, session.View(player).Revision, kind, target, x, y, inventory));
                void Clock(string id, int seconds) => Commit(id, CommandKind.AdvanceClock, x: seconds, y: 1);
                void Step(string id, int x, int y) { Commit(id, CommandKind.BeginWorldStep, "walk", x, y); Clock(id + ".paid", 6); }
                void Deny(ConnectedExpeditionSession target, Command command, ExpeditionResponse expected = ExpeditionResponse.Unavailable)
                {
                    var before = codec.Encode(ShortRestCapture(target));
                    Require(target.Submit(player, command).Response == expected && before.SequenceEqual(codec.Encode(ShortRestCapture(target))),
                        "Rest/calendar denial or retry changed complete state: " + command.Id);
                }
                VialWalk(session, "vial.approach", 108, 1);
                CommitVialRoute(session, VialPickup("vial.pickup", 110));
                Commit("vial.stow", CommandKind.HandlePortableEquipment, VialId,
                    inventory: new InventoryRequest(Q(1), ConnectedVialRules.PackId, HandlingKind.Stow));
                VialWalk(session, "tac.away", 112, -1);
                Step("calendar.approach.0", 0, -1); Step("calendar.approach.1", 0, -1); Step("calendar.approach.2", -1, 0);
                var arrival = Capture(); session.Save(FileAt("arrival"));
                Require(arrival.Revision == 120 && arrival.RuleClock == new RuleTime(56681) && arrival.Encounter?.Sparse == true
                    && arrival.Encounter.Id == "world.fixed-conflict" && !arrival.InventoryCombat && !session.View(player).InEncounter
                    && arrival.Actors.Single(x => x.Id == hero).X == 0 && arrival.Actors.Single(x => x.Id == hero).Y == 1,
                    "The public paid approach must retain its historical calendar outside combat.");

                var vial = new Command("calendar.ordinary-vial", hero, arrival.Revision, CommandKind.UseAlchemyDose, VialId,
                    inventory: new InventoryRequest(Q(1), hero));
                Require(policy.Resolve(arrival.Copy(), vial) == "AlchemyOwnTacticalTurnRequired", "Calendar presence cannot grant tactical vial use.");
                Deny(session, vial);
                var begin = new Command("calendar.begin", hero, arrival.Revision, CommandKind.BeginShortRest, ShortRestBerth.Id);
                var live = arrival.Copy(); live.InventoryCombat = true;
                Require(policy.Resolve(live, begin) == "ShortRestRequiresOrdinaryExploration", "Live combat at the same berth must deny rest.");
                var firstCombat = ConnectedExpeditionSession.StartWithShortRest();
                foreach (var receipt in arrival.Receipts) {
                    var c = CommandHistory.Read(receipt);
                    var response = c.Kind == CommandKind.AdvanceClock || c.Kind == CommandKind.EndFixedEncounter
                        ? firstCombat.SubmitSessionCommand(c) : firstCombat.Submit(c.Actor == ConnectedExpeditionSession.FirstOpponent
                            ? ExpeditionSeat.FirstOpponent : player, c);
                    Require(response.Response == ExpeditionResponse.Committed, "Public first-combat prefix failed.");
                    if (firstCombat.View(player).InEncounter) break;
                }
                Require(firstCombat.View(player).InEncounter, "Live-combat denial requires actual admitted public combat.");
                Deny(firstCombat, new Command("calendar.live-denial", hero, firstCombat.View(player).Revision, CommandKind.BeginShortRest, ShortRestBerth.Id));

                CommitVialRoute(session, begin);
                session.Save(FileAt("pending")); session.Restore(FileAt("pending"));
                var pending = Capture();
                Deny(session, begin, ExpeditionResponse.Duplicate);
                Clock("calendar.partial", 1);
                var partial = Capture();
                Require(ShortRestBerth.Active(partial) != null && partial.Encounter.Id == arrival.Encounter.Id,
                    "Historical calendar reconciliation must not interrupt the actual pending rest.");
                var interrupted = partial.Copy(); interrupted.InventoryCombat = true;
                typeof(TestOnlySharedWorldPolicy).GetMethod("ReconcileShortRest", BindingFlags.Instance | BindingFlags.NonPublic)
                    .Invoke(policy, new object[] { interrupted, new Command("calendar.external-combat", hero, partial.Revision, CommandKind.BeginFixedEncounter) });
                var ended = interrupted.ShortRests.Single();
                Require(ended.Outcome == ShortRestOutcome.Interrupted && ended.Interruption == ShortRestInterruption.Encounter
                    && ended.Benefit == ShortRestBenefit.NotCompleted && ended.EndedAt == partial.RuleClock
                    && ended.Healing == 0 && ShortRestBerth.BenefitsUsed(interrupted) == 0
                    && interrupted.Work.WorkerIntervals.Single(x => x.JobId == ended.Id).End == partial.RuleClock,
                    "Actual combat admission through shared reconciliation must cut occupancy and award no benefit.");

                Clock("calendar.before-end", 3598);
                Require(ShortRestBerth.Active(Capture()) != null, "A full uninterrupted hour is still required.");
                Clock("calendar.end", 1);
                var split = Capture(); session.Save(FileAt("split"));
                session.Restore(FileAt("pending")); Clock("calendar.whole", 3600);
                var whole = Capture(); session.Save(FileAt("whole"));
                Require(whole.ShortRests.Single().Outcome == ShortRestOutcome.Completed && whole.ShortRests.Single().Benefit == ShortRestBenefit.Eligible
                    && whole.ShortRests.Single().EndedAt == pending.RuleClock.AddSeconds(3600) && whole.RuleClock == split.RuleClock
                    && whole.RandomState == split.RandomState && whole.RandomState == pending.RandomState
                    && whole.Encounter.Id == arrival.Encounter.Id && whole.Encounter.Origin == arrival.Encounter.Origin
                    && whole.Encounter.InitialOrder.SequenceEqual(arrival.Encounter.InitialOrder)
                    && whole.Encounter.TurnOrdinal == split.Encounter.TurnOrdinal
                    && whole.WorldSchedule.ProcessedSlot == split.WorldSchedule.ProcessedSlot
                    && whole.WorldSchedule.ProcessedSlot == arrival.WorldSchedule.ProcessedSlot + 1200
                    && whole.Lives.Select(x => new { x.ActorId, x.Hp, x.MaximumHp, x.TemporaryHp, x.Stable, x.Dead, x.StableUntil })
                        .SequenceEqual(split.Lives.Select(x => new { x.ActorId, x.Hp, x.MaximumHp, x.TemporaryHp, x.Stable, x.Dead, x.StableUntil }))
                    && whole.WorldIntervals.Select(x => new { x.ActorId, x.LastStart, x.MovementSpent, x.ActionSpent, x.DashPaid, x.ReactionAvailable, x.Interactions })
                        .SequenceEqual(split.WorldIntervals.Select(x => new { x.ActorId, x.LastStart, x.MovementSpent, x.ActionSpent, x.DashPaid, x.ReactionAvailable, x.Interactions }))
                    && whole.Conditions.Zip(split.Conditions, (a, b) => a.SameAs(b)).All(x => x),
                    "Split and whole rest must preserve actual calendar progression, budgets, life, due conditions and RNG.");
                Require(whole.Lives.Single(x => x.ActorId == hero).Hp == 26 && whole.ShortRests.Single().Healing == 0
                    && whole.ShortRests.Single().RewardRandomWords == 0 && whole.ShortRests.Single().HitDiceSpent == 0,
                    "Calendar correction must not heal, draw dice or invent rest rewards.");
                Step("calendar.continue", 1, 0);
                session.Save(FileAt("continued"));
                var continued = Capture();
                var replay = ConnectedExpeditionSession.StartWithShortRest();
                foreach (var receipt in continued.Receipts) {
                    var c = CommandHistory.Read(receipt);
                    var response = c.Kind == CommandKind.AdvanceClock || c.Kind == CommandKind.EndFixedEncounter ? replay.SubmitSessionCommand(c)
                        : replay.Submit(c.Actor == ConnectedExpeditionSession.FirstOpponent ? ExpeditionSeat.FirstOpponent : player, c);
                    Require(response.Response == ExpeditionResponse.Committed, "Direct C# calendar/rest replay failed at " + receipt.Revision);
                }
                Require(codec.Encode(continued).SequenceEqual(codec.Encode(ShortRestCapture(replay)))
                    && continued.Actors.Single(x => x.Id == hero).X == 1 && !continued.InventoryCombat,
                    "Pending restore and uninterrupted direct C# replay must agree after paid ordinary continuation.");
            });
        }
    }
}
#endif
