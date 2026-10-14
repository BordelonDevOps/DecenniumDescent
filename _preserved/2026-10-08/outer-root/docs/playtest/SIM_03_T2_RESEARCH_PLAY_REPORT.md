# Simulation play report — T2 research expedition (SIM-T2-RES-03)

> **Historical rules snapshot:** This report preserves the terminology and mechanics used when the simulation was run. Current magic canon is [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md): RP + Dissonance/Refrain, no automatic alignment/reputation spell pricing, and Low Resonance instead of the retired Burnout subsystem. Historical observations remain useful, but superseded magic rulings are not current RAW.


**Playtest ID:** `SIM-T2-RES-03`  
**Campaign:** [`SIM_CAMPAIGN_PLAN.md`](./SIM_CAMPAIGN_PLAN.md) · Sim **#3 of 7**  
**DM Simulator run:** 2026-07-30  
**Tier:** T2 (Bloomdeep Marsh · Floors 11–15) · **Format:** 1 company × **7 PCs** · Research team ≥2  
**Ruleset:** Resonance Hybrid-B · draft XP · excel-sandbox bestiary · **synthetic sim constraint** [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) §6  
**Continuity in:** [`SIM_02_T1_CRAFT_PLAY_REPORT.md`](./SIM_02_T1_CRAFT_PLAY_REPORT.md) — L5 company · horn **58.5 h** · gate-kit · map through F10  
**Continuity out:** → Sim #4 `SIM-T3-MIX-04` (Anvil mixed companies)

---

## Expedition brief

### Setting

**Bloomdeep Marsh** F11–15 — bioluminescent swamp with no surface bazaar. Research focus: **Reedcaller’s Circle** signal doctrine, **Phantom Mire** recon, **Overgrown Reliquary** artifact chain, **Rootlight Sanctuary** haven.

### Goal

1. **Research team ≥2** identifies reliquary cache (Floors 14–15).  
2. Deliver **map through F15** to Concord cartographers.  
3. Keep **segment horn ≤48 h** while satisfying **120 h cumulative inequality**.  
4. Track **Oracle RC** separately from Weave RP.

### Stakes

- **Success:** Artifact ID + F15 map + horn segment ≤48 h → T3 mixed-company sim.  
- **Partial:** Map incomplete → Sim #4 with blind F21 entry.  
- **Fail:** Phantom Mire drowning **or** cumulative horn >95 h **or** Research team wiped.

---

## Synthetic sim constraint — T2 composite budget

Per [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) §4 (Research: **2–4 h per POI**) and §6 checklist:

```
120 ≥ 58.5 (prior) + Σ(T2 activities)   → T2 segment cap 48 h ⇒ cumulative max 106.5 h

Research POI hours: 2–4 h each (identify, map fragment, reconcile)
Craft hours: 0 (Resource off-rotation minimal — 2 h scribing only)
EV guard: cumulative EV_loss_pct < 70% between long rests
```

### T2 hour table (segment)

| Activity | Hours | Type |
|---|---:|---|
| F10→F11 marsh descent | 4 | travel |
| Reedcaller’s Circle — signal drill | 3 | research |
| Spore-Veil Falls — timed dash | 2 | travel/hazard |
| Phantom Mire — recon (Research + Recon) | 4 | research/recon |
| Overgrown Reliquary — artifact ID | 4 | research |
| Reliquary root-grasper combat (CR 2) | 1.5 | combat |
| Rootlight Sanctuary long rest | 8 | camp |
| F14–15 mapping sweep | 6 | research/travel |
| F15 bog wisp combat (CR 1 ×2) | 1.5 | combat |
| Return Rootlight → F11 cache | 4 | travel |
| Evening scribing (Research off-clock) | 2 | research |
| **T2 segment total** | **40** | |
| **Cumulative horn** | **98.5** | ≤120 ✓ |

**Segment ≤48 h:** ✓ (40 h) · **Buffer to horn:** 21.5 h

---

## Company roster (L5, Good/Neutral) — 7 PCs

Research-heavy trim: Brin and Torin rotate off (surface gate-kit duty); **Selene Thalen** (Oracle) joins for RC tracking.

