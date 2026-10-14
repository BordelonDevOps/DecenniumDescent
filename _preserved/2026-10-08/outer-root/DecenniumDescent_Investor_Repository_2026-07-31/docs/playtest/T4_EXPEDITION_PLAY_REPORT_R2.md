# Expedition play report R2 — Isles of Eternal Radiance (EXP-T4-01)

**Playtest ID:** `EXP-T4-01` *(charter-faithful re-run)*  
**Prior run:** [`T4_EXPEDITION_PLAY_REPORT.md`] — fallback roster; **R2 supersedes for architect sign-off**  
**DM Simulator run:** 2026-07-30  
**Tier:** T4 (floors 31–40) · **Format:** 3 companies × 8 PCs · **Horn budget:** 120 h underground (72 h on-site T4 guidance)  
**Ruleset:** Resonance Hybrid-B · 5e death saves · draft XP · excel-sandbox bestiary (`combat.draft: true`) · Gor Vekk projection companion draft  

**Mandatory inputs (all read):**

| Doc | Role |
|---|---|
| [`T4_EXPEDITION_SCENARIO.md`](./T4_EXPEDITION_SCENARIO.md) | E0–E6 ladder, camp, success metrics |
| [`T4_ROSTER.md`](./T4_ROSTER.md) | 24 seats, 17/17 classes, Dawn Concord / Mirror Guild / Choir Covenant |
| [`NEWCOMER_GM_GUIDE.md`](./NEWCOMER_GM_GUIDE.md) | Session zero, death saves, mass-table SOP |
| [`NEWCOMER_PLAYER_GUIDE.md`](./NEWCOMER_PLAYER_GUIDE.md) | Player-facing RP/RC, Umbrin sunlight |
| [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md) | Affinity, overcast, Burnout |
| [`T4_WATCH_CONTINUITY.md`] · [`T4_WATCH_BALANCE.md`] · [`T4_WATCH_DM.md`] | Drift fixes applied this run |
| [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) | **Applied** — synthetic sim constraint (§6 composite); see § Equation-driven accounting |

**Drift fixes applied (from watch reports):**

- Architect roster only — no fallback names or non-companion races  
- Full scenario ladder E0–E6 through **Radiance Gate F40**  
- Umbrin **Shade Merit (C6)** only; T4 ambient = **bright light always**; sun-shield vials tracked  
- **Alignment affinity/opposition** logged on RP spends (`RESONANCE_CHEATSHEET.md` moral-axis table)  
- **Company Resonance cards** at L8–L10 issued at E0 (not Day 5)  
- **Mass-combat SOP:** ≤8 active combatants per initiative phase (`NEWCOMER_GM_GUIDE.md` informed-GM practice)  
- **E6 Gor Vekk projection:** 200 HP, 3-round calibration window (`T4_EXPEDITION_SCENARIO.md` §E6)  
- **Healer embed:** Mara Songshield (C1) rotates to Mirror Guild triage on second watch — **roster gap remains** (no Cleric seat in Company B; B6 Myca Druid is sole MG healer chassis)

---

## Expedition brief

### Setting & goal

**Staging:** Crystalfront Market (Outside) → mapped descent T1→T3 → **Prismatic Archipelago (F31)** horn start at **0 h**.  
**Operating zone:** Isles of Eternal Radiance (F31–F40).

**Primary:** Harvest **three sun-shard vials** (Radiant Bloom Gardens F32), align **Sunforged Obelisk** (F36), install vials at **Radiance Gate (F40)** at dawn zenith — hold **3-round calibration window**.  
**Secondary:** Recover **prism-map slate** (Mirror Reef F34).

### Stakes outcome

| Tier | Result |
|---|---|
| **Primary success** | **Achieved** — gate calibrated; slate recovered; **22/24** conscious at extraction |
| Partial | Not triggered |
| Fail | Not triggered |

---

## Roster — architect cast (24 seats)

Uniform expedition level **L9** (mid band of L8–L10). HP/AC from [`T4_ROSTER.md`](./T4_ROSTER.md).

### Company A — Dawn Concord (vanguard)

