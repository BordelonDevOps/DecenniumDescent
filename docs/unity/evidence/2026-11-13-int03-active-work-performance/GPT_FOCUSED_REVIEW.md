Actual Unity Rules Engine Development reply `740bfffe-69a5-4752-ad88-5ede0606c31f`, recorded verbatim apart from trailing whitespace.

## INT-03/P1 long research advance — focused requirements met

**Reviewed source:** `26854d6f49842ae3ea40536d96cc102bc2896e24`
**Reviewed evidence:** `eaacf4f0eac17ecf5b8b13ef37f78a1003defdea`
**Controlling contract:** `5f3a0190-5c09-466b-9ce1-e9b888c24b7e`

**Groups 1–4 are met on the inspected source and focused evidence. Group 5’s connected, persistence and build portions are supported. I found no concrete blocker and request no source correction or additional focused scenario. Final acceptance remains held solely for E1: the completed exact-bound 1,488-case regression.**

The implementation-to-evidence comparison contains one documentation/artifact commit and **no subsequent engine or console-source changes**. Continue the current bound execution; no rebuild or restart is requested.

## 1. Disposition against the five groups

| Approved group | Focused verdict |
|---|---|
| **1. Immutable reuse and invalidation** | **Met.** Exact journal identity, separate base history, phase-aware projection and recomputation from the base preserve the selected calculation semantics. |
| **2. Scope and transaction isolation** | **Met.** Each selected resolver invocation creates its own scope; strict entry suppresses an outer scope; disposal restores the previous context. Independent verification does not reuse the tentative cache. |
| **3. Exact gameplay equivalence** | **Met.** The accepted research result, ordered calendar boundaries, complete public transcripts and connected checkpoints agree. The additional expiry/work comparison supports the shared helper behavior without claiming standalone optimization. |
| **4. Measured improvement** | **Met for the selected workload and both profiles.** The retained uninstrumented p95 values are below the agreed **2,800 ms** limit. |
| **5. Persistence and exact execution** | **Focused portion met; E1 pending.** Authentic restoration, atomic forged-history rejection, compilation/static evidence and exact bindings are retained. The full run is not yet claimed complete. |

## 2. Cache contents and lifetime preserve the trust boundary

### Exact identity, bounded retention and separate projection

`ConditionResolutionScope` keys entries by **reference identity of the immutable `ConditionJournal`**, not actor name, revision, operation count or structural similarity. A replacement journal receives a new reconstruction. Its reconstruction still passes through the existing `ConditionHistory.Restore`, including interpretation-policy validation.

Each entry holds the base `ConditionHistory` and at most one projected ledger. A projection miss uses:

```csharp
At(entry.History.Ledger, marker)
```

It does **not** advance the last cached projection. Consequently, requesting an earlier marker after a later projection cannot carry a later expiration backward. `EffectClockMarker.Equals` also preserves the phase distinction. The nonprojecting path returns the base ledger. Retention is bounded to 32 journal entries, with clearing on capacity and scope disposal.

The new focused case directly exercises journal replacement, repeated exact-marker reuse, a different phase, returning to an earlier marker, and preserving the base ledger’s unexpired state. It also checks nested strict suppression, a fresh nested qualified scope and restoration of the parent after an unsupported-policy exception.

### Deadline and append operations remain authoritative

The changed deadline and append paths use `ConditionResolutionScope.Read(journal).Ledger` or the returned base history’s existing `Append`. They do not use the projected ledger as the authoritative journal state.

This preserves the important distinction: a read projection may show that Poisoned has expired at a requested marker, while the scheduler must still append the actual due condition transition with its original clock, operation identity and consequences. The underlying condition interpreter and transition methods are unchanged.

The cache does not store composite permissions, available hands, sight eligibility or worker admission. Those calculations continue to combine the current condition result with the other live state they already use.

### Selected execution and independent replay remain separate

The scope is entered at the private resolver boundary only when the execution is explicitly verified and the existing selection predicate finds an ordinary `AdvanceClock` with working research in the selected policy. It does not recognize `i-94`, r103, the benchmark duration or an expected outcome.

Direct calls use the default `verifiedExecution: false`. A strict nested resolver suppresses any outer scope. The lexical `using` covers early returns and exceptions and disposes the scope before returning to verification.

The checkpoint still checks owner and sealed predecessor/candidate bytes before optimized resolution. Its independent path decodes the sealed predecessor and invokes the resolver again, creating a **new scope**, then compares the complete canonical successor. The condition cache is neither a checkpoint field nor a serialized proof.

I found no cross-pass cache sharing, new persisted state or change to the existing atomic adoption boundary.

## 3. Calendar, condition and concurrent-work evidence is sufficient

### The accepted research result is unchanged

Both profiles retain the same r103/r104 identities and the following actual outcome:

| Fact | Retained result |
|---|---|
| Shared clock | `26775/2 → 57617/2` |
| Research | `Working → Paused` |
| Credited labor | `0 → 30825/2` seconds |
| RNG | `1891099109`, unchanged |
| Public commitment | r104 |

The work-window pause remains distinct from the remaining elapsed time after that boundary. No extra research labor or check is introduced.

### Reduced reconstruction does not reduce calendar execution

The instrumented reference and candidate retain **2,570 boundaries per direct resolver pass and 5,140 per public submission**. The retention script compares the complete ordered boundary files byte-for-byte, rather than checking counts alone.

The diagnostic public reconstruction counts change from **431,891 to 35** for Default and **431,893 to 37** for Fishing Trap. The candidate’s direct uncached reference still records **215,933 reconstructions per profile**. Thus the evidence supports removing repeated reconstruction—not omitting the second resolver or skipping calendar segments.

