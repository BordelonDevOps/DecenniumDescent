/** Prestige classes — canon from decennium descent player rulebook.docx */
import lorebook from "./prestige-lorebook.json";

function cleanRole(text) {
  if (!text) return "";
  const cut = text.split("Character Story")[0].trim();
  return cut.replace(/\*\*/g, "");
}

/** @typedef {{ name: string; baseClass: string; summary: string; entrance: string; requirements: string; unlock: string; hallmarks: string[]; draftHallmarkIndices: number[]; capstone: string; draftCapstone: boolean; combatRole: string }} PrestigePath */

function trimField(value) {
  return typeof value === "string" ? value.trim() : "";
}

function cleanHallmarks(list) {
  return (list || []).map((h) => trimField(h)).filter(Boolean);
}

function cleanDraftHallmarkIndices(indices, hallmarks) {
  return [...new Set((indices || []).filter((index) => Number.isInteger(index) && index >= 0 && index < hallmarks.length))];
}

/** @type {PrestigePath[]} */
export const prestigePaths = lorebook.map((p) => {
  const hallmarks = cleanHallmarks(p.hallmarks);
  return {
    name: trimField(p.name),
    baseClass: trimField(p.baseClass),
    summary: trimField(p.summary),
    entrance: trimField(p.unlock || p.entrance),
    requirements: trimField(p.requirements),
    unlock: trimField(p.unlock || p.entrance),
    hallmarks,
    draftHallmarkIndices: cleanDraftHallmarkIndices(p.draftHallmarkIndices, hallmarks),
    capstone: trimField(p.capstone),
    draftCapstone: p.draftCapstone === true,
    combatRole: cleanRole(p.combatRole),
  };
});

const BASE_CLASS_ALIASES = {
  Bard: [],
  Cleric: ["Cleric"],
  "Crimson Agent": ["Crimson Agent"],
  Druid: ["Druid"],
  Mage: ["Mage", "Arcanist"],
  Mirrorsage: ["Mirrorsage"],
  Oracle: [],
  Paladin: [],
  Ranger: ["Ranger"],
  Shaman: ["Shaman"],
  Soldier: ["Soldier"],
  Thief: ["Thief"],
  Tinker: ["Tinker"],
  Warrior: ["Warrior"],
  Wizard: ["Mage", "Arcanist", "Wizard"],
  /** Legacy Fighter references map to Warrior for old save/prestige compatibility only. */
  Fighter: ["Warrior"],
  Monk: ["Monk"],
  Dragoon: ["Dragoon"],
};

/** Prestige paths whose requirements mention this base class name */
export function prestigeForBaseClass(className) {
  const needles = BASE_CLASS_ALIASES[className] ?? [className];
  return prestigePaths.filter((p) =>
    needles.some((n) => p.baseClass.toLowerCase().includes(n.toLowerCase()))
  );
}

export default prestigePaths;
