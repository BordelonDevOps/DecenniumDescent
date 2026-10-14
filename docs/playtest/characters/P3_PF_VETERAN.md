# Player 3 — Pathfinder 2e veteran

**Playtest slot:** P3 · [EXPEDITION_SCENARIO.md](../EXPEDITION_SCENARIO.md) — Glassbite Hollow (EXP-BGR-01), L3 party, 3 non-boss fights  
**Companion build:** Umbrin **Shadow Blade** · **Monk** L3 · **Master** arch path  
**Character name:** Kethren Quiet-Step (House Ashketh contract scout)  
**Data sources:** `builder-races.js`, `racial-variants.json`, `class-details.js`, `class-paths.js`, `class-hit-dice.js`, `resonance-economy.js`, `UMBRIN_LORE.md`, `floor-encounters.json` (T1), `COMBAT_SYSTEM_COMPARE.md`, `SESSION_LOOP.md`, `XP_ADVANCEMENT_CANON.md`, `CLASS_CEILING_CAPS.md`

---

## Persona

I run PF2 tables weekly. I think in **three actions**, **MAP**, **degrees of success**, and **encounter XP budgets**. I will accidentally call the GM “GM” and ask “what’s the DC?” on every roll.

For Decennium Descent I’m trying to be helpful, not smug — but my brain keeps translating:

| PF2 instinct | What DD actually gives me |
|--------------|---------------------------|
| Stride + Strike + Strike (flurry) | **Move + Action + Bonus** (5e-shaped); Flurry of Blows is a **bonus action**, not a 2-action activity |
| Enter stance (1 action) | **Stance Shift — free once per round** (`feat_compendium_output.txt` Monk stances) |
| Focus Point / Ki | **Ki Chain 0–5** (build via Flowing Form, crits, blocks — prose not a tidy action chart) |
| Reaction: Attack of Opportunity | **Opportunity attacks** exist in Ch. 8; Monk also has **Deflect Missile** (reaction) |
| Encounter budget (120 XP moderate at L3) | **No sourced CR→XP budget** — only cumulative level thresholds (`XP_ADVANCEMENT_CANON.md`) |
| Crit on beat DC by 10 | **Nat 20 = auto-hit + double damage dice** (5e rule) |

I picked a **martial with a secondary resource track** because casters would force me to learn **Resonance** on top of relearning action economy. Monk is the closest thing to “I manage my own action puzzle every turn.”

---

## Why this race × class for Blackglass Reach fringe

**Setting (canon):** Blackglass Reach is the surface and near-Murk marches — dark-glass outcrops, watchposts, wary border trade (`UMBRIN_LORE.md`). Our table fiction: Ashketh mercenaries escort a Crystalfront-bound probe into **Yieldheart Caverns** mouth routes (T1 `floor-encounters.json`) after surface scouts reported Automaton drift near the fringe.

| Choice | Rationale (PF2 brain) |
|--------|------------------------|
| **Umbrin** | Dex +2, Cha +1; **Superior Darkvision**; **Murkish** for oath-law slang the GM may throw at us (T7 survivor rumor: “Blackglass Reach mercenary slang” — we’re *from* that culture even if this delve is T1). |
| **Shadow Blade** lineage | **Webstep** (walls/ceilings 1 turn, 1/rest) — verticality on crystal/fringe outcrops without burning a whole turn on Climb. **Nightfang Training**: +10% damage and +2 stealth in total darkness — fringe marches and cavern mouth = dim light most of the time. |
| **Monk L3** | Stance triage (Tiger / Tortoise / Crane), **Ki Chain** resource, **Flurry** for multi-hit turns. **Master** arch path at L3 unlocks **Combo Step** (three different unarmed attacks in one round → stun) — closest DD gets to my Flurry of Blows muscle memory. |
| **Not Oracle / full caster** | Avoids parallel **RC vs RP** confusion while I’m still learning DD. Monk has a **draft minor RP pool** (see sheet) but I don’t plan to nova with it. |

---

## Sheet sketch (L3)

### Identity

| Field | Value |
|-------|-------|
| People / lineage | Umbrin · Shadow Blade |
| Class / path | Monk · Master (arch path, L3) |
| Level / XP | 3 · 900 XP (threshold per `XP_ADVANCEMENT_CANON.md`) |
| Proficiency bonus | +2 |
| Background (table) | Blackglass mercenary scout — transactional, not redeemed (`UMBRIN_LORE.md` playtest note) |
| Languages | Common, Elvish, Murkish |

### Ability scores (27-point buy, racial applied)

| STR | DEX | CON | INT | WIS | CHA |
|-----|-----|-----|-----|-----|-----|
| 10 (+0) | 17 (+3) | 13 (+1) | 10 (+0) | 15 (+2) | 12 (+1) |

### Combat stats

