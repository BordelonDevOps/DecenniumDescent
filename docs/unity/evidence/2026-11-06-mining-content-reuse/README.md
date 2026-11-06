# Authored mining content reuse on schema43

**Date:** 2026-11-06  
**Branch:** `Engine`  
**Status:** partial, TEST_ONLY; not release-approved.

This increment generalized mining fixture initialization and validation to consume authored deposit/category/unit records and physical worksite content. The extraction resolver no longer recognizes one receiver fit-rule identifier; it checks the existing explicit `FitMemberIds` membership contract. No persisted record or schema version changed.

`mining_shared_resolver_handles_distinct_authored_deposits_through_save_and_replay` runs two different authored definitions through the same command assessment, clock, deterministic check, settlement, save/restore and duplicate replay path. The definitions vary material, tier/DC, unit identity and quantity, receiver/profile/fit ID, and worksite coordinates. Each output is received by its own authored container. They are separate TEST_ONLY runs, not evidence of simultaneous multi-worker mining.

The source/provisional/fixture boundary, record responsibilities and remaining gaps are recorded in [MINING_RULE_DECISIONS.md](../../MINING_RULE_DECISIONS.md). The implementation map is [IMPLEMENTATION_TRACE.md](../../IMPLEMENTATION_TRACE.md). Source snapshots are copied from the preceding exposed-mineral checkpoint and bound by the SHA-256 values in `SOURCE_BINDINGS.json`.

## Validation

| Check | Result |
| --- | --- |
| `Test-Foundation.ps1` | **PASS — 1,143/1,143**, C# 9, warnings as errors |
| Focused authored-content case | **PASS — 1/1** |
| `Compile-Foundation.ps1` | **PASS — Core, Persistence and LabModel** |
| `Validate-Package.ps1` | **PASS — 18 checks, 217 assets, 217 unique GUIDs** |
| Current source/profile/test binding audit | **PASS — 7 source snapshots, 17 class profiles, 33 named tests** |

`HEADLESS_RESULTS.json`, `COMPILE_RESULTS.json`, `PACKAGE_RESULTS.json`, `SOURCE_BINDINGS.json` and `RULE_BINDINGS_VALIDATION.json` preserve the exact reports and tested source hashes. An earlier full-suite run failed because a constructor parameter shadowed the immutable fixture field; the focused case reproduced it. The assignment was corrected, then the focused case and final full-suite run passed.

This verifies content reuse over the existing schema43 extraction path. It does not establish complete mining coverage, production content, full-game readiness or release approval.
