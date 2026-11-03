#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static Injury[] Wounds(int count) => Enumerable.Repeat(Injury.None,count).ToArray();
        private static DamageResolution Hit(LifeState s, long damage, int natural = 20, int modifier = 5,
            int injury = 1, bool critical = false, bool maiming = false, bool knockout = false,
            bool melee = false, int? stableD4 = null, long now = 0)
            => PlaytestLife.Damage(s,damage,modifier,natural,injury,critical,maiming,knockout,melee,stableD4,now);
        private static void AddLifeCases(Dictionary<string,Action> cases)
        {
            cases.Add("life_exact_stable_recovery_preserves_fractional_origin_and_deadline",()=>{
                var s=PlaytestLife.StabilizeAt(new LifeState(40,0),1,T(1,3));
                Require(s.StableUntil==T(10801,3)&&PlaytestLife.StableRecoveryAt(s,T(3600)).Hp==0,"Stable deadline rounded down.");
                var recovered=PlaytestLife.StableRecoveryAt(s,T(10801,3));
                Require(recovered.Hp==1&&!recovered.Stable&&!recovered.StableUntil.HasValue,"Exact deadline did not recover once.");
                Require(PlaytestLife.StableRecoveryAt(recovered,T(7200)).Hp==1,"Stable recovery repeated."); });
            cases.Add("life_exact_knockout_records_fractional_completion",()=>{
                var s=PlaytestLife.DamageAt(new LifeState(40,5),5,T(2,7),woundNatural:20,knockout:true,melee:true,stableD4:2).State;
                Require(s.Stable&&s.StableUntil==T(50402,7)&&s.DeathFailures==0,"Knockout rounded or duplicated zero-HP consequences."); });
            cases.Add("life_exact_third_death_success_retains_start_phase",()=>{
                var s=PlaytestLife.DeathSaveAt(new LifeState(40,0,deathSuccesses:2),10,1,T(5,11),stableD4:4);
                Require(s.Stable&&s.StableUntil==T(158405,11)&&s.LastDeathTurn==1&&s.DeathSuccesses==0,"Death-save stabilization lost phase/counter reset."); });
            cases.Add("life_exact_prohibited_natural_twenty_stabilizes_without_transient_hp",()=>{
                var s=PlaytestLife.DeathSaveAt(new LifeState(40,0,deathFailures:2),20,1,T(1,7),stableD4:3,hpRecoveryProhibited:true);
                Require(s.Hp==0&&s.Stable&&s.StableUntil==T(75601,7)&&s.DeathFailures==0,"Blocked natural20 healed or rounded."); });
            cases.Add("life_exact_buffered_damage_retains_deadline_real_damage_cancels",()=>{
                var s=new LifeState(40,0,5,stable:true,stableUntil:T(10801,3));
                var buffered=PlaytestLife.DamageAt(s,5,T(1,3)).State;
                Require(buffered.StableUntil==s.StableUntil&&buffered.Stable,"Temporary HP absorption erased fractional recovery.");
                var broken=PlaytestLife.DamageAt(buffered,1,T(2,3)).State;
                Require(!broken.Stable&&!broken.StableUntil.HasValue&&broken.DeathFailures==1,"HP damage retained stale recovery."); });
            cases.Add("life_exact_capacity_and_wound_changes_preserve_recovery",()=>{
                var s=new LifeState(40,0,wounds:Wounds(2),stable:true,stableUntil:T(10801,3));
                var changed=PlaytestLife.RemoveWounds(PlaytestLife.ChangeMaximum(s,20),new[]{0});
                Require(changed.StableUntil==s.StableUntil&&changed.Hp==0&&changed.Wounds.Count==1&&s.Wounds.Count==2,"Non-HP changes moved recovery or mutated input."); });
            cases.Add("life_exact_overdue_prohibited_recovery_resumes_without_reanchoring",()=>{
                var s=PlaytestLife.StabilizeAt(new LifeState(40,0),1,T(1,3));
                var blocked=PlaytestLife.StableRecoveryAt(s,T(20000,3),true);
                Require(blocked.StableUntil==T(10801,3)&&blocked.Hp==0,"Blocked recovery restarted deadline.");
                Require(PlaytestLife.StableRecoveryAt(blocked,T(20001,3)).Hp==1,"Overdue legal recovery waited another hour."); });
            cases.Add("life_exact_legacy_deadline_view_never_truncates",()=>{
                var fractional=PlaytestLife.StabilizeAt(new LifeState(40,0),1,T(1,3));
                Throws<InvalidOperationException>(()=>{var ignored=fractional.StableUntilSeconds;});
                var whole=new LifeState(40,0,stable:true,stableUntil:T(7200,2));
                Require(whole.StableUntilSeconds==3600&&new LifeState(40,0,stable:true,stableUntilSeconds:3600).StableUntil==T(3600),"Legacy whole seconds lost exact equivalence."); });
            cases.Add("life_exact_deadline_requires_one_valid_stable_representation",()=>{
                Throws<ArgumentException>(()=>new LifeState(40,0,stable:true,stableUntil:T(1,3),stableUntilSeconds:0));
                Throws<ArgumentException>(()=>new LifeState(40,0,stableUntil:T(1,3)));
                Throws<ArgumentException>(()=>new LifeState(40,0,stable:true));
                Throws<ArgumentOutOfRangeException>(()=>new LifeState(40,0,stable:true,stableUntilSeconds:-1)); });
            cases.Add("life_exact_overflow_rejects_without_mutating_state",()=>{
                var s=new LifeState(40,0);var late=T(long.MaxValue,2);
                Throws<OverflowException>(()=>PlaytestLife.StabilizeAt(s,1,late));
                Throws<OverflowException>(()=>PlaytestLife.DeathSaveAt(s,20,1,late,stableD4:1,hpRecoveryProhibited:true));
                Require(!s.Stable&&!s.StableUntil.HasValue&&s.LastDeathTurn==0,"Failed exact timing changed source state."); });
            cases.Add("life_exact_recovery_uses_original_seven_actor_slot_phase",()=>{
                var e=new FixedEncounterRecord("test",T(1,3),Enumerable.Range(0,7).Select(i=>"actor"+i),new long[]{1});
                var phase=FixedEncounterRules.Start(e,1);var s=PlaytestLife.StabilizeAt(new LifeState(40,0),1,phase);
                Require(phase==T(25,21)&&s.StableUntil==T(75625,21)&&PlaytestLife.StableRecoveryAt(s,T(3601)).Hp==0
                    &&PlaytestLife.StableRecoveryAt(s,T(75625,21)).Hp==1,"Fractional encounter phase drifted on hour conversion."); });
            cases.Add("life_exact_positive_healing_clears_deadline_zero_healing_preserves",()=>{
                var s=new LifeState(40,0,stable:true,stableUntil:T(10801,3));
                Require(PlaytestLife.Heal(s,0).StableUntil==s.StableUntil&&PlaytestLife.Heal(s,10,true).StableUntil==s.StableUntil,"No actual healing canceled recovery.");
                var healed=PlaytestLife.Heal(s,1);Require(healed.Hp==1&&!healed.StableUntil.HasValue&&!healed.Stable,"Actual recovery retained Stable deadline."); });
            cases.Add("life_post_temp_threshold", () => {
                var r=Hit(new LifeState(40,40,10),25);
                Require(r.State.Hp==25 && r.State.TemporaryHp==0 && r.PostTempDamage==15 && r.TemporaryAbsorbed==10 && r.WoundSaves==0,"Use damage after temp HP."); });
            cases.Add("life_fully_buffered_and_maiming", () => {
                var s=new LifeState(40,40,30);
                var a=PlaytestLife.Damage(s,20);var b=Hit(s,20,maiming:true);
                Require(a.State.Hp==40 && a.WoundSaves==0 && b.State.Hp==40 && b.WoundSaves==1 && b.WoundDc==10,"Independent Maiming survives full absorption."); });
            cases.Add("life_one_save_for_overlapping_triggers", () => {
                var r=Hit(new LifeState(40,15),25,maiming:true);
                Require(r.State.Hp==0 && r.WoundSaves==1 && r.DeathFailuresAdded==0 && r.NormalHpLost==15,"Drop, half-max and Maiming share a save."); });
            cases.Add("life_third_wound_uses_pre_event_penalty", () => {
                var r=Hit(new LifeState(40,40,wounds:Wounds(2)),20,11,0);
                Require(r.WoundTotal==9 && r.State.Wounds.Count==3 && !r.State.Dead && r.InjuryRolls==0,"Third Wound is not the later fatal failure."); });
            cases.Add("life_severe_third_wound_links_one_injury", () => {
                var r=Hit(new LifeState(40,40,wounds:Wounds(2)),20,5,0,4);
                Require(r.State.Wounds.SequenceEqual(new[]{Injury.None,Injury.None,Injury.FineMotorTrauma}) && r.InjuryRolls==1 && !r.State.Dead,"One linked Injury."); });
            cases.Add("life_failed_save_at_three_kills_without_injury_roll", () => {
                var r=PlaytestLife.Damage(new LifeState(40,40,wounds:Wounds(3)),20,0,1);
                Require(r.State.Dead && r.State.Hp==0 && r.State.Wounds.Count==3 && r.InjuryRolls==0,"No fourth Wound or Injury roll."); });
            cases.Add("life_instant_death_precedes_wounds_and_knockout", () => {
                var r=PlaytestLife.Damage(new LifeState(40,20),60,knockout:true,melee:true);
                Require(r.State.Dead && r.InstantDeath && r.WoundSaves==0 && r.DeathFailuresAdded==0,"Excess equals maximum is instant death."); });
            cases.Add("life_at_zero_instant_death_skips_failures", () => {
                var r=PlaytestLife.Damage(new LifeState(40,0),40);
                Require(r.State.Dead && r.InstantDeath && r.DeathFailuresAdded==0,"Instant death at zero."); });
            cases.Add("life_damage_at_zero_and_critical_failures", () => {
                var a=PlaytestLife.Damage(new LifeState(40,0),1);
                var b=PlaytestLife.Damage(a.State,1,critical:true);
                Require(a.State.DeathFailures==1 && !a.State.Dead && b.State.DeathFailures==3 && b.State.Dead && b.DeathFailuresAdded==2,"Damage while dying."); });
            cases.Add("life_stable_buffer_preserves_deadline_then_damage_cancels", () => {
                var a=PlaytestLife.Damage(new LifeState(40,0,5,stable:true,stableUntilSeconds:7200),5);
                var b=PlaytestLife.Damage(a.State,1);
                Require(a.State.Stable && a.State.StableUntilSeconds==7200 && a.State.DeathFailures==0
                    && !b.State.Stable && b.State.StableUntilSeconds==null && b.State.DeathFailures==1,"Temp HP does not break Stable."); });
            cases.Add("life_knockout_sets_absolute_deadline", () => {
                var r=Hit(new LifeState(40,5),5,knockout:true,melee:true,stableD4:2,now:100);
                Require(r.State.Stable && r.State.StableUntilSeconds==7300 && r.State.DeathFailures==0 && r.WoundSaves==1,"Knockout after Wound save."); });
            cases.Add("life_knockout_cannot_override_fatal_wound", () => {
                var r=PlaytestLife.Damage(new LifeState(40,5,wounds:Wounds(3)),5,0,1,knockout:true,melee:true);
                Require(r.State.Dead && !r.State.Stable && r.State.StableUntilSeconds==null,"Fatal Wound prevents stabilization."); });
            cases.Add("life_ordinary_creature_death_or_knockout", () => {
                var initial=new LifeState(40,5,usesDeathSaves:false);
                var a=Hit(initial,5);var b=Hit(initial,5,knockout:true,melee:true,stableD4:2);
                var c=PlaytestLife.Damage(b.State,1);
                Require(a.State.Dead && b.State.Stable && !b.State.Dead && c.State.Dead && c.DeathFailuresAdded==0,"Ordinary monsters have no implicit death saves."); });
            cases.Add("life_critical_healing_ceiling_does_not_reduce_existing_hp", () => {
                Require(PlaytestLife.Heal(new LifeState(1,0,wounds:Wounds(3)),1).Hp==1
                    && PlaytestLife.Heal(new LifeState(40,40,wounds:Wounds(3)),5).Hp==40
                    && PlaytestLife.Heal(new LifeState(40,20,wounds:Wounds(3)),40).Hp==39,"Critical cap minimum1, capacity unchanged."); });
            cases.Add("life_healing_clears_counters_only_when_positive", () => {
                var initial=new LifeState(40,0,deathSuccesses:2,deathFailures:2);
                var zero=PlaytestLife.Heal(initial,0);var positive=PlaytestLife.Heal(initial,1);
                Require(zero.DeathSuccesses==2 && zero.DeathFailures==2 && positive.Hp==1
                    && positive.DeathSuccesses==0 && positive.DeathFailures==0,"Only actual positive recovery clears counters."); });
            cases.Add("life_stable_recovery_once_on_elapsed_clock", () => {
                var initial=new LifeState(40,0,stable:true,stableUntilSeconds:4*3600);
                var early=PlaytestLife.StableRecovery(initial,3*3600);
                var at=PlaytestLife.StableRecovery(initial,4*3600);
                var late=PlaytestLife.StableRecovery(at,8*3600);
                Require(early.Hp==0 && at.Hp==1 && !at.Stable && at.StableUntilSeconds==null && late.Hp==1,"Do not replay a recovery within a rest."); });
            cases.Add("life_stabilize_does_not_reroll_existing_deadline", () => {
                var s=PlaytestLife.Stabilize(new LifeState(40,0,deathSuccesses:2,deathFailures:2),3,100);
                Require(s.Stable && s.StableUntilSeconds==10900 && s.DeathSuccesses==0 && s.DeathFailures==0,"Stable clears counters.");
                Throws<ArgumentException>(()=>PlaytestLife.Stabilize(s,1,100)); });
            cases.Add("life_death_natural_twenty_overrides_modifier", () => {
                var r=PlaytestLife.DeathSave(new LifeState(40,0,deathSuccesses:2,deathFailures:2),20,1,modifier:int.MinValue);
                Require(r.Hp==1 && r.DeathSuccesses==0 && r.DeathFailures==0 && r.LastDeathTurn==1,"Specific natural20 restores1."); });
            cases.Add("life_death_natural_one_and_modified_other_rolls", () => {
                var a=PlaytestLife.DeathSave(new LifeState(40,0),1,1,modifier:int.MaxValue);
                var b=PlaytestLife.DeathSave(new LifeState(40,0),9,1,modifier:1);
                var c=PlaytestLife.DeathSave(new LifeState(40,0),10,1,modifier:-1);
                Require(a.DeathFailures==2 && b.DeathSuccesses==1 && c.DeathFailures==1,"Natural1 specific; other rolls use final total."); });
            cases.Add("life_third_success_stabilizes_and_third_failure_kills", () => {
                var a=PlaytestLife.DeathSave(new LifeState(40,0,deathSuccesses:2),10,4,stableD4:1,nowSeconds:12);
                var b=PlaytestLife.DeathSave(new LifeState(40,0,deathFailures:2),2,4);
                Require(a.Stable && a.StableUntilSeconds==3612 && a.DeathSuccesses==0 && a.DeathFailures==0 && a.LastDeathTurn==4
                    && b.Dead && b.DeathFailures==3 && b.LastDeathTurn==4,"Threshold transitions."); });
            cases.Add("life_death_saves_regular_once_only", () => {
                var s=PlaytestLife.DeathSave(new LifeState(40,0),10,5);
                foreach(long marker in new[]{0L,4L,5L}) Throws<ArgumentException>(()=>PlaytestLife.DeathSave(s,10,marker));
                Throws<ArgumentException>(()=>PlaytestLife.DeathSave(s,10,6,regular:false));
                foreach(var invalid in new[]{new LifeState(40,1),new LifeState(40,0,stable:true,stableUntilSeconds:100),new LifeState(40,0,dead:true),new LifeState(40,0,stable:true,usesDeathSaves:false,stableUntilSeconds:100)})
                    Throws<ArgumentException>(()=>PlaytestLife.DeathSave(invalid,10,6)); });
            cases.Add("life_dead_cannot_receive_ordinary_healing_or_treatment", () => {
                var dead=new LifeState(40,0,wounds:Wounds(1),dead:true);
                Throws<ArgumentException>(()=>PlaytestLife.Heal(dead,10));
                Throws<ArgumentException>(()=>PlaytestLife.Stabilize(dead,1,0));
                Throws<ArgumentException>(()=>PlaytestLife.RemoveWounds(dead,new[]{0}));
                Throws<ArgumentException>(()=>PlaytestLife.Damage(dead,1)); });
            cases.Add("life_duplicate_injuries_keep_separate_links", () => {
                var s=new LifeState(40,20,wounds:new[]{Injury.MobilityTrauma,Injury.MobilityTrauma,Injury.CognitiveTrauma});
                var first=PlaytestLife.RemoveWounds(s,new[]{0});var second=PlaytestLife.RemoveWounds(first,new[]{0});
                Require(PlaytestLife.ActiveInjuries(s).SequenceEqual(new[]{Injury.MobilityTrauma,Injury.CognitiveTrauma})
                    && PlaytestLife.ActiveInjuries(first).SequenceEqual(PlaytestLife.ActiveInjuries(s))
                    && PlaytestLife.ActiveInjuries(second).SequenceEqual(new[]{Injury.CognitiveTrauma})
                    && first.Hp==20 && first.HealingCeiling==40,"Removal does not heal; duplicate persists until last linked record removed."); });
            cases.Add("life_wound_selection_and_recovery_boundaries", () => {
                var s=new LifeState(40,20,wounds:Wounds(2));
                foreach(int[] selection in new[]{Array.Empty<int>(),new[]{0,0},new[]{-1},new[]{2}})
                    Throws<ArgumentException>(()=>PlaytestLife.RemoveWounds(s,selection));
                Require(PlaytestLife.HitDiceRecovered(1,3)==0 && PlaytestLife.HitDiceRecovered(5,2)==3,"Recovery penalty only.");
                Throws<ArgumentOutOfRangeException>(()=>PlaytestLife.HitDiceRecovered(1,4)); });
            cases.Add("life_invalid_state_rejected", () => {
                Throws<ArgumentException>(()=>new LifeState(10,5,deathFailures:1));
                Throws<ArgumentException>(()=>new LifeState(10,0,stable:true,deathSuccesses:1));
                Throws<ArgumentException>(()=>new LifeState(10,0,stable:true));
                Throws<ArgumentException>(()=>new LifeState(10,0,deathFailures:3));
                Throws<ArgumentException>(()=>new LifeState(10,0,stable:true,dead:true));
                Throws<ArgumentException>(()=>new LifeState(10,0,usesDeathSaves:false,deathFailures:1));
                Throws<ArgumentException>(()=>new LifeState(10,0,usesDeathSaves:false));
                Throws<ArgumentException>(()=>new LifeState(10,1,stableUntilSeconds:100));
                Throws<ArgumentException>(()=>new LifeState(10,0,stable:true,stableUntilSeconds:-1));
                Throws<ArgumentException>(()=>new LifeState(10,1,wounds:Wounds(4)));
                Throws<ArgumentException>(()=>new LifeState(10,1,wounds:new[]{(Injury)7}));
                Throws<ArgumentOutOfRangeException>(()=>new LifeState(0,0));
                Throws<ArgumentOutOfRangeException>(()=>new LifeState(10,11)); });
            cases.Add("life_required_rolls_and_rejection_leave_input_intact", () => {
                var s=new LifeState(40,5,wounds:Wounds(2));
                Throws<ArgumentException>(()=>PlaytestLife.Damage(s,5));
                Throws<ArgumentException>(()=>PlaytestLife.Damage(s,5,0,1));
                Throws<ArgumentException>(()=>PlaytestLife.Damage(s,5,20,20,knockout:true,melee:true));
                Throws<ArgumentException>(()=>PlaytestLife.Damage(s,5,20,20,knockout:true));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestLife.Damage(s,-1));
                Require(s.Hp==5 && s.Wounds.Count==2 && !s.Stable && !s.Dead,"Rejected event modified caller state."); });
            cases.Add("life_immutable_collections", () => {
                var input=Wounds(2);var s=new LifeState(40,20,wounds:input);input[0]=Injury.Concussion;
                Require(s.Wounds[0]==Injury.None,"Caller array escaped.");
                Throws<NotSupportedException>(()=>((IList<Injury>)s.Wounds).Clear());
                Throws<NotSupportedException>(()=>((IList<Injury>)PlaytestLife.ActiveInjuries(s)).Add(Injury.Concussion)); });
            cases.Add("life_long_arithmetic_and_half_threshold", () => {
                long halfFloor=long.MaxValue/2;
                var low=PlaytestLife.Damage(new LifeState(long.MaxValue,long.MaxValue),halfFloor);
                var high=PlaytestLife.Damage(new LifeState(long.MaxValue,long.MaxValue),halfFloor+1,int.MinValue,1,1);
                Require(low.WoundSaves==0 && high.WoundSaves==1 && high.WoundDc==(halfFloor+1)/2
                    && high.WoundTotal==-2147483647L && high.State.Wounds.Count==1,"No overflow or rounded-down half threshold.");
                Require(PlaytestLife.Heal(new LifeState(long.MaxValue,1),long.MaxValue).Hp==long.MaxValue,"Saturating healing without addition overflow.");
                Require(PlaytestLife.Damage(new LifeState(long.MaxValue,0),long.MaxValue).InstantDeath,"Maximum long instant death."); });
            cases.Add("life_deadline_overflow_rejected_without_mutation", () => {
                var s=new LifeState(40,0,deathSuccesses:2);
                Throws<OverflowException>(()=>PlaytestLife.Stabilize(s,1,long.MaxValue));
                Throws<OverflowException>(()=>PlaytestLife.DeathSave(s,10,1,stableD4:4,nowSeconds:long.MaxValue));
                Require(s.DeathSuccesses==2 && s.LastDeathTurn==0 && !s.Stable,"No half-applied deadline."); });
            cases.Add("life_blocked_natural_twenty_stabilizes_without_healing", () => {
                var s=new LifeState(40,0,deathSuccesses:2,deathFailures:2);
                var r=PlaytestLife.DeathSave(s,20,1,stableD4:2,nowSeconds:100,hpRecoveryProhibited:true);
                Require(r.Hp==0 && r.Stable && r.DeathSuccesses==0 && r.DeathFailures==0 && r.StableUntilSeconds==7300
                    && r.LastDeathTurn==1 && s.DeathFailures==2,"Decay bridge has no transient HP gain.");
                Throws<ArgumentException>(()=>PlaytestLife.DeathSave(s,20,1,hpRecoveryProhibited:true)); });
            cases.Add("life_blocked_recovery_retains_deadline_and_cannot_heal", () => {
                var s=new LifeState(40,0,stable:true,stableUntilSeconds:100);
                var blocked=PlaytestLife.StableRecovery(s,500,hpRecoveryProhibited:true);
                var resumed=PlaytestLife.StableRecovery(blocked,501);
                Require(blocked.Hp==0 && blocked.StableUntilSeconds==100 && resumed.Hp==1 && !resumed.Stable
                    && PlaytestLife.Heal(s,40,hpRecoveryProhibited:true).Hp==0,"Do not reroll or restart overdue recovery.");
                var broken=PlaytestLife.Damage(blocked,1).State;
                Require(PlaytestLife.StableRecovery(broken,501).Hp==0 && broken.StableUntilSeconds==null,"Damage cancels blocked Stable recovery."); });
            cases.Add("life_capacity_change_preserves_state_and_temp_hp", () => {
                var s=new LifeState(40,26,25,wounds:Wounds(3));
                var reduced=PlaytestLife.ChangeMaximum(s,15);var restored=PlaytestLife.ChangeMaximum(reduced,40);
                Require(reduced.Hp==15 && reduced.TemporaryHp==25 && reduced.Wounds.Count==3 && restored.Hp==15
                    && restored.HealingCeiling==39,"Clamp only; no damage, healing or temp-HP clamp.");
                foreach(var zero in new[]{new LifeState(40,0,stable:true,stableUntilSeconds:100),new LifeState(40,0,dead:true),new LifeState(40,0,deathFailures:2)}) {
                    var r=PlaytestLife.ChangeMaximum(zero,1);
                    Require(r.Hp==0 && r.Stable==zero.Stable && r.Dead==zero.Dead && r.DeathFailures==zero.DeathFailures
                        && r.StableUntilSeconds==zero.StableUntilSeconds,"Capacity cannot revive or cancel a deadline.");
                }
                Throws<ArgumentOutOfRangeException>(()=>PlaytestLife.ChangeMaximum(s,0)); });
            cases.Add("life_sampled_damage_state_invariants", () => {
                int count=0;
                foreach(int maximum in new[]{1,10,21,40}) for(int hp=0;hp<=maximum;hp++)
                foreach(int temp in new[]{0,10}) foreach(int woundCount in new[]{0,2,3})
                foreach(int damage in new[]{0,1,5,10,20,30,40,80}) foreach(int die in new[]{1,10,20}) {
                    var s=new LifeState(maximum,hp,temp,Wounds(woundCount));var r=Hit(s,damage,die,2);
                    Require(s.Hp==hp && s.TemporaryHp==temp && s.Wounds.Count==woundCount && !s.Dead,"Input mutated.");
                    Require(r.State.Hp>=0 && r.State.Hp<=maximum && r.State.TemporaryHp>=0 && r.State.Wounds.Count<=3
                        && r.WoundSaves<=1 && r.InjuryRolls<=1 && (!r.State.Dead || r.State.Hp==0)
                        && !(hp>0 && r.DeathFailuresAdded>0),"Sample invariant failed."); count++;
                }
                Require(count==10944,"Scenario set unexpectedly changed."); });
        }
    }
}
#endif
