# Character advancement history schema evidence

This increment adds snapshot schema30 for advancement-event choice lists. Each event stores a count followed by zero to four selected feature IDs in canonical ordinal order. Schemas 1–29 keep the former two-string event layout.

Schema30 validates recorded events in revision order against the actor’s historical level sequence, including the class-level position at each event. Current executable legality remains deliberately narrower: only the existing TEST_ONLY Soldier level 1→2 row can commit. Soldier level 3 choices remain unbound and reject without consuming the milestone, so the requested two-successive-level-up replay regression remains future work.

Validation results are recorded in [compile](COMPILE_RESULTS.json), [headless suite](HEADLESS_RESULTS.json), [package checks](PACKAGE_RESULTS.json) and [source projection](SOURCE_PROJECTION_RESULTS.json). The source projection is bound to the pinned class revision and catalog evidence. Unity import, compilation, Edit Mode, Play Mode and player build were not run.
