# TTRPG completion gap inventory

**Date:** 2026-07-31  
**Workspace:** `DecenniumDescent-main`  
**Scope:** What remains to call Decennium Descent a **shippable, table-ready full TTRPG** (campaign companion + books) — **not** a 3D MMO.  
**Strategy lock:** TTRPG companion first (rules, characters, spells, monsters, items/crafting, dungeon guide, cosmology, encounters, generators); just enough MMO feel; Unity/Unreal later only; no SWTOR in product.  
**Method:** Read-only scan of continuity SoT, Director/Player manuals, mechanics audits, companion features/data, playtest docs. **No feature work. No commit.**

**Primary citations:** [`CONTINUITY_SOURCE_OF_TRUTH.md`](./CONTINUITY_SOURCE_OF_TRUTH.md), [`RULESET_VULNERABILITIES.md`](./RULESET_VULNERABILITIES.md), [`CONTENT_GAPS.md`](../../src/data/CONTENT_GAPS.md), [`MECHANICS_ROADMAP.md`](../MECHANICS_ROADMAP.md), [`A_TO_Z_MASTERY_DIGEST.md`](../playtest/A_TO_Z_MASTERY_DIGEST.md), [`READY_TO_CONTINUE.md`](../playtest/READY_TO_CONTINUE.md), [`DIRECTOR_EDITION_BIBLE_REVIEW.md`](../manuals/DIRECTOR_EDITION_BIBLE_REVIEW.md), [`PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md`](./PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md), [`AUTHOR_REVIEW_QUEUE.md`](./AUTHOR_REVIEW_QUEUE.md), [`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md), [`BOOK_LINEUP.md`](../manuals/BOOK_LINEUP.md).

---

## 0. Verdict (one paragraph)

Decennium Descent is **past the “empty shell” stage** and into **early campaign product**: a Player Rulebook with Opening/Horn and Appendix B folk framing aligned to Director procedure; a Complete Director Edition bible usable through Tier 1 / Ashen Bell; companion tabs for chargen, Session, Dungeon Guide, spells (~832), bestiary (~700+), crafting recipe names (623), encounters/generators, and cosmology. Continuity process and major lore locks (Umbrin, 17 classes, Resonance Hybrid-B, Silent Ones = Old Ones, 2400/1200 clocks) are in place. It is **not** yet a **complete tabletop game** in the shippable sense: XP *awards* are rulebook-missing; most monster combat is sandbox-draft; Tiers 6–10 are rumor stubs; crafting has **zero** filled `components[]`; many Oracle/Paladin trees and prestige capstones remain unpromoted; Director book pointers still split across Complete Edition vs legacy manuals vs missing `The_Directors_Crucible.md` lineup paths. Honest estimate: **~60–70% of a Tier 1–5 table-ready campaign**, **~40–50% of a Floor 1–100 campaign product**, if “complete” means a Director can run without inventing core economy/combat/award rules from scratch.

---

## 1. What recently closed (baseline — do not re-open)

| Item | Status |
|------|--------|
| Opening **2400 h / 100 days**; Horn PoNR **1200 h / day 50** | Closed (Q-OV-1); bible typo + literature/app purge |
| Player Rulebook shared procedures vs DMG | Opening clock, public Crucible myth, coalitions, Appendix B folk rename/disclaimer |
| Bestiary lore pass + Gate Guardians CR ladder + ingest | Done (2026-07-30 pass) |
| Silent Ones = Old Ones; Heartcell authorship; Pact = Divine Pact | Owner locks (docs); **Q-OV-4 closed** in DM-01 Ch 8 + Guardrails (2026-07-31) |
| 17-class roster; Fighter/Swashbuckler archive | Locked |
| Resonance Hybrid-B + multiclass merge | Canon in companion + rulebook text |
| Mystery of Shadow + Oath of Grief | Promoted |
| Continuity SoT process + Cursor rule | Mandatory |
| **T6–10 / F1–100 Director stance** | Defined 2026-07-31 — DM-01 ops Ch 63–68 + Deep Opening stance; milestones through Marquis; Q6 Level 97 framing **RESOLVED** (regular zone + hidden chamber) ([`F1_100_RULES_TRACK_2026-07-31.md`](./F1_100_RULES_TRACK_2026-07-31.md)) |

---

## 2. Continuity stance — bible vs four-book rebuild

| Layer | Role | Gap |
|-------|------|-----|
| **`The_Directors_Crucible_Complete_Director_Edition.docx`** | Living Director **procedure bible** (recommended primary for ops) | Not yet renamed/promoted to `BOOK_LINEUP` DM-01 paths; Continuity SoT §2 still lists legacy `Decennium_Descent_Directors_Manual.*` as primary |
| **Four-book rebuild** (Codex / Instruments / Chronicle + intended Crucible) | Topic-split volumes (bestiary ecology, toolbox, setting) | `The_Directors_Crucible.md/.docx` **missing** from lineup filenames; Complete Edition overlaps Crucible scope |
| **Legacy Directors Manual + Bestiary of Aethel** | Generated archives / agent refs | Keep as archive once DM-01 path is fixed; regenerate script still points here |
| **Owner lock MDs** | Intent SoT | Do not silently overwrite Player Rulebook / Matrix `.docx` |

**Recommendation:** One owner decision — **promote Complete Edition as official DM-01** *or* extract it into lineup paths — then demote legacy Directors Manual to archive in Continuity SoT + `AGENT_SIMULATION_REFERENCE.md`.

---

## 3. Gap inventory by bucket

Priority tags:

- **Must-have** — required to honestly claim “complete / shippable TTRPG campaign product” (table can run T1–5 without inventing core systems; books + companion agree).
- **Should-have** — strongly improves trust, balance, depth, or Director comfort; playtest can proceed with draft badges + GM fiat.
- **Later / MMO-feel** — polish, deep tiers, automation, social persistence, 3D handoff — after TTRPG completeness or explicit pivot.

---

### 3.1 Core rules completeness (Player + Director)

| Gap | Priority | Notes |
|-----|----------|-------|
| **XP award rules** (CR→XP, split, encounter budgets) | **Resolved for Opening** — milestone-only official T1–10; no CR→XP published | [`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md); Session CR→XP stays optional/non-canon |
| **Burnout consequences** undefined / unwired | **Must-have** (or explicit GM-fiat ship label) | M-01 in vulnerabilities |
| **Class ceiling caps** informational only | **Must-have** (ratify as playtest law **or** write real rules) | CL-01 |
| **Resonance specialization discount** unwired; risk of zero-cost spells | **Should-have** | M-02 |
| **13 Weave classes** still on draft RP pool tables | **Must-have** for “rules locked”; **Should-have** if shipping “playtest companion” with badges | M-03 — only Wizard/Mage/Cleric/Druid have rulebook-complete tables |
| **Overcast** not tied to spell picker | **Should-have** | Manual entry works at table |
| Rulebook still contains **dual Resonance model prose** (A vs B) without player-facing “ignore A” flag in places | **Should-have** | Product canon is Hybrid-B |
| **Q-OV-2** expedition max **12** (no 24-PC charter) | **Done** | Owner lock 2026-07-31; coalitions text = RAW |
| **Q-OV-4** labeled GM-only Silent Ones / Heartcell section in **published** DM corpus | **Done** (DM-01) | Matrix/Cosmology `.docx` public layer may still omit labeled GM appendix (intentional dual-layer) |
| Promote Complete Edition → official DM-01 path | **Must-have** (production continuity) | BIB-2 |
| Explicit bible sentence: Silent Ones **are** Old Ones | **Should-have** | BIB-3 |
| Ch 10 Interstice stub; Retune/Full Harmony Director labels | **Later** | BIB-5/6 |
| Legacy `.doc` Player Rulebook sync/retire | **Should-have** | Avoid SoT confusion |
| Appendix B second tone-scrub (history/nations encyclopedia voice) | **Should-have** | Q-OV-3 remainder |

