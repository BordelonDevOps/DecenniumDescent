using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class ActorLifeCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.Characters.Length);
            foreach(var c in s.Characters.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,c.ActorId);Text(w,c.ProfileId);foreach(int score in c.Abilities)w.Write(score);
                w.Write(c.Levels.Count);foreach(var level in c.Levels){Text(w,level.ClassName);w.Write(level.BaseHp);}
            }
            w.Write(s.Lives.Length);
            foreach(var l in s.Lives.OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                Text(w,l.ActorId);w.Write(l.MaximumHp);w.Write(l.Hp);w.Write(l.TemporaryHp);
                w.Write(l.LinkedInjuries.Count);foreach(int i in l.LinkedInjuries)w.Write(i);
                w.Write(l.Stable);w.Write(l.Dead);w.Write(l.UsesDeathSaves);w.Write(l.DeathSuccesses);w.Write(l.DeathFailures);
                w.Write(l.StableUntil.HasValue);if(l.StableUntil.HasValue)Time(w,l.StableUntil.Value);
                w.Write(l.LastDeathTurn);w.Write(l.Prone);w.Write(l.HeldItems.Count);foreach(string id in l.HeldItems)Text(w,id);
            }
            w.Write(s.LifeEvents.Length);
            foreach(var e in s.LifeEvents) {
                Text(w,e.ActorId);w.Write(e.Revision);Time(w,e.At);w.Write((int)e.Kind);w.Write(e.TurnOrdinal);w.Write(e.Natural);
                w.Write(e.RecoveryD4);w.Write(e.RandomBefore);w.Write(e.RandomAfter);w.Write(e.WordsConsumed);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.Characters=new ActorCharacterRecord[Count(r,64)];
            for(int i=0;i<s.Characters.Length;i++) {
                string actor=Text(r),profile=Text(r);var scores=new int[6];for(int j=0;j<6;j++)scores[j]=r.ReadInt32();
                var levels=new CharacterLevelFact[Count(r,20)];for(int j=0;j<levels.Length;j++)levels[j]=new CharacterLevelFact(Text(r),r.ReadInt32());
                s.Characters[i]=new ActorCharacterRecord(actor,profile,scores,levels);
            }
            s.Lives=new ActorLifeRecord[Count(r,64)];
            for(int i=0;i<s.Lives.Length;i++) {
                string actor=Text(r);long max=r.ReadInt64(),hp=r.ReadInt64(),temp=r.ReadInt64();var injuries=new int[Count(r,3)];
                for(int j=0;j<injuries.Length;j++)injuries[j]=r.ReadInt32();
                bool stable=Bool(r),dead=Bool(r),uses=Bool(r);int successes=r.ReadInt32(),failures=r.ReadInt32();
                RuleTime? until=Bool(r)?Time(r):(RuleTime?)null;long last=r.ReadInt64();bool prone=Bool(r);var held=new string[Count(r,32)];
                for(int j=0;j<held.Length;j++)held[j]=Text(r);
                s.Lives[i]=new ActorLifeRecord(actor,max,hp,temp,injuries,stable,dead,uses,successes,failures,until,last,prone,held);
            }
            s.LifeEvents=new ActorLifeEvent[Count(r,256)];
            for(int i=0;i<s.LifeEvents.Length;i++)s.LifeEvents[i]=new ActorLifeEvent(Text(r),r.ReadInt64(),Time(r),(LifeEventKind)r.ReadInt32(),
                r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64());
        }
        private static void Time(BinaryWriter w,RuleTime time){w.Write(time.Numerator);w.Write(time.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid actor life flag.");return b==1;}
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid actor life count.");return n;}
        private static void Text(BinaryWriter w,string text){byte[] b=Utf8.GetBytes(text);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,96);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
    }
}
