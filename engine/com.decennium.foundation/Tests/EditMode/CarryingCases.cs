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
        private static RuleQuantity Q(long n,long d=1)=>new RuleQuantity(n,d);
        private static BurdenItem B(string id,RuleQuantity? pounds=null,RuleQuantity? load=null,string parent=null,
            string[] poundContents=null,string[] loadContents=null)=>new BurdenItem(id,parent,pounds,load,poundContents,loadContents);
        private static void AddCarryingCases(Dictionary<string,Action> cases)
        {
            cases.Add("quantity_normalizes_default_and_equivalent_fractions",()=>{
                Require(default(RuleQuantity)==Q(0)&&Q(6,9)==Q(2,3)&&Q(6,9).GetHashCode()==Q(2,3).GetHashCode()&&Q(2,3).ToString()=="2/3","Quantity normalization."); });
            cases.Add("quantity_exact_fractional_sum_scale_and_difference",()=>{
                Require(Q(2,3)+Q(1,6)==Q(5,6)&&Q(5,6)-Q(2,3)==Q(1,6)&&Q(1,4).Scale(1,10)==Q(1,40)
                    &&RuleQuantity.Sum(new[]{Q(2,3),Q(2,3),Q(2,3)})==Q(2),"Fractional goods rounded."); });
            cases.Add("quantity_wide_intermediates_reduce_before_bounds",()=>{
                Require(Q(long.MaxValue,2).Scale(2)==Q(long.MaxValue)
                    &&RuleQuantity.FromFraction((BigInteger)long.MaxValue*3,3)==Q(long.MaxValue)
                    &&Q(long.MaxValue,long.MaxValue-1)>Q(1),"Intermediate overflow or approximate compare."); });
            cases.Add("quantity_negative_zero_denominator_and_overflow_reject",()=>{
                Throws<ArgumentOutOfRangeException>(()=>Q(-1));Throws<ArgumentOutOfRangeException>(()=>Q(1,0));
                Throws<ArgumentOutOfRangeException>(()=>{var value=Q(0)-Q(1);});Throws<ArgumentOutOfRangeException>(()=>Q(1).Scale(-1));
                Throws<OverflowException>(()=>{var value=Q(long.MaxValue)+Q(1);});Throws<OverflowException>(()=>Q(long.MaxValue).Scale(2));
                Throws<OverflowException>(()=>Q(1,long.MaxValue).Scale(1,2));Throws<ArgumentNullException>(()=>RuleQuantity.Sum(null)); });
            cases.Add("carrying_four_sizes_match_authored_table",()=>{
                var sizes=new[]{CarrierSize.Tiny,CarrierSize.Small,CarrierSize.Medium,CarrierSize.Large};
                var pounds=new[]{Q(75),Q(150),Q(150),Q(300)};var loads=new[]{Q(5),Q(8),Q(10),Q(20)};var casualty=new[]{Q(3,2),Q(3),Q(6),Q(12)};
                for(int i=0;i<4;i++){var limits=PlaytestCarrying.Limits(sizes[i],10);
                    Require(limits.Pounds==pounds[i]&&limits.PushDragLiftPounds==pounds[i].Scale(2)&&limits.Load==loads[i]&&limits.CasualtyLoad==casualty[i],"Carrier size table mismatch.");} });
            cases.Add("carrying_current_strength_zero_and_extremes",()=>{
                Require(PlaytestCarrying.Limits(CarrierSize.Small,1).Load==Q(0)&&PlaytestCarrying.Limits(CarrierSize.Tiny,9).Load==Q(9,2)
                    &&PlaytestCarrying.Limits(CarrierSize.Large,int.MaxValue).PushDragLiftPounds==Q(128849018820),"Strength arithmetic or clamp.");
                Throws<ArgumentOutOfRangeException>(()=>PlaytestCarrying.Limits((CarrierSize)4,10));Throws<ArgumentOutOfRangeException>(()=>PlaytestCarrying.Limits(CarrierSize.Medium,-1)); });
            cases.Add("carrying_loaded_hawk_source_example",()=>{
                var limits=PlaytestCarrying.Limits(CarrierSize.Tiny,9);var external=new BurdenTotals(Q(30),Q(3),true);
                Require(limits.Pounds==Q(135,2)&&limits.Load==Q(9,2)&&PlaytestCarrying.CanCarry(limits,external)==true
                    &&PlaytestCarrying.IsBurdened(external.Load.Value,limits.Load),"Loaded Hawk example.");
                var rescued=PlaytestCarrying.Casualty(CarrierSize.Tiny,Q(180),false,new BurdenTotals(Q(60),Q(6),true));
                Require(rescued.Load==Q(15,2)&&rescued.Pounds==Q(240),"Rescuer omitted melded or external gear."); });
            cases.Add("carrying_half_full_zero_and_overload_thresholds",()=>{
                Require(!PlaytestCarrying.IsBurdened(Q(0),Q(0))&&!PlaytestCarrying.IsBurdened(Q(0),Q(10))
                    &&!PlaytestCarrying.IsBurdened(Q(499,100),Q(10))&&PlaytestCarrying.IsBurdened(Q(5),Q(10))
                    &&PlaytestCarrying.IsBurdened(Q(10),Q(10))&&!PlaytestCarrying.IsBurdened(Q(11),Q(10)),"Burden boundary changed."); });
            cases.Add("carrying_tiny_rational_capacity_comparison_does_not_overflow",()=>{
                var amount=Q(1,long.MaxValue);Require(PlaytestCarrying.IsBurdened(amount,amount),"Hypothetical half-capacity overflowed."); });
            cases.Add("carrying_burden_speed_reduction_clamps_and_preserves_fractions",()=>{
                Require(PlaytestCarrying.SpeedWithBurden(Q(30),true)==Q(20)&&PlaytestCarrying.SpeedWithBurden(Q(3),true)==Q(0)
                    &&PlaytestCarrying.SpeedWithBurden(Q(23,2),true)==Q(3,2)&&PlaytestCarrying.SpeedWithBurden(Q(30),false)==Q(30),"Burden Speed arithmetic."); });
            cases.Add("carrying_pounds_and_load_are_independent_checks",()=>{
                var limits=PlaytestCarrying.Limits(CarrierSize.Medium,10);
                Require(PlaytestCarrying.CanCarry(limits,new BurdenTotals(Q(150),Q(10),true))==true
                    &&PlaytestCarrying.CanCarry(limits,new BurdenTotals(Q(151),Q(1),true))==false
                    &&PlaytestCarrying.CanCarry(limits,new BurdenTotals(Q(1),Q(11),true))==false,"Only one carrying quantity checked."); });
            cases.Add("carrying_unknown_is_not_zero_or_automatic_permission",()=>{
                var limits=PlaytestCarrying.Limits(CarrierSize.Medium,10);
                Require(PlaytestCarrying.CanCarry(limits,new BurdenTotals(null,Q(1),false))==null
                    &&PlaytestCarrying.CanCarry(limits,new BurdenTotals(Q(1),null,true))==null
                    &&PlaytestCarrying.CanCarry(limits,new BurdenTotals(null,Q(11),false))==false,"Unknown measure granted permission or erased known overload."); });
            cases.Add("carrying_push_drag_limits_and_current_speed",()=>{
                var limits=PlaytestCarrying.Limits(CarrierSize.Medium,18);
                Require(PlaytestCarrying.PushDragSpeed(limits,Q(270),Q(30))==Q(30)&&PlaytestCarrying.PushDragSpeed(limits,Q(271),Q(30))==Q(5)
                    &&PlaytestCarrying.PushDragSpeed(limits,Q(540),Q(3))==Q(3)&&PlaytestCarrying.PushDragSpeed(limits,Q(540),Q(0))==Q(0)
                    &&PlaytestCarrying.PushDragSpeed(limits,Q(541),Q(30))==null&&PlaytestCarrying.CanLift(limits,Q(540))&&!PlaytestCarrying.CanLift(limits,Q(541)),"Push/drag/lift bounds."); });
            cases.Add("carrying_petrified_stone_casualty_source_example",()=>{
                var body=PlaytestCarrying.Casualty(CarrierSize.Medium,Q(180),true,new BurdenTotals(Q(0),Q(0),true));
                var rescuer=PlaytestCarrying.Limits(CarrierSize.Medium,18);
                Require(body.Pounds==Q(1800)&&body.Load==Q(6)&&!PlaytestCarrying.CanLift(rescuer,body.Pounds.Value)
                    &&PlaytestCarrying.CanCarry(rescuer,body)==false,"Petrified altered casualty Load or became movable."); });
            cases.Add("carrying_body_weight_does_not_depend_on_size_or_repeat_condition",()=>{
                Require(PlaytestCarrying.BodyPounds(Q(180),false)==Q(180)&&PlaytestCarrying.BodyPounds(Q(180),true)==Q(1800),"Base body weight changed.");
                var gear=new BurdenTotals(Q(30),Q(3),true);var a=PlaytestCarrying.Casualty(CarrierSize.Tiny,Q(180),true,gear);
                var b=PlaytestCarrying.Casualty(CarrierSize.Large,Q(180),true,gear);
                Require(a.Pounds==Q(1830)&&b.Pounds==a.Pounds&&a.Load==Q(9,2)&&b.Load==Q(15),"Body condition multiplied gear or size changed mass."); });
            cases.Add("carrying_estimated_mass_cannot_satisfy_documented_mass",()=>{
                var total=PlaytestCarrying.Total(new[]{B("load-only",load:Q(3,2))});
                Require(total.Pounds==Q(15)&&total.Load==Q(3,2)&&!total.PoundsDocumented,"Load estimate not labeled.");
                Throws<InvalidOperationException>(()=>total.RequireDocumentedPounds());
                Require(PlaytestCarrying.CanCarry(PlaytestCarrying.Limits(CarrierSize.Medium,10),total)==true,"Ordinary hauling estimate was forbidden."); });
            cases.Add("carrying_printed_load_wins_and_weight_fallback_is_exact",()=>{
                var total=PlaytestCarrying.Total(new[]{B("printed",Q(1),Q(3)),B("quarter",Q(1,4))});
                Require(total.RequireDocumentedPounds()==Q(5,4)&&total.Load==Q(121,40),"Printed Load replaced or fractional weight rounded."); });
            cases.Add("carrying_empty_and_unknown_item_totals",()=>{
                var empty=PlaytestCarrying.Total(Array.Empty<BurdenItem>());var unknown=PlaytestCarrying.Total(new[]{B("unknown")});
                Require(empty.Pounds==Q(0)&&empty.Load==Q(0)&&empty.PoundsDocumented&&unknown.Pounds==null&&unknown.Load==null&&!unknown.PoundsDocumented,"Unknown item disappeared."); });
            cases.Add("carrying_nested_empty_containers_and_contents_count_once",()=>{
                var items=new[]{B("pack",Q(2),Q(1,5)),B("box",Q(1),Q(1,10),"pack"),B("goods",Q(5),Q(1,2),"box")};
                var total=PlaytestCarrying.Total(items);var reversed=PlaytestCarrying.Total(items.Reverse());
                Require(total.Pounds==Q(8)&&total.Load==Q(4,5)&&reversed.Pounds==total.Pounds&&reversed.Load==total.Load,"Nested counting depends on input order or erases contents."); });
            cases.Add("carrying_inclusive_load_does_not_make_weight_inclusive",()=>{
                var total=PlaytestCarrying.Total(new[]{B("bag",Q(2),Q(1),loadContents:new[]{"child"}),B("child",Q(8),Q(4,5),"bag")});
                Require(total.Pounds==Q(10)&&total.Load==Q(1),"Inclusive Load suppressed contents weight."); });
            cases.Add("carrying_inclusive_weight_does_not_make_load_inclusive",()=>{
                var total=PlaytestCarrying.Total(new[]{B("bag",Q(10),Q(1,5),poundContents:new[]{"child"}),B("child",Q(8),Q(4,5),"bag")});
                Require(total.Pounds==Q(10)&&total.Load==Q(1),"Inclusive pounds suppressed contents Load."); });
            cases.Add("carrying_independent_explicit_coverage_sets",()=>{
                var total=PlaytestCarrying.Total(new[]{B("bag",Q(4),Q(3),poundContents:new[]{"a"},loadContents:new[]{"b"}),
                    B("a",Q(3),Q(1),"bag"),B("b",Q(5),Q(2),"bag")});
                Require(total.Pounds==Q(9)&&total.Load==Q(4),"Coverage leaked between units."); });
            cases.Add("carrying_inclusive_mass_cannot_hide_child_printed_load",()=>{
                var total=PlaytestCarrying.Total(new[]{B("bag",Q(20),poundContents:new[]{"child"}),B("child",load:Q(3),parent:"bag")});
                Require(total.Pounds==Q(20)&&total.PoundsDocumented&&total.Load==null,"Gross mass fallback masked printed child Load."); });
            cases.Add("carrying_inclusive_load_cannot_hide_child_documented_mass",()=>{
                var total=PlaytestCarrying.Total(new[]{B("bag",load:Q(2),loadContents:new[]{"child"}),B("child",Q(100),parent:"bag")});
                Require(total.Load==Q(2)&&total.Pounds==null&&!total.PoundsDocumented,"Gross Load estimate masked actual child mass."); });
            cases.Add("carrying_inclusive_values_below_known_contents_reject",()=>{
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("bag",Q(2),poundContents:new[]{"child"}),B("child",Q(3),parent:"bag")}));
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("bag",load:Q(2),loadContents:new[]{"child"}),B("child",load:Q(3),parent:"bag")})); });
            cases.Add("carrying_partial_aggregate_overlap_requires_exact_decomposition",()=>{
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("root",Q(10),poundContents:new[]{"box"}),
                    B("box",Q(5),parent:"root",poundContents:new[]{"child"}),B("child",Q(2),parent:"box")})); });
            cases.Add("carrying_root_total_cannot_hide_conflicting_nested_aggregates",()=>{
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("root",Q(200),poundContents:new[]{"box","child","leaf"}),
                    B("box",Q(100),parent:"root",poundContents:new[]{"child"}),
                    B("child",Q(300),parent:"box",poundContents:new[]{"leaf"}),B("leaf",Q(10),parent:"child")}));
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("root",Q(200),poundContents:new[]{"box","child","leaf"}),
                    B("box",Q(100),parent:"root",poundContents:new[]{"child","leaf"}),
                    B("child",Q(300),parent:"box",poundContents:new[]{"leaf"}),B("leaf",Q(10),parent:"child")})); });
            cases.Add("carrying_known_root_total_accepts_consistent_crossing_children",()=>{
                var total=PlaytestCarrying.Total(new[]{B("root",Q(30),poundContents:new[]{"box","child","leaf"}),
                    B("box",Q(12),parent:"root",poundContents:new[]{"child"}),
                    B("child",Q(11),parent:"box",poundContents:new[]{"leaf"}),B("leaf",Q(1),parent:"child")});
                Require(total.RequireDocumentedPounds()==Q(30)&&total.Load==null,"Known root mass rejected or unknown Load invented."); });
            cases.Add("carrying_nested_fully_covered_aggregate_not_double_counted",()=>{
                var total=PlaytestCarrying.Total(new[]{B("root",Q(10),Q(1),poundContents:new[]{"box","child"},loadContents:new[]{"box","child"}),
                    B("box",Q(5),Q(1,2),"root",new[]{"child"},new[]{"child"}),B("child",Q(2),Q(1,5),"box")});
                Require(total.Pounds==Q(10)&&total.Load==Q(1),"Inclusive subtree counted twice."); });
            cases.Add("carrying_missing_cycle_duplicate_and_non_descendant_reject",()=>{
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("a",parent:"missing")}));
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("a",parent:"b"),B("b",parent:"a")}));
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("a"),B("a")}));
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(new[]{B("a",Q(1),poundContents:new[]{"b"}),B("b",Q(1))}));
                Throws<ArgumentException>(()=>B("a",poundContents:new[]{"b"})); });
            cases.Add("carrying_input_collections_are_detached_readonly",()=>{
                var contents=new[]{"child"};var item=B("bag",Q(2),poundContents:contents);contents[0]="forged";
                Require(item.PoundsIncludes.Single()=="child","Caller mutated inclusive coverage.");
                Throws<NotSupportedException>(()=>((IList<string>)item.PoundsIncludes).Clear()); });
            cases.Add("carrying_session_capacity_and_exact_overflow_fail_closed",()=>{
                Throws<ArgumentException>(()=>PlaytestCarrying.Total(Enumerable.Range(0,257).Select(i=>B("item"+i,Q(0)))));
                Throws<OverflowException>(()=>PlaytestCarrying.Total(new[]{B("a",Q(long.MaxValue)),B("b",Q(1))}));
                Throws<OverflowException>(()=>PlaytestCarrying.BodyPounds(Q(long.MaxValue),true));
                Throws<ArgumentException>(()=>new BurdenTotals(null,Q(1),true)); });
        }
    }
}
#endif
