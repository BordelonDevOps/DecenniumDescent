#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Numerics;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string CropId="TEST_ONLY.crop";
        private static Simulation Farm(long seeds=8,long water=512)
        {var p=new TestOnlyCropPolicy(seeds,water);return new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);}
        private static Simulation MultiworkerFarm()
        {
            var p=new TestOnlyCropPolicy(workerIds:new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId});var state=p.Initial();
            var actor=state.Actors.Single(a=>a.Id==TestOnlyPolicy.ActorId);actor.X=2;actor.Y=3;
            return new Simulation(p,state,ExecutionProfile.Laboratory);
        }
        private static Command FarmCommand(Simulation s,CommandKind kind,string target=CropId,int x=0,int y=0,string actor=TestOnlyPolicy.CompanionId,string id=null)
            =>new Command(id??("farm-"+s.Capture().Revision),actor,s.Capture().Revision,kind,target,x,y);
        private static void FarmCommit(Simulation s,Command c)
        {var r=s.Execute(TestOnlyCropPolicy.Host(),c);Require(r.Outcome==Outcome.Committed,"Crop command rejected: "+c.Kind+" "+r.Code);}
        private static void FarmWork(Simulation s,CommandKind kind,string crop=CropId)=>FarmCommit(s,FarmCommand(s,kind,crop));
        private static CropBatchRecord Crop(Simulation s,string id=CropId)=>s.Capture().Crops.Single(c=>c.Id==id);
        private static RuleTime FarmDifference(RuleTime end,RuleTime start)=>RuleTime.FromFraction(
            (BigInteger)end.Numerator*start.Denominator-(BigInteger)start.Numerator*end.Denominator,(BigInteger)end.Denominator*start.Denominator);
        private static void FarmUntil(Simulation s,RuleTime target)
        {
            for(int count=0;s.Capture().RuleClock<target;count++) {
                Require(count<128,"Crop milestone loop failed to advance.");var now=s.Capture().RuleClock;
                RuleTime delta=FarmDifference(target,now);
                FarmCommit(s,FarmCommand(s,CommandKind.AdvanceClock,"",checked((int)delta.Numerator),checked((int)delta.Denominator),TestOnlyPolicy.ActorId));
                Require(s.Capture().RuleClock>now,"Due crop event did not progress.");
            }
            Require(s.Capture().RuleClock==target,"Crop clock overshot.");
        }
        private static void FarmAdvance(Simulation s,long seconds)=>FarmUntil(s,s.Capture().RuleClock.AddSeconds(seconds));
        private static void FarmConditions(Simulation s,bool suitable)
            =>FarmCommit(s,FarmCommand(s,CommandKind.SetCropConditions,TestOnlyCropPolicy.PlotId,suitable?1:0,actor:TestOnlyPolicy.ActorId));
        private static void Planted(Simulation s){FarmWork(s,CommandKind.PlantCrop);FarmAdvance(s,3600);}
        private static void Mature(Simulation s)
        {
            Planted(s);
            for(int day=0;day<6;day++) {
                var expires=Crop(s).CareUntil.Value;
                FarmUntil(s,FarmDifference(expires,T(900)));FarmWork(s,CommandKind.TendCrop);FarmUntil(s,expires);
            }
            FarmUntil(s,T(608400));Require(Crop(s).Stage==CropStage.Mature,"Seven cared growth days must mature.");
        }
        private static Simulation RestoreFarm(Simulation s)
            =>new Simulation(new TestOnlyCropPolicy(),new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);

        private static TestOnlySharedWorldPolicy FirstWorkWorld()
            =>new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableCampGreensAssignments().EnableCampGreensFirstWorkTending();

        private static Command AssignCampGreens(Simulation simulation,ExpeditionWorkProcedure procedure)
        {
            WorldCommit(simulation,ExpeditionCommand(simulation,CommandKind.AssignExpeditionWork,
                request:new ExpeditionAssignmentRequest(procedure,CropId)));
            var assignment=simulation.Capture().ExpeditionAssignments.Single(x=>x.Open);
            return ExpeditionCommand(simulation,CommandKind.StartExpeditionWork,assignment.Id);
        }

        private static ResourceReservation TendingClaim(Snapshot s)
        {
            var task=s.Crops.Single().Tasks.Last(x=>x.Kind==CropWorkKind.Tend);
            return s.Work.Reservations.Single(x=>x.Id==task.InputReservations.Single());
        }

        private static void AssertTendingWater(Snapshot s,long stock,long available,ReservationStatus status)
        {
            var claim=TendingClaim(s);
            Require(s.Work.Lots.Single(x=>x.Id==TestOnlyCropPolicy.WaterLotId).Quantity==stock
                &&s.Work.AvailableAmount(TestOnlyCropPolicy.WaterLotId)==new RuleQuantity(available)
                &&claim.Quantity==8&&claim.Status==status,"Wrong tending stock or claim settlement: "+claim.Status);
        }

        private static void AddFirstWorkTendingCases(Dictionary<string,Action> cases,string directory)
        {
            const string worker=TestOnlyPolicy.CompanionId;
            var host=TestOnlySharedWorldPolicy.Host();
            var codec=new SnapshotCodec();
            cases.Add("mgt08_tending_assigned_fractional_first_work_pause_save_harvest_and_intake",()=>{
                var policy=FirstWorkWorld();
                var run=World(policy);
                WorldCommit(run,AssignCampGreens(run,ExpeditionWorkProcedure.CropPlanting));
                WorldAdvance(run,3600);
                var originalCare=Crop(run).CareUntil;
                WorldAdvance(run,85493);
                var start=AssignCampGreens(run,ExpeditionWorkProcedure.CropTending);
                Require(run.Capture().Work.Reservations.Count==2,"Assigning tending created an input claim before work start.");
                byte[] before=Bytes(run);
                Require(run.QueryCommand(host,start).Admissible&&before.SequenceEqual(Bytes(run)),"Tending preview changed the world.");
                WorldCommit(run,start);
                var admitted=run.Capture();
                var task=Crop(run).Tasks.Last();
                Require(admitted.SchemaVersion==Snapshot.ExpeditionAssignmentSchema&&task.Progress==default
                    &&admitted.ExpeditionAssignments.Single(x=>x.Id==start.Target).WorkId==task.Id
                    &&Crop(run).CareUntil==originalCare,"Assigned admission changed care, progress, or task linkage.");
                AssertTendingWater(admitted,504,496,ReservationStatus.Reserved);
                byte[] afterStart=Bytes(run);
                Require(run.Execute(host,start).Outcome==Outcome.Duplicate&&afterStart.SequenceEqual(Bytes(run)),"Duplicate start changed the claim.");
                var conflict=new Command(start.Id,start.Actor,start.ExpectedRevision,start.Kind,"TEST_ONLY.other-assignment");
                Require(run.QueryCommand(host,conflict).Code=="CommandIdConflict"
                    &&run.Execute(host,conflict).Code=="CommandIdConflict"&&afterStart.SequenceEqual(Bytes(run)),"A conflicting receipt changed tending.");
                var busy=IC(run,CommandKind.TendCrop,CropId,actor:worker);
                var rejected=run.QueryCommand(host,busy);
                Require(rejected.Supported&&!rejected.Admissible&&run.Execute(host,busy).Code==rejected.Code
                    &&afterStart.SequenceEqual(Bytes(run)),"Concurrent tending preview and execution diverged.");
                WorldCommit(run,IC(run,CommandKind.PauseCrop,CropId,actor:worker));
                WorldAdvance(run,7);
                var paused=run.Capture();
                AssertTendingWater(paused,504,496,ReservationStatus.Reserved);
                Require(Crop(run).Tasks.Last().Progress==default&&!paused.Work.WorkerIntervals.Any(x=>x.JobId==task.Id)
                    &&Crop(run).CareUntil==originalCare,"Zero-work pause retained labor or renewed care.");
                string path=Path.Combine(directory,"assigned-tending-zero-progress.ddsave");
                var store=new FileSaveStore();store.Save(path,paused);
                var restored=new Simulation(policy,store.Load(path),ExecutionProfile.Laboratory);
                Require(Bytes(run).SequenceEqual(Bytes(restored)),"Paused tending changed on disk restore.");
                Throws<ArgumentException>(()=>new Simulation(new TestOnlySharedWorldPolicy(new SharedCombatFixture())
                    .EnableCampGreensAssignments(),store.Load(path),ExecutionProfile.Laboratory));
                foreach(var branch in new[]{run,restored}) {
                    WorldCommit(branch,IC(branch,CommandKind.TendCrop,CropId,actor:worker));
                    AssertTendingWater(branch.Capture(),504,496,ReservationStatus.Reserved);
                    WorldAdvance(branch,1,2);
                    AssertTendingWater(branch.Capture(),496,496,ReservationStatus.Consumed);
                    Require(Crop(branch).Tasks.Last().Id==task.Id&&Crop(branch).Tasks.Last().Progress==T(1,2)
                        &&Crop(branch).CareUntil==originalCare,"Fractional first work lost identity or renewed care.");
                    WorldAdvance(branch,1799,2);
                    Require(Crop(branch).CareUntil==originalCare.Value.AddSeconds(86400),"Completion did not renew care at its endpoint.");
                    for(int day=0;day<5;day++) {
                        WorldAdvance(branch,85500);
                        WorldCommit(branch,AssignCampGreens(branch,ExpeditionWorkProcedure.CropTending));
                        WorldAdvance(branch,900);
                    }
                    WorldAdvance(branch,86400);
                    WorldCommit(branch,AssignCampGreens(branch,ExpeditionWorkProcedure.CropHarvesting));
                    WorldAdvance(branch,3600);
                    var food=branch.Capture().CropFood.Single();
                    Require(Crop(branch).Stage==CropStage.Harvested&&IL(branch,food.LotId).Quantity==8,"The assigned harvest did not settle eight pounds once.");
                    string carried=HandleI(branch,food.LotId,Q(8),HandlingKind.Pickup,worker);
                    string serving=Portion(branch,Q(2,3),carried,worker);
                    foreach(var step in new[]{(0,1),(0,1),(1,0),(0,1),(1,0)}) {
                        WorldStep(branch,step.Item1,step.Item2);
                        WorldAdvance(branch,1);
                    }
                    string handed=HandleI(branch,serving,Q(2,3),HandlingKind.Handover,worker,TestOnlyPolicy.ActorId);
                    Eat(branch,Q(2,3),handed);
                    WorldAdvance(branch,600);
                    Require(Eaten(branch)==Q(2,3)&&OrdinaryInventory.EdibleFood(branch.Capture())==Q(28,3)
                        &&branch.Capture().InventoryLots.Single(x=>x.LotId==handed).FreshUntil==food.FreshUntil,
                        "The existing meal path lost yield, ownership lineage or freshness.");
                }
                Require(Bytes(run).SequenceEqual(Bytes(restored)),"Identical tending-to-meal commands diverged after restore.");
                store.Save(Path.Combine(directory,"assigned-tending-meal.ddsave"),restored.Capture());
            });

            cases.Add("mgt08_tending_inventory_clock_debits_once_across_post_debit_restore",()=>{
                var policy=FirstWorkWorld();
                var run=World(policy);
                WorldCommit(run,AssignCampGreens(run,ExpeditionWorkProcedure.CropPlanting));
                WorldAdvance(run,3600);
                WorldCommit(run,IC(run,CommandKind.TendCrop,CropId,actor:worker));
                AssertTendingWater(run.Capture(),504,496,ReservationStatus.Reserved);
                HandleI(run,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                AssertTendingWater(run.Capture(),496,496,ReservationStatus.Consumed);
                Require(Crop(run).Tasks.Last().Progress==T(1),"Inventory handling did not credit the first active second.");
                var path=Path.Combine(directory,"tending-after-inventory-debit.ddsave");
                var store=new FileSaveStore();store.Save(path,run.Capture());
                run=new Simulation(policy,store.Load(path),ExecutionProfile.Laboratory);
                for(int n=0;n<2;n++) {
                    WorldCommit(run,IC(run,CommandKind.PauseCrop,CropId,actor:worker));
                    WorldAdvance(run,3);
                    WorldCommit(run,IC(run,CommandKind.TendCrop,CropId,actor:worker));
                    WorldAdvance(run,1);
                    AssertTendingWater(run.Capture(),496,496,ReservationStatus.Consumed);
                }
            });

            cases.Add("mgt08_tending_terminal_release_and_positive_debit_survive_neglect",()=>{
                var policy=new TestOnlyCropPolicy(firstWorkTending:true);
                foreach(bool worked in new[]{false,true}) {
                    var run=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                    Planted(run);
                    FarmWork(run,CommandKind.TendCrop);
                    if(worked)FarmUntil(run,T(7201,2));
                    FarmWork(run,CommandKind.PauseCrop);
                    FarmUntil(run,Crop(run).CareUntil.Value.AddSeconds(CampGreens.WindowSeconds));
                    Require(Crop(run).Stage==CropStage.Failed&&Crop(run).Tasks.Last().Status==CropWorkStatus.Cancelled,
                        "Ordinary neglect did not terminate the paused work.");
                    AssertTendingWater(run.Capture(),worked?496:504,worked?496:504,
                        worked?ReservationStatus.Consumed:ReservationStatus.Released);
                }
                var endpoint=new Simulation(policy,policy.Initial(),ExecutionProfile.Laboratory);
                Planted(endpoint);
                var failure=Crop(endpoint).CareUntil.Value.AddSeconds(CampGreens.WindowSeconds);
                FarmUntil(endpoint,FarmDifference(failure,T(1,2)));
                FarmWork(endpoint,CommandKind.TendCrop);
                FarmUntil(endpoint,failure);
                Require(Crop(endpoint).Stage==CropStage.Failed&&Crop(endpoint).Tasks.Last().Progress==T(1,2),
                    "The neglect endpoint did not retain the positive labor immediately before failure.");
                AssertTendingWater(endpoint.Capture(),496,496,ReservationStatus.Consumed);
            });

            cases.Add("mgt08_tending_legacy_and_first_work_fingerprints_and_invalid_claims",()=>{
                var legacy=Farm();
                Planted(legacy);FarmWork(legacy,CommandKind.TendCrop);
                AssertTendingWater(legacy.Capture(),496,496,ReservationStatus.Consumed);
                Require(Crop(legacy).Tasks.Last().Progress==default,"Legacy admission was no longer the debit boundary.");
                var policy=new TestOnlyCropPolicy(workerIds:new[]{TestOnlyPolicy.ActorId,worker},firstWorkTending:true);
                var initial=policy.Initial();
                var other=initial.Actors.Single(x=>x.Id==TestOnlyPolicy.ActorId);other.X=2;other.Y=3;
                var run=new Simulation(policy,initial,ExecutionProfile.Laboratory);
                Planted(run);FarmWork(run,CommandKind.TendCrop);
                AssertTendingWater(run.Capture(),504,496,ReservationStatus.Reserved);
                Throws<ArgumentException>(()=>new Simulation(policy,codec.Decode(Bytes(legacy)),ExecutionProfile.Laboratory));
                void RejectClaim(Snapshot bad,ResourceReservation replacement) {
                    var claim=TendingClaim(bad);
                    bad.Work=new WorkLedger(bad.Work.Lots,bad.Work.WorkerIntervals,
                        bad.Work.Reservations.Where(x=>x.Id!=claim.Id).Concat(replacement==null
                            ?Array.Empty<ResourceReservation>():new[]{replacement}));
                    Throws<ArgumentException>(()=>new Simulation(policy,bad,ExecutionProfile.Laboratory));
                }
                var state=run.Capture();var claim=TendingClaim(state);
                RejectClaim(run.Capture(),null);
                RejectClaim(run.Capture(),new ResourceReservation(claim.Id,claim.JobId,claim.LotId,8,ReservationStatus.Released));
                RejectClaim(run.Capture(),new ResourceReservation(claim.Id,"TEST_ONLY.unrelated",claim.LotId,8));
                FarmWork(run,CommandKind.PauseCrop);
                RejectUnchanged(run,TestOnlyCropPolicy.Host(),FarmCommand(run,CommandKind.TendCrop,actor:TestOnlyPolicy.ActorId),"PolicyFailure");
                FarmWork(run,CommandKind.TendCrop);
                FarmAdvance(run,1);
                var positive=run.Capture();
                positive.Work=new WorkLedger(state.Work.Lots,positive.Work.WorkerIntervals,positive.Work.Reservations);
                RejectClaim(positive,claim);
            });

            cases.Add("mgt08_tending_composed_inventory_and_filling_preserve_explicit_profile",()=>{
                var crop=new TestOnlyCropPolicy(firstWorkTending:true);
                var inventory=new TestOnlyInventoryPolicy(cropPolicy:crop);
                var filling=new TestOnlyFillingPolicy(cropPolicy:crop,movableVessels:true);
                var composed=new[]{(policy:(ICommandPolicy)inventory,initial:inventory.Initial()),
                    (policy:(ICommandPolicy)filling,initial:filling.Initial())};
                foreach(var (policy,initial) in composed) {
                    var run=new Simulation(policy,initial,ExecutionProfile.Laboratory);
                    CommitI(run,IC(run,CommandKind.PlantCrop,CropId,actor:worker));AdvanceI(run,3600);
                    CommitI(run,IC(run,CommandKind.TendCrop,CropId,actor:worker));
                    AssertTendingWater(run.Capture(),504,496,ReservationStatus.Reserved);
                    run=new Simulation(policy,codec.Decode(Bytes(run)),ExecutionProfile.Laboratory);
                    AdvanceI(run,1,2);
                    AssertTendingWater(run.Capture(),496,496,ReservationStatus.Consumed);
                }
            });
        }

        private static void AddCropCases(Dictionary<string,Action> cases,string directory)
        {
            AddFirstWorkTendingCases(cases,directory);
            var host=TestOnlyCropPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("crop_start_commits_inputs_once_without_growth_or_yield",()=>{
                var s=Farm();var command=FarmCommand(s,CommandKind.PlantCrop);FarmCommit(s,command);var v=s.Capture();
                Require(v.Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.SeedLotId).Quantity==7
                    &&v.Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.WaterLotId).Quantity==504&&v.Work.Reservations.All(r=>r.Status==ReservationStatus.Consumed)
                    &&Crop(s).Stage==CropStage.Planting&&Crop(s).Growth==T(0)&&CampGreens.EdibleFood(v)==0&&v.RuleClock==T(0),"Planting input/time boundary.");
                var bytes=Bytes(s);Require(s.Execute(host,command).Outcome==Outcome.Duplicate&&bytes.SequenceEqual(Bytes(s)),"Repeated planting spent again."); });
            cases.Add("crop_missing_inputs_rejects_every_partial_change",()=>{
                foreach(var pair in new[]{(seed:0L,water:512L),(seed:1L,water:7L)}) {
                    var s=Farm(pair.seed,pair.water);RejectUnchanged(s,host,FarmCommand(s,CommandKind.PlantCrop),"PolicyFailure");
                } });
            cases.Add("crop_worker_location_authority_and_busy_guards",()=>{
                var s=Farm();RejectUnchanged(s,new Authority("guest",new[]{TestOnlyPolicy.ActorId}),FarmCommand(s,CommandKind.PlantCrop),"NotAuthorized");
                FarmWork(s,CommandKind.PlantCrop);
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.Move,"",x:-1),"WorkerBusy");
                FarmCommit(s,FarmCommand(s,CommandKind.Interact,TestOnlyPolicy.ContainerId,actor:TestOnlyPolicy.ActorId));
                Require(s.Capture().Objects[0].Opened&&Crop(s).Tasks[0].Progress==T(0),"Other actor's world interaction changed labor.");
                FarmWork(s,CommandKind.PauseCrop);
                FarmCommit(s,FarmCommand(s,CommandKind.Move,"",x:-1));FarmCommit(s,FarmCommand(s,CommandKind.Move,"",x:-1));
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.PlantCrop),"InvalidCropWorkAccess"); });
            cases.Add("crop_planting_interruption_retains_progress_and_spent_inputs",()=>{
                var s=Farm();FarmWork(s,CommandKind.PlantCrop);FarmUntil(s,T(1800));FarmWork(s,CommandKind.PauseCrop);FarmAdvance(s,3600);
                Require(Crop(s).Tasks[0].Progress==T(1800)&&Crop(s).Growth==T(0),"Paused planting progressed.");
                FarmWork(s,CommandKind.PlantCrop);FarmAdvance(s,1800);var crop=Crop(s);
                Require(crop.Stage==CropStage.Growing&&crop.CareUntil==T(93600)&&crop.Tasks[0].StartedAt==T(0)
                    &&s.Capture().Work.Reservations.Count==2&&s.Capture().Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.SeedLotId).Quantity==7,"Resume repaid or reset planting."); });
            cases.Add("crop_zero_progress_pause_cannot_be_reassigned",()=>{
                var s=MultiworkerFarm();FarmWork(s,CommandKind.PlantCrop);FarmWork(s,CommandKind.PauseCrop);
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.PlantCrop,actor:TestOnlyPolicy.ActorId),"PolicyFailure");
                var task=Crop(s).Tasks.Single();Require(task.Status==CropWorkStatus.Paused&&task.Progress==T(0)
                    &&task.WorkerId==TestOnlyPolicy.CompanionId&&s.Capture().Work.WorkerIntervals.Count==0,"Zero-progress reassignment changed the paused worker or booking."); });
            cases.Add("crop_positive_progress_pause_rejects_reassignment_and_allows_original_worker_resume",()=>{
                var s=MultiworkerFarm();FarmWork(s,CommandKind.PlantCrop);FarmAdvance(s,1);FarmWork(s,CommandKind.PauseCrop);
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.PlantCrop,actor:TestOnlyPolicy.ActorId),"PolicyFailure");
                var paused=Crop(s).Tasks.Single();Require(paused.Status==CropWorkStatus.Paused&&paused.Progress==T(1)
                    &&paused.WorkerId==TestOnlyPolicy.CompanionId,"Positive-progress rejection changed the paused task.");
                FarmWork(s,CommandKind.PlantCrop);FarmAdvance(s,3599);var v=s.Capture();var completed=Crop(s).Tasks.Single();
                Require(Crop(s).Stage==CropStage.Growing&&completed.Status==CropWorkStatus.Complete&&completed.WorkerId==TestOnlyPolicy.CompanionId
                    &&v.Work.WorkerIntervals.All(w=>w.WorkerId==TestOnlyPolicy.CompanionId)&&v.Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.SeedLotId).Quantity==7,
                    "Original worker resume lost progress, provenance or spent input.");
                var bytes=Bytes(s);var restoredPolicy=new TestOnlyCropPolicy(workerIds:new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId});
                var restored=new Simulation(restoredPolicy,codec.Decode(bytes),ExecutionProfile.Laboratory);
                Require(Bytes(restored).SequenceEqual(bytes),"Same-worker crop resume did not survive save/restore."); });
            cases.Add("crop_first_hour_is_active_growth_begins_after_completion",()=>{
                var s=Farm();FarmWork(s,CommandKind.PlantCrop);FarmUntil(s,T(10799,3));
                Require(Crop(s).Stage==CropStage.Planting&&Crop(s).Growth==T(0),"Rounded incomplete planting upward.");
                FarmUntil(s,T(3600));Require(Crop(s).Stage==CropStage.Growing&&Crop(s).CareUntil==T(90000),"Initial care origin.");
                FarmUntil(s,T(3601));Require(Crop(s).Growth==T(1),"Growth counted planting time."); });
            cases.Add("crop_large_advance_stops_at_first_milestone",()=>{
                var s=Farm();FarmWork(s,CommandKind.PlantCrop);
                FarmCommit(s,FarmCommand(s,CommandKind.AdvanceClock,"",604800,1,TestOnlyPolicy.ActorId));
                Require(s.Capture().RuleClock==T(3600)&&Crop(s).Stage==CropStage.Growing,"Skipped planting endpoint.");
                FarmCommit(s,FarmCommand(s,CommandKind.AdvanceClock,"",604800,1,TestOnlyPolicy.ActorId));
                Require(s.Capture().RuleClock==T(90000)&&Crop(s).UnsuitableSince==T(90000),"Skipped care endpoint."); });
            cases.Add("crop_passive_growth_does_not_reserve_worker",()=>{
                var s=Farm();Planted(s);var v=s.Capture();
                Require(v.Work.WorkerIntervals.All(w=>w.End<=v.RuleClock),"Passive growth holds active worker.");
                FarmCommit(s,FarmCommand(s,CommandKind.Move,"",x:-1));FarmAdvance(s,3600);
                Require(Crop(s).Growth==T(3600),"Independent worker movement stopped suitable passive growth."); });
            cases.Add("crop_tending_water_at_start_and_care_only_on_completion",()=>{
                var s=Farm();Planted(s);var initialCare=Crop(s).CareUntil;
                FarmWork(s,CommandKind.TendCrop);FarmAdvance(s,899);
                Require(Crop(s).CareUntil==initialCare&&s.Capture().Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.WaterLotId).Quantity==496,"Care or water commitment timing.");
                FarmAdvance(s,1);Require(Crop(s).CareUntil==T(90900),"Early tending banked another full day on previous deadline."); });
            cases.Add("crop_tending_pause_resume_never_rebuys_water",()=>{
                var s=Farm();Planted(s);FarmWork(s,CommandKind.TendCrop);FarmAdvance(s,450);FarmWork(s,CommandKind.PauseCrop);
                FarmAdvance(s,100);FarmWork(s,CommandKind.TendCrop);FarmAdvance(s,450);
                Require(Crop(s).Tasks.Count==2&&Crop(s).Tasks[1].Progress==T(900)&&Crop(s).CareUntil==T(91000)
                    &&s.Capture().Work.Reservations.Count==3,"Tending resume reset progress or inputs."); });
            cases.Add("crop_care_expiry_pauses_growth_and_completion_resumes_retained_growth",()=>{
                var s=Farm();Planted(s);FarmUntil(s,T(93600));
                Require(Crop(s).Growth==T(86400)&&Crop(s).UnsuitableSince==T(90000),"Neglected interval counted as growth.");
                FarmWork(s,CommandKind.TendCrop);FarmAdvance(s,900);
                Require(Crop(s).Growth==T(86400)&&!Crop(s).UnsuitableSince.HasValue,"Tending interval counted growth without care.");
                FarmAdvance(s,3600);Require(Crop(s).Growth==T(90000),"Retained growth did not resume."); });
            cases.Add("crop_unsuitable_conditions_pause_growth_without_restarting_care",()=>{
                var s=Farm();Planted(s);FarmAdvance(s,3600);FarmConditions(s,false);FarmAdvance(s,3600);FarmConditions(s,true);
                Require(Crop(s).Growth==T(3600)&&Crop(s).CareUntil==T(90000)&&!Crop(s).UnsuitableSince.HasValue,"Condition recovery reset earned growth or care.");
                FarmAdvance(s,3600);Require(Crop(s).Growth==T(7200),"Growth did not resume."); });
            cases.Add("crop_condition_changes_require_separate_host_authority",()=>{
                var s=Farm();var c=FarmCommand(s,CommandKind.SetCropConditions,TestOnlyCropPolicy.PlotId,0,actor:TestOnlyPolicy.ActorId);
                RejectUnchanged(s,new Authority("guest",new[]{TestOnlyPolicy.ActorId},true),c,"NotAuthorized");
                FarmCommit(s,c);Require(!s.Capture().CropPlots[0].Suitable,"Plot condition not changed.");
                RejectUnchanged(s,new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},true),c,"NotAuthorized");
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.PlantCrop),"PolicyFailure"); });
            cases.Add("crop_failure_at_48_continuous_hours_has_no_refund_or_yield",()=>{
                var s=Farm();Planted(s);FarmConditions(s,false);FarmUntil(s,T(176400));
                Require(Crop(s).Stage==CropStage.Failed&&Crop(s).ClosedAt==T(176400)&&CampGreens.EdibleFood(s.Capture())==0
                    &&s.Capture().Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.SeedLotId).Quantity==7,"Failure boundary or refund.");
                FarmConditions(s,true);Require(Crop(s).Stage==CropStage.Failed,"Recovery at failure resurrected crop."); });
            cases.Add("crop_tending_completing_at_failure_deadline_loses",()=>{
                var s=Farm();Planted(s);FarmUntil(s,T(261900));FarmWork(s,CommandKind.TendCrop);FarmUntil(s,T(262800));
                var crop=Crop(s);Require(crop.Stage==CropStage.Failed&&crop.Tasks[1].Progress==T(900)
                    &&crop.Tasks[1].Status==CropWorkStatus.Cancelled&&s.Capture().CropFood.Length==0,"Exact-deadline care beat failure."); });
            cases.Add("crop_recovery_strictly_before_failure_preserves_batch",()=>{
                var s=Farm();Planted(s);FarmUntil(s,T(261899));FarmWork(s,CommandKind.TendCrop);FarmUntil(s,T(262799));
                Require(Crop(s).Stage==CropStage.Growing&&!Crop(s).UnsuitableSince.HasValue,"Timely care failed.");
                FarmAdvance(s,1);Require(Crop(s).Stage==CropStage.Growing&&Crop(s).Growth==T(86401),"Old failure deadline remained active."); });
            cases.Add("crop_conditions_alone_cannot_reset_missing_care_failure",()=>{
                var s=Farm();Planted(s);FarmUntil(s,T(100000));FarmConditions(s,false);FarmConditions(s,true);
                Require(Crop(s).UnsuitableSince==T(90000),"Toggle erased continuous unmet care.");FarmUntil(s,T(262800));
                Require(Crop(s).Stage==CropStage.Failed,"Condition toggle extended neglected crop."); });
            cases.Add("crop_seven_growth_days_mature_at_care_expiry",()=>{
                var s=Farm();Mature(s);var crop=Crop(s);
                Require(crop.Growth==T(604800)&&crop.MaturedAt==T(608400)&&crop.CareUntil==T(608400)
                    &&!crop.UnsuitableSince.HasValue&&crop.Tasks.Count==7,"Maturity at exact care expiry.");
                FarmConditions(s,false);FarmAdvance(s,86400);
                Require(Crop(s).Stage==CropStage.Mature,"Mature crop still required daily growth care."); });
            cases.Add("crop_maturity_cancels_unfinished_tending_without_refund",()=>{
                var s=Farm();Planted(s);
                for(int day=0;day<6;day++){var expiry=Crop(s).CareUntil.Value;FarmUntil(s,FarmDifference(expiry,T(900)));FarmWork(s,CommandKind.TendCrop);FarmUntil(s,expiry);}
                FarmUntil(s,T(608000));FarmWork(s,CommandKind.TendCrop);FarmUntil(s,T(608400));
                var crop=Crop(s);Require(crop.Stage==CropStage.Mature&&crop.Tasks.Last().Status==CropWorkStatus.Cancelled&&crop.Tasks.Last().Progress==T(400)
                    &&s.Capture().Work.WorkerIntervals.All(w=>w.End<=T(608400))
                    &&s.Capture().Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.WaterLotId).Quantity==448,"Maturity lost spent work/input or held worker."); });
            cases.Add("crop_complete_harvest_once_at_plot_without_seeds_or_supply",()=>{
                var s=Farm();Mature(s);var harvest=FarmCommand(s,CommandKind.HarvestCrop);FarmCommit(s,harvest);FarmAdvance(s,3600);
                var v=s.Capture();Require(Crop(s).Stage==CropStage.Harvested&&CampGreens.EdibleFood(v)==8&&v.CropFood.Length==1
                    &&v.Work.Lots.Single(l=>l.Id==v.CropFood[0].LotId).LocationId==TestOnlyCropPolicy.PlotId
                    &&v.Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.SeedLotId).Quantity==7,"Harvest amount/location or automatic seeds.");
                var before=Bytes(s);Require(s.Execute(host,harvest).Outcome==Outcome.Duplicate&&before.SequenceEqual(Bytes(s)),"Start-harvest replay changed output.");
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.HarvestCrop),"PolicyFailure"); });
            cases.Add("crop_partial_harvest_is_labor_not_inventory",()=>{
                var s=Farm();Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,1800);FarmWork(s,CommandKind.PauseCrop);
                Require(Crop(s).Tasks.Last().Progress==T(1800)&&s.Capture().CropFood.Length==0&&CampGreens.EdibleFood(s.Capture())==0,"Partial harvest granted proportional food."); });
            cases.Add("crop_interrupted_harvest_retains_first_freshness_origin",()=>{
                var s=Farm();Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,1800);FarmWork(s,CommandKind.PauseCrop);
                FarmAdvance(s,3600);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,1800);
                Require(Crop(s).Stage==CropStage.Harvested&&s.Capture().CropFood[0].FreshUntil==T(781200),"Resume renewed first-harvest freshness."); });
            cases.Add("crop_harvest_exact_deadline_is_timely_but_expired_food_not_edible",()=>{
                var s=Farm();Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,1800);FarmWork(s,CommandKind.PauseCrop);
                FarmUntil(s,T(779400));FarmWork(s,CommandKind.HarvestCrop);FarmUntil(s,T(781200));var v=s.Capture();
                Require(Crop(s).Stage==CropStage.Harvested&&v.CropFood.Length==1&&v.CropFood[0].Expired&&CampGreens.EdibleFood(v)==0
                    &&v.Work.Lots.Single(l=>l.Id==v.CropFood[0].LotId).Quantity==8,"Exact harvest/freshness boundary lost physical outcome or granted edible food."); });
            cases.Add("crop_incomplete_harvest_at_deadline_fails_without_food",()=>{
                var s=Farm();Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,1800);FarmWork(s,CommandKind.PauseCrop);FarmUntil(s,T(781200));
                Require(Crop(s).Stage==CropStage.Failed&&Crop(s).Tasks.Last().Status==CropWorkStatus.Cancelled&&s.Capture().CropFood.Length==0,"Late partial harvest paid out."); });
            cases.Add("crop_food_expiry_is_exact_and_does_not_delete_physical_lot",()=>{
                var s=Farm();Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,3600);FarmUntil(s,T(781199));
                Require(CampGreens.EdibleFood(s.Capture())==8,"Food expired early.");FarmAdvance(s,1);
                Require(CampGreens.EdibleFood(s.Capture())==0&&s.Capture().CropFood[0].Expired
                    &&s.Capture().Work.Lots.Single(l=>l.Id==s.Capture().CropFood[0].LotId).Quantity==8,"Freshness endpoint rounded or deleted physical stock."); });
            cases.Add("crop_replant_failed_plot_preserves_history_and_requires_new_inputs",()=>{
                var s=Farm();Planted(s);FarmUntil(s,T(262800));RejectUnchanged(s,host,FarmCommand(s,CommandKind.PlantCrop),"PolicyFailure");
                FarmWork(s,CommandKind.PlantCrop,"TEST_ONLY.next-crop");FarmAdvance(s,3600);
                Require(s.Capture().Crops.Length==2&&Crop(s).Stage==CropStage.Failed&&Crop(s,"TEST_ONLY.next-crop").Stage==CropStage.Growing
                    &&s.Capture().Work.Lots.Single(l=>l.Id==TestOnlyCropPolicy.SeedLotId).Quantity==6,"Replant cleared history or refunded input."); });
            cases.Add("crop_replant_cannot_reset_unsuitable_plot",()=>{
                var s=Farm();Planted(s);FarmConditions(s,false);FarmUntil(s,T(176400));
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.PlantCrop,"TEST_ONLY.next-crop"),"PolicyFailure");
                Require(!s.Capture().CropPlots[0].Suitable,"New batch silently reset season/conditions."); });
            cases.Add("crop_new_batch_does_not_reset_or_delete_prior_food",()=>{
                var s=Farm();Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,3600);var output=s.Capture().CropFood[0];
                FarmWork(s,CommandKind.PlantCrop,"TEST_ONLY.next-crop");FarmAdvance(s,3600);var v=s.Capture();
                Require(v.CropFood.Length==1&&v.CropFood[0].LotId==output.LotId&&v.CropFood[0].FreshUntil==output.FreshUntil
                    &&CampGreens.EdibleFood(v)==8,"Plot reuse reset previous output."); });
            cases.Add("crop_restore_partial_work_continues_identically_without_offline_credit",()=>{
                var s=Farm();FarmWork(s,CommandKind.PlantCrop);FarmUntil(s,T(100,3));var loaded=RestoreFarm(s);
                Require(Bytes(s).SequenceEqual(Bytes(loaded))&&loaded.Capture().RuleClock==T(100,3),"Restore changed fractional time or state.");
                FarmUntil(s,T(3600));FarmUntil(loaded,T(3600));Require(Bytes(s).SequenceEqual(Bytes(loaded)),"Planting continuation diverged."); });
            cases.Add("crop_restore_growing_mature_and_harvested_states",()=>{
                var s=Farm();Planted(s);Require(Bytes(s).SequenceEqual(Bytes(RestoreFarm(s))),"Growing restore.");
                var mature=Farm();Mature(mature);Require(Bytes(mature).SequenceEqual(Bytes(RestoreFarm(mature))),"Mature restore.");
                FarmWork(mature,CommandKind.HarvestCrop);FarmAdvance(mature,3600);var restored=RestoreFarm(mature);
                Require(CampGreens.EdibleFood(restored.Capture())==8&&Bytes(restored).SequenceEqual(Bytes(mature)),"Harvested output restore."); });
            cases.Add("crop_work_receipt_replay_after_disk_restore",()=>{
                var s=Farm();var start=FarmCommand(s,CommandKind.PlantCrop);FarmCommit(s,start);FarmAdvance(s,30);
                var store=new FileSaveStore();string path=Path.Combine(directory,"crop.ddsave");store.Save(path,s.Capture());
                var restored=new Simulation(new TestOnlyCropPolicy(),store.Load(path),ExecutionProfile.Laboratory);var before=Bytes(restored);
                Require(restored.Execute(host,start).Outcome==Outcome.Duplicate&&before.SequenceEqual(Bytes(restored)),"Disk restore repeated input commitment."); });
            cases.Add("crop_failed_disk_commit_preserves_progress_inputs_and_receipts",()=>{
                var s=Farm();var store=new FileSaveStore();string path=Path.Combine(directory,"failed-crop.ddsave");
                store.Save(path,s.Capture());FarmWork(s,CommandKind.PlantCrop);store.Save(path,s.Capture());var before=File.ReadAllBytes(path);var backup=File.ReadAllBytes(path+".bak");
                FarmAdvance(s,3600);Throws<IOException>(()=>new FileSaveStore(new FailingCommit()).Save(path,s.Capture()));
                Require(before.SequenceEqual(File.ReadAllBytes(path))&&backup.SequenceEqual(File.ReadAllBytes(path+".bak"))
                    &&store.Load(path).Crops[0].Stage==CropStage.Planting,"Failed crop write separated state."); });
            cases.Add("crop_schema_guards_release_and_hidden_records",()=>{
                var p=new TestOnlyCropPolicy();Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                var hidden=p.Initial();hidden.SchemaVersion=2;Throws<ArgumentException>(()=>codec.Encode(hidden));
                var legacy=new TestOnlyPolicy().Initial();legacy.CropPlots=p.Initial().CropPlots;Throws<ArgumentException>(()=>codec.Encode(legacy));
                var unknown=p.Initial();unknown.CropPlots=new[]{new CropPlotRecord("unknown",TestOnlyPolicy.CompanionId,true)};
                Throws<ArgumentException>(()=>new Simulation(p,unknown,ExecutionProfile.Laboratory)); });
            cases.Add("crop_codec_corruption_future_schema_and_truncation_reject",()=>{
                var s=Farm();Planted(s);var original=Bytes(s);var bad=(byte[])original.Clone();bad[bad.Length-40]^=1;Throws<InvalidDataException>(()=>codec.Decode(bad));
                bad=(byte[])original.Clone();bad[4]=12;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));
                Throws<InvalidDataException>(()=>codec.Decode(original.Take(original.Length-1).ToArray()));
                bad=new byte[original.Length+1];Buffer.BlockCopy(original,0,bad,0,original.Length-32);Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad)); });
            cases.Add("crop_read_view_cannot_mutate_plot_task_or_food_state",()=>{
                var s=Farm();FarmWork(s,CommandKind.PlantCrop);var before=Bytes(s);var v=s.Capture();
                v.CropPlots[0]=new CropPlotRecord(TestOnlyCropPolicy.PlotId,TestOnlyPolicy.CompanionId,false);v.Crops=Array.Empty<CropBatchRecord>();
                Require(before.SequenceEqual(Bytes(s)),"Read view retained authoritative arrays.");
                Throws<NotSupportedException>(()=>((IList<CropWorkRecord>)Crop(s).Tasks).Clear());
                Throws<NotSupportedException>(()=>((IList<string>)Crop(s).Tasks[0].InputReservations).Clear()); });
            cases.Add("crop_restore_rejects_wrong_historical_worker_or_labor_time",()=>{
                foreach(string invalid in new[]{"worker","after-end","before-start"}) {
                    var s=Farm();if(invalid=="before-start")FarmAdvance(s,3600);Planted(s);FarmAdvance(s,3600);var v=s.Capture();var original=v.Work.WorkerIntervals.Single();
                    var forged=new WorkerInterval(original.Id,original.JobId,invalid=="worker"?TestOnlyPolicy.ActorId:original.WorkerId,
                        invalid=="after-end"?T(3600):T(0),invalid=="after-end"?T(7200):T(3600));
                    v.Work=new WorkLedger(v.Work.Lots,new[]{forged},v.Work.Reservations);
                    Throws<ArgumentException>(()=>new Simulation(new TestOnlyCropPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                } });
            cases.Add("crop_schema2_frozen_golden_still_roundtrips_unchanged",()=>{
                byte[] old=Convert.FromBase64String("RERGMQIAAAAZAAAAVEVTVF9PTkxZLndvcmstc2Vzc2lvbi12MQ0AAAB4b3JzaGlmdDMyLXYxAQAAAAAAAAAAAAAAAAAAAAABAAAAAgAAAA8AAABURVNUX09OTFkuYWN0b3IBAAAAAQAAAAAAAAATAAAAVEVTVF9PTkxZLmNvbXBhbmlvbgMAAAADAAAAAAAAAAEAAAATAAAAVEVTVF9PTkxZLmNvbnRhaW5lcgEAAAACAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAHAAAAHhvcnNoaWZ0MzItbm9uemVyby1yZWplY3QtdjGOAAAARFdMMQEAAAABAAAAEgAAAFRFU1RfT05MWS5tYXRlcmlhbA4AAABURVNUX09OTFkudW5pdAoAAAAAAAAADwAAAFRFU1RfT05MWS5zdG9yZRMAAABURVNUX09OTFkuY29tcGFuaW9uAAAAAAAAAACGEf7YBmg+6MrjL5zLGHlZtkIG7pa//1cCHBB3LOLqSEQly2NnouOaj4zLo2oQXD3EfkS7uJaLXL7e3nVwG2Ww");
                var restored=codec.Decode(old);Require(restored.SchemaVersion==2&&restored.CropPlots.Length==0&&restored.Crops.Length==0&&restored.CropFood.Length==0
                    &&old.SequenceEqual(codec.Encode(restored))&&old.SequenceEqual(Bytes(WorkSession())),"Schema2 was implicitly migrated or changed."); });
            cases.Add("crop_unreachable_deadline_overflow_does_not_block_earlier_time",()=>{
                var p=new TestOnlyCropPolicy();var initial=p.Initial();initial.RuleClock=T(long.MaxValue-103600);
                var s=new Simulation(p,initial,ExecutionProfile.Laboratory);Planted(s);FarmAdvance(s,100);
                Require(Crop(s).Growth==T(100),"Unreachable maturity blocked a representable advance.");
                FarmCommit(s,FarmCommand(s,CommandKind.AdvanceClock,"",int.MaxValue,1,TestOnlyPolicy.ActorId));
                Require(s.Capture().RuleClock==T(long.MaxValue-13600)&&Crop(s).UnsuitableSince==s.Capture().RuleClock,"Huge requested time did not stop at care expiry.");
                FarmAdvance(s,100);Require(Crop(s).Growth==T(86400),"Unreachable neglect deadline blocked valid time or credited growth.");
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.AdvanceClock,"",int.MaxValue,1,TestOnlyPolicy.ActorId),"PolicyFailure"); });
            cases.Add("crop_unrepresentable_stored_care_deadline_rolls_back",()=>{
                var p=new TestOnlyCropPolicy();var initial=p.Initial();initial.RuleClock=T(long.MaxValue-4000);
                var s=new Simulation(p,initial,ExecutionProfile.Laboratory);FarmWork(s,CommandKind.PlantCrop);
                RejectUnchanged(s,host,FarmCommand(s,CommandKind.AdvanceClock,"",3600,1,TestOnlyPolicy.ActorId),"PolicyFailure");
                Require(Crop(s).Tasks[0].Progress==T(0)&&Crop(s).Stage==CropStage.Planting,"Failed stored deadline partly committed labor."); });
            cases.Add("crop_chunked_advances_match_same_domain_state",()=>{
                var bulk=Farm();var chunks=Farm();FarmWork(bulk,CommandKind.PlantCrop);FarmWork(chunks,CommandKind.PlantCrop);
                FarmUntil(bulk,T(100000));
                foreach(long endpoint in new long[]{1,1799,3599,3600,6000,89999,90000,99999,100000})FarmUntil(chunks,T(endpoint));
                byte[] Domain(Simulation s){var v=s.Capture();v.Revision=0;v.Receipts=Array.Empty<CommandReceipt>();return codec.Encode(v);}
                Require(Domain(bulk).SequenceEqual(Domain(chunks)),"Command cadence changed labor, growth, stock or failure origin."); });
            cases.Add("crop_valid_checksum_cannot_hide_invalid_fields",()=>{
                var s=Farm();Planted(s);byte[] original=Bytes(s);
                int workLengthAt=FindMapping(original)+System.Text.Encoding.UTF8.GetByteCount(DiceStream.MappingVersion);
                int cropAt=workLengthAt+4+BitConverter.ToInt32(original,workLengthAt);
                int plotBoolAt=cropAt+4+4+TestOnlyCropPolicy.PlotId.Length+4+TestOnlyPolicy.CompanionId.Length;
                int batchAt=plotBoolAt+1+4;
                int stageAt=batchAt+4+CropId.Length+4+TestOnlyCropPolicy.PlotId.Length+4+TestOnlyCropPolicy.SeedLotId.Length+4+TestOnlyPolicy.CompanionId.Length+32;
                foreach(var mutation in new[]{(at:cropAt,value:9),(at:plotBoolAt,value:2),(at:stageAt,value:99)}) {
                    var bad=(byte[])original.Clone();bad[mutation.at]=(byte)mutation.value;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));
                }
                var v=s.Capture();var c=v.Crops[0];v.Crops=new[]{new CropBatchRecord(c.Id,c.PlotId,c.SeedLotId,c.OwnerId,c.CreatedAt,c.UpdatedAt,c.Stage,c.Growth,
                    c.CareUntil.Value.AddSeconds(1),c.UnsuitableSince,c.MaturedAt,c.ClosedAt,c.Tasks)};
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyCropPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("crop_restore_growth_requires_recorded_nonoverlapping_care",()=>{
                foreach(int earlyTends in new[]{0,6}) {
                    var s=Farm();Planted(s);
                    for(int i=0;i<earlyTends;i++){FarmWork(s,CommandKind.TendCrop);FarmAdvance(s,900);}
                    FarmUntil(s,T(608400));var v=s.Capture();var c=v.Crops[0];Require(c.Stage==CropStage.Failed,"Untended crop unexpectedly survived.");
                    v.Crops=new[]{new CropBatchRecord(c.Id,c.PlotId,c.SeedLotId,c.OwnerId,c.CreatedAt,c.UpdatedAt,CropStage.Mature,T(604800),
                        c.CareUntil,null,T(608400),null,c.Tasks)};
                    Throws<ArgumentException>(()=>new Simulation(new TestOnlyCropPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                }
                var young=Farm();Planted(young);FarmAdvance(young,100);var state=young.Capture();var crop=state.Crops[0];
                state.Crops=new[]{new CropBatchRecord(crop.Id,crop.PlotId,crop.SeedLotId,crop.OwnerId,crop.CreatedAt,crop.UpdatedAt,crop.Stage,T(101),
                    crop.CareUntil,crop.UnsuitableSince,crop.MaturedAt,crop.ClosedAt,crop.Tasks)};
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyCropPolicy(),codec.Decode(codec.Encode(state)),ExecutionProfile.Laboratory)); });
            cases.Add("crop_restore_complete_task_must_end_with_its_actual_labor",()=>{
                foreach(var kind in new[]{CropWorkKind.Plant,CropWorkKind.Tend,CropWorkKind.Harvest}) {
                    var s=Farm();if(kind==CropWorkKind.Harvest){Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,3600);}
                    else {Planted(s);if(kind==CropWorkKind.Tend){FarmWork(s,CommandKind.TendCrop);FarmAdvance(s,900);}}
                    FarmAdvance(s,3600);var v=s.Capture();var c=v.Crops[0];var tasks=c.Tasks.ToArray();var task=tasks.Last();
                    tasks[tasks.Length-1]=new CropWorkRecord(task.Id,task.WorkerId,task.Kind,task.Status,task.StartedAt,task.Progress,v.RuleClock,task.InputReservations);
                    v.Crops=new[]{new CropBatchRecord(c.Id,c.PlotId,c.SeedLotId,c.OwnerId,c.CreatedAt,c.UpdatedAt,c.Stage,
                        kind==CropWorkKind.Plant?T(0):c.Growth,kind==CropWorkKind.Harvest?c.CareUntil:v.RuleClock.AddSeconds(86400),
                        c.UnsuitableSince,c.MaturedAt,kind==CropWorkKind.Harvest?v.RuleClock:c.ClosedAt,tasks)};
                    Throws<ArgumentException>(()=>new Simulation(new TestOnlyCropPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                } });
            cases.Add("crop_restore_work_cannot_begin_before_its_phase",()=>{
                foreach(bool harvest in new[]{false,true}) {
                    var s=Farm();if(harvest)Mature(s);else Planted(s);
                    FarmWork(s,harvest?CommandKind.HarvestCrop:CommandKind.TendCrop);var v=s.Capture();var c=v.Crops[0];var tasks=c.Tasks.ToArray();var task=tasks.Last();
                    tasks[tasks.Length-1]=new CropWorkRecord(task.Id,task.WorkerId,task.Kind,task.Status,FarmDifference(task.StartedAt,T(1)),task.Progress,task.EndedAt,task.InputReservations);
                    v.Crops=new[]{new CropBatchRecord(c.Id,c.PlotId,c.SeedLotId,c.OwnerId,c.CreatedAt,c.UpdatedAt,c.Stage,c.Growth,
                        c.CareUntil,c.UnsuitableSince,c.MaturedAt,c.ClosedAt,tasks)};
                    Throws<ArgumentException>(()=>new Simulation(new TestOnlyCropPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                } });
            cases.Add("crop_active_tending_and_harvest_disk_resume_match_continuation",()=>{
                foreach(bool harvest in new[]{false,true}) {
                    var s=Farm();if(harvest)Mature(s);else Planted(s);
                    FarmWork(s,harvest?CommandKind.HarvestCrop:CommandKind.TendCrop);FarmAdvance(s,300);
                    string path=Path.Combine(directory,harvest?"harvest.ddsave":"tending.ddsave");var store=new FileSaveStore();store.Save(path,s.Capture());
                    var restored=new Simulation(new TestOnlyCropPolicy(),store.Load(path),ExecutionProfile.Laboratory);
                    FarmAdvance(s,harvest?3300:600);FarmAdvance(restored,harvest?3300:600);
                    Require(Bytes(s).SequenceEqual(Bytes(restored)),"Active crop work diverged after disk restore.");
                } });
            cases.Add("crop_schema3_maximum_structural_state_fits_save_capacity",()=>{
                // Structural codec capacity, deliberately not a lawful Camp Greens scenario.
                string Id(string prefix,int i)=>(prefix+i.ToString(System.Globalization.CultureInfo.InvariantCulture)).PadRight(96,'x');
                var s=new TestOnlyCropPolicy().Initial();s.ContentFingerprint=new string('f',96);s.RuleClock=T(1000);
                s.Actors=Enumerable.Range(0,64).Select(i=>new ActorState{Id=Id("actor",i)}).ToArray();
                s.Objects=Enumerable.Range(0,64).Select(i=>new ObjectState{Id=Id("object",i)}).ToArray();
                s.Revision=Validation.MaxReceipts;s.Receipts=Enumerable.Range(1,Validation.MaxReceipts).Select(i=>new CommandReceipt{
                    Principal=Id("principal",i),Id=Id("receipt",i),Fingerprint=new string('f',512),Revision=i}).ToArray();
                s.Work=new WorkLedger(Enumerable.Range(0,128).Select(i=>new ResourceLot(Id("lot",i),Id("unit",i),long.MaxValue,Id("place",i),Id("owner",i))),
                    Enumerable.Range(0,128).Select(i=>new WorkerInterval(Id("work",i),Id("task",i),s.Actors[0].Id,T(i),T(i+1))),
                    Enumerable.Range(0,128).Select(i=>new ResourceReservation(Id("claim",i),Id("task",i),Id("lot",i),long.MaxValue,ReservationStatus.Released)));
                s.CropPlots=Enumerable.Range(0,8).Select(i=>new CropPlotRecord(Id("plot",i),Id("owner",i),true)).ToArray();
                s.Crops=Enumerable.Range(0,8).Select(i=>new CropBatchRecord(Id("crop",i),Id("plot",i),Id("lot",i),Id("owner",i),T(0),T(1000),CropStage.Failed,
                    T(10),T(90000),T(500),T(600),T(1000),Enumerable.Range(i*32,32).Select(j=>new CropWorkRecord(Id("task",j),s.Actors[0].Id,CropWorkKind.Tend,
                        CropWorkStatus.Cancelled,T(0),T(1),T(1000),j<128?new[]{Id("claim",j)}:Array.Empty<string>())))).ToArray();
                s.CropFood=Enumerable.Range(0,8).Select(i=>new CropFoodRecord(Id("lot",i),Id("crop",i),T(90000),false)).ToArray();
                var bytes=codec.Encode(s);Require(bytes.Length<=SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximal accepted crop state exceeds save capacity.");
                File.WriteAllText(Path.Combine(directory,"maximal-crop-bytes.txt"),bytes.Length.ToString(System.Globalization.CultureInfo.InvariantCulture));
                s.CropPlots=s.CropPlots.Concat(new[]{new CropPlotRecord("extra",s.Actors[0].Id,true)}).ToArray();Throws<ArgumentException>(()=>codec.Encode(s));
                s.CropPlots=s.CropPlots.Take(8).ToArray();s.Work=new WorkLedger(s.Work.Lots.Concat(new[]{new ResourceLot("extra","unit",0,"place","owner")}),s.Work.WorkerIntervals,s.Work.Reservations);
                Throws<ArgumentException>(()=>codec.Encode(s)); });
        }
    }
}
#endif