---

### 3.2 Content libraries (monsters, spells, items, crafting)

| Gap | Priority | Notes |
|-----|----------|-------|
| **~698/708** bestiary combat rows = excel-sandbox `draft: true` | **Must-have** for combat-locked product; **Should-have** for T1–5 playtest if Guardians + GM AC/HP check | C-01 |
| **Gate Guardians** authored draft combat (10) — expand tactics / freeze metadata | **Must-have** for Gate play | C-02; lore/CR pass done |
| Excel **NeedsReview** Size/Type/CR not ingested; 430+ heuristic flags | **Must-have** for encounter planning trust | C-05 / Q-01 |
| Spells (~832): incomplete scaling / prep / class access normalization | **Should-have** | M-05 |
| **Feats:** 336 live vs 330-title doc; placeholders; legacy unwired | **Should-have** | Q-04 |
| **Crafting: 623 recipes, all `components[]` empty** | **Must-have** for items/crafting completeness | Instruments + CONTENT_GAPS; engine does not auto-deduct |
| Prestige **18/18 draftCapstone** | **Should-have** | X-05 |
| Generic SRD monster labels (Owlbear etc.) | **Later** / optional IP | Q-03 |
| Rulebook residual **Drow** strings vs Umbrin | **Should-have** | Q-02 |
| Move canonical bestiary JSON under `src/data/`; retire stale 50-row subset | **Should-have** (tooling) | CONTENT_GAPS |

