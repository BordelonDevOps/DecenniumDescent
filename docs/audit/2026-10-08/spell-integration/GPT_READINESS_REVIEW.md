The class layer is now far enough along that the next readiness bottlenecks are **integration layers**, not additional class authoring.

## 1. Ranked dependency-aware work packages

| Rank | Package | Status | Exact deliverables | Acceptance criteria |
|---|---|---|---|---|
| **1** | **Ordinary Spell Normalization + Class Integration** | **VERIFIED GAP** | Normalize all 848 spell records into one operational schema: ID/name/source, rank, school, class access, action, RP cost, range, targets, attack/save, duration, concentration, damage/healing, scaling, conditions, components, counterability, Dissonance/Refrain interaction, summon profile, source status. Produce a source-completeness ledger and unresolved-spell queue. Build an automated class-access/rank validator. | All **848** source records accounted for exactly once; every spell referenced by a class resolves to an operational record or explicit `blocked/incomplete` state; no spell bypasses class rank gates; no historical spell-slot or rank×2 cost silently overrides Core V2; concentration and repeated-cast behavior deterministic; zero undefined spell conditions; automated legality suite passes. |
| **2** | **Character Creation + Advancement Contract** | **VERIFIED GAP** | One authoritative playtest procedure from blank sheet → level 1 → Arch → Hero → 20. Normalize ancestry/background, attributes, HP, proficiencies, skills, starting equipment, feats/ASI, automatic class engines, class selections, Arch/Hero gates, level-up steps, retraining if any, and multiclass entry rules. Define machine-readable character-sheet schema. | Codex can generate a legal level-1 character for all 17 families and advance each automatically through 3, 10 and 20 with no duplicate automatic feature, illegal choice, missing prerequisite or stage leakage. Every resource required by a class has a sheet field. |
| **3** | **Shared Combat + Condition Reference** | **VERIFIED GAP** | Source-linked operational glossary for every condition and common mechanic actually used by cards/spells/monsters: Downed, dead, Wounds, Stunned, Restrained, Grappled, Poisoned, Frightened, Charmed, Bleed, Burn, Dread, Staggered, Shaken, silence, concealment, cover, prone, concentration, resistance, immunity, DR, temp HP, forced movement, reactions, extra Actions, recharge, encounter timing. | Every normalized class/spell term resolves to exactly one current playtest definition. Conflicting historical definitions remain preserved but cannot both execute. No class card needs Director invention to resolve its basic mechanics. |
| **4** | **Equipment, Inventory, Consumables + Crafting Integration** | **VERIFIED GAP** | Normalize weapons, armor, shields, ammunition, tools, consumables and item properties. Then normalize all **433 public crafting recipes** with inputs, quantities, time, tools, checks, costs, outputs, failure behavior and visibility. Define salvage and repair rules. | Every recipe produces a defined usable object; every ingredient resolves; crafting cannot create infinite money/material/healing loops; weapon/armor bonuses interact deterministically with class features; no recipe exposes Director-only material unintentionally. |
| **5** | **Monster / Encounter Interface** | **VERIFIED GAP** | Normalize monster action economy, attacks/DCs, defenses, conditions, boss/legendary flags, immunities, recharge, summons and encounter roles. Create an encounter-budget methodology using existing bestiary evidence rather than inventing a new CR system unless required. Produce representative encounters for Base, Arch and Hero play. | At least 3 validated encounters for each stage: **1–2, 3–9, 10–20**. Every monster action resolves under shared combat rules. Boss protections interact correctly with hard-denial rules. No monster depends on undefined external stat text. |
| **6** | **Campaign Procedure Layer** | **VERIFIED GAP** | Operational procedures for encounter start/end, rests, watches, travel, supplies, expedition pressure, downtime, crafting time, research, recovery, death/resurrection, Wounds, treasure/rewards, settlement activity and campaign clocks. Preserve Instruments/Director authority where assigned. | A Director can run a three-session expedition including travel → encounters → short rest → resource depletion → long-rest attempt → downtime without inventing a core procedure. Every class resource has an explicit recovery point. |
| **7** | **Public / Director Data Separation + Build Pipeline** | **VERIFIED GAP** | Tag every rules/data record as Public, Director, Secret/Conditional, or provenance-only. Build deterministic public and Director exports. Create stable cross-layer IDs so public references never require secret text. Audit current bestiary visibility discrepancy. | Automated leak test finds **zero Director-only text/IDs/content in public builds**. All public references resolve. Director build retains full source provenance. Publicly absent monsters/content are confirmed intentional rather than lost. |
| **8** | **Cross-System Rules Validator** | **RECOMMENDATION — current class checks are insufficient for this layer** | Extend existing validators beyond acquisition/reference integrity into executable scenarios: class + spell + equipment + condition + monster + rest interactions. Property-test resources, concentration, copies, summons, redirection, hard control, cooldowns, advancement and multiclassing. | Thousands of generated legal turns produce zero negative resources, over-cap resources, duplicate concentration, recursive copies, >1 extra full Action, repeated hard denial, illegal spell rank, infinite healing or stage leakage. Failures produce reproducible seeds. |
| **9** | **Human Playtest Program** | **VERIFIED GAP** | Tiered pregens, encounter scripts, campaign scripts, session logging form, rules-friction tracker, resource telemetry, damage/healing/action telemetry and issue classification: GAME GAP / HARNESS GAP / CALIBRATION CONCERN. | Human tables complete play at Base, Arch and Hero stages. Blocking procedural ambiguities are recorded and resolved separately from numerical tuning. No claim of balance until this occurs. |
| **10** | **Quickstart / Onboarding / Publication Assembly** | **RECOMMENDATION, dependent on 1–9** | Character-creation quickstart, combat reference, Director quick reference, sample party, starter scenario, glossary/index and generated player-facing class/spell/equipment extracts. | A new group can create characters and complete a session without the owner explaining missing procedures. This is where publication readiness begins, not before. |

