/**
 * Fill crafting-recipes.json components[] from validated xlsx.
 * Remaps IP/SRD monster-part labels to Decennium Descent / Aethel / Instruments salvage names.
 * Marks needsReview for Legendary/Mythic (deep-tier provisional).
 *
 * Usage: node scripts/fill-crafting-components.mjs
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import XLSX from "xlsx";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const xlsxPath = path.join(root, "decennium_descent_crafting_recipes_validated.xlsx");
const outPath = path.join(root, "src", "data", "crafting-recipes.json");
const backupDir = path.join(root, "src", "data", "backups");

const skip = new Set([
  "Dashboard",
  "Recipe Template",
  "Bestiary Cross-Reference",
  "Validation Report",
]);

/** IP / SRD / Great-Wheel monster parts → Aethel / Instruments / bestiary-aligned */
const MONSTER_REMAP = {
  "Storm Giant Heart": "Thunder-vein Core",
  "Frost Giant Blood": "Chillslag Blood",
  "Stone Giant Heart": "Stoneworks Heartstone",
  "Cloud Giant Hair": "Mist-strand Filament",
  "Giant Muscle": "Brute Muscle Bundle",
  "Giant Bone": "Giant Bone",
  "Red Dragon Scale": "Emberplate Scale",
  "Blue Dragon Gland": "Stormscale Gland",
  "Dragon Sinew": "Gateward Sinew",
  "Dragon Scale": "Emberplate Scale",
  "Dragon Blood": "Forge-ichor",
  "Dragon Tooth": "Emberplate Tooth",
  "Phoenix Feather": "Dawnflare Plume",
  "Phoenix Heart": "Dawnflare Heart",
  "Unicorn Horn": "Spiralhorn Shard",
  "Kraken Ink": "Abyssal Ink",
  "Mind Flayer Brain": "Echo-thought Mass",
  "Aboleth Slime": "Deep-memory Slime",
  "Displacer Beast Hide": "Phasehide Scrap",
  "Invisible Stalker Dust": "Veilstalker Dust",
  "Wizard's Brain": "Arcanist Cortex Residue",
  "Demon Heart": "Pactbound Heartchip",
  "Demon Horn": "Pactbound Horn",
  "Troll Blood": "Regenerant Ichor",
  "Merfolk Scales": "Reedcaller Scale",
  "Treant Bark": "Heartroot Bark",
  "Dryad Hair": "Bloomvine Strand",
  "Sylph Wing": "Air-sprite Membrane",
  "Winter Wolf Fur": "Ashen-pelt Fur",
  "Golem Core": "Animated Core",
  "Arcane Core": "Resonance Core",
  "Ooze Residue": "Cave-ooze Residue",
  "Poison Sac": "Spore Sac",
  "Toxic Secretion": "Spore Tox",
  "Venomous Gland": "Venom Gland",
  "Lightning Elemental Spark": "Storm-spark Shard",
  "Magical Residue": "Weave Residue",
  "Earth Elemental Core": "Earthvein Core",
  "Corrupted Spirit": "Shade Wisp",
  "Psychic Residue": "Echo Residue",
  "Acid Gland": "Corrosive Sac",
  "Air Elemental Essence": "Gale Essence",
  "Crystal Formation": "Luminous Crystal",
  "Shadow Essence": "Shade Essence",
  "Ice Elemental Core": "Frostcore Shard",
  "Undead Essence": "Hollow Essence",
  "Fire Elemental Essence": "Brogi Ash-essence",
  "Corrosive Secretion": "Acid Seep",
  "Water Elemental Essence": "Tide Essence",
  "Living Vine": "Root-grasper Tendon",
  "Elemental Core": "Elemental Core",
  "Gelatinous Sample": "Cave-ooze Residue",
  "Aberrant Ichor": "Aberrant Ichor",
  "Fey Dust": "Bloomdust",
  "Mind Crystal": "Echo Crystal",
  "Infernal Hide": "Pactbound Hide",
  "Death Energy": "Hollow Essence",
  "Corrupted Essence": "Shade Essence",
  "Blessed Essence": "Choir Essence",
  "Primal Essence": "Primal Essence",
  "Mechanical Part": "Mechanical Part",
  "Animated Core": "Animated Core",
};

/** Base ingredients that leak external IP or planar branding */
const BASE_REMAP = {
  "Mithral ingot": "Brightsteel Ingot",
  "Adamantine ingot": "Heartsteel Ingot",
  "Planar energy": "Resonance Charge",
  "Ethereal thread": "Veilthread",
  "Enchanted crystal": "Luminous Crystal",
  "Magical essence": "Weave Essence",
  "Magical pigment": "Resonance Pigment",
  "Magical filter": "Weave Filter",
  "Arcane dust": "Resonance Dust",
  "Arcane powder": "Resonance Powder",
  "Arcane symbols": "Resonance Glyphs",
  "Binding runes": "Binding Glyphs",
  "Focusing crystal": "Focusing Crystal",
  "Power source": "Resonance Cell",
};

