# Intact vessel handling review

2026-11-03. Separate reviewer `/root/source_review` performed read-only review of schema6 records/codec, custody/material history, permission ordering, reservation gates, shared timeline and all23 vessel cases. No remaining actionable findings were reported.

Parent and reviewer independently identified a final-revision overflow in historical burden lookup: `sequence + 1` could wrap at `long.MaxValue` and incorrectly rewind same-clock movement. The implementation now uses an explicit inclusive comparison. A focused regression observes the historical calculation at that boundary and requires3lb after pickup; the previous expression produced2lb. It also commits/restores the last legal revision and verifies subsequent atomic rejection. This was not an invented gameplay decision.

The reviewer independently executed an in-memory fill→pickup→handover→drink→handover→restore probe against the initial compiled implementation. It completed at123seconds with three movement records, retained companion liquid ownership and zero remaining water after actual one-pint intake. No files were written. This was not a full independent suite run.

Final functional review verified all53 source hashes against441/441 PASS in `run-20261103T221818780Z-7b1cf0ca`, including the MaxValue regression,64-move bound, atomic rejection, forged paused-reservation movement, failed saves and maximum schema6 size. The parent subsequently clarified two comments about schema5/6 and supplied hand capabilities, then reran441/441 in `run-20261103T222055777Z-b87c06a4`; executable behavior did not change.

The parent also compared42 unchanged persisted outputs from the418-case schema1–5 baseline. All matched byte-for-byte. Randomly named recovery-evidence paths were excluded when unmatched; this is sampled compatibility evidence, not every possible save state.

Limits: safe ready closed vessels, supplied capable hands/access, supported plot placement, no general equipment/hand-slot or nested-storage graph. History reconstructs vessel custody and physical amounts, not historical actor positions or arbitrary accessibility. No whole-encounter lifecycle, Unity execution or release qualification is claimed. The reviewer made no edits and did not rerun the full suite or independently perform the legacy comparison.