| Stat | Value | Notes |
|------|-------|-------|
| **HP** | **21** | d8 class: L1 9 + L2 6 + L3 6 (`estimateMaxHpFromHitDie`, CON +1) |
| **AC** | **15** | 10 + DEX + WIS (5e-style unarmed defense; **Unarmored Flow** adds % dodge in prose, not flat AC) |
| **Initiative** | +5 | DEX +3, +10% unarmored speed/initiative (rulebook Monk) |
| **Speed** | 30 ft | +10% while unarmored → treat as ~33 ft when GM allows |
| **Ki Chain** | 0–5 | Build via Flowing Form (move + strike alternating), crits (Tiger), blocks/dodges (Tortoise), etc. |
| **RP (draft)** | **2 / 2** | Monk = **minor** Weave tier: Cleric L3 pool 7 × 0.35 → **2** (`resonance-economy.js`, draft) |
| **Reactions** | 1/round | Deflect Missile; opportunity attack if I provoke |

### Racial & class features (L1–L3)

**Umbrin traits:** Superior Darkvision, Sunlight Sensitivity, Umbrin Magic, Umbrin Weapon Training  
**Shadow Blade:** Webstep (1/rest) · Nightfang Training (+10% damage, +2 Stealth in total darkness)  
**Monk L1:** Monk Stances (Tiger / Tortoise / Crane), Flurry of Blows, Flowing Form, Stance Shift (1/round)  
**Monk L2:** Deflect Missile, Step of the Wind  
**Monk L3:** Master arch path · **Combo Step** (three different unarmed attacks in one round → stun target)  
**Proficiencies:** Simple weapons, monk weapons (kama, nunchaku, staff); **no armor** (Unarmored Flow)

### Skills (pick 2 — table)

Acrobatics (+5), Stealth (+5, +7 in total darkness with Nightfang)

### Stances (quick reference)

| Stance | PF2-flavored read | When I use it |
|--------|-------------------|---------------|
| **Tiger** | Aggressive flurry stance | Single-target burst; build Ki on crits |
| **Tortoise** | Raise shield / taunt aura | Hold a choke at cavern mouth; protect P1/P2 |
| **Crane** | Mobile support | Kiting in Echoing Gallery–type terrain (T1 POI) |

---

## Positioning & action plan

Assumed expedition: **3 non-boss fights**, L3 party, fringe → Yieldheart mouth. Horn clock applies if we count this as a full delve (`SESSION_LOOP.md`: 120h; long rest +8h).

### Opening formation (every fight)

```
        [Backline / caster]
   [P2 tanky]     [P4 damage]
        [Kethren — offset flank lane]
              ↑ threat
```

I stay **one move away from the party’s rear flank**, not in front — PF2 taught me martials die when they body-block without stats for it. Tortoise if someone must hold a 5-ft choke; otherwise Tiger on approach.

### Turn template (how I map “3 actions”)

| DD slot | My default | Ki / notes |
|---------|------------|------------|
| **Move** | Stride to flank or Step of the Wind if needed | Flowing Form: if last turn I struck, this turn’s move+strike grants +1 Ki |
| **Action** | Unarmed Strike (different attack mode each round when fishing Combo Step) | Third distinct attack in the round → stun (Master L3) |
| **Bonus** | Flurry of Blows | Fish for Ki on crit (Tiger) |
| **Reaction** | Deflect Missile vs first ranged hit; else OA if enemy flees | — |
| **Free** | Stance Shift once if battlefield changes | Tiger ↔ Tortoise ↔ Crane |

**Webstep (1/rest):** Save for (a) vertical flank on crystal outcrop, (b) escape **Pact Rewrite**-style hazard if GM imports T7 oath vibe, or (c) avoid Automaton patrol surround at the cavern mouth.

### Per-encounter intent (table fiction)

| Fight | Terrain hook | Plan |
|-------|--------------|------|
| **1 — Fringe patrol** | Dim light, narrow glass ridge | Tiger; Nightfang active; build Ki with move-strike; **no Webstep** unless surprised |
| **2 — Cavern mouth swarm** | Echoing Gallery–style noise (T1 POI) | Tortoise near squishies; Deflect Missile for scouts; Combo Step on the leader once Ki ≥ 2 |
| **3 — Depth push before retreat** | Slippery floor / cover | Crane if party is wounded; otherwise Tiger burst + Flurry; **short rest** after for ¼ RP retune if I cast a draft utility |

### Rest budget

- **Short rest between fights:** ¼ max RP (0–1 recovered at 2 max) + Session’s RC+1 rule doesn’t apply to me (`SESSION_LOOP.md`).
- **Long rest:** Only if horn clock allows +8h — full RP, Ki resets narratively, Webstep back.

I am **not** planning to spend draft RP in combat unless the party needs a Weave utility; my kit is at-will martial.

---

## Critiques — DD clarity from a PF2 mindset

These are playtest friction notes, not “PF2 good, DD bad.”

