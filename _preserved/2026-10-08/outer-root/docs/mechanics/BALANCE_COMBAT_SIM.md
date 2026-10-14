# Combat-balance simulation

**Run:** 2026-07-30  
**Runner:** `node scripts/combat-balance-sim.mjs`

## Scope and method

This is a deterministic first-pass sanity check, not a rules-complete combat engine.

- Player HP uses the companion's published hit-die rule in `src/data/class-hit-dice.js`: maximum die + Constitution modifier at L1, then average die + Constitution modifier per later level.
- Player attack assumptions are intentionally visible in the script: mundane martial weapons use the displayed die plus a primary modifier, and only source-defined Mage `Force Spike` / `Magic Missile` entries are used.
- `The Bloom That Hungers` and `Vaskor, the Stone Maw` use their authored AC, HP, CR, and XP blocks (10 gate guardians total). Re-ingest removed 9 duplicate stub rows; **0** entries now use fabricated AC 10 / HP 1.
- **698 / 708** entries are metadata-only (name, CR, XP, zone, loot) — the Excel `Monsters` sheet has **no AC/HP/attack columns**. Incoming damage for non-guardian foes still requires a labeled CR proxy or future stat source.
- Therefore, incoming monster damage is a clearly labeled **provisional CR proxy** (36 raw DPR at CR 5; 54 at CR 8; then a stated hit chance). It is not companion data and cannot establish a final damage verdict.

## Results

| Scenario | Source foe / party | Estimated result | XP result | Verdict |
|---|---|---|---|---|
| L3 party of four | The Bloom That Hungers (CR 5, AC 15, 112 HP) vs Warrior / Paladin / Cleric / Mage | 14.9 party DPR; **8 rounds** to win. Draft `vine-maw`: **62.4 HP**, 63.7% of the 98-HP party | 1,800 listed XP → 450 each if split four ways | **Hard but survivable under draft at-will** |
| L8 party of four | Vaskor, the Stone Maw (CR 8, AC 17, 168 HP) vs Warrior / Paladin / Cleric / Mage | 32.3 party DPR; **6 rounds** to win. Draft `stone-maw`: **115.2 HP**, 46.8% of the 246-HP party | 3,900 listed XP → 975 each if split four ways | **Hard but survivable under draft at-will** |
| L5 single-target comparison | Mage vs Warrior, target AC 15 | Mage: 27 HP, 4.2 sustained `Force Spike` DPR / 10.5 `Magic Missile` burst. Warrior: 55 HP, 12.3 DPR from two d10+4 attacks | N/A | Durability split is appropriate; caster throughput remains **unknown** beyond the narrow source-defined spells |

The L3 encounter is a Tier 2 gate-guardian test, rather than a normal Tier 1 roaming encounter: the companion's floor data contains tier labels and bosses but no executable encounter roster or budget. Treat it as a deliberately hard boss sanity check, not proof that it is a standard L3 fight.

## Script output

```text
Decennium Descent combat balance simulation
Bestiary ingest: 708 entries from Bestiary.xlsx (+ bestiary_metadata_source.xlsx metadata supplement); 10 have authored AC/HP (gate guardians); 698 are metadata-only (no fabricated AC 10 / HP 1).
Structured combat quality: 10/708 entries have a usable draft combat payload.
Incoming damage prefers a structured at-will action; absent payloads remain clearly labeled CR proxies.

Scenario 1 — L3 party vs Tier 2 gate guardian
  Foe: The Bloom That Hungers — CR 5, AC 15, HP 112, 1800 listed XP
  Party DPR: 14.9 against AC 15; expected win: 8 rounds
  Enemy loss proxy: 21.6 DPR × 8 = 172.8 HP (176.3% of party HP)
  XP split (listed XP / 4): 450 each; award formula: not encoded
  Verdict: TOO HOT under proxy (likely TPK); final enemy-damage verdict UNKNOWN (no source attacks).

Scenario 2 — L8 party vs mid-tier gate guardian
  Foe: Vaskor, the Stone Maw — CR 8, AC 17, HP 168, 3900 listed XP
  Party DPR: 32.3 against AC 17; expected win: 6 rounds
  Enemy loss proxy: 32.4 DPR × 6 = 194.4 HP (79.0% of party HP)
  XP split (listed XP / 4): 975 each; award formula: not encoded
  Verdict: hard but survivable under proxy; final enemy-damage verdict UNKNOWN (no source attacks).

Scenario 3 — L5 glass-cannon caster vs martial frontliner (target AC 15)
  Mage: 27 HP; Force Spike sustained 4.2 DPR; Magic Missile burst 10.5 DPR.
  Warrior: 55 HP; two d10+4 attacks 12.3 DPR.
  Comparison: Mage has 49.1% of Warrior HP; sustained DPR is 34.2% and listed burst is 85.0%.
  Verdict: chassis gap is appropriate; full caster output remains UNKNOWN.

Scenario 4 — XP outcome
  Both simulations split each monster's listed `xp` evenly among four PCs.
  The companion exposes level thresholds and per-monster XP values, but no encounter-XP award or multiplier formula.
```

