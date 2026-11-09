# GPT implementation review — MGT-01 schema71

## Initial review of commit `bb4832e23b26a3f71b41bc14be627e22c390ad17`

**Verdict:** held. GPT found two concrete portable-handling defects and one historical-save evidence gap. It found the independent capacity calculations, source-qualified Load fallback, immutable profile definitions, installation-derived camp capacity and additive codec arrangement otherwise matched the inspected contract. It found no schema70 wire-layout change. Broader catalog coverage and additional adversarial nesting tests were optional.

### GPT’s actual response

> Hold acceptance on `bb4832e23b26a3f71b41bc14be627e22c390ad17`. I found two concrete handling defects in the inspected code.
>
> 1. The ordinary portable crate cannot be picked up or handed over. `PortableStorage.cs` required its initial actor custodian, Ground placement and original coordinates permanently. Ordinary pickup passed the portable assessment, but the resulting state failed the fixture validator with `PortableStorageCrateFixtureMismatch`, surfaced as `InvalidResult`. Query assessment did not run that final validator and could advertise the operation as admissible.
>
>    Smallest fix: separate immutable crate identity/mass/capacity facts from mutable placement and custody. Permit coherent movement through existing handling authority. Add pickup → handover → save/restore → drop coverage, preserving contents, ownership and burden, with query/execution agreement.
>
> 2. Opening or closing an adjacent ground container changes its coordinates. `SharedPortableEquipment.cs` assigned the acting character’s coordinates whenever the resulting placement was Ground—including stationary Open/Close. In the scenario, the companion at `(2,3)` could reach installed storage at `(1,3)`. Opening or closing attempted to relocate it to `(2,3)`, violating the installation placement validator. The test opened it through the hero standing at its original cell, masking this defect.
>
>    Smallest fix: preserve coordinates for stationary Open/Close in schema71, in both projected and committed transitions, while preserving historical-profile behavior. Test adjacent companion opening/closing; assert unchanged root position, installation claims, contents and synchronized lot locations.
>
> The historical-save evidence also needs clarification. The current test constructed a fresh schema70 initial state. That demonstrates current legacy-profile roundtrip, not an authentic pre-change save continuation. Supply retained pre-change schema70 bytes and current decode/encode/restore/continuation results, or identify existing evidence that does so.
>
> I inspected the substantive diff, relevant handling/validation/transaction and codec paths, connected test, pinned source clauses and matching blob identities, contract, trace/handoff, and retained passing/failing reports. Recorded hashes agreed across the full, focused, compile and package reports where they overlapped. Those reports showed `1,299/1,299`, standalone compilation PASS and `18/18` package checks. I did not independently compile, run tests, decode/replay saves, recompute source hashes or run Unity. I made no repository changes.
>
> Keep Codex on these corrections and the historical evidence requirement. This module is not yet accepted; no successor is selected in this review.

The review was returned in [Unity Rules Engine Development](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206). The exact source lines and acceptance implications are preserved in that chat and the commit links above.

## Codex correction and re-review packet

Codex changed the TEST_ONLY crate validator to preserve its fixed identity, owner, profile, mass and capacity while accepting Ground/Carried placement and either selected actor as custodian. The existing shared handler still owns movement and custody/link transitions. Schema71 stationary Open/Close now preserve ground coordinates in both query projection and committed state; historical profile behavior is unchanged. The connected test now exercises adjacent companion Open/Close, crate pickup/handover/save/restore/drop with query agreement and burden/ownership checks, and current-code continuation from the authentic paused schema70 save embedded from the retained pre-storage file.

The original schema70 bytes are retained at [the MGT-01 fixture path](fixtures/schema70-pre-mgt01-paused-camp-construction.ddsave). They came from the pre-storage Engine tree, blob `fd8b7d94d9061736dd40f760a4356d4828836e7e`, SHA-256 `5ef2f86460fd7af4daf8faf0d4651ec85bf6ca102e1b22081862dd748bc71214`. The test pins the bytes’ SHA-256, re-encodes them exactly, restores them under the current schema70 policy, and resumes/completes construction in two byte-identical branches. Source and result saves are linked from [the evidence README](README.md).

Codex validation for the corrected candidate: focused connected MGT-01 case PASS 1/1; full C# 9 warnings-as-errors suite PASS 1,299/1,299 (271 source hashes); standalone Core/Persistence/LabModel compilation PASS (197 source hashes); static package checks PASS 18/18 (297 assets/GUIDs); `git diff --check` PASS. Exact current reports: `final/review-fixes-final/focused/run-20261109T223329806Z-0dae20d5/results.json`, `final/review-fixes-final/full-suite/run-20261109T223711542Z-34c7ff34/results.json`, `final/review-fixes-final/assemblies/compile-20261109T224234881Z-36564b63/results.json` and `final/review-fixes-final/package/static-20261109T224254550Z-09ee053e/results.json`. The first correction attempts also exposed and fixed a nullable burden assertion compile error and a test sequencing error (`OffCalendarActionAlreadySpent`); reports are retained and summarized in the README. No Unity import, Editor tests, Play Mode or game build were run.

**Status:** the corrected exact commit has not yet been sent for GPT re-review. MGT-01 remains held, and no successor module may begin until the second actual review resolves concrete blockers and agrees acceptance.
