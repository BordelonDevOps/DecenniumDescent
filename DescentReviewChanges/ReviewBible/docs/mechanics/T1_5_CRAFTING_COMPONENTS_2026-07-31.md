# T1–5 crafting components fill

**Date:** 2026-07-31  
**Workspace:** `DecenniumDescent-main`  
**Status:** Companion data filled — not a Player Rulebook amend  
**No commit** (worker stamp only)

---

## Problem

`src/data/crafting-recipes.json` held **623** recipes with empty `components[]`. Companion + Instruments treated that as infinite-free craft unless the Director fiat-assigned parts. Gap inventory flagged this as a **Must-have** for items/crafting completeness ([`TTRPG_COMPLETION_GAP_2026-07-31.md`](../CURRENT_SYSTEM_STATUS.md) §3.2).

Validated workbook `decennium_descent_crafting_recipes_validated.xlsx` already had **Base Ingredients** + **Monster Parts** for every row; the live JSON ingest had never carried them through (and workbook monster labels were heavy SRD/IP).

---

## What changed

| Path | Role |
|------|------|
| `src/data/crafting-recipes.json` | Filled `components[]` for all 623 recipes; restored workbook fields (`skillLevel`, `tags`, `effects`, `quantity`); set `resultItem.tier` from skill band |
| `src/data/backups/crafting-recipes.json.bak-2026-07-31` | Pre-edit backup |
| `scripts/fill-crafting-components.mjs` | Authoritative ingest + Aethel remaps + `needsReview` |
| `scripts/reparse-crafting.mjs` | Thin wrapper → fill script |
| `docs/manuals/Instruments_of_the_Weave.md` | Corpus gap language updated |

**Not touched:** bestiary xlsx, SessionTracker XP, Player Rulebook `.docx` / `rulebook_output.txt`.

---

## Counts

| Metric | Count |
|--------|------:|
| Total recipes | **623** |
| `components[]` filled | **623** |
| Still empty | **0** |
| `status: "ready"` | **405** |
| `needsReview: true` | **218** |
| `status: "stub"` | **0** |
| **T1–5** (`resultItem.tier` ≤ 5) | **405** |
| T1–5 filled | **405** |
| T1–5 ready (no review flag) | **405** |
| Unique component names after remap | **186** |
| IP-label hits after remap (scrub regex) | **0** |

`needsReview` reasons (non-empty recipes):

- `legendary_or_mythic_provisional` — Quality Tier Legendary/Mythic  
- `skill_11_plus_deep_tier_provisional` — Required Skill Level ≥ 11 (maps to dungeon tier ≥ 6)

These still have real component costs; the flag means deep-tier balance is provisional for author review, not “free craft.”

---

## Schema (ingest-compatible)

Existing UI (`CraftingBuilder`, `ItemsLibrary`) reads:

```ts
components: {
  id: string;
  name: string;
  tier: number;
  rarity: string;
  category: string;      // "base" | "monster_part"
  value: number;
  weight: number;
  quantity: number;      // parsed from workbook "(N)"
  properties: string[];
}[]
```

**Restored / added recipe fields** (ignored by UI if unused; safe for JSON ingest):

| Field | Source |
|-------|--------|
| `skillLevel` | Required Skill Level |
| `quantity` | Output Quantity |
| `tags` | Crafting Tags |
| `effects` | Effects/Properties |
| `needsReview` | boolean |
| `needsReviewReason` | string when flagged |
| `status` | `"ready"` \| `"needsReview"` \| `"stub"` |
| `resultItem.tier` | `ceil(skillLevel / 2)` capped 1–10 (Opening T1–5 = skill 1–10 → tiers 1–5) |
| `resultItem.rarity` | Quality Tier |
| `rarity` | Quality Tier |

Quantity parse: `Crystal vial (5)` → name + `quantity: 5`.  
Part tier parse: `… (Tier 1)` → component `tier: 1`, quantity 1.

Engine still does **not** auto-deduct inventory.

---

## Lore / IP remaps (workbook → product)

Monster-part labels from the xlsx were remapped to Decennium / Aethel / Instruments salvage vocabulary (examples):

| Workbook (do not ship) | Product name |
|------------------------|--------------|
| Storm Giant Heart | Thunder-vein Core |
| Kraken Ink | Abyssal Ink |
| Mind Flayer Brain | Echo-thought Mass |
| Aboleth Slime | Deep-memory Slime |
| Displacer Beast Hide | Phasehide Scrap |
| Phoenix Feather / Heart | Dawnflare Plume / Heart |
| Unicorn Horn | Spiralhorn Shard |
| Red Dragon Scale | Emberplate Scale |
| Blue Dragon Gland | Stormscale Gland |
| Golem Core / Arcane Core | Animated Core / Resonance Core |
| Living Vine | Root-grasper Tendon |
| Poison Sac | Spore Sac |
| Mithral / Adamantine ingot | Brightsteel / Heartsteel Ingot |
| Planar energy / Ethereal thread | Resonance Charge / Veilthread |
| Arcane dust / Magical essence | Resonance Dust / Weave Essence |

Full tables live in `scripts/fill-crafting-components.mjs` (`MONSTER_REMAP`, `BASE_REMAP`).

Heartcell / Silent Ones stay **out** of component names (public / salvage layer only).

---

## Sources

1. **Workbook:** `decennium_descent_crafting_recipes_validated.xlsx` (623 rows, all sheets with Base + Monster columns populated)  
2. **Director Instruments:** `docs/manuals/Instruments_of_the_Weave.md` Part III (tier salvage tables — Director may substitute)  
3. **Player Rulebook:** crafting chapter thin (inventory/poison-kit mentions only); no component list to overwrite — companion mirrors workbook + Instruments naming  
4. **Playtest:** Sim #2 used table-assigned salvage while JSON was empty; workbook defaults now differ from that one-shot fiat (e.g. Standard Oil → vial + base + Abyssal Ink). Directors may still substitute Yieldheart salvage per Instruments.

---

## How to regenerate

```bash
node scripts/fill-crafting-components.mjs
# or
node scripts/reparse-crafting.mjs
```

Backup is written once per day under `src/data/backups/crafting-recipes.json.bak-YYYY-MM-DD`.

---

## Residual / follow-ups

- **218** `needsReview` deep-tier recipes: Director guidance stamped 2026-07-31 — [`DEEP_TIER_CRAFTING_DIRECTOR_GUIDANCE_2026-07-31.md`](./DEEP_TIER_CRAFTING_DIRECTOR_GUIDANCE_2026-07-31.md) + `directorGuidance` on each JSON row (components still filled). Author balance pass still open when T6–10 freezes.  
- Optional: wire CraftingBuilder badge/tooltip from `directorGuidance`; Session / inventory auto-deduct.  
- Optional: align Sim #2 salvage ledger examples to workbook defaults or document “Director substitute” explicitly in playtest reports.  
- Player Rulebook still lacks a published component chapter — Instruments provisional salvage remains Director SoT for substitution.

*Stamp only — 2026-07-31. No commit.*
