# Schema34 Defensive Formation verification

**Branch:** `Engine` (working tree; not committed or pushed)  
**Pinned rules revision:** `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`  
**Result:** the bounded schema34 increment compiles and passes the complete deterministic headless suite and static package validation.

## Verification

- `HEADLESS_RESULTS.json`: **1,089/1,089** deterministic cases passed, including six schema34 Defensive Formation cases; this result also covers the later shared-source increments.
- `COMPILE_RESULTS.json`: C# 9 Core, Persistence, and LabModel compilation passed with warnings as errors.
- `PACKAGE_RESULTS.json`: **14/14** static Unity package structure and source-binding checks passed.
- `CATALOG_VALIDATION.json`: pinned advancement projection passed for 17 classes, 340 schedule rows, and 1,223 card options.
- `SOURCE_BINDINGS.json`: exact snapshots, source hashes, implementation files, and six named regressions; run `pwsh -NoProfile -File engine/tools/Validate-RuleBindings.ps1` to reproduce the focused audit.

The regressions cover the third legal Soldier level-three pair, pure Bonus Action query, invalid hostile recipient, ordered accept/decline, independent movement after ordinary movement is exhausted, opportunity-attack suppression, dynamic adjacency and strongest-only reduction, unable-recipient skip, exact expiry and one-use enforcement, save/restore, and Press continuation. The schema34 shift uses the existing completed-movement dispatcher; Press has direct interaction coverage. The fixed Overwatch fixture targets only the hostile actor, so no schema34 test claims a simultaneous Overwatch offer during a legal ally shift.

## Limits

This is a bounded TEST_ONLY Soldier fixture with two eligible allies. It does not complete all Soldier cards, general class advancement, general area placement, the exploration and resource-management rule catalog, or the full engine objective. Unity Editor compilation, Edit Mode, Play Mode, player builds, historical-save byte comparison, and gameplay qualification remain unrun. The static package validator is not a Unity compile.
