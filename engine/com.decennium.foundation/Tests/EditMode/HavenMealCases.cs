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
        private const string HavenMealLot = TestOnlyHavenMealProfile.MealLotId;
        private const string HavenMealOfferVersion = TestOnlyHavenMealProfile.OfferVersionId;

        private static TestOnlySharedWorldPolicy MealPolicy(TestOnlyHavenMealProfile profile = null,
            ConditionCombatFixture conditions = null, CraftingMishapFact incident = null)
            => SalePolicy(conditions: conditions, incident: incident).EnableHavenMeal(profile ?? new TestOnlyHavenMealProfile());

        private static void EarnMealTender(Simulation s, bool withEncounter = false)
        {
            PresentSaleIron(s, withEncounter);
            SaleCommit(s, SaleCommand(s, CommandKind.StartHavenSale));
            WorldAdvance(s, 1800);
            WorldAdvance(s, 6);
            Require(s.Capture().HavenSales.Single().PaymentCopper == 2, "The prior funded sale did not supply the actual tender.");
        }

        private static Simulation MealAtCounter(TestOnlySharedWorldPolicy policy = null, bool withEncounter = false)
        {
            var s = PortableWorld(policy ?? MealPolicy());
            EarnMealTender(s, withEncounter);
            return s;
        }

        private static Command PurchaseMeal(Simulation s, string target = HavenMealOfferVersion, string actor = SaleSeller)
            => MiningCommand(s, CommandKind.PurchaseHavenMeal, target, actor: actor);

        private static void EatMeal(Simulation s, RuleQuantity amount, string lotId = HavenMealLot)
            => WorldCommit(s, IC(s, CommandKind.StartIntake, lotId, new InventoryRequest(amount), SaleSeller));

        private static Command HandleMeal(Simulation s, HandlingKind handling, string lotId = HavenMealLot, string destination = "")
            => Portable(s, CommandKind.HandlePortableEquipment, lotId, destination, handling, SaleSeller);

        private static void AddHavenMealCases(Dictionary<string, Action> cases, string directory)
        {
            var host = HavenSaleHost();
            cases.Add("mgt10_haven_meal_connected_sale_purchase_intake_restore_and_continue", () =>
            {
                var s = MealAtCounter(withEncounter: true);
                var saleState = s.Capture();
                Require(saleState.SchemaVersion == Snapshot.HavenMealSchema, "The funded meal did not select schema80.");
                RequireSaleAsset(saleState, SaleTender, SaleSeller, new RuleQuantity(2));
                RequireSaleAsset(saleState, HavenMealLot, SaleBuyer, new RuleQuantity(2, 3));
                var keepCoins = new Simulation(MealPolicy(), saleState, ExecutionProfile.Laboratory);
                WorldStep(keepCoins, 1, 0, actor: SaleSeller);
                WorldAdvance(keepCoins, 2);
                Require(keepCoins.Capture().HavenMealPurchases.Length == 0, "Leaving without a meal command spent the coins.");
                RequireSaleAsset(keepCoins.Capture(), SaleTender, SaleSeller, new RuleQuantity(2));
                var purchase = PurchaseMeal(s);
                var bytes = Bytes(s);
                var query = s.QueryCommand(host, purchase);
                Require(query.Admissible && query.HavenMealOffer?.ExactQuoteCopper == new RuleQuantity(2)
                    && query.HavenMealOffer.ServingPounds == new RuleQuantity(2, 3)
                    && query.HavenMealOffer.FreshUntil == T(86400) && bytes.SequenceEqual(Bytes(s))
                    && s.DiscoverCommands(host, SaleSeller).Any(x => x.Command.Kind == CommandKind.PurchaseHavenMeal && x.Query.Admissible),
                    "The authorized read-only quote omitted exact terms or touched state: " + query.Code);
                SaleCommit(s, purchase);
                var bought = s.Capture();
                var receipt = bought.HavenMealPurchases.Single();
                Require(bought.RuleClock == saleState.RuleClock.AddSeconds(1) && bought.RandomState == saleState.RandomState
                    && receipt.PriorSaleId == saleState.HavenSales.Single().Id && receipt.PaymentCopper == 2
                    && bought.Work.WorkerIntervals.Count(x => x.JobId == receipt.Id) == 2
                    && bought.Work.Reservations.Count(x => x.JobId == receipt.Id && x.ConsumedAmount == default && x.ReleasedAmount == x.Amount) == 2
                    && bought.Intakes.Length == saleState.Intakes.Length && ReferenceEquals(bought.HavenSales.Single(), saleState.HavenSales.Single())
                    && ReferenceEquals(bought.HavenAppraisals.Single(), saleState.HavenAppraisals.Single()),
                    "One-second purchase lost historical records, invented consumption, or booked the wrong work.");
                RequireSaleAsset(bought, SaleTender, SaleBuyer, new RuleQuantity(2));
                RequireSaleAsset(bought, HavenMealLot, SaleSeller, new RuleQuantity(2, 3));
                string boughtPath = Path.Combine(directory, "mgt10-haven-meal-purchased.ddsave");
                new FileSaveStore().Save(boughtPath, bought);
                Require(Bytes(new Simulation(MealPolicy(), new FileSaveStore().Load(boughtPath), ExecutionProfile.Laboratory))
                    .SequenceEqual(Bytes(s)), "The purchased serving changed on disk restore.");
                Throws<ArgumentException>(() => new Simulation(SalePolicy(), bought, ExecutionProfile.Laboratory));
                var conflict = new Command(purchase.Id, purchase.Actor, purchase.ExpectedRevision, purchase.Kind, "changed-offer");
                RejectUnchanged(s, host, conflict, "CommandIdConflict");
                RejectUnchanged(s, host, PurchaseMeal(s), "HavenMealAlreadyPurchased");
                RejectUnchanged(s, host, IC(s, CommandKind.BeginWorldStep, "walk", actor: SaleSeller, x: 1),
                    "HavenMealUnpackedTakeawayUnsupported");
                EatMeal(s, new RuleQuantity(2, 3));
                WorldAdvance(s, 1, 2);
                var partial = s.Capture();
                Require(OrdinaryInventory.Consumed(partial, SaleSeller, NutritionKind.FoodPounds) == new RuleQuantity(1, 1800),
                    "The shared intake did not debit fractional food at the existing rate.");
                string midPath = Path.Combine(directory, "mgt10-haven-meal-intake.ddsave");
                new FileSaveStore().Save(midPath, partial);
                var replay = new Simulation(MealPolicy(), new FileSaveStore().Load(midPath), ExecutionProfile.Laboratory);
                var audit = new List<string> { "event\tclock\tappraisal\tpriorSalePayment\tpurchasePayment\ttender\ttenderOwner\ttenderAmount\tmeal\tmealOwner\tmealAmount\tconsumed\tfreshUntil" };
                audit.Add(HavenMealAudit("paid-sale", saleState));
                audit.Add(HavenMealAudit("purchased", bought));
                audit.Add(HavenMealAudit("partial", partial));
                foreach (var run in new[] { s, replay }) {
                    WorldAdvance(run, 1199, 2);
                    var eaten = run.Capture();
                    Require(eaten.Work.Lots.Single(x => x.Id == HavenMealLot).Amount == default
                        && eaten.Intakes.Single(x => x.LotId == HavenMealLot).Status == IntakeStatus.Complete
                        && OrdinaryInventory.Consumed(eaten, SaleSeller, NutritionKind.FoodPounds) == new RuleQuantity(2, 3)
                        && eaten.HavenAppraisals.Single().ResultCopper == new RuleQuantity(15, 2)
                        && eaten.HavenSales.Single().PaymentCopper == 2 && eaten.HavenMealPurchases.Single().PaymentCopper == 2,
                        "Six hundred actual eating seconds failed to consume the one delivered serving and retain both receipts.");
                    WorldStep(run, 1, 0, actor: SaleSeller);
                    WorldAdvance(run, 2);
                    var continued = Bytes(run);
                    Require(run.Execute(host, purchase).Outcome == Outcome.Duplicate && continued.SequenceEqual(Bytes(run)),
                        "The prior purchase receipt lost idempotence after intake and movement.");
                }
                Require(Bytes(s).SequenceEqual(Bytes(replay)), "The same intake and onward exploration differed after save restoration.");
                audit.Add(HavenMealAudit("continued", s.Capture()));
                File.WriteAllLines(Path.Combine(directory, "haven-meal-audit.tsv"), audit);
            });
            cases.Add("mgt10_haven_meal_requires_prior_paid_tender_and_independent_vendor_authority", () =>
            {
                var fresh = PortableWorld(MealPolicy());
                RejectUnchanged(fresh, host, PurchaseMeal(fresh), "HavenMealPriorPaidTenderRequired");
                foreach (var entry in new[] {
                    (new TestOnlyHavenMealProfile(vendorConsented: false), "HavenMealVendorMandateMissing"),
                    (new TestOnlyHavenMealProfile(stockAvailable: false), "HavenMealServingUnavailable"),
                    (new TestOnlyHavenMealProfile(stockTitleCleared: false), "HavenMealStockTitleUnresolved"),
                    (new TestOnlyHavenMealProfile(spendingCleared: false), "HavenMealSpendingNotCleared"),
                    (new TestOnlyHavenMealProfile(currencyAccepted: false), "HavenMealTenderNotAccepted") }) {
                    var s = MealAtCounter(MealPolicy(entry.Item1));
                    RejectUnchanged(s, host, PurchaseMeal(s), entry.Item2);
                    Require(s.QueryCommand(host, PurchaseMeal(s)).Code == entry.Item2, "Read-only admission disagreed about independent authority.");
                }
                var policy = MealPolicy();
                var meal = MealAtCounter(policy);
                var customerOnly = new Authority(host.Principal, new[] { SaleSeller }, inventoryOwners: new[] { SaleSeller });
                RejectUnchanged(meal, customerOnly, PurchaseMeal(meal), "InventoryNotAuthorized");
                Require(meal.QueryCommand(customerOnly, PurchaseMeal(meal)).Code == "InventoryNotAuthorized",
                    "The customer's property grant implied vendor property permission.");
                var reserved = meal.Capture();
                reserved.Work = reserved.Work.Reserve("existing-meal-hold", Array.Empty<WorkerInterval>(),
                    new[] { new ResourceReservation("existing-meal-claim", "existing-meal-hold", HavenMealLot, new RuleQuantity(1, 3)) });
                Require(policy.QueryCommand(reserved, host, PurchaseMeal(meal)).Code == "HavenMealAssetReserved"
                    && policy.Resolve(reserved, PurchaseMeal(meal)) == "HavenMealAssetReserved"
                    && reserved.HavenMealPurchases.Length == 0, "A reserved serving admitted a purchase.");
                PortableCommit(meal, Portable(meal, CommandKind.HandlePortableEquipment, SaleTender, handling: HandlingKind.Drop, actor: SaleSeller));
                WorldAdvance(meal, 6);
                RejectUnchanged(meal, host, PurchaseMeal(meal), "HavenMealTenderUnavailable");
            });
            cases.Add("mgt10_haven_meal_partial_drop_return_and_descendant_takeaway_guards", () =>
            {
                var s = MealAtCounter();
                SaleCommit(s, PurchaseMeal(s));
                EatMeal(s, new RuleQuantity(2, 3));
                WorldAdvance(s, 150);
                var partial = s.Capture();
                var intake = partial.Intakes.Single(x => x.LotId == HavenMealLot);
                var drop = HandleMeal(s, HandlingKind.Drop);
                var beforeDrop = Bytes(s);
                var dropResult = s.Execute(host, drop);
                Require(dropResult.Outcome == Outcome.Rejected && beforeDrop.SequenceEqual(Bytes(s)),
                    "A reserved serving moved during active intake.");
                WorldCommit(s, IC(s, CommandKind.InterruptIntake, intake.Id, actor: SaleSeller));
                WorldAdvance(s, 6);
                var interrupted = s.Capture();
                Require(interrupted.Intakes.Single(x => x.Id == intake.Id).Status == IntakeStatus.Interrupted
                    && interrupted.Work.Lots.Single(x => x.Id == HavenMealLot).Amount == new RuleQuantity(1, 2)
                    && OrdinaryInventory.Consumed(interrupted, SaleSeller, NutritionKind.FoodPounds) == new RuleQuantity(1, 6),
                    "Interruption consumed untouched food or restored eaten stock.");
                string path = Path.Combine(directory, "mgt10-haven-meal-interrupted.ddsave");
                new FileSaveStore().Save(path, interrupted);
                var replay = new Simulation(MealPolicy(), new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                Require(Bytes(s).SequenceEqual(Bytes(replay)), "Interrupted serving state changed on restore.");
                foreach (var run in new[] { s, replay }) {
                    WorldCommit(run, IC(run, CommandKind.PortionInventory, HavenMealLot, new InventoryRequest(new RuleQuantity(1, 6)), SaleSeller));
                    var child = run.Capture().InventoryLots.Single(x => x.ParentId == HavenMealLot);
                    Require(child.FreshUntil == T(86400) && child.OwnerId == SaleSeller, "Portioning reset food age or title.");
                    RejectUnchanged(run, host, HandleMeal(run, HandlingKind.Stow, child.LotId, PortableKitFixture.Pack),
                        "HavenMealPackingUnsupported");
                    RejectUnchanged(run, host, HandleMeal(run, HandlingKind.Handover, child.LotId, SaleBuyer),
                        "HavenMealPackingUnsupported");
                    RejectUnchanged(run, host, IC(run, CommandKind.HandleInventory, child.LotId,
                        new InventoryRequest(new RuleQuantity(1, 6), handling: HandlingKind.Drop), SaleSeller), "HavenMealPackingUnsupported");
                    PortableCommit(run, HandleMeal(run, HandlingKind.Drop));
                    WorldAdvance(run, 6);
                    RejectUnchanged(run, host, IC(run, CommandKind.BeginWorldStep, "walk", actor: SaleSeller, x: 1),
                        "HavenMealUnpackedTakeawayUnsupported");
                    PortableCommit(run, HandleMeal(run, HandlingKind.Drop, child.LotId));
                    WorldStep(run, 1, 0, actor: SaleSeller);
                    WorldAdvance(run, 6);
                    RejectUnchanged(run, host, HandleMeal(run, HandlingKind.Pickup, child.LotId), "HavenMealServingRequiresCounter");
                    WorldStep(run, -1, 0, actor: SaleSeller);
                    WorldAdvance(run, 6);
                    PortableCommit(run, HandleMeal(run, HandlingKind.Pickup, child.LotId));
                    WorldAdvance(run, 6);
                    EatMeal(run, new RuleQuantity(1, 6), child.LotId);
                    WorldAdvance(run, 150);
                    WorldAdvance(run, 6);
                    PortableCommit(run, HandleMeal(run, HandlingKind.Pickup));
                    WorldAdvance(run, 6);
                    EatMeal(run, new RuleQuantity(1, 3));
                    WorldAdvance(run, 300);
                    var completed = run.Capture();
                    Require(OrdinaryInventory.Consumed(completed, SaleSeller, NutritionKind.FoodPounds) == new RuleQuantity(2, 3)
                        && completed.InventoryLots.Single(x => x.LotId == HavenMealLot).FreshUntil == T(86400)
                        && completed.HavenMealPurchases.Single().Offer.ServingPounds == new RuleQuantity(2, 3),
                        "Normal return and intake changed the delivered quantity, title or age.");
                    WorldStep(run, 1, 0, actor: SaleSeller);
                    WorldAdvance(run, 2);
                }
                Require(Bytes(s).SequenceEqual(Bytes(replay)), "The drop, return, and remainder continuation differed after replay.");
            });
            cases.Add("mgt10_haven_meal_delivery_and_eating_respect_original_expiry", () =>
            {
                var arrival = MealAtCounter().Capture().RuleClock;
                Require(arrival.Denominator == 1, "Deadline fixtures require a whole-second arrival.");
                int endpoint = checked((int)arrival.Numerator + 1);
                var offerTie = MealAtCounter(MealPolicy(new TestOnlyHavenMealProfile(expiresAt: endpoint)));
                RejectUnchanged(offerTie, host, PurchaseMeal(offerTie), "HavenMealOfferNotCurrent");
                var foodTie = MealAtCounter(MealPolicy(new TestOnlyHavenMealProfile(cookedAgeAtEpoch: 86400 - endpoint)));
                RejectUnchanged(foodTie, host, PurchaseMeal(foodTie), "HavenMealServingExpiresBeforeDelivery");
                foreach (int available in new[] { 300, 600 }) {
                    int freshUntil = endpoint + available;
                    var s = MealAtCounter(MealPolicy(new TestOnlyHavenMealProfile(cookedAgeAtEpoch: 86400 - freshUntil)));
                    SaleCommit(s, PurchaseMeal(s));
                    EatMeal(s, new RuleQuantity(2, 3));
                    WorldAdvance(s, 600);
                    var state = s.Capture();
                    var intake = state.Intakes.Single(x => x.LotId == HavenMealLot);
                    var expected = new RuleQuantity(available, 900);
                    Require(intake.EndedAt == T(freshUntil)
                        && intake.Status == (available == 600 ? IntakeStatus.Complete : IntakeStatus.Expired)
                        && state.HavenMealPurchases.Single().Offer.FreshUntil == T(freshUntil)
                        && OrdinaryInventory.Consumed(state, SaleSeller, NutritionKind.FoodPounds) == expected
                        && state.Work.Lots.Single(x => x.Id == HavenMealLot).Amount == new RuleQuantity(2, 3) - expected,
                        "Purchase reset food age or ordinary intake crossed its original freshness boundary.");
                }
            });
            cases.Add("mgt10_haven_meal_one_second_credits_unrelated_intake_and_fences_unsupported_boundary", () =>
            {
                var s = MealAtCounter();
                PortableCommit(s, Portable(s, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations,
                    handling: HandlingKind.Retrieve));
                WorldCommit(s, IC(s, CommandKind.StartIntake, PortableKitFixture.Rations, new InventoryRequest(new RuleQuantity(1))));
                var before = s.Capture();
                var buy = PurchaseMeal(s);
                var bytes = Bytes(s);
                Require(s.QueryCommand(host, buy).Admissible && bytes.SequenceEqual(Bytes(s)),
                    "A dry-run purchase credited the other worker on live state.");
                SaleCommit(s, buy);
                var after = s.Capture();
                Require(after.RuleClock == before.RuleClock.AddSeconds(1)
                    && OrdinaryInventory.Consumed(after, TestOnlyPolicy.ActorId, NutritionKind.FoodPounds) == new RuleQuantity(1, 900)
                    && OrdinaryInventory.Consumed(after, SaleSeller, NutritionKind.FoodPounds) == default,
                    "One physical exchange skipped or double-credited another worker, or consumed the new meal.");
                var end = MealAtCounter().Capture().RuleClock.AddSeconds(1);
                var conditions = new ConditionCombatFixture(CCApply("meal-stun", "Stunned", SaleSeller),
                    CCGrant("meal-ward", SaleSeller, new ConditionStamp(end), "Stunned"));
                var blocked = PortableWorld(MealPolicy(conditions: conditions));
                CCDispatch(blocked, "meal-stun", SaleSeller);
                CCDispatch(blocked, "meal-ward", SaleSeller);
                EarnMealTender(blocked);
                RejectUnchanged(blocked, host, PurchaseMeal(blocked), "TimedHandlingBoundaryUnsupported");
            });
            cases.Add("mgt10_haven_meal_actual_capacity_and_counter_reject_bilateral_delivery", () =>
            {
                var s = MealAtCounter(MealPolicy(new TestOnlyHavenMealProfile(customerBallast: true)));
                PortableCommit(s, Portable(s, CommandKind.HandlePortableEquipment, TestOnlyHavenMealProfile.CustomerBallastId,
                    actor: SaleSeller));
                WorldAdvance(s, 6);
                RejectUnchanged(s, host, PurchaseMeal(s), "CarryingCapacityExceeded");
                RequireSaleAsset(s.Capture(), HavenMealLot, SaleBuyer, new RuleQuantity(2, 3));
                RequireSaleAsset(s.Capture(), SaleTender, SaleSeller, new RuleQuantity(2));
                var at = MealAtCounter().Capture().RuleClock;
                var spill = new CraftingMishapFact("meal-counter-spill", 1, at: at, stationId: TestOnlyHavenSaleProfile.CounterId);
                var blocked = MealAtCounter(MealPolicy(incident: spill));
                CraftEvent(blocked, spill.Id);
                RejectUnchanged(blocked, host, PurchaseMeal(blocked), "HavenSaleCounterUnavailable");
                var fouling = new CraftingMishapFact("meal-order-only-fouling", 5, at: at, stationId: TestOnlyHavenSaleProfile.CounterId);
                var busy = MealAtCounter(MealPolicy(incident: fouling));
                CraftEvent(busy, fouling.Id);
                SaleCommit(busy, CraftCommand(busy, fouling.Id, CommandKind.StartCraftRemedy, SaleBuyer));
                RejectUnchanged(busy, host, PurchaseMeal(busy), "HavenSaleParticipantBusy");
                SaleCommit(busy, CraftCommand(busy, fouling.Id, CommandKind.PauseCraftRemedy, SaleBuyer));
                Require(busy.QueryCommand(host, PurchaseMeal(busy)).Admissible,
                    "An order-only restriction blocked the meal service after competing labor was paused.");
                var remote = MealAtCounter();
                SaleCommit(remote, IC(remote, CommandKind.BeginWorldStep, "walk", actor: SaleBuyer, x: 1));
                WorldAdvance(remote, 1, 2);
                RejectUnchanged(remote, host, PurchaseMeal(remote), "HavenSaleParticipantsNotAtCounter");
            });
            cases.Add("mgt10_haven_meal_rejects_misbound_stock_and_forged_successor_payment", () =>
            {
                var policy = MealPolicy();
                var s = MealAtCounter(policy);
                var shortTender = s.Capture();
                var lot = shortTender.Work.Lots.Single(x => x.Id == SaleTender);
                shortTender.Work = new WorkLedger(shortTender.Work.Lots.Select(x => x.Id != SaleTender ? x
                    : new ResourceLot(x.Id, x.UnitId, new RuleQuantity(1), x.LocationId, x.CustodianId)),
                    shortTender.Work.WorkerIntervals, shortTender.Work.Reservations);
                Require(lot.Amount == new RuleQuantity(2)
                    && policy.QueryCommand(shortTender, host, PurchaseMeal(s)).Code == "HavenMealTenderUnavailable",
                    "Admission accepted shortened proceeds.");
                Throws<ArgumentException>(() => new Simulation(MealPolicy(), shortTender, ExecutionProfile.Laboratory));
                var misbound = s.Capture();
                misbound.PortableEquipment = misbound.PortableEquipment.Select(x => x.Id != HavenMealLot ? x
                    : new PortableEquipmentRecord(x.Id, x.ProfileId, x.OwnerId, x.CustodianId, x.ParentId, x.Placement,
                        x.LinkKind, SaleTender, x.MassBasis, x.SourceWeightLb, x.OperationalWeightLb)).ToArray();
                Require(policy.QueryCommand(misbound, host, PurchaseMeal(s)).Code == "HavenMealServingUnavailable",
                    "Admission accepted a substituted food link.");
                Throws<ArgumentException>(() => new Simulation(MealPolicy(), misbound, ExecutionProfile.Laboratory));
                var reversal = s.Capture();
                reversal.InventoryLots = reversal.InventoryLots.Select(x => x.LotId != SaleTender ? x
                    : new InventoryLotRecord(x.LotId, x.ParentId, SaleBuyer, x.CreatedAmount, x.CreatedAt, x.Nutrition, x.FreshUntil, x.Access)).ToArray();
                reversal.PortableEquipment = reversal.PortableEquipment.Select(x => x.Id != SaleTender ? x
                    : new PortableEquipmentRecord(x.Id, x.ProfileId, SaleBuyer, x.CustodianId, x.ParentId, x.Placement,
                        x.LinkKind, x.LinkedId, x.MassBasis, x.SourceWeightLb, x.OperationalWeightLb)).ToArray();
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(reversal));
                SaleCommit(s, PurchaseMeal(s));
                var paid = s.Capture();
                var purchase = paid.HavenMealPurchases.Single();
                paid.HavenMealPurchases[0] = new HavenMealPurchaseRecord(purchase.Id, purchase.Offer, purchase.PriorSaleId,
                    purchase.PriorPaymentRevision + 1, purchase.Revision, purchase.StartedAt, purchase.EndedAt, purchase.PaymentCopper);
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(paid));
                Throws<ArgumentException>(() => new Simulation(MealPolicy(), paid, ExecutionProfile.Laboratory));
            });
        }

        private static string HavenMealAudit(string label, Snapshot s)
        {
            var tender = s.InventoryLots.Single(x => x.LotId == SaleTender);
            var meal = s.InventoryLots.Single(x => x.LotId == HavenMealLot);
            return string.Join("\t", label, s.RuleClock, s.HavenAppraisals.Single().ResultCopper,
                s.HavenSales.Single().PaymentCopper, s.HavenMealPurchases.SingleOrDefault()?.PaymentCopper,
                SaleTender, tender.OwnerId, s.Work.Lots.Single(x => x.Id == SaleTender).Amount,
                HavenMealLot, meal.OwnerId, s.Work.Lots.Single(x => x.Id == HavenMealLot).Amount,
                OrdinaryInventory.Consumed(s, SaleSeller, NutritionKind.FoodPounds), meal.FreshUntil);
        }
    }
}
#endif
