import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.dirname(fileURLToPath(import.meta.url)) + "/..";

function readJson(p) {
  return JSON.parse(fs.readFileSync(path.join(root, p), "utf8"));
}

const rb = fs.readFileSync(path.join(root, "rulebook_output.txt"), "utf8");
const feats = (await import(path.join(root, "src/data/feats.js"))).feats;
const spellsMod = await import(path.join(root, "src/data/spells.js"));
const spells = spellsMod.SPELLS;
const cd = (await import(path.join(root, "src/data/class-details.js"))).classDetails;
const bg = (await import(path.join(root, "src/data/backgrounds.js"))).BACKGROUNDS;
const br = (await import(path.join(root, "src/data/builder-races.js"))).builderRaces;

const results = {};

results.feats = {
  live: feats.length,
  placeholders: feats.filter((f) => /compendium|General feat from/i.test(f.description || "")).length,
  types: feats.reduce((a, f) => ((a[f.type] = (a[f.type] || 0) + 1), a), {}),
};

results.spells = {
  live: Object.keys(spells).length,
  schools: Object.values(spells).reduce((a, s) => ((a[s.school] = (a[s.school] || 0) + 1), a), {}),
};

results.classes = {
  live: Object.keys(cd).length,
  names: Object.keys(cd),
  levelDepth: Object.fromEntries(
    Object.entries(cd).map(([k, v]) => [k, Object.keys(v.levels || {}).length])
  ),
};

results.backgrounds = { live: bg.length };
results.races = { live: br.length, names: br.map((r) => r.name || r.id) };

const rv = readJson("src/data/racial-variants.json");
results.racialVariants = { live: rv.length };

const pl = readJson("src/data/prestige-lorebook.json");
results.prestige = { live: pl.length, names: pl.map((p) => p.name) };

const bestiary = readJson("src/bestiary_data_full.json");
results.bestiary = { live: bestiary.length };

const cr = readJson("src/data/crafting-recipes.json");
results.crafting = { live: cr.length };

const enc = readJson("src/data/floor-encounters.json");
let encCount = 0;
for (const t of Object.values(enc.tiers || {})) {
  for (const fl of t.floors || []) encCount += (fl.encounters || []).length;
}
results.encounters = { tiers: Object.keys(enc.tiers || {}).length, entries: encCount };

const classNames = [
  "Bard", "Cleric", "Crimson Agent", "Druid", "Mage", "Mirrorsage", "Oracle",
  "Paladin", "Ranger", "Shaman", "Soldier", "Swashbuckler", "Thief", "Tinker",
  "Warrior", "Wizard", "Monk", "Dragoon",
];
results.rulebookClasses = Object.fromEntries(
  classNames.map((c) => [c, new RegExp(`#+\\s*${c.replace(/ /g, "\\s+")}`, "i").test(rb)])
);

const bgMatches = rb.match(/## Background: ([^\n]+)/g) || [];
results.rulebookBackgrounds = bgMatches.map((m) => m.replace("## Background: ", ""));

const oaths = [...new Set((rb.match(/Oath of [A-Za-z ]+/g) || []))];
results.paladinOaths = oaths;

const dm = readJson("src/data/dungeon-mechanics.json");
results.dungeon = {
  gateBosses: (dm.gateBosses || []).length,
  hasExpedition: !!dm.expedition,
};

const cos = readJson("src/data/cosmology-lore.json");
results.cosmology = {
  planes: cos.planes?.length,
  worldSections: cos.worldSections?.length,
  firstSongChapters: cos.firstSongChapters?.length,
  firstSongLen: (cos.firstSong || "").length,
};

// unwired root files
for (const f of ["game-data.js", "additional-feats.js", "bestiary_data.json"]) {
  const p = path.join(root, f);
  if (fs.existsSync(p)) {
    const sz = fs.statSync(p).size;
    results.unwired = results.unwired || {};
    results.unwired[f] = sz;
  }
}

console.log(JSON.stringify(results, null, 2));
