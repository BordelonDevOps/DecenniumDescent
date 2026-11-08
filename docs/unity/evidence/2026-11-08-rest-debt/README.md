# Rest Watch and Rest Debt (schema63, TEST_ONLY)

## Module checkpoint

This is a connected MGT-03 C# simulation increment on the existing schema62 provisioning/Strain profile. GPT reviewed parent `ecfc8dea34a6bab27a661261e65d96289859b70e`, identified two concrete integration blockers, then accepted correction commit `3e9128786953f2beefb0d63d1c6f2c73660037d3` after reviewing both fixes and regressions. No concrete acceptance blocker remains. GPT's actual responses, inspection scope and checks it did not run are preserved in [GPT_REVIEW.md](GPT_REVIEW.md). The design consensus in [REST_DEBT_CONSENSUS.md](../2026-11-08-daily-provisioning/REST_DEBT_CONSENSUS.md) predates implementation review and is not presented as acceptance of the code.

The feature remains gated TEST_ONLY content. It does not complete the engine or authorize Unity gameplay integration.

## Changed files

Engine code and tests:

- `engine/com.decennium.foundation/Runtime/Core/ExpeditionProvisioningRecords.cs`
- `engine/com.decennium.foundation/Runtime/Core/Simulation.cs`
- `engine/com.decennium.foundation/Runtime/Persistence/ExpeditionProvisioningCodec.cs`
- `engine/com.decennium.foundation/Runtime/Persistence/SnapshotCodec.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedCraftingConsequences.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedDailyProvisioning.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedRestDebt.cs` and its Unity `.meta`
- `engine/com.decennium.foundation/Laboratory/Model/SharedWorldCommandQueries.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedWorldRangedCombat.cs`
- `engine/com.decennium.foundation/Laboratory/Model/SharedWorldCombatPolicy.cs`
- `engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs`
- `engine/com.decennium.foundation/Tests/EditMode/DailyProvisioningCases.cs`

Architecture and evidence:

- `.gitattributes` preserves the generated evidence reports byte-for-byte across Windows checkouts.
- `docs/unity/DEVELOPMENT_HANDOFF.md`
- `docs/unity/IMPLEMENTATION_TRACE.md`
- `docs/unity/evidence/2026-11-08-daily-provisioning/REST_DEBT_CONSENSUS.md`
- `docs/unity/evidence/2026-11-08-rest-debt/GPT_REVIEW.md`
- `docs/unity/evidence/2026-11-08-rest-debt/FOCUSED_REST_PHYSICAL_POSITION_RESULTS.json`
- `docs/unity/evidence/2026-11-08-rest-debt/FOCUSED_REST_QUERY_PARITY_RESULTS.json`
- The rest of this evidence directory, including the source-binding manifest, full and focused result reports, package report, exact compiled assemblies, reproduced attempts and this README.

The code commit SHA and the separate evidence commits, if any, are supplied in the GPT review message and recorded in the final GPT review entry.

## Agreed scope, sources and authorities

Responsibilities covered:

- Prospective per-actor selection of a scheduled Rest Watch, with canonical half-open Morning `[0h,8h)`, Afternoon `[8h,16h)` and Evening `[16h,24h)` slots. Evening remains the default.
- An actual continuous eight-hour Rest interval at an explicitly safe and qualifying profile site; shared active work and travel authorities prevent incompatible assigned activity.
- Once-only scheduled Watch outcomes; debt opening, due deadline, subsequent-miss reset, and debt clearance through a completed qualifying Rest.
- Debt-caused gains on the same `ExpeditionStrainGainRecord` history as provisioning, using the same shared clock, sequence, cap, endpoint and persistence authorities.
- Shared command discovery/query, save/restore, and deterministic replay.
- Safe-site admission through the shared exact physical-position resolver, with outstanding traversals (including suspended traversals) rejected as incompatible activity.
- One shared active-Rest command guard in execution and command queries, preserving the Rest control and `AdvanceClock` exceptions.

