# Player 4 — Optimizer / MMO-minded

**Playtest slot:** 4th party member (rotating synergy slot)  
**Level band:** L3 smoke + first dungeon floor  
**Companion refs:** `RACE_CLASS_SYNERGY_REPORT.md` · `CLASS_CEILING_CAPS.md` · `resonance-economy.js` · `class-hit-dice.js`

---

## Persona

**Name:** Kael "Meterwatch" Grunn  
**Voice:** Parses fight logs, compares race×class spreadsheets, and asks "what's our burst window?" before every pull. Treats the table like an MMO training dummy run: track effective HP, sustained vs burst DPR, and whether draft caps actually stop infinite loops.

**Goals this session**

- Validate the **#1 matrix synergy** at early levels (not just the L5 harness).
- **Stress `CLASS_CEILING_CAPS.md`** on Warrior — Juggernaut prose vs draft guardrails.
- Confirm **non-caster resource clarity**: Warrior has **no Weave RP pool** (`NO_POOL_CLASSES` in `resonance-economy.js`); Session should show martial resources only.

**Anti-goals:** Won't pick Gnome caster glass (matrix bottom traps at 27 HP / 100% solo death-flag). Won't argue for multiclass until single-class ceiling behavior is logged.

---

## Strong L3 pick: Swamp Troll · Warrior (Juggernaut)

| Field | Value |
| --- | --- |
| People | **Troll** → **Swamp Troll** |
| Class | **Warrior** |
| Arch path (L3) | **Juggernaut** (`class-paths.js`) |
| Fighting Style | Great Weapon Fighting (maximize nova swing) |
| Alignment | Neutral (Ironskin hero path later at L10) |

### Why this combo (real data)

Source: `scripts/output/race-class-matrix.json` + `RACE_CLASS_SYNERGY_REPORT.md` (L5 harness; extrapolated to L3 below).

| Metric | Swamp Troll Warrior | Notes |
| --- | ---: | --- |
| Synergy score | **60.5** | Rank **#1** of 765 combos |
| Δ vs Warrior class avg | **+16.7** | Largest class-relative spike in matrix |
| Δ vs Troll race avg | **+33.5** | Troll chassis favors martial, not caster |
| HP (L5 sim) | **54** | d12 + CON + Large +8% draft modifier |
| AC (L5 sim) | **17** | Heavy +6, DEX 0, **Natural Armor +1** |
| DPR (L5 sim) | **15** | 2× martial attack profile at L5 |
| Solo death-flag rate | **8.3%** | Best-in-matrix; only 1/12 CR samples fail |
| Party survival (CR 5 slot) | **72.8%** | Strong 4th-slot anchor |

**HP — race + class**

- Parent **Troll** (`races.js`): CON +2, STR +1, **Large**, traits **Regeneration**, **Powerful Build**, **Natural Armor**, **Keen Smell**.
- **Swamp Troll** (`racial-variants.json`): **Unnatural Regeneration** — heal 5% max HP every 2 turns in combat; **Primal Recovery** — once/combat clear a debuff.
- **Warrior** hit die: d12 (`class-hit-dice.js`).
- L3 HP (standard array CON 12 + racial +2 → mod +2): `estimateMaxHpFromHitDie(3, +2, Warrior)` = **32**, + **~8% Large** draft ≈ **35 HP** at L3 (sim reports **54 HP** at L5 with same assumptions).

**Traits — effective tankiness**

- **Natural Armor +1 AC** (parsed in matrix `traitMods`).
- **Regen 5%/2 turns** ≈ **~2 HP/round** at L3 (~1.75 HP on odd turns) — attrition win condition.
- **10% DR** not on Troll parent; Troll spike is HP/AC/regen, not resistance padding (contrast Flame Drakari Warrior at 39 HP / synergy 39).

**DPR — L3 vs L5**

- L5 sim **15 DPR** = two weapon attacks (Extra Attack L5) + STR mod + Fighting Style.
- **At L3** (no Extra Attack yet): sustained **~7–8 DPR** (1× martial weapon + STR +2).
- **Nova ceiling L3:** **Action Surge** (L2) → second Attack action ≈ **~15 damage in one round** before mutations/crits — matches half the L5 sim DPR in a single burst turn.

**Why not Dragoon / Paladin / caster**

- Swamp Troll Dragoon: synergy **24.6**, solo death **66.7%**, DPR **7.5** at L5 sim — same burst label, far worse survival.
- Tinker Gnome Mage: synergy **14.6**, **100%** solo death-flag — hard avoid.
- Warrior skips Weave entirely — cleaner meter for **martial-only** cap testing.

---

## Sheet sketch (L3)

Build in Companion → **CHARACTERS** → save as `P4 Meterwatch`.

### Ability scores (standard array + Troll ASI)

| Ability | Base | Racial | Total | Mod |
| --- | ---: | ---: | ---: | ---: |
| STR | 14 | +1 | 15 | +2 |
| DEX | 10 | — | 10 | +0 |
| CON | 12 | +2 | 14 | +2 |
| INT | 8 | — | 8 | −1 |
| WIS | 13 | — | 13 | +1 |
| CHA | 10 | — | 10 | +0 |

*(Matrix sim uses primary 14 / CON 12 before racial; this array matches that spine.)*

### Combat snapshot

| Stat | Value |
| --- | --- |
| Level | 3 |
| Max HP | **~35** (32 hit-die + Large draft) |
| AC | **17** (chain/plate heavy +6, DEX +0, Natural Armor +1) |
| Main weapon | Greataxe 1d12+2 (GWF) |
| Proficiency | +2 |
| Attacks / turn | **1** (Extra Attack at L5) |

