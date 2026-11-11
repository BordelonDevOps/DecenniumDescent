#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class TestOnlyHavenMealProfile
    {
        public const string CustomerId = TestOnlyHavenSaleProfile.SellerId;
        public const string VendorId = TestOnlyHavenSaleProfile.BuyerId;
        public const string OfferVersionId = "TEST_ONLY.haven-ordinary-hot-meal.v1";
        public const string MealLotId = "TEST_ONLY.haven-cooked-serving";
        public const string ServingSurfaceId = "TEST_ONLY.haven-food-safe-counter-surface";
        public const string VendorMandateId = "TEST_ONLY.haven-ordinary-meal-vendor-mandate";
        public const string StockTitleId = "TEST_ONLY.haven-vendor-cleared-serving-title";
        public const string SpendingClearanceId = "TEST_ONLY.haven-discretionary-sale-proceeds";
        public const string CustomerBallastId = "TEST_ONLY.haven-meal-capacity-ballast";
        internal const string MealItemProfileId = "TEST_ONLY.haven-hand-managed-cooked-food";
        internal const string ServingSurfaceProfileId = "TEST_ONLY.haven-food-safe-serving-surface";
        public static RuleQuantity ServingPounds => new RuleQuantity(2, 3);
        public static RuleQuantity ExactQuoteCopper => new RuleQuantity(2);

        public bool VendorConsented { get; }
        public bool StockAvailable { get; }
        public bool StockTitleCleared { get; }
        public bool SpendingCleared { get; }
        public bool CurrencyAccepted { get; }
        public bool CustomerBallast { get; }
        public int CookedAgeAtEpoch { get; }
        public RuleTime ValidFrom { get; }
        public RuleTime ExpiresAt { get; }
        public RuleTime FreshUntil => new RuleTime(86400 - CookedAgeAtEpoch);

        public TestOnlyHavenMealProfile(bool vendorConsented = true, bool stockAvailable = true, bool stockTitleCleared = true,
            bool spendingCleared = true, bool currencyAccepted = true, int cookedAgeAtEpoch = 0,
            int validFrom = 0, int expiresAt = 18000, bool customerBallast = false)
        {
            if (cookedAgeAtEpoch < 0 || cookedAgeAtEpoch >= 86400 || validFrom < 0 || expiresAt <= validFrom)
                throw new ArgumentException("Invalid finite prepared meal fixture.");
            VendorConsented = vendorConsented;
            StockAvailable = stockAvailable;
            StockTitleCleared = stockTitleCleared;
            SpendingCleared = spendingCleared;
            CurrencyAccepted = currencyAccepted;
            CustomerBallast = customerBallast;
            CookedAgeAtEpoch = cookedAgeAtEpoch;
            ValidFrom = new RuleTime(validFrom);
            ExpiresAt = new RuleTime(expiresAt);
        }

        internal HavenMealOffer Offer => new HavenMealOffer(OfferVersionId, CustomerId, VendorId, TestOnlyHavenSaleProfile.CounterId,
            ServingSurfaceId, VendorMandateId, StockTitleId, SpendingClearanceId, MealLotId, TestOnlyHavenSaleProfile.TenderLotId,
            TestOnlyHavenSaleProfile.CurrencyUnitId, ServingPounds, ExactQuoteCopper, ValidFrom, ExpiresAt, FreshUntil);

        internal string Key => string.Join("|", "FL05-FL21-FL22-FL24-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4",
            CustomerId, VendorId, OfferVersionId, TestOnlyHavenSaleProfile.CounterId, MealLotId, TestOnlyHavenSaleProfile.TenderLotId,
            ServingSurfaceId, ServingSurfaceProfileId, MealItemProfileId, VendorMandateId, StockTitleId, SpendingClearanceId,
            "on-site-hand-managed-serving-no-separate-fee-1-shared-second", ServingPounds, ExactQuoteCopper, VendorConsented,
            StockAvailable, StockTitleCleared, SpendingCleared, CurrencyAccepted, CookedAgeAtEpoch, ValidFrom, ExpiresAt,
            CustomerBallast, CustomerBallastId, "195/2 pound ballast");
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyHavenMealProfile havenMealProfile;

        public TestOnlySharedWorldPolicy EnableHavenMeal(TestOnlyHavenMealProfile profile)
        {
            if (profile == null) throw new ArgumentNullException(nameof(profile));
            if (initializationStarted || havenMealProfile != null || SelectedSchema != Snapshot.HavenSaleSchema)
                throw new InvalidOperationException("Select one funded meal after the bounded Haven sale and before initialization.");
            havenMealProfile = profile;
            using (var sha = SHA256.Create())
                ContentFingerprint = "TEST_ONLY.haven-meal-v1-" + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(ContentFingerprint + "|" + profile.Key)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
            return this;
        }

        private void InitializeHavenMeal(Snapshot s)
        {
            if (havenMealProfile == null) return;
            const string vendor = TestOnlyHavenMealProfile.VendorId;
            const string customer = TestOnlyHavenMealProfile.CustomerId;
            s.Structures = s.Structures.Append(new ObjectStructureRecord(TestOnlyHavenMealProfile.ServingSurfaceId,
                TestOnlyHavenMealProfile.ServingSurfaceProfileId, vendor, vendor, AppraisalGround, ObjectMaterial.WoodLeather,
                5, 5, 0, new RuleQuantity(10))).ToArray();
            if (havenMealProfile.StockAvailable) {
                const string meal = TestOnlyHavenMealProfile.MealLotId;
                var amount = TestOnlyHavenMealProfile.ServingPounds;
                s.Work = new WorkLedger(s.Work.Lots.Append(new ResourceLot(meal, TestOnlyInventoryPolicy.FoodUnit, amount, vendor, vendor)),
                    s.Work.WorkerIntervals, s.Work.Reservations);
                s.InventoryLots = s.InventoryLots.Append(new InventoryLotRecord(meal, "", vendor, amount, s.RuleClock,
                    NutritionKind.FoodPounds, havenMealProfile.FreshUntil, InventoryAccess.Ready)).ToArray();
                s.PortableEquipment = s.PortableEquipment.Append(new PortableEquipmentRecord(meal, TestOnlyHavenMealProfile.MealItemProfileId,
                    vendor, vendor, "", PortablePlacement.Carried, PortableLinkKind.InventoryLot, meal, PortableMassBasis.FoodPounds,
                    amount, null)).ToArray();
            }
            if (havenMealProfile.CustomerBallast) {
                var mass = new RuleQuantity(195, 2);
                s.PortableEquipment = s.PortableEquipment.Append(new PortableEquipmentRecord(TestOnlyHavenMealProfile.CustomerBallastId,
                    "TEST_ONLY.haven-meal-ballast", customer, customer, "", PortablePlacement.Ground, PortableLinkKind.None,
                    "", PortableMassBasis.Fixed, mass, mass, groundX: TestOnlyHavenAppraisalProfile.SiteX,
                    groundY: TestOnlyHavenAppraisalProfile.SiteY)).ToArray();
            }
        }

        private IEnumerable<Command> DiscoverHavenMealCommands(Snapshot s, string actor)
        {
            if (havenMealProfile != null && actor == TestOnlyHavenMealProfile.CustomerId && s.HavenMealPurchases.Length == 0
                && s.HavenSales.Any(x => x.Status == HavenSaleStatus.Paid))
                yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".haven-meal.buy", actor,
                    s.Revision, CommandKind.PurchaseHavenMeal, TestOnlyHavenMealProfile.OfferVersionId);
        }

        private string MealTermsFailure()
        {
            if (!havenMealProfile.VendorConsented) return "HavenMealVendorMandateMissing";
            if (!havenMealProfile.StockTitleCleared) return "HavenMealStockTitleUnresolved";
            if (!havenMealProfile.SpendingCleared) return "HavenMealSpendingNotCleared";
            if (!havenMealProfile.CurrencyAccepted) return "HavenMealTenderNotAccepted";
            return null;
        }

        private static bool UsableMealSurface(Snapshot s)
        {
            var surface = s.Structures.SingleOrDefault(x => x.Id == TestOnlyHavenMealProfile.ServingSurfaceId);
            return surface != null && surface.ProfileId == TestOnlyHavenMealProfile.ServingSurfaceProfileId
                && surface.LocationId == AppraisalGround && !surface.Broken && !CraftingRestrictions.StationUseBlocked(s, surface.Id);
        }

        private string MealAssetsFailure(Snapshot s, HavenMealOffer offer, out HavenSaleRecord prior)
        {
            prior = s.HavenSales.SingleOrDefault(x => x.Status == HavenSaleStatus.Paid);
            if (prior == null || prior.Basis.SellerId != offer.CustomerId || prior.Basis.BuyerId != offer.VendorId
                || prior.Basis.TenderLotId != offer.TenderLotId || prior.Basis.CurrencyUnitId != offer.CurrencyUnitId
                || prior.PaymentCopper != offer.PaymentCopper)
                return "HavenMealPriorPaidTenderRequired";
            if (!SaleAssetAtParty(s, offer.TenderLotId, offer.CustomerId, offer.CurrencyUnitId, new RuleQuantity(offer.PaymentCopper))
                || s.PortableEquipment.Single(x => x.Id == offer.TenderLotId).ProfileId != TestOnlyHavenSaleProfile.CoinProfileId)
                return "HavenMealTenderUnavailable";
            if (!SaleAssetAtParty(s, offer.MealLotId, offer.VendorId, TestOnlyInventoryPolicy.FoodUnit, offer.ServingPounds,
                NutritionKind.FoodPounds) || s.InventoryLots.Single(x => x.LotId == offer.MealLotId).FreshUntil != offer.FreshUntil
                || s.PortableEquipment.Single(x => x.Id == offer.MealLotId).ProfileId != TestOnlyHavenMealProfile.MealItemProfileId)
                return "HavenMealServingUnavailable";
            return null;
        }

        private static string ProjectMealDelivery(Snapshot s, HavenMealOffer offer, out Snapshot delivery,
            HavenMealPurchaseRecord purchase = null)
        {
            delivery = s.Copy();
            TransferWholePortableLotTitle(delivery, offer.TenderLotId, offer.VendorId);
            TransferWholePortableLotTitle(delivery, offer.MealLotId, offer.CustomerId);
            PortableEquipmentRules.SynchronizeLinks(delivery);
            if (purchase != null) delivery.HavenMealPurchases = new[] { purchase };
            return CheckPortableProjectedState(delivery);
        }

        private string MealClockFailure(Snapshot s, RuleTime end)
        {
            foreach (var deadline in new[] { NextConditionDeadline(s), NextDyingMarker(s), NextMiningBoundary(s), NextRemedyBoundary(s) })
                if (deadline.HasValue && deadline.Value <= end) return "TimedHandlingBoundaryUnsupported";
            return null;
        }

        private string ResolveHavenMealPurchase(Snapshot s, Command command, out HavenMealOffer offer)
        {
            offer = null;
            if (havenMealProfile == null || s.SchemaVersion != Snapshot.HavenMealSchema) return "HavenMealNotSelected";
            if (command.Actor != TestOnlyHavenMealProfile.CustomerId) return "HavenMealCustomerUnauthorized";
            if (command.Target != TestOnlyHavenMealProfile.OfferVersionId) return "HavenMealOfferUnknown";
            if (command.X != 0 || command.Y != 0 || command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null || command.ExpeditionAssignment != null
                || command.HarvestSelection != null || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null) return "InvalidHavenMealPayload";
            if (s.HavenMealPurchases.Length != 0) return "HavenMealAlreadyPurchased";
            var terms = havenMealProfile.Offer;
            var start = s.RuleClock;
            var end = start.AddSeconds(1);
            if (start < terms.ValidFrom || end >= terms.ExpiresAt) return "HavenMealOfferNotCurrent";
            if (end >= terms.FreshUntil) return "HavenMealServingExpiresBeforeDelivery";
            string failure = MealTermsFailure() ?? MealAssetsFailure(s, terms, out _);
            if (failure != null) return failure;
            if (s.Work.AvailableAmount(terms.MealLotId) != terms.ServingPounds
                || s.Work.AvailableAmount(terms.TenderLotId) != new RuleQuantity(terms.PaymentCopper))
                return "HavenMealAssetReserved";
            if (!UsableMealSurface(s)) return "HavenMealServingSurfaceUnavailable";
            failure = SaleCounterFailure(s) ?? SaleLaborFailure(s, end, false) ?? MealClockFailure(s, end)
                ?? ProjectMealDelivery(s, terms, out _);
            if (failure != null) return failure;

            long revision = s.Revision + 1;
            string id = "haven.meal." + revision.ToString(CultureInfo.InvariantCulture);
            var intervals = new[] { new WorkerInterval(id + ".customer", id, terms.CustomerId, start, end),
                new WorkerInterval(id + ".vendor", id, terms.VendorId, start, end) };
            var claims = new[] { new ResourceReservation(id + ".food", id, terms.MealLotId, terms.ServingPounds),
                new ResourceReservation(id + ".tender", id, terms.TenderLotId, new RuleQuantity(terms.PaymentCopper)) };
            s.Work = s.Work.Reserve(id, intervals, claims);
            failure = AdvanceTo(s, end, initiating: command);
            if (failure != null) return failure;
            if (s.RuleClock != end || end >= terms.ExpiresAt || end >= terms.FreshUntil) return "HavenMealDeliveryBoundaryInvalid";
            failure = MealTermsFailure() ?? SaleCounterFailure(s) ?? SaleLaborFailure(s, end, true);
            if (failure != null) return failure;
            if (!UsableMealSurface(s)) return "HavenMealServingSurfaceUnavailable";
            failure = MealAssetsFailure(s, terms, out var prior);
            if (failure != null) return failure;
            var purchase = new HavenMealPurchaseRecord(id, terms, prior.Id, prior.UpdatedRevision, revision, start, end, terms.PaymentCopper);
            failure = ProjectMealDelivery(s, terms, out var delivery, purchase);
            if (failure != null) return failure;
            s.Work = delivery.Work.Release(id, purchase.FoodClaimId).Release(id, purchase.TenderClaimId);
            s.InventoryLots = delivery.InventoryLots;
            s.PortableEquipment = delivery.PortableEquipment;
            s.HavenMealPurchases = delivery.HavenMealPurchases;
            offer = terms;
            return null;
        }

        private static bool IsMealLineage(Snapshot s, string lotId)
        {
            var lot = s.InventoryLots.SingleOrDefault(x => x.LotId == lotId);
            for (int depth = 0; lot != null && depth < s.InventoryLots.Length; depth++) {
                if (lot.LotId == TestOnlyHavenMealProfile.MealLotId) return true;
                string parent = lot.ParentId;
                lot = parent == "" ? null : s.InventoryLots.SingleOrDefault(x => x.LotId == parent);
            }
            return false;
        }

        private string HavenMealServingCommandFailure(Snapshot s, Command command)
        {
            if (havenMealProfile == null) return null;
            const string customer = TestOnlyHavenMealProfile.CustomerId;
            bool purchased = s.HavenMealPurchases.Length != 0;
            switch (command.Kind) {
                case CommandKind.BeginWorldStep: case CommandKind.ResumeWorldStep: case CommandKind.StartRouteTravel:
                case CommandKind.ResumeRouteTravel: case CommandKind.TacticalStep: case CommandKind.TacticalRepositionStep:
                case CommandKind.Move:
                    return purchased && command.Actor == customer && s.Work.Lots.Any(x => x.CustodianId == customer
                        && x.LocationId == customer && x.Amount > default(RuleQuantity) && IsMealLineage(s, x.Id))
                        ? "HavenMealUnpackedTakeawayUnsupported" : null;
                case CommandKind.PortionInventory: case CommandKind.StartIntake: case CommandKind.HandleInventory:
                case CommandKind.HandlePortableEquipment: case CommandKind.EquipPortableItem: case CommandKind.RemovePortableItem:
                    if (!IsMealLineage(s, command.Target)) return null;
                    if (!purchased || command.Actor != customer) return "HavenMealServingNotAuthorized";
                    if (!AtSalePosition(s, customer, TestOnlyHavenAppraisalProfile.SiteX, TestOnlyHavenAppraisalProfile.SiteY))
                        return "HavenMealServingRequiresCounter";
                    if (command.Kind == CommandKind.HandlePortableEquipment) {
                        if (command.Inventory?.Handling != HandlingKind.Pickup && command.Inventory?.Handling != HandlingKind.Drop)
                            return "HavenMealPackingUnsupported";
                        return UsableMealSurface(s) ? null : "HavenMealServingSurfaceUnavailable";
                    }
                    if (command.Kind == CommandKind.StartIntake || command.Kind == CommandKind.PortionInventory)
                        return s.InventoryLots.Single(x => x.LotId == command.Target).Access == InventoryAccess.Ready
                            ? null : "HavenMealServingRequiresReadyCustody";
                    return "HavenMealPackingUnsupported";
                default:
                    return null;
            }
        }
    }
}
#endif
