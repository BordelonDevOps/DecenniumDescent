# Expedition friction log — EXP-BGR-01

**Date:** 2026-07-30 · **DM Simulator re-run** · **Scenario:** Glassbite Hollow  
**Party:** Vesper Ashwhisper · Helga Stoneprayer · Kethren Quiet-Step · Kael "Meterwatch" Grunn @ L3

---

## Input status

| File | Character | Status |
|---|---|---|
| `P1_NOVICE.md` | Vesper Ashwhisper — Umbrin Cavern Mystic Bard | **Full sheet** — read |
| `P2_CASUAL_5E.md` | Helga Stoneprayer — Mountain Dwarf Cleric | **Full sheet** — read |
| `P3_PF_VETERAN.md` | Kethren Quiet-Step — Umbrin Shadow Blade Monk | **Full sheet** — read |
| `P4_OPTIMIZER.md` | Kael "Meterwatch" Grunn — Swamp Troll Warrior Juggernaut | **Full sheet** — read |

**Prior run error:** DM sim treated these as empty stubs and substituted Mira/Torin/Selene/Kael Venn — corrected in this pass.

---

## P1 — Novice (Vesper Ashwhisper)

| # | Friction | Severity | Table call / outcome |
|---:|---|---|---|
| 1 | Confused **4 max RP (draft)** with **“four spell slots”** | High | DM re-explained; still said “slots” in E2 |
| 2 | **Bardic Inspiration on self** pre-combat — allies never buffed | Medium | Allowed; wasted support value |
| 3 | Burned **2 RP** on *Dissonant Whispers* E1 (thematic) — acceptable but left only 2 RP | Medium | Retune +1 between fights insufficient for big spells |
| 4 | Walked into melee at hollow mouth — **18 HP** took 8 from Chitine drop | High | Novice positioning; agreed order ignored |
| 5 | Did not know **cantrips = 0 RP** until mid-E1 | Medium | *Vicious Mockery* spam after RP spend |
| 6 | **Sunlight Sensitivity** noticed at briefing; forgot during bridge | Low | No attack penalty ruled; Perception disadvantage once on approach |
| 7 | *Healing Word* on **healthy Kethren** E3 R1 (2 RP waste) while she would drop R2 | High | Panic misprioritization per persona |
| 8 | **Death saves** — no Session automation | Medium | Paper tracker; brief 0 HP before Helga bonus |
| 9 | Asked if **Virtuoso vs Discord** matters at L3 | Low | DM: path choice at L3 college only |
| 10 | Shard grab — thought it was **free object interaction** | Low | Contested vs Weaver; failed |

---

## P2 — Casual 5e (Helga Stoneprayer)

| # | Friction | Severity | Table call / outcome |
|---:|---|---|---|
| 1 | Called RP **“slots”** at briefing and after E1 | Medium | Corrected; **7 RP canon** trusted after one fight |
| 2 | Expected **Hit Dice** on short rest for Kael | Medium | **Not in Session UI** — Kael stayed wounded |
| 3 | **Retune ≈ ¼ pool + WIS** — expected full slot recovery | Medium | Got +3 RP; planned across 3 fights |
| 4 | **Life Domain** not in Builder — assumed PHB Life | Medium | Table-assumed; +1 *Cure Wounds* die unused |
| 5 | **Shield of Faith** on Kael E3 instead of **Bless** | Low | Valid 5e choice; lower hit buff than Bless on whole party |
| 6 | **Spiritual Weapon** (4 RP) never cast — Sacred Flame default | Low | Correct resource conservation for 3-fight day |
| 7 | Short rest after E1 wanted despite horn pressure | Low | Allowed; horn +1 h only |
| 8 | **Concentration** broken manually when Kael took 10 damage | Medium | No Session automation |
| 9 | **Forge / Stoneheart %** resist language vs 5e flat resist | Low | Asked once; table: treat as flavor until chart exists |
| 10 | Comfortable after E1 with **Healing Word** bonus-action heal | — | Positive — 5e muscle memory helped |

---

## P3 — PF veteran (Kethren Quiet-Step)

| # | Friction | Severity | Table call / outcome |
|---:|---|---|---|
| 1 | Mapped turns to **3 actions** — satisfied by Move/Action/Bonus | Low | Flurry = bonus; acceptable |
| 2 | **Stance Shift free 1/round** — swapped every round | Low | Used as written; no PF2 stance cost complaint |
| 3 | **Combo Step** stun — asked save DC and **Stunned 1 vs 3** | Medium | DC 13 WIS; duration **1 round** table ruling |
| 4 | **% crit / DR** in Tiger/Tortoise prose — stacking category unclear | Medium | GM applies narratively; sim uses AC/d20 |
| 5 | **Ki Chain** — Flowing Form timing ambiguous | Medium | +1 Ki when alternating move/strike — granted once E1 |
| 6 | **Webstep** ceiling — opportunity attacks? | Medium | **Yes** when leaving reach |
| 7 | Requested **flanking / flat-footed** | Medium | No flanking; Help once on Kael vs Consort |
| 8 | **Encounter XP budget** (PF2) — distrusted 387 draft XP | Medium | Labeled draft; milestone not promised |
| 9 | Over-planned **bridge grid** for single-melee Consort | Low | Persona-accurate over-engineering |
| 10 | **Murkish** at cult vault — flavor win | — | Positive engagement with Umbrin lore |

