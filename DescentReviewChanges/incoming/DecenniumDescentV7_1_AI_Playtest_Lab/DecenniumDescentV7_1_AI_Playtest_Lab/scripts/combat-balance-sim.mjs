#!/usr/bin/env node
/**
 * Deterministic combat-balance sanity check for Decennium Descent.
 *
 * Reads the companion bestiary. Player HP uses the published hit-die rule
 * (max die + CON at L1, average die + CON each later level). Uses structured
 * at-will actions when present; otherwise a visible CR proxy.
 */
import { readFile } from "node:fs/promises";
import {
  resolveMonsterCombat,
  sustainedAttackDpr,
  expectedRechargeDpr,
  totalExpectedMonsterDpr,
  listRechargeAttacks,
} from "../src/lib/monster-combat.mjs";

const bestiary = JSON.parse(
  await readFile(new URL("../src/bestiary_data_full.json", import.meta.url), "utf8"),
);

const HIT_DICE = {
  Bard: [8, 5], Cleric: [8, 5], "Crimson Agent": [8, 5], Dragoon: [10, 6],
  Druid: [8, 5], Mage: [6, 4], Monk: [8, 5], Mirrorsage: [6, 4],
  Oracle: [8, 5], Paladin: [10, 6], Ranger: [10, 6], Shaman: [8, 5],
  Soldier: [10, 6], Thief: [8, 5], Tinker: [8, 5], Warrior: [12, 7],
  Wizard: [6, 4],
};

const CR_PROXY_DPR = {
  0: 2, 1: 6, 2: 9, 3: 12, 4: 15, 5: 36, 6: 40, 7: 44, 8: 54,
  9: 58, 10: 62, 11: 66, 12: 70, 13: 74, 14: 78, 15: 82,
};

function hp(className, level, conMod) {
  const [max, average] = HIT_DICE[className];
  return max + conMod + (level - 1) * (average + conMod);
}

function hitChance(attackBonus, armorClass) {
  return Math.min(0.95, Math.max(0.05, (21 - (armorClass - attackBonus)) / 20));
}

function monster(name) {
  const matches = bestiary.filter((entry) => entry.name === name);
  if (matches.length === 0) throw new Error(`Missing monster: ${name}`);
  return matches.sort((left, right) => (right.hitPoints ?? 0) - (left.hitPoints ?? 0))[0];
}

function pickByCr(targetCr, typeFilter) {
  const crNum = Number(targetCr);
  const candidates = bestiary.filter((entry) => {
    const cr = Number(entry.challengeRating);
    if (Number.isNaN(cr) || cr !== crNum) return false;
    if (typeFilter && !String(entry.type).toLowerCase().includes(typeFilter)) return false;
    return entry.hitPoints != null && entry.armorClass != null;
  });
  if (candidates.length === 0) return null;
  candidates.sort((a, b) => a.name.localeCompare(b.name));
  return candidates[Math.floor(candidates.length / 2)];
}

const withCombatStats = bestiary.filter(
  (entry) => entry.hitPoints != null && entry.armorClass != null,
).length;
const withStructuredCombat = bestiary.filter(
  (entry) => resolveMonsterCombat(entry).combat,
).length;
const sandboxCombat = bestiary.filter(
  (entry) => entry.combat?.source === "excel-sandbox",
).length;

const withRecharge = bestiary.filter(
  (entry) => resolveMonsterCombat(entry).combat
    && listRechargeAttacks(resolveMonsterCombat(entry).combat).length > 0,
).length;

console.log("Decennium Descent combat balance simulation");
console.log(
  `Bestiary ingest: ${bestiary.length} entries; ${withCombatStats} have AC/HP; ${withStructuredCombat} with structured combat (${sandboxCombat} excel-sandbox drafts); ${withRecharge} with recharge payloads.`,
);
console.log(
  "Incoming damage prefers structured at-will actions; recharge uses draft cadence model when authored.",
);
console.log(
  "Recharge assumptions: available round 1; steady-state P(recharge)=roll success; save fail 55%, half on success; area=single-target expected.",
);

function expectedDpr(attacks, targetAc) {
  return attacks.reduce(
    (total, attack) => total + attack.count * attack.averageDamage * hitChance(attack.bonus, targetAc),
    0,
  );
}

function party(level, members, targetAc) {
  const resolved = members.map((member) => ({
    ...member,
    hp: hp(member.className, level, member.conMod),
    dpr: expectedDpr(member.attacks, targetAc),
  }));
  return {
    members: resolved,
    hp: resolved.reduce((total, member) => total + member.hp, 0),
    dpr: resolved.reduce((total, member) => total + member.dpr, 0),
  };
}

