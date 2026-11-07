using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class ReadyActionCodec
    {
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.ReadyActions.Length);
            foreach(var x in s.ReadyActions.OrderBy(x=>x.PreparedRevision)) {
                SnapshotCodec.WriteText(w,x.Id);SnapshotCodec.WriteText(w,x.PreparationCommandId);
                SnapshotCodec.WriteText(w,x.ActorId);SnapshotCodec.WriteText(w,x.TargetId);SnapshotCodec.WriteText(w,x.WeaponId);
                w.Write(x.TriggerDistanceFeet);w.Write((int)x.Knockout);w.Write(x.PreparedTurnOrdinal);w.Write(x.ExpiresAfterTurnOrdinal);
                w.Write(x.ExpiresAt.Numerator);w.Write(x.ExpiresAt.Denominator);w.Write(x.PreparedRevision);
                w.Write((int)x.Status);w.Write(x.ResolvedRevision);SnapshotCodec.WriteText(w,x.ResolutionId);
            }
            w.Write(s.ReadyOccurrences.Length);
            foreach(var x in s.ReadyOccurrences.OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                SnapshotCodec.WriteText(w,x.Id);SnapshotCodec.WriteText(w,x.ReadyActionId);SnapshotCodec.WriteText(w,x.MoveId);
                SnapshotCodec.WriteText(w,x.OwnerId);SnapshotCodec.WriteText(w,x.TargetId);w.Write(x.OwnerXAtTrigger);w.Write(x.OwnerYAtTrigger);
                w.Write(x.CreatedRevision);w.Write(x.SourceAppliedRevision);w.Write((int)x.Status);w.Write(x.ResolvedRevision);
                SnapshotCodec.WriteText(w,x.ResolutionCommandId);SnapshotCodec.WriteText(w,x.AttackId);
            }
        }

        public static void Read(BinaryReader r,Snapshot s)
        {
            s.ReadyActions=new ReadyActionRecord[SnapshotCodec.ReadCount(r,ReadyActionValidation.MaxActions)];
            for(int i=0;i<s.ReadyActions.Length;i++)
                s.ReadyActions[i]=new ReadyActionRecord(SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),
                    SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),r.ReadInt32(),(AttackKnockoutMode)r.ReadInt32(),r.ReadInt32(),
                    r.ReadInt32(),new RuleTime(r.ReadInt64(),r.ReadInt64()),r.ReadInt64(),(ReadyActionStatus)r.ReadInt32(),
                    r.ReadInt64(),SnapshotCodec.ReadText(r));
            s.ReadyOccurrences=new ReadyOccurrenceRecord[SnapshotCodec.ReadCount(r,ReadyActionValidation.MaxOccurrences)];
            for(int i=0;i<s.ReadyOccurrences.Length;i++)
                s.ReadyOccurrences[i]=new ReadyOccurrenceRecord(SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),
                    SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),r.ReadInt32(),r.ReadInt32(),r.ReadInt64(),r.ReadInt64(),
                    (ReadyOccurrenceStatus)r.ReadInt32(),r.ReadInt64(),SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r));
        }
    }
}
