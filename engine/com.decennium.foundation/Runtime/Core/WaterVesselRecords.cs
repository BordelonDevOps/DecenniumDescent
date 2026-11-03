using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum WaterVesselProfile { Waterskin, OrdinaryFlask }
    public enum WaterFillStatus { Working, Paused, Complete, Cancelled }
    /// <summary>A distinct physical vessel. Capacity and tare come from its selected source profile.
    /// This bounded schema records stable custody; a future movement procedure must preserve that history.</summary>
    public sealed class WaterVesselRecord
    {
        public string Id { get; }
        public WaterVesselProfile Profile { get; }
        public string OwnerId { get; }
        public string LocationId { get; }
        public string CustodianId { get; }
        public WaterVesselRecord(string id,WaterVesselProfile profile,string ownerId,string locationId,string custodianId)
        {
            if(!Validation.ValidId(id)||!Enum.IsDefined(typeof(WaterVesselProfile),profile)||!Validation.ValidId(ownerId)
                ||!Validation.ValidId(locationId)||!Validation.ValidId(custodianId))throw new ArgumentException("Invalid water vessel.");
            Id=id;Profile=profile;OwnerId=ownerId;LocationId=locationId;CustodianId=custodianId;
        }
    }
    /// <summary>Physical contents reference the existing ledger. No second liquid quantity is stored.</summary>
    public sealed class VesselContentRecord
    {
        public string LotId { get; }
        public string VesselId { get; }
        public VesselContentRecord(string lotId,string vesselId)
        {if(!Validation.ValidId(lotId)||!Validation.ValidId(vesselId))throw new ArgumentException("Invalid vessel content.");LotId=lotId;VesselId=vesselId;}
    }
    /// <summary>Working and paused jobs retain the declared destination-capacity reservation.
    /// The same amount has a separate source reservation in WorkLedger; it is never nutrition credit.</summary>
    public sealed class WaterFillRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public string SourceLotId { get; }
        public string DestinationId { get; }
        public string ReservationId { get; }
        public RuleQuantity Amount { get; }
        public RuleTime StartedAt { get; }
        public RuleTime Progress { get; }
        public RuleTime? EndedAt { get; }
        public WaterFillStatus Status { get; }
        public string OutputLotId { get; }
        public bool Pending=>Status==WaterFillStatus.Working||Status==WaterFillStatus.Paused;
        public WaterFillRecord(string id,string workerId,string sourceLotId,string destinationId,string reservationId,RuleQuantity amount,
            RuleTime startedAt,RuleTime progress,RuleTime? endedAt,WaterFillStatus status,string outputLotId="")
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(workerId)||!Validation.ValidId(sourceLotId)||!Validation.ValidId(destinationId)
                ||!Validation.ValidId(reservationId)||amount==default||!Enum.IsDefined(typeof(WaterFillStatus),status)
                ||outputLotId==null||(outputLotId!=""&&!Validation.ValidId(outputLotId))
                ||((status==WaterFillStatus.Working||status==WaterFillStatus.Paused)==endedAt.HasValue)
                ||((status==WaterFillStatus.Complete)!=(outputLotId!=""))||(endedAt.HasValue&&endedAt.Value<startedAt))
                throw new ArgumentException("Invalid water-filling job.");
            Id=id;WorkerId=workerId;SourceLotId=sourceLotId;DestinationId=destinationId;ReservationId=reservationId;Amount=amount;
            StartedAt=startedAt;Progress=progress;EndedAt=endedAt;Status=status;OutputLotId=outputLotId;
        }
    }
    public static class WaterVesselValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.Vessels==null||s.VesselContents==null||s.WaterFills==null||s.Vessels.Length>8||s.VesselContents.Length>128||s.WaterFills.Length>32
                ||s.Vessels.Any(x=>x==null)||s.VesselContents.Any(x=>x==null)||s.WaterFills.Any(x=>x==null))throw new ArgumentException("Invalid vessel collections.");
            if(s.SchemaVersion!=Snapshot.VesselSchema) {
                if(s.Vessels.Length!=0||s.VesselContents.Length!=0||s.WaterFills.Length!=0)throw new ArgumentException("Vessels require explicit schema5.");return;
            }
            if(s.Vessels.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.Vessels.Length
                ||s.Vessels.Any(v=>s.Actors.Any(x=>x.Id==v.Id)||s.Objects.Any(x=>x.Id==v.Id)||s.Work.Lots.Any(x=>x.Id==v.Id))
                ||s.VesselContents.Select(x=>x.LotId).Distinct(StringComparer.Ordinal).Count()!=s.VesselContents.Length
                ||s.WaterFills.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.WaterFills.Length
                ||s.WaterFills.Select(x=>x.ReservationId).Distinct(StringComparer.Ordinal).Count()!=s.WaterFills.Length
                ||s.WaterFills.Where(x=>x.Status==WaterFillStatus.Complete).Select(x=>x.OutputLotId).Distinct(StringComparer.Ordinal).Count()!=s.WaterFills.Count(x=>x.Status==WaterFillStatus.Complete))
                throw new ArgumentException("Duplicate or aliased vessel identity.");
            foreach(var row in s.VesselContents) {
                var vessel=s.Vessels.SingleOrDefault(v=>v.Id==row.VesselId);var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==row.LotId);
                if(vessel==null||lot==null||lot.LocationId!=vessel.Id||lot.CustodianId!=vessel.CustodianId
                    ||s.InventoryLots.Single(x=>x.LotId==lot.Id).Nutrition!=NutritionKind.WaterPints)throw new ArgumentException("Invalid contained water.");
            }
            if(s.Work.Lots.Any(l=>s.Vessels.Any(v=>v.Id==l.LocationId)&&!s.VesselContents.Any(x=>x.LotId==l.Id)))throw new ArgumentException("Unrecorded vessel content.");
            var otherJobs=s.Crops.SelectMany(c=>c.Tasks).Select(t=>t.Id).Concat(s.Intakes.Select(x=>x.Id)).Concat(s.Handling.Select(x=>x.Id)).ToArray();
            foreach(var job in s.WaterFills) {
                var claim=s.Work.Reservations.SingleOrDefault(r=>r.Id==job.ReservationId);
                if(otherJobs.Contains(job.Id)||!s.Actors.Any(a=>a.Id==job.WorkerId)||!s.Vessels.Any(v=>v.Id==job.DestinationId)
                    ||!s.Work.Lots.Any(l=>l.Id==job.SourceLotId)||claim==null||claim.JobId!=job.Id||claim.LotId!=job.SourceLotId||claim.Amount!=job.Amount
                    ||job.StartedAt>s.RuleClock||(job.EndedAt.HasValue&&job.EndedAt.Value>s.RuleClock)
                    ||(job.Status==WaterFillStatus.Complete&&!s.VesselContents.Any(x=>x.LotId==job.OutputLotId&&x.VesselId==job.DestinationId)))
                    throw new ArgumentException("Invalid filling references or chronology.");
            }
        }
    }
}
