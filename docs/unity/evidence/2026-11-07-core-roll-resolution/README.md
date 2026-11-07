# Shared roll-resolution evidence

## Scope

This no-schema-change increment routes the existing provisional task-check, attack-roll, ordinary-save and opposed-check calculations through one compile-gated `RuleResolution` service. `RuleDice` centralizes d20 presence selection and calls the existing `DiceStream`. `PlaytestRolls` and `PlaytestDice` keep their compatibility APIs and delegate to these shared implementations.

The same command records, action costs, accepted-command receipts, random state and consequences remain authoritative. The resolver does not choose character modifiers or make a command legal. It stays behind the existing `DECENNIUM_TEST_ONLY` LabModel gate; the provisional source procedures remain disabled for production runtime selection and are not release-approved.

## Source authority

- Pinned revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.
- `DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md`, sections **Rolls** and **Advantage and disadvantage**, SHA-256 `69d0e64394de58c4d86a3ec57cf282978d131a1a9c1eaa21632bb7d3b72562da`.
- `DescentReviewChanges/ReviewBible/tools/core_playtest_rules.py`, functions `task_check`, `attack_roll`, `saving_throw` and `opposed_check`, SHA-256 `a162117cf2c0c96a77ef5e594ce7247593930c57e6223fc7291ab12fc45c8d7d`.
- Existing deterministic RNG dependency: `Runtime/Core/DiceStream.cs` and `RandomV1` in `Runtime/Core/Simulation.cs`; the RNG algorithm and saved state are unchanged.

This code centralizes already implemented provisional semantics; it adds no new roll rule or modifier policy.

## Validation

- `Test-Foundation.ps1`: PASS, 1,212/1,212 cases, C# 9, warnings as errors. See [full results](FULL_TEST_RESULTS.json).
- `Validate-Package.ps1`: PASS, 18/18 static package checks, 258 assets and 258 unique GUIDs. See [package results](PACKAGE_RESULTS.json).
- The new cases compare exact RNG trace and compatibility parity, exercise all four roll families, and verify validation boundaries. Their names and tested-code hashes are in [source bindings](SOURCE_BINDINGS.json).
- Unity compilation, Edit Mode, Play Mode, standalone builds and gameplay observation were not run.

## Remaining scope

The resolver does not derive abilities, skills, proficiency, eligible advantage sources or applicable modifiers. It does not own command legality, spend command-owned RNG, apply damage, dispatch reactions, or persist any new state. Those remain in their connected procedures.
