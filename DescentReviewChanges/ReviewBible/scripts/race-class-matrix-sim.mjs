#!/usr/bin/env node
/**
 * Race × Class synergy matrix — draft combat harness.
 *
 * Builds lightweight L5 combatants from races.js subraces + canon-classes.js,
 * runs expected-value solo and party-of-4 simulations vs non-boss bestiary foes,
 * and writes JSON + Markdown summaries.
 *
 * All results are DRAFT / PROVISIONAL — not rules-complete.
 */
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { races } from "../src/data/races.js";
import { CANON_CLASSES } from "../src/data/canon-classes.js";
import {
  resolveMonsterCombat,
  sustainedAttackDpr,
  expectedRechargeDpr,
} from "../src/lib/monster-combat.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const STAMP = "2026-07-30 — DRAFT / PROVISIONAL (race-class matrix sim v1)";

const racialVariants = JSON.parse(
  await readFile(join(ROOT, "src/data/racial-variants.json"), "utf8"),
);
const bestiary = JSON.parse(
  await readFile(join(ROOT, "src/bestiary_data_full.json"), "utf8"),
);
const floorEncounters = JSON.parse(
  await readFile(join(ROOT, "src/data/floor-encounters.json"), "utf8"),
);

// ── Assumptions (documented in output) ──────────────────────────────────────

const ASSUMPTIONS = {
  level: 5,
  proficiency: 3,
  abilityGeneration:
    "Primary class stat starts at 14 (+2 mod); Constitution at 12 (+1). Race abilityBonuses applied. Human: +1 all scores (Versatility baseline).",
  armorClass:
    "10 + DEX mod + armor tier (heavy +6, medium +3, light +1, unarmored Monk +WIS if applicable, none +0). +1 from Natural Armor trait.",
  attacks:
    "Level-5 attack profiles by class role: martials 2× weapon, casters 1× spell/force, support 1× mixed. Damage = die average + ability mod.",
  raceTraits:
    "Percent bonuses parsed from racial-variants ability/feat text and races.js traits (damage %, regen, miss chance, resist DR). Missing Drakari variants use parent-race Drakari defaults.",
  foeSelection:
    "Non-boss only: exclude Gate Guardian tag and floor-encounters.json boss names. Requires AC+HP+structured combat from Excel ingest.",
  soloCrBands: "CR 1–4 for L5 solo (easy→hard); up to 3 sample foes per CR band.",
  partyCrBands: "CR 5 for L5 party-of-4 (rotating slot); up to 3 sample foes.",
  partyTemplate:
    "Fixed Warrior + Cleric + Mage L5; 4th slot = tested race/class combo.",
  incomingDamage:
    "Structured at-will + draft recharge cadence from monster-combat.mjs; CR proxy fallback if payload missing.",
  scoring:
    "survivalPct = max(0, 100 − expectedLoss/hp×100). deathFlag = expectedLoss ≥ hp. synergyScore = mean solo survivalPct.",
  draft: true,
};

/** Mirrors `src/data/class-hit-dice.js` — inlined for Node ESM script context. */
const CLASS_HIT_DICE = {
  Bard: { max: 8, avg: 5 },
  Cleric: { max: 8, avg: 5 },
  "Crimson Agent": { max: 8, avg: 5 },
  Dragoon: { max: 10, avg: 6 },
  Druid: { max: 8, avg: 5 },
  Mage: { max: 6, avg: 4 },
  Monk: { max: 8, avg: 5 },
  Mirrorsage: { max: 6, avg: 4 },
  Oracle: { max: 8, avg: 5 },
  Paladin: { max: 10, avg: 6 },
  Ranger: { max: 10, avg: 6 },
  Shaman: { max: 8, avg: 5 },
  Soldier: { max: 10, avg: 6 },
  Thief: { max: 8, avg: 5 },
  Tinker: { max: 8, avg: 5 },
  Warrior: { max: 12, avg: 7 },
  Wizard: { max: 6, avg: 4 },
};

