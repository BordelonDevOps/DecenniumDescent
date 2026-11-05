# Schema41 finite-source harvesting

**Branch:** `Engine` (uncommitted working tree)  
**Pinned rule revision:** `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`  
**Scope:** one TEST_ONLY fishing-remains extraction transaction; not the complete gathering system or engine.

## Implemented

The schema41 C# slice executes exact work intervals against a pre-existing dead fish, one finite selected material unit and actual fixture tools/site/receiver. It persists check and RNG receipts, links the resulting mass to inventory/cargo, conserves the remaining body mass, applies extraction failure consequences, interrupts incompatible work on tactical entry, and preserves progress and provenance across save/load.

GPT confirmed the source interpretation that an untrained lead may attempt generic extraction with Wisdom, zero proficiency, and disadvantage, provided actual physical and access requirements are satisfied. The code now follows that reading. The Fishing fallback accident is recorded and applied as piercing damage, as specified by the pinned harvest and trade references. See [decision record](../../HARVEST_RULE_DECISIONS.md) and [GPT consensus](GPT_CONSENSUS.md).

## Verification

- [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json): full C# 9 warnings-as-errors regression run, **1,115/1,115** cases passed. This includes the new untrained/disadvantage regression and trained single-PB, success, failure, critical-failure, pause/resume, save/load and replay cases.
- [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json): static Unity-package structure validation passed **14/14** checks. It does not compile the package in Unity.
- [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) and [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json): validation passed for 3 exact source snapshots, 17 class profiles, 340 RP cells and 7 named harvesting cases.
- [UNTRAINED_FOCUSED_RESULTS.json](UNTRAINED_FOCUSED_RESULTS.json): the separate focused untrained case passed **1/1** before the full suite.

Unity Editor import/compiler, Edit Mode, Play Mode, player build, gameplay, and release approval were **not run**. See the decision record for the bounded fixture and remaining engine gaps.