function format(value, digits = 1) {
  return Number(value).toFixed(digits);
}

function encounter({ label, level, monsterName, members, partyAc, note, includeRecharge = true }) {
  const foe = monster(monsterName);
  const group = party(level, members, foe.armorClass);
  const rounds = Math.max(1, Math.ceil(foe.hitPoints / Math.max(group.dpr, 0.1)));
  const structured = resolveMonsterCombat(foe);
  const crNum = Number(foe.challengeRating);
  const proxyRawDpr = CR_PROXY_DPR[crNum] ?? Math.round(8 + crNum * 4);
  const proxyHitChance = hitChance(crNum >= 8 ? 7 : 6, partyAc);
  const atWillDpr = structured.combat
    ? sustainedAttackDpr(structured.combat, partyAc, hitChance)
    : proxyRawDpr * proxyHitChance;
  const rechargeDpr = structured.combat && includeRecharge
    ? expectedRechargeDpr(structured.combat, partyAc, hitChance)
    : 0;
  const incomingDpr = atWillDpr + rechargeDpr;
  const expectedLoss = incomingDpr * rounds;
  const pct = expectedLoss / group.hp * 100;
  const xpEach = foe.xp / members.length;
  const rechargeCount = structured.combat ? listRechargeAttacks(structured.combat).length : 0;
  const incomingSource = structured.combat
    ? `draft at-will "${structured.combat.defaultActionId}"${rechargeCount && includeRecharge ? ` + ${rechargeCount} recharge (draft cadence)` : ""}`
    : `CR proxy (${structured.reason})`;
  const tooHot = expectedLoss >= group.hp;
  const verdict = tooHot ? "TOO HOT (likely TPK)" : pct >= 70 ? "very hard" : pct >= 40 ? "hard but survivable" : "moderate";

  console.log(`\n${label}`);
  if (note) console.log(`  Note: ${note}`);
  console.log(`  Foe: ${foe.name} — CR ${foe.challengeRating}, AC ${foe.armorClass}, HP ${foe.hitPoints}, ${foe.xp} XP`);
  console.log(`  Party: ${members.map((m) => `${m.className} ${hp(m.className, level, m.conMod)} HP`).join("; ")}`);
  console.log(`  Party DPR: ${format(group.dpr)} vs AC ${foe.armorClass}; win ~${rounds} rounds`);
  if (structured.combat && rechargeCount && includeRecharge) {
    console.log(`  Enemy at-will: ${format(atWillDpr)} DPR; recharge expected: ${format(rechargeDpr)} DPR`);
  }
  console.log(`  Enemy loss (${incomingSource}): ${format(incomingDpr)} DPR × ${rounds} = ${format(expectedLoss)} HP (${format(pct)}% party HP)`);
  console.log(`  XP split: ${format(xpEach, 0)} each`);
  console.log(`  Verdict: ${verdict}; all draft — not final balance.`);

  return {
    label, pct, tooHot, rounds, incomingDpr, atWillDpr, rechargeDpr,
    structured: Boolean(structured.combat), hasRecharge: rechargeCount > 0,
  };
}

const level3Party = [
  { className: "Warrior", conMod: 2, attacks: [{ count: 1, averageDamage: 8.5, bonus: 5 }] },
  { className: "Paladin", conMod: 2, attacks: [{ count: 1, averageDamage: 7.5, bonus: 5 }] },
  { className: "Cleric", conMod: 1, attacks: [{ count: 1, averageDamage: 4.5, bonus: 5 }] },
  { className: "Mage", conMod: 1, attacks: [{ count: 1, averageDamage: 6.5, bonus: 5 }] },
];

const level5Party = [
  { className: "Warrior", conMod: 3, attacks: [{ count: 2, averageDamage: 9.5, bonus: 7 }] },
  { className: "Paladin", conMod: 2, attacks: [{ count: 1, averageDamage: 8.5, bonus: 7 }] },
  { className: "Cleric", conMod: 1, attacks: [{ count: 1, averageDamage: 4.5, bonus: 7 }] },
  { className: "Ranger", conMod: 2, attacks: [{ count: 2, averageDamage: 7.5, bonus: 7 }] },
];

const level8Party = [
  { className: "Warrior", conMod: 3, attacks: [{ count: 2, averageDamage: 9.5, bonus: 7 }] },
  { className: "Paladin", conMod: 2, attacks: [{ count: 2, averageDamage: 8.5, bonus: 7 }] },
  { className: "Cleric", conMod: 1, attacks: [{ count: 1, averageDamage: 4.5, bonus: 7 }] },
  { className: "Mage", conMod: 1, attacks: [{ count: 1, averageDamage: 10.5, bonus: 99 }] },
];