### Class features owned at L3

| Level | Feature |
| ---: | --- |
| 1 | Fighting Style, **Second Wind** |
| 2 | **Action Surge** (1 / short rest) |
| 3 | **Martial Archetype — Juggernaut** |

### Juggernaut hooks relevant at L3

From `class-paths.js` (arch path passives):

- **Mutation Efficiency:** *May have **2 active mutations at once** (Lv 3).*
- **Brutal Fortitude:** +1 DR per Brutality stack (max +3) — track stacks on sheet.
- **Overpressure Response:** Once/round, when crit — **1 free mutation activation**.

*(Full mutation kit expands L11+ in `class-draft-levels.js`; L3 playtest uses arch path text only.)*

### Resonance / martial resources

| Resource | L3 state | Recovery |
| --- | --- | --- |
| **Weave RP** | **None** — Warrior ∈ `NO_POOL_CLASSES` | N/A |
| **Second Wind** | 1 / **short rest** (L1) | Short rest |
| **Action Surge** | 1 / **short rest** (L2) | Short rest |
| **Mutations (Juggernaut)** | 2 concurrent actives (arch L3 prose) | Per serum/mutation rules — **1 activation / round** under draft cap |
| **Primal Recovery** | 1 / **combat** (Swamp Troll feat) | Reset each combat |
| **Regeneration** | 5% max HP / 2 turns | Passive |

**Session Tracker expectation:** Pool column should **not** show RP for this PC. Log Second Wind + Action Surge manually on the encounter worksheet.

---

## Nova vs attrition plan

### Opening nova (single-target elite / CR spike)

**Turn 1 — burn window**

1. Move into melee (Large reach/tank position).
2. **Activate 1 mutation** (Juggernaut cap: counts as the round's activation even if arch text implies two *prepared* actives).
3. **Attack** (greataxe).
4. **Action Surge** → **second Attack** action → second greataxe swing.

**Target math (rough):** 2 × (6.5 + 2) ≈ **17 damage** baseline; GWF rerolls + mutation rider (table-defined) on top. Goal: delete **≥40%** of a CR-appropriate bruiser's HP before it acts twice.

**Do not** stack a third mutation activation same round unless logging a cap violation — see caps section.

### Attrition (multi-pull / low burst)

- **Front line:** AC 17 + 35 HP; expect to absorb **~2–3 CR-appropriate hits** before Second Wind.
- **Regen:** ~2 HP every other turn → **~6–8 HP** over a 5-round skirmish without spending resources.
- **Second Wind:** bump effective HP ~**1d10+3** (L3 Warrior level) once per short rest — use when HP < 50% or healer RP/RC is dry.
- **Primal Recovery:** hold for **stun/root/poison** that blocks Action Surge turn; once/combat.
- **Action Surge:** hold for **add spawn** or **execute window**; do not open on trash unless party comp lacks AoE.

### Rest cadence

| Rest | Recover |
| --- | --- |
| Short | Second Wind, Action Surge |
| Long | All martial + full HP; mutation prep refresh per table |

---

## Draft cap collisions (`CLASS_CEILING_CAPS.md`)

Warrior is a **flagged ceiling class** (`class-ceiling-caps.js`). At L3, Juggernaut already bumps prose against draft guardrails:

| Conflict | Arch / class prose | Draft cap (`CLASS_CEILING_CAPS.md`) | P4 playtest ruling |
| --- | --- | --- | --- |
| **Concurrent mutations** | Juggernaut L3: **2 active at once** | **3 prepared (L11+)**; **1 activation / round** | **Cap wins:** two serums may be *prepared*, but only **1 activation per round** unless Reflexive Mutation (L17). Log if Overpressure free activation stacks. |
| **Action Surge + mutation** | Action Surge grants second Attack action | **Action Surge + 1 mutation activation max / round** | Legal nova: Surge for attacks, **one** mutation activation same round. |
| **Overpressure Response** | **1 free mutation activation** when crit received | **1 activation / round** total | Treat free proc as consuming the round's activation slot — no double-mutate turns. |
| **Brutality Threshold** | L12 draft: 100% max HP dealt → Transcendent 3 rounds | Same in caps | **Not at L3** — note for L12+ retest; don't pre-track. |
| **Serum Overclock** | L9: inject 2 serums at once | Counts as **1 activation** | Future level; no conflict at L3. |

**Builder/Sheet:** expect **Draft ceiling caps** callout on Warrior — informational only (`RULESET_VULNERABILITIES.md` CL-01). P4 should **keep a paper ledger**: activations/round, Action Surge usage, regen ticks, cap overrides.

**Resonance cross-note:** Caps doc § Cross-class — Warrior has no RP curve; no burnout/retune interaction. If party forces a multiclass dip later, action-economy caps remain **shared** (still 1 mutation activation / round total).

---

## Playtest checklist (P4)

- [ ] Create **Swamp Troll Warrior L3 Juggernaut** in Builder; confirm **no RP slider** on Weave tab.
- [ ] Sheet shows **Warrior draft ceiling** callout.
- [ ] Session load → **no RP pool** on combatant row.
- [ ] Run one **nova turn** (Action Surge + 1 mutation) and log damage vs party baseline.
- [ ] Run one **attrition pull** (5+ rounds) and log regen + Second Wind value.
- [ ] Record any **Juggernaut vs cap** conflict for author review (Overpressure, dual-active mutations).

---

*Continuity: 2026-07-30 — P4 optimizer playtest persona; matrix rank #1 combo at L3 extrapolation; Warrior draft caps stressed.*
