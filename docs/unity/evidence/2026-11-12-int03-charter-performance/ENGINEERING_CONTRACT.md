# INT-03 P1 charter-plan submission engineering contract

Proposal against accepted gameplay `71e6612cbdc07d2e8e2f347f38355e62c493d5c6` and successor ruling `f10d1ba9-ac70-4275-b703-949d24dd4b44`. This gate covers `StartNextCharterPlan` in the existing default and opted-in Fishing Trap sessions. [INT-03 prerequisites](INT03_RECONCILIATION.md) · [Successor ruling](../2026-11-12-mgt06-connected-trap/GPT_FINAL_REVIEW.md)

## Baseline and diagnosis

The public benchmark replays each profile's accepted history through r74, restores that exact pre-submit state before each sample, and measures fresh Player submission through commitment and the permitted Player view. There is one warm-up and 30 warm samples per profile, with nearest-rank p95 and maxima. Strict restoration occurs before the public timer and is reported separately. Independent diagnostic probes measure the existing passage reconstruction, resolver, one snapshot copy, one encode, structural checks, and profile checks apart from the replay callback. Those probes overlap the public path and are not additive. [Raw measurements and accepted checkpoint identities](baseline/results.json)

The command proves that the named companion previously completed the selected walk from the appraisal stage to the approach. It starts at r74, with episode-close source r61 and qualifying walk start r48. `FindPlanningPassage` calls `Initial()` and replays from revision zero until the first qualifying completed walk. The resolver does this on fresh admission. The independently decoded verified-prefix transition executes the same resolver again and repeats the historical reconstruction. The timings isolate that historical work in each profile. The present independent verification, full external validation and normal rule decision remain acceptance requirements.

| Measured phase | Default median / p95 ms | Trap median / p95 ms |
| --- | ---: | ---: |
| Public submit through permitted view | 1121.03 / 1401.81 | 1125.27 / 1321.60 |
| One isolated passage reconstruction | 556.20 / 674.35 | 554.72 / 585.04 |
| One isolated resolver call | 550.34 / 704.51 | 553.66 / 589.77 |
| Structural validation | 0.54 / 4.18 | 0.55 / 4.74 |
| Profile checks apart from the history callback | 1.22 / 1.52 | 1.17 / 1.38 |
| One snapshot copy | 0.11 / 0.17 | 0.10 / 0.14 |
| One snapshot encoding | 3.34 / 7.02 | 3.81 / 7.09 |
| Permitted view | 0.19 / 0.24 | 0.21 / 0.25 |
| Strict r74 restore | 815.41 / 972.34 | 812.76 / 857.13 |

Public maxima were 1486.04 ms and 1324.98 ms. No concurrent regression was running. The separate exploratory run with fewer component probes reproduced the public bottleneck. Its raw artifacts are retained with the detailed run. The bound assemblies come from the [accepted MGT-06 packet](../2026-11-12-mgt06-connected-trap/BINDINGS.json).

## Proposed correction

Carry the first proven qualifying crossing as an in-memory fact of the existing sealed verified prefix for these two profiles. Its identity includes the policy instance and exact content fingerprint, verified origin, terms binding, witness, full coordinates, walk-start receipt/revision and the completion revision. The existing sealed canonical predecessor and receipt history bind the fact to the actual owned state. No field enters Snapshot, receipts, the save format, a process-wide cache or the public API. Do not generalize the new path to legacy or production policy.

Extract and share the reference's precise before/after predicate. It looks at the qualifying traversal immediately before a successful resolver call, then requires disappearance of that actor's traversal and the exact ordinary destination after resolution, together with the original accepted BeginWorldStep walk receipt. Preserve first qualifying crossing order, including its current use of the before-state Running flag. Keep walk-start and completion revisions distinct. Accept the proof for planning only when completion is within the actual close source revision and all existing terms/close checks pass. Verified absence through that cutoff must preserve the original missing-evidence result. If the verified capability or scope is unavailable, keep the strict reference behavior.

Initialize the fact only from history reconstructed under strict validation for the exact selected origin. Prefer deriving it as part of the existing validating replay. If a bounded extra pass is required, measure it as startup/restore cost and preserve atomicity. No caller-supplied proof or external file can seed it. Extend only after a command succeeds and the candidate matches an independently resolved canonical transition. Candidate mutation and rejection cannot advance it. The independent transition decodes the existing sealed predecessor and consumes the same previously verified fact; it must independently resolve the current command and match canonical bytes before adopting any successor. Apply current command authority and receipt checks first. Fresh origins, replacements and restore/recovery rebuild their own fact after validation. Preserve direct, query, and full-replay calls through the strict reference unless they already operate within the private verified capability.

The trusted entry point may require one narrow optional interface on the existing verified checkpoint, so the standard Simulation dispatch can pass the owned capability to candidate resolution. Keep existing callers and policies on the current path unless the optional capability exists, and make the optimized call contingent on the same owner and predecessor. Do not skip shape, profile or canonical transition validation. Leave long calendar commands and strict restoration optimization as separate work.

## Acceptance

- Match strict-reference disposition, receipt, Action/work, clock, RNG, plan passage identity and canonical save bytes for the same accepted public input in both profiles. Preserve live conditions, worker/desk/authority rejections, stale/duplicate/conflict behavior, and the exact plan history and continuation across restore/recovery.
- Prove qualifying and absent passages, earlier incomplete or reversed crossings, the first qualifying crossing among repeats, close-source cutoff, altered and cross-profile history, independent origins, and correct invalidation after rejection, replacement and restoration. Retain authentic default and opted-in saves and relevant standalone charter compatibility. An internal proof cannot authorize any outcome by itself.
- Run 30 or more isolated warm public submissions per profile. Require routine p95 at or below 150 ms in both. Report maxima, startup/strict restore separately, and component timing where useful. Keep complete external validation, independent candidate transition and artifact provenance. Report exact source, build, full regression and connected walkthrough/replay evidence for GPT review before advancing.
