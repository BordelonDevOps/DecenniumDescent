Actual Unity Rules Engine Development reply `ccf2e0a8-db41-42ea-af82-b15d08828723`, recorded verbatim apart from trailing whitespace.

## INT-03/P1 focused implementation review

**Source:** `e4c5f7f36f9c59b559fc42c6ccf0489c91225999`
**Focused packet:** `3b6459a6081ed656c0ae40a6a520f00686240caf`
**Authorization:** `76a47a76-0d85-4e74-82d0-98a6c2baaa25`

**No source-level blocker found in the bounded charter-submission optimization. No engine change or redesign is required by this review.**

The implementation preserves the authorized trust boundary, and the retained measurements meet the routine submission target. **One narrow evidence-only requirement remains before final acceptance: finish comparing the public response fields omitted by the continuation checker.** Keep the current 1,487-case execution and retained DLLs; that comparison does not require rebuilding or restarting the suite.

## 1. Remaining focused requirement: complete the public-response comparison

`Test-CharterContinuation.ps1` currently compares each accepted and new response’s:

- `Response` and `Revision`;
- `Clock.Numerator` and `Clock.Denominator`.

It does **not** compare `NextSeat`, `PendingDecision`, or `OpportunityPending`. These are actual public result fields, and they appear in the retained implementation transcript. The current checker therefore establishes matching disposition, revision and clock—not complete public-result equivalence. This is a **missing assertion, not an observed behavioral mismatch**.

**Required completion:** compare those additional fields, including field presence, across the corresponding accepted and implementation transcripts for both profiles. For records returning permitted views, compare the gameplay-bearing view payload as well. Any excluded environment-dependent field must be identified explicitly; do not normalize away tactical ownership, pending decisions, visibility or gameplay values.

Use the already retained transcripts. Retain the comparison result and identify its input artifacts. **No engine rerun, new gameplay fixture, changed test inventory or new preliminary source/API packet is required for this evidence check.** The two default and four Trap checkpoint comparisons remain valid evidence; they simply do not substitute for checking every intermediate public projection.

## 2. Source and trust-boundary findings

### Pre-use ownership and byte verification are correctly placed

`Simulation.Execute` still performs current command and authority preflight, duplicate handling and stale/conflict checks before attempting optimized resolution. The optional interface is consulted only afterward. Ordinary policies and unsupported commands retain the existing resolver path.

For the selected charter start, `ResolveNext` checks the owning origin and selected policy state, then compares **both the predecessor and untouched tentative candidate** against the sealed canonical predecessor before supplying the historical fact. This satisfies the earlier requirement that post-resolution verification alone was insufficient for the new earlier use.

The Core interface remains narrow: it carries the existing origin, snapshots and command, without introducing Laboratory charter types or Persistence implementation details into Core.

### The candidate cannot establish its own proof

The independent transition decodes the sealed predecessor, resolves the submitted receipt, encodes the reconstructed successor and compares complete candidate bytes. **Only after that equality succeeds** does it derive `nextPassage` from the independent replay result and construct the successor checkpoint.

That ordering is important because the historical fact is intentionally nonserialized. The implementation does not mistake snapshot-byte equality for validation of a fact supplied by the tentative candidate.

The fact is carried in the checkpoint rather than mutable policy-wide storage. Its receipt identities are copied, and normal rejection paths do not replace the checkpoint. `Simulation` adopts the committed snapshot and successor checkpoint only after successful verification. I found no new shared mutable proof context or exception-cleanup dependency.

### Passage semantics remain equivalent

The implementation preserves the relevant distinctions:

| Property | Source finding |
|---|---|
| Exact scope | The fact checks the content fingerprint and complete terms binding. The binding includes the witness, stage and approach coordinates, authorities, supply identities and authorization interval. |
| Returned passage identity | `StartThrough` returns the accepted start receipt’s revision. |
| Completion cutoff | Eligibility tests the distinct completion receipt against the close-source cutoff. |
| Verified absence | Coverage is bounded by the verified prefix revision; absence is not represented as an unscoped permanent result. |
| First match | Once found, the first start/completion pair is retained while coverage advances. |
| Unavailable optimization | The ordinary reference search remains available when the optional fact does not cover the requested scope. |

These findings follow from `PlanningPassage`, its use in charter basis assessment, and the complete `NextCharterPlanTerms.BindingKey`.

**The removed duplicate traversal-disappearance expression is not a semantic regression.** `AtSalePosition` itself requires the actor to have no world traversal, checks the resolved destination and excludes an active route-travel movement. The extracted completion predicate therefore retains the original disappearance requirement.

