# T4 expedition — DM Watcher report (EXP-IER-T4-01)

**Agent:** DM Watcher (playtest subdivision) — **not** the sim runner  
**Date:** 2026-07-30  
**Playtest ID:** `EXP-IER-T4-01` · Isles of Eternal Radiance (T4, floors 31–40)  
**Format:** 3 companies × 8 PCs = **24 seats** · L8–L10 · good/neutral only

**Sim deliverables read:**

| File | Status |
|---|---|
| [`T4_EXPEDITION_PLAY_REPORT.md`](./T4_EXPEDITION_PLAY_REPORT.md) | **Complete** — 10 combats, 12 days, 106/120 h horn, partial success |
| [`T4_ISSUES_LOG.md`](./T4_ISSUES_LOG.md) | **Complete** — 50 numbered issues |
| [`T4_EXPEDITION_SCENARIO.md`](./T4_EXPEDITION_SCENARIO.md) | On disk; **not read by sim** (issues #1) |
| [`T4_ROSTER.md`](./T4_ROSTER.md) | On disk; **not read by sim** (issues #2) |

**Watcher also read:** [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md), [`SESSION_LOOP.md`](../mechanics/SESSION_LOOP.md)

---

## Executive summary

| Question | Post-sim verdict |
|---|---|
| **Rules consistency** | **Partial** — CLASS_CEILING_CAPS enforced (Warrior, Paladin, Mirrorsage, Oracle, Dragoon); Retune/Burnout/death-at-0 in 5e-shaped table calls. **Gaps:** affinity/opposition never logged; RP still “slots” (issues #11, #34); draft vs canon pools unlabeled (#11–12). |
| **Fudge vs RAW** | **Heavy** — excel-sandbox names (#6); Gor Vekk at 200 HP vs CR 29 (#4, #10); Deva fought hostile; narrative Counterspell; boss ½ XP (#28); ad-hoc encounter set vs authored ladder. |
| **Human GM differently?** | **Yes** — squad initiative from Day 1, caster muster before T4, tighter scout spacing; sim’s horn-whistle SOP and F36 **retreat** match good GM practice (#21, #25). |
| **Newcomer / Resonance @ 24 PCs** | **Inadequate** — cheatsheet only (L3 examples); no newcomer guides (#3); briefing delayed to Day 5; 7× manual death saves (#47). |
| **DM-ready grade** | **C−** |

---

## Fallback roster vs architect roster

The sim **did not load** [`T4_ROSTER.md`](./T4_ROSTER.md). It authored an inline **fallback roster** in the play report. The architect roster exists on disk for live play — conclusions below are **valid for T4 tri-company ops** but **not a regression test** of Scenario Architect casting.

| | **Architect** [`T4_ROSTER.md`](./T4_ROSTER.md) | **Fallback (sim)** [`T4_EXPEDITION_PLAY_REPORT.md`](./T4_EXPEDITION_PLAY_REPORT.md) |
|---|---|---|
| **Playtest ID** | `EXP-T4-01` | `EXP-IER-T4-01` |
| **Companies** | Dawn Concord · Mirror Guild · Choir Covenant | Sunward Lance · Prism Watch · Dawn's Anvil |
| **Class coverage** | **17 / 17** canon classes | **~13 / 17** — no Tinker, Shaman, Crimson Agent; Thief×1, Soldier×1 |
| **Personas** | 15 distinct experience tags across 24 seats | 4 anchored (P1 Vesper, P2 Greta, P3 Kethren, P4 Kael); rest unnamed |
| **Umbrin** | C6 Shade Merit (neutral-good exile) | A1 Vesper + B3 Kethren |
| **Oracle** | B8 Sister Null Choir | B4 Selene Thalen |
| **Notable drift** | Widget Gearheart (Tinker L10), Coral Deepcurrent (Shaman), Sera Nightglass (Crimson Agent) | Reused EXP-BGR-01 names (Helga/Greta cousin, Kael, Kethren); **Dren Voss** alt of NPC Commander Rhal-Voss |
| **Sheet depth** | One-line stubs, no Builder exports | Inline HP/AC/RP in play report |

**Watcher impact:** Caps testing (Mirrorsage, Oracle, Dragoon) used fallback seats — still valid. **Class-coverage and persona-friction claims** from the sim **cannot** be transferred to the architect roster without re-run. Issues log items #1–2 remain **process blockers** for repeatability.

---

## 1. Rules consistency

### Applied well (issues log confirms)

| Rule | Evidence | Issue # |
|---|---|---|
| Warrior 1 mutation/round | Kael + Dren logged | #17 |
| Paladin LoH 50%/round, smite cap | Sera, Holt, Torin | #14 |
| Mirrorsage 1 copy release/round | Neme on Duodrone | #16 |
| Oracle hard deny | Selene RC Ward saves Edda (Flameskull) | #15 |
| Dragoon Momentum cap 6 @ L10 | Pax — no overflow | #18 |
| Heal-from-0 ends saves | Greta on Kethren B1 | #37 (positive) |
| Horn 120 h loop | 106 h at extraction; 3 long rests | — |
| Draft XP splits | 8 / 16 / 24-way manual | #26 |

### Inconsistent or skipped

| Rule | Evidence | Issue # |
|---|---|---|
| RP ≠ slots @ L9 | Vesper “14 spells”; Greta “slots” Days 5–7 | #11, #29, #34 |
| Overcast stack math | Vesper illegal Empowered+Widened; Edda costly Twinned *Hold Person* | #12 |
| Affinity / opposition | No cost breakdown on any cast | *(not filed — gap)* |
| Draft vs canon RP pools | Bard/Monk/Paladin draft beside Cleric/Mage canon — not labeled at muster | #11 |
| Retune across multi-fight days | No expedition day planner | #19 |
| Sun-shield / bright light | Narrative supply; Umbrin disadvantaged Day 10 | #23, #31 |
| Death saves | Manual ×7 | #47 |
| Hit Dice on short rest | Missing from Session | #48 |

**Watcher call:** **Informed GMs** can enforce caps and Burnout today. **Resonance teaching at 24 seats failed** — same L3-scale mistakes amplified to L9 (#11, #29).

---

## 2. Fudge vs RAW

| Fudge | Evidence | Issue # |
|---|---|---|
| Excel-sandbox on celestials | Deva *Aberrant Lash* | #6 |
| Gor Vekk CR 29 / 400 HP / 135k XP | Ran 200 HP manifestation; ½ XP on retreat | #4, #10, #28 |
| Gor Vekk Floor 90 prose | Bestiary zone wrong | #5 |
| Deva hostile despite neutral lore | “Fought anyway for sim” | play report |
| Counterspell | Mira vs Flameskull — table allow | play report |
| Encounter set vs authored ladder | Assassin, Flameskull×2, Duodrone×2, Cloaker×2, Deva, Berbalang — not scenario E1–E6 | #1 |
| *End Architecture* area | EV single-target; table ruled full-raid save (8 fails R1) | #10 |
| Raid DPR ×2.5 for 24 PCs | No canon mass-combat formula | play report |
| Heat fatigue / morale | Narrative only | #27 |
| Friendly fire | Vesper *Faerie Fire* on Joss, 12 radiant | #21 |

**Watcher call:** Retreat from Gor Vekk and ½ boss XP show **honest fudge discipline**. Overall fudge load is **high**; strict RAW audit would flag Deva fight, Counterspell, and unread scenario as invalidating ladder regression.

---

## 3. Human GM differences

| Area | Sim | Human GM likely |
|---|---|---|
| **Initiative** | Joint fights 16–24 active; ~2× wall-clock (#24) | Squad phases; ≤8 acting PCs/round from Day 1 |
| **Resonance briefing** | Cheatsheet T3; no shared re-brief until Day 5 | Caster-only muster before T4; L8–10 company RP cards |
| **Scout gap** | Beta 200 ft ahead → FF + delayed whistle (#25) | Tighter formation; no damaging AoE until IDs confirmed |
| **Watch Night 1** | Beta asleep → Assassin crit (#20) | Passive Perception roster or stricter failure table |
| **Flameskull / Duodrone** | Beta 45% HP; Gamma 53% (#49) | Long-rest gate before next push — sim partially rested Gamma |
| **Gor Vekk F36** | 8 fails R1; commanders retreat R3 | Same — no GM runs full CR 29 at this strength |
| **Partial success** | Camp + 3 vials + intel; probe aborted | Aligns with scenario partial-success band |
| **Session @ 24** | Not attempted (#23 in UX table) | Paper HP by company; Session for horn/RP only |

---

## 4. Newcomer doc / Resonance adequacy (24 PCs)

| Asset | Status | Issue # |
|---|---|---|
| [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md) | Used — L3 examples only | #11 |
| `NEWCOMER_GM_GUIDE.md` | Absent | #3 |
| `NEWCOMER_PLAYER_GUIDE.md` | Absent | #3 |
| Company-scoped L8–L10 RP cards | Absent | #11, #19 |
| Oracle RC one-pager | Selene used RC correctly once; triggers untaught | #15 |
| Sun-shield supply card | 12 issued, 4 left Day 10 | #23 |
| Watch rotation template | Missing | #20, issues log #7 |

| Audience | Rating |
|---|---|
| Novices (P1 Vesper) | **Fail** — #29–32 |
| Casual 5e (P2 Greta) | **Partial** — burnout #35; positive heal #37 |
| PF veteran (P3 Kethren) | **Pass** — #38–41 low/medium |
| Optimizer (P4 Kael) | **Pass** — #43–45 positive |
| **24-PC table overall** | **Fail without add-ons** |

---

## 5. Balance & outcome (from sim + issues log)

| Metric | Result |
|---|---|
| Calendar | 12 days surface-to-surface |
| Horn | **106 / 120 h** |
| Outcome | **Partial success** — camp, 3/3 vials, F36 probe → tactical retreat |
| 0 HP incidents | 7 (all stabilized) |
| Near-TPK | Beta vs Flameskull×2 (#49); Gor Vekk R1 save spike |
| Draft XP / PC | ~6,000 mean (~37–47% of one level) — high (#50) |
| EV accuracy | Flameskull, Duodrone, Cloaker EV matched table pain (#49) |

**Encounters not from authored ladder** — balance validates **T4 patrol density for 8-PC companies**, not scenario CR counts (Ogre Ram×6, Cloaker×4, Knight×6, etc.).

---

## 6. Grade: DM-ready

| Dimension | Grade | Notes |
|---|---|---|
| Architect scenario/roster (on disk) | B+ | Unverified by sim (#1–2) |
| Sim combat / balance evidence | B− | Company EV coherent; retreat correct |
| Rules application | C | Caps yes; Resonance teaching no |
| Player / GM documentation | D+ | Cheatsheet only (#3) |
| Mass-table procedure | C− | Horn SOP worked; initiative painful (#24) |
| Process / repeatability | D+ | Fallback roster; 50 issues filed |
| **Overall DM-ready** | **C−** |

**Movement:** Pre-flight **D** → post-sim **C−**.

**Held below C:** Sim used **fallback roster** (not architect 17/17 cast); scenario/roster unread at sim time; Resonance/newcomer gaps; 50 open issues including #20–23 high-severity ops friction.

**To reach B:** Re-run sim on architect roster + scenario; ship L9 company Resonance cards + GM mass-combat SOP; wire sun-shield supply (#23).

**To reach A:** 24 Builder exports; affinity logged every cast; zero slot-language after muster; Session or paper workflow for 24 combatants.

---

## 7. Priority recommendations (from watcher + issues log)

1. **Re-run sim** reading [`T4_EXPEDITION_SCENARIO.md`](./T4_EXPEDITION_SCENARIO.md) + [`T4_ROSTER.md`](./T4_ROSTER.md) — compare encounter set and persona friction to this pass.
2. **Resolve roster split** — document which roster is canonical for live EXP-T4-01 (architect) vs sim baseline (fallback).
3. **`T4_RESONANCE_101.md`** + newcomer guides (#3) — caster muster **before** T4 entry, not Day 5.
4. **Gor Vekk manifestation block** — promote scenario §E6; scrub CR 29 row / Floor 90 prose (#4–5).
5. **Sun-shield + watch templates** in Session scene notes or Items (#20, #23).
6. **Multi-participant XP split** helper — 8 / 16 / 24 (#26).

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | DM Watcher — T4 expedition (EXP-IER-T4-01) |
| **Date** | 2026-07-30 |
| **Verdict** | **Post-sim complete — partial success; DM-ready C−** |
| **Deliverable** | `docs/playtest/T4_WATCH_DM.md` |
| **Sim read** | `T4_EXPEDITION_PLAY_REPORT.md`, `T4_ISSUES_LOG.md` (50 issues) |
| **Roster note** | Sim = fallback (Sunward Lance / Prism Watch / Dawn's Anvil); architect = Dawn Concord / Mirror Guild / Choir Covenant — **not equivalent** |
| **No commit/push** | Per playtest brief |
