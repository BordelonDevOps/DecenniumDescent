using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class CharacterAdvancementCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.CharacterMilestones.Length);
            foreach(var m in s.CharacterMilestones.OrderBy(x=>x.AwardedRevision).ThenBy(x=>x.ActorId,StringComparer.Ordinal).ThenBy(x=>x.MilestoneId,StringComparer.Ordinal)) {
                Text(w,m.MilestoneId);Text(w,m.ActorId);w.Write(m.AwardedRevision);w.Write(m.ConsumedRevision);
            }
            w.Write(s.CharacterHitDice.Length);
            foreach(var d in s.CharacterHitDice.OrderBy(x=>x.ActorId,StringComparer.Ordinal).ThenBy(x=>x.LevelOrdinal)) {
                Text(w,d.ActorId);w.Write(d.LevelOrdinal);Text(w,d.ClassName);w.Write(d.DieSize);w.Write(d.Spent);
            }
            w.Write(s.CharacterFeatureGrants.Length);
            foreach(var g in s.CharacterFeatureGrants.OrderBy(x=>x.GrantedRevision).ThenBy(x=>x.ActorId,StringComparer.Ordinal).ThenBy(x=>x.FeatureId,StringComparer.Ordinal)) {
                Text(w,g.ActorId);Text(w,g.FeatureId);Text(w,g.ClassName);w.Write(g.ClassLevel);Text(w,g.MilestoneId);w.Write(g.GrantedRevision);
            }
            w.Write(s.CharacterAdvancements.Length);
            foreach(var a in s.CharacterAdvancements.OrderBy(x=>x.Revision)) {
                Text(w,a.ActorId);Text(w,a.MilestoneId);w.Write(a.Revision);w.Write(a.PreviousTotalLevel);w.Write(a.NewTotalLevel);
                Text(w,a.ClassName);w.Write(a.ClassLevel);w.Write(a.BaseHpGain);w.Write((int)a.HitPointMethod);
                w.Write(a.MaximumHpBefore);w.Write(a.MaximumHpAfter);w.Write(a.CurrentHpBefore);w.Write(a.CurrentHpAfter);Text(w,a.FeatureOne);Text(w,a.FeatureTwo);
            }
            w.Write(s.CharacterFeatureRuntime.Length);
            foreach(var f in s.CharacterFeatureRuntime.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,f.ActorId);w.Write(f.LastRegularStart);w.Write(f.BonusActionAvailable);w.Write(f.RepositionRechargeRemaining);
                w.Write(f.RepositionTurnOrdinal);w.Write(f.RepositionBudgetRemaining);
            }
            w.Write(s.TacticalCovers.Length);
            foreach(var c in s.TacticalCovers.OrderBy(x=>x.Id,StringComparer.Ordinal)){Text(w,c.Id);w.Write(c.X);w.Write(c.Y);}
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.CharacterMilestones=new CharacterMilestoneRecord[Count(r,256)];
            for(int i=0;i<s.CharacterMilestones.Length;i++)s.CharacterMilestones[i]=new CharacterMilestoneRecord(Text(r),Text(r),r.ReadInt64(),r.ReadInt64());
            s.CharacterHitDice=new CharacterHitDieRecord[Count(r,1280)];
            for(int i=0;i<s.CharacterHitDice.Length;i++)s.CharacterHitDice[i]=new CharacterHitDieRecord(Text(r),r.ReadInt32(),Text(r),r.ReadInt32(),Bool(r));
            s.CharacterFeatureGrants=new CharacterFeatureGrantRecord[Count(r,256)];
            for(int i=0;i<s.CharacterFeatureGrants.Length;i++)s.CharacterFeatureGrants[i]=new CharacterFeatureGrantRecord(Text(r),Text(r),Text(r),r.ReadInt32(),Text(r),r.ReadInt64());
            s.CharacterAdvancements=new CharacterAdvancementRecord[Count(r,128)];
            for(int i=0;i<s.CharacterAdvancements.Length;i++)s.CharacterAdvancements[i]=new CharacterAdvancementRecord(Text(r),Text(r),r.ReadInt64(),r.ReadInt32(),r.ReadInt32(),
                Text(r),r.ReadInt32(),r.ReadInt32(),(HitPointGainMethod)r.ReadInt32(),r.ReadInt64(),r.ReadInt64(),r.ReadInt64(),r.ReadInt64(),Text(r),Text(r));
            s.CharacterFeatureRuntime=new CharacterFeatureRuntimeRecord[Count(r,64)];
            for(int i=0;i<s.CharacterFeatureRuntime.Length;i++)s.CharacterFeatureRuntime[i]=new CharacterFeatureRuntimeRecord(Text(r),r.ReadInt32(),Bool(r),r.ReadInt32(),r.ReadInt32(),r.ReadInt64());
            s.TacticalCovers=new TacticalCoverRecord[Count(r,64)];
            for(int i=0;i<s.TacticalCovers.Length;i++)s.TacticalCovers[i]=new TacticalCoverRecord(Text(r),r.ReadInt32(),r.ReadInt32());
        }
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid advancement flag.");return b==1;}
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid advancement count.");return n;}
        private static void Text(BinaryWriter w,string text){byte[] b=Utf8.GetBytes(text);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
