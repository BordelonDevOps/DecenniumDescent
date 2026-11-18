# Next module definition: ordinary-world magical activity

Definition ID: **TAC-01-ORDINARY-MAGICAL-ACTIVITY**. Primary workstream: TAC-01; affected consumers: TAC-02, TAC-08 and CHR-05. This is one bounded implementation module, not a new formal workstream.

**Review state: proposed for actual GPT/Codex planning acceptance.** [Planning disposition](PLANNING_ACCEPTANCE.json) will carry the actual verdict. The module definition, source/API calendar amendment and runtime acceptance are three distinct decisions. **The calendar amendment remains OPEN; implementation is paused and unauthorized by this planning task.** No successor profile number is reserved.

## 1. Result to deliver

Close **CG-CONTEXT-01 for existing admitted post-encounter calendars**: an otherwise lawful magical Action outside initiative can execute after the actor's short virtual owner slot ends but before its ordinary Action allowance refreshes, without contradicting activity or Dissonance history.

In the inherited three-seat schedule, an owner Start is `s`, the slot End is `s+2 seconds`, and the next owner Start/ordinary allowance refresh is `s+6 seconds`. The required new-profile witness is a genuinely paid Consecrate at `s+3 seconds`. Removing `ConsecrateOpenOwnerSlotRequired` alone is insufficient: the existing End may already have settled idle/Grounding decay. Even with zero Dissonance, absence of a saved End row does not mean an old slot is open.

The successor must reuse the shared actor state, authoritative commands, clock, seeded RNG, inventory/custody, work, conditions and verified persistence. It must deliver connected gameplay as well as coherent calendar accounting.

## 2. Dependency order and accepted prerequisites

Accepted bounded sequence: geometry113 → Ferry114 → Consecration115. This proposed successor extends that operational sequence under the owner's new planning request. The previous acceptance did not select it. [GPT consultation](GPT_CONSULTATION.json) recommends it; the final planning review must accept its order explicitly.

The formal graph remains unchanged: TAC-01 ← FND-01/FND-02; TAC-02 ← TAC-01/RUL-05; TAC-08 ← TAC-02/TAC-05/TAC-07; CHR-05 ← CHR-03/TAC-02/TAC-05/TAC-08. All 49 rows, 120 edges and 100 completion obligations remain intact. No dependency is declared globally complete from a bounded witness.

These are scoped operational prerequisites and reusable accepted evidence, not new graph edges:

| Accepted slice | Retained acceptance | GPT response |
| --- | --- | --- |
| Ordinary Cleric casting/activity/End | [TAC-08](../2026-11-15-tac08-cleric-casting/GPT_FINAL_REVIEW.md) | `4380847f-3bdc-5003-b5a1-1803a4fed501` |
| Genuine RP funding through Long Rest | [MGT-03](../2026-11-15-mgt03-cleric-long-rest/GPT_FINAL_REVIEW.md) | `0361603a-8572-5112-896a-d04663473407` |
| Post-recovery encounter and allowance carry | [EXP-07](../2026-11-16-exp07-post-recovery/GPT_FINAL_REVIEW.md) | `7ed650ba-0d52-5376-9188-7ee179d7d397` |
| Earned Cleric 3/Bishop, Invocation and Aura | [CHR-03](../2026-11-16-chr03-bishop-runtime/GPT_FINAL_REVIEW.json) | `07ffc865-b1db-5bb0-9204-3e883bc9c559` |
| Declared geometry113 | [TAC-03](../2026-11-16-tac03-declared-geometry-runtime/GPT_FINAL_REVIEW.json) | `9e7360a4-f81d-5f06-8884-49e8ef8eda0a` |
| Ferry114, paid encounter and transitions | [TAC-10](../2026-11-16-tac10-ferry-wraith-runtime/FINAL_ACCEPTANCE.md) | `bc9b7b5d-cbca-5e57-b297-c6fd18cb39db` |
| Consecration115 | [CHR-05](../2026-11-17-chr05-consecration/FINAL_ACCEPTANCE.json) | `a34a0fba-bc6a-51c7-96d3-3a142e4028a7` |

