using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class WaterVesselCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.Vessels.Length);foreach(var v in s.Vessels.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,v.Id);w.Write((int)v.Profile);Text(w,v.OwnerId);Text(w,v.LocationId);Text(w,v.CustodianId);
            }
            w.Write(s.VesselContents.Length);foreach(var c in s.VesselContents.OrderBy(x=>x.LotId,StringComparer.Ordinal)){Text(w,c.LotId);Text(w,c.VesselId);}
            w.Write(s.WaterFills.Length);foreach(var j in s.WaterFills.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,j.Id);Text(w,j.WorkerId);Text(w,j.SourceLotId);Text(w,j.DestinationId);Text(w,j.ReservationId);
                w.Write(j.Amount.Numerator);w.Write(j.Amount.Denominator);Time(w,j.StartedAt);Time(w,j.Progress);
                w.Write(j.EndedAt.HasValue);if(j.EndedAt.HasValue)Time(w,j.EndedAt.Value);w.Write((int)j.Status);Text(w,j.OutputLotId);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.Vessels=new WaterVesselRecord[Count(r,8)];for(int i=0;i<s.Vessels.Length;i++)s.Vessels[i]=new WaterVesselRecord(Text(r),(WaterVesselProfile)r.ReadInt32(),Text(r),Text(r),Text(r));
            s.VesselContents=new VesselContentRecord[Count(r,128)];for(int i=0;i<s.VesselContents.Length;i++)s.VesselContents[i]=new VesselContentRecord(Text(r),Text(r));
            s.WaterFills=new WaterFillRecord[Count(r,32)];for(int i=0;i<s.WaterFills.Length;i++) {
                string id=Text(r),worker=Text(r),source=Text(r),dest=Text(r),claim=Text(r);var amount=new RuleQuantity(r.ReadInt64(),r.ReadInt64());
                RuleTime start=Time(r),progress=Time(r);RuleTime? end=Bool(r)?Time(r):(RuleTime?)null;
                s.WaterFills[i]=new WaterFillRecord(id,worker,source,dest,claim,amount,start,progress,end,(WaterFillStatus)r.ReadInt32(),Text(r));
            }
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid vessel count.");return n;}
        private static void Text(BinaryWriter w,string text){byte[] b=Utf8.GetBytes(text);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid vessel boolean.");return b==1;}
    }
}
