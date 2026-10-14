# Incoming packs (unapproved / staged)

**Role:** Staging for newly delivered bible / data packs before they become ReviewBible or main canon.

**Do not** treat files here as approved **main** release. Register them in [`docs/canon/CANON_MANIFEST.json`](../../docs/canon/CANON_MANIFEST.json).

## Workflow

See [`docs/canon/REPOSITORY_PROMOTION.md`](../../docs/canon/REPOSITORY_PROMOTION.md) § Promotion path.

1. Drop pack under `incoming/<pack-slug>/`.
2. Update `CANON_MANIFEST.json`.
3. Diff vs current authoritative paths.
4. Validate visibility (public | director | internal) and schemas.
5. Promote → ReviewBible after review; → main only with explicit owner approval.

## Currently staged

| Slug | Contents | Manifest domains | Status |
|------|----------|------------------|--------|
| `DecenniumDescentv7/` | Gameplay Loop Bible v1 + Cursor playtest packs 01–04 (+ Master Instructions). See `PENDING_REVIEW.md` | combat / expedition / Haven economy / seasonal (pending) | **`pending-review`** (2026-08-05) — do not promote |
| `DecenniumDescentv6/` | Full V6 Consolidated RC (companion + books + data + MM pack). See `PENDING_REVIEW.md` | multi-domain | **`cut-over-to-main`** (2026-08-05); folder retained as historical stage |
| `core-systems-bible-v1/` | Core Systems Bible v1 `.docx` + Data v1 `.json` (SHA-identical to v6 Director Full) | spellcasting, combat, gate-tier-scaling, economy | Main/RB winners = public **v2** + Director **v1**; incoming retained as pre-cutover stage |
| `crafting-bible/` | Crafting Bible v4 Standalone `.docx` + v4 `.json` | crafting | **`cut-over-to-main`** with V6 (live public runtime 433) |

## Not yet located (do not invent)

- `Feats and Skills Overview.txt` — place here or under a `feats/` slug when available.
- V7 pack **`05-readability-speed-onboarding`** — listed in Master Instructions; zip not in 2026-08-05 drop.

## Owner note (2026-08-05)

`DecenniumDescentv6/` promoted into ReviewBible then cut over to main. See `docs/canon/MAIN_CUTOVER_V6_2026-08-05.md`. `DecenniumDescentv7/` staged pending-review only.
