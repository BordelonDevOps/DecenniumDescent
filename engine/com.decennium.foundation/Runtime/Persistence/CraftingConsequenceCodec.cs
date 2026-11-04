using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class CraftingConsequenceCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.DyingCadences.Length);
            foreach (var c in s.DyingCadences.OrderBy(x => x.ActorId, StringComparer.Ordinal)) { Text(w, c.ActorId); Time(w, c.Onset); w.Write(c.NextOrdinal); }
            w.Write(s.WorldLifeMarkers.Length);
            foreach (var m in s.WorldLifeMarkers) { Text(w, m.ActorId); Text(w, m.CalendarId); Time(w, m.Origin); w.Write(m.Ordinal); w.Write(m.Sequence); Time(w, m.At); }
            w.Write(s.Structures.Length);
            foreach (var o in s.Structures.OrderBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, o.Id); Text(w, o.ProfileId); Text(w, o.OwnerId); Text(w, o.CustodianId); Text(w, o.LocationId); w.Write((int)o.Material);
                w.Write(o.MaximumHp); w.Write(o.Hp); w.Write(o.BaselineCopper); w.Write(o.MassPounds.Numerator); w.Write(o.MassPounds.Denominator);
            }
            w.Write(s.CraftingIncidents.Length);
            foreach (var i in s.CraftingIncidents.OrderBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, i.Id); Text(w, i.LeadId); Text(w, i.ToolId); Text(w, i.StationId); Text(w, i.TradeId); w.Write(i.Result); w.Write(i.Participants); foreach (string a in i.ParticipantIds) Text(w, a); w.Write(i.Revision);
                Time(w, i.At); Time(w, i.UpdatedAt); Time(w, i.RequiredLabor); Time(w, i.Labor); w.Write(i.Workers.Count); foreach (string a in i.Workers.OrderBy(x => x, StringComparer.Ordinal)) Text(w, a);
                w.Write(i.InjuryD4); w.Write(i.Damage); w.Write(i.WoundD20); w.Write(i.InjuryD6); w.Write(i.RandomBefore); w.Write(i.RandomAfter); w.Write(i.WordsConsumed);
            }
        }
        public static void Read(BinaryReader r, Snapshot s)
        {
            s.DyingCadences = new DyingCadenceRecord[Count(r, 64)];
            for (int i = 0; i < s.DyingCadences.Length; i++) s.DyingCadences[i] = new DyingCadenceRecord(Text(r), Time(r), r.ReadInt64());
            s.WorldLifeMarkers = new WorldLifeMarkerRecord[Count(r, 256)];
            for (int i = 0; i < s.WorldLifeMarkers.Length; i++) s.WorldLifeMarkers[i] = new WorldLifeMarkerRecord(Text(r), Text(r), Time(r), r.ReadInt64(), r.ReadInt64(), Time(r));
            s.Structures = new ObjectStructureRecord[Count(r, 64)];
            for (int i = 0; i < s.Structures.Length; i++) s.Structures[i] = new ObjectStructureRecord(Text(r), Text(r), Text(r), Text(r), Text(r), (ObjectMaterial)r.ReadInt32(),
                r.ReadInt64(), r.ReadInt64(), r.ReadInt64(), new RuleQuantity(r.ReadInt64(), r.ReadInt64()));
            s.CraftingIncidents = new CraftingIncidentRecord[Count(r, CraftingConsequenceValidation.MaxIncidents)];
            for (int i = 0; i < s.CraftingIncidents.Length; i++) {
                string id = Text(r), lead = Text(r), tool = Text(r), station = Text(r), trade = Text(r); int result = r.ReadInt32(); var participants = new string[Count(r, 64)]; for (int j = 0; j < participants.Length; j++) participants[j] = Text(r); long revision = r.ReadInt64();
                var at = Time(r); var updated = Time(r); var required = Time(r); var labor = Time(r); var workers = new string[Count(r, 64)];
                for (int j = 0; j < workers.Length; j++) workers[j] = Text(r);
                s.CraftingIncidents[i] = new CraftingIncidentRecord(id, lead, tool, station, trade, result, participants, revision, at, updated, required, labor, workers,
                    r.ReadInt32(), r.ReadInt64(), r.ReadInt32(), r.ReadInt32(), r.ReadUInt32(), r.ReadUInt32(), r.ReadInt64());
            }
        }
        private static void Time(BinaryWriter w, RuleTime t) { w.Write(t.Numerator); w.Write(t.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static int Count(BinaryReader r, int max) { int n = r.ReadInt32(); if (n < 0 || n > max) throw new InvalidDataException("Invalid consequence count."); return n; }
        private static void Text(BinaryWriter w, string t) { var b = Utf8.GetBytes(t); w.Write(b.Length); w.Write(b); }
        private static string Text(BinaryReader r) { int n = Count(r, 96); var b = r.ReadBytes(n); if (b.Length != n) throw new EndOfStreamException(); return Utf8.GetString(b); }
    }
}