---

### 3.3 Dungeon / Opening operational tools

| Gap | Priority | Notes |
|-----|----------|-------|
| **Tiers 1–5:** narrative strong; **executable floor encounter cards / rosters / budgets** thinner than Floor Encounters.docx | **Must-have** for “encounters complete” | D-03 / C-04 |
| **Tiers 6–10:** DM-01 operational chapters exist; companion may stay `mapped: false` until encounter agents expand | **Should-have** for full encounter cards; **Director stance defined** 2026-07-31 ([`F1_100_RULES_TRACK_2026-07-31.md`](./F1_100_RULES_TRACK_2026-07-31.md)) | D-01 |
| Gate boss Session HP still **stub** `40 + tier×25` | **Should-have** | Wire real bestiary stats |
| Horn clock **display only** — no overrun penalty table | **Later** (fiction of 10-year trap may suffice) | D-04 |
| Craft/research hours vs Opening clock | **Later** | SESSION_LOOP / digests |
| Cycle `entryClasses` / `victoryConsequences` Director draft | **Should-have** | Promote or mark permanent Director fiat |
| Generators: loot names work; full NPC/encounter gen thin | **Should-have** | Lane C |
| Opening Day / Ashen Bell starter already in bible | **Done enough** for T1 ops | Expand Chronicle surface gazetteer as Should-have |

---

### 3.4 Character creation / classes / Resonance

| Gap | Priority | Notes |
|-----|----------|-------|
| **Oracle Mysteries:** 8/10 draft | **Should-have** (batch promote) | Ancestor + Shadow canon |
| **Oracle Curses:** 9/10 draft | **Should-have** | Spiral-Touched canon |
| **Paladin Oaths:** 9/10 draft (incl. Mercy with rulebook prose) | **Should-have** | Grief canon; Mercy promote is high-traffic |
| **L11–20** milestones draft for most classes | **Should-have** for mid/high campaign | X-04 |
| Skill modifiers hardcoded in Builder | **Should-have** | CL-05 |
| Session **wild-shape** uses/CR tracker | **Should-have** | T-03 |
| Multiclass UI + RP merge | **Done** | — |
| 17 classes + paths + backgrounds + races | **Done enough** for chargen smoke | Cosmology-only races intentionally excluded |
| Character appearance mannequin stub | **Later / MMO-feel** | Strategy: workable stub only |

---

### 3.5 Cosmology & setting (player-safe vs Director)

