using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class HavenAppraisalCodec
    {
        public static void Write(BinaryWriter writer,Snapshot snapshot)
        {
            writer.Write(snapshot.HavenAppraisals.Length);
            foreach(var job in snapshot.HavenAppraisals.OrderBy(x=>x.StartRevision)) {
                var basis=job.Basis;
                foreach(string value in new[]{job.Id,job.WorkerId,basis.DeskId,basis.ProviderId,basis.UnitId,basis.DepositVersionId,
                    basis.OwnerId,basis.CustodianId,basis.EvidenceId,basis.ClearanceId,basis.ServiceTermsId,
                    basis.AssessmentContextId})SnapshotCodec.WriteText(writer,value);
                WritePair(writer,basis.Quantity.Numerator,basis.Quantity.Denominator);
                writer.Write(basis.BaseCopper);writer.Write((int)basis.Provenance);writer.Write((int)basis.Demand);
                writer.Write((int)basis.Condition);writer.Write((int)basis.Urgency);
                writer.Write(job.StartRevision);writer.Write(job.UpdatedRevision);
                WritePair(writer,job.StartedAt.Numerator,job.StartedAt.Denominator);
                WritePair(writer,job.UpdatedAt.Numerator,job.UpdatedAt.Denominator);
                WritePair(writer,job.Work.Labor.Numerator,job.Work.Labor.Denominator);
                writer.Write((int)job.Status);SnapshotCodec.WriteText(writer,job.Reason);
                writer.Write(job.ResultCopper.HasValue);
                if(job.ResultCopper.HasValue)WritePair(writer,job.ResultCopper.Value.Numerator,job.ResultCopper.Value.Denominator);
            }
        }

        public static void Read(BinaryReader reader,Snapshot snapshot)
        {
            var jobs=new HavenAppraisalRecord[SnapshotCodec.ReadCount(reader,HavenAppraisalValidation.MaxRecords)];
            for(int i=0;i<jobs.Length;i++) {
                string id=SnapshotCodec.ReadText(reader),worker=SnapshotCodec.ReadText(reader);
                var basis=new HavenAppraisalBasis(SnapshotCodec.ReadText(reader),SnapshotCodec.ReadText(reader),
                    SnapshotCodec.ReadText(reader),SnapshotCodec.ReadText(reader),SnapshotCodec.ReadText(reader),
                    SnapshotCodec.ReadText(reader),SnapshotCodec.ReadText(reader),SnapshotCodec.ReadText(reader),
                    SnapshotCodec.ReadText(reader),SnapshotCodec.ReadText(reader),
                    new RuleQuantity(reader.ReadInt64(),reader.ReadInt64()),reader.ReadInt64(),(MaterialProvenance)reader.ReadInt32(),
                    (MaterialDemand)reader.ReadInt32(),(MaterialCondition)reader.ReadInt32(),(MaterialUrgency)reader.ReadInt32());
                long started=reader.ReadInt64(),updated=reader.ReadInt64();
                var start=ReadTime(reader);var end=ReadTime(reader);var labor=ReadTime(reader);
                var status=(HavenAppraisalStatus)reader.ReadInt32();string reason=SnapshotCodec.ReadText(reader);
                RuleQuantity? result=SnapshotCodec.ReadBool(reader)?new RuleQuantity(reader.ReadInt64(),reader.ReadInt64()):(RuleQuantity?)null;
                jobs[i]=new HavenAppraisalRecord(id,worker,basis,started,updated,start,end,labor,status,reason,result);
            }
            snapshot.HavenAppraisals=jobs;
        }

        private static void WritePair(BinaryWriter writer,long numerator,long denominator)
        {writer.Write(numerator);writer.Write(denominator);}
        private static RuleTime ReadTime(BinaryReader reader)=>new RuleTime(reader.ReadInt64(),reader.ReadInt64());
    }
}
