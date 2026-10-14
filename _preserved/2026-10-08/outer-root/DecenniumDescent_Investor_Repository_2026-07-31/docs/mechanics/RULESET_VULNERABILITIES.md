# Ruleset vulnerabilities — finalize blockers

**Date:** 2026-07-30  
**Scope:** Honest inventory of remaining holes blocking a **finalized, playtest-locked ruleset** for Decennium Descent v1.  
**Sources:** `BALANCE_REPORT.md`, `XP_ADVANCEMENT_CANON.md`, `BESTIARY_INGEST.md`, `CLASS_CEILING_CAPS.md`, `BALANCE_PLAYER_CLASSES.md`, `CONTINUITY_SOURCE_OF_TRUTH.md`, `MECHANICS_ROADMAP.md`, live data in `src/data/*` and `src/bestiary_data_full.json`.

**Verdict:** The companion is **playable for table tracking and chargen smoke tests**, but the ruleset is **not balance-verifiable or lock-ready**. Confirmed canon stops at discrete islands (17 classes, L1–L20 XP thresholds, four full RP tables, Hybrid-B multiclass merge, two Oracle Mysteries + one Oath promoted, one Oracle Curse rulebook-complete). Everything else below is draft, heuristic, or unwired.

---

## Severity key

| Severity | Meaning |
|----------|---------|
| **Blocks finalize** | Cannot claim “ruleset locked” until resolved or explicitly accepted as GM fiat |
| **Playtest risk** | Table can run, but outcomes may be unfair, exploitable, or falsely labeled canon |
| **Polish** | UX, prose, or author-review quality; improvable without blocking a cautious playtest |

**Owner decision:** **Y** = requires owner sign-off before promotion to canon; **N** = engineering/author work only.

---

## 1. Combat / bestiary

| ID | Vulnerability | Severity | Owner? | Notes |
|----|---------------|----------|--------|-------|
| C-01 | **698 / 708** bestiary rows use **excel-sandbox** draft combat (`generate_bestiary_combat_sandbox.py` CR-band templates) | Blocks finalize | N | All marked `draft: true`, `source: "excel-sandbox"`. Usable for sim alerts only — not authored encounters. |
| C-02 | Only **10 gate guardians** have companion-authored draft combat; merge rule is Excel-wins-when-populated | Playtest risk | N | Bloom/Vaskor sim bands (~63–68% / ~46–58% L3/L8 party loss) depend on draft at-will payloads. |
| C-03 | **Recharge coverage:** **26 / 708** entries carry recharge payloads; sim uses **draft cadence assumptions** (available round 1, P(recharge) steady-state, 55% save fail, area = single-target) per `MONSTER_COMBAT_SCHEMA.md` | Playtest risk | N | Recharge DPR is alert-only. Bloom Spore Burst retuned 2026-07-30; area/multi-target still excluded from sim. |
| C-04 | **Non-boss / roaming coverage:** no floor encounter rosters, budgets, or validated substitutions — CR-tier browse is heuristic | Blocks finalize | Y | Gate bosses are sanity checks, not proof of tier-appropriate trash fights. |
| C-05 | Excel **`NeedsReview`** QA column is **not ingested** to JSON; **430+** metadata rows flagged for Size/Type/CR garbage (`BESTIARY_INGEST.md` heuristics) | Playtest risk | Y | Wrong CR/Size breaks encounter planning and draft XP lookups. |
| C-06 | High-impact class features and most spells lack executable action/save/duration/recharge fields — combat is **descriptive, not simulatable** | Blocks finalize | N | See `BALANCE_REPORT.md` §2 cross-cutting blockers. |

**Suggested fix order:** C-06 schema contract → C-02 expand authored guardians + spot-check bands → C-05 metadata QA pass (gate bosses frozen) → C-03 recharge author pass + revised sim assumptions → C-04 floor rosters from source docs → C-01 replace sandbox bulk only after benchmark suite exists.

---

## 2. Class balance

