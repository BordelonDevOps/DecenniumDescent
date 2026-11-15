using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class FrightenedCodec
    {
        internal static void Write(BinaryWriter w, Snapshot state)
        {
            w.Write(state.WarriorAbilityChoices.Length);
            foreach (var x in state.WarriorAbilityChoices.OrderBy(x => x.ActorId, StringComparer.Ordinal)) {
                Text(w,x.ActorId); w.Write((int)x.Ability); Text(w,x.SourceRevision); Text(w,x.EntitlementId); w.Write(x.AcquiredRevision);
            }
            w.Write(state.AbilityRecharges.Length);
            foreach (var x in state.AbilityRecharges.OrderBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.AbilityId, StringComparer.Ordinal)) {
                Text(w,x.ActorId); Text(w,x.AbilityId); Text(w,x.EpochId); w.Write(x.LastLocalStart); Time(w,x.LastStartAt); w.Write(x.Remaining);
            }
            w.Write(state.FrightenedUses.Length);
            foreach (var x in state.FrightenedUses) {
                Text(w,x.Id); Text(w,x.CommandId); w.Write(x.Revision); Text(w,x.ActorId); Text(w,x.SourceId); Text(w,x.SourceRevision);
                Text(w,x.EpochId); w.Write(x.LocalStart); Time(w,x.At); w.Write(x.Dc); w.Write(x.TargetIds.Count);
                foreach (string target in x.TargetIds) Text(w,target);
            }
            w.Write(state.FrightenedSaves.Length);
            foreach (var x in state.FrightenedSaves) {
                Text(w,x.Id); Text(w,x.UseId); Text(w,x.TargetId); Text(w,x.ApplicationId); w.Write(x.Revision); Time(w,x.At);
                w.Write(x.Repeat); w.Write(x.Dc); w.Write(x.Modifier); w.Write(x.First); w.Write(x.Second); w.Write(x.Natural);
                w.Write(x.Success); w.Write(x.AdmissionPrevented); w.Write(x.RandomBefore); w.Write(x.RandomAfter); w.Write(x.WordsConsumed);
            }
            w.Write(state.FrightenedTimings.Length);
            foreach (var x in state.FrightenedTimings) {
                Text(w,x.ApplicationId); Text(w,x.UseId); Text(w,x.TargetId); Text(w,x.EpochId); w.Write(x.TargetLocalEnd);
                Stamp(w,x.RepeatAt); Stamp(w,x.FinalAt);
            }
        }
        internal static void Read(BinaryReader r, Snapshot state)
        {
            state.WarriorAbilityChoices = new WarriorAbilityChoiceRecord[SnapshotCodec.ReadCount(r,16)];
            for(int i=0;i<state.WarriorAbilityChoices.Length;i++) state.WarriorAbilityChoices[i]=new WarriorAbilityChoiceRecord(
                Text(r),(CharacterAbility)r.ReadInt32(),Text(r),Text(r),r.ReadInt64());
            state.AbilityRecharges = new CharacterAbilityRechargeRecord[SnapshotCodec.ReadCount(r,128)];
            for(int i=0;i<state.AbilityRecharges.Length;i++) state.AbilityRecharges[i]=new CharacterAbilityRechargeRecord(
                Text(r),Text(r),Text(r),r.ReadInt64(),Time(r),r.ReadInt32());
            state.FrightenedUses = new FrightenedUseRecord[SnapshotCodec.ReadCount(r,128)];
            for(int i=0;i<state.FrightenedUses.Length;i++) {
                string id=Text(r),command=Text(r); long revision=r.ReadInt64();
                string actor=Text(r),source=Text(r),sourceRevision=Text(r),epoch=Text(r);long local=r.ReadInt64();var at=Time(r);int dc=r.ReadInt32();
                var targets=new string[SnapshotCodec.ReadCount(r,3)];for(int t=0;t<targets.Length;t++)targets[t]=Text(r);
                if(!targets.SequenceEqual(targets.OrderBy(x=>x,StringComparer.Ordinal)))throw new InvalidDataException("Noncanonical fear target order.");
                state.FrightenedUses[i]=new FrightenedUseRecord(id,command,revision,actor,source,sourceRevision,epoch,local,at,dc,targets);
            }
            state.FrightenedSaves = new FrightenedSaveRecord[SnapshotCodec.ReadCount(r,768)];
            for(int i=0;i<state.FrightenedSaves.Length;i++) state.FrightenedSaves[i]=new FrightenedSaveRecord(
                Text(r),Text(r),Text(r),Text(r),r.ReadInt64(),Time(r),Bool(r),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),r.ReadInt32(),
                r.ReadInt32(),Bool(r),Bool(r),r.ReadUInt32(),r.ReadUInt32(),r.ReadInt64());
            state.FrightenedTimings = new FrightenedTimingRecord[SnapshotCodec.ReadCount(r,384)];
            for(int i=0;i<state.FrightenedTimings.Length;i++) state.FrightenedTimings[i]=new FrightenedTimingRecord(
                Text(r),Text(r),Text(r),Text(r),r.ReadInt64(),Stamp(r),Stamp(r));
        }
        private static void Text(BinaryWriter w,string value)=>SnapshotCodec.WriteText(w,value);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Stamp(BinaryWriter w,ConditionStamp value){Time(w,value.Time);w.Write(value.Phase);}
        private static ConditionStamp Stamp(BinaryReader r)=>new ConditionStamp(Time(r),r.ReadInt32());
        private static bool Bool(BinaryReader r){byte value=r.ReadByte();if(value>1)throw new InvalidDataException("Invalid fear flag.");return value==1;}
    }
}
