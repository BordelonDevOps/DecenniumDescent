# XP and advancement provenance



**Status:** Thresholds **confirmed**; Opening-campaign awards = **milestone-only official** through **Tiers 1–10 / Floors 1–100** (2026-07-31). CR→XP companion helpers remain **optional / non-canon**.  

**Verified:** 2026-07-31  

**Stamps:** [`T1_5_RULES_PACKAGE_2026-07-31.md`](./T1_5_RULES_PACKAGE_2026-07-31.md) · [`F1_100_RULES_TRACK_2026-07-31.md`](./F1_100_RULES_TRACK_2026-07-31.md)



## Official Opening advancement (T1–10 / Floors 1–100)



| Layer | Ruling |

|-------|--------|

| **Opening campaigns** | **Milestone advancement is official** for the full Decennial Opening (Tiers 1–10 / Floors 1–100), including deep push past the Bar of Last Refuge / Canticle Gate. Director awards levels at Gate seals (through Marquis), major arc beats, the Old God Interstice crossing when used, or other milestones announced before the Opening begins. |

| **XP thresholds** | L1–L20 Character Advancement table remains **canon** for total level / proficiency and for tables that opt into XP tracking. |

| **Creature / encounter XP** | **Not published** in Player Rulebook or DM-01 at any depth. No CR→XP or encounter-budget table is rulebook canon. Depth does **not** unlock a creature-XP economy. |

| **Session UI** | CR→XP “Award” controls are **optional / non-canon** session tallies — never write-back to character saves; never presented as Opening law. |



**Sources:** Player Rulebook § Advancement in Opening Campaigns (2026-07-31 F1–100 pass); DM-01 “Treasure and awards” (Complete Director Edition).



## Confirmed rulebook canon — thresholds



### Advancement model



The editable primary source, `decennium descent player rulebook.docx`, Chapter 1 / **Beyond 1st Level** and **Character Advancement**, keeps the cumulative XP table. Opening campaigns use milestones; XP totals apply when the Director opts into XP tracking.



| Level | Total XP required | Proficiency bonus |

|---:|---:|---:|

| 1 | 0 | +2 |

| 2 | 300 | +2 |

| 3 | 900 | +2 |

| 4 | 2,700 | +2 |

| 5 | 6,500 | +3 |

| 6 | 14,000 | +3 |

| 7 | 23,000 | +3 |

| 8 | 34,000 | +3 |

| 9 | 48,000 | +4 |

| 10 | 64,000 | +4 |

| 11 | 85,000 | +4 |

| 12 | 100,000 | +4 |

| 13 | 120,000 | +5 |

| 14 | 140,000 | +5 |

| 15 | 165,000 | +5 |

| 16 | 195,000 | +5 |

| 17 | 225,000 | +6 |

| 18 | 265,000 | +6 |

| 19 | 305,000 | +6 |

| 20 | 355,000 | +6 |



On gaining a level, the rulebook grants one additional Hit Die and directs the player to their class description for features. Multiclassing: XP cost and proficiency use **total character level**.



### Provenance



| Status | Source | What it establishes |

|---|---|---|

| **Confirmed** | Player Rulebook Ch 1 | XP table + level-gain procedure |

| **Confirmed** | Player Rulebook multiclass | Total character level |

| **Confirmed 2026-07-31** | Player Rulebook + DM-01 | Opening T1–10 = milestone official; no published CR→XP |



## Not canon — companion draft helpers



The provisional CR→XP table in `src/lib/xp-economy.js` (`draft: true`) remains a **Director optional tool** only. It must stay labeled non-canon in Session UI.



### Proposed CR → XP award table (draft / optional)



| CR | XP (draft) | CR | XP (draft) |

|---:|---:|---:|---:|

| 0 | 10 | 11 | 7,200 |

| 1/8 | 25 | 12 | 8,400 |

| 1/4 | 50 | 13 | 10,000 |

| 1/2 | 100 | 14 | 11,500 |

| 1 | 200 | 15 | 13,000 |

| 2 | 450 | 16 | 15,000 |

| 3 | 700 | 17 | 18,000 |

| 4 | 1,100 | 18 | 20,000 |

| 5 | 1,800 | 19 | 22,000 |

| 6 | 2,300 | 20 | 25,000 |

| 7 | 2,900 | 21+ | 33,000 + 5,000 per CR above 20 |

| 8 | 3,900 | | |

| 9 | 5,000 | | |

| 10 | 5,900 | | |



Equal party split and encounter-budget sketches in `xp-economy.js` stay draft helpers — not Opening law.



## Companion wiring



| Layer | Status | Location |

|---|---|---|

| L1–L20 thresholds | **Wired** | `CANON_XP_THRESHOLDS` → Builder |

| Opening milestones | **Docs / books** | Player + DM-01; Session banner |

| CR→XP Session stub | **Optional non-canon** | Session foe defeat → scene notes + `draftXpSession` tally; **no save write-back** |



*Updated 2026-07-31 (F1–100 / T6–10 milestone extension) — no commit.*