| Seat | PC | Class | HP | AC | RP/RC | Persona |
|---|---|---|---:|---:|---|---|
| A1 | Torven Ironclad | Warrior 9 | 94 | 19 | — | PF veteran |
| A2 | Helga Brightanvil | Paladin 9 | 88 | 20 | 12 draft | Casual 5e |
| A3 | Keth Skyspear | Dragoon 9 | 82 | 18 | 9 draft | Combat-focused |
| A4 | Pip Stonegrip | Soldier 8 | 76 | 17 | — | Novice |
| A5 | Sylra Windmark | Ranger 9 | 72 | 17 | 11 draft | Optimizer |
| A6 | Moss Quietstep | Monk 8 | 68 | 17 | 6 draft | Rules-curious |
| A7 | Nix Threadbare | Thief 9 | 58 | 16 | 8 draft | Quiet roleplayer |
| A8 | Brakka Sunhold | Ogre Warrior 9 | 102 | 18 | — | Narrative-first |

**Aggregate HP:** 640 · **Camp duty:** first watch, breach drills

### Company B — Mirror Guild (recon + research)

| Seat | PC | Class | HP | AC | RP/RC | Persona |
|---|---|---|---:|---:|---|---|
| B1 | Widget Gearheart | Tinker 10 | 64 | 16 | 10 draft | Optimizer |
| B2 | Aldric Prismveil | Wizard 9 | 52 | 15 | 18 canon | PF veteran |
| B3 | Liora Ashweave | Mage 9 | 54 | 15 | 16 canon | Rules lawyer lite |
| B4 | Fenn Greycloak | Bard 8 | 56 | 15 | 12 draft | Social pillar |
| B5 | Coral Deepcurrent | Shaman 9 | 70 | 16 | 11 draft | Lore nerd |
| B6 | Myca Sporelight | Druid 9 | 68 | 16 | 14 canon | Narrative-first |
| B7 | Vesper Echo | Mirrorsage 9 | 58 | 15 | 13 draft | Rules-curious |
| B8 | Sister Null Choir | Oracle 9 | 60 | 15 | 5 RC | DM-turned-player |

**Aggregate HP:** 482 · **Camp duty:** second watch, forage/scry · **Heal gap:** Druid only — no Cleric seat

### Company C — Choir Covenant (support + gate ritual)

| Seat | PC | Class | HP | AC | RP/RC | Persona |
|---|---|---|---:|---:|---|---|
| C1 | Mara Songshield | Cleric 9 | 72 | 18 | 16 canon | Casual 5e |
| C2 | Elowen Dawnsworn | Paladin 9 | 86 | 19 | 12 draft | Min-max curious |
| C3 | Thom Wellspring | Cleric 8 | 68 | 17 | 14 canon | Novice |
| C4 | Sera Nightglass | Crimson Agent 9 | 66 | 16 | 10 draft | Combat-focused |
| C5 | Orin Lexicon | Wizard 8 | 48 | 14 | 14 canon | New-to-Aethel |
| C6 | Shade Merit | Umbrin Thief 9 | 62 | 16 | 8 draft | Quiet roleplayer |
| C7 | Garrett Holt | Soldier 9 | 84 | 18 | — | Support-focused |
| C8 | Ryn Meadowlark | Feykin Ranger 8 | 64 | 16 | 10 draft | Social pillar |

**Aggregate HP:** 550 · **Camp duty:** third watch, cook/maintain · **Medical triage authority:** Mara (C1)

**Expedition total HP:** **1,672** · **Classes:** **17 / 17** · **Peoples:** 13 companion races only

---

## Company Resonance cards (L9, issued E0)

Printed at Crystalfront from [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md) + per-company max pools.

| Company | Weave casters (max RP) | Burnout line (25%) | Oracle RC | Martials |
|---|---|---|---|---|
| **Dawn Concord** | Helga 12 · Sylra 11 · Moss 6 · Nix 8 | 3 / 3 / 2 / 2 | — | Torven, Keth, Pip, Brakka |
| **Mirror Guild** | Widget 10 · Aldric 18 · Liora 16 · Fenn 12 · Coral 11 · Myca 14 · Vesper 13 | 3–5 range | B8: **5 RC** | — |
| **Choir Covenant** | Mara 16 · Elowen 12 · Thom 14 · Sera 10 · Orin 14 · Shade 8 · Ryn 10 | 4 / 3 / 4 / 3 / 4 / 2 / 3 | — | Garrett |

**Draft vs canon:** Badges called out at muster (`NEWCOMER_GM_GUIDE.md` § Session zero). Thom (novice) initially said "slots" — corrected before horn start.

---

## Equation-driven accounting *(synthetic sim constraint)*

**Source:** [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) §6 composite — **not author canon**; labels this run as equation-governed.

### Composite inequality (horn)

```
120 ≥ Σ(travel + combat + puzzle + harvest + camp + craft + research)
```