Saint/resurrection remains held by [its prerequisite review](../2026-11-15-tac06-resurrection/GPT_CONTRACT_REVIEW.md), response `50395a8a-f1f7-58ac-81b6-a9e116e35f09`. Cleric 3/Bishop does not supply Cleric 16/Saint ownership, intervening acquisition consequences, death-occurrence/body/soul authority or return-to-schedule integration. Conversely, this module is not a new universal prerequisite for all advancement.

## 3. Authority and precise scope

[Source bindings](SOURCE_BINDINGS.json) pin Git blob IDs, SHA-256 and bytes. Original ReviewBible revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Required source files are `CLASS_PLAYTEST_RULES.md`, `COMBAT_ACTION_PLAYTEST.md` and `class_playtests/cleric.json`. Controlling later policies are separately pinned: shared-world decisions; TAC-08 approved casting contract P3/P4; corrected Consecration source/API contract §2, including CG-CONTEXT-01. These provisional/playtest sources and delegated prototype policies are not production promotion or recovered canon. A new amendment must identify which existing policy it changes, its profile boundary and the actual consensus.

Only a fresh, opt-in successor composition inheriting the accepted115 content is in scope. Check identifier/fingerprint availability before assigning a profile; never edit a115 save into the successor.

The existing admitted context inventory is derived from `WorldTiming.ForActor` and `CurrentCastingTurn`, not client labels:

| Context | Actual epoch binding | Outside admission boundary |
| --- | --- | --- |
| Reinforcement | `Reinforcement.Admission.Phase.Epoch` | Its actual encounter has closed; no live encounter |
| Post-recovery | `PostRecoveryEncounter.Admission.Epoch`, currently `TEST_ONLY.post-recovery-calendar` | Its actual encounter has closed; no live encounter |
| Ferry | `FerryWraith.Admission.Epoch`, currently `TEST_ONLY.ferry-calendar` | Its actual encounter has closed; no live encounter |

Use the epoch actually owning the actor; a retained older epoch is not a second spending opportunity. Include original allowance carry and admission before a first new owner Start. The exact settlement treatment is mandatory decision CAL-03 below. During initiative, preserve actual owned regular-turn admission. Pre-reinforcement/bootstrap calendars and arbitrary roster/calendar construction remain unsupported.

All six existing operations must be explicitly assessed in the amendment, with late outside admission required where their own source and state permit it. Any exception needs a specific source/API reason and actual review; do not silently omit a consumer.

| Operation | Existing semantic class | Required preserved restrictions/effects |
| --- | --- | --- |
| `UseConsecrate` | Magical class activity | Genuine card; Action +2RP; perception/range/effect/center; fixed terrain, source expiry/recharge; no RNG or clock advance |
| `UseHealingRite` | Magical class activity | Genuine grant; Action +2RP; living legal recipient; existing dice, positive-base trigger and Ground → Radiance → Aura settlement |
| `UseDivineInvocation` | Magical class activity | Earned Bishop; Action +3RP +2Conviction; existing target, dice, recharge and protected vent |
| `CastKnownSpell` | Spell activity | Actual known/source-permitted spell; existing Action, RP, components, concentration, target, dice, Dissonance and Refrain rules |
| `FocusDetectedAura` | Magical focus activity | Actual active Detect source/aura and existing focus Action, visibility and focus limits; no invented second casting cost |
| `GroundCastingStrain` | Grounding, not magical activity | Actual Action and existing eligibility; no simultaneous idle/Grounding benefit; source PB reduction only at the approved settlement |

Passive concentration is not newly classified as activity. No new spells, cards, levels, resources, attacks, terrain effects or character grants are introduced.

