# Temporary Camp construction contract

**Status:** Codex/GPT agreed on 2026-11-09 that the next bounded MGT-03 dependency is one TEST_ONLY FL-07 Temporary Camp construction profile. Implementation is authorized within this contract. This is not a production rule approval and does not complete MGT-03 or the engine.

## Pinned source authority

- ReviewBible revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.
- Player Book blob: `466871fc128dc5f06043a874da2b9c1d94ed80a5`.
- Pinned Player Book SHA-256: `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`.
- [FL-07 — Building and using a camp](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-07) supplies the site, work, check, mark, material, fixture and storage requirements.
- [FL-03 — One clock, work and rest](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-03) supplies one elapsed clock, incompatible-work scheduling, trained assistant bonuses and the generic 480-active-minute completion-check timing.
- The same pinned source lists route-tier DCs I 12, II 13, III 15, IV 16, V 18 and VI 19 in its route-check procedure. FL-07 says “tier DC” without explicitly binding camp construction to a route tier; the binding below is an explicit TEST_ONLY completion.

## Responsibilities

Implement one source-bound but explicitly TEST_ONLY Temporary Camp construction attempt at one existing schema69 `ExpeditionCampSiteRecord`. Reuse the actual site, route/checkpoint, character, work, inventory, clock, RNG, command receipt, snapshot and persistence authorities. The build adds neither route movement nor a second position or worker system.

The authored fixture is for one two-person camp. It requires one actual two-person tent and one actual Temporary fitting pack. The site itself must independently meet FL-07's legal access, stability, drainage, weather-protection, inhabitant-space, gear-space and 20×20-foot requirements. The profile cannot change site exposure, concealment, enemy knowledge, safety or Haven facts.

## Source requirements

- One build task uses 480 active Support minutes.
- The lead makes a STR or WIS check using an actually relevant tool or Survival proficiency against the tier DC.
- Up to three trained assistants can help. The generic FL-03 task rule gives each meaningful trained assistant +1; assistance does not shorten task duration.
- Success earns one build mark; Critical Success earns two; failure earns none.
- Required materials are reserved before work, and installation is recorded. Failure spends time and only goods actually damaged or used. Feasible unfinished physical progress survives pause.
- Temporary Camp requires one Support mark, real sleeping shelters, and the fitting pack (20 lb / 2 gp). Its storage limits are 20 Load, 200 lb and 20 ft³. The fitting pack provides rope, pegs, ground covering and racks. Tents and bedrolls are separate items; the pinned source two-person tent weighs 20 lb / costs 2 gp and holds two Small/Medium sleeping places.

## Existing authorities and implementation dependencies

- Existing schema69 `ExpeditionCampSiteRecord` and `ExpeditionCampActivityRecord`; existing route fixture and `WorldPositionResolver` remain authoritative for site and actor position.
- `RuleClock`, `WorkLedger`, `WorkerInterval`, `ResourceLot` and `ResourceReservation` remain authoritative for time, worker booking, physical stock and exclusive claims. Use the existing work progress/pause and reservation patterns in `SharedToolRepair` and `SharedManufacturing`; do not add another scheduler or material ledger.
- `ActorCharacterRecord`, `SkillTrainingRecord`, `CharacterStateFacts`, `AbilityCheckRules.Derive`, `RuleResolution.TaskCheck` and `RuleDice` remain authoritative for the declared method, character facts, result degree and deterministic roll evidence. Registration does not grant skill proficiency.
- `Snapshot.Copy`, simulation validation, command receipts and `SnapshotCodec` remain authoritative for transactions and replay. Construction adds persistent records, so the implementation uses additive schema70 encoding. Schema69 and earlier bytes/behavior remain in their existing branches.

New state is limited to the fingerprinted TEST_ONLY construction profile; fixed-team attempt and work-progress state; reservation links; causal check/result evidence; earned marks; and links to the installed physical lots. Derive Temporary Camp completion and its limits from the earned mark and required installed fixtures; do not add a duplicate camp grade or duplicate quantities. An installed tent or pack remains a physical lot: `WorkLedger.Consume` would delete quantity and is not installation. Keep installed fixtures under durable installation-linked exclusive claims, preserving their actual identities, ownership, custody and quantity. They cannot remain available for ordinary handling or another build. Dismantling is unsupported.

## Agreed TEST_ONLY completions

