# Shared ability-check modifier derivation

## Scope

This no-schema increment adds a pure `AbilityCheckRules` calculation for ability modifier plus an explicit recorded proficiency rank (0, 1 or 2), with a separate method to apply the existing strongest applicable injury penalty once when the check resolves. It is wired into existing skill-backed mining, prospecting, harvest, assay, fishing-trap and medicine checks, and into the fixture-backed supply-cache/receptacle lock check.

`ActorCharacterRecord` owns ability scores and chronological levels. `SkillTrainingRecord` owns explicit training rank. Existing domain attempts continue to own skill identity, selected ability, DC, advantage/disadvantage, roll audit, costs, outcomes and persistence. `PlaytestCharacters` supplies ability/proficiency calculations; `PlaytestLife` remains the injury policy. No global state, random selection, snapshot field, command, clock rule or save behavior was added.

The helper deliberately does not invent skill-to-ability mappings or training grants. Each caller supplies the ability already selected by its existing procedure. Existing results, timing, RNG use, reservations and replay semantics are retained. General automatic-result rules, complete source-specific modifiers and skill/training acquisition remain open.

## Source bindings

Pinned source revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

- `CORE_RESOLUTION_PLAYTEST.md` establishes task-check resolution and ability plus applicable proficiency contribution. Its pinned Git blob is `735e1a1f2661de6167dda58e0609749e0756ca85`.
- `CHARACTER_CREATION_PLAYTEST.md` establishes recorded ability scores, levels, training and the proficiency/expertise distinction. Its pinned Git blob is `04c77b3ddff460219600df2f28bac27d854647af`.
- Injury applicability is reused from the already implemented `PlaytestLife.AbilityCheckInjuryPenalty`; its lock-check binding is also recorded in [the supply-cache decision](../../SUPPLY_CACHE_RULE_DECISIONS.md).

The exact current local source-snapshot SHA-256 values and the implementation/test source hashes are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) and the complete headless run report. The helper does not claim complete coverage of either source document.

## Acceptance and validation

Four registered deterministic cases cover every proficiency tier with ranks 0–2; ability choice and negative modifiers; an injury applying once despite repeated matching wounds/flags; and invalid rank, level, index and actor-training references. A focused injury case passes **1/1**. The first complete run had **1,170/1,171** cases pass because the new test incorrectly expected a Fine-Motor injury not to affect a Wisdom tool check. The existing policy applies Fine-Motor injury to any tool check; the test was corrected to use a non-tool Wisdom check. The reproducing report is retained as `INITIAL_FAILURE_RESULTS.json`.

Final validation:

- C# 9 Roslyn compilation with warnings as errors and full deterministic suite: **PASS, 1,171/1,171** (`HEADLESS_RESULTS.json`).
- Focused injury acceptance: **PASS, 1/1** (`FOCUSED_RESULTS.json`).
- Static package validation: **PASS, 18 checks, 231 package assets, 231 unique GUIDs** (`PACKAGE_RESULTS.json`).
- `git -c core.whitespace=cr-at-eol diff --check`: **PASS**.

No GPT review has been completed for this increment; the last attempt to access the requested browser chat timed out. This evidence records implementation and validation facts, not independent review or production approval.
