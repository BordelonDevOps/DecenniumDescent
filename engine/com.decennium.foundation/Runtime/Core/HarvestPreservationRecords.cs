using System;
using System.Linq;

namespace Decennium.Foundation
{
    // Ordinary and Spoiled are query-only projections for the agreed eligibility matrix.
    // The TEST_ONLY reservation/work adapter below deliberately persists Fresh only.
    public enum HarvestIngredientRequirement { Fresh = 1, Ordinary = 2, Spoiled = 3 }
    public enum HarvestRequirementWorkStatus { Working = 1, Paused = 2 }
    public enum HarvestRequirementPauseReason { None = 0, Explicit = 1, IngredientNotFresh = 2, WorkerUnavailable = 3 }

    /// <summary>Read-only preservation facts derived from one physical inventory descendant and its
    /// extracted harvest root. No age, stage or value is copied into saved state.</summary>
    public sealed class HarvestPreservationView
    {
        public string InventoryLotId { get; }
        public string HarvestUnitId { get; }
        public RuleTime EvaluatedAt { get; }
        public HarvestPreservationState State { get; }
        public RuleQuantity ValueMultiplier { get; }

        internal HarvestPreservationView(string inventoryLotId,string harvestUnitId,RuleTime evaluatedAt,
            HarvestPreservationState state,RuleQuantity valueMultiplier)
        {
            InventoryLotId=inventoryLotId;HarvestUnitId=harvestUnitId;EvaluatedAt=evaluatedAt;
            State=state;ValueMultiplier=valueMultiplier;
        }
    }

    /// <summary>Schema-74 projection over the existing harvest and inventory authorities.</summary>
    public static class HarvestPreservationRules
    {
        public static bool SatisfiesRequirement(HarvestPreservationView view,HarvestIngredientRequirement requirement)
        {
            if(view==null||!Enum.IsDefined(typeof(HarvestIngredientRequirement),requirement))return false;
            switch(requirement) {
                case HarvestIngredientRequirement.Fresh:return view.State==HarvestPreservationState.Fresh;
                case HarvestIngredientRequirement.Ordinary:return view.State==HarvestPreservationState.Fresh
                    ||view.State==HarvestPreservationState.Degraded;
                case HarvestIngredientRequirement.Spoiled:return view.State==HarvestPreservationState.Spoiled;
                default:return false;
            }
        }

        public static bool TryProject(Snapshot s,string inventoryLotId,out HarvestPreservationView view)
        {
            view=null;
            if(s==null||s.SchemaVersion<Snapshot.HarvestPreservationSchema||s.InventoryLots==null
                ||s.HarvestUnits==null||s.Work==null||!Validation.ValidId(inventoryLotId))return false;
            var lot=s.InventoryLots.SingleOrDefault(x=>x.LotId==inventoryLotId);
            var resource=s.Work.Lots.SingleOrDefault(x=>x.Id==inventoryLotId);
            if(lot==null||resource==null||lot.Nutrition!=NutritionKind.None||resource.UnitId!="mass-pound")return false;

            var seen=new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal){lot.LotId};
            var root=lot;
            while(root.ParentId!="") {
                if(!seen.Add(root.ParentId))return false;
                root=s.InventoryLots.SingleOrDefault(x=>x.LotId==root.ParentId);
                if(root==null)return false;
            }
            var unit=s.HarvestUnits.SingleOrDefault(x=>x.Id==root.LotId);
            if(unit==null||unit.Status!=HarvestUnitStatus.Extracted
                ||root.FreshUntil!=unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds))return false;
            var physical=s.PortableEquipment?.SingleOrDefault(x=>x.LinkKind==PortableLinkKind.InventoryLot
                &&x.LinkedId==lot.LotId);
            if(physical==null||physical.Id!=lot.LotId||physical.MassBasis!=PortableMassBasis.GenericPounds)return false;

