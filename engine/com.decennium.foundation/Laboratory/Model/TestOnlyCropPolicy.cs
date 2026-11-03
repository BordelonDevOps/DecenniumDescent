#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>
    /// Bounded prepared-plot host for the adopted Camp Greens procedure. The synthetic world
    /// supplies a capable companion, compatible permanent tools and a prepared10x10-foot plot.
    /// Its abstract reach test is a fixture, not production geometry/tool acquisition or character legality.
    /// </summary>
    public sealed class TestOnlyCropPolicy : ICommandPolicy
    {
        public const string PlotId="TEST_ONLY.prepared-plot",SeedLotId="TEST_ONLY.seed-packets",WaterLotId="TEST_ONLY.water-pints";
        public const int PlotWidthFeet=10,PlotLengthFeet=10;
        private readonly long seeds,water;
        private readonly TestOnlyPolicy world=new TestOnlyPolicy();
        public TestOnlyCropPolicy(long seedPackets=8,long waterPints=512)
        {if(seedPackets<0||waterPints<0)throw new ArgumentOutOfRangeException(nameof(seedPackets));seeds=seedPackets;water=waterPints;}
        public string ContentFingerprint=>"TEST_ONLY.camp-greens-v1-s"+seeds.ToString(CultureInfo.InvariantCulture)+"-w"+water.ToString(CultureInfo.InvariantCulture);
        public bool TestOnly=>true;
        public static Authority Host()=>new Authority("TEST_ONLY.host",new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId},true,true);
        public Snapshot Initial()
        {
            var s=world.Initial();s.SchemaVersion=Snapshot.CropSchema;s.ContentFingerprint=ContentFingerprint;
            s.CropPlots=new[]{new CropPlotRecord(PlotId,TestOnlyPolicy.CompanionId,true)};
            s.Work=new WorkLedger(new[]{new ResourceLot(SeedLotId,CampGreens.SeedUnit,seeds,PlotId,TestOnlyPolicy.CompanionId),
                new ResourceLot(WaterLotId,CampGreens.WaterUnit,water,PlotId,TestOnlyPolicy.CompanionId)});
            return s;
        }
        private static bool AtPlot(ActorState actor)=>Math.Abs((long)actor.X-3)+Math.Abs((long)actor.Y-3)<=1;
        public string Resolve(Snapshot s,Command c)
        {
            if(c.Kind==CommandKind.AdvanceClock) {
                if(c.Target!=""||c.X<1||c.Y<1)return "InvalidCropAdvance";
                CampGreens.AdvanceBy(s,new RuleTime(c.X,c.Y));return null;
            }
            if(c.Kind==CommandKind.SetCropConditions) {
                if(c.Target!=PlotId||c.Y!=0||(c.X!=0&&c.X!=1))return "InvalidConditions";
                CampGreens.SetSuitable(s,PlotId,c.X==1);return null;
            }
            if(c.Kind==CommandKind.Move||c.Kind==CommandKind.Interact) {
                if(s.Crops.SelectMany(crop=>crop.Tasks).Any(t=>t.WorkerId==c.Actor&&t.Status==CropWorkStatus.Working))return "WorkerBusy";
                return world.Resolve(s,c);
            }
            if(c.Actor!=TestOnlyPolicy.CompanionId)return "WrongWorker";
            if(c.X!=0||c.Y!=0||!AtPlot(s.Actors.Single(a=>a.Id==c.Actor)))return "InvalidCropWorkAccess";
            switch(c.Kind) {
                case CommandKind.PlantCrop:CampGreens.Plant(s,c.Target,PlotId,SeedLotId,WaterLotId,c.Actor);return null;
                case CommandKind.TendCrop:CampGreens.Tend(s,c.Target,c.Actor,WaterLotId);return null;
                case CommandKind.HarvestCrop:CampGreens.Harvest(s,c.Target,c.Actor);return null;
                case CommandKind.PauseCrop:CampGreens.Pause(s,c.Target,c.Actor);return null;
                default:return "UnsupportedCommand";
            }
        }
        public string ValidateState(Snapshot s)
        {
            try{return ValidateCropState(s);}
            catch(Exception ex) when(ex is ArgumentException||ex is InvalidOperationException||ex is OverflowException)
            {return "InvalidCropState";}
        }
        private static bool GrowthHasRecordedCare(CropBatchRecord crop)
        {
            // Conditions are not an event journal. This is a necessary upper bound, not a replay claim.
            RuleTime horizon=crop.MaturedAt??crop.ClosedAt??crop.UpdatedAt;
            RuleTime cursor=crop.Tasks[0].EndedAt.Value;
            BigInteger earnedNumerator=0,earnedDenominator=1;
            foreach(var care in crop.Tasks.Where(t=>(t.Kind==CropWorkKind.Plant||t.Kind==CropWorkKind.Tend)
                &&t.Status==CropWorkStatus.Complete).OrderBy(t=>t.EndedAt.Value)) {
                RuleTime start=care.EndedAt.Value>cursor?care.EndedAt.Value:cursor;
                RuleTime end=care.EndedAt.Value.AddSeconds(CampGreens.CareSeconds);
                if(end>horizon)end=horizon;
                if(end<=start)continue;
                BigInteger n=(BigInteger)end.Numerator*start.Denominator-(BigInteger)start.Numerator*end.Denominator;
                BigInteger d=(BigInteger)end.Denominator*start.Denominator;
                earnedNumerator=earnedNumerator*d+n*earnedDenominator;earnedDenominator*=d;
                BigInteger gcd=BigInteger.GreatestCommonDivisor(earnedNumerator,earnedDenominator);
                earnedNumerator/=gcd;earnedDenominator/=gcd;cursor=end;
            }
            return (BigInteger)crop.Growth.Numerator*earnedDenominator<=earnedNumerator*crop.Growth.Denominator;
        }
        private string ValidateCropState(Snapshot s)
        {
            if(s.SchemaVersion!=Snapshot.CropSchema||s.Work==null)return "WrongCropSchema";
            string worldError=TestOnlyPolicy.ValidateWorld(s);if(worldError!=null)return worldError;
            if(s.CropPlots.Length!=1||s.CropPlots[0].Id!=PlotId||s.CropPlots[0].OwnerId!=TestOnlyPolicy.CompanionId)return "InvalidPlot";
            var tasks=s.Crops.SelectMany(c=>c.Tasks).ToArray();
            if(s.Work.Lots.Count!=2+s.CropFood.Length||s.Work.Reservations.Count!=tasks.Sum(t=>t.InputReservations.Count)
                ||s.Work.Reservations.Any(r=>r.Status!=ReservationStatus.Consumed||!tasks.Any(t=>t.Id==r.JobId&&t.InputReservations.Contains(r.Id)))
                ||s.Work.WorkerIntervals.Any(w=>!tasks.Any(t=>t.Id==w.JobId)))return "InvalidCropLedger";
            bool Stock(string id,string unit,long initial) {
                var lot=s.Work.Lots.Single(l=>l.Id==id);
                long consumed=s.Work.Reservations.Where(r=>r.LotId==id).Sum(r=>r.Quantity);
                return lot.UnitId==unit&&lot.LocationId==PlotId&&lot.CustodianId==TestOnlyPolicy.CompanionId
                    &&consumed<=initial&&lot.Quantity==initial-consumed;
            }
            if(!Stock(SeedLotId,CampGreens.SeedUnit,seeds)||!Stock(WaterLotId,CampGreens.WaterUnit,water))return "InvalidCropStock";
            if(s.Crops.Count(c=>c.Stage!=CropStage.Harvested&&c.Stage!=CropStage.Failed)>1)return "PlotOccupiedTwice";
            foreach(var crop in s.Crops) {
                if(crop.PlotId!=PlotId||crop.SeedLotId!=SeedLotId||crop.OwnerId!=TestOnlyPolicy.CompanionId
                    ||crop.Growth>new RuleTime(CampGreens.GrowthSeconds))return "InvalidCropProfile";
                if(crop.Tasks[0].Kind!=CropWorkKind.Plant||crop.Tasks.Count(t=>t.Kind==CropWorkKind.Plant)!=1
                    ||crop.Tasks.Count(t=>t.Kind==CropWorkKind.Harvest)>1)return "InvalidCropPhases";
                var plant=crop.Tasks[0];bool planted=plant.Status==CropWorkStatus.Complete;
                if((crop.Stage==CropStage.Planting)==planted)return "InvalidPlantingState";
                if(!planted&&(crop.Tasks.Count!=1||crop.Growth!=default||crop.CareUntil.HasValue||crop.MaturedAt.HasValue||crop.UnsuitableSince.HasValue))return "PrematureGrowth";
                if(planted) {
                    var lastCare=crop.Tasks.Where(t=>(t.Kind==CropWorkKind.Plant||t.Kind==CropWorkKind.Tend)&&t.Status==CropWorkStatus.Complete)
                        .Max(t=>t.EndedAt.Value);
                    if(crop.CareUntil!=lastCare.AddSeconds(CampGreens.CareSeconds))return "InvalidCareDeadline";
                    if(!GrowthHasRecordedCare(crop))return "UnsupportedGrowth";
                }
                if(crop.Stage==CropStage.Growing) {
                    if(crop.Growth>=new RuleTime(CampGreens.GrowthSeconds)||crop.MaturedAt.HasValue)return "MissedMaturity";
                    bool eligible=s.CropPlots[0].Suitable&&s.RuleClock<crop.CareUntil.Value;
                    if(eligible==crop.UnsuitableSince.HasValue
                        ||(crop.UnsuitableSince.HasValue&&CampGreens.CompareOffset(s.RuleClock,crop.UnsuitableSince.Value,CampGreens.WindowSeconds)>=0))return "InvalidNeglectState";
                }
                if(crop.Stage==CropStage.Mature||crop.Stage==CropStage.Harvested) {
                    if(crop.Growth!=new RuleTime(CampGreens.GrowthSeconds)||!crop.MaturedAt.HasValue||crop.UnsuitableSince.HasValue)return "InvalidMaturity";
                    if(crop.Stage==CropStage.Mature&&CampGreens.CompareOffset(s.RuleClock,crop.MaturedAt.Value,CampGreens.WindowSeconds)>=0)return "MissedHarvestDeadline";
                }
                if(crop.MaturedAt.HasValue&&CampGreens.CompareOffset(crop.MaturedAt.Value,plant.EndedAt.Value,CampGreens.GrowthSeconds)<0)return "EarlyMaturity";
                foreach(var task in crop.Tasks) {
                    if(task.WorkerId!=TestOnlyPolicy.CompanionId||task.Progress>new RuleTime(CampGreens.Duration(task.Kind)))return "InvalidLabor";
                    bool complete=task.Status==CropWorkStatus.Complete;
                    if((task.Kind==CropWorkKind.Tend&&(!planted||task.StartedAt<plant.EndedAt.Value))
                        ||(task.Kind==CropWorkKind.Harvest&&(!crop.MaturedAt.HasValue||task.StartedAt<crop.MaturedAt.Value))
                        ||(crop.ClosedAt.HasValue&&task.EndedAt.HasValue&&task.EndedAt.Value>crop.ClosedAt.Value)
                        ||(task.Kind==CropWorkKind.Tend&&crop.MaturedAt.HasValue&&task.EndedAt.HasValue&&task.EndedAt.Value>crop.MaturedAt.Value))return "InvalidPhaseChronology";
                    if(complete&&task.Progress!=new RuleTime(CampGreens.Duration(task.Kind)))return "IncompleteTask";
                    if((task.Status==CropWorkStatus.Working||task.Status==CropWorkStatus.Paused)&&task.Progress>=new RuleTime(CampGreens.Duration(task.Kind)))return "UnresolvedTask";
                    if(task.Status==CropWorkStatus.Working) {
                        if(!AtPlot(s.Actors.Single(a=>a.Id==task.WorkerId)))return "WorkerLeftPlot";
                        if((task.Kind==CropWorkKind.Plant&&crop.Stage!=CropStage.Planting)
                            ||(task.Kind==CropWorkKind.Tend&&crop.Stage!=CropStage.Growing)
                            ||(task.Kind==CropWorkKind.Harvest&&crop.Stage!=CropStage.Mature))return "WrongActivePhase";
                    }
                    if((crop.Stage==CropStage.Harvested||crop.Stage==CropStage.Failed)
                        &&(task.Status==CropWorkStatus.Working||task.Status==CropWorkStatus.Paused))return "ClosedCropHasWork";
                    var claims=task.InputReservations.Select(id=>s.Work.Reservations.Single(r=>r.Id==id)).ToArray();
                    int wanted=task.Kind==CropWorkKind.Plant?2:task.Kind==CropWorkKind.Tend?1:0;
                    if(claims.Length!=wanted||claims.Any(r=>r.Status!=ReservationStatus.Consumed||r.JobId!=task.Id))return "InvalidInputCommitment";
                    if(task.Kind!=CropWorkKind.Harvest&&claims.Count(r=>r.LotId==WaterLotId&&r.Quantity==8)!=1)return "InvalidWaterCommitment";
                    if(task.Kind==CropWorkKind.Plant&&claims.Count(r=>r.LotId==SeedLotId&&r.Quantity==1)!=1)return "InvalidSeedCommitment";
                    RuleTime actual=default;var intervals=s.Work.WorkerIntervals.Where(w=>w.JobId==task.Id).ToArray();
                    if(intervals.Any(w=>w.WorkerId!=task.WorkerId||w.Start<task.StartedAt
                        ||(task.EndedAt.HasValue&&w.End>task.EndedAt.Value)))return "InvalidLaborProvenance";
                    if(complete&&(intervals.Length==0||intervals.Max(w=>w.End)!=task.EndedAt.Value))return "InvalidCompletionTime";
                    foreach(var interval in intervals.Where(w=>w.Start<s.RuleClock)) {
                        RuleTime end=interval.End<s.RuleClock?interval.End:s.RuleClock;
                        actual=CampGreens.Add(actual,CampGreens.Subtract(end,interval.Start));
                        if(actual>new RuleTime(CampGreens.Duration(task.Kind)))return "ExcessLabor";
                    }
                    if(actual!=task.Progress)return "UncreditedLaborMismatch";
                    var future=intervals.Where(w=>w.End>s.RuleClock).ToArray();
                    if(task.Status==CropWorkStatus.Working) {
                        if(future.Length!=1||future[0].WorkerId!=task.WorkerId||future[0].Start>s.RuleClock
                            ||future[0].End!=CampGreens.Add(s.RuleClock,CampGreens.Subtract(new RuleTime(CampGreens.Duration(task.Kind)),task.Progress)))return "InvalidActiveBooking";
                    } else if(future.Length!=0)return "InactiveWorkBooked";
                }
                var foods=s.CropFood.Where(f=>f.BatchId==crop.Id).ToArray();
                if((crop.Stage==CropStage.Harvested)!=(foods.Length==1))return "InvalidHarvestSettlement";
                if(foods.Length==1) {
                    var harvest=crop.Tasks.Single(t=>t.Kind==CropWorkKind.Harvest);
                    if(harvest.Status!=CropWorkStatus.Complete||crop.ClosedAt!=harvest.EndedAt
                        ||CampGreens.CompareOffset(crop.ClosedAt.Value,crop.MaturedAt.Value,CampGreens.WindowSeconds)>0
                        ||foods[0].FreshUntil!=harvest.StartedAt.AddSeconds(CampGreens.WindowSeconds))return "InvalidHarvestTiming";
                }
            }
            foreach(var food in s.CropFood) {
                var lot=s.Work.Lots.Single(l=>l.Id==food.LotId);
                if(lot.UnitId!=CampGreens.FoodUnit||lot.Quantity!=8||lot.LocationId!=PlotId||lot.CustodianId!=TestOnlyPolicy.CompanionId
                    ||food.Expired!=(s.RuleClock>=food.FreshUntil))return "InvalidFoodLot";
            }
            return null;
        }
    }
}
#endif
