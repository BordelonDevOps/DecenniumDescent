# Schema40 off-calendar companion activity

This checkpoint adds a persisted six-second activity ledger for the one TEST_ONLY off-calendar companion. It supplies movement accounting for paid Dash without adding the companion to tactical initiative. The interval is anchored to the shared calendar origin, retains exact rational boundaries, and persists movement spending and exact work-history or command-receipt provenance.

The ledger normalizes `WorkLedger.WorkerIntervals` with procedure-specific `Working` records. Overlapping labor blocks Dash for that fixed interval; an unlinked `Working` record also blocks Dash, while a paused reservation without active labor does not. Positive credited labor commits `ActiveLabor`; adjacent segments retain their separate job histories while sharing the commitment. After Dash, modeled work starts/resumes are rejected and the scheduler cannot credit active labor. Walking may continue when movement remains.

A still-running route now automatically attempts a new legal Dash at each fixed interval boundary, after outgoing work and due shared-clock effects settle. It uses the retained originating run receipt resolved from `WorldTraversalRecord.StartedRevision`. A failed renewal spends nothing and leaves the partial route suspended; voluntary pauses stay suspended until explicit resume. Each interval's actor/calendar/ordinal identifies its renewal separately from the shared authorizing receipt. GPT confirmed this as delegated prototype completion; the exact rule was not found in source. See [GPT consensus receipt](GPT_CONSENSUS.md).

## Evidence

- [Pinned source/code/test bindings](SOURCE_BINDINGS.json) identify the Expedition Player Book FL-01–03 source clauses, owner/consensus policy, implementation files and two named regressions. The source clauses require actual activity/location/time accounting and prevent incompatible concurrent activities; the exact off-calendar six-second ledger is explicitly recorded as prototype integration policy.
- [Rule-binding validation](RULE_BINDINGS_VALIDATION.json): PASS, 2 exact source snapshots, 17 projected class profiles, 340 RP cells and 2 named test cases. This is a focused traceability check, not semantic certification.
- [Headless C# suite](HEADLESS_RESULTS.json): PASS, 1,108/1,108 cases. New cases check fixed six-second boundaries, fractional calendar origins, automatic renewal, voluntary suspension, ActiveLabor persistence and scheduler credit, unlinked procedure claims, labor/action overlap, walking after Dash, command ID reuse across principals, malformed receipt reference rejection and current-codec schema39 roundtrip.
- [Core/Persistence/LabModel compilation](COMPILE_RESULTS.json): PASS under C# 9 with warnings as errors.
- [Static Unity package checks](PACKAGE_RESULTS.json): PASS, 14 checks. These check package structure and dependency boundaries only.

The schema40 fields append after schema39 and older codec branches remain versioned. The schema39 case roundtrips a schema39 snapshot through the current codec and confirms that no activity record is encoded; it is not a frozen pre-schema40 byte comparison. Save/restore and pause/resume inside the same interval preserve the existing ledger. The off-calendar actor remains outside the tactical order and receives no turn, Reaction, death save or stance refresh. This does not establish a general expedition calendar, simultaneous movers, autonomous routing, all ordinary exploration Actions, production authority, Unity integration, or release approval.

Unity import/compilation, Edit Mode, Play Mode, player build, and observed gameplay were not run. The code remains TEST_ONLY and Unity integration stays deferred.