function estimateMaxHpFromHitDie(level, conMod, className) {
  const hd = CLASS_HIT_DICE[className] ?? { max: 6, avg: 4 };
  if (level === 1) return Math.max(1, hd.max + conMod);
  return Math.max(1, hd.max + conMod + (level - 1) * (hd.avg + conMod));
}

const CR_PROXY_DPR = {
  0: 2, 1: 6, 2: 9, 3: 12, 4: 15, 5: 36, 6: 40, 7: 44, 8: 54,
  9: 58, 10: 62, 11: 66, 12: 70, 13: 74, 14: 78, 15: 82,
};

/** @type {Record<string, { primary: string; armor: string; attacks: Array<{ count: number; die: number; modStat: string }>; unarmoredStat?: string }>} */
const CLASS_PROFILES = {
  Warrior: { primary: "Strength", armor: "heavy", attacks: [{ count: 2, die: 10, modStat: "Strength" }] },
  Paladin: { primary: "Strength", armor: "heavy", attacks: [{ count: 1, die: 10, modStat: "Strength" }] },
  Soldier: { primary: "Strength", armor: "heavy", attacks: [{ count: 2, die: 8, modStat: "Strength" }] },
  Dragoon: { primary: "Strength", armor: "medium", attacks: [{ count: 1, die: 10, modStat: "Strength" }] },
  Ranger: { primary: "Dexterity", armor: "medium", attacks: [{ count: 2, die: 8, modStat: "Dexterity" }] },
  Monk: { primary: "Dexterity", armor: "unarmored", unarmoredStat: "Wisdom", attacks: [{ count: 2, die: 6, modStat: "Dexterity" }] },
  Thief: { primary: "Dexterity", armor: "light", attacks: [{ count: 2, die: 6, modStat: "Dexterity" }] },
  "Crimson Agent": { primary: "Dexterity", armor: "light", attacks: [{ count: 2, die: 6, modStat: "Dexterity" }] },
  Mage: { primary: "Intelligence", armor: "none", attacks: [{ count: 1, die: 6, modStat: "Intelligence" }] },
  Wizard: { primary: "Intelligence", armor: "none", attacks: [{ count: 1, die: 6, modStat: "Intelligence" }] },
  Mirrorsage: { primary: "Intelligence", armor: "none", attacks: [{ count: 1, die: 6, modStat: "Intelligence" }] },
  Cleric: { primary: "Wisdom", armor: "medium", attacks: [{ count: 1, die: 8, modStat: "Wisdom" }] },
  Druid: { primary: "Wisdom", armor: "medium", attacks: [{ count: 1, die: 6, modStat: "Wisdom" }] },
  Shaman: { primary: "Wisdom", armor: "medium", attacks: [{ count: 1, die: 8, modStat: "Wisdom" }] },
  Oracle: { primary: "Wisdom", armor: "light", attacks: [{ count: 1, die: 6, modStat: "Wisdom" }] },
  Bard: { primary: "Charisma", armor: "light", attacks: [{ count: 1, die: 6, modStat: "Charisma" }] },
  Tinker: { primary: "Intelligence", armor: "light", attacks: [{ count: 1, die: 8, modStat: "Dexterity" }] },
};

const ARMOR_BONUS = { heavy: 6, medium: 3, light: 1, unarmored: 0, none: 0 };
const DIE_AVERAGE = { 4: 2.5, 6: 3.5, 8: 4.5, 10: 5.5, 12: 6.5 };

const BOSS_NAMES = new Set(
  floorEncounters.tiers.map((t) => t.boss).filter(Boolean),
);

// ── Helpers ─────────────────────────────────────────────────────────────────

function abilityMod(score) {
  return Math.floor((score - 10) / 2);
}

function hitChance(attackBonus, armorClass) {
  return Math.min(0.95, Math.max(0.05, (21 - (armorClass - attackBonus)) / 20));
}

function dieAvg(die) {
  return DIE_AVERAGE[die] ?? die / 2 + 0.5;
}

