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
        private static Simulation Living(TestOnlyActorLifePolicy p)=>new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);
        private static ActorLifeRecord Life(Simulation s,string actor=TestOnlyPolicy.ActorId)=>s.Capture().Lives.Single(x=>x.ActorId==actor);
        private static uint SeedForDeath(int natural){for(uint i=1;i<10000;i++)if(PlaytestDice.RollD20(i).Natural==natural)return i;throw new Exception("No fixture seed.");}
        private static Simulation RestoreLife(Simulation s,TestOnlyActorLifePolicy p)=>new Simulation(p,new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);
        private static void AddActorLifeCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlyFillingPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("actor_life_records_roundtrip_numerical_profiles_and_detach_collections",()=>{
                var p=new TestOnlyActorLifePolicy();var s=Living(p);var v=s.Capture();var c=v.Characters[0];
                Require(v.SchemaVersion==8&&v.Characters.Length==2&&c.Abilities.SequenceEqual(new[]{10,10,10,10,10,10})&&Life(s).MaximumHp==26,"Wrong numeric facts.");
                Throws<NotSupportedException>(()=>((IList<int>)c.Abilities)[0]=99);Throws<NotSupportedException>(()=>((IList<CharacterLevelFact>)c.Levels)[0]=new CharacterLevelFact("Mage",6));
                v.Lives=Array.Empty<ActorLifeRecord>();Require(s.Capture().Lives.Length==2,"Capture exposed owned arrays.");
                Require(Bytes(s).SequenceEqual(Bytes(RestoreLife(s,p))),"Actor records changed through codec."); });
            cases.Add("actor_life_preserves_temporary_hp_and_linked_injury_identity",()=>{
                var injuries=new[]{Injury.Concussion,Injury.None,Injury.Concussion};
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,7,5,injuries));var s=Living(p);injuries[0]=Injury.MobilityTrauma;
                BeginEncounter(s);EndTurn(s);s=RestoreLife(s,p);var life=Life(s);
                Require(life.Hp==7&&life.TemporaryHp==5&&life.LinkedInjuries.SequenceEqual(new[]{1,0,1})&&ActorLifeRules.Read(life).Critical
                    &&s.Capture().LifeEvents.Length==0&&s.Capture().RandomState==1,"Life persistence changed linked Wounds, buffered HP or consumed an unnecessary die."); });
            cases.Add("actor_life_decoder_bounds_new_collection_counts",()=>{
                var p=new TestOnlyActorLifePolicy();var v=p.Initial();var legacy=v.Copy();legacy.SchemaVersion=7;
                legacy.Characters=Array.Empty<ActorCharacterRecord>();legacy.Lives=Array.Empty<ActorLifeRecord>();
                int offset=codec.Encode(legacy).Length-32;byte[] bytes=codec.Encode(v);
                foreach(int count in new[]{-1,65,int.MaxValue}) {var bad=(byte[])bytes.Clone();Array.Copy(BitConverter.GetBytes(count),0,bad,offset,4);Resign(bad);
                    Throws<InvalidDataException>(()=>codec.Decode(bad));} });
            cases.Add("actor_life_first_start_rolls_once_before_voluntary_decisions",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0),seed:1);var s=Living(p);BeginEncounter(s);
                var e=s.Capture().LifeEvents.Single();Require(e.Natural==9&&e.WordsConsumed==1&&e.RecoveryD4==0&&e.At==T(0)
                    &&Life(s).DeathFailures==1&&Life(s).LastDeathTurn==1,"First Start did not own exactly one required d20.");
                RejectUnchanged(s,host,IC(s,CommandKind.EncounterDash,s.Capture().Encounter.CurrentTurnId),"ActorCannotAct");
                EndTurn(s);Require(s.Capture().LifeEvents.Length==1&&s.Capture().RuleClock==T(3),"Other actor's Start repeated death save."); });
            cases.Add("actor_life_natural_twenty_recovers_hp_but_retains_prone",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0,deathFailures:2),seed:SeedForDeath(20));var s=Living(p);BeginEncounter(s);
                var e=s.Capture().LifeEvents.Single();Require(Life(s).Hp==1&&Life(s).Prone&&!ActorLifeRules.ZeroHpUnconscious(s.Capture(),TestOnlyPolicy.ActorId)
                    &&Life(s).DeathFailures==0&&e.RecoveryD4==0&&e.WordsConsumed==1,"Natural20 rerolled recovery, retained unconsciousness or stood up.");
                EncounterCommand(s,CommandKind.EncounterDash);s=RestoreLife(s,p);Require(Life(s).Prone&&FixedEncounterRules.ActionSpent(s.Capture()),"Restore lost posture/spending."); });
            cases.Add("actor_life_third_success_draws_one_d4_and_preserves_fractional_start",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0,deathSuccesses:2),origin:T(1,3),seed:SeedForDeath(10));var s=Living(p);BeginEncounter(s);
                var e=s.Capture().LifeEvents.Single();Require(e.Natural==10&&e.RecoveryD4>=1&&e.RecoveryD4<=4&&e.WordsConsumed==2
                    &&Life(s).StableUntil==T(1,3).AddSeconds(e.RecoveryD4*3600L)&&Life(s).DeathSuccesses==0,"Stable transition lost conditional draw or phase.");
                EndTurn(s);EndTurn(s);Require(s.Capture().LifeEvents.Length==1,"Stable actor made a death save.");s=RestoreLife(s,p); });
            cases.Add("actor_life_natural_one_can_kill_without_blocking_slot_progression",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0,deathFailures:1),seed:SeedForDeath(1));var s=Living(p);BeginEncounter(s);
                Require(Life(s).Dead&&Life(s).DeathFailures==3&&!ActorLifeRules.ZeroHpUnconscious(s.Capture(),TestOnlyPolicy.ActorId),"Natural1 did not resolve fatal counter.");
                EndTurn(s);EndTurn(s);Require(s.Capture().RuleClock==T(6)&&s.Capture().LifeEvents.Length==1,"Dead actor lost slot or rolled again.");
                RejectUnchanged(s,host,IC(s,CommandKind.EncounterDash,s.Capture().Encounter.CurrentTurnId),"ActorCannotAct"); });
            cases.Add("actor_life_stable_recovery_occurs_inside_slot_for_nonroster_actor",()=>{
                var p=new TestOnlyActorLifePolicy(companionLife:new LifeState(26,0,stable:true,stableUntil:T(1,3)),resolvedOrder:new[]{TestOnlyPolicy.ActorId});var s=Living(p);
                BeginEncounter(s);uint random=s.Capture().RandomState;EndTurn(s);var e=s.Capture().LifeEvents.Single();
                Require(e.ActorId==TestOnlyPolicy.CompanionId&&e.At==T(1,3)&&e.Kind==LifeEventKind.StableRecovery&&e.WordsConsumed==0
                    &&s.Capture().RuleClock==T(6)&&Life(s,TestOnlyPolicy.CompanionId).Hp==1&&s.Capture().RandomState==random,"Off-roster recovery waited for a turn."); });
            cases.Add("actor_life_exact_incoming_start_recovery_precedes_death_save",()=>{
                var p=new TestOnlyActorLifePolicy(companionLife:new LifeState(26,0,stable:true,stableUntil:T(3)));var s=Living(p);BeginEncounter(s);EndTurn(s);
                Require(s.Capture().LifeEvents.Single().Kind==LifeEventKind.StableRecovery&&Life(s,TestOnlyPolicy.CompanionId).Hp==1
                    &&Life(s,TestOnlyPolicy.CompanionId).LastDeathTurn==0&&s.Capture().RandomState==1,"Incoming boundary rolled before due recovery."); });
            cases.Add("actor_life_simultaneous_recovery_is_deterministic_and_keeps_prone",()=>{
                var stable=new LifeState(26,0,stable:true,stableUntil:T(4,3));var p=new TestOnlyActorLifePolicy(stable,stable);var s=Living(p);BeginEncounter(s);EndTurn(s);
                Require(s.Capture().LifeEvents.Select(e=>e.ActorId).SequenceEqual(new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId})
                    &&s.Capture().Lives.All(l=>l.Hp==1&&l.Prone)&&s.Capture().RandomState==1,"Simultaneous recovery reordered, rolled or stood actors up.");s=RestoreLife(s,p); });
            cases.Add("actor_life_clock_progresses_when_every_actor_is_stable_or_dead",()=>{
                var p=new TestOnlyActorLifePolicy(new LifeState(26,0,stable:true,stableUntil:T(7,3)),new LifeState(26,0,dead:true,usesDeathSaves:false));var s=Living(p);
                AdvanceI(s,3);Require(Life(s).Hp==1&&Life(s).Prone&&Life(s,TestOnlyPolicy.CompanionId).Dead,"Incapable host actors prevented elapsed recovery.");
                s=RestoreLife(s,p);AdvanceI(s,10);Require(s.Capture().LifeEvents.Length==1,"Clock repeated a recovered deadline."); });
            cases.Add("actor_life_background_planting_and_recovery_share_exact_milestone",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0,stable:true,stableUntil:T(3600)),resolvedOrder:new[]{TestOnlyPolicy.ActorId});var s=Living(p);
                CommitI(s,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId));AdvanceI(s,3597);BeginEncounter(s);EndTurn(s);
                Require(Crop(s).Growth==T(3)&&Life(s).Hp==1&&s.Capture().LifeEvents.Single().At==T(3600)&&s.Capture().RuleClock==T(3603),"Independent work/recovery drifted.");s=RestoreLife(s,p); });
            cases.Add("actor_life_incapable_worker_rejects_without_resources_or_rng",()=>{
                var p=new TestOnlyActorLifePolicy(companionLife:new LifeState(26,0));var s=Living(p);
                RejectUnchanged(s,host,IC(s,CommandKind.PlantCrop,CropId,actor:TestOnlyPolicy.CompanionId),"ActorCannotAct");
                Require(s.Capture().Work.Reservations.Count==0&&s.Capture().RandomState==1,"Rejected labor spent inputs or dice."); });
            cases.Add("actor_life_empty_hands_is_preserved_by_explicit_command_gates",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0));var s=Living(p);var v=s.Capture();
                Require(v.Lives.All(l=>l.HeldItems.Count==0)&&v.Vessels.Any(x=>x.LocationId==TestOnlyPolicy.ActorId),"Carried stock was confused with held items.");
                RejectUnchanged(s,host,IC(s,CommandKind.HandleVessel,TestOnlyFillingPolicy.ActorSkinId,new InventoryRequest(Q(1),handling:HandlingKind.Drop)),"ActorLifeCommandNotImplemented");
                RejectUnchanged(s,host,IC(s,CommandKind.StartIntake,TestOnlyInventoryPolicy.FoodId,new InventoryRequest(Q(1))),"ActorLifeCommandNotImplemented"); });
            cases.Add("actor_life_rejection_retry_and_revoked_authority_preserve_death_draw",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0));var s=Living(p);var begin=IC(s,CommandKind.BeginFixedEncounter);CommitI(s,begin);var bytes=Bytes(s);
                Require(s.Execute(host,begin).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(bytes),"Entry retry consumed another die.");
                var revoked=new Authority(host.Principal,new[]{TestOnlyPolicy.CompanionId},true,true);RejectUnchanged(s,revoked,begin,"NotAuthorized");
                RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,"wrong-turn"),"WrongRegularTurn"); });
            cases.Add("actor_life_replay_rejects_forged_rng_and_missing_events",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0));var s=Living(p);BeginEncounter(s);
                var v=s.Capture();v.RandomState=1;Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                v=s.Capture();v.LifeEvents=Array.Empty<ActorLifeEvent>();Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("actor_life_replay_rejects_forged_counter_posture_and_deadline",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0,stable:true,stableUntil:T(10,3)));var s=Living(p);AdvanceI(s,1);
                foreach(int forged in new[]{0,1,2}) {var v=s.Capture();var l=v.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId);
                    v.Lives=v.Lives.Select(x=>x.ActorId!=l.ActorId?x:new ActorLifeRecord(l.ActorId,26,forged==0?1:0,0,Array.Empty<int>(),forged!=0,false,true,0,0,
                        forged==0?null:forged==1?T(11,3):l.StableUntil,0,forged!=2,Array.Empty<string>())).ToArray();
                    Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));} });
            cases.Add("actor_life_profile_ledger_and_fingerprint_mismatch_reject",()=>{
                var p=new TestOnlyActorLifePolicy();var s=Living(p);var v=s.Capture();var c=v.Characters[0];
                v.Characters[0]=new ActorCharacterRecord(c.ActorId,c.ProfileId,new[]{18,10,10,10,10,10},c.Levels);
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                Throws<ArgumentException>(()=>new Simulation(new TestOnlyActorLifePolicy(seed:2),codec.Decode(Bytes(s)),ExecutionProfile.Laboratory));
                Throws<ArgumentException>(()=>new TestOnlyActorLifePolicy(actorLife:new LifeState(27,27)));
                Throws<ArgumentException>(()=>new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0,stable:true,stableUntil:T(0)))); });
            cases.Add("actor_life_save_resume_draws_same_next_death_result",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0));var uninterrupted=Living(p);BeginEncounter(uninterrupted);var resumed=RestoreLife(uninterrupted,p);
                EndTurn(uninterrupted);EndTurn(uninterrupted);EndTurn(resumed);EndTurn(resumed);
                Require(Bytes(uninterrupted).SequenceEqual(Bytes(resumed))&&Life(resumed).LastDeathTurn==3,"Restore changed next required roll or marker."); });
            cases.Add("actor_life_save_backup_preserves_exact_recovery_and_schema",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0,stable:true,stableUntil:T(10,3)));var s=Living(p);string path=Path.Combine(directory,"actor-life.ddsave");var store=new FileSaveStore();
                store.Save(path,s.Capture());AdvanceI(s,4);store.Save(path,s.Capture());s=new Simulation(p,store.Load(path),ExecutionProfile.Laboratory);
                Require(Life(s).Hp==1&&store.Load(path+".bak").Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).StableUntil==T(10,3),"Backup lost exact unrecovered state.");
                Throws<InvalidDataException>(()=>store.Save(path,new TestOnlyEncounterPolicy().Initial())); });
            cases.Add("actor_life_release_legacy_fields_and_future_schema_reject",()=>{
                var p=new TestOnlyActorLifePolicy();Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                var v=p.Initial();v.SchemaVersion=7;Throws<ArgumentException>(()=>codec.Encode(v));
                byte[] bad=codec.Encode(p.Initial());bad[4]=9;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad)); });
            cases.Add("actor_life_history_rejects_incapable_dash_before_later_recovery",()=>{
                var stable=new LifeState(26,0,stable:true,stableUntil:T(3));var p=new TestOnlyActorLifePolicy(actorLife:stable);
                var template=Living(new TestOnlyActorLifePolicy());BeginEncounter(template);EncounterCommand(template,CommandKind.EncounterDash);EndTurn(template);EndTurn(template);
                var actual=Living(p);BeginEncounter(actual);EndTurn(actual);EndTurn(actual);
                var forged=template.Capture();var correct=actual.Capture();forged.ContentFingerprint=p.ContentFingerprint;forged.Lives=correct.Lives;
                var e=correct.LifeEvents.Single();forged.LifeEvents=new[]{new ActorLifeEvent(e.ActorId,3,e.At,e.Kind,e.TurnOrdinal,e.Natural,e.RecoveryD4,e.RandomBefore,e.RandomAfter,e.WordsConsumed)};
                Require(forged.Lives.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).Hp==1,"Fixture did not reach later recovery.");
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(forged)),ExecutionProfile.Laboratory)); });
            cases.Add("actor_life_history_rejects_encounter_before_fixture_origin",()=>{
                var template=Living(new TestOnlyActorLifePolicy());BeginEncounter(template);EndTurn(template);
                var p=new TestOnlyActorLifePolicy(origin:T(1));var forged=template.Capture();forged.ContentFingerprint=p.ContentFingerprint;
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(forged)),ExecutionProfile.Laboratory)); });
            cases.Add("actor_life_recovery_revision_must_cross_actual_deadline",()=>{
                var p=new TestOnlyActorLifePolicy(actorLife:new LifeState(26,0,stable:true,stableUntil:T(10)));var s=Living(p);AdvanceI(s,1);AdvanceI(s,9);
                var v=s.Capture();var e=v.LifeEvents.Single();Require(e.Revision==2&&e.At==T(10),"Fixture failed to recover in second command.");
                v.LifeEvents=new[]{new ActorLifeEvent(e.ActorId,1,e.At,e.Kind,e.TurnOrdinal,e.Natural,e.RecoveryD4,e.RandomBefore,e.RandomAfter,e.WordsConsumed)};
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("actor_life_replay_rejects_missing_clock_receipt_and_forged_elapsed_time",()=>{
                var p=new TestOnlyActorLifePolicy();var s=Living(p);AdvanceI(s,1);AdvanceI(s,9);var v=s.Capture();
                v.Receipts=v.Receipts.Skip(1).ToArray();Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));
                v=s.Capture();v.RuleClock=T(11);Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
        }
    }
}
#endif
