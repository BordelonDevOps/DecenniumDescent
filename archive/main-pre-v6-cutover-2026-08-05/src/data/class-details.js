/** Combat, proficiency, and level features keyed by class name (rulebook canon).
 * 17 entries match CANON_CLASSES; Swashbuckler is orphan reference only (not selectable).
 */
import classPaths from "./class-paths";
import classDraftLevels from "./class-draft-levels";
import { CANON_CLASSES, isCanonClass } from "./canon-classes";

export { CANON_CLASSES, isCanonClass };

export const classDetails = {
  Bard: {
    armor: ["Light armor"],
    weapons: ["Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
    tools: ["Three musical instruments"],
    skills: ["Choose any 3"],
    combat: ["Crescendo die (d6)", "Bardic Inspiration", "Song as bonus action focus"],
    levels: {
      1: ["Spellcasting", "Bardic Inspiration", "Crescendo (d6)"],
      2: ["Jack of All Trades", "Song of Rest"],
      3: ["Bard College", "Expertise"],
      4: ["Ability Score Improvement"],
      5: ["Font of Inspiration", "Crescendo die (d8)"],
      6: ["Skill tree tier II unlock", "Counter-Melody or College feature"],
      8: ["Ability Score Improvement"],
      10: ["Hero Path selection (Harmony / Virtuoso / Discord)", "Prestige discovery eligible"],
    },
  },
  Cleric: {
    armor: ["Light armor", "Medium armor", "Shields"],
    weapons: ["Simple weapons"],
    tools: ["None"],
    skills: ["History", "Insight", "Medicine", "Persuasion", "Religion — choose 2"],
    combat: ["Channel Divinity", "Turn Undead / Domain feature", "Prepared divine spells"],
    levels: {
      1: ["Spellcasting", "Divine Domain", "Domain spells"],
      2: ["Channel Divinity (1/rest)", "Domain feature"],
      3: ["Domain spells (2nd circle)"],
      4: ["Ability Score Improvement"],
      5: ["Destroy Undead (CR 1/2)", "Domain feature"],
      6: ["Channel Divinity (2/rest)", "Domain tier II"],
      8: ["Ability Score Improvement", "Divine Strike or Potent Spellcasting"],
      10: ["Hero Path selection (Saint / Priest / Cultist)", "Gravetouched / Soulrender eligible"],
    },
  },
  "Crimson Agent": {
    armor: ["Light armor"],
    weapons: ["Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
    tools: ["Thieves' tools", "Disguise kit"],
    skills: ["Choose 4 from Agent list"],
    combat: ["Sneak Strike", "Marked Contract", "Third-caster spell slot progression"],
    levels: {
      1: ["Blood Mark", "Sneak Attack (1d6)", "Expertise (1)"],
      2: ["Cunning Action", "Contract Sense"],
      3: ["Skill tree tier I", "Sneak Attack (2d6)"],
      4: ["Ability Score Improvement"],
      5: ["Uncanny Dodge", "Sneak Attack (3d6)"],
      6: ["Skill tree tier II", "Bloodbound prestige eligible"],
      8: ["Ability Score Improvement"],
      10: ["Hero Path selection (Bloodweaver / Shadow Operative / Thirstborn)", "Hexblade / Soulrender / Warlock eligible"],
    },
  },
  Druid: {
    armor: ["Light armor", "Medium armor", "Shields (non-metal)"],
    weapons: ["Clubs", "Daggers", "Darts", "Javelins", "Maces", "Quarterstaffs", "Scimitars", "Sickles", "Slings", "Spears"],
    tools: ["Herbalism kit"],
    skills: ["Choose 2 from Nature list"],
    combat: ["Wild Shape", "Primal spellcasting", "Circle feature"],
    levels: {
      1: ["Druidcraft", "Spellcasting"],
      2: ["Wild Shape", "Druid Circle"],
      3: ["Circle feature", "2nd-level slots"],
      4: ["Wild Shape improvement", "Ability Score Improvement"],
      5: ["3rd-level slots"],
      6: ["Land's Stride (Circle of Land)", "Magical beast attacks (Wild Shape)"],
      8: ["Ability Score Improvement", "Wild Shape CR increase"],
      10: ["Nature's Ward / Hero Druid Forms (circle)", "Beastmaster / Verdant Animist / Mooncursed eligible"],
      12: ["Ability Score Improvement"],
      14: ["Circle capstone (Nature's Sanctuary, Elemental Shapeshifting, etc.)"],
      16: ["Ability Score Improvement"],
      18: ["Timeless Body", "Beast Spells (cast in beast shape)"],
      19: ["Ability Score Improvement"],
      20: ["Archdruid — unlimited Shapeshifting, ignore verbal/somatic/material components"],
    },
  },
  Mage: {
    armor: ["None"],
    weapons: ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
    tools: ["None"],
    skills: ["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion — choose 2"],
    combat: ["Arcane Recovery", "Spell school focus", "Ritual casting"],
    levels: {
      1: ["Spellcasting", "Arcane Recovery", "Cantrips"],
      2: ["Arcane Tradition / school focus", "Spellbook — prepare +1 additional spell per long rest"],
      3: ["2nd-level slots", "Tradition feature"],
      4: ["Ability Score Improvement"],
      5: ["3rd-level slots"],
      6: ["Skill tree tier II", "School focus feature"],
      8: ["Ability Score Improvement"],
      10: ["Hero Path selection (Archmage / Elementalist / Lich)", "Chronomancer / Echomancer / Warlock eligible"],
    },
  },
  /** draftCap: see class-ceiling-caps.js — echo slots, copy/round, RP floor */
  Mirrorsage: {
    armor: ["None"],
    weapons: ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
    tools: ["Crystal focus"],
    skills: ["Arcana", "History", "Insight", "Investigation", "Nature", "Perception — choose 3"],
    combat: ["Spell Mimicry", "Arcane Echo", "Adaptive Casting", "Draft cap: 1 copy release/round · 6 echo slots"],
    levels: {
      1: ["Spell Mimicry", "Arcane Echo"],
      2: ["Adaptive Casting"],
      3: ["Mirror Tradition"],
      4: ["Ability Score Improvement"],
      5: ["Stolen Cadence"],
      6: ["Mirror Pulse improvement", "Echomancer prestige eligible"],
      8: ["Ability Score Improvement"],
      10: ["Hero Path selection (Light Weaver / Mirror Mage / Shattered One)", "Perfect Reflection capstone eligible"],
    },
  },
  /** draftCap: see class-ceiling-caps.js — RC 3–7, 1 RC recovery/round, revelation/round */
  Oracle: {
    armor: ["Light armor", "Medium armor", "Shields"],
    weapons: ["Simple weapons"],
    tools: ["None"],
    skills: ["History", "Insight", "Medicine", "Persuasion", "Religion", "Spellcraft — choose 4"],
    combat: ["Oracle's Curse", "Mystery Revelations", "Revelation Charges (3–7, not spell slots)", "Draft cap: 1 RC recovery/round · 1 revelation/round"],
    levels: {
      1: ["Revelation Charges (3, max 7)", "Oracle's Curse", "Mystery"],
      2: ["Oracle's Burden"],
      3: ["Tier I Revelation"],
      4: ["Ability Score Improvement"],
      5: ["Mystery feature"],
      6: ["Tier II Revelation (choose 1)", "Mystery surge"],
      8: ["Ability Score Improvement"],
      9: ["Tier III Revelation (Mystery capstone, 3 charges)"],
      10: ["Curse Boon III", "Grand Revelation foreshadow"],
      12: ["Mystic Insight (Minor Revelation or passive)"],
      15: ["Revelation Mastery", "Curse Boon IV"],
      18: ["Prophetic Surge (1/day free or extended Revelation)"],
      20: ["Final Revelation", "Curse Boon V"],
    },
  },
  /** draftCap: see class-ceiling-caps.js — aura stacking, smite/spell/round, LoH spend */
  Paladin: {
    armor: ["All armor", "Shields"],
    weapons: ["Simple weapons", "Martial weapons"],
    tools: ["None"],
    skills: ["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion — choose 2"],
    combat: ["Divine Smite", "Lay on Hands", "Aura (later levels)", "Draft cap: 1 smite or spell/round · one aura radius"],
    levels: {
      1: ["Divine Sense", "Lay on Hands"],
      2: ["Fighting Style", "Spellcasting", "Divine Smite"],
      3: ["Sacred Oath", "Divine Health"],
      4: ["Ability Score Improvement"],
      5: ["Extra Attack"],
      6: ["Aura 15 ft — secondary benefit (DR, saves)"],
      7: ["Aura 15 ft — reactive Smite or spell trigger"],
      8: ["Ability Score Improvement"],
      10: ["Aura 20 ft — persists 1 round if incapacitated", "Hero Path / Oath Mastery eligible"],
      11: ["Signature Power (Oath-specific, 1/rest)"],
      13: ["Divine Resistance (fire, necrotic, or psychic)"],
      15: ["Aura 30 ft — debuff enemies or buff allies"],
      17: ["Lay on Hands: Full Cleansing Wave (1/rest)", "Aura Surge (1/rest)"],
      18: ["Divine Sense — detect disguised outsiders"],
      20: ["Final Oath Gift", "Divine Manifestation aura (auto on initiative)"],
    },
  },
  Ranger: {
    armor: ["Light armor", "Medium armor", "Shields"],
    weapons: ["Simple weapons", "Martial weapons"],
    tools: ["None"],
    skills: ["Choose 3 from Ranger list"],
    combat: ["Favored Terrain (Decennium floors)", "Hunter's Mark style focus", "Half-caster spells"],
    levels: {
      1: ["Favored Enemy", "Natural Explorer (floors)"],
      2: ["Fighting Style", "Spellcasting"],
      3: ["Ranger Archetype", "Primeval Awareness"],
      4: ["Ability Score Improvement"],
      5: ["Extra Attack"],
      6: ["Elemental Imbue (Pathfinder)", "Beastmaster / Giant Killer eligible"],
      8: ["Ability Score Improvement", "Land's Stride"],
      9: ["Predator's Mark (Pathfinder)"],
      10: ["Hero Path selection (Warder / Stalker / Outrider)", "Wyrmslayer eligible"],
    },
  },
  Shaman: {
    armor: ["Light armor", "Medium armor", "Shields"],
    weapons: ["Simple weapons"],
    tools: ["Herbalism kit"],
    skills: ["Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival — choose 4"],
    combat: ["Spirit Guide", "Elemental Channel", "Full caster"],
    levels: {
      1: ["Spellcasting", "Spirit Guide"],
      2: ["Elemental Channel"],
      3: ["Spirit path feature"],
      4: ["Ability Score Improvement"],
      5: ["3rd-level slots"],
      6: ["Totem Pulse (on placement)", "Storm Lord prestige eligible (Lv 6+)"],
      8: ["Ability Score Improvement"],
      9: ["Spirit Saturation — free totem cast per combat (Spiritwalker)"],
      10: ["Hero Path selection (Theurgist / Soothsayer / Bloodcaller)", "Verdant Animist eligible"],
    },
  },
  Soldier: {
    armor: ["All armor", "Shields"],
    weapons: ["Simple weapons", "Martial weapons"],
    tools: ["One gaming set", "Vehicles (land)"],
    skills: ["Athletics", "Intimidation", "Perception", "Survival — choose 2"],
    combat: ["Second Wind", "Action Surge (archetype)", "Formation training"],
    levels: {
      1: ["Fighting Style", "Second Wind"],
      2: ["Action Surge (1)", "Formation Drill"],
      3: ["Martial Archetype"],
      4: ["Ability Score Improvement"],
      5: ["Extra Attack", "Palisade Deployment (Commander, 2×1 barrier)"],
      6: ["Intercepting Shot (reaction)", "Sapper / Giant Killer eligible"],
      8: ["Ability Score Improvement"],
      9: ["Fortify Zone — −2 ranged attacks vs allies in 3×3 (Commander)"],
      10: ["Hero Path selection (Champion / Artillerist / Tyrant)", "Wyrmslayer eligible"],
    },
  },
  /** ORPHAN — not in rulebook Classes Table; kept for reference only. Not selectable in UI. */
  Swashbuckler: {
    armor: ["Light armor"],
    weapons: ["Simple weapons", "Martial weapons (finesse focus)"],
    tools: ["One gaming set", "One musical instrument"],
    skills: ["Acrobatics", "Athletics", "Deception", "Insight", "Persuasion", "Sleight of Hand — choose 3"],
    combat: ["Fancy Footwork", "Rakish strike", "Panache"],
    levels: {
      1: ["Fancy Footwork", "Rakish Audacity"],
      2: ["Cunning Action"],
      3: ["Panache"],
      4: ["Ability Score Improvement"],
      5: ["Extra Attack"],
      6: ["Panache tier II", "Blademaster / Bloodbound eligible"],
      8: ["Ability Score Improvement"],
      10: ["Elegant Maneuver", "Hexblade eligible"],
    },
  },
  Thief: {
    armor: ["Light armor"],
    weapons: ["Simple weapons", "Hand crossbows", "Longswords", "Rapiers", "Shortswords"],
    tools: ["Thieves' tools"],
    skills: ["Choose 4 from rogue list"],
    combat: ["Sneak Attack", "Cunning Action", "Thieves' Cant"],
    levels: {
      1: ["Expertise", "Sneak Attack (1d6)", "Thieves' Cant"],
      2: ["Cunning Action"],
      3: ["Thievish Archetype", "Sneak Attack (2d6)"],
      4: ["Ability Score Improvement"],
      5: ["Uncanny Dodge", "Sneak Attack (3d6)"],
      6: ["Trap Sense (Rake)", "Sapper prestige eligible"],
      8: ["Ability Score Improvement"],
      9: ["Shadow Stab — crit teleports through target, applies Bleed (Rake)"],
      10: ["Hero Path selection (Arcane Trickster / Shadowblade / Blackguard)", "Blademaster / Hexblade eligible"],
      13: ["Distraction Tactics — free disengage once per turn (Rake)"],
      15: ["Crippling Strike — Sneak Attack applies Slow (Rake)"],
    },
  },
  /** draftCap: see class-ceiling-caps.js — deployable count, HP/damage/duration, action economy */
  Tinker: {
    armor: ["Light armor", "Medium armor"],
    weapons: ["Simple weapons", "Hand crossbows", "Firearms (if allowed)"],
    tools: ["Tinker's tools", "One artisan's tools"],
    skills: ["Arcana", "History", "Investigation", "Medicine", "Nature", "Perception — choose 2"],
    combat: ["Magical Tinkering", "Infuse Item", "Companion chassis", "Draft cap: 3 deployables · 1 deploy + 1 detonation/round"],
    levels: {
      1: ["Magical Tinkering", "Infuse Item"],
      2: ["Tool Expertise", "Infusions known +1"],
      3: ["Tinker Specialist"],
      4: ["Ability Score Improvement"],
      5: ["Companion Chassis prototype", "Extra Attack (tool-arm)"],
      6: ["Deploy Sentry Turret", "Deploy Net Trap", "Forge Master / Sapper eligible"],
      8: ["Ability Score Improvement"],
      9: ["Remote Detonation (Mechanist)"],
      10: ["Hero Path selection (Artificer / Techsmith / Warmachine)", "Apex gadget tier"],
    },
  },
  /** draftCap: see class-ceiling-caps.js — mutation slots, activations/round, Brutality Threshold */
  Warrior: {
    armor: ["All armor", "Shields"],
    weapons: ["Simple weapons", "Martial weapons"],
    tools: ["None"],
    skills: ["Choose 2 from Warrior list"],
    combat: ["Fighting Style", "Extra Attack", "Indomitable (later)", "Draft cap: 3 mutations · 1 activation/round"],
    levels: {
      1: ["Fighting Style", "Second Wind"],
      2: ["Action Surge"],
      3: ["Martial Archetype"],
      4: ["Ability Score Improvement"],
      5: ["Extra Attack"],
      6: ["Bone Hardened — DR +1 while not staggered", "Battlemage / Berserker eligible"],
      8: ["Ability Score Improvement"],
      9: ["Serum Overclock — inject 2 serums at once"],
      10: ["Hero Path selection (Wardborn / Ironskin / Dreadspawn)", "Most martial prestige paths eligible"],
      13: ["Mutation Slot III"],
      15: ["Brutal Adaptation — passive bonus from a mutation"],
      17: ["Reflexive Mutation — mutate reactively once per round"],
      20: ["Apex Form — 4th mutation slot, once/encounter ultimate form"],
    },
  },
  Wizard: {
    armor: ["None"],
    weapons: ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows"],
    tools: ["None"],
    skills: ["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion — choose 2"],
    combat: ["Arcane Recovery", "Spellbook", "School tradition"],
    levels: {
      1: ["Spellcasting", "Arcane Recovery", "Spellbook"],
      2: ["Arcane Tradition"],
      3: ["2nd-level slots", "Tradition feature"],
      4: ["Ability Score Improvement"],
      5: ["3rd-level slots"],
      6: ["Arcane Ward (resistance to chosen school's element)", "Arcane Tradition feature"],
      8: ["Ability Score Improvement"],
      7: ["Max spell Tier 4"],
      9: ["Dual Cast (2 Tier 1–2 spells per round)", "Max spell Tier 5"],
      10: ["Hero Path selection (Spellbinder / Elementalist / Necromancer)", "Chronomancer / Echomancer eligible"],
      11: ["Max spell Tier 6"],
      13: ["Overchannel — cast 1 tier higher once/day", "Max spell Tier 7"],
      15: ["Arcane Feedback — regain slot when countering", "Max spell Tier 8"],
      17: ["Tethered Cast — bonus action spell link 1/round", "Max spell Tier 9"],
      20: ["Grand Reservoir (1/day any school, any tier)", "Grand Tier"],
    },
  },
  /** draftCap: see class-ceiling-caps.js — Momentum cap/overflow, leaps/round, refund ceiling */
  Dragoon: {
    armor: ["Light armor", "Medium armor"],
    weapons: ["Simple weapons", "Polearms (spears, glaives, tridents)"],
    tools: ["Leatherworker's tools"],
    skills: ["Athletics", "Acrobatics", "Perception", "Survival — choose 2"],
    combat: ["Momentum Gauge (max 5, later 6)", "Dragon Leap", "Polearm mastery", "Draft cap: 1 leap/round · overflow +2d6 max/turn"],
    levels: {
      1: ["Skybound Assault", "Dragon Leap", "Momentum Engine"],
      2: ["Wyvern's Guard", "Draconic Roar"],
      3: ["Dragon Lancer arch class", "Crater Strike"],
      4: ["Ability Score Improvement"],
      5: ["Momentum Overflow cap increase"],
      6: ["Lance Tempo", "Giant Killer eligible"],
      8: ["Ability Score Improvement"],
      10: ["Hero Path selection (Dragon Guardian / Drake Rider / Dragon Tyrant)", "Wyrmslayer eligible"],
    },
  },
  Monk: {
    armor: ["None (Unarmored Flow)"],
    weapons: ["Simple weapons", "Shortswords", "Monk weapons (kama, nunchaku, staff)"],
    tools: ["One artisan's tool of your choice"],
    skills: ["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth — choose 2"],
    combat: ["Ki Chain (0–5)", "Stance system (Tiger / Tortoise / Crane)", "Unarmored Flow"],
    levels: {
      1: ["Monk Stances", "Flurry of Blows"],
      2: ["Deflect Missile", "Step of the Wind"],
      3: ["Master arch class", "Combo Step"],
      4: ["Ability Score Improvement"],
      5: ["Stunning Strike improvement"],
      6: ["Ki Reversal", "Blademaster eligible"],
      8: ["Ability Score Improvement"],
      10: ["Hero Path selection (Enlightened Master / Iron Fist Master / Way of Shadow)"],
    },
  },
};

for (const [name, paths] of Object.entries(classPaths)) {
  if (classDetails[name]) {
    Object.assign(classDetails[name], paths);
  }
}

for (const [name, draftLevels] of Object.entries(classDraftLevels)) {
  const detail = classDetails[name];
  if (!detail) continue;
  detail.levels = detail.levels || {};
  for (const [lvl, features] of Object.entries(draftLevels)) {
    const level = Number(lvl);
    if (!detail.levels[level]) {
      detail.levels[level] = features;
    }
  }
}

/** Sorted level keys that have feature entries for a class. */
export function sortedClassLevels(className) {
  const levels = classDetails[className]?.levels;
  if (!levels) return [];
  return Object.keys(levels)
    .map(Number)
    .sort((a, b) => a - b);
}

/** Arch / hero path blocks merged from class-paths.js */
export function classPathBlocks(className) {
  const detail = classDetails[className];
  if (!detail) return { archPaths: [], heroPaths: [] };
  return {
    archPaths: detail.archPaths ?? [],
    heroPaths: detail.heroPaths ?? [],
  };
}

export default classDetails;
