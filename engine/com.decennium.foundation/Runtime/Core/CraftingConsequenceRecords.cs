using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Only actors without an established activity calendar receive this cadence.
    /// The next marker is persisted, so mode changes and restore cannot restart it.</summary>
    public sealed class DyingCadenceRecord
    {
        public string ActorId { get; }
        public RuleTime Onset { get; }
        public long NextOrdinal { get; }
        public RuleTime NextAt => Onset.AddSeconds(checked(6 * NextOrdinal));
        public DyingCadenceRecord(string actor, RuleTime onset, long nextOrdinal = 1)
        {
            if (!Validation.ValidId(actor) || nextOrdinal < 1 || nextOrdinal > long.MaxValue / 6) throw new ArgumentException("Invalid dying cadence.");
            ActorId = actor; Onset = onset; NextOrdinal = nextOrdinal;
        }
    }
    public enum ObjectMaterial { ClothPaperRope, GlassCrystal, WoodLeather, Stone, IronSteel }
    /// <summary>Logical due identity and global audit sequence are distinct. These persist after
    /// a dying episode closes, independently of the remaining schedule cursor.</summary>
    public sealed class WorldLifeMarkerRecord
    {
        public string ActorId { get; }
        public string CalendarId { get; }
        public RuleTime Origin { get; }
        public long Ordinal { get; }
        public long Sequence { get; }
        public RuleTime At { get; }
        public WorldLifeMarkerRecord(string actor, string calendar, RuleTime origin, long ordinal, long sequence, RuleTime at)
        {
            if (!Validation.ValidId(actor) || !Validation.ValidId(calendar) || ordinal < 0 || sequence < 1 || at < origin) throw new ArgumentException("Invalid life marker identity.");
            ActorId = actor; CalendarId = calendar; Origin = origin; Ordinal = ordinal; Sequence = sequence; At = at;
        }
    }
    public sealed class ObjectStructureRecord
    {
        public string Id { get; }
        public string ProfileId { get; }
        public string OwnerId { get; }
        public string CustodianId { get; }
        public string LocationId { get; }
        public ObjectMaterial Material { get; }
        public long MaximumHp { get; }
        public long Hp { get; }
        public long BaselineCopper { get; }
        public RuleQuantity MassPounds { get; }
        public bool Broken => Hp == 0;
        public ObjectStructureRecord(string id, string profile, string owner, string custodian, string location,
            ObjectMaterial material, long maximumHp, long hp, long baselineCopper, RuleQuantity mass)
        {
            if (new[] { id, profile, owner, custodian, location }.Any(x => !Validation.ValidId(x))
                || !Enum.IsDefined(typeof(ObjectMaterial), material) || maximumHp < 1 || hp < 0 || hp > maximumHp || baselineCopper < 0)
                throw new ArgumentException("Invalid object structure.");
            Id = id; ProfileId = profile; OwnerId = owner; CustodianId = custodian; LocationId = location; Material = material;
            MaximumHp = maximumHp; Hp = hp; BaselineCopper = baselineCopper; MassPounds = mass;
        }
        public ObjectStructureRecord WithHp(long hp) => new ObjectStructureRecord(Id, ProfileId, OwnerId, CustodianId, LocationId, Material, MaximumHp, hp, BaselineCopper, MassPounds);
        public ObjectStructureRecord WithLocation(string locationId) => new ObjectStructureRecord(Id, ProfileId, OwnerId, CustodianId, locationId, Material, MaximumHp, Hp, BaselineCopper, MassPounds);
        public ObjectStructureRecord WithLocationAndCustodian(string locationId,string custodianId)
            =>new ObjectStructureRecord(Id,ProfileId,OwnerId,custodianId,locationId,Material,MaximumHp,Hp,BaselineCopper,MassPounds);
    }
    /// <summary>A settled, sourced mishap and any outstanding remedy. Labor is person-seconds;
    /// active worker identity is separate from the participants in the failed order.</summary>
    public sealed class CraftingIncidentRecord
    {
        public string Id { get; }
        public string LeadId { get; }
        public string ToolId { get; }
        public string StationId { get; }
        public string TradeId { get; }
        public int Result { get; }
        public int Participants => ParticipantIds.Count;
        public IReadOnlyList<string> ParticipantIds { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime RequiredLabor { get; }
        public RuleTime Labor { get; }
        public IReadOnlyList<string> Workers { get; }
        public int InjuryD4 { get; }
        public long Damage { get; }
        public int WoundD20 { get; }
        public int InjuryD6 { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public bool Remedied => Labor == RequiredLabor;
        public CraftingIncidentRecord(string id, string lead, string tool, string station, string trade, int result, IEnumerable<string> participants,
            long revision, RuleTime at, RuleTime updated, RuleTime required, RuleTime labor, IEnumerable<string> workers,
            int injuryD4, long damage, int woundD20, int injuryD6, uint randomBefore, uint randomAfter, long words)
        {
            if (new[] { id, lead, tool, station, trade }.Any(x => !Validation.ValidId(x)) || result < 1 || result > 6 || participants == null
                || revision < 1 || updated < at || labor > required || workers == null || injuryD4 < 0 || injuryD4 > 4 || damage < 0
                || woundD20 < 0 || woundD20 > 20 || injuryD6 < 0 || injuryD6 > 6 || randomBefore == 0 || randomAfter == 0 || words < 0)
                throw new ArgumentException("Invalid crafting incident.");
            var active = workers.ToArray(); var people = participants.ToArray();
            if (people.Length < 1 || people.Length > 64 || people.Any(x => !Validation.ValidId(x)) || !people.Contains(lead) || people.Distinct(StringComparer.Ordinal).Count() != people.Length) throw new ArgumentException("Invalid original participants.");
            if (active.Length > 64 || active.Any(x => !Validation.ValidId(x)) || active.Distinct(StringComparer.Ordinal).Count() != active.Length || labor == required && active.Length != 0)
                throw new ArgumentException("Invalid remedy workers.");
            Id = id; LeadId = lead; ToolId = tool; StationId = station; TradeId = trade; Result = result; ParticipantIds = Array.AsReadOnly(people);
            Revision = revision; At = at; UpdatedAt = updated; RequiredLabor = required; Labor = labor; Workers = Array.AsReadOnly(active);
            InjuryD4 = injuryD4; Damage = damage; WoundD20 = woundD20; InjuryD6 = injuryD6; RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = words;
        }
        public CraftingIncidentRecord WithWork(RuleTime at, RuleTime labor, IEnumerable<string> workers) => new CraftingIncidentRecord(Id, LeadId, ToolId, StationId, TradeId,
            Result, ParticipantIds, Revision, At, at, RequiredLabor, labor, workers, InjuryD4, Damage, WoundD20, InjuryD6, RandomBefore, RandomAfter, WordsConsumed);
    }
    public static class CraftingConsequenceValidation
    {
        public const int MaxIncidents = 32;
        public static void Validate(Snapshot s)
        {
            if (s.DyingCadences == null || s.Structures == null || s.CraftingIncidents == null || s.WorldLifeMarkers == null || s.WorldLifeMarkers.Length > 256 || s.WorldLifeMarkers.Any(x => x == null) || s.DyingCadences.Length > 64 || s.Structures.Length > 64 || s.CraftingIncidents.Length > MaxIncidents
                || s.DyingCadences.Any(x => x == null) || s.Structures.Any(x => x == null) || s.CraftingIncidents.Any(x => x == null)
                || s.SchemaVersion < Snapshot.CraftingConsequenceSchema && (s.DyingCadences.Length + s.Structures.Length + s.CraftingIncidents.Length + s.WorldLifeMarkers.Length != 0)) throw new ArgumentException("Invalid crafting consequence collections.");
            if (s.DyingCadences.Select(x => x.ActorId).Distinct().Count() != s.DyingCadences.Length || s.Structures.Select(x => x.Id).Distinct().Count() != s.Structures.Length
                || s.CraftingIncidents.Select(x => x.Id).Distinct().Count() != s.CraftingIncidents.Length) throw new ArgumentException("Duplicate consequence identity.");
            foreach (var cadence in s.DyingCadences)
                if (!s.Actors.Any(x => x.Id == cadence.ActorId) || cadence.Onset > s.RuleClock || cadence.NextAt <= s.RuleClock || WorldTiming.ForActor(s, cadence.ActorId) != null)
                    throw new ArgumentException("Invalid fallback cadence reference or cursor.");
            if (s.SchemaVersion >= Snapshot.CraftingConsequenceSchema) {
                var saves = s.LifeEvents.Where(x => x.Kind == LifeEventKind.DeathSave).ToArray();
                if (saves.Length != s.WorldLifeMarkers.Length) throw new ArgumentException("Missing logical life marker.");
                for (int i = 0; i < saves.Length; i++) {
                    var marker = s.WorldLifeMarkers[i];
                    if (marker.Sequence != i + 1 || marker.ActorId != saves[i].ActorId || marker.At != saves[i].At) throw new ArgumentException("Invalid life marker sequence.");
                    if (s.SchemaVersion == Snapshot.LaterEncounterSchema && marker.CalendarId != "outside.dying") {
                        var epoch = WorldTiming.FindEpoch(s, marker.CalendarId);
                        if (epoch == null || epoch.Origin != marker.Origin || marker.Ordinal > epoch.ProcessedSlot
                            || epoch.Start(marker.Ordinal) != marker.At || epoch.Order[(int)(marker.Ordinal % epoch.Order.Count)] != marker.ActorId)
                            throw new ArgumentException("Invalid life marker epoch.");
                    }
                }
            }
            foreach (var incident in s.CraftingIncidents)
                if (!s.Actors.Any(x => x.Id == incident.LeadId) || !s.Structures.Any(x => x.Id == incident.ToolId) || incident.Workers.Concat(incident.ParticipantIds).Any(w => !s.Actors.Any(x => x.Id == w))
                    || incident.Revision > s.Revision || incident.UpdatedAt > s.RuleClock) throw new ArgumentException("Invalid incident reference or timestamp.");
        }
    }
}
