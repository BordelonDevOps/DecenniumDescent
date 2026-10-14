/**
 * Oracle Mysteries — rulebook canon + Aethel draft tiers.
 *
 * Canon (player rulebook + Director approval): Ancestor and Shadow full trees.
 * Draft (author review): Battle–Time except Shadow full revelation trees — Aethel lore, tier structure
 *   inspired by Pathfinder Oracle mysteries / EQ class identity; not imported names.
 *
 * draftCap: docs/mechanics/CLASS_CEILING_CAPS.md — RC 3–7, 1 RC recovery/round,
 *   1 revelation/round, turn-denial per target; see class-ceiling-caps.js
 *
 * Sources: tools/oracle_rulebook_extract.txt, rulebook_output.txt
 */

/** @typedef {object} OracleRevelation
 * @property {string} name
 * @property {number} [charges]
 * @property {"passive" | "active"} kind
 * @property {string} description
 */

/** @typedef {object} OracleMystery
 * @property {string} id
 * @property {string} name
 * @property {string} theme
 * @property {string} [patron]
 * @property {string} [prophecyTrigger]
 * @property {string} [combatRole]
 * @property {string} [reputation]
 * @property {string} [rulebookRef]
 * @property {OracleRevelation} [level1]
 * @property {OracleRevelation[]} [tierI]
 * @property {OracleRevelation[]} [tierII]
 * @property {OracleRevelation} [tierIII]
 * @property {OracleRevelation} [mysticInsight]
 * @property {string[]} [revelationMastery]
 * @property {OracleRevelation} [propheticSurge]
 * @property {OracleRevelation} [finalRevelation]
 * @property {boolean} [draft]
 * @property {string} [source]
 * @property {string} [missingFromRulebook]
 */

/** Shared L1–2 base skills — rulebook extract lines 43–48 */
export const ORACLE_BASE_SKILLS = [
  "Channel Revelation — activate a Mystery Revelation (costs Revelation Charges)",
  "Prophetic Insight — brief glimpse of possible futures; advantage on next action",
  "Curse Manifestation — intensify Curse for benefits at increased limitations",
  "Divine Sense — detect divine, undead, or extraplanar entities",
  "Oracular Trance — prophetic visions related to a question or situation",
];

/** Shared L3–20 framework — rulebook extract lines 49–74 */
export const ORACLE_SHARED_PROGRESSION = [
  { level: 3, feature: "Tier I Revelation (choose 1, 1 charge) + Curse Boon I" },
  { level: 5, feature: "Curse Boon II" },
  { level: 6, feature: "Tier II Revelation (choose 1, 2 charges)" },
  { level: 9, feature: "Tier III Revelation (Mystery capstone, 3 charges)" },
  { level: 10, feature: "Curse Boon III" },
  { level: 12, feature: "Mystic Insight — minor Revelation or passive from your Mystery" },
  { level: 15, feature: "Revelation Mastery + Curse Boon IV" },
  { level: 18, feature: "Prophetic Surge (1/day free or extended Revelation)" },
  { level: 20, feature: "Final Revelation + Curse Boon V" },
];

