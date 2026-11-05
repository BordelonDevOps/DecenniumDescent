using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class TacticalMovementCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.TacticalActors.Length);foreach(var a in s.TacticalActors.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,a.ActorId);w.Write(a.LastRegularStart);w.Write(a.ReactionAvailable);w.Write(a.MobileFeet);w.Write(a.PressConsumed);w.Write(a.DisengageTurn); }
            w.Write(s.TacticalMoves.Length);foreach(var m in s.TacticalMoves.OrderBy(x=>x.Revision)) {
                Text(w,m.Id);w.Write(m.Revision);w.Write(m.ResolvedRevision);w.Write(m.TurnOrdinal);Text(w,m.ActorId);
                w.Write(m.FromX);w.Write(m.FromY);w.Write(m.ToX);w.Write(m.ToY);w.Write((int)m.Kind);w.Write((int)m.Status);
                w.Write(m.Reactors.Count);foreach(string id in m.Reactors)Text(w,id);w.Write(m.ResponseIndex);w.Write(m.CostPaid);Text(w,m.ParentPressOffer);
                if(s.SchemaVersion>=Snapshot.CommandStepSchema)Text(w,m.ParentCommandStepOffer);
                if(s.SchemaVersion>=Snapshot.DefensiveFormationSchema)Text(w,m.ParentDefensiveFormationId); }
            w.Write(s.PressOffers.Length);foreach(var p in s.PressOffers.OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.ArmedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,p.Id);Text(w,p.MoveId);Text(w,p.ActorId);Text(w,p.TargetId);w.Write(p.CreatedRevision);w.Write(p.ArmedRevision);w.Write((int)p.Status);w.Write(p.ResolvedRevision); }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.TacticalActors=new ActorTacticalRecord[Count(r,64)];for(int i=0;i<s.TacticalActors.Length;i++)s.TacticalActors[i]=new ActorTacticalRecord(Text(r),r.ReadInt32(),Bool(r),r.ReadInt32(),Bool(r),r.ReadInt32());
            s.TacticalMoves=new TacticalMoveRecord[Count(r,64)];for(int i=0;i<s.TacticalMoves.Length;i++) {
                string id=Text(r);long revision=r.ReadInt64(),resolved=r.ReadInt64();int ordinal=r.ReadInt32();string actor=Text(r);
                int fromX=r.ReadInt32(),fromY=r.ReadInt32(),toX=r.ReadInt32(),toY=r.ReadInt32();var kind=(TacticalMoveKind)r.ReadInt32();var status=(TacticalMoveStatus)r.ReadInt32();
                var reactors=new string[Count(r,64)];for(int j=0;j<reactors.Length;j++)reactors[j]=Text(r);
                int response=r.ReadInt32();long cost=r.ReadInt64();string parentPress=Text(r);
                string parentCommandStep=s.SchemaVersion>=Snapshot.CommandStepSchema?Text(r):"";
                string parentDefensiveFormation=s.SchemaVersion>=Snapshot.DefensiveFormationSchema?Text(r):"";
                s.TacticalMoves[i]=new TacticalMoveRecord(id,revision,resolved,ordinal,actor,fromX,fromY,toX,toY,kind,status,reactors,response,cost,parentPress,parentCommandStep,parentDefensiveFormation); }
            s.PressOffers=new PressOfferRecord[Count(r,128)];for(int i=0;i<s.PressOffers.Length;i++)s.PressOffers[i]=new PressOfferRecord(Text(r),Text(r),Text(r),Text(r),r.ReadInt64(),r.ReadInt64(),(PressOfferStatus)r.ReadInt32(),r.ReadInt64());
        }
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid tactical flag.");return b==1;}
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid tactical count.");return n;}
        private static void Text(BinaryWriter w,string t){byte[] b=Utf8.GetBytes(t);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
