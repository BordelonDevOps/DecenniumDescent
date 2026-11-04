#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Adopted stable ordinary-water procedure. All mutations target a detached transaction candidate.
    /// Material remains at source until completion. Pending jobs themselves reserve destination capacity.</summary>
    public static class WaterFilling
    {
        public static RuleQuantity Capacity(WaterVesselProfile profile)=>profile==WaterVesselProfile.Waterskin?new RuleQuantity(4)
            :profile==WaterVesselProfile.OrdinaryFlask?new RuleQuantity(1):throw new ArgumentException("Unsupported vessel profile.");
        public static RuleQuantity Tare(WaterVesselProfile profile)
        {Capacity(profile);return new RuleQuantity(1);} // Ordinary flask/tankard, not the separate oil-flask profile.
        public static RuleQuantity Contents(Snapshot s,string vessel)=>RuleQuantity.Sum(s.VesselContents.Where(x=>x.VesselId==vessel)
            .Select(x=>s.Work.Lots.Single(l=>l.Id==x.LotId).Amount));
        public static RuleQuantity ReservedCapacity(Snapshot s,string vessel)=>RuleQuantity.Sum(s.WaterFills.Where(x=>x.Pending&&x.DestinationId==vessel).Select(x=>x.Amount));
        public static RuleQuantity FreeCapacity(Snapshot s,string vessel)=>Capacity(s.Vessels.Single(v=>v.Id==vessel).Profile)-Contents(s,vessel)-ReservedCapacity(s,vessel);
        public static bool ReadyForIntake(Snapshot s,string actor,InventoryLotRecord item,ResourceLot lot)
        {
            if(item.Access!=InventoryAccess.Ready||lot.CustodianId!=actor)return false;
            if(lot.LocationId==actor)return true;
            return s.VesselContents.Any(x=>x.LotId==lot.Id&&s.Vessels.Any(v=>v.Id==x.VesselId&&v.LocationId==actor&&v.CustodianId==actor));
        }
        internal static bool AtPlot(Snapshot s,string actor)
        {var a=s.Actors.Single(x=>x.Id==actor);return Math.Abs((long)a.X-3)+Math.Abs((long)a.Y-3)<=1;}
        internal static bool Accessible(Snapshot s,string actor,WaterVesselRecord vessel)=>vessel.LocationId==TestOnlyCropPolicy.PlotId
            ?AtPlot(s,actor):vessel.LocationId==actor&&vessel.CustodianId==actor||SupplyCacheRules.Accessible(s,actor,vessel.LocationId);
        internal static bool Accessible(Snapshot s,string actor,ResourceLot lot)
        {
            var vessel=s.Vessels.SingleOrDefault(v=>v.Id==lot.LocationId);
            return vessel!=null?Accessible(s,actor,vessel):lot.LocationId==TestOnlyCropPolicy.PlotId&&AtPlot(s,actor)||SupplyCacheRules.Accessible(s,actor,lot.LocationId);
        }
        internal static string SourceVessel(Snapshot s,string lot)=>s.VesselContents.SingleOrDefault(x=>x.LotId==lot)?.VesselId;
        private static bool Involves(Snapshot s,WaterFillRecord job,string vessel)=>job.DestinationId==vessel||SourceVessel(s,job.SourceLotId)==vessel;
        internal static bool OpeningsAvailable(Snapshot s,string source,string destination,string exceptJob=null)
        {
            string sourceVessel=SourceVessel(s,source);
            return !s.WaterFills.Any(j=>j.Status==WaterFillStatus.Working&&j.Id!=exceptJob
                &&(Involves(s,j,destination)||(sourceVessel!=null&&Involves(s,j,sourceVessel))));
        }
        internal static string CarryAfterTransfer(Snapshot s,string actor,string source,string destination,RuleQuantity amount)
        {
            var burden=TestOnlyInventoryPolicy.CarriedBurden(s,actor);
            if(!burden.Pounds.HasValue||!burden.Load.HasValue)return "CarryingCapacityNotEstablished";
            var pounds=burden.Pounds.Value;
            var sourceVessel=s.Vessels.SingleOrDefault(v=>v.Id==SourceVessel(s,source));var dest=s.Vessels.Single(v=>v.Id==destination);
            if(sourceVessel!=null&&sourceVessel.LocationId==actor)pounds-=amount;
            if(dest.LocationId==actor)pounds+=amount;
            return PlaytestCarrying.CanCarry(PlaytestCarrying.Limits(CarrierSize.Medium,10),new BurdenTotals(pounds,pounds.Scale(1,10),true))==true
                ?null:"CarryingCapacityExceeded";
        }
        internal static string Prerequisite(Snapshot s,string actor,string source,string destination,RuleQuantity amount,string existingJob=null)
        {
            var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==source);var vessel=s.Vessels.SingleOrDefault(x=>x.Id==destination);
            var meta=s.InventoryLots.SingleOrDefault(x=>x.LotId==source);
            if(lot==null||vessel==null||meta==null)return "UnknownFillReference";
            if(meta.Nutrition!=NutritionKind.WaterPints||lot.UnitId!=TestOnlyInventoryPolicy.WaterUnit||meta.FreshUntil.HasValue)return "UnsupportedFillLiquid";
            if(SourceVessel(s,source)==destination)return "SameVesselFill";
            if(!Accessible(s,actor,lot)||!Accessible(s,actor,vessel))return "FillOutOfReach";
            if(!OpeningsAvailable(s,source,destination,existingJob))return "VesselOpeningBusy";
            string carrying=CarryAfterTransfer(s,actor,source,destination,amount);if(carrying!=null)return carrying;
            return null;
        }
        private static void Replace(Snapshot s,WaterFillRecord job)=>s.WaterFills=s.WaterFills.Select(x=>x.Id==job.Id?job:x).ToArray();
        private static WaterFillRecord Changed(WaterFillRecord j,WaterFillStatus status,RuleTime progress,RuleTime? ended=null,string output="")
            =>new WaterFillRecord(j.Id,j.WorkerId,j.SourceLotId,j.DestinationId,j.ReservationId,j.Amount,j.StartedAt,progress,ended,status,output);
        private static void Book(Snapshot s,WaterFillRecord job)
        {
            string interval=job.Id+".work."+(s.Revision+1).ToString(System.Globalization.CultureInfo.InvariantCulture);
            s.Work=s.Work.Reserve(job.Id,new[]{new WorkerInterval(interval,job.Id,job.WorkerId,s.RuleClock,
                CampGreens.Add(s.RuleClock,CampGreens.Subtract(new RuleTime(60),job.Progress)))},Array.Empty<ResourceReservation>());
        }
        public static void Start(Snapshot s,string actor,string source,string destination,RuleQuantity amount)
        {
            if(amount==default||amount>s.Work.AvailableAmount(source)||amount>FreeCapacity(s,destination))throw new ArgumentException("Unavailable fill quantity/capacity.");
            string id=OrdinaryInventory.Identity(s,"fill"),claim=id+".water";
            var job=new WaterFillRecord(id,actor,source,destination,claim,amount,s.RuleClock,default,null,WaterFillStatus.Working);
            s.Work=s.Work.Reserve(id,Array.Empty<WorkerInterval>(),new[]{new ResourceReservation(claim,id,source,amount)});
            Book(s,job);s.WaterFills=s.WaterFills.Concat(new[]{job}).ToArray();
        }
        public static void Pause(Snapshot s,WaterFillRecord job)
        {
            if(job.Status!=WaterFillStatus.Working)throw new ArgumentException("Fill is not working.");
            s.Work=s.Work.CancelFutureWork(job.Id,s.RuleClock);Replace(s,Changed(job,WaterFillStatus.Paused,job.Progress));
        }
        public static void Resume(Snapshot s,WaterFillRecord job)
        {
            if(job.Status!=WaterFillStatus.Paused)throw new ArgumentException("Fill is not paused.");
            Book(s,job);Replace(s,Changed(job,WaterFillStatus.Working,job.Progress));
        }
        public static void Cancel(Snapshot s,WaterFillRecord job)
        {
            if(!job.Pending)throw new ArgumentException("Fill is already terminal.");
            s.Work=s.Work.Release(job.Id,job.ReservationId).CancelFutureWork(job.Id,s.RuleClock);
            Replace(s,Changed(job,WaterFillStatus.Cancelled,job.Progress,s.RuleClock));
        }
        internal static void CreditWork(Snapshot s,RuleTime elapsed)
        {
            foreach(var job in s.WaterFills.Where(x=>x.Status==WaterFillStatus.Working).ToArray())
                Replace(s,Changed(job,job.Status,CampGreens.Add(job.Progress,elapsed)));
        }
        internal static void CompleteDue(Snapshot s)
        {
            foreach(var job in s.WaterFills.Where(x=>x.Status==WaterFillStatus.Working&&x.Progress==new RuleTime(60)).OrderBy(x=>x.Id,StringComparer.Ordinal).ToArray()) {
                string error=Prerequisite(s,job.WorkerId,job.SourceLotId,job.DestinationId,job.Amount,job.Id);
                if(error!=null)throw new ArgumentException(error); // This host excludes unsupported intervening physical events.
                var dest=s.Vessels.Single(v=>v.Id==job.DestinationId);string child=job.Id+".output";
                s.Work=s.Work.Release(job.Id,job.ReservationId);
                OrdinaryInventory.Descendant(s,job.SourceLotId,child,job.Amount,dest.Id,dest.CustodianId,
                    dest.LocationId==TestOnlyCropPolicy.PlotId?InventoryAccess.Ground:InventoryAccess.Ready);
                Replace(s,Changed(job,WaterFillStatus.Complete,job.Progress,s.RuleClock,child));
            }
        }
        public static string Validate(Snapshot s)
        {
            foreach(var vessel in s.Vessels) {
                if(Contents(s,vessel.Id)+ReservedCapacity(s,vessel.Id)>Capacity(vessel.Profile))return "VesselOverbooked";
                var use=s.WaterFills.Where(j=>Involves(s,j,vessel.Id)).SelectMany(j=>s.Work.WorkerIntervals.Where(w=>w.JobId==j.Id)).OrderBy(w=>w.Start).ThenBy(w=>w.End).ToArray();
                for(int i=1;i<use.Length;i++)if(use[i].Start<use[i-1].End)return "OverlappingVesselUse";
            }
            foreach(var job in s.WaterFills) {
                var source=s.InventoryLots.Single(x=>x.LotId==job.SourceLotId);var lot=s.Work.Lots.Single(x=>x.Id==job.SourceLotId);
                var claim=s.Work.Reservations.Single(x=>x.Id==job.ReservationId);
                var destination=s.Vessels.Single(v=>v.Id==job.DestinationId);var sourceContainer=s.Vessels.SingleOrDefault(v=>v.Id==SourceVessel(s,job.SourceLotId));
                if(s.SchemaVersion>=Snapshot.MovableVesselSchema) {
                    destination=VesselHandling.At(s,destination.Id,job.StartedAt,VesselHandling.CreationRevision(job.Id));
                    if(sourceContainer!=null)sourceContainer=VesselHandling.At(s,sourceContainer.Id,job.StartedAt,VesselHandling.CreationRevision(job.Id));
                }
                if((destination.LocationId!=TestOnlyCropPolicy.PlotId&&destination.LocationId!=job.WorkerId)
                    ||(sourceContainer!=null&&sourceContainer.LocationId!=TestOnlyCropPolicy.PlotId&&sourceContainer.LocationId!=job.WorkerId))return "InvalidHistoricalFillCustody";
                if(source.Nutrition!=NutritionKind.WaterPints||source.FreshUntil.HasValue||lot.UnitId!=TestOnlyInventoryPolicy.WaterUnit
                    ||SourceVessel(s,job.SourceLotId)==job.DestinationId||job.StartedAt<source.CreatedAt||job.Progress>new RuleTime(60)
                    ||claim.ConsumedAmount!=default)return "InvalidFillMaterial";
                if(job.Pending) {
                    if(s.InventoryCombat||job.Progress>=new RuleTime(60)||claim.RemainingAmount!=job.Amount||claim.ReleasedAmount!=default)return "InvalidPendingFill";
                } else if(claim.Status!=ReservationStatus.Released||claim.ReleasedAmount!=job.Amount)return "InvalidFillRelease";
                if(job.Status==WaterFillStatus.Complete) {
                    var output=s.InventoryLots.Single(x=>x.LotId==job.OutputLotId);
                    if(job.Progress!=new RuleTime(60)||output.ParentId!=job.SourceLotId||output.CreatedAmount!=job.Amount||output.CreatedAt!=job.EndedAt)
                        return "InvalidFillCompletion";
                }
                if(job.Status==WaterFillStatus.Cancelled&&job.Progress>=new RuleTime(60))return "MissedFillCompletion";
                var work=s.Work.WorkerIntervals.Where(x=>x.JobId==job.Id).ToArray();
                if(work.Any(w=>w.WorkerId!=job.WorkerId||w.Start<job.StartedAt||(job.EndedAt.HasValue&&w.End>job.EndedAt.Value)))return "InvalidFillLaborProvenance";
                RuleTime actual=default;
                foreach(var interval in work.Where(w=>w.Start<s.RuleClock))actual=CampGreens.Add(actual,CampGreens.Subtract(interval.End<s.RuleClock?interval.End:s.RuleClock,interval.Start));
                if(actual!=job.Progress)return "InvalidFillProgress";
                var future=work.Where(w=>w.End>s.RuleClock).ToArray();
                if(job.Status==WaterFillStatus.Working) {
                    if(future.Length!=1||future[0].Start>s.RuleClock||future[0].End!=CampGreens.Add(s.RuleClock,CampGreens.Subtract(new RuleTime(60),job.Progress)))return "InvalidFillBooking";
                    if(Prerequisite(s,job.WorkerId,job.SourceLotId,job.DestinationId,job.Amount,job.Id)!=null)return "InvalidFillAccess";
                } else if(future.Length!=0)return "InactiveFillBooked";
                if(job.Status==WaterFillStatus.Complete&&(work.Length==0||work.Max(w=>w.End)!=job.EndedAt))return "InvalidFillCompletionTime";
            }
            return null;
        }
    }
}
#endif
