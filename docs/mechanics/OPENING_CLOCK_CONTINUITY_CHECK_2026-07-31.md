# Opening / Horn clock continuity check — 2026-07-31

> **Superseded same day** by owner purge order: [`OPENING_CLOCK_PURGE_2026-07-31.md`](./OPENING_CLOCK_PURGE_2026-07-31.md). Runtime/`hornRule` debt listed below was cleared. Keep this file as the pre-purge inventory archive.

**Workspace:** `DecenniumDescent-main`  
**Owner lock (corrected 2026-07-31):** Opening = **2400 hours (100 days)**; Horn PoNR = **hour 1200 (day 50)**. Soft quit at Floor 50 Canticle ≠ Horn PoNR. **240/120 was a typo** and must not remain as live canon.  
**Method:** Ripgrep + Python scan of `.md` / `.txt` / `.json` / `.docx` (python-docx); classify PASS / FAIL / OK-CONTEXT / AMBIGUOUS / CODE-DEBT.  
**Scan artifacts (scratch):** `_scan_opening_clock.py`, `_analyze_opening_clock.py`, `_target_clock_verify.py`, `_final_clock_pass.py`, `_opening_clock_scan_raw.json` — disposable helpers under `docs/mechanics/`.

---

## Verdict: **mostly clean** (pre-purge snapshot)

Live Director literature (Complete Director Edition, Chronicle, Instruments, Codex soft-quit note, Matrix `.docx`, Matrix extract, Directors Manual front-matter clocks) teaches **2400 / 1200**. No live **Opening = 240 / ten-day** claims remain outside backups and explicit typo callouts.

Remaining friction in this snapshot was almost entirely **Session / JSON `hornRule` still asserting 120 h as PoNR** (cleared in purge) plus older playtest synthesis (updated in purge where GM-facing).

---

## Counts (live literature; `backups/` and player-rulebook `.pre-*` excluded)

| Class | Count (approx.) | Meaning |
|-------|----------------:|---------|
| **FAIL (Opening 240 as live canon)** | **0** after this pass | No remaining live “240 h / ten-day Opening” assertions |
| **FAIL (unmarked product-facing 120-as-PoNR)** | **was 3–5; auto-fixed** | README, MECHANICS_BIBLE_STUB, Frame-the-Cycle table rows |
| **OK-CONTEXT** | ~125+ | Typo callouts, superseded stamps, Q-OV-1, “code debt” annotations, historical sim logs |
| **AMBIGUOUS** | dozens (narrowed) | Playtest docs that treat wired **120 h** as “hard canon” while also citing owner lock 1200; mixed micro-budget caveat |
| **CODE-DEBT** | **7+ sites** | Runtime / product JSON / UI strings still on 120 |

Raw classifier dump before triage also flagged many false positives (expedition 12, XP 120000, hour 1200 matching `120`, continuity docs quoting the typo). Those are **not** counted as FAIL above.

---

## Canon reference (PASS patterns)

| Clock | Canon |
|-------|-------|
| Opening | **2400 hours / 100 days** |
| Horn PoNR | **1200 hours / day 50** |
| Soft quit | Floor 50 **Canticle** / Choralith seal — morale, **≠** Horn PoNR |
| Rejected typo | Opening **240** / Horn **120** / day **5** / “do not multiply by ten” defending 240 |

---

## Complete Director Edition — clock status: **fully PASS**

**Path:** `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx`

Strict scan (masking `1200`/`2400` so they cannot match `120`/`240`): **zero** live wrong-clock hits. Correct token counts ≈ **26× 2400**, **17× 1200**, plus 100-day / day-50 language. Explicit typo guardrail remains:

> Director canon … **2400-hour Opening (100 days)** with the Horn at **hour 1200 (day 50)**. Do not compress the Opening to **240/120** — that figure was a typo.

Pre-fix snapshot with 240/120 still lives only under `backups/The_Directors_Crucible_Complete_Director_Edition_20260731_070837.docx` and `backups/bible_clock_*.json` — **OK-CONTEXT / archive**, not live canon.

---

## Sister manuals / lore — PASS summary

| Source | Clock verdict |
|--------|----------------|
| `Chronicle_of_the_Decennial_Opening` (.md/.docx) | **PASS** — 100 days / 2,400 h; Horn day 50 / 1,200 h; Canticle soft-quit distinguished |
| `Instruments_of_the_Weave` (.md/.docx) | **PASS** — 2400/1200; legacy 120 labeled code debt |
| `Codex_of_the_Heartcell` | **PASS** on clocks (no wrong Opening); soft-quit ≠ Horn stated |
| `Decennium_Descent_Directors_Manual` front matter | **PASS** — 2400/1200; 120 flagged superseded |
| `The Decennium Descent and the Matrix of Oblivion.docx` | **PASS** — § “The 2400-Hour Descent (100 Days)” |
| `MATRIX_OF_OBLIVION_EXTRACT.md` | **PASS** — aligned 2400; horn 1200 noted in metadata |
| `AGENT_SIMULATION_REFERENCE.md` / `README_MANUALS.md` / rebuild briefs | **PASS** |
| Player Rulebook (`rulebook_output.txt` / `.docx`) | **N/A / PASS** — no Opening/Horn hour prose found (horn is companion/DM layer) |

