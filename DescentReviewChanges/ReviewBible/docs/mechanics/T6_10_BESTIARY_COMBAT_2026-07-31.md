# T6–10 bestiary combat trust — 2026-07-31

**Status:** complete (Excel + ingest refreshed; no commit)  
**Workspace:** `DecenniumDescent-main`  
**Continuity:** Player/Director zone+seal ladder honored; no Silent Ones inventing on monster sheets; lore renames preserved (Excel stays pre-scrub; ingest renames on read). T1–5 trusted set left intact. Opening clocks not touched.

---

## Goal

Raise **bestiary combat trust for Tier 6–10** (floors 51–100): freeze Gate Guardians at lore CR 22/24/26/28/30, trust zone+CR trash, then reduce remaining sandbox debt with **quality band trust** (in-band Size vs CR only — not garbage rush).

Prior stamp: [`T1_5_BESTIARY_COMBAT_2026-07-31.md`](./T1_5_BESTIARY_COMBAT_2026-07-31.md) (159 trusted; T1–5 guardians frozen).

---

## Selection rule (Director bible)

| Tier | Floors | Canonical zone | Excel zone aliases included | CR cap (seal) |
|------|--------|----------------|-----------------------------|---------------|
| 6 | 51–60 | Crossroads of the Shattered Thread | Crossroads…, **Planar Crossroads** | ≤ 22 (Lumen) |
| 7 | 61–70 | Pactbound Arena | Pactbound Arena | ≤ 24 (Xarog) |
| 8 | 71–80 | Duskshard Pools | Duskshard Pools, **Shardpools** | ≤ 26 (Eirfax) |
| 9 | 81–90 | Veiled Iron Spiral | Veiled Iron Spiral, **Veiled Expanse** | ≤ 28 (Threxus) |
| 10 | 91–100 | Silencebound Void | Silencebound Void, **Boundless Void** | ≤ 30 (Marquis) |

Rows in those zones with **CR above the seal cap** stay draft (`NeedsReview` flagged `t610-over-cap`).

**Zone note:** Null Zones / surface Aethel\* / Resonance Fields not aliased into T6–10. Clear aliases normalized where safe (Planar Crossroads → Crossroads…; Shardpools → Duskshard Pools; Veiled Expanse → Veiled Iron Spiral; Boundless Void → Silencebound Void).

---

## Counts (post-ingest)

