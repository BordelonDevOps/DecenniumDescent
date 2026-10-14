# Hidden dungeon equation — search report

> **Historical rules snapshot:** This report preserves the terminology and mechanics used when the simulation was run. Current magic canon is [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md): RP + Dissonance/Refrain, no automatic alignment/reputation spell pricing, and Low Resonance instead of the retired Burnout subsystem. Historical observations remain useful, but superseded magic rulings are not current RAW.


**Agent:** Expedition research (playtest subdivision)  
**Date:** 2026-07-30  
**Scope:** Repo-wide search for “hidden equation,” dungeon/expedition formulas, horn-clock math, tier pressure, radiance gate math, EV/combat budget  
**Verdict:** **No source uses the phrase “hidden equation of the dungeon.”** The rulebook and companion expose **separate, partially wired systems** below. Treat this doc as a **synthesis for GMs and sim runners**, not as recovered author canon.

---

## 1. Search summary

| Phrase / concept | Found? | Notes |
|---|---|---|
| “hidden equation” / “dungeon equation” | **No** | Zero hits in `docs/`, `src/`, `scripts/`, `.cursor/`, agent transcripts, or parent workspace extracts |
| Horn clock (1200 h / day 50) | **Yes** | `dungeon-mechanics.json`, `floor-encounters.json`, Session `HORN_AT = 1200` |
| Tier pressure / radiance gate math | **Partial** | Tier 4 **Radiance Gate** is narrative (3 sun-shard vials at dawn’s zenith); **no numeric formula** |
| Expedition teams (combat / research / resource) | **Yes (structure only)** | `dungeon-mechanics.json` — **not** a time or budget equation |
| EV / combat budget | **Yes (draft sim)** | `scripts/combat-balance-sim.mjs`, `src/lib/monster-combat.mjs` |
| Encounter XP budget | **Yes (draft)** | `src/lib/xp-economy.js` — marked `draft: true` |
| Tradeskills / crafting ↔ dungeon | **No equation** | 623 recipes with `skillLevel`; no expedition time or horn coupling |

---

## 2. Exact formulas as found in source

### 2.0 Decennial opening window vs horn clock

| Clock | Canon duration | Where | Companion |
|-------|----------------|-------|-----------|
| **Opening window** | **100 days / 2400 hours** | Owner lock + Matrix of Oblivion | Session tracks Opening hours toward Horn/seal |
| **Horn / point of no return** | **1200 hours / day 50** | Owner lock; `hornRule`; `HORN_AT = 1200` | **Wired** — primary Session PoNR deadline |
| **Soft quit** | Floor 50 Canticle | Codex / Chronicle | Morale turn-back — **≠** Horn |

