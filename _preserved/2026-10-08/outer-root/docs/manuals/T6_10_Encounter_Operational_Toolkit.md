# Tier 6–10 Encounter Operational Toolkit

**Audience:** Directors running Floors 51–100  
**Stamped:** 2026-07-31  
**Ingest:** `src/data/t6-10-encounter-toolkit.json` (mirrored at `scripts/t6-10-encounter-toolkit.json`)  
**Continuity stamp:** [`../mechanics/T6_10_ENCOUNTERS_2026-07-31.md`](../mechanics/T6_10_ENCOUNTERS_2026-07-31.md)  
**Bible:** `The_Directors_Crucible_Complete_Director_Edition.docx` (Ch 15 EV, Ch 16 eight-actor, Ch 29 workflow, Part IX Ch 63–68 ops, Ch 65 Old God Interstice)  
**Predecessor:** [`T1_5_Encounter_Operational_Toolkit.md`](./T1_5_Encounter_Operational_Toolkit.md)

---

## How to use this (60 seconds)

1. Pick the **tier → floor** row below.  
2. Name the encounter’s **job** (Teaching / Taxing / Revealing / Choosing / Climactic / HavenSiege / Interstice).  
3. Budget with **EV pressure bands**, not XP.  
4. Cap **detailed initiative at ~8 actors**; abstract the rest with clocks / morale / off-map seats.  
5. Pull a **sample roster** from the JSON or Encounters tab toolkit panel; look up stats in Monsters Library (label sandbox combat).  
6. Prefer **bible Ch 63–68** ops + sample floor seeds over inventing deep lore mid-session.

**XP stance:** Awards remain **BLOCKED** (`XP_ADVANCEMENT_CANON.md`). Milestone / narrative advancement assumed. Bestiary `xp` fields on Guardians are **not** table awards. Do not invent a second XP economy.

---

## Tier → floor map (bible + floor-encounters)

| Tier | Floors | Zone | Gate Guardian | Gate landmark |
|-----:|--------|------|---------------|---------------|
| 6 | 51–60 | Crossroads of the Shattered Thread | **Lumen of the Shattered Thread** (Elemental, Large, CR 22, CN) | Lumen Gate F60 — last normal civilization depth |
| 7 | 61–70 | Pactbound Arena | **Xarog, the Pactbound Furnace** (Fiend, Huge, CR 24, LE) | Furnace Gate F70; then optional **Old God Interstice** (not a Guardian) |
| 8 | 71–80 | Duskshard Pools | **Eirfax, the Dusk Crowned** (Fey, Medium, CR 26, NE) | Crown Gate F80 |
| 9 | 81–90 | Veiled Iron Spiral | **Threxus, the Iron Spiral** (Construct, Gargantuan, CR 28, LN) | Spiral Gate F90 |
| 10 | 91–100 | Silencebound Void | **The Marquis of Silence** (Fiend, Huge, CR 30, CE) | Marquis Gate F100 |

Opening **2400 h**; Horn PoNR **1200 h / day 50**. Expedition max **12**. Live Guardian names only. **Umbrin**, not Drow. No SWTOR. Silent Ones: **never name aloud**.

**Old God Interstice** (bible Ch 65): between T7 and T8 after Xarog — campaign-scale threshold, **not** Tier 7.5, **not** a Gate Guardian, **not** on the live roster.

---

## Threat / EV budgets (bible language)

Same method as T1–5 toolkit / Ch 15–16–29:

| Band | Incoming pressure vs party HP | Director reading |
|------|-------------------------------|------------------|
| Routine | &lt;20% | Teach / reveal / non-HP tax only |
| Standard | 20–40% | Win with visible cost |
| Hard | 40–65% | Drops possible; retreat required |
| Severe | 65–90% | Telegraph + leverage |
| Catastrophic | &gt;90% | Chosen risk / exits / non-damage win |

**Eight-actor rule:** ≤8 detailed initiative creatures.

| Tier | Default band | Note |
|-----:|--------------|------|
| 6 | Hard | Route/politics primary; seal Hard→Severe |
| 7 | Hard→Severe | Contest + term; Interstice = identity pressure |
| 8 | Severe | Delayed identity / reflections |
| 9 | Severe | False progress; circles empower Threxus |
| 10 | Severe→Catastrophic | Attractive stillness; multiple victory modes |

---

## What already existed (inventory)

| Asset | Role |
|-------|------|
| `src/data/floor-encounters.json` | T6–10 **draft** zones (`mapped: false`), havens, POIs, live bosses |
| Director bible Ch 63–68 | Tier ops purposes, pressures, revelation ceilings, gate prep, sample seeds |
| Director bible Ch 65 | Old God Interstice procedure |
| `Instruments_of_the_Weave.md` Part X | d8 compressed pressure tables T6–10 |
| T1–5 toolkit | Pattern this file mirrors |
| `bestiary_data_full.json` | Guardians CR 22/24/26/28/30 lore-pass; trash often sandbox |

**Gap this toolkit closes:** executable cards / rosters / EV budgets for T6–10 so Directors are not inventing deep pressure from draft stubs alone.

---

## Sample roster highlights (lore-scrubbed names)

Full actor lists, levers, and cards live in JSON. Highlights:

- **T6:** Thread Wraith *(Allip shell)*, Lantern Doubt Will-o', Void Broker, Umbrin Shadowblade, Shield Guardian, **Lumen CR 22**  
- **T7:** Pact Devil (White Court), Barbed Devil, Fracture-Kin Shadow Demon, Chain Devil, **Xarog CR 24**, Interstice Room With One History *(not a Guardian)*  
- **T8:** Slithering Tracker, reflection Allip doubles, Deathlock *(future-self shell)*, Yeth Hound, **Eirfax CR 26**  
- **T9:** Helmed Horror, Iron Cobra, Shield Guardian / Hellfire Engine *(siege timeline shells)*, **Threxus CR 28**  
- **T10:** Bodak *(sound-theft)*, Nightwalker *(void-lean shell)*, Voidmind, Fracture-Kin Shadow Demon, **Marquis CR 30**

When excel Type/CR is absurd, use bible **Ch 17** reskin from a same-band template and keep the display name. **Do not rewrite bestiary combat stats from this toolkit.**

---

## Companion surface

- Encounters tab shows a **T{n} Operational Toolkit** panel for tiers **1–10** (T1–5 JSON or T6–10 JSON by selection).  
- `floor-encounters.json` points at `operationalToolkit` (T1–5) and `operationalToolkitT6to10`.

---

## Gaps left

- T6–10 floors remain **draft-mapped** (`mapped: false`) — cards/ops density, not room-by-room keys.  
- Trash fauna **zoneFound / CR QA** still required for trusted auto-pick.  
- Guardian **combat freeze** + Session gate HP wiring (T6–10 still draft combat).  
- XP awards (owner decision).  
- Generators still do not auto-roll full EV-budgeted encounters from this JSON.  
- Old God Interstice needs table-specific scenario flesh beyond the Ch 65 seed.
