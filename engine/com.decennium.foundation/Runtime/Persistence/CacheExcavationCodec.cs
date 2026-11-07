using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class CacheExcavationCodec
    {
        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.BuriedCacheSites.Length);
            foreach (var site in s.BuriedCacheSites.OrderBy(x => x.CacheId, StringComparer.Ordinal))
            {
                SnapshotCodec.WriteText(w, site.CacheId); SnapshotCodec.WriteText(w, site.ShovelId);
                w.Write(site.X); w.Write(site.Y); WriteOptionalTime(w, site.ExposedAt);
            }
            w.Write(s.CacheExcavations.Length);
            foreach (var work in s.CacheExcavations.OrderBy(x => x.Id, StringComparer.Ordinal))
            {
                SnapshotCodec.WriteText(w, work.Id); SnapshotCodec.WriteText(w, work.AssignmentId);
                SnapshotCodec.WriteText(w, work.CacheId); SnapshotCodec.WriteText(w, work.WorkerId); SnapshotCodec.WriteText(w, work.ShovelId);
                WriteTime(w, work.StartedAt); WriteTime(w, work.UpdatedAt); WriteTime(w, work.WorkDone); w.Write((int)work.Status);
            }
        }
        public static void Read(BinaryReader r, Snapshot s)
        {
            s.BuriedCacheSites = new BuriedCacheSiteRecord[SnapshotCodec.ReadCount(r, CacheExcavationValidation.MaxSites)];
            for (int i = 0; i < s.BuriedCacheSites.Length; i++)
                s.BuriedCacheSites[i] = new BuriedCacheSiteRecord(SnapshotCodec.ReadText(r), SnapshotCodec.ReadText(r),
                    r.ReadInt32(), r.ReadInt32(), ReadOptionalTime(r));
            s.CacheExcavations = new CacheExcavationRecord[SnapshotCodec.ReadCount(r, CacheExcavationValidation.MaxExcavations)];
            for (int i = 0; i < s.CacheExcavations.Length; i++)
                s.CacheExcavations[i] = new CacheExcavationRecord(SnapshotCodec.ReadText(r), SnapshotCodec.ReadText(r),
                    SnapshotCodec.ReadText(r), SnapshotCodec.ReadText(r), SnapshotCodec.ReadText(r), ReadTime(r), ReadTime(r),
                    ReadTime(r), (CacheExcavationStatus)r.ReadInt32());
        }
        private static void WriteTime(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime ReadTime(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void WriteOptionalTime(BinaryWriter w, RuleTime? value)
        { w.Write(value.HasValue); if (value.HasValue) WriteTime(w, value.Value); }
        private static RuleTime? ReadOptionalTime(BinaryReader r) => SnapshotCodec.ReadBool(r) ? ReadTime(r) : (RuleTime?)null;
    }
}
