/**
 * Druid Shapeshifting — canon from rulebook_output.txt / Druid_Shapeshifting_System.docx themes.
 * Defines Aethel's native Shapeshifting system; forms unlock by level and circle.
 */

/** @typedef {object} BeastForm
 * @property {string} id
 * @property {string} name
 * @property {string} role
 * @property {string} levelRange
 * @property {string[]} traits
 * @property {boolean} [draft]
 * @property {string} [source]
 */

/** @type {BeastForm[]} */
export const BASE_DRUID_FORMS = [
  {
    id: "wolf",
    name: "Wolf Form",
    role: "Striker",
    levelRange: "1–10",
    traits: [
      "Pack Pace: +10 ft. movement — wolf-form stride cuts Aethel wild undergrowth and lower-tier trails",
      "Keen Senses: advantage on Perception (hearing/smell) — wolf-form ears and nose read Aethel wild trails and tier-shadow ambush",
      "Bite: 1d8 piercing + DC 11 Str save or prone — wolf-form jaws snap pack discipline onto lower-tier prey and wild trails",
    ],
  },
  {
    id: "bear",
    name: "Bear Form",
    role: "Tank",
    levelRange: "1–10",
    traits: [
      "Thick Hide Buffer: +20 temp HP — bear-form bulk absorbs blows like tier-rooted oak against wild impacts",
      "Rootbark Hide: AC 14 (unless normal AC is higher) — bear-form plate drinks tier-root impacts like storm-worn oak bark",
      "Claw: 2d6 slashing; +1 damage per attack (rage-like) — bear-form talons rake tier-rooted oak and wild bramble like storm fury",
    ],
  },
  {
    id: "hawk",
    name: "Hawk Form",
    role: "Scout",
    levelRange: "1–10",
    traits: [
      "Hawkwing Flight 60 ft. — base hawk form rides Weave updrafts between Aethel descent ledges",
      "Keen Sight: advantage on Perception (sight) — hawk-form eyes track tier-thermals and distant prey across Aethel descent ledges",
      "Dive Attack: 1d4 slashing + advantage from above — hawk-form stoop strikes from Weave updrafts between Aethel descent tiers",
    ],
  },
  {
    id: "boar",
    name: "Boar Form",
    role: "Brawler",
    levelRange: "1–10",
    traits: [
      "Gristle Hide: resistance to slashing — boar-form bristle and gristle turn blade edges along Aethel wild trails",
      "Charge: +10 ft. move toward target → +1d6 damage and push 5 ft.",
    ],
  },
  {
    id: "panther",
    name: "Panther Form",
    role: "Stealth",
    levelRange: "1–10",
    traits: [
      "Shadow Pelt: +4 Stealth — panther-form fur drinks light along tier-shadow and moonlit stone",
      "Night Eyes: 60 ft. darkvision — panther-form sight pierces undercroft gloom without torchlight",
      "Pounce: 20 ft. move + claw 2d4 → DC 12 Str or grappled — panther-form spring pins prey in tier-shadow and moonlit stone",
    ],
  },
];