## XP outcome

`bestiary_data_full.json` supplies static per-monster `xp` values, and the Character Builder exposes level thresholds (L3→L4: 1,500 XP; L8→L9: 6,500 XP). No rulebook or companion encounter-award, party-size, difficulty, or multiplier formula was found. The script reports an **assumed equal split**, not a verified award rule:

- Bloom: 450 XP per L3 character, or 30% of the next 1,500-XP threshold.
- Vaskor: 975 XP per L8 character, or 15% of the next 6,500-XP threshold.

## Verdict and top fixes

**Overall verdict: damage and XP are not yet balance-verifiable.** The proxy makes the L3 Bloom fight too hot and the L8 Vaskor fight hard but survivable, while the Mage/Warrior chassis gap looks directionally reasonable. These are useful alerts, not final tuning results.

1. Add structured monster actions: attack bonus, damage dice/type, multiattack, save DC, recharge, conditions, resistances, and target rules. Source AC/HP/attacks from a future column set or author pass — not present in `Bestiary.xlsx` or `bestiary_metadata_source.xlsx` today.
2. ~~Replace the 708 placeholder creature blocks~~ **Done (2026-07-30):** re-ingest removed fabricated AC 10 / HP 1 and duplicate gate-guardian stubs. Metadata rows are real; combat stats remain absent except on 10 gate guardians.
3. Publish encounter composition/budgets by floor and an XP-award formula, including party-size and boss multipliers; otherwise static XP cannot be evaluated.
4. Complete spell damage, scaling, action, and resource fields—especially for Mage—before making martial/caster parity changes.

## Structured combat pilot rerun — 2026-07-30 (post re-ingest)

Re-ingest verified: **708** live entries, **0** fabricated AC 10 / HP 1, **10** draft `combat` payloads on gate guardians. Sim output unchanged for Bloom/Vaskor (`node scripts/combat-balance-sim.mjs`):

- **Bloom:** draft `vine-maw` supplies 7.8 expected DPR against AC 15, or **62.4 HP / 63.7%** of the L3 party over eight expected rounds. Verdict: **hard but survivable under draft at-will** (recharge/area still excluded).
- **Vaskor:** draft `stone-maw` supplies 19.2 expected DPR against AC 16, or **115.2 HP / 46.8%** of the L8 party over six expected rounds. Verdict: **hard but survivable**.

The outcome is now tied to draft stat payloads instead of a CR proxy for these encounters, but it is not a final balance verdict until cited monster sources and full action-economy simulation exist.

## Bloom retune rerun — 2026-07-30

After owner-directed draft retune of **The Bloom That Hungers** structured at-will action only (`vine-maw` count 2 → 1; recharge/save payloads unchanged):

| Scenario | Source foe / party | Estimated result | XP result | Verdict |
|---|---|---|---|---|
| L3 party of four | The Bloom That Hungers (CR 5, AC 15, 112 HP) vs Warrior / Paladin / Cleric / Mage | 14.9 party DPR; **8 rounds** to win. Draft `vine-maw` incoming loss: **62.4 HP**, **63.7%** of the 98-HP party | 1,800 listed XP → 450 each if split four ways | **Hard but survivable under draft at-will**; recharge/area damage still excluded |
| L8 party of four | Vaskor, the Stone Maw (CR 8, AC 17, 168 HP) vs Warrior / Paladin / Cleric / Mage | 32.3 party DPR; **6 rounds** to win. Draft `stone-maw` incoming loss: **115.2 HP**, 46.8% of the 246-HP party | 3,900 listed XP → 975 each if split four ways | **Hard but survivable under draft at-will** |

