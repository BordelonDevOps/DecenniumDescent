# Expedition play report — Isles of Eternal Radiance (EXP-IER-T4-01)

> **Superseded for architect sign-off:** Charter-faithful re-run with Dawn Concord / Mirror Guild / Choir Covenant roster and full E0–E6 ladder — see [`T4_EXPEDITION_PLAY_REPORT_R2.md`](./T4_EXPEDITION_PLAY_REPORT_R2.md).

**Playtest ID:** `EXP-IER-T4-01`  
**DM Simulator run:** 2026-07-30  
**Tier:** T4 (Floors 31–40) · **Format:** 3 companies × 8 PCs · **Horn budget:** 120 h underground  
**Ruleset:** Resonance (Hybrid-B), 5e-style death saves, draft XP (`xp-economy.js`), excel-sandbox bestiary combat  
**Scenario inputs:** `T4_EXPEDITION_SCENARIO.md` — **missing (gap noted)** · `T4_ROSTER.md` — **missing (minimal roster authored below)**

---

## Input gap note

`docs/playtest/T4_EXPEDITION_SCENARIO.md` and `T4_ROSTER.md` were not present at sim time. This run uses **floor-encounters.json** T4 prose (Isles of Eternal Radiance), **120 h horn rule** from `SESSION_LOOP.md`, and a **minimal 3×8 roster** (Good/Neutral, L8–L10) aligned with prior EXP-BGR-01 persona distribution. Guides referenced where available: [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md). `NEWCOMER_GM_GUIDE.md` / `NEWCOMER_PLAYER_GUIDE.md` — **not found** in repo.

---

## Expedition brief

### Setting

**Isles of Eternal Radiance** — floating sun-kissed islets, crystal bridges, perpetual dawn glare. Tri-company contract from Shardspire Concord: establish a **forward camp** at Sunward Terrace (F33), harvest **three charged sun-shard vials** from Radiant Bloom Gardens (F32), map the Mirror Reef (F34), and **probe** the Sunforged Obelisk (F36). Gor Vekk, Architect of Ends, holds the Radiance Gate (F40) — **not** a primary kill objective at this strength.

### Stakes

- **Success:** Forward camp operational; 3 sun-shard vials secured; tier map through F36 delivered to Concord cartographers.
- **Partial success:** Camp established but vials incomplete or F36 probe aborted — half payment, no Radiance Gate key progress.
- **Fail:** Forced retreat without camp, or horn blown with two+ companies combat-incapacitated.

### Horn-clock pressure (T4 gate delve)

| Activity | Hours |
|---|---:|
| Tier 3 → T4 gate transit (established route) | 16 |
| Floor 31 survey + bridge rigging | 4 |
| Each combat (clear + field bind) | 1.5 |
| Each **Short rest** (Retune) | 0 |
| Each **Long rest** (+8 h in Session) | 8 |
| Camp build / watch rotation (per night) | 6 |
| Extraction march F33 → surface gate | 12 |

**Budget:** **120 h** underground (`dungeon-mechanics.json`). Exceeding 120 h triggers horn recall; remaining underground risks the **10-year Cycle trap**.

---

## Company rosters (minimal authored — gap fill)

Three companies, **24 PCs total**. Alignment mix **Good/Neutral only**. Levels uniform within company.

### Alpha Company — **Sunward Lance** (vanguard · avg L9 · Good)

| Slot | Character | Race / class | HP | AC | Pool | Persona |
|---|---|---|---:|---:|---|---|
| A1 | **Vesper Ashwhisper** | Umbrin · Bard (Virtuoso) L9 | 52 | 15 | 14 / 14 RP *(draft)* | P1 Novice |
| A2 | **Helga Stoneprayer** | Dwarf · Cleric (Life) L9 | 68 | 18 | 16 / 16 RP | — |
| A3 | **Kael "Meterwatch" Grunn** | Swamp Troll · Warrior (Juggernaut) L9 | 78 | 18 | — | P4 Optimizer |
| A4 | **Sera Dawnmantle** | Human · Paladin (Oath) L9 | 72 | 19 | 12 / 12 RP *(draft)* | — |
| A5 | **Tamsin Weft** | Elf · Mage L9 | 48 | 14 | 18 / 18 RP | — |
| A6 | **Orin Hale** | Human · Ranger L9 | 58 | 16 | 11 / 11 RP *(draft)* | — |
| A7 | **Brokk Ironvein** | Dwarf · Warrior (Berserker) L9 | 74 | 17 | — | — |
| A8 | **Li-Wei Chen** | Human · Monk (Master) L9 | 56 | 17 | 6 / 6 RP *(draft)* | — |

