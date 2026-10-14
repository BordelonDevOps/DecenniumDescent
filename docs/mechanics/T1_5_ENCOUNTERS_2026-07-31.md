# T1–5 encounters operational toolkit — stamp

**Date:** 2026-07-31  
**Workspace:** `DecenniumDescent-main`  
**Owner ask:** Build Tier 1–5 encounter operational toolkit (cards / rosters / EV budgets); inventory existing; align bible zones & Gate ladder; lore-scrubbed names; no inventing XP economy; backup before large JSON rewrites; no commit.  
**Scope owned:** Encounter ops only — not crafting JSON, not Player Rulebook Appendix B, no wholesale bible overwrite.

---

## 1. Inventory (what already existed)

| Asset | Finding |
|-------|---------|
| `src/data/floor-encounters.json` | T1–5 **mapped** with zone prose, havens, POIs, live Guardian bosses; T6–10 `mapped: false` stubs; `hornRule` already 1200/2400 |
| Director bible Part VII (Ashen Bell) | Complete ready-to-run **Tier 1** Opening → Vaskor; compact Director keys F4–9 |
| Director bible Ch 15 / 16 / 29 | **EV** formulas + pressure bands + **eight-actor** rule + encounter jobs/levers |
| Director bible Part IX Ch 58–62 | Tier ops purposes, core pressures, revelation ceilings, gate prep |
| `Instruments_of_the_Weave.md` Part X | d12 pressure tables T1–5 |
| `GeneratorsPanel.tsx` | Sparks only — not full roster budgets |
| `MonstersLibrary` / `bestiary_data_full.json` | Guardians present with lore-pass CR/Type; trash fauna often sandbox CR/`zoneFound` |
| Prior companion | Encounters browser = havens/POIs/boss only — **no** EV cards/rosters |

---

## 2. Tier → floor map used

Aligned to Complete Director Edition + `floor-encounters.json` + `dungeon-mechanics.json` Gate ladder:

| Tier | Floors | Zone | Guardian (Type / Size / CR / Align) | Seal floor |
|-----:|--------|------|--------------------------------------|----------:|
| 1 | 1–10 | Yieldheart Caverns | Vaskor, the Stone Maw — Elemental / Huge / **8** / N | 10 |
| 2 | 11–20 | Bloomdeep Marsh | The Bloom That Hungers — Plant / Huge / **11** / CE | 20 |
| 3 | 21–30 | Anvil of Brogi | Ashthirst the Hollow — Elemental / Huge / **14** / NE | 30 |
| 4 | 31–40 | Isles of Eternal Radiance | Gor Vekk, Architect of Ends — Aberration / Large / **17** / LE | 40 |
| 5 | 41–50 | Sanctum of Echoing Choirs | Choralith, Voice Below — Aberration / Large / **20** / N | 50 |

Note: Floor 3 **Warded Gate** ends automaton patrol; it is **not** Vaskor’s seal (F10).

Canon locks respected: Opening **2400** / Horn **1200**; Expedition max **12**; Umbrin not Drow; no SWTOR; live Guardian names only.

---

## 3. Budget decision (XP vs EV)

Per [`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md): XP **thresholds** confirmed; **awards / CR→XP / encounter XP budgets BLOCKED**.

**Toolkit choice:** threat / EV budgets only — bible Ch 15 incoming-pressure % of party HP + Ch 29 bands + Ch 16 eight-actor. Bestiary Guardian `xp` fields recorded as **non-award metadata** only. No second XP economy invented.

---

## 4. What shipped

| Path | Role |
|------|------|
| `src/data/t1-5-encounter-toolkit.json` | Ingestable T1–5 cards (38), sample rosters (16), EV guidance, Guardian ladder, inventory block |
| `scripts/t1-5-encounter-toolkit.json` | Mirror |
| `scripts/_build_t1_5_encounter_toolkit.py` | Regenerator for the JSON |
| `docs/manuals/T1_5_Encounter_Operational_Toolkit.md` | Director-facing digest |
| `docs/mechanics/T1_5_ENCOUNTERS_2026-07-31.md` | This stamp |
| `src/data/floor-encounters.json` (+ `scripts/` sync) | Pointer `operationalToolkit` + note (narrative tiers unchanged) |
| `src/components/EncountersBrowser.tsx` | Light UI panel for T1–5 toolkit cards/rosters/Guardian CR |
| `backups/t1_5_encounters_20260731_080035/` | Pre-edit backup of floor-encounters JSON |

Did **not** edit Player Rulebook, crafting JSON, or the Director bible `.docx`.

---

## 5. Gaps left

1. **Room-by-room** T2–5 keys still thinner than Ashen Bell F4–9 (cards + ops chapters, not full adventure text).  
2. Excel **NeedsReview** Type/CR/`zoneFound` for trash fauna — roster picks use scrubbed names + `intendedCrBand` / Ch 17 reskin notes.  
3. Gate Guardian **combat metadata freeze** + Session HP from real blocks (still draft combat).  
4. **XP awards** owner decision still open.  
5. **T6–10** intentionally out of scope (`mapped: false`).  
6. Generators still do not auto-roll full EV-budgeted encounters from this JSON.

---

## 6. Continuity

- Opened Continuity SoT + XP canon + lore-pass Guardian ladder + bible EV/eight-actor extracts.  
- No silent overwrite of published rulebook/DM `.docx`.  
- Conflict check: none — toolkit mirrors bible procedure and does not claim XP awards.