| Slot | Character | Race / class | Team | HP | AC | Pool | Role |
|---|---|---|---|---:|---:|---|---|
| R1 | **Mira Vale** | Human · Wizard L5 | Research | 30 | 14 | 12 / 12 RP | Arcana lead |
| R2 | **Saffron Reed** | Elf · Mirrorsage L5 | Research | 28 | 14 | 9 / 9 RP *(draft)* | Academic Factions +1 |
| R3 | **Selene Thalen** | Human · Oracle L5 | Research | 28 | 15 | **5 / 5 RC** | Mystery: Ancestor *(canon)* |
| R4 | **Vesper Ashwhisper** | Umbrin · Bard L5 | Face / Recon | 26 | 14 | 6 / 6 RP *(draft)* | Reedcaller signals |
| R5 | **Helga Stoneprayer** | Dwarf · Cleric L5 | Support | 36 | 17 | 10 / 10 RP | Spore remedy |
| R6 | **Joss Merrow** | Halfling · Thief L5 | Recon | 30 | 16 | 7 / 7 RP *(draft)* | Phantom Mire scout |
| R7 | **Kael Grunn** | Swamp Troll · Warrior L5 | Combat | 48 | 18 | — | Escort |

**Research team (3):** Mira, Saffron, Selene — exceeds ≥2 requirement.

---

## Session zero — Oracle RC vs RP

**DM tracks two pools on Selene:**

| Pool | Max | Recovery (Session defaults) |
|---|---:|---|
| **RC** (Revelation Charges) | **5** | L5: `3 + floor((5−1)/2)` per `session-utils.ts` |
| **RP** | **0** | Oracle excluded from Weave (`RESONANCE_CANON.md` §6) |

**Selene brief:** *Revelation* costs RC, not RP. Session shows RC column only when saved Oracle pulled.

**Party RP (Weave) separate:** Mira/Saffron/Vesper/Helga/Joss RP tracked independently; no party-pool confusion this sim.

---

## Phase A — F11 Reedcaller’s Circle (3 h research)

**Team:** Vesper (signals), Saffron (acoustics log), Joss (perimeter).

**Procedure:**

1. Establish **whistle–touch–light** code (no shouted commands).  
2. Saffron Investigation **16** — maps echo radius (~40 yd).  
3. Vesper Performance **14** — test false echo lures (0 RP *minor illusion*).

**Output:** **Signal doctrine v1** — reduces future marsh encounter surprise (−2 h travel on F14 sweep applied in Phase E).

