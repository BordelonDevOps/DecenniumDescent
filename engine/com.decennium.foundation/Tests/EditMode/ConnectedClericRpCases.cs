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
        private static ConnectedExpeditionSession NewClericExpedition()
            => ConnectedExpeditionSession.StartWithClericCompanion(ClericInitialSelection.AuthoredExample());

        private static TestOnlySharedWorldPolicy ClericPolicy(ConnectedExpeditionSession session)
            => (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession).GetField("policy", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(session);

        private static void ClericCommit(ConnectedExpeditionSession session, string actor, CommandKind kind,
            string target = "", int x = 0, int y = 0, CombatRequest combat = null)
        {
            long revision = session.View(ExpeditionSeat.Player).Revision;
            CommitVialRoute(session, new Command("cleric.route." + revision, actor, revision, kind, target, x, y, combat: combat));
        }
        private static void ClericGuard(ConnectedExpeditionSession session, string actor)
            => ClericCommit(session, actor, CommandKind.SelectCombatStance,
                combat: new CombatRequest(session.View(ExpeditionSeat.Player).TurnId, stance: 1));
        private static void ClericEnd(ConnectedExpeditionSession session, string actor)
            => ClericCommit(session, actor, CommandKind.EndRegularTurn, session.View(ExpeditionSeat.Player).TurnId);
        private static void ClericDefender(ConnectedExpeditionSession session)
        {
            int count = 0;
            while (session.View(ExpeditionSeat.Player).NextSeat == ExpeditionTurnSeat.AutomaticDefender)
                Require(count++ < 12 && session.AdvanceAutomaticDefender().Response == ExpeditionResponse.Committed,
                    "Actual defender decision did not commit.");
        }
        private static ConnectedExpeditionSession ClericInjuredArrival(ConnectedExpeditionSession selected = null)
        {
            var session = StartVialScenario(selected ?? NewClericExpedition());
            const string hero = ConnectedExpeditionSession.Hero, ally = ConnectedExpeditionSession.Companion;
            ClericCommit(session, ally, CommandKind.BeginWorldStep, "walk", -1);
            ClericCommit(session, hero, CommandKind.AdvanceClock, x: 6, y: 1);
            ClericCommit(session, hero, CommandKind.BeginWorldStep, "walk", -1);
            ClericCommit(session, hero, CommandKind.AdvanceClock, x: 12, y: 1);
            ClericCommit(session, ally, CommandKind.BeginReinforcementApproach, "TEST_ONLY.companion-reinforcement.v1");
            ClericGuard(session, hero);
            ClericCommit(session, hero, CommandKind.TacticalStep, session.View(ExpeditionSeat.Player).TurnId, y: 2);
            ClericDefender(session); ClericEnd(session, hero); ClericDefender(session);
            Require(ShortRestCapture(session).Reinforcement.Admission != null, "Actual paid reinforcement must admit the Cleric.");
            ClericGuard(session, ally); ClericEnd(session, ally); ClericGuard(session, hero);
            ClericCommit(session, hero, CommandKind.TacticalStep, session.View(ExpeditionSeat.Player).TurnId, y: 1);
            ClericDefender(session); ClericEnd(session, hero); ClericDefender(session);
            var arrival = ShortRestCapture(session);
            Require(arrival.Encounter.CurrentActor == ally && arrival.Lives.Single(x => x.ActorId == ally).Hp < 8
                && !arrival.Lives.Single(x => x.ActorId == ally).Dead, "Real later combat must injure the living Cleric before Healing Rite.");
            return session;
        }

        private static void AddConnectedClericRpCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("chr02_cleric_initial_class_source_funding_and_save_boundaries", () =>
            {
                var session = NewClericExpedition(); var policy = ClericPolicy(session); var codec = new SnapshotCodec();
                var initial = ShortRestCapture(session); const string ally = ClericRpProfile.Actor;
                var character = initial.Characters.Single(x => x.ActorId == ally); var pool = initial.ResonancePools.Single();
                Require(initial.WireSchemaVersion == 105 && initial.SchemaVersion == 90 && initial.TestOnly
                    && character.Levels.Single().ClassName == "Cleric" && character.Abilities.SequenceEqual(new[] { 10, 10, 10, 10, 14, 10 })
                    && initial.Lives.Single(x => x.ActorId == ally).Hp == 8 && initial.CharacterHitDice.Single().DieSize == 8
                    && initial.ClericEntry.PointBuyCost == 17 && !initial.ClericEntry.ConvictionSupported
                    && pool.Current == 3 && pool.Maximum == 3 && pool.InitialFunding.Revision == 0
                    && initial.CharacterFeatureGrants.All(x => ClericRpProfile.ValidInitialGrant(initial, x)),
                    "Typed initial class construction must bind the approved source and distinct TEST_ONLY funding.");
                Require(pool.Pay(2).ReconcileCapacity(9).Current == 1 && pool.Pay(2).ReconcileCapacity(0).Current == 0,
                    "Capacity reconciliation cannot fund RP.");
                string path = Path.Combine(directory, "cleric-initial.ddsave"); session.Save(path); session.Restore(path);
                Require(codec.Encode(initial).SequenceEqual(codec.Encode(ShortRestCapture(session))), "Initial save/restore must retain exact one-time funding.");
                var legacy = ConnectedExpeditionSession.Start(); Throws<ArgumentException>(() => legacy.Restore(path));
                Require(ShortRestCapture(legacy).ResonancePools.Length == 0 && legacy.View(ExpeditionSeat.Player).Revision == 0,
                    "Old profile must reject Cleric saves unchanged.");
                var before = codec.Encode(initial);
                Require(session.Submit(ExpeditionSeat.Player, new Command("cleric.no-rest", ConnectedExpeditionSession.Hero, 0,
                    CommandKind.BeginShortRest, ShortRestBerth.Id)).Response == ExpeditionResponse.Unavailable
                    && before.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Unsupported class recovery cannot grant time, HP or RP.");
                void Reject(Snapshot forged)
                {
                    bool rejected = false; try { codec.Encode(forged); } catch (ArgumentException) { rejected = true; }
                    Require(rejected || policy.ValidateState(forged) != null, "Forged class/funding state accepted.");
                }
                var bad = initial.Copy(); bad.ResonancePools = new[] { new ResonancePoolRecord(ally, 3, 2, pool.InitialFunding) }; Reject(bad);
                bad = initial.Copy(); bad.CharacterFeatureGrants = bad.CharacterFeatureGrants.Where(x => x.FeatureId != ClericRpProfile.HealingRite).ToArray(); Reject(bad);
                bad = initial.Copy(); bad.ResonancePools = new[] { new ResonancePoolRecord(ally, 3, 3,
                    new ResonanceFundingRecord("forged.funding", ally, ClericRpProfile.FundingPolicy, 3, 0)) }; Reject(bad);
                Throws<ArgumentNullException>(() => ConnectedExpeditionSession.StartWithClericCompanion(null));
                Throws<ArgumentException>(() => new ClericInitialSelection(new[] { 10, 10, 10, 10, 14, 10 },
                    new[] { "medicine", "medicine" }, ClericRpProfile.SelectedCards, ClericRpProfile.FavoredWeapon));
                Throws<ArgumentException>(() => new ClericInitialSelection(new[] { 10, 10, 10, 10, 14, 10 },
                    new[] { "medicine", "religion" }, new[] { "cleric.base.consecrate", "cleric.base.consecrated-ground",
                        "cleric.base.fervent-ritualist", "cleric.saint.resurrection" }, ClericRpProfile.FavoredWeapon));
            });

            cases.Add("chr02_cleric_connected_injury_payment_restore_and_continuation", () =>
            {
                var session = ClericInjuredArrival(); var codec = new SnapshotCodec(); var policy = ClericPolicy(session);
                const string hero = ConnectedExpeditionSession.Hero, ally = ConnectedExpeditionSession.Companion;
                const ExpeditionSeat player = ExpeditionSeat.Player;
                var before = ShortRestCapture(session);
                var command = new Command("cleric.paid-heal", ally, before.Revision, CommandKind.UseHealingRite, ally);
                var beforeBytes = codec.Encode(before);
                Require(session.Submit(ExpeditionSeat.FirstOpponent, command).Response == ExpeditionResponse.NotAuthorized
                    && beforeBytes.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Wrong seat cannot issue a shared RP payment.");
                ClericGuard(session, ally);
                command = new Command(command.Id, ally, session.View(player).Revision, CommandKind.UseHealingRite, ally);
                CommitVialRoute(session, command);
                var paid = ShortRestCapture(session); var healing = paid.HealingRites.Single();
                Require(healing.RpBefore == 3 && healing.RpPaid == 2 && healing.RpAfter == 1 && healing.ActualGain > 0
                    && healing.Modifier == 2 && paid.ResonancePools.Single().Current == 1 && paid.RandomState != before.RandomState
                    && paid.WorldIntervals.Single(x => x.ActorId == ally).ActionSpent,
                    "Actual injury must heal using one Action, shared RNG and exactly two finite RP.");
                var paidBytes = codec.Encode(paid);
                Require(session.Submit(player, command).Response == ExpeditionResponse.Duplicate
                    && paidBytes.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Retry must not spend twice.");
                session.SetSeatEnabled(player, false);
                Require(session.Submit(player, command).Response == ExpeditionResponse.NotAuthorized
                    && paidBytes.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Current authority must precede duplicate lookup.");
                session.SetSeatEnabled(player, true);
                string path = Path.Combine(directory, "cleric-paid.ddsave"); session.Save(path); session = NewClericExpedition(); session.Restore(path);
                Require(paidBytes.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Paid save must restore without refund or another RNG draw.");
                var forged = paid.Copy(); forged.ResonancePools = new[] { new ResonancePoolRecord(ally, 3, 3, paid.ResonancePools.Single().InitialFunding) };
                Throws<ArgumentException>(() => codec.Encode(forged));
                forged = paid.Copy();
                forged.HealingRites = new[] { new HealingRiteRecord(healing.CommandId, healing.Revision, healing.ActorId,
                    healing.TargetId, healing.SourceId, healing.SourceRevision, healing.TurnOrdinal, healing.At, 3, 2, 1,
                    healing.Die, healing.Modifier, healing.Potential, healing.HpBefore, healing.HpAfter,
                    healing.RandomBefore == 1 ? 2u : 1u, healing.RandomAfter, healing.WordsConsumed) };
                Require(policy.ValidateState(forged) != null, "Strict history must reject a forged paid RNG provenance.");
                ClericEnd(session, ally); ClericGuard(session, hero);
                ClericCommit(session, hero, CommandKind.TacticalStep, session.View(player).TurnId, y: 2);
                ClericEnd(session, hero); ClericDefender(session); ClericGuard(session, ally);
                var denied = ShortRestCapture(session); var retry = new Command("cleric.insufficient", ally, denied.Revision, CommandKind.UseHealingRite, ally);
                Require(!denied.WorldIntervals.Single(x => x.ActorId == ally).ActionSpent
                    && policy.Resolve(denied.Copy(), retry) == "InsufficientResonance", "Later available Action must reach the finite RP gate.");
                Require(session.Submit(player, retry).Response == ExpeditionResponse.Unavailable
                    && codec.Encode(denied).SequenceEqual(codec.Encode(ShortRestCapture(session))), "Insufficient RP denial must preserve the entire state.");
                ClericEnd(session, ally);
                for (int round = 0; ; round++) {
                    Require(round < 24, "Actual combat must conclude without injected damage.");
                    ClericGuard(session, hero);
                    if (ShortRestCapture(session).Lives.Single(x => x.ActorId == "TEST_ONLY.later-defender").Dead) break;
                    ClericCommit(session, hero, CommandKind.AttackClub, "TEST_ONLY.later-defender",
                        combat: new CombatRequest(session.View(player).TurnId, "TEST_ONLY.actor-club"));
                    ClericEnd(session, hero); ClericDefender(session); ClericGuard(session, ally); ClericEnd(session, ally);
                }
                ClericCommit(session, hero, CommandKind.EndFixedEncounter, session.View(player).TurnId);
                ClericCommit(session, hero, CommandKind.BeginWorldStep, "walk", y: -1);
                ClericCommit(session, hero, CommandKind.AdvanceClock, x: 6, y: 1);
                var continued = ShortRestCapture(session); session.Save(path); session.Restore(path);
                Require(!continued.InventoryCombat && continued.ResonancePools.Single().Current == 1
                    && continued.HealingRites.Length == 1 && codec.Encode(continued).SequenceEqual(codec.Encode(ShortRestCapture(session))),
                    "Paid ordinary continuation and strict replay must preserve the finite payment.");
            });

            cases.Add("chr02_healing_rite_detached_life_condition_and_admission_controls", () =>
            {
                // Detached mechanical controls are deliberately not accepted campaign history.
                // The preceding case supplies actual source, injury, payment and continuation evidence.
                var session = ClericInjuredArrival(); const string ally = ClericRpProfile.Actor;
                const string hero = ConnectedExpeditionSession.Hero;
                ClericGuard(session, ally); var baseline = ShortRestCapture(session); var policy = ClericPolicy(session);
                Command Use(Snapshot s, string target = hero, string actor = ally)
                    => new Command("detached.rite", actor, s.Revision, CommandKind.UseHealingRite, target);
                void Life(Snapshot s, string actor, long hp, bool stable = false, bool dead = false)
                {
                    var old = s.Lives.Single(x => x.ActorId == actor);
                    s.Lives = s.Lives.Select(x => x.ActorId != actor ? x : new ActorLifeRecord(actor, old.MaximumHp, hp, 3,
                        new[] { (int)Injury.Concussion }, stable, dead, true, hp == 0 && !stable && !dead ? 1 : 0,
                        dead ? 3 : hp == 0 && !stable ? 2 : 0, stable ? s.RuleClock.AddSeconds(900) : (RuleTime?)null,
                        old.LastDeathTurn, true, old.HeldItems)).ToArray();
                }
                void Condition(Snapshot s, string actor, string condition)
                {
                    var journal = s.Conditions.Single(x => x.Target == actor);
                    var changed = CJApply(ConditionHistory.Restore(journal), "detached." + condition, condition).State.Journal;
                    s.Conditions = s.Conditions.Select(x => x.Target == actor ? changed : x).ToArray();
                }
                void Deny(Snapshot s, string reason, string target = hero, string actor = ally)
                {
                    var lives = s.Lives; var pools = s.ResonancePools; var intervals = s.WorldIntervals; var history = s.HealingRites;
                    uint rng = s.RandomState; var time = s.RuleClock; long revision = s.Revision;
                    Require(policy.Resolve(s, Use(s, target, actor)) == reason && ReferenceEquals(lives, s.Lives)
                        && ReferenceEquals(pools, s.ResonancePools) && ReferenceEquals(intervals, s.WorldIntervals)
                        && ReferenceEquals(history, s.HealingRites) && rng == s.RandomState && time == s.RuleClock && revision == s.Revision,
                        "Detached preflight changed payment/life/clock state: " + reason);
                }
                var s = baseline.Copy(); Life(s, ally, 8);
                Require(policy.Resolve(s, Use(s, ally)) == null && s.HealingRites.Single().ActualGain == 0
                    && s.ResonancePools.Single().Current == 1 && s.RandomState != baseline.RandomState
                    && s.WorldIntervals.Single(x => x.ActorId == ally).ActionSpent,
                    "Legal full-HP self use must still pay one Action/two RP and draw the actual healing die.");
                foreach (bool stable in new[] { false, true }) {
                    s = baseline.Copy(); Life(s, hero, 0, stable);
                    var before = s.Lives.Single(x => x.ActorId == hero);
                    Require(policy.Resolve(s, Use(s)) == null, "Living zero-HP ally must be a legal ordinary-healing target.");
                    var healed = s.Lives.Single(x => x.ActorId == hero);
                    Require(healed.Hp > 0 && !healed.Stable && !healed.Dead && healed.DeathSuccesses == 0 && healed.DeathFailures == 0
                        && healed.StableUntil == null && healed.TemporaryHp == 3 && healed.LinkedInjuries.SequenceEqual(before.LinkedInjuries)
                        && healed.Prone == before.Prone && !s.DyingCadences.Any(x => x.ActorId == hero),
                        "Ordinary healing must clear dying/Stable while retaining injuries, temporary HP and posture.");
                }
                s = baseline.Copy(); Life(s, hero, 1); Condition(s, hero, "Corrupted");
                Require(policy.Resolve(s, Use(s)) == null && s.HealingRites.Single().Potential < s.HealingRites.Single().RolledPotential
                    && s.HealingRites.Single().Potential == PlaytestConditions.HpRestorationAmount(s.HealingRites.Single().RolledPotential, true),
                    "Shared Corrupted projection must reduce the actual paid heal before life resolution.");
                s = baseline.Copy(); Life(s, hero, 0, dead: true); Deny(s, "HealingRiteTargetUnavailable");
                s = baseline.Copy(); Life(s, ally, 0); Deny(s, "ConditionPreventsAction");
                s = baseline.Copy(); Condition(s, ally, "Stunned"); Deny(s, "ConditionPreventsAction");
                s = baseline.Copy(); Condition(s, ally, "Blinded"); Deny(s, "HealingRiteTargetUnavailable");
                s = baseline.Copy(); s.Actors.Single(x => x.Id == hero).X += 100; Deny(s, "HealingRiteTargetUnavailable");
                s = baseline.Copy(); Deny(s, "HealingRiteTargetUnavailable", "TEST_ONLY.later-defender");
                s = baseline.Copy(); Deny(s, "HealingRiteUnavailable", ally, hero);
                s = baseline.Copy(); s.CharacterFeatureGrants = s.CharacterFeatureGrants.Where(x => x.FeatureId != ClericRpProfile.HealingRite).ToArray();
                Deny(s, "HealingRiteNotOwned");
                s = baseline.Copy(); s.WorldIntervals = s.WorldIntervals.Select(x => x.ActorId == ally ? x.PayAction() : x).ToArray();
                Deny(s, "ActionAlreadySpent");
                s = baseline.Copy(); var pool = s.ResonancePools.Single();
                s.ResonancePools = new[] { pool.Pay(2) }; Deny(s, "InsufficientResonance");
            });
        }
    }
}
#endif