**Company HP:** **506** · **Commander:** Sera Dawnmantle · **Camp role:** point assault, sun-shield line

### Beta Company — **Prism Watch** (scout/logistics · avg L8 · Neutral)

| Slot | Character | Race / class | HP | AC | Pool | Persona |
|---|---|---|---:|---:|---|---|
| B1 | **Mira Vale** | Human · Wizard L8 | 44 | 14 | 16 / 16 RP | — |
| B2 | **Helga's cousin Greta Stoneprayer** | Dwarf · Cleric L8 | 62 | 17 | 14 / 14 RP | P2 Casual 5e |
| B3 | **Kethren Quiet-Step** | Umbrin · Monk (Master) L8 | 48 | 16 | 5 / 5 RP *(draft)* | P3 PF Veteran |
| B4 | **Selene Thalen** | Elf · Oracle L8 | 46 | 15 | 5 / 5 RC | — |
| B5 | **Torin Ashford** | Human · Paladin L8 | 64 | 18 | 10 / 10 RP *(draft)* | — |
| B6 | **Joss Merrow** | Halfling · Thief L8 | 42 | 16 | 8 / 8 RP *(draft)* | — |
| B7 | **Edda Brightquill** | Gnome · Bard L8 | 40 | 14 | 12 / 12 RP *(draft)* | — |
| B8 | **Rook Farwalker** | Human · Ranger L8 | 54 | 15 | 10 / 10 RP *(draft)* | — |

**Company HP:** **400** · **Commander:** Mira Vale · **Camp role:** watches, foraging, bridge scouts

### Gamma Company — **Dawn's Anvil** (heavy reserve · avg L10 · Good/Neutral)

| Slot | Character | Race / class | HP | AC | Pool | Persona |
|---|---|---|---:|---:|---|---|
| G1 | **Commander Rhal-Voss** *(PC alt)* **Dren Voss** | Human · Warrior (Juggernaut) L10 | 86 | 19 | — | — |
| G2 | **Yara Sunthread** | Aasimar · Cleric L10 | 76 | 19 | 18 / 18 RP | — |
| G3 | **Pax Dragoon** | Human · Dragoon L10 | 70 | 18 | 9 / 9 RP *(draft)* | — |
| G4 | **Archivist Neme** | Elf · Mirrorsage L10 | 50 | 15 | 15 / 15 RP *(draft)* | — |
| G5 | **Holt Grim** | Dwarf · Paladin L10 | 80 | 20 | 14 / 14 RP *(draft)* | — |
| G6 | **Zara Ember** | Human · Mage L10 | 54 | 15 | 20 / 20 RP | — |
| G7 | **Unit Seven** | Warforged · Soldier L10 | 72 | 18 | — | — |
| G8 | **Fenn Rootward** | Wood Elf · Druid L10 | 58 | 16 | 16 / 16 RP | — |

**Company HP:** **586** · **Commander:** Dren Voss · **Camp role:** reserve, camp fortification, boss probe anchor

**Aggregate expedition:** **1,492 HP** · **24 PCs** · weighted **AC ~17** · sim **party DPR ~51/company** (8 PCs, L8–L10 martial+caster mix)

---

## Calendar & horn timeline