| ID | Vulnerability | Severity | Owner? | Notes |
|----|---------------|----------|--------|-------|
| CL-01 | **`class-ceiling-caps.js` is informational only** — Builder/Sheet callouts, **zero enforcement** in Session or resolution | Blocks finalize | Y | Caps cover Mirrorsage, Oracle, Paladin, Warrior, Dragoon, Tinker only. Owner must accept caps as playtest law or author real rules. |
| CL-02 | **Mirrorsage** — copy eligibility, echo ceiling, boss exclusions undefined in mechanics | Playtest risk | Y | Highest ceiling risk per `BALANCE_PLAYER_CLASSES.md` §3. |
| CL-03 | **Oracle / Paladin / Tinker / Warrior / Dragoon** — draft L11–20 + subclass trees can exceed bounded play without table ledger | Playtest risk | Y | Tied to draft content promotion (§6). |
| CL-04 | **Armor/AC/proficiency conflicts** between `rulebook_output.txt` and companion for Crimson Agent, Dragoon, Mirrorsage, Oracle, Tinker | Playtest risk | Y | Paper audit cannot rank durability fairly. |
| CL-05 | **Skill modifiers** in Builder are static, not derived from abilities + proficiencies | Polish | N | Does not block combat but breaks chargen truth. |
| CL-06 | **34 ASI placeholder** strings in `class-draft-levels.js` remain intentional draft | Polish | N | Labeled draft; author replace from rulebook tables. |

**Suggested fix order:** CL-01 owner ratifies caps → CL-02 Mirrorsage eligibility list → CL-04 source reconciliation → CL-03 bounded playtests per `BALANCE_PLAYER_CLASSES.md` §5 → CL-05 skill derivation → CL-06 ASI ingest.

---

## 3. Magic

| ID | Vulnerability | Severity | Owner? | Notes |
|----|---------------|----------|--------|-------|
| M-01 | **Burnout unwired** — badges/hints only; **no Session enforcement** | Playtest risk (shipped as GM fiat) | N | 2026-07-31: permanent **GM fiat** (suggested: disadvantage on Weave checks until end of next turn). Not a rules-block for Opening play — see `T1_5_RULES_PACKAGE_2026-07-31.md`. |
| M-02 | **Specialization discount unwired** — `computeSpellCost()` accepts `specialization` but Builder/Session **never pass it**; no eligible-spell list or cost floor | Playtest risk | Y | −1 to −3 RP can zero-cost tier-1 spells under current formula. |
| M-03 | **13 non-core Weave casters** use **draft RP pools** (half 65%, hybrid 50%, minor 35% of Cleric curve) in `resonance-economy.js` | Playtest risk | Y | Wizard/Mage/Cleric/Druid only have rulebook-complete tables. UI shows “draft tier estimate.” |
| M-04 | **Overcast panel** uses manual spell tier + optional school affinity hint — **not tied to spell picker** base cost | Playtest risk | N | Empowered/Quickened/etc. can multiply output without guardrails until M-01 resolves. |
| M-05 | **832 spells** in `spells.js` — incomplete scaling, preparation limits, and class access normalization | Playtest risk | N | Caster vs martial parity unverified. |
| M-06 | Oracle **RC** economy wired for rest/triggers; draft Mystery/Curse trees can break **1 RC/round** intent without table enforcement | Playtest risk | Y | Same as CL-01 Oracle caps. |

**Suggested fix order:** M-01 owner defines Burnout consequences → M-02 specialization list + floor → M-03 promote or revise non-core RP tables → M-04 spell-linked overcast → M-05 spell schema completion → M-06 RC ledger in Session (optional enforce mode).

---

## 4. Progression

| ID | Vulnerability | Severity | Owner? | Notes |
|----|---------------|----------|--------|-------|
| P-01 | **CR→XP / encounter XP budgets unpublished** — Opening campaigns use **milestone-only** (official 2026-07-31) | Polish (optional XP track) | N | Thresholds + milestone Opening are canon. CR→XP remains optional/non-canon Session helpers only. See `XP_ADVANCEMENT_CANON.md`. |
| P-02 | **Draft award helpers** (`draftXpForCr`, `splitPartyXp`, `draftEncounterBudget`) wired in Session as **“Award draft XP”** — session-local tally only | Playtest risk | N | Increments `draftXpSession`; Scene notes line; **no `upsertCharacter()` write-back**; labeled optional/non-canon. |
| P-03 | Static Bestiary **`xp` fields** = metadata only (not Opening awards) | Polish | N | Do not use creature XP as milestone substitute. |
| P-04 | **No encounter-to-progression automation** — milestones are Director-awarded | Polish | N | Intentional for Opening; EV budgets live in T1–5 encounter toolkit. |
| P-05 | **Confirmed L1–L20 thresholds** wired in Builder (`CANON_XP_THRESHOLDS`) — **this part is done** | — | N | Not a vulnerability; included for boundary clarity. |

**Suggested fix order:** Keep milestone Opening as law → optionally author CR→XP later if owner wants XP-track campaigns → P-03 keep bestiary XP as non-award metadata.

---

## 5. Dungeon

