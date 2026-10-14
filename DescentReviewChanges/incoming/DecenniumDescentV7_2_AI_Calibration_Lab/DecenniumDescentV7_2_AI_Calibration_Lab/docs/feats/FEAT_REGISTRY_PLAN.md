# Feat registry — plan & ID scheme (§10)

**Status:** Started **2026-08-05**  
**Living status:** [`FEAT_REGISTRY_STATUS.md`](./FEAT_REGISTRY_STATUS.md)  
**Machine snapshot:** [`feat-registry-snapshot.json`](./feat-registry-snapshot.json)

---

## Located sources

| Source | Path | Role |
|--------|------|------|
| **Companion registry (main)** | `src/data/feats.js` | **Working registry** — 336 unique IDs (2026-08-05 audit) |
| **Companion registry (ReviewBible)** | `DescentReviewChanges/ReviewBible/src/data/feats.js` | Synced from main baseline this pass (§11) |
| **330 stub Word** | `Decennium_Descent_330_Feat_Compendium.docx` | **Stub output — not SoT**; do not force final count to 330/336 |
| **Compendium extract** | `feat_compendium_output.txt` | Large ingest dump (includes rulebook text); not the feat registry |
| **Category Word stubs** | `Decennium_Descent_{Combat,Magic,Skill,Feats}.docx`, racial abilities/feats docx | Legacy stubs; secondary to `feats.js` |
| **Extra JS** | `additional-feats.js`, `ENHANCED-FEATURES.JS` | Legacy / non-canonical overlays — do not merge blindly |
| **Feats and Skills Overview.txt** | **Not found** in workspace (2026-08-05 search) | Recorded missing; re-home if owner supplies path |

Final published count comes from **validation of complete entries**, not from stub filenames.

---

## Registry home

| Layer | Location |
|-------|----------|
| **Canonical companion array** | `src/data/feats.js` → `export const feats = [...]` |
| **Docs / status** | `docs/feats/` (this folder) |
| **Optional future split** | Prefer keeping one array until drafts stabilize; if split later, use `src/data/feats/*.json` imported by a thin `feats.js` barrel — **not required this pass** |

---

## Stable ID scheme

**Canonical form:** `snake_case` ASCII slug derived from the feat name.

| Rule | Example |
|------|---------|
| Lowercase words joined by `_` | `armor_crusher`, `battlefield_commander` |
| Keep legacy camelCase IDs already in saves | `abilityScoreImprovement`, `animalAffinity` — **do not rename** without a compatibility alias |
| Prestige / batch prefixes already present | `skill_feats1_*` — treat as **legacy**; prefer unprefixed snake_case for new work |
| Mutations | Keep type in `type` field (`Aberrant_mutation`, etc.); ID stays descriptive (`aberrant_mind`) |
| Deprecation | Keep ID; set `"deprecated": true` + `deprecatedReason` (see `skill_feats1_master_tracker`) |

**Uniqueness:** `id` must be unique across the array. Display `name` collisions require one canonical ID and deprecated aliases.

---

## Status labels (for `FEAT_REGISTRY_STATUS.md`)

| Label | Meaning |
|-------|---------|
| **complete** | No `draft: true`; description is full prose (not “Draft presentation…”); effect playable |
| **draft** | `draft: true` and/or “Draft presentation…” thin text |
| **duplicate** | Same display name or near-identical effect; keep one canonical, deprecate others |
| **placeholder** | Explicit TODO/TBD/stub effect or empty body (none counted in 2026-08-05 snapshot) |

---

## Dedupe plan

1. Prefer **unprefixed** snake_case ID when two drafts share a name (`master_tracker` over `skill_feats1_master_tracker`).
2. Mark losers `"deprecated": true` with reason; do not delete until save-migration audit.
3. Reconcile type mismatches (Skill vs General) toward the more specific type.
4. Do **not** pad the registry to 330/336 to match stub docx titles.

---

## Completion priority (checklist order)

1. Deprecate confirmed duplicates (Master Tracker — already flagged).
2. Combat drafts (`type: Combat`, thin) — high table impact.
3. Magic drafts — align effect language with Core Systems spellcasting packaging where relevant.
4. Skill drafts — all currently draft; promote in batches.
5. Remaining General drafts.
6. Leave mutation + Racial blocks alone unless audit finds errors (currently complete).

Full checklist IDs: `feat-registry-snapshot.json` → `priorityDraftChecklist`.
