# Opening clock purge — 2026-07-31

**Owner order:** 240/120 Opening clock issue must be **all gone** through product, runtime, and GM-facing docs.  
**Canon:** Opening **2400 hours / 100 days**; Horn PoNR **1200 hours / day 50**. Soft quit Floor 50 Canticle ≠ Horn.  
**No commit** (per brief).

Continuity typo stamp (single short record): [`DIRECTOR_BIBLE_CLOCK_TYPO_FIX_2026-07-31.md`](./DIRECTOR_BIBLE_CLOCK_TYPO_FIX_2026-07-31.md).  
Pre-purge inventory archive: [`OPENING_CLOCK_CONTINUITY_CHECK_2026-07-31.md`](./OPENING_CLOCK_CONTINUITY_CHECK_2026-07-31.md).

---

## Key constants (before → after)

| Location | Before | After |
|----------|--------|-------|
| `SessionTracker.tsx` `HORN_AT` | `120` | **`1200`** (+ UI labels: day 50 PoNR / Opening 2400h) |
| `dungeon-mechanics.json` `hornRule` | “At 120 hours underground…” | **1200 h / day 50** of **2400 h** Opening; soft quit ≠ Horn |
| `floor-encounters.json` `hornRule` (src + scripts) | “At 120 hours…” | same as above |
| `MonstersLibrary.tsx` banner / comment | “At 120 hours…” | **1200 hours (day 50)** |
| `scripts/ingest-data.mjs`, `parse-encounters.js`, `tools/ingest_lorebook.py` | embedded 120 h `hornRule` | **1200 / day 50** |

---

## Files changed (this purge)

### Runtime / data / ingest
- `src/components/SessionTracker.tsx`
- `src/components/MonstersLibrary.tsx`
- `src/data/dungeon-mechanics.json`
- `src/data/floor-encounters.json`
- `scripts/floor-encounters.json`
- `scripts/ingest-data.mjs`
- `scripts/parse-encounters.js`
- `tools/ingest_lorebook.py`

### Product / GM / Director synthesis (teach 2400/1200; retire code-debt framing)
- `README.md`
- `docs/MECHANICS_BIBLE_STUB.md`
- `docs/mechanics/DESCENT_WINDOW_CANON.md`
- `docs/mechanics/SESSION_LOOP.md`
- `docs/mechanics/WORLD_DUNGEON_LOOP.md`
- `docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md` (Q-OV-1 **closed**)
- `docs/mechanics/CONTINUITY_DETAILED_CHECK.md`
- `docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md`
- `docs/mechanics/BESTIARY_LORE_PASS_2026-07-30.md`
- `docs/mechanics/DIRECTOR_BIBLE_CLOCK_TYPO_FIX_2026-07-31.md`
- `docs/mechanics/OPENING_CLOCK_CONTINUITY_CHECK_2026-07-31.md` (superseded banner)
- `docs/playtest/HIDDEN_DUNGEON_EQUATION.md`
- `docs/playtest/A_TO_Z_MASTERY_DIGEST.md`
- `docs/playtest/NEWCOMER_GM_GUIDE.md`
- `docs/playtest/DUNGEON_CREATION_PURPOSE.md`
- `docs/playtest/READY_TO_CONTINUE.md`
- `docs/playtest/SIM_CAMPAIGN_PLAN.md`
- `docs/manuals/Decennium_Descent_Directors_Manual.md`
- `docs/manuals/DIRECTOR_EDITION_BIBLE_REVIEW.md`
- `docs/manuals/DIRECTOR_REBUILD_BRIEF.md`
- `docs/manuals/Instruments_of_the_Weave.md`
- `scripts/generate_official_manuals.py`
- `src/data/CONTINUITY_REPORT.md`
- `.cursor/rules/continuity-rulebooks.mdc`

### Backups
- `backups/opening_clock_purge_*` — JSON snapshots before rewrite

---

## Verification scan

**Tool:** `docs/mechanics/_purge_clock_verify.py` (masks `1200`/`2400` before matching `120`/`240`; skips `node_modules`, `.next`, `dist`, `out`, `backups`).

| Class | Count | Notes |
|-------|------:|-------|
| **LIVE-WRONG** | **0** | No live Opening=240 or Horn=120-as-PoNR in scanned product/source |
| **TYPO-CONTEXT** | few | Continuity stamps only |
| **ARCHIVE** | ~134 hits | Dated `SIM_*` / `T4_*` playtest logs + scan scratch JSON |

**Runtime checks:** `HORN_AT = 1200` and `hornRule` “1200 hours” present in SessionTracker, dungeon/floor JSON, MonstersLibrary, ingest scripts.

**Build artifact:** stale `out/` Next bundle may still embed old copy until next `next build` — not source of truth.

---

## Remaining FALSE-POSITIVES / non-issues (do not “fix”)

| Pattern | Why keep |
|---------|----------|
| Expedition max **12** | Roster RAW |
| CR / level **12**, chapter nums | Unrelated |
| **120 feet**, ranges | Distance |
| XP **120000** etc. | Economy |
| Historical sim lines `63/120 h`, `106/120 h` | Pre-purge Session UI archives |
| Typo stamps quoting **240/120** once | Continuity record only |
| Soft quit Floor **50** | Canticle ≠ Horn hour |

---

## Ambiguous leftovers

- **Historical sim reports** (`docs/playtest/SIM_*`, `T4_*`) still *record* the old 120 h UI clock — intentional archives, not teaching formulas.
- **Scan scratch** under `docs/mechanics/_opening_clock_scan_raw.json` and helper `_*.py` — disposable; supersede with this stamp + `_purge_clock_verify.py`.
- **Directors Manual `.docx`** Frame-table twin may still need a rebuild from `.md` if the binary was not re-exported this pass (`.md` is aligned).
- **`out/` production bundle** — rebuild to clear baked strings.

---

## Soft quit reminder

Floor 50 **Canticle** / Choralith = morale soft quit. **Horn hour 1200 / day 50** = calendar PoNR. Do not equate them.

*Stamp issued 2026-07-31 — no commit.*
