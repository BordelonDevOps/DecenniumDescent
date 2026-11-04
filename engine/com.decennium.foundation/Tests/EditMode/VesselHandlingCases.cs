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
        private static Simulation Vessels(int actorHands=2,int companionHands=2)
        {var p=new TestOnlyFillingPolicy(actorHands,companionHands,movableVessels:true);return new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);}
        private static void MoveVessel(Simulation s,string vessel,HandlingKind kind,string actor=TestOnlyPolicy.ActorId,string recipient="")
            =>CommitI(s,IC(s,CommandKind.HandleVessel,vessel,new InventoryRequest(Q(1),recipient,kind),actor));
        private static WaterVesselRecord Vessel(Simulation s,string id)=>s.Capture().Vessels.Single(x=>x.Id==id);
        private static Simulation RestoreVessels(Simulation s)=>new Simulation(new TestOnlyFillingPolicy(movableVessels:true),new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);
        private static void AddVesselHandlingCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlyFillingPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("vessel_pickup_moves_one_physical_empty_object_and_tare",()=>{
                var s=Vessels();MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);var v=s.Capture();
                Require(v.RuleClock==T(1)&&v.Vessels.Length==3&&v.InventoryLots.Length==5&&v.VesselMoves.Length==1
                    &&Vessel(s,TestOnlyFillingPolicy.FlaskId).LocationId==TestOnlyPolicy.CompanionId
                    &&TestOnlyInventoryPolicy.CarriedBurden(v,TestOnlyPolicy.CompanionId).Pounds==Q(3),"Empty pickup lost identity/tare or charged contents."); });
            cases.Add("vessel_fill_carry_handover_drink_preserves_original_liquid_title",()=>{
                var s=Vessels();string job=StartFill(s,Q(4));AdvanceI(s,60);AtCompanion(s);
                MoveVessel(s,TestOnlyFillingPolicy.CompanionSkinId,HandlingKind.Handover,TestOnlyPolicy.CompanionId,TestOnlyPolicy.ActorId);
                string water=Fill(s,job).OutputLotId;var before=s.Capture();
                Require(before.RuleClock==T(61)&&IL(s,water).LocationId==TestOnlyFillingPolicy.CompanionSkinId&&IL(s,water).CustodianId==TestOnlyPolicy.ActorId
                    &&before.InventoryLots.Single(x=>x.LotId==water).OwnerId==TestOnlyPolicy.CompanionId
                    &&Vessel(s,TestOnlyFillingPolicy.CompanionSkinId).OwnerId==TestOnlyPolicy.CompanionId,"Handover changed title or liquid identity.");
                Eat(s,Q(1),water);AdvanceI(s,30);s=RestoreVessels(s);AdvanceI(s,30);
                Require(IL(s,water).Amount==Q(3)&&OrdinaryInventory.Consumed(s.Capture(),TestOnlyPolicy.ActorId,NutritionKind.WaterPints)==Q(1)
                    &&IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(28),"Transferred water was duplicated or lost through intake/save."); });
            cases.Add("vessel_drop_pickup_moves_contents_chain_without_new_lots",()=>{
                var s=Vessels();AtCompanion(s);string child=Portion(s,Q(1,3),TestOnlyInventoryPolicy.WaterId);var before=s.Capture();
                MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Drop);MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);
                var v=s.Capture();Require(v.InventoryLots.Length==before.InventoryLots.Length&&v.Work.Lots.Count==before.Work.Lots.Count&&WaterFilling.Contents(v,TestOnlyFillingPolicy.ActorSkinId)==Q(4)
                    &&IL(s,child).CustodianId==TestOnlyPolicy.CompanionId&&IL(s,child).LocationId==TestOnlyFillingPolicy.ActorSkinId
                    &&v.InventoryLots.Single(x=>x.LotId==child).ParentId==TestOnlyInventoryPolicy.WaterId,"Intact movement created descendants or changed nested location.");
                s=RestoreVessels(s);Eat(s,Q(1,3),child,TestOnlyPolicy.CompanionId);AdvanceI(s,20);Require(IL(s,child).Amount==Q(0),"New custodian cannot use transferred water."); });
            cases.Add("vessel_multiple_liquid_histories_move_for_one_second",()=>{
                var s=Vessels();AtCompanion(s);string a=StartFill(s,Q(1,2),TestOnlyFillingPolicy.FlaskId,worker:TestOnlyPolicy.ActorId);AdvanceI(s,60);
                string b=StartFill(s,Q(1,2),TestOnlyFillingPolicy.FlaskId,TestOnlyInventoryPolicy.WaterId,TestOnlyPolicy.ActorId);AdvanceI(s,60);
                var roots=s.Capture().InventoryLots.Length;MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup);
                Require(s.Capture().RuleClock==T(121)&&s.Capture().InventoryLots.Length==roots&&IL(s,Fill(s,a).OutputLotId).Amount==Q(1,2)
                    &&IL(s,Fill(s,b).OutputLotId).Amount==Q(1,2),"Several histories caused several operations or merged water."); });
            cases.Add("vessel_tare_follows_emptying_and_handover_once",()=>{
                var s=Vessels();AtCompanion(s);Eat(s,Q(4),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,240);
                MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Handover,recipient:TestOnlyPolicy.CompanionId);var v=s.Capture();
                Require(TestOnlyInventoryPolicy.CarriedBurden(v,TestOnlyPolicy.ActorId).Pounds==Q(3)&&TestOnlyInventoryPolicy.CarriedBurden(v,TestOnlyPolicy.CompanionId).Pounds==Q(3)
                    &&v.Vessels.Length==3&&WaterFilling.Contents(v,TestOnlyFillingPolicy.ActorSkinId)==Q(0),"Empty transferred vessel lost or duplicated tare."); });
            cases.Add("vessel_drink_then_transfer_then_refill_restores_historical_access",()=>{
                var s=Vessels();AtCompanion(s);Eat(s,Q(2),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,120);
                MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Handover,recipient:TestOnlyPolicy.CompanionId);
                string fill=StartFill(s,Q(2),TestOnlyFillingPolicy.ActorSkinId);AdvanceI(s,60);s=RestoreVessels(s);
                MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Drop,TestOnlyPolicy.CompanionId);s=RestoreVessels(s);
                Require(Fill(s,fill).Status==WaterFillStatus.Complete&&s.Capture().Intakes.Single().ActorId==TestOnlyPolicy.ActorId
                    &&WaterFilling.Contents(s.Capture(),TestOnlyFillingPolicy.ActorSkinId)==Q(4),"Later custody invalidated real earlier intake/filling history."); });
            cases.Add("vessel_active_and_paused_fill_claims_block_intact_movement",()=>{
                var s=Vessels();AtCompanion(s);string fill=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId);
                foreach(bool paused in new[]{false,true}) {
                    if(paused)FillCommand(s,CommandKind.PauseWaterFill,fill);
                    RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.FlaskId,new InventoryRequest(Q(1))),"VesselHasPendingWork");
                }
                FillCommand(s,CommandKind.CancelWaterFill,fill);MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup);
                Require(IL(s,TestOnlyFillingPolicy.SupplyId).Amount==Q(32),"Movement cancelled or moved reserved fill water implicitly."); });
            cases.Add("vessel_source_reservation_blocks_moving_whole_vessel",()=>{
                var s=Vessels();AtCompanion(s);string fill=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId,TestOnlyInventoryPolicy.WaterId,TestOnlyPolicy.ActorId);
                FillCommand(s,CommandKind.PauseWaterFill,fill,TestOnlyPolicy.ActorId);
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,new InventoryRequest(Q(1),handling:HandlingKind.Drop)),"VesselHasPendingWork");
                FillCommand(s,CommandKind.CancelWaterFill,fill,TestOnlyPolicy.ActorId);MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Drop); });
            cases.Add("vessel_partial_intake_blocks_transfer_until_actual_interruption",()=>{
                var s=Vessels();AtCompanion(s);Eat(s,Q(1),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,30);
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,new InventoryRequest(Q(1),TestOnlyPolicy.CompanionId,HandlingKind.Handover)),"WorkerBusy");
                CommitI(s,IC(s,CommandKind.InterruptIntake,s.Capture().Intakes[0].Id));MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Handover,recipient:TestOnlyPolicy.CompanionId);
                Require(IL(s,TestOnlyInventoryPolicy.WaterId).Amount==Q(7,2)&&s.Capture().Work.Reservations[0].ConsumedAmount==Q(1,2),"Intact transfer erased partial intake or released it implicitly."); });
            cases.Add("vessel_one_hand_handling_does_not_inherit_two_hand_filling_cost",()=>{
                var s=Vessels(companionHands:1);MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);
                RejectUnchanged(s,host,IC(s,CommandKind.StartWaterFill,TestOnlyFillingPolicy.SupplyId,new InventoryRequest(Q(1),TestOnlyFillingPolicy.FlaskId),TestOnlyPolicy.CompanionId),"TwoHandsRequired");
                var no=Vessels(companionHands:0);RejectUnchanged(no,host,IC(no,CommandKind.HandleVessel,TestOnlyFillingPolicy.FlaskId,new InventoryRequest(Q(1)),TestOnlyPolicy.CompanionId),"HandlingHandRequired"); });
            cases.Add("vessel_recipient_consent_and_free_hand_are_required",()=>{
                var s=Vessels();AtCompanion(s);var c=IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,new InventoryRequest(Q(1),TestOnlyPolicy.CompanionId,HandlingKind.Handover));
                var unwilling=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},inventoryOwners:new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId});
                RejectUnchanged(s,unwilling,c,"RecipientNotWilling");StartFill(s,Q(1));
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,new InventoryRequest(Q(1),TestOnlyPolicy.CompanionId,HandlingKind.Handover)),"RecipientHandsUnavailable"); });
            cases.Add("vessel_permissions_cover_each_contained_owner_before_replay",()=>{
                var s=Vessels();AtCompanion(s);string job=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId,TestOnlyInventoryPolicy.WaterId,TestOnlyPolicy.ActorId);AdvanceI(s,60);
                var c=IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.FlaskId,new InventoryRequest(Q(1)));
                var onlyVessel=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},inventoryOwners:new[]{TestOnlyPolicy.CompanionId});
                var onlyWater=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},inventoryOwners:new[]{TestOnlyPolicy.ActorId});
                RejectUnchanged(s,onlyVessel,c,"InventoryNotAuthorized");RejectUnchanged(s,onlyWater,c,"InventoryNotAuthorized");CommitI(s,c);
                RejectUnchanged(s,onlyVessel,c,"InventoryNotAuthorized");RejectUnchanged(s,onlyWater,c,"InventoryNotAuthorized");
                var bytes=Bytes(s);Require(s.Execute(host,c).Outcome==Outcome.Duplicate&&bytes.SequenceEqual(Bytes(s)),"Intact movement repeated on retry."); });
            cases.Add("vessel_unsupported_placement_storage_and_partial_object_reject",()=>{
                var s=Vessels();RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,new InventoryRequest(Q(1),handling:HandlingKind.Drop)),"UnsupportedVesselPlacement");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,new InventoryRequest(Q(1),handling:HandlingKind.Stow)),"VesselStorageNotEstablished");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,new InventoryRequest(Q(1,2),handling:HandlingKind.Drop)),"InvalidVesselHandling");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.FlaskId,new InventoryRequest(Q(1))),"VesselOutOfReach"); });
            cases.Add("vessel_tactical_movement_shares_interaction_budget_with_food",()=>{
                var s=Vessels();AtCompanion(s);CommitI(s,IC(s,CommandKind.EnterInventoryCombat));
                MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Drop);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                Require(s.Capture().RuleClock==T(0)&&s.Capture().InventoryInteractions==2&&s.Capture().VesselMoves.Single().Tactical,"Tactical vessel movement charged time or separate allowance.");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.FlaskId,new InventoryRequest(Q(1))),"InteractionBudgetUnavailable");s=RestoreVessels(s); });
            cases.Add("vessel_same_clock_tactical_order_and_cancelled_fill_history_survive",()=>{
                var s=Vessels();AtCompanion(s);string fill=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId);FillCommand(s,CommandKind.CancelWaterFill,fill);
                CommitI(s,IC(s,CommandKind.EnterInventoryCombat));MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup);MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Handover,recipient:TestOnlyPolicy.CompanionId);
                s=RestoreVessels(s);Require(s.Capture().RuleClock==T(0)&&Vessel(s,TestOnlyFillingPolicy.FlaskId).CustodianId==TestOnlyPolicy.CompanionId,"Equal-time ordering lost true custody history."); });
            cases.Add("vessel_handling_processes_another_workers_fill_completion",()=>{
                var s=Vessels();AtCompanion(s);string fill=StartFill(s,Q(1));AdvanceI(s,119,2);MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup);
                Require(Fill(s,fill).EndedAt==T(60)&&s.Capture().RuleClock==T(121,2)&&s.Capture().VesselMoves.Single().EndedAt==T(121,2),"Handling skipped shared fill endpoint."); });
            cases.Add("vessel_store_preserves_custody_history_and_older_schema_meaning",()=>{
                var s=Vessels();AtCompanion(s);MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Drop);string path=Path.Combine(directory,"vessels.ddsave");var store=new FileSaveStore();store.Save(path,s.Capture());
                MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);store.Save(path,s.Capture());
                Require(store.Load(path).VesselMoves.Length==2&&store.Load(path+".bak").VesselMoves.Length==1,"Persistence lost movement history.");
                Throws<InvalidDataException>(()=>store.Save(path,new TestOnlyFillingPolicy().Initial()));
                var old=Filling();RejectUnchanged(old,host,IC(old,CommandKind.HandleVessel,TestOnlyFillingPolicy.FlaskId,new InventoryRequest(Q(1)),TestOnlyPolicy.CompanionId),"VesselMovementNotSupported"); });
            cases.Add("vessel_restore_rejects_unrecorded_location_and_broken_history",()=>{
                var s=Vessels();var v=s.Capture();var vessel=v.Vessels[0];v.Vessels[0]=new WaterVesselRecord(vessel.Id,vessel.Profile,vessel.OwnerId,TestOnlyCropPolicy.PlotId,vessel.CustodianId);
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyFillingPolicy(movableVessels:true),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                AtCompanion(s);MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup);v=s.Capture();var m=v.VesselMoves[0];
                v.VesselMoves=new[]{new VesselHandlingRecord(m.Id,m.Sequence,m.ActorId,m.VesselId,TestOnlyPolicy.CompanionId,m.FromCustodian,m.ToLocation,m.ToCustodian,m.Kind,m.StartedAt,m.EndedAt,m.Tactical)};
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyFillingPolicy(movableVessels:true),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("vessel_schema_release_legacy_fields_and_corruption_guards",()=>{
                var p=new TestOnlyFillingPolicy(movableVessels:true);Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                var s=Vessels();MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);var v=s.Capture();v.SchemaVersion=5;Throws<ArgumentException>(()=>codec.Encode(v));
                byte[] bytes=Bytes(s),bad=(byte[])bytes.Clone();bad[4]=12;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));
                bad=(byte[])bytes.Clone();bad[bad.Length-33]^=1;Throws<InvalidDataException>(()=>codec.Decode(bad));
                v=s.Capture();v.VesselMoves[0]=null;Require(bytes.SequenceEqual(Bytes(s)),"Detached movement history mutated simulation."); });
            cases.Add("vessel_last_revision_movement_commits_and_roundtrips_without_sequence_overflow",()=>{
                var p=new TestOnlyFillingPolicy(movableVessels:true);var v=p.Initial();v.Revision=long.MaxValue-1;var s=new Simulation(p,v,ExecutionProfile.Laboratory);
                MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);s=RestoreVessels(s);
                Require(s.Capture().Revision==long.MaxValue&&s.Capture().VesselMoves[0].Sequence==long.MaxValue
                    &&TestOnlyInventoryPolicy.CarriedBurden(s.Capture(),TestOnlyPolicy.CompanionId).Pounds==Q(3),"Last legal revision overflowed movement ordering.");
                // Observe the historical calculation used by restore, without widening the production API for a test.
                var historical=typeof(VesselHandling).GetMethod("BurdenAt",System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Static);
                Require((RuleQuantity)historical.Invoke(null,new object[]{s.Capture(),TestOnlyPolicy.CompanionId,T(1),long.MaxValue})==Q(3),"Maximum sequence rewound the completed movement during historical burden validation.");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.FlaskId,new InventoryRequest(Q(1),handling:HandlingKind.Drop),TestOnlyPolicy.CompanionId),"SessionCapacityReached"); });
            cases.Add("vessel_history_capacity_rejects_atomically_without_evicting_old_moves",()=>{
                var s=Vessels();for(int i=0;i<32;i++) {
                    MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);
                    MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Drop,TestOnlyPolicy.CompanionId);
                }
                Require(s.Capture().VesselMoves.Length==64&&s.Capture().RuleClock==T(64),"Movement bound lost previous records.");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.FlaskId,new InventoryRequest(Q(1)),TestOnlyPolicy.CompanionId),"InvalidResult");s=RestoreVessels(s); });
            cases.Add("vessel_restore_rejects_movement_during_paused_capacity_reservation",()=>{
                var s=Vessels();string fill=StartFill(s,Q(1),TestOnlyFillingPolicy.FlaskId);FillCommand(s,CommandKind.PauseWaterFill,fill);
                FillCommand(s,CommandKind.CancelWaterFill,fill);MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);
                var v=s.Capture();var j=v.WaterFills[0];
                v.WaterFills=new[]{new WaterFillRecord(j.Id,j.WorkerId,j.SourceLotId,j.DestinationId,j.ReservationId,j.Amount,j.StartedAt,j.Progress,null,WaterFillStatus.Paused)};
                v.Work=new WorkLedger(v.Work.Lots,v.Work.WorkerIntervals,v.Work.Reservations.Select(r=>new ResourceReservation(r.Id,r.JobId,r.LotId,r.Amount)));
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyFillingPolicy(movableVessels:true),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("vessel_store_failed_commit_preserves_pre_transfer_primary_and_backup",()=>{
                var s=Vessels();string path=Path.Combine(directory,"vessels-failure.ddsave");var store=new FileSaveStore();store.Save(path,s.Capture());
                MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Pickup,TestOnlyPolicy.CompanionId);store.Save(path,s.Capture());byte[] primary=File.ReadAllBytes(path),backup=File.ReadAllBytes(path+".bak");
                MoveVessel(s,TestOnlyFillingPolicy.FlaskId,HandlingKind.Drop,TestOnlyPolicy.CompanionId);
                Throws<IOException>(()=>new FileSaveStore(new FailingCommit()).Save(path,s.Capture()));
                Require(primary.SequenceEqual(File.ReadAllBytes(path))&&backup.SequenceEqual(File.ReadAllBytes(path+".bak")),"Failed transfer save damaged retained custody history."); });
        }
    }
}
#endif
