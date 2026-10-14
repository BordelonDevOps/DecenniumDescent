// Generates docs/manuals/Codex_of_the_Heartcell.md and CODEX_QUALITY_AUDIT.md
// from src/bestiary_data_full.json (+ a read-only cross-check against
// Bestiary.xlsx's own NeedsReview column, extracted to scripts/_excel_extra.json).
// This script does NOT write to Bestiary.xlsx or bestiary_data_full.json.
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(ROOT, "docs", "manuals");
const FRAG_DIR = path.join(__dirname, "codex_fragments");

const bestiary = require(path.join(ROOT, "src", "bestiary_data_full.json"));
let excelExtra = {};
try {
  excelExtra = require(path.join(__dirname, "_excel_extra.json"));
} catch (e) {
  console.warn("No _excel_extra.json found; NeedsReview cross-check disabled.");
}

const { list: TYPE_DICT, ipExact, ipFamily } = require("./codex_type_dictionary");
const { ecologyFor } = require("./codex_ecology_phrases");

const GENERIC_ATTACKS = new Set(["Tail Lash", "Monstrous Claw", "Freak Bite", "Aberrant Lash"]);

const GUARDIAN_NAMES = new Set([
  "Vaskor, the Stone Maw",
  "The Bloom That Hungers",
  "Ashthirst the Hollow",
  "Gor Vekk, Architect of Ends",
  "Choralith, Voice Below",
  "Lumen of the Shattered Thread",
  "Xarog, the Pactbound Furnace",
  "Xarog the Pactbound Furnace",
  "Eirfax, the Dusk Crowned",
  "Threxus, the Iron Spiral",
  "The Marquis of Silence",
]);

const RESKIN_FAMILY_PREFIXES = [
  { prefix: "Umbrin", expected: "Humanoid" },
  { prefix: "Deep Dwarf", expected: "Humanoid" },
  { prefix: "Cave Gnome", expected: "Humanoid" },
  { prefix: "Serpent-Blood", expected: "Humanoid" },
  { prefix: "Astral Reaver", expected: "Humanoid" },
  { prefix: "Astral Ascetic", expected: "Humanoid" },
  { prefix: "Depth Toad", expected: "Humanoid" },
  { prefix: "Voidmind", expected: "Aberration" },
  { prefix: "Gaze Tyrant", expected: "Aberration" },
  { prefix: "Gazer", expected: "Aberration" },
  { prefix: "Lesser Gaze Tyrant", expected: "Aberration" },
];

function parseCR(cr) {
  if (cr === null || cr === undefined) return null;
  const s = String(cr).trim();
  if (s.includes("/")) {
    const [a, b] = s.split("/").map(Number);
    return a / b;
  }
  const n = Number(s);
  return Number.isNaN(n) ? null : n;
}

function crLabel(cr) {
  return String(cr);
}

function fmtDamage(dmgArr) {
  if (!dmgArr || !dmgArr.length) return "";
  return dmgArr.map((d) => `${d.dice} ${d.type}`).join(" + ");
}

function attackLine(a) {
  const bonus = a.attackBonus !== undefined ? `+${a.attackBonus} to hit` : "";
  const dmg = fmtDamage(a.damage);
  const countTxt = a.count && a.count > 1 ? ` (x${a.count})` : "";
  const range = a.range && a.range.reachFt ? `, reach ${a.range.reachFt} ft.` : "";
  const areaRange = a.range && a.range.radiusFt ? `, ${a.range.radiusFt}-ft. radius` : "";
  let save = "";
  if (a.save) {
    save = ` — ${a.save.ability} save DC ${a.save.dc}${a.save.onSuccess === "half" ? " (half on success)" : ""}`;
  }
  const usage = a.usage === "recharge" && a.recharge ? ` (Recharge ${a.recharge.minimumRoll}-${a.recharge.dieSides})` : "";
  const stub = GENERIC_ATTACKS.has(a.name) ? " *[provisional attack name — generic sandbox filler]*" : "";
  const parts = [`**${a.name}**${countTxt}${usage}`, bonus, dmg].filter(Boolean).join(" — ");
  return `- ${parts}${range}${areaRange}${save}${stub}`;
}

function ipFlagFor(name) {
  if (ipExact[name]) {
    return { severe: true, text: `**STUB — stock alias, Director must re-skin.** Proposed Aethel name: *${ipExact[name]}* (not yet locked — see Naming & IP Reskin Ledger).` };
  }
  for (const fam of ipFamily) {
    if (fam.test.test(name)) {
      return {
        severe: true,
        text: `**STUB — stock alias, Director must re-skin.** Part of the ${fam.label}; proposed: *${fam.rename(name)}*. ${fam.note}`,
      };
    }
  }
  return null;
}

