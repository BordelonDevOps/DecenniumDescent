# MGT-07 extraction assistance implementation review

The schema77 `TEST_ONLY` extraction-assistance candidate is committed on `Engine` at [096173226781f15196ac2d2bfe009d474ac956c3](https://github.com/BordelonDevOps/DecenniumDescent/commit/096173226781f15196ac2d2bfe009d474ac956c3). GPT approved the [source/API contract](SOURCE_API_REVIEW.md). Implementation acceptance is pending.

The direct exposed-node extraction command optionally selects one fixed trained assistant. The shared work ledger books matching intervals under one job, reserves the finite selection once, and credits one interval of joint work. Losing either worker's eligibility pauses the pair. Resuming the unfinished job requires trusted authority over the same workers. Full joint labor supplies exactly +1 on the existing lead check with its original dice, proficiency, injury and tool handling. `MiningAttemptRecord` persists the assistant and settled bonus, and history binds that identity to the start command. The solo fingerprint remains `mining-selection-v1`. Assisted selections use `mining-selection-v2`. Assisted expedition assignments are rejected before history can be written.

The standalone mining profile leaves unrelated schema71 storage, schema67 Pressure and schema74–76 preservation collections empty. Their historical profile checks still apply in their original schemas. To give the default scenario a physically reachable assistant, the fixture places the declared helper on a free cardinal neighbor of its first deposit during initialization. Runtime access is assessed against the selected deposit and current shared actor state. The explicit fixture training rank supports both proficiency and expertise for regression coverage. The magic witness places a physically eligible helper-owned Mining Tool at a second authored deposit because the existing candidate binding requires the tool and deposit owner to match.

The pinned source hashes were recomputed from Git revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4` and match the source/API record. [Mining guide](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/MINING_CANDIDATE_GUIDE.md) · [Gathering guide](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md)

## Focused acceptance

| Case suffix after `mgt07_extraction_assistant_` | Witness |
| --- | --- |
| `full_task_bonus_save_restore_replay` | Real exposed stock and receiver, paired duration and one progress total, mid-work disk save and restore, positive paused gap, same-pair resume, solo control, one-point modifier, identical RNG and replay bytes, exact finite physical settlement, idempotent retry. |
| `team_pause_resume_and_interruption` | Authored Stunned event at 300 seconds interrupts the assistant, truncates both bookings and retains both finite claims. Resume rejects during incapacity and succeeds after expiration. |
| `rejects_invalid_training_authority_and_overlap` | Admission and execution agree for self, unknown, untrained, unauthorized, moving and out-of-reach participants. A detached policy-level ledger fixture checks future overlap; the scenario has no ordinary command for booking an unattributed future job. |
| `preserves_lead_rules_and_blocks_magic_transfer` | Rank 1 and rank 2 supply exactly one point each with the untrained lead's existing disadvantage and zero proficiency contribution. The helper's physically eligible tool does not participate in the lead's extraction. |
| `once_only_check_and_finite_settlement` | A failed assisted check consumes one normal draw, releases exactly the selected claims, preserves the exact receipt on restore, and rejects a conflicting command ID. |
| `schema_history_and_team_validation` | Rejects a nested assisted assignment and missing or mismatched helper labor, and checks the original schema43 solo request and snapshot. The full suite carries the broader historical schema coverage. |

## Retained evidence

- The C# 9 warnings-as-errors focused suite passed **6/6** with 283 source hashes. This run used the existing `Test-Foundation.ps1` compilation and case runner with a name filter for `mgt07_extraction_assistant_*`. [Results](development-attempts/focused/run-20261111T042255704Z-1f588786/results.json)
- Standalone Core, Persistence and LabModel C# 9 compilation passed with 207 source hashes. Static package validation passed **18/18** with 309 assets and 309 unique GUIDs. [Compilation](compilation/compile-20261111T042256292Z-f747406e/results.json) · [Package validation](package/static-20261111T042256453Z-d8df1fe9/results.json)
- All 13 changed C# source hashes match the exact committed Git blobs. All 207 overlapping focused and standalone compilation hashes match. The manifest indexes the compiled assemblies, reports and both connected-scenario saves. [Bindings](BINDINGS.json)
- The unfiltered regression suite is running against the same implementation revision. The full-suite verdict will be added when the report is available. Unity execution remains deferred.

Prospecting and assay assistance, assisted standalone preparation, assisted expedition assignment, changes to team membership, hiring, production geology and Unity integration remain open or deferred. This packet covers the bounded extraction-assistance contract.
