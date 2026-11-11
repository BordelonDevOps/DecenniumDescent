using System;
using System.Linq;

namespace Decennium.Foundation
{
    public sealed class HavenMealOffer
    {
        public string VersionId { get; }
        public string CustomerId { get; }
        public string VendorId { get; }
        public string CounterId { get; }
        public string ServingSurfaceId { get; }
        public string VendorMandateId { get; }
        public string StockTitleId { get; }
        public string SpendingClearanceId { get; }
        public string MealLotId { get; }
        public string TenderLotId { get; }
        public string CurrencyUnitId { get; }
        public RuleQuantity ServingPounds { get; }
        public RuleQuantity ExactQuoteCopper { get; }
        public RuleTime ValidFrom { get; }
        public RuleTime ExpiresAt { get; }
        public RuleTime FreshUntil { get; }

        public HavenMealOffer(string versionId, string customerId, string vendorId, string counterId, string servingSurfaceId,
            string vendorMandateId, string stockTitleId, string spendingClearanceId, string mealLotId, string tenderLotId,
            string currencyUnitId, RuleQuantity servingPounds, RuleQuantity exactQuoteCopper, RuleTime validFrom, RuleTime expiresAt,
            RuleTime freshUntil)
        {
            if (new[] { versionId, customerId, vendorId, counterId, servingSurfaceId, vendorMandateId, stockTitleId,
                spendingClearanceId, mealLotId, tenderLotId, currencyUnitId }.Any(id => !Validation.ValidId(id))
                || customerId == vendorId || mealLotId == tenderLotId || servingPounds == default || exactQuoteCopper == default
                || expiresAt <= validFrom || freshUntil == default)
                throw new ArgumentException("Invalid funded Haven meal offer.");
            VersionId = versionId;
            CustomerId = customerId;
            VendorId = vendorId;
            CounterId = counterId;
            ServingSurfaceId = servingSurfaceId;
            VendorMandateId = vendorMandateId;
            StockTitleId = stockTitleId;
            SpendingClearanceId = spendingClearanceId;
            MealLotId = mealLotId;
            TenderLotId = tenderLotId;
            CurrencyUnitId = currencyUnitId;
            ServingPounds = servingPounds;
            ExactQuoteCopper = exactQuoteCopper;
            ValidFrom = validFrom;
            ExpiresAt = expiresAt;
            FreshUntil = freshUntil;
        }

        public long PaymentCopper => checked(ExactQuoteCopper.Numerator / ExactQuoteCopper.Denominator
            + (ExactQuoteCopper.Numerator % ExactQuoteCopper.Denominator == 0 ? 0 : 1));
    }

    public sealed class HavenMealPurchaseRecord
    {
        public string Id { get; }
        public HavenMealOffer Offer { get; }
        public string PriorSaleId { get; }
        public long PriorPaymentRevision { get; }
        public long Revision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime EndedAt { get; }
        public long PaymentCopper { get; }
        public string FoodClaimId => Id + ".food";
        public string TenderClaimId => Id + ".tender";

        public HavenMealPurchaseRecord(string id, HavenMealOffer offer, string priorSaleId, long priorPaymentRevision,
            long revision, RuleTime startedAt, RuleTime endedAt, long paymentCopper)
        {
            if (!Validation.ValidId(id) || offer == null || !Validation.ValidId(priorSaleId) || priorPaymentRevision < 1
                || revision <= priorPaymentRevision || endedAt != startedAt.AddSeconds(1) || startedAt < offer.ValidFrom
                || endedAt >= offer.ExpiresAt || endedAt >= offer.FreshUntil || paymentCopper != offer.PaymentCopper)
                throw new ArgumentException("Invalid completed Haven meal purchase.");
            Id = id;
            Offer = offer;
            PriorSaleId = priorSaleId;
            PriorPaymentRevision = priorPaymentRevision;
            Revision = revision;
            StartedAt = startedAt;
            EndedAt = endedAt;
            PaymentCopper = paymentCopper;
        }
    }

