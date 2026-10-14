# Continuity detailed check — Oversight Phase A

**Agent:** Oversight (1)  
**Date:** 2026-07-30  
**Workspace:** `DecenniumDescent-main`  
**Inputs read:** `CONTINUITY_REPORT.md`, `CONTINUITY_GLOSSARY.md`, `AUTHOR_REVIEW_QUEUE.md`, `BALANCE_REPORT.md`, `RESONANCE_CANON.md`, `UMBRIN_LORE.md`, `BESTIARY_INGEST.md`, `XP_ADVANCEMENT_CANON.md`  
**Companion spot-checks:** Umbrin, Hybrid-B, Shadow/Grief promotion, Master Tracker singleton, Bestiary.xlsx workflow, draft flags, XP wiring (partial worker land)

---

## Executive summary

Collaborator **continuity gates A–G remain broadly green** for terminology, 17-class roster, prestige↔feats, save shape, and T1–5 dungeon alignment. **Phase C (2026-07-30): clean pass** — see Phase C section below. Phase A/B notes below are the pre-cleanup audit trail.

---

## Gate status (A–G)

| Gate | Label | Status | Notes |
|------|-------|--------|-------|
| **A** | Terminology & cosmology | **Pass** | Glossary current on Umbrin, Resonance, Murk geography, Echo Court / Hush. No Hybrid-B in player UI (code comments only). Cosmology XIV superseded by Dungeon Guide. |
| **B** | Class roster (17) | **Pass** | `CANON_CLASSES.length === 17`; Paladin present; Fighter/Swashbuckler not selectable. |
| **C** | Oracle / Paladin / Druid | **Pass with drift** | 10 mysteries + 10 curses + 7 circles wired. **Promoted:** Ancestor, **Shadow** (`draft: false`), Spiral-Touched (no draft flag). **Promoted oath:** **Grief** (`draft: false`). **Drift:** Gate C checklist still says “Mercy canon; others draft” but **Mercy is `draft: true`** in data. 8 mysteries + 9 oaths + 9 curses remain draft. |
| **D** | Prestige ↔ feats | **Pass** | Bloodbound resolved. **Master Tracker:** canonical `master_tracker` (Skill); `skill_feats1_master_tracker` `deprecated: true`, filtered in Builder (`!feat.deprecated`). |
| **E** | Character save & UI | **Pass** | `normalizeCharacter()` fields stable; Umbrin migration on load. Builder Advancement uses **`CANON_XP_THRESHOLDS`** from `src/lib/xp-economy.js` (rulebook table). Oracle excluded from Weave RP paths. Resonance multiclass merge implemented (`mergeMulticlassMaxRp`). |
| **F** | Dungeon & encounters | **Pass (T1–5) / Draft (T6–10)** | 10 gate bosses aligned in glossary + `floor-encounters.json`. Tiers **6–10** have survivor-rumor stubs (`mapped: false`, `draft: true`) — not authored encounter content. |
| **G** | Build hygiene | **Conditional** | Wave 63 reported green build. `BALANCE_REPORT.md` notes pre-existing `MonstersLibrary.tsx` tag-type `tsc` errors — re-verify after bestiary worker pass. |

**Collaborator invite:** Gates A, B, D, E, F (T1–5) are acceptable for external writers **if** Gate C drift (Mercy vs promoted Shadow/Grief) is understood as documentation lag, not product ambiguity.

---

## P0 / P1 / P2 open items

Two queues coexist; do not conflate them.

### Continuity queue (`OVERNIGHT_VAGUE_QUEUE.md`)

| Priority | Count | State |
|----------|------:|-------|
| **P0** | 0 | VQ-01–05 resolved (cosmology, Oracle RC, Resonance naming, 17 classes, Bloodbound). |
| **P1** | 0 | VQ-06–14 resolved (Gravetouched, dungeon entryClasses, T6–10 stubs, Session HP/rest/RP, multiclass merge, Umbrin rename). |
| **P2** | 11 | VQ-15–25 author review, reputation→RP wiring, wild-shape tracker, overcast panel, horn penalty, L97 myth watch, etc. |

