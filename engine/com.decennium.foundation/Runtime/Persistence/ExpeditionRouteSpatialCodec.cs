using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ExpeditionRouteSpatialCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        public static void Write(BinaryWriter writer, Snapshot snapshot)
        {
            writer.Write(snapshot.RouteTravelSpatial.Length);
            foreach (var value in snapshot.RouteTravelSpatial.OrderBy(x => x.TravelStartedRevision))
            {
                WriteText(writer, value.RouteId); WriteText(writer, value.TravelerId);
                writer.Write(value.TravelStartedRevision);
                WriteQuantity(writer, value.X); WriteQuantity(writer, value.Y); writer.Write(value.Detached);
            }
        }
        public static void Read(BinaryReader reader, Snapshot snapshot)
        {
            int count = ReadCount(reader, ExpeditionRouteTravelValidation.MaxRecords);
            snapshot.RouteTravelSpatial = new ExpeditionRouteSpatialRecord[count];
            for (int i = 0; i < count; i++)
                snapshot.RouteTravelSpatial[i] = new ExpeditionRouteSpatialRecord(ReadText(reader), ReadText(reader),
                    reader.ReadInt64(), ReadQuantity(reader), ReadQuantity(reader), ReadBool(reader));
        }
        private static void WriteQuantity(BinaryWriter writer, RuleQuantity value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }
        private static RuleQuantity ReadQuantity(BinaryReader reader) => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());
        private static int ReadCount(BinaryReader reader, int maximum)
        { int count = reader.ReadInt32(); if (count < 0 || count > maximum) throw new InvalidDataException("Invalid route spatial count."); return count; }
        private static bool ReadBool(BinaryReader reader)
        { byte value = reader.ReadByte(); if (value > 1) throw new InvalidDataException("Invalid route spatial boolean."); return value == 1; }
        private static void WriteText(BinaryWriter writer, string value)
        { byte[] bytes = Utf8.GetBytes(value); writer.Write(bytes.Length); writer.Write(bytes); }
        private static string ReadText(BinaryReader reader)
        {
            int length = ReadCount(reader, 96); byte[] bytes = reader.ReadBytes(length);
            if (bytes.Length != length) throw new EndOfStreamException(); return Utf8.GetString(bytes);
        }
    }
}
