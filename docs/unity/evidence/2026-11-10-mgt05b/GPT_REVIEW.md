# GPT review and authorization — MGT-05B schema75

## Prior MGT-05A gate

GPT's pasted blocker report concerns the superseded commit `300fa051bb40ceb6f535b20bcc58bde0e78d0729`. GPT later accepted the corrected MGT-05A commit `1e0bbc1168808686cec20a1d52ffa33284550646`, with: “No concrete acceptance blocker remains within the agreed MGT-05A scope.” The acceptance is recorded on `Engine` in commit `e4c8e540ed70081f0ee0e3b4d516261d5e6a9d72` and in [the MGT-05A verdict](../2026-11-10-mgt05a/GPT_REVIEW.md).

## MGT-05B contract and implementation authority

GPT reviewed the source/API boundary for a closed-container first treatment slice and approved schema75 as an explicit TEST_ONLY contract. It required unsupported interactions to be prevented, not merely omitted from documentation. The approved first material is the existing harvested `generic.ordinary-fish-meat` lot; the attempt uses one actual 0.5 lb supply lot, exact Cooking/Wisdom and Cook's-utensils fixture binding, a separately authored sealable preservation container with explicit TEST_ONLY fit facts, one DC10 check, and 24 hours of successful protection. GPT accepted derived preservation history and schema75 isolation while requiring schema74 to remain byte/fingerprint/behavior compatible. It left the listed exposure, re-treatment, interruption, broader-material, and production-recipe features deferred.

GPT's actual clarification of implementation authority:

> Yes—the phrase reflected the source/API-only scope of that review prompt, not a conflict with the owner’s standing authorization. My wording was too absolute and should not have created another authorization barrier.
>
> Under the standing engine-development authorization you’ve stated, Codex may proceed with MGT-05B implementation on Engine, strictly within the approved closed-container schema75 TEST_ONLY contract, including recording the specified fixture/API bindings.
>
> No additional owner decision or repeat authorization review is required.
>
> I identify no concrete conflict with that standing authorization. The deferred features remain excluded. Implementation permission is not module acceptance: MGT-05B’s resulting code and retained evidence must still pass implementation review before the module is closed.

The MGT-05B implementation was authorized under the standing engine-development direction and was subsequently accepted at the exact correction commit recorded below. The actual source/API review, implementation authorization, and final acceptance were communicated in the “Draft MGT05 API Contract” chat; this file distinguishes GPT's artifact review from Codex's retained execution results.

## Implementation review status

### First review — returned for bounded corrections

Codex sent the exact implementation commit `4d11fdceb25fb6a9f86b419484f3cca70a615211`, evidence/docs commit `bb6a2f5c45fd43728aebefe10f9bb9a3e6354012`, the complete code patch, file list, source bindings, and retained reports to GPT in “Draft MGT05 API Contract.” GPT replied: “MGT-05B is not accepted at implementation commit `4d11fdceb25fb6a9f86b419484f3cca70a615211`.” Its final disposition was: “Return MGT-05B for bounded correction.”

GPT identified three in-scope blockers: (1) treatment validation rejected children created before treatment, and age projection failed to stop an ancestor’s protection at the first branch separation; (2) the policy permitted whole closed-vessel handover, but fixture validation permanently required the original worker to remain supply custodian; (3) the passing package report did not hash-match the three committed `.meta` files. GPT confirmed these were bounded corrections within the approved contract and required no owner ruling, source/API re-review, or expansion into deferred features. Optional stress testing, exposure handling, re-treatment, broader materials, and production-food integration were explicitly not blockers.

GPT inspected the patch and retained reports, compared the exact GitHub revisions, and text/hash-checked the source artifacts. It explicitly did **not** compile or execute the submitted C# code or tests. The original findings and their source/reasoning are preserved in the GPT response in the chat and the before-fix reproductions are in the [correction evidence](review-corrections/README.md).

### Corrected implementation — accepted

GPT reviewed correction commit `9c0a4e92b7f2af8c62c07326934fad7524f64f9c` against the exact evidence/docs commit `6573b7882ee2f9c6323a2de96d95100820e80629` in the “Draft MGT05 API Contract” chat. Its final disposition was:

> MGT-05B: ACCEPTED at `9c0a4e92b7f2af8c62c07326934fad7524f64f9c`, with evidence/docs at `6573b7882ee2f9c6323a2de96d95100820e80629`.
>
> No concrete acceptance blocker remains within the agreed bounded schema75 TEST_ONLY contract. Codex may record this verdict and close the MGT-05B implementation-review gate. No further correction, owner ruling, or repeat design review is required for this slice. This review does not select or start another module.

GPT confirmed that the three returned findings are closed: branch-specific age projection no longer gives a late-created descendant protection its material did not experience; treatment validation permits children that separated before protection while preserving the restriction on in-window splits; and the legal closed-vessel handover validates current physical custody while retaining owner, treatment worker, and immutable history. The actual handover regression preserves protection, rejects opening/content retrieval, and verifies save/restore and replay.

GPT reviewed the retained results as follows: the full C# 9 regression reports **1,326/1,326**, all five MGT-05B cases pass in that suite, the focused lineage and handover corrections each report **1/1**, both pre-fix defect reproductions retain their expected `InvalidResult`, and static package validation reports **18/18** (308 assets, 308 GUIDs, 605 hashes). GPT independently matched report/patch digests and the 282 source entries to the refreshed package report, reconstructed and hashed the changed treatment-handler and test-file bytes, and confirmed the three corrected `.meta` hashes. It inspected the corrected core projection directly but did not independently recompute that entire file’s hash or load the retained assemblies.

One evidence qualification is explicitly nonblocking: the standalone lineage report is from an intermediate test-source revision, while the exact final full-suite report includes and passes that case; the focused handover report matches all 282 final source hashes. GPT said this requires no rerun. Deeper randomized lineage trees, repeated handovers, and stronger forged-snapshot tests are optional hardening, not acceptance blockers.

The acceptance remains limited to the bounded schema75 TEST_ONLY treatment slice. Exposure handling, clean-tool openings, re-treatment, active-protection content splitting/repackaging, cancellation settlement, other materials, and production recipes remain deferred. Unity import/compilation, Editor tests, Play Mode, player builds, and observed gameplay were not run. This does not complete all of MGT-05 or the engine.

## GPT's next-dependency recommendation

In response to “What should Codex work on next?”, GPT recommended: “Record the accepted MGT-05B verdict, then begin the next bounded MGT-05 source/API review: preservation exposure and controlled opening, provisionally MGT-05C.” It specified the contract should cover the strict brief-opening window, actual breach/contamination/incompatible-heat termination, physical portioning/which material remains protected, original age, shared-clock/persistence/event ordering, and a connected clean-opening plus protection-ending scenario. It warned not to assume a removed portion inherits the vessel's remaining protection. GPT said to present unsettled timing as narrowly labeled proposals and to defer re-treatment, broader materials, production food/recipes, generalized repackaging, and Unity. Its final line was: “Next deliverable: the exposure/opening contract—not another MGT-05B correction or optional test-expansion round.”

The source/API review draft is [MGT05C_SOURCE_API_REVIEW.md](../2026-11-10-mgt05c/MGT05C_SOURCE_API_REVIEW.md). No MGT-05C implementation has started; the contract must be aligned with GPT first. GPT stated that the owner's standing implementation authorization applies after the contract is agreed and no separate owner-permission cycle is needed.
