using System.IO;

namespace Decennium.Foundation
{
    internal static class FleshWardenCodec
    {
        internal static void Write(BinaryWriter w, FleshWardenRecord record)
        {
            var q = record.Qualification;
            Text(w, q.ActorId); Text(w, q.SourceRevision); w.Write((byte)q.Tier); w.Write((byte)q.Tree);
            w.Write(record.SlotOrdinal); Text(w, record.EquippedMutationId); Text(w, record.ApplicationId);
            w.Write(record.Choices.Count);
            foreach (var choice in record.Choices) {
                Text(w, choice.RestId); Text(w, choice.MutationId); w.Write(choice.Change != null);
                var c = choice.Change;
                if (c == null) continue;
                Text(w, c.PreviousMutationId); Text(w, c.PreviousApplicationId); Text(w, c.ApplicationId);
                w.Write(c.BaseMaximum); w.Write(c.MaximumBefore); w.Write(c.MaximumAfter);
                w.Write(c.EffectiveBefore); w.Write(c.EffectiveAfter); w.Write(c.HpBefore); w.Write(c.HpAfter);
            }
            w.Write(record.Applications.Count);
            foreach (var a in record.Applications) {
                Text(w, a.Id); Text(w, a.SourceId); Text(w, a.SourceRevision); Text(w, a.OwnerId); Text(w, a.TargetId);
                w.Write(a.WarriorLevel); Text(w, a.StartRestId); Time(w, a.StartedAt); Text(w, a.EndRestId);
                if (a.EndedAt.HasValue) Time(w, a.EndedAt.Value);
            }
        }
        internal static FleshWardenRecord Read(BinaryReader r)
        {
            var q = new MutationQualificationRecord(Text(r), Text(r), (MutationTier)r.ReadByte(), (MutationTree)r.ReadByte());
            int slot = r.ReadInt32(); string equipped = Text(r), application = Text(r);
            var choices = new MutationRestChoiceRecord[SnapshotCodec.ReadCount(r, ShortRestBerth.MaxAttempts)];
            for (int i = 0; i < choices.Length; i++) {
                string rest = Text(r), mutation = Text(r);
                MutationCapacityChangeRecord change = null;
                if (SnapshotCodec.ReadBool(r)) change = new MutationCapacityChangeRecord(Text(r), Text(r), Text(r),
                    r.ReadInt64(), r.ReadInt64(), r.ReadInt64(), r.ReadInt64(), r.ReadInt64(), r.ReadInt64(), r.ReadInt64());
                choices[i] = new MutationRestChoiceRecord(rest, mutation, change);
            }
            var effects = new MutationCapacityApplicationRecord[SnapshotCodec.ReadCount(r, ShortRestBerth.MaxAttempts)];
            for (int i = 0; i < effects.Length; i++) {
                string id = Text(r), source = Text(r), revision = Text(r), owner = Text(r), target = Text(r);
                int level = r.ReadInt32(); string start = Text(r); var at = Time(r); string end = Text(r);
                effects[i] = new MutationCapacityApplicationRecord(id, source, revision, owner, target, level, start, at,
                    end, end == "" ? (RuleTime?)null : Time(r));
            }
            return new FleshWardenRecord(q, slot, equipped, application, choices, effects);
        }
        private static void Text(BinaryWriter w, string value) => SnapshotCodec.WriteText(w, value);
        private static string Text(BinaryReader r) => SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
    }
}