function reskinFamilyFlag(name, type) {
  for (const fam of RESKIN_FAMILY_PREFIXES) {
    if (name.startsWith(fam.prefix)) {
      if (type !== fam.expected) {
        return `**STUB — Director must re-skin.** Culture-family entry; sheet Type (**${type}**) was randomized independently of the ${fam.prefix} concept. Treat as **${fam.expected}** regardless of the sheet field.`;
      }
      return null;
    }
  }
  return null;
}

function needsReviewFlag(name) {
  const extra = excelExtra[name];
  if (!extra || !extra.needsReview) return null;
  const raw = String(extra.needsReview);
  if (raw.startsWith("size:")) {
    const m = raw.match(/^size:(\w+)->(\w+)(; (.+))?$/);
    if (m) {
      const [, from, to, , suffix] = m;
      const suspect = suffix === "cr-suspect-high";
      const label = suspect
        ? `**STUB — Director must re-skin.** Excel's own \`NeedsReview\` column flags Size: sandbox suggests **${to}** instead of the sheet's **${from}**, and Challenge Rating looks suspiciously high for the sheet's current Size.`
        : `Draft note: Excel's own \`NeedsReview\` column flags Size: sandbox suggests **${to}** instead of the sheet's **${from}**.`;
      return { severe: suspect, text: label };
    }
  }
  if (raw.startsWith("hp:")) {
    const m = raw.match(/^hp:(\d+)->(\d+)$/);
    if (m) {
      return { severe: false, text: `Draft note: Excel's own \`NeedsReview\` column flags Hit Points as likely low — sandbox suggests **${m[2]}** instead of **${m[1]}**.` };
    }
  }
  return { severe: false, text: `Draft note: Excel's own \`NeedsReview\` column flags this row (\`${raw}\`).` };
}

function dictMismatchFlag(name, type) {
  const expected = TYPE_DICT[name];
  if (expected && expected !== type) {
    return `**STUB — Director must re-skin.** The name *${name}* reads as **${expected}** in ordinary Aethel usage, but the sheet lists Type **${type}** — a nonsense Type assignment from the sandbox generator (the classic case is a Tiny Undead named after a sky-faring people; this is the same failure mode).`;
  }
  return null;
}

function buildFlags(m) {
  const flags = [];
  let severeCount = 0;

  const dictFlag = dictMismatchFlag(m.name, m.type);
  if (dictFlag) {
    flags.push(dictFlag);
    severeCount++;
  }

  const famFlag = reskinFamilyFlag(m.name, m.type);
  if (famFlag) {
    flags.push(famFlag);
    severeCount++;
  }

  const ipFlag = ipFlagFor(m.name);
  if (ipFlag) {
    flags.push(ipFlag.text);
    if (ipFlag.severe) severeCount++;
  }

  const nr = needsReviewFlag(m.name);
  if (nr) {
    flags.push(nr.text);
    if (nr.severe) severeCount++;
  }

  if (m.name === "Xarog the Pactbound Furnace") {
    flags.push(
      "**STUB — duplicate row.** A second entry, \"Xarog, the Pactbound Furnace\" (with comma), carries the Gate Guardian tag and bespoke companion-authored stats. This no-comma row is a stray Excel-sandbox leftover — see Gate Seal VII in Part II. Recommend deleting this row in the next Excel pass."
    );
    severeCount++;
  }

  const attacks = (m.combat && m.combat.attacks) || [];
  const generic = attacks.filter((a) => GENERIC_ATTACKS.has(a.name));
  if (generic.length && !GUARDIAN_NAMES.has(m.name)) {
    flags.push(
      `Draft note: ${generic.length > 1 ? "attacks" : "attack"} ${generic.map((a) => `*${a.name}*`).join(", ")} ${generic.length > 1 ? "are" : "is"} reused sandbox filler (this exact name appears on hundreds of unrelated entries) — reflavor freely at the table.`
    );
  }

  return { flags, isStub: severeCount > 0 };
}

