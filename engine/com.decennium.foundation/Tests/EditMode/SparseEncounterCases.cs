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
        private static void AddSparseEncounterCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("sparse_encounter_day_seven_cursor_does_not_invent_start_commands", () => {
                var e = new FixedEncounterRecord("encounter.sparse", default, new[] { "a", "b" }, new long[] { 25, 28 }, new[] { 204000, 204001 });
                Require(e.TurnOrdinal == 204001 && e.CurrentActor == "b" && e.Round == 102001 && e.StartRevisions.Count == 2
                    && e.CurrentTurnId == "encounter.sparse.turn.204001" && FixedEncounterRules.Start(e, e.TurnOrdinal) == T(612003), "Sparse calendar cursor uses command count.");
                Require(EncounterHistory.MatchesTurn(e, 204000, "a") && !EncounterHistory.MatchesTurn(e, 0, "a") && !EncounterHistory.MatchesTurn(e, 204002, "a"), "Unobserved cursor accepted as action history.");
            });
            cases.Add("sparse_encounter_ordinals_are_explicit_ordered_and_bounded", () => {
                string[] order = { "a", "b" }; long[] revisions = { 1, 2 };
                foreach (var ordinals in new[] { new[] { -1, 2 }, new[] { 3, 3 }, new[] { 3, 2 }, new[] { 1 } })
                    Throws<ArgumentException>(() => new FixedEncounterRecord("encounter.sparse", default, order, revisions, ordinals));
                var source = new[] { 204000, 204002 }; var e = new FixedEncounterRecord("encounter.sparse", default, order, revisions, source); source[1] = 0;
                Require(e.TurnOrdinal == 204002 && e.CurrentActor == "a", "Caller mutated persisted ordinal collection.");
                var last = new FixedEncounterRecord("last", default, new[] { "a" }, new long[] { 1 }, new[] { int.MaxValue }); Require(last.Round == (long)int.MaxValue + 1, "Round arithmetic overflowed.");
            });
            cases.Add("sparse_encounter_schema14_roundtrips_without_reinterpreting_legacy_schema", () => {
                var s = ArchiveFixture(); s.SchemaVersion = Snapshot.CalendarCombatSchema; s.RuleClock = T(612003);
                s.Encounter = new FixedEncounterRecord("encounter.second", T(4), s.Encounter.Order, new long[] { 6, 7 }, new[] { 203998, 203999 });
                s.InventoryTurnActor = TestOnlyPolicy.CompanionId;
                s.Conditions = s.Conditions.Select(x => new ConditionJournal(ConditionHistory.PolicyId, x.Target, new ConditionStamp(s.RuleClock))).ToArray();
                s.ActorMovement = s.ActorMovement.Select(x => new ActorMovementRecord(x.ActorId, x.BaseWalkingSpeed)).ToArray();
                s.TacticalActors = s.TacticalActors.Select(x => new ActorTacticalRecord(x.ActorId)).ToArray();
                var path = Path.Combine(directory, "sparse-encounter-structural.bin"); new FileSaveStore().Save(path, s); var restored = new FileSaveStore().Load(path);
                Require(new SnapshotCodec().Encode(s).SequenceEqual(new SnapshotCodec().Encode(restored)) && restored.Encounter.ObservedOrdinals.SequenceEqual(new[] { 203998, 203999 }), "Sparse cursor lost on disk.");
                s.SchemaVersion = Snapshot.SharedWorldSchema; Throws<ArgumentException>(() => new SnapshotCodec().Encode(s));
                Throws<ArgumentException>(() => new Simulation(new TestOnlySharedWorldPolicy(), restored, ExecutionProfile.Laboratory));
            });
            cases.Add("sparse_encounter_latest_observed_actor_start_uses_slot_not_array_index", () => {
                var s = ArchiveFixture(); s.SchemaVersion = Snapshot.CalendarCombatSchema;
                s.Encounter = new FixedEncounterRecord("encounter.second", T(4), s.Encounter.Order, new long[] { 6, 7, 8 }, new[] { 204000, 204003, 204006 });
                Require(EncounterHistory.LatestStartOrdinal(s, TestOnlyPolicy.ActorId) == 204006 && EncounterHistory.LatestStartOrdinal(s, TestOnlyPolicy.CompanionId) == 204003,
                    "Sparse observation index mistaken for actor's real slot ordinal.");
            });
        }
    }
}
#endif
