# Monster Manual Canon Rewrite Source Pack

**Status:** **Authoritative Monster Manual line** (owner lock 2026-08-05 §6–7)  
**Path:** `docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/`

This pack is the **only** authored Source of Truth for the commercial / publication Monster Manual. Do not maintain a second independently authored manual under `docs/bestiary/monster-manual/`.

---

## Volumes

| Volume | Folder | Visibility | Role |
|--------|--------|------------|------|
| **Monster Manual of the Known Descent** | `Monster_Manual_of_the_Known_Descent_Source/` | Player-facing / ordinary table reference | What Aethel can know through Haven scholarship and recognized history. Stops at the **failed Sixth Gate**. |
| **Director’s Sealed Bestiary** | `Directors_Sealed_Bestiary_Source/` | Director-only | Full Sixth Gate, Tiers VII–X, Marquis origin / succession, and other sealed continuity. |

Each volume has:

- `entries/` — standardized markdown dossiers  
- `ENTRY_TEMPLATE.md` — required fields  
- `CANON_BOUNDARY.md` — public vs Director knowledge ceiling  
- `volume-metadata.json` — counts / gate disclosure notes  
- Generated `.docx` (publication artifact; regenerate from entries)

---

## Authority vs legacy

| Material | Status |
|----------|--------|
| **This Source Pack** | **Authoritative** — author and revise here |
| `docs/bestiary/monster-manual/` | **Generated publication target / mirror only** — not a competing authored line |
| `DescentReviewChanges/docs/bestiary/monster-manual/` (earlier MM-01) | **Legacy / reference-only** — migrate useful text into this pack; do not expand as SoT |
| First Monster Manual Volume I builds; conflicting ReviewBible bestiary volumes | Legacy / reference — useful material may be migrated |
| Any public file exposing Tiers VII–X, Marquis, or claimant system | Not authoritative; quarantine from public builds |

---

## Publication markers (required on every entry)

Use the entry header fields from `ENTRY_TEMPLATE.md`:

| Field | Purpose |
|-------|---------|
| **Publication classification** | `Public` · `Licensed` / deep-license · `Restricted` · `Director sealed` |
| **Knowledge status** | In-world reliability band |
| **Reliability / confirmed / rumored range** | What expeditions can trust |
| **Primary source** | In-world record provenance |

### Build buckets (see `BUILD_FILTERS.md` / `build-filters.json`)

| Bucket | Includes | Ships in |
|--------|----------|----------|
| **public** | Known Descent entries marked Public | Player / commercial Known Descent builds |
| **restricted** | Licensed / deep-license / restricted Known Descent entries | Licensed expedition / Director field kits — still **not** Sealed |
| **director-only** | Sealed Bestiary + Director sealed markers | Director-only builds only |

**Never** include `director-only` entries in player-facing books, companion public libraries, or web docs meant for players.

---

## Workflow

1. **Author / revise** standardized entries under the correct volume `entries/` folder.  
2. Set **publication classification** and knowledge/reliability fields.  
3. Respect `CANON_BOUNDARY.md` — public knowledge ends at failed Sixth Gate; no Floor 97/100 crystal path; no Marquis / Tiers VII–X in Known Descent.  
4. Refresh `build-filters.json` when adding/removing entries or changing classifications.  
5. **Generate** DOCX / web docs from this pack only.  
6. Optionally **mirror** generated output into `docs/bestiary/monster-manual/` — do not hand-author a parallel corpus there.  
7. Dual-write product docs to `DescentReviewChanges/` per activity-log rules when shipping game content.

---

## Classic labels

Commercial rename policy: [`../CLASSIC_LABEL_SCRUB_POLICY.md`](../CLASSIC_LABEL_SCRUB_POLICY.md).  
Unresolved distinctive labels → quarantine outside publication builds (`compatibilityAliases` internal only).

---

## Related continuity

- Floor 97 / Old God dual-layer: `docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md`  
- Continuity ops: `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`  
- Sim notes: `docs/manuals/AGENT_SIMULATION_REFERENCE.md`

*Authority stamp: 2026-08-05 — owner §6–7.*
