/**
 * Ingest floor encounters, feats, races ASI helpers, and crafting recipes
 * into src/data for the Next.js companion.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import XLSX from "xlsx";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const outDir = path.join(root, "src", "data");
fs.mkdirSync(outDir, { recursive: true });

const bosses = {
  1: "Vaskor, the Stone Maw",
  2: "The Bloom That Hungers",
  3: "Ashthirst the Hollow",
  4: "Gor Vekk, Architect of Ends",
  5: "Choralith, Voice Below",
  6: "Lumen of the Shattered Thread",
  7: "Xarog, the Pactbound Furnace",
  8: "Eirfax, the Dusk Crowned",
  9: "Threxus, the Iron Spiral",
  10: "The Marquis of Silence",
};

const difficulties = {
  1: "Novice",
  2: "Apprentice",
  3: "Journeyman",
  4: "Expert",
  5: "Master",
  6: "Adept",
  7: "Veteran",
  8: "Elite",
  9: "Mythic",
  10: "Legendary",
};

const deepStubs = [
  {
    tier: 6,
    name: "Crossroads of the Shattered Thread",
    floors: "51–60",
    description:
      "Where broken Weave-threads tangle into a labyrinth of half-real pathways. Expeditions beyond the Canticle Gate enter the Decennium's mid-depths.",
    safeHavens: [],
    pointsOfInterest: [],
    mapped: false,
  },
  {
    tier: 7,
    name: "Pactbound Arena",
    floors: "61–70",
    description:
      "A crucible of bargains and bloodsport where power is bought with oaths. Few maps survive the Arena's rewriting.",
    safeHavens: [],
    pointsOfInterest: [],
    mapped: false,
  },
  {
    tier: 8,
    name: "Duskshard Pools",
    floors: "71–80",
    description:
      "Twilight basins where light and hush trade places. The air tastes of cooling metal and old prayers.",
    safeHavens: [],
    pointsOfInterest: [],
    mapped: false,
  },
  {
    tier: 9,
    name: "Veiled Iron Spiral",
    floors: "81–90",
    description:
      "A descending helix of iron and shadow. Each coil tightens the Weave around those who refuse to turn back.",
    safeHavens: [],
    pointsOfInterest: [],
    mapped: false,
  },
  {
    tier: 10,
    name: "Silencebound Void",
    floors: "91–100",
    description:
      "The hush beneath the song. The Marquis of Silence waits where even the First Choir's echo fades.",
    safeHavens: [],
    pointsOfInterest: [],
    mapped: false,
  },
];

function readText(filePath) {
  const buf = fs.readFileSync(filePath);
  // Many extract dumps are UTF-16 LE
  if (buf.length >= 2 && buf[0] === 0xff && buf[1] === 0xfe) {
    return buf.toString("utf16le").replace(/^\uFEFF/, "");
  }
  if (buf.length >= 4 && buf[1] === 0x00 && buf[3] === 0x00) {
    return buf.toString("utf16le").replace(/^\uFEFF/, "");
  }
  return buf.toString("utf8").replace(/^\uFEFF/, "");
}

function parseEncounters() {
  const src = readText(path.join(root, "floor_encounters_new.txt"));
  const body = src.split(/\n={10,}[\r\n]+SUMMARY/)[0] || src.split("SUMMARY")[0];
  const blocks = body.split(/(?=^Tier \d+:)/m).filter((b) => /^Tier \d+:/m.test(b));

  const tiers = [];
  for (const block of blocks) {
    const header = block.match(/Tier (\d+):\s*(.+)/);
    if (!header) continue;
    const tier = Number(header[1]);
    const name = header[2].trim();
    const lines = block.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);

    let description = "";
    const safeHavens = [];
    const pointsOfInterest = [];
    let mode = "desc";
    let current = null;

    const isEntryTitle = (line) => {
      if (line.length > 90) return false;
      if (/^(Safe Havens|Points of Interest|What Is )/i.test(line)) return false;
      if (/^Tier \d+:/.test(line)) return false;
      // "Name (Floor …)" or "Name (Outside/Inside)"
      if (/\((Floor|Floors|Outside|Inside|End of Floor)/i.test(line)) return true;
      // Short title without sentence punctuation
      if (!/[.!?]$/.test(line) && line.split(/\s+/).length <= 8 && /^[A-Z]/.test(line)) {
        return !/^(Here|Beyond|Floors|This|Only|Nestled|Dug|A |An |The air|Within)/.test(line);
      }
      return false;
    };

    for (let i = 1; i < lines.length; i++) {
      const line = lines[i];
      if (line === "Safe Havens") {
        mode = "haven";
        current = null;
        continue;
      }
      if (line === "Points of Interest") {
        mode = "poi";
        current = null;
        continue;
      }
      if (/^What Is /.test(line)) {
        mode = "desc";
        continue;
      }
      if (mode === "desc") {
        if (!/^Tier /.test(line) && line !== name) {
          description += (description ? " " : "") + line;
        }
        continue;
      }
      if (mode === "haven" || mode === "poi") {
        if (isEntryTitle(line)) {
          current = { name: line, description: "" };
          (mode === "haven" ? safeHavens : pointsOfInterest).push(current);
        } else if (current) {
          current.description += (current.description ? " " : "") + line;
        }
      }
    }

    description = description.replace(/^ieldheart/, "Yieldheart").trim();
    // Always use canonical 10-floor bands (do not scrape "Floors 1–3" patrol text)
    const floors = `${(tier - 1) * 10 + 1}–${tier * 10}`;

    tiers.push({
      tier,
      name,
      floors,
      description,
      safeHavens,
      pointsOfInterest,
      boss: bosses[tier] || "Unknown",
      difficulty: difficulties[tier] || "Unknown",
      mapped: true,
    });
  }

  const byTier = new Map(tiers.map((t) => [t.tier, t]));
  for (const stub of deepStubs) {
    if (!byTier.has(stub.tier)) {
      byTier.set(stub.tier, {
        ...stub,
        boss: bosses[stub.tier],
        difficulty: difficulties[stub.tier],
      });
    }
  }

  return {
    hornRule:
      "At 1200 hours (day 50 of the 2400-hour Opening), a giant horn sounds throughout the Decennium — the point of no return. Adventurers must retreat or risk being trapped in the depths for 10 years. Soft quit at Floor 50 Canticle is separate from the Horn.",
    tiers: [...byTier.values()].sort((a, b) => a.tier - b.tier),
  };
}

function extractNamedObjects(source, constName) {
  const start = source.indexOf(`const ${constName}`);
  if (start < 0) return [];
  let i = source.indexOf("{", start);
  let depth = 0;
  let end = -1;
  for (; i < source.length; i++) {
    const ch = source[i];
    if (ch === "{") depth++;
    else if (ch === "}") {
      depth--;
      if (depth === 0) {
        end = i;
        break;
      }
    }
  }
  const block = source.slice(start, end + 1);
  const feats = [];
  const re =
    /(\w+)\s*:\s*\{\s*name:\s*"([^"]+)"\s*,\s*description:\s*"((?:\\.|[^"\\])*)"\s*,\s*prerequisite:\s*"((?:\\.|[^"\\])*)"\s*,\s*effect:\s*"((?:\\.|[^"\\])*)"\s*,\s*type:\s*"([^"]+)"/g;
  let m;
  while ((m = re.exec(block))) {
    feats.push({
      id: m[1],
      name: m[2],
      description: m[3].replace(/\\"/g, '"'),
      prerequisite: m[4].replace(/\\"/g, '"'),
      effect: m[5].replace(/\\"/g, '"'),
      type: m[6].charAt(0).toUpperCase() + m[6].slice(1),
    });
  }
  return feats;
}

function ingestFeats() {
  const gd = fs.readFileSync(path.join(root, "game-data.js"), "utf8");
  const add = fs.readFileSync(path.join(root, "additional-feats.js"), "utf8");
  const base = extractNamedObjects(gd, "FEATS");
  const extra = extractNamedObjects(add, "ADDITIONAL_FEATS");
  const byName = new Map();
  for (const f of [...base, ...extra]) byName.set(f.name, f);
  return [...byName.values()].sort((a, b) => a.name.localeCompare(b.name));
}

function parseAsiString(s) {
  // Keep string for display; structured bonuses when simple "+N" pairs exist
  const bonuses = {};
  if (!s || /OR/i.test(s) || /All ability/i.test(s)) {
    return { display: s || "", bonuses: {}, special: s || "" };
  }
  const parts = s.split(/,\s*/);
  for (const part of parts) {
    const m = part.match(/([A-Za-z]+)\s*\+(\d+)/);
    if (m) bonuses[m[1]] = Number(m[2]);
  }
  return { display: s, bonuses, special: "" };
}

