Actual Unity Rules Engine Development reply `e58e03d6-6dff-4767-b60d-b661bbcb9b2b`, recorded verbatim apart from trailing whitespace.

## INT-03/P1 charter-plan submission — accepted

**Accepted implementation:** `e4c5f7f36f9c59b559fc42c6ccf0489c91225999`
**Final evidence reviewed:** `7b66013bfe277bfffe4a6cbfbffa3d04785c48c7`
**Controlling contract:** `76a47a76-0d85-4e74-82d0-98a6c2baaa25`
**Closed review:** `ccf2e0a8-db41-42ea-af82-b15d08828723`

**Both pending items are closed: the complete public-response comparison and the exact bound regression. All five acceptance groups are met. I accept this exact bounded implementation. No concrete blocker remains, and no correction or additional acceptance test is requested.**

The source-to-evidence comparison contains three documentation/evidence commits and **no intervening engine or console-source changes**. This verdict carries forward the completed implementation and timing review rather than reopening unchanged source.

## 1. Complete public-response equivalence is established

The supplemental comparator checks each entire parsed JSON record. Its canonical representation sorts object keys but retains field presence, values, nested objects and array ordering. It does not use a selected-field allowlist or remove tactical ownership, pending decisions or permitted-view data. The finalizer now requires that comparison to pass without ignored fields and binds its input transcript digests to the retained files.

| Profile | Compared records | Permitted views | Result |
|---|---:|---:|---|
| Default | 277 | 30 | All fields match; recorded raw transcript hashes also match |
| Fishing Trap | 322 | 39 | All fields match; recorded raw transcript hashes also match |

The report explicitly records `IgnoredFields: []`. This closes the missing assertions for `NextSeat`, `PendingDecision`, `OpportunityPending` and the intermediate permitted views—not merely the final save comparison.

**The default reference adjustment is appropriate.** The older EXP-05 transcript predates the `FishingTrap` view field, so replaying its inputs with the accepted MGT-06 reference assemblies compares the same public API version without deleting that field. The retained reference and optimized default transcripts also have the same Git blob identity. The authentic EXP-05 r223 save remains unchanged. The Trap comparison continues to use its accepted MGT-06 transcript.

I inspected the comparator, comparison report, finalizer and reference-file identities. **I did not independently execute the reference replay or recompute the transcript hashes.**

## 2. Completed exact regression closes E1

The final report records **1,487 discovered, 1,487 passed and zero failed**, against the reviewed implementation and source archive:

```text
7cd9be3ba25c8d0fe8f2f97ee5aa0c24a9971f880203809cd3af170c3d087020
```

Its four recorded DLL digests—Core, Persistence, LabModel and HeadlessTests—agree with the final bindings and previously reviewed focused assembly set. These are retained execution results I inspected, **not executions I performed**.

The final manifest binds the report to:

```text
7f244cd5014183b5841dba0fed85a00240b718d01caac4de26a9ff5a931001e2
```

I inspected that recorded binding; I did not independently calculate its byte-level SHA-256.

### Execution identity and inventory

I read **all six worker completion records**. They identify run `88a4d60e8d494594b4a590bec9a37bdb`, agree on the four assembly digests and module identities, and retain their individual assignment, inventory and completed-journal bindings. Their counts are **250, 248, 248, 248, 247 and 246**, totaling 1,487.

The finalizer requires the unchanged **1,486 accepted predecessor names plus `int03_verified_charter_passage_ownership_and_cutoff`**, exact assignment-to-journal order, completion markers, unique passing rows without errors, and agreement with the focused result. The new control is included in the 1,487 total—not added to it afterward.

I inspected the new control’s actual passing journal row and representative inherited results covering the connected Trap, current authority, pending-state forgery, duplicate handling, restoration and shared work.

**I did not independently reconstruct the complete six-journal union or repeat the full artifact-hash audit.** Those exhaustive checks remain Codex’s reported verification.

**No further historical or unfiltered execution is required for this increment.**

## 3. Final disposition of the five groups

| Approved group | Final verdict |
|---|---|
| **1. Historical-proof equivalence** | **Met.** First qualifying passage, distinct start/completion identities, exact terms and completion cutoff retain their reference semantics. |
| **2. Capability and transaction integrity** | **Met.** The owned sealed predecessor is verified before use; independent reconstruction establishes the successor fact; rejection does not advance state or proof. |
| **3. Public behavior and persistence** | **Met.** Complete public results and views now compare, alongside the accepted save identities, restored/live submissions, authentic compatibility and atomic forged-history rejection. |
| **4. Measured improvement** | **Met for the selected command and profiles.** The reviewed public p95 measurements remain **12.1105 ms default** and **15.3064 ms Trap**, below the unchanged 150 ms target. |
| **5. Exact integration evidence** | **Met—E1 closed.** The completed bound regression supplements the focused, compilation, static and connected evidence. |

The reviewed default and Trap checkpoints, r74/r75 identities and timing artifacts remain retained in the final bindings. **The increased restoration cost remains accepted as a disclosed tradeoff for this bounded increment—not an improvement to, or closure of, strict-restoration P1 work.**

## 4. Immediate successor: long active-work advances first

**Proceed next to an INT-03/P1 engineering/source/API gate for long active-work `AdvanceClock` execution. Strict-restoration optimization follows as a separate gate. Do not implement either change before its contract is agreed.**

