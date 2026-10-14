# Core Systems Bible — authority registration

**Status:** Owner lock **2026-08-05** (§5 / priorities #4, #6, #7)  
**Version registered:** Core Systems Bible **v1.0** (meta date 2026-08-05)

---

## Registered artifacts

| Artifact | Path |
|----------|------|
| **Bible (Word)** | `Decennium_Descent_Core_Systems_Bible_v1.docx` (repo root) |
| **Machine data (JSON)** | `Decennium_Descent_Core_Systems_Data_v1.json` (repo root) |
| **Incoming stage pack** | `DescentReviewChanges/incoming/core-systems-bible-v1/` (docx + JSON copy) |
| **Domain registry** | `docs/canon/CANON_MANIFEST.json` → domains `spellcasting`, `combat`, `gate-tier-scaling`, `economy` |

JSON top-level domains in v1 data: `gate_tiers`, `resonance_costs`, `caster_pools`, `spells`, `conditions`, `combat_maneuvers`, `magical_substances`, `brews`, `tier_value_multipliers`.

---

## Authority — domains that **supersede** overlapping earlier sources

On these domains **only**, Core Systems Bible v1 (+ JSON) **wins** over overlapping text in the Player Rulebook, Instruments of the Weave, and earlier craft / economy working docs:

| Domain | Scope (what Core Systems owns) |
|--------|--------------------------------|
| **Spellcasting** | Resonance costs, caster pools, spell mechanical packaging aligned to Core Systems tables (not class fantasy / list identity) |
| **Combat** | Conditions, combat maneuvers, and combat resolution packaging defined in Core Systems |
| **Gate-tier scaling** | Tier ↔ floor / level / spell rank / craft band / item rarity / DC / threat / cargo / guardian / market table |
| **Economy** | Tier value multipliers, magical substances, brews, and related market/cargo scaling in Core Systems |

When companion code or older manuals disagree with Core Systems on these four domains: **prefer Core Systems**, then update mirrors — do **not** silently rewrite locked Player Rulebook prose without the §4 STOP-and-ask gate in `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`.

---

## Explicit **non**-supersession (still owned elsewhere)

Core Systems does **not** claim authority over:

- Class identity, fantasy, or progression identity
- Arch / hero / path structures
- Feats (see `docs/feats/`)
- Racial traits
- Crafting **recipes** (recipe corpus stays crafting bible / `crafting-recipes.json`)
- Creature lore / bestiary authorship
- Setting history
- Director cosmology (Matrix, Cosmology, DM-01 secret stratum)

Those remain under Player Rulebook, Director books, feat registry, racial data, crafting pack, and lore volumes as already locked.

---

## Relationship to ReviewBible drift policy

1. **2026-07-31:** “ReviewBible always wins” for continuity audits when main and ReviewBible diverge.
2. **2026-08-05 (§11):** One-way **main → ReviewBible baseline sync** so RB is not missing current companion baseline. After that sync, **future canon revisions land in ReviewBible / DescentReviewChanges**; do **not** auto-promote RB changes back to main.
3. Core Systems pack is staged under `DescentReviewChanges/incoming/` until owner promotes it into the ReviewBible book lineup.

See also: [`MAIN_TO_REVIEWBIBLE_SYNC_REPORT.md`](./MAIN_TO_REVIEWBIBLE_SYNC_REPORT.md).