const IP_LEAK_RE =
  /\b(mind\s*flayer|illithid|aboleth|displacer|beholder|owlbear|drow|mithral|mithril|adamantine|kraken|unicorn|phoenix|troll|treant|dryad|sylph|golem|elemental|dragon|demon|devil|giant|wizard'?s?\s*brain|winter\s*wolf|merfolk|invisible\s*stalker)\b/i;

function splitIngredients(raw) {
  return String(raw || "")
    .split(/[,;]/)
    .map((s) => s.trim())
    .filter(Boolean);
}

/** "Crystal vial (5)" or "Storm Giant Heart (Tier 1)" */
function parseIngredientToken(raw) {
  const s = String(raw).trim();
  const tierMatch = s.match(/^(.+?)\s*\(\s*Tier\s*(\d+)\s*\)\s*$/i);
  if (tierMatch) {
    return { name: tierMatch[1].trim(), quantity: 1, partTier: Number(tierMatch[2]) };
  }
  const qtyMatch = s.match(/^(.+?)\s*\((\d+)\)\s*$/);
  if (qtyMatch) {
    return { name: qtyMatch[1].trim(), quantity: Number(qtyMatch[2]), partTier: null };
  }
  return { name: s, quantity: 1, partTier: null };
}

function skillToDungeonTier(skillLevel) {
  const sl = Math.max(1, Number(skillLevel) || 1);
  return Math.min(10, Math.ceil(sl / 2));
}

function rarityForTier(tier) {
  if (tier <= 1) return "Common";
  if (tier === 2) return "Uncommon";
  if (tier === 3) return "Rare";
  if (tier === 4) return "Very Rare";
  if (tier === 5) return "Legendary";
  return "Mythic";
}

function remapName(name, table) {
  if (table[name]) return table[name];
  // Case-insensitive fallback
  const key = Object.keys(table).find((k) => k.toLowerCase() === name.toLowerCase());
  return key ? table[key] : name;
}

function slugId(prefix, recipeNum, idx, name) {
  const slug = name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_|_$/g, "")
    .slice(0, 48);
  return `${prefix}-${recipeNum}-${idx}-${slug || "part"}`;
}

function ensureBackup() {
  if (!fs.existsSync(outPath)) return;
  fs.mkdirSync(backupDir, { recursive: true });
  const stamp = new Date().toISOString().slice(0, 10);
  const bak = path.join(backupDir, `crafting-recipes.json.bak-${stamp}`);
  if (!fs.existsSync(bak)) {
    fs.copyFileSync(outPath, bak);
    console.log(`Backup → ${bak}`);
  } else {
    console.log(`Backup already present → ${bak}`);
  }
}

