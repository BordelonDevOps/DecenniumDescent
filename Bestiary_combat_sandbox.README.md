# Bestiary_combat_sandbox.xlsx — retired

**Canonical workbook:** [`Bestiary.xlsx`](./Bestiary.xlsx)

Combat columns (AC, HP, Speed, attacks, etc.) now live on the `Monsters` sheet of **`Bestiary.xlsx`**. Edit that file, then re-ingest:

```bash
python scripts/ingest_bestiary_from_excel.py
# or: npm run ingest:bestiary
```

The former `Bestiary_combat_sandbox.xlsx` was merged into `Bestiary.xlsx` on 2026-07-30. A backup may exist under `backups/`.

To regenerate draft CR-band combat columns in place:

```bash
python scripts/generate_bestiary_combat_sandbox.py
```

That script now writes combat columns directly into `Bestiary.xlsx` (with backup).
