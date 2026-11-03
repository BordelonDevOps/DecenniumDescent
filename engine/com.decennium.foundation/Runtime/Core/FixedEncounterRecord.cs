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
        public int TurnOrdinal=>StartRevisions.Count-1;
        public int Round=>TurnOrdinal/Order.Count+1;
        public string CurrentActor=>Order[TurnOrdinal%Order.Count];
        public string CurrentTurnId=>Id+".turn."+TurnOrdinal.ToString(System.Globalization.CultureInfo.InvariantCulture);
        public FixedEncounterRecord(string id,RuleTime origin,IEnumerable<string> order,IEnumerable<long> starts)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(id+".turn.127")||order==null||starts==null)throw new ArgumentException("Invalid encounter header.");
            var ids=order.ToArray();var revisions=starts.ToArray();
            if(ids.Length<1||ids.Length>64||ids.Any(x=>!Validation.ValidId(x))||ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length
                ||revisions.Length<1||revisions.Length>128||revisions.Any(x=>x<1)
                ||revisions.Where((x,i)=>i>0&&x<=revisions[i-1]).Any())throw new ArgumentException("Invalid fixed roster or regular-start history.");
            Id=id;Origin=origin;Order=Array.AsReadOnly(ids);StartRevisions=Array.AsReadOnly(revisions);
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
            if((e!=null)!=s.InventoryCombat||e==null&&s.EncounterDashes.Length!=0)throw new ArgumentException("Invalid encounter presence.");
            if(e==null)return;
            if(e.Origin>s.RuleClock||e.StartRevisions.Any(r=>r>s.Revision)||e.Order.Any(id=>!s.Actors.Any(a=>a.Id==id))
                ||s.InventoryTurnActor!=e.CurrentActor||s.EncounterDashes.Select(x=>x.Revision).Distinct().Count()!=s.EncounterDashes.Length
                ||s.EncounterDashes.Any(x=>x.Revision>s.Revision||x.TurnOrdinal>e.TurnOrdinal||e.Order[x.TurnOrdinal%e.Order.Count]!=x.ActorId))
                throw new ArgumentException("Invalid encounter references.");
        }
    }
}
