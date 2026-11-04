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
        private static TestOnlyClubAttackPolicy PosturePolicy(int actorSpeed=30,int companionSpeed=30,bool prone=false,uint seed=1,long companionHp=26)
            =>new TestOnlyClubAttackPolicy(actorProne:prone,seed:seed,companionHp:companionHp,actorBaseWalkingSpeed:actorSpeed,companionBaseWalkingSpeed:companionSpeed);
        private static void Posture(Simulation s,CommandKind kind)=>EncounterCommand(s,kind);
        private static void AddPostureCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlyFillingPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("posture_explicit_speeds_select_new_schema_without_legacy_defaults",()=>{
                var p=PosturePolicy(25,35);var s=Clubs(p);var v=s.Capture();Require(v.SchemaVersion==10&&TestOnlyClubAttackPolicy.WalkingSpeed(v,TestOnlyPolicy.ActorId)==25
                    &&TestOnlyClubAttackPolicy.WalkingSpeed(v,TestOnlyPolicy.CompanionId)==35&&v.ActorMovement.All(m=>m.TurnOrdinal==-1&&m.Spent==0),"Base Speed facts or initial ledger wrong.");
                Require(new TestOnlyClubAttackPolicy().Initial().SchemaVersion==9&&new TestOnlyClubAttackPolicy().Initial().ActorMovement.Length==0,"Old profile silently gained Speed.");
                Require(Bytes(s).SequenceEqual(Bytes(RestoreClub(s,p))),"Movement facts did not roundtrip.");
                Throws<ArgumentException>(()=>new TestOnlyClubAttackPolicy(actorBaseWalkingSpeed:30));Throws<ArgumentException>(()=>PosturePolicy(-1)); });
            cases.Add("posture_stand_requires_stance_and_uses_guarded_current_speed",()=>{
                var s=Clubs(PosturePolicy(prone:true));BeginEncounter(s);RejectUnchanged(s,host,IC(s,CommandKind.StandFromProne,s.Capture().Encounter.CurrentTurnId),"StanceRequired");
                Stance(s);Posture(s,CommandKind.StandFromProne);var v=s.Capture();
                Require(TestOnlyClubAttackPolicy.WalkingSpeed(v,TestOnlyPolicy.ActorId)==25&&TestOnlyClubAttackPolicy.WalkingLedger(v).Spent==12
                    &&TestOnlyClubAttackPolicy.WalkingLedger(v).Remaining(25)==13&&!Life(s).Prone&&v.RandomState==1&&v.RuleClock==T(0),"Standing spent Action/time/RNG or half base instead of current Speed."); });
            cases.Add("posture_drop_costs_no_movement_and_can_precede_stance",()=>{
                var s=Clubs(PosturePolicy());BeginEncounter(s);Posture(s,CommandKind.DropProne);var v=s.Capture();
                Require(Life(s).Prone&&v.Stances.Length==0&&TestOnlyClubAttackPolicy.WalkingLedger(v).Spent==0&&Life(s).HeldItems.Count==1,"Drop charged budget, chose stance or dropped equipment.");
                RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,v.Encounter.CurrentTurnId),"StanceRequired");Stance(s,CombatStance.Mobile);Posture(s,CommandKind.StandFromProne); });
            cases.Add("posture_zero_speed_allows_drop_but_never_free_standing",()=>{
                var s=Clubs(PosturePolicy(0));BeginEncounter(s);Posture(s,CommandKind.DropProne);Stance(s,CombatStance.Focused);
                RejectUnchanged(s,host,IC(s,CommandKind.StandFromProne,s.Capture().Encounter.CurrentTurnId),"ZeroSpeedCannotStand");
                Require(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==0,"Rejected zero-Speed stand spent movement."); });
            cases.Add("posture_odd_speed_floor_one_can_stand_at_zero_cost",()=>{
                var s=Clubs(PosturePolicy(1,prone:true));BeginEncounter(s);Stance(s,CombatStance.Mobile);Posture(s,CommandKind.StandFromProne);
                Require(!Life(s).Prone&&TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==0,"Positive Speed1 floor-half was incorrectly rounded up or treated as Speed0."); });
            cases.Add("posture_guarded_can_remove_standing_permission_at_small_speed",()=>{
                var s=Clubs(PosturePolicy(5,prone:true));BeginEncounter(s);Stance(s);
                Require(TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),TestOnlyPolicy.ActorId)==0,"Guarded did not reduce current Speed to zero.");
                RejectUnchanged(s,host,IC(s,CommandKind.StandFromProne,s.Capture().Encounter.CurrentTurnId),"ZeroSpeedCannotStand");EndTurn(s);Stance(s);EndTurn(s);
                Stance(s,CombatStance.Mobile);Posture(s,CommandKind.StandFromProne);Require(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==2,"New stance did not restore actual standing capability."); });
            cases.Add("posture_repeated_stands_exhaust_budget_without_refunding_drops",()=>{
                var s=Clubs(PosturePolicy(prone:true));BeginEncounter(s);Stance(s,CombatStance.Mobile);Posture(s,CommandKind.StandFromProne);Posture(s,CommandKind.DropProne);Posture(s,CommandKind.StandFromProne);Posture(s,CommandKind.DropProne);
                Require(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==30,"Drop refunded prior standing cost.");
                RejectUnchanged(s,host,IC(s,CommandKind.StandFromProne,s.Capture().Encounter.CurrentTurnId),"InsufficientMovement"); });
            cases.Add("posture_paid_dash_expands_cap_without_resetting_spent_cost",()=>{
                var s=Clubs(PosturePolicy(prone:true));BeginEncounter(s);Stance(s,CombatStance.Mobile);Posture(s,CommandKind.StandFromProne);Posture(s,CommandKind.DropProne);Posture(s,CommandKind.StandFromProne);Posture(s,CommandKind.DropProne);
                EncounterCommand(s,CommandKind.EncounterDash);Posture(s,CommandKind.StandFromProne);var ledger=TestOnlyClubAttackPolicy.WalkingLedger(s.Capture());
                Require(ledger.Spent==45&&ledger.Dashes==1&&ledger.Remaining(30)==15,"Dash reset expenditure or failed to expand cap.");
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub),"ActionAlreadySpent"); });
            cases.Add("posture_standing_preserves_available_action_and_attack_uses_new_posture",()=>{
                var s=Clubs(PosturePolicy(prone:true,seed:SeedForDeath(16)));BeginEncounter(s);Stance(s,CombatStance.Aggressive);Posture(s,CommandKind.StandFromProne);HitClub(s);
                Require(s.Capture().MeleeAttacks.Single().Attack.Second==0&&TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==15,"Standing spent Action or left Prone attack penalty.");
                Posture(s,CommandKind.DropProne);Posture(s,CommandKind.StandFromProne);Require(!Life(s).Prone,"Already-spent Action prevented legal standing."); });
            cases.Add("posture_dropped_prone_changes_attack_roll_without_touching_weapon",()=>{
                var s=Clubs(PosturePolicy());BeginEncounter(s);Stance(s);Posture(s,CommandKind.DropProne);HitClub(s);
                var a=s.Capture().MeleeAttacks.Single().Attack;Require(a.Second>0&&a.Selected==Math.Min(a.First,a.Second)&&Life(s).HeldItems.Single()==TestOnlyClubAttackPolicy.ActorClub,"Voluntary drop lost equipment or Prone disadvantage."); });
            cases.Add("posture_regular_start_refreshes_only_incoming_movement",()=>{
                var p=PosturePolicy(prone:true);var s=Clubs(p);BeginEncounter(s);Stance(s,CombatStance.Mobile);Posture(s,CommandKind.StandFromProne);EndTurn(s);Stance(s);
                Require(s.Capture().ActorMovement.Single(m=>m.ActorId==TestOnlyPolicy.ActorId).Spent==15&&TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==0,"Another actor's Start reset outgoing expenditure.");
                EndTurn(s);var m=TestOnlyClubAttackPolicy.WalkingLedger(s.Capture());Require(m.Spent==0&&m.Dashes==0&&s.Capture().ActorMovement.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).TurnOrdinal==2,"Own Start did not refresh cost.");s=RestoreClub(s,p); });
            cases.Add("posture_current_guarded_speed_expires_without_rewriting_history",()=>{
                var s=Clubs(PosturePolicy(prone:true));BeginEncounter(s);Stance(s);Posture(s,CommandKind.StandFromProne);EndTurn(s);
                Require(TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),TestOnlyPolicy.ActorId)==25,"Guarded expired before next own Start.");Stance(s);EndTurn(s);
                Require(TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),TestOnlyPolicy.ActorId)==30&&s.Capture().ActorMovement.Single(m=>m.ActorId==TestOnlyPolicy.ActorId).BaseWalkingSpeed==30,"Expiry permanently changed base Speed."); });
            cases.Add("posture_injury_and_critical_speed_penalties_apply_once",()=>{
                // Pure speed projection over explicit legal life facts; not an admitted mutation of this fixture.
                var v=PosturePolicy().Initial();var before=v.Lives.Single(l=>l.ActorId==TestOnlyPolicy.ActorId);
                v.Lives=v.Lives.Select(l=>l==before?new ActorLifeRecord(l.ActorId,26,2,0,new[]{3,3,0},false,false,true,0,0,null,0,false,l.HeldItems):l).ToArray();
                Require(TestOnlyClubAttackPolicy.WalkingSpeed(v,TestOnlyPolicy.ActorId)==15,"Duplicate Mobility injury stacked or Critical penalty missing."); });
            cases.Add("posture_knockout_freezes_choices_and_unconscious_cannot_stand",()=>{
                var p=PosturePolicy(seed:SeedForDeath(16),companionHp:1);var s=Clubs(p);BeginEncounter(s);Stance(s);HitClub(s,AttackKnockoutMode.AskIfEligible);
                RejectUnchanged(s,host,IC(s,CommandKind.DropProne,s.Capture().Encounter.CurrentTurnId),"KnockoutChoicePending");ChooseKnockout(s,true);EndTurn(s);var e=s.Capture().Encounter;
                RejectUnchanged(s,host,IC(s,CommandKind.StandFromProne,e.CurrentTurnId,actor:e.CurrentActor),"ActorCannotAct");
                Require(TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(),e.CurrentActor)==0&&TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent==0,"Unconscious actor gained movement.");EndTurn(s); });
            cases.Add("posture_restore_rejects_erased_expenditure_and_changed_base_speed",()=>{
                var p=PosturePolicy(prone:true);var s=Clubs(p);BeginEncounter(s);Stance(s);Posture(s,CommandKind.StandFromProne);var v=s.Capture();
                v.ActorMovement=v.ActorMovement.Select(m=>m.ActorId==TestOnlyPolicy.ActorId?new ActorMovementRecord(m.ActorId,m.BaseWalkingSpeed,m.TurnOrdinal):m).ToArray();
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                v=s.Capture();v.ActorMovement=v.ActorMovement.Select(m=>new ActorMovementRecord(m.ActorId,m.BaseWalkingSpeed+1,m.TurnOrdinal,m.Spent)).ToArray();
                Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory)); });
            cases.Add("posture_restore_rejects_unrecorded_position_and_posture_changes",()=>{
                var p=PosturePolicy();var v=p.Initial();v.Actors[0].X=2;Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory));
                v=p.Initial();var l=v.Lives[0];v.Lives[0]=new ActorLifeRecord(l.ActorId,l.MaximumHp,l.Hp,l.TemporaryHp,l.LinkedInjuries,l.Stable,l.Dead,l.UsesDeathSaves,l.DeathSuccesses,l.DeathFailures,l.StableUntil,l.LastDeathTurn,true,l.HeldItems);
                Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory)); });
            cases.Add("posture_duplicate_retry_and_revoked_actor_authority_preserve_budget",()=>{
                var p=PosturePolicy(prone:true);var s=Clubs(p);BeginEncounter(s);Stance(s);var c=IC(s,CommandKind.StandFromProne,s.Capture().Encounter.CurrentTurnId);CommitI(s,c);byte[] bytes=Bytes(s);
                s=RestoreClub(s,p);Require(s.Execute(host,c).Outcome==Outcome.Duplicate&&bytes.SequenceEqual(Bytes(s)),"Stand retry charged movement twice.");
                RejectUnchanged(s,new Authority(host.Principal,Array.Empty<string>()),c,"NotAuthorized"); });
            cases.Add("posture_rejects_wrong_turn_state_and_payload_without_spending",()=>{
                var s=Clubs(PosturePolicy());BeginEncounter(s);Stance(s);RejectUnchanged(s,host,IC(s,CommandKind.StandFromProne,s.Capture().Encounter.CurrentTurnId),"ActorNotProne");
                RejectUnchanged(s,host,IC(s,CommandKind.DropProne,"old.turn"),"WrongRegularTurn");Posture(s,CommandKind.DropProne);
                RejectUnchanged(s,host,IC(s,CommandKind.DropProne,s.Capture().Encounter.CurrentTurnId),"ActorAlreadyProne");
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.StandFromProne),"UnexpectedCombatPayload");
                RejectUnchanged(s,host,IC(s,CommandKind.Move,x:1),"ClubCommandNotImplemented"); });
            cases.Add("posture_save_restore_retains_spending_and_preserves_schema_boundary",()=>{
                var p=PosturePolicy(prone:true);var s=Clubs(p);BeginEncounter(s);Stance(s);Posture(s,CommandKind.StandFromProne);
                string path=Path.Combine(directory,"posture.bin");var store=new FileSaveStore();store.Save(path,s.Capture());var restored=new Simulation(p,store.Load(path),ExecutionProfile.Laboratory);
                Require(Bytes(restored).SequenceEqual(Bytes(s))&&TestOnlyClubAttackPolicy.WalkingLedger(restored.Capture()).Spent==12,"Saved standing cost lost.");
                Throws<InvalidDataException>(()=>store.Save(path,new TestOnlyClubAttackPolicy().Initial()));Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release)); });
            cases.Add("posture_codec_counts_future_schema_and_legacy_fields_reject",()=>{
                var p=PosturePolicy();var v=p.Initial();var legacy=v.Copy();legacy.SchemaVersion=9;legacy.ActorMovement=Array.Empty<ActorMovementRecord>();int offset=codec.Encode(legacy).Length-32;
                foreach(int count in new[]{-1,65,int.MaxValue}){byte[] bad=codec.Encode(v);Array.Copy(BitConverter.GetBytes(count),0,bad,offset,4);Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));}
                v.SchemaVersion=9;Throws<ArgumentException>(()=>codec.Encode(v));byte[] future=codec.Encode(p.Initial());future[4]=12;Resign(future);Throws<InvalidDataException>(()=>codec.Decode(future)); });
        }
    }
}
#endif