| Phase | Calendar day | Horn hours (cumulative) | Notes |
|---|---|---:|---|
| Surface march Shardspire → T3 gate | 1–4 | 0 (surface) | 4 days; 2 long rests; Umbrin **Sunlight Sensitivity** on open march |
| T3 traverse → T4 Radiance threshold | 5–6 | 16 | Haven rest at Anvil; heat-gear check |
| F31 landing + Alpha bridgehead | 7 | 20 | Crystal bridge rigging (+4 h) |
| **Night 1 camp** (F31 shelf) | 7 | 26 | Watch failure; Assassin strike on Beta |
| F32 Bloom harvest + fights | 8 | 38 | 2 combats; 1 short rest; **sun-shield vials −2** (supply) |
| F33 Sunward Terrace **camp build** | 8–9 | 50 | 6 h fortify; Gamma joins; long rest |
| **Night 2 camp** | 9 | 56 | 3-company watch rotation; morale event |
| F34 Mirror Reef mapping | 10 | 68 | Friendly-fire incident; Cloaker fight |
| F34–35 patrol corridor | 10 | 74 | Alpha Deva mis-ID; Gamma Duodrone ambush |
| **Night 3 camp** | 10 | 80 | Long rest; Greta RP "slot" argument |
| F36 Obelisk probe + **Gor Vekk manifestation** | 11 | 94 | Joint near-TPK; emergency retreat |
| Extraction F33 → gate | 11–12 | 106 | Beta carries wounded; Alpha covers |
| Surface debrief | 12 | 106 | **14 h horn remaining** |

**Total calendar time:** **12 days** (surface to surface)  
**On-site horn hours:** **106 / 120 h** (88 h active operations after T4 entry, incl. 3 long rests = 24 h sleep)

---

## Session zero — Resonance briefing (multi-company)

**Scene:** T3 Anvil staging camp, eve of T4 crossing. Three company commanders + 24 PCs.

**DM distributes** [`RESONANCE_CHEATSHEET.md`](./RESONANCE_CHEATSHEET.md) one-pagers.

| Persona | Company | Reaction |
|---|---|---|
| **P1 (Vesper, Alpha)** | "So fourteen points is fourteen spells?" — still conflates pool with slots at L9 scale | High friction |
| **P2 (Greta, Beta)** | Maps Retune to "short rest slots"; trusts **14 RP canon Cleric** curve | Medium → low after E1 |
| **P3 (Kethren, Beta)** | Asks Retune action cost; builds **3-action turn spreadsheet** for 8-PC company | Low friction |
| **P4 (Kael, Alpha)** | Opens `CLASS_CEILING_CAPS.md`; posts **Warrior mutation 1/round** card for both Warriors | Compliance |

**Sunlight briefing:** All three Umbrin (Vesper, Kethren) + surface-dwellers warned — T4 ambient light counts as **bright light** always. Disadvantage on Perception/attacks unless **sun-shield vial** (1 h each, 12 issued, **supply issue** below).

**Cross-company SOP agreed:** Alpha advances; Beta scouts 200 ft ahead; Gamma holds camp unless horn whistle **three short** = consolidate.

---

## Camp building, watches & supply

### Sunward Terrace forward camp (F33)

- **6 h build** (horn +6): Gamma erects sunstone windbreaks; Beta strings ward-line; Alpha digs cistern tap.
- **Supply issue — sun-shield vials:** Issued 12; ambient glare consumes **2 vials/day company-wide**. By F34, **4 vials remain** — Umbrin PCs fight at disadvantage on Day 10 unless rotated behind shields.
- **Heat fatigue:** Non-Aasimar PCs without vial: **1 level exhaustion** (table narrative) after 8 h exposure — affects Beta scout Edda, Alpha Vesper.

### Watch rotations

| Night | Plan | Failure |
|---|---|---|
| **1** (F31 shelf, pre-terrace) | Beta 1st, Gamma 2nd, Alpha 3rd | Beta watch **falls asleep** — Assassin bypasses; Greta takes surprise |
| **2** (F33 terrace) | Rotating 2-PC per company per shift | **Correct** — no encounter; Joss hears Mirror Reef echoes (foreshadow) |
| **3** (F33, pre-F36) | Double strength (post-Deva scare) | Alpha Vesper + Beta Edda **both** left post early for "warmth" — gap covered by Torin |

### Morale & RP burnout (cross-company)

- **Day 9 evening:** Umbrin players argue Sunward Lance should not lead daylight pushes. Commander Sera holds line; **−1 morale** (narrative) on Alpha until long rest.
- **Day 10 night:** Greta at **2 RP** (burnout line on 14 max) after overcasting *Spiritual Weapon* + *Guardian of Faith* in one day — **Burnout badge** shown; disadvantage on next Weave check (table).

---

## Play-by-play — combats by company