---

## P4 — Optimizer (Kael "Meterwatch" Grunn)

| # | Friction | Severity | Table call / outcome |
|---:|---|---|---|
| 1 | **No RP pool** — confirmed `NO_POOL_CLASSES` | — | Session row clean |
| 2 | **Action Surge + 1 mutation activation/round** — nova E2/E3 | — | Cap compliant; logged damage |
| 3 | **CLASS_CEILING_CAPS** **applies** (Warrior Juggernaut) | High | 2 prepared actives OK; **1 activation/round** enforced |
| 4 | **Overpressure Response** (free mutate on crit) — not triggered | — | N/A this run |
| 5 | **Regen 5%/2 turns** — tracked ~6 HP over E2+E3 | — | Validated attrition plan |
| 6 | **Second Wind** E2 — +8 HP at 15 HP threshold | — | Matches optimizer brief |
| 7 | Posted **Shadow Weave recharge ~33%** before E3 | — | Party pre-positioned |
| 8 | Missing **arcane nova** — party DPR sim **~17** vs stub Mage spike | Medium | Longer fights; still cleared in round budget |
| 9 | Large **+8% HP** draft on 35 HP — asked if sim includes | Low | Confirmed approximate |
| 10 | Wanted **recharge probability** on bestiary card | Low | Used `rechargeAvailabilityProbability` = 0.33 |

---

## System / rules ambiguities

| Topic | Gap | Table call used |
|---|---|---|
| Retune | No action/time cost | Free during short rest |
| Healing at 0 HP | vs concurrent death saves | 5e heal-from-0 ends saves |
| Bard RP @ L3 | **Draft** hybrid (4 RP) vs Cleric **canon** (7 RP) | Uneven player trust — label draft |
| Monk RP @ L3 | **Draft** minor (2 RP) | Used; barely touched |
| Life Domain | Builder incomplete | Table-assumed PHB Life |
| Monk stance % mods | Not executable in Session | GM narrative |
| Concentration | No automation | Manual tracking |
| Grapple/shove | Not in companion | Not needed this run |
| Sunlight Sensitivity | Fringe lighting | Per-scene DM ruling |
| Shadow Weave | Area vs single-target EV | Full-party WIS save |
| Bestiary names | *Freak Bite* on cultist | Accepted draft placeholder |
| Scenario fail (shard 3 rounds) | Untested | Weaver died before grab |
| Draft XP 387/PC | Not canon | 21.5% of L3→L4 gap |

---

## Balance friction (EV combat math)

**Party:** 101 HP · DPR ~17.6 vs AC 13 · ~16.3 vs AC 14 · incoming vs AC 16

| Encounter | EV party loss | Actual loss | Verdict |
|---|---:|---:|---|
| E1 2× Chitine (104 HP) | **35%** (~35 HP) | ~18 HP (18%) | Easy–moderate with focus fire |
| E2 Consort (68 HP) | **15%** (~15 HP) | ~20 HP on Kael (20%) | Moderate; tank + regen |
| E3 Gloom Weaver (88 HP) | **43%** (~43 HP) | ~45 HP; 2× down | Hard capstone |
| **Aggregate EV** | **~93%** of 101 HP | Win; 2 near-deaths | **Lethal if naive**; viable with heals + nova |

**Recharge:** Gloom Weaver *Shadow Weave* P(recharge) = **33%**; swingy — dropped Vesper and Kethren in one blast.

**Curve:** CR 1×2 → CR 2 → CR 3 appropriate for optimizers; **steep for P1-heavy tables**.

---

## Companion UX (Session)

| Feature | Status this run |
|---|---|
| Death saves | Manual only — used twice |
| RP tracking | Helga 7 RP clear; Vesper 4 RP draft confused P1 |
| Warrior row | No RP column — correct for Kael |
| Hit Dice on short rest | Missing — P2 friction |
| Award draft XP | Not clicked; totals match scenario (1,550 → 387 each) |
| Horn clock | 7/16 h — low pressure |
| Conditions | Free text — Stunned, concentration manual |

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | DM Simulator — **re-run with real player agents** |
| **Date** | 2026-07-30 |
| **Supersedes** | Prior friction log (stub party Mira/Torin/Selene/Kael Venn) |
| **Deliverable** | `EXPEDITION_FRICTION_LOG.md` |
| **No commit/push** | Per playtest brief |
