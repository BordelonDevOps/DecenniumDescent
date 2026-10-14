import { SPELLS } from "./spells";

/** Decennium class → spell-list class names (handles legacy lowercase entries). */
export const CLASS_SPELL_ALIASES = {
  Bard: ["Bard", "bard"],
  Cleric: ["Cleric", "cleric"],
  Druid: ["Druid"],
  Paladin: ["Paladin", "paladin"],
  Ranger: ["Ranger", "ranger"],
  Mage: ["Wizard", "mage"],
  Wizard: ["Wizard", "mage"],
  Mirrorsage: ["Wizard", "Bard", "mage"],
  Oracle: ["Cleric", "Bard", "cleric"],
  Shaman: ["Druid", "Cleric"],
  "Crimson Agent": ["Warlock", "Wizard", "mage"],
  Thief: ["Bard", "Warlock"],
  Tinker: ["Wizard", "mage"],
  Sorcerer: ["Sorcerer", "Wizard", "mage"],
  Warlock: ["Warlock"],
};

/** Optional school gate per class (mirrors spell workbook restrictions). */
export const CLASS_SPELL_SCHOOLS = {
  Bard: ["Enchantment", "Illusion", "Universal"],
  Cleric: ["Abjuration", "Divination", "Necromancy", "Universal"],
  Druid: ["Abjuration", "Conjuration", "Necromancy", "Transmutation"],
  Mage: ["Abjuration", "Conjuration", "Evocation", "Transmutation", "Universal"],
  Wizard: [
    "Abjuration",
    "Conjuration",
    "Divination",
    "Enchantment",
    "Evocation",
    "Illusion",
    "Necromancy",
    "Transmutation",
    "Universal",
  ],
  Mirrorsage: ["Illusion", "Enchantment", "Divination", "Universal"],
  Oracle: ["Divination", "Abjuration", "Enchantment", "Universal"],
  Shaman: ["Conjuration", "Divination", "Necromancy", "Transmutation"],
  Paladin: ["Abjuration", "Divination", "Enchantment", "Universal"],
  Ranger: ["Conjuration", "Divination", "Transmutation"],
  "Crimson Agent": ["Enchantment", "Illusion", "Necromancy"],
  Thief: ["Illusion", "Enchantment"],
  Tinker: ["Transmutation", "Conjuration", "Universal"],
  Sorcerer: ["Evocation", "Conjuration", "Transmutation", "Universal"],
  Warlock: ["Conjuration", "Enchantment", "Necromancy", "Universal"],
};

const NON_CASTERS = new Set(["Soldier", "Warrior"]);
/** Oracles power Mystery Revelations via Revelation Charges — not Weave spell slots (rulebook Ch Oracle). */
export const REVELATION_CASTERS = new Set(["Oracle"]);

export function isRevelationCaster(className) {
  return Boolean(className && REVELATION_CASTERS.has(className));
}

export function isSpellcasterClass(className) {
  return Boolean(className && !NON_CASTERS.has(className) && !REVELATION_CASTERS.has(className));
}

export function getSpellAliasesForClass(className) {
  if (!className) return [];
  return CLASS_SPELL_ALIASES[className] || [className];
}

export function isSpellAvailableToClass(spell, className) {
  if (!className || NON_CASTERS.has(className)) return false;
  const aliases = getSpellAliasesForClass(className);
  const classMatch = spell.classes.some((c) =>
    aliases.some((a) => a.toLowerCase() === c.toLowerCase())
  );
  if (!classMatch) return false;
  const schools = CLASS_SPELL_SCHOOLS[className];
  if (!schools) return true;
  return schools.includes(spell.school);
}

/** Stable key used in character saves — the SPELLS object key when possible. */
export function getSpellKey(spellOrName) {
  if (typeof spellOrName === "string") {
    const direct = SPELLS[spellOrName];
    if (direct) return spellOrName;
    const slug = spellOrName.toLowerCase().replace(/\s+/g, "-");
    if (SPELLS[slug]) return slug;
    const unders = spellOrName.toLowerCase().replace(/\s+/g, "_");
    if (SPELLS[unders]) return unders;
    const entry = Object.entries(SPELLS).find(
      ([, s]) => s.name.toLowerCase() === spellOrName.toLowerCase()
    );
    return entry ? entry[0] : slug;
  }
  const entry = Object.entries(SPELLS).find(([, s]) => s === spellOrName);
  if (entry) return entry[0];
  return spellOrName.name.toLowerCase().replace(/\s+/g, "-");
}

export function getSpellByKey(key) {
  if (!key) return null;
  if (SPELLS[key]) return SPELLS[key];
  const normalized = getSpellKey(key);
  return SPELLS[normalized] || null;
}

export function getSpellDisplayName(key) {
  return getSpellByKey(key)?.name || key.replace(/[-_]/g, " ");
}

export function normalizeSpellKeys(keys) {
  if (!Array.isArray(keys)) return [];
  const seen = new Set();
  const out = [];
  for (const k of keys) {
    const nk = getSpellKey(k);
    if (!seen.has(nk)) {
      seen.add(nk);
      out.push(nk);
    }
  }
  return out;
}

export function filterSpellsForClass(spells, className, { schoolFilter, levelFilter } = {}) {
  let list = [...spells];
  if (className) {
    list = list.filter((s) => isSpellAvailableToClass(s, className));
  }
  if (schoolFilter && schoolFilter !== "All") {
    list = list.filter((s) => s.school === schoolFilter);
  }
  if (levelFilter && levelFilter !== "All") {
    const level = levelFilter === "Cantrips" ? 0 : parseInt(levelFilter, 10);
    list = list.filter((s) => s.level === level);
  }
  return list.sort((a, b) => (a.level !== b.level ? a.level - b.level : a.name.localeCompare(b.name)));
}

export function getSpellEntries() {
  return Object.entries(SPELLS).map(([key, spell]) => ({ key, spell }));
}

export function getAllSpellClassNames() {
  const names = new Set(Object.keys(CLASS_SPELL_ALIASES));
  Object.values(SPELLS).forEach((s) => s.classes.forEach((c) => names.add(c)));
  return [...names].sort((a, b) => a.localeCompare(b));
}

/** Session / table lookup — match spell name (2+ chars), optional class gate. */
export function searchSpellsByName(query, className, limit = 8) {
  const q = String(query || "").trim().toLowerCase();
  if (q.length < 2) return [];
  return getSpellEntries()
    .filter(({ spell }) => spell.name.toLowerCase().includes(q))
    .filter(({ spell }) => !className || isSpellAvailableToClass(spell, className))
    .slice(0, limit)
    .map(({ key, spell }) => ({ key, name: spell.name, level: spell.level, school: spell.school }));
}
