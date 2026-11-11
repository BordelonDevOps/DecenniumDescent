using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum NutritionKind { None, FoodPounds, WaterPints }
    public enum InventoryAccess { Ground, Ready, Stowed }
    public enum HandlingKind { Pickup, Drop, Retrieve, Stow, Handover }
    public enum IntakeStatus { Working, Complete, Interrupted, Expired, CombatInterrupted }

    /// <summary>Immutable provenance for a ledger lot. Physical quantity exists only in WorkLedger.
    /// Parent records survive subdivision and transfer, including when their remaining stock is zero.</summary>
    public sealed class InventoryLotRecord
    {
        public string LotId { get; }
        public string ParentId { get; }
        public string OwnerId { get; }
        public RuleQuantity CreatedAmount { get; }
        public RuleTime CreatedAt { get; }
        public NutritionKind Nutrition { get; }
        public RuleTime? FreshUntil { get; }
        public InventoryAccess Access { get; }
        public InventoryLotRecord(string lotId,string parentId,string ownerId,RuleQuantity createdAmount,
            RuleTime createdAt,NutritionKind nutrition,RuleTime? freshUntil,InventoryAccess access)
        {
            if(!Validation.ValidId(lotId)||parentId==null||(parentId!=""&&!Validation.ValidId(parentId))
                ||!Validation.ValidId(ownerId)||!Enum.IsDefined(typeof(NutritionKind),nutrition)
                ||!Enum.IsDefined(typeof(InventoryAccess),access))throw new ArgumentException("Invalid inventory provenance.");
            LotId=lotId;ParentId=parentId;OwnerId=ownerId;CreatedAmount=createdAmount;CreatedAt=createdAt;
            Nutrition=nutrition;FreshUntil=freshUntil;Access=access;
        }
    }
    public sealed class IntakeRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string LotId { get; }
        public string ReservationId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime? EndedAt { get; }
        public IntakeStatus Status { get; }
        public IntakeRecord(string id,string actorId,string lotId,string reservationId,RuleTime startedAt,RuleTime? endedAt,IntakeStatus status)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(actorId)||!Validation.ValidId(lotId)||!Validation.ValidId(reservationId)
                ||!Enum.IsDefined(typeof(IntakeStatus),status)||(status==IntakeStatus.Working)==endedAt.HasValue
                ||(endedAt.HasValue&&endedAt.Value<startedAt))throw new ArgumentException("Invalid intake record.");
            Id=id;ActorId=actorId;LotId=lotId;ReservationId=reservationId;StartedAt=startedAt;EndedAt=endedAt;Status=status;
        }
    }
    public sealed class HandlingRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string SourceId { get; }
        public string ChildId { get; }
        public HandlingKind Kind { get; }
        public RuleTime StartedAt { get; }
        public RuleTime EndedAt { get; }
        public bool Tactical { get; }
        public HandlingRecord(string id,string actorId,string sourceId,string childId,HandlingKind kind,RuleTime startedAt,RuleTime endedAt,bool tactical)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(actorId)||!Validation.ValidId(sourceId)||!Validation.ValidId(childId)
                ||!Enum.IsDefined(typeof(HandlingKind),kind)||endedAt<startedAt)throw new ArgumentException("Invalid handling record.");
            Id=id;ActorId=actorId;SourceId=sourceId;ChildId=childId;Kind=kind;StartedAt=startedAt;EndedAt=endedAt;Tactical=tactical;
        }
    }
    /// <summary>Explicit command payload; destinations are identities, never grants or consent.</summary>
    public sealed class InventoryRequest
    {
        public RuleQuantity Amount { get; }
        public string Destination { get; }
        public HandlingKind Handling { get; }
        public InventoryRequest(RuleQuantity amount,string destination="",HandlingKind handling=HandlingKind.Pickup)
        {
            if(destination==null||(destination!=""&&!Validation.ValidId(destination))||!Enum.IsDefined(typeof(HandlingKind),handling))
                throw new ArgumentException("Invalid inventory request.");
            Amount=amount;Destination=destination;Handling=handling;
        }
        internal string Fingerprint=>Amount+"|"+Destination+"|"+((int)Handling).ToString(System.Globalization.CultureInfo.InvariantCulture);
    }
    public static class InventoryValidation
    {
        public static System.Collections.Generic.HashSet<string> FamilyAt(Snapshot state, string rootId, RuleTime asOf)
        {
            var children = state.InventoryLots.Where(x => x.CreatedAt <= asOf).ToLookup(x => x.ParentId, StringComparer.Ordinal);
            var family = new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal) { rootId };
            var pending = new System.Collections.Generic.Queue<string>();
            pending.Enqueue(rootId);
            while (pending.Count != 0) {
                foreach (var child in children[pending.Dequeue()])
                    if (family.Add(child.LotId)) pending.Enqueue(child.LotId);
            }
            return family;
        }

        public static void Validate(Snapshot s)
        {
            if(s.InventoryLots==null||s.Intakes==null||s.Handling==null||s.PortableHandling==null||s.InventoryTurnActor==null
                ||s.InventoryLots.Any(x=>x==null)||s.Intakes.Any(x=>x==null)||s.Handling.Any(x=>x==null)
                ||s.InventoryLots.Length>128||s.Intakes.Length>32||s.Handling.Length>64)throw new ArgumentException("Invalid inventory collections.");
            if(s.SchemaVersion<Snapshot.InventorySchema) {
                if(s.InventoryLots.Length!=0||s.Intakes.Length!=0||s.Handling.Length!=0||s.InventoryCombat
                    ||s.InventoryTurnActor!=""||s.InventoryInteractions!=0)throw new ArgumentException("Inventory requires its explicit schema.");
                return;
            }
            if(s.Receipts.Length>512||s.InventoryLots.Length!=s.Work.Lots.Count
                ||s.InventoryLots.Any(x=>!s.Work.Lots.Any(l=>l.Id==x.LotId))
                ||s.InventoryLots.Select(x=>x.LotId).Distinct(StringComparer.Ordinal).Count()!=s.InventoryLots.Length
                ||s.Intakes.Select(x=>x.Id).Concat(s.Handling.Select(x=>x.Id)).Concat(s.PortableHandling.Select(x=>x.Id)).Concat(s.Crops.SelectMany(x=>x.Tasks).Select(x=>x.Id))
                    .Distinct(StringComparer.Ordinal).Count()!=s.Intakes.Length+s.Handling.Length+s.PortableHandling.Length+s.Crops.Sum(x=>x.Tasks.Count))
                throw new ArgumentException("Invalid inventory identities or session capacity.");
            bool Actor(string id)=>s.Actors.Any(a=>a.Id==id);
            if(s.InventoryInteractions<0||s.InventoryInteractions>2
                ||(s.InventoryCombat?!Actor(s.InventoryTurnActor):s.InventoryTurnActor!=""||s.InventoryInteractions!=0))
                throw new ArgumentException("Invalid bounded tactical interaction state.");
            foreach(var item in s.InventoryLots) {
                var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==item.LotId)??throw new ArgumentException("Missing physical lot.");
                if(item.CreatedAt>s.RuleClock)throw new ArgumentException("Future inventory origin.");
                var seen=new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal){item.LotId};
                var current=item;
                while(current.ParentId!="") {
                    var parent=s.InventoryLots.SingleOrDefault(x=>x.LotId==current.ParentId)??throw new ArgumentException("Missing inventory ancestor.");
                    if(!seen.Add(parent.LotId)||parent.CreatedAt>current.CreatedAt||parent.OwnerId!=current.OwnerId
                        ||parent.Nutrition!=current.Nutrition||parent.FreshUntil!=current.FreshUntil
                        ||s.Work.Lots.Single(x=>x.Id==parent.LotId).UnitId!=lot.UnitId)throw new ArgumentException("Invalid inherited inventory history.");
                    current=parent;
                }
                if(RuleQuantity.Sum(s.InventoryLots.Where(x=>x.ParentId==item.LotId).Select(x=>x.CreatedAmount)
                    .Concat(s.Work.Reservations.Where(x=>x.LotId==item.LotId).Select(x=>x.ConsumedAmount)).Concat(new[]{lot.Amount}))!=item.CreatedAmount)
                    throw new ArgumentException("Inventory quantity conservation failed.");
            }
            foreach(var job in s.Intakes) {
                var claim=s.Work.Reservations.SingleOrDefault(x=>x.Id==job.ReservationId);
                if(!Actor(job.ActorId)||job.StartedAt>s.RuleClock||(job.EndedAt.HasValue&&job.EndedAt.Value>s.RuleClock)
                    ||claim==null||claim.JobId!=job.Id||claim.LotId!=job.LotId)throw new ArgumentException("Invalid intake references or time.");
            }
            foreach(var job in s.Handling) {
                var child=s.InventoryLots.SingleOrDefault(x=>x.LotId==job.ChildId);
                if(!Actor(job.ActorId)||job.EndedAt>s.RuleClock||child==null||child.ParentId!=job.SourceId||child.CreatedAt!=job.EndedAt)
                    throw new ArgumentException("Invalid handling references or time.");
            }
        }
    }
}
