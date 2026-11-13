Actual Unity Rules Engine Development reply `76a47a76-0d85-4e74-82d0-98a6c2baaa25`, recorded verbatim apart from trailing whitespace.

## INT-03/P1 charter-plan submission — approved for bounded implementation

**Reviewed proposal:** `2b63b7be6175fd48710ace0ded296a7de6e9bd22`
**Accepted reference implementation:** `71e6612cbdc07d2e8e2f347f38355e62c493d5c6`
**Controlling successor ruling:** `f10d1ba9-ac70-4275-b703-949d24dd4b44`

**Approve the proposed verified-prefix passage fact for the existing default and Fishing Trap sessions, subject to the implementation requirements below. No blocking source/API question remains. Codex may implement this bounded increment without another preliminary packet.**

The repository comparison confirms documentation/evidence changes only. This authorizes replacing repeated historical reconstruction with previously verified historical knowledge—not changing the charter’s eligibility rules or weakening candidate and external-state validation.

## 1. The measurements support the selected correction

The retained detailed report records:

| Measurement | Default | Fishing Trap |
|---|---:|---:|
| Public submission plus permitted view, median | 1,121.029 ms | 1,125.271 ms |
| Public submission plus permitted view, p95 | **1,401.808 ms** | **1,321.599 ms** |
| One passage reconstruction, median | 556.201 ms | 554.723 ms |
| One direct resolver call, median | 550.342 ms | 553.662 ms |
| Strict r74 restoration, median | 815.408 ms | 812.765 ms |

Each profile retains 30 warm observations. The measurement script reconstructs the actual r74 prefix, restores it before each submission, executes the original Player command, obtains the permitted view, and requires every resulting canonical digest to match that profile’s first measured output. Restoration is outside the public-command timer and reported separately.

The source supports the diagnosis. `FindPlanningPassage` reconstructs from `Initial()` during fresh charter admission. The current verified checkpoint independently replays the proposed receipt through the same resolver, causing that historical search again. The isolated component measurements overlap the public path and are **not additive**, but they identify a specific repeated operation worth removing.

The profile-validation probe’s empty history callback is acceptable **as diagnostic instrumentation only**. It is not an approved production validation shortcut.

## 2. Preserve the exact passage semantics

The proposal correctly separates the walk’s start from its completion. That distinction must survive the implementation.

### Return the start revision; test the completion cutoff

The existing reference returns **`traversal.StartedRevision`**, not the completing command’s revision. It finds that traversal by replaying only receipts at or before `close.SourceRevision`.

Therefore:

- The stored plan’s `PassageRevision` must remain the accepted **walk-start revision**.
- The private proof must separately retain the **actual completion revision**.
- Eligibility requires completion **at or before** the actual close’s `SourceRevision`.
- A walk begun before the cutoff but completed afterward is insufficient.

In these baseline reports, **48 is the walk-start identity**. It must not be relabelled as the completion revision or substituted for the completion-cutoff test.

### Share the precise existing before/after predicate

Preserve the reference’s actual requirements: the named witness’s matching traversal exists immediately before resolution, its `Running` flag meets the existing condition, that actor has no traversal afterward, its actual destination satisfies the existing position predicate, and the original start receipt is the witness’s accepted `BeginWorldStep` with target `"walk"`.

Do not replace that with current position, movement expenditure, a predicted arrival, a close-report location, or merely a receipt naming the destination. Conversely, do not add a new completion rule that changes which histories the accepted reference recognizes.

Preserve **the first qualifying crossing in receipt order**, not the most recent crossing or whichever one is easiest to retrieve. The accepted function’s early return makes that observable through the stored passage identity.

### Distinguish unavailable proof from verified absence

A missing capability is not evidence that no crossing occurred.

If absence is retained, it must mean **no qualifying crossing through an explicitly verified prefix boundary for this exact scope**. That fact can answer the close-cutoff question only when its verified coverage reaches that cutoff. It must advance with successfully verified transitions; it cannot become a permanent cached “missing passage” result.

A first crossing whose completion is later than the cutoff still produces the reference’s missing-evidence result for that close. Changing the cutoff must never reinterpret its start revision as timely completion.

An unsupported or unavailable proof scope falls back to the current reference search. An inconsistent owner, sealed prefix or purported proof is a validation failure—not an occasion to silently reseal current state.

## 3. Approve the narrow capability extension, with pre-use verification

The proposed optional checkpoint capability is appropriate because the current interface only verifies **after** candidate resolution. Avoiding both expensive searches requires a trusted way to supply the predecessor’s historical fact to the initial resolution as well as the independent transition replay.

### Verify ownership and predecessor bytes before using the fact

After normal current command preflight and duplicate handling, the optimized path must establish that the capability belongs to this exact simulation origin, selected policy/profile and sealed canonical predecessor **before** the fact influences resolution.

The existing `VerifyNext` owner and byte checks remain necessary, but their current post-resolution position is not by itself sufficient for this new earlier use. Neither the caller nor a candidate snapshot may supply or replace the passage fact.

Bind the fact to the complete relevant terms and witness geometry, not only a matching terms ID. Retain the accepted start receipt identity and distinct completion identity, with the verified prefix establishing their provenance.

### Use predecessor knowledge; do not let a candidate prove itself

Both resolver executions may use the same **previously verified predecessor fact**. The independent path must still decode the sealed predecessor, resolve the actual submitted receipt and compare the entire canonical successor.

Any newly observed crossing must be derived from the independent reference transition and adopted only after full successor equality. A value found only in the tentative candidate cannot become the premise that validates that candidate.

