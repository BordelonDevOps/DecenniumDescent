# Official manuals (Director library)

**Continuity bible:** open current books under `DescentReviewChanges/ReviewBible/docs/manuals/` (owner lock 2026-07-31). See `BOOK_LINEUP.md` and `../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`.

| Book | Files | Role |
|------|-------|------|
| **DM-01 — Complete Director Edition** | ReviewBible `The_Directors_Crucible_Complete_Director_Edition.docx` | **Authoritative** Director book for table + simulation agents |
| **Sister volumes** | Codex / Instruments / Chronicle / Bestiary (in ReviewBible) | Active supplements; Bestiary & Codex still development / publication-pending |
| **Archive — generated Directors Manual** | `Decennium_Descent_Directors_Manual.docx` / `.md` (main working tree only) | Searchable mirror; **not** DM-01; may be absent from ReviewBible |

## Regeneration (archive generators only)

```bash
python scripts/generate_official_manuals.py
```

Does **not** replace DM-01 Complete Director Edition.

## Continuity

- Do not put Silent Ones / Heartcell into player-facing books.
- Opening 2400 h · Horn PoNR 1200 h.
- Expedition max 12 (Player Rulebook RAW).
- No foreign tabletop-brand references in generated prose.
- Before overwriting Player Rulebook / DM-01 text in ReviewBible, ask the owner (see `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`).
