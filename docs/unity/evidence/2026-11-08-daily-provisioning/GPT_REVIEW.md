# GPT review — MGT-03 daily provisioning correction

## Reviewed commit and outcome

- Branch: `Engine`
- Commit reviewed: [`e4e12fb651fd029cec469e34ebf07214ce55194c`](https://github.com/BordelonDevOps/DecenniumDescent/commit/e4e12fb651fd029cec469e34ebf07214ce55194c)
- Parent: `d4662e3b26e16f665082270229f61830be630c68`
- Outcome: **accepted for the bounded TEST_ONLY MGT-03 module; no remaining concrete acceptance blocker.**

GPT confirmed the four corrections close its findings from the previous review:

1. Candidate `Current` projection includes the pending commit revision, while historical checks keep explicit causal cutoffs. Route partition equivalence and immediate work interruption are covered.
2. `ReadForResolution` supplies effective maximum HP, and `RecordFromResolution` preserves the persisted base maximum. Dose attribution, Critical Wounds healing ceiling, and damage thresholds are covered.
3. Initiative-based Dash timing requires active tactical control and membership in initiative order. Post-exit and off-calendar companion cases are covered.
4. Death-save recovery-d4 gating uses the modified result with natural-roll exceptions. Natural 10/11, RNG consumption, and restored continuation are covered.

GPT also confirmed the midnight-spanning intake case allocates one actual intake across both days: one pound per day and two pounds consumed overall. It found no new source-policy contradiction, duplicated authority, or confirmed older-schema compatibility defect in the changed paths. The correction adds no schema fields or codec changes.

## What GPT inspected and did not run

GPT inspected the pushed correction diff, relevant implementations, added test bodies, retained pre-fix failure results, source clauses, the decision contract, validation reports, implementation trace, and handoff. It checked that all thirteen named module cases appear as passing in the full report.

GPT did **not** run C# tests, builds, the package validator, Unity checks, or an independent 249-file hash audit. The reported passes are Codex-run evidence; GPT reviewed the retained reports rather than independently executing them.

Codex validation retained for this commit: C# 9 warnings-as-errors **1,255/1,255**, compiling Core, Persistence, LabModel, and HeadlessTests; static package validation **18/18** (275 assets / 275 unique GUIDs); source-bound audit **4 snapshots / 17 profiles / 340 RP cells / 13 named cases**; and `git diff --check` passed. Unity import/editor compilation, Unity tests, player build, and human-observed gameplay were not run.

## Optional hardening, not acceptance blockers

- Forged settlement, intake, and reservation-link restore tests.
- An authentic pre-change schema61 save and continuation.
- An end-to-end Critical Wounds healing scenario. Current coverage tests the critical healing ceiling through the resolution helper; capped dose use is connected to the simulation.

No implementation disagreement remains for the accepted MGT-03 increment.

## Selected next mapped dependency

GPT recommended continuing the existing MGT-03 map with **qualifying Rest Watch and Rest Debt accounting**, using pinned FL-03 and the recovery ordering in `STRAIN_PLAYTEST.md`. Codex agrees; this selection follows the existing MGT-03 row for supply, camps, rest, and pressure. It is recorded in `DEVELOPMENT_HANDOFF.md` and `IMPLEMENTATION_TRACE.md` before implementation.

The successor must reuse the shared `RuleClock`, work reservations, Strain projection/history, command receipts, and snapshot persistence. It must represent actual rest intervals and incompatible work, missed-rest debt and its exact deadline, once-only debt-related Strain gains, and debt clearance by a qualifying safe eight-hour Rest. Debt clearance remains separate from beneficial Long Rest rewards and from blocked Expedition Strain removal. Its connected acceptance combines companion work with the lead's missed and restored Rest, saves before a debt deadline, and compares whole versus split/restored advancement. The increment does not silently add Long Rest rewards, Strain recovery, Morale Rest, Haven care, or new safety/eligibility rules.

The relevant rules are in the pinned `EXPEDITION_PLAYER_BOOK.md` at source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, blob `466871fc128dc5f06043a874da2b9c1d94ed80a5` (FL-03), and pinned `STRAIN_PLAYTEST.md`, blob `7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4` (Rest Debt order and recovery distinctions). These exact snapshots are retained in this evidence directory.
