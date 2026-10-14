# Expedition scenario — Isles of Eternal Radiance (T4)

**Playtest ID:** `EXP-T4-01`  
**Tier band:** T4 — **Isles of Eternal Radiance** (floors 31–40)  
**Format:** 3 allied companies × 8 seats (24 PCs) · good/neutral ethos only · manual table + Session companion  
**Status:** Scenario Architect deliverable — **draft combat stats** from Excel ingest (`combat.source: excel-sandbox`) + companion-authored gate boss draft

---

## 1. Expedition brief

### Setting

**World:** Aethel — the Great Descent beneath the Shardspire.  
**Staging:** **Crystalfront Market (Outside)** at the Yieldheart cavern mouth ([`floor-encounters.json`](../../src/data/floor-encounters.json) T1 safe haven) — contract muster, sun-shard vial purchase, and Automaton clearance before the combined descent.  
**Operating zone:** **Isles of Eternal Radiance** (T4, floors 31–40): floating sunstone islets, crystal bridges, radiant mist sea, light-forged patrols. POIs used in this ladder: **Prismatic Archipelago (F31)**, **Radiant Bloom Gardens (F32)**, **Mirror Reef (F34)**, **Sunforged Obelisk (F36)**, safe havens **Sunward Terrace (F33)** and **Dawn's Refuge (F37)**, and the **Radiance Gate (F40)**.

This is a **Crystalfront-staged, T4-operating** expedition: surface logistics at the familiar market plaza; danger and horn pressure begin once the allied companies pass the Lavaflow Gate (T3) and transit into the radiant archipelago.

### Goal

**Primary:** Harvest and charge **three sun-shard vials** from the Radiant Bloom Gardens, align the **Sunforged Obelisk** glyph-rings, and install the vials at the **Radiance Gate** recesses at dawn's zenith — opening a **calibration window** for Cycle cartographers without triggering the gate's blinding failure surge.

**Secondary:** Recover a **prism-map slate** lost by a prior Journeyman company on Mirror Reef (lore handoff for Floor Encounters / cartography playtest).

### Stakes

- **Success:** Combined companies secure the calibration window; Tyrnathar-aligned guilds pay triple contract and grant T4 safe-pass sigils (narrative; no loot automation).
- **Failure:** A rival **Architect cult** completes its own gate ritual; the Radiance Gate floods the chamber with blinding radiance and the slate is lost for another Cycle.
- **Collateral:** Each **long rest** underground advances the **120-hour horn clock**; exceeding budget without retreat risks the Decennium trap ([`dungeon-mechanics.json`](../../src/data/dungeon-mechanics.json)).

### Alignment gate

**Good and neutral PCs only.** No evil-aligned characters on the roster. Umbrin and other stigmatized ancestries may appear as **neutral-good or lawful-neutral** allies (exile oaths, contract binders) — not as cult saboteurs.

---

## 2. Timeline assumptions

### Surface approach (pre-horn)

| Activity | Hours | Notes |
|---|---:|---|
| Muster at Crystalfront Market | 4 | Contracts, vial purchase, Company A/B/C assignment |
| Descent transit T1→T3 (mapped) | 16 | Narrative skip or montage; Automaton clearance through Yieldheart; no scripted combat |
| Lavaflow Gate key ritual (T3) | 2 | Skill challenge; failure costs 4h and 1d6 exhaustion (table) |
| **Subtotal before T4 horn start** | **22** | Track separately or zero Session horn at T4 entry |

**Director default:** Set Session **horn clock to 0h** when the first company sets foot on **Prismatic Archipelago (F31)** unless the table wants full descent continuity.

### On-site T4 operations (horn clock active)

| Activity | Hours |
|---|---:|
| Initial survey + company split | 2 |
| Each **combat encounter** (clear + field triage) | 2 |
| **Short rest** (retune) | 0 |
| **Long rest** (+8h in Session) | 8 |
| Sun-shard harvest (Radiant Bloom Gardens) | 4 |
| Obelisk alignment puzzle | 2 |
| Radiance Gate installation window | 1 |
| Extraction march to Sunward Terrace / surface recall | 4 |

**Budget:** **72 hours** on T4 (floors 31–40) before the table treats the **120-hour** rulebook horn as imminent — leaves ~48h buffer if the expedition entered T4 at horn 0h with prior transit untracked. Track in Session; **Advance +8h** only for narrative skips that are *not* long rests.

