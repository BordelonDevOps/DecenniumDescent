# Simulation play report — Umbrella tradeskill downtime (SIM-UMB-06)

**Playtest ID:** `SIM-UMB-06`  
**Campaign:** [`SIM_CAMPAIGN_PLAN.md`](./SIM_CAMPAIGN_PLAN.md) · Sim **#7 of 7** (Sim #6 evil contrast **skipped** — owner gate)  
**DM Simulator run:** 2026-07-30  
**Tier:** Transition camp · **Crystalfront Market** (surface haven) + F15 cache liaison  
**Format:** 8 PCs · **no mandatory combat** · Session **scene-notes-only** · Generators for flavor sparks  

> **Math disclaimer:** All horn, period-length, and opportunity-cost figures are **playtest composite only** (companion conventions + GM table). The owner's real **hidden equation + counterpoint are not uploaded** — do not treat [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) as their secret design.

**Continuity in:** Sims #1–4 — company **L5** · horn **118 h** at T3 extraction · **Fireguard Warhammer** · **Heartroot Surveyor's Seal** · F15/F24 maps · research notes · Academic Factions +2 · gate-kit depleted  
**Continuity out:** Filed Concord packet · craft backlog cleared · horn **paused at 118 h underground** (surface) · re-entry cost documented

---

## Expedition brief

### Setting

After Sim #4 aborted F24 scout at **118 / 120 h**, Mira ordered **forced retreat** along the mapped route to **Crystalfront Market** (`floor-encounters.json`: *“Crystalfront Market (Outside)”* — semicircular plaza at the cavern mouth). Vesper rejoins from F15 cache with sealed research satchel. No delving this sim — **umbrella camp** between tier pushes.

### Goal