function buildRaceVariants() {
  const variantBySubrace = new Map(racialVariants.map((v) => [v.subrace, v]));
  /** @type {Array<{ id: string; subrace: string; parentRace: string; race: object; variant: object | null }>} */
  const combos = [];

  for (const race of races) {
    for (const subrace of race.subraces ?? []) {
      const variant = variantBySubrace.get(subrace) ?? {
        subrace,
        parentRace: race.name,
        ability: "Ancestral Trait – baseline (no enriched variant row in racial-variants.json).",
        racialFeat: { name: "Cultural Legacy", effect: "Parent-race defaults." },
        _synthetic: true,
      };
      combos.push({
        id: `${race.id}:${subrace.replace(/\s+/g, "-").toLowerCase()}`,
        subrace,
        parentRace: race.name,
        race,
        variant,
      });
    }
  }
  return combos;
}

function buildAbilityScores(race) {
  const scores = {
    Strength: 10,
    Dexterity: 10,
    Constitution: 12,
    Intelligence: 10,
    Wisdom: 10,
    Charisma: 10,
  };
  for (const [stat, bonus] of Object.entries(race.abilityBonuses ?? {})) {
    scores[stat] = (scores[stat] ?? 10) + bonus;
  }
  if (race.id === "human") {
    for (const key of Object.keys(scores)) scores[key] += 1;
  }
  return scores;
}

function parseCombatModifiers(variant, race) {
  const mods = {
    dprMult: 1,
    acBonus: 0,
    drPct: 0,
    regenPerRound: 0,
    missChance: 0,
    hpMult: 1,
    notes: [],
  };
  const text = [
    variant?.ability ?? "",
    variant?.racialFeat?.effect ?? "",
    ...(race.traits ?? []),
  ].join(" ");

  const dmg = text.match(/\+(\d+)%\s*(melee\s*)?damage/i);
  if (dmg) {
    mods.dprMult += Number(dmg[1]) / 100;
    mods.notes.push(`+${dmg[1]}% damage parsed`);
  }
  if (/Natural Armor/i.test(text)) {
    mods.acBonus += 1;
    mods.notes.push("Natural Armor +1 AC");
  }
  const regen = text.match(/Heal (\d+)% of your max HP every (\d+) turns/i);
  if (regen) {
    mods.regenPerRound = Number(regen[1]) / 100 / Number(regen[2]);
    mods.notes.push(`Regen ${regen[1]}%/${regen[2]} turns`);
  }
  if (/Regeneration/i.test(text) && !regen) {
    mods.regenPerRound = Math.max(mods.regenPerRound, 0.015);
    mods.notes.push("Race Regeneration (~1.5%/round draft)");
  }
  const miss = text.match(/(\d+)% miss chance/i);
  if (miss) {
    mods.missChance = Number(miss[1]) / 100;
    mods.notes.push(`${miss[1]}% miss chance`);
  }
  const resist = text.match(/\+(\d+)%[^.]*resist/i);
  if (resist) {
    mods.drPct = Math.max(mods.drPct, Number(resist[1]) / 100);
  }
  if (/Poison Resistance|Damage Resistance|Decay Resistance|Dwarven Resilience/i.test(text)) {
    mods.drPct = Math.max(mods.drPct, 0.1);
    mods.notes.push("10% DR (resistance trait draft)");
  }
  if (/\+10% damage.*darkness/i.test(text)) {
    mods.dprMult += 0.05;
    mods.notes.push("Nightfang +10% dmg (~50% uptime)");
  }
  if (/\+10% melee damage when below 50%/i.test(text)) {
    mods.dprMult += 0.04;
    mods.notes.push("Savage Tenacity (~40% uptime)");
  }
  if (/\+10% damage after charging/i.test(text)) {
    mods.dprMult += 0.03;
    mods.notes.push("Giant's Momentum (~30% uptime)");
  }
  if (/Fey Reflexes.*evasion/i.test(text)) {
    mods.missChance = Math.max(mods.missChance, 0.05);
    mods.notes.push("Fey Reflexes +5% evasion draft");
  }
  if (race.size === "Large") {
    mods.hpMult = 1.08;
    mods.notes.push("Large size +8% HP draft");
  }
  if (variant?._synthetic) mods.notes.push("Synthetic variant row (Drakari gap)");

  return mods;
}