**One clock with a milestone:** Opening **2400 h**; Horn at **1200 h / day 50**. Soft quit at Floor 50 Canticle is separate. See [`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md). Early **240/120** drafts were a typo (corrected 2026-07-31).

---

### 2.1 Horn clock (canon)

**Source:** `src/data/dungeon-mechanics.json` (`hornRule`), mirrored in `src/data/floor-encounters.json`

```
At 1200 hours (day 50 of the 2400-hour Opening) → horn sounds (PoNR).
Retreat or risk 10 years trapped until the next Cycle.
Soft quit at Floor 50 Canticle ≠ Horn.
```

**Session implementation:** `src/components/SessionTracker.tsx`

```typescript
const HORN_AT = 1200; // day 50 PoNR; Opening = 2400 h
hoursLeft = max(0, HORN_AT - hours);
hornProgress = min(100, (hours / HORN_AT) * 100);
```

**Time advances (Director defaults — `docs/mechanics/SESSION_LOOP.md`, `WORLD_DUNGEON_LOOP.md`):**

| Action | Horn Δ | Source |
|---|---:|---|
| Manual +1h / exploration tick | +1 h | Session UI |
| Long rest | +8 h | Session UI + `applyLongRest()` |
| Short rest | 0 h | Session UI |
| Advance +8h (narrative skip, not rest) | +8 h | Session UI |

There is **no rulebook formula** for “+1 h per exploration segment” — that is a **companion GM convention** documented in playtest scenarios.

---

### 2.2 Expedition structure (canon ingest — not a math equation)

**Source:** `src/data/dungeon-mechanics.json` → `expedition`

```
maxSize = 12
teams: Combat (4–6), Reconnaissance (1–3), Research (1–3), Resource (2–4), Support (1–3)
timePeriods: ["morning", "afternoon", "evening"]
```

**Not encoded:** how many hours each period costs, how off-rotation teams affect combat budget, or research/tradeskill throughput. Session assumes **combat table only** (`SESSION_LOOP.md` § Gaps).

---

### 2.3 Combat EV loop (draft — balance sim)

**Sources:** `scripts/combat-balance-sim.mjs`, `src/lib/monster-combat.mjs`, `docs/mechanics/MONSTER_COMBAT_SCHEMA.md`

**Hit chance (d20 model):**

```
hitChance(attackBonus, targetAC) = clamp(0.05, 0.95, (21 - (targetAC - attackBonus)) / 20)
```

**Party output:**

```
partyHP = Σ memberHP
partyDPR = Σ (attackCount × averageDamage × hitChance) per member
roundsToWin = ceil(foeHP / max(partyDPR, 0.1))
```

**Monster incoming (structured combat):**

```
atWillDPR = sustainedAttackDpr(combat, partyAC, hitChance)
rechargeDPR = expectedRechargeDpr(...)   // draft cadence; see below
incomingDPR = atWillDPR + rechargeDPR
expectedLoss = incomingDPR × roundsToWin
EV_loss_pct = (expectedLoss / partyHP) × 100
```

**Recharge availability (`monster-combat.mjs`):**

```
P(recharge ready) = (dieSides - minimumRoll + 1) / dieSides
// e.g. recharge 5–6 on d6 → 2/6 ≈ 0.33 per round (steady-state draft)
```

**Save recharge damage:** 55% fail → full damage; success → half (`saveFailRate = 0.55`).

**Verdict bands (sim only — `combat-balance-sim.mjs`):**

| EV_loss_pct | Label |
|---:|---|
| ≥ 100% | TOO HOT (likely TPK) |
| ≥ 70% | very hard |
| ≥ 40% | hard but survivable |
| < 40% | moderate |

All marked **draft — not final balance**.

---

### 2.4 Encounter XP budget (draft — not canon awards)

**Source:** `src/lib/xp-economy.js`, `docs/mechanics/XP_ADVANCEMENT_CANON.md`

```
thresholdGap = CANON_XP_THRESHOLDS[level+1] - CANON_XP_THRESHOLDS[level]
totalBudget = round(thresholdGap × multiplier)
perCharacterTarget = floor(totalBudget / partySize)

multipliers: easy 0.5 | medium 1.0 | hard 1.5 | deadly 2.0
```

Example at avg party level 3: L3→L4 gap = **1,800 XP**; medium budget = **1,800 total** → **450 XP per PC** in a 4-PC party.

**CR → XP (draft table):** `draftXpForCr(cr)` — see `DRAFT_CR_XP_TABLE` in `xp-economy.js`. CR 21+ = `33000 + 5000 × (CR - 20)`.

**Party split:** `perMember = floor(totalXp / participantCount)`; remainder discarded.

---

### 2.5 Rest / Resonance economy (canon Hybrid-B + Session defaults)

**Source:** `src/data/resonance-economy.js`, `src/lib/session-utils.ts`

**Spell cost (Weave casters):**

```
cost = max(0, spellLevel × 2 - affinity + opposition + reputationMod - specialization)
cantrips = 0 RP
```

**Short rest (retune):**

```
RP_gain = round(maxRp / 4) + castingMod + retuneRepBonus
Oracle RC: +1 to max (cap 7)
Horn: 0 h
```

**Long rest:**

```
RP = maxRp; Oracle RC = maxRevelationCharges(level)
Horn: +8 h
```

These govern **how many fights fit between long rests**, which indirectly feeds the horn clock.

---

### 2.6 Gate boss / tier stubs (placeholder — not encounter math)

**Source:** `src/lib/session-utils.ts`

```
gateBossStubHp(tier) = 40 + tier × 25
```

Tier bands: 10 floors each, gate boss per tier (`dungeon-mechanics.json` `gateBosses[]`). **No tier-pressure formula** (e.g. “deeper = +X% encounter rate”) exists in data.

---

### 2.7 Playtest scenario time tables (architect draft — not rulebook)

These are **scenario-specific budgets** used by expedition sims; cite the scenario, not the rulebook.

**Fringe delve (`docs/playtest/EXPEDITION_SCENARIO.md`):**

| Activity | Hours |
|---|---:|
| Approach + survey | 2 |
| Combat (clear + bind) | 1 |
| Short rest | 0 |
| Long rest | 8 |
| Extraction | 2 |
| **On-site budget** | **16 h** (contract recall; **not** the 120 h trap) |

**T4 architect scenario (`docs/playtest/T4_EXPEDITION_SCENARIO.md`):**

| Activity | Hours |
|---|---:|
| Survey + company split | 2 |
| Combat | 2 |
| Short rest | 0 |
| Long rest | 8 |
| Sun-shard harvest | 4 |
| Obelisk puzzle | 2 |
| Radiance Gate install | 1 |
| Extraction | 4 |
| **T4 on-site budget** | **72 h** (example micro-budget within the Opening; not the Horn PoNR) |

**T4 sim actual (`docs/playtest/T4_EXPEDITION_PLAY_REPORT.md`):** ended **106 / 120 h** under the **pre-purge** Session UI (historical archive). Live canon Horn is **1200 h / day 50**.

---

## 3. Plain-language explanation for GMs / sim runners

Think of a Decennium delve as **four linked layers**, not one hidden formula:

0. **Opening window (macro):** When the Shardspire activates, the descent stays open **100 days (2400 h)** before sealing ([`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md)).