EV reference: `monster-combat.mjs` · 8-PC company **DPR ~51** vs AC 17 · **HP ~520** (Alpha 506, Beta 400, Gamma 586)

---

### Beta Company — Encounter B1 (Night 1 camp)

**Assassin** ×1 — cult agent of Gor Vekk's "Architect" sect probing camp.

| Stat | Value |
|---|---:|
| CR / XP | 8 / 3,900 |
| AC / HP | 16 / 142 |
| EV rounds / loss | 2.8 / **9%** (~38 HP) |

**Initiative highlight:** Assassin 22, Kethren 18, Greta 14.

- **R1:** Assassin *Multiattack* on sleeping Greta — **crit** (table), **26** damage → Greta **36/62**. Kethren **Tiger stance** awake from Ki sense; **Flurry** hit/hit **11**.
- **R2:** Greta **Sacred Flame** (0 RP); Assassin hits Kethren **14**. Torin **Divine Smite** rider (P2: "can I smite on first hit?" — yes, 2 RP).
- **R3:** Assassin down. Kethren **0 HP** from accumulated — **Helga-style** *Healing Word* from Greta (P2 bonus action).

**Outcome:** Win **3 rounds**. **Near-down:** Kethren. **Actual loss:** ~42 HP company-wide.

**Persona:** P3 satisfied by flurry pacing; P2 used bonus-action heal correctly at 0 HP.

**Draft XP:** 3,900 ÷ 8 = **487 each** (Beta)

**Horn:** +1.5 h → **27.5 h**

---

### Alpha Company — Encounter A1 (F32 Radiant Bloom Gardens)

**Knight** ×2 + **Allip** ×1 — light-forged patrol (excel-sandbox names; narrated as **Sunward Sentinels** + **Grief Wisp**)

| Stat | Value |
|---|---:|
| Total XP | 7,600 |
| HP pool | 246 + 95 |
| EV loss | **~31%** (~157 HP) |

**Round beats:** Kael **Action Surge** turn deletes Knight 1 (**P4 cap log**). Vesper **Empowered + Widened** *Shatter* attempt — **illegal overcast** (14 RP insufficient); downgraded to base *Shatter* (6 RP) — **Burnout risk** at 8 RP left. Tamsin *Scorching Ray* finishes Allip.

**Outcome:** Win **5 rounds**. Vesper **Sunlight Sensitivity** — disadvantage on *Shatter* save DC setup (GM ruled no effect on DC, disadvantage on her Perception to spot patrol). **Actual loss:** ~89 HP.

**Draft XP:** 7,600 ÷ 8 = **950 each** (Alpha)

**Horn:** +1.5 h → **40 h** · Short rest (+0 h) · **2 sun-shard vials** harvested (goal progress 2/3)

---

### Beta Company — Encounter B2 (F32 east terrace)

**Flameskull** ×2 — guarding bloom alcove Mira's scouts need.

| Stat | Value |
|---|---:|
| Total XP | 11,800 |
| EV loss | **53%** (~212 HP on 400 pool) |

**Near-TPK:** Edda **0 HP** (fire ray), Torin **0 HP** (recharge *Fire Ray* — P(recharge)=33%). Selene Oracle **RC** spends **Prophetic Ward** (3 RC) — table: negate one ray (cap **1 hard deny/encounter/target** per `CLASS_CEILING_CAPS.md`).

**Outcome:** Win **6 rounds**. Two death-save sequences. Mira *Counterspell* narrative on second skull (no authored counter — table allow). **Actual loss:** ~178 HP (**45%** Beta — **near-TPK**).

**Draft XP:** 11,800 ÷ 8 = **1,475 each** (Beta)

**Horn:** +1.5 h → **41.5 h**

---

### Gamma Company — Encounter G1 (F33 approach while camp builds)

**Duodrone** ×2 — sunforged constructs, misaligned glyph rings.

| Stat | Value |
|---|---:|
| Total XP | 16,800 |
| EV loss | **71%** (~415 HP on 586) |

**Hard fight:** Dren + Holt front line; Pax **Momentum** stacks (cap 6 L10). Neme **Mirrorsage** copies Pax lance ( **1 copy release/round** cap). Unit Seven **0 HP** once; Yara *Heal* (6 RP) at **Burnout line**.