These fill source gaps only for the finite fixture and are not quotations or production canon.

1. **Tier and method:** The route record has no Tier field. The fingerprinted construction profile binds an explicit tier to its route ID, using the pinned tier table. Do not infer tier from Risk or Quality and do not change historical route fingerprints. The profile/attempt locks the lead's STR/WIS and relevant Survival/tool method before work starts. Actual character training is required where the method calls for it.
2. **Fixed crew and work timing:** Use one fixed lead and up to three fixed, qualified assistants. Credit only clock intervals covered by the required workers' actual bookings; helpers add their qualified bonuses but do not reduce the 480-minute duration. Pause cancels future worker bookings while retaining feasible progress and material claims. Resume revalidates workers, site, method and stock.
3. **Check ordering:** Resolve one check only after 480 active minutes. At the exact completion endpoint, credit work, process due effects, revalidate the task and lead, then roll once. Preserve causal character/condition facts and RNG evidence. If completion-time incapacity prevents the check, retain completed work as awaiting revalidation; do not roll through incapacity or charge another eight hours.
4. **Fixtures and marks:** One 20 lb two-person tent plus one 20 lb fitting pack provides the required 40 lb of physical fixtures for this authored two-person camp. Their 2 gp source prices are references, not purchase debits. Any actual tool required by the chosen method is separate. Temporary Camp exists only when at least one Support mark and both fixture installations exist. Critical Success retains both earned marks but grants no higher tier or outpost/safety/concealment benefit. Its three storage limits are simultaneous constraints and create neither contents nor a storage-transfer handler.
5. **Failure:** The first fixture declares no goods damaged or used on failure. Success, failure and critical failure all spend the completed work time. Failure/critical failure earns no marks, installs nothing, preserves all goods and releases unused claims. The failed attempt is immutable. Any later retry, if admitted, is a new full-duration attempt, never another check on completed work.
6. **Camp-use/Pressure boundary:** Construction itself creates no camp-use interval or Pressure cause. Construction conflicts with lying-low for its workers through the existing work/camp assessment. Afterward, only actual existing camp-use/lying-low intervals invoke the accepted Pressure rules; the build cannot modify exposure facts.

## Runnable acceptance scenario

Use the existing route and schema69 camp site, actual test characters and skill records, an actual two-person tent lot and fitting-pack lot already at the site, and a fixed lead/assistant team. No purchase or currency debit is claimed.

1. Start the construction task. Prove that required worker and material claims are committed atomically, reserved/installed fixture lots cannot be handled or claimed by a competing job, and construction conflicts with lying-low for its participants.
2. Advance to half the required active work, pause, advance elapsed time while paused and prove work does not increase. Save/restore, resume with only remaining work booked, and complete at 480 active minutes. Compare against an uninterrupted branch for equivalent progress and outcomes; different command histories need not have identical receipts or snapshot bytes.
3. On a deterministic success branch, validate once-only STR/WIS/tool/Survival resolution, RNG and causal evidence, one/two marks, retained tent/pack identities and quantities under installation claims, ownership/custody, and all three derived capacity limits. Complete the appropriate actual use command and show the existing Pressure category continues without construction changing exposure.
4. On a deterministic failure branch, validate spent time, no mark or installation, unchanged physical quantities and released unused claims. Duplicate submission and replay must not award twice. Byte-identical snapshots and receipt replay are required between restored branches running the same command history.

## Excluded work and unresolved capabilities

Fortified Outpost, Research Station, Forward Base, higher-tier mark spending, general construction/site authoring, arbitrary item acquisition or currency payment, general storage transfer/containment, dismantling, off-route construction, dynamic safety/concealment/discovery, guard scheduling, and production/release authority remain outside this increment. Additional adversarial restore mutations are optional hardening. Unity gameplay integration remains deferred.

## Actual Codex/GPT agreement

GPT reviewed the pinned clauses, current map/handoff, route/profile definitions, inventory provenance, `WorkLedger`, and existing work/check patterns. It identified two needed corrections to the proposal: route records have no Tier, so the explicit binding belongs in the construction profile; and `WorkLedger.Consume` debits a physical lot, so installations must retain actual lots under exclusive claims. GPT agreed to the contract above, confirmed no owner escalation is needed, made no repository changes, and ran no compilation or tests. Its actual review is preserved in the Unity Rules Engine Development chat on 2026-11-09.
