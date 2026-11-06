# Schema44 authored-evidence prospecting checkpoint

**Date:** 2026-11-06 UTC  
**Branch:** `Engine`  
**Status:** partial, TEST_ONLY; not release-approved.

This increment adds prospecting against an already authored exposed patch. The persisted schema44 records capture canonical patch identity, linked immutable exposure facts, attempt progress, check/RNG audit, outcome, and findings learned. An attempt takes 600 active seconds and uses the shared clock, work intervals, command transaction, RNG, tool/hand/access checks, snapshot persistence and replay. Success returns only authored observable facts; it does not generate geology or mineral quantities. Exposure-change causes are trusted host assertions and are not externally authenticated by this fixture.

The source, delegated completion policy, record ownership, dependencies, fixture assumptions, remaining gaps, and acceptance case names are in [PROSPECTING_RULE_DECISIONS.md](../../PROSPECTING_RULE_DECISIONS.md). The implementation map is [IMPLEMENTATION_TRACE.md](../../IMPLEMENTATION_TRACE.md). Pinned source revisions and hashes are also listed in that decision record.

## Validation

| Check | Result |
| --- | --- |
| `Test-Foundation.ps1` | **PASS — 1,148/1,148**, C# 9, warnings as errors |
| `Compile-Foundation.ps1` | **PASS — Core, Persistence, LabModel** |
| `Validate-Package.ps1` | **PASS — 18 checks, 217 assets, 217 unique GUIDs** |
| `git -c core.whitespace=cr-at-eol diff --check` | **PASS** |

`HEADLESS_RESULTS.json`, `COMPILE_RESULTS.json`, and `PACKAGE_RESULTS.json` preserve the exact reports. The previous schema43 source/profile/test binding audit is historical and does not bind schema44 prospecting code; no current binding audit is claimed here. Headless compilation and static package checks do not establish a release build, full gameplay, or complete mining rules.

## Rule boundary

The implementation covers one method per exposure, authored required implements/hands, shared active labor, per-worker learned facts, failure without reliable finding, repeat prevention, and invalidation when materially changed exposure replaces an old version. The fixture admits only a no-hazard profile; it does not model assistants, tool bonuses, general hazards, assay, deposits, hidden reserves, or mineral quantity. The world event that changed exposure must be supplied by a trusted host; this test slice records the asserted cause ID and time but cannot verify the external event.
