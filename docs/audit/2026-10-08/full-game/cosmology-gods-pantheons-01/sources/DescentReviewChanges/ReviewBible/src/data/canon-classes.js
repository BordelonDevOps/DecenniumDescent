/**
 * Player rulebook Ch3 — Classes Table (`rulebook_output.txt` lines 861–877).
 * Sole selectable base classes in Character Builder and sheet UI.
 *
 * Product canon: 17 base classes (this list). Rulebook prose says "eighteen" —
 * treat that as a book typo; the 17-row Classes Table is authoritative.
 * Fighter has a full rulebook chapter but is not in the Classes Table — archive only.
 * Swashbuckler is not in the table — orphan reference in class-details.js only.
 */
export const CANON_CLASSES = [
  "Bard",
  "Cleric",
  "Crimson Agent",
  "Dragoon",
  "Druid",
  "Mage",
  "Monk",
  "Mirrorsage",
  "Oracle",
  "Ranger",
  "Shaman",
  "Soldier",
  "Thief",
  "Tinker",
  "Warrior",
  "Wizard",
  "Paladin",
];

/** @param {string | undefined | null} name */
export function isCanonClass(name) {
  return Boolean(name && CANON_CLASSES.includes(name));
}