/** Structured races derived from CharacterBuilder-compatible display strings + game-data ASI when present */
function ingestRaces() {
  // Parse abilityScoreIncrease objects from game-data via regex per race block
  const gd = fs.readFileSync(path.join(root, "game-data.js"), "utf8");
  const racesStart = gd.indexOf("const RACES");
  const classesStart = gd.indexOf("const CLASSES");
  const raceSection = gd.slice(racesStart, classesStart > 0 ? classesStart : gd.length);
  const races = [];
  const raceRe =
    /\n    (\w+):\s*\{\s*\n\s*name:\s*"([^"]+)"\s*,\s*\n\s*description:\s*"((?:\\.|[^"\\])*)"[\s\S]*?abilityScoreIncrease:\s*(\{[^}]+\})/g;
  let m;
  while ((m = raceRe.exec(raceSection))) {
    let asi = {};
    try {
      asi = Function(`"use strict"; return (${m[4]})`)();
    } catch {
      asi = {};
    }
    const display = Object.entries(asi)
      .map(([k, v]) => `${k.charAt(0).toUpperCase() + k.slice(1)} +${v}`)
      .join(", ");
    // subrace names
    const blockStart = m.index;
    const next = raceSection.indexOf("\n    },\n    ", blockStart + 10);
    const block = raceSection.slice(blockStart, next > 0 ? next : blockStart + 2500);
    const subNames = [...block.matchAll(/name:\s*"([^"]+)"/g)]
      .map((x) => x[1])
      .filter((n) => n !== m[2]);

    races.push({
      id: m[1],
      name: m[2],
      info: m[3].replace(/\\"/g, '"'),
      abilityScoreIncrease: display || "See traits",
      abilityBonuses: Object.fromEntries(
        Object.entries(asi).map(([k, v]) => [k.charAt(0).toUpperCase() + k.slice(1), v])
      ),
      size: (block.match(/size:\s*"([^"]+)"/) || [])[1] || "Medium",
      speed: String((block.match(/speed:\s*(\d+)/) || [])[1] || 30) + " feet",
      traits: [...block.matchAll(/"([^"]+):\s*[^"]+"/g)].slice(0, 6).map((x) => x[1].split(":")[0]),
      languages: ["Common"],
      subraces: subNames,
    });
  }
  return races;
}

function ingestCrafting() {
  const wb = XLSX.readFile(path.join(root, "decennium_descent_crafting_recipes_validated.xlsx"));
  const skip = new Set(["Dashboard", "Recipe Template", "Bestiary Cross-Reference", "Validation Report"]);
  const recipes = [];
  let id = 1;

  for (const sheetName of wb.SheetNames) {
    if (skip.has(sheetName)) continue;
    const rows = XLSX.utils.sheet_to_json(wb.Sheets[sheetName], { defval: "", header: 1 });
    if (!rows.length) continue;

    // Find header row containing Recipe / Name
    let headerIdx = rows.findIndex(
      (r) =>
        Array.isArray(r) &&
        r.some((c) => /recipe|item name|result|output/i.test(String(c)))
    );
    if (headerIdx < 0) headerIdx = 0;
    const header = (rows[headerIdx] || []).map((c) => String(c).trim());

    const col = (...names) => {
      for (const n of names) {
        const i = header.findIndex((h) => h.toLowerCase() === n.toLowerCase());
        if (i >= 0) return i;
      }
      for (const n of names) {
        const i = header.findIndex((h) => h.toLowerCase().includes(n.toLowerCase()));
        if (i >= 0) return i;
      }
      return -1;
    };

    const iName = col("Recipe Name", "Recipe", "Item Name", "Name", "Result", "Output");
    const iDiff = col("Difficulty", "DC", "Skill DC");
    const iTime = col("Time", "Crafting Time", "Duration");
    const iRarity = col("Rarity", "Quality", "Tier");
    const iIngredients = col("Ingredients", "Components", "Materials", "Reagents");
    const iResult = col("Result Item", "Creates", "Output Item", "Product");

    for (let r = headerIdx + 1; r < rows.length; r++) {
      const row = rows[r];
      if (!row || !row.length) continue;
      const name = String(iName >= 0 ? row[iName] : row[0] || "").trim();
      if (!name || /^(recipe|name|tradecraft|notes)/i.test(name)) continue;
      if (name.length < 2) continue;

      const ingredientsRaw = iIngredients >= 0 ? String(row[iIngredients] || "") : "";
      const components = ingredientsRaw
        .split(/[,;+]|(?:\band\b)/i)
        .map((s) => s.trim())
        .filter(Boolean)
        .map((n, idx) => ({
          id: `ing-${id}-${idx}`,
          name: n,
          tier: 1,
          rarity: "Common",
          category: sheetName.toLowerCase(),
          value: 0,
          weight: 0,
          quantity: 1,
          properties: [],
        }));

      recipes.push({
        id: `recipe-${id++}`,
        name,
        skill: sheetName,
        difficulty: Number(iDiff >= 0 ? row[iDiff] : 10) || 10,
        craftingTime: String(iTime >= 0 ? row[iTime] : "1 hour") || "1 hour",
        rarity: String(iRarity >= 0 ? row[iRarity] : "Common") || "Common",
        components,
        resultItem: {
          name: String(iResult >= 0 && row[iResult] ? row[iResult] : name),
          tier: 1,
          rarity: String(iRarity >= 0 ? row[iRarity] : "Common") || "Common",
          value: 0,
          properties: [],
        },
      });
    }
  }

  return recipes;
}

function ingestCosmologyLore() {
  const cosmoPath = path.join(root, "The_Cosmology_of_Decennium_Descent_EXTRACT.txt");
  const worldPath = path.join(root, "The_World_of_Aethel_Lore_EXTRACT.txt");
  const cosmo = fs.existsSync(cosmoPath) ? readText(cosmoPath) : "";
  const world = fs.existsSync(worldPath) ? readText(worldPath) : "";

  const planes = [
    {
      name: "Material Plane",
      summary: "The nexus of Aethel — where the Weave is thickest and mortal stories unfold.",
      color: "#4fc3f7",
    },
    {
      name: "Plane of Fire",
      summary: "Elemental fire in orbit around the Material — Brogi's forge-echo in the Weave.",
      color: "#ff6b35",
    },
    {
      name: "Plane of Water",
      summary: "Tidal memory and depth; the pull that taught the Weave to flow.",
      color: "#29b6f6",
    },
    {
      name: "Plane of Air",
      summary: "Breath, voice, and distance — the Choir's first medium.",
      color: "#e1f5fe",
    },
    {
      name: "Plane of Earth",
      summary: "Stone patience and the weight of Stillness given form.",
      color: "#8d6e63",
    },
    {
      name: "Throne of Accord",
      summary: "Seat of divine justice above the Material — where oaths find witness.",
      color: "#ffffcc",
    },
    {
      name: "Nessus",
      summary: "The deepest hush — hell's gravity, where silence keeps its own counsel.",
      color: "#4e0000",
    },
  ];

  const take = (text, max = 1800) => {
    const cleaned = text.replace(/\u0000/g, "").trim();
    if (cleaned.length <= max) return cleaned;
    return cleaned.slice(0, max).replace(/\s+\S*$/, "") + "…";
  };

  return {
    title: "The Cosmology of Decennium Descent",
    planes,
    firstSong: take(cosmo, 2200),
    worldOutline: take(world, 2200),
  };
}

// --- run ---
const encounters = parseEncounters();
fs.writeFileSync(path.join(outDir, "floor-encounters.json"), JSON.stringify(encounters, null, 2));
console.log(
  "encounters",
  encounters.tiers.length,
  "havens",
  encounters.tiers.reduce((n, t) => n + t.safeHavens.length, 0),
  "pois",
  encounters.tiers.reduce((n, t) => n + t.pointsOfInterest.length, 0)
);

const feats = ingestFeats();
fs.writeFileSync(
  path.join(outDir, "feats.js"),
  `/** Auto-generated from game-data.js + additional-feats.js */\nexport const feats = ${JSON.stringify(feats, null, 2)};\nexport default feats;\n`
);
console.log("feats", feats.length);

const races = ingestRaces();
if (races.length >= 8) {
  fs.writeFileSync(
    path.join(outDir, "races.js"),
    `/** Auto-generated race ASI from game-data.js */\nexport const races = ${JSON.stringify(races, null, 2)};\nexport default races;\n`
  );
  console.log("races", races.length);
} else {
  console.log("races parse weak (", races.length, ") — CharacterBuilder keeps inline list");
}

const recipes = ingestCrafting();
fs.writeFileSync(path.join(outDir, "crafting-recipes.json"), JSON.stringify(recipes, null, 2));
console.log("crafting recipes", recipes.length);

const lore = ingestCosmologyLore();
fs.writeFileSync(path.join(outDir, "cosmology-lore.json"), JSON.stringify(lore, null, 2));
console.log("cosmology lore ok");
