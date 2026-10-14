# Live control/pulse transaction review trail

The [original code submission](CODEX_TEMPORAL_CONTROL_WORLD_REVIEW.md) passed 36 integration methods. The [actual notebook response](GPT_TEMPORAL_CONTROL_WORLD_FINDINGS.md) returned five concrete integration defects and required an Oracle-zone concentration correction. The [repair submission](CODEX_TEMPORAL_CONTROL_WORLD_REPAIRS.md) passes 44 integration methods, with the 76 foundation and 22 payment/output methods still passing. Independent confirmation of this revision is pending.

| Finding | Implemented repair | Regression evidence |
| --- | --- | --- |
| Unobserved Garden missed upkeep could allow a contact cure | Project each pulse parent to current time before authorizing a child; reject ended projections without granting a benefit | Already-ended and unobserved-missed-upkeep parent tests |
| Snapshot numeric recipient round could impersonate encounter round 1 | Reject participant claims at capture until outside-round import exists; preserve outsider-only current claims | Import-rejection test; outsider conservation test |
| Separate independent-output ledgers could grant the same Ki twice | Require the host's existing `ConservedPulseOutputs`; reuse actual registrations and delegate resolution; stage missed opportunities into its one conserved set | Old-API then new-API and reverse-path tests across actual restore; guard state/binding/schema stale-plan cases |
| Speed suppression had no provenance | Reject an initially or subsequently suppressed record until a source adapter classifies it | Capture and restore rejection without cost/state changes |
| Concentration schema could change after preflight | Watch the complete concentration schema as well as current bindings | Added-field stale-plan counterexample |
| Oracle Final pulse profiles omitted concentration | Require it for Eternal Bloom and Crown Restored through the existing zone engine | Both exact source profiles reject a missing concentration identity |

The approved payment/output helper remains unchanged. The archived foundation remains unchanged; the current foundation extension still requires its own bounded disposition. Original sources, class catalog counts, seven missing major temporal integrations and whole-game completion status are unchanged. This log records engineering work, not independent approval.

## Follow-up review and 49-method revision

The [actual 44-method review](GPT_TEMPORAL_CONTROL_WORLD_REPAIR_REVIEW.md) explicitly confirms the first five repairs and both Oracle concentration corrections. It identifies two narrower admission defects: a future/already-ended pulse can enter the snapshot, and pulse/Bloom/contact/native component IDs were not checked. Both are repaired in the [exact incremental submission](CODEX_TEMPORAL_CONTROL_ADMISSION_REPAIRS.md), sent for actual confirmation.

Additional Codex probes preserved in `TEMPORAL_CONTROL_WORLD_SCHEMA_PROBES.json` reproduced partial mutation on four malformed collection types. The current adapter validates the expected sets, dictionaries and lists before payment or occurrence mutation. Tests verify the live state is unchanged on rejection. This does not change the existing approved primitive helpers.

The same revision reconciles Bloom's installment cursor with already-past original source markers. A restore at second 7 loses the missed share at second 6 without healing, while an authentic third pulse at second 12 can still deliver its original share. The new test's first run used an incorrect fixture HP expectation of 20; the canonical fixture starts at 25, so that assertion was corrected. No source or life-state rule changed to satisfy the test.

Current engineering result: 49 integration + 76 foundation + 22 payment/output methods pass. Full Time Loop and all seven larger integration domains remain open. The 49-method code is pending the notebook's actual disposition.

## Bounded live control/pulse transaction closure

The [actual GPT response](GPT_TEMPORAL_CONTROL_WORLD_CLOSURE.md) confirms the exact 50-method revision after the [callback-binding repair](CODEX_TEMPORAL_CONTROL_BINDING_REPAIR.md). It accepts all three same-ID replacement rejection cases and keeps the previous clock, admission, collection, shared-output and Bloom repairs closed. The separate `TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json` binds the exact live adapter, tests, foundation extension and unchanged payment bridge. 50 integration +76 foundation +22 payment/output methods pass.

This closes this bounded engineering checkpoint only. Complete source/parent lifecycles, final HP/Ki/Conviction application, all seven major Time Loop integrations, the full feature and whole-game flow review remain open. The human's conditional GitHub authorization persists; GPT's reference to an authorization gate is recorded as its own wording, not a request for renewed human permission. No original source was deleted and no GitHub push occurred.
