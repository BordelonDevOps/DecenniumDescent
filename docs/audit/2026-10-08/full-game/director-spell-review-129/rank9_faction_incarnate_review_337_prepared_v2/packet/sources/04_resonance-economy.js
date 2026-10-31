/**

 * Resonance + Dissonance canon economy helpers.

 *

 * Canon: docs/mechanics/RESONANCE_CANON.md (player-facing summary)

 * Ruling: docs/mechanics/RESONANCE_CANON.md — RP powers casting; Dissonance prevents repetition/overcast spam

 * Reputation hooks: docs/mechanics/REPUTATION.md, src/data/reputation.js

 *

 * Oracle is excluded — Oracle uses Revelation Charges (`oracle-mysteries.js`

 * / `oracle-curses.js`), not Resonance Points. Never call these helpers for

 * Oracle characters (`isSpellcasterClass()` in `spell-utils.js` already

 * excludes Oracle).

 */



/** @typedef {{ maxRp: number; draft: boolean; source: "canon" | "draft" | "none"; tier: string; multiclass?: { primary: string; primaryLevel: number; primaryPool: number; secondary: string; secondaryLevel: number; secondaryBonus: number } }} MaxRpResult */

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

 * Canon Weave-capacity tiers for the remaining Weave-casting classes. Multipliers are
 * applied to the Cleric reference curve and rounded. These tiers define capacity only;
 * each class still casts through its protected core mechanic and learning cadence.

 *

 * - `half`   — Paladin/Ranger (half-Weave casters).

 * - `hybrid` — Bard/Shaman/Mirrorsage/Crimson Agent (class-specific resource + smaller RP pool).

 * - `minor`  — Dragoon/Monk/Thief/Tinker (light Weave dabbling).

 */

export const CLASS_WEAVE_TIERS = {

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



const WEAVE_TIER_MULTIPLIERS = {

  half: 0.65,

  hybrid: 0.5,

  minor: 0.35,

};



/** Build L1–20 tier pool table from Cleric reference × tier multiplier. */

function buildTierPoolTable(multiplier) {

  const ref = CANON_POOL_TABLES.Cleric;

  const table = [null];

  for (let lvl = 1; lvl <= 20; lvl++) {

    table.push(Math.max(1, Math.round(ref[lvl] * multiplier)));

  }

  return table;

}



/**

 * Full L1–20 canon pool tables for the tier-derived Weave casters.
 * Derived from the Cleric reference curve × class tier multiplier.

 */

export const CLASS_POOL_TABLES = Object.fromEntries(

  Object.entries(CLASS_WEAVE_TIERS).map(([className, tier]) => [

    className,

    buildTierPoolTable(WEAVE_TIER_MULTIPLIERS[tier]),

  ])

);

// Deprecated aliases retained only for older imports; the tables themselves are canon.
export const DRAFT_CASTER_TIERS = CLASS_WEAVE_TIERS;
export const DRAFT_POOL_TABLES = CLASS_POOL_TABLES;



/** Combined lookup for every Weave-casting class. */

export const ALL_POOL_TABLES = { ...CANON_POOL_TABLES, ...CLASS_POOL_TABLES };



/** Classes with zero Weave RP pool (own resource track, or non-caster). */

export const NO_POOL_CLASSES = new Set(["Oracle", "Soldier", "Warrior"]);



/** All 14 Weave-casting classes among the 17-class roster (excludes Oracle/Soldier/Warrior). */

export const WEAVE_CASTER_CLASSES = [

  ...Object.keys(CANON_POOL_TABLES),

  ...Object.keys(CLASS_POOL_TABLES),

].sort();



/** Four Resonance reputation tracks from Ch9 / reputation.js. */

export const RESONANCE_TRACK_IDS = {

  academic: "academic-factions",

  religious: "religious-orders",

  arcane: "arcane-guilds",

  nature: "nature-circles",

};



/**

 * Legacy class-to-faction mapping retained for compatibility. Reputation no longer
 * changes intrinsic spell cost or maximum Resonance capacity.

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

  const tier = CLASS_WEAVE_TIERS[className];

  if (tier === "half") return 3;

  if (tier === "hybrid") return 2;

  if (tier === "minor") return 1;

  return 0;

}



function resolveRepModifier(_repModifierOrScores) {

  // Compatibility shim only. Reputation is social/institutional and never changes
  // intrinsic Resonance capacity. Numeric legacy modifiers are intentionally ignored.
  return 0;

}



function singleClassPoolBase(className, level) {

  const lvl = clampLevel(level);

  if (!className || NO_POOL_CLASSES.has(className)) return 0;

  const table = ALL_POOL_TABLES[className];

  if (table) return table[lvl];

  return Math.max(1, Math.round(CANON_POOL_TABLES.Cleric[lvl] * WEAVE_TIER_MULTIPLIERS.minor));

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

 * @param {number | ReputationScores} [_repModifierOrScores] Deprecated compatibility input; ignored.

 * @returns {MaxRpResult}

 */

export function mergeMulticlassMaxRp(classEntries, _repModifierOrScores = 0) {

  const weave = (classEntries || [])

    .filter((e) => e.className && !NO_POOL_CLASSES.has(e.className) && e.level > 0);



  if (weave.length === 0) {

    return { maxRp: 0, draft: false, source: "none", tier: "none" };

  }

  if (weave.length === 1) {

    return singleClassMaxRp(weave[0].className, weave[0].level);

  }



  const sorted = sortWeaveClassesForMulticlass(weave);

  const primary = sorted[0];

  const secondary = sorted[1];

  const primaryResult = singleClassMaxRp(primary.className, primary.level, 0);

  const secondaryResult = singleClassMaxRp(secondary.className, secondary.level, 0);

  const secondaryBonus = Math.ceil(secondaryResult.maxRp * 0.25);

  return {

    maxRp: Math.max(0, primaryResult.maxRp + secondaryBonus),

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

    },

  };

}



