#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Adopted prototype procedures. The host establishes authority, reach, hands, compatible
    /// storage and capacity. These methods operate only on a detached simulation candidate.</summary>
    public static class OrdinaryInventory
    {
        public static long SecondsPerUnit(NutritionKind kind)=>kind==NutritionKind.FoodPounds?900
            :kind==NutritionKind.WaterPints?60:throw new ArgumentException("Not ordinary food or water.");
        internal static RuleTime Duration(RuleQuantity amount,long rate)=>RuleTime.FromFraction((BigInteger)amount.Numerator*rate,amount.Denominator);
        internal static RuleQuantity Quantity(RuleTime time,long rate)=>RuleQuantity.FromFraction(time.Numerator,(BigInteger)time.Denominator*rate);
        internal static string Identity(Snapshot s,string suffix)=>"inventory."+(s.Revision+1).ToString(CultureInfo.InvariantCulture)+"."+suffix;
        public static bool Busy(Snapshot s,string actor)
            =>s.Work.WorkerIntervals.Any(x=>x.WorkerId==actor&&x.Start<=s.RuleClock&&x.End>s.RuleClock)
                ||WorldActivityProjection.CurrentWork(s).Any(x=>x.ActorId==actor);
        public static bool Fresh(Snapshot s,InventoryLotRecord lot)=>!lot.FreshUntil.HasValue||s.RuleClock<lot.FreshUntil.Value;
        public static RuleQuantity Consumed(Snapshot s,string actor,NutritionKind kind)=>RuleQuantity.Sum(s.Intakes.Where(x=>x.ActorId==actor
            &&s.InventoryLots.Single(l=>l.LotId==x.LotId).Nutrition==kind).Select(x=>s.Work.Reservations.Single(r=>r.Id==x.ReservationId).ConsumedAmount));
        public static RuleQuantity EdibleFood(Snapshot s)=>RuleQuantity.Sum(s.InventoryLots.Where(x=>x.Nutrition==NutritionKind.FoodPounds&&Fresh(s,x))
            .Select(x=>s.Work.Lots.Single(l=>l.Id==x.LotId).Amount));

        public static void Descendant(Snapshot s,string sourceId,string childId,RuleQuantity amount,string location,string custodian,InventoryAccess access)
        {
            var source=s.InventoryLots.Single(x=>x.LotId==sourceId);var lot=s.Work.Lots.Single(x=>x.Id==sourceId);
            if(amount==default||amount>s.Work.AvailableAmount(sourceId)||s.InventoryLots.Any(x=>x.LotId==childId))
                throw new ArgumentException("Invalid unreserved portion.");
            s.Work=new WorkLedger(s.Work.Lots.Select(x=>x.Id==sourceId?new ResourceLot(x.Id,x.UnitId,x.Amount-amount,x.LocationId,x.CustodianId):x)
                .Concat(new[]{new ResourceLot(childId,lot.UnitId,amount,location,custodian)}),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Concat(new[]{new InventoryLotRecord(childId,sourceId,source.OwnerId,amount,s.RuleClock,
                source.Nutrition,source.FreshUntil,access)}).ToArray();
            if(s.Vessels.Any(v=>v.Id==location))s.VesselContents=s.VesselContents.Concat(new[]{new VesselContentRecord(childId,location)}).ToArray();
            PortableEquipmentRules.RegisterInventoryLot(s,childId,location,custodian);
        }
        public static void StartIntake(Snapshot s,string actor,string lotId,RuleQuantity amount)
        {
            var item=s.InventoryLots.Single(x=>x.LotId==lotId);
            if(s.InventoryCombat||Busy(s,actor)||!Fresh(s,item)||amount==default)throw new ArgumentException("Intake unavailable.");
            long rate=SecondsPerUnit(item.Nutrition);string job=Identity(s,"intake"),reservation=job+".stock";
            RuleTime end=CampGreens.Add(s.RuleClock,Duration(amount,rate));
            s.Work=s.Work.Reserve(job,new[]{new WorkerInterval(job+".labor",job,actor,s.RuleClock,end)},
                new[]{new ResourceReservation(reservation,job,lotId,amount)});
            s.Intakes=s.Intakes.Concat(new[]{new IntakeRecord(job,actor,lotId,reservation,s.RuleClock,null,IntakeStatus.Working)}).ToArray();
        }
        public static void Interrupt(Snapshot s,IntakeRecord job,IntakeStatus status)
        {
            if(job.Status!=IntakeStatus.Working||status==IntakeStatus.Working||status==IntakeStatus.Complete)throw new ArgumentException("Invalid interruption.");
            s.Work=s.Work.Release(job.Id,job.ReservationId).CancelFutureWork(job.Id,s.RuleClock);
            Replace(s,new IntakeRecord(job.Id,job.ActorId,job.LotId,job.ReservationId,job.StartedAt,s.RuleClock,status));
        }
        private static void Replace(Snapshot s,IntakeRecord job)=>s.Intakes=s.Intakes.Select(x=>x.Id==job.Id?job:x).ToArray();
        public static void AdvanceTo(Snapshot s,RuleTime target,Action<Snapshot> beforeRecovery=null,Action<Snapshot,RuleTime> creditOtherWork=null)
        {
            if(target<=s.RuleClock)throw new ArgumentException("Positive shared advance required.");
            beforeRecovery?.Invoke(s);ActorLifeRules.RecoverDue(s);
            while(s.RuleClock<target) {
                RuleTime next=target;
                var lifeDeadline=ActorLifeRules.NextDeadline(s);if(lifeDeadline.HasValue&&lifeDeadline.Value<next)next=lifeDeadline.Value;
                foreach(var fill in s.WaterFills.Where(x=>x.Status==WaterFillStatus.Working)) {
                    var end=CampGreens.Add(s.RuleClock,CampGreens.Subtract(new RuleTime(60),fill.Progress));if(end<next)next=end;
                }
                foreach(var job in s.Intakes.Where(x=>x.Status==IntakeStatus.Working)) {
                    var item=s.InventoryLots.Single(x=>x.LotId==job.LotId);var claim=s.Work.Reservations.Single(x=>x.Id==job.ReservationId);
                    var finish=CampGreens.Add(job.StartedAt,Duration(claim.Amount,SecondsPerUnit(item.Nutrition)));
                    if(finish<next)next=finish;
                    if(item.FreshUntil.HasValue&&item.FreshUntil.Value<next)next=item.FreshUntil.Value;
                }
                // Camp Greens may stop at an earlier milestone. Credit intake only through the actual endpoint.
                RuleTime previous=s.RuleClock;CampGreens.Advance(s,next);RegisterCropOutput(s);
                WaterFilling.CreditWork(s,CampGreens.Subtract(s.RuleClock,previous));
                creditOtherWork?.Invoke(s,CampGreens.Subtract(s.RuleClock,previous));
                foreach(var job in s.Intakes.Where(x=>x.Status==IntakeStatus.Working).ToArray()) {
                    var item=s.InventoryLots.Single(x=>x.LotId==job.LotId);var claim=s.Work.Reservations.Single(x=>x.Id==job.ReservationId);
                    RuleQuantity consumed=Quantity(CampGreens.Subtract(s.RuleClock,job.StartedAt),SecondsPerUnit(item.Nutrition));
                    s.Work=s.Work.ConsumeThrough(job.Id,job.ReservationId,consumed);
                    if(consumed==claim.Amount)Replace(s,new IntakeRecord(job.Id,job.ActorId,job.LotId,job.ReservationId,job.StartedAt,s.RuleClock,IntakeStatus.Complete));
                    else if(!Fresh(s,item))Interrupt(s,job,IntakeStatus.Expired);
                }
                WaterFilling.CompleteDue(s);
                beforeRecovery?.Invoke(s);ActorLifeRules.RecoverDue(s);
            }
        }
        internal static void RegisterCropOutput(Snapshot s)
        {
            foreach(var food in s.CropFood.Where(f=>!s.InventoryLots.Any(x=>x.LotId==f.LotId))) {
                var crop=s.Crops.Single(c=>c.Id==food.BatchId);
                s.InventoryLots=s.InventoryLots.Concat(new[]{new InventoryLotRecord(food.LotId,"",crop.OwnerId,new RuleQuantity(8),
                    crop.ClosedAt.Value,NutritionKind.FoodPounds,food.FreshUntil,InventoryAccess.Ground)}).ToArray();
            }
        }
        public static void Handle(Snapshot s,Command c,string location,string custodian,InventoryAccess access)
        {
            string job=Identity(s,"handling"),child=Identity(s,"lot");RuleTime start=s.RuleClock;
            if(s.InventoryCombat) {
                if(c.Actor!=s.InventoryTurnActor||s.InventoryInteractions>=2)throw new ArgumentException("No tactical interaction budget.");
                s.InventoryInteractions++;
            } else {
                RuleTime end=start.AddSeconds(1);
                s.Work=s.Work.Reserve(job,new[]{new WorkerInterval(job+".labor",job,c.Actor,start,end)},Array.Empty<ResourceReservation>());
                AdvanceTo(s,end);
            }
            Descendant(s,c.Target,child,c.Inventory.Amount,location,custodian,access);
            s.Handling=s.Handling.Concat(new[]{new HandlingRecord(job,c.Actor,c.Target,child,c.Inventory.Handling,start,s.RuleClock,s.InventoryCombat)}).ToArray();
        }
        public static string Validate(Snapshot s)
        {
            var tactical=s.Handling.Where(x=>x.Tactical).ToArray();
            var tacticalVessels=s.VesselMoves.Where(x=>x.Tactical).ToArray();
            if(s.SchemaVersion<Snapshot.EncounterSchema&&(s.InventoryCombat?tactical.Length+tacticalVessels.Length!=s.InventoryInteractions||tactical.Any(x=>x.ActorId!=s.InventoryTurnActor)||tacticalVessels.Any(x=>x.ActorId!=s.InventoryTurnActor)
                :tactical.Length!=0||tacticalVessels.Length!=0||s.Intakes.Any(x=>x.Status==IntakeStatus.CombatInterrupted)))return "InvalidTacticalHistory";
            var cropTasks=s.Crops.SelectMany(x=>x.Tasks).ToArray();
            if(s.Work.Reservations.Any(r=>!cropTasks.Any(t=>t.InputReservations.Contains(r.Id))&&!s.Intakes.Any(j=>j.ReservationId==r.Id)&&!s.WaterFills.Any(j=>j.ReservationId==r.Id)
                    &&!s.HarvestRequirementWorks.Any(j=>j.ReservationId==r.Id&&j.Id==r.JobId&&j.InventoryLotId==r.LotId)
                    &&!s.MiningAttempts.Any(j=>j.Id==r.JobId&&j.SelectedUnitIds.Contains(r.LotId,StringComparer.Ordinal)))
                ||s.Work.WorkerIntervals.Any(w=>!cropTasks.Any(t=>t.Id==w.JobId)&&!s.Intakes.Any(j=>j.Id==w.JobId)&&!s.Handling.Any(j=>j.Id==w.JobId)&&!s.WaterFills.Any(j=>j.Id==w.JobId)&&!s.VesselMoves.Any(j=>j.Id==w.JobId)&&!s.SupplyCacheAttempts.Any(j=>j.Id==w.JobId)&&!s.PortableHandling.Any(j=>j.Id==w.JobId)&&!s.FishingTrapAttempts.Any(j=>j.Id==w.JobId)&&!s.HarvestAttempts.Any(j=>j.Id==w.JobId)&&!s.HarvestRequirementWorks.Any(j=>j.Id==w.JobId)&&!s.MiningAttempts.Any(j=>j.Id==w.JobId)&&!s.MineralPreparationAttempts.Any(j=>j.Id==w.JobId)))
                return "UnattributedInventoryLedger";
            foreach(var job in s.Intakes) {
                var item=s.InventoryLots.Single(x=>x.LotId==job.LotId);var lot=s.Work.Lots.Single(x=>x.Id==job.LotId);
                var claim=s.Work.Reservations.Single(x=>x.Id==job.ReservationId);long rate=SecondsPerUnit(item.Nutrition);
                var end=job.EndedAt??s.RuleClock;var elapsed=CampGreens.Subtract(end,job.StartedAt);
                if(!VesselHandling.ReadyForHistoricalIntake(s,job,item,lot)||job.StartedAt<item.CreatedAt
                    ||(item.FreshUntil.HasValue&&(job.StartedAt>=item.FreshUntil.Value||end>item.FreshUntil.Value))
                    ||Quantity(elapsed,rate)!=claim.ConsumedAmount)return "InvalidIntakeCredit";
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==job.Id).ToArray();
                RuleTime bookedEnd=job.Status==IntakeStatus.Working?CampGreens.Add(job.StartedAt,Duration(claim.Amount,rate)):end;
                if(bookedEnd==job.StartedAt?intervals.Length!=0:intervals.Length!=1||intervals[0].WorkerId!=job.ActorId
                    ||intervals[0].Start!=job.StartedAt||intervals[0].End!=bookedEnd)return "InvalidIntakeLabor";
                if(job.Status==IntakeStatus.Working) {
                    if(s.InventoryCombat||!Fresh(s,item)||claim.Status!=ReservationStatus.Reserved||claim.ReleasedAmount!=default)return "InvalidActiveIntake";
                } else if(job.Status==IntakeStatus.Complete) {
                    if(claim.Status!=ReservationStatus.Consumed)return "IncompleteIntake";
                } else {
                    if(claim.RemainingAmount!=default||claim.ReleasedAmount==default)return "UnreleasedIntake";
                    if(job.Status==IntakeStatus.Expired&&job.EndedAt!=item.FreshUntil)return "InvalidIntakeExpiry";
                    if(job.Status==IntakeStatus.CombatInterrupted&&(s.SchemaVersion>=Snapshot.SharedWorldSchema
                        ?!EncounterHistory.All(s).Any(e=>e.Origin==job.EndedAt&&e.Order.Contains(job.ActorId))
                        :job.EndedAt!=(s.SchemaVersion>=Snapshot.EncounterSchema?s.Encounter?.Origin:s.RuleClock)))return "InvalidCombatInterruptionTime";
                }
            }
            foreach(var job in s.Handling) {
                var source=s.InventoryLots.Single(x=>x.LotId==job.SourceId);
                if(job.StartedAt<source.CreatedAt)return "HandlingBeforeSource";
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==job.Id).ToArray();
                if(job.Tactical?(s.SchemaVersion>=Snapshot.EncounterSchema?!FixedEncounterRules.HistoricalHandling(s,job.Id,job.ActorId,job.StartedAt,job.EndedAt):job.EndedAt!=s.RuleClock||job.StartedAt!=job.EndedAt)||intervals.Length!=0
                    :job.EndedAt!=job.StartedAt.AddSeconds(1)||intervals.Length!=1||intervals[0].WorkerId!=job.ActorId
                        ||intervals[0].Start!=job.StartedAt||intervals[0].End!=job.EndedAt)return "InvalidHandlingLabor";
            }
            return null;
        }
    }
}
#endif
