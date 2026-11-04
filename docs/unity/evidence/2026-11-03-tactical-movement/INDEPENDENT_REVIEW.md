# Tactical movement review

The separate `/root/source_review` agent reviewed the bounded schema11 integration, source rules and controller/continuation contracts. It found two defects, both corrected before the final evidence run:

- The shared encounter constructor could admit the third actor outside its tactical host while its fingerprint conflated the third actor and companion. The public legacy constructor again admits only its original actors; an internal tactical-host constructor admits the third explicitly and fingerprints it distinctly. Regression coverage checks the public boundary.
- A qualifying own-turn OA forcibly replaced an existing unconsumed Press target. Source wording permits retaining it. The final explicit `PressHitInstruction` retains or replaces the target, including preserving an empty state, and persists through receipts and pending knockout. The source supplies discretion; precommitting the choice before dice is separately recorded as delegated Codex/GPT consensus policy.

The reviewer checked all 82 compiled source hashes against `run-20261104T012449038Z-e2720ad4` and the eight-check static receipt. It independently ran five compiled regressions: explicit schema11/legacy boundary, retain-or-replace during own-turn OA, nonattack/forged selector rejection, full continuation-capacity reservation, and detached collections/legacy-field rejection. All passed.

It also independently exercised keep-empty Press through pending knockout and in-memory SnapshotCodec save/restore. Attempted selector resubmission in ResolveKnockout rejected without mutation; valid completion retained the original selector and empty Press, and final replay restored. It did not write files, rerun the complete suite, independently run disk persistence, or execute Unity.

No actionable findings remained in the bounded review. The parent ran the full 683-case suite and eight package checks, validated exact source bindings and compared all 56 overlapping prior-schema saved outputs. New ordinary movement, pending OA, pending Press/KO and optional Press-choice tests define actual coverage. Structural capacity validation is not a claim of arbitrary64-actor gameplay; the command host admits only two or three explicitly supplied fixtures.