**P2 highlights needing doc refresh after owner promotions:**

- **VQ-15:** Now **8/10** draft mysteries (was “9 of 10”) — Ancestor + **Shadow** approved.
- **VQ-16:** Now **8/10** draft oaths (was “9 of 10”) — **Grief** approved; **Mercy still draft in code** despite glossary “Mercy canon” label.

### Balance / systems queue (`BALANCE_REPORT.md` §6)

| Priority | Open items (summarized) |
|----------|-------------------------|
| **P0** | (1) Rulebook provenance + `confirmed \| draft \| legacy-unverified` metadata; (2) Companion safety labels for unverified XP/CR/T6–10/combat; (3) Structured combat schemas — **708/708** have draft AC/HP/combat but **698 excel-sandbox**; (4) Class/spell effect schema for high-impact features (Mirrorsage, Oracle RC, Paladin, Warrior, Dragoon, Tinker, overcast); (5) Reproducible L1/L3/L5/L8/L10 test harness. |
| **P1** | Encounter worksheet, XP award ledger with write-back, authored floor encounter cards, bounded class playtests. |
| **P2** | Numerical tuning after evidence; comparison surfaces; expand authored bestiary/floors. |

### Oversight P0 synthesis (actionable now)

1. **Reconcile Mercy oath draft flag** vs glossary/Gate C “Mercy canon” — either promote in data or downgrade docs.
2. **Refresh Gate C checklist + VQ-15/16 counts** for Shadow/Grief promotions.
3. **Update stale CONTINUITY_REPORT wave-63 line** (“Resonance multiclass formula still draft”) — Hybrid-B merge is **approved canon** per `RESONANCE_CANON.md` §7 and `AUTHOR_REVIEW_QUEUE.md` §4.
4. **Label Bestiary sandbox combat** — 708 rows have stats; **not** source-backed balance (698 `excel-sandbox`).
5. **XP docs vs code** — `XP_ADVANCEMENT_CANON.md` and balance report still say Builder uses legacy thresholds; **Worker 1 wired canon** (`xp-economy.js` + Builder). Docs need reconciliation, not re-wiring.

---

## Contradictions found

| # | Topic | Evidence A | Evidence B | Severity |
|---|-------|------------|------------|----------|
| 1 | **Oath of Mercy canon status** | `CONTINUITY_GLOSSARY.md`, Gate C: “Mercy rulebook-complete” | `paladin-oaths.js` `mercy` → `draft: true`, `finalOathGiftDraft: true` | **P0 doc/data** |
| 2 | **Shadow promotion vs stamp timeline** | Owner stamp + `oracle-mysteries.js` Shadow `draft: false` | CONTINUITY stamp “Shadow + Time tone pass” (line ~2190) says Shadow retains `draft: true` via `draftMysteryRevelations` | **P1 stale stamp** — promotion superseded tone pass |
| 3 | **Resonance multiclass draft label** | CONTINUITY wave-63 status: “formula still draft” | `RESONANCE_CANON.md` §7, `AUTHOR_REVIEW_QUEUE.md` §4: approved canon, implemented | **P1 stale status** |
| 4 | **Builder XP thresholds** | `XP_ADVANCEMENT_CANON.md` § Companion conflict; `BALANCE_REPORT.md` P0 #1 | `CharacterBuilder.tsx` + `xp-economy.js` use confirmed `CANON_XP_THRESHOLDS`; CONTINUITY Worker 1 stamp documents wiring | **P1 doc lag** (code ahead of canon docs) |
| 5 | **Bestiary combat coverage narrative** | Older CONTINUITY stamps: “698 metadata-only, no AC/HP columns” | `BESTIARY_INGEST.md` + live JSON: **708/708** AC/HP/combat (698 sandbox + 10 authored) | **Resolved** — use Excel-first consolidation as truth |
| 6 | **Master Tracker presentation** | `AUTHOR_REVIEW_QUEUE.md` §3: resolved singleton | `master_tracker` still carries `draft: true` on presentation description (Skill record) | **P2 cosmetic** — selection works; draft badge may confuse |
| 7 | **Midnight author pack vs Grief** | Stamp: “all ten Sacred Oaths remain candidate-only draft” | `paladin-oaths.js` Grief `draft: false` | **P1 stale stamp** |
| 8 | **Shadow uses `draftMysteryRevelations()`** | Helper always sets `draft: true` internally | Shadow object overrides with `draft: false` after spread | **OK** — override intentional; document pattern for future promotions |

