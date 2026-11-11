using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Immutable closed encounter identity and its actual timeline. Closing eligibility,
    /// resource consequences and elapsed-time policy belong to the authoritative resolver.</summary>
    public sealed class ClosedEncounterRecord
    {
        public FixedEncounterRecord Encounter { get; }
        public long ClosedRevision { get; }
        public RuleTime ClosedAt { get; }
        public string Reason { get; }
        public ClosedEncounterRecord(FixedEncounterRecord encounter, long revision, RuleTime at, string reason)
        {
            if (encounter == null || revision <= encounter.StartRevisions.Last() || at < encounter.Origin || !Validation.ValidId(reason))
                throw new ArgumentException("Invalid closed encounter record.");
            Encounter = encounter; ClosedRevision = revision; ClosedAt = at; Reason = reason;
        }
    }

    public static class EncounterHistory
    {
        public const int MaxClosedEncounters = 16;
        public static IEnumerable<FixedEncounterRecord> All(Snapshot s) => s.ClosedEncounters.Select(x => x.Encounter)
            .Concat(s.Encounter == null ? Array.Empty<FixedEncounterRecord>() : new[] { s.Encounter });
        public static FixedEncounterRecord AtRevision(Snapshot s, long revision)
        {
            if (s.Encounter != null && revision >= s.Encounter.StartRevisions[0]) return s.Encounter;
            return s.ClosedEncounters.SingleOrDefault(x => revision >= x.Encounter.StartRevisions[0] && revision <= x.ClosedRevision)?.Encounter;
        }
        public static bool InCurrent(Snapshot s, long revision) => s.Encounter != null && AtRevision(s, revision)?.Id == s.Encounter.Id;
        public static bool MatchesTurn(FixedEncounterRecord e, int ordinal, string actor) => e != null && ordinal >= 0
            && e.ObservedOrdinals.Contains(ordinal) && e.ActorAt(ordinal) == actor;
        public static int LatestStartOrdinal(Snapshot s, string actor)
        {
            if (s.SchemaVersion >= Snapshot.CalendarCombatSchema && s.WorldSchedule != null)
                return checked((int)WorldTiming.LatestActorStart(s, actor));
            long revision = 0; int ordinal = -1;
            foreach (var e in All(s))
                for (int i = 0; i < e.StartRevisions.Count; i++)
                    if (e.ActorAt(e.ObservedOrdinals[i]) == actor && e.StartRevisions[i] > revision) { revision = e.StartRevisions[i]; ordinal = e.ObservedOrdinals[i]; }
            return ordinal;
        }
        public static void Validate(Snapshot s)
        {
            if (s.ClosedEncounters == null || s.ClosedEncounters.Length > MaxClosedEncounters || s.ClosedEncounters.Any(x => x == null))
                throw new ArgumentException("Invalid encounter archive.");
            if (s.SchemaVersion < Snapshot.SharedWorldSchema && s.ClosedEncounters.Length != 0)
                throw new ArgumentException("Encounter archives require schema13.");
            var records = s.ClosedEncounters.OrderBy(x => x.Encounter.StartRevisions[0]).ToArray();
            long lastRevision = 0; RuleTime lastTime = default;
            foreach (var x in records) {
                var e = x.Encounter;
                if (e.StartRevisions[0] <= lastRevision || e.Origin < lastTime || x.ClosedRevision > s.Revision || x.ClosedAt > s.RuleClock
                    || e.Order.Any(id => !s.Actors.Any(a => a.Id == id))) throw new ArgumentException("Invalid encounter archive sequence.");
                lastRevision = x.ClosedRevision; lastTime = x.ClosedAt;
            }
            if (s.Encounter != null && (s.Encounter.StartRevisions[0] <= lastRevision || s.Encounter.Origin < lastTime))
                throw new ArgumentException("Active encounter overlaps history.");
            var all = All(s).ToArray();
            if (all.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != all.Length)
                throw new ArgumentException("Encounter identity reused.");
        }
    }
}
