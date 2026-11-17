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

    /// <summary>
    /// Ephemeral actor-scoped join over disjoint numeric origin, skill-training and life records.
    /// The legacy Character/Rules accessors still require a real character; generic checks do not.
    /// It owns no gameplay state; the immutable records in Snapshot remain authoritative. Resolve
    /// it at the point of use rather than caching it across a command that replaces snapshot records.
    /// </summary>
    public readonly struct CharacterStateFacts
    {
        private readonly ActorCharacterRecord character;
        private readonly ActorNumericFacts numeric;
        private readonly ActorLifeRecord life;
        private readonly SkillTrainingRecord training;

        private CharacterStateFacts(ActorNumericFacts numeric,ActorCharacterRecord character, ActorLifeRecord life, SkillTrainingRecord training)
        {
            this.character = character;this.numeric=numeric;
            this.life = life ?? throw new ArgumentNullException(nameof(life));
            if (numeric.ActorId != life.ActorId || training != null && training.ActorId != numeric.ActorId)
                throw new ArgumentException("Character, life, and training facts must belong to the same actor.");
            this.training = training;
        }

        public string ActorId => numeric.ActorId;
        public ActorCharacterRecord Character => RequireCharacter();
        public ActorLifeRecord Life => life ?? throw new InvalidOperationException("Character-state query is uninitialized.");
        public SkillTrainingRecord Training => training;
        public int ProficiencyRank => training?.ProficiencyRank ?? 0;
        public CharacterRuleFacts Rules => CharacterRuleFacts.From(RequireCharacter());
        public ActorNumericFacts Numeric => numeric;

        public AbilityCheckModifier DeriveCheck(CharacterAbility ability)
            => new AbilityCheckModifier(ActorId,(int)ability,numeric.AbilityModifier(ability),ProficiencyRank,numeric.ProficiencyContribution(ProficiencyRank));

        public int InjuryPenalty(CharacterAbility ability, bool toolCheck = false, bool manipulatesObject = false,
            bool initiative = false, bool perception = false)
        {
            numeric.AbilityScore(ability);
            return PlaytestLife.AbilityCheckInjuryPenalty(ActorLifeRules.Read(Life), (int)ability,
                toolCheck, manipulatesObject, initiative, perception);
        }

        public int TotalWithInjury(AbilityCheckModifier check, bool toolCheck = false, bool manipulatesObject = false,
            bool initiative = false, bool perception = false)
        {
            if (check.ActorId != ActorId)
                throw new ArgumentException("Ability check belongs to a different actor.", nameof(check));
            return checked(check.Total + InjuryPenalty((CharacterAbility)check.AbilityIndex,
                toolCheck, manipulatesObject, initiative, perception));
        }

        public int TotalWithInjury(CharacterAbility ability, bool toolCheck = false, bool manipulatesObject = false,
            bool initiative = false, bool perception = false)
            => TotalWithInjury(DeriveCheck(ability), toolCheck, manipulatesObject, initiative, perception);

        public static CharacterStateFacts ForActor(Snapshot snapshot, string actorId, string skillId = null)
        {
            if (snapshot == null) throw new ArgumentNullException(nameof(snapshot));
            if (!Validation.ValidId(actorId)) throw new ArgumentException("Actor identity is required.", nameof(actorId));
            if (snapshot.Lives == null) throw new InvalidOperationException("Actor life state is unavailable.");
            var numeric=ActorNumericFacts.ForActor(snapshot,actorId);
            var character = snapshot.Characters.SingleOrDefault(x=>x.ActorId==actorId);
            var lives = snapshot.Lives.Where(x => x != null && x.ActorId == actorId).Take(2).ToArray();
            if (lives.Length != 1) throw new InvalidOperationException("Actor life state must resolve exactly once.");
            var skill = skillId == null ? null : CharacterSkillTrainingFacts.Find(snapshot, actorId, skillId);
            return new CharacterStateFacts(numeric,character, lives[0], skill);
        }

        private ActorCharacterRecord RequireCharacter()
            => character ?? throw new InvalidOperationException("A real character origin is required for character-only facts.");
    }
}
#endif
