# GPT implementation review record — schema70 Temporary Camp

## Review of `ae61cd16bc1c5ec88bc1a558696f71f7245e2188`

**Verdict:** hold acceptance for three concrete integration defects. The main construction scenario and the narrow hunting-trap schema admission correction looked sound, but GPT found supported-path issues in synchronous inventory handling, movement of released fixtures, and fractional resume query cost.

1. Synchronous handling advanced `RuleClock` without checking the camp-construction completion boundary or crediting booked construction work. GPT requested handling-credit and exact-boundary regressions.
2. Fixture validation required original ground placement even when an item was unclaimed, including after a failed attempt released its claims. GPT requested that placement requirements follow actual claims/installations, plus failure, pickup, save/restore, retry and installed-item protection coverage.
3. Resume queries reported `RuleTime.Numerator` as integer seconds while discarding a fractional denominator. GPT requested exact duration or omission of the integer cost for fractional remainders.

GPT assessed the missing construction entry in `WorldActivityProjection.OpenProcedures` as optional follow-up, not an acceptance blocker. It found no confirmed historical codec-layout regression, but did not certify every historical continuation. It found no named successor selected by the current map while schema70 acceptance remained open.

## Re-review of `e1bf33c3a52c4ccd365c8a5ff70880464e91a92e`

**Verdict:** acceptance remained on hold for the pre-attempt part of finding 2. Findings 1 and 3 were closed. GPT found post-failure pickup, restore, and return-before-retry covered, but observed that the condition `releasedByFailure && !activelyClaimed && !installed` still rejects pickup of an otherwise unclaimed tent before any attempt. The portable handler moves it, then whole-snapshot validation returns `InvalidResult`.

GPT's requested smallest correction is to allow coherent existing-authority movement whenever the fixture is neither actively claimed nor installed, while preserving fixture identity, ownership, quantity, and custody/location coherence. Construction admission and active claims/installations must still require the authored site. The requested regression is: before any attempt, pick up the tent, file-save/restore, verify construction is rejected while it is carried, return it, then start construction; keep installed-item pickup rejection.

The missing generic `WorldActivityProjection.OpenProcedures` display remained optional, not a blocker. GPT found no additional confirmed save-layout or historical-codec regression. It noted that the four correction-focused reports had an earlier test-file hash than the final full-suite report, but this was not a blocker because the full suite included all four cases and the connected-case/compile hash lists matched the full report. GPT's inspection covered the exact diff, runtime/tests, portable handling and transaction validation, contract, reports, and updated map/handoff. GPT did **not** independently compile, execute tests, recompute source hashes, or run Unity; it made no repository changes.

The current map/handoff does not name a post-construction successor. GPT directed that the residual item-movement case be fixed before successor work; no successor was added while acceptance remained open.

## Re-review of `2553c738ed17262b222d296458e6694ed1304ce8`

**Verdict:** accepted. GPT stated: “commit `2553c738` closes the remaining blocker. I find no confirmed acceptance blocker in this bounded schema70 TEST_ONLY module.”

GPT confirmed the pre-attempt pickup defect is closed: coherent existing portable-equipment movement is allowed while a fixture is neither actively claimed nor installed; identity, provenance, quantity, mass, ownership, and custody/location checks remain. Construction admission still requires both actual lots at the authored site, and active claims and installations remain protected. The new regression covers pickup before any attempt, file save/restore, construction rejection while carried, return, and a fresh claim on the same lot. The retained before report fails with `InvalidResult`; the after report passes.

GPT also confirmed the other two findings from its review of `ae61cd16` remain closed: synchronous handling credits construction and enforces the completion boundary, and fractional resume duration is no longer truncated. It accepted the bounded construction/save/resume/replay/Pressure scenario, found no new historical schema or codec conflict, and confirmed the `TEST_ONLY` boundary remains intact. The missing generic `WorldActivityProjection.OpenProcedures` display is optional integration work, not an acceptance blocker under the agreed contract.

GPT inspected the exact commit diff, fixture validation/admission, regression and connected-test assertions, review packet, evidence overview, before/after and final reports, and handoff/map. It compared shared recorded source-hash entries and found no mismatches. GPT did **not** independently compile, run tests, execute save roundtrips, recompute hashes, or run Unity; it made no repository changes. The retained reports show the C# 9 warnings-as-errors suite at 1,298/1,298, Core/Persistence/LabModel compilation passing, and static package checks at 18/18 (294 assets/GUIDs).

**Successor:** the current map/handoff names no post-construction dependency. GPT directed that this acceptance be recorded, then a next dependency be selected and agreed from the existing map before implementation. No successor has yet been selected or authorized. The full engine remains incomplete; Unity remains deferred.
