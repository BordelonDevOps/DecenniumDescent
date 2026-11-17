using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class ClericSettlementCodec
    {
        internal static void Write(BinaryWriter w, Snapshot s)
        {
            var d = s.ClericMilestone;
            Text(w,d.MilestoneId); Text(w,d.ActorId); Text(w,d.ObjectiveId); Text(w,d.SourceRevision); w.Write(d.DeclaredRevision);
            Text(w,d.FirstEncounterId); Text(w,d.LaterEncounterId); Text(w,d.SpecimenId); Text(w,d.RecipeId); Text(w,d.Digest);
            w.Write(s.ClericObjective != null);
            if (s.ClericObjective != null) {
                var x = s.ClericObjective;
                Text(w,x.DeclarationDigest); Text(w,x.FirstClosureCommand); w.Write(x.FirstClosureRevision);
                Text(w,x.BatchOrderId); w.Write(x.BatchSettlementRevision); Text(w,x.LaterClosureCommand); w.Write(x.Revision); Time(w,x.At);
            }
            w.Write(s.ClericInvocationPath != null);
            if (s.ClericInvocationPath != null) {
                var x = s.ClericInvocationPath;
                Text(w,x.ActorId); Text(w,x.PathId); Text(w,x.SourceRevision); Text(w,x.MilestoneId); w.Write(x.AcquiredRevision);
            }
            var capacity = s.ConvictionCapacity;
            Text(w,capacity.ActorId); Text(w,capacity.SourceRevision); Text(w,capacity.PoolMilestoneId); w.Write(capacity.PoolAcquiredRevision);
            w.Write(capacity.Maximum); w.Write(capacity.CurrentAvailable);
            w.Write(s.RadianceUses.Length);
            foreach (var x in s.RadianceUses) {
                Text(w,x.RiteCommandId); w.Write(x.Revision); Text(w,x.ActorId); Text(w,x.TargetId); Text(w,x.SourceRevision);
                Text(w,x.EpochId); w.Write(x.LocalStart); w.Write(x.PhaseFirstTurn); w.Write(x.GlobalStart); Time(w,x.At.Time); w.Write(x.At.Phase);
                w.Write(x.BaseHpAfter); w.Write(x.AdditionalPotential); w.Write(x.HpAfter); w.Write((int)x.CurePreference); Text(w,x.CureOperationId);
                w.Write(x.EndedApplicationIds.Count); foreach (string id in x.EndedApplicationIds) Text(w,id);
                if(s.Consecration!=null)w.Write(x.PreRadianceHp());
            }
        }
        internal static void Read(BinaryReader r, Snapshot s, bool consecration = false)
        {
            s.ClericMilestone = new ClericMilestoneDeclaration(Text(r),Text(r),Text(r),Text(r),r.ReadInt64(),
                Text(r),Text(r),Text(r),Text(r),Text(r));
            if (SnapshotCodec.ReadBool(r)) s.ClericObjective = new ClericObjectiveCompletion(Text(r),Text(r),r.ReadInt64(),
                Text(r),r.ReadInt64(),Text(r),r.ReadInt64(),Time(r));
            if (SnapshotCodec.ReadBool(r)) s.ClericInvocationPath = new ClericInvocationPathRecord(Text(r),Text(r),Text(r),Text(r),r.ReadInt64());
            s.ConvictionCapacity = new ConvictionCapacityRecord(Text(r),Text(r),Text(r),r.ReadInt64());
            if (r.ReadInt32() != s.ConvictionCapacity.Maximum || SnapshotCodec.ReadBool(r))
                throw new InvalidDataException("Unsupported Conviction capacity or fabricated balance.");
            s.RadianceUses = new RadianceUseRecord[SnapshotCodec.ReadCount(r,128)];
            for (int i=0;i<s.RadianceUses.Length;i++) {
                string rite=Text(r); long revision=r.ReadInt64(); string actor=Text(r),target=Text(r),source=Text(r),epoch=Text(r);
                long local=r.ReadInt64(); int first=r.ReadInt32(),global=r.ReadInt32(); var at=new ConditionStamp(Time(r),r.ReadInt32());
                long baseHp=r.ReadInt64(),potential=r.ReadInt64(),hp=r.ReadInt64(); var preference=(RadianceCurePreference)r.ReadInt32();
                string operation=Text(r); var ids=new string[SnapshotCodec.ReadCount(r,ConditionJournal.MaxOperations)];
                for(int j=0;j<ids.Length;j++)ids[j]=Text(r);
                if(!ids.SequenceEqual(ids.OrderBy(x=>x,StringComparer.Ordinal)))throw new InvalidDataException("Noncanonical Radiance cure identities.");
                s.RadianceUses[i]=new RadianceUseRecord(rite,revision,actor,target,source,epoch,local,first,global,at,baseHp,potential,hp,preference,operation,ids,consecration?r.ReadInt64():baseHp);
            }
        }
        private static void Text(BinaryWriter w,string value)=>SnapshotCodec.WriteText(w,value);
        private static string Text(BinaryReader r)=>SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
    }
}
