#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Pure ability plus recorded training derivation for one task check.</summary>
    public readonly struct AbilityCheckModifier
    {
        public string ActorId { get; }
        public int AbilityIndex { get; }
        public int AbilityModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int Total => checked(AbilityModifier + ProficiencyBonus);

        internal AbilityCheckModifier(string actorId, int abilityIndex, int abilityModifier, int proficiencyRank, int proficiencyBonus)
        {
            ActorId = actorId;
            AbilityIndex = abilityIndex;
            AbilityModifier = abilityModifier;
            ProficiencyRank = proficiencyRank;
            ProficiencyBonus = proficiencyBonus;
        }

        /// <summary>Applies the strongest existing applicable linked injury once at check resolution.</summary>
        public int TotalWithInjury(LifeState life, bool toolCheck = false, bool manipulatesObject = false,
            bool initiative = false, bool perception = false)
        {
            if (life == null) throw new ArgumentNullException(nameof(life));
            return checked(Total + PlaytestLife.AbilityCheckInjuryPenalty(life, AbilityIndex, toolCheck,
                manipulatesObject, initiative, perception));
        }

        public int TotalWithInjury(CharacterStateFacts character, bool toolCheck = false, bool manipulatesObject = false,
            bool initiative = false, bool perception = false)
        {
            if (character.ActorId != ActorId)
                throw new ArgumentException("Ability check belongs to a different actor.", nameof(character));
            return character.TotalWithInjury(this, toolCheck, manipulatesObject, initiative, perception);
        }
    }

    /// <summary>
    /// Shared, stateless modifier derivation. Callers still own the chosen ability, DC, dice,
    /// advantage sources, and task-specific outcomes. Skill-to-ability mappings and training grants
    /// are not inferred here; the supplied SkillTrainingRecord is authoritative when present.
    /// </summary>
    public static class AbilityCheckRules
    {
        public static AbilityCheckModifier Derive(Snapshot snapshot, string actorId, string skillId,
            CharacterAbility ability)
        {
            if (snapshot == null) throw new ArgumentNullException(nameof(snapshot));
            return CharacterStateFacts.ForActor(snapshot, actorId, skillId).DeriveCheck(ability);
        }

        public static AbilityCheckModifier Derive(ActorCharacterRecord character, SkillTrainingRecord training,
            int abilityIndex)
        {
            if (character == null) throw new ArgumentNullException(nameof(character));
            if (training != null && training.ActorId != character.ActorId)
                throw new ArgumentException("Training belongs to a different actor.", nameof(training));
            if (abilityIndex < 0 || abilityIndex >= character.Abilities.Count)
                throw new ArgumentOutOfRangeException(nameof(abilityIndex));
            var facts = CharacterRuleFacts.From(character);
            return Derive(facts, (CharacterAbility)abilityIndex, training?.ProficiencyRank ?? 0);
        }

        public static AbilityCheckModifier Derive(ActorCharacterRecord character, SkillTrainingRecord training,
            CharacterAbility ability)
            => Derive(character, training, (int)ability);

        /// <summary>Derives from an explicit rank, for fixture-backed checks not represented as skills.</summary>
        public static AbilityCheckModifier Derive(ActorCharacterRecord character, int abilityIndex, int proficiencyRank)
        {
            if (character == null) throw new ArgumentNullException(nameof(character));
            if (abilityIndex < 0 || abilityIndex >= character.Abilities.Count)
                throw new ArgumentOutOfRangeException(nameof(abilityIndex));
            return Derive(CharacterRuleFacts.From(character), (CharacterAbility)abilityIndex, proficiencyRank);
        }

        public static AbilityCheckModifier Derive(ActorCharacterRecord character, CharacterAbility ability, int proficiencyRank)
            => Derive(character, (int)ability, proficiencyRank);

        private static AbilityCheckModifier Derive(CharacterRuleFacts facts, CharacterAbility ability, int proficiencyRank)
        {
            int index = (int)ability;
            int proficiency = facts.ProficiencyContribution(proficiencyRank);
            return new AbilityCheckModifier(facts.ActorId, index, facts.AbilityModifier(ability), proficiencyRank, proficiency);
        }

        /// <summary>Rank 0 is untrained, rank 1 adds one proficiency bonus, rank 2 adds two.</summary>
        public static int ProficiencyContribution(int totalLevel, int proficiencyRank)
        {
            if (proficiencyRank < 0 || proficiencyRank > 2)
                throw new ArgumentOutOfRangeException(nameof(proficiencyRank));
            return checked(PlaytestCharacters.ProficiencyBonus(totalLevel) * proficiencyRank);
        }
    }
}
#endif