**No open ASK OWNER rows** (#1–#7 resolved/closed per `CONTINUITY_REPORT.md`).

---

## Spot-check results (companion)

### Umbrin

| Check | Result |
|-------|--------|
| Product name | **Umbrin** in `races.js`, `builder-races.js`, Builder pinned first, Sheet lore card, CosmologyViewer, ReputationPanel note |
| Legacy migration | `character-storage.js` maps Drow / Umbral Elf → Umbrin |
| Lore canon | `UMBRIN_LORE.md` locks Obsidian Burn → Murk → Blackglass Reach → Veyr-Obsid → Quiet Deep; transactional alliances |
| Draft boundary | Race/lore entries may retain `draft: true` in data where marked; **theology/geography decisions are canon** per owner 2026-07-30 |

### Hybrid-B (Resonance multiclass)

| Check | Result |
|-------|--------|
| Player UI | **No “Hybrid-B”** in components (grep clean) |
| Code | `resonance-economy.js` — `mergeMulticlassMaxRp`, reputation modifiers, draft flag when either class uses draft pool table |
| Canon | Formula approved; rulebook sync stamp present |
| Builder | Secondary class + level dropdowns; Draft badge when contributing pool is draft |

### Shadow / Grief promotion

| Entity | `draft` in data | `source` string |
|--------|-----------------|-----------------|
| Mystery of Shadow | `false` | Canon — Director-approved (2026-07-30) |
| Oath of Grief | `false` | Canon — Director-approved (2026-07-30) |
| `ORACLE_RULEBOOK_STATUS.fullTierTree` | includes `"Shadow"` | Matches code |

### Master Tracker singleton

| Record | Selectable | Notes |
|--------|------------|-------|
| `master_tracker` (Skill) | Yes | Builder filters `!deprecated` |
| `skill_feats1_master_tracker` (General) | No | `deprecated: true`, historical saves only |

### Bestiary.xlsx workflow

| Check | Result |
|-------|--------|
| Canonical workbook | `Bestiary.xlsx` (708 rows, combat columns merged from retired sandbox) |
| Ingest | `npm run ingest:bestiary` → `scripts/ingest_bestiary_from_excel.py` |
| Live JSON | **708** entries; **708** AC/HP; **708** structured attacks; **698** `excel-sandbox`; **10** `companion-authored draft` gate guardians |
| IP scrub | `rename_value()` on ingest; Excel names pre-scrub |

### Draft flags (summary counts)

| Domain | Approved / rulebook-complete | Draft |
|--------|------------------------------|-------|
| Oracle mysteries | Ancestor, **Shadow** (2) | 8 |
| Oracle curses | Spiral-Touched (1, no draft flag) | 9 |
| Paladin oaths | **Grief** (1 promoted) — **Mercy claimed canon in glossary but `draft: true` in code** | 9–10 depending on Mercy resolution |
| Bestiary combat | 10 authored gate guardians | 698 sandbox + authored payloads all `draft: true` |
| Floor tiers | T1–5 mapped | T6–10 `mapped: false`, survivor-rumor drafts |

### XP wiring (Worker 1 partial land — verify in Phase B)

| Layer | Status |
|-------|--------|
| Confirmed thresholds | `xp-economy.js` + Builder Advancement |
| Draft awards | Session **Award draft XP** → scene notes + `draftXpSession` tally; **no character save write-back** |
| Not wired | Encounters calculator, auto level-up, Bestiary XP canon promotion |

---

## Worker-gap watchlist (re-verify when workers finish)

| Worker lane | Re-check when landed |
|-------------|----------------------|
| **XP wire** | Builder threshold display matches save `currentXP`; Session draft award does not mutate saves unless explicitly scoped; update `XP_ADVANCEMENT_CANON.md` / `BALANCE_REPORT.md` conflict paragraphs; gate P0 #2 safety labels on draft XP UI |
| **Bestiary polish** | Re-ingest after Excel edits; confirm 708 count stable; gate guardian merge rules (Excel wins when populated); `MonstersLibrary.tsx` tsc clean; sandbox combat stays labeled draft in UI |
| **Class caps** | Mirrorsage/Oracle/Paladin/Warrior/Dragoon/Tinker — per-turn/encounter caps documented in effect schema; `class-draft-levels.js` L11–20 milestones still draft; no accidental promotion |
| **Combat recharges** | Gate guardian `combat.attacks` recharge fields; sim uses authored at-will only; Bloom/Vaskor band stays 40–70% / survivable under draft proxy |
| **T6–T10 drafts** | `floor-encounters.json` tiers 6–10 remain `mapped: false` until authored; no fabricated rosters; Quiet Deep / Murk lore consistent with Umbrin canon |

---

## Phase B — Oversight re-check list (for parent resume)

After parallel workers land, Oversight (1) must:

1. **Diff worker branches** against this baseline for unintended draft promotions or Hybrid-B UI leaks.
2. **Re-run gate C** with updated mystery/oath counts; **resolve Mercy** draft flag vs glossary.
3. **Reconcile XP canon docs** with `xp-economy.js` + Session award behavior; confirm no silent save write-back.
4. **Re-count bestiary JSON** post-ingest; spot-check 3 gate guardians + 3 sandbox rows for provenance labels.
5. **Re-run** `npx tsc --noEmit` and combat sim smoke (Bloom L3, Vaskor L8).
6. **Scan BALANCE P0** — structured combat schema progress and class-cap/recharge wiring for high-ceiling classes.
7. **T6–T10** — confirm still draft/unmapped unless worker explicitly scoped mapped content.
8. **Stamp** `CONTINUITY_REPORT.md` with Oversight Phase B outcome.

---

## References

- Gates definition: `src/data/CONTINUITY_REPORT.md` § Collaborator-ready continuity gates
- Author decisions: `docs/mechanics/AUTHOR_REVIEW_QUEUE.md`
- Balance backlog: `docs/mechanics/BALANCE_REPORT.md`
- Bestiary pipeline: `docs/mechanics/BESTIARY_INGEST.md`
- XP provenance: `docs/mechanics/XP_ADVANCEMENT_CANON.md`

*Oversight Phase A complete — 2026-07-30.*

---

## Oversight Phase B — worker re-check (2026-07-30)

**Agent:** Oversight (1)  
**Verdict:** **Pass with drift** — all five workers verified; Gate C Mercy drift **corrected in docs**; Bloom recharge sim above draft target band.

### Worker verification

| Worker | Claim | Verified |
|--------|-------|----------|
| **W1 XP** | `xp-economy.js`, Builder canon thresholds, Session draft award | **Pass** — `CANON_XP_THRESHOLDS` in Builder; Session **Award draft XP** → scene notes + `draftXpSession`; **no save write-back**. `XP_ADVANCEMENT_CANON.md` reconciled. |
| **W2 Bestiary** | 430 rows polished, NeedsReview, low-CR HP bumps, re-ingest | **Pass** — `BESTIARY_INGEST.md`: **430** rows touched, **320** size snaps, **233** HP floor bumps (CR ≤ 3); `NeedsReview` Excel column (not in JSON). Live JSON **708** entries unchanged count. Gate guardians skipped per worker boundary. |
| **W3 Caps** | `CLASS_CEILING_CAPS.md` + `class-ceiling-caps.js` + UI | **Pass** — draft guardrails for Mirrorsage, Oracle, Paladin, Warrior, Dragoon, Tinker; `ClassCeilingCapsCallout` in Builder + Sheet. |
| **W4 Combat** | 26 recharge enrichments; Bloom 93.2%; Vaskor 58.2% | **Pass** — JSON **26** attacks with `usage: recharge`; sim rerun matches (**Bloom 93.2%**, **Vaskor 58.2%**). Bloom/Vaskor spot-check: Vine Maw + Spore Burst / Stone Maw + Seismic Roar. |
| **W5 Dungeon** | T6–T10 draft seeds, still unmapped | **Pass** — tiers 6–10 have `regionNames`, `hazards`, `gateBossSeed`, `encounterVibe`; all **`mapped: false`**, **`draft: true`**. Umbrin geography touches selective (Quiet Deep, Blackglass Reach, Veyr-Obsid). |

### Phase B checklist results

| # | Item | Result |
|---|------|--------|
| 1 | Unintended promotions / Hybrid-B UI | **Clean** — only Shadow + Grief `draft: false`; no Hybrid-B in components |
| 2 | Gate C + Mercy | **Fixed** — glossary, Gate C checklist, VQ-16: Mercy **`draft: true`**; Grief promoted |
| 3 | XP docs ↔ code ↔ Session | **Reconciled** — canon thresholds wired; draft awards session-local only |
| 4 | Bestiary re-count | **708** total; **708** AC/HP/combat; **698** sandbox; **10** authored; **26** recharge |
| 5 | `tsc` + sim | **`npx tsc --noEmit` clean**; sim smoke pass (numbers above) |
| 6 | Balance P0 progress | **Partial** — see below |
| 7 | T6–T10 | **Still draft/unmapped** |
| 8–9 | Docs + stamp | This section + CONTINUITY_REPORT Phase B stamp |

### Gate status (post Phase B)

| Gate | Status |
|------|--------|
| A–B, D–G | **Pass** |
| C | **Pass** (Mercy drift corrected in continuity docs) |
| F | **Pass T1–5** / **Draft T6–10** |

### Balance P0 progress (W3 + W4)

| P0 item | Progress |
|---------|----------|
| Provenance / safety labels | Partial — draft XP UI labeled; sandbox combat `draft: true`; T6–10 Draft badges in Dungeon Guide |
| Structured combat schemas | Partial — recharge columns + 26 authored recharge rows; 708 draft payloads |
| Class/spell effect completion | Partial — **W3** ceiling caps (informational, not enforced) |
| Test harness | Partial — sim includes recharge expected DPR; CR 1/3/10 bands |
| Full rulebook ingest | **Open** |

### Drift / watch items

- **Bloom L3** at **93.2%** party HP loss with Spore Burst recharge — **above** 40–70% draft tuning band (sim flags “very hard”). Author tune or recharge cadence review.
- **Vaskor L8** at **58.2%** — within band.
- Historical CONTINUITY stamps (wave 63 multiclass “still draft”, midnight “all ten oaths draft”) **superseded** by Phase B current-status block; Grief promoted 2026-07-30.

### P0 remaining (post Phase B)

**Continuity VQ:** P0 = 0 · P1 = 0

**Balance P0 (still open):**

1. Full rulebook provenance metadata (`confirmed | draft | legacy-unverified`) across rules data  
2. Companion safety boundaries on Bestiary XP / CR-tier filters (partial)  
3. Executable combat beyond draft sandbox + recharge assumptions  
4. Enforced class/spell effect schemas (caps are informational only)  
5. Source-backed benchmark suite + owner-approved XP award canon  

**Mercy fix:** **Done** — continuity docs now match code (`draft: true`); owner did not promote Mercy.

*Oversight Phase B complete — 2026-07-30.*

---

## Oversight Phase C — continuity cleanup (2026-07-30)

**Agent:** Oversight (1)  
**Verdict:** **Clean pass** — all pass-with-drift items resolved; Gates A–G **Pass** (not pass-with-drift).

### Fixes applied

| # | Item | Action |
|---|------|--------|
| 1 | **Mercy canon drift** | Confirmed `draft: true` in data; fixed remaining stale claims in `CHARGEN_PROGRESSION.md`, `content-gap-report.json`, `CONTINUITY_REPORT.md` “good shape” bullet. Glossary + Gate C checklist already correct from Phase B. **No Mercy promotion.** |
| 2 | **Shadow / Grief promotions** | Updated `CHARGEN_PROGRESSION.md`, `OVERNIGHT_HANDOFF.md` coffee table, `content-gap-report.json`. Historical wave stamps marked superseded; Shadow tone-pass stamp annotated with promotion date. |
| 3 | **Resonance multiclass “still draft”** | Updated `OVERNIGHT_HANDOFF.md` current-status blocks; Hybrid-B = approved canon per `RESONANCE_CANON.md` §7. Historical wave logs unchanged. |
| 4 | **XP Builder legacy thresholds** | Verified `CANON_XP_THRESHOLDS` wired; updated `XP_ADVANCEMENT_CANON.md` owner-action line and `BALANCE_DM_XP.md` dependency order. |
| 5 | **Bloom hot (93.2%)** | Excel-first retune: Spore Burst **4d6 / recharge 5-6 → 1d8 / recharge 6**; re-ingest; sim **68.4%** party loss at L3. Vaskor **58.2%** unchanged. |
| 6 | **Combat sim docs** | `BALANCE_COMBAT_SIM.md` impact table + takeaway updated. `author_recharge_attacks.py` guardian template synced. |

### Gate status (post Phase C)

| Gate | Status |
|------|--------|
| A–G | **Pass** |

Gate C note: 10 mysteries + 10 curses + 7 circles wired. **Promoted:** Ancestor, **Shadow** (`draft: false`), Spiral-Touched (no draft flag). **Promoted oath:** **Grief** (`draft: false`). **Mercy** `draft: true` (rulebook prose exists, not promoted). 8 mysteries + 8 oaths + 9 curses remain draft.

### Validation

| Check | Result |
|-------|--------|
| `npx tsc --noEmit` | **Clean** |
| Combat sim smoke | **Pass** — Bloom **68.4%**, Vaskor **58.2%** |
| Bestiary ingest | **708** rows stable post Excel edit |
| Draft promotions | **None** — no mass oath/mystery promotion |

### Remaining (not continuity drift)

- Balance **P0** open: award canon, enforced effect schemas, full rulebook provenance metadata.
- T6–10 **still unmapped** (`mapped: false`, `draft: true`).
- All bestiary combat payloads remain **`draft: true`** (sandbox + authored).

*Oversight Phase C complete — 2026-07-30.*

---

## Oversight — decennial opening window (2026-07-30)

**Agent:** Continuity (owner lock)  
**Verdict:** **Drift cleared in companion docs**

| Topic | Resolution |
|-------|------------|
| **Opening window canon** | **100 days / 2400 hours** — owner lock 2026-07-30 |
| **Prior drift** | Matrix `.docx` + extract said **240 hours** — typo/drift, not horn |
| **1200 h Horn PoNR** | **Live** — `HORN_AT = 1200`; Opening **2400 h** |
| **Relationship** | **Pending owner** — how horn budgets nest inside 100-day opening |
| **Companion code** | **No change** — no opening-duration field in `dungeon-mechanics.json` |

**Deliverable:** [`DESCENT_WINDOW_CANON.md`](./DESCENT_WINDOW_CANON.md) · corrected [`MATRIX_OF_OBLIVION_EXTRACT.md`](../playtest/MATRIX_OF_OBLIVION_EXTRACT.md). No commit.

---

## Oversight — Silent Ones owner lore lock (2026-07-30)

**Agent:** Continuity (owner lock)  
**Verdict:** **GM-secret stratum documented**

| Topic | Resolution |
|-------|------------|
| **Silent Ones** | Owner lock — **unknown to world/PCs**; built dungeon **with loot as bait** for discover → release |
| **The PACT** | Keep Silent Ones **silent**; **war as dissonance**; Matrix of Oblivion **centralized** (maps to Divine Pact in Matrix extract) |
| **Peace trigger** | World **peace** → **Old Ones awaken** → silence universe |
| **Public vs secret** | Crucible / Calan'thir / Asmodeus / Divine Pact = **public myth layer**; not deleted — tension flagged |
| **Open** | Silent Ones = Old Ones? Public builder vs secret builder? |

**Deliverables:** [`SILENT_ONES_CANON.md`](./SILENT_ONES_CANON.md) · Owner lock § [`DUNGEON_CREATION_PURPOSE.md`](../playtest/DUNGEON_CREATION_PURPOSE.md) · Matrix extract note · `CONTINUITY_REPORT.md` stamp. **Not** in newcomer guides. No commit.

---

## Oversight — owner cosmology locks, round 2 (2026-07-30, same date)

**Agent:** Continuity (owner lock) · **Verdict:** **Six of seven owner questions answered and locked; Level 97 Old God (Q6) explicitly left open**

Same-day follow-up round answering the open questions the two locks above raised, plus new rulings on Appendix B and gate names. Full quote-heavy record: [`OWNER_COSMOLOGY_LOCKS_2026-07-30.md`](./OWNER_COSMOLOGY_LOCKS_2026-07-30.md).

| Topic | Resolution |
|-------|------------|
| **Silent Ones = Old Ones (Q1)** | **Confirmed same entity.** Supersedes round-1 open question. |
| **The Pact = Divine Pact (Q2)** | **Confirmed, no rename.** |
| **Authorship (Q3)** | **Two true layers, not competing.** Public: Calan'thir & Asmodeus, real joint builders of the Crucible. Secret: Silent Ones/Old Ones built the pre-existing **Heartcell** machine; Calan'thir & Asmodeus discovered/claimed/activated it. Loot-as-bait and "dungeon contradicts the Old Ones" are **one mechanism**. Player-knowledge model locked (public myth = complete at start; truth discoverable via floor contradictions, never common knowledge). |
| **Clocks (Q4)** | Opening **2400h/100 days unchanged**. **Horn re-stamped at 1200h/day 50 = point of no return, inside the opening**. **Runtime purged 2026-07-31** (`HORN_AT = 1200`, `hornRule` day-50) — see [`OPENING_CLOCK_PURGE_2026-07-31.md`](./OPENING_CLOCK_PURGE_2026-07-31.md). Prior 120h Session UI = archive only. |
| **Appendix B (Q5)** | **Kept as mortal folk religion, not objective canon.** Player Rulebook **patched 2026-07-31** (title + disclaimer + reframes) — [`PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md`](./PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md). Brief: [`APPENDIX_B_FOLK_RELIGION.md`](./APPENDIX_B_FOLK_RELIGION.md). |
| **Gate names (Q7)** | **Bestiary/live roster is the only canon gate-guardian set.** Older Velkyrion/Zeharra/Kharix-style cosmology names and the Cosmology XIV gate-boss list (Hollow King/Cindervore/Vox Prime) are **formally retired** as combat figures where they conflict — formalizes what `WORLD_DUNGEON_LOOP.md` WDL-1 already treated as resolved in practice. |
| **Level 97 Old God (Q6)** | **RESOLVED 2026-07-31.** Owner: **Floor 97 = regular zone with hidden chamber (Old Ones sleep); true conquest L100 boss → focusing crystal → weaken Old God; else L30 mind-control near wipe.** Do not invent further. Remains optional follow-ups for Silent Ones relation / F97 room. |

### Validation

| Check | Result |
|-------|--------|
| Files edited | Docs only — [`OWNER_COSMOLOGY_LOCKS_2026-07-30.md`](./OWNER_COSMOLOGY_LOCKS_2026-07-30.md) (new), `SILENT_ONES_CANON.md`, `DESCENT_WINDOW_CANON.md`, `DUNGEON_CREATION_PURPOSE.md`, `APPENDIX_B_FOLK_RELIGION.md` (new), `A_TO_Z_MASTERY_DIGEST.md`, `READY_TO_CONTINUE.md`, `CONTINUITY_REPORT.md`, this file. Annotation-only pointers added to `WORLD_DUNGEON_LOOP.md`, `NEWCOMER_GM_GUIDE.md`, `HIDDEN_DUNGEON_EQUATION.md`, `SESSION_LOOP.md`, `COMBAT_SYSTEM_COMPARE.md`. |
| `src/` code changes | **Purged 2026-07-31.** `HORN_AT = 1200`; `hornRule` day-50 PoNR — see [`OPENING_CLOCK_PURGE_2026-07-31.md`](./OPENING_CLOCK_PURGE_2026-07-31.md). |
| Historical playtest logs | **Intentionally unedited** (SIM_02/04, T4_* series, `characters/P2_CASUAL_5E.md`) — they record sessions actually run under the pre-existing 120h clock; rewriting their numbers would falsify the historical record. |
| Prior citations | **Not deleted.** Round-1 stamps in this file and `CONTINUITY_REPORT.md` remain, annotated as superseded-in-part rather than removed. |

*Oversight — owner cosmology locks round 2 complete — 2026-07-30. No commit.*

---

## Oversight — rulebook source-of-truth process (2026-07-30)

**Agent:** Continuity (process lock)  
**Verdict:** **Mandatory hierarchy documented; four override questions drafted for owner**

| Topic | Resolution |
|-------|------------|
| **Priority order** | Owner spoken lock → Player Rulebook / DM Manual (published) → companion code/data → playtest sims |
| **Player Rulebook paths** | `decennium descent player rulebook.docx` · `rulebook_output.txt` (UTF-16LE) · mirrors/backups listed in deliverable |
| **DM Manual layer** | **No file named "DM Manual" on disk** — Matrix, Cosmology, World of Aethel, Floor Encounters docx + extracts + JSON mirrors |
| **Audit protocol** | Continuity **must open both rulebooks** (or extracts) when auditing; encoding note for `rulebook_output.txt` |
| **Override gate** | STOP + ask owner **(a)/(b)/(c)** before overwriting published rulebook/DM text |
| **Open overrides (as of process lock day)** | Q-OV-1 · Q-OV-2 · Q-OV-3 · Q-OV-4 — **later same-week status:** Q-OV-1 **closed** (2400/1200); Q-OV-2 **closed** (**12 max** / rulebook RAW; T4 24-PC = playtest only); Q-OV-3 **player patch applied 2026-07-31**; Q-OV-4 **closed** (DM-01 Ch 8); Q6 framing **closed** (**Floor 97 = regular zone with hidden chamber (Old Ones sleep); true conquest L100 boss → focusing crystal → weaken Old God; else L30 mind-control near wipe**) — see [`CONTINUITY_SOURCE_OF_TRUTH.md`](./CONTINUITY_SOURCE_OF_TRUTH.md) §5. SoT split still **OPEN** |

**Deliverables:** [`CONTINUITY_SOURCE_OF_TRUTH.md`](./CONTINUITY_SOURCE_OF_TRUTH.md) · `.cursor/rules/continuity-rulebooks.mdc` · stamps in `CONTINUITY_REPORT.md`, `READY_TO_CONTINUE.md`, `A_TO_Z_MASTERY_DIGEST.md`. No commit.

---

## Oversight — expedition structure owner lock (2026-07-30)

**Agent:** Continuity (owner re-assertion) · **Verdict:** **RAW confirmed — structure locked; UI gaps documented**

| Check | Result |
|-------|--------|
| **Primary source located** | `rulebook_output.txt` **3801–3926** (UTF-16LE); duplicate in `feat_compendium_output.txt` |
| **JSON alignment** | `dungeon-mechanics.json` `expedition` matches team names, size bands, `timePeriods` — hard-coded via `tools/ingest_lorebook.py`, not parsed from rulebook at ingest |
| **Companion display** | `DungeonGuide.tsx` Expedition card — read-only |
| **Session UI** | Combat + horn only; **no** team assignment, period planner, or off-combat activity tracker |
| **Playtest drift flagged** | T4 **24 PC** sims = coalition exception; SIM #1–#4 **7–8 PC** = valid; historical logs unedited |
| **Code changes** | **None** |

**Deliverable:** [`EXPEDITION_STRUCTURE_CANON.md`](./EXPEDITION_STRUCTURE_CANON.md) · `CONTINUITY_REPORT.md` stamp · cross-links in `DESCENT_WINDOW_CANON.md`, `WORLD_DUNGEON_LOOP.md`, `A_TO_Z_MASTERY_DIGEST.md`, `READY_TO_CONTINUE.md`, `NEWCOMER_GM_GUIDE.md`, `SIM_CAMPAIGN_PLAN.md`, `SESSION_LOOP.md`. No commit/push per brief.
