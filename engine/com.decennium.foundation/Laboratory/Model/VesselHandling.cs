#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Safe intact handheld movement only. Fixture vessels are securely closed between uses,
    /// readily accessible, and fit the supplied supported plot placement. Jobs and liquid remain distinct.</summary>
    public static class VesselHandling
    {
        internal static long CreationRevision(string id)
        {
            var parts=id.Split('.');
            if(parts.Length<3||parts[0]!="inventory"||!long.TryParse(parts[1],NumberStyles.None,CultureInfo.InvariantCulture,out long n)||n<1)
                throw new ArgumentException("Invalid fixture event sequence.");
            return n;
        }
        internal static WaterVesselRecord At(Snapshot s,string vessel,RuleTime time,long beforeSequence=long.MaxValue,bool inclusive=false)
        {
            var current=s.Vessels.Single(v=>v.Id==vessel);
            foreach(var move in s.VesselMoves.Where(m=>m.VesselId==vessel&&(m.EndedAt>time||m.EndedAt==time&&(m.Sequence>beforeSequence||!inclusive&&m.Sequence==beforeSequence))).OrderByDescending(m=>m.Sequence))
                current=new WaterVesselRecord(current.Id,current.Profile,current.OwnerId,move.FromLocation,move.FromCustodian);
            return current;
        }
        internal static bool ReadyForHistoricalIntake(Snapshot s,IntakeRecord job,InventoryLotRecord item,ResourceLot lot)
        {
            string vessel=WaterFilling.SourceVessel(s,lot.Id);
            if(s.SchemaVersion<Snapshot.MovableVesselSchema||vessel==null)return WaterFilling.ReadyForIntake(s,job.ActorId,item,lot);
            var at=At(s,vessel,job.StartedAt,CreationRevision(job.Id));
            return item.Nutrition==NutritionKind.WaterPints&&at.LocationId==job.ActorId&&at.CustodianId==job.ActorId;
        }
        internal static bool PendingUse(Snapshot s,string vessel)=>s.WaterFills.Any(j=>j.Pending
            &&(j.DestinationId==vessel||WaterFilling.SourceVessel(s,j.SourceLotId)==vessel))
            ||s.VesselContents.Where(x=>x.VesselId==vessel).Any(x=>s.Work.Reservations.Any(r=>r.LotId==x.LotId&&r.RemainingAmount!=default));
        private static bool Near(Snapshot s,string actor,string other)
        {var a=s.Actors.Single(x=>x.Id==actor);var b=s.Actors.Single(x=>x.Id==other);return Math.Abs((long)a.X-b.X)+Math.Abs((long)a.Y-b.Y)<=1;}
        internal static string Resolve(Snapshot s,Command c,Func<string,int> hands)
        {
            if(c.Inventory==null||c.Inventory.Amount!=new RuleQuantity(1)||c.X!=0||c.Y!=0)return "InvalidVesselHandling";
            var vessel=s.Vessels.SingleOrDefault(v=>v.Id==c.Target);if(vessel==null)return "UnknownVessel";
            if(hands(c.Actor)<1)return "HandlingHandRequired";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(PendingUse(s,vessel.Id))return "VesselHasPendingWork";
            if(!WaterFilling.Accessible(s,c.Actor,vessel))return "VesselOutOfReach";
            string location,custodian;bool held=vessel.LocationId==c.Actor&&vessel.CustodianId==c.Actor;
            switch(c.Inventory.Handling) {
                case HandlingKind.Pickup:
                    if(held||vessel.LocationId!=TestOnlyCropPolicy.PlotId||c.Inventory.Destination!="")return "InvalidVesselPickup";
                    location=c.Actor;custodian=c.Actor;break;
                case HandlingKind.Drop:
                    if(!held||!WaterFilling.AtPlot(s,c.Actor)||c.Inventory.Destination!="")return "UnsupportedVesselPlacement";
                    location=TestOnlyCropPolicy.PlotId;custodian=c.Actor;break;
                case HandlingKind.Handover:
                    if(!held||c.Inventory.Destination==c.Actor||!s.Actors.Any(a=>a.Id==c.Inventory.Destination)||!Near(s,c.Actor,c.Inventory.Destination))return "InvalidVesselHandover";
                    if(hands(c.Inventory.Destination)<1||OrdinaryInventory.Busy(s,c.Inventory.Destination))return "RecipientHandsUnavailable";
                    location=c.Inventory.Destination;custodian=location;break;
                default:return "VesselStorageNotEstablished";
            }
            if(s.InventoryCombat&&(s.InventoryTurnActor!=c.Actor||s.InventoryInteractions>=2))return "InteractionBudgetUnavailable";
            if(s.Actors.Any(a=>a.Id==location)) {
                var pounds=TestOnlyInventoryPolicy.CarriedBurden(s,location).Pounds.Value+WaterFilling.Tare(vessel.Profile)+WaterFilling.Contents(s,vessel.Id);
                if(!Fits(pounds))return "CarryingCapacityExceeded";
            }
            string id=OrdinaryInventory.Identity(s,"vessel-move");RuleTime start=s.RuleClock;
            if(s.InventoryCombat)s.InventoryInteractions++;
            else {
                var end=start.AddSeconds(1);
                s.Work=s.Work.Reserve(id,new[]{new WorkerInterval(id+".labor",id,c.Actor,start,end)},Array.Empty<ResourceReservation>());
                OrdinaryInventory.AdvanceTo(s,end);
            }
            // Timeline work completes first; this fixture has no destructive or scheduled encounter event.
            s.Vessels=s.Vessels.Select(v=>v.Id==vessel.Id?new WaterVesselRecord(v.Id,v.Profile,v.OwnerId,location,custodian):v).ToArray();
            var contained=s.VesselContents.Where(x=>x.VesselId==vessel.Id).Select(x=>x.LotId).ToArray();
            s.Work=new WorkLedger(s.Work.Lots.Select(l=>contained.Contains(l.Id)?new ResourceLot(l.Id,l.UnitId,l.Amount,l.LocationId,custodian):l),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Select(l=>contained.Contains(l.LotId)?new InventoryLotRecord(l.LotId,l.ParentId,l.OwnerId,l.CreatedAmount,l.CreatedAt,l.Nutrition,l.FreshUntil,
                location==TestOnlyCropPolicy.PlotId?InventoryAccess.Ground:InventoryAccess.Ready):l).ToArray();
            s.VesselMoves=s.VesselMoves.Concat(new[]{new VesselHandlingRecord(id,s.Revision+1,c.Actor,vessel.Id,vessel.LocationId,vessel.CustodianId,
                location,custodian,c.Inventory.Handling,start,s.RuleClock,s.InventoryCombat)}).ToArray();return null;
        }
        private static bool Fits(RuleQuantity pounds)=>PlaytestCarrying.CanCarry(PlaytestCarrying.Limits(CarrierSize.Medium,10),new BurdenTotals(pounds,pounds.Scale(1,10),true))==true;
        private static bool BornBy(InventoryLotRecord lot,RuleTime time,long sequence)=>lot.CreatedAt<time
            ||lot.CreatedAt==time&&(lot.ParentId==""||CreationRevision(lot.LotId)<=sequence);
        internal static RuleQuantity AmountAt(Snapshot s,InventoryLotRecord lot,RuleTime time,long sequence)
        {
            if(!BornBy(lot,time,sequence))return default;
            var amount=lot.CreatedAmount-RuleQuantity.Sum(s.InventoryLots.Where(c=>c.ParentId==lot.LotId&&BornBy(c,time,sequence)).Select(c=>c.CreatedAmount));
            foreach(var intake in s.Intakes.Where(j=>j.LotId==lot.LotId&&j.StartedAt<time)) {
                var end=intake.EndedAt??s.RuleClock;if(end>time)end=time;
                amount-=OrdinaryInventory.Quantity(CampGreens.Subtract(end,intake.StartedAt),OrdinaryInventory.SecondsPerUnit(lot.Nutrition));
            }
            return amount;
        }
        internal static RuleQuantity BurdenAt(Snapshot s,string actor,RuleTime time,long sequence)
        {
            var vessels=s.Vessels.Select(v=>At(s,v.Id,time,sequence,true)).Where(v=>v.LocationId==actor).ToArray();
            return new RuleQuantity(1)+RuleQuantity.Sum(vessels.Select(v=>WaterFilling.Tare(v.Profile)))
                +RuleQuantity.Sum(s.InventoryLots.Where(i=>{var l=s.Work.Lots.Single(x=>x.Id==i.LotId);return l.LocationId==actor||vessels.Any(v=>v.Id==l.LocationId);})
                    .Select(i=>AmountAt(s,i,time,sequence)));
        }
        private static bool Conflicts(VesselHandlingRecord move,RuleTime start,RuleTime? end,long sequence)=>
            (move.EndedAt>start||move.EndedAt==start&&move.Sequence>sequence)&&(!end.HasValue||move.StartedAt<end.Value);
        internal static string Validate(Snapshot s,WaterVesselRecord[] initial,Func<string,int> hands)
        {
            if(s.Vessels.Length!=initial.Length||initial.Any(e=>!s.Vessels.Any(v=>v.Id==e.Id&&v.Profile==e.Profile&&v.OwnerId==e.OwnerId)))return "InvalidFixtureVessels";
            var states=initial.ToDictionary(v=>v.Id,StringComparer.Ordinal);RuleTime previous=default;
            foreach(var m in s.VesselMoves.OrderBy(x=>x.Sequence)) {
                var before=states[m.VesselId];
                if(m.Sequence!=CreationRevision(m.Id)||m.StartedAt<previous||before.LocationId!=m.FromLocation||before.CustodianId!=m.FromCustodian
                    ||hands(m.ActorId)<1)return "InvalidVesselHistory";
                bool held=m.FromLocation==m.ActorId&&m.FromCustodian==m.ActorId;
                bool valid=m.Kind==HandlingKind.Pickup?m.FromLocation==TestOnlyCropPolicy.PlotId&&m.ToLocation==m.ActorId&&m.ToCustodian==m.ActorId
                    :m.Kind==HandlingKind.Drop?held&&m.ToLocation==TestOnlyCropPolicy.PlotId&&m.ToCustodian==m.ActorId
                    :m.Kind==HandlingKind.Handover&&held&&m.ToLocation==m.ToCustodian&&m.ToCustodian!=m.ActorId&&s.Actors.Any(a=>a.Id==m.ToCustodian)&&hands(m.ToCustodian)>=1;
                if(!valid)return "InvalidVesselTransition";
                var work=s.Work.WorkerIntervals.Where(w=>w.JobId==m.Id).ToArray();
                if(m.Tactical?(s.SchemaVersion>=Snapshot.EncounterSchema?!FixedEncounterRules.HistoricalHandling(s,m.Id,m.ActorId,m.StartedAt,m.EndedAt):m.StartedAt!=m.EndedAt||m.EndedAt!=s.RuleClock)||work.Length!=0
                    :m.EndedAt!=m.StartedAt.AddSeconds(1)||work.Length!=1||work[0].WorkerId!=m.ActorId||work[0].Start!=m.StartedAt||work[0].End!=m.EndedAt)return "InvalidVesselLabor";
                if(m.Kind==HandlingKind.Handover&&s.Work.WorkerIntervals.Any(w=>w.WorkerId==m.ToCustodian&&w.Start<=m.StartedAt&&w.End>m.StartedAt))return "ReservedRecipientHands";
                if(s.WaterFills.Any(j=>(j.DestinationId==m.VesselId||WaterFilling.SourceVessel(s,j.SourceLotId)==m.VesselId)
                    &&Conflicts(m,j.StartedAt,j.EndedAt,CreationRevision(j.Id)))
                    ||s.Intakes.Any(j=>WaterFilling.SourceVessel(s,j.LotId)==m.VesselId&&Conflicts(m,j.StartedAt,j.EndedAt,CreationRevision(j.Id))))return "MovedReservedVessel";
                states[m.VesselId]=new WaterVesselRecord(before.Id,before.Profile,before.OwnerId,m.ToLocation,m.ToCustodian);previous=m.EndedAt;
                if(s.Actors.Any(a=>!Fits(BurdenAt(s,a.Id,m.EndedAt,m.Sequence))))return "HistoricalCarryingCapacityExceeded";
            }
            if(s.Vessels.Any(v=>v.LocationId!=states[v.Id].LocationId||v.CustodianId!=states[v.Id].CustodianId))return "UnrecordedVesselMovement";
            return null;
        }
    }
}
#endif
