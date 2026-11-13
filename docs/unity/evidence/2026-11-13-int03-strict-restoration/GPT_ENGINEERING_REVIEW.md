Actual Unity Rules Engine Development reply `7eb9c90e-b182-464e-863f-01561c9d5cf9`, recorded verbatim apart from trailing whitespace.

## INT-03/P1 strict restoration — approved for bounded implementation

**Reviewed proposal:** `6c70cde821b9decf09494d0e92e6e79e448fc230`
**Accepted reference implementation:** `26854d6f49842ae3ea40536d96cc102bc2896e24`
**Controlling successor ruling:** `91241370-a7b5-4ebd-a9e1-9973d3f26834`

**Approve the proposed combined validation-and-sealing construction path for the two selected profiles. Approve the proposed r104 public restore-through-view criterion of p95 ≤3,950 ms independently in each profile.**

No blocking source/API question remains. Codex may implement this bounded mechanism under the requirements below without another preliminary packet. The important clarification is that **collecting a passage fact during replay must not make either that fact or the new simulation origin trusted before the entire incoming state passes validation**.

The source-to-proposal comparison contains documentation and evidence changes only. This approval does not extend condition caching into external history or authorize a broader restoration rewrite.

## 1. The measured target is supported

The retained baseline records the following:

| Measurement | Default | Fishing Trap |
|---|---:|---:|
| Public r104 restore-through-view, median | 4,063.893 ms | 4,023.321 ms |
| **Public r104 restore-through-view, p95** | **4,427.223 ms** | **4,202.973 ms** |
| Public maximum | 4,581.436 ms | 4,216.489 ms |
| Historical replay and canonical comparison, median | 3,367.983 ms | 3,325.375 ms |
| Separate passage derivation and sealing, median | 668.532 ms | 663.769 ms |

The public distributions contain 30 warm samples per profile. The component probes contain **five samples**, not 30; their timings may overlap and must not be added together as a reconstructed public total.

The measurement script times the real `session.Restore` followed by a permitted Player view, then requires byte-identical re-encoding of the accepted r104 state. It reports initial loading and paired r103/longer-history controls separately. The Fishing Trap first-load observation occurs second in the same process; it is not a second independent cold-process measurement.

The source confirms the duplicated work being targeted. The constructor currently validates the detached candidate, creates its verified origin, and calls `Seal`. `Seal` then replays the prefix separately to derive the first passage. Removing that additional derivation while retaining complete validation is a coherent, narrow optimization.

**The proposed criterion is reasonable for this increment.** It is a bounded load-time improvement target, not a declaration that all restoration is fast enough or that broader P1 is complete.

## 2. Approve the optional construction capability—with a strict success boundary

The selected path may combine domain validation, full historical reconstruction and checkpoint establishment. It must preserve this sequence:

**Decode and structural checks → detach the candidate → selected scope/domain checks → complete uncached historical reconstruction → whole-state canonical equality → establish the owned checkpoint → adopt the replacement.**

### Core retains the construction checks

Core must retain responsibility for execution-profile and verification-mode validation, structural shape, content identity, TEST_ONLY/Release restrictions and ownership of the detached input. The optional capability is selected only for the supported default and Fishing Trap compositions in their intended verified-prefix mode.

The existing `FullReplay` constructor remains an executable reference. Unsupported profiles continue through their existing validation and sealing path. Distinguish **unsupported capability** from **failed validation**: an invalid selected file must not fall through to a weaker path, silently reseal or become a fresh initial session.

Reuse the existing selected domain checks with the real history-validation callback. The benchmark’s empty callback is diagnostic instrumentation only; it is not an implementation option.

### An early owner identity is not an early verification certificate

The current `VerifiedSimulationOrigin` is documented and constructed as a capability created **after full initial validation**. Do not merely move its live assignment above validation and retain that assumption elsewhere.