| Gap | Priority | Notes |
|-----|----------|-------|
| Public Crucible myth in Player Rulebook | **Done** (2026-07-31) | No Silent Ones in player book (correct) |
| Appendix B folk religion framing | **Mostly done**; optional second scrub | — |
| GM-secret Silent Ones / Heartcell in **official** DM volume | **Done** (DM-01 Ch 8 / Guardrails) | Q-OV-4 closed |
| **Level 97 / hidden chamber** | Framing locked; mechanical gaps optional | **RESOLVED** — **Floor 97 = regular zone with hidden chamber (Old Ones sleep); true conquest L100 boss → focusing crystal → weaken Old God; else L30 mind-control near wipe.** ([`LEVEL_97_OLD_GOD_Q6_OPEN.md`](./LEVEL_97_OLD_GOD_Q6_OPEN.md)); do not invent | Lock J / Q6 |
| **Peace-trigger** threshold (“world knows peace”) | **Should-have** for endgame Director tools | Still undefined |
| Cosmology First Song chapter nav / world section stubs | **Should-have** | Companion viewer polish |
| Owner’s **hidden equation / counterpoint** not in repo | **Later** (Director annex) | `HIDDEN_DUNGEON_EQUATION.md` is absence report only |
| Yieldheart naming collision (caverns vs city) | **Later** | Owner glance |
| Deep-tier gazetteer flesh (T7–10) | Tied to T6–10 stance | — |
| Surface travel / law / languages (Chronicle) | **Should-have** for campaign setting product | GAP_FILL setting topics |

---

### 3.6 Continuity / open owner questions

| ID | Topic | Blocks what | Status |
|----|-------|-------------|--------|
| **Q-OV-1** | Horn / Opening clocks | — | **RESOLVED** 2400/1200 |
| **Q-OV-2** | Expedition 12 vs T4 24-PC | — | **RESOLVED** 2026-07-31 — **12 max** / rulebook RAW; T4 24-PC = playtest only |
| **Q-OV-3** | Appendix B rewrite | — | **Player patch applied**; optional tone pass |
| **Q-OV-4** | Silent Ones authorship in published DM | Official Director secret section | **RESOLVED** DM-01 Ch 8 |
| **J / Q6** | Level 97 = regular zone + hidden chamber | Optional F97 / Silent Ones follow-ups | **RESOLVED** 2026-07-31 |
| **XP awards** | Approve draft CR→XP or author | Progression loop + rulebook | **RESOLVED** milestone-only Opening (T1–10) |
| **Burnout + specialization + ceiling caps** | Wire or explicit GM fiat | Ruleset lock claim | Burnout + ceilings = **GM fiat** ship labels; specialization still Should-have |
| **T6–10 product stance** | Full map vs “T5 campaign + stubs” | Scope of “complete” | **Defined** — Director ops in DM-01; encounter cards later ([`F1_100_RULES_TRACK_2026-07-31.md`](./F1_100_RULES_TRACK_2026-07-31.md)) |
| **Peace trigger** | Endgame Director tools | Cosmic stakes adjudication | **Open** |
| **BIB-2 lineup** | Which file is official DM-01 | Agent/Director SoT | **RESOLVED** Complete Edition = DM-01 |
| Nested micro-clock beside 1200h? | Owner caveat once floated | — | **Open / low** — default: no |

---

### 3.7 App companion — blocks table use vs nice-to-have

**Table-ready today (with draft honesty):** Character Builder/Sheet, Session (init, HP, RP/RC, Retune/Full, overcast stub, horn display, reputation), Spells/Monsters/Items/Crafting browsers, Dungeon Guide (tiers/gates), Encounters, Generators (partial), Cosmology viewer, Prestige requirements, Chargen warnings, Class ceiling callouts.