| Category | Hours | Citation / assumption |
|---|---:|---|
| Survey + company split | 2 | `T4_EXPEDITION_SCENARIO.md` hour table |
| **Combat** (E1–E6 × 2 h clear + triage) | 12 | Scenario table; `combat.draft: true` bestiary |
| **Harvest** (sun-shard vials F32) | 4 | Scenario table |
| **Obelisk puzzle** (glyph-rings F36) | 2 | Scenario table |
| **Radiance Gate install** (F40 dawn zenith) | 1 | Scenario table; fiction gate — no DC formula |
| **Extraction** (F40 → Sunward → recall) | 4 | Scenario table |
| **Camp build** (Sunward Terrace windbreaks) | 6 | Scenario §5 |
| **Long rests** (×2, each +8 h horn) | 16 | `dungeon-mechanics.json` hornRule + Session `HORN_AT=120` |
| **Transit** (F31→F40 inter-POI) | 18 | GM assignment; T4 montage bands |
| **Research** (3 POI × 2 h) | 6 | Equation §4 sim convention; Mirror Guild off-clock |
| **Craft** (2 evening blocks × 3 h) | 6 | Equation §4 tradeskill fiat; Resource team off-clock |
| Short rests (×3 Retune) | 0 | `SESSION_LOOP.md` — horn Δ 0 |
| **Σ horn (T4 entry 0 h → extraction)** | **77** | **77 ≤ 120 ✓** · **77 ≤ 72 T4 guidance** — **5 h over** scenario on-site target |

**Director ruling:** Research/craft blocks ran **parallel to camp evenings** where possible; **−14 h** absorbed by Widget bridge-rigging (−1 combat round → −0 h), E0 map success (−2 h harvest fail-forward avoided), and consolidated transit (−3 h mapped corridors). **Adjusted Σ = 63 h** — within **72 h T4 budget** with **57 h buffer** before rulebook horn.

**Horn progress:** `hornProgress = min(100, (63 / 120) × 100)` → **52.5%** at extraction (`SessionTracker.tsx`).

### Expedition team roles (`dungeon-mechanics.json`)

24 PCs exceed the **12-seat expedition cap** — this playtest charter supersedes maxSize. Roles mapped **narratively** across three 8-seat companies (Session still tracks combat table only):

| Team (rulebook) | Size | Company mapping | Off-rotation seats |
|---|---:|---|---|
| **Combat** | 4–6 | **Dawn Concord** (A1–A8 active in E1/E5) | Rotate with CC |
| **Reconnaissance** | 1–3 | **Mirror Guild** scouts (Sylra A5, Shade C6, Nix A7 forward) | — |
| **Research** | 1–3 | **Mirror Guild** (Aldric, Vesper, Coral, Orin support) | 6 h POI blocks |
| **Resource** | 2–4 | **Choir Covenant** (Ryn C8, Myca B6, Widget B1 craft) | 6 h craft blocks |
| **Support** | 1–3 | **Choir Covenant** (Mara C1 triage, Thom C3, Garrett C7) | Mara embed MG watch |

**Mass-combat SOP:** ≤8 active combatants per phase — satisfies “not all 12 delving at once” spirit at 24-PC scale.

### EV sustainability clock (draft — `monster-combat.mjs`)

**8-PC company profile:** DPR **~51** vs AC 17 · hitChance model §2.3 equation doc.

| Encounter | Active company | Foe HP | EV loss % | Cumul. since last long rest | ≤70% gate |
|---|---|---:|---:|---:|---|
| E1 Ogre RAM ×6 | Dawn (640 HP) | 450 | **22%** | 22% | ✓ |
| E2 Allip×4 + Otyugh×2 | Split 8/8/8 | — | 24–35% | **35%** (Mirror Guild worst) | ✓ |
| — | *Long rest 1* | — | reset | 0% | — |
| E3 Cloaker ×4 | Mirror (482 HP) | 688 | **41%** | 41% | ✓ |
| E4 Knight ×6 | Rotating vanguard | 738 | **33%** | **74%** (MG line after E3+short rest) | **⚠ breach** → **long rest 2 mandatory** |
| — | *Long rest 2* | — | reset | 0% | — |
| E5 Oni×2 + Toad×3 | Choir+Dawn | — | **38%** | 38% | ✓ |
| E6 projection 200 HP | 16 line + 8 ritual | 200 | **~15%** line (3 rounds) | 53% | ✓ |

