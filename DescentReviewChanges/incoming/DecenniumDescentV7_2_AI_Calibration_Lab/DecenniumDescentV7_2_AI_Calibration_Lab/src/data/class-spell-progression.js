/**
 * Canon class spell-acquisition curves.
 *
 * A spell has a Resonance Rank (0–9) that describes magical complexity and RP
 * cost. Each class then has its own class level at which that rank becomes
 * learnable. This intentionally permits a classic class-driven pattern where the
 * same named spell is learned by different classes at different character
 * levels without duplicating the spell record.
 *
 * Oracle is not a Weave caster: Mystery Revelations use Revelation Charges.
 * Soldier and Warrior have no general Weave list.
 */
export const CLASS_SPELL_PROGRESSION = {
  Bard: { mode: "hybrid", maxRank: 7, learnLevels: { 0: 1, 1: 1, 2: 4, 3: 7, 4: 10, 5: 13, 6: 16, 7: 19 } },
  Cleric: { mode: "full", maxRank: 9, learnLevels: { 0: 1, 1: 1, 2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 15, 9: 17 } },
  "Crimson Agent": { mode: "hybrid", maxRank: 6, learnLevels: { 0: 1, 1: 2, 2: 5, 3: 8, 4: 11, 5: 15, 6: 19 } },
  Dragoon: { mode: "minor", maxRank: 4, learnLevels: { 0: 3, 1: 3, 2: 8, 3: 13, 4: 18 } },
  Druid: { mode: "full", maxRank: 9, learnLevels: { 0: 1, 1: 1, 2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 15, 9: 17 } },
  Mage: { mode: "full", maxRank: 9, learnLevels: { 0: 1, 1: 1, 2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 15, 9: 17 } },
  Monk: { mode: "minor", maxRank: 4, learnLevels: { 0: 1, 1: 3, 2: 8, 3: 13, 4: 18 } },
  Mirrorsage: { mode: "hybrid", maxRank: 7, learnLevels: { 0: 1, 1: 1, 2: 4, 3: 7, 4: 10, 5: 13, 6: 16, 7: 19 } },
  Oracle: { mode: "revelation", maxRank: 0, learnLevels: {} },
  Ranger: { mode: "half", maxRank: 5, learnLevels: { 0: 1, 1: 2, 2: 5, 3: 9, 4: 13, 5: 17 } },
  Shaman: { mode: "hybrid", maxRank: 7, learnLevels: { 0: 1, 1: 1, 2: 4, 3: 7, 4: 10, 5: 13, 6: 16, 7: 19 } },
  Soldier: { mode: "none", maxRank: 0, learnLevels: {} },
  Thief: { mode: "minor", maxRank: 4, learnLevels: { 0: 1, 1: 3, 2: 8, 3: 13, 4: 18 } },
  Tinker: { mode: "minor", maxRank: 5, learnLevels: { 0: 1, 1: 2, 2: 6, 3: 10, 4: 14, 5: 18 } },
  Warrior: { mode: "none", maxRank: 0, learnLevels: {} },
  Wizard: { mode: "full", maxRank: 9, learnLevels: { 0: 1, 1: 1, 2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 15, 9: 17 } },
  Paladin: { mode: "half", maxRank: 5, learnLevels: { 0: 2, 1: 2, 2: 5, 3: 9, 4: 13, 5: 17 } },
};

export function getClassSpellProgression(className) {
  return CLASS_SPELL_PROGRESSION[className] || { mode: "none", maxRank: 0, learnLevels: {} };
}

export function getLearnLevelForRank(className, rank) {
  const progression = getClassSpellProgression(className);
  const level = progression.learnLevels?.[rank];
  return Number.isInteger(level) ? level : null;
}

export default CLASS_SPELL_PROGRESSION;