The real accepted sequence also provides more first-match coverage than the focused test’s name alone suggests: it contains the initial walk begun at r48, the reverse trip, and another same-direction companion walk begun at r63 after episode close. The retained charter still uses r48. **An additional manufactured repeated-crossing fixture is not required.**

### Strict reconstruction and replacement remain authoritative

Sealing performs the permitted additional derivation pass after initial validation. It stops when the first qualifying crossing is found. Extending that first-match fact’s coverage to the fully validated origin is coherent: later receipts cannot replace an earlier qualifying crossing. An absent crossing requires scanning the available history rather than assuming absence from missing capability.

The session enables the optimization for its existing selected profiles. Restore constructs and validates a replacement before adopting it; recovery likewise validates the replacement through the existing path. The new fact is not loaded from a save or exposed as player-supplied authority.

Direct resolution and strict history replay retain their reference behavior. The change supplies historical passage knowledge, not cached approval of the entire planning command; the existing live charter assessment still executes.

## 3. Performance findings

I inspected both complete 30-row sample files. The reported nearest-rank p95 values are the second-largest observations, as expected for 30 samples, and the reported maxima agree with those rows.

| Measurement | Default | Fishing Trap |
|---|---:|---:|
| Warm public submission plus permitted view, median | 11.2309 ms | 11.8662 ms |
| **Warm public submission plus permitted view, p95** | **12.1105 ms** | **15.3064 ms** |
| Public maximum | 12.1816 ms | 15.8151 ms |
| Ordinary-play accumulated-prefix submission, single sample | 21.7456 ms | 13.1528 ms |
| Strict r74 restore, p95 | 1,541.2675 ms | 1,832.7908 ms |

The live-prefix measurements are individual observations, not additional p95 estimates. The report also retains separate direct-reference reconstruction and resolver timings.

The measurement boundary is appropriate. The timer starts before the actual Player submission and ends after the permitted view. The optimized resolver’s owner checks, byte checks, independent transition and commitment therefore remain inside the measured public operation. Restoration is measured separately. The direct diagnostic probes occur outside that public interval and are not being substituted for the real command.

The script also checks normal-play r74 identity, live-versus-restored r75 identity, repeated sample output identity and the accepted reference output when the reference root is supplied. The retained report and bindings record matching profile-specific live and restored output digests.

**The 150 ms routine charter-submission requirement is met by the retained focused measurements.**

The restore regression is real and remains visible: p95 increased from approximately 972/857 ms to 1,541/1,833 ms. This is the disclosed consequence of choosing the separately derived proof after strict validation. That approach was authorized; it is **not a new blocker for this bounded submission optimization**, and it does not close or improve the separate strict-restore P1 work.

One reporting distinction should remain explicit: the Trap startup observation of 17.21 ms is the second profile in the same process, not a second independent cold-process measurement. The README already makes that distinction despite the shared JSON field name. No implementation change is required for it.

## 4. Focused evidence and the final suite gate

The new focused case exercises separate origins sharing a policy, altered predecessor bytes, altered candidate bytes, bounded absence, late completion, reversed geometry, the wrong witness and changed terms. Its detached predicate inputs are explicitly identified as probes. I am not treating them as executable historical evidence; the actual public histories and live/restored submissions supply the positive integration evidence.

The existing verified-prefix controls additionally cover rejected commands, independent candidate mismatch, ownership substitution, retries, conflicts, stale revisions, external forgery and restoration. Those remain relevant to the unchanged transaction machinery, while the new case covers the added passage capability.

**Full-suite acceptance remains pending.** The focused binding correctly records `regressionCases: null`, and the focused headless report records one executed case—not a completed 1,487-case pass.

For final review, retain the existing required evidence: the exact 1,486 predecessor cases plus the new case, complete successful journals, and the same source/DLL identities bound to the actual shard executions. The launch and retention scripts already provide for inventory checks, execution copies, assignments, process identities and completed-journal binding; their presence is not a substitute for the completed results.

### Final disposition

**The source implementation is acceptable at this focused review. No engine changes are requested.** Complete the evidence-only public-response comparison, preserve the current bound regression execution, and return its completed results for final acceptance.

I inspected the source, retained scripts, reports, both raw timing tables and relevant transcript excerpts. I did not execute the engine, benchmark, tests or DLLs, independently recompute binary/save hashes, or run Unity.

This ruling does not close broader P1, strict restoration, long advances or INT-03 as a whole. Production authority and the deferral of Unity gameplay integration remain unchanged.
