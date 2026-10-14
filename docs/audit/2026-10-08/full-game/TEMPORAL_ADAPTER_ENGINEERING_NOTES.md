# Temporal adapter engineering notes

Historical engineering preparation, followed by current implementation notes. The twelve boundary decisions are captured in GPT_TEMPORAL_WORLD_BOUNDARIES.md. The foundational kernel has completed its bounded independent review in GPT_TEMPORAL_KERNEL_FOUNDATION_CLOSURE.md; the full temporal adapter set remains unfinished. This file is not independent approval.

- The submitted state-holder V1 inventory captured dataclass declarations and constructor assignments. V2 additionally captures assignments in later methods, including Druid reserve/shifts/surges initialized by `_refill`. Preserve V1 as exact submitted evidence. Neither AST pass is a completeness certificate: `BufferLedger.ordinary_cast_events` is attached by the separate Harmonic Bulwark adapter.
- `ConcentrationLedger.current` stores `(cast_id,on_end_callback)`. A generic deep copy of a closure can retain a binding to the wrong live object graph. An actual restoration adapter must reconnect callbacks to the same restored canonical source instance and verify later concentration ending affects the intended world. Do not call fresh `start_committed` merely to restore a historical slot: that would run ordinary end/start behavior.
- `TransformationWorld` and `DruidState` hold references to the canonical shared `BufferLedger`, and may hold the same `CreatureWorld`. Preserve those aliases. A clone of a buffer or resource ledger is not another authorized pool. Source-specific serializers must distinguish payload fields from references to canonical objects.
- `OwnerRechargeClock` uses real elapsed seconds, monotonic actual regular markers and a six-second outside-initiative phase. Restoring an old integer `last_regular` cannot silently authorize extra ticks. Apply the actual final clock/iteration decision, not generic timestamp rebasing.
- The maximum-HP helper is `tools/maximum_hp_playtest_rules.py`. Stale snapshot maximum/currentHP cannot override conserved gear without the explicit source reconciliation now requested.
- Healing event history and `HealingCommitLedger.consumed_reducer_ids` are different obligations. The latter can conflict with a legally restored same-ID Agony record; implement the reviewed active-iteration/historical distinction only after the boundary answer.
- A complete restoration plan must be constructed and checked before any canonical resources mutate. Exceptions during staging leave the live state, Reaction and long-rest entitlement unchanged. The final commit must use a previously validated plan and preserve world-unique identities. A shallow metadata dictionary with a `complete=True` field is insufficient.

The full web companion runtime is a separate delivery. Its `src/lib/character-storage.js` normalizes saved characters and preserves other raw fields; it is not evidence that full temporal encounter serialization exists.

## Control/pulse integration in progress

The actual next conference is `CODEX_TEMPORAL_CONTROL_PULSE_CONFERENCE.md`:60 exact control records,32 pulse records,3 direct supplemental sources, all33 pulse/native/contact alias mappings, and the complete reviewed control/pulse guides and helpers. `TEMPORAL_CONTROL_PULSE_CONFERENCE_MANIFEST.json` binds the packet to its source hashes. Its nine proposals are not adopted rules until the actual completed reply is recorded.

The first implementation is `tools/temporal_control_playtest_rules.py::CanonicalPulseWallet`, exercised by10 methods in `validate_temporal_control_playtests.py`. It supplies the existing pulse helper's spending interface using the real actor Wallet and Scheduler.rc. It rejects changed canonical bindings, shared Wallet aliases, illegal costs and unavailable actions before payment. The integration tests run actual maintenance, Song of Mending and native recurrence helpers, and check the bridge after an actual foundation restore. This payment bridge does not restore or admit a PulseSeries and does not reduce the seven missing-integration count.

The source adapter must next maintain separate canonical holder references and serialized field payloads. A PulseSeries references one shared RecipientLedger; copying that ledger creates an unauthorized second recipient budget. Its dynamically initialized profile, opens, states and end fields must all be classified. GuidingStarMark's pending attack set must be empty at a complete event boundary. Its UUID identity and token sequence have different temporal roles from its two available entitlements. A source-aware record must carry the parent identity and endpoint; the generic helper type alone is insufficient.

No addition should mutate the reviewed foundation merely to change its status string. When actual integration requires an extension, preserve its reviewed hash and submit the substantive diff with the new tests. The foundation's external concentration map remains a projection; it cannot certify callback-bearing concentration or replace its seven missing source adapters.

## Temporal control/pulse source conference completed; code review in progress

The [actual nine-part response](GPT_TEMPORAL_CONTROL_PULSE_BOUNDARIES.md) settles the source policies. Sacred Chant's Conviction joins Transcendent Meditation's Ki under a conserved independent-output opportunity. Native healing gets one evaluated opportunity at a real regular start; declined, ineligible or unaffordable starts cannot be retried. Rapid Coagulation remains dependent on a missing movement-history adapter.

