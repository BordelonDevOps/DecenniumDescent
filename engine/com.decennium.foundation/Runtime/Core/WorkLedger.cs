using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>An exclusive active interval [Start,End). Passive elapsed time does not book a worker.</summary>
    public sealed class WorkerInterval
    {
        public string Id { get; }
        public string JobId { get; }
        public string WorkerId { get; }
        public RuleTime Start { get; }
        public RuleTime End { get; }
        public WorkerInterval(string id,string jobId,string workerId,RuleTime start,RuleTime end)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(jobId)||!Validation.ValidId(workerId)||end<=start)
                throw new ArgumentException("Invalid exclusive worker interval.");
            Id=id;JobId=jobId;WorkerId=workerId;Start=start;End=end;
        }
    }

    /// <summary>Quantity in an explicitly selected unit; the ledger does not convert units or create content.</summary>
    public sealed class ResourceLot
    {
        public string Id { get; }
        public string UnitId { get; }
        public string LocationId { get; }
        public string CustodianId { get; }
        public long Quantity { get; }
        public ResourceLot(string id,string unitId,long quantity,string locationId,string custodianId)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(unitId)||!Validation.ValidId(locationId)
                ||!Validation.ValidId(custodianId)||quantity<0) throw new ArgumentException("Invalid resource lot.");
            Id=id;UnitId=unitId;Quantity=quantity;LocationId=locationId;CustodianId=custodianId;
        }
        internal ResourceLot WithQuantity(long value) => new ResourceLot(Id,UnitId,value,LocationId,CustodianId);
    }

    public enum ReservationStatus { Reserved, Consumed, Released }
    public sealed class ResourceReservation
    {
        public string Id { get; }
        public string JobId { get; }
        public string LotId { get; }
        public long Quantity { get; }
        public ReservationStatus Status { get; }
        public ResourceReservation(string id,string jobId,string lotId,long quantity,ReservationStatus status=ReservationStatus.Reserved)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(jobId)||!Validation.ValidId(lotId)||quantity<=0
                ||!Enum.IsDefined(typeof(ReservationStatus),status)) throw new ArgumentException("Invalid reservation.");
            Id=id;JobId=jobId;LotId=lotId;Quantity=quantity;Status=status;
        }
        internal ResourceReservation WithStatus(ReservationStatus value) => new ResourceReservation(Id,JobId,LotId,Quantity,value);
    }

    /// <summary>
    /// Persistent-data component, not job-rule authorization. A trusted command policy validates workers,
    /// access, facilities, units, time credit and procedure-specific costs before applying these changes.
    /// Completed reservation IDs are retained so repeated settlement cannot spend or refund again.
    /// </summary>
    public sealed class WorkLedger
    {
        public const int MaxRecords=4096; // Serialization/session bound, not a gameplay capacity.
        public IReadOnlyList<ResourceLot> Lots { get; }
        public IReadOnlyList<WorkerInterval> WorkerIntervals { get; }
        public IReadOnlyList<ResourceReservation> Reservations { get; }
        public WorkLedger(IEnumerable<ResourceLot> lots=null,IEnumerable<WorkerInterval> workerIntervals=null,
            IEnumerable<ResourceReservation> reservations=null)
        {
            ResourceLot[] material=(lots??Array.Empty<ResourceLot>()).ToArray();
            WorkerInterval[] workers=(workerIntervals??Array.Empty<WorkerInterval>()).ToArray();
            ResourceReservation[] claims=(reservations??Array.Empty<ResourceReservation>()).ToArray();
            if(material.Length>MaxRecords||workers.Length>MaxRecords||claims.Length>MaxRecords
                ||material.Any(x=>x==null)||workers.Any(x=>x==null)||claims.Any(x=>x==null))
                throw new ArgumentException("Invalid work-ledger records or session capacity exceeded.");
            Unique(material.Select(x=>x.Id));Unique(workers.Select(x=>x.Id));Unique(claims.Select(x=>x.Id));
            var byLot=material.ToDictionary(x=>x.Id,StringComparer.Ordinal);
            foreach(var claim in claims)
                if(!byLot.ContainsKey(claim.LotId)) throw new ArgumentException("Reservation references an unknown lot.");
            foreach(var group in claims.Where(x=>x.Status==ReservationStatus.Reserved).GroupBy(x=>x.LotId,StringComparer.Ordinal)) {
                long remaining=byLot[group.Key].Quantity;
                foreach(var claim in group) {
                    if(claim.Quantity>remaining) throw new ArgumentException("Reserved quantity exceeds actual stock.");
                    remaining-=claim.Quantity;
                }
            }
            foreach(var group in workers.GroupBy(x=>x.WorkerId,StringComparer.Ordinal)) {
                RuleTime? priorEnd=null;
                foreach(var interval in group.OrderBy(x=>x.Start).ThenBy(x=>x.End)) {
                    if(priorEnd.HasValue && interval.Start<priorEnd.Value)
                        throw new ArgumentException("Worker has overlapping exclusive activities.");
                    priorEnd=interval.End;
                }
            }
            Lots=Array.AsReadOnly(material.OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray());
            WorkerIntervals=Array.AsReadOnly(workers.OrderBy(x=>x.Start).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray());
            Reservations=Array.AsReadOnly(claims.OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray());
        }
        private static void Unique(IEnumerable<string> ids)
        {
            var seen=new HashSet<string>(StringComparer.Ordinal);
            if(ids.Any(x=>!seen.Add(x))) throw new ArgumentException("Duplicate work-ledger identity.");
        }
        public long Available(string lotId)
        {
            var lot=Lots.FirstOrDefault(x=>x.Id==lotId)??throw new ArgumentException("Unknown lot.",nameof(lotId));
            long remaining=lot.Quantity;
            foreach(var claim in Reservations.Where(x=>x.LotId==lotId && x.Status==ReservationStatus.Reserved)) remaining-=claim.Quantity;
            return remaining;
        }
        /// <summary>Atomically book one job's intervals/materials. Source procedure decides when to consume.</summary>
        public WorkLedger Reserve(string jobId,IEnumerable<WorkerInterval> intervals,IEnumerable<ResourceReservation> reservations)
        {
            if(!Validation.ValidId(jobId)||intervals==null||reservations==null) throw new ArgumentException("Invalid job reservation request.");
            var workers=intervals.ToArray();var claims=reservations.ToArray();
            if(workers.Any(x=>x==null||x.JobId!=jobId)||claims.Any(x=>x==null||x.JobId!=jobId||x.Status!=ReservationStatus.Reserved))
                throw new ArgumentException("Request must reserve new records for the same job.");
            return new WorkLedger(Lots,WorkerIntervals.Concat(workers),Reservations.Concat(claims));
        }
        public WorkLedger Consume(string jobId,string reservationId) => Settle(jobId,reservationId,ReservationStatus.Consumed);
        public WorkLedger Release(string jobId,string reservationId) => Settle(jobId,reservationId,ReservationStatus.Released);
        private WorkLedger Settle(string jobId,string reservationId,ReservationStatus target)
        {
            var claim=Reservations.FirstOrDefault(x=>x.Id==reservationId)??throw new ArgumentException("Unknown reservation.");
            if(claim.JobId!=jobId) throw new ArgumentException("Reservation belongs to another job.");
            if(claim.Status==target) return this; // Same settlement is a harmless replay.
            if(claim.Status!=ReservationStatus.Reserved) throw new ArgumentException("Reservation already settled differently.");
            var lots=Lots.Select(x=>x.Id==claim.LotId && target==ReservationStatus.Consumed
                ? x.WithQuantity(checked(x.Quantity-claim.Quantity)) : x);
            return new WorkLedger(lots,WorkerIntervals,Reservations.Select(x=>x.Id==reservationId?x.WithStatus(target):x));
        }
        /// <summary>Remove unused scheduled work only; prior work and material settlements remain recorded.</summary>
        public WorkLedger CancelFutureWork(string jobId,RuleTime at)
        {
            if(!Validation.ValidId(jobId)) throw new ArgumentException("Invalid job identity.");
            var intervals=new List<WorkerInterval>();
            foreach(var row in WorkerIntervals) {
                if(row.JobId!=jobId || row.End<=at) intervals.Add(row);
                else if(row.Start<at) intervals.Add(new WorkerInterval(row.Id,row.JobId,row.WorkerId,row.Start,at));
            }
            return new WorkLedger(Lots,intervals,Reservations);
        }
    }
}
