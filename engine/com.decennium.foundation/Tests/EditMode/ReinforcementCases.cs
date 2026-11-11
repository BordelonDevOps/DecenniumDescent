#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string ReinforcingCompanion = TestOnlyPolicy.CompanionId;

        private static TestOnlySharedWorldPolicy ReinforcementPolicy(uint? seed = null,
            ConditionCombatFixture conditions = null, TerrainCost terrain = TerrainCost.Normal,
            TestOnlyReinforcementProfile profile = null)
            => MakeLaterPolicy(seed, conditions, terrain == TerrainCost.Normal
                ? Array.Empty<TacticalTerrainCell>() : new[] { new TacticalTerrainCell(1, 3, terrain) })
                .EnableCompanionReinforcement(profile ?? new TestOnlyReinforcementProfile());

        private static Simulation ReinforcementStaged(TestOnlySharedWorldPolicy policy, bool early = false)
        {
            var sim = early ? LaterEarly(policy) : LaterPrepared(policy);
            StageReinforcingCompanion(sim);
            return sim;
        }

        private static void StageReinforcingCompanion(Simulation sim)
        {
            if (Body(sim, ReinforcingCompanion).X == 4) PlanWalk(sim, -1, 0, ReinforcingCompanion);
            FarmWork(sim, CommandKind.PlantCrop);
            WorldAdvance(sim, 2);
            FarmWork(sim, CommandKind.PauseCrop);
            PlanWalk(sim, -1, 0, ReinforcingCompanion);
        }

        private static Command ReinforcementCommand(Simulation sim, CommandKind kind = CommandKind.BeginReinforcementApproach,
            string actor = ReinforcingCompanion)
        {
            var state = sim.Capture();
            return new Command("reinforcement." + state.Revision + "." + kind, actor, state.Revision,
                kind, ReinforcementValidation.IsInstruction(kind) ? state.Reinforcement.Definition.Id : "");
        }

        private static Command EndReinforcementTurn(Simulation sim, CombatStance stance = CombatStance.Guarded)
        {
            LaterStance(sim, stance);
            var command = Tac(sim, CommandKind.EndRegularTurn);
            LaterCommit(sim, command);
            return command;
        }

        private static WorldIntervalRecord ReinforcementInterval(Snapshot state, string actor)
            => state.WorldIntervals.Single(x => x.ActorId == actor);

        private static CropWorkRecord ReinforcementPlanting(Snapshot state)
            => state.Crops.SelectMany(x => x.Tasks).Single(x => x.WorkerId == ReinforcingCompanion && x.Kind == CropWorkKind.Plant);

        private static void AddReinforcementCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("exp07_companion_reinforcement_physical_arrival_and_same_fight", () =>
            {
                var sim = ReinforcementStaged(ReinforcementPolicy());
                var entry = EnterLater(sim);
                var before = sim.Capture();
                Require(before.SchemaVersion == Snapshot.ReinforcementSchema && before.RuleClock == T(23187, 2)
                    && Body(sim, ReinforcingCompanion).X == 2 && Body(sim, ReinforcingCompanion).Y == 3
                    && ReinforcementPlanting(before).Status == CropWorkStatus.Paused
                    && ReinforcementPlanting(before).Progress == T(2), "The actual staged companion or paid pause changed.");
                SaveBill(sim, ReinforcementPolicy(), directory, "exp07-reinforcement-before");
                var begin = ReinforcementCommand(sim);
                var result = LaterCommit(sim, begin);
                var moving = sim.Capture();
                var edge = moving.WorldTraversals.Single(x => x.ActorId == ReinforcingCompanion);
                Require(moving.Reinforcement.OwnsApproach(edge) && edge.DistanceFeet == default && moving.RuleClock == before.RuleClock
                    && moving.RandomState == before.RandomState && !moving.Encounter.Order.Contains(ReinforcingCompanion)
                    && moving.WorldActivityIntervals.Any(x => x.ActorId == ReinforcingCompanion),
                    "Voluntary approach created time, a draw, a roster member, or a second movement ledger.");
                Require(sim.Execute(host, begin).Revision == result.Revision && Bytes(sim).SequenceEqual(new SnapshotCodec().Encode(moving)),
                    "A repeated approach changed the committed snapshot.");
                EndReinforcementTurn(sim);
                var arrived = sim.Capture();
                Require(arrived.Reinforcement.Arrival.At == T(23189, 2) && arrived.RuleClock == T(23193, 2)
                    && arrived.Reinforcement.Arrival.Distance == new RuleQuantity(5) && arrived.RandomState == before.RandomState
                    && arrived.Encounter.Id == before.Encounter.Id && arrived.Encounter.Order.SequenceEqual(entry.Epoch.Order)
                    && Body(sim, ReinforcingCompanion).X == 1 && !arrived.WorldTraversals.Any(x => x.ActorId == ReinforcingCompanion),
                    "The real arrival drew initiative, changed the roster early, or missed the physical endpoint.");
                var restored = SaveBill(sim, ReinforcementPolicy(), directory, "exp07-reinforcement-arrived");
                var end = EndReinforcementTurn(sim);
                LaterStance(restored, CombatStance.Guarded);
                LaterCommit(restored, end);
                var joined = sim.Capture();
                var admission = joined.Reinforcement.Admission;
                Require(Bytes(sim).SequenceEqual(Bytes(restored)) && joined.RuleClock == T(23199, 2)
                    && joined.Encounter.Id == before.Encounter.Id && joined.Encounter.InitialOrder.SequenceEqual(entry.Epoch.Order)
                    && joined.Encounter.TurnOrdinal == 2 && joined.Encounter.Round == 2 && joined.Encounter.CurrentTurnId.EndsWith(".turn.2")
                    && admission.Phase.FirstTurn == 2 && admission.Phase.FirstRound == 2 && admission.Phase.Epoch.Order.Count == 3,
                    "The new roster must begin at the actual end-round of the same ongoing encounter.");
                Require(admission.Draw.RandomBefore == arrived.RandomState && admission.Draw.RandomAfter == joined.RandomState
                    && joined.LaterEncounter.Entry.Draws.Select(x => x.RandomAfter).SequenceEqual(entry.Draws.Select(x => x.RandomAfter))
                    && !joined.WorldActivityIntervals.Any(x => x.ActorId == ReinforcingCompanion)
                    && joined.WorldIntervals.Count(x => x.ActorId == ReinforcingCompanion) == 1
                    && admission.Carried.Single(x => x.Interval.ActorId == ReinforcingCompanion).Interval.MovementSpent == default
                    && ReinforcementPlanting(joined).Progress == T(2)
                    && joined.Clubs.Single(x => x.OwnerId == ReinforcingCompanion).HeldBy == "",
                    "Admission changed old draws, planting or gear, or left duplicate resources.");
                SaveBill(sim, ReinforcementPolicy(), directory, "exp07-reinforcement-admitted");
            });

            cases.Add("exp07_companion_reinforcement_partial_exact_late_and_cancelled", () =>
            {
                var exact = ReinforcementStaged(ReinforcementPolicy(terrain: TerrainCost.Severe));
                var exactEntry = EnterLater(exact);
                EndReinforcementTurn(exact);
                LaterCommit(exact, ReinforcementCommand(exact));
                var exactEnd = EndReinforcementTurn(exact);
                var atBoundary = exact.Capture();
                Require(atBoundary.Reinforcement.Arrival.At == exactEntry.Epoch.Start(2)
                    && atBoundary.Reinforcement.Joined.At == atBoundary.Reinforcement.Arrival.At
                    && atBoundary.Reinforcement.Arrival.CommandId == exactEnd.Id
                    && atBoundary.Reinforcement.Joined.CommandId == exactEnd.Id,
                    "Exact arrival and admission must share the real End, with arrival first.");
                SaveBill(exact, ReinforcementPolicy(terrain: TerrainCost.Severe), directory, "exp07-reinforcement-exact");

                var proneAt = exactEntry.Epoch.Start(1);
                var fixture = new ConditionCombatFixture(
                    CCApply("reinforcement-prone", "Prone", ReinforcingCompanion, at: new ConditionStamp(proneAt)),
                    CCApply("reinforcement-edge-restrained", "Restrained", ReinforcingCompanion,
                        at: new ConditionStamp(exactEntry.Epoch.Start(2))),
                    new ConditionFixtureEvent(ReinforcingCompanion, ConditionOperation.Cure("event.reinforcement-edge-cure",
                        new ConditionStamp(exactEntry.Epoch.Start(3)), "Restrained")));
                var late = ReinforcementStaged(ReinforcementPolicy(conditions: fixture, terrain: TerrainCost.Severe));
                var lateEntry = EnterLater(late);
                EndReinforcementTurn(late);
                LaterCommit(late, CCCommand(late, "reinforcement-prone", ReinforcingCompanion));
                LaterCommit(late, ReinforcementCommand(late));
                EndReinforcementTurn(late);
                var partial = late.Capture();
                var edge = partial.WorldTraversals.Single(x => x.ActorId == ReinforcingCompanion);
                var position = WorldPositionResolver.Position(partial, ReinforcingCompanion);
                Require(partial.RuleClock == lateEntry.Epoch.Start(2) && partial.Reinforcement.Pending
                    && partial.Reinforcement.Arrival == null && partial.RandomState == lateEntry.Draws.Last().RandomAfter
                    && edge.DistanceFeet == new RuleQuantity(15, 4) && position.X == new RuleQuantity(5, 4)
                    && partial.WorldActivityIntervals.Single(x => x.ActorId == ReinforcingCompanion).MovementSpent > default(RuleQuantity),
                    "The first End at a true partial edge must preserve position, spending and RNG without entry.");
                var cancelled = SaveBill(late, ReinforcementPolicy(conditions: fixture, terrain: TerrainCost.Severe), directory,
                    "exp07-reinforcement-partial");
                var incapacitated = SaveBill(late, ReinforcementPolicy(conditions: fixture, terrain: TerrainCost.Severe), directory,
                    "exp07-reinforcement-partial-control");
                LaterCommit(incapacitated, CCCommand(incapacitated, "reinforcement-edge-restrained", ReinforcingCompanion));
                var suspended = incapacitated.Capture();
                Require(suspended.Reinforcement.Events.Last().Kind == ReinforcementEventKind.Suspended
                    && suspended.Reinforcement.Events.Last().Reason == "ReinforcementActorIncapable"
                    && WorldPositionResolver.Position(suspended, ReinforcingCompanion) == position,
                    "Actual incapacity lost the partial position or failed to suspend.");
                RejectUnchanged(incapacitated, host, ReinforcementCommand(incapacitated, CommandKind.ResumeWorldStep),
                    "ConditionPreventsMovement");
                EndReinforcementTurn(incapacitated);
                LaterCommit(incapacitated, CCCommand(incapacitated, "reinforcement-edge-cure", ReinforcingCompanion));
                Require(WorldPositionResolver.Position(incapacitated.Capture(), ReinforcingCompanion) == position,
                    "Cure implicitly resumed or moved the actor.");
                LaterCommit(incapacitated, ReinforcementCommand(incapacitated, CommandKind.ResumeWorldStep));
                EndReinforcementTurn(incapacitated);
                Require(incapacitated.Capture().Reinforcement.Joined.At == lateEntry.Epoch.Start(4),
                    "Explicit supported resume after cure did not admit at the next actual end-round.");

                var resolved = new Simulation(ReinforcementPolicy(conditions: fixture, terrain: TerrainCost.Severe),
                    new SnapshotCodec().Decode(Bytes(cancelled)), ExecutionProfile.Laboratory);
                LaterCommit(resolved, ReinforcementCommand(resolved, CommandKind.SuspendWorldStep));
                FinishLaterFight(resolved, true);
                var noLongerNeeded = resolved.Capture();
                Require(noLongerNeeded.Reinforcement.Ended.Kind == ReinforcementEventKind.NoLongerNeeded
                    && noLongerNeeded.Reinforcement.Admission == null && Life(resolved, LaterDefender).Dead
                    && WorldPositionResolver.Position(noLongerNeeded, ReinforcingCompanion) == position
                    && !noLongerNeeded.ClosedEncounters[1].Encounter.Order.Contains(ReinforcingCompanion),
                    "Actual conflict resolution failed to win over the still-pending partial approach.");
                SaveBill(resolved, ReinforcementPolicy(conditions: fixture, terrain: TerrainCost.Severe), directory,
                    "exp07-reinforcement-no-longer-needed");

                LaterCommit(cancelled, ReinforcementCommand(cancelled, CommandKind.CancelReinforcementApproach));
                var stopped = cancelled.Capture();
                Require(stopped.Reinforcement.Ended.Kind == ReinforcementEventKind.Cancelled
                    && stopped.WorldTraversals.Single(x => x.ActorId == ReinforcingCompanion).Status == WorldTraversalStatus.Suspended
                    && stopped.WorldTraversals.Single(x => x.ActorId == ReinforcingCompanion).DistanceFeet == edge.DistanceFeet
                    && stopped.WorldActivityIntervals.Single(x => x.ActorId == ReinforcingCompanion).MovementSpent
                        == partial.WorldActivityIntervals.Single(x => x.ActorId == ReinforcingCompanion).MovementSpent,
                    "Cancellation refunded or moved the real partial traversal.");
                RejectUnchanged(cancelled, host, ReinforcementCommand(cancelled, CommandKind.ResumeWorldStep), "ReinforcementApproachNotPending");
                RejectUnchanged(cancelled, host, ReinforcementCommand(cancelled), "ReinforcementAlreadyAttempted");
                FinishLaterFight(cancelled, true);
                LaterCommit(cancelled, ReinforcementCommand(cancelled, CommandKind.ResumeWorldStep));
                LaterCommit(cancelled, LaterAdvance(cancelled, 2));
                Require(Body(cancelled, ReinforcingCompanion).X == 1 && cancelled.Capture().Reinforcement.Admission == null,
                    "Actual ordinary continuation after exit should retain the cancelled participation outcome.");
                SaveBill(cancelled, ReinforcementPolicy(conditions: fixture, terrain: TerrainCost.Severe), directory,
                    "exp07-reinforcement-cancelled-continued");

                EndReinforcementTurn(late);
                var waiting = late.Capture();
                Require(waiting.Reinforcement.Arrival.At == lateEntry.Epoch.Start(2).AddSeconds(1)
                    && waiting.Reinforcement.Pending && waiting.Encounter.TurnOrdinal == 3
                    && waiting.RandomState == partial.RandomState, "Arrival after E joined during an incumbent round.");
                EndReinforcementTurn(late);
                Require(late.Capture().Reinforcement.Joined.At == lateEntry.Epoch.Start(4)
                    && late.Capture().Encounter.TurnOrdinal == 4 && late.Capture().Encounter.Round == 3,
                    "The late arrival missed the next eligible actual end-round.");
                SaveBill(late, ReinforcementPolicy(conditions: fixture, terrain: TerrainCost.Severe), directory, "exp07-reinforcement-late");
            });

            cases.Add("exp07_companion_reinforcement_authority_incapacity_and_tactical_priority", () =>
            {
                var working = ReinforcementStaged(ReinforcementPolicy(), early: true);
                LaterCommit(working, FarmCommand(working, CommandKind.PlantCrop));
                EnterLater(working);
                RejectUnchanged(working, host, ReinforcementCommand(working), "WorkerBusy");
                Require(ReinforcementPlanting(working.Capture()).Status == CropWorkStatus.Working
                    && working.Capture().Reinforcement.Began == null, "A rejected instruction paused actual labor or created an attempt.");

                var profile = new TestOnlyReinforcementProfile(playerTieBound: false);
                var unbound = ReinforcementStaged(ReinforcementPolicy(profile: profile), early: true);
                EnterLater(unbound);
                RejectUnchanged(unbound, host, ReinforcementCommand(unbound), "ReinforcementTieAuthorityMissing");
                Require(!unbound.DiscoverCommands(host, ReinforcingCompanion).Any(x => x.Command.Kind == CommandKind.BeginReinforcementApproach),
                    "Discovery offered an unbound initiative decision.");

                var sim = ReinforcementStaged(ReinforcementPolicy());
                var entry = EnterLater(sim);
                var begin = ReinforcementCommand(sim);
                var heroOnly = new Authority("TEST_ONLY.host", new[] { PlanHero }, true, true);
                var alternate = new Authority("TEST_ONLY.other", new[] { ReinforcingCompanion }, true, true);
                RejectUnchanged(sim, heroOnly, begin, "NotAuthorized");
                RejectUnchanged(sim, alternate, begin, "ReinforcementControllerUnauthorized");
                Require(sim.QueryCommand(host, begin).Admissible
                    && sim.DiscoverCommands(host, ReinforcingCompanion).Count(x => x.Command.Kind == begin.Kind) == 1,
                    "The bound controller cannot discover or query the exact instruction.");
                RejectUnchanged(sim, host, ReinforcementCommand(sim, actor: PlanHero), "ReinforcementActorUnauthorized");
                RejectUnchanged(sim, host, LaterAdvance(sim, 1, 2), "TacticalDecisionClockPaused");

                LaterStance(sim, CombatStance.Guarded);
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 1, y: 3));
                RejectUnchanged(sim, host, ReinforcementCommand(sim), "Occupied");
                LaterCommit(sim, Tac(sim, CommandKind.EncounterDash));
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 2, y: 2));
                if (TestOnlyClubAttackPolicy.PendingMove(sim.Capture()) != null) LaterCommit(sim, Opportunity(sim, false));
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 3, y: 3));
                RejectUnchanged(sim, host, ReinforcementCommand(sim), "ReinforcementApproachTriggerUnsupported");
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 2, y: 2));
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 1, y: 3));
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 0, y: 4));
                LaterCommit(sim, ReinforcementCommand(sim));
                RejectUnchanged(sim, host, Tac(sim, CommandKind.AttackUnarmed, ReinforcingCompanion),
                    "ReinforcementPreAdmissionCombatUnsupported");
                RejectUnchanged(sim, host, Tac(sim, CommandKind.AttackUnarmed, LaterDefender, actor: ReinforcingCompanion),
                    "ActorOutsideEncounter");
                LaterCommit(sim, ReinforcementCommand(sim, CommandKind.SuspendWorldStep));
                EndReinforcementTurn(sim);
                LaterStance(sim, CombatStance.Guarded);
                LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 0, y: 2));
                Require(TestOnlyClubAttackPolicy.PendingMove(sim.Capture()) != null, "The real incumbent departure did not offer a Reaction.");
                RejectUnchanged(sim, host, Tac(sim, CommandKind.EndRegularTurn), "TacticalChoicePending");
                RejectUnchanged(sim, host, ReinforcementCommand(sim, CommandKind.ResumeWorldStep), "TacticalChoicePending");
                LaterCommit(sim, Opportunity(sim, false));
                LaterCommit(sim, ReinforcementCommand(sim, CommandKind.ResumeWorldStep));
                EndReinforcementTurn(sim);
                Require(sim.Capture().Reinforcement.Joined.At == entry.Epoch.Start(2)
                    && sim.Capture().Reinforcement.Arrival.At == entry.Epoch.Start(1).AddSeconds(1),
                    "A blocked End advanced approach time or lawful resume failed.");
                SaveBill(sim, ReinforcementPolicy(), directory, "exp07-reinforcement-pending-choice-recovered");

                var atEntry = entry.Epoch.Start(1);
                var firstBoundary = entry.Epoch.Start(2);
                var conditions = new ConditionCombatFixture(
                    CCApply("reinforcement-incapacity", "Incapacitated", ReinforcingCompanion,
                        expires: new ConditionStamp(firstBoundary.AddSeconds(1)), at: new ConditionStamp(atEntry)));
                var temporary = ReinforcementStaged(ReinforcementPolicy(conditions: conditions));
                EnterLater(temporary);
                LaterCommit(temporary, ReinforcementCommand(temporary));
                EndReinforcementTurn(temporary);
                LaterCommit(temporary, CCCommand(temporary, "reinforcement-incapacity", ReinforcingCompanion));
                EndReinforcementTurn(temporary);
                var deferred = temporary.Capture();
                Require(deferred.Reinforcement.Events.Last().Kind == ReinforcementEventKind.Deferred
                    && deferred.Reinforcement.Events.Last().Reason == "ReinforcementActorIncapable"
                    && deferred.Reinforcement.Events.Last().At == firstBoundary
                    && deferred.RandomState == deferred.LaterEncounter.Entry.Draws.Last().RandomAfter
                    && !deferred.Encounter.Order.Contains(ReinforcingCompanion),
                    "Temporary incapacity at the real boundary should leave a reason and preserve the pending attempt and RNG.");
                var recovered = SaveBill(temporary, ReinforcementPolicy(conditions: conditions), directory, "exp07-reinforcement-deferred");
                EndReinforcementTurn(recovered);
                Require(recovered.Capture().Reinforcement.Admission == null, "A mid-round recovery admitted the companion early.");
                EndReinforcementTurn(recovered);
                Require(recovered.Capture().Reinforcement.Joined.At == entry.Epoch.Start(4), "The later eligible round did not admit.");
            });

            cases.Add("exp07_companion_reinforcement_seeded_order_and_tie_authority", () =>
            {
                var witness = new List<string>();
                foreach (var expected in new[] {
                    (Seed: 2u, Hero: 14, Defender: 15, Entrant: 18, Order: new[] { ReinforcingCompanion, LaterDefender, PlanHero }),
                    (Seed: 1u, Hero: 18, Defender: 9, Entrant: 13, Order: new[] { PlanHero, ReinforcingCompanion, LaterDefender }),
                    (Seed: 15u, Hero: 7, Defender: 13, Entrant: 3, Order: new[] { LaterDefender, PlanHero, ReinforcingCompanion }),
                    (Seed: 19u, Hero: 19, Defender: 2, Entrant: 19, Order: new[] { PlanHero, ReinforcingCompanion, LaterDefender }),
                    (Seed: 6u, Hero: 10, Defender: 18, Entrant: 18, Order: new[] { LaterDefender, ReinforcingCompanion, PlanHero }),
                    (Seed: 309u, Hero: 13, Defender: 13, Entrant: 13, Order: new[] { LaterDefender, PlanHero, ReinforcingCompanion })
                }) {
                    var sim = ReinforcementStaged(ReinforcementPolicy(expected.Seed), early: true);
                    var entry = EnterLater(sim);
                    LaterCommit(sim, ReinforcementCommand(sim));
                    EndReinforcementTurn(sim);
                    var priorRng = sim.Capture().RandomState;
                    EndReinforcementTurn(sim);
                    var state = sim.Capture();
                    var admission = state.Reinforcement.Admission;
                    var definition = state.Reinforcement.Definition;
                    Require(entry.Draws[0].Total == expected.Hero && entry.Draws[1].Total == expected.Defender
                        && admission.Draw.Total == expected.Entrant && admission.Draw.RandomBefore == priorRng
                        && admission.Draw.RandomAfter == state.RandomState && admission.Draw.WordsConsumed == 1
                        && state.Encounter.Order.SequenceEqual(expected.Order)
                        && definition.PlayerTieChoiceId != "" && definition.DirectorTieChoiceId != definition.PlayerTieChoiceId,
                        "The actual initiative rolls, stable incumbent order or separate tie authorities diverged for seed " + expected.Seed + ".");
                    witness.Add(string.Join("\t", expected.Seed, expected.Hero, expected.Defender, expected.Entrant,
                        priorRng, state.RandomState, string.Join(",", expected.Order), definition.PlayerTieChoiceId, definition.DirectorTieChoiceId));
                }
                System.IO.File.WriteAllLines(System.IO.Path.Combine(directory, "exp07-reinforcement-initiative.tsv"), witness);
            });

            cases.Add("exp07_companion_reinforcement_resource_carry_virtual_markers_and_reaction", () =>
            {
                var delayedEntry = T(11598);
                var admissionAt = T(11604);
                var conditions = new ConditionCombatFixture(
                    new ConditionFixtureEvent(PlanHero, ConditionOperation.Apply("event.reinforcement-original-marker",
                        new ConditionStamp(delayedEntry), new ConditionApplicationData("reinforcement-original-marker",
                            PlanHero, "world.fixed-calendar.start.3868", "Poisoned", new ConditionStamp(admissionAt),
                            "original-regular-start", false))),
                    new ConditionFixtureEvent(PlanHero, ConditionOperation.Apply("event.reinforcement-two-person-marker",
                        new ConditionStamp(delayedEntry), new ConditionApplicationData("reinforcement-two-person-marker",
                            PlanHero, "TEST_ONLY.later-calendar.start.3", "Poisoned", new ConditionStamp(admissionAt.AddSeconds(3)),
                            "original-regular-start", false))));
                var sim = ReinforcementStaged(ReinforcementPolicy(conditions: conditions));
                WorldAdvance(sim, 9, 2);
                var entry = EnterLater(sim);
                LaterCommit(sim, CCCommand(sim, "reinforcement-original-marker"));
                LaterCommit(sim, CCCommand(sim, "reinforcement-two-person-marker"));
                LaterCommit(sim, ReinforcementCommand(sim));
                foreach (string actor in entry.Epoch.Order) {
                    LaterStance(sim, CombatStance.Guarded);
                    LaterCommit(sim, Tac(sim, CommandKind.EncounterDash, actor: actor));
                    EndReinforcementTurn(sim);
                }
                var joined = sim.Capture();
                var newPhase = joined.Reinforcement.Admission.Phase;
                var carry = joined.Reinforcement.Admission.Carried;
                var oldCalendar = joined.WorldSchedule;
                Require(joined.RuleClock == admissionAt && newPhase.Epoch.Order[0] == ReinforcingCompanion
                    && oldCalendar.Start(3868) == admissionAt && WorldActivityIntervalRecord.StartAt(oldCalendar,
                        WorldActivityIntervalRecord.IndexAt(oldCalendar, admissionAt)) == admissionAt
                    && carry.Single(x => x.Interval.ActorId == ReinforcingCompanion).Interval.MovementSpent == new RuleQuantity(5)
                    && ReinforcementInterval(joined, ReinforcingCompanion).MovementSpent == default
                    && ReinforcementInterval(joined, ReinforcingCompanion).ReactionAvailable
                    && joined.WorldIntervals.Where(x => entry.Epoch.Order.Contains(x.ActorId)).All(x => x.DashPaid && x.ActionSpent)
                    && TestOnlyClubAttackPolicy.ActiveStance(joined, LaterDefender) == null
                    && TestOnlyClubAttackPolicy.ActiveStance(joined, PlanHero)?.ExpiresAt == admissionAt.AddSeconds(3)
                    && ViewCondition(sim, "reinforcement-original-marker").EndedAt?.Time == admissionAt
                    && ViewCondition(sim, "reinforcement-two-person-marker").EndedAt == null,
                    "A coincident old activity refresh, old marker or new Start altered the carried resource transaction.");
                Require(joined.Encounter.ActorAt(0) == entry.Epoch.Order[0] && joined.Encounter.ActorAt(1) == entry.Epoch.Order[1]
                    && joined.Encounter.NextOwnStart(1) == admissionAt.AddSeconds(3)
                    && newPhase.Epoch.Start(1) == admissionAt.AddSeconds(2) && newPhase.Epoch.Start(2) == admissionAt.AddSeconds(4),
                    "Historical actor lookup or prospective cadence reinterpreted an old marker.");
                EndReinforcementTurn(sim);
                Require(!ReinforcementInterval(sim.Capture(), LaterDefender).DashPaid && ReinforcementInterval(sim.Capture(), PlanHero).DashPaid,
                    "The second actor’s real Start did not refresh only that actor.");
                EndReinforcementTurn(sim);
                var refreshed = sim.Capture();
                Require(refreshed.Encounter.CurrentActor == PlanHero && refreshed.Encounter.TurnOrdinal == 4
                    && !ReinforcementInterval(refreshed, PlanHero).DashPaid
                    && ViewCondition(sim, "reinforcement-two-person-marker").EndedAt?.Time == admissionAt.AddSeconds(3)
                    && WorldTiming.FindEpoch(refreshed, entry.Epoch.Id).Start(3) == admissionAt.AddSeconds(3),
                    "The old two-person deadline or actual hero refresh moved.");
                EndReinforcementTurn(sim);
                Require(sim.Capture().Encounter.Round == 3 && sim.Capture().Encounter.TurnOrdinal == 5
                    && sim.Capture().RuleClock == admissionAt.AddSeconds(6),
                    "The new cadence did not produce a continuous three-person round.");
                SaveBill(sim, ReinforcementPolicy(conditions: conditions), directory, "exp07-reinforcement-coincident-markers");

                var reacting = ReinforcementStaged(ReinforcementPolicy(15), early: true);
                EnterLater(reacting);
                LaterCommit(reacting, ReinforcementCommand(reacting));
                EndReinforcementTurn(reacting);
                EndReinforcementTurn(reacting);
                var prior = reacting.Capture();
                Require(prior.Encounter.Order.SequenceEqual(new[] { LaterDefender, PlanHero, ReinforcingCompanion })
                    && ReinforcementInterval(prior, ReinforcingCompanion).LastStart == -1
                    && ReinforcementInterval(prior, ReinforcingCompanion).ReactionAvailable,
                    "The late entrant lacks its one pre-first-turn Reaction.");
                LaterStance(reacting, CombatStance.Guarded);
                LaterCommit(reacting, Tac(reacting, CommandKind.TacticalStep, x: 1, y: 4));
                LaterCommit(reacting, Tac(reacting, CommandKind.TacticalStep, x: 2, y: 3));
                if (TestOnlyClubAttackPolicy.PendingMove(reacting.Capture()) != null) LaterCommit(reacting, Opportunity(reacting, false));
                LaterCommit(reacting, Tac(reacting, CommandKind.TacticalStep, x: 3, y: 3));
                Require(Opportunity(reacting, true).Actor == ReinforcingCompanion, "The real hostile departure did not offer the entrant's Reaction.");
                LaterCommit(reacting, Opportunity(reacting, true, press: PressHitInstruction.KeepExisting));
                var spent = reacting.Capture();
                Require(spent.MeleeAttacks.Last().Opportunity && spent.MeleeAttacks.Last().AttackerId == ReinforcingCompanion
                    && !ReinforcementInterval(spent, ReinforcingCompanion).ReactionAvailable
                    && ReinforcementInterval(spent, ReinforcingCompanion).LastStart == -1,
                    "The entrant did not spend its initial Reaction before its first actual Start.");
                EndReinforcementTurn(reacting);
                Require(!ReinforcementInterval(reacting.Capture(), ReinforcingCompanion).ReactionAvailable,
                    "Another actor's actual Start refreshed the entrant.");
                EndReinforcementTurn(reacting);
                Require(ReinforcementInterval(reacting.Capture(), ReinforcingCompanion).ReactionAvailable
                    && ReinforcementInterval(reacting.Capture(), ReinforcingCompanion).LastStart == 4,
                    "The entrant's own actual first Start did not refresh the spent Reaction.");
                SaveBill(reacting, ReinforcementPolicy(15), directory, "exp07-reinforcement-initial-reaction");
            });

            cases.Add("exp07_companion_reinforcement_unarmed_archive_work_and_canonical_replay", () =>
            {
                var sim = ReinforcementStaged(ReinforcementPolicy());
                const string filledSkin = "TEST_ONLY.pack-skin";
                const string emptySkin = TestOnlyFillingPolicy.CompanionSkinId;
                PlanWalk(sim, 0, 1);
                LaterCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, filledSkin, SaleBuyer, HandlingKind.Handover));
                LaterCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, emptySkin, SaleBuyer,
                    HandlingKind.Handover, ReinforcingCompanion));
                LaterCommit(sim, IC(sim, CommandKind.StartWaterFill, "TEST_ONLY.pack-water", new InventoryRequest(Q(1), emptySkin), SaleBuyer));
                PlanWalk(sim, 0, -1);

                var entry = EnterLater(sim);
                var entered = sim.Capture();
                var beforeWork = entered.WaterFills.Single();
                LaterCommit(sim, ReinforcementCommand(sim));
                EndReinforcementTurn(sim);
                EndReinforcementTurn(sim);
                var joined = sim.Capture();
                var afterWork = joined.WaterFills.Single();
                Require(afterWork.WorkerId == SaleBuyer && afterWork.Status == WaterFillStatus.Working
                    && afterWork.Progress == beforeWork.Progress.AddSeconds(6)
                    && joined.Work.WorkerIntervals.Count(x => x.JobId == afterWork.Id) == 1
                    && !joined.Encounter.Order.Contains(SaleBuyer)
                    && ReinforcementPlanting(joined).Progress == T(2),
                    "Independent real water-filling labor was duplicated, paused or pulled into the roster.");
                var replay = SaveBill(sim, ReinforcementPolicy(), directory, "exp07-reinforcement-admitted-with-remote-work");

                var codec = new SnapshotCodec();
                var altered = sim.Capture();
                var record = altered.Reinforcement;
                var rows = record.Events.Select(x => x.Kind == ReinforcementEventKind.Arrived
                    ? new ReinforcementEvent(x.Kind, x.Revision, x.CommandId, x.At.AddSeconds(1), x.Reason, x.Distance) : x);
                altered.Reinforcement = new ReinforcementRecord(record.Definition, rows, record.Admission);
                var forged = codec.Decode(codec.Encode(altered));
                bool rejected = false;
                try { new Simulation(ReinforcementPolicy(), forged, ExecutionProfile.Laboratory); }
                catch (ArgumentException error) { rejected = error.Message.Contains("InvalidSharedWorldReplay"); }
                Require(rejected, "A structurally plausible forged arrival bypassed canonical replay.");

                foreach (var run in new[] { sim, replay }) {
                    var ready = run.Capture();
                    Require(ready.Encounter.CurrentActor == ReinforcingCompanion && Body(run, ReinforcingCompanion).X == 1,
                        "The genuine companion turn is missing at the established entry.");
                    LaterStance(run);
                    LaterCommit(run, Tac(run, CommandKind.AttackUnarmed, LaterDefender));
                    var attacked = run.Capture();
                    var attack = attacked.MeleeAttacks.Last();
                    Require(attack.AttackerId == ReinforcingCompanion && attack.TargetId == LaterDefender
                        && attack.WeaponId == CombatProfileIds.OrdinaryUnarmed && !attack.Opportunity
                        && attack.TurnOrdinal == ready.Encounter.TurnOrdinal
                        && ReinforcementInterval(attacked, ReinforcingCompanion).ActionSpent
                        && attacked.RandomState != ready.RandomState,
                        "The companion's actual unarmed Action did not reach the shared combat engine.");
                    EndReinforcementTurn(run);
                    FinishLaterFight(run, true);
                    var closed = run.Capture();
                    var archived = closed.ClosedEncounters.Single(x => x.Encounter.Id == entered.Encounter.Id);
                    var phase = archived.Encounter.RosterPhase;
                    Require(closed.Encounter == null && !closed.InventoryCombat && closed.ClosedEncounters.Length == 2
                        && archived.Encounter.InitialOrder.SequenceEqual(entry.Epoch.Order) && phase.FirstTurn == 2
                        && phase.Epoch.Order.Contains(ReinforcingCompanion) && archived.Encounter.ActorAt(0) == entry.Epoch.Order[0]
                        && archived.ClosedAt == archived.Encounter.StartAt(archived.Encounter.TurnOrdinal + 1)
                        && closed.ClosedEncounters[0].ClosedRevision == entered.ClosedEncounters[0].ClosedRevision
                        && closed.CharterAttempt.Returned.Revision == entered.CharterAttempt.Returned.Revision
                        && Life(run, LaterDefender).Dead && ReinforcementPlanting(closed).Progress == T(2)
                        && closed.Clubs.Single(x => x.OwnerId == ReinforcingCompanion).HeldBy == "",
                        "Exit lost a roster phase, rewrote earlier provenance or created a new consequence.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "The actual companion Action and physical exit did not replay byte-identically.");
                var continuation = SaveBill(sim, ReinforcementPolicy(), directory, "exp07-reinforcement-closed");
                foreach (var run in new[] { sim, continuation }) {
                    var closed = run.Capture();
                    PlanWalk(run, 0, -1);
                    var continued = run.Capture();
                    Require(Body(run).Y == 2 && continued.Reinforcement.Admission.Phase.Epoch.ProcessedSlot
                        > closed.Reinforcement.Admission.Phase.Epoch.ProcessedSlot && continued.Encounter == null
                        && continued.ClosedEncounters[1].Encounter.TurnOrdinal == closed.ClosedEncounters[1].Encounter.TurnOrdinal,
                        "Post-exit ordinary movement did not continue the virtual phase, or changed the actual archive.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(continuation)), "Post-exit ordinary continuation replay diverged.");
                SaveBill(sim, ReinforcementPolicy(), directory, "exp07-reinforcement-continued");
            });
        }
    }
}
#endif
