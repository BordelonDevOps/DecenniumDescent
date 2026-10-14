const fs = require("fs");
const path = require("path");
const root = path.join(__dirname, "..");

function readJson(p) {
  return JSON.parse(fs.readFileSync(path.join(root, p), "utf8"));
}

const rb = fs.readFileSync(path.join(root, "rulebook_output.txt"), "utf8");
const featsMod = require(path.join(root, "src/data/feats.js"));
const spellsMod = require(path.join(root, "src/data/spells.js"));
const cdMod = require(path.join(root, "src/data/class-details.js"));
const bgMod = require(path.join(root, "src/data/backgrounds.js"));
const brMod = require(path.join(root, "src/data/builder-races.js"));

const feats = featsMod.feats || featsMod.default || featsMod;
const spells = spellsMod.SPELLS || spellsMod.default || spellsMod;
const cd = cdMod.classDetails || cdMod.default || cdMod;
const bg = bgMod.BACKGROUNDS;
const br = brMod.builderRaces || brMod.default || brMod;

const rulebookClasses = [];
for (const m of rb.matchAll(/^# (Bard|Cleric|Crimson Agent|Druid|Dragoon|Mage|Mirrorsage|Monk|Oracle|Paladin|Ranger|Shaman|Soldier|Swashbuckler|Thief|Tinker|Warrior|Wizard)\s*$/gm)) {
  rulebookClasses.push(m[1]);
}

const rulebookBgCount = (rb.match(/Skill Proficiencies:/g) || []).length;
const pl = readJson("src/data/prestige-lorebook.json");
const rv = readJson("src/data/racial-variants.json");
const bestiary = readJson("src/bestiary_data_full.json");
const cr = readJson("src/data/crafting-recipes.json");
const enc = readJson("src/data/floor-encounters.json");
const dm = readJson("src/data/dungeon-mechanics.json");
const cos = readJson("src/data/cosmology-lore.json");

const builderClasses = ["Bard","Cleric","Crimson Agent","Druid","Mage","Mirrorsage","Oracle","Paladin","Ranger","Shaman","Soldier","Thief","Tinker","Warrior","Wizard"];

console.log(JSON.stringify({
  feats: { live: feats.length, placeholders: feats.filter(f => /compendium|General feat from/i.test(f.description||"")).length },
  spells: { live: Object.keys(spells).length },
  classes: { rulebook: rulebookClasses, liveDetails: Object.keys(cd), builder: builderClasses, missingInBuilder: rulebookClasses.filter(c => !builderClasses.includes(c)), missingInDetails: rulebookClasses.filter(c => !Object.keys(cd).includes(c)) },
  backgrounds: { live: bg.length, rulebookSkillBlocks: rulebookBgCount },
  prestige: { live: pl.length },
  races: { live: br.length, variants: rv.length },
  bestiary: { live: bestiary.length, rootPartial: readJson("bestiary_data.json").length },
  crafting: { live: cr.length },
  encounters: { tiers: Object.keys(enc.tiers||{}).length },
  dungeon: { gateBosses: (dm.gateBosses||[]).length },
  cosmology: { planes: cos.planes?.length, worldSections: cos.worldSections?.length, chapters: cos.firstSongChapters?.length },
  oaths: [...new Set((rb.match(/Oath of [A-Za-z ]+/g)||[]))].slice(0,20),
}, null, 2));
