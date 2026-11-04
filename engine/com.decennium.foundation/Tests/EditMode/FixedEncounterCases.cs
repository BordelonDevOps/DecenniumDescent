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
        private static Simulation Encounters(params string[] order){var p=new TestOnlyEncounterPolicy(order);return new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);}
        private static void BeginEncounter(Simulation s,string actor=TestOnlyPolicy.ActorId)=>CommitI(s,IC(s,CommandKind.BeginFixedEncounter,actor:actor));
        private static void EncounterCommand(Simulation s,CommandKind kind)
        {var e=s.Capture().Encounter;CommitI(s,IC(s,kind,e.CurrentTurnId,actor:e.CurrentActor));}
        private static void EndTurn(Simulation s)=>EncounterCommand(s,CommandKind.EndRegularTurn);
        private static Simulation RestoreEncounter(Simulation s,params string[] order)=>new Simulation(new TestOnlyEncounterPolicy(order),new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);
        private static void AddFixedEncounterCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlyFillingPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("encounter_entry_preserves_clock_and_actual_partial_intake",()=>{
                var s=Encounters();Eat(s,Q(1),TestOnlyInventoryPolicy.WaterId);AdvanceI(s,15);BeginEncounter(s);var v=s.Capture();
                Require(v.RuleClock==T(15)&&v.Encounter.Origin==T(15)&&v.Encounter.Round==1&&v.Encounter.CurrentActor==TestOnlyPolicy.ActorId
                    &&v.Intakes.Single().Status==IntakeStatus.CombatInterrupted&&v.Work.Reservations.Single().ConsumedAmount==Q(1,4)
                    &&v.Work.Reservations.Single().ReleasedAmount==Q(3,4),"Encounter entry moved time or lost actual consumption.");
                EndTurn(s);s=RestoreEncounter(s);Require(s.Capture().RuleClock==T(18)&&s.Capture().Intakes.Single().EndedAt==T(15),"Later turn rewrote interruption timestamp."); });
            cases.Add("encounter_fixed_order_wrap_adds_six_seconds_once",()=>{
                var s=Encounters();AdvanceI(s,1,3);BeginEncounter(s);EndTurn(s);
                Require(s.Capture().RuleClock==T(10,3)&&s.Capture().Encounter.CurrentActor==TestOnlyPolicy.CompanionId&&s.Capture().Encounter.Round==1,"Wrong first slot end.");
                EndTurn(s);var e=s.Capture().Encounter;Require(s.Capture().RuleClock==T(19,3)&&e.CurrentActor==TestOnlyPolicy.ActorId&&e.Round==2&&e.TurnOrdinal==2,"Round wrap added another round or lost order.");
                EndTurn(s);EndTurn(s);Require(s.Capture().RuleClock==T(37,3)&&s.Capture().Encounter.Round==3,"Repeated fixed round drifted."); });
            cases.Add("encounter_exact_fractional_schedule_repeats_with_original_origin",()=>{
                var order=Enumerable.Range(0,7).Select(i=>"actor"+i).ToArray();var e=new FixedEncounterRecord("test",T(1,3),order,new long[]{1});
                Require(FixedEncounterRules.Start(e,1)==T(25,21)&&FixedEncounterRules.Start(e,7)==T(19,3)
                    &&FixedEncounterRules.Start(e,70)==T(181,3),"Fixed schedule rounded phases or multiplied actor time."); });
            cases.Add("encounter_single_actor_keeps_background_crop_on_shared_clock",()=>{
                var s=Encounters(TestOnlyPolicy.ActorId);AtCompanion(s);CommitI(s,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId));AdvanceI(s,3597);
                BeginEncounter(s);EndTurn(s);Require(s.Capture().RuleClock==T(3603)&&Crop(s).Growth==T(3)&&s.Capture().Encounter.Round==2,"Combat did not process background crop completion at3600.");
                s=RestoreEncounter(s,TestOnlyPolicy.ActorId);EndTurn(s);Require(Crop(s).Growth==T(9),"Background growth lost continuity after restore."); });
            cases.Add("encounter_order_is_supplied_and_cannot_be_implicitly_sorted",()=>{
                var ids=new[]{TestOnlyPolicy.CompanionId,TestOnlyPolicy.ActorId};var p=new TestOnlyEncounterPolicy(ids);ids[0]="changed";var s=new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);
                BeginEncounter(s,TestOnlyPolicy.CompanionId);Require(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.CompanionId,"Fixture order mutated or auto-sorted.");
                EndTurn(s);Require(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId,"Resolved second slot changed.");
                Throws<ArgumentException>(()=>RestoreEncounter(s));Throws<ArgumentException>(()=>new TestOnlyEncounterPolicy(TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId)); });
            cases.Add("encounter_wrong_actor_turn_identity_and_arbitrary_clock_reject",()=>{
                var s=Encounters();BeginEncounter(s);var e=s.Capture().Encounter;
                RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,e.CurrentTurnId,actor:TestOnlyPolicy.CompanionId),"WrongRegularTurn");
                RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,"wrong-turn"),"WrongRegularTurn");
                RejectUnchanged(s,host,IC(s,CommandKind.AdvanceClock,x:99,y:1),"EncounterCommandNotImplemented");
                RejectUnchanged(s,host,IC(s,CommandKind.Move,x:1),"EncounterCommandNotImplemented"); });
            cases.Add("encounter_entry_requires_host_world_authority_before_replay",()=>{
                var s=Encounters();var c=IC(s,CommandKind.BeginFixedEncounter);var restricted=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId},true);
                RejectUnchanged(s,restricted,c,"NotAuthorized");CommitI(s,c);RejectUnchanged(s,restricted,c,"NotAuthorized");
                var bytes=Bytes(s);Require(s.Execute(host,c).Outcome==Outcome.Duplicate&&bytes.SequenceEqual(Bytes(s)),"Entry retried a start marker."); });
            cases.Add("encounter_end_turn_replay_and_stale_command_do_not_repeat_markers",()=>{
                var s=Encounters();BeginEncounter(s);var e=s.Capture().Encounter;var c=IC(s,CommandKind.EndRegularTurn,e.CurrentTurnId);CommitI(s,c);var bytes=Bytes(s);
                Require(s.Execute(host,c).Outcome==Outcome.Duplicate&&bytes.SequenceEqual(Bytes(s)),"End replay advanced time twice.");
                RejectUnchanged(s,host,new Command("stale",TestOnlyPolicy.ActorId,c.ExpectedRevision,CommandKind.EndRegularTurn,e.CurrentTurnId),"StaleRevision");
                var revoked=new Authority(host.Principal,new[]{TestOnlyPolicy.CompanionId},true,true);RejectUnchanged(s,revoked,c,"NotAuthorized"); });
            cases.Add("encounter_pending_fill_and_busy_roster_entry_reject_atomically",()=>{
                var s=Encounters();string fill=StartFill(s,Q(1));FillCommand(s,CommandKind.PauseWaterFill,fill);Eat(s,Q(1),TestOnlyInventoryPolicy.WaterId);
                RejectUnchanged(s,host,IC(s,CommandKind.BeginFixedEncounter),"PendingFillEncounterTransitionUnsupported");
                FillCommand(s,CommandKind.CancelWaterFill,fill);CommitI(s,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId));
                RejectUnchanged(s,host,IC(s,CommandKind.BeginFixedEncounter),"EncounterWorkerBusy");
                Require(s.Capture().Intakes.Single().Status==IntakeStatus.Working,"Rejected entry interrupted intake on owned state."); });
            cases.Add("encounter_food_and_vessel_interactions_refresh_per_actor_turn",()=>{
                var s=Encounters();AtCompanion(s);BeginEncounter(s);MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Handover,recipient:TestOnlyPolicy.CompanionId);
                HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);Require(FixedEncounterRules.ActionSpent(s.Capture()),"Second interaction did not pay Action.");
                EndTurn(s);MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Handover,TestOnlyPolicy.CompanionId,TestOnlyPolicy.ActorId);EndTurn(s);
                Require(!FixedEncounterRules.ActionSpent(s.Capture())&&s.Capture().InventoryInteractions==0,"New regular turn did not refresh ordinary allowance.");
                HandleI(s,s.Capture().Handling[0].ChildId,Q(1),HandlingKind.Retrieve);s=RestoreEncounter(s);
                Require(s.Capture().RuleClock==T(6)&&s.Capture().Handling.Length==2&&s.Capture().VesselMoves.Length==2,"Past interactions were rebound to current actor/time."); });
            cases.Add("encounter_dash_and_second_interaction_share_one_action",()=>{
                var s=Encounters();BeginEncounter(s);EncounterCommand(s,CommandKind.EncounterDash);
                Require(FixedEncounterRules.CurrentMovement(s.Capture()).Dashes==1&&FixedEncounterRules.CurrentMovement(s.Capture()).Remaining(30)==60,"Paid Dash failed to grant current movement cap.");
                HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                RejectUnchanged(s,host,IC(s,CommandKind.HandleInventory,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1),handling:HandlingKind.Stow)),"ActionAlreadySpent");
                RejectUnchanged(s,host,IC(s,CommandKind.EncounterDash,s.Capture().Encounter.CurrentTurnId),"ActionAlreadySpent");
                EndTurn(s);EndTurn(s);Require(FixedEncounterRules.CurrentMovement(s.Capture()).Dashes==0&&!FixedEncounterRules.ActionSpent(s.Capture()),"Dash or spent Action leaked into next regular turn."); });
            cases.Add("encounter_two_interactions_block_dash_but_end_needs_no_action",()=>{
                var s=Encounters();BeginEncounter(s);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);
                RejectUnchanged(s,host,IC(s,CommandKind.EncounterDash,s.Capture().Encounter.CurrentTurnId),"ActionAlreadySpent");
                EndTurn(s);Require(s.Capture().Encounter.CurrentActor==TestOnlyPolicy.CompanionId&&s.Capture().RuleClock==T(3),"Ending a spent turn required another Action."); });
            cases.Add("encounter_dash_then_free_vessel_interaction_retains_action_spend",()=>{
                var s=Encounters();AtCompanion(s);BeginEncounter(s);EncounterCommand(s,CommandKind.EncounterDash);MoveVessel(s,TestOnlyFillingPolicy.ActorSkinId,HandlingKind.Drop);
                s=RestoreEncounter(s);Require(s.Capture().InventoryInteractions==1&&FixedEncounterRules.ActionSpent(s.Capture()),"Free interaction erased paid Dash Action.");EndTurn(s); });
            cases.Add("encounter_restore_rejects_forged_cursor_clock_and_dash_on_start",()=>{
                var s=Encounters();BeginEncounter(s);var v=s.Capture();v.RuleClock=T(1);
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                EncounterCommand(s,CommandKind.EncounterDash);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);v=s.Capture();
                v.EncounterDashes=new[]{new EncounterDashRecord(v.Encounter.StartRevisions[0],0,TestOnlyPolicy.ActorId)};
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("encounter_restore_rejects_future_food_history_before_it_can_stall_turns",()=>{
                var s=Encounters();BeginEncounter(s);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);var v=s.Capture();var h=v.Handling[0];
                v.Handling=new[]{new HandlingRecord("inventory.9223372036854775807.handling",h.ActorId,h.SourceId,h.ChildId,h.Kind,h.StartedAt,h.EndedAt,true)};
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                EndTurn(s);Require(s.Capture().RuleClock==T(3),"Valid source state was damaged by invalid restore."); });
            cases.Add("encounter_restore_rejects_handling_on_regular_start_revision",()=>{
                var s=Encounters();BeginEncounter(s);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);EndTurn(s);var v=s.Capture();var h=v.Handling[0];
                v.Handling=new[]{new HandlingRecord("inventory.3.handling",h.ActorId,h.SourceId,h.ChildId,h.Kind,h.StartedAt,h.EndedAt,true)};
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("encounter_restore_rejects_cross_action_revision_collision",()=>{
                var s=Encounters();BeginEncounter(s);EncounterCommand(s,CommandKind.EncounterDash);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);var v=s.Capture();
                v.EncounterDashes=new[]{new EncounterDashRecord(3,0,TestOnlyPolicy.ActorId)};
                Require(new TestOnlyEncounterPolicy().ValidateState(v)=="InvalidEncounterCommandHistory","One receipt paid both handling and Dash.");
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("encounter_restore_rejects_omitted_dash_spend",()=>{
                var s=Encounters();BeginEncounter(s);EncounterCommand(s,CommandKind.EncounterDash);var v=s.Capture();v.EncounterDashes=Array.Empty<EncounterDashRecord>();
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("encounter_restore_rejects_missing_action_and_its_receipt",()=>{
                var s=Encounters();BeginEncounter(s);EncounterCommand(s,CommandKind.EncounterDash);var v=s.Capture();
                v.EncounterDashes=Array.Empty<EncounterDashRecord>();v.Receipts=v.Receipts.Where(r=>r.Revision!=2).ToArray();
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("encounter_restore_rejects_unrelated_or_duplicate_command_receipts",()=>{
                var s=Encounters();BeginEncounter(s);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);EndTurn(s);
                foreach(int index in new[]{0,1,2}) {var v=s.Capture();v.Receipts[index].Fingerprint="unrelated";
                    Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));}
                var duplicate=s.Capture();var extra=duplicate.Receipts[1].Copy();extra.Id="different-id";duplicate.Receipts=duplicate.Receipts.Concat(new[]{extra}).ToArray();
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(duplicate)),ExecutionProfile.Laboratory)); });
            cases.Add("encounter_restore_rejects_two_interactions_plus_paid_dash",()=>{
                var s=Encounters();BeginEncounter(s);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);var v=s.Capture();
                v.Revision=4;v.EncounterDashes=new[]{new EncounterDashRecord(4,0,TestOnlyPolicy.ActorId)};
                v.Receipts=v.Receipts.Concat(new[]{new CommandReceipt{Id="forged-dash",Principal=host.Principal,Revision=4,
                    Fingerprint=((int)CommandKind.EncounterDash)+"|"+TestOnlyPolicy.ActorId+"|"+v.Encounter.CurrentTurnId+"|3|0|0"}}).ToArray();
                Require(new TestOnlyEncounterPolicy().ValidateState(v)=="OverspentRegularTurnAction","Three costs bypassed the shared one-Action limit.");
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("encounter_restored_old_turn_handling_cannot_move_to_a_new_turn",()=>{
                var s=Encounters();BeginEncounter(s);HandleI(s,TestOnlyInventoryPolicy.FoodId,Q(1),HandlingKind.Stow);EndTurn(s);var v=s.Capture();var h=v.Handling[0];
                v.Handling=new[]{new HandlingRecord(h.Id,h.ActorId,h.SourceId,h.ChildId,h.Kind,T(3),T(3),true)};
                v.InventoryLots=v.InventoryLots.Select(l=>l.LotId==h.ChildId?new InventoryLotRecord(l.LotId,l.ParentId,l.OwnerId,l.CreatedAmount,T(3),l.Nutrition,l.FreshUntil,l.Access):l).ToArray();
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyEncounterPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("encounter_save_resume_retains_turn_identity_budgets_and_backup",()=>{
                var s=Encounters();BeginEncounter(s);EncounterCommand(s,CommandKind.EncounterDash);var store=new FileSaveStore();string path=Path.Combine(directory,"encounter.ddsave");store.Save(path,s.Capture());
                EndTurn(s);store.Save(path,s.Capture());s=new Simulation(new TestOnlyEncounterPolicy(),store.Load(path),ExecutionProfile.Laboratory);EndTurn(s);
                Require(s.Capture().RuleClock==T(6)&&store.Load(path+".bak").EncounterDashes.Length==1&&store.Load(path+".bak").Encounter.TurnOrdinal==0,"Save/backup lost turn/payment state.");
                Throws<InvalidDataException>(()=>store.Save(path,new TestOnlyFillingPolicy(movableVessels:true).Initial())); });
            cases.Add("encounter_128_start_bound_rejects_without_clock_or_marker_loss",()=>{
                var s=Encounters(TestOnlyPolicy.ActorId);BeginEncounter(s);for(int i=0;i<127;i++)EndTurn(s);
                Require(s.Capture().RuleClock==T(762)&&s.Capture().Encounter.Round==128,"Bounded regular starts drifted.");
                RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,s.Capture().Encounter.CurrentTurnId),"EncounterHistoryCapacityReached");s=RestoreEncounter(s,TestOnlyPolicy.ActorId); });
            cases.Add("encounter_detached_order_release_legacy_and_malformed_records_reject",()=>{
                var p=new TestOnlyEncounterPolicy();Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                var s=Encounters();BeginEncounter(s);var v=s.Capture();Throws<NotSupportedException>(()=>((IList<string>)v.Encounter.Order)[0]="changed");
                v.SchemaVersion=6;Throws<ArgumentException>(()=>codec.Encode(v));byte[] bad=Bytes(s);bad[4]=12;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));
                Throws<ArgumentException>(()=>new FixedEncounterRecord(new string('a',90),T(0),new[]{"a"},new long[]{1}));
                Throws<ArgumentException>(()=>new FixedEncounterRecord("id",T(0),new[]{"a"},new long[]{2,1})); });
        }
    }
}
#endif
