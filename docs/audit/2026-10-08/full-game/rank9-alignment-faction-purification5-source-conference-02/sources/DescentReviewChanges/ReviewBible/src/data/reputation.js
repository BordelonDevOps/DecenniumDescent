/**
 * Reputation factions and tiers — Decennium Descent Ch4 + Weave Resonance tracks.
 * @see docs/mechanics/REPUTATION.md
 */

/** @typedef {{ id: string; name: string; category: string; description?: string; draft?: boolean; resonanceTrack?: boolean }} Faction */

/** @typedef {Record<string, number>} ReputationScores */

export const REPUTATION_TIERS = [
  { id: "hated", label: "Hated", min: -Infinity, max: -2 },
  { id: "disliked", label: "Disliked", min: -1, max: -1 },
  { id: "neutral", label: "Neutral", min: 0, max: 0 },
  { id: "liked", label: "Liked", min: 1, max: 1 },
  { id: "honored", label: "Honored", min: 2, max: Infinity },
];

/** @type {Faction[]} */
export const FACTIONS = [
  // Rulebook Ch Weave — Resonance reputation tracks (canon)
  {
    id: "academic-factions",
    name: "Academic Factions",
    category: "Resonance track",
    resonanceTrack: true,
    description: "Scholars, archivists, and plane-touched academies that gate rare lore.",
  },
  {
    id: "religious-orders",
    name: "Religious Orders",
    category: "Resonance track",
    resonanceTrack: true,
    description: "Temples and choir-backed orders whose favor steadies divine Weave work.",
  },
  {
    id: "arcane-guilds",
    name: "Arcane Guilds",
    category: "Resonance track",
    resonanceTrack: true,
    description: "Registered mage houses and guild halls that regulate arcane commerce.",
  },
  {
    id: "nature-circles",
    name: "Nature Circles",
    category: "Resonance track",
    resonanceTrack: true,
    description: "Druidic circles and wildling pacts tied to primal Weave regeneration.",
  },
  // Ch4 background factions (rulebook prose)
  {
    id: "aethel-authorities",
    name: "Aethel Authorities",
    category: "Civic",
    description: "City Guard, magistrates, and crown agents along the Shardspire routes.",
  },
  {
    id: "common-folk",
    name: "Common Folk",
    category: "Civic",
    description: "Market workers, refugees, and neighborhood folk who remember who helped them.",
  },
  {
    id: "arcane-institutions",
    name: "Formal Arcane Institutions",
    category: "Arcane",
    description: "Academies and licensed colleges that credential spellwrights.",
  },
  {
    id: "independent-mages",
    name: "Independent Mages",
    category: "Arcane",
    description: "Unregistered casters, hedge mages, and free scholars outside guild rolls.",
  },
  {
    id: "war-veterans",
    name: "War Veterans",
    category: "Military",
    description: "Survivors of Aethel's border wars and expeditionary companies.",
  },
  {
    id: "opposing-forces",
    name: "Opposing Forces",
    category: "Military",
    description: "Enemy banners and mercenary bands from conflicts you once fought.",
  },
  {
    id: "cleansing-orders",
    name: "Cleansing Orders",
    category: "Faith",
    description: "Orders that hunt corruption, rift bleed, and spiral-touched blight.",
  },
  {
    id: "corruption-scholars",
    name: "Corruption Scholars",
    category: "Arcane",
    description: "Researchers who study taint for power — tolerated only in whispers.",
    draft: true,
  },
  {
    id: "dark-cults",
    name: "Dark Cults",
    category: "Underworld",
    description: "Secretive cult cells, former patrons, and spiral cult remnants.",
  },
  {
    id: "anti-cult-groups",
    name: "Anti-Cult Alliances",
    category: "Faith",
    description: "Inquisitors, vigilantes, and lay networks that break cult chains.",
  },
  {
    id: "planar-scholars",
    name: "Planar Scholars",
    category: "Planar",
    description: "Multiverse archivists and rift cartographers who trade in crossing-lore.",
  },
  {
    id: "mundane-authorities",
    name: "Mundane Authorities",
    category: "Civic",
    description: "Skeptical officials who distrust rift-scarred or planar-touched folk.",
  },
  {
    id: "established-nobility",
    name: "Established Nobility",
    category: "Civic",
    description: "Old houses, courtiers, and scandal-watchers along the ascent routes.",
  },
  {
    id: "underworld",
    name: "Underworld",
    category: "Underworld",
    description: "Smugglers, syndicates, and revolutionary cells beneath Aethel's streets.",
  },
  {
    id: "druidic-circles",
    name: "Druidic Circles",
    category: "Wild",
    description: "Circle groves and oath-bound wardens of the wild margins.",
  },
  {
    id: "wildling-communities",
    name: "Wildling Communities",
    category: "Wild",
    description: "Isolated camps and fringe villages that trust the land over crowns.",
  },
  {
    id: "alchemists-guilds",
    name: "Alchemists Guilds",
    category: "Trade",
    description: "Guild distilleries and apothecary chains that guard recipe monopolies.",
  },
  {
    id: "artisan-guilds",
    name: "Artisan Guilds",
    category: "Trade",
    description: "Craft houses you trained under — or fled from.",
  },
  {
    id: "rival-guilds",
    name: "Rival Guilds & Independents",
    category: "Trade",
    description: "Competing craft leagues and unguilded masters.",
  },
  {
    id: "mainstream-faith",
    name: "Mainstream Religious Orders",
    category: "Faith",
    description: "Dominant temple hierarchies wary of fringe history and old pantheon talk.",
  },
  {
    id: "fringe-historians",
    name: "Fringe Historians",
    category: "Lore",
    description: "Hidden archivists, old-tradition keepers, and lost-pantheon seekers.",
  },
  {
    id: "underground-resistance",
    name: "Underground Resistance",
    category: "Underworld",
    description: "Cells that shelter fugitives and stolen relics from tyrannical powers.",
  },
  {
    id: "marked-pursuers",
    name: "Marked Pursuers",
    category: "Underworld",
    description: "The faction or order hunting what you stole — name varies by story.",
    draft: true,
  },
  {
    id: "merchant-guilds",
    name: "Merchant Guilds",
    category: "Trade",
    description: "Caravan masters and trade-company factors who fund expeditions.",
  },
  {
    id: "explorers-societies",
    name: "Explorers Societies",
    category: "Lore",
    description: "Societies that publish maps, fund delves, and argue over first claims.",
  },
  {
    id: "indigenous-tribes",
    name: "Indigenous Tribes",
    category: "Wild",
    description: "Peoples whose lands are mapped, mined, or crossed without invitation.",
  },
  {
    id: "planar-trading-guilds",
    name: "Planar Trading Guilds",
    category: "Planar",
    description: "Cross-plane merchants who broker relics and passage contracts.",
  },
  {
    id: "planar-customs",
    name: "Planar Customs Authorities",
    category: "Planar",
    description: "Inspectors who suspect smuggling through rift gates and echo ports.",
  },
  {
    id: "museums-collectors",
    name: "Museums & Collectors",
    category: "Lore",
    description: "Curators and private buyers hungry for relic provenance.",
  },
  {
    id: "indigenous-peoples",
    name: "Indigenous Peoples",
    category: "Wild",
    description: "Communities whose sacred sites are looted by relic hunters.",
    draft: true,
  },
  {
    id: "frontier-communities",
    name: "Frontier Communities",
    category: "Wild",
    description: "Settlements on the edge of mapped Aethel that trade grit for protection.",
  },
  {
    id: "urban-elites",
    name: "Urban Elites",
    category: "Civic",
    description: "Capital patrons who fund expeditions but disdain frontier hardship.",
    draft: true,
  },
  {
    id: "law-enforcement",
    name: "Law Enforcement",
    category: "Civic",
    description: "Watch captains and bounty boards with long memories.",
  },
  {
    id: "reformed-criminals",
    name: "Reformed Criminals",
    category: "Underworld",
    description: "Former syndicate members trying to walk a straighter path.",
    draft: true,
  },
  {
    id: "elemental-cultists",
    name: "Elemental Cultists",
    category: "Planar",
    description: "Cults that venerate a single elemental thread of the Weave.",
    draft: true,
  },
  {
    id: "opposing-elemental",
    name: "Opposing Elemental Factions",
    category: "Planar",
    description: "Rival element cults and primordial zealots.",
    draft: true,
  },
  {
    id: "good-temples",
    name: "Good-Aligned Temples",
    category: "Faith",
    description: "Temples and choir-backed charities that recognize celestial emissaries.",
  },
  {
    id: "fiendish-cults",
    name: "Fiendish Cults",
    category: "Underworld",
    description: "Infernal and abyssal cells that hunt celestial agents.",
  },
  {
    id: "prophecy-believers",
    name: "Believers in Prophecy",
    category: "Lore",
    description: "Communities that see your fate written in the Tenfold cycles.",
    draft: true,
  },
  {
    id: "prophecy-fearful",
    name: "Prophecy-Fearful",
    category: "Lore",
    description: "Authorities and cults that dread what your foretold path may unleash.",
    draft: true,
  },
];

