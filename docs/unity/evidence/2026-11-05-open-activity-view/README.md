# Open activity and manufacturing choice view — 2026-11-05

## Scope

This C# increment extends the existing transient read model over authoritative procedure and traversal records. `OpenProcedures` includes stored working, paused, and explicit awaiting states. `Traversals` exposes persisted partial route position and the existing admissible suspend/resume controls. The legacy `CurrentWork(snapshot)` membership and ordering remain unchanged for active-labor conflict checks.

The manufacturing addition is limited to pure query and discovery for the existing `ResolveManufacturingQuality` command. It uses the current quality/catalyst/yield validation and the existing resolver for actual settlement. The resolver remains authoritative for claims, output, XP, random state and pending clock continuation. No costs, gameplay rules, schema fields, or general procedure framework were added. Passive intervals and procedure-specific claims that are not stored in `WorkLedger` remain outside these views.

## Acceptance

- The two-configuration shared-world scenario checks a paused harvest against its stored progress while a different actor holds a partial exploration route. Both records survive save/load. The route can be suspended and restored, its exact distance and resume option are reconstructed, and the scenario continues through explicit harvest resume, result settlement and further exploration.
- The manufacturing pending-choice scenario checks the `AwaitingChoice` row, its stored claims, legal quality/catalyst choices, invalid-catalyst rejection, pure queries, reconstruction after save/load, exact continuation, and duplicate-command protection.
- The mid-round tactical scenario checks that the order owner can discover, query and resolve the saved quality choice while another actor owns the current turn, then resumes the original outgoing-slot continuation once.
- The manufacturing awaiting-check case confirms the procedure remains visible before the existing explicit recovery/check path.
- The Trap setup/retrieval and off-calendar gate cases preserve their prior query and resolver behavior.

## Validation

- Seven focused acceptances passed **1/1 each**: shared-world architecture, manufacturing `AwaitingCheck`, manufacturing `AwaitingChoice`, off-turn tactical manufacturing choice, Trap setup, Trap retrieval, and the off-calendar gate.
- Full deterministic suite: **1,118/1,126**. The eight failures are identical by name and `HarvestValidation` exception to the saved prior baseline in [Prowl/OpenRA extraction evidence](../2026-11-05-prowl-openra-extraction/BASELINE_RESULTS.json). Core, Persistence, LabModel and headless test sources compiled with C# 9 warnings as errors.
- Static package validation: **14/14 passed**.

The first architecture rerun exposed an assumption in the test helper: it rejected an integral target when the current clock was fractional after the new half-second route step. The same assertion reproduced on the second run. The helper was changed to advance by the exact rational remainder; the architecture scenario then passed. This was a test-helper limitation, not a simulation or projection failure.

`HEADLESS_RESULTS.json` retains full case outcomes and source hashes. Focused receipts retain the individual acceptance outcomes. `PACKAGE_RESULTS.json` retains the static package checks. Generated result files are receipts only; `engine/artifacts/` remains ignored build output.