The [actual incremental code packet](CODEX_TEMPORAL_PULSE_BRIDGE_REVIEW.md) contains22 passing payment/output tests and explicit limits. It asks the notebook to confirm ordinary maintenance retry wording and immutable initiative-start membership. It does not implement full pulse restoration or reduce the seven missing integrations. The current readable guide is `DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md`. No source promotion, deletion or GitHub push occurred.

## Bounded pulse payment/output bridge jointly reviewed

[GPT's actual completed review](GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md) finds no reproducible blocker within the22-test payment/resolved-output scope. Exact reviewed helper SHA256: `835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12`. The code and tests remain unchanged from the submitted packet.

The reply also confirms: early failed ordinary maintenance remains pending until its real deadline; exact-due failed upkeep ends immediately; an after-snapshot source cannot acquire snapshot membership; the supplied pulse profiles normally present at initiative have preserved outside-origin schedules. Native abilities exist at capture, but their healing occurrences do not. Any future exact initiative-creation exception requires its own ordering rule.

Next implementation: authentic regular-start receipts and evaluated native opportunities; source-qualified clock descriptors and same-object restoration; conserved missed-output reconciliation; actual parent/concentration and full resource-application transactions. Rapid Coagulation still requires snapshot movement history. The other six major integrations also remain unfinished. Full Time Loop, whole-game closure and GitHub delivery remain pending; no originals were deleted.

## Live control/pulse transaction candidate submitted

[The actual 36-method submission](CODEX_TEMPORAL_CONTROL_WORLD_REVIEW.md) includes the complete new holder adapter, tests, and a diff from the preserved approved foundation. The original foundation is preserved byte-for-byte as `temporal_playtest_rules_reviewed_foundation.py`; approval still binds that original hash. The current extension also passes the 76 foundation and 22 payment/output checks. No old approval has been transferred to the extension.

The candidate binds selected actual holders to the atomic transaction, verifies aliases and original clocks, requires genuine regular starts, distinguishes target-start Hemostasis, and checks current parent receipts for Bloom/contact benefits. Whole-card/source-parent behavior, outside-initiative round import, final HP/resource mutation and several dependent source families remain unfinished. During review, the source audit also identified Eternal Bloom/Crown Restored's required concentration via `oracle.engine[26]`; a local corrective check is being added and will be included in the next actual packet.

The seven major temporal integrations and whole-game/GitHub gates remain open. No original content was deleted, no catalog status was promoted and no push occurred.

## Bounded live control/pulse transaction closure

The [actual GPT response](GPT_TEMPORAL_CONTROL_WORLD_CLOSURE.md) confirms the exact 50-method revision after the [callback-binding repair](CODEX_TEMPORAL_CONTROL_BINDING_REPAIR.md). It accepts all three same-ID replacement rejection cases and keeps the previous clock, admission, collection, shared-output and Bloom repairs closed. The separate `TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json` binds the exact live adapter, tests, foundation extension and unchanged payment bridge. 50 integration +76 foundation +22 payment/output methods pass.

This closes this bounded engineering checkpoint only. Complete source/parent lifecycles, final HP/Ki/Conviction application, all seven major Time Loop integrations, the full feature and whole-game flow review remain open. The human's conditional GitHub authorization persists; GPT's reference to an authorization gate is recorded as its own wording, not a request for renewed human permission. No original source was deleted and no GitHub push occurred.

## Parent source conference completed

The [actual ten-case conference](GPT_TEMPORAL_PARENT_BOUNDARIES.md) and [Action-budget/cadence clarification](GPT_TEMPORAL_PARENT_CADENCE_CLARIFICATION.md) settle source policies for participant concentration, protected mixed-roster spells, permanent True Polymorph, paid Druid renewals, local/global spending, entry shields, authentic recharge, new-iteration windows, conserved cadence and expired anatomy. Five temporal rules are explicitly labeled new/provisional in the [authored parent guide](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md).

The Action clarification preserves the approved kernel: current turn allowances restore from the snapshot with all outstanding Time Loop Reaction debts; historical activation events and finite resource spending remain recorded. No new generic short-rest Dissonance reset was adopted from loose wording in the reply; actual source-authorized recovery still governs.

`TEMPORAL_PARENT_STATE_INVENTORY.json` accounts for85 actual fields across9 holder types, including Druid fields initialized outside the constructor, and links all26 exact form profiles. This is source/implementation preparation, not runtime validation. The new review-status manifest explicitly leaves parent code, all seven larger integrations, full Time Loop and whole-game approval unfinished. All exact previously reviewed helper hashes remain unchanged. No original content was deleted or pushed.
