# Bestiary ingest — Excel → companion JSON

**Workflow:** Edit `Bestiary.xlsx` → `python scripts/ingest_bestiary_from_excel.py` → refresh app

*(Or: `npm run ingest:bestiary`)*

**Date:** 2026-07-30 (Excel-first consolidation — single canonical workbook)

**Owner workflow:** Pull out **`Bestiary.xlsx`**, edit/submit in Excel, re-ingest. Companion JSON (`src/bestiary_data_full.json`) is a **build artifact** — do not hand-edit combat there.

---

## Source workbooks

| Asset | Path | Role |
|-------|------|------|
| **Canonical authoring workbook** | `DecenniumDescent-main/Bestiary.xlsx` | Identity, loot, metadata, and combat columns (708 rows, `Monsters` sheet) |
| **Metadata supplement (ingest only)** | `DecenniumDescent-main/bestiary_metadata_source.xlsx` | Backfills Size/Type/CR/XP/zones/tier drops when primary cells are blank |
| Live JSON | `src/bestiary_data_full.json` | Loaded by `MonstersLibrary.tsx`, Session handoff, crafting cross-refs |
| Ingest script | `scripts/ingest_bestiary_from_excel.py` | Rebuilds JSON from Excel; `--xlsx PATH` override |
| Combat generator | `scripts/generate_bestiary_combat_sandbox.py` | Optional: regenerate draft CR-band combat columns **in place** on `Bestiary.xlsx` |
| IP scrub | `scripts/scrub_bestiary_ip.py` | Idempotent Aethel renames applied on **read** via `rename_value()` |

The former combat-sandbox workbook was merged into `Bestiary.xlsx` and is no longer part of the repository.

Other xlsx sheets (Dashboard, Drops, category drop tabs, Crafting Materials, Drop Locations) support harvesting reference but are **not** merged into the live monster JSON by this pass.

---

## Row counts (2026-07-30 Excel-first pass)

| Stage | Count | Notes |
|-------|------:|-------|
| Primary `Bestiary.xlsx` `Monsters` rows | **708** | Names + loot + combat columns |
| Hidden (`Ul'nath, the Hollow Dream`) | **−1** | Filtered from product JSON |
| Merged authored gate guardians | **10** | Excel wins when combat cells populated; companion fallback when empty |
| Appended guardian not in Excel | **+1** | `Xarog, the Pactbound Furnace` |
| **Live JSON total** | **708** | **0 duplicate names** |

**Combat/stat coverage after consolidated ingest:**

| Metric | Count |
|--------|------:|
| With `armorClass` + `hitPoints` | **708** |
| With structured `combat.attacks` | **708** |
| `combat.source: excel-sandbox` (draft CR-band generated) | **698** |
| `combat.source: companion-authored draft` (gate guardians, Excel empty only) | **≤10** |
| With `lootTable` (Excel harvest JSON) | **10** |

---

## Column map — identity & loot (`Monsters` sheet)

| Excel column | JSON field | Source priority |
|--------------|------------|-----------------|
| `Name` | `name` | Primary → `rename_value()` IP scrub |
| `Size` | `size` | Primary, else supplement |
| `Type` | `type` | Primary, else supplement |
| `Tags` | `tags` | Primary, else supplement; gate guardians keep authored tags on merge |
| `Alignment` | `alignment` | Primary, else supplement |
| `Challenge` | `challengeRating` | Primary, else supplement; **gate guardians use authored CR/XP** |
| `XP` | `xp` | Primary, else supplement; **gate guardians use authored CR/XP** |
| `Zone Found` | `zoneFound` | Primary, else supplement |
| `Tier N Drop/Rate/Value` (N=1–6) | `loot.tierN` | Primary, else supplement |
| `Loot Table` | `lootTable` | Primary (Python literal or JSON array) |
| — | `description` | Excel `Description` if present, else generated; gate guardians keep authored text |
| — | `ingestSource` | `"Bestiary.xlsx:Monsters"` |

---

## Column map — combat/stat

Ingest scans headers case-insensitively on **`Bestiary.xlsx`**.

| Excel header | JSON field |
|--------------|------------|
| AC, Armor Class | `armorClass` |
| HP, Hit Points | `hitPoints` |
| Speed | `speed` |
| Attack1 Name/Bonus/Damage/Type | `combat.attacks[0]` (default at-will action) |
| Attack2 Name/Bonus/Damage/Type | `combat.attacks[1]` (optional secondary) |
| Multiattack | primary attack count |
| Save DC | `combat.saveDc` |
| Recharge Name / Kind / Bonus / Damage / Type / Save DC / Save Ability / Roll | optional `combat.attacks[]` entry with `usage: recharge` |
| Combat Provenance | drives `combat.source` |
| Resistances, Immunities, Condition Immunities | `combat.defenses.*` |
| NeedsReview | optional author QA notes (semicolon-separated; not ingested to JSON) |

All generator-produced combat sets `draft: true`, `source: "excel-sandbox"`.

**Regenerate draft combat columns:** `python scripts/generate_bestiary_combat_sandbox.py` (backs up `Bestiary.xlsx` to `backups/` first).

**Author recharge rows (gate guardians + CR samples):** `python scripts/author_recharge_attacks.py` (backs up first; use `--force` to overwrite).

---

