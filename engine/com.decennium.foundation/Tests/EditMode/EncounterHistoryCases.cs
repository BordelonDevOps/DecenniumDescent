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
        private static Snapshot ArchiveFixture()
        {
            var s = CCPolicy().Initial(); s.SchemaVersion = Snapshot.SharedWorldSchema; s.Revision = 8; s.RuleClock = T(4);
            var order = new[] { TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId };
            s.ClosedEncounters = new[] { new ClosedEncounterRecord(new FixedEncounterRecord("encounter.first", default, order, new long[] { 1, 3 }), 5, T(3), "TEST_ONLY.closed") };
            s.Encounter = new FixedEncounterRecord("encounter.second", T(4), order, new long[] { 6 });
            s.InventoryCombat = true; s.InventoryTurnActor = order[0];
            s.Conditions = s.Actors.Select(a => new ConditionJournal(ConditionHistory.PolicyId, a.Id, CJAt(4))).ToArray();
            // Deliberately structural data, not a lawful gameplay/receipt history.
            return s;
        }
        private static void AddEncounterHistoryCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("encounter_history_resolves_original_revision_not_current_ordinal", () => {
                var s = ArchiveFixture();
                Require(EncounterHistory.AtRevision(s, 2).Id == "encounter.first" && EncounterHistory.AtRevision(s, 5).Id == "encounter.first"
                    && EncounterHistory.AtRevision(s, 6).Id == "encounter.second" && EncounterHistory.AtRevision(s, 0) == null, "History range lookup changed identity.");
                Require(EncounterHistory.LatestStartOrdinal(s, TestOnlyPolicy.ActorId) == 0 && EncounterHistory.LatestStartOrdinal(s, TestOnlyPolicy.CompanionId) == 1, "Latest actual Start lost across episodes.");
            });
            cases.Add("encounter_history_previous_dash_does_not_spend_new_action_or_grant_speed", () => {
                var s = ArchiveFixture(); s.EncounterDashes = new[] { new EncounterDashRecord(2, 0, TestOnlyPolicy.ActorId) };
                s.ActorMovement = s.ActorMovement.Select(a => new ActorMovementRecord(a.ActorId, 30, a.ActorId == TestOnlyPolicy.ActorId ? 0 : 1)).ToArray();
                Validation.Snapshot(s);
                Require(!FixedEncounterRules.ActionSpent(s) && !TestOnlyClubAttackPolicy.ActionSpent(s) && TestOnlyClubAttackPolicy.WalkingLedger(s).Remaining(30) == 30,
                    "Previous encounter Dash reused at current turn0.");
            });
            cases.Add("encounter_history_retains_closed_records_with_no_active_encounter", () => {
                var s = ArchiveFixture(); s.Encounter = null; s.InventoryCombat = false; s.InventoryTurnActor = "";
                s.EncounterDashes = new[] { new EncounterDashRecord(2, 0, TestOnlyPolicy.ActorId) };
                s.ActorMovement = s.ActorMovement.Select(a => new ActorMovementRecord(a.ActorId, 30, a.ActorId == TestOnlyPolicy.ActorId ? 0 : 1, 5)).ToArray();
                s.TacticalActors = s.TacticalActors.Select(a => new ActorTacticalRecord(a.ActorId, a.ActorId == TestOnlyPolicy.ActorId ? 0 : 1, false)).ToArray();
                Validation.Snapshot(s); Require(!FixedEncounterRules.ActionSpent(s) && s.TacticalActors.All(a => !a.ReactionAvailable), "Archiving fabricated resource refresh.");
            });
            cases.Add("encounter_history_persistence_roundtrip_preserves_absolute_deadlines", () => {
                var s = ArchiveFixture(); s.Stances = new[] { new StanceSelectionRecord(TestOnlyPolicy.ActorId, 2, 0, CombatStance.Guarded, T(6)) };
                s.Presses = new[] { new PressRecord(TestOnlyPolicy.ActorId, TestOnlyPolicy.CompanionId, 2, T(6)) };
                var codec = new SnapshotCodec(); string path = Path.Combine(directory, "encounter-archive-structural.bin"); var store = new FileSaveStore(); store.Save(path, s);
                var restored = store.Load(path); Require(codec.Encode(s).SequenceEqual(codec.Encode(restored)) && restored.ClosedEncounters[0].ClosedAt == T(3)
                    && restored.Stances[0].ExpiresAt == T(6) && restored.Presses[0].ExpiresAt == T(6), "Archive save rebased deadline or history.");
                Throws<ArgumentException>(() => new Simulation(CCPolicy(), restored, ExecutionProfile.Laboratory));
            });
            cases.Add("encounter_history_rejects_overlap_reused_id_and_future_closure", () => {
                var s = ArchiveFixture(); var first = s.ClosedEncounters[0];
                s.Encounter = new FixedEncounterRecord("encounter.second", T(4), first.Encounter.Order, new long[] { 5 }); Throws<ArgumentException>(() => Validation.Snapshot(s));
                s = ArchiveFixture(); s.Encounter = new FixedEncounterRecord("encounter.first", T(4), first.Encounter.Order, new long[] { 6 }); Throws<ArgumentException>(() => Validation.Snapshot(s));
                s = ArchiveFixture(); s.ClosedEncounters = new[] { new ClosedEncounterRecord(first.Encounter, 5, T(5), "closed") }; Throws<ArgumentException>(() => Validation.Snapshot(s));
                s = ArchiveFixture(); s.ClosedEncounters = new[] { first, first }; Throws<ArgumentException>(() => Validation.Snapshot(s));
                Throws<ArgumentException>(() => new ClosedEncounterRecord(first.Encounter, 3, T(3), "closed"));
            });
            cases.Add("encounter_history_does_not_hide_gap_or_cross_episode_pending_movement", () => {
                var s = ArchiveFixture(); s.Encounter = new FixedEncounterRecord("encounter.second", T(4), s.Encounter.Order, new long[] { 7 });
                Require(EncounterHistory.AtRevision(s, 6) == null, "Inter-encounter revision attributed to old combat.");
                s.EncounterDashes = new[] { new EncounterDashRecord(6, 0, TestOnlyPolicy.ActorId) }; Throws<ArgumentException>(() => Validation.Snapshot(s));
                s = ArchiveFixture(); s.TacticalMoves = new[] { new TacticalMoveRecord("move.old", 2, 0, 0, TestOnlyPolicy.ActorId, 0, 0, 0, 1,
                    TacticalMoveKind.Ordinary, TacticalMoveStatus.AwaitingReactions, new[] { TestOnlyPolicy.CompanionId }) };
                Throws<ArgumentException>(() => Validation.Snapshot(s));
            });
            cases.Add("encounter_history_rejects_closed_press_and_knockout_choices", () => {
                var s = ArchiveFixture(); s.TacticalMoves = new[] { new TacticalMoveRecord("move.old", 2, 4, 0, TestOnlyPolicy.ActorId, 0, 0, 0, 1,
                    TacticalMoveKind.Ordinary, TacticalMoveStatus.Completed, Array.Empty<string>(), costPaid: 5) };
                s.PressOffers = new[] { new PressOfferRecord("press.old", "move.old", TestOnlyPolicy.CompanionId, TestOnlyPolicy.ActorId, 4, 2) };
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(s));
                var live = Tactical(CCPolicy(seed: SeedForDeath(16), companionHp: 1));
                CommitTac(live, Tac(live, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId, knockout: AttackKnockoutMode.AskIfEligible));
                s = ArchiveFixture(); s.MeleeAttacks = live.Capture().MeleeAttacks;
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(s));
            });
            cases.Add("encounter_history_rejects_continuations_resolved_in_another_episode", () => {
                var s = ArchiveFixture(); s.TacticalMoves = new[] { new TacticalMoveRecord("move.old", 2, 8, 0, TestOnlyPolicy.ActorId, 0, 0, 0, 1,
                    TacticalMoveKind.Ordinary, TacticalMoveStatus.Completed, Array.Empty<string>(), costPaid: 5) };
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(s));
                s = ArchiveFixture(); s.TacticalMoves = new[] { new TacticalMoveRecord("move.old", 2, 4, 0, TestOnlyPolicy.ActorId, 0, 0, 0, 1,
                    TacticalMoveKind.Ordinary, TacticalMoveStatus.Completed, Array.Empty<string>(), costPaid: 5) };
                s.PressOffers = new[] { new PressOfferRecord("press.old", "move.old", TestOnlyPolicy.CompanionId, TestOnlyPolicy.ActorId, 4, 2, PressOfferStatus.Declined, 8) };
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(s));
                s.PressOffers = new[] { new PressOfferRecord("press.new", "move.old", TestOnlyPolicy.CompanionId, TestOnlyPolicy.ActorId, 7, 2, PressOfferStatus.Declined, 8) };
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(s));
            });
            cases.Add("encounter_history_is_explicit_bounded_and_detached", () => {
                var s = ArchiveFixture(); var copy = s.Copy(); copy.ClosedEncounters[0] = null;
                Require(s.ClosedEncounters[0] != null, "Snapshot copy shares archive array.");
                s.SchemaVersion = Snapshot.ConditionSchema; Throws<ArgumentException>(() => new SnapshotCodec().Encode(s));
                s = ArchiveFixture(); s.ClosedEncounters = Enumerable.Repeat(s.ClosedEncounters[0], EncounterHistory.MaxClosedEncounters + 1).ToArray();
                Throws<ArgumentException>(() => Validation.Snapshot(s));
            });
        }
    }
}
#endif
