/**

 * Resonance (Hybrid-B canon) economy helpers.

 *

 * Canon: docs/mechanics/RESONANCE_CANON.md (player-facing summary)

 * Ruling: docs/mechanics/RESONANCE_MODELS.md §6 (DIRECTOR CHOICE: Hybrid-B, approved canon)

 * Reputation hooks: docs/mechanics/REPUTATION.md, src/data/reputation.js

 *

 * Oracle is excluded — Oracle uses Revelation Charges (`oracle-mysteries.js`

 * / `oracle-curses.js`), not Resonance Points. Never call these helpers for

 * Oracle characters (`isSpellcasterClass()` in `spell-utils.js` already

 * excludes Oracle).

 */



/** @typedef {{ maxRp: number; draft: boolean; source: "canon" | "draft" | "none"; tier: string; multiclass?: { primary: string; primaryLevel: number; primaryPool: number; secondary: string; secondaryLevel: number; secondaryBonus: number; repModifier?: number } }} MaxRpResult */

/** @typedef {Record<string, number>} ReputationScores */



/**

 * Rulebook-complete L1–20 Resonance Point pools (Player Rulebook Resonance chapter).

 * Index 0 is unused so `table[level]` reads naturally for levels 1–20.

 */

export const CANON_POOL_TABLES = {

  Wizard: [null, 4, 6, 10, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 80],

  Mage: [null, 3, 5, 8, 10, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56, 60],

  Cleric: [null, 3, 4, 7, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 58],

  Druid: [null, 3, 4, 7, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 58],

};



/**

 * Draft caster tiers for the remaining Weave-casting classes. Multipliers are

 * applied to the Cleric reference curve and rounded — **author review pending**.

 *

 * - `half`   — Paladin/Ranger (half-Weave casters).

 * - `hybrid` — Bard/Shaman/Mirrorsage/Crimson Agent (class-specific resource + smaller RP pool).

 * - `minor`  — Dragoon/Monk/Thief/Tinker (light Weave dabbling).

 */

export const DRAFT_CASTER_TIERS = {

  Paladin: "half",

  Ranger: "half",

  Bard: "hybrid",

  Shaman: "hybrid",

  Mirrorsage: "hybrid",

  "Crimson Agent": "hybrid",

  Dragoon: "minor",

  Monk: "minor",

  Thief: "minor",

  Tinker: "minor",

};



const DRAFT_TIER_MULTIPLIERS = {

  half: 0.65,

  hybrid: 0.5,

  minor: 0.35,

};



/** Build L1–20 draft pool table from Cleric reference × tier multiplier. */

function buildDraftPoolTable(multiplier) {

  const ref = CANON_POOL_TABLES.Cleric;

  const table = [null];

  for (let lvl = 1; lvl <= 20; lvl++) {

    table.push(Math.max(1, Math.round(ref[lvl] * multiplier)));

  }

  return table;

}



/**

 * Full L1–20 draft pool tables for all non-canon Weave casters.

 * Derived from Cleric curve × tier multiplier — flagged draft in UI.

 */

export const DRAFT_POOL_TABLES = Object.fromEntries(

  Object.entries(DRAFT_CASTER_TIERS).map(([className, tier]) => [

    className,

    buildDraftPoolTable(DRAFT_TIER_MULTIPLIERS[tier]),

  ])

);



/** Combined lookup: canon + draft tables for every Weave-casting class. */

export const ALL_POOL_TABLES = { ...CANON_POOL_TABLES, ...DRAFT_POOL_TABLES };



/** Classes with zero Weave RP pool (own resource track, or non-caster). */

export const NO_POOL_CLASSES = new Set(["Oracle", "Soldier", "Warrior"]);



/** All 14 Weave-casting classes among the 17-class roster (excludes Oracle/Soldier/Warrior). */

export const WEAVE_CASTER_CLASSES = [

  ...Object.keys(CANON_POOL_TABLES),

  ...Object.keys(DRAFT_POOL_TABLES),

].sort();