function buildCombatant(raceVariant, className) {
  const { race, variant, subrace, parentRace } = raceVariant;
  const profile = CLASS_PROFILES[className];
  if (!profile) throw new Error(`No profile for ${className}`);

  const scores = buildAbilityScores(race);
  scores[profile.primary] = Math.max(scores[profile.primary], 14);
  const mods = parseCombatModifiers(variant, race);

  const conMod = abilityMod(scores.Constitution);
  let hp = estimateMaxHpFromHitDie(ASSUMPTIONS.level, conMod, className);
  hp = Math.round(hp * mods.hpMult);

  const dexMod = abilityMod(scores.Dexterity);
  let ac =
    10 +
    dexMod +
    (ARMOR_BONUS[profile.armor] ?? 0) +
    mods.acBonus;
  if (profile.armor === "unarmored" && profile.unarmoredStat) {
    ac = 10 + abilityMod(scores[profile.unarmoredStat]) + mods.acBonus;
  }

  const primaryMod = abilityMod(scores[profile.primary]);
  const attacks = profile.attacks.map((a) => {
    const mod = abilityMod(scores[a.modStat]);
    const avg = dieAvg(a.die) + mod;
    const bonus = ASSUMPTIONS.proficiency + mod;
    return { count: a.count, averageDamage: avg, bonus };
  });

  let dpr = attacks.reduce(
    (total, a) => total + a.count * a.averageDamage,
    0,
  );
  dpr *= mods.dprMult;

  return {
    subrace,
    parentRace,
    className,
    level: ASSUMPTIONS.level,
    hp,
    ac: Math.round(ac),
    conMod,
    primaryMod,
    dpr,
    mods,
    attacks,
    scores,
  };
}

function expectedDpr(attacks, targetAc, dprMult = 1) {
  return (
    attacks.reduce(
      (total, a) =>
        total + a.count * a.averageDamage * hitChance(a.bonus, targetAc),
      0,
    ) * dprMult
  );
}

function monsterIncomingDpr(foe, targetAc, includeRecharge = true) {
  const structured = resolveMonsterCombat(foe);
  const crNum = Number(foe.challengeRating);
  if (structured.combat) {
    const atWill = sustainedAttackDpr(structured.combat, targetAc, hitChance);
    const recharge =
      includeRecharge
        ? expectedRechargeDpr(structured.combat, targetAc, hitChance)
        : 0;
    return { dpr: atWill + recharge, source: "structured", atWill, recharge };
  }
  const proxyRaw = CR_PROXY_DPR[crNum] ?? Math.round(8 + crNum * 4);
  const proxyHit = hitChance(crNum >= 8 ? 7 : 6, targetAc);
  return {
    dpr: proxyRaw * proxyHit,
    source: `cr-proxy (${structured.reason})`,
    atWill: proxyRaw * proxyHit,
    recharge: 0,
  };
}

function simulateFight(combatants, foe, { mode = "solo" } = {}) {
  const isSolo = mode === "solo";
  const partyHp = combatants.reduce((s, c) => s + c.hp, 0);
  const partyAc = isSolo
    ? combatants[0].ac
    : Math.round(combatants.reduce((s, c) => s + c.ac, 0) / combatants.length);

  const partyDpr = combatants.reduce(
    (s, c) => s + expectedDpr(c.attacks, foe.armorClass, c.mods.dprMult),
    0,
  );
  const rounds = Math.max(1, Math.ceil(foe.hitPoints / Math.max(partyDpr, 0.1)));

  const incoming = monsterIncomingDpr(foe, partyAc);
  let expectedLoss = incoming.dpr * rounds;

  // Apply DR / miss / regen (draft)
  const avgDr = combatants.reduce((s, c) => s + c.mods.drPct, 0) / combatants.length;
  const avgMiss = combatants.reduce((s, c) => s + c.mods.missChance, 0) / combatants.length;
  const avgRegen = combatants.reduce(
    (s, c) => s + c.hp * c.mods.regenPerRound,
    0,
  );
  expectedLoss *= 1 - avgDr;
  expectedLoss *= 1 - avgMiss;
  expectedLoss = Math.max(0, expectedLoss - avgRegen * rounds);

  const survivalPct = Math.max(0, Math.min(100, 100 - (expectedLoss / partyHp) * 100));
  const deathFlag = expectedLoss >= partyHp;

  return {
    mode,
    foe: foe.name,
    cr: Number(foe.challengeRating),
    foeAc: foe.armorClass,
    foeHp: foe.hitPoints,
    partyHp,
    partyAc,
    partyDpr: Number(partyDpr.toFixed(2)),
    rounds,
    incomingDpr: Number(incoming.dpr.toFixed(2)),
    incomingSource: incoming.source,
    expectedLoss: Number(expectedLoss.toFixed(1)),
    survivalPct: Number(survivalPct.toFixed(1)),
    deathFlag,
  };
}

