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
        private static TestOnlySharedWorldPolicy CraftPolicy(SharedCraftingFixture facts, uint seed = 1, SharedResearchFixture research = null, ConditionCombatFixture conditions = null)
            => new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed), research, facts, conditions: conditions);
        private static Command CraftCommand(Simulation s, string id, CommandKind kind = CommandKind.DispatchCraftingMishap, string actor = TestOnlyPolicy.CompanionId)
            => new Command("craft-command." + (s.Capture().Revision + 1), actor, s.Capture().Revision, kind, id);
        private static void CraftEvent(Simulation s, string id, string actor = TestOnlyPolicy.CompanionId) => WorldCommit(s, CraftCommand(s, id, actor: actor));
        private static void Remedy(Simulation s, string id, string actor = TestOnlyPolicy.CompanionId, bool pause = false)
            => WorldCommit(s, CraftCommand(s, id, pause ? CommandKind.PauseCraftRemedy : CommandKind.StartCraftRemedy, actor));
        private static CraftingIncidentRecord Incident(Simulation s, string id) => s.Capture().CraftingIncidents.Single(x => x.Id == id);
        private static readonly Dictionary<string, uint> MishapSeeds = new Dictionary<string, uint>();
        private static uint MishapSeed(int woundNatural, params int[] saves)
        {
            string key = woundNatural + ":" + string.Join(",", saves); if (MishapSeeds.TryGetValue(key, out uint cached)) return cached;
            for (uint seed = 1; seed < 2000000; seed++) {
                var d4 = DiceStream.Draw(seed, 4); var damage = PlaytestDamageDice.Resolve(new LifeState(26, 1), d4.Value + 1, default, d4.NextState);
                if (damage.WoundRoll.Natural != woundNatural) continue;
                uint next = damage.NextRandomState; bool matches = true;
                foreach (int natural in saves) { var d = PlaytestDice.RollD20(next); next = d.NextRandomState; if (d.Natural != natural) { matches = false; break; } }
                if (matches) { MishapSeeds.Add(key, seed); return seed; }
            }
            throw new Exception("No crafting fixture seed.");
        }
        private static void HeroToWorkshop(Simulation s)
        {
            // The arena's central wall requires the western/southern path; no relocation fixture.
            foreach (var step in new[] { (0, 1), (0, 1), (0, 1), (1, 0), (1, 0) }) { WorldStep(s, step.Item1, step.Item2); WorldAdvance(s, 1); }
        }
        private static void AddCraftingConsequenceCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host(); const string hero = TestOnlyPolicy.ActorId, worker = TestOnlyPolicy.CompanionId;
            cases.Add("crafting_consequence_schema16_explicit_authority_and_idempotency", () => {
                var p = CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("spill", 1) })); var s = World(p);
                Require(s.Capture().SchemaVersion == 16 && ResearchPolicy().Initial().SchemaVersion == 15, "Consequence opt-in changed prior schema.");
                Throws<InvalidOperationException>(() => new Simulation(p, p.Initial(), ExecutionProfile.Release));
                var c = CraftCommand(s, "spill"); var guest = new Authority("guest", new[] { worker }); RejectUnchanged(s, guest, c, "NotAuthorized");
                WorldCommit(s, c); byte[] bytes = Bytes(s); Require(s.Execute(host, c).Outcome == Outcome.Duplicate && Bytes(s).SequenceEqual(bytes), "Duplicate repeated mishap.");
                RejectUnchanged(s, guest, c, "NotAuthorized"); RejectUnchanged(s, host, CraftCommand(s, "spill"), "CraftingMishapAlreadyResolved");
                RejectUnchanged(s, host, CraftCommand(s, "arbitrary-damage"), "UnknownCraftingMishap");
            });
            cases.Add("crafting_accident_fixed_actor_zero_hp_drops_and_falls_without_encounter", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(heroHp: 1, events: new[] { new CraftingMishapFact("acid", 4, hero) }), MishapSeed(2)));
                CraftEvent(s, "acid", hero); var v = s.Capture();
                Require(v.Encounter == null && !v.InventoryCombat && Life(s).Hp == 0 && Life(s).LinkedInjuries.Count == 1 && Life(s).Prone
                    && Life(s).HeldItems.Count == 0 && v.Clubs.Single(x => x.Id == TestOnlyClubAttackPolicy.ActorClub).HeldBy == ""
                    && v.DyingCadences.Length == 0 && v.MeleeAttacks.Length == 0 && Incident(s, "acid").InjuryD6 != 0, "Accident invented combat/KO or missed Wound/drop/prone.");
                WorldAdvance(s, 5); Require(s.Capture().LifeEvents.Length == 0, "Scheduled actor received an immediate or another actor's save.");
                WorldAdvance(s, 1); Require(s.Capture().LifeEvents.Single().At == T(6) && s.Capture().LifeEvents.Single().TurnOrdinal == 2, "Fixed calendar Start was not used outside encounter.");
            });
            cases.Add("crafting_accident_remote_dying_disk_resume_processes_exact_marker_once", () => {
                var p = CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4, at: T(1, 3)) }), MishapSeed(10, 12));
                var s = World(p); WorldAdvance(s, 1, 3); CraftEvent(s, "acid"); WorldAdvance(s, 5);
                Require(s.Capture().DyingCadences.Single().NextAt == T(19, 3) && s.Capture().LifeEvents.Length == 0, "Fallback cadence rounded or started early.");
                string path = Path.Combine(directory, "craft-dying.bin"); var store = new FileSaveStore(); store.Save(path, s.Capture()); var restored = new Simulation(p, store.Load(path), ExecutionProfile.Laboratory);
                WorldAdvance(s, 1); WorldAdvance(restored, 1); Require(Bytes(s).SequenceEqual(Bytes(restored)), "Dying continuation diverged after disk restore.");
                var e = s.Capture().LifeEvents.Single(); Require(e.ActorId == worker && e.At == T(19, 3) && e.TurnOrdinal == -1 && e.Natural == 12
                    && Life(s, worker).LastDeathTurn == 1 && s.Capture().DyingCadences.Single().NextAt == T(37, 3), "Fallback saved the wrong actor/time or lost cursor.");
                s = new Simulation(p, new SnapshotCodec().Decode(Bytes(s)), ExecutionProfile.Laboratory); WorldAdvance(s, 1, 10); Require(s.Capture().LifeEvents.Length == 1, "Reload repeated a processed marker.");
            });
            cases.Add("crafting_dying_mode_entry_does_not_create_competing_series", () => {
                var p = CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4) }), MishapSeed(10, 12)); var s = World(p); CraftEvent(s, "acid");
                WorldAdvance(s, 1); BeginEncounter(s); ConnectedEnd(s); ConnectedEnd(s);
                Require(s.Capture().RuleClock == T(6) && s.Capture().LifeEvents.Single().ActorId == worker && s.Capture().LifeEvents.Single().At == T(6)
                    && s.Capture().DyingCadences.Single().NextAt == T(12), "Tactical entry retimed remote dying or duplicated a save.");
            });
            cases.Add("crafting_remote_dying_natural20_restores_hp_without_auto_resuming_work", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4, at: T(10)) }), MishapSeed(10, 20), new SharedResearchFixture()));
                ResearchStart(s); WorldAdvance(s, 10); CraftEvent(s, "acid"); WorldAdvance(s, 6);
                Require(Life(s, worker).Hp == 1 && Life(s, worker).Prone && s.Capture().DyingCadences.Length == 0 && ResearchJob(s).Status == FormulaWorkStatus.Paused
                    && ResearchJob(s).Work.Labor == T(10), "Death-save healing stood actor or resumed work.");
                ResearchControl(s, CommandKind.ResumeFormulaWork); WorldAdvance(s, 1); Require(ResearchJob(s).Work.Labor == T(11), "Recovered worker could not explicitly resume earned work.");
            });
            cases.Add("crafting_remote_three_successes_stable_deadline_recovers_once", () => {
                var p = CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4) }), MishapSeed(10, 10, 10, 10)); var s = World(p); CraftEvent(s, "acid"); WorldAdvance(s, 18);
                var life = Life(s, worker); Require(life.Stable && life.StableUntil.HasValue && s.Capture().DyingCadences.Length == 0 && s.Capture().LifeEvents.Length == 3, "Third success did not stop dying cadence.");
                Require(life.StableUntil.Value.Denominator == 1, "Expected integral recovery deadline."); WorldAdvance(s, checked((int)life.StableUntil.Value.Numerator - 19));
                Require(Life(s, worker).Hp == 0, "Stable recovery occurred early.");
                s = new Simulation(p, new SnapshotCodec().Decode(Bytes(s)), ExecutionProfile.Laboratory); WorldAdvance(s, 1); WorldAdvance(s, 6);
                Require(Life(s, worker).Hp == 1 && s.Capture().LifeEvents.Count(x => x.Kind == LifeEventKind.StableRecovery) == 1 && s.Capture().LifeEvents.Count(x => x.Kind == LifeEventKind.DeathSave) == 3, "Stable recovery duplicated or kept death saves.");
            });
            cases.Add("crafting_remote_three_failures_die_and_stop_future_randomness", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4) }), MishapSeed(10, 2, 2, 2))); CraftEvent(s, "acid"); WorldAdvance(s, 18);
                uint rng = s.Capture().RandomState; WorldAdvance(s, 1000);
                Require(Life(s, worker).Dead && s.Capture().DyingCadences.Length == 0 && s.Capture().LifeEvents.Length == 3 && s.Capture().RandomState == rng, "Dead actor kept receiving saves.");
            });
            cases.Add("crafting_accident_petrified_defense_applies_before_zero_hp", () => {
                uint seed = 1; while (DiceStream.Draw(seed, 4).Value != 0) seed++;
                var p = CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4) }), seed,
                    conditions: new ConditionCombatFixture(CCApply("stone", "Petrified", worker))); var s = World(p); CCDispatch(s, "stone", worker); CraftEvent(s, "acid");
                Require(Incident(s, "acid").InjuryD4 == 1 && Incident(s, "acid").Damage == 0 && Incident(s, "acid").WoundD20 == 0 && Life(s, worker).Hp == 1 && s.Capture().DyingCadences.Length == 0, "Accident bypassed actual resistance or rolled unnecessary Wound.");
            });
            cases.Add("crafting_accident_pauses_crop_fill_and_retains_their_contracts", () => {
                foreach (bool filling in new[] { false, true }) {
                    var s = World(CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4, at: T(10)) }), MishapSeed(10)));
                    if (filling) WorldCommit(s, IC(s, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId, new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), worker));
                    else FarmWork(s, CommandKind.PlantCrop);
                    WorldAdvance(s, 10); CraftEvent(s, "acid");
                    if (filling) Require(s.Capture().WaterFills.Single().Status == WaterFillStatus.Paused && s.Capture().WaterFills.Single().Progress == T(10), "Injury lost water-fill progress/reservations.");
                    else Require(Crop(s).Tasks.Single().Status == CropWorkStatus.Paused && Crop(s).Tasks.Single().Progress == T(10), "Injury erased crop work.");
                }
            });
            cases.Add("crafting_tool_damage_retains_broken_object_identity_mass_and_custody", () => {
                var p = CraftPolicy(new SharedCraftingFixture(toolHp: 1, events: new[] { new CraftingMishapFact("break", 3) }), research: new SharedResearchFixture()); var s = World(p); var before = s.Capture().Structures.Single(); CraftEvent(s, "break");
                var after = s.Capture().Structures.Single(); Require(after.Broken && after.Id == before.Id && after.OwnerId == before.OwnerId && after.CustodianId == before.CustodianId
                    && after.LocationId == before.LocationId && after.MassPounds == new RuleQuantity(8) && Incident(s, "break").Result == 3 && s.Capture().RandomState == 1, "Tool damage destroyed property or rolled an attack/fallback.");
                string path = Path.Combine(directory, "craft-broken-kit.bin"); new FileSaveStore().Save(path, s.Capture()); s = new Simulation(p, new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                RejectUnchanged(s, host, ResearchCommand(s), "ResearchToolsOrStationUnavailable"); WorldAdvance(s, 3600); Require(s.Capture().Structures.Single().Broken, "Elapsed time repaired tool.");
            });
            cases.Add("ordinary_tool_structure_material_immunity_compatibility_and_repair_math", () => {
                var kit = CraftPolicy(new SharedCraftingFixture()).Initial().Structures.Single();
                Require(ObjectStructureRules.MaterialAc(kit.Material) == 15 && ObjectStructureRules.MaterialAc(ObjectMaterial.IronSteel) == 19, "Material table changed.");
                foreach (var kind in new[] { StructuralDamageKind.Poison, StructuralDamageKind.Psychic }) Require(ObjectStructureRules.Damage(kit, 99, kind, true).Hp == 5, "Ordinary immunity missing.");
                Require(ObjectStructureRules.Damage(kit, 1, StructuralDamageKind.Bludgeoning, false).Hp == 5 && ObjectStructureRules.Damage(kit, 1, StructuralDamageKind.Bludgeoning, true).Hp == 4, "Compatibility or direct point resolution changed.");
                Require(ObjectStructureRules.RepairMaterialsCopper(kit) == new RuleQuantity(1250) && ObjectStructureRules.RepairLabor(kit) == T(3600)
                    && ObjectStructureRules.RepairSucceeds(8, 2) && !ObjectStructureRules.RepairSucceeds(7, 2), "Ordinary kit repair quantities/check wrong.");
            });
            cases.Add("crafting_spill_blocks_station_work_but_cleanup_reopens_it_once", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("spill", 1, at: T(10)) }), research: new SharedResearchFixture()));
                ResearchStart(s); WorldAdvance(s, 10); CraftEvent(s, "spill"); Require(ResearchJob(s).Status == FormulaWorkStatus.Paused, "Spilled station continued research.");
                RejectUnchanged(s, host, ResearchCommand(s, CommandKind.ResumeFormulaWork, ResearchJob(s).Id), "ResearchToolsOrStationUnavailable");
                Remedy(s, "spill"); WorldAdvance(s, 3599); Require(CraftingRestrictions.StationUseBlocked(s.Capture(), SharedCraftingFixture.StationId), "Cleanup cleared early.");
                WorldAdvance(s, 1); Require(Incident(s, "spill").Remedied && !CraftingRestrictions.StationUseBlocked(s.Capture(), SharedCraftingFixture.StationId) && ResearchJob(s).Status == FormulaWorkStatus.Paused, "Cleanup resumed unrelated work.");
                ResearchControl(s, CommandKind.ResumeFormulaWork); RejectUnchanged(s, host, CraftCommand(s, "spill", CommandKind.StartCraftRemedy), "CraftingRemedyComplete");
            });
            cases.Add("crafting_miscalibration_blocks_check_only_and_requires_proficiency", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("calibrate", 2) }), research: new SharedResearchFixture())); CraftEvent(s, "calibrate");
                Require(CraftingRestrictions.CraftingCheckBlocked(s.Capture(), SharedCraftingFixture.ToolId) && !CraftingRestrictions.NewOrderBlocked(s.Capture(), worker, SharedCraftingFixture.StationId, "Alchemy"), "Miscalibration became a universal prohibition.");
                ResearchStart(s); ResearchControl(s, CommandKind.PauseFormulaWork); HeroToWorkshop(s);
                RejectUnchanged(s, host, CraftCommand(s, "calibrate", CommandKind.StartCraftRemedy, hero), "CraftRemedyWorkerIneligible");
                Remedy(s, "calibrate"); WorldAdvance(s, 7200); Require(!CraftingRestrictions.CraftingCheckBlocked(s.Capture(), SharedCraftingFixture.ToolId) && s.Capture().Structures.Single().Hp == 5, "Recalibration failed or spent structural HP.");
            });
            cases.Add("crafting_remediation_pause_disk_resume_retains_exact_labor", () => {
                var p = CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("spill", 1) })); var s = World(p); CraftEvent(s, "spill"); Remedy(s, "spill"); WorldAdvance(s, 1, 3); Remedy(s, "spill", pause: true); WorldAdvance(s, 100);
                var path = Path.Combine(directory, "craft-remedy.bin"); new FileSaveStore().Save(path, s.Capture()); s = new Simulation(p, new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                Require(Incident(s, "spill").Labor == T(1, 3) && Incident(s, "spill").Workers.Count == 0, "Paused cleanup earned time or lost fractions.");
                Remedy(s, "spill"); WorldAdvance(s, 10799, 3); Require(Incident(s, "spill").Remedied && Incident(s, "spill").Labor == T(3600), "Resumed cleanup failed exact completion.");
            });
