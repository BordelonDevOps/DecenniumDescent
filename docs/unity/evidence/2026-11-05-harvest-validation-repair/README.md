# Schema42 harvest validation repair

**Status:** complete for the bounded TEST_ONLY fixture and existing resolver path. No harvest rule, snapshot schema, command fingerprint, or persistence field was added or changed.

## Responsibilities and authoritative state

This increment repairs the schema42 finite-harvest fixture and command admission so a valid manifest can be selected by its record ID while the requested anatomy version is checked against that manifest. `HarvestValidation` remains the authority for donor, manifest, category, unit, allocation and mass invariants. Existing `HarvestSelectionRequest`, `CommandReceipt`, shared RNG/clock, work ledger, inventory settlement and snapshot codec remain authoritative for command identity, timing, randomness, output and save/replay behavior.

## Reproduced causes

The initial Small fixture stored `TEST_ONLY.ordinary-river-fish-anatomy-v1` on its donor while the manifest stored `TEST_ONLY.small-river-fish-anatomy-v1`. Snapshot encoding rejected it with `Harvest manifest exceeds its actual donor anatomy or fixed allocation.` The validator was correct; the fixture was inconsistent. The repair creates both records from the same selected anatomy profile and asserts that invariant.

After that repair, the batch cases reached the resolver and exposed a separate gate defect. A valid command targets `harvest.manifest...` and supplies the anatomy version in `HarvestSelectionRequest.ManifestVersionId`. `AssessHarvestCommand` compared those distinct identifiers before looking up the manifest, so six valid-selection cases returned `HarvestSelectionRequired`. The corrected path looks up the manifest by `Command.Target`, then compares the request version to `manifest.AnatomyVersionId`. A wrong-version request still rejects with `HarvestManifestVersionMismatch`, before clock/RNG/state mutation.

The one-category fixture had a category record listing three units, but two unit records still named the second category. The fixture now assigns those unit records to the single selected category when that mode is enabled. It does not weaken exact category membership validation.

## Acceptance scenario

Create the Small finite-yield TEST_ONLY fish, encode/restore its two-category manifest, reject a wrong anatomy version without mutation, start the valid full allocation and roundtrip its canonical command receipt, save/restore active work, complete the one-check harvest, and verify output/mass conservation plus duplicate replay. In the single-category fixture, verify that all three preregistered material records match the one category and resolve under one check. Existing neighboring cases cover partial category timing/forfeiture, unique/tied failure choice, critical damaged-unit recovery and unknown values.

## Validation

- Initial defect reproduced: **0/1**, archived as [donor failure reproduction](REPRODUCE_DONOR_FAILURE.json).
- The first repair exposed the command ID/version and category-membership failures: **1,126/1,133**; archived as [intermediate failures](EXPOSED_SELECTION_FAILURES.json).
- Donor-profile, full two-category, and single-category focused acceptances: **1/1 each**; see the three `FOCUSED_*.json` results.
- C# 9 warnings-as-errors compilation: **PASS**; complete deterministic suite: **1,133/1,133 PASS** in [headless results](HEADLESS_RESULTS.json).
- Static package validation: **18/18 PASS**, 213 assets and 213 GUIDs in [package results](PACKAGE_RESULTS.json).
- Independent read-only review found no actionable defects. The reviewer did not run tests; validation above is from the recorded local runner.

## Source and limits

Harvest rules remain bound to the pinned sources and their hashes in [finite-source harvesting evidence](../2026-11-05-finite-source-harvesting/SOURCE_BINDINGS.json). This repair changes only TEST_ONLY fixture identity and resolver validation. It does not generalize anatomy authoring, implement additional creatures/categories, or qualify editor/runtime/player behavior.
