using System;
using System.IO;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Schema51 append-only encoding for per-observer knowledge and tactical check audits.</summary>
    internal static class ObservationCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);

        internal static void Write(BinaryWriter writer, Snapshot snapshot)
        {
            writer.Write(snapshot.ObservationMapWidth); writer.Write(snapshot.ObservationMapHeight);
            writer.Write(snapshot.ObservationCells.Length);
            foreach (var x in snapshot.ObservationCells)
            {
                writer.Write(x.X); writer.Write(x.Y); writer.Write(x.BlocksSight); writer.Write(x.BlocksEffect);
                writer.Write(x.BlocksMovement); writer.Write(x.Solid);
            }
            writer.Write(snapshot.ObservationProfiles.Length);
            foreach (var x in snapshot.ObservationProfiles)
            { WriteText(writer, x.ActorId); writer.Write(x.SightRangeFeet); writer.Write(x.SearchRangeFeet); }
            writer.Write(snapshot.ObservationActions.Length);
            foreach (var x in snapshot.ObservationActions)
            {
                WriteText(writer, x.Id); WriteText(writer, x.ActorId); WriteText(writer, x.TargetId);
                writer.Write((int)x.Kind); writer.Write((int)x.Outcome); WriteTime(writer, x.At); writer.Write(x.Revision);
                WriteQuantity(writer, x.X); WriteQuantity(writer, x.Y);
                writer.Write(x.First); writer.Write(x.Second); writer.Write(x.Natural); writer.Write(x.Modifier); writer.Write(x.Total);
                writer.Write((int)x.Selection); writer.Write(x.RandomBefore); writer.Write(x.RandomAfter); writer.Write(x.WordsConsumed);
            }
            writer.Write(snapshot.ObservationHideResults.Length);
            foreach (var x in snapshot.ObservationHideResults)
            {
                WriteText(writer, x.AttemptId); WriteText(writer, x.ObserverId);
                WriteQuantity(writer, x.ObserverX); WriteQuantity(writer, x.ObserverY); writer.Write(x.Dc);
                writer.Write((int)x.Degree); writer.Write(x.HiddenEstablished);
            }
            writer.Write(snapshot.ObserverKnowledge.Length);
            foreach (var x in snapshot.ObserverKnowledge)
            {
                WriteText(writer, x.ObserverId); WriteText(writer, x.TargetId); writer.Write(x.HasLastKnownLocation);
                writer.Write(x.CurrentLocationKnown); WriteQuantity(writer, x.LastKnownX); WriteQuantity(writer, x.LastKnownY);
                writer.Write((int)x.Evidence); WriteTime(writer, x.EvidenceAt); writer.Write(x.EvidenceRevision);
                WriteText(writer, x.HiddenAttemptId); WriteText(writer, x.RevealedInvisibleEpisodeId);
            }
        }

        internal static void Read(BinaryReader reader, Snapshot snapshot)
        {
            snapshot.ObservationMapWidth = reader.ReadInt32(); snapshot.ObservationMapHeight = reader.ReadInt32();
            snapshot.ObservationCells = new ObservationMapCellRecord[ReadCount(reader, ObservationValidation.MaxCells)];
            for (int i = 0; i < snapshot.ObservationCells.Length; i++)
                snapshot.ObservationCells[i] = new ObservationMapCellRecord(reader.ReadInt32(), reader.ReadInt32(),
                    ReadBool(reader), ReadBool(reader), ReadBool(reader), ReadBool(reader));
            snapshot.ObservationProfiles = new ObservationProfileRecord[ReadCount(reader, ObservationValidation.MaxProfiles)];
            for (int i = 0; i < snapshot.ObservationProfiles.Length; i++)
                snapshot.ObservationProfiles[i] = new ObservationProfileRecord(ReadText(reader), reader.ReadInt64(), reader.ReadInt64());
            snapshot.ObservationActions = new ObservationActionRecord[ReadCount(reader, ObservationValidation.MaxAttempts)];
            for (int i = 0; i < snapshot.ObservationActions.Length; i++)
                snapshot.ObservationActions[i] = new ObservationActionRecord(ReadText(reader), ReadText(reader), ReadText(reader),
                    (ObservationActionKind)reader.ReadInt32(), (ObservationActionOutcome)reader.ReadInt32(), ReadTime(reader), reader.ReadInt64(),
                    ReadQuantity(reader), ReadQuantity(reader), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(),
                    reader.ReadInt32(), reader.ReadInt64(), (ObservationDieSelection)reader.ReadInt32(), reader.ReadUInt32(),
                    reader.ReadUInt32(), reader.ReadInt64());
            snapshot.ObservationHideResults = new ObservationHideResultRecord[ReadCount(reader, ObservationValidation.MaxHideResults)];
            for (int i = 0; i < snapshot.ObservationHideResults.Length; i++)
                snapshot.ObservationHideResults[i] = new ObservationHideResultRecord(ReadText(reader), ReadText(reader),
                    ReadQuantity(reader), ReadQuantity(reader), reader.ReadInt32(),
                    (ObservationTaskDegree)reader.ReadInt32(), ReadBool(reader));
            snapshot.ObserverKnowledge = new ObserverKnowledgeRecord[ReadCount(reader, ObservationValidation.MaxKnowledgePairs)];
            for (int i = 0; i < snapshot.ObserverKnowledge.Length; i++)
                snapshot.ObserverKnowledge[i] = new ObserverKnowledgeRecord(ReadText(reader), ReadText(reader), ReadBool(reader), ReadBool(reader),
                    ReadQuantity(reader), ReadQuantity(reader), (ObservationEvidenceKind)reader.ReadInt32(), ReadTime(reader), reader.ReadInt64(),
                    ReadText(reader), ReadText(reader));
        }

        private static void WriteQuantity(BinaryWriter writer, RuleQuantity value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }
        private static RuleQuantity ReadQuantity(BinaryReader reader) => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());
        private static void WriteTime(BinaryWriter writer, RuleTime value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }
        private static RuleTime ReadTime(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
        private static void WriteText(BinaryWriter writer, string value)
        {
            byte[] bytes = Utf8.GetBytes(value);
            if (bytes.Length > 512) throw new InvalidDataException("Observation identity exceeds the save bound.");
            writer.Write(bytes.Length); writer.Write(bytes);
        }
        private static string ReadText(BinaryReader reader)
        {
            int length = ReadCount(reader, 512); byte[] bytes = reader.ReadBytes(length);
            if (bytes.Length != length) throw new EndOfStreamException();
            return Utf8.GetString(bytes);
        }
        private static int ReadCount(BinaryReader reader, int maximum)
        { int value = reader.ReadInt32(); if (value < 0 || value > maximum) throw new InvalidDataException("Invalid observation collection length."); return value; }
        private static bool ReadBool(BinaryReader reader)
        { byte value = reader.ReadByte(); if (value > 1) throw new InvalidDataException("Invalid observation boolean."); return value == 1; }
    }
}
