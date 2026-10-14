# T4 expedition issues log — EXP-IER-T4-01

**Date:** 2026-07-30 · **Agent:** Expedition Simulator  
**Scenario:** Isles of Eternal Radiance · T4 tri-company (24 PCs)  
**Deliverable pair:** [`T4_EXPEDITION_PLAY_REPORT.md`](./T4_EXPEDITION_PLAY_REPORT.md)

---

## Missing inputs (blocking for live table)

| # | Issue | Severity | Recommendation |
|---:|---|---|---|
| 1 | **`T4_EXPEDITION_SCENARIO.md` absent** | High | Author scenario with goals, fail conditions, supply table, boss probe rules |
| 2 | **`T4_ROSTER.md` absent** | High | Publish 24 PC stubs or chargen slots; sim used inline minimal roster |
| 3 | **`NEWCOMER_GM_GUIDE.md` / `NEWCOMER_PLAYER_GUIDE.md` absent** | Medium | Needed for multi-company Resonance briefing at T4 scale |
| 4 | **Gor Vekk CR 29 on T4 gate** | High | Bestiary lists CR 29 / 135k XP / 400 HP — mismatches tier 4 "Expert" band; add **manifestation** stat block or retune gate boss row |
| 5 | **Gor Vekk description cites Floor 90** | Medium | `bestiary_data_full.json` prose wrong zone; continuity scrub |

---

## Bestiary / combat data

| # | Issue | Severity | Evidence |
|---:|---|---|---|
| 6 | **Excel-sandbox attack names on celestials** | Medium | Deva uses *Aberrant Lash* / *Tail Lash* — breaks Radiant Isles tone |
| 7 | **`combat` object lacks AC/HP** | Low | Sim uses top-level `armorClass` / `hitPoints`; helper defaults mislead if only `combat` read |
| 8 | **CR field naming** | Low | `challengeRating` string vs `cr` — CR undefined in quick node queries |
| 9 | **Giant Fire Beetle XP 41,000** | High | Radiant Isles row likely ingest error — not used this run |
| 10 | **Recharge area saves** | Medium | *End Architecture* modeled single-target in EV; table ruled full-raid save (8 fails R1) |

---

## Resonance & class caps

| # | Issue | Severity | Persona / PC |
|---:|---|---|---|
| 11 | **RP pool ≠ slots at L9 scale** | High | P1 Vesper — repeated L3 mistake with 14 RP |
| 12 | **Overcast stack math opaque mid-fight** | High | Vesper Empowered+Widened *Shatter* illegal; Edda Twinned *Hold Person* costly |
| 13 | **Burnout badge without auto-penalty** | Medium | Greta at 2/14 RP — GM applied disadvantage manually |
| 14 | **Paladin LoH 50%/round cap** | Low | Sera tracked correctly; no Session automation |
| 15 | **Oracle hard deny cap** | Low | Selene RC Ward on Edda — `CLASS_CEILING_CAPS.md` followed |
| 16 | **Mirrorsage 1 copy release/round** | Low | Neme compliant during Duodrone fight |
| 17 | **Warrior 1 mutation activation/round** | Low | Kael + Dren both logged caps |
| 18 | **Dragoon Momentum cap 6 @ L10** | Low | Pax — no overflow complaint |
| 19 | **Retune scheduling across 3 fights/day** | Medium | No companion "expedition day planner" |

---

## Multi-company expedition ops

| # | Issue | Severity | Outcome |
|---:|---|---|---|
| 20 | **Watch rotation failure Night 1** | High | Beta asleep → Assassin surprise on Greta |
| 21 | **Friendly fire at Mirror Reef** | High | Vesper *Faerie Fire* hit ally Joss (12 radiant) |
| 22 | **Loot dispute Blessed Essence (T2)** | Medium | Commander split rule — no Items tab escrow |
| 23 | **Sun-shield vial supply not wired** | High | 12 issued, 4 left Day 10; Umbrin disadvantage |
| 24 | **3-company initiative latency** | Medium | Joint fights ~2× single-party duration |
| 25 | **Command SOP "200 ft scout gap"** | Medium | Too far at Mirror Reef — delayed horn whistle |
| 26 | **Cross-company XP split** | Low | 16-way and 24-way splits manual; Session awards per-foe only |
| 27 | **Morale / exhaustion from heat** | Medium | Narrative only — no Session condition for heat fatigue |
| 28 | **Partial boss XP (½ on retreat)** | Medium | No rules text for drive-off awards vs kill |

