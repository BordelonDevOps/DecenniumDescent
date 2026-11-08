# Secure Rest Expedition Strain recovery (schema64, TEST_ONLY)

**Review status:** GPT reviewed initial commit `ff98d7d4e527258523f6833409012af9c9f28ce4` and held acceptance for two concrete defects. The focused correction is implemented and local validation passes; GPT's re-review of the corrected pushed commit is pending. This is one bounded MGT-03 gameplay increment, not engine completion. Code, reports, compiled assemblies, pinned-source bindings, the first review, and failed development attempts are retained in this folder.

## Responsibilities and source requirements

This increment executes the existing Expedition Strain recovery rule for the supported provisioning point. A qualifying secure Rest that clears Rest Debt is recorded as a completed beneficial Rest even when a persistent provisioning block remains or there is no currently eligible point. That completion consumes the existing one-beneficial-Rest-per-24-hours allowance; it does not offer recovery while the source block is active or no point is eligible. Once a later actually supported day opens the gate and the 24-hour limit permits another qualifying Rest, the simulation offers one exact eligible point for player selection. Resolving the choice removes exactly that point from the current Strain projection while retaining its original gain and cause history; recovery does not heal, revive, or mutate character base data.

The primary source is pinned `DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md`, revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, blob `7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4`. It defines secure beneficial Long Rest as removing one eligible `expedition.strain` point, orders Rest Debt clearance before beneficial-rest assessment, and retains food/water/source blocks. `EXPEDITION_PLAYER_BOOK.md` at blob `466871fc128dc5f06043a874da2b9c1d94ed80a5` defines the shared clock, eight-hour Rest, one beneficial Long Rest per 24 hours, and the rule that a real sufficient provisioning plan must be available and maintained before the supply-shortfall removal block clears. `strain_bindings.json`, blob `2be335369152191d3aaf47a558f6c5344b18bb4a`, keeps `expedition.strain` separate from serum strain and other tracks. Exact source copies and hashes are referenced in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) and the prior pinned source set at [daily provisioning sources](../2026-11-08-daily-provisioning/sources/).

The fixture's secure site IDs and fixed roster remain fingerprinted `TEST_ONLY` content. Existing pinned rules define the benefit; this implementation does not promote the fixture to production authority. It does not add another recovery formula, additional rest reward, or generic cleanup rule.

## Authoritative records and dependencies

- `RuleClock`, `IntakeRecord`, lot freshness, consumed `WorkLedger` reservations, and the existing daily provisioning settlement remain the authorities for elapsed time and actual supported intake.
- Existing `RestIntervalRecord`, `RestWatchScheduleRecord`, and `RestDebtEventRecord` remain the authorities for physical qualifying Rest, completion, Watch, and debt status.
- `ExpeditionStrainGainRecord` remains append-only source history. Schema64 appends `ExpeditionStrainRecoveryGateUpdateRecord`, `ExpeditionBeneficialRestRecord`, `ExpeditionStrainRecoveryOfferRecord`, and `ExpeditionStrainRemovalRecord` to the shared snapshot and codec.
- The pending choice is a shared command with an exact offered point ID. Command discovery/query, execution receipts, candidate validation, event ordering, persistence, and replay remain on existing simulation authorities.
- The existing `ManufacturingAdvanceRecord`/`ManufacturingAdvance` snapshot field is reused to retain and resume the requested clock target across a pending recovery choice. Its historical name and schema64 serialized layout are unchanged; no parallel continuation clock or new save field was added.
- Exploration, vessel handover, water filling, inventory, custody, and carrying burden reuse their existing records and handlers. A narrowly gated schema64 adapter routes only declared base fixture vessels to `VesselHandling` when no portable-item ledger is selected; real portable links continue through `UsePortableEquipmentHandling`.

No second clock, Strain counter, inventory, work ledger, vessel contents, character record, or RNG was introduced. Schema64 adds records only after schema63's encoded bytes; prior branches remain versioned.

## Runnable acceptance

`secure_rest_recovers_one_provisioning_strain_point_after_supported_day_and_replays_choice` is the retained 1/1 focused scenario. It:

1. Starts from an unsupported provisioning day and missed Rest Watch, proving stock alone opens neither a recovery gate nor a recovery offer.
2. Records actual food/water intake, completes the existing companion water-fill procedure, explores to the work site, and performs one paid physical vessel handover. It checks unchanged lot identity and quantity, ownership/custody, current hand availability, pending-work rejection, linked-item routing, and no duplicated carrying mass.
3. Completes a secure Rest at hour 40 while provisioning is still blocked. The scenario verifies Rest Debt clears and a beneficial-Rest completion is saved even though no recovery offer is available. After the supported daily endpoint opens the gate at hour 48, the rest completed only eight hours earlier still consumes the 24-hour allowance, so no point is offered; this guards against an early recovery loophole.
4. Completes the next qualifying Rest exactly at hour 64. The exact eligible point is offered while a clock advance requested through hour 65 remains suspended in the existing continuation record. The scenario saves/restores before and during the offer, verifies duplicate advance/choice submissions are inert, and confirms the resolved offer resumes the requested target exactly once. A separate 60→64 then 64→65 split trace produces the same gameplay state.
5. Two restored branches resolve the same exact point to identical bytes; the original Strain gain history and Rest Debt events remain, current Strain falls by one, and HP/death state do not change. An explicit legacy schema64 profile fixture retains v1 fingerprint and replay semantics.

The scenario demonstrates exploration, inventory/resource use, shared time/work/rest, and deterministic persistence/replay for this recovery module. It does not include a tactical encounter; tactical behavior is covered by its own mapped modules and the full regression suite.

## Validation results

- Explicit C# 9 warnings-as-errors compile: **Core, Persistence, and LabModel PASS**; actual assemblies retained in [assemblies](assemblies/) and source hashes in [COMPILE_RESULTS.json](COMPILE_RESULTS.json).
- Full C# 9 warnings-as-errors headless suite: **1,260/1,260 PASS**, 252 source hashes; [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json).
- Focused module case: **1/1 PASS**; [MODULE_CASE_RESULTS.json](MODULE_CASE_RESULTS.json).
- Static package validation: **18/18 checks PASS**, **278 assets / 278 unique GUIDs**; [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). This does not represent Unity import or Editor compilation.
- Fresh source/profile/test binding audit: **4 pinned source snapshots / 17 profiles / 340 RP cells / 18 named cases PASS**; [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json). The older historical binding manifests were left unchanged.
- `git -c core.whitespace=cr-at-eol diff --check`: PASS, preserving the existing source line-ending convention.

Unity import/editor compilation, Edit Mode, Play Mode, player build, presentation integration, and gameplay were not run. Unity gameplay integration remains deferred.

## GPT review findings and correction

GPT held initial commit `ff98d7d4e527258523f6833409012af9c9f28ce4` for two concrete defects: (1) Rest completion and its 24-hour allowance were coupled to Strain recovery, so a secure Rest during the provisioning block did not count; and (2) `AdvanceTo` lost its requested target when a recovery choice suspended the clock. GPT found no other blocker in the inspected vessel routing, schema62/63 branches, or rule ordering. It did not run C# validation; it inspected the code, reports, and source bindings. The full response is recorded in [GPT_REVIEW.md](GPT_REVIEW.md).

The correction records the v2 beneficial Rest independently from an optional recovery offer, enforces the interval from the completed Rest, and reuses the existing `ManufacturingAdvanceRecord` to retain/resume an accepted clock target through all recovery choices. The resolver reuses the already-recorded benefit instead of creating a second one. The profile key/fingerprint moved to v2. `EnableLegacyExpeditionStrainRecovery` preserves the v1 fingerprint and old replay semantics for already-supported schema64 saves; the schema64 wire layout is unchanged.

During correction, early focused attempts exposed stale fixture expectations at the new hour-40/hour-48/hour-64 boundaries, duplicate benefit creation on choice resolution, duplicate completion records in a split-trace candidate, and two temporary test-diagnostic compile errors (`RestWatchOutcomeRecord.Kind` and `Command.Fingerprint` do not exist). Those were reproduced and corrected; their reports are retained under [development attempts](development-attempts/gpt-review-correction-20261108/). The default generic binding-script invocation also selected an older source-binding manifest and failed on a stale `ActorConditionRecord.cs` pin; the schema64-specific manifest was then run explicitly and passes against all tested source hashes. This is distinct from the fresh source/profile/test audit reported above.

## Limitations and review gate

This is a finite fixed-roster `TEST_ONLY` implementation. It does not implement Morale Rest, Haven care, other strain-source recovery, generalized Rest profiles, dynamic roster/site qualification, production authority, or all MGT-03 procedures. The only recovery candidates are supported daily-provisioning points; other source classifications remain as before. The portable-vessel bridge is limited to the explicit base fixtures and is inactive when a `PortableEquipment` ledger is present. The legacy-v1 regression reconstructs a v1-profile snapshot fixture and verifies fingerprint/behavior compatibility; an archived byte-identical save produced by the pre-correction commit has not been captured.

Final GPT re-review of the corrected exact commit is required by the project gate. Record its actual response, findings, exact reviewed commit, and checks GPT did or did not perform in [GPT_REVIEW.md](GPT_REVIEW.md) before starting the next mapped module.
