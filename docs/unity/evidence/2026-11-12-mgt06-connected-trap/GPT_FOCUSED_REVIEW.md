Actual Unity Rules Engine Development reply `182c0bfb-11fa-4e80-a965-44039d4b3f00`, recorded verbatim apart from trailing whitespace.

## MGT-06 focused implementation review

**Source reviewed:** `71e6612cbdc07d2e8e2f347f38355e62c493d5c6`
**Evidence reviewed:** `eed68d75725529affaf8e9a8043548f8a95202d3`
**Governing authorization:** `25f0927c-dab3-40cf-b4df-bd096401d90e`

**I found no concrete gameplay-source blocker in the bounded implementation. The opportunity-release correction and retrieval-payload correction are appropriate. Continue the exact regression without changing the gameplay source merely for this review.**

I found **two focused evidence-verification corrections** to address before final acceptance: the walkthrough verifier does not assert several public-response requirements, and the regression packager does not independently establish that the supplied journals were produced by the four assemblies it labels as executed. These are verification gaps—not evidence that the retained gameplay run failed.

**This is an interim implementation review, not final acceptance of the pending 1,486-case regression.**

## What I actually inspected

I inspected the seven changed source/test/tool files, including the affected initialization, fingerprint, session admission, observation, setup-Resume, opportunity validation and retrieval paths. I also read the complete added C# focused case; `Test-TrapWalkthrough.ps1`; `New-TrapWalkthrough.py`; `Retain-TrapEvidence.py`; `Start-ExactTrapRegression.ps1`; the referenced regression shard runner; and the historical-save verifier supplied in the evidence commit.

For retained results, I inspected `BINDINGS.json`, `connected/results.json`, compilation/static-report summaries, the MGT-06 input extension, and the corresponding setup, restore, away-check, opposing-seat, local-return, retrieval and retry responses. This was **not** a line-by-line rereview of the entire accepted 223-command predecessor expedition.

**I did not compile, load assemblies, execute tests, decode the binary saves, recompute their hashes, modify files or run Unity.** Byte-equality statements below describe the retained verifier/results and matching manifest entries, not an independently executed comparison.

## Implementation findings

### Initialization and profile separation meet the bounded design

`Start()` retains the ordinary expedition composition. `StartWithFishingTrap()` adds the selected Trap through a separate fingerprinted policy, and the console’s `-FishingTrap` switch selects that factory. Restore and backup recovery validate through the session’s existing selected policy before adopting replacement state; they do not infer a new profile from the incoming save.

The initializer addresses the identified composition problems directly:

- The connected Trap initializes **after** portable equipment, while existing non-connected profiles keep their previous order.
- The connected selection does not perform the standalone alternate-worker Club adjustment or overwrite the Bonus Action ledger.
- Source-correct WIS selection is enabled without enabling responsibility handover or importing its setter-score initialization.

The unequal-ability probe is appropriately isolated: it gives a copied test state WIS 16 and INT 8, runs actual setup resolution, and requires the captured Wisdom modifier to be `3` with one proficiency contribution of `2`. It does not alter the playable profile’s character facts.

### The opportunity-release correction is valid

**Keep this correction.**

For a previously released opportunity being reserved again, the historical release must not occur **after** the new reservation. Rejecting `LastReleasedAt > ReservedAt` is the correct direction; the previous comparison rejected an ordinary later reservation following an earlier release. `Reserve` still requires `Available`, and `Commit` still requires `Reserved`, so this correction does not reopen a spent opportunity.

The additional validator requires the release reference to identify an attempt for the same opportunity, with no opportunity commitment, in `Cancelled` or `CheckMissed` status. It also bounds the recorded release time between that attempt’s start and the current clock. That is appropriate structural validation alongside strict history verification.

This is a **shared Core validation correction**, not merely a session projection change. The main connected witness exercises its positive case through real cancellation followed by later setup. The retained schema37 soaking-save check is useful compatibility evidence, but it should not be described as specifically exercising the corrected release/re-reservation branch.

### Public controls and privacy are appropriately scoped

The public session restricts Trap interactions to the companion and the authorized operation subset. Retrieval now admits the required zero-amount `HandlingKind.Retrieve` payload, then checks the selected receiver and local observation before the native resolver handles physical eligibility. Generic portable handling and ordinary portion/intake controls cannot bypass the selected Trap/bait lifecycle.

The fresh setup-Resume reach requirement is implemented in both assessment and resolution through the same connected-profile predicate. Existing profiles retain their previous behavior. Receipt matching remains before fresh target admission, while current seat authority is checked before submission, preserving the distinction between a fresh remote Resume and an exact accepted-command retry.

The new projection exposes earned setup/deployment timing separately from locally observed physical status and outcome. Trap/bait entries are excluded from generic item projection, and generic work projection does not add raw fishing-attempt results. The opposing seat receives no Trap projection. I found no concrete result leak in these inspected paths.

## What the focused artifacts establish

The retained results report the following chronology, and the inspected console responses agree with the relevant public checkpoints.

| Checkpoint | Retained result |
|---|---|
| Ordinary expedition prefix | Revision **223**, with the Trap present from initialization and no fishing attempt yet. |
| Cancelled setup | One second of credited work; unspent bait and opportunity reservations released. |
| Fresh setup | Starts at **56874**; reaches **599/2** credited seconds before save/restore; deploys at **57174** after 300 seconds. |
| Away-time check | Resolves at **60174**; reports natural **13**, modifier **2**, and **one RNG word**; captures `TEST_ONLY.river-fish`. |
| Local return | Revision **237**, clock **60178**, companion at **(3,3)**; the public view reveals the actual captured result. |
| Retrieval completion | Revision **240**, clock **60478**; 300 credited retrieval seconds and `Retrieved` physical status. |
| Continued play | Revision **242**, clock **60480**. |