/** @type {OracleMystery[]} */
export const ORACLE_MYSTERIES = [
  {
    id: "ancestor",
    name: "Ancestor",
    theme: "Connection to ancestral spirits and legacy",
    patron: "Echo Court (an ancestral spirit chorus that binds lineage across time)",
    prophecyTrigger: "When you aid an ally who lands a critical hit, regain 1 Revelation Charge",
    combatRole:
      "Excel at supporting allies through spiritual guidance and protection, calling upon ancestral spirits to enhance the party's capabilities while providing tactical advantages.",
    reputation:
      "Often welcomed in civilized areas, their connections to positive divine forces making them valued advisors and healers.",
    rulebookRef: "Example Mystery: Ancestor — rulebook extract lines 75–125",
    level1: {
      name: "Ancestral Guardian",
      kind: "active",
      description:
        "Passive: spectral guardian grants +1 AC vs first attack each round and +5% resistance to mind-affecting effects. Once per long rest, intercept a single-target attack against an ally within 3 tiles (guardian takes the hit and vanishes until long rest).",
    },
    tierI: [
      {
        name: "Echo Voice",
        charges: 1,
        kind: "active",
        description:
          "Passive: telepathy with allies within 5 tiles. Active: spend 1 charge to let an ally repeat their last failed roll (attack, save, or skill) with +2.",
      },
      {
        name: "Ancestral Strike",
        charges: 1,
        kind: "active",
        description:
          "Spend 1 charge to channel a warrior ancestor. Next weapon or touch attack deals +50% bonus weapon damage and stuns on crit.",
      },
      {
        name: "Bloodline Sight",
        charges: 1,
        kind: "active",
        description:
          "Spend 1 charge to reveal all undead, invisible, or ethereal creatures within 6 tiles for 2 rounds; they cannot benefit from concealment or stealth.",
      },
    ],
    tierII: [
      {
        name: "Spirit Walk",
        charges: 2,
        kind: "active",
        description:
          "Spend 2 charges: leave your body for 1 turn — intangible, move through walls/creatures, cannot be targeted, may cast a Revelation through your spirit at full range.",
      },
      {
        name: "Echo Armor",
        kind: "passive",
        description:
          "+10% resistance to non-magical damage. Once per short rest, when reduced to 0 HP, an ancestral echo absorbs the blow and leaves you at 1 HP.",
      },
      {
        name: "Ghost Chant",
        charges: 2,
        kind: "active",
        description:
          "Spend 2 charges to inflict Dread on enemies within 3 tiles (−10% hit chance and saves for 2 turns).",
      },
    ],
    tierIII: {
      name: "Bloodline Convergence",
      charges: 3,
      kind: "active",
      description:
        "Spend 3 charges: for 2 turns, +2 actions per turn (Revelation or movement only); allies within 5 tiles gain +10% crit, +5% DR, immunity to Fear; cast 1 Revelation per round at no cost. After: Exhausted (−1 action, −10% resist for 1 round).",
    },
    mysticInsight: {
      name: "Ancestral Whispers",
      kind: "passive",
      description:
        "Advantage on History checks and immunity to surprise. Once per day, consult ancestors for cryptic but useful guidance.",
    },
    revelationMastery: [
      "Enhanced Echo Voice: affects all allies within range simultaneously",
      "Enhanced Spirit Walk: duration increased to 2 turns",
      "Enhanced Bloodline Convergence: no longer causes Exhaustion",
    ],
    propheticSurge: {
      name: "Ancestral Confluence",
      kind: "active",
      description:
        "Once per day, call all ancestors to cast any Revelation at no charge cost. For 1 turn after, all Revelations cost 1 fewer charge (minimum 0).",
    },
    finalRevelation: {
      name: "Echo Crowned",
      kind: "active",
      description:
        "Maintain 3 passive ancestral spirits (offense, defense, utility). Once per day, cast any Revelation twice in one turn using different Echoes. Sacrifice an Echo to prevent a party member's death or restore all Revelation Charges.",
    },
    source: "rulebook — Example Mystery: Ancestor (only full tier tree in player rulebook)",
  },
  {
    id: "battle",
    name: "Battle",
    theme:
      "The hard counsel of the battle line: courage held for others, command under fire, and fury made answerable to the living",
    combatRole:
      "Hold the line where it is breaking, turn a companion's opening into a shared advantage, and spend divine fury to keep the company moving rather than to chase glory.",
    reputation:
      "Earn respect among those who have stood beside them and caution among those who have seen a battle-oath carried too far; their conduct is judged by whom they bring home.",
    rulebookRef: "Mysteries list line 23; Combat Strategy line 152",
    ...draftMysteryRevelations({
      patron: "War Chorus (fallen champions of the Tenfold Cycles who speak through banner, blood, and battle-oaths)",
      prophecyTrigger: "When you or an ally drops an enemy to 0 HP, regain 1 Revelation Charge",
      level1: {
        name: "Omen of the Host",
        kind: "active",
        description:
          "Passive: you gain +1 to hit on your first attack each round, +5% resistance to fear, and cannot be surprised while conscious. Once per short rest, whisper a battle-oath to an ally within 3 tiles — they gain +2 initiative, advantage on their next attack, and +5% DR until the start of your next turn.",
      },
      tierI: [
        {
          name: "Vanguard's Step",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: you and one ally within 3 tiles may immediately move up to 2 tiles without provoking attacks; the ally gains +5% DR until start of your next turn and you both have advantage on opportunity attacks made before end of turn.",
        },
        {
          name: "Host's Cry",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: allies within 4 tiles gain +10% weapon damage and +5% DR for 2 rounds as the War Chorus roars through you; the first ally to drop an enemy while the cry persists regains 1d6 HP and you regain 1 Revelation Charge (once per cry).",
        },
        {
          name: "Mark of the Doomed",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: mark one enemy you can see for 2 rounds — you and allies within 5 tiles gain +2 to hit and +10% crit chance against them; the first attack that crits the mark deals +1d6 bonus damage and the marked target cannot benefit from concealment until the mark fades.",
        },
      ],
      tierII: [
        {
          name: "Divine Fury",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: for 2 rounds, your weapon and touch attacks deal +50% bonus weapon damage and ignore 5% DR; the War Chorus roars through each strike — on a critical hit, the target must save or suffer Fear (−10% hit) until end of next turn, and your second attack during the fury may be made as a bonus action if the first hit.",
        },
        {
          name: "Field Command",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: one ally within 5 tiles may immediately take a reaction to attack, move, or activate a class feature; the War Chorus marks them with command — they gain +10% damage on that action, +5% DR until start of your next turn, and you may grant a second ally within 5 tiles a free 1-tile reposition without provoking before the command resolves.",
        },
        {
          name: "Relentless Strike",
          kind: "passive",
          description:
            "Passive: when you miss with an attack, the War Chorus steels your next strike — gain +5% hit chance (stacks once) and +10% weapon damage if that attack hits. On a critical hit, regain 1 Revelation Charge (once per round) and the target must save or suffer Fear (−10% hit) until end of next turn.",
        },
      ],
      tierIII: {
        name: "Fury of the Host",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, allies within 5 tiles gain +1 action per turn (attack or move only), +10% crit chance, and +5% DR as the War Chorus banners them — you gain +2 AC and immunity to Fear; once per round you may cast one Tier I Battle Revelation at no cost, and the first ally to drop an enemy each round regains 1d6 HP. After: Exhausted (−1 action, −10% resist for 1 round).",
      },
      mysticInsight: {
        name: "Battle-Seer's Eye",
        kind: "passive",
        description:
          "Advantage on Perception and Initiative. Once per day, foretell an enemy's opening strike — you and one ally gain +2 AC against that enemy's next attack.",
      },
      revelationMastery: [
        "Enhanced Host's Cry: bonus damage and DR extend to all allies within 6 tiles",
        "Enhanced Divine Fury: affects a third attack",
        "Enhanced Fury of the Host: no longer causes Exhaustion",
      ],
      propheticSurge: {
        name: "War Prophecy",
        kind: "active",
        description:
          "Once per day, the War Chorus speaks through you — cast any Battle Revelation at no charge cost. For 1 round after, allies within 5 tiles gain +5% DR and +10% weapon damage as the host's banners flare; your next Tier I Revelation this encounter costs 0 charges.",
      },
      finalRevelation: {
        name: "Avatar of the War Chorus",
        kind: "active",
        description:
          "Once per day, manifest three War Chorus banners (offense, defense, rally) around you for 3 rounds: +2 AC, +2 attacks per turn, and all Tier I Revelations cost 0 charges. Allies within 5 tiles gain +5% DR and +10% weapon damage as the host answers; sacrifice a banner to prevent a party member's death or restore all Revelation Charges. When the banners fall, restore 2 Revelation Charges.",
      },
    }),
  },
  {
    id: "bones",
    name: "Bones",
    theme:
      "The unfinished account of death: decay faced without ornament, the rest owed to the fallen, and power borrowed only from what cannot speak for itself",
    combatRole:
      "Read the cost written in bone and breath, deny the enemy easy return, and use the dead's lingering force to shelter the living without mistaking command for ownership.",
    reputation:
      "Met with unease, especially near graves and battlefields; those who travel with them learn to watch whether their care for the dead matches the power they wield.",
    rulebookRef: "Mysteries list line 24; Combat Strategy line 153",
    ...draftMysteryRevelations({
      patron: "Pale Ledger (a chorus of unfinished deaths bound since the Binding of the Old God)",
      prophecyTrigger: "When an undead creature or a dying foe within 5 tiles perishes, regain 1 Revelation Charge",
      level1: {
        name: "Grave Attendant",
        kind: "active",
        description:
          "Passive: undead within 3 tiles treat you as neutral unless attacked, and you gain +5% resistance to necrotic damage. Once per long rest, animate one corpse within 2 tiles as a skeletal servant (1 HP, 1 attack) for 3 rounds — it intercepts the next single-target hit meant for you before crumbling.",
      },
      tierI: [
        {
          name: "Bone Whisper",
          charges: 1,
          kind: "active",
          description:
            "Passive: speak with corpses and recent dead as if under Speak with Dead. Active: spend 1 charge to learn one hidden truth a corpse witnessed before death; undead within 2 tiles must save or become unable to act until end of your next turn as the Pale Ledger speaks through the bones.",
        },
        {
          name: "Marrow Drain",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: touch attack deals 2d6 necrotic damage and you heal for half damage dealt; undead targets take +50% damage and cannot regain HP until end of your next turn as the Pale Ledger tallies their debt.",
        },
        {
          name: "Ashen Shroud",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: cloak yourself in grave-dust for 2 rounds — +10% DR vs non-magical damage, +5% necrotic resistance, and enemies within 2 tiles suffer −10% hit chance and −10% saves vs fear; when the shroud ends, corpses within 2 tiles cannot be raised as undead for 1 hour.",
        },
      ],
      tierII: [
        {
          name: "Ledger's Command",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: command up to 2 undead within 4 tiles for 2 rounds — each may attack once per round using your Revelation with +10% damage; commanded undead gain +5% DR and one may intercept the next single-target hit meant for you before crumbling (once per command).",
        },
        {
          name: "Rotting Touch",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: touch attack inflicts Decay — target takes +25% damage from all sources and −10% saves for 3 rounds; the Pale Ledger tallies their rot — on a failed save they also cannot regain HP and corpses within 2 tiles of them cannot be raised as undead until Decay ends; if the target is undead, they take 2d6 necrotic immediately and you heal half.",
        },
        {
          name: "Death's Threshold",
          kind: "passive",
          description:
            "When reduced below 25% HP, gain +10% necrotic resistance, +5% DR vs non-magical damage, and +1 to Revelation saves until healed above half HP (once per short rest) — the Pale Ledger marks you as owed, not finished; undead within 3 tiles hesitate to target you (−10% hit on their first attack each round while below threshold).",
        },
      ],
      tierIII: {
        name: "Unfinished Chorus",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, all enemies within 4 tiles suffer Dread (−10% hit/saves) as the Pale Ledger sings their unfinished deaths — once per round drain 1d6 HP from one target (heal half or redirect half to an ally within 3 tiles); undead you control gain +10% damage and +5% DR, and corpses within 4 tiles cannot be raised as undead until the chorus ends. After: Exhausted (−1 action, −10% necrotic resist for 1 round).",
      },
      mysticInsight: {
        name: "Ledger's Memory",
        kind: "passive",
        description:
          "Advantage on checks to identify undead, poison, and disease. Once per day, consult the Pale Ledger for the name and cause of death of any corpse you touch.",
      },
      revelationMastery: [
        "Enhanced Marrow Drain: also slows target movement by 1 tile",
        "Enhanced Ledger's Command: affects 3 undead",
        "Enhanced Unfinished Chorus: you may redirect drained HP to an ally within 3 tiles",
      ],
      propheticSurge: {
        name: "Death's Prophecy",
        kind: "active",
        description:
          "Once per day, cast any Bones Revelation at no cost. For 1 round, you and allies within 3 tiles gain +10% DR vs necrotic.",
      },
      finalRevelation: {
        name: "Ledger Unbound",
        kind: "active",
        description:
          "Once per day, open the Pale Ledger across the battlefield — all enemies within 5 tiles must save or suffer 25% max HP necrotic damage as unfinished deaths are tallied; you may raise up to 3 fallen corpses as loyal bone servants for 3 rounds (each may attack once per round and intercept one hit meant for you). Undead you control during the effect gain +10% damage and +5% DR.",
      },
    }),
  },
  {
    id: "cataclysm",
    name: "Cataclysm",
    theme: "Destruction, upheaval, and the perilous mercy of breaking what cannot endure",
    combatRole:
      "Turn the battlefield's fractures into an advantage, bringing down positions that cannot hold while opening a hard-won path for allies through earthquake, storm, and fire.",
    reputation:
      "Frequently met with fear or guarded respect: a Cataclysm oracle is remembered for the wall they broke, and for what stood behind it.",
    rulebookRef: "Mysteries list line 25; Combat Strategy line 154",
    ...draftMysteryRevelations({
      patron: "Shattered Seal (the wound left when the Old God was bound in the Descent's deepest tier)",
      prophecyTrigger: "When you deal area damage to 2 or more enemies with a Revelation, regain 1 Revelation Charge",
      level1: {
        name: "Tremor Sense",
        kind: "active",
        description:
          "Passive: detect structural instability and hidden passages within 3 tiles, and +5% resistance to bludgeoning damage. Once per short rest, cause a minor tremor — enemies within 2 tiles must save or fall prone; on success they still suffer −1 movement until your next turn.",
      },
      tierI: [
        {
          name: "Shardburst",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: erupt stone shards in a 2-tile burst centered on a point within 4 tiles — enemies take 1d6 bludgeoning and suffer −1 movement for 1 round; on a failed save they also fall prone if adjacent to a wall or rubble.",
        },
        {
          name: "Gale of Unmaking",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: unleash a 4-tile line of forceful wind — enemies in the path take 1d6 bludgeoning, are pushed 1 tile, and suffer −1 movement until your next turn; mundane flames are extinguished and loose debris becomes difficult terrain for 1 round.",
        },
        {
          name: "Fault Line",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: erupt a 3-tile line of cracked earth for 3 rounds — difficult terrain; enemies entering or starting turn there take 1d4 bludgeoning and must save or fall prone if adjacent to a wall; structures along the line may develop cracks (DM discretion).",
        },
      ],
      tierII: [
        {
          name: "Upheaval",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: erupt a 3-tile burst earthquake — enemies save or fall prone and take 2d6 bludgeoning damage; structures may crack (DM discretion); allies in the burst are immune to prone and gain +5% DR until start of your next turn as the Shattered Seal's tremor passes through them.",
        },
        {
          name: "Storm Crown",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: crown yourself in the Shattered Seal's storm for 2 rounds — at start of each of your turns, enemies within 3 tiles take 2d6 lightning or thunder damage (your choice) and must save or suffer −10% hit until end of turn; allies in the storm gain +5% DR vs ranged attacks and cannot be knocked prone by weather.",
        },
        {
          name: "Instability",
          kind: "passive",
          description:
            "Passive: when you take damage from an enemy, you may spend 1 charge as a reaction to fracture the Shattered Seal's wound — deal half that damage back as force in a 1-tile burst (once per round); enemies in the burst must save or fall prone, and allies in the burst gain +5% DR until start of your next turn as the tremor passes through them.",
        },
      ],
      tierIII: {
        name: "Seal's Fracture",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, once per turn create a 4-tile cataclysm zone (earthquake, storm, or fire — choose when cast) as the Shattered Seal weeps — enemies inside take 2d6 damage each round and suffer −10% saves; allies inside gain +5% DR and cannot be knocked prone by the zone; difficult terrain spreads 1 tile outward each round and structures inside may crack (DM discretion). After: Exhausted (−1 action, −10% resist for 1 round).",
      },
      mysticInsight: {
        name: "Wound of Creation",
        kind: "passive",
        description:
          "Advantage on checks involving geology, storms, or the Descent's unstable floors. Once per day, sense the nearest structural weak point within 10 tiles.",
      },
      revelationMastery: [
        "Enhanced Shardburst: radius +1 tile",
        "Enhanced Upheaval: allies in burst are immune to prone",
        "Enhanced Seal's Fracture: duration increased to 3 turns",
      ],
      propheticSurge: {
        name: "Cataclysm Prophecy",
        kind: "active",
        description:
          "Once per day, the Shattered Seal weeps through you — cast any Cataclysm Revelation at no charge cost. For 1 round after, the next area effect you create this encounter deals +25% damage and enemies inside must save or fall prone; structures in the zone may crack (DM discretion).",
      },
      finalRevelation: {
        name: "The Unbound Wound",
        kind: "active",
        description:
          "Once per day, tear open a fragment of the Shattered Seal and let its buried violence answer — create a 5-tile cataclysm for 3 rounds, dealing heavy mixed damage each round. You gain immunity to force and bludgeoning for the duration. After: Exhausted for 1 round.",
      },
    }),
  },
  {
    id: "dream",
    name: "Dream",
    theme: "Illusion, waking unreality, and the shaping of perception",
    combatRole:
      "Bend a contested moment toward doubt and misdirection, sheltering allies behind false certainty while foes struggle to trust what they see.",
    reputation:
      "Met with equal fascination and reserve; a Dream oracle's counsel is valued, though few welcome a vision that unsettles an easy answer.",
    rulebookRef: "Mysteries list line 26; Combat Strategy line 155",
    ...draftMysteryRevelations({
      patron: "Veiled Threshold (dreamers who walk between waking prophecy and the Hush beneath the First Song)",
      prophecyTrigger: "When you impose a condition or illusion on an enemy, regain 1 Revelation Charge (once per round)",
      level1: {
        name: "Dreamer's Veil",
        kind: "active",
        description:
          "Passive: +5% resistance to charm and illusion, and advantage on saves vs sleep. Once per long rest, wrap an ally within 3 tiles in a waking dream — they become invisible until they attack or 2 rounds pass; their first attack from concealment this encounter deals +25% psychic damage.",
      },
      tierI: [
        {
          name: "Mirage",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: create an illusory duplicate within 3 tiles for 2 rounds — enemies must save to distinguish real from false when targeting you; on a failed save they strike the mirage instead, and the duplicate may move 1 tile each round without provoking as a free action.",
        },
        {
          name: "Slumber Glimpse",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: one enemy within 4 tiles must save or lose their next action as they stagger through a waking dream; on a failed save they also suffer −10% initiative and cannot take reactions until the dream passes, and the next attack against them gains +2 to hit.",
        },
        {
          name: "False Memory",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: one creature within 3 tiles believes a brief false event occurred (e.g. ally fled, trap sprung, you already cast) for 1 round or until disproven; on a failed save they also suffer −10% initiative and cannot take reactions until the memory is shattered, and the next attack against them gains +2 to hit.",
        },
      ],
      tierII: [
        {
          name: "Shared Dream",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: you and up to 2 allies within 4 tiles enter a lucid dream-state for 1 round — each may reposition up to 2 tiles without provoking and gains concealment until they act; when the dream ends, the first enemy each dreamer strikes deals +25% psychic damage as the Veiled Threshold bleeds waking into nightmare.",
        },
        {
          name: "Nightmare Lash",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: lash one enemy within 5 tiles with waking nightmare — 2d8 + Charisma modifier psychic damage; on failed save, target suffers Dread (−10% hit/saves) for 2 turns and cannot take reactions for 1 round; the Veiled Threshold shows you their dread — if they were already suffering Dread or fear, the lash deals +50% damage and you regain 1 Revelation Charge (once per round).",
        },
        {
          name: "Unreality",
          kind: "passive",
          description:
            "Passive: when an enemy misses you with an attack, 25% chance they strike an illusory echo instead (once per round). Once per short rest, when you would take damage from an attack, you may instead vanish into unreality — the attack misses, you reappear 1 tile away, and the attacker must save or suffer Dread (−10% hit/saves) for 1 turn.",
        },
      ],
      tierIII: {
        name: "Threshold Collapse",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, enemies within 4 tiles suffer −10% hit chance and cannot benefit from flanking — allies within the zone gain +10% saves vs charm and fear; reality frays at the edges: once per round an enemy inside must save or believe an ally is absent (attacks vs that ally have disadvantage until disproven), and your illusions inside the zone require a second save to disbelieve.",
      },
      mysticInsight: {
        name: "Lucid Oracle",
        kind: "passive",
        description:
          "Advantage on saves vs sleep and illusion. Once per day, ask the Veiled Threshold one question — receive a symbolic but truthful vision.",
      },
      revelationMastery: [
        "Enhanced Mirage: creates 2 duplicates",
        "Enhanced Shared Dream: affects 3 allies",
        "Enhanced Threshold Collapse: enemies cannot use reactions inside the zone",
      ],
      propheticSurge: {
        name: "Dream Prophecy",
        kind: "active",
        description:
          "Once per day, the Veiled Threshold parts — cast any Dream Revelation at no charge cost. For 1 round after, all illusions you create require a second save to disbelieve, and enemies who fail their first save against your illusions suffer −10% hit until end of next turn.",
      },
      finalRevelation: {
        name: "The Waking Lie",
        kind: "active",
        description:
          "Once per day, rewrite one battlefield truth for 3 rounds: designate up to 4 tiles as 'dream' — enemies treat allies there as absent; allies gain concealment. Reality reasserts painfully when it ends (enemies save or take psychic damage).",
      },
    }),
  },
  {
    id: "flame",
    name: "Flame",
    theme: "Fire, conviction, and the costly mercy of a flame that can burn or restore",
    combatRole:
      "Carry decisive fire into a contested moment, striking the foe while preserving allies through hard-won, wrathful renewal.",
    reputation:
      "Often met with caution or fear: a Flame oracle may be sought in a crisis, but few mistake their gift for a gentle one.",
    rulebookRef: "Mysteries list line 27; Combat Strategy line 156",
    ...draftMysteryRevelations({
      patron: "Crown of First Flame (the shard-fire that crowned Tyrnathar's founder at the First Cycle)",
      prophecyTrigger: "When you heal an ally or burn an enemy with a Revelation, regain 1 Revelation Charge (once per round)",
      level1: {
        name: "Ember Mantle",
        kind: "active",
        description:
          "Passive: resistance to fire damage and +5% healing received. Once per long rest, ignite your ember mantle for 2 rounds — melee attackers take 1d4 fire damage on hit, you emit warm light in a 2-tile radius, and allies there gain +5% saves vs fear.",
      },
      tierI: [
        {
          name: "Wrathful Brand",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: mark one enemy with burning judgment for 1 round — your next attack against them deals +50% fire damage; if an ally attacks the marked target before the brand fades, they heal 1d6 and the target must save or suffer −10% hit until end of next round as cursed embers cling.",
        },
        {
          name: "Purging Flame",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: touch one ally within 1 tile to end one disease or poison and heal 1d8 + your Charisma modifier; undead touched instead take equal fire damage and must save or suffer −10% hit for 1 round as cursed ash clings.",
        },
        {
          name: "Passion's Rush",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: blaze up to 3 tiles in a line of harmless fire — enemies passed take 1d6 fire damage and must save or suffer −1 movement until your next turn; if you end adjacent to an ally, they gain +10% weapon damage and +5% DR for 1 round as embers cling to their weapons.",
        },
      ],
      tierII: [
        {
          name: "Crown's Burn",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: unleash a 3-tile burst of shard-fire — enemies take 2d6 fire damage and must save or suffer −10% hit until end of next turn; allies in the burst heal half the total damage dealt to enemies (minimum 1d6), and the Crown's embers cling — allies healed this way gain +5% DR vs fire until start of your next turn.",
        },
        {
          name: "Zealot's Renewal",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: one ally within 3 tiles regains HP equal to your Charisma modifier × level tier (minimum 1d8) but takes 1d4 fire backlash — wrathful healing; the Crown's embers cling — they end one minor poison or disease, gain +5% DR vs fire until start of your next turn, and adjacent enemies take 1d4 fire as cursed ash scatters from the renewal.",
        },
        {
          name: "Undying Ember",
          kind: "passive",
          description:
            "Passive: when reduced to 0 HP, erupt in shard-fire — adjacent enemies take 2d6 fire damage and must save or suffer −10% hit for 1 round; you stabilize at 1 HP (once per long rest). Allies within 2 tiles heal 1d6 as embers scatter from the Crown's mercy.",
        },
      ],
      tierIII: {
        name: "First Flame Convergence",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, your fire Revelations deal +25% damage and allies within 4 tiles heal 1d6 when you burn an enemy — you emit warm light and allies are immune to fear; the Crown's memory kindles: once per turn when you heal via wrathful fire, one ally within 4 tiles gains +5% DR until start of your next turn, and Zealot's Renewal backlash is suppressed during the convergence.",
      },
      mysticInsight: {
        name: "Founder's Memory",
        kind: "passive",
        description:
          "Advantage on History checks involving Tyrnathar and the Tenfold Cycles. Once per day, invoke the Crown's memory to reroll a failed save vs fire or fear.",
      },
      revelationMastery: [
        "Enhanced Wrathful Brand: mark lasts 2 rounds",
        "Enhanced Crown's Burn: allies need not be in burst to receive healing",
        "Enhanced First Flame Convergence: no backlash on Zealot's Renewal during effect",
      ],
      propheticSurge: {
        name: "Flame Prophecy",
        kind: "active",
        description:
          "Once per day, the Crown of First Flame kindles through you — cast any Flame Revelation at no charge cost. For 1 round after, your next wrathful heal this encounter deals no backlash and allies within 4 tiles gain +5% DR vs fire; burning enemies you hit take +10% fire damage until end of next turn.",
      },
      finalRevelation: {
        name: "Crown Restored",
        kind: "active",
        description:
          "Once per day, manifest the Crown of First Flame for 3 rounds: +2 fire damage on all attacks, allies within 5 tiles regenerate 1d6 per round, and you may cast Tier I fire Revelations at 0 cost once per round.",
      },
    }),
  },
  {
    id: "life",
    name: "Life",
    theme: "Restoration carried past the first wound: overflow healing, protective blooms, and the stubborn work of keeping life present",
    combatRole:
      "Keep allies standing through the hard center of a fight, turning restored strength into shelter and making a contested position briefly safe enough to endure.",
    reputation:
      "Commonly welcomed where healing is needed, though their gifts are valued most by those who understand that preservation asks as much courage as violence.",
    rulebookRef: "Mysteries list line 28; Combat Strategy line 157",
    ...draftMysteryRevelations({
      patron: "Verdant Resonance (living blooms that answer the First Song's call to mend what the Descent breaks)",
      prophecyTrigger: "When you restore HP to an ally (any source), regain 1 Revelation Charge (once per round)",
      level1: {
        name: "Bloom Ward",
        kind: "active",
        description:
          "Passive: allies within 2 tiles gain +5% healing received, and you gain +5% resistance to necrotic and poison damage. Once per long rest, sprout a protective bloom on an ally within 3 tiles — absorb next 10 + level damage, then wilt and scatter petals granting +5% saves vs fear for 1 round.",
      },
      tierI: [
        {
          name: "Overflowing Light",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: heal one ally within 4 tiles for 2d6 + your Charisma modifier; excess healing above max HP becomes temporary HP (max 10) for 2 rounds, and if any temp HP remains when it fades the ally ends one minor condition.",
        },
        {
          name: "Resonant Seed",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: plant a resonant seed in a 2-tile zone within 4 tiles for 3 rounds — allies starting turn there heal 1d4 and end one minor condition; undead entering or starting turn in the zone take 1d4 radiant and must save or suffer −1 movement until end of turn.",
        },
        {
          name: "Thorned Shelter",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: thorned vines erupt around one ally within 3 tiles — +2 AC, +10% DR, and +5% healing received for 2 rounds; the first melee attacker each round takes 1d4 piercing and cannot move away from the sheltered ally until end of turn.",
        },
      ],
      tierII: [
        {
          name: "Garden of Restoration",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: bloom a 4-tile garden of restoration for 3 rounds — allies inside regenerate 1d6 at start of turn and gain +5% healing received; undead inside take 1d6 radiant at start of turn and must save or suffer −10% hit; entering the garden ends one minor poison or disease on that ally (once each per garden).",
        },
        {
          name: "Life Linked",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: link yourself to one ally within 5 tiles for 2 rounds through the Verdant Resonance — you may transfer up to half damage they take to yourself (after DR); while linked, they gain +5% healing received and +10% DR vs necrotic, and when you heal them through the link they heal an additional 1d4 as blooms echo between you.",
        },
        {
          name: "Verdant Pulse",
          kind: "passive",
          description:
            "Passive: when you heal an ally below 50% HP, they gain +10% resistances and +5% healing received until end of next turn (once per ally per short rest). Once per combat, when an ally within 4 tiles would drop to 0 HP, a verdant pulse blooms — they stabilize at 1 HP and end one minor condition.",
        },
      ],
      tierIII: {
        name: "Song of Mending",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, all allies within 5 tiles regenerate 2d6 at start of turn and cannot be reduced below 1 HP by a single hit (once each) — the Verdant Resonance sings through them; when an ally is stabilized by this song, they end one minor condition and gain +10% healing received until the song ends.",
      },
      mysticInsight: {
        name: "Bloom Oracle",
        kind: "passive",
        description:
          "Advantage on Medicine and Nature. Once per day, diagnose any affliction by touch and learn one countermeasure the Verdant Resonance suggests.",
      },
      revelationMastery: [
        "Enhanced Overflowing Light: temp HP max 20",
        "Enhanced Garden of Restoration: also removes poison/disease on entry",
        "Enhanced Song of Mending: duration 3 turns",
      ],
      propheticSurge: {
        name: "Life Prophecy",
        kind: "active",
        description:
          "Once per day, the Verdant Resonance sings through you — cast any Life Revelation at no charge cost. For 1 round after, all healing you do is maximized and allies you heal gain +10% healing received until end of next turn; undead within 3 tiles of a healed ally take 1d4 radiant.",
      },
      finalRevelation: {
        name: "Eternal Bloom",
        kind: "active",
        description:
          "Once per day, raise a sanctuary bloom for 3 rounds in a 5-tile zone — allies inside are stabilized at 1 HP instead of dying, heal fully over the duration, and gain immunity to necrotic. Ends with petals scattering (brief obscurement).",
      },
    }),
  },
  {
    id: "shadow",
    name: "Shadow",
    theme:
      "Silence, concealment, and the disciplined use of fear against those who mistake darkness for safety",
    combatRole:
      "Claim a quiet angle in the fight, isolate a dangerous foe in dread, and strike from concealment before the enemy can answer.",
    reputation:
      "Regarded with caution: useful where discretion is necessary, but unsettling to those who fear what silence lets a person notice.",
    rulebookRef: "Mysteries list line 29; Combat Strategy line 158",
    ...draftMysteryRevelations({
      patron: "Hush Beneath the Song (silence that gathers where even the Choir's echo fades — see the Marquis of Silence)",
      prophecyTrigger: "When you strike an enemy who cannot see you or is suffering fear, regain 1 Revelation Charge",
      level1: {
        name: "Umbral Cloak",
        kind: "active",
        description:
          "Passive: +2 to Stealth in dim light or darkness and +5% resistance to psychic damage. Once per short rest, shroud yourself in the Hush — become invisible until you attack or 2 rounds pass; your first attack from concealment this encounter deals +25% psychic damage.",
      },
      tierI: [
        {
          name: "Psychic Lash",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: ranged psychic strike within 5 tiles dealing 1d8 + Charisma modifier psychic damage; if the target cannot see you, deal +50% damage, inflict Dread for 1 turn (−10% hit/saves), and they cannot take reactions until end of next turn.",
        },
        {
          name: "Fear's Whisper",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: one enemy within 4 tiles must save or suffer Fear for 2 turns (−10% hit, cannot approach you willingly); on a failed save they also cannot take reactions for 1 round and allies gain +10% crit chance against them while feared.",
        },
        {
          name: "Shadow Step",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: teleport up to 3 tiles to a space in dim light or darkness you can see; you leave no sound and gain +25% damage on your next attack from concealment before end of turn.",
        },
      ],
      tierII: [
        {
          name: "Night's Embrace",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: 3-tile zone of deeper shadow for 3 rounds — allies inside gain concealment and +5% DR; enemies inside suffer −10% hit and −10% saves vs fear; the Hush deepens each round — the first attack you make from inside the zone each round deals +25% psychic damage, and enemies who enter must save or lose reactions until end of turn.",
        },
        {
          name: "Mind Spike",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: drive a psychic spike into one enemy within 5 tiles — 2d8 + Charisma modifier psychic damage; on failed save, target cannot take reactions for 2 turns and suffers Dread (−10% hit/saves); if they were already feared, the spike deals +50% damage and you regain 1 Revelation Charge (once per round).",
        },
        {
          name: "Silent Hunter",
          kind: "passive",
          description:
            "Passive: first attack each combat from concealment deals +25% psychic damage and inflicts Dread (−10% hit/saves) for 1 turn on hit. Once per round after casting a Revelation while concealed, slip through the Hush — move 1 tile without provoking and gain +10% crit chance on your next attack before end of turn.",
        },
      ],
      tierIII: {
        name: "Hush Descends",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, suppress sound in 5 tiles — enemies cannot cast verbal components and suffer Dread; you and allies gain +10% crit from concealment — the Marquis's silence deepens: enemies who start their turn inside must save or lose their action to nameless dread (once per enemy), and your first psychic Revelation each turn from inside the zone costs 1 fewer charge (minimum 0).",
      },
      mysticInsight: {
        name: "Shadow Oracle",
        kind: "passive",
        description:
          "Advantage on Stealth and Insight. Once per day, read the hidden fear in one creature's heart — learn their greatest dread (DM provides truthful answer).",
      },
      revelationMastery: [
        "Enhanced Psychic Lash: range +2 tiles",
        "Enhanced Night's Embrace: allies gain +1 AC inside",
        "Enhanced Hush Descends: duration 3 turns",
      ],
      propheticSurge: {
        name: "Shadow Prophecy",
        kind: "active",
        description:
          "Once per day, the Hush Beneath the Song gathers — cast any Shadow Revelation at no charge cost. For 1 round after, you become invisible until you attack or end of next turn; your first attack from concealment during the effect deals +25% psychic damage and inflicts Dread (−10% hit/saves) on hit.",
      },
      finalRevelation: {
        name: "Marquis's Glimpse",
        kind: "active",
        description:
          "Once per day, invoke the Hush for 3 rounds: you exist partially in silence — untargetable by ranged attacks, all psychic Revelations deal double damage, and enemies within 4 tiles must save each round or lose an action to nameless dread.",
      },
    }),
    draft: false,
    source: "Canon — Director-approved Mystery of Shadow (2026-07-30)",
  },
  {
    id: "stars",
    name: "Stars",
    theme: "Radiant clarity, foresight, and the difficult reading of a path before it closes",
    combatRole:
      "Read a brief advantage in the dark and make it usable: mark the opening, guide an ally's hand, and bring precise radiance where a fight is about to turn.",
    reputation:
      "Sought as advisers and navigators, but met with reserve by those who would rather not hear which choices the sky makes difficult to ignore.",
    rulebookRef: "Mysteries list line 30; Combat Strategy line 159",
    ...draftMysteryRevelations({
      patron: "Celestial Concord (star-choirs that map fate's threads across the Tenfold sky)",
      prophecyTrigger: "When you grant advantage or reroll to an ally through a Revelation, regain 1 Revelation Charge",
      level1: {
        name: "Starlight Mantle",
        kind: "active",
        description:
          "Passive: +1 to ranged attack rolls and Revelation saves at night or under open sky, and +5% resistance to radiant damage. Once per long rest, illuminate 4 tiles with starlight for 2 rounds — reveal invisible and ethereal creatures; allies in the light gain +2 to hit on their next attack.",
      },
      tierI: [
        {
          name: "Guiding Bolt",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: hurl a radiant bolt within 6 tiles — deals 2d6 radiant damage; the target glows with star-mark for 2 rounds and the next ally to attack them gains +2 to hit and +10% crit chance.",
        },
        {
          name: "Fate's Glimpse",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: touch the thread of one ally within 5 tiles — they may reroll their next failed attack, save, or skill check with +2; if the reroll succeeds, you glimpse a second possible outcome and gain advantage on your next Revelation save before end of next turn.",
        },
        {
          name: "Clarity",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: end charm, illusion, or fear on one ally within 4 tiles; grant +10% saves for 2 rounds and reveal the true form of any shapeshifted or invisible creature within 2 tiles of them for 1 round.",
        },
      ],
      tierII: [
        {
          name: "Constellation Mark",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: mark up to 2 enemies within 6 tiles for 3 rounds — allies gain +10% crit and +2 to hit against marked targets; the first crit each round against a mark deals +1d6 radiant and reveals the target through concealment until the mark fades.",
        },
        {
          name: "Radiant Path",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: trace a line of star-fire up to 5 tiles — each enemy in the path takes 2d6 radiant damage and is marked with star-ash for 1 round; allies in the path heal half the total damage dealt (minimum 1d6); the Celestial Concord maps the route — you and one ally may shift 1 tile along the path without provoking before the radiance fades.",
        },
        {
          name: "Omen Reader",
          kind: "passive",
          description:
            "Passive: at initiative, the Celestial Concord reveals which enemy has the highest attack bonus — you and one ally within 5 tiles gain +2 AC vs that enemy's first attack each round. Once per combat, impose −2 on that enemy's first attack and mark them with star-ash — allies gain +10% crit against them until the mark fades.",
        },
      ],
      tierIII: {
        name: "Concord Alignment",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, allies within 5 tiles gain +10% hit, +10% crit, and advantage on saves vs charm and fear as stars align — the Celestial Concord reveals each ally's thread; once per turn you may grant one ally within range a reroll on a failed attack or save, and your Guiding Bolt and Constellation Mark effects extend +1 tile while alignment persists.",
      },
      mysticInsight: {
        name: "Stellar Oracle",
        kind: "passive",
        description:
          "Advantage on Astrology and Navigation. Once per day, read the sky (or a divination focus) for cryptic guidance on a party decision.",
      },
      revelationMastery: [
        "Enhanced Guiding Bolt: also slows target 1 tile on hit",
        "Enhanced Constellation Mark: affects 3 enemies",
        "Enhanced Concord Alignment: duration 3 turns",
      ],
      propheticSurge: {
        name: "Star Prophecy",
        kind: "active",
        description:
          "Once per day, the Celestial Concord aligns — cast any Stars Revelation at no charge cost. For 2 rounds after, allies within 5 tiles gain +2 initiative and +10% crit chance as star-threads map their paths; you may grant one ally within range advantage on their next attack before the alignment fades.",
      },
      finalRevelation: {
        name: "Concord Unveiled",
        kind: "active",
        description:
          "Once per day, call the Celestial Concord for 3 rounds: you see all enemies' intents (no surprise, +2 AC vs their attacks), all Stars Revelations cost 1 fewer charge, and once per round an ally within 6 tiles auto-succeeds one save.",
      },
    }),
  },
  {
    id: "time",
    name: "Time",
    theme:
      "Measured delay, costly reversal, and the care required when one moment is allowed to answer another",
    combatRole:
      "Turn a narrow instant into room for the party to act: steal tempo from an enemy, restore an ally's chance, and make one hard choice matter twice.",
    reputation:
      "Met with respect and reserve; their gifts are welcomed in a crisis, but few are comfortable owing a future moment to the Turning Spiral.",
    rulebookRef: "Mysteries list line 31; Combat Strategy line 160",
    ...draftMysteryRevelations({
      patron: "Turning Spiral (keepers of causality at the edge where the First Song's echo bends back on itself)",
      prophecyTrigger: "When initiative is reordered or an ally rerolls a failed roll through your Revelation, regain 1 Revelation Charge",
      level1: {
        name: "Spiral Echo",
        kind: "active",
        description:
          "Passive: you gain +2 initiative and cannot have your place in initiative order reduced below your current slot. Once per short rest, delay one spell, attack, or condition effect targeting you by 1 round — it resolves at the start of your next turn instead, and you may move 1 tile without provoking when it lands.",
      },
      tierI: [
        {
          name: "Moment's Pause",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: one enemy within 4 tiles must save or lose their next action as time snags around them; on a failed save they also suffer −10% initiative until end of next round and cannot take reactions until the pause resolves.",
        },
        {
          name: "Echo Strike",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: after you hit with a weapon or touch attack, an echo of the strike repeats at half damage on the same target (no extra charge); if the echo reduces the target below half HP, you regain 1 Revelation Charge (once per round).",
        },
        {
          name: "Borrowed Beat",
          charges: 1,
          kind: "active",
          description:
            "Spend 1 charge: one ally within 3 tiles may immediately move up to 2 tiles or cast one Tier I Revelation before the next enemy acts; if they move, they do not provoke until they stop, and you both gain +2 initiative until end of next round (once per combat).",
        },
      ],
      tierII: [
        {
          name: "Rewind Wound",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: touch ally within 1 tile — the Turning Spiral folds causality; undo the last instance of damage they took in the past round (restore HP, remove one condition inflicted by that hit if any); they gain +5% DR and +2 initiative until start of your next turn, and if the undone damage would have dropped them below half HP, you regain 1 Revelation Charge (once per round).",
        },
        {
          name: "Temporal Rift",
          charges: 2,
          kind: "active",
          description:
            "Spend 2 charges: open a 3-tile temporal rift for 2 rounds — enemies inside act last in initiative and suffer −10% hit on their first attack each round; allies inside gain +2 initiative and +10% DR vs effects that would reduce their actions; once per rift, when an ally inside fails a save, you may spend 1 charge to let them reroll with +2.",
        },
        {
          name: "Paradox Skin",
          kind: "passive",
          description:
            "Passive: when hit, 10% chance the attack lands on a temporal echo instead (miss). Resistance to time, aging, and slow effects. Once per short rest, when an ally within 3 tiles fails a save vs a time or aging effect, you may absorb the effect — they reroll with +2 as causality snags around you.",
        },
      ],
      tierIII: {
        name: "Spiral Convergence",
        charges: 3,
        kind: "active",
        description:
          "Spend 3 charges: for 2 turns, once per round rewind one failed ally roll within 5 tiles (attack, save, or skill) as if it never happened — the Turning Spiral folds causality; you gain +1 action per turn (Revelation or move only) and +2 initiative, allies rewound this way gain +10% DR until start of your next turn, and enemies who benefited from the undone roll must save or lose their reaction. After: Exhausted (−1 action, −10% resist for 1 round).",
      },
      mysticInsight: {
        name: "Spiral Oracle",
        kind: "passive",
        description:
          "Advantage on checks involving history, prophecy, or the Tenfold Cycles. Once per day, ask the Turning Spiral whether a specific action will provoke disaster (yes/no with cryptic hint).",
      },
      revelationMastery: [
        "Enhanced Echo Strike: echo deals full damage",
        "Enhanced Rewind Wound: can target self",
        "Enhanced Spiral Convergence: no action restriction on bonus actions",
      ],
      propheticSurge: {
        name: "Time Prophecy",
        kind: "active",
        description:
          "Once per day, the Turning Spiral folds causality — cast any Time Revelation at no charge cost. Initiative resets with you acting first this round; for 1 round after, allies within 5 tiles gain +2 initiative and may reroll one failed save each as the spiral echoes backward.",
      },
      finalRevelation: {
        name: "The Spiral Opens",
        kind: "active",
        description:
          "Once per day, open a causality spiral for 3 rounds: at start of each round, choose one — repeat last round's beneficial Revelation at no cost, or force one enemy to repeat their last turn's worst action against their allies. Allies remember all timelines.",
      },
    }),
  },
];

