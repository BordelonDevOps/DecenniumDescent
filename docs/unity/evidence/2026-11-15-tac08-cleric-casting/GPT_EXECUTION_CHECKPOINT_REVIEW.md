# TAC08 actual execution-checkpoint review

Actual request: `3d8e9401-ca5e-48b8-be45-135cda01c8be`; actual GPT response: `ab86f808-3d58-5629-8796-57523b2b5f73`, in **Unity Rules Engine Development Part 2**. Reviewed source: `242108be4ee18f2e6a10d9cd03ba1f185df557e5`; evidence: `d8f70bac32d98426663a39ec2d82588bd8bffcfa`.

## Codex agreement and current gate

Agree with both findings. The controller continuation was actually reproduced from the retained revision128 save against the frozen engine DLLs: pending revision130 selects AcceptOpportunity, receives SanctuaryTargetProhibitedThisInterval, returns Unavailable, and leaves movement pending. Correct the controller and retain genuine nonzero Refrain across the caster's idle and weapon intervals, followed by a new source/binary freeze and complete qualification. No final acceptance or successor authorization.

The old corrected run was explicitly stopped at487 passes with zero reported failures after reproducing the runtime blocker. Its original launch, PIDs, journals, termination record and preserved checkpoint-prefix continuity are retained in `review-correction/`. It is incomplete and cannot qualify the later runtime correction. The first failed run remains separate. No successor module or Unity integration has begun.

## Actual response

The JSON record preserves the original Markdown exactly; presentation-only trailing line-break spaces are omitted below.

**I found one concrete controller blocker and one required evidence gap. Both need resolution before final acceptance.**

1. **The automatic defender mishandles a cached Sanctuary failure during a later opportunity attack.**
   [LaterDefenderController.cs:79](https://github.com/BordelonDevOps/DecenniumDescent/blob/242108be4ee18f2e6a10d9cd03ba1f185df557e5/engine/com.decennium.foundation/Laboratory/Model/LaterDefenderController.cs#L79) selects `AcceptOpportunity` without checking `DirectAttackAllowed`. The regular attack branch checks it correctly. The shared Sanctuary gate then rejects with `SanctuaryTargetProhibitedThisInterval`, which the controller does not handle by declining the opportunity.

   The retained genuine `tac08-sanctuary-carried-parent-resumed.ddsave` provides a concrete starting point at revision128: hero `(0,1)`, defender `(0,3)`, an empty `(0,2)`, and the defender’s Reaction still available after failed-save/forgo. Re-entering `(0,2)` and departing again before the defender’s next Start creates another opportunity occurrence under the same failed-save cache. The controller selects the prohibited attack and leaves movement unresolved.

   **Required correction:** honor the known prohibition and issue the existing decline response. Retain a regression covering the second occurrence, completed parent movement, unchanged RNG/save count, preserved Reaction and save/restore continuation. This finding comes from source tracing and retained-state inspection; **I did not execute that continuation**.

2. **The required genuine Refrain persistence witness is incomplete.**
   The [approved contract](https://github.com/BordelonDevOps/DecenniumDescent/blob/d8f70bac32d98426663a39ec2d82588bd8bffcfa/docs/unity/evidence/2026-11-15-tac08-cleric-casting/APPROVED_CASTING_CONTRACT.md) requires persistence through idle and weapon turns. The genuine cadence case resets Refrain to zero using a different spell at [SpellCastingCases.cs:507](https://github.com/BordelonDevOps/DecenniumDescent/blob/242108be4ee18f2e6a10d9cd03ba1f185df557e5/engine/com.decennium.foundation/Tests/EditMode/SpellCastingCases.cs#L507) before its idle/Grounding checks. The nonzero-counter preservation control is detached; the genuine weapon attack elsewhere belongs to the hero, not the Cleric caster.

   **Required evidence:** establish nonzero Refrain, cross an actual caster idle interval and a lawful caster weapon-action interval, then demonstrate the retained counter on the next same-spell cast. Preserve actual Action, clock, RNG and restore/replay history. If the selected host cannot admit the weapon continuation, return that precise boundary for resolution. This is an evidence gap, not a demonstrated strain implementation defect.

Otherwise, I found no additional concrete blocker in the inspected casting/component authority, chronological validation, strict replay, calendar mapping, Purify accounting, Detect disclosure, concentration/life ordering or focus-onset handling. The genuine versus detached distinctions are appropriately disclosed; no earlier evidence exception is needed to explain the inspected controls.

My independent checks included:

- All **1,178 indexed artifact lengths and SHA256 hashes**, **95 historical pins**, the frozen source archive and compilation-input bindings.
- The exact 60-file implementation and one-file reflection correction; unchanged runtime DLLs, including hashes and MVIDs parsed from the archived binaries.
- Original assignments, starts/PIDs, ordered journals and termination/completion records: **376 pass/1 failure** in the stopped run, **59 passes** in the corrected checkpoint, and **27 completed focused cases**.
- The exact **1,524 predecessor relative order**, plus 27 new cases.
- **135 canonical and 270 filtered-view comparisons**, six final-save matches, 23 authentic compatibility continuations, 92 old console views and 35 unchanged denial/retry pairs.

**I did not run compilation, gameplay, tests or the retainer, or observe live workers.** Build/static outcomes remain retained reports whose source bindings I checked.

Final acceptance remains pending. A runtime correction needs its own frozen source/binary bindings and full regression qualification; completion of the current run cannot qualify changed binaries. Preserve existing run provenance. No successor is authorized by this checkpoint review.
