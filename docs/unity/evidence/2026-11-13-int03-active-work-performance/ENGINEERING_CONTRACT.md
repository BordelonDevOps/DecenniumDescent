# INT-03/P1 long active-work advance

Proposal against accepted source `e4c5f7f36f9c59b559fc42c6ccf0489c91225999` and successor ruling `e58e03d6-6dff-4767-b60d-b661bbcb9b2b`. The selected workload is `i-94`, the real `AdvanceClock` of 15,421 seconds after starting `formula.103`. The default and opted-in Fishing Trap profiles use the same accepted command at r103. [Successor decision](../2026-11-12-int03-charter-performance/GPT_FINAL_REVIEW.md)

## Accepted behavior and measurement

The real command commits r104 and moves the shared clock from 26775/2 to 57617/2. Research starts Working at zero labor, earns 30825/2 seconds through its actual work window, and pauses at 28800. The remaining 17/2 seconds advance the calendar without crediting work. RNG stays at 1891099109. Each public path independently resolves the proposed receipt against the sealed prefix. The retained pre/post saves identify the exact state for both profiles. [Baseline and output identities](baseline/results.json)

| Phase | Default median / p95 ms | Fishing Trap median / p95 ms |
| --- | ---: | ---: |
| Public submission through permitted view | 3358.27 / 3631.09 | 3369.80 / 3605.75 |
| One direct resolver pass | 1616.42 / 1764.68 | 1671.83 / 1758.72 |
| Core shape checks | 0.85 / 6.00 | 0.79 / 1.22 |
| Profile checks outside the history callback | 1.47 / 2.81 | 1.38 / 2.43 |
| One snapshot copy | 0.14 / 0.21 | 0.11 / 0.16 |
| One encode | 4.87 / 6.27 | 4.52 / 8.13 |
| Permitted view | 0.38 / 0.72 | 0.41 / 1.11 |
| Strict r103 restore | 2614.70 / 3108.17 | 2624.95 / 2743.13 |

Each profile has 30 warm samples with nearest-rank p95. Public maxima were 3892.13 and 3653.28 ms. Each sample restores the same actual r103 before the timed command and requires identical r104 bytes. Separate diagnostics use a temporary instrumented LabModel built from the accepted sources. This is a single diagnostic observation per profile and execution mode, with overlapping timers. The diagnostic public runs produced the same canonical bytes as the uninstrumented run. [Raw timings](baseline/results.json) · [Diagnostic phase counts](diagnostic/results.json)

The instrumented direct resolver visits 2,570 segments. The public path visits 5,140 because it independently resolves the command twice. The direct default pass spends about 1,749 ms in the scheduler. Selection takes 202 ms, inventory/work 379 ms, settlement 1,155 ms, and actual formula credit 37 ms. One direct pass invokes the journal restore/projection path 177,378 times and spends 682 ms inside it. That time overlaps the scheduler phases. The Trap profile has comparable costs. Copying and encoding are small relative to scheduler execution.

## Proposed correction

Reuse immutable condition journal reconstruction inside one qualified resolver pass. The same journal instance and interpretation policy yield the same reconstructed immutable base ledger. For `ConditionsFor`, reuse the projected immutable ledger only for the exact current `EffectClockMarker`, including its phase. One most-recent projected ledger per journal is sufficient. A different journal identity or marker requires recomputation. A replacement journal created by a condition operation is a miss. The native deadline code still examines every current journal and appends the same transitions with the same clock, ordering and subevent IDs.

Keep the existing calendar loop and every segment boundary. Preserve all worker activity, ordinary and tactical timing, conditions/immunities, current sight and capabilities, spoilage/protection, due checks, fishing, remote work, RNG order, pending choices and receipts. Use a fresh isolated scope for each tentative or independent resolver pass. No reuse crosses the boundary between them. Never place a cached ledger in snapshots, receipts, proof fields or process-wide retained storage. Scope entry and disposal must preserve nested execution and clear references on exceptions. Use an explicit scope where practical. If reaching existing condition helpers requires an ambient pointer, constrain it to synchronous thread-local stack scope and restore the previous value in `finally`. Unsupported callers, external validation and the strict reference retain the existing path.

Start with the two selected session profiles and ordinary long active formula-research advances. Gate using actual selected profile, command kind, ordinary mode, and active research state, with no dependency on the recorded command ID or revision. Keep the same event and check logic for any simultaneous supported work. If a combination cannot be demonstrated safe under exact journal/marker identity, retain the reference. No new broad condition semantics, persisted cache or clock jump is proposed. The related research and manufacturing advances remain comparison and regression controls.

## Acceptance proposal

- Require isolated warm **p95 at or below 2,800 ms in each profile** for the same single public `i-94` input, with at least 30 samples and full command, independent verification, commitment and permitted view in the timer. This is about 22% below the slower observed baseline and is conservative against the measured repeated reconstruction cost. Keep the 150 ms routine target and separate 350 ms stabilization allowance. Report maxima, live accumulation and strict restoration separately.
- Preserve the exact r103/r104 bytes, full public results and subsequent accepted route with the same pending/save/restore checkpoints. Compare segment counts, endpoints, labor, expiry and journal operation identities. Exercise source journal replacement, equal/different markers, nested and failed scope cleanup, and separate resolution passes. Retain representative cases with meaningful condition expiration and due work, with current supported reference fallback where applicable.
- Retain exact source, build, focused and bound full regression evidence for review. Strict external reconstruction and the added charter proof derivation remain under the later restoration gate. Unity gameplay integration stays deferred.
