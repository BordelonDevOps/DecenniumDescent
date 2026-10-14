# Decennium Descent balance report

**Owner-facing synthesis:** 2026-07-30  
**Inputs:** player-class audit, DM/XP audit, and deterministic combat sanity simulation.

## 1. Executive verdict

**No: damage, XP, and classes cannot yet be called “working” as balanced game systems.**

- **Damage:** the available combat results are directional alerts, not tuning proof. Most enemy stat blocks have no executable attacks, while many high-impact class and spell features lack final action, targeting, scaling, duration, save, recharge, and stacking rules.
- **XP and encounter math:** the editable rulebook confirms L1–L20 XP thresholds and total-level advancement; **Builder now uses confirmed thresholds** (`xp-economy.js`). No reviewed source establishes XP **awards**, CR-to-XP canon, encounter budgets, party adjustments, or reward handling. Bestiary XP values and draft Session awards remain unverified/reference.
- **Classes:** the roster has readable roles and broadly sensible HP bands, but only fragments of its resource and feature rules are complete enough to compare numerically. Several classes have unconstrained ceilings.

The project is ready to convert its existing content into testable rules and tools. It is **not** ready for balance claims, automated encounter recommendations, or source-canon XP awards.

## 2. Cross-cutting blockers

1. **Rules are descriptive rather than executable.** Core combat payloads frequently omit action type, range, targets, hit/save rules, damage/healing, duration, recharge, scaling, conditions, and stacking limits.
2. **Source authority is unresolved.** Rulebook and companion data conflict on armor/AC, class access, and XP thresholds. The confirmed XP table does not include XP-award/CR/encounter rules; companion UI values must not be presented as canon without citations.
3. **The Bestiary cannot drive full combat math yet.** Re-ingest (2026-07-30 pm) confirmed **708 real rows** from **`Bestiary.xlsx`** (names + gate `lootTable`) with metadata supplemented from `final_bestiary.xlsx`; neither workbook has AC/HP/attack columns. Only **10 authored gate guardians** carry companion AC/HP and draft `combat` payloads.
4. **No encounter-to-progression loop exists.** Session does not aggregate encounter value, calculate difficulty, award/split XP, or write progress back to saved characters.
5. **No shared benchmark suite exists.** Class comparisons, monster tuning, encounter difficulty, rest cadence, gear assumptions, resistance frequency, and floor budgets need a single published test matrix.
6. **Resource/action economy is unbounded in high-impact cases.** RP discounts, overcast, retuning, Oracle RC recovery, copied abilities, summons/deployables, and bonus-action wording cannot be evaluated consistently until their floors, eligibility, recovery, and per-turn limits are explicit.

## 3. Player-class risks

1. **Mirrorsage — highest ceiling risk.** Mimicry, stored Echoes, cost reduction, and copied abilities lack an eligibility list, ceiling, action cost, duration, and exclusions for unique or boss effects. It can potentially exceed the original class while retaining its own kit.
2. **Oracle — draft content can become encounter-renewable control/burst.** Its 3–7 RC pool is not comparable to RP without tracking trigger-based recovery. Draft Mystery/Curse entries include extra actions, turn denial, rerolls, stabilization, and prevention without a complete, tested common rules layer.
3. **Paladin — too much value can be compressed into one chassis.** Sturdy defenses, offense, healing, aura support, and control are strong before Oath effects, which still need final resource, save, duration, targeting, and stacking rules.
4. **Warrior and Dragoon — burst plus durability needs caps.** Mutation stacking, self-healing/resistance, Momentum overflow, armor-ignore, mobility, and extra-action wording need encounter and turn constraints before comparison with fragile precision classes.
5. **Tinker — deployable multiplication is undefined.** Gadgets, drones, turrets, traps, bombs, concurrency, remote detonation, and ally safety cannot be priced without complete action, damage, HP, duration, range, recharge, and targeting data.
6. **Caster/martial parity remains unknown.** Only Wizard, Mage, Cleric, and Druid have rulebook-complete RP tables. Spell scaling, preparation/known limits, specialization discounts, and several non-core pools remain incomplete or draft.