---

## Top FAIL / debt paths (pre-fix → disposition)

### Auto-fixed this pass (literature only; no commit)

| Path | Was | Fix |
|------|-----|-----|
| `README.md` | “horn sounds at **120 hours**, marking the point of no return” | Replaced with **2400 / 1200** + soft-quit ≠ Horn + Session 120 = code debt |
| `docs/MECHANICS_BIBLE_STUB.md` | Horn Clock = 120 h as if canon | Split **canon 2400/1200** vs **Session code debt 120** |
| `docs/mechanics/WORLD_DUNGEON_LOOP.md` | Frame table: “120h horn” unmarked | Opening 2400 / Horn 1200 + legacy UI note |
| `docs/manuals/Decennium_Descent_Directors_Manual.md` | Same Frame table + stale “Matrix still 240” provenance | Aligned Frame table; Matrix provenance → verified 2400 |
| `docs/manuals/Decennium_Descent_Directors_Manual.docx` | Frame table “120h horn” | Same Frame-table wording fix |
| `docs/mechanics/DESCENT_WINDOW_CANON.md` | Claimed Matrix `.docx` still “240 hours” | Updated — Matrix **aligned** on disk (2026-07-31 verify) |
| `docs/playtest/DUNGEON_CREATION_PURPOSE.md` | “Matrix `.docx` still 240 h” | Updated to aligned 2400 |

### Left for owner (do not silently rewrite)

| Path | Severity | Notes |
|------|----------|-------|
| `src/components/SessionTracker.tsx` `HORN_AT = 120` | **CODE-DEBT** | Runtime constant; product decision (UI “hours underground” vs Opening hours) |
| `src/data/dungeon-mechanics.json` `hornRule` | **CODE-DEBT** | Player-visible via Dungeon Guide |
| `src/data/floor-encounters.json` `hornRule` | **CODE-DEBT** | Player-visible via Encounters |
| `scripts/floor-encounters.json` + ingest parsers | **CODE-DEBT** | Upstream copy of hornRule |
| `src/components/MonstersLibrary.tsx` | **CODE-DEBT** | Hardcoded “At 120 hours… point of no return” banner |
| Q-OV-1 in `CONTINUITY_SOURCE_OF_TRUTH.md` | **Open override** | Partial: bible typo fixed; Session/JSON still open |
| Historical `docs/playtest/SIM_*`, `T4_*` reports | **OK-CONTEXT** | Records of sessions run under 120 UI — leave as history |
| `docs/playtest/HIDDEN_DUNGEON_EQUATION.md`, `A_TO_Z_MASTERY_DIGEST.md` | **AMBIGUOUS** | Document owner lock 1200 but still teach wired 120 formulas as “hard canon” for sims — annotate further only if owner wants playtest docs rewritten |

### Archive only (not live FAIL)

- `backups/The_Directors_Crucible_Complete_Director_Edition_20260731_070837.docx`
- `backups/bible_clock_hits_20260731.json` / `bible_clock_replacements_20260731.json`

---

## Soft quit vs Horn

Confirmed correctly separated in Codex / Chronicle / AGENT refs: **Canticle Gate (Floor 50)** = soft quit / morale turn-back; **Horn hour 1200 / day 50** = calendar PoNR. No literature found equating Canticle with Horn PoNR as a single clock.

---

## Implementation debt bucket (code — report only)

| Location | Current | Canon target (when owner asks) |
|----------|---------|--------------------------------|
| `SessionTracker.tsx` | `HORN_AT = 120` | Likely `1200` **or** nested micro-budget semantics — owner must choose |
| `dungeon-mechanics.json` / `floor-encounters.json` | “At 120 hours…” | Rewrite to 1200 day-50 PoNR **or** dual-clock wording |
| `MonstersLibrary.tsx` | Hardcoded 120 PoNR warning | Same |
| Session UI label “hours underground” | May not mean “hours since Opening” | Product copy decision before number swap |

**Not changed** this pass (per brief).

---

## False positives consciously ignored

Expedition max **12**, CR/level **12**, **120 feet**, XP **120000**, “6–12 hour session”, chapter numbers, changelog/typo narratives, and substrings of **1200** / **2400**.

---

## Bottom line for parent agent

- **Verdict:** mostly clean  
- **Opening 240 live FAIL:** 0  
- **Complete Director Edition:** fully **PASS** on clock  
- **Auto-fixed:** README, MECHANICS_BIBLE_STUB, WORLD_DUNGEON_LOOP Frame row, Directors Manual md+docx Frame row, DESCENT_WINDOW_CANON + related Matrix-stale stamps  
- **Left for owner:** Session `HORN_AT` / `hornRule` / MonstersLibrary strings; optional playtest-synthesis rewrite; Q-OV-1 code option  
- **Report path:** `docs/mechanics/OPENING_CLOCK_CONTINUITY_CHECK_2026-07-31.md`  
- **No commit**
