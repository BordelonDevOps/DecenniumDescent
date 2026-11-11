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
        private const string PlanHero = TestOnlyNextCharterPlanProfile.PlannerId;
        private const string PlanVersion = TestOnlyNextCharterPlanProfile.VersionId;

        private static TestOnlySharedWorldPolicy PlanPolicy(TestOnlyNextCharterPlanProfile profile = null,
            ConditionCombatFixture conditions = null, CraftingMishapFact incident = null)
            => BillPolicy(conditions: conditions, incident: incident).EnableExpeditionClose(new TestOnlyExpeditionCloseProfile())
                .EnableNextCharterPlan(profile ?? new TestOnlyNextCharterPlanProfile());

        private static Command PlanCommand(Simulation sim, CommandKind kind = CommandKind.StartNextCharterPlan,
            string target = PlanVersion, string actor = PlanHero) => MiningCommand(sim, kind, target, actor: actor);

        private static NextCharterPlanRecord PlanJob(Simulation sim) => sim.Capture().NextCharterPlans.Last();

        private static void PlanWalk(Simulation sim, int x, int y, string actor = PlanHero)
        {
            WorldStep(sim, x, y, actor: actor);
            WorldAdvance(sim, 6);
        }

        private static Simulation PlanReady(TestOnlySharedWorldPolicy policy = null, bool passage = true, bool atDesk = true, Action<Snapshot> beforeClose = null)
        {
            var sim = MealAtCounter(policy ?? PlanPolicy(), withEncounter: true);
            SaleCommit(sim, PurchaseMeal(sim));
            InterruptCloseMeal(sim);
            WorldCommit(sim, IC(sim, CommandKind.PortionInventory, HavenMealLot, new InventoryRequest(new RuleQuantity(1, 6)), SaleSeller));
            string portion = sim.Capture().InventoryLots.Single(x => x.ParentId == HavenMealLot).LotId;
            PortableCommit(sim, HandleMeal(sim, HandlingKind.Drop));
            WorldAdvance(sim, 6);
            PortableCommit(sim, HandleMeal(sim, HandlingKind.Drop, portion));
            if (passage) {
                PlanWalk(sim, 1, 0, SaleSeller);
                PlanWalk(sim, -1, 0, SaleSeller);
            }
            PortableCommit(sim, HandleMeal(sim, HandlingKind.Pickup, portion));
            WorldAdvance(sim, 6);
            EatMeal(sim, new RuleQuantity(1, 6), portion);
            WorldAdvance(sim, 156);
            PortableCommit(sim, HandleMeal(sim, HandlingKind.Pickup));
            WorldAdvance(sim, 6);
            EatMeal(sim, new RuleQuantity(1, 3));
            WorldAdvance(sim, 300);
            SaleCommit(sim, BillCommand(sim));
            WorldAdvance(sim, 1800);
            beforeClose?.Invoke(sim.Capture());
            SaleCommit(sim, CloseCommand(sim));
            Require(Closure(sim).Members.Single(x => x.ActorId == SaleSeller).X == new RuleQuantity(2),
                "Historical passage must be usable even when the witness later closes at the desk.");
            PlanWalk(sim, 1, 0, SaleSeller);
            if (atDesk) {
                PlanWalk(sim, -1, 0);
                PlanWalk(sim, 0, 1);
                PlanWalk(sim, 0, 1);
                PlanWalk(sim, 0, 1);
                PlanWalk(sim, 1, 0);
            }
            return sim;
        }

        private static void AddNextCharterPlanCases(Dictionary<string, Action> cases, string directory)
        {
            var host = HavenSaleHost();
            var planner = new Authority(host.Principal, new[] { PlanHero });

            cases.Add("mgt10_next_charter_connected_exact_shared_labor_and_replay", () =>
            {
                var sim = PlanReady();
                var start = PlanCommand(sim);
                var before = sim.Capture();
                var query = sim.QueryCommand(planner, start);
                Require(query.Supported && query.Admissible && query.NextCharterPlanAssessment?.Occupied == true
                    && query.NextCharterPlanAssessment.Walkable
                    && sim.DiscoverCommands(planner, PlanHero).Any(x => x.Command.Kind == start.Kind && x.Query.Admissible)
                    && new SnapshotCodec().Encode(before).SequenceEqual(Bytes(sim)), "Authorized preview changed state or hid the occupied edge: " + query.Code);
                var commandResult = sim.Execute(planner, start);
                Require(commandResult.Outcome == Outcome.Committed, "Planning admission failed: " + commandResult.Code);
                Require(sim.Execute(planner, start).Outcome == Outcome.Duplicate, "Planning start was not idempotent.");
                RejectUnchanged(sim, planner, new Command(start.Id, start.Actor, start.ExpectedRevision, start.Kind, "different-plan"), "CommandIdConflict");
                var job = PlanJob(sim);
                var admitted = sim.Capture();
                Require(admitted.SchemaVersion == Snapshot.NextCharterPlanSchema && job.PriorCloseRevision == before.ExpeditionEpisodeClose.CloseRevision
                    && job.PassageRevision < job.PriorCloseRevision && job.Work.Labor == default && job.Report == null
                    && admitted.RuleClock == before.RuleClock && admitted.RandomState == before.RandomState
                    && !admitted.Work.Reservations.Any(x => x.JobId == job.Id), "Admission lost the prior basis or changed gameplay state.");
                var controls = sim.DiscoverCommands(planner, PlanHero);
                Require(WorldActivityProjection.OpenProcedures(admitted, controls).Any(x => x.Kind == WorldProcedureKind.NextCharterPlan
                    && x.Id == job.Id && x.RecordedWorkDone == T(0) && x.RecordedWorkRequired == T(3600)),
                    "The shared activity projection did not identify the active planner's job.");
                SaveBill(sim, PlanPolicy(), directory, "mgt10-plan-active");
                WorldAdvance(sim, 1, 2);
                SaleCommit(sim, PlanCommand(sim, CommandKind.PauseNextCharterPlan, job.Id));
                WorldAdvance(sim, 13, 2);
                Require(PlanJob(sim).Work.Labor == new RuleTime(1, 2), "Paused time was counted as labor.");
                var replay = SaveBill(sim, PlanPolicy(), directory, "mgt10-plan-paused");
                foreach (var branch in new[] { sim, replay }) {
                    SaleCommit(branch, PlanCommand(branch, CommandKind.ResumeNextCharterPlan, job.Id));
                    WorldAdvance(branch, 3599);
                    Require(PlanJob(branch).Work.Labor == new RuleTime(7199, 2) && PlanJob(branch).Report == null,
                        "A report appeared before the actual 3,600 seconds.");
                    WorldAdvance(branch, 1, 2);
                    var completed = PlanJob(branch);
                    var after = branch.Capture();
                    var report = completed.Report;
                    Require(completed.Status == NextCharterPlanStatus.CompletedConditional && completed.Work.Labor == T(3600)
                        && completed.UpdatedAt == new RuleTime(before.RuleClock.Numerator * 2 + 7213, 2)
                        && report.At == after.RuleClock && report.Revision == after.Revision && report.Occupied
                        && !report.CharterAccepted && !report.DeparturePermitted && !report.AccessibilityCheckPerformed
                        && !completed.Terms.SupportCommitted && completed.Terms.SupportProposedCarried
                        && after.RandomState == before.RandomState && after.ExpeditionEpisodeClose.CloseRevision == job.PriorCloseRevision
                        && after.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))
                            .SequenceEqual(before.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))),
                        "Completion altered resources, credited the future activity, or lost report provenance.");
                    Require(report.ActualPounds == PortableEquipmentRules.CarriedBurden(after, PlanHero).Pounds
                        && report.Supplies[0].Lots.Single().PhysicalAmount == new RuleQuantity(20)
                        && report.Supplies[0].Required == new RuleQuantity(4)
                        && report.Supplies[1].EligibleAvailable == new RuleQuantity(4) && report.Supplies[2].EligibleAvailable == default
                        && report.Supplies[2].Lots.Single().PhysicalAmount == new RuleQuantity(4)
                        && report.Supplies[2].VesselLocationId == SupplyCacheFixture.CacheId
                        && report.Supplies[2].Deficit == new RuleQuantity(4)
                        && after.RuleClock > after.ExpeditionBillCharter.AuthorizationUntil
                        && report.Supplies[1].VesselId == PortableKitFixture.Skin && report.Supplies[2].VesselId == TestOnlyFillingPolicy.ActorSkinId
                        && report.Pressure == null && report.Strain == null && report.RestDebt == null && !report.WiderObligationsResolved
                        && !report.HazardSafetyEstablished && completed.Terms.NewCashLimitCopper == 0
                        && after.InventoryLots.Single(x => x.LotId == SaleTender).OwnerId == SaleBuyer,
                        "The report assumed risk, counted an unrelated source, or underweighted physical stock.");
                    RejectUnchanged(branch, planner, PlanCommand(branch), "NextCharterPlanningAlreadyCompleted");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Identical resumed planning diverged after disk restore.");
                var continued = SaveBill(sim, PlanPolicy(), directory, "mgt10-plan-complete");
                foreach (var branch in new[] { sim, continued }) {
                    PlanWalk(branch, -1, 0);
                    Require(PlanJob(branch).Report.Occupied && PlanJob(branch).Report.ScoutAtStage, "Later movement altered the historical report.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(continued)), "Ordinary continuation diverged after completed-plan restore.");
                SaveBill(sim, PlanPolicy(), directory, "mgt10-plan-continued");
                File.WriteAllLines(Path.Combine(directory, "mgt10-plan-connected.tsv"), new[] {
                    PlanAudit("historical-completion", PlanJob(sim), PlanJob(sim).Report),
                    PlanAudit("ordinary-continuation", PlanJob(sim), InspectPlan(sim, planner)) });
            });

            cases.Add("mgt10_next_charter_admission_separates_authority_past_passage_and_current_conditions", () =>
            {
                var fresh = PortableWorld(PlanPolicy());
                RejectUnchanged(fresh, planner, PlanCommand(fresh), "NextCharterPlanningCloseRequired");
                var noPassage = PlanReady(passage: false);
                RejectUnchanged(noPassage, planner, PlanCommand(noPassage), "NextCharterPlanningPassageEvidenceMissing");
                var remote = PlanReady(atDesk: false);
                RejectUnchanged(remote, planner, PlanCommand(remote), "NextCharterPlanningWorkerNotAtDesk");
                var sim = PlanReady();
                RejectUnchanged(sim, new Authority("no-hero", new[] { SaleSeller }), PlanCommand(sim), "NotAuthorized");
                RejectUnchanged(sim, host, PlanCommand(sim, actor: SaleSeller), "NextCharterPlanningWorkerUnauthorized");
                RejectUnchanged(sim, planner, PlanCommand(sim, target: "other-plan"), "NextCharterPlanningDefinitionUnknown");
                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations, handling: HandlingKind.Retrieve));
                WorldAdvance(sim, 6);
                WorldCommit(sim, IC(sim, CommandKind.StartIntake, PortableKitFixture.Rations, new InventoryRequest(new RuleQuantity(1))));
                RejectUnchanged(sim, planner, PlanCommand(sim), "NextCharterPlanningWorkerBusy");
                foreach (var entry in new[] {
                    (new TestOnlyNextCharterPlanProfile(mandateAuthorized: false), "NextCharterPlanningMandateMissing"),
                    (new TestOnlyNextCharterPlanProfile(evidenceAccessible: false), "NextCharterPlanningEvidenceUnavailable"),
                    (new TestOnlyNextCharterPlanProfile(deskPermitted: false), "NextCharterPlanningDeskUnavailable"),
                    (new TestOnlyNextCharterPlanProfile(writingFacilitiesAvailable: false), "NextCharterPlanningDeskUnavailable"),
                    (new TestOnlyNextCharterPlanProfile(duplicateWaterSource: true), "NextCharterPlanningWaterSourcesNotDistinct")
                }) {
                    var run = PlanReady(PlanPolicy(entry.Item1));
                    Require(run.QueryCommand(planner, PlanCommand(run)).Code == entry.Item2, "Preview admitted invalid authority or stock identity.");
                    RejectUnchanged(run, planner, PlanCommand(run), entry.Item2);
                }
                var unknown = PlanReady(PlanPolicy(new TestOnlyNextCharterPlanProfile(approachAccess: null)));
                SaleCommit(unknown, PlanCommand(unknown));
                WorldAdvance(unknown, 3600);
                Require(PlanJob(unknown).Report?.ApproachAccess == null && PlanJob(unknown).Status == NextCharterPlanStatus.CompletedConditional,
                    "Unresolved prospective access should survive in a valid conditional report.");
            });

            cases.Add("mgt10_next_charter_stock_claims_custody_access_and_live_reassessment", () =>
            {
                var sim = PlanReady();
                var preview = sim.QueryCommand(planner, PlanCommand(sim)).NextCharterPlanAssessment;
                Require(preview != null && preview.Supplies[0].EligibleAvailable == new RuleQuantity(20) && preview.Supplies[0].RequiresPreparation,
                    "Initial preview failed to distinguish physical from ready stock.");
                SaleCommit(sim, PlanCommand(sim));
                WorldAdvance(sim, 1, 2);
                string job = PlanJob(sim).Id;
                SaleCommit(sim, PlanCommand(sim, CommandKind.PauseNextCharterPlan, job));
                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations, handling: HandlingKind.Retrieve));
                WorldAdvance(sim, 6);
                WorldCommit(sim, IC(sim, CommandKind.PortionInventory, PortableKitFixture.Rations, new InventoryRequest(new RuleQuantity(17))));
                string portion = sim.Capture().InventoryLots.Single(x => x.ParentId == PortableKitFixture.Rations).LotId;
                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, portion, SaleSeller, HandlingKind.Handover));
                WorldAdvance(sim, 6);
                PortableCommit(sim, Portable(sim, CommandKind.ClosePortableContainer, PortableKitFixture.Pack));
                WorldAdvance(sim, 6);
                var resume = sim.QueryCommand(planner, PlanCommand(sim, CommandKind.ResumeNextCharterPlan, job));
                Require(resume.Admissible && resume.NextCharterPlanAssessment.Supplies[0].Deficit == new RuleQuantity(1), "Resume ignored the cumulative ration deficit.");
                SaleCommit(sim, PlanCommand(sim, CommandKind.ResumeNextCharterPlan, job));
                WorldAdvance(sim, 7199, 2);
                var historical = PlanJob(sim).Report;
                Require(historical != null && historical.Occupied && historical.Supplies[0].Deficit == new RuleQuantity(1)
                    && historical.Supplies[0].Lots.Single(x => x.LotId == portion).OwnerId == PlanHero
                    && historical.Supplies[0].Lots.Single(x => x.LotId == portion).CustodianId == SaleSeller
                    && historical.Supplies[1].EligibleAvailable == new RuleQuantity(4) && historical.Supplies[1].AccessibleAvailable == default
                    && historical.Supplies[1].RequiresPreparation && historical.Supplies[2].VesselLocationId == SupplyCacheFixture.CacheId && historical.Supplies[2].ReadyAvailable == default,
                    "Completion conflated ownership, custody, vessel accessibility or current occupancy.");
                PortableCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, portion, PlanHero, HandlingKind.Handover, SaleSeller));
                WorldAdvance(sim, 6);
                PlanWalk(sim, -1, 0);
                PlanWalk(sim, 1, 0, SaleSeller);
                PlanWalk(sim, 1, 0);
                var recovered = InspectPlan(sim, planner);
                Require(recovered != null && !recovered.Occupied && recovered.Revision == sim.Capture().Revision
                    && recovered.At > historical.At && recovered.Supplies[0].EligibleAvailable == new RuleQuantity(20)
                    && recovered.Supplies[0].Deficit == default && !recovered.DeparturePermitted,
                    "Later actual improvements did not appear in the current projection.");
                WorldCommit(sim, IC(sim, CommandKind.StartIntake, portion, new InventoryRequest(new RuleQuantity(16))));
                var exact = InspectPlan(sim, planner);
                Require(exact.Supplies[0].EligibleAvailable == new RuleQuantity(4) && exact.Supplies[0].Deficit == default,
                    "Exactly four unreserved pounds did not cover both proposed allocations.");
                WorldCommit(sim, IC(sim, CommandKind.InterruptIntake, sim.Capture().Intakes.Last().Id));
                WorldCommit(sim, IC(sim, CommandKind.StartIntake, portion, new InventoryRequest(new RuleQuantity(17))));
                var claimed = InspectPlan(sim, planner);
                Require(claimed.Supplies[0].EligibleAvailable == new RuleQuantity(3) && claimed.Supplies[0].Deficit == new RuleQuantity(1)
                    && claimed.Supplies[0].Lots.Single(x => x.LotId == portion).PhysicalAmount == new RuleQuantity(17)
                    && ReferenceEquals(PlanJob(sim).Report, historical), "A real competing claim was counted twice or rewrote the historical report.");
                var inspect = PlanCommand(sim, CommandKind.InspectNextCharterPlan, job);
                RejectUnchanged(sim, planner, inspect, "NextCharterPlanningReadOnly");
                RejectUnchanged(sim, new Authority("no-hero", new[] { SaleSeller }), inspect, "NotAuthorized");
                File.WriteAllLines(Path.Combine(directory, "mgt10-plan-resources.tsv"), new[] {
                    PlanAudit("historical-shortage", PlanJob(sim), historical), PlanAudit("later-recovered", PlanJob(sim), recovered), PlanAudit("exact-four", PlanJob(sim), exact),
                    PlanAudit("competing-claim", PlanJob(sim), claimed) });
                SaveBill(sim, PlanPolicy(), directory, "mgt10-plan-live-claim");
            });

            cases.Add("mgt10_next_charter_shared_interruption_cancel_station_and_handling", () =>
            {
                var sim = PlanReady();
                SaleCommit(sim, PlanCommand(sim));
                string first = PlanJob(sim).Id;
                WorldAdvance(sim, 1, 2);
                SaleCommit(sim, Portable(sim, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Drop, actor: SaleBuyer));
                Require(PlanJob(sim).Work.Labor == new RuleTime(3, 2), "Unrelated timed handling did not credit exactly one second.");
                WorldCommit(sim, IC(sim, CommandKind.BeginFixedEncounter));
                Require(PlanJob(sim).Status == NextCharterPlanStatus.Paused && PlanJob(sim).Work.Labor == new RuleTime(3, 2),
                    "Tactical control failed to interrupt actual labor.");
                SaleCommit(sim, PlanCommand(sim, CommandKind.CancelNextCharterPlan, first));
                Require(PlanJob(sim).Status == NextCharterPlanStatus.Cancelled && PlanJob(sim).Report == null
                    && sim.Capture().Work.WorkerIntervals.All(x => x.JobId != first || x.End <= sim.Capture().RuleClock),
                    "Cancellation discarded elapsed labor or left a booking.");
                var restarted = PlanReady();
                SaleCommit(restarted, PlanCommand(restarted));
                WorldAdvance(restarted, 2);
                SaleCommit(restarted, PlanCommand(restarted, CommandKind.CancelNextCharterPlan, PlanJob(restarted).Id));
                SaleCommit(restarted, PlanCommand(restarted));
                Require(PlanJob(restarted).Work.Labor == default && restarted.Capture().NextCharterPlans.Length == 2,
                    "A new attempt inherited cancelled labor.");
                var at = PlanReady().Capture().RuleClock.AddSeconds(300);
                foreach (int result in new[] { 1, 5 }) {
                    var incident = new CraftingMishapFact("planning-desk-incident", result, at: at, stationId: TestOnlyExpeditionBillProfile.DeskId);
                    var run = PlanReady(PlanPolicy(incident: incident));
                    SaleCommit(run, PlanCommand(run));
                    WorldAdvance(run, 300);
                    CraftEvent(run, incident.Id);
                    var job = PlanJob(run);
                    if (result == 1) {
                        Require(job.Status == NextCharterPlanStatus.Paused && job.Work.Labor == T(300)
                            && job.Reason == "NextCharterPlanningDeskUseBlocked", "A real result-1 restriction failed to pause at its boundary.");
                        RejectUnchanged(run, planner, PlanCommand(run, CommandKind.ResumeNextCharterPlan, job.Id), job.Reason);
                        Remedy(run, incident.Id, actor: PlanHero);
                        WorldAdvance(run, 3606);
                        Require(PlanJob(run).Status == NextCharterPlanStatus.Paused && PlanJob(run).Work.Labor == T(300), "Cleanup resumed planning.");
                        SaleCommit(run, PlanCommand(run, CommandKind.ResumeNextCharterPlan, job.Id));
                    } else {
                        Require(job.Status == NextCharterPlanStatus.Working, "The result-5 crafting-order restriction leaked into planning.");
                    }
                    WorldAdvance(run, 3300);
                    Require(PlanJob(run).Report != null, "Eligible planning failed to finish.");
                }
            });

            cases.Add("mgt10_next_charter_pending_exact_deadline_and_finalize", () =>
            {
                var begin = PlanReady().Capture().RuleClock;
                var endpoint = begin.AddSeconds(3600);
                int deadline = checked((int)endpoint.Numerator);
                Require(endpoint.Denominator == 1, "Expected the fixed scenario to end on a whole second.");
                var tie = PlanReady(PlanPolicy(new TestOnlyNextCharterPlanProfile(authorizationUntil: deadline)));
                RejectUnchanged(tie, planner, PlanCommand(tie), "NextCharterPlanningAuthorizationWindow");
                var profile = new TestOnlyNextCharterPlanProfile(authorizationUntil: deadline + 1);
                var paused = PlanReady(PlanPolicy(profile));
                SaleCommit(paused, PlanCommand(paused));
                WorldAdvance(paused, 1, 2);
                string id = PlanJob(paused).Id;
                SaleCommit(paused, PlanCommand(paused, CommandKind.PauseNextCharterPlan, id));
                WorldAdvance(paused, 1);
                RejectUnchanged(paused, planner, PlanCommand(paused, CommandKind.ResumeNextCharterPlan, id), "NextCharterPlanningAuthorizationWindow");
                WorldAdvance(paused, 7199, 2);
                Require(PlanJob(paused).Status == NextCharterPlanStatus.Expired && PlanJob(paused).UpdatedAt == T(deadline + 1),
                    "Paused work survived exact authority expiry.");

                var conditions = new ConditionCombatFixture(CCApply("plan-stun", "Stunned", PlanHero, at: new ConditionStamp(begin)),
                    new ConditionFixtureEvent(PlanHero, ConditionOperation.Grant("event.plan-ward", new ConditionStamp(begin),
                        new ConditionImmunityData("plan-ward", "owner", "ward", new[] { "Stunned" }, new ConditionStamp(endpoint), "ward-end"))),
                    new ConditionFixtureEvent(PlanHero, ConditionOperation.Cure("event.plan-cure", new ConditionStamp(endpoint), "Stunned")));
                var sim = PlanReady(PlanPolicy(profile, conditions));
                SaleCommit(sim, CCCommand(sim, "plan-stun"));
                SaleCommit(sim, CCCommand(sim, "plan-ward"));
                SaleCommit(sim, PlanCommand(sim));
                WorldAdvance(sim, 3600);
                var pending = PlanJob(sim);
                Require(pending.Status == NextCharterPlanStatus.PendingCompletion && pending.Work.Labor == T(3600) && pending.UpdatedAt == endpoint
                    && sim.Capture().Work.WorkerIntervals.All(x => x.JobId != pending.Id || x.End <= endpoint),
                    "Endpoint incapacity did not preserve fully earned unbooked labor: " + pending.Status + " " + pending.Reason);
                var restored = SaveBill(sim, PlanPolicy(profile, conditions), directory, "mgt10-plan-pending");
                WorldAdvance(sim, 1);
                Require(PlanJob(sim).Status == NextCharterPlanStatus.Expired && PlanJob(sim).Report == null, "Pending expiry produced a report.");
                RejectUnchanged(restored, planner, PlanCommand(restored, CommandKind.FinalizeNextCharterPlan, pending.Id), "NextCharterPlanningWorkerIncapable");
                SaleCommit(restored, CCCommand(restored, "plan-cure"));
                Require(PlanJob(restored).Status == NextCharterPlanStatus.PendingCompletion, "Cure finalized without a command.");
                var before = restored.Capture();
                SaleCommit(restored, PlanCommand(restored, CommandKind.FinalizeNextCharterPlan, pending.Id));
                Require(PlanJob(restored).Report != null && restored.Capture().RuleClock == before.RuleClock
                    && restored.Capture().RandomState == before.RandomState, "Explicit finalization consumed time or RNG.");
                WorldAdvance(restored, 1);
                Require(InspectPlan(restored, planner) != null && PlanJob(restored).Report.At == endpoint,
                    "Appointment expiry destroyed the valid completed report or current read authority.");
                SaveBill(restored, PlanPolicy(profile, conditions), directory, "mgt10-plan-finalized");
            });

            cases.Add("mgt10_next_charter_carried_reserve_positive_fixture_preserves_actual_mass_and_history", () =>
            {
                var positive = new TestOnlyNextCharterPlanProfile(reserveWaterStartsCarried: true);
                var cacheInitial = PortableWorld(PlanPolicy()).Capture();
                var carriedInitial = PortableWorld(PlanPolicy(positive)).Capture();
                VerifyWaterPlacement(cacheInitial, SupplyCacheFixture.CacheId, InventoryAccess.Ground);
                VerifyWaterPlacement(carriedInitial, PlanHero, InventoryAccess.Ready);
                Require(cacheInitial.ContentFingerprint != carriedInitial.ContentFingerprint,
                    "The initial placement choice did not bind the exact save profile.");
                var codec = new SnapshotCodec();
                File.WriteAllBytes(Path.Combine(directory, "mgt10-plan-cache-initial.ddsave"), codec.Encode(cacheInitial));
                File.WriteAllBytes(Path.Combine(directory, "mgt10-plan-carried-initial.ddsave"), codec.Encode(carriedInitial));
                var sim = PlanReady(PlanPolicy(positive), beforeClose: state => {
                    VerifyWaterPlacement(state, PlanHero, InventoryAccess.Ready);
                    File.WriteAllBytes(Path.Combine(directory, "mgt10-plan-carried-before-close.ddsave"), codec.Encode(state));
                });
                var before = sim.Capture();
                VerifyWaterPlacement(before, PlanHero, InventoryAccess.Ready);
                Require(before.ExpeditionEpisodeClose.Vessels.Single(x => x.Id == TestOnlyFillingPolicy.ActorSkinId).LocationId == PlanHero
                    && before.ExpeditionEpisodeClose.Stock.Single(x => x.Stock.Id == TestOnlyInventoryPolicy.WaterId).Stock.Amount == new RuleQuantity(4),
                    "The immutable close did not observe the carried starting arrangement.");
                var replay = SaveBill(sim, PlanPolicy(positive), directory, "mgt10-plan-carried-after-close");
                RejectUnchanged(sim, host, IC(sim, CommandKind.HandleVessel, TestOnlyFillingPolicy.ActorSkinId,
                    new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Drop)), "PortableEquipmentRequired");
                foreach (var branch in new[] { sim, replay }) {
                    var start = PlanCommand(branch);
                    byte[] beforeQuery = Bytes(branch);
                    var preview = branch.QueryCommand(planner, start).NextCharterPlanAssessment;
                    Require(preview != null && preview.Supplies.Skip(1).All(x => x.EligibleAvailable == new RuleQuantity(4))
                        && preview.Supplies[2].ReadyAvailable == new RuleQuantity(4) && preview.ActualPounds == new RuleQuantity(68)
                        && beforeQuery.SequenceEqual(Bytes(branch)), "The available reserve or its actual mass was not observed at the desk.");
                    SaleCommit(branch, start);
                    VerifyWaterPlacement(branch.Capture(), PlanHero, InventoryAccess.Ready);
                    WorldAdvance(branch, 3600);
                    var job = PlanJob(branch);
                    var report = job.Report;
                    var after = branch.Capture();
                    VerifyWaterPlacement(after, PlanHero, InventoryAccess.Ready);
                    Require(job.Status == NextCharterPlanStatus.CompletedConditional && report.ActualPounds == new RuleQuantity(68)
                        && report.ActualPounds == PortableEquipmentRules.CarriedBurden(after, PlanHero).Pounds
                        && report.Supplies[0].Lots.Single().PhysicalAmount == new RuleQuantity(20)
                        && report.Supplies.All(x => x.Deficit == default) && report.Supplies[2].ReadyAvailable == new RuleQuantity(4)
                        && report.Pressure == null && report.Strain == null && report.RestDebt == null
                        && !report.DeparturePermitted && !report.WiderObligationsResolved
                        && after.Work.Reservations.Select(x => (x.Id, x.ConsumedAmount, x.RemainingAmount))
                            .SequenceEqual(before.Work.Reservations.Select(x => (x.Id, x.ConsumedAmount, x.RemainingAmount))),
                        "Sufficient physical support changed placement, stock, readiness, or claims at planning completion.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "The fingerprinted carried arrangement failed deterministic replay.");
                SaveBill(sim, PlanPolicy(positive), directory, "mgt10-plan-carried-complete");
                Throws<ArgumentException>(() => new Simulation(PlanPolicy(), sim.Capture(), ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(PlanPolicy(positive), cacheInitial, ExecutionProfile.Laboratory));
                File.WriteAllLines(Path.Combine(directory, "mgt10-plan-carried.tsv"), new[] {
                    PlanAudit("carried-resource-sufficiency", PlanJob(sim), PlanJob(sim).Report) });
            });

            cases.Add("mgt10_next_charter_replay_rejects_coherent_false_historical_report", () =>
            {
                var sim = PlanReady();
                SaleCommit(sim, PlanCommand(sim));
                WorldAdvance(sim, 3600);
                var actual = PlanJob(sim);
                var report = actual.Report;
                var codec = new SnapshotCodec();
                var fake = new NextCharterPlanObservation(report.At, report.Revision, report.Walkable, !report.Occupied, report.PathReserved,
                    report.TacticalTransition, report.ApproachAccess, report.ScoutCapable, report.ScoutAtStage, report.ActualPounds,
                    report.ActualLoad, report.CanCarry, report.Burdened, 0, report.Strain, report.RestDebt, report.Supplies);
                var forged = sim.Capture();
                forged.NextCharterPlans = new[] { CopyPlan(actual, fake) };
                var decoded = codec.Decode(codec.Encode(forged));
                bool rejectedByReplay = false;
                try { new Simulation(PlanPolicy(), decoded, ExecutionProfile.Laboratory); }
                catch (ArgumentException ex) { rejectedByReplay = ex.Message.Contains("InvalidSharedWorldReplay"); }
                Require(rejectedByReplay, "Coherently encoded false occupancy and pressure bypassed historical replay.");
                var supply = report.Supplies[0];
                var stock = supply.Lots.Single();
                var falseStock = new NextCharterStockObservation(stock.LotId, stock.OwnerId, stock.CustodianId, stock.LocationId,
                    stock.PhysicalAmount, new RuleQuantity(19), stock.UseAuthorized, stock.CorrectCustody, stock.Carried, stock.Suitable, stock.Accessible, stock.Ready);
                var falseSupply = new NextCharterSupplyObservation(supply.RootId, "", null, "", "", "", supply.Required, new[] { falseStock });
                fake = new NextCharterPlanObservation(report.At, report.Revision, report.Walkable, report.Occupied, report.PathReserved,
                    report.TacticalTransition, report.ApproachAccess, report.ScoutCapable, report.ScoutAtStage, report.ActualPounds,
                    report.ActualLoad, report.CanCarry, report.Burdened, report.Pressure, report.Strain, report.RestDebt,
                    new[] { falseSupply, report.Supplies[1], report.Supplies[2] });
                forged.NextCharterPlans = new[] { CopyPlan(actual, fake) };
                Throws<ArgumentException>(() => new Simulation(PlanPolicy(), codec.Decode(codec.Encode(forged)), ExecutionProfile.Laboratory));
                forged.NextCharterPlans = new[] { CopyPlan(actual, report, actual.PriorCloseRevision - 1) };
                Throws<ArgumentException>(() => codec.Encode(forged));
                forged.NextCharterPlans = new[] { new NextCharterPlanRecord(actual.Id, actual.Terms, actual.PriorCloseRevision,
                    actual.PassageRevision, actual.StartRevision, actual.UpdatedRevision, actual.StartedAt, actual.UpdatedAt, T(3599),
                    NextCharterPlanStatus.Cancelled, "forged-labor") };
                Throws<ArgumentException>(() => codec.Encode(forged));
                var substitutedVessel = new NextCharterSupplyObservation(report.Supplies[2].RootId, TestOnlyFillingPolicy.CompanionSkinId,
                    report.Supplies[2].VesselCapacity, report.Supplies[2].VesselOwnerId, report.Supplies[2].VesselCustodianId,
                    report.Supplies[2].VesselLocationId, report.Supplies[2].Required, report.Supplies[2].Lots);
                var falseVessel = CopyPlanObservation(report, report.At, new[] { report.Supplies[0], report.Supplies[1], substitutedVessel });
                Throws<ArgumentException>(() => CopyPlan(actual, falseVessel));
                var early = RuleTime.FromFraction(report.At.Numerator - report.At.Denominator, report.At.Denominator);
                var falseTime = CopyPlanObservation(report, early, report.Supplies);
                Throws<ArgumentException>(() => CopyPlan(actual, falseTime));
                Throws<ArgumentException>(() => new Simulation(PlanPolicy(new TestOnlyNextCharterPlanProfile(authorizationUntil: 47000)),
                    sim.Capture(), ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(ClosePolicy(), sim.Capture(), ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(PlanPolicy(), sim.Capture(), ExecutionProfile.Release));
                PlanWalk(sim, -1, 0);
                SaveBill(sim, PlanPolicy(), directory, "mgt10-plan-historical-after-movement");
            });
        }

        private static void VerifyWaterPlacement(Snapshot state, string expectedLocation, InventoryAccess expectedAccess)
        {
            var skin = state.Vessels.Single(x => x.Id == TestOnlyFillingPolicy.ActorSkinId);
            var stock = state.Work.Lots.Single(x => x.Id == TestOnlyInventoryPolicy.WaterId);
            var inventory = state.InventoryLots.Single(x => x.LotId == stock.Id);
            Require(skin.LocationId == expectedLocation && skin.OwnerId == PlanHero && skin.CustodianId == PlanHero
                && stock.LocationId == skin.Id && stock.Amount == new RuleQuantity(4) && stock.CustodianId == PlanHero
                && inventory.OwnerId == PlanHero && inventory.Access == expectedAccess && inventory.ParentId == ""
                && inventory.CreatedAt == default && inventory.CreatedAmount == new RuleQuantity(4)
                && state.VesselContents.Single(x => x.LotId == stock.Id).VesselId == skin.Id
                && !state.PortableEquipment.Any(x => x.LinkKind == PortableLinkKind.WaterVessel && x.LinkedId == skin.Id)
                && state.VesselContents.Single(x => x.LotId == PortableKitFixture.Water).VesselId == PortableKitFixture.Skin
                && state.Work.Lots.Single(x => x.Id == PortableKitFixture.Water).Amount == new RuleQuantity(4),
                "Initial or connected water placement changed the existing stock, title or vessel linkage.");
        }

        private static NextCharterPlanObservation CopyPlanObservation(NextCharterPlanObservation report, RuleTime at,
            IEnumerable<NextCharterSupplyObservation> supplies)
            => new NextCharterPlanObservation(at, report.Revision, report.Walkable, report.Occupied, report.PathReserved,
                report.TacticalTransition, report.ApproachAccess, report.ScoutCapable, report.ScoutAtStage, report.ActualPounds,
                report.ActualLoad, report.CanCarry, report.Burdened, report.Pressure, report.Strain, report.RestDebt, supplies);

        private static NextCharterPlanRecord CopyPlan(NextCharterPlanRecord job, NextCharterPlanObservation report, long? closeRevision = null)
            => new NextCharterPlanRecord(job.Id, job.Terms, closeRevision ?? job.PriorCloseRevision, job.PassageRevision, job.StartRevision,
                job.UpdatedRevision, job.StartedAt, job.UpdatedAt, job.Work.Labor, job.Status, job.Reason, report);

        private static NextCharterPlanObservation InspectPlan(Simulation sim, Authority planner)
        {
            var command = PlanCommand(sim, CommandKind.InspectNextCharterPlan, PlanJob(sim).Id);
            byte[] before = Bytes(sim);
            var result = sim.QueryCommand(planner, command);
            Require(result.Admissible && result.NextCharterPlanAssessment != null && before.SequenceEqual(Bytes(sim)),
                "Authorized current assessment failed or mutated state: " + result.Code);
            return result.NextCharterPlanAssessment;
        }

        private static string PlanAudit(string label, NextCharterPlanRecord plan, NextCharterPlanObservation observation)
            => string.Join("\t", label, plan.Id, plan.Status, "close-rev=" + plan.PriorCloseRevision,
                "passage-rev=" + plan.PassageRevision, "start-rev=" + plan.StartRevision, "start=" + plan.StartedAt,
                "completion-rev=" + plan.UpdatedRevision, "completion=" + plan.UpdatedAt, "active=" + plan.Work.Labor,
                "non-labor=" + (new RuleQuantity(plan.UpdatedAt.Numerator, plan.UpdatedAt.Denominator)
                    - new RuleQuantity(plan.StartedAt.Numerator, plan.StartedAt.Denominator)
                    - new RuleQuantity(plan.Work.Labor.Numerator, plan.Work.Labor.Denominator)),
                "food=" + plan.Terms.IntendedFood + "+" + plan.Terms.ReserveFood, "water-per-vessel=" + plan.Terms.WaterPerVessel,
                "new-cash-limit=" + plan.Terms.NewCashLimitCopper,
                observation.At, observation.Revision, "walkable=" + observation.Walkable, "occupied=" + observation.Occupied, "path-reserved=" + observation.PathReserved,
                "tactical=" + observation.TacticalTransition, "at-stage=" + observation.ScoutAtStage,
                "scout-capable=" + observation.ScoutCapable, "access=" + (observation.ApproachAccess?.ToString() ?? "unresolved"),
                "pounds=" + observation.ActualPounds, "pressure=" + (observation.Pressure?.ToString() ?? "unresolved"),
                "strain=" + (observation.Strain?.ToString() ?? "unresolved"), "restDebt=" + (observation.RestDebt?.ToString() ?? "unresolved"),
                "accepted=" + observation.CharterAccepted, "departure=" + observation.DeparturePermitted,
                string.Join(";", observation.Supplies.Select(x => string.Join(",", x.RootId, x.VesselId, x.Required,
                    x.EligibleAvailable, x.AccessibleAvailable, x.ReadyAvailable, x.Deficit, x.VesselOwnerId, x.VesselCustodianId, x.VesselLocationId,
                    string.Join("|", x.Lots.Select(lot => string.Join(":", lot.LotId, lot.PhysicalAmount, lot.UnreservedAmount,
                        lot.OwnerId, lot.CustodianId, lot.LocationId, lot.CorrectCustody, lot.Carried, lot.Accessible)))))));
    }
}
#endif

