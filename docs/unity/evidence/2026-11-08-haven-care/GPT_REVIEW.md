# GPT implementation review 2 — schema66 Haven care

**Target reviewed:** `c70fb682dbeea8a3f6ffa9b1face7037130b5ba0` on `Engine`.

## Actual verdict

> “The three execution defects are corrected, but one query/execution mismatch still blocks acceptance of `c70fb682`. It is a small gap in the existing combat-entry correction—not a new rule or expanded scope.”

GPT marked historical-death validation and benign-condition interruption **closed**. It marked combat interruption **corrected in execution**, with one remaining acceptance blocker in movement query admission:

- The regression setup has the companion in active care at `(3,3)` while the hero at `(2,0)` attempts an eastward step toward a hostile.
- `AssessWorldStep` detects `StartsEncounter` but did not check active Haven care.
- `QuerySharedWorldCommand` therefore returned `Supported=true`, `Admissible=true`, `EncounterTransition` for a command that `ResolveCore` rejects as `HavenCareCombatTransitionUnsupported`.
- The outer query guard only checked whether the command actor was the care patient, so it missed another actor's movement.

GPT's smallest proposed correction was to enforce the Haven restriction in shared `AssessWorldStep`, then query and execute the same command in the regression and require the same rejection code with unchanged snapshot bytes. No schema or gameplay-policy change was requested.

GPT reviewed the exact diff, code paths, public query, replay validation, regressions, before/after reports, source bindings, compatibility evidence, trace and handoff. GPT **did not execute** compilation, tests, validators or Unity checks and did not independently recompute hashes. It confirmed the omitted forged-batch, duplicate-care-command, fractional-endpoint and independently partitioned-clock tests were optional hardening absent a concrete failure. It found no wire-layout or historical-codec blocker and kept the schema65 report scoped to byte-identical codec roundtrip evidence.

## Codex reproduction and correction

The exact combat-transition test was extended to call `QueryCommand` on the same movement command before execution. Against `c70fb682`, that regression failed with `Movement query advertised a combat transition that active Haven care rejects.` The result is retained under `development-attempts/gpt-review-reproduction/failure-before-query-fix/`.

`AssessWorldStep` now returns `HavenCareCombatTransitionUnsupported` when an encounter-triggering step occurs during any active Haven-care interval. The existing execution resolver and public query share this assessment. The same-command query and execution regression passes in [the focused result](final/focused/combat-query/run-20261109T050747956Z-814d9c53/results.json). The new correction is awaiting GPT follow-up review; this review did not accept the module.