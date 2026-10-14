# Deep-tier crafting — Director guidance (218 `needsReview`)

**Date:** 2026-07-31  
**Workspace:** `DecenniumDescent-main`  
**Scope:** Tiers 6–10 / skill 11+ / Legendary–Mythic recipes only  
**Rule:** **Do not empty `components[]`.** Costs stay real; the flag means **balance is provisional**, not free craft.  
**No commit.**

---

## Counts (post-enrichment)

| Metric | Count |
|--------|------:|
| Total recipes | **623** |
| T1–5 `ready` (no review) | **405** |
| `needsReview: true` | **218** |
| — `skill_11_plus_deep_tier_provisional` | **159** |
| — `legendary_or_mythic_provisional` | **59** |
| Empty `components[]` | **0** |
| Recipes with `directorGuidance` | **218** |

| Result tier | skill_11+ | Legendary/Mythic | Total |
|------------:|----------:|-----------------:|------:|
| 6 | 39 | 0 | 39 |
| 7 | 34 | 0 | 34 |
| 8 | 50 | 0 | 50 |
| 9 | 36 | 13 | 49 |
| 10 | 0 | 46 | 46 |

---

## How to run these at the table

### Always

1. Charge **listed components** (or a 1:1 Instruments salvage swap of equal/higher tier).  
2. Log deductions on a salvage ledger — engine still does **not** auto-deduct.  
3. Keep **Heartcell / Silent Ones** names out of the public craft ledger.  
4. Treat Session “craft” as fiat until inventory wiring lands.

### Skill 11+ (deep-tier provisional)

- Gate availability behind **Floor/tier access** or a named haven workshop in T6–10 zones.  
- If the result feels too strong for the party’s current floor: add downtime (**skillLevel × 2 hours** suggested) or a rare catalyst from the current Gate zone.  
- Prefer Instruments Part III tier salvage tables over inventing new reagents.

### Legendary / Mythic (quality provisional)

- Campaign-defining only: **Gate seal**, research breakthrough, or named NPC commission.  
- Optional Resonance ritual: **1 long rest + Weave check DC 15 + skillLevel** before completion.  
- Do not mass-produce; one Legendary/Mythic per Expedition arc is a safe default.

### Companion UI

JSON field `directorGuidance` (string) is present on all 218 flagged recipes for future CraftingBuilder surfacing. Until UI reads it, Directors use this stamp + Instruments Part III.

---

## Continuity

- Opening clocks / guardians / expedition size / player spoilers: **unchanged** by this pass.  
- Does **not** amend Player Rulebook (crafting chapter remains thin).  
- Regenerating via `node scripts/fill-crafting-components.mjs` may overwrite `directorGuidance` until the fill script is taught to re-apply it — prefer re-running the enrichment block in this stamp’s companion script notes, or re-apply from this doc’s Always / Skill / Legendary rules.

### Re-apply guidance (idempotent)

```bash
# From DecenniumDescent-main — sets directorGuidance on needsReview rows only
node -e "/* or use docs/mechanics/_enrich_deep_tier_crafting_guidance.py if present */"
```

Python helper shipped: `docs/mechanics/_enrich_deep_tier_crafting_guidance.py`.

---

## Residual

- Author balance pass on the 59 Legendary/Mythic rows when T6–10 content freezes.  
- Wire CraftingBuilder badge for `needsReview` + tooltip from `directorGuidance`.  
- Optional inventory auto-deduct (Later).

*Stamp 2026-07-31 — integration spine.*