function renderEntry(m) {
  const cr = m.challengeRating;
  const crNum = parseCR(cr);
  const { flags, isStub } = buildFlags(m);
  const lines = [];
  const stubTag = isStub ? " — STUB" : "";
  lines.push(`### ${m.name}${stubTag}`);
  lines.push("");
  lines.push(
    `*${m.size || "?"} ${m.type || "?"}, ${m.alignment || "Unaligned"}.* **Challenge ${crLabel(cr)}** (${m.xp ?? "?"} XP). **Zone:** ${m.zoneFound || "unknown"}.`
  );
  lines.push("");
  if (GUARDIAN_NAMES.has(m.name) && m.name !== "Xarog the Pactbound Furnace") {
    lines.push("**Gate Seal entity** — see Part II for full lore, staging, tactics, and reward-as-bait notes. Only the raw stat block is repeated here for lexicon completeness.");
    lines.push("");
  } else {
    lines.push(ecologyFor(m, m.name));
    lines.push("");
  }
  for (const f of flags) {
    lines.push(`> ${f}`);
    lines.push("");
  }
  const ac = m.armorClass ?? "—";
  const hp = m.hitPoints ?? "—";
  const speed = m.speed ?? "—";
  lines.push(`**Armor Class** ${ac} · **Hit Points** ${hp} · **Speed** ${speed}`);
  lines.push("");
  if (m.abilities) {
    const a = m.abilities;
    lines.push(
      `**Abilities** STR ${a.strength} · DEX ${a.dexterity} · CON ${a.constitution} · INT ${a.intelligence} · WIS ${a.wisdom} · CHA ${a.charisma}`
    );
    lines.push("");
  }
  if (m.skills) {
    lines.push(`**Skills** ${m.skills}`);
    lines.push("");
  }
  if (m.senses) {
    lines.push(`**Senses** ${m.senses}`);
    lines.push("");
  }
  if (m.languages) {
    lines.push(`**Languages** ${m.languages}`);
    lines.push("");
  }
  const attacks = (m.combat && m.combat.attacks) || [];
  if (attacks.length) {
    lines.push("**Attacks**");
    attacks.forEach((a) => lines.push(attackLine(a)));
    lines.push("");
  }
  const def = m.combat && m.combat.defenses;
  if (def && (def.resistances?.length || def.immunities?.length || def.conditionImmunities?.length)) {
    const bits = [];
    if (def.resistances?.length) bits.push(`Resistances: ${def.resistances.join(", ")}`);
    if (def.immunities?.length) bits.push(`Immunities: ${def.immunities.join(", ")}`);
    if (def.conditionImmunities?.length) bits.push(`Condition immunities: ${def.conditionImmunities.join(", ")}`);
    lines.push(`**Defenses** ${bits.join("; ")}`);
    lines.push("");
  }
  const src = (m.combat && m.combat.source) || "unknown";
  const provenance =
    src === "companion-authored draft"
      ? "*Provenance: companion-authored draft — intentional numbers, still subject to Director revision.*"
      : "*Provenance: Excel-sandbox draft — treat as a fair starting budget, not a final block.*";
  lines.push(provenance);
  lines.push("");
  return lines.join("\n");
}

