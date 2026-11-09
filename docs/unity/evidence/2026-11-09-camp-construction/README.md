# Schema 70 Temporary Camp construction evidence

**Status:** implementation checks pass; GPT implementation review is pending. This bounded profile remains `TEST_ONLY`; it does not complete MGT-03 or the C# gameplay simulation.

## Scope, authorities, and acceptance

This increment implements one two-person Temporary Camp build at an existing schema 69 expedition camp site. It binds the route tier explicitly in the fingerprinted TEST_ONLY profile because route records have no tier field. It uses the shared simulation command/query path, RuleClock, WorkLedger worker intervals and material reservations, actual character and skill-training records, condition/check resolution, deterministic RNG, receipts, snapshot transaction, and additive schema 70 persistence. The source and agreed completions are pinned in [the camp-construction contract](../../CAMP_CONSTRUCTION_RULE_DECISIONS.md).

The bounded source requirements are 480 active Support minutes, one lead check after completion at the route tier DC, up to three actually trained assistants at +1 each without reducing duration, one Support mark for success and two for critical success. The fixed fixture requires an actual two-person tent and fitting pack, both retained as physical lots under durable installation-linked claims. Completion and the 20 Load / 200 lb / 20 ft³ capacity are derived from the saved check and both installations. Failure preserves undamaged goods, releases unused claims, and awards no marks. Construction creates no camp-use Pressure cause and conflicts with lying-low through existing authorities.

The runnable case `temporary_camp_construction_schema70_save_resume_replay_and_pressure` travels through the existing route, starts construction with two trained characters, reserves both physical fixtures, works four hours, pauses, saves/restores, resumes, completes the check, verifies one/two derived marks and installed lots, then invokes actual camp use and the existing Pressure procedure. It compares restored deterministic continuation with an identical restored command history and with uninterrupted semantic outcomes. Separate cases cover failure/retry, lying-low exclusion, and composition with the existing hunting-trap fixture. The paused save is preserved in [saves](saves/temporary-camp-construction-paused.ddsave).

## Exact validation

- Full C# 9 warnings-as-errors foundation suite: **PASS, 1,294/1,294**, 268 source hashes: [report](reports/full-suite/results.json).
- Dedicated Core, Persistence, and LabModel compilation: **PASS**, 196 source hashes; tests and Unity compilation were not part of this command: [report](reports/compile/results.json).
- Static package validation: **PASS, 18/18**, 294 package assets and 294 unique GUIDs; this is not Unity import or Editor validation: [report](reports/package-validation/results.json).
- Focused success/mark/replay case: **PASS, 1/1**: [report](reports/focused-success/results.json).
- Focused failure/claim-release/retry case: **PASS, 1/1**: [report](reports/focused-failure/results.json).
- Focused schema 70 plus hunting-trap composition case: **PASS, 1/1**: [report](reports/focused-composition/results.json).
- Focused saved-result mark projection (Success/Critical Success/Failure => 1/2/0): **PASS, 1/1**: [report](reports/focused-mark-projection/results.json).
- `git diff --check`: **PASS**.

The final full-suite, compile, and package reports were generated against the same final C# sources. Unity Editor import/compilation, Edit Mode, Play Mode, standalone game builds, and observed player gameplay were **not run**.

## Review corrections and retained failed attempts

An independent read-only code review identified that the hunting-trap fixture validator rejected the schema 70 composition. The validator now admits schema 70 only when the camp-construction profile is selected, and the combined-fixture regression passes. The reviewer also pointed out that the contract's one/two Support marks needed an explicit projection and assertions. `SupportMarks` now derives the count from immutable successful check results, without storing duplicate mark state; the success and failure regressions assert the derived count. No other mutable mark ledger was added.

During implementation, compilation first discovered use of an internal character-rule helper by the test fixture; the test now uses the public `AbilityCheckRules.Derive`. The first complete suite failed 3 of 1,292 construction cases because linked GenericPounds equipment incorrectly supplied an independent operational weight; the fixture now leaves that derived field unset. A later start attempt returned `InvalidResult` because existing portable-equipment and hunting-trap work-attribution validators did not recognize construction job IDs; the attempt IDs were added to those existing allowlists. Focused runs also exposed a test that manually edited the initial skill-training snapshot rather than using the fingerprinted route-mapping fixture, missing schema 70 composition in route-mapping/travel validators, and a completion receipt revision off by one. These were corrected in the shared records/model or fixture, then rerun in the final suite. The first compilation and full-suite result files are retained under [development attempts](development-attempts/).

The independent reviewer noted one optional integration gap: construction progress and controls are not yet emitted by the generic `WorldActivityProjection.OpenProcedures`. The agreed source contract and runnable command/query acceptance do not include that projection; this remains an explicit follow-up question for GPT, not an implemented or silently assumed feature.

## Boundaries and unsupported capabilities

This is one authored two-person TEST_ONLY profile. It does not provide production crew qualification, a general site-authoring system, arbitrary purchases/currency, other camp tiers, general storage transfer, dismantling, multiple camps, off-route construction, general guard scheduling, or higher-tier mark spending. The three storage limits are derived facts only; no storage contents or transfer handler are created. The 2 gp source references do not debit currency. Existing site exposure/concealment facts remain authoritative. The complete MGT-03 subsystem and engine are unfinished.

**GPT implementation review:** pending. No claim of acceptance or successor-module agreement has been made yet.
