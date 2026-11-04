using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class PeriodicRiderCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.PeriodicRiders.Length);
            foreach(var x in s.PeriodicRiders.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ProfileId);Text(w,x.FamilyId);Text(w,x.OwnerId);Text(w,x.SourceId);Text(w,x.TargetId);
                Text(w,x.OriginEventId);Text(w,x.DamageType);w.Write(x.ApplyingDc);w.Write(x.ApplicationOrder);Time(w,x.AppliedAt);
                w.Write(x.NextStartSlot);w.Write(x.RemainingTicks);w.Write(x.Suppressed);w.Write(x.EndedAt.HasValue);
                if(x.EndedAt.HasValue)Time(w,x.EndedAt.Value);Text(w,x.EndingMethod);
            }
            w.Write(s.PeriodicImmunities.Length);
            foreach(var x in s.PeriodicImmunities.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.TargetId);Text(w,x.FamilyId);Text(w,x.SourceId);Time(w,x.GrantedAt);w.Write(x.EndedAt.HasValue);
                if(x.EndedAt.HasValue)Time(w,x.EndedAt.Value);
            }
            w.Write(s.SkillTraining.Length);
            foreach(var x in s.SkillTraining.OrderBy(x=>x.ActorId,StringComparer.Ordinal).ThenBy(x=>x.SkillId,StringComparer.Ordinal)) {
                Text(w,x.ActorId);Text(w,x.SkillId);w.Write(x.ProficiencyRank);
            }
            w.Write(s.PeriodicRiderEvents.Length);
            foreach(var x in s.PeriodicRiderEvents.OrderBy(x=>x.Revision).ThenBy(x=>x.EventId,StringComparer.Ordinal)) {
                Text(w,x.EventId);w.Write((int)x.Kind);w.Write((int)x.Outcome);w.Write(x.Revision);Time(w,x.At);w.Write(x.WorldSlot);
                Text(w,x.ActorId);Text(w,x.TargetId);Text(w,x.RiderId);Text(w,x.SourceId);w.Write(x.Flag);w.Write(x.Natural);w.Write(x.Modifier);
                w.Write(x.Dc);w.Write(x.Die);w.Write(x.Amount);w.Write(x.HitPointGain);w.Write((int)x.CheckDegree);w.Write(x.CheckTotal);w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.WordsConsumed);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.PeriodicRiders=new PeriodicRiderRecord[Count(r,PeriodicRiderValidation.MaxRiders)];
            for(int i=0;i<s.PeriodicRiders.Length;i++) {
                string id=Text(r),profile=Text(r),family=Text(r),owner=Text(r),source=Text(r),target=Text(r),origin=Text(r),damage=Text(r);
                int dc=r.ReadInt32();long order=r.ReadInt64();var at=Time(r);long marker=r.ReadInt64();int ticks=r.ReadInt32();bool suppressed=Bool(r);
                RuleTime? ended=Bool(r)?(RuleTime?)Time(r):null;string method=Text(r);
                s.PeriodicRiders[i]=new PeriodicRiderRecord(id,profile,family,owner,source,target,origin,damage,dc,order,at,marker,ticks,suppressed,ended,method);
            }
            s.PeriodicImmunities=new PeriodicFamilyImmunityRecord[Count(r,PeriodicRiderValidation.MaxImmunities)];
            for(int i=0;i<s.PeriodicImmunities.Length;i++) {
                string id=Text(r),target=Text(r),family=Text(r),source=Text(r);var granted=Time(r);RuleTime? ended=Bool(r)?(RuleTime?)Time(r):null;
                s.PeriodicImmunities[i]=new PeriodicFamilyImmunityRecord(id,target,family,source,granted,ended);
            }
            s.SkillTraining=new SkillTrainingRecord[Count(r,PeriodicRiderValidation.MaxSkillRecords)];
            for(int i=0;i<s.SkillTraining.Length;i++)s.SkillTraining[i]=new SkillTrainingRecord(Text(r),Text(r),r.ReadInt32());
            s.PeriodicRiderEvents=new PeriodicRiderEventRecord[Count(r,PeriodicRiderValidation.MaxEvents)];
            for(int i=0;i<s.PeriodicRiderEvents.Length;i++) {
                string id=Text(r);var kind=(PeriodicRiderEventKind)r.ReadInt32();var outcome=(PeriodicRiderOutcome)r.ReadInt32();long revision=r.ReadInt64();var at=Time(r);
                long slot=r.ReadInt64();string actor=Text(r),target=Text(r),rider=Text(r),source=Text(r);bool flag=Bool(r);int natural=r.ReadInt32(),modifier=r.ReadInt32(),dc=r.ReadInt32(),die=r.ReadInt32();
                long amount=r.ReadInt64(),gain=r.ReadInt64();var checkDegree=(PeriodicRiderCheckDegree)r.ReadInt32();long checkTotal=r.ReadInt64();uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();
                s.PeriodicRiderEvents[i]=new PeriodicRiderEventRecord(id,kind,outcome,revision,at,slot,actor,target,rider,source,flag,natural,modifier,dc,die,amount,gain,before,after,words,checkDegree,checkTotal);
            }
        }
        private static int Count(BinaryReader r,int max){int n=r.ReadInt32();if(n<0||n>max)throw new InvalidDataException("Invalid periodic rider count.");return n;}
        private static bool Bool(BinaryReader r){byte b=r.ReadByte();if(b>1)throw new InvalidDataException("Invalid periodic rider flag.");return b==1;}
        private static void Text(BinaryWriter w,string v){byte[] b=Utf8.GetBytes(v);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=Count(r,512);byte[] b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
    }
}
