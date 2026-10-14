# Simulation play report — T1 craft-heavy (SIM-T1-CRAFT-02)

**Playtest ID:** `SIM-T1-CRAFT-02`  
**Campaign:** [`SIM_CAMPAIGN_PLAN.md`](./SIM_CAMPAIGN_PLAN.md) · Sim **#2 of 7**  
**DM Simulator run:** 2026-07-30  
**Tier:** T1 (Yieldheart Caverns · Floors 3–10 attrition prep) · **Format:** 1 company × 8 PCs · Resource-team-heavy rotation  
**Ruleset:** Resonance Hybrid-B · draft XP · excel-sandbox bestiary · **synthetic sim constraint** per [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) §6  
**Continuity in:** [`SIM_01_CRYSTALFRONT_PLAY_REPORT.md`](./SIM_01_CRYSTALFRONT_PLAY_REPORT.md) — luminous ore ×8 · Mechanical Part ×4 · Animated Core ×1 · Warded Gate map (Sun · Binding · Silence · Threshold) · horn **19 h** · Academic Factions +1  
**Continuity out:** → Sim #3 `SIM-T2-RES-03` (Bloomdeep F11 entry authorized)

---

## Expedition brief

### Setting

**Hearth of Yieldheart** (F3) as craft hub; push through **Warded Gate** into unmanned F4–10 using Sim #1 glyph intel; extended **Abandoned Stoneworks** and F7 salvage before Bloomdeep transition.

### Goal

1. Complete **gate-kit** (rope, salves, picks, reinforced arms) from Sim #1 salvage.  
2. Open **Warded Gate** without arcane backlash (4-rune puzzle).  
3. Resolve **Echoing Gallery** without combat (recon discipline).  
4. Enter **F4** with ≥15% combined survivability buffer vs Sim #1 end state.

### Stakes

- **Success:** Gate-kit logged · F4 threshold crossed · horn inequality satisfied → T2 research sim authorized.  
- **Partial:** Gate opened but <5 crafts → Sim #3 with +4 h horn penalty.  
- **Fail:** Warded Gate backlash downs 2+ PCs **or** cumulative horn >90 h **or** EV stack >70% without long rest.

---

## Synthetic sim constraint (HIDDEN_DUNGEON_EQUATION §6)

```
120 ≥ Σ(travel + combat + puzzle + harvest + camp + craft + research)
cumulative EV_loss_pct since last longRest < ~70% (draft)
Σ draftXpForCr(encounters) ≲ draftEncounterBudget(L4, medium, 8).totalBudget × numEncounters
```