const FACTION_BY_ID = Object.fromEntries(FACTIONS.map((f) => [f.id, f]));

/** Background → starting faction scores (Ch4 rulebook backgrounds). */
export const BACKGROUND_STARTING_REPUTATION = {
  "Aethel City Guard Veteran": {
    "aethel-authorities": 0,
    "common-folk": 1,
  },
  "Arcane Academy Dropout": {
    "arcane-institutions": -1,
    "independent-mages": 0,
    "academic-factions": -1,
  },
  "Battlefield Medic": {
    "war-veterans": 1,
    "opposing-forces": 0,
  },
  "Corruption Survivor": {
    "cleansing-orders": 1,
    "corruption-scholars": -1,
  },
  "Cult Escapee": {
    "dark-cults": -2,
    "anti-cult-groups": 1,
    "religious-orders": 1,
  },
  "Dimensional Refugee": {
    "common-folk": 0,
    "planar-scholars": 1,
    "academic-factions": 0,
  },
  "Disgraced Noble Scion": {
    "established-nobility": -1,
    "underworld": 0,
  },
  "Expedition Cartographer": {
    "merchant-guilds": 1,
    "explorers-societies": 1,
    "indigenous-tribes": 0,
  },
  "Frontier Settler": {
    "frontier-communities": 1,
    "urban-elites": 0,
    "nature-circles": 0,
  },
  "Guild Artisan Dropout": {
    "artisan-guilds": -1,
    "rival-guilds": 0,
  },
  "Marked Fugitive": {
    "underground-resistance": 1,
    "marked-pursuers": -2,
  },
  "Planar Merchant": {
    "planar-trading-guilds": 1,
    "planar-customs": -1,
  },
  "Relic Hunter": {
    "museums-collectors": 1,
    "indigenous-peoples": -1,
  },
  "Rift Scarred Survivor": {
    "planar-scholars": 0,
    "mundane-authorities": -1,
  },
  "Seeker of the Lost Pantheon": {
    "mainstream-faith": 0,
    "fringe-historians": 1,
    "religious-orders": 0,
  },
  "Wildling Herbalist": {
    "druidic-circles": 1,
    "wildling-communities": 1,
    "alchemists-guilds": -1,
    "nature-circles": 1,
  },
  "Prophecy Bearer": {
    "prophecy-believers": 1,
    "prophecy-fearful": -1,
  },
  "Underworld Escapee": {
    "law-enforcement": -1,
    "underworld": -2,
    "reformed-criminals": 0,
  },
  "Elemental Touched": {
    "elemental-cultists": 1,
    "opposing-elemental": -1,
  },
  "Celestial Emissary": {
    "good-temples": 1,
    "fiendish-cults": -2,
    "religious-orders": 1,
  },
};

