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
        private static ConnectedExpeditionSession ShortRestArrival()
        {
            var session = StartVialScenario(ConnectedExpeditionSession.StartWithShortRest());
            const string hero = ConnectedExpeditionSession.Hero, ally = ConnectedExpeditionSession.Companion;
            const ExpeditionSeat player = ExpeditionSeat.Player;
            void Commit(string id, string actor, CommandKind kind, string target = "", int x = 0, int y = 0,
                InventoryRequest inventory = null, CombatRequest combat = null)
                => CommitVialRoute(session, new Command(id, actor, session.View(player).Revision, kind, target, x, y, inventory, combat));
            void Guard(string actor) => Commit("rest.guard." + session.View(player).Revision, actor, CommandKind.SelectCombatStance,
                combat: new CombatRequest(session.View(player).TurnId, stance: 1));
            void End(string actor) => Commit("rest.end." + session.View(player).Revision, actor, CommandKind.EndRegularTurn, session.View(player).TurnId);
            void Step(int y) => Commit("rest.step." + session.View(player).Revision, hero, CommandKind.TacticalStep, session.View(player).TurnId, y: y);
            void Defender()
            {
                int count = 0;
                while (session.View(player).NextSeat == ExpeditionTurnSeat.AutomaticDefender)
                    Require(count++ < 12 && session.AdvanceAutomaticDefender().Response == ExpeditionResponse.Committed, "Actual defender turn did not resolve.");
            }
            void NextRound() { End(hero); Defender(); Guard(ally); End(ally); }
            VialWalk(session, "vial.approach", 108, 1);
            CommitVialRoute(session, VialPickup("vial.pickup", 110));
            Commit("vial.stow", hero, CommandKind.HandlePortableEquipment, VialId,
                inventory: new InventoryRequest(Q(1), ConnectedVialRules.PackId, HandlingKind.Stow));
            VialWalk(session, "tac.away", 112, -1);
            Commit("ally.stage", ally, CommandKind.BeginWorldStep, "walk", -1);
            Commit("ally.stage-paid", hero, CommandKind.AdvanceClock, x: 6, y: 1);
            VialWalk(session, "ally.entry", 116, -1, 12);
            Commit("ally.reinforcement", ally, CommandKind.BeginReinforcementApproach, "TEST_ONLY.companion-reinforcement.v1");
            Commit("ally.retrieve", hero, CommandKind.HandlePortableEquipment, VialId, inventory: new InventoryRequest(Q(1), handling: HandlingKind.Retrieve));
            Guard(hero); Step(2); Defender(); End(hero); Defender();
            Guard(ally); End(ally); Guard(hero); Step(1); Defender(); End(hero); Defender();
            Guard(ally); End(ally); Guard(hero); Step(2); NextRound();
            foreach (int turn in new[] { 9, 12, 15, 18, 21 }) {
                Guard(hero);
                Commit("rest.attack." + turn, hero, CommandKind.AttackClub, "TEST_ONLY.later-defender",
                    combat: new CombatRequest(session.View(player).TurnId, "TEST_ONLY.actor-club"));
                NextRound();
            }
            for (int rounds = 0; ; rounds++) {
                Guard(hero);
                var before = ShortRestCapture(session);
                var enemy = before.Lives.Single(x => x.ActorId == "TEST_ONLY.later-defender");
                Require(rounds < 12, "Later defender must resolve through actual combat.");
                if (enemy.Dead && rounds > 0) {
                    Commit("rest.decay", hero, CommandKind.ConsumeDecay, ConsumeDecaySite.Id);
                    break;
                }
                if (!enemy.Dead) Commit("rest.finish." + before.Revision, hero, CommandKind.AttackClub, enemy.ActorId,
                    combat: new CombatRequest(session.View(player).TurnId, "TEST_ONLY.actor-club"));
                NextRound();
            }
            NextRound(); Guard(hero);
            Commit("rest.heal", hero, CommandKind.UseAlchemyDose, VialId, inventory: new InventoryRequest(Q(1), hero));
            Commit("rest.close", hero, CommandKind.EndFixedEncounter, session.View(player).TurnId);
            Commit("rest.arrive", hero, CommandKind.BeginWorldStep, "walk", y: -1);
            Commit("rest.arrival-paid", hero, CommandKind.AdvanceClock, x: 6, y: 1);
            return session;
        }

        private static Snapshot ShortRestCapture(ConnectedExpeditionSession session)
            => ((Simulation)typeof(ConnectedExpeditionSession).GetField("simulation", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(session)).Capture();

        private static void AddConnectedShortRestCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("mgt03_connected_short_rest_deadlines_cadence_interruption_and_restore", () =>
            {
                const string hero = ShortRestBerth.Actor;
                const ExpeditionSeat player = ExpeditionSeat.Player;
                var session = ShortRestArrival();
                var codec = new SnapshotCodec();
                var store = new FileSaveStore();
                var policy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession)
                    .GetField("policy", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(session);
                Snapshot Capture() => ShortRestCapture(session);
                string FileAt(string label) => Path.Combine(directory, "short-rest-" + label + ".ddsave");
                Snapshot Save(string label) { session.Save(FileAt(label)); return store.Load(FileAt(label)); }
                Command Begin(string id) => new Command(id, hero, session.View(player).Revision, CommandKind.BeginShortRest, ShortRestBerth.Id);
                void Commit(Command command) => CommitVialRoute(session, command);
                void Advance(string id, int seconds) => Commit(new Command(id, hero, session.View(player).Revision, CommandKind.AdvanceClock, x: seconds, y: 1));
                void Deny(Command command, ExpeditionResponse response = ExpeditionResponse.Unavailable, ExpeditionSeat seat = player)
                {
                    var before = codec.Encode(Capture());
                    Require(session.Submit(seat, command).Response == response && before.SequenceEqual(codec.Encode(Capture())),
                        "Rest denial or retry changed state: " + command.Id);
                }
                ActorLifeRecord Hero(Snapshot state) => state.Lives.Single(x => x.ActorId == hero);

                var arrival = Save("arrival");
                Require(arrival.WireSchemaVersion == 103 && arrival.SchemaVersion == 90 && arrival.RuleClock == new RuleTime(113481, 2)
                    && !arrival.InventoryCombat && arrival.Encounter == null && Hero(arrival).Hp == 26 && Hero(arrival).TemporaryHp == 3
                    && arrival.ConsumeDecay.Deadline == new RuleTime(120653, 2), "Rest must follow the actual accepted late route.");
                Require(arrival.Characters.Single(x => x.ActorId == hero).Levels.All(x => x.ClassName == "Warrior")
                    && arrival.Characters.Single(x => x.ActorId == hero).Levels.Count == 3
                    && !arrival.CharacterFeatureGrants.Any(x => x.ActorId == hero)
                    && !arrival.CharacterFeatureRuntime.Any(x => x.ActorId == hero)
                    && session.View(player).ShortRest.WarriorStrain == 0 && session.View(player).ShortRest.BenefitsRemaining == 2,
                    "The selected actual profile has Warrior levels, zero initial Warrior Strain, and no owned feature refreshes.");
                var old = ConnectedExpeditionSession.StartWithConsumeDecay();
                Throws<ArgumentException>(() => old.Restore(FileAt("arrival")));
                Require(old.View(player).Revision == 0 && old.View(player).ShortRest == null
                    && session.View(ExpeditionSeat.FirstOpponent).ShortRest == null, "The opt-in rest must preserve old profiles and seat privacy.");
                var begin = Begin("rest.begin");
                Deny(begin, ExpeditionResponse.NotAuthorized, ExpeditionSeat.FirstOpponent);
                Deny(new Command("rest.dice", hero, arrival.Revision, CommandKind.BeginShortRest, ShortRestBerth.Id, 1));
                Deny(new Command("rest.foreign", hero, arrival.Revision, CommandKind.BeginShortRest, WoundTreatmentStation.Location));
                Deny(new Command("rest.actor", ConnectedExpeditionSession.Companion, arrival.Revision, CommandKind.BeginShortRest, ShortRestBerth.Id));
                Deny(new Command("rest.payload", hero, arrival.Revision, CommandKind.BeginShortRest, ShortRestBerth.Id, inventory: new InventoryRequest(Q(1))));
                Deny(new Command("rest.stale", hero, arrival.Revision - 1, CommandKind.BeginShortRest, ShortRestBerth.Id), ExpeditionResponse.StaleRevision);

                // Detached adversarial facts call the same resolver; they grant no public edit authority.
                var occupied = arrival.Copy();
                occupied.Actors.Single(x => x.Id == ConnectedExpeditionSession.Companion).X = 0;
                occupied.Actors.Single(x => x.Id == ConnectedExpeditionSession.Companion).Y = 1;
                Require(policy.Resolve(occupied, begin) == "ShortRestBerthOccupied", "Actual berth occupancy must deny admission.");
                var blocked = arrival.Copy();
                blocked.ObservationCells = blocked.ObservationCells.Append(new ObservationMapCellRecord(0, 1, false, true, false, false)).ToArray();
                Require(policy.Resolve(blocked, begin) == "ShortRestRequiresStationaryBerthAccess", "Site qualification must use actual geometry.");
                var busy = arrival.Copy();
                busy.Work = busy.Work.Reserve("rest.control.work", new[] { new WorkerInterval("rest.control.interval", "rest.control.work", hero,
                    busy.RuleClock.AddSeconds(1), busy.RuleClock.AddSeconds(10)) }, Array.Empty<ResourceReservation>());
                Require(policy.Resolve(busy, begin) == "ShortRestActorOccupied", "Future exclusive work must deny a full-hour interval.");
                var incapacitated = arrival.Copy();
                incapacitated.Conditions = incapacitated.Conditions.Select(x => x.Target == hero
                    ? x.Append(ConditionOperation.Advance("rest.incap-clock", new ConditionStamp(arrival.RuleClock)))
                        .Append(CCApply("rest-incapacitated", "Incapacitated", at: new ConditionStamp(arrival.RuleClock)).Operation) : x).ToArray();
                Require(policy.Resolve(incapacitated, begin) == null && ShortRestBerth.Active(incapacitated) != null,
                    "Incapacitated by itself must not prohibit the approved rest.");

                Commit(begin);
                var pending = Save("pending");
                Require(pending.RandomState == arrival.RandomState && pending.RuleClock == arrival.RuleClock
                    && !WorldActivityValidation.HasActiveLabor(pending, hero, pending.RuleClock, pending.RuleClock.AddSeconds(1))
                    && ShortRestBerth.Active(pending).DueAt == new RuleTime(120681, 2), "Rest occupancy is not productive labor, a roll or an immediate reward.");
                var lostAccess = pending.Copy();
                lostAccess.ObservationCells = lostAccess.ObservationCells.Append(new ObservationMapCellRecord(0, 1, false, true, false, false)).ToArray();
                Require(policy.Resolve(lostAccess, new Command("rest.access-lost", hero, pending.Revision, CommandKind.AdvanceClock, x: 1, y: 1)) == null
                    && lostAccess.ShortRests.Single().Interruption == ShortRestInterruption.AccessLost
                    && lostAccess.ShortRests.Single().EndedAt == pending.RuleClock && !lostAccess.Work.WorkerIntervals.Any(x => x.JobId == pending.ShortRests.Single().Id),
                    "Actual access loss must terminate immediately and free future occupancy.");
                var admittedEncounter = pending.Copy();
                admittedEncounter.InventoryCombat = true;
                admittedEncounter.Encounter = arrival.ClosedEncounters.Last().Encounter;
                typeof(TestOnlySharedWorldPolicy).GetMethod("ReconcileShortRest", BindingFlags.Instance | BindingFlags.NonPublic)
                    .Invoke(policy, new object[] { admittedEncounter, new Command("rest.external-encounter", hero, pending.Revision, CommandKind.BeginFixedEncounter) });
                Require(admittedEncounter.ShortRests.Single().Interruption == ShortRestInterruption.Encounter
                    && admittedEncounter.ShortRests.Single().Benefit == ShortRestBenefit.NotCompleted,
                    "The same post-admission hook must terminate a rest when the hero joins an encounter.");
                var tied = pending.Copy();
                tied.ConsumeDecay = new ConsumeDecayRecord(tied.ConsumeDecay.CommandId, tied.ConsumeDecay.Revision, pending.RuleClock, 3, true);
                Require(policy.Resolve(tied, new Command("rest.tied-clock", hero, pending.Revision, CommandKind.AdvanceClock, x: 3600, y: 1)) == null
                    && tied.ConsumeDecay.End == TemporaryHpEnd.Expired && tied.ConsumeDecay.EndedAt == tied.ShortRests.Single().EndedAt
                    && tied.ShortRests.Single().Outcome == ShortRestOutcome.Completed && Hero(tied).TemporaryHp == 0,
                    "Tied expiry must be resolved on the shared deadline before completion settlement.");
                session.Restore(FileAt("pending"));
                Deny(begin, ExpeditionResponse.Duplicate);
                session.SetSeatEnabled(player, false); Deny(begin, ExpeditionResponse.NotAuthorized); session.SetSeatEnabled(player, true);
                Deny(new Command(begin.Id, hero, begin.ExpectedRevision, begin.Kind, hero), ExpeditionResponse.CommandIdConflict);
                Deny(new Command("rest.move-denied", hero, pending.Revision, CommandKind.BeginWorldStep, "walk", x: 1));
                Deny(new Command("rest.work-denied", hero, pending.Revision, CommandKind.StartWoundTreatment, ConnectedExpeditionSession.Companion));
                Deny(new Command("rest.wrong-interval", hero, pending.Revision, CommandKind.InterruptShortRest, "TEST_ONLY.short-rest.99"));
                Advance("rest.until-before-expiry", 3585);
                var beforeExpiry = Save("before-expiry");
                session.Restore(FileAt("before-expiry"));
                Advance("rest.expiry", 1);
                var expiry = Save("expiry");
                Require(Hero(beforeExpiry).TemporaryHp == 3 && Hero(expiry).TemporaryHp == 0
                    && expiry.RuleClock == new RuleTime(120653, 2) && expiry.ConsumeDecay.End == TemporaryHpEnd.Expired
                    && ShortRestBerth.Active(expiry) != null && ShortRestBerth.BenefitsUsed(expiry) == 0,
                    "The real buffer deadline must precede rest completion by fourteen seconds.");
                Advance("rest.before-end", 13);
                Require(ShortRestBerth.Active(Capture()) != null, "An hour minus one second gives no credit.");
                Save("before-completion");
                Advance("rest.end", 1);
                var completed = Save("completed");
                var rest = completed.ShortRests.Single();
                Require(rest.Outcome == ShortRestOutcome.Completed && rest.Benefit == ShortRestBenefit.Eligible
                    && rest.WarriorStrainReduction == ShortRestBenefit.Eligible && rest.WarriorStrainBefore == 0 && rest.WarriorStrainAfter == 0
                    && rest.HitDiceSpent == 0 && rest.Healing == 0 && rest.RewardRandomWords == 0
                    && rest.EndCommandId == "rest.end" && rest.EndRevision == completed.Revision
                    && Hero(completed).Hp == 26 && Hero(completed).TemporaryHp == 0, "Completed rest must retain its zero-dice eligible outcome.");
                session.Restore(FileAt("pending"));
                Advance("rest.whole", 3600);
                var whole = Save("whole");
                Require(whole.RuleClock == completed.RuleClock && whole.RandomState == completed.RandomState
                    && Hero(whole).Hp == Hero(completed).Hp && Hero(whole).MaximumHp == Hero(completed).MaximumHp
                    && Hero(whole).TemporaryHp == Hero(completed).TemporaryHp && whole.ConsumeDecay.EndedAt == expiry.RuleClock
                    && whole.ShortRests.Single().DueAt == rest.DueAt && whole.ShortRests.Single().Benefit == rest.Benefit
                    && whole.Conditions.Zip(completed.Conditions, (left, right) => left.SameAs(right)).All(x => x),
                    "Equivalent shared-clock partitions must preserve deadlines, conditions, life, reward and RNG.");

                session.Restore(FileAt("pending"));
                Advance("rest.partial", 1200);
                var interrupt = new Command("rest.interrupt", hero, session.View(player).Revision, CommandKind.InterruptShortRest, rest.Id);
                Commit(interrupt);
                var interrupted = Save("interrupted");
                session.Restore(FileAt("interrupted"));
                Deny(interrupt, ExpeditionResponse.Duplicate);
                Require(interrupted.ShortRests.Single().Benefit == ShortRestBenefit.NotCompleted
                    && interrupted.Work.WorkerIntervals.Single(x => x.JobId == rest.Id).End == interrupted.RuleClock,
                    "Interruption keeps elapsed history, cancels future occupancy and earns no completion.");
                Commit(Begin("rest.restart"));
                Save("restart");
                Advance("rest.restart-before", 3599);
                Require(ShortRestBerth.Active(Capture()) != null && ShortRestBerth.BenefitsUsed(Capture()) == 0, "Interrupted time cannot shorten a restart.");
                Advance("rest.restart-end", 1);
                Save("first-benefit");
                Commit(Begin("rest.second")); Advance("rest.second-end", 3600); Save("second-benefit");
                Commit(Begin("rest.third")); Advance("rest.third-end", 3600);
                var third = Save("third-completion");
                Require(third.ShortRests.Count(x => x.Outcome == ShortRestOutcome.Completed) == 3
                    && ShortRestBerth.BenefitsUsed(third) == 2 && third.ShortRests.Last().Benefit == ShortRestBenefit.Ineligible
                    && third.ShortRests.Last().WarriorStrainReduction == ShortRestBenefit.Ineligible
                    && session.View(player).ShortRest.BenefitsRemaining == 0, "The third completed hour is distinct from an eligible floor-zero result.");
                Commit(new Command("rest.continue", hero, third.Revision, CommandKind.BeginWorldStep, "walk", y: -1));
                Deny(Begin("rest.traversing"));
                Advance("rest.continue-paid", 6);
                var continued = Save("continued");
                Require(continued.Actors.Single(x => x.Id == hero).Y == 0 && continued.RuleClock > third.RuleClock, "Paid ordinary movement must continue after rest.");
                Deny(Begin("rest.offsite"));

                var forged = completed.Copy();
                forged.ShortRests = new[] { new ShortRestRecord(rest.Sequence, rest.StartCommandId, rest.StartRevision, rest.StartedAt,
                    ShortRestOutcome.Completed, ShortRestBenefit.Ineligible, endCommandId: rest.EndCommandId, endRevision: rest.EndRevision, endedAt: rest.EndedAt) };
                Throws<ArgumentException>(() => codec.Encode(forged));
                forged = completed.Copy();
                forged.ShortRests = new[] { new ShortRestRecord(rest.Sequence, rest.StartCommandId, rest.StartRevision, rest.StartedAt,
                    rest.Outcome, rest.Benefit, endCommandId: "rest.before-end", endRevision: rest.EndRevision - 1, endedAt: rest.EndedAt) };
                store.Save(FileAt("forged-terminal"), forged);
                Throws<ArgumentException>(() => session.Restore(FileAt("forged-terminal")));
                forged = pending.Copy(); forged.ShortRests = Array.Empty<ShortRestRecord>();
                Throws<ArgumentException>(() => codec.Encode(forged));
                Require(codec.Encode(continued).SequenceEqual(codec.Encode(Capture())), "Forgery rejection must preserve the live continuation.");

                var direct = ConnectedExpeditionSession.StartWithShortRest();
                foreach (var receipt in continued.Receipts) {
                    var command = CommandHistory.Read(receipt);
                    var response = receipt.Principal == "TEST_ONLY.tac10-later-defender.v1" ? direct.AdvanceAutomaticDefender()
                        : command.Kind == CommandKind.AdvanceClock || command.Kind == CommandKind.EndFixedEncounter ? direct.SubmitSessionCommand(command)
                        : direct.Submit(command.Actor == ConnectedExpeditionSession.FirstOpponent ? ExpeditionSeat.FirstOpponent : player, command);
                    Require(response.Response == ExpeditionResponse.Committed, "Direct public replay failed at " + receipt.Revision);
                }
                Require(codec.Encode(continued).SequenceEqual(codec.Encode(ShortRestCapture(direct))), "Restored route and direct public C# replay must agree byte for byte.");
            });
        }
    }
}
#endif