This matters because the proposed fact is deliberately **not serialized**: canonical snapshot equality cannot, by itself, validate an arbitrary value placed into an unencoded checkpoint field.

### Preserve atomic failure and instance isolation

Adopt the new state, new sealed prefix and updated historical fact as one successful transition. Rule denial, exception, failed comparison, duplicate, conflict, rejected restoration or failed replacement must leave all three unchanged.

No static cache, policy-constructor cache or shared mutable “last passage” is authorized. Two simulations may use the same policy instance without sharing proof ownership. Prefer explicit command-scoped context; any temporary context must be isolated and cleared on every exit path, including nested calls and exceptions.

Keep the assembly boundary: Core may own a narrow optional interface and dispatch lifecycle, but it must not acquire dependencies on Laboratory charter types or Persistence internals.

### Keep strict reconstruction authoritative

External construction, restore and backup recovery must fully validate the incoming history before establishing a new owned fact. The existing strict path reconstructs from `Initial()` and compares complete canonical state; retain that reference behavior.

Collecting the fact during that validating replay is preferred. The proposal’s alternative—a bounded extra derivation pass after successful validation—is acceptable if its complete startup/restoration cost is reported. It must not read a claimed proof from a file.

Ordinary direct resolver calls, queries and full-reference execution remain on their existing behavior unless they are explicitly inside the private verified capability. Unsupported profiles retain their current paths.

**These are implementation requirements within the approved proposal, not a request to redesign or resubmit it.**

## 4. Existing live charter checks remain live

The cached fact proves one historical crossing. It does not prove that the current planning command is authorized or available.

Retain current checks for mandate, evidence access, episode and charter identity, actual close membership, distinct supply sources, desk condition and permission, actor capability, position, pending decisions, incompatible work and the authorization interval. Existing-plan handling must also preserve its recorded passage and prior-close binding.

Do not cache the whole assessment, an “Available” result, current grants or resource sufficiency. The optimization must not grant planning, acceptance, departure, supplies or objective credit.

No new Snapshot field, receipt field, wire version, content fingerprint or gameplay switch is required. Strict reference mode remains executable.

## 5. Implementation acceptance groups

| Group | Required evidence |
|---|---|
| **1. Historical-proof equivalence** | Match the strict search for the first qualifying crossing, its start identity and completion cutoff. Cover absent, incomplete, reversed, repeated and late crossings, plus altered witness/geometry/terms. Distinguish unavailable capability from verified absence. |
| **2. Capability and transaction integrity** | Reject wrong-origin or mismatched-prefix use; prove failed candidates cannot update the fact. Exercise separate simulations, including shared-policy construction, failed commands between valid ones, duplicates, conflicts, revoked grants and restoration/replacement. |
| **3. Public behavior and persistence** | Both profiles match the accepted pre/post charter bytes and the strict candidate’s public outcomes. Continue their actual histories, including pending choices and saved work, and retain default/Trap compatibility and the four accepted Trap checkpoints. Valid external files reconstruct strictly; plausible forged history still rejects atomically. |
| **4. Measured improvement** | At least 30 isolated warm public submissions per profile, after a warm-up, with **p95 ≤150 ms in each**. Include all capability checks, resolution, independent replay, canonical comparison, commitment and permitted view. Retain raw samples, maxima and separate startup/full-restore measurements. |
| **5. Exact integration evidence** | Exact source/build bindings, focused cases, compilation/static checks and the completed bound regression: all **1,486 accepted predecessor cases** plus the new controls. Preserve actual loaded-assembly and shard-execution provenance. |

Use genuine command histories for positive crossing witnesses. Detached negative projections may test otherwise inaccessible invalid inputs, but must be labelled as such; do not fabricate accepted receipts to claim executable chronology.

The performance evidence must demonstrate both ways the fact becomes available: accumulation through normal committed play and reconstruction after strict restoration. It must not conceal the work in an untimed public query or repeatedly move it to another routine command. Report incremental maintenance and initialization costs where relevant.

The **150 ms routine target remains unchanged**. The separate 350 ms stabilization allowance does not apply to charter submission. A correctness pass with a missed performance target leaves this P1 increment unmet.

## 6. INT-03 reconciliation and scope

The ten-row reconciliation is sufficient for this engineering gate. It identifies the selected EXP-03/04/05, EXP-07, TAC-04/05/10, MGT-10, MGT-06 and FND-02 behaviors and distinguishes supporting scenarios from the exact connected route. It does not claim complete domain catalogues or production authority. No additional gameplay prerequisite is introduced before this work.

**Long work advances, strict-load optimization and further gameplay modules remain outside this implementation.** Their existing P1 dispositions stand. This gate is about removing repeated proof of an already established historical fact while preserving the rules and trust boundary.

## Inspection limits and final ruling

I inspected the engineering contract, ten-row reconciliation, complete measurement script, detailed results/environment records, selected raw sample rows and source-to-proposal comparison. I also inspected the relevant `SharedNextCharterPlan` basis/search/admission code, the complete current `VerifiedSharedWorldCheckpoint`, and the pertinent `Simulation` construction, preflight, execution and strict-history paths.

The recorded DLL hashes agree with the accepted predecessor identities. **I did not execute the benchmark, independently certify machine isolation, recalculate all percentiles, load DLLs or saves, recompute hashes, modify source or run Unity.** I have not independently proved the proposed optimization’s correctness or speed; that remains the implementation gate.

**Final disposition: authorize this bounded INT-03/P1 charter-plan submission implementation under the contract above. No further preliminary source/API packet is required.**

Prior acceptances stand. P1 and INT-03 remain open until their applicable implementation evidence is accepted; production authority is unchanged, and Unity gameplay integration stays deferred.
