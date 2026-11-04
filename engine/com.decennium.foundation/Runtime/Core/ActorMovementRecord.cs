using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Explicit base walking Speed and spent cost for the last recorded regular turn.
    /// Current Speed and legal Dash count are derived by the selected policy, never stored twice.</summary>
    public sealed class ActorMovementRecord
    {
        public string ActorId { get; }
        public int BaseWalkingSpeed { get; }
        public int TurnOrdinal { get; }
        public long Spent { get; }
        public ActorMovementRecord(string actor,int baseWalkingSpeed,int ordinal=-1,long spent=0)
        {
            if(!Validation.ValidId(actor)||baseWalkingSpeed<0||ordinal< -1||spent<0||ordinal==-1&&spent!=0)throw new ArgumentException("Invalid actor movement record.");
            ActorId=actor;BaseWalkingSpeed=baseWalkingSpeed;TurnOrdinal=ordinal;Spent=spent;
        }
        public bool SameAs(ActorMovementRecord x)=>x!=null&&ActorId==x.ActorId&&BaseWalkingSpeed==x.BaseWalkingSpeed&&TurnOrdinal==x.TurnOrdinal&&Spent==x.Spent;
    }
    public static class ActorMovementValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.ActorMovement==null||s.ActorMovement.Length>64||s.ActorMovement.Any(m=>m==null))throw new ArgumentException("Invalid movement collection.");
            if(s.SchemaVersion<Snapshot.PostureSchema){if(s.ActorMovement.Length!=0)throw new ArgumentException("Movement state requires schema10.");return;}
            if(!s.Actors.Select(a=>a.Id).OrderBy(a=>a,StringComparer.Ordinal).SequenceEqual(s.ActorMovement.Select(m=>m.ActorId).OrderBy(a=>a,StringComparer.Ordinal)))throw new ArgumentException("Invalid movement actor identities.");
            foreach(var m in s.ActorMovement) {
                if(m.TurnOrdinal>=0&&(s.Encounter==null||m.TurnOrdinal>s.Encounter.TurnOrdinal||s.Encounter.Order[m.TurnOrdinal%s.Encounter.Order.Count]!=m.ActorId))throw new ArgumentException("Invalid movement turn.");
            }
        }
    }
}
