# Combat system comparison — Decennium Descent vs peers

**Date:** 2026-07-30  
**Audience:** Owner / Director  
**Scope:** Design intent and implementation status of DD combat vs **Trench Crusade** (clarified below), **D&D 2024/5.5**, and **Pathfinder 2e**. Sources: `rulebook_output.txt` (rulebook extract), companion docs (`RESONANCE_CANON.md`, `SESSION_LOOP.md`, `BALANCE_*.md`, `MECHANICS_BIBLE.md`), and public summaries of peer systems.

---

## 1. What “Trench Warfare” means (ambiguity)

There is **no TTRPG product literally named “Trench Warfare”** in this workspace or in a targeted web search. The closest matches:

| Candidate | What it is | Why compare here |
|-----------|------------|------------------|
| **Trench Crusade Roleplay (TCRP)** | Grimdark d100 TTRPG playtest (WWI trenches + crusader horror). Faith Points for miracles; Corruption for forbidden rites; wounds stack quickly; tiered archetype advancement. | Best **TTRPG** match if the owner meant “trench-themed latest edition.” |
| **Trench Crusade (miniatures wargame 1.0.x)** | Skirmish wargame (~6–20 models). Turns = Initiative → alternating **model activations** → Morale. 2d6 success rolls (7+), **injury/down** system, Blood/Blessing markers, no hero HP pool. | Best match if the owner meant the **published wargame**, not a narrative RPG. |
| **Never Going Home / Ross Rifles** | WWI trench RPGs (+One / PbtA). Party-focused, horror, card-based mental resources. | Thematic cousins; less “crunch combat” than DD. |

**This document compares DD primarily to TCRP** (narrative RPG peer) and briefly notes the **Trench Crusade wargame** where the model differs sharply.

---

## 2. DD combat pillars (what sources actually say)

### Core resolution

- **d20 + modifier vs target** for ability checks, saves, and attacks (`rulebook_output.txt` ~5682; `MECHANICS_BIBLE.md` §1).
- **Advantage/disadvantage** present (e.g. armor without proficiency ~4874).
- **Proficiency bonus** scales with level (+2 at L1, up to +6 at L20 per advancement table).

### Action economy (5e-shaped)

From **Chapter 8: Combat in Aethel** (`rulebook_output.txt` ~5916–5971):

| On your turn | Limit |
|--------------|-------|
| Move | Up to speed (splittable) |
| Action | One |
| Bonus action | One (even if multiple features grant options) |
| Reaction | One per round (refreshes start of your turn) |
| Free interaction | One object/environment interaction |

Standard actions: Attack, Cast a Spell, Dash, Disengage, Dodge, Help, Hide, Ready, Search, Use an Object, class features. **Opportunity attacks, grappling, shoving, cover, two-weapon fighting** follow familiar 5e structure (~5990–6002).

**Round length:** ~6 seconds (~5917).

**Design note:** Several class features use **percentage modifiers** (+15% crit, −20% accuracy, +10% DR) alongside d20 language — a hybrid that reads closer to CRPG/MMO tuning than pure tabletop die steps. Many of these lack final action/recharge/stacking rules in companion data (`BALANCE_PLAYER_CLASSES.md` §3).

### Attack, AC, damage

- **Attack:** d20 + ability mod + proficiency (if proficient) vs **AC** (~5973–5981).
- **Nat 1** always misses; **nat 20** always hits and **crits** (double damage dice ~6009–6010).
- **AC** from armor category + Dex (with medium cap +2) + shield (~4874–4922).
- **Damage types, resistance (half), vulnerability (double), temp HP** — standard 5e pattern (~6011–6040).

### HP and death

- **HP at L1:** max Hit Die + CON; later levels: roll HD + CON or fixed average (`rulebook_output.txt` ~83–86, 885–886).
- **Hit Die spread:** d6 (Wizard/Mage) through **d12 (Warrior)** (~875).
- **At 0 HP:** instant death if remaining damage ≥ max HP; else unconscious + **death saves** (3 successes stable / 3 failures dead) (~6019–6032).
- **Monsters** usually die at 0 HP (~6035–6036).

