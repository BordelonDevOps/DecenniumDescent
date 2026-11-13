Actual Unity Rules Engine Development reply `5f3a0190-5c09-466b-9ce1-e9b888c24b7e`, recorded verbatim apart from trailing whitespace.

## INT-03/P1 long active-work advance — approved for bounded implementation

**Reviewed proposal:** `dae4d183ff967b62e9fe6810fe00db624f230eb2`
**Accepted reference implementation:** `e4c5f7f36f9c59b559fc42c6ccf0489c91225999`
**Controlling successor ruling:** `e58e03d6-6dff-4767-b60d-b661bbcb9b2b`

**Approve the proposed per-resolver condition reconstruction cache for the two selected sessions, under the requirements below. Approve the proposed 2,800 ms public p95 criterion for this first long-work workload. No blocking source/API question remains, and no additional preliminary packet is required.**

The source-to-proposal comparison contains documentation and evidence changes only. This authorizes reuse of immutable calculations **within one isolated resolver execution**. It does not authorize skipping calendar segments, caching gameplay eligibility, sharing tentative work with independent verification, or optimizing external restoration.

## 1. The baseline supports this target

The retained report identifies the actual `i-94` command at r103 and its canonical r104 result in both profiles. It advances the clock from **`26775/2` to `57617/2`**, credits **`30825/2` seconds** to research, and leaves the job Paused. The last **`17/2` seconds** advance the calendar after the work-window boundary without crediting research. RNG remains `1891099109`.

| Baseline measurement | Default | Fishing Trap |
|---|---:|---:|
| Public submission through permitted view, p95 | **3,631.089 ms** | **3,605.746 ms** |
| One direct resolver pass, median | 1,616.425 ms | 1,671.825 ms |
| Strict r103 restore, p95 | 3,108.167 ms | 2,743.131 ms |

The benchmark reconstructs the actual history, measures a live accumulated-prefix submission, and then performs 30 warm restored submissions after a warm-up. The public timer includes `SubmitSessionCommand` and the permitted Player view; restoration and diagnostic probes are separate. Each sample must reproduce the same canonical successor.

The instrumented observations provide a credible reason to investigate condition reuse: **2,570 segments per direct resolver pass, 5,140 during public submission**, and approximately **177,378 visits to the condition restoration/projection helper per direct pass**. The measured helper time is approximately 672–682 ms per pass.

**That timing is not a guaranteed recoverable saving.** The probe surrounds the restoration-and-projection helper, not only `ConditionHistory.Restore`; its time overlaps the larger scheduler phases and includes instrumentation overhead. The diagnostic script checks the instrumented public result against the uninstrumented canonical output, which supports using these observations for diagnosis—not as the final performance measurement.

## 2. Approved cache contents and invalidation

The inspected journal, history and ledger APIs support the proposed approach. `ConditionJournal` copies its operations into a read-only collection, condition changes produce replacement journals, and ledger transitions return new states rather than mutating the original ledger.

Approve two narrowly separated cached values:

| Cached value | Required identity and behavior |
|---|---|
| **Reconstructed base history/ledger** | The actual immutable journal object and its supported interpretation policy. A different journal object is a miss, even when actor, time or operation count match. |
| **Read-only projected ledger** | That base journal identity plus the exact requested `EffectClockMarker`, including phase, and the applicable projection mode. One most-recent projected value per journal is sufficient. |

### Preserve the current projection rule exactly

`ConditionsFor` currently reconstructs the journal, returns the base ledger for older nonprojecting schemas, and otherwise advances a read-only projection only when the base ledger’s marker precedes the requested marker. Preserve that distinction.

On a projection miss, calculate from the **base reconstructed ledger**, not by advancing the previously cached projection. The latter could incorrectly preserve expiration from a later marker when another legitimate calculation asks about an earlier marker or a different phase.

Do not key by actor ID, rounded seconds, world-slot number, revision or operation count alone. Do not treat equal timestamps with different phases as equal markers.

A replacement journal created by Apply, Cure, suppression, immunity, expiry or another condition operation must be observed on the next lookup. Do not reuse the old value because the replacement retains the same actor or clock.

### Cache calculations—not decisions

