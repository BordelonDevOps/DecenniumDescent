# Morale Rest over shared Expedition Strain (schema65, TEST_ONLY)

**Implementation status:** the original implementation review found three concrete blockers. The focused corrections below are implemented and validated; GPT's follow-up implementation review is pending. The source labels Morale Rest `NEW`, so it remains candidate/TEST_ONLY behavior. This does not complete MGT-03, the C# engine, or a playable three-layer game. Unity gameplay integration remains deferred.

The pre-implementation contract, including GPT's actual design consensus, is in [MORALE_REST_CONSENSUS.md](MORALE_REST_CONSENSUS.md). The exact source snapshots, profiles and named-test bindings are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The actual GPT implementation review will be recorded in [GPT_REVIEW.md](GPT_REVIEW.md) after it is received.

## Responsibilities and source requirements

This increment records a real voluntary four-hour recreation interval, interruption and completion on the shared simulation; blocks incompatible participant procedures while allowing other actors to continue compatible activity; enforces Morale's independent 24-hour benefit limit; and offers one exact eligible Expedition Strain point through the existing patient-choice command. It applies mandatory provisioning and Rest Debt boundary effects first and never clears or satisfies Rest Debt through Morale.

The pinned primary sources are `STRAIN_PLAYTEST.md` blob `7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4` and `EXPEDITION_PLAYER_BOOK.md` blob `466871fc128dc5f06043a874da2b9c1d94ed80a5`, both at ReviewBible revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. The source directly specifies four consecutive safe hours of voluntarily chosen recreation, the work/travel/sleep/Short Rest exclusions, a once-per-24-hours Morale benefit, one eligible Expedition Strain point, no Wound removal, and separate Morale/secure-Long-Rest reductions. Because the Morale endpoint is explicitly `NEW`, site safety, participant roster, overlap/interruption details, no-time patient choice, blocked/no-candidate allowance consumption, and exact boundary behavior are identified as TEST_ONLY operational completions in the consensus record.

## Authoritative state and dependencies

- `ExpeditionMoraleRestIntervalRecord` binds actor/site/activity, actual start, scheduled end, actual end/status, causal command IDs and revisions.
- `ExpeditionMoraleRestBenefitRecord` records each qualifying Morale allowance at its exact completion time, independently of whether an offer exists.
- The shared `ExpeditionStrainRecoveryOfferRecord` carries `RecoveryKind`, activity/completion identity, actor, exact point IDs, initiating command and choice resolution.
- Existing `ExpeditionStrainRemovalRecord` stores the typed recovery cause in the single historical Strain mutation stream; `SecureLongRest` keeps the compatibility `BeneficialRestId` projection and `MoraleRest` uses the same event history.
- `RuleClock`, physical position/traversal, `WorkLedger`, actual assignments, condition/life facts, ordinary intake, daily settlement, Rest Watch/Rest Debt, shared Strain projection, command discovery/query/receipts, existing `ManufacturingAdvanceRecord` continuation and schema-aware codecs remain authoritative.

The schema65 codec appends Morale interval/benefit arrays and typed recovery provenance after schema64 content. Schemas through 64 retain their existing encoded branches and v1 profile behavior. There is no second clock, work ledger, inventory, RNG, character state, Strain counter or recovery history.

## Runnable connected acceptance

`morale_rest_connects_provisioning_assignment_debt_and_independent_recovery_replay` is the retained **1/1** focused case. It exercises:

1. An actual unsupported-day Strain point and a four-hour Morale interval completing with no eligible recovery candidate; its allowance is recorded. A later interval inside that allowance completes without benefit or reset.
2. A companion starts actual assigned Camp Greens planting during the hero's active Morale interval. The test saves at 30 minutes, restores, and advances the shared clock; the companion finishes the crop while the hero's interval continues.
3. A second actual provisioning shortfall creates a second eligible source point. Existing real-lot food and water intake opens the source-specific gate at the later supported daily endpoint. Rest Debt remains separate and is opened at the same endpoint as the later Morale completion.
4. A secure Long Rest clears Rest Debt and independently removes the next point at its own 24-hour endpoint. Morale can remove a supply-qualified point while debt remains owed; neither benefit removes the null-classified Rest Debt point.
5. A represented level-five incapacity interrupts at the boundary with no benefit. A separate manual interruption after one active hour awards nothing; restart needs and receives four fresh consecutive hours. Overlapping Long Rest and Morale are rejected.
6. At the qualifying Morale boundary, the accepted clock command targets hour73 and suspends at hour72 for exact patient choice. A pending save/restore preserves that continuation; unrelated clock advancement is rejected identically by query and execution; resolving the exact point resumes to hour73. Two same-trace branches remain byte-identical and a separate split trace reaches the same gameplay state.
7. Duplicate choice submission is inert. Strain gain history, Rest Debt, HP and death state are preserved; only the selected point is removed. A distinct secure Long Rest later removes the second source-qualified point.