Core may reserve a fresh private ownership identity during construction. Until complete success, however, it is only a **provisional construction identity**. Neither it nor a provisional checkpoint may authorize commands, be adopted by the session, or be reused by another attempt. A provisional identity or an equivalent success-only construction result is sufficient; this ruling does not prescribe a particular class design.

The accepted input, the bytes compared during validation, the state ultimately owned by the simulation and the checkpoint’s sealed predecessor must all describe the **same detached candidate**. Do not validate one mutable object and seal another, or repair an invalid external candidate into validity during construction.

Any validation failure or exception returns no usable checkpoint. Missing or internally inconsistent success output must fail closed.

### Keep the assembly boundary narrow

An optional Core interface may describe construction success/failure and ownership without importing Laboratory charter types or Persistence internals into Core. The selected policy remains responsible for its domain interpretation; this is not a new unrestricted “trust this snapshot” API.

## 3. Collect the passage as an observer of replay—not as an input to validation

The first-passage collector should observe the actual before/after transitions in the required outer historical replay. Preserve the existing terms binding, witness and geometry, accepted walk-start receipt, distinct completion receipt, first-match ordering and verified coverage.

**Continue validating every later receipt after a qualifying crossing is found.** Finding an early valid crossing cannot authorize a file with a corrupted later command or a final canonical mismatch.

During that validating replay, do not feed the provisional passage back into historical charter admission. The proposal explicitly retains the original charter assessment for historical commands, and that is the approved scope. The derived fact becomes available to later live execution only after complete validation succeeds.

The existing passage semantics remain unchanged:

- The stored passage identity is the **walk-start revision**.
- Eligibility at a close cutoff depends on the **completion revision**.
- The first qualifying crossing is retained, not the latest.
- Verified absence is bounded by the history actually validated.
- An unfinished crossing at the end of a valid save must remain capable of becoming the first crossing through subsequent genuine live execution.

The existing predicates and `PlanningPassage` already encode these distinctions; reuse them rather than creating another interpretation.

### Clarify the diagnostic “once” claim

The proposed statement that validation resolves “every receipt once” needs a precise counter boundary.

**The outer validating traversal should visit every retained receipt once, and the separate post-validation sealing replay should disappear.** But the unchanged historical charter assessment can itself call `FindPlanningPassage`, which performs a nested prefix replay. Those reference calls remain within this proposal.

Report outer-replay visits, nested reference reconstruction and dedicated sealing replay separately. Do not assert that the total number of resolver invocations must equal 104, or remove nested reference work merely to achieve that count.

This is an evidence-definition clarification, not a request for another proposal.

## 4. Preserve rejection, recovery and subsequent execution

Each load must reconstruct a fresh owned simulation. A filename, checksum, previously successful load, matching revision or another instance’s checkpoint supplies no authority to skip validation.

All provisional passage data must remain local to that construction attempt. Do not retain it in mutable policy fields, static caches, saved records or a reusable “last validated” result. Two simulations sharing a policy and repeated loads into one session must remain isolated.

On failure, preserve the entire live state and checkpoint, controller binding and current seat permissions—not merely the revision. The next legitimate command must behave as it would have before the failed load.

For backup recovery, validate and prepare the complete replacement before displacing files or adopting state. Preserve the existing recovery guarantees on validation and I/O failure. A rejected backup must not damage the live session or overwrite evidence needed for recovery.

Successful restoration must not advance simulated time, pay a cost, redraw RNG, resolve a pending choice or repeat a world consequence. Pending work and tactical responses must continue through their actual owning seat and normal command processing.

**Per-receipt condition reuse in external history remains outside this contract.** Keep the uncached reference resolver during validating replay. The accepted live condition optimization and independent-transition validation remain unchanged.

## 5. Performance acceptance: approve 3,950 ms

The primary criterion is:

> **At least 30 isolated warm r104 public restore-through-view samples, with nearest-rank p95 ≤3,950 ms in Default and independently ≤3,950 ms in Fishing Trap.**

