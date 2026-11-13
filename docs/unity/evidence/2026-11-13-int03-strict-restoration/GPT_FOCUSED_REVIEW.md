Actual Unity Rules Engine Development reply `5aecdef8-9301-4d50-a863-e36c394fbe61`, recorded verbatim apart from trailing whitespace.

## INT-03/P1 strict restoration — focused requirements met

**Reviewed source:** `75872e1e01fea9b17fce0c5c6c34d56679848961`
**Reviewed evidence:** `7b1a4c3d8fe2db46f750d30b05454e9eab4ef585`
**Controlling contract:** `7eb9c90e-b182-464e-863f-01561c9d5cf9`

**No concrete source-level blocker found. Groups 1–3 are met on the inspected source and focused evidence. I accept the complete repeat as satisfying group 4’s bounded, per-run timing criterion, with the first-run failure retained explicitly. Group 5’s focused portions are supported; final acceptance remains held solely for the completed exact-bound 1,489-case regression.**

**No source correction, additional focused scenario or further timing run is requested for this increment.** The timing qualification below is important: this is not a claim of consistent compliance across both runs or completion of broader P1.

The source-to-evidence comparison contains one documentation/artifact commit and no subsequent engine or console-source changes.

## 1. Construction preserves the validation and ownership boundary

### Core creates the real origin only after validation succeeds

The selected constructor branch retains structural validation before copying, detaches the input, and performs Core shape/content-scope checks on that owned candidate. It selects the new capability only for verified-prefix Laboratory construction with the trusted TEST_ONLY policy.

`ValidateForConstruction` must return successfully before Core creates `VerifiedSimulationOrigin`. A missing factory or a factory that cannot establish the checkpoint throws; there is no fallback that treats failed selected validation as an unsupported optimization. The ordinary `FullReplay` branch and legacy sealing path remain executable.

This implements the approved success boundary without prematurely making an unvalidated origin usable.

### The passage observes replay without authorizing replay

`ReconstructCanonicalHistory` begins from `Initial()` and processes every receipt in revision order. It calls:

```csharp
ReplayReceipt(replay, receipt)
```

without supplying the collected passage or enabling verified execution. Historical charter assessment therefore remains on its original reference path, and condition execution remains uncached during external reconstruction.

The provisional passage observes the before/after transition. Its output and the canonical byte output remain unset until the full replay finishes and the complete reconstructed state matches the incoming candidate. Finding the first crossing does not terminate validation or excuse a later invalid receipt.

### The factory seals the exact validated state

The returned factory captures the successful canonical bytes and passage. Before constructing a checkpoint, it captures the actual new origin and checks both passage coverage and complete byte equality.

The checkpoint then retains the existing origin-identity, fingerprint, predecessor-byte, receipt-extension and independent-transition checks. No persisted proof, policy-wide “last validated state,” or cross-load cache was added. The passage’s first-match, start/completion and cutoff methods remain unchanged.

I found no route in the selected implementation that adopts a provisional passage after failed history validation.

## 2. The diagnostic counts demonstrate the intended removal

The retained instrumentation separates the three kinds of replay work correctly:

| Replay category, both profiles | Accepted reference | Candidate |
|---|---:|---:|
| Outer validating receipt visits | 104 | 104 |
| Nested historical charter-search visits | 49 | 49 |
| Dedicated post-validation sealing visits | 49 | 0 |

The candidate and reference diagnostic reports retain the same profile-specific r104 canonical identities. The instrumenter counts the outer validator, nested charter search and old sealing loop at separate source locations.

**The optimization removes the dedicated sealing replay—not the required validation and not the historical charter reference search.** It would be inaccurate to describe the total reconstruction as only 104 resolver calls.

The `SealMs`/reference-seal diagnostic still invokes the old method outside the public-load timer. Its presence in a report does not imply that the optimized restore performs that extra replay.

## 3. Focused restoration, rejection and continuation evidence is supported

### Actual partial movement and independent continuation

The new registered case runs both profiles through an actual partial ordinary movement, saves it, restores it twice and continues it. It compares complete canonical state among the live session, restored session and uncached `FullReplay` reference.

It also exercises an exact duplicate, an encodable altered-RNG save, a revoked Player grant across rejection, byte-identical live state after failure, and subsequent usability of the original receipt/checkpoint. The recorded focused execution is one discovered case, one pass and zero failures—not a completed full-suite result.

### Negative loads fail at distinct stages

The public r104 rejection verifier does more than corrupt a checksum. It constructs separate malformed, cross-profile, later-receipt and final-state cases, then requires rejection, preserved Player revocation and identical complete live-state hashes.

The retained results distinguish:

| Negative input | Recorded failure |
|---|---|
| Malformed file | `Invalid save length.` |
| Other selected profile | `Content fingerprint or scope mismatch.` |
| Invalid late receipt | `InvalidSharedWorldHistory` |
| Structurally encodable altered final RNG | `InvalidSharedWorldReplay` |

Both historical failures occur after the history has passed the point containing the qualifying crossing. This directly supports the requirement that an early collected fact cannot authorize a bad later history or mismatching final state.

The recovery controls require an invalid backup to leave the primary, backup and current grant unchanged. Successful recovery preserves the accepted backup, replaces the primary with the accepted bytes, retains the displaced primary and leaves the original committed clock receipt idempotent. These are retained verifier results; I did not independently perform the file operations.

