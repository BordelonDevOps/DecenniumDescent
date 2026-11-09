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

`AssessWorldStep` now returns `HavenCareCombatTransitionUnsupported` when an encounter-triggering step occurs during any active Haven-care interval. The existing execution resolver and public query share this assessment. The same-command query and execution regression passes in [the focused result](final/focused/combat-query/run-20261109T050747956Z-814d9c53/results.json). GPT's follow-up review accepted correction commit `808ff151253b7b1168d1625d64b6f74d8bb815e2` and found no remaining concrete blocker.

## GPT follow-up review 3 — accepted

**Target reviewed:** `808ff151253b7b1168d1625d64b6f74d8bb815e2` on `Engine`.

> “Yes. `808ff151253b7b1168d1625d64b6f74d8bb815e2` closes my sole remaining blocker. I accept the bounded schema66 TEST_ONLY Haven-care increment against the agreed scope.”

GPT confirmed all findings closed: historical care assessments survive later ordinary death; benign condition events preserve care; unsupported combat transitions reject without interrupting care; and movement query and execution agree on that rejection. GPT found no remaining concrete acceptance blocker and confirmed no records, codec layout or gameplay rule changed.

GPT inspected the exact diff, shared admission callers, regression, retained before/after evidence, compile/package/source-binding reports, compatibility result, trace and handoff. GPT **did not independently compile, execute tests or validators, recompute source hashes, or perform Unity checks**. The generic binding audit remains a disclosed pre-test failure; the schema65 evidence establishes codec roundtrip, not an archived continuation comparison. Forged-batch, fractional-endpoint and independently partitioned-clock regressions were classified as optional hardening, not acceptance conditions.

**Next mapped dependency recommended by GPT:** MGT-03 expedition Pressure and Watch-end complication processing, already present in [the implementation map](../../IMPLEMENTATION_TRACE.md#L651) and governed by pinned FL-08/FL-09. GPT recommends beginning with a bounded authored group/route, actual exposure causes, and predeclared complication stakes, reusing shared clock, RNG and receipt history. Resolve its precise source-bound contract before implementation. MGT-03 remains partial; the engine remains unfinished and Unity remains deferred.