Use the accepted r104 files and comparable recorded hardware/runtime conditions. The current environment record identifies the i5-4590, PowerShell 7.6.9 and .NET 10.0.14, with DLL hashes matching the accepted baseline set.

The timer includes file loading, decoding, required copies and checks, full replay, canonical comparison, passage collection, checkpoint creation, adoption and the permitted view. No proof may be prepared outside that timer or reused from a preceding sample.

Retain every raw observation, median, p95 and maximum. Report initial load/startup separately and keep r103, default r223 and Trap r242 as comparison controls. Those longer restores are not automatically subject to the r104 limit.

Use uninstrumented assemblies for acceptance timing. Instrumented receipt/phase counts may demonstrate that the extra derivation disappeared, but they remain diagnostic. Verify unchanged output bytes after every timed restore.

The five-sample baseline component results support the mechanism, but do not guarantee a 665 ms saving in every public run. **A correct implementation that misses 3,950 ms has not met the performance group.** Do not silently adjust the criterion or expand into external-history condition caching to recover the target.

The existing 150 ms routine, 350 ms named stabilization and 2,800 ms selected long-advance criteria are unaffected.

## 6. Required implementation acceptance groups

| Group | Required evidence |
|---|---|
| **1. Complete strict-validation equivalence** | New construction and the retained strict reference accept the same valid states and reject malformed, wrong-profile and checksum-valid altered histories. Every outer receipt is processed, final canonical equality remains mandatory, and no separate sealing replay remains. |
| **2. Passage and ownership correctness** | Preserve first-match, start/completion identity, cutoff and bounded-absence behavior. Exercise a valid early crossing followed by invalid later history, an incomplete crossing that completes after restore, separate origins, repeated loads and policy sharing. No failed attempt produces reusable proof. |
| **3. Public restoration, recovery and continuation** | Both r104 profiles re-encode exactly and continue through actual commands. Compare complete public results and permitted views. Retain pending-work/choice controls, duplicate and revoked-authority behavior, atomic rejected loads, backup rejection/success, authentic prior saves and the established connected checkpoints. |
| **4. Measured improvement** | Meet the **3,950 ms p95** criterion independently in both profiles, with the entire required path timed. Retain maxima, initial loads and longer controls; use correctly separated replay/sealing diagnostics. |
| **5. Exact integration evidence** | Exact source/archive and four-assembly bindings, focused controls, compilation/static evidence, and completed execution of all **1,488 accepted predecessor cases plus the new controls**, using the established loaded-module and ordered-journal provenance. |

The negative-history tests should fail at more than one stage: malformed input, domain/profile mismatch, a later historical failure after a passage has already been collected, and a structurally plausible final-state mismatch. Compare complete live bytes around rejected public restoration and check that the original session remains usable afterward.

Reuse existing authoritative fixtures and recovery controls where they fit. No new gameplay source, fabricated accepted receipt or additional preliminary source/API packet is required.

## Inspection limits and final ruling

I inspected the pinned engineering contract, complete measurement script, baseline/environment reports, proposal diff and source-to-proposal comparison. I also inspected the relevant `Simulation` origin, construction, validation and execution code; the complete existing checkpoint/sealing implementation; and the charter passage predicates and historical assessment path.

**I did not execute the benchmark, independently certify machine isolation, recalculate every sample distribution, load assemblies or binary saves, recompute hashes, modify source or run Unity.** The baseline timings are retained Codex measurements; the proposed improvement remains to be demonstrated.

**Final disposition: authorize this bounded strict-restoration implementation and its proposed 3,950 ms r104 p95 criterion.** The provisional-origin boundary and replay-count distinction above are required implementation and evidence clarifications, not blocking requests to resubmit the design.

Prior acceptances stand. Broader P1 and INT-03 remain open, production authority is unchanged, and Unity gameplay integration stays deferred.