## 4. DM and XP holes

1. **Reconcile the confirmed advancement table, then publish the missing award and encounter rules.** XP is used for level advancement, but awards, shares, CR-to-XP, party adjustments, difficulty, rest/daily budgets, bypass/noncombat awards, and boss handling remain unsourced.
2. **Mark unverified reference data.** Bestiary XP, CR-to-tier browse filters, draft Session XP tally, gate-boss HP stubs, and the simulator's CR damage proxy — not canon awards. *(Builder threshold conflict **resolved** Worker 1.)*
3. **Do not treat CR-tier filtering or the CR damage proxy as encounter balance.** Both are unverified heuristics with no party level, party size, creature-count, action-economy, terrain, or rest adjustment.
4. **Floor content is not yet encounter content.** Floor briefs and generator prompts lack rosters, budgets, hazards/procedures, rewards, and resolution consequences. T6–T10 are expressly unmapped/draft.
5. **Session is table tracking, not a DM resolution workflow.** Bestiary imports preserve a name, HP, CR, and zone only; XP is discarded and CR does no later math. Manual enemy and gate-boss HP formulas are placeholders, not recommendations.

## 5. Combat simulation results

The simulation is a deterministic sanity check using player hit-die rules, narrow source-defined Mage spells, selected authored guardian records, and a clearly provisional CR-based incoming-damage proxy. It is not a rules-complete engine.

- **L3 party vs The Bloom That Hungers (CR 5):** 14.9 party DPR against AC 15; approximately 8 rounds to defeat 112 HP. Draft `vine-maw` predicts 62.4 incoming HP, **63.7%** of the 98-HP party. **Hard but survivable under draft at-will**; recharge/area actions still excluded.
- **L8 party vs Vaskor, the Stone Maw (CR 8):** 32.3 party DPR against AC 17; approximately 6 rounds to defeat 168 HP. Draft `stone-maw` predicts 115.2 incoming HP, **46.8%** of the 246-HP party. **Hard but survivable under draft at-will**; final verdict pending cited sources and full action economy.
- **L5 Mage vs Warrior, AC 15:** Mage has 27 HP, 4.2 sustained Force Spike DPR, and 10.5 Magic Missile burst; Warrior has 55 HP and 12.3 DPR from two d10+4 attacks. The fragile-caster/durable-martial chassis split is directionally plausible, but full caster throughput remains unknown.
- **Illustrative XP split only:** listed Bloom XP produces 450 each for four PCs; listed Vaskor XP produces 975 each. These are equal-split calculations, **not validated award rules**.

## 6. Prioritized implementation queue

### P0 — make the systems testable and stop false canon

