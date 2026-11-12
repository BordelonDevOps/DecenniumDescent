# INT-03 scoped session evidence

Implementation `3c7b13728d13bfddbf47976220cd867652d4762d` is the local C# session and PowerShell console on `Engine`. The C# implementation lives in the TEST_ONLY laboratory assembly, using the ordinary selected recipe-4 fingerprint `TEST_ONLY.recipe4-batch-v1-8e3fd0fe4005207e90bffc01cd900efddcfd6e976e7aab4b46000d64d50c4d01`. The only test inventory change is the added scoped session case. [Approved contract](../2026-11-12-int03-playability/GPT_REVIEW.md) · [Session instructions](README.md)

The session holds the four grants privately. The exact Haven sale and meal inputs use a transaction-specific companion and buyer inventory grant. The resolver still checks the authored offer, mandate and assets. The buyer inventory grant is unavailable to arbitrary handling commands or to either opponent. The public C# boundary gives the embedding local host the responsibility to bind requests to seats and control file access.

## Connected play and persistence

The C# and console walks both start from the real initial profile and commit 165 inputs. The player contributes 90 receipts, the first-opponent director 4, the trusted calendar and closure adapter 47, and the automatic later defender 24. The party closes its first encounter, mines and retrieves the ore, receives two historical copper from the Haven sale, provisions and closes the expedition, and completes the charter return. The companion preserves the selected specimen, researches the formula and completes the actual recipe-4 batch. The manufacturing roll is 15 and the result is Exceptional, with six doses. The player owns the quality choice at revision 106. [Command inputs](walkthrough.jsonl) · [C# timeline](connected/timeline.json) · [Console transcript](console/responses.jsonl)

The later movement interrupts at revision 113 with a pending opportunity for the automatic defender. The player sees the responsible seat, and neither human seat receives the defender token or can answer in its place. The actual defender response commits after file restore. A subsequent dose raises the hero from 23 to 26 HP. The final ordinary travel commit follows the second legal encounter closure, at revision 165 and clock `113415/2`. The resumed route and console reach the same canonical bytes as the uninterrupted C# session. [Pending save](connected/saves/checkpoint-113.ddsave) · [Continued save](connected/saves/checkpoint-165.ddsave) · [Restored continuation](connected/saves/restored-165.ddsave)

The focused C# case exercises scoped views and grants, hidden versus absent target denials, wrong-seat delivery, stale and conflicting inputs, duplicate delivery, revocation, and delivery after recovery, failed external restore and explicit backup recovery. The walkthrough additionally rejects an encodable false RNG history before replacing the live predecessor. It restores and re-encodes an authentic ordinary MGT-04 wire95 predecessor byte-for-byte. Replaying the already committed sale submission after restore returns Duplicate and retains its two-copper historical settlement. [Focused case](compile/headless.json) · [Connected result](connected/results.json)

## Execution cost

The reported C# samples time the actual public input through its committed result and a scoped view. The console report separately includes JSON processing, startup and full pending file restore over the entire walkthrough. The accepted reference budgets apply to the eight named checkpoints. The raw timing report includes every measured input, including the existing long calendar advances and the charter-plan submission, which reconstructs the prior passage in its resolver. [Public C# results](connected/results.json) · [All samples](connected/samples.csv) · [Console result](console/results.json)

The Intel Core i5-4590 Windows host ran PowerShell 7.6.9 on .NET 10.0.14. One complete walkthrough warmed the process before 30 measured walks, with nearest-rank p95 and no concurrent regression. Every measured walk reached the same final SHA-256, `6f1bc7afa0f5727e76dccc26d0d33911682f791a3ca3e971ca1350c64dcdd521`.

| Reference input | Starting revision | Median ms | P95 ms | Max ms | P95 budget ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| Opening step | 0 | 4.681 | 6.006 | 6.337 | 150 |
| First encounter attack | 9 | 4.903 | 5.640 | 5.666 | 150 |
| Mid-expedition clock advance | 49 | 64.371 | 68.004 | 98.322 | 150 |
| Stabilization milestone | 104 | 197.773 | 218.744 | 289.837 | 350 |
| Off-turn opportunity | 113 | 11.675 | 14.684 | 24.937 | 150 |
| Defender stance | 116 | 9.374 | 23.374 | 25.876 | 150 |
| Defender tactical step | 117 | 11.353 | 24.028 | 24.926 | 150 |
| Ordinary continuation | 164 | 15.071 | 30.047 | 30.657 | 150 |

Three existing long advances had p95 values between 2,598.301 and 3,030.663 ms, at revisions 95, 97 and 106. The charter-plan submission at revision 66 had p95 1,192.519 ms. These inputs were outside the eight predeclared reference workloads. The report retains all 4,950 samples so the responsiveness review can account for the full route.

Cold C# start with the first view took 587.292 ms after 87.413 ms assembly loading. Warm startup median was 5.612 ms. Pending save took 15.246 ms, standalone load and decode 2.494 ms, and full restore through the session 5,957.889 ms. The entire console path took 20,818.979 ms for 172 input lines, including 165 commits, four views, two saves and one restore.

## Validation status

C# 9 warnings-as-errors compilation passed for Core, Persistence, LabModel and the focused headless test assembly. The standalone compile and static package checks also passed. The exact four executed assemblies and their source inputs are bound to the implementation commit. The original unfiltered regression finished with 1,481 passes, including all 1,480 previously accepted cases and the original session case. The original implementation remains held in its historical review. The tactical decision correction has its own source, assemblies and unfiltered execution. Unity gameplay integration remains deferred. [Original regression](regression/results.json) · [Artifact bindings](BINDINGS.json) · [Correction](correction/README.md)
