using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class ResonanceCodec
    {
        internal static void Write(BinaryWriter w, Snapshot state)
        {
            var entry = state.ClericEntry;
            Text(w, entry.ActorId); Text(w, entry.SourceRevision); w.Write(entry.PointBuyCost);
            Text(w, entry.FavoredWeaponProfile); Text(w, entry.EngineSelector);
            foreach (var skill in entry.SelectedSkills) Text(w, skill);
            foreach (var save in entry.SavingThrows) Text(w, save);
            w.Write(state.ResonancePools.Length);
            foreach (var pool in state.ResonancePools.OrderBy(x => x.ActorId, System.StringComparer.Ordinal)) {
                Text(w, pool.ActorId); w.Write(pool.Maximum); w.Write(pool.Current);
                var funding = pool.InitialFunding;
                Text(w, funding.Id); Text(w, funding.ActorId); Text(w, funding.PolicyId); w.Write(funding.Amount); w.Write(funding.Revision);
            }
            w.Write(state.HealingRites.Length);
            foreach (var result in state.HealingRites) {
                Text(w, result.CommandId); w.Write(result.Revision); Text(w, result.ActorId); Text(w, result.TargetId);
                Text(w, result.SourceId); Text(w, result.SourceRevision); w.Write(result.TurnOrdinal); Time(w, result.At);
                w.Write(result.RpBefore); w.Write(result.RpPaid); w.Write(result.RpAfter); w.Write(result.Die); w.Write(result.Modifier);
                w.Write(result.Potential); w.Write(result.HpBefore); w.Write(result.HpAfter);
                w.Write(result.RandomBefore); w.Write(result.RandomAfter); w.Write(result.WordsConsumed);
            }
        }
        internal static void Read(BinaryReader r, Snapshot state)
        {
            string actor = Text(r), source = Text(r); int points = r.ReadInt32();
            string favored = Text(r), engine = Text(r);
            state.ClericEntry = new ClericClassEntryRecord(actor, source, points, favored, engine,
                new[] { Text(r), Text(r) }, new[] { Text(r), Text(r) });
            state.ResonancePools = new ResonancePoolRecord[SnapshotCodec.ReadCount(r, 64)];
            for (int i = 0; i < state.ResonancePools.Length; i++) {
                string owner = Text(r); int maximum = r.ReadInt32(), current = r.ReadInt32();
                var funding = new ResonanceFundingRecord(Text(r), Text(r), Text(r), r.ReadInt32(), r.ReadInt64());
                state.ResonancePools[i] = new ResonancePoolRecord(owner, maximum, current, funding);
            }
            state.HealingRites = new HealingRiteRecord[SnapshotCodec.ReadCount(r, 128)];
            for (int i = 0; i < state.HealingRites.Length; i++)
                state.HealingRites[i] = new HealingRiteRecord(Text(r), r.ReadInt64(), Text(r), Text(r), Text(r), Text(r),
                    r.ReadInt32(), Time(r), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(),
                    r.ReadInt64(), r.ReadInt64(), r.ReadInt64(), r.ReadUInt32(), r.ReadUInt32(), r.ReadInt64());
        }
        private static void Text(BinaryWriter w, string value) => SnapshotCodec.WriteText(w, value);
        private static string Text(BinaryReader r) => SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
    }
}
