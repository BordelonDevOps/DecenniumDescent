/**
 * Parse floor_encounters_new.txt into structured JSON for the companion app.
 */
const fs = require("fs");
const path = require("path");

const src = fs.readFileSync(path.join(__dirname, "../floor_encounters_new.txt"), "utf8");
const body = src.split("SUMMARY")[0];

const tierBlocks = body.split(/(?=Tier \d+:)/).filter((b) => /Tier \d+:/.test(b));

function parseTier(text) {
  const tiers = [];
  for (const block of tierBlocks) {
    const header = block.match(/Tier (\d+):\s*(.+)/);
    if (!header) continue;
    const tier = parseInt(header[1], 10);
    const name = header[2].trim();
    const lines = block.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);

    let description = "";
    const safeHavens = [];
    const pointsOfInterest = [];
    let mode = "desc";
    let current = null;

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
        if (!/^Tier /.test(line) && line !== name) description += (description ? " " : "") + line;
        continue;
      }
      // Title lines are typically short / Title Case without ending period sometimes
      const isTitle =
        line.length < 80 &&
        !line.endsWith(".") &&
        /^[A-Z]/.test(line) &&
        (/\(/.test(line) || !/[a-z]{4,}.*[a-z]{4,}.*[a-z]{4,}/.test(line));

      if (mode === "haven" || mode === "poi") {
        // Heuristic: new entry if line looks like a name (contains Floor/Outside/Inside or short proper name)
        const looksLikeName =
          /\((Floor|Floors|Outside|Inside)/i.test(line) ||
          (line.length < 55 && /^[A-Z][\w''\- ]+( \([^)]+\))?$/.test(line));

        if (looksLikeName && !line.includes("…") && line.split(" ").length < 10) {
          current = { name: line, description: "" };
          (mode === "haven" ? safeHavens : pointsOfInterest).push(current);
        } else if (current) {
          current.description += (current.description ? " " : "") + line;
        } else if (mode === "desc") {
          description += " " + line;
        } else {
          // orphan description after section header — attach to last or start new generic
          current = { name: line.slice(0, 60), description: "" };
          (mode === "haven" ? safeHavens : pointsOfInterest).push(current);
        }
      }
    }

    // Floors range guess
    const floorMatch = description.match(/Floors?\s+(\d+)\s*[–-]\s*(\d+)/i);
    const floors = floorMatch ? `${floorMatch[1]}–${floorMatch[2]}` : `${(tier - 1) * 10 + 1}–${tier * 10}`;

    tiers.push({
      tier,
      name,
      floors,
      description: description.replace(/^ieldheart/, "Yieldheart").trim(),
      safeHavens,
      pointsOfInterest,
    });
  }
  return tiers;
}

const mapped = [
  { tier: 6, name: "Crossroads of the Shattered Thread", floors: "51–60", description: "Where broken Weave-threads tangle into a labyrinth of half-real pathways. Expeditions beyond the Canticle Gate enter the Decennium's mid-depths.", safeHavens: [], pointsOfInterest: [], boss: "Lumen of the Shattered Thread", mapped: false },
  { tier: 7, name: "Pactbound Arena", floors: "61–70", description: "A crucible of bargains and bloodsport where power is bought with oaths. Few maps survive the Arena's rewriting.", safeHavens: [], pointsOfInterest: [], boss: "Xarog, the Pactbound Furnace", mapped: false },
  { tier: 8, name: "Duskshard Pools", floors: "71–80", description: "Twilight basins where light and hush trade places. The air tastes of cooling metal and old prayers.", safeHavens: [], pointsOfInterest: [], boss: "Eirfax, the Dusk Crowned", mapped: false },
  { tier: 9, name: "Veiled Iron Spiral", floors: "81–90", description: "A descending helix of iron and shadow. Each coil tightens the Weave around those who refuse to turn back.", safeHavens: [], pointsOfInterest: [], boss: "Threxus, the Iron Spiral", mapped: false },
  { tier: 10, name: "Silencebound Void", floors: "91–100", description: "The hush beneath the song. The Marquis of Silence waits where even the First Choir's echo fades.", safeHavens: [], pointsOfInterest: [], boss: "The Marquis of Silence", mapped: false },
];

const bosses = {
  1: "Vaskor, the Stone Maw",
  2: "The Bloom That Hungers",
  3: "Ashthirst the Hollow",
  4: "Gor Vekk, Architect of Ends",
  5: "Choralith, Voice Below",
};

const tiers = parseTier(body).map((t) => ({
  ...t,
  boss: bosses[t.tier] || "Unknown",
  mapped: true,
}));

const all = [...tiers, ...mapped].sort((a, b) => a.tier - b.tier);

const out = {
  hornRule:
    "At 1200 hours (day 50 of the 2400-hour Opening), a giant horn sounds throughout the Decennium — the point of no return. Adventurers must retreat or risk being trapped in the depths for 10 years. Soft quit at Floor 50 Canticle is separate from the Horn.",
  tiers: all,
};

fs.writeFileSync(path.join(__dirname, "floor-encounters.json"), JSON.stringify(out, null, 2));
console.log(
  "Wrote floor-encounters.json tiers=",
  all.length,
  "mapped POIs=",
  tiers.reduce((n, t) => n + t.pointsOfInterest.length, 0)
);
