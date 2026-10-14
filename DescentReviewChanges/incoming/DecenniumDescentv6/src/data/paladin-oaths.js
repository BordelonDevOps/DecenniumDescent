/**
 * Paladin Sacred Oaths — canon from rulebook_output.txt + Paladin_Oaths_*.docx themes.
 * Select at L3; violation risks Oathbreaker inversion.
 *
 * draftCap: docs/mechanics/CLASS_CEILING_CAPS.md — aura stacking, 1 smite or spell/round,
 *   Lay on Hands spend cap; oath revelation riders bounded per class-ceiling-caps.js
 */

/** @typedef {object} SacredOath
 * @property {string} id
 * @property {string} name
 * @property {string} theme
 * @property {string} smiteType
 * @property {string} auraEffect
 * @property {string} signaturePower
 * @property {string[]} conductClause
 * @property {{ level: number; spell: string }[]} revelationSpells
 * @property {{ name: string; deathTouch: string; aura: string; blasphemousWord: string }} oathbreaker
 * @property {string} [finalOathGift]
 * @property {boolean} [finalOathGiftDraft]
 * @property {boolean} [draft]
 * @property {string} [source]
 */

/** @type {SacredOath[]} */
export const SACRED_OATHS = [
  {
    id: "mercy",
    name: "Oath of Mercy",
    theme: "Mercy is a shelter kept open in the worst hour: protection, healing, and the preservation of life before vengeance can make another wound.",
    smiteType: "Radiant — bonus radiant damage; heals nearby allies for a portion dealt",
    auraEffect: "Aura of Mercy — allies gain increased healing received and resistance to necrotic damage",
    signaturePower: "Miracle Veil — protective barrier; ally cannot drop below 1 HP for the duration (1/rest)",
    conductClause: [
      "Never refuse a genuine plea for healing or protection when the oath can answer it",
      "Set the saving of life before the taking of it, even when anger makes the latter easier",
      "Offer defeated foes the mercy their surrender can bear, without abandoning those still in danger",
      "Do not raise lethal force against the innocent or defenseless; strength was given to stand between them and harm",
    ],
    revelationSpells: [
      { level: 3, spell: "Blessing of the Meek — heal + AC if HP < 50%" },
      { level: 5, spell: "Ward of Shelter — allies +2 DR, resist fear" },
      { level: 9, spell: "Channel Life — transfer HP from self to ally" },
      { level: 13, spell: "Sanctify Ground — zone removes conditions each round" },
      { level: 17, spell: "Grace Reversal — revive fallen ally if you fall to 0 HP" },
    ],
    oathbreaker: {
      name: "Cruelty",
      deathTouch: "Life Drain AoE — steal life from all creatures around you",
      aura: "Healing Suppression — all healing within aura reduced by 50%",
      blasphemousWord: "Exsanguinate — drain life in large radius, heal self for damage dealt",
    },
    finalOathGift:
      "Grace Eternal — once per day, Miracle Veil extends to all allies within your aura for 1 round; any ally reduced to 0 HP in that round rises to 1 HP instead, heals 2d8, and gains resistance to necrotic until end of next turn; you may Lay on Hands once as a free action during the veil.",
    finalOathGiftDraft: true,
    draft: true,
    source: "Draft — Aethel Sacred Oath; bounded rulebook-tone pass only, with mechanics and revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
  {
    id: "vengeance",
    name: "Oath of Vengeance",
    theme: "Vengeance is judgment carried through the long road: fury disciplined into pursuit, execution held to a sworn account, and no refuge promised to the unrepentant.",
    smiteType: "Necrotic or radiant — bonus damage vs marked foes; applies Vengeance Mark",
    auraEffect: "Aura of Judgment — marked enemies within aura suffer −1 saves and cannot hide from you",
    signaturePower: "Judgment Brand — doom mark on target; bonus crit damage and pursuit (1/rest)",
    conductClause: [
      "Pursue sworn enemies until justice is served or they surrender; let no convenience excuse a broken charge",
      "Do not abandon allies to feed a private vendetta, for judgment that leaves the faithful behind is only rage",
      "Accept the surrender of those who genuinely repent, and hold them to the peace they have asked for",
    ],
    revelationSpells: [
      { level: 3, spell: "Mark of Retribution — mark one foe within 30 ft on failed Wis save; +1d8 smite damage vs marked and advantage on opportunity attacks against them until end of next turn" },
      { level: 5, spell: "Relentless Pursuit — ignore difficult terrain vs marked target" },
      { level: 9, spell: "Sentence of Doom — smite deals max dice vs marked" },
      { level: 13, spell: "No Escape — marked foes within 60 ft cannot teleport, become invisible, or use extradimensional travel; if they leave your aura, opportunity attacks against them have advantage until end of next turn" },
      { level: 17, spell: "Final Verdict — marked foe at or below half HP within 30 ft saves or drops to 0 HP; on success, your next smite deals max dice and they cannot regain HP until end of next turn" },
    ],
    oathbreaker: {
      name: "Malice",
      deathTouch: "Execute chance on wounded targets",
      aura: "Fearbrand — allies near you suffer morale penalties",
      blasphemousWord: "Fearbrand — increased damage to wounded; spread fear",
    },
    finalOathGift:
      "Verdict Absolute — once per day, your Judgment Brand cannot be resisted: marked foes suffer max-dice smites, cannot teleport or become invisible, and if reduced to 0 HP you restore your full Lay on Hands pool; unmarked foes who witness the execution must save or become frightened until end of next turn.",
    draft: true,
    source: "Draft — Aethel Sacred Oath; revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
  {
    id: "dominion",
    name: "Oath of Dominion",
    theme:
      "Authority held as a public burden: law spoken plainly, judgment bound to truth, and rulership measured by the safety it keeps",
    smiteType: "Radiant or psychic — bonus damage; compels truth on failed save; liars in aura suffer −1 saves until end of next turn",
    auraEffect: "Aura of Authority — allies +1 to Intimidation; enemies must save to lie within aura",
    signaturePower: "Heaven's Decree — command obey or suffer psychic damage (1/rest)",
    conductClause: [
      "Uphold legitimate law and order, but do not call convenience or cruelty a lawful charge",
      "Speak truth when acting as arbiter, and hear the whole matter before you command another",
      "Do not use authority for personal gain; a decree that serves only its speaker has already failed the oath",
    ],
    revelationSpells: [
      { level: 3, spell: "Compelled Truth — 10-ft zone where deception fails; oath-breakers take psychic damage on failed Charisma save" },
      { level: 5, spell: "Binding Word — restrain on failed Charisma save" },
      { level: 9, spell: "Law's Weight — 20-ft zone for 3 rounds; lawbreakers (those who lied in your aura this combat) save or half speed, −2 AC, and cannot benefit from haste or dash until zone ends" },
      { level: 13, spell: "Decree of Submission — 30-ft command; target save or charmed (obey one command) or frightened (cannot approach you) for 1 minute; oath-breakers have disadvantage" },
      { level: 17, spell: "Sovereign Mandate — allies in aura gain advantage on saves vs charm, fear, and compulsion for 1 minute; enemies who fail a Wis save when entering aura cannot lie in your presence until end of next turn" },
    ],
    oathbreaker: {
      name: "Tyranny",
      deathTouch: "Will control on touch",
      aura: "Obey — psychic damage for disobedience within aura",
      blasphemousWord: "Obey — mass command with psychic backlash",
    },
    finalOathGift:
      "Sovereign's Ascendance — once per day, Heaven's Decree affects all enemies in aura without save; allies gain advantage on Charisma saves and +2 to Intimidation for 3 rounds, and enemies who fail cannot lie or disobey a direct command until end of next turn.",
    draft: true,
    source: "Draft — Aethel Sacred Oath; bounded rulebook-tone pass only, with mechanics and revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
  {
    id: "flame",
    name: "Oath of Flame",
    theme:
      "A fire kept for cleansing rather than hunger: zeal tempered by restraint, corruption confronted, and renewal guarded after the ash",
    smiteType: "Fire and radiant — bonus damage; purges one condition from undead/fiend on hit",
    auraEffect: "Aura of Purification — allies resist disease; undead in aura take radiant damage at start of turn",
    signaturePower: "Holy Inferno — AoE smite purge; fire and radiant damage (1/rest)",
    conductClause: [
      "Purify corruption and undeath where found, but name the thing being purged before you raise the flame",
      "Do not burn the innocent in zeal; fire that cannot distinguish harm from shelter has forsaken this oath",
      "Accept that fire renews as well as destroys, and remain to protect what must grow after the burning",
    ],
    revelationSpells: [
      { level: 3, spell: "Cleansing Brand — fire damage + remove curse on crit" },
      { level: 5, spell: "Zealot's Flame — weapon ignites for 1 minute; attacks deal +1d6 fire and purge one disease from you on hit; undead in aura take 1d6 radiant at start of their turns" },
      { level: 9, spell: "Purge the Tainted — zone damages undead each round" },
      { level: 13, spell: "Sanctified Immolation — next smite or Holy Inferno ignores fire resistance and deals +1d6 radiant to undead; if target is cursed or diseased, purge one condition on hit" },
      { level: 17, spell: "Phoenix Rebirth — when ally in aura drops to 0 HP, revive to half max HP with fire shield (resist fire, 2d6 fire to melee attackers) once per combat per ally" },
    ],
    oathbreaker: {
      name: "Inferno",
      deathTouch: "Burn healed enemies",
      aura: "Scorch the Sanctified — remove buffs; block regeneration",
      blasphemousWord: "Scorch the Sanctified — AoE purge that harms allies",
    },
    finalOathGift:
      "Purifying Crown — once per day, manifest sanctified fire for 3 rounds: undead and fiends in your aura take radiant+fire damage each turn, allies gain immunity to disease and poison, and Holy Inferno immediately recharges once.",
    draft: true,
    source: "Draft — Aethel Sacred Oath; bounded rulebook-tone pass only, with mechanics and revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
  {
    id: "ancients",
    name: "Oath of the Ancients",
    theme:
      "The living memory of the old places: nature guarded as a covenant, ancient power answered with humility, and renewal left possible for those who follow",
    smiteType: "Force or radiant — bonus damage; roots target until end of next turn on crit; fey and elementals have disadvantage on saves vs your smites",
    auraEffect: "Aura of Remembrance — allies resist charm; fey/elementals hesitate to attack you",
    signaturePower: "Thorn Crown — reflect status effects back at attacker (1/rest)",
    conductClause: [
      "Protect ancient places and living memory, especially where no living voice remains to speak for them",
      "Do not destroy what cannot be restored; power does not excuse a wound made for haste",
      "Honor pacts with fey and primal spirits, and do not mistake an old promise for permission to command",
    ],
    revelationSpells: [
      { level: 3, spell: "Roots of Memory — 10-ft burst on smite hit; on failed Str save target restrained and you learn one fact about its origin (fey, elemental, or ancient place)" },
      { level: 5, spell: "Primal Ward — allies in aura gain resistance to cold, fire, lightning, or thunder (choose at cast); fey and elementals have disadvantage on saves vs. your smites while ward persists" },
      { level: 9, spell: "Echo of Ages — you and allies in aura gain advantage on saves vs charm and frightened for 1 minute; fey and elementals that fail a Wis save when entering aura hesitate and cannot attack until end of next turn" },
      { level: 13, spell: "Standing Stone — 20-ft zone of difficult terrain for enemies for 3 rounds; fey and elementals save or are slowed; allies treat zone as normal terrain" },
      { level: 17, spell: "Primordial Surge — allies in aura gain temp HP equal to 2× CHA mod from land; fey/elementals in aura save or are rooted until end of next turn" },
    ],
    oathbreaker: {
      name: "Withering Grove",
      deathTouch: "Blight terrain on touch",
      aura: "Lifeleech Bloom — remove regeneration and resistance",
      blasphemousWord: "Lifeleech Bloom — drain vitality from plants and allies",
    },
    finalOathGift:
      "Primordial Crown — once per day, Thorn Crown persists for 3 rounds without cost; roots on crit spread to adjacent foes, fey and elementals within aura cannot attack allies, and allies gain advantage on saves vs charm while the crown persists.",
    draft: true,
    source: "Draft — Aethel Sacred Oath; bounded rulebook-tone pass only, with mechanics and revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
  {
    id: "silence",
    name: "Oath of Silence",
    theme: "Humility, watchful restraint, and strength held in quiet",
    smiteType: "Psychic or radiant — bonus damage when you have not spoken since last turn",
    auraEffect: "Aura of Stillness — allies gain +1 to concentration; loud noises suppressed in aura",
    signaturePower: "Vow Unbroken — bonus smite if you stay silent this combat (1/rest)",
    conductClause: [
      "Speak when words serve the oath; let silence bear the rest",
      "Do not claim glory for the work entrusted to you",
      "Hear the whole matter before you judge it",
    ],
    revelationSpells: [
      { level: 3, spell: "Hush — silence one creature on failed save; if you have not spoken since combat start, target also suffers disadvantage on its next attack" },
      { level: 5, spell: "Quiet Step — move silently; advantage on Stealth" },
      { level: 9, spell: "Wordless Ward — shield ally without verbal components" },
      { level: 13, spell: "Still Mind — immunity to charm and frightened while you remain silent this combat; if you break silence, allies in aura gain +2 concentration saves for 1 round" },
      { level: 17, spell: "Silent Judgment — smite without alerting nearby foes; on hit target cannot speak or cast verbal components until end of next turn and you gain advantage on Stealth until you speak" },
    ],
    oathbreaker: {
      name: "Silent Heretic",
      deathTouch: "Silence + psychic damage on touch",
      aura: "Null Command — prevent verbal casting in aura",
      blasphemousWord: "Null Command — mass silence with psychic damage",
    },
    finalOathGift:
      "Vow Absolute — once per day, Vow Unbroken lasts the entire combat if you remain silent; all smites deal +50% psychic damage, enemies within aura cannot cast verbal components, and the first smite each round does not break your vow of silence.",
    draft: true,
    source: "Draft — Aethel Sacred Oath; bounded rulebook-tone pass only, with mechanics and revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
  {
    id: "chain",
    name: "Oath of the Chain",
    theme: "A vigil of iron: martyrdom, warding, and the burden freely borne for another",
    smiteType: "Radiant — bonus damage; when a bonded ally within aura takes damage, redirect up to CHA mod (min 3) to yourself once/round",
    auraEffect: "Aura of Bonds — allies within aura share 10% damage reduction",
    signaturePower: "Warden's Lock — lock enemies in zone; cannot leave without save (1/rest)",
    conductClause: [
      "Stand between the helpless and harm, even when the cost is yours to bear",
      "Keep every ward entrusted to you; do not abandon the bound when danger closes",
      "Take suffering freely to spare another, but never make a chain of their sacrifice",
    ],
    revelationSpells: [
      { level: 3, spell: "Linked Ward — mark ally within aura; as reaction when they take damage, redirect up to 2× CHA mod radiant to yourself; if you fall to 0 HP this round, ally gains temp HP equal to damage redirected" },
      { level: 5, spell: "Chain of Duty — mark ally; teleport to them when they fall" },
      { level: 9, spell: "Martyr's Share — take half ally's damage as reaction" },
      { level: 13, spell: "Unbreakable Bond — chosen ally in aura cannot be charmed, frightened, or magically compelled; when they fail a save vs charm, you may take the effect instead once per round" },
      { level: 17, spell: "Final Stand — for 1 round, absorb all damage dealt to one chosen ally in aura; if you fall to 0 HP from redirected damage, ally gains temp HP equal to your level and resistance to all damage until end of next turn" },
    ],
    oathbreaker: {
      name: "Shackled Lord",
      deathTouch: "Steal reactions on touch",
      aura: "Iron Leash — slow and control debuffs",
      blasphemousWord: "Iron Leash — bind enemies; steal their actions",
    },
    finalOathGift:
      "Unbroken Covenant — once per day, Warden's Lock expands to your full aura radius for 3 rounds; bonded allies share your AC, cannot be moved against their will, and when you redirect damage to yourself they gain temp HP equal to half damage absorbed until the lock ends.",
    draft: true,
    source: "Draft — Aethel Sacred Oath; bounded rulebook-tone pass only, with mechanics and revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
  {
    id: "grief",
    name: "Oath of Grief",
    theme: "Sorrow, remembrance, and the duty of passage",
    smiteType: "Necrotic and radiant — bonus damage; against a creature that killed an ally this combat, the smite deals +1d8 and applies Grief Mark (−1 attacks until end of next turn)",
    auraEffect: "Aura of Mourning — allies gain a bonus on saves against fear; undead suffer disadvantage within the aura",
    signaturePower: "Final Vigil — call upon a fallen ally's memory for one round (1/rest)",
    conductClause: [
      "Keep faith with the dead and with those they leave behind",
      "Do not make sport of grief or profane a place of remembrance",
      "Guide the departed toward rest; do not claim them for undeath",
    ],
    revelationSpells: [
      { level: 3, spell: "Dirge — 30-ft cone or single target; on failed Wis save target −2 attacks and cannot benefit from morale buffs for 1 minute; undead also take 2d6 radiant" },
      { level: 5, spell: "Last Rites — touch or 30 ft on dying creature; stabilize and grant +2 death saves and resistance to necrotic for 1 hour; undead within 10 ft must save or be turned until end of next turn" },
      { level: 9, spell: "Memorial Flame — conjure 30-ft memorial light for 1 minute; reveals hidden undead, grants allies +2 to death saves, and undead in light have disadvantage on attacks" },
      { level: 13, spell: "Sorrow's Weight — 20-ft zone for 3 rounds; creatures save or half speed and 2d6 necrotic each round; undead fail save automatically" },
      { level: 17, spell: "Echo of the Fallen — summon spirit of fallen ally within aura for 1 round; it makes one attack or grants chosen ally +2 AC as reaction" },
    ],
    oathbreaker: {
      name: "Gravetongue",
      deathTouch: "Necrotic + grief effects",
      aura: "Dirge of Ruin — block resurrection and healing",
      blasphemousWord: "Dirge of Ruin — necrotic wave that prevents healing",
    },
    finalOathGift:
      "Dirge of Passage — once per day, Final Vigil can channel two fallen allies simultaneously for 2 rounds; undead in aura suffer vulnerability to radiant and cannot benefit from healing, and survivors gain +2 death saves while either spirit is active.",
    draft: false,
    source: "Canon — Director-approved Oath of Grief (2026-07-30)",
  },
  {
    id: "chains-broken",
    name: "Oath of Chains Broken",
    theme: "Liberty, the breaking of unjust bonds, and freedom guarded against a new tyranny",
    smiteType: "Force or radiant — bonus damage vs oppressors and bound foes; on hit, target loses grapple or restraint until end of next turn",
    auraEffect: "Aura of Liberation — allies resist restraint; escape grapple as bonus action once/turn in aura",
    signaturePower: "Righteous Quake — break bindings; AoE push and damage (1/rest)",
    conductClause: [
      "Break the bonds of the unjustly imprisoned, and do not turn liberation into license to abandon them",
      "Resist every tyrant, including the one who would rule in freedom's name",
      "Guard the newly freed from exploitation, for an open door is not yet a safe road",
    ],
    revelationSpells: [
      { level: 3, spell: "Break Bonds — touch or 30-ft ally; end one restraint or grapple; if ally was magically bound, +10 ft movement and advantage on next escape attempt until end of next turn" },
      { level: 5, spell: "Liberty's Step — ignore opportunity attacks when moving to ally" },
      { level: 9, spell: "Shatter Shackles — dispel magical restraint in area" },
      { level: 13, spell: "Revolution's Cry — allies in aura gain +10 ft movement and advantage on saves vs restraint for 3 rounds; oppressors in aura save or lose reaction until end of next turn" },
      { level: 17, spell: "Unbound Host — party in aura cannot be restrained or magically bound for 1 minute; when an ally breaks free, they gain +10 ft movement until end of next turn" },
    ],
    oathbreaker: {
      name: "Unbound Flame",
      deathTouch: "Burn and charm effects",
      aura: "Reign of Ashes — prevent buffs and escape",
      blasphemousWord: "Reign of Ashes — chaotic fire that traps foes",
    },
    finalOathGift:
      "Liberty Unbound — once per day, Righteous Quake breaks all magical restraint on allies in aura, grants +10 ft movement and immunity to grapple for 3 rounds, and oppressors in the burst save or are pushed 10 ft and lose reactions until end of next turn.",
    draft: true,
    source: "Draft — Aethel Sacred Oath; bounded rulebook-tone pass only, with mechanics and revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
  {
    id: "martyr-king",
    name: "Oath of the Martyr King",
    theme: "Stewardship, the burden of the crown, and sacrifice freely borne for those in your care",
    smiteType: "Radiant — bonus damage; allies in aura gain temp HP when you smite; you may redirect 5 damage from one ally per round",
    auraEffect: "Aura of the Crown — allies +1 saves; you may redirect damage from one ally per round",
    signaturePower: "Crown of Embers — team-wide DR + damage redirection (1/rest)",
    conductClause: [
      "Bear the responsibility of command without treating those in your care as a means to your glory",
      "Set the realm's need above personal gain, and spend your own strength before you spend another's",
      "Never demand a burden you would not freely take upon yourself",
    ],
    revelationSpells: [
      { level: 3, spell: "Noble Bearing — allies within aura +1 to morale saves; when you smite, one chosen ally gains temp HP equal to half radiant dealt" },
      { level: 5, spell: "Royal Decree — command one creature within 30 ft; on failed Wis save it kneels prone or moves up to its speed toward you; allies in aura gain +1 to morale saves until end of next turn" },
      { level: 9, spell: "Burden Shared — distribute damage among willing allies" },
      { level: 13, spell: "Throne's Grace — Lay on Hands and healing you grant reach full aura radius for 3 rounds; allies in aura heal +1 HP per die and gain +1 death saves while the grace persists" },
      { level: 17, spell: "Last King's Gift — when ally in aura would drop to 0 HP, they drop to 1 HP instead and gain temp HP equal to your level once per combat per ally" },
    ],
    oathbreaker: {
      name: "Usurper's Crown",
      deathTouch: "Steal passive powers on touch",
      aura: "Crownshatter Decree — damage required for healing",
      blasphemousWord: "Crownshatter Decree — steal boons from allies",
    },
    finalOathGift:
      "Crown Undying — once per day, Crown of Embers lasts 3 rounds without concentration; damage you redirect heals the ally for half absorbed, allies in aura gain +1 saves while the crown persists, and you may redirect from two allies per round.",
    draft: true,
    source: "Draft — Aethel Sacred Oath; revelation spells pending author review (see CONTINUITY_GLOSSARY: Sacred Oath / Revelation spells)",
  },
];

/** Aura radius milestones (all oaths) — rulebook canon */
export const PALADIN_AURA_SCALING = [
  { level: 3, radius: "10 ft", note: "Base aura active while conscious" },
  { level: 6, radius: "15 ft", note: "Secondary benefit (DR, saves)" },
  { level: 7, radius: "15 ft", note: "Reactive Smite or spell trigger" },
  { level: 10, radius: "20 ft", note: "Persists 1 round if incapacitated" },
  { level: 15, radius: "30 ft", note: "Debuff enemies or buff allies" },
  { level: 17, radius: "30 ft", note: "Aura Surge (1/rest)" },
  { level: 20, radius: "30+ ft", note: "Divine Manifestation — auto on initiative" },
];

export function getOathById(id) {
  return SACRED_OATHS.find((o) => o.id === id);
}

export function getOathByName(name) {
  return SACRED_OATHS.find((o) => o.name === name || o.id === name);
}

export default SACRED_OATHS;
