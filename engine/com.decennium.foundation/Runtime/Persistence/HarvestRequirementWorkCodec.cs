using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Schema74 append-only TEST_ONLY work-adapter section. Preservation remains derived.</summary>
    internal static class HarvestRequirementWorkCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string value)
        {byte[] bytes=Utf8.GetBytes(value);w.Write(bytes.Length);w.Write(bytes);}
        private static string Text(BinaryReader r)
        {
            int length=r.ReadInt32();if(length<0||length>96)throw new InvalidDataException("Invalid harvest requirement text length.");
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
            var phases=new RuleTime[SnapshotCodec.ReadCount(r,ActiveWorkProgress.MaxPhases)];
            for(int i=0;i<phases.Length;i++)phases[i]=Time(r);
            return new ActiveWorkProgress(phases,r.ReadInt32(),Time(r),Time(r));
        }
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.HarvestRequirementWorks.Length);
            foreach(var x in s.HarvestRequirementWorks.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.WorkerId);Text(w,x.InventoryLotId);Text(w,x.ReservationId);
                Quantity(w,x.RequiredAmount);w.Write((int)x.Requirement);w.Write((int)x.Status);w.Write((int)x.PauseReason);
                Time(w,x.StartedAt);Time(w,x.UpdatedAt);Progress(w,x.Work);
            }
        }
        public static void Read(BinaryReader r,Snapshot s)
        {
            s.HarvestRequirementWorks=new HarvestRequirementWorkRecord[SnapshotCodec.ReadCount(r,HarvestRequirementWorkValidation.MaxRecords)];
            for(int i=0;i<s.HarvestRequirementWorks.Length;i++) {
                string id=Text(r),worker=Text(r),lot=Text(r),reservation=Text(r);var amount=Quantity(r);
                var requirement=(HarvestIngredientRequirement)r.ReadInt32();var status=(HarvestRequirementWorkStatus)r.ReadInt32();
                var reason=(HarvestRequirementPauseReason)r.ReadInt32();var started=Time(r);var updated=Time(r);var progress=Progress(r);
                s.HarvestRequirementWorks[i]=new HarvestRequirementWorkRecord(id,worker,lot,reservation,amount,
                    requirement,status,reason,started,updated,progress);
            }
        }
    }
}
