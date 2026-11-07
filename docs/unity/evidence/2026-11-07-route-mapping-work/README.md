# Schema59 Map Route work evidence

This packet records one bounded, TEST_ONLY stationary Map Route work/check increment on branch `Engine`. It is a C# simulation procedure over shared state; it is not release content or a claim that the rules engine is complete.

## Source and policy boundary

The pinned authority is EX58 Player Book FL-02/03/10 at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, SHA-256 `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`, together with `GAMEPLAY_LOOP_CANON.md` §2 and `CORE_RESOLUTION_PLAYTEST.md`. Their generic expedition task and Mapping rules do not fully specify ordinary Map Route's method, check skill, work location, failure/retry cost, or the precise use of 480 active work minutes. Those choices are explicitly recorded as prototype policy in [ROUTE_MAPPING_WORK_RULE_DECISIONS.md](../../ROUTE_MAPPING_WORK_RULE_DECISIONS.md). FL-11 Forced March's +6 is not imported.

Schema59 adds immutable work-attempt and completion-check records. Work intervals reserve every participant in the shared `WorkLedger`, advance only through the common `RuleClock`, and use the existing task-check and deterministic RNG path. Mapping results enter the existing append-only route knowledge ledger. A stationary mapping result changes knowledge but does not establish passage feasibility: an Unknown route remains blocked. Work binds to one route but does not prevent unrelated travelers from using it.

## Runnable acceptance

- `route_mapping_work_uses_reserved_team_time_rng_and_persists`: pure query and command-cost behavior; untrained lead plus trained assistant; invalid assistance; reservation exclusion; pause, save/restore and exact resume; deterministic completion; Mapping accounting; Unknown-route rejection; and canonical replay.
- `route_mapping_work_applies_poisoned_disadvantage_and_persists_both_dice` and `route_mapping_work_uses_post_boundary_condition_state_at_completion`: a Poisoned lead selects disadvantage and persists both dice; Poisoned expiring exactly at the work endpoint is absent for the check.
- `route_mapping_work_check_uses_condition_history_at_its_causal_point`: applies Poisoned after a normal check at the same shared-clock timestamp and verifies the earlier check survives validation, save/restore and canonical replay. This regression reproduces a timestamp-only validation defect and confirms the saved condition-history prefix correction.
- `route_mapping_work_synchronous_handling_cannot_cross_fractional_completion`: one-second inventory handling is rejected half a second before the task endpoint; a half-second shared-clock advance resolves the check at the exact fractional timestamp.
- `failed_route_mapping_retry_requires_a_fresh_480_minutes`: immutable failure, zero-progress retry and completion only after a new full 28,800 active seconds.
- `route_mapping_work_does_not_stop_an_unrelated_route_traveler`: concurrent route travel and stationary route work against one authored route.

## Validation

- [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json): `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` — **PASS, 1,225/1,225**, C# 9 warnings as errors. Includes the Poisoned, post-boundary, causal-history, negative-prefix, exact fractional completion, retry and concurrent route/travel cases.
- [FOCUSED_WORK_RESULT.json](FOCUSED_WORK_RESULT.json): `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1 -CaseName route_mapping_work_uses_reserved_team_time_rng_and_persists` — **PASS, 1/1** against the final implementation.
- [FOCUSED_BOUNDARY_RESULT.json](FOCUSED_BOUNDARY_RESULT.json): `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1 -CaseName route_mapping_work_synchronous_handling_cannot_cross_fractional_completion` — **PASS, 1/1** against the final implementation.
- [FOCUSED_CAUSAL_HISTORY_RESULT.json](FOCUSED_CAUSAL_HISTORY_RESULT.json): `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1 -CaseName route_mapping_work_check_uses_condition_history_at_its_causal_point` — **PASS, 1/1** against the final implementation.
- [FOCUSED_NEGATIVE_PREFIX_RESULT.json](FOCUSED_NEGATIVE_PREFIX_RESULT.json): `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1 -CaseName route_mapping_work_check_rejects_negative_condition_prefix` — **PASS, 1/1**. The record constructor and state validator reject a negative prefix count.
- [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json): `pwsh -NoProfile -File engine/tools/Validate-Package.ps1` — **PASS, 18/18** static checks; 265 package assets and 265 unique GUIDs.

These checks use the headless C# regression harness and package-structure validator. They do not attest to release behavior. [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) records the branch base, pinned source revisions, tested implementation hashes and report hashes.

## Independent design review

GPT agreed with the bounded proposal before implementation and reviewed the first implementation packet with no confirmed blocker. It then identified a timestamp-only condition-history validation risk. A same-timestamp post-check Poisoned regression reproduced it as `InvalidResult`; schema59 now stores the exact condition-journal operation count at check resolution. The regression passes through save/restore/replay. GPT's follow-up review found no concrete blocker under the current append-only journal model and highlighted explicit bounds checking and canonical replay as the relevant validation guarantees. The record constructor already rejected negative counts; schema59 state validation now also checks the lower bound explicitly, with a dedicated regression. GPT reviewed supplied excerpts and Codex-reported results; it did not inspect the checkout or run local checks.

GPT noted that the new field changes the in-development schema59 binary layout. The pre-correction schema59 layout is not a supported save contract; schemas through 58 retain their existing branches. Future condition-journal compaction must preserve or migrate the saved prefix reference. Review details are recorded in [GPT_REVIEW.md](GPT_REVIEW.md).