/** Four Resonance reputation tracks from Ch9 / reputation.js. */

export const RESONANCE_TRACK_IDS = {

  academic: "academic-factions",

  religious: "religious-orders",

  arcane: "arcane-guilds",

  nature: "nature-circles",

};



/**

 * Primary Resonance track per class for spell-cost ±1 modifier (draft mapping).

 * @type {Record<string, string>}

 */

export const CLASS_SPELL_REP_TRACK = {

  Wizard: RESONANCE_TRACK_IDS.arcane,

  Mage: RESONANCE_TRACK_IDS.arcane,

  Tinker: RESONANCE_TRACK_IDS.arcane,

  Mirrorsage: RESONANCE_TRACK_IDS.academic,

  Cleric: RESONANCE_TRACK_IDS.religious,

  Paladin: RESONANCE_TRACK_IDS.religious,

  Shaman: RESONANCE_TRACK_IDS.religious,

  Monk: RESONANCE_TRACK_IDS.religious,

  Dragoon: RESONANCE_TRACK_IDS.religious,

  Druid: RESONANCE_TRACK_IDS.nature,

  Ranger: RESONANCE_TRACK_IDS.nature,

  Bard: RESONANCE_TRACK_IDS.academic,

  "Crimson Agent": RESONANCE_TRACK_IDS.arcane,

  Thief: RESONANCE_TRACK_IDS.academic,

};



function clampLevel(level) {

  const n = Math.round(Number(level) || 1);

  return Math.max(1, Math.min(20, n));

}



/** Caster-tier rank for multiclass primary pick (RESONANCE_CANON.md §7). */

function casterTierRank(className) {

  if (CANON_POOL_TABLES[className]) return 4;

  const tier = DRAFT_CASTER_TIERS[className];

  if (tier === "half") return 3;

  if (tier === "hybrid") return 2;

  if (tier === "minor") return 1;

  return 0;

}



function resolveRepModifier(repModifierOrScores) {

  return typeof repModifierOrScores === "object" && repModifierOrScores !== null

    ? maxRpRepModifier(repModifierOrScores)

    : Math.round(Number(repModifierOrScores) || 0);

}



function singleClassPoolBase(className, level) {

  const lvl = clampLevel(level);

  if (!className || NO_POOL_CLASSES.has(className)) return 0;

  const table = ALL_POOL_TABLES[className];

  if (table) return table[lvl];

  return Math.max(1, Math.round(CANON_POOL_TABLES.Cleric[lvl] * DRAFT_TIER_MULTIPLIERS.minor));

}



function sortWeaveClassesForMulticlass(entries) {

  return [...entries].sort((a, b) => {

    const rankDiff = casterTierRank(b.className) - casterTierRank(a.className);

    if (rankDiff !== 0) return rankDiff;

    const levelDiff = b.level - a.level;

    if (levelDiff !== 0) return levelDiff;

    return singleClassPoolBase(b.className, b.level) - singleClassPoolBase(a.className, a.level);

  });

}



/**

 * Parse multiclass class levels from explicit opts or a character save.

 * Supports `secondaryClass` + `secondaryLevel`, or `classLevels: { Wizard: 10, Cleric: 6 }`.

 * @param {Record<string, unknown> | null | undefined} input

 * @returns {{ className: string; level: number }[] | null}

 */

export function parseMulticlassLevels(input) {

  if (!input || typeof input !== "object") return null;



  if (input.classLevels && typeof input.classLevels === "object") {

    const entries = Object.entries(input.classLevels)

      .map(([className, level]) => ({ className, level: clampLevel(level) }))

      .filter((e) => e.level > 0);

    return entries.length > 1 ? entries : null;

  }



  const primaryClass = input.primaryClass || input.class || input.className;

  const primaryLevel = input.primaryLevel ?? input.level;

  const { secondaryClass, secondaryLevel } = input;



  if (secondaryClass && secondaryLevel != null) {

    return [

      { className: String(primaryClass || ""), level: clampLevel(primaryLevel) },

      { className: String(secondaryClass), level: clampLevel(secondaryLevel) },

    ].filter((e) => e.className);

  }



  return null;

}



