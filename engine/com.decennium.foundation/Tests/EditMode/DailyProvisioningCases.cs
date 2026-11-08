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
        private static TestOnlySharedWorldPolicy ProvisioningPolicy()
            => new TestOnlySharedWorldPolicy().EnableDailyProvisioning();

        private static Simulation RestoreProvisioning(Simulation simulation, TestOnlySharedWorldPolicy policy = null)
        {
            policy = policy ?? ProvisioningPolicy();
            return new Simulation(policy, new SnapshotCodec().Decode(Bytes(simulation)), ExecutionProfile.Laboratory);
        }

        private static string ProvisioningHandle(Simulation simulation, string lot, RuleQuantity amount,
            HandlingKind handling, string actor = TestOnlyPolicy.ActorId, string destination = "")
        {
            WorldCommit(simulation, IC(simulation, CommandKind.HandleInventory, lot,
                new InventoryRequest(amount, destination, handling), actor));
            return "inventory." + simulation.Capture().Revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".lot";
        }

        private static uint StrainedDeathSaveSequenceSeed(int woundSaveModifier)
        {
            const long mishapAt = 172800;
            for (uint seed = 1; seed < 1000000; seed++) {
                var damage = DiceStream.Draw(seed, 4);
                var hit = PlaytestDamageDice.Resolve(new LifeState(26, 1), damage.Value + 1,
                    new RuleTime(mishapAt), damage.NextState, constitutionSaveModifier: woundSaveModifier);
                if (hit.Outcome.State.Hp != 0 || hit.Outcome.State.Dead || hit.Outcome.State.Stable) continue;
                uint next = hit.NextRandomState;
                var first = PlaytestDice.RollD20(next); next = first.NextRandomState;
                var second = PlaytestDice.RollD20(next); next = second.NextRandomState;
                var third = PlaytestDice.RollD20(next); next = third.NextRandomState;
                var fourth = PlaytestDice.RollD20(next);
                if (first.Natural + -1 >= 10 && second.Natural + -1 >= 10
                    && third.Natural == 10 && fourth.Natural == 11) return seed;
            }
            throw new Exception("No deterministic Strain death-save sequence fixture seed.");
        }

        private static void AddDailyProvisioningCases(Dictionary<string, Action> cases, string directory)
        {
            var codec = new SnapshotCodec();
            var host = TestOnlySharedWorldPolicy.Host();
            void AdvanceTo(Simulation simulation, long targetSeconds)
            {
                var now = simulation.Capture().RuleClock;
                long remaining = checked(targetSeconds * now.Denominator - now.Numerator);
                if (remaining < 0) throw new ArgumentOutOfRangeException(nameof(targetSeconds));
                if (remaining != 0) WorldAdvance(simulation, checked((int)remaining), checked((int)now.Denominator));
            }
            void RunOneLegalStep(Simulation simulation, string actor)
            {
                var rejected = new List<string>();
                foreach (var direction in new[] { (1, 0), (0, 1), (-1, 0), (0, -1) }) {
                    var command = IC(simulation, CommandKind.BeginWorldStep, "run", actor: actor,
                        x: direction.Item1, y: direction.Item2);
                    var query = simulation.QueryCommand(host, command);
                    if (query.Supported && query.Admissible) {
                        WorldCommit(simulation, command);
                        return;
                    }
                    rejected.Add(direction.Item1 + "," + direction.Item2 + ":" + query.Code + "/" + query.Admissible);
                }
                var state = simulation.Capture();
                var body = state.Actors.Single(x => x.Id == actor);
                throw new Exception("No legal exploration Dash step was available for " + actor + " at " + body.X + "," + body.Y
                    + " (clock=" + state.RuleClock + ", combat=" + state.InventoryCombat + ", speed="
                    + TestOnlyClubAttackPolicy.WalkingSpeed(state, actor) + ", queries=" + string.Join(";", rejected) + ").");
            }
            void WaitForNextDashAllowance(Simulation simulation, string actor)
            {
                var state = simulation.Capture();
                if (state.WorldSchedule.Order.Contains(actor)) {
                    long priorStart = state.WorldIntervals.Single(x => x.ActorId == actor).LastStart;
                    for (int interval = 0; interval < 4
                        && simulation.Capture().WorldIntervals.Single(x => x.ActorId == actor).LastStart == priorStart; interval++)
                        WorldAdvance(simulation, 6);
                } else {
                    long priorIndex = state.WorldActivityIntervals.Single(x => x.ActorId == actor).IntervalIndex;
                    for (int interval = 0; interval < 2
                        && simulation.Capture().WorldActivityIntervals.Single(x => x.ActorId == actor).IntervalIndex == priorIndex; interval++)
                        WorldAdvance(simulation, 6);
                }
            }
            TestOnlySharedWorldPolicy RestDebtPolicy(TestOnlyRestDebtProfile restProfile = null)
                => new TestOnlySharedWorldPolicy().EnableCampGreensAssignments()
                    .EnableDailyProvisioning().EnableRestDebt(restProfile);
            Simulation RestoreRestDebt(Simulation simulation, TestOnlySharedWorldPolicy policy)
                => new Simulation(policy, codec.Decode(Bytes(simulation)), ExecutionProfile.Laboratory);
            void ScheduleRest(Simulation simulation, long day, RestWatchSlot slot, string actor = TestOnlyPolicy.ActorId)
                => WorldCommit(simulation, IC(simulation, CommandKind.ScheduleRestWatch,
                    "day." + day.ToString(System.Globalization.CultureInfo.InvariantCulture), actor: actor, x: (int)slot));
            void AdvanceRestDebt(Simulation simulation, int seconds)
            {
                var command = IC(simulation, CommandKind.AdvanceClock, actor: TestOnlyPolicy.ActorId,
                    x: seconds, y: 1, id: "rest.clock." + simulation.Capture().Revision.ToString(System.Globalization.CultureInfo.InvariantCulture));
                var result = simulation.Execute(TestOnlySharedWorldPolicy.Host(), command);
                Require(result.Outcome == Outcome.Committed, command.Id + " (" + command.Kind + "): " + result.Code
                    + " [target=" + command.Target + ", x=" + command.X + ", y=" + command.Y + ", inventory="
                    + (command.Inventory == null) + ", clock=" + simulation.Capture().RuleClock + "]");
            }
            void StartAssignedPlanting(Simulation simulation, string cropId)
            {
                var request = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.CropPlanting, cropId);
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.AssignExpeditionWork,
                    request: request, actor: TestOnlyPolicy.CompanionId));
                var assignment = simulation.Capture().ExpeditionAssignments.Single(x => x.WorkerId == TestOnlyPolicy.CompanionId);
                Require(assignment.Status == ExpeditionAssignmentStatus.Ready,
                    "Companion was not already at the registered Camp Greens work site.");
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.StartExpeditionWork,
                    assignment.Id, actor: TestOnlyPolicy.CompanionId));
            }
            string[] StrainSemantics(Snapshot s) => s.ExpeditionStrainGains
                .Where(x => x.ActorId == TestOnlyPolicy.ActorId)
                .OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.GainSequence).ThenBy(x => x.Id, StringComparer.Ordinal)
                .Select(x => x.CauseKind + "|" + x.At + "|" + x.GainSequence + "|" + x.LevelBefore + "|"
                    + x.AttemptedAmount + "|" + x.AddedAmount + "|" + x.OrdinaryRemovable + "|"
                    + x.RemovalGateMet + "|" + x.Endpoint).ToArray();
            string[] DebtSemantics(Snapshot s) => s.RestDebtEvents.Where(x => x.ActorId == TestOnlyPolicy.ActorId)
                .OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.EventSequence)
                .Select(x => x.Kind + "|" + x.At + "|" + x.DeadlineBefore + "|" + x.DeadlineAfter + "|"
                    + (x.StrainGainId != "") + "|" + x.EventSequence).ToArray();

            cases.Add("daily_provisioning_profile_is_test_only_fingerprinted_and_restorable", () => {
                var policy = ProvisioningPolicy();
                var simulation = World(policy);
                var initial = simulation.Capture();
                Require(initial.SchemaVersion == Snapshot.DailyProvisioningSchema && initial.TestOnly
                    && initial.DailyProvisioningSettlements.Length == 0 && initial.ExpeditionStrainGains.Length == 0
                    && initial.RuleClock == default(RuleTime),
                    "Daily profile did not begin at its fixed TEST_ONLY epoch.");
                var restored = RestoreProvisioning(simulation);
                Require(Bytes(simulation).SequenceEqual(Bytes(restored)), "Daily profile failed byte-exact codec restore.");
                Throws<InvalidOperationException>(() => new Simulation(policy, initial, ExecutionProfile.Release));
                Throws<InvalidOperationException>(() => policy.EnableDailyProvisioning());
            });

            cases.Add("daily_provisioning_exploration_intake_boundary_restore_and_replay", () => {
                var policy = ProvisioningPolicy();
                var simulation = World(policy);

                // Explore to the prepared plot and hand one physical pound of the existing rations
                // to the companion. No resource is created by the transfer.
                foreach (var step in new[] { new[] { 1, 0 }, new[] { 1, 0 }, new[] { 1, 0 }, new[] { 0, 1 }, new[] { 0, 1 } }) {
                    WorldStep(simulation, step[0], step[1]);
                    WorldAdvance(simulation, 1);
                }
                Require(simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 3
                    && simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2,
                    "Exploration route did not reach the plot edge.");
                string meal = ProvisioningHandle(simulation, TestOnlyInventoryPolicy.FoodId, new RuleQuantity(1),
                    HandlingKind.Handover, destination: TestOnlyPolicy.CompanionId);
                Require(simulation.Capture().InventoryLots.Single(x => x.LotId == meal).OwnerId == TestOnlyPolicy.ActorId
                    && simulation.Capture().Work.Lots.Single(x => x.Id == meal).CustodianId == TestOnlyPolicy.CompanionId,
                    "Handover failed to preserve ownership and transfer custody.");

                // The companion begins a real 15-minute meal one second before midnight. A one-second
                // vessel pickup by the lead crosses the endpoint while that intake completes.
                WorldAdvance(simulation, 85494);
                WorldCommit(simulation, IC(simulation, CommandKind.StartIntake, meal,
                    new InventoryRequest(new RuleQuantity(1)), TestOnlyPolicy.CompanionId));
                var beforeBoundary = Path.Combine(directory, "daily-provisioning-before-boundary.ddsave");
                new FileSaveStore().Save(beforeBoundary, simulation.Capture());
                simulation = new Simulation(policy, new FileSaveStore().Load(beforeBoundary), ExecutionProfile.Laboratory);
                WorldAdvance(simulation, 899);
                Require(simulation.Capture().RuleClock == T(86399)
                    && simulation.Capture().Intakes.Single().Status == IntakeStatus.Working,
                    "Saved intake did not remain partial one second before midnight.");
                var beforeDirectCrossing = Bytes(simulation);
                simulation = new Simulation(policy, codec.Decode(beforeDirectCrossing), ExecutionProfile.Laboratory);
                var boundaryHandling = IC(simulation, CommandKind.HandleInventory, TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Drop));
                WorldCommit(simulation, boundaryHandling);

                var state = simulation.Capture();
                var companionSettlement = state.DailyProvisioningSettlements.Single(x => x.DayOrdinal == 0
                    && x.ActorId == TestOnlyPolicy.CompanionId);
                var leadSettlement = state.DailyProvisioningSettlements.Single(x => x.DayOrdinal == 0
                    && x.ActorId == TestOnlyPolicy.ActorId);
                var intake = state.Intakes.Single();
                var evidence = state.DailyProvisioningConsumption.Single(x => x.SettlementId == companionSettlement.Id);
                Require(state.RuleClock == T(86400) && intake.Status == IntakeStatus.Complete
                    && intake.EndedAt == T(86400) && evidence.Amount == new RuleQuantity(1)
                    && evidence.IntakeId == intake.Id && evidence.LotId == meal && evidence.ReservationId == intake.ReservationId
                    && companionSettlement.FoodConsumed == new RuleQuantity(1) && companionSettlement.FoodShortfall
                    && companionSettlement.WaterShortfall && companionSettlement.StrainGainId != ""
                    && leadSettlement.FoodConsumed == default(RuleQuantity) && leadSettlement.StrainGainId != "",
                    "Boundary settlement did not credit the completed real intake once before closing both days.");
                byte[] closed = Bytes(simulation);
                Require(simulation.Execute(host, boundaryHandling).Outcome == Outcome.Duplicate && closed.SequenceEqual(Bytes(simulation)),
                    "Retried direct boundary crossing duplicated the settlement or its Strain gain.");

                // Intake started after closure cannot rewrite day zero. It remains ordinary work
                // and is eligible only for the next half-open day.
                WorldCommit(simulation, IC(simulation, CommandKind.StartIntake, TestOnlyInventoryPolicy.WaterId,
                    new InventoryRequest(new RuleQuantity(1)), TestOnlyPolicy.ActorId));
                Require(simulation.Capture().DailyProvisioningConsumption.All(x => x.SettlementId != leadSettlement.Id),
                    "A same-time late intake rewrote the closed day.");
                simulation = RestoreProvisioning(simulation);
                Require(Bytes(simulation).SequenceEqual(Bytes(RestoreProvisioning(simulation))),
                    "Continued daily profile changed across a second save/restore.");
            });

            cases.Add("daily_provisioning_one_intake_is_attributed_across_both_midnight_intervals", () => {
                var policy = ProvisioningPolicy();
                var simulation = World(policy);
                foreach (var step in new[] { new[] { 1, 0 }, new[] { 1, 0 }, new[] { 1, 0 }, new[] { 0, 1 }, new[] { 0, 1 } }) {
                    WorldStep(simulation, step[0], step[1]);
                    WorldAdvance(simulation, 1);
                }
                string meal = ProvisioningHandle(simulation, TestOnlyInventoryPolicy.FoodId, new RuleQuantity(2),
                    HandlingKind.Handover, destination: TestOnlyPolicy.CompanionId);
                AdvanceTo(simulation, 85500);
                WorldCommit(simulation, IC(simulation, CommandKind.StartIntake, meal,
                    new InventoryRequest(new RuleQuantity(2)), TestOnlyPolicy.CompanionId));
                WorldAdvance(simulation, 899);
                Require(simulation.Capture().RuleClock == T(86399)
                    && simulation.Capture().Intakes.Single().Status == IntakeStatus.Working,
                    "The two-pound intake did not remain active one second before midnight.");

                byte[] checkpoint = Bytes(simulation);
                simulation = new Simulation(policy, codec.Decode(checkpoint), ExecutionProfile.Laboratory);
                var replay = new Simulation(policy, codec.Decode(checkpoint), ExecutionProfile.Laboratory);
                WorldAdvance(simulation, 1); WorldAdvance(replay, 1);
                WorldAdvance(simulation, 900); WorldAdvance(replay, 900);
                Require(Bytes(simulation).SequenceEqual(Bytes(replay)),
                    "The same saved intake diverged across the midnight split.");
                var dayZero = simulation.Capture();
                var firstSettlement = dayZero.DailyProvisioningSettlements.Single(x => x.DayOrdinal == 0
                    && x.ActorId == TestOnlyPolicy.CompanionId);
                var firstEvidence = dayZero.DailyProvisioningConsumption.Where(x => x.SettlementId == firstSettlement.Id).ToArray();
                Require(dayZero.RuleClock == T(87300) && dayZero.Intakes.Single().Status == IntakeStatus.Complete
                    && firstSettlement.FoodConsumed == new RuleQuantity(1)
                    && firstEvidence.Length == 1 && firstEvidence[0].IntakeId == dayZero.Intakes.Single().Id
                    && firstEvidence[0].LotId == meal && firstEvidence[0].ReservationId == dayZero.Intakes.Single().ReservationId
                    && firstEvidence[0].Amount == new RuleQuantity(1),
                    "The first half-open day did not receive exactly the intake's pre-midnight pound.");

                byte[] completedIntake = Bytes(simulation);
                simulation = new Simulation(policy, codec.Decode(completedIntake), ExecutionProfile.Laboratory);
                replay = new Simulation(policy, codec.Decode(completedIntake), ExecutionProfile.Laboratory);
                AdvanceTo(simulation, 172800); AdvanceTo(replay, 172800);
                var final = simulation.Capture();
                var secondSettlement = final.DailyProvisioningSettlements.Single(x => x.DayOrdinal == 1
                    && x.ActorId == TestOnlyPolicy.CompanionId);
                var secondEvidence = final.DailyProvisioningConsumption.Where(x => x.SettlementId == secondSettlement.Id).ToArray();
                var reservation = final.Work.Reservations.Single(x => x.Id == final.Intakes.Single().ReservationId);
                Require(Bytes(simulation).SequenceEqual(Bytes(replay)) && final.Intakes.Single().Status == IntakeStatus.Complete
                    && secondSettlement.FoodConsumed == new RuleQuantity(1) && secondEvidence.Length == 1
                    && secondEvidence[0].IntakeId == final.Intakes.Single().Id && secondEvidence[0].LotId == meal
                    && secondEvidence[0].ReservationId == reservation.Id && secondEvidence[0].Amount == new RuleQuantity(1)
                    && reservation.ConsumedAmount == new RuleQuantity(2),
                    "The second half-open day lost attribution or save/restore replay diverged.");
            });

            cases.Add("daily_provisioning_candidate_strain_changes_route_pace_across_one_transaction", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Mapped);
                var wholePolicy = RouteTravelPolicy(routes).EnableDailyProvisioning();
                var whole = World(wholePolicy);
                RouteTravelReachSource(whole);
                AdvanceTo(whole, 171900);
                WorldCommit(whole, RouteTravelCommand(whole, CommandKind.StartRouteTravel, "provisioning.route.whole"));
                WorldAdvance(whole, 4500);

                var splitPolicy = RouteTravelPolicy(RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Mapped)).EnableDailyProvisioning();
                var split = World(splitPolicy);
                RouteTravelReachSource(split);
                AdvanceTo(split, 171900);
                WorldCommit(split, RouteTravelCommand(split, CommandKind.StartRouteTravel, "provisioning.route.split"));
                WorldAdvance(split, 900);
                var boundaryView = split.Capture();
                int boundaryLevel = ExpeditionStrainRules.Current(boundaryView, TestOnlyPolicy.ActorId).Level;
                var boundaryEffort = boundaryView.RouteTravels.Single().NominalEffort;
                Require(boundaryLevel == 2 && boundaryEffort == T(800),
                    "The boundary did not settle the second Strain level after the first 900 seconds of route effort. Clock="
                    + boundaryView.RuleClock + ", level=" + boundaryLevel + ", effort=" + boundaryEffort + ", speed="
                    + TestOnlyClubAttackPolicy.WalkingSpeed(boundaryView, TestOnlyPolicy.ActorId) + ".");
                byte[] afterBoundary = Bytes(split);
                split = new Simulation(splitPolicy, codec.Decode(afterBoundary), ExecutionProfile.Laboratory);
                var restored = new Simulation(splitPolicy, codec.Decode(afterBoundary), ExecutionProfile.Laboratory);
                WorldAdvance(split, 3600); WorldAdvance(restored, 3600);
                var wholeEffort = whole.Capture().RouteTravels.Single().NominalEffort;
                var splitEffort = split.Capture().RouteTravels.Single().NominalEffort;
                Require(wholeEffort == T(2400) && splitEffort == wholeEffort
                    && Bytes(split).SequenceEqual(Bytes(restored)),
                    "A whole boundary-crossing route advance used stale candidate Strain, or restored continuation diverged. Whole="
                    + wholeEffort + ", split=" + splitEffort + ".");
            });

            cases.Add("daily_provisioning_candidate_strain_interrupts_work_inside_boundary_transaction", () => {
                var workPolicy = ProvisioningPolicy();
                var work = World(workPolicy);
                foreach (var step in new[] { new[] { 1, 0 }, new[] { 1, 0 }, new[] { 1, 0 }, new[] { 0, 1 }, new[] { 0, 1 } }) {
                    WorldStep(work, step[0], step[1]);
                    WorldAdvance(work, 1);
                }
                string meal = ProvisioningHandle(work, TestOnlyInventoryPolicy.FoodId, new RuleQuantity(2),
                    HandlingKind.Handover, destination: TestOnlyPolicy.CompanionId);
                AdvanceTo(work, 431100);
                Require(ExpeditionStrainRules.Current(work.Capture(), TestOnlyPolicy.CompanionId).Level == 4,
                    "The work fixture did not reach the pre-incapacitation Strain level.");
                WorldCommit(work, IC(work, CommandKind.StartIntake, meal,
                    new InventoryRequest(new RuleQuantity(2)), TestOnlyPolicy.CompanionId));
                WorldAdvance(work, 899);
                byte[] beforeIncapacitation = Bytes(work);
                work = new Simulation(workPolicy, codec.Decode(beforeIncapacitation), ExecutionProfile.Laboratory);
                var workReplay = new Simulation(workPolicy, codec.Decode(beforeIncapacitation), ExecutionProfile.Laboratory);
                WorldAdvance(work, 1); WorldAdvance(workReplay, 1);
                var interrupted = work.Capture();
                var intake = interrupted.Intakes.Single();
                var claim = interrupted.Work.Reservations.Single(x => x.Id == intake.ReservationId);
                Require(Bytes(work).SequenceEqual(Bytes(workReplay)) && intake.Status == IntakeStatus.Interrupted
                    && ExpeditionStrainRules.Current(interrupted, TestOnlyPolicy.CompanionId).Level == 5
                    && claim.ConsumedAmount == new RuleQuantity(1) && claim.ReleasedAmount == new RuleQuantity(1),
                    "The exact fifth-day Strain transaction did not interrupt active food work after preserving consumed labor and stock. Status="
                    + intake.Status + ", level=" + ExpeditionStrainRules.Current(interrupted, TestOnlyPolicy.CompanionId).Level
                    + ", consumed=" + claim.ConsumedAmount + ", released=" + claim.ReleasedAmount + ", clock=" + interrupted.RuleClock + ".");
            });

            cases.Add("daily_provisioning_effective_maximum_bounds_healing_and_dose_attribution", () => {
                var policy = ManufacturePolicy(TacticalSeed(6, 4, 3),
                    crafting: new SharedCraftingFixture(heroHp: 17)).EnableDailyProvisioning();
                var simulation = World(policy);
                LearnManufacturing(simulation);
                ManufactureStart(simulation);
                WorldAdvance(simulation, 14400);
                AdvanceTo(simulation, 4 * 86400);
                var beforeWork = simulation.Capture();
                Require(ExpeditionStrainRules.Current(beforeWork, TestOnlyPolicy.ActorId).Level == 4
                    && beforeWork.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).MaximumHp == 26
                    && beforeWork.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).Hp == 17,
                    "The life fixture did not retain base HP 26 and current HP 17 at Strain level four.");
                var criticalAuthority = new ActorLifeRecord(TestOnlyPolicy.ActorId, 26, 17, 0,
                    new[] { 0, 1, 2 }, false, false, true, 0, 0, null, 0, false, Array.Empty<string>());
                var criticalLife = ActorLifeRules.ReadForResolution(beforeWork, criticalAuthority);
                var criticalHeal = PlaytestLife.Heal(criticalLife, 12);
                var thresholdDamage = PlaytestLife.DamageAt(new LifeState(criticalLife.MaximumHp, 1), 20, T(345600));
                Require(criticalLife.MaximumHp == 19 && criticalHeal.Hp == 18 && thresholdDamage.State.Dead
                    && criticalAuthority.MaximumHp == 26,
                    "Critical healing ceiling or instant-death damage threshold did not use effective maximum HP while preserving base authority.");

                foreach (var step in new[] { (0, 1), (0, 1), (0, 1), (1, 0), (1, 0) }) {
                    WorldStep(simulation, step.Item1, step.Item2);
                    WorldAdvance(simulation, 2);
                }
                WorldAdvance(simulation, 1);
                BeginEncounter(simulation);
                byte[] readyToHeal = Bytes(simulation);
                simulation = new Simulation(policy, codec.Decode(readyToHeal), ExecutionProfile.Laboratory);
                var replay = new Simulation(policy, codec.Decode(readyToHeal), ExecutionProfile.Laboratory);
                for (int turn = 0; simulation.Capture().Encounter.CurrentActor != TestOnlyPolicy.ActorId; turn++) {
                    Require(turn < 4, "The saved encounter never returned control to the injured lead.");
                    var current = simulation.Capture();
                    if (!current.Stances.Any(x => x.TurnOrdinal == current.Encounter.TurnOrdinal)) {
                        WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                            stance: (int)CombatStance.Aggressive));
                        WorldCommit(replay, Tac(replay, CommandKind.SelectCombatStance,
                            stance: (int)CombatStance.Aggressive));
                    }
                    WorldCommit(simulation, Tac(simulation, CommandKind.EndRegularTurn));
                    WorldCommit(replay, Tac(replay, CommandKind.EndRegularTurn));
                }
                string dose = simulation.Capture().AlchemyDoses[0].Id;
                WorldCommit(simulation, DoseCommand(simulation, dose));
                WorldCommit(replay, DoseCommand(replay, dose));
                var view = simulation.Capture();
                var spent = view.AlchemyDoses.Single(x => x.Id == dose);
                var life = view.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId);
                Require(Bytes(simulation).SequenceEqual(Bytes(replay)) && spent.Spent
                    && spent.PotentialHealing >= 2 && spent.ActualHealing == 2
                    && life.MaximumHp == 26 && life.Hp == 19,
                    "Strain's effective HP ceiling did not bound real dose healing and its recorded actual healing. Potential="
                    + spent.PotentialHealing + ", actual=" + spent.ActualHealing + ", HP=" + life.Hp
                    + ", base maximum=" + life.MaximumHp + ".");
            });

            cases.Add("daily_provisioning_dash_deadline_uses_exploration_after_encounter_exit", () => {
                var policy = ConnectedPolicy(1, SeedForD20(20)).EnableDailyProvisioning();
                var simulation = World(policy);
                WorldAdvance(simulation, 3 * 86400);
                for (int step = 0; step < 3 && !simulation.Capture().InventoryCombat; step++) {
                    WorldStep(simulation, 1, 0);
                    if (!simulation.Capture().InventoryCombat) WorldAdvance(simulation, 2);
                }
                Require(simulation.Capture().InventoryCombat
                    && ExpeditionStrainRules.Current(simulation.Capture(), TestOnlyPolicy.ActorId).Level == 3,
                    "The Strain-three approach did not enter the authored connected encounter.");
                for (int turn = 0; simulation.Capture().Encounter.CurrentActor != TestOnlyPolicy.ActorId; turn++) {
                    Require(turn < 4, "The connected encounter never offered the lead a turn.");
                    ConnectedEnd(simulation);
                }
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                    stance: (int)CombatStance.Aggressive));
                TacStep(simulation, 3, 0);
                DefeatConnectedEnemy(simulation);
                WorldCommit(simulation, Tac(simulation, CommandKind.EndFixedEncounter));
                var exited = simulation.Capture();
                Require(!exited.InventoryCombat && exited.Encounter != null
                    && !exited.Encounter.Order.Contains(TestOnlyPolicy.CompanionId),
                    "The fixture did not retain encounter history with the companion off initiative after exit.");

                WaitForNextDashAllowance(simulation, TestOnlyPolicy.ActorId);
                RunOneLegalStep(simulation, TestOnlyPolicy.ActorId);
                var heroLock = simulation.Capture().ExpeditionDashLocks.Single(x => x.ActorId == TestOnlyPolicy.ActorId);
                bool heroDeadlineCorrect = !heroLock.InitiativeAnchored
                    && heroLock.Deadline == heroLock.AppliedAt.AddSeconds(6);
                WorldAdvance(simulation, 2);
                string companionFailure = "";
                try { RunOneLegalStep(simulation, TestOnlyPolicy.CompanionId); }
                catch (Exception error) { companionFailure = error.Message; }
                var companionLock = simulation.Capture().ExpeditionDashLocks.SingleOrDefault(x => x.ActorId == TestOnlyPolicy.CompanionId);
                bool companionDeadlineCorrect = companionLock != null && !companionLock.InitiativeAnchored
                    && companionLock.Deadline == companionLock.AppliedAt.AddSeconds(6);
                byte[] bytes = Bytes(simulation);
                var restored = new Simulation(policy, codec.Decode(bytes), ExecutionProfile.Laboratory);
                Require(heroDeadlineCorrect && companionFailure == "" && companionDeadlineCorrect
                    && Bytes(restored).SequenceEqual(bytes),
                    "Post-exit Dash used retained initiative or failed for an off-calendar actor. Hero lock="
                    + (heroLock == null ? "missing" : heroLock.InitiativeAnchored + "/" + heroLock.Deadline)
                    + ", companion failure=" + companionFailure + ", companion lock="
                    + (companionLock == null ? "missing" : companionLock.InitiativeAnchored + "/" + companionLock.Deadline) + ".");
            });

            cases.Add("daily_provisioning_modified_death_save_gates_d4_and_restores_rng", () => {
                var facts = new SharedCraftingFixture(heroHp: 1,
                    events: new[] { new CraftingMishapFact("strained-death-save", 4,
                        lead: TestOnlyPolicy.ActorId, at: T(172800)) });
                var seedPolicy = CraftPolicy(facts).EnableDailyProvisioning();
                var initial = seedPolicy.Initial();
                var loadout = initial.InitialCharacterLoadouts.SingleOrDefault(x => x.ActorId == TestOnlyPolicy.ActorId);
                int conProficiency = loadout != null && loadout.SavingThrowProficiencyIds.Contains("CON", StringComparer.Ordinal)
                    ? CharacterRuleFacts.ForActor(initial, TestOnlyPolicy.ActorId).ProficiencyBonus : 0;
                int woundSaveModifier = checked(CharacterRuleFacts.ForActor(initial, TestOnlyPolicy.ActorId)
                    .AbilityModifier(CharacterAbility.Constitution)
                    + conProficiency - 1);
                uint seed = StrainedDeathSaveSequenceSeed(woundSaveModifier);
                var policy = CraftPolicy(facts, seed).EnableDailyProvisioning();
                var simulation = World(policy);
                WorldAdvance(simulation, 172800);
                CraftEvent(simulation, "strained-death-save", TestOnlyPolicy.ActorId);
                Require(simulation.Capture().Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).Hp == 0
                    && ExpeditionStrainRules.Current(simulation.Capture(), TestOnlyPolicy.ActorId).Level == 2,
                    "The fixture did not create a living, dying actor under Strain level two.");

                void AdvanceUntilSaves(Simulation value, int saveCount)
                {
                    for (int step = 0; value.Capture().LifeEvents.Count(x => x.ActorId == TestOnlyPolicy.ActorId
                        && x.Kind == LifeEventKind.DeathSave) < saveCount; step++) {
                        Require(step < 16, "The world clock did not reach the requested lead death-save marker.");
                        WorldAdvance(value, 6);
                    }
                }
                AdvanceUntilSaves(simulation, 2);
                var afterTwo = simulation.Capture();
                Require(afterTwo.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).DeathSuccesses == 2,
                    "The natural-11 fixture rolls did not establish two modified successes.");
                byte[] checkpoint = Bytes(simulation);
                simulation = new Simulation(policy, codec.Decode(checkpoint), ExecutionProfile.Laboratory);
                var replay = new Simulation(policy, codec.Decode(checkpoint), ExecutionProfile.Laboratory);
                AdvanceUntilSaves(simulation, 3); AdvanceUntilSaves(replay, 3);
                var third = simulation.Capture().LifeEvents.Where(x => x.ActorId == TestOnlyPolicy.ActorId
                    && x.Kind == LifeEventKind.DeathSave).OrderBy(x => x.Revision).ElementAt(2);
                var d20 = PlaytestDice.RollD20(third.RandomBefore);
                Require(Bytes(simulation).SequenceEqual(Bytes(replay)) && third.Natural == 10
                    && third.RecoveryD4 == 0 && third.WordsConsumed == 1
                    && third.RandomAfter == d20.NextRandomState
                    && simulation.Capture().Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).DeathFailures == 1,
                    "Natural 10 with Strain's -1 modifier incorrectly drew stable-recovery d4 or advanced RNG. Natural="
                    + third.Natural + ", d4=" + third.RecoveryD4 + ", words=" + third.WordsConsumed + ".");

                byte[] afterFailedSave = Bytes(simulation);
                simulation = new Simulation(policy, codec.Decode(afterFailedSave), ExecutionProfile.Laboratory);
                replay = new Simulation(policy, codec.Decode(afterFailedSave), ExecutionProfile.Laboratory);
                AdvanceUntilSaves(simulation, 4); AdvanceUntilSaves(replay, 4);
                var fourth = simulation.Capture().LifeEvents.Where(x => x.ActorId == TestOnlyPolicy.ActorId
                    && x.Kind == LifeEventKind.DeathSave).OrderBy(x => x.Revision).ElementAt(3);
                Require(Bytes(simulation).SequenceEqual(Bytes(replay)) && fourth.Natural == 11
                    && fourth.RecoveryD4 >= 1 && simulation.Capture().Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).Stable,
                    "Natural 11 did not use the corrected stream, succeed under -1, and draw its required recovery d4.");
            });

            cases.Add("daily_provisioning_full_food_and_water_uses_real_shared_lots", () => {
                var policy = ProvisioningPolicy();
                var simulation = World(policy);
                foreach (var step in new[] { new[] { 1, 0 }, new[] { 1, 0 }, new[] { 1, 0 }, new[] { 0, 1 }, new[] { 0, 1 } }) {
                    WorldStep(simulation, step[0], step[1]);
                    WorldAdvance(simulation, 1);
                }

                string meal = ProvisioningHandle(simulation, TestOnlyInventoryPolicy.FoodId, new RuleQuantity(2),
                    HandlingKind.Handover, destination: TestOnlyPolicy.CompanionId);
                var transferred = simulation.Capture().InventoryLots.Single(x => x.LotId == meal);
                var custody = simulation.Capture().Work.Lots.Single(x => x.Id == meal);
                Require(transferred.OwnerId == TestOnlyPolicy.ActorId && custody.CustodianId == TestOnlyPolicy.CompanionId,
                    "Provisioning handover failed to preserve the food lot's ownership and update custody.");
                WorldCommit(simulation, IC(simulation, CommandKind.StartIntake, meal,
                    new InventoryRequest(new RuleQuantity(2)), TestOnlyPolicy.CompanionId));
                WorldAdvance(simulation, 1800);
                for (int portion = 0; portion < 2; portion++) {
                    WorldCommit(simulation, IC(simulation, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId,
                        new InventoryRequest(new RuleQuantity(4), TestOnlyFillingPolicy.CompanionSkinId),
                        TestOnlyPolicy.CompanionId));
                    WorldAdvance(simulation, 60);
                    var fill = simulation.Capture().WaterFills.OrderBy(x => x.StartedAt).Last();
                    Require(fill.WorkerId == TestOnlyPolicy.CompanionId && fill.Status == WaterFillStatus.Complete
                        && fill.OutputLotId != "",
                        "The shared filling authority did not complete one four-pint transfer.");
                    WorldCommit(simulation, IC(simulation, CommandKind.StartIntake, fill.OutputLotId,
                        new InventoryRequest(new RuleQuantity(4)), TestOnlyPolicy.CompanionId));
                    WorldAdvance(simulation, 240);
                }

                byte[] beforeBoundary = Bytes(simulation);
                var restored = RestoreProvisioning(simulation, policy);
                Require(beforeBoundary.SequenceEqual(Bytes(restored)),
                    "Full food/water intake and physical fill changed through save/restore.");
                var close = IC(simulation, CommandKind.AdvanceClock, x: 83994, y: 1);
                WorldCommit(simulation, close);
                WorldCommit(restored, close);
                var view = simulation.Capture();
                var hero = view.DailyProvisioningSettlements.Single(x => x.DayOrdinal == 0
                    && x.ActorId == TestOnlyPolicy.ActorId);
                var companion = view.DailyProvisioningSettlements.Single(x => x.DayOrdinal == 0
                    && x.ActorId == TestOnlyPolicy.CompanionId);
                var companionEvidence = view.DailyProvisioningConsumption.Where(x => x.SettlementId == companion.Id).ToArray();
                Require(view.RuleClock == T(86400) && companion.FoodConsumed == new RuleQuantity(2)
                    && companion.WaterConsumed == new RuleQuantity(8) && !companion.FoodShortfall && !companion.WaterShortfall
                    && companion.StrainGainId == "" && hero.FoodConsumed == default(RuleQuantity)
                    && hero.WaterConsumed == default(RuleQuantity) && hero.StrainGainId != ""
                    && companionEvidence.Length == 3
                    && RuleQuantity.Sum(companionEvidence.Where(x => x.Nutrition == NutritionKind.FoodPounds)
                        .Select(x => x.Amount)) == new RuleQuantity(2)
                    && RuleQuantity.Sum(companionEvidence.Where(x => x.Nutrition == NutritionKind.WaterPints)
                        .Select(x => x.Amount)) == new RuleQuantity(8)
                    && companionEvidence.All(x => view.Intakes.Any(i => i.Id == x.IntakeId && i.ActorId == x.ActorId
                        && i.LotId == x.LotId && i.ReservationId == x.ReservationId)
                        && view.Work.Reservations.Any(r => r.Id == x.ReservationId && r.LotId == x.LotId
                            && r.ConsumedAmount >= x.Amount)),
                    "Daily provisioning did not distinguish complete, lot-backed intake from the companion's actual deficit.");
                Require(Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Restored branch did not deterministically close the same provisioned day.");
            });

            cases.Add("daily_provisioning_single_advance_settles_every_crossed_day", () => {
                var policy = ProvisioningPolicy();
                var simulation = World(policy);
                WorldAdvance(simulation, 3 * 86400);
                var view = simulation.Capture();
                Require(view.RuleClock == T(3 * 86400) && view.DailyProvisioningSettlements.Length == 6
                    && view.DailyProvisioningSettlements.Select(x => x.DayOrdinal).Distinct().OrderBy(x => x)
                        .SequenceEqual(new long[] { 0, 1, 2 })
                    && view.ExpeditionStrainGains.Length == 6
                    && ExpeditionStrainRules.Current(view, TestOnlyPolicy.ActorId).Level == 3
                    && ExpeditionStrainRules.Current(view, TestOnlyPolicy.CompanionId).Level == 3,
                    "One clock advance did not settle each crossed day exactly once for the fixed roster.");
                var bytes = Bytes(simulation);
                var restored = RestoreProvisioning(simulation, policy);
                Require(bytes.SequenceEqual(Bytes(restored)), "Multi-day settlement did not roundtrip exactly.");
                var continuation = IC(simulation, CommandKind.AdvanceClock, x: 1, y: 1);
                WorldCommit(simulation, continuation);
                WorldCommit(restored, continuation);
                Require(Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Post-restore continuation diverged after a multi-day settlement.");
            });

            cases.Add("daily_provisioning_map_route_and_reconnaissance_checks_use_strain", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var mapPolicy = RouteTravelPolicy(routes).EnableRouteMappingWork(RouteMappingWorkProfile(routes))
                    .EnableDailyProvisioning();
                var map = World(mapPolicy);
                RouteTravelReachSource(map);
                WorldAdvance(map, 172791, 2);
                Require(ExpeditionStrainRules.Current(map.Capture(), TestOnlyPolicy.ActorId).Level == 1,
                    "Map Route did not begin after the first canonical provisioning boundary.");
                WorldCommit(map, RouteMappingWorkCommand(map, CommandKind.StartRouteMappingWork,
                    RouteTravelId, "provisioning.map-route.start"));
                WorldAdvance(map, 28800);
                var mapView = map.Capture();
                var mapCheck = mapView.RouteMappingWorkAttempts.Single().Check;
                var mapFacts = CharacterStateFacts.ForActor(mapView, TestOnlyPolicy.ActorId,
                    TestOnlyExpeditionRouteMappingWorkFixture.SkillId);
                int expectedMap = checked(mapFacts.DeriveCheck(CharacterAbility.Wisdom).TotalWithInjury(mapFacts) - 1);
                Require(mapCheck != null && mapCheck.LeadModifier == expectedMap
                    && mapCheck.At == mapView.RuleClock,
                    "Registered Map Route completion did not include the current Strain modifier in its causal check.");

                var reconPolicy = RouteReconnaissancePolicy(routes, SeedForD20(20), 1, null,
                    new TestOnlyRouteReconnaissanceSkillFact(TestOnlyPolicy.ActorId, 1)).EnableDailyProvisioning();
                var recon = World(reconPolicy);
                RouteTravelReachSource(recon);
                WorldAdvance(recon, 172791, 2);
                WorldCommit(recon, RouteReconnaissanceCommand(recon, CommandKind.StartRouteReconnaissance,
                    RouteTravelId, "provisioning.route-recon.start"));
                WorldAdvance(recon, 28800);
                var reconView = recon.Capture();
                var reconCheck = reconView.RouteReconnaissanceAttempts.Single().Check;
                var reconFacts = CharacterStateFacts.ForActor(reconView, TestOnlyPolicy.ActorId,
                    TestOnlyExpeditionRouteReconnaissanceFixture.SkillId);
                int expectedRecon = checked(reconFacts.DeriveCheck(CharacterAbility.Wisdom).TotalWithInjury(reconFacts) - 1);
                Require(reconCheck != null && reconCheck.LeadModifier == expectedRecon
                    && reconCheck.At == reconView.RuleClock,
                    "Registered route reconnaissance completion did not include current Strain in its causal check.");
            });

            cases.Add("daily_provisioning_level_two_reaches_shared_tactical_attack", () => {
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableDailyProvisioning();
                var simulation = World(policy);
                WorldStep(simulation, 1, 0); WorldAdvance(simulation, 1);
                WorldStep(simulation, 1, 0); WorldAdvance(simulation, 1);
                WorldAdvance(simulation, 2 * 86400 - 2);
                Require(ExpeditionStrainRules.Current(simulation.Capture(), TestOnlyPolicy.ActorId).Level == 2,
                    "Combat fixture did not reach the source-selected second Strain level.");
                WorldStep(simulation, 1, 0);
                Require(simulation.Capture().InventoryCombat,
                    "The authored shared-world encounter did not begin after exploration movement.");
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                    stance: (int)CombatStance.Aggressive));
                TacStep(simulation, 3, 0);
                WorldCommit(simulation, Tac(simulation, CommandKind.AttackClub, AdditionalTacticalActor.Id,
                    weapon: TestOnlyClubAttackPolicy.ActorClub));
                var attack = simulation.Capture().MeleeAttacks.Single(x => x.AttackerId == TestOnlyPolicy.ActorId);
                Require(attack.Attack.Modifier == -1,
                    "The shared tactical attack resolver did not apply level-two Expedition Strain.");
            });

            cases.Add("daily_provisioning_multiday_catchup_projects_strain_and_death", () => {
                var policy = ProvisioningPolicy();
                var simulation = World(policy);
                uint random = simulation.Capture().RandomState;
                var order = simulation.Capture().WorldSchedule.Order.ToArray();
                for (int day = 1; day <= 6; day++) {
                    WorldAdvance(simulation, 86400);
                    var view = simulation.Capture();
                    Require(view.DailyProvisioningSettlements.Count(x => x.DayOrdinal == day - 1) == 2
                        && view.ExpeditionStrainGains.Count(x => x.At == T(day * 86400)) == 2,
                        "A crossed endpoint was skipped, duplicated, or produced more than one daily point.");
                    var hero = ExpeditionStrainRules.Current(view, TestOnlyPolicy.ActorId);
                    var companion = ExpeditionStrainRules.Current(view, TestOnlyPolicy.CompanionId);
                    Require(hero.Level == day && companion.Level == day,
                        "Fixed-roster Strain did not accumulate one point per short day.");
                    Require(view.RandomState == random && view.WorldSchedule.Order.SequenceEqual(order),
                        "Daily settlement consumed RNG or rewrote authored initiative order.");
                    if (day == 1)
                        Require(hero.InitiativeModifier == -1 && hero.ExpeditionCheckModifier == -1,
                            "Level 1 modifiers were not projected.");
                    if (day == 2)
                        Require(hero.AttackModifier == -1 && hero.SavingThrowModifier == -1 && hero.FlatSpeedModifier == -10,
                            "Level 2 combat and travel penalties were not projected.");
                    if (day == 3)
                        Require(hero.ExpeditionCheckDisadvantage && hero.InitiativeModifier == -1,
                            "Level 3 registered-check disadvantage was not projected.");
                    if (day == 4)
                        Require(hero.EffectiveMaximumHp(view.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).MaximumHp)
                            == PlaytestMaximumHp.SystemicMaximum(view.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).MaximumHp, expedition: 4),
                            "Level 4 effective maximum HP projection differs from the shared HP authority.");
                    if (day == 5)
                        Require(hero.Incapacitated && !hero.TacticalVoluntaryMovementAllowed && hero.SlowTravel
                            && hero.DashProhibited && view.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).Hp
                                <= hero.EffectiveMaximumHp(view.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).MaximumHp),
                            "Level 5 incapacitation, movement or effective HP was not applied.");
                    if (day == 6)
                        Require(view.Lives.Where(x => x.ActorId == TestOnlyPolicy.ActorId || x.ActorId == TestOnlyPolicy.CompanionId)
                            .All(x => x.Dead && x.Hp == 0)
                            && view.ExpeditionStrainGains.Where(x => x.At == T(6 * 86400))
                                .All(x => x.Endpoint == ExpeditionStrainEndpoint.OrdinaryDeath),
                            "Level 6 did not apply the explicitly selected ordinary death endpoint.");
                }
                var restored = RestoreProvisioning(simulation);
                Require(Bytes(simulation).SequenceEqual(Bytes(restored)), "Multi-day Strain history failed byte-exact restore.");
                var repeatedAdvance = IC(simulation, CommandKind.AdvanceClock, x: 1, y: 1);
                WorldCommit(simulation, repeatedAdvance);
                var deterministic = RestoreProvisioning(restored);
                WorldCommit(deterministic, repeatedAdvance);
                Require(Bytes(simulation).SequenceEqual(Bytes(deterministic)),
                    "Post-restore command replay diverged after multi-day settlement.");
            });

            cases.Add("rest_debt_connects_companion_work_safe_rest_deadline_and_replay", () => {
                const string cropId = "TEST_ONLY.rest-debt-assigned-crop";
                var policy = RestDebtPolicy();
                var simulation = World(policy);
                Require(simulation.Capture().SchemaVersion == Snapshot.RestDebtSchema
                    && simulation.Capture().TestOnly,
                    "Rest Debt did not select its isolated schema63 TEST_ONLY profile.");
                var restOptions = simulation.DiscoverCommands(host, TestOnlyPolicy.ActorId);
                var beginRestOption = restOptions.SingleOrDefault(x => x.Command.Kind == CommandKind.BeginRest);
                var scheduleOption = restOptions.FirstOrDefault(x => x.Command.Kind == CommandKind.ScheduleRestWatch);
                Require(beginRestOption != null && beginRestOption.Query.Supported && beginRestOption.Query.Admissible
                    && beginRestOption.Query.Costs.Single().Kind == "rest-seconds"
                    && scheduleOption != null && scheduleOption.Query.Supported && scheduleOption.Query.Admissible,
                    "The active safe-rest and prospective Rest Watch controls were not discoverable through the shared command query.");
                var encounterPolicy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: 39))
                    .EnableDailyProvisioning().EnableRestDebt();
                var restingCombat = World(encounterPolicy);
                WorldCommit(restingCombat, IC(restingCombat, CommandKind.BeginRest, "TEST_ONLY.safe-berth"));
                byte[] beforeUnsupportedEmergency = Bytes(restingCombat);
                var emergency = restingCombat.Execute(host, IC(restingCombat, CommandKind.BeginFixedEncounter,
                    actor: AdditionalTacticalActor.Id));
                Require(emergency.Outcome == Outcome.Rejected && emergency.Code == "RestInterruptionAuthorityUnsupported"
                    && beforeUnsupportedEmergency.SequenceEqual(Bytes(restingCombat)),
                    "A tactical interruption without an authoritative emergency event changed an active Rest (outcome="
                    + emergency.Outcome + ", code=" + emergency.Code + ", rest="
                    + restingCombat.Capture().RestIntervals.Single().Status + ").");
                ScheduleRest(simulation, 1, RestWatchSlot.Afternoon);
                AdvanceRestDebt(simulation, 16 * 3600);
                StartAssignedPlanting(simulation, cropId);
                var plant = simulation.Capture().Crops.Single(x => x.Id == cropId).Tasks.Single();
                Require(plant.Status == CropWorkStatus.Working && plant.StartedAt == T(16 * 3600),
                    "Companion crop work did not start on the shared Rest Watch clock.");

                AdvanceRestDebt(simulation, 8 * 3600);
                var atMiss = simulation.Capture();
                var missedEvening = atMiss.RestWatchOutcomes.Single(x => x.ActorId == TestOnlyPolicy.ActorId && x.DayOrdinal == 0);
                var opened = atMiss.RestDebtEvents.Single(x => x.ActorId == TestOnlyPolicy.ActorId);
                var companionPlant = atMiss.Crops.Single(x => x.Id == cropId).Tasks.Single();
                var workInterval = atMiss.Work.WorkerIntervals.Single(x => x.JobId == companionPlant.Id);
                Require(atMiss.RuleClock == T(24 * 3600) && missedEvening.Slot == RestWatchSlot.Evening
                    && missedEvening.Outcome == RestWatchOutcomeKind.Missed && opened.Kind == RestDebtEventKind.Opened
                    && opened.At == T(24 * 3600) && opened.DeadlineAfter == T(40 * 3600)
                    && companionPlant.Status == CropWorkStatus.Complete
                    && workInterval.Start == T(16 * 3600) && workInterval.End == T(17 * 3600),
                    "Evening Rest miss, 40-hour deadline, or real companion work interval did not settle together.");

                string beforeDeadlinePath = Path.Combine(directory, "rest-debt-before-deadline.ddsave");
                new FileSaveStore().Save(beforeDeadlinePath, atMiss);
                simulation = new Simulation(policy, new FileSaveStore().Load(beforeDeadlinePath), ExecutionProfile.Laboratory);
                byte[] preDeadline = Bytes(simulation);
                var restored = RestoreRestDebt(simulation, policy);
                Require(preDeadline.SequenceEqual(Bytes(restored)), "Schema63 Rest Debt state changed through save/restore.");

                var clearBranch = RestoreRestDebt(simulation, policy);
                int strainBeforeClear = ExpeditionStrainRules.Current(clearBranch.Capture(), TestOnlyPolicy.ActorId).Level;
                WorldCommit(clearBranch, IC(clearBranch, CommandKind.BeginRest, "TEST_ONLY.safe-berth"));
                string activeRestPath = Path.Combine(directory, "rest-debt-active-safe-rest.ddsave");
                new FileSaveStore().Save(activeRestPath, clearBranch.Capture());
                clearBranch = new Simulation(policy, new FileSaveStore().Load(activeRestPath), ExecutionProfile.Laboratory);
                AdvanceRestDebt(clearBranch, 8 * 3600);
                var cleared = clearBranch.Capture();
                Require(cleared.RestIntervals.Single(x => x.ActorId == TestOnlyPolicy.ActorId).Status == RestIntervalStatus.Completed
                    && cleared.RestDebtEvents.Last(x => x.ActorId == TestOnlyPolicy.ActorId).Kind == RestDebtEventKind.Cleared
                    && cleared.RestDebtEvents.Last(x => x.ActorId == TestOnlyPolicy.ActorId).At == T(32 * 3600)
                    && ExpeditionStrainRules.Current(cleared, TestOnlyPolicy.ActorId).Level == strainBeforeClear,
                    "A qualifying safe Rest did not clear debt at hour32 without removing Strain.");

                var unsafeProfile = new TestOnlyRestDebtProfile(sites: new[] {
                    new TestOnlyRestSiteFact("TEST_ONLY.safe-berth", 0, 0, true, true),
                    new TestOnlyRestSiteFact("TEST_ONLY.exposed-berth", 1, 0, false, true)
                });
                var unsafePolicy = RestDebtPolicy(unsafeProfile);
                var unsafeSimulation = World(unsafePolicy);
                AdvanceRestDebt(unsafeSimulation, 24 * 3600);
                WorldCommit(unsafeSimulation, IC(unsafeSimulation, CommandKind.BeginRest, "TEST_ONLY.safe-berth"));
                AdvanceRestDebt(unsafeSimulation, 8 * 3600);
                var forgedUnsafeClear = unsafeSimulation.Capture().Copy();
                forgedUnsafeClear.RestIntervals = forgedUnsafeClear.RestIntervals.Select(x => x.ActorId == TestOnlyPolicy.ActorId
                    ? new RestIntervalRecord(x.Id, x.ActorId, "TEST_ONLY.exposed-berth", x.StartedAt, x.ScheduledEnd,
                        x.EndedAt, x.Status, x.Revision) : x).ToArray();
                Throws<ArgumentException>(() => new Simulation(unsafePolicy, forgedUnsafeClear, ExecutionProfile.Laboratory));

                // Whole versus split clock advancement, with a restore before the hour40 boundary.
                var whole = RestoreRestDebt(simulation, policy);
                AdvanceRestDebt(whole, 16 * 3600);
                var split = RestoreRestDebt(simulation, policy);
                AdvanceRestDebt(split, 8 * 3600);
                string beforeDuePath = Path.Combine(directory, "rest-debt-before-hour40.ddsave");
                new FileSaveStore().Save(beforeDuePath, split.Capture());
                split = new Simulation(policy, new FileSaveStore().Load(beforeDuePath), ExecutionProfile.Laboratory);
                AdvanceRestDebt(split, 8 * 3600);
                var wholeState = whole.Capture(); var splitState = split.Capture();
                var dueAndMiss = wholeState.RestDebtEvents.Where(x => x.ActorId == TestOnlyPolicy.ActorId
                    && x.At == T(40 * 3600)).OrderBy(x => x.EventSequence).ToArray();
                var linkedGains = wholeState.ExpeditionStrainGains.Where(x => dueAndMiss.Any(e => e.StrainGainId == x.Id))
                    .OrderBy(x => x.GainSequence).ToArray();
                Require(wholeState.RuleClock == T(40 * 3600) && splitState.RuleClock == wholeState.RuleClock
                    && dueAndMiss.Select(x => x.Kind).SequenceEqual(new[] { RestDebtEventKind.UnpaidDeadline, RestDebtEventKind.MissedWhileIndebted })
                    && dueAndMiss[1].DeadlineAfter == T(56 * 3600)
                    && linkedGains.Length == 2 && linkedGains[0].CauseKind == ExpeditionStrainCauseKind.RestDebtDeadline
                    && linkedGains[1].CauseKind == ExpeditionStrainCauseKind.RestMissedWhileIndebted
                    && linkedGains[0].LevelBefore + linkedGains[0].AddedAmount == linkedGains[1].LevelBefore
                    && StrainSemantics(wholeState).SequenceEqual(StrainSemantics(splitState))
                    && DebtSemantics(wholeState).SequenceEqual(DebtSemantics(splitState)),
                    "Hour40 deadline and same-time missed Rest did not produce two ordered gains/reset or partition equivalence.");
                var duplicateDue = wholeState.Copy();
                var originalDue = dueAndMiss.Single(x => x.Kind == RestDebtEventKind.UnpaidDeadline);
                int nextEventSequence = duplicateDue.RestDebtEvents.Where(x => x.ActorId == originalDue.ActorId
                    && x.Revision == originalDue.Revision).Max(x => x.EventSequence) + 1;
                duplicateDue.RestDebtEvents = duplicateDue.RestDebtEvents.Concat(new[] { new RestDebtEventRecord(
                    "rest.debt.duplicate-due", originalDue.ActorId, originalDue.Kind, originalDue.At,
                    originalDue.Revision, nextEventSequence, originalDue.EpisodeId, originalDue.EvidenceId,
                    originalDue.DeadlineBefore, originalDue.DeadlineAfter, originalDue.StrainGainId) }).ToArray();
                Throws<ArgumentException>(() => Validation.Snapshot(duplicateDue));
                var wrongActor = wholeState.Copy();
                wrongActor.RestDebtEvents = wrongActor.RestDebtEvents.Select(x => x.Id != originalDue.Id ? x
                    : new RestDebtEventRecord(x.Id, TestOnlyPolicy.CompanionId, x.Kind, x.At, x.Revision,
                        x.EventSequence, x.EpisodeId, x.EvidenceId, x.DeadlineBefore, x.DeadlineAfter,
                        x.StrainGainId)).ToArray();
                Throws<ArgumentException>(() => Validation.Snapshot(wrongActor));
                AdvanceRestDebt(whole, 1);
                Require(whole.Capture().RestDebtEvents.Count(x => x.ActorId == TestOnlyPolicy.ActorId
                    && x.Kind == RestDebtEventKind.UnpaidDeadline) == 1,
                    "Rest Debt produced a repeated deadline gain merely because time continued.");

                var replayA = RestoreRestDebt(simulation, policy);
                var replayB = RestoreRestDebt(simulation, policy);
                var replayCommand = IC(replayA, CommandKind.AdvanceClock, x: 16 * 3600, y: 1,
                    id: "rest.replay." + replayA.Capture().Revision.ToString(System.Globalization.CultureInfo.InvariantCulture));
                WorldCommit(replayA, replayCommand); WorldCommit(replayB, replayCommand);
                byte[] replayed = Bytes(replayA);
                Require(replayed.SequenceEqual(Bytes(replayB))
                    && replayA.Execute(TestOnlySharedWorldPolicy.Host(), replayCommand).Outcome == Outcome.Duplicate
                    && replayed.SequenceEqual(Bytes(replayA)),
                    "Rest Debt due/missed events diverged on deterministic save/restore replay or duplicate submission.");
            });

            cases.Add("rest_debt_and_daily_provisioning_share_same_time_strain_order", () => {
                const string cropId = "TEST_ONLY.rest-debt-morning-crop";
                var policy = RestDebtPolicy(); var simulation = World(policy);
                ScheduleRest(simulation, 0, RestWatchSlot.Morning);
                StartAssignedPlanting(simulation, cropId);
                AdvanceRestDebt(simulation, 8 * 3600);
                var opened = simulation.Capture().RestDebtEvents.Single(x => x.ActorId == TestOnlyPolicy.ActorId);
                Require(opened.At == T(8 * 3600) && opened.DeadlineAfter == T(24 * 3600),
                    "Morning miss did not open the second-following-Watch deadline at hour24.");
                AdvanceRestDebt(simulation, 16 * 3600);
                var state = simulation.Capture();
                var sameTime = state.ExpeditionStrainGains.Where(x => x.ActorId == TestOnlyPolicy.ActorId
                    && x.At == T(24 * 3600)).OrderBy(x => x.GainSequence).ToArray();
                Require(sameTime.Length == 2 && sameTime[0].CauseKind == ExpeditionStrainCauseKind.DailyProvisioning
                    && sameTime[1].CauseKind == ExpeditionStrainCauseKind.RestDebtDeadline
                    && sameTime[0].GainSequence == 0 && sameTime[1].GainSequence == 1
                    && sameTime[0].LevelBefore == 0 && sameTime[1].LevelBefore == sameTime[0].LevelAfter
                    && sameTime[1].OrdinaryRemovable == null && sameTime[1].RemovalGateMet == null
                    && ExpeditionStrainRules.Current(state, TestOnlyPolicy.ActorId).Level == 2,
                    "Shared timestamp/command Strain gains did not preserve their ordered cumulative source history.");

                var forged = state.Copy();
                var target = forged.ExpeditionStrainGains.Single(x => x.CauseKind == ExpeditionStrainCauseKind.RestDebtDeadline);
                var forgedKind = state.Copy();
                forgedKind.ExpeditionStrainGains = forgedKind.ExpeditionStrainGains.Select(x => x.Id != target.Id ? x
                    : new ExpeditionStrainGainRecord(x.Id, x.PointId, ExpeditionStrainCauseKind.RestMissedWhileIndebted,
                        x.CauseId, x.GainSequence, x.ActorId, x.SourceId, x.TrackId, x.At, x.Revision,
                        x.LevelBefore, x.AttemptedAmount, x.AddedAmount, x.OrdinaryRemovable,
                        x.RemovalGateMet, x.Endpoint)).ToArray();
                Throws<ArgumentException>(() => Validation.Snapshot(forgedKind));
                forged.ExpeditionStrainGains = forged.ExpeditionStrainGains.Select(x => x.Id != target.Id ? x
                    : new ExpeditionStrainGainRecord(x.Id, x.PointId, x.CauseKind, "rest.debt.forged", x.GainSequence,
                        x.ActorId, x.SourceId, x.TrackId, x.At, x.Revision, x.LevelBefore, x.AttemptedAmount,
                        x.AddedAmount, x.OrdinaryRemovable, x.RemovalGateMet, x.Endpoint)).ToArray();
                Throws<ArgumentException>(() => Validation.Snapshot(forged));
            });
        }
    }
}
#endif
