# Schema 70 Temporary Camp correction review packet

**Re-review target:** the corrected `Engine` revision containing this packet. Base runtime revision: `ae61cd16bc1c5ec88bc1a558696f71f7245e2188`.

## Scope and authority

This packet documents corrections for the three concrete defects found in the bounded schema70 Temporary Camp implementation review. It does not expand the feature or create a new gameplay rule. The scope, source pins, and acceptance contract are [CAMP_CONSTRUCTION_RULE_DECISIONS.md](../../../../CAMP_CONSTRUCTION_RULE_DECISIONS.md). The module remains a fixed `TEST_ONLY` two-person build using the shared `Simulation` command/query path, `RuleClock`, `WorkLedger`, existing inventory and portable-equipment records, actual character/training/condition/check data, deterministic RNG, receipts, snapshot transaction, and additive schema70 persistence. Schema69 and older codec branches are unchanged.

## Findings reproduced and corrected

1. **Synchronous handling and concurrent construction work.** `HandlePortableEquipment` advances the shared clock, but its handling-boundary preflight did not include the active construction completion boundary, and its elapsed-time settlement did not credit construction worker bookings. `TestOnlySharedWorldPolicy` now blocks a one-second handling operation when it would cross an unsupported construction completion boundary, and credits construction work from the actual shared `RuleClock` delta on accepted handling.
2. **Fixture movement after failed attempt.** The test-only fixture validator required the tent and pack to remain at the authored ground site even after a resolved failed attempt released the exact lots' claims. It now allows movement only for a lot whose matching resolved failed attempt released the entire claim, with no active claim or installation. Owner, provenance, lot identity, profile, mass, custody/location coherence remain checked; active claims/installations still require the authored placement.
3. **Fractional resume query.** The resume query exposed the numerator of exact `RuleTime` as an integer `CommandCost`, truncating a fractional remainder. It now uses the exact rational remainder and reports a cost only when the denominator is one. Full work requirements and saved progress remain exact.

Changed runtime/test files:

- `engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedTemporaryCampConstruction.cs`
- `engine/com.decennium.foundation/Tests/EditMode/TemporaryCampConstructionCases.cs`

The test file adds four narrow regressions: handling by an idle companion credits the lead worker's construction interval; handling cannot pass the completion boundary; a released failed-attempt fixture can be picked up and returned before a fresh full-duration retry; and a fractional resume query does not report a truncated duration.

## Reproduction and acceptance evidence

All four defect tests failed against the base runtime before the correction. Each corresponding focused test passes after the fix:

- Handling credit: [before](../gpt-review-reproduction/failure-before-fix/run-20261109T181459193Z-ed210844/results.json), [after](../gpt-review-reproduction/after-fix/case-1/run-20261109T181915825Z-941d7747/results.json).
- Completion boundary: [before](../gpt-review-reproduction/failure-before-fix/run-20261109T181703865Z-4b5d1df9/results.json), [after](../gpt-review-reproduction/after-fix/case-1-boundary/run-20261109T181954697Z-e9222f28/results.json).
- Failed-claim release and retry: [before](../gpt-review-reproduction/failure-before-fix/run-20261109T181540052Z-b141707f/results.json), [after](../gpt-review-reproduction/after-fix/case-2/run-20261109T182101486Z-d15e4e33/results.json).
- Fractional resume query: [before](../gpt-review-reproduction/failure-before-fix/run-20261109T181624950Z-8b42fd1d/results.json), [after](../gpt-review-reproduction/after-fix/case-3/run-20261109T182029378Z-346c2547/results.json).
- Existing connected save/resume/replay/Pressure scenario: [PASS, 1/1](focused-success/run-20261109T182502013Z-fc52c2f8/results.json).
- Full C# 9 warnings-as-errors suite: [PASS, 1,297/1,297](full-suite/run-20261109T182613929Z-17526785/results.json), 268 source hashes.
- Core, Persistence, and LabModel compilation: [PASS](compile/compile-20261109T182957815Z-4afc9b60/results.json), 196 source hashes. Unity compilation was not run.
- Static package validation: [PASS, 18/18](package-validation/static-20261109T182957870Z-9b5c0189/results.json), 294 assets and 294 unique GUIDs; this is not Unity validation.
- `git diff --check`: PASS.

## Review limits and remaining scope

The optional omission of construction progress/controls from generic `WorldActivityProjection.OpenProcedures` remains unimplemented and is submitted for blocker assessment; the agreed command/query scenario does not claim that UI-facing projection. Only this authored two-person `TEST_ONLY` profile is supported. Production crew/site rules, higher tiers, general storage/transfer, purchasing, dismantling, multiple/off-route camps, and general guard scheduling remain unsupported. Unity Editor import/compilation, Edit Mode, Play Mode, standalone build, and observed player gameplay were not run. These results do not complete MGT-03 or the engine. No successor implementation should begin until GPT reviews this exact revision, resolves concrete blockers, and agrees the current module meets acceptance and the next dependency follows the existing map.
