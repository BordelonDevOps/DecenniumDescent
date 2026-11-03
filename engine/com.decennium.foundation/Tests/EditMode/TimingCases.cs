#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static RuleTime T(long numerator,long denominator=1) => new RuleTime(numerator,denominator);
        private static void AddTimingCases(Dictionary<string,Action> cases)
        {
            cases.Add("time_exact_rational_normalization_and_default", () => {
                Require(T(2,6)==T(1,3) && default(RuleTime)==T(0) && T(0,long.MaxValue).Denominator==1
                    && T(1,3).AddSeconds(6)==T(19,3) && T(2,6).GetHashCode()==T(1,3).GetHashCode(),"Exact fractions and zero."); });
            cases.Add("time_comparison_widens_intermediate_products", () => {
                var a=T(long.MaxValue,long.MaxValue-1);var b=T(long.MaxValue-1,long.MaxValue-2);
                Require(a<b && b>a && a>=T(1) && a<=b && a!=b,"Cross-products must not wrap or round.");
                Require(T(long.MaxValue).AddSeconds(0)==T(long.MaxValue),"Maximum representable integer."); });
            cases.Add("time_invalid_fraction_and_overflow_rejected", () => {
                Throws<ArgumentOutOfRangeException>(()=>T(-1));Throws<ArgumentOutOfRangeException>(()=>T(1,0));
                Throws<ArgumentOutOfRangeException>(()=>T(1,-1));Throws<ArgumentOutOfRangeException>(()=>T(0).AddSeconds(-1));
                Throws<OverflowException>(()=>T(long.MaxValue).AddSeconds(1)); });
            cases.Add("time_future_target_end_and_current_end_exclusion", () => {
                Require(PlaytestTiming.MarkerDeadline(T(1),T(3),2)==T(9)
                    && PlaytestTiming.MarkerDeadline(T(1),T(3),2,T(3))==T(15)
                    && PlaytestTiming.MarkerDeadline(T(1),T(3),1,T(3))==T(9),"Count future markers, excluding only the specific current end."); });
            cases.Add("time_marker_at_or_after_excluded_end_does_not_double_skip", () => {
                Require(PlaytestTiming.MarkerDeadline(T(3),T(3),1,T(3))==T(9)
                    && PlaytestTiming.MarkerDeadline(T(4),T(3),1,T(3))==T(9)
                    && PlaytestTiming.MarkerDeadline(T(0),T(0))==T(6),"Strictly future marker."); });
            cases.Add("time_source_three_round_buff_and_absolute_duration", () => {
                Require(PlaytestTiming.MarkerDeadline(T(1,2),T(0),3)==T(18)
                    && PlaytestTiming.AbsoluteDuration(T(2),3)==T(20),"Source turn4 start; outside initiative absolute deadline."); });
            cases.Add("time_fractional_phase_and_preserved_virtual_schedule", () => {
                var original=PlaytestTiming.MarkerDeadline(T(1,3),T(2,3),2);
                Require(original==T(20,3) && PlaytestTiming.MarkerDeadline(T(1,3),T(20,3),2)==original,"Phase-equivalent virtual markers.");
                Require(PlaytestTiming.MarkerDeadline(T(20,3),T(2,3))==T(38,3),"Strict next rational occurrence."); });
            cases.Add("time_ready_effect_begins_on_release", () => {
                Require(PlaytestTiming.ReadyEffectDeadline(T(0),T(4),3)==T(22)
                    && PlaytestTiming.ReadyEffectDeadline(T(1),T(4),3,T(3))==T(21),"Preparation does not start manifested effect duration.");
                Throws<ArgumentException>(()=>PlaytestTiming.ReadyEffectDeadline(T(4),T(1),3)); });
            cases.Add("time_invalid_counts_and_unrepresentable_deadline", () => {
                Throws<ArgumentOutOfRangeException>(()=>PlaytestTiming.MarkerDeadline(T(1),T(3),0));
                Throws<ArgumentOutOfRangeException>(()=>PlaytestTiming.AbsoluteDuration(T(0),-1));
                Throws<OverflowException>(()=>PlaytestTiming.MarkerDeadline(T(long.MaxValue),T(0)));
                Throws<OverflowException>(()=>PlaytestTiming.AbsoluteDuration(T(long.MaxValue),1)); });
            cases.Add("time_effect_application_sequence_and_ordinal_ties", () => {
                var input=new[]{new EffectOrderRecord("b","A",T(1),1),new EffectOrderRecord("a","B",T(1),1),
                    new EffectOrderRecord("z","Z",T(0),100),new EffectOrderRecord("c","A",T(1),1),new EffectOrderRecord("d","Z",T(1),0)};
                var sorted=PlaytestTiming.OrderedEffects(input);Array.Reverse(input);
                Require(sorted.Select(x=>x.ApplicationId).SequenceEqual(new[]{"z","d","b","c","a"}),"Timestamp, sequence, mechanical ID, application ID.");
                Throws<NotSupportedException>(()=>((IList<EffectOrderRecord>)sorted).Clear()); });
            cases.Add("time_ordering_rejects_duplicate_or_invalid_records", () => {
                var r=new EffectOrderRecord("a","effect",T(0),0);
                Throws<ArgumentException>(()=>PlaytestTiming.OrderedEffects(new[]{r,r}));
                Throws<ArgumentException>(()=>PlaytestTiming.OrderedEffects(new EffectOrderRecord[]{null}));
                Throws<ArgumentNullException>(()=>PlaytestTiming.OrderedEffects(null));
                Throws<ArgumentException>(()=>new EffectOrderRecord("bad|id","effect",T(0),0));
                Throws<ArgumentException>(()=>new EffectOrderRecord("a","effect",T(0),-1)); });
        }
    }
}
#endif
