#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>
    /// Read-only projection over persisted character facts. It stores no state of its own:
    /// ability scores and ordered attained levels remain authoritative in ActorCharacterRecord.
    /// Current life, injury, posture and inventory facts remain in their existing ledgers.
    /// </summary>
    public readonly struct CharacterRuleFacts
    {
        private readonly ActorCharacterRecord character;

        private CharacterRuleFacts(ActorCharacterRecord character)
        {
            this.character = character ?? throw new ArgumentNullException(nameof(character));
        }

        public string ActorId => RequireCharacter().ActorId;
        public string ProfileId => RequireCharacter().ProfileId;
        public ActorCharacterRecord Source => RequireCharacter();
        public int TotalLevel => RequireCharacter().Levels.Count;
        public int ProficiencyBonus => PlaytestCharacters.ProficiencyBonus(TotalLevel);

        public int AbilityScore(CharacterAbility ability)
        {
            int index = AbilityIndex(ability);
            return RequireCharacter().Abilities[index];
        }

        public int AbilityModifier(CharacterAbility ability)
            => PlaytestCharacters.AbilityModifier(AbilityScore(ability));

        public int ProficiencyContribution(int proficiencyRank)
            => AbilityCheckRules.ProficiencyContribution(TotalLevel, proficiencyRank);

        public static CharacterRuleFacts From(ActorCharacterRecord character)
            => new CharacterRuleFacts(character);

        public static CharacterRuleFacts ForActor(Snapshot snapshot, string actorId)
        {
            if (snapshot == null) throw new ArgumentNullException(nameof(snapshot));
            if (string.IsNullOrEmpty(actorId)) throw new ArgumentException("Actor identity is required.", nameof(actorId));
            if (snapshot.Characters == null) throw new InvalidOperationException("Character state is unavailable.");
            var matches = snapshot.Characters.Where(x => x != null && x.ActorId == actorId).Take(2).ToArray();
            if (matches.Length != 1) throw new InvalidOperationException("Character identity must resolve exactly once.");
            return new CharacterRuleFacts(matches[0]);
        }

        private ActorCharacterRecord RequireCharacter()
            => character ?? throw new InvalidOperationException("Character facts query is uninitialized.");

        private static int AbilityIndex(CharacterAbility ability)
        {
            int index = (int)ability;
            if (index < (int)CharacterAbility.Strength || index > (int)CharacterAbility.Charisma)
                throw new ArgumentOutOfRangeException(nameof(ability));
            return index;
        }
    }
}
#endif