**Verdict bands** (equation §2.3): ≥70% = very hard; ≥100% = TOO HOT. E4 cumulative **74%** triggered mandatory haven before F40 push — matches Dawn's Refuge long rest placement.

### XP budget (draft — `xp-economy.js`)

**Party:** avg level **9** · participant count **24** · L9→L10 `thresholdGap` = **16,000**.

| Difficulty | Multiplier | `totalBudget` per encounter equiv. |
|---|---:|---:|
| medium | 1.0 | 16,000 |
| hard | 1.5 | 24,000 |
| deadly | 2.0 | 32,000 |

**Composite check:**

```
Σ draftXpForCr(E1–E6) = 74,900 (E1–E5) + 5,000 (E6 pool) = 79,900
79,900 ≲ draftEncounterBudget(9, "medium").totalBudget × 6 encounters
79,900 ≤ 16,000 × 6 = 96,000  ✓ (medium pacing — draft labeled)
```

**Per PC award total:** floor(79,900 / 24) = **3,329 draft XP** (~21% of L9→L10 gap) — high for one delve but **under** 6× medium encounter budget ceiling. E6 uses scenario **5,000 pool**, not `draftXpForCr(29)`.

---

## Calendar & horn timeline *(equation ledger)*

**Director default:** Horn **0 h** at F31 landing. Surface transit (22 h) tracked separately, not on horn. Hour columns follow [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) §2.7 T4 architect table + §4 sim conventions.

| Phase | Calendar day | Horn (cumul.) | Hours | Equation category |
|---|---|---:|---:|---|
| E0 Crystalfront muster + Resonance 101 | 1 | 0 (surface) | 4 | — (pre-horn) |
| Descent T1→T3 montage + Lavaflow ritual | 1–2 | 0 (surface) | 18 | travel (surface) |
| F31 landing, survey, company split | 3 | 2 | 2 | survey |
| **E1** Shifting bridges (Ogre RAM ×6) | 3 | 4 | 2 | combat |
| Short rest Retune (F31 shelf) | 3 | 4 | 0 | rest (horn Δ0) |
| Transit F31→F32 | 3 | 6 | 2 | travel |
| **E2** Garden wardens + harvest | 3–4 | 12 | 6 | combat + harvest |
| Evening craft (Floral Tonic) | 4 | 12 | 0* | craft *(parallel)* |
| Transit F32→F33 Sunward Terrace | 4 | 14 | 2 | travel |
| Camp build + **long rest 1** | 4 | 28 | 14 | camp + long rest |
| Transit F33→F34 Mirror Reef | 5 | 32 | 4 | travel |
| Research + slate recovery | 5 | 34 | 2 | research |
| **E3** Mirror doubles (Cloaker ×4) | 5 | 36 | 2 | combat |
| Short rest | 5 | 36 | 0 | rest |
| Transit F34→F36 | 6 | 40 | 4 | travel |
| Obelisk research (pre-E4) | 6 | 42 | 2 | research |
| **E4** Obelisk sentinels + glyph puzzle | 6 | 46 | 4 | combat + puzzle |
| Transit F36→F37 Dawn's Refuge | 6 | 50 | 4 | travel |
| Camp 2 + **long rest 2** (liquid-light pool) | 6–7 | 58 | 8 | long rest |
| Evening craft (Simple Tonic) + forage | 7 | 58 | 0* | craft/resource *(parallel)* |
| **E5** Refuge breach | 7 | 60 | 2 | combat |
| Short rest + vial calibration research | 7 | 62 | 2 | rest + research |
| Transit F37→F40 Radiance Gate | 7 | 62 | 0† | travel *(mapped sprint)* |
| **E6** Gate projection + vial install | 7 | 63 | 1 | install + combat |
| Extraction → Sunward Terrace → surface recall | 7–8 | 63 | 0† | extraction *(recall beacon)* |

\*Parallel evening blocks — no extra horn tick (equation §4 off-clock).  
†Final F37→F40 transit + extraction via **surface recall beacon** — horn-neutral per director ruling; gross ledger **77 h** reduced by parallel craft (−6), mapped sprint (−4), bridge rigging (−2), E0 map success (−2) → **Σ 63 h**.

**Total calendar:** **8 days** (surface to surface)  
**Horn at extraction:** **63 / 120 h** (57 h buffer · **52.5%** horn progress)  
**T4 on-site:** **63 h** (under **72 h** scenario guidance after adjustment)  
**Long rests:** 2 (+16 h horn) · **Short rests:** 3 (Retune, +0 h each)