The instrumenter modifies a temporary source copy and records the scheduler’s ordered boundaries and reconstruction calls. Its loaded-run timings are diagnostic, overlapping measurements; **they are not the performance acceptance samples**. I inspected the instrumentation and comparison logic, but did not independently compare every boundary-file line.

### The expiry witness is correctly bounded

`Test-AdvanceConditionChronology.ps1` first creates a genuine admitted standalone history: dispatch timed Poisoned, start real formula research, and start ordinary intake. It then compares uncached and explicitly scoped `ResolveCore` execution of detached copies of that same admitted predecessor.

The retained result records **500 seconds of research**, completed intake and these actual condition operations:

```text
event.work.poison at 0/1
host.clock.4.2 at 20/1
host.clock.4.4 at 500/1
```

The scoped and strict canonical digests agree. The recorded post-save digest agrees with that result as well.

**This is supporting detached resolver-equivalence evidence, not a claim that the standalone production dispatch has been opted into caching.** The script explicitly invokes the shared core under a controlled scope for that comparison; its ordinary `Simulation.Execute` remains on the reference path. That distinction is correctly stated in the packet.

Combined with the selected-profile public histories and unchanged scheduler, this satisfies the focused condition/work requirement. No artificial connected poison command or additional fixture is requested.

## 4. Performance criterion is met

I inspected both complete 30-row uninstrumented sample files. Their reported nearest-rank p95 and maximum values agree with the second-highest and highest public observations, respectively. No outlier was removed or pooled across profiles.

| Measurement, milliseconds | Default | Fishing Trap |
|---|---:|---:|
| Public median | 1,657.917 | 1,646.414 |
| **Public p95** | **1,807.036** | **1,731.607** |
| Public maximum | 1,851.900 | 1,733.118 |
| Agreed p95 limit | 2,800 | 2,800 |
| Live accumulated-prefix submission, single observation | 1,794.435 | 1,672.819 |
| Strict r103 restore p95, separately measured | 2,771.247 | 2,694.022 |

The live-prefix figures are single observations, not additional p95 distributions. The public measurements include submission and the permitted view; canonical output is checked against the accepted baseline for each profile. Direct resolver and validation probes remain separate diagnostics.

**Group 4 is met under the existing 2,800 ms criterion.** No threshold change or additional timing run is requested for this bounded item.

This does not turn a roughly 1.7–1.8-second operation into a routine sub-150 ms command, or establish performance for every long advance. The existing **150 ms routine** and **350 ms named stabilization** criteria are unchanged. Strict restoration remains uncached and separately tracked; its observed timing variation here is not acceptance of a restoration optimization.

## 5. Full public continuation and persistence are retained

The current continuation verifier first requires the **raw SHA-256 of each complete console transcript** to equal its accepted charter-performance reference. That covers all intermediate results and permitted views, not only revision/clock fields. It then checks the existing saved checkpoints and authentic predecessor round trips.

For the Trap profile it also attempts the accepted forged-history restoration, requires rejection, and compares complete live-save hashes before and afterward.

The retained report records:

| Profile | Console inputs | Committed actions | Matching connected checkpoints |
|---|---:|---:|---:|
| Default | 277 | 223 | 2 |
| Fishing Trap | 322 | 242 | 4 |

The two final digests remain the accepted default and Trap continuations, respectively:

```text
90d28e236200e017267f367f20d244f3df2223a355f09b1ebec5ac35ae491e41
14add8d9963d41cbdec7433254413fc095499f1ad02086065608acdc14dda712
```

The complete transcript digests also remain unchanged. **I compared the recorded identities and checking logic; I did not independently hash the transcripts or replay the histories.**

## 6. Builds and the sole remaining E1

The focused report records **one discovered case, one pass and zero failures** for `int03_active_work_condition_scope_isolation`. The separate standalone C# 9 report passes Core, Persistence and LabModel. Static validation records **18/18 passing checks, 397 assets and 397 unique GUIDs**. These are retained Codex executions I inspected—not executions I performed—and do not establish Unity validation.

The packager binds compilation inputs to the implementation archive and retains the four focused DLLs, connected evidence, timing files, expiry comparison and ordered boundary evidence. The manifest correctly leaves `regressionCases` null.

**E1 requires the already-running exact-bound 1,488-case execution:** the ordered **1,487 accepted predecessor names plus this one new control**, all passing, with the established launch/start/completion, assignment, loaded-assembly and journal bindings. The new case is included in 1,488, not additional to it. The launcher and finalizer preserve that requirement.

No replacement focused witness, redundant regression or new source/API proposal is requested.

## Inspection limits and final disposition

I inspected the complete implementation diff and new focused test; the complete condition-scope and verified-checkpoint implementations; the chronology, continuation, instrumentation, retention and regression-launch scripts; both complete raw timing tables; the performance, ordered-reference/candidate, expiry and connected reports; build/static summaries; bindings; and the source-to-evidence comparison.

**I did not execute scripts or tests, compile, load DLLs or binary saves, certify machine isolation, recompute artifact hashes, read every transcript or ordered-boundary line, modify repository files or run Unity.** The recorded executions and exhaustive hash checks remain Codex’s evidence.

**Final focused disposition: no concrete correction required. Groups 1–4 and the focused portions of group 5 are met. Hold final acceptance of `26854d6f49842ae3ea40536d96cc102bc2896e24` solely for completed E1.**

Prior acceptances stand. Strict-restoration engineering remains separately gated after actual acceptance; broader P1 and INT-03 remain open, production authority is unchanged, and Unity gameplay integration stays deferred.
