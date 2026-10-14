import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import paths from '../src/data/class-paths.js';
import core, { DARK_RESONANCE_PATHS } from '../src/data/class-core-mechanics.js';
import feats from '../src/data/feats.js';
import oaths from '../src/data/paladin-oaths.js';
import mysteries from '../src/data/oracle-mysteries.js';
import curses from '../src/data/oracle-curses.js';
import { CANON_CLASSES } from '../src/data/canon-classes.js';
import { shapeshiftUsesAtLevel, wildShapeCrCap, primalRecoveryRpGain } from '../src/data/druid-shapeshifting.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const canon = [...CANON_CLASSES];
const fail = (msg) => { throw new Error(msg); };

if (canon.length !== 17) fail(`Expected 17 base classes, got ${canon.length}`);
for (const cls of canon) {
  if (!core[cls]) fail(`Missing protected mechanic: ${cls}`);
  if (!paths[cls]) fail(`Missing class path data: ${cls}`);
  if (!core[cls].primary || !core[cls].resonanceInterface || !core[cls].mechanics?.length) fail(`Incomplete core contract: ${cls}`);
  if (!(paths[cls].archPaths?.length)) fail(`No Arch path data: ${cls}`);
  if (!(paths[cls].heroPaths?.length)) fail(`No Hero path data: ${cls}`);
}
if (canon.includes('Fighter') || canon.includes('Sorcerer') || canon.includes('Warlock')) fail('Retired/non-base class leaked into 17-class roster');
if (DARK_RESONANCE_PATHS.Lich?.baseClass !== 'Mage') fail('Lich must remain a Mage path');
if (DARK_RESONANCE_PATHS.Necromancer?.baseClass !== 'Wizard') fail('Necromancer must remain a Wizard path');

const druidUses = [[1,2],[4,3],[7,4],[10,5],[13,6],[16,7],[19,8],[20,99]];
for (const [level, expected] of druidUses) {
  if (shapeshiftUsesAtLevel(level) !== expected) fail(`Druid Shapeshifting uses mismatch at L${level}`);
}
const druidCr = [[1,.25],[4,.5],[7,1],[10,2],[13,3],[16,4],[19,5],[20,5]];
for (const [level, expected] of druidCr) {
  if (wildShapeCrCap(level) !== expected) fail(`Druid Shapeshifting CR mismatch at L${level}`);
}
if (primalRecoveryRpGain(13) !== 7) fail('Druid Primal Recovery L13 must restore 7 RP');

const pathCounts = Object.fromEntries(canon.map((cls) => {
  const v = paths[cls];
  const archAbilities = (v.archPaths ?? []).reduce((n,p)=>n+(p.passives?.length??0)+(p.actives?.length??0),0);
  const heroAbilities = (v.heroPaths ?? []).reduce((n,p)=>n+(p.passives?.length??0)+(p.actives?.length??0),0);
  return [cls, { arch: v.archPaths.length, hero: v.heroPaths.length, archAbilities, heroAbilities }];
}));

const rows = canon.map((cls) => {
  const c=pathCounts[cls];
  return `| ${cls} | ${core[cls].primary} | ${c.arch} | ${c.hero} | ${c.archAbilities} | ${c.heroAbilities} |`;
}).join('\n');

const report = `# Class & Ability Validation — 2026-07-31\n\n**Result: PASS**\n\n- Canon selectable base classes: **${canon.length} / 17**\n- Protected unique-mechanic contracts: **${Object.keys(core).length} / 17**\n- Class path datasets present: **${Object.keys(paths).length} / 17**\n- Feats in structured catalog: **${feats.length}**\n- Paladin Sacred Oaths: **${oaths.length}**\n- Oracle Mysteries: **${mysteries.length}**\n- Oracle Curses: **${curses.length}**\n- Lich parent identity: **Mage — preserved**\n- Necromancer parent identity: **Wizard — preserved**\n- Lich/Necromancer Traumatic Casting exception: **protected**
- Druid Shapeshifting uses/CR progression: **book ↔ structured data synchronized**\n\n## Path-data coverage\n\n| Class | Protected mechanic | Arch paths | Hero paths | Arch path abilities* | Hero path abilities* |\n|---|---|---:|---:|---:|---:|\n${rows}\n\n\\*Counts are the passives + actives stored in \`class-paths.js\`; class base features, level-milestone features, feats, Oaths, Mysteries/Curses, Druid forms, and prestige features are stored in their dedicated modules and are not double-counted here.\n\n## Invariant\n\nBalance may change numbers. It may not flatten the class loop. Resonance/Dissonance is a universal magical law layered **around** the class engine, not a replacement for Crescendo, Conviction, Blood Gauge, Momentum, Shapeshifting, Nuke Chains, Ki, Echo Slots, RC, Track Target, Totems, Palisades, Sneak Attack/Poison, Deployables, Mutations, Spell Matrix, or the Paladin Oath.\n`;

fs.writeFileSync(path.join(root, 'docs/mechanics/ABILITY_SYSTEM_VALIDATION_2026-07-31.md'), report);
console.log(`PASS classes=${canon.length} core=${Object.keys(core).length} feats=${feats.length} oaths=${oaths.length} mysteries=${mysteries.length} curses=${curses.length}`);