1. **Horn clock (hard canon — PoNR):** At **1200 hours / day 50** the Cycle horn sounds. Every **long rest costs 8 hours** on that clock. Miss the ascent and accept the **10-year trap** (`dungeon-mechanics.json`). Soft quit at Floor 50 Canticle ≠ Horn. The companion tracks this in Session; it does not auto-penalize overrun.

2. **Action economy clock (table + scenario):** Combats, travel, puzzles, harvest, and camp each cost **hours the GM assigns**. Playtest scenarios publish **example tables**; the rulebook does not give a universal “1 fight = X hours” law. Short rests **do not** tick the horn in Session; long rests **do**.

3. **Combat sustainability clock (draft math):** For planning, the sim uses **expected value (EV)**: if enemy damage × expected fight length ≥ party HP, the fight is probably too hot for that rest state. Use this to decide whether another long rest is mandatory before the next gate push.

**Radiance Gate (T4)** is a **fiction gate**, not math: three charged sun-shard vials in recesses at dawn’s zenith (`floor-encounters.json` F40 POI). Failure = blinding surge; no DC or hour formula in data.

**Expedition teams** mean **not all 12 PCs fight at once** — but the companion does not yet enforce who is on the combat track vs research/resource. GMs split narratively; sims should document assumptions (e.g. “8 PCs in combat company, 2 research off-clock”).

---

## 4. How this should drive sim systems

### Travel time

- **Canon anchor:** Horn PoNR at **1200 h / day 50**; Opening **2400 h**; long rest **+8 h**.
- **Sim default:** adopt scenario table or define per-tier bands (e.g. T1 mapped transit 16 h montage in `T4_EXPEDITION_SCENARIO.md`).
- **Rule:** `hornRemaining = 1200 - Σ(activityHours)`; flag when `hornRemaining < plannedActivities`.

### Camp

- **Canon:** safe havens per tier in `floor-encounters.json`; long rest = +8 h horn + full RP/RC.
- **Sim default (T4 architect):** camp build **6 h**, three-watch night, failed watch **+2 h** + wandering foe (`T4_EXPEDITION_SCENARIO.md` §5).
- **Attrition:** supply tables (sun-shields, rations) are **scenario content**, not engine formulas — but they **must** affect combat (Umbrin Sunlight Sensitivity in radiant zones per `UMBRIN_LORE.md`).