/**

 * Multiclass max RP — RESONANCE_CANON.md §7: approved highest-tier Weave pool + 25% secondary (ceil).

 * @param {{ className: string; level: number }[]} classEntries

 * @param {number | ReputationScores} [repModifierOrScores]

 * @returns {MaxRpResult}

 */

export function mergeMulticlassMaxRp(classEntries, repModifierOrScores = 0) {

  const weave = (classEntries || [])

    .filter((e) => e.className && !NO_POOL_CLASSES.has(e.className) && e.level > 0);



  if (weave.length === 0) {

    return { maxRp: 0, draft: false, source: "none", tier: "none" };

  }

  if (weave.length === 1) {

    return singleClassMaxRp(weave[0].className, weave[0].level, repModifierOrScores);

  }



  const sorted = sortWeaveClassesForMulticlass(weave);

  const primary = sorted[0];

  const secondary = sorted[1];

  const primaryResult = singleClassMaxRp(primary.className, primary.level, 0);

  const secondaryResult = singleClassMaxRp(secondary.className, secondary.level, 0);

  const secondaryBonus = Math.ceil(secondaryResult.maxRp * 0.25);

  const repMod = resolveRepModifier(repModifierOrScores);



  return {

    maxRp: Math.max(0, primaryResult.maxRp + secondaryBonus + repMod),

    draft: primaryResult.draft || secondaryResult.draft,

    source: primaryResult.draft || secondaryResult.draft ? "draft" : "canon",

    tier: "multiclass",

    multiclass: {

      primary: primary.className,

      primaryLevel: primary.level,

      primaryPool: primaryResult.maxRp,

      secondary: secondary.className,

      secondaryLevel: secondary.level,

      secondaryBonus,

      repModifier: repMod,

    },

  };

}



/**

 * Player-facing multiclass RP breakdown lines (RESONANCE_CANON.md §7 — approved formula).

 * @param {MaxRpResult & { multiclass?: { primary: string; primaryLevel: number; primaryPool: number; secondary: string; secondaryLevel: number; secondaryBonus: number; repModifier?: number } }} result

 * @returns {{ lines: string[]; summary: string } | null}

 */

export function multiclassRpBreakdown(result) {

  const mc = result?.multiclass;

  if (!mc) return null;



  const lines = [

    `${mc.primary} L${mc.primaryLevel}: ${mc.primaryPool} RP (primary pool)`,

    `+ ⌈25% × ${mc.secondary} L${mc.secondaryLevel}⌉ = +${mc.secondaryBonus} RP`,

  ];

  const repMod = Number(mc.repModifier) || 0;

  if (repMod !== 0) {

    lines.push(`Arcane Guilds rep: ${repMod >= 0 ? "+" : ""}${repMod} RP`);

  }

  lines.push(`= ${result.maxRp} RP max (approved multiclass formula)`);



  return { lines, summary: lines.join(" · ") };

}



/** Tooltip / aria text for max RP — includes multiclass breakdown when applicable. */

export function formatMaxRpTooltip(result, classLabel = "") {

  if (!result || result.maxRp <= 0) return "No Weave Resonance pool";

  const breakdown = multiclassRpBreakdown(result);

  if (breakdown) return breakdown.summary;

  const draftNote = result.draft ? " — draft RP pool (playtest estimate)" : "";

  return classLabel

    ? `Resonance max for ${classLabel}${draftNote}`

    : `Resonance max${draftNote}: ${result.maxRp} RP`;

}



