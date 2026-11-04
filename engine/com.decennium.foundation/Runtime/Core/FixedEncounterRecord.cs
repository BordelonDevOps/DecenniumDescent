using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Completed boundary transactions only. A start revision identifies one regular turn;
    /// earlier starts are retained so historical actions never bind to the current cursor.</summary>
    public sealed class FixedEncounterRecord
    {
        public string Id { get; }
        public RuleTime Origin { get; }
        public IReadOnlyList<string> Order { get; }
        public IReadOnlyList<long> StartRevisions { get; }
        // Schema14 can record sparse cursor observations against an established calendar. These
        // revisions are actual commands, not claims that every earlier Start was a new command.
        public IReadOnlyList<int> ObservedOrdinals { get; }
        public bool Sparse=>ObservedOrdinals.Where((n,i)=>n!=i).Any();
        public int TurnOrdinal=>ObservedOrdinals[ObservedOrdinals.Count-1];
        public long Round=>(long)TurnOrdinal/Order.Count+1;
        public string CurrentActor=>Order[TurnOrdinal%Order.Count];
        public string CurrentTurnId=>Id+".turn."+TurnOrdinal.ToString(System.Globalization.CultureInfo.InvariantCulture);
        public FixedEncounterRecord(string id,RuleTime origin,IEnumerable<string> order,IEnumerable<long> starts)
            :this(id,origin,order,starts,null) { }
        public FixedEncounterRecord(string id,RuleTime origin,IEnumerable<string> order,IEnumerable<long> starts,IEnumerable<int> observedOrdinals)
        {
            if(!Validation.ValidId(id)||order==null||starts==null)throw new ArgumentException("Invalid encounter header.");
            var ids=order.ToArray();var revisions=starts.ToArray();
            var ordinals=observedOrdinals==null?Enumerable.Range(0,revisions.Length).ToArray():observedOrdinals.ToArray();
            if(ids.Length<1||ids.Length>64||ids.Any(x=>!Validation.ValidId(x))||ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length
                ||revisions.Length<1||revisions.Length>128||revisions.Any(x=>x<1)
                ||revisions.Where((x,i)=>i>0&&x<=revisions[i-1]).Any()||ordinals.Length!=revisions.Length||ordinals.Any(x=>x<0)
                ||ordinals.Where((x,i)=>i>0&&x<=ordinals[i-1]).Any())throw new ArgumentException("Invalid fixed roster or regular-start history.");
            if(!Validation.ValidId(id+".turn."+Math.Max(127,ordinals.Last()).ToString(System.Globalization.CultureInfo.InvariantCulture)))throw new ArgumentException("Encounter turn identity exceeds bounds.");
            Id=id;Origin=origin;Order=Array.AsReadOnly(ids);StartRevisions=Array.AsReadOnly(revisions);ObservedOrdinals=Array.AsReadOnly(ordinals);
        }
    }
    public sealed class EncounterDashRecord
    {
        public long Revision { get; }
        public int TurnOrdinal { get; }
        public string ActorId { get; }
        public EncounterDashRecord(long revision,int turnOrdinal,string actor)
        {if(revision<1||turnOrdinal<0||!Validation.ValidId(actor))throw new ArgumentException("Invalid paid Dash.");Revision=revision;TurnOrdinal=turnOrdinal;ActorId=actor;}
    }
    public static class FixedEncounterValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.EncounterDashes==null||s.EncounterDashes.Length>128||s.EncounterDashes.Any(x=>x==null))throw new ArgumentException("Invalid encounter action collection.");
            if(s.SchemaVersion<Snapshot.EncounterSchema) {
                if(s.Encounter!=null||s.EncounterDashes.Length!=0)throw new ArgumentException("Fixed encounter requires schema7.");return;
            }
            var e=s.Encounter;
            if(s.SchemaVersion<Snapshot.CalendarCombatSchema&&EncounterHistory.All(s).Any(x=>x.Sparse))throw new ArgumentException("Sparse encounter cursor requires schema14.");
            bool world=s.SchemaVersion>=Snapshot.CalendarCombatSchema&&s.WorldSchedule!=null;
            if((world?s.InventoryCombat&&e==null:(e!=null)!=s.InventoryCombat)||s.SchemaVersion<Snapshot.SharedWorldSchema&&e==null&&s.EncounterDashes.Length!=0)throw new ArgumentException("Invalid encounter presence.");
            if(e!=null&&(e.Origin>s.RuleClock||e.StartRevisions.Any(r=>r>s.Revision)||e.Order.Any(id=>!s.Actors.Any(a=>a.Id==id))
                ||(s.InventoryCombat&&s.InventoryTurnActor!=e.CurrentActor))||s.EncounterDashes.Select(x=>x.Revision).Distinct().Count()!=s.EncounterDashes.Length
                ||s.EncounterDashes.Any(x=>x.Revision>s.Revision||!EncounterHistory.MatchesTurn(EncounterHistory.AtRevision(s,x.Revision),x.TurnOrdinal,x.ActorId)))
                throw new ArgumentException("Invalid encounter references.");
        }
    }
}
