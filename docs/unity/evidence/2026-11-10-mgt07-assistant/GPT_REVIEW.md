# MGT-07 implementation review and correction

The [Unity Rules Engine Development review](https://chatgpt.com/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c) held acceptance of `096173226781f15196ac2d2bfe009d474ac956c3` with evidence at `057471b903ee3bb68c4c8e7e8a8d50e722d5fdbd`. GPT traced the combat entry, tactical dispatch and turn advancement paths and found that the helper could remain booked in extraction while participating in tactical combat. The review preserved the accepted MGT-05A/B/C and MGT-06 dispositions and left the successor gate closed.

GPT found no other concrete behavior defect in the inspected scope. It read the 13 changed files, relevant combat code, all six test bodies and the retained evidence summaries. It did not reproduce the defect, execute tests or Unity, load saves, replay commands, or independently recompute hashes. It requested explicit historical schema43–49 coverage and separate forged assistant-binding and progress cases. It stated that the pending unfiltered regression and deferred Unity validation were independent of the hold.

Codex reproduced the defect with a normal `BeginFixedEncounter` command after 300 seconds of assisted work. The lead was outside the tactical roster, and the helper was in it. The command left the attempt `Working` with 300 seconds credited. [Before-fix report](combat-correction/reproduction/run-20261111T044453191Z-be526695/results.json)

The correction applies the existing tactical-participant eligibility restriction to the helper. The schema77 combat-entry path reconciles mining immediately after setting tactical control, before any tactical turn advances time. It truncates both bookings at the encounter boundary and preserves earned work and claims. The new case covers encounter entry, later combat time, start and resume rejections, and concurrent off-calendar solo extraction. The paired snapshot case also exercises forged progress and a canonical start receipt that omits the persisted assistant.

## Corrected implementation evidence

Correction commit [`5082abfd90d821baac2017a8a2c312c7b1473978`](https://github.com/BordelonDevOps/DecenniumDescent/commit/5082abfd90d821baac2017a8a2c312c7b1473978) changes `SharedMining.cs`, `SharedWorldCombatPolicy.cs`, and `MiningCases.cs`. The focused C# 9 warnings-as-errors suite passed **7/7**, including the exact tactical regression that failed before the fix. The historical and connected suite passed **30/30**. Both reports bind to the same 283 source hashes. Standalone C# 9 warnings-as-errors compilation passed for Core, Persistence and LabModel with 207 matching hashes. Package validation passed **18/18** with 309 assets and 309 unique GUIDs. The bindings match all 14 changed C# files to the corrected Git blobs and retain the assemblies and scenario saves. [Focused results](combat-correction/focused/run-20261111T044737856Z-6f6808f2/results.json) · [Historical and connected results](combat-correction/historical/run-20261111T044737894Z-44d765be/results.json) · [Compilation](combat-correction/compilation/compile-20261111T044604519Z-b5bf9d6d/results.json) · [Package](combat-correction/package/static-20261111T044811373Z-a7e2c1b3/results.json) · [Bindings](combat-correction/BINDINGS.json)

| Schema | Retained historical witness |
| --- | --- |
| 43 | `mining_partial_selection_commits_then_pauses_saves_resumes_and_receives_once` |
| 44 | `prospecting_pause_save_resume_and_repeat_prevention_preserve_shared_labor` |
| 45 | `mining_assay_uses_shared_work_save_resume_and_only_authored_findings` |
| 46 | `mining_destructive_assay_consumes_one_authored_portion_at_first_work_and_resumes_from_save` |
| 47 | `expedition_assignment_travels_to_mine_and_dispatches_shared_extraction` and `connected_exploration_combat_and_assigned_mining_share_one_saved_timeline` |
| 48 | `mineral_preparation_conserves_measured_mass_and_resumes_after_save` |
| 49 | `recipe347_mining_tool_applies_check_reserve_and_integrated_dressing_through_shared_extraction` |

The initial unfiltered suite recorded 1,340 passing cases, but it computed hashes after the correction began. Three hashes refer to the later working files while the loaded assemblies still contained the original candidate. That run is excluded from exact-source acceptance evidence. The corrected unfiltered run passed **1,341/1,341**. All 283 hashes match the corrected focused report, and the run includes the extraction, connected exploration/combat/mining, and connected exploration/encounter/storage/crafting/continue cases. This run completed after GPT's acceptance. [Corrected full results](combat-correction/validation/run-20261111T044738526Z-be2248da/results.json)

## Actual GPT disposition

[Unity Rules Engine Development](https://chatgpt.com/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c) accepted correction commit `5082abfd90d821baac2017a8a2c312c7b1473978` with evidence commit `f17ec17897f58dcb228ca35be226b61e48bb9359`. It closed the tactical-entry blocker and the historical and forged-state coverage gaps. GPT found no remaining concrete blocker in the bounded schema77 `TEST_ONLY` direct-extraction contract. It accepted the exact focused, historical/connected, compilation, and static package evidence and excluded the initial unfiltered run. The corrected unfiltered run and Unity execution were outside its acceptance basis.

GPT inspected the complete correction diff, both changed tests, the before-fix and corrected reports, all 30 historical results, the source/API contract, current handoff, map, and dependency order. It cross-checked the two runtime files' listed hashes against the bindings and the focused, historical and compilation reports. It did not independently hash all files, run tests or compile C#, load binary saves, replay commands, or run Unity.

GPT identified MGT-08 Farming and agricultural companion work as the next mapped review area, with prerequisites MGT-01 and MGT-02. Codex checked that dependency order against the implementation map and agrees. MGT-08 begins at [source/API review](../2026-11-10-mgt08-camp-greens/SOURCE_API_REVIEW.md). Existing MGT-05A/B/C and MGT-06 acceptances stand.