1. **Rulebook provenance and reconciliation:** use the confirmed L1–L20 XP table from [`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md) *(Builder reconciled)*; ingest/cite XP-award, CR, encounter, monster, spell, and class chapters. Add source-section metadata and an explicit `confirmed | draft | legacy-unverified` status to rule and companion data.
2. **Companion safety boundaries:** visibly label Builder thresholds, Bestiary XP, CR-tier filters, gate-boss HP, T6–T10 floor material, and all draft mechanics as unverified where appropriate; prevent these fields from presenting as balanced recommendations.
3. **Structured combat schemas:** add complete, typed monster action and defense fields (attack bonus, damage/type, multiattack, save DC, recharge, conditions, resistances, target rules). **Partial (Worker 4):** recharge columns + 26 creatures; 708 draft AC/HP/combat (698 excel-sandbox). Ten gate guardians have authored payloads.
4. **Class/spell rule completion:** normalized effect schema for high-impact features. **Partial (Worker 3):** draft ceiling caps doc + informational UI callouts — not enforced in code.
5. **Reproducible balance harness:** **Partial (Worker 4):** sim includes recharge expected DPR and CR 1/3/10 bands; expand to full L1/L3/L5/L8/L10 source-backed suite.

### P1 — create usable DM and progression workflows

1. **Source-backed encounter worksheet:** accept party members/levels, target difficulty, roster, and stated modifiers; show cited math, assumptions, unresolved data, and GM overrides separately.
2. **XP award ledger:** after source confirmation, add Session-local proposed awards, split/override controls, noncombat award support where applicable, confirmation, audit trail, and explicit character write-back.
3. **Encounter cards for authored floors:** connect POIs/gate bosses to validated rosters or source-backed substitution rules, terrain/hazards, success/failure consequences, rewards, and mapped/draft status. Do not fabricate content for T6–T10.
4. **Bounded class playtests:** run predefined party tests for copy, RC, aura/interception, mutation, deployable, mark/totem, and multiclass combinations across frequent-rest and scarce-rest days.

### P2 — tune after evidence exists

1. Tune damage, HP, armor, spell/resource pools, and monster difficulty from benchmark results—not prose impressions.
2. Add class comparison and DM encounter guidance surfaces only from cited rules plus validated simulation/playtest ranges.
3. Expand authored Bestiary and floor tiers after each entry has structured combat data and encounter provenance.

## 7. Source reports

- [Player class balance audit](./BALANCE_PLAYER_CLASSES.md)
- [XP and advancement provenance](./XP_ADVANCEMENT_CANON.md)
- [DM balance audit — XP, CR, and encounters](./BALANCE_DM_XP.md)
- [Combat-balance simulation](./BALANCE_COMBAT_SIM.md)

---

**CONTINUITY_REPORT:** Balance status is intentionally conservative: the L1–L20 XP threshold table is confirmed, while award rules and encounter math are not. The companion may preserve and expose draft/reference content, but must distinguish it from confirmed rules and must not imply a source-backed XP award or encounter system until the missing chapters and data are reconciled.

**OVERNIGHT_HANDOFF:** Start next with P0 rulebook/provenance and structured combat schemas; then rerun the reproducible test suite before changing numerical balance.

---

**Bestiary re-ingest stamp — 2026-07-30 (pm):** [`BESTIARY_INGEST.md`](./BESTIARY_INGEST.md) documents dual-source ingest from **`Bestiary.xlsx`** + **`final_bestiary.xlsx`**. Live JSON: **708 unique entries** (698 metadata-only + 10 gate guardians with AC/HP/combat drafts + Excel `lootTable`). `python scripts/ingest_bestiary_from_excel.py` to rebuild.

**XP draft stamp — 2026-07-30:** [`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md) includes **DRAFT — OWNER APPROVAL REQUIRED** CR→XP / split / budget sketches. **Worker 1:** confirmed thresholds wired in Builder; Session draft-award stub session-local only.

**Combat sandbox stamp — 2026-07-30 (pm):** [BESTIARY_INGEST.md](./BESTIARY_INGEST.md) — **Bestiary_combat_sandbox.xlsx** is canonical for ingest. **708/708** entries have draft AC/HP/combat (698 excel-sandbox, 10 authored guardians). Sim expanded to CR 1/3/10 bands.

**Oversight Phase C stamp — 2026-07-30:** Continuity clean pass. Bloom Spore Burst retuned (**68.4%** L3 sim); Vaskor **58.2%**. Doc drift cleared (Mercy, XP thresholds, Shadow/Grief, multiclass). Balance P0 partially advanced; award canon and enforced caps still open.

**Oversight Phase B stamp — 2026-07-30 (historical):** Workers W1–W5 verified. W3 ceiling caps + W4 recharge (26 creatures; Bloom **93.2%** pre-Phase C retune, Vaskor **58.2%** sim). Gate C Mercy drift fixed in glossary.
