#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        // Literal expectations from CORE_RESOLUTION_PLAYTEST.md, Rolls, and the existing
        // validate_core_playtests.py examples. Boundary cases are derived from the prose,
        // not generated from the resolver under test. See SOURCE_BINDINGS.json.
        private static void AddRollCases(Dictionary<string, Action> cases)
        {
            cases.Add("roll_attack_natural_one_misses", () => {
                var r = PlaytestRolls.AttackRoll(1, 100, 10);
                Require(r.Total == 101 && !r.Hit && !r.Critical, "Natural 1 must miss."); });
            cases.Add("roll_attack_natural_twenty_hits_and_crits", () => {
                var r = PlaytestRolls.AttackRoll(20, -5, 99);
                Require(r.Total == 15 && r.Hit && r.Critical, "Natural 20 must hit and crit."); });
            cases.Add("roll_attack_meets_ac", () => {
                var r = PlaytestRolls.AttackRoll(10, 2, 12);
                Require(r.Hit && !r.Critical, "Meeting AC must hit without a critical."); });
            cases.Add("roll_attack_large_margin_does_not_crit", () => {
                var r = PlaytestRolls.AttackRoll(10, 15, 15);
                Require(r.Hit && !r.Critical, "A ten-point margin does not grant a critical."); });
            cases.Add("roll_attack_expanded_critical_requires_hit", () => {
                var miss = PlaytestRolls.AttackRoll(19, 0, 25, 19);
                var hit = PlaytestRolls.AttackRoll(19, 0, 18, 19);
                var below = PlaytestRolls.AttackRoll(18, 0, 18, 19);
                Require(!miss.Hit && !miss.Critical && hit.Hit && hit.Critical && below.Hit && !below.Critical,
                    "Expanded range requires both a hit and its threshold."); });
            cases.Add("roll_save_naturals_do_not_override_total", () => {
                Require(!PlaytestRolls.SavingThrow(20, 0, 25).Success && PlaytestRolls.SavingThrow(1, 20, 15).Success,
                    "Ordinary saves have no natural-result override."); });
            cases.Add("roll_save_margin_and_tie", () => {
                var fail = PlaytestRolls.SavingThrow(1, 4, 10);
                var tie = PlaytestRolls.SavingThrow(10, 2, 12);
                var above = PlaytestRolls.SavingThrow(10, 5, 12);
                Require(!fail.Success && fail.Total == 5 && fail.FailureMargin == 5
                    && tie.Success && tie.FailureMargin == 0 && above.Success && above.FailureMargin == 0,
                    "Failure margin uses the final total and floors at zero."); });
            cases.Add("roll_task_exact_degree_boundaries", () => {
                Require(PlaytestRolls.TaskCheck(10, 10, 10).Degree == TaskDegree.CriticalSuccess, "DC+10 boundary.");
                Require(PlaytestRolls.TaskCheck(10, 9, 10).Degree == TaskDegree.Success, "DC+9 boundary.");
                Require(PlaytestRolls.TaskCheck(10, 0, 10).Degree == TaskDegree.Success, "DC boundary.");
                Require(PlaytestRolls.TaskCheck(10, -1, 10).Degree == TaskDegree.Failure, "DC-1 boundary.");
                Require(PlaytestRolls.TaskCheck(10, -9, 10).Degree == TaskDegree.Failure, "DC-9 boundary.");
                Require(PlaytestRolls.TaskCheck(10, -10, 10).Degree == TaskDegree.CriticalFailure, "DC-10 boundary."); });
            cases.Add("roll_task_twenty_can_still_fail", () => {
                var r = PlaytestRolls.TaskCheck(20, -15, 20);
                Require(r.Total == 5 && r.Degree == TaskDegree.Failure && !r.Success, "Natural 20 improves once."); });
            cases.Add("roll_task_one_can_still_succeed", () => {
                var r = PlaytestRolls.TaskCheck(1, 30, 10);
                Require(r.Total == 31 && r.Degree == TaskDegree.Success && r.Success, "Natural 1 worsens once."); });
            cases.Add("roll_task_naturals_cross_success_boundary", () => {
                var up = PlaytestRolls.TaskCheck(20, -11, 10);
                var down = PlaytestRolls.TaskCheck(1, 9, 10);
                Require(up.Degree == TaskDegree.Success && up.Success && down.Degree == TaskDegree.Failure && !down.Success,
                    "Shift must affect collapsed success/failure too."); });
            cases.Add("roll_task_natural_shifts_are_bounded", () => {
                var up = PlaytestRolls.TaskCheck(20, 10, 10);
                var down = PlaytestRolls.TaskCheck(1, -20, 10);
                Require(up.Degree == TaskDegree.CriticalSuccess && up.Success
                    && down.Degree == TaskDegree.CriticalFailure && !down.Success, "Degrees cannot leave their four bounds."); });
            cases.Add("roll_opposed_tie_preserves_state", () => {
                var r = PlaytestRolls.OpposedCheck(20, 0, 10, 10);
                Require(r.ActorTotal == 20 && r.DefenderTotal == 20 && !r.ChangesState, "Tie must preserve state."); });
            cases.Add("roll_opposed_higher_total_wins_without_natural_shifts", () => {
                Require(PlaytestRolls.OpposedCheck(1, 20, 20, 0).ChangesState, "Higher total wins even on natural 1.");
                Require(!PlaytestRolls.OpposedCheck(20, 0, 1, 20).ChangesState, "Lower total loses even on natural 20."); });
            cases.Add("roll_invalid_naturals_rejected_for_every_operand", () => {
                foreach (int value in new[] { int.MinValue, 0, 21, int.MaxValue }) {
                    Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.TaskCheck(value, 0, 10));
                    Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.AttackRoll(value, 0, 10));
                    Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.SavingThrow(value, 0, 10));
                    Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.OpposedCheck(value, 0, 10, 0));
                    Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.OpposedCheck(10, 0, value, 0));
                } });
            cases.Add("roll_negative_dc_or_ac_rejected", () => {
                Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.TaskCheck(10, 0, -1));
                Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.AttackRoll(10, 0, -1));
                Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.SavingThrow(10, 0, -1)); });
            cases.Add("roll_zero_dc_and_ac_supported", () => {
                Require(PlaytestRolls.TaskCheck(10, -10, 0).Success, "Zero task DC.");
                Require(PlaytestRolls.AttackRoll(10, -10, 0).Hit, "Zero AC.");
                Require(PlaytestRolls.SavingThrow(10, -10, 0).Success, "Zero save DC."); });
            cases.Add("roll_critical_threshold_bounds", () => {
                Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.AttackRoll(20, 0, 0, 1));
                Throws<ArgumentOutOfRangeException>(() => PlaytestRolls.AttackRoll(20, 0, 0, 21));
                Require(PlaytestRolls.AttackRoll(2, 0, 2, 2).Critical, "Lowest allowed critical threshold is 2.");
                Require(!PlaytestRolls.AttackRoll(1, 100, 2, 2).Critical, "Natural 1 never crits."); });
            cases.Add("roll_extreme_integer_totals_do_not_wrap", () => {
                var task = PlaytestRolls.TaskCheck(10, int.MaxValue, int.MaxValue);
                var attack = PlaytestRolls.AttackRoll(10, int.MaxValue, int.MaxValue);
                var save = PlaytestRolls.SavingThrow(1, int.MinValue, int.MaxValue);
                var opposed = PlaytestRolls.OpposedCheck(1, int.MaxValue, 20, int.MinValue);
                Require(task.Total == 2147483657L && task.Degree == TaskDegree.CriticalSuccess, "Task overflow.");
                Require(attack.Total == 2147483657L && attack.Hit && !attack.Critical, "Attack overflow.");
                Require(save.Total == -2147483647L && !save.Success && save.FailureMargin == 4294967294L, "Save overflow.");
                Require(opposed.ActorTotal == 2147483648L && opposed.DefenderTotal == -2147483628L && opposed.ChangesState,
                    "Opposed overflow."); });
            cases.Add("shared_rule_resolution_is_authority_for_all_four_roll_types", () => {
                var task = RuleResolution.TaskCheck(1, 9, 10);
                var attack = RuleResolution.AttackRoll(19, 0, 18, 19);
                var save = RuleResolution.SavingThrow(1, 4, 10);
                var opposed = RuleResolution.OpposedCheck(20, 0, 10, 10);
                Require(task.Total == 10 && task.Degree == RuleTaskDegree.Failure && !task.Success
                    && task.Degree == (RuleTaskDegree)PlaytestRolls.TaskCheck(1, 9, 10).Degree
                    && attack.Total == 19 && attack.Hit && attack.Critical
                    && attack.Hit == PlaytestRolls.AttackRoll(19, 0, 18, 19).Hit
                    && save.Total == 5 && !save.Success && save.FailureMargin == 5
                    && save.FailureMargin == PlaytestRolls.SavingThrow(1, 4, 10).FailureMargin
                    && opposed.ActorTotal == 20 && opposed.DefenderTotal == 20 && !opposed.ChangesState
                    && opposed.ChangesState == PlaytestRolls.OpposedCheck(20, 0, 10, 10).ChangesState,
                    "Core resolution and the compatibility surface must produce the same sourced results."); });
            cases.Add("shared_rule_resolution_rejects_invalid_and_zero_bounds", () => {
                Throws<ArgumentOutOfRangeException>(() => RuleResolution.TaskCheck(0, 0, 10));
                Throws<ArgumentOutOfRangeException>(() => RuleResolution.AttackRoll(10, 0, -1));
                Throws<ArgumentOutOfRangeException>(() => RuleResolution.SavingThrow(10, 0, -1));
                Throws<ArgumentOutOfRangeException>(() => RuleResolution.OpposedCheck(1, 0, 21, 0));
                Require(RuleResolution.TaskCheck(10, -10, 0).Success
                    && RuleResolution.AttackRoll(10, -10, 0).Hit
                    && RuleResolution.SavingThrow(10, -10, 0).Success,
                    "Zero fixed thresholds remain legal."); });
        }
    }
}
#endif
