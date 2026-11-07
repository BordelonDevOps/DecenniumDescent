using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ExpeditionRouteTravelCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);

        public static void Write(BinaryWriter writer, Snapshot snapshot)
        {
            writer.Write(snapshot.RouteTravels.Length);
            foreach (var travel in snapshot.RouteTravels.OrderBy(x => x.StartedRevision))
            {
                WriteText(writer, travel.RouteId); WriteText(writer, travel.TravelerId); writer.Write(travel.StartedRevision);
                WriteQuantity(writer, travel.SegmentStartProgress); WriteQuantity(writer, travel.SegmentProgressAward);
                WriteQuantity(writer, travel.Progress); writer.Write(travel.NominalEffort.Numerator); writer.Write(travel.NominalEffort.Denominator);
                writer.Write((int)travel.StartingMapping); writer.Write((int)travel.Status);
            }
        }

        public static void Read(BinaryReader reader, Snapshot snapshot)
        {
            int count = ReadCount(reader, ExpeditionRouteTravelValidation.MaxRecords);
            snapshot.RouteTravels = new ExpeditionRouteTravelRecord[count];
            for (int i = 0; i < count; i++)
                snapshot.RouteTravels[i] = new ExpeditionRouteTravelRecord(ReadText(reader), ReadText(reader), reader.ReadInt64(),
                    ReadQuantity(reader), ReadQuantity(reader), ReadQuantity(reader), new RuleTime(reader.ReadInt64(), reader.ReadInt64()),
                    (ExpeditionRouteMapping)reader.ReadInt32(), (ExpeditionRouteTravelStatus)reader.ReadInt32());
        }

        private static void WriteQuantity(BinaryWriter writer, RuleQuantity value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }
        private static RuleQuantity ReadQuantity(BinaryReader reader) => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());
        private static int ReadCount(BinaryReader reader, int maximum)
        { int count = reader.ReadInt32(); if (count < 0 || count > maximum) throw new InvalidDataException("Invalid route travel count."); return count; }
        private static void WriteText(BinaryWriter writer, string value)
        { byte[] bytes = Utf8.GetBytes(value); writer.Write(bytes.Length); writer.Write(bytes); }
        private static string ReadText(BinaryReader reader)
        {
            int length = ReadCount(reader, 96); byte[] bytes = reader.ReadBytes(length);
            if (bytes.Length != length) throw new EndOfStreamException(); return Utf8.GetString(bytes);
        }
    }
}
