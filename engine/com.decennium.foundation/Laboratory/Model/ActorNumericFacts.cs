#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Ephemeral numeric origin projection. No class, PB, equipment or skill grant is
    /// manufactured for a creature. The snapshot and trusted source records remain authoritative.</summary>
    public readonly struct ActorNumericFacts
    {
        private readonly ActorCharacterRecord character;
        private readonly CreatureActorRecord creature;
        private ActorNumericFacts(ActorCharacterRecord character,CreatureActorRecord creature)
        {
            if((character==null)==(creature==null))throw new ArgumentException("Actor requires exactly one numeric origin.");
            this.character=character; this.creature=creature;
        }
        public string ActorId => creature?.ActorId ?? RequireCharacter().ActorId;
        public bool IsCreature => creature!=null;
        public CreatureActorRecord Creature => creature;
        public int? ProficiencyBonus => creature!=null ? (int?)null : CharacterRuleFacts.From(RequireCharacter()).ProficiencyBonus;
        public int AbilityScore(CharacterAbility ability)
        {
            int index=(int)ability;
            if(index<0||index>5)throw new ArgumentOutOfRangeException(nameof(ability));
            return creature!=null ? creature.Abilities[index] : RequireCharacter().Abilities[index];
        }
        public int AbilityModifier(CharacterAbility ability) => PlaytestCharacters.AbilityModifier(AbilityScore(ability));
        public int BaseArmorClass => creature!=null ? creature.ArmorClass : checked((int)PrototypeArmor.UnarmoredBaseAc(AbilityScore(CharacterAbility.Dexterity)));
        public int ProficiencyContribution(int rank)
        {
            if(rank<0||rank>2)throw new ArgumentOutOfRangeException(nameof(rank));
            if(rank==0)return 0;
            if(creature!=null)throw new InvalidOperationException("Creature proficiency is not established by its source.");
            return CharacterRuleFacts.From(RequireCharacter()).ProficiencyContribution(rank);
        }
        private ActorCharacterRecord RequireCharacter() => character ?? throw new InvalidOperationException("Character numeric origin unavailable.");
        public static ActorNumericFacts ForActor(Snapshot state,string actor)
        {
            if(state==null)throw new ArgumentNullException(nameof(state));
            var characters=state.Characters.Where(x=>x!=null&&x.ActorId==actor).Take(2).ToArray();
            var creatures=state.Creatures.Where(x=>x!=null&&x.ActorId==actor).Take(2).ToArray();
            if(characters.Length+creatures.Length!=1)throw new InvalidOperationException("Actor numeric origin must resolve exactly once.");
            return new ActorNumericFacts(characters.SingleOrDefault(),creatures.SingleOrDefault());
        }
    }
}
#endif