---

# 2. Decisions / notebook knowledge Codex should verify against local evidence

These should be **checked**, not guessed or silently rewritten.

1. **Spell repertoire authority.** Confirm exact known/prepared spell counts, class lists and rank gates for every casting class. The shared fallback counts currently used where sources are incomplete must remain explicitly provisional.

2. **Core V2 + Dissonance integration.** Confirm that the current pilot intentionally uses Core V2 RP costs plus the protected Dissonance/Refrain layer, with historical Burn/fizzle and rank×2 cost systems preserved but not simultaneously active.

3. **Multiclassing.** Determine from local evidence whether multiclassing is approved gameplay, experimental, or merely supported by legacy formulas. If active, specify Base/Arch/Hero eligibility, class-level gates, resource pools and spell-rank access before broad balance testing.

4. **Condition authority.** Find the domain authority for every common condition. The recent Poisoned conflict demonstrates why this needs an explicit source-linked registry rather than definitions embedded separately in classes.

5. **Downed / death / Wounds / resurrection.** Verify exact sequence, death thresholds, corpse state, resurrection windows and what Wounds survive recovery. Many high-level abilities now deliberately reference these interfaces.

6. **Equipment math.** Confirm authoritative armor, shield, cover, DR and weapon-property rules. Class normalization assumes these have stable meanings but did not redefine them.

7. **Encounter definition and rest legality.** The shared draft now uses genuine uncertain opposition, 1-hour short rest and 8-hour Rest Watch. Confirm these against the correct campaign/Director sources before those assumptions propagate into spell/item testing.

8. **Monster boss/legendary interface.** Determine exactly what qualifies as boss, legendary defense, anatomy immunity and denial immunity. Many class cards defer correctly to these protections, but the monster side must actually expose the flags.

9. **Feat integration.** There are **335 feats**. Verify acquisition prerequisites, duplicates, ASI substitution, class-specific prerequisites and whether any feat still assumes superseded slots/RP/Burn/class structures.

10. **Crafting economy authority.** Verify time units, currency, material rarity, salvage, recipe discovery and Director-secret recipes before mechanically normalizing all 433 public recipes.

11. **Public/secret ontology.** Verify whether a visibility field or equivalent already exists anywhere in V6/V7 tooling before inventing another tagging system.

12. **Supplemental playtest completions.** Preserve clear labeling on new level-20 completions, fallback spell-known schedules, Oathbreaker forbidden spells and similar gap-fill rules. They are useful test material, but should never become indistinguishable from recovered approved text.

---

# 3. Best package to build now

## **Spell Integration Baseline v0.1**

This is the highest-value next build **without changing approved canon**.

Why: the class layer is now mechanically rich enough that ordinary spells are the largest unresolved interface touching combat, resource economy, concentration, class identity, character sheets, encounter testing and multiclass legality. Until spells are normalized, a large portion of the 17-class suite cannot receive meaningful integrated testing.

I would build it in this order:

1. **Inventory all 848 spell records** with source path/hash/reference and current implementation state.
2. Define the normalized spell schema.
3. Map every existing class reference to an exact spell ID.
4. Operationalize **all rank 0–3 spells plus every named spell referenced by a class packet**, regardless of rank.
5. Validate Core V2 RP costs, rank gates, class/school access, concentration, Dissonance/Refrain and countering.
6. Produce an explicit queue for ambiguous/incomplete rank 4–Grand entries.
7. Once the schema survives the early-rank slice, normalize the remaining records mechanically without altering their source text.

### Acceptance gate for that package

Do not call it complete until:

- `sourceSpellCount == 848`
- every record has unique stable ID + provenance;
- every class-referenced spell resolves;
- every operational spell has action, cost, legal targets, range, duration, resolution and scaling;
- every ranked spell has one legal Core V2 RP cost and rank;
- no spell grants access merely because the caster can afford its RP;
- concentration is explicit;
- damage/healing copies cannot recursively proc;
- summons use either an approved specific profile or the bounded shared companion interface;
- no undefined spell slots/Burn/rank×2 costs remain executable;
- automated spell legality tests pass.

That package gives you the largest increase in **actual playable game surface** for the least canon risk. After it, Character Creation/Sheet integration should be next, because at that point Codex can construct legal PCs whose class and spell layers are both executable.