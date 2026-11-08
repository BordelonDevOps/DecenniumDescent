# Rest Watch and Rest Debt (schema63, TEST_ONLY)

## Module checkpoint

This is a connected MGT-03 C# simulation increment on the existing schema62 provisioning/Strain profile. It is implemented locally on branch `Engine` and is awaiting GPT's implementation review. The design consensus in [REST_DEBT_CONSENSUS.md](../2026-11-08-daily-provisioning/REST_DEBT_CONSENSUS.md) predates this implementation review and is not presented as GPT acceptance of the current code.

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
- This evidence directory, including the source-binding manifest, full and focused result reports, package report, exact compiled assemblies, reproduced attempts, and this handoff.

The code commit SHA and the separate evidence commits, if any, are supplied in the GPT review message and recorded in the final GPT review entry.

## Agreed scope, sources and authorities

Responsibilities covered:

- Prospective per-actor selection of a scheduled Rest Watch, with canonical half-open Morning `[0h,8h)`, Afternoon `[8h,16h)` and Evening `[16h,24h)` slots. Evening remains the default.
- An actual continuous eight-hour Rest interval at an explicitly safe and qualifying profile site; shared active work and travel authorities prevent incompatible assigned activity.
- Once-only scheduled Watch outcomes; debt opening, due deadline, subsequent-miss reset, and debt clearance through a completed qualifying Rest.
- Debt-caused gains on the same `ExpeditionStrainGainRecord` history as provisioning, using the same shared clock, sequence, cap, endpoint and persistence authorities.
- Shared command discovery/query, save/restore, and deterministic replay.

The operative source is pinned `EXPEDITION_PLAYER_BOOK.md`, FL-03, commit `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, blob `466871fc128dc5f06043a874da2b9c1d94ed80a5`. Rest Debt order/recovery context is pinned `STRAIN_PLAYTEST.md`, blob `7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4`. Binding 27 in pinned `strain_bindings.json`, blob `2be335369152191d3aaf47a558f6c5344b18bb4a`, establishes only the `campaign.rest-debt` → `expedition.strain` identity. Exact snapshots are retained in [the daily provisioning source set](../2026-11-08-daily-provisioning/sources/) and hashes are listed in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json).

The zero epoch and Watch segmentation reuse the adopted TEST_ONLY daily profile; they are not a second clock. The fingerprint binds the Evening default, eight-hour Watch length, two-following-Watch deadline, explicit sites/actors and the same-boundary event-order version. `RuleClock` remains time authority, `WorkLedger` and existing assignment/traversal records remain activity authority, and the unified Strain history remains Strain authority. Schema63 adds event/cause references only where needed. Schema62 retains its existing serialized gain shape and fixed profile.

GPT agreed in advance that coincident unpaid-deadline and new-miss causes each produce a separate gain, with deadline settlement first and Watch-miss settlement second. FL-03 does not specify their relative order; this ordering is explicitly TEST_ONLY. Each event/gain retains its own cause identity and same-boundary sequence.

## Runnable acceptance

The full C# harness compiled all four assemblies and passed **1,257/1,257** cases. The two Rest Debt cases appear in [MODULE_CASE_RESULTS.json](MODULE_CASE_RESULTS.json) and the complete source-hashed run is [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json).

- `rest_debt_connects_companion_work_safe_rest_deadline_and_replay`: starts actual companion crop-planting work at hour16, resolves the hero's missed Evening Rest at hour24, opens debt due at hour40, then verifies safe Rest from hour24 to32 clears debt without reducing Strain. It saves/restores both before the deadline and during an active Rest. Whole and split clock advances converge through hour40, where the unpaid prior deadline and new missed Rest create two ordered gains and reset the debt deadline to hour56. Further time creates no duplicate deadline. Duplicate command submission, exact replay bytes, exposed/unsafe-site restore rejection, duplicate due-event and wrong-actor event rejection, command discovery and fail-closed combat interruption are also checked.
- `rest_debt_and_daily_provisioning_share_same_time_strain_order`: reaches hour24 with a daily-provisioning shortfall and an unpaid Rest Debt deadline in the same command. It verifies the daily and debt gains share one ordered Strain history, with sequential level-before/after values and the unclassified Rest Debt recovery flags. It rejects forged cause kind and cause ID.

The actual compiled Core, Persistence, LabModel and HeadlessTests assemblies are retained in [assemblies](assemblies/). Focused run reports are [here](FOCUSED_REST_DEBT_RESULTS.json) and [here](FOCUSED_STRAIN_ORDER_RESULTS.json).

## Validation results

- Full C# 9 warnings-as-errors headless run: **1,257/1,257 passed**, **250 source hashes**. The four resulting assemblies are present above.
- Static package structure: **18/18 passed**, **276 package assets / 276 unique GUIDs** — [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). This is not Unity import or runtime validation.
- Fresh exact source/profile/test binding audit: **4 pinned snapshots / 17 profiles / 340 RP cells / 15 named tests passed** — [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json). The historical default binding manifest was not rewritten.
- `git diff --check`: passed after preserving the source file's existing mixed line-ending convention.
- Unity Editor compilation, Edit Mode, Play Mode, player build and gameplay checks were not run; Unity gameplay integration is deferred.

## Reproduced failures and corrections

The final source passes. The retained intermediate reports in [development-attempts](development-attempts/) record the checks that failed while refining the test and audit inputs:

- The first discovery assertion used `SingleOrDefault` for `ScheduleRestWatch`, but discovery correctly returned multiple admissible future slots. The test now chooses one option and confirms the query result.
- The first unsupported-emergency test used the resting actor to initiate combat, so the existing actor-rest check rejected it earlier with `ActorCurrentlyResting`. The corrected test uses another scheduled combatant and verifies `RestInterruptionAuthorityUnsupported` with unchanged state bytes.
- The no-argument source-binding audit pointed to the prior daily-provisioning result and correctly rejected its stale C# source hashes. A separate Rest Debt manifest points to the current full run and validates the pinned source snapshots, profile projection and all named tests. The earlier historical audit remains intact.

## Limitations and remaining review gate

The finite TEST_ONLY profile binds only explicit site facts; it does not establish production site safety, generalized actor conditions, dynamic rosters or general Watch calendars. The code has no authoritative emergency event/dispatcher, so a combat entry while Rest is active is rejected without state mutation; emergency-specific Rest interruption and debt opening are not simulated. Long Rest rewards, Morale Rest, Haven care, Strain recovery/removal and other Rest effects remain out of scope. Unity gameplay integration is deferred.

GPT still needs to review the exact implementation commit, changed-file list, source bounds, test reports, connected scenario, and these limitations. No successor module should begin until that review accepts the stated criteria or all concrete blockers are fixed and re-reviewed.
