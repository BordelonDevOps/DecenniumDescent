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
        private static Simulation World(TestOnlySharedWorldPolicy p = null) { p = p ?? new TestOnlySharedWorldPolicy(); return new Simulation(p, p.Initial(), ExecutionProfile.Laboratory); }
        private static void WorldCommit(Simulation s, Command c) { var result = s.Execute(TestOnlySharedWorldPolicy.Host(), c); Require(result.Outcome == Outcome.Committed, c.Kind + ": " + result.Code); }
        private static void WorldStep(Simulation s, int x, int y, bool run = false, string actor = TestOnlyPolicy.ActorId)
            => WorldCommit(s, IC(s, CommandKind.BeginWorldStep, run ? "run" : "walk", actor: actor, x: x, y: y));
        private static void WorldAdvance(Simulation s, int seconds, int denominator = 1) => WorldCommit(s, IC(s, CommandKind.AdvanceClock, x: seconds, y: denominator));
        private static WorldIntervalRecord WorldLedger(Simulation s, string actor = TestOnlyPolicy.ActorId) => s.Capture().WorldIntervals.Single(x => x.ActorId == actor);
        private static void AddSharedWorldCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("world_calendar_exact_slots_bootstrap_and_unique_markers", () => {
                var schedule = new WorldScheduleRecord("calendar.one", T(1, 3), new[] { "a", "b", "c" });
                Require(schedule.Start(1) == T(7, 3) && schedule.Start(3) == T(19, 3) && schedule.SlotAt(T(7, 3)) == 1, "Fractional origin/slot boundary changed.");
                Require(schedule.LatestStart("a", 0) == 0 && schedule.LatestStart("b", 0) == -1 && schedule.LatestStart("c", 4) == 2, "Bootstrap fabricated a pre-origin turn.");
                Require(schedule.SlotAt(T(604801)) == 302400 && schedule.LatestStart("b", 302400) == 302398, "Sparse calendar calculation wrong.");
                Require(schedule.MarkerId(0) != schedule.MarkerId(3) && schedule.MarkerId(0) != new WorldScheduleRecord("calendar.two", T(1, 3), schedule.Order).MarkerId(0), "Marker identity reused.");
                Throws<ArgumentException>(() => schedule.SlotAt(default)); Throws<ArgumentException>(() => schedule.LatestStart("missing", 1));
                Throws<ArgumentException>(() => new WorldScheduleRecord("calendar", default, new[] { "a", "a" }));
            });
            cases.Add("shared_world_explicit_profile_has_one_world_and_remote_worker", () => {
                var p = new TestOnlySharedWorldPolicy(); var s = World(p); var v = s.Capture();
                Require(v.SchemaVersion == 13 && v.Encounter == null && !v.InventoryCombat && v.WorldSchedule.Order.Count == 2
                    && !v.WorldSchedule.Order.Contains(TestOnlyPolicy.CompanionId) && v.Actors.Length == 3, "Calendar confused with encounter/expedition roster.");
                Require(v.WorldIntervals.Single(x => x.ActorId == AdditionalTacticalActor.Id).LastStart == -1 && v.WorldIntervals.All(x => x.ReactionAvailable), "Initial allowance duplicated or omitted.");
                Require(v.Work.Lots.Any(x => x.Id == TestOnlyCropPolicy.SeedLotId) && v.Vessels.Length == 3 && v.Conditions.Length == 3, "Initial shared resources missing.");
                Throws<InvalidOperationException>(() => new Simulation(p, p.Initial(), ExecutionProfile.Release));
            });
            cases.Add("shared_world_two_feet_after_point_four_seconds", () => {
                var s = World(); WorldStep(s, 1, 0); WorldAdvance(s, 2, 5); var v = s.Capture();
                Require(v.Actors.Single(a => a.Id == TestOnlyPolicy.ActorId).X == 0 && v.WorldTraversals.Single().DistanceFeet == new RuleQuantity(2)
                    && WorldLedger(s).MovementSpent == new RuleQuantity(2) && v.RuleClock == T(2, 5), "Movement snapped or rounded to a grid cell.");
                WorldAdvance(s, 3, 5); v = s.Capture();
                Require(v.WorldTraversals.Length == 0 && v.Actors.Single(a => a.Id == TestOnlyPolicy.ActorId).X == 1 && WorldLedger(s).MovementSpent == new RuleQuantity(5), "Arrival cost or position wrong.");
            });
            cases.Add("shared_world_chunked_movement_and_companion_work_agree", () => {
                var a = World(); var b = World(); foreach (var s in new[] { a, b }) { FarmWork(s, CommandKind.PlantCrop); WorldStep(s, 1, 0); }
                WorldAdvance(a, 1); for (int i = 0; i < 10; i++) WorldAdvance(b, 1, 10);
                Require(WorldLedger(a).MovementSpent == WorldLedger(b).MovementSpent && a.Capture().RuleClock == b.Capture().RuleClock
                    && Crop(a).Tasks[0].Progress == T(1) && Crop(a).Tasks[0].Progress == Crop(b).Tasks[0].Progress
                    && a.Capture().WorldTraversals.Length == 0 && b.Capture().WorldTraversals.Length == 0, "Time chunks changed work or movement.");
            });
            cases.Add("shared_world_pause_save_resume_retains_exact_partial_position", () => {
                var p = new TestOnlySharedWorldPolicy(); var s = World(p); WorldStep(s, 1, 0); WorldAdvance(s, 1, 7);
                WorldCommit(s, IC(s, CommandKind.SuspendWorldStep)); WorldAdvance(s, 30);
                var path = Path.Combine(directory, "shared-world-partial.bin"); var store = new FileSaveStore(); store.Save(path, s.Capture());
                var restored = new Simulation(p, store.Load(path), ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(restored)) && restored.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(5, 7), "Paused save lost exact position.");
                WorldCommit(restored, IC(restored, CommandKind.ResumeWorldStep)); WorldAdvance(restored, 6, 7);
                Require(restored.Capture().WorldTraversals.Length == 0 && WorldLedger(restored).MovementSpent == new RuleQuantity(30, 7), "Resume repaid previous interval or reset position.");
            });
            cases.Add("shared_world_speed_three_waits_for_real_refresh_without_banked_movement", () => {
                var s = World(new TestOnlySharedWorldPolicy(3)); WorldStep(s, 1, 0); WorldAdvance(s, 6);
                Require(s.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(3) && WorldLedger(s).LastStart == 2 && WorldLedger(s).MovementSpent == default, "Boundary did not refresh exactly once.");
                WorldAdvance(s, 4); Require(s.Capture().WorldTraversals.Length == 0 && WorldLedger(s).MovementSpent == new RuleQuantity(2), "Slow edge did not continue from three feet.");
            });
            cases.Add("shared_world_running_pays_dash_again_at_actual_start", () => {
                var s = World(new TestOnlySharedWorldPolicy(3)); WorldAdvance(s, 11, 2); WorldStep(s, 1, 0, true); WorldAdvance(s, 1);
                Require(s.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(1) && WorldLedger(s).LastStart == 2 && WorldLedger(s).DashPaid
                    && WorldLedger(s).ActionSpent && WorldLedger(s).MovementSpent == new RuleQuantity(1, 2), "Running reset distance or got free post-Start Dash.");
                WorldCommit(s, IC(s, CommandKind.SuspendWorldStep)); var before = WorldLedger(s);
                WorldCommit(s, IC(s, CommandKind.ResumeWorldStep)); Require(WorldLedger(s).LastStart == before.LastStart && WorldLedger(s).MovementSpent == before.MovementSpent, "Input resume refilled interval.");
            });
            cases.Add("shared_world_later_actor_bootstrap_refresh_is_deliberately_short", () => {
                var s = World(new TestOnlySharedWorldPolicy(3)); WorldAdvance(s, 2); WorldStep(s, 0, -1, true, AdditionalTacticalActor.Id); WorldAdvance(s, 2);
                var a = WorldLedger(s, AdditionalTacticalActor.Id);
                Require(a.LastStart == 1 && a.DashPaid && a.MovementSpent == new RuleQuantity(1) && s.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(2), "Later actor's first Start was fabricated or lost.");
            });
            cases.Add("shared_world_terrain_and_crawl_charge_exact_cost_and_elapsed_time", () => {
                var p = new TestOnlySharedWorldPolicy(30, new ConditionCombatFixture(CCApply("down", "Prone")), new TacticalTerrainCell(1, 0, TerrainCost.Difficult));
                var s = World(p); CCDispatch(s, "down"); WorldStep(s, 1, 0); WorldAdvance(s, 1);
                Require(s.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(5, 3) && WorldLedger(s).MovementSpent == new RuleQuantity(5), "Terrain/crawl arithmetic lost fraction.");
                WorldAdvance(s, 2); Require(s.Capture().WorldTraversals.Length == 0 && WorldLedger(s).MovementSpent == new RuleQuantity(15), "Terrain/crawl arrival cost wrong.");
            });
            cases.Add("shared_world_immunity_expiry_stops_at_actual_two_foot_position", () => {
                var cure = new ConditionFixtureEvent(TestOnlyPolicy.ActorId, ConditionOperation.Cure("event.cure", new ConditionStamp(T(1)), "Stunned"));
                var p = new TestOnlySharedWorldPolicy(30, new ConditionCombatFixture(CCApply("stun", "Stunned"), CCGrant("ward", TestOnlyPolicy.ActorId, new ConditionStamp(T(2, 5)), "Stunned"), cure));
                var s = World(p); CCDispatch(s, "stun"); CCDispatch(s, "ward"); WorldStep(s, 1, 0); WorldAdvance(s, 1);
                var edge = s.Capture().WorldTraversals.Single(); Require(edge.DistanceFeet == new RuleQuantity(2) && edge.Status == WorldTraversalStatus.Suspended && WorldLedger(s).MovementSpent == new RuleQuantity(2), "Deadline over-credited movement.");
                CCDispatch(s, "cure"); Require(s.Capture().WorldTraversals.Single().Status == WorldTraversalStatus.Suspended, "Condition ending automatically resumed input.");
                WorldCommit(s, IC(s, CommandKind.ResumeWorldStep)); WorldAdvance(s, 3, 5); Require(s.Capture().WorldTraversals.Length == 0, "Explicit resume failed.");
            });
            cases.Add("shared_world_partial_interactions_and_unsupported_physical_drop_reject_without_snap", () => {
                var p = new TestOnlySharedWorldPolicy(30, new ConditionCombatFixture(CCApply("sleep", "Unconscious", at: new ConditionStamp(T(2, 5)))));
                var s = World(p); WorldStep(s, 1, 0); WorldAdvance(s, 2, 5);
                RejectUnchanged(s, host, IC(s, CommandKind.StartIntake, TestOnlyInventoryPolicy.FoodId, new InventoryRequest(new RuleQuantity(1))), "TraversalRequiresStationaryInteraction");
                RejectUnchanged(s, host, CCCommand(s, "sleep"), "OffGridPhysicalConsequenceUnsupported");
                RejectUnchanged(s, host, IC(s, CommandKind.Move, x: 1), "UseWorldTraversal");
                RejectUnchanged(s, host, IC(s, CommandKind.BeginFixedEncounter), "SharedCommandNotImplemented");
            });
            cases.Add("shared_world_world_authority_duplicates_and_release_gate", () => {
                var s = World(); var c = IC(s, CommandKind.BeginWorldStep, "walk", x: 1); WorldCommit(s, c); byte[] bytes = Bytes(s);
                Require(s.Execute(host, c).Outcome == Outcome.Duplicate && bytes.SequenceEqual(Bytes(s)), "Duplicate repeated movement start.");
                RejectUnchanged(s, new Authority(host.Principal, Array.Empty<string>()), c, "NotAuthorized");
                RejectUnchanged(s, new Authority("guest", new[] { TestOnlyPolicy.ActorId }), IC(s, CommandKind.AdvanceClock, x: 1, y: 1), "NotAuthorized");
                RejectUnchanged(s, host, IC(s, CommandKind.BeginWorldStep, "walk", actor: TestOnlyPolicy.CompanionId, x: 1), "NoActivityCalendar");
            });
            cases.Add("shared_world_week_calendar_is_sparse_and_farm_harvest_is_real", () => {
                var s = World(); Mature(s); FarmWork(s, CommandKind.HarvestCrop); WorldAdvance(s, 3600); var v = s.Capture();
                Require(v.RuleClock == T(612000) && v.WorldSchedule.ProcessedSlot == 204000 && v.WorldIntervals.Length == 2 && v.Encounter == null
                    && v.LifeEvents.Length == 0 && v.Conditions.All(x => x.Operations.Count < 40), "Farming week expanded empty virtual-turn history.");
                Require(v.CropFood.Length == 1 && v.Work.Lots.Single(x => x.Id == v.CropFood[0].LotId).Amount == new RuleQuantity(8), "Shared host failed actual seven-day harvest.");
                Require(v.WorldIntervals.All(x => !x.ActionSpent && x.MovementSpent == default), "Skipped intervals banked spending or retained expired budget.");
            });
            cases.Add("shared_world_companion_condition_pauses_crop_and_requires_explicit_resume", () => {
                var p = new TestOnlySharedWorldPolicy(30, new ConditionCombatFixture(CCApply("stun", "Stunned", TestOnlyPolicy.CompanionId, new ConditionStamp(T(20)), new ConditionStamp(T(10)))));
                var s = World(p); FarmWork(s, CommandKind.PlantCrop); WorldAdvance(s, 10); CCDispatch(s, "stun", TestOnlyPolicy.CompanionId); WorldAdvance(s, 20);
                Require(Crop(s).Tasks[0].Status == CropWorkStatus.Paused && Crop(s).Tasks[0].Progress == T(10)
                    && s.Capture().Work.Lots.Single(x => x.Id == TestOnlyCropPolicy.SeedLotId).Quantity == 7, "Interruption refunded input or continued labor.");
                FarmWork(s, CommandKind.PlantCrop); WorldAdvance(s, 3590); Require(Crop(s).Stage == CropStage.Growing, "Explicit planting resume failed.");
            });
            cases.Add("shared_world_pause_filling_keeps_progress_reservations_and_intake_consumption", () => {
                var p = new TestOnlySharedWorldPolicy(30, new ConditionCombatFixture(CCApply("stun", "Stunned", TestOnlyPolicy.CompanionId, new ConditionStamp(T(20)), new ConditionStamp(T(10)))));
                var s = World(p); WorldCommit(s, IC(s, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId, new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), TestOnlyPolicy.CompanionId));
                Eat(s, new RuleQuantity(1)); WorldAdvance(s, 10); CCDispatch(s, "stun", TestOnlyPolicy.CompanionId); WorldAdvance(s, 20);
                var v = s.Capture(); Require(v.WaterFills.Single().Status == WaterFillStatus.Paused && v.WaterFills.Single().Progress == T(10)
                    && Eaten(s) == new RuleQuantity(1, 30) && WaterFilling.FreeCapacity(v, TestOnlyFillingPolicy.FlaskId) == default, "Paused fill leaked capacity, work or interrupted other actor's intake.");
                WorldCommit(s, IC(s, CommandKind.ResumeWaterFill, v.WaterFills.Single().Id, actor: TestOnlyPolicy.CompanionId)); WorldAdvance(s, 50);
                Require(s.Capture().WaterFills.Single().Status == WaterFillStatus.Complete, "Stable fill did not resume retained progress.");
            });
            cases.Add("shared_world_replay_rejects_forged_position_budget_calendar_and_crop_progress", () => {
                var p = new TestOnlySharedWorldPolicy(); var s = World(p); FarmWork(s, CommandKind.PlantCrop); WorldStep(s, 1, 0); WorldAdvance(s, 2, 5);
                var v = s.Capture(); v.WorldTraversals = new[] { v.WorldTraversals[0].With(new RuleQuantity(3), WorldTraversalStatus.Moving) };
                Throws<ArgumentException>(() => new Simulation(p, v, ExecutionProfile.Laboratory));
                v = s.Capture(); v.WorldIntervals = v.WorldIntervals.Select(x => new WorldIntervalRecord(x.ActorId, x.LastStart)).ToArray(); Throws<ArgumentException>(() => new Simulation(p, v, ExecutionProfile.Laboratory));
                v = s.Capture(); v.WorldSchedule = v.WorldSchedule.At(2); Throws<ArgumentException>(() => new SnapshotCodec().Encode(v));
                v = s.Capture(); v.Crops = Array.Empty<CropBatchRecord>(); Throws<ArgumentException>(() => new Simulation(p, v, ExecutionProfile.Laboratory));
                v = s.Capture(); v.WorldSchedule = new WorldScheduleRecord("forged-calendar", default, v.WorldSchedule.Order); Throws<ArgumentException>(() => new Simulation(p, v, ExecutionProfile.Laboratory));
            });
            cases.Add("shared_world_forged_consumption_and_paused_save_are_replay_checked", () => {
                var p = new TestOnlySharedWorldPolicy(); var s = World(p); Eat(s, new RuleQuantity(1)); WorldAdvance(s, 90);
                var path = Path.Combine(directory, "shared-world-intake.bin"); new FileSaveStore().Save(path, s.Capture());
                var loaded = new FileSaveStore().Load(path); new Simulation(p, loaded, ExecutionProfile.Laboratory);
                loaded.Intakes = Array.Empty<IntakeRecord>(); Throws<ArgumentException>(() => new Simulation(p, loaded, ExecutionProfile.Laboratory));
                var copy = s.Capture(); copy.WorldIntervals[0] = null; Require(s.Capture().WorldIntervals.All(x => x != null), "Snapshot shares writable world array.");
            });
            cases.Add("shared_world_explore_grow_harvest_acquire_eat_explore_loop", () => {
                var p = new TestOnlySharedWorldPolicy(); var s = World(p); FarmWork(s, CommandKind.PlantCrop);
                foreach (var step in new[] { new[] { 1, 0 }, new[] { 1, 0 }, new[] { 1, 0 }, new[] { 0, 1 }, new[] { 0, 1 } }) { WorldStep(s, step[0], step[1]); WorldAdvance(s, 1); }
                Require(Crop(s).Tasks[0].Progress == T(5), "Direct exploration stopped remote planting.");
                FarmUntil(s, T(3600));
                for (int day = 0; day < 6; day++) { FarmUntil(s, FarmDifference(Crop(s).CareUntil.Value, T(900))); FarmWork(s, CommandKind.TendCrop); FarmAdvance(s, 900); }
                FarmUntil(s, T(608400)); FarmWork(s, CommandKind.HarvestCrop); WorldAdvance(s, 3600);
                string food = s.Capture().CropFood.Single().LotId;
                string portion = HandleI(s, food, new RuleQuantity(2, 3), HandlingKind.Pickup);
                Eat(s, new RuleQuantity(2, 3), portion); WorldAdvance(s, 600);
                var save = Path.Combine(directory, "shared-world-expedition-loop.bin"); new FileSaveStore().Save(save, s.Capture());
                s = new Simulation(p, new FileSaveStore().Load(save), ExecutionProfile.Laboratory);
                Require(Eaten(s) == new RuleQuantity(2, 3) && s.Capture().InventoryLots.Single(x => x.LotId == portion).OwnerId == TestOnlyPolicy.CompanionId,
                    "Acquisition lost original owner or intake credit.");
                WorldStep(s, -1, 0); WorldAdvance(s, 1); Require(s.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 2, "Exploration did not continue after management/save.");
            });
            cases.Add("shared_world_handling_cannot_skip_condition_deadline_or_moving_recipient", () => {
                var p = new TestOnlySharedWorldPolicy(30, new ConditionCombatFixture(CCApply("blind", "Blinded", expires: new ConditionStamp(T(1, 2)))));
                var s = World(p); CCDispatch(s, "blind");
                RejectUnchanged(s, host, IC(s, CommandKind.HandleInventory, TestOnlyInventoryPolicy.FoodId, new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Stow)), "TimedHandlingBoundaryUnsupported");
                WorldAdvance(s, 1); WorldStep(s, 1, 0);
                RejectUnchanged(s, host, IC(s, CommandKind.HandleVessel, TestOnlyFillingPolicy.FlaskId, new InventoryRequest(new RuleQuantity(1)), TestOnlyPolicy.CompanionId), "ConcurrentTraversalHandlingUnsupported");
            });
            cases.Add("shared_world_boundary_refresh_does_not_automatically_resume_suspended_run", () => {
                var p = new TestOnlySharedWorldPolicy(3, new ConditionCombatFixture(CCApply("daze", "Dazed", expires: new ConditionStamp(T(7)), at: new ConditionStamp(T(11, 2)))));
                var s = World(p); WorldAdvance(s, 5); WorldStep(s, 1, 0, true); WorldAdvance(s, 1, 2); CCDispatch(s, "daze"); WorldAdvance(s, 3);
                Require(s.Capture().WorldTraversals.Single().Status == WorldTraversalStatus.Suspended && s.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(1, 2)
                    && !WorldLedger(s).DashPaid, "Run silently resumed or got free speed at new Start.");
                WorldCommit(s, IC(s, CommandKind.ResumeWorldStep)); Require(WorldLedger(s).DashPaid, "Explicit resumed run did not pay current Dash.");
            });
            cases.Add("shared_world_records_reject_missing_calendar_invalid_edges_and_invalid_spending", () => {
                var s = World().Capture(); s.SchemaVersion = Snapshot.ConditionSchema; Throws<ArgumentException>(() => Validation.Snapshot(s));
                s = World().Capture(); s.WorldSchedule = null; Throws<ArgumentException>(() => Validation.Snapshot(s));
                Throws<ArgumentException>(() => new WorldIntervalRecord("a", 0, dashPaid: true));
                Throws<ArgumentException>(() => new WorldIntervalRecord("a", 0, actionSpent: true, dashPaid: true, interactions: 2));
                Throws<ArgumentException>(() => new WorldTraversalRecord("a", 1, 0, 0, 1, 1));
                Throws<ArgumentException>(() => new WorldTraversalRecord("a", 1, 0, 0, 1, 0, new RuleQuantity(5)));
            });
            cases.Add("shared_world_simultaneous_hostile_edges_cannot_bypass_combat_boundary", () => {
                var s = World();
                foreach (var delta in new[] { new[] { 0, -1 }, new[] { 0, -1 }, new[] { -1, 0 } }) { WorldStep(s, delta[0], delta[1], actor: AdditionalTacticalActor.Id); WorldAdvance(s, 1); }
                WorldStep(s, 1, 0); WorldAdvance(s, 1); WorldStep(s, 0, 1);
                RejectUnchanged(s, host, IC(s, CommandKind.BeginWorldStep, "walk", actor: AdditionalTacticalActor.Id, x: -1), "ConcurrentHostileTraversalUnsupported");
                WorldAdvance(s, 1);
                RejectUnchanged(s, host, IC(s, CommandKind.BeginWorldStep, "walk", actor: AdditionalTacticalActor.Id, x: -1), "TacticalTransitionRequired");
            });
            cases.Add("shared_world_filling_requires_actual_two_free_hands", () => {
                var s = World(); var v = s.Capture();
                Require(v.Lives.Single(x => x.ActorId == TestOnlyPolicy.CompanionId).HeldItems.Count == 0 && v.Clubs.Single(x => x.Id == TestOnlyClubAttackPolicy.CompanionClub).HeldBy == "", "Remote worker still holds Club while claiming two free hands.");
                RejectUnchanged(s, host, IC(s, CommandKind.StartWaterFill, TestOnlyInventoryPolicy.WaterId, new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.ActorSkinId)), "TwoHandsRequired");
                WorldCommit(s, IC(s, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId, new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), TestOnlyPolicy.CompanionId));
                Require(s.Capture().WaterFills.Length == 1, "Actually empty-handed companion cannot fill.");
            });
        }
    }
}
#endif