**Outcome:** Win **8 rounds**. **Actual loss:** ~312 HP (**53%**). Long rest recommended — taken same night.

**Draft XP:** 16,800 ÷ 8 = **2,100 each** (Gamma)

**Horn:** +1.5 h → **51.5 h**

---

### Beta + Alpha — Encounter AB1 (F34 Mirror Reef) — **friendly fire**

**Cloaker** ×2 — illusory doubles spawn from crystal lagoon.

| Stat | Value |
|---|---:|
| Total XP | 11,800 (split **16 ways** — both companies engaged) |
| EV loss | **53%** per company if isolated |

**Cross-company incident:** Beta scouts trigger illusions; Alpha sees Beta silhouettes as cloakers. **Round 0:** Kael **readied** greataxe; Vesper casts *Faerie Fire* into mirror plane — **hits real Beta scout Joss** (friendly fire, **12** radiant). Commander Sera **horn whistle** stops volley.

**Combat:** Kethren **Webstep** ceiling strike (P3); Kael focus fire. Cloaker **Moan** (recharge save) — **4 PCs fail** including Vesper (**0 HP** again).

**Outcome:** Win **7 rounds**. **Loot dispute** after: Cloaker drop **Radiant Feather (T1)** + **Blessed Essence (T2)** — Alpha Vesper "found it" vs Beta forager claim. Sera rules **Concord split** (sell at Shardspire, shares to companies).

**Draft XP:** 11,800 ÷ 16 = **737 each** (Alpha + Beta participants)

**Horn:** +1.5 h → **69.5 h**

---

### Alpha + Gamma — Encounter AG1 (F35 sunlit corridor)

**Deva** ×1 — **misidentified as hostile** (actually Radiant Isles neutral observer; fight anyway for sim)

| Stat | Value |
|---|---:|
| XP | 7,200 |
| AC / HP | 17 / 187 |
| EV loss | **14%** (~72 HP) |

**Narrative:** Deva opens with *Aberrant Lash* (sandbox name — immersion fail). Sera **Lay on Hands** cap tracking (**50% pool/round** per Paladin ceiling). Vesper burns **Quickened** *Healing Word* (5 RP total) on wrong target again — **P1 pattern**.

**Outcome:** Win **4 rounds** after Sera parley attempt fails (Deva does not stop — table: sandbox aggression). **Actual loss:** ~64 HP combined.

**Draft XP:** 7,200 ÷ 16 = **450 each** (Alpha + Gamma)

**Horn:** +1.5 h → **74 h**

---

### Beta — Encounter B3 (F35 rear guard)

**Berbalang** ×1 — astral echo harasses supply mules.

| Stat | Value |
|---|---:|
| XP | 8,400 |
| EV loss | **18%** |

**Outcome:** Win **4 rounds**. Kethren stun attempt (**DC 13**). Greta holds RP for *Revivify* prep (not used).

**Draft XP:** 8,400 ÷ 8 = **1,050 each** (Beta)

**Horn:** +1.5 h → **75.5 h**

---

### ALL COMPANIES — Encounter BOSS (F36 Sunforged Obelisk) — **Gor Vekk manifestation**

**Gor Vekk, Architect of Ends** — not full gate boss fight; **manifestation** during obelisk alignment (3-round ritual timer before wipe).

| Stat | Value |
|---|---:|
| CR / listed XP | 29 / 135,000 |
| AC / HP | 23 / 400 |
| EV (24-PC raid) | **~7.8 rounds**, **100%+ loss** if sustained |

**Setup:** Zara aligns glyph rings; 3 sun-shard vials placed (3/3). Gor Vekk **manifests** at 50% HP phantom (table: **200 HP** effective for this probe). *Reality Sunder* ×3 + *End Architecture* recharge (33%).

**Round beats:**

- **R1:** *End Architecture* recharge **6** — DC 21 save; **8 PCs fail**; Alpha line **−120 HP** aggregate. Dren **Brutality Threshold** unlocked (100% max HP dealt — Warrior cap).
- **R2:** Pax **Apex Assault** + Holt **Smite** (Paladin **1 smite OR spell/round** cap). Gor Vekk **200 → 90** HP.
- **R3:** Manifestation **wins ritual timer** — obelisk **blinding radiance** (narrative fail-forward). Commanders call **retreat**. Kael **0 HP** holding rear; Yara stabilizes.

