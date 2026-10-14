/**
 * Draft bounded ceiling caps for high-risk classes (playtest guardrails).
 *
 * Canon status: **draft only** — informational callouts in Builder/Sheet.
 * Source: docs/mechanics/CLASS_CEILING_CAPS.md · BALANCE_PLAYER_CLASSES.md §3
 * Continuity: Worker 3 · 2026-07-30
 *
 * These caps do NOT enforce mechanics in code; they surface playtest limits only.
 */

/** @typedef {{ category: string; cap: string; note?: string }} CeilingCapRow */

/** @typedef {{ summary: string; caps: CeilingCapRow[]; playtestLedger: string[] }} ClassCeilingProfile */

/** @type {Record<string, ClassCeilingProfile>} */
export const CLASS_CEILING_CAPS = {
  Mirrorsage: {
    summary:
      "Adaptive copier — bound echo slots, copy releases per round, RP discount floor, and boss-unique exclusions.",
    caps: [
      { category: "Actions / round", cap: "1 witnessed copy release", note: "Action or bonus action, not both" },
      { category: "Echo slots", cap: "6 concurrent (L11+); 1 permanent Infinite Reflection (L20)" },
      {
        category: "Copy eligibility",
        cap: "No legendary, 1/day, 1/encounter, or boss-unique effects",
        note: "Copied tier cannot exceed source owner's level gate",
      },
      { category: "RP discount", cap: "Half-cost min 1 RP; max 2 RP discount / round" },
      { category: "Mirror Beast", cap: "2 shifts / encounter (L16+); no extra copy release on shift" },
    ],
    playtestLedger: ["Echo slot contents", "Copy releases / round", "RP spent on echoes"],
  },
  Oracle: {
    summary:
      "Revelation support/control — strict RC pool, 1 RC recovery per round, and turn-denial per-target caps.",
    caps: [
      { category: "RC pool", cap: "3–7 max; no short-rest recovery" },
      { category: "RC recovery / round", cap: "1 from all Prophecy Triggers combined" },
      { category: "Actions / round", cap: "1 Revelation activation", note: "Tier III (3 RC) = one activation" },
      { category: "Turn denial", cap: "1 hard deny / target / encounter", note: "Stun, skip turn, auto-fail" },
      { category: "Prophetic Surge", cap: "1 / day", note: "Does not bypass 1 RC / round recovery cap" },
    ],
    playtestLedger: ["RC start/end per round", "Trigger source", "Revelations activated"],
  },
  Paladin: {
    summary:
      "Armored striker + aura support — compress smite/spell riders, aura stacking, and Lay on Hands spend.",
    caps: [
      {
        category: "Actions / round",
        cap: "Extra Attack + 1 Smite or 1 leveled spell",
        note: "L7 reactive trigger counts as that rider",
      },
      { category: "Aura stacking", cap: "One aura radius; 1 reactive aura trigger / round" },
      { category: "Lay on Hands", cap: "Pool 5 × level; max 50% pool spent / round" },
      { category: "Aura Surge", cap: "1 / rest (L17 draft)" },
      { category: "Oath revelation smite", cap: "1 / long rest rider without slot (L16 draft)" },
    ],
    playtestLedger: ["Smite uses", "LoH spent", "Aura triggers", "Oath spell riders"],
  },
  Warrior: {
    summary:
      "Mutation bruiser — slot count, one activation per round, Brutality Threshold gate, toxicity strain limits.",
    caps: [
      { category: "Mutation slots", cap: "3 prepared; 4 for Apex Form 1 / encounter (L20)" },
      { category: "Mutations / round", cap: "1 activation; Reflexive Mutation 1 / round (L17)" },
      { category: "Serum Overclock", cap: "2 serums at once = 1 activation (L9)" },
      { category: "Actions / round", cap: "Action Surge + 1 mutation activation max" },
      { category: "Brutality Threshold", cap: "100% max HP dealt → Transcendent 3 rounds; 1 / short rest" },
    ],
    playtestLedger: ["Active mutations", "Activations / round", "Strain applied", "Threshold triggers"],
  },
  Dragoon: {
    summary:
      "Mobile reach striker — Momentum cap/overflow, leap action economy, refund and overflow damage ceilings.",
    caps: [
      { category: "Momentum cap", cap: "5 (L1–12); 6 (L13+)" },
      {
        category: "Overflow",
        cap: "Temp HP = tier floor × overflow stacks (L17)",
        note: "Overflow does not raise cap",
      },
      { category: "Overflow damage", cap: "+1d6 / stack above cap, max +2d6 / turn (L12+)" },
      { category: "Actions / round", cap: "Extra Attack + 1 Wyvern's Flow or Apex Assault" },
      { category: "Momentum refund", cap: "1 / turn from Wyvern's Flow on hit (L13+)" },
      { category: "Sky Sovereign", cap: "1 / day (L20); no extra attacks from OAs immunity" },
    ],
    playtestLedger: ["Momentum start/end", "Overflow stacks", "Leaps / round", "Refund sources"],
  },
  Tinker: {
    summary:
      "Deployable control — concurrent gadget count, HP/damage/duration ceilings, shared deploy action economy.",
    caps: [
      { category: "Deployables", cap: "3 concurrent gadgets; only 2 autonomous actors may take independent turns; 2 drones share HP pool (L11+)" },
      { category: "Flask / bomb", cap: "4 concurrent; remote detonation 60 ft (L13+)" },
      { category: "Deployable HP", cap: "Draft +2 milestones; max 2 × level HP per device" },
      { category: "Damage", cap: "Overcharge double 1 / short rest; +5 ft first remote detonation / encounter" },
      { category: "Duration", cap: "Encounter; Mech Overdrive 1 permanent / battle (L20)" },
      { category: "Actions / round", cap: "1 deploy + 1 detonation; 2 deployables = 1 bonus action (L16)" },
    ],
    playtestLedger: ["Deployable count", "HP remaining", "Detonations / round", "Overcharge uses"],
  },
};

/** Classes flagged for ceiling-cap callouts in UI. */
export const CEILING_CAP_CLASS_NAMES = Object.freeze(Object.keys(CLASS_CEILING_CAPS));

/**
 * @param {string | null | undefined} className
 * @returns {ClassCeilingProfile | null}
 */
export function getClassCeilingCaps(className) {
  if (!className || typeof className !== "string") return null;
  return CLASS_CEILING_CAPS[className] ?? null;
}

/**
 * @param {string | null | undefined} className
 */
export function hasClassCeilingCaps(className) {
  return Boolean(getClassCeilingCaps(className));
}

/**
 * Compact one-line summary for tooltips.
 * @param {string | null | undefined} className
 */
export function ceilingCapSummaryLine(className) {
  const profile = getClassCeilingCaps(className);
  if (!profile) return null;
  return profile.caps.map((c) => `${c.category}: ${c.cap}`).join(" · ");
}
