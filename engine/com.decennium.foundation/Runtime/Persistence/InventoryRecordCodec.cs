using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class InventoryRecordCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.InventoryLots.Length);
            foreach(var x in s.InventoryLots.OrderBy(x=>x.LotId,StringComparer.Ordinal)) {
                Text(w,x.LotId);Text(w,x.ParentId);Text(w,x.OwnerId);Quantity(w,x.CreatedAmount);Time(w,x.CreatedAt);
                w.Write((int)x.Nutrition);Optional(w,x.FreshUntil);w.Write((int)x.Access);
            }
            w.Write(s.Intakes.Length);
            foreach(var x in s.Intakes.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ActorId);Text(w,x.LotId);Text(w,x.ReservationId);Time(w,x.StartedAt);Optional(w,x.EndedAt);w.Write((int)x.Status);
            }
            w.Write(s.Handling.Length);
            foreach(var x in s.Handling.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ActorId);Text(w,x.SourceId);Text(w,x.ChildId);w.Write((int)x.Kind);Time(w,x.StartedAt);Time(w,x.EndedAt);w.Write(x.Tactical);
            }
            w.Write(s.InventoryCombat);Text(w,s.InventoryTurnActor);w.Write(s.InventoryInteractions);
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.InventoryLots=new InventoryLotRecord[Count(r,128)];
            for(int i=0;i<s.InventoryLots.Length;i++)s.InventoryLots[i]=new InventoryLotRecord(Text(r),Text(r),Text(r),Quantity(r),Time(r),
                (NutritionKind)r.ReadInt32(),Optional(r),(InventoryAccess)r.ReadInt32());
            s.Intakes=new IntakeRecord[Count(r,32)];
            for(int i=0;i<s.Intakes.Length;i++)s.Intakes[i]=new IntakeRecord(Text(r),Text(r),Text(r),Text(r),Time(r),Optional(r),(IntakeStatus)r.ReadInt32());
            s.Handling=new HandlingRecord[Count(r,64)];
            for(int i=0;i<s.Handling.Length;i++)s.Handling[i]=new HandlingRecord(Text(r),Text(r),Text(r),Text(r),(HandlingKind)r.ReadInt32(),Time(r),Time(r),Bool(r));
            s.InventoryCombat=Bool(r);s.InventoryTurnActor=Text(r);s.InventoryInteractions=r.ReadInt32();
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid inventory length.");return n;}
        private static void Text(BinaryWriter w,string text){byte[] b=Utf8.GetBytes(text);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid inventory boolean.");return b==1;}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Quantity(BinaryWriter w,RuleQuantity q){w.Write(q.Numerator);w.Write(q.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
        private static void Optional(BinaryWriter w,RuleTime? t){w.Write(t.HasValue);if(t.HasValue)Time(w,t.Value);}
        private static RuleTime? Optional(BinaryReader r)=>Bool(r)?Time(r):(RuleTime?)null;
    }
}
