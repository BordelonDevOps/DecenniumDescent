/**
 * XP advancement and award helpers.
 *
 * Canon: docs/mechanics/XP_ADVANCEMENT_CANON.md
 *
 * Confirmed rulebook L1–L20 cumulative thresholds and proficiency bonuses are
 * exported without `draft`. CR→XP, party split, and encounter budget helpers are
 * **draft: true** — owner approval required before treating as canon.
 */

/** @typedef {"easy" | "medium" | "hard" | "deadly"} DraftEncounterDifficulty */

/**
 * Confirmed cumulative XP required per level (rulebook Character Advancement table).
 * Index 0 unused; `CANON_XP_THRESHOLDS[level]` for levels 1–20.
 */
export const CANON_XP_THRESHOLDS = [
  null,
  0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000,
  85000, 100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000,
];

/** Confirmed proficiency bonus by character level (total level for multiclass). */
export const CANON_PROFICIENCY_BONUS = [
  null,
  2, 2, 2, 2, 3, 3, 3, 3, 4, 4,
  4, 4, 5, 5, 5, 5, 6, 6, 6, 6,
];

/** Cumulative XP threshold for a level (1–20). */
export function xpThresholdForLevel(level = 1) {
  const lvl = Math.max(1, Math.min(20, Math.round(Number(level) || 1)));
  return CANON_XP_THRESHOLDS[lvl] ?? 0;
}

/** Confirmed proficiency bonus for total character level (1–20). */
export function proficiencyBonusForLevel(level = 1) {
  const lvl = Math.max(1, Math.min(20, Math.round(Number(level) || 1)));
  return CANON_PROFICIENCY_BONUS[lvl] ?? 2;
}

/** XP still needed to reach the next level from `currentXp` at `currentLevel`. */
export function xpToNextLevel(currentLevel = 1, currentXp = 0) {
  const lvl = Math.max(1, Math.min(19, Math.round(Number(currentLevel) || 1)));
  const next = CANON_XP_THRESHOLDS[lvl + 1] ?? CANON_XP_THRESHOLDS[20];
  return Math.max(0, next - (Number(currentXp) || 0));
}

/** Confirmed gap between adjacent level thresholds (e.g. L3→L4 = 1,800). */
export function levelThresholdGap(level = 1) {
  const lvl = Math.max(1, Math.min(19, Math.round(Number(level) || 1)));
  const cur = CANON_XP_THRESHOLDS[lvl] ?? 0;
  const next = CANON_XP_THRESHOLDS[lvl + 1] ?? cur;
  return Math.max(0, next - cur);
}

/** Derive character level from cumulative XP using confirmed thresholds. */
export function levelFromXp(xp = 0) {
  const total = Math.max(0, Number(xp) || 0);
  for (let lvl = 20; lvl >= 1; lvl -= 1) {
    if (total >= (CANON_XP_THRESHOLDS[lvl] ?? 0)) return lvl;
  }
  return 1;
}

export function formatXp(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return "0";
  return n.toLocaleString("en-US");
}

// --- DRAFT — OWNER APPROVAL REQUIRED ---

export const XP_ECONOMY_DRAFT = {
  draft: true,
  owner: "DRAFT — OWNER APPROVAL REQUIRED",
  source: "docs/mechanics/XP_ADVANCEMENT_CANON.md § DRAFT",
};

/** Draft CR → XP award table (provisional; mirrors bestiary pattern, unverified). */
export const DRAFT_CR_XP_TABLE = {
  0: 10,
  "1/8": 25,
  "1/4": 50,
  "1/2": 100,
  1: 200,
  2: 450,
  3: 700,
  4: 1100,
  5: 1800,
  6: 2300,
  7: 2900,
  8: 3900,
  9: 5000,
  10: 5900,
  11: 7200,
  12: 8400,
  13: 10000,
  14: 11500,
  15: 13000,
  16: 15000,
  17: 18000,
  18: 20000,
  19: 22000,
  20: 25000,
};

/** Draft encounter difficulty multipliers vs per-character threshold gap. */
export const DRAFT_ENCOUNTER_BUDGET_MULTIPLIERS = {
  easy: 0.5,
  medium: 1,
  hard: 1.5,
  deadly: 2,
};