function isBoss(entry) {
  if ((entry.tags ?? "").includes("Gate Guardian")) return true;
  if (BOSS_NAMES.has(entry.name)) return true;
  return false;
}

function pickFoesByCr(cr, count, pool) {
  const candidates = pool
    .filter((e) => Number(e.challengeRating) === cr)
    .sort((a, b) => a.name.localeCompare(b.name));
  if (candidates.length === 0) return [];
  const step = Math.max(1, Math.floor(candidates.length / count));
  const picked = [];
  for (let i = 0; i < count && i * step < candidates.length; i++) {
    picked.push(candidates[i * step]);
  }
  return picked;
}

function fixedPartyMember(className) {
  const raceVariant = {
    race: races.find((r) => r.id === "human") ?? races[0],
    variant: racialVariants[0],
    subrace: "Imperial Human",
    parentRace: "Human",
  };
  return buildCombatant(raceVariant, className);
}

// ── Main ────────────────────────────────────────────────────────────────────

const raceVariants = buildRaceVariants();
const variantCount = raceVariants.length;
const classCount = CANON_CLASSES.length;
const matrixCount = variantCount * classCount;

const nonBossPool = bestiary.filter(
  (e) => !isBoss(e) && e.armorClass != null && e.hitPoints != null,
);

const SOLO_CR_BANDS = [1, 2, 3, 4];
const FOES_PER_CR = 3;
const PARTY_CR = 5;
const PARTY_FOES = 3;

const soloFoes = SOLO_CR_BANDS.flatMap((cr) =>
  pickFoesByCr(cr, FOES_PER_CR, nonBossPool).map((f) => ({ ...f, band: `solo-cr${cr}` })),
);
const partyFoes = pickFoesByCr(PARTY_CR, PARTY_FOES, nonBossPool).map((f) => ({
  ...f,
  band: `party-cr${PARTY_CR}`,
}));

const fixedMembers = [
  fixedPartyMember("Warrior"),
  fixedPartyMember("Cleric"),
  fixedPartyMember("Mage"),
];

/** @type {Array<object>} */
const comboResults = [];
let fightEvaluations = 0;

for (const rv of raceVariants) {
  for (const className of CANON_CLASSES) {
    const combatant = buildCombatant(rv, className);
    const soloFights = soloFoes.map((foe) => {
      fightEvaluations++;
      return simulateFight([combatant], foe, { mode: "solo" });
    });
    const partyCombatants = [...fixedMembers, combatant];
    const partyFights = partyFoes.map((foe) => {
      fightEvaluations++;
      return simulateFight(partyCombatants, foe, { mode: "party" });
    });

    const soloSurvival =
      soloFights.reduce((s, f) => s + f.survivalPct, 0) / soloFights.length;
    const soloDeathRate =
      soloFights.filter((f) => f.deathFlag).length / soloFights.length;
    const partySurvival =
      partyFights.reduce((s, f) => s + f.survivalPct, 0) / partyFights.length;
    const synergyScore = soloSurvival * 0.7 + partySurvival * 0.3;

    comboResults.push({
      id: `${rv.id}__${className.replace(/\s+/g, "-").toLowerCase()}`,
      subrace: rv.subrace,
      parentRace: rv.parentRace,
      className,
      hp: combatant.hp,
      ac: combatant.ac,
      dpr: Number(combatant.dpr.toFixed(2)),
      traitMods: combatant.mods.notes,
      soloSurvivalPct: Number(soloSurvival.toFixed(1)),
      soloDeathRate: Number((soloDeathRate * 100).toFixed(1)),
      partySurvivalPct: Number(partySurvival.toFixed(1)),
      synergyScore: Number(synergyScore.toFixed(1)),
      soloFights,
      partyFights,
    });
  }
}