Example durability bands from audit (`BALANCE_PLAYER_CLASSES.md` §1, CON +2): Warrior **12 / 44 / 84** HP at L1 / L5 / L10; Mage **8 / 32 / 62**.

### Initiative & Session tracker

**Rulebook:** d20 + Dex; order fixed for encounter; surprise rules (~5918–5927).

**Companion (`SESSION_LOOP.md`):**

- Auto-roll on add; manual override; **Sort** / **Roll all**.
- **Tie-break:** higher initiative → higher Dex → player add-order → **allies before foes**.
- Tracks **round/turn**, HP, free-text **conditions** (no automated condition rules), **horn clock** (`HORN_AT = 1200` — Opening PoNR at day 50 inside the 2400h Opening; purged 2026-07-31 — see [`DESCENT_WINDOW_CANON.md`](./DESCENT_WINDOW_CANON.md)).
- **No spell picker**, **no death-save automation**, **no encounter budget/XP workflow**.

### Resonance (RP) vs Oracle (RC)

**Canon:** **Resonance Points + Dissonance** (`RESONANCE_CANON.md`).

| Topic | Rule |
|-------|------|
| Pool | One **RP capacity pool** by class/level — not Vancian slots. All 14 Weave-casting base classes have authoritative L1–20 curves. |
| Cost | `Resonance Rank × 2`, then explicit class/item specialization + Dissonance surcharge + chosen Overcast costs. |
| Cantrips | 0 RP |
| Short rest (“Retune”) | ≈¼ max pool + casting mod; Dissonance resets to 0. |
| Long rest | Full pool |
| Overcast | Empowered (+2 RP, +50% dmg/heal), Extended, Widened, Quickened, Twinned, etc. |
| Dissonance | Repetition/high-rank/Overcast strain: In Tune → Frayed → Discordant → Fractured. Fractured ordinary casters cannot cast Rank 1+. |
| Multiclass | Highest caster pool + **25%** of one secondary pool (round up); tertiary adds none |
| Reputation | Institutional access, teachers, focuses, sanctuaries, and explicit boons only; standing itself never modifies RP capacity, spell cost, or Retune |

**Oracle exception:** **Revelation Charges (RC)** 3–7, **not RP**. Recovery via each Mystery’s **Prophecy Trigger**, not rest (`RESONANCE_CANON.md` §6; Oracle chapter in extract). The Session tracker does **not** automatically restore RC on rests; recovery follows each Mystery's Prophecy Trigger or an explicit Revelation feature.

### Martial & hybrid resources (selected)

| Class / system | Resource | Source sketch |
|----------------|----------|---------------|
| **Dragoon** | **Momentum** (cap 5 → 7); build via movement/hits; spend on leaps, overflow, extra-action tempo | `rulebook_output.txt` ~1289–1358 |
| **Monk** | **Ki Chain** (0–5, companion draft cap 7); stances (free switch 1/round); % dodge/DR | ~2069–2097 |
| **Warrior** | **Mutation trees** (Basic/Advanced/Apex), BT stacks, serums; apex forms grant +2 attacks/round, cleave, etc. | ~3330–3409 |
| **Bard** | **Crescendo** die (stack to 5, spend for party tempo) | `MECHANICS_BIBLE.md` §2 |
| **Paladin** | Lay on Hands pool, Divine Smite, **half-Weave RP curve**, Oath revelations | `BALANCE_PLAYER_CLASSES.md` |
| **Soldier / Thief / etc.** | Mostly at-will chassis + feats; fewer pooled resources | class audit |

### Encounter design & XP (DD gaps)

**Confirmed:** L1–L20 **cumulative XP thresholds** and total-level multiclass advancement (`XP_ADVANCEMENT_CANON.md`).