1. Run **morning / afternoon / evening × 2 days** per `dungeon-mechanics.json` `expedition.timePeriods`.  
2. Rotate **all 16 tradeskills** through camp queue (craft backlog from Sims #1–4).  
3. **File research notes** (Surveyor's Seal, signal doctrine, anvil map) to Concord liaison.  
4. State **horn opportunity cost** of downtime vs re-entry.  
5. Propose **minimum viable downtime rules** for companion/table.

### Stakes

- **Success:** All four campaign metrics · no horn lock · re-entry plan documented.  
- **Partial:** <16 skills touched → note gaps in proposal.  
- **Fail:** Table treats surface camp as long-rest spam without opportunity cost (not modeled here).

---

## Extraction beat (pre-camp · playtest composite)

| Step | Horn Δ | Cumulative underground |
|---|---:|---:|
| Sim #4 end (F24 lip) | — | 118 |
| Extraction march → Crystalfront gate mouth | +2 | **120** |
| **Surface haven reached** | *pause* | **120 (frozen)** |

**Table convention (playtest composite):** Horn tracks **hours underground** per `dungeon-mechanics.json` hornRule. At **Crystalfront Market (Outside)**, clock **pauses** — party is not deeper. The extraction **spent the last 2 h buffer**; at gate mouth the table narrates distant horn **echo** (warning) without triggering 10-year trap because PCs are **outside** the counted depth. **Not owner canon** — cite as sim convention until equation uploads.

**Re-entry opportunity cost:** Next delve resumes at **120 h already banked** → **0 h buffer** unless DM grants surface recall reset (not assumed). Any future underground hour risks horn lock immediately.

---

## Company roster (L5, camp rotation)

| PC | Class | Camp lead skills |
|---|---|---|
| **Brin Copperledger** | Tinker L5 | Tinkering, Blacksmithing, Mining |
| **Helga Stoneprayer** | Cleric L5 | Herbalism, Alchemy, Cooking |
| **Joss Merrow** | Thief L5 | Salvaging, Skinning, Poisoncrafting |
| **Mira Vale** | Wizard L5 | Scribing, Enchanting, Rune Carving |
| **Saffron Reed** | Mirrorsage L5 | Scribing (research), Jewelcrafting |
| **Selene Thalen** | Oracle L5 | Scribing (omen logs) — **RC only**, no craft RP |
| **Kael Grunn** | Warrior L5 | Leatherworking (strap work), Fishing |
| **Torin Ashford** | Paladin L5 | Tailoring (mend), Cooking assist |
| **Vesper Ashwhisper** | Bard L5 | Scribing (copy), Cooking (morale meals) |

**Vesper** returns from F15 cache Day 1 morning. **Session tab:** scene notes only — horn display **frozen at 120** with GM annotation “SURFACE PAUSED.”

---

## Two-day schedule (3 periods × 2 days)

**Period length (playtest composite):** **4 h each** — 12 h active camp per day, 12 h sleep/watch (not horn-tracked on surface).

### Day 1 — backlog clear

| Period | Lead | Activities | Skill(s) |
|---|---|---|---|
| **Morning** | Brin + Helga | Refit Fireguard haft; brew salve batch; file **Surveyor's Seal** rubbing with Saffron | Blacksmithing · Herbalism · Scribing |
| **Afternoon** | Joss + Kael | Salvage soot-mask rivets into kit; skin marsh eel from cache ice; **Generators** loot spark → “cooled slag tongs” | Salvaging · Skinning · Tinkering |
| **Evening** | Helga + Torin + Vesper | **Practical Spiced Feast** ×2; mend cloaks; Vesper copies signal doctrine for Concord | Cooking · Tailoring · Scribing |

### Day 2 — full skill rotation + research filing

| Period | Lead | Activities | Skill(s) |
|---|---|---|---|
| **Morning** | Mira + Saffron | Enchant lantern lens (luminous ore ×1); jewel polish for seal case; poison antidote vial (marsh toxin sample) | Enchanting · Jewelcrafting · Poisoncrafting |
| **Afternoon** | Brin + Mira | **Rune Carving** on gate-pick (Threshold rune); mine-grade sort of remaining ore ×3; Alchemy oil batch | Rune Carving · Mining · Alchemy |
| **Evening** | Kael + Joss | **Fishing** at Crystalfront runoff pool (table: no combat); Leatherworking bracers; Concord **research packet** handoff | Fishing · Leatherworking · (filing) |

**16 / 16 tradeskills touched:** Alchemy, Blacksmithing, Cooking, Enchanting, Fishing, Herbalism, Jewelcrafting, Leatherworking, Mining, Poisoncrafting, Rune Carving, Salvaging, Scribing, Skinning, Tailoring, Tinkering ✓

---

## Craft queue (selected recipes)

All from `crafting-recipes.json`; **empty `components[]`** — table-assigned from camp stock (consistent Sims #1–2 friction).

| Recipe | Skill | Crafter | Output |
|---|---|---|---|
| *Standard Herbalist's Healing Salve* | Herbalism | Helga | +4 doses |
| *Practical Spiced Feast* ×2 | Cooking | Helga/Torin | camp meals |
| *Standard Oil* | Alchemy | Helga | 2 flasks |
| Lantern lens enchant (workbench) | Enchanting | Mira | +1 luminous lantern |
| Gate-pick Threshold rune | Rune Carving | Brin/Mira | Warded Gate aid |
| Leather bracers (proxy) | Leatherworking | Kael | +1 AC wrist slot narrative |
| Antidote vial (proxy) | Poisoncrafting | Saffron | 1 dose |
| Jewel case polish | Jewelcrafting | Saffron | Seal transport safe |

**Items → Session handoff:** Each line appended to scene notes via `pushItemHandoff()` pattern — **positive repeat** from Sim #1.

---

## Research notes filing

**Concord liaison:** Quartermaster **Rhal-Voss** (callback from `EXP-BGR-01` fringe watchpost — existing NPC, no new lore).

| Document | Authors | Status |
|---|---|---|
| Heartroot Surveyor's Seal ID + rubbings | Saffron, Selene | **Filed** |
| Bloomdeep F11–15 map grid | Saffron, Mira | **Filed** |
| Reedcaller signal doctrine v1 | Vesper, Saffron | **Filed** |
| F24 Chained Anvil swing cadence map | Joss, Brin | **Filed** |
| T3 Gearspark craft manifest | Brin | **Filed** |
| Forge Master / "Third Hammer" field note | Brin | **Filed (prestige seed, L5 ineligible)** |

**Academic Factions:** Filing complete → **+1 rep** (narrative total **+3** since campaign start). **Religious Orders:** Helga's clinic hours → remains **Liked**. **Arcane Guilds:** Mira's enchant ledger → **Liked** held. Reputation still **not persisted in Session** — Builder save only.

---

## Horn opportunity cost (playtest composite)

| Cost type | Hours | Meaning |
|---|---:|---|
| **Banked underground** | 120 | Re-entry starts at horn ceiling |
| **Downtime days (surface)** | 0 horn Δ | Clock paused at haven |
| **Opportunity cost (if re-entered today)** | 12 h/day × 2 = **24 h** | Equivalent underground progress **not** made |
| **Minimum safe re-entry budget** | 0 h | Would require surface recall reset or author equation — **not granted** |
| **Implied table choice** | — | Camp 2 days **or** immediate horn-risk delve — party chose camp |

**Statement for GMs:** Two days umbrella camp traded **~24 h of potential delve time** for **16-skill maintenance + filing** while avoiding horn lock at depth. On re-entry without reset, **every hour underground triggers recall pressure**.

---

## Minimum viable downtime rules (proposal — metric #4)

Draft for companion/table; **not rules canon**.

| Rule | Proposal |
|---|---|
| **1. Surface pause** | Horn stops at havens tagged **Outside** or explicit surface camps (`floor-encounters.json` Crystalfront); resumes on descent. |
| **2. Periods** | Use `morning / afternoon / evening` — **4 h each** default craft/research block; 12 h camp day. |
| **3. Skill throughput** | One significant recipe or research filing per PC per period; helpers add +1 h, not double output. |
| **4. No combat XP** | Downtime sims award **0 combat XP** unless random encounter table invoked (opt-in). |
| **5. Research filing** | Research team output converts to **rep narrative + scene note**; Academic Factions +1 per major packet (manual). |
| **6. Re-entry cost** | Display **banked horn + opportunity hours** on Session banner when leaving camp. |
| **7. Components gap** | Until recipe `components[]` wired, camp consumes **abstract Supply units** (1 per craft) from loot handoff list. |
| **8. Owner equation** | Replace §1–6 when owner uploads real hidden equation + counterpoint. |

---

## Playtest composite reference (NOT owner design)

Sim #7 **does not apply** `HIDDEN_DUNGEON_EQUATION.md` as secret design. That file remains a **repo synthesis** of companion mechanics. This run used only:

- Horn pause at surface (GM convention)  
- 4 h × 6 periods = 24 h camp activity  
- 24 h opportunity cost vs delve  

---

## Success metrics (Sim #7)

| Metric | Target | Result |
|---|---|---|
| 3 periods × 2 days | yes | ✓ 6 blocks logged |
| Horn opportunity cost stated | hours | ✓ 24 h delve-equivalent; 120 h banked |
| Equation doc | if available | ✓ Referenced as **non-owner synthesis only** |
| Downtime rules proposal | yes | ✓ § above |

---

## Friction log

| # | Area | Friction | Severity |
|---:|---|---|---|
| 1 | Horn | Surface pause not in Session UI — GM note only | High |
| 2 | Crafting | 16 skills × empty components — Supply fiat | High |
| 3 | Reputation | Filing doesn't auto-update ReputationPanel | Medium |
| 4 | Fishing | No fishing minigame — single Survival check | Low |
| 5 | Positive | Research packet closes Sims #1–4 arc for Concord | Low |

---

## Sim #7 conclusion

**Outcome: SUCCESS.**

Forced to **Crystalfront Market** at **120 h banked underground** (118 + 2 h extraction), the company ran **two full camp days** (morning/afternoon/evening × 2) with **all 16 tradeskills**, cleared craft backlog, and **filed** the Surveyor's Seal, tier maps, and T3 field notes with Concord. Horn **paused on surface**; **24 h delve opportunity cost** documented. Sim #6 evil contrast remains **skipped** (owner gate). Campaign ecosystem queue **complete** pending owner equation and optional T4 live re-run.

**Carry-forward (campaign end state):** Research packet filed · salves/feasts stocked · horn **120 h banked / paused surface** · **zero buffer on re-entry** · Academic +3 narrative · Fireguard Warhammer maintained.

---

## Appendix

- `src/data/dungeon-mechanics.json` (`expedition.timePeriods`, `hornRule`)  
- `src/data/floor-encounters.json` (Crystalfront Market)  
- `src/data/crafting-recipes.json` · `src/data/reputation.js`  
- `src/components/GeneratorsPanel.tsx` · `src/lib/session-handoff.ts`  
- Prior sims: `SIM_01` through `SIM_04` play reports
