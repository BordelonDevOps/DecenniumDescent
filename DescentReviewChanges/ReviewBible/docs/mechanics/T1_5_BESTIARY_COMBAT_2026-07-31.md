# T1–5 bestiary combat trust — 2026-07-31

**Status:** complete (Excel + ingest refreshed; no commit)  
**Workspace:** `DecenniumDescent-main`  
**Continuity:** Player/Director zone+seal ladder honored; no Silent Ones inventing on monster sheets; lore renames preserved (Excel stays pre-scrub; ingest renames on read). Opening clocks not touched (2400/1200 already aligned).

---

## Goal

Raise **bestiary combat trust for Tier 1–5** so sandbox drafts are no longer a ship blocker for the T1–5 campaign slice. Freeze **Gate Guardians in the T1–5 band** as fully trusted.

---

## Selection rule (Director bible)

| Tier | Floors | Canonical zone | Excel zone aliases included | CR cap (seal) |
|------|--------|----------------|-----------------------------|---------------|
| 1 | 1–10 | Yieldheart Caverns | Yieldheart, Yieldheart Caverns | ≤ 8 (Vaskor) |
| 2 | 11–20 | Bloomdeep Marsh | Bloomdeep Marsh, Bloomdeep, **Aethel Swamps** | ≤ 11 (Bloom) |
| 3 | 21–30 | Anvil of Brogi | Anvil of Brogi, **Bastion of Flame** | ≤ 14 (Ashthirst) |
| 4 | 31–40 | Isles of Eternal Radiance | Isles…, Radiant Isles | ≤ 17 (Gor Vekk) |
| 5 | 41–50 | Sanctum of Echoing Choirs | Sanctum…, Choir Sanctum | ≤ 20 (Choralith) |

Rows in those zones with **CR above the seal cap** are **not** trusted (left draft; `NeedsReview` flagged `t15-over-cap`).

**Zone note:** Bastion of Flame / Aethel Swamps remain Excel zone strings (cosmology / surface aliases). Clear dungeon aliases normalized where safe: Yieldheart → Yieldheart Caverns; Radiant Isles → Isles of Eternal Radiance; Choir Sanctum → Sanctum of Echoing Choirs.

---

## Counts (post-ingest)

| Metric | Count |
|--------|------:|
| Excel `Monsters` rows | **708** (−1 hidden Ul'nath) |
| Live JSON (`src/bestiary_data_full.json`) | **707** |
| **Trusted `draft: false`** | **159** |
| — Gate Guardians T1–5 (`gate-guardian-trusted`) | **5** |
| — Zone+CR trash (`t1-5-trusted`) | **154** |
| Remaining sandbox / draft | **548** |
| Over-cap in T1–5 zones (still draft) | **15** |

### Trusted by tier

| Tier | Trusted creatures |
|------|------------------:|
| T1 | 25 |
| T2 | 30 |
| T3 | 40 |
| T4 | 43 |
| T5 | 21 |
| **Total** | **159** |

---

## Gate Guardians (T1–5) — frozen trusted

| Name | Type | Size | Align | Zone | CR | XP | AC | HP | Attacks | Provenance |
|------|------|------|-------|------|----|----|----|----|---------|------------|
| Vaskor, the Stone Maw | Elemental | Huge | Neutral | Yieldheart Caverns | 8 | 3900 | 17 | 284 | Stone Maw, Crushing Jaw, Seismic Roar (R) | `gate-guardian-trusted-2026-07-31` |
| The Bloom That Hungers | Plant | Huge | Chaotic Evil | Bloomdeep Marsh | 11 | 7200 | 15 | 374 | Vine Maw, Root Constrict, Spore Burst (R) | same |
| Ashthirst the Hollow | Elemental | Huge | Neutral Evil | Anvil of Brogi | 14 | 11500 | 16 | 464 | Ash Claw, Cinder Lash, Hollow Wail (R) | same |
| Gor Vekk, Architect of Ends | Aberration | Large | Lawful Evil | Isles of Eternal Radiance | **17** | 18000 | **19** | **416** | Reality Sunder, End Thesis, End Architecture (R) | same — **CR 17 seal budget** (not CR 29 leftover) |
| Choralith, Voice Below | Aberration | Large | Neutral | Sanctum of Echoing Choirs | 20 | 25000 | 19 | 483 | Resonant Lash, Echo Needle, Subsonic Chord (R) | same |

JSON: `combat.draft = false`, `combat.source = gate-guardian-trusted`.

**T6–10 guardians** (Lumen, Xarog, Eirfax, Threxus, Marquis) still `draft: true` / lore-pass provenance — **out of scope** for this stamp.

---

## Trash combat work

- Replaced sandbox / lore-pass generic Attack1/2 with **type-flavored** CR-band usable stats.
- Provenance: `t1-5-trusted-2026-07-31` → JSON `source: t1-5-trusted`, `draft: false`.
- Metadata QA on the set: Size snaps vs CR band, Alignment fill, zone alias normalize, culture/archetype Type floors (via canonical lore name; Excel Name stays pre-scrub).
- Collapsed scrub double-prefix garbage (`Fracture-Kin Fracture-Kin…`) when present in Excel Name.
- HP/AC floors preserved when already above regenerated band (Worker 2 bumps).

---

## Remaining sandbox debt (outside T1–5 trust)

| Debt | Approx | Notes |
|------|-------:|-------|
| Draft rows outside T1–5 set | **548** | Still `draft: true`; mostly `lore-pass-2026-07-30-attacks` |
| Over-cap in T1–5 zones | **15** | Wrong CR for zone (e.g. CR 23–30 in Bastion/Choir/Yieldheart); flagged `NeedsReview` |
| T6–10 Gate Guardians | **5** | Lore/CR locked earlier; combat trust **not** frozen this pass |
| Surface / non-dungeon zones | large | Aethel Forests/Caves/etc. untouched unless they matched T1–5 aliases |
| Type/Size garbage outside set | many | `bestiary_metadata_source.xlsx` still mirrors bad pairings; not auto-fixed outside T1–5 |

---

## Backups

- `backups/Bestiary_pre_t15_combat_20260731_080349.xlsx` (first run)
- Later re-runs under `backups/Bestiary_pre_t15_combat_*.xlsx` (idempotent)

---

## Scripts

| Script | Role |
|--------|------|
| `scripts/t1_5_bestiary_combat_trust.py` | Idempotent T1–5 combat + guardian freeze + metadata QA |
| `scripts/ingest_bestiary_from_excel.py` | Honors `trusted` provenance → `draft: false`; collapses repeated name prefixes; skips superseded JSON orphans |

```bash
python scripts/t1_5_bestiary_combat_trust.py
npm run ingest:bestiary
```

### Ingest confirmation (final)

```
excel_rows 708
json_rows 707
skipped_hidden 1
with_combat_attacks 707
trusted draft=false: 159  (5 gate-guardian-trusted + 154 t1-5-trusted)
sandbox/draft remaining: 548
```

---

## Continuity checks

- No Silent Ones / Old Ones lore authored onto monster sheets.
- Lore renames not wiped (Excel pre-scrub Names retained; companion JSON still scrubbed on ingest).
- Gate Guardian CR ladder for T1–5 unchanged (8 / 11 / 14 / 17 / 20).
- Horn/Opening clocks not reintroduced as 240/120.

**Todos:** Excel upgraded · guardians frozen · ingest done · stamp written · no commit.