Exceeding **120h total underground** triggers the rulebook consequence: retreat or risk the **10-year trap** ([`SESSION_LOOP.md`](../mechanics/SESSION_LOOP.md)).

### Recommended in-fiction duration

**4–5 table days** on T4: two long rests maximum (Sunward Terrace, Dawn's Refuge) if the ladder is run complete.

---

## 3. Allied companies (24 seats)

Each company is **8 seats** — one PC per seat. Uniform level band **L8–L10** (see [`T4_ROSTER.md`](./T4_ROSTER.md)); pick one level per company or one level for the whole expedition before play.

| Company | Call sign | Role emphasis | Default camp duty |
|---|---|---|---|
| **A** | **Dawn Concord** | Vanguard — bridge assault, obelisk escort | First watch, breach drills |
| **B** | **Mirror Guild** | Recon + research — Mirror Reef, obelisk glyphs, slate recovery | Second watch, forage/scry |
| **C** | **Choir Covenant** | Support — healing, resonance tuning, gate ritual | Third watch, cook/maintain |

**Command:** Rotating **Expedition Marshal** (one player per day) resolves cross-company disputes; **Choir Covenant** Cleric/Paladin holds **medical triage** authority.

**Split vs. combined:** Encounters 1–2 may split by company; Encounters 3–6 assume **combined 24-PC** availability unless casualties remove seats.

---

## 4. Encounter ladder

All foes are from `Bestiary.xlsx` → `src/bestiary_data_full.json`, **`zoneFound: Radiant Isles`**. Stats below are ingested; **`combat.draft: true`** — validate at table. Scale counts for 24 PCs at L8–L10; adjust if running fewer seats live.

### Encounter 0 — Crystalfront muster (non-combat)

**Scene:** Bronze Automatons at the plaza gates; merchants hawk sun-shard kits.  
**Beat:** Companies receive conflicting map fragments; **Mirror Guild** must reconcile before descent.  
**Fail forward:** Missing fragment adds 2h to E2 harvest.

---

### Encounter 1 — Shifting bridges (Prismatic Archipelago, F31)

**Scene:** Six sunstone islets; crystal bridges change angle every 2 rounds. **Dawn Concord** leads crossing while others anchor ropes.

| Foe | Qty | CR | XP each | AC | HP | Speed |
|---|---:|---:|---:|---:|---:|---|
| **Ogre Battering Ram** | 6 | 4 | 1,100 | 14 | 75 | 40 ft. |

**At-will**

| Action | To hit | Damage |
|---|---|---|
| **Monstrous Claw** (action, 1 target) | +6 | 2d6+3 slashing |

**Recharge:** none.

**Draft encounter XP:** 6,600 total.

---

### Encounter 2 — Garden wardens (Radiant Bloom Gardens, F32)

**Scene:** Dawn-glow flower terraces; three vials must be filled while patrollers circle. Companies may split 8/8/8 across terraces.

| Foe | Qty | CR | XP each | AC | HP | Speed |
|---|---:|---:|---:|---:|---:|---|
| **Allip** | 4 | 5 | 1,800 | 15 | 95 | 40 ft. |
| **Otyugh** | 2 | 5 | 1,800 | 15 | 95 | 40 ft. |

**At-will (both types)**

| Action | To hit | Damage |
|---|---|---|
| **Monstrous Claw** (action, 1 target) | +6 | 2d8+4 slashing |
| **Tail Lash** (action, 1 target) | +6 | 2d8+3 bludgeoning |

**Recharge:** none.

**Draft encounter XP:** 10,800 total.

---

### Encounter 3 — Mirror doubles (Mirror Reef, F34)

**Scene:** Liquid-crystal lagoon; illusory doubles of PCs emerge. **Mirror Guild** leads; radiant damage resistance from Garden tonic (optional narrative buff) suggested.

| Foe | Qty | CR | XP each | AC | HP | Speed |
|---|---:|---:|---:|---:|---:|---|
| **Cloaker** | 4 | 10 | 5,900 | 17 | 172 | 40 ft. |

**At-will**

| Action | To hit | Damage |
|---|---|---|
| **Freak Bite** (action, 1 target) | +8 | 2d10+6 piercing |
| **Tail Lash** (action, 1 target) | +8 | 2d10+5 bludgeoning |

**Recharge:** none.

**Draft encounter XP:** 23,600 total.

---

### Encounter 4 — Obelisk sentinels (Sunforged Obelisk, F36)

**Scene:** Glyph-rings must align during combat; one round of puzzle progress per sentinel destroyed.

| Foe | Qty | CR | XP each | AC | HP | Speed |
|---|---:|---:|---:|---:|---:|---|
| **Knight** | 6 | 7 | 2,900 | 15 | 123 | 40 ft. |

**At-will**

| Action | To hit | Damage |
|---|---|---|
| **Monstrous Claw** (action, 1 target) | +7 | 2d8+5 slashing (×2 attacks) |
| **Tail Lash** (action, 1 target) | +7 | 2d8+4 bludgeoning |

**Recharge:** none.

**Draft encounter XP:** 17,400 total.

---

### Encounter 5 — Refuge breach (Dawn's Refuge approach, F37)

**Scene:** Architect cultists drive light-forged brutes toward the hollow spire; **Choir Covenant** must hold the pool while injured PCs from E3–E4 recover.

| Foe | Qty | CR | XP each | AC | HP | Speed |
|---|---:|---:|---:|---:|---:|---|
| **Oni** | 2 | 8 | 3,900 | 16 | 142 | 40 ft. |
| **Depth Toad Taskmaster** | 3 | 7 | 2,900 | 15 | 123 | 40 ft. |

**At-will — Oni**

| Action | To hit | Damage |
|---|---|---|
| **Monstrous Claw** (action, 1 target) | +7 | 2d10+5 slashing (×2) |
| **Tail Lash** (action, 1 target) | +7 | 2d10+4 bludgeoning |

**At-will — Depth Toad Taskmaster**

| Action | To hit | Damage |
|---|---|---|
| **Freak Bite** (action, 1 target) | +7 | 2d8+5 piercing (×2) |
| **Tail Lash** (action, 1 target) | +7 | 2d8+4 bludgeoning |

**Recharge:** none.

**Draft encounter XP:** 16,500 total.

---

### Encounter 6 — Gate-adjacent: Architect's projection (Radiance Gate, F40)

**Scene:** **Not a full gate-boss kill.** As the three vials seat, **Gor Vekk, Architect of Ends** manifests a **projection** — gate-adjacent threat only. Defeating the projection or surviving **3 rounds** while the calibration completes wins; the true boss (CR 29) does not enter melee at full stat block unless the table explicitly escalates.

| Foe | Qty | CR | XP (listed) | AC | HP | Speed |
|---|---:|---:|---:|---:|---:|---|
| **Gor Vekk, Architect of Ends** (projection) | 1 | 29† | 135,000† | 23 | 400 | 50 ft., fly 120 ft. |

†Listed bestiary values; **playtest default:** use **200 HP projection** (same AC/attacks) or run as **skill/ritual race** — 3 rounds to complete vial install while projection acts.

**At-will** (`combat.source: companion-authored draft`)

| Action | To hit | Damage |
|---|---|---|
| **Reality Sunder** (action, 1 target, ×3 attacks) | +14 | 3d12+7 force |

**Recharge (5–6)**

| Action | Save | Damage |
|---|---|---|
| **End Architecture** (action, area) | DC 22 Intelligence, half on success | 9d8 force |

**Draft encounter XP:** 135,000 listed — **do not auto-award**; Director awards narrative milestone XP or split a fixed 5,000 draft XP pool if the projection is reduced.

---

**Full ladder draft XP (E1–E5 foes defeated, excluding E6 projection):** 74,900 total → **≈3,120 XP per PC** if split 24 ways (Session **Award draft XP** only; not canon — see [`XP_ADVANCEMENT_CANON.md`](../mechanics/XP_ADVANCEMENT_CANON.md)).

---

## 5. Camp, building, and logistics beats

### Safe havens

| Haven | Floor | Use in this scenario |
|---|---|---|
| **Sunward Terrace** | 33 | First long rest after E2; sun-shard vial refill; heat-fatigue treatment |
| **Dawn's Refuge** | 37 | Second long rest after E4; liquid-light pool clears exhaustion; gate prep |

### Watch rotations

Three companies → **three-watch night** (4 PCs awake per watch). Roll or assign:

| Watch | Hours (8h rest block) | Default company |
|---|---|---|
| First | 0–2h | Dawn Concord |
| Second | 2–5h | Mirror Guild |
| Third | 5–8h | Choir Covenant |

**Failed perception on watch:** Roll wandering threat — one **Allip** (CR 5) or cult scout encounter; +2h horn.

### Forage and supply

- **Radiant Bloom Gardens:** Harvest grants 3 vials + 1d4 tonic doses (resist radiant 1 hour) — requires E2 clear.
- **Sunward Terrace cistern:** Unlimited water; no food unless brought from Crystalfront.
- **Rations budget:** 5 days × 24 PCs = 120 person-days; **Resource team** (2 PCs per company off-rotation) tracks consumption; shortfall imposes exhaustion on failed Forage/Survival (DC 14).

### Social beats

- **Crystalfront muster (E0):** Umbrin PCs face merchant side-eye — roleplay neutral-good contract binders.
- **Sunward Terrace (camp 1):** Debate whether to push for gate or retreat with partial maps.
- **Dawn's Refuge (camp 2):** Architect cult parley offer (false truce); **Choir Covenant** mediates.

### Injury and recovery

- **Field triage:** Choir Covenant sets **stabilization order**; Session tracks HP only — no death-save automation ([`COMBAT_SYSTEM_COMPARE.md`](../mechanics/COMBAT_SYSTEM_COMPARE.md)).
- **Liquid-light pool (Dawn's Refuge):** Narrative: clear 1 level of exhaustion + minor burns; once per PC per expedition.
- **Casualty threshold:** **3+ PCs dead** (not stabilized before next long rest) triggers **forced retreat** fail condition unless Marshal calls combined retreat vote.

---

## 6. Success metrics

### Primary success

- Three **sun-shard vials** installed at **Radiance Gate** at dawn's zenith.
- **Calibration window** held for 3 rounds (E6 complete).
- **≥18 of 24 PCs** exit T4 conscious to Sunward Terrace or surface recall.
- **Horn clock ≤ 120h** underground at extraction.

### Partial success

- Gate calibrated but **horn 72h+ on T4 alone** or **6+ PCs** dead/unrecovered — guild pays standard rate; slate lost.

### Fail

Any of:

- **TPK** or **<12 conscious PCs** at extraction.
- **Vials destroyed** (E6 End Architecture wipes uninstalled vials on round 3+ failure).
- **Horn 120h exceeded** without agreed retreat.
- **Architect cult** completes rival ritual (E6 lasts 5+ rounds without projection damage).

### Playtest instrumentation (companion)

| Metric | How to capture |
|---|---|
| Encounter duration (rounds) | Session notes per E1–E6 |
| HP loss % per company | Session combatant HP track |
| Rest count vs. horn | Horn clock before/after long rests |
| RP/RC drain | Party Resonance card after each encounter |
| Player confusion | [`EXPEDITION_FRICTION_LOG.md`](./EXPEDITION_FRICTION_LOG.md) tags |
| Draft stat trust | DM marks `combat.draft` validated Y/N per foe |

---

## 7. Rules references

| Topic | Doc | Table note |
|---|---|---|
| **Resonance (RP)** | [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md) | Short rest = retune (~¼ max); long rest = full pool + 8h horn |
| **Oracle (RC)** | [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md) §6 | RC +1 on short rest (companion convenience) |
| **Horn clock** | [`SESSION_LOOP.md`](../mechanics/SESSION_LOOP.md) | 120h deadline; +8h on long rest |
| **Expedition teams** | [`dungeon-mechanics.json`](../../src/data/dungeon-mechanics.json) | 12-PC max rule superseded by this 24-PC playtest charter |
| **T4 zone data** | [`floor-encounters.json`](../../src/data/floor-encounters.json) | Isles of Eternal Radiance POIs + Radiance Gate |
| **Bestiary provenance** | [`BESTIARY_INGEST.md`](../mechanics/BESTIARY_INGEST.md) | Excel-sandbox; validate damage at table |
| **Roster** | [`T4_ROSTER.md`](./T4_ROSTER.md) | 24 PCs, L8–L10, good/neutral |

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Scenario Architect (playtest subdivision) |
| **Date** | 2026-07-30 |
| **Scope** | `docs/playtest/T4_EXPEDITION_SCENARIO.md` + `docs/playtest/T4_ROSTER.md` |
| **Sources** | `floor-encounters.json` (T1 Crystalfront, T4 Isles); `dungeon-mechanics.json`; `bestiary_data_full.json` (Radiant Isles); `SESSION_LOOP.md`; `RESONANCE_CANON.md`; `canon-classes.js` |
| **Combat** | Excel-sandbox + Gor Vekk companion-authored draft; gate-adjacent projection only |
| **Simulation** | **Not run** — roster + scenario only |
| **Git** | No commit/push |
