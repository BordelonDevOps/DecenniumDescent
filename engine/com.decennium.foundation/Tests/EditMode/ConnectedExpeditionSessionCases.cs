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
        }
    }
}
#endif
