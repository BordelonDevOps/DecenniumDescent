# Schema45 nondestructive manifest-assay checkpoint

**Date:** 2026-11-06 UTC  
**Branch:** `Engine` at `4df6738972ccba92cc7cf2495a3b0bf2547b596e` (working tree; no commit made)  
**Status:** partial TEST_ONLY implementation; the cited operational playtest sources are not release approval.

This increment adds a one-active-minute WIS/Mining assay over an explicitly authored exposed mineral manifest. It persists the manifest-bound profile and attempt/check/finding audit in schema45, uses existing shared commands, clock, worker intervals, RNG, persistence and receipts, and records only authored category, suitability and handling facts. The bounded procedure is nondestructive: mineral units, physical items and inventory lots remain unchanged. It does not generate deposits, hidden reserves, samples, properties or quantity.

Responsibilities, source bindings, code ownership, dependencies, fixture facts, accepted source behavior and unsupported work are in [the assay decision record](../../MINERAL_ASSAY_RULE_DECISIONS.md). Schema45 is mapped in [the implementation trace](../../IMPLEMENTATION_TRACE.md). The focused source-binding record is [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json).

## Validation

| Check | Result |
| --- | --- |
| `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` | **PASS — 1,152/1,152**, C# 9, warnings as errors; all 4 assay cases pass |
| `pwsh -NoProfile -File engine/tools/Compile-Foundation.ps1` | **PASS — Core, Persistence and LabModel**, C# 9, warnings as errors |
| `pwsh -NoProfile -File engine/tools/Validate-Package.ps1` | **PASS — 18 checks, 225 assets and 225 unique GUIDs** |
| `git -c core.whitespace=cr-at-eol diff --check` | **PASS** after documentation updates |
| Unity import/editor compilation, play mode, build, production gameplay | **NOT RUN** |

Exact reports are `HEADLESS_RESULTS.json`, `COMPILE_RESULTS.json`, and `PACKAGE_RESULTS.json` in this folder. Static package checks do not establish Unity import, release compilation, or full gameplay. The full engine is incomplete.

## Diagnosed failures during this increment

The first full-suite run discovered a stale test sentinel: `(CommandKind)99` had become the valid `PauseMiningAssay` enum value after command kinds were appended. The malformed-command case therefore reached the base policy and correctly returned `UnsupportedCommand`, not `InvalidCommand`. The regression now uses an out-of-range enum value.

After adding the assay cases, command discovery omitted all three assay commands from `SupportsCommand`. The resolver and query assessment existed, but the shared discovery gate silently filtered the options. Adding `StartMiningAssay`, `PauseMiningAssay` and `ResumeMiningAssay` fixed the missing path. The final full suite passes.

A focused profile-identity regression then reproduced a knowledge leak: the query matched learned finding IDs across every assay profile instead of the profile referenced by the successful attempt. The query now joins through each successful attempt's profile. The isolated case and final full suite pass.

## Remaining boundary

The fixture supports only a nondestructive assay of one authored exposed manifest. Learned finding queries are scoped to each worker's successful attempt and that attempt's profile. Actual sample debit, portion selection/debit timing, retries based on materially changed evidence, assistants, magical tool benefits, production geological state and broader mining procedures remain unimplemented. Do not treat the one-profile attempt limit or synthetic values as general game rules.
