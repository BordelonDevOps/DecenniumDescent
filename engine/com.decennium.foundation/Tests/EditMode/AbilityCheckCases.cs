#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ActorCharacterRecord CheckCharacter(string actor = "worker", int levels = 5)
            => new ActorCharacterRecord(actor, "check-profile", new[] { 12, 8, 10, 15, 14, 9 },
                Enumerable.Range(0, levels).Select(_ => new CharacterLevelFact("Bard", 8)));

        private static void AddAbilityCheckCases(Dictionary<string, Action> cases)
        {
            cases.Add("ability_check_rank_and_level_matrix", () => {
                foreach (int level in new[] { 1, 4, 5, 8, 9, 12, 13, 16, 17, 20 })
                    foreach (int rank in new[] { 0, 1, 2 })
                        Require(AbilityCheckRules.ProficiencyContribution(level, rank)
                            == PlaytestCharacters.ProficiencyBonus(level) * rank, "Rank contribution changed at a proficiency tier."); });
            cases.Add("ability_check_derives_selected_ability_and_training_once", () => {
                var character = CheckCharacter();
                var trained = new SkillTrainingRecord("worker", "medicine", 1);
                var expert = new SkillTrainingRecord("worker", "mining-tools", 2);
                var untrainedCheck = AbilityCheckRules.Derive(character, (SkillTrainingRecord)null, 1);
                var trainedCheck = AbilityCheckRules.Derive(character, trained, 4);
                var expertCheck = AbilityCheckRules.Derive(character, expert, 3);
                Require(untrainedCheck.AbilityIndex == 1 && untrainedCheck.AbilityModifier == -1
                    && untrainedCheck.ProficiencyRank == 0 && untrainedCheck.ProficiencyBonus == 0 && untrainedCheck.Total == -1,
                    "Untrained DEX check did not preserve the negative score modifier.");
                Require(trainedCheck.AbilityIndex == 4 && trainedCheck.AbilityModifier == 2
                    && trainedCheck.ProficiencyRank == 1 && trainedCheck.ProficiencyBonus == 3 && trainedCheck.Total == 5,
                    "WIS check did not add exactly one recorded proficiency contribution.");
                Require(expertCheck.AbilityIndex == 3 && expertCheck.AbilityModifier == 2
                    && expertCheck.ProficiencyRank == 2 && expertCheck.ProficiencyBonus == 6 && expertCheck.Total == 8,
                    "Rank-two check did not add the recorded double contribution."); });
            cases.Add("ability_check_injury_is_applied_once_at_resolution", () => {
                var check = AbilityCheckRules.Derive(CheckCharacter(), new SkillTrainingRecord("worker", "craft", 1), 1);
                var life = new LifeState(20, 20, wounds: new[] { Injury.FineMotorTrauma, Injury.FineMotorTrauma, Injury.FineMotorTrauma });
                Require(check.Total == 2 && check.TotalWithInjury(life, toolCheck: true, manipulatesObject: true) == 1,
                    "Applicable Fine Motor injury must apply one penalty, even with multiple matching wounds/flags.");
                var unaffected = AbilityCheckRules.Derive(CheckCharacter(), null, 4);
                Require(unaffected.TotalWithInjury(life) == unaffected.Total,
                    "Fine Motor injury penalized a non-tool Wisdom ability check."); });
            cases.Add("ability_check_rejects_mismatched_training_and_invalid_inputs", () => {
                var character = CheckCharacter();
                Throws<ArgumentException>(() => AbilityCheckRules.Derive(character,
                    new SkillTrainingRecord("another-worker", "medicine", 1), 4));
                foreach (int index in new[] { -1, 6 })
                    Throws<ArgumentOutOfRangeException>(() => AbilityCheckRules.Derive(character, null, index));
                foreach (int rank in new[] { -1, 3 })
                    Throws<ArgumentOutOfRangeException>(() => AbilityCheckRules.Derive(character, 4, rank));
                foreach (int level in new[] { 0, 21 })
                    Throws<ArgumentOutOfRangeException>(() => AbilityCheckRules.ProficiencyContribution(level, 1));
                Throws<ArgumentNullException>(() => AbilityCheckRules.Derive(null, null, 0));
                Throws<ArgumentNullException>(() => AbilityCheckRules.Derive(character, null, 0).TotalWithInjury(null)); });
        }
    }
}
#endif