The original GPT implementation review found three defects. Each now has a separate regression:

- `morale_rest_recovery_continuation_uses_authorized_clock_receipt_for_incapacity` starts the companion's actual secure-Long-Rest offer while the hero is recreating. The accepted hour121 `AdvanceClock` suspends at hour118, survives save/restore, and resumes after the exact point choice. Hero incapacity interrupts Morale at hour120, attributed to the original accepted clock command ID and revision held in `ManufacturingAdvanceRecord`, not to the later choice command. Both restored branches match byte-for-byte; duplicate choice is inert. No schema or validator relaxation was needed.
- `morale_rest_resolved_encounter_history_allows_physical_return_and_replay` defeats an actual encounter, exits tactical control while retaining resolved encounter history, saves/restores, physically returns to the authored recreation site, then starts and completes Morale. The retained encounter is historical; unresolved conflict and active tactical combat remain blocked.
- `morale_rest_rejects_one_second_handling_across_exact_completion-boundary` starts Morale and reaches one-half second before completion. A one-second inventory pickup is rejected as `TimedHandlingBoundaryUnsupported` without mutation; an exact half-second clock advance completes the interval once and replays identically after save/restore.

For this bounded scenario, the fingerprinted provisioning/Rest Debt roster enrolls the hero while the companion is the assigned worker. The default schema62 profile still enrolls both existing actors with its unchanged canonical roster/fingerprint. This fixture distinction prevents an unrelated companion provisioning shortfall from incapacitating the worker before the concurrent-work proof.

## Validation results

- Original connected module case: **1/1 PASS**; three GPT-finding regressions: **3/3 PASS**; retained named-case results are under [review-corrections](development-attempts/review-corrections/).
- Full C# 9 warnings-as-errors regression suite: **1,264/1,264 PASS**, 254 tested-source hashes; [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json).
- Fresh explicit Roslyn compile: **Core, Persistence and LabModel PASS**, 185 C# source hashes; [COMPILE_RESULTS.json](COMPILE_RESULTS.json). Build assemblies and generated save bundles remain local and are omitted from the repository commit.
- Fresh static package validation: **18/18 PASS**, **280 package assets / 280 unique GUIDs**; [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). This is not Unity import or Editor compilation.
- Fresh source/profile/test binding: **4 pinned source snapshots / 17 profiles / 340 RP cells / 22 named implementation tests PASS**; [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json). The schema65 Morale entry directly binds all four Morale scenarios.
- `git -c core.whitespace=cr-at-eol diff --check`: PASS.

All final reports bind the exact tested C# source hashes. Failed development attempts are retained under [development-attempts](development-attempts/).

## Failed attempts and corrections

- The first runtime compile caught `CS1628`: an `out` parameter was captured in a LINQ predicate. The resolver now uses a local selected-offer alias; the focused case and explicit compile pass.
- An early scenario tried to assign work to the companion after its two-actor test roster had accrued incapacitating Strain. The test now uses the explicit hero-only admission profile while retaining the companion as the actual concurrent worker; no default-roster rule or fingerprint changed.
- Boundary assertions initially scheduled the wrong Rest Watch slot for the expected simultaneous Rest Debt opening. The profile now schedules the Evening Watch that actually ends at hour72.
- Static package validation caught missing metadata for the two new C# assets. Both now have unique Unity GUID metadata; the rerun passes.
- Continuation assertions initially named nonexistent fields. Compilation identified the existing API names (`ManufacturingAdvanceRecord.CommandId`, `ExpeditionStrainRemovalRecord.At`); corrected assertions then passed the focused case.

The attempt reports also preserve their exact compiler/test/package diagnostics. They are not reported as final-pass evidence.

## Limits and review gate

This is not production Morale authority. General recreation activities, dynamic safety, other Strain-source recovery, Haven care, unrepresented emergency interruption, complete MGT-03, combat-specific recovery, Unity integration, and human gameplay qualification remain unsupported or outside scope. `QueryCommand` does not expose the generic one-second `HandleInventory` operation in this fixture (`UnsupportedOperation`), so the exact-boundary regression proves read-only query non-mutation and the execution rejection, not query admissibility parity. Unity import/compilation, Edit Mode, Play Mode, player builds and observed gameplay were not run.

GPT must review the exact implementation commit and this evidence before the next mapped increment begins. Passing tests or package validation alone do not establish acceptance or engine completion.
