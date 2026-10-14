/**

 * Oracle Curses — rulebook canon + Aethel draft boons.

 * Spiral-Touched is the only fully worked rulebook example; nine others are playable drafts.

 */



/** @typedef {object} OracleCurseBoon

 * @property {number} level

 * @property {string} name

 * @property {string} description

 */



/** @typedef {object} OracleCurse

 * @property {string} id

 * @property {string} name

 * @property {string} blurb

 * @property {string[]} [limitations]

 * @property {OracleCurseBoon[]} boons

 * @property {boolean} [draft]

 * @property {string} [source]

 */



/** @param {number} level */

export function curseBoonsAtLevel(level) {

  return (curse) => curse.boons.filter((b) => b.level === level);

}



/** @type {OracleCurse[]} */

export const ORACLE_CURSES = [

  {

    id: "spiral-touched",

    name: "Spiral-Touched",

    blurb: "Manipulates initiative, gains time-based echoes",

    limitations: [

      "You sometimes respond to events before they happen, causing confusion in social situations",

      "You occasionally experience time differently than others, potentially missing turns in combat (5% chance)",

      "You cannot maintain concentration on mundane tasks for extended periods",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "See 1 round into the future during initiative (+3 initiative). Once per day, reroll a failed save as you briefly step outside the timestream.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "Spend 1 Revelation Charge to act out of turn once per combat. You gain resistance to time-based magic and aging effects.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "When you would be reduced to 0 HP, you may instead phase out of time for 1 round, becoming untargetable and regaining 25% of your maximum HP. Once per long rest.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "You exist in multiple timestreams simultaneously, allowing you to make two different actions in a single turn once per combat. Enemies attacking you have a 10% chance to hit your echo instead, causing the attack to miss.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "You gain the ability to create a time loop, resetting an entire combat encounter to its beginning state once per day. All allies retain knowledge of the original timeline, allowing them to make different choices.",

      },

    ],

    source: "rulebook — Example Curse: Spiral-Touched (only full curse tree in player rulebook)",

  },

  {

    id: "wound-eater",

    name: "Wound Eater",

    blurb: "Lives by wounds taken from the living, never by an easy cure",

    limitations: [

      "Natural healing and healing granted by another restore only half their usual amount to you",

      "Before each long rest ends, you must drain life from a living foe or gain Exhaustion",

      "Your flesh carries a hollow, withered look that makes many mortals recoil at first meeting",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "When you hit a living foe with a weapon or touch attack, drain 1d6 HP; you heal for half the amount drained. Undead and constructs are immune.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "When you reduce a living foe to 0 HP, regain 1 Revelation Charge. Resistance to necrotic damage from non-Revelation sources.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "Once per short rest, siphon a dying enemy's remaining HP as a burst heal (up to 25% of your max HP). The Pale Ledger records their final breath.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Drain aura: at the start of your turn, living enemies within 2 tiles take necrotic damage; you heal for the total drained. You may suppress this aura in civilized areas.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, become a conduit of the unfinished hunger — all living enemies within 4 tiles lose 25% max HP; you heal for half the total. Allies are unaffected.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

  {

    id: "soul-cracked",

    name: "Soul-Cracked",

    blurb: "A fractured spirit refuses easy command and answers magic unevenly",

    limitations: [

      "Divination reads your aura and alignment inconsistently; even allies struggle to scry your intent",

      "Once each encounter, the resonance type of your Revelations may shift without warning",

      "Binding oaths and geas magic cause you physical pain until they are resolved",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "Immune to charm and compulsion. Once per day, reroll a failed save against mind-affecting effects as your soul fractures around the blow.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "After rolling initiative, choose once per combat to shift the damage type of your next Revelation (fire, cold, lightning, necrotic, psychic, or radiant). Until that Revelation resolves, your aura reads as blank to divination — scrying your intent fails for the round.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "When you would be charmed or dominated, reflect the effect onto the source (once per long rest). The source must save or suffer the effect instead.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Fractured soul: gain resistance to psychic damage and +2 to saves vs control. Divination targeting you has 50% chance to return contradictory results.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, shatter a binding curse, geas, or possession on yourself or an ally within 3 tiles. The broken magic lashes the originator for psychic damage.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

  {

    id: "haunted",

    name: "Haunted",

    blurb: "Restless dead attend your steps, offering aid at a social cost",

    limitations: [

      "Restless spirits draw attention: you suffer −2 to Stealth in haunted places or crowded civilized areas",

      "Spirits sometimes speak through you at inopportune moments; social checks may require a Wisdom save",

      "You sometimes address people who are not yet present, unsettling those who witness it",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "Spectral attendants grant +1 AC against the first attack each round. Once per day, a spirit whispers a warning — you cannot be surprised.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "Once per combat, a bound spirit intercepts a single-target attack against you, absorbing up to 5 + level damage before dissipating. The spirit wails as it fades — the attacker must save or suffer −2 to their next attack as dread clings to them.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "Spirits murmur of danger — you and allies within 3 tiles cannot be surprised while you are conscious. Echoes of the dead grant +2 to Insight checks nearby.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Summon a wailing chorus: enemies within 3 tiles suffer Dread (−10% hit chance and saves) for 2 turns. Once per long rest.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, bind a hostile or friendly spirit to scout, speak with the dead at a distance, or deliver a prophetic message along a path you have walked. The spirit persists for 10 minutes or until it completes one task; when it returns, it whispers what it saw and one name you did not send it to find.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

  {

    id: "tongues",

    name: "Tongues",

    blurb: "Many voices share your speech, making truth harder to hear cleanly",

    limitations: [

      "Unless you suppress the curse, social checks with mortals who do not share your mystery tongue suffer −2",

      "Even accurate prophetic speech is often misheard; listeners may hear what they fear",

      "You cannot fully silence the chorus; concentrating on mundane tasks longer than 1 hour requires a Wisdom save",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "Understand all spoken languages and read divine script fragments. Allies within 5 tiles gain +2 to Lore and Insight checks when you interpret for them.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "Confounding babble: one enemy within 3 tiles must save or lose their next action, overwhelmed by overlapping voices. Once per combat.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "Prophetic utterance — force one creature within 3 tiles to truthfully answer a yes/no question drawn from the Choir's echo. Once per day.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Polyglot surge: communicate with beasts, plants, and spirits for 1 hour as the First Song's vocabulary flows through you. Once per long rest.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, speak a single Word in the tongue of creation — all who hear must save or obey one short command. Those who resist take psychic damage.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

  {

    id: "burning-blood",

    name: "Burning Blood",

    blurb: "Air kindles your spilled blood into a fire that harms friend and foe alike",

    limitations: [

      "When slashing or piercing damage wounds you, you and adjacent foes take 1d4 fire damage as your blood sparks",

      "You cannot benefit from cold-based healing or resistances; your curse rejects the chill",

      "Open wounds glow faintly, imposing −2 to Stealth until treated or until you rest",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "Resistance to fire. Melee attackers take 1d4 fire damage when they hit you with a weapon attack. Your wounds smolder briefly — enemies within 1 tile take 1 fire damage when your blood first ignites each round.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "Spend 1 Revelation Charge to ignite your blood — your next Revelation deals +50% fire damage and cannot be extinguished by mundane means. While ignited, slashing and piercing damage against you no longer sparks fire on adjacent allies; the Crown's flame answers only to your will.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "When your blood ignites from damage, allies within 2 tiles gain +10% weapon damage for 1 round as shard-fire answers your pain. You may extend the flare to 3 tiles by spending 1 Revelation Charge — enemies in the burst take 1d4 fire damage as embers leap from your wounds.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Blood flare: when reduced below 50% HP, erupt fire in a 3-tile burst (once per short rest). Enemies take fire damage; you are not harmed by your own flare.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, become a living pyre for 3 rounds — fire aura in 3 tiles; enemies take fire damage at start of turn; you heal 1d6 when an enemy takes fire damage from you. Allies in the aura gain fire resistance and treat your ignited blood as bright light that reveals hidden foes within 2 tiles.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

  {

    id: "false-life",

    name: "False Life",

    blurb: "Magic mistakes your living breath for death and answers accordingly",

    limitations: [

      "Healing spells cast on you without a successful Insight check have a 50% chance to fail; magic reads you as corpse-cold",

      "Unless you suppress the curse, divination treats you as undead",

      "Clerics of life-deities may hesitate to aid you without proof that you still breathe",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "Advantage on saves vs death effects and negative energy. Once per long rest, when you would die, stabilize at 1 HP as your body feigns death perfectly.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "Feign death perfectly for 1 minute — undead ignore you unless attacked; you remain conscious but motionless. Once per combat.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "When reduced to 0 HP, remain conscious for 1 round before falling — you may move, speak, or cast one Revelation. Once per long rest.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Necrotic resilience: +10% DR vs necrotic and negative energy. Undead attackers have 10% chance to miss you entirely, sensing kinship.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, return from death's threshold — after 1 round of appearing dead at 0 HP, rise at 25% max HP with immunity to necrotic for 2 rounds. Undead within 3 tiles treat you as kin until you act, and divination cast during your feigned death returns false results of your choosing.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

  {

    id: "shattered-mind",

    name: "Shattered Mind",

    blurb: "Your thoughts divide into competing fragments that act before they agree",

    limitations: [

      "Concentration checks are at −2 as competing thoughts contend for control",

      "In tense social scenes, make a Wisdom save or speak a prophetic fragment aloud on an impulse not wholly your own",

      "After a long rest, make a Wisdom save or wake with fragmented memories of others' dreams",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "Once per combat, take a bonus move or activate one Tier I Revelation as a bonus action (not both a full action and bonus action in the same turn). The fragment acting is not wholly yours — observers may hear you answer questions you were never asked.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "Fragmented focus: +2 initiative; immune to being stunned. Your initiative roll may be made twice — take the higher result.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "Split thought: maintain two Revelation effects simultaneously for 1 round without paying double charges. Once per combat.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Mind echo: reroll one failed Intelligence or Wisdom check per short rest. Prophetic fragments grant +2 to Insight when reading motives.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, act twice in a single round — second action may be a Revelation or move only. Each action uses a different fragment of your mind.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

  {

    id: "consumed",

    name: "Consumed",

    blurb: "Your Mystery remakes your body until its element shows through",

    limitations: [

      "As you gain levels, your appearance shifts toward your Mystery's theme: flame hair, starlit eyes, bone protrusions, and the like",

      "Some civilized NPCs react with fear or awe; concealing the change in formal courts requires ongoing effort",

      "As your body changes, armor and gear must be refitted periodically (roleplay / downtime cost)",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "Gain +5% resistance aligned with your Mystery's element or theme (fire, necrotic, force, psychic, etc.). Once per day, suppress visible transformation for 1 hour in civilized areas — the Mystery still leaks through divination.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "Elemental skin: +1 AC while wearing light or no armor as your flesh hardens into mystery-matter. Unarmed strikes and natural weapons you wield count as magical and deal +1d4 thematic damage.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "Mystery infusion: weapon and touch attacks deal +1d4 thematic damage matching your Mystery. Revelation potency visibly bleeds into your strikes.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Partial transformation: ignore difficult terrain tied to your Mystery (fire walks, shadow steps, temporal stutter, etc.). Allies who follow within 1 tile during the same round may treat that terrain as normal ground until your next turn.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, fully embody your Mystery's element for 3 rounds — immunity to that damage type, +2 effective Revelation potency, and visible manifestation (aura, wings of flame, star corona, etc.). Allies within 2 tiles gain +1 AC as your transformation steadies the battlefield; suppression is impossible while the embodiment lasts.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

  {

    id: "fate-bound",

    name: "Fate-Bound",

    blurb: "Foreknowledge marks your path, but each omen narrows the road ahead",

    limitations: [

      "You cannot voluntarily break a sworn oath or prophecy without losing 1 Revelation Charge and suffering psychic backlash",

      "Major life choices may feel predetermined once you have seen the threads that lead to them",

      "Trying to flee a foreseen disaster without confronting it imposes −2 to saves until you face the omen",

    ],

    boons: [

      {

        level: 3,

        name: "Curse Boon I",

        description:

          "Once per day, glimpse one likely outcome before a party decision — the ally acting gains +2 to the related check or save. You must speak the omen aloud; allies who heard it retain the bonus even if the party chooses a different path.",

      },

      {

        level: 5,

        name: "Curse Boon II",

        description:

          "Fated dodge: once per combat, force an attack against you to reroll as fate rewinds the strike. You must declare after the roll but before damage.",

      },

      {

        level: 10,

        name: "Curse Boon III",

        description:

          "When an ally within 5 tiles would critically fail a save, you may accept the failure on yourself instead (once per long rest). The thread binds to you.",

      },

      {

        level: 15,

        name: "Curse Boon IV",

        description:

          "Thread of destiny: +2 to saves vs death, fate-altering magic, and effects that would remove you from a prophesied path. Once per long rest, reroll a failed death save as the Concord refuses to cut your thread early.",

      },

      {

        level: 20,

        name: "Curse Boon V",

        description:

          "Once per day, declare a prophetic outcome — one ally within 6 tiles auto-succeeds their next save or attack as the Concord enforces the written thread. You must describe the outcome aloud before the roll; if the prophecy fails to come true by end of combat, you lose 1 Revelation Charge as the thread frays.",

      },

    ],

    draft: true,

    source: "Draft — Aethel lore, pending author review",

  },

];



/** Revelation charge pool — rulebook Core Mechanics */

export const ORACLE_REVELATION_CHARGES = {

  initial: 3,

  maximum: 7,

  note: "Revelation Charges power Mystery Revelations (initially 3, maximum 7). Each Mystery has a Prophecy Trigger to recover charges.",

};



/** Curse boon unlock levels shared by all curses — rulebook L3–20 framework */

export const ORACLE_CURSE_BOON_LEVELS = [3, 5, 10, 15, 20];



/** What the player rulebook actually contains — for gap reporting */

export const ORACLE_CURSE_RULEBOOK_STATUS = {

  cursesNamed: 10,

  cursesWithFullTree: 1,

  fullTree: ["Spiral-Touched"],

  draftTree: [

    "Wound Eater",

    "Soul-Cracked",

    "Haunted",

    "Tongues",

    "Burning Blood",

    "False Life",

    "Shattered Mind",

    "Consumed",

    "Fate-Bound",

  ],

};



/** @param {string} id */

export function getCurseById(id) {

  return ORACLE_CURSES.find((c) => c.id === id) ?? null;

}



export default ORACLE_CURSES;

