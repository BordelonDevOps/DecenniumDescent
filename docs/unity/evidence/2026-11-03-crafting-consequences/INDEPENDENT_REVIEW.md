# Independent engineering review

Reviewer: `/root/source_review`. Scope: schema16 immutable consequence records, codec, replay, fixed/fallback dying and shared labor/remediation.

One confirmed defect was reproduced through legal public commands. A supplied occurred-event ID `formula.1` was used directly as the cleanup WorkLedger job ID. Starting hero cleanup silently truncated the companion's unrelated `formula.1` research reservation, while subsequent research continued earning unbooked work. Save/restore accepted the resulting history because it replayed the same faulty command behavior.

Cleanup now uses a dedicated generated `craft.remedy.<incident revision>` job ID consistently for booking, cancellation, boundary selection and credit checks. The permanent regression supplies the colliding public ID, runs simultaneous research/cleanup, checks the original booking, rejects a second companion assignment, pauses cleanup and verifies restored research continuation.

Final candidate: `engine/artifacts/run-20261104T042538457Z-a1d47fde`. The reviewer independently ran27 focused nondisk cases: all passed. The run covers the collision, logical marker persistence after an episode closes, simultaneous life events, remediation boundaries, work windows and current tool permission before duplicate/resume. All113 compiled-source hashes matched the final files. No outstanding findings were reported for the bounded increment.

The parent ran894/894 tests. The reviewer did not independently rerun the full suite, disk tests, legacy byte comparison or Unity. Manufacturing settlement, actual repair jobs, arbitrary content and complete-engine qualification remain outside this review.
