# Schema 70 Temporary Camp construction evidence

**Status:** the three concrete review blockers below are corrected and the focused regressions plus full C# validations pass; GPT re-review is pending. This bounded profile remains `TEST_ONLY`; it does not complete MGT-03 or the C# gameplay simulation.

## Scope, authorities, and acceptance

This increment implements one two-person Temporary Camp build at an existing schema 69 expedition camp site. It binds the route tier explicitly in the fingerprinted TEST_ONLY profile because route records have no tier field. It uses the shared simulation command/query path, RuleClock, WorkLedger worker intervals and material reservations, actual character and skill-training records, condition/check resolution, deterministic RNG, receipts, snapshot transaction, and additive schema 70 persistence. The source and agreed completions are pinned in [the camp-construction contract](../../CAMP_CONSTRUCTION_RULE_DECISIONS.md).

The bounded source requirements are 480 active Support minutes, one lead check after completion at the route tier DC, up to three actually trained assistants at +1 each without reducing duration, one Support mark for success and two for critical success. The fixed fixture requires an actual two-person tent and fitting pack, both retained as physical lots under durable installation-linked claims. Completion and the 20 Load / 200 lb / 20 ft³ capacity are derived from the saved check and both installations. Failure preserves undamaged goods, releases unused claims, and awards no marks. Construction creates no camp-use Pressure cause and conflicts with lying-low through existing authorities.

The runnable case `temporary_camp_construction_schema70_save_resume_replay_and_pressure` travels through the existing route, starts construction with two trained characters, reserves both physical fixtures, works four hours, pauses, saves/restores, resumes, completes the check, verifies one/two derived marks and installed lots, then invokes actual camp use and the existing Pressure procedure. It compares restored deterministic continuation with an identical restored command history and with uninterrupted semantic outcomes. Separate cases cover failure/retry, lying-low exclusion, and composition with the existing hunting-trap fixture. The paused save is preserved in [saves](saves/temporary-camp-construction-paused.ddsave).

## Exact validation

- Full C# 9 warnings-as-errors foundation suite after the review corrections: **PASS, 1,297/1,297**, 268 source hashes: [report](development-attempts/gpt-review-fixes/full-suite/run-20261109T182613929Z-17526785/results.json).
- Dedicated Core, Persistence, and LabModel C# compilation: **PASS**, 196 source hashes; tests and Unity compilation were not part of this command: [report](development-attempts/gpt-review-fixes/compile/compile-20261109T182957815Z-4afc9b60/results.json).
- Static package validation: **PASS, 18/18**, 294 package assets and 294 unique GUIDs; this is not Unity import or Editor validation: [report](development-attempts/gpt-review-fixes/package-validation/static-20261109T182957870Z-9b5c0189/results.json).
- Main save/resume/replay/Pressure scenario: **PASS, 1/1**: [report](development-attempts/gpt-review-fixes/focused-success/run-20261109T182502013Z-fc52c2f8/results.json).
- Four focused regressions covering the three review findings: **PASS, 4/4** after correction. Their before/after reports are linked below.
- Focused success/mark/replay case: **PASS, 1/1**: [report](reports/focused-success/results.json).
- Focused failure/claim-release/retry case: **PASS, 1/1**: [report](reports/focused-failure/results.json).
- Focused schema 70 plus hunting-trap composition case: **PASS, 1/1**: [report](reports/focused-composition/results.json).
- Focused saved-result mark projection (Success/Critical Success/Failure => 1/2/0): **PASS, 1/1**: [report](reports/focused-mark-projection/results.json).
- `git diff --check`: **PASS**.

The final full-suite, compile, and package reports were generated against the same final C# sources. Unity Editor import/compilation, Edit Mode, Play Mode, standalone game builds, and observed player gameplay were **not run**.

## Review corrections and retained failed attempts

An earlier read-only code review identified that the hunting-trap fixture validator rejected the schema 70 composition. The validator now admits schema 70 only when the camp-construction profile is selected, and the combined-fixture regression passes. The reviewer also pointed out that the contract's one/two Support marks needed an explicit projection and assertions. `SupportMarks` now derives the count from immutable successful check results, without storing duplicate mark state; the success and failure regressions assert the derived count. No other mutable mark ledger was added.

A subsequent review found three concrete implementation defects. First, synchronous one-second inventory handling did not preflight or credit concurrently booked camp-construction work through the shared `RuleClock`; handling now rejects an unsupported completion boundary and credits the construction worker interval for elapsed shared time. Second, the authored-fixture validator still required an item to remain at its original ground site after a failed attempt had released the claim; it now permits movement only after the matching resolved failure released that lot, while retaining identity/provenance checks and the original-site requirement for active claims/installations. Third, the resume query truncated fractional `RuleTime` by reporting its numerator as integer cost; it now exposes a cost only for an integral remainder, while keeping full work and the exact remainder authoritative. Baseline failures and post-fix passes are retained in [the review reproduction reports](development-attempts/gpt-review-reproduction/); the exact correction set and evidence index are in [the review-fix record](development-attempts/gpt-review-fixes/REVIEW_PACKET.md).

During implementation, compilation first discovered use of an internal character-rule helper by the test fixture; the test now uses the public `AbilityCheckRules.Derive`. The first complete suite failed 3 of 1,292 construction cases because linked GenericPounds equipment incorrectly supplied an independent operational weight; the fixture now leaves that derived field unset. A later start attempt returned `InvalidResult` because existing portable-equipment and hunting-trap work-attribution validators did not recognize construction job IDs; the attempt IDs were added to those existing allowlists. Focused runs also exposed a test that manually edited the initial skill-training snapshot rather than using the fingerprinted route-mapping fixture, missing schema 70 composition in route-mapping/travel validators, and a completion receipt revision off by one. These were corrected in the shared records/model or fixture, then rerun in the final suite. The first compilation and full-suite result files are retained under [development attempts](development-attempts/).

The independent reviewer noted one optional integration gap: construction progress and controls are not yet emitted by the generic `WorldActivityProjection.OpenProcedures`. The agreed source contract and runnable command/query acceptance do not include that projection; this remains an explicit follow-up question for GPT, not an implemented or silently assumed feature.

## Boundaries and unsupported capabilities

This is one authored two-person TEST_ONLY profile. It does not provide production crew qualification, a general site-authoring system, arbitrary purchases/currency, other camp tiers, general storage transfer, dismantling, multiple camps, off-route construction, general guard scheduling, or higher-tier mark spending. The three storage limits are derived facts only; no storage contents or transfer handler are created. The 2 gp source references do not debit currency. Existing site exposure/concealment facts remain authoritative. The complete MGT-03 subsystem and engine are unfinished.

**GPT implementation re-review:** pending for the corrected revision. The next module remains gated; no claim of schema70 acceptance or successor-module agreement has been made.
