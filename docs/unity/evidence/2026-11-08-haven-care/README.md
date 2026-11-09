# Haven-care recovery (schema66, TEST_ONLY)

**Implementation review status:** GPT's first review of `f37617dcf57f044a63ec4d6e576364dd01ee43ff` held acceptance on three concrete defects. GPT's second review of `c70fb682dbeea8a3f6ffa9b1face7037130b5ba0` confirmed those execution fixes, then held acceptance on one query/execution mismatch: movement query admission advertised an encounter transition during another actor's active Haven care. Codex reproduced that failure, moved the care-transition guard into shared `AssessWorldStep`, and added same-command query/execution coverage. This correction awaits GPT follow-up review before the increment is accepted or a successor begins. See [actual GPT review](GPT_REVIEW.md). This remains a bounded TEST_ONLY candidate and does not complete MGT-03 or the engine.

## Scope and sources

This increment implements the already-mapped MGT-03 Haven-care recovery dependency. It records one finite TEST_ONLY care interval and its evidence, uses actual shared-clock food/water intake, and removes the complete set of eligible ordinary points from the existing Expedition Strain ledger at completion.

The pinned sources are [STRAIN_PLAYTEST.md](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md), [EXPEDITION_PLAYER_BOOK.md](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md), and [strain_bindings.json](../../../../DescentReviewChanges/ReviewBible/data/playtest/strain_bindings.json), all at ReviewBible revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Exact blob IDs, SHA-256 values and source scope are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The [pre-implementation contract](HAVEN_CARE_CONSENSUS.md) records the agreed policy boundary; it is separate from the required implementation review.

The source requires 24 consecutive hours of qualifying Haven care and location, actual care/food/water, a fresh full window after interruption, completion recovery of all eligible ordinary Expedition Strain points, and preservation of blocked/special points. FL-03 provides 2 lb food and 8 pints water for a Small/Medium person-day. FL-24 says a Haven name does not itself grant a service or provisions, compatible patients may rest during care, and active provider work cannot double-count as the provider's rest.

## Responsibilities and authoritative state

- `ExpeditionHavenCareIntervalRecord` stores ID, patient, provider/service/site IDs, start and scheduled end, actual end/status, start command ID/revision, ending command ID/receipt revision, and actual apply revision.
- `ExpeditionHavenCareAssessmentRecord` stores the completion time/revision, food and water supported from actual intake, provisioning-block status, source intake IDs, and the exact eligible Strain point IDs selected as one batch.
- `ExpeditionStrainRemovalRecord` keeps point removals in the existing source-qualified history with `RecoveryKind.HavenCare`. Gain history and Rest Debt causes are not rewritten.
- `WorkLedger` reservations and existing `IntakeRecord` history are the sole consumption evidence. Care support is clipped to the half-open `[StartedAt, ScheduledEnd)` window and food freshness; the implementation does not create a second debit ledger.
- The profile binds finite TEST_ONLY provider/service/site identities, a fixed roster, one-patient capacity, an authored care qualification fact, availability and physical site. The shared `RuleClock`, world position/traversal, actual crop assignment/work, daily provisioning, Rest Debt, Morale Rest, Strain projection, commands/receipts, and persistence remain authoritative.

Schema66 appends interval and assessment records after schema65 codec state. Haven provenance and records are rejected in older schemas. A saved 6,257-byte schema65 Morale Rest snapshot decodes and re-encodes byte-identically with the schema66 Core/Persistence build; see [historical roundtrip results](final/historical-save-roundtrip/results.json).

## Connected acceptance scenario

The runnable case is `haven_care_batches_supported_strain_after_real_provisioning_and_replays` in [HavenCareCases.cs](../../../../engine/com.decennium.foundation/Tests/EditMode/HavenCareCases.cs). Run it with:

```powershell
pwsh -NoProfile -File engine/tools/Test-Foundation.ps1 -ResultsRoot <results-directory> -CaseName haven_care_batches_supported_strain_after_real_provisioning_and_replays
```

It moves the patient to the authored service site; produces two source-qualified daily-provisioning points and opens Rest Debt using existing clock/provisioning/Rest authorities; starts a 24-hour care interval; proves active-care save/restore and patient travel/roster admission guards; and branches through unsupported care and interruption/restart, which grant no early benefit. In the supported path, the patient eats 2 lb and drinks 8 pints from real lots during the interval. The companion completes a real Camp Greens planting assignment, fills its own waterskin through the existing two-hand 60-second fill job, hands that vessel to the patient, and receives it back after the patient's actual intake.

The case saves and restores during care, advances both branches to hour68, begins compatible Morale Rest, and resolves Morale and Haven care together at hour72. The care assessment removes the two exact eligible daily-provisioning points in one batch, leaves the two null-classified Rest Debt points untouched, records no duplicate Morale recovery offer, and yields Strain level2. The original, restored and codec-replayed completed states compare byte-for-byte. It then continues through ordinary daily provisioning until the patient reaches the source-defined ordinary-death endpoint; the earlier recovery assessment survives another save, restore and deterministic receipt replay.

