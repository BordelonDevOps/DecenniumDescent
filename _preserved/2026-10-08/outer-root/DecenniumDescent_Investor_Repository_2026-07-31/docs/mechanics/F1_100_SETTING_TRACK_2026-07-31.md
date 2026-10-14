# F1–100 Setting / Chronicle / Deep Gazetteer — continuity track

**Date:** 2026-07-31  
**Task force:** Floor 1–100 · Setting / Chronicle / deep gazetteer  
**Scope this stamp:** Director-facing **Floors 51–100 / T6–10** geographic & campaign guidance  
**Workspace:** `DecenniumDescent-main`  
**Commit:** none (brief)

---

## 1. Deliverable

| Artifact | Path | Role |
|----------|------|------|
| **Director deep gazetteer** | [`docs/manuals/F51_100_Director_Deep_Gazetteer.md`](../manuals/F51_100_Director_Deep_Gazetteer.md) | Primary fill — tone, factions, travel, seal, Horn, public/secret per deep tier + Interstice + Q6 staging |
| **This track stamp** | `docs/mechanics/F1_100_SETTING_TRACK_2026-07-31.md` | Inventory, gaps closed/open, coordination |
| **Chronicle (GZ-01)** | `docs/manuals/Chronicle_of_the_Decennial_Opening.md` | Surgical link: T6–10 status → digest; Interstice stub pointer |
| **DM-01 bible** | `docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx` | **No large rewrite** — already contains Ch 31, 34, 63–68; extract used as authority |

---

## 2. Inventory — what existed before this pass

| Source | T6–10 / Interstice coverage | Gap |
|--------|----------------------------|-----|
| **DM-01** Ch 8 geography blurbs | Named zones, guardians, landmarks | Ops detail lives in later chapters |
| **DM-01** Ch 31 | Civilization line; T6 last stable depth; T7–10 exceptional | — |
| **DM-01** Ch 34 / 65 | Old God Interstice forms, limits, consequences | Not mirrored in Chronicle as its own gazetteer entry |
| **DM-01** Ch 63–68 | Full ops: purpose, pressures, revelation ceilings, gate prep, sample seeds | Chronicle still labeled **survivor-rumor stub** only |
| **Chronicle** Part VII T6–10 | Principle, thin culture, 3 seeds, rumor havens, Director boxes | Explicitly "until author ingest"; no Interstice section; Appendix B Mapped = **rumor** |
| **Instruments** T6–10 d8 | Compressed pressure tables | Not geographic digest |
| **floor-encounters.json** | Zone names, draft POIs, guardians, landmarks | `mapped: false` — **leave** (coordinate: no large rewrite) |
| **OWNER / SILENT_ONES / DESCENT_WINDOW** | Authorship, Horn 2400/1200, Q6 open | Peace trigger still open |
| **EXPEDITION_STRUCTURE_CANON** | 12-person RAW | Deep ops must not invent 24-PC RAW |
| **T1–5 package** | Mapped encounters + toolkit | T6–10 product stance deferred for combat/encounters |

---

## 3. Gaps closed this pass

| Gap | Disposition |
|-----|-------------|
| Chronicle/bible product felt "rumor-only" for T6–10 | Closed via Director digest synthesizing DM-01 ops + Chronicle seeds + locks |
| No single Director sheet for tone/factions/travel/seal/Horn/layers | Closed in `F51_100_Director_Deep_Gazetteer.md` |
| Interstice stub missing from gazetteer lineup | Closed as dedicated digest section (not a floor band) |
| Level 97 temptation to invent | Explicitly **Q6 OPEN** with safe staging notes only |
| Horn confusion in deep tiers | Restated: 1200 PoNR · 2400 seal · soft quit ≠ Horn |

---

## 4. Gaps still open (do not invent)

| ID | Question | Authority |
|----|----------|-----------|
| **Q6** | Level 97 Old God — identity, relation to Silent Ones/Heartcell/Interstice, whether to author F97 room | OWNER lock; WDL-4; SILENT_ONES §4.5 |
| **Peace trigger** | What counts as "world knows peace" | SILENT_ONES §4.4 |
| **Q-OV-2** | Expedition 12 RAW vs T4 24-PC sims | CONTINUITY_SOURCE_OF_TRUTH §5 |
| **T6–10 mapped encounters** | Full POI/haven/encounter ingest | Deferred — JSON stays `mapped: false` |
| **T6–10 Guardian combat freeze** | Combat trust | Out of scope (lore-pass / draft) |
| **DM-01 .docx surgical sync** | Whether Word needs Interstice/gazetteer cross-links | Optional owner — MD digest + extract already sufficient for agents |

---

## 5. Zones covered (this digest)

| Zone | Floors | Guardian / note |
|------|--------|-----------------|
| Crossroads of the Shattered Thread | 51–60 | Lumen of the Shattered Thread |
| Pactbound Arena | 61–70 | Xarog, the Pactbound Furnace |
| Old God Interstice | between T7–T8 | Not a Guardian; campaign threshold |
| Duskshard Pools | 71–80 | Eirfax, the Dusk Crowned |
| Veiled Iron Spiral | 81–90 | Threxus, the Iron Spiral |
| Silencebound Void | 91–100 | The Marquis of Silence |
| Level 97 (myth only) | — | **Q6 open** — staging notes only |

---

## 6. Coordination / do-not-touch

- **No commit / push**  
- **No Player Rulebook** Silent Ones / Heartcell / Q6 writes  
- **No large rewrite** of `floor-encounters.json` or bestiary xlsx  
- **No Unity / 3D** work  
- Bible `.docx` left intact (authority already present; MD digest is the fill)

---

## 7. Related stamps

| Doc | Relation |
|-----|----------|
| `T1_5_RULES_PACKAGE_2026-07-31.md` | T1–5 done; T6–10 defer OK for encounters |
| `T1_5_ENCOUNTERS_2026-07-31.md` | Confirms T6–10 `mapped: false` |
| `DESCENT_WINDOW_CANON.md` | 2400 / 1200 |
| `SILENT_ONES_CANON.md` | Secret stratum + Q6 |
| `BOOK_LINEUP.md` | DM-01 + GZ-01 Chronicle |

*Track stamped 2026-07-31.*