One shared, versioned activity-context assessment must derive actor/epoch/allowance/clock identity from authoritative state. Clients cannot supply a paid flag, activity class, interval or completed End. No independent activity-payment command is introduced. Existing `ConnectedExpeditionSession.Submit`, `QueryCastingCommand`, `DiscoverCastingCommands`, seat-filtered observations, console dispatch, `Save`, `Restore` and `RecoverBackup` must agree. Query/discovery remains pure and deterministically ordered.

Principal existing seams: `SharedSpellCasting.cs`, `SharedConsecration.cs`, `SharedResonance.cs`, `SharedDivineInvocation.cs`, `SpellCastingRecords.cs`, `SpellCastingValidation.cs`, `WorldScheduleRecord.cs`, `LaterEncounterRecords.cs`, snapshot codecs and verified receipt restoration. Integration must preserve shared Action/RP/Conviction, conditions, exact positions, component custody, busy-work/traversal exclusions, pending choices and genuinely elapsed compatible work. Context changes never refill or reset anything.

## 4. Mandatory source/API calendar amendment before coding

**All five decisions are OPEN.** The module definition can be accepted as a plan with these explicit prerequisites; it is not an executable implementation contract until the decisions and source-derived expectations are accepted by actual GPT review plus Codex concurrence.

| Decision | Required written disposition before implementation |
| --- | --- |
| CAL-01 — interval identity | Exact outside activity interval identity, opening/closing boundaries and relation to Action refresh; source/policy rationale and new-profile-only binding |
| CAL-02 — settlement | Exact idle/Grounding settlement, late magic and zero-Dissonance/no-End-row behavior; prove no retrospective reversal or double reduction |
| CAL-03 — transitions | Entry, closure, carried allowance and transition before the next owner Start, across all three admitted contexts; bind activity provenance and avoid fictitious future turns |
| CAL-04 — event order | Exact order versus regular markers, condition/life events, effect expiry, recharge, work completion and pending choices; whole/partitioned advance equivalence |
| CAL-05 — consumer/API matrix | Exact changed admission checks for all six operations, causal record/codec/version semantics, deterministic discovery and historical compatibility |

A versioned actor-interval design derived from the shared calendar is an investigation candidate, not an approved mechanic. Existing shared-world policy ends a slot at the next actor Start; P4 settles idle/Grounding there. No permission is given to move regular Ends, invent a second clock or change those facts by implication.

Stop and resolve with GPT if a design erases a settled End, undoes applied decay, reassigns past activity, uses a fictitious future turn, grants an extra allowance, resets a deadline, weakens restore authenticity or silently changes an old profile. If consensus cannot resolve a source gap, report the precise unresolved rule under the existing owner escalation policy.

## 5. Concrete runtime acceptance criteria

These are future obligations, **not passes reported by this documentation task**.

