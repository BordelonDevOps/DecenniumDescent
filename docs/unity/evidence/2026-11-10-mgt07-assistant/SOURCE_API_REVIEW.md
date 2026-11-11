# MGT-07 extraction assistance: GPT source/API contract review

**Status:** GPT approved the bounded contract for implementation on 2026-11-10. This is source/API agreement only; no MGT-07 code or tests were changed or run as part of the review. Implementation acceptance remains a separate gate.

**Conversation:** ChatGPT in-app browser, project chat “Draft MGT05 API Contract.” The actual response heading was “MGT-07 mining assistance — source/API contract agreed.”

## GPT’s actual disposition

GPT approved an extraction-only increment: one predeclared trained assistant accompanies the lead through the complete exposed-node extraction task and contributes exactly +1 to the single check. The contract uses a fixed-team pause/resume model, an explicit TEST_ONLY profile and schema77. Prospecting assistance, both assay paths, standalone mineral-preparation assistance, and assisted expedition assignments remain outside this increment.

GPT confirmed MGT-05A/B/C and MGT-06 remain accepted, identified MGT-07 as the active mapped gate, and found no source conflict requiring an owner ruling. It said it made no repository changes and did not execute gameplay code or tests. It inspected the pinned Mining and shared Gathering guides and the relevant Mining, WorkLedger, training, route-team, command-history and persistence APIs at code head `3405eac15b9deff4772ce66b913cc9df255e499c`. It did not independently recompute the supplied source SHA-256.

The detailed agreed boundaries and acceptance criteria below record the substance of GPT’s complete response; the in-app conversation retains the full response.

## Pinned source authority

The Mining candidate guide is pinned at source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, canonical path `DescentReviewChanges/ReviewBible/docs/mechanics/MINING_CANDIDATE_GUIDE.md`, SHA-256 `726cb84a1104901f5b05b412039b458af5bb5168e4482fb9e9844b1b42b697c3`. It states: “One trained assistant working the full information or extraction task can supply +1; the assistant’s item magic does not transfer.” The source also bounds exposed extraction to its predeclared finite selection, existing lead ability choice, duration and single resolution.

The shared Gathering candidate guide is pinned at the same revision, canonical path `DescentReviewChanges/ReviewBible/docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md`, SHA-256 `9b1e4defcd18569ad8d8305552ad740e62be1faea3e1de448e364bd7536215bc`. It says equipment ownership does not confer training, work time/access/hands/workspace cannot be double-counted, a pause preserves progress and claims absent an event that undoes them, and an assistant’s magical item bonus does not transfer.

These are reviewed operational playtest sources. The implementation remains TEST_ONLY and does not promote them to release authority.

## Agreed module contract

### Scope and existing authorities

- Apply the assistance mechanic to direct `StartMining` exposed-node extraction only. The optional empty assistant choice preserves the solo control.
- Reuse `MiningSelectionRequest`, `MiningAttemptRecord`, `SharedMining`, `MiningCodec`, `CommandHistory`, `WorkLedger`, shared `RuleClock`, `Authority`, RNG, command receipts, finite mineral units, inventory provenance and receiver settlement.
- Extend the current request and attempt rather than adding another assistant job or scheduler. Persist each participant’s active work in `WorkLedger`; credit task progress once, not once per participant.
- Do not copy the route-mapping rule that allows up to three assistants or scales its bonus by team size. Its synchronized booking/pause behavior is a code precedent only.

### Training, lead and equipment rules

- Bind “trained assistant” to `CharacterSkillTrainingFacts.IsTrained(snapshot, assistantId, "mining-tools")`, meaning an existing persisted `SkillTrainingRecord` with rank greater than zero. This is the smallest supported source-to-API binding and is explicitly TEST_ONLY.
- Proficiency rank 1 or 2 qualifies; neither gives more than +1. Do not add the assistant’s proficiency bonus, ability modifier, expertise multiplier, level or another die.
- Preserve the lead’s current ability, proficiency, DC, tools, selection, receiving constraints and disadvantage. Do not reject an otherwise-admissible untrained lead just because the task is assisted. The special untrained-lead WIS rule applies to ordinary Mining information tasks; exposed extraction retains its own Strength-or-Wisdom selection.
- Both participants must be physically capable of their assigned work at the deposit and pass existing access, work-conflict, movement, hands and worksite checks. Do not allow two workers to claim simultaneous exclusive use of one implement. Do not invent a second-toolkit requirement where the source does not require one.
- The lead remains responsible for its own item and equipment effects. The assistant’s equipment cannot enter the lead’s check, reserve recovery or preparation-benefit selection merely because the assistant participates.
- At start and resume, the trusted authority must control both booked participants. This is a TEST_ONLY authorization binding, not source text. Do not infer control from a supplied assistant ID or invent assistant consent/hiring.

### Full-task timing and interruption

- Membership is selected on the original start command and persists unchanged. No late joining, replacement, removal or conversion of a solo attempt to assisted work.
- “Full task” includes setup, removal, and sorting/receipt for the complete existing applicable duration. Existing full, partial-category and feasible hurried duration calculations remain unchanged.
- Book matching lead and assistant intervals for the same remaining duration under the same mining job ID. Reserve the mineral allocation once. Reject overlapping work across the entire proposed interval, including future bookings, during shared assessment so query and execution agree.
- Adopt fixed-team pause as an operational TEST_ONLY completion because the Mining source does not specify whether the lead can continue alone. Loss of either participant’s work eligibility pauses the attempt at the event boundary, credits only the preceding valid joint segment, truncates both future bookings, and preserves earned work and material claims. Resume requires the same eligible pair and books the same remaining duration for each. Paused clock time credits neither worker.
- After the full joint duration is earned, preserve the assistance qualification while the attempt is `AwaitingCheck`; a later delay does not demand additional assistant work or erase completed participation. Resolve once through the existing lead check; the assistant causes no RNG draw.