/**

 * Player-facing multiclass RP breakdown lines (RESONANCE_CANON.md §7 — approved formula).

 * @param {MaxRpResult} result

 * @returns {{ lines: string[]; summary: string } | null}

 */

export function multiclassRpBreakdown(result) {

  const mc = result?.multiclass;

  if (!mc) return null;



  const lines = [

    `${mc.primary} L${mc.primaryLevel}: ${mc.primaryPool} RP (primary pool)`,

    `+ ⌈25% × ${mc.secondary} L${mc.secondaryLevel}⌉ = +${mc.secondaryBonus} RP`,

  ];


  lines.push(`= ${result.maxRp} RP max (approved multiclass formula)`);



  return { lines, summary: lines.join(" · ") };

}



/** Tooltip / aria text for max RP — includes multiclass breakdown when applicable. */

export function formatMaxRpTooltip(result, classLabel = "") {

  if (!result || result.maxRp <= 0) return "No Weave Resonance pool";

  const breakdown = multiclassRpBreakdown(result);

  if (breakdown) return breakdown.summary;

  return classLabel

    ? `Resonance max for ${classLabel}`

    : `Resonance max: ${result.maxRp} RP`;

}



function singleClassMaxRp(className, level, _repModifierOrScores = 0) {

  const lvl = clampLevel(level);

  if (!className || NO_POOL_CLASSES.has(className)) {

    return { maxRp: 0, draft: false, source: "none", tier: "none" };

  }



  const table = ALL_POOL_TABLES[className];

  if (table) {

    const base = table[lvl];

    const tier = CANON_POOL_TABLES[className] ? "full" : CLASS_WEAVE_TIERS[className] || "minor";

    return {

      maxRp: Math.max(0, base),
      draft: false,
      source: "canon",
      tier,
    };

  }

  const fallbackBase = Math.max(1, Math.round(CANON_POOL_TABLES.Cleric[lvl] * WEAVE_TIER_MULTIPLIERS.minor));
  return { maxRp: Math.max(0, fallbackBase), draft: false, source: "canon", tier: "minor" };

}



/**

 * @deprecated Reputation never changes intrinsic maximum RP. Retained for saved-data/API compatibility.

 * @param {ReputationScores | undefined} reputation

 * @returns {number}

 */