            HarvestPreservationState state=unit.PreservationAt(s.RuleClock);
            RuleQuantity multiplier=state==HarvestPreservationState.Fresh?new RuleQuantity(1)
                :state==HarvestPreservationState.Degraded?new RuleQuantity(1,2):default;
            view=new HarvestPreservationView(lot.LotId,unit.Id,s.RuleClock,state,multiplier);
            return true;
        }
    }

    /// <summary>Persisted TEST_ONLY ingredient/work binding. Work progress is the existing exact
    /// ActiveWorkProgress record; current preservation remains a derived query.</summary>
    public sealed class HarvestRequirementWorkRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public string InventoryLotId { get; }
        public string ReservationId { get; }
        public RuleQuantity RequiredAmount { get; }
        public HarvestIngredientRequirement Requirement { get; }
        public HarvestRequirementWorkStatus Status { get; }
        public HarvestRequirementPauseReason PauseReason { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }

        public HarvestRequirementWorkRecord(string id,string workerId,string inventoryLotId,string reservationId,
            RuleQuantity requiredAmount,HarvestIngredientRequirement requirement,HarvestRequirementWorkStatus status,
            HarvestRequirementPauseReason pauseReason,RuleTime startedAt,RuleTime updatedAt,ActiveWorkProgress work)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(workerId)||!Validation.ValidId(inventoryLotId)
                ||!Validation.ValidId(reservationId)||requiredAmount==default
                ||!Enum.IsDefined(typeof(HarvestIngredientRequirement),requirement)
                ||!Enum.IsDefined(typeof(HarvestRequirementWorkStatus),status)
                ||!Enum.IsDefined(typeof(HarvestRequirementPauseReason),pauseReason)||updatedAt<startedAt||work==null)
                throw new ArgumentException("Invalid harvest requirement work binding.");
            Id=id;WorkerId=workerId;InventoryLotId=inventoryLotId;ReservationId=reservationId;
            RequiredAmount=requiredAmount;Requirement=requirement;Status=status;PauseReason=pauseReason;
            StartedAt=startedAt;UpdatedAt=updatedAt;Work=work;
        }

        public HarvestRequirementWorkRecord With(RuleTime at,ActiveWorkProgress work,
            HarvestRequirementWorkStatus status,HarvestRequirementPauseReason pauseReason)
            =>new HarvestRequirementWorkRecord(Id,WorkerId,InventoryLotId,ReservationId,RequiredAmount,
                Requirement,status,pauseReason,StartedAt,at,work);
    }

    public static class HarvestRequirementWorkValidation
    {
        public const int MaxRecords=16;

        private static RuleTime Add(RuleTime first,RuleTime second)
        {
            var sum=new RuleQuantity(first.Numerator,first.Denominator)+new RuleQuantity(second.Numerator,second.Denominator);
            return new RuleTime(sum.Numerator,sum.Denominator);
        }

        private static RuleTime Subtract(RuleTime first,RuleTime second)
        {
            if(second>first)throw new ArgumentException("Negative work interval.");
            var difference=new RuleQuantity(first.Numerator,first.Denominator)-new RuleQuantity(second.Numerator,second.Denominator);
            return new RuleTime(difference.Numerator,difference.Denominator);
        }

        public static void Validate(Snapshot s)
        {
            if(s.HarvestRequirementWorks==null||s.HarvestRequirementWorks.Length>MaxRecords
                ||s.HarvestRequirementWorks.Any(x=>x==null)
                ||s.HarvestRequirementWorks.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.HarvestRequirementWorks.Length)
                throw new ArgumentException("Invalid harvest requirement work collection.");
            if(s.SchemaVersion<Snapshot.HarvestPreservationSchema) {
                if(s.HarvestRequirementWorks.Length!=0)throw new ArgumentException("Harvest requirement work requires schema 74.");
                return;
            }
            if(s.SchemaVersion!=Snapshot.HarvestPreservationSchema||!s.TestOnly)
                throw new ArgumentException("Harvest preservation schema 74 is TEST_ONLY.");

            foreach(var job in s.HarvestRequirementWorks) {
                if(!s.Actors.Any(x=>x.Id==job.WorkerId)||job.StartedAt>s.RuleClock||job.UpdatedAt>s.RuleClock
                    ||job.Requirement!=HarvestIngredientRequirement.Fresh||job.Work.Phases.Count!=1
                    ||job.Work.Complete||job.Work.Retained!=job.Work.Labor)
                    throw new ArgumentException("Invalid harvest requirement work progress.");
                if(!HarvestPreservationRules.TryProject(s,job.InventoryLotId,out var view))
                    throw new ArgumentException("Harvest requirement work has no resolved physical harvest root.");
                if(job.Work.Required!=new RuleTime(checked(s.HarvestUnits.Single(x=>x.Id==view.HarvestUnitId).PreservationIntervalSeconds*2L)))
                    throw new ArgumentException("Invalid TEST_ONLY harvest requirement work duration.");
                var reservation=s.Work.Reservations.SingleOrDefault(x=>x.Id==job.ReservationId);
                if(reservation==null||reservation.JobId!=job.Id||reservation.LotId!=job.InventoryLotId
                    ||reservation.Amount!=job.RequiredAmount||reservation.ConsumedAmount!=default
                    ||reservation.ReleasedAmount!=default||reservation.RemainingAmount!=job.RequiredAmount)
                    throw new ArgumentException("Harvest requirement reservation changed unexpectedly.");
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==job.Id).ToArray();
                if(intervals.Any(x=>x.WorkerId!=job.WorkerId||x.Start<job.StartedAt||x.Start>s.RuleClock))
                    throw new ArgumentException("Invalid harvest requirement work interval.");
                RuleTime booked=default;
                foreach(var interval in intervals)booked=Add(booked,Subtract(interval.End,interval.Start));
                RuleTime expectedBooked=job.Status==HarvestRequirementWorkStatus.Working?job.Work.Required:job.Work.Labor;
                if(booked!=expectedBooked)throw new ArgumentException("Harvest requirement work booking does not match active or retained work.");
                RuleTime credited=default;
                foreach(var interval in intervals) {
                    if(interval.Start>=s.RuleClock)continue;
                    RuleTime end=interval.End<s.RuleClock?interval.End:s.RuleClock;
                    if(end>interval.Start)credited=Add(credited,Subtract(end,interval.Start));
                }
                if(credited!=job.Work.Labor)throw new ArgumentException("Harvest requirement work does not match credited labor.");
                bool active=intervals.Any(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock);
                if(job.Status==HarvestRequirementWorkStatus.Working) {
                    if(job.UpdatedAt!=s.RuleClock||job.PauseReason!=HarvestRequirementPauseReason.None
                        ||view.State!=HarvestPreservationState.Fresh||!active
                        ||intervals.Count(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock)!=1)
                        throw new ArgumentException("Invalid active Fresh-required work.");
                } else if(job.Status==HarvestRequirementWorkStatus.Paused) {
                    if(active||job.PauseReason==HarvestRequirementPauseReason.None
                        ||job.PauseReason==HarvestRequirementPauseReason.IngredientNotFresh&&view.State==HarvestPreservationState.Fresh)
                        throw new ArgumentException("Invalid paused Fresh-required work.");
                } else throw new ArgumentException("Unknown harvest requirement work status.");
            }
        }
    }
}
