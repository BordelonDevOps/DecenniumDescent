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
        private static Simulation Inventory(long fresh=2592000){var p=new TestOnlyInventoryPolicy(fresh);return new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);}
        private static Command IC(Simulation s,CommandKind kind,string target="",InventoryRequest request=null,string actor=TestOnlyPolicy.ActorId,int x=0,int y=0,string id=null)
            =>new Command(id??("i-"+s.Capture().Revision),actor,s.Capture().Revision,kind,target,x,y,request);
        private static void CommitI(Simulation s,Command c){var r=s.Execute(TestOnlyInventoryPolicy.Host(),c);Require(r.Outcome==Outcome.Committed,c.Kind+" rejected: "+r.Code);}
        private static void AdvanceI(Simulation s,int seconds,int denominator=1)=>CommitI(s,IC(s,CommandKind.AdvanceClock,x:seconds,y:denominator));
        private static void Eat(Simulation s,RuleQuantity amount,string lot=TestOnlyInventoryPolicy.FoodId,string actor=TestOnlyPolicy.ActorId)
            =>CommitI(s,IC(s,CommandKind.StartIntake,lot,new InventoryRequest(amount),actor));
        private static string Portion(Simulation s,RuleQuantity amount,string lot=TestOnlyInventoryPolicy.FoodId,string actor=TestOnlyPolicy.ActorId)
        {string id="inventory."+(s.Capture().Revision+1)+".lot";CommitI(s,IC(s,CommandKind.PortionInventory,lot,new InventoryRequest(amount),actor));return id;}
        private static string HandleI(Simulation s,string lot,RuleQuantity amount,HandlingKind kind,string actor=TestOnlyPolicy.ActorId,string recipient="")
        {string id="inventory."+(s.Capture().Revision+1)+".lot";CommitI(s,IC(s,CommandKind.HandleInventory,lot,new InventoryRequest(amount,recipient,kind),actor));return id;}
        private static ResourceLot IL(Simulation s,string id)=>s.Capture().Work.Lots.Single(x=>x.Id==id);
        private static RuleQuantity Eaten(Simulation s,string actor=TestOnlyPolicy.ActorId)=>OrdinaryInventory.Consumed(s.Capture(),actor,NutritionKind.FoodPounds);
        private static Simulation RestoreI(Simulation s,long fresh=2592000)=>new Simulation(new TestOnlyInventoryPolicy(fresh),new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);
        private static void AtCompanion(Simulation s){CommitI(s,IC(s,CommandKind.Move,x:0,y:1));CommitI(s,IC(s,CommandKind.Move,x:1,y:0));CommitI(s,IC(s,CommandKind.Move,x:0,y:1));}
        private static void AddInventoryCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlyInventoryPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("inventory_fractional_portion_is_timeless_and_retains_history",()=>{
                var s=Inventory();string child=Portion(s,Q(1,3));var v=s.Capture();var meta=v.InventoryLots.Single(x=>x.LotId==child);
                Require(IL(s,TestOnlyInventoryPolicy.FoodId).Amount==Q(5,3)&&IL(s,child).Amount==Q(1,3)&&v.RuleClock==T(0)
                    &&meta.ParentId==TestOnlyInventoryPolicy.FoodId&&meta.FreshUntil==T(2592000)&&meta.OwnerId==TestOnlyPolicy.ActorId
                    &&IL(s,child).LocationId==TestOnlyPolicy.ActorId&&v.Work.Reservations.Count==0,"Portion moved, renewed or duplicated food.");
                Require(Bytes(s).SequenceEqual(Bytes(RestoreI(s))),"Fractional portion failed roundtrip."); });
            cases.Add("inventory_portion_keeps_existing_reservation_identity",()=>{
                var s=Inventory();Eat(s,Q(2,3));var claim=s.Capture().Work.Reservations[0];string child=Portion(s,Q(4,3));
                Require(s.Capture().Work.Reservations[0].Id==claim.Id&&s.Capture().Work.Reservations[0].LotId==TestOnlyInventoryPolicy.FoodId
                    &&IL(s,child).Amount==Q(4,3)&&s.Capture().Work.AvailableAmount(TestOnlyInventoryPolicy.FoodId)==Q(0),"Portion moved claimed stock.");
                AdvanceI(s,300);Require(Eaten(s)==Q(1,3)&&IL(s,TestOnlyInventoryPolicy.FoodId).Amount==Q(1,3),"Original intake lost reserved remainder."); });
            cases.Add("inventory_reserved_portion_rejection_is_atomic",()=>{
                var s=Inventory();Eat(s,Q(2));RejectUnchanged(s,host,IC(s,CommandKind.PortionInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1,1000))),"InventoryQuantityUnavailable"); });
            cases.Add("inventory_food_partial_credit_and_completion_use_exact_rates",()=>{
                var s=Inventory();Eat(s,Q(2,3));AdvanceI(s,300);Require(Eaten(s)==Q(1,3)&&IL(s,TestOnlyInventoryPolicy.FoodId).Amount==Q(5,3),"Half meal mismatch.");
                s=RestoreI(s);AdvanceI(s,300);Require(Eaten(s)==Q(2,3)&&s.Capture().Intakes[0].Status==IntakeStatus.Complete
                    &&IL(s,TestOnlyInventoryPolicy.FoodId).Amount==Q(4,3),"Full ordinary meal mismatch."); });
            cases.Add("inventory_water_proportional_rate_and_fixed_skin",()=>{
                var s=Inventory();Eat(s,Q(1,2),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,15);
                Require(OrdinaryInventory.Consumed(s.Capture(),TestOnlyPolicy.ActorId,NutritionKind.WaterPints)==Q(1,4),"Water quarter pint credit.");
                AdvanceI(s,15);Require(IL(s,TestOnlyInventoryPolicy.WaterId).Amount==Q(7,2)&&s.Capture().Intakes[0].Status==IntakeStatus.Complete,"Water half pint finish."); });
            cases.Add("inventory_fractional_second_and_quantity_have_no_quantum",()=>{
                var s=Inventory();Eat(s,Q(1,2700));AdvanceI(s,1,3);
                Require(Eaten(s)==Q(1,2700)&&s.Capture().RuleClock==T(1,3)&&s.Capture().Intakes[0].Status==IntakeStatus.Complete,"Quantity rounded to inventory quantum."); });
            cases.Add("inventory_interruption_preserves_consumed_and_releases_remainder",()=>{
                var s=Inventory();Eat(s,Q(2,3));AdvanceI(s,300);var job=s.Capture().Intakes[0];CommitI(s,IC(s,CommandKind.InterruptIntake,job.Id));
                var r=s.Capture().Work.Reservations[0];Require(Eaten(s)==Q(1,3)&&r.ReleasedAmount==Q(1,3)&&r.Status==ReservationStatus.Mixed
                    &&s.Capture().Work.AvailableAmount(TestOnlyInventoryPolicy.FoodId)==Q(5,3)&&s.Capture().Work.WorkerIntervals[0].End==T(300),"Interrupted stock or labor incorrect.");
                s=RestoreI(s);AdvanceI(s,300);Require(Eaten(s)==Q(1,3),"Interrupted intake resumed itself."); });
            cases.Add("inventory_zero_work_interruption_books_no_labor_or_credit",()=>{
                var s=Inventory();Eat(s,Q(1));CommitI(s,IC(s,CommandKind.InterruptIntake,s.Capture().Intakes[0].Id));
                Require(Eaten(s)==Q(0)&&s.Capture().Work.WorkerIntervals.Count==0&&s.Capture().Work.Reservations[0].Status==ReservationStatus.Released,"No-work cancellation invented labor."); });
            cases.Add("inventory_expiry_stops_at_exact_boundary_and_retains_physical_stock",()=>{
                var s=Inventory(300);Eat(s,Q(2,3));AdvanceI(s,1000);var v=s.Capture();
                Require(v.RuleClock==T(1000)&&Eaten(s)==Q(1,3)&&v.Intakes[0].EndedAt==T(300)&&v.Intakes[0].Status==IntakeStatus.Expired
                    &&IL(s,TestOnlyInventoryPolicy.FoodId).Amount==Q(5,3)&&OrdinaryInventory.EdibleFood(v)==Q(0),"Expiry lost food or credited expired stock.");
                RejectUnchanged(s,host,IC(s,CommandKind.StartIntake,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1,3))),"IntakeExpired"); });
            cases.Add("inventory_completion_at_expiry_credits_only_preceding_interval",()=>{
                var s=Inventory(300);Eat(s,Q(1,3));AdvanceI(s,300);Require(Eaten(s)==Q(1,3)&&s.Capture().Intakes[0].Status==IntakeStatus.Complete
                    &&OrdinaryInventory.EdibleFood(s.Capture())==Q(0),"Exact completion/expiry mismatch."); });
            cases.Add("inventory_two_intakes_and_handling_cannot_overlap_worker",()=>{
                var s=Inventory();Eat(s,Q(1));RejectUnchanged(s,host,IC(s,CommandKind.StartIntake,TestOnlyInventoryPolicy.WaterId,new InventoryRequest(Q(1))),"WorkerBusy");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1),handling:HandlingKind.Stow)),"WorkerBusy");
                RejectUnchanged(s,host,IC(s,CommandKind.Move,x:0,y:1),"WorkerBusy"); });
            cases.Add("inventory_handling_consumes_one_second_and_changes_custody_on_completion",()=>{
                var s=Inventory();string stowed=HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1,3),HandlingKind.Stow);
                Require(s.Capture().RuleClock==T(1)&&s.Capture().InventoryLots.Single(x=>x.LotId==stowed).Access==InventoryAccess.Stowed
                    &&s.Capture().Handling[0].EndedAt==T(1),"Handling time or access wrong.");
                RejectUnchanged(s,host,IC(s,CommandKind.StartIntake,stowed,new InventoryRequest(Q(1,3))),"IntakeRequiresReadyCustody");
                string retrieved=HandleI(s,stowed,Q(1,3),HandlingKind.Retrieve);Eat(s,Q(1,3),retrieved);AdvanceI(s,300);
                Require(Eaten(s)==Q(1,3)&&s.Capture().RuleClock==T(302),"Retrieval/intake double charged or skipped."); });
            cases.Add("inventory_handling_endpoint_expiry_does_not_erase_item",()=>{
                var s=Inventory(1);string child=HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                Require(IL(s,child).Amount==Q(1)&&!OrdinaryInventory.Fresh(s.Capture(),s.Capture().InventoryLots.Single(x=>x.LotId==child))
                    &&OrdinaryInventory.EdibleFood(s.Capture())==Q(0),"Handling renewed freshness."); });
            cases.Add("inventory_drop_and_pickup_preserve_owner_and_history",()=>{
                var s=Inventory();AtCompanion(s);string ground=HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Drop);
                string held=HandleI(s,ground,Q(1),HandlingKind.Pickup,TestOnlyPolicy.CompanionId);
                Require(IL(s,held).LocationId==TestOnlyPolicy.CompanionId&&s.Capture().InventoryLots.Single(x=>x.LotId==held).OwnerId==TestOnlyPolicy.ActorId
                    &&s.Capture().RuleClock==T(2),"Pickup changed owner or free movement."); });
            cases.Add("inventory_handover_requires_consent_and_reach",()=>{
                var s=Inventory();var req=new InventoryRequest(Q(1),TestOnlyPolicy.CompanionId,HandlingKind.Handover);
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,req),"InvalidHandover");AtCompanion(s);
                var noConsent=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},inventoryOwners:new[]{TestOnlyPolicy.ActorId});
                RejectUnchanged(s,noConsent,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,req),"RecipientNotWilling");
                string child=HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Handover,recipient:TestOnlyPolicy.CompanionId);
                Require(IL(s,child).CustodianId==TestOnlyPolicy.CompanionId&&s.Capture().InventoryLots.Single(x=>x.LotId==child).OwnerId==TestOnlyPolicy.ActorId
                    &&s.Capture().Work.WorkerIntervals.Count==1&&s.Capture().Work.WorkerIntervals[0].WorkerId==TestOnlyPolicy.ActorId,"Receiver paid action or owner changed."); });
            cases.Add("inventory_current_owner_permission_applies_before_duplicate",()=>{
                var s=Inventory();var c=IC(s,CommandKind.PortionInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1)));CommitI(s,c);var bytes=Bytes(s);
                Require(s.Execute(host,c).Outcome==Outcome.Duplicate&&bytes.SequenceEqual(Bytes(s)),"Portion duplicate changed state.");
                RejectUnchanged(s,new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId}),c,"InventoryNotAuthorized"); });
            cases.Add("inventory_payload_changes_conflict_with_persisted_command_id",()=>{
                var s=Inventory();var c=IC(s,CommandKind.PortionInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1)));CommitI(s,c);s=RestoreI(s);
                RejectUnchanged(s,host,new Command(c.Id,c.Actor,c.ExpectedRevision,c.Kind,c.Target,inventory:new InventoryRequest(Q(1,2))),"CommandIdConflict"); });
            cases.Add("inventory_water_portion_does_not_pour_or_transfer_container",()=>{
                var s=Inventory();string child=Portion(s,Q(1,2),TestOnlyInventoryPolicy.WaterId);
                Require(IL(s,child).LocationId==TestOnlyPolicy.ActorId&&s.Capture().RuleClock==T(0),"Logical water division poured water.");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,child,new InventoryRequest(Q(1,2),handling:HandlingKind.Stow)),"VesselProcedureNotImplemented"); });
            cases.Add("inventory_combat_entry_interrupts_and_tactical_intake_stays_gated",()=>{
                var s=Inventory();Eat(s,Q(1));AdvanceI(s,90);CommitI(s,IC(s,CommandKind.EnterInventoryCombat));
                Require(Eaten(s)==Q(1,10)&&s.Capture().Intakes[0].Status==IntakeStatus.CombatInterrupted&&s.Capture().Work.Reservations[0].ReleasedAmount==Q(9,10),"Combat entry reset eaten food.");
                RejectUnchanged(s,host,IC(s,CommandKind.StartIntake,TestOnlyInventoryPolicy.WaterId,new InventoryRequest(Q(1))),"TacticalIntakeNotAdopted"); });
            cases.Add("inventory_tactical_interaction_then_action_has_no_elapsed_charge",()=>{
                var s=Inventory();CommitI(s,IC(s,CommandKind.EnterInventoryCombat));string one=HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                string two=HandleI(s,one,Q(1),HandlingKind.Retrieve);s=RestoreI(s);
                Require(s.Capture().RuleClock==T(0)&&s.Capture().InventoryInteractions==2&&s.Capture().Work.WorkerIntervals.Count==0,"Tactical handling charged time or donor labor.");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,two,new InventoryRequest(Q(1),handling:HandlingKind.Stow)),"InteractionBudgetUnavailable");
                RejectUnchanged(s,host,IC(s,CommandKind.EnterInventoryCombat),"InvalidCombatEntry");
                RejectUnchanged(s,host,IC(s,CommandKind.AdvanceClock,x:6,y:1),"EncounterClockNotImplemented"); });
            cases.Add("inventory_combat_entry_requires_current_host_authority",()=>{
                var s=Inventory();RejectUnchanged(s,new Authority("guest",new[]{TestOnlyPolicy.ActorId}),IC(s,CommandKind.EnterInventoryCombat),"NotAuthorized"); });
            cases.Add("inventory_shared_advance_credits_companion_crop_and_actor_intake_once",()=>{
                var s=Inventory();CommitI(s,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId));Eat(s,Q(2,3));AdvanceI(s,4000);
                Require(Eaten(s)==Q(2,3)&&s.Capture().Intakes[0].EndedAt==T(600)&&Crop(s).Stage==CropStage.Growing&&Crop(s).Growth==T(400)
                    &&s.Capture().RuleClock==T(4000)&&s.Capture().RandomState==1,"Shared timeline skipped or duplicated subsystem time."); });
            cases.Add("inventory_handling_advances_independent_crop_labor",()=>{
                var s=Inventory();CommitI(s,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId));
                HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                Require(Crop(s).Tasks[0].Progress==T(1)&&s.Capture().RuleClock==T(1),"Handling froze companion work."); });
            cases.Add("inventory_handling_advances_independent_intake_to_completion",()=>{
                var s=Inventory();AtCompanion(s);string food=HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Handover,recipient:TestOnlyPolicy.CompanionId);
                Eat(s,Q(1,1800),food,TestOnlyPolicy.CompanionId);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                Require(Eaten(s,TestOnlyPolicy.CompanionId)==Q(1,1800)&&s.Capture().Intakes[0].EndedAt==T(3,2)&&s.Capture().RuleClock==T(2),"One-second handling skipped earlier intake completion."); });
            cases.Add("inventory_bulk_and_chunked_advances_have_identical_domain_state",()=>{
                var a=Inventory(500);var b=Inventory(500);
                foreach(var s in new[]{a,b}){CommitI(s,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId));Eat(s,Q(1));}
                AdvanceI(a,100000);foreach(int dt in new[]{1,299,200,1,3099,86400,10000})AdvanceI(b,dt);
                byte[] Domain(Simulation s){var v=s.Capture();v.Revision=0;v.Receipts=Array.Empty<CommandReceipt>();return codec.Encode(v);}
                Require(Domain(a).SequenceEqual(Domain(b)),"Advance partition changed crops or intake."); });
            cases.Add("inventory_schema4_save_resume_and_incompatible_save_guard",()=>{
                string path=Path.Combine(directory,"inventory.ddsave");var store=new FileSaveStore();var s=Inventory();Eat(s,Q(2,3));AdvanceI(s,300);store.Save(path,s.Capture());
                var resumed=new Simulation(new TestOnlyInventoryPolicy(),store.Load(path),ExecutionProfile.Laboratory);AdvanceI(resumed,300);store.Save(path,resumed.Capture());
                Require(store.Load(path).Intakes[0].Status==IntakeStatus.Complete&&store.Load(path+".bak").Work.Reservations[0].ConsumedAmount==Q(1,3),"Saved partial progress lost.");
                Throws<InvalidDataException>(()=>store.Save(path,new TestOnlyCropPolicy().Initial())); });
            cases.Add("inventory_rejects_implicit_legacy_downgrade_and_release_selection",()=>{
                var p=new TestOnlyInventoryPolicy();Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                foreach(int schema in new[]{1,2,3}){var v=p.Initial();v.SchemaVersion=schema;Throws<ArgumentException>(()=>codec.Encode(v));} });
            cases.Add("inventory_decode_checks_corruption_unknown_version_and_boolean",()=>{
                byte[] bytes=Bytes(Inventory());var bad=(byte[])bytes.Clone();bad[10]^=1;Throws<InvalidDataException>(()=>codec.Decode(bad));
                bad=(byte[])bytes.Clone();bad[4]=12;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));
                bad=(byte[])bytes.Clone();bad[bad.Length-32-9]=2;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));
                Throws<InvalidDataException>(()=>codec.Decode(bytes.Take(bytes.Length-1).ToArray())); });
            cases.Add("inventory_restore_rejects_quantity_creation_and_freshness_reset",()=>{
                var s=Inventory();string child=Portion(s,Q(1));var v=s.Capture();var m=v.InventoryLots.Single(x=>x.LotId==child);
                v.InventoryLots=v.InventoryLots.Select(x=>x.LotId==child?new InventoryLotRecord(x.LotId,x.ParentId,x.OwnerId,x.CreatedAmount,x.CreatedAt,x.Nutrition,T(9999999),x.Access):x).ToArray();
                Throws<ArgumentException>(()=>codec.Encode(v));v=s.Capture();v.Work=new WorkLedger(v.Work.Lots.Select(x=>x.Id==child?new ResourceLot(x.Id,x.UnitId,Q(2),x.LocationId,x.CustodianId):x));
                Throws<ArgumentException>(()=>codec.Encode(v)); });
            cases.Add("inventory_restore_rejects_missing_parent_and_cycles",()=>{
                var s=Inventory();string child=Portion(s,Q(1));
                foreach(string parent in new[]{"unknown",child}){var v=s.Capture();v.InventoryLots=v.InventoryLots.Select(x=>x.LotId==child?new InventoryLotRecord(x.LotId,parent,x.OwnerId,x.CreatedAmount,x.CreatedAt,x.Nutrition,x.FreshUntil,x.Access):x).ToArray();Throws<ArgumentException>(()=>codec.Encode(v));} });
            cases.Add("inventory_restore_rejects_forged_intake_credit_and_tactical_reset",()=>{
                var s=Inventory();Eat(s,Q(1));AdvanceI(s,300);var v=s.Capture();var j=v.Intakes[0];v.Intakes=new[]{new IntakeRecord(j.Id,j.ActorId,j.LotId,j.ReservationId,T(1),null,IntakeStatus.Working)};
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyInventoryPolicy(),v,ExecutionProfile.Laboratory));
                s=Inventory();CommitI(s,IC(s,CommandKind.EnterInventoryCombat));HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);v=s.Capture();v.InventoryInteractions=0;
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyInventoryPolicy(),v,ExecutionProfile.Laboratory)); });
            cases.Add("inventory_detached_capture_cannot_change_live_history",()=>{
                var s=Inventory();Portion(s,Q(1));var before=Bytes(s);var v=s.Capture();v.InventoryLots=Array.Empty<InventoryLotRecord>();v.Intakes=new IntakeRecord[1];v.InventoryCombat=true;
                Require(before.SequenceEqual(Bytes(s)),"Capture exposed authoritative inventory arrays."); });
            cases.Add("inventory_complete_farming_harvest_portion_handover_intake_loop",()=>{
                var s=Inventory();Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,3600);string root=s.Capture().CropFood.Single().LotId;
                Require(OrdinaryInventory.EdibleFood(s.Capture())==Q(10),"Harvest was not registered once in physical inventory.");
                string carried=HandleI(s,root,Q(8),HandlingKind.Pickup,TestOnlyPolicy.CompanionId);
                string serving=Portion(s,Q(2,3),carried,TestOnlyPolicy.CompanionId);AtCompanion(s);
                string handed=HandleI(s,serving,Q(2,3),HandlingKind.Handover,TestOnlyPolicy.CompanionId,TestOnlyPolicy.ActorId);
                Eat(s,Q(2,3),handed);AdvanceI(s,300);s=RestoreI(s);AdvanceI(s,300);
                Require(Eaten(s)==Q(2,3)&&OrdinaryInventory.EdibleFood(s.Capture())==Q(28,3)&&IL(s,root).Amount==Q(0)
                    &&s.Capture().InventoryLots.Single(x=>x.LotId==handed).OwnerId==TestOnlyPolicy.CompanionId
                    &&s.Capture().InventoryLots.Single(x=>x.LotId==handed).FreshUntil==s.Capture().CropFood[0].FreshUntil,
                    "Farm-to-meal loop lost ownership, freshness, actual quantity or consumed credit.");
                Throws<InvalidOperationException>(()=>CampGreens.EdibleFood(s.Capture())); });
            cases.Add("inventory_history_capacity_rejects_without_partial_reservation",()=>{
                var s=Inventory();for(int i=0;i<32;i++){Eat(s,Q(1,900));AdvanceI(s,1);}
                RejectUnchanged(s,host,IC(s,CommandKind.StartIntake,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1,900))),"InvalidResult"); });
            cases.Add("inventory_receipt_capacity_is_checked_before_work",()=>{
                var p=new TestOnlyInventoryPolicy();var v=p.Initial();v.Revision=512;
                v.Receipts=Enumerable.Range(1,512).Select(i=>new CommandReceipt{Id="receipt"+i,Principal="old",Fingerprint="old",Revision=i}).ToArray();
                var s=new Simulation(p,v,ExecutionProfile.Laboratory);
                RejectUnchanged(s,host,IC(s,CommandKind.PortionInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1))),"SessionCapacityReached"); });
            cases.Add("inventory_maximum_component_counts_fit_snapshot_codec",()=>{
                string Id(string prefix,int i=0)=>(prefix+i.ToString()).PadRight(96,'x');
                var v=new Snapshot{SchemaVersion=Snapshot.InventorySchema,ContentFingerprint=Id("content"),TestOnly=true,Revision=512,RandomState=1,RuleClock=T(1),
                    Actors=Enumerable.Range(0,64).Select(i=>new ActorState{Id=Id("actor",i)}).ToArray(),
                    Objects=Enumerable.Range(0,64).Select(i=>new ObjectState{Id=Id("object",i)}).ToArray(),
                    Receipts=Enumerable.Range(1,512).Select(i=>new CommandReceipt{Id=Id("receipt",i),Principal=Id("principal",i),Fingerprint=new string('f',512),Revision=i}).ToArray()};
                var lots=Enumerable.Range(0,128).Select(i=>new ResourceLot(Id("lot",i),Id("unit"),Q(0),Id("location"),Id("owner"))).ToArray();
                var claims=Enumerable.Range(0,128).Select(i=>new ResourceReservation(Id("claim",i),Id("job",i),lots[i].Id,Q(1,3),released:Q(1,3))).ToArray();
                var intervals=Enumerable.Range(0,128).Select(i=>new WorkerInterval(Id("labor",i),Id("job",i),v.Actors[i%64].Id,T(i),T(i+1))).ToArray();
                v.Work=new WorkLedger(lots,intervals,claims);
                v.InventoryLots=lots.Select(l=>new InventoryLotRecord(l.Id,"",Id("owner"),Q(0),T(0),NutritionKind.None,null,InventoryAccess.Ground)).ToArray();
                v.Intakes=Enumerable.Range(0,32).Select(i=>new IntakeRecord(Id("job",i),v.Actors[i].Id,lots[i].Id,claims[i].Id,T(0),T(1),IntakeStatus.Interrupted)).ToArray();
                v.CropPlots=Enumerable.Range(0,8).Select(i=>new CropPlotRecord(Id("plot",i),Id("owner"),true)).ToArray();
                v.Crops=Enumerable.Range(0,8).Select(i=>new CropBatchRecord(Id("crop",i),v.CropPlots[i].Id,lots[0].Id,Id("owner"),T(0),T(1),CropStage.Failed,T(0),null,null,null,T(1),
                    Enumerable.Range(0,32).Select(j=>new CropWorkRecord(Id("task",i*32+j),v.Actors[0].Id,CropWorkKind.Plant,CropWorkStatus.Cancelled,T(0),T(0),T(1),Array.Empty<string>())))).ToArray();
                v.CropFood=Enumerable.Range(0,8).Select(i=>new CropFoodRecord(lots[i].Id,v.Crops[i].Id,T(1),true)).ToArray();
                // Add maximum handling records without new quantity: retained zero-stock descendants preserve conserved history.
                v.InventoryLots=v.InventoryLots.Select((x,i)=>i<64?x:new InventoryLotRecord(x.LotId,lots[i-64].Id,x.OwnerId,Q(0),T(1),x.Nutrition,null,x.Access)).ToArray();
                v.Handling=Enumerable.Range(0,64).Select(i=>new HandlingRecord(Id("handle",i),v.Actors[i].Id,lots[i].Id,lots[i+64].Id,HandlingKind.Drop,T(0),T(1),false)).ToArray();
                var bytes=codec.Encode(v);Require(bytes.Length<SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximum accepted component counts do not roundtrip within save bound.");
                // Structural codec bounds, independently of the smaller playable fixture and its policy.
                v.SchemaVersion=Snapshot.VesselSchema;
                v.Vessels=Enumerable.Range(0,8).Select(i=>new WaterVesselRecord(Id("vessel",i),WaterVesselProfile.Waterskin,Id("owner"),Id("location"),Id("owner"))).ToArray();
                v.VesselContents=lots.Select((l,i)=>new VesselContentRecord(l.Id,v.Vessels[i%8].Id)).ToArray();
                v.Work=new WorkLedger(lots.Select((l,i)=>new ResourceLot(l.Id,l.UnitId,l.Amount,v.Vessels[i%8].Id,l.CustodianId)),intervals,claims);
                v.InventoryLots=v.InventoryLots.Select(x=>new InventoryLotRecord(x.LotId,x.ParentId,x.OwnerId,x.CreatedAmount,x.CreatedAt,NutritionKind.WaterPints,null,x.Access)).ToArray();
                v.WaterFills=Enumerable.Range(32,32).Select(i=>new WaterFillRecord(Id("job",i),v.Actors[i].Id,lots[i].Id,v.Vessels[(i+1)%8].Id,claims[i].Id,Q(1,3),T(0),T(0),null,WaterFillStatus.Paused)).ToArray();
                bytes=codec.Encode(v);Require(bytes.Length<SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximum schema5 component counts exceed save bound or fail roundtrip.");
                v.SchemaVersion=Snapshot.MovableVesselSchema;
                v.VesselMoves=Enumerable.Range(0,64).Select(i=>new VesselHandlingRecord(Id("vessel-move",i),i+1,v.Actors[i].Id,v.Vessels[i%8].Id,
                    Id("from"),Id("owner"),v.Actors[i].Id,v.Actors[i].Id,HandlingKind.Pickup,T(0),T(1),false)).ToArray();
                bytes=codec.Encode(v);Require(bytes.Length<SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximum schema6 component counts exceed save bound or fail roundtrip.");
                v.SchemaVersion=Snapshot.EncounterSchema;v.InventoryCombat=true;v.InventoryTurnActor=v.Actors[63].Id;
                v.Encounter=new FixedEncounterRecord(new string('e',87),T(0),v.Actors.Select(a=>a.Id),Enumerable.Range(1,128).Select(i=>(long)i));
                v.EncounterDashes=Enumerable.Range(0,128).Select(i=>new EncounterDashRecord(129+i,i,v.Actors[i%64].Id)).ToArray();
                bytes=codec.Encode(v);Require(bytes.Length<SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximum schema7 component counts exceed save bound or fail roundtrip.");
                v.SchemaVersion=Snapshot.ActorLifeSchema;
                v.Characters=v.Actors.Select(a=>new ActorCharacterRecord(a.Id,Id("profile"),Enumerable.Repeat(int.MaxValue,6),
                    Enumerable.Range(0,20).Select(i=>new CharacterLevelFact(Id("class",i),int.MaxValue)))).ToArray();
                v.Lives=v.Actors.Select(a=>new ActorLifeRecord(a.Id,long.MaxValue,0,long.MaxValue,new[]{0,1,2},true,false,true,0,0,T(1,3),long.MaxValue,true,
                    Enumerable.Range(0,32).Select(i=>Id("held",i)))).ToArray();
                v.LifeEvents=Enumerable.Range(0,256).Select(i=>new ActorLifeEvent(v.Actors[i%64].Id,i+1,T(1),LifeEventKind.StableRecovery,-1,0,0,1,1,0)).ToArray();
                bytes=codec.Encode(v);Require(bytes.Length<SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximum schema8 component counts exceed save bound or fail roundtrip.");
                File.WriteAllText(Path.Combine(directory,"maximal-actor-life-bytes.txt"),bytes.Length.ToString(System.Globalization.CultureInfo.InvariantCulture));
                v.SchemaVersion=Snapshot.ClubAttackSchema;
                v.Clubs=v.Actors.Select((a,i)=>new ClubInstance(Id("club",i),Id("profile"),a.Id,a.Id,a.Id,int.MaxValue,int.MinValue)).ToArray();
                v.Stances=Enumerable.Range(0,128).Select(i=>new StanceSelectionRecord(v.Actors[i%64].Id,i+1,i,CombatStance.Aggressive,T(6))).ToArray();
                var attack=new CombatAttackRoll(20,20,20,int.MaxValue,int.MaxValue,true,true,uint.MaxValue,uint.MaxValue,long.MaxValue);
                var damage=new CombatDamageRoll(new[]{4,4},long.MaxValue,long.MaxValue,uint.MaxValue,uint.MaxValue,long.MaxValue,20,6,4);
                v.MeleeAttacks=Enumerable.Range(0,128).Select(i=>new MeleeAttackRecord(Id("attack",i),i+1,i+1,i,v.Actors[i%64].Id,v.Actors[(i+1)%64].Id,v.Clubs[i%64].Id,T(1),AttackKnockoutMode.KnockOutIfEligible,attack,damage)).ToArray();
                v.Presses=v.Actors.Select((a,i)=>new PressRecord(a.Id,v.Actors[(i+1)%64].Id,i+1,T(6))).ToArray();
                bytes=codec.Encode(v);Require(bytes.Length<SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximum schema9 component counts exceed save bound or fail roundtrip.");
                File.WriteAllText(Path.Combine(directory,"maximal-club-bytes.txt"),bytes.Length.ToString(System.Globalization.CultureInfo.InvariantCulture));
                v.SchemaVersion=Snapshot.PostureSchema;v.ActorMovement=v.Actors.Select((a,i)=>new ActorMovementRecord(a.Id,int.MaxValue,i,long.MaxValue)).ToArray();
                bytes=codec.Encode(v);Require(bytes.Length<SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximum schema10 component counts exceed bound or fail roundtrip.");
                File.WriteAllText(Path.Combine(directory,"maximal-posture-bytes.txt"),bytes.Length.ToString(System.Globalization.CultureInfo.InvariantCulture));
                v.SchemaVersion=Snapshot.TacticalMovementSchema;
                v.TacticalActors=v.Actors.Select((a,i)=>new ActorTacticalRecord(a.Id,i,false,5,true,i)).ToArray();
                v.TacticalMoves=v.Actors.Select((a,i)=>new TacticalMoveRecord(Id("move",i),i+1,i+1,i,a.Id,int.MinValue,int.MinValue,int.MaxValue,int.MaxValue,
                    TacticalMoveKind.Press,TacticalMoveStatus.Completed,v.Actors.Where(other=>other.Id!=a.Id).Select(other=>other.Id),63,long.MaxValue,Id("offer",i))).ToArray();
                v.PressOffers=Enumerable.Range(0,128).Select(i=>new PressOfferRecord(Id("offer",i),Id("move",i%64),v.Actors[(i+1)%64].Id,v.Actors[i%64].Id,
                    i+1,i+1,PressOfferStatus.Accepted,i+1)).ToArray();
                bytes=codec.Encode(v);Require(bytes.Length<SnapshotCodec.MaxBytes&&bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Maximum schema11 component counts exceed bound or fail roundtrip.");
                File.WriteAllText(Path.Combine(directory,"maximal-tactical-bytes.txt"),bytes.Length.ToString(System.Globalization.CultureInfo.InvariantCulture)); });
            cases.Add("inventory_restore_rejects_handling_before_source_creation",()=>{
                var s=Inventory();AdvanceI(s,10);string source=Portion(s,Q(1));string child=HandleI(s,source,Q(1),HandlingKind.Stow);var v=s.Capture();var h=v.Handling[0];
                v.Handling=new[]{new HandlingRecord(h.Id,h.ActorId,h.SourceId,h.ChildId,h.Kind,T(9),T(10),false)};
                v.InventoryLots=v.InventoryLots.Select(x=>x.LotId==child?new InventoryLotRecord(x.LotId,x.ParentId,x.OwnerId,x.CreatedAmount,T(10),x.Nutrition,x.FreshUntil,x.Access):x).ToArray();
                v.Work=new WorkLedger(v.Work.Lots,new[]{new WorkerInterval(v.Work.WorkerIntervals[0].Id,h.Id,h.ActorId,T(9),T(10))},v.Work.Reservations);
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyInventoryPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("inventory_restore_rejects_tactical_work_before_frozen_entry_time",()=>{
                var s=Inventory();Eat(s,Q(1));AdvanceI(s,10);CommitI(s,IC(s,CommandKind.EnterInventoryCombat));var v=s.Capture();v.RuleClock=T(11);
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyInventoryPolicy(),v,ExecutionProfile.Laboratory));
                s=Inventory();CommitI(s,IC(s,CommandKind.EnterInventoryCombat));HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);v=s.Capture();v.RuleClock=T(1);
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyInventoryPolicy(),v,ExecutionProfile.Laboratory)); });
            cases.Add("inventory_nested_ledger_requires_schema_specific_version_and_checksum",()=>{
                byte[] ReplaceLedger(byte[] original,byte[] work) {
                    int lengthAt=FindMapping(original)+DiceStream.MappingVersion.Length,offset=lengthAt+4,oldLength=BitConverter.ToInt32(original,lengthAt);
                    var next=new byte[original.Length-oldLength+work.Length];Buffer.BlockCopy(original,0,next,0,lengthAt);
                    Buffer.BlockCopy(BitConverter.GetBytes(work.Length),0,next,lengthAt,4);Buffer.BlockCopy(work,0,next,offset,work.Length);
                    Buffer.BlockCopy(original,offset+oldLength,next,offset+work.Length,original.Length-32-offset-oldLength);Resign(next);return next;
                }
                var p=new TestOnlyInventoryPolicy();var v=p.Initial();var current=codec.Encode(v);
                Throws<InvalidDataException>(()=>codec.Decode(ReplaceLedger(current,new WorkLedgerCodec().Encode(v.Work,1))));
                var old=new TestOnlyCropPolicy().Initial();Throws<InvalidDataException>(()=>codec.Decode(ReplaceLedger(codec.Encode(old),new WorkLedgerCodec().Encode(old.Work,2))));
                var inner=new WorkLedgerCodec().Encode(v.Work,2);inner[20]^=1;Throws<InvalidDataException>(()=>codec.Decode(ReplaceLedger(current,inner)));
                inner=new WorkLedgerCodec().Encode(v.Work,2);inner[4]=3;Resign(inner);Throws<InvalidDataException>(()=>codec.Decode(ReplaceLedger(current,inner)));
            });
            cases.Add("inventory_stowing_requires_known_container_fit_not_just_carry_capacity",()=>{
                var s=Inventory();Mature(s);FarmWork(s,CommandKind.HarvestCrop);FarmAdvance(s,3600);string root=s.Capture().CropFood.Single().LotId;
                string greens=HandleI(s,root,Q(8),HandlingKind.Pickup,TestOnlyPolicy.CompanionId);
                foreach(var amount in new[]{Q(8),Q(1)})RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,greens,
                    new InventoryRequest(amount,handling:HandlingKind.Stow),TestOnlyPolicy.CompanionId),"ContainerFitNotEstablished");
                // A checksum-valid forged stow cannot bypass the same host storage prerequisite on restore.
                var v=s.Capture();string child="forged-greens",job="forged-stow";var start=v.RuleClock;var end=start.AddSeconds(1);var source=v.InventoryLots.Single(x=>x.LotId==greens);
                v.Work=new WorkLedger(v.Work.Lots.Select(x=>x.Id==greens?new ResourceLot(x.Id,x.UnitId,Q(7),x.LocationId,x.CustodianId):x)
                    .Concat(new[]{new ResourceLot(child,CampGreens.FoodUnit,Q(1),TestOnlyPolicy.CompanionId,TestOnlyPolicy.CompanionId)}),
                    v.Work.WorkerIntervals.Concat(new[]{new WorkerInterval(job+".labor",job,TestOnlyPolicy.CompanionId,start,end)}),v.Work.Reservations);
                OrdinaryInventory.AdvanceTo(v,end);
                v.InventoryLots=v.InventoryLots.Concat(new[]{new InventoryLotRecord(child,greens,source.OwnerId,Q(1),end,source.Nutrition,source.FreshUntil,InventoryAccess.Stowed)}).ToArray();
                v.Handling=v.Handling.Concat(new[]{new HandlingRecord(job,TestOnlyPolicy.CompanionId,greens,child,HandlingKind.Stow,start,end,false)}).ToArray();
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyInventoryPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("inventory_fixed_container_tares_count_once_and_survive_emptying",()=>{
                var s=Inventory();var burden=TestOnlyInventoryPolicy.CarriedBurden(s.Capture(),TestOnlyPolicy.ActorId);
                Require(burden.Pounds==Q(8)&&burden.Load==Q(4,5)&&TestOnlyInventoryPolicy.CarriedBurden(s.Capture(),TestOnlyPolicy.CompanionId).Pounds==Q(1),"Initial pouch/skin tare omitted or double counted.");
                HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                Require(TestOnlyInventoryPolicy.CarriedBurden(s.Capture(),TestOnlyPolicy.ActorId).Pounds==Q(8),"Stowing duplicated content weight.");
                Eat(s,Q(4),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,240);burden=TestOnlyInventoryPolicy.CarriedBurden(s.Capture(),TestOnlyPolicy.ActorId);
                Require(burden.Pounds==Q(4)&&burden.Load==Q(2,5)&&IL(s,TestOnlyInventoryPolicy.WaterId).Amount==Q(0),"Empty skin or pouch lost its own weight.");
            });
            cases.Add("inventory_failed_file_commit_preserves_partial_intake",()=>{
                string path=Path.Combine(directory,"inventory-fail.ddsave");var s=Inventory();var store=new FileSaveStore();store.Save(path,s.Capture());Eat(s,Q(1));AdvanceI(s,300);store.Save(path,s.Capture());
                var before=File.ReadAllBytes(path);AdvanceI(s,300);Throws<IOException>(()=>new FileSaveStore(new FailingCommit()).Save(path,s.Capture()));
                Require(before.SequenceEqual(File.ReadAllBytes(path)),"Failed file commit lost partial intake."); });
        }
    }
}
#endif