| ID | Required demonstration and retained evidence |
| --- | --- |
| OMA-01 | CAL-01 through CAL-05 closed in one versioned source/API amendment, with exact source clauses, decision IDs, public API/record changes, expected boundary outcomes and actual GPT/Codex acceptance before coding. Profile availability checked. |
| OMA-02 | Fresh successor genesis follows lawful explore → encounter → acquire → manage/fund → prepare → actual closure → Consecrate at s+3 → meaningful terrain consumption → genuine transition → paid ordinary continuation. Retain complete commands, receipts, actual spending/RNG/deadlines and named checkpoints. No edited115 save, fabricated funding/damage/history or injected allowance. If one route cannot realize every interaction, keep genuine branches and parent checkpoints separate. |
| OMA-03 | Genuine nonzero Dissonance plus late magical activity prevents inappropriate idle/Grounding gain under the accepted amendment. Also demonstrate idle, Grounding, zero-Dissonance/no-End-row and every changed operation/classification. Validate semantic equivalence before sharing a handler witness; an unexercised consumer is not covered by naming it. |
| OMA-04 | For each admitted context: before/at/after old slot End; just before/at next owner Start; Action already spent; original recharge ready/not-ready; zone expiry/replacement ties; admission/closure before next owner Start. Whole versus partitioned time advancement gives identical ordered results, canonical state and RNG. Preserve original endpoints and no extra allowance. |
| OMA-05 | Actual busy work, traversal, incapacity, concentration, components, pending decisions and source target restrictions remain authoritative. Compatible work progresses exactly once; incompatible work keeps its defined pause/cancel behavior. No context-selection RNG, resource recovery, duplicated stock/reservations or timer reset. |
| OMA-06 | Query/discovery and execution agree for all six operations; pure reads preserve canonical state/RNG. Wrong/revoked seats, stale revision, conflicting IDs/payloads, illegal targets and exhausted record capacity reject atomically, with filtered diagnostics. Persisted authorized receipt retry is qualified separately from a direct helper repeat denial. |
| OMA-07 | Save/verified restore during an open outside interval, after late activation, before/after settlement and across a real epoch transition; continue ordinary play and recover backup. Reject causal forgeries of interval, activity, End, payment, allowance, source or transition history even with recomputed checksums. Preserve the existing supported historical matrix and authentic115 saves/receipts/continuation without backfilled semantics. |
| OMA-08 | Run five complete modes from the lawful successor start to continued play: console uninterrupted, console restored, typed uninterrupted, typed restored, persisted receipt replay. Compare canonical state, RNG, filtered views and ordered discovery at named equivalent checkpoints covering the new gap, settlement and transition. A driver file or one terminal state is insufficient. |
| OMA-09 | Preserve the 1,587 predecessor case inventory with exact disposition; add meaningful source-derived cases for this module. Reconcile affected/full required regressions against one new frozen runtime. Retain every failure and correction with actual terminal results. Old accepted qualification remains intact; a new-runtime run does not replace or reopen the TAC-10/Consecration acceptances. |
| OMA-10 | Retain source/policy hashes, exact changed files, compiler/version/options, C#9 warnings-as-errors, runtime/console/test inputs and DLL identities, required package checks and actual results, connected/path/compatibility evidence and unresolved-capability ledger. Actual final GPT review of the frozen candidate and Codex concurrence must accept every obligation before any successor. |

New genuine-witness blockers must be reported with a finite lawful investigation and retained result. Any mechanical supplement needs explicit new allocation; no automatic inheritance from prior cure allocations. The accepted TAC-10 and Consecration cure dispositions remain closed within their exact scopes; this module does not restart those searches.

## 6. Phase boundaries and exclusions

1. **Current task:** agree this module definition/order/scope/acceptance; validate and publish documentation to Engine; report the verified GitHub commit to GPT. No gameplay/build/benchmark runs or runtime edits.
2. **Before implementation:** resolve and review CAL-01–05, exact source/API contract and prospective evidence plan. Runtime work also requires the owner's further instruction lifting the implementation pause.
3. **When authorized:** implement the one bounded module, freeze runtime, retain source/build/test/connected evidence, resolve concrete blockers and obtain actual final GPT/Codex acceptance. Commit exact changed files after the module; do not begin a successor without its gate.

Excluded: bootstrap/pre-reinforcement casting, arbitrary rosters, broader advancement, Saint/resurrection, new spells/abilities, general production authority, storage cleanup, GitHub Support and Unity integration. Mandatory excluded capabilities remain open in the unchanged [pre-Unity completion contract](../../PRE_UNITY_COMPLETION_CONTRACT.md).

UR-01 through UR-08 retain their existing dispositions. Full capability/identity/interaction closure, performance qualification, source authority and whole-engine review are still required. Defining or accepting this module cannot establish Unity readiness. [Current implementation map](../../IMPLEMENTATION_MAP.md) distinguishes accepted Consecration115 from this planned successor.
