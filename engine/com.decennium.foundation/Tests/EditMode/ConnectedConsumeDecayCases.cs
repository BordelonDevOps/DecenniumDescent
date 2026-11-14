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
        private static void AddConnectedConsumeDecayCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac06_connected_consume_decay_depletion_healing_and_expiry", () =>
            {
                const string hero = ConnectedExpeditionSession.Hero;
                const string ally = ConnectedExpeditionSession.Companion;
                const string enemy = "TEST_ONLY.later-defender";
                const ExpeditionSeat player = ExpeditionSeat.Player;
                const BindingFlags hidden = BindingFlags.Instance | BindingFlags.NonPublic;
                var simulation = typeof(ConnectedExpeditionSession).GetField("simulation", hidden);
                var session = StartVialScenario(ConnectedExpeditionSession.StartWithConsumeDecay());
                var codec = new SnapshotCodec();
                var store = new FileSaveStore();
                Snapshot Capture() => ((Simulation)simulation.GetValue(session)).Capture();
                string FileAt(string key) => Path.Combine(directory, "consume-decay-" + key + ".ddsave");
                Snapshot Save(string key) { session.Save(FileAt(key)); return store.Load(FileAt(key)); }
                ActorLifeRecord Hero(Snapshot s) => s.Lives.Single(x => x.ActorId == hero);
                AlchemyDoseRecord Vial(Snapshot s) => s.AlchemyDoses.Single(x => x.Id == VialId);
                Command Grant(string id, long? revision = null)
                    => new Command(id, hero, revision ?? session.View(player).Revision, CommandKind.ConsumeDecay, ConsumeDecaySite.Id);
                void Commit(string id, string actor, CommandKind kind, string target = "", int x = 0, int y = 0,
                    InventoryRequest inventory = null, CombatRequest combat = null)
                    => CommitVialRoute(session, new Command(id, actor, session.View(player).Revision, kind, target, x, y, inventory, combat));
                void Guard(string actor)
                    => Commit("decay.guard." + session.View(player).Revision, actor, CommandKind.SelectCombatStance,
                        combat: new CombatRequest(session.View(player).TurnId, stance: 1));
                void End(string actor)
                    => Commit("decay.end." + session.View(player).Revision, actor, CommandKind.EndRegularTurn, session.View(player).TurnId);
                void Step(int x, int y)
                    => Commit("decay.step." + session.View(player).Revision, hero, CommandKind.TacticalStep, session.View(player).TurnId, x, y);
                void Defender()
                {
                    int count = 0;
                    while (session.View(player).NextSeat == ExpeditionTurnSeat.AutomaticDefender)
                        Require(count++ < 12 && session.AdvanceAutomaticDefender().Response == ExpeditionResponse.Committed,
                            "Actual defender turn did not resolve.");
                }
                void Heal() => Commit("decay.vial", hero, CommandKind.UseAlchemyDose, VialId, inventory: new InventoryRequest(Q(1), hero));
                void Deny(Command command, ExpeditionResponse expected = ExpeditionResponse.Unavailable, ExpeditionSeat seat = player)
                {
                    var before = codec.Encode(Capture());
                    Require(session.Submit(seat, command).Response == expected && before.SequenceEqual(codec.Encode(Capture())),
                        "Denial changed Consume Decay state: " + command.Id);
                }
                void FightRound(int turn)
                {
                    Guard(hero);
                    Require(Capture().Encounter.TurnOrdinal == turn, "Unexpected hero turn in the real later encounter.");
                    Commit("decay.attack." + turn, hero, CommandKind.AttackClub, enemy,
                        combat: new CombatRequest(session.View(player).TurnId, "TEST_ONLY.actor-club"));
                }
                void NextRound()
                {
                    End(hero); Defender(); Guard(ally); End(ally);
                }
                void CloseAndWalk(string label)
                {
                    Commit("decay.close", hero, CommandKind.EndFixedEncounter, session.View(player).TurnId);
                    Save(label + "-closed");
                    Commit("decay.continue", hero, CommandKind.BeginWorldStep, "walk", y: -1);
                    Commit("decay.walk-paid", hero, CommandKind.AdvanceClock, x: 6, y: 1);
                    var after = Save(label + "-continued");
                    var position = after.Actors.Single(x => x.Id == hero);
                    Require(!after.InventoryCombat && position.X == 0 && position.Y == 1, "Ordinary continuation must use a paid step.");
                }

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
                Guard(hero);
                var entry = Save("entry");
                Require(entry.WireSchemaVersion == 102 && entry.SchemaVersion == 90 && entry.ConsumeDecay == null
                    && session.View(player).KnownTargets[CommandKind.ConsumeDecay] == ConsumeDecaySite.Id
                    && !session.View(ExpeditionSeat.FirstOpponent).Commands.Contains(CommandKind.ConsumeDecay),
                    "The selected public command must remain owner-scoped.");
                var old = ConnectedExpeditionSession.StartWithWoundTreatment();
                Throws<ArgumentException>(() => old.Restore(FileAt("entry")));
                Require(old.View(player).Revision == 0 && !old.View(player).Commands.Contains(CommandKind.ConsumeDecay), "Wire101 is independent.");

                // Detached controls use the same resolver and do not edit or restore the live route.
                var policy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession).GetField("policy", hidden).GetValue(session);
                var usedAction = entry.Copy();
                usedAction.WorldIntervals = usedAction.WorldIntervals.Select(x => x.ActorId == hero ? x.PayAction() : x).ToArray();
                Require(policy.Resolve(usedAction, Grant("decay.probe-action")) == "ActionAlreadySpent", "Action ownership is enforced.");
                var blocked = entry.Copy();
                blocked.ObservationCells = blocked.ObservationCells.Append(new ObservationMapCellRecord(
                    ConsumeDecaySite.X, ConsumeDecaySite.Y, false, true, false, false)).ToArray();
                Require(policy.Resolve(blocked, Grant("decay.probe-blocked")) == "ConsumeDecaySubstrateOutOfReach",
                    "Five-foot geometry does not bypass obstructed access.");
                var oldGrant = new ConsumeDecayRecord("decay.arbitration.old", 1, new RuleTime(1), 6, true);
                var larger = new ConsumeDecayRecord("decay.arbitration.larger", 2, new RuleTime(2), 4, true);
                var equal = new ConsumeDecayRecord("decay.arbitration.equal", 3, new RuleTime(3), 3, true);
                var smaller = new ConsumeDecayRecord("decay.arbitration.smaller", 4, new RuleTime(4), 2, true);
                var winner = TemporaryHpRules.Select(oldGrant, 3, larger);
                var equalResult = TemporaryHpRules.Select(oldGrant, 3, equal);
                var smallerResult = TemporaryHpRules.Select(oldGrant, 3, smaller);
                Require(ReferenceEquals(winner.Grant, larger) && winner.Remaining == 4 && winner.Grant.Deadline == larger.Deadline
                    && ReferenceEquals(equalResult.Grant, oldGrant) && equalResult.Remaining == 3 && equalResult.Grant.Deadline == oldGrant.Deadline
                    && ReferenceEquals(smallerResult.Grant, oldGrant) && smallerResult.Remaining == 3 && smallerResult.Grant.Deadline == oldGrant.Deadline,
                    "Shared arbitration must retain the winning identity, actual balance and its original deadline.");
                var stale = TemporaryHpRules.Expire(winner.Grant, winner.Remaining, oldGrant, oldGrant.Deadline);
                var atWinnerEnd = TemporaryHpRules.Expire(stale.Grant, stale.Remaining, larger, larger.Deadline);
                var discardedEnd = TemporaryHpRules.Expire(atWinnerEnd.Grant, atWinnerEnd.Remaining, equal, equal.Deadline);
                var finalEnd = TemporaryHpRules.Expire(discardedEnd.Grant, discardedEnd.Remaining, smaller, smaller.Deadline);
                var retainedEnd = TemporaryHpRules.Expire(equalResult.Grant, equalResult.Remaining, oldGrant, oldGrant.Deadline);
                Require(ReferenceEquals(stale.Grant, larger) && stale.Remaining == 4
                    && atWinnerEnd.Grant == null && atWinnerEnd.Remaining == 0
                    && discardedEnd.Grant == null && discardedEnd.Remaining == 0 && finalEnd.Grant == null && finalEnd.Remaining == 0
                    && retainedEnd.Grant == null && retainedEnd.Remaining == 0,
                    "Replacement and discarded deadlines cannot clear or revive another grant.");
                var overflow = PlaytestDamageDice.Resolve(new LifeState(26, 21, 3), 5, entry.RuleClock, entry.RandomState).Outcome;
                Require(overflow.TemporaryAbsorbed == 3 && overflow.PostTempDamage == 2
                    && overflow.State.TemporaryHp == 0 && overflow.State.Hp == 19 && overflow.State.MaximumHp == 26,
                    "Detached same-packet overflow must settle each part once through shared damage.");

                var early = Grant("decay.early");
                Deny(early, ExpeditionResponse.NotAuthorized, ExpeditionSeat.FirstOpponent);
                CommitVialRoute(session, early);
                var granted = Save("early-granted");
                Require(granted.ConsumeDecay.Active && granted.ConsumeDecay.Offer == 3
                    && Hero(granted).TemporaryHp == 3 && Hero(granted).Hp == Hero(entry).Hp
                    && Hero(granted).MaximumHp == Hero(entry).MaximumHp && granted.RandomState == entry.RandomState
                    && granted.RuleClock == entry.RuleClock && granted.InventoryInteractions == entry.InventoryInteractions
                    && granted.WorldIntervals.Single(x => x.ActorId == hero).ActionSpent
                    && session.View(player).Actors.Single(x => x.Position.Id == hero).TemporaryHp == 3,
                    "Activation must spend one Action and one source use without changing actual life or RNG.");
                session.Restore(FileAt("early-granted"));
                Deny(early, ExpeditionResponse.Duplicate);
                session.SetSeatEnabled(player, false);
                Deny(early, ExpeditionResponse.NotAuthorized);
                session.SetSeatEnabled(player, true);
                Deny(new Command(early.Id, hero, early.ExpectedRevision, early.Kind, hero), ExpeditionResponse.CommandIdConflict);
                Step(0, 2); Defender();
                var depleted = Save("depleted");
                Require(depleted.ConsumeDecay.End == TemporaryHpEnd.Depleted && Hero(depleted).TemporaryHp == 0
                    && Hero(depleted).Hp == 26 && depleted.MeleeAttacks.Last().Damage.Total == 3
                    && depleted.MeleeAttacks.Last().ResolvedRevision == depleted.ConsumeDecay.EndRevision,
                    "A genuine defender opportunity must consume the three-point buffer.");
                End(hero); Defender();
                var admitted = Save("admitted-after-depletion");
                Require(Hero(admitted).Hp == 24 && admitted.MeleeAttacks.Last().Damage.Total == 2, "Later genuine damage must hit normal HP.");
                Deny(Grant("decay.wrong-turn"));
                Guard(ally); End(ally); Guard(hero);
                Step(0, 1); Defender(); End(hero); Defender(); Guard(ally); End(ally); Guard(hero);
                Step(0, 2);
                Deny(Grant("decay.spent"));
                Heal();
                var earlyHealing = Save("early-healing");
                Require(Vial(earlyHealing).ActualHealing == 2 && Hero(earlyHealing).Hp == 26 && Hero(earlyHealing).TemporaryHp == 0,
                    "Real healing must leave an empty buffer empty.");
                NextRound();
                foreach (int turn in new[] { 9, 12, 15, 18, 21 }) { FightRound(turn); if (turn != 21) NextRound(); }
                CloseAndWalk("early");

                session.Restore(FileAt("entry"));
                Step(0, 2);
                var pending = Save("pending");
                Require(session.View(player).OpportunityPending, "An actual defender choice must be pending.");
                Deny(Grant("decay.pending"));
                Defender(); End(hero); Defender();
                Guard(ally); End(ally); Guard(hero); Step(0, 1); Defender(); End(hero); Defender();
                Guard(ally); End(ally); Guard(hero);
                Deny(Grant("decay.out-of-reach"));
                Step(0, 2); NextRound();
                foreach (int turn in new[] { 9, 12, 15, 18, 21 }) { FightRound(turn); NextRound(); }
                for (int rounds = 0; ; rounds++) {
                    Guard(hero);
                    var before = Capture();
                    var opponent = before.Lives.Single(x => x.ActorId == enemy);
                    Require(rounds < 12 && Hero(before).Hp > 0 && Hero(before).Hp < Hero(before).MaximumHp,
                        "Late route needs a genuinely injured hero and ordinary encounter closure.");
                    if (opponent.Dead && rounds > 0) {
                        CommitVialRoute(session, Grant("decay.late"));
                        break;
                    }
                    if (opponent.Hp > 0)
                        Commit("decay.finish." + before.Revision, hero, CommandKind.AttackClub, enemy,
                            combat: new CombatRequest(session.View(player).TurnId, "TEST_ONLY.actor-club"));
                    NextRound();
                }
                var lateGrant = Save("late-granted");
                Require(lateGrant.ConsumeDecay.Active && Hero(lateGrant).Hp < Hero(lateGrant).MaximumHp
                    && Hero(lateGrant).TemporaryHp == 3, "Late grant must leave real HP untouched.");
                NextRound();
                Guard(hero); Heal();
                var lateHealing = Save("late-healing");
                Require(Vial(lateHealing).ActualHealing > 0 && Hero(lateHealing).Hp > Hero(lateGrant).Hp
                    && Hero(lateHealing).MaximumHp == 26 && Hero(lateHealing).TemporaryHp == 3, "The real vial must heal without replenishing or replacing the buffer.");
                CloseAndWalk("late");
                var continuation = Capture();
                Require(!continuation.InventoryCombat && Hero(continuation).TemporaryHp == 3, "Closing and leaving must retain the grant.");
                int untilLastSecond = checked((int)(lateGrant.ConsumeDecay.Deadline.Numerator - continuation.RuleClock.Numerator) / 2 - 1);
                Commit("decay.before-expiry", hero, CommandKind.AdvanceClock, x: untilLastSecond, y: 1);
                var justBefore = Save("before-expiry");
                session.Restore(FileAt("before-expiry"));
                Commit("decay.expire", hero, CommandKind.AdvanceClock, x: 1, y: 1);
                var expired = Save("expired");
                Require(justBefore.RuleClock.AddSeconds(1) == expired.RuleClock && expired.RuleClock == lateGrant.ConsumeDecay.Deadline
                    && expired.ConsumeDecay.End == TemporaryHpEnd.Expired && expired.ConsumeDecay.EndRevision == expired.Revision
                    && expired.RandomState == justBefore.RandomState && Hero(expired).TemporaryHp == 0
                    && Hero(expired).Hp == Hero(justBefore).Hp && Hero(expired).MaximumHp == Hero(justBefore).MaximumHp
                    && Hero(expired).Prone == Hero(justBefore).Prone && Hero(expired).LinkedInjuries.SequenceEqual(Hero(justBefore).LinkedInjuries)
                    && expired.Conditions.Zip(justBefore.Conditions, (left, right) => left.SameAs(right)).All(x => x),
                    "Exact expiry changes only the still-active temporary HP and its terminal evidence.");
                session.Restore(FileAt("expired"));
                Require(codec.Encode(expired).SequenceEqual(codec.Encode(Capture())), "Expired grant must restore canonically.");

                var forged = justBefore.Copy();
                var grant = forged.ConsumeDecay;
                forged.ConsumeDecay = new ConsumeDecayRecord(grant.CommandId, grant.Revision, grant.StartedAt, grant.Offer + 1, true);
                store.Save(FileAt("forged-offer"), forged);
                Throws<ArgumentException>(() => session.Restore(FileAt("forged-offer")));
                forged = expired.Copy();
                forged.ConsumeDecay = new ConsumeDecayRecord(grant.CommandId, grant.Revision, grant.StartedAt,
                    grant.Offer, true, TemporaryHpEnd.Depleted, justBefore.RuleClock, justBefore.Revision);
                store.Save(FileAt("forged-end"), forged);
                Throws<ArgumentException>(() => session.Restore(FileAt("forged-end")));
                forged = granted.Copy();
                forged.ConsumeDecay = null;
                Throws<ArgumentException>(() => codec.Encode(forged));
                Require(codec.Encode(expired).SequenceEqual(codec.Encode(Capture())), "Forged grant must not replace the live state.");
            });
        }
    }
}
#endif
