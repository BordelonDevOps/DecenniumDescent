using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ManufacturingCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string value){var b=Utf8.GetBytes(value);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);var b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid manufacturing collection length.");return n;}
        private static bool Boolean(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid manufacturing boolean.");return b==1;}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void OptionalTime(BinaryWriter w,RuleTime? t){w.Write(t.HasValue);if(t.HasValue)Time(w,t.Value);}
        private static RuleTime? OptionalTime(BinaryReader r)=>Boolean(r)?Time(r):(RuleTime?)null;
        private static void Strings(BinaryWriter w,System.Collections.Generic.IReadOnlyList<string> values){w.Write(values.Count);foreach(string x in values)Text(w,x);}
        private static string[] Strings(BinaryReader r){var a=new string[Count(r,32)];for(int i=0;i<a.Length;i++)a[i]=Text(r);return a;}
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.ManufacturingAdvance!=null);if(s.ManufacturingAdvance!=null){var a=s.ManufacturingAdvance;Time(w,a.Target);w.Write(a.ExitAfterSlot);Text(w,a.CommandId);w.Write(a.CommandRevision);Text(w,a.OutgoingSlotId);w.Write(a.NextPhase);}
            w.Write(s.ManufacturingOrders.Length);
            foreach(var j in s.ManufacturingOrders.OrderBy(x=>x.Id,StringComparer.Ordinal)){
                Text(w,j.Id);Text(w,j.WorkerId);Text(w,j.RecipeId);w.Write(j.MaterialSet);w.Write(j.ExtraVials);w.Write(j.TakeTen);w.Write((int)j.Status);
                w.Write(j.Work.Phases.Count);foreach(var p in j.Work.Phases)Time(w,p);w.Write(j.Work.CompletedPhases);Time(w,j.Work.Partial);Time(w,j.Work.Labor);
                Time(w,j.StartedAt);Time(w,j.UpdatedAt);OptionalTime(w,j.StabilizedAt);w.Write(j.First);w.Write(j.Second);w.Write(j.Natural);
                w.Write((int)j.Quality);w.Write((int)j.Choice);w.Write(j.RetainedCatalyst);w.Write(j.Mishap);w.Write(j.XpAward);Text(w,j.FindingId);Text(w,j.MishapIncidentId);
            }
            w.Write(s.Trades.Length);foreach(var t in s.Trades.OrderBy(x=>x.WorkerId,StringComparer.Ordinal).ThenBy(x=>x.TradeId,StringComparer.Ordinal)){
                Text(w,t.WorkerId);Text(w,t.TradeId);w.Write(t.Level);w.Write(t.Xp);Strings(w,t.SuccessfulRecipes);Strings(w,t.Findings);
            }
            w.Write(s.AlchemyDoses.Length);foreach(var d in s.AlchemyDoses.OrderBy(x=>x.Id,StringComparer.Ordinal)){
                foreach(string text in new[]{d.Id,d.OrderId,d.RecipeId,d.MakerId,d.OwnerId,d.CustodianId,d.LocationId})Text(w,text);
                Time(w,d.CreatedAt);w.Write(d.MaximumHp);w.Write(d.Hp);OptionalTime(w,d.UsedAt);Text(w,d.UserId);Text(w,d.RecipientId);
                w.Write(d.FirstD4);w.Write(d.SecondD4);w.Write(d.PotentialHealing);w.Write(d.ActualHealing);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            if(Boolean(r)){s.ManufacturingAdvance=new ManufacturingAdvanceRecord(Time(r),Boolean(r),Text(r),r.ReadInt64(),Text(r));if(r.ReadInt32()!=1)throw new InvalidDataException("Unsupported manufacturing continuation phase.");}else s.ManufacturingAdvance=null;
            s.ManufacturingOrders=new ManufacturingOrderRecord[Count(r,ManufacturingValidation.MaxOrders)];
            for(int i=0;i<s.ManufacturingOrders.Length;i++){
                string id=Text(r),worker=Text(r),recipe=Text(r);int set=r.ReadInt32(),extra=r.ReadInt32();bool take=Boolean(r);var status=(ManufacturingStatus)r.ReadInt32();
                var phases=new RuleTime[Count(r,ActiveWorkProgress.MaxPhases)];for(int p=0;p<phases.Length;p++)phases[p]=Time(r);
                var work=new ActiveWorkProgress(phases,r.ReadInt32(),Time(r),Time(r));var start=Time(r);var updated=Time(r);var stabilized=OptionalTime(r);
                s.ManufacturingOrders[i]=new ManufacturingOrderRecord(id,worker,recipe,set,extra,take,status,work,start,updated,stabilized,
                    r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),(CraftQuality)r.ReadInt32(),(CraftQualityChoice)r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),Text(r),Text(r));
            }
            s.Trades=new TradeProgressRecord[Count(r,ManufacturingValidation.MaxTrades)];for(int i=0;i<s.Trades.Length;i++)s.Trades[i]=new TradeProgressRecord(Text(r),Text(r),r.ReadInt32(),r.ReadInt32(),Strings(r),Strings(r));
            s.AlchemyDoses=new AlchemyDoseRecord[Count(r,ManufacturingValidation.MaxDoses)];
            for(int i=0;i<s.AlchemyDoses.Length;i++){
                string id=Text(r),order=Text(r),recipe=Text(r),maker=Text(r),owner=Text(r),custodian=Text(r),location=Text(r);var created=Time(r);int max=r.ReadInt32(),hp=r.ReadInt32();var used=OptionalTime(r);string user=Text(r),recipient=Text(r);
                s.AlchemyDoses[i]=new AlchemyDoseRecord(id,order,recipe,maker,owner,custodian,location,created,max,hp,used,user,recipient,r.ReadInt32(),r.ReadInt32(),r.ReadInt64(),r.ReadInt64());
            }
        }
    }
}