function singleClassMaxRp(className, level, repModifierOrScores = 0) {

  const lvl = clampLevel(level);

  if (!className || NO_POOL_CLASSES.has(className)) {

    return { maxRp: 0, draft: false, source: "none", tier: "none" };

  }



  const repMod = resolveRepModifier(repModifierOrScores);

  const table = ALL_POOL_TABLES[className];

  if (table) {

    const base = table[lvl];

    const isCanon = Boolean(CANON_POOL_TABLES[className]);

    const tier = isCanon ? "full" : DRAFT_CASTER_TIERS[className] || "minor";

    return {

      maxRp: Math.max(0, base + repMod),

      draft: !isCanon,

      source: isCanon ? "canon" : "draft",

      tier,

    };

  }



  const fallbackBase = Math.max(1, Math.round(CANON_POOL_TABLES.Cleric[lvl] * DRAFT_TIER_MULTIPLIERS.minor));

  return { maxRp: Math.max(0, fallbackBase + repMod), draft: true, source: "draft", tier: "minor" };

}



function trackScore(reputation, trackId) {

  if (!reputation || !trackId) return 0;

  return Number(reputation[trackId]) || 0;

}



/**

 * Arcane Guilds standing → ± max RP (rulebook: ±2 at honored/hated extremes).

 * @param {ReputationScores | undefined} reputation

 * @returns {number}

 */

export function maxRpRepModifier(reputation) {

  const score = trackScore(reputation, RESONANCE_TRACK_IDS.arcane);

  if (score >= 2) return 2;

  if (score <= -2) return -2;

  if (score >= 1) return 1;

  if (score <= -1) return -1;

  return 0;

}



/**

 * Class-relevant Resonance track → spell cost ±1 (liked/honored −1, disliked/hated +1).

 * @param {string} className

 * @param {ReputationScores | undefined} reputation

 * @returns {number}

 */

export function spellCostRepModifier(className, reputation) {

  const trackId = CLASS_SPELL_REP_TRACK[className];

  if (!trackId) return 0;

  const score = trackScore(reputation, trackId);

  if (score >= 1) return -1;

  if (score <= -1) return 1;

  return 0;

}



/**

 * Nature Circles standing → short-rest retune bonus (draft: ±1 RP).

 * @param {ReputationScores | undefined} reputation

 * @returns {number}

 */

export function retuneRepBonus(reputation) {

  const score = trackScore(reputation, RESONANCE_TRACK_IDS.nature);

  if (score >= 1) return 1;

  if (score <= -1) return -1;

  return 0;

}



/**

 * Resolve alignment → school affinity/opposition flags for spellCost().

 * @param {string | undefined} alignment e.g. "Lawful Good", "Neutral Evil"

 * @param {string | undefined} school Spell school name

 * @returns {{ affinity: boolean; opposition: boolean }}

 */

export function schoolAffinityMods(alignment, school) {

  if (!alignment || !school) return { affinity: false, opposition: false };

  const axis = alignment.split(/\s+/).pop() || alignment;

  const entry = ALIGNMENT_SCHOOL_AFFINITY[axis];

  if (!entry) return { affinity: false, opposition: false };

  return {

    affinity: entry.affinity.includes(school),

    opposition: entry.opposition.includes(school),

  };

}



/**

 * Resolve a class/level to a Resonance Point pool size.

 * @param {string} className

 * @param {number} level

 * @param {number | ReputationScores} [repModifierOrScores] Net max-RP modifier, or reputation object (Arcane Guilds applied automatically).

 * @returns {MaxRpResult}

 */

export function defaultMaxRp(className, level, repModifierOrScores = 0, multiclassInput = undefined) {

  const parsed = parseMulticlassLevels(

    multiclassInput !== undefined

      ? { primaryClass: className, primaryLevel: level, ...(multiclassInput || {}) }

      : null

  );

  if (parsed && parsed.length > 1) {

    return mergeMulticlassMaxRp(parsed, repModifierOrScores);

  }

  return singleClassMaxRp(className, level, repModifierOrScores);

}



/** Convenience wrapper: class + level + reputation scores → max RP result. */

export function resolveMaxRp(className, level, reputation, characterOrMulticlass) {

  return defaultMaxRp(className, level, reputation || {}, characterOrMulticlass);

}



/** True for the 4 classes with a rulebook-complete L1–20 pool table. */