The inspected away-check response has `ObservedLocally=false`, with `PhysicalStatus`, `CheckOutcome` and `CapturedCreatureId` all null. The opposing-seat response has `FishingTrap=null`. On local return, the view reports the deployed Trap and the existing captured fish; after retrieval, it reports `Retrieved` and 300 retrieval seconds.

The actual retained transcript also contains successful `Restored` responses at the new setup, away-pending and pending-retrieval loads. At revision 240, the two fresh claims return `Unavailable`, and the exact Set and Retrieve retries both return `Duplicate`, without advancing the recorded revision or clock.

The verifier compares four canonical checkpoints across the restored console route, uninterrupted console route and public C# committed-action replay. The latter replans automatic defender actions instead of simply submitting recorded defender commands. The manifest lists matching checkpoint hashes across all three paths, plus matching historical standalone-save/re-encoding hashes. **Those are meaningful retained checks, subject to the inspection limits above.**

## Focused corrections before final closure

### 1. Make the public walkthrough checks explicit and fail closed

**Affected verifier:** `Test-TrapWalkthrough.ps1`.

The current verifier checks committed totals, fresh repeat-claim rejection, selected redaction fields and checkpoint equality. However, several reported requirements are not asserted strongly enough:

**Observation expectations come from the output being tested.** The privacy check runs only when the returned `ObservedLocally` is false. A regression that incorrectly reports `ObservedLocally=true` while away would skip that check. A missing/failed view is also not explicitly rejected before its nullable fields are examined. Positive local observation and agreement with the actual resolved result are not asserted.

**Successful loads and exact retry responses are not required.** Replacing a `Restored` response or either expected `Duplicate` with `Unavailable` need not change the committed-action total or final save. The launcher deliberately converts caught exceptions into a bounded `Unavailable` response, so the verifier must distinguish an expected rejection from an unexpected failure.

**Atomicity checks compare revision only.** The cross-profile and altered-history controls require an exception and an unchanged revision, but do not compare the whole live state before and after rejection. The inspected session implementation validates before adoption, so this is not a demonstrated atomicity defect; it is weaker evidence than the stated atomicity claim.

**Required correction:** define expected response/view behavior from the known input checkpoint, independently of the returned values. Require successful saves/loads, both exact `Duplicate` replies, a real enabled Player Trap view, explicit away/local observation expectations, and local outcome/identity agreement with the actual saved result. Check Trap-related leakage in both Items and Work. Compare canonical live state before and after rejected restores, rather than revision alone.

Apply the relevant response checks to both console histories. Keep the direct C# path accurately described as **committed-action replay** unless it is extended to replay the noncommitting inputs too.

**The retained responses I inspected already show the expected behavior. This correction makes the verifier enforce that behavior; it does not call for forcing a catch, changing the seed, or changing gameplay source.**

### 2. Bind final regression journals to their execution assemblies

**Affected evidence path:** `Start-ExactTrapRegression.ps1`, its referenced shard runner, and `Retain-TrapEvidence.py`.

The final packager performs useful exactness checks: 1,486 unique names, the accepted 1,485-name predecessor inventory, assigned journal order, completed shards, no duplicate/failed cases, and agreement with the focused case. Preserve those checks.

The remaining gap is that it computes `executedAssemblies` from the files supplied through `--headless`, then places that identity on results assembled from the separately supplied `--regression` directory. It does not compare those journals against a run-specific assembly manifest. The launcher records an assembly-root path, while the shard runner validates test names and permits journal resumption without an assembly-digest check. Equal test names do not establish equal compiled behavior.

**Required correction for the final packet:** retain and validate execution provenance connecting each shard—and any resumed portion—to the exact four assembly digests in the packet. The packager must reject a mismatched run identity instead of attaching the current assembly identity to otherwise matching journals.

Use genuine retained launch/run evidence where available. Do not retrospectively label newly measured file hashes as proof of what an earlier process loaded. The same distinction applies to the historical standalone-save claim: retain its prior-assembly provenance separately from the current restoration result.

**This finding does not establish that the running regression used different assemblies.** It identifies what the current verifier cannot independently prove. An evidence-only correction does not by itself require a gameplay rebuild or discarding completed journals whose execution identity can be established.

## Regression, performance and scope disposition

The focused headless report records one passing case; the separate compilation report records Core, Persistence and LabModel compilation success; the static report explicitly limits itself to package structure. `BINDINGS.json` correctly leaves `regressionCases` null. None of these should be promoted to a completed full-regression or Unity result.

The retained timings are approximately **14.94–198.16 ms for submission plus view** and **12.29–12.69 seconds for strict checkpoint restores**. They remain single-run observations, not performance acceptance or justification for weakening validation. P1 stays open.

**Final interim disposition: no concrete gameplay-source blocker found; two focused evidence-verifier corrections required before final closure.** Keep source `71e6612…` and the live outcome unchanged unless an actual failing test establishes a source defect. Complete the exact journals and return with the strengthened verification and execution bindings. No new preliminary source/API packet is required. Broader INT-03 remains open, and Unity integration remains deferred.