**Outcome:** **Tactical retreat** — obelisk probe **partial fail**, camp intel secured. **Not a kill** — award **½ listed XP** table ruling for driving manifestation off + surviving.

**Draft XP:** 67,500 ÷ 24 = **2,812 each** (all PCs)

**Horn:** +1.5 h → **94 h** · +12 h extraction → **106 h**

---

## Injuries & near-TPKs summary

| Company | 0 HP incidents | Stabilized? | Permanent loss |
|---|---|---|---|
| Alpha | Vesper ×2, Kael ×1 | All yes | None |
| Beta | Kethren ×1, Edda ×1, Torin ×1 | All yes | None |
| Gamma | Unit Seven ×1 | Yes | None |

**Nearest TPK:** Beta vs Flameskulls (**45% HP**, three PCs at 0 sequentially). **Boss probe:** 8 PCs failed save R1 — would TPK without retreat call.

---

## Resonance mistakes (novice & casual)

| PC | Mistake | Cost |
|---|---|---|
| Vesper (P1) | Empowered+Widened *Shatter* without RP math | Burnout risk; downgraded cast |
| Vesper | *Healing Word* on healthy ally during Deva fight | 5 RP wasted (Quickened) |
| Vesper | Conflated 14 RP with "14 spells" entire expedition | 3 Retunes still left pool empty Day 10 |
| Greta (P2) | *Guardian of Faith* + *Spiritual Weapon* same day without Retune plan | Burnout at 2 RP |
| Edda (Beta Bard) | Overcast **Twinned** *Hold Person* at L8 — paid 7 RP, broke concentration next round | Medium |

---

## Draft XP summary (session-local)

Per-PC totals depend on company assignment and participation in joint fights.

### Representative PC (fought all company encounters + boss probe)

| Company | PC proxy | Company XP | Joint XP (AB1+AG1+BOSS) | **Total** | % of next level |
|---|---|---:|---:|---:|---:|
| Alpha | Kael | 950 + 950 = 1,900 | 737 + 450 + 2,812 = 3,999 | **5,899** | L9→L10 gap 16,000 = **37%** |
| Beta | Greta | 487 + 1,475 + 1,050 = 3,012 | 737 + 2,812 = 3,549 | **6,561** | L8→L9 gap 14,000 = **47%** |
| Gamma | Dren | 2,100 | 450 + 2,812 = 3,262 | **5,362** | L10→L11 gap 21,000 = **26%** |

### Expedition aggregate (draft, not canon)

| Metric | Value |
|---|---:|
| Total XP awarded (all sources, 24 PCs) | **~145,000** (incl. boss half-award) |
| Mean per PC | **~6,040** |
| Encounters fought | **10** (9 company + 1 joint boss probe) |
| Boss kill | **No** — half XP table ruling |

**Level band check:** At **hard** budget (~1.5× threshold gap), a 10-fight T4 expedition targeting **~47%** of one level for L8 PCs is **high but plausible** for multi-day gate work with boss contact.

---

## Cross-company coordination scorecard

| Issue | Severity | Resolution |
|---|---|---|
| Friendly fire (Mirror Reef) | High | Horn whistle SOP; *Faerie Fire* friendly hit Joss |
| Loot dispute (Blessed Essence) | Medium | Commander split rule |
| Sun-shield supply | High | 4 vials left; Umbrin disadvantage Day 10 |
| Watch failure Night 1 | High | Assassin surprise; policy change Night 2 |
| Morale (Umbrin daylight) | Medium | Long rest + Sera speech |
| Command latency (3 companies) | Medium | Beta scouts 200 ft — too far at Mirror Reef |
| RP burnout (Greta, Vesper) | Medium | Cheat sheet re-read; Retune scheduling |

---

## Balance notes (EV combat math)

**8-PC company profile:** DPR **~51** vs AC 17 · incoming vs PC AC 17

