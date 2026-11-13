# MGT-06 connected finite unattended Fishing Trap

Implementation `71e6612cbdc07d2e8e2f347f38355e62c493d5c6` on `Engine` follows the bounded [source/API proposal](SOURCE_API_REVIEW.md) and [actual approval](GPT_SOURCE_REVIEW.md). The new C# session starts through `ConnectedExpeditionSession.StartWithFishingTrap()`. The existing console accepts `-FishingTrap` to select it. The profile is TEST_ONLY and uses wire95/base90.

- The console plays the complete EXP-05 route from r0 to r223 under the new profile. The companion reaches (3,3) with the existing hands, character, equipment and activity ledger. The selected staged Trap is at (3,4).
- The first setup spends one second of real work. Cancellation releases the reserved opportunity and bait. The next setup starts at clock 56874, preserves 599/2 seconds of work across a save, and deploys at 57174 after exactly 300 seconds. Deployment consumes the original bait and commits the original opportunity.
- The companion takes paid travel out of reach and restores a save half a second before the due check. At clock 60174 the live shared check consumes one RNG word, rolls 13 + 2 against DC 12, and captures the original river fish. The remote public view withholds the result. Returning by ordinary movement reveals the outcome.
- The companion reserves the existing receiving location and pays the full 300 seconds to retrieve the same Trap and fish. A save with 599/2 seconds worked retains the same receiver reservation. The Trap ends on the ground at the receiver and the fish moves to that location under companion custody. Fresh repeat claims reject. Exact Set and Retrieve retries return Duplicate. Ordinary movement continues to r242 at clock 60480.

The restored console route, uninterrupted console route, and receipt-based C# replay through the public session methods are compared at four canonical saves. Defender actions are planned again. The unchanged default profile restores and reproduces the authentic EXP-05 r223 bytes. The focused test also covers differing Wisdom and Intelligence in an isolated resolver probe, paused remote Resume, current authority and explicit backup recovery.

A schema37 r2 soaking save produced by the archived standalone assemblies from the accepted MGT-06 handover packet restores and re-encodes byte for byte under the current C# assemblies. The connected checks reject both cross-profile restore directions and a structurally valid save whose RNG provenance was altered. [Historical standalone result](connected/historical-results.json)

The first route exposed a reversed comparison in the existing opportunity record. It rejected a legitimate new reservation after release once the clock advanced. The correction keeps the earlier release attached to its real uncommitted attempt and permits a later reservation. The live profile and demonstration inputs use the same seed, stock, and DC throughout.

The [focused GPT review](GPT_FOCUSED_REVIEW.md) requested two evidence corrections, and [the follow-up](GPT_EVIDENCE_REVIEW.md) confirmed the corrected evidence. The verifier now checks both actual console histories against expected public saves, loads, views and retries, and compares complete live bytes across rejected restores. The [initial regression launch](superseded-regression/README.md) tracked assembly paths only. It was superseded by a fresh run on the same DLL bytes. The new launcher and each worker record digests before execution, and each worker binds its loaded modules and completion journal to that launch. Standalone save generation and current restoration separately record the loaded assembly identities.

The complete fresh regression passed all **1,486** registered cases, including the new focused control, with zero failures. The finalizer verified all six ordered journals and completion records against the common launch and four retained DLLs. [Bound regression](regression/results.json)

[Console inputs](connected/walkthrough.jsonl) · [Console responses](connected/responses.jsonl) · [Assertions and timings](connected/results.json) · [Source and assembly bindings](BINDINGS.json)

The selected composition covers one ordinary finite lifecycle. Broader INT-03 and P1 remain open. Unity gameplay integration stays deferred.
