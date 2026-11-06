# Observation, Hide and Search — 2026-11-06 evidence

## Current Hidden-clearance acceptance

The current rerun is archived in [`hidden-clearance-20261106`](hidden-clearance-20261106/). The focused case, `observation_partial_exposure_clears_hidden_only_for_the_observer_who_sees`, establishes Hidden through actual shared-world `BeginFixedEncounter` and `Hide` commands with a deterministic successful roll against two observers. From the resulting valid saved state, it submits an exact 0-to-1.25-foot segment to the same `ObservationRules.ProcessWorldTraversalSegments` method called by shared movement.

The authored sight gap lets the companion see the moving actor during that interval while the second observer remains occluded. The test confirms direct-sight evidence clears only the companion's Hidden attempt, preserves Hidden for the second observer, saves and restores the partial snapshot byte-for-byte, repeats deterministically from identical Hide-state bytes, and leaves clock, RNG, revision and command receipts unchanged. It is processor-seam coverage: the test does not claim one legal command trace from tactical Hide through encounter exit into later exploration movement. The older shared movement trace separately verifies that the shared `WorldAdvance` path invokes the observation processor and retains stale fractional location knowledge after the actor reaches a concealed endpoint.

The follow-up [`attack-effect-blocker-20261106`](attack-effect-blocker-20261106/) adds shared-command acceptance for attack targeting: the target is visible and its location known through a transparent effect-only barrier, but line of effect rejects the attack atomically. This verifies the existing distinction between sight and effect in the combat transaction. It does not close post-attack disclosure. The current visual-only policy has no supported event-sensory channel for perceiving a hidden attacker's location; see the observation decision record.

The follow-up [`invisible-latch-20261106`](invisible-latch-20261106/) closes one pinned Invisible transition: when the target's location is already current as Invisible begins, sight is blocked but the location remains known and the observer latches that continuous episode. A shared tactical step then moves the target unseen; current knowledge expires, the prior coordinates remain stale, and the same episode latch survives save/restore. The acceptance deterministically replays the shared encounter/condition trace. The first runs reproduced the missing episode latch; a later expanded-test run exposed an invalid nonadjacent fixture destination, corrected to the legal adjacent destination. Both diagnoses and original reports are retained with the passing results.

## Validation

- Focused Hidden-clearance case: **PASS, 1/1**.
- Follow-up blocked-line-of-effect case: **PASS, 1/1**.
- At the Hidden-clearance checkpoint, the full C# 9 warnings-as-errors suite passed **1,176/1,176**, zero failed; static package validation passed **18 checks; 237 assets; 237 unique GUIDs**.
- Source bindings and report timestamps: [`hidden-clearance-20261106/SOURCE_BINDINGS.json`](hidden-clearance-20261106/SOURCE_BINDINGS.json) and [`attack-effect-blocker-20261106/SOURCE_BINDINGS.json`](attack-effect-blocker-20261106/SOURCE_BINDINGS.json).

The newest Invisible-latch focused case passes **1/1**; the newest full suite passes **1,177/1,177** and static package validation passes **18 checks; 237 assets; 237 unique GUIDs**. Exact receipts and source hashes, including the diagnosed failed attempts, are in [`invisible-latch-20261106`](invisible-latch-20261106/).

The prior traversal reports remain in the original archive files for historical context; their 1,174/1,174 count predates this acceptance. The current three reports are in the `hidden-clearance-20261106` directory.

## Review scope

The observation review packet was owner-authorized for transmission, but is still not transmitted: two fresh Chrome window captures timed out under the required computer-use workflow. The new [`invisible-latch-20261106/REVIEW_PACKET.md`](invisible-latch-20261106/REVIEW_PACKET.md) contains the requested increment summary, changed C# excerpts and validation for the next allowed review attempt. Earlier GPT feedback covered supplied excerpts of schema51 geometry and placement validation only. The retained [`CODE_REVIEW_PACKET.md`](CODE_REVIEW_PACKET.md) is historical and must not be treated as a current source review.