/** @type {BeastForm[]} */
export const ARCH_DRUID_FORMS = [
  {
    id: "dire-wolf",
    name: "Dire Wolf",
    role: "Pack Striker",
    levelRange: "11–20",
    traits: [
      "Pack Tactics: advantage if ally within 5 ft. — arch dire-wolf flanks read pack-leader signals across Aethel wild tiers",
      "Alpha Bite: 2d6 piercing — arch dire-wolf fangs tear through tier-beast hide and pack-leader prey",
      "Howl (action): 30 ft. Wis save or frightened 1 minute — arch dire-wolf cry echoes pack-leader dread across Aethel wild tiers",
    ],
  },
  {
    id: "earth-warden",
    name: "Earth Warden (Dire Bear)",
    role: "Tank",
    levelRange: "11–20",
    traits: [
      "Stoneheart Buffer: 30 temp HP in form — earth-warden bulk drinks tier-stone impacts like riverbed gravel under siege",
      "Earth Slam (action): 10-ft. radius Dex save or 2d6 bludgeoning + prone",
      "Stone Resistance: resist nonmagical B/P/S — earth-warden hide drinks tier-stone impacts like riverbed gravel",
    ],
  },
  {
    id: "sky-serpent",
    name: "Sky Serpent",
    role: "Skirmisher",
    levelRange: "11–20",
    traits: [
      "Sky Coil Flight 80 ft. — ride Weave updrafts between descent tiers; hover without losing reactions",
      "Lightning Bite: 2d8 lightning — sky-serpent fangs crack Weave storm-blood; wet targets spark once per transformation",
      "Glide Reflexes: +2 Dex saves — sky-serpent coils read Weave updrafts and dodge tier-lightning across Aethel descent air",
    ],
  },
  {
    id: "ironhorn-ram",
    name: "Ironhorn Ram",
    role: "Bruiser",
    levelRange: "11–20",
    traits: [
      "Hornplate Hide: AC 17 (unless higher) — ironhorn ram-form hide rings like tier-forged bronze against wild impacts",
      "Charge: 20 ft. → +3d6 bludgeoning + DC 14 Str or push 10 ft.",
      "Ironhorn Stance: cannot be knocked prone — ram-form legs brace like tier-forged bronze against wild impacts and siege pushes",
    ],
  },
  {
    id: "shadow-lynx",
    name: "Shadow Lynx",
    role: "Assassin",
    levelRange: "11–20",
    traits: [
      "Shadow Blink (reaction): teleport 30 ft. when hit — arch lynx dissolves into tier-shadow; reappears with muffled footfalls",
      "Shadow-Touched Strikes: attacks count as magical — arch lynx claws cut through tier-shadow wards and mundane wild defenses",
      "Shadow Pounce: advantage on first attack after Blink; +2 Stealth while motionless",
    ],
  },
];

