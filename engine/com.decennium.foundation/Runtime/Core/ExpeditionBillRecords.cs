using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    [Flags]
    public enum ExpeditionBillCoverage
    {
        None = 0, CompleteSaleRegister = 1, DirectTaxEstablished = 2, NoMandatoryRescueOrQuarantineExpense = 4,
        NoConflictingSuperiorClaim = 8,
        Required = CompleteSaleRegister | DirectTaxEstablished | NoMandatoryRescueOrQuarantineExpense | NoConflictingSuperiorClaim
    }

    public enum ExpeditionBillStatus { Working = 1, Paused, PendingCompletion, Reconciled, Cancelled, Expired, Invalidated }

    /// <summary>The prospective Self/own-capital charter and its separately authorized bookkeeping service.</summary>
    public sealed class ExpeditionBillCharter
    {
        public string EpisodeId { get; }
        public string VersionId { get; }
        public string BillVersionId { get; }
        public string RepresentativeId { get; }
        public string BeneficiaryId => RepresentativeId;
        public IReadOnlyList<string> MemberIds { get; }
        public string CapitalOwnerId { get; }
        public string CapitalId { get; }
        public string ResponsibilityTermsId { get; }
        public string ScopeId { get; }
        public string LedgerAuthorityId { get; }
        public string DeskId { get; }
        public ExpeditionBillCoverage Coverage { get; }
        public RuleTime AcceptedAt { get; }
        public RuleTime DueAt { get; }
        public RuleTime ValidFrom { get; }
        public RuleTime AuthorizationUntil { get; }
        public RuleQuantity GrossTargetCopper { get; }
        public RuleQuantity NetTargetCopper { get; }
        public RuleQuantity ProfitAfterReservesTargetCopper { get; }
        public RuleQuantity SelfShareRate => default;

        public ExpeditionBillCharter(string episodeId, string versionId, string billVersionId, string representativeId,
            IEnumerable<string> memberIds, string capitalOwnerId, string capitalId, string responsibilityTermsId,
            string scopeId, string ledgerAuthorityId, string deskId, ExpeditionBillCoverage coverage,
            RuleTime acceptedAt, RuleTime dueAt, RuleTime validFrom, RuleTime authorizationUntil,
            RuleQuantity grossTargetCopper, RuleQuantity netTargetCopper, RuleQuantity profitAfterReservesTargetCopper)
        {
            var members = memberIds?.ToArray();
            if (new[] { episodeId, versionId, billVersionId, representativeId, capitalOwnerId, capitalId, responsibilityTermsId,
                scopeId, ledgerAuthorityId, deskId }.Any(id => !Validation.ValidId(id))
                || members == null || members.Length < 1 || members.Length > 12 || members.Any(id => !Validation.ValidId(id))
                || members.Distinct(StringComparer.Ordinal).Count() != members.Length || !members.Contains(representativeId)
                || !members.Contains(capitalOwnerId) || (coverage & ~ExpeditionBillCoverage.Required) != 0
                || dueAt <= acceptedAt || validFrom < acceptedAt || authorizationUntil <= validFrom)
                throw new ArgumentException("Invalid prospective Expedition bill charter.");
            EpisodeId = episodeId;
            VersionId = versionId;
            BillVersionId = billVersionId;
            RepresentativeId = representativeId;
            MemberIds = Array.AsReadOnly(members);
            CapitalOwnerId = capitalOwnerId;
            CapitalId = capitalId;
            ResponsibilityTermsId = responsibilityTermsId;
            ScopeId = scopeId;
            LedgerAuthorityId = ledgerAuthorityId;
            DeskId = deskId;
            Coverage = coverage;
            AcceptedAt = acceptedAt;
            DueAt = dueAt;
            ValidFrom = validFrom;
            AuthorizationUntil = authorizationUntil;
            GrossTargetCopper = grossTargetCopper;
            NetTargetCopper = netTargetCopper;
            ProfitAfterReservesTargetCopper = profitAfterReservesTargetCopper;
        }

        public bool AuthorizedAt(RuleTime now) => ValidFrom <= now && now < AuthorizationUntil;

        // Bind all prospective facts into the selected fixture fingerprint and compare them on restore.
        public string BindingKey => string.Join("|", EpisodeId, VersionId, BillVersionId, RepresentativeId,
            string.Join(",", MemberIds), CapitalOwnerId, CapitalId, ResponsibilityTermsId, ScopeId, LedgerAuthorityId,
            DeskId, ((int)Coverage).ToString(CultureInfo.InvariantCulture), AcceptedAt, DueAt, ValidFrom, AuthorizationUntil,
            GrossTargetCopper, NetTargetCopper, ProfitAfterReservesTargetCopper);
    }

    public sealed class ExpeditionBillBasis
    {
        public string CharterVersionId { get; }
        public string BillVersionId { get; }
        public string SaleId { get; }
        public long SalePaymentRevision { get; }
        public string MealId { get; }
        public long MealPaymentRevision { get; }
        public string AppraisalId { get; }
        public string ClearanceId { get; }
        public string ExemptionId { get; }
        public string SpendingAuthorityId { get; }
        public string TenderLotId { get; }
        public long CutoffRevision { get; }
        public RuleTime AccountingCutoff { get; }
        public long GrossSaleCopper { get; }
        public long MealExpenseCopper { get; }
        public long DirectTaxCopper => 0; // The admitted disposition has a verified applicable exemption.
        public long MandatoryRescueQuarantineCopper => 0; // Explicit complete coverage is required.
        public long SponsorBaseCopper => Math.Max(0, GrossSaleCopper - DirectTaxCopper - MandatoryRescueQuarantineCopper);
        public long SponsorShareCopper => 0; // The bound charter is Self at zero percent.
        public long NetExpeditionCopper => GrossSaleCopper - DirectTaxCopper - MandatoryRescueQuarantineCopper - SponsorShareCopper;
        public long AccountedCashChangeCopper => NetExpeditionCopper - MealExpenseCopper;
        public long? TrueProfitAfterReservesCopper => null;

        public ExpeditionBillBasis(string charterVersionId, string billVersionId, string saleId, long salePaymentRevision,
            string mealId, long mealPaymentRevision, string appraisalId, string clearanceId, string exemptionId,
            string spendingAuthorityId, string tenderLotId, long cutoffRevision, RuleTime accountingCutoff,
            long grossSaleCopper, long mealExpenseCopper)
        {
            if (new[] { charterVersionId, billVersionId, saleId, mealId, appraisalId, clearanceId, exemptionId,
                spendingAuthorityId, tenderLotId }.Any(id => !Validation.ValidId(id)) || saleId == mealId
                || salePaymentRevision < 1 || mealPaymentRevision <= salePaymentRevision || cutoffRevision < mealPaymentRevision
                || grossSaleCopper <= 0 || mealExpenseCopper != grossSaleCopper)
                throw new ArgumentException("Invalid Expedition bill payment references.");
            CharterVersionId = charterVersionId;
            BillVersionId = billVersionId;
            SaleId = saleId;
            SalePaymentRevision = salePaymentRevision;
            MealId = mealId;
            MealPaymentRevision = mealPaymentRevision;
            AppraisalId = appraisalId;
            ClearanceId = clearanceId;
            ExemptionId = exemptionId;
            SpendingAuthorityId = spendingAuthorityId;
            TenderLotId = tenderLotId;
            CutoffRevision = cutoffRevision;
            AccountingCutoff = accountingCutoff;
            GrossSaleCopper = grossSaleCopper;
            MealExpenseCopper = mealExpenseCopper;
        }

        public bool GrossTargetMet(ExpeditionBillCharter charter) => new RuleQuantity(GrossSaleCopper) >= charter.GrossTargetCopper;
        public bool NetTargetMet(ExpeditionBillCharter charter) => new RuleQuantity(NetExpeditionCopper) >= charter.NetTargetCopper;

        public bool MatchesReceipts(Snapshot state, ExpeditionBillCharter charter)
        {
            var sale = state.HavenSales.SingleOrDefault(x => x.Status == HavenSaleStatus.Paid);
            var meal = state.HavenMealPurchases.SingleOrDefault();
            return sale != null && meal != null && charter.Coverage == ExpeditionBillCoverage.Required
                && CharterVersionId == charter.VersionId && BillVersionId == charter.BillVersionId
                && sale.Basis.SellerId == charter.RepresentativeId && meal.Offer.CustomerId == charter.RepresentativeId
                && charter.AcceptedAt < sale.StartedAt && sale.UpdatedAt <= meal.StartedAt && meal.EndedAt <= AccountingCutoff
                && sale.Id == SaleId && sale.UpdatedRevision == SalePaymentRevision && sale.PaymentCopper == GrossSaleCopper
                && sale.Basis.AppraisalId == AppraisalId && sale.Basis.ClearanceId == ClearanceId
                && sale.Basis.ExemptionId == ExemptionId && sale.Basis.TenderLotId == TenderLotId
                && meal.Id == MealId && meal.Revision == MealPaymentRevision && meal.PaymentCopper == MealExpenseCopper
                && meal.PriorSaleId == SaleId && meal.PriorPaymentRevision == SalePaymentRevision
                && meal.Offer.SpendingClearanceId == SpendingAuthorityId && meal.Offer.TenderLotId == TenderLotId;
        }
    }

    /// <summary>At completion only title and amount need to be captured. Financial figures come from the frozen basis.</summary>
    public sealed class ExpeditionBillTenderObservation
    {
        public string OwnerId { get; }
        public RuleQuantity PhysicalCount { get; }
        public ExpeditionBillTenderObservation(string ownerId, RuleQuantity physicalCount)
        {
            if (!Validation.ValidId(ownerId) || physicalCount == default) throw new ArgumentException("Invalid traced tender.");
            OwnerId = ownerId;
            PhysicalCount = physicalCount;
        }

        public RuleQuantity RepresentativeOwnedCount(ExpeditionBillCharter charter)
            => OwnerId == charter.RepresentativeId ? PhysicalCount : default;
    }

    public sealed class ExpeditionBillRecord
    {
        public const int RequiredSeconds = 1800;
        public string Id { get; }
        public string WorkerId { get; }
        public ExpeditionBillBasis Basis { get; }
        public long StartRevision { get; }
        public long UpdatedRevision { get; }
        public RuleTime StartedAt => Basis.AccountingCutoff;
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }
        public ExpeditionBillStatus Status { get; }
        public string Reason { get; }
        public ExpeditionBillTenderObservation Report { get; }
        public bool Open => Status == ExpeditionBillStatus.Working || Status == ExpeditionBillStatus.Paused
            || Status == ExpeditionBillStatus.PendingCompletion;

        public ExpeditionBillRecord(string id, string workerId, ExpeditionBillBasis basis, long startRevision,
            long updatedRevision, RuleTime updatedAt, RuleTime labor, ExpeditionBillStatus status, string reason,
            ExpeditionBillTenderObservation report = null)
        {
            var required = new RuleTime(RequiredSeconds);
            if (!Validation.ValidId(id) || !Validation.ValidId(workerId) || basis == null
                || startRevision < 1 || startRevision - 1 != basis.CutoffRevision
                || updatedRevision < startRevision || updatedAt < basis.AccountingCutoff || labor > required
                || !Enum.IsDefined(typeof(ExpeditionBillStatus), status) || !Validation.ValidId(reason)
                || (status == ExpeditionBillStatus.Reconciled) != (report != null)
                || (status == ExpeditionBillStatus.Reconciled || status == ExpeditionBillStatus.PendingCompletion) && labor != required
                || (status == ExpeditionBillStatus.Working || status == ExpeditionBillStatus.Paused) && labor == required)
                throw new ArgumentException("Invalid Expedition bill work.");
            Id = id;
            WorkerId = workerId;
            Basis = basis;
            StartRevision = startRevision;
            UpdatedRevision = updatedRevision;
            UpdatedAt = updatedAt;
            Work = new ActiveWorkProgress(new[] { required });
            if (labor != default) Work = Work.Credit(labor);
            Status = status;
            Reason = reason;
            Report = report;
        }

        public ExpeditionBillRecord With(Snapshot state, RuleTime labor, ExpeditionBillStatus status, string reason,
            ExpeditionBillTenderObservation report = null)
            => new ExpeditionBillRecord(Id, WorkerId, Basis, StartRevision, state.Revision + 1, state.RuleClock,
                labor, status, reason, report);
    }

    public static class ExpeditionBillValidation
    {
        public const int MaxAttempts = 8;

        public static void Validate(Snapshot state)
        {
            var charter = state.ExpeditionBillCharter;
            var jobs = state.ExpeditionBills;
            if (jobs == null) throw new ArgumentException("Missing Expedition bill history.");
            if (state.SchemaVersion < Snapshot.ExpeditionBillSchema) {
                if (charter != null || jobs.Length != 0) throw new ArgumentException("Unexpected Expedition bill history.");
                return;
            }
            if (!state.TestOnly || charter == null || charter.AcceptedAt != default || !charter.MemberIds.All(id => state.Actors.Any(a => a.Id == id))
                || !state.Structures.Any(x => x.Id == charter.DeskId) || !state.PortableEquipment.Any(x => x.Id == charter.CapitalId)
                || jobs.Length > MaxAttempts || jobs.Any(x => x == null) || jobs.Select(x => x.Id).Distinct().Count() != jobs.Length
                || jobs.Count(x => x.Open || x.Status == ExpeditionBillStatus.Reconciled) > 1)
                throw new ArgumentException("Invalid Expedition bill charter or history.");
            foreach (var job in jobs) ValidateJob(state, charter, job);
        }

        private static void ValidateJob(Snapshot state, ExpeditionBillCharter charter, ExpeditionBillRecord job)
        {
            var start = state.Receipts.SingleOrDefault(x => x.Revision == job.StartRevision);
            var update = state.Receipts.SingleOrDefault(x => x.Revision == job.UpdatedRevision);
            if (start == null || update == null || job.UpdatedAt > state.RuleClock || job.WorkerId != charter.RepresentativeId
                || !charter.AuthorizedAt(job.StartedAt) || job.Open && !charter.AuthorizedAt(state.RuleClock)
                || job.Status == ExpeditionBillStatus.Expired && job.UpdatedAt != charter.AuthorizationUntil
                || job.Report != null && !charter.AuthorizedAt(job.UpdatedAt)
                || !job.Basis.MatchesReceipts(state, charter)
                || state.Work.Reservations.Any(x => x.JobId == job.Id))
                throw new ArgumentException("Invalid Expedition bill authority or payment basis.");
            var command = CommandHistory.Read(start);
            if (command.Kind != CommandKind.StartExpeditionBill || command.Actor != job.WorkerId
                || command.Target != charter.BillVersionId
                || job.Id != "expedition.bill." + job.StartRevision.ToString(CultureInfo.InvariantCulture))
                throw new ArgumentException("Expedition bill start receipt mismatch.");
            var intervals = state.Work.WorkerIntervals.Where(x => x.JobId == job.Id).ToArray();
            if (intervals.Any(x => x.WorkerId != job.WorkerId || x.Start < job.StartedAt || x.Start > job.UpdatedAt
                || x.End >= charter.AuthorizationUntil || job.Status != ExpeditionBillStatus.Working && x.End > job.UpdatedAt)
                || intervals.Count(x => x.End > state.RuleClock) != (job.Status == ExpeditionBillStatus.Working ? 1 : 0))
                throw new ArgumentException("Invalid Expedition bill labor provenance.");
            foreach (var interval in intervals) ValidateBookingReceipt(state, job, interval);
            var current = intervals.SingleOrDefault(x => x.End > state.RuleClock);
            if (current != null && Seconds(current.End) - Seconds(state.RuleClock) != Seconds(job.Work.Remaining))
                throw new ArgumentException("Expedition bill booking exceeds or truncates its remaining work.");
            var elapsed = RuleQuantity.Sum(intervals.Select(x => Seconds(x.End < state.RuleClock ? x.End : state.RuleClock) - Seconds(x.Start)));
            if (elapsed != Seconds(job.Work.Labor)) throw new ArgumentException("Expedition bill labor differs from ledger intervals.");
            if (job.Report == null) return;
            var completingCommand = CommandHistory.Read(update);
            if (intervals.Max(x => x.End) < job.UpdatedAt
                && (completingCommand.Kind != CommandKind.FinalizeExpeditionBill || completingCommand.Actor != job.WorkerId
                    || completingCommand.Target != job.Id))
                throw new ArgumentException("Delayed Expedition bill completion lacks an explicit finalization receipt.");
            // Under this profile the paid purchase transfers title of the whole tender once. Subsequent handling can change custody.
            var meal = state.HavenMealPurchases.Single();
            if (job.Report.OwnerId != meal.Offer.VendorId || job.Report.PhysicalCount != new RuleQuantity(meal.PaymentCopper))
                throw new ArgumentException("Expedition bill traced tender observation contradicts paid title history.");
        }

        private static void ValidateBookingReceipt(Snapshot state, ExpeditionBillRecord job, WorkerInterval interval)
        {
            string prefix = job.Id + ".labor.";
            if (!interval.Id.StartsWith(prefix, StringComparison.Ordinal)
                || !long.TryParse(interval.Id.Substring(prefix.Length), NumberStyles.None, CultureInfo.InvariantCulture, out long revision)
                || revision < job.StartRevision || revision > job.UpdatedRevision)
                throw new ArgumentException("Invalid Expedition bill booking identity.");
            if (revision == job.StartRevision) {
                if (interval.Start != job.StartedAt) throw new ArgumentException("Expedition bill initial booking start mismatch.");
                return;
            }
            var receipt = state.Receipts.SingleOrDefault(x => x.Revision == revision);
            if (receipt == null) throw new ArgumentException("Expedition bill booking lacks its resume receipt.");
            var command = CommandHistory.Read(receipt);
            if (command.Kind != CommandKind.ResumeExpeditionBill || command.Actor != job.WorkerId || command.Target != job.Id)
                throw new ArgumentException("Expedition bill resume receipt mismatch.");
        }

        private static RuleQuantity Seconds(RuleTime time) => new RuleQuantity(time.Numerator, time.Denominator);
    }
}
