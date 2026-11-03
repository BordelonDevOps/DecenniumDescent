#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static Simulation Filling(int hands=2){var p=new TestOnlyFillingPolicy(companionUsableHands:hands);return new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);}
        private static string StartFill(Simulation s,RuleQuantity amount,string destination=TestOnlyFillingPolicy.CompanionSkinId,
            string source=TestOnlyFillingPolicy.SupplyId,string worker=TestOnlyPolicy.CompanionId)
        {string id="inventory."+(s.Capture().Revision+1)+".fill";CommitI(s,IC(s,CommandKind.StartWaterFill,source,new InventoryRequest(amount,destination),worker));return id;}
        private static void FillCommand(Simulation s,CommandKind kind,string job,string actor=TestOnlyPolicy.CompanionId)=>CommitI(s,IC(s,kind,job,actor:actor));
        private static WaterFillRecord Fill(Simulation s,string id)=>s.Capture().WaterFills.Single(x=>x.Id==id);
        private static Simulation RestoreFilling(Simulation s)=>new Simulation(new TestOnlyFillingPolicy(),new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);
        private static void AddWaterFillingCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlyFillingPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("filling_reserves_real_source_and_destination_without_movement",()=>{
                var s=Filling();string job=StartFill(s,Q(4));var v=s.Capture();
                Require(IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(32)&&v.Work.AvailableAmount(TestOnlyFillingPolicy.SupplyId)==Q(28)
                    &&WaterFilling.Contents(v,TestOnlyFillingPolicy.CompanionSkinId)==Q(0)&&WaterFilling.FreeCapacity(v,TestOnlyFillingPolicy.CompanionSkinId)==Q(0)
                    &&Fill(s,job).Progress==T(0)&&v.RuleClock==T(0)&&v.Work.WorkerIntervals[0].End==T(60),"Starting fill moved liquid or skipped reservations."); });
            cases.Add("filling_small_quantity_still_requires_full_minute",()=>{
                var s=Filling();string job=StartFill(s,Q(1,3));AdvanceI(s,59);Require(Fill(s,job).Progress==T(59)&&IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(32)
                    &&WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.CompanionSkinId)==Q(0),"Partial fill moved liquid early.");
                AdvanceI(s,1);Require(Fill(s,job).Status==WaterFillStatus.Complete&&WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.CompanionSkinId)==Q(1,3),"Partial quantity duration discounted or completion missed."); });
            cases.Add("filling_completion_transfers_once_without_consumption_credit",()=>{
                var s=Filling();string job=StartFill(s,Q(4));var advance=IC(s,CommandKind.AdvanceClock,x:60,y:1);CommitI(s,advance);var v=s.Capture();var done=Fill(s,job);
                Require(IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(28)&&IL(s,done.OutputLotId).Amount==Q(4)&&v.Work.Reservations[0].Status==ReservationStatus.Released
                    &&v.Work.Reservations[0].ConsumedAmount==Q(0)&&OrdinaryInventory.Consumed(v,TestOnlyPolicy.CompanionId,NutritionKind.WaterPints)==Q(0),"Filling consumed or duplicated water.");
                var bytes=Bytes(s);Require(s.Execute(host,advance).Outcome==Outcome.Duplicate&&bytes.SequenceEqual(Bytes(s)),"Repeated completion transferred twice.");
                AdvanceI(s,60);Require(IL(s,done.OutputLotId).Amount==Q(4)&&s.Capture().WaterFills.Length==1,"Elapsed time repeated output."); });
            cases.Add("filling_pause_preserves_progress_and_both_claims_across_reload",()=>{
                var s=Filling();string job=StartFill(s,Q(3,2));AdvanceI(s,25);FillCommand(s,CommandKind.PauseWaterFill,job);s=RestoreFilling(s);AdvanceI(s,1000);
                Require(Fill(s,job).Progress==T(25)&&Fill(s,job).Status==WaterFillStatus.Paused&&WaterFilling.ReservedCapacity(s.Capture(),TestOnlyFillingPolicy.CompanionSkinId)==Q(3,2)
                    &&s.Capture().Work.AvailableAmount(TestOnlyFillingPolicy.SupplyId)==Q(61,2),"Paused fill lost reservations or earned work.");
                FillCommand(s,CommandKind.ResumeWaterFill,job);AdvanceI(s,35);Require(Fill(s,job).Status==WaterFillStatus.Complete&&Fill(s,job).EndedAt==T(1060)
                    &&s.Capture().Work.WorkerIntervals.Count==2&&IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(61,2),"Resume restarted or credited paused time."); });
            cases.Add("filling_cancel_retains_labor_but_moves_no_water",()=>{
                foreach(bool paused in new[]{false,true}) {
                    var s=Filling();string job=StartFill(s,Q(4));AdvanceI(s,30);if(paused)FillCommand(s,CommandKind.PauseWaterFill,job);
                    FillCommand(s,CommandKind.CancelWaterFill,job);AdvanceI(s,100);var v=s.Capture();
                    Require(Fill(s,job).Status==WaterFillStatus.Cancelled&&Fill(s,job).Progress==T(30)&&Fill(s,job).EndedAt==T(30)
                        &&IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(32)&&WaterFilling.FreeCapacity(v,TestOnlyFillingPolicy.CompanionSkinId)==Q(4)
                        &&v.Work.WorkerIntervals.Single().End==T(30)&&v.Work.AvailableAmount(TestOnlyFillingPolicy.SupplyId)==Q(32),"Cancellation moved/refunded water or erased labor.");
                } });
            cases.Add("filling_zero_work_pause_cancel_removes_only_unused_bookings",()=>{
                var s=Filling();string job=StartFill(s,Q(1));FillCommand(s,CommandKind.PauseWaterFill,job);
                Require(s.Capture().Work.WorkerIntervals.Count==0&&Fill(s,job).Progress==T(0),"Instant pause booked historical labor.");
                FillCommand(s,CommandKind.ResumeWaterFill,job);FillCommand(s,CommandKind.CancelWaterFill,job);
                Require(s.Capture().Work.WorkerIntervals.Count==0&&Fill(s,job).Status==WaterFillStatus.Cancelled,"No-work cancel retained future labor."); });
            cases.Add("filling_paused_capacity_cannot_be_double_reserved",()=>{
                var s=Filling();AtCompanion(s);string job=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId);FillCommand(s,CommandKind.PauseWaterFill,job);
                RejectUnchanged(s,host,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(1,100),TestOnlyFillingPolicy.FlaskId)),"FillCapacityUnavailable");
                FillCommand(s,CommandKind.CancelWaterFill,job);StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId,worker:TestOnlyPolicy.ActorId);AdvanceI(s,60);
                Require(WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.FlaskId)==Q(1),"Released capacity was not reusable."); });
            cases.Add("filling_reserved_capacity_coexists_with_other_feasible_fill",()=>{
                var s=Filling();AtCompanion(s);string a=StartFill(s,Q(1,2),TestOnlyFillingPolicy.FlaskId);FillCommand(s,CommandKind.PauseWaterFill,a);
                string b=StartFill(s,Q(1,2),TestOnlyFillingPolicy.FlaskId,worker:TestOnlyPolicy.ActorId);AdvanceI(s,60);
                Require(WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.FlaskId)==Q(1,2)&&WaterFilling.ReservedCapacity(s.Capture(),TestOnlyFillingPolicy.FlaskId)==Q(1,2),"Partial capacity reservation lost.");
                FillCommand(s,CommandKind.ResumeWaterFill,a);AdvanceI(s,60);
                Require(Fill(s,b).Status==WaterFillStatus.Complete&&WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.FlaskId)==Q(1)
                    &&s.Capture().VesselContents.Count(x=>x.VesselId==TestOnlyFillingPolicy.FlaskId)==2,"Separate filling histories were merged or overfilled."); });
            cases.Add("filling_single_opening_cannot_be_worked_by_two_actors_at_once",()=>{
                var s=Filling();AtCompanion(s);StartFill(s,Q(1,2),TestOnlyFillingPolicy.FlaskId);
                RejectUnchanged(s,host,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(1,2),TestOnlyFillingPolicy.FlaskId)),"VesselOpeningBusy"); });
            cases.Add("filling_source_reservation_survives_logical_portioning",()=>{
                var s=Filling();string job=StartFill(s,Q(4));string free=Portion(s,Q(28),TestOnlyFillingPolicy.SupplyId,TestOnlyPolicy.CompanionId);
                Require(s.Capture().Work.Reservations.Single().LotId==TestOnlyFillingPolicy.SupplyId&&IL(s,free).Amount==Q(28),"Portion reassigned source claim.");
                RejectUnchanged(s,host,IC(s,CommandKind.PortionInventory,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(1)),TestOnlyPolicy.CompanionId),"InventoryQuantityUnavailable");
                AdvanceI(s,60);Require(IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(0)&&IL(s,Fill(s,job).OutputLotId).Amount==Q(4),"Portion broke completion debit."); });
            cases.Add("filling_rejects_overfull_and_same_vessel_without_cost",()=>{
                var s=Filling();AtCompanion(s);
                RejectUnchanged(s,host,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(1),TestOnlyFillingPolicy.ActorSkinId)),"FillCapacityUnavailable");
                RejectUnchanged(s,host,IC(s,CommandKind.StartWaterFill,TestOnlyInventoryPolicy.WaterId,new InventoryRequest(Q(1),TestOnlyFillingPolicy.ActorSkinId)),"SameVesselFill");
                RejectUnchanged(s,host,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(5),TestOnlyFillingPolicy.CompanionSkinId),TestOnlyPolicy.CompanionId),"FillCapacityUnavailable"); });
            cases.Add("filling_two_hands_reach_and_worker_exclusivity_are_required",()=>{
                var one=Filling(1);RejectUnchanged(one,host,IC(one,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(1),TestOnlyFillingPolicy.CompanionSkinId),TestOnlyPolicy.CompanionId),"TwoHandsRequired");
                var s=Filling();RejectUnchanged(s,host,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(1),TestOnlyFillingPolicy.FlaskId)),"FillOutOfReach");
                string job=StartFill(s,Q(1));RejectUnchanged(s,host,IC(s,CommandKind.Move,actor:TestOnlyPolicy.CompanionId,x:-1),"WorkerBusy");
                RejectUnchanged(s,host,IC(s,CommandKind.TendCrop,CropId,actor:TestOnlyPolicy.CompanionId),"PolicyFailure");
                FillCommand(s,CommandKind.PauseWaterFill,job);CommitI(s,IC(s,CommandKind.Move,actor:TestOnlyPolicy.CompanionId,x:0,y:1));CommitI(s,IC(s,CommandKind.Move,actor:TestOnlyPolicy.CompanionId,x:-1,y:0));
                RejectUnchanged(s,host,IC(s,CommandKind.ResumeWaterFill,job,actor:TestOnlyPolicy.CompanionId),"FillOutOfReach"); });
            cases.Add("filling_reserved_hands_prevent_receiving_handheld_food",()=>{
                var s=Filling();AtCompanion(s);StartFill(s,Q(1));
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1),TestOnlyPolicy.CompanionId,HandlingKind.Handover)),"RecipientHandsReserved"); });
            cases.Add("filling_pause_frees_worker_for_other_work",()=>{
                var s=Filling();string job=StartFill(s,Q(1));AdvanceI(s,20);FillCommand(s,CommandKind.PauseWaterFill,job);
                CommitI(s,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId));
                RejectUnchanged(s,host,IC(s,CommandKind.ResumeWaterFill,job,actor:TestOnlyPolicy.CompanionId),"WorkerBusy");AdvanceI(s,3600);
                FillCommand(s,CommandKind.ResumeWaterFill,job);AdvanceI(s,40);Require(Fill(s,job).Status==WaterFillStatus.Complete&&Crop(s).Growth==T(40),"Paused assignment did not release worker."); });
            cases.Add("filling_shared_clock_advances_other_intake_without_extra_elapsed_time",()=>{
                var s=Filling();StartFill(s,Q(4));Eat(s,Q(1),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,120);
                Require(s.Capture().RuleClock==T(120)&&s.Capture().WaterFills.Single().EndedAt==T(60)&&s.Capture().Intakes.Single().EndedAt==T(60)
                    &&WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.ActorSkinId)==Q(3)&&WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.CompanionSkinId)==Q(4),"Parallel work multiplied elapsed clock."); });
            cases.Add("filling_shared_crop_and_handling_milestones_do_not_skip_completion",()=>{
                var s=Filling();AtCompanion(s);CommitI(s,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId));
                string job=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId,worker:TestOnlyPolicy.ActorId);AdvanceI(s,4000);
                Require(Fill(s,job).EndedAt==T(60)&&Crop(s).Growth==T(400),"Crop/fill ordering skipped a milestone.");
                s=Filling();job=StartFill(s,Q(1));AdvanceI(s,119,2);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                Require(Fill(s,job).EndedAt==T(60)&&s.Capture().RuleClock==T(121,2),"Handling second skipped fractional fill endpoint."); });
            cases.Add("filling_then_drinking_uses_the_same_physical_water",()=>{
                var s=Filling();string job=StartFill(s,Q(2,3));AdvanceI(s,60);string liquid=Fill(s,job).OutputLotId;Eat(s,Q(1,3),liquid,TestOnlyPolicy.CompanionId);
                AdvanceI(s,10);s=RestoreFilling(s);AdvanceI(s,10);var v=s.Capture();
                Require(IL(s,liquid).Amount==Q(1,3)&&OrdinaryInventory.Consumed(v,TestOnlyPolicy.CompanionId,NutritionKind.WaterPints)==Q(1,3)
                    &&IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(94,3)&&WaterFilling.Contents(v,TestOnlyFillingPolicy.CompanionSkinId)==Q(1,3),"Fill/drink copied physical water or lost intake progress."); });
            cases.Add("filling_decant_preserves_constituent_owner_and_original_lineage",()=>{
                var s=Filling();AtCompanion(s);string job=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId,TestOnlyInventoryPolicy.WaterId,TestOnlyPolicy.ActorId);AdvanceI(s,60);
                string water=Fill(s,job).OutputLotId;var meta=s.Capture().InventoryLots.Single(x=>x.LotId==water);
                Require(meta.ParentId==TestOnlyInventoryPolicy.WaterId&&meta.OwnerId==TestOnlyPolicy.ActorId&&IL(s,water).CustodianId==TestOnlyPolicy.CompanionId
                    &&WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.ActorSkinId)==Q(3),"Decant changed title or fabricated consumption."); });
            cases.Add("filling_claimed_source_can_still_supply_unreserved_intake_after_pause",()=>{
                var s=Filling();AtCompanion(s);string job=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId,TestOnlyInventoryPolicy.WaterId,TestOnlyPolicy.ActorId);
                AdvanceI(s,20);FillCommand(s,CommandKind.PauseWaterFill,job,TestOnlyPolicy.ActorId);Eat(s,Q(3),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,180);
                Require(IL(s,TestOnlyInventoryPolicy.WaterId).Amount==Q(1)&&s.Capture().Work.AvailableAmount(TestOnlyInventoryPolicy.WaterId)==Q(0),"Consumption spent reserved transfer water.");
                FillCommand(s,CommandKind.ResumeWaterFill,job,TestOnlyPolicy.ActorId);AdvanceI(s,40);Require(IL(s,TestOnlyInventoryPolicy.WaterId).Amount==Q(0),"Remaining reserved water failed to transfer."); });
            cases.Add("filling_portions_in_a_vessel_preserve_single_occupancy_and_tare",()=>{
                var s=Filling();string child=Portion(s,Q(1,3),TestOnlyInventoryPolicy.WaterId);var v=s.Capture();
                Require(v.VesselContents.Single(x=>x.LotId==child).VesselId==TestOnlyFillingPolicy.ActorSkinId&&WaterFilling.Contents(v,TestOnlyFillingPolicy.ActorSkinId)==Q(4)
                    &&TestOnlyInventoryPolicy.CarriedBurden(v,TestOnlyPolicy.ActorId).Pounds==Q(8),"Logical water portion duplicated volume or tare."); });
            cases.Add("filling_tactical_and_pending_encounter_transition_remain_gated",()=>{
                var s=Filling();string job=StartFill(s,Q(1));RejectUnchanged(s,host,IC(s,CommandKind.EnterInventoryCombat),"PendingFillEncounterTransitionUnsupported");
                FillCommand(s,CommandKind.PauseWaterFill,job);RejectUnchanged(s,host,IC(s,CommandKind.EnterInventoryCombat),"PendingFillEncounterTransitionUnsupported");
                FillCommand(s,CommandKind.CancelWaterFill,job);CommitI(s,IC(s,CommandKind.EnterInventoryCombat));
                RejectUnchanged(s,host,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(1),TestOnlyFillingPolicy.FlaskId)),"TacticalFillingUnsupported"); });
            cases.Add("filling_permissions_cover_liquid_and_destination_before_duplicate",()=>{
                var s=Filling();AtCompanion(s);var c=IC(s,CommandKind.StartWaterFill,TestOnlyInventoryPolicy.WaterId,new InventoryRequest(Q(1),TestOnlyFillingPolicy.FlaskId));
                var noDest=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},inventoryOwners:new[]{TestOnlyPolicy.ActorId});
                RejectUnchanged(s,noDest,c,"InventoryNotAuthorized");CommitI(s,c);RejectUnchanged(s,noDest,c,"InventoryNotAuthorized");
                var noSource=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},inventoryOwners:new[]{TestOnlyPolicy.CompanionId});RejectUnchanged(s,noSource,c,"InventoryNotAuthorized"); });
            cases.Add("filling_resume_rechecks_permission_and_cancel_can_release_after_revocation",()=>{
                var s=Filling();string job=StartFill(s,Q(1));FillCommand(s,CommandKind.PauseWaterFill,job);
                var revoked=new Authority(host.Principal,new[]{TestOnlyPolicy.CompanionId});RejectUnchanged(s,revoked,IC(s,CommandKind.ResumeWaterFill,job,actor:TestOnlyPolicy.CompanionId),"InventoryNotAuthorized");
                Require(s.Execute(revoked,IC(s,CommandKind.CancelWaterFill,job,actor:TestOnlyPolicy.CompanionId)).Outcome==Outcome.Committed,"Revoked use permission prevented cleanup."); });
            cases.Add("filling_source_vessel_owner_is_checked_separately_from_water_owner",()=>{
                var s=Filling();AtCompanion(s);string job=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId,TestOnlyInventoryPolicy.WaterId,TestOnlyPolicy.ActorId);AdvanceI(s,60);
                string water=Fill(s,job).OutputLotId;
                // Actor owns the water and destination skin; companion still owns the source flask.
                var restricted=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},inventoryOwners:new[]{TestOnlyPolicy.ActorId});
                var c=IC(s,CommandKind.StartWaterFill,water,new InventoryRequest(Q(1),TestOnlyFillingPolicy.ActorSkinId));
                RejectUnchanged(s,restricted,c,"InventoryNotAuthorized");CommitI(s,c);RejectUnchanged(s,restricted,c,"InventoryNotAuthorized"); });
            cases.Add("filling_drinking_requires_vessel_use_permission_separate_from_liquid_title",()=>{
                var s=Filling();AtCompanion(s);Eat(s,Q(1),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,60);
                string job=StartFill(s,Q(1),TestOnlyFillingPolicy.ActorSkinId,worker:TestOnlyPolicy.ActorId);AdvanceI(s,60);string water=Fill(s,job).OutputLotId;
                var restricted=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},inventoryOwners:new[]{TestOnlyPolicy.CompanionId});
                var c=IC(s,CommandKind.StartIntake,water,new InventoryRequest(Q(1)));
                RejectUnchanged(s,restricted,c,"InventoryNotAuthorized");CommitI(s,c);RejectUnchanged(s,restricted,c,"InventoryNotAuthorized"); });
            cases.Add("filling_bulk_and_chunked_advances_match_domain_state",()=>{
                var a=Filling();var b=Filling();foreach(var s in new[]{a,b}){StartFill(s,Q(1));Eat(s,Q(2,3));}
                AdvanceI(a,1000);foreach(int n in new[]{1,29,29,1,100,400,40,400})AdvanceI(b,n);
                byte[] Domain(Simulation s){var v=s.Capture();v.Revision=0;v.Receipts=Array.Empty<CommandReceipt>();return codec.Encode(v);}
                Require(Domain(a).SequenceEqual(Domain(b)),"Clock partition changed transfer/intake results."); });
            cases.Add("filling_store_restores_paused_reservations_and_preserves_old_schema",()=>{
                var store=new FileSaveStore();string path=Path.Combine(directory,"filling.ddsave");var s=Filling();string job=StartFill(s,Q(1));AdvanceI(s,20);FillCommand(s,CommandKind.PauseWaterFill,job);store.Save(path,s.Capture());
                s=new Simulation(new TestOnlyFillingPolicy(),store.Load(path),ExecutionProfile.Laboratory);FillCommand(s,CommandKind.ResumeWaterFill,job);AdvanceI(s,40);store.Save(path,s.Capture());
                Require(store.Load(path).WaterFills[0].Status==WaterFillStatus.Complete&&store.Load(path+".bak").WaterFills[0].Progress==T(20),"Save/resume lost filling history.");
                Throws<InvalidDataException>(()=>store.Save(path,new TestOnlyInventoryPolicy().Initial()));
                var old=new TestOnlyInventoryPolicy().Initial();var bytes=codec.Encode(old);Require(codec.Decode(bytes).SchemaVersion==4&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Schema4 migrated implicitly."); });
            cases.Add("filling_restore_rejects_forged_progress_labor_and_completion_time",()=>{
                var s=Filling();string id=StartFill(s,Q(1));AdvanceI(s,30);var v=s.Capture();var j=v.WaterFills[0];
                v.WaterFills=new[]{new WaterFillRecord(j.Id,j.WorkerId,j.SourceLotId,j.DestinationId,j.ReservationId,j.Amount,j.StartedAt,T(31),null,j.Status)};
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyFillingPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                AdvanceI(s,30);v=s.Capture();j=v.WaterFills[0];v.RuleClock=T(61);
                v.WaterFills=new[]{new WaterFillRecord(j.Id,j.WorkerId,j.SourceLotId,j.DestinationId,j.ReservationId,j.Amount,j.StartedAt,j.Progress,T(61),j.Status,j.OutputLotId)};
                v.InventoryLots=v.InventoryLots.Select(x=>x.LotId==j.OutputLotId?new InventoryLotRecord(x.LotId,x.ParentId,x.OwnerId,x.CreatedAmount,T(61),x.Nutrition,x.FreshUntil,x.Access):x).ToArray();
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyFillingPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("filling_restore_rejects_missing_content_and_aliased_vessel_ids",()=>{
                var p=new TestOnlyFillingPolicy();var v=p.Initial();v.VesselContents=Array.Empty<VesselContentRecord>();Throws<ArgumentException>(()=>codec.Encode(v));
                v=p.Initial();v.VesselContents=new[]{v.VesselContents[0],v.VesselContents[0]};Throws<ArgumentException>(()=>codec.Encode(v));
                v=p.Initial();v.Vessels[0]=new WaterVesselRecord(TestOnlyPolicy.ActorId,WaterVesselProfile.Waterskin,TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId);
                Throws<ArgumentException>(()=>codec.Encode(v)); });
            cases.Add("filling_restore_rejects_completed_work_using_another_actors_carried_vessel",()=>{
                var s=Filling();StartFill(s,Q(1));AdvanceI(s,60);var v=s.Capture();var j=v.WaterFills[0];
                v.WaterFills=new[]{new WaterFillRecord(j.Id,TestOnlyPolicy.ActorId,j.SourceLotId,j.DestinationId,j.ReservationId,j.Amount,j.StartedAt,j.Progress,j.EndedAt,j.Status,j.OutputLotId)};
                v.Work=new WorkLedger(v.Work.Lots,v.Work.WorkerIntervals.Select(w=>new WorkerInterval(w.Id,w.JobId,TestOnlyPolicy.ActorId,w.Start,w.End)),v.Work.Reservations);
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyFillingPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("filling_schema_release_future_version_and_corruption_guards",()=>{
                var p=new TestOnlyFillingPolicy();Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                var v=p.Initial();v.SchemaVersion=4;Throws<ArgumentException>(()=>codec.Encode(v));var bytes=Bytes(Filling());var bad=(byte[])bytes.Clone();bad[4]=6;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));
                bad=(byte[])bytes.Clone();bad[bad.Length-40]^=1;Throws<InvalidDataException>(()=>codec.Decode(bad));Throws<InvalidDataException>(()=>codec.Decode(bytes.Take(bytes.Length-1).ToArray())); });
            cases.Add("filling_detached_views_do_not_change_owned_reservations",()=>{
                var s=Filling();StartFill(s,Q(1));var bytes=Bytes(s);var v=s.Capture();v.Vessels[0]=null;v.VesselContents=Array.Empty<VesselContentRecord>();v.WaterFills=Array.Empty<WaterFillRecord>();
                Require(bytes.SequenceEqual(Bytes(s)),"Read model mutated vessel/job state."); });
            cases.Add("filling_failed_disk_commit_keeps_paused_primary_and_backup",()=>{
                string path=Path.Combine(directory,"filling-failure.ddsave");var store=new FileSaveStore();var s=Filling();store.Save(path,s.Capture());string job=StartFill(s,Q(1));AdvanceI(s,20);FillCommand(s,CommandKind.PauseWaterFill,job);store.Save(path,s.Capture());
                byte[] before=File.ReadAllBytes(path),backup=File.ReadAllBytes(path+".bak");FillCommand(s,CommandKind.ResumeWaterFill,job);AdvanceI(s,40);
                Throws<IOException>(()=>new FileSaveStore(new FailingCommit()).Save(path,s.Capture()));Require(before.SequenceEqual(File.ReadAllBytes(path))&&backup.SequenceEqual(File.ReadAllBytes(path+".bak")),"Failed commit damaged saved fill state."); });
        }
    }
}
#endif