| Metric | Count |
|--------|------:|
| Excel `Monsters` rows | **708** (−1 hidden Ul'nath) |
| Live JSON (`src/bestiary_data_full.json`) | **707** |
| **Trusted `draft: false`** | **696** |
| — Gate Guardians all tiers (`gate-guardian-trusted`) | **10** |
| — T1–5 zone trash (`t1-5-trusted`) | **154** |
| — T6–10 zone trash (`t6-10-trusted`) | **102** (103 Excel; Ul'nath skipped) |
| — Remaining in-band sandbox (`band-trusted`) | **430** |
| Remaining sandbox / draft | **11** |
| Over-cap in T6–10 zones (still draft) | **4** |

### T6–10 zone set by tier (Excel selected = guardians + in-cap trash)

| Tier | Selected |
|------|---------:|
| T6 | 6 |
| T7 | 1 (Xarog only — no Excel trash in Pactbound Arena) |
| T8 | 30 |
| T9 | 43 |
| T10 | 28 |
| **Total** | **108** |

---

## Gate Guardians (T6–10) — frozen trusted

| Name | Type | Size | Align | Zone | CR | XP | AC | HP | Attacks | Provenance |
|------|------|------|-------|------|----|----|----|----|---------|------------|
| Lumen of the Shattered Thread | Elemental | Large | Chaotic Neutral | Crossroads of the Shattered Thread | 22 | 41000 | 19 | 528 | Thread Lance, Thread Bind, Thread Shatter (R) | `gate-guardian-trusted-2026-07-31` |
| Xarog, the Pactbound Furnace | **Fiend** | Huge | Lawful Evil | Pactbound Arena | 24 | 62000 | 19 | 764 | Pact Claw, Oath Brand, Inferno Pact (R) | same — Elemental-flavored leftovers replaced |
| Eirfax, the Dusk Crowned | Fey | Medium | Neutral Evil | Duskshard Pools | 26 | 90000 | 21 | 412 | Dusk Blade, Mirror Crown, Crown of Dusk (R) | same — lore Size Medium retained |
| Threxus, the Iron Spiral | Construct | Gargantuan | Lawful Neutral | Veiled Iron Spiral | 28 | 120000 | 20 | 1105 | Spiral Strike, Coil Crush, Iron Vortex (R) | same |
| The Marquis of Silence | Fiend | Huge | Chaotic Evil | Silencebound Void | 30 | 155000 | 21 | 944 | Silent Decree, Hush Rend, Zone of Silence (R) | same — hush/fear Traits only; **no Silent Ones spoilers** |

JSON: `combat.draft = false`, `combat.source = gate-guardian-trusted`.

**T1–5 guardians** remain frozen (Vaskor / Bloom / Ashthirst / Gor Vekk / Choralith) — not rewritten this pass.

---

## Trash + remaining sandbox

- **T6–10 zone trash:** type-flavored CR-band attacks; provenance `t6-10-trusted-2026-07-31` → JSON `source: t6-10-trusted`, `draft: false`.
- **Band trust (remaining):** Size within 1 step of CR floor + usable Type → type-flavored combat; provenance `band-trusted-2026-07-31`. Out-of-band Size/CR garbage left draft (11).
- Metadata QA on T6–10 set: Size snaps (≥2 steps), Alignment fill, zone alias normalize, culture/archetype Type floors (canonical lore name; Excel Name pre-scrub).
- HP/AC floors preserved when already above regenerated band.
- Spoiler-name rows: combat shell only; no Old Ones / Silent Ones sheet lore.

### Remaining draft (11)

Over-cap T6–10 (4): Fire Giant (Planar Crossroads CR 30), Hush-Broker Manyclaw / Pixie / Xvart Warlock… (Shardpools CR 27–29).  
Out-of-band Size (7): e.g. Cow Large @ CR 1/4, several Medium @ CR 1/4 vs Tiny floor, etc.

---

## Backups

- `backups/Bestiary_pre_t610_combat_20260731_081828.xlsx` (first run)
- Idempotent re-runs under `backups/Bestiary_pre_t610_combat_*.xlsx`

---

## Scripts

| Script | Role |
|--------|------|
| `scripts/t6_10_bestiary_combat_trust.py` | Idempotent T6–10 guardian freeze + zone trash + band debt pass |
| `scripts/ingest_bestiary_from_excel.py` | Honors `gate-guardian-trusted` / `t6-10-trusted` / `t1-5-trusted` / `band-trusted` → `draft: false` |

```bash
python scripts/t6_10_bestiary_combat_trust.py
npm run ingest:bestiary
```

### Ingest confirmation (final)

```
excel_rows 708
json_rows 707
skipped_hidden 1
with_combat_attacks 707
trusted draft=false: 696
  gate-guardian-trusted: 10
  t1-5-trusted: 154
  t6-10-trusted: 102
  band-trusted: 430
sandbox/draft remaining: 11
```

Idempotent re-run: `guardians=5 trash_upgraded=0 band_trusted=0`.

---

## Continuity checks

- No Silent Ones / Old Ones lore authored onto monster sheets (Marquis Traits = hush/fear pressure only).
- Lore renames not wiped (Excel pre-scrub Names retained; companion JSON scrubbed on ingest).
- Gate Guardian CR ladder T6–10 unchanged (22 / 24 / 26 / 28 / 30); Xarog remains **Fiend**.
- T1–5 trusted combat preserved.
- Horn/Opening clocks not reintroduced as 240/120.

**Todos:** Excel upgraded · T6–10 guardians frozen · band debt reduced · ingest done · stamp written · no commit.
