using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>One damage boundary, before life settlement. The selected profile replays the
    /// source event and defenses; this record is evidence, never a caller supplied damage grant.</summary>
    public sealed class TypedDamageRecord
    {
        public const int MaxRecords=2048;
        public string EventId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public string TargetId { get; }
        public string DamageType { get; }
        public long Raw { get; }
        public long AfterFlatReduction { get; }
        public bool SuccessfulSaveHalf { get; }
        public long AfterSave => SuccessfulSaveHalf?Raw/2:Raw;
        public string InnateResistanceSource { get; }
        public string ImmunitySource { get; }
        public bool Petrified { get; }
        public bool ResistanceApplies => InnateResistanceSource!=""||Petrified&&DamageType!="corruption";
        public long Effective => ImmunitySource!=""?0:ResistanceApplies?AfterFlatReduction/2:AfterFlatReduction;
        public TypedDamageRecord(string eventId,long revision,RuleTime at,string targetId,string damageType,
            long raw,long afterFlatReduction,bool successfulSaveHalf,string innateResistanceSource,string immunitySource,bool petrified)
        {
            if(!Validation.ValidId(eventId)||revision<1||!Validation.ValidId(targetId)||!SupportedType(damageType)
                ||raw<0||afterFlatReduction<0||afterFlatReduction>(successfulSaveHalf?raw/2:raw)
                ||innateResistanceSource==null||innateResistanceSource!=""&&!Validation.ValidId(innateResistanceSource)
                ||immunitySource==null||immunitySource!=""&&!Validation.ValidId(immunitySource))
                throw new ArgumentException("Invalid typed damage resolution.");
            EventId=eventId;Revision=revision;At=at;TargetId=targetId;DamageType=damageType;Raw=raw;
            AfterFlatReduction=afterFlatReduction;SuccessfulSaveHalf=successfulSaveHalf;
            InnateResistanceSource=innateResistanceSource;ImmunitySource=immunitySource;Petrified=petrified;
        }
        // Only currently sourced consumers and the approved defense controls are admitted.
        public static bool SupportedType(string type)=>type=="bludgeoning"||type=="piercing"||type=="slashing"
            ||type=="fire"||type=="acid"||type=="necrotic"||type=="poison"||type=="corruption";
        internal static void Validate(Snapshot s)
        {
            if(s.TypedDamage==null||s.TypedDamage.Length>MaxRecords||s.TypedDamage.Any(x=>x==null)
                ||s.FerryWraith==null&&s.TypedDamage.Length!=0
                ||s.TypedDamage.GroupBy(x=>x.EventId+"|"+x.TargetId).Any(x=>x.Count()!=1))
                throw new ArgumentException("Invalid typed damage history.");
            foreach(var x in s.TypedDamage) {
                var source=s.Creatures.SingleOrDefault(c=>c.ActorId==x.TargetId);
                string resistance=source!=null&&source.DamageResistances.Contains(x.DamageType)?source.SourceId:"";
                string immunity=source!=null&&source.DamageImmunities.Contains(x.DamageType)?source.SourceId:"";
                if(!s.Actors.Any(a=>a.Id==x.TargetId)||x.Revision>s.Revision||x.At>s.RuleClock
                    ||x.InnateResistanceSource!=resistance||x.ImmunitySource!=immunity)
                    throw new ArgumentException("Typed defense differs from its immutable source.");
            }
        }
    }
}
