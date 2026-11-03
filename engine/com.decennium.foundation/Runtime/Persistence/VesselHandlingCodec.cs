using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class VesselHandlingCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.VesselMoves.Length);
            foreach(var m in s.VesselMoves.OrderBy(x=>x.Sequence)) {
                Text(w,m.Id);w.Write(m.Sequence);Text(w,m.ActorId);Text(w,m.VesselId);Text(w,m.FromLocation);Text(w,m.FromCustodian);
                Text(w,m.ToLocation);Text(w,m.ToCustodian);w.Write((int)m.Kind);Time(w,m.StartedAt);Time(w,m.EndedAt);w.Write(m.Tactical);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.VesselMoves=new VesselHandlingRecord[Count(r,64)];
            for(int i=0;i<s.VesselMoves.Length;i++) {
                string id=Text(r);long sequence=r.ReadInt64();string actor=Text(r),vessel=Text(r),from=Text(r),fromCustodian=Text(r),to=Text(r),toCustodian=Text(r);
                var kind=(HandlingKind)r.ReadInt32();var start=Time(r);var end=Time(r);byte tactical=r.ReadByte();if(tactical>1)throw new InvalidDataException("Invalid movement boolean.");
                s.VesselMoves[i]=new VesselHandlingRecord(id,sequence,actor,vessel,from,fromCustodian,to,toCustodian,kind,start,end,tactical==1);
            }
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid movement count.");return n;}
        private static void Text(BinaryWriter w,string t){byte[] b=Utf8.GetBytes(t);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
    }
}