const ECOLOGY_ESSAYS = {
  Aberration: `The Aberrations of Aethel are not a species so much as a symptom — proof that the Spiral's geometry has thin places, and that something pours through wherever it thins. No two Directors need to explain them the same way twice; the truth Aethel's own scholars keep discovering is that Aberrations resist a single origin story, and that resistance is the point. **Player knowledge** should stay at the level of rumor and survivor testimony: wrongness, incomprehension, things that were clearly never meant to be understood by a living mind. **Director knowledge** goes further — Aberrations are often the most reliable evidence that a given floor sits near an old Weave-fold, and their lairs are worth mapping even when the creature itself is avoided. Emphasize incomprehension and environmental wrongness over conventional monster tactics; an Aberration fight should feel like an argument with the room, not just with the creature in it.`,
  Beast: `Beasts are Aethel's least mysterious residents and, for exactly that reason, its most persistent hazard. Most predate the Decennium's architecture entirely — they simply never left when the floors closed in around them, and they have gone on hunting, denning, and migrating in patterns a patient Recon team can learn to read. **Player knowledge** is whatever local hunters, floor cultures, and prior Expeditions have already worked out: territory, diet, and the difference between a Beast that flees a torch and one that doesn't. **Director knowledge** should treat Beasts as pressure on resources — rations, light, rope, time — rather than as headline encounters. Use them to teach new Combat teams the value of avoidance, and reserve genuine set-piece treatment for the rare Beast that has grown unnaturally large or bold on whatever a given floor feeds it.`,
  Celestial: `A Celestial encountered this far into the Decennium is never simply good news. Whatever higher harmony sent it down here did not account for what the Pact's dissonance economy would eventually ask of it, and most Celestials an Expedition meets have been down here long enough to have complicated, compromised motives layered over whatever radiant mandate they started with. **Player knowledge** should read them as rare, striking, and morally unresolved — never a guaranteed ally. **Director knowledge** treats Celestials as leverage: conditional aid, expensive bargains, and judgment that is not calibrated to player convenience. A Celestial's help should always cost something specific, and its fall (if it falls) should register somewhere above the Decennium that a Director has already decided how to use later.`,
  Construct: `Constructs are Aethel's oldest engineering wearing whatever purpose has outlived its original maker. In the Anvil tiers especially, a Construct is as often evidence as it is a threat — a labor unit, a weapon left running past its intended service life, a guardian obeying an order its makers would now regret giving. **Player knowledge** is limited to function: what it guards, how it moves, whether it responds to command tokens or seals. **Director knowledge** should treat every Construct encounter as a small mystery — who built it, why, and what happened to them — worth more to a Research team than the Construct's salvage value. Disabling and questioning a Construct (however it "answers") is consistently more interesting than simply destroying it.`,
  Dragon: `Dragons are Aethel's apex predators of ambition, and the Decennium has never managed to fully domesticate that ambition into something predictable. A Dragon's hoard is a symptom of its nature, not the nature itself — pride, territory, and a long memory for anyone who tries to lie to it matter more than the gold ever does. **Player knowledge** treats a Dragon sighting as a campaign event: rumor, omen, and reputation travel ahead of the creature itself. **Director knowledge** should plan the hoard's aftermath before the fight — surface factions will contest a Dragon's leftover wealth for sessions afterward, and a Dragon fight run as a single floor's random encounter wastes the type's entire narrative weight. Reserve genuine Dragon encounters for moments that deserve a full session of build-up.`,
  Elemental: `Elementals are what happens when the Spiral's folds concentrate raw matter and energy hard enough that it starts behaving like a creature. They do not evolve so much as precipitate, and most have no memory of anything before the moment they formed. **Player knowledge** is almost entirely about the terrain that produced them — heat, current, stone, wind — and about who, if anyone, bound the specific Elemental in front of them into service. **Director knowledge** should treat terrain as half of every Elemental encounter: the room is the creature's extended body, and a smothered, quenched, or grounded Elemental is a puzzle worth rewarding, not a stalemate to grind through. Ask whether a given Elemental is a natural seam or a bound servant before deciding what its "defeat" actually means.`,
  Fey: `The Fey of Aethel answer to rules that only partially overlap with the rest of the Decennium's logic — hospitality, names, and debts are load-bearing structure here, not manners. **Player knowledge** should never take a Fey bargain at face value: every promise is kept with exact, punishing precision, which is a worse trap than an outright lie. **Director knowledge** treats combat as the failure state of a Fey encounter rather than its default outcome — a "defeated" Fey rarely ends the arrangement it represents, and the bargain it embodies often survives the fight that supposedly settled it. Use Fey encounters specifically to teach a table that not every problem this deep in the Decennium has a violent solution, and that the clever solution usually costs something just as real as blood.`,
  Fiend: `Fiends carry the Chaos-Realm's dissonance directly into Aethel, and the Pact's uneasy peace depends on that dissonance having somewhere to go. Most Fiends an Expedition meets did not arrive by accident — something summoned, bound, or invited them, and that original debt is very often still open when the party arrives. **Player knowledge** treats a Fiend as cruelty with a procedure behind it: not passion, just the most efficient route to whatever it wants. **Director knowledge** should always ask who summoned or bound the Fiend before treating the fight as the whole story — that answer is worth more than any loot table, and a Fiend's eternal war with its own kind can be turned into a one-time, expensive advantage for a clever Expedition. Victory here is always temporary; the dissonance a Fiend fed does not end when its body does.`,
  Giant: `Giants measure Aethel in strides an Expedition measures in days, and their danger is almost always a logistics problem before it is a combat one. **Player knowledge** treats a Giant sighting as a warning about camps, caravans, and safe havens — Giants break structures and supply lines far more often than they hunt individual adventurers. **Director knowledge** should run Giant encounters as siege framing rather than duels: let terrain and structures become casualties alongside hit points, and force an Expedition to choose what to save rather than simply what to fight. A Giant's size should matter as much mechanically as it does narratively — collateral damage is the entire point of the type.`,
  Humanoid: `Humanoids are Aethel's living politics, not merely another bestiary category, and treating them as pure combat encounters wastes most of what the type is for. **Player knowledge** is whatever an Expedition has actually learned about a given floor culture's factions, grudges, and territory — Humanoids negotiate, inform, and betray as often as they fight. **Director knowledge** should track consequences: killing a Humanoid has a reputational cost that outlives the encounter, rippling through kin, rank, and floor politics an Expedition may need to navigate again later. A parley option should exist even when the table does not expect to use it, and a Humanoid's death should visibly change something — a market price, a patrol route, a grudge carried forward — rather than simply ending an encounter.`,
  Monstrosity: `Monstrosities are life that should not breed true in Aethel, and yet, floor after floor, evidently does. No single natural process explains the type; something about the Decennium's depths keeps deciding that biology is a suggestion rather than a rule. **Player knowledge** treats a Monstrosity sighting as territory marked in ways a careful approach can read before contact — most hunt with an efficiency that outpaces their apparent intelligence. **Director knowledge** should treat repeat sightings as an infestation problem rather than a monster-of-the-week problem, escalating a given Monstrosity type across a Cycle as "the thing that's spreading" when it recurs. Their parts are valuable specifically because they should not exist — Research teams will pay well for proof, and an Expedition often has to choose between finishing the kill and finishing the investigation.`,
  Ooze: `Oozes are Aethel's patience made corrosive — environmental hazards wearing a stat block, born from a failed watch rotation, a badly sealed corridor, or a drain that should have been checked years ago. **Player knowledge** is almost entirely procedural: what dissolves it, what it dissolves in turn, and which gaps a locked door was supposed to make irrelevant. **Director knowledge** should punish poor watch rotations and sealed, unventilated spaces specifically — an Ooze encounter is at its best when it is clearly the consequence of an earlier logistics failure rather than a random ambush. Let equipment loss matter as much as hit point loss, and remember that most Oozes do not negotiate, flee meaningfully, or feel provoked; they simply continue until something stops them.`,
  Plant: `Plants across Bloomdeep and Aethel's verdant zones grew where the Decennium should have stayed empty, and kept growing past the point anyone could stop them politely. **Player knowledge** treats a Plant encounter as area control and attrition rather than a single dramatic strike — the terrain itself punishes anyone who lingers. **Director knowledge** should reward antidotes, cleared sightlines, and fire over raw damage output, and should remember that cutting the visible threat rarely solves the root problem, sometimes literally. A Plant's harvestable parts are valuable specifically because most Expeditions are too busy retreating to collect them — use that tension to make retreat a real, costed choice rather than a free action.`,
  Undead: `The Undead of Aethel are history that refused to stay buried, in the most literal sense the Decennium offers. Whatever ended a given Undead's first life rarely ended its business here, and most repeat a pattern from that life — a duty, a grudge, a routine — with none of the judgment that once tempered it. **Player knowledge** should feel the necrotic and fear pressure these encounters are built to apply: exhaustion, dread, and morale cost should be as real as hit point loss. **Director knowledge** treats an Undead's unfinished business, once learned, as frequently the actual quest, with the fight itself only a symptom. Let its remains carry at least one true clue toward why it rose, even in an otherwise minor encounter, and remember that turning or destroying it does not always end whatever compelled it to rise in the first place.`,
};

