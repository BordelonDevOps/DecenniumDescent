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
            cases.Add("character_rule_facts_are_ephemeral_queries_over_the_authoritative_record", () => {
                var character = CheckCharacter();
                var facts = CharacterRuleFacts.From(character);
                var trained = new SkillTrainingRecord(character.ActorId, "survival", 1);
                var check = AbilityCheckRules.Derive(character, trained, CharacterAbility.Wisdom);
                Require(ReferenceEquals(facts.Source, character) && facts.ActorId == character.ActorId
                    && facts.ProfileId == character.ProfileId && facts.TotalLevel == 5 && facts.ProficiencyBonus == 3
                    && facts.AbilityScore(CharacterAbility.Strength) == 12
                    && facts.AbilityModifier(CharacterAbility.Dexterity) == -1
                    && facts.AbilityModifier(CharacterAbility.Intelligence) == 2
                    && check.AbilityIndex == (int)CharacterAbility.Wisdom && check.Total == 5,
                    "Derived facts or the check did not use the one persisted character record.");
                var snapshot = World(ConnectedPolicy()).Capture();
                var actorFacts = CharacterRuleFacts.ForActor(snapshot, TestOnlyPolicy.ActorId);
                Require(ReferenceEquals(actorFacts.Source, snapshot.Characters.Single(x => x.ActorId == TestOnlyPolicy.ActorId)),
                    "Actor lookup returned a copied or detached character record.");
                Throws<InvalidOperationException>(() => CharacterRuleFacts.ForActor(snapshot, "missing-character"));
                var duplicate = snapshot.Characters[0];
                snapshot.Characters = snapshot.Characters.Concat(new[] { duplicate }).ToArray();
                Throws<InvalidOperationException>(() => CharacterRuleFacts.ForActor(snapshot, duplicate.ActorId));
                Throws<ArgumentOutOfRangeException>(() => facts.AbilityScore((CharacterAbility)99)); });
            cases.Add("character_skill_training_queries_share_the_persisted_rank_records", () => {
                var snapshot = World(ConnectedPolicy()).Capture();
                string hero = TestOnlyPolicy.ActorId, companion = TestOnlyPolicy.CompanionId;
                snapshot.SkillTraining = new[] {
                    new SkillTrainingRecord(hero, "perception", 2),
                    new SkillTrainingRecord(companion, "perception", 1),
                    new SkillTrainingRecord(hero, "medicine", 0)
                };
                var records = snapshot.SkillTraining;
                var expert = CharacterSkillTrainingFacts.Find(snapshot, hero, "perception");
                var heroCheck = AbilityCheckRules.Derive(snapshot, hero, "perception", CharacterAbility.Wisdom);
                var companionCheck = AbilityCheckRules.Derive(snapshot, companion, "perception", CharacterAbility.Wisdom);
                Require(ReferenceEquals(records, snapshot.SkillTraining) && ReferenceEquals(expert, records[0])
                    && heroCheck.ProficiencyRank == 2 && heroCheck.ProficiencyBonus
                        == CharacterRuleFacts.ForActor(snapshot, hero).ProficiencyContribution(2)
                    && companionCheck.ProficiencyRank == 1
                    && CharacterSkillTrainingFacts.ProficiencyRank(snapshot, hero, "medicine") == 0
                    && !CharacterSkillTrainingFacts.IsTrained(snapshot, hero, "medicine")
                    && CharacterSkillTrainingFacts.Find(snapshot, companion, "medicine") == null,
                    "Skill reads copied, crossed, or changed the persisted actor/training facts.");
                snapshot.SkillTraining = records.Concat(new[] { new SkillTrainingRecord(hero, "perception", 1) }).ToArray();
                Throws<InvalidOperationException>(() => CharacterSkillTrainingFacts.Find(snapshot, hero, "perception"));
                Throws<ArgumentNullException>(() => CharacterSkillTrainingFacts.Find(null, hero, "perception"));
                Throws<ArgumentException>(() => CharacterSkillTrainingFacts.Find(snapshot, hero, "")); });
            cases.Add("character_state_facts_join_existing_actor_records_without_copying", () => {
                var snapshot = World(ConnectedPolicy()).Capture();
                string hero = TestOnlyPolicy.ActorId, companion = TestOnlyPolicy.CompanionId;
                snapshot.SkillTraining = new[] { new SkillTrainingRecord(hero, "tool-work", 1) };
                var originalLife = snapshot.Lives.Single(x => x.ActorId == hero);
                var injuredLife = new ActorLifeRecord(originalLife.ActorId, originalLife.MaximumHp, originalLife.Hp,
                    originalLife.TemporaryHp, new[] { (int)Injury.FineMotorTrauma }, originalLife.Stable, originalLife.Dead,
                    originalLife.UsesDeathSaves, originalLife.DeathSuccesses, originalLife.DeathFailures,
                    originalLife.StableUntil, originalLife.LastDeathTurn, originalLife.Prone, originalLife.HeldItems);
                snapshot.Lives = snapshot.Lives.Select(x => x.ActorId == hero ? injuredLife : x).ToArray();

                var facts = CharacterStateFacts.ForActor(snapshot, hero, "tool-work");
                var check = AbilityCheckRules.Derive(snapshot, hero, "tool-work", CharacterAbility.Intelligence);
                Require(ReferenceEquals(facts.Character, snapshot.Characters.Single(x => x.ActorId == hero))
                    && ReferenceEquals(facts.Life, injuredLife)
                    && ReferenceEquals(facts.Training, snapshot.SkillTraining[0])
                    && facts.ActorId == hero && facts.ProficiencyRank == 1
                    && check.ActorId == hero && check.ProficiencyRank == 1
                    && check.TotalWithInjury(facts, toolCheck: true, manipulatesObject: true) == check.Total - 1,
                    "The actor-scoped facts copied, crossed, or failed to combine the persisted character, training, and injury records.");
                var other = CharacterStateFacts.ForActor(snapshot, companion);
                Throws<ArgumentException>(() => check.TotalWithInjury(other, toolCheck: true, manipulatesObject: true));
                snapshot.Lives = snapshot.Lives.Concat(new[] { injuredLife }).ToArray();
                Throws<InvalidOperationException>(() => CharacterStateFacts.ForActor(snapshot, hero));
            });
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