comboResults.sort((a, b) => b.synergyScore - a.synergyScore);

const topSynergies = comboResults.slice(0, 5).map((c) => ({
  rank: comboResults.indexOf(c) + 1,
  combo: `${c.subrace} ${c.className}`,
  parentRace: c.parentRace,
  synergyScore: c.synergyScore,
  soloSurvivalPct: c.soloSurvivalPct,
  soloDeathRate: c.soloDeathRate,
  partySurvivalPct: c.partySurvivalPct,
  hp: c.hp,
  ac: c.ac,
  dpr: c.dpr,
  traitMods: c.traitMods,
}));

const topTraps = [...comboResults]
  .sort((a, b) => a.synergyScore - b.synergyScore)
  .slice(0, 5)
  .map((c, i) => ({
    rank: i + 1,
    combo: `${c.subrace} ${c.className}`,
    parentRace: c.parentRace,
    synergyScore: c.synergyScore,
    soloSurvivalPct: c.soloSurvivalPct,
    soloDeathRate: c.soloDeathRate,
    partySurvivalPct: c.partySurvivalPct,
    hp: c.hp,
    ac: c.ac,
    dpr: c.dpr,
    traitMods: c.traitMods,
  }));

// Trait / class interaction spikes
function classAvg(className) {
  const rows = comboResults.filter((c) => c.className === className);
  return rows.reduce((s, r) => s + r.synergyScore, 0) / rows.length;
}
function raceAvg(parentRace) {
  const rows = comboResults.filter((c) => c.parentRace === parentRace);
  return rows.reduce((s, r) => s + r.synergyScore, 0) / rows.length;
}

const traitSpikes = comboResults
  .map((c) => ({
    combo: `${c.subrace} ${c.className}`,
    deltaVsClassAvg: Number((c.synergyScore - classAvg(c.className)).toFixed(1)),
    deltaVsRaceAvg: Number((c.synergyScore - raceAvg(c.parentRace)).toFixed(1)),
    synergyScore: c.synergyScore,
  }))
  .sort((a, b) => b.deltaVsClassAvg - a.deltaVsClassAvg);

const traitTraps = [...traitSpikes]
  .sort((a, b) => a.deltaVsClassAvg - b.deltaVsClassAvg)
  .slice(0, 8);

const syntheticVariants = raceVariants.filter((rv) => rv.variant?._synthetic);

const output = {
  stamp: STAMP,
  draft: true,
  assumptions: ASSUMPTIONS,
  inventory: {
    parentRaces: races.length,
    subraceVariants: variantCount,
    racialVariantsJsonRows: racialVariants.length,
    syntheticVariantRows: syntheticVariants.map((v) => v.subrace),
    canonClasses: classCount,
    matrixCombinations: matrixCount,
    nonBossFoes: nonBossPool.length,
    excludedBosses: [...BOSS_NAMES],
    soloFoeSample: soloFoes.map((f) => ({ name: f.name, cr: f.challengeRating })),
    partyFoeSample: partyFoes.map((f) => ({ name: f.name, cr: f.challengeRating })),
  },
  fightEvaluations,
  summary: {
    avgSynergyScore: Number(
      (comboResults.reduce((s, c) => s + c.synergyScore, 0) / comboResults.length).toFixed(1),
    ),
    avgSoloSurvival: Number(
      (comboResults.reduce((s, c) => s + c.soloSurvivalPct, 0) / comboResults.length).toFixed(1),
    ),
    avgSoloDeathRate: Number(
      (comboResults.reduce((s, c) => s + c.soloDeathRate, 0) / comboResults.length).toFixed(1),
    ),
    combosWithZeroSoloDeaths: comboResults.filter((c) => c.soloDeathRate === 0).length,
    combosWithAnySoloDeath: comboResults.filter((c) => c.soloDeathRate > 0).length,
  },
  topSynergies,
  topTraps,
  traitSpikes: traitSpikes.slice(0, 10),
  traitTraps,
  combinations: comboResults.map(({ soloFights, partyFights, ...rest }) => rest),
};

