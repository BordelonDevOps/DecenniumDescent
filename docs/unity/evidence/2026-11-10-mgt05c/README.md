# MGT-05C implementation review packet

**Current state: corrected implementation committed and pushed; GPT re-review pending.** MGT-05C is not accepted yet, and no successor module has started. The original schema76 implementation is code commit [`27dea8d0343b385539b8703255064301974c6e27`](https://github.com/BordelonDevOps/DecenniumDescent/commit/27dea8d0343b385539b8703255064301974c6e27). The focused correction is [`4b88ed7b2876e69dee3d104fc9745b3eba0829ae`](https://github.com/BordelonDevOps/DecenniumDescent/commit/4b88ed7b2876e69dee3d104fc9745b3eba0829ae), changing `HarvestPreservationRecords.cs` and `HarvestPreservationTreatmentCases.cs`. The original 14-file change is preserved in [MGT05C_IMPLEMENTATION.patch](MGT05C_IMPLEMENTATION.patch), SHA-256 `31542e1b05224a88edf6865f1334ed86d6f69f3e08adf5e36da040df30733dd3`. The correction-only diff is [MGT05C_CORRECTION.patch](MGT05C_CORRECTION.patch), SHA-256 `b4e74ee02279623caac317305beF2d294b9ab17b557a0f8cd5787ad5e0336f89`; reverse application against the corrected checkout passes.

## Responsibility and authority

This bounded schema76 `TEST_ONLY` increment covers controlled clean opening, one evidenced in-vessel portion, physical retrieval ending that portion’s future protection, and three typed fixture exposure events. Its source requirements and adopted interpretation are in [MGT05C_RULE_DECISIONS.md](MGT05C_RULE_DECISIONS.md), based on the pinned “Preservation and spoilage” source at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

The implementation reuses successful treatment history, harvest origin, shared `RuleClock`, `PortableHandlingRecord`, `PortableEquipmentRecord`, inventory ancestry and `WorkLedger`, command receipts and revisions, and the existing snapshot codec. It adds append-only schema76 evidence only. It stores no second age, location, quantity, mutable protection flag, or clock. Schemas74 and75 retain their existing codec branches and historical meaning. This remains an authored TEST_ONLY fish/vessel/tool/exposure profile, not production environmental simulation.

## GPT implementation review and correction

GPT reviewed the initial implementation and identified a concrete lineage defect. A later legal descendant of the evidenced in-vessel portion stopped receiving the already-earned protection interval when queried; the portion itself remained correct. GPT requested that the interval be carried through the descendant’s ancestry up to the first later split, while keeping that descendant unprotected after retrieval. It also requested a save/restore/replay regression and explicit evidence for actor-only exposure rejection, exact command retry after restore, and conflicting payload rejection. The actual review and its limits are recorded in [GPT_IMPLEMENTATION_REVIEW.md](GPT_IMPLEMENTATION_REVIEW.md).

The corrected derivation locates the evidenced child in the queried lot’s lineage and bounds its continuation interval at the first later descendant creation and at the child’s `ProtectionEnd`. It does not reactivate protection after retrieval. The regression spends time in-vessel, retrieves the child, subdivides it while unprotected, and checks equal derived age at the split, unchanged origin/freshness/mass, save/restore and replay. Exposure regressions now check authority rejection, exact post-restore retry idempotency, and conflicting command-ID payload rejection.

The defect was reproduced before the fix. The pre-fix MGT-05C connected case compiled but failed at the new assertion that a descendant of a removed portion must retain earned protected time without regaining active protection: [pre-fix reproduction report](validation/attempt-results/gpt-correction-before/run-20261110T234914655Z-3022b330/results.json). The corrected case passes: [post-fix report](validation/attempt-results/gpt-correction-after/run-20261110T235018773Z-d9c08a3d/results.json).

## Focused acceptance evidence

Eight focused cases pass after the correction. Each report compiled Core, Persistence, LabModel and HeadlessTests with C# 9 warnings as errors and contains the same 283 C# source hashes. The sorted source/hash set digest is `9580902fdfa371a9a7f591c0c888a95c33c984b850e1ee87a427c5cb197372a4`. The detailed report paths and compiled assembly hashes are in [BINDINGS.json](validation/BINDINGS.json); the four representative DLLs are retained in [validation/assemblies](validation/assemblies/).

| Case | Result | Retained report |
| --- | --- | --- |
| MGT-05A harvest preservation, work deadline, save/restore and replay | PASS 1/1 | [results](validation/attempt-results/gpt-correction-focused/run-20261110T235220450Z-f44b8ec2/results.json) |
| MGT-05B closed-vessel treatment, lineage, save/restore and replay | PASS 1/1 | [results](validation/attempt-results/gpt-correction-focused/run-20261110T235304410Z-fd3ffe6c/results.json) |
| MGT-05B failed treatment spends supply once without protection | PASS 1/1 | [results](validation/attempt-results/gpt-correction-focused/run-20261110T235424075Z-989d1f9f/results.json) |
| MGT-05B degraded treatment and spoilage deadlines | PASS 1/1 | [results](validation/attempt-results/gpt-correction-focused/run-20261110T235455262Z-03ddc902/results.json) |
| MGT-05B lineage cutoff, save/restore and replay | PASS 1/1 | [results](validation/attempt-results/gpt-correction-focused/run-20261110T235523124Z-b0bf2323/results.json) |
| MGT-05B closed-vessel handover, custody, ownership and replay | PASS 1/1 | [results](validation/attempt-results/gpt-correction-focused/run-20261110T235557054Z-f15b1fe2/results.json) |
| MGT-05C controlled opening, in-vessel portion, retrieval cutoff, later unprotected descendant, save/restore and replay | PASS 1/1 | [results](validation/attempt-results/gpt-correction-after/run-20261110T235018773Z-d9c08a3d/results.json) |
| MGT-05C deadline and exposure authority, duplicate, retry and conflict boundaries | PASS 1/1 | [results](validation/attempt-results/gpt-correction-focused/run-20261110T235630800Z-75597948/results.json) |

Static package validation passes **18/18** checks across **309 assets**, **309 unique GUIDs** and **607 file hashes**. The report is [validation/package/results.json](validation/package/results.json). It is structural package validation, not Unity import or compilation.

### Retained non-passing attempts

- The pre-fix failure above is the intentional reproduction of GPT’s concrete defect; it passed compilation and failed the regression before the correction.
- One runner-selection invocation used a stale MGT-05B case name and failed before executing a case: [runner-selection report](validation/attempt-results/gpt-correction-focused/run-20261110T235331587Z-c8d25450/results.json). The actual current case name was then run and passed in the table above. This is a runner selection error, not a gameplay failure.
- The full all-cases suite was not run on the corrected source. Unity import/compilation, Editor Edit Mode, Play Mode, player build, scenes and observed gameplay were not run; Unity remains deferred.

## Code excerpts and limits

- The continuation interval is derived from the evidenced child’s lineage and first later split in [`HarvestPreservationRules.UnprotectedAgeAt`](https://github.com/BordelonDevOps/DecenniumDescent/blob/4b88ed7b2876e69dee3d104fc9745b3eba0829ae/engine/com.decennium.foundation/Runtime/Core/HarvestPreservationRecords.cs#L329).
- The save/restore, in-vessel elapsed-time, retrieval and later-subdivision regression is in [`HarvestPreservationTreatmentCases.cs`](https://github.com/BordelonDevOps/DecenniumDescent/blob/4b88ed7b2876e69dee3d104fc9745b3eba0829ae/engine/com.decennium.foundation/Tests/EditMode/HarvestPreservationTreatmentCases.cs#L502).
- Actor-only exposure rejection is asserted at [the host-authority boundary](https://github.com/BordelonDevOps/DecenniumDescent/blob/4b88ed7b2876e69dee3d104fc9745b3eba0829ae/engine/com.decennium.foundation/Tests/EditMode/HarvestPreservationTreatmentCases.cs#L650).
- Exposure retry and conflicting command-ID assertions are in the same test file [here](https://github.com/BordelonDevOps/DecenniumDescent/blob/4b88ed7b2876e69dee3d104fc9745b3eba0829ae/engine/com.decennium.foundation/Tests/EditMode/HarvestPreservationTreatmentCases.cs#L663).

Supported saves retain schema74 and schema75 behavior. The bounded slice still does not implement other foods/materials, generalized repackaging, recursive protected subdivision, re-treatment, production recipes, or broad environmental causes. GPT has not yet reviewed the corrected code/evidence, so MGT-05C acceptance and any successor step remain pending.
