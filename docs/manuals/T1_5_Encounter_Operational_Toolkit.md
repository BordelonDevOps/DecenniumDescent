# Tier 1–5 Encounter Operational Toolkit

**Audience:** Directors running Floors 1–50  
**Stamped:** 2026-07-31  
**Ingest:** `src/data/t1-5-encounter-toolkit.json` (mirrored at `scripts/t1-5-encounter-toolkit.json`)  
**Continuity stamp:** [`../mechanics/T1_5_ENCOUNTERS_2026-07-31.md`](../mechanics/T1_5_ENCOUNTERS_2026-07-31.md)  
**Bible:** `The_Directors_Crucible_Complete_Director_Edition.docx` (Ch 15 EV, Ch 16 eight-actor, Ch 29 workflow, Part VII Ashen Bell, Part IX ops)

---

## How to use this (60 seconds)

1. Pick the **tier → floor** row below.  
2. Name the encounter’s **job** (Teaching / Taxing / Revealing / Choosing / Climactic / Pursuit).  
3. Budget with **EV pressure bands**, not XP.  
4. Cap **detailed initiative at ~8 actors**; abstract the rest with clocks / morale / off-map seats.  
5. Pull a **sample roster** from the JSON or Encounters tab toolkit panel; look up stats in Monsters Library (label sandbox combat).  
6. For Tier 1, prefer **Ashen Bell** keys in the bible over improvising F4–10.

**XP stance:** Awards remain **BLOCKED** (`XP_ADVANCEMENT_CANON.md`). Bestiary `xp` fields on Guardians are **not** table awards. Do not invent a second XP economy.

---

## Tier → floor map (bible + floor-encounters)

| Tier | Floors | Zone | Gate Guardian | Gate landmark |
|-----:|--------|------|---------------|---------------|
| 1 | 1–10 | Yieldheart Caverns | **Vaskor, the Stone Maw** (Elemental, Huge, CR 8, N) | Seal F10; Warded Gate F3 ends automaton patrol only |
| 2 | 11–20 | Bloomdeep Marsh | **The Bloom That Hungers** (Plant, Huge, CR 11, CE) | Sporemist Gate F20 |
| 3 | 21–30 | Anvil of Brogi | **Ashthirst the Hollow** (Elemental, Huge, CR 14, NE) | Lavaflow Gate F30 |
| 4 | 31–40 | Isles of Eternal Radiance | **Gor Vekk, Architect of Ends** (Aberration, Large, CR 17, LE) | Radiance Gate F40 |
| 5 | 41–50 | Sanctum of Echoing Choirs | **Choralith, Voice Below** (Aberration, Large, CR 20, N) | Canticle Gate F50; Bar of Last Refuge = soft quit ≠ Horn |

Opening **2400 h**; Horn PoNR **1200 h / day 50**. Expedition max **12**. Live Guardian names only. **Umbrin**, not Drow. No SWTOR.

---

## Threat / EV budgets (bible language)

**Core estimate (Ch 15)**

- Rounds ≈ foe total HP ÷ party DPR  
- Incoming pressure ≈ (foe DPR × foes) × rounds  
- Compare to party total HP

| Band | Incoming pressure vs party HP | Director reading |
|------|-------------------------------|------------------|
| Routine | &lt;20% | Teach / reveal / non-HP tax only |
| Standard | 20–40% | Win with visible cost |
| Hard | 40–65% | Drops possible; retreat required |
| Severe | 65–90% | Telegraph + leverage |
| Catastrophic | &gt;90% | Chosen risk / exits / non-damage win |

**Role pressure (Ch 29):** +1 band step if two or more uncountered control factors; −1 for surprise / chokepoint / researched vuln / real allies.

**Eight-actor rule (Ch 16):** ≤8 detailed initiative creatures. Abstract with reinforcement clocks, morale tracks, off-map seat checks. Waves need visible triggers.

| Tier | Default band | Note |
|-----:|--------------|------|
| 1 | Teaching→Standard | Seal Hard→Severe with Recognition |
| 2 | Standard | Contamination as non-HP tax |
| 3 | Standard→Hard | Stated machine cycles add free pressure if ignored |
| 4 | Hard | Shade/sun-shields are Resource budget |
| 5 | Hard→Severe | Wear + sound; Bar quit is honorable |

---

## What already existed (inventory)

| Asset | Role |
|-------|------|
| `src/data/floor-encounters.json` | Mapped T1–5 zones, havens, POIs, bosses; T6–10 stubs |
| Director bible Part VII | **Ashen Bell** full T1 Opening through Vaskor + F4–9 keys |
| Director bible Part IX Ch 58–62 | Tier ops purposes, pressures, revelation ceilings |
| `Instruments_of_the_Weave.md` Part X | d12 pressure tables |
| `GeneratorsPanel.tsx` | Name/hook/POI/loot sparks — thin encounter gen |
| `MonstersLibrary` + `bestiary_data_full.json` | Guardians tagged; trash fauna often sandbox CR/zone |

**Gap this toolkit closes:** executable cards / rosters / EV budgets for T1–5 so Directors are not inventing pressure from scratch.

---

## Sample roster highlights (lore-scrubbed names)

Full actor lists, levers, and cards live in JSON. Highlights:

- **T1:** Pact Automaton Sentinel *(reskin Deep Scion)*, Spiral Worm, Cave Bear, Umbrin Arachnid, Hookbeast *(scale CR — excel CR 0 is sandbox)*, Vaskor CR 8  
- **T2:** Giant Toad, Sporefolk Sprout/Adult, Banderhobb, Violet Fungus, Bloom CR 11  
- **T3:** Magma/Steam Mephit, Earth/Fire Elemental Myrmidon, Iron Cobra, Hellfire Engine, Ashthirst CR 14  
- **T4:** Lumen Drifter *(scrubbed)*, Slithering Tracker, Allip doubles, Cloaker, Gor Vekk CR 17  
- **T5:** Dust/Smoke Mephit, Voidmind, Gibbering Mouther *(treat as sound-horror)*, Choralith CR 20  

When excel Type/CR is absurd, use bible **Ch 17** reskin from a same-band template and keep the display name.

---

## Companion surface

- Encounters tab shows a **T1–5 Operational Toolkit** panel (cards + rosters + Guardian CR) when a mapped upper tier is selected.  
- `floor-encounters.json` points at `operationalToolkit: "t1-5-encounter-toolkit.json"`.

---

## Gaps left

- Per-floor **full keyed maps** beyond Ashen Bell F4–9 and POI seeds (T2–5 still card-density, not room-by-room).  
- Trash fauna **zoneFound / CR QA** in Excel (NeedsReview) still required for trusted auto-pick.  
- Guardian **combat freeze** + Session gate HP wiring.  
- XP awards (owner decision).  
- T6–10 remain rumor stubs (`mapped: false`).
