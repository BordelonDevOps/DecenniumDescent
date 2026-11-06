# Schema49 recipe-347 mining-tool integration

Schema49 composes one actual recipe-347 Mining Tool candidate with the existing finite mining extraction. This is a source-bound **TEST_ONLY** implementation, not a release approval or a general gathering-tool system.

## Source and adopted completion

The governing checkout is pinned to source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Exact Git blob IDs, SHA-256 values and source snapshots are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) and [sources](sources/).

The recipe card supplies +2 to Mining checks, one predeclared ordinary reserve only on Critical Success, and preparation of one eligible recovered ordinary unit up to 1 lb as part of the same extraction. The card/body source and shared tool guide also constrain the actual lead's direct participation, complete equipment body, physical access, structural HP, suppression/melding state, support, capacity and result-time eligibility.

The source does not assign the preparation interval inside a staged partial extraction or define whether its physical split waits for the extraction roll. Codex and Unity Rules Engine Development completed those operational boundaries under the owner's standing authorization to use their consensus:

- Preparation occupies the final 600 feasible active seconds of the extraction's removal stage. It does not add to or reduce the existing full duration or stage plan. A task with less than 600 removal seconds does not prepare a unit.
- The physical split commits on the 600th feasible second before the later extraction check. Before that boundary there are no child lots or inferred partial waste. At completion the parent amount becomes zero and measured retained and gangue children exactly equal the original mass.
- Successful eligible extraction receives only the retained child as dressed material. Ordinary failure awards nothing; if the prepared unit is its failure victim, the unit is ruined but both physical descendants remain at ground. Critical Failure also preserves a completed split. Pause/save/restore/resume keep work and claims.
- The reserve is a separate, explicitly named actual unit, reserved through `WorkLedger`. It is excluded from baseline selection and forfeiture and is received only for a qualifying Critical Success. Otherwise the claim is released.

These completions are identified as provisional operational decisions in [MINING_RULE_DECISIONS.md](../../MINING_RULE_DECISIONS.md); they are not presented as verbatim source rules.

## Responsibilities and authoritative records

| Concern | Authority |
| --- | --- |
| Recipe-347 card/body facts and fixed effect identity | `MiningToolCandidateProfileRecord` with source identity in `MiningToolContentBinding` |
| Current candidate item, custody, placement, mass and receiver relationship | Existing `PortableEquipmentRecord` and `ObjectStructureRecord` |
| Missing primary/optional members, suppression and melding | `MiningToolInstanceStateRecord` (explicit TEST_ONLY state; no dynamic lifecycle command yet) |
| Mining lead, selection, stage schedule, check and outcome | Existing `MiningAttemptRecord` |
| Candidate participation, prepared target, reserve and effect audit | One `MiningToolUseRecord` linked to the attempt |
| Active work, exact intervals and target/reserve claims | Existing `WorkLedger` |
| Retained/gangue ancestry, mass and ground/receiver custody | Existing `InventoryLotRecord`, `ResourceLot`, `PortableEquipmentRecord` and `OrdinaryInventory.Descendant` |
| Clock, RNG, command authorization, rollback, receipts and replay | Existing shared `Snapshot`/simulation pipeline |
| Durable representation | `MiningToolCodec` appended after schema48 through `SnapshotCodec` schema49 |

The shared pure eligibility rule is `MiningToolCandidateRules`; assessment, result resolution and snapshot validation use it. Ordinary mining tools and pick remain separate required equipment. The candidate tool cannot replace them, grant proficiency, authorize manufacturing/acquisition, improve prospecting/assay, or grant any unprinted effect.

## Runnable acceptance and validation

| Check | Result |
| --- | --- |
| `recipe347_mining_tool_applies_check_reserve_and_integrated_dressing_through_shared_extraction` | **PASS — 1/1** |
| `recipe347_failed_extraction_preserves_unawarded_prepared_mass_and_releases_reserve` | **PASS — 1/1** |
| `recipe347_ineligible_candidate_has_no_effect_and_falls_back_to_base_mining` | **PASS — 1/1** |
| `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` | **PASS — 1,163/1,163**, C# 9 warnings as errors |
| `pwsh -NoProfile -File engine/tools/Validate-Package.ps1` | **PASS — 18 checks, 225 assets, 225 unique GUIDs** |

The Critical Success case selects an intact 0.5 lb preparation target and a distinct 0.5 lb damaged baseline while a separate 0.5 lb reserve remains unselected. It saves halfway through preparation, completes the 0.4 lb retained/0.1 lb gangue split exactly at the removal boundary, applies the +2 check, receives one reserve and recovers the damaged baseline. It verifies unchanged 2,400-second extraction timing, mass conservation, custody, exact save/restore and duplicate-command idempotency. The ordinary-failure case confirms no award and preserves the already-completed descendants at ground. The ineligible cases cover a missing primary member, broken structure, suppression, melding, inaccessible placement and missing item; base extraction still resolves without candidate effects.

Final per-case reports and complete source hashes are [FOCUSED_CRITICAL_SUCCESS.json](FOCUSED_CRITICAL_SUCCESS.json), [FOCUSED_FAILURE.json](FOCUSED_FAILURE.json), [FOCUSED_INELIGIBLE.json](FOCUSED_INELIGIBLE.json), [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json) and [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). `SOURCE_BINDINGS_VALIDATION.json` compares source snapshots with the pinned Git blobs and records implementation/report hash checks.

## Scope left open

This is one exact recipe and one pre-authored physical instance. Candidate state is explicit in snapshots, but this increment adds no command for losing/restoring tool members or changing suppression/melding dynamically. General recipe/family candidate registration, multiple candidates, a reusable tool acquisition/crafting path, portions, arbitrary item-on-surface geometry, additional mining recipes, production content, full source parity and release qualification remain outside this acceptance. The engine as a whole is not complete.

The schema49 code and evidence were later committed in `31eefbe7` and pushed to `Engine`. The retained packet is a review artifact; no GPT review of this source batch is recorded.