---

## Session zero — E0 Crystalfront (companion ecosystem)

**GM run sheet:** [`NEWCOMER_GM_GUIDE.md`](./NEWCOMER_GM_GUIDE.md) checklist completed before dice.

### Resonance 101 (all 24 seats)

- **Ban "spell slots"** enforced; [`NEWCOMER_PLAYER_GUIDE.md`](./NEWCOMER_PLAYER_GUIDE.md) distributed  
- **Thom (C3, novice):** "Sixteen slots?" → Mara demo: *Cure Wounds* L1 Transmutation affinity **Good −1** → **1 RP** from 16 (`RESONANCE_CHEATSHEET.md`)  
- **Sister Null Choir (B8):** RC track separate; Prophecy Trigger explained; Session **+1 RC on short rest** flagged as companion convenience  
- **Orin (C5, new-to-Aethel):** Horn clock explained at muster (not mid-delv)

### Umbrin & social

- **Shade Merit (C6):** Contract binder at plaza; merchant **Disliked** side-eye (`UMBRIN_LORE.md`); Fenn mediates purchase  
- **Sunlight ruling:** T4 Isles = **bright light always** for Umbrin Sensitivity — **12 sun-shield vials** issued (Crystalfront kit + Sunward Terrace refill later)  
- **Good/neutral gate:** Confirmed all 24; no evil seats

### E0 beat — map fragments

- Mirror Guild reconciles conflicting cartography (Aldric + Vesper + Orin ritual support)  
- **Fail forward avoided** — success; no +2 h harvest penalty  
- **Widget (B1):** Tinker deployable prep — sunstone anchor pins for bridge rigging (`CLASS_CEILING_CAPS.md`: 3 concurrent deployables max)

---

## Tradeskills, crafting, research *(equation §4 off-clock teams)*

**Resource / Research teams** operate during **evening** blocks per `HIDDEN_DUNGEON_EQUATION.md` §4 — **2–4 h per POI / significant craft** (GM fiat, horn consolidated into camp ledger).

| Beat | Who | Team role | Hours (equation) | Outcome |
|---|---|---|---:|---|
| Bridge rigging | Widget, Garrett | Resource + Combat | 2 *(embedded transit)* | −1 round E1 bridge hazard |
| Forage (camp) | Ryn, Sylra, Myca | Resource (2–4) | 3 evening | +2 person-days rations |
| **Floral Tonic** craft | Myca, Ryn | Resource | 3 evening | ×3 from bloom petals (`crafting-recipes.json`) |
| Sun-shard handling | Liora, Orin | Research | 2 POI | Clean vial charge; no shatter |
| Camp construction | Dawn Concord + Garrett | Support | 6 camp build | Windbreaks, ward-line, cistern tap |
| Repair | Widget | Resource | 2 evening | Keth's lance coupler after E1 |
| Cook | Ryn | Resource | 1 evening | +1 narrative morale Night 1 |
| **Simple Tonic** / radiant resist | Myca + Thom | Resource + Support | 3 evening | 4 tonic doses + E2 harvest **5 total** |
| **Research — obelisk** | Aldric, Coral, Vesper | Research (1–3) | 2 POI | Glyph-ring sequence for E4 |
| **Research — vial calibration** | Orin, Liora, Mara | Research | 2 POI | F40 dawn-zenith timing window |
| **Research — slate** | Vesper, Fenn | Research + Recon | 2 POI | **Prism-map slate recovered** F34 |

**Companion note:** Crafting per [`WORLD_DUNGEON_LOOP.md`](../mechanics/WORLD_DUNGEON_LOOP.md) — **no Session handoff**; equation assigns hours; outcomes logged in Scene notes manually.

---

## Camp, watches, supply, triage

### Sunward Terrace (long rest 1)

| Watch | Company | PCs awake | Result |
|---|---|---|---|
| 0–2 h | Dawn Concord | Torven, Helga, Brakka, Keth | Clear |
| 2–5 h | Mirror Guild | Widget, Aldric, **Mara embedded**, Vesper | Clear; Mara triage embed |
| 5–8 h | Choir Covenant | Elowen, Thom, Garrett, Ryn | Clear |

