#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static Authority DefenderCasePlayer()
        {
            var actors = new[] { PlanHero, BatchWorker };
            return new Authority("TEST_ONLY.host", actors, true, true, actors, actors);
        }

        private static CommandResult DefenderCaseCommit(Simulation sim, Authority authority, Command command)
        {
            var result = sim.Execute(authority, command);
            Require(result.Outcome == Outcome.Committed, command.Kind + " failed: " + result.Code);
            return result;
        }

        private static string DefenderViewFacts(DefenderDecisionView view)
            => FormattableString.Invariant($"{view.Slot}|{view.OwnCell.X},{view.OwnCell.Y}|{view.CanSelectStance}|{view.StanceSelected}|{view.CanAttack}|{view.CanMove}|{view.HasClub}|{view.EligibleOpportunity}|{view.VisibleProvokerId}|")
                + string.Join("|", view.VisibleOpponents.Select(x => FormattableString.Invariant($"{x.ActorId},{x.Cell.X},{x.Cell.Y},{x.ClearLineOfEffect}")))
                + ":" + string.Join("|", view.ApproachCells.Select(x => FormattableString.Invariant($"{x.X},{x.Y}")));

        private static void AddDetachedDefenderCondition(Snapshot snapshot, string actor, string kind, string id)
        {
            var journal = ConditionHistory.Restore(snapshot.Conditions.Single(x => x.Target == actor));
            var at = new ConditionStamp(snapshot.RuleClock);
            if (!journal.Journal.Now.Equals(at))
                journal = journal.Append(ConditionOperation.Advance("clock." + id, at)).State;
            var updated = CJApply(journal, id, kind).State.Journal;
            snapshot.Conditions = snapshot.Conditions.Select(x => x.Target == actor ? updated : x).ToArray();
        }

        private static void DefenderProjectionControls(TestOnlySharedWorldPolicy policy, Snapshot guarded,
            Authority defender, Command preferred)
        {
            var clear = guarded.Copy();
            var hiddenActor = clear.Actors.Single(x => x.Id == BatchWorker);
            AddDetachedDefenderCondition(clear, BatchWorker, "Invisible", "tac10-hidden-blocker");
            var occupied = clear.Copy();
            var blocker = occupied.Actors.Single(x => x.Id == hiddenActor.Id);
            blocker.X = preferred.X;
            blocker.Y = preferred.Y;
            occupied.Lives = occupied.Lives.Select(x => x.ActorId == PlanHero
                ? new ActorLifeRecord(x.ActorId, x.MaximumHp, 3, x.TemporaryHp, x.LinkedInjuries, x.Stable, x.Dead,
                    x.UsesDeathSaves, x.DeathSuccesses, x.DeathFailures, x.StableUntil, x.LastDeathTurn, x.Prone, x.HeldItems) : x).ToArray();
            var visibleA = policy.ObserveLaterDefender(clear, defender);
            var visibleB = policy.ObserveLaterDefender(occupied, defender);
            var selected = LaterDefenderDecisionPolicy.Select(visibleB);
            Require(DefenderViewFacts(visibleA) == DefenderViewFacts(visibleB)
                && selected.Kind == DefenderIntentKind.Step && selected.Destination.X == preferred.X
                && selected.Destination.Y == preferred.Y, "The view or move depended on hidden occupancy or private HP.");
            var admission = (ICommandAdmissionPolicy)policy;
            Require(admission.AssessAdmission(clear, preferred) == null
                && admission.AssessAdmission(occupied, preferred) == "OccupiedTacticalStep",
                "The trusted movement guard did not recheck the one attempted cell.");

            var known = guarded.Copy();
            AddDetachedDefenderCondition(known, PlanHero, "Invisible", "tac10-invisible-hero");
            var hero = known.Actors.Single(x => x.Id == PlanHero);
            known.ObserverKnowledge = known.ObserverKnowledge.Where(x => x.ObserverId != LaterDefender || x.TargetId != PlanHero)
                .Concat(new[] { new ObserverKnowledgeRecord(LaterDefender, PlanHero, true, true,
                    Q(hero.X), Q(hero.Y), ObservationEvidenceKind.Search, known.RuleClock, known.Revision,
                    revealedInvisibleEpisodeId: "tac10-invisible-hero") }).ToArray();
            Require(ObservationRules.LocationKnown(known, LaterDefender, PlanHero)
                && !ObservationRules.CanSee(known, LaterDefender, PlanHero)
                && LaterDefenderDecisionPolicy.Select(policy.ObserveLaterDefender(known, defender)).Kind == DefenderIntentKind.End,
                "A known unseen location drove the defender's attack or movement.");

            var obstructed = guarded.Copy();
            var origin = obstructed.Actors.Single(x => x.Id == LaterDefender);
            var target = obstructed.Actors.Single(x => x.Id == PlanHero);
            target.X = origin.X + 2;
            target.Y = origin.Y;
            int wallX = origin.X + 1;
            obstructed.ObservationCells = obstructed.ObservationCells.Where(x => x.X != wallX || x.Y != origin.Y)
                .Concat(new[] { new ObservationMapCellRecord(wallX, origin.Y, false, true, false, false) }).ToArray();
            Require(policy.ObserveLaterDefender(obstructed, defender).VisibleOpponents.Single(x => x.ActorId == PlanHero)
                .ClearLineOfEffect == false, "Direct sight hid the separate line-of-effect channel.");
        }

        private static void DefenderDeliveryControls(TestOnlySharedWorldPolicy policy, Snapshot state, Authority defender)
        {
            foreach (bool conflict in new[] { false, true }) {
                var fork = new Simulation(policy, state, ExecutionProfile.Laboratory);
                var controller = new LaterDefenderController(fork, policy);
                var plan = controller.Plan(defender);
                Require(plan.Intent.Kind == DefenderIntentKind.Step, "The delivery control needs a plan with an End fallback.");
                var competing = conflict
                    ? new Command(plan.Primary.Id, LaterDefender, state.Revision, CommandKind.EndRegularTurn, state.Encounter.CurrentTurnId)
                    : new Command("tac10.other-step", LaterDefender, state.Revision, CommandKind.TacticalStep,
                        state.Encounter.CurrentTurnId, plan.Primary.X, plan.Primary.Y);
                DefenderCaseCommit(fork, defender, competing);
                var beforeRetry = Bytes(fork);
                var expected = conflict ? DefenderDispatchStatus.Rejected : DefenderDispatchStatus.Stale;
                Require(controller.Dispatch(defender, plan) == expected && Bytes(fork).SequenceEqual(beforeRetry),
                    "A stale or conflicting planned move was converted into an extra turn End.");
            }
        }

        private static void DefenderHiddenBlocker(TestOnlySharedWorldPolicy policy, Simulation original, Authority defender,
            Authority player, string directory)
        {
            var blocked = SaveBill(original, policy, directory, "tac10-before-hidden-blocker");
            var fixtureHost = new Authority("TEST_ONLY.tac10-fixture", new[] { BatchWorker }, canModifyWorld: true);
            DefenderCaseCommit(blocked, fixtureHost, CCCommand(blocked, "tac10-worker-invisible", BatchWorker));
            DefenderCaseCommit(blocked, player, Tac(blocked, CommandKind.TacticalStep, x: 3, y: 4));
            DefenderCaseCommit(blocked, player, Tac(blocked, CommandKind.TacticalStep, x: 4, y: 4));
            DefenderCaseCommit(blocked, player, Tac(blocked, CommandKind.EndRegularTurn));
            var controller = new LaterDefenderController(blocked, policy);
            for (int decisions = 0; decisions < 6; decisions++) {
                var choice = controller.Plan(defender);
                var before = blocked.Capture();
                Require(choice.Primary != null, "The hidden-blocker witness lost its defender slot.");
                var admission = blocked.AssessCommandAdmission(defender, choice.Primary);
                if (admission.Code == "OccupiedTacticalStep") {
                    var hidden = before.Actors.Single(x => x.Id == BatchWorker);
                    Require(choice.Intent.Kind == DefenderIntentKind.Step && choice.Primary.X == hidden.X
                        && choice.Primary.Y == hidden.Y && !ObservationRules.CanSee(before, LaterDefender, BatchWorker),
                        "The preferred destination was not blocked by the genuinely unseen worker.");
                    Require(controller.Dispatch(defender, choice) == DefenderDispatchStatus.Committed,
                        "The fixed ordinary End fallback did not commit.");
                    var after = blocked.Capture();
                    Require(after.Revision == before.Revision + 1 && after.Encounter.CurrentActor == PlanHero
                        && after.TacticalMoves.Length == before.TacticalMoves.Length
                        && after.MeleeAttacks.Length == before.MeleeAttacks.Length,
                        "The fallback attempted another destination, attack or extra command.");
                    var bytes = Bytes(blocked);
                    Require(controller.Dispatch(defender, choice) == DefenderDispatchStatus.Duplicate
                        && Bytes(blocked).SequenceEqual(bytes), "Repeating a fallback delivery ended a second turn.");
                    SaveBill(blocked, policy, directory, "tac10-hidden-blocker-ended");
                    return;
                }
                Require(admission.Status == CommandAdmissionStatus.Admitted && controller.Dispatch(defender, choice) == DefenderDispatchStatus.Committed,
                    "Unexpected hidden-blocker setup admission: " + admission.Code);
            }
            throw new Exception("No real hidden-occupancy denial occurred on the selected approach.");
        }

        private static void AddLaterDefenderCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac10_later_defender_connected_decisions_restore_and_continue", () =>
            {
                var defender = LaterDefenderController.DefenderAuthority();
                var player = DefenderCasePlayer();
                var condition = CCApply("tac10-defender-stun", "Stunned", LaterDefender, at: new ConditionStamp(T(113301, 2)));
                var invisibility = CCApply("tac10-worker-invisible", "Invisible", BatchWorker, at: new ConditionStamp(T(113301, 2)));
                var policy = BatchPolicy(new[] { condition, invisibility });
                var sim = BatchReady(policy);
                var initialRoute = sim.Capture();
                Require(initialRoute.HavenSales.Single().PaymentCopper == 2 && initialRoute.LaterEncounter.FirstExit != null,
                    "The connected run did not retain acquisition and first encounter closure.");
                DefenderCaseCommit(sim, player, BatchCommand(sim, CommandKind.StartManufacturing, y: 2));
                WorldAdvance(sim, 900);
                WorldAdvance(sim, 13500);
                Require(BatchOrder(sim).Quality == CraftQuality.Exceptional, "The native connected quality check changed.");
                DefenderCaseCommit(sim, player, BatchCommand(sim, CommandKind.ResolveManufacturingQuality, (int)CraftQualityChoice.FullYield));
                DefenderCaseCommit(sim, player, BloodVesselCommand(sim, CommandKind.ClosePortableContainer));
                EnterLater(sim);
                var initialController = new LaterDefenderController(sim, policy);
                var waiting = initialController.Plan(defender);
                Require(waiting.Intent.Kind == DefenderIntentKind.Wait
                    && initialController.Dispatch(defender, waiting) == DefenderDispatchStatus.Waiting
                    && initialController.Dispatch(defender, waiting) == DefenderDispatchStatus.Waiting,
                    "The defender retried or acted during the hero's regular slot.");

                var stunned = SaveBill(sim, policy, directory, "tac10-later-entry");
                var fixtureHost = new Authority("TEST_ONLY.tac10-fixture", new[] { LaterDefender }, canModifyWorld: true);
                DefenderCaseCommit(stunned, fixtureHost, CCCommand(stunned, "tac10-defender-stun", LaterDefender));
                DefenderCaseCommit(stunned, player, Tac(stunned, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
                DefenderCaseCommit(stunned, player, Tac(stunned, CommandKind.EndRegularTurn));
                var impaired = new LaterDefenderController(stunned, policy);
                var impairedChoice = impaired.Plan(defender);
                if (impairedChoice.Intent.Kind == DefenderIntentKind.Guard) {
                    Require(impaired.Dispatch(defender, impairedChoice) == DefenderDispatchStatus.Committed,
                        "The existing Stunned turn could not select its required stance.");
                    impairedChoice = impaired.Plan(defender);
                }
                Require(!impairedChoice.View.CanAttack && !impairedChoice.View.CanMove
                    && impairedChoice.Intent.Kind == DefenderIntentKind.End
                    && impaired.Dispatch(defender, impairedChoice) == DefenderDispatchStatus.Committed
                    && stunned.Capture().MeleeAttacks.All(x => x.AttackerId != LaterDefender),
                    "The defender acted through real Stunned restrictions or failed to yield legally.");
                SaveBill(stunned, policy, directory, "tac10-stunned-yield");

                DefenderCaseCommit(sim, player, Tac(sim, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
                DefenderCaseCommit(sim, player, Tac(sim, CommandKind.TacticalStep, x: 1, y: 3));
                DefenderCaseCommit(sim, player, Tac(sim, CommandKind.TacticalStep, x: 2, y: 3));
                var move = TestOnlyClubAttackPolicy.PendingMove(sim.Capture());
                Require(move?.Pending == true && Body(sim).X == 1,
                    "The hero's actual move did not suspend for the defender.");
                var restored = SaveBill(sim, policy, directory, "tac10-pending-opportunity");
                var timings = new List<string> { "sample,projection_ms,admission_ms,dispatch_ms" };
                string opportunityId = "";
                foreach (var run in new[] { sim, restored }) {
                    var controller = new LaterDefenderController(run, policy);
                    var before = run.Capture();
                    var bytes = Bytes(run);
                    var clock = Stopwatch.StartNew();
                    var plan = controller.Plan(defender);
                    double projection = clock.Elapsed.TotalMilliseconds;
                    Require(plan.Intent.Kind == DefenderIntentKind.AcceptOpportunity && plan.Primary.Actor == LaterDefender
                        && before.Encounter.CurrentActor == PlanHero && !player.Controls(LaterDefender),
                        "The actual responder did not own the off-turn decision.");
                    if (run == sim) opportunityId = plan.Primary.Id;
                    Require(plan.Primary.Id == opportunityId
                        && run.Execute(player, plan.Primary).Code == "NotAuthorized", "Wrong owner or divergent restored intent.");
                    clock.Restart();
                    var admission = run.AssessCommandAdmission(defender, plan.Primary);
                    double admissionMs = clock.Elapsed.TotalMilliseconds;
                    var policyAdmission = (ICommandAdmissionPolicy)policy;
                    var unsupported = new Command("tac10.unsupported-end", LaterDefender, before.Revision,
                        CommandKind.EndFixedEncounter, before.Encounter.CurrentTurnId);
                    Require(admission.Status == CommandAdmissionStatus.Admitted && Bytes(run).SequenceEqual(bytes)
                        && policyAdmission.AssessAdmission(before, plan.Primary) == null
                        && policyAdmission.AssessAdmission(before, unsupported) == "DefenderAdmissionUnavailable"
                        && new SnapshotCodec().Encode(before).SequenceEqual(bytes),
                        "Pre-roll admission mutated the suspended candidate or accepted an unsupported command.");
                    var revoked = new Authority(LaterDefenderController.Principal, new[] { LaterDefender });
                    Require(controller.Dispatch(revoked, plan) == DefenderDispatchStatus.Rejected
                        && Bytes(run).SequenceEqual(bytes), "A revoked Club grant reached the fallback.");
                    clock.Restart();
                    var response = controller.Dispatch(defender, plan);
                    double dispatch = clock.Elapsed.TotalMilliseconds;
                    timings.Add(FormattableString.Invariant($"opportunity,{projection:F3},{admissionMs:F3},{dispatch:F3}"));
                    var after = run.Capture();
                    Require(response == DefenderDispatchStatus.Committed && after.RuleClock == before.RuleClock
                        && after.Revision == before.Revision + 1 && after.MeleeAttacks.Last().Opportunity
                        && after.MeleeAttacks.Last().AttackerId == LaterDefender
                        && !after.TacticalActors.Single(x => x.ActorId == LaterDefender).ReactionAvailable
                        && after.TacticalMoves.Last().Status == TacticalMoveStatus.Completed
                        && after.Actors.Single(x => x.Id == PlanHero).X == 2,
                        "The actual response did not pay Reaction and resume the suspended movement.");
                    bytes = Bytes(run);
                    Require(controller.Dispatch(defender, plan) == DefenderDispatchStatus.Duplicate
                        && controller.Dispatch(revoked, plan) == DefenderDispatchStatus.Rejected
                        && Bytes(run).SequenceEqual(bytes), "An accepted duplicate or revoked retry changed the turn.");
                    var conflict = new Command(plan.Primary.Id, LaterDefender, before.Revision, CommandKind.EndRegularTurn,
                        before.Encounter.CurrentTurnId);
                    Require(run.AssessCommandAdmission(defender, conflict).Code == "CommandIdConflict",
                        "The normal receipt path lost its command-ID conflict.");

                    string doseId = after.AlchemyDoses[0].Id;
                    var dose = run.DiscoverCommands(player, PlanHero).Single(x => x.Command.Kind == CommandKind.UseAlchemyDose
                        && x.Command.Target == doseId && x.Command.Inventory.Destination == PlanHero);
                    Require(dose.Query.Admissible, "The player could not lawfully use the finite output.");
                    DefenderCaseCommit(run, player, dose.Command);
                    if (run == sim) DefenderHiddenBlocker(policy, run, defender, player, directory);
                    DefenderCaseCommit(run, player, Tac(run, CommandKind.EndRegularTurn));

                    bool step = false, attack = false;
                    for (int decisions = 0; decisions < 48 && run.Capture().InventoryCombat; decisions++) {
                        var state = run.Capture();
                        if (state.Encounter.CurrentActor == LaterDefender) {
                            clock.Restart();
                            var choice = controller.Plan(defender);
                            projection = clock.Elapsed.TotalMilliseconds;
                            Require(choice.Primary != null, "The defender did not own its actual regular choice.");
                            if (run == sim && !step && choice.Intent.Kind == DefenderIntentKind.Step) {
                                DefenderProjectionControls(policy, state, defender, choice.Primary);
                                DefenderDeliveryControls(policy, state, defender);
                            }
                            clock.Restart();
                            admission = run.AssessCommandAdmission(defender, choice.Primary);
                            admissionMs = clock.Elapsed.TotalMilliseconds;
                            Require(admission.Status == CommandAdmissionStatus.Admitted,
                                "The selected regular action did not admit: " + admission.Code);
                            clock.Restart();
                            Require(controller.Dispatch(defender, choice) == DefenderDispatchStatus.Committed,
                                "A legal defender choice did not commit.");
                            dispatch = clock.Elapsed.TotalMilliseconds;
                            timings.Add(FormattableString.Invariant($"{choice.Intent.Kind},{projection:F3},{admissionMs:F3},{dispatch:F3}"));
                            var paid = run.Capture();
                            if (choice.Intent.Kind == DefenderIntentKind.Step) {
                                step = true;
                                Require(paid.WorldIntervals.Single(x => x.ActorId == LaterDefender).MovementSpent
                                    > state.WorldIntervals.Single(x => x.ActorId == LaterDefender).MovementSpent, "The step did not pay movement.");
                            }
                            if (choice.Intent.Kind == DefenderIntentKind.Attack) {
                                attack = true;
                                Require(paid.WorldIntervals.Single(x => x.ActorId == LaterDefender).ActionSpent
                                    && controller.Plan(defender).Intent.Kind == DefenderIntentKind.End, "An attack failed to use the real Action.");
                            }
                            continue;
                        }
                        DefenderCaseCommit(run, player, Tac(run, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
                        if (!run.Capture().Lives.Single(x => x.ActorId == LaterDefender).Dead) {
                            Require(ActorLifeRules.CanAct(state, PlanHero), "The actual defender defeated this witness.");
                            DefenderCaseCommit(run, player, Tac(run, CommandKind.AttackClub, LaterDefender,
                                weapon: TestOnlyClubAttackPolicy.ActorClub));
                        }
                        bool defeated = run.Capture().Lives.Single(x => x.ActorId == LaterDefender).Dead;
                        DefenderCaseCommit(run, player, Tac(run, defeated ? CommandKind.EndFixedEncounter : CommandKind.EndRegularTurn));
                    }
                    Require(step && attack && !run.Capture().InventoryCombat && run.Capture().AlchemyDoses.Count(x => x.Spent) == 1,
                        "The controller-driven encounter did not close after actual movement, attack and dose use.");
                    PlanWalk(run, 0, -1);
                }
                Require(Bytes(sim).SequenceEqual(Bytes(restored)), "The controller-driven continuation diverged after authentic restore.");
                SaveBill(sim, policy, directory, "tac10-continued");
                File.WriteAllLines(Path.Combine(directory, "tac10-timings.csv"), timings);
            });
        }
    }
}
#endif