The scope may reuse the immutable history/ledger needed by existing helpers. It must **not** cache composite results such as current capability, available hands, movement permission, target visibility, worker eligibility or command admission using only the journal/marker key.

Those results also depend on live state outside the condition journal. For example, the existing condition code combines ledger clauses with actor life, Action/movement expenditure, surprise restrictions and strain. Those inputs must still be evaluated where they are currently evaluated.

Unsupported policies, malformed journals and invalid operations must retain their existing failures. A cache miss is not permission to suppress an exception or substitute an empty condition set.

## 3. Keep projected state separate from authoritative condition transitions

**This is the most important semantic boundary.**

The scheduler’s deadline queries must continue to examine the current authoritative journals and their reconstructed **base** ledgers. They must not consult a projected ledger that has already marked a condition or immunity expired and then conclude that no journaled expiry is due.

The existing implementation separately:

- finds condition deadlines;
- projects conditions for current decisions;
- appends authoritative clock/condition operations;
- commits resulting world consequences.

That separation must remain intact.

`ConditionHistory.Restore` deliberately reconstructs historical state without returning old consequences as pending work. Conversely, a new `Append` produces a new transition whose current consequences must be committed once. **Do not replay cached historical consequences, discard a newly due consequence, or reuse an operation result merely because its inputs resemble an earlier operation.**

The unchanged calendar must still visit and settle the same boundaries. Preserve expiry phases, journal operation IDs, subevent numbering, work-window pauses, personal allowance refreshes, remote work, spoilage/protection, fishing checks, pending choices and tactical yields. The existing scheduler explicitly orders these operations; the cache does not acquire authority to reorder them.

For the measured command, **2,570 segments per resolver pass remain the reference**. This increment reduces repeated calculations inside those segments; it is not a segment-coalescing optimization.

## 4. Resolver scope and reference-path requirements

### Limit selection to the approved live path

Select the optimization from the actual supported profile and command state: the default or opted-in Fishing Trap session, an ordinary `AdvanceClock`, and an actual working formula-research project.

Do not recognize the benchmark by command ID `i-94`, revision 103, a particular duration, RNG value or expected result. Those identify evidence, not gameplay eligibility.

The selection guard does not freeze the researcher’s capability or job status. If an event pauses research or changes another actor during the command, subsequent decisions still read the resulting current state.

### Every execution starts with an empty scope

The tentative resolver and the independently reconstructed resolver must each receive a **fresh, separate cache**. Nothing computed by tentative execution may populate or warm the independent pass—even if immutable journal references happen to be shared by a snapshot copy.

Dispose the scope before returning to validation, public views or the next command. Do not retain it in the checkpoint, policy, snapshot, receipt, save file or process-wide lookup.

This optimization is not another verified historical fact. It needs no new proof field, save version, content fingerprint or player-facing switch.

### Explicit context is preferred; a constrained ambient pointer is permitted

The proposed synchronous thread-local stack scope is acceptable if plumbing explicit context through existing helpers would be unnecessarily invasive. Its obligations are:

**Each nested qualified resolver gets a fresh child scope.** It must not inherit the parent’s entries. A nested strict or unsupported call must suppress the outer optimization rather than accidentally using it.

**Every exit restores the previous scope in `finally`.** That includes rule denial, exceptions, early completion, suspension and pending-choice returns. Clear owned references on disposal and keep retained entries bounded; this cannot become an accumulating history cache.

**No asynchronous or cross-thread propagation is included.** The permitted ambient object is only a pointer to the current synchronous scope, not a global reusable cache.

Tests must demonstrate those properties rather than relying on the current single-threaded session lock to conceal leakage.

### Preserve an uncached executable reference

Do not enable the optimization solely because an arbitrary call to the public `Resolve` happens to contain an eligible-looking snapshot. The accepted implementation uses that resolver in several reference contexts. Its public entry and private execution path are already distinct.

Direct reference calls, external validation, full historical reconstruction, queries and unsupported selections must retain their uncached path. The two authorized live resolver passes may use the cache, but their independent decoding, structural/profile validation, canonical comparison and atomic commitment remain required.

**These are implementation requirements within the proposal, not a request for another design submission.**

## 5. Performance criterion — 2,800 ms approved for this workload