export function isCanonPoolClass(className) {

  return Boolean(className && CANON_POOL_TABLES[className]);

}



/**

 * Base Resonance cost formula (Player Rulebook Resonance chapter, Model B spine):

 * `spell level × 2`, modified by school affinity/opposition, faction

 * reputation, and class specialization. Cantrips always cost 0.

 *

 * @param {number} level Spell level (0 = cantrip).

 * @param {{ affinity?: boolean; opposition?: boolean; reputationModifier?: number; specialization?: number }} [mods]

 * @returns {number} Final RP cost, floored at 0.

 */

export function spellCost(level, mods = {}) {

  const lvl = Math.max(0, Number(level) || 0);

  if (lvl === 0) return 0;



  const { affinity = false, opposition = false, reputationModifier = 0, specialization = 0 } = mods;

  let cost = lvl * 2;

  if (affinity) cost -= 1;

  if (opposition) cost += 1;

  cost += Number(reputationModifier) || 0;

  cost -= Number(specialization) || 0;

  return Math.max(0, Math.round(cost));

}



/**

 * Full spell cost from spell metadata + character context.

 * @param {{ level?: number; school?: string }} spell

 * @param {{ className?: string; alignment?: string; reputation?: ReputationScores; specialization?: number }} ctx

 * @returns {number}

 */

export function computeSpellCost(spell, ctx = {}) {

  const { affinity, opposition } = schoolAffinityMods(ctx.alignment, spell?.school);

  return spellCost(spell?.level ?? 0, {

    affinity,

    opposition,

    reputationModifier: spellCostRepModifier(ctx.className || "", ctx.reputation),

    specialization: ctx.specialization ?? 0,

  });

}



/**

 * Short rest "retune" — ≈¼ max pool (+ casting-attribute modifier + Nature Circles bonus).

 * @param {number} maxRp

 * @param {number} [castingMod]

 * @param {ReputationScores | undefined} [reputation]

 */

export function retuneAmount(maxRp, castingMod = 0, reputation) {

  const pool = Math.max(0, Number(maxRp) || 0);

  const natureBonus = reputation ? retuneRepBonus(reputation) : 0;

  return Math.max(0, Math.round(pool / 4) + (Number(castingMod) || 0) + natureBonus);

}



/** Long rest "full harmony" — pool returns to max. */

export function fullRestore(maxRp) {

  return Math.max(0, Number(maxRp) || 0);

}



/** @deprecated Use retuneAmount */

export function shortRestRecovery(maxRp, castingMod = 0) {

  return retuneAmount(maxRp, castingMod);

}



/** @deprecated Use fullRestore */

export function longRestRecovery(maxRp) {

  return fullRestore(maxRp);

}



/** Optional 10-minute meditation, once/day — casting-attribute modifier only. */

export function meditationRecovery(castingMod = 0) {

  return Math.max(0, Number(castingMod) || 0);

}



/** Burnout risk line — below 25% of max RP (Player Rulebook Resonance chapter). */

export function burnoutThreshold(maxRp) {

  return Math.ceil(Math.max(0, Number(maxRp) || 0) * 0.25);

}



export function isBurnoutRisk(currentRp, maxRp) {

  return Number(currentRp) < burnoutThreshold(maxRp);

}



/**

 * Post-cast Overcast Burnout hint (Phase 2 stub).

 * When RP drops below 25% max after a cast, surface Mage L17-style concentration check text.

 * @returns {null | { dc: number; summary: string; lowPool: boolean; highTierOvercast: boolean }}

 */

