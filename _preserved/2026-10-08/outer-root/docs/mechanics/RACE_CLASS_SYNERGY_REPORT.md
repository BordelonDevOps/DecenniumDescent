# Race × Class Synergy Report

**2026-07-30 — DRAFT / PROVISIONAL (race-class matrix sim v1)**

> **DRAFT / PROVISIONAL** — automated harness output. Not rules-complete combat. Do not treat as canon balance.

## Inventory

| Metric | Count |
| --- | ---: |
| Parent races (`races.js`) | 14 |
| Subrace variants (people picker / `races.js` subraces) | **45** |
| `racial-variants.json` enriched rows | 42 |
| Synthetic fallback rows (missing JSON) | 3 (Stone Drakari, Gale Drakari, Wave Drakari) |
| Canon classes (`canon-classes.js`) | **17** |
| **Race × class matrix** | **765** |
| Non-boss bestiary foes | 698 |
| Fight evaluations run | **11,475** |

## Method (assumptions)

- **Level:** 5 — Primary class stat starts at 14 (+2 mod); Constitution at 12 (+1). Race abilityBonuses applied. Human: +1 all scores (Versatility baseline).
- **HP:** `class-hit-dice.js` rulebook formula + race size/regen modifiers (draft).
- **AC / attacks:** 10 + DEX mod + armor tier (heavy +6, medium +3, light +1, unarmored Monk +WIS if applicable, none +0). +1 from Natural Armor trait. Level-5 attack profiles by class role: martials 2× weapon, casters 1× spell/force, support 1× mixed. Damage = die average + ability mod.
- **Race traits:** Percent bonuses parsed from racial-variants ability/feat text and races.js traits (damage %, regen, miss chance, resist DR). Missing Drakari variants use parent-race Drakari defaults.
- **Foes:** Non-boss only: exclude Gate Guardian tag and floor-encounters.json boss names. Requires AC+HP+structured combat from Excel ingest. Sample pools: solo CR 1/2/3/4 (3 each), party CR 5 (3).
- **Party template:** Fixed Warrior + Cleric + Mage L5; 4th slot = tested race/class combo.
- **Incoming damage:** Structured at-will + draft recharge cadence from monster-combat.mjs; CR proxy fallback if payload missing.
- **Scoring:** survivalPct = max(0, 100 − expectedLoss/hp×100). deathFlag = expectedLoss ≥ hp. synergyScore = mean solo survivalPct. Party weight 30%.

Excluded bosses: Vaskor, the Stone Maw; The Bloom That Hungers; Ashthirst the Hollow; Gor Vekk, Architect of Ends; Choralith, Voice Below; Lumen of the Shattered Thread; Xarog, the Pactbound Furnace; Eirfax, the Dusk Crowned; Threxus, the Iron Spiral; The Marquis of Silence.

## Aggregate results

| Metric | Value |
| --- | ---: |
| Mean synergy score | 21 |
| Mean solo survival % | 4.9% |
| Mean solo death-flag rate | 84.1% |
| Combos with 0% solo death flags | 0 / 765 |
| Combos with any solo death flag | 765 / 765 |

## Top 5 synergies

| Rank | Combo | Synergy | Solo surv% | Solo death% | Party surv% | HP | AC | DPR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Swamp Troll Warrior | 60.5 | 55.2 | 8.3 | 72.8 | 54 | 17 | 15 |
| 2 | Stone Troll Warrior | 60.5 | 55.2 | 8.3 | 72.8 | 54 | 17 | 15 |
| 3 | Blood Troll Warrior | 60.5 | 55.2 | 8.3 | 72.8 | 54 | 17 | 15 |
| 4 | Spore Mycelian Warrior | 52.1 | 44.1 | 8.3 | 70.9 | 50 | 16 | 15 |
| 5 | Decay Mycelian Warrior | 52.1 | 44.1 | 8.3 | 70.9 | 50 | 16 | 15 |

