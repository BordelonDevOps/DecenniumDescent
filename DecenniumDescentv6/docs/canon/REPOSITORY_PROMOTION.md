# Repository promotion hierarchy

**Status:** Owner lock 2026-08-05 (§1, §12; priorities #1, #8)  
**Manifest:** [`CANON_MANIFEST.json`](./CANON_MANIFEST.json)

Do not treat every file dropped at the `-main` root as approved canon. Domain authority is whatever `CANON_MANIFEST.json` registers.

---

## Layers

| Layer | Path | Role |
|-------|------|------|
| **Approved release** | `DecenniumDescent-main` working tree (esp. published books + `src/` shipped with product) | **main** — approved release state |
| **Assembled review build** | `DescentReviewChanges/ReviewBible/` | Curated pack for continuity audits and review; main baseline + proposed/promoted changes |
| **Unapproved staging** | `DescentReviewChanges/` (outside ReviewBible) | Revisions, dual-write review copies, work-in-progress packs |
| **Incoming packs** | `DescentReviewChanges/incoming/` | Newly delivered bible/data packs awaiting review before ReviewBible or main promotion |

---

## Promotion path for new bible packs (§12)

1. Place the new pack under `DescentReviewChanges/incoming/<pack-slug>/`.
2. Record it in `CANON_MANIFEST.json` with `status: "pending-review"` (or `pending-locate` if files are missing).
3. Compare against current authoritative paths for that domain.
4. Identify superseded, conflicting, and newly added material.
5. Validate schemas, public vs Director visibility, and cross-book references.
6. Promote into **ReviewBible** only after review.
7. Promote into **main** only after **explicit owner approval**, with change manifest, validation report, and rollback snapshot.

Root drops may remain for inventory, but they are **not** auto-canonical. Prefer staging into `incoming/` immediately.

---

## Main ↔ ReviewBible sync (§11)

- **One-way baseline:** synchronize current main companion/data into ReviewBible so the pack is not a stale subset.
- Apply proposed revisions in ReviewBible or `DescentReviewChanges/`.
- Do **not** auto-sync ReviewBible → main.
- Main stays approved release until an explicit cutover.

---

## Manifest vs dual SoT files

- **One registry** (`CANON_MANIFEST.json`) points at domain owners.
- Main `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` = **agent ops protocol** + override tracker (not a second copy of domain rules).
- ReviewBible pack SoT = **book open order + sync pointer**; it must not independently own the same override/baseline facts — mirror or generate from domain sources / ops tracker via the manifest.