/** Hero forms keyed by druid circle id */
export const HERO_FORMS_BY_CIRCLE = {
  land: {
    circle: "Circle of the Land",
    unlockLevel: 10,
    forms: [
      {
        id: "blight-elk",
        name: "Blight Elk",
        traits: [
          "Aura of Decay: 5 ft. — 1d4 poison at start of enemy turn — Land-circle rot breath seeps from tier blight and poisoned undergrowth",
          "Blight Antlers: 2d8 piercing — Land-circle decay rides the charge; poisoned targets save at disadvantage vs Aura of Decay",
          "Toxic Presence: wither plants and taint water — Land-circle rot spreads in your wake; poisoned drinking water imposes disadvantage on next Con save",
        ],
      },
      {
        id: "tanglemaw",
        name: "Tanglemaw",
        traits: [
          "Rootmaw Bite: 2d6 piercing + DC 14 Str or restrained — Land-circle thorn-vines hold prey; restrained foes take Thorny Body damage each turn",
          "Thorny Body: 1d4 piercing to melee attackers — barbed bark sheds on contact; attackers save or bleed 1d4 at start of their next turn",
          "Root Network: sense creatures on ground within 30 ft. — Land-circle root-sense pulses through tier soil and tangled undergrowth",
        ],
      },
    ],
  },
  moon: {
    circle: "Circle of the Moon",
    unlockLevel: 10,
    forms: [
      {
        id: "beastlord",
        name: "Beastlord (Alpha Hybrid)",
        traits: [
          "Chimera Cub: attacks +1d4 fire/cold/lightning each — Moon-beastlord cub fangs crackle with primal tri-element bite",
          "Alpha Dire Wolf: action — Wis save or frightened 15 ft. — Moon-beastlord howl echoes across Aethel wild tiers",
          "Pack Leader: beast allies within 30 ft. gain advantage on attacks — Moon-circle scent and command keep the pack pressing the same marked quarry through Aethel's wild tiers",
        ],
      },
      {
        id: "mooncursed",
        name: "Mooncursed",
        traits: [
          "Lycanthropic Resilience: resist all damage except silver — Moon-circle curse-flesh shrugs off steel and spell across Aethel tiers",
          "Lunar Rage: +1d8 damage under a full moon — Moon-circle blood answers the high moon; silvered foes still resist as normal",
          "Howl of the Wild: grant temporary HP to allies or frighten enemies within 30 ft. — choose the call's sheltering or hunting note when it breaks across the tier",
        ],
      },
    ],
  },
  storm: {
    circle: "Circle of the Storm",
    unlockLevel: 10,
    forms: [
      {
        id: "tempest-raptor",
        name: "Tempest Raptor",
        traits: [
          "Stormtalon Claw: 2d6 lightning — Circle storm-blood arcs on strike; wet targets take +1d4 lightning once per transformation",
          "Stormwing Flight 60 ft. — Circle storm-blood lifts you; advantage on saves vs wind and lightning while airborne",
          "Storm Shroud: 1d6 lightning to melee attackers — storm-blood fur crackles on contact; metal weapons touching you save or drop for 1 round",
        ],
      },
      {
        id: "thunderhorn-stag",
        name: "Thunderhorn Stag",
        traits: [
          "Thunder Charge: 2d8 thunder + Con save or deafened — storm-circle horns crack the air; deafened foes can't hear ally calls",
          "Thunder Step (1/transformation): teleport 30 ft.; the departure or arrival erupts in a 2d8 thunder AoE, carrying the stag between storm-split footholds",
          "Weather Sense: sense storms 24 hours ahead — Storm-circle horns tingle as Voltyros pressure and Weave charge shift across the descent tiers",
        ],
      },
    ],
  },
  thorns: {
    circle: "Circle of Thorns",
    unlockLevel: 10,
    forms: [
      {
        id: "blight-elk-thorns",
        name: "Blight Elk",
        traits: [
          "Aura of Decay: 5 ft. — 1d4 poison at start of enemy turn — Thorns-circle thorn-rot seeps from blighted undergrowth",
          "Antlers: 2d8 piercing; poisoned targets take +1d4 poison on horn hits — thorn-rot follows the horn wound until the victim shakes it free",
          "Thorned Presence: create difficult terrain in 10 ft.; allies ignore its thorns — the circle's briars bend aside for companions but clutch at pursuers",
        ],
      },
      {
        id: "tanglemaw-thorns",
        name: "Tanglemaw",
        traits: [
          "Thornmaw Bite: 2d6 piercing + DC 14 Str or restrained — Thorns-circle briars snag on impact; restrained foes take extra Thorny Body damage each turn",
          "Thorny Body: 1d4 piercing to melee attackers; restrained foes take 1d4/turn — briars bloom on contact across thorn-circle undergrowth",
          "Root Network: sense creatures on the ground within 30 ft.; gain advantage against being knocked prone as thorn-roots anchor through the tier soil",
        ],
      },
    ],
  },
  winterfang: {
    circle: "Circle of Winterfang",
    unlockLevel: 10,
    forms: [
      {
        id: "snow-leopard",
        name: "Snow Leopard",
        traits: [
          "Glacier Claw: 2d6 cold — Winterfang ice shards cling to strikes; slowed targets take +1d4 cold",
          "Snowveil Stealth: +10 Stealth on ice or snow — Winterfang white fur blurs into rime drifts; gain advantage on hide checks after moving through snow",
          "Frost Walk: ignore ice and snow penalties — Winterfang pads grip glacier stone and leave no clumsy slide across rime or slush",
        ],
      },
      {
        id: "frost-wyrmling",
        name: "Frost Wyrmling",
        traits: [
          "Breath Weapon: 30-ft. cone 4d6 cold (1/rest in form) — Winterfang rime breath freezes tier-mist into shard hail",
          "Rime Scales: +2 AC — frost plating hardens on ice or snow; resist nonmagical B/P/S while in cold terrain",
          "Rimeheart Immunity: immune to cold; breath and claw frost ignore resistance once per target each transformation as the wyrmling's rime finds a seam in warding",
        ],
      },
    ],
  },
  rotshaper: {
    circle: "Circle of the Rotshaper",
    unlockLevel: 10,
    forms: [
      {
        id: "carrion-rat-king",
        name: "Carrion Rat King",
        traits: [
          "Poison Bite: 1d8 + 2d6 poison; DC 13 Con or poisoned — Rotshaper plague-fangs drip undercroft venom across lower tiers",
          "Summon Swarm (action): conjure a rat swarm for 1 minute — the Rotshaper carrion-king calls plague-rats from Aethel's undercroft cracks to screen, harry, and occupy prey",
          "Rotshaper Immunity: immune to disease and poison — carrion crown tolerates Aethel blight and venom without the poisoned condition",
        ],
      },
      {
        id: "insect-broodmother",
        name: "Insect Broodmother",
        traits: [
          "Brood Burst: spawn 1d4 insect swarms on transforming — hatchlings pour from decay-tier burrows at your feet, spreading outward before the larger form advances",
          "Brood Chitin: +3 AC — layered carapace sheds once per transformation to negate one crit",
          "Brood Wall Crawl: climb walls and ceilings without checks — Rotshaper brood-limbs grip decay-softened stone across lower tiers",
        ],
      },
    ],
  },
  ashen: {
    circle: "Circle of the Ashen Grove",
    unlockLevel: 10,
    forms: [
      {
        id: "charbear",
        name: "Charbear",
        draft: true,
        traits: [
          "Flame Aura: 5 ft. — 1d6 fire at start of enemy turn — Ashen Grove char-hide smolders; foes in aura save or catch embers as the form advances through ash-choked tier wind",
          "Ember Claw: 2d8 fire — Ashen Grove ash ignites on hit; ignited foes shed 1d4 fire at start of their turn while cinders cling to their retreat",
          "Smoke Cloud (action): 20-ft. heavily obscured sphere — Ashen Grove ash-choked breath blinds foes in smoldering tier smoke and gives allies a moment to reposition",
        ],
      },
      {
        id: "blazewood-stag",
        name: "Blazewood Stag",
        draft: true,
        traits: [
          "Flaming Trail: 1d8 fire on entering trail tile — Ashen Grove embers cling to ash-scorched stone across descent tiers, sketching a dangerous route behind the charge",
          "Burning Charge: +2d6 fire on horn charge — Ashen Grove embers trail the antlers through smoke and ash, carrying the stag's momentum into the first impact",
          "Conflagration (1/long rest): 10 ft. 6d6 fire Dex save — Ashen Grove antler-burst ignites ash-choked undergrowth before the blaze gutters back to drifting cinders",
        ],
      },
    ],
  },
};

