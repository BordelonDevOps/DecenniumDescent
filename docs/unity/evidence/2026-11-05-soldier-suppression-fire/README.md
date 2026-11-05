# Soldier Suppression Fire checkpoint

**Status:** schema33 TEST_ONLY increment, source-bound and provisional.

Schema33 enables the second source-legal Soldier level-three pair, Tactical Assessment + Suppression Fire. The advancement, new feature grant, Action cost, three loaded bolts, shared 3d6, target DEX save/damage, Recharge countdown, slow lifecycle, history and replay are covered by the shared C# suite.

The authored card and shared combat geometry source do not establish general square placement/orientation. Per Codex/GPT consensus, this fixture uses a saved axis-aligned 3×3-cell (15 ft × 15 ft) square centered at cell (4,0), footprint x=3..5, y=-1..1, and the fixture's one known target. The activation record stores its center. It does not move with a target. General placement, rotation, boundary policy, and multi-target perception/cover/resolution remain out of scope.

- Full headless suite: 1,077/1,077.
- C# compilation: Core, Persistence and LabModel pass under C# 9 with warnings as errors.
- Static package validation: 14 checks pass.
- Pinned class catalog projection validation: pass for all 17 classes, 340 schedule rows and 1,223 card options.
- Unity compilation, Edit Mode, Play Mode, player build and gameplay qualification were not run.

Exact results and implementation/source hashes are in [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json), [COMPILE_RESULTS.json](COMPILE_RESULTS.json), [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json), [CATALOG_VALIDATION.json](CATALOG_VALIDATION.json), and [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The full source/decision analysis is in [SOLDIER_LEVEL3_RULE_DECISIONS.md](../../SOLDIER_LEVEL3_RULE_DECISIONS.md).