export function maxRpRepModifier(_reputation) {
  return 0;
}



/**

 * @deprecated Reputation never changes intrinsic spell cost. Retained for saved-data/API compatibility.

 * @param {string} className

 * @param {ReputationScores | undefined} reputation

 * @returns {number}

 */

export function spellCostRepModifier(_className, _reputation) {
  return 0;
}



/**

 * @deprecated Reputation never changes automatic Retune recovery. Explicit faction rewards may grant situational aid.

 * @param {ReputationScores | undefined} reputation

 * @returns {number}

 */

export function retuneRepBonus(_reputation) {
  return 0;
}



/**

 * @deprecated Moral alignment never changes intrinsic school efficiency. Retained for saved-data/API compatibility.

 * @param {string | undefined} alignment e.g. "Lawful Good", "Neutral Evil"

 * @param {string | undefined} school Spell school name

 * @returns {{ affinity: boolean; opposition: boolean }}

 */

export function schoolAffinityMods(_alignment, _school) {

  // Moral alignment is narrative context, not a magical-efficiency switch.
  return { affinity: false, opposition: false };

}



/**

 * Resolve a class/level to a Resonance Point pool size.

 * @param {string} className

 * @param {number} level

 * @param {number | ReputationScores} [repModifierOrScores] Deprecated compatibility input; reputation no longer changes base capacity.

 * @returns {MaxRpResult}

 */

export function defaultMaxRp(className, level, _repModifierOrScores = 0, multiclassInput = undefined) {

  const parsed = parseMulticlassLevels(

    multiclassInput !== undefined

      ? { primaryClass: className, primaryLevel: level, ...(multiclassInput || {}) }

      : null

  );

  if (parsed && parsed.length > 1) {

    return mergeMulticlassMaxRp(parsed);

  }

  return singleClassMaxRp(className, level);

}



/** Convenience wrapper. Reputation is accepted only for saved-call compatibility and is ignored. */

export function resolveMaxRp(className, level, _reputation, characterOrMulticlass) {

  return defaultMaxRp(className, level, 0, characterOrMulticlass);

}



/** True for the 4 classes with a rulebook-complete L1–20 pool table. */

export function isCanonPoolClass(className) {

  return Boolean(className && CANON_POOL_TABLES[className]);

}



/**

 * Base Resonance cost formula:

 * `Resonance Rank × 2`, modified only by explicit class specialization and
 * current Dissonance surcharge. Faction standing never changes intrinsic spell physics. Cantrips always cost 0 RP but

 * still generate Refrain Dissonance when repeated. Moral alignment does not

 * change the physics of the Weave.

 *

 * @param {number} level Spell level (0 = cantrip).

 * @param {{ specialization?: number; dissonanceSurcharge?: number }} [mods]

 * @returns {number} Final RP cost, floored at 0.

 */

export function spellCost(level, mods = {}) {

  const lvl = Math.max(0, Number(level) || 0);

  if (lvl === 0) return 0;



  const { specialization = 0, dissonanceSurcharge = 0 } = mods;

  let cost = lvl * 2;
  cost -= Number(specialization) || 0;
  cost += Number(dissonanceSurcharge) || 0;

  return Math.max(0, Math.round(cost));

}



/**

 * Full spell cost from spell metadata + character context.

 * @param {{ level?: number; school?: string }} spell

 * @param {{ className?: string; specialization?: number; dissonance?: number; dissonanceLimit?: number }} ctx

 * @returns {number}

 */

export function computeSpellCost(spell, ctx = {}) {

  const className = ctx.className || "";
  const rank = spell?.classRanks?.[className] ?? spell?.classLevels?.[className] ?? spell?.resonanceRank ?? spell?.level ?? 0;
  const surcharge = dissonanceRpSurcharge(ctx.dissonance ?? 0, ctx.dissonanceLimit ?? Infinity);

  return spellCost(rank, {
    specialization: ctx.specialization ?? 0,
    dissonanceSurcharge: surcharge,
  });

}