| ID | Vulnerability | Severity | Owner? | Notes |
|----|---------------|----------|--------|-------|
| D-01 | **Tiers 6–10** remain **`mapped: false`** — draft seeds only (`regionNames`, `hazards`, `gateBossSeed`, `encounterVibe`) | Blocks finalize | Y | No routes, maps, encounter resolution, rewards, HP, or tactics. GM improv flagged. |
| D-02 | **`entryClasses` / `victoryConsequences`** in `dungeon-mechanics.json` are Director draft (all 17 eligible) | Playtest risk | Y | Re-open if rulebook Ch XII restricts entry. |
| D-03 | Floor encounter **tables** thinner than `Floor Encounters.docx` for T1–5; T6–10 have **no deep-doc ingest** | Playtest risk | N | Narrative ok; executable encounter cards missing. |
| D-04 | **Horn clock** display only — **1200 h / day 50** PoNR → 10-year trap has **no in-session mechanical penalty table** | Polish | Y | Lane A design question (VQ-24). |

**Suggested fix order:** D-01 owner accepts rumor-tier play vs waits for Floor Encounters deep docs → D-03 ingest T1–5 tables → D-02 Ch XII reconciliation → D-04 penalty table if desired.

---

## 6. Content still draft

| ID | Vulnerability | Severity | Owner? | Notes |
|----|---------------|----------|--------|-------|
| X-01 | **Oracle Mysteries:** **8 / 10** draft (`draftMysteryRevelations()` — Battle, Bones, Cataclysm, Dream, Flame, Life, Stars, Time). **Canon:** Ancestor, Shadow | Playtest risk | **Y** | promote individually only after author review. |
| X-02 | **Oracle Curses:** **9 / 10** draft. **Canon:** Spiral-Touched only | Playtest risk | **Y** | Full playable trees exist; tone/mechanics unapproved. |
| X-03 | **Paladin Oaths:** **9 / 10** `draft: true` including **Mercy** (rulebook prose exists; **not promoted** in data). **Canon:** Grief only | Playtest risk | **Y** | Doc drift cleared 2026-07-30 — data still draft. |
| X-04 | **`class-draft-levels.js`** — all **17 classes** L11–20 milestones flagged draft pending rulebook cross-check | Playtest risk | N | Full coverage shipped; promotion is author/owner review. |
| X-05 | **Prestige (`prestige-lorebook.json`):** **18 / 18** `draftCapstone: true`; multiple `draftHallmarkIndices` | Playtest risk | Y | Paths wired; capstones/hallmarks need owner tone + mechanics pass. |
| X-06 | **Cosmology** First Song blob — chapter nav IX–XII incomplete | Polish | N | XIV gate bosses superseded by Dungeon Guide. |

**Suggested fix order:** X-03 Mercy + high-traffic oaths → X-01/X-02 mystery/curse batches → X-04 L11–20 table reconciliation → X-05 prestige capstones → X-06 cosmology split.

---

## 7. Data quality

| ID | Vulnerability | Severity | Owner? | Notes |
|----|---------------|----------|--------|-------|
| Q-01 | **Excel Size/Type/CR scrambled** — `bestiary_metadata_source.xlsx` **mirrors** bad pairings; do not use for metadata fixes | Playtest risk | Y | `huge-at-low-cr`, `tiny-at-high-cr`, etc. heuristics documented. |
| Q-02 | **Umbrin race rename** | — | N | **CLOSED 2026-07-31** — living `rulebook_output.txt` / Player Rulebook `.docx` = **0** whole-word Drow; companion + migration use Umbrin. Legacy saves still migrate. |
| Q-03 | **Generic SRD labels** remain (Owlbear, Behir, etc.) — out of scope per `BESTIARY_SCRUB_LOG.md` | Polish | Y | Owner decides full de-brand pass. |
| Q-04 | **Feats:** 336 live vs 330-title doc; placeholder descriptions; `additional-feats.js` / root `game-data.js` legacy unwired | Playtest risk | N | Reconciliation needed before feat-heavy builds. |
| Q-05 | **Provenance labels** inconsistent — some docs still call multiclass merge “draft” though **Hybrid-B promoted 2026-07-30** | Polish | N | Continuity cleanup in progress; data is canon. |

**Suggested fix order:** Q-01 Bestiary metadata QA workbook → Q-04 feats reconciliation → Q-03 optional SRD pass → Q-05 doc sweep.

---

## 8. Tooling / continuity

