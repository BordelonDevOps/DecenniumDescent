# Monster Manual of the Decennium — LEGACY / REFERENCE-ONLY

> **⚠️ LEGACY — NOT AUTHORITATIVE (owner lock 2026-08-05 §6–7)**  
> The authoritative Monster Manual line is the **Canon Rewrite Source Pack**:  
> `docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/`  
> (**Monster Manual of the Known Descent** + **Director’s Sealed Bestiary**).  
> This MM-01 Markdown pack is **legacy / reference-only**. Useful material may be **migrated** into the Source Pack; do **not** expand this folder as a competing authored SoT.  
> `docs/bestiary/monster-manual/` on main is a **generated publication mirror** only.

**Book code (historical):** MM-01  
**Working title:** *Monster Manual of the Decennium*  
**Continuity bible:** `DescentReviewChanges/ReviewBible/` (owner lock — ReviewBible always wins)  
**Status:** Architecture / compilation scaffold — **superseded as authority** by Canon Rewrite Source Pack; retained for migration reference

---

## Purpose (historical — do not treat as live SoT)

This folder was the **publication-facing Monster Manual compilation path** scaffold. It is retained so editors can mine Tranche A/B entries when migrating into the Canon Rewrite Source Pack. **New authorship belongs in the Source Pack only.**

Historical compile steps (migrate into Source Pack instead of expanding here):

1. Author or upgrade creature entries to a consistent **full-entry** standard (`ENTRY_TEMPLATE.md`).
2. Compile toward a future commercial MM volume (or tier volumes) without overwriting ReviewBible’s living development bestiaries.
3. Cite Excel / JSON / sister volumes as sources while rewriting ecology and tactics in original prose.

---

## Ownership

| Role | Owns |
|------|------|
| **Continuity / ReviewBible** | Canon creature identity when ReviewBible books/data diverge from main |
| **BE-01 Bestiary of Aethel** | Searchable development encyclopedia (Excel → ingest → A–Z lexicon) |
| **BB-01 Codex of the Heartcell** | Ecology-first Director essays + Gate Seal set-pieces |
| **MM-01 (this pack)** | **Legacy** scaffold — migrate into Canon Rewrite Source Pack; not live SoT |
| **Companion JSON** | Executable `combat` payloads (`docs/mechanics/MONSTER_COMBAT_SCHEMA.md`) |
| **Instruments / Crafting Bible** | Harvest profiles, tradeskill parts, recipe linkage (cite; do not invent forbidden Matrical craft) |

**Do not** treat this pack as permission to overwrite:

- `Decennium_Descent_Bestiary_of_Aethel.docx` / `.md` (BE-01)
- `Codex_of_the_Heartcell.docx` / `.md` (BB-01)
- Player Rulebook or DM-01 combat/economy locks

If an MM entry would change locked rulebook or Director-book text, **STOP and ask** the owner (continuity protocol).

---

## How agents compile entries

1. **Pick source identity** from ReviewBible first: `src/bestiary_data_full.json` and/or BE-01 / BB-01. Prefer `combat.draft: false` for table-ready numbers.
2. **Check publication status** — `docs/development/BESTIARY_PUBLICATION_STATUS.md` (ReviewBible). Compatibility placeholders are coverage shells, not commercial copy.
3. **Copy `ENTRY_TEMPLATE.md`** into `entries/<slug>.md` (lowercase hyphenated name).
4. **Fill required fields**; mark optional fields `—` or omit only when the template marks them optional.
5. **Write original prose** — no stock OGL ecology paste; no foreign product jargon (use **Seal Pulse**, Weave, Opening, Expedition roles).
6. **Map mechanics** to DD: Armor / HP / Speed / defenses / attacks from JSON combat schema; floors/tiers from Chronicle / combat-trust docs when zone text disagrees with the sheet.
7. **Harvest / craft** — cite Excel loot tiers or Crafting Bible harvest profiles; label provisional drops.
8. **Provenance honesty** — always state `combat.source`, draft flag, and whether Type/Size/CR were corrected in fiction only.
9. **Dual-write** the markdown under `DescentReviewChanges/docs/bestiary/monster-manual/` (same relative path).
10. **Do not** regenerate or overwrite BE-01/BB-01 `.docx` from this pack unless the owner explicitly approves a publication pass.

### Entry readiness grades

| Grade | Meaning | Ship in MM? |
|-------|---------|-------------|
| **Publication** | Original ecology + trusted or companion-authored combat + floor placement + harvest note | Yes |
| **Expedition-ready** | Trusted combat + short ecology; harvest optional | Yes (Field Brief chapter or condensed block) |
| **Development cite** | Points at BE-01/JSON only; STUB metadata | No — appendix index only |

---

## Pack contents

| Path | Role |
|------|------|
| `README.md` | This file — purpose, ownership, compile rules |
| `MM_BOOK_PLAN.md` | Title, TOC, volume strategy, density goals, BE-01 relationship, STOP note |
| `ENTRY_TEMPLATE.md` | Full entry schema (required / optional) |
| `entries/` | Authored MM entries (markdown) |
| `entries/_EXAMPLE_ENTRY.md` | Worked example (Spiral Worm) |
| `REFERENCE_MM_BENCHMARK.md` | Optional — if present, use for density/structure norms only (never copy WotC text) |

---

## Related sources (read, do not overwrite)

- ReviewBible `BOOK_LINEUP.md` — BE-01, BB-01 status
- `docs/mechanics/T1_5_BESTIARY_COMBAT_2026-07-31.md` — trusted T1–5 set
- `docs/mechanics/MONSTER_COMBAT_SCHEMA.md` — combat payload shape
- `docs/manuals/GAP_FILL_FROM_REFERENCE_TOPICS.md` — topic checklist (MM-type gaps → historically BB-01; MM-01 now owns publication compilation)

---

*Scaffold stamp: 2026-08-04 — Agent 3 book architecture.*
