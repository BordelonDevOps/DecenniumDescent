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
        private static void AddConnectedWoundTreatmentCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac06_connected_wound_treatment_ordinary_supply_and_strain", () =>
            {
                const string hero = ConnectedExpeditionSession.Hero;
                const string patient = ConnectedExpeditionSession.Companion;
                const ExpeditionSeat player = ExpeditionSeat.Player;
                var codec = new SnapshotCodec();
                var store = new FileSaveStore();
                var session = StartVialScenario(ConnectedExpeditionSession.StartWithWoundTreatment());
                const BindingFlags hidden = BindingFlags.Instance | BindingFlags.NonPublic;
                var simulation = typeof(ConnectedExpeditionSession).GetField("simulation", hidden);
                Snapshot Capture() => ((Simulation)simulation.GetValue(session)).Capture();
                string PathAt(string mark) => Path.Combine(directory, "wound-treatment-" + mark + ".ddsave");
                Snapshot Save(string mark) { session.Save(PathAt(mark)); return store.Load(PathAt(mark)); }
                ActorLifeRecord Life(Snapshot state) => state.Lives.Single(x => x.ActorId == patient);
                void Commit(string id, string actor, CommandKind kind, string target = "", int x = 0, int y = 0,
                    InventoryRequest inventory = null, CombatRequest combat = null)
                    => CommitVialRoute(session, new Command(id, actor, session.View(player).Revision, kind, target, x, y, inventory, combat));
                void Guard(string actor)
                    => Commit("wound.guard." + session.View(player).Revision, actor, CommandKind.SelectCombatStance,
                        combat: new CombatRequest(session.View(player).TurnId, stance: 1));
                void End(string actor)
                    => Commit("wound.end." + session.View(player).Revision, actor, CommandKind.EndRegularTurn, session.View(player).TurnId);
                void Step(string actor, int x, int y)
                    => Commit("wound.step." + session.View(player).Revision, actor, CommandKind.TacticalStep, session.View(player).TurnId, x, y);
                void Auto()
                {
                    int count = 0;
                    while (session.View(player).NextSeat == ExpeditionTurnSeat.AutomaticDefender)
                        Require(count++ < 12 && session.AdvanceAutomaticDefender().Response == ExpeditionResponse.Committed, "Defender route diverged.");
                }
                Command Treatment(string id, CommandKind kind, string actor = hero, string target = patient)
                    => new Command(id, actor, session.View(player).Revision, kind, target);
                void Clock(string id, int x, int y = 1) => Commit(id, hero, CommandKind.AdvanceClock, x: x, y: y);
                void Deny(Command command, ExpeditionResponse expected = ExpeditionResponse.Unavailable, ExpeditionSeat seat = player)
                {
                    var before = codec.Encode(Capture());
                    Require(session.Submit(seat, command).Response == expected && before.SequenceEqual(codec.Encode(Capture())),
                        "Denial mutated state or returned a different response: " + command.Id);
                }
                void RequireStock(Snapshot state, int basket, bool spent)
                {
                    var stock = WoundTreatmentStation.Stock(basket).ToArray();
                    foreach (var item in stock)
                        Require(state.Work.Lots.Single(x => x.Id == item.Id).Amount == (spent ? default : item.Amount),
                            "Basket stock did not settle exactly once.");
                    var vessels = WoundTreatmentStation.Vessels(basket);
                    Require(vessels.Select(x => x.Id).Distinct().Count() == 3
                        && vessels.Select(x => x.CapacityPints).SequenceEqual(new[] { 4, 4, 1 })
                        && vessels.Select(x => x.GrossPounds(state.Work)).SequenceEqual(spent
                            ? new[] { Q(1), Q(1), new RuleQuantity(1, 4) } : new[] { Q(5), Q(5), Q(1) }),
                        "Treatment must preserve the same vessels and exact tare.");
                }

                VialWalk(session, "vial.approach", 108, 1);
                CommitVialRoute(session, VialPickup("vial.pickup", 110));
                Commit("vial.stow", hero, CommandKind.HandlePortableEquipment, VialId,
                    inventory: new InventoryRequest(Q(1), ConnectedVialRules.PackId, HandlingKind.Stow));
                VialWalk(session, "tac.away", 112, -1);
                Commit("ally.stage", patient, CommandKind.BeginWorldStep, "walk", -1);
                Clock("ally.stage-paid", 6);
                VialWalk(session, "ally.entry", 116, -1, 12);
                Commit("ally.reinforcement", patient, CommandKind.BeginReinforcementApproach, "TEST_ONLY.companion-reinforcement.v1");
                Guard(hero); Step(hero, 0, 2); Auto(); End(hero); Auto(); Guard(patient); End(patient);
                Guard(hero); Step(hero, 0, 1); Auto(); End(hero); Auto(); Guard(patient); End(patient); Guard(hero);
                for (int count = 0; ; count++) {
                    var state = Capture();
                    Require(count < 250 && !Life(state).Dead, "Companion must reach the genuine dying state.");
                    var actor = state.Encounter.CurrentActor;
                    if (Life(state).Hp == 0 && actor == hero) break;
                    if (session.View(player).NextSeat == ExpeditionTurnSeat.AutomaticDefender) { Auto(); continue; }
                    if (state.Lives.Single(x => x.ActorId == actor).Hp > 0 && !state.Stances.Any(x => x.ActorId == actor
                        && x.TurnOrdinal == state.Encounter.TurnOrdinal && EncounterHistory.InCurrent(state, x.Revision))) Guard(actor);
                    if (actor == patient && state.Encounter.TurnOrdinal == 71) { Step(patient, 2, 3); Auto(); }
                    End(actor);
                }
                Guard(hero); Step(hero, 1, 2);
                Deny(Treatment("wound.combat-denial", CommandKind.StartWoundTreatment));
                Commit("wound.stabilize", hero, CommandKind.StabilizeCompanion, patient);
                End(hero); Auto(); End(patient);
                foreach (int turn in new[] { 75, 78, 81 }) {
                    Guard(hero);
                    Require(Capture().Encounter.TurnOrdinal == turn, "Unexpected later encounter turn.");
                    Commit("wound.attack." + turn, hero, CommandKind.AttackClub, "TEST_ONLY.later-defender",
                        combat: new CombatRequest(session.View(player).TurnId, "TEST_ONLY.actor-club"));
                    if (turn < 81) { End(hero); Auto(); End(patient); }
                }
                Commit("wound.exit", hero, CommandKind.EndFixedEncounter, session.View(player).TurnId);

                var exit = Save("exit");
                Require(exit.WireSchemaVersion == 101 && exit.SchemaVersion == 90 && exit.Revision == 317
                    && exit.RuleClock == new RuleTime(113673, 2) && !exit.InventoryCombat && Life(exit).Hp == 0 && Life(exit).Stable
                    && Life(exit).StableUntil == new RuleTime(128033, 2) && Life(exit).Prone
                    && Life(exit).LinkedInjuries.SequenceEqual(new[] { 0 }), "Treatment must start at the authentic Stable-zero exit.");
                RequireStock(exit, 0, false);
                RequireStock(exit, 1, false);
                // Detached admission probes leave the actual session and its evidence untouched.
                var policy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession).GetField("policy", hidden).GetValue(session);
                string Assess(Snapshot probe) => policy.Resolve(probe, Treatment("wound.probe", CommandKind.StartWoundTreatment));
                var moved = exit.Copy();
                moved.Actors.Single(x => x.Id == patient).Y--;
                Require(Assess(moved) == "WoundTreatmentRequiresStationaryAccess", "The approved patient position is required.");
                var dying = exit.Copy();
                var priorLife = Life(exit);
                dying.Lives = dying.Lives.Select(x => x.ActorId == patient
                    ? new ActorLifeRecord(patient, priorLife.MaximumHp, 0, 0, priorLife.LinkedInjuries,
                        false, false, true, 0, 0, null, priorLife.LastDeathTurn, true, priorLife.HeldItems) : x).ToArray();
                Require(Assess(dying) == "WoundTreatmentPatientIneligible", "A dying zero-HP patient cannot start treatment.");
                var noKit = exit.Copy();
                noKit.Work = noKit.Work.Reserve("probe.kit", Array.Empty<WorkerInterval>(),
                    new[] { new ResourceReservation("probe.claim", "probe.kit", WoundTreatmentStation.KitLot, 1) });
                Require(Assess(noKit) == "WoundTreatmentSupplyOrKitUnavailable", "A reserved kit cannot fund another job.");
                var shortStock = exit.Copy();
                var food = WoundTreatmentStation.Stock(0).First();
                shortStock.Work = new WorkLedger(shortStock.Work.Lots.Where(x => x.Id != food.Id),
                    shortStock.Work.WorkerIntervals, shortStock.Work.Reservations);
                Require(Assess(shortStock) == "WoundTreatmentSupplyOrKitUnavailable", "Missing stock must reject before any debit.");
                var old = ConnectedExpeditionSession.StartWithCompanionStabilization();
                Throws<ArgumentException>(() => old.Restore(PathAt("exit")));
                Require(old.View(player).Revision == 0 && !old.View(player).Commands.Contains(CommandKind.StartWoundTreatment),
                    "Wire100 must retain its own save and command boundary.");

                var start = Treatment("wound.start", CommandKind.StartWoundTreatment);
                Deny(start, ExpeditionResponse.NotAuthorized, ExpeditionSeat.FirstOpponent);
                Deny(Treatment("wound.wrong-actor", CommandKind.StartWoundTreatment, actor: patient));
                Deny(Treatment("wound.wrong-target", CommandKind.StartWoundTreatment, target: hero));
                Deny(Treatment("wound.no-active", CommandKind.InterruptWoundTreatment));
                CommitVialRoute(session, start);
                var active = Save("active");
                Require(active.RuleClock == exit.RuleClock && active.RandomState == exit.RandomState
                    && Life(active).SameAs(Life(exit)) && active.WoundTreatments.Single().DueAt == new RuleTime(171273, 2)
                    && active.Work.Available(WoundTreatmentStation.KitLot) == 0, "Start must reserve and spend without advancing or rolling.");
                RequireStock(active, 0, true);
                RequireStock(active, 1, false);
                var job = active.WoundTreatments.Single();
                var healerInterval = active.Work.WorkerIntervals.Single(x => x.JobId == job.Id && x.WorkerId == hero);
                Require(WorldActivityValidation.HasActiveLabor(active, hero, healerInterval.Start, healerInterval.End)
                    && !WorldActivityValidation.HasActiveLabor(active, patient, healerInterval.Start, healerInterval.End),
                    "Patient access must stay distinct from healer labor.");
                Deny(Treatment("wound.parallel", CommandKind.StartWoundTreatment));
                Deny(new Command("wound.occupied-move", patient, active.Revision, CommandKind.BeginWorldStep, "walk", x: 1));
                Deny(new Command("wound.take-stock", hero, active.Revision, CommandKind.StartIntake,
                    WoundTreatmentStation.Stock(1).First().Id, inventory: new InventoryRequest(Q(1))));
                session.Restore(PathAt("active"));
                Require(session.Submit(player, start).Response == ExpeditionResponse.Duplicate
                    && codec.Encode(active).SequenceEqual(codec.Encode(Capture())), "A restored duplicate spent stock or changed work.");
                session.SetSeatEnabled(player, false);
                Deny(start, ExpeditionResponse.NotAuthorized);
                session.SetSeatEnabled(player, true);

                Clock("wound.recovery-before", 7179);
                var beforeRecovery = Save("before-recovery");
                Clock("wound.recovery", 1);
                var recovered = Save("recovered");
                var recovery = recovered.LifeEvents.Single(x => x.ActorId == patient && x.Kind == LifeEventKind.StableRecovery);
                Require(Life(beforeRecovery).Hp == 0 && Life(recovered).Hp == 1 && !Life(recovered).Stable
                    && Life(recovered).Prone && Life(recovered).LinkedInjuries.SequenceEqual(new[] { 0 })
                    && recovered.WoundTreatments.Single().Outcome == WoundTreatmentOutcome.Active
                    && recovery.At == new RuleTime(128033, 2) && recovery.WordsConsumed == 0,
                    "Recovery must occur independently at the native deadline while treatment continues.");
                Clock("wound.complete", 21620);
                var completed = Save("completed");
                var check = completed.WoundTreatments.Single();
                Require(check.Outcome == WoundTreatmentOutcome.Success && check.Natural == 17 && check.Modifier == 0
                    && check.WordsConsumed == 1 && check.EndedAt == new RuleTime(171273, 2) && check.EndRevision == completed.Revision
                    && check.RandomBefore == recovered.RandomState && check.RandomAfter == completed.RandomState
                    && Life(completed).Hp == 1 && Life(completed).MaximumHp == Life(recovered).MaximumHp
                    && Life(completed).Prone && Life(completed).LinkedInjuries.Count == 0
                    && completed.ExpeditionStrainGains.Length == 0 && completed.Work.Available(WoundTreatmentStation.KitLot) == 1,
                    "The eight-hour Medicine result must remove only the actual Wound.");
                Deny(Treatment("wound.already-treated", CommandKind.StartWoundTreatment));
                session.Restore(PathAt("completed"));
                Require(codec.Encode(completed).SequenceEqual(codec.Encode(Capture())), "Completed treatment did not strictly restore.");
                Deny(new Command("wound.pressure-block", hero, completed.Revision, CommandKind.BeginWorldStep, "walk", y: -1));
                Commit("wound.continue", hero, CommandKind.BeginWorldStep, "walk", x: 1);
                Clock("wound.continue-paid", 6);
                var continued = Save("continued");
                var position = continued.Actors.Single(x => x.Id == hero);
                Require(position.X == 2 && position.Y == 2 && Life(continued).SameAs(Life(completed)),
                    "Ordinary movement must continue through the legal side of the station after treatment.");

                session.Restore(PathAt("recovered"));
                var interrupt = Treatment("wound.interrupt", CommandKind.InterruptWoundTreatment);
                CommitVialRoute(session, interrupt);
                var interrupted = Save("interrupted");
                Require(interrupted.WoundTreatments.Single().Outcome == WoundTreatmentOutcome.Interrupted
                    && interrupted.WoundTreatments.Single().WordsConsumed == 0 && interrupted.RandomState == recovered.RandomState
                    && Life(interrupted).SameAs(Life(recovered)) && interrupted.Work.Available(WoundTreatmentStation.KitLot) == 1
                    && interrupted.Work.WorkerIntervals.Where(x => x.JobId == job.Id).All(x => x.End == interrupted.RuleClock),
                    "Interruption must keep elapsed work and release future occupancy without a roll or benefit.");
                RequireStock(interrupted, 0, true);
                RequireStock(interrupted, 1, false);
                Deny(interrupt, ExpeditionResponse.Duplicate);
                Clock("wound.intermission", 204767, 2);
                CommitVialRoute(session, Treatment("wound.restart", CommandKind.StartWoundTreatment));
                var restarted = Save("restarted");
                Require(restarted.WoundTreatments[1].StartedAt == new RuleTime(166400)
                    && restarted.WoundTreatments[1].DueAt == new RuleTime(195200), "Restart requires its own full eight hours.");
                RequireStock(restarted, 1, true);
                session.Restore(PathAt("restarted"));
                Clock("wound.restart-complete", 28800);
                var failed = Save("critical-failure");
                var failure = failed.WoundTreatments[1];
                var gain = failed.ExpeditionStrainGains.Single();
                var strain = ExpeditionStrainRules.Current(failed, patient);
                Require(failure.Outcome == WoundTreatmentOutcome.CriticalFailure && failure.Natural == 2 && failure.WordsConsumed == 1
                    && Life(failed).SameAs(Life(restarted)) && gain.ActorId == patient && gain.CauseId == failure.Id
                    && gain.Revision == failure.EndRevision && gain.At == failure.EndedAt
                    && gain.CauseKind == ExpeditionStrainCauseKind.WoundTreatmentCriticalFailure
                    && strain.Level == 1 && strain.InitiativeModifier == -1 && strain.ExpeditionCheckModifier == -1
                    && strain.AttackModifier == 0 && strain.SavingThrowModifier == 0 && ExpeditionStrainRules.Current(failed, hero).Level == 0,
                    "Critical Failure must add one shared Expedition Strain to the patient and keep the Wound.");
                Deny(Treatment("wound.no-third-basket", CommandKind.StartWoundTreatment));
                session.Restore(PathAt("critical-failure"));
                Require(codec.Encode(failed).SequenceEqual(codec.Encode(Capture())), "Critical Failure history did not strictly restore.");

                var forged = failed.Copy();
                forged.ExpeditionStrainGains = Array.Empty<ExpeditionStrainGainRecord>();
                Throws<ArgumentException>(() => codec.Encode(forged));
                forged = completed.Copy();
                forged.WoundTreatments = new[] { new WoundTreatmentRecord(check.Basket, check.StartCommandId, check.StartRevision,
                    check.StartedAt, check.LinkedInjury, check.Outcome, check.EndCommandId, check.EndRevision, check.EndedAt,
                    check.First, check.Second, check.Natural, check.Modifier + 1, check.RandomBefore, check.RandomAfter, check.WordsConsumed) };
                store.Save(PathAt("forged-check"), forged);
                Throws<ArgumentException>(() => session.Restore(PathAt("forged-check")));
                Require(codec.Encode(failed).SequenceEqual(codec.Encode(Capture())), "Forged check modified the live session.");
            });
        }
    }
}
#endif
