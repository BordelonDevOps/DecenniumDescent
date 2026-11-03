#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>
    /// Owner-approved prototype crop procedure. Operates only on a detached transaction candidate.
    /// The selected host policy must establish plot, tools, worker capability, access and ownership.
    /// Advances stop at each earliest milestone; no offline, proportional or duplicate output.
    /// </summary>
    public static class CampGreens
    {
        public const long PlantSeconds=3600,TendSeconds=900,HarvestSeconds=3600,GrowthSeconds=604800,CareSeconds=86400,WindowSeconds=172800;
        public const string SeedUnit="prototype.camp-greens.seed-packet",WaterUnit="prototype.suitable-water.pint",FoodUnit="prototype.camp-greens.food-pound";
        internal static RuleTime Add(RuleTime a,RuleTime b)=>RuleTime.FromFraction((BigInteger)a.Numerator*b.Denominator
            +(BigInteger)b.Numerator*a.Denominator,(BigInteger)a.Denominator*b.Denominator);
        internal static RuleTime Subtract(RuleTime a,RuleTime b)=>RuleTime.FromFraction((BigInteger)a.Numerator*b.Denominator
            -(BigInteger)b.Numerator*a.Denominator,(BigInteger)a.Denominator*b.Denominator);
        internal static int CompareOffset(RuleTime value,RuleTime origin,long seconds)=>
            ((BigInteger)value.Numerator*origin.Denominator).CompareTo(
                ((BigInteger)origin.Numerator+(BigInteger)seconds*origin.Denominator)*value.Denominator);
        internal static long Duration(CropWorkKind kind)=>kind==CropWorkKind.Plant?PlantSeconds:kind==CropWorkKind.Tend?TendSeconds:HarvestSeconds;
        private static bool Closed(CropStage stage)=>stage==CropStage.Harvested||stage==CropStage.Failed;
        private static bool Eligible(CropDraft crop,RuleTime at)=>crop.Suitable&&crop.CareUntil.HasValue&&at<crop.CareUntil.Value;
        private static CropWorkRecord UpdateTask(CropWorkRecord task,CropWorkStatus status,RuleTime progress,RuleTime? end,string worker=null)
            =>new CropWorkRecord(task.Id,worker??task.WorkerId,task.Kind,status,task.StartedAt,progress,end,task.InputReservations);
        private static void Replace(Snapshot state,CropBatchRecord crop)
        {state.Crops=state.Crops.Select(c=>c.Id==crop.Id?crop:c).ToArray();}
        private static string NewId(Snapshot state,string kind)=>"crop."+kind+"."+checked(state.Revision+1).ToString(CultureInfo.InvariantCulture);

        public static void Plant(Snapshot state,string batchId,string plotId,string seedLotId,string waterLotId,string workerId)
        {
            if(!Validation.ValidId(batchId))throw new ArgumentException("Invalid crop identity.");
            var existing=state.Crops.SingleOrDefault(c=>c.Id==batchId);
            if(existing!=null) {
                if(existing.Stage!=CropStage.Planting)throw new ArgumentException("Crop identity cannot be reused.");
                StartWork(state,existing,CropWorkKind.Plant,workerId,waterLotId);return;
            }
            if(state.Crops.Any(c=>c.PlotId==plotId&&!Closed(c.Stage)))throw new ArgumentException("Plot is occupied.");
            var plot=state.CropPlots.SingleOrDefault(p=>p.Id==plotId)??throw new ArgumentException("Unknown plot.");
            if(!plot.Suitable)throw new ArgumentException("Planting conditions are unsuitable.");
            if(state.Crops.Length>=Snapshot.MaxCropBatches)throw new InvalidOperationException("Crop session history is full.");
            var task=CreateTask(state,CropWorkKind.Plant,workerId,plotId,seedLotId,waterLotId);
            var crop=new CropBatchRecord(batchId,plotId,seedLotId,plot.OwnerId,state.RuleClock,state.RuleClock,CropStage.Planting,
                default,null,null,null,null,new[]{task});
            state.Crops=state.Crops.Concat(new[]{crop}).ToArray();
            Book(state,task);
        }
        public static void Tend(Snapshot state,string batchId,string workerId,string waterLotId)
        {
            var crop=Find(state,batchId);if(crop.Stage!=CropStage.Growing)throw new ArgumentException("Only growing crops need tending.");
            StartWork(state,crop,CropWorkKind.Tend,workerId,waterLotId);
        }
        public static void Harvest(Snapshot state,string batchId,string workerId)
        {
            var crop=Find(state,batchId);if(crop.Stage!=CropStage.Mature)throw new ArgumentException("Crop is not harvestable.");
            StartWork(state,crop,CropWorkKind.Harvest,workerId,null);
        }
        private static CropBatchRecord Find(Snapshot state,string id)=>state.Crops.SingleOrDefault(c=>c.Id==id)??throw new ArgumentException("Unknown crop.");
        private static void StartWork(Snapshot state,CropBatchRecord crop,CropWorkKind kind,string worker,string waterLot)
        {
            if(crop.Tasks.Any(t=>t.Status==CropWorkStatus.Working))throw new ArgumentException("Crop already has active work.");
            var draft=Draft(state,crop);var paused=draft.Tasks.SingleOrDefault(t=>t.Kind==kind&&t.Status==CropWorkStatus.Paused);
            CropWorkRecord task;
            if(paused!=null) {
                task=UpdateTask(paused,CropWorkStatus.Working,paused.Progress,null,worker);
                draft.Tasks[draft.Tasks.IndexOf(paused)]=task;
            } else {
                if(kind==CropWorkKind.Plant || draft.Tasks.Count>=CropBatchRecord.MaxTasks)throw new ArgumentException("Cannot create this crop task.");
                task=CreateTask(state,kind,worker,crop.PlotId,null,waterLot);draft.Tasks.Add(task);
            }
            Book(state,task);Replace(state,draft.Build());
        }
        private static CropWorkRecord CreateTask(Snapshot state,CropWorkKind kind,string worker,string plot,string seedLot,string waterLot)
        {
            string id=NewId(state,"task");var claims=new List<ResourceReservation>();
            void Input(string suffix,string lotId,string unit,long quantity) {
                var lot=state.Work.Lots.SingleOrDefault(l=>l.Id==lotId)??throw new ArgumentException("Missing crop input lot.");
                if(lot.UnitId!=unit||lot.LocationId!=plot)throw new ArgumentException("Wrong crop input unit or location.");
                claims.Add(new ResourceReservation(id+suffix,id,lotId,quantity));
            }
            if(kind==CropWorkKind.Plant)Input(".seed",seedLot,SeedUnit,1); // One explicitly authored0.1-lb packet.
            if(kind!=CropWorkKind.Harvest)Input(".water",waterLot,WaterUnit,8);
            state.Work=state.Work.Reserve(id,Array.Empty<WorkerInterval>(),claims);
            foreach(var claim in claims)state.Work=state.Work.Consume(id,claim.Id);
            return new CropWorkRecord(id,worker,kind,CropWorkStatus.Working,state.RuleClock,default,null,claims.Select(c=>c.Id));
        }
        private static void Book(Snapshot state,CropWorkRecord task)
        {
            var remaining=Subtract(new RuleTime(Duration(task.Kind)),task.Progress);
            var interval=new WorkerInterval(NewId(state,"labor"),task.Id,task.WorkerId,state.RuleClock,Add(state.RuleClock,remaining));
            state.Work=state.Work.Reserve(task.Id,new[]{interval},Array.Empty<ResourceReservation>());
        }
        public static void Pause(Snapshot state,string batchId,string worker)
        {
            var draft=Draft(state,Find(state,batchId));var task=draft.Tasks.SingleOrDefault(t=>t.Status==CropWorkStatus.Working);
            if(task==null||task.WorkerId!=worker)throw new ArgumentException("Worker has no active crop task.");
            state.Work=state.Work.CancelFutureWork(task.Id,state.RuleClock);
            draft.Tasks[draft.Tasks.IndexOf(task)]=UpdateTask(task,CropWorkStatus.Paused,task.Progress,null);
            Replace(state,draft.Build());
        }
        public static void SetSuitable(Snapshot state,string plotId,bool suitable)
        {
            var plot=state.CropPlots.SingleOrDefault(p=>p.Id==plotId)??throw new ArgumentException("Unknown plot.");
            state.CropPlots=state.CropPlots.Select(p=>p.Id==plotId?new CropPlotRecord(p.Id,p.OwnerId,suitable):p).ToArray();
            foreach(var crop in state.Crops.Where(c=>c.PlotId==plotId)) {
                var draft=Draft(state,crop);
                if(draft.Stage==CropStage.Growing) {
                    if(draft.UnsuitableSince.HasValue && CompareOffset(state.RuleClock,draft.UnsuitableSince.Value,WindowSeconds)>=0)Fail(state,draft);
                    else RefreshEligibility(draft,state.RuleClock);
                }
                Replace(state,draft.Build());
            }
        }
        private static void RefreshEligibility(CropDraft crop,RuleTime at)
        {if(Eligible(crop,at))crop.UnsuitableSince=null;else if(!crop.UnsuitableSince.HasValue)crop.UnsuitableSince=at;}

        public static RuleTime Advance(Snapshot state,RuleTime requestedEnd)
            =>AdvanceExact(state,requestedEnd.Numerator,requestedEnd.Denominator);
        public static RuleTime AdvanceBy(Snapshot state,RuleTime elapsed)
            =>AdvanceExact(state,(BigInteger)state.RuleClock.Numerator*elapsed.Denominator
                +(BigInteger)elapsed.Numerator*state.RuleClock.Denominator,(BigInteger)state.RuleClock.Denominator*elapsed.Denominator);
        private static RuleTime AdvanceExact(Snapshot state,BigInteger targetNumerator,BigInteger targetDenominator)
        {
            RuleTime now=state.RuleClock;
            if(targetNumerator*now.Denominator<=((BigInteger)now.Numerator*targetDenominator))throw new ArgumentException("Positive crop advance required.");
            // Compare before converting: an unreachable later deadline may exceed RuleTime capacity.
            void DueAfter(RuleTime origin,RuleTime delay) {
                BigInteger n=(BigInteger)origin.Numerator*delay.Denominator+(BigInteger)delay.Numerator*origin.Denominator;
                BigInteger d=(BigInteger)origin.Denominator*delay.Denominator;
                if(n*now.Denominator<(BigInteger)now.Numerator*d)throw new ArgumentException("Unresolved overdue crop milestone.");
                if(n*targetDenominator<targetNumerator*d){targetNumerator=n;targetDenominator=d;}
            }
            void Due(RuleTime at)=>DueAfter(at,default);
            foreach(var record in state.Crops) {
                var crop=Draft(state,record);
                foreach(var task in crop.Tasks.Where(t=>t.Status==CropWorkStatus.Working))DueAfter(now,Subtract(new RuleTime(Duration(task.Kind)),task.Progress));
                if(crop.Stage==CropStage.Growing) {
                    if(Eligible(crop,now)) {Due(crop.CareUntil.Value);DueAfter(now,Subtract(new RuleTime(GrowthSeconds),crop.Growth));}
                    else DueAfter(crop.UnsuitableSince.Value,new RuleTime(WindowSeconds));
                }
                if(crop.Stage==CropStage.Mature)DueAfter(crop.MaturedAt.Value,new RuleTime(WindowSeconds));
            }
            foreach(var food in state.CropFood.Where(f=>!f.Expired))Due(food.FreshUntil);
            RuleTime target=RuleTime.FromFraction(targetNumerator,targetDenominator);
            var elapsed=Subtract(target,now);var outputs=state.CropFood.ToList();var crops=new List<CropBatchRecord>();
            foreach(var record in state.Crops) {
                var crop=Draft(state,record);crop.UpdatedAt=target;
                if(crop.Stage==CropStage.Growing&&Eligible(crop,now))crop.Growth=Add(crop.Growth,elapsed);
                for(int i=0;i<crop.Tasks.Count;i++) {
                    var task=crop.Tasks[i];if(task.Status==CropWorkStatus.Working)
                        crop.Tasks[i]=UpdateTask(task,task.Status,Add(task.Progress,elapsed),null);
                }
                // Failure wins over care recovery exactly at the continuous-neglect endpoint.
                if(crop.Stage==CropStage.Growing&&crop.UnsuitableSince.HasValue&&CompareOffset(target,crop.UnsuitableSince.Value,WindowSeconds)>=0)Fail(state,crop);
                if(!Closed(crop.Stage)) {
                    for(int i=0;i<crop.Tasks.Count;i++) {
                        var task=crop.Tasks[i];if(task.Status!=CropWorkStatus.Working||task.Progress!=new RuleTime(Duration(task.Kind)))continue;
                        crop.Tasks[i]=UpdateTask(task,CropWorkStatus.Complete,task.Progress,target);
                        if(task.Kind==CropWorkKind.Plant) {crop.Stage=CropStage.Growing;crop.CareUntil=target.AddSeconds(CareSeconds);RefreshEligibility(crop,target);}
                        if(task.Kind==CropWorkKind.Tend) {crop.CareUntil=target.AddSeconds(CareSeconds);RefreshEligibility(crop,target);}
                        if(task.Kind==CropWorkKind.Harvest) {
                            crop.Stage=CropStage.Harvested;crop.ClosedAt=target;
                            string lotId=task.Id+".food";RuleTime freshness=task.StartedAt.AddSeconds(WindowSeconds);
                            state.Work=new WorkLedger(state.Work.Lots.Concat(new[]{new ResourceLot(lotId,FoodUnit,8,crop.PlotId,crop.OwnerId)}),
                                state.Work.WorkerIntervals,state.Work.Reservations);
                            outputs.Add(new CropFoodRecord(lotId,crop.Id,freshness,target>=freshness));
                        }
                    }
                    if(crop.Stage==CropStage.Growing&&crop.Growth==new RuleTime(GrowthSeconds)) {
                        crop.Stage=CropStage.Mature;crop.MaturedAt=target;crop.UnsuitableSince=null;CancelTasks(state,crop);
                    }
                    if(crop.Stage==CropStage.Mature&&CompareOffset(target,crop.MaturedAt.Value,WindowSeconds)>=0)Fail(state,crop);
                    if(crop.Stage==CropStage.Growing)RefreshEligibility(crop,target);
                }
                crops.Add(crop.Build());
            }
            state.CropFood=outputs.Select(f=>!f.Expired&&target>=f.FreshUntil?new CropFoodRecord(f.LotId,f.BatchId,f.FreshUntil,true):f).ToArray();
            state.Crops=crops.ToArray();state.RuleClock=target;return target;
        }
        private static void Fail(Snapshot state,CropDraft crop)
        {crop.Stage=CropStage.Failed;crop.ClosedAt=crop.UpdatedAt;CancelTasks(state,crop);}
        private static void CancelTasks(Snapshot state,CropDraft crop)
        {
            for(int i=0;i<crop.Tasks.Count;i++) {
                var task=crop.Tasks[i];if(task.Status!=CropWorkStatus.Working&&task.Status!=CropWorkStatus.Paused)continue;
                state.Work=state.Work.CancelFutureWork(task.Id,crop.UpdatedAt);
                foreach(var id in task.InputReservations) {
                    var claim=state.Work.Reservations.Single(r=>r.Id==id);
                    if(claim.Status==ReservationStatus.Reserved)state.Work=state.Work.Release(task.Id,id);
                }
                crop.Tasks[i]=UpdateTask(task,CropWorkStatus.Cancelled,task.Progress,crop.UpdatedAt);
            }
        }
        public static long EdibleFood(Snapshot state)=>state.SchemaVersion==Snapshot.InventorySchema
            ?throw new InvalidOperationException("Use the exact inventory food projection for schema4 descendants."):state.CropFood.Where(f=>!f.Expired&&state.RuleClock<f.FreshUntil)
            .Sum(f=>state.Work.Lots.Single(l=>l.Id==f.LotId).Quantity);
        private static CropDraft Draft(Snapshot state,CropBatchRecord crop)=>new CropDraft(crop,state.CropPlots.Single(p=>p.Id==crop.PlotId).Suitable);

        private sealed class CropDraft
        {
            public string Id,PlotId,SeedLotId,OwnerId;public RuleTime CreatedAt,UpdatedAt,Growth;public CropStage Stage;public bool Suitable;
            public RuleTime? CareUntil,UnsuitableSince,MaturedAt,ClosedAt;public List<CropWorkRecord> Tasks;
            public CropDraft(CropBatchRecord c,bool suitable){Id=c.Id;PlotId=c.PlotId;SeedLotId=c.SeedLotId;OwnerId=c.OwnerId;CreatedAt=c.CreatedAt;UpdatedAt=c.UpdatedAt;
                Growth=c.Growth;Stage=c.Stage;Suitable=suitable;CareUntil=c.CareUntil;UnsuitableSince=c.UnsuitableSince;MaturedAt=c.MaturedAt;ClosedAt=c.ClosedAt;Tasks=c.Tasks.ToList();}
            public CropBatchRecord Build()=>new CropBatchRecord(Id,PlotId,SeedLotId,OwnerId,CreatedAt,UpdatedAt,Stage,Growth,CareUntil,UnsuitableSince,MaturedAt,ClosedAt,Tasks);
        }
    }
}
#endif
