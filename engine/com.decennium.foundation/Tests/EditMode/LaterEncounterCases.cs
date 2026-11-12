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
        private const string LaterDefender = TestOnlySharedWorldPolicy.LaterDefenderId;
        private const string LaterClub = TestOnlySharedWorldPolicy.LaterDefenderClubId;

        private static TestOnlySharedWorldPolicy LaterPolicy(uint? seed = null, ConditionCombatFixture conditions = null)
            => MakeLaterPolicy(seed, conditions, Array.Empty<TacticalTerrainCell>());

        private static TestOnlySharedWorldPolicy MakeLaterPolicy(uint? seed, ConditionCombatFixture conditions, TacticalTerrainCell[] terrain,
            SharedCraftingFixture crafting = null)
        {
            if (!seed.HasValue && terrain.Length == 0 && crafting == null) return AttemptPolicy(conditions: conditions).EnableLaterEncounter();
            uint combatSeed = seed ?? 1;
            if (!seed.HasValue) {
                while (PlaytestDice.RollD20(combatSeed).Natural != 12) combatSeed++;
            }
            var combat = new SharedCombatFixture(enemyHp: 1, seed: combatSeed);
            var policy = crafting == null
                ? new TestOnlySharedWorldPolicy(new PortableKitFixture(), combat, new SupplyCacheFixture(), conditions: conditions, terrain: terrain)
                : new TestOnlySharedWorldPolicy(new PortableKitFixture(), combat, crafting, new SupplyCacheFixture(), conditions: conditions, terrain: terrain);
            return policy.EnableMining(new SharedMiningFixture())
                .EnableHavenAppraisal(new TestOnlyHavenAppraisalProfile())
                .EnableHavenSale(new TestOnlyHavenSaleProfile())
                .EnableHavenMeal(new TestOnlyHavenMealProfile())
                .EnableExpeditionBill(new TestOnlyExpeditionBillProfile())
                .EnableExpeditionClose(new TestOnlyExpeditionCloseProfile())
                .EnableNextCharterPlan(new TestOnlyNextCharterPlanProfile(reserveWaterStartsCarried: true))
                .EnableNextCharterAgreement(new TestOnlyNextCharterAgreementProfile())
                .EnableCharterAttempt(new TestOnlyCharterAttemptProfile())
                .EnableLaterEncounter();
        }

        private static Authority LaterHost()
        {
            var actors = new[] { PlanHero, TestOnlyPolicy.CompanionId, SaleBuyer, AdditionalTacticalActor.Id, LaterDefender };
            return new Authority("TEST_ONLY.host", actors, true, true, actors, actors);
        }

        private static Simulation LaterPrepared(TestOnlySharedWorldPolicy policy = null)
        {
            var sim = AttemptReady(policy ?? LaterPolicy());
            PlanWalk(sim, 1, 0);
            PlanWalk(sim, -1, 0);
            StartAttempt(sim);
            WorldStep(sim, 1, 0);
            WorldAdvance(sim, 3, 2);
            ObserveAttempt(sim);
            WorldStep(sim, -1, 0);
            WorldAdvance(sim, 3, 2);
            PlanWalk(sim, -1, 0);
            Require(sim.Capture().RuleClock == T(11578) && Attempt(sim).Outcome == CharterAttemptOutcome.ReturnedComplete,
                "The accepted connected history changed before the later approach.");
            return sim;
        }

        private static Simulation LaterEarly(TestOnlySharedWorldPolicy policy = null)
        {
            var sim = PortableWorld(policy ?? LaterPolicy());
            ResolveAppraisalExpeditionEncounter(sim);
            while (Body(sim).X > 1) PlanWalk(sim, -1, 0);
            while (Body(sim).Y < 3) PlanWalk(sim, 0, 1);
            Require(Body(sim).X == 1 && Body(sim).Y == 3 && sim.Capture().CharterAttempt == null,
                "The pre-charter control did not reach the actual approach.");
            return sim;
        }

        private static Command LaterApproach(Simulation sim)
            => new Command("later.approach." + sim.Capture().Revision, PlanHero, sim.Capture().Revision,
                CommandKind.BeginWorldStep, "walk", -1, 0);

        private static Command LaterAdvance(Simulation sim, int seconds = 12, int denominator = 1)
            => new Command("later.advance." + sim.Capture().Revision, PlanHero, sim.Capture().Revision,
                CommandKind.AdvanceClock, "", seconds, denominator);

        private static CommandResult LaterCommit(Simulation sim, Command command)
        {
            var result = sim.Execute(LaterHost(), command);
            Require(result.Outcome == Outcome.Committed, command.Kind + " failed: " + result.Code);
            return result;
        }

        private static LaterEncounterEntry EnterLater(Simulation sim)
        {
            LaterCommit(sim, LaterApproach(sim));
            var result = LaterCommit(sim, LaterAdvance(sim));
            var entry = sim.Capture().LaterEncounter.Entry;
            Require(entry != null && result.TacticalDecisionAt == entry.Epoch.Origin && sim.Capture().RuleClock == entry.Epoch.Origin,
                "Actual later entry or explicit reached boundary is absent.");
            return entry;
        }

        private static void LaterStance(Simulation sim, CombatStance stance = CombatStance.Aggressive)
        {
            var state = sim.Capture();
            var encounter = state.Encounter;
            if (ActorLifeRules.CanAct(state, encounter.CurrentActor)
                && !state.Stances.Any(x => x.TurnOrdinal == encounter.TurnOrdinal && EncounterHistory.InCurrent(state, x.Revision)))
                LaterCommit(sim, Tac(sim, CommandKind.SelectCombatStance, stance: (int)stance));
        }

        private static void FinishLaterFight(Simulation sim, bool defenderAttacked)
        {
            for (int turns = 0; turns < 38; turns++) {
                var state = sim.Capture();
                if (state.Lives.Single(x => x.ActorId == LaterDefender).Dead) {
                    LaterStance(sim);
                    LaterCommit(sim, Tac(sim, CommandKind.EndFixedEncounter));
                    return;
                }
                string current = state.Encounter.CurrentActor;
                LaterStance(sim, current == PlanHero ? CombatStance.Aggressive : CombatStance.Guarded);
                if (ActorLifeRules.CanAct(state, current)) {
                    if (current == PlanHero)
                        LaterCommit(sim, Tac(sim, CommandKind.AttackClub, LaterDefender, weapon: TestOnlyClubAttackPolicy.ActorClub));
                    else if (!defenderAttacked) {
                        LaterCommit(sim, Tac(sim, CommandKind.AttackClub, PlanHero, weapon: LaterClub));
                        defenderAttacked = true;
                    }
                }
                if (sim.Capture().Lives.Single(x => x.ActorId == LaterDefender).Dead) {
                    LaterCommit(sim, Tac(sim, CommandKind.EndFixedEncounter));
                    return;
                }
                LaterCommit(sim, Tac(sim, CommandKind.EndRegularTurn));
            }
            throw new Exception("Supported ordinary combat did not resolve the later opponent within the finite witness.");
        }

        private static void AddLaterEncounterCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            var codec = new SnapshotCodec();

            cases.Add("exp07_later_encounter_connected_arrival_and_fractional_replay", () =>
            {
                var sim = LaterPrepared();
                var before = sim.Capture();
                var definition = before.LaterEncounter.Definition;
                var prior = before.LaterEncounter.FirstExit;
                Require(before.SchemaVersion == Snapshot.LaterEncounterSchema && before.ClosedEncounters.Length == 0
                    && prior.ClosedAt == T(15) && prior.ClosedRevision == 15 && prior.Encounter.TurnOrdinal == 4
                    && before.Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Dead
                    && before.Lives.Single(x => x.ActorId == LaterDefender).Hp == 8
                    && before.Clubs.Single(x => x.Id == LaterClub).HeldBy == LaterDefender
                    && Body(sim, LaterDefender).X == 0 && Body(sim, LaterDefender).Y == 4
                    && !before.WorldSchedule.Order.Contains(LaterDefender),
                    "The initially present later body, exact original combat exit, or scope was lost.");
                SaveBill(sim, LaterPolicy(), directory, "exp07-later-before-entry");

                var step = LaterApproach(sim);
                var bytes = Bytes(sim);
                Require(sim.QueryCommand(host, step).Admissible && bytes.SequenceEqual(Bytes(sim)),
                    "An approach query changed state or failed to describe the real step.");
                LaterCommit(sim, step);
                Require(!sim.Capture().InventoryCombat && sim.Capture().LaterEncounter.Entry == null
                    && sim.Capture().RandomState == before.RandomState, "A declaration rolled initiative or entered combat.");
                LaterCommit(sim, LaterAdvance(sim, 1, 2));
                var partial = sim.Capture();
                var position = WorldPositionResolver.Position(partial, PlanHero);
                Require(partial.RuleClock == T(23157, 2) && HeroEdge(sim).DistanceFeet == new RuleQuantity(5, 3)
                    && position.X == new RuleQuantity(2, 3) && partial.RandomState == before.RandomState
                    && partial.LaterEncounter.Entry == null, "Fractional approach manufactured arrival or spent randomness.");
                var replay = SaveBill(sim, LaterPolicy(), directory, "exp07-later-partial-edge");
                foreach (var run in new[] { sim, replay }) {
                    var advance = LaterAdvance(run);
                    var beforeQuery = Bytes(run);
                    Require(run.QueryCommand(host, advance).Admissible && beforeQuery.SequenceEqual(Bytes(run)),
                        "An advance query drew initiative or advanced the clock.");
                    var result = LaterCommit(run, advance);
                    var after = run.Capture();
                    var entry = after.LaterEncounter.Entry;
                    Require(result.Code == "CommittedAtTacticalDecision" && !result.IsSuspended
                        && result.ReachedClock == T(23159, 2) && result.TacticalDecisionAt == after.RuleClock
                        && entry.RequestedUntil > after.RuleClock && after.InventoryCombat
                        && after.Encounter.Id == definition.EncounterId
                        && after.Encounter.Order.OrderBy(x => x, StringComparer.Ordinal).SequenceEqual(new[] { PlanHero, LaterDefender })
                        && entry.HeroExpenditureAtArrival.MovementSpent == new RuleQuantity(5)
                        && after.ClosedEncounters.Single().Encounter.TurnOrdinal == 4
                        && after.ExpeditionEpisodeClose.EncounterExitRevision == prior.ClosedRevision
                        && WorldTiming.FindEpoch(after, before.WorldSchedule.Id).Start(5) == prior.ClosedAt
                        && after.CharterAttempt.Returned.Revision == before.CharterAttempt.Returned.Revision,
                        "Entry did not yield at the real paid boundary or invalidated earlier history.");
                    var entered = Bytes(run);
                    var duplicate = run.Execute(host, advance);
                    Require(duplicate.Outcome == Outcome.Duplicate && duplicate.TacticalDecisionAt == result.TacticalDecisionAt
                        && entered.SequenceEqual(Bytes(run)), "A duplicate entry redrew or consumed remaining time.");
                    RejectUnchanged(run, host, new Command(advance.Id, advance.Actor, advance.ExpectedRevision,
                        advance.Kind, "", advance.X + 1, advance.Y), "CommandIdConflict");
                    RejectUnchanged(run, host, LaterAdvance(run), "TacticalDecisionClockPaused");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Restored partial approach replay diverged.");
                SaveBill(sim, LaterPolicy(), directory, "exp07-later-entered");
                File.WriteAllLines(Path.Combine(directory, "exp07-later-entry.tsv"), LaterAudit(sim.Capture()));
            });

            cases.Add("exp07_later_encounter_shared_initiative_and_pre_start_reaction", () =>
            {
                var sim = LaterPrepared();
                WorldAdvance(sim, 2);
                WorldStep(sim, 0, -1, run: true);
                WorldAdvance(sim, 3, 4);
                WorldStep(sim, 0, 1, run: true);
                WorldAdvance(sim, 3, 4);
                var before = sim.Capture();
                var entry = EnterLater(sim);
                var hero = WorldLedger(sim);
                Require(entry.Epoch.Order[0] == LaterDefender && entry.Draws.Select(x => x.ActorId).SequenceEqual(new[] { PlanHero, LaterDefender })
                    && entry.Draws[0].Natural == 9 && entry.Draws[1].Natural == 12
                    && entry.Draws[0].RandomBefore == before.RandomState && entry.Draws[1].RandomAfter == sim.Capture().RandomState
                    && hero.LastStart == -1 && hero.MovementSpent == new RuleQuantity(15) && hero.ActionSpent && hero.DashPaid
                    && hero.ReactionAvailable, "Defender-first entry did not preserve actual paid movement and Action or apply source initial Reaction.");
                LaterStance(sim, CombatStance.Guarded);
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 1, y: 4));
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 1, y: 3));
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 2, y: 3));
                var pending = TestOnlyClubAttackPolicy.PendingMove(sim.Capture());
                Require(pending != null && pending.Reactors.SequenceEqual(new[] { PlanHero }),
                    "A real defender departure did not offer the late hero's initial Reaction.");
                RejectUnchanged(sim, host, Tac(sim, CommandKind.EndFixedEncounter), "TacticalChoicePending");
                LaterCommit(sim, Opportunity(sim, true));
                Require(!WorldLedger(sim).ReactionAvailable && WorldLedger(sim).LastStart == -1
                    && sim.Capture().MeleeAttacks.Last().Opportunity && sim.Capture().MeleeAttacks.Last().AttackerId == PlanHero,
                    "An accepted pre-first-Start Reaction was not spent once on the actual attack.");
                LaterCommit(sim, Tac(sim, CommandKind.EndRegularTurn));
                hero = WorldLedger(sim);
                Require(sim.Capture().RuleClock == entry.Epoch.Origin.AddSeconds(3) && hero.LastStart == 1
                    && hero.MovementSpent == default && !hero.ActionSpent && !hero.DashPaid && hero.ReactionAvailable,
                    "The actual hero Start failed to refresh once after carried expenditure and spent initial Reaction.");

                var seeded = new List<string>();
                foreach (var control in new[] { (Seed: 1u, Hero: 18, Defender: 9), (Seed: 32u, Hero: 5, Defender: 5) }) {
                    var run = LaterEarly(LaterPolicy(control.Seed));
                    var earlier = run.Capture();
                    var rolled = EnterLater(run);
                    Require(earlier.CharterAttempt == null && earlier.NextCharterAgreement == null,
                        "Actual entry required the completed charter.");
                    bool heroFirst = control.Hero > control.Defender;
                    Require(rolled.Draws[0].Total == control.Hero && rolled.Draws[1].Total == control.Defender
                        && rolled.Draws[0].RandomBefore == earlier.RandomState
                        && rolled.Epoch.Order[0] == (heroFirst ? PlanHero : LaterDefender),
                        "Actual deterministic initiative or the equal-total Director decision was replaced.");
                    Require(rolled.HeroExpenditureAtArrival.MovementSpent == new RuleQuantity(5)
                        && WorldLedger(run).LastStart == (heroFirst ? 0 : -1)
                        && WorldLedger(run).MovementSpent == (heroFirst ? default : new RuleQuantity(5)),
                        "The legal first regular Start and the late hero's carried expenditure diverged.");
                    seeded.Add((heroFirst ? "hero-first" : "tied") + " seed=" + control.Seed + " " + string.Join(" ", LaterAudit(run.Capture())));
                }
                File.WriteAllLines(Path.Combine(directory, "exp07-later-initiative.tsv"),
                    seeded.Concat(new[] { "defender-first " + string.Join(" ", LaterAudit(sim.Capture())) }));
            });

            cases.Add("exp07_later_encounter_old_marker_and_remote_labor", () =>
            {
                var due = new ConditionStamp(T(11586));
                const string marker = "world.fixed-calendar.start.3862";
                var condition = new ConditionCombatFixture(new ConditionFixtureEvent(PlanHero,
                    ConditionOperation.Apply("event.later-old-marker", new ConditionStamp(T(11584)),
                        new ConditionApplicationData("later-old-marker", PlanHero, marker, "Dazed", due,
                            "original-regular-start", false))));
                var sim = LaterPrepared(LaterPolicy(conditions: condition));
                PlanWalk(sim, -1, 0, TestOnlyPolicy.CompanionId);
                Require(sim.Capture().RuleClock == T(11584), "Remote-worker placement did not reach the intended marker control.");
                FarmWork(sim, CommandKind.PlantCrop);
                LaterCommit(sim, CCCommand(sim, "later-old-marker"));
                var coincident = SaveBill(sim, LaterPolicy(conditions: condition), directory, "exp07-later-remote-before-entry");
                var entry = EnterLater(sim);
                Require(entry.Epoch.Origin == T(23171, 2) && entry.Epoch.Order[0] == LaterDefender
                    && ViewCondition(sim, "later-old-marker").EndedAt == null && Crop(sim).Tasks.Single().Progress == T(3, 2),
                    "The old-bound effect or compatible remote work was discarded at entry.");
                var state = sim.Capture();
                var old = WorldTiming.FindEpoch(state, "world.fixed-calendar");
                Require(old.MarkerId(3862) == marker && old.Start(3862) == T(11586) && old.Start(3862) < entry.Epoch.Start(1)
                    && WorldLedger(sim).LastStart == -1 && WorldLedger(sim).MovementSpent == new RuleQuantity(5),
                    "The old marker was reinterpreted as a new regular Start.");
                LaterStance(sim);
                LaterCommit(sim, Tac(sim, CommandKind.EndRegularTurn));
                var ended = ViewCondition(sim, "later-old-marker");
                Require(ended.Application.Source == marker && ended.EndedAt?.Time == T(11586)
                    && sim.Capture().RuleClock == T(23177, 2) && WorldLedger(sim).LastStart == 1
                    && Crop(sim).Tasks.Single().Status == CropWorkStatus.Working && Crop(sim).Tasks.Single().Progress == T(9, 2),
                    "Old marker expiry, new refresh or remote labor was duplicated or retimed.");
                SaveBill(sim, LaterPolicy(conditions: condition), directory, "exp07-later-remote-and-marker");
                LaterCommit(coincident, LaterAdvance(coincident, 1, 2));
                var tied = EnterLater(coincident);
                Require(tied.Epoch.Origin == T(11586) && tied.Epoch.Order[0] == LaterDefender
                    && WorldTiming.FindEpoch(coincident.Capture(), old.Id).ProcessedSlot == 3862
                    && ViewCondition(coincident, "later-old-marker").EndedAt?.Time == tied.Epoch.Origin
                    && WorldLedger(coincident).LastStart == -1 && WorldLedger(coincident).MovementSpent == new RuleQuantity(5)
                    && Crop(coincident).Tasks.Single().Progress == T(2),
                    "Coincident old expiry refreshed the late participant or duplicated the elapsed remote work.");
                LaterStance(coincident);
                LaterCommit(coincident, Tac(coincident, CommandKind.EndRegularTurn));
                Require(WorldLedger(coincident).LastStart == 1 && WorldLedger(coincident).MovementSpent == default
                    && Crop(coincident).Tasks.Single().Progress == T(5), "Only the genuine later hero Start should refresh.");
                File.WriteAllLines(Path.Combine(directory, "exp07-later-markers.tsv"),
                    LaterAudit(sim.Capture()).Concat(LaterAudit(coincident.Capture())));
            });

            cases.Add("exp07_later_encounter_real_combat_archive_and_ordinary_exit", () =>
            {
                var sim = LaterPrepared();
                var entry = EnterLater(sim);
                var before = sim.Capture();
                var oldExit = before.ClosedEncounters.Single();
                Require(before.Encounter.CurrentActor == LaterDefender, "The retained connected seed should put the defender first.");
                RejectUnchanged(sim, host, Tac(sim, CommandKind.EndFixedEncounter), "ConflictNotResolved");
                LaterStance(sim);
                LaterCommit(sim, Tac(sim, CommandKind.AttackClub, PlanHero, weapon: LaterClub));
                var attacked = sim.Capture();
                Require(attacked.MeleeAttacks.Last().AttackerId == LaterDefender && attacked.MeleeAttacks.Last().TargetId == PlanHero
                    && attacked.Lives.Single(x => x.ActorId == PlanHero).Hp < before.Lives.Single(x => x.ActorId == PlanHero).Hp,
                    "The distinct defender's real turn did not affect shared life state.");
                LaterCommit(sim, Tac(sim, CommandKind.EndRegularTurn));
                var replay = SaveBill(sim, LaterPolicy(), directory, "exp07-later-mid-fight");
                foreach (var run in new[] { sim, replay }) {
                    FinishLaterFight(run, defenderAttacked: true);
                    var closed = run.Capture();
                    var archives = closed.ClosedEncounters;
                    var later = archives.Single(x => x.Encounter.Id == closed.LaterEncounter.Definition.EncounterId);
                    Require(!closed.InventoryCombat && closed.Encounter == null && archives.Length == 2
                        && archives[0].Encounter.Id == oldExit.Encounter.Id && archives[0].ClosedRevision == oldExit.ClosedRevision
                        && archives[0].ClosedAt == oldExit.ClosedAt && archives[0].Encounter.TurnOrdinal == 4
                        && later.ClosedAt == closed.RuleClock && later.ClosedRevision == closed.Revision
                        && later.Encounter.TurnOrdinal + 1 == closed.LaterEncounter.Entry.Epoch.ProcessedSlot
                        && closed.Lives.Single(x => x.ActorId == LaterDefender).Dead && closed.Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Dead
                        && closed.Lives.Single(x => x.ActorId == PlanHero).Hp == attacked.Lives.Single(x => x.ActorId == PlanHero).Hp
                        && closed.Clubs.Single(x => x.Id == LaterClub).OwnerId == LaterDefender
                        && closed.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))
                            .SequenceEqual(before.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId)))
                        && closed.CharterAttempt.Returned.Revision == before.CharterAttempt.Returned.Revision,
                        "Actual later exit rewrote earlier provenance, granted loot or replenished persistent resources.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Actual later fight replay diverged.");
                var resumed = SaveBill(sim, LaterPolicy(), directory, "exp07-later-closed");
                foreach (var run in new[] { sim, resumed }) {
                    var closed = run.Capture();
                    PlanWalk(run, 1, 0);
                    Require(Body(run).X == 1 && Body(run).Y == 3 && run.Capture().RandomState == closed.RandomState
                        && run.Capture().ClosedEncounters.Length == 2 && run.Capture().Encounter == null
                        && run.Capture().LaterEncounter.Entry.ArrivalRevision == entry.ArrivalRevision,
                        "Ordinary continuation repeated initiative or changed the archive.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(resumed)), "Post-exit ordinary continuation replay diverged.");
                SaveBill(sim, LaterPolicy(), directory, "exp07-later-continued");
                File.WriteAllLines(Path.Combine(directory, "exp07-later-combat.tsv"), LaterAudit(sim.Capture()));
            });

            cases.Add("exp07_later_encounter_rejections_and_actual_arrival_interruption", () =>
            {
                var unresolved = PortableWorld(LaterPolicy());
                PlanWalk(unresolved, 1, 0);
                for (int i = 0; i < 3; i++) PlanWalk(unresolved, 0, 1);
                RejectUnchanged(unresolved, host, LaterApproach(unresolved), "LaterEncounterPriorConflictUnresolved");
                var blocked = LaterEarly();
                string companion = TestOnlyPolicy.CompanionId;
                PlanWalk(blocked, -1, 0, companion);
                PlanWalk(blocked, 0, -1, companion);
                PlanWalk(blocked, -1, 0, companion);
                PlanWalk(blocked, -1, 0, companion);
                PlanWalk(blocked, 0, 1, companion);
                RejectUnchanged(blocked, host, LaterApproach(blocked), "Occupied");

                var fixture = new ConditionCombatFixture(
                    CCApply("later-blinded-defender", "Blinded", LaterDefender, at: new ConditionStamp(T(23157, 2))),
                    new ConditionFixtureEvent(LaterDefender, ConditionOperation.Cure("event.later-defender-cure",
                        new ConditionStamp(T(23159, 2)), "Blinded")));
                var sim = LaterPrepared(LaterPolicy(conditions: fixture));
                var detached = sim.Capture();
                detached.Actors.Single(x => x.Id == LaterDefender).X = 1;
                Require(LaterPolicy(conditions: fixture).QueryCommand(detached, host, LaterApproach(sim)).Code == "LaterEncounterParticipantsIneligible",
                    "The detached changed-defender control bypassed actual position eligibility.");
                LaterCommit(sim, LaterApproach(sim));
                LaterCommit(sim, LaterAdvance(sim, 1, 2));
                var before = sim.Capture();
                LaterCommit(sim, CCCommand(sim, "later-blinded-defender", LaterDefender));
                var advance = LaterAdvance(sim);
                var interrupted = LaterCommit(sim, advance);
                var after = sim.Capture();
                Require(interrupted.Code == "LaterEncounterAwarenessUnavailable" && interrupted.TacticalDecisionAt == null
                    && interrupted.ReachedClock == T(23159, 2) && after.RuleClock == interrupted.ReachedClock
                    && after.LaterEncounter.Entry == null && after.ClosedEncounters.Length == 0
                    && after.LaterEncounter.Interruptions.Single().ApproachRevision == before.WorldTraversals.Single().StartedRevision
                    && after.RandomState == before.RandomState && after.WorldTraversals.Length == 0 && Body(sim).X == 0
                    && WorldLedger(sim).MovementSpent == new RuleQuantity(5),
                    "An actual mid-edge change erased elapsed movement or drew initiative after rejected eligibility.");
                var restored = SaveBill(sim, LaterPolicy(conditions: fixture), directory, "exp07-later-interrupted-arrival");
                foreach (var run in new[] { sim, restored }) {
                    Require(run.Execute(host, advance).Outcome == Outcome.Duplicate, "An interrupted arrival was repeated.");
                    LaterCommit(run, CCCommand(run, "later-defender-cure", LaterDefender));
                    PlanWalk(run, 1, 0);
                    EnterLater(run);
                    Require(run.Capture().LaterEncounter.Interruptions.Count == 1, "A fresh approach lost the earlier actual interruption.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(restored)), "Interrupted arrival restore/replay diverged.");
            });

            cases.Add("exp07_later_encounter_provenance_and_profile_compatibility", () =>
            {
                var sim = LaterEarly();
                EnterLater(sim);
                var actual = sim.Capture();
                var record = actual.LaterEncounter;
                var entry = record.Entry;
                Throws<ArgumentException>(() => new Simulation(AttemptPolicy(), actual, ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(LaterPolicy(), actual, ExecutionProfile.Release));
                var wrongRoster = actual.Copy();
                wrongRoster.Encounter = new FixedEncounterRecord(actual.Encounter.Id, actual.Encounter.Origin,
                    new[] { PlanHero, AdditionalTacticalActor.Id }, actual.Encounter.StartRevisions);
                Throws<ArgumentException>(() => codec.Encode(wrongRoster));

                LaterEncounterEntry ReplaceEntry(WorldScheduleRecord epoch = null, IEnumerable<LaterInitiativeDraw> draws = null,
                    WorldIntervalRecord expenditure = null) => new LaterEncounterEntry(epoch ?? entry.Epoch, entry.ApproachRevision,
                    entry.ArrivalRevision, entry.ArrivalCommandId, entry.RequestedUntil, draws ?? entry.Draws,
                    expenditure ?? entry.HeroExpenditureAtArrival);

                var altered = actual.Copy();
                var forgedDraws = entry.Draws.Select((row, index) => index != 0 ? row
                    : new LaterInitiativeDraw(row.ActorId, row.Natural == 20 ? 19 : row.Natural + 1, row.DexterityModifier,
                        row.Natural == 20 ? row.Bonus + 1 : row.Bonus - 1, row.RandomBefore, row.RandomAfter, row.WordsConsumed));
                altered.LaterEncounter = record.WithEntry(ReplaceEntry(draws: forgedDraws));
                RejectLaterCanonical(codec, altered);

                var spend = entry.HeroExpenditureAtArrival;
                altered.LaterEncounter = record.WithEntry(ReplaceEntry(expenditure: new WorldIntervalRecord(spend.ActorId,
                    spend.LastStart, new RuleQuantity(4), spend.ActionSpent, spend.DashPaid, spend.ReactionAvailable, spend.Interactions)));
                RejectLaterCanonical(codec, altered);
                altered.LaterEncounter = record.WithEntry(ReplaceEntry(epoch: entry.Epoch.At(entry.Epoch.ProcessedSlot + 1)));
                Throws<ArgumentException>(() => codec.Encode(altered));

                var first = record.FirstExit;
                var wrongExit = new ClosedEncounterRecord(first.Encounter, first.ClosedRevision, first.ClosedAt, "forged.exit");
                altered.LaterEncounter = new LaterEncounterRecord(record.Definition, wrongExit, entry);
                altered.ClosedEncounters = new[] { wrongExit };
                Throws<ArgumentException>(() => codec.Encode(altered));
                var history = first.Encounter;
                var truncated = new FixedEncounterRecord(history.Id, history.Origin, history.Order,
                    history.StartRevisions.Skip(1), history.ObservedOrdinals.Skip(1));
                var forgedPrefix = new ClosedEncounterRecord(truncated, first.ClosedRevision, first.ClosedAt, first.Reason);
                altered.LaterEncounter = new LaterEncounterRecord(record.Definition, forgedPrefix, entry);
                altered.ClosedEncounters = new[] { forgedPrefix };
                RejectLaterStructureOrReplay(codec, altered);

                var restored = SaveBill(sim, LaterPolicy(), directory, "exp07-later-profile-control");
                Require(Bytes(restored).SequenceEqual(Bytes(sim)), "The admitted new profile roundtrip changed accepted bytes.");
            });
        }

        private static ConditionInstance ViewCondition(Simulation sim, string id)
            => ConditionHistory.Restore(sim.Capture().Conditions.Single(x => x.Target == PlanHero)).Ledger.Applications
                .Single(x => x.Application.Id == id);

        private static void RejectLaterCanonical(SnapshotCodec codec, Snapshot altered)
        {
            var decoded = codec.Decode(codec.Encode(altered));
            bool rejected = false;
            try { new Simulation(LaterPolicy(), decoded, ExecutionProfile.Laboratory); }
            catch (ArgumentException ex) { rejected = ex.Message.Contains("InvalidSharedWorldReplay"); }
            Require(rejected, "A coherent forged later-encounter fact bypassed canonical replay.");
        }

        private static void RejectLaterStructureOrReplay(SnapshotCodec codec, Snapshot altered)
        {
            byte[] bytes;
            try { bytes = codec.Encode(altered); }
            catch (ArgumentException) { return; }
            Throws<ArgumentException>(() => new Simulation(LaterPolicy(), codec.Decode(bytes), ExecutionProfile.Laboratory));
        }

        private static string[] LaterAudit(Snapshot state)
        {
            var entry = state.LaterEncounter.Entry;
            var first = state.LaterEncounter.FirstExit;
            string[] starts = EncounterHistory.All(state).Where(x => x.Id == state.LaterEncounter.Definition.EncounterId)
                .SelectMany(x => x.ObservedOrdinals.Zip(x.StartRevisions,
                    (ordinal, revision) => ordinal + "@" + entry.Epoch.Start(ordinal) + ":" + revision)).ToArray();
            return new[] {
                "first-exit=" + first.ClosedAt + " rev=" + first.ClosedRevision + " outgoing=" + first.Encounter.TurnOrdinal
                    + " old-virtual-next=" + state.WorldSchedule.Start(first.Encounter.TurnOrdinal + 1),
                "episode-close=" + state.ExpeditionEpisodeClose?.CloseRevision + " approach-rev=" + entry.ApproachRevision
                    + " entry=" + entry.Epoch.Origin + " rev=" + entry.ArrivalRevision + " carried=" + entry.HeroExpenditureAtArrival.MovementSpent
                    + " requested=" + entry.RequestedUntil + " order=" + string.Join(",", entry.Epoch.Order)
                    + " draws=" + string.Join(",", entry.Draws.Select(d => d.ActorId + ":" + d.Natural + ":" + d.Total
                        + ":" + d.RandomBefore + ":" + d.RandomAfter)),
                "later-starts=" + string.Join(",", starts) + " exits=" + string.Join(",", state.ClosedEncounters.Select(x =>
                    x.Encounter.Id + ":" + x.ClosedAt + ":" + x.ClosedRevision + ":" + x.Reason))
            };
        }
    }
}
#endif
