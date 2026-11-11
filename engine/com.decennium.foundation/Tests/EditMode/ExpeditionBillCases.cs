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
        private const string BillVersion = TestOnlyExpeditionBillProfile.BillVersionId;

        private static TestOnlySharedWorldPolicy BillPolicy(TestOnlyExpeditionBillProfile profile = null,
            ConditionCombatFixture conditions = null, CraftingMishapFact incident = null)
            => MealPolicy(conditions: conditions, incident: incident).EnableExpeditionBill(profile ?? new TestOnlyExpeditionBillProfile());

        private static Simulation BillAtDesk(TestOnlySharedWorldPolicy policy = null, bool withEncounter = false)
        {
            var run = MealAtCounter(policy ?? BillPolicy(), withEncounter);
            BuyAndEatBillMeal(run);
            return run;
        }

        private static void BuyAndEatBillMeal(Simulation run)
        {
            SaleCommit(run, PurchaseMeal(run));
            EatMeal(run, new RuleQuantity(2, 3));
            WorldAdvance(run, 600);
        }

        private static Command BillCommand(Simulation run, CommandKind kind = CommandKind.StartExpeditionBill,
            string target = BillVersion, string actor = SaleSeller) => MiningCommand(run, kind, target, actor: actor);

        private static ExpeditionBillRecord BillJob(Simulation run) => run.Capture().ExpeditionBills.Last();

        private static Simulation SaveBill(Simulation run, TestOnlySharedWorldPolicy policy, string directory, string name)
        {
            string path = Path.Combine(directory, name + ".ddsave");
            new FileSaveStore().Save(path, run.Capture());
            var restored = new Simulation(policy, new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
            Require(Bytes(restored).SequenceEqual(Bytes(run)), "Expedition bill did not roundtrip on disk: " + name);
            return restored;
        }

        private static void AddExpeditionBillCases(Dictionary<string, Action> cases, string directory)
        {
            var host = HavenSaleHost();
            cases.Add("mgt10_expedition_bill_connected_reconciled_replay_and_continue", () =>
            {
                var run = BillAtDesk(withEncounter: true);
                WorldStep(run, 1, 0, actor: SaleSeller);
                WorldAdvance(run, 2);
                RejectUnchanged(run, host, BillCommand(run), "ExpeditionBillWorkerNotAtDesk");
                WorldStep(run, -1, 0, actor: SaleSeller);
                WorldAdvance(run, 6);
                var before = run.Capture();
                var charter = before.ExpeditionBillCharter;
                var sale = before.HavenSales.Single();
                var purchase = before.HavenMealPurchases.Single();
                Require(before.SchemaVersion == Snapshot.ExpeditionBillSchema && charter.AcceptedAt == default
                    && charter.MemberIds.SequenceEqual(new[] { TestOnlyPolicy.ActorId, SaleSeller })
                    && !charter.MemberIds.Contains(SaleBuyer) && charter.BeneficiaryId == SaleSeller
                    && charter.SelfShareRate == default && charter.CapitalOwnerId == TestOnlyPolicy.ActorId
                    && before.PortableEquipment.Any(x => x.Id == charter.CapitalId && x.OwnerId == charter.CapitalOwnerId)
                    && purchase.PriorSaleId == sale.Id && purchase.PriorPaymentRevision == sale.UpdatedRevision
                    && before.HavenAppraisals.Single().ResultCopper == new RuleQuantity(15, 2)
                    && OrdinaryInventory.Consumed(before, SaleSeller, NutritionKind.FoodPounds) == new RuleQuantity(2, 3),
                    "The prospective self-funded roster and real prior activity were not carried into the ledger scenario.");
                var start = BillCommand(run);
                byte[] beforeQuery = Bytes(run);
                var bookkeeper = new Authority(host.Principal, new[] { SaleSeller }, inventoryOwners: Array.Empty<string>());
                var draft = run.QueryCommand(bookkeeper, start);
                Require(draft.Admissible && draft.ExpeditionBillDraft?.GrossSaleCopper == 2
                    && draft.ExpeditionBillDraft.TrueProfitAfterReservesCopper == null
                    && run.DiscoverCommands(bookkeeper, SaleSeller).Any(x => x.Command.Kind == CommandKind.StartExpeditionBill && x.Query.Admissible)
                    && beforeQuery.SequenceEqual(Bytes(run)), "Ledger preview requires no property grant and must be read-only: " + draft.Code);
                Require(run.Execute(bookkeeper, start).Outcome == Outcome.Committed, "Authorized representative could not book independent work.");
                var open = BillJob(run);
                Require(open.Basis.AccountingCutoff == before.RuleClock && open.Basis.CutoffRevision == before.Revision
                    && open.Basis.MealPaymentRevision == purchase.Revision && open.Basis.SalePaymentRevision == sale.UpdatedRevision
                    && run.Capture().Work.Reservations.All(x => x.JobId != open.Id), "Bill admission froze the wrong basis or reserved physical assets.");
                WorldAdvance(run, 1, 2);
                SaveBill(run, BillPolicy(), directory, "mgt10-expedition-bill-active");
                var forgedBooking = run.Capture();
                forgedBooking.Work = new WorkLedger(forgedBooking.Work.Lots, forgedBooking.Work.WorkerIntervals.Select(x =>
                    x.JobId == open.Id ? new WorkerInterval(x.Id, x.JobId, x.WorkerId, x.Start, x.End.AddSeconds(1)) : x),
                    forgedBooking.Work.Reservations);
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(forgedBooking));
                SaleCommit(run, BillCommand(run, CommandKind.PauseExpeditionBill, open.Id));
                WorldAdvance(run, 13, 2);
                Require(BillJob(run).Work.Labor == T(1, 2), "A positive paused gap earned labor.");
                var replay = SaveBill(run, BillPolicy(), directory, "mgt10-expedition-bill-paused");
                var audit = new List<string> {
                    "event\tstatus\tcutoffTime\tcutoffRevision\tobservedTime\tobservedRevision\tsaleId\tsaleRevision\tmealId\tmealRevision\tgrossCp\tdirectTaxCp\tmandatoryRescueQuarantineCp\tbaseCp\tselfRate\tshareCp\tnetExpeditionCp\tmealCp\taccountedCashChangeCp\tgrossTargetCp\tgrossMet\tnetTargetCp\tnetMet\tprofitTargetCp\tprofitComparison\tcreditedSeconds\ttenderLot\ttenderOwner\ttenderCount\trepresentativeTenderCount"
                };
                audit.Add(BillAudit("paused", run.Capture()));
                foreach (var branch in new[] { run, replay }) {
                    SaleCommit(branch, BillCommand(branch, CommandKind.ResumeExpeditionBill, open.Id));
                    WorldAdvance(branch, 1799);
                    Require(BillJob(branch).Work.Labor == T(3599, 2) && BillJob(branch).Report == null,
                        "A report was issued before 1,800 active seconds.");
                    var complete = IC(branch, CommandKind.AdvanceClock, x: 1, y: 2);
                    SaleCommit(branch, complete);
                    var result = branch.Capture();
                    var bill = BillJob(branch);
                    Require(bill.Status == ExpeditionBillStatus.Reconciled && bill.Work.Labor == T(1800)
                        && bill.Basis.GrossSaleCopper == 2 && bill.Basis.DirectTaxCopper == 0
                        && bill.Basis.MandatoryRescueQuarantineCopper == 0 && bill.Basis.SponsorBaseCopper == 2
                        && bill.Basis.SponsorShareCopper == 0 && bill.Basis.NetExpeditionCopper == 2
                        && bill.Basis.MealExpenseCopper == 2 && bill.Basis.AccountedCashChangeCopper == 0
                        && bill.Basis.GrossTargetMet(charter) && !bill.Basis.NetTargetMet(charter)
                        && bill.Basis.TrueProfitAfterReservesCopper == null && bill.Report.PhysicalCount == new RuleQuantity(2)
                        && bill.Report.OwnerId == SaleBuyer && bill.Report.RepresentativeOwnedCount(charter) == default,
                        "The exact settlement basis, independent targets, or actual tender observation changed.");
                    var expectedEnd = RuleTime.FromFraction(before.RuleClock.Numerator * 2 + 3613 * before.RuleClock.Denominator,
                        before.RuleClock.Denominator * 2);
                    Require(bill.UpdatedAt == expectedEnd, "The report occurred at " + bill.UpdatedAt + " instead of " + expectedEnd + ".");
                    Require(result.RandomState == before.RandomState, "No-roll bookkeeping changed shared RNG.");
                    Require(result.Work.Reservations.Count == before.Work.Reservations.Count, "Bookkeeping created a physical reservation.");
                    Require(result.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))
                            .SequenceEqual(before.Work.Lots.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId)))
                        && result.InventoryLots.OrderBy(x => x.LotId, StringComparer.Ordinal).Select(x => (x.LotId, x.OwnerId))
                            .SequenceEqual(before.InventoryLots.OrderBy(x => x.LotId, StringComparer.Ordinal).Select(x => (x.LotId, x.OwnerId))),
                        "Bookkeeping changed stock, physical location, custody or title.");
                    Require(result.HavenSales.Single().UpdatedRevision == sale.UpdatedRevision
                        && result.HavenMealPurchases.Single().Revision == purchase.Revision
                        && result.CharacterAdvancements.SequenceEqual(before.CharacterAdvancements)
                        && result.CharacterMilestones.SequenceEqual(before.CharacterMilestones), "Bookkeeping rewrote a payment or granted advancement.");
                    Require(branch.Execute(host, complete).Outcome == Outcome.Duplicate, "Identical clock replay produced a second report.");
                    Require(branch.Execute(bookkeeper, start).Outcome == Outcome.Duplicate, "Identical admission did not retain its receipt.");
                    RejectUnchanged(branch, host, new Command(start.Id, start.Actor, start.ExpectedRevision, start.Kind, "changed"), "CommandIdConflict");
                    RejectUnchanged(branch, host, BillCommand(branch), "ExpeditionBillAlreadyReconciled");
                    WorldStep(branch, 1, 0, actor: SaleSeller);
                    WorldAdvance(branch, 2);
                    Require(ReferenceEquals(BillJob(branch), bill), "Ordinary onward travel rewrote the historical report.");
                }
                Require(Bytes(run).SequenceEqual(Bytes(replay)), "The same resume, boundary and onward commands replayed differently.");
                RequireSaleAsset(run.Capture(), SaleTender, SaleBuyer, new RuleQuantity(2));
                SaveBill(run, BillPolicy(), directory, "mgt10-expedition-bill-complete");
                Throws<ArgumentException>(() => new Simulation(MealPolicy(), run.Capture(), ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(BillPolicy(new TestOnlyExpeditionBillProfile(dueAt: 14399)), run.Capture(), ExecutionProfile.Laboratory));
                audit.Add(BillAudit("reconciled-and-continued", run.Capture()));
                File.WriteAllLines(Path.Combine(directory, "expedition-bill-audit.tsv"), audit);
            });
            cases.Add("mgt10_expedition_bill_requires_charter_scope_paid_inputs_and_eligible_worker", () =>
            {
                var fresh = PortableWorld(BillPolicy());
                RejectUnchanged(fresh, host, BillCommand(fresh), "ExpeditionBillPaidRecordsMissing");
                var cancelledPurchase = MealAtCounter(BillPolicy());
                RejectUnchanged(cancelledPurchase, host, BillCommand(cancelledPurchase), "ExpeditionBillPaidRecordsMissing");
                SaleCommit(cancelledPurchase, PurchaseMeal(cancelledPurchase));
                EatMeal(cancelledPurchase, new RuleQuantity(2, 3));
                Require(!cancelledPurchase.QueryCommand(host, BillCommand(cancelledPurchase)).Admissible,
                    "A worker eating the meal was allowed to take an incompatible ledger booking.");
                RejectUnchanged(cancelledPurchase, host, BillCommand(cancelledPurchase, actor: TestOnlyPolicy.ActorId),
                    "ExpeditionBillRepresentativeUnauthorized");
                RejectUnchanged(cancelledPurchase, host, BillCommand(cancelledPurchase, target: "different-charter-bill"),
                    "ExpeditionBillVersionUnknown");
                foreach (var entry in new[] {
                    (new TestOnlyExpeditionBillProfile(representativeAuthorized: false), "ExpeditionBillRepresentativeUnauthorized"),
                    (new TestOnlyExpeditionBillProfile(recordsAccessible: false), "ExpeditionBillRecordsUnavailable"),
                    (new TestOnlyExpeditionBillProfile(coverage: ExpeditionBillCoverage.Required
                        & ~ExpeditionBillCoverage.NoMandatoryRescueOrQuarantineExpense), "ExpeditionBillScopeIncomplete"),
                    (new TestOnlyExpeditionBillProfile(coverage: ExpeditionBillCoverage.Required
                        & ~ExpeditionBillCoverage.CompleteSaleRegister), "ExpeditionBillScopeIncomplete"),
                    (new TestOnlyExpeditionBillProfile(coverage: ExpeditionBillCoverage.Required
                        & ~ExpeditionBillCoverage.NoConflictingSuperiorClaim), "ExpeditionBillSuperiorClaimUncleared"),
                    (new TestOnlyExpeditionBillProfile(writingFacilitiesAvailable: false), "ExpeditionBillDeskUnavailable")
                }) {
                    var run = BillAtDesk(BillPolicy(entry.Item1));
                    RejectUnchanged(run, host, BillCommand(run), entry.Item2);
                    var preview = run.QueryCommand(host, BillCommand(run));
                    Require(preview.Supported && !preview.Admissible && preview.Code == entry.Item2 && preview.ExpeditionBillDraft == null,
                        "A missing authority or incomplete register exposed an eligible draft.");
                }
            });
            cases.Add("mgt10_expedition_bill_cancellation_keeps_history_and_new_attempt_earns_own_work", () =>
            {
                var run = BillAtDesk();
                SaleCommit(run, BillCommand(run));
                WorldAdvance(run, 1, 2);
                var first = BillJob(run);
                SaleCommit(run, BillCommand(run, CommandKind.CancelExpeditionBill, first.Id));
                var cancelled = BillJob(run);
                Require(cancelled.Status == ExpeditionBillStatus.Cancelled && cancelled.Work.Labor == T(1, 2)
                    && run.Capture().Work.WorkerIntervals.All(x => x.JobId != cancelled.Id || x.End <= cancelled.UpdatedAt),
                    "Cancellation did not retain earned work and truncate its booking.");
                RejectUnchanged(run, host, BillCommand(run, CommandKind.ResumeExpeditionBill, first.Id), "ExpeditionBillWorkNotOpen");
                WorldAdvance(run, 6);
                SaleCommit(run, BillCommand(run));
                Require(BillJob(run).Id != first.Id && BillJob(run).Work.Labor == default && run.Capture().ExpeditionBills.Length == 2,
                    "A fresh attempt imported the cancelled attempt's time.");
                WorldAdvance(run, 1800);
                Require(BillJob(run).Status == ExpeditionBillStatus.Reconciled, "The independent attempt did not reconcile.");
            });
            cases.Add("mgt10_expedition_bill_station_result_one_cleanup_and_result_five", () =>
            {
                var at = BillAtDesk().Capture().RuleClock.AddSeconds(300);
                var profile = new TestOnlyExpeditionBillProfile(authorizationUntil: 15000);
                foreach (int result in new[] { 1, 5 }) {
                    var incident = new CraftingMishapFact("bill-desk-incident", result, at: at, stationId: TestOnlyExpeditionBillProfile.DeskId);
                    var run = BillAtDesk(BillPolicy(profile, incident: incident));
                    SaleCommit(run, BillCommand(run));
                    WorldAdvance(run, 300);
                    CraftEvent(run, incident.Id);
                    var job = BillJob(run);
                    if (result == 5) {
                        Require(job.Status == ExpeditionBillStatus.Working, "A crafting-order restriction blocked ledger work.");
                        WorldAdvance(run, 1500);
                    } else {
                        Require(job.Status == ExpeditionBillStatus.Paused && job.Reason == "ExpeditionBillDeskUseBlocked"
                            && job.Work.Labor == T(300)
                            && run.Capture().Work.WorkerIntervals.All(x => x.JobId != job.Id || x.End <= at),
                            "Actual station restriction did not stop ledger work at its application time.");
                        RejectUnchanged(run, host, BillCommand(run, CommandKind.ResumeExpeditionBill, job.Id), "ExpeditionBillDeskUseBlocked");
                        Remedy(run, incident.Id);
                        WorldAdvance(run, 3606);
                        Require(BillJob(run).Status == ExpeditionBillStatus.Paused && BillJob(run).Work.Labor == T(300),
                            "Cleanup automatically resumed bookkeeping.");
                        SaleCommit(run, BillCommand(run, CommandKind.ResumeExpeditionBill, job.Id));
                        WorldAdvance(run, 1500);
                    }
                    Require(BillJob(run).Status == ExpeditionBillStatus.Reconciled, "Eligible ledger work did not finish.");
                }
            });
            cases.Add("mgt10_expedition_bill_condition_interrupt_alternate_clock_and_tactical_entry", () =>
            {
                var at = BillAtDesk().Capture().RuleClock.AddSeconds(300);
                var conditions = new ConditionCombatFixture(CCApply("bill-stun", "Stunned", SaleSeller, at: new ConditionStamp(at)),
                    new ConditionFixtureEvent(SaleSeller, ConditionOperation.Cure("event.bill-cure", new ConditionStamp(at.AddSeconds(6)), "Stunned")));
                var run = BillAtDesk(BillPolicy(conditions: conditions));
                SaleCommit(run, BillCommand(run));
                var before = run.Capture().RuleClock;
                PortableCommit(run, Portable(run, CommandKind.HandlePortableEquipment, PortableKitFixture.Tools, handling: HandlingKind.Retrieve));
                Require(run.Capture().RuleClock == before.AddSeconds(1) && BillJob(run).Work.Labor == T(1),
                    "A different actor's admitted handling failed to credit one shared second.");
                WorldAdvance(run, 299);
                SaleCommit(run, CCCommand(run, "bill-stun", SaleSeller));
                var job = BillJob(run);
                Require(job.Status == ExpeditionBillStatus.Paused && job.Reason == "ExpeditionBillWorkerIncapable"
                    && job.Work.Labor == T(300), "Condition dispatch did not truncate actual work at the event time.");
                RejectUnchanged(run, host, BillCommand(run, CommandKind.ResumeExpeditionBill, job.Id), "ExpeditionBillWorkerIncapable");
                WorldAdvance(run, 6);
                SaleCommit(run, CCCommand(run, "bill-cure", SaleSeller));
                SaleCommit(run, BillCommand(run, CommandKind.ResumeExpeditionBill, job.Id));
                WorldStep(run, 1, 0);
                WorldAdvance(run, 2);
                WorldStep(run, 1, 0);
                WorldAdvance(run, 2);
                WorldStep(run, 1, 0);
                Require(run.Capture().InventoryCombat && BillJob(run).Status == ExpeditionBillStatus.Paused
                    && BillJob(run).Work.Labor == T(304) && BillJob(run).Reason == "ExpeditionBillCombatUnavailable",
                    "Tactical entry did not pause the ledger worker at the shared clock boundary.");
            });
            cases.Add("mgt10_expedition_bill_full_labor_pending_and_half_open_expiry", () =>
            {
                var arrival = BillAtDesk().Capture().RuleClock;
                int endpoint = checked((int)arrival.Numerator + 1800);
                Require(arrival.Denominator == 1, "Deadline scenario requires a whole-second arrival.");
                var tie = BillAtDesk(BillPolicy(new TestOnlyExpeditionBillProfile(authorizationUntil: endpoint)));
                RejectUnchanged(tie, host, BillCommand(tie), "ExpeditionBillAuthorizationWindow");

                var profile = new TestOnlyExpeditionBillProfile(authorizationUntil: endpoint + 1);
                var paused = BillAtDesk(BillPolicy(profile));
                SaleCommit(paused, BillCommand(paused));
                WorldAdvance(paused, 1, 2);
                SaleCommit(paused, BillCommand(paused, CommandKind.PauseExpeditionBill, BillJob(paused).Id));
                WorldAdvance(paused, 1);
                RejectUnchanged(paused, host, BillCommand(paused, CommandKind.ResumeExpeditionBill, BillJob(paused).Id),
                    "ExpeditionBillAuthorizationWindow");
                WorldAdvance(paused, 3599, 2);
                Require(BillJob(paused).Status == ExpeditionBillStatus.Expired && BillJob(paused).UpdatedAt == T(endpoint + 1)
                    && BillJob(paused).Work.Labor == T(1, 2) && BillJob(paused).Report == null, "Paused authorization failed to expire exactly.");

                var conditions = BillEndpointConditions(T(endpoint));
                var pending = PortableWorld(BillPolicy(profile, conditions));
                SaleCommit(pending, CCCommand(pending, "bill-endpoint-stun", SaleSeller));
                SaleCommit(pending, CCCommand(pending, "bill-ward", SaleSeller));
                EarnMealTender(pending);
                BuyAndEatBillMeal(pending);
                SaleCommit(pending, BillCommand(pending));
                WorldAdvance(pending, 1800);
                var job = BillJob(pending);
                Require(job.Status == ExpeditionBillStatus.PendingCompletion && job.Work.Labor == T(1800)
                    && job.UpdatedAt == T(endpoint) && job.Report == null
                    && pending.Capture().Work.WorkerIntervals.All(x => x.JobId != job.Id || x.End <= job.UpdatedAt),
                    "Endpoint condition did not retain fully earned, unbooked work: " + job.Status + " " + job.UpdatedAt + " " + job.Reason);
                var restored = SaveBill(pending, BillPolicy(profile, conditions), directory, "mgt10-expedition-bill-pending");
                WorldAdvance(pending, 1);
                Require(BillJob(pending).Status == ExpeditionBillStatus.Expired && BillJob(pending).UpdatedAt == T(endpoint + 1)
                    && BillJob(pending).Work.Labor == T(1800) && BillJob(pending).Report == null, "Pending work settled at exact authority expiry.");
                RejectUnchanged(restored, host, BillCommand(restored, CommandKind.FinalizeExpeditionBill, job.Id), "ExpeditionBillWorkerIncapable");
                SaleCommit(restored, CCCommand(restored, "bill-endpoint-cure", SaleSeller));
                Require(BillJob(restored).Status == ExpeditionBillStatus.PendingCompletion, "Cure automatically issued the report.");
                var cured = restored.Capture();
                SaleCommit(restored, BillCommand(restored, CommandKind.FinalizeExpeditionBill, job.Id));
                Require(BillJob(restored).Report != null && restored.Capture().RuleClock == cured.RuleClock
                    && restored.Capture().RandomState == cured.RandomState, "Explicit finalization changed elapsed time or RNG.");
            });
            cases.Add("mgt10_expedition_bill_legacy_pending_finalize_busy_retains_domain_code", () =>
            {
                var baseline = MealAtCounter(BillPolicy());
                SaleCommit(baseline, PurchaseMeal(baseline));
                var endpoint = baseline.Capture().RuleClock.AddSeconds(1800);
                var pending = PortableWorld(BillPolicy(conditions: BillEndpointConditions(endpoint)));
                SaleCommit(pending, CCCommand(pending, "bill-endpoint-stun", SaleSeller));
                SaleCommit(pending, CCCommand(pending, "bill-ward", SaleSeller));
                EarnMealTender(pending);
                SaleCommit(pending, PurchaseMeal(pending));
                SaleCommit(pending, BillCommand(pending));
                WorldAdvance(pending, 1800);
                var bill = BillJob(pending);
                Require(pending.Capture().SchemaVersion == Snapshot.ExpeditionBillSchema
                    && bill.Status == ExpeditionBillStatus.PendingCompletion && bill.UpdatedAt == endpoint
                    && bill.Work.Labor == T(1800) && bill.Report == null,
                    "The original bill profile did not reach its fully earned pending endpoint.");
                SaleCommit(pending, CCCommand(pending, "bill-endpoint-cure", SaleSeller));
                WorldAdvance(pending, 6);
                EatMeal(pending, new RuleQuantity(2, 3));
                Require(pending.Capture().Intakes.Single().Status == IntakeStatus.Working,
                    "The representative was not actually eating the purchased meal.");
                var finalize = BillCommand(pending, CommandKind.FinalizeExpeditionBill, bill.Id);
                byte[] before = Bytes(pending);
                var query = pending.QueryCommand(host, finalize);
                Require(query.Supported && !query.Admissible && query.Code == "ExpeditionBillWorkerBusy"
                    && before.SequenceEqual(Bytes(pending)),
                    "Schema81 busy finalization query changed its code or state: " + query.Code);
                RejectUnchanged(pending, host, finalize, "ExpeditionBillWorkerBusy");
            });
            cases.Add("mgt10_expedition_bill_rejects_forged_totals_charter_receipts_and_preserves_asof", () =>
            {
                var profile = new TestOnlyExpeditionBillProfile(authorizationUntil: 30000);
                var run = BillAtDesk(BillPolicy(profile));
                WorldAdvance(run, 18001);
                Require(run.Capture().RuleClock > run.Capture().HavenMealPurchases.Single().Offer.ExpiresAt
                    && run.Capture().RuleClock > run.Capture().HavenSales.Single().Basis.ExpiresAt
                    && run.Capture().RuleClock > profile.Charter.DueAt,
                    "This control requires old offers and the distinct charter due date to have passed.");
                SaleCommit(run, Portable(run, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Drop, actor: SaleBuyer));
                SaleCommit(run, BillCommand(run));
                WorldAdvance(run, 1800);
                var complete = run.Capture();
                var job = BillJob(run);
                var b = job.Basis;
                var codec = new SnapshotCodec();
                foreach (var altered in new[] {
                    new ExpeditionBillBasis(b.CharterVersionId, b.BillVersionId, b.SaleId, b.SalePaymentRevision, b.MealId,
                        b.MealPaymentRevision, b.AppraisalId, b.ClearanceId, b.ExemptionId, b.SpendingAuthorityId, b.TenderLotId,
                        b.CutoffRevision, b.AccountingCutoff, 3, 3),
                    new ExpeditionBillBasis(b.CharterVersionId, b.BillVersionId, b.SaleId, b.SalePaymentRevision, "unrelated-payment",
                        b.MealPaymentRevision, b.AppraisalId, b.ClearanceId, b.ExemptionId, b.SpendingAuthorityId, b.TenderLotId,
                        b.CutoffRevision, b.AccountingCutoff, b.GrossSaleCopper, b.MealExpenseCopper),
                    new ExpeditionBillBasis(b.CharterVersionId, b.BillVersionId, b.SaleId, b.SalePaymentRevision, b.MealId,
                        b.MealPaymentRevision, b.AppraisalId, b.ClearanceId, "contradictory-exemption", b.SpendingAuthorityId, b.TenderLotId,
                        b.CutoffRevision, b.AccountingCutoff, b.GrossSaleCopper, b.MealExpenseCopper)
                }) {
                    var forged = complete.Copy();
                    forged.ExpeditionBills[0] = new ExpeditionBillRecord(job.Id, job.WorkerId, altered, job.StartRevision,
                        job.UpdatedRevision, job.UpdatedAt, job.Work.Labor, job.Status, job.Reason, job.Report);
                    Throws<ArgumentException>(() => codec.Encode(forged));
                }
                Throws<ArgumentException>(() => new ExpeditionBillBasis(b.CharterVersionId, b.BillVersionId, b.SaleId,
                    b.SalePaymentRevision, b.SaleId, b.MealPaymentRevision, b.AppraisalId, b.ClearanceId, b.ExemptionId,
                    b.SpendingAuthorityId, b.TenderLotId, b.CutoffRevision, b.AccountingCutoff, b.GrossSaleCopper, b.MealExpenseCopper));
                var omitted = complete.Copy();
                omitted.HavenMealPurchases = Array.Empty<HavenMealPurchaseRecord>();
                Throws<ArgumentException>(() => codec.Encode(omitted));
                var substituted = complete.Copy();
                substituted.ExpeditionBillCharter = new TestOnlyExpeditionBillProfile(authorizationUntil: 30000, dueAt: 16000).Charter;
                Throws<ArgumentException>(() => new Simulation(BillPolicy(profile), codec.Decode(codec.Encode(substituted)), ExecutionProfile.Laboratory));
                var forgedTitle = complete.Copy();
                forgedTitle.ExpeditionBills[0] = job.With(forgedTitle, job.Work.Labor, job.Status, job.Reason,
                    new ExpeditionBillTenderObservation(SaleSeller, new RuleQuantity(2)));
                Throws<ArgumentException>(() => codec.Encode(forgedTitle));
                SaleCommit(run, Portable(run, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Pickup, actor: SaleBuyer));
                Require(BillJob(run).Report == job.Report && BillJob(run).UpdatedRevision == job.UpdatedRevision
                    && run.Capture().InventoryLots.Single(x => x.LotId == SaleTender).OwnerId == SaleBuyer,
                    "Later lawful coin handling rewrote a historical observation or payment.");
            });
        }

        private static ConditionCombatFixture BillEndpointConditions(RuleTime endpoint)
            => new ConditionCombatFixture(CCGrant("bill-ward", SaleSeller, new ConditionStamp(endpoint), "Stunned"),
                CCApply("bill-endpoint-stun", "Stunned", SaleSeller),
                new ConditionFixtureEvent(SaleSeller, ConditionOperation.Cure("event.bill-endpoint-cure", new ConditionStamp(endpoint), "Stunned")));

        private static string BillAudit(string name, Snapshot state)
        {
            var job = state.ExpeditionBills.Last();
            var b = job.Basis;
            var c = state.ExpeditionBillCharter;
            return string.Join("\t", name, job.Status, b.AccountingCutoff, b.CutoffRevision, job.Report == null ? "pending" : job.UpdatedAt.ToString(),
                job.Report == null ? "pending" : job.UpdatedRevision.ToString(), b.SaleId, b.SalePaymentRevision, b.MealId, b.MealPaymentRevision,
                b.GrossSaleCopper, b.DirectTaxCopper, b.MandatoryRescueQuarantineCopper, b.SponsorBaseCopper, c.SelfShareRate,
                b.SponsorShareCopper, b.NetExpeditionCopper, b.MealExpenseCopper, b.AccountedCashChangeCopper,
                c.GrossTargetCopper, b.GrossTargetMet(c), c.NetTargetCopper, b.NetTargetMet(c), c.ProfitAfterReservesTargetCopper,
                "unresolved-costs-and-reserve-basis", job.Work.Labor, b.TenderLotId, job.Report?.OwnerId ?? "unobserved",
                job.Report?.PhysicalCount.ToString() ?? "unobserved", job.Report?.RepresentativeOwnedCount(c).ToString() ?? "unobserved");
        }
    }
}
#endif
