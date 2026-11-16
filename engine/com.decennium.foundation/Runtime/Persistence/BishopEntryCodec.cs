using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class BishopEntryCodec
    {
        internal static void Write(BinaryWriter w,BishopEntryRecord entry)
        {
            SnapshotCodec.WriteText(w,entry.DeclarationDigest);
            var p=entry.Departure;w.Write(p!=null);
            if(p!=null) {
                SnapshotCodec.WriteText(w,p.RestId);SnapshotCodec.WriteText(w,p.RiteCommandId);w.Write(p.RiteRevision);
                SnapshotCodec.WriteText(w,p.StepCommandId);w.Write(p.StepRevision);Time(w,p.StartedAt);
                SnapshotCodec.WriteText(w,p.CompletionCommandId);w.Write(p.CompletedRevision);Time(w,p.CompletedAt);
            }
            w.Write(entry.Invocations.Count);
            foreach(var use in entry.Invocations) {
                Text(w,use.CommandId);w.Write(use.Revision);Text(w,use.Turn.ActorId);Text(w,use.Turn.EpochId);
                w.Write(use.Turn.LocalStart);w.Write(use.Turn.GlobalStart);Time(w,use.At);
                w.Write(use.Choice.TargetIds.Count);foreach(string id in use.Choice.TargetIds)Text(w,id);
                Text(w,use.Choice.CureTargetId);w.Write((int)use.Choice.CurePreference);
                w.Write(use.RpBefore);w.Write(use.ConvictionBefore);w.Write(use.DissonanceBefore);w.Write(use.Die);
                w.Write(use.RandomBefore);w.Write(use.RandomAfter);w.Write(use.WordsConsumed);
                foreach(var recipient in use.Recipients){w.Write(recipient.HpBefore);w.Write(recipient.Potential);w.Write(recipient.HpAfter);}
                Time(w,use.CureAt.Time);w.Write(use.CureAt.Phase);Text(w,use.CureOperationId);
                w.Write(use.EndedApplicationIds.Count);foreach(string id in use.EndedApplicationIds)Text(w,id);
            }
            AuraOfFaithCodec.Write(w,entry);
            w.Write(entry.Dispels.Count);
            foreach(var x in entry.Dispels){Text(w,x.CommandId);w.Write(x.Revision);Time(w,x.At);Text(w,x.ObservationId);
                Text(w,x.DetectionEffectId);Text(w,x.EndedEffectId);Text(w,x.OriginalCastId);w.Write(x.OriginalCastRevision);}
        }
        internal static BishopEntryRecord Read(BinaryReader r)
        {
            string digest=SnapshotCodec.ReadText(r);BishopDepartureProof proof=null;
            if(SnapshotCodec.ReadBool(r))proof=new BishopDepartureProof(SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),r.ReadInt64(),
                SnapshotCodec.ReadText(r),r.ReadInt64(),Time(r),SnapshotCodec.ReadText(r),r.ReadInt64(),Time(r));
            var uses=new DivineInvocationRecord[Count(r,128)];
            for(int i=0;i<uses.Length;i++) {
                string command=Text(r);long revision=r.ReadInt64();var turn=new SpellTurnIdentity(Text(r),Text(r),r.ReadInt64(),r.ReadInt64());
                var at=Time(r);var targets=new string[Count(r,3)];for(int n=0;n<targets.Length;n++)targets[n]=Text(r);
                var choice=new DivineInvocationRequest(targets,Text(r),(RadianceCurePreference)r.ReadInt32());
                int rp=r.ReadInt32(),conviction=r.ReadInt32(),dissonance=r.ReadInt32(),die=r.ReadInt32();
                uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();
                var rows=targets.Select(id=>new InvocationHealingRecord(id,r.ReadInt64(),r.ReadInt64(),r.ReadInt64())).ToArray();
                var stamp=new ConditionStamp(Time(r),r.ReadInt32());string operation=Text(r);
                var ended=new string[Count(r,128)];for(int n=0;n<ended.Length;n++)ended[n]=Text(r);
                uses[i]=new DivineInvocationRecord(command,revision,turn,at,choice,rp,conviction,dissonance,die,before,after,words,rows,stamp,operation,ended);
            }
            AuraOfFaithCodec.Read(r,out var saves,out var healing);
            var dispels=new BishopDispelRecord[Count(r,128)];
            for(int i=0;i<dispels.Length;i++)dispels[i]=new BishopDispelRecord(Text(r),r.ReadInt64(),Time(r),Text(r),Text(r),Text(r),Text(r),r.ReadInt64());
            return new BishopEntryRecord(digest,proof,uses,saves,healing,dispels);
        }
        private static int Count(BinaryReader r,int maximum){int count=r.ReadInt32();if(count<0||count>maximum)throw new ArgumentException("Invalid Bishop history count.");return count;}
        private static void Text(BinaryWriter w,string text)=>SnapshotCodec.WriteText(w,text);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w,RuleTime at){w.Write(at.Numerator);w.Write(at.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
    }
}
