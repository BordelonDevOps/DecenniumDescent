# T4 expedition balance watch — EXP-IER-T4-01 (Isles of Eternal Radiance)

**Agent:** Balance Watcher (playtest subdivision)  
**Date:** 2026-07-30  
**Playtest ID:** `EXP-IER-T4-01`  
**Sim status:** **Complete** — [`T4_EXPEDITION_PLAY_REPORT.md`](./T4_EXPEDITION_PLAY_REPORT.md), [`T4_ISSUES_LOG.md`](./T4_ISSUES_LOG.md)  
**Scenario (authored post-sim):** [`T4_EXPEDITION_SCENARIO.md`](./T4_EXPEDITION_SCENARIO.md) · **Roster (authored post-sim):** [`T4_ROSTER.md`](./T4_ROSTER.md)

> **Roster mismatch:** The sim **did not read** `T4_ROSTER.md` (absent at run time). It authored a **gap-fill 3×8 roster** inline: **Sunward Lance** / **Prism Watch** / **Dawn's Anvil** with BGR-01 carryovers (Vesper, Greta, Kethren, Kael) plus stub PCs (Mira, Torin, Selene, etc.). The published roster uses **Dawn Concord / Mirror Guild / Choir Covenant** with different names, levels, and company heal layout. **Balance grades below reflect the sim roster**, not a live run of `T4_ROSTER.md`. Re-run recommended against authored roster before live table.

---

## Executive summary

| Dimension | Post-sim verdict |
|---|---|
| **Overall difficulty** | **B** — Expert-tier T4 validated; deadly patrol pairs and Gor Vekk retreat behave as designed |
| **Damage economy** | Patrol CR 7–10 equivalents **appropriate** for 8-PC L8–L10 companies with long rests; **Flameskull×2** and **Duodrone×2** sit at **deadly EV** and produced near-TPKs |
| **Healing / RP economy** | **Adequate chassis, poor novice spend** — five stabilizations, zero deaths; P1/P2 RP burnout repeated L3 mistakes at L9 scale |
| **Gate-adjacent (Gor Vekk)** | **Fair as manifestation + retreat** — 200 HP effective, R1 *End Architecture* forced tactical withdraw; **unfightable** at listed CR 29 / 400 HP |
| **Camp attrition** | **High impact** — sun-shield depletion, watch failure, heat exhaustion, and burnout materially shaped combats |
| **Outcome** | **Partial success** — camp + 3 vials secured; F36 obelisk probe aborted R3; **106 / 120 h** horn |

**Provisional B− superseded:** Pre-sim roster audit overstated E1 vanguard ogre risk (not fought in sim) and Company B heal gap (sim Beta had Greta Cleric). Post-sim deadly band is **Flameskull / Duodrone pairs**, not company split geometry alone.

---

## 1. Damage / healing / RP economy (actual sim)

### Aggregate chassis (sim roster)

| Metric | Sim value | Notes |
|---|---:|---|
| **Total expedition HP** | **1,492** | Alpha 506 · Beta 400 · Gamma 586 |
| **Weighted AC** | **~17** | Range 14–20 |
| **8-PC company DPR** | **~51** vs AC 17 | `monster-combat.mjs` profile |
| **24-PC raid DPR (boss)** | **~×2.5** scaled | Used at F36 manifestation |
| **0 HP incidents** | **7** (all stabilized) | Vesper ×2, Kael ×1, Kethren, Edda, Torin, Unit Seven |
| **Permanent deaths** | **0** | |

### RP / RC spend (high-signal)

