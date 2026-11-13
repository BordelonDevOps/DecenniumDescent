#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddConnectedExpeditionSessionCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("mgt06_session_trap_profile_restore_and_remote_resume", () =>
            {
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const string companion = ConnectedExpeditionSession.Companion;
                const string hero = ConnectedExpeditionSession.Hero;
                const string trap = SharedFishingTrapFixture.TrapId;
                var session = ConnectedExpeditionSession.StartWithFishingTrap();
                var original = ConnectedExpeditionSession.Start();
                var store = new FileSaveStore();
                string baseline = Path.Combine(directory, "mgt06-default.ddsave");
                string selected = Path.Combine(directory, "mgt06-opt-in.ddsave");
                original.Save(baseline);
                session.Save(selected);
                var before = store.Load(baseline);
                var after = store.Load(selected);
                Require(before.WireSchemaVersion == after.WireSchemaVersion && before.ContentFingerprint != after.ContentFingerprint
                    && after.FishingTraps.Single().TrapId == trap
                    && after.PortableEquipment.Select(x => x.Id).Where(x => x != trap)
                        .SequenceEqual(before.PortableEquipment.Select(x => x.Id))
                    && before.Clubs.Select(x => x.Id + ":" + x.HeldBy).SequenceEqual(after.Clubs.Select(x => x.Id + ":" + x.HeldBy))
                    && before.BonusActions.Select(x => x.ActorId).SequenceEqual(after.BonusActions.Select(x => x.ActorId))
                    && after.SkillTraining.Count(x => x.SkillId == "fishing-tackle" && x.ActorId == companion) == 1,
                    "The separate wire-compatible profile must preserve existing equipment and ledgers.");
                foreach (var pair in new[] { (Session: session, Path: baseline), (Session: original, Path: selected) }) {
                    bool rejected = false;
                    try { pair.Session.Restore(pair.Path); }
                    catch (ArgumentException) { rejected = true; }
                    Require(rejected && pair.Session.View(player).Revision == 0, "Wrong-profile restore must be atomic.");
                }
                Command Interact(string id, long revision, FishingTrapInteraction operation)
                    => new Command(id, companion, revision, CommandKind.Interact, trap, (int)operation);
                var start = Interact("trap.test.set", 0, FishingTrapInteraction.Set);
                // An isolated resolver probe gives WIS and INT different values without changing the playable profile.
                var policy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession)
                    .GetField("policy", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic).GetValue(session);
                var probe = after.Copy();
                var character = probe.Characters.Single(x => x.ActorId == companion);
                int[] abilities = character.Abilities.ToArray();
                abilities[(int)CharacterAbility.Wisdom] = 16;
                abilities[(int)CharacterAbility.Intelligence] = 8;
                probe.Characters = probe.Characters.Select(x => x.ActorId == companion
                    ? new ActorCharacterRecord(x.ActorId, x.ProfileId, abilities, x.Levels) : x).ToArray();
                Require(policy.Resolve(probe, start) == null, "The isolated Wisdom probe must book real setup.");
                probe.Revision = 1;
                Require(policy.Resolve(probe, new Command("trap.test.wisdom", hero, 1, CommandKind.AdvanceClock, x: 300, y: 1)) == null
                    && probe.FishingTrapAttempts.Single().WisdomModifier == 3
                    && probe.FishingTrapAttempts.Single().ProficiencyBonus == 2,
                    "The opted-in resolver must capture Wisdom and one proficiency contribution at completed setup.");
                Require(session.View(ExpeditionSeat.FirstOpponent).FishingTrap == null
                    && session.Submit(ExpeditionSeat.FirstOpponent, start).Response == ExpeditionResponse.NotAuthorized
                    && session.Submit(player, start).Response == ExpeditionResponse.Committed, "Setup must use the ordinary companion grant.");
                Require(session.SubmitSessionCommand(new Command("trap.test.labor", hero, 1, CommandKind.AdvanceClock, x: 1, y: 2))
                        .Response == ExpeditionResponse.Committed
                    && session.Submit(player, Interact("trap.test.pause", 2, FishingTrapInteraction.Pause))
                        .Response == ExpeditionResponse.Committed, "Setup work must pause with exact labor.");
                Require(session.Submit(player, new Command("trap.test.depart", companion, 3, CommandKind.BeginWorldStep, "walk", x: 1))
                        .Response == ExpeditionResponse.Committed
                    && session.SubmitSessionCommand(new Command("trap.test.walk", hero, 4, CommandKind.AdvanceClock, x: 6, y: 1))
                        .Response == ExpeditionResponse.Committed, "Paused setter must be able to leave the site.");
                string remote = Path.Combine(directory, "mgt06-remote.ddsave");
                session.Save(remote);
                session.Restore(remote);
                var view = session.View(player);
                Require(!view.FishingTrap.ObservedLocally && view.FishingTrap.PhysicalStatus == null
                    && view.FishingTrap.CheckOutcome == null && view.FishingTrap.SetupLabor == new RuleTime(1, 2)
                    && view.FishingTrap.ScheduledCheckAt == new RuleTime(3300)
                    && view.Items.All(x => x.Id != trap && x.Id != SharedFishingTrapFixture.BaitLotId)
                    && session.Submit(player, Interact("trap.test.remote.resume", 5, FishingTrapInteraction.Resume))
                        .Response == ExpeditionResponse.Unavailable
                    && session.Submit(player, start).Response == ExpeditionResponse.Duplicate
                    && session.View(player).Revision == 5, "A fresh remote Resume and exact receipt retry must differ.");
                session.Save(remote);
                File.WriteAllBytes(remote, new byte[] { 1, 2, 3 });
                session.RecoverBackup(remote);
                Require(session.View(player).FishingTrap.SetupLabor == new RuleTime(1, 2),
                    "Explicit recovery must keep the selected profile and paid work.");
            });

            cases.Add("exp05_session_exact_local_traversal_restore", () =>
            {
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const string hero = ConnectedExpeditionSession.Hero;
                const string companion = ConnectedExpeditionSession.Companion;
                var session = ConnectedExpeditionSession.Start();
                Require(session.View(player).MiningSite.ObservedLocally && session.View(ExpeditionSeat.FirstOpponent).MiningSite == null,
                    "The selected site must remain scoped to the party worker.");
                var step = new Command("travel.local.step", companion, 0, CommandKind.BeginWorldStep, "walk", x: 1);
                Require(session.Submit(ExpeditionSeat.FirstOpponent, step).Response == ExpeditionResponse.NotAuthorized
                    && session.Submit(player, step).Response == ExpeditionResponse.Committed, "The companion owns the ordinary approach.");
                var tick = new Command("travel.local.partial", hero, 1, CommandKind.AdvanceClock, x: 1, y: 2);
                Require(session.SubmitSessionCommand(tick).Response == ExpeditionResponse.Committed, "Fractional clock advance failed.");
                var partial = session.View(player);
                var travel = partial.Actors.Single(x => x.Position.Id == companion).Traversal;
                Require(travel != null && travel.ExactX > new RuleQuantity(3) && travel.ExactX < new RuleQuantity(4)
                    && travel.ExactY == new RuleQuantity(3) && travel.DistanceFeet + travel.EdgeFeetRemaining == new RuleQuantity(5)
                    && travel.MovementSpent == travel.DistanceFeet && !travel.PersonalStart && travel.IntervalIndex == 0
                    && partial.MiningSite.ClaimClosed == null && partial.MiningSite.Units.Count == 0
                    && session.View(ExpeditionSeat.FirstOpponent).Actors.All(x => x.Traversal == null),
                    "Own fractional progress and spending must not expose remote site state or another seat's travel.");
                string file = Path.Combine(directory, "exp05-traversal.ddsave");
                session.Save(file);
                var restored = ConnectedExpeditionSession.Start();
                restored.Restore(file);
                var resumed = restored.View(player).Actors.Single(x => x.Position.Id == companion).Traversal;
                Require(resumed.ExactX == travel.ExactX && resumed.ExactY == travel.ExactY
                    && resumed.MovementSpent == travel.MovementSpent && resumed.MovementRemaining == travel.MovementRemaining
                    && resumed.CalendarId == travel.CalendarId && resumed.IntervalIndex == travel.IntervalIndex
                    && restored.Submit(player, step).Response == ExpeditionResponse.Duplicate,
                    "Restore and duplicate delivery must preserve the exact edge and allowance.");
                var complete = new Command("travel.local.complete", hero, 2, CommandKind.AdvanceClock, x: 2, y: 1);
                foreach (var run in new[] { session, restored }) {
                    Require(run.SubmitSessionCommand(complete).Response == ExpeditionResponse.Committed,
                        "The existing clock must complete the edge.");
                    var actor = run.View(player).Actors.Single(x => x.Position.Id == companion);
                    Require(actor.Traversal == null && actor.Position.X == 4 && actor.Position.Y == 3,
                        "Arrival must keep the exact destination.");
                }
                string a = Path.Combine(directory, "exp05-traversal-continued.ddsave");
                string b = Path.Combine(directory, "exp05-traversal-restored.ddsave");
                session.Save(a);
                restored.Save(b);
                Require(File.ReadAllBytes(a).SequenceEqual(File.ReadAllBytes(b)), "Exact partial restore changed continued bytes.");
            });

            cases.Add("exp04_session_ordinary_observation_scope_before_charter", () =>
            {
                var session = ConnectedExpeditionSession.Start();
                var player = session.View(ExpeditionSeat.Player);
                var director = session.View(ExpeditionSeat.FirstOpponent);
                Require(player.Observation != null && !player.Observation.OrdinaryStageOpen
                    && player.Observation.HideStartId == null && player.Observation.SearchStartId == null
                    && player.Observation.HideAttempts.Count == 0 && player.Observation.SearchAttempts.Count == 0
                    && director.Observation == null, "The unopened stage and opposing seat must disclose no observation inputs.");
                var hide = new Command("observation.early.hide", ConnectedExpeditionSession.Hero, 0, CommandKind.Hide,
                    "world.fixed-calendar.start.0");
                var search = new Command("observation.early.search", ConnectedExpeditionSession.Companion, 0, CommandKind.Search,
                    "world.fixed-calendar.activity.0", 1, 0);
                Require(session.Submit(ExpeditionSeat.Player, hide).Response == ExpeditionResponse.Unavailable
                    && session.Submit(ExpeditionSeat.Player, search).Response == ExpeditionResponse.Unavailable
                    && session.Submit(ExpeditionSeat.FirstOpponent, search).Response == ExpeditionResponse.NotAuthorized
                    && session.View(ExpeditionSeat.Player).Revision == 0, "Early or wrong-seat observation must leave history unchanged.");
            });

            cases.Add("int03_session_scoped_views_delivery_and_validated_file_recovery", () =>
            {
                const string hero = ConnectedExpeditionSession.Hero;
                const string opponent = ConnectedExpeditionSession.FirstOpponent;
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const ExpeditionSeat director = ExpeditionSeat.FirstOpponent;
                var session = ConnectedExpeditionSession.Start();
                var initial = session.View(player);
                var directorInitial = session.View(director);
                Require(initial.TestOnly && initial.Revision == 0 && !initial.InEncounter
                    && initial.Actors.Select(x => x.Position.Id).SequenceEqual(new[] { hero, ConnectedExpeditionSession.Companion })
                    && initial.Actors.All(x => x.VisibleOpponents.Count == 0)
                    && directorInitial.Actors.Single().Position.Id == opponent && directorInitial.Work.Count == 0
                    && directorInitial.Items.All(x => x.OwnerId == opponent) && directorInitial.KnownTargets.Count == 0,
                    "The two local views must expose only their permitted starting actors, jobs, targets and resources.");
                var walk = new Command("session.walk.1", hero, 0, CommandKind.BeginWorldStep, "walk", x: 1);
                Require(session.Submit(director, walk).Response == ExpeditionResponse.NotAuthorized
                    && session.SubmitSessionCommand(walk).Response == ExpeditionResponse.Unavailable
                    && session.Submit(player, new Command("session.clock.early", hero, 0, CommandKind.AdvanceClock, x: 2, y: 1))
                        .Response == ExpeditionResponse.Unavailable, "Player, director and trusted calendar authorities must be separate.");
                Require(session.Submit(player, walk).Response == ExpeditionResponse.Committed, "Public walk failed.");
                Require(session.Submit(player, walk).Response == ExpeditionResponse.Duplicate
                    && session.Submit(player, new Command(walk.Id, hero, 0, CommandKind.BeginWorldStep, "walk", x: -1))
                        .Response == ExpeditionResponse.CommandIdConflict
                    && session.Submit(player, new Command("session.walk.stale", hero, 0, CommandKind.BeginWorldStep, "walk", x: 1))
                        .Response == ExpeditionResponse.StaleRevision, "Duplicate, conflict or stale delivery changed.");
                session.SetSeatEnabled(player, false);
                var revoked = session.View(player);
                Require(session.Submit(player, walk).Response == ExpeditionResponse.NotAuthorized
                    && !revoked.Enabled && revoked.Actors.Count == 0 && revoked.Items.Count == 0 && revoked.Work.Count == 0,
                    "Revocation must apply before duplicate handling and projection.");
                session.SetSeatEnabled(player, true);

                var clock = new Command("session.clock.2", hero, 1, CommandKind.AdvanceClock, x: 2, y: 1);
                string file = Path.Combine(directory, "int03-session-recovery.ddsave");
                session.Save(file);
                Require(session.SubmitSessionCommand(clock).Response == ExpeditionResponse.Committed, "Trusted clock failed.");
                session.Save(file);
                File.WriteAllBytes(file, new byte[] { 1, 2, 3 });
                bool rejected = false;
                try { session.Restore(file); }
                catch (InvalidDataException) { rejected = true; }
                Require(rejected && session.View(player).Revision == 2, "Corrupt external load must preserve the live session.");
                string displaced = session.RecoverBackup(file);
                Require(File.ReadAllBytes(displaced).SequenceEqual(new byte[] { 1, 2, 3 })
                    && File.ReadAllBytes(file).SequenceEqual(File.ReadAllBytes(file + ".bak"))
                    && session.View(player).Revision == 1 && session.Submit(player, walk).Response == ExpeditionResponse.Duplicate
                    && session.SubmitSessionCommand(clock).Response == ExpeditionResponse.Committed,
                    "Explicit recovery must preserve both files and resume from the validated backup.");

                Require(session.Submit(player, new Command("session.walk.3", hero, 2, CommandKind.BeginWorldStep, "walk", x: 1))
                        .Response == ExpeditionResponse.Committed
                    && session.SubmitSessionCommand(new Command("session.clock.4", hero, 3, CommandKind.AdvanceClock, x: 2, y: 1))
                        .Response == ExpeditionResponse.Committed
                    && session.Submit(player, new Command("session.walk.5", hero, 4, CommandKind.BeginWorldStep, "walk", x: 1))
                        .Response == ExpeditionResponse.Committed, "First tactical entry through ordinary inputs failed.");
                var firstTurn = session.View(director);
                var playerTurn = session.View(player);
                Require(firstTurn.NextSeat == ExpeditionTurnSeat.FirstOpponent && firstTurn.ActingActorId == opponent
                    && firstTurn.TurnId != "" && playerTurn.TurnId == "" && playerTurn.ActingActorId == ""
                    && playerTurn.Actors.All(x => x.Position.Id != opponent), "The first turn token belongs to the director.");
                var stance = new Command("session.stance.6", opponent, 5, CommandKind.SelectCombatStance,
                    combat: new CombatRequest(firstTurn.TurnId, stance: (int)CombatStance.Aggressive));
                var hidden = new Command("session.hidden.6", opponent, 5, CommandKind.AttackClub, TestOnlySharedWorldPolicy.LaterDefenderId,
                    combat: new CombatRequest(firstTurn.TurnId, AdditionalTacticalActor.ClubId));
                var absent = new Command("session.absent.6", opponent, 5, CommandKind.AttackClub, "absent",
                    combat: hidden.Combat);
                Require(session.Submit(player, stance).Response == ExpeditionResponse.NotAuthorized
                    && session.Submit(director, hidden).Response == ExpeditionResponse.Unavailable
                    && session.Submit(director, absent).Response == ExpeditionResponse.Unavailable
                    && session.AdvanceAutomaticDefender().Response == ExpeditionResponse.Waiting
                    && session.Submit(director, stance).Response == ExpeditionResponse.Committed,
                    "The director must use the actual first turn and may not probe the later defender.");
                session.Save(file);
                var snapshot = new FileSaveStore().Load(file);
                Require(snapshot.TestOnly && snapshot.WireSchemaVersion == Snapshot.ConnectedRecipe4BatchSchema
                    && snapshot.Receipts.Last().Principal == ConnectedExpeditionSession.FirstOpponentPrincipal,
                    "The ordinary wire95 save must retain the separate opponent receipt.");
            });

            cases.Add("int03_session_off_turn_knockout_and_press_restore", () =>
            {
                const string hero = ConnectedExpeditionSession.Hero;
                const string opponent = ConnectedExpeditionSession.FirstOpponent;
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const ExpeditionSeat director = ExpeditionSeat.FirstOpponent;
                var session = ConnectedExpeditionSession.Start();
                Command Input(string actor, CommandKind kind, string target = "", int x = 0, int y = 0,
                    CombatRequest combat = null)
                {
                    long revision = session.View(player).Revision;
                    return new Command("session.choice." + (revision + 1).ToString(System.Globalization.CultureInfo.InvariantCulture),
                        actor, revision, kind, target, x, y, combat: combat);
                }
                ExpeditionActionResult Commit(ExpeditionActionResult result)
                {
                    Require(result.Response == ExpeditionResponse.Committed, "The public choice branch failed: " + result.Response);
                    return result;
                }
                void AssertChoice(ExpeditionSeat seat, ExpeditionSeat other, ExpeditionDecisionKind kind, string actor)
                {
                    var view = session.View(seat);
                    var privateView = session.View(other);
                    Require(view.PendingDecision == kind && view.ActingActorId == actor && view.DecisionId != ""
                        && view.TurnId != "" && privateView.DecisionId == "" && privateView.ActingActorId == "",
                        "Only the actual responding actor's seat may see its token and submit the pending choice.");
                }

                for (int step = 0; step < 3; step++) {
                    Commit(session.Submit(player, Input(hero, CommandKind.BeginWorldStep, "walk", x: 1)));
                    if (step < 2) Commit(session.SubmitSessionCommand(Input(hero, CommandKind.AdvanceClock, x: 2, y: 1)));
                }
                var thirdTurn = session.View(director).TurnId;
                Commit(session.Submit(director, Input(opponent, CommandKind.SelectCombatStance,
                    combat: new CombatRequest(thirdTurn, stance: (int)CombatStance.Aggressive))));
                Commit(session.Submit(director, Input(opponent, CommandKind.TacticalStep, thirdTurn, x: 3)));
                string before = Path.Combine(directory, "int03-session-choice-fork.ddsave");
                session.Save(before);

                Commit(session.Submit(director, Input(opponent, CommandKind.TacticalStep, thirdTurn, x: 4)));
                AssertChoice(player, director, ExpeditionDecisionKind.Opportunity, hero);
                string opportunityFile = Path.Combine(directory, "int03-session-choice-opportunity.ddsave");
                session.Save(opportunityFile);
                session = ConnectedExpeditionSession.Start();
                session.Restore(opportunityFile);
                AssertChoice(player, director, ExpeditionDecisionKind.Opportunity, hero);
                var reaction = session.View(player);
                Require(reaction.TurnId == thirdTurn, "An off-turn player needs the actual turn token for its opportunity.");
                var strike = Input(hero, CommandKind.RespondOpportunityAttack, reaction.DecisionId,
                    combat: new CombatRequest(reaction.TurnId, TestOnlyClubAttackPolicy.ActorClub,
                        knockout: AttackKnockoutMode.AskIfEligible, choice: true));
                Require(session.Submit(director, strike).Response == ExpeditionResponse.NotAuthorized,
                    "Only the player may answer the off-turn opportunity.");
                var suspended = Commit(session.Submit(player, strike));
                Require(suspended.PendingDecision == ExpeditionDecisionKind.Knockout && !suspended.OpportunityPending
                    && suspended.NextSeat == ExpeditionTurnSeat.Player, "Knockout must take priority over its suspended opportunity move.");
                AssertChoice(player, director, ExpeditionDecisionKind.Knockout, hero);
                string pending = Path.Combine(directory, "int03-session-choice-knockout.ddsave");
                session.Save(pending);
                var pendingFile = new FileSaveStore().Load(pending);
                var move = TestOnlyClubAttackPolicy.PendingMove(pendingFile);
                Require(move != null && move.ResponseIndex == move.Reactors.Count,
                    "This branch must suspend a move with its last opportunity already submitted.");
                session = ConnectedExpeditionSession.Start();
                session.Restore(pending);
                AssertChoice(player, director, ExpeditionDecisionKind.Knockout, hero);
                var knockout = session.View(player);
                var resolve = Input(hero, CommandKind.ResolveKnockout, knockout.DecisionId,
                    combat: new CombatRequest(knockout.TurnId));
                Require(session.Submit(director, resolve).Response == ExpeditionResponse.NotAuthorized
                    && session.Submit(player, strike).Response == ExpeditionResponse.Duplicate,
                    "Only the player may decide the knockout, and retrying the reaction may not roll again.");
                Require(Commit(session.Submit(player, resolve)).PendingDecision == ExpeditionDecisionKind.None,
                    "Resolving the real knockout must release the tactical continuation.");

                session.Restore(before);
                Commit(session.Submit(director, Input(opponent, CommandKind.AttackClub, hero,
                    combat: new CombatRequest(thirdTurn, AdditionalTacticalActor.ClubId))));
                Commit(session.Submit(director, Input(opponent, CommandKind.EndRegularTurn, thirdTurn)));
                string heroTurn = session.View(player).TurnId;
                Commit(session.Submit(player, Input(hero, CommandKind.SelectCombatStance,
                    combat: new CombatRequest(heroTurn, stance: (int)CombatStance.Aggressive))));
                Commit(session.Submit(player, Input(hero, CommandKind.TacticalStep, heroTurn, x: 1)));
                AssertChoice(director, player, ExpeditionDecisionKind.Opportunity, opponent);
                var opportunity = session.View(director);
                Require(opportunity.TurnId == heroTurn, "An off-turn opponent needs the actual turn token for its opportunity.");
                Commit(session.Submit(director, Input(opponent, CommandKind.RespondOpportunityAttack, opportunity.DecisionId,
                    combat: new CombatRequest(opportunity.TurnId))));
                AssertChoice(director, player, ExpeditionDecisionKind.Press, opponent);
                string pressFile = Path.Combine(directory, "int03-session-choice-press.ddsave");
                session.Save(pressFile);
                session = ConnectedExpeditionSession.Start();
                session.Restore(pressFile);
                AssertChoice(director, player, ExpeditionDecisionKind.Press, opponent);
                var press = session.View(director);
                var follow = Input(opponent, CommandKind.RespondPress, press.DecisionId,
                    combat: new CombatRequest(press.TurnId, choice: true));
                Require(session.Submit(player, follow).Response == ExpeditionResponse.NotAuthorized,
                    "The player cannot decide the director's Press.");
                Require(Commit(session.Submit(director, follow)).PendingDecision == ExpeditionDecisionKind.None
                    && session.View(director).Actors.Single().Position.X == 2,
                    "Accepting Press must perform the existing follow step and return control.");
                Require(session.Submit(director, follow).Response == ExpeditionResponse.Duplicate,
                    "Retrying the Press response may not repeat the follow step.");
            });
        }
    }
}
#endif
