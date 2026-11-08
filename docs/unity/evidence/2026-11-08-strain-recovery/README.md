# Secure Rest Expedition Strain recovery (schema64, TEST_ONLY)

**Review status:** Implementation and local validation are complete; final implementation review by GPT is pending. This is one bounded MGT-03 gameplay increment, not engine completion. The code, reports, assemblies, pinned-source bindings, and development-attempt records are retained in this folder.

## Responsibilities and source requirements

This increment executes the existing Expedition Strain recovery rule for the supported provisioning point: after an actual, fully supported later day clears the provisioning removal gate, a completed secure beneficial Long Rest can offer one eligible point for player selection. Rest Debt is cleared first under the existing schema63 order. The choice is limited to one beneficial Rest per 24 hours. Completing the choice removes exactly that point from the current Strain projection while retaining its original gain and cause history; recovery does not heal, revive, or mutate character base data.

The primary source is pinned `DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md`, revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, blob `7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4`. It defines secure beneficial Long Rest as removing one eligible `expedition.strain` point, orders Rest Debt clearance before beneficial-rest assessment, and retains food/water/source blocks. `EXPEDITION_PLAYER_BOOK.md` at blob `466871fc128dc5f06043a874da2b9c1d94ed80a5` defines the shared clock, eight-hour Rest, one beneficial Long Rest per 24 hours, and the rule that a real sufficient provisioning plan must be available and maintained before the supply-shortfall removal block clears. `strain_bindings.json`, blob `2be335369152191d3aaf47a558f6c5344b18bb4a`, keeps `expedition.strain` separate from serum strain and other tracks. Exact source copies and hashes are referenced in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) and the prior pinned source set at [daily provisioning sources](../2026-11-08-daily-provisioning/sources/).

The fixture's secure site IDs and fixed roster remain fingerprinted `TEST_ONLY` content. Existing pinned rules define the benefit; this implementation does not promote the fixture to production authority. It does not add another recovery formula, additional rest reward, or generic cleanup rule.

## Authoritative records and dependencies

- `RuleClock`, `IntakeRecord`, lot freshness, consumed `WorkLedger` reservations, and the existing daily provisioning settlement remain the authorities for elapsed time and actual supported intake.
- Existing `RestIntervalRecord`, `RestWatchScheduleRecord`, and `RestDebtEventRecord` remain the authorities for physical qualifying Rest, completion, Watch, and debt status.
- `ExpeditionStrainGainRecord` remains append-only source history. Schema64 appends `ExpeditionStrainRecoveryGateUpdateRecord`, `ExpeditionBeneficialRestRecord`, `ExpeditionStrainRecoveryOfferRecord`, and `ExpeditionStrainRemovalRecord` to the shared snapshot and codec.
- The pending choice is a shared command with an exact offered point ID. Command discovery/query, execution receipts, candidate validation, event ordering, persistence, and replay remain on existing simulation authorities.
- Exploration, vessel handover, water filling, inventory, custody, and carrying burden reuse their existing records and handlers. A narrowly gated schema64 adapter routes only declared base fixture vessels to `VesselHandling` when no portable-item ledger is selected; real portable links continue through `UsePortableEquipmentHandling`.

No second clock, Strain counter, inventory, work ledger, vessel contents, character record, or RNG was introduced. Schema64 adds records only after schema63's encoded bytes; prior branches remain versioned.

## Runnable acceptance

`secure_rest_recovers_one_provisioning_strain_point_after_supported_day_and_replays_choice` is the retained 1/1 focused scenario. It:

1. Starts from an unsupported provisioning day and missed Rest Watch, proving stock alone opens neither a recovery gate nor a recovery offer.
2. Records actual food/water intake, completes the existing companion water-fill procedure, explores to the work site, and performs one paid physical vessel handover. It checks unchanged lot identity and quantity, ownership/custody, current hand availability, pending-work rejection, linked-item routing, and no duplicated carrying mass.
3. Returns to the secure site and starts the existing qualifying Rest. It saves/restores the active Rest, then advances to the supported daily endpoint where real consumed lots settle, the provisioning gate opens, Rest Debt clears, and the exact original eligible point is offered.
4. Verifies the unresolved choice is discovered and queryable, blocks unrelated mutations, and survives save/restore. Two restored branches resolve the same exact point to identical bytes; duplicate submission is inert; the original Strain gain history and Rest Debt events remain, current Strain falls by one, and HP/death state do not change.

The scenario demonstrates exploration, inventory/resource use, shared time/work/rest, and deterministic persistence/replay for this recovery module. It does not include a tactical encounter; tactical behavior is covered by its own mapped modules and the full regression suite.

## Validation results

- Explicit C# 9 warnings-as-errors compile: **Core, Persistence, and LabModel PASS**; actual assemblies retained in [assemblies](assemblies/) and source hashes in [COMPILE_RESULTS.json](COMPILE_RESULTS.json).
- Full C# 9 warnings-as-errors headless suite: **1,260/1,260 PASS**, 252 source hashes; [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json).
- Focused module case: **1/1 PASS**; [MODULE_CASE_RESULTS.json](MODULE_CASE_RESULTS.json).
- Static package validation: **18/18 checks PASS**, **278 assets / 278 unique GUIDs**; [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). This does not represent Unity import or Editor compilation.
- Fresh source/profile/test binding audit: **4 pinned source snapshots / 17 profiles / 340 RP cells / 18 named cases PASS**; [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json). The older historical binding manifests were left unchanged.
- `git -c core.whitespace=cr-at-eol diff --check`: PASS, preserving the existing source line-ending convention.

Unity import/editor compilation, Edit Mode, Play Mode, player build, presentation integration, and gameplay were not run. Unity gameplay integration remains deferred.

## Reproduced failure and correction

The first full suite run failed **1,259/1,260** at `manufacturing_suspended_status_is_scoped_to_actual_principal_receipt`. Re-running that one case reproduced the same failure. Schema64 had generalized pending-choice status by command ID alone; command IDs are principal-scoped, so a second principal's older receipt could be mislabeled as suspended. The helper now requires the accepted receipt's exact ID and revision to match the pending continuation or offer. The targeted regression then passed **1/1**, followed by the full **1,260/1,260** suite and the final explicit compile. The failing reports and corrected focused report are retained in [development-attempts](development-attempts/).

The initial static package check also found missing Unity `.meta` files for the two new C# assets. Matching stable metadata was added; the final 18/18 package report passes. During evidence preparation, the first binding run found a duplicated schema64 test entry in the new manifest (not a gameplay or compilation failure); the duplicate was removed and the fresh audit passes.

## Limitations and review gate

This is a finite fixed-roster `TEST_ONLY` implementation. It does not implement Morale Rest, Haven care, other strain-source recovery, generalized Rest profiles, dynamic roster/site qualification, production authority, or all MGT-03 procedures. The only recovery candidates are supported daily-provisioning points; other source classifications remain as before. The portable-vessel bridge is limited to the explicit base fixtures and is inactive when a `PortableEquipment` ledger is present.

Final GPT review is still required by the project gate. Record its actual response, findings, exact reviewed commit, and checks GPT did or did not perform in [GPT_REVIEW.md](GPT_REVIEW.md) before starting the next mapped module.
