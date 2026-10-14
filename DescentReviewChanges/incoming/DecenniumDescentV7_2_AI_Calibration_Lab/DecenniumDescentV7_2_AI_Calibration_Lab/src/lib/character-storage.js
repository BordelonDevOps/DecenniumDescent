import { normalizeSpellKeys } from "@/data/spell-utils";
import { normalizeReputation } from "@/data/reputation";

/** Shared localStorage helpers for Decennium Descent characters */
export const CHARACTERS_KEY = "dd_characters";

/** Legacy race labels from pre–Umbrin renames (bestiary scrub 2026-07-29; Umbrin 2026-07-29 PM). */
const LEGACY_RACE_ALIASES = {
  Drow: "Umbrin",
  "Umbral Elf": "Umbrin",
  "umbral-elf": "Umbrin",
  drow: "Umbrin",
};
const LEGACY_SUBRACE_ALIASES = {
  "Noble Drow": "Obsidian Highborn",
  "Noble Umbral Elf": "Obsidian Highborn",
};

function migrateRaceFields(raw) {
  const race = LEGACY_RACE_ALIASES[raw.race] ?? raw.race ?? "";
  const subrace = LEGACY_SUBRACE_ALIASES[raw.subrace] ?? raw.subrace ?? "";
  return { race, subrace };
}

/** Coerce saved JSON into a consistent shape for load/export. */
export function normalizeCharacter(raw) {
  if (!raw || typeof raw !== "object") return null;
  const { race, subrace } = migrateRaceFields(raw);
  const abilities = Array.isArray(raw.abilities)
    ? raw.abilities.map((a) => ({
        name: a.name || "",
        score: Number(a.score) || 10,
        modifier:
          typeof a.modifier === "number"
            ? a.modifier
            : Math.floor(((Number(a.score) || 10) - 10) / 2),
      }))
    : [];
  return {
    ...raw,
    id: raw.id || "",
    name: typeof raw.name === "string" ? raw.name : "",
    race,
    subrace,
    class: raw.class || "",
    archClass: raw.archClass || "",
    heroPath: raw.heroPath || "",
    sacredOath: raw.sacredOath || "",
    druidCircle: raw.druidCircle || "",
    oracleMystery: raw.oracleMystery || "",
    oracleCurse: raw.oracleCurse || "",
    background: raw.background || "",
    alignment: raw.alignment || "",
    level: Number(raw.level) || 1,
    xp: Number(raw.xp) || 0,
    resonancePoints: Number(raw.resonancePoints ?? 3),
    feats: Array.isArray(raw.feats) ? raw.feats : [],
    abilities,
    knownSpells: normalizeSpellKeys(raw.knownSpells || []),
    preparedSpells: normalizeSpellKeys(raw.preparedSpells || []),
    appearance: raw.appearance || null,
    notes: raw.notes || "",
    reputation: normalizeReputation(raw.reputation),
    secondaryClass: raw.secondaryClass || "",
    secondaryLevel:
      raw.secondaryClass && raw.secondaryLevel != null
        ? Number(raw.secondaryLevel) || 1
        : undefined,
  };
}

export function loadSavedCharacters() {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(CHARACTERS_KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list.map(normalizeCharacter).filter(Boolean) : [];
  } catch {
    return [];
  }
}

export function persistCharacters(list) {
  localStorage.setItem(CHARACTERS_KEY, JSON.stringify(list));
}

export function upsertCharacter(character) {
  const list = loadSavedCharacters();
  const id = character.id || `char_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  const next = { ...normalizeCharacter(character), id, updatedAt: new Date().toISOString() };
  const idx = list.findIndex((c) => c.id === id);
  if (idx >= 0) list[idx] = next;
  else list.push(next);
  persistCharacters(list);
  return next;
}

export function deleteCharacter(id) {
  const list = loadSavedCharacters().filter((c) => c.id !== id);
  persistCharacters(list);
  return list;
}

export function characterDisplayName(c) {
  return c?.name?.trim() || `${c?.race || "Unknown"} ${c?.class || "Adventurer"}`.trim();
}
