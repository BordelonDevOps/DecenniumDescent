using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class SupplyCacheCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string x){var b=Utf8.GetBytes(x);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=r.ReadInt32();if(n<0||n>512)throw new InvalidDataException("Invalid cache identity length.");var b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid cache record count.");return n;}
        private static bool Bool(BinaryReader r){byte x=r.ReadByte();if(x>1)throw new InvalidDataException("Invalid cache boolean.");return x==1;}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void OptionalTime(BinaryWriter w,RuleTime? t){w.Write(t.HasValue);if(t.HasValue)Time(w,t.Value);}
        private static RuleTime? OptionalTime(BinaryReader r)=>Bool(r)?Time(r):(RuleTime?)null;
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.SupplyCaches.Length);
            foreach(var c in s.SupplyCaches.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,c.Id);Text(w,c.OwnerId);w.Write(c.X);w.Write(c.Y);w.Write(c.Locked);w.Write(c.Open);w.Write(c.ToolsProficient);Text(w,c.RationLotId);Text(w,c.WaterskinId);
            }
            w.Write(s.SupplyCacheEquipment.Length);
            foreach(var e in s.SupplyCacheEquipment.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,e.Id);w.Write((int)e.Kind);Text(w,e.OwnerId);Text(w,e.LocationId);Text(w,e.CustodianId);
            }
            w.Write(s.SupplyCacheAttempts.Length);
            foreach(var a in s.SupplyCacheAttempts.OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,a.Id);Text(w,a.CacheId);Text(w,a.ActorId);Text(w,a.EquipmentId);w.Write((int)a.Method);Time(w,a.StartedAt);OptionalTime(w,a.EndedAt);
                w.Write((int)a.Status);w.Write(a.Natural);w.Write(a.Modifier);w.Write(a.Tactical);w.Write(a.AutomaticFailure);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.SupplyCaches=new SupplyCacheRecord[Count(r,1)];
            for(int i=0;i<s.SupplyCaches.Length;i++)s.SupplyCaches[i]=new SupplyCacheRecord(Text(r),Text(r),r.ReadInt32(),r.ReadInt32(),Bool(r),Bool(r),Bool(r),Text(r),Text(r));
            s.SupplyCacheEquipment=new SupplyCacheEquipmentRecord[Count(r,8)];
            for(int i=0;i<s.SupplyCacheEquipment.Length;i++)s.SupplyCacheEquipment[i]=new SupplyCacheEquipmentRecord(Text(r),(SupplyCacheEquipmentKind)r.ReadInt32(),Text(r),Text(r),Text(r));
            s.SupplyCacheAttempts=new SupplyCacheAttemptRecord[Count(r,128)];
            for(int i=0;i<s.SupplyCacheAttempts.Length;i++)s.SupplyCacheAttempts[i]=new SupplyCacheAttemptRecord(Text(r),Text(r),Text(r),Text(r),
                (SupplyCacheUnlockMethod)r.ReadInt32(),Time(r),OptionalTime(r),(SupplyCacheAttemptStatus)r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),Bool(r),Bool(r));
        }
    }
}
