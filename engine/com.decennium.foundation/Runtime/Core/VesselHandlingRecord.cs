using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>One intact vessel movement, with unchanged physical contents and distinct ownership.
    /// Sequence is the committed command revision, including ordering between zero-time interactions.</summary>
    public sealed class VesselHandlingRecord
    {
        public string Id { get; }
        public long Sequence { get; }
        public string ActorId { get; }
        public string VesselId { get; }
        public string FromLocation { get; }
        public string FromCustodian { get; }
        public string ToLocation { get; }
        public string ToCustodian { get; }
        public HandlingKind Kind { get; }
        public RuleTime StartedAt { get; }
        public RuleTime EndedAt { get; }
        public bool Tactical { get; }
        public VesselHandlingRecord(string id,long sequence,string actor,string vessel,string fromLocation,string fromCustodian,
            string toLocation,string toCustodian,HandlingKind kind,RuleTime start,RuleTime end,bool tactical)
        {
            if(!new[]{id,actor,vessel,fromLocation,fromCustodian,toLocation,toCustodian}.All(Validation.ValidId)
                ||sequence<1||!Enum.IsDefined(typeof(HandlingKind),kind)||end<start)throw new ArgumentException("Invalid vessel handling record.");
            Id=id;Sequence=sequence;ActorId=actor;VesselId=vessel;FromLocation=fromLocation;FromCustodian=fromCustodian;
            ToLocation=toLocation;ToCustodian=toCustodian;Kind=kind;StartedAt=start;EndedAt=end;Tactical=tactical;
        }
    }
    public static class VesselHandlingValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.VesselMoves==null||s.VesselMoves.Length>64||s.VesselMoves.Any(x=>x==null))throw new ArgumentException("Invalid vessel movement collection.");
            if(s.SchemaVersion!=Snapshot.MovableVesselSchema) {
                if(s.VesselMoves.Length!=0)throw new ArgumentException("Vessel movement requires schema6.");return;
            }
            var ids=s.WaterFills.Select(x=>x.Id).Concat(s.Intakes.Select(x=>x.Id)).Concat(s.Handling.Select(x=>x.Id))
                .Concat(s.Crops.SelectMany(c=>c.Tasks).Select(x=>x.Id)).ToArray();
            if(s.VesselMoves.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.VesselMoves.Length
                ||s.VesselMoves.Select(x=>x.Sequence).Distinct().Count()!=s.VesselMoves.Length
                ||s.VesselMoves.Any(x=>ids.Contains(x.Id)||!s.Actors.Any(a=>a.Id==x.ActorId)||!s.Vessels.Any(v=>v.Id==x.VesselId)
                    ||x.Sequence>s.Revision||x.EndedAt>s.RuleClock))throw new ArgumentException("Invalid vessel movement identity, sequence or reference.");
        }
    }
}
