# Unity Rules Engine Development corrected timing review

Response `d088f634-c183-41a0-abf4-a9c4ce39944c` reviewed implementation `3d866e6fa8e2996a6799b1a1f51a05b735b70b45` and timing evidence `ac22f07bba0781c8d0c96cbe87ad8f96ed4db28a`. [Review chat](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

## Corrected session reference-performance evidence — accepted

**Measured implementation:** `3d866e6fa8e2996a6799b1a1f51a05b735b70b45`
**Evidence reviewed:** `ac22f07bba0781c8d0c96cbe87ad8f96ed4db28a`
**Closed requirement:** corrected reference-performance verification from `98339499-82e2-403d-a8b8-c8e534d53319`

**The isolated corrected measurements satisfy all eight existing p95 criteria. Close this performance requirement. No threshold change, source correction or additional benchmark is requested for this bounded item.**

**B1 and B2 remain closed. E1 is now the sole outstanding requirement for final bounded-session acceptance.** Broader P1 and INT-03 remain open.

The source-to-evidence comparison contains documentation and evidence changes only, with **no subsequent C# or console-source changes**.

## 1. All eight reference workloads meet their original criteria

The report uses **30 measured samples per input after one complete warm-up**, on the stated Intel Core i5-4590 host, PowerShell 7.6.9 and .NET 10.0.14. The measurement remains actual C# submission through commitment and one permitted `View`, excluding script input construction and JSON presentation.

All values below are milliseconds:

| Reference workload | Median | p95 | Maximum | Existing p95 limit | Verdict |
|---|---:|---:|---:|---:|---|
| Opening step | 5.048 | 6.871 | 7.968 | 150 | Met |
| First encounter attack | 5.330 | 11.571 | 23.505 | 150 | Met |
| Mid-expedition clock advance | 72.631 | 130.112 | 168.983 | 150 | Met |
| Stabilization milestone | 223.587 | 236.987 | 251.650 | 350 | Met |
| Off-turn opportunity | 13.508 | 25.027 | 28.879 | 150 | Met |
| Defender stance | 10.574 | 18.711 | 21.126 | 150 | Met |
| Defender tactical step | 13.132 | 20.983 | 26.160 | 150 | Met |
| Ordinary continuation | 18.680 | 50.686 | 286.319 | 150 | Met |

The corresponding report entries retain 30 observations and `MetBudget: true`; the documentation’s table agrees with those entries.

### The above-budget maxima do not invalidate a p95 pass

The agreed criterion is **p95**, not maximum latency. The script sorts each input’s observations and selects nearest rank `ceil(0.95 × n)`: for 30 samples, that is the 29th ordered observation. It does not discard the highest observation or average percentiles across workloads.

Therefore, the **168.983 ms** mid-expedition maximum and **286.319 ms** ordinary-continuation maximum remain visible tail-latency observations, but do not fail their respective p95 limits. The latter maximum is present in the retained raw data as the final input of measured walk 30, rather than being omitted from the report.

This is an observed pass for the selected hardware, workloads and history—not a guarantee that every future command will finish below those limits.

## 2. The measurement path and execution remain bound

I inspected the benchmark’s complete measurement and reporting logic. Each measured walk starts a new selected session, submits the actual public inputs, obtains a permitted view, and checks the committed revision and clock. Timing begins before submission and stops after that view. Every measured walk must then reproduce the warm-up’s complete final canonical digest. The script retains all 165 measurements per walk, producing the **4,950-sample** dataset.

Only the eight predeclared reference inputs receive the existing thresholds. Other route timings remain in the report with no implied budget pass. The status calculation does not reinterpret a long advance as the named stabilization exception.

The corrected performance and console reports preserve the original pending and final digests. The console still records **172 input lines, 165 commitments and final revision 165**, including the real pending restore. Its total elapsed time includes JSON handling, projections, startup and restoration; it is not represented as a per-command latency measurement.

The final manifest identifies the same corrected source archive and four DLL digests previously reviewed. It binds the isolated report to:

```text
acd653057c46c481af87f31b2e0a54dc68842bfb2d4825da1fd17ad6e5f9f8b5
```

**I compared the recorded bindings; I did not independently recompute the DLL, report or sample-file hashes.**

## 3. The contended miss remains retained—not relabelled

The prior one-sample contended run remains separate, including its **1,133.642 ms stabilization miss**, **8,210.284 ms long advance** and **14,619.955 ms full restore**. Its recorded artifact bindings are unchanged from the correction packet.

The retention script explicitly preserves that one-sample report when retaining the new 30-sample performance report and requires their final continuation hashes to agree. **This ruling neither combines the contended sample into the isolated distribution nor retroactively labels it a pass.**

The timing documentation records that the original regression ended before these measurements and the corrected regression began afterward. I accept that as the reported execution schedule; **I did not independently certify machine isolation or the absence of unrelated operating-system activity throughout the run**. No causal explanation for individual spikes is inferred.

## 4. Broader P1 disposition is unchanged

The complete route still exposes costs outside the eight reference workloads:

| Operation | Isolated result |
|---|---:|
| Charter-plan submission | **1,463.167 ms p95** |
| Long advance recorded at revision 95 | **3,659.727 ms p95** |
| Long advance recorded at revision 97 | **3,684.711 ms p95** |
| Long advance recorded at revision 106 | **3,861.787 ms p95** |
| Full pending restore | **7,750.837 ms**, separately measured |
| Pending save / file load and decode | **20.156 ms / 2.756 ms** |

The three long advances and charter submission remain explicit in the full report, while complete restoration is measured separately from live execution.

**These remain unresolved broader-P1 constraints, not additional blockers to the corrected reference-performance requirement.** The report’s `PASS` establishes the eight named criteria; it does not establish session-wide interactive responsiveness.

The existing follow-up remains: profile and address the expensive charter reconstruction, settle explicit criteria for long work advances, and preserve visibility of strict restoration cost. Any optimization must retain the established equivalence, atomicity, clock, receipt and validation boundaries. This timing review authorizes no architectural shortcut.

## 5. Remaining gate and inspection limits

**E1 remains open for the corrected 1,482-case execution.** The manifest still records no completed corrected regression. The separately retained **1,481/1,481** report identifies the original implementation `3c7b13728d13bfddbf47976220cd867652d4762d` and its original assemblies. It is valid historical evidence for that source, not a substitute for corrected E1.

For this review, I inspected the timing document, all eight relevant report entries, the slower full-route entries, startup/file-operation results, benchmark and retention scripts, selected raw sample ranges, console report, final bindings, original-regression header and source comparison.

**I did not execute programs, independently recalculate all percentiles from the 4,950 observations, hash artifacts, load saves, audit the complete original regression, modify files or run Unity.** These are source-and-retained-evidence findings.

### Final disposition

**Accept the corrected reference-performance evidence at `ac22f07bba0781c8d0c96cbe87ad8f96ed4db28a` for implementation `3d866e6fa8e2996a6799b1a1f51a05b735b70b45`. Close the performance requirement from `98339499-82e2-403d-a8b8-c8e534d53319`.**

B1 and B2 remain closed. **Only corrected E1 remains before final bounded-session acceptance.** No successor is authorized by this review; broader P1/INT-03 remains open, and Unity gameplay integration stays deferred.