    public static class HavenMealPurchaseValidation
    {
        public static void Validate(Snapshot s)
        {
            if (s.HavenMealPurchases == null || s.HavenMealPurchases.Length > 1
                || s.SchemaVersion < Snapshot.HavenMealSchema && s.HavenMealPurchases.Length != 0)
                throw new ArgumentException("Invalid Haven meal purchase history.");
            foreach (var purchase in s.HavenMealPurchases) ValidatePurchase(s, purchase);
        }

        private static void ValidatePurchase(Snapshot s, HavenMealPurchaseRecord purchase)
        {
            if (purchase == null) throw new ArgumentException("Missing Haven meal purchase.");
            var offer = purchase.Offer;
            var predecessor = s.HavenSales.SingleOrDefault(x => x.Id == purchase.PriorSaleId && x.Status == HavenSaleStatus.Paid);
            var receipt = s.Receipts.SingleOrDefault(x => x.Revision == purchase.Revision);
            if (receipt == null || predecessor == null || predecessor.UpdatedRevision != purchase.PriorPaymentRevision
                || predecessor.UpdatedAt > purchase.StartedAt || purchase.EndedAt > s.RuleClock
                || predecessor.Basis.SellerId != offer.CustomerId || predecessor.Basis.BuyerId != offer.VendorId
                || predecessor.Basis.TenderLotId != offer.TenderLotId || predecessor.Basis.CurrencyUnitId != offer.CurrencyUnitId
                || predecessor.PaymentCopper != purchase.PaymentCopper)
                throw new ArgumentException("Invalid causal tender history for Haven meal purchase.");
            var command = CommandHistory.Read(receipt);
            if (command.Kind != CommandKind.PurchaseHavenMeal || command.Actor != offer.CustomerId || command.Target != offer.VersionId)
                throw new ArgumentException("Haven meal purchase receipt mismatch.");
            if (!s.InventoryLots.Any(x => x.LotId == offer.MealLotId && x.ParentId == "" && x.OwnerId == offer.CustomerId
                && x.CreatedAmount == offer.ServingPounds && x.FreshUntil == offer.FreshUntil && x.Nutrition == NutritionKind.FoodPounds)
                || !s.PortableEquipment.Any(x => x.Id == offer.MealLotId && x.LinkedId == offer.MealLotId && x.OwnerId == offer.CustomerId)
                || !s.Structures.Any(x => x.Id == offer.ServingSurfaceId))
                throw new ArgumentException("Haven meal receipt lacks its original stock and delivery basis.");
            var intervals = s.Work.WorkerIntervals.Where(x => x.JobId == purchase.Id).ToArray();
            if (intervals.Length != 2 || intervals.Any(x => x.Start != purchase.StartedAt || x.End != purchase.EndedAt)
                || !intervals.Any(x => x.WorkerId == offer.CustomerId) || !intervals.Any(x => x.WorkerId == offer.VendorId))
                throw new ArgumentException("Haven meal purchase lacks concurrent one-second work.");
            if (s.Work.Reservations.Count(x => x.JobId == purchase.Id) != 2)
                throw new ArgumentException("Haven meal purchase lacks its two physical claims.");
            ValidateClaim(s, purchase, purchase.FoodClaimId, offer.MealLotId, offer.ServingPounds);
            ValidateClaim(s, purchase, purchase.TenderClaimId, offer.TenderLotId, new RuleQuantity(purchase.PaymentCopper));
        }

        private static void ValidateClaim(Snapshot s, HavenMealPurchaseRecord purchase, string claimId, string lotId, RuleQuantity amount)
        {
            if (!s.Work.Reservations.Any(x => x.Id == claimId && x.JobId == purchase.Id && x.LotId == lotId
                && x.Amount == amount && x.ConsumedAmount == default && x.ReleasedAmount == amount))
                throw new ArgumentException("Invalid nonconsuming Haven meal purchase claim.");
        }
    }
}
