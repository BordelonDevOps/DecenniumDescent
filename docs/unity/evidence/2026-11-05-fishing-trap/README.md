# Schema37 unattended Trap and physical retrieval

**Branch:** `Engine` (working tree; uncommitted)  
**Pinned source revision:** `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`  
**Authority:** reviewed operational PLAYTEST source, exercised only through explicit TEST_ONLY content.

## What this increment implements

The C# simulation now carries a bounded unattended Trap attempt through real setup, finite opportunity and bait reservation, deployed physical Trap state, one scheduled check, same-creature capture, and five-minute retrieval into a supported receiving location. It persists all relevant identities, custody, location, worker labor, reservations, check/RNG facts and save/replay state.

The retrieval checks access, a capable worker with two free hands, idle work status, intact Trap/support/receiver, matching site, cord length, and receiving mass/volume capacity. The setter identity, site/Trap/receiver IDs, check DC and proficiency profile can be supplied by the fixture; the check snapshots that setter's own WIS/proficiency. Retrieval does not require the setter: a different fixture worker walks to the site and successfully receives the same Trap and fish. A paused retrieval retains progress and its receiving-location reservation across save/load. Exact check/retrieval ties resolve the scheduled check first. Early retrieval closes without a roll or catch while spent bait/opportunity remain spent. If the setter abandons during active retrieval, this fixture pauses the worker and keeps the receiver reserved so the work may resume.

Schema35 retains the legacy no-bait record, schema36 the historical bait/timing projection, and schema37 adds physical opportunity, creature, Trap, receiver and retrieval records. The exact boundary between source rules and fixture policy is recorded in [FISHING_TRAP_RULE_DECISIONS.md](../../FISHING_TRAP_RULE_DECISIONS.md).

## Verification

- [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json): **1,099/1,099** deterministic cases passed; includes 16 named fishing regressions.
- [COMPILE_RESULTS.json](COMPILE_RESULTS.json): Core, Persistence and LabModel compile under C# 9 with warnings as errors.
- [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json): **14/14** static package checks passed.
- [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json): exact source snapshots, implementation paths and named tests. [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json) passes with 17 profiles, 340 RP cells and 16 bound fishing regressions.
- Unity import/compiler, Edit Mode, Play Mode, player build, historical-release byte comparison and gameplay qualification were **not run**.

## Limits

This bounded lifecycle supports multiple authored profiles in one TEST_ONLY saved world. One regression runs two independent profiles sequentially across save/restore; another gives two distinct opportunity and stock-version labels one shared creature identity, verifies only the first exposure reserves it, and confirms the losing opportunity spends its bait without a replacement response while its empty Trap remains physical and retrievable. Shared candidate sets beyond one body, versioned stock manifests, overlapping allocation-set audits across differently labeled sites/routes, weighted selection, renewal, attraction and pathing remain unimplemented. The system still does not implement all of MGT-06: it also lacks hazards, prey movement/anatomy admission, full Trap-component histories, Rod, Net, attended fishing, assistant bonuses, equipment bonuses, finished Bait receipts or suppression, escaped-prey recovery, general deployment allowances or holder handover. Its C# evidence does not establish the complete explore → encounter → acquire → manage → prepare → explore loop or complete the engine. Unity integration remains deferred.