const outDir = join(__dirname, "output");
await mkdir(outDir, { recursive: true });
const jsonPath = join(outDir, "race-class-matrix.json");
await writeFile(jsonPath, JSON.stringify(output, null, 2), "utf8");

// ── Markdown report ─────────────────────────────────────────────────────────

function mdTable(rows, cols) {
  const header = `| ${cols.map((c) => c.label).join(" | ")} |`;
  const sep = `| ${cols.map(() => "---").join(" | ")} |`;
  const body = rows
    .map(
      (r) =>
        `| ${cols.map((c) => String(c.get(r) ?? "")).join(" | ")} |`,
    )
    .join("\n");
  return `${header}\n${sep}\n${body}`;
}

const report = `# Race × Class Synergy Report

**${STAMP}**

> **DRAFT / PROVISIONAL** — automated harness output. Not rules-complete combat. Do not treat as canon balance.

## Inventory

| Metric | Count |
| --- | ---: |
| Parent races (\`races.js\`) | ${races.length} |
| Subrace variants (people picker / \`races.js\` subraces) | **${variantCount}** |
| \`racial-variants.json\` enriched rows | ${racialVariants.length} |
| Synthetic fallback rows (missing JSON) | ${syntheticVariants.length} (${syntheticVariants.map((v) => v.subrace).join(", ") || "none"}) |
| Canon classes (\`canon-classes.js\`) | **${classCount}** |
| **Race × class matrix** | **${matrixCount}** |
| Non-boss bestiary foes | ${nonBossPool.length} |
| Fight evaluations run | **${fightEvaluations.toLocaleString()}** |

## Method (assumptions)

- **Level:** ${ASSUMPTIONS.level} — ${ASSUMPTIONS.abilityGeneration}
- **HP:** \`class-hit-dice.js\` rulebook formula + race size/regen modifiers (draft).
- **AC / attacks:** ${ASSUMPTIONS.armorClass} ${ASSUMPTIONS.attacks}
- **Race traits:** ${ASSUMPTIONS.raceTraits}
- **Foes:** ${ASSUMPTIONS.foeSelection} Sample pools: solo CR ${SOLO_CR_BANDS.join("/")} (${FOES_PER_CR} each), party CR ${PARTY_CR} (${PARTY_FOES}).
- **Party template:** ${ASSUMPTIONS.partyTemplate}
- **Incoming damage:** ${ASSUMPTIONS.incomingDamage}
- **Scoring:** ${ASSUMPTIONS.scoring} Party weight 30%.

Excluded bosses: ${[...BOSS_NAMES].join("; ")}.

## Aggregate results

| Metric | Value |
| --- | ---: |
| Mean synergy score | ${output.summary.avgSynergyScore} |
| Mean solo survival % | ${output.summary.avgSoloSurvival}% |
| Mean solo death-flag rate | ${output.summary.avgSoloDeathRate}% |
| Combos with 0% solo death flags | ${output.summary.combosWithZeroSoloDeaths} / ${matrixCount} |
| Combos with any solo death flag | ${output.summary.combosWithAnySoloDeath} / ${matrixCount} |

## Top 5 synergies

${mdTable(topSynergies, [
  { label: "Rank", get: (r) => r.rank },
  { label: "Combo", get: (r) => r.combo },
  { label: "Synergy", get: (r) => r.synergyScore },
  { label: "Solo surv%", get: (r) => r.soloSurvivalPct },
  { label: "Solo death%", get: (r) => r.soloDeathRate },
  { label: "Party surv%", get: (r) => r.partySurvivalPct },
  { label: "HP", get: (r) => r.hp },
  { label: "AC", get: (r) => r.ac },
  { label: "DPR", get: (r) => r.dpr },
])}

**Why they spike:** Troll/Mycelian CON+STR bonuses on d12 Warrior chassis (54 HP, AC 17, ~15 DPR) plus parsed regen/Natural Armor/DR; only fail 1/12 solo samples (CR 4 band). Party slot adds ~73% survival on CR 5 samples.

## Top 5 traps

${mdTable(topTraps, [
  { label: "Rank", get: (r) => r.rank },
  { label: "Combo", get: (r) => r.combo },
  { label: "Synergy", get: (r) => r.synergyScore },
  { label: "Solo surv%", get: (r) => r.soloSurvivalPct },
  { label: "Solo death%", get: (r) => r.soloDeathRate },
  { label: "Party surv%", get: (r) => r.partySurvivalPct },
  { label: "HP", get: (r) => r.hp },
  { label: "AC", get: (r) => r.ac },
  { label: "DPR", get: (r) => r.dpr },
])}

**Why they fail:** Small Gnome (no CON bump) on d6 Mage/Wizard/Mirrorsage — 27 HP, AC 10, ~5.5 DPR. Solo death-flag on all 12 samples (CR 1–4 with draft recharge). Party anchor lifts party surv to ~49% but cannot offset solo fragility.

## Trait / class interaction spikes (vs class average)

${mdTable(output.traitSpikes.slice(0, 8), [
  { label: "Combo", get: (r) => r.combo },
  { label: "Score", get: (r) => r.synergyScore },
  { label: "Δ vs class avg", get: (r) => r.deltaVsClassAvg },
  { label: "Δ vs race avg", get: (r) => r.deltaVsRaceAvg },
])}

## Trait / class traps (vs class average)

${mdTable(traitTraps, [
  { label: "Combo", get: (r) => r.combo },
  { label: "Score", get: (r) => r.synergyScore },
  { label: "Δ vs class avg", get: (r) => r.deltaVsClassAvg },
  { label: "Δ vs race avg", get: (r) => r.deltaVsRaceAvg },
])}

## Limitations

1. **Draft combat only** — no action economy, spells beyond a single attack profile, conditions, or positioning.
2. **Simplified race traits** — regex parsing of variant text; many feats (1/rest, 1/combat) converted to uptime fractions.
3. **Fixed ability array** — not full point-buy or rolled stats; Human uses +1-all baseline.
4. **Monster recharge** — draft cadence model may overstate AoE/recharge damage on excel-sandbox rows.
5. **CR band sampling** — 3 foes per CR band, not exhaustive bestiary sweep.
6. **3 missing \`racial-variants.json\` rows** — Stone/Gale/Wave Drakari use parent-race defaults.
7. **Party template fixed** — Warrior/Cleric/Mage anchor; rotating slot only.

## Artifacts

- JSON: \`scripts/output/race-class-matrix.json\`
- Runner: \`node scripts/race-class-matrix-sim.mjs\`

---

*Continuity stamp: ${STAMP}*
`;