**Not in reviewed sources:** CR→XP awards, encounter budgets, party-size/difficulty multipliers, rest-day cadence (`BALANCE_DM_XP.md`).

**Companion gaps:**

- **698 / 708** bestiary entries lack AC/HP/attacks in source spreadsheet (`BESTIARY_INGEST.md`); **10 gate guardians** have companion-authored combat drafts — not “708 placeholders.”
- Session gate-boss HP stub: `40 + tier×25` — explicitly **not** balance advice.
- CR-to-tier filter in UI is browse heuristic only (2 CR per tier).
- Floor Encounters are **location briefs**, not budgeted rosters; T6–T10 unmapped/draft.

**Simulation (draft only):** L3 party vs Bloom (CR 5) ~8 rounds, hard; L8 vs Vaskor (CR 8) ~6 rounds, survivable — using draft guardian payloads (`BALANCE_COMBAT_SIM.md`). Not proof of final tuning.

---

## 3. Comparison matrix

### Complexity / learning curve

| System | Curve | Notes |
|--------|-------|-------|
| **DD** | **Medium–high** for players who know 5e; **high** for GMs | Core loop is familiar (move/action/bonus/reaction). Complexity stacks from **Resonance + Dissonance tracking**, **overcast menu**, **17 classes** with parallel resources (Momentum, Ki Chain, mutations, RC triggers), and **%‑based class text** that isn’t fully executable yet. |
| **D&D 2024** | **Medium** | Same skeleton as 2014; 2024 adds **Heroic Inspiration** (reroll any die), **Weapon Mastery**, streamlined species/backgrounds. Easiest onboarding if table already knows 5e. |
| **PF2e** | **High** | 3-action economy, traits, degrees of success, reactive rules, codified conditions — steep until fluency. |
| **TCRP** | **Medium** (d100 tradition) | Percentile skills/combat; fewer “exceptions per class” than DD’s 17 kits, but **wound/morale/corruption** layers reward system mastery. |
| **TC wargame** | **Medium** (rules) / **high** (tactics) | Small ruleset, but alternating activation + injury/markers reward practice. |

### Pacing (rounds, nova vs attrition)

| System | Typical pacing | Nova vs attrition |
|--------|----------------|-------------------|
| **DD** | **Intent:** multi-round set pieces; **short-rest retune** (+ Oracle trigger recovery) favors **attrition across several fights** if the table rests between delves. **Risk:** overcast Quickened/Twinned + Paladin/Mirrorsage/Oracle draft features can **nova** if caps aren’t finalized. Simulation: **6–8 rounds** vs gate bosses (draft). | RP pool is broader than slot-by-tier casting at comparable level (e.g. L10 Wizard **36 RP** ≈ many tier‑1 casts before discounts) + **¼ pool per short rest** pushes **repeated casting** over single nova — *because* Refrain/Dissonance makes repetition progressively costly. |
| **D&D 2024** | **3–6 rounds** common for standard encounters; **1-minute** short-rest warlock/paladin/etc. still exist. Full casters mostly **long-rest nova** unless pacing is enforced. | **Nova-default** for full casters unless DM uses gritty resting; martials steadier; 2024 **Heroic Inspiration** reduces swinginess. |
| **PF2e** | **4–8+ rounds**; focus spells and 3-action turns stretch combats. | **Encounter budget + focus points** encourage **sustained pressure**; casters less “empty after one fight” than 5e slots. |
| **TCRP** | **Slow, lethal**; planning and cooperation emphasized. | **Attrition / wound stack**; Faith/Corruption spent for spikes, not full daily nova. |
| **TC wargame** | Scenario-driven; **activation count** = pacing knob. | **Attrition** via injuries, morale, marker spend; no caster nova analogue. |

### Martial vs caster balance philosophy