function buildRecipes() {
  const wb = XLSX.readFile(xlsxPath);
  const recipes = [];
  let id = 1;
  const unmappedMons = new Map();
  const unmappedBases = new Map();
  let needsReviewCount = 0;
  let ipLeakAfter = 0;

  for (const sheetName of wb.SheetNames) {
    if (skip.has(sheetName)) continue;
    const rows = XLSX.utils.sheet_to_json(wb.Sheets[sheetName], { header: 1, defval: "" });
    const headerIdx = rows.findIndex(
      (r) => Array.isArray(r) && r.some((c) => String(c).trim() === "Recipe Name")
    );
    if (headerIdx < 0) continue;
    const header = rows[headerIdx].map((c) => String(c).trim());
    const col = (name) => header.findIndex((h) => h === name);

    const iName = col("Recipe Name");
    const iQuality = col("Quality Tier");
    const iSkillLvl = col("Required Skill Level");
    const iBase = col("Base Ingredients");
    const iMonster = col("Monster Parts");
    const iTags = col("Crafting Tags");
    const iDC = col("Crafting DC");
    const iTime = col("Creation Time");
    const iQty = col("Output Quantity");
    const iEffects = col("Effects/Properties");
    const iValue = col("Value (GP)");

    for (let r = headerIdx + 1; r < rows.length; r++) {
      const row = rows[r];
      if (!row || !row.length) continue;
      const name = String(iName >= 0 ? row[iName] : "").trim();
      if (!name || /recipe name/i.test(name)) continue;

      const recipeNum = id++;
      const skillLevel = Number(iSkillLvl >= 0 ? row[iSkillLvl] : 1) || 1;
      const dungeonTier = skillToDungeonTier(skillLevel);
      const quality = String(iQuality >= 0 ? row[iQuality] : "Common") || "Common";
      const effects = String(iEffects >= 0 ? row[iEffects] : "");
      const tags = String(iTags >= 0 ? row[iTags] : "");
      const value = Number(iValue >= 0 ? row[iValue] : 0) || 0;
      const difficulty = Number(iDC >= 0 ? row[iDC] : 10) || 10;
      const craftingTime = String(iTime >= 0 ? row[iTime] : "1 hour") || "1 hour";
      const quantity = Number(iQty >= 0 ? row[iQty] : 1) || 1;

      const baseRaw = splitIngredients(iBase >= 0 ? row[iBase] : "");
      const monRaw = splitIngredients(iMonster >= 0 ? row[iMonster] : "");

      const components = [];
      let idx = 0;

      for (const token of baseRaw) {
        const parsed = parseIngredientToken(token);
        const remapped = remapName(parsed.name, BASE_REMAP);
        if (remapped === parsed.name && IP_LEAK_RE.test(parsed.name)) {
          unmappedBases.set(parsed.name, (unmappedBases.get(parsed.name) || 0) + 1);
        }
        const cTier = parsed.partTier || dungeonTier;
        components.push({
          id: slugId("ing", recipeNum, idx++, remapped),
          name: remapped,
          tier: cTier,
          rarity: rarityForTier(cTier),
          category: "base",
          value: 0,
          weight: 0,
          quantity: parsed.quantity,
          properties: [],
        });
      }

      for (const token of monRaw) {
        const parsed = parseIngredientToken(token);
        const remapped = remapName(parsed.name, MONSTER_REMAP);
        if (!MONSTER_REMAP[parsed.name] && remapped === parsed.name) {
          // Try stripping trailing tier already handled; track unknowns
          if (IP_LEAK_RE.test(parsed.name) || /dragon|flayer|aboleth|displacer|kraken|unicorn|phoenix/i.test(parsed.name)) {
            unmappedMons.set(parsed.name, (unmappedMons.get(parsed.name) || 0) + 1);
          }
        }
        const cTier = parsed.partTier || dungeonTier;
        components.push({
          id: slugId("part", recipeNum, idx++, remapped),
          name: remapped,
          tier: cTier,
          rarity: rarityForTier(cTier),
          category: "monster_part",
          value: 0,
          weight: 0,
          quantity: parsed.quantity,
          properties: ["salvage"],
        });
      }

      const deepQuality = /^(Legendary|Mythic)$/i.test(quality);
      const deepSkill = skillLevel >= 11;
      const empty = components.length === 0;
      const leak = components.some((c) => IP_LEAK_RE.test(c.name));
      if (leak) ipLeakAfter++;

      let needsReview = false;
      let needsReviewReason = "";
      let status = "ready";

      if (empty) {
        needsReview = true;
        needsReviewReason = "no_ingredients_in_workbook";
        status = "stub";
      } else if (leak) {
        needsReview = true;
        needsReviewReason = "possible_ip_label_after_remap";
        status = "needsReview";
      } else if (deepQuality) {
        needsReview = true;
        needsReviewReason = "legendary_or_mythic_provisional";
        status = "needsReview";
      } else if (deepSkill) {
        needsReview = true;
        needsReviewReason = "skill_11_plus_deep_tier_provisional";
        status = "needsReview";
      }

      if (needsReview) needsReviewCount++;

      recipes.push({
        id: `recipe-${recipeNum}`,
        name,
        skill: sheetName,
        skillLevel,
        difficulty,
        craftingTime,
        rarity: quality,
        quantity,
        tags,
        effects,
        needsReview,
        ...(needsReviewReason ? { needsReviewReason } : {}),
        status,
        components,
        resultItem: {
          name,
          tier: dungeonTier,
          rarity: quality,
          value,
          properties: effects ? [effects] : [],
        },
      });
    }
  }

  return { recipes, unmappedMons, unmappedBases, needsReviewCount, ipLeakAfter };
}

ensureBackup();
const { recipes, unmappedMons, unmappedBases, needsReviewCount, ipLeakAfter } = buildRecipes();
fs.writeFileSync(outPath, JSON.stringify(recipes, null, 2));

const filled = recipes.filter((r) => r.components.length > 0).length;
const empty = recipes.length - filled;
const t15 = recipes.filter((r) => (r.resultItem?.tier || 1) <= 5);
const t15Filled = t15.filter((r) => r.components.length > 0).length;
const t15Ready = t15.filter((r) => r.status === "ready").length;
const bySkill = {};
for (const r of recipes) {
  bySkill[r.skill] = bySkill[r.skill] || { n: 0, filled: 0, review: 0 };
  bySkill[r.skill].n++;
  if (r.components.length) bySkill[r.skill].filled++;
  if (r.needsReview) bySkill[r.skill].review++;
}

console.log(
  JSON.stringify(
    {
      wrote: outPath,
      total: recipes.length,
      filled,
      empty,
      needsReview: needsReviewCount,
      ipLeakAfterRemap: ipLeakAfter,
      t1_5: { total: t15.length, filled: t15Filled, statusReady: t15Ready },
      unmappedMons: Object.fromEntries([...unmappedMons].sort((a, b) => b[1] - a[1])),
      unmappedBases: Object.fromEntries([...unmappedBases].sort((a, b) => b[1] - a[1])),
      bySkill,
      sample: recipes.slice(0, 2),
      simRecipes: ["recipe-2", "recipe-42", "recipe-43", "recipe-433"].map((id) => {
        const r = recipes.find((x) => x.id === id);
        return r
          ? { id: r.id, name: r.name, components: r.components.map((c) => `${c.name}×${c.quantity}`), status: r.status }
          : { id, missing: true };
      }),
    },
    null,
    2
  )
);
