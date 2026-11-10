# GPT implementation review request — MGT-04 recipe-347

Review the implementation commit and retained evidence attached to this request in Unity Rules Engine Development. The source/API contract in `MGT04_RECIPE347_RULE_DECISIONS.md` was already agreed; please review the code and results against that exact contract rather than reopening its settled rules.

## Review target and changed files

The requesting message supplies the exact Engine commit. The changed-file list is the commit's `git show --stat` / `git show --name-only`; implementation files are indexed in `README.md`. The relevant additions are schema72 `Recipe347WorkOrderRecord`, output provenance, reusable physical Mining Tool profile, per-attempt use evidence, clock-derived tool work segments, codec, validation, the shared crafting/mining composition, focused connected cases, and architecture-map/handoff updates.

## Agreed scope and source requirements

The bounded scope is one `TEST_ONLY` recipe-347 work order that uses the pinned source card, recipe occurrence data and crafting/mining guides listed in `SOURCE_BINDINGS.json`. Reuse the existing `WorkLedger`, `ActiveWorkProgress`, shared clock and continuation, character/check facts, RNG, inventory/physical body/structure, command receipts, mining attempt/stock path, persistence and replay. Preserve Alchemy schemas18/20 and legacy deposit-bound schema49 save behavior. Transform the separately reserved existing body into the actual output; do not mint a duplicate item.

The full acceptance checklist is in `MGT04_RECIPE347_RULE_DECISIONS.md`. The implementation evidence explicitly identifies which checklist items remain unproven, so this request does not claim full module acceptance.

## Validation evidence

- `final-full-suite/run-20261110T015923929Z-15aece1b/results.json`: C# 9 regression pass, 1,302/1,302; the two-deposit case is among the passing cases; 276 source hashes.
- `final-assembly-compilation/compile-20261110T020716546Z-55c5d943/results.json`: warnings-as-errors C# 9 Core, Persistence and LabModel compile pass; 201 source hashes.
- `final-package-validation/static-20261110T020716539Z-d0fa9a1c/results.json`: 18/18 static structure checks; 302 package assets and 302 unique GUIDs.
- `two-deposit-1/.../results.json`: retained failure and corrected timing cause.

## Requested GPT response

Please inspect the exact code diff, record constructors/validation/codec branches, work and settlement logic, mining-use attribution, the test cases, the agreed contract and these reports. State what you actually inspected and which checks you did not run. Identify only concrete acceptance blockers or mismatches with the already-agreed contract; separate optional hardening from blockers. If the current increment still falls short, specify the smallest corrections/tests needed to close it and confirm that no successor module should start yet. If it satisfies the agreed bounded acceptance despite the limitations documented in `README.md`, say so and name the next dependency in the existing map. Codex will record your actual response and resolve any concrete blocker before starting another module.
