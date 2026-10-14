// Comprehensive Spell Database for Decennium Descent
// Organized by school and level with search functionality

export const SPELL_SCHOOLS = [
  "Abjuration",
  "Conjuration", 
  "Divination",
  "Enchantment",
  "Evocation",
  "Illusion",
  "Necromancy",
  "Transmutation",
  "Universal"
];

export const SPELL_LEVELS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

export const SPELLS = {
  // Cantrips (Level 0) - Abjuration
  "resistance": {
    name: "Resistance",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a miniature cloak)",
    duration: "Concentration, up to 1 minute",
    description: "You touch one willing creature. Once before the spell ends, the target can roll a d4 and add the number rolled to one saving throw of its choice. The spell then ends.",
    classes: ["Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "ward": {
    name: "Ward",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Self",
    components: "V, S",
    duration: "1 round",
    description: "You create a shimmering barrier around yourself. You gain a +1 bonus to AC until the start of your next turn.",
    classes: ["Cleric", "Paladin", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  // Conjuration Cantrips
  "acid-splash": {
    name: "Acid Splash",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a small orb of acid that you can hurl at a target. You must succeed on a ranged touch attack to hit your target. The orb deals 1d3 points of acid damage.",
    classes: ["Wizard"]
  },
  "conjure-water": {
    name: "Conjure Water",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create up to 2 gallons of clean, drinkable water in an open container within range. The water appears in the container and remains there until used.",
    classes: ["Cleric", "Druid", "Ranger"]
  },
  "mending": {
    name: "Mending",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V, S",
    duration: "Instantaneous",
    description: "You repair minor breaks or tears in objects. All of the pieces of an object must be present for this spell to function. A break or tear in an object that is no larger than 1 foot in any dimension can be fixed.",
    classes: ["Bard", "Cleric", "Druid", "Wizard"]
  },
  "summon-minor-ally": {
    name: "Summon Minor Ally",
    level: 0,
    school: "Conjuration",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a tiny bag and a small candle)",
    duration: "1 minute",
    description: "You summon a Tiny animal (such as a bat, rat, or toad) to serve you as a temporary ally. The creature appears where you designate and acts immediately.",
    classes: ["Druid", "Ranger", "Wizard"]
  },
  "minor-portal": {
    name: "Minor Portal",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "5 ft.",
    components: "V, S",
    duration: "Instantaneous",
    description: "You instantly teleport to a designated space within 5 feet. You must have line of sight to the destination, and the space must be unoccupied.",
    classes: ["Wizard"]
  },
  // Illusion Cantrips
  "ghost-sound": {
    name: "Ghost Sound",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a bit of wool or a small lump of wax)",
    duration: "1 round/level",
    description: "Ghost sound allows you to create a volume of sound that rises, recedes, approaches, or remains at a fixed place. You choose what type of sound ghost sound creates when casting it.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "color-spray": {
    name: "Color Spray",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "15 ft.",
    components: "V, S, M (red, yellow, and blue powder or colored sand)",
    duration: "Instantaneous",
    description: "A vivid cone of clashing colors springs forth from your hand, causing creatures to become stunned, perhaps also blinded, and possibly knocking them unconscious.",
    classes: ["Wizard", "Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "silent-image": {
    name: "Silent Image",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F (a bit of fleece)",
    duration: "Concentration",
    description: "This spell creates the visual illusion of an object, creature, or force, as visualized by you. The illusion does not create sound, smell, texture, or temperature.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "ventriloquism": {
    name: "Ventriloquism",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, F (parchment rolled into cone)",
    duration: "1 min./level",
    description: "You can make your voice (or any sound that you can normally make vocally) seem to issue from someplace else.",
    classes: ["Bard", "Wizard"]
  },
  "minor-illusion": {
    name: "Minor Illusion",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "30 feet",
    components: "S, M (a bit of fleece)",
    duration: "1 minute",
    description: "You create a sound or an image of an object within range that lasts for the duration. The illusion also ends if you dismiss it as an action or cast this spell again. If you create a sound, its volume can range from a whisper to a scream. It can be your voice, someone else's voice, a lion's roar, a beating of drums, or any other sound you choose. The sound continues unabated throughout the duration, or you can make discrete sounds at different times before the spell ends. If you create an image of an object—such as a chair, muddy footprints, or a small chest—it must be no larger than a 5-foot cube. The image can't create sound, light, smell, or any other sensory effect. Physical interaction with the image reveals it to be an illusion, because things can pass through it.",
    classes: ["Bard", "Warlock", "Wizard"]
  },
  "arcane-ray": {
    name: "Arcane Ray",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a shimmering ray of pure magical energy that streaks toward a creature within range. Make a ranged spell attack against the target. On a hit, the target takes 1d4 force damage. This spell's damage increases by 1d4 when you reach 5th level (2d4), 11th level (3d4), and 17th level (4d4).",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "sparkbolt": {
    name: "Sparkbolt",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You hurl a mote of crackling energy at a creature within range. Make a ranged spell attack against the target. On a hit, the target takes 1d6 lightning damage, and if the target is wearing metal armor or is made of metal, it takes an additional 1 lightning damage. This spell's damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level (4d6).",
    classes: ["Sorcerer", "Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "freezing-touch": {
    name: "Freezing Touch",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "You touch a creature, and a numbing cold flows from your hand. Make a melee spell attack against the target. On a hit, the target takes 1d8 cold damage, and its speed is reduced by 10 feet until the end of its next turn. This spell's damage increases by 1d8 when you reach 5th level (2d8), 11th level (3d8), and 17th level (4d8).",
    classes: ["Druid", "Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  // Transmutation Cantrips
  "shimmerstep": {
    name: "Shimmerstep",
    level: 0,
    school: "Transmutation",
    castingTime: "1 swift action",
    range: "Personal",
    components: "S",
    duration: "Instantaneous",
    description: "You briefly shimmer and shift your position. You can move 5 feet in any direction. This movement does not provoke attacks of opportunity.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "stone-touch": {
    name: "Stone Touch",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 round",
    description: "You temporarily harden a small object or a 1-foot square surface, making it more resilient. If you touch a creature's armor, it gains a +1 circumstance bonus to AC for 1 round.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "minor-enhancement": {
    name: "Minor Enhancement",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 round",
    description: "You touch a creature and grant it a minor physical boost. The target gains a +1 circumstance bonus on its next Strength or Dexterity-based skill check.",
    classes: ["Bard", "Cleric", "Druid", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  // Divination Cantrips
  "detect-magic-divination": {
    name: "Detect Magic",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "Self",
    components: "V, S",
    duration: "Concentration, up to 10 minutes",
    description: "For the duration, you sense the presence of magic within 30 feet of you. If you sense magic in this way, you can use your action to see a faint aura around any visible creature or object in the area that bears magic.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Wizard"]
  },
  "detect-poison": {
    name: "Detect Poison",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You determine whether a creature, object, or area has been poisoned or is poisonous. You can determine the exact type of poison with a DC 20 Wisdom check.",
    classes: ["Cleric", "Druid", "Paladin", "Ranger"]
  },
  "guidance": {
    name: "Guidance",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Concentration, up to 1 minute",
    description: "You touch one willing creature. Once before the spell ends, the target can roll a d4 and add the number rolled to one ability check of its choice.",
    classes: ["Cleric", "Druid"]
  },
  "know-direction": {
    name: "Know Direction",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "Instantaneous",
    description: "You instantly know the direction of north from your current position. The spell is effective in any environment in which 'north' exists, but it may not work in extraplanar settings.",
    classes: ["Bard", "Druid", "Ranger"]
  },
  "read-magic-divination": {
    name: "Read Magic",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, F (a clear crystal or mineral prism)",
    duration: "10 min./level",
    description: "You can decipher magical inscriptions on objects that would otherwise be unintelligible. This deciphering does not normally invoke the magic contained in the writing.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Wizard"]
  },
  "sense-motive": {
    name: "Sense Motive",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 minute/level",
    description: "You gain a +5 insight bonus on Sense Motive checks to determine whether someone is lying or to discern hidden motives.",
    classes: ["Bard", "Cleric", "Paladin"]
  },
  "true-strike-lesser": {
    name: "True Strike, Lesser",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, F (a small straight piece of iron)",
    duration: "See text",
    description: "Your next attack roll (if it is made before the end of the next round) gains a +10 insight bonus. Additionally, you are not affected by the miss chance that applies to attackers trying to strike a concealed target.",
    classes: ["Bard", "Ranger", "Wizard"]
  },
  "detect-undead-lesser": {
    name: "Detect Undead, Lesser",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "60 ft.",
    components: "V, S, M (earth from a grave)",
    duration: "Concentration, up to 1 minute",
    description: "You can detect the aura that surrounds undead creatures. The amount of information revealed depends on how long you study a particular area.",
    classes: ["Cleric", "Paladin"]
  },
  // Universal Cantrips
  "detect-magic": {
    name: "Detect Magic",
    level: 0,
    school: "Universal",
    castingTime: "1 action",
    range: "Self",
    components: "V, S",
    duration: "Concentration, up to 10 minutes",
    description: "For the duration, you sense the presence of magic within 30 feet of you. If you sense magic in this way, you can use your action to see a faint aura around any visible creature or object.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Wizard", "Mirrorsage", "Oracle", "Shaman"]
  },
  "read-magic": {
    name: "Read Magic",
    level: 0,
    school: "Universal",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, F (a clear crystal or mineral prism)",
    duration: "10 min./level",
    description: "You can decipher magical inscriptions on objects that would otherwise be unintelligible. This deciphering does not normally invoke the magic contained in the writing.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Wizard"]
  },
  "magical-ping": {
    name: "Magical Ping",
    level: 0,
    school: "Universal",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "Instantaneous",
    description: "You send out a subtle pulse of arcane energy. For a brief moment, you become aware of the number and general location of any active magical effects or items within a 10-foot radius.",
    classes: ["Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "fire-bolt": {
    name: "Fire Bolt",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You hurl a mote of fire at a creature or object within range. Make a ranged spell attack. On a hit, the target takes 1d10 fire damage.",
    classes: ["Mage"]
  },

  "flame-lash": {
    name: "Flame Lash",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "15 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a whip of fire that lashes out at a target. Make a ranged spell attack. On a hit, the target takes 1d4 fire damage and is pulled 5 feet closer to you.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "mage-hand-enhanced": {
    name: "Mage Hand",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Concentration, up to 1 minute",
    description: "You point your finger at an object and can lift it and move it at will from a distance. As a move action, you can move the object up to 15 feet in any direction.",
    classes: ["Bard", "Wizard"]
  },
  "minor-illusion-enhanced": {
    name: "Minor Illusion",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 minute/level",
    description: "You create a visual illusion of an object, creature, or force. The illusion does not create sound, smell, texture, or temperature. You can move the image within the limits of the size of the effect.",
    classes: ["Bard", "Wizard"]
  },
  "disguise-self-cantrip": {
    name: "Disguise Self",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "10 min./level",
    description: "You make yourself—including clothing, armor, weapons, and equipment—look different. You can seem 1 foot shorter or taller, thin, fat, or in between.",
    classes: ["Bard", "Wizard"]
  },
  "prestidigitation-enhanced": {
    name: "Prestidigitation",
    level: 0,
    school: "Universal",
    castingTime: "1 action",
    range: "10 feet",
    components: "V, S",
    duration: "1 hour",
    description: "Prestidigitations are minor magical tricks. Once cast, a prestidigitation spell enables you to perform simple magical effects for 1 hour.",
    classes: ["Bard", "Wizard"]
  },

  // Level 1 Spells - Abjuration
  "shield-enhanced": {
    name: "Shield",
    level: 1,
    school: "Abjuration",
    castingTime: "1 reaction",
    range: "Self",
    components: "V, S",
    duration: "1 round",
    description: "An invisible barrier of magical force appears and protects you. Until the start of your next turn, you have a +5 bonus to AC, including against the triggering attack.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "protection-from-evil": {
    name: "Protection from Evil",
    level: 1,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (holy water or powdered silver and iron)",
    duration: "Concentration, up to 10 minutes",
    description: "Until the spell ends, one willing creature you touch is protected against certain types of creatures: aberrations, celestials, elementals, fey, fiends, and undead.",
    classes: ["Cleric", "Paladin", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "sanctuary": {
    name: "Sanctuary",
    level: 1,
    school: "Abjuration",
    castingTime: "1 bonus action",
    range: "30 feet",
    components: "V, S, M (a small silver mirror)",
    duration: "1 minute",
    description: "You ward a creature within range against attack. Until the spell ends, any creature who targets the warded creature with an attack or a harmful spell must first make a Wisdom saving throw.",
    classes: ["Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  // Level 1 Spells - Conjuration
  "summon-monster-i": {
    name: "Summon Monster I",
    level: 1,
    school: "Conjuration",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, F/DF (a tiny bag and a small candle)",
    duration: "1 round/level",
    description: "This spell summons an extraplanar creature (typically an outsider, elemental, or magical beast native to another plane). It appears where you designate and acts immediately.",
    classes: ["Bard", "Cleric", "Wizard"]
  },
  "grease": {
    name: "Grease",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S, M (a bit of pork rind or butter)",
    duration: "1 minute",
    description: "Slick grease covers the ground in a 10-foot square centered on a point within range and turns it into difficult terrain for the duration.",
    classes: ["Wizard"]
  },
  "unseen-servant": {
    name: "Unseen Servant",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S, M (a piece of string and a bit of wood)",
    duration: "1 hour",
    description: "This spell creates an invisible, mindless, shapeless force that performs simple tasks at your command until the spell ends.",
    classes: ["Bard", "Wizard"]
  },
  // Level 1 Spells - Divination
  "comprehend-languages": {
    name: "Comprehend Languages",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "Self",
    components: "V, S, M (a pinch of soot and salt)",
    duration: "1 hour",
    description: "For the duration, you understand the literal meaning of any spoken language that you hear. You also understand any written language that you see, but you must be touching the surface on which the words are written.",
    classes: ["Bard", "Cleric", "Wizard"]
  },
  "detect-secret-doors": {
    name: "Detect Secret Doors",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "60 ft.",
    components: "V, S",
    duration: "Concentration, up to 10 minutes",
    description: "You can detect secret doors, compartments, caches, and so forth. Only passages, doors, or openings that have been specifically constructed to escape detection are detected by this spell.",
    classes: ["Bard", "Wizard"]
  },
  "detect-undead": {
    name: "Detect Undead",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "60 ft.",
    components: "V, S, M (earth from a grave)",
    duration: "Concentration, up to 10 minutes",
    description: "You can detect the aura that surrounds undead creatures. The amount of information revealed depends on how long you study a particular area or subject.",
    classes: ["Cleric", "Paladin"]
  },
  "identify": {
    name: "Identify",
    level: 1,
    school: "Divination",
    castingTime: "1 minute",
    range: "Touch",
    components: "V, S, M (a pearl worth at least 100 gp and an owl feather)",
    duration: "Instantaneous",
    description: "You choose one object that you must touch throughout the casting of the spell. If it is a magic item or some other magic-imbued object, you learn its properties and how to use them.",
    classes: ["Bard", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "true-strike": {
    name: "True Strike",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "30 feet",
    components: "S",
    duration: "Concentration, up to 1 round",
    description: "You extend your hand and point a finger at a target in range. Your magic grants you a brief insight into the target's defenses. On your next turn, you gain advantage on your first attack roll against the target.",
    classes: ["Bard", "Ranger", "Wizard"]
  },
  "detect-charm": {
    name: "Detect Charm",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "30 ft.",
    components: "V, S",
    duration: "Concentration, up to 1 minute",
    description: "For the duration, you know if there is an enchantment spell or effect within 30 feet of you. You also know the location of any such effect but not its nature.",
    classes: ["Cleric", "Paladin"]
  },
  "anticipate-peril": {
    name: "Anticipate Peril",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 minute/level",
    description: "A creature touched by this spell becomes more aware of danger. The target gains a +2 insight bonus on Reflex saves and a +2 insight bonus to AC against attacks of opportunity.",
    classes: ["Cleric", "Ranger"]
  },
  "heightened-awareness": {
    name: "Heightened Awareness",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "10 minutes/level",
    description: "Your senses become preternaturally sharp. You gain a +4 competence bonus on Listen and Spot checks for the duration of the spell.",
    classes: ["Bard", "Ranger"]
  },
  // Level 1 Spells - Enchantment
  "charm-person-enhanced": {
    name: "Charm Person",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "30 feet",
    components: "V, S",
    duration: "1 hour",
    description: "You attempt to charm a humanoid you can see within range. It must make a Wisdom saving throw, and it does so with advantage if you or your companions are fighting it.",
    classes: ["Bard", "Druid", "Wizard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },

  "disguise-self-1": {
    name: "Disguise Self",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "Self",
    components: "V, S",
    duration: "1 hour",
    description: "You make yourself—including your clothing, armor, weapons, and other belongings on your person—look different until the spell ends or until you use your action to dismiss it.",
    classes: ["Bard", "Wizard"]
  },

  "blur": {
    name: "Blur",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "Self",
    components: "V",
    duration: "Concentration, up to 1 minute",
    description: "Your body becomes blurred, shifting and wavering to all who can see you. For the duration, any creature has disadvantage on attack rolls against you. An attacker is immune to this effect if it doesn't rely on sight, as with blindsight, or can see through illusions, as with truesight.",
    classes: ["Sorcerer", "Wizard", "Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },

  "blur-self": {
    name: "Blur Self",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 min./level",
    description: "The subject's outline appears blurred, shifting and wavering. This distortion grants the subject concealment (20% miss chance). A see invisibility spell does not counteract the blur effect, but a true seeing spell does. Opponents that cannot see the subject ignore the spell's effect.",
    classes: ["Bard", "Wizard"]
  },
  "illusory-disguise": {
    name: "Illusory Disguise",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "10 min./level",
    description: "You make yourself—including your clothing, armor, weapons, and other belongings on your person—look different. You can seem 1 foot shorter or taller and can appear thin, fat, or in between. You cannot change your body type, so you must adopt a form that has the same basic arrangement of limbs. Otherwise, the extent of the apparent change is up to you. The changes wrought by this spell fail to hold up to physical inspection.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  // Level 1 Spells - Transmutation
  "expeditious-retreat": {
    name: "Expeditious Retreat",
    level: 1,
    school: "Transmutation",
    castingTime: "1 bonus action",
    range: "Self",
    components: "V, S",
    duration: "Concentration, up to 10 minutes",
    description: "This spell allows you to move at an incredible pace. When you cast this spell, and then as a bonus action on each of your turns until the spell ends, you can take the Dash action.",
    classes: ["Wizard"]
  },
  "feather-fall": {
    name: "Feather Fall",
    level: 1,
    school: "Transmutation",
    castingTime: "1 reaction",
    range: "60 feet",
    components: "V, M (a small feather or piece of down)",
    duration: "1 minute",
    description: "Choose up to five falling creatures within range. A falling creature's rate of descent slows to 60 feet per round until the spell ends.",
    classes: ["Bard", "Wizard"]
  },
  "jump": {
    name: "Jump",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a grasshopper's hind leg)",
    duration: "1 minute",
    description: "You touch a creature. The creature's jump distance is tripled until the spell ends.",
    classes: ["Druid", "Ranger", "Wizard"]
  },
  // Level 1 Spells - Universal
  "spellshift": {
    name: "Spellshift",
    level: 1,
    school: "Universal",
    castingTime: "1 swift action",
    range: "Personal",
    components: "V",
    duration: "Instantaneous",
    description: "You can alter the energy type of a spell you are about to cast. Choose a different energy type (acid, cold, electricity, fire, or sonic) for the spell.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "arcane-lock": {
    name: "Arcane Lock",
    level: 1,
    school: "Universal",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (gold dust worth at least 25 gp, which the spell consumes)",
    duration: "Until dispelled",
    description: "You touch a closed door, window, gate, chest, or other entryway, and it becomes locked for the duration.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "mage-hand": {
    name: "Mage Hand",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "30 feet",
    components: "V, S",
    duration: "1 minute",
    description: "A spectral, floating hand appears at a point you choose within range. The hand can manipulate objects, open doors, or retrieve items.",
    classes: ["Mage", "Bard"]
  },
  "prestidigitation": {
    name: "Prestidigitation",
    level: 0,
    school: "Universal",
    castingTime: "1 action",
    range: "10 feet",
    components: "V, S",
    duration: "1 hour",
    description: "This spell is a minor magical trick that novice spellcasters use for practice. You create one of several minor effects.",
    classes: ["Mage", "Bard", "Cleric", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "mage-light": {
    name: "Mage Light",
    level: 0,
    school: "Universal",
    castingTime: "1 action",
    range: "Touch",
    components: "V, M (a bit of phosphorus)",
    duration: "1 hour/level",
    description: "You touch an object, causing it to glow like a torch. It sheds normal light in a 20-foot radius.",
    classes: ["Mage", "Cleric", "Bard", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "arcane-tether": {
    name: "Arcane Tether",
    level: 0,
    school: "Universal",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "10 min./level",
    description: "You create a faint arcane link between yourself and a target object or willing creature. You have a vague sense of the target's direction and distance.",
    classes: ["Bard", "Mage", "Cleric", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "glyph-trace": {
    name: "Glyph Trace",
    level: 0,
    school: "Universal",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Concentration, up to 1 min./level",
    description: "You cause any magical runes, sigils, or glyphs to faintly glow. Gives +5 circumstance bonus on Perception checks to find magical traps.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  "sacred-flame": {
    name: "Sacred Flame",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "Flame-like radiance descends on a creature that you can see within range. The target must succeed on a Dexterity saving throw or take 1d8 radiant damage.",
    classes: ["Cleric"]
  },
  "thaumaturgy": {
    name: "Thaumaturgy",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "30 feet",
    components: "V",
    duration: "1 minute",
    description: "You manifest a minor wonder, a sign of supernatural power, within range.",
    classes: ["Cleric"]
  },

  // 1ST LEVEL SPELLS
  "magic-missile": {
    name: "Magic Missile",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range. A dart deals 1d4 + 1 force damage.",
    classes: ["Mage"]
  },
  "cure-wounds": {
    name: "Cure Wounds",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier.",
    classes: ["Cleric", "Bard", "Paladin", "Ranger"]
  },
  "fireburst": {
    name: "Fireburst",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (10-foot radius)",
    components: "V, S",
    duration: "Instantaneous",
    description: "Flames burst out from you in all directions. Each creature within 10 feet of you must make a Dexterity saving throw. On a failed save, a creature takes 2d6 fire damage, or half as much on a successful save.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "frost-arrow": {
    name: "Frost Arrow",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create an arrow of crystalline ice and hurl it at a target. Make a ranged spell attack. On a hit, the target takes 1d8 cold damage and their speed is reduced by 10 feet until the end of their next turn.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "chain-jolt": {
    name: "Chain Jolt",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "Lightning jumps from your fingertips to a target, then arcs to nearby enemies. Make a ranged spell attack against the primary target. On a hit, it takes 1d6 lightning damage, and the lightning jumps to up to 2 other creatures within 15 feet of the original target, each taking 1d4 lightning damage.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "force-spike": {
    name: "Force Spike",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "90 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a spike of pure force energy that pierces through armor and magical defenses. Make a ranged spell attack. On a hit, the target takes 1d8 + 2 force damage. This attack ignores cover and magical armor bonuses.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },

  "healing-word": {
    name: "Healing Word",
    level: 1,
    school: "Evocation",
    castingTime: "1 bonus action",
    range: "60 feet",
    components: "V",
    duration: "Instantaneous",
    description: "A creature of your choice that you can see within range regains hit points equal to 1d4 + your spellcasting ability modifier.",
    classes: ["Bard", "Cleric"]
  },

  "sleep": {
    name: "Sleep",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "90 feet",
    components: "V, S, M (a pinch of fine sand, rose petals, or a cricket)",
    duration: "1 minute",
    description: "This spell sends creatures into a magical slumber. Roll 5d8; the total is how many hit points of creatures this spell can affect.",
    classes: ["Bard", "Mage", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },

  "burning-hands": {
    name: "Burning Hands",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (15-foot cone)",
    components: "V, S",
    duration: "Instantaneous",
    description: "As you hold your hands with thumbs touching and fingers spread, a thin sheet of flames shoots forth from your outstretched fingertips.",
    classes: ["Mage"]
  },



  // 2ND LEVEL SPELLS
  "scorching-ray": {
    name: "Scorching Ray",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You blast your enemies with fiery rays. You may fire one ray, plus one additional ray for every four levels beyond 1st. Each ray requires a ranged touch attack to hit and deals 1d6 points of fire damage.",
    classes: ["Wizard"]
  },
  "lightning-pulse": {
    name: "Lightning Pulse",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (15-foot radius)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You release a pulse of electrical energy. Each creature within 15 feet of you must make a Constitution saving throw. On a failed save, a creature takes 3d6 lightning damage and is stunned until the end of their next turn. On a successful save, they take half damage and are not stunned.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "frost-nova": {
    name: "Frost Nova",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (20-foot radius)",
    components: "V, S",
    duration: "Instantaneous",
    description: "Ice explodes outward from you in all directions. Each creature within 20 feet must make a Dexterity saving throw. On a failed save, a creature takes 2d8 cold damage and their speed becomes 0 until the end of their next turn. On a successful save, they take half damage and their speed is reduced by half.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "arcane-implosion": {
    name: "Arcane Implosion",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a point of intense magical energy that implodes. Choose a point within range. Each creature within a 10-foot radius of that point must make a Strength saving throw. On a failed save, a creature takes 2d6 force damage and is pulled 10 feet toward the center. On a successful save, they take half damage and are not moved.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "acid-arrow": {
    name: "Acid Arrow",
    level: 2,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (rhubarb leaf and an adder's stomach), F (a dart)",
    duration: "1 round + 1 round per three levels",
    description: "An arrow of acid springs from your hand and speeds to its target. You must succeed on a ranged touch attack to hit your target. The arrow deals 2d4 points of acid damage with no splash damage.",
    classes: ["Wizard"]
  },

  "cat-grace": {
    name: "Cat's Grace",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a pinch of cat fur)",
    duration: "1 min./level",
    description: "The transmuted creature becomes more graceful, agile, and coordinated. The spell grants a +4 enhancement bonus to Dexterity.",
    classes: ["Bard", "Druid", "Ranger", "Wizard"]
  },
  "fireball": {
    name: "Fireball",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "150 feet",
    components: "V, S, M (a tiny ball of bat guano and sulfur)",
    duration: "Instantaneous",
    description: "A bright flash of fire expands from your fingertips. Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw.",
    classes: ["Mage"]
  },
  "hold-person": {
    name: "Hold Person",
    level: 2,
    school: "Enchantment",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S, M (a small, straight piece of iron)",
    duration: "Concentration, up to 1 minute",
    description: "Choose a humanoid that you can see within range. The target must succeed on a Wisdom saving throw or be paralyzed for the duration.",
    classes: ["Bard", "Cleric", "Mage"]
  },
  "invisibility": {
    name: "Invisibility",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (an eyelash encased in gum arabic)",
    duration: "Concentration, up to 1 hour",
    description: "A creature you touch becomes invisible until the spell ends. Anything the target is wearing or carrying is invisible as long as it is on the target's person.",
    classes: ["Bard", "Mage", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "web": {
    name: "Web",
    level: 2,
    school: "Conjuration",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S, M (a bit of spiderweb)",
    duration: "Concentration, up to 1 hour",
    description: "You conjure a mass of thick, sticky webbing at a point of your choice within range.",
    classes: ["Mage"]
  },
  "spiritual-weapon": {
    name: "Spiritual Weapon",
    level: 2,
    school: "Evocation",
    castingTime: "1 bonus action",
    range: "60 feet",
    components: "V, S",
    duration: "1 minute",
    description: "You create a floating, spectral weapon within range that lasts for the duration or until you cast this spell again.",
    classes: ["Cleric"]
  },
  // Level 2 Spells - Divination
  "augury": {
    name: "Augury",
    level: 2,
    school: "Divination",
    castingTime: "1 minute",
    range: "Personal",
    components: "V, S, M (specially marked sticks, bones, or similar tokens worth at least 25 gp)",
    duration: "Instantaneous",
    description: "By casting gem-inlaid sticks, rolling dragon bones, laying out ornate cards, or employing some other divining tool, you receive an omen from an otherworldly entity about the results of a specific course of action.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "detect-thoughts": {
    name: "Detect Thoughts",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "Self",
    components: "V, S, M (a copper piece)",
    duration: "Concentration, up to 1 minute",
    description: "For the duration, you can read the thoughts of certain creatures. When you cast the spell and as your action on each turn until the spell ends, you can focus your mind on any one creature.",
    classes: ["Bard", "Wizard"]
  },
  "find-traps": {
    name: "Find Traps",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You sense the presence of any trap within range that is within line of sight. A trap, for the purpose of this spell, includes anything that would inflict a sudden or unexpected effect.",
    classes: ["Cleric", "Druid", "Ranger"]
  },
  "locate-object": {
    name: "Locate Object",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "Self",
    components: "V, S, M (a forked twig)",
    duration: "Concentration, up to 10 minutes",
    description: "Describe or name an object that is familiar to you. You sense the direction to the object's location, as long as that object is within 1,000 feet of you.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Wizard"]
  },
  "see-invisibility": {
    name: "See Invisibility",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "Self",
    components: "V, S, M (a pinch of talc and a small sprinkling of powdered silver)",
    duration: "1 hour",
    description: "For the duration, you see invisible creatures and objects as if they were visible, and you can see into the Ethereal Plane.",
    classes: ["Bard", "Wizard"]
  },
  "status": {
    name: "Status",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a bit of fur from a bloodhound)",
    duration: "8 hours",
    description: "You touch a creature and magically know the creature's current status. You know if the creature is alive, wounded, disabled, staggered, unconscious, dying, nauseated, panicked, stunned, poisoned, diseased, confused, or otherwise debilitated.",
    classes: ["Cleric"]
  },
  "ancestral-communion": {
    name: "Ancestral Communion",
    level: 2,
    school: "Divination",
    castingTime: "10 minutes",
    range: "Personal",
    components: "V, S, M (burning incense)",
    duration: "Instantaneous",
    description: "You contact the spirits of your ancestors or the collective unconscious of your race and ask a simple question that can be answered with yes or no. You have a 60% + 1% per caster level chance of getting a correct answer.",
    classes: ["Cleric", "Druid"]
  },
  "zone-of-truth": {
    name: "Zone of Truth",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S",
    duration: "10 minutes",
    description: "You create a magical zone that guards against deception in a 15-foot-radius sphere centered on a point of your choice within range. Until the spell ends, a creature that enters the spell's area for the first time on a turn or starts its turn there must make a Charisma saving throw.",
    classes: ["Bard", "Cleric", "Paladin", "Mirrorsage", "Oracle", "Ranger", "Shaman"]
  },

  // Level 2 Spells - Illusion
  "phantasmal-assailants": {
    name: "Phantasmal Assailants",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 round/level",
    description: "You create phantasmal images of attackers that only the target can see. The target must make a Will save each round or take 1d6 points of damage and be shaken for 1 round. Even with a successful save, the target takes 1 point of damage. This spell draws inspiration from the mind-affecting illusions of Elder Scrolls and the phantasmal abilities of EverQuest illusionists.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "invisibility-sphere": {
    name: "Invisibility Sphere",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "Personal or touch",
    components: "V, S, M (an eyelash encased in gum arabic)",
    duration: "1 min./level (D)",
    description: "This spell functions like invisibility, except that this spell confers invisibility upon all creatures within 10 feet of the recipient. The center of the effect is mobile with the recipient. Those affected by this spell can see each other and themselves as if unaffected by the spell. Any affected creature that attacks any creature breaks the spell for all recipients.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },

  // HIGHER LEVEL SPELLS
  "counterspell": {
    name: "Counterspell",
    level: 3,
    school: "Abjuration",
    castingTime: "1 reaction",
    range: "60 feet",
    components: "S",
    duration: "Instantaneous",
    description: "You attempt to interrupt a creature in the process of casting a spell.",
    classes: ["Mage", "Cleric", "Druid", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "haste": {
    name: "Haste",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a shaving of licorice root)",
    duration: "1 round/level",
    description: "The transmuted creature moves and acts more quickly than normal. This extra speed has several effects.",
    classes: ["Bard", "Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "slow": {
    name: "Slow",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a drop of molasses)",
    duration: "1 round/level",
    description: "An affected creature moves and attacks at a drastically slowed rate.",
    classes: ["Bard", "Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "fly": {
    name: "Fly",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, F (a wing feather from any bird)",
    duration: "1 min./level",
    description: "The subject can fly at a speed of 60 feet (or 40 feet if it wears medium or heavy armor, or if it carries a medium or heavy load).",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "dispel-magic": {
    name: "Dispel Magic",
    level: 3,
    school: "Abjuration",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "Choose one creature, object, or magical effect within range. Any spell of 3rd level or lower on the target ends.",
    classes: ["Bard", "Cleric", "Mage", "Paladin", "Druid", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "lightning-bolt": {
    name: "Lightning Bolt",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (100-foot line)",
    components: "V, S, M (a bit of fur and a rod of amber, crystal, or glass)",
    duration: "Instantaneous",
    description: "A stroke of lightning forming a line 100 feet long and 5 feet wide blasts out from you in a direction you choose.",
    classes: ["Mage"]
  },
  "flame-geyser": {
    name: "Flame Geyser",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S, M (a piece of sulfur)",
    duration: "Instantaneous",
    description: "You cause a geyser of flame to erupt from the ground at a point you can see within range. Each creature in a 10-foot radius, 20-foot high cylinder centered on that point must make a Dexterity saving throw. On a failed save, a creature takes 4d6 fire damage, or half as much on a successful save.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "chain-lightning-jr": {
    name: "Chain Lightning Jr.",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "150 feet",
    components: "V, S, M (a bit of fur; a piece of amber, glass, or crystal rod)",
    duration: "Instantaneous",
    description: "You create a bolt of lightning that arcs toward a target of your choice that you can see within range. The lightning then jumps to up to 3 other targets within 30 feet of the original target. Each target must make a Dexterity saving throw, taking 3d8 lightning damage on a failed save, or half as much on a successful one.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "shardstorm": {
    name: "Shardstorm",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (30-foot cone)",
    components: "V, S, M (a piece of crystal or glass)",
    duration: "Instantaneous",
    description: "You create a storm of razor-sharp crystal shards in a 30-foot cone. Each creature in the area must make a Dexterity saving throw. On a failed save, a creature takes 3d6 piercing damage and 1d6 force damage. On a successful save, they take half damage.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  // Level 3 Spells - Divination
  "arcane-sight": {
    name: "Arcane Sight",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 min./level",
    description: "This spell makes your eyes glow blue and allows you to see magical auras within 120 feet of you. The effect is similar to that of a detect magic spell, but arcane sight does not require concentration.",
    classes: ["Wizard"]
  },
  "clairaudience-clairvoyance": {
    name: "Clairaudience/Clairvoyance",
    level: 3,
    school: "Divination",
    castingTime: "10 minutes",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F/DF (a small horn or a glass eye)",
    duration: "1 min./level",
    description: "You create an invisible magical sensor within range in a location familiar to you or in an obvious location that is unfamiliar to you. The sensor can be directed to look in any direction.",
    classes: ["Bard", "Cleric", "Wizard"]
  },
  "speak-with-dead": {
    name: "Speak with Dead",
    level: 3,
    school: "Divination",
    castingTime: "10 minutes",
    range: "10 ft.",
    components: "V, S, M (burning incense)",
    duration: "10 minutes",
    description: "You grant the semblance of life and intelligence to a corpse, allowing it to answer several questions that you put to it.",
    classes: ["Cleric"]
  },
  "tongues": {
    name: "Tongues",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "Touch",
    components: "V, M (a small clay model of a ziggurat)",
    duration: "1 hour",
    description: "This spell grants the creature touched the ability to speak and understand the language of any intelligent creature, whether it is a racial tongue or a regional dialect.",
    classes: ["Bard", "Cleric", "Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "locate-weakness": {
    name: "Locate Weakness",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 round/level",
    description: "You can sense the defensive weaknesses of creatures within the spell's range. You gain a +5 insight bonus on attack rolls against creatures in the area.",
    classes: ["Ranger", "Wizard"]
  },
  "seek-thoughts": {
    name: "Seek Thoughts",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "40 ft.",
    components: "V, S, M (a copper piece)",
    duration: "Concentration, up to 1 minute",
    description: "Similar to detect thoughts, but you can search for specific thoughts or memories within the minds of creatures in the area.",
    classes: ["Bard", "Wizard"]
  },
  "scrying": {
    name: "Scrying",
    level: 3,
    school: "Divination",
    castingTime: "10 minutes",
    range: "See text",
    components: "V, S, M/DF (a focus worth at least 1,000 gp)",
    duration: "1 hour",
    description: "You can observe a creature at any distance. If the subject succeeds on a Will save, the scrying attempt simply fails.",
    classes: ["Bard", "Cleric", "Druid", "Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "tactical-insight": {
    name: "Tactical Insight",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 round/level",
    description: "You gain an intuitive understanding of battlefield tactics. You gain a +4 insight bonus to initiative and can act in the surprise round even if you are surprised.",
    classes: ["Bard", "Ranger"]
  },

  // Level 3 Spells - Illusion
  "displacement": {
    name: "Displacement",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "Touch",
    components: "V, M (a piece of leather twisted into a loop)",
    duration: "1 round/level",
    description: "The subject of this spell appears to be about 2 feet away from its true location. The creature benefits from a 50% miss chance as if it had total concealment. However, unlike actual total concealment, displacement does not prevent enemies from targeting the creature normally. True seeing reveals its true location and negates the miss chance.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "illusory-script": {
    name: "Illusory Script",
    level: 3,
    school: "Illusion",
    castingTime: "1 minute or longer",
    range: "Touch",
    components: "V, S, M (a lead-based ink worth at least 50 gp, which the spell consumes)",
    duration: "10 days",
    description: "You write on parchment, paper, or some other suitable writing material and imbue it with a potent illusion that lasts for the duration. To you and any creatures you designate when you cast the spell, the writing appears normal, written in your hand, and conveys whatever meaning you intended when you wrote the text. To all others, the writing appears as if it were written in an unknown or magical script that is unintelligible.",
    classes: ["Bard", "Warlock", "Wizard"]
  },
  "major-image": {
    name: "Major Image",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S, M (a bit of fleece)",
    duration: "Concentration, up to 10 minutes",
    description: "You create the image of an object, a creature, or some other visible phenomenon that is no larger than a 20-foot cube. The image appears at a spot that you can see within range and lasts for the duration. It seems completely real, including sounds, smells, and temperature appropriate to the thing depicted. You can't create sufficient heat or cold to cause damage, a sound loud enough to deal thunder damage or deafen a creature, or a smell that might sicken a creature (like a troglodyte's stench).",
    classes: ["Bard", "Warlock", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "phantom-steed": {
    name: "Phantom Steed",
    level: 3,
    school: "Illusion",
    castingTime: "1 minute",
    range: "30 feet",
    components: "V, S",
    duration: "1 hour",
    description: "A Large quasi-real, horselike creature appears on the ground in an unoccupied space of your choice within range. You decide the creature's appearance, but it is equipped with a saddle, bit, and bridle. Any of the equipment created by the spell vanishes in a puff of smoke if it is carried more than 10 feet away from the steed. For the duration, you or a creature you choose can ride the steed. The creature uses the statistics for a riding horse, except it has a speed of 100 feet and can travel 10 miles in an hour, or 13 miles at a fast pace.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "spectral-force": {
    name: "Spectral Force",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a bit of fleece and jade dust worth 25 gp)",
    duration: "Concentration, up to 1 min./level",
    description: "This spell creates a visual illusion that includes sight, sound, smell, and thermal illusions. Unlike silent image, this spell includes audible, olfactory, and thermal elements. The illusion can be up to four 10-ft. cubes, plus one 10-ft. cube per caster level. You can move the image within the range. The image disappears when struck by an opponent unless you cause the illusion to react appropriately.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "illusory-wall": {
    name: "Illusory Wall",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Permanent",
    description: "This spell creates the illusion of a wall, floor, ceiling, or similar surface. It appears absolutely real when viewed, but physical objects can pass through it without difficulty. When the spell is cast, you can specify which creatures can see the wall's illusory nature; they see it as a transparent outline.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "phantasmal-killer": {
    name: "Phantasmal Killer",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You tap into the nightmares of a creature you can see within range and create an illusory manifestation of its deepest fears, visible only to that creature. The target must make a Wisdom saving throw. On a failed save, the target becomes frightened for the duration. At the end of each of the target's turns before the spell ends, the target must succeed on a Wisdom saving throw or take 4d10 psychic damage. On a successful save, the spell ends.",
    classes: ["Wizard"]
  },

  "polymorph": {
    name: "Polymorph",
    level: 4,
    school: "Transmutation",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S, M (a caterpillar cocoon)",
    duration: "Concentration, up to 1 hour",
    description: "This spell transforms a creature that you can see within range into a new form.",
    classes: ["Bard", "Mage"]
  },
  "greater-invisibility": {
    name: "Greater Invisibility",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Concentration, up to 1 minute",
    description: "You or a creature you touch becomes invisible until the spell ends.",
    classes: ["Bard", "Mage", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "inferno-wave": {
    name: "Inferno Wave",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (30-foot cone)",
    components: "V, S, M (a piece of sulfur)",
    duration: "Instantaneous",
    description: "You unleash a wave of intense fire in a 30-foot cone. Each creature in the area must make a Dexterity saving throw. On a failed save, a creature takes 6d6 fire damage and is knocked prone. On a successful save, they take half damage and are not knocked prone.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "orb-of-annihilation": {
    name: "Orb of Annihilation",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S",
    duration: "Instantaneous",
    description: "You project a globe of shimmering force. Make a ranged spell attack. On a hit, the target takes 5d6 force damage and must make a Reflex save or be knocked prone.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "freezing-rain": {
    name: "Freezing Rain",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S, M (a pinch of dust and a few drops of water)",
    duration: "Instantaneous",
    description: "Great magical hailstones pound down in a 20-foot radius, 40-foot high cylinder. Each creature in the area takes 3d6 bludgeoning damage and 2d6 cold damage. The area becomes difficult terrain for 1 round.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "voltaic-detonation": {
    name: "Voltaic Detonation",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (30-foot cone)",
    components: "V, S, F (a small metal cone)",
    duration: "Instantaneous",
    description: "You emit an ear-splitting yell infused with electrical energy. Creatures in the cone are deafened for 2d6 rounds and take 5d6 sonic/electricity damage. A successful Fortitude save negates deafness and halves damage.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },

  // Level 4 Spells - Illusion
  "hallucinatory-terrain": {
    name: "Hallucinatory Terrain",
    level: 4,
    school: "Illusion",
    castingTime: "10 minutes",
    range: "300 feet",
    components: "V, S, M (a stone, a twig, and a bit of green plant)",
    duration: "24 hours",
    description: "You make natural terrain in a 150-foot cube in range look, sound, and smell like some other sort of natural terrain. Thus, open fields or a road can be made to resemble a swamp, hill, crevasse, or some other difficult or impassable terrain. A pond can be made to seem like a grassy meadow, a precipice like a gentle slope, or a rock-strewn gully like a wide and smooth road.",
    classes: ["Bard", "Druid", "Warlock", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "illusory-wall-greater": {
    name: "Illusory Wall, Greater",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Permanent",
    description: "This spell functions like illusory wall, except that it also blocks incorporeal creatures and creatures with tremorsense or blindsight. The wall can be up to 1 foot thick per four caster levels.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "rainbow-pattern": {
    name: "Rainbow Pattern",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V (Bard only), S, M (a piece of phosphor)",
    duration: "Concentration, up to 1 min./level (D)",
    description: "A glowing, rainbow-hued pattern of interweaving colors fascinates creatures within it. Rainbow pattern fascinates a number of HD of creatures equal to your caster level (maximum 20 HD). Creatures with the lowest HD are affected first. Among creatures with equal HD, those who are closest to the spell's point of origin are affected first.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "shadow-conjuration": {
    name: "Shadow Conjuration",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "See text",
    components: "V, S",
    duration: "See text",
    description: "You use material from the Plane of Shadow to shape quasi-real illusions of one or more creatures, objects, or forces. Shadow conjuration can mimic any sorcerer or wizard conjuration (summoning) or conjuration (creation) spell of 3rd level or lower. Shadow conjurations are one-fifth (20%) as strong as the real things, though creatures who believe the shadow conjurations to be real are affected by them at full strength.",
    classes: ["Sorcerer", "Wizard"]
  },
  "phantasmal-terrain": {
    name: "Phantasmal Terrain",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a bit of fleece and jade dust worth 25 gp)",
    duration: "1 hour/level (D)",
    description: "This spell creates the illusion of terrain features within the area of effect. The illusion includes audible, visual, tactile, and olfactory elements. Unlike hallucinatory terrain, this spell affects the minds of creatures rather than creating a visual illusion, making it harder to disbelieve but affecting a smaller area.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "invisibility-mass": {
    name: "Invisibility, Mass",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (an eyelash encased in gum arabic)",
    duration: "1 min./level (D)",
    description: "This spell functions like invisibility, except that the effect moves with the group and is broken when anyone in the group attacks. Individuals in the group cannot see each other. The spell is broken for any individual who moves more than 180 feet from the nearest member of the group.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },

  "teleport": {
    name: "Teleport",
    level: 7,
    school: "Conjuration",
    castingTime: "1 action",
    range: "10 feet",
    components: "V",
    duration: "Instantaneous",
    description: "This spell instantly transports you and up to eight willing creatures of your choice that you can see within range, or a single object that you can see within range, to a destination you select.",
    classes: ["Bard", "Mage"]
  },
  "wish": {
    name: "Wish",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Self",
    components: "V",
    duration: "Instantaneous",
    description: "Wish is the mightiest spell a mortal creature can cast. By simply speaking aloud, you can alter the very foundations of reality in accord with your desires.",
    classes: ["Mage"]
  },
  "time-stop": {
    name: "Time Stop",
    level: 9,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Self",
    components: "V",
    duration: "Instantaneous",
    description: "You briefly stop the flow of time for everyone but yourself. No time passes for other creatures, while you take 1d4 + 1 turns in a row.",
    classes: ["Mage", "Bard", "Cleric", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "meteor-swarm": {
    name: "Meteor Swarm",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "Meteor swarm is a very powerful and spectacular spell that is similar to fireball in many aspects. When you cast it, four 2-foot-diameter spheres spring from your outstretched hand and streak in straight lines to the spots you select.",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "gate": {
    name: "Gate",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, XP; see text",
    duration: "Instantaneous or concentration (up to 1 round/level); see text",
    description: "Casting a gate spell has two effects. First, it creates an interdimensional connection between your plane of existence and a plane you specify.",
    classes: ["Cleric", "Wizard"]
  },
  "imprisonment": {
    name: "Imprisonment",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Until dispelled",
    description: "When you cast imprisonment and touch a creature, it is entombed in a state of suspended animation in a small sphere far beneath the surface of the earth.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },

  // Additional Level 0 Spells
  "dancing-lights": {
    name: "Dancing Lights",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 minute",
    description: "Depending on the version selected, you create up to four lights that resemble lanterns or torches, or up to four glowing spheres of light.",
    classes: ["Bard", "Wizard"]
  },
  "daze": {
    name: "Daze",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a pinch of wool or similar substance)",
    duration: "1 round",
    description: "This enchantment clouds the mind of a humanoid creature with 4 or fewer Hit Dice so that it takes no actions.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "flare": {
    name: "Flare",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "Instantaneous",
    description: "This cantrip creates a burst of light. If you cause the light to burst directly in front of a single creature, that creature is dazzled for 1 minute.",
    classes: ["Bard", "Druid", "Wizard"]
  },
  "guidance": {
    name: "Guidance",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Concentration, up to 1 minute",
    description: "You touch one willing creature. Once before the spell ends, the target can roll a d4 and add the number rolled to one ability check of its choice.",
    classes: ["Cleric", "Druid"]
  },
  "light": {
    name: "Light",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, M (a firefly or phosphorescent moss)",
    duration: "10 min./level",
    description: "This spell causes an object to glow like a torch, shedding bright light in a 20-foot radius.",
    classes: ["Bard", "Cleric", "Druid", "Wizard"]
  },
  "ray-of-frost": {
    name: "Ray of Frost",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "A frigid beam of blue-white light streaks toward a creature within range. Make a ranged spell attack against the target.",
    classes: ["Wizard"]
  },
  "touch-of-fatigue": {
    name: "Touch of Fatigue",
    level: 0,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a drop of sweat)",
    duration: "1 round/level",
    description: "You channel negative energy through your touch, fatiguing the target. You must succeed on a touch attack to affect a creature.",
    classes: ["Wizard"]
  },
  "virtue": {
    name: "Virtue",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "1 min.",
    description: "The subject gains 1 temporary hit point.",
    classes: ["Cleric", "Druid", "Paladin"]
  },

  // Additional Level 1 Spells
  "alarm": {
    name: "Alarm",
    level: 1,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, F/DF (a tiny bell and a piece of very fine silver wire)",
    duration: "2 hours/level",
    description: "Alarm sounds a mental or audible alarm each time a creature of Tiny or larger size enters the warded area or touches it.",
    classes: ["Ranger", "Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "animate-rope": {
    name: "Animate Rope",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 round/level",
    description: "You can animate a nonliving rope-like object. The maximum length assumes a rope with a 1-inch diameter.",
    classes: ["Bard", "Wizard"]
  },
  "burning-hands": {
    name: "Burning Hands",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "15 ft.",
    components: "V, S",
    duration: "Instantaneous",
    description: "A cone of searing flame shoots from your fingertips. Any creature in the area of the flames takes 1d4 points of fire damage per caster level.",
    classes: ["Wizard"]
  },
  "cause-fear": {
    name: "Cause Fear",
    level: 1,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1d4 rounds or 1 round; see text",
    description: "The affected creature becomes frightened. If the subject succeeds on a Will save, it is shaken for 1 round.",
    classes: ["Bard", "Cleric", "Wizard"]
  },
  "chill-touch": {
    name: "Chill Touch",
    level: 1,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "A touch from your hand, which glows with blue energy, disrupts the life force of living creatures.",
    classes: ["Wizard"]
  },
  "comprehend-languages": {
    name: "Comprehend Languages",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M/DF (pinch of soot and salt)",
    duration: "10 min./level",
    description: "You can understand the spoken words of creatures or read otherwise incomprehensible written messages.",
    classes: ["Bard", "Cleric", "Wizard"]
  },
  "cure-light-wounds": {
    name: "Cure Light Wounds",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "When laying your hand upon a living creature, you channel positive energy that cures 1d8 points of damage +1 point per caster level.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger"]
  },
  "detect-secret-doors": {
    name: "Detect Secret Doors",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "60 ft.",
    components: "V, S",
    duration: "Concentration, up to 1 min./level",
    description: "You can detect secret doors, compartments, caches, and so forth.",
    classes: ["Bard", "Wizard"]
  },
  "detect-undead": {
    name: "Detect Undead",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "60 ft.",
    components: "V, S, M/DF (earth from a grave)",
    duration: "Concentration, up to 1 minute/level",
    description: "You can detect the aura that surrounds undead creatures.",
    classes: ["Cleric", "Paladin", "Wizard"]
  },
  "endure-elements": {
    name: "Endure Elements",
    level: 1,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "24 hours",
    description: "A creature protected by endure elements suffers no harm from being in a hot or cold environment.",
    classes: ["Cleric", "Druid", "Paladin", "Ranger", "Wizard", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "enlarge-person": {
    name: "Enlarge Person",
    level: 1,
    school: "Transmutation",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (powdered iron)",
    duration: "1 min./level",
    description: "This spell causes instant growth of a humanoid creature, doubling its height and multiplying its weight by 8.",
    classes: ["Wizard"]
  },
  "erase": {
    name: "Erase",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "Erase removes writings of either magical or mundane nature from a scroll or from one or two pages of paper, parchment, or similar surfaces.",
    classes: ["Bard", "Wizard"]
  },

  "magic-weapon": {
    name: "Magic Weapon",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "1 min./level",
    description: "Magic weapon gives a weapon a +1 enhancement bonus on attack and damage rolls.",
    classes: ["Cleric", "Paladin", "Wizard"]
  },
  "mount": {
    name: "Mount",
    level: 1,
    school: "Conjuration",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a bit of horse hair)",
    duration: "2 hours/level",
    description: "You summon a light horse or a pony to serve you as a mount.",
    classes: ["Wizard"]
  },
  "obscuring-mist": {
    name: "Obscuring Mist",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "20 ft.",
    components: "V, S",
    duration: "1 min./level",
    description: "A misty vapor arises around you. It is stationary once created. The vapor obscures all sight, including darkvision, beyond 5 feet.",
    classes: ["Cleric", "Druid", "Wizard"]
  },
  "reduce-person": {
    name: "Reduce Person",
    level: 1,
    school: "Transmutation",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a pinch of powdered iron)",
    duration: "1 min./level",
    description: "This spell causes instant diminution of a humanoid creature, halving its height, length, and width and dividing its weight by 8.",
    classes: ["Wizard"]
  },
  "shield-of-faith": {
    name: "Shield of Faith",
    level: 1,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a small parchment with a bit of holy text written on it)",
    duration: "1 min./level",
    description: "This spell creates a shimmering, magical field around the touched creature that averts attacks. The spell grants the subject a +2 deflection bonus to AC.",
    classes: ["Cleric", "Paladin", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "shocking-grasp": {
    name: "Shocking Grasp",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "Your successful melee touch attack deals 1d6 points of electricity damage per caster level (maximum 5d6).",
    classes: ["Wizard"]
  },
  "sleep": {
    name: "Sleep",
    level: 1,
    school: "Enchantment",
    castingTime: "1 round",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (fine sand, rose petals, or a live cricket)",
    duration: "1 min./level",
    description: "A sleep spell causes a magical slumber to come upon 4d4 Hit Dice of creatures.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief", "true-strike", "True Strike", "Divination", "1 action", "Personal", "V, F (a small wooden replica of an archery target)", "See text", "You gain temporary, intuitive insight into the immediate future during your next attack."]
  },

  // Additional Level 2 Spells
  "bulls-strength": {
    name: "Bull's Strength",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (a few hairs, or a pinch of dung, from a bull)",
    duration: "1 min./level",
    description: "The subject becomes stronger. The spell grants a +4 enhancement bonus to Strength.",
    classes: ["Cleric", "Druid", "Paladin", "Wizard"]
  },
  "bears-endurance": {
    name: "Bear's Endurance",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (a few hairs, or a pinch of dung, from a bear)",
    duration: "1 min./level",
    description: "The affected creature gains greater vitality and stamina. The spell grants a +4 enhancement bonus to Constitution.",
    classes: ["Cleric", "Druid", "Ranger", "Wizard"]
  },
  "eagles-splendor": {
    name: "Eagle's Splendor",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (feathers or droppings from an eagle)",
    duration: "1 min./level",
    description: "The transmuted creature becomes more poised, articulate, and personally forceful. The spell grants a +4 enhancement bonus to Charisma.",
    classes: ["Bard", "Cleric", "Paladin", "Wizard"]
  },
  "foxs-cunning": {
    name: "Fox's Cunning",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (hairs or dung from a fox)",
    duration: "1 min./level",
    description: "The target becomes smarter. The spell grants a +4 enhancement bonus to Intelligence.",
    classes: ["Bard", "Wizard"]
  },
  "owls-wisdom": {
    name: "Owl's Wisdom",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (feathers or droppings from an owl)",
    duration: "1 min./level",
    description: "The transmuted creature becomes wiser. The spell grants a +4 enhancement bonus to Wisdom.",
    classes: ["Cleric", "Druid", "Paladin", "Ranger", "Wizard"]
  },

  "knock": {
    name: "Knock",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V",
    duration: "Instantaneous; see text",
    description: "The knock spell opens stuck, barred, locked, held, or arcane locked doors.",
    classes: ["Wizard"]
  },
  "levitate": {
    name: "Levitate",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal or close (25 ft. + 5 ft./2 levels)",
    components: "V, S, F (a leather loop or golden wire bent into a cup shape)",
    duration: "1 min./level",
    description: "Levitate allows you to move yourself, another creature, or an object up and down as you wish.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "mirror-image": {
    name: "Mirror Image",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 min./level",
    description: "Several illusory duplicates of you pop into being, making it difficult for enemies to know which target to attack.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "misdirection": {
    name: "Misdirection",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 hour/level",
    description: "By means of this spell, you misdirect the information from divination spells that reveal auras.",
    classes: ["Bard", "Wizard"]
  },

  // Additional Level 3 Spells
  "blink": {
    name: "Blink",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 round/level",
    description: "You 'blink' back and forth between the Material Plane and the Ethereal Plane.",
    classes: ["Bard", "Wizard"]
  },
  "clairaudience-clairvoyance": {
    name: "Clairaudience/Clairvoyance",
    level: 3,
    school: "Divination",
    castingTime: "10 minutes",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F/DF (a small horn or a glass eye)",
    duration: "1 min./level",
    description: "Clairaudience/clairvoyance creates an invisible magical sensor at a specific location.",
    classes: ["Bard", "Wizard"]
  },
  "displacement": {
    name: "Displacement",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "Touch",
    components: "V, M (a small strip of leather twisted into a loop)",
    duration: "1 round/level",
    description: "The subject of this spell appears to be about 2 feet away from its true location.",
    classes: ["Bard", "Wizard"]
  },
  "gaseous-form": {
    name: "Gaseous Form",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "S, M/DF (a bit of gauze and a wisp of smoke)",
    duration: "2 min./level",
    description: "The subject and all its gear become insubstantial, misty, and translucent.",
    classes: ["Bard", "Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },

  "lightning-bolt": {
    name: "Lightning Bolt",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 ft.",
    components: "V, S, M (a bit of fur and a rod of amber, crystal, or glass)",
    duration: "Instantaneous",
    description: "You release a powerful stroke of electrical energy that deals 1d6 points of electricity damage per caster level.",
    classes: ["Wizard"]
  },
  "major-image": {
    name: "Major Image",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F (a bit of fleece)",
    duration: "Concentration + 3 rounds",
    description: "This spell functions like silent image, except that sound, smell, and thermal illusions are included in the spell effect.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief", "protection-from-energy", "Protection from Energy", "Abjuration", "1 action", "Touch", "V, S, DF", "10 min./level or until discharged", "Protection from energy grants temporary immunity to the type of energy you specify when you cast it.", "Cleric", "Druid", "Paladin", "Ranger"]
  },
  "rage": {
    name: "Rage",
    level: 3,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Concentration + 1 round/level",
    description: "Each affected creature gains a +2 morale bonus to Strength and Constitution, a +1 morale bonus on Will saves, and a -2 penalty to AC.",
    classes: ["Bard", "Wizard"]
  },
  "suggestion-3": {
    name: "Suggestion",
    level: 3,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, M (a snake's tongue and a honeycomb)",
    duration: "1 hour/level or until completed",
    description: "This spell functions like suggestion, except that it can affect more creatures.",
    classes: ["Bard", "Wizard"]
  },

  // Additional Level 4 Spells
  "charm-monster": {
    name: "Charm Monster",
    level: 4,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 day/level",
    description: "This charm makes a creature regard you as its trusted friend and ally.",
    classes: ["Bard", "Wizard"]
  },
  "confusion": {
    name: "Confusion",
    level: 4,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M/DF (three nut shells)",
    duration: "1 round/level",
    description: "This spell causes the targets to become confused, making them unable to independently determine what they will do.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "dimension-door": {
    name: "Dimension Door",
    level: 4,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V",
    duration: "Instantaneous",
    description: "You instantly transfer yourself from your current location to any other spot within range.",
    classes: ["Bard", "Wizard"]
  },
  "greater-invisibility": {
    name: "Greater Invisibility",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "Personal or touch",
    components: "V, S",
    duration: "1 round/level",
    description: "This spell functions like invisibility, except that it doesn't end if the subject attacks.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief", "ice-storm", "Ice Storm", "Evocation", "1 action", "Long (400 ft. + 40 ft./level)", "V, S, M/DF (a pinch of dust and a few drops of water)", "1 full round", "Great magical hailstones pound down for 1 full round, dealing 3d6 points of bludgeoning damage and 2d6 points of cold damage.", "Druid"]
  },

  "stoneskin": {
    name: "Stoneskin",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (granite and 250 gp worth of diamond dust)",
    duration: "10 min./level or until discharged",
    description: "The warded creature gains resistance to blows, cuts, stabs, and slashes.",
    classes: ["Druid", "Wizard", "Cleric", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "wall-of-fire": {
    name: "Wall of Fire",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M/DF (a small piece of phosphorus)",
    duration: "Concentration + 1 round/level",
    description: "An immobile, blazing curtain of shimmering violet fire springs into existence.",
    classes: ["Druid", "Wizard"]
  },

  // Additional Level 5 Spells
  "cone-of-cold": {
    name: "Cone of Cold",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "60 ft.",
    components: "V, S, M (a crystal or glass cone)",
    duration: "Instantaneous",
    description: "Cone of cold creates an area of extreme cold, originating at your hand and extending outward in a cone.",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "flame-typhoon": {
    name: "Flame Typhoon",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S, M (a piece of charcoal)",
    duration: "Instantaneous",
    description: "You create a swirling vortex of fire in a 20-foot radius, 40-foot high cylinder. Each creature in the area takes 6d6 fire damage and must make a Strength saving throw or be knocked prone. The area remains burning for 1 round, dealing 2d6 fire damage to creatures that start their turn there.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "frozen-tomb": {
    name: "Frozen Tomb",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S, M (a shard of ice)",
    duration: "Concentration, up to 1 minute",
    description: "You encase a creature in a tomb of ice. The target must make a Constitution saving throw. On a failed save, they take 4d8 cold damage and are restrained. On subsequent turns, they can repeat the save to break free, taking 2d8 cold damage on each failed attempt.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "meteor-spear": {
    name: "Meteor Spear",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "150 feet",
    components: "V, S, M (a small meteorite)",
    duration: "Instantaneous",
    description: "You hurl a blazing spear of cosmic energy. Make a ranged spell attack. On a hit, the target takes 6d6 fire damage plus 3d6 force damage. All creatures within 10 feet of the target must make a Dexterity saving throw or take 3d6 fire damage.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "arc-surge": {
    name: "Arc Surge",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (60-foot line)",
    components: "V, S, M (a copper wire)",
    duration: "Instantaneous",
    description: "You unleash a powerful bolt of lightning in a 60-foot line that is 5 feet wide. Each creature in the line must make a Dexterity saving throw, taking 8d6 lightning damage on a failed save, or half as much on a successful one.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "dominate-person": {
    name: "Dominate Person",
    level: 5,
    school: "Enchantment",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 day/level",
    description: "You can control the actions of any humanoid creature through a telepathic link.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "feeblemind": {
    name: "Feeblemind",
    level: 5,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a handful of clay, crystal, glass, or mineral spheres)",
    duration: "Instantaneous",
    description: "Target creature's Intelligence and Charisma each drop to 1.",
    classes: ["Wizard"]
  },
  "hold-monster": {
    name: "Hold Monster",
    level: 5,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, F/DF (one hard metal bar or rod)",
    duration: "1 round/level",
    description: "This spell functions like hold person, except that it affects any living creature.",
    classes: ["Bard", "Wizard"]
  },

  "wall-of-force": {
    name: "Wall of Force",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (powdered quartz)",
    duration: "1 round/level",
    description: "A wall of force spell creates an invisible wall of force.",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },

  // Level 5 Spells - Illusion
  "false-vision": {
    name: "False Vision",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (the ground dust of a piece of jade worth at least 250 gp, which the spell consumes)",
    duration: "24 hours",
    description: "Any divination (scrying) spell used to view anything within the area of this spell instead receives a false image (as the major image spell), sounds, and other sensory information that you determine. As long as the duration lasts, you can concentrate to change the image as a standard action.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "mirage-arcana": {
    name: "Mirage Arcana",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Concentration, up to 10 minutes",
    description: "This spell functions like hallucinatory terrain, except that it enables you to make any area appear to be something other than it is. The illusion includes audible, visual, tactile, and olfactory elements. Unlike hallucinatory terrain, the spell can alter the appearance of structures (or add them where none are present).",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "nightmare": {
    name: "Nightmare",
    level: 5,
    school: "Illusion",
    castingTime: "10 minutes",
    range: "Unlimited",
    components: "V, S",
    duration: "Instantaneous",
    description: "You send a hideous and unsettling phantasmagorical vision to a specific creature that you name or otherwise specifically designate. The nightmare prevents restful sleep and causes 1d10 points of damage. The nightmare leaves the subject fatigued and unable to regain arcane spells for the next 24 hours.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "persistent-image": {
    name: "Persistent Image",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F (a bit of fleece)",
    duration: "1 min./level (D)",
    description: "This spell functions like silent image, except that the figment includes visual, auditory, olfactory, and thermal elements, and the spell is permanent. The figment performs the actions you designate when you cast the spell; it cannot be changed thereafter.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "seeming": {
    name: "Seeming",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "12 hours (D)",
    description: "This spell functions like disguise self, except that you can change the appearance of other creatures as well. Affected creatures resume their normal appearances if slain. Unwilling targets can negate the spell's effect on them by making Willpower saves or with spell resistance.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "shadow-evocation": {
    name: "Shadow Evocation",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "See text",
    components: "V, S",
    duration: "See text",
    description: "You tap energy from the Plane of Shadow to cast a quasi-real evocation spell of 4th level or lower. Spells that deal damage have normal effects unless the affected creature succeeds on a Will save. Each disbelieving creature takes only one-fifth (20%) damage from the attack.",
    classes: ["Sorcerer", "Wizard"]
  },
  "phantasmal-web": {
    name: "Phantasmal Web",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a bit of spider web)",
    duration: "1 min./level (D)",
    description: "You create an illusion of a massive web that appears to entangle creatures in a 20-foot-radius spread. Creatures in the area must make a Will save or believe they are entangled. Those who believe are effectively entangled and take a -2 penalty to attack rolls and a -4 penalty to Dexterity.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "mislead": {
    name: "Mislead",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "S",
    duration: "1 round/level (D)",
    description: "You become invisible (as greater invisibility, a 4th-level spell), and at the same time, an illusory double of you (as major image, a 3rd-level spell) appears. You are then free to go elsewhere while your double moves away.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },

  // Additional Level 6 Spells
  "chain-lightning": {
    name: "Chain Lightning",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F (a bit of fur; a piece of amber, glass, or a crystal rod; plus one silver pin for each of your caster levels)",
    duration: "Instantaneous",
    description: "This spell creates an electrical discharge that begins as a single stroke commencing from your fingertips.",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "solar-flare": {
    name: "Solar Flare",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S, M (a piece of amber)",
    duration: "Instantaneous",
    description: "You create a brilliant burst of solar energy in a 30-foot radius sphere. Each creature in the area takes 8d6 radiant damage and must make a Constitution saving throw or be blinded for 1 minute. Undead creatures take an additional 2d6 damage.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "absolute-zero": {
    name: "Absolute Zero",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "60 feet",
    components: "V, S, M (a diamond worth at least 500 gp)",
    duration: "Instantaneous",
    description: "You create a zone of absolute cold in a 20-foot radius sphere. Each creature in the area takes 10d6 cold damage and their speed is reduced to 0 until the end of their next turn. A successful Constitution saving throw halves the damage and negates the speed reduction.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "arcane-mortar": {
    name: "Arcane Mortar",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "300 feet",
    components: "V, S, M (a small crystal sphere)",
    duration: "Instantaneous",
    description: "You launch a sphere of pure magical energy that explodes on impact. Choose a point within range. Each creature within 20 feet of that point takes 8d6 force damage and must make a Strength saving throw or be knocked prone.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "sonic-collapse": {
    name: "Sonic Collapse",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (60-foot cone)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You emit a devastating sonic wave. Each creature in the cone takes 7d8 thunder damage and must make a Constitution saving throw. On a failed save, they are deafened for 1 minute and stunned until the end of their next turn.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "disintegrate": {
    name: "Disintegrate",
    level: 6,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M/DF (a lodestone and a pinch of dust)",
    duration: "Instantaneous",
    description: "A thin, green ray springs from your pointing finger.",
    classes: ["Wizard"]
  },
  "flesh-to-stone": {
    name: "Flesh to Stone",
    level: 6,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (lime, water, and earth)",
    duration: "Instantaneous",
    description: "The subject, along with all its carried gear, turns into a mindless, inert statue.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "greater-dispel-magic": {
    name: "Greater Dispel Magic",
    level: 6,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like dispel magic, except that the maximum caster level on your dispel check is +20 instead of +10.",
    classes: ["Bard", "Cleric", "Druid", "Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior", "Monk"]
  },
  "mass-suggestion": {
    name: "Mass Suggestion",
    level: 6,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, M (a snake's tongue and a honeycomb)",
    duration: "1 hour/level or until completed",
    description: "This spell functions like suggestion, except that it can affect more creatures.",
    classes: ["Bard", "Wizard"]
  },
  "true-seeing": {
    name: "True Seeing",
    level: 6,
    school: "Divination",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (an ointment for the eyes that costs 250 gp)",
    duration: "1 min./level",
    description: "You confer on the subject the ability to see all things as they actually are.",
    classes: ["Cleric", "Druid", "Wizard", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },

  // Level 6 Spells - Illusion
  "mislead-greater": {
    name: "Mislead, Greater",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "S",
    duration: "1 round/level (D)",
    description: "This spell functions like mislead, except that you can create multiple illusory doubles (one per three caster levels) and can switch your consciousness between them as a free action. Each double can act independently.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "permanent-image": {
    name: "Permanent Image",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F (a bit of fleece plus powdered jade worth 100 gp)",
    duration: "Permanent (D)",
    description: "This spell functions like persistent image, except that the figment is permanent. It performs the actions you designate when you cast the spell, following a simple program you set. The figment can be dispelled but otherwise lasts until destroyed.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "programmed-image": {
    name: "Programmed Image",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a bit of fleece and jade dust worth 25 gp)",
    duration: "Permanent until triggered, then 1 round/level",
    description: "This spell functions like persistent image, except that this spell's figment activates when a specific condition occurs. The figment includes visual, auditory, olfactory, and thermal elements, including intelligible speech.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "shadow-walk": {
    name: "Shadow Walk",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 hour/level (D)",
    description: "To use the shadow walk spell, you must be in an area of shadowy illumination. You and any creatures you touch are then transported along a coiling path of shadowstuff to the edge of the Material Plane where it borders the Plane of Shadow.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "veil": {
    name: "Veil",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Concentration, up to 1 hour",
    description: "You instantly change the appearance of the subjects and then maintain that appearance for the spell's duration. You can make the subjects appear to be anything you wish. The subjects look, feel, and smell just like the creatures the spell makes them resemble.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "shadow-conjuration-greater": {
    name: "Shadow Conjuration, Greater",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "See text",
    components: "V, S",
    duration: "See text",
    description: "This spell functions like shadow conjuration, except that it can duplicate any sorcerer or wizard conjuration spell of 5th level or lower. The illusory conjurations created deal three-fifths (60%) damage to nonbelievers.",
    classes: ["Sorcerer", "Wizard"]
  },
  "phantasmal-disorientation": {
    name: "Phantasmal Disorientation",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a spinning top)",
    duration: "1 round/level",
    description: "You create a powerful illusion that disorients creatures in a 30-foot radius. Affected creatures become confused and have their movement speed halved. They must make a Will save each round or act randomly as if affected by a confusion spell.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "project-image": {
    name: "Project Image",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a small replica of you worth 5 gp)",
    duration: "1 round/level (D)",
    description: "You tap energy from the Plane of Shadow to create a quasi-real, illusory version of yourself. The projected image looks, sounds, and smells like you but is intangible. The projected image mimics your actions (including speech) unless you direct it to act differently.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },

  // Additional Level 7 Spells
  "finger-of-death": {
    name: "Finger of Death",
    level: 7,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You can slay any one living creature within range.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "lightning-grave": {
    name: "Lightning Grave",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S, M (a rod of copper and zinc)",
    duration: "Concentration, up to 1 minute",
    description: "You create a 30-foot radius area of crackling electrical energy. When a creature enters the area or starts its turn there, it takes 6d6 lightning damage. Creatures that die in this area rise as lightning-charged zombies under your control.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "pyroclasm": {
    name: "Pyroclasm",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "150 feet",
    components: "V, S, M (a piece of volcanic rock)",
    duration: "Instantaneous",
    description: "You cause the ground to erupt in a 40-foot radius sphere of molten rock and fire. Each creature in the area takes 12d6 fire damage and must make a Dexterity saving throw or be knocked prone. The area becomes difficult terrain for 10 minutes.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "frost-reaver": {
    name: "Frost Reaver",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "Self (120-foot line)",
    components: "V, S, M (a shard of eternal ice)",
    duration: "Instantaneous",
    description: "You unleash a devastating beam of absolute cold in a 120-foot line that is 10 feet wide. Each creature in the line takes 10d8 cold damage and must make a Constitution saving throw or be paralyzed for 1 minute.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "arcbolt-singularity": {
    name: "Arcbolt Singularity",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "120 feet",
    components: "V, S, M (a sphere of magnetized metal)",
    duration: "Concentration, up to 1 minute",
    description: "You create a point of intense electrical energy that pulls creatures toward it. Each creature within 60 feet must make a Strength saving throw or be pulled 30 feet toward the center and take 8d6 lightning damage. The effect repeats at the start of each of your turns.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior"]
  },
  "plane-shift": {
    name: "Plane Shift",
    level: 7,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, F (a forked, metal rod attuned to the plane of travel)",
    duration: "Instantaneous",
    description: "You move yourself or some other creature to another plane of existence or alternate dimension.",
    classes: ["Cleric", "Wizard"]
  },
  "power-word-blind": {
    name: "Power Word Blind",
    level: 7,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "See text",
    description: "You utter a single word of power that causes one creature of your choice to become blinded.",
    classes: ["Wizard"]
  },
  "reverse-gravity": {
    name: "Reverse Gravity",
    level: 7,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M/DF (a lodestone and iron filings)",
    duration: "1 round/level",
    description: "This spell reverses gravity in an area, causing all unattached objects and creatures within that area to fall upward.",
    classes: ["Druid", "Wizard"]
  },
  "spell-turning": {
    name: "Spell Turning",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M/DF (a small silver mirror)",
    duration: "Until expended or 10 min./level",
    description: "Spells and spell-like effects targeted on you are turned back upon the original caster.",
    classes: ["Bard", "Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },

  // Level 7 Spells - Illusion
  "mass-invisibility": {
    name: "Mass Invisibility",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (an eyelash encased in gum arabic)",
    duration: "1 min./level (D)",
    description: "This spell functions like greater invisibility, except that the effect moves with the group and is broken when anyone in the group attacks. The spell can affect one creature per caster level.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "project-image-greater": {
    name: "Project Image, Greater",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a small replica of you worth 50 gp)",
    duration: "1 round/level (D)",
    description: "This spell functions like project image, except that the projected image can cast spells of 3rd level or lower that you know, using your spell slots. The image has all your abilities but only half your hit points.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "shadow-conjuration-supreme": {
    name: "Shadow Conjuration, Supreme",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "See text",
    components: "V, S",
    duration: "See text",
    description: "This spell functions like shadow conjuration, except that it can duplicate any sorcerer or wizard conjuration spell of 6th level or lower. The illusory conjurations created deal four-fifths (80%) damage to nonbelievers.",
    classes: ["Sorcerer", "Wizard"]
  },
  "shadow-evocation-greater": {
    name: "Shadow Evocation, Greater",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "See text",
    components: "V, S",
    duration: "See text",
    description: "This spell functions like shadow evocation, except that it enables you to create quasi-real, illusory versions of sorcerer or wizard evocation spells of 6th level or lower. The damage dealt is three-fifths (60%) of normal.",
    classes: ["Sorcerer", "Wizard"]
  },
  "simulacrum": {
    name: "Simulacrum",
    level: 7,
    school: "Illusion",
    castingTime: "12 hours",
    range: "0 ft.",
    components: "V, S, M (ice or snow plus the spell component pouch of the creature to be duplicated)",
    duration: "Instantaneous",
    description: "Simulacrum creates an illusory duplicate of any creature. The duplicate creature is partially real and formed from ice or snow. It appears to be the same as the original, but it has only half of the real creature's levels or Hit Dice.",
    classes: ["Sorcerer", "Wizard"]
  },
  "weird": {
    name: "Weird",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like phantasmal killer, except that it can affect more than one creature. Only the affected creatures see the phantasmal creatures attacking them, though you see the attackers as shadowy shapes.",
    classes: ["Sorcerer", "Wizard"]
  },
  "phantasmal-revenge": {
    name: "Phantasmal Revenge",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a drop of the target's blood)",
    duration: "Instantaneous",
    description: "You create a powerful phantasm that appears as the target's greatest fear or most hated enemy. The target must make a Will save or take 1d4 points of Wisdom damage and be stunned for 1d4 rounds as the phantasm attacks them with their own memories.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "illusory-double": {
    name: "Illusory Double",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a small mirror)",
    duration: "1 hour/level (D)",
    description: "You create a perfect illusory duplicate of yourself that can act independently. The double has all your memories and abilities but cannot cast spells above 3rd level. It can make decisions and act as you would, making it nearly impossible to distinguish from the real you.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },

  // Additional Level 8 Spells
  "maze": {
    name: "Maze",
    level: 8,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "See text",
    description: "You banish the subject into an extradimensional labyrinth of force planes.",
    classes: ["Wizard"]
  },
  "sunburst": {
    name: "Sunburst",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M/DF (fire source)",
    duration: "Instantaneous",
    description: "Sunburst causes a globe of searing radiance to explode silently from a point you select. All creatures in the globe are blinded and take 6d6 points of damage. A creature to which sunlight is harmful or unnatural takes double damage.",
    classes: ["Mage"]
  },
  "polar-ray": {
    name: "Polar Ray",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, F (a white or clear prism)",
    duration: "Instantaneous",
    description: "A blue-white ray of freezing air and ice springs from your hand. You must succeed on a ranged touch attack with the ray to deal damage to a target. The ray deals 1d6 points of cold damage per caster level (maximum 25d6).",
    classes: ["Mage"]
  },
  "incendiary-cloud": {
    name: "Incendiary Cloud",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 round/level (D)",
    description: "An incendiary cloud spell creates a cloud of roiling smoke shot through with white-hot embers. The smoke obscures all sight as a fog cloud does. In addition, the white-hot embers within the cloud deal 4d6 points of fire damage to everything within the cloud on your turn each round.",
    classes: ["Mage"]
  },
  "horrid-wilting": {
    name: "Horrid Wilting",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M/DF (a bit of sponge)",
    duration: "Instantaneous",
    description: "This spell evaporates moisture from the body of each subject living creature, dealing 1d6 points of damage per caster level (maximum 20d6). This spell is especially devastating to water elementals and plant creatures.",
    classes: ["Mage", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "mind-blank": {
    name: "Mind Blank",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "24 hours",
    description: "The subject is protected from all devices and spells that detect, influence, or read emotions or thoughts.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "power-word-stun": {
    name: "Power Word Stun",
    level: 8,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "See text",
    description: "You utter a single word of power that instantly causes one creature of your choice to become stunned.",
    classes: ["Wizard"]
  },
  "temporal-stasis": {
    name: "Temporal Stasis",
    level: 8,
    school: "Transmutation",
    castingTime: "10 minutes",
    range: "Touch",
    components: "V, S, M (powdered diamond, emerald, ruby, and sapphire, each worth at least 100 gp)",
    duration: "Permanent until triggered",
    description: "You must succeed on a melee touch attack. You place the subject into a state of suspended animation.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },

  // Level 8 Spells - Illusion
  "scintillating-pattern": {
    name: "Scintillating Pattern",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Concentration, up to 2 rounds + 1 round/level",
    description: "A twisting pattern of coruscating colors weaves through the air, affecting creatures within it. The pattern appears in the air in any sequence you desire. The pattern affects a maximum number of Hit Dice of creatures equal to your caster level (maximum 20 Hit Dice).",
    classes: ["Sorcerer", "Wizard"]
  },
  "screen": {
    name: "Screen",
    level: 8,
    school: "Illusion",
    castingTime: "10 minutes",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "24 hours",
    description: "This spell creates a powerful protection from scrying and observation. The spell wards a 30-foot cube per caster level. Any attempt to view anything within the warded area instead receives false information (as the false vision spell).",
    classes: ["Sorcerer", "Wizard"]
  },
  "shadow-evocation-supreme": {
    name: "Shadow Evocation, Supreme",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "See text",
    components: "V, S",
    duration: "See text",
    description: "This spell functions like shadow evocation, except that it enables you to create quasi-real, illusory versions of sorcerer or wizard evocation spells of 7th level or lower. The damage dealt is four-fifths (80%) of normal.",
    classes: ["Sorcerer", "Wizard"]
  },
  "simulacrum-greater": {
    name: "Simulacrum, Greater",
    level: 8,
    school: "Illusion",
    castingTime: "24 hours",
    range: "0 ft.",
    components: "V, S, M (ice or snow plus the spell component pouch of the creature to be duplicated, plus 1,000 gp worth of materials)",
    duration: "Instantaneous",
    description: "This spell functions like simulacrum, except that the duplicate has three-quarters of the original's levels or Hit Dice and can use spells and abilities up to 6th level.",
    classes: ["Sorcerer", "Wizard"]
  },
  "superior-invisibility": {
    name: "Superior Invisibility",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "Personal or touch",
    components: "V, S, M (an eyelash encased in gum arabic)",
    duration: "1 min./level (D)",
    description: "This spell functions like greater invisibility, except that the subject remains invisible even when attacking and cannot be detected by any divination magic short of a wish or miracle spell.",
    classes: ["Sorcerer", "Wizard"]
  },
  "weird-greater": {
    name: "Weird, Greater",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like weird, except that it affects all creatures in a 30-foot radius and deals 2d4 points of Wisdom damage to those who fail their save. Creatures reduced to 0 Wisdom fall into a catatonic state.",
    classes: ["Sorcerer", "Wizard"]
  },
  "phantasmal-hell": {
    name: "Phantasmal Hell",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a vial of unholy water)",
    duration: "1 round/level",
    description: "You create a terrifying illusion of a hellish landscape in a 40-foot radius. All creatures in the area must make Will saves each round or be paralyzed with fear. The illusion deals 2d6 points of damage per round to all creatures within as they experience the torments of the damned.",
    classes: ["Sorcerer", "Wizard"]
  },
  "illusory-reality": {
    name: "Illusory Reality",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a piece of the Ethereal Plane)",
    duration: "1 hour/level",
    description: "You make one aspect of an illusion spell you cast become real. The chosen element becomes a permanent part of reality until the spell ends. For example, illusory fire becomes real fire, an illusory bridge becomes a real bridge.",
    classes: ["Sorcerer", "Wizard"]
  },

  // Additional Level 9 Spells
  "astral-projection": {
    name: "Astral Projection",
    level: 9,
    school: "Necromancy",
    castingTime: "30 minutes",
    range: "Touch",
    components: "V, S, M (jacinth worth at least 1,000 gp, plus a silver bar worth at least 5 gp for each person to be affected)",
    duration: "See text",
    description: "By freeing your spirit from your physical body, this spell allows you to project an astral body onto another plane altogether.",
    classes: ["Cleric", "Wizard"]
  },
  "meteor-swarm": {
    name: "Meteor Swarm",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "Meteor swarm is a very powerful and spectacular spell that is similar to fireball in many aspects. When you cast it, four 2-foot-diameter spheres spring from your outstretched hand and streak in straight lines to the spots you select.",
    classes: ["Mage", "Crimson Agent", "Dragoon", "Warrior", "energy-drain", "Energy Drain", "Evocation", "1 action", "Close (25 ft. + 5 ft./2 levels)", "V, S", "Instantaneous", "You point your finger and utter the incantation, releasing a black ray of crackling negative energy that suppresses the life force of any living creature it strikes."]
  },
  "wail-of-the-banshee": {
    name: "Wail of the Banshee",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "Instantaneous",
    description: "You emit a terrible scream that kills creatures that hear it (except for yourself). Creatures closest to the point of origin are affected first.",
    classes: ["Mage"]
  },
  "implosion": {
    name: "Implosion",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Concentration (up to 1 round per 2 levels)",
    description: "You create a destructive resonance in a corporeal creature's body. For each round you concentrate, you can cause one creature to collapse in on itself, killing it.",
    classes: ["Mage"]
  },
  "gate": {
    name: "Gate",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, XP; see text",
    duration: "Instantaneous or concentration (up to 1 round/level); see text",
    description: "Casting a gate spell has two effects. First, it creates an interdimensional connection between your plane of existence and a plane you specify.",
    classes: ["Cleric", "Wizard"]
  },
  "imprisonment": {
    name: "Imprisonment",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "When you cast imprisonment and touch a creature, it is entombed in a state of suspended animation in a small sphere far beneath the surface of the earth.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "power-word-kill": {
    name: "Power Word Kill",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "Instantaneous",
    description: "You utter a single word of power that instantly kills one creature of your choice.",
    classes: ["Wizard"]
  },



  // Level 9 Spells - Illusion
  "shades": {
    name: "Shades",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See text",
    components: "V, S",
    duration: "See text",
    description: "This spell functions like shadow conjuration, except that it mimics conjuration spells of 8th level or lower. The illusory conjurations created deal four-fifths (80%) damage to nonbelievers, and nondamaging effects are 80% likely to work against nonbelievers.",
    classes: ["Sorcerer", "Wizard"]
  },
  "weird-supreme": {
    name: "Weird, Supreme",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like weird, except that it affects all creatures in a 60-foot radius and deals 3d4 points of Wisdom damage. Creatures that die from this spell have their souls trapped in a nightmare realm for 24 hours.",
    classes: ["Sorcerer", "Wizard"]
  },
  "programmed-amnesia": {
    name: "Programmed Amnesia",
    level: 9,
    school: "Illusion",
    castingTime: "1 hour",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a piece of parchment with the target's name)",
    duration: "Permanent",
    description: "You selectively erase memories from the target's mind. You can remove specific memories, skills, or even entire periods of the target's life. The target must make a Will save or lose the designated memories permanently.",
    classes: ["Bard", "Sorcerer", "Wizard"]
  },
  "reality-revision": {
    name: "Reality Revision",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See text",
    components: "V, S, M (a diamond worth 25,000 gp)",
    duration: "Instantaneous",
    description: "You alter reality itself within a limited scope. This spell can duplicate the effects of any spell of 8th level or lower, but the changes are made through illusion that becomes real. The spell can affect an area up to 1 mile in radius.",
    classes: ["Sorcerer", "Wizard"]
  },
  "illusory-trap": {
    name: "Illusory Trap",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a miniature maze made of precious metals worth 5,000 gp)",
    duration: "Permanent until triggered",
    description: "You create an elaborate illusory trap that activates when specific conditions are met. The trap can mimic any spell effect of 8th level or lower and affects all creatures in a 100-foot radius when triggered.",
    classes: ["Sorcerer", "Wizard"]
  },
  "shadow-landscape": {
    name: "Shadow Landscape",
    level: 9,
    school: "Illusion",
    castingTime: "1 hour",
    range: "1 mile",
    components: "V, S, M (shadow essence worth 10,000 gp)",
    duration: "Permanent",
    description: "You transform a 1-mile radius area into a landscape of your choosing, drawing power from the Plane of Shadow. The transformation is both illusory and partially real, creating a demiplane-like effect that persists indefinitely.",
    classes: ["Sorcerer", "Wizard"]
  },
  "phantasmal-armageddon": {
    name: "Phantasmal Armageddon",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "1 mile",
    components: "V, S, M (a vial containing the essence of a destroyed city)",
    duration: "1 hour",
    description: "You create a massive illusion of an apocalyptic event across a 1-mile radius. All creatures in the area experience their worst fears of destruction and must make Will saves each round or be paralyzed with terror. The illusion deals 4d6 damage per round to all within.",
    classes: ["Sorcerer", "Wizard"]
  },
  "true-illusion": {
    name: "True Illusion",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "Unlimited",
    components: "V, S, M (a perfect crystal worth 50,000 gp)",
    duration: "Permanent",
    description: "You create an illusion so perfect that it becomes indistinguishable from reality. The illusion can affect any number of senses and cannot be disbelieved through normal means. Only divine intervention or reality-altering magic can dispel this illusion.",
    classes: ["Sorcerer", "Wizard"]
  },

  // Additional Cleric Spells
  "bless": {
    name: "Bless",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "50 ft.",
    components: "V, S, M (a sprinkling of holy water)",
    duration: "1 min./level",
    description: "Bless fills your allies with courage. Each ally gains a +1 morale bonus on attack rolls and on saving throws against fear effects.",
    classes: ["Cleric", "Paladin"]
  },
  "command": {
    name: "Command",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "1 round",
    description: "You give the subject a single command, which it obeys to the best of its ability at its earliest opportunity.",
    classes: ["Cleric"]
  },
  "sanctuary": {
    name: "Sanctuary",
    level: 1,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "1 round/level",
    description: "Any opponent attempting to strike or otherwise directly attack the warded creature must attempt a Will save.",
    classes: ["Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "spiritual-weapon": {
    name: "Spiritual Weapon",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, DF",
    duration: "1 round/level",
    description: "A weapon made of force appears and attacks foes at a distance, as you direct it, dealing 1d8 force damage per hit.",
    classes: ["Cleric"]
  },
  "silence": {
    name: "Silence",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "1 min./level",
    description: "Upon the casting of this spell, complete silence prevails in the affected area.",
    classes: ["Bard", "Cleric"]
  },
  "prayer": {
    name: "Prayer",
    level: 3,
    school: "Enchantment",
    castingTime: "1 action",
    range: "40 ft.",
    components: "V, S, DF",
    duration: "1 round/level",
    description: "You bring special favor upon yourself and your allies while bringing disfavor to your enemies.",
    classes: ["Cleric", "Paladin"]
  },
  "dispel-magic": {
    name: "Dispel Magic",
    level: 3,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You can use dispel magic to end ongoing spells that have been cast on a creature or object.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Wizard", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "freedom-of-movement": {
    name: "Freedom of Movement",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal or touch",
    components: "V, S, M (a leather thong, bound around the arm or a similar appendage)",
    duration: "10 min./level",
    description: "This spell enables you or a creature you touch to move and attack normally for the duration of the spell.",
    classes: ["Bard", "Cleric", "Druid", "Ranger", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "flame-strike": {
    name: "Flame Strike",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, DF",
    duration: "Instantaneous",
    description: "A flame strike produces a vertical column of divine fire roaring downward.",
    classes: ["Cleric", "Druid"]
  },

  // Additional Druid Spells
  "entangle": {
    name: "Entangle",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, DF",
    duration: "1 min./level",
    description: "Grasses, weeds, bushes, and even trees wrap, twist, and entwine about creatures in the area or those that enter the area.",
    classes: ["Druid", "Ranger"]
  },
  "barkskin": {
    name: "Barkskin",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "10 min./level",
    description: "Barkskin toughens a creature's skin. The spell grants a +2 enhancement bonus to the creature's existing natural armor bonus.",
    classes: ["Druid", "Ranger"]
  },
  "call-lightning": {
    name: "Call Lightning",
    level: 3,
    school: "Evocation",
    castingTime: "1 round",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 min./level",
    description: "Immediately upon completion of the spell, and once per round thereafter, you may call down a 5-foot-wide, 30-foot-long, vertical bolt of lightning.",
    classes: ["Druid"]
  },
  "spike-growth": {
    name: "Spike Growth",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    duration: "1 hour/level",
    components: "V, S, DF",
    description: "Any ground-covering vegetation in the spell's area becomes very hard and sharply pointed without changing its appearance.",
    classes: ["Druid", "Ranger"]
  },
  "wall-of-thorns": {
    name: "Wall of Thorns",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "10 min./level",
    description: "A wall of thorns spell creates a barrier of very tough, pliable, tangled brush bearing needle-sharp thorns.",
    classes: ["Druid"]
  },

  // Additional Bard Spells
  "fascinate": {
    name: "Fascinate",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Concentration + 1 round/level",
    description: "This spell causes one or more creatures to become fascinated with you.",
    classes: ["Bard"]
  },
  "hideous-laughter": {
    name: "Hideous Laughter",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (tiny tarts and a feather that is waved in the air)",
    duration: "1 round/level",
    description: "This spell afflicts the subject with uncontrollable laughter.",
    classes: ["Bard", "Wizard"]
  },
  "shatter": {
    name: "Shatter",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M/DF (a chip of mica)",
    duration: "Instantaneous",
    description: "Shatter creates a loud, ringing noise that breaks brittle, nonmagical objects.",
    classes: ["Bard", "Cleric", "Wizard"]
  },
  "glibness": {
    name: "Glibness",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "S",
    duration: "10 min./level",
    description: "Your speech becomes fluent and more believable. You gain a +30 bonus on Bluff checks made to convince another of the truth of your words.",
    classes: ["Bard"]
  },

  // Additional Ranger Spells
  "hunters-mark": {
    name: "Hunter's Mark",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "1 hour/level",
    description: "This spell creates a mystical connection between you and a creature within range.",
    classes: ["Ranger"]
  },
  "pass-without-trace": {
    name: "Pass without Trace",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "1 hour/level",
    description: "The subject or subjects can move through any type of terrain and leave neither footprints nor scent.",
    classes: ["Druid", "Ranger"]
  },
  "animal-messenger": {
    name: "Animal Messenger",
    level: 2,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a morsel of food)",
    duration: "1 day/level",
    description: "You compel a Tiny animal to go to a spot you designate.",
    classes: ["Bard", "Druid", "Ranger"]
  },

  // Expanded Necromancy Spells - Level 0 (Cantrips)
  "grave-spark": {
    name: "Grave Spark",
    level: 0,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You hurl a tiny spark of necrotic energy at a target. Make a ranged touch attack. If it hits a creature, it deals 1d4 points of necrotic damage. If it hits an object, it causes minor decay or a faint, unsettling chill.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "rotting-touch": {
    name: "Rotting Touch",
    level: 0,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S",
    duration: "3 rounds",
    description: "Your touch inflicts a minor, festering rot. Make a melee touch attack. If it hits, the target must make a Fortitude save. If it fails, it takes 1 point of necrotic damage each round for 3 rounds. This damage does not stack with multiple applications of this spell.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "finger-of-the-dead-minor": {
    name: "Finger of the Dead (Minor)",
    level: 0,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You point your finger, and a faint, ghostly appendage lances out to touch a creature. The target takes 1d3 points of necrotic damage, and you regain 1 hit point. This healing cannot increase your hit points above your maximum.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "corpse-light": {
    name: "Corpse Light",
    level: 0,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S, M (a pinch of bone dust)",
    duration: "1 hour (D)",
    description: "You touch a corpse, causing it to emanate a faint, eerie green or blue glow. The light is equivalent to that of a candle, providing dim illumination in a 5-foot radius. This spell is primarily for utility, such as marking corpses or providing minimal light in dark areas.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "chill-of-the-crypt": {
    name: "Chill of the Crypt",
    level: 0,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 round",
    description: "You instill a bone-chilling cold in a creature. The target must make a Fortitude save. If it fails, its weapon attacks deal 1 less point of damage for 1 round due to numb fingers and slowed reactions.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "whispers-from-beyond": {
    name: "Whispers from Beyond",
    level: 0,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 round",
    description: "You whisper faint, unsettling words that only the target can hear, seemingly from beyond the grave. The target must make a Will save or have disadvantage (or a -2 penalty) on its next attack roll made before the end of its next turn.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "spectral-claw": {
    name: "Spectral Claw",
    level: 0,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "Your hand briefly transforms into a shadowy, spectral claw as you make a melee touch attack. If it hits, the target takes 1d4 points of slashing damage and 1 point of necrotic damage.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "gravewind-flicker": {
    name: "Gravewind Flicker",
    level: 0,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "S",
    duration: "Instantaneous",
    description: "You create a brief, localized puff of spectral wind. You can use this to push a small, unattended object up to 5 feet, gently close or open an unlocked door or window, or cause loose papers to flutter.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Level 1 Necromancy Spells
  "decay": {
    name: "Decay",
    level: 1,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a pinch of grave dirt)",
    duration: "Instantaneous and 3 rounds (see text)",
    description: "You unleash a wave of necrotic energy that causes flesh to rot and wither. The target takes 2d6 points of necrotic damage immediately. Additionally, if the target fails a Fortitude save, it takes an additional 1d6 points of necrotic damage each round for the next 3 rounds as the decay continues.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "lifedraw": {
    name: "Lifedraw",
    level: 1,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You drain life force from a target to heal yourself. The target takes 3d6 points of necrotic damage, and you regain hit points equal to half the damage dealt (rounded down). This healing cannot increase your hit points above your maximum.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "summon-lesser-skeleton": {
    name: "Summon Lesser Skeleton",
    level: 1,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a tiny piece of bone and a drop of blood)",
    duration: "1 min./level (D)",
    description: "You animate a pile of bones or summon them from the earth to create a Small or Medium humanoid skeleton. It appears where you designate and acts immediately, on your turn. It attacks your opponents to the best of its ability. The skeleton has 10 HP, AC 13, and a single claw or rusty weapon attack dealing 1d6 damage. It has the standard undead traits.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "dread-whisper": {
    name: "Dread Whisper",
    level: 1,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 round + 1d4 rounds (see text)",
    description: "You utter a terrifying whisper that instills deep dread. The target must make a Will save. If it fails, it becomes frightened for 1 round and takes 1d4 points of psychic damage from the sheer terror. If the save succeeds, the target is shaken for 1 round and takes 1 point of psychic damage. A frightened creature flees from the source of its fear as best it can.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "putrefy-corpse": {
    name: "Putrefy Corpse",
    level: 1,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S, M (a pinch of sulfur)",
    duration: "Instantaneous",
    description: "You accelerate the decomposition of a corpse, rendering it unusable for spells that require a relatively intact body, such as animate dead or raise dead. The corpse becomes a foul, decaying mess. This spell does not affect undead creatures.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "pact-of-bone": {
    name: "Pact of Bone",
    level: 1,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S, F (a small, carved bone fetish)",
    duration: "10 min./level (D)",
    description: "You draw upon necromantic energies to fortify your form. You gain a +1 enhancement bonus to your natural armor (or a +1 natural armor bonus if you have no natural armor) and resistance 2 to necrotic damage.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "soul-tap": {
    name: "Soul Tap",
    level: 1,
    school: "Necromancy",
    castingTime: "1 Swift Action",
    range: "Personal",
    components: "V",
    duration: "1 round",
    description: "You imbue your next successful melee or ranged touch attack made before the end of your turn with a minor life-draining effect. If the attack hits a living creature, in addition to its normal effects, you steal 1d4 hit points from the target. This healing cannot increase your hit points above your maximum.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "eyes-of-the-grave": {
    name: "Eyes of the Grave",
    level: 1,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S, M (a dried eyeball or a piece of obsidian)",
    duration: "1 min./level (D)",
    description: "Your eyes glow with an eerie light, allowing you to perceive undead creatures. For the duration, you can detect the presence and location of undead creatures within 60 feet, as if you had blindsense specifically for undead. This also allows you to distinguish between different types of undead if you are familiar with them.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Level 2 Necromancy Spells
  "summon-bone-archer": {
    name: "Summon Bone Archer",
    level: 2,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a sharpened bone splinter and a piece of sinew)",
    duration: "1 min./level (D)",
    description: "You animate or summon a Medium humanoid skeleton equipped with a shortbow and a quiver of 20 arrows. It appears where you designate and acts immediately, on your turn. It attacks your opponents to the best of its ability, prioritizing ranged combat. The Bone Archer has 20 HP, AC 14, and makes one ranged attack per round dealing 1d6 piercing damage + 1d4 necrotic damage. It has standard undead traits.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "ghoul-touch": {
    name: "Ghoul Touch",
    level: 2,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S, M (a small piece of rotten flesh)",
    duration: "1d6+2 rounds (paralysis); Instantaneous (damage)",
    description: "Your touch mimics the paralyzing and sickening touch of a ghoul. Make a melee touch attack. If it hits, the target takes 1d8 points of necrotic damage and must succeed on a Fortitude save or be paralyzed for 1d6+2 rounds. Elves are immune to this paralysis effect. Even if the save against paralysis is successful, the target is sickened for 1 round from the foul contact.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "cursed-soulrot": {
    name: "Cursed Soulrot",
    level: 2,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, F (a desiccated worm)",
    duration: "5 rounds",
    description: "You inflict a virulent, soul-corrupting disease upon a creature. The target must make a Fortitude save. If it fails, it takes 1d6 points of necrotic damage each round for 5 rounds. Additionally, while affected, the creature cannot regain hit points through magical healing (natural healing still functions). A successful remove disease or similar magic can end this effect prematurely.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "drain-vigor": {
    name: "Drain Vigor",
    level: 2,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 min./level (Strength penalty); Instantaneous (damage)",
    description: "You sap the physical strength and vitality from a target. The target takes 2d6 points of necrotic damage and suffers a -2 penalty to Strength for 1 minute per caster level. A successful Fortitude save halves the necrotic damage and negates the Strength penalty. The Strength penalty from multiple castings of this spell does not stack.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "command-undead": {
    name: "Command Undead",
    level: 2,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a piece of bone and a drop of blood)",
    duration: "1 day/level",
    description: "You can command a single undead creature with Hit Dice no greater than your caster level. If the creature is intelligent, it gets a Will save to negate the effect. If it is non-intelligent (like a zombie or skeleton), it gets no saving throw. If the save is successful, you cannot attempt to command that particular undead again for 24 hours. If the save fails (or no save is allowed), the creature follows your verbal commands to the best of its ability for the duration.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "spectral-hand": {
    name: "Spectral Hand",
    level: 2,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 min./level (D)",
    description: "You create a ghostly, glowing hand, about the size of your own, that you can use to deliver touch spells at a distance. For the duration of the spell, you can use the spectral hand to deliver any touch spell of 3rd level or lower that you cast. The hand moves as you direct it (a move action), and you perceive through it as if it were your own hand for the purpose of delivering the touch spell. The hand is incorporeal and cannot be harmed.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Level 3 Necromancy Spells
  "summon-dreadknight": {
    name: "Summon Dreadknight",
    level: 3,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a blackened finger bone and a shard of obsidian)",
    duration: "1 min./level (D)",
    description: "You summon a Medium undead warrior wreathed in shadows, known as a Dreadknight. It appears where you designate and acts immediately, on your turn. It attacks your opponents with a shadowy greatsword. The Dreadknight has 40 HP, AC 16, and makes one attack per round with its greatsword dealing 2d6 slashing damage + 1d6 necrotic damage. It has standard undead traits and an aura of fear (creatures within 10 feet must make a Will save or be shaken for 1d4 rounds).",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "black-rot": {
    name: "Black Rot",
    level: 3,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, F (a piece of rotted meat)",
    duration: "Instantaneous and 3 rounds (see text)",
    description: "You inflict a potent, flesh-eating disease. The target takes 3d6 points of necrotic damage immediately. Additionally, if the target fails a Fortitude save, it takes an additional 2d6 points of necrotic damage each round for the next 3 rounds and takes 1 point of Constitution damage each round the ongoing damage persists. A successful remove disease or similar magic can end this effect prematurely.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "fearmongers-cry": {
    name: "Fearmonger's Cry",
    level: 3,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "15 ft.",
    components: "V, S",
    duration: "1d4 rounds",
    description: "You unleash a terrifying cry infused with necromantic dread. All living creatures within a 15-foot cone must make a Will save or become panicked for 1d4 rounds. A panicked creature drops everything it holds and flees at top speed from the source of its fear, as well as any other dangers it encounters, along a random path. It can't take any other actions.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "soul-mirror": {
    name: "Soul Mirror",
    level: 3,
    school: "Necromancy",
    castingTime: "1 Immediate Action",
    range: "Personal",
    components: "V, S",
    duration: "Instantaneous",
    description: "When you are targeted by a single-target spell of 3rd level or lower that allows spell resistance, you can attempt to reflect it back at its caster. You must make a caster level check (1d20 + your caster level) against a DC of 11 + the spell's caster level. If successful, the spell is turned back on its caster as if you had cast it. If you fail the check, you are affected by the spell normally.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "animate-dead-lesser": {
    name: "Animate Dead (Lesser)",
    level: 3,
    school: "Necromancy",
    castingTime: "1 minute",
    range: "Touch",
    components: "V, S, M (a black onyx gem worth at least 25 gp per HD of undead to be created)",
    duration: "Instantaneous (see text)",
    description: "This spell turns the bones or bodies of dead creatures into undead skeletons or zombies that follow your spoken commands. You can animate a number of Hit Dice of undead equal to twice your caster level (maximum 20 HD at 10th level). The undead remain animated until they are destroyed. You can control only 4 HD worth of undead creatures per caster level.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "vampiric-touch": {
    name: "Vampiric Touch",
    level: 3,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous/1 hour (see text)",
    description: "You must succeed on a melee touch attack. Your touch deals 1d6 points of damage per two caster levels (maximum 5d6). You gain temporary hit points equal to the damage you deal. These temporary hit points last for up to 1 hour. They do not stack with other temporary hit points.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Level 4 Necromancy Spells
  "summon-corpse-golem": {
    name: "Summon Corpse Golem",
    level: 4,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a collection of at least three humanoid corpses or equivalent mass of body parts, and a black pearl worth 100 gp)",
    duration: "1 min./level (D)",
    description: "You animate a grotesque golem stitched together from available corpses. It appears where you designate and acts immediately, on your turn. It mindlessly attacks your opponents. The Corpse Golem is a Large construct with 60 HP, AC 15, and two slam attacks per round dealing 2d8+4 bludgeoning damage each. It also has an Aura of Slowing (creatures within 10 feet must make a Fortitude save or have their speed halved for 1 round).",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "leeching-plague": {
    name: "Leeching Plague",
    level: 4,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, F (a live leech)",
    duration: "4 rounds",
    description: "You inflict a debilitating plague that drains life force from the target and transfers it to you. The target must make a Fortitude save. If it fails, it takes 2d6 points of necrotic damage each round for 4 rounds. You regain hit points equal to half the damage dealt by this spell each round. This healing cannot increase your hit points above your maximum. A successful remove disease or similar magic can end this effect prematurely.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "aura-of-dread": {
    name: "Aura of Dread",
    level: 4,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S",
    duration: "1 min./level (D)",
    description: "You emanate an aura of palpable dread. Enemies who enter or start their turn within 10 feet of you must make a Will save or take a -1 penalty on attack rolls and saving throws while they remain in the aura and for 1 round after leaving it. A creature that successfully saves against this aura cannot be affected by it again for 24 hours. This is a fear effect.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "soulburn-pact": {
    name: "Soulburn Pact",
    level: 4,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S, M (a drop of your blood and a pinch of ash from a cremated humanoid)",
    duration: "Instantaneous",
    description: "You make a pact with dark energies, sacrificing a portion of your life force to regain magical power. You take 20 points of damage (this damage cannot be reduced or redirected in any way), and in return, you regain one expended spell slot of 3rd level or lower. You cannot use this spell if you have less than 21 hit points.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "contagion": {
    name: "Contagion",
    level: 4,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "The subject contracts a disease selected from the table below, which strikes immediately (no incubation period). The DC noted is for the subsequent saves (use disease rules) the victim must make to avoid the disease's debilitating effects. The victim must make an immediate Fortitude save. If this initial save fails, the victim loses 1d3 points of Constitution immediately, and must continue to make saves every day thereafter.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Level 5 Necromancy Spells
  "summon-bone-legion": {
    name: "Summon Bone Legion",
    level: 5,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a collection of bones from at least five different humanoids and a ruby worth 200 gp)",
    duration: "1 min./level (D)",
    description: "You summon a small legion of skeletal warriors. You summon 1d4+1 Medium skeletons that appear where you designate and act immediately, on your turn. Each skeleton has 15 HP, AC 13, and makes one attack per round dealing 1d6 slashing damage + 1d4 necrotic damage. They have standard undead traits and follow your mental commands.",
    classes: ["Wizard", "Cleric"]
  },
  "necrotic-wave": {
    name: "Necrotic Wave",
    level: 5,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "30-ft.-radius burst",
    components: "V, S, M (a vial of grave dirt)",
    duration: "Instantaneous and 3 rounds (see text)",
    description: "You unleash a wave of potent necrotic energy, causing flesh to rapidly decay. All enemies within a 30-foot radius take 4d8 points of necrotic damage immediately. Additionally, any enemy that fails a Fortitude save takes an additional 2d6 points of necrotic damage each round for the next 3 rounds as the decay continues to ravage their bodies.",
    classes: ["Wizard", "Cleric"]
  },
  "terror-chain": {
    name: "Terror Chain",
    level: 5,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a small, twisted iron chain link)",
    duration: "3 rounds (initial target); 1 round (secondary targets)",
    description: "You instill overwhelming terror in a primary target. The target must make a Will save or become panicked for 3 rounds. If the primary target fails its save, at the start of its next turn, the terror can leap to one additional living creature of your choice within 30 feet of the primary target. This chain effect can continue each round for the spell's duration, potentially affecting a new secondary target each round.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "grave-gift": {
    name: "Grave Gift",
    level: 5,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "You make a perilous pact, transferring your own life force to save an ally. You sacrifice up to half your current hit points (minimum 10 HP sacrificed). The touched ally, if they are dying (between -1 and -9 hit points, or equivalent), is immediately stabilized and healed for twice the amount of hit points you sacrificed. You cannot sacrifice more hit points than would bring you below 1 HP.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "waves-of-fatigue": {
    name: "Waves of Fatigue",
    level: 5,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "30-ft. cone",
    components: "V, S",
    duration: "Instantaneous (see text)",
    description: "Waves of negative energy wash out from you. Any living creature in the area of effect becomes fatigued (no save). Creatures already fatigued become exhausted. Creatures immune to fatigue are not affected. This spell has no effect on creatures that are already exhausted.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "blight": {
    name: "Blight",
    level: 5,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, DF",
    duration: "Instantaneous",
    description: "This spell withers a single plant creature or one ordinary plant of any size. An ordinary plant targeted by blight takes 1d6 points of damage per caster level (maximum 15d6) and withers and dies unless it makes a Fortitude save. A plant creature targeted by blight takes the same damage but can attempt a Fortitude save for half damage.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Shaman", "Thief"]
  },

  // Level 6 Necromancy Spells
  "summon-soul-wraith": {
    name: "Summon Soul Wraith",
    level: 6,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a black sapphire worth 250 gp and a lock of hair from a creature that died of sorrow)",
    duration: "1 min./level (D)",
    description: "You summon a Soul Wraith, a powerful incorporeal undead creature composed of tormented spirits. It appears where you designate and acts immediately, on your turn. The Soul Wraith is a Medium undead creature with 100 HP, AC 18, and is incorporeal. It makes two touch attacks per round, each dealing 2d8 cold damage + 1d6 Wisdom drain. A creature whose Wisdom is drained to 0 becomes a helpless, catatonic shell until its Wisdom is restored.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "blood-fog": {
    name: "Blood Fog",
    level: 6,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a pint of blood, fresh or preserved)",
    duration: "1 round/level (D)",
    description: "You conjure a roiling cloud of crimson mist that reeks of blood. The area within the cloud is heavily obscured. Additionally, any living creature that starts its turn within the Blood Fog takes 3d6 points of necrotic damage as the mist leeches its vitality (Fortitude save for half damage). Undead creatures within the Blood Fog are healed for 1d6 hit points at the start of their turn.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "command-undeath-greater": {
    name: "Command Undeath (Greater)",
    level: 6,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a black onyx gem worth 500 gp)",
    duration: "Permanent (see text)",
    description: "This spell functions like command undead, but you can command up to two undead creatures, and their total Hit Dice can be up to twice your caster level. The undead creatures must be within 30 feet of each other when targeted. Commanded undead remain under your control indefinitely until they are destroyed or you release them. You can control a total number of HD of undead equal to 4 x your caster level through this spell and animate dead.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "soulfire-nova": {
    name: "Soulfire Nova",
    level: 6,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "30-ft. radius burst centered on you",
    components: "V, S",
    duration: "Instantaneous",
    description: "You unleash an explosive nova of sickly green and black soulfire. All creatures in the area take 6d6 points of fire damage and 6d6 points of necrotic damage (Reflex save for half fire damage; necrotic damage is not halved). Additionally, all undead creatures in the area that fail a Will save are blinded for 1d4 rounds by the searing unholy light.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "circle-of-death": {
    name: "Circle of Death",
    level: 6,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (the powder of a crushed black pearl worth 500 gp)",
    duration: "Instantaneous",
    description: "Negative energy bursts forth in all directions from a point you select, snuffing out the life force of nearby creatures. The spell slays 1d4 HD worth of living creatures per caster level (maximum 20d4). Creatures with the fewest HD are affected first; among creatures with equal HD, those who are closest to the spell's point of origin are affected first. No creature with 9 or more HD can be affected.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "undeath-to-death": {
    name: "Undeath to Death",
    level: 6,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (the powder of a crushed diamond worth 500 gp)",
    duration: "Instantaneous",
    description: "This spell is the reverse of circle of death and destroys undead creatures. It destroys 1d4 HD worth of undead creatures per caster level (maximum 20d4). Creatures with the fewest HD are affected first; among creatures with equal HD, those who are closest to the spell's point of origin are affected first. No creature with 9 or more HD can be affected.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Level 7 Necromancy Spells
  "summon-bone-colossus": {
    name: "Summon Bone Colossus",
    level: 7,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a complete humanoid skeleton of a Large creature and a black diamond worth 1,000 gp)",
    duration: "10 min./level (D)",
    description: "You animate a towering Bone Colossus from a large skeleton or summon one forth. It appears where you designate and acts immediately, on your turn. It is a Huge undead creature with 140 HP, AC 19, and makes two slam attacks per round, each dealing 2d10+7 bludgeoning damage. Once every 1d4 rounds, it can unleash a Cleave attack, hitting all creatures in a 15-foot cone for its slam damage. It has DR 10/bludgeoning and magic, and standard undead traits.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "black-reaping": {
    name: "Black Reaping",
    level: 7,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "30-ft. cone",
    components: "V, S, DF",
    duration: "Instantaneous",
    description: "You unleash a devastating wave of necrotic energy in a cone, sapping the life from all in its path. All living creatures in the cone take 6d8 points of necrotic damage (Fortitude save for half). You heal hit points equal to the total necrotic damage dealt to all targets (up to your maximum hit points).",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "wail-of-the-damned": {
    name: "Wail of the Damned",
    level: 7,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "30-ft.-radius spread centered on you",
    components: "V",
    duration: "Instantaneous (stun); 1d4 rounds (shaken)",
    description: "You unleash an unearthly wail composed of the tormented cries of countless souls. All living creatures within a 30-foot radius must make a Will save. Those who fail are stunned for 1 round and take 3d6 points of psychic damage. Those who succeed on the save are instead shaken for 1d4 rounds and take 1d6 psychic damage. This is a fear effect.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "chain-of-the-grave": {
    name: "Chain of the Grave",
    level: 7,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a link from a rusted iron chain)",
    duration: "3 rounds",
    description: "You conjure spectral chains, cold as the grave, to bind a creature and anchor it to the Material Plane. The target must make a Will save. If it fails, for 3 rounds, it cannot use any form of extradimensional travel. Furthermore, its movement speed is halved, and it takes a -2 penalty to AC and Dexterity-based skill checks due to the encumbering spectral chains.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "control-undead": {
    name: "Control Undead",
    level: 7,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a piece of bone and a drop of blood for each HD of the target, up to 1,000 gp total)",
    duration: "1 min./level (D)",
    description: "This spell enables you to control an undead creature. If the creature is intelligent, it perceives your words and actions in the most favorable way (treat its attitude as friendly). It will not attack you while the spell lasts. You can give the subject orders, but you must win an opposed Charisma check to convince it to do anything it wouldn't ordinarily do.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Additional Divination Spells
  "augury": {
    name: "Augury",
    level: 2,
    school: "Divination",
    castingTime: "1 minute",
    range: "Personal",
    components: "V, S, M (incense worth at least 25 gp), F (a set of marked sticks, bones, or similar tokens of at least 25 gp value)",
    duration: "Instantaneous",
    description: "An augury can tell you whether a particular action will bring good or bad results for you in the immediate future.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman", "locate-object", "Locate Object", "Divination", "1 action", "Long (400 ft. + 40 ft./level)", "V, S, F/DF (a forked twig)", "1 min./level", "You sense the direction of a well-known or clearly visualized object.", "Bard", "Wizard"]
  },
  "scrying": {
    name: "Scrying",
    level: 4,
    school: "Divination",
    castingTime: "1 hour",
    range: "See text",
    components: "V, S, M/DF (a pool of water), F (a silver mirror worth at least 1,000 gp)",
    duration: "1 min./level",
    description: "You can observe a creature at any distance.",
    classes: ["Bard", "Cleric", "Druid", "Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior", "commune", "Commune", "Divination", "10 minutes", "Personal", "V, S, M (incense and a sacrificial offering appropriate to your religion, together worth at least 500 gp)", "1 round/level", "You contact your deity\u2014or agents thereof\u2014and ask questions that can be answered by a simple yes or no."]
  },
  "legend-lore": {
    name: "Legend Lore",
    level: 6,
    school: "Divination",
    castingTime: "See text",
    range: "Personal",
    components: "V, S, M (incense worth at least 250 gp), F (four ivory strips worth at least 50 gp each)",
    duration: "See text",
    description: "Legend lore brings to your mind legends about an important person, place, or thing.",
    classes: ["Bard", "Wizard"]
  },
  "vision": {
    name: "Vision",
    level: 7,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (incense worth at least 25 gp)",
    duration: "See text",
    description: "This spell functions like legend lore, except that it works more quickly and produces some strain on you.",
    classes: ["Cleric"]
  },
  "discern-location": {
    name: "Discern Location",
    level: 8,
    school: "Divination",
    castingTime: "10 minutes",
    range: "Unlimited",
    components: "V, S, F (a forked twig)",
    duration: "Instantaneous",
    description: "A discern location spell is among the most powerful means of locating creatures or objects.",
    classes: ["Cleric", "Wizard"]
  },
  "foresight": {
    name: "Foresight",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal or touch",
    components: "V, S, M (a hummingbird's feather)",
    duration: "10 min./level",
    description: "This spell grants you a powerful sixth sense in relation to yourself or another.",
    classes: ["Druid", "Wizard"]
  },

  // Additional Enchantment Spells
  "daze": {
    name: "Daze",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a pinch of wool or similar substance)",
    duration: "1 round",
    description: "This enchantment clouds the mind of a humanoid creature with 4 or fewer Hit Dice so that it takes no actions.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief", "sleep", "Sleep", "Enchantment", "1 round", "Medium (100 ft. + 10 ft./level)", "V, S, M (fine sand, rose petals, or a live cricket)", "1 min./level", "A sleep spell causes a magical slumber to come upon 4d4 Hit Dice of creatures.", "enthrall", "Enthrall", "V, S", "1 hour or less", "If you have the attention of a group of creatures, you can use this spell to hold them spellbound.", "Cleric"]
  },
  "heroism": {
    name: "Heroism",
    level: 3,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "10 min./level",
    description: "This spell imbues a single creature with great bravery and morale in battle.",
    classes: ["Bard", "Wizard"]
  },
  "geas-lesser": {
    name: "Geas, Lesser",
    level: 4,
    school: "Enchantment",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "1 day/level or until discharged",
    description: "A lesser geas places a magical command on a creature to carry out some service or to refrain from some action or course of activity.",
    classes: ["Bard", "Wizard"]
  },
  "mind-fog": {
    name: "Mind Fog",
    level: 5,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "30 minutes and 2d6 rounds; see text",
    description: "Mind fog produces a bank of thin mist that weakens the mental resistance of those caught in it.",
    classes: ["Bard", "Wizard"]
  },
  "geas-greater": {
    name: "Geas, Greater",
    level: 6,
    school: "Enchantment",
    castingTime: "10 minutes",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "Permanent until discharged",
    description: "This spell functions similarly to lesser geas, except that it affects a creature of any HD and allows no saving throw.",
    classes: ["Bard", "Cleric", "Wizard"]
  },
  "insanity": {
    name: "Insanity",
    level: 7,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "The affected creature suffers from a continuous confusion effect, as the spell.",
    classes: ["Wizard"]
  },
  "mass-charm-monster": {
    name: "Mass Charm Monster",
    level: 8,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 day/level",
    description: "This spell functions like charm monster, except that mass charm monster affects a number of creatures whose combined HD do not exceed twice your level.",
    classes: ["Bard", "Wizard"]
  },
  "dominate-monster": {
    name: "Dominate Monster",
    level: 9,
    school: "Enchantment",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 day/level",
    description: "This spell functions like dominate person, except that the spell is not restricted by creature type.",
    classes: ["Wizard", "Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },

  // Additional Evocation Spells
  "dancing-lights": {
    name: "Dancing Lights",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 minute",
    description: "Depending on the version selected, you create up to four lights that resemble lanterns or torches.",
    classes: ["Bard", "Wizard"]
  },
  "burning-hands": {
    name: "Burning Hands",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "15 ft.",
    components: "V, S",
    duration: "Instantaneous",
    description: "A cone of searing flame shoots from your fingertips.",
    classes: ["Wizard"]
  },
  "continual-flame": {
    name: "Continual Flame",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (ruby dust worth 50 gp)",
    duration: "Permanent",
    description: "A flame, equivalent in brightness to a torch, springs forth from an object that you touch.",
    classes: ["Cleric", "Wizard"]
  },
  "daylight": {
    name: "Daylight",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "10 min./level",
    description: "The object touched sheds light as bright as full daylight in a 60-foot radius.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Wizard"]
  },
  "wall-of-ice": {
    name: "Wall of Ice",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a piece of quartz or similar rock crystal)",
    duration: "1 min./level",
    description: "This spell creates an anchored plane of ice or a hemisphere of ice, depending on the version selected.",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "sending": {
    name: "Sending",
    level: 5,
    school: "Evocation",
    castingTime: "10 minutes",
    range: "See text",
    components: "V, S, M/DF (fine copper wire)",
    duration: "1 round; see text",
    description: "You contact a particular creature with which you are familiar and send a short message of twenty-five words or less to the subject.",
    classes: ["Cleric", "Wizard"]
  },
  "contingency": {
    name: "Contingency",
    level: 6,
    school: "Evocation",
    castingTime: "At least 10 minutes; see text",
    range: "Personal",
    components: "V, S, M (quicksilver, an eyelash of an ogre mage, and a sapphire worth at least 1,500 gp)",
    duration: "1 day/level or until discharged",
    description: "You can place another spell upon your person so that it comes into effect under some condition you dictate when casting contingency.",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "forcecage": {
    name: "Forcecage",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (ruby dust worth 1,500 gp)",
    duration: "2 hours/level",
    description: "This powerful spell brings into being an immobile, invisible cubical prison composed of either bars of force or solid walls of force.",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "sunburst": {
    name: "Sunburst",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M/DF (fire and a piece of sunstone)",
    duration: "Instantaneous",
    description: "Sunburst causes a globe of searing radiance to explode silently from a point you select.",
    classes: ["Druid", "Wizard"]
  },
  "meteor-swarm": {
    name: "Meteor Swarm",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "Meteor swarm is a very powerful and spectacular spell that is similar to fireball in many aspects.",
    classes: ["Wizard", "Crimson Agent", "Dragoon", "Mage", "Warrior", "sanctuary", "Sanctuary", "Abjuration", "1 action", "Touch", "V, S, DF", "1 round/level", "Any opponent attempting to strike or otherwise directly attack the warded creature, even with a targeted spell, must attempt a Will save.", "Cleric"]
  },
  "obscure-object": {
    name: "Obscure Object",
    level: 2,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (chameleon skin)",
    duration: "8 hours",
    description: "This spell hides an object from location by divination (scrying) effects, such as the scrying spell or a crystal ball.",
    classes: ["Bard", "Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "magic-circle-against-evil": {
    name: "Magic Circle against Evil",
    level: 3,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (a 3-ft.-diameter circle of powdered silver)",
    duration: "10 min./level",
    description: "All creatures within the area gain the effects of a protection from evil spell, and no nongood summoned creatures can enter the area either.",
    classes: ["Cleric", "Paladin", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "dimensional-anchor": {
    name: "Dimensional Anchor",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 min./level",
    description: "A green ray springs from your hand. You must make a ranged touch attack to hit the target. Any creature or object struck by the ray is covered with a shimmering emerald field that completely blocks extradimensional travel.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "break-enchantment": {
    name: "Break Enchantment",
    level: 5,
    school: "Abjuration",
    castingTime: "1 minute",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell frees victims from enchantments, transmutations, and curses.",
    classes: ["Bard", "Cleric", "Paladin", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "antimagic-field": {
    name: "Antimagic Field",
    level: 6,
    school: "Abjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V, S, M/DF (pinch of powdered iron or iron filings)",
    duration: "10 min./level",
    description: "An invisible barrier surrounds you and moves with you. The space within this barrier is impervious to most magical effects, including spells, spell-like abilities, and supernatural abilities.",
    classes: ["Cleric", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior", "Druid", "Monk"]
  },
  "spell-turning": {
    name: "Spell Turning",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M/DF (a small silver mirror)",
    duration: "Until expended or 10 min./level",
    description: "Spells and spell-like effects targeted on you are turned back upon the original caster.",
    classes: ["Bard", "Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "mind-blank": {
    name: "Mind Blank",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "24 hours",
    description: "The subject is protected from all devices and spells that detect, influence, or read emotions or thoughts.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "prismatic-sphere": {
    name: "Prismatic Sphere",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V",
    duration: "10 min./level",
    description: "This spell functions like prismatic wall, except you conjure up an immobile, opaque globe of shimmering, multicolored light that surrounds you and protects you from all forms of attack.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },

  // Additional Conjuration Spells
  "mount": {
    name: "Mount",
    level: 1,
    school: "Conjuration",
    castingTime: "1 round",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a bit of horse hair)",
    duration: "2 hours/level",
    description: "You summon a light horse or a pony (your choice) to serve you as a mount.",
    classes: ["Wizard"]
  },
  "fog-cloud": {
    name: "Fog Cloud",
    level: 2,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "10 min./level",
    description: "A bank of fog billows out from the point you designate. The fog obscures all sight, including darkvision, beyond 5 feet.",
    classes: ["Druid", "Wizard"]
  },
  "stinking-cloud": {
    name: "Stinking Cloud",
    level: 3,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a rotten egg or several skunk cabbage leaves)",
    duration: "1 round/level",
    description: "Stinking cloud creates a bank of fog like that created by fog cloud, except that the vapors are nauseating.",
    classes: ["Wizard"]
  },
  "evards-black-tentacles": {
    name: "Evard's Black Tentacles",
    level: 4,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (octopus or squid tentacle)",
    duration: "1 round/level",
    description: "This spell conjures a field of rubbery black tentacles, each 10 feet long, that rise from the ground.",
    classes: ["Wizard"]
  },
  "wall-of-stone": {
    name: "Wall of Stone",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M/DF (a small block of granite)",
    duration: "Instantaneous",
    description: "This spell creates a wall of rock that merges into adjoining rock surfaces.",
    classes: ["Cleric", "Druid", "Wizard"]
  },
  "planar-binding": {
    name: "Planar Binding",
    level: 6,
    school: "Conjuration",
    castingTime: "10 minutes",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a jewel worth at least 1,000 gp)",
    duration: "Instantaneous",
    description: "This spell attempts to bargain with a creature from another plane in order to exchange services.",
    classes: ["Wizard"]
  },
  "plane-shift": {
    name: "Plane Shift",
    level: 7,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, F (a forked, metal rod attuned to the plane of travel)",
    duration: "Instantaneous",
    description: "You move yourself or some other creature to another plane of existence or alternate dimension.",
    classes: ["Cleric", "Wizard"]
  },
  "maze": {
    name: "Maze",
    level: 8,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "See text",
    description: "You banish the subject into an extradimensional labyrinth of force planes.",
    classes: ["Wizard"]
  },
  "gate": {
    name: "Gate",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action or see text",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, XP; see text",
    duration: "Instantaneous or concentration (up to 1 round/level); see text",
    description: "Casting a gate spell has two effects. First, it creates an interdimensional connection between your plane of existence and a plane you specify.",
    classes: ["Cleric", "Wizard"]
  },

  // Additional Illusion Spells

  "hypnotic-pattern": {
    name: "Hypnotic Pattern",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a stick of incense or a crystal rod filled with phosphorescent material)",
    duration: "Concentration, up to 2 rounds + 1 round/level",
    description: "A twisting pattern of subtle, shifting colors weaves through the air, fascinating creatures within it.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "major-image": {
    name: "Major Image",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F (a bit of fleece)",
    duration: "Concentration + 3 rounds",
    description: "This spell functions like silent image, except that sound, smell, and thermal illusions are included in the spell effect.",
    classes: ["Bard", "Wizard", "Crimson Agent", "Mirrorsage", "Monk", "Thief", "hallucinatory-terrain", "Hallucinatory Terrain", "Illusion", "10 minutes", "Long (400 ft. + 40 ft./level)", "V, S, M (a stone, a twig, and a bit of green plant)", "2 hours/level", "You make natural terrain look, sound, and smell like some other sort of natural terrain.", "Druid", "seeming", "Seeming", "1 action", "Close (25 ft. + 5 ft./2 levels)", "V, S", "12 hours", "This spell functions like disguise self, except that you can change the appearance of other people as well."]
  },
  "programmed-image": {
    name: "Programmed Image",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (jade dust worth 25 gp)",
    duration: "Permanent until triggered, then 1 round/level",
    description: "This spell functions like major image, except that this spell's figment activates when a specific condition occurs.",
    classes: ["Bard", "Wizard"]
  },
  "project-image": {
    name: "Project Image",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a small replica of you worth 5 gp)",
    duration: "1 round/level",
    description: "You tap energy from the Plane of Shadow to create a quasi-real, illusory version of yourself.",
    classes: ["Bard", "Wizard"]
  },
  "screen": {
    name: "Screen",
    level: 8,
    school: "Illusion",
    castingTime: "10 minutes",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "24 hours",
    description: "This spell combines several elements to create a powerful protection from scrying and direct observation.",
    classes: ["Wizard"]
  },
  "weird": {
    name: "Weird",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like phantasmal killer, except it can affect more than one creature.",
    classes: ["Wizard"]
  },

  // Additional Transmutation Spells
  // Level 0 Transmutation Spells
  "magehand": {
    name: "Magehand",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Concentration",
    description: "You point your finger at an object and can lift it and move it at will from a distance. As a move action, you can propel the object as far as 15 feet in any direction, though the spell ends if the distance between you and the object ever exceeds the spell's range.",
    classes: ["Bard", "Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "shimmerstep": {
    name: "Shimmerstep",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 round",
    description: "Your form shimmers and becomes slightly translucent. You gain a +2 dodge bonus to AC against the next attack made against you before the start of your next turn.",
    classes: ["Bard", "Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior", "stone-touch", "Stone Touch", "Transmutation", "1 action", "Touch", "V, S", "1 minute", "You touch a small object (no larger than 1 cubic foot) and temporarily transform it into stone. The object becomes as hard as stone but retains its original shape and size. If used on a weapon, it deals bludgeoning damage instead of its normal damage type.", "mold-matter", "Mold Matter", "You can slightly reshape a small amount of soft material (clay, wax, soft metal, etc.) no larger than 1 cubic foot. The change is minor and cosmetic only."]
  },
  "minor-enhancement": {
    name: "Minor Enhancement",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 minute",
    description: "You touch a simple tool or weapon and grant it a +1 enhancement bonus to its function. For tools, this might mean a +1 bonus to relevant skill checks. For weapons, this grants a +1 enhancement bonus to attack rolls only.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior", "fleeting-flight", "Fleeting Flight", "Transmutation", "1 action", "Personal", "V, S", "1 round", "You gain a fly speed of 20 feet with poor maneuverability for 1 round. You must land at the end of your turn or fall."]
  },
  "snap-freeze-gentle-warmth": {
    name: "Snap Freeze/Gentle Warmth",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "You can instantly freeze or warm up to 1 cubic foot of liquid or small object. This can freeze water into ice or melt ice into water, but deals no damage to creatures.",
    classes: ["Druid", "Wizard"]
  },
  "flicker-skin": {
    name: "Flicker Skin",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 round",
    description: "Your skin briefly takes on the coloration and texture of your surroundings. You gain a +4 bonus to Hide checks for 1 round.",
    classes: ["Druid", "Ranger", "Wizard", "Dragoon", "Mage", "Monk", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },

  "expeditious-retreat": {
    name: "Expeditious Retreat",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 min./level",
    description: "This spell increases your base land speed by 30 feet.",
    classes: ["Bard", "Wizard"]
  },
  "featherstep": {
    name: "Featherstep",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "10 minutes/level",
    description: "The target's weight is reduced by half, allowing them to walk on fragile surfaces without breaking them and granting a +4 bonus to Jump checks.",
    classes: ["Druid", "Ranger", "Wizard", "Dragoon", "Mage", "Monk", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "stoneflesh": {
    name: "Stoneflesh",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a small piece of granite)",
    duration: "1 minute/level",
    description: "The target's skin becomes as hard as stone, granting damage reduction 2/- against physical attacks.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "weaponbend": {
    name: "Weaponbend",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 round/level",
    description: "You cause a metal weapon to become flexible like rubber. The weapon deals nonlethal damage and has a -2 penalty to attack rolls.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "spider-climb": {
    name: "Spider Climb",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a live spider)",
    duration: "10 min./level",
    description: "The subject can climb and travel on vertical surfaces or even traverse ceilings as well as a spider does.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "feral-might": {
    name: "Feral Might",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 minute/level",
    description: "The target gains animalistic features: +2 to Strength, natural claws that deal 1d4 damage, and low-light vision.",
    classes: ["Druid", "Ranger", "Dragoon", "Mage", "Monk", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "steel-skin": {
    name: "Steel Skin",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a piece of steel)",
    duration: "1 minute/level",
    description: "The target's skin takes on a metallic sheen and becomes resistant to slashing and piercing damage, gaining damage reduction 3/bludgeoning.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "magnetic-grip": {
    name: "Magnetic Grip",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (iron filings)",
    duration: "10 minutes/level",
    description: "The target's hands become magnetic, allowing them to cling to metal surfaces and granting a +8 bonus to Climb checks on metal surfaces. Metal weapons cannot be disarmed from the target.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "unravel-threads": {
    name: "Unravel Threads",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "You cause cloth, rope, or similar fibrous material to unravel. This can destroy clothing, weaken ropes (reducing their break DC by 10), or create difficult terrain from carpets.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "alter-self": {
    name: "Alter Self",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "10 min./level",
    description: "You assume the form of a creature of the same type as your normal form.",
    classes: ["Bard", "Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "transmute-weapon": {
    name: "Transmute Weapon",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a small piece of the desired material)",
    duration: "1 hour/level",
    description: "You change the material composition of a weapon. The weapon can be made of wood, stone, metal, or crystal, changing its damage type and properties accordingly.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "swiftness": {
    name: "Swiftness",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 minute/level",
    description: "The target gains an extra move action each round and a +2 bonus to Reflex saves.",
    classes: ["Bard", "Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "stone-shape": {
    name: "Stone Shape",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (soft clay)",
    duration: "Instantaneous",
    description: "You can form an existing piece of stone into any shape that suits your purpose.",
    classes: ["Cleric", "Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "disable-limb": {
    name: "Disable Limb",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 minute/level",
    description: "You temporarily disable one of the target's limbs. An arm cannot hold items or cast spells with somatic components, a leg reduces movement speed by half.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "bulls-strength": {
    name: "Bull's Strength",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (a few hairs, or a pinch of dung, from a bull)",
    duration: "1 min./level",
    description: "The subject becomes stronger. The spell grants a +4 enhancement bonus to Strength, adding the usual benefits to melee attack rolls, melee damage rolls, and other uses of the Strength modifier.",
    classes: ["Cleric", "Druid", "Wizard"]
  },

  "bears-endurance": {
    name: "Bear's Endurance",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (a few hairs, or a pinch of dung, from a bear)",
    duration: "1 min./level",
    description: "The affected creature gains greater vitality and stamina. The spell grants a +4 enhancement bonus to Constitution, adding the usual benefits to hit points, Fortitude saves, Constitution checks, and so forth.",
    classes: ["Cleric", "Druid", "Ranger", "Wizard"]
  },
  "gaseous-form": {
    name: "Gaseous Form",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "S, M/DF (a bit of gauze and a wisp of smoke)",
    duration: "2 min./level",
    description: "The subject and all its gear become insubstantial, misty, and translucent.",
    classes: ["Bard", "Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior", "slow", "Slow", "Transmutation", "1 action", "Close (25 ft. + 5 ft./2 levels)", "V, S, M (a drop of molasses)", "1 round/level", "An affected creature moves and acts more slowly than normal. A slowed creature can take only a single move action or standard action each turn, but not both (nor may it take full-round actions).", "formshift", "Formshift", "Touch", "V, S, M (a piece of clay)", "10 minutes/level", "You alter the target's physical form, allowing them to take on aspects of different creature types. The target can gain one of the following: natural armor +2, natural weapon (1d6), or a special movement mode (swim, climb, or burrow at half speed)."]
  },
  "shatter-earth": {
    name: "Shatter Earth",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a piece of broken stone)",
    duration: "Instantaneous",
    description: "You cause the ground in a 20-foot radius to crack and shift. Creatures in the area must make a Reflex save or fall prone. The area becomes difficult terrain.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "keen-edge": {
    name: "Keen Edge",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "10 min./level",
    description: "This spell makes a weapon magically keen, improving its ability to deal telling blows. This benefit doesn't stack with any other effects that improve the weapon's threat range.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },

  "greater-stoneflesh": {
    name: "Greater Stoneflesh",
    level: 4,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a diamond chip worth 50 gp)",
    duration: "1 min./level",
    description: "The target's skin becomes exceptionally hard, like dense granite. The creature gains a +4 enhancement bonus to its natural armor and Damage Reduction 5/adamantine against non-magical bludgeoning, piercing, and slashing damage. Movement speed is reduced by 10 feet.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "crystalline-growth": {
    name: "Crystalline Growth",
    level: 4,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a quartz crystal)",
    duration: "1 round/level",
    description: "You cause sharp, crystalline structures to erupt from the ground in a 20-foot radius. The area becomes difficult terrain. Any creature moving into or starting its turn in the area takes 3d6 points of piercing damage (Reflex save negates).",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "teleport-object": {
    name: "Teleport Object",
    level: 4,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You instantly transport one non-living, unattended object from one location to another within range. The destination must be a spot you can see. You cannot teleport an object into an area already occupied by another solid object or creature.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "formlock": {
    name: "Formlock",
    level: 4,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a drop of quick-setting glue)",
    duration: "1 min./level",
    description: "You attempt to magically lock a creature into its current physical form. The target cannot willingly change its shape or form for the duration. This prevents the use of polymorph effects, wild shape, gaseous form, or any other ability that changes its physical structure.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "stone-skin": {
    name: "Stone Skin",
    level: 4,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (granite and diamond dust worth 250 gp)",
    duration: "10 min./level or until discharged",
    description: "The subject gains damage reduction 10/adamantine. It ignores the first 10 points of damage from each attack. Once the spell has prevented a total of 10 points of damage per caster level (maximum 150 points), it is discharged.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "polymorph-self": {
    name: "Polymorph Self",
    level: 4,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a piece of the creature whose form you plan to take)",
    duration: "1 min./level",
    description: "You change your form, taking on the appearance and many of the abilities of another creature. You can assume the form of any Small or Medium creature of the animal, humanoid, or elemental type. You gain the new form's physical ability scores, size, speed, natural armor, and natural attacks.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "transmute-terrain": {
    name: "Transmute Terrain",
    level: 5,
    school: "Transmutation",
    castingTime: "10 minutes",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a sample of the desired terrain type)",
    duration: "24 hours",
    description: "You permanently alter the terrain in a large area. You can change one type of terrain into another common type (e.g., forest to plains, swamp to solid ground, sand to shallow water). The new terrain is mundane and non-magical.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "ironskin-legion": {
    name: "Ironskin Legion",
    level: 5,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a small iron ingot)",
    duration: "1 min./level",
    description: "The skin of the affected creatures turns to a dull, iron-like sheen. Each target gains a +2 enhancement bonus to their natural armor and Damage Reduction 5/adamantine against bludgeoning, piercing, and slashing damage.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "petrify-limb": {
    name: "Petrify Limb",
    level: 5,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, F (a pebble from a petrified creature)",
    duration: "1 round/level",
    description: "You attempt to turn one of the target's limbs to stone. If an arm is petrified, the creature drops anything held in that hand and takes a -4 penalty to Dexterity. If a leg is petrified, the creature's movement speed is reduced to 5 feet, and it falls prone.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "magnetize-field": {
    name: "Magnetize Field",
    level: 5,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a lodestone)",
    duration: "1 round/level",
    description: "You create a powerful magnetic field in a 20-foot radius. All creatures wearing significant metal armor within the area must make a Strength save or be pulled 10 feet towards the center of the effect each round. Attacks with metallic weapons take a -2 penalty.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "baleful-polymorph": {
    name: "Baleful Polymorph",
    level: 5,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a caterpillar cocoon)",
    duration: "Permanent",
    description: "You change a subject into a Small or smaller, harmless animal. The subject must make a Fortitude save to negate the transformation. If the save fails and a subsequent Will save also fails, the creature loses its extraordinary abilities and its Intelligence becomes 1.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "passwall": {
    name: "Passwall",
    level: 5,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a pinch of sesame)",
    duration: "1 hour/level",
    description: "You create a passage through wooden, plaster, or stone walls, but not through metal or other harder materials. The passage is 5 feet wide, 8 feet tall, and 10 feet deep.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "telekinesis": {
    name: "Telekinesis",
    level: 5,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Concentration, up to 1 round/level, or instantaneous; see text",
    description: "You move objects or creatures by concentrating on them.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "disintegrate": {
    name: "Disintegrate",
    level: 6,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M/DF (a lodestone and a pinch of dust)",
    duration: "Instantaneous",
    description: "A thin, green ray springs from your pointing finger.",
    classes: ["Wizard"]
  },
  "reverse-gravity": {
    name: "Reverse Gravity",
    level: 7,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M/DF (a lodestone and iron filings)",
    duration: "1 round/level",
    description: "This spell reverses gravity in an area, causing all unattached objects and creatures within that area to fall upward.",
    classes: ["Druid", "Wizard"]
  },
  "polymorph-any-object": {
    name: "Polymorph Any Object",
    level: 8,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M/DF (mercury, gum arabic, and smoke)",
    duration: "See text",
    description: "This spell functions like polymorph, except that it changes one object or creature into another.",
    classes: ["Wizard"]
  },
  "shapechange": {
    name: "Shapechange",
    level: 9,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, F (a jade circlet worth at least 1,500 gp)",
    duration: "10 min./level",
    description: "This spell functions like polymorph, except that it enables you to assume the form of any single nonunique creature.",
    classes: ["Druid", "Wizard"]
  },
  "elemental-rebind": {
    name: "Elemental Rebind",
    level: 6,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a vial containing samples of two different elements)",
    duration: "1 minute/level",
    description: "You alter the elemental composition of a creature or object. You can change one energy type to another (fire to cold, electricity to acid, etc.). This affects the target's resistances, immunities, and energy-based attacks for the duration.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "earthstep": {
    name: "Earthstep",
    level: 6,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a handful of earth from two different locations)",
    duration: "1 round/level",
    description: "You can step into any natural earth or stone surface and emerge from another such surface within 1 mile. This movement is instantaneous and does not provoke attacks of opportunity.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "metaburst": {
    name: "Metaburst",
    level: 6,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a crystal worth 500 gp)",
    duration: "1 minute/level",
    description: "The target's metabolism accelerates dramatically. They gain fast healing 5, +4 to all physical ability scores, but must consume twice as much food and water, and age 1 day for every hour the spell is active.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "displace-structure": {
    name: "Displace Structure",
    level: 6,
    school: "Transmutation",
    castingTime: "1 minute",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (architectural plans worth 1000 gp)",
    duration: "Permanent",
    description: "You can move a building or structure up to 100 feet in any direction. The structure must be no larger than a 60-foot cube. The movement is gradual and does not damage the structure or its contents.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "flesh-to-stone": {
    name: "Flesh to Stone",
    level: 6,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (lime, water, and earth)",
    duration: "Instantaneous",
    description: "The subject, along with all its carried gear, turns into a mindless, inert statue. If the statue resulting from this spell is broken or damaged, the subject (if ever returned to flesh) has similar damage or deformities.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior", "stone-to-flesh", "Stone to Flesh", "Transmutation", "1 action", "Medium (100 ft. + 10 ft./level)", "V, S, M (a pinch of earth and a drop of blood)", "Instantaneous", "This spell restores a petrified creature to its normal state, restoring life and goods. The creature must make a DC 15 Fortitude save to survive the process. Failure means the creature dies."]
  },
  "metal-to-glass": {
    name: "Metal to Glass",
    level: 7,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a piece of glass and metal)",
    duration: "Permanent",
    description: "You transform metal objects into glass. The glass retains the shape and general properties of the original metal but becomes fragile. Weapons and armor made of glass have half their normal hardness and hit points.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "titanic-grip": {
    name: "Titanic Grip",
    level: 7,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a giant's fingernail)",
    duration: "1 minute/level",
    description: "The target's size increases by one category, and their Strength increases by +8. They can wield weapons as if they were one size category smaller and deal additional damage based on their increased size.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "flash-freeze": {
    name: "Flash Freeze",
    level: 7,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a vial of liquid nitrogen)",
    duration: "Instantaneous",
    description: "You instantly freeze a 40-foot radius area. All creatures and liquids in the area must make a Fortitude save or be frozen solid for 1d4 rounds. The area becomes difficult terrain covered in ice.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "transmute-being": {
    name: "Transmute Being",
    level: 7,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (essence of the target creature type worth 2000 gp)",
    duration: "Permanent",
    description: "You permanently change a creature's type (humanoid to construct, animal to magical beast, etc.). The creature retains its memories and personality but gains the traits of its new type.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "statue": {
    name: "Statue",
    level: 7,
    school: "Transmutation",
    castingTime: "1 round",
    range: "Touch",
    components: "V, S, M (powdered diamond and opal worth 5,000 gp)",
    duration: "1 hour/level",
    description: "The subject can become a statue at will. While in statue form, the subject is aware of its surroundings, has damage reduction 8/-, and is immune to most spells. It cannot move or take actions.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "control-weather": {
    name: "Control Weather",
    level: 7,
    school: "Transmutation",
    castingTime: "10 minutes",
    range: "2 miles",
    components: "V, S",
    duration: "4d12 hours",
    description: "You change the weather in the local area. You can call forth weather appropriate to the climate and season of the area you are in.",
    classes: ["Cleric", "Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "molecular-destabilization": {
    name: "Molecular Destabilization",
    level: 8,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a vial of acid worth 1000 gp)",
    duration: "Instantaneous",
    description: "You cause the molecular bonds of a target to become unstable. The target takes 15d6 points of damage as their body begins to dissolve. A successful Fortitude save reduces the damage by half.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "shifting-fortress": {
    name: "Shifting Fortress",
    level: 8,
    school: "Transmutation",
    castingTime: "1 hour",
    range: "Touch",
    components: "V, S, M (architectural plans and rare materials worth 10,000 gp)",
    duration: "Permanent",
    description: "You transform a building into a mobile fortress. The structure gains the ability to move at a speed of 30 feet and can change its configuration. It gains defensive capabilities and can house up to 100 people.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "deep-crust-spike": {
    name: "Deep Crust Spike",
    level: 8,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a diamond worth 5000 gp)",
    duration: "Instantaneous",
    description: "You cause a massive spike of stone to erupt from deep within the earth. The spike is 10 feet wide and 100 feet tall, dealing 20d6 damage to anything in its path. The spike remains as a permanent terrain feature.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "perfect-form": {
    name: "Perfect Form",
    level: 8,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a perfect gem worth 25,000 gp)",
    duration: "24 hours",
    description: "The target's body becomes a perfect version of itself. All ability scores become 20, they gain immunity to disease and poison, and regeneration 10. They also gain a +10 enhancement bonus to all skills.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "iron-body": {
    name: "Iron Body",
    level: 8,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a piece of iron that once was part of either a weapon that has killed or armor that has been worn by a hero)",
    duration: "1 min./level",
    description: "Your body becomes living iron. You gain damage reduction 15/adamantine, immunity to blindness, critical hits, ability score damage, deafness, disease, drowning, electricity, poison, stunning, and all spells or attacks that affect your physiology or respiration.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "temporal-stasis": {
    name: "Temporal Stasis",
    level: 8,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (powdered diamond, emerald, ruby, and sapphire worth 5,000 gp each)",
    duration: "Permanent",
    description: "You place the subject into a state of suspended animation. For the creature, time ceases to flow and its condition becomes fixed. The creature does not grow older. Its body functions virtually cease, and no force or effect can harm it.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior", "transmute-flesh-to-energy", "Transmute Flesh to Energy", "Transmutation", "1 action", "Touch", "V, S, M (a prism worth 10,000 gp)", "Permanent", "You transform a living creature into pure energy. The creature becomes an energy being, gaining immunity to physical damage but vulnerability to dispelling effects. They can pass through solid matter and manipulate energy directly."]
  },
  "timeless-form": {
    name: "Timeless Form",
    level: 9,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (an hourglass filled with sand from the Plane of Time worth 50,000 gp)",
    duration: "Permanent",
    description: "The target becomes immune to aging, disease, and the passage of time. They no longer need to eat, drink, or breathe. They gain immunity to time-based effects and can exist indefinitely without change.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "reverse-gravity-field": {
    name: "Reverse Gravity Field",
    level: 9,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a lodestone and iron filings worth 10,000 gp)",
    duration: "1 round/level",
    description: "You create a field where gravity is reversed in a 100-foot radius. All creatures and objects fall upward at normal falling speed. You can designate certain areas within the field to have normal gravity.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "eternal-anvil": {
    name: "Eternal Anvil",
    level: 9,
    school: "Transmutation",
    castingTime: "1 hour",
    range: "Touch",
    components: "V, S, M (an anvil made of adamantine worth 100,000 gp)",
    duration: "Permanent",
    description: "You create a magical anvil that can forge items from pure thought and energy. The anvil can create any non-magical item instantly and can enhance magical items beyond normal limits.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "matter-conversion": {
    name: "Matter Conversion",
    level: 9,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (samples of both materials worth 25,000 gp total)",
    duration: "Permanent",
    description: "You can convert any type of matter into any other type of matter. You can turn lead into gold, stone into water, or air into solid matter. The conversion affects up to 1000 cubic feet of material.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "elemental-shell": {
    name: "Elemental Shell",
    level: 9,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (essences of all four elements worth 50,000 gp)",
    duration: "1 hour/level",
    description: "You become a being of pure elemental energy. You gain immunity to all four basic elements, can assume any elemental form at will, and can manipulate elemental forces within a 1-mile radius.",
    classes: ["Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "body-to-void": {
    name: "Body to Void",
    level: 9,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a sphere of annihilation)",
    duration: "Permanent",
    description: "You transform the target into a living void. They become incorporeal, immune to all physical effects, and can pass through any barrier. They can only be affected by force effects and specific void-affecting magic.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "reality-anchor": {
    name: "Reality Anchor",
    level: 9,
    school: "Transmutation",
    castingTime: "1 minute",
    range: "1 mile",
    components: "V, S, M (a perfect crystal worth 100,000 gp)",
    duration: "Permanent",
    description: "You anchor reality in a 1-mile radius, preventing any transmutation, teleportation, or reality-altering effects. The area becomes a zone of absolute stability where the laws of physics cannot be changed.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },

  // Additional Necromancy Spells
  "chill-touch": {
    name: "Chill Touch",
    level: 0,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "A touch from your hand, which glows with blue energy, disrupts the life force of living creatures.",
    classes: ["Wizard"]
  },
  "cause-fear": {
    name: "Cause Fear",
    level: 1,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1d4 rounds or 1 round; see text",
    description: "The affected creature becomes frightened.",
    classes: ["Bard", "Cleric", "Wizard"]
  },
  "false-life": {
    name: "False Life",
    level: 1,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a small amount of alcohol or distilled spirits)",
    duration: "1 hour/level or until discharged; see text",
    description: "You harness the power of unlife to grant yourself a limited ability to avoid death.",
    classes: ["Wizard"]
  },
  "ghoul-touch": {
    name: "Ghoul Touch",
    level: 2,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (small leather glove dusted with grave dirt)",
    duration: "1d6+2 rounds",
    description: "Imbuing you with negative energy, this spell allows you to paralyze a single living humanoid for the duration of the spell with a successful melee touch attack.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief", "vampiric-touch", "Vampiric Touch", "Necromancy", "1 action", "Touch", "V, S", "Instantaneous", "You must make a melee touch attack. Your touch deals 1d6 points of damage per two caster levels (maximum 10d6).", "enervation", "Enervation", "Close (25 ft. + 5 ft./2 levels)", "You point your finger and utter the incantation, releasing a black ray of crackling negative energy that suppresses the life force of any living creature it strikes."]
  },
  "blight": {
    name: "Blight",
    level: 4,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "Instantaneous",
    description: "This spell withers a single plant of any size.",
    classes: ["Druid", "Wizard", "Cleric", "Crimson Agent", "Shaman", "Thief", "magic-jar", "Magic Jar", "Necromancy", "1 action", "Medium (100 ft. + 10 ft./level)", "V, S, F (a gem or crystal worth at least 100 gp)", "1 hour/level or until you return to your body", "By casting magic jar, you place your soul in a gem or large crystal (known as the magic jar), leaving your body lifeless."]
  },
  "circle-of-death": {
    name: "Circle of Death",
    level: 6,
    school: "Necromancy",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (the powder of a crushed black pearl worth at least 500 gp)",
    duration: "Instantaneous",
    description: "A circle of death snuffs out the life force of living creatures, killing them instantly.",
    classes: ["Wizard", "Cleric", "Crimson Agent", "Druid", "Shaman", "Thief", "control-undead", "Control Undead", "Necromancy", "1 action", "Close (25 ft. + 5 ft./2 levels)", "V, S, M (a shred of raw meat and a splinter of bone)", "1 min./level", "This spell enables you to command undead creatures for a short period of time.", "horrid-wilting", "Horrid Wilting", "Long (400 ft. + 40 ft./level)", "V, S, M/DF (a bit of sponge)", "Instantaneous", "This spell evaporates moisture from the body of each subject living creature, dealing 1d6 points of damage per caster level (maximum 20d6).", "energy-drain", "Energy Drain", "V, S", "You point your finger and utter the incantation, releasing a black ray of crackling negative energy that suppresses the life force of any living creature it strikes."]
  },

  // Additional Level 8 Necromancy Spells
  "summon-bone-titan": {
    name: "Summon Bone Titan",
    level: 8,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (the skull of a giant and a black diamond worth 5,000 gp)",
    duration: "10 min./level (D)",
    description: "You summon a colossal skeletal titan from the bones of ancient giants. The Bone Titan is a Huge undead creature with 300 HP, AC 28, and devastating attacks. It has two slam attacks (3d8+15 bludgeoning plus 2d8 necrotic) and can trample enemies. The titan has DR 20/bludgeoning and good, spell resistance 25, and an aura of fear (60-foot radius, Will DC 20 + Cha mod or become frightened for 1d6 rounds).",
    classes: ["Cleric", "Wizard"]
  },
  "necrotic-apocalypse": {
    name: "Necrotic Apocalypse",
    level: 8,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a vial of lich dust and a meteorite fragment)",
    duration: "Instantaneous",
    description: "You unleash a devastating wave of necrotic energy across a vast area. All living creatures within a 100-foot radius take 12d8 points of necrotic damage (Fortitude save for half). Creatures that die from this spell rise as zombies under your control 1 round later. The area becomes cursed ground for 24 hours, causing all healing effects to be reduced by half.",
    classes: ["Cleric", "Sorcerer", "Wizard"]
  },
  "soul-explosion": {
    name: "Soul Explosion",
    level: 8,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (one corpse)",
    duration: "Instantaneous",
    description: "You target a single corpse within range, causing it to erupt in a violent explosion of soul-fueled fire and necrotic energy. All creatures within a 20-foot radius of the exploding corpse take 8d6 points of fire damage and 8d6 points of necrotic damage (Reflex save for half of both types of damage). The targeted corpse is utterly consumed in the process.",
    classes: ["Cleric", "Sorcerer", "Wizard"]
  },
  "flesh-to-grave": {
    name: "Flesh to Grave",
    level: 8,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, F (a shriveled heart)",
    duration: "Instantaneous (death); Permanent (undead)",
    description: "You attempt to snuff out a creature's life and raise it as an undead servant. The target must have 100 hit points or fewer. The target must make a Fortitude save. If it fails, it dies instantly. One round later, its body rises as a zombie under your permanent control (as if created by animate dead). You can control a maximum number of HD of undead from this spell equal to your caster level; any excess become uncontrolled. If the target succeeds on its Fortitude save, it instead takes 6d6 points of necrotic damage.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "create-greater-undead": {
    name: "Create Greater Undead",
    level: 8,
    school: "Necromancy",
    castingTime: "1 hour",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a black onyx gem worth 100 gp per HD of the undead to be created, and the corpse of the appropriate type)",
    duration: "Instantaneous",
    description: "You create a more powerful type of undead. You can create a ghast, mummy, mohrg, spectre, or wight from a suitable corpse. The type of undead you can create depends on your caster level (Ghast CL 9th, Wight CL 11th, Spectre CL 13th, Mummy CL 15th, Mohrg CL 17th). The created undead is under your command and remains so until destroyed or released. You can control a maximum of 2 HD of undead per caster level created by this spell or animate dead. Exceeding this limit causes excess undead to become uncontrolled.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Additional Level 9 Necromancy Spells
  "summon-avatar-of-decay": {
    name: "Summon Avatar of Decay",
    level: 9,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a lich's heart, or a specially prepared heart from a powerful evil outsider, and a black opal worth 10,000 gp)",
    duration: "10 min./level (D)",
    description: "You summon an Avatar of Decay, a terrifying Huge undead entity that embodies rot and unlife. It appears where you designate and acts immediately, on your turn. It is intelligent and can command other undead creatures of lesser power (up to 20 HD total) within 60 feet as a free action if you direct it. The Avatar of Decay has 250 HP, AC 25 (natural armor, unholy protection), and makes three attacks per round: two slams (2d10+10 bludgeoning plus 2d6 necrotic) and one bite (2d8+5 piercing plus Constitution drain 1d4). It has an Aura of Rot (living creatures within 30 feet take 2d6 necrotic damage per round, Fortitude DC 22 + Cha mod half). It has DR 15/good and epic, spell resistance 30, regeneration 10 (acid or fire), and standard undead traits.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "doom-greater": {
    name: "Doom (Greater)",
    level: 9,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, F (an effigy of the target inscribed with its name, which is consumed)",
    duration: "5 rounds (see text)",
    description: "You pronounce a dire curse of inevitable doom upon a creature. The target must make a Fortitude save. If it fails, it is afflicted by a creeping doom. For the next 5 rounds, at the start of each of its turns, the target takes 2d6 points of unholy damage (this damage bypasses most resistances and immunities) and cannot regain hit points or be healed by any means. If the target is reduced to 0 hit points while under the effect of this spell, it dies and its soul is trapped, preventing resurrection by any means short of a miracle or wish spell. If the target survives the 5 rounds, the curse ends, but it is exhausted.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "soul-harvest": {
    name: "Soul Harvest",
    level: 9,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "60-ft.-radius burst centered on you",
    components: "V, S",
    duration: "Instantaneous",
    description: "You unleash a terrifying vortex of necrotic energy that rips at the souls of your enemies. All living enemies within a 60-foot radius take 10d8 points of necrotic damage (Fortitude save for half). You absorb a portion of the stolen life force, regaining hit points equal to one-quarter of the total necrotic damage dealt to all targets (up to your maximum hit points). Additionally, for each enemy slain by this spell, you gain a +1 profane bonus to attack rolls, damage rolls, and saving throws for 1 minute (maximum +5 bonus).",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "unholy-ascendance": {
    name: "Unholy Ascendance",
    level: 9,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S, M (a vial of blood from a vampire and a lich's finger bone)",
    duration: "1 minute/level (D)",
    description: "You transform into a powerful demi-lich like creature, gaining significant undead traits and powers. Your type changes to Undead for the duration. You gain DR 15/good and bludgeoning, immunity to cold, electricity, mind-affecting effects, paralysis, poison, sleep, and stunning. You gain a fly speed of 60 feet (perfect). Your touch attacks deal an additional 2d8 negative energy damage. All your necromancy spells are cast as if with the Empower Spell feat without increasing their spell level or casting time. You do not need to breathe, eat, or sleep. When the spell ends, you are exhausted.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "field-of-endless-dead": {
    name: "Field of Endless Dead",
    level: 9,
    school: "Necromancy",
    castingTime: "10 minutes",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a black onyx gem worth 50 gp for each skeleton or zombie to be created, and a large number of corpses)",
    duration: "Instantaneous (see text)",
    description: "This spell functions like animate dead, but you can animate up to eight humanoid corpses as skeletons or zombies. These undead are under your permanent control until destroyed. You can control a total number of HD of undead from this spell and other animation spells equal to 4 x your caster level. Any excess become uncontrolled. This spell requires a significant number of available corpses in the target area.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "final-word": {
    name: "Final Word",
    level: 9,
    school: "Necromancy",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "Instantaneous",
    description: "You utter a single, potent word of unmaking. If the target creature has 50 hit points or fewer, it must make a Fortitude save. If it fails, it dies instantly. If the creature dies from this spell, you capture a fragment of its soul, which you can use once within the next hour to recall and cast any one spell of 5th level or lower that you know and have already expended today, without expending a spell slot. If the target succeeds on its save, it is instead stunned for 1 round.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "phantom-armageddon": {
    name: "Phantom Armageddon",
    level: 9,
    school: "Necromancy",
    castingTime: "1 Round",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, F (a shard from a tombstone struck by lightning)",
    duration: "Instantaneous",
    description: "You create a horrifying illusion of an apocalyptic event intertwined with waves of pure necrotic energy. All enemies in a 60-foot radius must make a Will save to disbelieve the illusionary component (e.g., skies raining blood, the ground opening to fiery pits, colossal skeletal figures). Regardless of the Will save, all enemies in the area take 12d8 points of necrotic damage (Fortitude save for half). Those who fail the Will save to disbelieve the illusion are also panicked for 1d4 rounds.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "eternal-pact": {
    name: "Eternal Pact",
    level: 9,
    school: "Necromancy",
    castingTime: "1 hour",
    range: "Personal",
    components: "V, S, M (a diamond worth 25,000 gp, which is consumed, and a ritual involving your own blood)",
    duration: "Contingent (see text)",
    description: "You forge a pact with the forces of undeath, ensuring your return from the brink. The next time you would be killed (reduced to -10 hit points or equivalent, or by a death effect), this spell triggers. You instead fall to 1 hit point, and all your expended spell slots of 8th level and lower are instantly refreshed. This effect occurs once, and then the spell is discharged. This spell does not protect against effects that utterly destroy the body or trap the soul in such a way that it cannot return to the body.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },

  // Additional Universal Spells


  "magic-weapon": {
    name: "Magic Weapon",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "1 min./level",
    description: "Magic weapon gives a weapon a +1 enhancement bonus on attack and damage rolls.",
    classes: ["Cleric", "Paladin", "Wizard"]
  },
  "arcane-lock": {
    name: "Arcane Lock",
    level: 2,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (gold dust worth 25 gp)",
    duration: "Permanent",
    description: "An arcane lock spell cast upon a door, chest, or portal magically locks it.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior", "magic-weapon-greater", "Magic Weapon, Greater", "Transmutation", "1 action", "Close (25 ft. + 5 ft./2 levels)", "V, S, M/DF (powdered lime and carbon)", "1 hour/level", "This spell functions like magic weapon, except that it gives a weapon an enhancement bonus on attack and damage rolls of +1 per four caster levels (maximum +5).", "Druid", "Monk"]
  },

  // Additional Druid Spells
  "animal-friendship": {
    name: "Animal Friendship",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a morsel of food)",
    duration: "24 hours",
    description: "This spell allows you to convince a beast that you mean it no harm.",
    classes: ["Druid", "Ranger"]
  },
  "speak-with-animals": {
    name: "Speak with Animals",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 min./level",
    description: "You can ask questions of and receive answers from animals.",
    classes: ["Bard", "Druid", "Ranger"]
  },
  "goodberry": {
    name: "Goodberry",
    level: 1,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a sprig of mistletoe)",
    duration: "1 day/level",
    description: "Casting goodberry upon a handful of freshly picked berries makes 2d4 of them magical.",
    classes: ["Druid"]
  },
  "heat-metal": {
    name: "Heat Metal",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, DF",
    duration: "7 rounds",
    description: "Heat metal makes metal extremely warm.",
    classes: ["Druid"]
  },
  "warp-wood": {
    name: "Warp Wood",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You cause wood to bend and warp, permanently destroying its straightness, form, and strength.",
    classes: ["Druid"]
  },
  "plant-growth": {
    name: "Plant Growth",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "See text",
    components: "V, S, DF",
    duration: "Instantaneous",
    description: "Plant growth has different effects depending on the version chosen.",
    classes: ["Druid", "Ranger"]
  },
  "stone-shape": {
    name: "Stone Shape",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (soft clay)",
    duration: "Instantaneous",
    description: "You can form an existing piece of stone into any shape that suits your purpose.",
    classes: ["Cleric", "Druid", "Wizard", "Dragoon", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior", "ice-storm", "Ice Storm", "Evocation", "1 action", "Long (400 ft. + 40 ft./level)", "V, S, M/DF (a pinch of dust and a few drops of water)", "1 full round", "Great magical hailstones pound down for 1 full round in a cylinder 40 feet across and 20 feet high."]
  },
  "wall-of-thorns": {
    name: "Wall of Thorns",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "10 min./level",
    description: "A wall of thorns spell creates a barrier of very tough, pliable, tangled brush bearing needle-sharp thorns as long as a human's finger.",
    classes: ["Druid"]
  },
  "transport-via-plants": {
    name: "Transport via Plants",
    level: 6,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Unlimited",
    components: "V, S",
    duration: "1 round",
    description: "You can enter any normal plant (equal to your size or larger) and pass any distance to a plant of the same kind in a single round.",
    classes: ["Druid"]
  },
  "changestaff": {
    name: "Changestaff",
    level: 7,
    school: "Transmutation",
    castingTime: "1 round",
    range: "Touch",
    components: "V, S, F (a quarterstaff that has never been used as a weapon)",
    duration: "1 hour/level",
    description: "You change a specially prepared quarterstaff into a Huge treant-like creature.",
    classes: ["Druid"]
  },
  "earthquake": {
    name: "Earthquake",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, DF",
    duration: "1 round",
    description: "When you cast earthquake, an intense but highly localized tremor rips the ground.",
    classes: ["Cleric", "Druid"]
  },
  "storm-of-vengeance": {
    name: "Storm of Vengeance",
    level: 9,
    school: "Conjuration",
    castingTime: "1 round",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Concentration (maximum 10 rounds)",
    description: "This spell creates an enormous black storm cloud.",
    classes: ["Cleric", "Druid"]
  },

  // Additional Paladin Spells
  "detect-evil": {
    name: "Detect Evil",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "60 ft.",
    components: "V, S, DF",
    duration: "Concentration, up to 10 min./level",
    description: "You can sense the presence of evil.",
    classes: ["Cleric", "Paladin"]
  },
  "divine-favor": {
    name: "Divine Favor",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, DF",
    duration: "1 minute",
    description: "Calling upon the strength and wisdom of a deity, you gain a +1 luck bonus on attack and weapon damage rolls for every three caster levels you have.",
    classes: ["Paladin"]
  },
  "bulls-strength": {
    name: "Bull's Strength",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (a few hairs, or a pinch of dung, from a bull)",
    duration: "1 min./level",
    description: "The subject becomes stronger. The spell grants a +4 enhancement bonus to Strength.",
    classes: ["Cleric", "Druid", "Paladin", "Wizard"]
  },
  "remove-disease": {
    name: "Remove Disease",
    level: 3,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "Remove disease cures all diseases that the subject is suffering from.",
    classes: ["Cleric", "Druid", "Paladin"]
  },
  "neutralize-poison": {
    name: "Neutralize Poison",
    level: 4,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M/DF (charcoal)",
    duration: "Instantaneous",
    description: "You detoxify any sort of venom in the creature or object touched.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger"]
  },

  // Additional Ranger Spells
  "detect-animals-or-plants": {
    name: "Detect Animals or Plants",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Concentration, up to 10 min./level",
    description: "You can detect a particular kind of animal or plant in a cone emanating out from you in whatever direction you face.",
    classes: ["Druid", "Ranger"]
  },
  "resist-energy": {
    name: "Resist Energy",
    level: 2,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "10 min./level",
    description: "This abjuration grants a creature limited protection from damage of whichever one of five energy types you select.",
    classes: ["Cleric", "Druid", "Paladin", "Ranger", "Wizard", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "water-walk": {
    name: "Water Walk",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, DF",
    duration: "10 min./level",
    description: "The transmuted creatures can tread on any liquid as if it were firm ground.",
    classes: ["Cleric", "Ranger"]
  },
  "tree-stride": {
    name: "Tree Stride",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, DF",
    duration: "1 hour/level or until expended; see text",
    description: "You gain the ability to enter trees and move from inside one tree to inside another tree.",
    classes: ["Druid", "Ranger"]
  },

  // Additional Bard Spells
  "cure-light-wounds": {
    name: "Cure Light Wounds",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "When laying your hand upon a living creature, you channel positive energy that cures 1d8 points of damage +1 point per caster level (maximum +5).",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger"]
  },
  "lesser-restoration": {
    name: "Lesser Restoration",
    level: 2,
    school: "Conjuration",
    castingTime: "3 rounds",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "Lesser restoration dispels any magical effects reducing one of the subject's ability scores or cures 1d4 points of temporary ability damage to one of the subject's ability scores.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger"]
  },
  "cure-serious-wounds": {
    name: "Cure Serious Wounds",
    level: 3,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like cure light wounds, except that it cures 3d8 points of damage +1 point per caster level (maximum +15).",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Ranger"]
  },
  "zone-of-silence": {
    name: "Zone of Silence",
    level: 4,
    school: "Illusion",
    castingTime: "1 round",
    range: "Personal",
    components: "V, S",
    duration: "1 hour/level",
    description: "By casting zone of silence, you manipulate sound waves in your immediate vicinity so that you and those within the spell's area can converse normally, yet no one outside can hear your voices or any other sounds from within.",
    classes: ["Bard"]
  },
  "greater-heroism": {
    name: "Greater Heroism",
    level: 5,
    school: "Enchantment",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 min./level",
    description: "This spell functions like heroism, except the creature gains a +4 morale bonus on attack rolls, saves, and skill checks, immunity to fear effects, and temporary hit points equal to your caster level.",
    classes: ["Bard", "Wizard"]
  },
  "mass-cure-light-wounds": {
    name: "Mass Cure Light Wounds",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like cure light wounds, except that it affects multiple creatures.",
    classes: ["Bard", "Cleric", "Druid"]
  },

  // Additional Wizard Spells
  "magic-aura": {
    name: "Magic Aura",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, F (a small square of silk that must be passed over the object that receives the aura)",
    duration: "1 day/level",
    description: "You alter an item's aura so that it registers to detect spells (and spells with similar capabilities) as though it were nonmagical, or a magic item of a kind you specify, or the subject of a spell you specify.",
    classes: ["Bard", "Wizard"]
  },
  "rope-trick": {
    name: "Rope Trick",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (powdered corn extract and a twisted loop of parchment)",
    duration: "1 hour/level",
    description: "When this spell is cast upon a piece of rope from 5 to 30 feet long, one end of the rope rises into the air until the whole rope hangs perpendicular to the ground, as if affixed at the top to an invisible support.",
    classes: ["Wizard"]
  },
  "phantom-steed": {
    name: "Phantom Steed",
    level: 3,
    school: "Conjuration",
    castingTime: "10 minutes",
    range: "0 ft.",
    components: "V, S",
    duration: "1 hour/level",
    description: "You conjure a Large, quasi-real, horselike creature.",
    classes: ["Bard", "Wizard"]
  },
  "locate-creature": {
    name: "Locate Creature",
    level: 4,
    school: "Divination",
    castingTime: "1 action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S, M (a bit of fur from a bloodhound)",
    duration: "10 min./level",
    description: "This spell functions like locate object, except this spell locates a known or familiar creature.",
    classes: ["Bard", "Wizard"]
  },
  "passwall": {
    name: "Passwall",
    level: 5,
    school: "Transmutation",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (sesame seeds)",
    duration: "1 hour/level",
    description: "You create a passage through wooden, plaster, or stone walls, but not through metal or other harder materials.",
    classes: ["Wizard", "Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior", "guards-and-wards", "Guards and Wards", "Abjuration", "30 minutes", "Anywhere within the area to be warded", "V, S, M (burning incense, a small measure of brimstone and oil, a knotted string, and a small amount of blood), F (a small silver rod)", "2 hours/level", "This powerful spell is primarily used to defend a stronghold or fortress by creating a number of magical wards and effects."]
  },
  "limited-wish": {
    name: "Limited Wish",
    level: 7,
    school: "Universal",
    castingTime: "1 action",
    range: "See text",
    components: "V, S, XP (300 XP)",
    duration: "See text",
    description: "A limited wish lets you create nearly any type of effect.",
    classes: ["Wizard"]
  },

  // Expanded Universal Spells - Level 0
  "mage-light": {
    name: "Mage Light",
    level: 0,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, M (a firefly or a piece of phosphorescent moss)",
    duration: "10 min./level (D)",
    description: "This spell causes an object to glow like a torch, shedding bright light in a 20-foot radius and increasing the light level for an additional 20 feet by one step. The effect is immobile, but it can be cast on a movable object. Light taken into an area of magical darkness does not function.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "arcane-tether-universal": {
    name: "Arcane Tether",
    level: 0,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S",
    duration: "10 min./level (D)",
    description: "You create a faint arcane link between yourself and a target object or willing creature. For the duration, you have a vague sense of the target's direction and general distance from you. The tether provides no information about the target's condition or surroundings. If the target moves to another plane, the tether is broken.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "glyph-trace-universal": {
    name: "Glyph Trace",
    level: 0,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Concentration, up to 1 min./level",
    description: "You cause any magical runes, sigils, glyphs, or similar magical writings to faintly glow, becoming more visible. This spell gives you a +5 circumstance bonus on Perception checks made to find magical traps or writings.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "momentary-pause": {
    name: "Momentary Pause",
    level: 0,
    school: "Universal",
    castingTime: "See text (often a Free Action before initiative is rolled)",
    range: "Personal",
    components: "S",
    duration: "Instantaneous",
    description: "You briefly attune yourself to the flow of combat. If you and one or more other creatures roll the same initiative result, you act before them. This spell is typically cast as a free action immediately before initiative is rolled.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "spectral-quill": {
    name: "Spectral Quill",
    level: 0,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "10 minutes/level",
    description: "You create a translucent, floating quill that can write at your mental command. The quill can write up to one page per minute and follows simple instructions like 'copy this text' or 'take dictation.' It uses any ink and paper you provide.",
    classes: ["Bard", "Cleric", "Sorcerer", "Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "cantrip-echo": {
    name: "Cantrip Echo",
    level: 0,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S",
    duration: "1 round/level",
    description: "The next cantrip (0-level spell) you cast within the duration is automatically repeated at the start of your next turn, targeting the same target(s) if possible. If the original target is no longer valid, the echo fizzles harmlessly.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "magical-ping": {
    name: "Magical Ping",
    level: 0,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You send out a brief magical pulse that reveals the presence and general location of magical auras within range. You learn the number of magical auras present and their approximate directions, but not their specific nature or strength.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "spellshift": {
    name: "Spellshift",
    level: 1,
    school: "Universal",
    castingTime: "1 Swift Action",
    range: "Personal",
    components: "V",
    duration: "Until the end of your next turn",
    description: "When you cast this spell, you can alter the energy type of the next spell you cast before the end of your next turn that deals acid, cold, electricity, fire, or sonic damage.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "ritual-anchor": {
    name: "Ritual Anchor",
    level: 1,
    school: "Universal",
    castingTime: "10 minutes",
    range: "Touch",
    components: "V, S, M (a silver pin and incense worth 10 gp)",
    duration: "24 hours",
    description: "You create an arcane anchor point at a specific location. For the next 24 hours, ritual effects you perform can manifest at the anchored location if you can see it.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "mana-tether": {
    name: "Mana Tether",
    level: 1,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S",
    duration: "1 hour/level",
    description: "You create a magical connection with a willing spellcaster. While within 30 feet of each other, you can share spell slots of the same level, allowing one caster to use the other's expended slots.",
    classes: ["Bard", "Cleric", "Sorcerer", "Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "delay-spell": {
    name: "Delay Spell",
    level: 1,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S",
    duration: "1 round/level or until discharged",
    description: "The next spell you cast of 3rd level or lower is held in magical suspension and can be released as a free action on any subsequent turn within the duration.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "flare-sigil": {
    name: "Flare Sigil",
    level: 1,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 hour/level or until triggered",
    description: "You place an invisible magical sigil on a surface. When a creature comes within 5 feet, the sigil flares with bright light, illuminating a 20-foot radius and potentially blinding creatures for 1 round (Will save negates).",
    classes: ["Bard", "Cleric", "Sorcerer", "Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "quick-cast": {
    name: "Quick Cast",
    level: 1,
    school: "Universal",
    castingTime: "1 Swift Action",
    range: "Personal",
    components: "V",
    duration: "Instantaneous",
    description: "The next spell you cast this round with a casting time of 1 standard action can be cast as a move action instead. This spell can only be used once per round.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Expanded Universal Spells - Level 2
  "arcane-portal": {
    name: "Arcane Portal",
    level: 2,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a small mirror)",
    duration: "1 round/level",
    description: "You create two linked portals within range. Creatures and objects can pass through one portal and emerge from the other. Each portal is 5 feet in diameter and can be placed on any solid surface.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "spell-mirror": {
    name: "Spell Mirror",
    level: 2,
    school: "Universal",
    castingTime: "1 Immediate Action",
    range: "Personal",
    components: "V, S",
    duration: "Instantaneous",
    description: "When targeted by a spell of 2nd level or lower, you can reflect it back at the caster. Make a caster level check (1d20 + caster level) against the original spell's DC. If successful, the spell affects the original caster instead.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "thread-tap": {
    name: "Thread Tap",
    level: 2,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "You tap into the magical threads of a spell effect, gaining insight into its nature. You learn the spell's level, school, caster level, and remaining duration. If you beat the original caster's level by 5 or more, you also learn how to dispel it most effectively.",
    classes: ["Bard", "Cleric", "Wizard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "echo-cast": {
    name: "Echo Cast",
    level: 2,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S",
    duration: "1 round/level",
    description: "The next spell you cast of 1st level or lower creates an echo that repeats the spell on the following round, targeting the same target(s) if possible. The echo uses your caster level and save DCs from when you cast this spell.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Expanded Universal Spells - Level 3
  "blink-step": {
    name: "Blink Step",
    level: 3,
    school: "Universal",
    castingTime: "1 Move Action",
    range: "Personal",
    components: "V",
    duration: "Instantaneous",
    description: "You instantly teleport up to 30 feet to any location you can see. This movement does not provoke attacks of opportunity and can be used in place of your normal movement.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "unravel-spell": {
    name: "Unravel Spell (Dispel Magic)",
    level: 3,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You can end ongoing spells that have been cast on a creature or object, temporarily suppress the magical abilities of a magic item, or counter another spellcaster's spell. A dispelled spell ends as if its duration had expired.",
    classes: ["Bard", "Cleric", "Druid", "Paladin", "Sorcerer", "Wizard", "Mage", "Mirrorsage", "Oracle", "Soldier", "Tinker", "Warrior"]
  },
  "spatial-fold": {
    name: "Spatial Fold",
    level: 3,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a folded piece of paper)",
    duration: "1 minute/level",
    description: "You fold space to bring two points closer together. Choose two locations within range; the distance between them is halved for the purpose of movement, spells, and ranged attacks. This creates a visible distortion in the air.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "mana-shield": {
    name: "Mana Shield",
    level: 3,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S",
    duration: "1 minute/level or until discharged",
    description: "You create a barrier of magical energy around yourself. When you take damage, you can spend a spell slot to reduce the damage by 1d6 per level of the spell slot expended (maximum 5d6).",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "haste-universal": {
    name: "Haste (Universal Variant)",
    level: 3,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a shaving of licorice root)",
    duration: "1 round/level",
    description: "The transmuted creature moves and acts more quickly than normal. This increase in speed has several effects: +1 bonus on attack rolls, +1 dodge bonus to AC and Reflex saves, and an additional move action each round.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Expanded Universal Spells - Level 4
  "spell-theft": {
    name: "Spell Theft",
    level: 4,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You steal a prepared spell or spell slot from a target spellcaster. Make a caster level check against the target's caster level + 10. If successful, you gain one of their prepared spells or spell slots of 3rd level or lower, and they lose it.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "time-skip": {
    name: "Time Skip",
    level: 4,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S, M (a small hourglass)",
    duration: "Instantaneous",
    description: "You skip forward in time by 1 round. You disappear from the current timeline and reappear at the start of your next turn, 1 round later. Any effects targeting you when you cast this spell are suspended until you return.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "arcane-reversal": {
    name: "Arcane Reversal",
    level: 4,
    school: "Universal",
    castingTime: "1 Immediate Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You reverse the effects of a spell cast within the last round. The spell's effects are undone as if it had never been cast, though spell slots and components are not recovered.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "mystic-gate": {
    name: "Mystic Gate (Dimension Door)",
    level: 4,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Long (400 ft. + 40 ft./level)",
    components: "V",
    duration: "Instantaneous",
    description: "You instantly transfer yourself from your current location to any other spot within range. You always arrive at exactly the spot desired. You can bring along objects and one willing creature of your size or smaller.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Expanded Universal Spells - Level 5
  "planar-gate": {
    name: "Planar Gate (Plane Shift)",
    level: 5,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S, F (a forked, metal rod attuned to the plane of travel)",
    duration: "Instantaneous",
    description: "You move yourself or some other creature to another plane of existence or alternate dimension. You can transport up to eight willing creatures, linking hands in a circle.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "quicken-cast": {
    name: "Quicken Cast",
    level: 5,
    school: "Universal",
    castingTime: "1 Free Action",
    range: "Personal",
    components: "V",
    duration: "Instantaneous",
    description: "The next spell you cast this round of 3rd level or lower is cast as a swift action instead of its normal casting time. This does not stack with other quickening effects.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "spell-seal": {
    name: "Spell Seal",
    level: 5,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a wax seal)",
    duration: "Permanent until triggered",
    description: "You seal a spell of 4th level or lower into an object or location. The spell activates when specific conditions you set are met. The sealed spell uses your caster level and save DCs when it activates.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "dimensional-shift": {
    name: "Dimensional Shift (Teleport)",
    level: 5,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal and touch",
    components: "V",
    duration: "Instantaneous",
    description: "This spell instantly transports you to a designated destination. Distance is not a factor, but interplanar travel is not possible. You can bring along objects and creatures up to your maximum load.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Expanded Universal Spells - Level 6
  "chrono-lock": {
    name: "Chrono Lock",
    level: 6,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a small clock)",
    duration: "1 round/level",
    description: "You lock a creature or object in temporal stasis. The target cannot move, act, or be affected by any spells or effects for the duration. The target is aware but helpless.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "rift-spiral": {
    name: "Rift Spiral",
    level: 6,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, M (a spiral shell)",
    duration: "1 round/level",
    description: "You create a swirling rift in space that pulls creatures and objects toward its center. Creatures within 30 feet must make a Strength save each round or be pulled 10 feet closer to the center.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "arcane-clone": {
    name: "Arcane Clone (Mislead)",
    level: 6,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "S",
    duration: "1 round/level (D)",
    description: "You become invisible and create an illusory double of yourself. The double appears where you were standing and can move and act as you direct, though it cannot attack or cast spells.",
    classes: ["Bard", "Sorcerer", "Wizard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "spell-sculptor": {
    name: "Spell Sculptor (Contingency)",
    level: 6,
    school: "Universal",
    castingTime: "At least 10 minutes",
    range: "Personal",
    components: "V, S, M (quicksilver, an eyelash from a hare, and a gem worth at least 1,500 gp), F (ivory statuette of you or the target, 1,500 gp)",
    duration: "1 day/level or until discharged (D)",
    description: "You can place another spell upon your person so that it comes into effect under some condition you dictate when casting contingency. The contingency spell and the companion spell are cast at the same time.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Expanded Universal Spells - Level 7
  "chain-gate": {
    name: "Chain Gate (Greater Teleport)",
    level: 7,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal or Touch",
    components: "V",
    duration: "Instantaneous",
    description: "This spell functions like teleport, except that there is no range limit and you do not need to see the destination. You must have at least a reliable description of the place to which you are teleporting.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "cast-echo": {
    name: "Cast Echo (Spell Turning)",
    level: 7,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S, M/DF (a small silver mirror)",
    duration: "10 min./level or until discharged (D)",
    description: "Spells and spell-like abilities that target you are turned back upon the original caster. The spell affects spells of 1st through 7th level. The exact number of spell levels turned is 1d4+6.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "erase-from-reality": {
    name: "Erase from Reality (Sequester)",
    level: 7,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Touch",
    components: "V, S, M (a powder composed of diamond, emerald, ruby, and sapphire dust, each worth 500 gp)",
    duration: "1 day/level (D)",
    description: "This spell makes a creature or object invisible to sight and scrying; it also cannot be detected by divination spells or clairsentience. The sequestered creature or object is effectively undetectable.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "meta-surge": {
    name: "Meta Surge (Limited Wish)",
    level: 7,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "See text",
    components: "V, S, XP (300 XP)",
    duration: "See text",
    description: "A limited wish lets you create nearly any type of effect. A limited wish can duplicate any sorcerer/wizard spell of 6th level or lower, or duplicate any other spell of 5th level or lower.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Expanded Universal Spells - Level 8
  "dimensional-break": {
    name: "Dimensional Break (Maze)",
    level: 8,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "See text (D)",
    description: "You banish the subject to an extradimensional labyrinth of force. Each round on its turn, the subject may attempt a DC 20 Intelligence check to escape the labyrinth as a full-round action.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "reality-patch": {
    name: "Reality Patch (Mind Blank)",
    level: 8,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "24 hours (D)",
    description: "The subject is protected from all devices and spells that detect, influence, or read emotions or thoughts. This spell protects against all mind-affecting spells and effects as well as information gathering by divination spells.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "time-echo": {
    name: "Time Echo (Temporal Acceleration)",
    level: 8,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S, M (a pinch of diamond dust worth 500 gp)",
    duration: "1 round/2 levels (see text) (D)",
    description: "You move and act incredibly fast. For the duration, you can take one extra standard action or move action during each of your turns. When the spell ends, you are fatigued for a period equal to the time you spent under the spell's effect.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Expanded Universal Spells - Level 9
  "absolute-gate": {
    name: "Absolute Gate (Gate)",
    level: 9,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S, XP (1,000 XP)",
    duration: "Concentration, up to 1 round/level (D)",
    description: "You create an interdimensional connection between your plane of existence and a plane you specify, allowing travel and the calling of creatures between the two planes.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "world-rewrite": {
    name: "World Rewrite (Wish)",
    level: 9,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "See text",
    components: "V, S, XP (5,000 XP or more, see text)",
    duration: "See text",
    description: "Wish is the mightiest spell a mortal creature can cast. By simply speaking aloud, you can alter reality to better suit you. A wish can produce any one of many effects.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "planar-collapse": {
    name: "Planar Collapse (Implosion)",
    level: 9,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Concentration, up to 4 rounds",
    description: "Each round you concentrate, you can choose one corporeal creature as a target and cause it to collapse in upon itself and be utterly destroyed. A creature targeted by implosion must make a Fortitude save.",
    classes: ["Cleric", "Sorcerer", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "perfect-spell": {
    name: "Perfect Spell (Maximize Spell)",
    level: 9,
    school: "Universal",
    castingTime: "1 Free Action",
    range: "Personal",
    components: "V",
    duration: "Instantaneous",
    description: "This spell allows you to cast another spell of 8th level or lower as if it were affected by the Maximize Spell feat, without increasing the spell's actual level or casting time.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "ritual-mastery": {
    name: "Ritual Mastery",
    level: 9,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Personal",
    components: "V, S, M (a page from a sacred text and incense worth 1,000 gp)",
    duration: "Instantaneous",
    description: "You instantly complete any one ritual that you know and are capable of performing, provided you have all necessary material components for that ritual on hand.",
    classes: ["Cleric", "Druid", "Wizard", "Bard", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "unmake-spell": {
    name: "Unmake Spell (Mage's Disjunction)",
    level: 9,
    school: "Universal",
    castingTime: "1 Standard Action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "All magical effects and magic items within the radius of the spell, except for those on your person, are disjoined. Spells and spell-like effects are separated into their individual components.",
    classes: ["Sorcerer", "Wizard"]
  },
  "collapse-timeline": {
    name: "Collapse Timeline (Genesis)",
    level: 9,
    school: "Universal",
    castingTime: "1 week (8 hours/day)",
    range: "180 ft.",
    components: "V, S, M (rare earths, minerals, and reagents worth 25,000 gp), XP (5,000 XP)",
    duration: "Instantaneous",
    description: "You create a finite plane: a demiplane. This demiplane is very small, but it can be customized to your liking. The demiplane is a 180-foot cube.",
    classes: ["Sorcerer", "Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "clone": {
    name: "Clone",
    level: 8,
    school: "Necromancy",
    castingTime: "10 minutes",
    range: "0 ft.",
    components: "V, S, M (laboratory supplies worth 1,000 gp), F (special laboratory equipment worth 500 gp)",
    duration: "Instantaneous",
    description: "This spell makes an inert duplicate of a creature.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },

  // Additional Abjuration Spells from Rebalanced School
  "arcane-ward": {
    name: "Arcane Ward",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Self",
    components: "V, S",
    duration: "1 round",
    description: "You create a momentary magical barrier that grants you +1 to AC against the next attack that targets you before the start of your next turn. At character level 10, this increases to +2 AC.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "resist-elements": {
    name: "Resist Elements",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 round",
    description: "You grant the target minor resistance to one energy type of your choice (acid, cold, electricity, fire, or sonic). The target gains resistance 2 to that energy type. At character level 10, this increases to resistance 3.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "alarm-ward": {
    name: "Alarm Ward",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "1 hour",
    description: "You place a minor ward on a 5-foot cube. If any creature enters the warded area, you receive a mental ping alerting you to the intrusion.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "disrupt-magic": {
    name: "Disrupt Magic",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "You send a pulse of disruptive energy that interferes with magic. If targeted at a magical effect, it has a 10% chance of ending that effect if the effect was created by a spell of 1st level or lower.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "protective-whisper": {
    name: "Protective Whisper",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 minute",
    description: "You whisper protective words that grant the target a +1 bonus on the next saving throw they make within the duration. This bonus increases to +2 at character level 10.",
    classes: ["Bard", "Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "detect-warding": {
    name: "Detect Warding",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "60 ft.",
    components: "V, S",
    duration: "Concentration, up to 1 minute",
    description: "You detect the presence of abjuration magic in the area. The amount of information revealed depends on how long you study a particular area.",
    classes: ["Bard", "Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "purify": {
    name: "Purify",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "Instantaneous",
    description: "You purify 1 cubic foot of food or water, removing all mundane poisons, diseases, and contaminants. This spell does not neutralize magical poisons or diseases but will reveal their presence with a faint glow.",
    classes: ["Cleric", "Druid", "Wizard", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "repel-vermin": {
    name: "Repel Vermin",
    level: 0,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "10 minutes",
    description: "You create a minor barrier that repels ordinary vermin of Tiny or smaller size (rats, bats, spiders, etc.). Such creatures cannot enter the protected area unless they succeed on a Will save.",
    classes: ["Druid", "Ranger", "Wizard", "Cleric", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "obscuring-ward": {
    name: "Obscuring Ward",
    level: 1,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 minute/level",
    description: "You surround yourself with a ward that obscures divination magic. For the duration, you gain a +4 bonus on saving throws against divination spells, and anyone attempting to scry on you takes a -4 penalty on their scrying check.",
    classes: ["Bard", "Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "protection-from-arrows": {
    name: "Protection from Arrows",
    level: 2,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a piece of tortoise shell or turtle shell)",
    duration: "1 hour/level or until discharged",
    description: "The warded creature gains resistance to ranged weapons. The subject gains damage reduction 10/magic against ranged weapons. Once the spell has prevented a total of 10 points of damage per caster level (maximum 100 points), it is discharged.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "warding-bond": {
    name: "Warding Bond",
    level: 2,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a pair of platinum rings worth 50 gp each, worn by both you and the target)",
    duration: "1 hour/level",
    description: "This spell creates a mystic connection between you and the target, granting the target a +1 bonus to AC and saving throws, and resistance 5 to all damage. Additionally, each time the target takes damage, you take the same amount of damage.",
    classes: ["Cleric", "Paladin", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "spell-immunity-lesser": {
    name: "Spell Immunity, Lesser",
    level: 2,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a diamond dust worth 100 gp)",
    duration: "10 minutes/level",
    description: "The warded creature is immune to the effects of one specified spell of 2nd level or lower. The spell can be one that follows a specific target or an area effect spell.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "curse-ward": {
    name: "Curse Ward",
    level: 2,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S",
    duration: "1 hour/level",
    description: "You place a protective ward against curses on the target. The target gains a +4 resistance bonus on saving throws against curses and curse-like effects. If the target is already under the effect of a curse, the curse is suppressed (but not removed) for the duration of this spell.",
    classes: ["Cleric", "Paladin", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "consecrate-object": {
    name: "Consecrate Object",
    level: 2,
    school: "Abjuration",
    castingTime: "1 minute",
    range: "Touch",
    components: "V, S, M (holy water and silver dust worth 25 gp)",
    duration: "Permanent",
    description: "You consecrate a single object, making it resistant to evil forces. The object gains a +2 sacred bonus to saving throws against all effects and cannot be directly handled by evil outsiders or undead.",
    classes: ["Cleric", "Paladin", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "magic-circle-against-evil": {
    name: "Magic Circle against Evil",
    level: 3,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a little powdered silver)",
    duration: "10 minutes/level",
    description: "All creatures within the area gain the effects of a protection from evil spell, and evil summoned creatures cannot enter the area either.",
    classes: ["Cleric", "Paladin", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "dispel-magic-greater": {
    name: "Dispel Magic, Greater",
    level: 3,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like dispel magic, except that it can end more than one spell on a target and it can be used to target multiple creatures.",
    classes: ["Bard", "Cleric", "Druid", "Wizard", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "spell-turning-lesser": {
    name: "Spell Turning, Lesser",
    level: 3,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a small silver mirror)",
    duration: "Until expended or 10 minutes/level",
    description: "Spells and spell-like effects targeted on you are turned back upon the original caster. This lesser version of spell turning affects only 1d4 spell levels.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "glyph-of-warding": {
    name: "Glyph of Warding",
    level: 3,
    school: "Abjuration",
    castingTime: "10 minutes",
    range: "Touch",
    components: "V, S, M (powdered diamond worth at least 200 gp)",
    duration: "Permanent until discharged",
    description: "This powerful inscription harms those who enter, pass, or open the warded area or object. A glyph of warding can guard a bridge or passage, ward a portal, trap a chest or box, and so on.",
    classes: ["Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "globe-of-invulnerability-lesser": {
    name: "Globe of Invulnerability, Lesser",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V, S, M (a glass or crystal bead)",
    duration: "1 round/level",
    description: "An immobile, faintly shimmering magical sphere surrounds you and excludes all spell effects of 3rd level or lower. The area or effect of any such spells does not include the area of the lesser globe of invulnerability.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "dimensional-lock": {
    name: "Dimensional Lock",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 day/level",
    description: "You create a shimmering emerald barrier that completely blocks extradimensional travel. Forms of movement barred include astral projection, blink, dimension door, ethereal jaunt, etherealness, gate, maze, plane shift, shadow walk, teleport, and similar spell-like abilities.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "repulsion": {
    name: "Repulsion",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Up to 10 ft./level",
    components: "V, S, M (a pair of small magnetized iron bars attached to two small canine statuettes, one ivory and one ebony)",
    duration: "1 round/level",
    description: "An invisible, mobile field surrounds you and prevents creatures from approaching you. You decide how big the field is at the time of casting. Any creature within or entering the field must attempt a save.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "curse-ward-greater": {
    name: "Curse Ward, Greater",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a silver mirror worth 100 gp)",
    duration: "1 hour/level",
    description: "You place a powerful protective ward against curses on the target. The target gains immunity to curses and curse-like effects for the duration.",
    classes: ["Cleric", "Paladin", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "elemental-shield": {
    name: "Elemental Shield",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S",
    duration: "1 round/level",
    description: "This spell creates a protective shield that surrounds you and protects you from the specified energy type. The shield absorbs the first 12 points of energy damage per round that you would normally take. In addition, the shield deals 1d6+2 points of damage of the opposite energy type to any creature that makes a successful melee attack against you.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "dimensional-seal": {
    name: "Dimensional Seal",
    level: 4,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a small platinum ring)",
    duration: "1 round/level",
    description: "You place a seal on a target creature that prevents it from using any form of teleportation or extradimensional travel. The target cannot use spells or abilities like dimension door, teleport, plane shift, or similar effects for the duration of the spell.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "spell-resistance": {
    name: "Spell Resistance",
    level: 5,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a diamond worth 1,000 gp)",
    duration: "1 minute/level",
    description: "The target gains spell resistance equal to 12 + your caster level (maximum SR 25). Spell resistance can be overcome by a spellcaster with a sufficiently high caster level check (1d20 + caster level against the SR).",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "dismissal": {
    name: "Dismissal",
    level: 5,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (any item that is distasteful to the subject)",
    duration: "Instantaneous",
    description: "This spell forces an extraplanar creature back to its proper plane if it fails a Will save. If the spell is successful, the creature is instantly whisked away, but there is a 20% chance of actually sending the subject to a plane other than its own.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "break-enchantment": {
    name: "Break Enchantment",
    level: 5,
    school: "Abjuration",
    castingTime: "1 minute",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell frees victims from enchantments, transmutations, and curses. Break enchantment can reverse even an instantaneous effect. For each such effect, you make a caster level check (1d20 + caster level, maximum +15) against a DC of 11 + caster level of the effect.",
    classes: ["Bard", "Cleric", "Paladin", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Soldier", "Tinker"]
  },
  "mages-private-sanctum": {
    name: "Mage's Private Sanctum",
    level: 5,
    school: "Abjuration",
    castingTime: "10 minutes",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a thin sheet of lead, a piece of opaque glass, a wad of cotton or cloth, and powdered chrysolite)",
    duration: "24 hours",
    description: "This spell ensures privacy. Anyone looking into the area from outside sees only a dark, foggy mass. No sounds can escape the area. Those inside can see out normally. Divination spells cannot perceive anything within the area, and those within are immune to detect thoughts.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "globe-of-invulnerability": {
    name: "Globe of Invulnerability",
    level: 5,
    school: "Abjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V, S, M (a glass or crystal bead)",
    duration: "1 round/level",
    description: "This spell functions like lesser globe of invulnerability, except that it also excludes 4th-level spells and spell-like effects.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "banishment": {
    name: "Banishment",
    level: 5,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (any item that is distasteful to the subject, plus an object or substance that is anathema to the subject)",
    duration: "Instantaneous",
    description: "A banishment spell is a more powerful version of the dismissal spell. It enables you to force extraplanar creatures out of your home plane. As many as 2 HD of creatures per caster level can be banished.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "spell-turning-greater": {
    name: "Spell Turning, Greater",
    level: 5,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a small silver mirror)",
    duration: "Until expended or 10 minutes/level",
    description: "This spell functions like lesser spell turning, except it affects 1d4+6 spell levels.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "antimagic-aura": {
    name: "Antimagic Aura",
    level: 5,
    school: "Abjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V, S, M (a pinch of powdered iron)",
    duration: "1 round/level",
    description: "You are surrounded by a mobile antimagic field that suppresses magical effects. This functions like antimagic field, except the radius is only 10 feet, and you can move the field with you. Spells and magical effects within the field are suppressed but not dispelled.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },

  // Level 6 Abjuration Spells
  "dispel-magic-supreme": {
    name: "Dispel Magic, Supreme",
    level: 6,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like greater dispel magic, except that the maximum caster level on your dispel check is +20 instead of +10. Additionally, supreme dispel magic has a chance to dispel any effect that remove curse can remove, even if dispel magic can't dispel that effect.",
    classes: ["Bard", "Cleric", "Druid", "Wizard", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "guards-and-wards": {
    name: "Guards and Wards",
    level: 6,
    school: "Abjuration",
    castingTime: "30 minutes",
    range: "Anywhere within the area to be warded",
    components: "V, S, M (burning incense, a small measure of brimstone and oil, a knotted string, a small amount of monster blood, and a small silver rod worth 10 gp)",
    duration: "2 hours/level",
    description: "This powerful spell is primarily used to defend your stronghold. The ward protects 200 square feet per caster level. The spell creates magical effects within the warded area: fog, arcane locks, webs, confusion effect, lost doors, and summon guardian.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "repulsion-field": {
    name: "Repulsion Field",
    level: 6,
    school: "Abjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V, S, M (a pair of small magnetized iron bars)",
    duration: "1 minute/level",
    description: "You create a mobile field that surrounds you and prevents creatures from approaching you. Any creature within or entering the field must attempt a Will save. If it fails, it becomes unable to move toward you for the duration of the spell.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "spell-immunity-greater": {
    name: "Spell Immunity, Greater",
    level: 6,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (diamond dust worth 500 gp)",
    duration: "10 minutes/level",
    description: "This spell functions like spell immunity, except the immunity applies to spells of 8th level or lower. A creature can have only one spell immunity or greater spell immunity spell in effect on it at a time.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "planar-binding-lesser": {
    name: "Planar Binding, Lesser",
    level: 6,
    school: "Abjuration",
    castingTime: "10 minutes",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "Casting this spell attempts a dangerous act: to lure a creature from another plane to a specifically prepared trap, which must lie within the spell's range. The called creature is held in the trap until it agrees to perform one service in return for its freedom.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "glyph-of-warding-greater": {
    name: "Glyph of Warding, Greater",
    level: 6,
    school: "Abjuration",
    castingTime: "10 minutes",
    range: "Touch",
    components: "V, S, M (powdered diamond worth at least 400 gp)",
    duration: "Permanent until discharged",
    description: "This spell functions like glyph of warding, except that a greater blast glyph deals up to 10d8 points of damage, and a greater spell glyph can store a spell of 6th level or lower.",
    classes: ["Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "dimensional-barrier": {
    name: "Dimensional Barrier",
    level: 6,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "24 hours",
    description: "You create a shimmering barrier that completely blocks extradimensional travel. This spell functions like dimensional lock, except the barrier extends into the Ethereal Plane, blocking ethereal travel as well.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },

  // Level 7 Abjuration Spells
  "banishment-greater": {
    name: "Banishment, Greater",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (any item that is distasteful to the subject, plus an object or substance that is anathema to the subject)",
    duration: "Instantaneous",
    description: "This spell functions like banishment, except that there is no HD limit. Additionally, for each object or substance that is anathema to the subject, you gain a +2 bonus on your caster level check to overcome the target's spell resistance (if any), and the saving throw DC increases by 2.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "sequester": {
    name: "Sequester",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a basilisk eyelash and gum arabic)",
    duration: "1 day/level",
    description: "When cast, this spell not only prevents divination spells from working to detect or locate the creature or object affected by sequester, it also renders the affected creature or object invisible to any form of sight or seeing. Creatures affected by sequester become comatose and are effectively in a state of suspended animation until the spell wears off or is dispelled.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "spell-turning": {
    name: "Spell Turning",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a small silver mirror)",
    duration: "Until expended or 10 minutes/level",
    description: "Spells and spell-like effects targeted on you are turned back upon the original caster. The abjuration turns only spells that have you as a target. From seven to ten (1d4+6) spell levels are affected by the turning.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "planar-binding": {
    name: "Planar Binding",
    level: 7,
    school: "Abjuration",
    castingTime: "10 minutes",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like lesser planar binding, except that you can call a single creature of 12 HD or less, or up to three creatures of the same kind whose Hit Dice total no more than 12.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "energy-immunity": {
    name: "Energy Immunity",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a piece of the appropriate element)",
    duration: "24 hours",
    description: "The subject is immune to damage from one specified energy type (acid, cold, electricity, fire, or sonic). Energy immunity absorbs only damage; the subject could still suffer side effects, such as drowning in acid or becoming encased in ice.",
    classes: ["Cleric", "Druid", "Wizard", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "prismatic-wall": {
    name: "Prismatic Wall",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "10 minutes/level",
    description: "Prismatic wall creates a vertical, opaque wall—a shimmering, multicolored plane of light that protects you from all forms of attack. The wall flashes with seven colors, each of which has a distinct power and purpose. The wall's seven layers must be breached in order from red to violet.",
    classes: ["Wizard", "Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior", "Druid", "Monk"]
  },
  "dimensional-anchor-mass": {
    name: "Dimensional Anchor, Mass",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 minute/level",
    description: "This spell functions like dimensional anchor, except that it affects up to one creature per three caster levels, no two of which can be more than 30 feet apart. Each target must be hit by a ranged touch attack.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "sanctuary-mass": {
    name: "Sanctuary, Mass",
    level: 7,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a small silver mirror)",
    duration: "1 round/level",
    description: "This spell functions like sanctuary, except it affects multiple creatures.",
    classes: ["Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },

  // Level 8 Abjuration Spells
  "mind-blank": {
    name: "Mind Blank",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "24 hours",
    description: "The subject is protected from all devices and spells that gather information about the target through divination magic. This spell also grants a +8 resistance bonus on saving throws against all mind-affecting spells and effects.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "dimensional-lock-greater": {
    name: "Dimensional Lock, Greater",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Medium (100 ft. + 10 ft./level)",
    components: "V, S",
    duration: "1 day/level",
    description: "This spell functions like dimensional lock, except the area affected is a 60-foot-radius emanation, and the effect extends into the Ethereal Plane and the Plane of Shadow, preventing ethereal and shadow travel as well.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "protection-from-spells": {
    name: "Protection from Spells",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a diamond of at least 500 gp value)",
    duration: "10 minutes/level",
    description: "The subject gains spell resistance equal to 12 + your caster level. This spell resistance cannot be voluntarily lowered. Protection from spells provides no defense against supernatural or spell-like abilities.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "planar-binding-greater": {
    name: "Planar Binding, Greater",
    level: 8,
    school: "Abjuration",
    castingTime: "10 minutes",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like lesser planar binding, except that you can call a single creature of 18 HD or less, or up to three creatures of the same kind whose Hit Dice total no more than 18.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "antimagic-field-greater": {
    name: "Antimagic Field, Greater",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V, S, M (a pinch of powdered iron or iron filings)",
    duration: "10 minutes/level",
    description: "This spell functions like antimagic field, except the radius is 20 feet, and you can move the field with you. Additionally, the field suppresses supernatural abilities as well as magical effects.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "spell-immunity-supreme": {
    name: "Spell Immunity, Supreme",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (diamond dust worth 1,500 gp)",
    duration: "10 minutes/level",
    description: "This spell functions like spell immunity, except the immunity applies to spells of 9th level or lower. A creature can have only one spell immunity spell in effect on it at a time.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "prismatic-wall-greater": {
    name: "Prismatic Wall, Greater",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "10 minutes/level",
    description: "This spell functions like prismatic wall, except that it creates a sphere instead of a wall. The sphere can be up to 10 feet in radius per caster level. Creatures inside the sphere when it is created are not harmed, but they cannot leave without going through the prismatic layers.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "divine-aegis": {
    name: "Divine Aegis",
    level: 8,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a shield blessed by a deity)",
    duration: "1 round/level",
    description: "You are surrounded by a shimmering field of divine energy that provides immunity to death effects, energy drain, and ability drain. Additionally, you gain spell resistance equal to 15 + your caster level against spells with the evil descriptor.",
    classes: ["Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },

  // Level 9 Abjuration Spells
  "prismatic-sphere": {
    name: "Prismatic Sphere",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "10 ft.",
    components: "V",
    duration: "10 minutes/level",
    description: "This spell functions like prismatic wall, except you conjure up an immobile, opaque globe of shimmering, multicolored light that surrounds you and protects you from all forms of attack. The sphere flashes in all colors of the visible spectrum.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "mages-disjunction": {
    name: "Mage's Disjunction",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V",
    duration: "Instantaneous",
    description: "All magical effects and magic items within the radius of the spell, except for those that you carry or touch, are disjoined. That is, spells and spell-like effects are separated into their individual components (ending the effect as a dispel magic spell does), and each permanent magic item must make a successful Will save or be turned into a normal item.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "freedom": {
    name: "Freedom",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S",
    duration: "Instantaneous",
    description: "The subject is freed from spells and effects that restrict its movement, including binding, entangle, grappling, imprisonment, maze, paralysis, petrification, pinning, sleep, slow, stunning, temporal stasis, and web. To free a creature from imprisonment or maze, you must know its name and background, and you must cast this spell at the spot where it was entombed or banished into the maze.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "gate-seal": {
    name: "Gate Seal",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a diamond worth at least 5,000 gp)",
    duration: "Permanent",
    description: "You seal a gate, portal, or similar magical opening, preventing its use. The seal cannot be dispelled, but it can be destroyed by a mage's disjunction spell or by dealing 50 points of damage to it (the seal has hardness 20).",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "invulnerability": {
    name: "Invulnerability",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a small piece of adamantine worth 500 gp)",
    duration: "1 round/level",
    description: "This spell makes you immune to all damage. You take no damage from any attack or effect that deals hit point damage. However, you are not immune to effects that don't deal damage, such as ability damage, level drain, or death effects.",
    classes: ["Wizard", "Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "spell-resistance-mass": {
    name: "Spell Resistance, Mass",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Close (25 ft. + 5 ft./2 levels)",
    components: "V, S, M (a diamond worth at least 1,000 gp per target)",
    duration: "1 minute/level",
    description: "This spell functions like spell resistance, except it affects up to one creature per caster level, no two of which can be more than 30 feet apart. Each target gains spell resistance equal to 12 + your caster level.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "divine-shield": {
    name: "Divine Shield",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Personal",
    components: "V, S, M (a shield blessed by your deity)",
    duration: "1 round/level",
    description: "You are surrounded by a barrier of pure divine energy. You gain immunity to all spells and spell-like abilities of 8th level or lower. Additionally, you gain spell resistance equal to 25 + your caster level against spells of 9th level.",
    classes: ["Cleric", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "planar-immunity": {
    name: "Planar Immunity",
    level: 9,
    school: "Abjuration",
    castingTime: "1 action",
    range: "Touch",
    components: "V, S, M (a piece of the target plane worth 1,000 gp)",
    duration: "24 hours",
    description: "The subject becomes immune to all harmful planar effects of one specific plane of existence. This includes environmental dangers, planar traits that cause damage or penalties, and effects that would forcibly transport the subject to or from that plane.",
    classes: ["Cleric", "Wizard", "Druid", "Mage", "Monk", "Oracle", "Paladin", "Soldier", "Tinker"]
  },
  "flare-spark": {
    name: "Flare Spark",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "1d6 fire damage.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "dust-gust": {
    name: "Dust Gust",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Push small object or scatter 5 ft of sand/dust.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "crackle-jolt": {
    name: "Crackle Jolt",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "1d4 lightning; arcs to second target for 1 damage.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "lodestone-pull": {
    name: "Lodestone Pull",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Draws metal object 5 ft toward caster.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "minor-elemental-ward": {
    name: "Minor Elemental Ward",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "+1 to next saving throw vs elemental damage.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "flicker-flame": {
    name: "Flicker Flame",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Create dim dancing light source for 10 minutes.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "stone-skin-sliver": {
    name: "Stone Skin Sliver",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "+1 AC for 1 round (concentration).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "mana-kindle": {
    name: "Mana Kindle",
    level: 0,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Recover 1 expended cantrip slot (once per long rest).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-fire-pet": {
    name: "Summon Fire Pet",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Small elemental: HP 10, AC 13, 1d8 fire melee.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "burning-sands": {
    name: "Burning Sands",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "2d6 fire + target must save or have movement halved.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "shockwave": {
    name: "Shockwave",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "1d10 lightning in a 15-ft line; DEX save for half.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "earthen-grip": {
    name: "Earthen Grip",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target restrained, STR save or immobilized 1 round.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-minor-weapon": {
    name: "Summon Minor Weapon",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Create a spectral melee weapon: 1d6 damage.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "flame-armor": {
    name: "Flame Armor",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "+2 AC; melee attackers take 1 fire damage.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "heat-metal-conjured": {
    name: "Heat Metal (Conjured)",
    level: 1,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target's armor or weapon deals 1d6 fire to user each round.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-air-pet": {
    name: "Summon Air Pet",
    level: 2,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Elemental pet: HP 20, AC 15, 2 attacks at 1d6 slashing.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "elemental-barrage": {
    name: "Elemental Barrage",
    level: 2,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "2d8 damage (choose fire, cold, lightning).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "conjure-shield-of-sparks": {
    name: "Conjure Shield of Sparks",
    level: 2,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "+3 AC and reflects 1d4 lightning to attacker.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-weaponry-satchel": {
    name: "Summon Weaponry Satchel",
    level: 2,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Conjures magical ammo or tools usable for 1 hour.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-earth-pet": {
    name: "Summon Earth Pet",
    level: 3,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "HP 30, AC 17, 1d10 bludgeon, + knockdown.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "conjure-elemental-lance": {
    name: "Conjure Elemental Lance",
    level: 3,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Line 30 ft: 4d6 elemental damage, save for half.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "burst-of-flamewind": {
    name: "Burst of Flamewind",
    level: 3,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All enemies in 15 ft cone take 3d8 fire and are pushed back 5 ft.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "elemental-displacement": {
    name: "Elemental Displacement",
    level: 3,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Teleport self or ally 30 ft.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-water-pet": {
    name: "Summon Water Pet",
    level: 4,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "HP 35, AC 14, can heal allies for 2d6 or attack for 1d10 cold.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "crystalline-barrier": {
    name: "Crystalline Barrier",
    level: 4,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Wall of elemental glass (AC 18, HP 40), blocks line of sight.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "elemental-drain": {
    name: "Elemental Drain",
    level: 4,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target loses 2 spell slots and takes 3d6 damage (random element).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "bind-element": {
    name: "Bind Element",
    level: 4,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Trap one elemental creature in place (WIS save or paralyzed 2 rounds).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-greater-fire-pet": {
    name: "Summon Greater Fire Pet",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "HP 60, AC 17, 2d10 fire, aura burns adjacent foes.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "massive-elemental-blast": {
    name: "Massive Elemental Blast",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All enemies in 20 ft radius: 5d8 elemental damage.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "living-magma": {
    name: "Living Magma",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target must CON save or suffer 1d10/round for 3 rounds.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "elemental-banishment": {
    name: "Elemental Banishment",
    level: 5,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Remove 1 summoned enemy from battlefield (CHA save).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-greater-air-pet": {
    name: "Summon Greater Air Pet",
    level: 6,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "HP 65, AC 18, 2d8 wind slash, 50% miss chance vs projectiles.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "elemental-warp-field": {
    name: "Elemental Warp Field",
    level: 6,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Allies within 10 ft gain resistance to elemental damage.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "chain-arc": {
    name: "Chain Arc",
    level: 6,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Jumping lightning: 6 targets, 3d8 damage, arcs randomly.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "conjure-skybrand-weapon": {
    name: "Conjure Skybrand Weapon",
    level: 6,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Floating weapon makes 2 attacks/round for 1d12 lightning.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-greater-earth-pet": {
    name: "Summon Greater Earth Pet",
    level: 7,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "HP 80, AC 20, Tremor Slam (2d10, knocks prone).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "volcanic-cage": {
    name: "Volcanic Cage",
    level: 7,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Traps 1–3 creatures in molten rock: 6d6 fire, CON save or immobilized.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-living-armor": {
    name: "Summon Living Armor",
    level: 7,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Conjure suit of magical armor (grants +4 AC to self or ally).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "prismatic-conflux": {
    name: "Prismatic Conflux",
    level: 7,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Each enemy takes 2d8 random elemental type (roll separately).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-greater-water-pet": {
    name: "Summon Greater Water Pet",
    level: 8,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "HP 90, AC 16, healing wave (3d6 AoE heal) or 2d10 cold blast.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "frozen-time-prism": {
    name: "Frozen Time Prism",
    level: 8,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Freeze 1 creature in place for 1 round, WIS save ends.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "conjure-sky-fortress": {
    name: "Conjure Sky Fortress",
    level: 8,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Floating platform appears, grants high ground or ranged cover.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "mana-furnace": {
    name: "Mana Furnace",
    level: 8,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Converts all elemental damage taken into spell slot regeneration.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "summon-elemental-avatar": {
    name: "Summon Elemental Avatar",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "HP 180, attacks 3x/round, elemental resistances, aura damage.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "cataclysmic-conjuration": {
    name: "Cataclysmic Conjuration",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "60 ft radius: 10d10 of chosen element.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "elemental-fusion": {
    name: "Elemental Fusion",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Merge with summoned pet: share stats, cast 2 spells/round.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "storm-cage": {
    name: "Storm Cage",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Traps creature in electrical field: 8d6/round, cannot escape.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "elemental-convergence": {
    name: "Elemental Convergence",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All four base pets summoned at once for 1 minute.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "conjure-magmatic-wyrm": {
    name: "Conjure Magmatic Wyrm",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Massive fire serpent: HP 250, breathes 6d12 fire in cone.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "eternal-forge": {
    name: "Eternal Forge",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Create magical weapon or item permanently (DM discretion).",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "planar-overload": {
    name: "Planar Overload",
    level: 9,
    school: "Conjuration",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Tear open rift; all enemies in 100 ft take 12d8 elemental.",
    classes: ["Dragoon", "Druid", "Mage", "Ranger", "Shaman", "Tinker"]
  },
  "foresight-flicker": {
    name: "Foresight Flicker",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Next enemy roll against you has Disadvantage.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "guiding-spark": {
    name: "Guiding Spark",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Know true north or locate nearest magical presence.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "omen-whisper": {
    name: "Omen Whisper",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Hear a vague message from beyond; DM gives cryptic tip.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "detect-emotion": {
    name: "Detect Emotion",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Sense basic emotion of one creature (happy, afraid, angry, etc.).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "aura-glimpse": {
    name: "Aura Glimpse",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "See magical auras briefly (10-ft radius).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "far-echo": {
    name: "Far Echo",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Replay last 6 seconds of speech in location.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "predict-movement": {
    name: "Predict Movement",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Gain +1 to next DEX save or attack roll.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "soul-mark": {
    name: "Soul Mark",
    level: 0,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Tag a creature for 1 minute; you know its direction if within 1 mile.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "true-sight-lesser": {
    name: "True Sight (Lesser)",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "See invisible/hidden creatures for 1 minute.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "warning-ward": {
    name: "Warning Ward",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Trap glows if enemy enters; does no damage.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "scribe-destiny": {
    name: "Scribe Destiny",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Learn a creature’s greatest desire or fear (WIS save resists).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "mark-omen": {
    name: "Mark Omen",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Mark a creature; reroll 1 attack against them within 1 hour.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "clairaudience-lesser": {
    name: "Clairaudience (Lesser)",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Hear a distant known location for 1 minute.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "fate-coin": {
    name: "Fate Coin",
    level: 1,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Once in next hour, flip coin to reroll any 1 die result.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "divine-perception": {
    name: "Divine Perception",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "See if target is under divine influence (blessed, cursed, possessed).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "clairvoyance": {
    name: "Clairvoyance",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "See or hear a location within 1 mile.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "vision-trap": {
    name: "Vision Trap",
    level: 2,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Plant false sight into an enemy's mind; disorients and causes 2d6 psychic.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "eyes-of-the-divine": {
    name: "Eyes of the Divine",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "See through magical and mundane disguises.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "future-echo": {
    name: "Future Echo",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Next round, choose initiative order for allies.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "reveal-weakness": {
    name: "Reveal Weakness",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target's next saving throw is made with Disadvantage.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "planar-window": {
    name: "Planar Window",
    level: 3,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Open vision into another plane; detect native beings and effects.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "fate-reversal": {
    name: "Fate Reversal",
    level: 4,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Force a reroll of one attack, save, or check anywhere on battlefield.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "seal-vision": {
    name: "Seal Vision",
    level: 4,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Block divination spells from affecting an area or creature.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "aspect-of-insight": {
    name: "Aspect of Insight",
    level: 4,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Gain advantage on all mental saves and +2 INT/WIS for 1 minute.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "planar-summons-lesser": {
    name: "Planar Summons (Lesser)",
    level: 5,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Summon a celestial, elemental, or outsider (CR 5 or lower).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "prophetic-frenzy": {
    name: "Prophetic Frenzy",
    level: 5,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Gain 3 premonitions: spend to negate hits, auto succeed saves, etc.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "vision-of-ruin": {
    name: "Vision of Ruin",
    level: 5,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target sees future self's demise: WIS save or stunned 1 round + 5d6 psychic.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "woven-threads": {
    name: "Woven Threads",
    level: 5,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Alter a creature’s recent memory (last 1 minute, WIS save resists).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "planar-binding-minor": {
    name: "Planar Binding (Minor)",
    level: 6,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Compel an extraplanar creature to serve you (up to CR 8).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "eye-of-judgement": {
    name: "Eye of Judgement",
    level: 6,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Reveal and suppress one creature’s class features for 1 round (WIS save resists).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "mass-revelation": {
    name: "Mass Revelation",
    level: 7,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Reveal hidden traps, enemies, magic, and lies in 60-ft cone.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "planar-summons-greater": {
    name: "Planar Summons (Greater)",
    level: 7,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Summon two extraplanar allies (up to CR 8 each).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "premonition-shield": {
    name: "Premonition Shield",
    level: 7,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You or an ally takes no damage from next 2 attacks or spells.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "fate-echo": {
    name: "Fate Echo",
    level: 7,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Copy one non-damaging spell cast in last 3 rounds.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "divine-intervention-lesser": {
    name: "Divine Intervention (Lesser)",
    level: 8,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Call on deity to cast a spell of 6th level or lower as free action.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "mind-ravel": {
    name: "Mind Ravel",
    level: 8,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target suffers confusion and forgets last 5 minutes; WIS save resists.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "stitch-fate": {
    name: "Stitch Fate",
    level: 8,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Change one failed death save or auto-revive a dying target.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "seal-of-banishment": {
    name: "Seal of Banishment",
    level: 8,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Banish up to 3 extraplanar creatures (CHA save resists).",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "divine-intervention-greater": {
    name: "Divine Intervention (Greater)",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Ask your god a single question or task; result is GM-determined miracle.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "summon-herald-of-the-planes": {
    name: "Summon Herald of the Planes",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Call a unique CR 15+ celestial, elemental, or outsider to aid you.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "prophecy-fulfilled": {
    name: "Prophecy Fulfilled",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Declare one creature’s next action: they must succeed INT save or do it.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "time-fracture": {
    name: "Time Fracture",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Enemies reroll all d20s at disadvantage for 1 minute.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "foresight-perfect": {
    name: "Foresight (Perfect)",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You cannot be surprised or critically hit for 1 hour; advantage on all saves.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "oracle-of-eternity": {
    name: "Oracle of Eternity",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Ask 3 yes/no questions and receive divine truth.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "soul-reflection": {
    name: "Soul Reflection",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target is forced to fight a version of themselves for 3 rounds.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "thread-severance": {
    name: "Thread Severance",
    level: 9,
    school: "Divination",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Instantly end 1 effect or condition, or cause death if creature fails CHA save and is under 25 HP.",
    classes: ["Cleric", "Mirrorsage", "Oracle", "Paladin", "Ranger", "Shaman"]
  },
  "calm-whispers": {
    name: "Calm Whispers",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target makes WIS save or has disadvantage on next attack.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mental-flicker": {
    name: "Mental Flicker",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Disorient minor creature; 1d4 psychic.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "false-comfort": {
    name: "False Comfort",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target believes they are healing; no effect, distraction only.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "glimmering-eyes": {
    name: "Glimmering Eyes",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Caster gains +2 to Persuasion or Deception for 1 minute.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "disrupt-memory": {
    name: "Disrupt Memory",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target forgets last 6 seconds; ends concentration.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "enthralling-tune": {
    name: "Enthralling Tune",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Play a tone that draws attention; 1 target loses focus.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mental-tap": {
    name: "Mental Tap",
    level: 0,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "1d4 psychic; caster gains +1 to next save if damage dealt.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mesmerize": {
    name: "Mesmerize",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target creature is stunned and unaware for 1 round (CHA save).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "pacify": {
    name: "Pacify",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Enemy cannot attack or cast damaging spells for 1 round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "confusing-flash": {
    name: "Confusing Flash",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target makes WIS save or randomly attacks or flees.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "weaken-will": {
    name: "Weaken Will",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "-2 to next WIS save; 1 minute duration.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "distract": {
    name: "Distract",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Interrupt enemy action (no opportunity attacks this round).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "voice-of-peace": {
    name: "Voice of Peace",
    level: 1,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Negotiate ceasefire; 1 enemy will not attack unless provoked.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "deep-mesmerize": {
    name: "Deep Mesmerize",
    level: 2,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target stunned 2 rounds or until damaged.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "dire-charm": {
    name: "Dire Charm",
    level: 2,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target becomes loyal servant for 1 minute (WIS save at end of each turn).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "group-pacify": {
    name: "Group Pacify",
    level: 2,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All enemies in 15-ft cone cannot initiate combat unless provoked.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "illusive-commands": {
    name: "Illusive Commands",
    level: 2,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Force simple action: drop item, walk away, kneel.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mass-mesmerize": {
    name: "Mass Mesmerize",
    level: 3,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Up to 4 creatures stunned for 1 round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "dominate-beast": {
    name: "Dominate Beast",
    level: 3,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Control a beast’s actions (INT save resists).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "terrifying-gaze": {
    name: "Terrifying Gaze",
    level: 3,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Frighten one target for 3 rounds; WIS save ends early.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mental-chains": {
    name: "Mental Chains",
    level: 3,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target cannot move more than 10 ft from original spot.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mass-pacify": {
    name: "Mass Pacify",
    level: 4,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All enemies in 30-ft radius cannot attack unless attacked.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "erase-emotion": {
    name: "Erase Emotion",
    level: 4,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Removes anger, fear, or pain; target cannot use rage/fear abilities.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mass-sleep": {
    name: "Mass Sleep",
    level: 5,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "60 HP worth of creatures fall asleep for 1 minute.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "group-illusion": {
    name: "Group Illusion",
    level: 5,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Create illusionary party of allies; target enemy misdirected.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mental-bomb": {
    name: "Mental Bomb",
    level: 5,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All enemies in 20-ft radius take 4d6 psychic and lose next reaction.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mass-charm": {
    name: "Mass Charm",
    level: 6,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Charm up to 6 creatures for 1 minute (WIS save ends early).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "haze-of-forgetting": {
    name: "Haze of Forgetting",
    level: 6,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All targets in 30 ft forget last 1 minute (INT save resists).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "puppet-strings": {
    name: "Puppet Strings",
    level: 6,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Control a target’s movement for 2 rounds (STR save resists).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "willbreaker": {
    name: "Willbreaker",
    level: 6,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target cannot cast spells or use magic items (WIS save ends).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mass-confusion": {
    name: "Mass Confusion",
    level: 7,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Each enemy in 30-ft radius behaves randomly.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "dominate-greater-beast": {
    name: "Dominate Greater Beast",
    level: 7,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Control magical beasts (CR 12 or lower).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mindfog-field": {
    name: "Mindfog Field",
    level: 7,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Area causes -2 to INT/WIS/CHA checks and saves.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "lasting-control": {
    name: "Lasting Control",
    level: 7,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Extend duration of all current enchantment spells by 10 minutes.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mass-dominate": {
    name: "Mass Dominate",
    level: 8,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Control up to 3 creatures (CR 10 or less, WIS save each turn).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "paralyzing-presence": {
    name: "Paralyzing Presence",
    level: 8,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Enemies who see you must WIS save or become paralyzed 1 round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "erase-mind": {
    name: "Erase Mind",
    level: 8,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Remove all short-term memory of event; identity shaken (WIS save resists).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mental-collapse": {
    name: "Mental Collapse",
    level: 8,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target loses all ability to communicate or cast spells for 1 minute.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "absolute-domination": {
    name: "Absolute Domination",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Control any creature (WIS save at end of each turn); lasts 1 minute.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "mass-willbreaker": {
    name: "Mass Willbreaker",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All enemies in range cannot use abilities or spells (WIS save ends).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "frightful-sovereignty": {
    name: "Frightful Sovereignty",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All enemies take 6d6 psychic, WIS save or flee for 3 rounds.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "puppetmaster-s-realm": {
    name: "Puppetmaster’s Realm",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You control battlefield: redirect attacks, block movements for 1 minute.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "command-reality": {
    name: "Command Reality",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "One creature must obey a one-sentence command (WIS save resists).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "rewrite-loyalty": {
    name: "Rewrite Loyalty",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Make target believe they’ve always served your cause (CHA save resists).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "perfect-mesmerize": {
    name: "Perfect Mesmerize",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "One creature stunned, silent, defenseless for full duration unless damaged.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "erase-soul": {
    name: "Erase Soul",
    level: 9,
    school: "Enchantment",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target forgets who they are; cannot act for 3 rounds (no action, WIS negates early).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Paladin", "Thief"]
  },
  "soundburst": {
    name: "Soundburst",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a sudden, loud burst of sound. Each creature in the area takes 1d3 points of sonic damage and must make a Fortitude save or be deafened for 1 round.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "minor-combustion": {
    name: "Minor Combustion",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Light a torch or small object instantly.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "force-needle": {
    name: "Force Needle",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You project a tiny, needle-like dart of force. Make a ranged touch attack against the target. This ray ignores cover, including total cover if you have line of effect to the target. If it hits, the needle deals 1d4 points of piercing force damage.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arcane-echo": {
    name: "Arcane Echo",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "After casting this spell, if you cast another Evocation cantrip that deals damage before the end of your current turn, you can immediately cast that same damaging cantrip again as a free action, targeting the same or a different creature. The second casting uses the same attack roll or save DC as the first. This effect can only be used once per casting of Arcane Echo.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "magic-missile-storm": {
    name: "Magic Missile Storm",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "3 missiles, each 1d4+1; auto-hit.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "thunder-clap": {
    name: "Thunder Clap",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "15-ft cone, 2d6 thunder, DEX save halves.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arcane-shield-shatter": {
    name: "Arcane Shield Shatter",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Dispel shield spells; deals 1d8 arcane damage.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "ignition-bolt": {
    name: "Ignition Bolt",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You hurl a searing bolt of fire. Make a ranged touch attack against a target. If it hits, the target takes 1d10 points of fire damage. Whether the bolt hits or misses, it explodes upon impact (or at the end of its range if it misses), dealing 1d4 points of fire damage to all creatures within a 5-foot radius of the impact point (Reflex save for half). The primary target does not take this splash damage.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "scorching-raystorm": {
    name: "Scorching Raystorm",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Fire 3 rays, each 2d6 fire damage.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arc-flash": {
    name: "Arc Flash",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Blinds enemies in 20-ft radius, 3d6 lightning.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "elemental-devastation": {
    name: "Elemental Devastation",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "20-ft radius: 10d10 elemental damage (roll per enemy).",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "supernova-lance": {
    name: "Supernova Lance",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "100-ft line: 12d6 fire + push back 20 ft.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "absolute-silence": {
    name: "Absolute Silence",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "30-ft zone where thunder spells are doubled; no speech or sound.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "crystalline-flash": {
    name: "Crystalline Flash",
    level: 8,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Exploding prism: 8d10 radiant or cold; causes blindness.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arcane-apocalypse": {
    name: "Arcane Apocalypse",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "60-ft radius: 12d10 force damage, structures obliterated.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "thunder-wrath": {
    name: "Thunder Wrath",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Storm cloud strikes 5 times per round for 6d6 lightning.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "hellstorm": {
    name: "Hellstorm",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Rain of fire over 100 ft, 8d10/round for 3 rounds.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "frozen-eternity": {
    name: "Frozen Eternity",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Time stop for 1 target; no action for 3 rounds (WIS save ends).",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arc-furnace": {
    name: "Arc Furnace",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Forge of energy: allies' spell damage +50% in zone.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "starfire-core": {
    name: "Starfire Core",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Nuclear burst of arcane and fire: 15d10, terrain permanently scorched.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "final-spark": {
    name: "Final Spark",
    level: 9,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Sacrifice self: 200 damage in 60-ft radius, unavoidable.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "minor-combustion-light": {
    name: "Minor Combustion (Light)",
    level: 0,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell causes an object to glow like a torch, shedding normal light in a 20-foot radius, and increasing the light level by one step for an additional 20 feet beyond that area (darkness becomes dim light, and dim light becomes normal light). The effect is immobile, but it can be cast on a movable object. Light taken into an area of magical darkness does not function. This spell can also be used to instantly light a torch, candle, or small, easily flammable object.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "magic-missile-storm-magic-missile": {
    name: "Magic Missile Storm (Magic Missile)",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create three shimmering missiles of magical energy that unerringly strike their targets. Each missile deals 1d4+1 points of force damage. The missiles all strike simultaneously and can be directed at a single creature or several creatures. A creature cannot be targeted by more than one missile from a single casting of this spell unless you are targeting fewer than three creatures.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "thunder-clap-thunderwave": {
    name: "Thunder Clap (Thunderwave)",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "A wave of thunderous force sweeps out from you. Each creature in a 15-foot cube originating from you must make a Constitution saving throw. On a failed save, a creature takes 2d6 thunder damage and is pushed 10 feet away from you. On a successful save, the creature takes half as much damage and isn’t pushed. In addition, unsecured objects that are completely within the area of effect are automatically pushed 10 feet away from you by the spell’s effect, and the spell emits a thunderous boom audible out to 300 feet.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arcane-shield-shatter-dispel-magic-lesser": {
    name: "Arcane Shield Shatter (Dispel Magic, Lesser)",
    level: 1,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You can use this spell to attempt to dispel one ongoing magical effect of 1st level or lower (such as *shield*, *mage armor*, or *protection from evil*). Make a caster level check (1d20 + your caster level, maximum +5) against a DC of 11 + the spell effect’s caster level. If successful, the spell ends. Alternatively, if targeted at a creature currently benefiting from a *shield* spell or similar 1st-level force-based defensive effect, this spell automatically dispels that effect and deals 1d8 points of force damage to the creature.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "scorching-raystorm-scorching-ray": {
    name: "Scorching Raystorm (Scorching Ray)",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You blast your enemies with fiery rays. You can fire one ray, plus one additional ray for every four caster levels beyond 3rd (to a maximum of three rays at 11th level). Each ray requires a ranged touch attack to hit and deals 4d6 points of fire damage. The rays may be fired at the same or different targets, but all rays must be aimed at targets within 30 feet of each other and fired simultaneously.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "lightning-pulse-lightning-bolt-lesser": {
    name: "Lightning Pulse (Lightning Bolt - Lesser)",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You release a powerful stroke of electrical energy that deals 3d6 points of electricity damage to each creature within its area. The bolt begins at your fingertips. The lightning bolt sets fire to combustibles and damages objects in its path. It can melt metals with a low melting point, such as lead, gold, copper, silver, or bronze.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arcane-implosion-shatter": {
    name: "Arcane Implosion (Shatter)",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a sudden, intense vibration in a nonmagical object of up to 10 pounds per caster level or a crystalline creature. The spell deals 1d6 points of sonic damage per caster level (maximum 10d6) to the object or creature. If the target is a creature, it can attempt a Fortitude save for half damage. If the damage is sufficient to destroy the object or creature, it explodes in a shower of fragments, dealing 1d6 points of piercing damage to all creatures within 5 feet (Reflex save for no damage). Alternatively, you can target a point in space and create a 5-foot-radius sonic burst that deals 4d6 points of force/sonic damage to all creatures in the area (Fortitude save for half) and makes unattended crystalline or brittle objects shatter.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "flaming-sphere": {
    name: "Flaming Sphere",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "A burning globe of fire rolls in whichever direction you point and burns those it strikes. It moves 30 feet per round. As part of this movement, it can ascend or jump up to 30 feet to strike a target. If it enters a space with a creature, it stops moving for the round and deals 3d6 points of fire damage to that creature, though a successful Reflex save negates the damage. A flaming sphere rolls over barriers less than 4 feet tall. It ignites flammable substances it touches and illuminates the same area as a torch. You can direct the sphere as a move action.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "gust-of-wind": {
    name: "Gust of Wind",
    level: 2,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell creates a severe blast of air (approximately 50 mph) that originates from you, affecting all creatures in its path. Creatures of size Small or smaller are knocked prone and rolled 1d4×10 feet away from you. Medium creatures are knocked prone. Large creatures are checked. Huge or larger creatures are unaffected. Flying creatures are blown back 2d6×10 feet. The gust automatically extinguishes candles, torches, and similar unprotected flames. It causes protected flames, such as those of lanterns, to dance wildly and has a 50% chance to extinguish them.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "flame-geyser-fireball": {
    name: "Flame Geyser (Fireball)",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "A fireball spell is an explosion of flame that detonates with a low roar and deals 1d6 points of fire damage per caster level (maximum 10d6) to every creature within the area. Unattended objects also take this damage. The explosion creates almost no pressure. You point your finger and determine the range (distance and height) at which the fireball is to burst. A glowing, pea-sized bead streaks from the pointing digit and, unless it impacts upon a material body or solid barrier prior to attaining the prescribed range, blossoms into the fireball at that point. If you attempt to send the bead through a narrow passage, such as through an arrow slit, you must “hit” the opening with a ranged touch attack, or else the bead strikes the barrier and detonates prematurely. The fireball sets fire to combustibles and damages objects in the area. It can melt metals with a low melting point, such as lead, gold, copper, silver, or bronze.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "chain-lightning-jr-lightning-bolt": {
    name: "Chain Lightning Jr. (Lightning Bolt)",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You release a powerful stroke of electrical energy that deals 1d6 points of electricity damage per caster level (maximum 10d6) to each creature within its area. The bolt begins at your fingertips. The lightning bolt sets fire to combustibles and damages objects in its path. It can melt metals with a low melting point, such as lead, gold, copper, silver, or bronze. Alternatively, you can choose to have the lightning strike a primary target for full damage, then arc to up to two additional targets within 30 feet of the primary (or each other), each taking half the damage rolled for the primary target.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "shardstorm-ice-storm-modified": {
    name: "Shardstorm (Ice Storm - modified)",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Great magical hailstones pound down in a cylinder 20 feet in radius and 40 feet high. Each creature in the cylinder takes 3d6 points of bludgeoning damage from the impact of the hailstones. Additionally, the area is filled with a storm of razor-sharp ice shards, dealing 5d4 points of piercing and cold damage to creatures in the area (Reflex save for half). This spell does not create a slippery surface.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arc-flash-daylight-modified": {
    name: "Arc Flash (Daylight - modified)",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a blinding flash of arcane lightning. The spell brings forth light in a 60-foot radius. Creatures within 20 feet of the center of this flash must make a Reflex save or be blinded for 1d4 rounds. Additionally, these creatures take 3d6 points of electricity damage (Fortitude save for half). Creatures with light sensitivity are particularly affected by the flash.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "sleet-storm": {
    name: "Sleet Storm",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Driving sleet blocks all sight (even darkvision) within it and causes the ground in the area to be icy. A creature can walk within or through the area of sleet at half normal speed with a DC 10 Acrobatics check. Failure means it can’t move in that round, while failure by 5 or more means it falls. The sleet extinguishes torches and small fires.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "wind-wall": {
    name: "Wind Wall",
    level: 3,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "An invisible vertical curtain of wind appears. It is 2 feet thick and of considerable strength. It is a solid wall of wind, and any creature attempting to pass through it must make a Strength check (DC 10 + caster level) or be unable to penetrate. Loose materials and cloth garments fly upward when caught in a wind wall. Arrows and bolts are deflected upward and miss, while any other normal ranged weapon passing through the wall has a 30% miss chance. (Giant-thrown boulders, siege engine projectiles, and other massive ranged weapons are not affected.) Gases, most gaseous breath weapons, and creatures in gaseous form cannot pass through the wall (although it is no barrier to incorporeal creatures). While the wall must be vertical, you can shape it in a curve. The wind wall can be made into a ringed wall with a 5-foot radius.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "inferno-wave-wall-of-fire": {
    name: "Inferno Wave (Wall of Fire)",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "An immobile, blazing curtain of shimmering violet fire springs into existence. One side of the wall, selected by you, sends forth waves of heat, dealing 2d4 points of fire damage to creatures within 10 feet and 1d4 points of fire damage to those past 10 feet but within 20 feet. The wall deals this damage when it appears and on your turn each round to all creatures in the area. In addition, the wall deals 2d6 points of fire damage + 1 point of fire damage per caster level (maximum +20) to any creature that passes through it. The wall also deals this damage to any creature that ends its turn within 10 feet of the wall on the heated side. If any 5-foot length of wall takes 20 points of cold damage or more in 1 round, it is temporarily suppressed (it does not deal damage that round). An opaque wall of fire blocks line of sight. The \"Inferno Wave\" concept can be represented by the heat radiating from this wall and the damage on passing through.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "orb-of-annihilation-orb-of-force": {
    name: "Orb of Annihilation (Orb of Force)",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You project a globe of shimmering force. You must succeed on a ranged touch attack to hit your target. The orb deals 1d6 points of force damage per two caster levels (maximum 5d6 at 10th level). For every two dice of damage, the orb also has a chance to knock the target prone; the target must make a Reflex save or be knocked down. (e.g., at 4d6 damage, DC is based on a 4th level spell). This is a more controlled force effect than a pure annihilation, fitting the Orb theme.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "freezing-rain-ice-storm": {
    name: "Freezing Rain (Ice Storm)",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Great magical hailstones pound down in a cylinder 20 feet in radius and 40 feet high. Each creature in the cylinder takes 3d6 points of bludgeoning damage and 2d6 points of cold damage. This spell does not create a slippery surface but the sheer volume of ice and hail makes the area difficult terrain for 1 round after the spell ends.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "voltaic-detonation-shout": {
    name: "Voltaic Detonation (Shout)",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You emit an ear-splitting yell infused with electrical energy that deafens and damages creatures in its path. Any creature within the area is deafened for 2d6 rounds and takes 5d6 points of sonic/electricity damage. A successful save negates the deafness and halves the damage. Any exposed brittle or crystalline object or crystalline creature takes 1d6 points of sonic/electricity damage per caster level (maximum 15d6). An affected creature is stunned for 1 round if it fails its save against the damage.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "resilient-sphere": {
    name: "Resilient Sphere",
    level: 4,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "A globe of shimmering force encloses a creature, provided the creature is small enough to fit within the diameter of the sphere (the sphere can be up to 1 foot in diameter per caster level). The sphere is not subject to damage of any sort except from a *disintegrate* spell or a *rod of cancellation*, *sphere of annihilation*, or *Mordenkainen’s disjunction*. These effects destroy the sphere without harm to the subject. Nothing can pass through the sphere, inside or out, though the subject can breathe normally. The sphere negates all targeted spells and effects. Area effects that include the sphere are not affected by it. The subject may struggle, but the sphere cannot be physically moved either by people outside it or by the struggles of those within.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "flame-typhoon-cone-of-cold-fire-version": {
    name: "Flame Typhoon (Cone of Cold - Fire version)",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Cone of cold deals 1d6 points of fire damage per caster level (maximum 15d6). The cone of fire is so intense it can briefly create a vortex effect, pulling unsecured Small or smaller objects towards the caster within the first 10 feet of the cone. Creatures caught in the cone take fire damage. (Adapting Cone of Cold to a fire theme for \"Flame Typhoon\").",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "frozen-tomb-wall-of-force-icy-prison": {
    name: "Frozen Tomb (Wall of Force - Icy Prison)",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You conjure a prison of magical ice and force around a single creature. The target must make a Reflex save. If it fails, it is encased in a tomb of shimmering, ice-hard force. The tomb is immobile and impervious to most damage (similar to *wall of force*). The creature inside is trapped. Each round on its turn, the trapped creature takes 5d8 points of cold damage and must make a Fortitude save or be paralyzed for that round by the intense cold. The tomb melts away when the spell ends. A creature can attempt to break free with a Strength check (DC 25) as a full-round action, but takes the cold damage and paralysis check regardless.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "meteor-spear-flame-strike-modified": {
    name: "Meteor Spear (Flame Strike - modified)",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You call down a column of roaring flame, shot through with streaks of molten rock, to smite an area. The spell deals 1d6 points of damage per caster level (maximum 15d6). Half the damage is fire damage, but the other half results directly from divine power and is therefore not subject to being reduced by resistance to fire-based attacks. This functions as a vertical spear of meteoric impact.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arc-surge-chain-lightning-lesser": {
    name: "Arc Surge (Chain Lightning - Lesser)",
    level: 5,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell creates an electrical discharge that begins as a single stroke commencing from your fingertips. Unlike *lightning bolt*, *chain lightning* strikes one object or creature initially, then arcs to other targets. The bolt deals 1d6 points of electricity damage per caster level (maximum 15d6) to the primary target. After it strikes, lightning can arc to a number of secondary targets equal to your caster level (maximum 15). The secondary bolts each strike one target and deal half the damage dealt to the primary target. You choose secondary targets as you like, but they must all be within 30 feet of the primary target, and no target can be struck more than once. You can choose to affect fewer secondary targets than the maximum.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "solar-flare-sunburst-modified": {
    name: "Solar Flare (Sunburst - modified)",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Sunburst causes a globe of searing radiance to explode silently from a point you select. All creatures in the globe are blinded and take 6d6 points of fire damage. A successful Reflex save negates the blindness and reduces the damage to half. Undead creatures, and creatures particularly vulnerable to light (such as certain oozes and fungi), take 1d6 points of fire damage per caster level (maximum 20d6), and they are destroyed utterly if they fail their saves. The ultraviolet light generated by the spell deals damage to fungi, mold, oozes, and slimes as if they were undead creatures. This functions as a powerful flashbang and area denial.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "absolute-zero-otiluke-s-freezing-sphere-modified": {
    name: "Absolute Zero (Otiluke's Freezing Sphere - modified)",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You can use this spell in two ways:",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arcane-mortar-acid-fog": {
    name: "Arcane Mortar (Acid Fog)",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell creates a roiling cloud of acidic fog similar to *fog cloud*, except that its vapors are highly acidic. In addition to the effects of *fog cloud* (obscuring sight), creatures in the acid fog take 2d6 points of acid damage each round on your turn. This functions as a persistent area denial, like an arcane mortar shelling an area with acid.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "sonic-collapse-shout-greater": {
    name: "Sonic Collapse (Shout, Greater)",
    level: 6,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell functions like *shout*, except that it deals 10d6 points of sonic damage, and the deafness lasts for 4d6 rounds. A successful save negates the deafness and halves the damage. Any exposed brittle or crystalline object or crystalline creature takes 1d6 points of sonic damage per caster level (maximum 20d6). An affected creature is stunned for 1d4 rounds if it fails its save against the damage. The sheer force can cause collapse in weak structures (GM discretion).",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "lightning-grave-delayed-blast-fireball-lightning-version": {
    name: "Lightning Grave (Delayed Blast Fireball - Lightning Version)",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "A small, glowing bead of electrical energy streaks from your pointing finger to a point you choose within range, where it blossoms into a roaring sphere of lightning. The spell functions like *fireball*, except that it deals electricity damage. You can choose to have the bead detonate on impact, or you can delay the detonation for up to 5 rounds. You select the length of the delay at the time of casting, and the delay cannot be changed once set unless you concentrate on the bead. If you concentrate, you can choose to have the bead detonate at any time during the concentration. If you cease concentrating before the chosen delay is reached, the bead detonates immediately. The bead explodes if it strikes a solid barrier before reaching the target point. The lightning deals 1d6 points of electricity damage per caster level (maximum 20d6). The \"Lightning Grave\" concept is that if a creature is marked (i.e., the bead is near them) and they move or act in a way that triggers the detonation, it explodes.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "pyroclasm-fire-storm": {
    name: "Pyroclasm (Fire Storm)",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "A fire storm spell creates a maelstrom of roaring flame. The spell deals 1d6 points of fire damage per caster level (maximum 20d6) to all creatures and objects within its area. You can choose to affect an area as small as a single 10-foot cube, or a number of 10-foot cubes equal to your caster level. These cubes must be contiguous. The fire damages objects in the area and ignites combustibles. If a creature is in an area of fire storm for more than 1 round, it takes damage each round on your turn.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "frost-reaver-control-weather-localized-blizzard": {
    name: "Frost Reaver (Control Weather - Localized Blizzard)",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You alter the weather in the local area. It takes 10 minutes to cast the spell and an additional 10 minutes for the effects to manifest. You can call forth a localized blizzard (extreme cold, heavy snow, strong winds) in a 1-mile radius centered on a point you choose within the spell's range. Creatures in the blizzard take 1d6 cold damage per 10 minutes of exposure, visibility is severely limited, and movement is hampered. The \"Frost Reaver\" aspect is that a specific target you designate when casting (if within the blizzard's initial area) takes 8d8 cold damage immediately when the blizzard manifests and is slowed (as the *slow* spell) for as long as they remain in the blizzard, with no save against the initial damage or slow if they are the designated target. The general blizzard effects apply to all others.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "arcbolt-singularity-prismatic-spray": {
    name: "Arcbolt Singularity (Prismatic Spray)",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell causes seven shimmering, multicolored beams of light to spray from your hand. Each beam has a different power. Creatures in the area of the spell with 8 HD or less are automatically blinded for 2d4 rounds. Every creature in the area is randomly struck by one or more beams, which have additional effects:",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "mordenkainen-s-sword": {
    name: "Mordenkainen’s Sword",
    level: 7,
    school: "Evocation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create a sword-shaped plane of force that hovers in the air and attacks opponents at a distance, as you direct it, starting in the round that you cast the spell. The sword attacks with your base attack bonus (possibly allowing it multiple attacks per round in subsequent rounds) plus your spellcasting ability modifier as an attack bonus. It deals 4d6+3 points of force damage. The sword always strikes from your direction. It cannot flank targets as a creature could. If the sword goes beyond the spell range, if it goes out of your sight, or if you are not directing it, the sword returns to you and hovers.",
    classes: ["Crimson Agent", "Dragoon", "Mage", "Warrior"]
  },
  "minor-image": {
    name: "Minor Image",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Visual illusion fits in 5-ft cube; lasts 1 round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "flickerstep": {
    name: "Flickerstep",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Brief displacement: +1 AC vs one attack.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "silent-echo": {
    name: "Silent Echo",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Mimics last word or phrase said within 10 ft.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mirage-spark": {
    name: "Mirage Spark",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "1d4 psychic if target fails INT save; believes they are burned.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "illusive-flash": {
    name: "Illusive Flash",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Disorienting burst; next enemy attack roll is at Disadvantage.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "shadow-puppet": {
    name: "Shadow Puppet",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Move small object or shadow in 10 ft radius.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "blurred-visage": {
    name: "Blurred Visage",
    level: 0,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Caster gains half cover vs ranged for 1 round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "illusory-blade": {
    name: "Illusory Blade",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Melee spell attack; 2d6 psychic, target thinks they’re stabbed.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "veil-of-mist": {
    name: "Veil of Mist",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Light fog illusion, 20 ft radius; grants concealment.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "phantom-grasp": {
    name: "Phantom Grasp",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Spectral hand grabs target: 1d6 psychic, DEX save or restrained 1 round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mask-voice": {
    name: "Mask Voice",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Mimic another voice within 60 ft; WIS save to detect.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "false-footsteps": {
    name: "False Footsteps",
    level: 1,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Cause audible steps in direction of choice; lasts 3 rounds.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "phantom-decoy": {
    name: "Phantom Decoy",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Exploding image of caster; 2d6 psychic in 10-ft burst on detonation.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "illusory-flames": {
    name: "Illusory Flames",
    level: 2,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target believes they are on fire: 3d6 psychic, panicked if fail WIS.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "phantasmal-force": {
    name: "Phantasmal Force",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target perceives dangerous illusion; 1d6 psychic/round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "cloak-of-shades": {
    name: "Cloak of Shades",
    level: 3,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Grants invisibility in dim light or darkness.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mind-maze": {
    name: "Mind Maze",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target loses 1 round in confusion unless WIS save passed.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "illusory-clone": {
    name: "Illusory Clone",
    level: 4,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Clone mimics caster’s movements, swaps place once per round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mass-mirage": {
    name: "Mass Mirage",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Up to 6 targets appear as others; includes voice and silhouette.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "veil-of-terror": {
    name: "Veil of Terror",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Enemy sees worst fear; WIS save or frightened + 4d6 psychic.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "echofield": {
    name: "Echofield",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Area repeats sounds randomly; stealth impossible, confuses enemies.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "phantom-swarm": {
    name: "Phantom Swarm",
    level: 5,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Illusory insects deal 5d6 psychic, targets must move away.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "greater-phantasmal-killer": {
    name: "Greater Phantasmal Killer",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target takes 4d6 psychic/round, WIS save ends.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "spectral-army": {
    name: "Spectral Army",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Summon 5 ghostly soldiers: all fake, 6d6 AoE psychic when attacked.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "invisible-tide": {
    name: "Invisible Tide",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Creatures in 30 ft must DEX save or be knocked prone (illusory wave).",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "reality-fracture": {
    name: "Reality Fracture",
    level: 6,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Field of unreality; all creatures see different illusions.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mirage-legion": {
    name: "Mirage Legion",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Creates 6 illusory duplicates that cast harmless spells.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "inescapable-labyrinth": {
    name: "Inescapable Labyrinth",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target sees ever-shifting terrain, WIS save or speed 0.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "perfect-veil": {
    name: "Perfect Veil",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Caster and up to 3 allies become completely unnoticeable unless interacted with.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mindtrap-echo": {
    name: "Mindtrap Echo",
    level: 7,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "WIS save or target repeats last spell or action, confused.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mass-hallucination": {
    name: "Mass Hallucination",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "30-ft radius: All enemies see entire battlefield differently.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "phantom-execution": {
    name: "Phantom Execution",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target believes they are dying; drops to 0 HP illusionarily.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "reality-rewrite": {
    name: "Reality Rewrite",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Convince one creature reality has changed; WIS save or stunned.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "illusory-wall-of-doom": {
    name: "Illusory Wall of Doom",
    level: 8,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Huge wall appears to collapse: creatures take 8d6 psychic and fall prone.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "supreme-illusion": {
    name: "Supreme Illusion",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Imitate any spell of 6th level or lower; must convince target.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mass-phantom-killer": {
    name: "Mass Phantom Killer",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Up to 5 enemies take 6d6 psychic/round; WIS save ends.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mind-collapse": {
    name: "Mind Collapse",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target stunned for 3 rounds, INT save ends early.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "astral-shell": {
    name: "Astral Shell",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Protective illusion that grants full resistance to damage types for 1 minute.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "mirrored-world": {
    name: "Mirrored World",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Entire battlefield appears mirrored; enemies must roll twice to hit.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "ethereal-disjunction": {
    name: "Ethereal Disjunction",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Enemies partially phased, 50% chance to miss attacks and spells.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "unravel-identity": {
    name: "Unravel Identity",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target loses all class abilities for 1 round, believes they are someone else.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "phantom-cataclysm": {
    name: "Phantom Cataclysm",
    level: 9,
    school: "Illusion",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Enemies believe world ends: 12d10 psychic, stunned 1 round.",
    classes: ["Bard", "Crimson Agent", "Mirrorsage", "Monk", "Thief"]
  },
  "finger-of-the-dead": {
    name: "Finger of the Dead",
    level: 0,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "1d4 necrotic, heal 1 HP.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "putrefy": {
    name: "Putrefy",
    level: 1,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Corpse unusable for divine magic.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "fearmonger-s-cry": {
    name: "Fearmonger’s Cry",
    level: 3,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "15-ft cone, WIS save or flee.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "summon-death-knight": {
    name: "Summon Death Knight",
    level: 5,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You summon a powerful undead warrior, a Death Knight, clad in ominous black armor. It appears where you designate and acts immediately, on your turn. It wields a greatsword imbued with shadowy energy. If you can communicate with it, you can direct its actions. The Death Knight is a Large undead creature with 80 HP, AC 18, and makes two attacks per round with its greatsword, each dealing 2d8 slashing damage + 1d8 necrotic damage. It has standard undead traits, resistance 10 to cold and electricity, and DR 5/bludgeoning or magic. It also possesses an Aura of Despair (enemies within 10 feet take a -2 penalty on saving throws against fear effects).",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "mass-decay": {
    name: "Mass Decay",
    level: 5,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You unleash a wave of potent necrotic energy, causing flesh to rapidly decay. All enemies within a 30-foot radius take 4d8 points of necrotic damage immediately. Additionally, any enemy that fails a Fortitude save takes an additional 2d6 points of necrotic damage each round for the next 3 rounds as the decay continues to ravage their bodies.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "command-undeath": {
    name: "Command Undeath",
    level: 6,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Permanently bind up to 2 CR 2 undead to caster.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "summon-archlich-shade": {
    name: "Summon Archlich Shade",
    level: 8,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You summon a powerful Archlich Shade, an echo of a once-mighty undead sorcerer. It appears where you designate and acts immediately, on your turn. It is wreathed in dark energies and can cast a variety of necromantic spells. If you can communicate with it, you can direct its actions. The Archlich Shade is a Medium undead creature with 160 HP, AC 22 (natural armor, deflection), and has a touch attack dealing 2d8 cold damage + 1d6 Constitution drain. It can cast *finger of death*, *vampiric touch*, and *enervation* 3 times per day each (as if cast by a 15th-level sorcerer, save DCs are Charisma-based for the Shade). It has DR 15/bludgeoning and good, spell resistance 25, and standard undead traits.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "mass-resurrection-denial": {
    name: "Mass Resurrection Denial",
    level: 8,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create an area suffused with powerful negative energy that thwarts attempts to restore life. Any attempt to cast a spell that raises a creature from the dead (such as *raise dead*, *resurrection*, *true resurrection*, or *reincarnate*) within this area automatically fails if the spell is of 7th level or lower. Spells of 8th or 9th level have a 50% chance of failure. This spell does not prevent creatures from being healed or stabilized, only from being brought back from death.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "soul-pyre": {
    name: "Soul Pyre",
    level: 8,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You target a single corpse within range, causing it to erupt in a violent explosion of soul-fueled fire and necrotic energy. All creatures within a 20-foot radius of the exploding corpse take 8d6 points of fire damage and 8d6 points of necrotic damage (Reflex save for half of both types of damage). The targeted corpse is utterly consumed in the process.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "doom": {
    name: "Doom",
    level: 9,
    school: "Necromancy",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target suffers 10d6 necrotic over 5 rounds and cannot heal.",
    classes: ["Cleric", "Crimson Agent", "Druid", "Shaman", "Thief"]
  },
  "snap-freeze": {
    name: "Snap Freeze",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Chill a drink, preserve food, or freeze a 1-ft square.",
    classes: ["Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "snap-freeze-gentle-warmth-2": {
    name: "Snap Freeze / Gentle Warmth",
    level: 0,
    school: "Transmutation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You can instantly chill or warm a small, non-living object or a small quantity of liquid. You can make a drink cold, preserve food for a few extra hours by chilling it, or freeze a 1-foot square patch of water (if thin enough). Alternatively, you can make a drink pleasantly warm or slightly thaw a frozen object. This cannot cause damage.",
    classes: ["Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "bull-s-strength": {
    name: "Bull’s Strength",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "The subject becomes stronger. The spell grants a +4 enhancement bonus to Strength, adding the usual benefits to melee attack rolls, melee damage rolls, and other uses of the Strength modifier.",
    classes: ["Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "cat-s-grace": {
    name: "Cat’s Grace",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "The subject becomes more graceful, agile, and coordinated. The spell grants a +4 enhancement bonus to Dexterity, adding the usual benefits to AC, Reflex saves, and other uses of the Dexterity modifier.",
    classes: ["Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "bear-s-endurance": {
    name: "Bear’s Endurance",
    level: 2,
    school: "Transmutation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "The subject becomes more resilient and healthier. The spell grants a +4 enhancement bonus to Constitution, adding the usual benefits to hit points, Fortitude saves, and other uses of the Constitution modifier.",
    classes: ["Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "water-breathing": {
    name: "Water Breathing",
    level: 3,
    school: "Transmutation",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "The transmuted creatures can breathe water freely. Divide the duration evenly among all the creatures you touch. The spell does not make creatures unable to breathe air.",
    classes: ["Dragoon", "Druid", "Mage", "Monk", "Ranger", "Shaman", "Soldier", "Thief", "Tinker", "Warrior"]
  },
  "magic-thread": {
    name: "Magic Thread",
    level: 1,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You imbue an object or willing creature with a minor magical effect that is triggered by a specific condition you set (e.g., a spoken word, a touch from a specific person, opening a container). The effect must be a cantrip you know. When the trigger condition occurs, the cantrip effect manifests as if you had cast it. The magic thread then dissipates. You can only have one magic thread active at a time.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "unravel-spell-2": {
    name: "Unravel Spell",
    level: 3,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Dispel any spell effect up to 4th level.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "mystic-gate-2": {
    name: "Mystic Gate",
    level: 4,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Summon a two-way portal for 1 minute between two points.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "planar-gate-2": {
    name: "Planar Gate",
    level: 5,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Create a portal to another plane for 1 minute.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "dimensional-shift-2": {
    name: "Dimensional Shift",
    level: 3,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Swap positions with any target within 100 ft.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "arcane-clone-2": {
    name: "Arcane Clone",
    level: 6,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Create 1 illusionary copy of caster for 3 rounds.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "spell-sculptor-2": {
    name: "Spell Sculptor",
    level: 6,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Reshape AoE spells to exclude allies.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "chain-gate-2": {
    name: "Chain Gate",
    level: 7,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Summon 3 linked portals in rapid sequence.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "cast-echo-2": {
    name: "Cast Echo",
    level: 7,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Repeat any spell cast within the last 3 rounds.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "erase-from-reality-2": {
    name: "Erase from Reality",
    level: 7,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Target is untargetable for 1 round; memory fades temporarily.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "meta-surge-2": {
    name: "Meta Surge",
    level: 7,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "For 1 minute, all metamagic effects cost no extra resources.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "dimensional-break-2": {
    name: "Dimensional Break",
    level: 8,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Tear open unstable gate: 8d10 force + banish 1 enemy.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "reality-patch-2": {
    name: "Reality Patch",
    level: 8,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Stabilize an unstable zone, spell, or planar rift.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "time-echo-2": {
    name: "Time Echo",
    level: 8,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You and 1 ally repeat full last round of actions.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "absolute-gate-2": {
    name: "Absolute Gate",
    level: 9,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Permanent portal to any known plane or place.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "world-rewrite-2": {
    name: "World Rewrite",
    level: 9,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Recast any 1 spell you’ve ever known; counts as 9th level.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "planar-collapse-2": {
    name: "Planar Collapse",
    level: 9,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Area ripped between dimensions: 12d6 force, prone, banished.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "perfect-spell-2": {
    name: "Perfect Spell",
    level: 9,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Cast any spell ignoring components, costs, and casting time.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "unmake-spell-2": {
    name: "Unmake Spell",
    level: 9,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Erase a spell from enemy memory; they can no longer cast it.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "collapse-timeline-2": {
    name: "Collapse Timeline",
    level: 9,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "Force entire battlefield into alternate future: GM determines outcome.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "fabricate": {
    name: "Fabricate",
    level: 5,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You convert raw materials into finished items of the same material. For example, you can fabricate a wooden bridge from a clump of trees, a cloth gown from a pile of wool, or a stone statue from a rock. The quality of items made by this spell is commensurate with the quality of material used as a component for the spell. The casting time depends on the volume of material and complexity of the item, typically 1 round per 10 cubic feet of material for simple items, or 1 minute per cubic foot for complex items. You must make an appropriate Craft check to make complex items.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "phase-door": {
    name: "Phase Door",
    level: 7,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "You create an ethereal passage through a wooden, plaster, or stone wall. The passage is invisible and intangible from the Ethereal Plane. From the Material Plane, it looks like a faint, shimmering outline of a door. You (and any creature you designate who is touching you when you cast the spell) can use the *phase door* once per two caster levels. Each use allows a creature to pass through the wall in either direction. The passage does not permit light, sound, or spell effects to pass through it. The *phase door* is subject to *dispel magic*.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "leyline-flow-symbol-of-death": {
    name: "Leyline Flow (Symbol of Death)",
    level: 8,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "This spell allows you to scribe a potent rune of power upon a surface. When triggered, a *symbol of death* kills one or more creatures within 60 feet of the symbol (treat as a burst) whose combined total current hit points do not exceed 150. The *symbol of death* affects the closest creatures first, skipping creatures with too many hit points to affect. Once triggered, the symbol becomes active and glows, lasting for 10 minutes per caster level or until it has affected 150 HD of creatures. A creature that succeeds on a Fortitude save is not killed, but takes 6d6 points of negative energy damage. The symbol is triggered whenever a creature does one or more of the following, as you select: looks at the rune; reads the rune; touches the rune; passes over the rune; passes through a portal bearing the rune.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  },
  "unmake-spell-mage-s-disjunction": {
    name: "Unmake Spell (Mage’s Disjunction)",
    level: 9,
    school: "Universal",
    castingTime: "1 action",
    range: "See spell description",
    components: "V, S",
    duration: "Instantaneous",
    description: "All magical effects and magic items within the radius of the spell, except for those on your person, are disjoined. That is, spells and spell-like effects are separated into their individual components (ending the effect as a *greater dispel magic* spell does), and each permanent magic item must make a Will save or be turned into a normal item. An item in a creature’s possession uses its own Will save bonus or its possessor’s Will save bonus, whichever is higher. If an artifact is targeted, there is a 1% chance per caster level that the *mage’s disjunction* works. If it fails, the artifact is unaffected. If it succeeds, the artifact’s functions are suppressed for 1d4 rounds.",
    classes: ["Bard", "Cleric", "Mage", "Mirrorsage", "Oracle", "Paladin", "Soldier", "Tinker", "Warrior"]
  }
};

// Utility functions for spell filtering and searching
export function getSpellsBySchool(school) {
  return Object.values(SPELLS).filter(spell => spell.school === school);
}

export function getSpellsByLevel(level) {
  return Object.values(SPELLS).filter(spell => spell.level === level);
}

export function getSpellsByClass(className) {
  return Object.values(SPELLS).filter(spell => spell.classes.includes(className));
}

export function searchSpells(query) {
  const lowercaseQuery = query.toLowerCase();
  return Object.values(SPELLS).filter(spell => 
    spell.name.toLowerCase().includes(lowercaseQuery) ||
    spell.description.toLowerCase().includes(lowercaseQuery) ||
    spell.school.toLowerCase().includes(lowercaseQuery)
  );
}

export function getSpellsBySchoolAndLevel(school, level) {
  return Object.values(SPELLS).filter(spell => 
    spell.school === school && spell.level === level
  );
}

export function getCantrips() {
  return Object.values(SPELLS).filter(spell => spell.level === 0);
}

export function getHighLevelSpells(minLevel = 6) {
  return Object.values(SPELLS).filter(spell => spell.level >= minLevel);
}

export function getSpellCount() {
  return Object.keys(SPELLS).length;
}

export function getSpellsByComponent(component) {
  return Object.values(SPELLS).filter(spell => 
    spell.components.toLowerCase().includes(component.toLowerCase())
  );
}

export function getSpellsByDuration(durationType) {
  return Object.values(SPELLS).filter(spell => 
    spell.duration.toLowerCase().includes(durationType.toLowerCase())
  );
}

export default SPELLS;
