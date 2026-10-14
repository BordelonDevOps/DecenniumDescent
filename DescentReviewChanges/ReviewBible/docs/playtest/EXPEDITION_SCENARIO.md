# Expedition scenario — Blackglass Reach fringe

> **Historical rules snapshot:** This report preserves the terminology and mechanics used when the simulation was run. Current magic canon is [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md): RP + Dissonance/Refrain, no automatic alignment/reputation spell pricing, and Low Resonance instead of the retired Burnout subsystem. Historical observations remain useful, but superseded magic rulings are not current RAW.


**Playtest ID:** `EXP-BGR-01`  
**Tier band:** T1–T2 (surface fringe, not gate descent)  
**Format:** 3 encounters · non-boss · 4-seat party · manual table + Session companion  
**Status:** Scenario Architect deliverable — **draft combat stats** from Excel ingest (`combat.source: excel-sandbox`)

---

## 1. Expedition brief

### Setting

**Blackglass Reach** — the surface marches where dark-glass outcrops, Murk trade routes, and wary border watchposts meet the upper Aethel wilds ([`UMBRIN_LORE.md`](../mechanics/UMBRIN_LORE.md)). This delve is a **fringe sinkhole network** (“Glassbite Hollow”) one day's march from the nearest Reach watchpost. Cult scouts from the Murk have been seen marking the entrance.

### Goal

Recover a **Resonance Shard** — a fist-sized obsidian sliver humming with trapped First Song echo — from the hollow's collapsed inner vault before Murk cult agents extract it.

### Stakes

- **Success:** Watchpost Commander Rhal-Voss pays contract gold and grants a Reach safe-pass sigil (narrative; no loot automation).
- **Failure:** Cultists carry the shard toward Veyr-Obsid trade cells; the watchpost loses resonance-scrying coverage for the next tenday.
- **Collateral:** Loud fighting or a second long rest may draw a Murk patrol (DM optional add-on — not scripted here).

### Horn-clock pressure

This is a **short fringe delve**, not a full 120-hour gate descent. Treat horn clock as **operational time on site**:

| Activity | Hours |
|---|---:|
| Approach + initial survey | 2 |
| Each combat encounter (clear + bind wounds) | 1 |
| Each **Short rest** (retune) | 0 |
| Each **Long rest** (+8h in Session) | 8 |
| Extraction march | 2 |

**Budget:** **16 hours** on-site before the watchpost recall horn sounds (contract clause). Track in Session; use **Advance +8h** only for narrative time skips that are *not* long rests.

Exceeding 16h does not trigger the 120h → 10-year trap — that rule applies to deeper gate delves. Instead, the party must **retreat without the shard** or face arriving Murk reinforcements (fail condition).

---

## 2. Encounter list

All foes are **non–gate-guardian** entries from `Bestiary.xlsx` → `src/bestiary_data_full.json`. Stats below are Excel-ingested; **`combat.draft: true`** — validate at table.

### Encounter 1 — Glass thicket scouts

**Scene:** Obsidian-streaked briar at the hollow mouth. Two chitines drop from the glass canopy when the party crosses the marked stones.

| Foe | CR | XP (Bestiary) | AC | HP | Speed |
|---|---:|---:|---:|---:|---|
| **Chitine** ×2 | 1 | 200 each | 13 | 52 | 40 ft. |

**At-will**

| Action | To hit | Damage |
|---|---|---|
| **Freak Bite** (action, 1 target) | +4 | 1d8+2 piercing |

**Recharge:** none.

**Draft encounter XP:** 400 total (≈100 per PC if split four ways).

---

### Encounter 2 — Consort on the rope bridge

**Scene:** A swaying bridge of blackglass slats over a steam vent. An **Umbrin Favored Consort** — a house-bred war beast — blocks the path, handler already fled.

| Foe | CR | XP (Bestiary) | AC | HP | Speed |
|---|---:|---:|---:|---:|---|
| **Umbrin Favored Consort** ×1 | 2 | 450 | 13 | 68 | 40 ft. |

**At-will**

| Action | To hit | Damage |
|---|---|---|
| **Monstrous Claw** (action, 1 target) | +5 | 1d10+2 slashing |

**Recharge:** none.

**Draft encounter XP:** 450 total (≈112 per PC).

---

### Encounter 3 — Vault weaver

**Scene:** Collapsed vault chamber; the shard pulses on a cracked plinth. A **Gloom Weaver** — cult shadow-binder — is mid-ritual and turns as the party enters.

| Foe | CR | XP (Bestiary) | AC | HP | Speed |
|---|---:|---:|---:|---:|---|
| **Gloom Weaver** ×1 | 3 | 700 | 14 | 88 | 40 ft. |

**At-will**

| Action | To hit | Damage |
|---|---|---|
| **Freak Bite** (action, 1 target) | +5 | 2d6+2 piercing |

**Recharge (5–6)**

| Action | Save | Damage |
|---|---|---|
| **Shadow Weave** (action, area) | DC 13 Wisdom, half on success | 3d6 necrotic |