### Combat budget

- **Planning:** `draftEncounterBudget(avgLevel, difficulty, partySize)` for XP pacing (`xp-economy.js`).
- **Survivability:** EV loop §2.3 — stop stacking fights when `EV_loss_pct` cumulatively exceeds ~70% without long rest.
- **Gate bosses:** use bestiary when authored; Session stub `40 + tier×25` HP only for quick adds.

### Tradeskills

- **Data:** `crafting-recipes.json` — recipes have **Required Skill Level** (ingested as `skillLevel`).
- **Gap:** no rule ties crafting to horn hours or expedition periods. **Sim convention:** Resource team off-rotation PCs may craft during **evening** blocks; charge **2–4 h** per significant craft unless scenario says otherwise.

### Research

- **Data:** `dungeon-mechanics.json` Research team (1–3 seats).
- **Gap:** no research throughput formula. **Sim convention:** Mirror Guild / Research team activities cost **2–4 h** per POI (identify artifact, reconcile map fragment); success may **reduce** later encounter hours (e.g. −2 h harvest if map complete — `T4_EXPEDITION_SCENARIO.md` E0 fail-forward).

---

## 5. Closest canonical systems (since “hidden equation” is absent)

| System | Status | Use for sims? |
|---|---|---|
| **100 d / 2400 h opening window** | Owner lock; Matrix; Session Opening track | **Macro** — Cycle seal pressure; [`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md) |
| **1200 h / day 50 Horn PoNR + 10-year trap** | `hornRule` + `HORN_AT = 1200` | **Yes — primary Opening PoNR deadline** |
| **Expedition 12 / five teams / three periods** | Rulebook ingest, unwired | **Narrative split only** |
| **EV combat loop** | Draft sim | **Yes — fight pacing & TPK guard** |
| **draftEncounterBudget / draftXpForCr** | Draft helpers | **Yes — label draft XP** |
| **Resonance rest economy** | Canon + Session | **Yes — long rest vs horn tradeoff** |
| **Scenario hour tables** | Playtest architect | **Yes — per-scenario, cite file** |
| **Radiance Gate / tier gates** | Lore POI | **Fiction checks, not formulas** |
| **Tradeskills ↔ dungeon time** | **Missing** | GM fiat or scenario table |
| **Research throughput** | **Missing** | GM fiat or scenario table |

---

## 6. Recommended composite for expedition sims (synthetic — not author canon)

Until an owner publishes a true “dungeon equation,” sim runners may use this **checklist inequality**:

```
120 ≥ Σ(travelHours + combatHours + puzzleHours + harvestHours + campHours + craftHours + researchHours)
   where each longRest ⊂ campHours includes +8 horn internally

AND for each combat block:
   cumulative EV_loss_pct since last longRest < ~70% (draft threshold)

AND for XP pacing (draft):
   Σ draftXpForCr(encounter) ≲ draftEncounterBudget(partyLevel, difficulty).totalBudget × numEncounters
```

Label any run using this block **“synthetic sim constraint”** in play reports.

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Hidden-equation search (playtest subdivision) |
| **Date** | 2026-07-30 |
| **Deliverable** | `docs/playtest/HIDDEN_DUNGEON_EQUATION.md` |
| **Primary sources** | `dungeon-mechanics.json`, `floor-encounters.json`, `SessionTracker.tsx`, `session-utils.ts`, `monster-combat.mjs`, `combat-balance-sim.mjs`, `xp-economy.js`, `resonance-economy.js`, `SESSION_LOOP.md`, `WORLD_DUNGEON_LOOP.md`, `T4_EXPEDITION_SCENARIO.md`, `T4_EXPEDITION_PLAY_REPORT.md`, [`DESCENT_WINDOW_CANON.md`](../mechanics/DESCENT_WINDOW_CANON.md) |
| **Opening vs horn** | **2400 h / 100 d** Opening; Horn PoNR **1200 h / day 50**; soft quit Floor 50 Canticle ≠ Horn — see §2.0 |
| **No commit/push** | Per brief |