Approve **warm public p95 ≤2,800 ms in each profile**, measured with at least 30 samples after a warm-up on the same selected command and comparable isolated environment.

This is a bounded improvement target for the long research advance—roughly a 22–23% reduction from the observed p95 values. **It is not a redefinition of an interactive routine command, a blanket long-command allowance, or closure of broader P1.**

The existing **150 ms routine target** and **350 ms named stabilization allowance** remain unchanged.

The acceptance timer must include scope creation, all cache misses and maintenance, tentative execution, independent execution, normal validation and canonical comparison, commitment, and the permitted view. No prewarming from a query, prior resolver pass or restored cache is allowed.

Use the ordinary uninstrumented implementation for the performance gate. Retain all raw samples, median, p95 and maximum; report startup, live accumulated-prefix execution and strict restore separately. Instrumented hit/miss and reconstruction counts may explain the result, but must remain diagnostic.

The current schema-validation probe with an empty history callback remains **measurement-only instrumentation**. It is not an authorized shortcut in the actual submission.

A correct implementation that misses 2,800 ms has not met this performance group. Do not relax the criterion afterward or broaden the optimization without reviewing the reason.

## 6. Implementation acceptance groups

| Group | Required evidence |
|---|---|
| **1. Immutable reuse and invalidation** | Base and projected outputs match the uncached reference. Exercise replacement journals at the same time, equal/different markers and phases, expiry/immunity changes, unsupported interpretation and preserved exception behavior. Prove that projection is recomputed from the base on a miss. |
| **2. Scope and transaction isolation** | Separate tentative/reference caches; nested qualified and strict calls; exception and early-return cleanup; independent sessions; rejection followed by a valid command; no retained cache in snapshots, checkpoints or subsequent commands. |
| **3. Exact gameplay equivalence** | Preserve r103/r104 canonical bytes, complete public results/views, ordered segment boundaries and condition operations, labor, pause, clock and RNG. Continue both accepted routes and retain their existing save checkpoints. Include meaningful condition expiry and supported simultaneous work, not only an unchanged-condition benchmark. |
| **4. Measured improvement** | Meet **2,800 ms p95 independently in both profiles**, with the full required path timed and all samples retained. Show reduced reconstruction work without reducing calendar segments or independent execution. Report the related research/manufacturing advances as controls, not silently expanded scopes. |
| **5. Persistence and exact execution** | Authentic saves and backup/restore behavior remain unchanged; altered histories still reject atomically. Retain exact source/assembly identities, compilation/static checks and the completed bound regression containing all **1,487 accepted predecessors plus the new controls**. |

For meaningful condition/work cases, reuse existing admitted procedures and fixtures. An optimized combination must receive evidence that its due behavior is preserved; otherwise it remains on the strict fallback. Detached cache/predicate probes may supplement this and should be labelled accurately—they do not replace executable chronology.

Full transcript comparison must include field presence and all gameplay-bearing public values, not only revision, clock or final-state hashes. Likewise, matching segment counts alone is insufficient: retain enough ordered boundary and event evidence to establish that the same events occurred in the same order.

## Inspection limits and final ruling

I inspected the engineering contract; complete measurement and diagnostic scripts; temporary instrumenter; baseline and diagnostic reports and recorded diagnostic assembly identities; the source-to-proposal comparison; `ConditionJournal`, `ConditionHistory`, `ConditionLedger` and `ConditionCombatPolicy`; and relevant shared scheduler, research and resolver-entry code.

The instrumentation uses a temporary LabModel copy, and its public diagnostic outputs match the recorded uninstrumented baseline digests. **I did not execute that instrumentation or benchmark, independently certify isolation, recalculate every percentile, load assemblies or saves, recompute artifact hashes, modify source or run Unity.** This approves a technically supported implementation plan, not an unimplemented speedup.

**Final disposition: authorize the bounded per-resolver condition-reuse implementation under this contract, including the proposed 2,800 ms first-workload p95 target. No additional preliminary source/API packet is required.**

Strict-restoration optimization remains the separate next P1 engineering gate. Prior acceptances stand; broader P1 and INT-03 remain open, production authority is unchanged, and Unity gameplay integration stays deferred.
