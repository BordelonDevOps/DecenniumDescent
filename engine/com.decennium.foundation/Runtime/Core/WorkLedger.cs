using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

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
        public RuleQuantity Amount { get; }
        public long Quantity=>Amount.Denominator==1?Amount.Numerator:throw new InvalidOperationException("Fractional amount requires the exact quantity API.");
        public ResourceLot(string id,string unitId,long quantity,string locationId,string custodianId)
            :this(id,unitId,new RuleQuantity(quantity),locationId,custodianId) { }
        public ResourceLot(string id,string unitId,RuleQuantity amount,string locationId,string custodianId)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(unitId)||!Validation.ValidId(locationId)
                ||!Validation.ValidId(custodianId)) throw new ArgumentException("Invalid resource lot.");
            Id=id;UnitId=unitId;Amount=amount;LocationId=locationId;CustodianId=custodianId;
        }
        internal ResourceLot WithAmount(RuleQuantity value) => new ResourceLot(Id,UnitId,value,LocationId,CustodianId);
    }

    public enum ReservationStatus { Reserved, Consumed, Released, Mixed }
    public sealed class ResourceReservation
    {
        public string Id { get; }
        public string JobId { get; }
        public string LotId { get; }
        public RuleQuantity Amount { get; }
        public RuleQuantity ConsumedAmount { get; }
        public RuleQuantity ReleasedAmount { get; }
        public RuleQuantity RemainingAmount { get; }
        public long Quantity=>Amount.Denominator==1?Amount.Numerator:throw new InvalidOperationException("Fractional reservation requires the exact quantity API.");
        public ReservationStatus Status=>RemainingAmount>default(RuleQuantity)?ReservationStatus.Reserved
            :ConsumedAmount==Amount?ReservationStatus.Consumed:ReleasedAmount==Amount?ReservationStatus.Released:ReservationStatus.Mixed;
        public bool LegacyRepresentable=>Amount.Denominator==1&&(ConsumedAmount==Amount||ReleasedAmount==Amount
            ||(ConsumedAmount==default&&ReleasedAmount==default));
        public ResourceReservation(string id,string jobId,string lotId,long quantity,ReservationStatus status=ReservationStatus.Reserved)
            :this(id,jobId,lotId,new RuleQuantity(quantity),status==ReservationStatus.Consumed?new RuleQuantity(quantity):default,
                status==ReservationStatus.Released?new RuleQuantity(quantity):default)
        {if(status!=ReservationStatus.Reserved&&status!=ReservationStatus.Consumed&&status!=ReservationStatus.Released)throw new ArgumentException("Invalid legacy reservation status.");}
        public ResourceReservation(string id,string jobId,string lotId,RuleQuantity amount,RuleQuantity consumed=default,RuleQuantity released=default)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(jobId)||!Validation.ValidId(lotId)||amount==default)throw new ArgumentException("Invalid reservation.");
            BigInteger d=(BigInteger)amount.Denominator*consumed.Denominator*released.Denominator;
            BigInteger n=(BigInteger)amount.Numerator*consumed.Denominator*released.Denominator
                -(BigInteger)consumed.Numerator*amount.Denominator*released.Denominator
                -(BigInteger)released.Numerator*amount.Denominator*consumed.Denominator;
            RemainingAmount=RuleQuantity.FromFraction(n,d);
            Id=id;JobId=jobId;LotId=lotId;Amount=amount;ConsumedAmount=consumed;ReleasedAmount=released;
        }
        internal ResourceReservation WithSettlement(RuleQuantity consumed,RuleQuantity released)=>new ResourceReservation(Id,JobId,LotId,Amount,consumed,released);
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
        public bool RequiresRationalSchema=>Lots.Any(l=>l.Amount.Denominator!=1)||Reservations.Any(r=>!r.LegacyRepresentable);
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
                var reserved=ReservedTotal(group);var stock=byLot[group.Key].Amount;
                if(reserved.Numerator*stock.Denominator>(BigInteger)stock.Numerator*reserved.Denominator)
                    throw new ArgumentException("Reserved quantity exceeds actual stock.");
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
        private static (BigInteger Numerator,BigInteger Denominator) ReservedTotal(IEnumerable<ResourceReservation> claims)
        {
            BigInteger n=0,d=1;
            foreach(var claim in claims){var q=claim.RemainingAmount;n=n*q.Denominator+(BigInteger)q.Numerator*d;d*=q.Denominator;
                var gcd=BigInteger.GreatestCommonDivisor(n,d);n/=gcd;d/=gcd;}
            return(n,d);
        }
        public long Available(string lotId)
        {var value=AvailableAmount(lotId);return value.Denominator==1?value.Numerator:throw new InvalidOperationException("Fractional availability requires the exact quantity API.");}
        public RuleQuantity AvailableAmount(string lotId)
        {
            var lot=Lots.FirstOrDefault(x=>x.Id==lotId)??throw new ArgumentException("Unknown lot.",nameof(lotId));
            var reserved=ReservedTotal(Reservations.Where(x=>x.LotId==lotId && x.Status==ReservationStatus.Reserved));
            return RuleQuantity.FromFraction((BigInteger)lot.Amount.Numerator*reserved.Denominator-reserved.Numerator*lot.Amount.Denominator,
                (BigInteger)lot.Amount.Denominator*reserved.Denominator);
        }
        /// <summary>Atomically book one job's intervals/materials. Source procedure decides when to consume.</summary>
        public WorkLedger Reserve(string jobId,IEnumerable<WorkerInterval> intervals,IEnumerable<ResourceReservation> reservations)
        {
            if(!Validation.ValidId(jobId)||intervals==null||reservations==null) throw new ArgumentException("Invalid job reservation request.");
            var workers=intervals.ToArray();var claims=reservations.ToArray();
            if(workers.Any(x=>x==null||x.JobId!=jobId)||claims.Any(x=>x==null||x.JobId!=jobId||x.ConsumedAmount!=default||x.ReleasedAmount!=default))
                throw new ArgumentException("Request must reserve new records for the same job.");
            return new WorkLedger(Lots,WorkerIntervals.Concat(workers),Reservations.Concat(claims));
        }
        private ResourceReservation Claim(string jobId,string reservationId)
        {
            var claim=Reservations.FirstOrDefault(x=>x.Id==reservationId)??throw new ArgumentException("Unknown reservation.");
            if(claim.JobId!=jobId) throw new ArgumentException("Reservation belongs to another job.");
            return claim;
        }
        public WorkLedger Consume(string jobId,string reservationId)=>ConsumeThrough(jobId,reservationId,Claim(jobId,reservationId).Amount);
        /// <summary>Commit a cumulative consumed amount. Repeating that endpoint is harmless; reversal or spending released quantity rejects.</summary>
        public WorkLedger ConsumeThrough(string jobId,string reservationId,RuleQuantity consumedTotal)
        {
            var claim=Claim(jobId,reservationId);
            if(consumedTotal==claim.ConsumedAmount)return this;
            if(consumedTotal<claim.ConsumedAmount
                ||((BigInteger)consumedTotal.Numerator*claim.ReleasedAmount.Denominator+(BigInteger)claim.ReleasedAmount.Numerator*consumedTotal.Denominator)*claim.Amount.Denominator
                    >(BigInteger)claim.Amount.Numerator*consumedTotal.Denominator*claim.ReleasedAmount.Denominator)throw new ArgumentException("Invalid cumulative consumption.");
            RuleQuantity Debit(RuleQuantity stock)=>RuleQuantity.FromFraction(
                (BigInteger)stock.Numerator*claim.ConsumedAmount.Denominator*consumedTotal.Denominator
                    +(BigInteger)claim.ConsumedAmount.Numerator*stock.Denominator*consumedTotal.Denominator
                    -(BigInteger)consumedTotal.Numerator*stock.Denominator*claim.ConsumedAmount.Denominator,
                (BigInteger)stock.Denominator*claim.ConsumedAmount.Denominator*consumedTotal.Denominator);
            return new WorkLedger(Lots.Select(x=>x.Id==claim.LotId?x.WithAmount(Debit(x.Amount)):x),WorkerIntervals,
                Reservations.Select(x=>x.Id==reservationId?x.WithSettlement(consumedTotal,x.ReleasedAmount):x));
        }
        public WorkLedger Release(string jobId,string reservationId)
        {
            var claim=Claim(jobId,reservationId);
            if(claim.RemainingAmount==default) {
                if(claim.ReleasedAmount>default(RuleQuantity))return this;
                throw new ArgumentException("Consumed reservation cannot be released.");
            }
            return new WorkLedger(Lots,WorkerIntervals,Reservations.Select(x=>x.Id==reservationId
                ?x.WithSettlement(x.ConsumedAmount,x.Amount-x.ConsumedAmount):x));
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