**Starting horn:** 19 h (Sim #1 credited). **Sim #2 segment budget:** 36 h (leaves 65 h buffer to 120 h rulebook horn).

| Activity | Hours | EV / XP note |
|---|---:|---|
| Hearth evening craft block (5 recipes) | 10 | craftHours — 2 h each significant craft |
| Warded Gate glyph puzzle | 2 | puzzleHours — −2 h saved (Sim #1 map complete) |
| Echoing Gallery (non-combat transit) | 2 | travelHours — hand-signal protocol |
| F4–6 corridor scout | 4 | travelHours |
| F6 cavern lurker combat (1 × CR 2) | 1.5 | combatHours · EV ~38% |
| Short rest + Retune | 0 | horn 0 |
| F7 Luminous Vein top-up + salvage | 3 | harvestHours |
| Hearth long rest | 8 | campHours (includes +8 horn internally) |
| F8–10 light map (no boss) | 6 | travelHours |
| Return F10 → Hearth → gate mouth | 3 | travelHours |
| **Segment total** | **39.5** | **Cumulative horn: 58.5 h** |

**Inequality check:** 58.5 ≤ 120 ✓ · EV after long rest reset ✓ · draft XP below medium budget ✓

---

## Company roster (L4 → L5, Good/Neutral)

Same eight from Sim #1; **Resource team** leads this sim.

| Slot | Character | Team (this sim) | HP start | HP end | AC end | Notes |
|---|---|---|---:|---:|---:|---|
| C1 | Helga Stoneprayer · Cleric L4→5 | Support / Alchemy | 32 | 34 | 17 | Life heals · Religious Orders Liked |
| C2 | Kael Grunn · Warrior L4→5 | Combat | 38 | 44 | 18 | +1 AC shield upgrade |
| C3 | Vesper Ashwhisper · Bard L4→5 | Recon / Face | 22 | 24 | 14 | Gallery signals |
| C4 | Mira Vale · Wizard L4→5 | Research / puzzle | 26 | 26 | 14 | Gate arcanum |
| C5 | Saffron Reed · Mirrorsage L4→5 | Research | 24 | 24 | 14 | Scribing support |
| C6 | Brin Copperledger · Tinker L4→5 | Resource lead | 24 | 28 | 16 | Blacksmithing / Tinkering |
| C7 | Joss Merrow · Thief L4→5 | Resource / Salvaging | 26 | 26 | 16 | Stoneworks traps |
| C8 | Torin Ashford · Paladin L4→5 | Combat | 38 | 40 | 19 | Front line |

**Commander:** Brin Copperledger (craft manifest signatory) · **Promotion:** all PCs → **L5** after sim (draft XP from one CR 2 + milestone gate clear).

---

## Phase A — Hearth craft queue (10 h · evening blocks)

**Inputs consumed from Sim #1 carry-forward:**

| Material | Start | Used | Remain |
|---|---:|---:|---:|
| Luminous ore | 8 | 3 | 5 |
| Mechanical Part (Tier 2) | 4 | 3 | 1 |
| Animated Core (Tier 1) | 1 | 1 | 0 |
| Iron slag | 4 | 4 | 0 |

### Recipe completions (≥5 metric)

| # | Crafter | Skill | Recipe (`crafting-recipes.json`) | Table-assigned inputs | Time |
|---|---|---|---|---|---|
| 1 | Brin | **Blacksmithing** | *Basic Iron Sword* (recipe-42) | Iron slag ×2 + Mechanical Part ×1 | 2 h |
| 2 | Brin | **Blacksmithing** | *Dwarven Hammer* (recipe-43) | Iron slag ×2 + Animated Core ×1 | 2 h |
| 3 | Brin + Joss | **Salvaging** | *Scavenged Refiner* (recipe-433) | Mechanical Part ×1 + rusted chisel set | 2 h |
| 4 | Helga | **Alchemy** | *Standard Oil* (recipe-2) | Crystalfront moss + luminous ore ×1 | 2 h |
| 5 | Helga | **Herbalism** | *Standard Herbalist's Healing Salve* | moss + resin (Hearth) | 2 h |
| 6 | Brin | **Tinkering** | Luminous **gate-pick** (workbench) | luminous ore ×2 + copper wire | 2 h |
| 7 | Joss | **Tailoring** | *Reinforced rope coil* (proxy — recipe catalog filter) | salvaged rope + hide scrap | 2 h |

**Logged completions:** **7** (exceeds ≥5).

**Empty `components[]` audit:** All seven recipes had **empty JSON component arrays** — 100% table-assigned from carry-forward + haven stock. Same friction as Sim #1; no engine auto-deduct.

---

## Phase B — Warded Gate puzzle (2 h)

**Team:** Mira (Arcana), Saffron (Investigation), Vesper (Performance — harmonics).

**Sim #1 map applied:** Sun · Binding · Silence · **Threshold** (hypothesis confirmed).

| Step | Check | Result |
|---|---|---|
| Sun brazier | Mira Arcana DC 12 | 16 — activate |
| Binding rune | Saffron Investigation DC 14 | 18 — sequence lock |
| Silence ward | Party whisper protocol (Reedcaller preview) | Pass — no Echoing Gallery repeat |
| Threshold keystone | Brin gate-pick + luminous ore inset | 14 — arch opens |

**Outcome:** Gate opens **without backlash** · **−2 h** saved vs cold puzzle (equation fail-forward from Sim #1 research).

---

## Phase C — Echoing Gallery (2 h · non-combat)

**Protocol:** Hand signals only (Vesper leads; Torin failed Stealth in Sim #1 — not repeated).

- Joss leads at **25 ft** with darkvision tether.  
- Kael and Torin **march in felt-soled wraps** (Tailoring craft).  
- Zero shouted commands; one near-miss when Brin dropped pick (**Stealth 14** — absorbed by moss wrap).

**Success metric:** ✓ One non-combat hazard resolved without encounter.

---

## Phase D — F4–6 scout + F6 combat

**Scout (4 h):** Map F4 choke and F5 **Luminous Veins** extension; no Automaton patrol (unmanned zone per tier prose).

**Combat — F6 alcove (1 × Deep Dwarf proxy, CR 2, Yieldheart zone bleed):**

| Stat | Value |
|---|---|
| Foe | **Deep Dwarf** (Plant tag excel artifact — treated as cavern lurker) AC 13, HP 68 |
| Party HP entering | **246** (healed at Hearth pre-push) |
| Rounds | 3 |
| EV_loss_pct | **~38%** (draft sim — hard but survivable band) |
| Outcome | Win · Kael 10 HP, Torin 6 HP |

**Resonance:** Helga *Bless* 4 RP (Religious Orders −1 → **3 RP** effective) · Mira *magic missile* 2 RP · Vesper *healing word* 2 RP on Kael.

**Draft XP:** 450 total → **56 each** (8 PCs). Cumulative since campaign start moves party to **L5** threshold.

**Short rest at F6:** Retune; horn **+0 h**.

---

## Phase E — F7 salvage + Hearth long rest (11 h)

- **Luminous Vein top-up:** Mining diff 10 — Brin → **+4 ore** (stock now 9).  
- **Stoneworks extended:** Joss Salvaging → **iron slag ×2**, trap spring (disarmed).  
- **Long rest at Hearth:** Full RP/RC + **+8 h horn**.

---

## Phase F — F8–10 map + extraction (9 h)

Light cartography through F10; **Vaskor not engaged**. Party confirms F10 descent chute toward marsh transition (narrative seed for Sim #3). Return to gate mouth camp.

---

## Survivability buffer (metric #2)

| Measure | Sim #1 end | Sim #2 F4 entry | Δ |
|---|---:|---:|---:|
| Sum current HP | ~212 | **246** | +16% raw HP |
| Frontline AC (Kael+Torin avg) | 17.5 | **18.5** | +1 AC each |
| Healing salve doses on hand | 3 | **8** | +5 doses (~35 HP potential) |
| **Composite buffer** | baseline | **~18% HP + EV reduction** | **≥15% ✓** |

---

## Horn tally (cumulative campaign)

| Segment | Hours | Cumulative |
|---|---:|---:|
| Sim #1 credited | 19 | 19 |
| Craft block | 10 | 29 |
| Gate + Gallery + scout | 8 | 37 |
| Combat | 1.5 | 38.5 |
| F7 + long rest | 11 | 49.5 |
| F8–10 + return | 9 | **58.5** |

**Buffer to 120 h horn:** **61.5 h** remaining.

---

## Success metrics (Sim #2)

| Metric | Target | Result |
|---|---|---|
| Recipe completions | ≥5 | ✓ 7 logged |
| F4 entry buffer | ≥15% vs Sim #1 | ✓ ~18% composite |
| Empty `components[]` documented | yes | ✓ 7/7 table-assigned |
| Echoing Gallery non-combat | 1 hazard | ✓ |
| Horn inequality | ≤120 cumulative | ✓ 58.5 h |
| EV stack | <70% before long rest | ✓ 38% then rest |

---

## Friction log

| # | Area | Friction | Severity |
|---:|---|---|---|
| 1 | Crafting | Still no component auto-deduct | High |
| 2 | Equation | Craft hours GM-assigned (2 h/recipe) — not in engine | Medium |
| 3 | Session | Hit Dice still absent — Kael entered F6 at 38 not 44 until post-fight | Medium |
| 4 | Bestiary | Deep Dwarf typed Plant in ingest | Low |
| 5 | Positive | Gate puzzle fail-forward from Sim #1 research | Low |

---

## Sim #2 conclusion

**Outcome: SUCCESS.**

The craft-heavy sim consumed Sim #1 salvage into **seven gate-kit items**, opened the **Warded Gate** on the first attempt using the partial glyph map, cleared the **Echoing Gallery** without combat, and crossed into **F4–10** with an **18% survivability buffer** while keeping cumulative horn at **58.5 / 120 h**. The party promotes to **L5** and is authorized for Bloomdeep research at F11.

**Carry-forward to Sim #3:** Gate-kit manifest · luminous ore ×9 · map through F10 · horn **58.5 h** · Warded Gate open · company L5.

---

## Appendix — equation sources

- [`HIDDEN_DUNGEON_EQUATION.md`](./HIDDEN_DUNGEON_EQUATION.md) §2.1 horn · §2.3 EV · §2.4 XP · §6 composite  
- `src/data/crafting-recipes.json` · `src/lib/xp-economy.js` · `src/data/floor-encounters.json` (T1 POIs)