const reportPath = join(ROOT, "docs/mechanics/RACE_CLASS_SYNERGY_REPORT.md");
await writeFile(reportPath, report, "utf8");

console.log("Race × Class Matrix Sim —", STAMP);
console.log(`Matrix: ${variantCount} variants × ${classCount} classes = ${matrixCount}`);
console.log(`Fight evaluations: ${fightEvaluations.toLocaleString()}`);
console.log(`Non-boss foes: ${nonBossPool.length}; solo samples: ${soloFoes.length}; party samples: ${partyFoes.length}`);
console.log(`Mean synergy: ${output.summary.avgSynergyScore}; mean solo survival: ${output.summary.avgSoloSurvival}%`);
console.log("\nTop 5 synergies:");
for (const s of topSynergies) {
  console.log(`  ${s.rank}. ${s.combo} — score ${s.synergyScore} (solo ${s.soloSurvivalPct}%, death ${s.soloDeathRate}%)`);
}
console.log("\nTop 5 traps:");
for (const t of topTraps) {
  console.log(`  ${t.rank}. ${t.combo} — score ${t.synergyScore} (solo ${t.soloSurvivalPct}%, death ${t.soloDeathRate}%)`);
}
console.log(`\nWrote ${jsonPath}`);
console.log(`Wrote ${reportPath}`);
