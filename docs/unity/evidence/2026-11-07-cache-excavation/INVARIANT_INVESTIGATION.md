# Excavation progress tamper investigation

During final invariant review, I checked whether a paused excavation could be restored with its `WorkDone` increased while its worker intervals and command history stayed unchanged.

1. The adversarial snapshot was rejected. A temporary diagnostic probe was added to identify why; its first version used an unconditional `throw` before the rest of the acceptance body, so warnings-as-errors correctly stopped compilation with C# `CS0162` (unreachable code). That was an instrumentation error, not a gameplay failure. See [the compiler report](investigation/DIAGNOSTIC_COMPILER_PROBE.json).
2. Rewriting the probe to report the caught exception produced `InvalidSharedWorldReplay` for a paused record changed from 100 to 101 seconds without a matching command. See [the replay rejection report](investigation/FORGED_PROGRESS_REPLAY_REJECTION.json).
3. Local inspection confirmed why: `TestOnlySharedWorldPolicy.ValidateState` reconstructs from the initial policy, replays every persisted command receipt, and compares the canonical encoded snapshot across all subsystems. The forged progress differs from that deterministic replay and cannot be accepted by a restored `Simulation`.

The final acceptance now asserts the exact `InvalidSharedWorldReplay` result. No second earned-work authority or redundant progress validator was introduced. The corrected focused acceptance passes; the full suite and package gate are recorded in [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json) and [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json).
