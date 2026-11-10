# MGT-04 recipe-347 correction review packet

**Review status:** GPT accepted source `381942726e470d283fad16dfb061f792da184b56` for the agreed bounded `TEST_ONLY` recipe-347 increment and found no remaining concrete acceptance blocker. The accepted candidate closes the two prior code/test findings and the missing-evidence publication gap. This does not complete all of MGT-04 or the engine. GPT's next mapped recommendation is a MGT-05 source/API review of preservation/spoilage with physical inventory; no MGT-05 implementation has started.

## Agreed scope and authority

This remains the bounded `TEST_ONLY` recipe-347 craft-to-mining increment described by [MGT04_RECIPE347_RULE_DECISIONS.md](../../MGT04_RECIPE347_RULE_DECISIONS.md), bound to the pinned source rows in [SOURCE_BINDINGS.json](../2026-11-09-mgt04-recipe347/SOURCE_BINDINGS.json). It adds no new recipe, character-creation, advancement, class or balance rules.

The work order, output provenance, reusable mining-tool profile, attempt-use evidence and measured work segments use the existing `WorkLedger`, active work, `RuleClock`, character/check facts, shared RNG, inventory lots, physical equipment/structures, mining records, command receipts and snapshot codec. Recipe records use schema72 and counted lots compose at schema73. Existing history and inventory remain authoritative; no duplicate clock, RNG, inventory or mutable Watch counter was introduced.

## Actual previous GPT verdict and correction

GPT reviewed the seven-file correction `11e77c5` and returned **HOLD**. It closed the earlier findings about Mishap 3 damage validation, indivisible counted quantities, schema49 lifecycle isolation, and the connected scenario, but identified two remaining blockers:

1. **Fouled-apparatus remedy was gated too broadly.** Physical Miner’s-kit custody and `mining-tools` training were imposed on every recipe Mining remedy. The pinned mishap result 5 allows any physically capable worker, including concurrent workers, to clear the fouled station. Those kit/training constraints belong to recalibration; source-qualified result 6 keeps its lead-worker rule. GPT requested result-specific gates and a result-5 regression with an untrained capable worker, save/restore and replay.
2. **The Work Watch test did not reach its asserted boundary.** It paused recipe work at 24 hours plus one second, which truncates the booked interval there, but asserted an endpoint at hour 32. GPT requested an actual boundary-touching booking while preserving both booking-order checks and without changing work accounting.
3. **Evidence was missing from the pushed review packet.** GPT followed all seven result links and got 404 because only the README and request were published. It also requested correcting an older note that attributed the mishap target to AssayKit; the checked source targets `MiningToolsStructureId`.

The actual review and its inspection/validation limits are recorded in [GPT_REVIEW.md](GPT_REVIEW.md). GPT did not compile, run tests, replay saves, recompute hashes or run Unity. Optional hardening suggested for future consideration was authenticated historical schema18/49 golden saves and a conservation-valid forged fractional snapshot; these were not blockers in its verdict.

## Current candidate and changed source files