/** @type {{ id: string; label: string }[]} */
export const DRUID_CIRCLES = [
  { id: "land", label: "Circle of the Land" },
  { id: "moon", label: "Circle of the Moon" },
  { id: "storm", label: "Circle of the Storm" },
  { id: "thorns", label: "Circle of Thorns" },
  { id: "winterfang", label: "Circle of Winterfang" },
  { id: "rotshaper", label: "Circle of the Rotshaper" },
  { id: "ashen", label: "Circle of the Ashen Grove" },
];

export const SHAPESHIFT_RULES = {
  activation: "Bonus action to assume beast form",
  duration: "10 minutes per use; revert early as bonus action",
  usesByLevel: [
    { level: 1, uses: 2 },
    { level: 4, uses: 3 },
    { level: 7, uses: 4 },
    { level: 10, uses: 5 },
    { level: 13, uses: 6 },
    { level: 16, uses: 7 },
    { level: 19, uses: 8 },
    { level: 20, uses: "Unlimited (Archdruid)" },
  ],
  limitations: [
    "Cannot cast spells unless Hero Class or Beast Spells (18+) allows",
    "Speech limited (preserved in arch/hero forms)",
    "Retain mental scores (Int, Wis, Cha)",
    "Gain physical traits of chosen form",
  ],
  unlocks: [
    { level: 1, forms: "Base Druid Forms" },
    { level: 10, forms: "Hero Druid Forms (circle-specific)" },
    { level: 11, forms: "Arch Druid Forms" },
  ],
};

/** Map circle id → arch path name in class-paths.js */
export const DRUID_CIRCLE_ARCH_PATH_NAMES = {
  land: "Circle of the Land",
  moon: "Circle of the Moon",
  storm: "Circle of the Storm",
  thorns: "Circle of Thorns",
  winterfang: "Circle of Winterfang",
  rotshaper: "Circle of the Rotshaper",
  ashen: "Circle of the Ashen Grove",
};

export function getHeroFormsForCircle(circleId) {
  return HERO_FORMS_BY_CIRCLE[circleId] ?? null;
}

/** Whether this circle's hero-form content includes an author-review draft. */
export function hasDraftHeroFormsForCircle(circleId) {
  return Boolean(getHeroFormsForCircle(circleId)?.forms.some((form) => form.draft));
}

/** Filter arch/hero path blocks to the selected circle for Paths tab display. */
export function druidPathBlocksForCircle(circleId, archPaths = [], heroPaths = []) {
  const archName = DRUID_CIRCLE_ARCH_PATH_NAMES[circleId];
  const circleArch = archName ? archPaths.filter((p) => p.name === archName) : [];
  const heroData = getHeroFormsForCircle(circleId);
  const circleHero = heroData
    ? [
        {
          name: `${heroData.circle} — Hero Forms`,
          tagline: `Unlock L${heroData.unlockLevel}+ · ${heroData.forms.map((f) => f.name).join(", ")}`,
          draft: heroData.forms.some((f) => f.draft),
          passives: heroData.forms.flatMap((f) => f.traits),
          actives: ["Bonus-action shapeshift into circle hero form"],
        },
      ]
    : [];
  return {
    archPaths: circleArch.length ? circleArch : archPaths,
    heroPaths: circleHero.length ? circleHero : heroPaths,
  };
}