```text
Scenario 1 — L3 party vs Tier 2 gate guardian
  Foe: The Bloom That Hungers — CR 5, AC 15, HP 112, 1800 listed XP
  Party DPR: 14.9 against AC 15; expected win: 8 rounds
  Enemy loss (draft structured at-will action "vine-maw"): 7.8 DPR × 8 = 62.4 HP (63.7% of party HP)
  XP split (listed XP / 4): 450 each; award formula: not encoded
  Verdict: hard but survivable; final enemy-damage verdict remains DRAFT (no cited source attacks).
```

Bloom now lands in the requested **40–70%** draft tuning band for sustained at-will damage. Spore Burst and other non-at-will actions remain outside this pass.

## Combat sandbox rerun — 2026-07-30 (pm)

**Source:** `Bestiary.xlsx` combat columns via `scripts/generate_bestiary_combat_sandbox.py` + re-ingest.

| Metric | Value |
|--------|------:|
| Entries with AC/HP | 708 |
| Structured combat payloads | 708 |
| excel-sandbox drafts | 698 |
| companion-authored (gate guardians) | 10 |

### Expanded CR-band scenarios

| Scenario | Foe | Party-loss % | Verdict |
|----------|-----|-------------:|---------|
| L3 vs Bloom (CR 5 guardian) | The Bloom That Hungers | 63.7% | hard but survivable |
| L8 vs Vaskor (CR 8 guardian) | Vaskor, the Stone Maw | 46.8% | hard but survivable |
| L3 vs CR 1 sandbox | Kraken Priest | 6.6% | moderate (foe dies fast) |
| L5 vs CR 3 sandbox | Gloom Weaver | 5.6% | moderate |
| L8 vs CR 10 sandbox | Lizardfolk | 53.9% | hard but survivable |

Gate guardians unchanged (Bloom/Vaskor in 40–70% band). Low-CR sandbox foes die in ~2 rounds so party-loss % is low — expected for draft bands. CR 10 sandbox lands in band.

**Overall:** Sandbox enables structured sim across CR bands; all results remain **draft**.

## Recharge enrichment — Worker 4 / 5 (2026-07-30)

**Source:** `Bestiary.xlsx` recharge columns via `scripts/author_recharge_attacks.py` + ingest + `expectedRechargeDpr()` in `src/lib/monster-combat.mjs`.

| Metric | Value |
|--------|------:|
| Creatures with recharge payloads | **26** (10 gate guardians + 16 CR-band samples) |
| Excel columns added | Recharge Name/Kind/Bonus/Damage/Type/Save DC/Save Ability/Roll |
| Sim model | At-will + expected recharge DPR (draft cadence; see `MONSTER_COMBAT_SCHEMA.md`) |

### Recharge assumptions (sim)

1. Recharge available round 1; steady-state availability = P(d6 ≥ minimumRoll) (e.g. `5-6` → **33%**/round).
2. Save recharges: **55%** fail rate; success halves damage.
3. Area recharges modeled as single-target expected damage (conservative lower bound vs multi-target).
4. Recharge stacks with at-will in the same round when available (upper-bound burst).

### Impact vs at-will-only rerun

| Scenario | At-will only | + Recharge | Party-loss % | Verdict |
|----------|-------------:|-----------:|-------------:|---------|
| L3 vs **The Bloom That Hungers** | 7.8 DPR | **8.4 DPR** (+0.6) | **68.4%** (Phase C: **1d8**, recharge **6**) | **hard but survivable** — in 40–70% band |
| L8 vs **Vaskor, the Stone Maw** | 19.2 DPR | **23.9 DPR** (+4.7) | **58.2%** (was 46.8%) | **hard but survivable** — still in band |
| L5 vs **Gloom Weaver** (CR 3) | 5.0 DPR | **7.7 DPR** (+2.7) | **8.7%** | moderate (short fight) |

**Takeaway:** Phase C retuned Bloom Spore Burst to **1d8 poison** (DC 14) with recharge **6** only — L3 sim **68.4%** party loss, within the 40–70% draft band. Vaskor unchanged at **58.2%**.

```text
Decennium Descent combat balance simulation (Phase C)
Bestiary ingest: 708 entries; 708 have AC/HP; 708 with structured combat; 26 with recharge payloads.
Bloom: at-will 7.8 + recharge 0.6 = 8.4 DPR × 8 rounds = 67.0 HP (68.4% party HP)
Vaskor: at-will 19.2 + recharge 4.7 = 23.9 DPR × 6 rounds = 143.1 HP (58.2% party HP)
```

**Worker 4 / 5 continuity stamp:** Recharge columns authored Excel-first; ingest maps to `combat.attacks[]`; sim optionally includes expected recharge DPR. No commit.