Two focused regressions cover the other first-review findings. A benign condition-clear event during active care preserves the interval through save/restore and completion. A different scheduled actor's fixed-encounter and inventory-combat entry commands are rejected without changing snapshot bytes, receipts, care status or clock; a movement-triggered encounter is also rejected while another party member is in care. The initial blockers and the later query mismatch are recorded with reproduced-before/focused-after results in [GPT_REVIEW_FIXES_RESULTS.json](GPT_REVIEW_FIXES_RESULTS.json).

## Validation

- Focused connected scenario: **1/1 PASS**; [MODULE_CASE_RESULTS.json](MODULE_CASE_RESULTS.json). It includes later ordinary death and historical care-assessment replay.
- Movement query/execution regression: **1/1 PASS**; [focused report](final/focused/combat-query/run-20261109T050747956Z-814d9c53/results.json). The same command is rejected by query and execution without mutation.
- Full C# 9 warnings-as-errors suite: **1,267/1,267 PASS**, **257** compiled/tested source hashes; [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json).
- Explicit Core, Persistence and LabModel compilation: **PASS**, **187** source hashes; [COMPILE_RESULTS.json](COMPILE_RESULTS.json).
- Static package validation: **18/18 PASS**; [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). This is not Unity Editor import or runtime qualification.
- Pinned source validation: **3/3 PASS** for the Git blob IDs, committed source snapshots and current source SHA-256 values; [validator](Validate-HavenCareBindings.ps1) and [results](SOURCE_BINDINGS_VALIDATION.json).
- Historical schema65 save: **6,257 bytes, byte-identical encode/decode**, SHA-256 `b8a30ad33bfb6292f4dd4de7bb5dbe11e20499b7ebbfeea63519e59a5abd6dd7`; [roundtrip result](final/historical-save-roundtrip/results.json).
- After staging, `git -c core.whitespace=cr-at-eol diff --cached --check`: **PASS** for this correction set. This repository keeps Windows line endings in its evidence files.
- The general rule-binding validator did **not** pass: it stopped before named tests because its pinned report expects an `ActorConditionRecord.cs` hash that differs from the current branch (`boundTests: 0`). The failure is preserved in [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json); it is not presented as Haven-care evidence or a pass. The three pinned Haven source snapshots independently pass [their scoped validator](Validate-HavenCareBindings.ps1).
- Unity import/compile, Edit Mode, Play Mode, game builds and observed presentation were not run; gameplay integration remains deferred.

## Reproduced failures and corrections

- The first connected water-fill attempt gave the equipped patient `TwoHandsRequired`. The scenario now uses the companion's two-hand waterskin and existing 1-second vessel handovers, preserving the source's actual hand and custody rules.
- The first exact-boundary commit returned `InvalidResult` with `HavenCareAssessmentEvidenceMismatch`: validation recomputed eligibility after the same assessment had already removed its points. Validation now reconstructs the pre-batch view by excluding only that assessment's removals, so same-revision upstream gains remain visible. The full endpoint scenario passes after this correction.
- The first assertion counted 12 pints: 4 pints from the initial skin plus two additional four-pint fills. The accepted care quantity is 8 pints, so the scenario now consumes 4 initial pints and exactly one four-pint companion fill.
- GPT's first implementation review identified three blockers. The death regression reproduced a rejected later daily `AdvanceClock`: historical eligibility validation used the snapshot's current `Lives.Dead` value when reconstructing an earlier completion. Historical reconstruction now omits that present-life predicate; shared-world receipt replay re-executes the care completion with the existing live-patient guard at its causal boundary. The focused acceptance reaches later ordinary death and restores/replays the earlier care assessment.
- The condition regression reproduced an otherwise benign `DispatchConditionEvent` committing with the care interval changed to `Interrupted`. That unconditional interrupt was removed; the condition continues through the existing condition authority, and represented life/site loss remains subject to existing boundary validation.
- GPT's second review found the movement execution rejection was not mirrored by its public query. The regression reproduced the mismatch against `c70fb682`; active-care combat admission now runs in shared `AssessWorldStep`, and the same-command query/execution test passes. GPT follow-up review is pending.
- The combat regression reproduced a different scheduled actor entering a fixed encounter and changing the patient's active interval. Active-care transitions to fixed or inventory combat now return `HavenCareCombatTransitionUnsupported` before mutation; the movement-triggered encounter path uses the same rejection, and the patient may explicitly interrupt care before combat.
- Failed focused/diagnostic reports are retained under [development-attempts](development-attempts/), including the exact 72-hour boundary validator error and the earlier two-hand failure.

## Limits

Nonlethal level-six Expedition Collapse and its condition lifecycle are not represented by this simulation, and no collapse-recovery scenario is claimed. The fixed TEST_ONLY service uses an authored `CanDeliverReviewedCare` fact and finite provider/site availability; it does not implement production staffing, service pricing, arbitrary Haven facilities, dynamic rosters/capacity, Wound treatment, HP healing or resurrection. Care during combat/emergencies remains unsupported; active care requires explicit interruption before an admitted combat transition. The Haven-care cases do not independently test forged assessment snapshots, duplicate care-command semantics, fractional completion endpoints, or whole-versus-split clock partitioning; the saved branches reuse the same continuation sequence. This bounded service cannot establish completion of MGT-03 or the complete gameplay engine.