### Complete public histories remain equal

`Test-RestoreContinuation.ps1` first requires whole-file transcript hash equality with the accepted public histories. That check covers all response fields and permitted views—not merely the later selected-field loop.

The packet retains the Default **277-row/223-command** history and Fishing Trap **322-row/242-command** history, all six accepted checkpoints, authentic-save round trips and complete live-byte equality around forged restoration rejection.

**I compared the recorded identities and verification logic. I did not independently recompute transcript or save hashes.**

## 4. Timing ruling: accept the repeat, preserve the failed run

I inspected all four raw 30-sample files. Their p95 values agree with the nearest-rank definition used by the measurement script: the 29th ordered observation for 30 samples.

| Run | Default p95 / maximum | Fishing Trap p95 / maximum | Against 3,950 ms |
|---|---:|---:|---|
| First complete run | **4,330.263 / 5,079.605 ms** | **3,715.552 / 3,938.162 ms** | Default fails; Trap passes |
| Complete same-DLL repeat | **3,851.091 / 3,939.597 ms** | **3,626.773 / 3,817.534 ms** | Both pass |

The first Default distribution contains **four observations above 3,950 ms**. The repeat contains none. Those are distinct experimental outcomes; the second run does not retroactively convert the first into a pass.

### Explicit disposition

**The complete repeat satisfies the agreed bounded criterion: an isolated 30-sample warm public run meeting p95 ≤3,950 ms independently in both profiles. No additional measurement is required for this implementation gate.**

That acceptance is deliberately limited:

- The first Default miss remains part of the record, with no discarded samples.
- I am **not** claiming a pooled 60-sample Default pass. Combining the two retained Default distributions gives nearest-rank p95 **4,105.871 ms**, above the threshold.
- The cause of the run-to-run variation is not established by this packet. It should not be attributed confidently to operating-system load, warm-up, garbage collection or the implementation without evidence.

The agreed gate did not specify a pooled multi-run criterion or require every independent run to pass. I am not adding either requirement retrospectively. Equally, the successful repeat is not evidence of a stable tail-latency guarantee across all runs and environments.

### The measured boundary remains correct

The timer includes the actual public `Restore` and a permitted Player view. Every sample then saves and checks the complete accepted r104 bytes. It does not reuse a proof from the preceding load or time only the factory. The component probes and old `Seal` invocation occur afterward, outside that public interval.

The repeat separately records first loads of approximately **4,494 ms Default** and **3,449 ms Trap**. The Trap profile is second in the same process, not a separate cold-process measurement. Longer r223/r242 controls remain approximately **6.67/6.65 seconds**. These costs remain visible and do not become covered by the r104 criterion.

**Group 4 is met for the bounded measured repeat. Broader restoration responsiveness and timing variability remain open under P1.**

## 5. Acceptance groups and remaining E1

| Group | Focused disposition |
|---|---|
| **1. Complete strict-validation equivalence** | **Met.** Full uncached reconstruction and canonical equality remain mandatory; only the separate sealing replay is removed. |
| **2. Passage and ownership correctness** | **Met.** The passage remains provisional during validation, preserves its existing semantics, and is sealed only to the validated origin bytes. |
| **3. Public restoration, recovery and continuation** | **Met.** Actual continuation, distinct negative loads, complete public transcript equality, recovery controls and accepted saves are retained. |
| **4. Measured improvement** | **Met on the complete repeat**, with the first-run failure and variability qualifications above. |
| **5. Exact integration evidence** | **Focused portion met; E1 pending.** The exact unfiltered execution is still running. |

The separate standalone C# 9 report passes Core, Persistence and LabModel. Static validation records **18/18 passing checks, 397 assets and 397 unique GUIDs**. These are Codex’s retained executions I inspected, not executions I performed, and they do not establish Unity validation.

The finalizer retains both timing distributions and requires the completed regression to contain the unchanged **1,488 accepted predecessor names plus `int03_strict_restore_constructs_fresh_owned_prefix`**, for **1,489 total**. Its launch/start/completion, loaded-assembly, assignment and journal checks remain in place. The focused manifest correctly leaves `regressionCases` null.

**Continue the current bound run. No rebuild, restart, replacement scenario or redundant regression is requested.**

## Inspection limits and final disposition

I inspected the complete four-file implementation diff and new focused case; the complete checkpoint/factory code; Core’s constructor and shape-validation branch; the reconstructed-history path; the measurement, instrumentation, rejection/recovery, continuation and retention scripts; both timing reports and all four raw sample files; replay-count reports; rejection results; build/static summaries; bindings; and the source-to-evidence comparison.

**I did not execute tests or scripts, compile, load DLLs or binary saves, independently replay either public history, recompute artifact hashes, certify machine isolation or modify repository files.** The reported executions and exhaustive source/artifact checks remain Codex’s evidence.

**Final focused disposition: no concrete correction required. Hold final acceptance of `75872e1e01fea9b17fce0c5c6c34d56679848961` solely for completed E1.**

Prior acceptances stand. This does not close broader P1 or INT-03, authorize a successor, promote production authority or change the deferral of Unity gameplay integration.
