using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class HavenSaleCodec
    {
        public static void Write(BinaryWriter writer, Snapshot state)
        {
            writer.Write(state.HavenSales.Length);
            foreach (var sale in state.HavenSales.OrderBy(x => x.StartRevision)) {
                var basis = sale.Basis;
                foreach (string id in new[] { sale.Id, basis.OfferId, basis.OfferVersionId, basis.SellerId, basis.BuyerId,
                    basis.CounterId, basis.MandateId, basis.ClearanceId, basis.ExemptionId, basis.ExemptionIssuerId,
                    basis.JurisdictionId, basis.AppraisalId, basis.GoodsLotId, basis.TenderLotId, basis.CurrencyUnitId, basis.MintId })
                    SnapshotCodec.WriteText(writer, id);
                WritePair(writer, basis.GoodsQuantity.Numerator, basis.GoodsQuantity.Denominator);
                writer.Write(basis.TenderCount);
                WritePair(writer, basis.ExactQuoteCopper.Numerator, basis.ExactQuoteCopper.Denominator);
                WriteTime(writer, basis.ValidFrom);
                WriteTime(writer, basis.ExpiresAt);
                writer.Write(sale.StartRevision);
                writer.Write(sale.UpdatedRevision);
                WriteTime(writer, sale.StartedAt);
                WriteTime(writer, sale.UpdatedAt);
                WriteTime(writer, sale.Work.Labor);
                writer.Write((int)sale.Status);
                SnapshotCodec.WriteText(writer, sale.Reason);
                writer.Write(sale.PaymentCopper.HasValue);
                if (sale.PaymentCopper.HasValue) writer.Write(sale.PaymentCopper.Value);
            }
        }

        public static void Read(BinaryReader reader, Snapshot state)
        {
            var sales = new HavenSaleRecord[SnapshotCodec.ReadCount(reader, HavenSaleValidation.MaxRecords)];
            for (int i = 0; i < sales.Length; i++) {
                string Text() => SnapshotCodec.ReadText(reader);
                string id = Text();
                var basis = new HavenSaleBasis(Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text(),
                    Text(), Text(), Text(), Text(), Text(), Text(), Text(), ReadQuantity(reader), reader.ReadInt64(),
                    ReadQuantity(reader), ReadTime(reader), ReadTime(reader));
                long started = reader.ReadInt64(), updated = reader.ReadInt64();
                var start = ReadTime(reader);
                var end = ReadTime(reader);
                var labor = ReadTime(reader);
                var status = (HavenSaleStatus)reader.ReadInt32();
                string reason = Text();
                long? payment = SnapshotCodec.ReadBool(reader) ? reader.ReadInt64() : (long?)null;
                sales[i] = new HavenSaleRecord(id, basis, started, updated, start, end, labor, status, reason, payment);
            }
            state.HavenSales = sales;
        }

        private static void WritePair(BinaryWriter writer, long numerator, long denominator)
        {
            writer.Write(numerator);
            writer.Write(denominator);
        }

        private static void WriteTime(BinaryWriter writer, RuleTime time) => WritePair(writer, time.Numerator, time.Denominator);
        private static RuleTime ReadTime(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
        private static RuleQuantity ReadQuantity(BinaryReader reader) => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());
    }
}