| PC | Pool | End-state pattern | Issue |
|---|---:|---|---|
| Vesper (P1, Bard L9) | 14 RP *(draft)* | Empty by Day 10; illegal Empowered+Widened *Shatter* downgraded | #11, #12 — RP ≠ slots at L9 |
| Greta (P2, Cleric L8) | 14 RP *(canon curve)* | **2 / 14** after *Guardian of Faith* + *Spiritual Weapon* | #13 burnout |
| Kael (P4, Warrior) | — | Action Surge nova; cap card posted | Compliant |
| Selene (Oracle L8) | 5 RC | **Prophetic Ward** on Flameskull ray — 1 hard deny/encounter | Cap followed (#15) |
| Edda (Bard L8) | 12 RP *(draft)* | Twinned *Hold Person* 7 RP; concentration broken | Overcast opacity (#12) |
| Yara (Cleric L10) | 18 RP | *Heal* (6 RP) at burnout line during Duodrone fight | Gamma anchor |

**Healing throughput (felt at table):**

| Source | Key uses | Verdict |
|---|---|---|
| Greta *Healing Word* @ 0 HP | Kethren after Assassin fight (B1) | **Critical save** — P2 positive (#37) |
| Selene RC Ward | Negated Flameskull ray on Edda | **Cap-compliant** prevent death |
| Sera / Holt LoH | Deva + Gor Vekk rear guard | 50%/round cap tracked manually |
| Yara *Heal* | Unit Seven after Duodrone | **Long-rest-tier** spend justified |
| Tri-company triage | 7 manual death-save tracks | No Session automation (#47) |

**Cross-company damage incidents:**

| Event | HP impact | Balance note |
|---|---|---|
| Vesper *Faerie Fire* → Joss (AB1) | **12** radiant friendly | Mirror Reef POI + scout gap = systemic (#21) |
| Gor Vekk *End Architecture* R1 | **~120** aggregate (8 fails) | Area save at raid scale — **retreat mandatory** (#10) |
| Sunlight (no vial) | Disadvantage on Vesper, Kethren, Edda | **Ongoing DPR tax** — 4 vials left Day 10 (#23) |

---

## 2. Experience personas — thrived / suffered (sim)

| Persona | PC / company | Verdict | Evidence |
|---|---|---|---|
| **P4 Optimizer** | Kael, Alpha | **Thrived** | Action Surge delete Knight; mutation cap card; pre-read Gor Vekk EV "retreat or wipe" (#43–45) |
| **P3 PF veteran** | Kethren, Beta | **Thrived** | Flurry pacing B1; Webstep ceiling AB1; 8-PC turn spreadsheet (#38) |
| **P2 Casual 5e** | Greta, Beta | **Mixed** | Correct 0 HP heal chain; burnout from 5e "slot spam" (*Guardian* + *Spiritual Weapon*) (#34–35) |
| **P1 Novice** | Vesper, Alpha | **Suffered** | 14 RP = "14 spells"; wrong-target Quickened *Healing Word*; sunlight + watch lapses; loot dispute (#29–33) |
| **Commanders** | Sera, Mira, Dren | **Thrived** | Horn whistle stopped Mirror Reef wipe; retreat call at F36 |
| **Glass casters** | Tamsin, Mira, Edda | **Suffered** | 40–48 HP pools; Edda 0 HP Flameskull; Vesper 0 HP ×2 |
| **Gamma reserve** | Dren, Holt, Yara | **Thrived under fire** | Absorbed Gor Vekk R1; Duodrone fight 53% loss then long rest |

**Persona takeaway:** Table skill **compressed EV** on Alpha (A1 **18%** loss vs **31%** EV) via nova + LoH. **Beta without optimizer frontline** took the expedition's worst fight (B2 **45%**, three sequential downs). Novice RP mistakes **scale with level** — L9 Bard pool did not fix L3 confusion.

---

## 3. Encounter fairness (including Gor Vekk retreat)

### Company patrol fights (E1–E7 equivalent)

| Fight | Company | Foes | EV loss | Actual loss | Fairness |
|---|---|---|---:|---:|---|
| B1 | Beta | Assassin CR 8 | 9% | ~10% | **Fair** — watch-fail tax |
| A1 | Alpha | Knight×2 + Allip | 31% | ~18% | **Fair (easy side)** — Kael nova |
| B2 | Beta | Flameskull×2 | 53% | **45%** | **Deadly — fair for tier**; near-TPK (#49) |
| G1 | Gamma | Duodrone×2 | 71% | **53%** | **Hard — fair** with long rest after |
| AB1 | Alpha+Beta | Cloaker×2 | 53%/co. | ~40% + FF | **Hard**; friendly fire adds variance |
| AG1 | Alpha+Gamma | Deva×1 | 14% | ~13% | **Fair**; mis-ID narrative |
| B3 | Beta | Berbalang×1 | 18% | ~15% | **Fair** |

**Non-boss verdict:** T4 patrol pairs at CR 7–10 equivalents are **correctly deadly** for 8-PC L8–L10 without inter-fight long rest. Scenario must **space havens** after Flameskull/Duodrone bands (#49). Excel-sandbox names (*Aberrant Lash* on Deva) do not affect math (#6).

### Gate-adjacent — Gor Vekk manifestation (F36)

| Parameter | Sim ruling | Fairness |
|---|---|---|
| **HP** | **200 effective** (50% phantom of 400 listed) | **Fair** for probe — not a kill quest |
| **Win condition** | 3-round ritual timer + **tactical retreat** | **Correct** — partial success path |
| **R1 *End Architecture*** | Recharge 6; **8 / 24 fail** DC 21; ~120 HP raid-wide | **Fair spike** if retreat SOP exists; **lethal** without it |
| **R2–R3** | Dren Brutality Threshold; Pax + Holt burst; **200 → 90 HP** | Shows damage **can** answer manifestation |
| **R3 timer** | Obelisk blinding radiance — **fail-forward** | Avoids TPK while denying full win |
| **XP** | **½ listed** (67,500 ÷ 24 = **2,812 each**) | Reasonable for drive-off (#28) |
| **Listed CR 29 / 400 HP** | Not used for melee to completion | **Unfightable** — retreat mandatory (#4, #50) |

**Gor Vekk retreat verdict:** **Fair and well-designed** at manifestation tuning. Full gate boss row is **mis-tiered** for T4 Expert band — sim correctly **did not** attempt kill. Issue #10: EV modeled single-target; table ruled **full-raid save** — actual R1 worse than EV, reinforcing retreat.

---

## 4. Camp attrition impact

| System | Sim outcome | Balance impact |
|---|---|---|
| **Sun-shield vials** | 12 issued → **4 left** Day 10 | Umbrin/disadvantaged DPR tax on Vesper, Kethren (#23) |
| **Heat fatigue** | 1 exhaustion after 8 h exposure (narrative) | Edda, Vesper — compounded sunlight (#27) |
| **Watch Night 1** | Beta asleep → Assassin surprise Greta | **+42 HP** company cost; policy fix Night 2 (#20) |
| **Watch Night 3** | Vesper + Edda left early | Covered by Torin — gap risk |
| **Long rests** | **3** (+24 h horn) | Required after G1 Duodrone; spacing validated |
| **RP burnout** | Greta 2/14; Vesper empty Day 10 | **Post-fight power cliff** — not modeled in EV (#13) |
| **Morale** | Alpha −1 until long rest (Umbrin daylight push) | Narrative pressure on composition |
| **Horn final** | **106 / 120 h** | **14 h buffer** — tight but not blown |
| **Rations / forage** | Not stress-tested to failure | Supply gap in Session (#23) |

**Attrition verdict:** Camp layer **materially changed combat outcomes** — not cosmetic. Sun-shield + watch failures belong in **`T4_EXPEDITION_SCENARIO.md`** supply tables (#1, #7).

---

## 5. Recommendations

### Encounter / tuning (validated)

| Priority | Action | Rationale |
|---|---|---|
| **P0** | Publish **Gor Vekk manifestation** stat block separate from CR 29 gate boss | Sim + issues #4 — retreat path works at 200 HP |
| **P0** | Haven spacing: **mandatory long rest** after Flameskull/Duodrone pairs | #49 — deadly EV confirmed |
| **P1** | Mirror Reef: **friendly-fire** briefing or POI rule (illusion delay before AoE) | #21 — 12 HP + near-wipe tension |
| **P1** | Re-run sim against **authored `T4_ROSTER.md`** | Company heal layout differs from gap-fill |
| **P2** | Alpha patrol tuning optional | A1 easier than EV — acceptable nova reward |

### Economy / class

| Target | Fix |
|---|---|
| L9 Bard (Vesper) | Pre-brief **circle × 2 RP** + overcast stack chart (#11–12) |
| Cleric burnout | Retune planner across multi-fight days (#19) |
| Draft XP ~6,040 mean / PC | Verify vs `draftEncounterBudget()` before canon (#50) |
| ½ boss XP on retreat | Add rules text for drive-off awards (#28) |

### Doc / tooling

| Item | Fix |
|---|---|
| `T4_EXPEDITION_SCENARIO.md` | Wire sun-shield, watch template (#1, #7) |
| Session | 8 / 16 / 24 XP split helper (#26); supply counter (#23) |
| Bestiary | Scrub Radiant Isles sandbox attack names (#6) |
| Gor Vekk row | Fix Floor 90 description (#5) |

---

## 6. Final grade

| Criterion | Grade | Post-sim evidence |
|---|---|---|
| **Patrol encounter curve** | **B+** | EV matched Flameskull near-TPK and Duodrone hard fight; easier wins on Alpha nova acceptable |
| **Gate-adjacent (Gor Vekk)** | **A−** | Manifestation + retreat + half XP — correct tier gate; full stats appropriately excluded |
| **Healing / RP economy** | **C+** | Chassis saved 7 downs; novice/draft pool misuse caused burnout — player error + doc gap |
| **Camp attrition** | **B** | Sun-shield, watches, heat changed fights; not fully wired in Session |
| **24-PC / multi-company** | **C** | Friendly fire, initiative latency, command gap — ops friction not math failure |
| **Rules verifiability** | **Incomplete** | [`BALANCE_REPORT.md`](../mechanics/BALANCE_REPORT.md) blockers remain; excel-sandbox combat |

### **Overall expedition difficulty: B**

**One-line:** T4 tri-company playtest delivers **Expert-tier pressure with correct deadly spikes**, a **fair Gor Vekk retreat** instead of a bogus boss kill, and **partial success** at 106/120 h — held back from A by novice RP scaling, camp systems not in Session, and sim roster ≠ authored roster.

**vs provisional B−:** Pre-sim over-weighted hypothetical E1 ogre split and Mirror Guild heal gap. Sim shows **real bottleneck is patrol pair EV (Flameskull, Duodrone)** and **Gor Vekk R1 area save**, both handled by rests + retreat SOP.

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Balance Watcher — T4 expedition (EXP-IER-T4-01) |
| **Date** | 2026-07-30 |
| **Sim status** | **Complete** |
| **Deliverable** | `docs/playtest/T4_WATCH_BALANCE.md` (post-sim overwrite) |
| **Inputs read** | [`T4_EXPEDITION_PLAY_REPORT.md`](./T4_EXPEDITION_PLAY_REPORT.md), [`T4_ISSUES_LOG.md`](./T4_ISSUES_LOG.md), [`T4_EXPEDITION_SCENARIO.md`](./T4_EXPEDITION_SCENARIO.md), [`T4_ROSTER.md`](./T4_ROSTER.md), [`BALANCE_REPORT.md`](../mechanics/BALANCE_REPORT.md), [`CLASS_CEILING_CAPS.md`](../mechanics/CLASS_CEILING_CAPS.md), [`RACE_CLASS_SYNERGY_REPORT.md`](../mechanics/RACE_CLASS_SYNERGY_REPORT.md) |
| **Roster caveat** | Sim used **Sunward Lance / Prism Watch / Dawn's Anvil** gap-fill; not live **`T4_ROSTER.md`** |
| **Final grade** | **B** (supersedes provisional **B−**) |
| **Git** | No commit/push |

**CONTINUITY_REPORT:** Post-sim balance watch confirms T4 patrol math and Gor Vekk manifestation retreat. Re-grade after second sim against authored roster if company composition shifts heal distribution materially.
