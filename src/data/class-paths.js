/** Arch class (L3–9) and hero path (L10+) skill lists — canon from rulebook_output.txt */

/** @typedef {{ name: string; levels: string; passives: string[]; actives: string[]; capstone?: string }} ArchPath */
/** @typedef {{ name: string; alignment: string; tagline?: string; passives: string[]; actives: string[]; finale?: string }} HeroPath */

/** @type {Record<string, { archPaths?: ArchPath[]; heroPaths?: HeroPath[] }>} */
export const classPaths = {
  Bard: {
    archPaths: [
      {
        name: "Virtuoso",
        levels: "3–9",
        passives: [
          "Fluid Tempo: Crescendo stacks no longer drop when hit.",
          "Verses Unbound: Verses can now crit, dealing x1.5 damage.",
          "Chorus Shield: Using a Chant grants a minor damage shield to self and nearest ally.",
          "Signature Sound: Choose a single element (Fire/Ice/Lightning). Your Verses deal +10% of that type.",
          "Perfect Pitch (Capstone): At 5 Crescendo, Verses also apply a debuff: -10% enemy resistances for 2 turns.",
        ],
        actives: [
          "Virtuoso's Verse: Enhanced musical phrase with moderate damage and Signature Sound debuff chance.",
          "Resonant Chant: Sustained melody with healing and defensive bonus to allies in range.",
          "Cascading Echo: Multiple echoes of your previous ability at diminishing potency.",
          "Tempo Control: Increase allies' action speed while decreasing enemies' speed.",
          "Harmonic Convergence: Consume all Crescendo for area damage and ally support.",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Harmony",
        alignment: "Good",
        tagline: "Supportive songsmith focused on healing, cleansing, and morale.",
        passives: [
          "Song of Serenity: Nearby allies regenerate minor HP over 2 turns after a Chant.",
          "Cleansing Verse: Crescendo 5 grants group-wide status cleanse.",
          "Echo of Light: Echoes apply +10% healing received.",
          "Divine Chorus: Party gains +1 action every 3 turns while Crescendo is active.",
          "Finale: Crescendo of Hope: On death, performs one last healing Chant automatically. (1/day)",
        ],
        actives: [
          "Healing Harmony",
          "Protective Verse",
          "Chorus of Renewal",
          "Inspiring Performance",
          "Symphony of Serenity",
        ],
      },
      {
        name: "Virtuoso",
        alignment: "Neutral",
        tagline: "Absolute mastery of tempo, combos, and battlefield manipulation.",
        passives: [
          "Echo Reverb: Echo effects trigger a second time for 50% potency.",
          "Chant Cascade: Using a Chant resets cooldown on your last Verse.",
          "Encore: 20% chance a Bard skill refunds its cooldown.",
          "Tempo Theft: Gain +5% action speed for each enemy affected by your Chants.",
          "Finale: Grand Performance: Spend 5 Crescendo to grant an extra action to all allies in range. (1/day)",
        ],
        actives: [
          "Masterful Verse",
          "Tempo Manipulation",
          "Virtuoso's Medley",
          "Harmonic Resonance",
          "Symphony of Mastery",
        ],
      },
      {
        name: "Discord",
        alignment: "Evil",
        tagline: "Twisted songweaver who manipulates madness, fear, and ruin.",
        passives: [
          "Dissonant Pulse: Chants deal minor psychic damage each round.",
          "Cacophony: Verses apply a stacking -5% Accuracy debuff.",
          "Maddening Echo: Echoes may confuse enemies for 1 turn (25% chance).",
          "Twisted Chorus: Crescendo 5 causes enemies to suffer -10% to all saves for 2 turns.",
          "Finale: Dirge of Madness: Once per long rest, enemies in a wide area are stunned and take psychic damage based on Crescendo stacks.",
        ],
        actives: [
          "Verse of Agony",
          "Chant of Fear",
          "Discordant Echo",
          "Mind-Rending Performance",
          "Symphony of Madness",
        ],
      },
    ],
  },
  Cleric: {
    archPaths: [
      {
        name: "Bishop",
        levels: "3–9",
        passives: [
          "Aura of Faith: Allies in range gain +5% healing received and +1 to saves.",
          "Sermon of Purpose: Chants now generate 1 Conviction every 2 turns.",
          "Liturgical Flow: Chaining 2 Rites reduces cooldown of your next Invocation by 1 turn.",
          "Anointed Guardian: First time an ally drops below 20% HP per combat, grant 30% damage reduction shield for 2 rounds.",
          "Sanctified Reprisal: Whenever you heal, next Smite deals 20% more damage and stuns Undead.",
          "Miraculous Channel: Sacrificing 3 Conviction causes your next Rite to affect the full party.",
          "Capstone: Bishop's Mandate: Activating a Sacrament automatically casts a free Invocation without cost or cooldown.",
        ],
        actives: [
          "Divine Invocation",
          "Sacrament",
          "Banish Unholy",
          "Blessing of Protection",
          "Commune",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Saint",
        alignment: "Good",
        tagline: "Master of mass healing and divine immunity.",
        passives: [
          "Aura of Grace: Allies in range resist critical hits and gain minor HP regen.",
          "Divine Rebirth: On revive, ally returns with 50% HP and a temporary resistance shield.",
          "Merciful Sacrament: Sacraments cost no Conviction if used on an ally under 25% HP.",
          "Unyielding Light: Once per day, prevents party wipe and restores 30% HP.",
          "Final Miracle: Celestial Resurgence: Revive all allies who died within the last 3 turns.",
        ],
        actives: [
          "Mass Healing Light",
          "Divine Intervention",
          "Sanctify Being",
          "Radiant Burst",
          "Resurrection",
        ],
      },
      {
        name: "Priest",
        alignment: "Neutral",
        tagline: "Pragmatic defender of faith and balance.",
        passives: [
          "Scriptural Echo: Casting a Rite repeats the Invocation used previously for 50% effect.",
          "Words of Equilibrium: Heal and Damage dealt scale off the higher of INT or WIS.",
          "Balanced Scales: Enemies take divine damage if they attack healed targets.",
          "Doctrine Shield: Gain 1 Conviction anytime a condition is removed.",
          "Final Miracle: Word of Binding: Enemies in a large AoE are silenced, snared, and take +25% divine damage for 3 turns.",
        ],
        actives: [
          "Balance Restoration",
          "Divine Judgment",
          "Ritual of Cleansing",
          "Word of Power",
          "Cosmic Equilibrium",
        ],
      },
      {
        name: "Cultist",
        alignment: "Evil",
        tagline: "Twisted zealot using death, sacrifice, and dark rites.",
        passives: [
          "Sanguine Rite: Rites damage enemies and heal allies for a portion of the same amount.",
          "Blasphemous Tongue: Sacraments inflict Doomed, reducing healing received and buff duration.",
          "Dark Conviction: Killing an enemy grants 1 Conviction instantly.",
          "Zealot's Touch: Healing over time effects become life drain if cast on enemies.",
          "Final Miracle: Rite of the Crimson Choir: Summon 4 fanatics for 3 turns. Each heals you for 10% of their damage dealt and explodes in death.",
        ],
        actives: [
          "Blood Sacrifice",
          "Dark Sacrament",
          "Corrupt Divinity",
          "Zealot's Fervor",
          "Ritual of Undeath",
        ],
      },
    ],
  },
  Druid: {
    archPaths: [
      {
        name: "Circle of the Land",
        levels: "2–9",
        passives: [
          "Bonus Cantrip at L2",
          "Natural Recovery: regain RP on short rest (half level, rounded up)",
          "Circle Spells by terrain (Arctic, Coast, Desert, Forest, Grassland, Mountain, Swamp, Murk)",
          "Land's Stride (L6): ignore difficult terrain and plant hazards",
          "Nature's Ward (L10): immune charm/fear from elementals/fey; poison and disease immunity",
          "Nature's Sanctuary (L14): beasts/plants hesitate to attack you",
        ],
        actives: [
          "Circle spell preparation (always prepared, no slot count)",
          "Terrain-linked spell access at L3/5/7/9",
        ],
      },
      {
        name: "Circle of the Moon",
        levels: "2–9",
        passives: [
          "Combat Shapeshifting: bonus action Wild Shape; spend RP to heal in form",
          "Circle Forms: higher CR beasts by druid level",
          "Primal Strike (L6): beast attacks count as magical",
          "Elemental Shapeshifting (L14): air/earth/fire/water elemental (2/rest)",
        ],
        actives: [
          "Bonus-action shapeshift",
          "RP-fueled healing while transformed",
        ],
      },
      {
        name: "Circle of the Storm",
        levels: "2–9",
        passives: [
          "Storm Magic (L2): subtle weather control; know thunderwave & fog cloud",
          "Thunderous Strike (L2): push Large or smaller on lightning/thunder damage",
          "Storm's Embrace (L6): resist lightning/thunder; add Wis to spell damage",
          "Eye of the Storm (L14): calm sphere in storms; allies auto-save on your storm spells",
        ],
        actives: [
          "Weather nudge (1 hour after maintaining)",
          "Thunderwave / fog cloud (always prepared)",
        ],
      },
      {
        name: "Circle of Thorns",
        levels: "2–9",
        passives: [
          "Toxic Affinity (L2): poison resistance; advantage vs poisoned; poison spray cantrip",
          "Blighted Touch (L2): touch attack — poison damage + poisoned (Wis mod uses/long rest)",
          "Withering Aura (L6): 10 ft decay aura — poison damage to chosen creatures",
          "Master of Decay (L14): poison immunity; chosen foes auto-fail poison spell saves",
        ],
        actives: [
          "Blighted Touch",
          "Withering Aura (bonus action, 1 minute)",
        ],
      },
      {
        name: "Circle of Winterfang",
        levels: "2–9",
        passives: [
          "Frost Magic (L2): ray of frost + ice knife (always known)",
          "Cold Resistance (L2): resist cold; adapted to arctic climates",
          "Winter's Embrace (L6): 10 ft cold aura — damage + speed reduction",
          "Master of Winter (L14): cold immunity; control weather (winter conditions only, 1/long rest)",
        ],
        actives: [
          "Winter's Embrace (bonus action, 1 minute)",
          "Ice knife / frost cantrips",
        ],
      },
      {
        name: "Circle of the Rotshaper",
        levels: "2–9",
        passives: [
          "Vermin Affinity (L2): speak with tiny beasts; vermin indifferent by default",
          "Swarm Summoning (L2): summon insect/rat/spider swarm (1/short rest)",
          "Plague Bearer (L6): melee hit inflicts poisoned + ongoing poison damage",
          "Master of Vermin (L14): swarm shapeshift form; summon spells may create swarms",
        ],
        actives: [
          "Swarm Summoning",
          "Plague Bearer (1/short rest)",
        ],
      },
      {
        name: "Circle of the Ashen Grove",
        levels: "2–9",
        passives: [
          "Fire Affinity (L2): fire resistance; produce flame cantrip",
          "Blazing Rebirth (L2): reaction — temp HP when ally takes fire damage (Wis mod uses/long rest)",
          "Flame Stride (L6): move through fire; leave burning trail (1d6 fire)",
          "Master of Ash (L14): fire immunity; fire spell auto-fail option; plant growth restores fire-scarred land",
        ],
        actives: [
          "Blazing Rebirth (reaction)",
          "Flame Stride trail",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Hero Druid Forms",
        tagline: "Circle-specific beast forms at L10; Arch forms at L11",
        passives: [
          "Land / Thorns: Blight Elk, Tanglemaw",
          "Moon: Beastlord, Mooncursed",
          "Storm: Tempest Raptor, Thunderhorn Stag",
          "Winterfang: Snow Leopard, Frost Wyrmling",
          "Rotshaper: Carrion Rat King, Insect Broodmother",
          "Ashen Grove: Charbear, Blazewood Stag",
        ],
        actives: [
          "Beastmaster / Verdant Animist / Mooncursed prestige eligible at L10",
        ],
      },
    ],
  },
  Oracle: {
    archPaths: [
      {
        name: "Mystery & Revelations (L1–9)",
        levels: "1–9",
        passives: [
          "L1: Choose Mystery + Curse; Revelation Charges (3, max 7) instead of spell slots",
          "L3: Tier I Revelation (choose 1, 1 charge) + Curse Boon I",
          "L5: Curse Boon II",
          "L6: Tier II Revelation (choose 1, 2 charges)",
          "L9: Tier III Revelation (Mystery capstone, 3 charges)",
          "Ten Mysteries: Ancestor, Battle, Bones, Cataclysm, Dream, Flame, Life, Shadow, Stars, Time — see oracle-mysteries.js",
        ],
        actives: [
          "Channel Revelation",
          "Prophetic Insight",
          "Curse Manifestation",
          "Divine Sense",
          "Oracular Trance",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Revelation Mastery (L10+)",
        tagline: "Curse Boons III–V, Mystic Insight, Final Revelation",
        passives: [
          "L10: Curse Boon III",
          "L12: Mystic Insight — minor Revelation or passive",
          "L15: Revelation Mastery + Curse Boon IV",
          "L18: Prophetic Surge (1/day free or extended Revelation)",
          "L20: Final Revelation + Curse Boon V",
        ],
        actives: [
          "Mystery-specific Final Revelation at L20 — see oracle-mysteries.js (Ancestor rulebook canon; Battle–Time Aethel draft)",
        ],
      },
    ],
  },
  Paladin: {
    archPaths: [
      {
        name: "Sacred Oath (L3)",
        levels: "3–9",
        passives: [
          "Swear Oath at L3: Smite Type, Aura, Revelation spells, Conduct Clause",
          "L3 Aura: 10 ft radius, base effect while conscious",
          "L6 Aura: 15 ft + secondary benefit (DR, saves)",
          "L7 Aura: reactive Smite or spell trigger",
          "L10 Aura: 20 ft; persists 1 round if incapacitated",
        ],
        actives: [
          "Divine Smite (Oath-flavored)",
          "Lay on Hands pool (5 × paladin level)",
          "Revelation spell list (5–6 Oath spells)",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Oath Mastery (L10+)",
        tagline: "Signature Power, resistance, cleansing wave, final gift",
        passives: [
          "L11: Signature Power (Oath-specific, 1/rest)",
          "L13: Divine Resistance — fire, necrotic, or psychic",
          "L15: Aura 30 ft — debuff enemies or buff allies",
          "L17: Lay on Hands Full Cleansing Wave + Aura Surge (1/rest)",
          "L18: Divine Sense detects disguised outsiders",
          "L20: Final Oath Gift + Divine Manifestation aura",
        ],
        actives: [
          "Mercy: Miracle Veil · Vengeance: Judgment Brand · Dominion: Heaven's Decree",
          "Flame: Holy Inferno · Ancients: Thorn Crown · Silence: Vow Unbroken",
          "Chain: Warden's Lock · Grief: Final Vigil · Chains Broken: Righteous Quake",
          "Martyr King: Crown of Embers",
        ],
      },
    ],
  },
  "Crimson Agent": {
    archPaths: [
      {
        name: "Hemomancer",
        levels: "3–9",
        passives: [
          "Blood Echo: Bleeds now stack twice and deal +10% more damage.",
          "Bio-Alchemical Flow: Veinweaves do not break stealth.",
          "Spill Control: Max Blood Gauge increased to 6.",
          "Rupture Trigger: Detonating a Blood Mark causes AoE Bleed in a small radius.",
          "Crimson Flow: Using Blood Gauge grants +10% movement and attack speed for 2 turns.",
          "Crimson Harmony: Maintain 2 Veinweaves simultaneously.",
          "Capstone – Bloodbound Edge: Once per rest, convert all Bleeds on enemies to instant True Damage.",
        ],
        actives: [
          "Veinweave: Bloodshield",
          "Rupture",
          "Bloodtrail",
          "Veinweave: Sensory Theft",
          "Hemostasis",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Bloodweaver",
        alignment: "Good",
        tagline: "Blood-magic defender who uses hemomancy to heal and shield others.",
        passives: [
          "Bloodbond: Link with an ally; share 25% incoming damage and transfer 10% healing to them.",
          "Hemostasis: Bleeds applied to allies now heal them instead.",
          "Protective Flow: Allies affected by your Veinweaves gain 10% DR and +1 to all saves.",
          "Veinlock Tether: Form a damage-sharing link with an ally for 3 turns.",
          "Final Cut – Crimson Pact: Detonate all enemy Bleeds to heal nearby allies and grant them barriers. (1/day)",
        ],
        actives: [
          "Transfusion",
          "Veinweave: Vitality Link",
          "Blood Ward",
          "Purify Blood",
          "Lifewell",
        ],
      },
      {
        name: "Shadow Operative",
        alignment: "Neutral",
        tagline: "Master of sabotage, stealth dominance, and disruption.",
        passives: [
          "Ghost Vein: Attacks from stealth ignore 25% of target resistances.",
          "Blackout Agent: Dodging an attack blinds the attacker for 1 turn.",
          "Ghostflow Reflexes: While Veinweave is active: +5% dodge, cooldowns -1, +10% crit resistance.",
          "Veinjammer: Bleeds reduce enemy casting and action speed by 10%.",
          "Final Cut – Total Silence: AoE disables all enemy passives and silences for 2 turns.",
        ],
        actives: [
          "Phantom Strike",
          "Veinweave: Shadow Meld",
          "Disrupt Flow",
          "Blood Cipher",
          "Blackout",
        ],
      },
      {
        name: "Thirstborn",
        alignment: "Evil",
        tagline: "Blood-crazed executioner who turns suffering into strength.",
        passives: [
          "Blood Frenzy: +5% damage per enemy actively bleeding (max +25%).",
          "Hemorrhagic Plague: Bleeds automatically spread to nearby enemies every 3 turns.",
          "Pain-to-Power Conduction: Veinweaves explode when struck, dealing AoE Bleed and minor Fear.",
          "Carrion Conductor: Corpses leave behind blood pools that explode for AoE damage.",
          "Final Cut – Veinburst Requiem: Detonates all Bleeds and Blood Gauge effects in range. Enemies under 25% HP are instantly executed. (1/day)",
        ],
        actives: [
          "Exsanguinate",
          "Veinweave: Blood Frenzy",
          "Blood Boil",
          "Crimson Harvest",
          "Bloodstorm",
        ],
      },
    ],
  },
  Dragoon: {
    archPaths: [
      {
        name: "Dragon Lancer",
        levels: "3–9",
        passives: [
          "Crater Strike: Leap attack that applies knockdown in a small AoE.",
          "Momentum Overflow: Exceed Momentum cap (Max 7), bonus damage scales with overflow.",
          "Piercing Howl: Next polearm strike ignores 50% armor.",
          "Lance Tempo: If you moved this turn, gain +10% evasion and +10% crit damage.",
          "Wyvern's Flow: Successful leaps refund 1 Momentum and reduce next cooldown by 1.",
          "Apex Assault: Ultimate leap finisher that consumes all Momentum.",
          "Capstone – Lancer's Apex: Leap attacks now cost no action if performed at max Momentum (1/encounter).",
        ],
        actives: [
          "Dragonflight",
          "Spear Cyclone",
          "Momentum Burst",
          "Aerial Recovery",
          "Dragon's Eye",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Dragon Guardian",
        alignment: "Good",
        tagline: "Protector who uses leaps to intercept danger and shield allies.",
        passives: [
          "Aegis Leap: Leap to an ally and intercept the next attack made against them.",
          "Wyrmhide: Gain +10% DR and immunity to Bleed/Burn/Poison while above 50% HP.",
          "Momentum Shield: Spending Momentum grants temporary HP.",
          "Spiral Defense: Automatically counter melee attacks with a polearm when at max Momentum.",
          "Final Flight – Bastion Descent: Slam down between allies, cleansing effects and shielding the group.",
        ],
        actives: [
          "Guardian's Intercept",
          "Draconic Ward",
          "Wyrmscale Defense",
          "Momentum Barrier",
          "Dragon's Sanctuary",
        ],
      },
      {
        name: "Drake Rider",
        alignment: "Neutral",
        tagline: "Balanced rider of power and discipline with elemental tactics.",
        passives: [
          "Drake Mark: Each leap attack marks enemies. Marked enemies take +10% damage from you.",
          "Elemental Spearcraft: Infuse polearms with Fire, Ice, or Lightning for 3 turns (switchable).",
          "Air Mastery: Gain +20% jump range and 10% reduced cooldown on leap skills.",
          "Momentum Tempo: After spending 3+ Momentum in a round, gain an extra action next turn.",
          "Final Flight – Drakestorm Dive: Choose an element and leap into a group, triggering a large AoE blast.",
        ],
        actives: [
          "Elemental Lance",
          "Drake's Agility",
          "Aerial Combo",
          "Elemental Adaptation",
          "Drakestorm",
        ],
      },
      {
        name: "Dragon Tyrant",
        alignment: "Evil",
        tagline: "Draconic wrath, devastating bursts, and terrain-breaking leaps.",
        passives: [
          "Tyrant's Crash: Leap attack applies Fear and Sunder Armor in an AoE.",
          "Momentum Feeder: Killing or critting grants +2 Momentum.",
          "Wyrmblood Surge: Each Momentum spent grants +5% damage for the next 2 turns.",
          "Skypiercer Stance: Gain passive +15% crit and ignore height restrictions on leaps.",
          "Final Flight – Sovereign Descent: Break the ground in a large radius, stunning enemies and applying Bleed and Burn. (1/rest)",
        ],
        actives: [
          "Tyrant's Impale",
          "Draconic Dominance",
          "Momentum Rampage",
          "Terrain Shatter",
          "Wyrmking's Wrath",
        ],
      },
    ],
  },
  Mage: {
    archPaths: [
      {
        name: "Arcanist",
        levels: "3–9",
        passives: [
          "Arcane Stability: Reduce spell fizzle chance by 25%.",
          "Overload Crits: Critical strikes deal +50% splash damage to nearby enemies.",
          "Arcane Bypass: Once per rest, ignore all enemy resistances for one spell.",
          "Metaspell Access: Choose one Universal Metamagic effect to apply to a spell once per day.",
          "Elemental Mastery: Increase the effectiveness of your chosen element's secondary effects.",
          "Spell Efficiency: Reduce the mana cost of spells cast in sequence with the same element.",
        ],
        actives: [
          "Elemental Surge",
          "Arcane Barrage",
          "Conjure Elemental Familiar",
          "Displacement",
          "Counterspell",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Archmage",
        alignment: "Good",
        tagline: "True mastery means knowing when not to destroy.",
        passives: [
          "Ward of Purity: Create an AoE shield that reflects 25% of incoming spells.",
          "Celestial Comet: Cast a Radiant/Arcane AoE that blinds enemies.",
          "Empowered Link: Share buffs with allies in a 5-tile radius.",
          "Harmonized Core: Spells heal allies for 10% of base damage as temporary HP.",
        ],
        actives: [
          "Arcane Sanctuary",
          "Purifying Beam",
          "Spell Sharing",
          "Mana Transfusion",
          "Arcane Convergence",
        ],
      },
      {
        name: "Elementalist",
        alignment: "Neutral",
        tagline: "Master not one element, but the storm that binds them all.",
        passives: [
          "Elemental Pivot: Switch focus element mid-combat as a bonus action.",
          "Voltaic Pulse: Create an AoE jump-stun effect.",
          "Elemental Overload: Deal dual-element damage in a 3x3 blast.",
          "Elemental Supremacy: Deal +10% damage against elemental vulnerabilities; reset chain cooldown on kill.",
        ],
        actives: [
          "Elemental Fusion",
          "Cascade Storm",
          "Elemental Absorption",
          "Primal Channeling",
          "Elemental Mastery",
        ],
      },
      {
        name: "Lich",
        alignment: "Evil",
        tagline: "Multi-phase phylactery ritual at Level 10.",
        passives: [
          "Undying Spellform: When reduced to 0 HP, continue casting for 1 full round before death.",
          "Soul Reservoir: All DoT damage you deal feeds mana recovery.",
          "Necromantic Mastery: Gain access to enhanced necromancy spells and abilities.",
          "Undead Immunities: Immune to poison, disease, fear, sleep, and mind control.",
        ],
        actives: [
          "Lingering Malice",
          "Mana to Flesh",
          "Flesh to Ash",
          "Corpse Gateway",
          "Soulbound Ritual",
        ],
      },
    ],
  },
  Mirrorsage: {
    archPaths: [
      {
        name: "Reflectionist",
        levels: "3–9",
        passives: [
          "Advanced Mirrorcall: Mirror Beast can shift once per fight into a new form based on a second Echo.",
          "Echo Slot Expansion II: Max Echo Slots: 5",
          "Dual Echo Cast: Spend 2 Echoes in one turn; must be from different creatures.",
          "Mimicry Focus: Gain +1 Focus Point per battle. Can spend Focus to empower Echoes.",
          "Mirror Shell: Once per long rest, reflect the first ability cast at you.",
          "Capstone – Perfect Reflection: Reflect any observed ability back at the caster for full effect (1/day).",
        ],
        actives: [
          "Echo Fusion",
          "Mirror Shift",
          "Focus Channel",
          "Reflective Analysis",
          "Mirror Dimension",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Light Weaver",
        alignment: "Good",
        passives: [
          "Blessed Copy: Echoed heals or buffs also affect a second ally.",
          "Luminant Bond: Charmed/Beast emits aura that reveals invisible and grants +5% saves.",
          "Sacred Echo Slot: +1 additional slot for healing/support abilities.",
          "Final – Radiant Archive: Cast 3 stored divine Echoes at once (once/day).",
        ],
        actives: [
          "Divine Reflection",
          "Radiant Mirror Beast",
          "Blessing Echo",
          "Light Binding",
          "Purifying Reflection",
        ],
      },
      {
        name: "Mirror Mage",
        alignment: "Neutral",
        passives: [
          "Mirror Double: Create a copy of yourself for 1 turn. It casts your last Echo at 50% power.",
          "Fused Echo: Combine two Echoes to create a custom hybrid. Once per long rest.",
          "Floating Memory Slot: Temporarily store a 6th Echo. Auto-erases after combat.",
          "Final – Reflected Repertoire: Reset all Echo slots. Next 3 Echoes cast without consuming slots.",
        ],
        actives: [
          "Echo Manipulation",
          "Mirror Image",
          "Prismatic Reflection",
          "Echo Preservation",
          "Reality Fracture",
        ],
      },
      {
        name: "Shattered One",
        alignment: "Evil",
        passives: [
          "Corrupted Mirrorcall: Mirror Beast gains a random mutation (e.g., Burn Aura, Bleed Burst).",
          "Shatterbind: Echoes from undead/demons/aberrations gain necrotic or psychic damage tags.",
          "Fractured Echo: 25% chance each Echo triggers again randomly the next round.",
          "Final – Fractured Dominion: For 2 turns, every Echo cast also generates a Glitched Clone Echo.",
        ],
        actives: [
          "Corrupt Echo",
          "Shattered Mirror Beast",
          "Echo Leech",
          "Fractured Reality",
          "Mind Shatter",
        ],
      },
    ],
  },
  Monk: {
    archPaths: [
      {
        name: "Master",
        levels: "3–9",
        passives: [
          "Combo Step: Use three different unarmed attacks in one round to stun the target.",
          "Ki Reversal: At 4+ Ki Chain, auto-counter the next melee hit.",
          "Perfect Balance: Standing still: +15% crit. Moving: +15% dodge.",
          "Breath of Focus: Skip an attack to gain +1 Ki Chain.",
          "Rhythmic Flow: Every 3rd round, next strike auto-crits at max Ki.",
          "Martial Apex (Capstone): At 5 Ki, your next ability costs no action and deals +100% damage (1/encounter).",
          "Stone Shell Discipline: +15% DR and Ki Chain protection at 3+ Ki. Immune to forced movement.",
          "Redirecting Palm: Spend 1 Ki to redirect 50% of incoming melee damage to a nearby enemy.",
          "Iron Shell Pulse: Spend 3 Ki: grant nearby allies 10% DR and retaliation aura.",
          "Echoing Guard: Blocking/dodging applies Stagger (-10% damage, -1 move).",
          "Final Form – Bastion of Breath: Become immune for 1 round. Enemies who strike are stunned.",
        ],
        actives: [
          "Whirlwind Stance",
          "Focused Ki Burst",
          "Diamond Soul",
          "Pressure Point Strike",
          "Meditative Healing",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Enlightened Master",
        alignment: "Good",
        passives: [
          "Tranquil Lotus Step: Move to ally, absorb their debuff, and grant +15% healing received (2 Ki).",
          "Serenity Breaker Palm: Strike enemy; cleanse allies in 2 tiles (3 Ki).",
          "Balance Beyond Flesh: Allies in Crane stance range heal 5% each time they spend a resource.",
          "Final – Breath of the Thousand Petals: AoE revive and death immunity (1 round).",
        ],
        actives: [
          "Healing Touch",
          "Purifying Palm",
          "Circle of Harmony",
          "Shared Breath",
          "Transcendent Meditation",
        ],
      },
      {
        name: "Iron Fist Master",
        alignment: "Neutral",
        passives: [
          "Ribcrusher Strike: Heavy strike, reduces enemy max HP by 10% (2 Ki).",
          "Centerline Blitz: Dash in a line, striking all targets. Final one is stunned at max Ki (3 Ki).",
          "Steel Reflection Form: Reflect 15% melee damage for 3 turns.",
          "Final – Limit Break Spiral: 2 bonus actions; all strikes crit this turn (1/day).",
        ],
        actives: [
          "Iron Palm",
          "Flowing Combo",
          "Focused Breathing",
          "Bone-Breaking Strike",
          "One Hundred Fists",
        ],
      },
      {
        name: "Way of Shadow",
        alignment: "Evil",
        passives: [
          "Veinlock Nerve Jab: Strike blocks healing/resource gain (2 turns). Silences if hidden (2 Ki).",
          "Twilight Mirage: Summon a 1-turn clone to mirror strikes and intercept attacks (3 Ki).",
          "Nerve Fade Technique: Stacking Shadow Rot debuff (-saves, psychic DoT) (1 Ki).",
          "Final – Deathless Silence: Untargetable 1 turn → teleport to 3 enemies and apply Void Palm.",
        ],
        actives: [
          "Shadow Step",
          "Nerve Strike",
          "Poison Hand",
          "Mind Cloud",
          "Death Touch",
        ],
      },
    ],
  },
  Ranger: {
    archPaths: [
      {
        name: "Pathfinder",
        levels: "3–9",
        passives: [
          "Ignore Difficult Terrain: Move normally through any type of difficult terrain.",
          "Enhanced Stealth and Perception: Gain +2 to Stealth and Perception checks.",
          "Tactical Draw: Gain +1 AC after switching from bow to blade or vice versa.",
          "Vigilant Heart: Become immune to surprise and scrying attempts.",
          "Dual Style: Gain the ability to swap weapons as a free action (level 5).",
          "Elemental Imbue: Infuse weapons with fire, cold, or poison (level 6).",
        ],
        actives: [
          "Pathfinder's Mark",
          "Natural Camouflage",
          "Terrain Analysis",
          "Swift Traverse",
          "Predator's Mark (level 9)",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Warder",
        alignment: "Good",
        tagline: "The land provides for those who protect it.",
        passives: [
          "Living Pulse: Regenerate 2 HP per round while in natural terrain.",
          "Beast Empathy: Communicate basic concepts with natural beasts.",
          "Warden's Vigilance: Detect threats to natural areas within a large radius.",
          "Healing Touch: Your healing spells and items are 25% more effective on allies.",
        ],
        actives: [
          "Rootcall Quake",
          "Healing Briar",
          "Warden's Step",
          "Nature's Blessing",
          "Beast Companion",
        ],
      },
      {
        name: "Stalker",
        alignment: "Neutral",
        passives: [
          "Hunter's Reflex: Gain +10% Dodge chance after making a ranged attack.",
          "Shadow Step: Leave no tracks and make no sound when moving at normal speed.",
          "Keen Hunter: Tracked targets cannot hide from you within your line of sight.",
          "Efficient Killer: Reduce the Hit Chain requirement for Druidic Arrow to 2 hits instead of 3.",
        ],
        actives: [
          "Camouflage Step",
          "Silent Volley",
          "Shattershot",
          "Ghost Strike",
          "Vanishing Act",
        ],
      },
      {
        name: "Outrider",
        alignment: "Evil",
        passives: [
          "Predator's Grin: Killing a tracked target grants you an extra action once per rest.",
          "Toxic Affinity: Gain immunity to poison and disease.",
          "Corruption Touch: Elemental imbues last twice as long and spread on crits.",
          "Blight Infusion: Druidic Arrows inflict Blight on hit if the terrain is corrupted.",
        ],
        actives: [
          "Venom Rain",
          "Rotting Tether",
          "Entropic March",
          "Withering Shot",
          "Plague Bearer",
        ],
      },
    ],
  },
  Shaman: {
    archPaths: [
      {
        name: "Spiritwalker",
        levels: "3–9",
        passives: [
          "Enhanced Elemental Attunement: Your chosen element grants additional benefits.",
          "Extended Totem Duration: Totems last for an additional round.",
          "Spirit Cache: Store one flask or totem effect to recast later (once per encounter).",
          "Totem Pulse: Totems create an immediate area effect when placed (level 6).",
          "Spirit Saturation: Gain one free totem cast per combat (level 9).",
        ],
        actives: [
          "Elemental Channeling",
          "Spirit Walk",
          "Ancestral Guardian",
          "Elemental Surge",
          "Spirit Binding",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Theurgist",
        alignment: "Good",
        passives: [
          "Echo Totem: Automatically cast a second, weaker totem when placing your primary totem.",
          "Elemental Harmony: Your elemental summons gain increased duration and health.",
          "Spiritual Resonance: Totems affect a larger area when placed near each other.",
          "Benevolent Spirits: Healing effects are 25% more powerful on allies below half health.",
        ],
        actives: [
          "Summon Ice Wisp",
          "Summon Airling",
          "Summon Cinderflame",
          "Summon Stonekin",
          "Elemental Chorus",
        ],
      },
      {
        name: "Soothsayer",
        alignment: "Neutral",
        passives: [
          "Divining Totem: Reveals enemy actions before they occur (one target per round).",
          "Predictive Alchemy: Flasks have a chance to not be consumed when used.",
          "Fate's Whisper: Gain advantage on one saving throw per encounter.",
          "Balanced Elements: Elemental effects last longer and have secondary effects.",
        ],
        actives: [
          "Delayed Detonation",
          "Healing Splash",
          "Omen Brand",
          "Fate Weaving",
          "Omen Loop",
        ],
      },
      {
        name: "Bloodcaller",
        alignment: "Evil",
        tagline: "Permanently transforms into a Hagraven; loses traditional spellcasting.",
        passives: [
          "Hagraven Form: Twisted avian-humanoid hybrid with natural weapons and resistances.",
          "Blood Feast: Heal when enemies near you are bleeding.",
          "Necrotic Aura: Enemies within 10 feet take minor necrotic damage each round.",
          "Spell Resistance: Gain advantage on saves against spells and magical effects.",
        ],
        actives: [
          "Blight Totem",
          "Blood Curse",
          "Talon Strike",
          "Death Shriek",
          "Bloodroot Trail",
        ],
      },
    ],
  },
  Soldier: {
    archPaths: [
      {
        name: "Commander",
        levels: "3–9",
        passives: [
          "Command Step: Once per round, shift one adjacent ally 1 tile in any direction.",
          "Formation Lock: Allies adjacent to you cannot be flanked.",
          "Iron Orders: All allies within 3 tiles gain +1 Save vs Fear and +1 AC.",
          "Palisade Deployment: Deploy a 2x1 barrier (level 5).",
          "Intercepting Shot: Reaction fire at an enemy about to hit an ally within 5 tiles (level 6).",
          "Fortify Zone: Enemies in a 3x3 area take –2 to ranged attacks against your allies (level 9).",
        ],
        actives: [
          "Tactical Assessment",
          "Coordinated Maneuver",
          "Suppression Fire",
          "Defensive Formation",
          "Hold the Line",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Champion",
        alignment: "Good",
        tagline: "No one falls while I stand.",
        passives: [
          "Protective Aura: Nearby allies ignore fear and charm effects while you stand.",
          "Selfless Guardian: Take reduced damage when intercepting attacks meant for allies.",
          "Inspiring Presence: Allies within sight gain a bonus to morale saves.",
          "Defensive Expertise: Gain additional damage reduction when using defensive abilities.",
        ],
        actives: [
          "Guardian's Rush",
          "Divine Lockdown",
          "Wall of Aegis",
          "Rallying Cry",
          "Sacrificial Defense",
        ],
      },
      {
        name: "Artillerist",
        alignment: "Neutral",
        passives: [
          "Enhanced Overwatch: Overwatch can reveal and fire on stealthed or invisible enemies.",
          "Tactical Reload: Reload your crossbow as a free action once per round.",
          "Palisade Synergy: Attacks deal additional damage to enemies adjacent to your palisades.",
          "Precision Engineering: Deployed structures have increased durability and effectiveness.",
        ],
        actives: [
          "Net Bolt",
          "Shatterburst",
          "Repel Shot",
          "Turret Deployment",
          "Bubble of Discipline",
        ],
      },
      {
        name: "Tyrant",
        alignment: "Evil",
        passives: [
          "Intimidating Presence: Enemies that can see you have disadvantage on morale checks.",
          "Cruel Efficiency: Stacking damage bonus when hitting the same target consecutively.",
          "Marked for Death: Designated enemies take –1 to saves and deal –1 damage vs allies other than you.",
          "Ruthless Tactician: Advantage on attacks against flanked or terrain-hindered enemies.",
        ],
        actives: [
          "Crushing Decree",
          "Impale Line",
          "Execution Zone",
          "Demoralizing Shot",
          "Brutal Example",
        ],
      },
    ],
  },
  Thief: {
    archPaths: [
      {
        name: "Rake",
        levels: "3–9",
        passives: [
          "Combat Opener: Gain +5 to initiative rolls.",
          "Ambush Focus: Deal +2 damage against unaware or distracted targets.",
          "Evasion: Take half damage on successful saves against area effects (level 5).",
          "Trap Sense: Gain passive trap detection and disarm bonuses (level 6).",
          "Shadow Stab: On critical hit, teleport through target and apply Bleed (level 9).",
        ],
        actives: [
          "Precision Feint",
          "Vanish",
          "Analyze Weakness",
          "Distraction Tactics (level 13)",
          "Crippling Strike (level 15)",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Arcane Trickster",
        alignment: "Good",
        passives: [
          "Mage Sense: Detect all magical effects and passives within 5 tiles.",
          "Arcane Resistance: Gain +2 to saves against magic.",
          "Illusory Stealth: Casting illusion or utility spells does not break stealth.",
          "Spell Disruptor: Poisons suppress passive magical abilities for 1 round on critical hits.",
        ],
        actives: [
          "Magebane Blade",
          "Pocket Illusion",
          "Flash Shift",
          "Arcane Theft",
          "Spell Snare",
        ],
      },
      {
        name: "Shadowblade",
        alignment: "Neutral",
        passives: [
          "Ambusher's Grace: After kill or crit on Bleed/Poison target, become untargetable until next turn.",
          "Double Poison: Apply two poisons instead of one on critical hits.",
          "Persistent Bleed: Bleeds you cause refresh on hit instead of expiring.",
          "Shadow Affinity: Advantage on Stealth checks in dim light or darkness.",
        ],
        actives: [
          "Dark Step",
          "Shadow Dive",
          "Vein Cutter",
          "Smoke Bomb",
          "Death Blossom (level 17)",
        ],
      },
      {
        name: "Blackguard",
        alignment: "Evil",
        passives: [
          "Exsanguinate: Gain 1 HP per round for each bleeding target within 3 tiles.",
          "Prolonged Suffering: Bleeds you cause last twice as long.",
          "Venom Master: On critical hits, poisons also apply -1 to all saves.",
          "Exotic Toxins: Use monster-only venoms if harvested from bestiary bosses.",
        ],
        actives: [
          "Crippling Lash",
          "Toxic Shiv",
          "Vile Tactics",
          "Terror Strike",
          "Unseen Hand (level 20)",
        ],
      },
    ],
  },
  Tinker: {
    archPaths: [
      {
        name: "Mechanist",
        levels: "3–9",
        passives: [
          "Enhanced Drone Control: Anacite Drone gains improved targeting and responsiveness.",
          "Bomb Specialization: Explosive devices deal additional damage or have enhanced effects.",
          "Pet Upgrade Slot: Modify drone with Offensive, Defensive, or Support module (level 5).",
          "Deployable Expertise: Deployed devices have increased durability and effectiveness.",
          "Remote Detonation: Detonate devices remotely for area damage or stunning (level 9).",
        ],
        actives: [
          "Deploy Sentry Turret (level 6)",
          "Deploy Net Trap (level 6)",
          "Overcharge",
          "Recalibrate",
          "Emergency Protocols",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Artificer",
        alignment: "Good",
        passives: [
          "Calibrated Precision: Allies within 3 tiles gain +1 to hit.",
          "Safe Detonation: Bombs deal no damage to allies.",
          "Protective Programming: Drone prioritizes defending vulnerable allies.",
          "Efficient Power Cells: Devices last 50% longer before needing recharging.",
        ],
        actives: [
          "Nano-Aegis Drone",
          "Repair Pulse",
          "Magnetic Wall",
          "Restoration Field",
          "Overload Suppression",
        ],
      },
      {
        name: "Techsmith",
        alignment: "Neutral",
        passives: [
          "Automated Field Kit: Carry an extra bomb and reduce deployable cooldowns by 1 round.",
          "Enhanced Targeting: Turrets gain +1 to hit.",
          "Efficient Recycling: Recover components from destroyed devices.",
          "Technical Mastery: Devices have a 10% chance to function twice when activated.",
        ],
        actives: [
          "Advanced Turret Bay",
          "Gadget Sync Protocol",
          "Snap Rebuild",
          "Reconfiguration",
          "Field Fabrication",
        ],
      },
      {
        name: "Warmachine",
        alignment: "Evil",
        passives: [
          "Malfunction Field: Enemies near your devices must roll twice on spell attacks and take the lower result.",
          "Volatile Components: Devices explode when destroyed, damaging nearby enemies.",
          "Unstable Enhancements: Bombs have a 25% chance to deal double damage but may affect allies.",
          "Scrap Salvage: Create temporary minions from destroyed devices.",
        ],
        actives: [
          "Boomcore Drone",
          "Overpressure Bombs",
          "Scrap Reaper",
          "Volatile Injection",
          "Catastrophic Overload",
        ],
      },
    ],
  },
  Warrior: {
    archPaths: [
      {
        name: "Juggernaut",
        levels: "3–9",
        passives: [
          "Mutation Efficiency: May have 2 active mutations at once (Lv 3).",
          "Brutal Fortitude: Gain +1 DR for each BT stack (max +3).",
          "Overpressure Response: Once per round, when struck by a critical hit, gain 1 free mutation activation.",
          "Crushing Advance: Once per long rest, move in a straight line up to 20 ft, knocking aside enemies.",
          "Pain Conversion: Convert 10% of damage taken into temporary Strength bonus.",
          "Adaptive Tissue: Gain resistance to the last damage type that critically hit you until next rest.",
          "Brutality Momentum: Killing a marked vulnerable target instantly readies your next Brutal Strike.",
        ],
        actives: [
          "Mutation Overload",
          "Serum Cocktail",
          "Brutality Unleashed",
          "Survival Adaptation",
          "Intimidating Transformation",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Wardborn",
        alignment: "Good",
        tagline: "Self-mutated protector armored in flesh and tenacity.",
        passives: [
          "Guardian Tissue: Absorb 30% of adjacent ally damage as a reaction.",
          "Protective Mutations: 5-foot aura grants allies +10% damage resistance.",
          "Serum Sharing: Inject allies with diluted serums at 50% benefit.",
          "Controlled Transformation: Mutations appear less monstrous and can be partially concealed.",
          "Final Form – Aegis Incarnate: Living shield for 3 rounds; redirect 50% of ally damage within 15 feet.",
        ],
        actives: [
          "Bulwark Mutation Tree",
          "Mutated Guard",
          "Guardian Pulse",
          "Warding Mutation",
          "Stabilizing Injection",
        ],
      },
      {
        name: "Ironskin",
        alignment: "Neutral",
        tagline: "Mutation-hardened warbeast built to survive what others can't.",
        passives: [
          "Environmental Adaptation: Auto-adapt to extreme environments after 1 minute.",
          "Regenerative Mutation: Heal 5% max HP each round while at least one mutation is active.",
          "Serum Recycling: 20% chance to not consume a serum when activating a mutation.",
          "Damage Memory: Increasing resistance to repeated damage types.",
          "Final Form – Adaptive Perfection: Immunity to damage types and environmental effects exposed to today (3 rounds).",
        ],
        actives: [
          "Gore Mutation Tree",
          "Stack Overflow",
          "Auto-Rupture",
          "Adaptive Mutation",
          "Cellular Reconstruction",
        ],
      },
      {
        name: "Dreadspawn",
        alignment: "Evil",
        tagline: "Cursed evolution beyond mortal flesh.",
        passives: [
          "Horrific Appearance: Enemies who see you activate a mutation must save or be frightened.",
          "Infectious Mutation: 10% chance attacks cause minor painful mutations in targets.",
          "Serum Toxicity: Serums poisonous to others; blood deals acid damage to those who wound you.",
          "Pain Empowerment: +5% damage for each 10% of health you are missing.",
          "Final Form – Abomination Ascendant: Nightmarish creature for 3 rounds with fear aura (30 ft).",
        ],
        actives: [
          "Aberrant Mutation Tree",
          "Terror Radius",
          "Apex Aberration (1/day)",
          "Horrific Mutation",
          "Toxic Secretion",
        ],
      },
    ],
  },
  Wizard: {
    archPaths: [
      {
        name: "Arcanist",
        levels: "3–9",
        passives: [
          "Floating Slot: Prepare 1 extra spell from any school each day.",
          "Sigil Rewrite: Once/day, instantly swap a spell for another of the same tier.",
          "Spell Tether: Maintain 2 self-buff spells without concentration (1/rest).",
          "Matrix Mastery: Modify spell matrices to change minor aspects of prepared spells.",
          "Arcane Tradition: Choose a school of magic to specialize in.",
          "Spell Efficiency: Reduce mana cost of frequently cast spells by 10%.",
          "Improved Concentration: Advantage on concentration checks when taking damage.",
        ],
        actives: [
          "Counterspell",
          "Arcane Lock",
          "Dispel Magic",
          "Dimensional Pocket",
          "Arcane Sight",
        ],
      },
    ],
    heroPaths: [
      {
        name: "Spellbinder",
        alignment: "Good",
        tagline: "Master of arcane lockdown and anti-magic warfare.",
        passives: [
          "Sigil Authority: +1 to counterspell rolls; +2 DC vs crowd-controlled targets.",
          "Spell Preservation: Spellbook cannot be destroyed by non-artifact means.",
          "Knowledge Shield: When you cast a protective spell, allies gain +2 to saving throws.",
          "Matrix Sharing: Grant an ally temporary access to one prepared spell.",
          "Arcane Memory: Recall and cast any spell you've ever prepared once per long rest.",
        ],
        actives: [
          "Seal Magic",
          "Runic Snare",
          "Counterpulse",
          "Spell Absorption",
          "Knowledge Transfer",
        ],
        finale: "Arcane Sanctuary: Demiplane of safety for 1 hour where harmful magic cannot function (1/week).",
      },
      {
        name: "Elementalist",
        alignment: "Neutral",
        tagline: "Embodiment of elemental devastation and chain reactions.",
        passives: [
          "Core Sync: Chosen element spells cost 1 fewer slot at Tier 1–2; change affinity once per long rest.",
          "Matrix Innovation: Combine aspects of two different spells into one casting.",
          "Spell Adaptation: Change a spell's damage type or effect type once per short rest.",
          "Efficient Casting: 20% chance to not consume a spell slot when casting.",
          "Arcane Experimentation: Advantage on checks to create new spells or magical items.",
        ],
        actives: [
          "Elemental Affinity",
          "Combo Surge",
          "Cycling Ward",
          "Spell Modification",
          "Arcane Fusion",
        ],
        finale: "Reality Edit: Temporarily change one aspect of reality in a small area (1/week).",
      },
      {
        name: "Necromancer",
        alignment: "Evil",
        tagline: "Summoner of the dead and pactbound with infernal patrons.",
        passives: [
          "Flesh Ascendant: All undead gain +2 HP per Wizard level; 2+ undead grants +1 AC and Save.",
          "Mind Matrix: Enchantment spells are harder to resist (+2 to save DC).",
          "Will Domination: Failed saves by 5+ stun for 1 round.",
          "Arcane Leech: Gain temporary hit points when a creature fails a save against your spells.",
          "Binding Sigil: Mark a creature for advantage on spell attacks against it.",
        ],
        actives: [
          "Corpse Harvest",
          "Ghoul Lash",
          "Infernal Pact (Quest-based unlock)",
          "Mental Binding",
          "Arcane Domination",
        ],
        finale: "Mind Prison: Trap a creature's mind in an illusory reality while controlling its body (1/week).",
      },
    ],
  },
};

export default classPaths;