**Draft encounter XP:** 700 total (≈175 per PC).

---

**Full delve draft XP (all foes defeated, split 4 ways):** 1,550 total → **≈387 XP per PC** (hard band vs. L3→L4 gap per [`XP_ADVANCEMENT_CANON.md`](../mechanics/XP_ADVANCEMENT_CANON.md) draft budget sketch).

---

## 3. Party slots

Four seats. **Recommended level: L3 or L4** (party should be uniform — pick one before chargen). Race and class are **player choice**; player agents fill [`characters/`](./characters/) stubs.

| Slot | Persona file | Level | Notes |
|---|---|---:|---|
| **P1** | [`P1_NOVICE.md`](./characters/P1_NOVICE.md) | L3 or L4 | New to TTRPGs; needs clear prompts |
| **P2** | [`P2_CASUAL_5E.md`](./characters/P2_CASUAL_5E.md) | L3 or L4 | Casual 5e familiarity |
| **P3** | [`P3_PF_VETERAN.md`](./characters/P3_PF_VETERAN.md) | L3 or L4 | Pathfinder / 3.5 veteran |
| **P4** | [`P4_OPTIMIZER.md`](./characters/P4_OPTIMIZER.md) | L3 or L4 | Builds for efficiency |

**Chargen:** Companion **CHARACTERS** tab → save → **SESSION** tab → add combatants. See [`PLAYTEST_SMOKE.md`](../mechanics/PLAYTEST_SMOKE.md).

---

## 4. Rules references

Point players and DM to these **informational** docs — table resolves manually; Session tracks HP, RP/RC, horn, and draft XP tally only.

| Topic | Doc | Table note |
|---|---|---|
| **Resonance (RP)** | [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md) | One pool; cost = spell level × 2 ± modifiers; cantrips 0 RP. Short rest = retune (~¼ max); long rest = full pool + 8h horn. |
| **Hybrid-B multiclass** | [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md) §7 | Internal label only — **not player-facing UI**. Max RP = highest caster pool + 25% of one secondary pool (round up). |
| **Oracle (RC)** | [`RESONANCE_CANON.md`](../mechanics/RESONANCE_CANON.md) §6 | Oracles use **Revelation Charges**, not RP. Session grants RC +1 on short rest as companion convenience. |
| **Death saves** | [`COMBAT_SYSTEM_COMPARE.md`](../mechanics/COMBAT_SYSTEM_COMPARE.md) § HP and death | At 0 HP: unconscious; 3 successes = stable, 3 failures = dead. Massive damage ≥ max HP = instant death. **No automation in Session.** |
| **Draft XP awards** | [`XP_ADVANCEMENT_CANON.md`](../mechanics/XP_ADVANCEMENT_CANON.md) | Bestiary `xp` + draft CR table are **not canon**; Session **Award draft XP** is session-local only (no save write-back). Split evenly among participants (round down). |
| **Class ceiling caps** | [`CLASS_CEILING_CAPS.md`](../mechanics/CLASS_CEILING_CAPS.md) | Draft playtest guardrails for Mirrorsage, Oracle, Paladin, Warrior, Dragoon, Tinker — informational in Builder/Sheet; **not enforced** in Session. |
| **Session loop** | [`SESSION_LOOP.md`](../mechanics/SESSION_LOOP.md) | Initiative, rests, horn clock, handoff from Encounters tab. |
| **Bestiary provenance** | [`BESTIARY_INGEST.md`](../mechanics/BESTIARY_INGEST.md) | Excel-first; `combat.draft: true` on sandbox-generated columns. |

---

## 5. Success and fail conditions

### Success (primary)

Party **claims the Resonance Shard** and **exits Glassbite Hollow** with at least one conscious PC carrying it, within the **16-hour** on-site horn budget.

### Partial success

Shard recovered but horn budget exceeded **or** two+ PCs dead (not stabilized before extraction). Counts as win for combat data; narrative contract payment halved.

### Fail

Any of:

- **TPK** (no PC stabilizes before ritual completes).
- **Cult escape:** Gloom Weaver survives 3 rounds while holding the shard (ritual completes; cult agents flee via shadow).
- **Forced retreat:** Horn budget exceeded without shard secured.
- **Abandon contract:** Party leaves before Encounter 3 without DM-agreed alternate goal.

---

## Continuity stamp

| Field | Value |
|---|---|
| **Agent** | Scenario Architect (playtest subdivision) |
| **Date** | 2026-07-30 |
| **Scope** | `docs/playtest/EXPEDITION_SCENARIO.md` + four character stubs |
| **Sources** | `Bestiary.xlsx` ingest → `src/bestiary_data_full.json`; `UMBRIN_LORE.md`; `RESONANCE_CANON.md`; `XP_ADVANCEMENT_CANON.md`; `CLASS_CEILING_CAPS.md`; `SESSION_LOOP.md` |
| **Combat** | Excel-sandbox stats only; no gate guardians; no commit/push |
| **Open** | Player agents populate character stubs; DM validates draft damage at table |