/**
 * Normalize CR input to a lookup key (number or fraction string).
 * @param {string | number | null | undefined} cr
 */
export function parseCrValue(cr) {
  if (cr == null || cr === "" || cr === "?") return null;
  const raw = String(cr).trim().toLowerCase();
  if (raw === "0") return 0;
  if (raw === "1/8" || raw === "⅛") return "1/8";
  if (raw === "1/4" || raw === "¼") return "1/4";
  if (raw === "1/2" || raw === "½") return "1/2";
  const num = Number(raw);
  if (Number.isFinite(num) && num >= 0) return num;
  return null;
}

/** Parse CR from Session foe notes (`CR 5 · Zone`). */
export function parseCrFromNotes(notes = "") {
  const match = String(notes).match(/\bCR\s+([0-9]+(?:\/[0-9]+)?|\?)/i);
  if (!match) return null;
  return parseCrValue(match[1]);
}

/**
 * Draft XP for one defeated creature at the given CR.
 * CR 21+ → 33,000 + 5,000 per CR above 20.
 * @param {string | number | null | undefined} cr
 */
export function draftXpForCr(cr) {
  const key = parseCrValue(cr);
  if (key == null) return 0;
  if (typeof key === "number" && key > 20) {
    return 33000 + 5000 * (key - 20);
  }
  const xp = DRAFT_CR_XP_TABLE[key];
  return typeof xp === "number" ? xp : 0;
}

/**
 * Draft equal party split — divide total XP among participants (round down each).
 * @param {number} totalXp
 * @param {number} participantCount
 */
export function splitPartyXp(totalXp, participantCount) {
  const total = Math.max(0, Math.floor(Number(totalXp) || 0));
  const count = Math.max(0, Math.floor(Number(participantCount) || 0));
  if (count <= 0 || total <= 0) {
    return { perMember: 0, remainder: total, participantCount: count, totalXp: total, draft: true };
  }
  const perMember = Math.floor(total / count);
  const remainder = total - perMember * count;
  return { perMember, remainder, participantCount: count, totalXp: total, draft: true };
}

/**
 * Draft encounter budget sketch for a standard four-character party.
 * @param {number} avgPartyLevel
 * @param {DraftEncounterDifficulty} difficulty
 * @param {number} [partySize=4]
 */
export function draftEncounterBudget(avgPartyLevel, difficulty = "medium", partySize = 4) {
  const lvl = Math.max(1, Math.min(19, Math.round(Number(avgPartyLevel) || 1)));
  const gap = levelThresholdGap(lvl);
  const mult = DRAFT_ENCOUNTER_BUDGET_MULTIPLIERS[difficulty] ?? 1;
  const totalBudget = Math.round(gap * mult);
  const size = Math.max(1, Math.floor(Number(partySize) || 4));
  const split = splitPartyXp(totalBudget, size);
  return {
    draft: true,
    avgPartyLevel: lvl,
    difficulty,
    partySize: size,
    thresholdGap: gap,
    multiplier: mult,
    totalBudget,
    perCharacterTarget: split.perMember,
    ...XP_ECONOMY_DRAFT,
  };
}

/**
 * Sum draft CR→XP for multiple creatures in an encounter.
 * @param {Array<string | number | null | undefined>} crs
 */
export function draftEncounterXpTotal(crs = []) {
  const total = crs.reduce((sum, cr) => sum + draftXpForCr(cr), 0);
  return { totalXp: total, creatureCount: crs.length, draft: true };
}

/**
 * Build a Session-facing draft XP award summary line (does not mutate saves).
 * @param {object} opts
 * @param {string} opts.foeName
 * @param {string | number | null | undefined} opts.cr
 * @param {number} opts.participantCount
 */
export function formatDraftXpAwardLine({ foeName, cr, participantCount }) {
  const totalXp = draftXpForCr(cr);
  const split = splitPartyXp(totalXp, participantCount);
  const crLabel = cr == null || cr === "" ? "?" : String(cr);
  return `[Draft XP] ${foeName} (CR ${crLabel}): ${formatXp(totalXp)} total → ${formatXp(split.perMember)} each (${split.participantCount} participant${split.participantCount === 1 ? "" : "s"})`;
}
