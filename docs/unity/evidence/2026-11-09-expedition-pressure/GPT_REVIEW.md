# GPT implementation reviews — Expedition Pressure (TEST_ONLY)

## Review of correction commit 3d00c97457682f7fdac9eaef7bf82a83c24845a1

**Verdict:** Held. GPT confirmed that the three original schema67 blockers were addressed by the schema68 changes, but found three new concrete lifecycle/compatibility blockers. The module is not accepted and no successor dependency may start.

**Review scope:** GPT inspected the exact commit diff, movement/clock/replay and codec paths, connected and correction tests, pinned FL-08/FL-09/TR-13 sources, consensus/source bindings, retained reports, implementation trace and handoff. It did not compile, run tests, independently recompute source hashes, or perform Unity checks. It compared report manifests: package/full-suite overlap matched; correction-focused reports used an earlier `ExpeditionPressureCases.cs` hash, while the final full-suite report included all five correction cases.

### Original blockers — closure confirmed

| Prior blocker from review of 1f9e295 | GPT's result on 3d00c974 |
| --- | --- |
| Haven arrival resolved its consequence after physical admission, so Standard delay did not delay arrival and Severe left no retreat position. | Gate-side staging and deadline-based admission are implemented; the shared advance loop retains its accepted target. |
| Tactical movement could bypass a Severe route closure. | Exploration and admitted tactical movement now share the pressure movement assessment. |
| Severe exposure ended before actual withdrawal, and retreat completion stranded later movement. | Exposure persists through retreat and ends on departure; the new same-time causal defects below remain. |

### Concrete blockers

1. **Schema67 exact-Watch Haven arrival no longer replays canonically.** In `SharedExpeditionPressure.cs`, checkpoint reason selection now keys on `stagedHavenArrival`, which is always false for schema67. Schema67 arrival exactly at a Watch end therefore records `WatchEnd`; the former schema67 behavior recorded `HavenArrivalAtWatchEnd`. Existing saves with that checkpoint will fail canonical replay. GPT's smallest fix: preserve the original `safeArrival` reason selection for schema67 and add an exact-Watch schema67 continuation/restore regression. The current compatibility case only covers early arrival.

2. **A later same-Watch attack conflicts with an already-resolved early-Haven checkpoint.** The correction properly retains exposure after Standard delay or Severe retreat. However, `ExpeditionPressureValidation` requires every checkpoint's cause count to equal all combat changes for that cohort and Watch across the entire snapshot. If a Severe Haven checkpoint occurs first, then a lawful encounter and attack occurs at the gate later in that Watch, the attack source is appended but is absent from the immutable earlier checkpoint. Snapshot validation rejects the otherwise lawful attack. GPT's smallest fix: validate a checkpoint against the causal source set available at its settlement revision, retain later actual attack evidence, preserve exactly one checkpoint and do not rewrite or roll again. The gameplay projection for such late same-Watch causes was sent back to GPT as a precise follow-up question and remains unresolved until GPT responds.

3. **Same-time tactical withdrawal can invalidate attacks already recorded.** `TacticalMovementPolicy` ends exposure at RuleTime T on the off-route step. Pressure validation and `AttackWithinExposure` currently require an attack timestamp strictly before `EndedAt`; an attack at T with an earlier receipt revision than the later retreat at T then fails validation. A related opportunity attack during the departure can be omitted because the collector runs after retreat and searches only for an open exposure. GPT's smallest fix: determine exposure membership at the attack's causal position from existing attack/movement history and receipt ordering, not final exposure state or timestamp alone. Add an attack followed by same-time tactical withdrawal regression, including an opportunity attack during the departure.

### Optional hardening (not blockers)

- Authentic older-save continuation replay beyond the schema66 byte-identical codec roundtrip.
- Additional adversarial checkpoint/reference restore cases beyond the concrete causal compatibility defects above.

**Next step:** Correct these three blockers, resolve the late-cause projection question through the established GPT delegation, rerun the relevant focused cases and full C# / package validations, retain final-source evidence, then request GPT's review of the correction commit. Do not begin a successor module until GPT actually accepts the current module and confirms dependency alignment.

## Follow-up consensus on a cause recorded after an early Haven checkpoint

GPT answered the bounded clarification for the early-checkpoint/later-attack sequence. **Choose the derived carry-forward behavior (option B), with timing made explicit.**

- Keep the early checkpoint unchanged. Its cause set, Pressure, die, result and consequence are facts at that checkpoint's applied revision.
- A later committed attack in the same Watch only establishes one outstanding OpenCombat category if that category was not already counted by the early checkpoint. Multiple later attacks add evidence but not more category increases.
- Reconcile that Watch's arithmetic once when the adjustment becomes due, using the original checkpoint's `PressureBefore`, the union of actual categories available by then, already-accounted reduction credits and the captured Risk floor. Derive the difference from the earlier `StoredPressure`; do not add one blindly after clamping. GPT's example: starting Pressure 0, one secured-route reduction and later combat remain `clamp(0 + 1 - 1) = 0`.
- The derived current Pressure includes the once-only adjustment at the Watch closing endpoint, or earlier actual safe-Haven admission. No second checkpoint, stored counter, or complication roll is created. The next eligible checkpoint incorporates the adjustment into `PressureBefore` once, then settles its own Watch categories.
- Historical validation reconstructs the adjustment from source history available at each checkpoint's causal position, not from the final journal indiscriminately.

GPT grounded the reconciliation in FL-08's once-only category increases and FL-09's one routine complication per active Watch. The source does not spell out the failed-Haven-admission sequence, so this is an explicit TEST_ONLY completion, not a claim that the extra timing rule appears in FL-08/FL-09. GPT confirmed no owner escalation or roadmap addition is needed. Requested acceptance: early checkpoint → later attack → duplicate-category attack → save/restore → reconciliation → next checkpoint, including no second roll, unchanged earlier checkpoint, one effective category, PressureBefore carry-forward, clamp/floor, and whole/split/restored agreement.

## Codex correction status before the next GPT review

Codex added regressions for the three blockers above and reproduced each against the `3d00c974` runtime. The correction preserves schema67 exact-Watch settlement reason, validates checkpoint source rows as of their applied revision, derives late same-Watch Pressure once at Watch close or actual Haven admission, and validates same-time attacks by receipt order with explicit completed-move evidence for a same-receipt departure opportunity attack. The earlier checkpoint and consequence remain immutable, with no second roll or serialized state.

The corrected cases pass individually. The full C# 9 warnings-as-errors suite passes **1,281/1,281** with 261 source hashes; dedicated Core/Persistence/LabModel compilation passes; static package validation passes **18/18** with 287 assets and 287 unique GUIDs. Baseline reproductions, focused reports, compiled assemblies, and scenario saves are retained in [the correction attempt packet](development-attempts/gpt-review-fixes-3d00c974/). These facts are Codex's validation only; GPT has not yet reviewed the correction commit. The next mapped module remains gated until GPT reviews the exact pushed commit, resolves any concrete blocker, and confirms dependency alignment.
