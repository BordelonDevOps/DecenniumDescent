import { SPELLS } from "./spells";
import { CANON_CLASSES } from "./canon-classes";
import { getClassSpellProgression } from "./class-spell-progression";

/**
 * Direct base-class spell identities. The spell catalog no longer depends on
 * retired Sorcerer/Warlock aliases. Warlock remains a prestige path only.
 */
export const CLASS_SPELL_ALIASES = Object.fromEntries(
  CANON_CLASSES.map((className) => [className, [className]])
);

/** Player Rulebook / class_spell_school_mapping.csv — general Weave access. */
export const CLASS_SPELL_SCHOOLS = {
  Bard: ["Enchantment", "Illusion", "Universal"],
  Cleric: ["Abjuration", "Divination", "Necromancy", "Universal"],
  "Crimson Agent": ["Enchantment", "Evocation", "Illusion", "Necromancy"],
  Dragoon: ["Conjuration", "Evocation", "Transmutation"],
  Druid: ["Abjuration", "Conjuration", "Necromancy", "Transmutation"],
  Mage: ["Abjuration", "Conjuration", "Evocation", "Transmutation", "Universal"],
  Monk: ["Abjuration", "Illusion", "Transmutation"],
  Mirrorsage: ["Divination", "Enchantment", "Illusion", "Universal"],
  Oracle: [],
  Ranger: ["Conjuration", "Divination", "Transmutation"],
  Shaman: ["Conjuration", "Divination", "Necromancy", "Transmutation"],
  Soldier: [],
  Thief: ["Enchantment", "Illusion", "Necromancy", "Transmutation"],
  Tinker: ["Abjuration", "Conjuration", "Transmutation", "Universal"],
  Warrior: [],
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
  Paladin: ["Abjuration", "Divination", "Enchantment", "Universal"],
};

export const NON_WEAVE_CLASSES = new Set(["Oracle", "Soldier", "Warrior"]);
/** Oracles power Mystery Revelations via Revelation Charges — not Resonance Points. */
export const REVELATION_CASTERS = new Set(["Oracle"]);

export function isRevelationCaster(className) {
  return Boolean(className && REVELATION_CASTERS.has(className));
}

export function isSpellcasterClass(className) {
  return Boolean(className && !NON_WEAVE_CLASSES.has(className));
}

export function getSpellAliasesForClass(className) {
  if (!className) return [];
  return CLASS_SPELL_ALIASES[className] || [className];
}

/** Effective Resonance Rank for this class when a spell has multiple school placements. */
export function getSpellLevelForClass(spell, className) {
  if (!spell) return null;
  if (!className || className === "All") return spell.level ?? null;
  const level = spell.classLevels?.[className];
  return Number.isInteger(level) ? level : null;
}

/** Effective school used for this class's lowest-level placement. */
export function getSpellSchoolForClass(spell, className) {
  if (!spell) return null;
  if (!className || className === "All") return spell.school ?? null;
  return spell.classSchools?.[className] ?? null;
}

export function isSpellAvailableToClass(spell, className) {
  if (!className || NON_WEAVE_CLASSES.has(className)) return false;
  return Number.isInteger(getSpellLevelForClass(spell, className));
}

/** Preferred name for new code: class-specific Resonance Rank (0–9). */
export function getSpellRankForClass(spell, className) {
  return getSpellLevelForClass(spell, className);
}

/** Character level at which this class can learn the spell. */
export function getSpellLearnLevelForClass(spell, className) {
  if (!spell || !className || className === "All") return null;
  const explicit = spell.classLearnLevels?.[className];
  if (Number.isInteger(explicit)) return explicit;
  const rank = getSpellLevelForClass(spell, className);
  if (!Number.isInteger(rank)) return null;
  const progression = getClassSpellProgression(className);
  const fallback = progression.learnLevels?.[rank];
  return Number.isInteger(fallback) ? fallback : null;
}

export function isSpellLearnableAtLevel(spell, className, characterLevel) {
  if (!isSpellAvailableToClass(spell, className)) return false;
  const learnLevel = getSpellLearnLevelForClass(spell, className);
  if (!Number.isInteger(learnLevel)) return false;
  return Number(characterLevel || 0) >= learnLevel;
}

/** Stable key used in character saves — the SPELLS object key when possible. */
export function getSpellKey(spellOrName) {
  if (typeof spellOrName === "string") {
    const direct = SPELLS[spellOrName];
    if (direct) return spellOrName;
    const slug = spellOrName.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    if (SPELLS[slug]) return slug;
    const entry = Object.entries(SPELLS).find(
      ([, spell]) => spell.name.toLowerCase() === spellOrName.toLowerCase()
    );
    return entry ? entry[0] : slug;
  }
  const entry = Object.entries(SPELLS).find(([, spell]) => spell === spellOrName);
  if (entry) return entry[0];
  return spellOrName.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
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
  for (const key of keys) {
    const normalized = getSpellKey(key);
    if (!seen.has(normalized)) {
      seen.add(normalized);
      out.push(normalized);
    }
  }
  return out;
}

export function filterSpellsForClass(spells, className, { schoolFilter, levelFilter, characterLevel } = {}) {
  let list = [...spells].filter((spell) => isSpellAvailableToClass(spell, className));
  if (characterLevel != null) {
    list = list.filter((spell) => isSpellLearnableAtLevel(spell, className, characterLevel));
  }
  if (schoolFilter && schoolFilter !== "All") {
    list = list.filter((spell) => {
      const level = getSpellLevelForClass(spell, className);
      return (spell.placements || []).some(
        (placement) =>
          placement.school === schoolFilter &&
          placement.level === level &&
          CLASS_SPELL_SCHOOLS[className]?.includes(placement.school)
      );
    });
  }
  if (levelFilter && levelFilter !== "All") {
    const level = levelFilter === "Cantrips" ? 0 : parseInt(levelFilter, 10);
    list = list.filter((spell) => getSpellLevelForClass(spell, className) === level);
  }
  return list.sort((a, b) => {
    const aLevel = getSpellLevelForClass(a, className) ?? 99;
    const bLevel = getSpellLevelForClass(b, className) ?? 99;
    return aLevel !== bLevel ? aLevel - bLevel : a.name.localeCompare(b.name);
  });
}

export function getSpellEntries() {
  return Object.entries(SPELLS).map(([key, spell]) => ({ key, spell }));
}

export function getAllSpellClassNames() {
  return CANON_CLASSES.filter((className) => isSpellcasterClass(className));
}

/**
 * Session / table lookup — match spell name (2+ chars), optional class gate.
 * @param {string} query
 * @param {string | undefined | null} className
 * @param {number} [limit]
 * @param {number | null} [characterLevel]
 */
export function searchSpellsByName(query, className, limit = 8, characterLevel = null) {
  const q = String(query || "").trim().toLowerCase();
  if (q.length < 2) return [];
  return getSpellEntries()
    .filter(({ spell }) => spell.name.toLowerCase().includes(q))
    .filter(({ spell }) => !className || isSpellAvailableToClass(spell, className))
    .filter(({ spell }) => characterLevel == null || !className || isSpellLearnableAtLevel(spell, className, characterLevel))
    .slice(0, limit)
    .map(({ key, spell }) => ({
      key,
      name: spell.name,
      resonanceRank: className ? getSpellLevelForClass(spell, className) : spell.level,
      level: className ? getSpellLevelForClass(spell, className) : spell.level,
      learnLevel: className ? getSpellLearnLevelForClass(spell, className) : null,
      school: className ? getSpellSchoolForClass(spell, className) : spell.school,
    }));
}