export function getFactionById(id) {
  return FACTION_BY_ID[id] || null;
}

export function tierFromScore(score) {
  const n = Number(score) || 0;
  return REPUTATION_TIERS.find((t) => n >= t.min && n <= t.max) || REPUTATION_TIERS[2];
}

export function tierLabel(score) {
  return tierFromScore(score).label;
}

export function scoreFromTierLabel(label) {
  const normalized = String(label || "").trim().toLowerCase();
  const map = {
    hated: -2,
    disliked: -1,
    neutral: 0,
    liked: 1,
    honored: 2,
  };
  return map[normalized] ?? 0;
}

/** Clamp reputation score to playable range. */
export function clampReputationScore(score) {
  return Math.max(-3, Math.min(3, Math.round(Number(score) || 0)));
}

/** Normalize persisted reputation object. */
export function normalizeReputation(raw) {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return {};
  /** @type {ReputationScores} */
  const out = {};
  for (const [key, val] of Object.entries(raw)) {
    if (getFactionById(key)) out[key] = clampReputationScore(val);
  }
  return out;
}

export function emptyReputation() {
  return /** @type {ReputationScores} */ ({});
}

export function getStartingReputationForBackground(backgroundName) {
  const starts = BACKGROUND_STARTING_REPUTATION[backgroundName];
  if (!starts) return emptyReputation();
  /** @type {ReputationScores} */
  const out = {};
  for (const [factionId, score] of Object.entries(starts)) {
    out[factionId] = clampReputationScore(score);
  }
  return out;
}