export function overcastBurnoutHintAfterCast(currentRp, maxRp, spellTier = 0, casterLevel = 1, casterClass = "") {

  const tier = Math.max(0, Math.round(Number(spellTier) || 0));

  const max = Math.max(0, Number(maxRp) || 0);

  const lowPool = isBurnoutRisk(currentRp, max);

  const weaveCaster = casterClass === "Mage" || casterClass === "Wizard";

  const highTierOvercast = weaveCaster && Number(casterLevel) >= 17 && tier >= 8;

  if (!lowPool && !highTierOvercast) return null;

  const dc = 15 + (tier > 0 ? tier : 8);

  const parts = [];

  if (lowPool) {

    parts.push(`Post-cast RP below 25% max (${currentRp}/${max})`);

  }

  if (highTierOvercast || (lowPool && tier >= 8)) {

    parts.push(`Concentration save DC ${dc} or Burnout`);

  } else if (lowPool) {

    parts.push(`${BURNOUT_EFFECT_STUB.summary}`);

  }

  return {

    dc,

    lowPool,

    highTierOvercast,

    summary: `${parts.join(" — ")} (Mage L17 draft)`,

  };

}



/** Draft player-facing Burnout effects — not auto-applied to rolls (Phase 2). */

export const BURNOUT_EFFECT_STUB = {

  label: "Burnout (GM fiat)",

  summary: "GM fiat until final table — disadvantage on Weave checks; −1 action this turn (suggested)",

  disadvantageNote: "Disadvantage on Weave-related ability checks and spell attacks",

  actionPenalty: "−1 action this turn (suggested)",

};



/** Sum RP cost for selected overcast option ids. */

export function overcastRpCost(overcastIds) {

  if (!Array.isArray(overcastIds) || !overcastIds.length) return 0;

  const byId = Object.fromEntries(OVERCAST_OPTIONS.map((o) => [o.id, o.rpCost]));

  return overcastIds.reduce((sum, id) => sum + (byId[id] || 0), 0);

}



/**

 * Total RP for a cast: base spell cost + overcast surcharges.

 * @param {number} baseCost From spellCost/computeSpellCost

 * @param {string[]} [overcastIds]

 */

export function totalCastCost(baseCost, overcastIds = []) {

  return Math.max(0, Math.round(Number(baseCost) || 0) + overcastRpCost(overcastIds));

}



/** Lookup overcast option by id. */

export function getOvercastOption(id) {

  return OVERCAST_OPTIONS.find((o) => o.id === id) || null;

}



/**

 * Overcast menu (Player Rulebook Resonance chapter). Session overcast picker is a

 * Phase 2 stub — applies cost modifiers + burnout flag only.

 */

export const OVERCAST_OPTIONS = [

  { id: "empowered", label: "Empowered", rpCost: 2, effect: "+50% damage or healing" },

  { id: "extended", label: "Extended", rpCost: 1, effect: "2× duration" },

  { id: "widened", label: "Widened", rpCost: 3, effect: "2× area of effect" },

  { id: "heightened", label: "Heightened", rpCost: 4, effect: "+1 effective spell level" },

  { id: "quickened", label: "Quickened", rpCost: 3, effect: "Cast as a bonus action" },

  { id: "subtle", label: "Subtle", rpCost: 1, effect: "No verbal/somatic components" },

  { id: "distant", label: "Distant", rpCost: 1, effect: "2× range" },

  { id: "twinned", label: "Twinned", rpCost: 3, effect: "Target a second creature" },

];



/** Nine ethos alignments for Builder + Session picker (affinity uses moral axis only). */
export const PLAYER_ALIGNMENTS = [
  "Lawful Good",
  "Neutral Good",
  "Chaotic Good",
  "Lawful Neutral",
  "True Neutral",
  "Chaotic Neutral",
  "Lawful Evil",
  "Neutral Evil",
  "Chaotic Evil",
];

/** Alignment school affinity/opposition (Player Rulebook Resonance chapter). */

export const ALIGNMENT_SCHOOL_AFFINITY = {

  Good: { affinity: ["Abjuration", "Divination", "Transmutation"], opposition: ["Necromancy", "Enchantment"] },

  Neutral: { affinity: ["Conjuration", "Illusion", "Universal"], opposition: ["Evocation", "Necromancy"] },

  Evil: { affinity: ["Necromancy", "Enchantment", "Evocation"], opposition: ["Abjuration", "Divination"] },

};


