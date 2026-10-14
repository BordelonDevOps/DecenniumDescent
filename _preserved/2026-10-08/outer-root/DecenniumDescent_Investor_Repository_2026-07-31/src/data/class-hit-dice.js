/**
 * Rulebook Ch3 Classes Table — hit dice for all 17 CANON_CLASSES.
 * Source: Player Rulebook Ch. 3 / `rulebook_output.txt`.
 */
import { CANON_CLASSES } from "./canon-classes";

/** @type {Record<string, { die: number; max: number; avg: number }>} */
export const CLASS_HIT_DICE = {
  Bard: { die: 8, max: 8, avg: 5 },
  Cleric: { die: 8, max: 8, avg: 5 },
  "Crimson Agent": { die: 8, max: 8, avg: 5 },
  Dragoon: { die: 10, max: 10, avg: 6 },
  Druid: { die: 8, max: 8, avg: 5 },
  Mage: { die: 6, max: 6, avg: 4 },
  Monk: { die: 8, max: 8, avg: 5 },
  Mirrorsage: { die: 6, max: 6, avg: 4 },
  Oracle: { die: 8, max: 8, avg: 5 },
  Paladin: { die: 10, max: 10, avg: 6 },
  Ranger: { die: 10, max: 10, avg: 6 },
  Shaman: { die: 8, max: 8, avg: 5 },
  Soldier: { die: 10, max: 10, avg: 6 },
  Thief: { die: 8, max: 8, avg: 5 },
  Tinker: { die: 8, max: 8, avg: 5 },
  Warrior: { die: 12, max: 12, avg: 7 },
  Wizard: { die: 6, max: 6, avg: 4 },
};

/**
 * Rulebook HP: 1st level = max hit die + CON mod; each level after = avg die + CON mod.
 * @param {number} level Character level in the class (1–20).
 * @param {number} conMod Constitution modifier.
 * @param {string} [className] CANON_CLASSES name.
 * @returns {number}
 */
export function estimateMaxHpFromHitDie(level, conMod, className) {
  const lvl = Math.max(1, Math.min(20, Math.round(Number(level) || 1)));
  const con = Math.round(Number(conMod) || 0);
  const hd = CLASS_HIT_DICE[className] ?? { die: 6, max: 6, avg: 4 };
  if (lvl === 1) return Math.max(1, hd.max + con);
  return Math.max(1, hd.max + con + (lvl - 1) * (hd.avg + con));
}

if (process.env.NODE_ENV !== "production") {
  const missing = CANON_CLASSES.filter((name) => !CLASS_HIT_DICE[name]);
  if (missing.length) {
    console.warn("CLASS_HIT_DICE missing CANON_CLASSES entries", missing);
  }
}