### 1. Action economy is 5e, but class text reads like a CRPG

Ch. 8 gives clean **Move / Action / Bonus / Reaction** (`COMBAT_SYSTEM_COMPARE.md`). Monk stances say **+15% crit**, **−20% accuracy**, **+20% DR** — I want to know: *is that a status bonus, a circumstance bonus, or just “GM decides”?* PF2 trains me to stack categories; DD mixes d20 targets with percentages without a stacking chart (`RULESET_VULNERABILITIES.md` C-06: features not executable).

### 2. Ki Chain lacks a action-by-action chart

**Flowing Form**, crit builds, and **Breath of Focus** (“skip an attack”) are prose-only. I cannot tell if “skip an attack” means **lose my Action** or **decline a Flurry hit** — that matters for my turn budget the way “Spend 1 action to Feint” matters in PF2.

### 3. Stance Shift is free — too good compared to PF2 stance cost

I like the tempo, but it removes the “plan next turn’s stance now” puzzle. If DD wants PF2-like tactical depth, stances might need a cost or a once-per-encounter swap limit. As written I’ll swap every round because the rules tell me to.

### 4. No encounter budget → I cannot sanity-check difficulty

PF2: “Party of 4 at L3, moderate = 120 XP.” DD: I see **CR labels** on bestiary browse and **draft** sim notes (e.g. L3 vs CR 5 Bloom ≈ hard, `BALANCE_COMBAT_SIM.md`) but **no sourced award table** (`XP_ADVANCEMENT_CANON.md` BLOCKED). I don’t know if three fringe fights should cost 1 or 3 short rests.

### 5. Degrees of success don’t exist — but crit rules are harsher in a different axis

PF2 crits on +10; DD **nat 20 always crits**. I’ll overestimate crit rate on high-AC targets. Conversely, no **crit fail** on saves means control spells feel binary compared to PF2.

### 6. Conditions in Session are labels, not mechanics

`SESSION_LOOP.md`: conditions are free text — no duration, no auto flat check, no MAP. I’ll track **Stunned** from Combo Step on paper, but PF2 expects Stunned 1 vs Stunned 3. DD doesn’t say which.

### 7. Percentage modifiers vs AC math

I estimate AC 15; enemies with “−20% accuracy” in Tortoise aura aren’t the same as **AC +2** or **flat −2 to attack rolls**. Sim tools use AC and d20 (`BALANCE_COMBAT_SIM.md`); class prose uses %. Reconcile before I trust sims.

### 8. Resonance is well-documented — but multiclass parties hurt my brain

`RESONANCE_CANON.md` is clear for primary casters. At a mixed table (Oracle RC + Mage RP + my 2 RP draft), Session shows different columns — good — but **short rest RC +1 for Oracle** is a companion default, not trigger-based recovery. PF2 me wants one recovery diagram per resource.

### 9. Draft caps exist for six classes — Monk isn’t one of them

`CLASS_CEILING_CAPS.md` covers Mirrorsage, Oracle, Paladin, Warrior, Dragoon, Tinker. Monk **Master** capstone text includes **“+100% damage”** and **auto-crit at max Ki** with no draft ceiling. I’ll play L3 only, but I notice the gap.

### 10. Blackglass / tier continuity is lore-rich, mechanics-thin

T7 **Pactbound Arena** has oath-law vibe (`floor-encounters.json`, draft). Our fringe expedition is T1-mapped Yieldheart — fine fictionally, but **encounter procedures** (Automaton patrol scope, safe haven rules) are briefs not stat blocks. PF2 expects a creature stat block every time; DD bestiary often has identity/CR without full combat columns (`BESTIARY_INGEST.md`).

---

## Questions I’d ask the DM (PF2 habits)

1. When I **Combo Step** for stun, what’s the save DC — 8 + prof + WIS? Fixed DC? No save?
2. Does **Sunlight Sensitivity** apply to crystal lantern light in Yieldheart, or only true sunlight?
3. Is **Flowing Form** “move then strike” or “move and strike” on the same turn — and does Flurry count as “strike” for that?
4. For **Nightfang +10% damage**, is that applied to dice or to the final total after doubling on crit?
5. What’s the **encounter budget** for this three-fight day — and do we get XP via draft award or milestone?
6. If I use **Webstep** on a ceiling, do opportunity attacks trigger when I leave a tile?

---

## Roleplay choices (suboptimal-adjacent, not stupid)

- I **negotiate before rolling** at the fringe — Blackglass oath-law habit — even when P4 wants to alpha strike (matches T7 encounter *vibe*, not mechanics).
- I **refuse “redemption” arcs** for Umbrin; I push transactional payment (`UMBRIN_LORE.md`).
- I will **call out flank positioning** every round until the table tells me 5e flanking isn’t a rule — then I’ll sulk and use Help instead.

---

*Playtest persona doc — P3 PF2 veteran · 2026-07-30 · no commit.*
