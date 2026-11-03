#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddPrototypePolicyCases(Dictionary<string,Action> cases)
        {
            cases.Add("prototype_jump_runup_strength_and_modifier_examples",()=>{
                var jump=PrototypeTraversal.JumpLimits(15,true);
                Require(jump.HorizontalFeet==15m && jump.VerticalFeet==5m && PrototypeTraversal.RequiredRunUpFeet==10,"Approved run-up limits.");
                jump=PrototypeTraversal.JumpLimits(9,true);
                Require(jump.HorizontalFeet==9m && jump.VerticalFeet==2m,"Negative modifier must use floor division."); });
            cases.Add("prototype_standing_jump_retains_half_foot_limits",()=>{
                var jump=PrototypeTraversal.JumpLimits(15,false);
                Require(jump.HorizontalHalfFeet==15 && jump.VerticalHalfFeet==5 && jump.HorizontalFeet==7.5m && jump.VerticalFeet==2.5m,"Standing limits were rounded."); });
            cases.Add("prototype_jump_zero_low_and_large_scores",()=>{
                for(int score=0;score<=5;score++)Require(PrototypeTraversal.JumpLimits(score,true).VerticalFeet==0,"Low-strength vertical floor.");
                var max=PrototypeTraversal.JumpLimits(int.MaxValue,true);
                Require(max.HorizontalHalfFeet==4294967294L && max.VerticalFeet==1073741821m,"Wide strength arithmetic.");
                Throws<ArgumentOutOfRangeException>(()=>PrototypeTraversal.JumpLimits(-1,true)); });
            cases.Add("prototype_run_requires_paid_dash_and_exact_double_pace",()=>{
                Require(PrototypeTraversal.RunningPace(2.5m,true)==5m && PrototypeTraversal.RunningPace(0,true)==0,"Running pace ratio.");
                Throws<ArgumentException>(()=>PrototypeTraversal.RunningPace(5,false));
                Throws<ArgumentOutOfRangeException>(()=>PrototypeTraversal.RunningPace(-1,true));
                Throws<OverflowException>(()=>PrototypeTraversal.RunningPace(decimal.MaxValue,true)); });
            cases.Add("prototype_ordinary_climb_swim_add_one_per_foot",()=>{
                Require(PrototypeTraversal.MovementCost(7,OrdinaryTraversal.Climb)==14
                    && PrototypeTraversal.MovementCost(7,OrdinaryTraversal.Swim)==14
                    && PrototypeTraversal.MovementCost(7,OrdinaryTraversal.Walk)==7,"Ordinary traversal surcharge."); });
            cases.Add("prototype_running_pace_rejects_decimal_precision_loss",()=>{
                Throws<OverflowException>(()=>PrototypeTraversal.RunningPace(7.9228162514264337593543950331m,true));
                Require(PrototypeTraversal.RunningPace(7.9228162514264337593543950330m,true)==15.845632502852867518708790066m,
                    "Exactly representable double with removable trailing zero was rejected."); });
            cases.Add("prototype_dedicated_speed_removes_only_traversal_surcharge",()=>{
                foreach(var mode in new[]{OrdinaryTraversal.Climb,OrdinaryTraversal.Swim}) {
                    Require(PrototypeTraversal.MovementCost(5,mode,true,TerrainCost.Difficult)==10
                        && PrototypeTraversal.MovementCost(5,mode,false,TerrainCost.Difficult)==15
                        && PrototypeTraversal.MovementCost(5,mode,false,TerrainCost.Severe,true,true)==30,"Terrain/crawl/squeeze and mode surcharge composition.");
                } });
            cases.Add("prototype_traversal_invalid_inputs_and_overflow_reject",()=>{
                Throws<ArgumentException>(()=>PrototypeTraversal.MovementCost(1,(OrdinaryTraversal)99));
                Throws<ArgumentOutOfRangeException>(()=>PrototypeTraversal.MovementCost(-1,OrdinaryTraversal.Climb));
                Throws<ArgumentOutOfRangeException>(()=>PrototypeTraversal.MovementCost(1,OrdinaryTraversal.Swim,terrain:(TerrainCost)0));
                Throws<OverflowException>(()=>PrototypeTraversal.MovementCost(long.MaxValue,OrdinaryTraversal.Swim)); });
            cases.Add("prototype_exploration_advances_exact_one_to_one",()=>{
                Require(PrototypeClock.Exploration(T(1,3),T(2,3),SoloPause.None)==T(1),"Exact real/game delta ratio.");
                var now=T(0);for(int i=0;i<10;i++)now=PrototypeClock.Exploration(now,T(1,10),SoloPause.None);
                Require(now==T(1),"Frame-sized fractions accumulated rounding."); });
            cases.Add("prototype_every_solo_pause_reason_freezes_shared_time",()=>{
                for(int flags=1;flags<=15;flags++)Require(PrototypeClock.Exploration(T(7),T(100),(SoloPause)flags)==T(7),"Pause did not freeze.");
                Throws<ArgumentException>(()=>PrototypeClock.Exploration(T(0),T(1),(SoloPause)16)); });
            cases.Add("prototype_exploration_stops_at_earliest_supplied_milestone",()=>{
                Require(PrototypeClock.Exploration(T(1),T(10),SoloPause.None,T(5,3))==T(5,3),"Skipped an intervening milestone.");
                Require(PrototypeClock.Exploration(T(1),T(10),SoloPause.None,T(1))==T(1),"Due decision/barrier was skipped.");
                Throws<ArgumentException>(()=>PrototypeClock.Exploration(T(2),T(1),SoloPause.None,T(1))); });
            cases.Add("prototype_declared_activities_spend_time_in_bounded_segments",()=>{
                Require(PrototypeClock.DeclaredActivity(T(0),T(3600),T(300))==T(300)
                    && PrototypeClock.DeclaredActivity(T(300),T(3600),T(4000))==T(3600),"Activity skipped boundary or over-advanced.");
                Throws<ArgumentException>(()=>PrototypeClock.DeclaredActivity(T(2),T(1)));
                Throws<ArgumentException>(()=>PrototypeClock.DeclaredActivity(T(2),T(3),T(1))); });
            cases.Add("prototype_clock_bounds_before_unrepresentable_target",()=>{
                var now=T(long.MaxValue-1);
                Require(PrototypeClock.Exploration(now,T(2),SoloPause.None,T(long.MaxValue))==T(long.MaxValue)
                    && PrototypeClock.Exploration(now,T(2),SoloPause.None,now)==now,"Representable earlier barrier rejected.");
                Throws<OverflowException>(()=>PrototypeClock.Exploration(now,T(2),SoloPause.None)); });
            cases.Add("prototype_restore_never_awards_offline_time",()=>{
                Require(PrototypeClock.RestoreAfterOffline(T(100,3))==T(100,3),"Offline restore changed game time."); });
            cases.Add("prototype_round_total_six_seconds_for_any_checkpoint_count",()=>{
                foreach(int count in new[]{1,2,3,7,64}) {
                    var round=new PrototypeRoundWindow(T(1,3),T(1,3));
                    for(int i=1;i<=count;i++)round=round.AdvanceTo(T(count+18L*i,3L*count),SoloPause.None);
                    Require(round.Complete && round.Current==T(19,3) && round.AdvanceTo(round.End,SoloPause.None).Current==T(19,3),"Round time multiplied by participant count or retry.");
                } });
            cases.Add("prototype_round_decisions_pause_and_deadlines_interrupt_resolution",()=>{
                var round=new PrototypeRoundWindow(T(10),T(10));
                Require(round.AdvanceTo(T(16),SoloPause.TacticalDecision).Current==T(10),"Decision time advanced.");
                round=round.AdvanceTo(T(16),SoloPause.None,T(23,2));
                Require(round.Current==T(23,2) && !round.Complete && round.End==T(16),"Deadline altered round end.");
                Require(round.AdvanceTo(round.End,SoloPause.None).Complete,"Resolution cannot continue."); });
            cases.Add("prototype_round_reversal_overrun_and_overflow_reject",()=>{
                Throws<ArgumentException>(()=>new PrototypeRoundWindow(T(1),T(0)));
                Throws<ArgumentException>(()=>new PrototypeRoundWindow(T(1),T(8)));
                Throws<OverflowException>(()=>new PrototypeRoundWindow(T(long.MaxValue),T(long.MaxValue)));
                var round=new PrototypeRoundWindow(T(0),T(2));
                Throws<ArgumentException>(()=>round.AdvanceTo(T(1),SoloPause.None));
                Throws<ArgumentException>(()=>round.AdvanceTo(T(7),SoloPause.None));
                Throws<ArgumentException>(()=>round.AdvanceTo(T(3),(SoloPause)16)); });
        }
    }
}
#endif
