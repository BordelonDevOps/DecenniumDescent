# Registered tool-repair assignment evidence

## Scope

This TEST_ONLY increment extends the existing worker/site assignment profile to one physical tool-repair fixture. It also corrects a confirmed alias in custom Camp Greens worker-list fingerprints. Schema61 remains the persisted baseline; the snapshot layout, codec branches, and migrations are unchanged.

Pinned rule evidence comes from source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Exact snapshots are under [`sources/`](sources/); profile and named-test coverage is summarized in [`SOURCE_BINDINGS.json`](SOURCE_BINDINGS.json) and the [fresh binding audit](rule-bindings/bindings-20261108T081033049Z-062057de/results.json).

## Responsibilities and authorities

- `ExpeditionWorkAssignmentRecord` remains authoritative for assigned worker, procedure, target, registered site coordinates, readiness, status, and the linked `WorkId`.
- Existing `RepairWorkRecord` and repair commands remain authoritative for the repair job, retained labor, check outcome, and material reservation/settlement.
- Existing structure records remain authoritative for the tool, Carpenter toolkit, and physical repair-material lot locations. In this bounded repair fixture, `RepairAccess` requires the existing `IsRepairWorker` actor eligibility and the explicit `SharedRepairFixture.Trained` fixture fact; assignment registration changes neither. This path does not derive Carpenter qualification from `SkillTrainingRecord` or `CharacterRuleFacts`.
- The shared `WorkLedger`, `RuleClock`, deterministic RNG, command receipts, and `SnapshotCodec` are reused. No parallel job or simulation authority was added.
- `TestOnlyCropPolicy.ContentFingerprint` hashes the complete custom profile—seed quantity, water quantity, worker count, and length-prefixed worker IDs—behind a fixed 25-character prefix. Custom identities remain within the 96-character snapshot header limit. Exact default and established actor/companion custom identities remain compatible. The two formerly colliding custom rosters now reject cross-profile restoration through both inventory and filling policies.

## Connected acceptance

`registered_tool_repair_composes_crop_exploration_save_and_replay`:

1. Registers a repair-eligible actor with `SharedRepairFixture.Trained == true` for an existing damaged tool and a separate worker for Camp Greens planting at their actual fixture sites.
2. Verifies an untrained worker can register but cannot start repair, reserve/consume materials, or create repair work.
3. Runs crop planting and repair on the shared clock while the lead directly explores.
4. Pauses repair at 300 active labor seconds and verifies one repair material is consumed once, the crop task retains its work, and the lead's movement remains in the same snapshot.
5. Saves/restores; rejects repair resume by a different worker; resumes as the assigned carpenter.
6. Advances both restored branches through 3,600 repair labor seconds. The existing clock resolves the eligible check; both branches end byte-for-byte equal with the same RNG state, repaired target, completed crop task, assignment links, and exactly one consumed repair material. Duplicate start/resume receipts do not mutate the settled state.

`crop_worker_profile_delimiter_collision_is_rejected` compares `[TEST_ONLY.actor, TEST_ONLY.companion]` with `[TEST_ONLY.actor-TEST_ONLY.companion]`, which the previous delimiter-joined fingerprint represented identically. It checks exact compatibility for the established custom fingerprint, distinct new identities, and rejected cross-profile inventory and filling restores in both directions.

`custom_crop_policy_fingerprint_fits_header_and_roundtrips` directly initializes a crop-only simulation with the custom roster `[TEST_ONLY.actor]`, encodes and restores the snapshot, verifies the identity remains within the 96-character header limit, and checks that seed and water quantity changes alter the hashed profile identity.

## Validation results

- [`FOCUSED_REPAIR_RESULTS.json`](FOCUSED_REPAIR_RESULTS.json): pass, **1/1** named acceptance.
- [`FOCUSED_CROP_HEADER_RESULTS.json`](FOCUSED_CROP_HEADER_RESULTS.json), [`FOCUSED_FINGERPRINT_RESULTS.json`](FOCUSED_FINGERPRINT_RESULTS.json), [`FOCUSED_PROFILE_COMPAT_RESULTS.json`](FOCUSED_PROFILE_COMPAT_RESULTS.json), and [`FOCUSED_REPAIR_RESULTS.json`](FOCUSED_REPAIR_RESULTS.json): each pass **1/1**; together the focused validation is **4/4**.
- [`HEADLESS_RESULTS.json`](HEADLESS_RESULTS.json): full C# 9 warnings-as-errors compile and headless regression pass, **1,242/1,242**; this current run includes source hashes for the correction.
- [`PACKAGE_RESULTS.json`](PACKAGE_RESULTS.json): static package validation pass, **18/18** checks, **271 assets / 271 unique GUIDs**. This is not Unity Editor import or compilation.
- Fresh source-bound audit: **5 source snapshots, 17 profiles, 340 rule-profile cells, 4 named tests**; see the audit result linked above.
- `git diff --check` is run after documentation and evidence changes before commit.

## Reproduced issues and compatibility limits

- The fingerprint regression was first run against the old implementation and failed because two distinct worker arrays produced the same content fingerprint. [`PROFILE_COLLISION_BEFORE_FIX.json`](reproductions/PROFILE_COLLISION_BEFORE_FIX.json) records that reproduction. The count/length-prefixed hash corrects it.
- The direct custom-crop test initially failed with `Invalid snapshot header` because the variable-length worker/hash suffix pushed the crop fingerprint past the 96-character `ValidId` limit. [`CUSTOM_CROP_HEADER_BEFORE_FIX.json`](reproductions/CUSTOM_CROP_HEADER_BEFORE_FIX.json) records the reproduced failure. Hashing the full custom configuration behind a fixed prefix reduces the identity to 89 characters.
- An early scenario attempt moved the lead west from the fixture's actual `(0,0)` origin and was rejected by the bounded map. [`LEAD_PATH_OUT_OF_BOUNDS_FIXTURE.json`](reproductions/LEAD_PATH_OUT_OF_BOUNDS_FIXTURE.json) records the fixture mismatch; the acceptance now moves north and no traversal implementation was changed.
- An early assertion expected repair to pause at `AwaitingCheck` after full labor. The shared clock already resolves an eligible repair check at its completion boundary; the fixed-seed acceptance observes the existing successful outcome. [`ELIGIBLE_REPAIR_AUTO_COMPLETES_CHECK.json`](reproductions/ELIGIBLE_REPAIR_AUTO_COMPLETES_CHECK.json) records this behavior. No repair timing rule was changed.
- The default profile and the established actor/companion custom profile retain their exact prior identities. Arbitrary custom TEST_ONLY rosters do not receive a general legacy fingerprint migration; their content identity may differ under the collision-safe encoding. No production profile identity is introduced.

## Remaining limits

This covers one registered repair target, one fixed physical site, and the existing TEST_ONLY content. It does not add recruitment, autonomous travel, general scheduling, general repair-site discovery/geometry, started-work reassignment, or production content.

## Review status

GPT's review of commits `e8cc6365` and `532721b0` found no blocker in repair dispatch, worker binding, or material settlement. It identified the custom-fingerprint header overflow and corrected this evidence's description of the repair qualification gate; both findings are addressed in the current correction. Review of the corrective commit remains pending.
