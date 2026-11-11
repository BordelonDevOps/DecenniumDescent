using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum HavenSaleStatus { Working=1, Paused, PendingSettlement, Paid, Cancelled, Expired, Invalidated }

    public sealed class HavenSaleBasis
    {
        public string OfferId { get; }
        public string OfferVersionId { get; }
        public string SellerId { get; }
        public string BuyerId { get; }
        public string CounterId { get; }
        public string MandateId { get; }
        public string ClearanceId { get; }
        public string ExemptionId { get; }
        public string ExemptionIssuerId { get; }
        public string JurisdictionId { get; }
        public string AppraisalId { get; }
        public string GoodsLotId { get; }
        public string TenderLotId { get; }
        public string CurrencyUnitId { get; }
        public string MintId { get; }
        public RuleQuantity GoodsQuantity { get; }
        public long TenderCount { get; }
        public RuleQuantity ExactQuoteCopper { get; }
        public RuleTime ValidFrom { get; }
        public RuleTime ExpiresAt { get; }

        public HavenSaleBasis(string offerId, string offerVersionId, string sellerId, string buyerId, string counterId,
            string mandateId, string clearanceId, string exemptionId, string exemptionIssuerId, string jurisdictionId,
            string appraisalId, string goodsLotId, string tenderLotId, string currencyUnitId, string mintId,
            RuleQuantity goodsQuantity, long tenderCount, RuleQuantity exactQuoteCopper, RuleTime validFrom, RuleTime expiresAt)
        {
            if (new[] { offerId, offerVersionId, sellerId, buyerId, counterId, mandateId, clearanceId, exemptionId,
                exemptionIssuerId, jurisdictionId, appraisalId, goodsLotId, tenderLotId, currencyUnitId, mintId }
                .Any(id => !Validation.ValidId(id)) || sellerId == buyerId || goodsLotId == tenderLotId
                || goodsQuantity == default || tenderCount < 1
                || exactQuoteCopper.Numerator / exactQuoteCopper.Denominator != tenderCount || expiresAt <= validFrom)
                throw new ArgumentException("Invalid whole-lot sale agreement or final copper rounding.");
            OfferId = offerId;
            OfferVersionId = offerVersionId;
            SellerId = sellerId;
            BuyerId = buyerId;
            CounterId = counterId;
            MandateId = mandateId;
            ClearanceId = clearanceId;
            ExemptionId = exemptionId;
            ExemptionIssuerId = exemptionIssuerId;
            JurisdictionId = jurisdictionId;
            AppraisalId = appraisalId;
            GoodsLotId = goodsLotId;
            TenderLotId = tenderLotId;
            CurrencyUnitId = currencyUnitId;
            MintId = mintId;
            GoodsQuantity = goodsQuantity;
            TenderCount = tenderCount;
            ExactQuoteCopper = exactQuoteCopper;
            ValidFrom = validFrom;
            ExpiresAt = expiresAt;
        }

        public bool ValidAt(RuleTime now) => ValidFrom <= now && now < ExpiresAt;
    }

    public sealed class HavenSaleRecord
    {
        public const int RequiredSeconds = 1800;
        public string Id { get; }
        public HavenSaleBasis Basis { get; }
        public long StartRevision { get; }
        public long UpdatedRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }
        public HavenSaleStatus Status { get; }
        public string Reason { get; }
        public long? PaymentCopper { get; }
        public string GoodsClaimId => Id + ".goods";
        public string TenderClaimId => Id + ".tender";
        public bool Open => Status == HavenSaleStatus.Working || Status == HavenSaleStatus.Paused
            || Status == HavenSaleStatus.PendingSettlement;

        public HavenSaleRecord(string id, HavenSaleBasis basis, long startRevision, long updatedRevision, RuleTime startedAt,
            RuleTime updatedAt, RuleTime labor, HavenSaleStatus status, string reason, long? paymentCopper)
        {
            var required = new RuleTime(RequiredSeconds);
            if (!Validation.ValidId(id) || basis == null || startRevision < 1 || updatedRevision < startRevision
                || updatedAt < startedAt || !basis.ValidAt(startedAt) || labor > required
                || !Enum.IsDefined(typeof(HavenSaleStatus), status) || !Validation.ValidId(reason)
                || (status == HavenSaleStatus.Paid) != paymentCopper.HasValue
                || (status == HavenSaleStatus.Paid || status == HavenSaleStatus.PendingSettlement) && labor != required
                || (status == HavenSaleStatus.Working || status == HavenSaleStatus.Paused) && labor == required
                || status == HavenSaleStatus.Expired && updatedAt != basis.ExpiresAt
                || paymentCopper.HasValue && (paymentCopper.Value != basis.TenderCount || !basis.ValidAt(updatedAt)))
                throw new ArgumentException("Invalid timed Haven sale or payment.");
            Id = id;
            Basis = basis;
            StartRevision = startRevision;
            UpdatedRevision = updatedRevision;
            StartedAt = startedAt;
            UpdatedAt = updatedAt;
            Work = new ActiveWorkProgress(new[] { required });
            if (labor > default(RuleTime)) Work = Work.Credit(labor);
            Status = status;
            Reason = reason;
            PaymentCopper = paymentCopper;
        }

        public HavenSaleRecord With(Snapshot state, RuleTime labor, HavenSaleStatus status, string reason)
            => new HavenSaleRecord(Id, Basis, StartRevision, state.Revision + 1, StartedAt, state.RuleClock, labor, status,
                reason, status == HavenSaleStatus.Paid ? Basis.TenderCount : (long?)null);
    }

    public static class HavenSaleValidation
    {
        public const int MaxRecords = 8;

        public static void Validate(Snapshot s)
        {
            var sales = s.HavenSales;
            if (sales == null || sales.Length > MaxRecords || sales.Any(x => x == null)
                || sales.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != sales.Length
                || s.SchemaVersion != Snapshot.HavenSaleSchema && sales.Length != 0
                || sales.Count(x => x.Open) > 1 || sales.Count(x => x.Status == HavenSaleStatus.Paid) > 1)
                throw new ArgumentException("Invalid Haven sale history.");
            foreach (var sale in sales) ValidateSale(s, sale);
        }

        private static void ValidateSale(Snapshot s, HavenSaleRecord sale)
        {
            var basis = sale.Basis;
            var start = s.Receipts.SingleOrDefault(x => x.Revision == sale.StartRevision);
            var appraisal = s.HavenAppraisals.SingleOrDefault(x => x.Id == basis.AppraisalId);
            if (start == null || !s.Receipts.Any(x => x.Revision == sale.UpdatedRevision) || sale.UpdatedAt > s.RuleClock
                || sale.Open && !basis.ValidAt(s.RuleClock) || appraisal?.Status != HavenAppraisalStatus.Completed
                || appraisal.UpdatedRevision >= sale.StartRevision || appraisal.Basis.UnitId != basis.GoodsLotId
                || appraisal.Basis.OwnerId != basis.SellerId || appraisal.Basis.Quantity != basis.GoodsQuantity
                || !s.Actors.Any(x => x.Id == basis.SellerId) || !s.Actors.Any(x => x.Id == basis.BuyerId)
                || !s.Structures.Any(x => x.Id == basis.CounterId))
                throw new ArgumentException("Invalid Haven sale provenance.");
            var command = CommandHistory.Read(start);
            if (command.Kind != CommandKind.StartHavenSale || command.Actor != basis.SellerId || command.Target != basis.OfferVersionId)
                throw new ArgumentException("Haven sale start receipt mismatch.");
            if (s.Work.Reservations.Count(x => x.JobId == sale.Id) != 2)
                throw new ArgumentException("Haven sale requires two nonconsuming reservations.");
            ValidateClaim(s, sale, sale.GoodsClaimId, basis.GoodsLotId, basis.GoodsQuantity);
            ValidateClaim(s, sale, sale.TenderClaimId, basis.TenderLotId, new RuleQuantity(basis.TenderCount));
            ValidateLabor(s, sale);
            if (sale.Status == HavenSaleStatus.Paid) {
                ValidateDelivery(s, basis.GoodsLotId, "mass-pound", basis.GoodsQuantity, basis.BuyerId);
                ValidateDelivery(s, basis.TenderLotId, basis.CurrencyUnitId, new RuleQuantity(basis.TenderCount), basis.SellerId);
            }
        }

        private static void ValidateDelivery(Snapshot s, string lotId, string unit, RuleQuantity quantity, string owner)
        {
            if (!s.Work.Lots.Any(x => x.Id == lotId && x.UnitId == unit && x.Amount == quantity)
                || !s.InventoryLots.Any(x => x.LotId == lotId && x.OwnerId == owner && x.CreatedAmount == quantity && x.ParentId == "")
                || !s.PortableEquipment.Any(x => x.Id == lotId && x.LinkedId == lotId && x.OwnerId == owner))
                throw new ArgumentException("Paid Haven sale lacks its bilateral stock and title transition.");
        }

        private static void ValidateClaim(Snapshot s, HavenSaleRecord sale, string id, string lot, RuleQuantity amount)
        {
            var claim = s.Work.Reservations.SingleOrDefault(x => x.Id == id);
            if (claim == null || claim.JobId != sale.Id || claim.LotId != lot || claim.Amount != amount
                || claim.ConsumedAmount != default || claim.ReleasedAmount != (sale.Open ? default : claim.Amount))
                throw new ArgumentException("Haven sale claim mismatch.");
        }

        private static void ValidateLabor(Snapshot s, HavenSaleRecord sale)
        {
            var intervals = s.Work.WorkerIntervals.Where(x => x.JobId == sale.Id).ToArray();
            var seller = intervals.Where(x => x.WorkerId == sale.Basis.SellerId).OrderBy(x => x.Start).ToArray();
            var buyer = intervals.Where(x => x.WorkerId == sale.Basis.BuyerId).OrderBy(x => x.Start).ToArray();
            if (seller.Length + buyer.Length != intervals.Length || !seller.Select(x => (x.Start, x.End)).SequenceEqual(buyer.Select(x => (x.Start, x.End)))
                || seller.Any(x => x.Start < sale.StartedAt || x.Start > s.RuleClock || !sale.Open && x.End > sale.UpdatedAt)
                || seller.Count(x => x.End > s.RuleClock) != (sale.Status == HavenSaleStatus.Working ? 1 : 0))
                throw new ArgumentException("Invalid Haven sale paired labor provenance.");
            var elapsed = RuleQuantity.Sum(seller.Select(x => ExactTime(x.End < s.RuleClock ? x.End : s.RuleClock) - ExactTime(x.Start)));
            if (elapsed != ExactTime(sale.Work.Labor)) throw new ArgumentException("Haven sale labor differs from its ledger intervals.");
        }

        private static RuleQuantity ExactTime(RuleTime value) => new RuleQuantity(value.Numerator, value.Denominator);
    }
}