/**
 * Merge background starting scores onto existing (background keys win).
 * @param {ReputationScores | undefined} existing
 * @param {string} backgroundName
 */
export function applyBackgroundReputation(existing, backgroundName) {
  const starts = getStartingReputationForBackground(backgroundName);
  return { ...normalizeReputation(existing), ...starts };
}

export function adjustReputationScore(scores, factionId, delta) {
  const base = normalizeReputation(scores);
  const current = base[factionId] ?? 0;
  return { ...base, [factionId]: clampReputationScore(current + delta) };
}

export function setReputationScore(scores, factionId, score) {
  return { ...normalizeReputation(scores), [factionId]: clampReputationScore(score) };
}

/** Factions with non-zero scores, sorted by name. */
export function activeReputationEntries(scores) {
  const norm = normalizeReputation(scores);
  return Object.entries(norm)
    .filter(([, score]) => score !== 0)
    .map(([factionId, score]) => ({
      factionId,
      faction: getFactionById(factionId),
      score,
      tier: tierFromScore(score),
    }))
    .filter((e) => e.faction)
    .sort((a, b) => a.faction.name.localeCompare(b.faction.name));
}

/** All factions for editor UI — resonance tracks first, then by category. */
export function factionsForEditor() {
  const categoryOrder = ["Resonance track", "Civic", "Faith", "Arcane", "Wild", "Trade", "Lore", "Military", "Planar", "Underworld"];
  return [...FACTIONS].sort((a, b) => {
    const ai = categoryOrder.indexOf(a.category);
    const bi = categoryOrder.indexOf(b.category);
    if (ai !== bi) return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
    return a.name.localeCompare(b.name);
  });
}

export function reputationSummary(scores) {
  const entries = activeReputationEntries(scores);
  if (!entries.length) return "All factions Neutral (unset scores count as 0).";
  return entries.map((e) => `${e.faction.name}: ${e.tier.label}`).join(" · ");
}

export const FACTION_COUNT = FACTIONS.length;
export const RESONANCE_TRACK_COUNT = FACTIONS.filter((f) => f.resonanceTrack).length;
