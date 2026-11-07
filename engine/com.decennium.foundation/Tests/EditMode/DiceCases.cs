#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddDiceCases(Dictionary<string,Action> cases)
        {
            cases.Add("dice_advantage_presence_cancellation_not_source_count", () => {
                Require(PlaytestDice.Selection(0,0)==D20Selection.Normal
                    && PlaytestDice.Selection(3,0)==D20Selection.Advantage
                    && PlaytestDice.Selection(0,3)==D20Selection.Disadvantage
                    && PlaytestDice.Selection(3,1)==D20Selection.Normal
                    && PlaytestDice.Selection(1,int.MaxValue)==D20Selection.Normal,"Any opposing source cancels, without counting votes."); });
            cases.Add("dice_seed_one_literal_nonzero_domain_mapping", () => {
                var a=DiceStream.Draw(1,20);var b=DiceStream.Draw(a.NextState,20);
                Require(a.NextState==270369 && a.Value==8 && a.WordsConsumed==1
                    && b.NextState==67634689 && b.Value==8 && b.WordsConsumed==1,"Known xorshift words minus one before modulo."); });
            cases.Add("dice_advantage_and_disadvantage_consume_two_dice", () => {
                var a=PlaytestDice.RollD20(123456789,1);var b=PlaytestDice.RollD20(123456789,0,1);
                // Independent xorshift vectors: 2714967881,2238813396 => faces1 and16.
                Require(a.First==1 && a.Second==16 && a.Natural==16 && b.Natural==1
                    && a.NextRandomState==2238813396 && a.NextRandomState==b.NextRandomState && a.WordsConsumed==2,"Higher/lower exactly two d20s."); });
            cases.Add("dice_cancelled_roll_consumes_only_one_die", () => {
                var normal=PlaytestDice.RollD20(123456789);var cancelled=PlaytestDice.RollD20(123456789,100,1);
                Require(cancelled.Second==null && cancelled.Natural==normal.Natural && cancelled.NextRandomState==normal.NextRandomState
                    && cancelled.WordsConsumed==normal.WordsConsumed,"Cancellation before rolling."); });
            cases.Add("dice_invalid_requests_rejected", () => {
                Throws<ArgumentException>(()=>DiceStream.Draw(0,20));
                Throws<ArgumentOutOfRangeException>(()=>DiceStream.Draw(1,0));
                Throws<ArgumentOutOfRangeException>(()=>DiceStream.Draw(1,-1));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestDice.RollD20(1,-1));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestDice.RollD20(1,0,-1)); });
            cases.Add("dice_rejection_tail_and_exact_acceptance_boundary", () => {
                // Seeds obtained by independently inverting the three xor/shift transforms.
                // A d20 retains4294967280 of the4294967295 nonzero words.
                var max=DiceStream.Draw(1584200935,20);
                var firstRejected=DiceStream.Draw(3632016218,20);
                var lastAccepted=DiceStream.Draw(717860467,20);
                Require(max.NextState==253983 && max.Value==2 && max.WordsConsumed==2
                    && firstRejected.NextState==3809745 && firstRejected.Value==4 && firstRejected.WordsConsumed==2
                    && lastAccepted.NextState==4294967280 && lastAccepted.Value==19 && lastAccepted.WordsConsumed==1,
                    "Reject the excess tail, then use the next authoritative word.");
                Require(DiceStream.Draw(1584200935,1).WordsConsumed==1,"One outcome retains the complete nonzero domain."); });
            cases.Add("dice_replay_state_and_boundaries", () => {
                uint state=17;
                foreach(int bound in new[]{1,2,4,6,8,10,12,20,int.MaxValue}) {
                    var a=DiceStream.Draw(state,bound);var b=DiceStream.Draw(state,bound);
                    Require(a.Value>=0 && a.Value<bound && a.NextState!=0 && a.WordsConsumed>=1
                        && a.Value==b.Value && a.NextState==b.NextState && a.WordsConsumed==b.WordsConsumed,"Bounded deterministic draw.");
                    state=a.NextState;
                } });
            cases.Add("shared_rule_d20_matches_lab_adapter_and_keeps_trace", () => {
                var core = RuleDice.RollD20(123456789, 1, 0);
                var lab = PlaytestDice.RollD20(123456789, 1, 0);
                Require(core.Selection == RuleD20Selection.Advantage && core.First == 1 && core.Second == 16
                    && core.Natural == 16 && core.NextRandomState == 2238813396 && core.WordsConsumed == 2
                    && (int)core.Selection == (int)lab.Selection && core.First == lab.First && core.Second == lab.Second
                    && core.Natural == lab.Natural && core.NextRandomState == lab.NextRandomState
                    && core.WordsConsumed == lab.WordsConsumed, "Core and gated adapter must share one exact RNG path."); });
            cases.Add("shared_rule_d20_rejects_invalid_modifier_counts_and_zero_state", () => {
                Throws<ArgumentOutOfRangeException>(() => RuleDice.SelectD20(-1, 0));
                Throws<ArgumentOutOfRangeException>(() => RuleDice.SelectD20(0, -1));
                Throws<ArgumentException>(() => RuleDice.RollD20(0)); });
        }
    }
}
#endif