### Records, command-history and save compatibility

- Add optional scalar `AssistantId` to `MiningSelectionRequest`; empty means solo. Persist the fixed identity on `MiningAttemptRecord`.
- Store settled `AssistantBonus` on the attempt/check result as 0 before resolution or on solo resolution, and 1 for a completed qualified assisted check. This is immutable result evidence, not a mutable qualification cache.
- Use a new `mining-selection-v2` request fingerprint only when an assistant is present. Preserve the no-assistant `mining-selection-v1` fingerprint byte-for-byte. Add explicit v2 parsing in `CommandHistory`; retain strict canonical reconstruction and existing receipt bounds.
- Reject a nonempty assistant inside expedition-assignment mining requests; do not silently omit it or change the existing `expedition-mining-assignment-v1` format. Solo assignments remain unchanged.
- Add explicit schema77 TEST_ONLY mining-assistance profile and fingerprint. Append assistant identity and settled bonus to MiningAttempt encoding only under schema77. Older schemas decode empty/zero. Preserve schema43–49 layouts and all existing schema50–76 profiles, fingerprints, solo semantics and replay. Do not migrate, retag or discard assistant data.

### Required integration points

The implementation must extend `AssessMiningCommand`/`MiningAssessment` for participant identity, training, trusted authority, physical eligibility and complete-interval overlap. `BookMining`, pause/resume compatibility and mining boundaries must understand matching pair intervals. `CreditMiningWork` must validate both intervals and increment progress once. `ResolveReadyMining`/`FinishMiningCheck` must apply exactly one assistance point only after complete joint labor. `MiningValidation.ValidateAttempt` must validate matched interval history and reject missing, extra, mismatched or double-counted participant intervals. `WorldActivityProjection` must represent the helper as active work. Request, receipt-history parser, codec and profile selection must use the versioned bindings above.

## Agreed runnable acceptance

Proposed registration names (they do not yet exist):

| Case | Required witness |
| --- | --- |
| `mgt07_extraction_assistant_full_task_bonus_save_restore_replay` | Real exposed parcel, trained helper, unchanged full duration, paired labor, exactly +1 in persisted check, real receiver settlement, mid-work save/restore and identical command replay. |
| `mgt07_extraction_assistant_team_pause_resume_and_interruption` | Positive paused-time gap, paired booking truncation, no paused credit, same-pair resume, actual admitted eligibility-loss interruption, retained work and mineral claims. |
| `mgt07_extraction_assistant_rejects_invalid_training_authority_and_overlap` | Reject self, unknown, untrained, unauthorized, inaccessible and busy helper, including future-interval overlap; query/execution agreement and unchanged state. |
| `mgt07_extraction_assistant_preserves_lead_rules_and_blocks_magic_transfer` | Solo/assisted control, rank 1 and rank 2 both yield only +1, untrained lead retains its existing no-proficiency/disadvantage behavior, helper’s actual magical tool does not affect the lead. |
| `mgt07_extraction_assistant_once_only_check_and_finite_settlement` | Success and failure, one check/claim, no duplicate stock/output, exact retry after restore and conflicting command-ID rejection. |
| `mgt07_extraction_assistant_schema_history_and_team_validation` | Reconstruct v2 request, schema77 roundtrip/continuation, historical schema43–49 regression coverage, forged assistant/progress/interval rejection, nested assisted assignment rejection. |

Primary connected scenario: start with a full non-hurried authored finite deposit; book the pair; credit partial work; save/restore; pause over a positive clock gap; resume the same pair; complete and settle into the actual receiver. Assert both workers have the complete task duration, while `WorkDone` advances only once; check exact selected units, amounts, provenance and location. Compare a solo branch from identical starting facts and seed in a separate simulation because current mining validation permits one attempt per deposit. Assert `assisted CheckModifier = otherwise-equivalent solo CheckModifier + 1`, with unchanged lead ability/proficiency/DC/dice-selection rules. Use a seed avoiding a result-specific critical-failure side path for clean RNG comparison and retain separate failure coverage. Byte identity is required for identical command sequences, not branches with deliberately different pauses or clock advances.

## Explicit exclusions and gaps

Prospecting assistance, nondestructive and destructive assay assistance, standalone mineral-preparation assistance, assisted expedition assignment, late join/replacement/drop-to-solo, hiring/autonomous assistants, deposits/material creation, broader hazards/renewal, production authority and Unity remain deferred. Source-silent edges resolved for this TEST_ONLY module are fixed-pair pause/resume, trusted control of all booked participants, and retention of already-earned full-task assistance after work completes. No disagreement or owner ruling remains at the source/API gate.

## Final disposition

GPT’s actual conclusion: “the MGT-07 extraction-only, one-trained-assistant contract and acceptance gate are agreed and ready for implementation under the existing standing authorization.” The eventual code and retained evidence still require GPT implementation acceptance before another mapped dependency begins.
