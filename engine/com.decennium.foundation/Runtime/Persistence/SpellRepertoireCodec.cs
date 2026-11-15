using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class SpellRepertoireCodec
    {
        internal static void Write(BinaryWriter writer, Snapshot state)
        {
            writer.Write(state.KnownSpells.Length);
            foreach (var spell in state.KnownSpells.OrderBy(x => x.ActorId, StringComparer.Ordinal)
                .ThenBy(x => x.ClassName, StringComparer.Ordinal).ThenBy(x => x.SpellId, StringComparer.Ordinal)) {
                Text(writer, spell.ActorId); Text(writer, spell.ClassName); Text(writer, spell.SpellId);
                Text(writer, spell.SourceRevision); Text(writer, spell.WholeCardSha256); Text(writer, spell.ProcedureSha256);
                Text(writer, spell.School); writer.Write(spell.Rank); writer.Write((int)spell.Origin);
                writer.Write(spell.ClassLevel); writer.Write(spell.LevelOrdinal); Text(writer, spell.EntitlementId);
                Text(writer, spell.MilestoneId); writer.Write(spell.AcquiredRevision);
            }
        }
        internal static void Read(BinaryReader reader, Snapshot state)
        {
            state.KnownSpells = new KnownSpellRecord[SnapshotCodec.ReadCount(reader, 128)];
            for (int i = 0; i < state.KnownSpells.Length; i++)
                state.KnownSpells[i] = new KnownSpellRecord(Text(reader), Text(reader), Text(reader), Text(reader), Text(reader),
                    Text(reader), Text(reader), reader.ReadInt32(), (SpellAcquisitionOrigin)reader.ReadInt32(), reader.ReadInt32(),
                    reader.ReadInt32(), Text(reader), Text(reader), reader.ReadInt64());
        }
        private static void Text(BinaryWriter writer, string value) => SnapshotCodec.WriteText(writer, value);
        private static string Text(BinaryReader reader) => SnapshotCodec.ReadText(reader);
    }
}
