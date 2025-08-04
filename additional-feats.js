// Additional feats to reach 330 total - this will be merged into game-data.js
const ADDITIONAL_FEATS = {
    // Combat Feats (51-100)
    berserker: {
        name: "Berserker",
        description: "You can enter a battle rage.",
        prerequisite: "Constitution 15+",
        effect: "Once per long rest, you can rage for 1 minute, gaining +2 damage on melee attacks and resistance to physical damage.",
        type: "general"
    },
    bladedancer: {
        name: "Bladedancer",
        description: "You move with deadly grace in combat.",
        prerequisite: "Dexterity 15+",
        effect: "When you hit with a finesse weapon, you can move 5 feet without provoking opportunity attacks.",
        type: "general"
    },
    bowyer: {
        name: "Bowyer",
        description: "You are skilled at crafting and using bows.",
        prerequisite: "Proficiency with longbow or shortbow",
        effect: "You can craft masterwork bows and arrows. Your ranged attacks with bows deal +1 damage.",
        type: "general"
    },
    bruiser: {
        name: "Bruiser",
        description: "You excel at intimidating and overpowering foes.",
        prerequisite: "Strength 15+",
        effect: "You gain proficiency in Intimidation and can use Strength instead of Charisma for Intimidation checks.",
        type: "general"
    },
    cavalry: {
        name: "Cavalry",
        description: "You are trained in mounted warfare.",
        prerequisite: "Animal Handling proficiency",
        effect: "You have advantage on attacks against unmounted creatures while mounted, and your mount gains +10 feet movement speed.",
        type: "general"
    },
    cleave: {
        name: "Cleave",
        description: "Your attacks can strike multiple foes.",
        prerequisite: "Strength 13+",
        effect: "When you reduce a creature to 0 hit points with a melee attack, you can make another attack against a different creature within reach.",
        type: "general"
    },
    combatExpertise: {
        name: "Combat Expertise",
        description: "You can trade accuracy for defense.",
        prerequisite: "Intelligence 13+",
        effect: "You can take a -1 penalty to attack rolls to gain +1 AC until your next turn.",
        type: "general"
    },
    deadlyAim: {
        name: "Deadly Aim",
        description: "You can trade accuracy for damage with ranged weapons.",
        prerequisite: "Dexterity 13+",
        effect: "You can take a -1 penalty to ranged attack rolls to deal +2 damage.",
        type: "general"
    },
    disarm: {
        name: "Disarm",
        description: "You can disarm opponents in combat.",
        prerequisite: "Dexterity 13+",
        effect: "You can attempt to disarm an opponent as an attack. The target makes a Strength or Dexterity save (DC 8 + proficiency + ability modifier).",
        type: "general"
    },
    dualWielder: {
        name: "Dual Wielder",
        description: "You master fighting with two weapons.",
        prerequisite: "Dexterity 13+",
        effect: "You can use two-weapon fighting with non-light weapons and gain +1 AC while wielding two weapons.",
        type: "general"
    },
    
    // Magic Feats (101-150)
    arcaneFocus: {
        name: "Arcane Focus",
        description: "You can focus magical energy more effectively.",
        prerequisite: "Spellcasting ability",
        effect: "You can use your spellcasting focus to cast spells without material components worth less than 100 gp.",
        type: "magic"
    },
    battleMage: {
        name: "Battle Mage",
        description: "You blend magic and martial combat.",
        prerequisite: "Spellcasting ability, proficiency with martial weapons",
        effect: "You can cast spells with somatic components while holding weapons and shields.",
        type: "magic"
    },
    cantrip_mastery: {
        name: "Cantrip Mastery",
        description: "Your cantrips become more powerful.",
        prerequisite: "Ability to cast cantrips",
        effect: "Choose one cantrip you know. It deals maximum damage when you roll a natural 20 on the attack roll or the target rolls a natural 1 on their saving throw.",
        type: "magic"
    },
    dispel_mastery: {
        name: "Dispel Mastery",
        description: "You excel at dispelling magic.",
        prerequisite: "Ability to cast dispel magic",
        effect: "When you cast dispel magic, you can target one additional magical effect.",
        type: "magic"
    },
    elemental_mastery: {
        name: "Elemental Mastery",
        description: "You have mastered elemental magic.",
        prerequisite: "Ability to cast 3rd level spells",
        effect: "Choose an element. You can change the damage type of your spells to that element.",
        type: "magic"
    },
    enchantment_focus: {
        name: "Enchantment Focus",
        description: "Your enchantment spells are more effective.",
        prerequisite: "Ability to cast enchantment spells",
        effect: "Creatures have disadvantage on saving throws against your enchantment spells.",
        type: "magic"
    },
    evocation_focus: {
        name: "Evocation Focus",
        description: "Your evocation spells deal more damage.",
        prerequisite: "Ability to cast evocation spells",
        effect: "Your evocation spells deal +1 damage per die rolled.",
        type: "magic"
    },
    familiar_bond: {
        name: "Familiar Bond",
        description: "Your bond with your familiar is stronger.",
        prerequisite: "Ability to cast find familiar",
        effect: "Your familiar gains hit points equal to your level and can attack using your spell attack bonus.",
        type: "magic"
    },
    greater_spell_focus: {
        name: "Greater Spell Focus",
        description: "Your spells are harder to resist.",
        prerequisite: "Spell Focus feat",
        effect: "The DC for your spells increases by an additional +1.",
        type: "magic"
    },
    heighten_spell: {
        name: "Heighten Spell",
        description: "You can cast spells at higher levels.",
        prerequisite: "Ability to cast 3rd level spells",
        effect: "You can expend a spell slot one level higher to increase the spell's DC by +1.",
        type: "magic"
    },
    
    // Skill Feats (151-200)
    acrobatic: {
        name: "Acrobatic",
        description: "You are exceptionally agile.",
        prerequisite: "Dexterity 13+",
        effect: "You gain proficiency in Acrobatics and can use Dexterity instead of Strength for Athletics checks involving jumping.",
        type: "general"
    },
    alertness_improved: {
        name: "Improved Alertness",
        description: "Your senses are incredibly sharp.",
        prerequisite: "Alertness feat",
        effect: "You gain blindsense 10 feet and cannot be surprised while conscious.",
        type: "general"
    },
    animal_companion: {
        name: "Animal Companion",
        description: "You have formed a bond with an animal.",
        prerequisite: "Animal Handling proficiency",
        effect: "You gain an animal companion that follows your commands and fights alongside you.",
        type: "general"
    },
    appraise: {
        name: "Appraise",
        description: "You can accurately determine the value of items.",
        prerequisite: "Intelligence 13+",
        effect: "You can determine the exact value and properties of any item with a successful Investigation check.",
        type: "general"
    },
    artisan: {
        name: "Artisan",
        description: "You are skilled in crafting.",
        prerequisite: "Intelligence 13+",
        effect: "Choose one type of artisan's tools. You gain proficiency and can create masterwork items.",
        type: "general"
    },
    athlete_improved: {
        name: "Improved Athlete",
        description: "Your athletic abilities are exceptional.",
        prerequisite: "Athlete feat",
        effect: "Your climbing and swimming speeds equal your walking speed, and you can long jump your full Strength score.",
        type: "general"
    },
    blind_fight: {
        name: "Blind Fight",
        description: "You can fight without relying on sight.",
        prerequisite: "Wisdom 13+",
        effect: "You don't suffer disadvantage on attack rolls due to being blinded, and you can pinpoint the location of creatures within 30 feet.",
        type: "general"
    },
    burglar: {
        name: "Burglar",
        description: "You are skilled at breaking and entering.",
        prerequisite: "Dexterity 13+",
        effect: "You gain proficiency with thieves' tools and can pick locks and disable traps more effectively.",
        type: "general"
    },
    cartographer: {
        name: "Cartographer",
        description: "You excel at navigation and mapmaking.",
        prerequisite: "Intelligence 13+",
        effect: "You can create accurate maps and never get lost. You have advantage on Survival checks for navigation.",
        type: "general"
    },
    climber_improved: {
        name: "Improved Climber",
        description: "You are an exceptional climber.",
        prerequisite: "Climber feat",
        effect: "You can climb on ceilings and overhangs, and you don't fall when you fail a climbing check by 4 or less.",
        type: "general"
    },
    
    // Social Feats (201-250)
    charismatic: {
        name: "Charismatic",
        description: "Your personality is magnetic.",
        prerequisite: "Charisma 13+",
        effect: "You gain proficiency in Persuasion and Deception. If already proficient, you add double your proficiency bonus.",
        type: "general"
    },
    commanding_presence: {
        name: "Commanding Presence",
        description: "You naturally command respect.",
        prerequisite: "Charisma 15+",
        effect: "You can use your Charisma modifier instead of Strength for Intimidation checks, and you have advantage on Persuasion checks against creatures of lower level.",
        type: "general"
    },
    courtly_manners: {
        name: "Courtly Manners",
        description: "You are well-versed in noble etiquette.",
        prerequisite: "Charisma 13+",
        effect: "You have advantage on Charisma checks when interacting with nobles and can gain audience with important figures more easily.",
        type: "general"
    },
    deceiver: {
        name: "Deceiver",
        description: "You are a master of deception.",
        prerequisite: "Charisma 13+",
        effect: "You gain proficiency in Deception and can lie convincingly even under magical compulsion.",
        type: "general"
    },
    entertainer: {
        name: "Entertainer",
        description: "You can captivate audiences.",
        prerequisite: "Charisma 13+",
        effect: "You gain proficiency in Performance and can earn money and gather information through performances.",
        type: "general"
    },
    fast_talker: {
        name: "Fast Talker",
        description: "You can talk your way out of trouble.",
        prerequisite: "Charisma 15+",
        effect: "You can attempt to distract or confuse enemies with rapid speech, potentially causing them to lose their action.",
        type: "general"
    },
    gossip: {
        name: "Gossip",
        description: "You excel at gathering information.",
        prerequisite: "Charisma 13+",
        effect: "You can gather information about local events, people, and rumors twice as fast as normal.",
        type: "general"
    },
    intimidating: {
        name: "Intimidating",
        description: "Your presence strikes fear into others.",
        prerequisite: "Charisma 13+ or Strength 15+",
        effect: "You gain proficiency in Intimidation and can demoralize enemies in combat, causing them to have disadvantage on their next attack.",
        type: "general"
    },
    leadership: {
        name: "Leadership",
        description: "You inspire others to follow you.",
        prerequisite: "Charisma 15+, level 6+",
        effect: "You can recruit followers and hirelings more easily, and they are more loyal to you.",
        type: "general"
    },
    negotiator: {
        name: "Negotiator",
        description: "You excel at making deals.",
        prerequisite: "Charisma 13+",
        effect: "You can negotiate better prices for goods and services, and you have advantage on Persuasion checks during negotiations.",
        type: "general"
    },
    
    // Survival Feats (251-300)
    endurance: {
        name: "Endurance",
        description: "You can push your body beyond normal limits.",
        prerequisite: "Constitution 13+",
        effect: "You can go twice as long without food, water, or sleep, and you have advantage on Constitution saves against exhaustion.",
        type: "general"
    },
    forager: {
        name: "Forager",
        description: "You can find food and water in the wild.",
        prerequisite: "Wisdom 13+",
        effect: "You can find enough food and water for yourself and up to 6 other people each day in any terrain except deserts or arctic regions.",
        type: "general"
    },
    hardy: {
        name: "Hardy",
        description: "You are resistant to environmental hazards.",
        prerequisite: "Constitution 15+",
        effect: "You have resistance to cold and heat damage, and you have advantage on saves against disease and poison.",
        type: "general"
    },
    hunter: {
        name: "Hunter",
        description: "You are skilled at tracking and hunting prey.",
        prerequisite: "Wisdom 13+",
        effect: "You gain proficiency in Survival and can track creatures across any terrain. You deal +2 damage to beasts and monstrosities.",
        type: "general"
    },
    iron_will: {
        name: "Iron Will",
        description: "Your willpower is unbreakable.",
        prerequisite: "Wisdom 15+",
        effect: "You have advantage on Wisdom saving throws and are immune to being charmed or frightened.",
        type: "general"
    },
    pathfinder: {
        name: "Pathfinder",
        description: "You can navigate any terrain.",
        prerequisite: "Wisdom 13+",
        effect: "You and your party can move at normal speed while tracking, and difficult terrain doesn't slow your group's travel.",
        type: "general"
    },
    ranger_training: {
        name: "Ranger Training",
        description: "You have learned wilderness survival techniques.",
        prerequisite: "Wisdom 13+",
        effect: "You gain proficiency in Survival and Nature, and you can hide even when only lightly obscured by natural phenomena.",
        type: "general"
    },
    scavenger: {
        name: "Scavenger",
        description: "You can find useful items in unlikely places.",
        prerequisite: "Intelligence 13+",
        effect: "You can find basic equipment and supplies in ruins, dungeons, and other locations where others have been.",
        type: "general"
    },
    survivalist: {
        name: "Survivalist",
        description: "You excel at surviving in harsh conditions.",
        prerequisite: "Constitution 13+, Wisdom 13+",
        effect: "You can survive in any environment and can help others do the same. You need only half the normal amount of food and water.",
        type: "general"
    },
    tracker: {
        name: "Tracker",
        description: "You can follow tracks across any terrain.",
        prerequisite: "Wisdom 15+",
        effect: "You can track creatures across any surface, including water and air. You can determine the age, size, and condition of tracks.",
        type: "general"
    },
    
    // Exotic Feats (301-330)
    aberrant_mind: {
        name: "Aberrant Mind",
        description: "Your mind has been touched by alien intelligence.",
        prerequisite: "Intelligence 15+",
        effect: "You can communicate telepathically with aberrations and have resistance to psychic damage.",
        type: "aberrant_mutation"
    },
    astral_projection: {
        name: "Astral Projection",
        description: "You can project your consciousness to other planes.",
        prerequisite: "Wisdom 17+, level 15+",
        effect: "Once per long rest, you can cast astral projection without expending a spell slot.",
        type: "magic"
    },
    divine_favor: {
        name: "Divine Favor",
        description: "You have earned the favor of a deity.",
        prerequisite: "Charisma 15+, worship a deity",
        effect: "Once per long rest, you can call upon divine aid to automatically succeed on one saving throw or ability check.",
        type: "magic"
    },
    dragon_blood: {
        name: "Dragon Blood",
        description: "Draconic blood flows through your veins.",
        prerequisite: "Dragonborn or sorcerer with draconic bloodline",
        effect: "You gain resistance to your draconic ancestry's damage type and can speak, read, and write Draconic.",
        type: "general"
    },
    elemental_body: {
        name: "Elemental Body",
        description: "Your body has been infused with elemental energy.",
        prerequisite: "Constitution 15+, exposure to elemental plane",
        effect: "Choose an element. You gain resistance to that damage type and your unarmed strikes deal that damage type.",
        type: "general"
    },
    fey_ancestry: {
        name: "Fey Ancestry",
        description: "You have fey blood in your lineage.",
        prerequisite: "Charisma 13+",
        effect: "You have advantage on saving throws against being charmed, and magic can't put you to sleep.",
        type: "general"
    },
    giant_strength: {
        name: "Giant Strength",
        description: "You possess the strength of giants.",
        prerequisite: "Strength 17+",
        effect: "Your carrying capacity doubles, and you can wield weapons one size larger than normal without penalty.",
        type: "general"
    },
    immortal_vigor: {
        name: "Immortal Vigor",
        description: "You age more slowly than normal.",
        prerequisite: "Constitution 17+, level 10+",
        effect: "You age at half the normal rate and have advantage on death saving throws.",
        type: "general"
    },
    planar_binding: {
        name: "Planar Binding",
        description: "You can bind extraplanar creatures to your service.",
        prerequisite: "Charisma 15+, ability to cast 5th level spells",
        effect: "You can cast planar binding once per long rest without expending a spell slot.",
        type: "magic"
    },
    void_touched: {
        name: "Void Touched",
        description: "You have been exposed to the void between planes.",
        prerequisite: "Wisdom 15+",
        effect: "You have resistance to necrotic damage and can see normally in magical darkness.",
        type: "general"
    }
};

// Export for merging
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ADDITIONAL_FEATS;
}