| Encounter | Foe HP | EV rounds | EV loss % | Felt at table |
|---|---:|---:|---:|---|
| B1 Assassin | 142 | 2.8 | 9% | Moderate surprise |
| A1 Knight×2+Allip | 341 | 6.7 | 31% | Moderate |
| B2 Flameskull×2 | 344 | 6.7 | 53% | **Near-TPK** |
| G1 Duodrone×2 | 404 | 7.9 | 71% | Hard; long rest after |
| AB1 Cloaker×2 | 344 | 6.7 | 53% | Hard + friendly fire |
| AG1 Deva | 187 | 3.7 | 14% | Moderate mis-ID |
| B3 Berbalang | 202 | 4.0 | 18% | Moderate |
| BOSS Gor Vekk (200 eff.) | 200 | 3.9* | 100%+ | **Retreat or die** |

\*Raid DPR scaled ~×2.5 for 24 PCs active; manifestation HP halved for probe.

**Verdict:** T4 patrol fights (CR 7–10 equivalents) are **appropriate for L8–10 eight-PC companies** with rests. **Duodrone pair** and **Flameskull pair** exceed safe EV without long rest — matched table near-TPKs. **Gor Vekk** at listed stats is **not viable** at this strength — probe + retreat correct.

**Sandbox noise:** *Aberrant Lash* on Deva, *Freak Bite* patterns from fringe playtest persist — math usable, immersion poor.

---

## Synergies observed

| Combo | Effect |
|---|---|
| **Dren + Holt (dual frontline L10)** | Absorbed Gor Vekk R1 save failure; enabled retreat |
| **Kael Action Surge + Sera Bless/LoH** | Alpha cleared Knight pair 1 round faster than EV |
| **Selene RC Ward + Greta heal chain** | Beta Flameskull fight — 1 PC death avoided |
| **Neme Mirrorsage copy + Pax lance** | Gamma Duodrone fight — cap-compliant burst |
| **Tri-company horn SOP** | Stopped Mirror Reef TPK from becoming cross-company wipe |

**Anti-synergy:**

- **Sunlight + Umbrin** — two PCs permanently disadvantaged without vial rotation.
- **No shared Resonance briefing** until Day 5 — novices repeated L3 mistakes at L9 scale.
- **Three-company initiative** — joint fights took 2× wall-clock at table sim.

---

## DM verdict — T4 tri-company ready?

**Conditional yes for informed GMs; not for novice-only tables.**

| Ready | Not ready |
|---|---|
| 120 h horn + long rest loop | 24-PC initiative burden |
| 8-PC company EV math coherent | Friendly-fire risk at Mirror Reef POI |
| CLASS_CEILING_CAPS tested (Paladin, Warrior, Mirrorsage, Oracle) | Gor Vekk stats ≠ tier 4 gate boss expectation (CR 29) |
| Partial success path works | Sun-shield supply not in Items tab |
| Draft XP ~½ level feels fair for 12-day | `T4_EXPEDITION_SCENARIO.md` / roster **missing** |
| Multi-company command narrative rich | Death saves ×7 manual |

**Recommendation:** Author **`T4_EXPEDITION_SCENARIO.md`** with supply tables, watch rotation template, and **Gor Vekk manifestation** stat block (separate from gate boss). Label excel-sandbox attack names before live play.

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Expedition Simulator (playtest subdivision) |
| **Date** | 2026-07-30 |
| **Deliverables** | `T4_EXPEDITION_PLAY_REPORT.md`, `T4_ISSUES_LOG.md` |
| **Inputs read** | `floor-encounters.json` T4; `SESSION_LOOP.md`; `RESONANCE_CHEATSHEET.md`; `CLASS_CEILING_CAPS.md`; `XP_ADVANCEMENT_CANON.md`; `EXPEDITION_PLAY_REPORT.md` (style); `monster-combat.mjs`; `xp-economy.js`; persona stubs P1–P4 |
| **Inputs missing** | `T4_EXPEDITION_SCENARIO.md`, `T4_ROSTER.md`, `NEWCOMER_GM_GUIDE.md`, `NEWCOMER_PLAYER_GUIDE.md` |
| **Roster** | Minimal 3×8 Good/Neutral L8–L10 authored in this report (gap fill) |
| **Helpers used** | `monster-combat.mjs` EV (`totalExpectedMonsterDpr`, `rechargeAvailabilityProbability`) |
| **No commit/push** | Per playtest brief |
