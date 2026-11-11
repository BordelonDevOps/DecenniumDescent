# GPT implementation review: MGT-05C

**Review target:** initial MGT-05C implementation code commit `27dea8d0343b385539b8703255064301974c6e27`, with evidence/docs commit `2da15f7546cdb91abf530db9dbdf6ffc4e2dddb0`.

**First review result:** GPT did not accept the initial implementation. It found one concrete lineage defect and requested targeted evidence. MGT-05A and MGT-05B acceptance and the MGT-05C source/API contract approval remained settled.

## Findings from GPT

1. `HarvestPreservationRules.UnprotectedAgeAt` extended the in-vessel interval only when the queried lot ID exactly equaled the evidenced `ChildLotId`. A later legal descendant of a removed, now-unprotected portion therefore lost previously earned protected time, causing its derived unprotected age to jump at subdivision.
2. GPT requested a regression that treats, opens, splits in-vessel, spends time protected, retrieves the portion, then subdivides the now-unprotected carried portion. The parent and grandchild must have equal age at the same instant, remain unprotected, preserve mass and origin, and behave identically after save/restore and replay.
3. GPT requested explicit witness cases for actor-only exposure authority denial with unchanged state; exact original exposure-command retry after restore returning `Duplicate` without state/clock/RNG changes; and rejection of a conflicting payload using the same command ID without state changes.
4. GPT required rerunning the existing schema74 `mgt05a_harvest_mass_preservation_work_deadline_save_restore_and_replay` case against the corrected source.

The smallest requested code change was to find the evidenced portion child in the queried lot’s ancestry, include the continuation interval through that child’s protection end, and stop at the first descendant created below it. The descendant remains unprotected after retrieval. The source/API contract did not change; GPT found no reason to reopen the approved MGT-05C scope or select a different dependency.

## Correction and retained results

The correction was implemented and pushed at code commit `4b88ed7b2876e69dee3d104fc9745b3eba0829ae`. It modifies only `HarvestPreservationRecords.cs` and `HarvestPreservationTreatmentCases.cs`. The defect was reproduced before the fix; the new connected regression failed at the expected earned-time assertion. After the fix, the MGT-05A schema74 regression, all five targeted MGT-05B compatibility cases, and both MGT-05C cases pass as eight separate runs. Every passing report binds to the same 283 source hashes and source/hash-set digest `9580902fdfa371a9a7f591c0c888a95c33c984b850e1ee87a427c5cb197372a4`. Static package validation passes 18/18 checks. The exact reports, code diffs, source excerpts and artifact hashes are in [the updated review packet](README.md) and [BINDINGS.json](validation/BINDINGS.json).

## GPT correction review and acceptance

GPT re-reviewed the exact corrected code commit `4b88ed7b2876e69dee3d104fc9745b3eba0829ae` and evidence/docs commit `c4c4342149ce16efffcaaa9872759e9b17c59adf` in the [Draft MGT05 API Contract conversation](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af2fe69-dcf8-83ea-a491-59512e8f5e51). It explicitly accepted the bounded schema76 TEST_ONLY MGT-05C implementation and stated that no concrete blocker remains within scope. GPT confirmed the correction carries earned protection through later descendants while retrieval still ends future protection, and that the exact lineage regression, exposure authority/retry checks, schema74 continuation run, five MGT-05B regressions, and package results close the prior findings. GPT said the next mapped gameplay dependency may now follow. No disagreement remains on MGT-05C.

This was source-and-retained-evidence acceptance. GPT inspected the correction patch, corrected source/test bodies, packet, bindings, all eight result records, pre-fix failure and static package report, but did not compile or execute C#, run tests, or load saved snapshots through the engine. It independently cross-checked the two corrected source-file hash entries between the connected case and package reports, but did not recompute the full 283-file source set digest, patch SHA-256, or compiled-assembly hashes. These limits do not block the bounded acceptance. A full all-cases rerun and broader randomized/forged-snapshot checks remain optional hardening; Unity was not touched.

## Review limits

The eight C# 9 warnings-as-errors focused runs and static package validation are Codex-run and retained, not GPT-run. The README and [BINDINGS.json](validation/BINDINGS.json) enumerate exact report paths, 283 source hashes, the source-set digest, correction patch digest, and four DLL digests.

**Conversation:** [Draft MGT05 API Contract](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af2fe69-dcf8-83ea-a491-59512e8f5e51).
