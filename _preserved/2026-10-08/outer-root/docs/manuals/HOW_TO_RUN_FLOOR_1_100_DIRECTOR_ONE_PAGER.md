# How to run Floor 1–100 — Director one-pager

**Print / PDF:** Open this file → Print → Save as PDF (Letter, narrow margins).  
**Companion:** Session + Dungeon Guide + Encounters + Bestiary + Crafting tabs.  
**Canon books:** Player Rulebook + **DM-01** `The_Directors_Crucible_Complete_Director_Edition.docx`.  
**Date:** 2026-07-31 · Integration spine

---

## 1. Clocks (never compress)

| Clock | Value | Meaning |
|-------|------:|---------|
| **Opening** | **2400 h / 100 days** | Seal / end of Cycle window |
| **Horn PoNR** | **1200 h / day 50** | Retreat or 10-year trap |
| Soft quit | Floor 50 Canticle / Bar of Last Refuge | **≠ Horn** |

Session tracks Opening hours (`HORN_AT = 1200`). Fringe on-site budgets (e.g. 16 h) are scenario tools only.

---

## 2. Party structure

- **Expedition max 12** PCs · five teams · morning / afternoon / evening periods.  
- Larger forces = **coordinating Expeditions**, not one RAW roster of 24 (Q-OV-2 charter still optional).  
- Session zero: Resonance ≠ spell slots; Oracle = **RC**, Weave = **RP**.

---

## 3. Advancement

- Opening campaigns = **milestone-only** (Gate seals, major arc beats).  
- L1–20 XP **thresholds** remain for level math.  
- Session “Award draft XP” = **optional / non-canon** tally — never cite as Opening law.  
- Use **EV / pressure** for fights (DM-01 Ch 15/29; T1–5 encounter toolkit) — not CR→XP budgets.

---

## 4. Tier ladder (live Gate Guardians only)

| Tier | Floors | Zone | Guardian | Status |
|-----:|--------|------|----------|--------|
| 1 | 1–10 | Yieldheart Caverns | Vaskor, the Stone Maw | Mapped · combat trusted |
| 2 | 11–20 | Bloomdeep Marsh | The Bloom That Hungers | Mapped · trusted |
| 3 | 21–30 | Anvil of Brogi | Ashthirst the Hollow | Mapped · trusted |
| 4 | 31–40 | Isles of Eternal Radiance | Gor Vekk, Architect of Ends | Mapped · trusted |
| 5 | 41–50 | Sanctum of Echoing Choirs | Choralith, Voice Below | Mapped · trusted · soft quit |
| 6 | 51–60 | Crossroads of the Shattered Thread | Lumen of the Shattered Thread | Toolkit cards · `mapped: false` · combat draft |
| 7 | 61–70 | Pactbound Arena | Xarog, the Pactbound Furnace | Toolkit · Interstice seed · combat draft |
| 8 | 71–80 | Duskshard Pools | Eirfax, the Dusk Crowned | Toolkit · combat draft |
| 9 | 81–90 | Veiled Iron Spiral | Threxus, the Iron Spiral | Toolkit · combat draft |
| 10 | 91–100 | Silencebound Void | The Marquis of Silence | Toolkit · combat draft |

Retired as Guardians: Velkyrion, Zeharra, Kharix, Hollow King, Cindervore, Vox Prime.

---

## 5. Session flow (minimum)

1. Saved PCs → **SESSION** → set tier + Opening hours.  
2. Load scene from Encounters toolkit (T1–5) or Generators spark (T6–10 until mapped).  
3. Foes from Bestiary — prefer `draft: false` (159 trusted T1–5); check AC/HP on drafts.  
4. Track HP / RP / RC; paper death saves.  
5. Craft: charge `components[]`; deep-tier `needsReview` = provisional balance (see deep-tier crafting guidance).  
6. Award **milestones** at seals / beats — not per trash kill XP.

---

## 6. Lore boundaries (do not leak)

| Layer | Players hear | Directors keep |
|-------|--------------|----------------|
| Public myth | Calan'thir & Asmodeus built the Crucible | — |
| Folk religion | Appendix B faiths = mortal models | Objective cosmology in DM-01 |
| Authorship | — | Silent Ones **are** Old Ones / Heartcell (DM-01 Ch 8) |
| Race | **Umbrin** (not Drow) | — |
| Product | No SWTOR branding / ripped MMO models | — |

---

## 7. Honest product stance

- **Tiers 1–5:** table-ready campaign slice (rules, encounters toolkit, 159 trusted creatures, 405 ready crafts).  
- **Tiers 6–10:** DM-01 ops + deep gazetteer + encounter toolkit (35 cards); floors remain **`mapped: false`**; Guardian combat still draft until bestiary T6–10 trust lands.  
- Static export `out/` may lag source — **rebuild** (`npm run build`) before shipping a frozen companion.

**Master stamp:** [`../mechanics/F1_100_RULES_TRACK_2026-07-31.md`](../mechanics/F1_100_RULES_TRACK_2026-07-31.md)