## Metadata quality rules (Worker 2 draft — 2026-07-30)

`bestiary_metadata_source.xlsx` **does not** correct scrambled Size/Type/CR — it mirrors the same bad pairings. Do not rely on it for metadata fixes.

**Backup first:** copy `Bestiary.xlsx` to `backups/Bestiary_worker2_<stamp>.xlsx` before bulk edits.

**Size/CR garbage detection (draft heuristics):**

| Flag | Rule |
|------|------|
| `huge-at-low-cr` | Huge/Gargantuan while CR ≤ ¼ |
| `tiny-at-high-cr` | Tiny while CR ≥ 10 |
| `small-at-legendary-cr` | Small while CR ≥ 15 |
| `oversized-for-cr*` | Size ≥ 2 ranks above CR-band floor |
| `undersized-for-cr*` | Size ≥ 2 ranks below CR-band floor |
| `cr-suspect-high` | Size was undersized for listed CR — CR may be wrong; author confirm |
| `cr-suspect-low` | Huge at low CR — CR may be wrong; author confirm |

**CR-band size floor (draft, not SRD):** CR 0 → Tiny; ¼ → Small; 1 → Medium; 5 → Large; 11 → Huge; 20+ → Gargantuan.

**Auto-fix priority:**

1. **Never edit gate guardians** (10 named bosses) — ingest preserves authored CR/XP/combat.
2. Snap Size to CR-band floor when mismatch ≥ 2 ranks or `huge-at-low-cr` / `tiny-at-high-cr`.
3. Invalid/missing Type → `Monstrosity` (do not invent lore types).
4. Do **not** auto-change CR without author sign-off — set `NeedsReview` with `cr-suspect-*` instead.
5. Write all changes to `NeedsReview` (semicolon-separated).

**Low-CR HP tuning (L1–L3 sandbox, draft):** bump Excel `HP` only — do not regenerate guardian combat. Apply **max(% bump, CR floor)**:

| CR band | % bump | HP floor |
|---------|--------|----------|
| 0 | +35% | 8 |
| ⅛ | +30% | 10 |
| ¼ | +25% | 14 |
| ½ | +20% | 26 |
| 1 | +15% | 52 |
| 2 | +10% | 68 |
| 3 | +8% | 88 |

Helper script: `python scripts/worker2_bestiary_tune.py` (one-shot; backs up first).

---

## Authored override merge rules

When a live JSON entry has a `combat` payload (or is a gate guardian with HP > 1):

1. Build creature from `Bestiary.xlsx` + `bestiary_metadata_source.xlsx` supplement.
2. Merge with existing authored record:
   - **Excel wins** for scalar stats (AC, HP, speed, abilities) when Excel cells are populated.
   - **Excel wins** for `combat.attacks` when Excel attack cells are populated (including gate guardians).
   - **Companion fallback** for `combat.attacks` only when Excel attack cells are empty.
   - **Authored wins** for gate-guardian CR/XP, description, and tags.
   - **Excel wins** for `lootTable` when present.

Gate guardians: The Bloom That Hungers, Vaskor, Ashthirst, Choralith, Lumen, Threxus, Eirfax, Xarog, Gor Vekk, Marquis of Silence.

---

## Re-run ingest

```bash
cd DecenniumDescent-main
python scripts/ingest_bestiary_from_excel.py
# override: python scripts/ingest_bestiary_from_excel.py --xlsx path/to/copy.xlsx
node scripts/combat-balance-sim.mjs
```

After xlsx name edits, also run:

```bash
python scripts/scrub_bestiary_ip.py
python scripts/ingest_bestiary_from_excel.py
```

---

## Known data quality notes

- `Bestiary.xlsx` is scrubbed to current Aethel names. Ingest retains the rename map only as a defensive compatibility layer for older source values.
- `bestiary_metadata_source.xlsx` metadata may not match SRD expectations — author review is separate; **supplement mirrors primary garbage for Size/Type/CR** (Worker 2 confirmed 2026-07-30).
- Sandbox CR-band stats inherit metadata quality issues (wrong Size/Type/CR pairings produce odd AC/HP).
- Generic SRD creature labels (Owlbear, Behir, etc.) remain per `BESTIARY_SCRUB_LOG.md` out-of-scope pass.
- After Worker 2 pass: **320** size snaps, **233** low-CR HP floor bumps, **430** rows touched; **9** gate guardians skipped.

---

**CONTINUITY:** **`Bestiary.xlsx` is the single canonical authoring workbook** (identity + loot + combat + optional recharge columns). Ingest reads it by default; JSON is a build artifact. **708 rows** with draft combat columns consolidated from the retired sandbox. Gate guardians: Excel combat wins when populated; companion-authored combat is fallback only. **Worker 4 / 5 (2026-07-30):** Recharge columns + draft rows for 10 gate guardians and ~15 CR-band creatures; sim adds optional expected recharge DPR. **Worker 2 / 5 (2026-07-30):** Metadata QA rules + `NeedsReview` column; 320 size snaps to CR-band floor, 233 HP floor bumps (CR ≤ 3 sandbox tuning); backup `backups/Bestiary_worker2_20260730T170216Z.xlsx`; guardians untouched; sim sandbox avg party-loss 22.1% → 25.6% (CR 1/3 fights +1 round).
