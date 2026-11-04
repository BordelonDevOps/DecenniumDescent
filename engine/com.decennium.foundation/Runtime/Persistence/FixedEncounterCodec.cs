using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class FixedEncounterCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.Encounter!=null);
            if(s.Encounter!=null)WriteRecord(w,s.Encounter);
            w.Write(s.EncounterDashes.Length);foreach(var dash in s.EncounterDashes.OrderBy(x=>x.Revision)){w.Write(dash.Revision);w.Write(dash.TurnOrdinal);Text(w,dash.ActorId);}
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            byte present=r.ReadByte();if(present>1)throw new InvalidDataException("Invalid encounter presence.");
            if(present==1)s.Encounter=ReadRecord(r);
            s.EncounterDashes=new EncounterDashRecord[Count(r,128)];for(int i=0;i<s.EncounterDashes.Length;i++)s.EncounterDashes[i]=new EncounterDashRecord(r.ReadInt64(),r.ReadInt32(),Text(r));
        }
        internal static void WriteRecord(BinaryWriter w,FixedEncounterRecord e)
        {
            Text(w,e.Id);w.Write(e.Origin.Numerator);w.Write(e.Origin.Denominator);
            w.Write(e.Order.Count);foreach(string id in e.Order)Text(w,id);
            w.Write(e.StartRevisions.Count);foreach(long revision in e.StartRevisions)w.Write(revision);
        }
        internal static FixedEncounterRecord ReadRecord(BinaryReader r)
        {
            string id=Text(r);var origin=new RuleTime(r.ReadInt64(),r.ReadInt64());var order=new string[Count(r,64)];for(int i=0;i<order.Length;i++)order[i]=Text(r);
            var starts=new long[Count(r,128)];for(int i=0;i<starts.Length;i++)starts[i]=r.ReadInt64();return new FixedEncounterRecord(id,origin,order,starts);
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid encounter count.");return n;}
        private static void Text(BinaryWriter w,string t){byte[] b=Utf8.GetBytes(t);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