This is the selected priority:

| Priority | Target | Reason |
|---|---|---|
| **First** | One existing long active-work advance in the connected session | It blocks an ordinary gameplay submission while the player progresses work. It is the next unresolved live-execution cost after charter submission. |
| **Second** | Strict restoration, including repeated reconstruction and the added passage-derivation pass | It remains a material load/recovery cost, but its trust boundary should be reviewed separately from live calendar execution. |

Improving a shared resolver may also reduce work performed during strict replay, but **that is a possible secondary benefit, not an assumed result or permission to weaken restoration**.

### Select one concrete first workload

Use the existing formula-research advance following `StartFormulaResearch` as the primary workload. The current accepted default history supplies an exact starting point:

**`i-94`, submitted at revision 103, advancing 15,421 seconds during `formula.103`.**

Use the corresponding accepted checkpoint and command in the Fishing Trap profile as well. The subsequent research advance and manufacturing advance are related measurements and regression controls; they do not automatically become additional optimization scopes. The accepted history identifies those separately as `i-96` and `i-105`.

The next packet should establish the actual current pre/post states and endpoint behavior. Do not rely on revision labels or timing figures from an older walkthrough version.

### Required engineering questions before implementation

**Measure the current cost before choosing the mechanism.** Retain an isolated baseline for both accepted profiles, with exact input/output saves and public command-through-permitted-view timing. Separate direct resolver work, repeated calendar processing, active-work calculations, validation, independent transition replay, copying and encoding sufficiently to identify the expensive operation. Component probes are diagnostic and must not be added together when they overlap.

**Propose the smallest semantics-preserving correction.** No blanket clock jump, tick skipping, new cache, asynchronous commitment, receipt splitting or scheduler rewrite is approved by this acceptance. The contract must identify precisely which repeated computation can be removed and why every relevant boundary remains represented.

**Preserve all observable execution.** The new path must retain actual labor, pauses and work windows; personal Starts and Ends; condition expiry; spoilage/protection deadlines; remote work; RNG order; due checks; pending choices; tactical yields; reached-clock results; receipts and canonical state. In the Trap profile, the presence of fishing state must not cause either an omitted due event or a new event that the reference would not execute.

Do not optimize only the final totals and ignore an intermediate boundary that can change what happens next. An unsupported combination must retain the reference path until it is explicitly covered.

### Set its performance criterion in that contract

The **150 ms routine-command target remains unchanged**. The **350 ms allowance remains specific to the previously identified stabilization workload**; it is not a general exception for arbitrary long advances.

For the selected long-work submission, propose an explicit wall-clock acceptance bound, supported by the new baseline, before implementation. Report at least 30 isolated warm samples, median, p95 and maximum, including the full public submission and required verification. Merely displaying a busy indicator does not satisfy a command-cost target.

Retain the accepted implementation as the strict reference. Acceptance must compare the same command’s full public result, intermediate rule-event consequences and canonical successor, then continue the connected history. Do not silently replace one submitted command with several separately committed commands to make the individual measurements smaller.

### Strict restoration remains a distinct follow-up

Its later contract should examine full historical reconstruction, copying/decoding and the additional passage derivation separately. Collecting the passage fact during an already required validating replay may be worth investigating, but **that change is not authorized here**.

External saves and recovery inputs must still establish valid history before adoption. An on-disk checksum, a previously trusted session or a serialized proof cannot be substituted for that requirement.

## 5. Approved dependency order remains intact

This remains **INT-03 engineering over its accepted minimum slices**, not a new gameplay module or a reopening of those acceptances.

The direct prerequisite rows remain:

**EXP-03, EXP-04, EXP-05, EXP-07; TAC-04, TAC-05, TAC-10; MGT-10, MGT-06; and FND-02.**

The reconciliation distinguishes the actual connected route, supporting scenario coverage and remaining unsupported areas. No new gameplay prerequisite is needed before profiling the selected advance.

Keep the order **long active-work advance contract → reviewed bounded correction → separate strict-restoration contract → remaining INT-03/P1 closure assessment**. A newly discovered concrete dependency can change an implementation plan, but no new recipe, encounter, production profile or Unity feature should be inserted merely to avoid the measured engineering work.

## Inspection limits and final ruling

For this final review, I inspected the comparison script and report, updated finalizer, final bindings and report header, launch manifest, all six completion records, actual journal excerpts, reference/implementation transcript-file identities, and the source-to-evidence comparison. I also checked the retained INT-03 reconciliation and the actual research/manufacturing inputs used to select the successor.

The earlier implementation review remains the basis for unchanged proof logic and timing findings. **I did not execute tests or scripts, compile, load DLLs or binary saves, regenerate the reference transcript, recompute hashes, verify every journal row, modify repository files or run Unity.**

**Final ruling: accept `e4c5f7f36f9c59b559fc42c6ccf0489c91225999` with evidence `7b66013bfe277bfffe4a6cbfbffa3d04785c48c7`. Close both pending items and all five bounded charter-submission groups.**

The immediate next work is **the scoped long active-work advance engineering contract, beginning with the existing formula-research advance**. Strict restoration is second and separately gated. Prior acceptances stand; broader P1 and INT-03 remain open, production authority is unchanged, and Unity gameplay integration stays deferred.
