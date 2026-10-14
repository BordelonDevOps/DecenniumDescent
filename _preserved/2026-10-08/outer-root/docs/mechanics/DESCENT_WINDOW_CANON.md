# Decennial opening window — canon stamp

**Status:** **Owner-locked canon** (2026-07-30; horn re-stamped round 2; **code + literature purge 2026-07-31**)  
**Scope:** How long the Great Descent stays **open for entry** once the Shardspire activates each Cycle, and when its horn/point-of-no-return falls inside that window

---

## 1. Canon

| Field | Value |
|-------|-------|
| **Opening duration** | **100 days** = **2400 hours** |
| **Horn / point of no return** | **1200 hours / day 50** (halfway through the Opening) |
| **Soft quit** | Floor 50 **Canticle** / Choralith seal — morale turn-back; **≠** Horn PoNR |
| **Event** | Decennial opening — the dungeon opens to mortal expeditions when the Shardspire activates (tenth year of the 10-year rotation) |
| **End state** | At the end of the opening window, the dungeon **seals**. Those still inside are not necessarily killed; they may be trapped until the **next decennial opening** |
| **Authority** | Product owner lock **2026-07-30** + **2026-07-31** confirmation: prior **240/120** framing was a typo |

### Provenance

| Status | Source | What it establishes |
|--------|--------|---------------------|
| **Owner lock** | Chat directive 2026-07-30; clock confirmation 2026-07-31 | **100 days / 2400 hours** Opening; Horn **1200 h / day 50** PoNR |
| **Matrix source (aligned)** | `The Decennium Descent and the Matrix of Oblivion.docx` — § "The 2400-Hour Descent (100 Days)" | Finite opening, seal at end |
| **Extract (aligned)** | `docs/playtest/MATRIX_OF_OBLIVION_EXTRACT.md` | Same prose with **2400 h / 100 days** |
| **Companion wired** | `SessionTracker.tsx` `HORN_AT = 1200`; `hornRule` in dungeon/floor JSON | Session countdown matches Opening PoNR |

---

## 2. One clock, one milestone

> Opening: **2400 hours / 100 days**. Horn sounds at **1200 hours / day 50** = **point of no return**. Soft quit at Floor 50 Canticle is separate.

| Clock | Duration | Status |
|-------|----------|--------|
| **Decennial opening window** | **2400 h / 100 days** | Live canon |
| **Horn / point of no return** | **1200 h / day 50** | Live canon — halfway milestone; retreat-or-be-trapped-until-next-Cycle |
| **Soft quit** | Floor 50 Canticle | Morale / expedition end line — **not** a calendar hour |

**Continuity stamp only:** early drafts briefly used **240/120**; that was a typo. Correct values are **2400/1200**. See [`DIRECTOR_BIBLE_CLOCK_TYPO_FIX_2026-07-31.md`](./DESCENT_WINDOW_CANON.md) and [`OPENING_CLOCK_PURGE_2026-07-31.md`](./DESCENT_WINDOW_CANON.md).

**Do not:**
- Treat historical playtest logs that ran under a pre-purge **120 h** Session UI as live teaching formulas — those are dated archives.
- Invent additional Opening sub-clocks beyond the day-50 Horn milestone.

---

## 3. Continuity actions

| Item | Action |
|------|--------|
| Matrix extract + source `.docx` | **Aligned** — 2400 h |
| Companion code / JSON / ingest | **Purged 2026-07-31** — `HORN_AT = 1200`, `hornRule` → 1200 / day 50 |
| Soft quit vs Horn | Documented as distinct |

---

## 4. Related docs

| File | Role |
|------|------|
| [`WORLD_DUNGEON_LOOP.md`](./WORLD_DUNGEON_LOOP.md) | GM wiring — horn, tiers, Cycle frame |
| [`SESSION_LOOP.md`](./SESSION_LOOP.md) | Session horn tick rules (+8 h long rest) |
| [`OPENING_CLOCK_PURGE_2026-07-31.md`](./DESCENT_WINDOW_CANON.md) | End-to-end purge stamp + false-positive list |
| [`DIRECTOR_BIBLE_CLOCK_TYPO_FIX_2026-07-31.md`](./DESCENT_WINDOW_CANON.md) | Single typo-correction continuity stamp |
| [`CANON_CORE.md`](../canon/CANON_CORE.md) | Round 2 owner lock Q4 |
| [`src/data/dungeon-mechanics.json`](../../src/data/dungeon-mechanics.json) | Horn + Cycle data |

*Stamp updated 2026-07-31 — no commit/push per brief.*