/** Shared L10+ progression alias — rulebook extract lines 61–74 */
export const ORACLE_HERO_PROGRESSION = {
  tagline: "Curse Boons III–V, Mystic Insight, Final Revelation",
  milestones: ORACLE_SHARED_PROGRESSION.filter((m) => m.level >= 10),
};

/** What the player rulebook actually contains — for gap reporting */
export const ORACLE_RULEBOOK_STATUS = {
  sourceFiles: [
    "rulebook_output.txt (Oracle chapter)",
    "decennium descent player rulebook.docx (verified identical Oracle content)",
    "tools/oracle_rulebook_extract.txt (re-extracted 2026-07-29)",
  ],
  mysteriesNamed: 10,
  mysteriesWithFullTierTree: 10,
  fullTierTree: ["Ancestor", "Shadow"],
  draftTierTree: ["Battle", "Bones", "Cataclysm", "Dream", "Flame", "Life", "Stars", "Time"],
  namedOnly: [],
  exampleBlocks: ["Example Mystery: Ancestor", "Example Curse: Spiral-Touched"],
  docxScan: {
    exampleMysteryCount: 1,
    patronCount: 1,
    namedFinalRevelationCount: 1,
  },
};

/**
 * Playable draft tiers for mysteries named in rulebook without full revelation text.
 * @param {object} config
 * @returns {Pick<OracleMystery, "patron" | "prophecyTrigger" | "level1" | "tierI" | "tierII" | "tierIII" | "mysticInsight" | "revelationMastery" | "propheticSurge" | "finalRevelation" | "draft" | "source">}
 */
function draftMysteryRevelations(config) {
  return {
    patron: config.patron,
    prophecyTrigger: config.prophecyTrigger,
    level1: config.level1,
    tierI: config.tierI,
    tierII: config.tierII,
    tierIII: config.tierIII,
    mysticInsight: config.mysticInsight,
    revelationMastery: config.revelationMastery,
    propheticSurge: config.propheticSurge,
    finalRevelation: config.finalRevelation,
    draft: true,
    source: "Draft — Aethel lore, pending author review",
  };
}

/** @param {string} id */
export function getMysteryById(id) {
  return ORACLE_MYSTERIES.find((m) => m.id === id) ?? null;
}

export default ORACLE_MYSTERIES;
