using System.IO;

namespace Decennium.Foundation
{
    internal static class HuntingTrapCodec
    {
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.HuntingTrapDeployments.Length);
            foreach(var x in s.HuntingTrapDeployments) {
                SnapshotCodec.WriteText(w,x.Id);SnapshotCodec.WriteText(w,x.TrapItemId);SnapshotCodec.WriteText(w,x.SetterId);
                w.Write(x.AnchorX);w.Write(x.AnchorY);w.Write(x.ArmedRevision);Time(w,x.ArmedAt);w.Write((int)x.Status);SnapshotCodec.WriteText(w,x.TriggerId);
            }
            w.Write(s.HuntingTrapActions.Length);
            foreach(var x in s.HuntingTrapActions) {
                SnapshotCodec.WriteText(w,x.Id);w.Write((int)x.Kind);SnapshotCodec.WriteText(w,x.ActorId);SnapshotCodec.WriteText(w,x.TrapItemId);
                SnapshotCodec.WriteText(w,x.TargetActorId);SnapshotCodec.WriteText(w,x.DeploymentId);Time(w,x.StartedAt);
                w.Write(x.EndedAt.HasValue);if(x.EndedAt.HasValue)Time(w,x.EndedAt.Value);w.Write((int)x.Status);w.Write(x.Tactical);
                w.Write(x.AutomaticFailure);w.Write(x.Natural);w.Write(x.Modifier);w.Write(x.Dc);w.Write(x.Total);w.Write(x.CheckSuccess);
                w.Write(x.Damage);w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.WordsConsumed);
            }
            w.Write(s.HuntingTrapTriggers.Length);
            foreach(var x in s.HuntingTrapTriggers) {
                SnapshotCodec.WriteText(w,x.Id);SnapshotCodec.WriteText(w,x.DeploymentId);SnapshotCodec.WriteText(w,x.EntryId);
                w.Write((int)x.EntryKind);SnapshotCodec.WriteText(w,x.RouteId);w.Write(x.RouteStartedRevision);
                w.Write(x.RouteProgress.Numerator);w.Write(x.RouteProgress.Denominator);SnapshotCodec.WriteText(w,x.EntrantId);
                w.Write(x.CreatedRevision);w.Write(x.ResolvedRevision);
                w.Write(x.SourceAppliedRevision);Time(w,x.At);w.Write((int)x.Status);w.Write(x.AutomaticFailure);w.Write(x.Natural);
                w.Write(x.Modifier);w.Write(x.Dc);w.Write(x.Total);w.Write(x.SaveSuccess);w.Write(x.DamageRoll);w.Write(x.DamageApplied);
                SnapshotCodec.WriteText(w,x.TetherId);w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.WordsConsumed);
            }
            w.Write(s.HuntingTrapTethers.Length);
            foreach(var x in s.HuntingTrapTethers) {
                SnapshotCodec.WriteText(w,x.Id);SnapshotCodec.WriteText(w,x.TriggerId);SnapshotCodec.WriteText(w,x.DeploymentId);
                SnapshotCodec.WriteText(w,x.TrapItemId);SnapshotCodec.WriteText(w,x.ActorId);w.Write(x.AnchorX);w.Write(x.AnchorY);
                w.Write((int)x.Status);w.Write(x.ReleasedRevision);SnapshotCodec.WriteText(w,x.ReleaseActionId);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.HuntingTrapDeployments=new HuntingTrapDeploymentRecord[SnapshotCodec.ReadCount(r,HuntingTrapValidation.MaxDeployments)];
            for(int i=0;i<s.HuntingTrapDeployments.Length;i++)s.HuntingTrapDeployments[i]=new HuntingTrapDeploymentRecord(
                SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),r.ReadInt32(),r.ReadInt32(),r.ReadInt64(),Time(r),
                (HuntingTrapDeploymentStatus)r.ReadInt32(),SnapshotCodec.ReadText(r));
            s.HuntingTrapActions=new HuntingTrapActionRecord[SnapshotCodec.ReadCount(r,HuntingTrapValidation.MaxActions)];
            for(int i=0;i<s.HuntingTrapActions.Length;i++) {
                string id=SnapshotCodec.ReadText(r);var kind=(HuntingTrapActionKind)r.ReadInt32();string actor=SnapshotCodec.ReadText(r);
                string trap=SnapshotCodec.ReadText(r),target=SnapshotCodec.ReadText(r),deployment=SnapshotCodec.ReadText(r);var started=Time(r);
                RuleTime? ended=r.ReadBoolean()?(RuleTime?)Time(r):null;var status=(HuntingTrapActionStatus)r.ReadInt32();bool tactical=r.ReadBoolean();
                bool automatic=r.ReadBoolean();int natural=r.ReadInt32(),modifier=r.ReadInt32(),dc=r.ReadInt32();long total=r.ReadInt64();bool success=r.ReadBoolean();
                int damage=r.ReadInt32();uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();
                s.HuntingTrapActions[i]=new HuntingTrapActionRecord(id,kind,actor,trap,target,deployment,started,ended,status,tactical,
                    automatic,natural,modifier,dc,total,success,damage,before,after,words);
            }
            s.HuntingTrapTriggers=new HuntingTrapTriggerRecord[SnapshotCodec.ReadCount(r,HuntingTrapValidation.MaxTriggers)];
            for(int i=0;i<s.HuntingTrapTriggers.Length;i++) {
                string id=SnapshotCodec.ReadText(r),deployment=SnapshotCodec.ReadText(r),entry=SnapshotCodec.ReadText(r);
                var kind=(HuntingTrapEntryKind)r.ReadInt32();string routeId=SnapshotCodec.ReadText(r);long routeStarted=r.ReadInt64();
                var routeProgress=new RuleQuantity(r.ReadInt64(),r.ReadInt64());string entrant=SnapshotCodec.ReadText(r);
                long created=r.ReadInt64(),resolved=r.ReadInt64(),source=r.ReadInt64();var at=Time(r);
                var status=(HuntingTrapTriggerStatus)r.ReadInt32();bool automatic=r.ReadBoolean();int natural=r.ReadInt32(),modifier=r.ReadInt32(),dc=r.ReadInt32();
                long total=r.ReadInt64();bool success=r.ReadBoolean();int damage=r.ReadInt32();long applied=r.ReadInt64();string tether=SnapshotCodec.ReadText(r);
                uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();
                s.HuntingTrapTriggers[i]=new HuntingTrapTriggerRecord(id,deployment,entry,kind,entrant,created,resolved,source,at,status,
                    automatic,natural,modifier,dc,total,success,damage,applied,tether,before,after,words,routeId,routeStarted,routeProgress);
            }
            s.HuntingTrapTethers=new HuntingTrapTetherRecord[SnapshotCodec.ReadCount(r,HuntingTrapValidation.MaxTethers)];
            for(int i=0;i<s.HuntingTrapTethers.Length;i++)s.HuntingTrapTethers[i]=new HuntingTrapTetherRecord(
                SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),SnapshotCodec.ReadText(r),
                r.ReadInt32(),r.ReadInt32(),(HuntingTrapTetherStatus)r.ReadInt32(),r.ReadInt64(),SnapshotCodec.ReadText(r));
        }
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
    }
}
