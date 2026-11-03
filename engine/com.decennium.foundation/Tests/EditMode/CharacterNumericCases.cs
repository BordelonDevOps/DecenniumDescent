#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        // Literal source examples and independently calculated boundaries; no Python execution.
        // Source pointers and exact class projection: 2026-11-03-characters/SOURCE_BINDINGS.json.
        private static void AddCharacterCases(Dictionary<string, Action> cases)
        {
            cases.Add("character_ability_source_examples_and_negative_odds", () => {
                int[] scores = { 3, 8, 9, 10, 13, 16 };
                int[] expected = { -4, -1, -1, 0, 1, 3 };
                Require(scores.Select(PlaytestCharacters.AbilityModifier).SequenceEqual(expected), "Floor toward negative infinity."); });
            cases.Add("character_ability_extremes_widen_before_subtraction", () => {
                Require(PlaytestCharacters.AbilityModifier(int.MinValue) == -1073741829
                    && PlaytestCharacters.AbilityModifier(int.MinValue + 1) == -1073741829
                    && PlaytestCharacters.AbilityModifier(int.MinValue + 2) == -1073741828
                    && PlaytestCharacters.AbilityModifier(int.MaxValue) == 1073741818, "Ability subtraction/rounding overflow."); });
            cases.Add("character_proficiency_all_twenty_total_levels", () => {
                int[] expected = { 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5, 6,6,6,6 };
                Require(Enumerable.Range(1,20).Select(PlaytestCharacters.ProficiencyBonus).SequenceEqual(expected), "PB band mismatch."); });
            cases.Add("character_proficiency_rejects_outside_campaign_levels", () => {
                foreach (int value in new[] { int.MinValue, 0, 21, int.MaxValue })
                    Throws<ArgumentOutOfRangeException>(() => PlaytestCharacters.ProficiencyBonus(value)); });
            cases.Add("character_all_seventeen_class_hit_dice_and_fixed_bases", () => {
                string[] names = { "Bard", "Cleric", "Crimson Agent", "Dragoon", "Druid", "Mage", "Mirrorsage", "Monk",
                    "Oracle", "Paladin", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior", "Wizard" };
                int[] dice = { 8,8,8,10,8,6,8,8,6,10,8,8,10,8,8,12,6 };
                int[] fixedBases = { 5,5,5,6,5,4,5,5,4,6,5,5,6,5,5,7,4 };
                Require(names.Select(PlaytestCharacters.HitDieForClass).SequenceEqual(dice), "Exact source HD exceptions.");
                Require(names.Select(PlaytestCharacters.FixedHpBaseForClass).SequenceEqual(fixedBases), "Fixed rounded-up averages."); });
            cases.Add("character_unknown_and_legacy_classes_rejected", () => {
                foreach (string name in new[] { "", "bard", "Bard ", "Fighter", "Swashbuckler", "TEST_ONLY.unknown" }) {
                    Throws<ArgumentException>(() => PlaytestCharacters.HitDieForClass(name));
                    Throws<ArgumentException>(() => PlaytestCharacters.FixedHpBaseForClass(name));
                    Throws<ArgumentException>(() => new CharacterLevelRecord(name, 1));
                }
                Throws<ArgumentNullException>(() => PlaytestCharacters.HitDieForClass(null));
                Throws<ArgumentNullException>(() => PlaytestCharacters.FixedHpBaseForClass(null));
                Throws<ArgumentNullException>(() => new CharacterLevelRecord(null, 1)); });
            cases.Add("character_bard_first_level_source_example", () => {
                var r = PlaytestCharacters.BaseMaximumHp(new[] { new CharacterLevelRecord("Bard",8) },14);
                Require(r.BaseMaximum == 10 && r.Contributions.SequenceEqual(new long[] { 10 })
                    && r.TotalLevel == 1 && r.ProficiencyBonus == 2 && r.HitDiceBySize.Count == 1
                    && r.HitDiceBySize[8] == 1, "Bard level 1 source example."); });
            cases.Add("character_bard_advancement_capacity_does_not_heal", () => {
                var r = PlaytestCharacters.BaseMaximumHp(new[] {
                    new CharacterLevelRecord("Bard",8), new CharacterLevelRecord("Bard",5) },14);
                Require(r.BaseMaximum == 17 && r.Contributions.SequenceEqual(new long[] { 10,7 })
                    && r.HitDiceBySize[8] == 2 && PlaytestCharacters.ClampAfterCapacityChange(6,r.BaseMaximum) == 6,
                    "Advancement raises maximum 10 to 17; current remains 6."); });
            cases.Add("character_new_class_first_level_uses_recorded_later_base", () => {
                var r = PlaytestCharacters.BaseMaximumHp(new[] {
                    new CharacterLevelRecord("Bard",8), new CharacterLevelRecord("Mage",4) },14);
                Require(r.BaseMaximum == 16 && r.Contributions.SequenceEqual(new long[] { 10,6 })
                    && r.HitDiceBySize.Count == 2 && r.HitDiceBySize[8] == 1 && r.HitDiceBySize[6] == 1,
                    "Mage class level 1 does not automatically receive max die."); });
            cases.Add("character_later_maximum_roll_is_still_legal", () => {
                var r = PlaytestCharacters.BaseMaximumHp(new[] {
                    new CharacterLevelRecord("Bard",8), new CharacterLevelRecord("Mage",6) },14);
                Require(r.BaseMaximum == 18, "A recorded max-face roll is legal; do not force the fixed option."); });
            cases.Add("character_first_character_level_requires_maximum_die", () => {
                foreach (string name in new[] { "Mage", "Bard", "Dragoon", "Warrior" }) {
                    int lower = PlaytestCharacters.FixedHpBaseForClass(name);
                    Throws<ArgumentException>(() => PlaytestCharacters.BaseMaximumHp(new[] { new CharacterLevelRecord(name,lower) },14));
                } });
            cases.Add("character_record_rejects_base_outside_each_die", () => {
                foreach (string name in new[] { "Mage", "Bard", "Dragoon", "Warrior" }) {
                    foreach (int value in new[] { int.MinValue, 0, PlaytestCharacters.HitDieForClass(name)+1, int.MaxValue })
                        Throws<ArgumentOutOfRangeException>(() => new CharacterLevelRecord(name,value));
                } });
            cases.Add("character_default_record_cannot_bypass_validation", () => {
                Throws<ArgumentException>(() => PlaytestCharacters.BaseMaximumHp(new CharacterLevelRecord[1],10));
                Throws<ArgumentException>(() => PlaytestCharacters.BaseMaximumHp(new[] { new CharacterLevelRecord("Mage",6), default },10)); });
            cases.Add("character_hp_rejects_null_empty_and_level_twenty_one", () => {
                Throws<ArgumentNullException>(() => PlaytestCharacters.BaseMaximumHp(null,10));
                Throws<ArgumentException>(() => PlaytestCharacters.BaseMaximumHp(Array.Empty<CharacterLevelRecord>(),10));
                Throws<ArgumentException>(() => PlaytestCharacters.BaseMaximumHp(
                    Enumerable.Repeat(new CharacterLevelRecord("Mage",6),21).ToArray(),10)); });
            cases.Add("character_hp_retroactive_constitution_recomputes_floors", () => {
                var levels = new[] { new CharacterLevelRecord("Mage",6), new CharacterLevelRecord("Mage",1) };
                var before = PlaytestCharacters.BaseMaximumHp(levels,6);
                var after = PlaytestCharacters.BaseMaximumHp(levels,8);
                Require(before.BaseMaximum == 5 && before.Contributions.SequenceEqual(new long[] { 4,1 })
                    && after.BaseMaximum == 6 && after.Contributions.SequenceEqual(new long[] { 5,1 }), "Recomputed HP must be 6, not 7."); });
            cases.Add("character_hp_first_and_later_contributions_floor_individually", () => {
                var r = PlaytestCharacters.BaseMaximumHp(new[] {
                    new CharacterLevelRecord("Mage",6), new CharacterLevelRecord("Warrior",1) },-10);
                Require(r.BaseMaximum == 2 && r.Contributions.SequenceEqual(new long[] { 1,1 }), "Both attained levels retain minimum 1."); });
            cases.Add("character_hp_total_level_proficiency_ignores_class_split", () => {
                var levels = Enumerable.Repeat(new CharacterLevelRecord("Bard",5),10).ToArray();
                levels[0] = new CharacterLevelRecord("Bard",8);
                for (int i=5; i<10; i++) levels[i] = new CharacterLevelRecord("Mage",4);
                var r = PlaytestCharacters.BaseMaximumHp(levels,10);
                Require(r.TotalLevel == 10 && r.ProficiencyBonus == 4 && r.BaseMaximum == 48
                    && r.HitDiceBySize[8] == 5 && r.HitDiceBySize[6] == 5, "Bard5/Mage5 uses total10 PB+4."); });
            cases.Add("character_hp_history_preserves_interleaved_class_order", () => {
                var levels = new[] { new CharacterLevelRecord("Bard",8), new CharacterLevelRecord("Mage",4),
                    new CharacterLevelRecord("Bard",5), new CharacterLevelRecord("Mage",1) };
                var r = PlaytestCharacters.BaseMaximumHp(levels,14);
                Require(r.BaseMaximum == 26 && r.Contributions.SequenceEqual(new long[] { 10,6,7,3 })
                    && r.Levels.Select(x=>x.ClassName).SequenceEqual(new[] { "Bard","Mage","Bard","Mage" }), "Chronology reordered.");
                Array.Reverse(levels);
                Throws<ArgumentException>(() => PlaytestCharacters.BaseMaximumHp(levels,14)); });
            cases.Add("character_hp_twenty_levels_and_integer_extremes", () => {
                var levels = Enumerable.Repeat(new CharacterLevelRecord("Warrior",12),20).ToArray();
                var high = PlaytestCharacters.BaseMaximumHp(levels,int.MaxValue);
                var low = PlaytestCharacters.BaseMaximumHp(levels,int.MinValue);
                Require(high.BaseMaximum == 21474836600L && high.Contributions.All(x=>x==1073741830L)
                    && low.BaseMaximum == 20 && low.Contributions.All(x=>x==1)
                    && high.TotalLevel == 20 && high.ProficiencyBonus == 6 && high.HitDiceBySize[12] == 20, "HP overflow or level cap."); });
            cases.Add("character_hp_results_detach_from_caller_history", () => {
                var levels = new List<CharacterLevelRecord> { new CharacterLevelRecord("Bard",8), new CharacterLevelRecord("Mage",4) };
                var r = PlaytestCharacters.BaseMaximumHp(levels,14);
                levels[0] = new CharacterLevelRecord("Warrior",12);
                levels.Clear();
                Require(r.BaseMaximum == 16 && r.TotalLevel == 2 && r.Levels[0].ClassName == "Bard"
                    && r.Levels[1].BaseHp == 4 && r.HitDiceBySize[8] == 1, "Caller edits changed prior result."); });
            cases.Add("character_hp_result_collections_reject_mutation", () => {
                var r = PlaytestCharacters.BaseMaximumHp(new[] { new CharacterLevelRecord("Bard",8) },14);
                Throws<NotSupportedException>(() => ((IList<CharacterLevelRecord>)r.Levels)[0] = new CharacterLevelRecord("Mage",6));
                Throws<NotSupportedException>(() => ((IList<long>)r.Contributions)[0] = 999);
                Throws<NotSupportedException>(() => ((IDictionary<int,int>)r.HitDiceBySize)[8] = 999);
                Require(r.BaseMaximum == 10 && r.Levels[0].ClassName == "Bard" && r.Contributions[0] == 10
                    && r.HitDiceBySize[8] == 1, "Result collections mutated."); });
            cases.Add("character_hp_recalculation_does_not_mutate_records_or_prior_results", () => {
                var levels = new[] { new CharacterLevelRecord("Mage",6), new CharacterLevelRecord("Mage",1) };
                var a = PlaytestCharacters.BaseMaximumHp(levels,6);
                var b = PlaytestCharacters.BaseMaximumHp(levels,8);
                var c = PlaytestCharacters.BaseMaximumHp(levels,6);
                Require(a.BaseMaximum == 5 && b.BaseMaximum == 6 && c.BaseMaximum == 5
                    && a.Contributions.SequenceEqual(c.Contributions) && levels[0].BaseHp == 6 && levels[1].BaseHp == 1,
                    "Recalculation must use stored bases, never feed back the modified maximum."); });
            cases.Add("character_capacity_only_clamps_downward", () => {
                Require(PlaytestCharacters.ClampAfterCapacityChange(6,17) == 6
                    && PlaytestCharacters.ClampAfterCapacityChange(19,17) == 17
                    && PlaytestCharacters.ClampAfterCapacityChange(17,17) == 17, "Capacity is not healing or recovery."); });
            cases.Add("character_capacity_zero_stays_zero_and_zero_maximum_clamps", () => {
                Require(PlaytestCharacters.ClampAfterCapacityChange(0,17) == 0
                    && PlaytestCharacters.ClampAfterCapacityChange(0,0) == 0
                    && PlaytestCharacters.ClampAfterCapacityChange(6,0) == 0, "No revival from a capacity increase."); });
            cases.Add("character_capacity_negative_inputs_rejected", () => {
                foreach (long value in new[] { -1L,long.MinValue }) {
                    Throws<ArgumentOutOfRangeException>(() => PlaytestCharacters.ClampAfterCapacityChange(value,17));
                    Throws<ArgumentOutOfRangeException>(() => PlaytestCharacters.ClampAfterCapacityChange(0,value));
                } });
            cases.Add("character_capacity_long_limits_preserve_value", () => {
                Require(PlaytestCharacters.ClampAfterCapacityChange(long.MaxValue,long.MaxValue) == long.MaxValue
                    && PlaytestCharacters.ClampAfterCapacityChange(21474836600L,long.MaxValue) == 21474836600L
                    && PlaytestCharacters.ClampAfterCapacityChange(long.MaxValue,21474836600L) == 21474836600L,
                    "Capacity clamp must support widened HP without overflow."); });
        }
    }
}
#endif
