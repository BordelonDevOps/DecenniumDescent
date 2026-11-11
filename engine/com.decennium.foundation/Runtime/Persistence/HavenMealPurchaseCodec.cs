using System.IO;

namespace Decennium.Foundation
{
    internal static class HavenMealPurchaseCodec
    {
        public static void Write(BinaryWriter writer, Snapshot state)
        {
            writer.Write(state.HavenMealPurchases.Length);
            foreach (var purchase in state.HavenMealPurchases) {
                var offer = purchase.Offer;
                foreach (string id in new[] { purchase.Id, purchase.PriorSaleId, offer.VersionId, offer.CustomerId,
                    offer.VendorId, offer.CounterId, offer.ServingSurfaceId, offer.VendorMandateId, offer.StockTitleId,
                    offer.SpendingClearanceId, offer.MealLotId, offer.TenderLotId, offer.CurrencyUnitId })
                    SnapshotCodec.WriteText(writer, id);
                WritePair(writer, offer.ServingPounds.Numerator, offer.ServingPounds.Denominator);
                WritePair(writer, offer.ExactQuoteCopper.Numerator, offer.ExactQuoteCopper.Denominator);
                WriteTime(writer, offer.ValidFrom);
                WriteTime(writer, offer.ExpiresAt);
                WriteTime(writer, offer.FreshUntil);
                writer.Write(purchase.PriorPaymentRevision);
                writer.Write(purchase.Revision);
                WriteTime(writer, purchase.StartedAt);
                WriteTime(writer, purchase.EndedAt);
                writer.Write(purchase.PaymentCopper);
            }
        }

        public static void Read(BinaryReader reader, Snapshot state)
        {
            var purchases = new HavenMealPurchaseRecord[SnapshotCodec.ReadCount(reader, 1)];
            for (int i = 0; i < purchases.Length; i++) {
                string Text() => SnapshotCodec.ReadText(reader);
                string id = Text();
                string prior = Text();
                var offer = new HavenMealOffer(Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text(),
                    Text(), Text(), ReadQuantity(reader), ReadQuantity(reader), ReadTime(reader), ReadTime(reader), ReadTime(reader));
                purchases[i] = new HavenMealPurchaseRecord(id, offer, prior, reader.ReadInt64(), reader.ReadInt64(),
                    ReadTime(reader), ReadTime(reader), reader.ReadInt64());
            }
            state.HavenMealPurchases = purchases;
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