| System | Philosophy |
|--------|------------|
| **DD** | **Design intent:** 5e-like **martial baseline + class resource spikes** (Momentum, mutations) while casters use **flexible RP pool** and Oracle uses **trigger-gated RC**. Paladin/Warrior/Dragoon prose packs **defense + burst + support** on one chassis — audit flags **martial/caster parity unverified** until high-impact features are bounded (`BALANCE_PLAYER_CLASSES.md`). |
| **D&D 2024** | **Martials buffed** (Weapon Mastery, some class tweaks); casters still spike but **Heroic Inspiration** helps everyone; long-rest casters remain apex if rested. |
| **PF2e** | **Explicit parity goal:** martials have **comparable action economy**; casters use **focus spells + slots**; buff/debuff math is transparent. |
| **TCRP** | **Faith vs Corruption** mirrors divine vs forbidden power; combat role often **archetype-locked** (soldier vs sorcerer), not modular multiclass. |
| **TC wargame** | **List/build synergy**; no class divide — every model is a package of actions and injury profile. |

### Resource systems

| System | Model |
|--------|--------|
| **DD** | **RP pool** (Rank × 2) + **Dissonance/Refrain** + Overcast; **RC** parallel track for Oracle; martial **Momentum/Ki/mutations/Crescendo** remain class-specific. |
| **D&D 2024** | **Spell slots** (+ Pact Magic, Ki, Rage, etc.); short-rest partial recovery on some classes; **Heroic Inspiration** separate. |
| **PF2e** | **Spell slots by rank** + **Focus Points** (refocus 10 min / daily); **Hero Points** (reroll); class-specific pools (Focus, Infused Reagents, etc.). |
| **TCRP** | **Faith Points** (miracles) vs **Corruption** (dark rites); equipment scarcity; wounds not HP. |
| **TC wargame** | **Blood/Blessing markers** spent to modify rolls/injuries; warband progression between scenarios. |

### Deadliness / HP bloat

| System | Profile |
|--------|---------|
| **DD** | **5e HP curve** (death saves, instant death on massive hit); **Warrior d12** pushes durable martials. Companion audit: Mage ~**49%** of Warrior HP at L5 — “appropriate chassis gap,” not proven parity (`BALANCE_COMBAT_SIM.md`). **Not gritty** by default; horn-clock dungeon push adds **time pressure**, not wound simulation. |
| **D&D 2024** | **HP bloat continues**; Heroic Inspiration reduces feel-bad; still swingy at low level. |
| **PF2e** | **Tighter math**, **crit effects**, **wound** at 0 HP (dying value); generally **deadlier** than 5e at same narrative tier. |
| **TCRP / TC** | **Brutal** — wounds, down results, morale failure; HP bloat not the model. |

### Encounter design

| System | Tools |
|--------|-------|
| **DD** | **CR labels** on bestiary; **tier zones** (UI heuristic); **floor gate bosses**; **no sourced XP budget**. Director must improvise or use **draft** CR→XP sketch in `XP_ADVANCEMENT_CANON.md` (not canon). |
| **D&D 2024** | **CR + XP budget tables**; encounter multiplier for monster count; daily adventuring guidance. |
| **PF2e** | **XP budget per level**, creature level as primary knob, tight encounter math. |
| **TCRP** | Scenario/scenario packs; archetype tiers; emphasis on objective + attrition. |
| **TC wargame** | **Scenario Victory Points**, Morale checks, warband size ~6–20. |

---

## 4. Verdict — where DD stands

### Design intent (what DD is trying to be)

**Strengths relative to peers:**

1. **Familiar tactical RPG spine** — lowest friction for 5e tables; full combat chapter mirrors action economy, cover, grappling, mounted combat.
2. **Distinctive magic economy** — **Resonance capacity + Dissonance/Refrain + Overcast + class-specific cadence** is a clearer identity than renamed slots. Short-rest **retune** + large pools push **dungeon-delving attrition** that fits the **2400h Opening / 1200h Horn PoNR** and multi-fight expeditions.
3. **Class fantasy depth** — 17 classes with **parallel resource languages** (Momentum, Ki Chain, mutations, RC triggers, Crescendo) support long-horizon MMO-adjacent identity without requiring a 3D client.
4. **Oracle as parallel track** — RC + Prophecy Triggers are a genuine alternative to RP, not a reskin.
5. **Vertical dungeon structure** — tiered gate bosses and floor briefs give **campaign-shaped combat** even before encounter math exists.