The follow-up source commit is [`381942726e470d283fad16dfb061f792da184b56`](https://github.com/BordelonDevOps/DecenniumDescent/commit/381942726e470d283fad16dfb061f792da184b56). It changes:

- `engine/com.decennium.foundation/Laboratory/Model/SharedCraftingConsequences.cs`
- `engine/com.decennium.foundation/Tests/EditMode/Recipe347Cases.cs`

Together with `11e77c5`, the correction sequence changes seven unique source files: the two above plus `Laboratory/Model/PortableEquipment.cs`, `Laboratory/Model/SharedRecipe347.cs`, `Laboratory/Model/TestOnlyInventoryPolicy.cs`, `Runtime/Core/MiningRecords.cs`, and `Runtime/Core/PortableEquipmentRecords.cs`.

The remedy now applies the kit/training gate only to recalibration, permits a capable untrained worker to clear a recipe result-5 fouled apparatus, preserves source-qualified result-6 lead-only behavior, and identifies recipe mishaps through matching `Recipe347WorkOrders.IncidentId` rather than including unrelated Mining incidents. The Work Watch case now reaches the real 32-hour interval boundary and selects the recipe interval ending there; both booking orders remain covered. No work accounting rule changed.

## Acceptance criteria and runnable evidence

The acceptance is source-bound result settlement, correct shared records, preservation of earlier schema behavior, and one connected explore → encounter → acquire → manage → craft/use → continue scenario with save/restore and deterministic replay. The full-suite current-source report includes the connected two-deposit case, result-5 cleanup/replay, remedy/result bands, mishap damage/replay, schema49 behavior, counted-lot conservation/replay and both Watch booking orders.

- [Current-source full C# 9 regression suite — PASS 1,318/1,318; 276 source hashes](full-suite-final/run-20261110T101919804Z-1df8af6c/results.json). The connected case is `recipe347_connected_exploration_encounter_cache_storage_crafting_two_deposits_and_continue`.
- [Current-source result-5 cleanup by untrained concurrent workers, with save/restore and deterministic replay — PASS 1/1](focused-final/run-20261110T110140654Z-863c34ba/results.json). Its changed-test hash matches the full-suite report. GPT noted that the earlier focused report has an old test-file hash; the full suite already reran the test successfully on final source.
- [Work Watch boundary in either booking order — PASS 1/1](focused/run-20261110T101738012Z-2e9c4c6f/results.json).
- [Current-source standalone C# 9 warnings-as-errors compile — PASS: Core, Persistence, LabModel; 201 source hashes](compile-final/compile-20261110T104543311Z-25993525/results.json).
- [Static package validation — PASS 18/18; 302 assets and 302 unique GUIDs](package-final/static-20261110T104603167Z-a4fca96f/results.json). This is structural validation, not Unity compilation.
- `git diff --check` passed on the source candidate before this documentation update.

### Reproduced failures and test correction

- [Before fix: result-5 cleanup rejects the capable untrained worker](reproductions/run-20261110T101149780Z-741dea70/results.json). This demonstrated the over-broad production gate; the current-source focused and full-suite reports above pass after its correction.
- [Before test correction: Watch interval did not reach the asserted hour-32 endpoint](reproductions/run-20261110T100125009Z-cafa80e0/results.json). The cause was the test pausing at 24h+1s, which correctly truncated future work. The test was changed to reach the boundary.
- [First boundary-test adjustment selected the recipe's earlier 15-minute phase interval](focused/run-20261110T101614397Z-b932748e/results.json). The corrected test selects the interval whose end equals the next job's start; the final boundary report passes.

The full suite's earlier attempt was stopped after compiling but before producing a report; it is incomplete and superseded by the current-source 1,318/1,318 result. Unity Editor import, Editor/Play Mode tests, player builds and observed player gameplay were not run. Schema18/49 behavior has versioned regression coverage, but this increment does not add authenticated pre-increment golden saves. The connected scenario is C# simulation acceptance, not a Unity presentation build.

## GPT acceptance and next mapped work

GPT accepted this exact bounded recipe-347 candidate in the [actual review record](GPT_REVIEW.md), closed both prior blockers and the evidence gap, and reported no remaining concrete acceptance blocker. It did not independently compile, execute gameplay tests, replay saves, or run Unity. Authenticated schema18/49 golden saves and stronger forged-snapshot coverage remain optional hardening. GPT recommends the existing MGT-05 “Harvesting, foraging, gathering and preservation” map row, beginning with source/API review of preservation/spoilage integration with physical inventory. The mapped row lists MGT-01, MGT-02 and RUL-01 as prerequisites. The map does not name a post-MGT-04 successor; this is GPT's selection from the existing map. This accepted recipe increment does not complete all of MGT-04 or the engine. See the [review request](GPT_REVIEW_REQUEST.md), [implementation trace](../../IMPLEMENTATION_TRACE.md), and [handoff](../../DEVELOPMENT_HANDOFF.md).
