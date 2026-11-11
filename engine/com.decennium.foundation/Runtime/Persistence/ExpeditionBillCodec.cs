using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class ExpeditionBillCodec
    {
        public static void Write(BinaryWriter writer, Snapshot state)
        {
            void Text(string value) => SnapshotCodec.WriteText(writer, value);
            void Pair(long numerator, long denominator) { writer.Write(numerator); writer.Write(denominator); }
            void Time(RuleTime value) => Pair(value.Numerator, value.Denominator);
            void Quantity(RuleQuantity value) => Pair(value.Numerator, value.Denominator);

            var charter = state.ExpeditionBillCharter;
            foreach (string value in new[] { charter.EpisodeId, charter.VersionId, charter.BillVersionId, charter.RepresentativeId,
                charter.CapitalOwnerId, charter.CapitalId, charter.ResponsibilityTermsId, charter.ScopeId,
                charter.LedgerAuthorityId, charter.DeskId }) Text(value);
            writer.Write(charter.MemberIds.Count);
            foreach (string member in charter.MemberIds) Text(member);
            writer.Write((int)charter.Coverage);
            Time(charter.AcceptedAt);
            Time(charter.DueAt);
            Time(charter.ValidFrom);
            Time(charter.AuthorizationUntil);
            Quantity(charter.GrossTargetCopper);
            Quantity(charter.NetTargetCopper);
            Quantity(charter.ProfitAfterReservesTargetCopper);

            writer.Write(state.ExpeditionBills.Length);
            foreach (var job in state.ExpeditionBills.OrderBy(x => x.StartRevision)) {
                var basis = job.Basis;
                foreach (string value in new[] { job.Id, job.WorkerId, basis.CharterVersionId, basis.BillVersionId,
                    basis.SaleId, basis.MealId, basis.AppraisalId, basis.ClearanceId, basis.ExemptionId,
                    basis.SpendingAuthorityId, basis.TenderLotId }) Text(value);
                writer.Write(basis.SalePaymentRevision);
                writer.Write(basis.MealPaymentRevision);
                writer.Write(basis.CutoffRevision);
                Time(basis.AccountingCutoff);
                writer.Write(basis.GrossSaleCopper);
                writer.Write(basis.MealExpenseCopper);
                writer.Write(job.StartRevision);
                writer.Write(job.UpdatedRevision);
                Time(job.UpdatedAt);
                Time(job.Work.Labor);
                writer.Write((int)job.Status);
                Text(job.Reason);
                if (job.Report != null) {
                    Text(job.Report.OwnerId);
                    Quantity(job.Report.PhysicalCount);
                }
            }
        }

        public static void Read(BinaryReader reader, Snapshot state)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
            RuleQuantity Quantity() => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());

            string episode = Text(), version = Text(), bill = Text(), representative = Text(), capitalOwner = Text(),
                capital = Text(), terms = Text(), scope = Text(), authority = Text(), desk = Text();
            int memberCount = SnapshotCodec.ReadCount(reader, 12);
            var members = Enumerable.Range(0, memberCount).Select(_ => Text()).ToArray();
            state.ExpeditionBillCharter = new ExpeditionBillCharter(episode, version, bill, representative, members,
                capitalOwner, capital, terms, scope, authority, desk, (ExpeditionBillCoverage)reader.ReadInt32(),
                Time(), Time(), Time(), Time(), Quantity(), Quantity(), Quantity());

            var jobs = new ExpeditionBillRecord[SnapshotCodec.ReadCount(reader, ExpeditionBillValidation.MaxAttempts)];
            for (int i = 0; i < jobs.Length; i++) {
                string id = Text(), worker = Text(), charterVersion = Text(), billVersion = Text(),
                    sale = Text(), meal = Text(), appraisal = Text(), clearance = Text(), exemption = Text(),
                    spendingAuthority = Text(), tender = Text();
                long saleRevision = reader.ReadInt64(), mealRevision = reader.ReadInt64(), cutoffRevision = reader.ReadInt64();
                var basis = new ExpeditionBillBasis(charterVersion, billVersion, sale, saleRevision, meal, mealRevision,
                    appraisal, clearance, exemption, spendingAuthority, tender, cutoffRevision, Time(), reader.ReadInt64(), reader.ReadInt64());
                long start = reader.ReadInt64(), updated = reader.ReadInt64();
                var updatedAt = Time();
                var labor = Time();
                var status = (ExpeditionBillStatus)reader.ReadInt32();
                string reason = Text();
                var report = status == ExpeditionBillStatus.Reconciled ? new ExpeditionBillTenderObservation(Text(), Quantity()) : null;
                jobs[i] = new ExpeditionBillRecord(id, worker, basis, start, updated, updatedAt, labor, status, reason, report);
            }
            state.ExpeditionBills = jobs;
        }
    }
}