| Gap | Priority |
|-----|----------|
| XP write-back to character saves (after award canon) | **Must-have** for progression loop |
| Gate boss / foe HP from real bestiary combat | **Should-have** |
| Spell-linked overcast + Burnout enforcement | **Should-have** (after owner defines Burnout) |
| Wild-shape Session tracker | **Should-have** |
| Global header search (decorative today) | **Later** |
| Expedition team/period assignment UI | **Later / MMO-feel** (rulebook exists; Session is combat table) |
| Death saves automation | **Later** (explicitly out of scope) |
| Meditation recovery UI | **Later** |
| Full effect schema for sim/enforcement | **Later** unless claiming balance-locked |
| Unity / character models beyond mannequin | **Later / MMO** — strategy forbids now |

---

### 3.8 Production (editing, print/PDF, indexes, art)

| Gap | Priority | Notes |
|-----|----------|-------|
| Single **print/PDF pipeline** for Player + Director line | **Must-have** for “shipped book product” | Markdown/docx exist; layout/proof not proven |
| Cross-book **indexes**, condition appendices, page refs | **Should-have** | |
| Art direction stubs / placeholder plates (no SWTOR) | **Should-have** for commercial feel; **Later** for private playtest | |
| Newcomer GM + Player guides already exist | **Done enough** for playtest onboarding | Polish as Should-have |
| IP scrub pass on Player Rulebook Great Wheel leftovers / SRD terms | **Should-have** | Folk framing reduces urgency |
| Copyrighted reference PDFs in `docs/manuals/` | **Process** — topic checklist only; do not ship mirrors | `GAP_FILL_FROM_REFERENCE_TOPICS.md` |

---

## 4. Sequenced roadmap

### Phase 0 — Owner decisions (do these first; they unblock authorship)

