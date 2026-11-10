using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Schema75 append-only TEST_ONLY treatment history. Derived freshness and protection
    /// deadlines are deliberately absent from the wire format.</summary>
    internal static class HarvestPreservationTreatmentCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string value)
        {byte[] bytes=Utf8.GetBytes(value);w.Write(bytes.Length);w.Write(bytes);}
        private static string Text(BinaryReader r)
        {
            int length=r.ReadInt32();if(length<0||length>96)throw new InvalidDataException("Invalid treatment text length.");
            byte[] bytes=r.ReadBytes(length);if(bytes.Length!=length)throw new EndOfStreamException();return Utf8.GetString(bytes);
        }
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void Quantity(BinaryWriter w,RuleQuantity value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
        private static void Progress(BinaryWriter w,ActiveWorkProgress work)
        {
            w.Write(work.Phases.Count);foreach(var phase in work.Phases)Time(w,phase);
            w.Write(work.CompletedPhases);Time(w,work.Partial);Time(w,work.Labor);
        }
        private static ActiveWorkProgress Progress(BinaryReader r)
        {
            int count=SnapshotCodec.ReadCount(r,ActiveWorkProgress.MaxPhases);
            var phases=new RuleTime[count];for(int i=0;i<count;i++)phases[i]=Time(r);
            return new ActiveWorkProgress(phases,r.ReadInt32(),Time(r),Time(r));
        }
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.HarvestPreservationTreatmentAttempts.Length);
            foreach(var x in s.HarvestPreservationTreatmentAttempts.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.WorkerId);Text(w,x.SkillId);Text(w,x.InventoryLotId);Quantity(w,x.TreatedAmount);
                Text(w,x.ContainerId);Text(w,x.ToolId);Text(w,x.SupplyLotId);Text(w,x.TargetReservationId);Text(w,x.SupplyReservationId);
                Time(w,x.StartedAt);Time(w,x.UpdatedAt);Progress(w,x.Work);w.Write((int)x.Status);
                w.Write(x.CompletedAt.HasValue);if(x.CompletedAt.HasValue)Time(w,x.CompletedAt.Value);
                w.Write(x.SealedAt.HasValue);if(x.SealedAt.HasValue)Time(w,x.SealedAt.Value);
                w.Write(x.AbilityModifier);w.Write(x.ProficiencyRank);w.Write(x.ProficiencyBonus);w.Write(x.Natural);w.Write((int)x.Degree);
                w.Write(x.RandomBefore);w.Write(x.RandomAfter);w.Write(x.RandomWordsConsumed);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.HarvestPreservationTreatmentAttempts=new HarvestPreservationTreatmentAttemptRecord[
                SnapshotCodec.ReadCount(r,HarvestPreservationTreatmentValidation.MaxRecords)];
            for(int i=0;i<s.HarvestPreservationTreatmentAttempts.Length;i++) {
                string id=Text(r),worker=Text(r),skill=Text(r),lot=Text(r);RuleQuantity amount=Quantity(r);
                string container=Text(r),tool=Text(r),supply=Text(r),targetReservation=Text(r),supplyReservation=Text(r);
                RuleTime started=Time(r),updated=Time(r);ActiveWorkProgress work=Progress(r);
                var status=(HarvestPreservationTreatmentStatus)r.ReadInt32();
                RuleTime? completed=r.ReadBoolean()?Time(r):(RuleTime?)null;RuleTime? sealedAt=r.ReadBoolean()?Time(r):(RuleTime?)null;
                int ability=r.ReadInt32(),rank=r.ReadInt32(),proficiency=r.ReadInt32(),natural=r.ReadInt32();
                var degree=(HarvestPreservationTreatmentDegree)r.ReadInt32();
                uint before=r.ReadUInt32(),after=r.ReadUInt32();long words=r.ReadInt64();
                s.HarvestPreservationTreatmentAttempts[i]=new HarvestPreservationTreatmentAttemptRecord(id,worker,skill,lot,
                    amount,container,tool,supply,targetReservation,supplyReservation,started,updated,work,status,completed,sealedAt,
                    ability,rank,proficiency,natural,degree,before,after,words);
            }
        }
    }
}