**Why they spike:** Troll/Mycelian CON+STR bonuses on d12 Warrior chassis (54 HP, AC 17, ~15 DPR) plus parsed regen/Natural Armor/DR; only fail 1/12 solo samples (CR 4 band). Party slot adds ~73% survival on CR 5 samples.

## Top 5 traps

| Rank | Combo | Synergy | Solo surv% | Solo death% | Party surv% | HP | AC | DPR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Tinker Gnome Mage | 14.6 | 0 | 100 | 48.6 | 27 | 10 | 5.5 |
| 2 | Tinker Gnome Mirrorsage | 14.6 | 0 | 100 | 48.6 | 27 | 10 | 5.5 |
| 3 | Tinker Gnome Wizard | 14.6 | 0 | 100 | 48.6 | 27 | 10 | 5.5 |
| 4 | Arcanist Gnome Mage | 14.6 | 0 | 100 | 48.6 | 27 | 10 | 5.5 |
| 5 | Arcanist Gnome Mirrorsage | 14.6 | 0 | 100 | 48.6 | 27 | 10 | 5.5 |

**Why they fail:** Small Gnome (no CON bump) on d6 Mage/Wizard/Mirrorsage — 27 HP, AC 10, ~5.5 DPR. Solo death-flag on all 12 samples (CR 1–4 with draft recharge). Party anchor lifts party surv to ~49% but cannot offset solo fragility.

## Trait / class interaction spikes (vs class average)

| Combo | Score | Δ vs class avg | Δ vs race avg |
| --- | --- | --- | --- |
| Swamp Troll Warrior | 60.5 | 16.7 | 33.5 |
| Stone Troll Warrior | 60.5 | 16.7 | 33.5 |
| Blood Troll Warrior | 60.5 | 16.7 | 33.5 |
| Swamp Troll Soldier | 49.9 | 16.7 | 22.9 |
| Stone Troll Soldier | 49.9 | 16.7 | 22.9 |
| Blood Troll Soldier | 49.9 | 16.7 | 22.9 |
| Swamp Troll Ranger | 44.7 | 14.6 | 17.7 |
| Stone Troll Ranger | 44.7 | 14.6 | 17.7 |

## Trait / class traps (vs class average)

| Combo | Score | Δ vs class avg | Δ vs race avg |
| --- | --- | --- | --- |
| Tinker Gnome Warrior | 35.5 | -8.3 | 16.7 |
| Arcanist Gnome Warrior | 35.5 | -8.3 | 16.7 |
| Prankster Gnome Warrior | 35.5 | -8.3 | 16.7 |
| Imperial Human Warrior | 35.5 | -8.3 | 16.7 |
| Nomadic Human Warrior | 35.5 | -8.3 | 16.7 |
| Scholarly Human Warrior | 35.5 | -8.3 | 16.7 |
| Tinker Gnome Soldier | 27 | -6.2 | 8.2 |
| Arcanist Gnome Soldier | 27 | -6.2 | 8.2 |

## Limitations

1. **Draft combat only** — no action economy, spells beyond a single attack profile, conditions, or positioning.
2. **Simplified race traits** — regex parsing of variant text; many feats (1/rest, 1/combat) converted to uptime fractions.
3. **Fixed ability array** — not full point-buy or rolled stats; Human uses +1-all baseline.
4. **Monster recharge** — draft cadence model may overstate AoE/recharge damage on excel-sandbox rows.
5. **CR band sampling** — 3 foes per CR band, not exhaustive bestiary sweep.
6. **3 missing `racial-variants.json` rows** — Stone/Gale/Wave Drakari use parent-race defaults.
7. **Party template fixed** — Warrior/Cleric/Mage anchor; rotating slot only.

## Artifacts

- JSON: `scripts/output/race-class-matrix.json`
- Runner: `node scripts/race-class-matrix-sim.mjs`

---

*Continuity stamp: 2026-07-30 — DRAFT / PROVISIONAL (race-class matrix sim v1)*