1. **XP awards:** ~~Approve draft CR→XP~~ **RESOLVED 2026-07-31** — milestone-only official for Opening T1–10 ([`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md)).
2. **T6–10 product stance:** **DEFINED 2026-07-31** — Director ops in DM-01; companion encounter maps may lag ([`F1_100_RULES_TRACK_2026-07-31.md`](./F1_100_RULES_TRACK_2026-07-31.md)).
3. **Q-OV-4:** **RESOLVED** — Silent Ones / Heartcell in DM-01 Ch 8 + Guardrails.
4. **Level 97 (Q6):** Framing **RESOLVED** — **Floor 97 = regular zone with hidden chamber (Old Ones sleep); true conquest L100 boss → focusing crystal → weaken Old God; else L30 mind-control near wipe.** Optional gaps remain ([`LEVEL_97_OLD_GOD_Q6_OPEN.md`](./LEVEL_97_OLD_GOD_Q6_OPEN.md)).
5. **Burnout + ceiling caps + specialization:** Burnout + ceilings = permanent GM fiat; specialization still Should-have to wire.
6. **BIB-2:** **RESOLVED** — Complete Director Edition is official DM-01.
7. ~~**Q-OV-2 (optional):** Charter exception~~ — **RESOLVED** 2026-07-31: **12 max**; coalitions-only.

### Phase 1 — Lock the table loop (Must-have for “playable campaign product”)

8. Ingest XP rules into Player Rulebook (or milestone chapter) + Session write-back.  
9. Floor **encounter cards / rosters / budgets for T1–5** from Floor Encounters sources.  
10. Freeze **10 Gate Guardians** combat + metadata QA; wire Session gate HP from bestiary.  
11. Fill **crafting `components[]`** (or ship salvage tables + honest “recipes are unlock names only”).  
12. Apply Q-OV-4 into the official Director volume; stamp Continuity SoT pointers to DM-01.

### Phase 2 — Chargen trust & mid-campaign (Should-have)

13. Promote **Mercy** + next 2–3 high-traffic Mysteries/Oaths/Curses per owner review sessions.  
14. Author or promote **non-core RP pool tables**; wire specialization + Burnout if Phase 0 chose wire.  
15. Feats reconciliation; skill derivation; prestige capstone pass.  
16. L11–20 rulebook cross-check for classes that will see play beyond T5.

### Phase 3 — Full hundred-floor / production (Must-have only if Phase 0 chose full depth)

17. Author T6–10 routes, encounters, rewards (and Level 97 if Q6 says yes).  
18. Expand Chronicle surface gazetteer + deep-tier flavor.  
19. Print/PDF + indexes + art stubs.  
20. Optional: balance harness, effect schema, global search, wild-shape enforcement.

### Phase 4 — Later / MMO-feel (explicitly after TTRPG completeness)

- Persistent social/guild hooks, richer appearance editor, expedition UI for five teams/periods, 3D client — **only after** Phase 1–2 (and Phase 3 if required by stance), or on explicit owner pivot.

---

## 5. Recommended next 5–12 concrete actions

**Owner (decisions — do first):**

1. Approve or reject draft **XP award** package (or milestone-only).  
2. Choose **T1–5 complete vs full T1–10** definition of “done.”  
3. Answer **Q-OV-4** + **Level 97 Old God**.  
4. Ratify **Burnout / caps / specialization** as fiat vs wire.  
5. **Promote DM-01** path (Complete Edition → lineup).

**Workers (after Phase 0):**

6. Patch Continuity SoT + `BOOK_LINEUP` / agent refs to DM-01.  
7. Build T1–5 encounter operational cards from Floor Encounters.  
8. Fill crafting components (or documented salvage workaround).  
9. Session: XP write-back + real gate-boss stats.  
10. Author-review batch: Mercy + 2 Mysteries/Curses.  
11. Bestiary metadata QA pass (NeedsReview → JSON flags).  
12. Optional App B tone scrub + legacy `.doc` retire.

---

## 6. Definition checklist — “complete TTRPG” (proposal)

Use this as the acceptance bar once Phase 0 is answered:

| Criterion | Minimum bar |
|-----------|-------------|
| Player Rulebook | Chargen → combat → Resonance → expeditions → Opening clocks → folk cosmology consistent with Director public layer |
| Director bible | Session zero → T1 seal → Opening ops → secret/public layering; clocks 2400/1200; lineup unambiguous |
| Combat | Gate Guardians playable; T1–5 trash plannable (authored or budgeted substitutions); draft sandbox labeled |
| Progression | Confirmed thresholds **and** approved award method (or milestone) |
| Content | Spells/feats usable; crafting not infinite-free; 17 classes selectable with draft honesty |
| Dungeon | T1–5 operational; T6–10 either authored **or** explicitly out of v1 scope |
| Companion | Supports chargen + session loop without contradicting books |
| Production | Exportable Player + Director books (PDF/docx) without SWTOR/IP landmines |

---

## 7. Related documents

| Doc | Use |
|-----|-----|
| [`CONTINUITY_SOURCE_OF_TRUTH.md`](./CONTINUITY_SOURCE_OF_TRUTH.md) | Priority hierarchy + Q-OV-* |
| [`RULESET_VULNERABILITIES.md`](./RULESET_VULNERABILITIES.md) | Finalize blockers |
| [`MECHANICS_ROADMAP.md`](../MECHANICS_ROADMAP.md) | Lane A/B/C work packages |
| [`CONTENT_GAPS.md`](../../src/data/CONTENT_GAPS.md) | Library inventory |
| [`DIRECTOR_EDITION_BIBLE_REVIEW.md`](../manuals/DIRECTOR_EDITION_BIBLE_REVIEW.md) | Bible vs rebuild stance |
| [`PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md`](./PLAYERBOOK_DMG_ALIGNMENT_2026-07-31.md) | Player↔DM shared procedures |
| [`READY_TO_CONTINUE.md`](../playtest/READY_TO_CONTINUE.md) | Owner locks one-pager |
| [`GAP_FILL_FROM_REFERENCE_TOPICS.md`](../manuals/GAP_FILL_FROM_REFERENCE_TOPICS.md) | Manual topic checklist |

---

*Inventory only — 2026-07-31. No commit. No feature implementation.*
