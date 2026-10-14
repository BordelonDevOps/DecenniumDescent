# Monster Manual — public vs Director build filters

**Authority:** Canon Rewrite Source Pack (`README.md` in this folder)  
**Machine manifest:** [`build-filters.json`](./build-filters.json)  
**Owner lock:** 2026-08-05 §7 priority #5  

---

## Purpose

Publication builds must not ship Director-only creatures (or sealed endgame truths) into player-facing books, companion public libraries, or web docs.

This filter is the simple gate between:

1. **Known Descent** (player / licensed table)  
2. **Sealed Bestiary** (Director-only)

---

## Buckets

| Bucket | Source | Count (2026-08-05) | Include in player builds? |
|--------|--------|-------------------:|---------------------------|
| **public** | Known Descent · `Publication classification: Public` (and plain Public variants) | 26 | Yes |
| **restricted** | Known Descent · Licensed / deep-license / Restricted (incl. dual public+restricted annex) | 39 | Licensed / Director field kits only — still **not** Sealed |
| **director-only** | Sealed Bestiary entries (all currently Director sealed) | 5 | **Never** |

Totals: **70** authored Source Pack dossiers (65 Known Descent + 5 Sealed).

### Mapping from entry header → bucket

```
Director sealed                          → director-only
Licensed / Deep-license / Restricted*    → restricted
Public                                   → public
```

\*Including strings such as “Public history with restricted tactical annex” → **restricted** (safer default: withhold the restricted annex from pure public builds).

### Sealed volume (always director-only)

- `eirfax-the-dusk-crowned`
- `lumen-of-the-shattered-thread`
- `the-marquis-of-silence`
- `threxus-the-iron-spiral`
- `xarog-the-pactbound-furnace`

---

## Build recipes (conceptual)

| Build | Include buckets | Exclude |
|-------|-----------------|---------|
| **Player Known Descent DOCX / web** | `public` | `restricted`, `director-only` |
| **Licensed expedition kit** | `public` + `restricted` | `director-only` |
| **Full Director kit** | all three | — |
| **Companion public monster browser** | `public` (optionally `restricted` behind GM flag) | `director-only` |

Canon boundary still applies inside every bucket: no Floor 97/100 crystal path, no claimant system, no Tiers VII–X in Known Descent prose (`CANON_BOUNDARY.md`).

---

## Maintaining the manifest

When you add, remove, or reclassify an entry:

1. Edit the entry’s **Publication classification** header.  
2. Regenerate `build-filters.json` (re-run the inventory script or update lists by hand).  
3. Confirm Sealed volume entries remain `director-only`.  
4. Do **not** copy Sealed entries into `docs/bestiary/monster-manual/` public mirrors.

Optional PowerShell sketch (repo-local):

```powershell
# Scan Source Pack entries → refresh build-filters.json buckets by Publication classification
```

---

## Quarantine interaction

Entries under classic-label quarantine (`../CLASSIC_LABEL_SCRUB_POLICY.md`) are withheld from **commercial** builds even if their bucket would otherwise include them, until renamed or cleared.

*Filter stamp: 2026-08-05.*