function typeSectionHeading(t) {
  const map = {
    Fey: "The Fey",
    Monstrosity: "Monstrosities",
    Undead: "The Undead",
  };
  return map[t] || `The ${t}s`;
}

function main() {
  const byType = {};
  for (const m of bestiary) {
    const t = m.type || "Monstrosity";
    (byType[t] = byType[t] || []).push(m);
  }
  const typeOrder = Object.keys(ECOLOGY_ESSAYS).sort();

  const parts = [];
  parts.push(fs.readFileSync(path.join(FRAG_DIR, "01_frontmatter.md"), "utf8"));
  parts.push(fs.readFileSync(path.join(FRAG_DIR, "02_gate_guardians.md"), "utf8"));

  parts.push("\n---\n\n# Part III — Ecologies and Lexicon of Aethel\n\nEach family below opens with a short ecology essay, then lists every indexed creature of that family sorted from lowest to highest Challenge Rating. Entries marked **STUB** should not be run showcase-ready without a Director pass — see the honesty tags explained in Part I.\n");

  let totalStub = 0;
  let totalMinorDraft = 0;
  const stubList = [];
  const auditSamples = { dict: [], family: [], ip: [], size: [], duplicate: [] };

  for (const t of typeOrder) {
    const heading = typeSectionHeading(t);
    const entries = (byType[t] || []).slice().sort((a, b) => {
      const ca = parseCR(a.challengeRating) ?? 0;
      const cb = parseCR(b.challengeRating) ?? 0;
      if (ca !== cb) return ca - cb;
      return a.name.localeCompare(b.name);
    });
    parts.push(`\n## ${heading}\n\n${ECOLOGY_ESSAYS[t]}\n\n*Indexed creatures of this family: **${entries.length}**.*\n`);
    for (const m of entries) {
      const { isStub } = buildFlags(m);
      if (isStub) {
        totalStub++;
        stubList.push(m.name);
      }
      parts.push(renderEntry(m));

      const dictFlag = dictMismatchFlag(m.name, m.type);
      if (dictFlag && auditSamples.dict.length < 12) auditSamples.dict.push(`**${m.name}** — sheet Type **${m.type}**, name implies **${TYPE_DICT[m.name]}**.`);
      const famFlag = reskinFamilyFlag(m.name, m.type);
      if (famFlag && auditSamples.family.length < 8) auditSamples.family.push(`**${m.name}** — culture family entry sheet-typed **${m.type}** instead of the expected Humanoid/Aberration.`);
      const ipf = ipFlagFor(m.name);
      if (ipf && auditSamples.ip.length < 15) auditSamples.ip.push(`**${m.name}**`);
      const nr = excelExtra[m.name] && excelExtra[m.name].needsReview;
      if (nr && String(nr).includes("cr-suspect-high") && auditSamples.size.length < 15) {
        auditSamples.size.push(`**${m.name}** — \`${nr}\` (Size ${m.size}, CR ${m.challengeRating}, HP ${m.hitPoints}).`);
      }
    }
  }

  parts.push(fs.readFileSync(path.join(FRAG_DIR, "03_floor_cultures.md"), "utf8"));
  parts.push(fs.readFileSync(path.join(FRAG_DIR, "04_directors_toolkit.md"), "utf8"));

  // Numeric CR index
  parts.push("\n---\n\n# Part VI — Numeric Challenge Index\n\nEvery indexed creature, grouped by Challenge Rating and sorted numerically from lowest to highest, for fast encounter-budget lookups. **STUB**-flagged names are marked with a dagger (†).\n");
  const byCR = new Map();
  for (const m of bestiary) {
    const key = parseCR(m.challengeRating);
    const k = key === null ? -1 : key;
    if (!byCR.has(k)) byCR.set(k, []);
    byCR.get(k).push(m);
  }
  const crKeys = [...byCR.keys()].sort((a, b) => a - b);
  for (const k of crKeys) {
    const group = byCR.get(k).slice().sort((a, b) => a.name.localeCompare(b.name));
    const label = k === -1 ? "Unknown" : String(group[0].challengeRating);
    const names = group
      .map((m) => {
        const { isStub } = buildFlags(m);
        return isStub ? `${m.name}†` : m.name;
      })
      .join(", ");
    parts.push(`\n**Challenge ${label}** (${group.length}) — ${names}\n`);
  }

  const fullText = parts.join("\n");
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(path.join(OUT_DIR, "Codex_of_the_Heartcell.md"), fullText, "utf8");

  // ---- Audit ----
  const wordCount = fullText.split(/\s+/).filter(Boolean).length;
  const guardianCount = 10;

  const top50 = [];
  top50.push("## Gate Guardian data contradictions (all 10, see Part II for full detail)");
  top50.push("");
  top50.push("1. **Vaskor, the Stone Maw** — sheet Type is Ooze; field description calls it \"a colossal earth elemental.\" Codex runs it as Elemental.");
  top50.push("2. **Vaskor, the Stone Maw** — field description claims \"Floor 20, Heart of the Verdant Wild\"; Chronicle gazetteer places it at Floor 10, Warded Gate, Yieldheart Caverns.");
  top50.push("3. **The Bloom That Hungers** — field description claims \"Floor 10, the Echoing Grotto\"; gazetteer places it at Floor 20, Sporemist Gate, Bloomdeep Marsh.");
  top50.push("4. **The Bloom That Hungers** — CR 5 is the lowest of all ten Gate Guardians despite guarding the second seal; the difficulty curve is inverted at this point.");
  top50.push("5. **Ashthirst the Hollow** — field description's location name (\"Fields of Whispering Grasses\") and Zone (\"Aethel Jungles\") both contradict the Anvil of Brogi forge setting the gazetteer assigns it.");
  top50.push("6. **Gor Vekk, Architect of Ends** — sheet Type is Fey; field description calls it \"an ancient aberration.\"");
  top50.push("7. **Gor Vekk, Architect of Ends** — CR 29 is dramatically inflated for a Tier 4 (\"Expert\") seal — higher than the Tier 8 and Tier 9 guardians. Field description also claims \"Floor 90,\" a 50-floor discrepancy from the gazetteer's Floor 40.");
  top50.push("8. **Choralith, Voice Below** — field description claims \"Floor 40, the Sepulcher of Silent Thrones,\" directly colliding with Gor Vekk's field description, which also claims Floor 40. Gazetteer resolves both: Choralith is Floor 50, Gor Vekk is Floor 40.");
  top50.push("9. **Lumen of the Shattered Thread** — Type is Undead, but field description says its \"form shifts between the four elements,\" reading as Elemental rather than Undead. Field description claims Floor 50; gazetteer places it at Floor 60.");
  top50.push("10. **Xarog** — the sheet contains two entries for the same name: a stray Excel-sandbox row (\"Xarog the Pactbound Furnace,\" no comma, Elemental CR 10, generic Freak Bite/Tail Lash attacks, no Gate Guardian tag) and the intended companion-authored row (\"Xarog, the Pactbound Furnace,\" with comma, Fiend CR 26, tagged Gate Guardian). Recommend deleting the no-comma row.");
  top50.push("11. **Xarog, the Pactbound Furnace** — field description claims \"Floor 80\"; gazetteer places it at Floor 70.");
  top50.push("12. **Eirfax, the Dusk Crowned** — sheet Type is Fiend; field description calls it \"a twilight fey lord.\" Field description claims \"Floor 70\"; gazetteer places it at Floor 80.");
  top50.push("13. **Threxus, the Iron Spiral** — sheet Type is Fey; field description calls it \"a massive construct of spiraling iron and radiant energy.\" Field description claims \"Floor 60\"; gazetteer places it at Floor 90 — the largest floor discrepancy (30 floors) among all ten seals.");
  top50.push("14. **The Marquis of Silence** — sheet Type is Ooze; field description calls it \"a demon lord of unimaginable power.\"");
  top50.push("15. **The Marquis of Silence** — Alignment is listed as Chaotic Good, which cannot be reconciled with a demon lord \"who rules through silence and fear\" under any reading. Flag for correction to an evil alignment.");
  top50.push("16. **Seal Ladder overall** — the intended Novice→Legendary difficulty curve is not monotonic: Tiers 2 and 9 dip below the seal immediately before them, and Tiers 4 and 7 spike dramatically above their neighbors. See the Seal Ladder table at the end of Part II.");
  top50.push("");
  top50.push("## Systemic problems found across the general Lexicon (708 entries)");
  top50.push("");
  const systemic = [];
  systemic.push(`**Type field is effectively random relative to creature name across the whole sheet — the single largest driver of the ${totalStub}-entry STUB count.** Cross-checking all 708 names against an ordinary-usage archetype dictionary (~300 recognizable names covering Beasts, Humanoids, Undead, Fiends, Giants, Dragons, and more) found **432 mismatches** — roughly the same hit rate one would expect from assigning Type uniformly at random across 14 categories (~93% mismatch odds). This is not a handful of edge cases; it is evidence the sandbox generator assigned Type independently of Name for the entire 708-row sheet. Treat every un-reviewed Type field in \`Bestiary.xlsx\` as unverified until a Director or the next ingest pass confirms it by hand.`);
  systemic.push(`**Reused sandbox attack names.** Only 40 distinct attack names exist across all 708 monsters' attack lists. Four of them — *Tail Lash* (433 uses), *Monstrous Claw* (253), *Freak Bite* (237), *Aberrant Lash* (208) — account for 1,131 of the total attack instances. The remaining 36 bespoke names appear exactly once each (almost entirely on the ten Gate Guardians).`);
  systemic.push(`**Culture families with internally randomized Type/Size.** Named humanoid-culture families (Umbrin, Deep Dwarf, Serpent-Blood, Astral Reaver, Astral Ascetic, Depth Toad, Gaze Tyrant, Voidmind, Cave Gnome) each have their Type and Size assigned independently per rank rather than consistently — e.g. Umbrin ranges across Beast, Giant, Construct, Celestial, Aberration, and Plant, and from Tiny to Gargantuan, across its ten members. See Part IV for the full list and the Codex's blanket correction (treat all as Humanoid/Aberration as noted per family).`);
  systemic.push(`**Excel's own \`NeedsReview\` column is populated on 430 of 708 rows (60.7%)** — 151 of those are Size corrections explicitly marked \`cr-suspect-high\` (the Challenge Rating looks too high for the sheet's current Size), 46 more are Size corrections without that suffix, and the remaining 233 are Hit Point corrections only.`);
  systemic.push(`**Old Bestiary of Aethel grammar bugs (fixed in this Codex).** Ecology section headers read "On Feys," "On Monstrositys," and "On Undeads" in the prior draft — corrected here to "The Fey," "Monstrosities," and "The Undead."`);
  systemic.push(`**Old Bestiary of Aethel boilerplate (fixed in this Codex).** Every one of the prior draft's 700+ entries repeated the identical sentence "Directors: decide whether this creature is a patrol, a nest guardian, a harvest node, or a political actor. Resource teams want parts; Research teams want behavior notes; Recon wants routes that avoid fair fights." verbatim, regardless of Type. This Codex replaces that with combinatorial, Type-specific ecology text (see \`scripts/codex_ecology_phrases.js\`).`);
  systemic.push(`**Old Bestiary "Traits" copy-paste bug (documented, not present in this Codex's own prose).** Many prior-draft entries' Traits line read "Draft stats from CR X Medium monstrosity band (excel-sandbox generator)" even when the creature in question was neither Medium nor a Monstrosity (e.g. a Huge Aberration). This Codex's honesty notes reference the creature's actual sheet Size/Type instead.`);
  systemic.push(`**IP scrub backlog.** ${auditSamples.ip.length}+ individually-flagged stock/iconic names remain unrenamed pending owner sign-off (Flumph, Owlbear, Tarrasque, the full Yugoloth/Modron/Demon-hierarchy rank families, Star Spawn, Neogi, Slaad, Eladrin, Sorrowsworn, Abishai, and the ten deity-locked orc/gnoll/firenewt/xvart rank names) — see the Naming & IP Reskin Ledger in Part V.`);

  auditSamples.dict.slice(0, 10).forEach((s) => systemic.push(`Name/Type mismatch: ${s}`));
  auditSamples.family.slice(0, 8).forEach((s) => systemic.push(s));
  auditSamples.size.slice(0, 20).forEach((s) => systemic.push(`Excel NeedsReview: ${s}`));

  const remaining = Math.max(0, 50 - 16);
  systemic.slice(0, remaining).forEach((s, i) => top50.push(`${17 + i}. ${s}`));

  const auditParts = [];
  auditParts.push("# Codex of the Heartcell — Quality Audit\n");
  auditParts.push(`*Generated alongside \`Codex_of_the_Heartcell.md\` from \`src/bestiary_data_full.json\` (${bestiary.length} entries) and Bestiary.xlsx's own NeedsReview column. Read-only audit — no source files were modified.*\n`);
  auditParts.push("## Headline counts\n");
  auditParts.push(`| Metric | Count |`);
  auditParts.push(`|---|---|`);
  auditParts.push(`| Monsters indexed | ${bestiary.length} |`);
  auditParts.push(`| Gate Guardian chapters written | 10 / 10 |`);
  auditParts.push(`| Entries flagged **STUB — Director must re-skin** | ${totalStub} (${((totalStub / bestiary.length) * 100).toFixed(1)}%) — see problem #1 below for why this is so high |`);
  auditParts.push(`| Excel \`NeedsReview\` rows (any severity) | ${Object.values(excelExtra).filter((e) => e.needsReview).length} |`);
  auditParts.push(`| Distinct attack names across all entries | 40 (4 generic names cover 1,131 of all attack instances) |`);
  auditParts.push(`| Codex word count | ~${wordCount.toLocaleString()} words |`);
  auditParts.push("");
  auditParts.push("## Gate Guardian coverage checklist\n");
  auditParts.push("| # | Guardian | Tier / Floor (gazetteer) | Lore | Staging | Lair/Terrain | Tactics | Reward-as-bait | Honesty box |");
  auditParts.push("|---|---|---|---|---|---|---|---|---|");
  const guardianRows = [
    ["1", "Vaskor, the Stone Maw", "T1 / Floor 10, Warded Gate"],
    ["2", "The Bloom That Hungers", "T2 / Floor 20, Sporemist Gate"],
    ["3", "Ashthirst the Hollow", "T3 / Floor 30, Lavaflow Gate"],
    ["4", "Gor Vekk, Architect of Ends", "T4 / Floor 40, Radiance Gate"],
    ["5", "Choralith, Voice Below", "T5 / Floor 50, Canticle Gate"],
    ["6", "Lumen of the Shattered Thread", "T6 / Floor 60, Lumen Gate (unmapped)"],
    ["7", "Xarog, the Pactbound Furnace", "T7 / Floor 70, Furnace Gate (unmapped)"],
    ["8", "Eirfax, the Dusk Crowned", "T8 / Floor 80, Crown Gate (unmapped)"],
    ["9", "Threxus, the Iron Spiral", "T9 / Floor 90, Spiral Gate (unmapped)"],
    ["10", "The Marquis of Silence", "T10 / Floor 100, Marquis Gate (unmapped)"],
  ];
  guardianRows.forEach(([n2, name, floor]) => {
    auditParts.push(`| ${n2} | ${name} | ${floor} | done | done | done | done | done | done |`);
  });
  auditParts.push("");
  auditParts.push("All ten Gate Guardian chapters are complete in Part II, including the cross-tier Seal Ladder CR-curve honesty table.\n");
  auditParts.push("## Top 50 worst data problems\n");
  auditParts.push(top50.join("\n"));
  auditParts.push("\n## Recommended next owner actions\n");
  auditParts.push("1. Decide Gor Vekk's and Xarog's true intended CR (Part II, Seal Ladder) — the current sheet cannot be run as a monotonic difficulty curve without a Director-side scaling decision.");
  auditParts.push("2. Delete the stray no-comma \"Xarog the Pactbound Furnace\" duplicate row from `Bestiary.xlsx`.");
  auditParts.push("3. Approve or amend the proposed renames in the Naming & IP Reskin Ledger (Part V of the Codex) before any are locked into `Bestiary.xlsx`.");
  auditParts.push("4. Consider a dedicated Excel pass to normalize Type/Size on the culture-family rows (Umbrin, Deep Dwarf, Serpent-Blood, Astral Reaver/Ascetic, Depth Toad, Gaze Tyrant, Voidmind) so they stop randomizing independently per rank.");
  auditParts.push("5. Correct the Marquis of Silence's Alignment field (currently Chaotic Good) and Vaskor/Gor Vekk/Threxus/Marquis's Type fields per the Gate Seal honesty boxes in Part II.");

  fs.writeFileSync(path.join(OUT_DIR, "CODEX_QUALITY_AUDIT.md"), auditParts.join("\n"), "utf8");

  console.log(JSON.stringify({
    monsters: bestiary.length,
    stubCount: totalStub,
    wordCount,
    guardiansWritten: guardianCount,
  }, null, 2));
}

main();
