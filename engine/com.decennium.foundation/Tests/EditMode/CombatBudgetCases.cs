#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddCombatBudgetCases(Dictionary<string,Action> cases)
        {
            cases.Add("combat_movement_spent_cost_survives_mode_changes", () => {
                var m=new MovementLedger().Spend(PlaytestCombatBudgets.MovementCost(10,TerrainCost.Difficult),30);
                Require(m.Spent==20 && m.Remaining(30)==10 && m.Remaining(15)==0 && m.Remaining(40)==20 && m.Remaining(30)==10,"Speed changes never refund spent cost."); });
            cases.Add("combat_multiple_legal_dashes_add_current_speed", () => {
                var m=new MovementLedger(20).AddPaidDash();
                Require(m.Remaining(30)==40 && m.AddPaidDash().Remaining(30)==70 && m.Spent==20,"Every paid Dash adds a current Speed."); });
            cases.Add("combat_standing_floor_and_zero_speed", () => {
                Require(new MovementLedger().Stand(30).Remaining(30)==15 && new MovementLedger().Stand(25).Spent==12,"Half speed rounded down.");
                Throws<ArgumentException>(()=>new MovementLedger().Stand(0));
                Throws<ArgumentException>(()=>new MovementLedger(20).Stand(30)); });
            cases.Add("combat_rejected_movement_preserves_ledger", () => {
                var m=new MovementLedger(20);
                Throws<ArgumentException>(()=>m.Spend(11,30));
                Throws<ArgumentException>(()=>m.Spend(-1,30));
                Require(m.Spent==20 && m.Dashes==0,"Rejected spend changed ledger."); });
            cases.Add("combat_terrain_crawl_squeeze_additive", () => {
                Require(PlaytestCombatBudgets.MovementCost(5,TerrainCost.Difficult,true,true)==20
                    && PlaytestCombatBudgets.MovementCost(5,TerrainCost.Severe,true)==20
                    && PlaytestCombatBudgets.MovementCost(5,TerrainCost.Normal)==5,"Strongest terrain plus crawl/squeeze."); });
            cases.Add("combat_separate_special_budgets", () => {
                Require(!PlaytestCombatBudgets.CanSpecialMove(SpecialMovement.Interpose,30,5,TerrainCost.Difficult)
                    && PlaytestCombatBudgets.CanSpecialMove(SpecialMovement.Press,30,5)
                    && !PlaytestCombatBudgets.CanSpecialMove(SpecialMovement.Press,0,5)
                    && PlaytestCombatBudgets.CanSpecialMove(SpecialMovement.Interpose,0,0)
                    && PlaytestCombatBudgets.SpecialBudget(SpecialMovement.Ready,20)==20
                    && PlaytestCombatBudgets.SpecialBudget(SpecialMovement.Withdraw,25)==12,"No ordinary movement refund."); });
            cases.Add("combat_movement_invalid_inputs_and_overflow", () => {
                Throws<ArgumentOutOfRangeException>(()=>new MovementLedger(-1));
                Throws<ArgumentOutOfRangeException>(()=>new MovementLedger(0,-1));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestCombatBudgets.MovementCost(5,(TerrainCost)0));
                Throws<ArgumentException>(()=>PlaytestCombatBudgets.SpecialBudget((SpecialMovement)100,30));
                Throws<ArgumentException>(()=>PlaytestCombatBudgets.SpecialBudget(SpecialMovement.Ready,-1));
                Throws<OverflowException>(()=>PlaytestCombatBudgets.MovementCost(long.MaxValue,TerrainCost.Difficult));
                Throws<OverflowException>(()=>new MovementLedger(dashes:1).Remaining(long.MaxValue));
                Throws<OverflowException>(()=>new MovementLedger(dashes:int.MaxValue).AddPaidDash()); });
            cases.Add("combat_movement_285_sampled_mode_states", () => {
                int count=0;
                for(int spent=0;spent<=90;spent+=5) foreach(int speed in new[]{0,5,15,30,60}) foreach(int dashes in new[]{0,1,2}) {
                    var m=new MovementLedger(spent,dashes);long cap=(1L+dashes)*speed;
                    long remaining=m.Remaining(speed);m.Remaining(0);m.Remaining(60);
                    Require(remaining>=0 && remaining<=cap && remaining+spent==Math.Max(cap,spent) && m.Spent==spent,"Spent-cost conservation.");count++;
                }
                Require(count==285,"Sample set changed."); });
            cases.Add("combat_reaction_initial_then_own_start_same_round", () => {
                var r=new ReactionClock().Spend();var refreshed=r.RegularStart(0);
                Require(!r.Available && refreshed.Available && !refreshed.Spend().Available,"May react twice separated by own regular start in same numbered round."); });
            cases.Add("combat_reaction_extra_turn_and_round_do_not_refresh", () => {
                var r=new ReactionClock().RegularStart(0).Spend().ExtraTurn().RoundBoundary();
                Require(!r.Available,"No round or extra-turn refresh.");
                Throws<ArgumentException>(()=>r.Spend());
                Throws<ArgumentException>(()=>r.RegularStart(0));
                Require(r.RegularStart(1).Available,"Next regular start refreshes."); });
            cases.Add("combat_surprise_blocks_until_first_regular_end", () => {
                var r=new ReactionClock(surprisePending:true);
                Throws<ArgumentException>(()=>r.Spend());
                Throws<ArgumentException>(()=>r.EndFirstRegularTurn());
                r=r.RegularStart(0);Throws<ArgumentException>(()=>r.Spend());
                Require(!r.EndFirstRegularTurn().Spend().Available,"Surprise ends after first regular turn."); });
            cases.Add("combat_reaction_prohibition_preserves_available_resource", () => {
                var r=new ReactionClock();Throws<ArgumentException>(()=>r.Spend(prohibited:true));
                Require(r.Available && r.LastRegularStart==-1,"Prohibition must not spend.");
                Throws<ArgumentException>(()=>r.RegularStart(-1));
                Throws<ArgumentOutOfRangeException>(()=>new ReactionClock(lastRegularStart:-2)); });
            cases.Add("combat_extra_action_cap_and_no_recursive_grant", () => {
                var c=new ExtraActionClock().Spend(1);
                Throws<ArgumentException>(()=>c.Spend(1));
                Throws<ArgumentException>(()=>c.Spend(2,true));
                Require(c.Spend(2).SpentRounds.SequenceEqual(new[]{1L,2L}) && c.SpentRounds.SequenceEqual(new[]{1L}),"One separately granted extra Action per numbered round."); });
            cases.Add("combat_extra_action_history_detached_and_validated", () => {
                var a=new[]{2L,1L};var c=new ExtraActionClock(a);a[0]=99;
                Require(c.SpentRounds.SequenceEqual(new[]{1L,2L}),"Detached stable history.");
                Throws<NotSupportedException>(()=>((IList<long>)c.SpentRounds).Clear());
                Throws<ArgumentException>(()=>new ExtraActionClock(new[]{1L,1L}));
                Throws<ArgumentException>(()=>new ExtraActionClock().Spend(0)); });
            cases.Add("combat_reinforcement_complete_ordered_slot", () => {
                Require(PlaytestCombatBudgets.ReinforcementFirstRound(3,true)==3
                    && PlaytestCombatBudgets.ReinforcementFirstRound(3,false)==4
                    && PlaytestCombatBudgets.ReinforcementFirstRound(3,true,true)==4,"Exact slot counts as passed; end-round entry waits.");
                Throws<ArgumentOutOfRangeException>(()=>PlaytestCombatBudgets.ReinforcementFirstRound(0,true));
                Throws<OverflowException>(()=>PlaytestCombatBudgets.ReinforcementFirstRound(long.MaxValue,false)); });
        }
    }
}
#endif
