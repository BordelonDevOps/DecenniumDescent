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
        private static TestOnlySharedWorldPolicy HavenCarePolicy(SharedCombatFixture combat = null,
            ConditionCombatFixture conditions = null, int siteX = 3, int siteY = 2, string[] patients = null)
        {
            var actors = patients ?? new[] { TestOnlyPolicy.ActorId };
            var restSite = new TestOnlyRestSiteFact("TEST_ONLY.safe-berth", 3, 2, true, true);
            var moraleSite = new TestOnlyMoraleRestSiteFact("TEST_ONLY.haven-recreation",
                "TEST_ONLY.campfire-recreation", 3, 2, true, true);
            return new TestOnlySharedWorldPolicy(combat, conditions: conditions).EnableCampGreensAssignments()
                .EnableDailyProvisioning(new TestOnlyDailyProvisioningProfile(actors))
                .EnableRestDebt(new TestOnlyRestDebtProfile(actors, new[] { restSite }))
                .EnableExpeditionStrainRecovery()
                .EnableMoraleRest(new TestOnlyMoraleRestProfile(actors, new[] { moraleSite }))
                .EnableHavenCare(new TestOnlyHavenCareProfile(actors, siteX: siteX, siteY: siteY));
        }

        private static void HavenCareIntake(Simulation s, string lotId, RuleQuantity amount,
            int activeSeconds, string id)
        {
            WorldCommit(s, new Command(id + ".start", TestOnlyPolicy.ActorId, s.Capture().Revision,
                CommandKind.StartIntake, lotId, inventory: new InventoryRequest(amount)));
            WorldAdvance(s, activeSeconds);
            var intake = s.Capture().Intakes.Single(x => x.LotId == lotId && x.ActorId == TestOnlyPolicy.ActorId
                && x.Status == IntakeStatus.Complete);
            var reservation = s.Capture().Work.Reservations.Single(x => x.Id == intake.ReservationId);
            Require(reservation.ConsumedAmount == amount, "Ordinary intake did not consume the full requested amount.");
        }

        private static void HavenCareFillAndDrink(Simulation s, int sequence)
        {
            const string worker = TestOnlyPolicy.CompanionId;
            const string patient = TestOnlyPolicy.ActorId;
            const string vessel = TestOnlyFillingPolicy.CompanionSkinId;
            WorldCommit(s, IC(s, CommandKind.StartWaterFill, TestOnlyFillingPolicy.SupplyId,
                new InventoryRequest(new RuleQuantity(4), vessel), worker));
            WorldAdvance(s, 60);
            var fill = s.Capture().WaterFills.Single(x => x.WorkerId == worker
                && x.DestinationId == vessel && x.Status == WaterFillStatus.Complete
                && x.EndedAt == s.Capture().RuleClock);
            WorldCommit(s, IC(s, CommandKind.HandleVessel, vessel,
                new InventoryRequest(new RuleQuantity(1), patient, HandlingKind.Handover), worker));
            HavenCareIntake(s, fill.OutputLotId, new RuleQuantity(4), 4 * 60,
                "haven.fill." + sequence.ToString() + ".drink");
            WorldCommit(s, IC(s, CommandKind.HandleVessel, vessel,
                new InventoryRequest(new RuleQuantity(1), worker, HandlingKind.Handover), patient));
        }

        private static void AddHavenCareCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("haven_care_benign_condition_event_preserves_active_interval", () =>
            {
                var benignClear = new ConditionFixtureEvent(TestOnlyPolicy.ActorId,
                    ConditionOperation.Cure("event.haven-care.noop", new ConditionStamp(T(0)), "Blinded"));
                var policy = HavenCarePolicy(conditions: new ConditionCombatFixture(benignClear), siteX: 0, siteY: 0);
                var simulation = World(policy);
                WorldCommit(simulation, IC(simulation, CommandKind.BeginHavenCare, "TEST_ONLY.haven-care-service"));
                var active = simulation.Capture().ExpeditionHavenCareIntervals.Single();
                WorldCommit(simulation, CCCommand(simulation, "haven-care.noop"));
                Require(simulation.Capture().ExpeditionHavenCareIntervals.Single(x => x.Id == active.Id).Status
                        == HavenCareIntervalStatus.Active,
                    "A benign condition clear canceled an otherwise eligible Haven-care interval.");

                byte[] activeBytes = Bytes(simulation);
                var store = new FileSaveStore();
                string path = Path.Combine(directory, "haven-care-benign-condition.ddsave");
                store.Save(path, simulation.Capture());
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                Require(activeBytes.SequenceEqual(Bytes(restored)),
                    "A benign condition event or active care interval changed through save/restore.");
                WorldAdvance(simulation, 24 * 60 * 60);
                WorldAdvance(restored, 24 * 60 * 60);
                Require(Bytes(simulation).SequenceEqual(Bytes(restored))
                    && simulation.Capture().ExpeditionHavenCareIntervals.Single(x => x.Id == active.Id).Status
                        == HavenCareIntervalStatus.Completed,
                    "The benign condition clear did not preserve deterministic care completion after restore.");
            });

            cases.Add("haven_care_rejects_external_combat_transition_without_mutation", () =>
            {
                var policy = HavenCarePolicy(new SharedCombatFixture(), siteX: 0, siteY: 0);
                var simulation = World(policy);
                WorldCommit(simulation, IC(simulation, CommandKind.BeginHavenCare, "TEST_ONLY.haven-care-service"));
                var before = simulation.Capture();
                Require(before.WorldSchedule.Order.Contains(AdditionalTacticalActor.Id),
                    "Combat-transition test actor is not part of the authored schedule.");
                byte[] beforeBytes = Bytes(simulation);
                var result = simulation.Execute(host, IC(simulation, CommandKind.BeginFixedEncounter,
                    actor: AdditionalTacticalActor.Id));
                var after = simulation.Capture();
                Require(result.Outcome == Outcome.Rejected && result.Code == "HavenCareCombatTransitionUnsupported"
                    && after.RuleClock == before.RuleClock && after.Receipts.Length == before.Receipts.Length
                    && after.ExpeditionHavenCareIntervals.Single().Status == HavenCareIntervalStatus.Active
                    && beforeBytes.SequenceEqual(Bytes(simulation)),
                    "An external combat transition changed or interrupted an active Haven-care interval.");
                var inventoryCombat = simulation.Execute(host, IC(simulation, CommandKind.EnterInventoryCombat,
                    actor: AdditionalTacticalActor.Id));
                Require(inventoryCombat.Outcome == Outcome.Rejected
                    && inventoryCombat.Code == "HavenCareCombatTransitionUnsupported"
                    && beforeBytes.SequenceEqual(Bytes(simulation)),
                    "Inventory-combat entry changed or interrupted an active Haven-care interval.");

                var movementPolicy = HavenCarePolicy(new SharedCombatFixture(), siteX: 3, siteY: 3,
                    patients: new[] { TestOnlyPolicy.CompanionId });
                var movement = World(movementPolicy);
                WorldCommit(movement, IC(movement, CommandKind.BeginHavenCare,
                    "TEST_ONLY.haven-care-service", actor: TestOnlyPolicy.CompanionId));
                WorldStep(movement, 1, 0, actor: TestOnlyPolicy.ActorId);
                WorldAdvance(movement, 1);
                WorldStep(movement, 1, 0, actor: TestOnlyPolicy.ActorId);
                WorldAdvance(movement, 1);
                var beforeApproach = movement.Capture();
                byte[] beforeApproachBytes = Bytes(movement);
                var approach = movement.Execute(host, IC(movement, CommandKind.BeginWorldStep, "walk",
                    actor: TestOnlyPolicy.ActorId, x: 1, y: 0));
                Require(approach.Outcome == Outcome.Rejected
                    && approach.Code == "HavenCareCombatTransitionUnsupported"
                    && movement.Capture().RuleClock == beforeApproach.RuleClock
                    && movement.Capture().ExpeditionHavenCareIntervals.Single().Status == HavenCareIntervalStatus.Active
                    && beforeApproachBytes.SequenceEqual(Bytes(movement)),
                    "Movement-triggered combat changed or interrupted another actor's active Haven care.");
            });

            cases.Add("haven_care_batches_supported_strain_after_real_provisioning_and_replays", () =>
            {
                string milestone = "initialization";
                try
                {
                var policy = HavenCarePolicy();
                var simulation = World(policy);
                Require(simulation.Capture().SchemaVersion == Snapshot.HavenCareSchema
                    && simulation.Capture().TestOnly
                    && simulation.Capture().ExpeditionHavenCareIntervals.Length == 0,
                    "Haven care did not select isolated schema66 TEST_ONLY state.");

                // Reach the exact authored service site adjacent to the ordinary water pool.
                foreach (var step in new[] { new[] { 1, 0 }, new[] { 1, 0 }, new[] { 1, 0 },
                    new[] { 0, 1 }, new[] { 0, 1 } })
                {
                    WorldStep(simulation, step[0], step[1]);
                    WorldAdvance(simulation, 1);
                }
                Require(simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 3
                    && simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2,
                    "The patient did not reach the co-located Haven, recreation and safe-berth sites.");

                // Day zero has one provisioning shortfall but completes its authored evening Rest.
                // Day one remains unsupported and misses its evening Watch, opening Rest Debt.
                milestone = "two-day Strain setup";
                WorldCommit(simulation, IC(simulation, CommandKind.ScheduleRestWatch, "day.0",
                    x: (int)RestWatchSlot.Evening));
                WorldAdvance(simulation, 16 * 60 * 60 - 5);
                WorldCommit(simulation, IC(simulation, CommandKind.BeginRest, "TEST_ONLY.safe-berth"));
                WorldAdvance(simulation, 8 * 60 * 60);
                var firstDay = simulation.Capture();
                Require(firstDay.RuleClock == T(24 * 60 * 60)
                    && firstDay.DailyProvisioningSettlements.Single(x => x.ActorId == TestOnlyPolicy.ActorId
                        && x.DayOrdinal == 0).HasShortfall
                    && firstDay.RestWatchOutcomes.Single(x => x.ActorId == TestOnlyPolicy.ActorId
                        && x.DayOrdinal == 0).Outcome == RestWatchOutcomeKind.Rested
                    && firstDay.RestDebtEvents.Length == 0,
                    "The completed Rest Watch did not prevent unrelated Rest Debt while preserving its provisioning shortfall.");
                WorldAdvance(simulation, 24 * 60 * 60);
                var preCare = simulation.Capture();
                string[] priorPointIds = preCare.ExpeditionStrainGains.Where(x => x.ActorId == TestOnlyPolicy.ActorId
                    && x.CauseKind == ExpeditionStrainCauseKind.DailyProvisioning && x.AddedAmount == 1)
                    .Select(x => x.PointId).OrderBy(x => x, StringComparer.Ordinal).ToArray();
                Require(priorPointIds.Length == 2 && preCare.RestDebtEvents.Any(x => x.ActorId == TestOnlyPolicy.ActorId
                        && x.Kind == RestDebtEventKind.Opened),
                    "The setup did not produce two unpaid supported-day gates and Rest Debt.");

                milestone = "Haven-care admission discovery";
                var discovered = simulation.DiscoverCommands(host, TestOnlyPolicy.ActorId)
                    .Single(x => x.Command.Kind == CommandKind.BeginHavenCare);
                byte[] beforeBeginQuery = Bytes(simulation);
                var beginQuery = simulation.QueryCommand(host, discovered.Command);
                Require(discovered.Query.Supported && discovered.Query.Admissible && beginQuery.Admissible
                    && beforeBeginQuery.SequenceEqual(Bytes(simulation)),
                    "Starting Haven care was not discoverable and pure at its qualified site.");
                WorldCommit(simulation, discovered.Command);
                var active = simulation.Capture().ExpeditionHavenCareIntervals.Single();
                Require(active.Status == HavenCareIntervalStatus.Active && active.StartedAt == T(48 * 60 * 60)
                    && active.ScheduledEnd == T(72 * 60 * 60),
                    "Haven-care did not create its exact 24-hour shared-clock interval.");
                byte[] careStartBytes = Bytes(simulation);
                string careStartPath = Path.Combine(directory, "haven-care-start.ddsave");
                var store = new FileSaveStore();
                store.Save(careStartPath, simulation.Capture());
                var careStartRestored = new Simulation(policy, store.Load(careStartPath), ExecutionProfile.Laboratory);
                Require(careStartBytes.SequenceEqual(Bytes(careStartRestored)),
                    "An active schema66 Haven interval changed through save/restore.");

                var blockedMove = IC(simulation, CommandKind.BeginWorldStep, "walk", actor: TestOnlyPolicy.ActorId, x: 0, y: 1);
                byte[] beforeBlockedMove = Bytes(simulation);
                var blockedMoveQuery = simulation.QueryCommand(host, blockedMove);
                var blockedMoveResult = simulation.Execute(host, blockedMove);
                Require(blockedMoveQuery.Supported && !blockedMoveQuery.Admissible
                    && blockedMoveQuery.Code == "ActorCurrentlyInHavenCare"
                    && blockedMoveResult.Outcome == Outcome.Rejected
                    && blockedMoveResult.Code == "ActorCurrentlyInHavenCare"
                    && beforeBlockedMove.SequenceEqual(Bytes(simulation)),
                    "Care did not require explicit interruption before patient travel.");
                var unregisteredPatient = new Command("haven.not-admitted", TestOnlyPolicy.CompanionId,
                    simulation.Capture().Revision, CommandKind.BeginHavenCare, "TEST_ONLY.haven-care-service");
                var unregisteredQuery = simulation.QueryCommand(host, unregisteredPatient);
                RejectUnchanged(simulation, host, unregisteredPatient, "HavenCarePatientNotAdmitted");
                Require(unregisteredQuery.Supported && !unregisteredQuery.Admissible
                    && unregisteredQuery.Code == "HavenCarePatientNotAdmitted",
                    "A patient outside the finite TEST_ONLY admission roster was not rejected consistently.");

                // An unsupported care window cannot recover the points at its endpoint.
                milestone = "unsupported care attempt";
                var unsupported = new Simulation(policy, new SnapshotCodec().Decode(careStartBytes),
                    ExecutionProfile.Laboratory);
                WorldAdvance(unsupported, 24 * 60 * 60);
                var unsupportedState = unsupported.Capture();
                var unsupportedAssessment = unsupportedState.ExpeditionHavenCareAssessments.SingleOrDefault();
                Require(unsupportedAssessment != null
                    && unsupportedState.RuleClock == T(72 * 60 * 60)
                    && unsupportedAssessment.CompletedAt == T(72 * 60 * 60)
                    && !unsupportedAssessment.SupportQualified && unsupportedAssessment.EligiblePointIds.Length == 0
                    && unsupportedState.ExpeditionStrainRemovals.All(x => x.RecoveryKind != ExpeditionRecoveryKind.HavenCare),
                    "An unsupported Haven interval granted or retroactively applied recovery. clock="
                    + unsupportedState.RuleClock + ", intervals=" + string.Join(";", unsupportedState.ExpeditionHavenCareIntervals
                        .Select(x => x.Id + ":" + x.Status + ":" + x.ScheduledEnd))
                    + ", assessments=" + unsupportedState.ExpeditionHavenCareAssessments.Length
                    + ", actor=" + unsupportedState.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X + ","
                    + unsupportedState.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y
                    + ", dead=" + unsupportedState.Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).Dead
                    + ", encounter=" + (unsupportedState.Encounter != null)
                    + ", inventoryCombat=" + unsupportedState.InventoryCombat);

                // Interruption starts a fresh 24-hour attempt; the original deadline cannot complete it.
                milestone = "interrupted fresh attempt";
                var restart = new Simulation(policy, new SnapshotCodec().Decode(careStartBytes),
                    ExecutionProfile.Laboratory);
                WorldCommit(restart, IC(restart, CommandKind.InterruptHavenCare, active.Id));
                WorldAdvance(restart, 60 * 60);
                WorldCommit(restart, IC(restart, CommandKind.BeginHavenCare, "TEST_ONLY.haven-care-service"));
                var restartedInterval = restart.Capture().ExpeditionHavenCareIntervals.Single(x =>
                    x.Status == HavenCareIntervalStatus.Active);
                Require(restartedInterval.StartedAt == T(49 * 60 * 60)
                    && restartedInterval.ScheduledEnd == T(73 * 60 * 60),
                    "Restarting care reused the interrupted interval's old completion deadline.");
                WorldAdvance(restart, 23 * 60 * 60);
                Require(restart.Capture().RuleClock == T(72 * 60 * 60)
                    && restart.Capture().ExpeditionHavenCareIntervals.Single(x => x.Id == restartedInterval.Id).Status
                        == HavenCareIntervalStatus.Active
                    && restart.Capture().ExpeditionHavenCareAssessments.All(x => x.IntervalId != restartedInterval.Id),
                    "A restarted interval completed at the abandoned attempt's original deadline.");

                // Real shared authorities consume all food and water during the care window while
                // the companion performs ordinary Camp Greens planting at the adjacent plot.
                milestone = "real intake and companion planting";
                const string cropId = "TEST_ONLY.haven-care-companion-crop";
                var planting = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.CropPlanting, cropId);
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.AssignExpeditionWork,
                    request: planting, actor: TestOnlyPolicy.CompanionId));
                var assignment = simulation.Capture().ExpeditionAssignments.Single(x =>
                    x.WorkerId == TestOnlyPolicy.CompanionId && x.Open);
                Require(assignment.Status == ExpeditionAssignmentStatus.Ready,
                    "The companion was not ready for its authored Camp Greens task.");
                WorldCommit(simulation, ExpeditionCommand(simulation, CommandKind.StartExpeditionWork,
                    assignment.Id, actor: TestOnlyPolicy.CompanionId));

                HavenCareIntake(simulation, TestOnlyInventoryPolicy.FoodId, new RuleQuantity(2), 30 * 60,
                    "haven.food");
                HavenCareIntake(simulation, TestOnlyInventoryPolicy.WaterId, new RuleQuantity(4), 4 * 60,
                    "haven.water.initial");
                WorldAdvance(simulation, 26 * 60);
                Require(simulation.Capture().Crops.Single(x => x.Id == cropId).Tasks.Single().Status
                    == CropWorkStatus.Complete,
                    "The companion did not complete its hour-long planting assignment during Haven care.");
                HavenCareFillAndDrink(simulation, 1);

                milestone = "mid-interval save and replay";
                var midCare = simulation.Capture();
                var crop = midCare.Crops.Single(x => x.Id == cropId);
                Require(midCare.ExpeditionHavenCareIntervals.Single(x => x.Id == active.Id).Status
                        == HavenCareIntervalStatus.Active
                    && crop.Tasks.Single().Status == CropWorkStatus.Complete
                    && midCare.Intakes.Where(x => x.ActorId == TestOnlyPolicy.ActorId && x.Status == IntakeStatus.Complete).Any(),
                    "The active care window did not share time with real food, water and companion work.");
                string midCarePath = Path.Combine(directory, "haven-care-midinterval.ddsave");
                byte[] midCareBytes = Bytes(simulation);
                store.Save(midCarePath, midCare);
                var restored = new Simulation(policy, store.Load(midCarePath), ExecutionProfile.Laboratory);
                Require(midCareBytes.SequenceEqual(Bytes(restored)),
                    "The active care interval, intake evidence or work reservation changed through save/restore.");

                milestone = "same-boundary Morale Rest and care completion";
                const int secondsToHour68 = 18 * 60 * 60 + 54 * 60 + 58;
                WorldAdvance(simulation, secondsToHour68);
                WorldAdvance(restored, secondsToHour68);
                Require(Bytes(simulation).SequenceEqual(Bytes(restored))
                    && simulation.Capture().Crops.Single(x => x.Id == cropId).Tasks.Single().Status == CropWorkStatus.Complete,
                    "Restored deterministic replay diverged or companion work failed to complete.");
                var moraleStart = simulation.DiscoverCommands(host, TestOnlyPolicy.ActorId)
                    .Single(x => x.Command.Kind == CommandKind.BeginMoraleRest).Command;
                WorldCommit(simulation, moraleStart);
                WorldCommit(restored, moraleStart);
                WorldAdvance(simulation, 4 * 60 * 60);
                WorldAdvance(restored, 4 * 60 * 60);
                var completed = simulation.Capture();
                Require(Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Full care completion and typed recovery diverged after save/restore replay.");
                var interval = completed.ExpeditionHavenCareIntervals.Single(x => x.Id == active.Id);
                var assessment = completed.ExpeditionHavenCareAssessments.Single(x => x.IntervalId == active.Id);
                var batch = completed.ExpeditionStrainRemovals.Where(x =>
                        x.RecoveryKind == ExpeditionRecoveryKind.HavenCare && x.RecoveryCompletionId == assessment.Id)
                    .OrderBy(x => x.MutationSequence).ToArray();
                var restDebtPoints = completed.ExpeditionStrainGains.Where(x => x.ActorId == TestOnlyPolicy.ActorId
                    && (x.CauseKind == ExpeditionStrainCauseKind.RestDebtDeadline
                        || x.CauseKind == ExpeditionStrainCauseKind.RestMissedWhileIndebted)).ToArray();
                var moraleBenefit = completed.ExpeditionMoraleRestBenefits.Single();
                Require(completed.RuleClock == T(72 * 60 * 60)
                    && interval.Status == HavenCareIntervalStatus.Completed && interval.EndedAt == interval.ScheduledEnd
                    && interval.EndRevision == assessment.Revision
                    && interval.EndCommandRevision <= interval.EndRevision
                    && assessment.SupportQualified && assessment.FoodConsumed == new RuleQuantity(2)
                    && assessment.WaterConsumed == new RuleQuantity(8)
                    && assessment.EligiblePointIds.SequenceEqual(priorPointIds, StringComparer.Ordinal)
                    && batch.Select(x => x.PointId).SequenceEqual(priorPointIds, StringComparer.Ordinal)
                    && batch.Length == 2
                    && batch.Select(x => x.MutationSequence).SequenceEqual(
                        batch.Select(x => x.MutationSequence).OrderBy(x => x))
                    && completed.ExpeditionStrainRemovals.Count(x => x.RecoveryKind == ExpeditionRecoveryKind.HavenCare) == 2
                    && moraleBenefit.CompletedAt == T(72 * 60 * 60) && moraleBenefit.RecoveryOfferId == ""
                    && completed.ExpeditionStrainRecoveryOffers.Length == 0
                    && completed.RestDebtEvents.Any(x => x.ActorId == TestOnlyPolicy.ActorId
                        && x.Kind == RestDebtEventKind.Opened)
                    && completed.RestDebtEvents.Last(x => x.ActorId == TestOnlyPolicy.ActorId).Kind
                        == RestDebtEventKind.MissedWhileIndebted
                    && restDebtPoints.Length == 2 && restDebtPoints.All(x => x.OrdinaryRemovable == null
                        && x.RemovalGateMet == null)
                    && ExpeditionStrainRules.Current(completed, TestOnlyPolicy.ActorId).Level == 2,
                    "Haven care did not apply the exact supported batch before a same-boundary Morale offer. clock="
                    + completed.RuleClock + ", interval=" + interval.Status + ", end=" + interval.EndedAt
                    + ", endRevision=" + interval.EndRevision + ", assessment=" + assessment.SupportQualified
                    + ":food=" + assessment.FoodConsumed + ":water=" + assessment.WaterConsumed
                    + ":block=" + assessment.ProvisioningBlockActive
                    + ", eligible=" + string.Join(",", assessment.EligiblePointIds)
                    + ", prior=" + string.Join(",", priorPointIds)
                    + ", batch=" + string.Join(",", batch.Select(x => x.PointId))
                    + ", debtPoints=" + restDebtPoints.Length + ", lastDebt="
                    + completed.RestDebtEvents.Last(x => x.ActorId == TestOnlyPolicy.ActorId).Kind
                    + ", morale=" + moraleBenefit.CompletedAt + ":offer=" + moraleBenefit.RecoveryOfferId
                    + ", offers=" + completed.ExpeditionStrainRecoveryOffers.Length
                    + ", strain=" + ExpeditionStrainRules.Current(completed, TestOnlyPolicy.ActorId).Level);

                // The current policy validator deterministically replays the complete committed
                // command receipt history, including the interval's authorizing receipt and apply revision.
                var finalBytes = Bytes(simulation);
                var replayed = new Simulation(policy, new SnapshotCodec().Decode(finalBytes), ExecutionProfile.Laboratory);
                Require(finalBytes.SequenceEqual(Bytes(replayed)),
                    "The completed care scenario did not reproduce byte-for-byte from its saved command history.");

                milestone = "later ordinary death and historical care replay";
                bool dead = false;
                for (int day = 0; day < 10 && !dead; day++)
                {
                    WorldAdvance(simulation, 24 * 60 * 60);
                    dead = simulation.Capture().Lives.Single(x => x.ActorId == TestOnlyPolicy.ActorId).Dead;
                }
                Require(dead && simulation.Capture().ExpeditionHavenCareAssessments.Any(x => x.IntervalId == active.Id),
                    "The shared provisioning/Strain authorities did not reach ordinary death after completed care.");
                byte[] deathBytes = Bytes(simulation);
                string deathPath = Path.Combine(directory, "haven-care-later-death.ddsave");
                store.Save(deathPath, simulation.Capture());
                var deathRestored = new Simulation(policy, store.Load(deathPath), ExecutionProfile.Laboratory);
                Require(deathBytes.SequenceEqual(Bytes(deathRestored)),
                    "A later ordinary death rejected or changed the earlier care assessment during save/replay.");
                }
                catch (Exception ex)
                {
                    throw new Exception("Haven-care scenario failed at " + milestone + ".", ex);
                }
            });
        }
    }
}
#endif
