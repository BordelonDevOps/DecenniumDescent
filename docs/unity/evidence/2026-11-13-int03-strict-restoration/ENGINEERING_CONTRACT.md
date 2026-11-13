# INT-03/P1 strict external restoration

Proposal against accepted gameplay `26854d6f49842ae3ea40536d96cc102bc2896e24`. The selected workload restores the authentic r104 post-research save in each profile. Paired r103 and the longer accepted r223/r242 are comparison points. [Controlling decision](../2026-11-13-int03-active-work-performance/GPT_FINAL_REVIEW.md)

## Proposed validation and ownership boundary

Keep the existing external file decode, structural checks, selected profile and TEST_ONLY checks, detached input, complete replay from `Initial()`, and whole-state canonical equality. An optional construction capability for the two exact selected profiles can perform the profile checks, full validating replay and checkpoint creation together. Core supplies the actual candidate and newly owned origin through that capability only after its normal shape and scope checks. Other profiles and executable strict reference continue through the existing constructor and validator.

During the required selected replay, reconstruct the first qualifying passage by applying the existing before/after predicate to each accepted transition. Keep the result local and provisional until all receipts resolve and the canonical bytes agree. Preserve the distinct start and completion receipts, binding, cutoff and coverage. The replay uses the original charter assessment for every historical command. After complete success, seal the verified bytes and derived fact to the actual new origin. A failure returns no checkpoint and changes no live session.

Use the existing uncached resolver throughout the validating replay. The first correction targets the separately measured extra sealing pass. Per-receipt condition reuse within strict history is outside this contract. Keep the public direct resolver, existing full-reference constructor and unsupported combinations on their existing paths. This proposal preserves the live advance optimization, calendar behavior, fingerprint, wire format and authority.

Backup recovery validates and seals the replacement before filesystem displacement and adoption. Failed validation preserves canonical live bytes, current controller and seat grants and produces no reusable proof. File identity, checksums and prior loads supply no authority. No proof is saved, shared between attempts, or retained in policy-level mutable state.

## Verification plan

Require identical public results and full permitted views, supported save bytes, replay and actual continuation in both profiles. Exercise checksum-valid altered history, malformed files, profile mismatch, backup rejection and successful recovery, pending work/choices, exact retries and separate origin ownership. Verify actual receipt count, ordered event behavior, and passage cutoff. Keep authentic old saves and complete source/build/assembly-bound regression. Timing uses at least 30 warm public restore-to-view samples per profile and a separate first-load observation.

## Isolated accepted-source baseline

| Operation | Default median / p95 ms | Fishing Trap median / p95 ms |
| --- | ---: | ---: |
| Public r104 restore through permitted view | 4063.89 / 4427.22 | 4023.32 / 4202.97 |
| Full historical replay and canonical comparison | 3367.98 / 3460.34 | 3325.37 / 3361.45 |
| Current separate passage derivation and sealing | 668.53 / 684.77 | 663.77 / 719.81 |
| File read | 5.24 / 17.77 | 2.58 / 7.55 |
| Decode | 2.20 / 15.15 | 2.25 / 8.03 |
| One detached copy | 0.10 / 14.60 | 0.10 / 0.16 |
| Core shape checks | 0.65 / 14.94 | 0.72 / 1.54 |
| Profile checks outside the replay callback | 1.35 / 29.25 | 1.25 / 2.13 |
| Permitted view | 0.44 / 0.73 | 0.42 / 0.94 |

The public rows use 30 warm samples. The isolated component probes use five samples and may overlap. The profile-only probe is diagnostic. Public maxima were 4581.44 and 4216.49 ms. First public loads measured 5778.94 and 4024.36 ms, with Fishing Trap second in the same process. The paired r103 observations were 2507.97 and 2805.94 ms. The default r223 and Trap r242 comparison restores measured 7198.24 and 7479.46 ms. Every sampled restore reproduces the accepted bytes. [Raw baseline](baseline/results.json)

Proposed acceptance is **r104 public restore-to-view p95 at or below 3,950 ms in each profile** in an isolated 30-sample warm run. The bound reflects removal of the measured roughly 665 ms additional sealing pass, with margin for variance and ordinary sealing. Record maxima, cold/startup and the longer controls separately. Retain diagnostic receipt counts to show full validation still resolves every receipt once and that no second passage replay remains.
