#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static MaximumHpApplication HpBonus(string id, MaximumHpSource source = MaximumHpSource.Tenacity,
            int level = 10, string target = "target", EffectClockMarker starts = default)
        { return new MaximumHpApplication(id, "owner", target, new MaximumHpMagnitude(source, characterLevel:level,
            warriorLevel:level, wizardLevel:level, acquisitionLevel:3, creationWizardLevel:level), starts); }
        private static MaximumHpApplication HpTrauma(string id, long amount, string owner = "monk", string target = "target",
            EffectClockMarker starts = default, EffectClockMarker? expires = null, bool rest = true)
        { return new MaximumHpApplication(id, owner, target, new MaximumHpMagnitude(MaximumHpSource.Ribcrusher,
            scale:1, modifier:amount-1), starts, expires, endsOnCompletedRest:rest); }
        private static MaximumHpCalculation HpMaximum(long baseMaximum, params MaximumHpApplication[] records)
            => PlaytestMaximumHp.Calculate(baseMaximum, records, "target");
        private static void AddMaximumHpCases(Dictionary<string, Action> cases)
        {
            cases.Add("maximum_hp_source_example_combines_flats_before_rational_product",()=>{
                var rows = new[]{HpBonus("flesh",MaximumHpSource.FleshWarden),HpTrauma("trauma",9)};
                var r=PlaytestMaximumHp.Calculate(101,rows,"target",expedition:4,exhaustion:4);
                Require(r.BaseMaximum==101&&r.AdditiveBonuses==20&&r.MonkTraumaReduction==9&&r.PreSystemicMaximum==112&&r.EffectiveMaximum==42,"Source maximum example diverged.");
                r=PlaytestMaximumHp.Calculate(101,new[]{rows[0],rows[1].WithSuppression(true)},"target",expedition:4,exhaustion:4);
                Require(r.EffectiveMaximum==45&&rows[1].Suppressed==false,"Suppression mutated original or subtracted twice.");
            });
            cases.Add("maximum_hp_all_supported_magnitude_formulas_retain_inputs",()=>{
                foreach(var item in new[]{(MaximumHpSource.Ribcrusher,7L),(MaximumHpSource.BoneBreakingStrike,10L),(MaximumHpSource.DeathlessSilence,16L)}) {
                    var m=new MaximumHpMagnitude(item.Item1,scale:3,modifier:4);Require(m.Amount==item.Item2&&m.Scale==3&&m.Modifier==4,"Monk source formula or snapshot wrong."); }
                Require(new MaximumHpMagnitude(MaximumHpSource.FleshWarden,warriorLevel:5,characterLevel:12).Amount==10,"Used character level for Flesh Warden.");
                Require(new MaximumHpMagnitude(MaximumHpSource.Conjuration,wizardLevel:12,creationWizardLevel:5).Amount==5,"Creation snapshot replaced by current level.");
                Require(new MaximumHpMagnitude(MaximumHpSource.FleshAscendant,wizardLevel:12).Amount==24,"Current controller level missing.");
                foreach(var source in new[]{MaximumHpSource.FamiliarBond,MaximumHpSource.Tenacity,MaximumHpSource.ToughAsNails,MaximumHpSource.DarkFortitude})
                    Require(new MaximumHpMagnitude(source,characterLevel:12).Amount==(source==MaximumHpSource.FamiliarBond||source==MaximumHpSource.Tenacity?12:24),"Current-level feat formula wrong.");
                var tough=new MaximumHpMagnitude(MaximumHpSource.Tough,characterLevel:12,acquisitionLevel:3);Require(tough.Amount==6&&tough.AcquisitionLevel==3,"Tough snapshot grew.");
            });
            cases.Add("maximum_hp_distinct_feat_identities_add_duplicate_identity_does_not",()=>{
                var rows=new[]{HpBonus("tenacity"),HpBonus("tough",MaximumHpSource.Tough),HpBonus("nails",MaximumHpSource.ToughAsNails),HpBonus("dark",MaximumHpSource.DarkFortitude),HpBonus("duplicate")};
                var r=HpMaximum(20,rows);Require(r.EffectiveMaximum==76&&r.SelectedApplications.Count==4,"Distinct feat bonus or duplicate arbitration wrong.");
            });
            cases.Add("maximum_hp_wizard_exception_stacks_and_alias_has_one_identity",()=>{
                var source=PlaytestMaximumHp.SourceFromId("wizard.engine[24]");Require(source==PlaytestMaximumHp.SourceFromId("wizard.hero.necromancer.flesh-ascendant"),"Alias created another modifier source.");
                var flesh=HpBonus("one-actual-effect",source);var school=HpBonus("school",MaximumHpSource.Conjuration);
                Require(HpMaximum(20,flesh,school).EffectiveMaximum==50,"Wizard explicit pair did not add.");
                Require(HpMaximum(20,flesh.WithSuppression(true),school).EffectiveMaximum==30,"Suppression left alias operative.");
                Throws<ArgumentException>(()=>HpMaximum(20,flesh,flesh));
            });
            cases.Add("maximum_hp_monk_arbitration_is_global_across_owners_and_cards",()=>{
                var small=HpTrauma("small",5,"monk-a");
                var big=new MaximumHpApplication("big","monk-b","target",new MaximumHpMagnitude(MaximumHpSource.BoneBreakingStrike,scale:4,modifier:1),endsOnCompletedRest:true);
                Require(HpMaximum(30,small,big).EffectiveMaximum==21&&HpMaximum(30,small,big).MonkTraumaReduction==9,"Monk reductions stacked across owners.");
                Require(HpMaximum(30,small,big.WithSuppression(true)).EffectiveMaximum==25,"Smaller record did not resume.");
                Require(HpMaximum(30,small,big,HpTrauma("repeat",7,"monk-a")).EffectiveMaximum==21,"Repeated card stacked.");
            });
            cases.Add("maximum_hp_ties_use_earliest_marker_then_ordinal_id",()=>{
                var early=HpTrauma("z",5,starts:new EffectClockMarker(T(1,3),10));
                var late=HpTrauma("a",5,starts:new EffectClockMarker(T(1,3),20));
                var same=HpTrauma("b",5,starts:early.Starts);var now=new EffectClockMarker(T(2));
                foreach(var rows in new[]{new[]{early,late,same},new[]{same,late,early}}) {
                    var r=PlaytestMaximumHp.Calculate(20,rows,"target",now);Require(r.SelectedApplications["monk-trauma-global"]=="b","Tie winner depended on enumeration or ignored phase."); }
            });
            cases.Add("maximum_hp_exact_phase_endpoints_keep_application_before_expiry",()=>{
                var start=new EffectClockMarker(T(1,3),EffectClockMarker.EndEffectApplication);
                var end=new EffectClockMarker(T(1,3),EffectClockMarker.EndEffectExpiry);
                var r=HpTrauma("phase",5,starts:start,expires:end,rest:false);
                Require(!r.Operative(new EffectClockMarker(T(1,3)))&&r.Operative(start)&&r.Operative(new EffectClockMarker(T(1,3),19))&&!r.Operative(end),"Same-instant phase lifetime collapsed.");
                Require(new EffectClockMarker(T(2,6),10).Equals(start)&&new EffectClockMarker(T(2,6),10).GetHashCode()==start.GetHashCode(),"Equivalent rational marker mismatch.");
                Require(new EffectClockMarker(T(long.MaxValue),0).CompareTo(new EffectClockMarker(T(long.MaxValue-1),int.MaxValue))>0,"Phase overrode physical chronology.");
            });
            cases.Add("maximum_hp_future_expiry_and_suppression_preserve_each_clock",()=>{
                var weak=HpTrauma("weak",5,expires:new EffectClockMarker(T(5)));
                var strong=HpTrauma("strong",9,starts:new EffectClockMarker(T(2)),expires:new EffectClockMarker(T(8)));
                Require(PlaytestMaximumHp.Calculate(30,new[]{weak,strong},"target",new EffectClockMarker(T(1))).EffectiveMaximum==25,"Future stronger effect applied early.");
                Require(PlaytestMaximumHp.Calculate(30,new[]{weak,strong},"target",new EffectClockMarker(T(5))).EffectiveMaximum==21,"Winner borrowed weaker deadline.");
                Require(PlaytestMaximumHp.Calculate(30,new[]{weak,strong.WithSuppression(true)},"target",new EffectClockMarker(T(6))).EffectiveMaximum==30,"Suppressed clock revived expired loser.");
                Require(PlaytestMaximumHp.Calculate(30,new[]{strong.WithSuppression(false)},"target",new EffectClockMarker(T(8))).EffectiveMaximum==30,"Unsuppression restarted duration.");
            });
            cases.Add("maximum_hp_completed_rest_removes_all_target_default_traumas",()=>{
                var rows=new[]{HpTrauma("small",5,"one"),HpTrauma("big",9,"two").WithSuppression(true),HpBonus("feat"),HpTrauma("other",7,target:"other")};
                var ended=PlaytestMaximumHp.CompleteRest(rows,"target",true,CompletedRestKind.Short);
                Require(!ended[0].Present&&!ended[1].Present&&ended[2].Present&&ended[3].Present&&ended[1].Suppressed,"Completed rest missed suppression or removed another source/target.");
                Require(ended[0].EndedReason=="completed-target-short-rest"&&rows[0].Present,"Rest mutated history.");
                Require(ReferenceEquals(PlaytestMaximumHp.CompleteRest(ended,"target",true,CompletedRestKind.Long)[0],ended[0]),"Repeated rest rewrote ended history.");
                Throws<NotSupportedException>(()=>((IList<MaximumHpApplication>)ended)[0]=rows[0]);
            });
            cases.Add("maximum_hp_interrupted_rest_and_explicit_only_endpoint_survive",()=>{
                var rows=new[]{HpTrauma("default",5),HpTrauma("explicit",9,expires:new EffectClockMarker(T(8)),rest:false)};
                Require(PlaytestMaximumHp.CompleteRest(rows,"target",false,CompletedRestKind.Long).SequenceEqual(rows),"Interrupted rest removed trauma.");
                var ended=PlaytestMaximumHp.CompleteRest(rows,"target",true,CompletedRestKind.Long);
                Require(!ended[0].Present&&ended[1].Present,"Default rest replaced explicit-only endpoint.");
            });
            cases.Add("maximum_hp_target_and_presence_filter_without_removing_provenance",()=>{
                var removed=HpBonus("removed").Remove("source-ended");var rows=new[]{removed,HpBonus("other",target:"other")};
                Require(HpMaximum(20,rows).EffectiveMaximum==20&&removed.Magnitude.CharacterLevel==10&&removed.EndedReason=="source-ended","Inactive record applied or lost provenance.");
                Require(!removed.WithSuppression(false).Present,"Unsuppression resurrected removed effect.");
            });
            cases.Add("maximum_hp_systemic_factors_round_once_and_retain_minimum",()=>{
                Require(PlaytestMaximumHp.SystemicMaximum(11,4,4)==4,"Sequential rounding lost one HP.");
                Require(PlaytestMaximumHp.SystemicMaximum(1,6,6)==1&&HpMaximum(30,HpTrauma("overwhelming",100)).EffectiveMaximum==1,"Minimum capacity disappeared.");
            });
            cases.Add("maximum_hp_systemic_reference_grid_909_states",()=>{
                int count=0;for(int max=1;max<=101;max++)foreach(int expedition in new[]{0,4,6})foreach(int exhaustion in new[]{0,4,6}) {
                    // Independent closed-form table for the four compatible factor combinations.
                    int expected=Math.Max(1,expedition>=4?(exhaustion>=4?3*max/8:3*max/4):(exhaustion>=4?max/2:max));
                    Require(PlaytestMaximumHp.Calculate(max,Array.Empty<MaximumHpApplication>(),"target",expedition:expedition,exhaustion:exhaustion).EffectiveMaximum==expected,"Systemic source grid diverged.");count++;
                }Require(count==909,"Systemic grid incomplete.");
            });
            cases.Add("maximum_hp_capacity_clamp_is_neither_damage_nor_healing",()=>{
                var before=new LifeState(30,26,35);var changed=PlaytestMaximumHp.Recompute(before,30,new[]{HpTrauma("trauma",15)},"target");
                Require(changed.State.MaximumHp==15&&changed.State.Hp==15&&changed.State.TemporaryHp==35&&changed.CapacityClamp==11,"Capacity clamp or temp HP wrong.");
                Require(changed.ActualHpDamage==0&&changed.ActualHpGained==0&&changed.WoundSaves==0&&changed.DeathFailuresAdded==0&&changed.State.Wounds.Count==0,"Capacity change created an HP effect.");
                Require(before.Hp==26&&before.MaximumHp==30,"Original state mutated.");
                var restored=PlaytestMaximumHp.Recompute(changed.State,30,Array.Empty<MaximumHpApplication>(),"target");
                Require(restored.State.Hp==15&&restored.State.MaximumHp==30&&restored.CapacityClamp==0,"Capacity restoration healed.");
            });
            cases.Add("maximum_hp_critical_healing_ceiling_is_recomputed_separately",()=>{
                var before=new LifeState(30,26,25,new[]{Injury.None,Injury.Concussion,Injury.MobilityTrauma});
                var after=PlaytestMaximumHp.ApplyCapacity(before,15);
                Require(after.Hp==15&&after.HealingCeiling==14&&after.MaximumHp==15&&after.Wounds.SequenceEqual(before.Wounds),"Critical was treated as another max reduction or clamp.");
                after=PlaytestMaximumHp.ApplyCapacity(after,1);Require(after.Hp==1&&after.HealingCeiling==1&&after.TemporaryHp==25,"Tiny capacity changed unrelated life state.");
            });
            cases.Add("maximum_hp_preserves_dead_dying_stable_and_exact_deadline",()=>{
                var states=new[]{new LifeState(30,0,7,dead:true,deathFailures:3,lastDeathTurn:9),new LifeState(30,0,7,deathSuccesses:1,deathFailures:2,lastDeathTurn:9),new LifeState(30,0,7,stable:true,stableUntil:T(10,3),lastDeathTurn:9)};
                foreach(var before in states) {
                    var after=PlaytestMaximumHp.ApplyCapacity(before,50);
                    Require(after.MaximumHp==50&&after.Hp==0&&after.Dead==before.Dead&&after.Stable==before.Stable&&after.StableUntil==before.StableUntil
                        &&after.DeathSuccesses==before.DeathSuccesses&&after.DeathFailures==before.DeathFailures&&after.LastDeathTurn==9&&after.TemporaryHp==7,"Capacity change altered life history."); }
                var ordinary=new LifeState(30,0,stable:true,stableUntil:T(5,3),usesDeathSaves:false);
                Require(!PlaytestMaximumHp.ApplyCapacity(ordinary,1).UsesDeathSaves,"Capacity change granted death saves.");
            });
            cases.Add("maximum_hp_numeric_track_six_never_rekills_survivor",()=>{
                var before=new LifeState(30,0,stable:true,stableUntil:T(9,7));
                var after=PlaytestMaximumHp.Recompute(before,30,new[]{HpTrauma("trauma",100)},"target",expedition:6,exhaustion:6).State;
                Require(after.MaximumHp==1&&after.Stable&&!after.Dead&&after.StableUntil==T(9,7),"Numeric factor became lethal track transition.");
            });
            cases.Add("maximum_hp_creation_final_capacity_does_not_heal_later_acquisition",()=>{
                var rows=new[]{HpBonus("school",MaximumHpSource.Conjuration),HpBonus("flesh",MaximumHpSource.FleshAscendant)};
                long max=HpMaximum(20,rows).EffectiveMaximum;var created=new LifeState(max,max);
                var gained=PlaytestMaximumHp.Recompute(new LifeState(20,20),20,rows,"target");
                Require(created.Hp==50&&created.MaximumHp==50&&gained.State.MaximumHp==50&&gained.State.Hp==20,"Creation initialization and later capacity gain conflated.");
            });
            cases.Add("maximum_hp_widened_intermediate_and_final_overflow_guards",()=>{
                var bonus=HpBonus("bonus",level:20);
                var reduced=PlaytestMaximumHp.Calculate(long.MaxValue,new[]{bonus},"target",exhaustion:4);
                Require(reduced.PreSystemicMaximum==(BigInteger)long.MaxValue+20&&reduced.EffectiveMaximum==4611686018427387913L,"Intermediate overflow before systemic reduction.");
                Throws<OverflowException>(()=>HpMaximum(long.MaxValue,bonus));
                Require(HpMaximum(long.MaxValue,bonus,HpTrauma("trauma",long.MaxValue)).EffectiveMaximum==20,"Wide additive/subtractive ordering wrapped.");
                Throws<OverflowException>(()=>new MaximumHpMagnitude(MaximumHpSource.DeathlessSilence,scale:4,modifier:long.MaxValue));
            });
            cases.Add("maximum_hp_calculation_detaches_selected_winners",()=>{
                var rows=new[]{HpBonus("first")};var r=HpMaximum(20,rows);rows[0]=HpBonus("replacement");
                Require(r.SelectedApplications.Values.Single()=="first"&&r.EffectiveMaximum==30,"Caller array changed calculation.");
                Throws<NotSupportedException>(()=>((IDictionary<string,string>)r.SelectedApplications).Add("fake","fake"));
            });
            cases.Add("maximum_hp_threshold_exact_odd_and_inclusive_boundaries",()=>{
                Require(PlaytestMaximumHp.Threshold(25,100,HpFraction.Quarter,HpThresholdRelation.AtOrBelow)&&!PlaytestMaximumHp.Threshold(25,100,HpFraction.Quarter),"Quarter boundary wrong.");
                Require(!PlaytestMaximumHp.Threshold(26,101,HpFraction.Quarter,HpThresholdRelation.AtOrBelow)&&PlaytestMaximumHp.Threshold(50,101,HpFraction.Half),"Odd threshold rounded before comparison.");
                Require(!PlaytestMaximumHp.Threshold(50,100,HpFraction.Half)&&PlaytestMaximumHp.Threshold(50,100,HpFraction.Half,HpThresholdRelation.AtOrAbove),"Half equality wrong.");
                Require(PlaytestMaximumHp.Threshold(100,100,new HpFraction(1,1),HpThresholdRelation.AtOrBelow)&&PlaytestMaximumHp.Threshold(0,100,default,HpThresholdRelation.AtOrAbove),"Zero/one fraction endpoints wrong.");
            });
            cases.Add("maximum_hp_thresholds_widen_cross_products",()=>{
                Require(PlaytestMaximumHp.Threshold(long.MaxValue/2,long.MaxValue,HpFraction.Half),"Large half comparison overflowed.");
                Require(PlaytestMaximumHp.Threshold(long.MaxValue-1,long.MaxValue,new HpFraction(long.MaxValue-1,long.MaxValue),HpThresholdRelation.AtOrBelow)
                    &&!PlaytestMaximumHp.Threshold(long.MaxValue-1,long.MaxValue,new HpFraction(long.MaxValue-1,long.MaxValue)),"Large exact rational equality lost.");
            });
            cases.Add("maximum_hp_damage_and_direct_loss_crossings_exclude_capacity",()=>{
                foreach(var kind in new[]{HpChangeKind.Damage,HpChangeKind.DirectHpLoss,HpChangeKind.CapacityChange}) {
                    var e=new HpEventSnapshot("event",26,25,100,kind);Require(e.FallsAcross(HpFraction.Quarter)==(kind!=HpChangeKind.CapacityChange),"Fall event classification wrong."); }
                Require(!new HpEventSnapshot("already",20,19,100,HpChangeKind.Damage).FallsAcross(HpFraction.Quarter),"Already-low loss retriggered first fall.");
                Require(!new HpEventSnapshot("absorbed",26,26,100,HpChangeKind.Damage).FallsAcross(HpFraction.Quarter),"Temp-only absorption crossed HP threshold.");
            });
            cases.Add("maximum_hp_strict_crossing_and_actual_healing_exit",()=>{
                Require(!new HpEventSnapshot("to-half",51,50,100,HpChangeKind.Damage).FallsAcross(HpFraction.Half,false)
                    &&new HpEventSnapshot("from-half",50,49,100,HpChangeKind.Damage).FallsAcross(HpFraction.Half,false),"Strict half crossing wrong.");
                Require(new HpEventSnapshot("heal",50,51,100,HpChangeKind.Healing).HealedAboveHalf&&new HpEventSnapshot("higher",60,61,100,HpChangeKind.Healing).HealedAboveHalf,"Actual healing exit required an unnecessary crossing.");
                Require(!new HpEventSnapshot("zero",60,60,100,HpChangeKind.Healing).HealedAboveHalf&&!new HpEventSnapshot("capacity",60,60,100,HpChangeKind.CapacityChange).HealedAboveHalf,"No-gain/capacity satisfied healing exit.");
            });
            cases.Add("maximum_hp_historical_damage_uses_recorded_maximum_without_first_crossing",()=>{
                var old=new HpEventSnapshot("old-damage",60,49,100,HpChangeKind.Damage);
                Require(old.DamageLeftBelowHalf&&!PlaytestMaximumHp.Threshold(49,60,HpFraction.Half),"Later maximum rewrote stored event.");
                Require(new HpEventSnapshot("already-low",40,30,100,HpChangeKind.Damage).DamageLeftBelowHalf,"Rewind damage required first crossing.");
                Require(!new HpEventSnapshot("absorbed",40,40,100,HpChangeKind.Damage).DamageLeftBelowHalf&&!new HpEventSnapshot("loss",40,30,100,HpChangeKind.DirectHpLoss).DamageLeftBelowHalf,"Non-damage or no HP loss satisfied Rewind gate.");
            });
            cases.Add("maximum_hp_continuous_predicate_can_change_without_hp_event",()=>{
                Require(!PlaytestMaximumHp.Threshold(25,100,HpFraction.Quarter)&&PlaytestMaximumHp.Threshold(25,101,HpFraction.Quarter),"Strict-quarter continuous condition ignored capacity change.");
                Require(!new HpEventSnapshot("capacity",25,25,101,HpChangeKind.CapacityChange).FallsAcross(HpFraction.Quarter),"Continuous predicate granted first fall.");
            });
            cases.Add("maximum_hp_pain_bands_and_percentage_source_minimums",()=>{
                Require(PlaytestMaximumHp.PainEmpowerment(91,101)==0&&PlaytestMaximumHp.PainEmpowerment(90,101)==1&&PlaytestMaximumHp.PainEmpowerment(1,101)==5,"Pain full ten-percent bands wrong.");
                Require(PlaytestMaximumHp.PainEmpowerment(0,long.MaxValue)==5&&PlaytestMaximumHp.PainEmpowerment(long.MaxValue,long.MaxValue)==0,"Pain overflow.");
                Require(PlaytestMaximumHp.PercentageAmount(3,4)==0&&PlaytestMaximumHp.PercentageAmount(3,4,1)==1&&PlaytestMaximumHp.PercentageAmount(1,2,1)==1,"Invented/lost source minimum.");
                Require(PlaytestMaximumHp.PercentageAmount(11,3,1)==3,"Third recovery rounded up.");
            });
            cases.Add("maximum_hp_attack_metrics_freeze_before_separate_trauma",()=>{
                var before=new LifeState(30,30);var damage=PlaytestLife.Damage(before,4);
                var history=new HpEventSnapshot("attack",before.Hp,damage.State.Hp,before.MaximumHp,HpChangeKind.Damage);
                var changed=PlaytestMaximumHp.Recompute(damage.State,30,new[]{HpTrauma("bone",15)},"target");
                Require(damage.NormalHpLost==4&&damage.State.Hp==26&&changed.State.Hp==15&&changed.CapacityClamp==11,"Attack and capacity losses merged.");
                Require(history.EffectiveMaximum==30&&history.AfterHp==26&&!history.DamageLeftBelowHalf&&changed.ActualHpDamage==0,"Stat clamp rewrote historical attack metrics.");
            });
            cases.Add("maximum_hp_missing_snapshots_unknown_sources_and_endpoint_rejection",()=>{
                Throws<ArgumentException>(()=>new MaximumHpMagnitude(MaximumHpSource.Tough,characterLevel:12));
                Throws<ArgumentException>(()=>new MaximumHpMagnitude(MaximumHpSource.Conjuration,wizardLevel:12));
                Throws<ArgumentException>(()=>new MaximumHpMagnitude(MaximumHpSource.Ribcrusher,scale:1));
                Throws<ArgumentException>(()=>new MaximumHpMagnitude(MaximumHpSource.Tough,characterLevel:2,acquisitionLevel:3));
                Throws<ArgumentException>(()=>new MaximumHpMagnitude((MaximumHpSource)99));Throws<ArgumentException>(()=>PlaytestMaximumHp.SourceFromId("spell:invented"));
                Throws<ArgumentException>(()=>new MaximumHpApplication("endless","owner","target",new MaximumHpMagnitude(MaximumHpSource.Ribcrusher,scale:1,modifier:1)));
                Throws<ArgumentException>(()=>new MaximumHpApplication("rest-feat","owner","target",HpBonus("bonus").Magnitude,endsOnCompletedRest:true));
                Throws<ArgumentException>(()=>HpTrauma("backward",5,starts:new EffectClockMarker(T(1)),expires:new EffectClockMarker(T(1))));
                Throws<ArgumentException>(()=>new MaximumHpApplication("bad","owner","target",HpBonus("bonus").Magnitude,endedReason:"already-ended"));
            });
            cases.Add("maximum_hp_invalid_records_levels_and_systemic_inputs_fail_closed",()=>{
                var r=HpBonus("same");Throws<ArgumentException>(()=>HpMaximum(20,r,r));Throws<ArgumentException>(()=>HpMaximum(20,(MaximumHpApplication)null));
                Throws<ArgumentNullException>(()=>PlaytestMaximumHp.Calculate(20,null,"target"));Throws<ArgumentException>(()=>PlaytestMaximumHp.Calculate(20,new[]{r}," "));
                Throws<ArgumentOutOfRangeException>(()=>HpMaximum(0));Throws<ArgumentOutOfRangeException>(()=>PlaytestMaximumHp.SystemicMaximum(10,7));Throws<ArgumentOutOfRangeException>(()=>PlaytestMaximumHp.SystemicMaximum(10,exhaustion:-1));
                Throws<ArgumentOutOfRangeException>(()=>new MaximumHpMagnitude(MaximumHpSource.Tenacity,characterLevel:21));Throws<ArgumentException>(()=>new MaximumHpMagnitude(MaximumHpSource.Ribcrusher,scale:5,modifier:1));
                Throws<ArgumentOutOfRangeException>(()=>new EffectClockMarker(T(1),-1));Throws<ArgumentException>(()=>PlaytestMaximumHp.CompleteRest(new[]{r},"target",true,(CompletedRestKind)99));
                Throws<ArgumentNullException>(()=>PlaytestMaximumHp.Recompute(null,20,new[]{r},"target"));Throws<ArgumentNullException>(()=>PlaytestMaximumHp.ApplyCapacity(null,20));
            });
            cases.Add("maximum_hp_invalid_threshold_and_event_inputs_fail_closed",()=>{
                Throws<ArgumentException>(()=>new HpFraction(1,0));Throws<ArgumentException>(()=>new HpFraction(-1,4));Throws<ArgumentException>(()=>new HpFraction(5,4));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestMaximumHp.Threshold(21,20,HpFraction.Half));Throws<ArgumentOutOfRangeException>(()=>PlaytestMaximumHp.Threshold(0,0,HpFraction.Half));
                Throws<ArgumentException>(()=>PlaytestMaximumHp.Threshold(1,20,HpFraction.Half,(HpThresholdRelation)99));
                Throws<ArgumentException>(()=>new HpEventSnapshot("",1,0,20,HpChangeKind.Damage));Throws<ArgumentException>(()=>new HpEventSnapshot("bad",0,1,20,HpChangeKind.Damage));
                Throws<ArgumentException>(()=>new HpEventSnapshot("bad",1,0,20,HpChangeKind.Healing));Throws<ArgumentException>(()=>new HpEventSnapshot("bad",1,1,20,(HpChangeKind)99));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestMaximumHp.PercentageAmount(20,0));Throws<ArgumentOutOfRangeException>(()=>PlaytestMaximumHp.PercentageAmount(20,4,-1));Throws<ArgumentOutOfRangeException>(()=>PlaytestMaximumHp.PainEmpowerment(-1,20));
            });
        }
    }
}
#endif