/**

 * Short rest "Retune" — ≈¼ max pool + casting-attribute modifier.
 * Faction benefits, if earned, are explicit scene rewards rather than automatic physics.

 * @param {number} maxRp

 * @param {number} [castingMod]

 * @param {ReputationScores | undefined} [reputation]

 */

export function retuneAmount(maxRp, castingMod = 0, _reputation) {

  const pool = Math.max(0, Number(maxRp) || 0);

  return Math.max(0, Math.round(pool / 4) + (Number(castingMod) || 0));

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



/**
 * Dissonance is the anti-spam pressure track paired with Resonance Points.
 * RP measures remaining power; Dissonance measures accumulated phase strain.
 */
export function dissonanceLimit(proficiencyBonus = 2, castingMod = 0) {
  const pb = Math.max(2, Math.round(Number(proficiencyBonus) || 2));
  const mod = Math.max(0, Math.round(Number(castingMod) || 0));
  return Math.max(4, 2 + pb + mod);
}

export function dissonanceState(currentDissonance = 0, limit = 6) {
  const current = Math.max(0, Math.round(Number(currentDissonance) || 0));
  const cap = Math.max(4, Math.round(Number(limit) || 6));
  if (current >= cap + 6) return { id: "fractured", label: "Fractured", rpSurcharge: 3, overcastAllowed: false, rankedCastingAllowed: false };
  if (current >= cap + 3) return { id: "discordant", label: "Discordant", rpSurcharge: 2, overcastAllowed: false, rankedCastingAllowed: true };
  if (current >= cap) return { id: "frayed", label: "Frayed", rpSurcharge: 1, overcastAllowed: true, rankedCastingAllowed: true };
  return { id: "tuned", label: "In Tune", rpSurcharge: 0, overcastAllowed: true, rankedCastingAllowed: true };
}

export function dissonanceRpSurcharge(currentDissonance = 0, limit = 6) {
  return dissonanceState(currentDissonance, limit).rpSurcharge;
}

/**
 * Lich (Mage) and Necromancer (Wizard) are deliberate dark-path exceptions.
 * They do not become harmonious at high Dissonance; they force the note through
 * anyway and accept direct magical trauma. This exception belongs only to these
 * Hero Paths and never replaces the parent class's unique mechanic.
 */
export const DARK_TRAUMA_PATHS = new Set(["Lich", "Necromancer"]);

export function isDarkTraumaPath(heroPath = "") {
  return DARK_TRAUMA_PATHS.has(String(heroPath || ""));
}

export function castingPermissionsAtDissonance(currentDissonance = 0, limit = 6, heroPath = "") {
  const state = dissonanceState(currentDissonance, limit);
  if (isDarkTraumaPath(heroPath)) {
    return { ...state, overcastAllowed: true, rankedCastingAllowed: true, traumaticCasting: state.id !== "tuned" };
  }
  return { ...state, traumaticCasting: false };
}

/**
 * Backlash from deliberately forcing a dark-path spell through unstable Resonance.
 * Damage is direct magical trauma: Frayed = 1x Rank, Discordant = 2x,
 * Fractured = 3x (minimum 1). It is applied after the spell resolves.
 */
export function traumaticCastingBacklash({ heroPath = "", rank = 0, currentDissonance = 0, limit = 6 } = {}) {
  if (!isDarkTraumaPath(heroPath)) return { applies: false, damage: 0, state: dissonanceState(currentDissonance, limit).id };
  const state = dissonanceState(currentDissonance, limit);
  const multiplier = state.id === "frayed" ? 1 : state.id === "discordant" ? 2 : state.id === "fractured" ? 3 : 0;
  if (!multiplier) return { applies: false, damage: 0, state: state.id };
  const r = Math.max(0, Math.round(Number(rank) || 0));
  return { applies: true, damage: Math.max(1, r * multiplier), state: state.id, multiplier };
}

/**
 * Dissonance gained by one spell. `repeatCount` is the number of immediate prior
 * consecutive casts of the same named spell. Refrain Dissonance caps at +3.
 * Cantrips have no base Dissonance, but repeated free cantrips still build it.
 */
export function dissonanceGain({ rank = 0, repeatCount = 0, overcastCount = 0, outsideKeyThread = false } = {}) {
  const r = Math.max(0, Math.round(Number(rank) || 0));
  const repeat = Math.min(3, Math.max(0, Math.round(Number(repeatCount) || 0)));
  const overcast = Math.max(0, Math.round(Number(overcastCount) || 0));
  const base = r > 0 ? 1 : 0;
  const highRank = r >= 6 ? 1 : 0;
  return base + repeat + overcast + highRank + (outsideKeyThread ? 1 : 0);
}

/** In combat, Ground the Note: spend the action without casting and bleed off strain. */
export function groundDissonance(currentDissonance, proficiencyBonus = 2) {
  const current = Math.max(0, Math.round(Number(currentDissonance) || 0));
  const amount = Math.max(2, Math.round(Number(proficiencyBonus) || 2));
  return Math.max(0, current - amount);
}

/** A turn with no spell or Weave ability resolves one point naturally. */
export function passiveDissonanceDecay(currentDissonance) {
  return Math.max(0, Math.round(Number(currentDissonance) || 0) - 1);
}

/** A short-rest Retune re-establishes the caster's baseline phase. */
export function retuneDissonance() { return 0; }

/** Meditation reduces strain without fully restoring RP. */
export function meditationDissonanceRecovery(currentDissonance, proficiencyBonus = 2, castingMod = 0) {
  const amount = Math.max(1, Math.round(Number(proficiencyBonus) || 2) + Math.max(0, Math.round(Number(castingMod) || 0)));
  return Math.max(0, Math.round(Number(currentDissonance) || 0) - amount);
}

/** Informational low-Resonance threshold. Dissonance—not low RP—is the anti-spam rule. */
export function lowResonanceThreshold(maxRp) {
  return Math.ceil(Math.max(0, Number(maxRp) || 0) * 0.25);
}

export function isLowResonance(currentRp, maxRp) {
  return Number(currentRp) < lowResonanceThreshold(maxRp);
}

/** @deprecated Backward-compatible aliases for saved-session/UI code. */
export const burnoutThreshold = lowResonanceThreshold;
/** @deprecated Backward-compatible alias; this is an informational low-RP warning only. */
export const isBurnoutRisk = isLowResonance;

/** @deprecated Dissonance states replace the old Burnout check. */
export function overcastBurnoutHintAfterCast() {
  return null;
}

/** @deprecated Kept only so older imports/saves do not break. */
export const BURNOUT_EFFECT_STUB = {
  label: "Low Resonance",
  summary: "Below 25% RP — informational only; Dissonance governs casting strain",
  disadvantageNote: "No automatic penalty",
  actionPenalty: "No automatic penalty",
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

 * Overcast modifies RP cost and adds Dissonance; it does not use a separate Burnout subsystem.

 */

export const OVERCAST_OPTIONS = [

  { id: "empowered", label: "Empowered", rpCost: 2, dissonance: 1, effect: "+50% damage or healing" },

  { id: "extended", label: "Extended", rpCost: 1, dissonance: 1, effect: "2× duration" },

  { id: "widened", label: "Widened", rpCost: 3, dissonance: 1, effect: "2× area of effect" },

  { id: "heightened", label: "Heightened", rpCost: 4, dissonance: 1, effect: "+1 effective spell level" },

  { id: "quickened", label: "Quickened", rpCost: 3, dissonance: 1, effect: "Cast as a bonus action" },

  { id: "subtle", label: "Subtle", rpCost: 1, dissonance: 1, effect: "No verbal/somatic components" },

  { id: "distant", label: "Distant", rpCost: 1, dissonance: 1, effect: "2× range" },

  { id: "twinned", label: "Twinned", rpCost: 3, dissonance: 1, effect: "Target a second creature" },

];



/** Nine ethos alignments for roleplay and path requirements. Alignment does not alter RP cost. */
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

/** @deprecated Moral alignment no longer changes Resonance efficiency. */

export const ALIGNMENT_SCHOOL_AFFINITY = {
  Good: { affinity: [], opposition: [] },
  Neutral: { affinity: [], opposition: [] },
  Evil: { affinity: [], opposition: [] },
};


