# Temporal kernel development and independent-review record

This is an intermediate implementation record. It is not approval of Time Loop or the whole game. The original sources and every submitted packet remain preserved.

## Initial 46-test packet

`CODEX_TEMPORAL_KERNEL_REVIEW.md` and `TEMPORAL_KERNEL_REVIEW_MANIFEST.json` preserve the exact code first sent to Calibration Review. All 46 methods passed. The owner then asked the notebook what it was checking; the completed response in `GPT_TEMPORAL_KERNEL_SCOPE_EXPLANATION.md` explains scope and contains no independent findings or approval. Do not record it as closure.

## Local 52-test revision

Before receiving independent findings, Codex added six regressions and these repairs:

- Preserve before/after state in a conserved Director/engine audit frame for every committed restore. Discarded death/bind/grant records remain evidence without entering character memory.
- Restore a destroyed participant's physical root under the same immutable identity, and reject deleted/reused provenance or a changed body ownership/enrollment without an adapter.
- Use the existing BufferLedger's actual completed-long-rest epoch for Time Loop, removing the duplicate scheduler rest counter.
- Give the current external maximum-HP record precedence over a stale same-ID projection, after checking owner/target/application identity.
- Reject a world marker or actual regular history that moved backward before the original snapshot.

`CODEX_TEMPORAL_KERNEL_REVIEW_V2.md` and its manifest preserve the exact updated 52-test packet sent to the notebook. Its helper hash is `682bb64b0b1804051b7c9cc74e0da552c16c35b680c5d53f69cc835c52a08e34`. The screenshot `gpt-temporal-kernel-review-v2.png` confirms actual receipt and an ongoing independent review.

## Geometry regression reproduced and repaired locally

While the second review was ongoing, its visible progress flagged a physical/environment consistency concern. Codex independently reproduced two concrete failures against the submitted 52-test helper:

1. A post-snapshot temporal wall was marked physically retired, but its blocked cells survived in `Geometry.anchors`.
2. A post-snapshot temporal floor was similarly retired without removing its support cells. Because preflight still saw that support, it wrongly allowed a restore with a protected outsider standing on that floor.

Two new regression methods failed before the repair; the saved `TEMPORAL_KERNEL_GEOMETRY_REPRO.json` records that failure against the exact submitted hash. The repair filters retired IDs from the candidate environment-anchor map before restoring snapshot anchors and checking support/reachability. The participant-pose retirement already existed; environment retirement must use the same identity set.

All 54 methods then passed. The repaired helper hash is `c4fa1b3ef209faf0decf8d69dff2232ae04a40c4becd20ccd7c4364ea50e596b`. This fix has not yet received a completed independent disposition. Further findings from the notebook's second review still need to be captured, reproduced and reconciled.

Seven major source integrations remain missing, and `playable_plan()` still always rejects. No catalog promotion, source deletion or GitHub push has occurred.

## Six temporal-kernel findings repaired; independent confirmation pending

The actual notebook returned [six findings](GPT_TEMPORAL_KERNEL_FINDINGS.md). The [repair packet](CODEX_TEMPORAL_KERNEL_REPAIRS.md) contains the updated helper, all70 passing test methods, current scope guide and unchanged existing maximum-HP source constructor. It was submitted for independent confirmation. The source constructor already rejects the review's two invented max-HP IDs; an explicit temporal table also now rejects actual valid sources with unimplemented temporal policies. Full Time Loop stays unavailable, the seven larger integrations remain unfinished, and no domain was promoted.

The next control/pulse source preparation is [V3](TEMPORAL_CONTROL_PULSE_POLICY_SOURCES_V3.json):44 selected control records,32 pulse binding records,3 direct supplemental records and all33 pulse/native/contact aliases. This is evidence preparation, not an adopted temporal policy. Earlier preparation versions remain preserved.

## Bounded temporal foundation jointly reviewed

The [actual completed GPT reply](GPT_TEMPORAL_KERNEL_FOUNDATION_CLOSURE.md) finds no remaining reproducible blocker in the admitted foundation. The [exact identity-repair diff](CODEX_TEMPORAL_KERNEL_IDENTITY_REPAIRS.md) resolves the three follow-up findings; the six earlier findings also remain resolved. All76 adversarial test methods pass. Reviewed helper SHA256: `b821829ed352e69ce1ecf3c3d753f0206c8f8d2ec5a5d64bc89d5fd7d8a72151`.

This closes only the bounded foundational checkpoint. Seven real integrations remain: transformations/concentration, Druid, creatures, devices, remaining lifecycles, complete FeatWorld, and control/healing pulses. Full Time Loop stays unavailable and unpromoted. The final whole-game flow/GitHub gate remains open. No original was deleted and nothing was pushed.

A source scan confirms the existing healing ledger is the only other production helper directly reading `consumed_reducer_ids`; the temporal subclass overrides that commit method. FeatWorld uses returned canonical application IDs. This is compatibility evidence for the admitted interface, not proof of the still-missing full FeatWorld synchronization.