#if HEADLESS_TESTS
            cases.Add("crafting_default_fingerprint_restores_and_continues_authentic_schema16_save", () => {
                var root=new DirectoryInfo(Environment.CurrentDirectory);
                while(root!=null&&!Directory.Exists(Path.Combine(root.FullName,"docs","unity","evidence")))root=root.Parent;
                Require(root!=null,"Could not locate the repository root for the pinned historical fixture.");
                var path=Path.Combine(root.FullName,"docs","unity","evidence","2026-11-09-mgt04-recipe347",
                    "historical-schema16","craft-remedy.bin");
                byte[] bytes=File.ReadAllBytes(path);var codec=new SnapshotCodec();var saved=codec.Decode(bytes);
                var policy=CraftPolicy(new SharedCraftingFixture(events:new[]{new CraftingMishapFact("spill",1)}));
                Require(saved.SchemaVersion==Snapshot.CraftingConsequenceSchema
                    &&saved.ContentFingerprint==policy.Initial().ContentFingerprint,
                    "The authentic pre-increment schema16 save lost its supported default content fingerprint. saved="
                    +saved.ContentFingerprint+" current="+policy.Initial().ContentFingerprint);
                var customPolicy=CraftPolicy(new SharedCraftingFixture(events:new[]{new CraftingMishapFact("spill",1,
                    toolId:"TEST_ONLY.custom.tool",stationId:"TEST_ONLY.custom.station",tradeId:"Mining")}));
                Require(saved.ContentFingerprint!=customPolicy.Initial().ContentFingerprint,
                    "Versioned custom mishap targets must produce distinct content fingerprints.");
                var simulation=new Simulation(policy,saved,ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(simulation))&&Incident(simulation,"spill").Labor==T(1,3)
                    &&Incident(simulation,"spill").Workers.Count==0,
                    "The authentic paused schema16 cleanup did not restore byte-identically with exact retained labor.");
                Remedy(simulation,"spill");WorldAdvance(simulation,10799,3);
                Require(Incident(simulation,"spill").Remedied&&Incident(simulation,"spill").Labor==T(3600),
                    "The historical schema16 cleanup could not continue to its original exact completion.");
            });
