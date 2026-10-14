# Tranche A — Monster Manual Compilation Progress

**Tranche:** A — early / low-tier (Tier 1–2 · Floors 1–20 · lowest CR band)  
**Agent:** 4 of 5 (COMPILE)  
**Date:** 2026-08-04  
**Template:** Agent 3 `ENTRY_TEMPLATE.md` is authoritative (MM-01). Most Tranche A bodies are **Expedition-ready Field Briefs** with full tactics/ecology; section headers still use Agent 4’s interim layout and should be remapped to Identity / Provenance / Role vs Expedition / Harvest tables in a polish pass. **`spiral-worm.md`** was replaced with Agent 3’s `_EXAMPLE_ENTRY.md` (full template match).

## Counts

| Metric | Count |
|--------|------:|
| Creature entry files (excl. `_EXAMPLE_ENTRY`) | **28** |
| Minimum target | 15 |
| Stretch target | 25–40 |
| Dual-written | yes → `DescentReviewChanges/docs/bestiary/monster-manual/` |

## Checklist

| Done | Slug | Creature | Tier | CR | Notes |
|------|------|----------|------|----|-------|
| [x] | `vaskor-the-stone-maw` | Vaskor, the Stone Maw | T1 | 8 | Gate Guardian · seal F10 |
| [x] | `the-bloom-that-hungers` | The Bloom That Hungers | T2 | 11 | Gate Guardian · seal F20 |
| [x] | `spiral-worm` | Spiral Worm | T1 | 2 | Agent 3 example promoted to live entry |
| [x] | `umbrin-arachnid` | Umbrin Arachnid | T1 | 1 | Toolkit roster |
| [x] | `ferry-wraith-of-the-hush` | Ferry-Wraith of the Hush | T1 | 0 | Hush omen / low combat |
| [x] | `deep-dwarf` | Deep Dwarf | T1 | 2 | Claim politics |
| [x] | `deep-dwarf-kavalrachni` | Deep Dwarf Kavalrachni | T1 | 3 | Vertical cavalry |
| [x] | `deep-dwarf-xarrorn` | Deep Dwarf Xarrorn | T1 | 5 | War-caste |
| [x] | `deep-scion` | Deep Scion | T1 | 4 | Automaton reskin template |
| [x] | `pact-automaton-sentinel` | Pact Automaton Sentinel | T1 | 4* | Display entry · no native JSON row |
| [x] | `hookbeast` | Hookbeast | T1 | 0→3–4* | Toolkit matriarch scale note |
| [x] | `cave-bear` | Cave Bear | T1 | 2 | Toolkit roster |
| [x] | `crystal-shardling` | Crystal Shardling | T1 | 1/4 | Display name · Ochre Jelly stats |
| [x] | `dimetrodon` | Dimetrodon | T1 | 1/2 | Vein-basker fauna |
| [x] | `sporefolk-sprout` | Sporefolk Sprout | T2 | 1/2 | Toolkit swarm |
| [x] | `sporefolk-adult` | Sporefolk Adult | T2 | 14→6–8* | Scale honesty |
| [x] | `poison-skin` | Poison-Skin | T2 | 3 | Marsh enclave |
| [x] | `season-bound-winter` | Season-Bound Winter | T2 | 2 | Season-Bound family |
| [x] | `pact-devil-blue-court` | Pact Devil (Blue Court) | T2 | 2 | Pact Devil family |
| [x] | `voidmind-archivist` | Voidmind Archivist | T2 | 1/2 | Aberration clerk |
| [x] | `void-broker` | Void Broker | T2 | 6 | Hard late-marsh |
| [x] | `serpent-blood-broodguard` | Serpent-Blood Broodguard | T2 | 1/4 | Swarm nest guard |
| [x] | `umbrin-favored-consort` | Umbrin Favored Consort | T2 | 2 | Murk politics |
| [x] | `umbrin-shadowblade` | Umbrin Shadowblade | T1 | 7 | Late-T1 elite |
| [x] | `giant-constrictor-snake` | Giant Constrictor Snake | T2 | 1/4 | Size honesty flag |
| [x] | `order-drone-tetrad` | Order-Drone Tetrad | T1† | 1/4 | Adjacent construct lesson |
| [x] | `pact-devil-black-court` | Pact Devil (Black Court) | T1† | 1/2 | Still-water oaths |
| [x] | `umbrin` | Umbrin | T1–2 | 1/2 | Baseline Murk mortal |

† Sheet zone outside Yieldheart/Bloomdeep; included as early-tier / low-CR Aethel family support.

## Deferred / blockers

| Item | Why deferred |
|------|----------------|
| Unscrubbed compatibility names still in T1–2 trusted set (Orc, Centaur, Banshee, Imp, Hydra, Helmed Horror, …) | Not publication-cleared; thin Aethel lore; IP-prose risk |
| Native **Automaton** JSON row | Missing — MM documents Deep Scion reskin |
| Native **Crystal Shardling** / **Heartroot Tendril** rows | Toolkit display names only |
| Hookbeast / Sporefolk Adult excel CR | Documented scale notes; Excel untouched (MM layer only) |
| Giant Toad / Banderhobb / Violet Fungus toolkit names | Await scrub or Aethel rewrite |
| Main `src/bestiary_data_full.json` | Corrupt JSON — ReviewBible 707-row copy used |
| Naming collisions | Spiral Worm ≠ Iron Spiral ≠ Turning Spiral; Umbrin ≠ Drow; Ferry-Wraith ≠ Silent Ones |
| Template remapping | 27 entries need header remap to Agent 3 Identity/Provenance/Role tables |

## Sources

- ReviewBible `src/bestiary_data_full.json` (trusted combat)
- `src/data/floor-encounters.json`, `t1-5-encounter-toolkit.json`
- Codex of the Heartcell (Guardian lore; F10/F20 placement from gazetteer + combat trust)
- `UMBRIN_LORE.md`, `T1_5_BESTIARY_COMBAT_2026-07-31.md`, `BESTIARY_PUBLICATION_STATUS.md`
- Agent 2 inventory + Agent 3 MM-01 template/plan

## Dual-write

Entries + this progress file under `DescentReviewChanges/docs/bestiary/monster-manual/`. Live Excel/JSON bestiary **not** modified.
