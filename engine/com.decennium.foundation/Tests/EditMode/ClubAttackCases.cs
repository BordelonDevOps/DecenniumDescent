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
        private static Simulation Clubs(TestOnlyClubAttackPolicy p=null){p=p??new TestOnlyClubAttackPolicy();return new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);}
        private static Command ClubCommand(Simulation s,CommandKind kind,string target="",int stance=0,AttackKnockoutMode knockout=AttackKnockoutMode.OrdinaryOutcome,bool choice=false,string weapon=null,string actor=null)
        {
            var v=s.Capture();actor=actor??v.Encounter.CurrentActor;
            if(kind==CommandKind.AttackClub){target=target==""?(actor==TestOnlyPolicy.ActorId?TestOnlyPolicy.CompanionId:TestOnlyPolicy.ActorId):target;weapon=weapon??(actor==TestOnlyPolicy.ActorId?TestOnlyClubAttackPolicy.ActorClub:TestOnlyClubAttackPolicy.CompanionClub);}
            return new Command("club.command."+(v.Revision+1),actor,v.Revision,kind,target,combat:new CombatRequest(v.Encounter.CurrentTurnId,weapon??"",stance,knockout,choice));
        }
        private static void Stance(Simulation s,CombatStance stance=CombatStance.Guarded)=>CommitI(s,ClubCommand(s,CommandKind.SelectCombatStance,stance:(int)stance));
        private static void HitClub(Simulation s,AttackKnockoutMode knockout=AttackKnockoutMode.OrdinaryOutcome)=>CommitI(s,ClubCommand(s,CommandKind.AttackClub,knockout:knockout));
        private static Simulation RestoreClub(Simulation s,TestOnlyClubAttackPolicy p)=>new Simulation(p,new SnapshotCodec().Decode(Bytes(s)),ExecutionProfile.Laboratory);
        private static Simulation PendingClub(out TestOnlyClubAttackPolicy p)
        {p=new TestOnlyClubAttackPolicy(companionHp:1,seed:SeedForDeath(16),origin:T(1,3));var s=Clubs(p);BeginEncounter(s);Stance(s);HitClub(s,AttackKnockoutMode.AskIfEligible);Require(s.Capture().MeleeAttacks.Single().Pending,"Fixture did not offer knockout.");return s;}
        private static void ChooseKnockout(Simulation s,bool yes)=>CommitI(s,ClubCommand(s,CommandKind.ResolveKnockout,s.Capture().MeleeAttacks.Single(a=>a.Pending).Id,choice:yes));
        private static void AddClubAttackCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlyFillingPolicy.Host();var codec=new SnapshotCodec();
            cases.Add("club_initial_equipment_and_numeric_profile_are_explicit",()=>{
                var p=new TestOnlyClubAttackPolicy();var s=Clubs(p);var v=s.Capture();
                Require(v.SchemaVersion==9&&v.Clubs.Length==2&&v.Actors.Single(a=>a.Id==TestOnlyPolicy.ActorId).X==0
                    &&v.Lives.All(l=>l.HeldItems.Count==1&&v.Clubs.Single(w=>w.HeldBy==l.ActorId).Id==l.HeldItems.Single())
                    &&TestOnlyInventoryPolicy.CarriedBurden(v,TestOnlyPolicy.ActorId).Pounds==Q(10),"Physical Club/weight/hands facts missing.");
                Require(Bytes(s).SequenceEqual(Bytes(RestoreClub(s,p))),"Initial equipment changed through codec."); });
            cases.Add("club_requires_own_stance_before_attack_and_conscious_end",()=>{
                var s=Clubs();BeginEncounter(s);
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub),"StanceRequired");
                RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,s.Capture().Encounter.CurrentTurnId),"StanceRequired");
                Stance(s);RejectUnchanged(s,host,ClubCommand(s,CommandKind.SelectCombatStance,stance:1),"StanceAlreadySelected");EndTurn(s); });
            cases.Add("club_no_encounter_wide_default_stance_before_first_turn",()=>{
                var s=Clubs(new TestOnlyClubAttackPolicy(seed:SeedForDeath(16)));BeginEncounter(s);Stance(s,CombatStance.Aggressive);HitClub(s);
                Require(TestOnlyClubAttackPolicy.ActiveStance(s.Capture(),TestOnlyPolicy.CompanionId)==null&&s.Capture().MeleeAttacks.Single().Attack.ArmorClass==10,"Defender received an automatic stance."); });
            cases.Add("club_stance_expires_at_exact_next_own_start",()=>{
                var p=new TestOnlyClubAttackPolicy(seed:SeedForDeath(16),origin:T(1,3));var s=Clubs(p);BeginEncounter(s);Stance(s,CombatStance.Aggressive);EndTurn(s);Stance(s);
                HitClub(s);Require(s.Capture().MeleeAttacks.Single().Attack.ArmorClass==8,"Aggressive defense did not persist into other actor's turn.");
                EndTurn(s);Require(s.Capture().RuleClock==T(19,3)&&TestOnlyClubAttackPolicy.ActiveStance(s.Capture(),TestOnlyPolicy.ActorId)==null,"Stance survived own Start.");
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub),"StanceRequired");s=RestoreClub(s,p);Stance(s,CombatStance.Mobile); });
            cases.Add("club_guarded_ac_and_nonproficient_strength_attack",()=>{
                var s=Clubs(new TestOnlyClubAttackPolicy(seed:SeedForDeath(10)));BeginEncounter(s);Stance(s);EndTurn(s);Stance(s,CombatStance.Focused);HitClub(s);
                var a=s.Capture().MeleeAttacks.Single();Require(a.Attack.ArmorClass==11&&a.Attack.Modifier==0&&!a.Attack.Hit&&a.Damage.Dice.Count==0,"Borrowed Club proficiency or ignored Guarded AC."); });
            cases.Add("club_aggressive_critical_doubles_dice_only",()=>{
                var s=Clubs(new TestOnlyClubAttackPolicy(seed:SeedForDeath(20)));BeginEncounter(s);Stance(s,CombatStance.Aggressive);HitClub(s);var a=s.Capture().MeleeAttacks.Single();
                Require(a.Attack.Critical&&a.Damage.Dice.Count==2&&a.Damage.Total==a.Damage.Dice.Sum()+2&&a.Damage.WoundNatural==0,"Critical doubled flat stance bonus or drew unnecessary Wound save."); });
            cases.Add("club_miss_pays_action_and_never_rolls_damage",()=>{
                var s=Clubs(new TestOnlyClubAttackPolicy(seed:SeedForDeath(1)));BeginEncounter(s);Stance(s);HitClub(s);var a=s.Capture().MeleeAttacks.Single();
                Require(!a.Attack.Hit&&a.Damage.Dice.Count==0&&a.Attack.RandomAfter==s.Capture().RandomState&&s.Capture().Presses.Length==0,"Miss rolled damage or armed Press.");
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub),"ActionAlreadySpent");
                RejectUnchanged(s,host,IC(s,CommandKind.EncounterDash,s.Capture().Encounter.CurrentTurnId),"ActionAlreadySpent"); });
            cases.Add("club_dash_shares_action_and_does_not_choose_stance",()=>{
                var s=Clubs();BeginEncounter(s);EncounterCommand(s,CommandKind.EncounterDash);
                RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,s.Capture().Encounter.CurrentTurnId),"StanceRequired");Stance(s);
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub),"ActionAlreadySpent");EndTurn(s);Stance(s);HitClub(s); });
            cases.Add("club_carrying_requires_actual_applicable_penalty",()=>{
                var s=Clubs();BeginEncounter(s);RejectUnchanged(s,host,ClubCommand(s,CommandKind.SelectCombatStance,stance:5),"NoApplicableCargoPenalty");
                Stance(s,CombatStance.Focused);Require(TestOnlyClubAttackPolicy.ActiveStance(s.Capture(),TestOnlyPolicy.ActorId).Kind==CombatStance.Focused,"Non-Club stance silently substituted."); });
            cases.Add("club_range_diagonal_is_five_feet_and_remote_target_rejects",()=>{
                var near=Clubs(new TestOnlyClubAttackPolicy(companionX:1,companionY:1));BeginEncounter(near);Stance(near);HitClub(near);
                var far=Clubs(new TestOnlyClubAttackPolicy(companionX:2));BeginEncounter(far);Stance(far);RejectUnchanged(far,host,ClubCommand(far,CommandKind.AttackClub),"TargetOutOfReach"); });
            cases.Add("club_legality_rejects_wrong_weapon_actor_turn_and_target_before_rng",()=>{
                var s=Clubs();BeginEncounter(s);Stance(s);
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub,weapon:TestOnlyClubAttackPolicy.CompanionClub),"ClubNotHeld");
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub,target:TestOnlyPolicy.ActorId),"InvalidLivingTarget");
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub,actor:TestOnlyPolicy.CompanionId),"WrongRegularTurn");
                var c=ClubCommand(s,CommandKind.AttackClub);RejectUnchanged(s,host,new Command(c.Id,c.Actor,c.ExpectedRevision,c.Kind,c.Target,combat:new CombatRequest("old.turn",TestOnlyClubAttackPolicy.ActorClub)),"WrongRegularTurn"); });
            cases.Add("club_prone_attack_and_target_advantage_cancel_without_extra_die",()=>{
                var p=new TestOnlyClubAttackPolicy(actorProne:true,companionProne:true,seed:SeedForDeath(16));var s=Clubs(p);BeginEncounter(s);Stance(s);HitClub(s);
                Require(s.Capture().MeleeAttacks.Single().Attack.Second==0,"Opposing Prone effects did not cancel.");
                s=Clubs(new TestOnlyClubAttackPolicy(actorProne:true));BeginEncounter(s);Stance(s);HitClub(s);var a=s.Capture().MeleeAttacks.Single().Attack;
                Require(a.Second>0&&a.Selected==Math.Min(a.First,a.Second),"Prone attacker did not use disadvantage."); });
            cases.Add("club_prone_target_advantage_does_not_automatically_critical",()=>{
                uint seed=1;while(PlaytestDice.RollD20(seed,1).Natural<10||PlaytestDice.RollD20(seed,1).Natural==20)seed++;
                var s=Clubs(new TestOnlyClubAttackPolicy(companionProne:true,seed:seed));BeginEncounter(s);Stance(s);HitClub(s);var a=s.Capture().MeleeAttacks.Single().Attack;
                Require(a.Second>0&&a.Selected==Math.Max(a.First,a.Second)&&a.Hit&&!a.Critical,"Prone target was treated as Unconscious."); });
            cases.Add("club_hit_arms_press_even_when_temporary_hp_absorbs_everything",()=>{
                var s=Clubs(new TestOnlyClubAttackPolicy(companionTemporaryHp:100,seed:SeedForDeath(16)));BeginEncounter(s);Stance(s);HitClub(s);var v=s.Capture();
                Require(Life(s,TestOnlyPolicy.CompanionId).Hp==26&&TestOnlyClubAttackPolicy.ActivePress(v,TestOnlyPolicy.ActorId)?.TargetId==TestOnlyPolicy.CompanionId,"Temp HP erased a melee-hit entitlement.");
                EndTurn(s);Stance(s);EndTurn(s);Require(TestOnlyClubAttackPolicy.ActivePress(s.Capture(),TestOnlyPolicy.ActorId)==null,"Press survived next own Start."); });
            cases.Add("club_zero_hp_drops_only_held_item_and_preserves_title",()=>{
                var s=Clubs(new TestOnlyClubAttackPolicy(companionHp:1,seed:SeedForDeath(16)));BeginEncounter(s);Stance(s);HitClub(s,AttackKnockoutMode.KnockOutIfEligible);
                var v=s.Capture();var l=Life(s,TestOnlyPolicy.CompanionId);var w=v.Clubs.Single(x=>x.Id==TestOnlyClubAttackPolicy.CompanionClub);
                Require(l.Hp==0&&l.Stable&&l.Prone&&l.HeldItems.Count==0&&w.HeldBy==""&&w.OwnerId==TestOnlyPolicy.CompanionId&&w.CustodianId==TestOnlyPolicy.CompanionId
                    &&w.CellX==1&&w.CellY==0&&v.Vessels.Any(x=>x.LocationId==TestOnlyPolicy.CompanionId)&&TestOnlyInventoryPolicy.CarriedBurden(v,TestOnlyPolicy.CompanionId).Pounds==Q(2),"Unconsciousness lost custody/title or dropped carried vessels."); });
            cases.Add("club_knockout_deadline_keeps_fractional_attack_instant",()=>{
                var s=PendingClub(out var p);ChooseKnockout(s,true);var a=s.Capture().MeleeAttacks.Single();
                Require(Life(s,TestOnlyPolicy.CompanionId).StableUntil==T(1,3).AddSeconds(3600L*a.Damage.StableD4)&&a.Damage.StableD4>0,"Knockout rounded exact recovery.");s=RestoreClub(s,p); });
            cases.Add("club_pending_choice_preserves_paid_rolls_and_freezes_other_commands",()=>{
                var s=PendingClub(out var p);var v=s.Capture();Require(Life(s,TestOnlyPolicy.CompanionId).Hp==1&&Life(s,TestOnlyPolicy.CompanionId).HeldItems.Count==1&&TestOnlyClubAttackPolicy.ActionSpent(v),"Pending choice applied provisional life or lost Action.");
                RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,v.Encounter.CurrentTurnId),"KnockoutChoicePending");
                RejectUnchanged(s,host,IC(s,CommandKind.AdvanceClock,x:1,y:1),"KnockoutChoicePending");
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub),"KnockoutChoicePending");s=RestoreClub(s,p);Require(Bytes(s).SequenceEqual(codec.Encode(v)),"Pending save changed outcomes."); });
            cases.Add("club_late_knockout_equals_conditional_early_instruction",()=>{
                var late=PendingClub(out var p);uint paid=late.Capture().RandomState;var before=late.Capture().MeleeAttacks.Single();ChooseKnockout(late,true);
                var early=Clubs(p);BeginEncounter(early);Stance(early);HitClub(early,AttackKnockoutMode.KnockOutIfEligible);
                var result=late.Capture().MeleeAttacks.Single();Require(Life(late,TestOnlyPolicy.CompanionId).SameAs(Life(early,TestOnlyPolicy.CompanionId))&&late.Capture().RandomState==early.Capture().RandomState
                    &&result.Attack.SameAs(before.Attack)&&result.Damage.WoundNatural==before.Damage.WoundNatural&&result.Damage.InjuryD6==before.Damage.InjuryD6
                    &&result.Damage.StableD4==DiceStream.Draw(paid,4).Value+1&&result.ResolvedRevision==4&&result.Revision==3,"Post-roll choice rerolled, repaid or changed outcome."); });
            cases.Add("club_declining_knockout_consumes_no_additional_randomness",()=>{
                var s=PendingClub(out var p);uint paid=s.Capture().RandomState;ChooseKnockout(s,false);
                Require(s.Capture().RandomState==paid&&Life(s,TestOnlyPolicy.CompanionId).Hp==0&&!Life(s,TestOnlyPolicy.CompanionId).Stable&&s.Capture().MeleeAttacks.Single().Damage.StableD4==0,"Decline consumed recovery die or left pending life.");
                s=RestoreClub(s,p);EndTurn(s);Require(s.Capture().LifeEvents.Length==1,"Incoming dying actor did not roll automatic death save."); });
            cases.Add("club_choice_authority_and_duplicate_retry_do_not_reroll",()=>{
                var s=PendingClub(out var p);string id=s.Capture().MeleeAttacks.Single().Id;
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.ResolveKnockout,id,choice:true,actor:TestOnlyPolicy.CompanionId),"InvalidKnockoutChoice");
                var c=ClubCommand(s,CommandKind.ResolveKnockout,id,choice:true);CommitI(s,c);byte[] bytes=Bytes(s);
                Require(s.Execute(host,c).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(bytes),"Retry repeated choice/d4.");
                RejectUnchanged(s,new Authority(host.Principal,Array.Empty<string>()),c,"NotAuthorized");
                var conflict=new Command(c.Id,c.Actor,c.ExpectedRevision,c.Kind,c.Target,combat:new CombatRequest(c.Combat.TurnId,choice:false));RejectUnchanged(s,host,conflict,"CommandIdConflict");s=RestoreClub(s,p); });
            cases.Add("club_attack_retry_keeps_pending_stage_and_all_prior_draws",()=>{
                var p=new TestOnlyClubAttackPolicy(companionHp:1,seed:SeedForDeath(16));var s=Clubs(p);BeginEncounter(s);Stance(s);var c=ClubCommand(s,CommandKind.AttackClub,knockout:AttackKnockoutMode.AskIfEligible);CommitI(s,c);
                byte[] bytes=Bytes(s);s=RestoreClub(s,p);Require(s.Execute(host,c).Outcome==Outcome.Duplicate&&Bytes(s).SequenceEqual(bytes),"Pending attack retry charged Action/RNG twice."); });
            cases.Add("club_current_weapon_permission_applies_before_attack_and_duplicate",()=>{
                var s=Clubs(new TestOnlyClubAttackPolicy(companionHp:1,seed:SeedForDeath(16)));BeginEncounter(s);Stance(s);
                var restricted=new Authority(host.Principal,new[]{TestOnlyPolicy.ActorId});var c=ClubCommand(s,CommandKind.AttackClub,knockout:AttackKnockoutMode.AskIfEligible);
                RejectUnchanged(s,restricted,c,"InventoryNotAuthorized");CommitI(s,c);RejectUnchanged(s,restricted,c,"InventoryNotAuthorized");
                var choice=ClubCommand(s,CommandKind.ResolveKnockout,s.Capture().MeleeAttacks.Single().Id,choice:true);
                Require(s.Execute(restricted,choice).Outcome==Outcome.Committed,"Weapon permission revocation stranded the attacker's already-paid choice."); });
            cases.Add("club_restore_preserves_chronological_life_event_order",()=>{
                uint seed=0;
                for(uint i=1;i<10000;i++){var a=PlaytestDice.RollD20(i);if(a.Natural<10||a.Natural==20)continue;var d=DiceStream.Draw(a.NextRandomState,4);
                    var damage=PlaytestDamageDice.Resolve(new LifeState(26,1),d.Value+1,T(0),d.NextState,melee:true);
                    var first=PlaytestDice.RollD20(damage.NextRandomState);if(first.Natural>1&&first.Natural<20){seed=i;break;}}
                var p=new TestOnlyClubAttackPolicy(companionHp:1,seed:seed);var s=Clubs(p);BeginEncounter(s);Stance(s);HitClub(s);EndTurn(s);EndTurn(s);Stance(s);EndTurn(s);
                var v=s.Capture();Require(v.LifeEvents.Length==2,"Fixture did not record two life events.");v.LifeEvents=v.LifeEvents.Reverse().ToArray();
                Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); });
            cases.Add("club_unconscious_slot_requires_no_default_stance",()=>{
                var s=Clubs(new TestOnlyClubAttackPolicy(companionHp:1,seed:SeedForDeath(16)));BeginEncounter(s);Stance(s);HitClub(s,AttackKnockoutMode.KnockOutIfEligible);EndTurn(s);
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.SelectCombatStance,stance:2),"ActorCannotAct");EndTurn(s);
                Require(s.Capture().RuleClock==T(6)&&s.Capture().Stances.Length==1,"Unconscious actor stopped the round or received a default stance."); });
            cases.Add("club_unconscious_hit_is_critical_and_adds_two_death_failures",()=>{
                // Find a seed whose first hit knocks out, then whose advantage attack hits on round two.
                uint seed=0;
                for(uint i=1;i<10000;i++) {var a=PlaytestDice.RollD20(i);if(a.Natural<10||a.Natural==20)continue;var d=DiceStream.Draw(a.NextRandomState,4);
                    var damage=PlaytestDamageDice.Resolve(new LifeState(26,1),d.Value+1,T(0),d.NextState,melee:true,knockout:KnockoutInstruction.KnockOutIfEligible);
                    var second=PlaytestDice.RollD20(damage.NextRandomState,1);if(second.Natural>=10&&second.Natural<20){seed=i;break;}}
                Require(seed!=0,"No sequence seed.");var s=Clubs(new TestOnlyClubAttackPolicy(companionHp:1,seed:seed));BeginEncounter(s);Stance(s);HitClub(s,AttackKnockoutMode.KnockOutIfEligible);EndTurn(s);EndTurn(s);Stance(s);HitClub(s);
                var last=s.Capture().MeleeAttacks.Last();Require(last.Attack.Selected!=20&&last.Attack.Critical&&last.Damage.Dice.Count==2
                    &&Life(s,TestOnlyPolicy.CompanionId).DeathFailures==2&&!Life(s,TestOnlyPolicy.CompanionId).Stable,"Unconscious hit lost critical or stable-ending damage."); });
            cases.Add("club_natural_twenty_recovery_keeps_prone_and_dropped_weapon",()=>{
                uint seed=0;
                for(uint i=1;i<10000;i++){var a=PlaytestDice.RollD20(i);if(a.Natural<10||a.Natural==20)continue;var d=DiceStream.Draw(a.NextRandomState,4);
                    var damage=PlaytestDamageDice.Resolve(new LifeState(26,1),d.Value+1,T(0),d.NextState,melee:true);
                    if(PlaytestDice.RollD20(damage.NextRandomState).Natural==20){seed=i;break;}}
                Require(seed!=0,"No recovery sequence seed.");var s=Clubs(new TestOnlyClubAttackPolicy(companionHp:1,seed:seed));BeginEncounter(s);Stance(s);HitClub(s);EndTurn(s);
                var l=Life(s,TestOnlyPolicy.CompanionId);Require(l.Hp==1&&l.Prone&&l.HeldItems.Count==0,"Automatic recovery stood up or repicked dropped Club.");
                var e=s.Capture().Encounter;RejectUnchanged(s,host,IC(s,CommandKind.EndRegularTurn,e.CurrentTurnId,actor:e.CurrentActor),"StanceRequired");Stance(s);
                RejectUnchanged(s,host,ClubCommand(s,CommandKind.AttackClub),"ClubNotHeld");EndTurn(s); });
            cases.Add("club_unsupported_commands_and_mixed_payloads_fail_closed",()=>{
                var s=Clubs();RejectUnchanged(s,host,IC(s,CommandKind.Move,x:1),"ClubCommandNotImplemented");BeginEncounter(s);
                var c=ClubCommand(s,CommandKind.SelectCombatStance,stance:2);
                RejectUnchanged(s,host,new Command(c.Id,c.Actor,c.ExpectedRevision,c.Kind,inventory:new InventoryRequest(Q(1)),combat:c.Combat),"UnexpectedCombatPayload");
                RejectUnchanged(s,host,new Command(c.Id,c.Actor,c.ExpectedRevision,CommandKind.EndRegularTurn,s.Capture().Encounter.CurrentTurnId,combat:c.Combat),"UnexpectedCombatPayload");
                RejectUnchanged(s,host,new Command(c.Id,c.Actor,c.ExpectedRevision,CommandKind.AttackClub),"UnexpectedCombatPayload"); });
            cases.Add("club_restore_rejects_forged_rng_roll_equipment_and_pending_state",()=>{
                var s=PendingClub(out var p);var original=s.Capture();
                void Bad(Action<Snapshot> alter){var v=original.Copy();alter(v);Throws<ArgumentException>(()=>new Simulation(p,codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory));}
                Bad(v=>v.RandomState=123);Bad(v=>v.Clubs=v.Clubs.Select(w=>w.Id==TestOnlyClubAttackPolicy.ActorClub?new ClubInstance(w.Id,w.ProfileId,w.OwnerId,w.CustodianId,"",w.CellX,w.CellY):w).ToArray());
                Bad(v=>{var a=v.MeleeAttacks.Single();v.MeleeAttacks=new[]{new MeleeAttackRecord(a.Id,a.Revision,a.Revision,a.TurnOrdinal,a.AttackerId,a.TargetId,a.WeaponId,a.At,a.Instruction,a.Attack,a.Damage)};});
                Bad(v=>{var a=v.MeleeAttacks.Single();var d=a.Damage;v.MeleeAttacks=new[]{new MeleeAttackRecord(a.Id,a.Revision,0,a.TurnOrdinal,a.AttackerId,a.TargetId,a.WeaponId,a.At,a.Instruction,a.Attack,
                    new CombatDamageRoll(d.Dice,d.Total+1,d.DiceWords,d.EffectsSeed,d.FinalRandom,d.EffectsWords,d.WoundNatural,d.InjuryD6,0))};}); });
            cases.Add("club_restore_rejects_missing_paid_history_and_duplicate_stance",()=>{
                var p=new TestOnlyClubAttackPolicy(seed:SeedForDeath(1));var s=Clubs(p);BeginEncounter(s);Stance(s);HitClub(s);var v=s.Capture();v.MeleeAttacks=Array.Empty<MeleeAttackRecord>();
                Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory));EndTurn(s);Stance(s);v=s.Capture();v.Stances=new[]{v.Stances[0],v.Stances[0]};Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory));
                v=s.Capture();v.Receipts=v.Receipts.Where(r=>r.Revision!=3).ToArray();Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory)); });
            cases.Add("club_restore_rejects_background_changes_outside_admitted_commands",()=>{
                var p=new TestOnlyClubAttackPolicy();var v=p.Initial();var lot=v.Work.Lots.First();v.Work=new WorkLedger(v.Work.Lots.Select(l=>l.Id==lot.Id?new ResourceLot(l.Id,l.UnitId,l.Amount+Q(1),l.LocationId,l.CustodianId):l));
                Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory));v=p.Initial();v.CropPlots=new[]{new CropPlotRecord(v.CropPlots[0].Id,v.CropPlots[0].OwnerId,false)};Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory)); });
            cases.Add("club_codec_bounds_and_legacy_schema_reject_new_fields",()=>{
                var p=new TestOnlyClubAttackPolicy();var v=p.Initial();var legacy=v.Copy();legacy.SchemaVersion=8;legacy.Clubs=Array.Empty<ClubInstance>();int offset=codec.Encode(legacy).Length-32;
                foreach(int count in new[]{-1,65,int.MaxValue}){byte[] bad=codec.Encode(v);Array.Copy(BitConverter.GetBytes(count),0,bad,offset,4);Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad));}
                v.SchemaVersion=8;Throws<ArgumentException>(()=>codec.Encode(v));byte[] future=codec.Encode(p.Initial());future[4]=10;Resign(future);Throws<InvalidDataException>(()=>codec.Decode(future)); });
            cases.Add("club_release_gate_and_save_roundtrip_pending_then_resolved",()=>{
                var s=PendingClub(out var p);Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                string path=Path.Combine(directory,"pending-club.bin");var store=new FileSaveStore();store.Save(path,s.Capture());s=new Simulation(p,store.Load(path),ExecutionProfile.Laboratory);ChooseKnockout(s,true);store.Save(path,s.Capture());
                Require(store.Load(path+".bak").MeleeAttacks.Single().Pending&&!store.Load(path).MeleeAttacks.Single().Pending,"Atomic save lost resumable decision stage."); });
        }
    }
}
#endif
