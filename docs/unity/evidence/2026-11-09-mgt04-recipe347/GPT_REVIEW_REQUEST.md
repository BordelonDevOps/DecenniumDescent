# GPT implementation review request — MGT-04 recipe-347

Review the exact Engine implementation commit supplied with this packet. The pinned source/API contract in `MGT04_RECIPE347_RULE_DECISIONS.md` was already agreed. Review implementation and evidence against that contract; do not reopen settled source decisions.

## Scope and source requirements

This is one `TEST_ONLY` recipe-347 work order connected to the existing physical Mining Tool body and mining path. Reuse `WorkLedger`, `ActiveWorkProgress`, shared clock and continuation, character/check facts, RNG, inventory and physical body/structure, command receipts, existing mining attempts/stock, persistence and replay. Recipe records are gated at schema72; the composed counted-lot simulation selects schema73. Preserve Alchemy schema18/20 and legacy deposit-bound mining schema49 behavior.

The pinned sources and blob hashes are in `SOURCE_BINDINGS.json`; the agreed contract, including source-derived requirements and explicitly TEST_ONLY operational decisions, is in `MGT04_RECIPE347_RULE_DECISIONS.md` and `GPT_CONSENSUS.md`.

## Acceptance evidence

- Full C# 9 warnings-as-errors suite: **PASS 1,314/1,314**, 276 source hashes: `final-full-suite-after-rest-watch-fix/run-20261110T072657128Z-d0682274/results.json`.
- Standalone warnings-as-errors compilation: **PASS** Core, Persistence and LabModel, 201 source hashes: `final-assembly-compilation-after-rest-watch-fix/compile-20261110T074206511Z-bc20a1f8/results.json`.
- Static package validation: **PASS 18/18**, 302 assets / 302 unique GUIDs: `final-package-validation-after-rest-watch-fix/static-20261110T074206559Z-89732e3d/results.json`.
- Two-deposit same-item mining, movement, restore and replay: included in the full report and focused rerun `review-fixes/rest-watch-corrected/run-20261110T072316709Z-a3660239/results.json`.
- The initial post-Watch-gate full run failed **2/1,314** at `Recipe347ScheduledRestWatch`; both cases reproduced individually. Only fixture timing was corrected. Original report: `final-full-suite-rerun/run-20261110T070232405Z-b1aeb32a/results.json`; reproductions: `review-fixes/reproduce-rest-watch/`.

The implementation evidence README indexes the connected scenarios, exact source responsibilities, limitations and validation results. This request does not claim GPT acceptance.

## Review requested

Inspect the exact code diff and changed-file list, constructors/validation/codec branches, work booking and settlement, mining-use attribution, runnable scenarios, source bindings, reports, architecture trace and handoff. State what you actually inspected and which checks you did not perform. Separate concrete blockers from optional hardening. In particular, assess whether existing versioned schema18/20/49 tests are sufficient for the historical-save requirement despite the lack of an authenticated pre-increment schema18/49 golden save in this packet, and whether the connected scenarios satisfy the agreed acquisition-to-crafting-to-mining acceptance.

If the current bounded increment satisfies its agreed criteria, say so and name the next dependency in the existing map. If not, identify the smallest corrections and tests required. Codex will record your actual response and resolve concrete blockers before starting a successor module.
