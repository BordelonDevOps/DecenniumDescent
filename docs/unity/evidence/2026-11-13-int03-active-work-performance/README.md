# INT-03/P1 long research advance

Source `26854d6f49842ae3ea40536d96cc102bc2896e24` on `Engine` follows the [engineering contract](ENGINEERING_CONTRACT.md) and [actual GPT authorization](GPT_ENGINEERING_REVIEW.md). Each verified resolver pass for ordinary active research starts a fresh bounded condition scope. It reuses immutable journal reconstruction by exact object identity and a read-only projection by exact marker. Deadline and append operations read the base journal history. The scheduler and its event order remain intact.

| Profile | Baseline p95 | Optimized p95 | Optimized max | Live prefix sample | Strict r103 restore p95 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default | 3631.09 ms | 1807.04 ms | 1851.90 ms | 1794.43 ms | 2771.25 ms |
| Fishing Trap | 3605.75 ms | 1731.61 ms | 1733.12 ms | 1672.82 ms | 2694.02 ms |

The 30 warm uninstrumented public samples per profile use the same approved r103 command and exact r104 outputs. Restore is timed separately. The 2,800 ms target applies to this selected long advance. The direct resolver remains uncached and supplies the reference timing and behavior. The earlier standalone candidate run also met the target. [Exact timings](performance/results.json) · [Baseline](baseline/results.json)

The separate instrumented reference and candidate each visit the same ordered 2,570 boundaries per pass and 5,140 per public submission. Public journal reconstruction counts fall from 431,891 to 35 for Default and from 431,893 to 37 for Fishing Trap. The direct reference remains at 215,933 reconstructions per profile. The instrumentation ran under regression load and supplies counts and order. The uninstrumented results supply the acceptance timing. [Reference counts and boundaries](ordered/Reference/results.json) · [Candidate counts and boundaries](ordered/Candidate/results.json)

The focused control covers identity replacement, phase-aware projections from the base, authoritative expiration, nested strict and qualified calls, and cleanup after an unsupported interpretation exception. A separate real standalone chronology dispatches timed poison, starts formula research and concurrently starts ordinary intake, then advances through expiry. The same admitted state is used for an explicitly scoped versus uncached detached resolver comparison. Both preserve the journal operations and canonical result. The two normal selected console routes compare every response and view byte and preserve their accepted checkpoints and authentic saves. [Expiry and work comparison](expiry/results.json) · [Connected result](connected/results.json) · [Bindings](BINDINGS.json)

Strict restoration remains separate P1 work. Unity gameplay integration stays deferred.

The complete bound regression passed all **1,488** cases, with the 1,487 accepted predecessors and the new scope-isolation case. All six journals match their launch, assignments, loaded modules and completion records. [Focused review](GPT_FOCUSED_REVIEW.md) · [Exact regression](regression/results.json)