**Academic Factions:** Saffron’s acoustics appendix → **+1 rep** (narrative; now **+2 total** since Sim #1).

---

## Phase B — Spore-Veil Falls hazard (2 h)

**Table call (documented per success metric #4):**

| Hazard | Rule | Outcome |
|---|---|---|
| Spore burst | CON save DC 13 on mist contact or **Blinded 1 min** | Helga **15**, Joss **17**, Kael **12 fail** — blind 1 round |
| Timing dash | DEX group check DC 12 between spurts | **Success** — no extra horn |
| Remedy | *Standard Oil* (Sim #2 craft) smear → advantage next CON save | Helga applies; no RP |

**Horn:** +2 h · **No combat.**

---

## Phase C — Phantom Mire recon (4 h)

**Team:** Joss (lead), Selene (RC), Saffron (map), Kael ( tether rope).

- Joss Survival **18** — identifies shallow shelf path.  
- Selene spends **1 RC** — *Ancestor’s Warning* (table: advantage on next Perception vs ambush) — **RC 4/5**.  
- Misstep scare: Kael Strength save DC 14 **16** — holds line; no drowning.

**Research output:** Phantom Mire **safe corridor** marked on F12–13 border map.

---

## Phase D — Overgrown Reliquary (4 h research + 1.5 h combat)

**Location:** F14–15 POI (`floor-encounters.json`).

**Artifact ID (success metric #1):**

| Step | Actor | Check | Result |
|---|---|---|---|
| Sarcophagus survey | Mira | Investigation DC 14 | **19** |
| Statue alignment | Saffron | History DC 13 | **15** — **First Cycle surveyor** era |
| Oracle read | Selene | **2 RC** — *Spirit Communion* (Revelation) | Names cache: **“Heartroot Surveyor’s Seal”** |
| Scribe copy | Saffron | Scribing 2 h (evening block deferred) | Rubbing secured |

**Artifact ID: SUCCESS** — seal identifies pre-Bloom cartography network.

**Combat — animated root-graspers (2 × CR 1 proxy, Deep Dwarf stat reskin HP 52):**

| EV (draft) | Value |
|---|---:|
| Party HP | 226 |
| EV_loss_pct | **~32%** |
| Rounds | 4 |

**Resonance spend:**

| PC | Spend | Pool after |
|---|---|---|
| Mira | *Burning hands* 2 RP | 10/12 |
| Helga | *Spiritual weapon* 4 RP → 3 RP (Religious −1) | 6/10 |
| Vesper | *Healing word* 2 RP | 4/6 |
| Selene | **0 RC combat** (saved) | 2/5 |

**Draft XP:** 400 → **57 each** (7 PCs).

---

## Phase E — Rootlight long rest + F14–15 map (14 h)

**Rootlight Sanctuary** — long rest **+8 h horn** · full RP · Selene **RC → 5/5**.

**F14–15 mapping (6 h):** Research team completes **Concord grid through F15** including Phantom Mire corridor and Reliquary annotation.

**Signal doctrine bonus:** −2 h applied (net 4 h effective for sweep).

---

## Phase F — F15 bog wisp combat + extraction (5.5 h)

**Encounter:** 2 × CR 1 (Drider ooze proxy — Yieldheart bleed) — quick clear.

- EV_loss_pct **~22%** cumulative since long rest.  
- **Draft XP:** 400 → **57 each**.

**Return to F11 cache** (4 h) · **Scribing** (2 h evening): Saffron transcribes seal rubbings.

---

## Oracle RC ledger (metric #5)

| Event | RC Δ | RC current |
|---|---:|---:|
| Start | — | 5/5 |
| Phantom Mire *Ancestor’s Warning* | −1 | 4/5 |
| Reliquary *Spirit Communion* | −2 | 2/5 |
| Long rest (Full) | → max | **5/5** |
| Combat | 0 | 5/5 |
| **End state** | | **5/5** |

**No RC conflated with RP** — Session RC column used; Weave casters never assigned RC.

---

## Horn tally

| Segment | Hours | Cumulative |
|---|---:|---:|
| Sim #1–2 carry | 58.5 | 58.5 |
| Descent + Reedcaller | 7 | 65.5 |
| Spore + Phantom Mire | 6 | 71.5 |
| Reliquary + combat | 5.5 | 77 |
| Long rest | 8 | 85 |
| F14–15 map | 6 | 91 |
| F15 combat + return + scribe | 7.5 | **98.5** |

**T2 segment:** 40 h (≤48 ✓) · **Campaign cumulative:** 98.5 h (≤120 ✓, **21.5 h buffer**)

---

## XP pacing (draft — equation §2.4)

```
draftEncounterBudget(5, medium, 7):
  L5→L6 gap = 9,000 XP × 1.0 = 9,000 total → ~1,285 per PC medium budget

This sim awards: 57 + 57 = 114 XP per PC (2 fights) — well under budget (intentional research sim)
```

---

## Success metrics (Sim #3)

| Metric | Target | Result |
|---|---|---|
| Artifact ID | Reliquary cache | ✓ Heartroot Surveyor’s Seal |
| Map through F15 | delivered | ✓ Concord grid complete |
| Horn segment | ≤48 h | ✓ 40 h |
| Spore hazard table call | documented | ✓ Phase B |
| Oracle RC separate | tracked | ✓ RC ledger; no RP bleed |

---

## Friction log

| # | Area | Friction | Severity |
|---:|---|---|---|
| 1 | Research | Still no Research UI — paper POI hours | Medium |
| 2 | Equation | −2 h map bonus GM-applied, not engine | Low |
| 3 | Bestiary | No Bloomdeep zone tag — Yieldheart proxies | Medium |
| 4 | Oracle | RC spend narrative — no Revelation picker in Session | Medium |
| 5 | Positive | Reedcaller doctrine carried from Sim #1 Gallery preview | Low |

---

## Sim #3 conclusion

**Outcome: SUCCESS.**

The T2 research expedition fielded **three Research specialists** (including Oracle **RC** tracked separately), identified the **Heartroot Surveyor’s Seal** at the Overgrown Reliquary, mapped **through F15**, and closed the segment at **40 h** (cumulative **98.5 / 120 h**) while documenting **Spore-Veil Falls** hazard calls. The company is positioned for **Tier 3 mixed-company** rotation at the Sporemist Gate approach.

**Carry-forward to Sim #4:** F15 map · Surveyor’s Seal · horn **98.5 h** (**21.5 h buffer** — long rest before T3 mandatory) · signal doctrine v1 · Selene RC mechanics validated.

---

## Appendix

- [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) · `src/data/floor-encounters.json` (T2) · `docs/mechanics/RESONANCE_CANON.md` · `src/lib/session-utils.ts`
