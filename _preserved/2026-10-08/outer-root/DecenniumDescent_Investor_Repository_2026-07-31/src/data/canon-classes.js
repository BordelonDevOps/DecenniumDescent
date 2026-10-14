/**
 * Player Rulebook Ch. 3 — Classes Table (`rulebook_output.txt`).
 * Sole selectable base classes in Character Builder and sheet UI.
 *
 * Product canon: 17 base classes (this list). The Player Rulebook is aligned
 * to this roster. Fighter and Swashbuckler survive only as legacy input aliases
 * where backward compatibility requires them; neither is a selectable base class.
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