| ID | Vulnerability | Severity | Owner? | Notes |
|----|---------------|----------|--------|-------|
| T-01 | **No reproducible balance harness** beyond narrow sim (`combat-balance-sim.mjs`) — no full L1/L3/L5/L8/L10 suite | Blocks finalize | N | Partial CR 1/3/10 bands added; expand per `BALANCE_REPORT.md` P0. |
| T-02 | **Global header search** non-functional (tab focus only) | Polish | N | `Header.tsx` placeholder. |
| T-03 | **Session wild-shape tracker** stub — uses/CR/forms partial; not full encounter enforcement | Playtest risk | N | VQ-22 partial ship. |
| T-04 | **No structured effect schema** for class features — caps and sim cannot enforce | Blocks finalize | N | Tied to C-06. |
| T-05 | **CONTINUITY_REPORT / vague queue** report P0=P1=0 for terminology — **balance finalize blockers live elsewhere** (this doc) | — | N | Do not confuse continuity green with ruleset locked. |
| T-06 | **Director OK gate** — draft data must not ship as canon without promotion | Playtest risk | N | Process guardrail; relies on draft badges (mostly wired). |

**Suggested fix order:** T-04 effect schema → T-01 benchmark suite → T-03 wild-shape completion → T-02 search index → T-05 keep balance docs linked from handoff.

---

## Finalize roadmap (P0 → P2)

Target: **“Ruleset locked for playtest”** — meaning confirmed sources, labeled drafts, bounded high-ceiling kits, and one reproducible encounter→XP→level loop (even if manual).

### P0 — Stop false canon (must complete before “locked” claim)

1. **Opening XP:** milestone-only is official; treat draft CR→XP as optional only (`XP_ADVANCEMENT_CANON.md`).
2. **Owner ratifies class ceiling caps** (or replaces with authored rules) for Mirrorsage, Oracle, Paladin, Warrior, Dragoon, Tinker.
3. **Owner defines Burnout consequences** and specialization eligibility/floor — wire or explicitly defer to GM fiat with UI labels.
4. **Promote provenance model** everywhere: `confirmed | draft | legacy-unverified` on combat, XP, pools, dungeon seeds.
5. **Structured combat + feature schema** — minimum viable fields for sim and Session (action, recharge, save, damage, duration).
6. **Bestiary metadata QA** — resolve or flag `NeedsReview` rows; freeze 10 gate guardians.

### P1 — Playtest-ready workflows

1. **Session XP ledger with character write-back** after P0-1 approval.
2. **Spell-linked overcast + Burnout enforcement** in Session (not hints alone).
3. **Bounded playtest matrix** — L1/L5/L10 parties vs authored bosses + one trash band; scarce-rest vs frequent-rest days.
4. **Oracle/Paladin promotion batch** — owner picks next 2–3 oaths/mysteries/curses per session; no mass promotion.
5. **T6–10 stance decision** — play on rumor seeds with Draft banners vs gate playtest to T5 only.
6. **Floor encounter cards T1–5** — POI → roster or substitution rules from source docs.

### P2 — Tune and polish after evidence

1. Replace excel-sandbox combat in bulk **only** where benchmark suite shows drift.
2. Recharge sim v2 (action economy, multi-target saves, initiative).
3. Feats compendium reconciliation + skill modifier derivation.
4. Global search, wild-shape CR enforcement, cosmology chapter split.
5. Prestige capstone promotion; L11–20 milestone cross-check vs rulebook tables.
6. Rulebook Umbrin + generic SRD de-brand if owner wants full IP cleanliness.

---

## CONTINUITY_REPORT stamp

**Ruleset vulnerabilities audit — 2026-07-30**

- **Balance verdict unchanged:** L1–L20 XP **thresholds** confirmed; **awards/encounters** not. Bestiary **708/708** have draft AC/HP/combat (**698 excel-sandbox**, **10** guardian-authored). **26** recharge payloads use **draft sim assumptions**.
- **Class caps:** `CLASS_CEILING_CAPS.md` + `class-ceiling-caps.js` — **informational only**; not enforced.
- **Magic:** Burnout stub + unwired specialization; **13** draft RP pool tables for non-core casters.
- **Progression:** Session **Award draft XP** is session-local; **no save write-back**.
- **Dungeon:** T6–T10 **`mapped: false`** — draft seeds only (Quiet Deep / Blackglass / Veyr-Obsid touches).
- **Draft content:** Oracle **8** mysteries + **9** curses draft; Paladin **9** oaths draft (**Mercy** still `draft: true`); prestige **18/18** draft capstones; Shadow Mystery + Grief Oath promoted.
- **Data quality:** Excel metadata garbage outside T1–5 trusted set; Umbrin race rename closed; feats reconciliation open.
- **Continuity P0/P1 terminology queue:** cleared in the current canon pass — **does not** clear balance-finalization blockers listed in this document.
- **No commit** per owner request.

---

*Deliverable for owner ruleset-finalize planning. Update when P0 items close or promotion batches land.*