---

## Persona friction (by playtest agent)

### P1 — Novice (Vesper Ashwhisper, Alpha L9)

| # | Friction | Severity |
|---:|---|---|
| 29 | 14 RP treated as "14 spells" entire expedition | High |
| 30 | Wrong-target *Healing Word* (Quickened) vs Deva | High |
| 31 | Sunlight Sensitivity forgotten without vial | Medium |
| 32 | Left watch early Night 3 with Edda | Medium |
| 33 | "Found" loot trigger for dispute | Low |

### P2 — Casual 5e (Greta Stoneprayer, Beta L8)

| # | Friction | Severity |
|---:|---|---|
| 34 | RP called "slots" Days 5–7 | Medium |
| 35 | Burnout after *Guardian of Faith* + *Spiritual Weapon* | Medium |
| 36 | *Revivify* component anxiety (not used) | Low |
| 37 | Correct 0 HP *Healing Word* on Kethren B1 | — (positive) |

### P3 — PF veteran (Kethren Quiet-Step, Beta L8)

| # | Friction | Severity |
|---:|---|---|
| 38 | 8-PC company turn spreadsheet | Low |
| 39 | Stun DC 13 — asked degrees of success | Medium |
| 40 | Webstep + opportunity attacks | Medium |
| 41 | No flanking rule — Help once | Medium |
| 42 | Murkish/Radiant lore color wanted | Low |

### P4 — Optimizer (Kael Grunn, Alpha L9)

| # | Friction | Severity |
|---:|---|---|
| 43 | Action Surge + mutation cap logged | — (positive) |
| 44 | Posted Shadow Weave / recharge odds for boss | — (positive) |
| 45 | Gor Vekk EV "retreat or wipe" pre-read | — (positive) |
| 46 | Missing unified party DPR dashboard for 24 PCs | Low |

---

## Companion UX (Session tab)

| Feature | Status this run | Issue # |
|---|---|---|
| Horn clock 106/120 h | Manual +8 long rests | — |
| 24-PC initiative | Not attempted in Session | 23 |
| Death saves | Manual ×7 | 47 |
| Hit Dice on short rest | Missing | 48 |
| Sun-shield / supply counters | Missing | 23 |
| Multi-company camp watch template | Missing | 20 |
| Award draft XP | Per-foe; no 16/24 split helper | 26 |
| Conditions (heat fatigue, Sunlight) | Free text only | 27 |
| Friendly-fire flag | None | 21 |

---

## Balance findings (EV vs table)

| Encounter | EV loss (8-PC) | Actual | Verdict |
|---|---:|---:|---|
| Assassin | 9% | ~10% | OK |
| Knight×2 + Allip | 31% | ~18% | Easier (nova) |
| Flameskull×2 | 53% | ~45% | **Near-TPK** — EV accurate |
| Duodrone×2 | 71% | ~53% | Hard — long rest warranted |
| Cloaker×2 | 53% | ~40% + FF | Hard |
| Deva | 14% | ~13% | OK |
| Berbalang | 18% | ~15% | OK |
| Gor Vekk manifestation | 100%+ | Retreat R3 | **Unfightable at CR 29 stats** |

**Issue 49:** T4 patrol pairs (Duodrone, Flameskull) sit at **deadly** EV for 8-PC L8–9 without long rest between — intentional for tier, but needs haven spacing in scenario doc.

**Issue 50:** Aggregate expedition awards **~6,000 draft XP/PC** (~37–47% of one level) — high for 12 days; verify against `draftEncounterBudget()` bands before canonizing.

---

## Priority fix queue

1. Author **`T4_EXPEDITION_SCENARIO.md`** + **`T4_ROSTER.md`**
2. Retune or split **Gor Vekk** (manifestation vs gate boss)
3. Wire **supply / sun-shield** tracker or Items handoff
4. Scrub **sandbox attack names** on Radiant Isles zone foes
5. **Multi-PC XP split** helper (8 / 16 / 24 participants)
6. **Newcomer guides** for multi-company Resonance + sunlight
7. **Watch rotation** camp mini-game or checklist in Session scene notes template

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Expedition Simulator |
| **Date** | 2026-07-30 |
| **Playtest ID** | EXP-IER-T4-01 |
| **Deliverable** | `T4_ISSUES_LOG.md` |
| **Issues filed** | 50 numbered |
| **No commit/push** | Per playtest brief |