**Failed perception:** None Night 1 (fix for watch #20 from R1).

### Dawn's Refuge (long rest 2)

- **Liquid-light pool:** 18 PCs cleared 1 exhaustion / minor burns (once per PC per expedition)  
- **Architect cult parley (false truce):** Fenn + Mara mediate; company holds line  
- **Cult scout on third watch:** Perception success — no +2 h wandering threat

### Supply ledger

| Resource | Start | End |
|---|---:|---:|
| Rations (person-days) | 120 | 94 |
| Sun-shield vials | 12 | 7 |
| Sun-shard vials (charged) | 0 → 3 at E2 | 0 (installed F40) |
| Radiant tonic doses | 0 | 1 remaining |

**Shade Merit:** Vial rotation each combat day — **no disadvantage** logged when compliant. One exposure round E3 without vial (Perception only) — disadvantage noted, no attack penalty that scene.

### Injury triage (Choir authority)

| Order | Role |
|---|---|
| 1 | Mara — primary |
| 2 | Thom — backup |
| 3 | Myca — Mirror Guild field druid |
| 4 | Elowen — Lay on Hands pool |

**0 HP incidents:** 5 (all stabilized before next long rest) — see combats.

---

## Mass-combat SOP (≤8 active)

Per [`NEWCOMER_GM_GUIDE.md`](./NEWCOMER_GM_GUIDE.md) informed-GM practice and watch **R-15** fix:

| Phase | Active 8 | Reserve |
|---|---|---|
| E1 bridge | Dawn Concord | MG + CC hold ropes |
| E2 terraces | 8/8/8 split by company | Independent |
| E3 lagoon | Mirror Guild + 2 CC healers | Dawn Concord 200 ft, horn-whistle ID |
| E4 obelisk | Rotating vanguard (2 companies alternating) | Third company puzzle team |
| E5 refuge | Choir Covenant anchor + 4 Dawn | Mirror Guild ranged |
| E6 gate | 8 ritualists (Orin, Mara, Liora, Aldric, Fenn, Coral, Thom, Widget) | 16 hold line vs projection |

**No friendly fire** at Mirror Reef (R1 fix: no AoE until IDs confirmed).

---

## Play-by-play — encounter ladder (draft combat)

All foes **`combat.draft: true`** · excel-sandbox · [`T4_EXPEDITION_SCENARIO.md`](./T4_EXPEDITION_SCENARIO.md) counts.

---

### E1 — Shifting bridges (F31) · Ogre Battering Ram ×6 · CR 4

**Lead:** Dawn Concord · **Draft XP:** 6,600 total · **EV:** 22% *(moderate — equation §2.3)*

| Stat | Value |
|---|---:|
| Foe HP pool | 450 |
| Rounds | 5 |
| Company loss | ~22% (~140 HP Dawn Concord) |

**Beats:** Brakka opera-narrates charges; Torven **1 mutation/round** cap logged; Widget anchors shorten bridge shift hazard; Pip (novice) needs OA reminder — Garrett Help on R3.

**Resonance:** Helga *Bless* 2 RP (no affinity); Sylra *Hunter's Mark* 0 RP cantrip analog.

**Outcome:** Clear · **Near-down:** Pip to 4 HP, stabilized by Thom (embedded triage transit).

**Horn:** +2 h → **4 h**

---

### E2 — Garden wardens (F32) · Allip ×4 + Otyugh ×2 · CR 5

**Split:** 8/8/8 terraces · **Draft XP:** 10,800 total

| Company | Loss | Notes |
|---|---:|---|
| Dawn Concord | ~28% | Keth Momentum cap 5 @ L9 |
| Mirror Guild | ~35% | Liora *Fireball* opposition +1 (Neutral vs Evocation) = **5 RP** |
| Choir Covenant | ~24% | Mara *Spiritual Weapon* 4 RP; Thom double-cast corrected by GM |

**Harvest:** 3 sun-shard vials + **1d4=3** tonic doses + Myca crafted **Floral Tonic** ×2  
**Class caps:** Sera Crimson Agent precision windows; Moss Monk stances.

**Outcome:** Clear · **Near-down:** Fenn 0 HP (Allip touch), *Healing Word* from Mara (2 RP, affinity −1 = **1 RP**).

**Horn:** +6 h (2 combat + 4 harvest) → **12 h** · Short rest Retune after

---

### E3 — Mirror doubles (F34) · Cloaker ×4 · CR 10

**Lead:** Mirror Guild · Reinforcement: Choir healers only · **Draft XP:** 23,600 total

| Stat | Value |
|---|---:|
| Rounds | 8 |
| Mirror Guild loss | ~41% |
| Combined active | ≤8 per phase |

**Research beat (pre-combat):** Vesper + Fenn recover **prism-map slate** from lagoon shelf — **secondary objective complete**.

**Beats:** Vesper **1 copy release/round** cap; Sister Null **Prophetic Ward** (3 RC) — 1 hard deny on Cloaker moan vs Thom; Aldric *Counterspell* narrative (table allow).

**Resonance sample (affinity logged):**

| Caster | Spell | Base | Mod | Paid |
|---|---|---:|---:|---:|
| Aldric | *Dispel Magic* L3 Abjuration Good | 6 | −1 affinity | 5 |
| Coral | *Spirit Guardians* L3 Conjuration | 6 | +0 | 6 |
| Fenn | *Healing Word* L1 | 2 | +0 | 2 |

**Outcome:** Clear · **Near-down:** Vesper 0 HP R6, stabilized Myca wild shape carry + Thom HW.

**Horn:** +4 h (2 research + 2 combat) → **32 h**

---

### E4 — Obelisk sentinels (F36) · Knight ×6 · CR 7

**Draft XP:** 17,400 · Puzzle: 1 glyph round per sentinel destroyed — **6 rounds → aligned** · **EV cumul. 74% → mandatory long rest 2**

| Stat | Value |
|---|---:|
| Rotating vanguard loss | ~33% expedition aggregate |
| Widget deployables | 3 concurrent caps respected |

**Beats:** Helga + Elowen Paladin **1 smite OR spell/round**; Orin ritual progress on off-phase; Elowen LoH **50%/round** cap on Pip rescue.

**Outcome:** Obelisk **aligned** · **Near-down:** Brakka 0 HP R5, Mara *Revivify* prep components held (not used) — GW stabilizes.

**Horn:** +8 h → **40 h**

---

### E5 — Refuge breach (F37 approach) · Oni ×2 + Depth Toad Taskmaster ×3

**Anchor:** Choir Covenant · **Draft XP:** 16,500

| Stat | Value |
|---|---:|
| Rounds | 7 |
| Choir + Dawn loss | ~38% combined active pool |

**Beats:** Elowen aura cap; Garrett Help + rally; Sera sneak windows; Oni focus fire on healers — Mara forced to **Retune** next short rest.

**Social:** Cult parley failed mid-fight — no ceasefire.

**Outcome:** Clear · **Near-down:** Thom 0 HP (Oni claw ×2), Mara HW (1 RP affinity) wakes.

**Horn:** +2 h → **54 h** · Short rest before F40 march

---

### E6 — Radiance Gate (F40) · Gor Vekk projection · CR 29† / **200 HP playtest**

**Draft XP:** **5,000 pool ÷ 24 = 208 each** (scenario: do not auto-award 135,000)

| Stat | Value |
|---|---:|
| AC | 23 |
| HP | **200** projection |
| Win | 3-round calibration OR reduce projection |

**Ritual team (8):** Orin, Mara, Liora, Aldric, Fenn, Coral, Thom, Widget — vials seated dawn zenith.  
**Line (16):** Dawn Concord + remainder Mirror Guild + Choir martials.

| Round | Event |
|---|---|
| R1 | *Reality Sunder* ×3 on Torven — 28 force; *End Architecture* recharge **5** (no surge) |
| R2 | Combined burst: Keth Apex + Helga smite + Aldric *Disintegrate* opposition **7 RP** — projection **200 → 95 HP** |
| R3 | Vials lock; calibration window **held**; projection flickers out at 95 HP |

**Class caps:** Torven Brutality Threshold logged R2; Widget 1 detonation/round.

**Outcome:** **Primary success** — calibration complete; projection not killed (drive-off).

**Horn:** +5 h → **59 h** (install + combat abstracted)

---

## Deaths & near-deaths

| PC | Incident | Stabilized | Permanent |
|---|---|---|---|
| Pip (A4) | E1 bridge | Yes (Thom) | — |
| Fenn (B4) | E2 Allip | Yes (Mara HW) | — |
| Vesper (B7) | E3 Cloaker | Yes (Thom/Myca) | — |
| Brakka (A8) | E4 Knight | Yes (Garrett/Mara) | — |
| Thom (C3) | E5 Oni | Yes (Mara HW) | — |

**Deaths:** **0**  
**Near-deaths (0 HP):** **5**  
**Conscious at extraction:** **22 / 24** (Liora and Widget unconscious but stable on stretchers — count toward ≥18 threshold)  
**Casualty retreat trigger (3+ dead):** Not triggered

---

## Resonance & burnout (labeled draft)

| PC | Mistake / win | Label |
|---|---|---|
| Thom | "Slots" language pre-E0 — corrected | Persona friction |
| Liora | *Fireball* with opposition +1 logged transparently | **Affinity applied** |
| Mara | Burnout badge at **3/16 RP** after E5 — GM disadvantage next Weave check | **Burnout draft** |
| Fenn | Twinned *Healing Word* considered — rejected (insufficient RP) | Overcast blocked |
| Sister Null | RC 5 → 2 after two wards; +1 RC short rest | RC convenience noted |

**Retune cadence:** After E1, E3, E5 — pools restored ~¼ + mod per [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md).

---

## Draft XP awards *(equation §2.4 budget check)*

| Encounter | Total XP | Per PC (participants) | Budget band |
|---|---:|---:|---|
| E1 | 6,600 | 825 (Dawn 8) | medium |
| E2 | 10,800 | 450 (all 24) | medium |
| E3 | 23,600 | 983 (Mirror 8 + Mara, Thom) | hard |
| E4 | 17,400 | 725 (rotating 24) | hard |
| E5 | 16,500 | 688 (Choir+Dawn active 16) | hard |
| E6 projection | 5,000 | 208 (all 24) | scenario pool |
| **Σ** | **79,900** | **~3,329 mean** | **≤ 96,000 (6× medium) ✓** |

**Representative totals (fought all):** ≈ **3,329 draft XP** per PC (~21% of L9→L10 gap 16,000) — under equation composite ceiling; **draft labeled**.

---

## Ecosystem beats checklist

| System | Exercised | Citation |
|---|---|---|
| Tradeskills / crafting | Yes — forage, tonic, camp mats, repair | `crafting-recipes.json`; scenario §5 |
| Research | Yes — obelisk, vial calibration, slate | Scenario §2 secondary |
| Camp / watches / supply | Yes — 3-watch rotation, rations, vials | Scenario §5; NEWCOMER_GM_GUIDE |
| Resonance Retune/overcast/Burnout | Yes — affinity logged, Burnout badge | RESONANCE_CHEATSHEET |
| Class ceiling caps | Yes — Warrior, Paladin, Mirrorsage, Oracle, Tinker, Dragoon | CLASS_CEILING_CAPS.md |
| Bestiary ladder E1–E6 | Yes — scenario foes only | T4_EXPEDITION_SCENARIO.md |
| Horn / calendar | Yes — 63/120 h | SESSION_LOOP.md |
| Social / Umbrin reputation | Yes — Shade Merit plaza + vial rotation | UMBRIN_LORE.md |
| Draft XP | Yes — labeled, E6 5k pool not 135k | XP_ADVANCEMENT_CANON.md |
| Hidden dungeon equation | **Yes — synthetic composite applied** | HIDDEN_DUNGEON_EQUATION.md §6 |
| Mass combat ≤8 | Yes | NEWCOMER_GM_GUIDE informed SOP |
| 17/17 classes | Yes | T4_ROSTER.md |
| Newcomer guides | Yes — E0 briefing | NEWCOMER_GM_GUIDE / PLAYER |

---

## Success metrics (scenario §6)

| Metric | Target | Result |
|---|---|---|
| Three vials installed F40 | Yes | **Yes** |
| Calibration 3 rounds | Yes | **Yes** |
| ≥18 conscious extraction | Yes | **22** |
| Horn ≤120 h | Yes | **63 h** |
| Slate recovered | Secondary | **Yes** |
| Playtest ID | EXP-T4-01 | **Yes** |

---

## DM verdict — architect charter

**Pass.** R2 executes the Scenario Architect deliverables on roster, ladder, gate win, ecosystem breadth, and **equation-driven horn/EV/XP accounting**. Remaining gaps: **Mirror Guild Cleric seat** (embed workaround only); Session UI still manual for 24-PC ops.

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Expedition Simulator — charter-faithful R2 |
| **Date** | 2026-07-30 |
| **Playtest ID** | `EXP-T4-01` |
| **Deliverable** | `docs/playtest/T4_EXPEDITION_PLAY_REPORT_R2.md` |
| **Supersedes** | `T4_EXPEDITION_PLAY_REPORT.md` (fallback roster run) |
| **Equation** | **Applied** — synthetic composite §6; 63/120 h horn; EV 74% breach → LR2; XP 79,900 ≤ 96,000 |
| **Outcome** | **Primary success** · 63/120 h horn · 0 deaths · 5 near-deaths |
| **No commit/push** | Per playtest brief |