The operative source is pinned `EXPEDITION_PLAYER_BOOK.md`, FL-03, commit `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, blob `466871fc128dc5f06043a874da2b9c1d94ed80a5`. Rest Debt order/recovery context is pinned `STRAIN_PLAYTEST.md`, blob `7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4`. Binding 27 in pinned `strain_bindings.json`, blob `2be335369152191d3aaf47a558f6c5344b18bb4a`, establishes only the `campaign.rest-debt` → `expedition.strain` identity. Exact snapshots are retained in [the daily provisioning source set](../2026-11-08-daily-provisioning/sources/) and hashes are listed in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json).

The zero epoch and Watch segmentation reuse the adopted TEST_ONLY daily profile; they are not a second clock. The fingerprint binds the Evening default, eight-hour Watch length, two-following-Watch deadline, explicit sites/actors and the same-boundary event-order version. `RuleClock` remains time authority, the existing `WorldPositionResolver` resolves exact physical position over movement records, `WorkLedger` and existing assignment/traversal records remain activity authority, and the unified Strain history remains Strain authority. Schema63 adds event/cause references only where needed. Schema62 retains its existing serialized gain shape and fixed profile.

GPT agreed in advance that coincident unpaid-deadline and new-miss causes each produce a separate gain, with deadline settlement first and Watch-miss settlement second. FL-03 does not specify their relative order; this ordering is explicitly TEST_ONLY. Each event/gain retains its own cause identity and same-boundary sequence.

## Runnable acceptance

The final post-correction C# harness compiled all four assemblies and passed **1,259/1,259** cases. The four Rest Debt cases appear in [MODULE_CASE_RESULTS.json](MODULE_CASE_RESULTS.json) and the complete source-hashed run is [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json).

- `rest_debt_connects_companion_work_safe_rest_deadline_and_replay`: starts actual companion crop-planting work at hour16, resolves the hero's missed Evening Rest at hour24, opens debt due at hour40, then verifies safe Rest from hour24 to32 clears debt without reducing Strain. It saves/restores both before the deadline and during an active Rest. Whole and split clock advances converge through hour40, where the unpaid prior deadline and new missed Rest create two ordered gains and reset the debt deadline to hour56. Further time creates no duplicate deadline. Duplicate command submission, exact replay bytes, exposed/unsafe-site restore rejection, duplicate due-event and wrong-actor event rejection, command discovery and fail-closed combat interruption are also checked.
- `rest_debt_and_daily_provisioning_share_same_time_strain_order`: reaches hour24 with a daily-provisioning shortfall and an unpaid Rest Debt deadline in the same command. It verifies the daily and debt gains share one ordered Strain history, with sequential level-before/after values and the unclassified Rest Debt recovery flags. It rejects forged cause kind and cause ID.
- `rest_debt_requires_physical_safe_site_after_suspended_traversal_restore`: moves the hero partway from the safe berth, suspends, and verifies discovery and execution reject Rest without snapshot mutation before and after a real save/restore. It then completes travel, physically returns to the berth, and verifies a qualifying Rest becomes admissible.
- `resting_movement_query_and_execution_share_admission_guard`: during active Rest, verifies an otherwise legal walk is rejected with the same `ActorCurrentlyResting` reason by query and execution without state change; after explicit interruption, the same movement is discoverable and executes.

The actual compiled Core, Persistence, LabModel and HeadlessTests assemblies are retained in [assemblies](assemblies/). The original focused Rest Debt reports are [here](FOCUSED_REST_DEBT_RESULTS.json) and [here](FOCUSED_STRAIN_ORDER_RESULTS.json); the two correction regressions have reports for [physical-position/save-restore](FOCUSED_REST_PHYSICAL_POSITION_RESULTS.json) and [Rest query/execution parity](FOCUSED_REST_QUERY_PARITY_RESULTS.json).

## Validation results

- Full C# 9 warnings-as-errors headless run: **1,259/1,259 passed**, **250 source hashes**. Core, Persistence, LabModel and HeadlessTests compiled; the four resulting assemblies are retained above.
- Static package structure: **18/18 passed**, **276 package assets / 276 unique GUIDs** — [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). This is not Unity import or runtime validation.
- Fresh exact source/profile/test binding audit: **4 pinned snapshots / 17 profiles / 340 RP cells / 17 named tests passed** — [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json). The historical default binding manifest was not rewritten.
- `git diff --check`: passed after preserving the source file's existing mixed line-ending convention.
- Unity Editor compilation, Edit Mode, Play Mode, player build and gameplay checks were not run; Unity gameplay integration is deferred.

## Reproduced failures and corrections

The final source passes. GPT's first implementation review found two uncovered blockers; [GPT_REVIEW.md](GPT_REVIEW.md) preserves its actual assessment. Rest-site admission now uses `WorldPositionResolver` and rejects pending traversals, including suspended edges; query and execution use the same active-Rest guard. Both named regressions pass, including byte-preserving rejection before and after save/restore, followed by admissible Rest after returning to the berth. The retained intermediate reports in [development-attempts](development-attempts/) also record the checks that failed while refining the test and audit inputs:

- The first discovery assertion used `SingleOrDefault` for `ScheduleRestWatch`, but discovery correctly returned multiple admissible future slots. The test now chooses one option and confirms the query result.
- The first unsupported-emergency test used the resting actor to initiate combat, so the existing actor-rest check rejected it earlier with `ActorCurrentlyResting`. The corrected test uses another scheduled combatant and verifies `RestInterruptionAuthorityUnsupported` with unchanged state bytes.
- The no-argument source-binding audit pointed to the prior daily-provisioning result and correctly rejected its stale C# source hashes. A separate Rest Debt manifest points to the current full run and validates the pinned source snapshots, profile projection and all named tests. The earlier historical audit remains intact.

## Limitations and remaining review gate

The finite TEST_ONLY profile binds only explicit site facts; it does not establish production site safety, generalized actor conditions, dynamic rosters or general Watch calendars. The code has no authoritative emergency event/dispatcher, so a combat entry while Rest is active is rejected without state mutation; emergency-specific Rest interruption and debt opening are not simulated. Long Rest rewards, Morale Rest, Haven care, Strain recovery/removal and other Rest effects remain out of scope. Unity gameplay integration is deferred.

The two first-review blockers are corrected and all post-correction checks pass. GPT must review the correction commit, exact changed-file list, source bounds, refreshed reports, connected scenario and limitations; no successor module should begin until that second review accepts the stated criteria. GPT identified authentic pre-change schema62 save continuation as optional hardening, not an acceptance blocker. Unity gameplay integration remains deferred.