**Weaker or unfinished vs peers:**

1. **Executable completeness** — Peers ship **closed loops** (attack lines, budgets, awards). DD’s `BALANCE_REPORT.md` verdict: **not balance-verifiable yet** — rules often descriptive; high-impact features lack action/cap/stacking data.
2. **Encounter/XP loop** — D&D/PF2 give sourced **CR→XP→budget** pipelines. DD has **thresholds only**; Session doesn’t award XP; bestiary XP unverified.
3. **Bestiary as combat engine** — Excel has 708 real identity/CR/XP/loot rows but no combat-stat columns; 10 gate guardians have **draft** structured payloads. PF2/D&D monsters are playable on day one when full stat blocks exist in source.
4. **Dissonance / Overcast / specialization** — anti-spam cutoff is now explicit; remaining balance work is numeric tuning of Overcast and class-specific discounts.
5. **Internal consistency** — % modifiers vs d20; armor/AC conflicts on some classes; Builder XP thresholds **conflict** with confirmed rulebook table.
6. **Martial/caster parity** — **Unproven.** Audit highlights Mirrorsage copy ceiling, Oracle draft renewals, Paladin aura stacking, Warrior/Dragoon burst — none fully capped.
7. **Session tracker** — Good **table aide** for initiative/RP/RC/horn; **not** a combat resolver or DM encounter tool vs D&D Beyond / PF2 tools.

### vs D&D 2024/5.5 specifically

- DD is **intentionally “5e-compatible feel + Resonance + dungeon clock + wider class roster.”**
- DD is **not** trying to be 2024’s **Heroic Inspiration** or **Weapon Mastery** refresh — it trades that for **RP/overcast/reputation** and **mutation/momentum** class kits.
- If the goal is **low-friction pickup**, mainstream d20 fantasy remains simpler. If the goal is **distinctive delving economy**, DD now has an executable RP/Dissonance identity; remaining risk is balance tuning and bestiary trust.

### vs Pathfinder 2e specifically

- PF2e wins on **crunch clarity, encounter math, and balance process**.
- DD avoids PF2’s **3-action cognitive load** but also lacks PF2’s **predictable fairness**.
- DD’s **percentage-based class modifiers** and **draft Oracle/Mirrorsage ceilings** feel closer to **CRPG tuning** than PF2’s **degrees-of-success simulationism**.

### vs Trench Crusade (TCRP / wargame)

- **Tone:** TC is **grim, wound-forward, scarce gear**; DD is **heroic HP + death saves + high-magic delving** — opposite defaults.
- **Pacing:** TC attrition is **physical and moral**; DD attrition is **RP/horn time** (when implemented).
- **Overlap:** Both care about **faith/corruption themes** (DD: alignment/reputation/Corruption damage hook in combat chapter ~6012), but DD still resolves primarily through **HP pools**.
- If the owner meant **Trench Crusade wargame**, comparison is mostly **moot** — different medium (narrative d20 party vs alternating-activation skirmish).

---

## 5. Recommended owner read order

1. `rulebook_output.txt` — Ch. 8 Combat; Resonance System (~5916+, ~6069+)
2. `docs/mechanics/RESONANCE_CANON.md`
3. `docs/mechanics/SESSION_LOOP.md`
4. `docs/mechanics/BALANCE_REPORT.md` (synthesis)
5. `docs/mechanics/BALANCE_PLAYER_CLASSES.md` (class risks)
6. `docs/mechanics/BALANCE_DM_XP.md` (encounter/XP gaps)

---

*No rules invented beyond cited sources. Draft/companion estimates labeled throughout.*