const results = [];

results.push(encounter({
  label: "Scenario 1 — L3 party vs gate guardian (CR 5)",
  level: 3,
  monsterName: "The Bloom That Hungers",
  members: level3Party,
  partyAc: 15,
  note: "Authored guardian; includes Spore Burst recharge (draft cadence)",
}));

results.push(encounter({
  label: "Scenario 2 — L8 party vs gate guardian (CR 8)",
  level: 8,
  monsterName: "Vaskor, the Stone Maw",
  members: level8Party,
  partyAc: 16,
  note: "Authored guardian",
}));

const cr1Sample = pickByCr(1);
if (cr1Sample) {
  results.push(encounter({
    label: `Scenario 3 — L3 party vs CR 1 sandbox (${cr1Sample.name})`,
    level: 3,
    monsterName: cr1Sample.name,
    members: level3Party,
    partyAc: 15,
    note: "excel-sandbox draft band",
  }));
}

const cr3Sample = pickByCr(3);
if (cr3Sample) {
  results.push(encounter({
    label: `Scenario 4 — L5 party vs CR 3 sandbox (${cr3Sample.name})`,
    level: 5,
    monsterName: cr3Sample.name,
    members: level5Party,
    partyAc: 15,
    note: "excel-sandbox draft band",
  }));
}

const cr5Sample = pickByCr(5, "beast");
if (cr5Sample && cr5Sample.name !== "The Bloom That Hungers") {
  results.push(encounter({
    label: `Scenario 5 — L5 party vs CR 5 beast sandbox (${cr5Sample.name})`,
    level: 5,
    monsterName: cr5Sample.name,
    members: level5Party,
    partyAc: 15,
    note: "Compare to Bloom guardian",
  }));
}

const cr10Sample = pickByCr(10);
if (cr10Sample) {
  results.push(encounter({
    label: `Scenario 6 — L8 party vs CR 10 sandbox (${cr10Sample.name})`,
    level: 8,
    monsterName: cr10Sample.name,
    members: level8Party,
    partyAc: 16,
    note: "High-CR sandbox band",
  }));
}

console.log("\n=== Recharge enrichment summary ===");
const enriched = results.filter((r) => r.hasRecharge);
for (const r of enriched) {
  console.log(`  ${r.label.split("—").pop()?.trim() ?? r.label}: at-will ${format(r.atWillDpr)} + recharge ${format(r.rechargeDpr)} DPR → ${format(r.pct)}% party loss`);
}
console.log(`  Scenarios with recharge: ${enriched.length}/${results.length}`);

console.log("\n=== CR band summary ===");
const sandboxResults = results.filter((r) => r.label.includes("sandbox"));
const tooHotCount = sandboxResults.filter((r) => r.tooHot).length;
const avgPct = sandboxResults.length
  ? sandboxResults.reduce((s, r) => s + r.pct, 0) / sandboxResults.length
  : 0;
console.log(`  Sandbox scenarios: ${sandboxResults.length}; TPK-likely: ${tooHotCount}; avg party-loss %: ${format(avgPct)}%`);
console.log("  Target band for draft tuning: 40–70% party HP loss over expected fight length.");
console.log("  Gate guardians Bloom/Vaskor should remain in band; sandbox CR bands are sanity checks only.");

const level5MageHp = hp("Mage", 5, 1);
const level5WarriorHp = hp("Warrior", 5, 3);
const mageSustained = expectedDpr([{ count: 1, averageDamage: 6.5, bonus: 7 }], 15);
const mageBurst = 10.5;
const warriorDpr = expectedDpr([{ count: 2, averageDamage: 9.5, bonus: 7 }], 15);
console.log("\nScenario 7 — L5 glass-cannon caster vs martial (AC 15)");
console.log(`  Mage: ${level5MageHp} HP; sustained ${format(mageSustained)} DPR; burst ${format(mageBurst)} DPR.`);
console.log(`  Warrior: ${level5WarriorHp} HP; ${format(warriorDpr)} DPR.`);
console.log(`  Mage HP is ${format(level5MageHp / level5WarriorHp * 100)}% of Warrior; sustained DPR ${format(mageSustained / warriorDpr * 100)}%.`);

console.log("\nScenario 8 — XP outcome");
console.log("  Simulations split listed `xp` evenly among four PCs.");
console.log("  No encounter-award formula encoded; equal split is illustrative only.");
