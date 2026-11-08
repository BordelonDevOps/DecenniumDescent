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

        private static void AddDailyProvisioningCases(Dictionary<string, Action> cases, string directory)
        {
            var codec = new SnapshotCodec();
            var host = TestOnlySharedWorldPolicy.Host();

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
        }
    }
}
#endif
