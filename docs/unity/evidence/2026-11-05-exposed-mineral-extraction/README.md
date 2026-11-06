# Schema43 exposed mineral extraction checkpoint

**Date:** 2026-11-05  
**Branch:** `Engine`  
**Status:** partial, TEST_ONLY; not release-approved.

This checkpoint implements one explicitly authored exposed mineral parcel through the shared C# simulation. It adds deposit/category/unit/attempt records, deterministic extraction checks, labor and stock reservations, finite output receipt, pause/resume, strict save decoding, timed-handling integration and command replay. It does not generate mineral deposits or stock.

Responsibilities, authoritative records, source/provisional/fixture distinctions, dependencies, deferred behavior and the runnable acceptance are recorded in [MINING_RULE_DECISIONS.md](../../MINING_RULE_DECISIONS.md). The architecture map is [IMPLEMENTATION_TRACE.md](../../IMPLEMENTATION_TRACE.md).

## Validation

| Check | Result |
| --- | --- |
| `Test-Foundation.ps1` | **PASS — 1,142/1,142**, C# 9, warnings as errors |
| `Compile-Foundation.ps1` | **PASS — Core, Persistence and LabModel** |
| `Validate-Package.ps1` | **PASS — 18 checks, 217 assets, 217 unique GUIDs** |
| Current pinned-source/profile/test binding audit | **PASS — 7 source snapshots, 17 class profiles, 32 named tests** |

`HEADLESS_RESULTS.json`, `COMPILE_RESULTS.json`, `PACKAGE_RESULTS.json`, `SOURCE_BINDINGS.json` and `RULE_BINDINGS_VALIDATION.json` retain the exact output and source hashes. The binding audit uses the current full-suite result and adds mining source snapshots and named cases.

The first call to `Validate-RuleBindings.ps1` used its default older expedition-assignment binding record. That historical test report pins `ActorConditionRecord.cs` to `15d25317…`, while the unchanged file in the current checkout hashes to `47b3c923…`. The mismatch is in previously archived evidence, not this mining diff. The old failure is retained as `RULE_BINDINGS_STALE_BASELINE.json`; a new audit against the current 1,142-case report passes without rewriting the older checkpoint.

The first run of the added cases had two faulty test assumptions: it mutated abilities after fixture initialization, breaking the fixture content fingerprint, and it expected an unseeded die result to be Success. The regression setup now fingerprints the ability override and accepts all valid completed check degrees. The corrected full run passes.

## Source pins

The source snapshot paths and SHA-256 values for the Mining candidate guide, Gathering Tools candidate guide, and gathering body catalogue are recorded in [MINING_RULE_DECISIONS.md](../../MINING_RULE_DECISIONS.md) and `SOURCE_BINDINGS.json`. The output and source hashes correspond to the repository state at this checkpoint.

This result proves compilation and the bounded headless/static contracts only. It does not establish a complete mining system, clause-by-clause rule parity, presentation integration, full-game readiness or release approval.