#endif
            cases.Add("crafting_remediation_incapacity_pauses_without_automatic_resume", () => {
                var p = CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("spill", 1) }), conditions: new ConditionCombatFixture(CCApply("stun", "Stunned", worker, new ConditionStamp(T(20)), new ConditionStamp(T(10)))));
                var s = World(p); CraftEvent(s, "spill"); Remedy(s, "spill"); WorldAdvance(s, 10); CCDispatch(s, "stun", worker); WorldAdvance(s, 10);
                Require(Incident(s, "spill").Labor == T(10) && Incident(s, "spill").Workers.Count == 0, "Incapacity erased work or ending resumed it."); Remedy(s, "spill"); WorldAdvance(s, 1); Require(Incident(s, "spill").Labor == T(11), "Explicit cleanup resume failed.");
            });
            cases.Add("crafting_fouling_uses_original_participants_and_parallel_actual_labor", () => {
                var people = new[] { hero, worker }; var fact = new CraftingMishapFact("foul", 5, participants: people); people[0] = worker;
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { fact }))); CraftEvent(s, "foul"); HeroToWorkshop(s); Remedy(s, "foul"); Remedy(s, "foul", hero); WorldAdvance(s, 3600);
                Require(Incident(s, "foul").ParticipantIds.SequenceEqual(new[] { hero, worker }) && Incident(s, "foul").Labor == T(7200) && Incident(s, "foul").Remedied
                    && Incident(s, "foul").Workers.Count == 0 && !CraftingRestrictions.OrderWorkBlocked(s.Capture(), SharedCraftingFixture.StationId), "Parallel work used later crew size for requirement or banked excess.");
            });
            cases.Add("crafting_parallel_cleanup_rebooks_on_join_and_leave_without_extra_credit", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("foul", 5, participants: new[] { hero, worker }) })));
                CraftEvent(s, "foul"); HeroToWorkshop(s); Remedy(s, "foul"); WorldAdvance(s, 10); Remedy(s, "foul", hero); WorldAdvance(s, 10); Remedy(s, "foul", hero, true); WorldAdvance(s, 10);
                Require(Incident(s, "foul").Labor == T(40) && Incident(s, "foul").Workers.SequenceEqual(new[] { worker }), "Joined/left cleaner was counted twice or continued contributing.");
                RejectUnchanged(s, host, ResearchCommand(s), "FormulaWorkNotSelected");
            });
            cases.Add("crafting_lost_log_is_lead_and_trade_specific_preserves_formula", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("notes", 6, at: T(3600)) }), research: new SharedResearchFixture())); ResearchStart(s, copy: true); WorldAdvance(s, 3600); CraftEvent(s, "notes");
                Require(FormulaResearchRules.Knows(s.Capture(), worker, SharedResearchFixture.Recipe) && CraftingRestrictions.NewOrderBlocked(s.Capture(), worker, SharedCraftingFixture.StationId, "Alchemy")
                    && !CraftingRestrictions.NewOrderBlocked(s.Capture(), hero, SharedCraftingFixture.StationId, "Alchemy") && !CraftingRestrictions.NewOrderBlocked(s.Capture(), worker, SharedCraftingFixture.StationId, "Smithing"), "Lost log erased formula or blocked other leads/trades.");
                HeroToWorkshop(s); RejectUnchanged(s, host, CraftCommand(s, "notes", CommandKind.StartCraftRemedy, hero), "CraftRemedyWorkerIneligible"); Remedy(s, "notes"); WorldAdvance(s, 3600);
                Require(Incident(s, "notes").Remedied && s.Capture().RandomState == 1, "Log reconstruction rolled or failed.");
            });
            cases.Add("crafting_remedy_obligations_are_independent_and_single_worker_when_required", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("spill1", 1), new CraftingMishapFact("spill2", 1) }))); CraftEvent(s, "spill1"); CraftEvent(s, "spill2"); HeroToWorkshop(s); Remedy(s, "spill1");
                RejectUnchanged(s, host, CraftCommand(s, "spill1", CommandKind.StartCraftRemedy, hero), "CraftRemedySingleWorker");
                WorldAdvance(s, 3600); Require(Incident(s, "spill1").Remedied && !Incident(s, "spill2").Remedied && CraftingRestrictions.StationUseBlocked(s.Capture(), SharedCraftingFixture.StationId), "One cleanup cleared another incident.");
            });
            cases.Add("crafting_consequence_restore_rejects_forged_damage_and_cadence", () => {
                var p = CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4) }), MishapSeed(10)); var s = World(p); CraftEvent(s, "acid");
                var bad = s.Capture(); bad.DyingCadences = new[] { new DyingCadenceRecord(worker, T(1)) }; Throws<ArgumentException>(() => new Simulation(p, bad, ExecutionProfile.Laboratory));
                bad = s.Capture(); bad.Structures = new[] { bad.Structures.Single().WithHp(4) }; Throws<ArgumentException>(() => new Simulation(p, bad, ExecutionProfile.Laboratory));
            });
            cases.Add("crafting_fixed_dying_uses_next_start_not_six_seconds_after_injury", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(heroHp: 1, events: new[] { new CraftingMishapFact("acid", 4, hero, T(59, 10)) }), MishapSeed(10, 12)));
                WorldAdvance(s, 59, 10); CraftEvent(s, "acid", hero); WorldAdvance(s, 1, 10);
                Require(s.Capture().LifeEvents.Single().At == T(6) && Life(s).DeathSuccesses == 1 && s.Capture().DyingCadences.Length == 0, "Existing calendar was replaced by onset fallback.");
                BeginEncounter(s); Require(s.Capture().LifeEvents.Length == 1, "Boundary entry repeated virtual Start.");
            });
            cases.Add("crafting_simultaneous_life_markers_have_stable_order_and_chunk_parity", () => {
                var p = CraftPolicy(new SharedCraftingFixture(heroHp: 1, companionHp: 1, events: new[] { new CraftingMishapFact("hero-acid", 4, hero), new CraftingMishapFact("worker-acid", 4) }));
                var a = World(p); var b = World(p); foreach (var s in new[] { a, b }) { CraftEvent(s, "hero-acid", hero); CraftEvent(s, "worker-acid"); }
                WorldAdvance(a, 6); for (int i = 0; i < 12; i++) WorldAdvance(b, 1, 2);
                var events = a.Capture().LifeEvents; Require(events.Length == 2 && events[0].ActorId == hero && events[1].ActorId == worker && events.All(x => x.At == T(6))
                    && events.Select(x => x.ActorId).SequenceEqual(b.Capture().LifeEvents.Select(x => x.ActorId)) && a.Capture().RandomState == b.Capture().RandomState
                    && a.Capture().Lives.All(x => x.SameAs(b.Capture().Lives.Single(y => y.ActorId == x.ActorId))) && Life(a).LastDeathTurn == 1 && Life(a, worker).LastDeathTurn == 2,
                    "Chunking changed due identity, equal-time order or unique audit sequence.");
            });
            cases.Add("crafting_death_recovery_does_not_cure_independent_unconsciousness", () => {
                var p = CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4) }), MishapSeed(10, 20),
                    conditions: new ConditionCombatFixture(CCApply("sleep", "Unconscious", worker, new ConditionStamp(T(7))))); var s = World(p); CCDispatch(s, "sleep", worker); CraftEvent(s, "acid"); WorldAdvance(s, 6);
                Require(Life(s, worker).Hp == 1 && CCState(s, worker).View().Has(ConditionKind.Unconscious), "Natural20 cured an independent condition.");
                WorldAdvance(s, 1); Require(!CCState(s, worker).View().Has(ConditionKind.Unconscious) && CCState(s, worker).View().Has(ConditionKind.Prone), "Expiry incorrectly erased persistent Prone.");
            });
            cases.Add("crafting_remedy_final_labor_survives_endpoint_incapacity_without_check", () => {
                var p = CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("spill", 1) }), conditions: new ConditionCombatFixture(CCApply("stun", "Stunned", worker), CCGrant("ward", worker, new ConditionStamp(T(3600)), "Stunned")));
                var s = World(p); CCDispatch(s, "stun", worker); CCDispatch(s, "ward", worker); CraftEvent(s, "spill"); Remedy(s, "spill"); WorldAdvance(s, 3600);
                Require(Incident(s, "spill").Remedied && s.Capture().RandomState == 1 && CCState(s, worker).View().Has(ConditionKind.Stunned), "Earned cleanup required an invented endpoint act or roll.");
            });
            cases.Add("crafting_remedy_work_window_ends_without_free_labor_or_erasure", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("calibrate", 2, at: T(28000)) })));
                WorldAdvance(s, 28000); CraftEvent(s, "calibrate"); Remedy(s, "calibrate"); WorldAdvance(s, 900);
                Require(Incident(s, "calibrate").Labor == T(800) && Incident(s, "calibrate").Workers.Count == 0, "Remedy worked across unscheduled Watch.");
                Remedy(s, "calibrate"); WorldAdvance(s, 6400); Require(Incident(s, "calibrate").Remedied, "Remedy could not finish during next legal window.");
            });
            cases.Add("crafting_participant_entry_pauses_cleanup_remote_worker_continues", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("foul", 5, participants: new[] { hero, worker }) })));
                CraftEvent(s, "foul"); HeroToWorkshop(s); Remedy(s, "foul"); Remedy(s, "foul", hero); WorldAdvance(s, 1); BeginEncounter(s);
                Require(Incident(s, "foul").Workers.SequenceEqual(new[] { worker }) && Incident(s, "foul").Labor == T(2), "Entry failed to detach participating cleaner.");
                ConnectedEnd(s); Require(Incident(s, "foul").Labor == T(5), "Remote cleanup did not earn exact remaining slot.");
            });
            cases.Add("crafting_recalibration_rechecks_current_tool_permission_before_duplicate", () => {
                var s = World(CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("calibrate", 2) }))); CraftEvent(s, "calibrate"); var c = CraftCommand(s, "calibrate", CommandKind.StartCraftRemedy); WorldCommit(s, c);
                var revoked = new Authority(host.Principal, new[] { worker }); RejectUnchanged(s, revoked, c, "InventoryNotAuthorized"); Remedy(s, "calibrate", pause: true);
                RejectUnchanged(s, revoked, CraftCommand(s, "calibrate", CommandKind.StartCraftRemedy), "InventoryNotAuthorized");
            });
            cases.Add("crafting_pending_knockout_blocks_accident_rng_and_preserves_completion", () => {
                var p = new TestOnlySharedWorldPolicy(new SharedCombatFixture(1, SeedForDeath(16)), null, new SharedCraftingFixture(events: new[] { new CraftingMishapFact("acid", 4, at: T(2)) })); var s = ConnectedArena(p);
                WorldCommit(s, Tac(s, CommandKind.AttackUnarmed, AdditionalTacticalActor.Id, knockout: AttackKnockoutMode.AskIfEligible));
                Require(s.Capture().MeleeAttacks.Single().Pending, "Expected paid pending KO."); RejectUnchanged(s, host, CraftCommand(s, "acid"), "TacticalChoicePending");
                WorldCommit(s, Tac(s, CommandKind.ResolveKnockout, s.Capture().MeleeAttacks.Single().Id, choice: true)); CraftEvent(s, "acid");
                Require(s.Capture().Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Stable && s.Capture().CraftingIncidents.Length == 1, "Accident stranded paid choice or was lost.");
            });
            cases.Add("crafting_incident_identity_cannot_cancel_an_unrelated_research_reservation", () => {
                var p = CraftPolicy(new SharedCraftingFixture(events: new[] { new CraftingMishapFact("formula.1", 5) }), research: new SharedResearchFixture()); var s = World(p);
                ResearchStart(s); CraftEvent(s, "formula.1"); HeroToWorkshop(s); Remedy(s, "formula.1", hero); WorldAdvance(s, 10);
                Require(ResearchJob(s).Id == "formula.1" && s.Capture().Work.WorkerIntervals.Any(x => x.JobId == "formula.1" && x.WorkerId == worker && x.End == T(28800))
                    && ResearchJob(s).Work.Labor == T(15) && Incident(s, "formula.1").Labor == T(10), "Cleanup stole the research job reservation.");
                RejectUnchanged(s, host, IC(s, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId, new InventoryRequest(new RuleQuantity(1), TestOnlyFillingPolicy.FlaskId), worker), "WorkerBusy");
                Remedy(s, "formula.1", hero, true); s = new Simulation(p, new SnapshotCodec().Decode(Bytes(s)), ExecutionProfile.Laboratory); WorldAdvance(s, 1);
                Require(ResearchJob(s).Work.Labor == T(16) && Incident(s, "formula.1").Labor == T(10), "Stopping colliding-name cleanup changed research labor.");
            });
            cases.Add("crafting_logical_dying_markers_persist_after_episode_closes", () => {
                var p = CraftPolicy(new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4, at: T(1, 3)) }), MishapSeed(10, 20)); var s = World(p); WorldAdvance(s, 1, 3); CraftEvent(s, "acid"); WorldAdvance(s, 6);
                s = new Simulation(p, new SnapshotCodec().Decode(Bytes(s)), ExecutionProfile.Laboratory); var marker = s.Capture().WorldLifeMarkers.Single();
                Require(s.Capture().DyingCadences.Length == 0 && marker.CalendarId == "outside.dying" && marker.ActorId == worker && marker.Origin == T(1, 3)
                    && marker.Ordinal == 1 && marker.Sequence == 1 && marker.At == T(19, 3), "Closed episode lost its logical marker identity.");
                var bad = s.Capture(); bad.WorldLifeMarkers = new[] { new WorldLifeMarkerRecord(worker, "outside.dying", default, 1, 1, T(19, 3)) };
                Throws<ArgumentException>(() => new Simulation(p, bad, ExecutionProfile.Laboratory));
            });
        }
    }
}
#endif
