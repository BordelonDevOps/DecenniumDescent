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
        private const string SaleBuyer = TestOnlyHavenSaleProfile.BuyerId;
        private const string SaleSeller = TestOnlyHavenSaleProfile.SellerId;
        private const string SaleOffer = TestOnlyHavenSaleProfile.OfferVersionId;
        private const string SaleTender = TestOnlyHavenSaleProfile.TenderLotId;

        private static Authority HavenSaleHost()
        {
            string[] actors = { TestOnlyPolicy.ActorId, SaleSeller, SaleBuyer, AdditionalTacticalActor.Id };
            return new Authority("TEST_ONLY.host", actors, true, true, actors, actors);
        }

        private static TestOnlySharedWorldPolicy SalePolicy(TestOnlyHavenSaleProfile profile = null,
            ConditionCombatFixture conditions = null, CraftingMishapFact incident = null)
            => AppraisalPolicy(conditions: conditions, incident: incident).EnableHavenSale(profile ?? new TestOnlyHavenSaleProfile());

        private static Command SaleCommand(Simulation s, CommandKind kind, string target = SaleOffer, string actor = SaleSeller)
            => MiningCommand(s, kind, target, actor: actor);

        private static void SaleCommit(Simulation s, Command command)
        {
            var result = s.Execute(HavenSaleHost(), command);
            Require(result.Outcome == Outcome.Committed, command.Kind + " rejected: " + result.Code);
        }

        private static void PresentSaleIron(Simulation s, bool withEncounter = false)
        {
            if (withEncounter) ResolveAppraisalExpeditionEncounter(s);
            ExtractAppraisalIron(s);
            PlaceIronAtAppraisalDesk(s);
            MiningCommit(s, AppraisalCommand(s, CommandKind.StartHavenAppraisal));
            WorldAdvance(s, 1800);
            Require(s.Capture().HavenAppraisals.Single().ResultCopper == new RuleQuantity(15, 2),
                "The physical subject did not receive its independent historical appraisal.");
            PortableCommit(s, AppraisalHandling(s, HandlingKind.Pickup));
            WorldAdvance(s, 6);
        }

        private static Simulation SaleAtCounter(TestOnlySharedWorldPolicy policy = null, bool withEncounter = false)
        {
            var s = PortableWorld(policy ?? SalePolicy());
            PresentSaleIron(s, withEncounter);
            return s;
        }

        private static void RequireSaleAsset(Snapshot s, string id, string owner, RuleQuantity amount)
        {
            var stock = s.Work.Lots.Single(x => x.Id == id);
            var item = s.PortableEquipment.Single(x => x.Id == id);
            Require(stock.Amount == amount && stock.CustodianId == owner && stock.LocationId == owner
                && s.InventoryLots.Single(x => x.LotId == id).OwnerId == owner
                && item.OwnerId == owner && item.CustodianId == owner && item.LinkedId == id
                && item.Placement == PortablePlacement.Carried && item.ParentId == "",
                "The whole physical lot, title, or linked custody disagrees after disposition.");
        }

        private static void AddHavenSaleCases(Dictionary<string, Action> cases, string directory)
        {
            var host = HavenSaleHost();
            cases.Add("mgt10_haven_sale_connected_joint_work_pause_restore_pay_and_continue", () =>
            {
                var s = SaleAtCounter(withEncounter: true);
                var before = s.Capture();
                Require(before.SchemaVersion == Snapshot.HavenSaleSchema
                    && !before.WorldSchedule.Order.Contains(SaleBuyer) && !before.Encounter.Order.Contains(SaleBuyer)
                    && !before.Clubs.Any(x => x.OwnerId == SaleBuyer), "The authored buyer gained tactical membership or a weapon.");
                RequireSaleAsset(before, AppraisalIron, SaleSeller, new RuleQuantity(1));
                RequireSaleAsset(before, SaleTender, SaleBuyer, new RuleQuantity(2));
                var start = SaleCommand(s, CommandKind.StartHavenSale);
                var initial = Bytes(s);
                var query = s.QueryCommand(host, start);
                Require(query.Supported && query.Admissible && query.HavenSaleOffer?.ExactQuoteCopper == new RuleQuantity(7, 3)
                    && query.HavenSaleOffer.TenderCount == 2
                    && s.DiscoverCommands(host, SaleSeller).Any(x => x.Command.Kind == CommandKind.StartHavenSale && x.Query.Admissible)
                    && initial.SequenceEqual(Bytes(s)),
                    "Query failed to expose admission or touched stock.");
                var declined = new Simulation(SalePolicy(), before, ExecutionProfile.Laboratory);
                WorldStep(declined, 1, 0, actor: SaleSeller);
                WorldAdvance(declined, 2);
                Require(declined.Capture().HavenSales.Length == 0, "Leaving the counter without acceptance sold the iron.");
                RequireSaleAsset(declined.Capture(), AppraisalIron, SaleSeller, new RuleQuantity(1));
                WorldAdvance(s, 6);
                Require(s.Capture().HavenSales.Length == 0, "Ignoring the offer generated a transaction.");
                RequireSaleAsset(s.Capture(), AppraisalIron, SaleSeller, new RuleQuantity(1));
                start = SaleCommand(s, CommandKind.StartHavenSale);
                SaleCommit(s, start);
                var open = s.Capture().HavenSales.Single();
                Require(open.Basis.ExactQuoteCopper == new RuleQuantity(7, 3) && !open.PaymentCopper.HasValue
                    && s.Capture().Work.WorkerIntervals.Count(x => x.JobId == open.Id) == 2,
                    "Admission paid or failed to book the pair under the exact quote.");
                WorldAdvance(s, 1, 2);
                string activePath = Path.Combine(directory, "mgt10-haven-sale-active.ddsave");
                new FileSaveStore().Save(activePath, s.Capture());
                Require(Bytes(new Simulation(SalePolicy(), new FileSaveStore().Load(activePath), ExecutionProfile.Laboratory))
                    .SequenceEqual(Bytes(s)), "Active paired work did not survive restoration.");
                SaleCommit(s, SaleCommand(s, CommandKind.PauseHavenSale, open.Id));
                WorldAdvance(s, 6);
                var paused = s.Capture();
                Require(paused.HavenSales.Single().Work.Labor == T(1, 2)
                    && paused.Work.AvailableAmount(AppraisalIron) == default && paused.Work.AvailableAmount(SaleTender) == default,
                    "Joint pause lost labor or either physical claim.");
                string path = Path.Combine(directory, "mgt10-haven-sale-paused.ddsave");
                new FileSaveStore().Save(path, paused);
                var replay = new Simulation(SalePolicy(), new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(replay)), "Paused paired work failed exact restore.");
                var audit = new List<string> {
                    "event\tclock\trevision\tjob\tstatus\twork\tappraisalCopper\texactQuoteCopper\tpaidCopper\tgoods\tgoodsAmount\tgoodsOwner\tgoodsCustodian\ttender\ttenderCount\ttenderOwner\ttenderCustodian\tcoinMassPounds\tbuyerBurdenPounds\tsellerBurdenPounds"
                };
                audit.Add(SaleAuditRow("paused", paused));
                foreach (var run in new[] { s, replay }) {
                    SaleCommit(run, SaleCommand(run, CommandKind.ResumeHavenSale, open.Id));
                    WorldAdvance(run, 1799);
                    var almost = run.Capture();
                    Require(almost.HavenSales.Single().Work.Labor == T(3599, 2)
                        && !almost.HavenSales.Single().PaymentCopper.HasValue, "A sale was paid before completing 1,800 joint seconds.");
                    RequireSaleAsset(almost, AppraisalIron, SaleSeller, new RuleQuantity(1));
                    RequireSaleAsset(almost, SaleTender, SaleBuyer, new RuleQuantity(2));
                    var pay = IC(run, CommandKind.AdvanceClock, x: 1, y: 2);
                    WorldCommit(run, pay);
                    var paid = run.Capture();
                    var receipt = paid.HavenSales.Single();
                    Require(receipt.Status == HavenSaleStatus.Paid && receipt.Work.Labor == T(1800)
                        && receipt.PaymentCopper == 2 && paid.RandomState == before.RandomState
                        && paid.HavenAppraisals.Single().ResultCopper == new RuleQuantity(15, 2)
                        && paid.CharacterAdvancements.Length == before.CharacterAdvancements.Length,
                        "Endpoint settlement changed appraisal, advancement, RNG or final sale payment.");
                    RequireSaleAsset(paid, AppraisalIron, SaleBuyer, new RuleQuantity(1));
                    RequireSaleAsset(paid, SaleTender, SaleSeller, new RuleQuantity(2));
                    Require(PortableEquipmentValidation.Mass(paid, paid.PortableEquipment.Single(x => x.Id == SaleTender)) == new RuleQuantity(1, 25)
                        && PortableEquipmentRules.CarriedBurden(paid, SaleBuyer).Pounds == new RuleQuantity(1),
                        "The tender mass or buyer's final burden was counted incorrectly.");
                    Require(paid.Work.Reservations.Where(x => x.JobId == open.Id).All(x => x.ConsumedAmount == default && x.ReleasedAmount == x.Amount),
                        "One of the two actual assets was consumed or remained claimed.");
                    if (run == s) {
                        audit.Add(SaleAuditRow("paid", paid));
                        string paidPath = Path.Combine(directory, "mgt10-haven-sale-paid.ddsave");
                        new FileSaveStore().Save(paidPath, paid);
                        Require(Bytes(new Simulation(SalePolicy(), new FileSaveStore().Load(paidPath), ExecutionProfile.Laboratory))
                            .SequenceEqual(Bytes(run)), "Paid state could not be restored exactly.");
                        Throws<ArgumentException>(() => new Simulation(AppraisalPolicy(), paid, ExecutionProfile.Laboratory));
                    }
                    Require(run.Execute(host, pay).Outcome == Outcome.Duplicate, "Duplicate clock committed a second payment.");
                    Require(run.Execute(host, start).Outcome == Outcome.Duplicate, "Recorded party grants lost the admitted receipt after title transfer.");
                    RejectUnchanged(run, host, SaleCommand(run, CommandKind.StartHavenSale), "HavenSaleAlreadyPaid");
                    RejectUnchanged(run, host, SaleCommand(run, CommandKind.CancelHavenSale, open.Id), "HavenSaleAgreementNotOpen");
                    WorldAdvance(run, 6);
                    SaleCommit(run, Portable(run, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Drop, actor: SaleSeller));
                    WorldStep(run, 1, 0, actor: SaleSeller);
                    WorldAdvance(run, 2);
                    Require(run.Capture().HavenSales.Single().PaymentCopper == 2 && run.Capture().HavenAppraisals.Single().ResultCopper == new RuleQuantity(15, 2),
                        "Post-sale handling altered the historical payment or appraisal.");
                    var continued = Bytes(run);
                    Require(run.Execute(host, pay).Outcome == Outcome.Duplicate && continued.SequenceEqual(Bytes(run)),
                        "A historical duplicate paid after later portable handling.");
                }
                Require(Bytes(s).SequenceEqual(Bytes(replay)), "Sale continuation differed after replay.");
                audit.Add(SaleAuditRow("continued", s.Capture()));
                File.WriteAllLines(Path.Combine(directory, "haven-sale-audit.tsv"), audit);
            });
            cases.Add("mgt10_haven_sale_admission_requires_consent_cleared_disposition_exemption_and_funds", () =>
            {
                foreach (var entry in new[] {
                    (new TestOnlyHavenSaleProfile(buyerConsented: false), "HavenSaleBuyerMandateMissing"),
                    (new TestOnlyHavenSaleProfile(dispositionCleared: false), "HavenSaleDispositionNotCleared"),
                    (new TestOnlyHavenSaleProfile(writtenExemption: false), "HavenSaleExemptionMissing"),
                    (new TestOnlyHavenSaleProfile(currencyAccepted: false), "HavenSaleTenderNotAccepted"),
                    (new TestOnlyHavenSaleProfile(openingCoins: 1), "HavenSaleTenderUnavailable") }) {
                    var s = SaleAtCounter(SalePolicy(entry.Item1));
                    var start = SaleCommand(s, CommandKind.StartHavenSale);
                    RejectUnchanged(s, host, start, entry.Item2);
                    var result = s.QueryCommand(host, start);
                    Require(result.Supported && !result.Admissible && result.Code == entry.Item2, "Quote query admitted invalid terms.");
                }
                var policy = SalePolicy();
                var sale = SaleAtCounter(policy);
                var sellerOnly = new Authority(host.Principal, new[] { SaleSeller }, inventoryOwners: new[] { SaleSeller });
                var command = SaleCommand(sale, CommandKind.StartHavenSale);
                RejectUnchanged(sale, sellerOnly, command, "InventoryNotAuthorized");
                Require(sale.QueryCommand(sellerOnly, command).Code == "InventoryNotAuthorized", "Seller control granted buyer property access.");
                RejectUnchanged(sale, host, SaleCommand(sale, CommandKind.StartHavenSale, TestOnlyHavenAppraisalProfile.ContextId),
                    "HavenSaleOfferUnknown");
                var reserved = sale.Capture();
                reserved.Work = reserved.Work.Reserve("existing-tender-hold", Array.Empty<WorkerInterval>(),
                    new[] { new ResourceReservation("existing-tender-claim", "existing-tender-hold", SaleTender, new RuleQuantity(1)) });
                Require(policy.QueryCommand(reserved, host, command).Code == "HavenSaleAssetReserved"
                    && policy.Resolve(reserved, command) == "HavenSaleAssetReserved" && reserved.HavenSales.Length == 0,
                    "An existing physical tender reservation allowed admission.");
                SaleCommit(sale, Portable(sale, CommandKind.HandlePortableEquipment, SaleTender, SaleSeller, HandlingKind.Handover, SaleBuyer));
                Require(sale.Capture().InventoryLots.Single(x => x.LotId == SaleTender).OwnerId == SaleBuyer,
                    "Ordinary pre-sale custody handover changed legal title.");
                RejectUnchanged(sale, host, SaleCommand(sale, CommandKind.StartHavenSale), "HavenSaleTenderUnavailable");
            });
            cases.Add("mgt10_haven_sale_paired_claims_block_handling_and_buyer_may_cancel", () =>
            {
                var s = SaleAtCounter();
                var start = SaleCommand(s, CommandKind.StartHavenSale);
                SaleCommit(s, start);
                var job = s.Capture().HavenSales.Single();
                var conflict = new Command(start.Id, start.Actor, start.ExpectedRevision, start.Kind, "different-offer");
                RejectUnchanged(s, host, conflict, "CommandIdConflict");
                WorldAdvance(s, 1, 2);
                SaleCommit(s, SaleCommand(s, CommandKind.PauseHavenSale, job.Id, SaleBuyer));
                WorldAdvance(s, 6);
                RejectUnchanged(s, host, AppraisalHandling(s, HandlingKind.Drop), "PortableItemHasPendingWork");
                RejectUnchanged(s, host, Portable(s, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Drop, actor: SaleBuyer),
                    "PortableItemHasPendingWork");
                var buyerControl = new Authority(host.Principal, new[] { SaleBuyer });
                var cancel = SaleCommand(s, CommandKind.CancelHavenSale, job.Id, SaleBuyer);
                Require(s.Execute(buyerControl, cancel).Outcome == Outcome.Committed, "The buyer could not withdraw its own mandate.");
                var stopped = s.Capture();
                var closed = stopped.HavenSales.Single();
                Require(closed.Status == HavenSaleStatus.Cancelled && closed.Work.Labor == T(1, 2) && !closed.PaymentCopper.HasValue
                    && stopped.Work.AvailableAmount(AppraisalIron) == new RuleQuantity(1)
                    && stopped.Work.AvailableAmount(SaleTender) == new RuleQuantity(2),
                    "Cancellation mutated or failed to release one of the original lots.");
                RequireSaleAsset(stopped, AppraisalIron, SaleSeller, new RuleQuantity(1));
                RequireSaleAsset(stopped, SaleTender, SaleBuyer, new RuleQuantity(2));
                SaleCommit(s, Portable(s, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Drop, actor: SaleBuyer));
                PortableCommit(s, AppraisalHandling(s, HandlingKind.Drop));
            });
            cases.Add("mgt10_haven_sale_pending_endpoint_delivery_capacity_is_atomic_and_restorable", () =>
            {
                var profile = new TestOnlyHavenSaleProfile(buyerBallast: true);
                var endpoint = SaleAtCounter().Capture().RuleClock.AddSeconds(1800);
                var conditions = BuyerEndpointConditions(endpoint);
                var s = PortableWorld(SalePolicy(profile, conditions));
                SaleCommit(s, CCCommand(s, "buyer-stun", SaleBuyer));
                SaleCommit(s, CCCommand(s, "buyer-ward", SaleBuyer));
                PresentSaleIron(s);
                SaleCommit(s, SaleCommand(s, CommandKind.StartHavenSale));
                WorldAdvance(s, 1800);
                var pending = s.Capture().HavenSales.Single();
                Require(pending.Status == HavenSaleStatus.PendingSettlement && pending.Work.Complete
                    && pending.UpdatedAt == endpoint && !pending.PaymentCopper.HasValue
                    && s.Capture().Work.WorkerIntervals.All(x => x.JobId != pending.Id || x.End <= endpoint),
                    "Endpoint incapacity failed to leave fully earned, unbooked, unpaid work.");
                string path = Path.Combine(directory, "mgt10-haven-sale-pending.ddsave");
                new FileSaveStore().Save(path, s.Capture());
                var replay = new Simulation(SalePolicy(profile, conditions), new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                Require(Bytes(replay).SequenceEqual(Bytes(s)), "Pending sale changed on disk restoration.");
                foreach (var run in new[] { s, replay }) {
                    RejectUnchanged(run, host, SaleCommand(run, CommandKind.FinalizeHavenSale, pending.Id), "HavenSaleParticipantIncapable");
                    SaleCommit(run, CCCommand(run, "buyer-cure", SaleBuyer));
                    Require(run.Capture().HavenSales.Single().Status == HavenSaleStatus.PendingSettlement,
                        "Curing the buyer automatically settled a pending sale.");
                    string ballast = TestOnlyHavenSaleProfile.BuyerBallastId;
                    SaleCommit(run, Portable(run, CommandKind.HandlePortableEquipment, ballast, actor: SaleBuyer));
                    RejectUnchanged(run, host, SaleCommand(run, CommandKind.FinalizeHavenSale, pending.Id), "CarryingCapacityExceeded");
                    RequireSaleAsset(run.Capture(), AppraisalIron, SaleSeller, new RuleQuantity(1));
                    RequireSaleAsset(run.Capture(), SaleTender, SaleBuyer, new RuleQuantity(2));
                    WorldAdvance(run, 6);
                    SaleCommit(run, Portable(run, CommandKind.HandlePortableEquipment, ballast, handling: HandlingKind.Drop, actor: SaleBuyer));
                    var before = run.Capture();
                    var finish = SaleCommand(run, CommandKind.FinalizeHavenSale, pending.Id);
                    SaleCommit(run, finish);
                    var paid = run.Capture();
                    Require(paid.RuleClock == before.RuleClock && paid.RandomState == before.RandomState
                        && paid.HavenSales.Single().PaymentCopper == 2, "Explicit finalization added labor, time or RNG.");
                    var sellerOnly = new Authority(host.Principal, new[] { SaleSeller }, inventoryOwners: new[] { SaleSeller });
                    RejectUnchanged(run, sellerOnly, finish, "InventoryNotAuthorized");
                    var terminal = Bytes(run);
                    Require(run.Execute(host, finish).Outcome == Outcome.Duplicate && terminal.SequenceEqual(Bytes(run)),
                        "The settled seller could not repeat the receipt idempotently with recorded party grants.");
                }
                Require(Bytes(s).SequenceEqual(Bytes(replay)), "Pending settlement continuation differed after restore.");
            });
            cases.Add("mgt10_haven_sale_each_participant_interrupts_paired_labor", () =>
            {
                var arrival = SaleAtCounter().Capture().RuleClock;
                var interruption = arrival.AddSeconds(300);
                foreach (string actor in new[] { SaleSeller, SaleBuyer }) {
                    var conditions = new ConditionCombatFixture(
                        CCApply("sale-stun", "Stunned", actor, at: new ConditionStamp(interruption)),
                        new ConditionFixtureEvent(actor, ConditionOperation.Cure("event.sale-cure",
                            new ConditionStamp(interruption.AddSeconds(6)), "Stunned")));
                    var s = SaleAtCounter(SalePolicy(conditions: conditions));
                    SaleCommit(s, SaleCommand(s, CommandKind.StartHavenSale));
                    WorldAdvance(s, 300);
                    SaleCommit(s, CCCommand(s, "sale-stun", actor));
                    var snapshot = s.Capture();
                    var job = snapshot.HavenSales.Single();
                    Require(job.Status == HavenSaleStatus.Paused && job.Work.Labor == T(300)
                        && snapshot.Work.WorkerIntervals.Count(x => x.JobId == job.Id && x.End == interruption) == 2
                        && snapshot.Work.AvailableAmount(AppraisalIron) == default && snapshot.Work.AvailableAmount(SaleTender) == default,
                        "One participant's interruption did not release both work schedules and retain both claims.");
                    RejectUnchanged(s, host, SaleCommand(s, CommandKind.ResumeHavenSale, job.Id), "HavenSaleParticipantIncapable");
                    WorldAdvance(s, 6);
                    SaleCommit(s, CCCommand(s, "sale-cure", actor));
                    Require(s.Capture().HavenSales.Single().Work.Labor == T(300), "Joint labor advanced during an interruption.");
                    SaleCommit(s, SaleCommand(s, CommandKind.ResumeHavenSale, job.Id));
                    WorldAdvance(s, 1500);
                    Require(s.Capture().HavenSales.Single().PaymentCopper == 2, "The resumed pair did not finish.");
                }
            });
            cases.Add("mgt10_haven_sale_half_open_expiry_covers_exact_tie_paused_and_pending", () =>
            {
                var arrival = SaleAtCounter().Capture().RuleClock;
                Require(arrival.Denominator == 1, "Expiry fixture requires a whole-second presentation.");
                int endpoint = checked((int)arrival.Numerator + 1800);
                var tie = SaleAtCounter(SalePolicy(new TestOnlyHavenSaleProfile(expiresAt: endpoint)));
                RejectUnchanged(tie, host, SaleCommand(tie, CommandKind.StartHavenSale), "HavenSaleCannotFinishBeforeExpiry");
                WorldAdvance(tie, 1800);
                RejectUnchanged(tie, host, SaleCommand(tie, CommandKind.StartHavenSale), "HavenSaleOfferNotCurrent");
                var valid = SaleAtCounter(SalePolicy(new TestOnlyHavenSaleProfile(expiresAt: endpoint + 1)));
                SaleCommit(valid, SaleCommand(valid, CommandKind.StartHavenSale));
                WorldAdvance(valid, 1800);
                Require(valid.Capture().HavenSales.Single().Status == HavenSaleStatus.Paid
                    && valid.Capture().HavenSales.Single().UpdatedAt == T(endpoint), "The last eligible whole second did not pay.");
                var paused = SaleAtCounter(SalePolicy(new TestOnlyHavenSaleProfile(expiresAt: endpoint + 1)));
                SaleCommit(paused, SaleCommand(paused, CommandKind.StartHavenSale));
                WorldAdvance(paused, 1, 2);
                SaleCommit(paused, SaleCommand(paused, CommandKind.PauseHavenSale, paused.Capture().HavenSales.Single().Id));
                WorldAdvance(paused, 1800);
                Require(paused.Capture().HavenSales.Single().Status == HavenSaleStatus.Paused,
                    "A paused mandate expired before its exact deadline.");
                WorldAdvance(paused, 1, 2);
                RequireExpiredSale(paused, T(endpoint + 1), T(1, 2));
                var conditions = BuyerEndpointConditions(T(endpoint));
                var pending = PortableWorld(SalePolicy(new TestOnlyHavenSaleProfile(expiresAt: endpoint + 1), conditions));
                SaleCommit(pending, CCCommand(pending, "buyer-stun", SaleBuyer));
                SaleCommit(pending, CCCommand(pending, "buyer-ward", SaleBuyer));
                PresentSaleIron(pending);
                SaleCommit(pending, SaleCommand(pending, CommandKind.StartHavenSale));
                WorldAdvance(pending, 1800);
                Require(pending.Capture().HavenSales.Single().Status == HavenSaleStatus.PendingSettlement,
                    "The endpoint setup did not hold the full unpaid agreement.");
                WorldAdvance(pending, 3);
                RequireExpiredSale(pending, T(endpoint + 1), T(1800));
                RejectUnchanged(pending, host, SaleCommand(pending, CommandKind.FinalizeHavenSale,
                    pending.Capture().HavenSales.Single().Id), "HavenSaleAgreementNotOpen");
            });
            cases.Add("mgt10_haven_sale_requires_both_stationary_available_workers_and_usable_counter", () =>
            {
                var arrival = SaleAtCounter().Capture().RuleClock;
                var blockedFact = new CraftingMishapFact("sale-counter-spill", 1, at: arrival,
                    stationId: TestOnlyHavenSaleProfile.CounterId);
                var blocked = SaleAtCounter(SalePolicy(incident: blockedFact));
                CraftEvent(blocked, blockedFact.Id);
                RejectUnchanged(blocked, host, SaleCommand(blocked, CommandKind.StartHavenSale), "HavenSaleCounterUnavailable");
                var orderFact = new CraftingMishapFact("sale-counter-order-fouling", 5, at: arrival,
                    stationId: TestOnlyHavenSaleProfile.CounterId);
                var busy = SaleAtCounter(SalePolicy(incident: orderFact));
                CraftEvent(busy, orderFact.Id);
                SaleCommit(busy, CraftCommand(busy, orderFact.Id, CommandKind.StartCraftRemedy, SaleBuyer));
                Require(busy.Capture().Work.WorkerIntervals.Any(x => x.WorkerId == SaleBuyer && x.End > arrival),
                    "The buyer did not book conflicting existing work.");
                RejectUnchanged(busy, host, SaleCommand(busy, CommandKind.StartHavenSale), "HavenSaleParticipantBusy");
                SaleCommit(busy, CraftCommand(busy, orderFact.Id, CommandKind.PauseCraftRemedy, SaleBuyer));
                Require(busy.QueryCommand(host, SaleCommand(busy, CommandKind.StartHavenSale)).Admissible,
                    "An unrelated crafting-order restriction blocked the sale counter.");
                SaleCommit(busy, IC(busy, CommandKind.BeginWorldStep, "walk", actor: SaleBuyer, x: 1, y: 0));
                WorldAdvance(busy, 1, 2);
                RejectUnchanged(busy, host, SaleCommand(busy, CommandKind.StartHavenSale), "HavenSaleParticipantsNotAtCounter");
                WorldAdvance(busy, 6);
                RejectUnchanged(busy, host, SaleCommand(busy, CommandKind.StartHavenSale), "HavenSaleParticipantsNotAtCounter");
            });
            cases.Add("mgt10_haven_sale_result_one_counter_restriction_pauses_pair_until_cleanup", () =>
            {
                var arrival = SaleAtCounter().Capture().RuleClock;
                var spill = new CraftingMishapFact("sale-active-counter-spill", 1, at: arrival.AddSeconds(300),
                    stationId: TestOnlyHavenSaleProfile.CounterId);
                var s = SaleAtCounter(SalePolicy(incident: spill));
                SaleCommit(s, SaleCommand(s, CommandKind.StartHavenSale));
                WorldAdvance(s, 300);
                CraftEvent(s, spill.Id);
                var blocked = s.Capture();
                var job = blocked.HavenSales.Single();
                Require(job.Status == HavenSaleStatus.Paused && job.Reason == "HavenSaleCounterUnavailable"
                    && job.Work.Labor == T(300) && blocked.Work.WorkerIntervals.Count(x => x.JobId == job.Id && x.End == spill.At) == 2,
                    "A current station-use restriction did not interrupt both sale bookings.");
                RejectUnchanged(s, host, SaleCommand(s, CommandKind.ResumeHavenSale, job.Id), "HavenSaleCounterUnavailable");
                Remedy(s, spill.Id);
                WorldAdvance(s, 3600);
                var clean = s.Capture();
                Require(clean.HavenSales.Single().Status == HavenSaleStatus.Paused && clean.HavenSales.Single().Work.Labor == T(300)
                    && clean.Work.AvailableAmount(AppraisalIron) == default && clean.Work.AvailableAmount(SaleTender) == default,
                    "Cleanup advanced sale labor or released either physical claim.");
                WorldAdvance(s, 6);
                SaleCommit(s, SaleCommand(s, CommandKind.ResumeHavenSale, job.Id));
                WorldAdvance(s, 1500);
                Require(s.Capture().HavenSales.Single().PaymentCopper == 2, "Explicit resumption failed after normal cleanup.");
            });
            cases.Add("mgt10_haven_sale_shared_handling_credits_pair_and_encounter_entry_interrupts", () =>
            {
                var s = SaleAtCounter();
                SaleCommit(s, SaleCommand(s, CommandKind.StartHavenSale));
                PortableCommit(s, Portable(s, CommandKind.HandlePortableEquipment, PortableKitFixture.Tools,
                    handling: HandlingKind.Retrieve));
                Require(s.Capture().HavenSales.Single().Work.Labor == T(1),
                    "Unrelated one-second handling did not advance joint labor exactly once.");
                WorldStep(s, 1, 0);
                WorldAdvance(s, 2);
                WorldStep(s, 1, 0);
                WorldAdvance(s, 2);
                WorldStep(s, 1, 0);
                var tactical = s.Capture();
                var job = tactical.HavenSales.Single();
                Require(tactical.InventoryCombat && !tactical.Encounter.Order.Contains(SaleBuyer)
                    && job.Status == HavenSaleStatus.Paused && job.Work.Labor == T(5)
                    && tactical.Work.WorkerIntervals.All(x => x.JobId != job.Id || x.End <= tactical.RuleClock)
                    && tactical.Work.AvailableAmount(AppraisalIron) == default && tactical.Work.AvailableAmount(SaleTender) == default,
                    "Tactical entry did not stop both commitments at the real clock boundary.");
            });
            cases.Add("mgt10_haven_sale_rejects_forged_quote_paid_title_and_misbound_tender", () =>
            {
                var policy = SalePolicy();
                var s = SaleAtCounter(policy);
                var forged = s.Capture();
                forged.PortableEquipment = forged.PortableEquipment.Select(item => item.Id != SaleTender ? item
                    : new PortableEquipmentRecord(item.Id, item.ProfileId, item.OwnerId, item.CustodianId, item.ParentId,
                        item.Placement, item.LinkKind, AppraisalIron, item.MassBasis, item.SourceWeightLb, item.OperationalWeightLb)).ToArray();
                Require(policy.QueryCommand(forged, host, SaleCommand(s, CommandKind.StartHavenSale)).Code == "HavenSaleTenderUnavailable",
                    "Direct admission accepted misbound physical tender.");
                Throws<ArgumentException>(() => new Simulation(SalePolicy(), forged, ExecutionProfile.Laboratory));
                SaleCommit(s, SaleCommand(s, CommandKind.StartHavenSale));
                WorldAdvance(s, 1800);
                var paid = s.Capture();
                var record = paid.HavenSales.Single();
                var basis = record.Basis;
                var replacement = new HavenSaleBasis(basis.OfferId, basis.OfferVersionId, basis.SellerId, basis.BuyerId, basis.CounterId,
                    basis.MandateId, basis.ClearanceId, basis.ExemptionId, basis.ExemptionIssuerId, basis.JurisdictionId,
                    basis.AppraisalId, basis.GoodsLotId, basis.TenderLotId, basis.CurrencyUnitId, basis.MintId, basis.GoodsQuantity,
                    basis.TenderCount, new RuleQuantity(8, 3), basis.ValidFrom, basis.ExpiresAt);
                var changedQuote = paid.Copy();
                changedQuote.HavenSales[0] = new HavenSaleRecord(record.Id, replacement, record.StartRevision, record.UpdatedRevision,
                    record.StartedAt, record.UpdatedAt, record.Work.Labor, record.Status, record.Reason, record.PaymentCopper);
                var codec = new SnapshotCodec();
                Throws<ArgumentException>(() => new Simulation(SalePolicy(), codec.Decode(codec.Encode(changedQuote)), ExecutionProfile.Laboratory));
                var originalOwner = paid.InventoryLots.Single(x => x.LotId == SaleTender);
                paid.InventoryLots = paid.InventoryLots.Select(item => item.LotId != SaleTender ? item
                    : new InventoryLotRecord(item.LotId, item.ParentId, SaleBuyer, item.CreatedAmount, item.CreatedAt,
                        item.Nutrition, item.FreshUntil, item.Access)).ToArray();
                paid.PortableEquipment = paid.PortableEquipment.Select(item => item.Id != SaleTender ? item
                    : new PortableEquipmentRecord(item.Id, item.ProfileId, SaleBuyer, item.CustodianId, item.ParentId,
                        item.Placement, item.LinkKind, item.LinkedId, item.MassBasis, item.SourceWeightLb, item.OperationalWeightLb)).ToArray();
                Require(originalOwner.OwnerId == SaleSeller, "The original paid receipt lacked tender title.");
                Throws<ArgumentException>(() => codec.Encode(paid));
                Throws<ArgumentException>(() => new Simulation(SalePolicy(), paid, ExecutionProfile.Laboratory));
            });
        }

        private static ConditionCombatFixture BuyerEndpointConditions(RuleTime endpoint)
            => new ConditionCombatFixture(CCApply("buyer-stun", "Stunned", SaleBuyer),
                CCGrant("buyer-ward", SaleBuyer, new ConditionStamp(endpoint), "Stunned"),
                new ConditionFixtureEvent(SaleBuyer, ConditionOperation.Cure("event.buyer-cure", new ConditionStamp(endpoint), "Stunned")));

        private static void RequireExpiredSale(Simulation s, RuleTime deadline, RuleTime labor)
        {
            var state = s.Capture();
            var sale = state.HavenSales.Single();
            Require(sale.Status == HavenSaleStatus.Expired && sale.UpdatedAt == deadline && sale.Work.Labor == labor
                && !sale.PaymentCopper.HasValue && state.Work.AvailableAmount(AppraisalIron) == new RuleQuantity(1)
                && state.Work.AvailableAmount(SaleTender) == new RuleQuantity(2), "Expiry failed to close and release the exact unpaid agreement.");
            RequireSaleAsset(state, AppraisalIron, SaleSeller, new RuleQuantity(1));
            RequireSaleAsset(state, SaleTender, SaleBuyer, new RuleQuantity(2));
        }

        private static string SaleAuditRow(string label, Snapshot s)
        {
            var job = s.HavenSales.Single();
            var basis = job.Basis;
            var goods = s.PortableEquipment.Single(x => x.Id == basis.GoodsLotId);
            var tender = s.PortableEquipment.Single(x => x.Id == basis.TenderLotId);
            return string.Join("\t", label, s.RuleClock, s.Revision, job.Id, job.Status, job.Work.Labor,
                s.HavenAppraisals.Single().ResultCopper, basis.ExactQuoteCopper, job.PaymentCopper,
                goods.Id, s.Work.Lots.Single(x => x.Id == goods.Id).Amount, goods.OwnerId, goods.CustodianId,
                tender.Id, s.Work.Lots.Single(x => x.Id == tender.Id).Amount, tender.OwnerId, tender.CustodianId,
                PortableEquipmentValidation.Mass(s, tender), PortableEquipmentRules.CarriedBurden(s, SaleBuyer).Pounds,
                PortableEquipmentRules.CarriedBurden(s, SaleSeller).Pounds);
        }
    }
}
#endif