export function formsAvailableAtLevel(level) {
  const forms = [...BASE_DRUID_FORMS];
  if (level >= 11) forms.push(...ARCH_DRUID_FORMS);
  return forms;
}

/** Shapeshifting uses per long rest by druid level (SHAPESHIFT_RULES.usesByLevel). */
export function shapeshiftUsesAtLevel(level) {
  const lvl = Math.max(1, Math.min(20, Math.round(Number(level) || 1)));
  let uses = 2;
  for (const row of SHAPESHIFT_RULES.usesByLevel) {
    if (lvl >= row.level) {
      uses = row.uses === "Unlimited (Archdruid)" ? 99 : Number(row.uses) || uses;
    }
  }
  return uses;
}

/**
 * Draft CR cap for Shapeshifting forms by level.
 * L11+ arch forms: tier floor −1 (min CR 2) per class-draft-levels.
 */
export function wildShapeCrCap(level) {
  const lvl = Math.max(1, Math.min(20, Math.round(Number(level) || 1)));
  if (lvl >= 19) return 5;
  if (lvl >= 16) return 4;
  if (lvl >= 13) return 3;
  if (lvl >= 10) return 2;
  if (lvl >= 7) return 1;
  if (lvl >= 4) return 0.5;
  return 0.25;
}

/** Default Shapeshifting duration per use (SHAPESHIFT_RULES.duration). */
export function wildShapeDurationMinutes() {
  return 10;
}

/**
 * Draft RP regain for Primal Recovery (L13+ class-draft-levels):
 * regain RP equal to half druid level, rounded up.
 */
export function primalRecoveryRpGain(level) {
  return Math.ceil(Math.max(1, Number(level) || 1) / 2);
}

/** True when druid level qualifies for Primal Recovery draft milestone. */
export function hasPrimalRecovery(level) {
  return Math.max(1, Math.round(Number(level) || 1)) >= 13;
}

/** True when druid level qualifies for Arch form attunement (L15 draft). */
export function hasArchFormAttunement(level) {
  return Math.max(1, Math.round(Number(level) || 1)) >= 15;
}

/** Max attuned arch forms per L15 draft milestone. */
export const ARCH_ATTUNEMENT_MAX = 2;

/**
 * Whether shifting from one attuned arch form to another skips a Shapeshifting use (once/encounter).
 * @param {string} fromFormId
 * @param {string} toFormId
 * @param {string[]} attunedIds
 */
export function isFreeArchAttunementSwap(fromFormId, toFormId, attunedIds) {
  if (!fromFormId || !toFormId || fromFormId === toFormId) return false;
  const attuned = new Set(Array.isArray(attunedIds) ? attunedIds : []);
  return attuned.has(fromFormId) && attuned.has(toFormId);
}

/** Forms a druid combatant may pick at table — base, circle hero (L10+), arch (L11+). */
export function shapeshiftFormsForDruid(level, circleId) {
  const lvl = Math.max(1, Math.min(20, Math.round(Number(level) || 1)));
  const forms = BASE_DRUID_FORMS.map((f) => ({ id: f.id, name: f.name, tier: "base", draft: false }));
  if (lvl >= 10 && circleId) {
    const hero = getHeroFormsForCircle(circleId);
    if (hero?.forms) {
      for (const f of hero.forms) {
        forms.push({ id: f.id, name: f.name, tier: "hero", draft: Boolean(f.draft) });
      }
    }
  }
  if (lvl >= 11) {
    for (const f of ARCH_DRUID_FORMS) {
      forms.push({ id: f.id, name: f.name, tier: "arch", draft: false });
    }
  }
  return forms;
}

const druidShapeshifting = {
  BASE_DRUID_FORMS,
  ARCH_DRUID_FORMS,
  HERO_FORMS_BY_CIRCLE,
  DRUID_CIRCLES,
  SHAPESHIFT_RULES,
};

export default druidShapeshifting;
