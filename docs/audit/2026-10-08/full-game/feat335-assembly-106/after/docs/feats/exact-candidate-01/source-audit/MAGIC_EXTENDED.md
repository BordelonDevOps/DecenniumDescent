# Magic Extended — source reconciliation

Derived complete-text assembly 106; exact parent review and integration pending.

Original source decisions below are historical receipts. The complete current candidate procedure and linked complete case review control this derived reading.

## MX-01 — Arcane Armor

### Complete original object

```json
{
  "id": "arcane_armor",
  "name": "Arcane Armor",
  "description": "A caster reinforces their defenses with a brief arcane ward while shaping a spell.",
  "prerequisite": "Level 4",
  "effect": "While you are casting or concentrating on a spell, gain a +1 bonus to AC and saving throws against reactions triggered by that casting.",
  "type": "Magic",
  "legacyEffect": "+5% resistance while casting",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve whether the reaction-trigger qualifier limits both AC and saves, or only saves, and what concentrating contributes after casting ends. Identify casting-triggered reactions, onset before interruption, exact expiry, stacking and level4 gate. Preserve inactive+5-percent legacy text without turning the ward into general resistance."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcane_armor",
  "name": "Arcane Armor",
  "cohort": "magic_extended",
  "questionId": "MX-01",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/0",
  "originalQuestion": "Resolve whether the reaction-trigger qualifier limits both AC and saves, or only saves, and what concentrating contributes after casting ends. Identify casting-triggered reactions, onset before interruption, exact expiry, stacking and level4 gate. Preserve inactive+5-percent legacy text without turning the ward into general resistance.",
  "originalSourceObject": {
    "id": "arcane_armor",
    "name": "Arcane Armor",
    "description": "A caster reinforces their defenses with a brief arcane ward while shaping a spell.",
    "prerequisite": "Level 4",
    "effect": "While you are casting or concentrating on a spell, gain a +1 bonus to AC and saving throws against reactions triggered by that casting.",
    "type": "Magic",
    "legacyEffect": "+5% resistance while casting",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "ff51dd1251fc19cbd5488ec361412ec08c9e6821a59eeda9b95d3af0a5eb2357",
  "submittedProcedure": "Require character level 4. NEW the qualifier governs BOTH+1 AC and+1 saving throws: they apply only against a Reaction whose actual printed trigger is your casting or continuing concentration on a spell. Begin eligibility at commitment of that cast, before interruption; end when its casting/held concentration/ordinary concentration ends. Merely attacking a concentrating caster is insufficient. The relevant Reaction must itself cause an attack against you or a save you make; Counterspell’s caster-side ability check is neither and receives no penalty. A triggered attack still uses ordinary critical rules. The bonus is passive, grants no Reaction, and cannot protect unrelated attacks or ongoing damage. Current same-stat bonus arbitration applies. Preserve the alternative broad AC reading and old 5% resistance as inactive source alternatives.",
  "submittedNewChoices": "Both bonuses are narrowly trigger-qualified, including an expressly concentration-triggered Reaction; no general AC or resistance.",
  "submittedWorkedCases": [
    "An actual on-cast Reaction attacks AC 14: eligible+1 makes AC 15, unless a stronger same-stat bonus already governs.",
    "An enemy’s ordinary attack during your ongoing concentration receives no Arcane Armor modifier."
  ],
  "decision": "Adopt the narrow grammatical scope on both AC and saves: only casting-triggered Reactions, not all attacks during concentration; keep+1, not legacy percentage resistance.",
  "completeAuthoringProcedure": "Require character level 4. NEW the qualifier governs BOTH+1 AC and+1 saving throws: they apply only against a Reaction whose actual printed trigger is your casting or continuing concentration on a spell. Begin eligibility at commitment of that cast, before interruption; end when its casting/held concentration/ordinary concentration ends. Merely attacking a concentrating caster is insufficient. The relevant Reaction must itself cause an attack against you or a save you make; Counterspell’s caster-side ability check is neither and receives no penalty. A triggered attack still uses ordinary critical rules. The bonus is passive, grants no Reaction, and cannot protect unrelated attacks or ongoing damage. Distinct eligible flat feat bonuses add under FS-03 after existing non-feat families resolve; duplicate Arcane Armor contributes only once. Preserve the alternative broad AC reading and old 5% resistance as inactive source alternatives.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An actual on-cast Reaction attacks AC 14: eligible+1 makes AC 15, unless a stronger same-stat bonus already governs.",
    "An enemy’s ordinary attack during your ongoing concentration receives no Arcane Armor modifier."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require character level 4. NEW the qualifier governs BOTH+1 AC and+1 saving throws: they apply only against a Reaction whose actual printed trigger is your casting or continuing concentration on a spell. Begin eligibility at commitment of that cast, before interruption; end when its casting/held concentration/ordinary concentration ends. Merely attacking a concentrating caster is insufficient. The relevant Reaction must itself cause an attack against you or a save you make; Counterspell’s caster-side ability check is neither and receives no penalty. A triggered attack still uses ordinary critical rules. The bonus is passive, grants no Reaction, and cannot protect unrelated attacks or ongoing damage. Distinct eligible flat feat bonuses add under FS-03 after existing non-feat families resolve; duplicate Arcane Armor contributes only once. Preserve the alternative broad AC reading and old 5% resistance as inactive source alternatives.

### Original-position authored review references

```json
[
  {
    "id": "MX-01-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/0"
  },
  {
    "id": "MX-01-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/1"
  }
]
```

## MX-02 — Arcane Flexibility

### Complete original object

```json
{
  "id": "arcane_flexibility",
  "name": "Arcane Flexibility",
  "description": "Careful preparation leaves room to exchange one readied spell when the party rests.",
  "prerequisite": "Intelligence 15+",
  "effect": "When you finish a short rest, exchange one prepared spell for another spell of the same tier that your class can prepare.",
  "type": "Magic",
  "legacyEffect": "Swap one prepared spell per rest",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind prepared spells to an actual class repertoire and same class-specific rank; specify completed Short Rest, replacement timing, losing a currently maintained spell and temporary/copied grants. Does this permit a class without prepared spells to prepare one? Preserve the existing acquisition limits and no imported preparation subsystem."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcane_flexibility",
  "name": "Arcane Flexibility",
  "cohort": "magic_extended",
  "questionId": "MX-02",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/1",
  "originalQuestion": "Bind prepared spells to an actual class repertoire and same class-specific rank; specify completed Short Rest, replacement timing, losing a currently maintained spell and temporary/copied grants. Does this permit a class without prepared spells to prepare one? Preserve the existing acquisition limits and no imported preparation subsystem.",
  "originalSourceObject": {
    "id": "arcane_flexibility",
    "name": "Arcane Flexibility",
    "description": "Careful preparation leaves room to exchange one readied spell when the party rests.",
    "prerequisite": "Intelligence 15+",
    "effect": "When you finish a short rest, exchange one prepared spell for another spell of the same tier that your class can prepare.",
    "type": "Magic",
    "legacyEffect": "Swap one prepared spell per rest",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "91dcda8344af3e705d0f9e4bcd4a84306f0fa856e850bcacb4f15029a5203f47",
  "submittedProcedure": "At completion of each beneficial Short Rest, optionally replace exactly one currently prepared spell in one actual class preparation list with another spell of the same rank in that same class. It must already be a legal known/book/repertoire choice under that class’s preparation procedure and current class level/school limits. Decide after ordinary rest endpoints/recovery; record the previous and replacement preparation. No extra prepared capacity, learned spell, copied grant or class alias. A class without a preparation list gains no new list. NEW unpreparing does not retroactively dispel a legally ongoing spell; maintain its actual concentration/deadline, but no new cast through the removed preparation. One exchange per rest event across classes, not one per class or duplicate feat representation.",
  "submittedNewChoices": "One character-wide exchange and preservation of already established effects, without inventing preparation access.",
  "submittedWorkedCases": [
    "A Wizard exchanges one prepared Wizard-rank 2 spell for another already eligible Wizard-rank 2 spell after SR.",
    "Knowing the replacement through another class at rank 2 does not establish Wizard preparation eligibility."
  ],
  "decision": "Keep one actual same-rank owned repertoire substitution at a beneficial short rest; no class-list union, free knowledge or duplicate selection.",
  "completeAuthoringProcedure": "At completion of each beneficial Short Rest, optionally replace exactly one currently prepared spell in one actual class preparation list with another spell of the same rank in that same class. It must already be a legal known/book/repertoire choice under that class’s preparation procedure and current class level/school limits. Decide after ordinary rest endpoints/recovery; record the previous and replacement preparation. No extra prepared capacity, learned spell, copied grant or class alias. A class without a preparation list gains no new list. NEW unpreparing does not retroactively dispel a legally ongoing spell; maintain its actual concentration/deadline, but no new cast through the removed preparation. One exchange per rest event across classes, not one per class or duplicate feat representation.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A Wizard exchanges one prepared Wizard-rank 2 spell for another already eligible Wizard-rank 2 spell after SR.",
    "Knowing the replacement through another class at rank 2 does not establish Wizard preparation eligibility."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At completion of each beneficial Short Rest, optionally replace exactly one currently prepared spell in one actual class preparation list with another spell of the same rank in that same class. It must already be a legal known/book/repertoire choice under that class’s preparation procedure and current class level/school limits. Decide after ordinary rest endpoints/recovery; record the previous and replacement preparation. No extra prepared capacity, learned spell, copied grant or class alias. A class without a preparation list gains no new list. NEW unpreparing does not retroactively dispel a legally ongoing spell; maintain its actual concentration/deadline, but no new cast through the removed preparation. One exchange per rest event across classes, not one per class or duplicate feat representation.

### Original-position authored review references

```json
[
  {
    "id": "MX-02-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/2"
  },
  {
    "id": "MX-02-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/3"
  }
]
```

## MX-03 — Arcane Pulse

### Complete original object

```json
{
  "id": "arcane_pulse",
  "name": "Arcane Pulse",
  "description": "Condensed force erupts around the caster, driving nearby foes away from the blast.",
  "prerequisite": "Level 7",
  "effect": "As an action, spend 3 RP to release force in a 10-foot radius. Creatures of your choice make a Strength save against your spell save DC, taking 3d6 force damage and being pushed 10 feet on a failure, or half damage without the push on a success.",
  "type": "Magic",
  "legacyEffect": "AoE force blast knocks back enemies",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define spell versus nonspell classification, casting ability/DC for a level7 character without casting, actual shared RP access and payment. Specify self-centered10-foot geometry, sight/line, chosen targets including self, one damage roll, Strength save, push direction/collision and half rounding. No resource pool is created by an unstated prerequisite."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcane_pulse",
  "name": "Arcane Pulse",
  "cohort": "magic_extended",
  "questionId": "MX-03",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/2",
  "originalQuestion": "Define spell versus nonspell classification, casting ability/DC for a level7 character without casting, actual shared RP access and payment. Specify self-centered10-foot geometry, sight/line, chosen targets including self, one damage roll, Strength save, push direction/collision and half rounding. No resource pool is created by an unstated prerequisite.",
  "originalSourceObject": {
    "id": "arcane_pulse",
    "name": "Arcane Pulse",
    "description": "Condensed force erupts around the caster, driving nearby foes away from the blast.",
    "prerequisite": "Level 7",
    "effect": "As an action, spend 3 RP to release force in a 10-foot radius. Creatures of your choice make a Strength save against your spell save DC, taking 3d6 force damage and being pushed 10 feet on a failure, or half damage without the push on a success.",
    "type": "Magic",
    "legacyEffect": "AoE force blast knocks back enemies",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "584e2c452cf8056bede651f0f85de602c91e63d8835f1a1fb79d894c351a8a33",
  "submittedProcedure": "At character level 7, use an Action and pay 3 actual shared RP. NEW this is a magical feat technique, not an ordinary spell: no rank, spell components, Counterspell window or Dissonance/Refrain from this activation. At acquisition choose INT, WIS or CHA permanently for this feat’s DC=8+PB+that current modifier; this supplies neither spellcasting qualification norRPcapacity. Center a 10 ft radius on your own occupied space under ordinary area geometry. Choose perceived creatures with line of effect in it, including yourself if desired, before rolling. Roll 3d6 force once. Each makesSTRsave: failure full damage then push up to 10 ft directly away from the origin along a legal unobstructed route; success half damage rounded down, no push. Self can take damage but has no away-from-self push. Stop at obstruction/occupied destination; no collision damage, opportunity attack or unstated prone. Large bodies retain real fitting requirements. Immunity to forced movement blocks only push.",
  "submittedNewChoices": "Explicit nonspell classification and permanent mental-stat choice fill the missing noncaster DC without creating RP.",
  "submittedWorkedCases": [
    "A level 7 Warrior with noRPpool cannot pay 3 RP, even though acquiring this feat was legal.",
    "A shared roll 11 produces 11 on failure or 5 on success; a wall 3 ft behind the victim limits actual push."
  ],
  "decision": "Adopt3RP Action, own10ft radius and3d6force/STR push resolution as NEW; actual RP capacity required, no Warrior pool invented.",
  "completeAuthoringProcedure": "At character level 7, use an Action and pay 3 actual shared RP. NEW this is a magical feat technique, not an ordinary spell: no rank, spell components, Counterspell window or Dissonance/Refrain from this activation. At acquisition choose INT, WIS or CHA permanently for this feat’s DC=8+PB+that current modifier; this supplies neither spellcasting qualification norRPcapacity. Center a 10 ft radius on your own occupied space under ordinary area geometry. Choose perceived creatures with line of effect in it, including yourself if desired, before rolling. Roll 3d6 force once. Each makesSTRsave: failure full damage then push up to 10 ft directly away from the origin along a legal unobstructed route; success half damage rounded down, no push. Self can take damage but has no away-from-self push. Stop at obstruction/occupied destination; no collision damage, opportunity attack or unstated prone. Large bodies retain real fitting requirements. Immunity to forced movement blocks only push.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A level 7 Warrior with noRPpool cannot pay 3 RP, even though acquiring this feat was legal.",
    "A shared roll 11 produces 11 on failure or 5 on success; a wall 3 ft behind the victim limits actual push."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At character level 7, use an Action and pay 3 actual shared RP. NEW this is a magical feat technique, not an ordinary spell: no rank, spell components, Counterspell window or Dissonance/Refrain from this activation. At acquisition choose INT, WIS or CHA permanently for this feat’s DC=8+PB+that current modifier; this supplies neither spellcasting qualification norRPcapacity. Center a 10 ft radius on your own occupied space under ordinary area geometry. Choose perceived creatures with line of effect in it, including yourself if desired, before rolling. Roll 3d6 force once. Each makesSTRsave: failure full damage then push up to 10 ft directly away from the origin along a legal unobstructed route; success half damage rounded down, no push. Self can take damage but has no away-from-self push. Stop at obstruction/occupied destination; no collision damage, opportunity attack or unstated prone. Large bodies retain real fitting requirements. Immunity to forced movement blocks only push.

### Original-position authored review references

```json
[
  {
    "id": "MX-03-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/4"
  },
  {
    "id": "MX-03-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/5"
  }
]
```

## MX-04 — Arcane Recall

### Complete original object

```json
{
  "id": "arcane_recall",
  "name": "Arcane Recall",
  "description": "Practiced recall recovers a spent spell through a deliberate return to its familiar pattern.",
  "prerequisite": "Level 10",
  "effect": "After casting a ranked spell, recover RP equal to that spell’s tier, to a maximum of 5 RP. You regain this use after a long rest.",
  "type": "Magic",
  "legacyEffect": "Regain used spell once per day",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define actual completed ranked cast, tier/rank, min(rank,5) recovery, RP ceiling, zero-cost or interrupted casts, rest use and timing relative to other refunds. Decide paid-cost/funding safeguards with current recovery rules; preserve current effect separately from regain-used-spell legacy."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcane_recall",
  "name": "Arcane Recall",
  "cohort": "magic_extended",
  "questionId": "MX-04",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/3",
  "originalQuestion": "Define actual completed ranked cast, tier/rank, min(rank,5) recovery, RP ceiling, zero-cost or interrupted casts, rest use and timing relative to other refunds. Decide paid-cost/funding safeguards with current recovery rules; preserve current effect separately from regain-used-spell legacy.",
  "originalSourceObject": {
    "id": "arcane_recall",
    "name": "Arcane Recall",
    "description": "Practiced recall recovers a spent spell through a deliberate return to its familiar pattern.",
    "prerequisite": "Level 10",
    "effect": "After casting a ranked spell, recover RP equal to that spell’s tier, to a maximum of 5 RP. You regain this use after a long rest.",
    "type": "Magic",
    "legacyEffect": "Regain used spell once per day",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "94a97965abcda719dfebc38bf3f68acc8538656f2305c8dd3dcd74f7e2d6a0d8",
  "submittedProcedure": "After a completed personal rank 1–9 cast, optionally consume the once LR use to recover min(actual rank,5, RP headroom, unrefunded RP actually paid for that cast). NEW the funding ceiling counts only actual personal RP expenditure, including legal surcharges; it cannot refund charges, HP, other pools, free price or an ally’s contribution. Register the cast’s paid RP and every direct refund/recovery against the same expense once, across this feat and other refund sources; choose a legal order without exceeding that expense. A legal fully saved/missed cast qualifies; countered/interrupted, copied or released-again casts do not. A readied cast qualifies once when successfully prepared, never at release. If the computed recovery is 0, decline before committing the use; no newRPpool/cap. Ordinary ongoing effects need not finish their entire duration.",
  "submittedNewChoices": "Completed-cast timing and shared actual-expense ceiling resolve zero-cost/refund loops.",
  "submittedWorkedCases": [
    "Rank 3 paid 5 RP with enough headroom returns 3; a previous 4 RP refund leaves at most 1 for Recall.",
    "A free charged rank 3 cast cannot produce 3 RP through this proposed funding rule."
  ],
  "decision": "Keep one bounded return after a completed ranked cast with actual unrefunded payment/headroom, not rank-based free RP from a waived cast.",
  "completeAuthoringProcedure": "After a completed personal rank 1–9 cast, optionally consume the once LR use to recover min(actual rank,5, RP headroom, unrefunded RP actually paid for that cast). NEW the funding ceiling counts only actual personal RP expenditure, including legal surcharges; it cannot refund charges, HP, other pools, free price or an ally’s contribution. Register the cast’s paid RP and every direct refund/recovery against the same expense once, across this feat and other refund sources; choose a legal order without exceeding that expense. A legal fully saved/missed cast qualifies; countered/interrupted, copied or released-again casts do not. A readied cast qualifies once when successfully prepared, never at release. If the computed recovery is 0, decline before committing the use; no newRPpool/cap. Ordinary ongoing effects need not finish their entire duration.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Rank 3 paid 5 RP with enough headroom returns 3; a previous 4 RP refund leaves at most 1 for Recall.",
    "A free charged rank 3 cast cannot produce 3 RP through this proposed funding rule."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After a completed personal rank 1–9 cast, optionally consume the once LR use to recover min(actual rank,5, RP headroom, unrefunded RP actually paid for that cast). NEW the funding ceiling counts only actual personal RP expenditure, including legal surcharges; it cannot refund charges, HP, other pools, free price or an ally’s contribution. Register the cast’s paid RP and every direct refund/recovery against the same expense once, across this feat and other refund sources; choose a legal order without exceeding that expense. A legal fully saved/missed cast qualifies; countered/interrupted, copied or released-again casts do not. A readied cast qualifies once when successfully prepared, never at release. If the computed recovery is 0, decline before committing the use; no newRPpool/cap. Ordinary ongoing effects need not finish their entire duration.

### Original-position authored review references

```json
[
  {
    "id": "MX-04-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/6"
  },
  {
    "id": "MX-04-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/7"
  },
  {
    "id": "FA-16",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/additionalBoundaryReviews/1"
  }
]
```

## MX-05 — Arcane Transfusion

### Complete original object

```json
{
  "id": "arcane_transfusion",
  "name": "Arcane Transfusion",
  "description": "The caster trades endurance for magical reserve, drawing power from their own vitality.",
  "prerequisite": "Level 9",
  "effect": "As a bonus action, take necrotic damage equal to twice the RP restored; this damage cannot be reduced. Restore up to your proficiency bonus in RP. You regain this use after a long rest.",
  "type": "Magic",
  "legacyEffect": "Convert HP to mana at 2:1",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Specify declared restoration amount and actual RP headroom before paying2 necrotic damage per RP; define unreducible damage versus true-HP funding, temporary HP, zeroHP/incapacity, Wounds, concentration and interrupts. Bind proficiency cap, Bonus Action and Long Rest ledger; prevent recovery/healing loops without silently importing Blood Ritual costs."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcane_transfusion",
  "name": "Arcane Transfusion",
  "cohort": "magic_extended",
  "questionId": "MX-05",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/4",
  "originalQuestion": "Specify declared restoration amount and actual RP headroom before paying2 necrotic damage per RP; define unreducible damage versus true-HP funding, temporary HP, zeroHP/incapacity, Wounds, concentration and interrupts. Bind proficiency cap, Bonus Action and Long Rest ledger; prevent recovery/healing loops without silently importing Blood Ritual costs.",
  "originalSourceObject": {
    "id": "arcane_transfusion",
    "name": "Arcane Transfusion",
    "description": "The caster trades endurance for magical reserve, drawing power from their own vitality.",
    "prerequisite": "Level 9",
    "effect": "As a bonus action, take necrotic damage equal to twice the RP restored; this damage cannot be reduced. Restore up to your proficiency bonus in RP. You regain this use after a long rest.",
    "type": "Magic",
    "legacyEffect": "Convert HP to mana at 2:1",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "b12fb64390ea9072deae96b57d27aade100572eb52b772bcbe90a3a44e9522cb",
  "submittedProcedure": "Once LR as a Bonus Action, choose integerN from 1 through min(current PB, actualRPheadroom) and preflight the shared normal HP funding rule for 2 Nnecrotic damage. Commit BA/use, then resolve that cost as one packet with normal Wound/death/concentration consequences. If still alive after the complete packet, restore exactlyNactual RP, capped by then-current capacity; later headroom loss does not refund HP. NEW this explicitly bypasses temp HP, resistance, redirection and floors for funding while retaining damage consequences. No use at 0 HP without an exact independent BA permission and sufficient actual funding, which the at-least 1 HP requirement normally forbids. No heal, charge creation, maximum RP increase or incidental resource trigger from self-damage. Ordinary later paid healing remains possible; it does not reset this LR use.",
  "submittedNewChoices": "DeclaredN/headroom, normal HP funding and survival-before-credit are explicit NEW safeguards.",
  "submittedWorkedCases": [
    "PB 3 and 2 missing RP allowN 2: lose 4 normal HP and, if surviving, regain 2 RP.",
    "HP 4 cannot fundN 2 even with 20 temp HP; the illegal attempt spends nothing."
  ],
  "decision": "Adopt explicit normal-HP-funded necrotic damage cost, leaving at least1 before Wound consequences; it is not Temp HP or a refundable resource loop.",
  "completeAuthoringProcedure": "Once LR as a Bonus Action, choose integerN from 1 through min(current PB, actualRPheadroom) and preflight the shared normal HP funding rule for 2 Nnecrotic damage. Commit BA/use, then resolve that cost as one packet with normal Wound/death/concentration consequences. If still alive after the complete packet, restore exactlyNactual RP, capped by then-current capacity; later headroom loss does not refund HP. NEW this explicitly bypasses temp HP, resistance, redirection and floors for funding while retaining damage consequences. No use at 0 HP without an exact independent BA permission and sufficient actual funding, which the at-least 1 HP requirement normally forbids. No heal, charge creation, maximum RP increase or incidental resource trigger from self-damage. Ordinary later paid healing remains possible; it does not reset this LR use.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "PB 3 and 2 missing RP allowN 2: lose 4 normal HP and, if surviving, regain 2 RP.",
    "HP 4 cannot fundN 2 even with 20 temp HP; the illegal attempt spends nothing."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR as a Bonus Action, choose integerN from 1 through min(current PB, actualRPheadroom) and preflight the shared normal HP funding rule for 2 Nnecrotic damage. Commit BA/use, then resolve that cost as one packet with normal Wound/death/concentration consequences. If still alive after the complete packet, restore exactlyNactual RP, capped by then-current capacity; later headroom loss does not refund HP. NEW this explicitly bypasses temp HP, resistance, redirection and floors for funding while retaining damage consequences. No use at 0 HP without an exact independent BA permission and sufficient actual funding, which the at-least 1 HP requirement normally forbids. No heal, charge creation, maximum RP increase or incidental resource trigger from self-damage. Ordinary later paid healing remains possible; it does not reset this LR use.

### Original-position authored review references

```json
[
  {
    "id": "MX-05-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/8"
  },
  {
    "id": "MX-05-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/9"
  }
]
```

## MX-06 — Blood Magic

### Complete original object

```json
{
  "id": "blood_magic",
  "name": "Blood Magic",
  "description": "An experienced caster draws on their own vitality to boost a spell.",
  "prerequisite": "Level 9",
  "effect": "When casting a spell, you may take necrotic damage equal to twice the spell tier to increase its save DC by 1 or add one damage die. This damage cannot be reduced. Once used, you cannot use this feat again until a short rest.",
  "type": "Magic",
  "legacyEffect": "Boost spell using own HP",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve spell tier0, actual paid casting route, declaration and the choice of+1 DC or one damage die. Define die type/packet/targets/critical/maximized cases, all-save versus one-save scope and the2xTier unreducible-necrotic payment at zeroHP. Use Short Rest ledger; no double dipping with reviewed Blood Ritual or copied results."
```

### Preserved original source direction (historical)

```json
{
  "featId": "blood_magic",
  "name": "Blood Magic",
  "cohort": "magic_extended",
  "questionId": "MX-06",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/5",
  "originalQuestion": "Resolve spell tier0, actual paid casting route, declaration and the choice of+1 DC or one damage die. Define die type/packet/targets/critical/maximized cases, all-save versus one-save scope and the2xTier unreducible-necrotic payment at zeroHP. Use Short Rest ledger; no double dipping with reviewed Blood Ritual or copied results.",
  "originalSourceObject": {
    "id": "blood_magic",
    "name": "Blood Magic",
    "description": "An experienced caster draws on their own vitality to boost a spell.",
    "prerequisite": "Level 9",
    "effect": "When casting a spell, you may take necrotic damage equal to twice the spell tier to increase its save DC by 1 or add one damage die. This damage cannot be reduced. Once used, you cannot use this feat again until a short rest.",
    "type": "Magic",
    "legacyEffect": "Boost spell using own HP",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "9e08b460dc68a3ce583322123ac512ae3aef9e316dade1a56d3f37893ff565f6",
  "submittedProcedure": "Once per beneficial SR or LR, when committing an actual spell, declare either+1 to that cast’s spell-save DC or one extra native damage die under the shared added-die procedure. Pay the spell’s actual ordinary costs plus 2×its actual rank as the shared unreducible-necrotic normal HP cost, before establishing its new concentration and opening interruption. Existing concentration must face the self-damage normally before displacement; death/action loss aborts the unfinished spell without refund. Rank 0 explicitly costs 0 HP but still spends the feat use; a cantrip is not excluded by the source. DC mode changes all actual saves caused by that same cast, including its legal repeats, while that cast lasts; it supplies no saves to automatic effects and no inherited DC for unrelated children. Damage mode cannot modify a flat-only or nondamaging spell. No two modes, doubled cast orHPrefund; copying never regrants the modifier.",
  "submittedNewChoices": "Rank 0 allowed at 0 HP cost; one native packet for die mode and one whole cast’s genuine saves for DC mode.",
  "submittedWorkedCases": [
    "Rank 2 spell DC 14 becomes 15 after 4 normal HP cost; an ordinary area save for each target uses 15.",
    "A flat damage effect has no eligible die for die mode; choose a legal DC mode or decline before payment."
  ],
  "decision": "Adopt normal-HP-funded typed damage cost and one DC/die option, preserving real Wound/concentration consequences; not the already reviewed Blood Ritual.",
  "completeAuthoringProcedure": "Once per beneficial SR or LR, when committing an actual spell, declare either+1 to that cast’s spell-save DC or one extra native damage die under the shared added-die procedure. Pay the spell’s actual ordinary costs plus 2×its actual rank as the shared unreducible-necrotic normal HP cost, before establishing its new concentration and opening interruption. Existing concentration must face the self-damage normally before displacement; death/action loss aborts the unfinished spell without refund. Rank 0 explicitly costs 0 HP but still spends the feat use; a cantrip is not excluded by the source. DC mode changes all actual saves caused by that same cast, including its legal repeats, while that cast lasts; it supplies no saves to automatic effects and no inherited DC for unrelated children. Damage mode cannot modify a flat-only or nondamaging spell. No two modes, doubled cast orHPrefund; copying never regrants the modifier.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Rank 2 spell DC 14 becomes 15 after 4 normal HP cost; an ordinary area save for each target uses 15.",
    "A flat damage effect has no eligible die for die mode; choose a legal DC mode or decline before payment."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per beneficial SR or LR, when committing an actual spell, declare either+1 to that cast’s spell-save DC or one extra native damage die under the shared added-die procedure. Pay the spell’s actual ordinary costs plus 2×its actual rank as the shared unreducible-necrotic normal HP cost, before establishing its new concentration and opening interruption. Existing concentration must face the self-damage normally before displacement; death/action loss aborts the unfinished spell without refund. Rank 0 explicitly costs 0 HP but still spends the feat use; a cantrip is not excluded by the source. DC mode changes all actual saves caused by that same cast, including its legal repeats, while that cast lasts; it supplies no saves to automatic effects and no inherited DC for unrelated children. Damage mode cannot modify a flat-only or nondamaging spell. No two modes, doubled cast orHPrefund; copying never regrants the modifier.

### Original-position authored review references

```json
[
  {
    "id": "MX-06-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/10"
  },
  {
    "id": "MX-06-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/11"
  }
]
```

## MX-07 — Channeled Flow

### Complete original object

```json
{
  "id": "channeled_flow",
  "name": "Channeled Flow",
  "description": "Sustained focus carries a channel spell beyond its usual duration.",
  "prerequisite": "Level 10",
  "effect": "When a spell requires you to spend an action on later turns to maintain it, you may maintain it once as a bonus action instead. You regain this use after a short rest.",
  "type": "Magic",
  "legacyEffect": "Extend channel spells by 50%",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve current one maintained Action replaced by one Bonus Action per Short Rest, not the legacy50-percent duration extension. Define qualifying actual later-turn maintenance, costs/concentration, prohibited actions, which turn spends the use and whether other commands share the same action budget."
```

### Preserved original source direction (historical)

```json
{
  "featId": "channeled_flow",
  "name": "Channeled Flow",
  "cohort": "magic_extended",
  "questionId": "MX-07",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/6",
  "originalQuestion": "Preserve current one maintained Action replaced by one Bonus Action per Short Rest, not the legacy50-percent duration extension. Define qualifying actual later-turn maintenance, costs/concentration, prohibited actions, which turn spends the use and whether other commands share the same action budget.",
  "originalSourceObject": {
    "id": "channeled_flow",
    "name": "Channeled Flow",
    "description": "Sustained focus carries a channel spell beyond its usual duration.",
    "prerequisite": "Level 10",
    "effect": "When a spell requires you to spend an action on later turns to maintain it, you may maintain it once as a bonus action instead. You regain this use after a short rest.",
    "type": "Magic",
    "legacyEffect": "Extend channel spells by 50%",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "f8f8ba24695ce316267b8eb3b6b2c44464589698687ab42b371a425b88a6c4d2",
  "submittedProcedure": "Once per beneficial SR or LR, on your own actual later turn, replace one Action explicitly required solely to maintain one of your already established spells with one Bonus Action. Declare and consume at that maintenance commitment. Preserve concentration, RP/material upkeep, targeting, existing pulse/command limits and the original spell deadline. It cannot shorten initial casting, Ready setup, a ritual, an attack granted by the spell, or an optional Action to issue a new damaging command unless that exact source identifies it as required maintenance. An Action that combines required maintenance with another benefit retains the combined printed payload but still supplies no second occurrence. One actual BA must be available; Incapacitated/other restrictions still apply. The source’s prior 50% duration wording remains an inactive alternative.",
  "submittedNewChoices": "Only one actual later maintenance commitment changes action type; no duration or extra activation.",
  "submittedWorkedCases": [
    "Maintaining an existing spell with an explicit Action upkeep uses BA once, retaining its required 2 RP upkeep.",
    "A summoned creature’s optional attack command is not automatically qualifying maintenance."
  ],
  "decision": "Keep conversion of one genuinely required upkeep Action only, with original maintenance costs and concentration; no conversion of initial casting or optional attacks.",
  "completeAuthoringProcedure": "Once per beneficial SR or LR, on your own actual later turn, replace one Action explicitly required solely to maintain one of your already established spells with one Bonus Action. Declare and consume at that maintenance commitment. Preserve concentration, RP/material upkeep, targeting, existing pulse/command limits and the original spell deadline. It cannot shorten initial casting, Ready setup, a ritual, an attack granted by the spell, or an optional Action to issue a new damaging command unless that exact source identifies it as required maintenance. An Action that combines required maintenance with another benefit retains the combined printed payload but still supplies no second occurrence. One actual BA must be available; Incapacitated/other restrictions still apply. The source’s prior 50% duration wording remains an inactive alternative.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Maintaining an existing spell with an explicit Action upkeep uses BA once, retaining its required 2 RP upkeep.",
    "A summoned creature’s optional attack command is not automatically qualifying maintenance."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per beneficial SR or LR, on your own actual later turn, replace one Action explicitly required solely to maintain one of your already established spells with one Bonus Action. Declare and consume at that maintenance commitment. Preserve concentration, RP/material upkeep, targeting, existing pulse/command limits and the original spell deadline. It cannot shorten initial casting, Ready setup, a ritual, an attack granted by the spell, or an optional Action to issue a new damaging command unless that exact source identifies it as required maintenance. An Action that combines required maintenance with another benefit retains the combined printed payload but still supplies no second occurrence. One actual BA must be available; Incapacitated/other restrictions still apply. The source’s prior 50% duration wording remains an inactive alternative.

### Original-position authored review references

```json
[
  {
    "id": "MX-07-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/12"
  },
  {
    "id": "MX-07-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/13"
  }
]
```

## MX-08 — Concentrated Will

### Complete original object

```json
{
  "id": "concentrated_will",
  "name": "Concentrated Will",
  "description": "At level 5, sustained focus receives the listed +2 bonus on concentration checks.",
  "prerequisite": "Level 5",
  "effect": "Gain a +2 bonus to Constitution saving throws made to maintain concentration.",
  "type": "Magic",
  "legacyEffect": "+2 to concentration checks",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind+2 to actual Constitution concentration saves, spell and nonspell concentration scope, multi-packet damage timing, advantage/disadvantage and stacking with Combat Casting/War Caster. Level5 is a prerequisite, not a caster level or new ability modifier."
```

### Preserved original source direction (historical)

```json
{
  "featId": "concentrated_will",
  "name": "Concentrated Will",
  "cohort": "magic_extended",
  "questionId": "MX-08",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/7",
  "originalQuestion": "Bind+2 to actual Constitution concentration saves, spell and nonspell concentration scope, multi-packet damage timing, advantage/disadvantage and stacking with Combat Casting/War Caster. Level5 is a prerequisite, not a caster level or new ability modifier.",
  "originalSourceObject": {
    "id": "concentrated_will",
    "name": "Concentrated Will",
    "description": "At level 5, sustained focus receives the listed +2 bonus on concentration checks.",
    "prerequisite": "Level 5",
    "effect": "Gain a +2 bonus to Constitution saving throws made to maintain concentration.",
    "type": "Magic",
    "legacyEffect": "+2 to concentration checks",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "f6de1ea15975052eb9aebbb136821732316e06cfa90264d00fd4cc4e74e665a0",
  "submittedProcedure": "At character level 5, gain+2 on actualCONsaving throws made to maintain concentration, including nonspell concentration that explicitly uses the same save. Apply current same-stat flat-bonus arbitration; ordinary advantage/disadvantage and proficiency remain independent. Each genuinely separate damage packet generates only its actual required save, not one per damage type or extra feat test. No modifier to unrelated CON, Wound or death saves, automatic concentration loss from incapacity/death, or a special source’s non-CON test. This creates neither concentration capacity nor permission to act at 0 HP. A legally held Ready spell has actual concentration and qualifies.",
  "submittedNewChoices": "Actual CON concentration scope with current strongest-bonus stacking.",
  "submittedWorkedCases": [
    "A real damage concentrationCONsave gets the feat bonus and can also have existing advantage.",
    "Becoming Incapacitated ends ordinary concentration without a save; the feat cannot invent a roll."
  ],
  "decision": "Keep+2 on actual concentration Constitution saves, including qualifying nonspell concentration; distinct applicable feat bonuses add, no generic Wound/save bonus.",
  "completeAuthoringProcedure": "At character level 5, gain+2 on actualCONsaving throws made to maintain concentration, including nonspell concentration that explicitly uses the same save. Apply current same-stat flat-bonus arbitration; ordinary advantage/disadvantage and proficiency remain independent. Each genuinely separate damage packet generates only its actual required save, not one per damage type or extra feat test. No modifier to unrelated CON, Wound or death saves, automatic concentration loss from incapacity/death, or a special source’s non-CON test. This creates neither concentration capacity nor permission to act at 0 HP. A legally held Ready spell has actual concentration and qualifies.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A real damage concentrationCONsave gets the feat bonus and can also have existing advantage.",
    "Becoming Incapacitated ends ordinary concentration without a save; the feat cannot invent a roll."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At character level 5, gain+2 on actualCONsaving throws made to maintain concentration, including nonspell concentration that explicitly uses the same save. Apply current same-stat flat-bonus arbitration; ordinary advantage/disadvantage and proficiency remain independent. Each genuinely separate damage packet generates only its actual required save, not one per damage type or extra feat test. No modifier to unrelated CON, Wound or death saves, automatic concentration loss from incapacity/death, or a special source’s non-CON test. This creates neither concentration capacity nor permission to act at 0 HP. A legally held Ready spell has actual concentration and qualifies.

### Original-position authored review references

```json
[
  {
    "id": "MX-08-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/14"
  },
  {
    "id": "MX-08-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/15"
  },
  {
    "id": "FA-04",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/additionalBoundaryReviews/0"
  }
]
```

## MX-09 — Counterspell Adept

### Complete original object

```json
{
  "id": "counterspell_adept",
  "name": "Counterspell Adept",
  "description": "At level 6, practiced countering receives the listed +4 bonus on interrupt checks.",
  "prerequisite": "Level 6",
  "effect": "Gain a +2 bonus to checks made to counter or interrupt a spell. If your system uses a save DC instead, increase your counterspell DC by 1.",
  "type": "Magic",
  "legacyEffect": "+4 to interrupt checks",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"The description/legacy say+4 while active effect says+2 checks or+1 counterspell DC. Resolve that source conflict explicitly against the actual Counterspell procedure, what interrupt checks include, and whether the alternative DC clause has any current target. Do not apply both branches or grant Counterspell access."
```

### Preserved original source direction (historical)

```json
{
  "featId": "counterspell_adept",
  "name": "Counterspell Adept",
  "cohort": "magic_extended",
  "questionId": "MX-09",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/8",
  "originalQuestion": "The description/legacy say+4 while active effect says+2 checks or+1 counterspell DC. Resolve that source conflict explicitly against the actual Counterspell procedure, what interrupt checks include, and whether the alternative DC clause has any current target. Do not apply both branches or grant Counterspell access.",
  "originalSourceObject": {
    "id": "counterspell_adept",
    "name": "Counterspell Adept",
    "description": "At level 6, practiced countering receives the listed +4 bonus on interrupt checks.",
    "prerequisite": "Level 6",
    "effect": "Gain a +2 bonus to checks made to counter or interrupt a spell. If your system uses a save DC instead, increase your counterspell DC by 1.",
    "type": "Magic",
    "legacyEffect": "+4 to interrupt checks",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "494aec9a4f5ef0ac334f58e400276430baf3fdbd57dcef5c011831abba8d04f8",
  "submittedProcedure": "At character level 6, NEW select the active effect’s+2 over preserved description/legacy+4. Add+2 to an actual ability/task check whose operative source directly counters or interrupts a pending spell, using current strongest same-stat bonus rules. Ordinary Counterspell remains actual casting ability+PB versus 10+2×trigger rank, with task degrees/natural shifts collapsed to success/failure. The alternative+1 DC branch applies only if a separately operational counter source truly uses its own save DC; current ordinary and cited class Counterspells use checks, so noDCbranch applies to them. Never apply both to one attempt. This feat grants no spell, Reaction, extra attempt, automatic low-rank success, spell attack bonus or check to identify magic.",
  "submittedNewChoices": "Active+2 selected; conditionalDCbranch dormant where no actual DC-based source exists.",
  "submittedWorkedCases": [
    "Against rank 3, Counterspell DC 16 and ability+PB 5 become check+7 before rolling.",
    "Mystic Focus’s spell-attack bonus does not apply to that task check; neither feat invents a penetration check."
  ],
  "decision": "Select current+2 interrupt checks and conditional+1 counter-save DC over legacy+4. Ordinary Counterspell is its actual task; no saving throw is invented.",
  "completeAuthoringProcedure": "At character level 6, NEW select the active effect’s+2 over preserved description/legacy+4. Add+2 to an actual ability/task check whose operative source directly counters or interrupts a pending spell, with FS-03 distinct flat feat bonuses additive after each existing non-feat family resolves. Ordinary Counterspell remains actual casting ability+PB versus 10+2×trigger rank, with task degrees/natural shifts collapsed to success/failure. The alternative+1 DC branch applies only if a separately operational counter source truly uses its own save DC; current ordinary and cited class Counterspells use checks, so noDCbranch applies to them. Never apply both to one attempt. This feat grants no spell, Reaction, extra attempt, automatic low-rank success, spell attack bonus or check to identify magic.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Against rank 3, Counterspell DC 16 and ability+PB 5 become check+7 before rolling.",
    "Mystic Focus’s spell-attack bonus does not apply to that task check; neither feat invents a penetration check."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At character level 6, NEW select the active effect’s+2 over preserved description/legacy+4. Add+2 to an actual ability/task check whose operative source directly counters or interrupts a pending spell, with FS-03 distinct flat feat bonuses additive after each existing non-feat family resolves. Ordinary Counterspell remains actual casting ability+PB versus 10+2×trigger rank, with task degrees/natural shifts collapsed to success/failure. The alternative+1 DC branch applies only if a separately operational counter source truly uses its own save DC; current ordinary and cited class Counterspells use checks, so noDCbranch applies to them. Never apply both to one attempt. This feat grants no spell, Reaction, extra attempt, automatic low-rank success, spell attack bonus or check to identify magic.

### Original-position authored review references

```json
[
  {
    "id": "MX-09-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/16"
  },
  {
    "id": "MX-09-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/17"
  }
]
```

## MX-10 — Dispel Precision

### Complete original object

```json
{
  "id": "dispel_precision",
  "name": "Dispel Precision",
  "description": "Precise arcane study improves the chance to remove the intended effect.",
  "prerequisite": "Intelligence 15+",
  "effect": "When dispelling an effect from a target affected by multiple spells, choose the effect you attempt to end rather than determining it randomly. Gain +1 on the dispel check.",
  "type": "Magic",
  "legacyEffect": "+20% chance to remove intended effect",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Use actual Dispel Magic selection/check rules. Determine whether selecting the effect is already standard and whether+1 affects each actual eligible dispel check. Resolve one target with several spells, automatic endings, Dispel Mastery extra target and no invented random selector or generic antimagic permission."
```

### Preserved original source direction (historical)

```json
{
  "featId": "dispel_precision",
  "name": "Dispel Precision",
  "cohort": "magic_extended",
  "questionId": "MX-10",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/9",
  "originalQuestion": "Use actual Dispel Magic selection/check rules. Determine whether selecting the effect is already standard and whether+1 affects each actual eligible dispel check. Resolve one target with several spells, automatic endings, Dispel Mastery extra target and no invented random selector or generic antimagic permission.",
  "originalSourceObject": {
    "id": "dispel_precision",
    "name": "Dispel Precision",
    "description": "Precise arcane study improves the chance to remove the intended effect.",
    "prerequisite": "Intelligence 15+",
    "effect": "When dispelling an effect from a target affected by multiple spells, choose the effect you attempt to end rather than determining it randomly. Gain +1 on the dispel check.",
    "type": "Magic",
    "legacyEffect": "+20% chance to remove intended effect",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "d890a25238951fadbba1b7026a0873c33d0e192738b61073be9c6d437fa099d3",
  "submittedProcedure": "When a legal dispelling source would randomly select among individually eligible effects, choose its one eligible effect instead; identify an effect only to the extent the source permits. Ordinary reviewed Dispel Magic already chooses one perceptible ongoing spell rank 0–3 and ends it automatically: this feat changes neither its target count nor its rank/protection limits. Add+1 only to a real dispel check explicitly required by a different operative source. No check is invented for an automatic success, and no roll can exceed a source’s allowed scope. If the separate proposed Dispel Mastery is adopted, each of its legal targets retains its own existing procedure; Precision does not duplicate attempts. Hidden/protected curses, permanent magic items and class engines remain outside ordinary Dispel Magic.",
  "submittedNewChoices": "Preserves already-standard selection and conditional+1 without inventing randomness or checks.",
  "submittedWorkedCases": [
    "Choose one visible rank 2 spell among three on a creature; ordinary Dispel Magic ends it without a+1 roll.",
    "A rank 5 effect remains ineligible for that ordinary spell despite this feat."
  ],
  "decision": "Keep+1 only where a genuine dispelling check exists; current ordinary Dispel Magic has no check. Preserve exact selected-effect/multieffect scope.",
  "completeAuthoringProcedure": "When a legal dispelling source would randomly select among individually eligible effects, choose its one eligible effect instead; identify an effect only to the extent the source permits. Ordinary reviewed Dispel Magic already chooses one perceptible ongoing spell rank 0–3 and ends it automatically: this feat changes neither its target count nor its rank/protection limits. Add+1 only to a real dispel check explicitly required by a different operative source. No check is invented for an automatic success, and no roll can exceed a source’s allowed scope. If the separate proposed Dispel Mastery is adopted, each of its legal targets retains its own existing procedure; Precision does not duplicate attempts. Hidden/protected curses, permanent magic items and class engines remain outside ordinary Dispel Magic.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Choose one visible rank 2 spell among three on a creature; ordinary Dispel Magic ends it without a+1 roll.",
    "A rank 5 effect remains ineligible for that ordinary spell despite this feat."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

When a legal dispelling source would randomly select among individually eligible effects, choose its one eligible effect instead; identify an effect only to the extent the source permits. Ordinary reviewed Dispel Magic already chooses one perceptible ongoing spell rank 0–3 and ends it automatically: this feat changes neither its target count nor its rank/protection limits. Add+1 only to a real dispel check explicitly required by a different operative source. No check is invented for an automatic success, and no roll can exceed a source’s allowed scope. If the separate proposed Dispel Mastery is adopted, each of its legal targets retains its own existing procedure; Precision does not duplicate attempts. Hidden/protected curses, permanent magic items and class engines remain outside ordinary Dispel Magic.

### Original-position authored review references

```json
[
  {
    "id": "MX-10-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/18"
  },
  {
    "id": "MX-10-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/19"
  }
]
```

## MX-11 — Echo Spell

### Complete original object

```json
{
  "id": "echo_spell",
  "name": "Echo Spell",
  "description": "A prepared casting leaves an echo to repeat its effect next round at half power.",
  "prerequisite": "Intelligence 15+",
  "effect": "After casting a spell of Tier 1–3, you may create an echo. At the start of your next turn, repeat one numerical effect at half value without spending RP or changing targets. You regain this use after a long rest.",
  "type": "Magic",
  "legacyEffect": "Repeat spell effect next round at half power",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define creation timing, use/cost, next regular start, selected numerical effect and half rounding. Bound damage/healing/buff/area packets, targets moving or becoming illegal, saves/attacks, concentration, ownership and no recursive echo/cast/resource/action generation. Preserve Tier1–3 and compare Spell Echo Chamber without merging identities."
```

### Preserved original source direction (historical)

```json
{
  "featId": "echo_spell",
  "name": "Echo Spell",
  "cohort": "magic_extended",
  "questionId": "MX-11",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/10",
  "originalQuestion": "Define creation timing, use/cost, next regular start, selected numerical effect and half rounding. Bound damage/healing/buff/area packets, targets moving or becoming illegal, saves/attacks, concentration, ownership and no recursive echo/cast/resource/action generation. Preserve Tier1–3 and compare Spell Echo Chamber without merging identities.",
  "originalSourceObject": {
    "id": "echo_spell",
    "name": "Echo Spell",
    "description": "A prepared casting leaves an echo to repeat its effect next round at half power.",
    "prerequisite": "Intelligence 15+",
    "effect": "After casting a spell of Tier 1–3, you may create an echo. At the start of your next turn, repeat one numerical effect at half value without spending RP or changing targets. You regain this use after a long rest.",
    "type": "Magic",
    "legacyEffect": "Repeat spell effect next round at half power",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "1a5d3c7e335f7de432456888fddb3bd226136820aa3be5fca20abe5429b0a3cf",
  "submittedProcedure": "Once LR immediately after a personal rank 1–3 spell completes its initial payload, select one numeric damage, HP healing, temp HP or flat stat-bonus component and its original eligible recipients. NEW no echo from Ready preparation until actual release, copies, summons, creation, resource/action grants, movement, hard control or maxima-changing effects. Snapshot that component’s native roll/flat value before external bonuses, original attack/save rules, type, origin and source DC. At your next future regular start, if alive/conscious and any source-required concentration still holds, repeat only that component at half native value floored;0 gives no effect. Recheck original recipients’ actual range/perception/line of effect from the recorded origin, which must still exist; no replacement target. Make fresh original attack/save tests, then ordinary defenses/healing caps, without new critical dice or external damage/heal add-ons. A selected shared area retains only original recipients still in the original area. Temp HP uses the single grant ledger; a flat bonus uses strongest-family arbitration and expires at the earlier of original deadline or your next regular end. Echo heals block healing-copy/resource outputs and create no convertible excess. No new cast, RP, components or duration for the parent; an invalid echo expires without refund.",
  "submittedNewChoices": "Finite numeric categories, explicit stored native magnitude, current defenses and nonrecursive single-start repeat; excludes state/resource production.",
  "submittedWorkedCases": [
    "An original native 11 force area creates a 5 force echo against original still-legal recipients, each with a fresh original save.",
    "A summoned creature’s HP, attacks and future turns are not a repeatable numerical spell component."
  ],
  "decision": "Adopt one bounded delayed half-native secondary result, not a cast, resource refund, extra body or general duplicated spell; recheck genuine original targets and expiry.",
  "completeAuthoringProcedure": "Once LR immediately after a personal rank 1–3 spell completes its initial payload, select one numeric damage, HP healing, temp HP or flat stat-bonus component and its original eligible recipients. NEW no echo from Ready preparation until actual release, copies, summons, creation, resource/action grants, movement, hard control or maxima-changing effects. Snapshot that component’s native roll/flat value before external bonuses, original attack/save rules, type, origin and source DC. At your next future regular start, if alive/conscious and any source-required concentration still holds, repeat only that component at half native value floored;0 gives no effect. Recheck original recipients’ actual range/perception/line of effect from the recorded origin, which must still exist; no replacement target. Make fresh original attack/save tests, then ordinary defenses/healing caps, without new critical dice or external damage/heal add-ons. A selected shared area retains only original recipients still in the original area. Temp HP uses the single grant ledger; a flat bonus uses strongest-family arbitration and expires at the earlier of original deadline or your next regular end. Echo heals block healing-copy/resource outputs and create no convertible excess. No new cast, RP, components or duration for the parent; an invalid echo expires without refund.\nFS-08 secondary-echo flag applies: this delayed result is not another cast. Its flat bonus is a continuation of the original bonus identity/family, not a distinct feat-stacking source; the strongest original-family rule remains. No new resource, copy, hit-trigger chain or source-specific no-resource exception is created.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An original native 11 force area creates a 5 force echo against original still-legal recipients, each with a fresh original save.",
    "A summoned creature’s HP, attacks and future turns are not a repeatable numerical spell component."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR immediately after a personal rank 1–3 spell completes its initial payload, select one numeric damage, HP healing, temp HP or flat stat-bonus component and its original eligible recipients. NEW no echo from Ready preparation until actual release, copies, summons, creation, resource/action grants, movement, hard control or maxima-changing effects. Snapshot that component’s native roll/flat value before external bonuses, original attack/save rules, type, origin and source DC. At your next future regular start, if alive/conscious and any source-required concentration still holds, repeat only that component at half native value floored;0 gives no effect. Recheck original recipients’ actual range/perception/line of effect from the recorded origin, which must still exist; no replacement target. Make fresh original attack/save tests, then ordinary defenses/healing caps, without new critical dice or external damage/heal add-ons. A selected shared area retains only original recipients still in the original area. Temp HP uses the single grant ledger; a flat bonus uses strongest-family arbitration and expires at the earlier of original deadline or your next regular end. Echo heals block healing-copy/resource outputs and create no convertible excess. No new cast, RP, components or duration for the parent; an invalid echo expires without refund.
FS-08 secondary-echo flag applies: this delayed result is not another cast. Its flat bonus is a continuation of the original bonus identity/family, not a distinct feat-stacking source; the strongest original-family rule remains. No new resource, copy, hit-trigger chain or source-specific no-resource exception is created.

### Original-position authored review references

```json
[
  {
    "id": "MX-11-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/20"
  },
  {
    "id": "MX-11-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/21"
  }
]
```

## MX-12 — Efficient Caster

### Complete original object

```json
{
  "id": "efficient_caster",
  "name": "Efficient Caster",
  "description": "Measured spellwork lowers the RP cost of every spell.",
  "prerequisite": "Wisdom 13+",
  "effect": "Once per round when you cast a ranked spell, reduce its RP cost by 1 (minimum 1). After using this feat a number of times equal to your proficiency bonus, regain all uses after a long rest.",
  "type": "Magic",
  "legacyEffect": "-10% mana cost to all spells",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind once-per-round to the existing regular-turn clock, proficiency uses per Long Rest and ranked spell eligibility. Place−1/min1 in the actual RP cost order, accounting for ancestry charges, zero-price casts, armor additions, other reductions and final Resonance Influence. Resolve use expenditure if no reduction can occur."
```

### Preserved original source direction (historical)

```json
{
  "featId": "efficient_caster",
  "name": "Efficient Caster",
  "cohort": "magic_extended",
  "questionId": "MX-12",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/11",
  "originalQuestion": "Bind once-per-round to the existing regular-turn clock, proficiency uses per Long Rest and ranked spell eligibility. Place−1/min1 in the actual RP cost order, accounting for ancestry charges, zero-price casts, armor additions, other reductions and final Resonance Influence. Resolve use expenditure if no reduction can occur.",
  "originalSourceObject": {
    "id": "efficient_caster",
    "name": "Efficient Caster",
    "description": "Measured spellwork lowers the RP cost of every spell.",
    "prerequisite": "Wisdom 13+",
    "effect": "Once per round when you cast a ranked spell, reduce its RP cost by 1 (minimum 1). After using this feat a number of times equal to your proficiency bonus, regain all uses after a long rest.",
    "type": "Magic",
    "legacyEffect": "-10% mana cost to all spells",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "06ccc12fdf3789653dbf97ff9767f61fd734643ad6915ed077cce8e639ddd1c7",
  "submittedProcedure": "Gain PB uses per completed LR, with current PB as maximum and no mid-epoch replenishment from growth. Once per numbered round, at a personal ranked cast’s declaration, optionally reduce its otherwise payable RP by 1, minimum 1. NEW apply after existing eligible base discounts and printed extra costs including component and strain/armor additions, but before final Resonance Influence; this is a discrete reduction, not a new base-rank price. A charged/free normal-price route still pays its independent costs; use is allowed only when this stage’s actualRPprice is at least 2. A genuine reduction commits both use and round entitlement with the cast, even if a later permitted final adjustment or interruption changes the outcome. Cannot reduce charges, HP, specialresources or manufacture a 1 RP charge on a 0 RP cast. Current rank/repertoire/strain cutoff remain.",
  "submittedNewChoices": "Defined price-order placement and only actual positive reductions consume entitlement.",
  "submittedWorkedCases": [
    "A rank 1 cast’s eligible price 2 becomes 1 before a separately applicable final Influence adjustment.",
    "A charged spell with only 1 independent RP surcharge offers no reducible price and spends no feat use."
  ],
  "decision": "Keep finite PB uses, actual price stage and minimum1; no discount on a genuinely free cast or conversion of an independent cost into a free waiver.",
  "completeAuthoringProcedure": "Gain PB uses per completed LR, with current PB as maximum and no mid-epoch replenishment from growth. Once per numbered round, at a personal ranked cast’s declaration, optionally reduce its otherwise payable RP by 1, minimum 1. NEW apply after existing eligible base discounts and printed extra costs including component and strain/armor additions, but before final Resonance Influence; this is a discrete reduction, not a new base-rank price. A charged/free normal-price route still pays its independent costs; use is allowed only when this stage’s actualRPprice is at least 2. A genuine reduction commits both use and round entitlement with the cast, even if a later permitted final adjustment or interruption changes the outcome. Cannot reduce charges, HP, specialresources or manufacture a 1 RP charge on a 0 RP cast. Current rank/repertoire/strain cutoff remain.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A rank 1 cast’s eligible price 2 becomes 1 before a separately applicable final Influence adjustment.",
    "A charged spell with only 1 independent RP surcharge offers no reducible price and spends no feat use."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Gain PB uses per completed LR, with current PB as maximum and no mid-epoch replenishment from growth. Once per numbered round, at a personal ranked cast’s declaration, optionally reduce its otherwise payable RP by 1, minimum 1. NEW apply after existing eligible base discounts and printed extra costs including component and strain/armor additions, but before final Resonance Influence; this is a discrete reduction, not a new base-rank price. A charged/free normal-price route still pays its independent costs; use is allowed only when this stage’s actualRPprice is at least 2. A genuine reduction commits both use and round entitlement with the cast, even if a later permitted final adjustment or interruption changes the outcome. Cannot reduce charges, HP, specialresources or manufacture a 1 RP charge on a 0 RP cast. Current rank/repertoire/strain cutoff remain.

### Original-position authored review references

```json
[
  {
    "id": "MX-12-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/22"
  },
  {
    "id": "MX-12-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/23"
  }
]
```

## MX-13 — Energy Sink

### Complete original object

```json
{
  "id": "energy_sink",
  "name": "Energy Sink",
  "description": "Hard-won magical resilience restores RP after a spell strikes.",
  "prerequisite": "Wisdom 15+",
  "effect": "When you succeed on a saving throw against a spell or take no damage from it, use your reaction to recover 1 RP. You can do so a number of times equal to your proficiency bonus per long rest.",
  "type": "Magic",
  "legacyEffect": "Restore mana when hit by spells",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define success-on-save OR no-damage trigger for one actual spell event, including harmless, friendly, prevented, immune, missed, ongoing and multi-target effects. Bind Reaction, PB uses, RP ceiling, actual caster attribution and zeroHP restrictions; decide anti-farming and refund limits explicitly, not by deleting one printed trigger."
```

### Preserved original source direction (historical)

```json
{
  "featId": "energy_sink",
  "name": "Energy Sink",
  "cohort": "magic_extended",
  "questionId": "MX-13",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/12",
  "originalQuestion": "Define success-on-save OR no-damage trigger for one actual spell event, including harmless, friendly, prevented, immune, missed, ongoing and multi-target effects. Bind Reaction, PB uses, RP ceiling, actual caster attribution and zeroHP restrictions; decide anti-farming and refund limits explicitly, not by deleting one printed trigger.",
  "originalSourceObject": {
    "id": "energy_sink",
    "name": "Energy Sink",
    "description": "Hard-won magical resilience restores RP after a spell strikes.",
    "prerequisite": "Wisdom 15+",
    "effect": "When you succeed on a saving throw against a spell or take no damage from it, use your reaction to recover 1 RP. You can do so a number of times equal to your proficiency bonus per long rest.",
    "type": "Magic",
    "legacyEffect": "Restore mana when hit by spells",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "53d1cc54a7512d05fc22d5998999281898cb718648ff98064cc55a63b6909db2",
  "submittedProcedure": "PB uses per completed LR; no mid-epoch refill fromPBgrowth. After one actual hostile spell event targeting/affecting you resolves, if you either succeeded on its real save OR received no positive resolved damage from that event, you may spend a Reaction/use to recover 1 RP up to your real maximum. NEW require meaningful unwilling opposition: harmless, allied, cooperative, self-authored or farming spells do not qualify. A spell attack that legally targeted you but missed, immunity, or complete prevention can satisfy the no-damage branch; temp HP absorption is damage and alone cannot. A failed save against a hostile nondamaging control spell still satisfies literal no-damage, but only if its result leaves you able to react. One grant per actual cast identity across later ticks/events; no fan-out or repeating-zone farm. Positive saved-against damage may qualify through success. Resolve full damage/control/death first; no ordinary Reaction at 0 HP. Decline before spending if noRPheadroom. This is recovery, not transfer from the attacker or a new pool.",
  "submittedNewChoices": "Hostile-threat and one-cast identity bounds preserve both printed branches while blocking harmless farming.",
  "submittedWorkedCases": [
    "Successful save halves a hostile spell to 5 damage: the success branch permits oneReaction for 1 RP.",
    "A missed hostile spell attack can qualify; receiving a friendly harmless cantrip cannot."
  ],
  "decision": "Keep Reaction to an original hostile spell event with actual source conditions; actual Temp HP damage counts, and all source-specific no-resource flags remain.",
  "completeAuthoringProcedure": "PB uses per completed LR; no mid-epoch refill fromPBgrowth. After one actual hostile spell event targeting/affecting you resolves, if you either succeeded on its real save OR received no positive resolved damage from that event, you may spend a Reaction/use to recover 1 RP up to your real maximum. NEW require meaningful unwilling opposition: harmless, allied, cooperative, self-authored or farming spells do not qualify. A spell attack that legally targeted you but missed, immunity, or complete prevention can satisfy the no-damage branch; temp HP absorption is damage and alone cannot. A failed save against a hostile nondamaging control spell still satisfies literal no-damage, but only if its result leaves you able to react. One grant per actual cast identity across later ticks/events; no fan-out or repeating-zone farm. Positive saved-against damage may qualify through success. Resolve full damage/control/death first; no ordinary Reaction at 0 HP. Decline before spending if noRPheadroom. This is recovery, not transfer from the attacker or a new pool.\nFor this trigger, actual damage includes damage absorbed by Temp HP, so a spell that damages only Temp HP is not a no-damage event. A genuine ward that prevents all damage may leave a qualifying original hostile spell event; the ward does not itself generate a second event. Every explicit no-resource source flag remains controlling; see FS-07.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Successful save halves a hostile spell to 5 damage: the success branch permits oneReaction for 1 RP.",
    "A missed hostile spell attack can qualify; receiving a friendly harmless cantrip cannot."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

PB uses per completed LR; no mid-epoch refill fromPBgrowth. After one actual hostile spell event targeting/affecting you resolves, if you either succeeded on its real save OR received no positive resolved damage from that event, you may spend a Reaction/use to recover 1 RP up to your real maximum. NEW require meaningful unwilling opposition: harmless, allied, cooperative, self-authored or farming spells do not qualify. A spell attack that legally targeted you but missed, immunity, or complete prevention can satisfy the no-damage branch; temp HP absorption is damage and alone cannot. A failed save against a hostile nondamaging control spell still satisfies literal no-damage, but only if its result leaves you able to react. One grant per actual cast identity across later ticks/events; no fan-out or repeating-zone farm. Positive saved-against damage may qualify through success. Resolve full damage/control/death first; no ordinary Reaction at 0 HP. Decline before spending if noRPheadroom. This is recovery, not transfer from the attacker or a new pool.
For this trigger, actual damage includes damage absorbed by Temp HP, so a spell that damages only Temp HP is not a no-damage event. A genuine ward that prevents all damage may leave a qualifying original hostile spell event; the ward does not itself generate a second event. Every explicit no-resource source flag remains controlling; see FS-07.

### Original-position authored review references

```json
[
  {
    "id": "MX-13-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/24"
  },
  {
    "id": "MX-13-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/25"
  }
]
```

## MX-14 — Ether Anchor

### Complete original object

```json
{
  "id": "ether_anchor",
  "name": "Ether Anchor",
  "description": "At level 12, an anchored presence resists banishment effects.",
  "prerequisite": "Level 12",
  "effect": "You have advantage on saving throws against banishment, forced teleportation, and planar displacement. Once per long rest, you may choose to succeed on one such save.",
  "type": "Magic",
  "legacyEffect": "Immune to banishment effects",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve advantage plus one optional auto-success per Long Rest, not legacy immunity. Define an actual allowed save against banishment/forced teleport/displacement, declaration and no-save effects. Keep movement/space rules and do not invent planes, destinations or cosmological eligibility."
```

### Preserved original source direction (historical)

```json
{
  "featId": "ether_anchor",
  "name": "Ether Anchor",
  "cohort": "magic_extended",
  "questionId": "MX-14",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/13",
  "originalQuestion": "Preserve advantage plus one optional auto-success per Long Rest, not legacy immunity. Define an actual allowed save against banishment/forced teleport/displacement, declaration and no-save effects. Keep movement/space rules and do not invent planes, destinations or cosmological eligibility.",
  "originalSourceObject": {
    "id": "ether_anchor",
    "name": "Ether Anchor",
    "description": "At level 12, an anchored presence resists banishment effects.",
    "prerequisite": "Level 12",
    "effect": "You have advantage on saving throws against banishment, forced teleportation, and planar displacement. Once per long rest, you may choose to succeed on one such save.",
    "type": "Magic",
    "legacyEffect": "Immune to banishment effects",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "efaa2bf95c1782139f2e043a825cc952e844f987737e5401a7220ffe9dad3626",
  "submittedProcedure": "At character level 12, gain advantage on actual saving throws against an effect that would banish, forcibly teleport or displace you between planes. Once LR, after such a save fails but before consequences, optionally replace that failure with success; use the source’s actual success outcome, which may retain other effects. No Action or Reaction is required. It does not create a save against a save-less effect, convert willing travel to hostility, anchor nearby creatures, reveal destinations or permit an otherwise illegal movement. A save against damage accompanying independent displacement qualifies only if that same save actually determines the unwanted displacement. Existing explicit unpreventable/no-replacement rules control. No permanent immunity or new cosmological fact is implied.",
  "submittedNewChoices": "After-failure optional success on an existing displacement save only.",
  "submittedWorkedCases": [
    "A failed actual banishment save becomes success and consumes theLRuse.",
    "A source with automatic displacement and no save supplies no roll for this feat to improve."
  ],
  "decision": "Keep existing forced-teleport/banishment saves and one post-failure autosuccess; no save or general relocation immunity is created.",
  "completeAuthoringProcedure": "At character level 12, gain advantage on actual saving throws against an effect that would banish, forcibly teleport or displace you between planes. Once LR, after such a save fails but before consequences, optionally replace that failure with success; use the source’s actual success outcome, which may retain other effects. No Action or Reaction is required. It does not create a save against a save-less effect, convert willing travel to hostility, anchor nearby creatures, reveal destinations or permit an otherwise illegal movement. A save against damage accompanying independent displacement qualifies only if that same save actually determines the unwanted displacement. Existing explicit unpreventable/no-replacement rules control. No permanent immunity or new cosmological fact is implied.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A failed actual banishment save becomes success and consumes theLRuse.",
    "A source with automatic displacement and no save supplies no roll for this feat to improve."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At character level 12, gain advantage on actual saving throws against an effect that would banish, forcibly teleport or displace you between planes. Once LR, after such a save fails but before consequences, optionally replace that failure with success; use the source’s actual success outcome, which may retain other effects. No Action or Reaction is required. It does not create a save against a save-less effect, convert willing travel to hostility, anchor nearby creatures, reveal destinations or permit an otherwise illegal movement. A save against damage accompanying independent displacement qualifies only if that same save actually determines the unwanted displacement. Existing explicit unpreventable/no-replacement rules control. No permanent immunity or new cosmological fact is implied.

### Original-position authored review references

```json
[
  {
    "id": "MX-14-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/26"
  },
  {
    "id": "MX-14-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/27"
  }
]
```

## MX-15 — Flash Cast

### Complete original object

```json
{
  "id": "flash_cast",
  "name": "Flash Cast",
  "description": "Quick spellwork grants the listed one instant-cast spell per day.",
  "prerequisite": "Dexterity 14+",
  "effect": "Once per long rest, cast a spell with a normal casting time of one action as a bonus action. You cannot cast another ranked spell during the same turn.",
  "type": "Magic",
  "legacyEffect": "1 instant-cast spell per day",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define normal one-Action casting, one Bonus Action, Long Rest use, costs/components and the whole-turn ban on another ranked spell before or after use. Resolve reaction casts on that turn, cantrips, extra turns, copied releases and interruption without importing a universal bonus-action spell restriction."
```

### Preserved original source direction (historical)

```json
{
  "featId": "flash_cast",
  "name": "Flash Cast",
  "cohort": "magic_extended",
  "questionId": "MX-15",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/14",
  "originalQuestion": "Define normal one-Action casting, one Bonus Action, Long Rest use, costs/components and the whole-turn ban on another ranked spell before or after use. Resolve reaction casts on that turn, cantrips, extra turns, copied releases and interruption without importing a universal bonus-action spell restriction.",
  "originalSourceObject": {
    "id": "flash_cast",
    "name": "Flash Cast",
    "description": "Quick spellwork grants the listed one instant-cast spell per day.",
    "prerequisite": "Dexterity 14+",
    "effect": "Once per long rest, cast a spell with a normal casting time of one action as a bonus action. You cannot cast another ranked spell during the same turn.",
    "type": "Magic",
    "legacyEffect": "1 instant-cast spell per day",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "aaa57bd1d07cb9f2f6b6dfa260e9f8f6aef37f2c965c241d9929a36d922284f8",
  "submittedProcedure": "Once LR, declare an actually known/prepared spell with printed normal casting time oneAction as a Bonus Action instead; maintain every other access, component, RP, concentration and strain rule. NEW the whole actual turn, including any on-turn Reaction casts, may contain no other ranked cast before or after this cast. Preflight the turn’s existing cast history; committing this feat establishes the restriction even if countered. The chosen spell may be rank 0; other cantrips remain legal with their actual action resources. A later genuine extra turn is a distinct turn for this prohibition but does not refresh theLRuse or other regular-turn budgets. Ready release/copy with no new cast is not another ranked cast, while preparing a readied ranked spell is. No long-cast compression, Reaction conversion, free BA or universal restriction on unrelated turns.",
  "submittedNewChoices": "Whole actual-turn ranked-cast history and optional rank 0 target preserve printed timing.",
  "submittedWorkedCases": [
    "After casting a ranked spell as anAction this turn, Flash Cast is ineligible even for a cantrip.",
    "Flash-casting a rank 2 spell allows a later legalAction cantrip but forbids an on-turn ranked Counterspell."
  ],
  "decision": "Adopt one Action-to-BA conversion and the whole-actual-turn ranked-spell restriction, including earlier casts and later Reactions; no second Action grant.",
  "completeAuthoringProcedure": "Once LR, declare an actually known/prepared spell with printed normal casting time oneAction as a Bonus Action instead; maintain every other access, component, RP, concentration and strain rule. NEW the whole actual turn, including any on-turn Reaction casts, may contain no other ranked cast before or after this cast. Preflight the turn’s existing cast history; committing this feat establishes the restriction even if countered. The chosen spell may be rank 0; other cantrips remain legal with their actual action resources. A later genuine extra turn is a distinct turn for this prohibition but does not refresh theLRuse or other regular-turn budgets. Ready release/copy with no new cast is not another ranked cast, while preparing a readied ranked spell is. No long-cast compression, Reaction conversion, free BA or universal restriction on unrelated turns.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "After casting a ranked spell as anAction this turn, Flash Cast is ineligible even for a cantrip.",
    "Flash-casting a rank 2 spell allows a later legalAction cantrip but forbids an on-turn ranked Counterspell."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR, declare an actually known/prepared spell with printed normal casting time oneAction as a Bonus Action instead; maintain every other access, component, RP, concentration and strain rule. NEW the whole actual turn, including any on-turn Reaction casts, may contain no other ranked cast before or after this cast. Preflight the turn’s existing cast history; committing this feat establishes the restriction even if countered. The chosen spell may be rank 0; other cantrips remain legal with their actual action resources. A later genuine extra turn is a distinct turn for this prohibition but does not refresh theLRuse or other regular-turn budgets. Ready release/copy with no new cast is not another ranked cast, while preparing a readied ranked spell is. No long-cast compression, Reaction conversion, free BA or universal restriction on unrelated turns.

### Original-position authored review references

```json
[
  {
    "id": "MX-15-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/28"
  },
  {
    "id": "MX-15-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/29"
  }
]
```

## MX-16 — Foresight Surge

### Complete original object

```json
{
  "id": "foresight_surge",
  "name": "Foresight Surge",
  "description": "After casting divination, foresight grants the listed initiative increase.",
  "prerequisite": "Wisdom 13+",
  "effect": "After you cast a divination spell, gain +2 initiative for the next hour. If initiative is already rolled, move up one place in the order at the start of the next round.",
  "type": "Magic",
  "legacyEffect": "+10 initiative after casting divination",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve both+2 future initiative for one hour and one-place movement when already rolled. Define actual Divination cast, repeated applications, round-boundary update, top slot/ties, pending turn cursor and extra-turn conservation. A move in order must not create or delete a regular turn, refresh or pulse."
```

### Preserved original source direction (historical)

```json
{
  "featId": "foresight_surge",
  "name": "Foresight Surge",
  "cohort": "magic_extended",
  "questionId": "MX-16",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/15",
  "originalQuestion": "Preserve both+2 future initiative for one hour and one-place movement when already rolled. Define actual Divination cast, repeated applications, round-boundary update, top slot/ties, pending turn cursor and extra-turn conservation. A move in order must not create or delete a regular turn, refresh or pulse.",
  "originalSourceObject": {
    "id": "foresight_surge",
    "name": "Foresight Surge",
    "description": "After casting divination, foresight grants the listed initiative increase.",
    "prerequisite": "Wisdom 13+",
    "effect": "After you cast a divination spell, gain +2 initiative for the next hour. If initiative is already rolled, move up one place in the order at the start of the next round.",
    "type": "Magic",
    "legacyEffect": "+10 initiative after casting divination",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "5b5efb4e326c93e9f768b648de10bb48062f8851b2f73499c04755a4901c01fa",
  "submittedProcedure": "After a completed actual Divination cast, gain a nonstacking+2 to future initiative rolls for one elapsed hour, refreshing that deadline on later eligible casts. The selected casting class must use Divination for this identity. If already participating in rolled initiative, also queue one move up one baseline place at the next numbered-round boundary. NEW one queued move per owner per boundary; repeated casts cannot accumulate jumps. At that boundary finish previous-round events, restore temporary permutations, then process pending advances in stable activation order by swapping the owner with the immediately preceding still-participating baseline actor; top actor stays. Apply later reviewed temporary permutations, such as Future Echo, to the resulting baseline. Every participant still receives one regular slot. A departed/disabled pending record expires without makeup. Existing virtual deadlines, recharge, periodic clocks and spent budgets do not move or refresh; no reroll or extra turn.",
  "submittedNewChoices": "One nonstacking hour bonus and bounded baseline swap with conserved regular turns.",
  "submittedWorkedCases": [
    "OrderA, B, C withCqueued becomesA, C, B next round;Cdoes not act again in the current round.",
    "Three Divination casts before that boundary still queue only one advance forC."
  ],
  "decision": "Adopt+2 initiative and one bounded next-round baseline ordering advance; integrate actual Future Echo permutation restoration without removing incapacitated actors or granting turns.",
  "completeAuthoringProcedure": "After a completed actual Divination cast, gain a nonstacking+2 to future initiative rolls for one elapsed hour, refreshing that deadline on later eligible casts. The selected casting class must use Divination for this identity. If already participating in rolled initiative, also queue one move up one baseline place at the next numbered-round boundary. NEW one queued move per owner per boundary; repeated casts cannot accumulate jumps. At that boundary finish previous-round events, restore temporary permutations, then process pending advances in stable activation order by swapping the owner with the immediately preceding still-participating baseline actor; top actor stays. Apply later reviewed temporary permutations, such as Future Echo, to the resulting baseline. Every participant still receives one regular slot. A departed actor without a retained initiative slot loses its pending advance without makeup. Incapacitation alone does not remove an actor’s regular slot or this pending ordering change. Existing virtual deadlines, recharge, periodic clocks and spent budgets do not move or refresh; no reroll or extra turn.\nFor actual Future Echo, restore an expiring permutation first, apply this feat’s pending baseline advances once in the stated stable order, then apply a newly established Future Echo permutation to the resulting baseline. Preserve actual slots and spent turns; no extra turn or resource refresh occurs.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "OrderA, B, C withCqueued becomesA, C, B next round;Cdoes not act again in the current round.",
    "Three Divination casts before that boundary still queue only one advance forC."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After a completed actual Divination cast, gain a nonstacking+2 to future initiative rolls for one elapsed hour, refreshing that deadline on later eligible casts. The selected casting class must use Divination for this identity. If already participating in rolled initiative, also queue one move up one baseline place at the next numbered-round boundary. NEW one queued move per owner per boundary; repeated casts cannot accumulate jumps. At that boundary finish previous-round events, restore temporary permutations, then process pending advances in stable activation order by swapping the owner with the immediately preceding still-participating baseline actor; top actor stays. Apply later reviewed temporary permutations, such as Future Echo, to the resulting baseline. Every participant still receives one regular slot. A departed actor without a retained initiative slot loses its pending advance without makeup. Incapacitation alone does not remove an actor’s regular slot or this pending ordering change. Existing virtual deadlines, recharge, periodic clocks and spent budgets do not move or refresh; no reroll or extra turn.
For actual Future Echo, restore an expiring permutation first, apply this feat’s pending baseline advances once in the stated stable order, then apply a newly established Future Echo permutation to the resulting baseline. Preserve actual slots and spent turns; no extra turn or resource refresh occurs.

### Original-position authored review references

```json
[
  {
    "id": "MX-16-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/30"
  },
  {
    "id": "MX-16-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/31"
  }
]
```

## MX-17 — Illusionist’s Trick

### Complete original object

```json
{
  "id": "illusionist_s_trick",
  "name": "Illusionist’s Trick",
  "description": "Charisma 14+ gives an illusion the listed extra hit before it vanishes.",
  "prerequisite": "Charisma 14+",
  "effect": "The first time an illusory creature or object you create would be ended by an attack or interaction, it persists until the end of the current turn, allowing observers to make the normal investigation save afterward.",
  "type": "Magic",
  "legacyEffect": "Illusions take 1 extra hit before vanishing",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Identify actual illusory creature/object sources and their normal ending/investigation procedure; investigation save is not automatically a core save type. Define first hit/interaction, simultaneous invalidation, persistence through current turn, observers knowing the truth, concentration and nonphysical blocking. No real HP, extra creature or automatic belief."
```

### Preserved original source direction (historical)

```json
{
  "featId": "illusionist_s_trick",
  "name": "Illusionist’s Trick",
  "cohort": "magic_extended",
  "questionId": "MX-17",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/16",
  "originalQuestion": "Identify actual illusory creature/object sources and their normal ending/investigation procedure; investigation save is not automatically a core save type. Define first hit/interaction, simultaneous invalidation, persistence through current turn, observers knowing the truth, concentration and nonphysical blocking. No real HP, extra creature or automatic belief.",
  "originalSourceObject": {
    "id": "illusionist_s_trick",
    "name": "Illusionist’s Trick",
    "description": "Charisma 14+ gives an illusion the listed extra hit before it vanishes.",
    "prerequisite": "Charisma 14+",
    "effect": "The first time an illusory creature or object you create would be ended by an attack or interaction, it persists until the end of the current turn, allowing observers to make the normal investigation save afterward.",
    "type": "Magic",
    "legacyEffect": "Illusions take 1 extra hit before vanishing",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "c66976c2a278db385bab4940a17191568dee3adc37cf74287f0faa113222d02b",
  "submittedProcedure": "For each actual illusory creature/object you personally create, the first attack or interaction that would end that particular illusion’s existence instead delays only that ending until the current actual turn ends. NEW outside initiative use the end of the current canonical six-second window. It remains nonphysical and observers retain information already obtained; known illusions do not regain concealment, cover, belief or control. Losing required concentration, natural expiry, dispel, source death or another independent ending still ends it immediately. The feat does not postpone an observer’s ordinary Investigation check or direct physical proof unless that source’s actual rule specifically ends the illusion itself. At the deferred endpoint end the illusion as originally required; where the source only grants a disbelief test rather than termination, use its actual Investigation check/save at its printed timing, with no free new save type. Current Minor Illusion/Silent Image physical interaction reveals to observers but does not end the global image, so normally does not trigger this delay.",
  "submittedNewChoices": "Per-illusion first actual destruction, preserving immediate evidence and source-specific Investigation.",
  "submittedWorkedCases": [
    "A source illusion explicitly destroyed by a hit can remain visibly present until this turn ends, with no substance.",
    "Walking through Silent Image reveals it immediately; this feat cannot make the witness believe the wall is solid."
  ],
  "decision": "Keep narrow delay of a genuine interaction-caused illusion ending only; disbelief, visible contradictions, concentration loss and independent expiry remain.",
  "completeAuthoringProcedure": "For each actual illusory creature/object you personally create, the first attack or interaction that would end that particular illusion’s existence instead delays only that ending until the current actual turn ends. NEW outside initiative use the end of the current canonical six-second window. It remains nonphysical and observers retain information already obtained; known illusions do not regain concealment, cover, belief or control. Losing required concentration, natural expiry, dispel, source death or another independent ending still ends it immediately. The feat does not postpone an observer’s ordinary Investigation check or direct physical proof unless that source’s actual rule specifically ends the illusion itself. At the deferred endpoint end the illusion as originally required; where the source only grants a disbelief test rather than termination, use its actual Investigation check/save at its printed timing, with no free new save type. Current Minor Illusion/Silent Image physical interaction reveals to observers but does not end the global image, so normally does not trigger this delay.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A source illusion explicitly destroyed by a hit can remain visibly present until this turn ends, with no substance.",
    "Walking through Silent Image reveals it immediately; this feat cannot make the witness believe the wall is solid."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

For each actual illusory creature/object you personally create, the first attack or interaction that would end that particular illusion’s existence instead delays only that ending until the current actual turn ends. NEW outside initiative use the end of the current canonical six-second window. It remains nonphysical and observers retain information already obtained; known illusions do not regain concealment, cover, belief or control. Losing required concentration, natural expiry, dispel, source death or another independent ending still ends it immediately. The feat does not postpone an observer’s ordinary Investigation check or direct physical proof unless that source’s actual rule specifically ends the illusion itself. At the deferred endpoint end the illusion as originally required; where the source only grants a disbelief test rather than termination, use its actual Investigation check/save at its printed timing, with no free new save type. Current Minor Illusion/Silent Image physical interaction reveals to observers but does not end the global image, so normally does not trigger this delay.

### Original-position authored review references

```json
[
  {
    "id": "MX-17-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/32"
  },
  {
    "id": "MX-17-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/33"
  }
]
```

## MX-18 — Lingering Magic

### Complete original object

```json
{
  "id": "lingering_magic",
  "name": "Lingering Magic",
  "description": "Wisdom 13+ sustains spell effects for the listed 20% longer duration.",
  "prerequisite": "Wisdom 13+",
  "effect": "When you cast a spell with a duration of at least 1 round and no concentration, extend its duration by 1 round. Once per spell.",
  "type": "Magic",
  "legacyEffect": "Spell effects last 20% longer",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Use active+1 round once per nonconcentration spell, not description/legacy20percent. Define round-to-seconds/end-marker conversion for minute/hour spells, delayed riders, initial/recurring pulses, until-discharged effects and explicit caps. No extra charge, summon use or extension after an independent ending condition."
```

### Preserved original source direction (historical)

```json
{
  "featId": "lingering_magic",
  "name": "Lingering Magic",
  "cohort": "magic_extended",
  "questionId": "MX-18",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/17",
  "originalQuestion": "Use active+1 round once per nonconcentration spell, not description/legacy20percent. Define round-to-seconds/end-marker conversion for minute/hour spells, delayed riders, initial/recurring pulses, until-discharged effects and explicit caps. No extra charge, summon use or extension after an independent ending condition.",
  "originalSourceObject": {
    "id": "lingering_magic",
    "name": "Lingering Magic",
    "description": "Wisdom 13+ sustains spell effects for the listed 20% longer duration.",
    "prerequisite": "Wisdom 13+",
    "effect": "When you cast a spell with a duration of at least 1 round and no concentration, extend its duration by 1 round. Once per spell.",
    "type": "Magic",
    "legacyEffect": "Spell effects last 20% longer",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "518ce2ce11f7dbb2c54aa90fddbac846bde2d2ddd1de9d09934ed4581db8ed82",
  "submittedProcedure": "NEW select the active+1 round wording over preserved 20%. At a completed nonconcentration spell’s creation, extend its finite stated duration of at least one round by exactly one six-second/regular-marker interval, once per original cast. Round effects add one original regular marker; minute/hour deadlines add 6 elapsed seconds. A Ready spell’s temporary held concentration does not disqualify a normally nonconcentration payload; extend its payload at release, never its Ready deadline. Independently capped charges, target counts, specified number of pulses, item stock and discharge/consumption endpoints remain. An ongoing effect whose ordinary pulse exists solely while its duration persists may get the one naturally reached extra pulse; an explicit three-pulse effect remains three. No extension of instantaneous/permanent effects, resurrection windows classified separately from spell duration, concentration spells, linked separate conditions, or an independent end such as destroyed support. No stacking with itself or repeated recasting of the same instance.",
  "submittedNewChoices": "Exact 6 second extension, source caps preserved and Ready hold distinguished from payload concentration.",
  "submittedWorkedCases": [
    "A nonconcentration 60 second effect lasts 66 seconds unless independently discharged earlier.",
    "A printed three-pulse effect still has three pulses even if its remaining cosmetic duration extends."
  ],
  "decision": "Select current one-round extension over legacy20%, retaining non-concentration and actual independent endpoints; it creates no additional fixed-count pulses.",
  "completeAuthoringProcedure": "NEW select the active+1 round wording over preserved 20%. At a completed nonconcentration spell’s creation, extend its finite stated duration of at least one round by exactly one six-second/regular-marker interval, once per original cast. Round effects add one original regular marker; minute/hour deadlines add 6 elapsed seconds. A Ready spell’s temporary held concentration does not disqualify a normally nonconcentration payload; extend its payload at release, never its Ready deadline. Independently capped charges, target counts, specified number of pulses, item stock and discharge/consumption endpoints remain. An ongoing effect whose ordinary pulse exists solely while its duration persists may get the one naturally reached extra pulse; an explicit three-pulse effect remains three. No extension of instantaneous/permanent effects, resurrection windows classified separately from spell duration, concentration spells, linked separate conditions, or an independent end such as destroyed support. No stacking with itself or repeated recasting of the same instance.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A nonconcentration 60 second effect lasts 66 seconds unless independently discharged earlier.",
    "A printed three-pulse effect still has three pulses even if its remaining cosmetic duration extends."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW select the active+1 round wording over preserved 20%. At a completed nonconcentration spell’s creation, extend its finite stated duration of at least one round by exactly one six-second/regular-marker interval, once per original cast. Round effects add one original regular marker; minute/hour deadlines add 6 elapsed seconds. A Ready spell’s temporary held concentration does not disqualify a normally nonconcentration payload; extend its payload at release, never its Ready deadline. Independently capped charges, target counts, specified number of pulses, item stock and discharge/consumption endpoints remain. An ongoing effect whose ordinary pulse exists solely while its duration persists may get the one naturally reached extra pulse; an explicit three-pulse effect remains three. No extension of instantaneous/permanent effects, resurrection windows classified separately from spell duration, concentration spells, linked separate conditions, or an independent end such as destroyed support. No stacking with itself or repeated recasting of the same instance.

### Original-position authored review references

```json
[
  {
    "id": "MX-18-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/34"
  },
  {
    "id": "MX-18-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/35"
  }
]
```

## MX-19 — Magical Fortitude

### Complete original object

```json
{
  "id": "magical_fortitude",
  "name": "Magical Fortitude",
  "description": "A Constitution-trained caster or defender gains the listed +2 protection on saves against spells.",
  "prerequisite": "Constitution 13+",
  "effect": "Gain +2 to saving throws against spells.",
  "type": "Magic",
  "legacyEffect": "+2 saves vs spells",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define+2 on actual saving throws caused by spells, including repeat/concentration/death saves where applicable, and spell versus magical class/item effects. Constitution13 does not grant proficiency or spellcasting. Resolve stacking with other feats and jewelry without changing source save DCs."
```

### Preserved original source direction (historical)

```json
{
  "featId": "magical_fortitude",
  "name": "Magical Fortitude",
  "cohort": "magic_extended",
  "questionId": "MX-19",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/18",
  "originalQuestion": "Define+2 on actual saving throws caused by spells, including repeat/concentration/death saves where applicable, and spell versus magical class/item effects. Constitution13 does not grant proficiency or spellcasting. Resolve stacking with other feats and jewelry without changing source save DCs.",
  "originalSourceObject": {
    "id": "magical_fortitude",
    "name": "Magical Fortitude",
    "description": "A Constitution-trained caster or defender gains the listed +2 protection on saves against spells.",
    "prerequisite": "Constitution 13+",
    "effect": "Gain +2 to saving throws against spells.",
    "type": "Magic",
    "legacyEffect": "+2 saves vs spells",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "c6faf69945c73e274e8a3f173a7a3ee3ed694e3b94688c620ac5814b8f9e642a",
  "submittedProcedure": "Gain+2 to your actual saving throws directly required by an operative spell’s payload, including later repeat saves and a spell explicitly requiring a save to maintain another effect. Current strongest same-stat bonus arbitration applies, so another+2 save feat is not automatic+4. Ordinary damage-induced concentrationCONsaves, Core Wound saves and death saves are consequences of shared life/concentration rules rather than the damaging spell’s printed payload and receive no bonus from this feat; Concentrated Will has its own exact concentration scope. A spell that directly calls for a death-effect saving throw can qualify, but ordinary death saves do not. Magical nonspell class/item/feat effects are not spells unless their actual source classifies the activation as one. CON 13 is acquisition only; no new proficiency, casting ability or defense against a Counterspell task check.",
  "submittedNewChoices": "Direct spell-save causation excludes ordinary damage concentration/Wound/death saves.",
  "submittedWorkedCases": [
    "A repeatWISsave explicitly supplied by an ongoing spell gains+2.",
    "TheCONsave to maintain concentration after taking a spell’s damage uses Concentrated Will if owned, not this feat."
  ],
  "decision": "Keep+2 actual saves against direct spell effects, including source repeats; adopt distinct-flat-feat addition without extending it to indirect Wound or concentration saves.",
  "completeAuthoringProcedure": "Gain+2 to your actual saving throws directly required by an operative spell’s payload, including later repeat saves and a spell explicitly requiring a save to maintain another effect. NEW FS-03 applies: a distinct eligible+2 save feat adds to this+2, giving+4; duplicate copies of this feat do not. Existing non-feat families retain their own arbitration. Ordinary damage-induced concentrationCONsaves, Core Wound saves and death saves are consequences of shared life/concentration rules rather than the damaging spell’s printed payload and receive no bonus from this feat; Concentrated Will has its own exact concentration scope. A spell that directly calls for a death-effect saving throw can qualify, but ordinary death saves do not. Magical nonspell class/item/feat effects are not spells unless their actual source classifies the activation as one. CON 13 is acquisition only; no new proficiency, casting ability or defense against a Counterspell task check.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A repeatWISsave explicitly supplied by an ongoing spell gains+2.",
    "TheCONsave to maintain concentration after taking a spell’s damage uses Concentrated Will if owned, not this feat."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Gain+2 to your actual saving throws directly required by an operative spell’s payload, including later repeat saves and a spell explicitly requiring a save to maintain another effect. NEW FS-03 applies: a distinct eligible+2 save feat adds to this+2, giving+4; duplicate copies of this feat do not. Existing non-feat families retain their own arbitration. Ordinary damage-induced concentrationCONsaves, Core Wound saves and death saves are consequences of shared life/concentration rules rather than the damaging spell’s printed payload and receive no bonus from this feat; Concentrated Will has its own exact concentration scope. A spell that directly calls for a death-effect saving throw can qualify, but ordinary death saves do not. Magical nonspell class/item/feat effects are not spells unless their actual source classifies the activation as one. CON 13 is acquisition only; no new proficiency, casting ability or defense against a Counterspell task check.

### Original-position authored review references

```json
[
  {
    "id": "MX-19-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/36"
  },
  {
    "id": "MX-19-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/37"
  }
]
```

## MX-20 — Mana Burn

### Complete original object

```json
{
  "id": "mana_burn",
  "name": "Mana Burn",
  "description": "Intelligence-trained offensive spellwork carries the feat's listed drain against an enemy's RP.",
  "prerequisite": "Intelligence 13+",
  "effect": "When a creature fails a save against your damaging spell, it loses 1 RP if it has an RP pool. A creature can lose RP this way only once per round.",
  "type": "Magic",
  "legacyEffect": "Offensive spells drain enemy mana",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind actual failed save against your damaging spell, including successful damage prevention, repeated saves, RP-less creatures and minimum0. Define one recipient-wide once-per-round ledger across multiple users, phase timing, no RP transfer to caster and no charge/slot pool substitution."
```

### Preserved original source direction (historical)

```json
{
  "featId": "mana_burn",
  "name": "Mana Burn",
  "cohort": "magic_extended",
  "questionId": "MX-20",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/19",
  "originalQuestion": "Bind actual failed save against your damaging spell, including successful damage prevention, repeated saves, RP-less creatures and minimum0. Define one recipient-wide once-per-round ledger across multiple users, phase timing, no RP transfer to caster and no charge/slot pool substitution.",
  "originalSourceObject": {
    "id": "mana_burn",
    "name": "Mana Burn",
    "description": "Intelligence-trained offensive spellwork carries the feat's listed drain against an enemy's RP.",
    "prerequisite": "Intelligence 13+",
    "effect": "When a creature fails a save against your damaging spell, it loses 1 RP if it has an RP pool. A creature can lose RP this way only once per round.",
    "type": "Magic",
    "legacyEffect": "Offensive spells drain enemy mana",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "c2b9a56891f19dcb6da67ac7bbe9292d14bc77975b7622c8f736fbf7bcdfc1cd",
  "submittedProcedure": "After a creature fails an actual save against your personally cast damaging spell, remove 1 from its realRPpool, minimum 0. NEW damaging means that same spell application has a native damage component governed by that save; full prevention/immunity may leave 0 damage without negating the failed-save trigger. A repeat save solely ending nondamaging control after earlier damage does not qualify. Commit one recipient-wide Mana Burn entitlement per numbered round across all owners/casts on the first qualifying failure with anRPpool, even at RP 0; no further loss that round. Resolve native damage and immediate survival replacements first, then loss if the target still exists as a living resource holder. No transfer to you, charge/RC/slot substitution, maximum reduction or loss from RP-less creatures. Copies, echoes and reflected packets cannot create a fresh proc.",
  "submittedNewChoices": "One target-wide round record, failed damaging-save predicate and no resource substitution.",
  "submittedWorkedCases": [
    "Two casters trigger Mana Burn against the same RP 4 foe this round: total loss is 1, leaving 3.",
    "A target immune to the damage can still lose 1 RP after failing the associated save; an RP-less monster loses nothing."
  ],
  "decision": "Keep at most1 actual RP lost per target/numbered round on the relevant failed damaging-spell save; no RC/slot conversion, RP creation or transfer.",
  "completeAuthoringProcedure": "After a creature fails an actual save against your personally cast damaging spell, remove 1 from its realRPpool, minimum 0. NEW damaging means that same spell application has a native damage component governed by that save; full prevention/immunity may leave 0 damage without negating the failed-save trigger. A repeat save solely ending nondamaging control after earlier damage does not qualify. Commit one recipient-wide Mana Burn entitlement per numbered round across all owners/casts on the first qualifying failure with anRPpool, even at RP 0; no further loss that round. Resolve native damage and immediate survival replacements first, then loss if the target still exists as a living resource holder. No transfer to you, charge/RC/slot substitution, maximum reduction or loss from RP-less creatures. Copies, echoes and reflected packets cannot create a fresh proc.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Two casters trigger Mana Burn against the same RP 4 foe this round: total loss is 1, leaving 3.",
    "A target immune to the damage can still lose 1 RP after failing the associated save; an RP-less monster loses nothing."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After a creature fails an actual save against your personally cast damaging spell, remove 1 from its realRPpool, minimum 0. NEW damaging means that same spell application has a native damage component governed by that save; full prevention/immunity may leave 0 damage without negating the failed-save trigger. A repeat save solely ending nondamaging control after earlier damage does not qualify. Commit one recipient-wide Mana Burn entitlement per numbered round across all owners/casts on the first qualifying failure with anRPpool, even at RP 0; no further loss that round. Resolve native damage and immediate survival replacements first, then loss if the target still exists as a living resource holder. No transfer to you, charge/RC/slot substitution, maximum reduction or loss from RP-less creatures. Copies, echoes and reflected packets cannot create a fresh proc.

### Original-position authored review references

```json
[
  {
    "id": "MX-20-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/38"
  },
  {
    "id": "MX-20-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json",
      "bytes": 895941,
      "sha256": "17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b"
    },
    "pointer": "/originalCaseReviews/39"
  }
]
```

## MX-21 — Mental Buffer

### Complete original object

```json
{
  "id": "mental_buffer",
  "name": "Mental Buffer",
  "description": "Wisdom 15+ supports the feat's listed once-per-day defense against confusion.",
  "prerequisite": "Wisdom 15+",
  "effect": "Once per long rest, when you would become confused, dominated, or unable to distinguish allies from enemies, ignore that condition until the end of your next turn.",
  "type": "Magic",
  "legacyEffect": "Negate confusion once per day",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define the exact source control components called confused/dominated/mistaken-allies and automatic versus voluntary use. Specify prevention versus suppression until end of next regular turn, underlying duration/save clocks, recurrence, multiple components and reactivation. Do not turn one-turn relief into a cure or unrestricted control immunity."
```

### Preserved original source direction (historical)

```json
{
  "featId": "mental_buffer",
  "name": "Mental Buffer",
  "cohort": "magic_extended",
  "questionId": "MX-21",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/20",
  "originalQuestion": "Define the exact source control components called confused/dominated/mistaken-allies and automatic versus voluntary use. Specify prevention versus suppression until end of next regular turn, underlying duration/save clocks, recurrence, multiple components and reactivation. Do not turn one-turn relief into a cure or unrestricted control immunity.",
  "originalSourceObject": {
    "id": "mental_buffer",
    "name": "Mental Buffer",
    "description": "Wisdom 15+ supports the feat's listed once-per-day defense against confusion.",
    "prerequisite": "Wisdom 15+",
    "effect": "Once per long rest, when you would become confused, dominated, or unable to distinguish allies from enemies, ignore that condition until the end of your next turn.",
    "type": "Magic",
    "legacyEffect": "Negate confusion once per day",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "1d5c0aa8a3d8189dde1c6965646ca48a2bd78704da429e23a2171969658b78ad",
  "submittedProcedure": "Once LR, when a new source application would impose confusion/randomized action selection, a dominated/commanded Action or turn, or an explicit inability to distinguish friend from foe, voluntarily suppress only that application’s eligible control components through the end of your next future regular turn. No Action/Reaction is required; choose before those components first take effect. NEW qualify by actual written behavior, not a condition’s suggestive name. Ordinary Charmed/Frightened alone, illusion disbelief, blindness, truthful uncertainty and incapacity without such a component do not qualify. Preserve unrelated damage/slow and the original source, duration, concentration, repeat saves and spent hard-control entitlement. Suppressed clocks continue; legal ending saves still occur. If the original component has already expired or been cured by the boundary it never returns; otherwise it resumes for its remaining duration without replaying a past commanded turn. One application only, not immunity to later separate sources.",
  "submittedNewChoices": "Voluntary temporary component suppression, with unchanged original clocks and no replayed command.",
  "submittedWorkedCases": [
    "A dominated Action scheduled inside the protected interval is skipped, not stored for a later extra command.",
    "Another source’s independent Stunned effect remains operative."
  ],
  "decision": "Adopt one bounded delayed application interval for supported confusion/misidentification control; no arbitrary condition cure or replay of suppressed pulses.",
  "completeAuthoringProcedure": "Once LR, when a new source application would impose confusion/randomized action selection, a dominated/commanded Action or turn, or an explicit inability to distinguish friend from foe, voluntarily suppress only that application’s eligible control components through the end of your next future regular turn. No Action/Reaction is required; choose before those components first take effect. NEW qualify by actual written behavior, not a condition’s suggestive name. Ordinary Charmed/Frightened alone, illusion disbelief, blindness, truthful uncertainty and incapacity without such a component do not qualify. Preserve unrelated damage/slow and the original source, duration, concentration, repeat saves and spent hard-control entitlement. Suppressed clocks continue; legal ending saves still occur. If the original component has already expired or been cured by the boundary it never returns; otherwise it resumes for its remaining duration without replaying a past commanded turn. One application only, not immunity to later separate sources.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A dominated Action scheduled inside the protected interval is skipped, not stored for a later extra command.",
    "Another source’s independent Stunned effect remains operative."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR, when a new source application would impose confusion/randomized action selection, a dominated/commanded Action or turn, or an explicit inability to distinguish friend from foe, voluntarily suppress only that application’s eligible control components through the end of your next future regular turn. No Action/Reaction is required; choose before those components first take effect. NEW qualify by actual written behavior, not a condition’s suggestive name. Ordinary Charmed/Frightened alone, illusion disbelief, blindness, truthful uncertainty and incapacity without such a component do not qualify. Preserve unrelated damage/slow and the original source, duration, concentration, repeat saves and spent hard-control entitlement. Suppressed clocks continue; legal ending saves still occur. If the original component has already expired or been cured by the boundary it never returns; otherwise it resumes for its remaining duration without replaying a past commanded turn. One application only, not immunity to later separate sources.

### Original-position authored review references

```json
[
  {
    "id": "MX-21-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/0"
  },
  {
    "id": "MX-21-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/1"
  }
]
```

## MX-22 — Mirror Cast

### Complete original object

```json
{
  "id": "mirror_cast",
  "name": "Mirror Cast",
  "description": "Intelligence 16+ permits the feat's listed once-per-day spell cast from a reflection.",
  "prerequisite": "Intelligence 16+",
  "effect": "Once per long rest, cast a spell as though originating from a reflective surface you can see within 60 feet. Range and line of effect are measured from that surface.",
  "type": "Magic",
  "legacyEffect": "Cast spell from reflection (once per day)",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define a real visible reflective surface within60ft, selecting the origin at cast time, its space/size, range/line/sight requirements, Self/Touch/cones, hostile-held surfaces, moving/destroyed mirrors and ongoing effects. Preserve caster ownership, actions, components, RP and Long Rest use; no duplicate caster or remote senses."
```

### Preserved original source direction (historical)

```json
{
  "featId": "mirror_cast",
  "name": "Mirror Cast",
  "cohort": "magic_extended",
  "questionId": "MX-22",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/21",
  "originalQuestion": "Define a real visible reflective surface within60ft, selecting the origin at cast time, its space/size, range/line/sight requirements, Self/Touch/cones, hostile-held surfaces, moving/destroyed mirrors and ongoing effects. Preserve caster ownership, actions, components, RP and Long Rest use; no duplicate caster or remote senses.",
  "originalSourceObject": {
    "id": "mirror_cast",
    "name": "Mirror Cast",
    "description": "Intelligence 16+ permits the feat's listed once-per-day spell cast from a reflection.",
    "prerequisite": "Intelligence 16+",
    "effect": "Once per long rest, cast a spell as though originating from a reflective surface you can see within 60 feet. Range and line of effect are measured from that surface.",
    "type": "Magic",
    "legacyEffect": "Cast spell from reflection (once per day)",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "90667484007440d2751956b7bed9dd9a2bf4fb8e1548cab02f96acd642728673",
  "submittedProcedure": "Once LR at cast declaration choose a real reflective surface you can see within 60 ft of your actual body. NEW require an unobstructed line of effect from you to that surface, at least hand-sized, sufficiently exposed to form a recognizable reflection; a drawn picture of a mirror is insufficient. Choose an unoccupied origin point immediately at its visible face. Measure spell range/line of effect and area orientation from that point; you still must personally perceive targets where the spell requires it, receiving no remote senses. Self-area/cone origins can relocate, but a Self-only body buff still affects you and Touch spells still require actual touch; no remote grasp. Hostile-held surfaces may serve if visibly legal; no possession or movement of the object. Commit ordinary costs/components/feat use at your body, preserving its interruption window. The origin is snapshotted for immediate resolution; destruction before resolution fails the changed origin with no refund. Ongoing created areas retain their actual fixed/moving rules and deadlines; the mirror is neither a second caster nor an unprinted tether.",
  "submittedNewChoices": "Visible substantial surface, body-to-surface line and explicit Self/Touch limits.",
  "submittedWorkedCases": [
    "A cone can originate at a visible mirror 40 ft away and point along a chosen legal direction.",
    "An unseen creature behind the mirror gains no free visibility; a Touch heal cannot cross 40 ft through it."
  ],
  "decision": "Adopt finite real mirror-origin redirection with actual visibility, line of effect and caster targeting; no remote Touch, mirror-created sight or continuing tether.",
  "completeAuthoringProcedure": "Once LR at cast declaration choose a real reflective surface you can see within 60 ft of your actual body. NEW require an unobstructed line of effect from you to that surface, at least hand-sized, sufficiently exposed to form a recognizable reflection; a drawn picture of a mirror is insufficient. Choose an unoccupied origin point immediately at its visible face. Measure spell range/line of effect and area orientation from that point; you still must personally perceive targets where the spell requires it, receiving no remote senses. Self-area/cone origins can relocate, but a Self-only body buff still affects you and Touch spells still require actual touch; no remote grasp. Hostile-held surfaces may serve if visibly legal; no possession or movement of the object. Commit ordinary costs/components/feat use at your body, preserving its interruption window. The origin is snapshotted for immediate resolution; destruction before resolution fails the changed origin with no refund. Ongoing created areas retain their actual fixed/moving rules and deadlines; the mirror is neither a second caster nor an unprinted tether.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A cone can originate at a visible mirror 40 ft away and point along a chosen legal direction.",
    "An unseen creature behind the mirror gains no free visibility; a Touch heal cannot cross 40 ft through it."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR at cast declaration choose a real reflective surface you can see within 60 ft of your actual body. NEW require an unobstructed line of effect from you to that surface, at least hand-sized, sufficiently exposed to form a recognizable reflection; a drawn picture of a mirror is insufficient. Choose an unoccupied origin point immediately at its visible face. Measure spell range/line of effect and area orientation from that point; you still must personally perceive targets where the spell requires it, receiving no remote senses. Self-area/cone origins can relocate, but a Self-only body buff still affects you and Touch spells still require actual touch; no remote grasp. Hostile-held surfaces may serve if visibly legal; no possession or movement of the object. Commit ordinary costs/components/feat use at your body, preserving its interruption window. The origin is snapshotted for immediate resolution; destruction before resolution fails the changed origin with no refund. Ongoing created areas retain their actual fixed/moving rules and deadlines; the mirror is neither a second caster nor an unprinted tether.

### Original-position authored review references

```json
[
  {
    "id": "MX-22-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/2"
  },
  {
    "id": "MX-22-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/3"
  }
]
```

## MX-23 — Mystic Focus

### Complete original object

```json
{
  "id": "mystic_focus",
  "name": "Mystic Focus",
  "description": "At level 6, focused spellwork receives the feat's listed +2 spell penetration.",
  "prerequisite": "Level 6",
  "effect": "Gain +1 to spell attack rolls and to checks made to overcome magical resistance.",
  "type": "Magic",
  "legacyEffect": "+2 spell penetration",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve active+1 spell attacks and checks versus description/legacy+2 spell penetration. Define actual magical-resistance checks from sourced mechanics and stacking with Spell Penetration. No invented resistance statistic, Spell Focus identity or universal spell-save-DC bonus."
```

### Preserved original source direction (historical)

```json
{
  "featId": "mystic_focus",
  "name": "Mystic Focus",
  "cohort": "magic_extended",
  "questionId": "MX-23",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/22",
  "originalQuestion": "Resolve active+1 spell attacks and checks versus description/legacy+2 spell penetration. Define actual magical-resistance checks from sourced mechanics and stacking with Spell Penetration. No invented resistance statistic, Spell Focus identity or universal spell-save-DC bonus.",
  "originalSourceObject": {
    "id": "mystic_focus",
    "name": "Mystic Focus",
    "description": "At level 6, focused spellwork receives the feat's listed +2 spell penetration.",
    "prerequisite": "Level 6",
    "effect": "Gain +1 to spell attack rolls and to checks made to overcome magical resistance.",
    "type": "Magic",
    "legacyEffect": "+2 spell penetration",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "cce89df2cb1912ebaf6c52eac34e4691aac45209c6a306f8d8563b5adc276b38",
  "submittedProcedure": "At character level 6, NEW choose active+1 rather than legacy/description+2 penetration. Gain+1 on actual spell attack rolls and actual checks explicitly required to overcome magical resistance. Current strongest same-stat bonuses apply. No generic resistance check exists: ordinary damage resistance still halves its eligible damage and spell resistance that grants save advantage is not a caster check. Apply the second branch only to an operative source’s real test. This is not Spell Focus, supplies no saveDCbonus, spell access, damage increase or extra Counterspell/Dispel check. A Counterspell check is interruption, not overcoming magical resistance unless its exact source separately establishes that predicate.",
  "submittedNewChoices": "Active+1 and actual-test predicate preserve both clauses without inventing penetration stats.",
  "submittedWorkedCases": [
    "A legal spell attack+6 becomes+7 if no stronger applicable flat bonus replaces it.",
    "A creature with fire resistance retains that resistance; there is no new+1 penetration roll."
  ],
  "decision": "Select current+1 spell attacks/real resistance checks over legacy+2 penetration; distinct feat bonuses add, but absent checks are not created.",
  "completeAuthoringProcedure": "At character level 6, NEW choose active+1 rather than legacy/description+2 penetration. Gain+1 on actual spell attack rolls and actual checks explicitly required to overcome magical resistance. NEW distinct applicable flat feat bonuses add under FS-03; resolve existing class/spell/item families first without changing their rules. No generic resistance check exists: ordinary damage resistance still halves its eligible damage and spell resistance that grants save advantage is not a caster check. Apply the second branch only to an operative source’s real test. This is not Spell Focus, supplies no saveDCbonus, spell access, damage increase or extra Counterspell/Dispel check. A Counterspell check is interruption, not overcoming magical resistance unless its exact source separately establishes that predicate.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A legal spell attack+6 becomes+7 if no stronger applicable flat bonus replaces it.",
    "A creature with fire resistance retains that resistance; there is no new+1 penetration roll."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At character level 6, NEW choose active+1 rather than legacy/description+2 penetration. Gain+1 on actual spell attack rolls and actual checks explicitly required to overcome magical resistance. NEW distinct applicable flat feat bonuses add under FS-03; resolve existing class/spell/item families first without changing their rules. No generic resistance check exists: ordinary damage resistance still halves its eligible damage and spell resistance that grants save advantage is not a caster check. Apply the second branch only to an operative source’s real test. This is not Spell Focus, supplies no saveDCbonus, spell access, damage increase or extra Counterspell/Dispel check. A Counterspell check is interruption, not overcoming magical resistance unless its exact source separately establishes that predicate.

### Original-position authored review references

```json
[
  {
    "id": "MX-23-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/4"
  },
  {
    "id": "MX-23-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/5"
  }
]
```

## MX-24 — Mystic Recoil

### Complete original object

```json
{
  "id": "mystic_recoil",
  "name": "Mystic Recoil",
  "description": "When a spell fails at level 7, mystic recoil leaves you ready to take the feat's listed extra action next turn.",
  "prerequisite": "Level 7",
  "effect": "Once per short rest, when a spell you cast is countered or all its targets succeed on their saves, gain one additional bonus action on your next turn. This bonus action cannot cast a ranked spell.",
  "type": "Magic",
  "legacyEffect": "If spell fails, gain +1 action next turn",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define countered versus all targets succeed, including no-save/mixed-target/automatic-success spells and invalid targets. Specify use declaration, next regular turn extra Bonus Action, expiration and restrictions on ranked spells/commands. Preserve once per Short Rest and prevent repeated failure/echo events from generating extra actions."
```

### Preserved original source direction (historical)

```json
{
  "featId": "mystic_recoil",
  "name": "Mystic Recoil",
  "cohort": "magic_extended",
  "questionId": "MX-24",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/23",
  "originalQuestion": "Define countered versus all targets succeed, including no-save/mixed-target/automatic-success spells and invalid targets. Specify use declaration, next regular turn extra Bonus Action, expiration and restrictions on ranked spells/commands. Preserve once per Short Rest and prevent repeated failure/echo events from generating extra actions.",
  "originalSourceObject": {
    "id": "mystic_recoil",
    "name": "Mystic Recoil",
    "description": "When a spell fails at level 7, mystic recoil leaves you ready to take the feat's listed extra action next turn.",
    "prerequisite": "Level 7",
    "effect": "Once per short rest, when a spell you cast is countered or all its targets succeed on their saves, gain one additional bonus action on your next turn. This bonus action cannot cast a ranked spell.",
    "type": "Magic",
    "legacyEffect": "If spell fails, gain +1 action next turn",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "c82a390d865174b819a1bbe19e6d9661cb127142923e721ab9e2445591f688c0",
  "submittedProcedure": "Once SR/LR after your own actual spell is countered, or after every originally legal recipient of its initial save-based payload actually succeeds on every required initial save, optionally commit the use and queue one extra BA for your next future regular turn. NEW require at least one actual initial save and all original recipients resolved legally; a no-save, mixed attack/save or lost-target cast cannot qualify by vacuous success. An automatic successful save counts where a real save was called for. No copying/echoing or each-tick retrigger. The BA becomes available on that one regular turn, even if other BA is spent, and expires unused at its end; incapacity creates no makeup. It may perform an actually acquired legal BA, including ordinary command, but cannot prepare/cast a ranked spell or create more actions/banked allowances. It does not bypass shared companion offense, concentration, RP or other use caps. No extra fullAction, Reaction or duration-clock tick.",
  "submittedNewChoices": "One queued regular-turn BA and explicit all-initial-target success predicate.",
  "submittedWorkedCases": [
    "Both targets succeed on the spell’s only two initial saves: next regular turn gains one restricted BA.",
    "One target failed but was immune to damage: the all-success branch does not trigger."
  ],
  "decision": "Adopt extra bounded non-ranked-spell BA only after actual countering or all initial recipients genuinely saving; no empty-set trigger or extra full Action.",
  "completeAuthoringProcedure": "Once SR/LR after your own actual spell is countered, or after every originally legal recipient of its initial save-based payload actually succeeds on every required initial save, optionally commit the use and queue one extra BA for your next future regular turn. NEW require at least one actual initial save and all original recipients resolved legally; a no-save, mixed attack/save or lost-target cast cannot qualify by vacuous success. An automatic successful save counts where a real save was called for. No copying/echoing or each-tick retrigger. The BA becomes available on that one regular turn, even if other BA is spent, and expires unused at its end; incapacity creates no makeup. It may perform an actually acquired legal BA, including ordinary command, but cannot prepare/cast a ranked spell or create more actions/banked allowances. It does not bypass shared companion offense, concentration, RP or other use caps. No extra fullAction, Reaction or duration-clock tick.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Both targets succeed on the spell’s only two initial saves: next regular turn gains one restricted BA.",
    "One target failed but was immune to damage: the all-success branch does not trigger."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once SR/LR after your own actual spell is countered, or after every originally legal recipient of its initial save-based payload actually succeeds on every required initial save, optionally commit the use and queue one extra BA for your next future regular turn. NEW require at least one actual initial save and all original recipients resolved legally; a no-save, mixed attack/save or lost-target cast cannot qualify by vacuous success. An automatic successful save counts where a real save was called for. No copying/echoing or each-tick retrigger. The BA becomes available on that one regular turn, even if other BA is spent, and expires unused at its end; incapacity creates no makeup. It may perform an actually acquired legal BA, including ordinary command, but cannot prepare/cast a ranked spell or create more actions/banked allowances. It does not bypass shared companion offense, concentration, RP or other use caps. No extra fullAction, Reaction or duration-clock tick.

### Original-position authored review references

```json
[
  {
    "id": "MX-24-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/6"
  },
  {
    "id": "MX-24-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/7"
  }
]
```

## MX-25 — Overchannel

### Complete original object

```json
{
  "id": "overchannel",
  "name": "Overchannel",
  "description": "At level 10, an overchanneled spell takes the listed backlash to boost its damage by 25%.",
  "prerequisite": "Level 10",
  "effect": "Once per long rest, add one additional damage die per spell tier to a damaging spell. After it resolves, take force damage equal to twice the spell tier; this damage cannot be reduced.",
  "type": "Magic",
  "legacyEffect": "Boost spell damage by 25%, take backlash",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Use active one extra damage die per spell tier and2xTier force backlash after resolution, not legacy25percent. Specify dice type/packets/targets/critical interactions, rank0, miss/no damage/counterspell, concentration and zeroHP. Preserve unreducible backlash and Long Rest use without manufacturing healing or refund loops."
```

### Preserved original source direction (historical)

```json
{
  "featId": "overchannel",
  "name": "Overchannel",
  "cohort": "magic_extended",
  "questionId": "MX-25",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/24",
  "originalQuestion": "Use active one extra damage die per spell tier and2xTier force backlash after resolution, not legacy25percent. Specify dice type/packets/targets/critical interactions, rank0, miss/no damage/counterspell, concentration and zeroHP. Preserve unreducible backlash and Long Rest use without manufacturing healing or refund loops.",
  "originalSourceObject": {
    "id": "overchannel",
    "name": "Overchannel",
    "description": "At level 10, an overchanneled spell takes the listed backlash to boost its damage by 25%.",
    "prerequisite": "Level 10",
    "effect": "Once per long rest, add one additional damage die per spell tier to a damaging spell. After it resolves, take force damage equal to twice the spell tier; this damage cannot be reduced.",
    "type": "Magic",
    "legacyEffect": "Boost spell damage by 25%, take backlash",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "3010ff829aa510c4fa202d0616d500f80b067bad53f5ed51cf742dd9024d504b",
  "submittedProcedure": "Once LR at damaging spell declaration, add one existing native damage die per actual spell rank to one immediate native packet under the shared added-die rule. NEW choose this active rule over legacy 25%. Commit use with the cast. After its immediate attempted resolution, including a miss, all saves or Counterspell, take 2×rank force backlash as one self-damage event. This damage cannot be reduced or redirected; NEW it does pass through real temp HP before normal HP, unlike the explicitly proposed normal HP-funded blood costs. Resolve ordinary Wound/death/concentration consequences and no incidental reflection/resource/lifesteal triggers from this self-authored cost. It requires noHPprepayment and can kill the caster. A readied cast takes backlash after preparation/interruption, not after eventual release; its added dice attach once to the eventual immediate payload. Rank 0 legally adds 0 dice and 0 damage but still spends the use if chosen. Flat-only/no-native-die spells are ineligible.",
  "submittedNewChoices": "One native packet, post-attempt backlash including counters, and explicit temp HP-compatible damage rather than HP funding.",
  "submittedWorkedCases": [
    "Rank 3 native 4d6 becomes 7d6 in the selected shared area roll, followed by 6 unreducible force backlash.",
    "If Counterspell negates that spell, the committedLRuse and 6 backlash still occur."
  ],
  "decision": "Select current one native damage die per rank and2×rank unreducible post-attempt force backlash over legacy25%; actual Temp HP can absorb this distinct backlash.",
  "completeAuthoringProcedure": "Once LR at damaging spell declaration, add one existing native damage die per actual spell rank to one immediate native packet under the shared added-die rule. NEW choose this active rule over legacy 25%. Commit use with the cast. After its immediate attempted resolution, including a miss, all saves or Counterspell, take 2×rank force backlash as one self-damage event. This damage cannot be reduced or redirected; NEW it does pass through real temp HP before normal HP, unlike the explicitly proposed normal HP-funded blood costs. Resolve ordinary Wound/death/concentration consequences and no incidental reflection/resource/lifesteal triggers from this self-authored cost. It requires noHPprepayment and can kill the caster. A readied cast takes backlash after preparation/interruption, not after eventual release; its added dice attach once to the eventual immediate payload. Rank 0 legally adds 0 dice and 0 damage but still spends the use if chosen. Flat-only/no-native-die spells are ineligible.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Rank 3 native 4d6 becomes 7d6 in the selected shared area roll, followed by 6 unreducible force backlash.",
    "If Counterspell negates that spell, the committedLRuse and 6 backlash still occur."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR at damaging spell declaration, add one existing native damage die per actual spell rank to one immediate native packet under the shared added-die rule. NEW choose this active rule over legacy 25%. Commit use with the cast. After its immediate attempted resolution, including a miss, all saves or Counterspell, take 2×rank force backlash as one self-damage event. This damage cannot be reduced or redirected; NEW it does pass through real temp HP before normal HP, unlike the explicitly proposed normal HP-funded blood costs. Resolve ordinary Wound/death/concentration consequences and no incidental reflection/resource/lifesteal triggers from this self-authored cost. It requires noHPprepayment and can kill the caster. A readied cast takes backlash after preparation/interruption, not after eventual release; its added dice attach once to the eventual immediate payload. Rank 0 legally adds 0 dice and 0 damage but still spends the use if chosen. Flat-only/no-native-die spells are ineligible.

### Original-position authored review references

```json
[
  {
    "id": "MX-25-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/8"
  },
  {
    "id": "MX-25-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/9"
  }
]
```

## MX-26 — Planar Knowledge

### Complete original object

```json
{
  "id": "planar_knowledge",
  "name": "Planar Knowledge",
  "description": "Intelligence 14+ supports recognizing an enemy's resistances in the middle of a fight.",
  "prerequisite": "Intelligence 14+",
  "effect": "As a bonus action, make an Arcana check against DC 10 + the creature’s challenge rating. On a success, learn one resistance, immunity, vulnerability, or planar trait. Once per creature.",
  "type": "Magic",
  "legacyEffect": "Know enemy resistances mid-fight",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define Bonus Action range/senses, actual creature CR including fractional/missing values, DC10+CR rounding, choosing one existing fact, retries and once-per-creature identity. Read actual resistance/immunity/vulnerability records; planar-trait content remains deferred where cosmology would be required. No invented trait or origin."
```

### Preserved original source direction (historical)

```json
{
  "featId": "planar_knowledge",
  "name": "Planar Knowledge",
  "cohort": "magic_extended",
  "questionId": "MX-26",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/25",
  "originalQuestion": "Define Bonus Action range/senses, actual creature CR including fractional/missing values, DC10+CR rounding, choosing one existing fact, retries and once-per-creature identity. Read actual resistance/immunity/vulnerability records; planar-trait content remains deferred where cosmology would be required. No invented trait or origin.",
  "originalSourceObject": {
    "id": "planar_knowledge",
    "name": "Planar Knowledge",
    "description": "Intelligence 14+ supports recognizing an enemy's resistances in the middle of a fight.",
    "prerequisite": "Intelligence 14+",
    "effect": "As a bonus action, make an Arcana check against DC 10 + the creature’s challenge rating. On a success, learn one resistance, immunity, vulnerability, or planar trait. Once per creature.",
    "type": "Magic",
    "legacyEffect": "Know enemy resistances mid-fight",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "22b4512c035663f9bbb1d4a1f44433ec2538acb95774510c39900c5c735e10f7",
  "submittedProcedure": "Once per actual creature identity, as a Bonus Action examine one creature you can perceive within 60 ft and line of effect. NEW commit the per-creature attempt before rolling INT(Arcana) against DC 10+its actual printedCR, rounding the finalDCdown by current fraction rules. If noCR is assigned, Director must establish the encounter’s rating before attempts; absence is notCR 0 and an unsupported target is ineligible without spending. Success lets the Director truthfully disclose one existing damage resistance, immunity, vulnerability or explicitly established planar-trait fact; you may name a category, but no nonexistent fact is invented. If that category has none, report that absence only, not all other hidden data. Failure gives no fact and no retry through alias/form/encounter reset. Existing source disguises/protected information still apply. Planar traits requiring the deferred cosmology review remain unasserted; other recorded defenses are still usable.",
  "submittedNewChoices": "60 ft examination, once-attempt identity and actualCR/one-fact disclosure without new ontology.",
  "submittedWorkedCases": [
    "CR 1/2 gives DC 10 after rounding; success can reveal one actual cold resistance.",
    "An unrated story entity is not automatically DC 10, and success cannot invent its planar origin."
  ],
  "decision": "Keep bounded observable ordinary defensive information and explicit no-cosmology scope; NEW DC15 fallback for otherwise eligible genuinely unrated creatures, never invented CR.",
  "completeAuthoringProcedure": "Once per actual creature identity, as a Bonus Action examine one creature you can perceive within 60 ft and line of effect. NEW commit the per-creature attempt before rolling INT(Arcana) against DC 10+its actual printedCR, rounding the finalDCdown by current fraction rules. NEW for an otherwise genuinely eligible creature with no assigned CR, use DC15; preserve the missing/null CR rather than inventing a rating. A missing creature identity, ordinary information payload or permission is still not supplied by this fallback. Success lets the Director truthfully disclose one existing damage resistance, immunity, vulnerability or explicitly established planar-trait fact; you may name a category, but no nonexistent fact is invented. If that category has none, report that absence only, not all other hidden data. Failure gives no fact and no retry through alias/form/encounter reset. Existing source disguises/protected information still apply. Planar traits requiring the deferred cosmology review remain unasserted; other recorded defenses are still usable.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "CR 1/2 gives DC 10 after rounding; success can reveal one actual cold resistance.",
    "An unrated story entity is not automatically DC 10, and success cannot invent its planar origin."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per actual creature identity, as a Bonus Action examine one creature you can perceive within 60 ft and line of effect. NEW commit the per-creature attempt before rolling INT(Arcana) against DC 10+its actual printedCR, rounding the finalDCdown by current fraction rules. NEW for an otherwise genuinely eligible creature with no assigned CR, use DC15; preserve the missing/null CR rather than inventing a rating. A missing creature identity, ordinary information payload or permission is still not supplied by this fallback. Success lets the Director truthfully disclose one existing damage resistance, immunity, vulnerability or explicitly established planar-trait fact; you may name a category, but no nonexistent fact is invented. If that category has none, report that absence only, not all other hidden data. Failure gives no fact and no retry through alias/form/encounter reset. Existing source disguises/protected information still apply. Planar traits requiring the deferred cosmology review remain unasserted; other recorded defenses are still usable.

### Original-position authored review references

```json
[
  {
    "id": "MX-26-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/10"
  },
  {
    "id": "MX-26-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/11"
  }
]
```

## MX-27 — Protective Casting

### Complete original object

```json
{
  "id": "protective_casting",
  "name": "Protective Casting",
  "description": "At level 6, casting grants the listed +10% AC for 5 seconds.",
  "prerequisite": "Level 6",
  "effect": "After casting a ranked spell, gain +1 AC until the start of your next turn.",
  "type": "Magic",
  "legacyEffect": "+10% AC for 5s after casting",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Use+1 AC until next regular start after a real ranked cast, not legacy10percent/5seconds. Define successful versus interrupted/countered casting, repeated nonstacking applications and combination with Arcane Armor/other AC families. No retroactive protection for the triggering cast unless explicitly decided."
```

### Preserved original source direction (historical)

```json
{
  "featId": "protective_casting",
  "name": "Protective Casting",
  "cohort": "magic_extended",
  "questionId": "MX-27",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/26",
  "originalQuestion": "Use+1 AC until next regular start after a real ranked cast, not legacy10percent/5seconds. Define successful versus interrupted/countered casting, repeated nonstacking applications and combination with Arcane Armor/other AC families. No retroactive protection for the triggering cast unless explicitly decided.",
  "originalSourceObject": {
    "id": "protective_casting",
    "name": "Protective Casting",
    "description": "At level 6, casting grants the listed +10% AC for 5 seconds.",
    "prerequisite": "Level 6",
    "effect": "After casting a ranked spell, gain +1 AC until the start of your next turn.",
    "type": "Magic",
    "legacyEffect": "+10% AC for 5s after casting",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "28cf2b62cb44ecfdd3be5a30d1388b44d548f7d18a03324794990fa0ddda2914",
  "submittedProcedure": "At character level 6, after a completed personal ranked cast gain+1 AC until your next future regular start. NEW select active+1/regular-start over preserved 10%/5 seconds. It begins after the cast’s immediate resolution or successful Ready preparation, so does not protect against that cast’s earlier interruption attacks. Miss/all-save still qualify; a countered cast does not. Repeated legal casts refresh one same-family record without stacking magnitude; current strongest same-statACbonus applies with other sources. Ready release does not grant again. Incapacity does not itself end this nonconcentration buff; ordinary expiry/source-suppression does. No additional armor, resistance, spell use or cast trigger from copies.",
  "submittedNewChoices": "Completed-cast timing, one nonstacking+1 record and original regular-start expiry.",
  "submittedWorkedCases": [
    "A saved-against rank 2 spell still grants+1 AC after resolution.",
    "Two ranked casts create one+1 record; a reaction attack during the first cast resolves before it begins."
  ],
  "decision": "Select current ranked-cast+1AC until next start over legacy10%/five seconds; completed failed-target casts qualify, countered casts do not, and distinct flat feats add.",
  "completeAuthoringProcedure": "At character level 6, after a completed personal ranked cast gain+1 AC until your next future regular start. NEW select active+1/regular-start over preserved 10%/5 seconds. It begins after the cast’s immediate resolution or successful Ready preparation, so does not protect against that cast’s earlier interruption attacks. Miss/all-save still qualify; a countered cast does not. Repeated legal casts refresh one same-family record without stacking magnitude; distinct eligible flat feat AC bonuses add under FS-03, after existing AC formula/item/class/spell arbitration. Ready release does not grant again. Incapacity does not itself end this nonconcentration buff; ordinary expiry/source-suppression does. No additional armor, resistance, spell use or cast trigger from copies.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A saved-against rank 2 spell still grants+1 AC after resolution.",
    "Two ranked casts create one+1 record; a reaction attack during the first cast resolves before it begins."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At character level 6, after a completed personal ranked cast gain+1 AC until your next future regular start. NEW select active+1/regular-start over preserved 10%/5 seconds. It begins after the cast’s immediate resolution or successful Ready preparation, so does not protect against that cast’s earlier interruption attacks. Miss/all-save still qualify; a countered cast does not. Repeated legal casts refresh one same-family record without stacking magnitude; distinct eligible flat feat AC bonuses add under FS-03, after existing AC formula/item/class/spell arbitration. Ready release does not grant again. Incapacity does not itself end this nonconcentration buff; ordinary expiry/source-suppression does. No additional armor, resistance, spell use or cast trigger from copies.

### Original-position authored review references

```json
[
  {
    "id": "MX-27-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/12"
  },
  {
    "id": "MX-27-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/13"
  }
]
```

## MX-28 — Quick Ritualist

### Complete original object

```json
{
  "id": "quick_ritualist",
  "name": "Quick Ritualist",
  "description": "Wisdom 14+ supports halving the listed ritual casting time.",
  "prerequisite": "Wisdom 14+",
  "effect": "Halve the additional casting time required to cast a spell as a ritual, to a minimum of 5 minutes.",
  "type": "Magic",
  "legacyEffect": "Ritual casting time halved",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Apply half to additional ritual casting time only, minimum5minutes; preserve base casting time and exact rounding. Bind actual ritual access, long rituals, interruption and other reductions. Ritual Caster/Ritual Channeler are pending dependencies, not automatic access or multiplicative approvals."
```

### Preserved original source direction (historical)

```json
{
  "featId": "quick_ritualist",
  "name": "Quick Ritualist",
  "cohort": "magic_extended",
  "questionId": "MX-28",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/27",
  "originalQuestion": "Apply half to additional ritual casting time only, minimum5minutes; preserve base casting time and exact rounding. Bind actual ritual access, long rituals, interruption and other reductions. Ritual Caster/Ritual Channeler are pending dependencies, not automatic access or multiplicative approvals.",
  "originalSourceObject": {
    "id": "quick_ritualist",
    "name": "Quick Ritualist",
    "description": "Wisdom 14+ supports halving the listed ritual casting time.",
    "prerequisite": "Wisdom 14+",
    "effect": "Halve the additional casting time required to cast a spell as a ritual, to a minimum of 5 minutes.",
    "type": "Magic",
    "legacyEffect": "Ritual casting time halved",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "d4225b24c84ee70b5267f0536929163a756c58d19208b2a492366f05018eb1ce",
  "submittedProcedure": "For a spell you can actually cast through a legal ritual route, halve only the route’s additional ritual time, with resulting additional time at least 5 minutes; retain the base printed casting time in full. NEW measure the result in elapsed seconds and round up to the next whole second so fractions never shorten a required interval. An original 10 minute addition becomes 5 minutes, not half the whole cast. An original shorter addition is not increased: use min(original additional time, max(300, ceil(original/2))). This explicit non-worsening interpretation preserves the minimum for reductions without penalizing a preexisting faster route. Components, formula/repertoire, costs, concentration, helpers and interruptions remain. It grants no Ritual tag or access; the separate proposed Ritual Caster overlay needs its own approval. Apply this additional-time change before any separately legal group active-time adjustment, whose minimum rule remains.",
  "submittedNewChoices": "Additional-time-only arithmetic, no worsening of already-shorter routes and second rounding.",
  "submittedWorkedCases": [
    "A 1 Action base plus 10 minutes ritual addition becomes the same 1 Action base plus 5 minutes.",
    "A source’s 2 minute special addition stays 2 minutes, and this feat creates no ritual permission."
  ],
  "decision": "Adopt half the added ritual labor, not base cast time, with a non-worsening five-minute floor and explicit composition with Ritual Channeler.",
  "completeAuthoringProcedure": "For a spell you can actually cast through a legal ritual route, halve only the route’s additional ritual time, with resulting additional time at least 5 minutes; retain the base printed casting time in full. NEW measure the result in elapsed seconds and round up to the next whole second so fractions never shorten a required interval. An original 10 minute addition becomes 5 minutes, not half the whole cast. An original shorter addition is not increased: use min(original additional time, max(300, ceil(original/2))). This explicit non-worsening interpretation preserves the minimum for reductions without penalizing a preexisting faster route. Components, formula/repertoire, costs, concentration, helpers and interruptions remain. It grants no Ritual tag or access; the separate proposed Ritual Caster overlay needs its own approval. Apply this additional-time change before any separately legal group active-time adjustment, whose minimum rule remains.\nNEW common ritual arithmetic: let B be the spell’s actual base casting labor and A its separately required added ritual labor, in whole seconds. Quick Ritualist changes A to min(A,max(300,ceil(A/2))), leaving B unchanged. This never lengthens an already shorter source procedure. Literal source-required elapsed waiting is not active labor to halve.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "For a rank1 ritual with base Action6seconds plus600seconds added ritual labor, Quick Ritualist gives6+300=306seconds. It does not halve the base casting Action.",
    "With Ritual Channeler as well,ceil(306×0.75)=230 would breach the6+300floor, so the result remains306seconds. No helper creates another spell, omitted component or concentration slot."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

For a spell you can actually cast through a legal ritual route, halve only the route’s additional ritual time, with resulting additional time at least 5 minutes; retain the base printed casting time in full. NEW measure the result in elapsed seconds and round up to the next whole second so fractions never shorten a required interval. An original 10 minute addition becomes 5 minutes, not half the whole cast. An original shorter addition is not increased: use min(original additional time, max(300, ceil(original/2))). This explicit non-worsening interpretation preserves the minimum for reductions without penalizing a preexisting faster route. Components, formula/repertoire, costs, concentration, helpers and interruptions remain. It grants no Ritual tag or access; the separate proposed Ritual Caster overlay needs its own approval. Apply this additional-time change before any separately legal group active-time adjustment, whose minimum rule remains.
NEW common ritual arithmetic: let B be the spell’s actual base casting labor and A its separately required added ritual labor, in whole seconds. Quick Ritualist changes A to min(A,max(300,ceil(A/2))), leaving B unchanged. This never lengthens an already shorter source procedure. Literal source-required elapsed waiting is not active labor to halve.

### Original-position authored review references

```json
[
  {
    "id": "MX-28-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/14"
  },
  {
    "id": "MX-28-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/15"
  },
  {
    "id": "FA-20",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/additionalBoundaryReviews/0"
  }
]
```

## MX-29 — Ritual Channeler

### Complete original object

```json
{
  "id": "ritual_channeler",
  "name": "Ritual Channeler",
  "description": "Intelligence 14+ supports the listed 25% faster group rituals.",
  "prerequisite": "Intelligence 14+",
  "effect": "When participating in a group ritual, reduce its required active casting time by 25 percent and count as two ordinary assistants.",
  "type": "Magic",
  "legacyEffect": "Group rituals 25% faster",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define a real group ritual and ordinary assistant procedure before applying25percent active-time reduction and two-assistant contribution. Specify assistant caps, multiple feat users, overlapping work, base versus additional time, rounding, interruptions and material/formula costs. Do not silently treat every crafting work order as a ritual."
```

### Preserved original source direction (historical)

```json
{
  "featId": "ritual_channeler",
  "name": "Ritual Channeler",
  "cohort": "magic_extended",
  "questionId": "MX-29",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/28",
  "originalQuestion": "Define a real group ritual and ordinary assistant procedure before applying25percent active-time reduction and two-assistant contribution. Specify assistant caps, multiple feat users, overlapping work, base versus additional time, rounding, interruptions and material/formula costs. Do not silently treat every crafting work order as a ritual.",
  "originalSourceObject": {
    "id": "ritual_channeler",
    "name": "Ritual Channeler",
    "description": "Intelligence 14+ supports the listed 25% faster group rituals.",
    "prerequisite": "Intelligence 14+",
    "effect": "When participating in a group ritual, reduce its required active casting time by 25 percent and count as two ordinary assistants.",
    "type": "Magic",
    "legacyEffect": "Group rituals 25% faster",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "18826e6cdcf456cbfb6e4b4e7e5d65e445f1c7966a3bed2f59091368331bc3ec",
  "submittedProcedure": "NEW a group ritual is one actual legally available ritual spell with a designated lead and at least one physically present willing assistant continuously performing that same ritual’s active work; it is not simultaneous crafting, travel or independent casts. Use the exact source’s assistant qualifications/cap. If it supplies none, the proposed default assistant must know that ritual or have proficiency in the lead’s actual relevant Arcana/Religion/Nature skill; count at most two ordinary assistant contributions, with no numeric roll bonus when the source has no assistant benefit. This feat-holder contributes as two ordinary assistants within that cap, never as two leads or two physical bodies for a separate location requirement. One or more holders reduce the group’s total active casting time once by 25%, rounding up seconds; passive waiting is unchanged. Apply after Quick Ritualist’s additional-time reduction, but never reduce that remaining additional ritual portion below 5 minutes unless it was already shorter. Source-required simultaneous people, costs, lead concentration, interruptions and minimum times remain. No multiplicative 25%stack or free spell/resource. NEW the double-assistant contribution applies only while actually serving as an assistant. A lead who owns this feat can supply the time reduction but cannot simultaneously count as two assistants; one person never performs both assigned jobs at once.",
  "submittedNewChoices": "Finite default group/assistant procedure and single 25%time reduction with preserved minimums.",
  "submittedWorkedCases": [
    "A 20 minute fully active ritual with no stronger minimum takes 15 minutes with one qualified Channeler.",
    "Two Channelers do not halve that time again and cannot replace two required bodies at distant ritual stations."
  ],
  "decision": "Adopt one25% group-labor reduction and double ordinary assistant contribution only for the actual assistant role; no extra physical bodies, fabricated check or per-helper compounding.",
  "completeAuthoringProcedure": "NEW a group ritual is one actual legally available ritual spell with a designated lead and at least one physically present willing assistant continuously performing that same ritual’s active work; it is not simultaneous crafting, travel or independent casts. Use the exact source’s assistant qualifications/cap. If it supplies none, the proposed default assistant must know that ritual or have proficiency in the lead’s actual relevant Arcana/Religion/Nature skill; count at most two ordinary assistant contributions, with no numeric roll bonus when the source has no assistant benefit. This feat-holder contributes as two ordinary assistants within that cap, never as two leads or two physical bodies for a separate location requirement. One or more holders reduce the group’s total active casting time once by 25%, rounding up seconds; passive waiting is unchanged. Apply after Quick Ritualist’s additional-time reduction, but never reduce that remaining additional ritual portion below 5 minutes unless it was already shorter. Source-required simultaneous people, costs, lead concentration, interruptions and minimum times remain. No multiplicative 25%stack or free spell/resource. NEW the double-assistant contribution applies only while actually serving as an assistant. A lead who owns this feat can supply the time reduction but cannot simultaneously count as two assistants; one person never performs both assigned jobs at once.\nNEW apply the one25% helper reduction to the actual total ritual labor after any Quick Ritualist reduction, never once per helper. For the standard added-ritual route, final total=min(previous total,max(B+300,ceil(previous total×3/4))). No reduction removes the actual base casting work or the five-minute added-ritual floor, and a source already shorter is not lengthened. Every required helper attends the full resulting procedure. No check or numeric helper bonus is invented where the actual source has none.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A source with600seconds base labor plus600seconds added ritual labor takes900seconds with the25% group reduction alone, respecting its600+300floor. Each actual helper works all900seconds.",
    "Two Channelers do not apply25% twice or count as two physically separate station operators. A source with no check receives no invented numeric helper bonus."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW a group ritual is one actual legally available ritual spell with a designated lead and at least one physically present willing assistant continuously performing that same ritual’s active work; it is not simultaneous crafting, travel or independent casts. Use the exact source’s assistant qualifications/cap. If it supplies none, the proposed default assistant must know that ritual or have proficiency in the lead’s actual relevant Arcana/Religion/Nature skill; count at most two ordinary assistant contributions, with no numeric roll bonus when the source has no assistant benefit. This feat-holder contributes as two ordinary assistants within that cap, never as two leads or two physical bodies for a separate location requirement. One or more holders reduce the group’s total active casting time once by 25%, rounding up seconds; passive waiting is unchanged. Apply after Quick Ritualist’s additional-time reduction, but never reduce that remaining additional ritual portion below 5 minutes unless it was already shorter. Source-required simultaneous people, costs, lead concentration, interruptions and minimum times remain. No multiplicative 25%stack or free spell/resource. NEW the double-assistant contribution applies only while actually serving as an assistant. A lead who owns this feat can supply the time reduction but cannot simultaneously count as two assistants; one person never performs both assigned jobs at once.
NEW apply the one25% helper reduction to the actual total ritual labor after any Quick Ritualist reduction, never once per helper. For the standard added-ritual route, final total=min(previous total,max(B+300,ceil(previous total×3/4))). No reduction removes the actual base casting work or the five-minute added-ritual floor, and a source already shorter is not lengthened. Every required helper attends the full resulting procedure. No check or numeric helper bonus is invented where the actual source has none.

### Original-position authored review references

```json
[
  {
    "id": "MX-29-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/16"
  },
  {
    "id": "MX-29-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/17"
  }
]
```

## MX-30 — Runic Shield

### Complete original object

```json
{
  "id": "runic_shield",
  "name": "Runic Shield",
  "description": "Wisdom 14+ supports the listed absorption of the first 50 spell damage per combat.",
  "prerequisite": "Wisdom 14+",
  "effect": "At the start of combat, gain a runic ward with 15 hit points. The ward absorbs spell damage first and vanishes when depleted. It refreshes after a short rest.",
  "type": "Magic",
  "legacyEffect": "Absorbs first 50 spell damage per combat",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve description50 versus active15 ward HP and start-of-combat versus Short Rest refresh. Define ward versus temporary HP, one physical owner/source identity, spell-only damage interception order, damage event and concentration/Wound thresholds, depletion, encounter farming and transfer. Preserve both activation and recovery clauses explicitly."
```

### Preserved original source direction (historical)

```json
{
  "featId": "runic_shield",
  "name": "Runic Shield",
  "cohort": "magic_extended",
  "questionId": "MX-30",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/29",
  "originalQuestion": "Resolve description50 versus active15 ward HP and start-of-combat versus Short Rest refresh. Define ward versus temporary HP, one physical owner/source identity, spell-only damage interception order, damage event and concentration/Wound thresholds, depletion, encounter farming and transfer. Preserve both activation and recovery clauses explicitly.",
  "originalSourceObject": {
    "id": "runic_shield",
    "name": "Runic Shield",
    "description": "Wisdom 14+ supports the listed absorption of the first 50 spell damage per combat.",
    "prerequisite": "Wisdom 14+",
    "effect": "At the start of combat, gain a runic ward with 15 hit points. The ward absorbs spell damage first and vanishes when depleted. It refreshes after a short rest.",
    "type": "Magic",
    "legacyEffect": "Absorbs first 50 spell damage per combat",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "86fe7ff8c18e04df50c7c8172eb7dc3bd928b3e2e63a4defd5d279c5afda9259",
  "submittedProcedure": "NEW select 15 ward HP over preserved 50. The feat has one armed grant per beneficial SR/LR; acquisition arms it. At the first real encounter start after arming, automatically create one personal runic ward with 15 points and spend that entitlement, even if surprised/incapacitated; a dead creature receives none. It persists between encounters until depleted or the next beneficial SR/LR, when any old ward ends and entitlement rearms for the next combat, not immediate refill in combat. Repeated initiative does not refill it. This is a distinct spell-only ward, not temp HP: after ordinary defenses and before temp HP, intercept up to its remaining points of actual incoming spell damage in stable component order. Nonspell damage bypasses it. Record ward absorption separately, excluded from actual damage received by the body, Wound/death thresholds and concentration checks; any surviving packet resolves once normally. No transfer, double ledger, HP healing, return on revival or resource proc from ward absorption. Counterspell/dispel cannot target this nonspell passive ward without explicit applicable source permission.",
  "submittedNewChoices": "Separate 15 point spell-only pre-temp ward, one armed combat grant per rest and no encounter refills.",
  "submittedWorkedCases": [
    "A post-defense 20 spell-damage packet consumes 15 ward then passes 5 to temp HP/normal HP.",
    "A sword’s 8 nonspell damage ignores the ward entirely; starting another encounter does not restore spent ward points."
  ],
  "decision": "Select15 ward HP over legacy50, armed once by an actual beneficial rest and consumed across later encounters until refreshed; no encounter-entry refill farming.",
  "completeAuthoringProcedure": "NEW select 15 ward HP over preserved 50. The feat has one armed grant per beneficial SR/LR; acquisition arms it. At the first real encounter start after arming, automatically create one personal runic ward with 15 points and spend that entitlement, even if surprised/incapacitated; a dead creature receives none. It persists between encounters until depleted or the next beneficial SR/LR, when any old ward ends and entitlement rearms for the next combat, not immediate refill in combat. Repeated initiative does not refill it. This is a distinct spell-only ward, not temp HP: after ordinary defenses and before temp HP, intercept up to its remaining points of actual incoming spell damage in stable component order. Nonspell damage bypasses it. Record ward absorption separately, excluded from actual damage received by the body, Wound/death thresholds and concentration checks; any surviving packet resolves once normally. No transfer, double ledger, HP healing, return on revival or resource proc from ward absorption. Counterspell/dispel cannot target this nonspell passive ward without explicit applicable source permission.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A post-defense 20 spell-damage packet consumes 15 ward then passes 5 to temp HP/normal HP.",
    "A sword’s 8 nonspell damage ignores the ward entirely; starting another encounter does not restore spent ward points."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW select 15 ward HP over preserved 50. The feat has one armed grant per beneficial SR/LR; acquisition arms it. At the first real encounter start after arming, automatically create one personal runic ward with 15 points and spend that entitlement, even if surprised/incapacitated; a dead creature receives none. It persists between encounters until depleted or the next beneficial SR/LR, when any old ward ends and entitlement rearms for the next combat, not immediate refill in combat. Repeated initiative does not refill it. This is a distinct spell-only ward, not temp HP: after ordinary defenses and before temp HP, intercept up to its remaining points of actual incoming spell damage in stable component order. Nonspell damage bypasses it. Record ward absorption separately, excluded from actual damage received by the body, Wound/death thresholds and concentration checks; any surviving packet resolves once normally. No transfer, double ledger, HP healing, return on revival or resource proc from ward absorption. Counterspell/dispel cannot target this nonspell passive ward without explicit applicable source permission.

### Original-position authored review references

```json
[
  {
    "id": "MX-30-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/18"
  },
  {
    "id": "MX-30-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/19"
  }
]
```

## MX-31 — Silent Casting

### Complete original object

```json
{
  "id": "silent_casting",
  "name": "Silent Casting",
  "description": "Level 7 supports the listed casting without a verbal component.",
  "prerequisite": "Level 7",
  "effect": "You may cast a spell without its verbal component by increasing its RP cost by 1. This cannot bypass components with a stated magical command word.",
  "type": "Magic",
  "legacyEffect": "Cast without verbal component",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define+1 RP surcharge for removing V at declaration, price ordering, rank0 and charge-only casts without an RP interface/pool. Preserve command-word exclusion and S/material requirements; identify what a stated magical command word means from actual spell text. No universal undetectable casting."
```

### Preserved original source direction (historical)

```json
{
  "featId": "silent_casting",
  "name": "Silent Casting",
  "cohort": "magic_extended",
  "questionId": "MX-31",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/30",
  "originalQuestion": "Define+1 RP surcharge for removing V at declaration, price ordering, rank0 and charge-only casts without an RP interface/pool. Preserve command-word exclusion and S/material requirements; identify what a stated magical command word means from actual spell text. No universal undetectable casting.",
  "originalSourceObject": {
    "id": "silent_casting",
    "name": "Silent Casting",
    "description": "Level 7 supports the listed casting without a verbal component.",
    "prerequisite": "Level 7",
    "effect": "You may cast a spell without its verbal component by increasing its RP cost by 1. This cannot bypass components with a stated magical command word.",
    "type": "Magic",
    "legacyEffect": "Cast without verbal component",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "d747a352a2965c345cd78b03afbcc8fca4a203d873322dcb302d141e0fd7d52d",
  "submittedProcedure": "At declaration of a spell actually requiringV, remove only that verbal component by adding 1 actual RP to its price before ordinary final cost adjustments. NEW the independent 1 RP payment cannot itself be waived by a charged/free normal-rank route; an actualRPpool and sufficient final payment are required. Rank 0 can use the feat and still pays the independent surcharge; cantrip strain rules remain. A component or exact activation explicitly demanding a magical command word cannot be removed. Ordinary audibleV alone is not a protected command word unless identified as such by the operative source. PreserveS, F/materials, physical access and action permissions. Silence no longer blocks the removedV, but Incapacitated/other restrictions remain. It creates neither undetectable casting nor automatic concealment; other visible components/effects and observers’ real senses still determine interruption eligibility.",
  "submittedNewChoices": "Only explicitV removal with real independentRPprice and exact command-word exclusion.",
  "submittedWorkedCases": [
    "A V, S cantrip may be cast silently with S and 1 real RP, provided every other permission holds.",
    "A charged spell cast by someone with noRPpool cannot pay the extra 1 RP through its charge."
  ],
  "decision": "Keep+1 real independent RP to remove V only; no removal of F/S, actual command channels or source-required spoken effects.",
  "completeAuthoringProcedure": "At declaration of a spell actually requiringV, remove only that verbal component by adding 1 actual RP to its price before ordinary final cost adjustments. NEW the independent 1 RP payment cannot itself be waived by a charged/free normal-rank route; an actualRPpool and sufficient final payment are required. Rank 0 can use the feat and still pays the independent surcharge; cantrip strain rules remain. A component or exact activation explicitly demanding a magical command word cannot be removed. Ordinary audibleV alone is not a protected command word unless identified as such by the operative source. PreserveS, F/materials, physical access and action permissions. Silence no longer blocks the removedV, but Incapacitated/other restrictions remain. It creates neither undetectable casting nor automatic concealment; other visible components/effects and observers’ real senses still determine interruption eligibility.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A V, S cantrip may be cast silently with S and 1 real RP, provided every other permission holds.",
    "A charged spell cast by someone with noRPpool cannot pay the extra 1 RP through its charge."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At declaration of a spell actually requiringV, remove only that verbal component by adding 1 actual RP to its price before ordinary final cost adjustments. NEW the independent 1 RP payment cannot itself be waived by a charged/free normal-rank route; an actualRPpool and sufficient final payment are required. Rank 0 can use the feat and still pays the independent surcharge; cantrip strain rules remain. A component or exact activation explicitly demanding a magical command word cannot be removed. Ordinary audibleV alone is not a protected command word unless identified as such by the operative source. PreserveS, F/materials, physical access and action permissions. Silence no longer blocks the removedV, but Incapacitated/other restrictions remain. It creates neither undetectable casting nor automatic concealment; other visible components/effects and observers’ real senses still determine interruption eligibility.

### Original-position authored review references

```json
[
  {
    "id": "MX-31-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/20"
  },
  {
    "id": "MX-31-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/21"
  }
]
```

## MX-32 — Spell Deflection

### Complete original object

```json
{
  "id": "spell_deflection",
  "name": "Spell Deflection",
  "description": "Intelligence 16+ supports the listed 10% chance to redirect hostile spell.",
  "prerequisite": "Intelligence 16+",
  "effect": "Once per long rest, when targeted by a single-target hostile spell, roll a d20. On 16 or higher, redirect it to another legal target within its original range; otherwise gain advantage on the saving throw.",
  "type": "Magic",
  "legacyEffect": "10% chance to redirect hostile spell",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Use actual d20≥16, not legacy10percent. Define optional Long Rest declaration, action/Reaction, hostile single-target spell, legal new target from original origin, save/attack handling and no-legal-target outcome. Preserve fallback advantage, prevent reflection recursion and distinguish redirects from new casts."
```

### Preserved original source direction (historical)

```json
{
  "featId": "spell_deflection",
  "name": "Spell Deflection",
  "cohort": "magic_extended",
  "questionId": "MX-32",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/31",
  "originalQuestion": "Use actual d20≥16, not legacy10percent. Define optional Long Rest declaration, action/Reaction, hostile single-target spell, legal new target from original origin, save/attack handling and no-legal-target outcome. Preserve fallback advantage, prevent reflection recursion and distinguish redirects from new casts.",
  "originalSourceObject": {
    "id": "spell_deflection",
    "name": "Spell Deflection",
    "description": "Intelligence 16+ supports the listed 10% chance to redirect hostile spell.",
    "prerequisite": "Intelligence 16+",
    "effect": "Once per long rest, when targeted by a single-target hostile spell, roll a d20. On 16 or higher, redirect it to another legal target within its original range; otherwise gain advantage on the saving throw.",
    "type": "Magic",
    "legacyEffect": "10% chance to redirect hostile spell",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "9ad53f4997080cefafe4451ae900240426645f4537eec298a3f4f1c858876f71",
  "submittedProcedure": "Once LR, NEW spend a Reaction when a hostile pending spell has selected you as its sole creature target, after ordinary cast interruptions but before its attack/save/effect resolution. It must be an actual single-target payload, not one target remaining from an area or multi-target mode. Roll an unmodifiedd 20;16–20 redirects, preserving this explicit 25%procedure over legacy 10%. On success choose a different legal creature under the original spell’s actual target restrictions, range/line measured from the original origin, personally perceived by you where necessary; the original caster remains owner and supplies all stats/choices. Recheck legality, then use fresh original attack/save procedure against that new target; nothing resolves against you. If no legal new target exists, or on 1–15, the spell continues against you with advantage on each actual initial save it requires; no save is invented for an attack/automatic spell. Use/Reaction remain spent. A redirected/reflected/copy packet cannot be redirected again by this family or Spell Reflection. Protected/self-only/source-specific exclusions remain.",
  "submittedNewChoices": "Reaction window, d20 threshold, no-target fallback and shared redirect-once provenance.",
  "submittedWorkedCases": [
    "Roll 17 redirects an eligible hostile ray to another legal creature within the original caster’s range.",
    "Roll 9 against an attack spell grants no save orACbonus; the original attack proceeds normally."
  ],
  "decision": "Select one-LR unmodified d20≥16 redirection over legacy10%; actual sole-target eligibility, paid Reaction and fallback saving advantage create no new save.",
  "completeAuthoringProcedure": "Once LR, NEW spend a Reaction when a hostile pending spell has selected you as its sole creature target, after ordinary cast interruptions but before its attack/save/effect resolution. It must be an actual single-target payload, not one target remaining from an area or multi-target mode. Roll an unmodifiedd 20;16–20 redirects, preserving this explicit 25%procedure over legacy 10%. On success choose a different legal creature under the original spell’s actual target restrictions, range/line measured from the original origin, personally perceived by you where necessary; the original caster remains owner and supplies all stats/choices. Recheck legality, then use fresh original attack/save procedure against that new target; nothing resolves against you. If no legal new target exists, or on 1–15, the spell continues against you with advantage on each actual initial save it requires; no save is invented for an attack/automatic spell. Use/Reaction remain spent. A redirected/reflected/copy packet cannot be redirected again by this family or Spell Reflection. Protected/self-only/source-specific exclusions remain.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Roll 17 redirects an eligible hostile ray to another legal creature within the original caster’s range.",
    "Roll 9 against an attack spell grants no save orACbonus; the original attack proceeds normally."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR, NEW spend a Reaction when a hostile pending spell has selected you as its sole creature target, after ordinary cast interruptions but before its attack/save/effect resolution. It must be an actual single-target payload, not one target remaining from an area or multi-target mode. Roll an unmodifiedd 20;16–20 redirects, preserving this explicit 25%procedure over legacy 10%. On success choose a different legal creature under the original spell’s actual target restrictions, range/line measured from the original origin, personally perceived by you where necessary; the original caster remains owner and supplies all stats/choices. Recheck legality, then use fresh original attack/save procedure against that new target; nothing resolves against you. If no legal new target exists, or on 1–15, the spell continues against you with advantage on each actual initial save it requires; no save is invented for an attack/automatic spell. Use/Reaction remain spent. A redirected/reflected/copy packet cannot be redirected again by this family or Spell Reflection. Protected/self-only/source-specific exclusions remain.

### Original-position authored review references

```json
[
  {
    "id": "MX-32-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/22"
  },
  {
    "id": "MX-32-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/23"
  }
]
```

## MX-33 — Spell Reservoir

### Complete original object

```json
{
  "id": "spell_reservoir",
  "name": "Spell Reservoir",
  "description": "Intelligence 14+ supports the listed gain of 1 additional ranked-spell recovery per day.",
  "prerequisite": "Intelligence 14+",
  "effect": "Once per long rest after finishing a short rest, recover RP equal to your proficiency bonus.",
  "type": "Magic",
  "legacyEffect": "Gain 1 additional spell slot per day",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Specify completion of an actual Short Rest within one Long Rest use ledger, PB amount, RP cap and timing with ordinary rest recovery. No new spell slot, maximum RP increase, charge conversion or repeated claim from one rest event; source description and old slot wording stay separately preserved."
```

### Preserved original source direction (historical)

```json
{
  "featId": "spell_reservoir",
  "name": "Spell Reservoir",
  "cohort": "magic_extended",
  "questionId": "MX-33",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/32",
  "originalQuestion": "Specify completion of an actual Short Rest within one Long Rest use ledger, PB amount, RP cap and timing with ordinary rest recovery. No new spell slot, maximum RP increase, charge conversion or repeated claim from one rest event; source description and old slot wording stay separately preserved.",
  "originalSourceObject": {
    "id": "spell_reservoir",
    "name": "Spell Reservoir",
    "description": "Intelligence 14+ supports the listed gain of 1 additional ranked-spell recovery per day.",
    "prerequisite": "Intelligence 14+",
    "effect": "Once per long rest after finishing a short rest, recover RP equal to your proficiency bonus.",
    "type": "Magic",
    "legacyEffect": "Gain 1 additional spell slot per day",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "bd213445cee9d049335a2a4fbe73e3b93451ffe7d41adff00209e69c1a730f41",
  "submittedProcedure": "Once LR, immediately after completing a beneficial SR and its ordinary recovery, optionally restore currentPBactual RP capped by remaining merged-pool headroom. Commit theLRuse and that actual rest-event claim together; another listener, duplicate receipt or resumed rest completion cannot claim again. If no headroom, you may decline without spending, but cannot bank that past rest’s trigger for later; a later beneficial SR can supply a new opportunity while theLRuse remains. It creates no maximumRPincrease, charge, slot, second classpool or independent Retune. A long rest alone does not count as the printedSRtrigger. PB changes before a future legal use affect that use’s amount but never refresh spent entitlement.",
  "submittedNewChoices": "Post-normalSRrecovery timing and no banked completion claim.",
  "submittedWorkedCases": [
    "PB 4 with 2 RP missing after normalSRrecovery restores 2 and spends theLRuse.",
    "At full RP you may decline; spending RP later does not reopen that already-finished rest."
  ],
  "decision": "Keep one LR-bounded recovery at a genuine beneficial short-rest completion, capped by actual PB and headroom; no old-rest trigger banking.",
  "completeAuthoringProcedure": "Once LR, immediately after completing a beneficial SR and its ordinary recovery, optionally restore currentPBactual RP capped by remaining merged-pool headroom. Commit theLRuse and that actual rest-event claim together; another listener, duplicate receipt or resumed rest completion cannot claim again. If no headroom, you may decline without spending, but cannot bank that past rest’s trigger for later; a later beneficial SR can supply a new opportunity while theLRuse remains. It creates no maximumRPincrease, charge, slot, second classpool or independent Retune. A long rest alone does not count as the printedSRtrigger. PB changes before a future legal use affect that use’s amount but never refresh spent entitlement.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "PB 4 with 2 RP missing after normalSRrecovery restores 2 and spends theLRuse.",
    "At full RP you may decline; spending RP later does not reopen that already-finished rest."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR, immediately after completing a beneficial SR and its ordinary recovery, optionally restore currentPBactual RP capped by remaining merged-pool headroom. Commit theLRuse and that actual rest-event claim together; another listener, duplicate receipt or resumed rest completion cannot claim again. If no headroom, you may decline without spending, but cannot bank that past rest’s trigger for later; a later beneficial SR can supply a new opportunity while theLRuse remains. It creates no maximumRPincrease, charge, slot, second classpool or independent Retune. A long rest alone does not count as the printedSRtrigger. PB changes before a future legal use affect that use’s amount but never refresh spent entitlement.

### Original-position authored review references

```json
[
  {
    "id": "MX-33-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/24"
  },
  {
    "id": "MX-33-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/25"
  }
]
```

## MX-34 — Spellweave

### Complete original object

```json
{
  "id": "spellweave",
  "name": "Spellweave",
  "description": "Wisdom 14+ supports the listed stacking of minor buffs onto the next spell.",
  "prerequisite": "Wisdom 14+",
  "effect": "When you cast a spell that grants a minor buff, you may hold that buff until the end of your next turn and apply it to the next spell you cast instead. Only one buff may be held.",
  "type": "Magic",
  "legacyEffect": "Stack minor buffs onto next spell",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define a finite meaning of minor buff and eligible transfer rather than arbitrary Director improvisation. Specify original recipient/payment, one held record, expiry, concentration, next actual cast attachment and components/scaling. Preserve every source clause while preventing duplicated buffs, resources or impossible effect-type conversions."
```

### Preserved original source direction (historical)

```json
{
  "featId": "spellweave",
  "name": "Spellweave",
  "cohort": "magic_extended",
  "questionId": "MX-34",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/33",
  "originalQuestion": "Define a finite meaning of minor buff and eligible transfer rather than arbitrary Director improvisation. Specify original recipient/payment, one held record, expiry, concentration, next actual cast attachment and components/scaling. Preserve every source clause while preventing duplicated buffs, resources or impossible effect-type conversions.",
  "originalSourceObject": {
    "id": "spellweave",
    "name": "Spellweave",
    "description": "Wisdom 14+ supports the listed stacking of minor buffs onto the next spell.",
    "prerequisite": "Wisdom 14+",
    "effect": "When you cast a spell that grants a minor buff, you may hold that buff until the end of your next turn and apply it to the next spell you cast instead. Only one buff may be held.",
    "type": "Magic",
    "legacyEffect": "Stack minor buffs onto next spell",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "b1daa6ff11260688ede3baaf513b690e37acbe89399c67b8896d96eafc962d76",
  "submittedProcedure": "NEW use the finite three-spell minor-buff table below: personally cast Guidance, Resistance or True Strike with yourself as the otherwise legal recipient. At its completion hold that entire one-use buff instead of receiving it normally; only one held record, replacing loses the old. Original costs, cast history and earlier deadline remain, with an additional deadline at your next future regular end. The next actual spell you commit consumes/attaches the record automatically, even if countered or unsuitable; no indefinite skipping. Guidance adds its one 1d4 only to one actual ability/task check made by that next spell, declared before rolling; Resistance adds its one 1d4 only to one actual concentration save maintaining that next spell; True Strike grants advantage only on that next spell’s first actual spell attack. They create no check/save/attack. The attachment expires at the original held deadline or actual spell end, whichever first, even if unused. Current one-bonus-die/advantage rules apply. A copied buff, borrowed duplicate or another Spellweave cannot be held; no duration/resource/HP/stat transfer or new cast.",
  "submittedNewChoices": "Explicit NEW whitelist and typed transfer meanings replace the undefined minor-buff promise without claiming recovered canon.",
  "submittedWorkedCases": [
    "Held Guidance attaches to a legal next Counterspell and can add 1d4 to its actual counter check.",
    "Held True Strike consumed by a next spell with no attack produces no benefit and cannot wait for a third cast."
  ],
  "decision": "Adopt the closed Guidance/Resistance/True Strike transfer table using the actual current non-concentration payloads; one real held buff, no invented check/save or generic Insight exchange.",
  "completeAuthoringProcedure": "NEW use the finite three-spell minor-buff table below: personally cast Guidance, Resistance or True Strike with yourself as the otherwise legal recipient. At its completion hold that entire one-use buff instead of receiving it normally; only one held record, replacing loses the old. Original costs, cast history and earlier deadline remain, with an additional deadline at your next future regular end. The next actual spell you commit consumes/attaches the record automatically, even if countered or unsuitable; no indefinite skipping. Guidance adds its one 1d4 only to one actual ability/task check made by that next spell, declared before rolling; Resistance adds its one 1d4 only to one actual concentration save maintaining that next spell; True Strike grants advantage only on that next spell’s first actual spell attack. They create no check/save/attack. The attachment expires at the original held deadline or actual spell end, whichever first, even if unused. Current one-bonus-die/advantage rules apply. A copied buff, borrowed duplicate or another Spellweave cannot be held; no duration/resource/HP/stat transfer or new cast.\nThe three selected current buffs are non-concentration spells. Holding/attaching their one-use benefit adds no concentration requirement and does not change that source fact. There is still only one held Spellweave record and each original deadline/cost/history; no newly invented check or save may redeem it.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Held Guidance attaches to a legal next Counterspell and can add 1d4 to its actual counter check.",
    "Held True Strike consumed by a next spell with no attack produces no benefit and cannot wait for a third cast."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW use the finite three-spell minor-buff table below: personally cast Guidance, Resistance or True Strike with yourself as the otherwise legal recipient. At its completion hold that entire one-use buff instead of receiving it normally; only one held record, replacing loses the old. Original costs, cast history and earlier deadline remain, with an additional deadline at your next future regular end. The next actual spell you commit consumes/attaches the record automatically, even if countered or unsuitable; no indefinite skipping. Guidance adds its one 1d4 only to one actual ability/task check made by that next spell, declared before rolling; Resistance adds its one 1d4 only to one actual concentration save maintaining that next spell; True Strike grants advantage only on that next spell’s first actual spell attack. They create no check/save/attack. The attachment expires at the original held deadline or actual spell end, whichever first, even if unused. Current one-bonus-die/advantage rules apply. A copied buff, borrowed duplicate or another Spellweave cannot be held; no duration/resource/HP/stat transfer or new cast.
The three selected current buffs are non-concentration spells. Holding/attaching their one-use benefit adds no concentration requirement and does not change that source fact. There is still only one held Spellweave record and each original deadline/cost/history; no newly invented check or save may redeem it.

### Original-position authored review references

```json
[
  {
    "id": "MX-34-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/26"
  },
  {
    "id": "MX-34-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/27"
  },
  {
    "id": "FA-21",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/additionalBoundaryReviews/1"
  }
]
```

## MX-35 — Still Casting

### Complete original object

```json
{
  "id": "still_casting",
  "name": "Still Casting",
  "description": "Level 7 supports the listed casting without somatic gestures.",
  "prerequisite": "Level 7",
  "effect": "You may cast a spell without its somatic component by increasing its RP cost by 1. This does not function while fully restrained.",
  "type": "Magic",
  "legacyEffect": "Cast without somatic gestures",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define+1 RP surcharge for removing S and actual fully-restrained boundary against current Restrained/hand rules. Specify charge-only/cantrip casts, price order, material/focus handling and V. Removing somatic gestures does not supply hands for other components or permit actions under Incapacitated."
```

### Preserved original source direction (historical)

```json
{
  "featId": "still_casting",
  "name": "Still Casting",
  "cohort": "magic_extended",
  "questionId": "MX-35",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/34",
  "originalQuestion": "Define+1 RP surcharge for removing S and actual fully-restrained boundary against current Restrained/hand rules. Specify charge-only/cantrip casts, price order, material/focus handling and V. Removing somatic gestures does not supply hands for other components or permit actions under Incapacitated.",
  "originalSourceObject": {
    "id": "still_casting",
    "name": "Still Casting",
    "description": "Level 7 supports the listed casting without somatic gestures.",
    "prerequisite": "Level 7",
    "effect": "You may cast a spell without its somatic component by increasing its RP cost by 1. This does not function while fully restrained.",
    "type": "Magic",
    "legacyEffect": "Cast without somatic gestures",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "5a2efe5fee621693b5e704398da6ba582bced1b65e9523c040cefb9a8e03c7c1",
  "submittedProcedure": "At declaration of a spell requiringS, remove only that somatic component by adding 1 actual RP before final pricing; use Silent Casting’s independent-surcharge convention, including actualRPrequirement for rank 0/charged routes. NEW fully restrained means actual hands/arms physically or explicitly magically immobilized so no usable casting gesture exists; CoreRestrained alone imposes its printed penalties and does not prove that anatomy restriction. This feat expressly fails under such complete physical/explicit gesture immobilization, despite removing ordinaryS. It also supplies no Action under Incapacitated, no freedom from binding, and no hand for actualF/material manipulation. RemovingS andV with two feats pays both independent surcharges; each protected command/material requirement remains. Spell perception/counterability follows real remaining cues.",
  "submittedNewChoices": "Exact physical/explicit gesture restraint boundary, avoiding invented universal CoreRestrained casting ban.",
  "submittedWorkedCases": [
    "A net’s actual full arm binding blocks this feat; a source’s mere Speed 0/Restrained penalty need not.",
    "RemovingS still leaves a required held focus that the caster must legally handle."
  ],
  "decision": "Keep+1 real independent RP to remove S only with genuine remaining component access; no assumption every restraint disables hands or focus, and no V waiver.",
  "completeAuthoringProcedure": "At declaration of a spell requiringS, remove only that somatic component by adding 1 actual RP before final pricing; use Silent Casting’s independent-surcharge convention, including actualRPrequirement for rank 0/charged routes. NEW fully restrained means actual hands/arms physically or explicitly magically immobilized so no usable casting gesture exists; CoreRestrained alone imposes its printed penalties and does not prove that anatomy restriction. This feat expressly fails under such complete physical/explicit gesture immobilization, despite removing ordinaryS. It also supplies no Action under Incapacitated, no freedom from binding, and no hand for actualF/material manipulation. RemovingS andV with two feats pays both independent surcharges; each protected command/material requirement remains. Spell perception/counterability follows real remaining cues.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A net’s actual full arm binding blocks this feat; a source’s mere Speed 0/Restrained penalty need not.",
    "RemovingS still leaves a required held focus that the caster must legally handle."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At declaration of a spell requiringS, remove only that somatic component by adding 1 actual RP before final pricing; use Silent Casting’s independent-surcharge convention, including actualRPrequirement for rank 0/charged routes. NEW fully restrained means actual hands/arms physically or explicitly magically immobilized so no usable casting gesture exists; CoreRestrained alone imposes its printed penalties and does not prove that anatomy restriction. This feat expressly fails under such complete physical/explicit gesture immobilization, despite removing ordinaryS. It also supplies no Action under Incapacitated, no freedom from binding, and no hand for actualF/material manipulation. RemovingS andV with two feats pays both independent surcharges; each protected command/material requirement remains. Spell perception/counterability follows real remaining cues.

### Original-position authored review references

```json
[
  {
    "id": "MX-35-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/28"
  },
  {
    "id": "MX-35-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/29"
  }
]
```

## MX-36 — Temporal Flux

### Complete original object

```json
{
  "id": "temporal_flux",
  "name": "Temporal Flux",
  "description": "Level 8 supports the listed slowing of enemies hit by time spells.",
  "prerequisite": "Level 8",
  "effect": "When a creature fails a save against one of your time-tagged spells, reduce its speed by 10 feet and prevent reactions until the start of its next turn.",
  "type": "Magic",
  "legacyEffect": "Slow all enemies hit by time spells",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Identify exact time-tagged spell authority and failed-save trigger. Bind−10ft Speed with current strongest/stacking floors and no-Reaction component until target next regular start, repeated/multiple-source effects and cure/suppression. No legacy all-hits trigger or enabling unfinished Time Loop."
```

### Preserved original source direction (historical)

```json
{
  "featId": "temporal_flux",
  "name": "Temporal Flux",
  "cohort": "magic_extended",
  "questionId": "MX-36",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/35",
  "originalQuestion": "Identify exact time-tagged spell authority and failed-save trigger. Bind−10ft Speed with current strongest/stacking floors and no-Reaction component until target next regular start, repeated/multiple-source effects and cure/suppression. No legacy all-hits trigger or enabling unfinished Time Loop.",
  "originalSourceObject": {
    "id": "temporal_flux",
    "name": "Temporal Flux",
    "description": "Level 8 supports the listed slowing of enemies hit by time spells.",
    "prerequisite": "Level 8",
    "effect": "When a creature fails a save against one of your time-tagged spells, reduce its speed by 10 feet and prevent reactions until the start of its next turn.",
    "type": "Magic",
    "legacyEffect": "Slow all enemies hit by time spells",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "64677fd3c7c2e8b5b3336f5ba306c211523465a24578473cde0493ebefa3f102",
  "submittedProcedure": "At character level 8, when a creature fails an actual save against your personally cast time-tagged spell, apply one softSpeed−10 ft record and one no-new-Reactions component until its next future regular start. NEW finite feat-tag overlay: Slow’s two actual modes, Haste and Future Echo only; current source tags do not supply an explicitTime tag. Their full current spell procedures remain unchanged, and a save-less buff creates no trigger. Wider tags require separate review; spell names or narrative time flavor alone do not qualify. Speed records compete under current strongest-adverse-control arithmetic rather than add;0 floor, real modes and existing movement spent remain. Already committed Reactions finish. Same owner/target/profile refreshes one record without extra magnitude; different sources retain their real deadlines. No new save, hardActiondenial, extra turn, state restoration or enabledTime Loop.",
  "submittedNewChoices": "Explicit NEW three-identity tag overlay and exact target-start soft-control expiry.",
  "submittedWorkedCases": [
    "A failed Slow save on Speed 30 already produces halfSpeed 15; Flux−10 competes as 20, so effectiveSpeed stays 15.",
    "Haste ordinarily has no recipient save, so its new feat tag alone does not trigger Flux."
  ],
  "decision": "Adopt feat-only Time membership for Slow/Haste/Future Echo, but require an actual failed save; no Save appears on the save-less comparison cards.",
  "completeAuthoringProcedure": "At character level 8, when a creature fails an actual save against your personally cast time-tagged spell, apply one softSpeed−10 ft record and one no-new-Reactions component until its next future regular start. NEW finite feat-tag overlay: Slow’s two actual modes, Haste and Future Echo only; current source tags do not supply an explicitTime tag. Their full current spell procedures remain unchanged, and a save-less buff creates no trigger. Wider tags require separate review; spell names or narrative time flavor alone do not qualify. Speed records compete under current strongest-adverse-control arithmetic rather than add;0 floor, real modes and existing movement spent remain. Already committed Reactions finish. Same owner/target/profile refreshes one record without extra magnitude; different sources retain their real deadlines. No new save, hardActiondenial, extra turn, state restoration or enabledTime Loop.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A failed Slow save on Speed 30 already produces halfSpeed 15; Flux−10 competes as 20, so effectiveSpeed stays 15.",
    "Haste ordinarily has no recipient save, so its new feat tag alone does not trigger Flux."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At character level 8, when a creature fails an actual save against your personally cast time-tagged spell, apply one softSpeed−10 ft record and one no-new-Reactions component until its next future regular start. NEW finite feat-tag overlay: Slow’s two actual modes, Haste and Future Echo only; current source tags do not supply an explicitTime tag. Their full current spell procedures remain unchanged, and a save-less buff creates no trigger. Wider tags require separate review; spell names or narrative time flavor alone do not qualify. Speed records compete under current strongest-adverse-control arithmetic rather than add;0 floor, real modes and existing movement spent remain. Already committed Reactions finish. Same owner/target/profile refreshes one record without extra magnitude; different sources retain their real deadlines. No new save, hardActiondenial, extra turn, state restoration or enabledTime Loop.

### Original-position authored review references

```json
[
  {
    "id": "MX-36-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/30"
  },
  {
    "id": "MX-36-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/31"
  }
]
```

## MX-37 — Twin Cast

### Complete original object

```json
{
  "id": "twin_cast",
  "name": "Twin Cast",
  "description": "Level 8 supports the listed 5% chance to auto-cast a spell twice.",
  "prerequisite": "Level 8",
  "effect": "Once per long rest, after casting a single-target spell of Tier 1–3, target a second legal creature within range without paying additional RP.",
  "type": "Magic",
  "legacyEffect": "5% chance to auto-cast spell twice",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Use once-per-Long-Rest second legal creature after a Tier1–3 single-target cast, not legacy5percent double cast. Define attack/save results, concentration, components, range/sight recheck, origin, already-multitarget/upcast spells and one source identity. No duplicate refund, extra summon or copied paid resource."
```

### Preserved original source direction (historical)

```json
{
  "featId": "twin_cast",
  "name": "Twin Cast",
  "cohort": "magic_extended",
  "questionId": "MX-37",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/36",
  "originalQuestion": "Use once-per-Long-Rest second legal creature after a Tier1–3 single-target cast, not legacy5percent double cast. Define attack/save results, concentration, components, range/sight recheck, origin, already-multitarget/upcast spells and one source identity. No duplicate refund, extra summon or copied paid resource.",
  "originalSourceObject": {
    "id": "twin_cast",
    "name": "Twin Cast",
    "description": "Level 8 supports the listed 5% chance to auto-cast a spell twice.",
    "prerequisite": "Level 8",
    "effect": "Once per long rest, after casting a single-target spell of Tier 1–3, target a second legal creature within range without paying additional RP.",
    "type": "Magic",
    "legacyEffect": "5% chance to auto-cast spell twice",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "17ddc39fc895a0b6da8dbc206f20b617072f44314c2b5240caae1bb4f2c9b7d8",
  "submittedProcedure": "Once LR after a personal rank 1–3 single-creature spell completes its initial payload, choose one additional different creature currently legal under that same mode, range, sight, line of effect and willingness/type restrictions. NEW only an originally exactly-one-creature payload qualifies; no area, multi-ray/multi-target, Self-only, summon/object creation, resource/action-grant, resurrection, maximumHPchange or copied payload. Consume the feat use and extend that same cast’s original immediate damage/heal/condition/buff to the second recipient. Roll a fresh actual attack/save and native dice for that recipient; no newRPprice, cast, components, Dissonance/Refrain or class/featproc. Independent per-recipient material/HP/finite reserve requirements remain actual costs and must be affordable before choosing. One concentration ID governs both; original deadline and source target-ending rules remain. This is an explicit two-target exception only for this cast, not another spell identity or separate duration. Preserve old 5%autodouble wording as inactive alternative.",
  "submittedNewChoices": "One bounded additional original-payload recipient under one cast/concentration, with explicit nonduplicable categories.",
  "submittedWorkedCases": [
    "A legal rank 1 one-creature damage spell resolves anew against one second eligible creature without another baseRPcost.",
    "A spell already selecting up to two creatures cannot qualify merely because the caster chose only one."
  ],
  "decision": "Select one LR-bounded second legal target for rank1–3 over legacy5% repeated cast; native secondary result only, no extra cast/history/concentration or production.",
  "completeAuthoringProcedure": "Once LR after a personal rank 1–3 single-creature spell completes its initial payload, choose one additional different creature currently legal under that same mode, range, sight, line of effect and willingness/type restrictions. NEW only an originally exactly-one-creature payload qualifies; no area, multi-ray/multi-target, Self-only, summon/object creation, resource/action-grant, resurrection, maximumHPchange or copied payload. Consume the feat use and extend that same cast’s original immediate damage/heal/condition/buff to the second recipient. Roll a fresh actual attack/save and native dice for that recipient; no newRPprice, cast, components, Dissonance/Refrain or class/featproc. Independent per-recipient material/HP/finite reserve requirements remain actual costs and must be affordable before choosing. One concentration ID governs both; original deadline and source target-ending rules remain. This is an explicit two-target exception only for this cast, not another spell identity or separate duration. Preserve old 5%autodouble wording as inactive alternative.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A legal rank 1 one-creature damage spell resolves anew against one second eligible creature without another baseRPcost.",
    "A spell already selecting up to two creatures cannot qualify merely because the caster chose only one."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once LR after a personal rank 1–3 single-creature spell completes its initial payload, choose one additional different creature currently legal under that same mode, range, sight, line of effect and willingness/type restrictions. NEW only an originally exactly-one-creature payload qualifies; no area, multi-ray/multi-target, Self-only, summon/object creation, resource/action-grant, resurrection, maximumHPchange or copied payload. Consume the feat use and extend that same cast’s original immediate damage/heal/condition/buff to the second recipient. Roll a fresh actual attack/save and native dice for that recipient; no newRPprice, cast, components, Dissonance/Refrain or class/featproc. Independent per-recipient material/HP/finite reserve requirements remain actual costs and must be affordable before choosing. One concentration ID governs both; original deadline and source target-ending rules remain. This is an explicit two-target exception only for this cast, not another spell identity or separate duration. Preserve old 5%autodouble wording as inactive alternative.

### Original-position authored review references

```json
[
  {
    "id": "MX-37-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/32"
  },
  {
    "id": "MX-37-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/33"
  }
]
```

## MX-38 — Arcane Adaptation

### Complete original object

```json
{
  "id": "arcane_adaptation",
  "name": "Arcane Adaptation",
  "description": "Your magic bends to mirror what strikes you, letting you reshape your defenses after every reflected blow. Prestige lineage: Echomancer. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, Intelligence 13+",
  "effect": "When you successfully reflect or copy a spell or supernatural ability, you gain resistance to that damage type until the end of your next turn. Once per short rest, you may treat a copied effect as if you had always known it for 2 rounds.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you successfully reflect or copy a spell or supernatural ability, you gain resistance to that damage type until the end of your next turn. Once per short rest, you may treat a copied effect as if you had always known it for 2 rounds.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define actual successful reflection/copy event, which real damage type(s) grant resistance and end-of-next-turn duration. Separately bind Short Rest treat-as-known effect for2rounds: permitted repertoire/rank/costs/actions/copy profile. No permanent learning, boss/legendary access, recursive copying or borrowing of Mirrorsage class eligibility."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcane_adaptation",
  "name": "Arcane Adaptation",
  "cohort": "magic_extended",
  "questionId": "MX-38",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/37",
  "originalQuestion": "Define actual successful reflection/copy event, which real damage type(s) grant resistance and end-of-next-turn duration. Separately bind Short Rest treat-as-known effect for2rounds: permitted repertoire/rank/costs/actions/copy profile. No permanent learning, boss/legendary access, recursive copying or borrowing of Mirrorsage class eligibility.",
  "originalSourceObject": {
    "id": "arcane_adaptation",
    "name": "Arcane Adaptation",
    "description": "Your magic bends to mirror what strikes you, letting you reshape your defenses after every reflected blow. Prestige lineage: Echomancer. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability, Intelligence 13+",
    "effect": "When you successfully reflect or copy a spell or supernatural ability, you gain resistance to that damage type until the end of your next turn. Once per short rest, you may treat a copied effect as if you had always known it for 2 rounds.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you successfully reflect or copy a spell or supernatural ability, you gain resistance to that damage type until the end of your next turn. Once per short rest, you may treat a copied effect as if you had always known it for 2 rounds.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "1ba36366e81b072e6be761b4b7113ab03b8252f58ccb90a4f127a51e02caa949",
  "submittedProcedure": "After an actual successful legal reflection or capture of a spell/supernatural effect through a separately owned source, gain resistance to the one real damage type expressed by its selected copied/reflected component until your next future regular end. NEW choose one observed type for a mixed packet; nondamaging effects grant no damage resistance. It begins after capture/redirect, does not retroactively mitigate earlier damage, and grants no copying permission by itself. Once SR/LR at that event, also mark the one legal captured profile as temporarily known through your second future regular start. During that interval you may activate that exact bounded profile using its actual action, RP, components, rank ceiling and concentration, even if its original one-use record was consumed; no other original spell/monster ability is learned. Each activation is a copy retaining the original no-proc/no-copy/resource flags and the shared one-copy-release/round cap below. Existing Mirrorsage records retain their actual release costs/caps and printed bounded profile. No restoration of archive slots or legacy boss power. Expiry removes permission but not legitimately established effects before their own deadlines.",
  "submittedNewChoices": "One observed damage type and finite temporary known-profile route with paid repeat activations, no permanent repertoire.",
  "submittedWorkedCases": [
    "Capturing a fire Strike grants fire resistance through next end; adapting it permits paid bounded releases within two regular-start intervals.",
    "Copying a harmless warning reveals no damage type and grants no invented resistance."
  ],
  "decision": "Adopt bounded witnessed-type resistance and temporary access to one supported paid copy profile; no Mirrorsage archive, rank ceiling or release allowance is duplicated.",
  "completeAuthoringProcedure": "After an actual successful legal reflection or capture of a spell/supernatural effect through a separately owned source, gain resistance to the one real damage type expressed by its selected copied/reflected component until your next future regular end. NEW choose one observed type for a mixed packet; nondamaging effects grant no damage resistance. It begins after capture/redirect, does not retroactively mitigate earlier damage, and grants no copying permission by itself. Once SR/LR at that event, also mark the one legal captured profile as temporarily known through your second future regular start. During that interval you may activate that exact bounded profile using its actual action, RP, components, rank ceiling and concentration, even if its original one-use record was consumed; no other original spell/monster ability is learned. Each activation is a copy retaining the original no-proc/no-copy/resource flags and the shared one-copy-release/round cap below. Existing Mirrorsage records retain their actual release costs/caps and printed bounded profile. No restoration of archive slots or legacy boss power. Expiry removes permission but not legitimately established effects before their own deadlines.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Capturing a fire Strike grants fire resistance through next end; adapting it permits paid bounded releases within two regular-start intervals.",
    "Copying a harmless warning reveals no damage type and grants no invented resistance."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After an actual successful legal reflection or capture of a spell/supernatural effect through a separately owned source, gain resistance to the one real damage type expressed by its selected copied/reflected component until your next future regular end. NEW choose one observed type for a mixed packet; nondamaging effects grant no damage resistance. It begins after capture/redirect, does not retroactively mitigate earlier damage, and grants no copying permission by itself. Once SR/LR at that event, also mark the one legal captured profile as temporarily known through your second future regular start. During that interval you may activate that exact bounded profile using its actual action, RP, components, rank ceiling and concentration, even if its original one-use record was consumed; no other original spell/monster ability is learned. Each activation is a copy retaining the original no-proc/no-copy/resource flags and the shared one-new-feat-copy-commitment-per-numbered-round cap below (direct cast or Ready preparation, not completion of the same paid hold). Existing Mirrorsage records retain their actual release costs/caps and printed bounded profile. No restoration of archive slots or legacy boss power. Expiry removes permission but not legitimately established effects before their own deadlines.

FEAT335-COPY-RELEASE-SOURCE-01-ADDENDUM — controlling release completion.
NEW feat-copy chronological identity. Every paid feat-copy cast records `castFamilyKey = feat-copy::<canonicalSourceEffectId>`. `canonicalSourceEffectId` is the stable identity of the actually witnessed underlying spell/effect from which the bounded profile was captured; for a source-qualified monster ability use that ability's stable source identity. Changing the capture event, owner, Eldritch Echo/Mimicry/Arcane Adaptation permission, bounded profile, selected damage/type component, q, or qualifying casting-ability route does not create a new family. Copies sharing that key use the ordinary chronological Refrain history together. An ordinary cast of the underlying spell uses its ordinary spell family and does not share the feat-copy family; Mirrorsage Echo Release likewise keeps its own class family. A missing stable underlying source identity is ineligible for release rather than being assigned a favorable new key. This key grants no ordinary spell knowledge or access.

NEW feat-copy concentration tags. Strike: no. Burst: no. Mend: no. Ward: yes. Hindrance: yes. Boon: yes. Step: no; its movement/teleport resolves instantaneously. A concentration-required copy establishes the releaser's one concentration burden during casting commitment under the ordinary sequence, ending an incompatible existing concentration before the counter window. If that cast is later countered, prior concentration remains ended and no copied lasting effect remains. Loss of concentration ends the Ward/Hindrance/Boon copied effect immediately; their printed earlier deadlines still cap duration. Immediate profiles establish no new concentration burden. Ready is separate: preparation already occupies concentration. On release, an immediate profile resolves and that Ready concentration ends with the released spell; a concentration-required Ward/Hindrance/Boon continues on that same one concentration burden, never a second slot. No witnessed original concentration tag is inherited or used to change these seven profile tags.

COPY-ROUTE STRAIN SCOPE. A paid feat-copy cast under FS-08 is an independent feat-casting route for strain purposes. Use FS-09 exactly: base Dissonance 0 for q/rank 0, 1 for ranks 1-5, and 2 for ranks 6-9; apply ordinary same-family Refrain using CRS-01; and use `Limit = max(4, 2*PB + casting modifier)` for that copy route, including its existing surcharge/block thresholds. The owned route chosen to qualify the copy supplies only the permitted casting ability, rank ceiling and other expressly required source credentials; it does not import that class engine's protected Dissonance reduction, routing, vent, prepared-matrix treatment or proc chain into the feat-copy cast. In particular a Wizard-qualified copy is not a prepared matrix, a Shaman-qualified copy is not an ordinary Shaman spell for the totem vent, and a Mirrorsage-qualified copy is not class Echo Release. The ordinary `max(4, 2 + PB + max(0, modifier))` Limit in SPELL_INTEGRATION_RULES remains controlling for ordinary class spells within its existing scope and is not globally changed here. If the only qualifying route is the feat-only Eldritch Blast grant, it supplies CHA and only its actual rank-0 ceiling; it does not change the copy engine or Limit, create a Warlock/class engine, or qualify a ranked q>0 copy.

COPY-READY-ALLOWANCE-02 — owner-directed preparation-round-only successor for the seven FS-08/SUP-07 feat-copy profiles used through Arcane Adaptation, Eldritch Echo and Mimicry. This supersedes COPY-READY-ALLOWANCE-01's both-touched-round policy only. All earlier archives and receipts retain their exact historical wording. This selection changes no profile payload, acquisition predicate, ordinary Ready rule, ordinary class casting cadence or unrelated Mirrorsage class Echo procedure.

PREPARATION. The shared feat-copy cap counts new paid feat-copy casting commitments: a direct cast commits in its current numbered round; a Readied feat copy commits in its preparation numbered round. Require and atomically spend that round's owner feat-copy allowance. If the owner actually has the separately acquired Mirrorsage shared-release engine to which the exact source binds this feat copy, also require and spend that same preparation round's actual shared class allowance. A qualifying ability route alone never creates that engine. Validate the actual setup prerequisites first. At legal preparation commitment, pay the Action, current quote and other actual costs, consume the applicable permission/use once, provide components, record the independent feat-copy family/Dissonance/Refrain once, and establish the one Ready concentration burden before its single preparation counter window. No partial class/feat/resource debit is allowed. Countering, abandonment, replacement, expiry or concentration loss after commitment never refunds those preparation spends, recreates a capture, restores displaced concentration or reopens that round's allowance. Failed precommit validation spends nothing and cannot delete an existing valid hold.

HELD RECORD. Bind one unique preparation ID and actual owner to its fixed captured source/profile/q/mode, preparation-bound choices, paid transaction, consumed permission receipt, preparation round and actual ledger identities. Preserve its original Ready deadline and every independently applicable earlier source/capture/use deadline. Consuming the capture permission at preparation is not itself loss of this paid hold's authorization, but the hold cannot extend the original permission window. No future round's allowance is reserved. The hold remains subject to ordinary concentration, body/source availability and valid replacement rules. Paid preparation alone creates no payload. Earlier prose calling the limit one-copy-release per round is controlled here: it limits new direct casts and Ready preparations, not a later completion of this same paid hold.

RELEASE. After an actual perceivable trigger has completed and before every governing deadline, validate the actual hold and its preparation receipts, the available lawful Reaction, continuing concentration and the release predicates at the points required by their actual sources. Select legal current targets/ordered recipients/area/destination at release under the fixed preparation profile and mode; do not freeze a setup-time ghost target or rewrite preparation-bound choices from hidden results. Neither same-round nor later-round release checks, reserves or spends a new feat-copy allowance or a new Mirrorsage shared-release allowance. The preparation receipts remain spent in their original round. An otherwise lawful delayed release therefore remains eligible even when the release round's feat allowance, an actually owned class shared allowance, or both have already been spent by another lawful use. This exemption belongs only to completion of that specific paid feat-copy hold; it does not waive any new direct cast's or unrelated class Echo's own allowances.

A declined trigger or an invalid precommit release, including no actual Reaction, invalid target/geometry, missing source predicate or uncompleted/unperceived trigger, spends no Reaction, makes no new debit and grants no hidden diagnostic. Keep the existing hold only while its actual concentration and original deadlines permit; another genuine trigger occurrence may be considered. An already-spent release-round copy allowance alone is NOT a failed-release reason. At an exact governing expiry, expiry wins. Lost concentration, actual abandonment, successful replacement or another real ending terminates the hold without a refund; a failed release cannot restore a hold that ended.

On a valid release commitment, atomically consume this hold once and spend the real Reaction before resolving its one payload. No second RP/material payment, capture-use consumption, casting-family/Refrain update, cast hook or Counterspell window occurs. Subsequent prevention or a failed attack/save outcome does not refund the Reaction or preparation; actual source-specific hidden-eligibility checks retain their own paid timing. Duplicate callbacks/retry IDs cannot create a second payload or debit. Immediate Strike/Burst/Mend/Step end the held concentration after resolution. Ward/Hindrance/Boon continue the same one burden under their actual effect clock and earlier limits, never a second concentration slot.

OTHER USES AND PERSISTENCE. Another copy in the release round still needs its own genuinely available Action/source permission, current legal resources/credentials, its own new-commitment allowances and all ordinary concentration/cadence predicates. No Action, Reaction refresh, capture or second concentration slot is granted. A concentration-breaking new cast can end the old hold even though its allowance is irrelevant to the old release. Releasing a prior hold first leaves a genuinely free current-round allowance available for a separate lawful new commitment; a lawful prior current-round use does not by itself block the old hold's release. Actual competing-use opportunities before the owner's next regular START are illustrative prerequisites unless supplied by a real source; the old Ready cannot be carried past that START merely to obtain the ordinary Action. Save/load, extra turns, changing routes/profiles or round labels must preserve owner/hold identity, original expiry, actual consumed receipts, completed release identity and chronological/per-round ledgers. Release never rewrites a later cast's history. This rule is a proposed authoring successor, not implementation of scheduling, live perception, source-qualified recipient effects, canonical persistence or the game engine.

### Original-position authored review references

```json
[
  {
    "id": "MX-38-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/34"
  },
  {
    "id": "MX-38-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/35"
  }
]
```

## MX-39 — Arcane Calculus

### Complete original object

```json
{
  "id": "arcane_calculus",
  "name": "Arcane Calculus",
  "description": "You solve combat like an equation—measuring intervals, vectors, and the precise moment a spell must land. Prestige lineage: Chronomancer. completed from the existing development record.)",
  "prerequisite": "Intelligence 15+, proficiency in Arcana",
  "effect": "You gain +2 to initiative while concentrating on a spell. Once per short rest, you may store one prepared spell's timing: cast it on a later turn without using an action, as if you had readied it mathematically. When you cast a stored spell this way, one creature of your choice within 30 feet must succeed on a Dexterity save or take force damage equal to your spellcasting modifier (minimum 1).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You gain +2 to initiative while concentrating on a spell. Once per short rest, you may store one prepared spell's timing: cast it on a later turn without using an action, as if you had readied it mathematically. When you cast a stored spell this way, one creature of your choice within 30 feet must succeed on a Dexterity save or take force damage equal to your spellcasting modifier (minimum 1).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind+2 initiative only while actually concentrating, timing of the check and later loss. Define storing one prepared spell, setup action/RP/components/concentration, lifetime, free release on a later turn, counterability and legal targets. Define the separate30ft Dexterity-save force rider/DC/one spellcasting modifier and no action-generation loop."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcane_calculus",
  "name": "Arcane Calculus",
  "cohort": "magic_extended",
  "questionId": "MX-39",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/38",
  "originalQuestion": "Bind+2 initiative only while actually concentrating, timing of the check and later loss. Define storing one prepared spell, setup action/RP/components/concentration, lifetime, free release on a later turn, counterability and legal targets. Define the separate30ft Dexterity-save force rider/DC/one spellcasting modifier and no action-generation loop.",
  "originalSourceObject": {
    "id": "arcane_calculus",
    "name": "Arcane Calculus",
    "description": "You solve combat like an equation—measuring intervals, vectors, and the precise moment a spell must land. Prestige lineage: Chronomancer. completed from the existing development record.)",
    "prerequisite": "Intelligence 15+, proficiency in Arcana",
    "effect": "You gain +2 to initiative while concentrating on a spell. Once per short rest, you may store one prepared spell's timing: cast it on a later turn without using an action, as if you had readied it mathematically. When you cast a stored spell this way, one creature of your choice within 30 feet must succeed on a Dexterity save or take force damage equal to your spellcasting modifier (minimum 1).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You gain +2 to initiative while concentrating on a spell. Once per short rest, you may store one prepared spell's timing: cast it on a later turn without using an action, as if you had readied it mathematically. When you cast a stored spell this way, one creature of your choice within 30 feet must succeed on a Dexterity save or take force damage equal to your spellcasting modifier (minimum 1).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "267a418aa2a83fb5c330ce4bc822bab28ee7b20a32fd7ba752ef9471bb25e72d",
  "submittedProcedure": "Gain+2 to an actual initiative roll only while concentrating on a spell when that roll occurs; losing concentration later does not rewrite initiative. Once SR/LR use an Action to prepare one currently legally prepared normalActionspell through the exact Ready casting procedure, paying costs/components/history and opening interruption at preparation. NEW it shares the one pendingReady slot and concentration requirement, but its hold lasts through your next future regular end, and release is a voluntary non-action on that next regular turn only. Choose/recheck original legal targets then; no Reaction or second cast. Expiry, replacement or lostconcentration wastes paid costs. On successful release, choose one perceived creature within 30 ft of your body and line of effect:DEX save against the stored cast’s actual DC or take force equal to max(1, its actual casting modifier snapshotted at preparation),0 on success. One immediate noncopyable feat rider, no added release/action/castproc. Readied spells lacking a preparation route remain ineligible; the feat grants no preparation list.",
  "submittedNewChoices": "Action/cost-paid extendedReady with next-regular-turn free release and one finite DC-bound rider.",
  "submittedWorkedCases": [
    "Prepare a legal spell now, then release next regular turn without spendingAction; one nearby creature may face the separateDEXsave.",
    "A Counterspell at preparation prevents storage and the later rider; there is no second Counterspell window at release."
  ],
  "decision": "Adopt the explicit next-own-regular-turn non-Action Ready release extension, maintaining one Ready/concentration slot, original price/history and shared free-release cap.",
  "completeAuthoringProcedure": "Gain+2 to an actual initiative roll only while concentrating on a spell when that roll occurs; losing concentration later does not rewrite initiative. Once SR/LR use an Action to prepare one currently legally prepared normalActionspell through the exact Ready casting procedure, paying costs/components/history and opening interruption at preparation. NEW it shares the one pendingReady slot and concentration requirement, but its hold lasts through your next future regular end, and release is a voluntary non-action on that next regular turn only. Choose/recheck original legal targets then; no Reaction or second cast. Expiry, replacement or lostconcentration wastes paid costs. On successful release, choose one perceived creature within 30 ft of your body and line of effect:DEX save against the stored cast’s actual DC or take force equal to max(1, its actual casting modifier snapshotted at preparation),0 on success. One immediate noncopyable feat rider, no added release/action/castproc. Readied spells lacking a preparation route remain ineligible; the feat grants no preparation list.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Prepare a legal spell now, then release next regular turn without spendingAction; one nearby creature may face the separateDEXsave.",
    "A Counterspell at preparation prevents storage and the later rider; there is no second Counterspell window at release."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Gain+2 to an actual initiative roll only while concentrating on a spell when that roll occurs; losing concentration later does not rewrite initiative. Once SR/LR use an Action to prepare one currently legally prepared normalActionspell through the exact Ready casting procedure, paying costs/components/history and opening interruption at preparation. NEW it shares the one pendingReady slot and concentration requirement, but its hold lasts through your next future regular end, and release is a voluntary non-action on that next regular turn only. Choose/recheck original legal targets then; no Reaction or second cast. Expiry, replacement or lostconcentration wastes paid costs. On successful release, choose one perceived creature within 30 ft of your body and line of effect:DEX save against the stored cast’s actual DC or take force equal to max(1, its actual casting modifier snapshotted at preparation),0 on success. One immediate noncopyable feat rider, no added release/action/castproc. Readied spells lacking a preparation route remain ineligible; the feat grants no preparation list.

### Original-position authored review references

```json
[
  {
    "id": "MX-39-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/36"
  },
  {
    "id": "MX-39-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/37"
  }
]
```

## MX-40 — Arcane Momentum

### Complete original object

```json
{
  "id": "arcane_momentum",
  "name": "Arcane Momentum",
  "description": "Each sword stroke feeds your spellcraft. In Aethel's battlefields, steel and sigil are one rhythm. Prestige lineage: Battlemage. completed from the existing development record.)",
  "prerequisite": "Power Attack or Combat Casting, spellcasting ability",
  "effect": "When you hit with a melee weapon attack, gain 1 Momentum stack (max 3). Spend 1 stack to reduce the casting time of your next spell by one step, or spend all stacks to add +10% force damage per stack to a spell you cast before the end of your turn.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you hit with a melee weapon attack, gain 1 Momentum stack (max 3). Spend 1 stack to reduce the casting time of your next spell by one step, or spend all stacks to add +10% force damage per stack to a spell you cast before the end of your turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve actual Power Attack OR Combat Casting prerequisites. Define melee-hit stack gain, maximum3, lifetime/reset, per-hit cadence and one-step casting-time ladder. Separately define spending all stacks for+10percent force damage per stack: base, packet/area/critical rounding, duration and whether damage is added or converted. No arbitrary free cast or imported class Momentum pool."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcane_momentum",
  "name": "Arcane Momentum",
  "cohort": "magic_extended",
  "questionId": "MX-40",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/39",
  "originalQuestion": "Resolve actual Power Attack OR Combat Casting prerequisites. Define melee-hit stack gain, maximum3, lifetime/reset, per-hit cadence and one-step casting-time ladder. Separately define spending all stacks for+10percent force damage per stack: base, packet/area/critical rounding, duration and whether damage is added or converted. No arbitrary free cast or imported class Momentum pool.",
  "originalSourceObject": {
    "id": "arcane_momentum",
    "name": "Arcane Momentum",
    "description": "Each sword stroke feeds your spellcraft. In Aethel's battlefields, steel and sigil are one rhythm. Prestige lineage: Battlemage. completed from the existing development record.)",
    "prerequisite": "Power Attack or Combat Casting, spellcasting ability",
    "effect": "When you hit with a melee weapon attack, gain 1 Momentum stack (max 3). Spend 1 stack to reduce the casting time of your next spell by one step, or spend all stacks to add +10% force damage per stack to a spell you cast before the end of your turn.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you hit with a melee weapon attack, gain 1 Momentum stack (max 3). Spend 1 stack to reduce the casting time of your next spell by one step, or spend all stacks to add +10% force damage per stack to a spell you cast before the end of your turn.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "eca5bfe0bf65522633848224b69072f0448e796a413fd4c7ff96e6a2245d51bf",
  "submittedProcedure": "Require actual Power Attack OR Combat Casting plus actual spellcasting ability. NEW each personal direct melee-weapon hit against meaningful opposition gives one featMomentum, max 3, with a once-per-attack identity and no gain from copies/companions/retaliation. This separate pool starts 0, ends at encounter end or one minute without a qualifying hostile hit; no alias to any class Momentum. At spell declaration choose ONE mode. Spend 1 to shorten a printed normalActionspell to BA; no other casting time has a shorter step in this explicit finite ladder, so no BA-to-free, Reaction-to-Action or ritual compression. OR spend all current 1–3 stacks to add floor(native immediate damage×stacks/10) as force to one selected native packet/shared area roll before this actual turn ends, after native critical/flat formula but before defenses. It adds damage rather than converts the original type, and does not compound other percentage bonuses. No damage means 0, no future periodic/ray replication; a miss/counter wastes stacks. Cannot combine both modes on one cast or bank the declared enhancement for a later turn.",
  "submittedNewChoices": "Distinct finite pool/lifetime, singleAction-to BA ladder and one pre-defense additiveforce component.",
  "submittedWorkedCases": [
    "Native 19 damage with 3 stacks adds 5 force; native damage keeps its original type.",
    "A printedBAspell cannot be made free by spending a stack."
  ],
  "decision": "Adopt separate finite3-stack melee momentum, not Dragoon Momentum; spend on one legal Action conversion or separately floored native damage rider, never both.",
  "completeAuthoringProcedure": "Require actual Power Attack OR Combat Casting plus actual spellcasting ability. NEW each personal direct melee-weapon hit against meaningful opposition gives one featMomentum, max 3, with a once-per-attack identity and no gain from copies/companions/retaliation. This separate pool starts 0, ends at encounter end or one minute without a qualifying hostile hit; no alias to any class Momentum. At spell declaration choose ONE mode. Spend 1 to shorten a printed normalActionspell to BA; no other casting time has a shorter step in this explicit finite ladder, so no BA-to-free, Reaction-to-Action or ritual compression. OR spend all current 1–3 stacks to add floor(native immediate damage×stacks/10) as force to one selected native packet/shared area roll before this actual turn ends, after native critical/flat formula but before defenses. It adds damage rather than converts the original type, and does not compound other percentage bonuses. No damage means 0, no future periodic/ray replication; a miss/counter wastes stacks. Cannot combine both modes on one cast or bank the declared enhancement for a later turn.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Native 19 damage with 3 stacks adds 5 force; native damage keeps its original type.",
    "A printedBAspell cannot be made free by spending a stack."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Power Attack OR Combat Casting plus actual spellcasting ability. NEW each personal direct melee-weapon hit against meaningful opposition gives one featMomentum, max 3, with a once-per-attack identity and no gain from copies/companions/retaliation. This separate pool starts 0, ends at encounter end or one minute without a qualifying hostile hit; no alias to any class Momentum. At spell declaration choose ONE mode. Spend 1 to shorten a printed normalActionspell to BA; no other casting time has a shorter step in this explicit finite ladder, so no BA-to-free, Reaction-to-Action or ritual compression. OR spend all current 1–3 stacks to add floor(native immediate damage×stacks/10) as force to one selected native packet/shared area roll before this actual turn ends, after native critical/flat formula but before defenses. It adds damage rather than converts the original type, and does not compound other percentage bonuses. No damage means 0, no future periodic/ray replication; a miss/counter wastes stacks. Cannot combine both modes on one cast or bank the declared enhancement for a later turn.

### Original-position authored review references

```json
[
  {
    "id": "MX-40-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/38"
  },
  {
    "id": "MX-40-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json",
      "bytes": 728843,
      "sha256": "6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4"
    },
    "pointer": "/originalCaseReviews/39"
  }
]
```

## MX-41 — Conjure Flora

### Complete original object

```json
{
  "id": "conjure_flora",
  "name": "Conjure Flora",
  "description": "Seeds answer your call, rooting as guardians, lashing as spears, blooming as verdict. Prestige lineage: Verdant Animist. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, proficiency in Nature",
  "effect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve lash, spores and10ft-square entangle modes, one seedling/second atlevel10 and all-seedling Bonus Action command. Define creation action, separate Short Rest use and capacity, one-minute expiry, HP/AC/size/placement, each mode stats/save/DC, targets and shared damage-command cap. No unbounded seed, loot, independent turn or cosmology inference from plant spirit."
```

### Preserved original source direction (historical)

```json
{
  "featId": "conjure_flora",
  "name": "Conjure Flora",
  "cohort": "magic_extended",
  "questionId": "MX-41",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/40",
  "originalQuestion": "Preserve lash, spores and10ft-square entangle modes, one seedling/second atlevel10 and all-seedling Bonus Action command. Define creation action, separate Short Rest use and capacity, one-minute expiry, HP/AC/size/placement, each mode stats/save/DC, targets and shared damage-command cap. No unbounded seed, loot, independent turn or cosmology inference from plant spirit.",
  "originalSourceObject": {
    "id": "conjure_flora",
    "name": "Conjure Flora",
    "description": "Seeds answer your call, rooting as guardians, lashing as spears, blooming as verdict. Prestige lineage: Verdant Animist. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability, proficiency in Nature",
    "effect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "808a209ce707a2ec064754fa08fac439570e76406bec62b4632950d324e46bd2",
  "submittedProcedure": "Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW to make the second-capacity clause usable, at level 10 this same committed use permits one additional Action before the first plant expires to create one second plant; no second rest use, no later replacement of that spent creation. This is an explicit proposed addition to the printed one-seedling creation, not a recovered rule. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.",
  "submittedNewChoices": "Explicit NEW second Action at level 10 reconciles otherwise unusable capacity with once-rest creation; full bodies/modes and one coordinated offense.",
  "submittedWorkedCases": [
    "Two active plants can extend where the single 1d6 lash originates; they do not produce 2d6 or two attacks.",
    "At level 10, a second Action during the first plant’s lifetime can consume the one proposed additional-creation entitlement; it does not allow repeated replacement plants."
  ],
  "decision": "Adopt three closed finite plant profiles with actual attached command phases and capacity/creation entitlements; no anonymous autonomous attack, corpse, harvest or class minion grant.",
  "completeAuthoringProcedure": "Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW to make the second-capacity clause usable, at level 10 this same committed use permits one additional Action before the first plant expires to create one second plant; no second rest use, no later replacement of that spent creation. This is an explicit proposed addition to the printed one-seedling creation, not a recovered rule. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.\nNEW ordinary command scheduling: each plant has one attached phase immediately after its owner’s regular turn, not an independent initiative turn. Its ordinary commanded action requires the owner’s shared Bonus Action within60ft through the specified perceivable command channel and spends the one offensive companion allowance per owner per numbered round if offensive. With no legal command it has no autonomous attack. Trapcasting’s explicitly adopted entry-trigger or burst is a separate narrow exception spending that same shared offensive allowance, never another free attack.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Two active plants can extend where the single 1d6 lash originates; they do not produce 2d6 or two attacks.",
    "At level 10, a second Action during the first plant’s lifetime can consume the one proposed additional-creation entitlement; it does not allow repeated replacement plants."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW second-capacity permission is the single original-use window defined by FLQ-02–03 below; it costs another Action, not another rest use. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.
FEAT335-FLORA-SOURCE-CHECK-01 / FLQ-04 — NEW split command/phase completion. On the owner's regular turn, first establish a legal shared Bonus Action, an available owner/numbered-round offensive-companion allowance, and actual receipt of the required within-60-ft audible or visible command by each nominated participating plant. At that legal commitment spend the Bonus Action and that one shared offensive allowance once; record the owner, original regular-turn/round identity, participating plant IDs, one chosen mode and target or area, its permitted origin or nominated Lash origins, and the immediately following attached phase. This is a paid pending command, not a Readied action, independent plant turn or extra allowance. It need not be the owner's last voluntary decision that turn. Resolve it once in the attached phase after that same regular turn's actual end processing, using the preserved schedule; an extra turn neither advances nor duplicates that phase. Recheck the surviving unended, unsuppressed, otherwise capable participating plant and the mode's actual target/area, range, perception and line-of-effect requirements. For Lash, an independently legal surviving nominated origin may support the same selected target; losing the selected Spore/Entangle origin does not authorize another origin or mode. For an area, resolve its actual occupants at that phase. If the chosen outcome is no longer legal, close the pending command with no effect, no refund, no new target and no carry to a later phase. After actual receipt, later owner incapacity, Silence, loss of owner-to-plant sight/range/channel, or owner death alone does not retract that command: no continuous concentration/channel/consciousness requirement is added. These states can prevent a NEW command or personal creation/Bloom Burst. An effect expressly cancelling the pending command or disabling/ending its plant still controls. Once committed, no other companion or armed trap can spend the same owner-round allowance, and the phase does not spend it a second time.
KEEP the already-operative SUP-07 floraBody/dc acquisition requirement: at acquisition permanently select and record one actual possessed spellcasting route as this feat's DC provider. Use DC 8 + current PB + that route's current casting-ability modifier; do not invent Wisdom, Spellcraft or another default. This source choice is separate from the later seedling mode/burst-type choice. Ownership initializes only the finite creation allowance and body capacity, with no plant, pending additional creation, command or active effect. All printed acquisition predicates and the actual earned feat opportunity remain required.
FEAT335-FLORA-SOURCE-CHECK-01 / FLQ-01 — KEEP acquisition-only provider selection. A valid paid Conjure Flora acquisition permanently binds its actual qualifying personal casting route and the ability operand supplied by that route. Later loss, expiry, retraining-away or temporary unavailability of that casting grant does not by itself remove Conjure Flora, reselect its provider, prohibit an otherwise legal Flora creation/command/Bloom Burst, terminate an existing seedling or disable an already armed entry trap. Current prepared repertoire, renewable casting charges and RP are not new ongoing Flora prerequisites. This does not qualify a NEW feat acquisition through a grant that is actually gone; ACQ-03 still governs that separate snapshot. Flora is a magical nonspell feat, not a cast through the provider: a spell-only prohibition applies only to its actual scope, Silence still blocks an audible command, and an effect actually suppressing this feat, a plant, its magic or the required action applies under that effect's own rule. NEW explicit lost-provider representation: retain the original provider/ability binding and compute Flora DC as 8 + the owner's current lawful PB + the current modifier of that bound ability; no alternative route, Wisdom default, reconstructed casting entitlement or favorable old ability score is substituted. A missing or invalid original acquisition/provider record is not cured by this rule. Completed results are not recalculated, and existing body HP/save snapshots, deadlines, spent uses and ownership are not reset.
FEAT335-FLORA-SOURCE-CHECK-01 / FLQ-02–03 — NEW second-creation window completion. Each legally completed first creation records one original use ID, its first-plant ID and that plant's original minute deadline, with at most one additional creation unspent. This is a bounded open-use record even when the owner is below total level 10; it is not another rest use or an immediately usable creation at that level. Admit a second creation only while that same first plant remains present and unended, before its original deadline, with the additional creation unspent, current total character level at least 10, actual free plant capacity, and every ordinary Action, ground, range, line-of-effect and use predicate satisfied. The level-10 condition is live at the additional Action, not snapshotted at first creation. Genuine advancement during that open window can make the existing unspent permission usable, but creates no body, charge, healing or new window. Destruction, uprooting, Bloom Burst consumption, expiry or another actual ending of the first plant permanently closes any unused additional-creation permission immediately; its old future deadline does not keep that permission alive. Suppression without an actual ending is not by itself an ending. A legal additional creation consumes that one permission and costs its own Action, but no second rest use; its own minute begins at its own creation. Once the second plant exists, ending the first does not shorten the second's independent deadline. No ended plant, spent permission, missed deadline, level change, recovery, new ID or subsequent body can reopen the old use. A later beneficial rest restores only the ordinary creation allowance under FS-06; a later first creation starts a genuinely new use.
FEAT335-FLORA-SOURCE-CHECK-01 / FLQ-04 — NEW explicit owner/instance continuity. These particular one-minute, nonconcentration Flora bodies do not end merely because their owner is incapacitated or dies; retain the same owner, mode, actual body state, original deadline and no-resource restrictions. No recipient, ally, host, companion or replacement actor inherits control. A received pending command may resolve only at its already attached original phase under the split-command rule, even if the owner's live initiative slot is removed; preserve that one scheduled phase, not a new recurring independent turn. An already armed Trapcasting plant may perform its specified first-eligible-entry exception without a new owner Action/Reaction or remote command channel, even while its owner cannot act or is dead, but it still needs the actual qualifying entry, operative plant/trap, target legality and unspent same-owner numbered-round allowance. Incapacity/death neither refreshes that allowance nor rearms or moves the trap. Preserve the owner's last lawful PB/selected-ability state when its live actor view ends, applying any subsequently due source-defined changes; death is not a zero ability score, a new provider or a freeze of expiring modifiers. Use that continuing lawful record for later Flora DCs; a missing authoritative operand is an invalid/unestablished input, not permission to invent one. Lawful recovery continues the same history without replaying missed phases or refilling anything. Ending a generating plant still ends its own Poisoned/Restrained records immediately. A legally committed Bloom Burst binds its existing DC/type/area event, consumes its body before its one payload, and does not fail merely because that required consumption has occurred; it grants no other action to the ended body. Other independently applicable cancellation, suppression, condition, duration and target rules retain their own actual scope. No Animal Companion release/death rule or standard-companion movement/Dodge/attack is imported into these fixed Flora profiles.

### Original-position authored review references

```json
[
  {
    "id": "MX-41-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/0"
  },
  {
    "id": "MX-41-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/1"
  }
]
```

## MX-42 — Curse Channeling

### Complete original object

```json
{
  "id": "curse_channeling",
  "name": "Curse Channeling",
  "description": "Doom flows through your blade like ink through water—every cut writes a sentence the target cannot unread. Prestige lineage: Hexblade. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability or proficiency in Arcana, level 6+",
  "effect": "When you hit a creature with a weapon attack, you can apply a Hex Mark. Marked creatures take +1d6 necrotic damage the next time they are hit before the start of your next turn. You can maintain one mark at a time; at level 10+, two. When a marked creature drops to 0 hit points, you regain 1d6 hit points or gain advantage on your next attack before the end of your next turn (your choice).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you hit a creature with a weapon attack, you can apply a Hex Mark. Marked creatures take +1d6 necrotic damage the next time they are hit before the start of your next turn. You can maintain one mark at a time; at level 10+, two. When a marked creature drops to 0 hit points, you regain 1d6 hit points or gain advantage on your next attack before the end of your next turn (your choice).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define optional Hex Mark application on a weapon hit, one/two capacity, expiry/replacement, next-hit+1d6 ownership and whether triggering hit qualifies. Resolve next-hit consumption versus later zeroHP benefit, which marked death/zeroHP event grants1d6 healing or next-attack advantage, true-healing gates and anti-farming. Keep unrelated generic Marked condition separate."
```

### Preserved original source direction (historical)

```json
{
  "featId": "curse_channeling",
  "name": "Curse Channeling",
  "cohort": "magic_extended",
  "questionId": "MX-42",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/41",
  "originalQuestion": "Define optional Hex Mark application on a weapon hit, one/two capacity, expiry/replacement, next-hit+1d6 ownership and whether triggering hit qualifies. Resolve next-hit consumption versus later zeroHP benefit, which marked death/zeroHP event grants1d6 healing or next-attack advantage, true-healing gates and anti-farming. Keep unrelated generic Marked condition separate.",
  "originalSourceObject": {
    "id": "curse_channeling",
    "name": "Curse Channeling",
    "description": "Doom flows through your blade like ink through water—every cut writes a sentence the target cannot unread. Prestige lineage: Hexblade. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability or proficiency in Arcana, level 6+",
    "effect": "When you hit a creature with a weapon attack, you can apply a Hex Mark. Marked creatures take +1d6 necrotic damage the next time they are hit before the start of your next turn. You can maintain one mark at a time; at level 10+, two. When a marked creature drops to 0 hit points, you regain 1d6 hit points or gain advantage on your next attack before the end of your next turn (your choice).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you hit a creature with a weapon attack, you can apply a Hex Mark. Marked creatures take +1d6 necrotic damage the next time they are hit before the start of your next turn. You can maintain one mark at a time; at level 10+, two. When a marked creature drops to 0 hit points, you regain 1d6 hit points or gain advantage on your next attack before the end of your next turn (your choice).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "2744aa959f867d419044ba0308e7179ed427c404668f3189023e61a4279c1443",
  "submittedProcedure": "Require character 6 plus actual spellcasting OR Arcana proficiency. After a personal direct weapon hit, optionally place oneHexMark on that creature; the triggering hit cannot consume it. Capacity 1, or 2 at total 10; new beyond cap replaces oldest. Each record expires at your next future regular start and has two distinct one-use riders. The next genuinely separate hit against that target adds 1d6 necrotic to that hit’s packet, critical-doubled if that hit truly crits, then consumes only the damage rider; attribution remains to your feat, not the attacker’s spell for proc purposes. While the record remains, the first drop from positiveHPto 0 by genuine hostile conflict lets you choose 1d6 ordinary self-healing or advantage on your next actual attack roll through next regular end. Commit that drop rider even if blocked/full HP; no floor-prevented drop, staged victims or repeated same-target cycling within the encounter. NEW one drop benefit per owner/target/encounter; healing is finite paid-feat trigger, no healing-copy/resource output or convertible excess. Mark ends early only on replacement/cure/source rule; separate source marks do not stack the same damage rider on one hit.",
  "submittedNewChoices": "Two independently consumed riders preserve the later drop benefit; one target/encounter recovery boundary.",
  "submittedWorkedCases": [
    "An ally’s later hit spends the mark’s 1d6, but a subsequent lawful drop before expiry can still grant the one self-heal.",
    "Your original marking hit supplies neither its own bonus die nor a drop reward if the target was already 0 before the mark existed."
  ],
  "decision": "Keep owned finite mark, later distinct hit rider and bounded actual positive-to-zero reward; actual death is not required and copying/refreshing cannot duplicate entitlements.",
  "completeAuthoringProcedure": "Require character 6 plus actual spellcasting OR Arcana proficiency. After a personal direct weapon hit, optionally place oneHexMark on that creature; the triggering hit cannot consume it. Capacity 1, or 2 at total 10; new beyond cap replaces oldest. Each record expires at your next future regular start and has two distinct one-use riders. The next genuinely separate hit against that target adds 1d6 necrotic to that hit’s packet, critical-doubled if that hit truly crits, then consumes only the damage rider; attribution remains to your feat, not the attacker’s spell for proc purposes. While the record remains, the first drop from positiveHPto 0 by genuine hostile conflict lets you choose 1d6 ordinary self-healing or advantage on your next actual attack roll through next regular end. Commit that drop rider even if blocked/full HP; no floor-prevented drop, staged victims or repeated same-target cycling within the encounter. NEW one drop benefit per owner/target/encounter; healing is finite paid-feat trigger, no healing-copy/resource output or convertible excess. Mark ends early only on replacement/cure/source rule; separate source marks do not stack the same damage rider on one hit.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An ally’s later hit spends the mark’s 1d6, but a subsequent lawful drop before expiry can still grant the one self-heal.",
    "Your original marking hit supplies neither its own bonus die nor a drop reward if the target was already 0 before the mark existed."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require character 6 plus actual spellcasting OR Arcana proficiency. After a personal direct weapon hit, optionally place oneHexMark on that creature; the triggering hit cannot consume it. Capacity 1, or 2 at total 10; new beyond cap replaces oldest. Each record expires at your next future regular start and has two distinct one-use riders. The next genuinely separate hit against that target adds 1d6 necrotic to that hit’s packet, critical-doubled if that hit truly crits, then consumes only the damage rider; attribution remains to your feat, not the attacker’s spell for proc purposes. While the record remains, the first drop from positiveHPto 0 by genuine hostile conflict lets you choose 1d6 ordinary self-healing or advantage on your next actual attack roll through next regular end. Commit that drop rider even if blocked/full HP; no floor-prevented drop, staged victims or repeated same-target cycling within the encounter. NEW one drop benefit per owner/target/encounter; healing is finite paid-feat trigger, no healing-copy/resource output or convertible excess. Mark ends early only on replacement/cure/source rule; separate source marks do not stack the same damage rider on one hit.

### Original-position authored review references

```json
[
  {
    "id": "MX-42-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/2"
  },
  {
    "id": "MX-42-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/3"
  }
]
```

## MX-43 — Curse Weaving

### Complete original object

```json
{
  "id": "curse_weaving",
  "name": "Curse Weaving",
  "description": "You knot malice into syllables, letting debuffs compound like threads pulled tight. Prestige lineage: Warlock. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, Charisma 13+",
  "effect": "When you cast a spell that forces a saving throw, you may weave a curse: on a failed save, the target suffers an additional escalating debuff each round (–1 to attacks, then –1 to saves, then disadvantage on concentration) until they succeed on a save at the end of their turn.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you cast a spell that forces a saving throw, you may weave a curse: on a failed save, the target suffers an additional escalating debuff each round (–1 to attacks, then –1 to saves, then disadvantage on concentration) until they succeed on a save at the end of their turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define optional curse on a failed save, eligible targets, per-cast use/cost/cadence and escalating components. Specify whether−1 attacks,−1 saves,concentration disadvantage accumulate, round/turn order, end-turn save ability/DC, maximum duration, independent spell end/cure/suppression and multiple applications. No indefinite undefined debuff ladder."
```

### Preserved original source direction (historical)

```json
{
  "featId": "curse_weaving",
  "name": "Curse Weaving",
  "cohort": "magic_extended",
  "questionId": "MX-43",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/42",
  "originalQuestion": "Define optional curse on a failed save, eligible targets, per-cast use/cost/cadence and escalating components. Specify whether−1 attacks,−1 saves,concentration disadvantage accumulate, round/turn order, end-turn save ability/DC, maximum duration, independent spell end/cure/suppression and multiple applications. No indefinite undefined debuff ladder.",
  "originalSourceObject": {
    "id": "curse_weaving",
    "name": "Curse Weaving",
    "description": "You knot malice into syllables, letting debuffs compound like threads pulled tight. Prestige lineage: Warlock. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability, Charisma 13+",
    "effect": "When you cast a spell that forces a saving throw, you may weave a curse: on a failed save, the target suffers an additional escalating debuff each round (–1 to attacks, then –1 to saves, then disadvantage on concentration) until they succeed on a save at the end of their turn.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you cast a spell that forces a saving throw, you may weave a curse: on a failed save, the target suffers an additional escalating debuff each round (–1 to attacks, then –1 to saves, then disadvantage on concentration) until they succeed on a save at the end of their turn.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "e9c892ae4ee37ad28015f0b47a0670ff04a3ea228f39d8199c9ce4d464404b50",
  "submittedProcedure": "At a personal actual spell declaration that forces an initial save, select at most one original creature recipient for this NEW curse rider. Once per owner/target/numbered round, if it fails that actual initial save, establish an inflicted removablemagicalcurse with that save’s ability/DC and maximum one minute. Tier/rank for an actual rank-limited cure is the generating cast’s rank. Immediate stage 1 is−1 attack rolls; at the target’s next future regular start add stage 2−1 saves; at its following regular start add stage 3 disadvantage on actual concentration saves. Cap at 3; components accumulate within this record, not as repeated−1 stacks. At every affected regular end, including a current turn where applicable, repeat the original save; success ends the record. Original spell concentration loss/termination ends this attached curse; instantaneous spells leave its bounded independent minute. Suppression preserves stage clock and legal cures/saves without backlogged effects. Reapplication does not reset stage/extend beyond the later legal deadline or duplicate magnitude; different sources retain identity but same penalties use strongest. No forcedAction, deniedturn or hidden perpetual escalation.",
  "submittedNewChoices": "One chosen recipient, explicit three-stage removablecurse and repeated actual source save with minute cap.",
  "submittedWorkedCases": [
    "Failing initialWISsave gives−1 attacks; next regular start adds−1 saves, then the regular-endWISsave can end both.",
    "A second copy of the same stage cannot create−2 attacks or a fourth escalation."
  ],
  "decision": "Adopt explicit staged curse clocks and saves; same target/source refresh preserves stage and one magnitude, no reset farming or automatic parent spell promotion.",
  "completeAuthoringProcedure": "At a personal actual spell declaration that forces an initial save, select at most one original creature recipient for this NEW curse rider. Once per owner/target/numbered round, if it fails that actual initial save, establish an inflicted removablemagicalcurse with that save’s ability/DC and maximum one minute. Tier/rank for an actual rank-limited cure is the generating cast’s rank. Immediate stage 1 is−1 attack rolls; at the target’s next future regular start add stage 2−1 saves; at its following regular start add stage 3 disadvantage on actual concentration saves. Cap at 3; components accumulate within this record, not as repeated−1 stacks. At every affected regular end, including a current turn where applicable, repeat the original save; success ends the record. Original spell concentration loss/termination ends this attached curse; instantaneous spells leave its bounded independent minute. Suppression preserves stage clock and legal cures/saves without backlogged effects. Reapplication does not reset stage/extend beyond the later legal deadline or duplicate magnitude; different sources retain identity but same penalties use strongest. No forcedAction, deniedturn or hidden perpetual escalation.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Failing initialWISsave gives−1 attacks; next regular start adds−1 saves, then the regular-endWISsave can end both.",
    "A second copy of the same stage cannot create−2 attacks or a fourth escalation."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At a personal actual spell declaration that forces an initial save, select at most one original creature recipient for this NEW curse rider. Once per owner/target/numbered round, if it fails that actual initial save, establish an inflicted removablemagicalcurse with that save’s ability/DC and maximum one minute. Tier/rank for an actual rank-limited cure is the generating cast’s rank. Immediate stage 1 is−1 attack rolls; at the target’s next future regular start add stage 2−1 saves; at its following regular start add stage 3 disadvantage on actual concentration saves. Cap at 3; components accumulate within this record, not as repeated−1 stacks. At every affected regular end, including a current turn where applicable, repeat the original save; success ends the record. Original spell concentration loss/termination ends this attached curse; instantaneous spells leave its bounded independent minute. Suppression preserves stage clock and legal cures/saves without backlogged effects. Reapplication does not reset stage/extend beyond the later legal deadline or duplicate magnitude; different sources retain identity but same penalties use strongest. No forcedAction, deniedturn or hidden perpetual escalation.

### Original-position authored review references

```json
[
  {
    "id": "MX-43-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/4"
  },
  {
    "id": "MX-43-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/5"
  }
]
```

## MX-44 — Dark Affinity

### Complete original object

```json
{
  "id": "dark_affinity",
  "name": "Dark Affinity",
  "description": "Shadow clings to you willingly. The night recognizes its own. Prestige lineage: Bloodbound. completed from the existing development record.)",
  "prerequisite": "Charisma 13+",
  "effect": "You have resistance to necrotic damage, darkvision out to 60 feet (or +30 feet if you already have it), and advantage on saving throws against charm effects from undead creatures. While in dim light or darkness, you have advantage on Stealth checks and once per short rest you may step into shadow as a bonus action, teleporting up to 15 feet to an unoccupied space you can see that is also in dim light or darkness.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You have resistance to necrotic damage, darkvision out to 60 feet (or +30 feet if you already have it), and advantage on saving throws against charm effects from undead creatures. While in dim light or darkness, you have advantage on Stealth checks and once per short rest you may step into shadow as a bonus action, teleporting up to 15 feet to an unoccupied space you can see that is also in dim light or darkness.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Retain necrotic resistance,60ft darkvision or+30ft extension, undead-charm save advantage, dim/dark Stealth advantage and15ft Bonus Action shadow teleport once per Short Rest. Define actual light/sight/space/line, legal hiding, source-undead/charm predicate and darkvision stacking. No invisibility, creature conversion or soul/origin inference."
```

### Preserved original source direction (historical)

```json
{
  "featId": "dark_affinity",
  "name": "Dark Affinity",
  "cohort": "magic_extended",
  "questionId": "MX-44",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/43",
  "originalQuestion": "Retain necrotic resistance,60ft darkvision or+30ft extension, undead-charm save advantage, dim/dark Stealth advantage and15ft Bonus Action shadow teleport once per Short Rest. Define actual light/sight/space/line, legal hiding, source-undead/charm predicate and darkvision stacking. No invisibility, creature conversion or soul/origin inference.",
  "originalSourceObject": {
    "id": "dark_affinity",
    "name": "Dark Affinity",
    "description": "Shadow clings to you willingly. The night recognizes its own. Prestige lineage: Bloodbound. completed from the existing development record.)",
    "prerequisite": "Charisma 13+",
    "effect": "You have resistance to necrotic damage, darkvision out to 60 feet (or +30 feet if you already have it), and advantage on saving throws against charm effects from undead creatures. While in dim light or darkness, you have advantage on Stealth checks and once per short rest you may step into shadow as a bonus action, teleporting up to 15 feet to an unoccupied space you can see that is also in dim light or darkness.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You have resistance to necrotic damage, darkvision out to 60 feet (or +30 feet if you already have it), and advantage on saving throws against charm effects from undead creatures. While in dim light or darkness, you have advantage on Stealth checks and once per short rest you may step into shadow as a bonus action, teleporting up to 15 feet to an unoccupied space you can see that is also in dim light or darkness.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "08e8713f8fd48a01b90d63e3877abaa200781483e4ec364b0e9ed52345e34e9d",
  "submittedProcedure": "Gain necrotic resistance once and darkvision 60 ft, or add 30 ft to one actual independently granted darkvision range if already possessed; NEW compute from other valid sources without recursively counting this feat, reverting to 60 if that other source ends. It does not see through magicaldarkness unless separately allowed. Advantage applies to actual saves against a Charmed/explicitcharm component sourced by a creature actuallyUndead at application; no free type detection or general mind immunity. While your occupied space is actually dim/dark, gainStealthadvantage subject to ordinary hiding/perception; NEW whole footprint must qualify. Once SR/LR use BA from such a space to teleport up to 15 ft into an unoccupied fitting space you can see that is also dim/dark. No traversed path, but NEW line of effect to destination required; obey actual teleport/consent/restraint restrictions. Costs/use commit normally; no invisibility, freeHide, ancestry conversion or soul/origin claim.",
  "submittedNewChoices": "Nonrecursive darkvision extension, actual light/Undead predicates and bounded legal destination.",
  "submittedWorkedCases": [
    "Existing 60 ftdarkvision becomes 90 ft; Darkness that defeats that sense remains opaque.",
    "A lit destination cannot receive the shadow step even if it is within 15 ft."
  ],
  "decision": "Adopt necrotic resistance, actual Undead charm-save predicate and real dim-light step; correct darkvision to a fixed acquisition branch rather than a dynamic free fallback.",
  "completeAuthoringProcedure": "Gain necrotic resistance once. NEW darkvision branch is fixed at acquisition as specified below; an extension does not revert to a60ft base when its underlying source ends. It does not see through magicaldarkness unless separately allowed. Advantage applies to actual saves against a Charmed/explicitcharm component sourced by a creature actuallyUndead at application; no free type detection or general mind immunity. While your occupied space is actually dim/dark, gainStealthadvantage subject to ordinary hiding/perception; NEW whole footprint must qualify. Once SR/LR use BA from such a space to teleport up to 15 ft into an unoccupied fitting space you can see that is also dim/dark. No traversed path, but NEW line of effect to destination required; obey actual teleport/consent/restraint restrictions. Costs/use commit normally; no invisibility, freeHide, ancestry conversion or soul/origin claim.\nNEW exact darkvision branch, replacing any dynamic fallback reading: snapshot whether an independent darkvision source exists at acquisition. No source then gives a60ft base; an existing source then gives a+30ft extension to the current strongest independent operative range. Losing/suppressing every underlying source makes that extension inoperative, not a new60ft base. Record the branch permanently; unrelated future base ranges use normal strongest-base arbitration.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Existing 60 ftdarkvision becomes 90 ft; Darkness that defeats that sense remains opaque.",
    "A lit destination cannot receive the shadow step even if it is within 15 ft."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Gain necrotic resistance once. NEW darkvision branch is fixed at acquisition as specified below; an extension does not revert to a60ft base when its underlying source ends. It does not see through magicaldarkness unless separately allowed. Advantage applies to actual saves against a Charmed/explicitcharm component sourced by a creature actuallyUndead at application; no free type detection or general mind immunity. While your occupied space is actually dim/dark, gainStealthadvantage subject to ordinary hiding/perception; NEW whole footprint must qualify. Once SR/LR use BA from such a space to teleport up to 15 ft into an unoccupied fitting space you can see that is also dim/dark. No traversed path, but NEW line of effect to destination required; obey actual teleport/consent/restraint restrictions. Costs/use commit normally; no invisibility, freeHide, ancestry conversion or soul/origin claim.
NEW exact darkvision branch, replacing any dynamic fallback reading: snapshot whether an independent darkvision source exists at acquisition. No source then gives a60ft base; an existing source then gives a+30ft extension to the current strongest independent operative range. Losing/suppressing every underlying source makes that extension inoperative, not a new60ft base. Record the branch permanently; unrelated future base ranges use normal strongest-base arbitration.

### Original-position authored review references

```json
[
  {
    "id": "MX-44-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/6"
  },
  {
    "id": "MX-44-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/7"
  }
]
```

## MX-45 — Dark Binding

### Complete original object

```json
{
  "id": "dark_binding",
  "name": "Dark Binding",
  "description": "You and your cursed weapon share one hunger. Neither leaves the other's grasp easily. Prestige lineage: Hexblade. completed from the existing development record.)",
  "prerequisite": "Curse Channeling or level 8+",
  "effect": "You bind to one cursed weapon over a blood ritual (1 hour). While bound, the weapon cannot be disarmed against your will and deals an additional 1d4 necrotic damage on hit. If the weapon is destroyed, you take 2d10 psychic damage and cannot rebind until you complete a new ritual.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You bind to one cursed weapon over a blood ritual (1 hour). While bound, the weapon cannot be disarmed against your will and deals an additional 1d4 necrotic damage on hit. If the weapon is destroyed, you take 2d10 psychic damage and cannot rebind until you complete a new ritual.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve Curse Channeling OR level8 gate, one actual cursed weapon, one-hour ritual/tools/payment, rebind/unbind and original identity. Define cannot-be-disarmed versus forced dropping/incapacity, actual wielding+1d4 necrotic, thrown/ammunition/multi-hit limits and destruction2d10 psychic timing. This blood ritual is not automatically the reviewed Blood Ritual feat or free cursed-item creation."
```

### Preserved original source direction (historical)

```json
{
  "featId": "dark_binding",
  "name": "Dark Binding",
  "cohort": "magic_extended",
  "questionId": "MX-45",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/44",
  "originalQuestion": "Resolve Curse Channeling OR level8 gate, one actual cursed weapon, one-hour ritual/tools/payment, rebind/unbind and original identity. Define cannot-be-disarmed versus forced dropping/incapacity, actual wielding+1d4 necrotic, thrown/ammunition/multi-hit limits and destruction2d10 psychic timing. This blood ritual is not automatically the reviewed Blood Ritual feat or free cursed-item creation.",
  "originalSourceObject": {
    "id": "dark_binding",
    "name": "Dark Binding",
    "description": "You and your cursed weapon share one hunger. Neither leaves the other's grasp easily. Prestige lineage: Hexblade. completed from the existing development record.)",
    "prerequisite": "Curse Channeling or level 8+",
    "effect": "You bind to one cursed weapon over a blood ritual (1 hour). While bound, the weapon cannot be disarmed against your will and deals an additional 1d4 necrotic damage on hit. If the weapon is destroyed, you take 2d10 psychic damage and cannot rebind until you complete a new ritual.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You bind to one cursed weapon over a blood ritual (1 hour). While bound, the weapon cannot be disarmed against your will and deals an additional 1d4 necrotic damage on hit. If the weapon is destroyed, you take 2d10 psychic damage and cannot rebind until you complete a new ritual.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "88063512111fad301c6558490136a36443e55800d0b9cf608ff0e48e29fcde03",
  "submittedProcedure": "Require Curse Channeling OR character 8. Spend one uninterrupted hour in contact with one actual owned/willingly entrusted weapon carrying an established curse record; no feat-created curse, weapon or hidden curse diagnosis. NEW ritual needs your voluntary symbolic drop of blood but no numeric HP/material charge, and is unrelated to Blood Ritual. Completion replaces your old binding; interrupted work creates none and leaves the old. While personally wielding the bound original weapon, you cannot be involuntarily disarmed by an actual disarm effect; mandatory dropping from Unconscious/incapacity, loss of body/hand, voluntary release and physical destruction still apply. Each actual direct hit you make with that weapon adds 1d4 necrotic, critical-doubled normally. Thrown original weapon qualifies on its hit but does not return; ammunition launched by a bound bow qualifies as its weapon hit without becoming a bound item. No copying or companion use. Actual destruction ends the bond and causes one 2d10 psychic damage packet to you under ordinary defenses, at any distance; repair never rebinds. A fresh fullhour ritual is required for a new bond.",
  "submittedNewChoices": "Actual curseditem/onehour bond, exact disarm boundary and destruction once per original identity.",
  "submittedWorkedCases": [
    "An enemy disarm cannot take a consciously wielded bound sword; becomingUnconscious still drops it.",
    "Destroying a bound thrown weapon causes one 2d10 psychic packet, with ordinary psychic resistance if present."
  ],
  "decision": "Adopt finite real weapon ritual/bond and destruction consequence with continuing body/custody; not possession of a free cursed weapon, soul lore or refillable RP.",
  "completeAuthoringProcedure": "Require Curse Channeling OR character 8. Spend one uninterrupted hour in contact with one actual owned/willingly entrusted weapon carrying an established curse record; no feat-created curse, weapon or hidden curse diagnosis. NEW ritual needs your voluntary symbolic drop of blood but no numeric HP/material charge, and is unrelated to Blood Ritual. Completion replaces your old binding; interrupted work creates none and leaves the old. While personally wielding the bound original weapon, you cannot be involuntarily disarmed by an actual disarm effect; mandatory dropping from Unconscious/incapacity, loss of body/hand, voluntary release and physical destruction still apply. Each actual direct hit you make with that weapon adds 1d4 necrotic, critical-doubled normally. Thrown original weapon qualifies on its hit but does not return; ammunition launched by a bound bow qualifies as its weapon hit without becoming a bound item. No copying or companion use. Actual destruction ends the bond and causes one 2d10 psychic damage packet to you under ordinary defenses, at any distance; repair never rebinds. A fresh fullhour ritual is required for a new bond.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An enemy disarm cannot take a consciously wielded bound sword; becomingUnconscious still drops it.",
    "Destroying a bound thrown weapon causes one 2d10 psychic packet, with ordinary psychic resistance if present."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require Curse Channeling OR character 8. Spend one uninterrupted hour in contact with one actual owned/willingly entrusted weapon carrying an established curse record; no feat-created curse, weapon or hidden curse diagnosis. NEW ritual needs your voluntary symbolic drop of blood but no numeric HP/material charge, and is unrelated to Blood Ritual. Completion replaces your old binding; interrupted work creates none and leaves the old. While personally wielding the bound original weapon, you cannot be involuntarily disarmed by an actual disarm effect; mandatory dropping from Unconscious/incapacity, loss of body/hand, voluntary release and physical destruction still apply. Each actual direct hit you make with that weapon adds 1d4 necrotic, critical-doubled normally. Thrown original weapon qualifies on its hit but does not return; ammunition launched by a bound bow qualifies as its weapon hit without becoming a bound item. No copying or companion use. Actual destruction ends the bond and causes one 2d10 psychic damage packet to you under ordinary defenses, at any distance; repair never rebinds. A fresh fullhour ritual is required for a new bond.

### Original-position authored review references

```json
[
  {
    "id": "MX-45-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/8"
  },
  {
    "id": "MX-45-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/9"
  }
]
```

## MX-46 — Eldritch Echo

### Complete original object

```json
{
  "id": "eldritch_echo",
  "name": "Eldritch Echo",
  "description": "Your patron's voice returns through you, repeating power that was never meant for mortal throats. Prestige lineage: Warlock. completed from the existing development record.)",
  "prerequisite": "Forbidden Pact or spellcasting ability, level 3+",
  "effect": "You gain Eldritch Blast as a known cantrip if you do not already have it; it scales with your level. Once per short rest, when a creature within 60 feet casts a spell, you may echo a simplified version of that spell on your next turn (DM adjudicates equivalent level, usually half the original).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You gain Eldritch Blast as a known cantrip if you do not already have it; it scales with your level. Once per short rest, when a creature within 60 feet casts a spell, you may echo a simplified version of that spell on your next turn (DM adjudicates equivalent level, usually half the original).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve prerequisite grouping and missing Eldritch Blast definition/level scaling. Separately bound witnessing a cast within60ft, Short Rest echo trigger, next-turn release action/RP/rank/profile and half-level rounding. Preserve adjudication text but require finite playable choices; no arbitrary monster powers, copying a copy or invented Warlock class access."
```

### Preserved original source direction (historical)

```json
{
  "featId": "eldritch_echo",
  "name": "Eldritch Echo",
  "cohort": "magic_extended",
  "questionId": "MX-46",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/45",
  "originalQuestion": "Resolve prerequisite grouping and missing Eldritch Blast definition/level scaling. Separately bound witnessing a cast within60ft, Short Rest echo trigger, next-turn release action/RP/rank/profile and half-level rounding. Preserve adjudication text but require finite playable choices; no arbitrary monster powers, copying a copy or invented Warlock class access.",
  "originalSourceObject": {
    "id": "eldritch_echo",
    "name": "Eldritch Echo",
    "description": "Your patron's voice returns through you, repeating power that was never meant for mortal throats. Prestige lineage: Warlock. completed from the existing development record.)",
    "prerequisite": "Forbidden Pact or spellcasting ability, level 3+",
    "effect": "You gain Eldritch Blast as a known cantrip if you do not already have it; it scales with your level. Once per short rest, when a creature within 60 feet casts a spell, you may echo a simplified version of that spell on your next turn (DM adjudicates equivalent level, usually half the original).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You gain Eldritch Blast as a known cantrip if you do not already have it; it scales with your level. Once per short rest, when a creature within 60 feet casts a spell, you may echo a simplified version of that spell on your next turn (DM adjudicates equivalent level, usually half the original).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "ba683a0523e837af91dfc936148d7ba19f4b659ca843ca2adf06f1bee9ae9767",
  "submittedProcedure": "Require character 3 AND (Forbidden Pact OR actual spellcasting). Gain the exact NEW Eldritch Blast cantrip profile below once; duplicate grant through Forbidden Pact shares one identity. Once SR/LR when you actually perceive a creature within 60 ft/line of effect completing an eligible noncopyspell, use a Reaction to capture one matching bounded copy profile below. NEW the source may be ally or foe, but cannot be a resource/copy/production effect or protected boss/legendary ability. Record original rank and the profile’s half-rankq; it must fit your actual qualifying casting route’s learnable ceiling, with Forbidden Pact’s explicit rank 0 grant supplying no ranked ceiling by itself. On your next future regular turn use anAction, actualRPprice and V/S to release that one profile; otherwise it expires at that turn’s end. It is a copied spell activation with actual Dissonance/Refrain/history and interruption at release, no new proc/capture. No free original full spell, copied casterstatistics or Warlockclass.",
  "submittedNewChoices": "Grouping, missingcantrip, Reactioncapture and finite paid next-turn copy profile replace open adjudication.",
  "submittedWorkedCases": [
    "Observe rank 4 damage: half-rankq 2 Strike may be captured if your real route can learn rank 2, then costs 3 RP next turn.",
    "Forbidden Pact alone supplies the cantrip, not a rank 2 spell repertoire orRPpool for that copied release."
  ],
  "decision": "Adopt the separate feat-only CHA Eldritch Blast plus one bounded captured profile; release is an actual paid feat-copy cast, not an ordinary spell grant or free class Echo.",
  "completeAuthoringProcedure": "Require character 3 AND (Forbidden Pact OR actual spellcasting). Gain the exact NEW Eldritch Blast cantrip profile below once; duplicate grant through Forbidden Pact shares one identity. Once SR/LR when you actually perceive a creature within 60 ft/line of effect completing an eligible noncopyspell, use a Reaction to capture one matching bounded copy profile below. NEW the source may be ally or foe, but cannot be a resource/copy/production effect or protected boss/legendary ability. Record original rank and the profile’s half-rankq; it must fit your actual qualifying casting route’s learnable ceiling, with Forbidden Pact’s explicit rank 0 grant supplying no ranked ceiling by itself. On your next future regular turn use anAction, actualRPprice and V/S and any additional actual copied-profile component requirement to release that one profile; otherwise it expires at that turn’s end. It is a copied spell activation with actual Dissonance/Refrain/history and interruption at release, no new proc/capture. No free original full spell, copied casterstatistics or Warlockclass.\nNEW classification reconciliation, FS-08: releasing this captured spell is a paid feat-copy cast, using the releaser’s specified ability/PB, actual components, current RP price, rank and ordinary Dissonance/Refrain. It is not a resource-free nonspell release. It grants no ordinary repertoire/class feature or further capture, echo, reflection, external feat amplification, class resource/proc or reward chain. The concrete copy profile and its independent component/range/target/deadline limits still apply. This is deliberately different from Echo Spell/Twin Cast secondary results and from an actual Mirrorsage class Echo Release.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Observe rank 4 damage: half-rankq 2 Strike may be captured if your real route can learn rank 2, then costs 3 RP next turn.",
    "Forbidden Pact alone supplies the cantrip, not a rank 2 spell repertoire orRPpool for that copied release."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require character 3 AND (Forbidden Pact OR actual spellcasting). Gain the exact NEW Eldritch Blast cantrip profile below once; duplicate grant through Forbidden Pact shares one identity. Once SR/LR when you actually perceive a creature within 60 ft/line of effect completing an eligible noncopyspell, use a Reaction to capture one matching bounded copy profile below. NEW the source may be ally or foe, but cannot be a resource/copy/production effect or protected boss/legendary ability. Record original rank and the profile’s half-rankq; it must fit your actual qualifying casting route’s learnable ceiling, with Forbidden Pact’s explicit rank 0 grant supplying no ranked ceiling by itself. On your next future regular turn use anAction, actualRPprice and V/S and any additional actual copied-profile component requirement to release that one profile; otherwise it expires at that turn’s end. It is a copied spell activation with actual Dissonance/Refrain/history and interruption at release, no new proc/capture. No free original full spell, copied casterstatistics or Warlockclass.
NEW classification reconciliation, FS-08: releasing this captured spell is a paid feat-copy cast, using the releaser’s specified ability/PB, actual components, current RP price, rank and ordinary Dissonance/Refrain. It is not a resource-free nonspell release. It grants no ordinary repertoire/class feature or further capture, echo, reflection, external feat amplification, class resource/proc or reward chain. The concrete copy profile and its independent component/range/target/deadline limits still apply. This is deliberately different from Echo Spell/Twin Cast secondary results and from an actual Mirrorsage class Echo Release.

FEAT335-COPY-RELEASE-SOURCE-01-ADDENDUM — controlling release completion.
NEW feat-copy chronological identity. Every paid feat-copy cast records `castFamilyKey = feat-copy::<canonicalSourceEffectId>`. `canonicalSourceEffectId` is the stable identity of the actually witnessed underlying spell/effect from which the bounded profile was captured; for a source-qualified monster ability use that ability's stable source identity. Changing the capture event, owner, Eldritch Echo/Mimicry/Arcane Adaptation permission, bounded profile, selected damage/type component, q, or qualifying casting-ability route does not create a new family. Copies sharing that key use the ordinary chronological Refrain history together. An ordinary cast of the underlying spell uses its ordinary spell family and does not share the feat-copy family; Mirrorsage Echo Release likewise keeps its own class family. A missing stable underlying source identity is ineligible for release rather than being assigned a favorable new key. This key grants no ordinary spell knowledge or access.

NEW feat-copy concentration tags. Strike: no. Burst: no. Mend: no. Ward: yes. Hindrance: yes. Boon: yes. Step: no; its movement/teleport resolves instantaneously. A concentration-required copy establishes the releaser's one concentration burden during casting commitment under the ordinary sequence, ending an incompatible existing concentration before the counter window. If that cast is later countered, prior concentration remains ended and no copied lasting effect remains. Loss of concentration ends the Ward/Hindrance/Boon copied effect immediately; their printed earlier deadlines still cap duration. Immediate profiles establish no new concentration burden. Ready is separate: preparation already occupies concentration. On release, an immediate profile resolves and that Ready concentration ends with the released spell; a concentration-required Ward/Hindrance/Boon continues on that same one concentration burden, never a second slot. No witnessed original concentration tag is inherited or used to change these seven profile tags.

COPY-ROUTE STRAIN SCOPE. A paid feat-copy cast under FS-08 is an independent feat-casting route for strain purposes. Use FS-09 exactly: base Dissonance 0 for q/rank 0, 1 for ranks 1-5, and 2 for ranks 6-9; apply ordinary same-family Refrain using CRS-01; and use `Limit = max(4, 2*PB + casting modifier)` for that copy route, including its existing surcharge/block thresholds. The owned route chosen to qualify the copy supplies only the permitted casting ability, rank ceiling and other expressly required source credentials; it does not import that class engine's protected Dissonance reduction, routing, vent, prepared-matrix treatment or proc chain into the feat-copy cast. In particular a Wizard-qualified copy is not a prepared matrix, a Shaman-qualified copy is not an ordinary Shaman spell for the totem vent, and a Mirrorsage-qualified copy is not class Echo Release. The ordinary `max(4, 2 + PB + max(0, modifier))` Limit in SPELL_INTEGRATION_RULES remains controlling for ordinary class spells within its existing scope and is not globally changed here. If the only qualifying route is the feat-only Eldritch Blast grant, it supplies CHA and only its actual rank-0 ceiling; it does not change the copy engine or Limit, create a Warlock/class engine, or qualify a ranked q>0 copy.

COPY-READY-ALLOWANCE-02 — owner-directed preparation-round-only successor for the seven FS-08/SUP-07 feat-copy profiles used through Arcane Adaptation, Eldritch Echo and Mimicry. This supersedes COPY-READY-ALLOWANCE-01's both-touched-round policy only. All earlier archives and receipts retain their exact historical wording. This selection changes no profile payload, acquisition predicate, ordinary Ready rule, ordinary class casting cadence or unrelated Mirrorsage class Echo procedure.

PREPARATION. The shared feat-copy cap counts new paid feat-copy casting commitments: a direct cast commits in its current numbered round; a Readied feat copy commits in its preparation numbered round. Require and atomically spend that round's owner feat-copy allowance. If the owner actually has the separately acquired Mirrorsage shared-release engine to which the exact source binds this feat copy, also require and spend that same preparation round's actual shared class allowance. A qualifying ability route alone never creates that engine. Validate the actual setup prerequisites first. At legal preparation commitment, pay the Action, current quote and other actual costs, consume the applicable permission/use once, provide components, record the independent feat-copy family/Dissonance/Refrain once, and establish the one Ready concentration burden before its single preparation counter window. No partial class/feat/resource debit is allowed. Countering, abandonment, replacement, expiry or concentration loss after commitment never refunds those preparation spends, recreates a capture, restores displaced concentration or reopens that round's allowance. Failed precommit validation spends nothing and cannot delete an existing valid hold.

HELD RECORD. Bind one unique preparation ID and actual owner to its fixed captured source/profile/q/mode, preparation-bound choices, paid transaction, consumed permission receipt, preparation round and actual ledger identities. Preserve its original Ready deadline and every independently applicable earlier source/capture/use deadline. Consuming the capture permission at preparation is not itself loss of this paid hold's authorization, but the hold cannot extend the original permission window. No future round's allowance is reserved. The hold remains subject to ordinary concentration, body/source availability and valid replacement rules. Paid preparation alone creates no payload. Earlier prose calling the limit one-copy-release per round is controlled here: it limits new direct casts and Ready preparations, not a later completion of this same paid hold.

RELEASE. After an actual perceivable trigger has completed and before every governing deadline, validate the actual hold and its preparation receipts, the available lawful Reaction, continuing concentration and the release predicates at the points required by their actual sources. Select legal current targets/ordered recipients/area/destination at release under the fixed preparation profile and mode; do not freeze a setup-time ghost target or rewrite preparation-bound choices from hidden results. Neither same-round nor later-round release checks, reserves or spends a new feat-copy allowance or a new Mirrorsage shared-release allowance. The preparation receipts remain spent in their original round. An otherwise lawful delayed release therefore remains eligible even when the release round's feat allowance, an actually owned class shared allowance, or both have already been spent by another lawful use. This exemption belongs only to completion of that specific paid feat-copy hold; it does not waive any new direct cast's or unrelated class Echo's own allowances.

A declined trigger or an invalid precommit release, including no actual Reaction, invalid target/geometry, missing source predicate or uncompleted/unperceived trigger, spends no Reaction, makes no new debit and grants no hidden diagnostic. Keep the existing hold only while its actual concentration and original deadlines permit; another genuine trigger occurrence may be considered. An already-spent release-round copy allowance alone is NOT a failed-release reason. At an exact governing expiry, expiry wins. Lost concentration, actual abandonment, successful replacement or another real ending terminates the hold without a refund; a failed release cannot restore a hold that ended.

On a valid release commitment, atomically consume this hold once and spend the real Reaction before resolving its one payload. No second RP/material payment, capture-use consumption, casting-family/Refrain update, cast hook or Counterspell window occurs. Subsequent prevention or a failed attack/save outcome does not refund the Reaction or preparation; actual source-specific hidden-eligibility checks retain their own paid timing. Duplicate callbacks/retry IDs cannot create a second payload or debit. Immediate Strike/Burst/Mend/Step end the held concentration after resolution. Ward/Hindrance/Boon continue the same one burden under their actual effect clock and earlier limits, never a second concentration slot.

OTHER USES AND PERSISTENCE. Another copy in the release round still needs its own genuinely available Action/source permission, current legal resources/credentials, its own new-commitment allowances and all ordinary concentration/cadence predicates. No Action, Reaction refresh, capture or second concentration slot is granted. A concentration-breaking new cast can end the old hold even though its allowance is irrelevant to the old release. Releasing a prior hold first leaves a genuinely free current-round allowance available for a separate lawful new commitment; a lawful prior current-round use does not by itself block the old hold's release. Actual competing-use opportunities before the owner's next regular START are illustrative prerequisites unless supplied by a real source; the old Ready cannot be carried past that START merely to obtain the ordinary Action. Save/load, extra turns, changing routes/profiles or round labels must preserve owner/hold identity, original expiry, actual consumed receipts, completed release identity and chronological/per-round ledgers. Release never rewrites a later cast's history. This rule is a proposed authoring successor, not implementation of scheduling, live perception, source-qualified recipient effects, canonical persistence or the game engine.

### Original-position authored review references

```json
[
  {
    "id": "MX-46-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/10"
  },
  {
    "id": "MX-46-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/11"
  },
  {
    "id": "FA-17",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/additionalBoundaryReviews/0"
  }
]
```

## MX-47 — Forbidden Pact

### Complete original object

```json
{
  "id": "forbidden_pact",
  "name": "Forbidden Pact",
  "description": "You signed in blood and silence. Something old signed back. Prestige lineage: Warlock. completed from the existing development record.)",
  "prerequisite": "Charisma 13+, level 3+",
  "effect": "You forge a soul pact with an entity beyond the known planes. You gain Eldritch Blast and one pact sigil (e.g., shadowstep, hex bonus, or energy resistance) chosen with your DM. Once per encounter, you may spend hit points equal to twice the spell's level instead of a ranked-spell recovery.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You forge a soul pact with an entity beyond the known planes. You gain Eldritch Blast and one pact sigil (e.g., shadowstep, hex bonus, or energy resistance) chosen with your DM. Once per encounter, you may spend hit points equal to twice the spell's level instead of a spell slot.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve exact pact/origin wording without reviewing or revising cosmology before push. Mechanically resolve missing Eldritch Blast, a finite pact-sigil menu with actual stats/cadence and once-per-encounter2xRank HP substitution for ranked recovery. Specify true-HP funding, RP route, zeroHP, interruption and encounter ledger; no unstated entity powers, spell-slot pool or permanent soul transaction procedure."
```

### Preserved original source direction (historical)

```json
{
  "featId": "forbidden_pact",
  "name": "Forbidden Pact",
  "cohort": "magic_extended",
  "questionId": "MX-47",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/46",
  "originalQuestion": "Preserve exact pact/origin wording without reviewing or revising cosmology before push. Mechanically resolve missing Eldritch Blast, a finite pact-sigil menu with actual stats/cadence and once-per-encounter2xRank HP substitution for ranked recovery. Specify true-HP funding, RP route, zeroHP, interruption and encounter ledger; no unstated entity powers, spell-slot pool or permanent soul transaction procedure.",
  "originalSourceObject": {
    "id": "forbidden_pact",
    "name": "Forbidden Pact",
    "description": "You signed in blood and silence. Something old signed back. Prestige lineage: Warlock. completed from the existing development record.)",
    "prerequisite": "Charisma 13+, level 3+",
    "effect": "You forge a soul pact with an entity beyond the known planes. You gain Eldritch Blast and one pact sigil (e.g., shadowstep, hex bonus, or energy resistance) chosen with your DM. Once per encounter, you may spend hit points equal to twice the spell's level instead of a ranked-spell recovery.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You forge a soul pact with an entity beyond the known planes. You gain Eldritch Blast and one pact sigil (e.g., shadowstep, hex bonus, or energy resistance) chosen with your DM. Once per encounter, you may spend hit points equal to twice the spell's level instead of a spell slot.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "e1fa56ac44d906226345bea586a6be100bfcc5838f8aa37f890a3e1d23cf7a65",
  "submittedProcedure": "Require CHA 13 and character 3. Preserve the original beyond-known-planes soul-pact wording as unreviewed setting provenance; this procedure grants no soul transfer, patron demands or cosmological claim. Mechanically gain the exact NEW Eldritch Blast profile and choose permanently one of three finite sigils below with the Director. This feat’s casting ability is CHA and grants rank 0 access only, not anRPpool or ranked repertoire. NEW reconcile “instead of a ranked-spell recovery” and old “instead of a spell slot” as once per real encounter substituting 2×actualrank normal HP sacrifice for the ordinary baseRPprice of one independently known/prepared rank 1–9 spell. Commit true HP loss while retaining at least 1 normal HP; temp HP, mitigation, floors/refunds cannot fund it. It is sacrifice, not damage, so no Wound/concentration/damageproc from the payment. AdditionalRPcosts, strain/armor/component surcharges, materials and action remain actual payments; final price calculation waives only original rankbase before those additions. NoRPis restored, no chargeuse bypassed, no separate ranked grant and no incidental resource output. Interrupted spell keeps all costs/use spent.",
  "submittedNewChoices": "Finitecantrip/sigil grants plus explicit NEW base RP substitution resolve the inconsistent recovery/slot phrase without new ontology.",
  "submittedWorkedCases": [
    "An independently legal rank 2 cast may substitute 4 normal HP for base 3 RP once this encounter, still paying an actual extra 1 RP surcharge.",
    "A pact-holder who knows only Eldritch Blast gains no ranked spell to pay for this way."
  ],
  "decision": "Adopt one of three closed sigils and the distinct normal-HP sacrifice substitution; sacrifice is a state payment, not Arcane Transfusion damage, and creates no patron/class ontology.",
  "completeAuthoringProcedure": "Require CHA 13 and character 3. Preserve the original beyond-known-planes soul-pact wording as unreviewed setting provenance; this procedure grants no soul transfer, patron demands or cosmological claim. Mechanically gain the exact NEW Eldritch Blast profile and choose permanently one of three finite sigils below with the Director. This feat’s casting ability is CHA and grants rank 0 access only, not anRPpool or ranked repertoire. NEW reconcile “instead of a ranked-spell recovery” and old “instead of a spell slot” as once per real encounter substituting 2×actualrank normal HP sacrifice for the ordinary baseRPprice of one independently known/prepared rank 1–9 spell. Commit true HP loss while retaining at least 1 normal HP; temp HP, mitigation, floors/refunds cannot fund it. It is sacrifice, not damage, so no Wound/concentration/damageproc from the payment. AdditionalRPcosts, strain/armor/component surcharges, materials and action remain actual payments; final price calculation waives only original rankbase before those additions. NoRPis restored, no chargeuse bypassed, no separate ranked grant and no incidental resource output. Interrupted spell keeps all costs/use spent.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An independently legal rank 2 cast may substitute 4 normal HP for base 3 RP once this encounter, still paying an actual extra 1 RP surcharge.",
    "A pact-holder who knows only Eldritch Blast gains no ranked spell to pay for this way."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require CHA 13 and character 3. Preserve the original beyond-known-planes soul-pact wording as unreviewed setting provenance; this procedure grants no soul transfer, patron demands or cosmological claim. Mechanically gain the exact NEW Eldritch Blast profile and choose permanently one of three finite sigils below with the Director. This feat’s casting ability is CHA and grants rank 0 access only, not anRPpool or ranked repertoire. NEW reconcile “instead of a ranked-spell recovery” and old “instead of a spell slot” as once per real encounter substituting 2×actualrank normal HP sacrifice for the ordinary baseRPprice of one independently known/prepared rank 1–9 spell. Commit true HP loss while retaining at least 1 normal HP; temp HP, mitigation, floors/refunds cannot fund it. It is sacrifice, not damage, so no Wound/concentration/damageproc from the payment. AdditionalRPcosts, strain/armor/component surcharges, materials and action remain actual payments; final price calculation waives only original rankbase before those additions. NoRPis restored, no chargeuse bypassed, no separate ranked grant and no incidental resource output. Interrupted spell keeps all costs/use spent.

### Original-position authored review references

```json
[
  {
    "id": "MX-47-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/12"
  },
  {
    "id": "MX-47-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/13"
  }
]
```

## MX-48 — Hemocraft

### Complete original object

```json
{
  "id": "hemocraft",
  "name": "Hemocraft",
  "description": "Blood is ink, blade is quill—you write power in crimson script across flesh and air. Prestige lineage: Bloodbound. completed from the existing development record.)",
  "prerequisite": "Intelligence or Charisma 13+",
  "effect": "When you score a critical hit with a melee attack, the target gains a Bleed stack (1d4 ongoing damage at the start of its turns). You can consume one Bleed stack from a creature within 30 feet to heal 1d8 hit points or deal 1d8 necrotic damage to that creature.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you score a critical hit with a melee attack, the target gains a Bleed stack (1d4 ongoing damage at the start of its turns). You can consume one Bleed stack from a creature within 30 feet to heal 1d8 hit points or deal 1d8 necrotic damage to that creature.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind real melee critical, Bleed-stack identity/ownership/cap/duration/cure and1d4 target-start pulse. Define action/cadence/range/sight for consuming one actually existing stack, choice of1d8 healing versus necrotic damage, which creature receives healing, save/attack and true-healing gates. Prevent free repeated consumption, copied Bleed and recursive zeroHP/resource events."
```

### Preserved original source direction (historical)

```json
{
  "featId": "hemocraft",
  "name": "Hemocraft",
  "cohort": "magic_extended",
  "questionId": "MX-48",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/47",
  "originalQuestion": "Bind real melee critical, Bleed-stack identity/ownership/cap/duration/cure and1d4 target-start pulse. Define action/cadence/range/sight for consuming one actually existing stack, choice of1d8 healing versus necrotic damage, which creature receives healing, save/attack and true-healing gates. Prevent free repeated consumption, copied Bleed and recursive zeroHP/resource events.",
  "originalSourceObject": {
    "id": "hemocraft",
    "name": "Hemocraft",
    "description": "Blood is ink, blade is quill—you write power in crimson script across flesh and air. Prestige lineage: Bloodbound. completed from the existing development record.)",
    "prerequisite": "Intelligence or Charisma 13+",
    "effect": "When you score a critical hit with a melee attack, the target gains a Bleed stack (1d4 ongoing damage at the start of its turns). You can consume one Bleed stack from a creature within 30 feet to heal 1d8 hit points or deal 1d8 necrotic damage to that creature.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you score a critical hit with a melee attack, the target gains a Bleed stack (1d4 ongoing damage at the start of its turns). You can consume one Bleed stack from a creature within 30 feet to heal 1d8 hit points or deal 1d8 necrotic damage to that creature.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "afb81f247749105961d26ea98a0b2eb4f117dde8fecc8e7985210ca66ac60e5b",
  "submittedProcedure": "After a personal genuine melee critical hit against meaningful opposition, apply one NEW Hemocraft Bleed record to the still-living eligible target. It pulses 1d4 slashing at each of its next three regular starts; source immunity/anatomy restrictions and the existing Bleeding-family arbitration/cures remain. NEW max 3 own records per target; at cap refresh the earliest deadline without adding a fourth. Same-family parallel records do not all deal damage: existing strongest-die arbitration selects one, but distinct consumable records retain identity. Once per numbered round use BA to consume one present unexpired own Hemocraft record on a creature you perceive within 30 ft/line of effect, including one temporarily suppressed record, choosing 1d8 ordinary self-healing OR one 1d8 necrotic packet to that creature withCONsave against DC 8+PB+your chosenINTor CHA modifier for half. Choose stat permanently at feat acquisition. Pay by ending that exact record before outcome; no refund or consumption of another source’s Bleed. Healing spends a NEW finite Hemocraft Reserve of 2×character level set only at beneficial LR, paying actual restored HP, no excess/copy/resource outputs. Reserve starts 0 on acquisition. No consuming historical/already-cured Bleed or staged victims. The record’s ordinary Medicine-ending DC is the same chosen feat DC; actual positive-potential magical healing ends eligible Bleed through the existing cure procedure.",
  "submittedNewChoices": "Three bounded ownBleedrecords, BA/cadence, complete damage/save/cures and finite healing reserve.",
  "submittedWorkedCases": [
    "Consume one actual record to roll 7 healing with 2 Reserve and sufficient missing HP: restore 2 and spend 2.",
    "A suppressed still-present record can be consumed, but an ended record cannot return for another heal."
  ],
  "decision": "Adopt finite3-record Bleed handling, one consumption per round and2×level healing reserve starting0 until a beneficial LR; no healing from cured/foreign/staged records.",
  "completeAuthoringProcedure": "After a personal genuine melee critical hit against meaningful opposition, apply one NEW Hemocraft Bleed record to the still-living eligible target. It pulses 1d4 slashing at each of its next three regular starts; source immunity/anatomy restrictions and the existing Bleeding-family arbitration/cures remain. NEW max 3 own records per target; at cap refresh the earliest deadline without adding a fourth. Same-family parallel records do not all deal damage: existing strongest-die arbitration selects one, but distinct consumable records retain identity. Once per numbered round use BA to consume one present unexpired own Hemocraft record on a creature you perceive within 30 ft/line of effect, including one temporarily suppressed record, choosing 1d8 ordinary self-healing OR one 1d8 necrotic packet to that creature withCONsave against DC 8+PB+your chosenINTor CHA modifier for half. Choose stat permanently at feat acquisition. Pay by ending that exact record before outcome; no refund or consumption of another source’s Bleed. Healing spends a NEW finite Hemocraft Reserve of 2×character level set only at beneficial LR, paying actual restored HP, no excess/copy/resource outputs. Reserve starts 0 on acquisition. No consuming historical/already-cured Bleed or staged victims. The record’s ordinary Medicine-ending DC is the same chosen feat DC; actual positive-potential magical healing ends eligible Bleed through the existing cure procedure.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Consume one actual record to roll 7 healing with 2 Reserve and sufficient missing HP: restore 2 and spend 2.",
    "A suppressed still-present record can be consumed, but an ended record cannot return for another heal."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After a personal genuine melee critical hit against meaningful opposition, apply one NEW Hemocraft Bleed record to the still-living eligible target. It pulses 1d4 slashing at each of its next three regular starts; source immunity/anatomy restrictions and the existing Bleeding-family arbitration/cures remain. NEW max 3 own records per target; at cap refresh the earliest deadline without adding a fourth. Same-family parallel records do not all deal damage: existing strongest-die arbitration selects one, but distinct consumable records retain identity. Once per numbered round use BA to consume one present unexpired own Hemocraft record on a creature you perceive within 30 ft/line of effect, including one temporarily suppressed record, choosing 1d8 ordinary self-healing OR one 1d8 necrotic packet to that creature withCONsave against DC 8+PB+your chosenINTor CHA modifier for half. Choose stat permanently at feat acquisition. Pay by ending that exact record before outcome; no refund or consumption of another source’s Bleed. Healing spends a NEW finite Hemocraft Reserve of 2×character level set only at beneficial LR, paying actual restored HP, no excess/copy/resource outputs. Reserve starts 0 on acquisition. No consuming historical/already-cured Bleed or staged victims. The record’s ordinary Medicine-ending DC is the same chosen feat DC; actual positive-potential magical healing ends eligible Bleed through the existing cure procedure.

### Original-position authored review references

```json
[
  {
    "id": "MX-48-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/14"
  },
  {
    "id": "MX-48-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/15"
  },
  {
    "id": "FA-26",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/additionalBoundaryReviews/2"
  }
]
```

## MX-49 — Lightning Affinity

### Complete original object

```json
{
  "id": "lightning_affinity",
  "name": "Lightning Affinity",
  "description": "Storm-blood runs quiet in you until the sky asks it to speak. Prestige lineage: Storm Lord. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability or proficiency in Nature",
  "effect": "You have resistance to lightning damage. Your lightning spells deal +1 damage per die and ignore half cover when the target is outdoors or under open sky. You have advantage on saving throws against electrical and paralyzing effects. When you take lightning damage, you can use your reaction to store the excess (after resistance) as Storm Charge (max 2); spend 1 charge to add 1d6 lightning to your next spell or weapon attack before the end of your next turn.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You have resistance to lightning damage. Your lightning spells deal +1 damage per die and ignore half cover when the target is outdoors or under open sky. You have advantage on saving throws against electrical and paralyzing effects. When you take lightning damage, you can use your reaction to store the excess (after resistance) as Storm Charge (max 2); spend 1 charge to add 1d6 lightning to your next spell or weapon attack before the end of your next turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve resistance, lightning spell+1/die, conditional half-cover ignoring, electrical/paralysis save advantage and reactive Storm Charges. Define post-resistance received damage versus charges gained,max2/lifetime, Reaction, spending timing/cadence, next spell/weapon+1d6 packet and expiry. Resolve multi-die/area/critical/zero-damage cases without converting every damage point into a charge."
```

### Preserved original source direction (historical)

```json
{
  "featId": "lightning_affinity",
  "name": "Lightning Affinity",
  "cohort": "magic_extended",
  "questionId": "MX-49",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/48",
  "originalQuestion": "Preserve resistance, lightning spell+1/die, conditional half-cover ignoring, electrical/paralysis save advantage and reactive Storm Charges. Define post-resistance received damage versus charges gained,max2/lifetime, Reaction, spending timing/cadence, next spell/weapon+1d6 packet and expiry. Resolve multi-die/area/critical/zero-damage cases without converting every damage point into a charge.",
  "originalSourceObject": {
    "id": "lightning_affinity",
    "name": "Lightning Affinity",
    "description": "Storm-blood runs quiet in you until the sky asks it to speak. Prestige lineage: Storm Lord. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability or proficiency in Nature",
    "effect": "You have resistance to lightning damage. Your lightning spells deal +1 damage per die and ignore half cover when the target is outdoors or under open sky. You have advantage on saving throws against electrical and paralyzing effects. When you take lightning damage, you can use your reaction to store the excess (after resistance) as Storm Charge (max 2); spend 1 charge to add 1d6 lightning to your next spell or weapon attack before the end of your next turn.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You have resistance to lightning damage. Your lightning spells deal +1 damage per die and ignore half cover when the target is outdoors or under open sky. You have advantage on saving throws against electrical and paralyzing effects. When you take lightning damage, you can use your reaction to store the excess (after resistance) as Storm Charge (max 2); spend 1 charge to add 1d6 lightning to your next spell or weapon attack before the end of your next turn.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "911dfe95c6641846355ad890fc9d469b14907f08191c21fbd38779fe66dc1021",
  "submittedProcedure": "Gain lightning resistance and+1 damage per actual native lightning die in your personally cast spells, including native critical dice, as a flat adjustment before save/defense; no bonus per flatpoint, added nonlightning die or copied packet. Against a target actually outdoors/open-sky, your lightning spell attack/save geometry ignores halfcover only; threequarters/total cover remain. Gainadvantage on actual saves against a lightning/electrical payload or a component imposingParalyzed, not everyCONsave. After a hostile meaningful lightning packet deals positive actual numeric damage to you, spendReaction to gain oneStormCharge, max 2. NEW no charge per damagepoint; genuine tempHPabsorption qualifies, fully prevented/floor-only numeric 0 doesnot. Each charge lasts one minute from gain; no maximum cap refresh from a rejected gain. On your own turn, spend one charge withoutAction to prime your next personal weapon attack or immediate damaging spell before next regular end: add 1d6 lightning to one selected hit/packet/shared area roll under added-die rules. Attackmiss consumes the primed rider; no stacking multiplecharges on oneactivation. No charge from self/cooperative/copy/retaliationdamage.",
  "submittedNewChoices": "Native lightningdice, oneReactioncharge/event, one-minute stored lifetime and one primed packet.",
  "submittedWorkedCases": [
    "A native 3d6 lightningspell adds 3 before saves; a reaction to 8 actual lightningdamage gains 1 charge, not 8.",
    "A miss wastes the primed die; a later attack cannot recover that spent charge."
  ],
  "decision": "Adopt native lightning-die+1, actual half-cover scope and two separately expiring charges; respect source no-resource flags and do not refresh old charges at capacity.",
  "completeAuthoringProcedure": "Gain lightning resistance and+1 damage per actual native lightning die in your personally cast spells, including native critical dice, as a flat adjustment before save/defense; no bonus per flatpoint, added nonlightning die or copied packet. Against a target actually outdoors/open-sky, your lightning spell attack/save geometry ignores halfcover only; threequarters/total cover remain. Gainadvantage on actual saves against a lightning/electrical payload or a component imposingParalyzed, not everyCONsave. After a hostile meaningful lightning packet deals positive actual numeric damage to you, spendReaction to gain oneStormCharge, max 2. NEW no charge per damagepoint; genuine tempHPabsorption qualifies, fully prevented/floor-only numeric 0 doesnot. Each charge lasts one minute from gain; no maximum cap refresh from a rejected gain. On your own turn, spend one charge withoutAction to prime your next personal weapon attack or immediate damaging spell before next regular end: add 1d6 lightning to one selected hit/packet/shared area roll under added-die rules. Attackmiss consumes the primed rider; no stacking multiplecharges on oneactivation. No charge from self/cooperative/copy/retaliationdamage.\nPreserve per-charge origin and expiry: receiving a further charge at capacity does not refresh an older charge. FS-07 respects each underlying spell’s no-resource/trigger flags. The native lightning-die+1 excludes external riders and secondary/copy results; it can add to an independently eligible Evocation Focus bonus on an actually rolled kept die, not on a fictitious maximized face.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A native 3d6 lightningspell adds 3 before saves; a reaction to 8 actual lightningdamage gains 1 charge, not 8.",
    "A miss wastes the primed die; a later attack cannot recover that spent charge."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Gain lightning resistance and+1 damage per actual native lightning die in your personally cast spells, including native critical dice, as a flat adjustment before save/defense; no bonus per flatpoint, added nonlightning die or copied packet. Against a target actually outdoors/open-sky, your lightning spell attack/save geometry ignores halfcover only; threequarters/total cover remain. Gainadvantage on actual saves against a lightning/electrical payload or a component imposingParalyzed, not everyCONsave. After a hostile meaningful lightning packet deals positive actual numeric damage to you, spendReaction to gain oneStormCharge, max 2. NEW no charge per damagepoint; genuine tempHPabsorption qualifies, fully prevented/floor-only numeric 0 doesnot. Each charge lasts one minute from gain; no maximum cap refresh from a rejected gain. On your own turn, spend one charge withoutAction to prime your next personal weapon attack or immediate damaging spell before next regular end: add 1d6 lightning to one selected hit/packet/shared area roll under added-die rules. Attackmiss consumes the primed rider; no stacking multiplecharges on oneactivation. No charge from self/cooperative/copy/retaliationdamage.
Preserve per-charge origin and expiry: receiving a further charge at capacity does not refresh an older charge. FS-07 respects each underlying spell’s no-resource/trigger flags. The native lightning-die+1 excludes external riders and secondary/copy results; it can add to an independently eligible Evocation Focus bonus on an actually rolled kept die, not on a fictitious maximized face.

### Original-position authored review references

```json
[
  {
    "id": "MX-49-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/16"
  },
  {
    "id": "MX-49-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/17"
  }
]
```

## MX-50 — Mimicry

### Complete original object

```json
{
  "id": "mimicry",
  "name": "Mimicry",
  "description": "See it once, steal its thunder—your mirror learns faster than pride allows. Prestige lineage: Echomancer. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, Intelligence 15+",
  "effect": "When you witness a spell or monster ability used against you or within 30 feet, you can mimic a simplified version once before your next short rest. The mimicked effect lasts up to 2 rounds and is usually at half potency (DM adjudicates).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you witness a spell or monster ability used against you or within 30 feet, you can mimic a simplified version once before your next short rest. The mimicked effect lasts up to 2 rounds and is usually at half potency (DM adjudicates).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define witnessed/targeted spell or monster ability,30ft senses, one stored simplified profile and acquisition/cast costs/cadence. Replace usually-half/Director-adjudicates ambiguity with explicit finite playable rules while preserving originals. Specify next Short Rest expiry,two-round effect cap,rank/DC/targets and exclusions for resources,actions,copy recursion and unsupported abilities."
```

### Preserved original source direction (historical)

```json
{
  "featId": "mimicry",
  "name": "Mimicry",
  "cohort": "magic_extended",
  "questionId": "MX-50",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/49",
  "originalQuestion": "Define witnessed/targeted spell or monster ability,30ft senses, one stored simplified profile and acquisition/cast costs/cadence. Replace usually-half/Director-adjudicates ambiguity with explicit finite playable rules while preserving originals. Specify next Short Rest expiry,two-round effect cap,rank/DC/targets and exclusions for resources,actions,copy recursion and unsupported abilities.",
  "originalSourceObject": {
    "id": "mimicry",
    "name": "Mimicry",
    "description": "See it once, steal its thunder—your mirror learns faster than pride allows. Prestige lineage: Echomancer. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability, Intelligence 15+",
    "effect": "When you witness a spell or monster ability used against you or within 30 feet, you can mimic a simplified version once before your next short rest. The mimicked effect lasts up to 2 rounds and is usually at half potency (DM adjudicates).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you witness a spell or monster ability used against you or within 30 feet, you can mimic a simplified version once before your next short rest. The mimicked effect lasts up to 2 rounds and is usually at half potency (DM adjudicates).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "95973108b8f8fbd61a5870ec56c389888207190a4aa7b075a9923588c43a71a0",
  "submittedProcedure": "Once between beneficial SR/LR completions, when you perceive an eligible real spell/monster ability used against you at its lawful range OR resolving within 30 ft of you and line of effect, capture one matching finite copy profile below withoutAction. NEW one record and one release entitlement per rest epoch; cannot erase/replace to gain repeated uses. No copy from a copy, protectedunique/legendary/boss feature, classengine, resource/action/creation effect or an unobserved component. Actual targeted-at-you clause may exceed 30 ft only if you genuinely perceive the source and effect. The stored profile expires at the next beneficial SR/LR; release before then usesAction, V/S, actualRPprice and its actual qualifying casting ability/rank ceiling. Its numeric native ceiling is half the observed eligible component as detailed below and duration at most two future regular intervals; no original source stats/unboundedDirector invention. Successful capture alone is not a cast; release commits ordinary spell history/interruption and the one-copy-release/round allowance. Failed/countered release consumes record/use, and a later rest never refills a missing copy.",
  "submittedNewChoices": "One capture/release perrest, targeted range branch and explicit half-potency profile rules.",
  "submittedWorkedCases": [
    "A perceived attack spell directed at you from 60 ft may qualify through the targeted clause despite the ordinary 30 ftwitness radius.",
    "Observing a monster restore RP cannot produce a copied recovery profile."
  ],
  "decision": "Adopt actual observed/targeted capture into a finite profile and paid feat-copy cast; preserve rank, RP, visibility and once-rest limits without copying class engines or unknown powers.",
  "completeAuthoringProcedure": "Once between beneficial SR/LR completions, when you perceive an eligible real spell/monster ability used against you at its lawful range OR resolving within 30 ft of you and line of effect, capture one matching finite copy profile below withoutAction. NEW one record and one release entitlement per rest epoch; cannot erase/replace to gain repeated uses. No copy from a copy, protectedunique/legendary/boss feature, classengine, resource/action/creation effect or an unobserved component. Actual targeted-at-you clause may exceed 30 ft only if you genuinely perceive the source and effect. The stored profile expires at the next beneficial SR/LR; release before then usesAction, V/S, actualRPprice and its actual qualifying casting ability/rank ceiling. Its numeric native ceiling is half the observed eligible component as detailed below and duration at most two future regular intervals; no original source stats/unboundedDirector invention. Successful capture alone is not a cast; release commits ordinary spell history/interruption and the one-copy-release/round allowance. Failed/countered release consumes record/use, and a later rest never refills a missing copy.\nNEW classification reconciliation, FS-08: releasing this captured spell is a paid feat-copy cast, using the releaser’s specified ability/PB, actual components, current RP price, rank and ordinary Dissonance/Refrain. It is not a resource-free nonspell release. It grants no ordinary repertoire/class feature or further capture, echo, reflection, external feat amplification, class resource/proc or reward chain. The concrete copy profile and its independent component/range/target/deadline limits still apply. This is deliberately different from Echo Spell/Twin Cast secondary results and from an actual Mirrorsage class Echo Release.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A perceived attack spell directed at you from 60 ft may qualify through the targeted clause despite the ordinary 30 ftwitness radius.",
    "Observing a monster restore RP cannot produce a copied recovery profile."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once between beneficial SR/LR completions, when you perceive an eligible real spell/monster ability used against you at its lawful range OR resolving within 30 ft of you and line of effect, capture one matching finite copy profile below withoutAction. NEW one record and one release entitlement per rest epoch; cannot erase/replace to gain repeated uses. No copy from a copy, protectedunique/legendary/boss feature, classengine, resource/action/creation effect or an unobserved component. Actual targeted-at-you clause may exceed 30 ft only if you genuinely perceive the source and effect. The stored profile expires at the next beneficial SR/LR; release before then usesAction, V/S, actualRPprice and its actual qualifying casting ability/rank ceiling. Its numeric native ceiling is half the observed eligible component as detailed below and duration at most two future regular intervals; no original source stats/unboundedDirector invention. Successful capture alone is not a cast. A direct cast, or the preparation of a legal Ready, commits ordinary spell history/interruption and the one-new-feat-copy-commitment-per-numbered-round allowance. A paid failed/countered casting retains its consumed record/use; an invalid uncommitted Ready release has no second permission charge. A later rest never refills a missing copy.
NEW classification reconciliation, FS-08: releasing this captured spell is a paid feat-copy cast, using the releaser’s specified ability/PB, actual components, current RP price, rank and ordinary Dissonance/Refrain. It is not a resource-free nonspell release. It grants no ordinary repertoire/class feature or further capture, echo, reflection, external feat amplification, class resource/proc or reward chain. The concrete copy profile and its independent component/range/target/deadline limits still apply. This is deliberately different from Echo Spell/Twin Cast secondary results and from an actual Mirrorsage class Echo Release.

FEAT335-COPY-RELEASE-SOURCE-01-ADDENDUM — controlling release completion.
NEW feat-copy chronological identity. Every paid feat-copy cast records `castFamilyKey = feat-copy::<canonicalSourceEffectId>`. `canonicalSourceEffectId` is the stable identity of the actually witnessed underlying spell/effect from which the bounded profile was captured; for a source-qualified monster ability use that ability's stable source identity. Changing the capture event, owner, Eldritch Echo/Mimicry/Arcane Adaptation permission, bounded profile, selected damage/type component, q, or qualifying casting-ability route does not create a new family. Copies sharing that key use the ordinary chronological Refrain history together. An ordinary cast of the underlying spell uses its ordinary spell family and does not share the feat-copy family; Mirrorsage Echo Release likewise keeps its own class family. A missing stable underlying source identity is ineligible for release rather than being assigned a favorable new key. This key grants no ordinary spell knowledge or access.

NEW feat-copy concentration tags. Strike: no. Burst: no. Mend: no. Ward: yes. Hindrance: yes. Boon: yes. Step: no; its movement/teleport resolves instantaneously. A concentration-required copy establishes the releaser's one concentration burden during casting commitment under the ordinary sequence, ending an incompatible existing concentration before the counter window. If that cast is later countered, prior concentration remains ended and no copied lasting effect remains. Loss of concentration ends the Ward/Hindrance/Boon copied effect immediately; their printed earlier deadlines still cap duration. Immediate profiles establish no new concentration burden. Ready is separate: preparation already occupies concentration. On release, an immediate profile resolves and that Ready concentration ends with the released spell; a concentration-required Ward/Hindrance/Boon continues on that same one concentration burden, never a second slot. No witnessed original concentration tag is inherited or used to change these seven profile tags.

COPY-ROUTE STRAIN SCOPE. A paid feat-copy cast under FS-08 is an independent feat-casting route for strain purposes. Use FS-09 exactly: base Dissonance 0 for q/rank 0, 1 for ranks 1-5, and 2 for ranks 6-9; apply ordinary same-family Refrain using CRS-01; and use `Limit = max(4, 2*PB + casting modifier)` for that copy route, including its existing surcharge/block thresholds. The owned route chosen to qualify the copy supplies only the permitted casting ability, rank ceiling and other expressly required source credentials; it does not import that class engine's protected Dissonance reduction, routing, vent, prepared-matrix treatment or proc chain into the feat-copy cast. In particular a Wizard-qualified copy is not a prepared matrix, a Shaman-qualified copy is not an ordinary Shaman spell for the totem vent, and a Mirrorsage-qualified copy is not class Echo Release. The ordinary `max(4, 2 + PB + max(0, modifier))` Limit in SPELL_INTEGRATION_RULES remains controlling for ordinary class spells within its existing scope and is not globally changed here. If the only qualifying route is the feat-only Eldritch Blast grant, it supplies CHA and only its actual rank-0 ceiling; it does not change the copy engine or Limit, create a Warlock/class engine, or qualify a ranked q>0 copy.

COPY-READY-ALLOWANCE-02 — owner-directed preparation-round-only successor for the seven FS-08/SUP-07 feat-copy profiles used through Arcane Adaptation, Eldritch Echo and Mimicry. This supersedes COPY-READY-ALLOWANCE-01's both-touched-round policy only. All earlier archives and receipts retain their exact historical wording. This selection changes no profile payload, acquisition predicate, ordinary Ready rule, ordinary class casting cadence or unrelated Mirrorsage class Echo procedure.

PREPARATION. The shared feat-copy cap counts new paid feat-copy casting commitments: a direct cast commits in its current numbered round; a Readied feat copy commits in its preparation numbered round. Require and atomically spend that round's owner feat-copy allowance. If the owner actually has the separately acquired Mirrorsage shared-release engine to which the exact source binds this feat copy, also require and spend that same preparation round's actual shared class allowance. A qualifying ability route alone never creates that engine. Validate the actual setup prerequisites first. At legal preparation commitment, pay the Action, current quote and other actual costs, consume the applicable permission/use once, provide components, record the independent feat-copy family/Dissonance/Refrain once, and establish the one Ready concentration burden before its single preparation counter window. No partial class/feat/resource debit is allowed. Countering, abandonment, replacement, expiry or concentration loss after commitment never refunds those preparation spends, recreates a capture, restores displaced concentration or reopens that round's allowance. Failed precommit validation spends nothing and cannot delete an existing valid hold.

HELD RECORD. Bind one unique preparation ID and actual owner to its fixed captured source/profile/q/mode, preparation-bound choices, paid transaction, consumed permission receipt, preparation round and actual ledger identities. Preserve its original Ready deadline and every independently applicable earlier source/capture/use deadline. Consuming the capture permission at preparation is not itself loss of this paid hold's authorization, but the hold cannot extend the original permission window. No future round's allowance is reserved. The hold remains subject to ordinary concentration, body/source availability and valid replacement rules. Paid preparation alone creates no payload. Earlier prose calling the limit one-copy-release per round is controlled here: it limits new direct casts and Ready preparations, not a later completion of this same paid hold.

RELEASE. After an actual perceivable trigger has completed and before every governing deadline, validate the actual hold and its preparation receipts, the available lawful Reaction, continuing concentration and the release predicates at the points required by their actual sources. Select legal current targets/ordered recipients/area/destination at release under the fixed preparation profile and mode; do not freeze a setup-time ghost target or rewrite preparation-bound choices from hidden results. Neither same-round nor later-round release checks, reserves or spends a new feat-copy allowance or a new Mirrorsage shared-release allowance. The preparation receipts remain spent in their original round. An otherwise lawful delayed release therefore remains eligible even when the release round's feat allowance, an actually owned class shared allowance, or both have already been spent by another lawful use. This exemption belongs only to completion of that specific paid feat-copy hold; it does not waive any new direct cast's or unrelated class Echo's own allowances.

A declined trigger or an invalid precommit release, including no actual Reaction, invalid target/geometry, missing source predicate or uncompleted/unperceived trigger, spends no Reaction, makes no new debit and grants no hidden diagnostic. Keep the existing hold only while its actual concentration and original deadlines permit; another genuine trigger occurrence may be considered. An already-spent release-round copy allowance alone is NOT a failed-release reason. At an exact governing expiry, expiry wins. Lost concentration, actual abandonment, successful replacement or another real ending terminates the hold without a refund; a failed release cannot restore a hold that ended.

On a valid release commitment, atomically consume this hold once and spend the real Reaction before resolving its one payload. No second RP/material payment, capture-use consumption, casting-family/Refrain update, cast hook or Counterspell window occurs. Subsequent prevention or a failed attack/save outcome does not refund the Reaction or preparation; actual source-specific hidden-eligibility checks retain their own paid timing. Duplicate callbacks/retry IDs cannot create a second payload or debit. Immediate Strike/Burst/Mend/Step end the held concentration after resolution. Ward/Hindrance/Boon continue the same one burden under their actual effect clock and earlier limits, never a second concentration slot.

OTHER USES AND PERSISTENCE. Another copy in the release round still needs its own genuinely available Action/source permission, current legal resources/credentials, its own new-commitment allowances and all ordinary concentration/cadence predicates. No Action, Reaction refresh, capture or second concentration slot is granted. A concentration-breaking new cast can end the old hold even though its allowance is irrelevant to the old release. Releasing a prior hold first leaves a genuinely free current-round allowance available for a separate lawful new commitment; a lawful prior current-round use does not by itself block the old hold's release. Actual competing-use opportunities before the owner's next regular START are illustrative prerequisites unless supplied by a real source; the old Ready cannot be carried past that START merely to obtain the ordinary Action. Save/load, extra turns, changing routes/profiles or round labels must preserve owner/hold identity, original expiry, actual consumed receipts, completed release identity and chronological/per-round ledgers. Release never rewrites a later cast's history. This rule is a proposed authoring successor, not implementation of scheduling, live perception, source-qualified recipient effects, canonical persistence or the game engine.

### Original-position authored review references

```json
[
  {
    "id": "MX-50-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/18"
  },
  {
    "id": "MX-50-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/19"
  },
  {
    "id": "FA-18",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/additionalBoundaryReviews/1"
  }
]
```

## MX-51 — Quickened Thought

### Complete original object

```json
{
  "id": "quickened_thought",
  "name": "Quickened Thought",
  "description": "Your mind outpaces the tick of Aethel's clocks—ideas arrive finished in the Temporal Tower's shadow, as if tomorrow's spell were already written in today's breath. Prestige lineage: Chronomancer. completed from the existing development record.)",
  "prerequisite": "Intelligence 15+, Arcane Calculus or Temporal Theory",
  "effect": "You gain +2 to initiative and advantage on concentration saves while holding a readied spell. Once per short rest, you may cast a spell of 2nd level or lower as a bonus action; if you do, you cannot take a reaction until the start of your next turn. When you roll initiative, you may bank one cantrip cast—release it on any later turn in the encounter without spending an action.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You gain +2 to initiative and advantage on concentration saves while holding a readied spell. Once per short rest, you may cast a spell of 2nd level or lower as a bonus action; if you do, you cannot take a reaction until the start of your next turn. When you roll initiative, you may bank one cantrip cast—release it on any later turn in the encounter without spending an action.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve Arcane Calculus OR Temporal Theory, readied-spell+2 initiative and concentration advantage. Define rank≤2 Bonus Action cast once per Short Rest, no-Reaction debt and expiry. Separately define initiative-banked cantrip setup/payment/one record/release on any later turn, target recheck and no free-copy or extra-turn loop."
```

### Preserved original source direction (historical)

```json
{
  "featId": "quickened_thought",
  "name": "Quickened Thought",
  "cohort": "magic_extended",
  "questionId": "MX-51",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/50",
  "originalQuestion": "Resolve Arcane Calculus OR Temporal Theory, readied-spell+2 initiative and concentration advantage. Define rank≤2 Bonus Action cast once per Short Rest, no-Reaction debt and expiry. Separately define initiative-banked cantrip setup/payment/one record/release on any later turn, target recheck and no free-copy or extra-turn loop.",
  "originalSourceObject": {
    "id": "quickened_thought",
    "name": "Quickened Thought",
    "description": "Your mind outpaces the tick of Aethel's clocks—ideas arrive finished in the Temporal Tower's shadow, as if tomorrow's spell were already written in today's breath. Prestige lineage: Chronomancer. completed from the existing development record.)",
    "prerequisite": "Intelligence 15+, Arcane Calculus or Temporal Theory",
    "effect": "You gain +2 to initiative and advantage on concentration saves while holding a readied spell. Once per short rest, you may cast a spell of 2nd level or lower as a bonus action; if you do, you cannot take a reaction until the start of your next turn. When you roll initiative, you may bank one cantrip cast—release it on any later turn in the encounter without spending an action.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You gain +2 to initiative and advantage on concentration saves while holding a readied spell. Once per short rest, you may cast a spell of 2nd level or lower as a bonus action; if you do, you cannot take a reaction until the start of your next turn. When you roll initiative, you may bank one cantrip cast—release it on any later turn in the encounter without spending an action.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "0d000584a8395778af19d53894037aed14421a1b82cf15552af4776f4d176bfc",
  "submittedProcedure": "Require INT 15 and (Arcane Calculus OR Temporal Theory). NEW resolve the grammatical scope as+2 initiative AND concentration-saveadvantage only while actually holding a readied spell; initiative is not recomputed later. Once SR/LR change an actually available normalActionspell of actualrank 0–2 to BA, paying every normal cost. From commitment until your next regular start you cannot commit anyReaction, even if the spell is countered; existing stacked Reactions finish. Separately, at first legitimate initiative roll of a real encounter, you may immediately prepare one legal normalActioncantrip as a non-action: pay components/independent RP/history, establish held concentration, open interruption, and use the same single pendingReady slot. NEW release that cantrip once withoutAction on one of your later own regular turns in that encounter, retaining actual concentration until then; target legality rechecks at release. This replaces any oldReady, ends at encounter end or lostconcentration, cannot be banked again by reroll/reentry, and shares the free-stored-release cap of one per owner/numbered round with Arcane Calculus. No extra cast/copy/proc at release.",
  "submittedNewChoices": "Both passivebonuses scoped to actual hold, one initial cantrip preparation and persistent no Reaction debt.",
  "submittedWorkedCases": [
    "A banked cantrip paid at initiative can release on your second regular turn withoutAction if concentration survives.",
    "Using theBAspell branch then leaves noReaction for Counterspell until the real next regular start."
  ],
  "decision": "Keep the source later-any-turn banked cantrip release rather than own-turn-only; it is between events, concentration-bound and shared-cap, not a free interrupt or extra turn.",
  "completeAuthoringProcedure": "Require INT 15 and (Arcane Calculus OR Temporal Theory). NEW resolve the grammatical scope as+2 initiative AND concentration-saveadvantage only while actually holding a readied spell; initiative is not recomputed later. Once SR/LR change an actually available normalActionspell of actualrank 0–2 to BA, paying every normal cost. From commitment until your next regular start you cannot commit anyReaction, even if the spell is countered; existing stacked Reactions finish. Separately, at first legitimate initiative roll of a real encounter, you may immediately prepare one legal normalActioncantrip as a non-action: pay components/independent RP/history, establish held concentration, open interruption, and use the same single pendingReady slot. NEW release that cantrip once without an Action on any later actual turn in that encounter, between completed events, retaining actual concentration until then; target legality rechecks at release. This replaces any oldReady, ends at encounter end or lostconcentration, cannot be banked again by reroll/reentry, and shares the free-stored-release cap of one per owner/numbered round with Arcane Calculus. No extra cast/copy/proc at release.\nNEW exact banked-cantrip release window supersedes a narrower own-turn-only draft: the held cantrip may be voluntarily released without an Action or Reaction on any later actual turn before its preserved Ready deadline, between completed events, not retroactively or as an interruption. Use the shared one free release per owner per numbered round; no extra turn is created. Holding still consumes the one actual concentration/Ready slot and its original costs/history. Arcane Calculus retains its expressly narrower next-own-regular-turn release window.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A banked cantrip paid at initiative can release on your second regular turn withoutAction if concentration survives.",
    "Using theBAspell branch then leaves noReaction for Counterspell until the real next regular start."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require INT 15 and (Arcane Calculus OR Temporal Theory). NEW resolve the grammatical scope as+2 initiative AND concentration-saveadvantage only while actually holding a readied spell; initiative is not recomputed later. Once SR/LR change an actually available normalActionspell of actualrank 0–2 to BA, paying every normal cost. From commitment until your next regular start you cannot commit anyReaction, even if the spell is countered; existing stacked Reactions finish. Separately, at first legitimate initiative roll of a real encounter, you may immediately prepare one legal normalActioncantrip as a non-action: pay components/independent RP/history, establish held concentration, open interruption, and use the same single pendingReady slot. NEW release that cantrip once without an Action on any later actual turn in that encounter, between completed events, retaining actual concentration until then; target legality rechecks at release. This replaces any oldReady, ends at encounter end or lostconcentration, cannot be banked again by reroll/reentry, and shares the free-stored-release cap of one per owner/numbered round with Arcane Calculus. No extra cast/copy/proc at release.
NEW exact banked-cantrip release window supersedes a narrower own-turn-only draft: the held cantrip may be voluntarily released without an Action or Reaction on any later actual turn before its preserved Ready deadline, between completed events, not retroactively or as an interruption. Use the shared one free release per owner per numbered round; no extra turn is created. Holding still consumes the one actual concentration/Ready slot and its original costs/history. Arcane Calculus retains its expressly narrower next-own-regular-turn release window.

### Original-position authored review references

```json
[
  {
    "id": "MX-51-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/20"
  },
  {
    "id": "MX-51-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/21"
  }
]
```

## MX-52 — Spell Reflection

### Complete original object

```json
{
  "id": "spell_reflection",
  "name": "Spell Reflection",
  "description": "What was sent returns wearing your sigil—mirrors do not forgive. Prestige lineage: Echomancer. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, level 8+",
  "effect": "Once per short rest, when you are targeted by a single-target spell, you may reflect it back at the caster as an immediate reaction (they make saving throws as if they had cast it on themselves). When you take spell damage, the attacker takes psychic damage equal to half the damage you received (once per round).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Once per short rest, when you are targeted by a single-target spell, you may reflect it back at the caster as an immediate reaction (they make saving throws as if they had cast it on themselves). When you take spell damage, the attacker takes psychic damage equal to half the damage you received (once per round).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define once-per-Short-Rest single-target redirect as an actual Reaction, caster target legality, original attack versus save/DC and recursion prevention. Separately define half-actual-spell-damage psychic retaliation once per round: attribution,range,rounding,resistance,zeroHP and repeated packets. Source text cannot automatically copy class/monster powers or all target riders."
```

### Preserved original source direction (historical)

```json
{
  "featId": "spell_reflection",
  "name": "Spell Reflection",
  "cohort": "magic_extended",
  "questionId": "MX-52",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/51",
  "originalQuestion": "Define once-per-Short-Rest single-target redirect as an actual Reaction, caster target legality, original attack versus save/DC and recursion prevention. Separately define half-actual-spell-damage psychic retaliation once per round: attribution,range,rounding,resistance,zeroHP and repeated packets. Source text cannot automatically copy class/monster powers or all target riders.",
  "originalSourceObject": {
    "id": "spell_reflection",
    "name": "Spell Reflection",
    "description": "What was sent returns wearing your sigil—mirrors do not forgive. Prestige lineage: Echomancer. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability, level 8+",
    "effect": "Once per short rest, when you are targeted by a single-target spell, you may reflect it back at the caster as an immediate reaction (they make saving throws as if they had cast it on themselves). When you take spell damage, the attacker takes psychic damage equal to half the damage you received (once per round).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "Once per short rest, when you are targeted by a single-target spell, you may reflect it back at the caster as an immediate reaction (they make saving throws as if they had cast it on themselves). When you take spell damage, the attacker takes psychic damage equal to half the damage you received (once per round).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "d0f609a26941f67277a95f8665445a16c19e51d123d4c4b13f8ce350ab7521e8",
  "submittedProcedure": "Once SR/LR spendReaction in Spell Deflection’s same pre-payload window when you are the sole creature target of an actual single-target spell. NEW redirect to the original caster only if that caster is a legal recipient under its own spell’s target/range/line rules; preserve original owner, rank, attackbonus, DC, payment and concentration. Resolve its original attack/save against itself; no automatic self-hit or invented save. Noarea, multi-target, copied/alreadyredirected or protectedpayload; an illegal caster-recipient makes this activation unavailable withoutpayment. Redirecting does not teach/capture the spell. Separately, once per numbered round after an owned hostile spell deals positive actualnumericdamage to you, the living personally perceived caster within 60 ft/line of effect takes psychicdamage=floor(actualDamageDealt/2). NEW this passive retaliation requires you stillalive after the complete packet, noReaction, excludes overkill and self/friendly/copy/reflection roots, and consumes at first qualifying packet even if half rounds 0. Ordinary psychicdefenses apply. It cannot itself reflect, capture, heal, generate RP or restart a damageproc; no summing multiple area victims.",
  "submittedNewChoices": "Legal original-caster redirect plus bounded 60 ft nonrecursive half-actual-damage retaliation.",
  "submittedWorkedCases": [
    "A hostile spell removes 3 HP from HP 3 despite 12 rawdamage: if you survive, retaliation is 1 psychic, not 6.",
    "A willing-only allybuff cannot be reflected into an unwilling original caster merely because it selected you."
  ],
  "decision": "Keep original caster ownership on redirection and bounded actual spell-damage reflection; no reflected copy, recursive retaliation, free spell or resource farming.",
  "completeAuthoringProcedure": "Once SR/LR spendReaction in Spell Deflection’s same pre-payload window when you are the sole creature target of an actual single-target spell. NEW redirect to the original caster only if that caster is a legal recipient under its own spell’s target/range/line rules; preserve original owner, rank, attackbonus, DC, payment and concentration. Resolve its original attack/save against itself; no automatic self-hit or invented save. Noarea, multi-target, copied/alreadyredirected or protectedpayload; an illegal caster-recipient makes this activation unavailable withoutpayment. Redirecting does not teach/capture the spell. Separately, once per numbered round after an owned hostile spell deals positive actualnumericdamage to you, the living personally perceived caster within 60 ft/line of effect takes psychicdamage=floor(actualDamageDealt/2). NEW this passive retaliation requires you stillalive after the complete packet, noReaction, excludes overkill and self/friendly/copy/reflection roots, and consumes at first qualifying packet even if half rounds 0. Ordinary psychicdefenses apply. It cannot itself reflect, capture, heal, generate RP or restart a damageproc; no summing multiple area victims.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A hostile spell removes 3 HP from HP 3 despite 12 rawdamage: if you survive, retaliation is 1 psychic, not 6.",
    "A willing-only allybuff cannot be reflected into an unwilling original caster merely because it selected you."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once SR/LR spendReaction in Spell Deflection’s same pre-payload window when you are the sole creature target of an actual single-target spell. NEW redirect to the original caster only if that caster is a legal recipient under its own spell’s target/range/line rules; preserve original owner, rank, attackbonus, DC, payment and concentration. Resolve its original attack/save against itself; no automatic self-hit or invented save. Noarea, multi-target, copied/alreadyredirected or protectedpayload; an illegal caster-recipient makes this activation unavailable withoutpayment. Redirecting does not teach/capture the spell. Separately, once per numbered round after an owned hostile spell deals positive actualnumericdamage to you, the living personally perceived caster within 60 ft/line of effect takes psychicdamage=floor(actualDamageDealt/2). NEW this passive retaliation requires you stillalive after the complete packet, noReaction, excludes overkill and self/friendly/copy/reflection roots, and consumes at first qualifying packet even if half rounds 0. Ordinary psychicdefenses apply. It cannot itself reflect, capture, heal, generate RP or restart a damageproc; no summing multiple area victims.

### Original-position authored review references

```json
[
  {
    "id": "MX-52-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/22"
  },
  {
    "id": "MX-52-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/23"
  }
]
```

## MX-53 — Stormcaller

### Complete original object

```json
{
  "id": "stormcaller",
  "name": "Stormcaller",
  "description": "You whistle up weather like a shepherd calls dogs—clouds come hungry. Prestige lineage: Storm Lord. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, proficiency in Nature or Spellcraft",
  "effect": "You can create a 15-foot Static Field as an action (once per short rest): creatures entering or starting their turn there take 1d6 lightning damage and have disadvantage on Dexterity saves until they leave the field. Once per short rest, you may Stormstep up to 30 feet to a target you can see, dealing 1d8 thunder damage to adjacent creatures and leaving a crackling afterimage that grants you half cover until the start of your next turn. While outdoors during a storm, your Static Field radius increases to 20 feet and lightning spells you cast ignore the first instance of half cover between you and the target.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You can create a 15-foot Static Field as an action (once per short rest): creatures entering or starting their turn there take 1d6 lightning damage and have disadvantage on Dexterity saves until they leave the field. Once per short rest, you may Stormstep up to 30 feet to a target you can see, dealing 1d8 thunder damage to adjacent creatures and leaving a crackling afterimage that grants you half cover until the start of your next turn. While outdoors during a storm, your Static Field radius increases to 20 feet and lightning spells you cast ignore the first instance of half cover between you and the target.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve Nature OR undefined Spellcraft credential. Define15ft Static Field radius/placement/duration/concentration, entry/start cadence, damage/save and DEX-save-disadvantage ending, plus storm20ft variant. Separately define30ft Stormstep action/legal space,1d8 adjacent-thunder targets/save and afterimage half-cover geometry; two Short Rest ledgers and cover bypass stay distinct."
```

### Preserved original source direction (historical)

```json
{
  "featId": "stormcaller",
  "name": "Stormcaller",
  "cohort": "magic_extended",
  "questionId": "MX-53",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/52",
  "originalQuestion": "Resolve Nature OR undefined Spellcraft credential. Define15ft Static Field radius/placement/duration/concentration, entry/start cadence, damage/save and DEX-save-disadvantage ending, plus storm20ft variant. Separately define30ft Stormstep action/legal space,1d8 adjacent-thunder targets/save and afterimage half-cover geometry; two Short Rest ledgers and cover bypass stay distinct.",
  "originalSourceObject": {
    "id": "stormcaller",
    "name": "Stormcaller",
    "description": "You whistle up weather like a shepherd calls dogs—clouds come hungry. Prestige lineage: Storm Lord. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability, proficiency in Nature or Spellcraft",
    "effect": "You can create a 15-foot Static Field as an action (once per short rest): creatures entering or starting their turn there take 1d6 lightning damage and have disadvantage on Dexterity saves until they leave the field. Once per short rest, you may Stormstep up to 30 feet to a target you can see, dealing 1d8 thunder damage to adjacent creatures and leaving a crackling afterimage that grants you half cover until the start of your next turn. While outdoors during a storm, your Static Field radius increases to 20 feet and lightning spells you cast ignore the first instance of half cover between you and the target.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You can create a 15-foot Static Field as an action (once per short rest): creatures entering or starting their turn there take 1d6 lightning damage and have disadvantage on Dexterity saves until they leave the field. Once per short rest, you may Stormstep up to 30 feet to a target you can see, dealing 1d8 thunder damage to adjacent creatures and leaving a crackling afterimage that grants you half cover until the start of your next turn. While outdoors during a storm, your Static Field radius increases to 20 feet and lightning spells you cast ignore the first instance of half cover between you and the target.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "2e321e17129a273ff26e821f76db500763e56e2ce5fe7130495abc5f61d1881b",
  "submittedProcedure": "Require actual spellcasting AND (Nature proficiency OR a separately established Spellcraft credential). Spellcraft is not an Arcana alias; if absent, use the Nature alternative. Once per beneficial SR/LR, an Action places a fixed 15 ft radius Static Field at a perceived point within 60 ft and line of effect, requiring concentration for up to one minute. It affects all creatures, including allies: first actual entry or regular start inside per target per numbered round deals 1d6 lightning automatically. Placement covering a creature counts as entry once. While inside an active field, creatures have disadvantage on DEX saves, ending immediately on exit; actual immunities/suppression apply. Outdoors during an established storm, choose a 20 ft radius at creation. A separate once-SR/LR Action, Stormstep, teleports you up to 30 ft to a visible fitting unoccupied space with line of effect. Every other creature within 5 ft of arrival makes a DEX save against your actual casting DC for 1d8 thunder, half on success. NEW select the actual owned casting route at acquisition for both feat activations. Your afterimage supplies half cover until your next regular start only when the geometric ray from the incoming effect origin to your new position passes through your previous occupied space; it is not a solid object or general AC bonus. During an actual outdoor storm, your lightning spells also ignore half cover, but not stronger cover. These activations are nonspell magical feat techniques; they do not create weather, RP or extra casting resources.",
  "submittedNewChoices": "TwoAction activations/ledgers, fixedconcentrationfield, explicit automaticpulse and directionalafterimage.",
  "submittedWorkedCases": [
    "Entering then exiting/reentering thefield inoneround deals onlyonepulse tothatcreature.",
    "A normalrainstorm canqualifyif theDirector’s actualweatherrecord saysstorm; thefeat doesnotdeclareone."
  ],
  "decision": "Adopt finite static field/Stormstep nonspell techniques with actual owned casting route and Nature-or-real-Spellcraft prerequisite; explicitly fix20ft storm radius at creation.",
  "completeAuthoringProcedure": "Require actual spellcasting AND (Nature proficiency OR a separately established Spellcraft credential). Spellcraft is not an Arcana alias; if absent, use the Nature alternative. Once per beneficial SR/LR, an Action places a fixed 15 ft radius Static Field at a perceived point within 60 ft and line of effect, requiring concentration for up to one minute. It affects all creatures, including allies: first actual entry or regular start inside per target per numbered round deals 1d6 lightning automatically. Placement covering a creature counts as entry once. While inside an active field, creatures have disadvantage on DEX saves, ending immediately on exit; actual immunities/suppression apply. Outdoors during an established storm, choose a 20 ft radius at creation. A separate once-SR/LR Action, Stormstep, teleports you up to 30 ft to a visible fitting unoccupied space with line of effect. Every other creature within 5 ft of arrival makes a DEX save against your actual casting DC for 1d8 thunder, half on success. NEW select the actual owned casting route at acquisition for both feat activations. Your afterimage supplies half cover until your next regular start only when the geometric ray from the incoming effect origin to your new position passes through your previous occupied space; it is not a solid object or general AC bonus. During an actual outdoor storm, your lightning spells also ignore half cover, but not stronger cover. These activations are nonspell magical feat techniques; they do not create weather, RP or extra casting resources.\nNEW storm-size choice is fixed at creation, as this proposal specifies:20ft requires actual outdoor-storm premises at that placement. A later weather change does not enlarge or shrink the placed field; suppression, concentration and its original minute deadline still end it. The separate half-cover benefit checks the actual outdoor-storm predicate when each lightning spell attack resolves. These are source-authoring completions, not permission to interpret the named storm’s setting origin.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Entering then exiting/reentering thefield inoneround deals onlyonepulse tothatcreature.",
    "A normalrainstorm canqualifyif theDirector’s actualweatherrecord saysstorm; thefeat doesnotdeclareone."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual spellcasting AND (Nature proficiency OR a separately established Spellcraft credential). Spellcraft is not an Arcana alias; if absent, use the Nature alternative. Once per beneficial SR/LR, an Action places a fixed 15 ft radius Static Field at a perceived point within 60 ft and line of effect, requiring concentration for up to one minute. It affects all creatures, including allies: first actual entry or regular start inside per target per numbered round deals 1d6 lightning automatically. Placement covering a creature counts as entry once. While inside an active field, creatures have disadvantage on DEX saves, ending immediately on exit; actual immunities/suppression apply. Outdoors during an established storm, choose a 20 ft radius at creation. A separate once-SR/LR Action, Stormstep, teleports you up to 30 ft to a visible fitting unoccupied space with line of effect. Every other creature within 5 ft of arrival makes a DEX save against your actual casting DC for 1d8 thunder, half on success. NEW select the actual owned casting route at acquisition for both feat activations. Your afterimage supplies half cover until your next regular start only when the geometric ray from the incoming effect origin to your new position passes through your previous occupied space; it is not a solid object or general AC bonus. During an actual outdoor storm, your lightning spells also ignore half cover, but not stronger cover. These activations are nonspell magical feat techniques; they do not create weather, RP or extra casting resources.
NEW storm-size choice is fixed at creation, as this proposal specifies:20ft requires actual outdoor-storm premises at that placement. A later weather change does not enlarge or shrink the placed field; suppression, concentration and its original minute deadline still end it. The separate half-cover benefit checks the actual outdoor-storm predicate when each lightning spell attack resolves. These are source-authoring completions, not permission to interpret the named storm’s setting origin.

### Original-position authored review references

```json
[
  {
    "id": "MX-53-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/24"
  },
  {
    "id": "MX-53-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/25"
  }
]
```

## MX-54 — Temporal Theory

### Complete original object

```json
{
  "id": "temporal_theory",
  "name": "Temporal Theory",
  "description": "Time is not a river—it is a ledger. You have learned to borrow from tomorrow and repay in fatigue. Prestige lineage: Chronomancer. completed from the existing development record.)",
  "prerequisite": "Intelligence 15+, proficiency in Arcana, level 8+",
  "effect": "At the end of your turn, you may bank one unused action (move, object interaction, or bonus action if available), storing up to 2 banked actions. Spend banked actions on later turns. After spending 2 banked actions in one encounter, you gain one level of fatigue when combat ends.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "At the end of your turn, you may bank one unused action (move, object interaction, or bonus action if available), storing up to 2 banked actions. Spend banked actions on later turns. After spending 2 banked actions in one encounter, you gain one level of fatigue when combat ends.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define unused move/object-interaction/Bonus Action as actual existing separate budgets, not an interchangeable Action. Specify end-turn banking,max2,expiry/type-preserving spending on later turns,no overlap/double-spend and real movement units. Resolve after2spent-per-encounter fatigue as an actual condition, timing and recovery. No action generation, extra turns or unfinished Time Loop activation."
```

### Preserved original source direction (historical)

```json
{
  "featId": "temporal_theory",
  "name": "Temporal Theory",
  "cohort": "magic_extended",
  "questionId": "MX-54",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/53",
  "originalQuestion": "Define unused move/object-interaction/Bonus Action as actual existing separate budgets, not an interchangeable Action. Specify end-turn banking,max2,expiry/type-preserving spending on later turns,no overlap/double-spend and real movement units. Resolve after2spent-per-encounter fatigue as an actual condition, timing and recovery. No action generation, extra turns or unfinished Time Loop activation.",
  "originalSourceObject": {
    "id": "temporal_theory",
    "name": "Temporal Theory",
    "description": "Time is not a river—it is a ledger. You have learned to borrow from tomorrow and repay in fatigue. Prestige lineage: Chronomancer. completed from the existing development record.)",
    "prerequisite": "Intelligence 15+, proficiency in Arcana, level 8+",
    "effect": "At the end of your turn, you may bank one unused action (move, object interaction, or bonus action if available), storing up to 2 banked actions. Spend banked actions on later turns. After spending 2 banked actions in one encounter, you gain one level of fatigue when combat ends.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "At the end of your turn, you may bank one unused action (move, object interaction, or bonus action if available), storing up to 2 banked actions. Spend banked actions on later turns. After spending 2 banked actions in one encounter, you gain one level of fatigue when combat ends.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "8a452260e4a24a0c67efea565e1705a45b7d25570a6d86bedd55f11720c73d9b",
  "submittedProcedure": "At your original regular-turn end, bank at most one genuinely unused NORMAL allowance: your wholly unspent movement budget, ordinary free object interaction, or unused ordinary Bonus Action. You must be conscious, able to act and actually possess it; prohibited, extra, borrowed, banked, readied or generated allowances cannot fund a token. Movement requires zero movement spent this turn; snapshot actual legal distance and modes. Consume the chosen allowance into one typed token; hold at most two, expiring at encounter end. On a later own regular turn, spend at most one token of each type without Action for its exact purpose: move up to min(stored feet, current legal normal Speed), one ordinary interaction, or one currently legal BA ability. Pay current terrain; modes must still exist. No conversion to full Action, Reaction, work time or new token, and no refresh of feature uses/cadences. After the second token spent in the real encounter, record one irrevocable fatigue cost due at encounter end: NEW one Core Exhaustion level, with actual immunity/recovery and lethal level 6 rules. Further spending creates no extra fatigue under this source but cannot erase the cost. No Time Loop, rewind or resource restoration.",
  "submittedNewChoices": "Typed ordinary allowances, regular-turn banking, finite expiry and explicit Core Exhaustion translation.",
  "submittedWorkedCases": [
    "Store a wholly unused 30 ft movement allowance. If current Speed is 20 when later spent, it supplies at most 20 additional feet, with current terrain costs.",
    "A Bonus Action supplied by Mystic Recoil cannot be banked into a persistent token."
  ],
  "decision": "Adopt two recorded unused native-budget tokens and one end-encounter Exhaustion cost after spending two; no generated budget rebanking, erased spent movement or Strain alias.",
  "completeAuthoringProcedure": "At your original regular-turn end, bank at most one genuinely unused NORMAL allowance: your wholly unspent movement budget, ordinary free object interaction, or unused ordinary Bonus Action. You must be conscious, able to act and actually possess it; prohibited, extra, borrowed, banked, readied or generated allowances cannot fund a token. Movement requires zero movement spent this turn; snapshot actual legal distance and modes. Consume the chosen allowance into one typed token; hold at most two, expiring at encounter end. On a later own regular turn, spend at most one token of each type without Action for its exact purpose: move up to min(stored feet, current legal normal Speed), one ordinary interaction, or one currently legal BA ability. Pay current terrain; modes must still exist. No conversion to full Action, Reaction, work time or new token, and no refresh of feature uses/cadences. After the second token spent in the real encounter, record one irrevocable fatigue cost due at encounter end: NEW one Core Exhaustion level, with actual immunity/recovery and lethal level 6 rules. Further spending creates no extra fatigue under this source but cannot erase the cost. No Time Loop, rewind or resource restoration.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Store a wholly unused 30 ft movement allowance. If current Speed is 20 when later spent, it supplies at most 20 additional feet, with current terrain costs.",
    "A Bonus Action supplied by Mystic Recoil cannot be banked into a persistent token."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At your original regular-turn end, bank at most one genuinely unused NORMAL allowance: your wholly unspent movement budget, ordinary free object interaction, or unused ordinary Bonus Action. You must be conscious, able to act and actually possess it; prohibited, extra, borrowed, banked, readied or generated allowances cannot fund a token. Movement requires zero movement spent this turn; snapshot actual legal distance and modes. Consume the chosen allowance into one typed token; hold at most two, expiring at encounter end. On a later own regular turn, spend at most one token of each type without Action for its exact purpose: move up to min(stored feet, current legal normal Speed), one ordinary interaction, or one currently legal BA ability. Pay current terrain; modes must still exist. No conversion to full Action, Reaction, work time or new token, and no refresh of feature uses/cadences. After the second token spent in the real encounter, record one irrevocable fatigue cost due at encounter end: NEW one Core Exhaustion level, with actual immunity/recovery and lethal level 6 rules. Further spending creates no extra fatigue under this source but cannot erase the cost. No Time Loop, rewind or resource restoration.

### Original-position authored review references

```json
[
  {
    "id": "MX-54-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/26"
  },
  {
    "id": "MX-54-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/27"
  }
]
```

## MX-55 — Trapcasting

### Complete original object

```json
{
  "id": "trapcasting",
  "name": "Trapcasting",
  "description": "Roots, thorns, and spore-mines—you sow violence that waits patiently to bloom. Prestige lineage: Verdant Animist. completed from the existing development record.)",
  "prerequisite": "Conjure Flora or Verdant Bond",
  "effect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot area, 2d6 damage, type chosen at conjuring).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot AoE, 2d6 damage, type chosen at conjuring).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve Conjure Flora OR Verdant Bond gate without granting seedlings by implication. Define source seedling trap mode, real hostile entry/forced movement, save/DC/cadence/damage/restraint/poison duration and detection/disarm. Bind Bonus Action detonation consuming exactly one seedling,10ft geometry,2d6 chosen type,targets/save and conservation with existing commands/expiry."
```

### Preserved original source direction (historical)

```json
{
  "featId": "trapcasting",
  "name": "Trapcasting",
  "cohort": "magic_extended",
  "questionId": "MX-55",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/54",
  "originalQuestion": "Preserve Conjure Flora OR Verdant Bond gate without granting seedlings by implication. Define source seedling trap mode, real hostile entry/forced movement, save/DC/cadence/damage/restraint/poison duration and detection/disarm. Bind Bonus Action detonation consuming exactly one seedling,10ft geometry,2d6 chosen type,targets/save and conservation with existing commands/expiry.",
  "originalSourceObject": {
    "id": "trapcasting",
    "name": "Trapcasting",
    "description": "Roots, thorns, and spore-mines—you sow violence that waits patiently to bloom. Prestige lineage: Verdant Animist. completed from the existing development record.)",
    "prerequisite": "Conjure Flora or Verdant Bond",
    "effect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot area, 2d6 damage, type chosen at conjuring).",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot AoE, 2d6 damage, type chosen at conjuring).",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "00d62e8310000da8a9ae745e5b75891605f674e8ef0e541927d672643e221ddf",
  "submittedProcedure": "Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.",
  "submittedNewChoices": "Exact plant eligibility, one shared offensive allowance, entry/disarm procedure and body-consuming burst.",
  "submittedWorkedCases": [
    "Forced hostile entry can trigger a plant, but another plant cannot produce a second offensive outcome after the group allowance is spent that round.",
    "Detonation consumes the actual plant even if every creature saves. An expired plant cannot be detonated."
  ],
  "decision": "Adopt entry-trigger/burst exceptions explicitly spending the same one owner-round offensive-companion allowance as ordinary plant commands; no simultaneous free offense or recreated plants.",
  "completeAuthoringProcedure": "Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.\nNEW phase exception is explicit: its first eligible hostile-entry attack may occur on that actual entry outside the ordinary attached phase, but spends the same owner-round offensive companion allowance immediately. Its paid burst likewise spends that allowance; neither can occur when it is already spent. Placement itself is not an entry-trigger unless this exact procedure expressly says so. General Conjure Flora commands retain their attached phase, shared Bonus Action and sensory channel.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Forced hostile entry can trigger a plant, but another plant cannot produce a second offensive outcome after the group allowance is spent that round.",
    "Detonation consumes the actual plant even if every creature saves. An expired plant cannot be detonated."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.
NEW phase exception is explicit: its first eligible hostile-entry attack may occur on that actual entry outside the ordinary attached phase, but spends the same owner-round offensive companion allowance immediately. Its paid burst likewise spends that allowance; neither can occur when it is already spent. Placement itself is not an entry-trigger unless this exact procedure expressly says so. General Conjure Flora commands retain their attached phase, shared Bonus Action and sensory channel.
FEAT335-FLORA-SOURCE-CHECK-01 interface binding. Apply Conjure Flora's FLQ-01 provider and FLQ-04 owner/instance continuity completions to these actual Flora bodies. A valid earlier acquisition remains necessary, but continuing possession or immediate usability of its original casting provider is not an additional trap prerequisite. The entry exception is automatic only as already specified; it needs no new command and does not require a living/conscious owner, but uses that same owner's conserved numbered-round offensive allowance. A legally committed ordinary Flora command already spends that allowance before its attached phase, so entry cannot steal or duplicate it. A new personal Bloom Burst still requires its legal Bonus Action, perception, range, line of effect and unspent shared allowance. Ending the first plant by a Burst closes any unused second-creation window; a second plant already created keeps its own original deadline. Verdant Bond-only ownership still creates no Flora body or casting provider, and no new unreviewed conjured-plant profile is admitted.

### Original-position authored review references

```json
[
  {
    "id": "MX-55-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/28"
  },
  {
    "id": "MX-55-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/29"
  }
]
```

## MX-56 — Verdant Bond

### Complete original object

```json
{
  "id": "verdant_bond",
  "name": "Verdant Bond",
  "description": "The green speaks to you in sap and silence. You answer with growth. Prestige lineage: Verdant Animist. completed from the existing development record.)",
  "prerequisite": "Proficiency in Nature, spellcasting ability",
  "effect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve simple plant communication/coarse sensations within60ft, Nature advantage in wilderness, active-flora+1 nature spell DC/attacks, plant-terrain movement and24-hour stored warning. Define finite eligible natural-spell predicate,actual senses/knowledge,one stand/message/ally trigger and costs. No universal sentience, omniscient plants, new conjuration or cosmology review."
```

### Preserved original source direction (historical)

```json
{
  "featId": "verdant_bond",
  "name": "Verdant Bond",
  "cohort": "magic_extended",
  "questionId": "MX-56",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/55",
  "originalQuestion": "Preserve simple plant communication/coarse sensations within60ft, Nature advantage in wilderness, active-flora+1 nature spell DC/attacks, plant-terrain movement and24-hour stored warning. Define finite eligible natural-spell predicate,actual senses/knowledge,one stand/message/ally trigger and costs. No universal sentience, omniscient plants, new conjuration or cosmology review.",
  "originalSourceObject": {
    "id": "verdant_bond",
    "name": "Verdant Bond",
    "description": "The green speaks to you in sap and silence. You answer with growth. Prestige lineage: Verdant Animist. completed from the existing development record.)",
    "prerequisite": "Proficiency in Nature, spellcasting ability",
    "effect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "f78aa83ed9e26c223772d8ab455bb18bc2a09a238ba069aa7af28f91158404e2",
  "submittedProcedure": "While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Current strongest same-stat bonus applies. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.",
  "submittedNewChoices": "Explicit class-route Nature predicate and one-shot 25 word stored message.",
  "submittedWorkedCases": [
    "With an active plant, a spell actually cast through the Ranger route may receive the proposed +1 DC, subject to strongest-bonus arbitration.",
    "The stored message is audible to anyone close enough to hear when the designated ally triggers it."
  ],
  "decision": "Adopt actual plant-linked Druid/Ranger/Shaman route bonus and one finite real audible message; include owner as an eligible ally, preserve LAX evidence and original spell access.",
  "completeAuthoringProcedure": "While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Distinct eligible flat feat bonuses add under FS-03; this same feat contributes only once. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.\nSOURCE ally scope: the owner may be the one chosen message recipient. It triggers on that recipient’s first genuinely future qualifying passage after recording, not immediate creation beside the tree; the audible stored message is not private telepathy or general tree fluency.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "With an active qualifying plant, a spell actually cast through the Ranger route gains the stated+1DC. An independently acquired eligible Spell Focus+1 adds, for+2total; duplicate Verdant Bond does not.",
    "The stored message is audible to anyone close enough to hear when the designated ally triggers it."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Distinct eligible flat feat bonuses add under FS-03; this same feat contributes only once. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.
SOURCE ally scope: the owner may be the one chosen message recipient. It triggers on that recipient’s first genuinely future qualifying passage after recording, not immediate creation beside the tree; the audible stored message is not private telepathy or general tree fluency.

### Original-position authored review references

```json
[
  {
    "id": "MX-56-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/30"
  },
  {
    "id": "MX-56-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/31"
  }
]
```

## MX-57 — Voltyros Pact

### Complete original object

```json
{
  "id": "voltyros_pact",
  "name": "Voltyros Pact",
  "description": "You bargained with the Plane of Storms itself—Voltyros marks you with copper taste and crown-light. Prestige lineage: Storm Lord. completed from the existing development record.)",
  "prerequisite": "Stormcaller or Lightning Affinity, level 6+",
  "effect": "Your lightning spells chain to one additional target within 15 feet for half damage. While you remain stationary for a full round, you gain resistance to all damage until the start of your next turn and +2 to spell damage (Eye of the Tempest). Once per long rest, you may call a stormform burst: 30-foot line of lightning for 4d6 damage.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Your lightning spells chain to one additional target within 15 feet for half damage. While you remain stationary for a full round, you gain resistance to all damage until the start of your next turn and +2 to spell damage (Eye of the Tempest). Once per long rest, you may call a stormform burst: 30-foot line of lightning for 4d6 damage.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve Stormcaller OR Lightning Affinity pluslevel6 mechanically while preserving the named pact/plane text for post-push review. Define one extra target15ft/half-lightning damage,actual chain eligibility and no recursion. Define a stationary full-round marker, forced movement, all-damage resistance endpoint,+2 spell damage packet; define30ft4d6 line activation,save/DC,width and Long Rest use."
```

### Preserved original source direction (historical)

```json
{
  "featId": "voltyros_pact",
  "name": "Voltyros Pact",
  "cohort": "magic_extended",
  "questionId": "MX-57",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/56",
  "originalQuestion": "Resolve Stormcaller OR Lightning Affinity pluslevel6 mechanically while preserving the named pact/plane text for post-push review. Define one extra target15ft/half-lightning damage,actual chain eligibility and no recursion. Define a stationary full-round marker, forced movement, all-damage resistance endpoint,+2 spell damage packet; define30ft4d6 line activation,save/DC,width and Long Rest use.",
  "originalSourceObject": {
    "id": "voltyros_pact",
    "name": "Voltyros Pact",
    "description": "You bargained with the Plane of Storms itself—Voltyros marks you with copper taste and crown-light. Prestige lineage: Storm Lord. completed from the existing development record.)",
    "prerequisite": "Stormcaller or Lightning Affinity, level 6+",
    "effect": "Your lightning spells chain to one additional target within 15 feet for half damage. While you remain stationary for a full round, you gain resistance to all damage until the start of your next turn and +2 to spell damage (Eye of the Tempest). Once per long rest, you may call a stormform burst: 30-foot line of lightning for 4d6 damage.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "Your lightning spells chain to one additional target within 15 feet for half damage. While you remain stationary for a full round, you gain resistance to all damage until the start of your next turn and +2 to spell damage (Eye of the Tempest). Once per long rest, you may call a stormform burst: 30-foot line of lightning for 4d6 damage.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "550f930a364ef57b28b12cb3288bea92900569ae98316fa3013906c4bb50a7b8",
  "submittedProcedure": "Require character 6 AND (Stormcaller OR Lightning Affinity); preserve the named pact/plane story undecided. Once per personal noncopy lightning spell’s initial resolution, choose one additional creature within 15 ft of one original recipient, perceived with line of effect from that recipient. It must satisfy original creature eligibility and not already be targeted by that cast. Deal only half the selected original native lightning packet before defenses, rounded down; use the original DC/save ability for a fresh save or original attack bonus for a fresh attack, with original half/none on success. No other riders, new cast or chain from a chain. After one entire original start-to-next-start interval without any position change, gain Eye of the Tempest: resistance to all damage and+2 to one immediate native packet/shared roll of each personal spell until the following regular start. Any movement, teleport or forced displacement ends Eye immediately; riding a moving mount counts as movement. Repeated stationary intervals may renew without stacking. Separately, once LR use Action for a 30 ft-long 5 ft-wide lightning line: all creatures DEX save,4d6 lightning half success. DC=8+PB+one actual casting ability selected at acquisition, or INT if no casting source. The line is a magical nonspell feat technique, with noRPpool or weather creation.",
  "submittedNewChoices": "One lightning-only chain, exact stationary interval and complete nonspell line profile.",
  "submittedWorkedCases": [
    "Native 17 lightning damage gives a chain base of 8 before the new target’s save and defenses; that child cannot chain again.",
    "Forced movement prevents the stationary interval. Riding a moving mount is not stationary."
  ],
  "decision": "Adopt bounded one additional lightning recipient, actual stationary Eye interval and separate finite line; keep the printed+2 personal spell scope, no weather, RP or plane-origin grant.",
  "completeAuthoringProcedure": "Require character 6 AND (Stormcaller OR Lightning Affinity); preserve the named pact/plane story undecided. Once per personal noncopy lightning spell’s initial resolution, choose one additional creature within 15 ft of one original recipient, perceived with line of effect from that recipient. It must satisfy original creature eligibility and not already be targeted by that cast. Deal only half the selected original native lightning packet before defenses, rounded down; use the original DC/save ability for a fresh save or original attack bonus for a fresh attack, with original half/none on success. No other riders, new cast or chain from a chain. After one entire original start-to-next-start interval without any position change, gain Eye of the Tempest: resistance to all damage and+2 to one immediate native packet/shared roll of each personal spell until the following regular start. Any movement, teleport or forced displacement ends Eye immediately; riding a moving mount counts as movement. Repeated stationary intervals may renew without stacking. Separately, once LR use Action for a 30 ft-long 5 ft-wide lightning line: all creatures DEX save,4d6 lightning half success. DC=8+PB+one actual casting ability selected at acquisition, or INT if no casting source. The line is a magical nonspell feat technique, with noRPpool or weather creation.\nThe Eye bonus is+2 to one immediate native packet/shared roll of each personal spell as printed here; it is not limited to lightning spells. Half-damage chaining uses a resolved native lightning packet, not an attack that missed, a reflected/copy result, external rider or new target-independent resource event. Existing stance, terrain, body and actual stationary interval rules remain.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Native 17 lightning damage gives a chain base of 8 before the new target’s save and defenses; that child cannot chain again.",
    "Forced movement prevents the stationary interval. Riding a moving mount is not stationary."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require character 6 AND (Stormcaller OR Lightning Affinity); preserve the named pact/plane story undecided. Once per personal noncopy lightning spell’s initial resolution, choose one additional creature within 15 ft of one original recipient, perceived with line of effect from that recipient. It must satisfy original creature eligibility and not already be targeted by that cast. Deal only half the selected original native lightning packet before defenses, rounded down; use the original DC/save ability for a fresh save or original attack bonus for a fresh attack, with original half/none on success. No other riders, new cast or chain from a chain. After one entire original start-to-next-start interval without any position change, gain Eye of the Tempest: resistance to all damage and+2 to one immediate native packet/shared roll of each personal spell until the following regular start. Any movement, teleport or forced displacement ends Eye immediately; riding a moving mount counts as movement. Repeated stationary intervals may renew without stacking. Separately, once LR use Action for a 30 ft-long 5 ft-wide lightning line: all creatures DEX save,4d6 lightning half success. DC=8+PB+one actual casting ability selected at acquisition, or INT if no casting source. The line is a magical nonspell feat technique, with noRPpool or weather creation.
The Eye bonus is+2 to one immediate native packet/shared roll of each personal spell as printed here; it is not limited to lightning spells. Half-damage chaining uses a resolved native lightning packet, not an attack that missed, a reflected/copy result, external rider or new target-independent resource event. Existing stance, terrain, body and actual stationary interval rules remain.

### Original-position authored review references

```json
[
  {
    "id": "MX-57-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/32"
  },
  {
    "id": "MX-57-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/33"
  }
]
```

## MX-58 — Wounding Magic

### Complete original object

```json
{
  "id": "wounding_magic",
  "name": "Wounding Magic",
  "description": "Your spells leave wounds that resist closure—pain that outlasts the casting. Prestige lineage: Soulrender. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability",
  "effect": "When you deal damage with a spell, you may leave an Agony wound: the target takes 1d4 necrotic damage at the start of each of its turns for 3 rounds (save ends). Wounded targets have disadvantage on Constitution saves to regain hit points and on saves against resurrection effects.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you deal damage with a spell, you may leave an Agony wound: the target takes 1d4 necrotic damage at the start of each of its turns for 3 rounds (save ends). Wounded targets have disadvantage on Constitution saves to regain hit points and on saves against resurrection effects.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Define optional spell-damage Agony application,frequency,target/source ledger,1d4 necrotic start pulses,3round duration,save ability/DC and cure/suppression. Define disadvantage only on actual existing CON healing/resurrection saves and compatibility with Wounded/true-healing gates. No invented healing save, resurrection permission or soul taxonomy; secondary damage cannot recursively create wounds."
```

### Preserved original source direction (historical)

```json
{
  "featId": "wounding_magic",
  "name": "Wounding Magic",
  "cohort": "magic_extended",
  "questionId": "MX-58",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json",
  "sourceFileSha256": "e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380",
  "sourcePointer": "/records/57",
  "originalQuestion": "Define optional spell-damage Agony application,frequency,target/source ledger,1d4 necrotic start pulses,3round duration,save ability/DC and cure/suppression. Define disadvantage only on actual existing CON healing/resurrection saves and compatibility with Wounded/true-healing gates. No invented healing save, resurrection permission or soul taxonomy; secondary damage cannot recursively create wounds.",
  "originalSourceObject": {
    "id": "wounding_magic",
    "name": "Wounding Magic",
    "description": "Your spells leave wounds that resist closure—pain that outlasts the casting. Prestige lineage: Soulrender. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability",
    "effect": "When you deal damage with a spell, you may leave an Agony wound: the target takes 1d4 necrotic damage at the start of each of its turns for 3 rounds (save ends). Wounded targets have disadvantage on Constitution saves to regain hit points and on saves against resurrection effects.",
    "type": "Magic",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you deal damage with a spell, you may leave an Agony wound: the target takes 1d4 necrotic damage at the start of each of its turns for 3 rounds (save ends). Wounded targets have disadvantage on Constitution saves to regain hit points and on saves against resurrection effects.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "23951a1ccf9e256e5eb5ebfa31efc8fc9a5e8d6a8e37f5e184bfad4384e8ebb4",
  "submittedProcedure": "After your personally cast noncopy spell deals positive resolved damage, optionally apply one Agony record to one living damaged target, once per owner/target/numbered round. Reapplication refreshes one profile without stacked dice. It deals 1d4 necrotic at the next three original target regular-start markers; a CON save against the generating cast DC at each affected regular end, including a current turn if applicable, ends it. The final third scheduled pulse ends the record after damage; no extra ending save afterward. It is a magical ongoing wound, not Core Wound, maximum HP injury or Bleeding by name. NEW a legal positive-potential magical heal or Action Medicine vs source DC ends it; suppressed records remain curable. While active, disadvantage applies only to actual existing CON saves to regain HP and actual saves against resurrection effects; no such save is invented. Death suspends living damage, retaining only the unexpired record tied to that exact death instance until the original third-start deadline; missed pulses are consumed, never backlogged. A legal revival closes that corpse-specific resurrection rider and retains only any still-future living pulse schedule until cured/expired. This grants no resurrection block or permission. Secondary ticks cannot create further Agony, copies, lifesteal or resource procs. Any independent Necrotic Affinity seal needs its own real fatal-root predicate.",
  "submittedNewChoices": "Three actual scheduled pulses, bounded death-instance rider, explicit cure and actual-save-only disadvantage.",
  "submittedWorkedCases": [
    "The first 1d4 pulse resolves at the target’s regular start; a successful CON save at its regular end removes the remaining pulses.",
    "A normal heal with no save gains no new saving throw. Death skips living pulses without extending the original deadline or granting resurrection permission."
  ],
  "decision": "Adopt separate three-tick spell Agony with exact immunity/cure/deadline metadata, not Core Wounds, extra spell casts or an invented healing saving throw.",
  "completeAuthoringProcedure": "After your personally cast noncopy spell deals positive resolved damage, optionally apply one Agony record to one living damaged target, once per owner/target/numbered round. Reapplication refreshes one profile without stacked dice. It deals 1d4 necrotic at the next three original target regular-start markers; a CON save against the generating cast DC at each affected regular end, including a current turn if applicable, ends it. The final third scheduled pulse ends the record after damage; no extra ending save afterward. It is a magical ongoing wound, not Core Wound, maximum HP injury or Bleeding by name. NEW a legal positive-potential magical heal or Action Medicine vs source DC ends it; suppressed records remain curable. While active, disadvantage applies only to actual existing CON saves to regain HP and actual saves against resurrection effects; no such save is invented. Death suspends living damage, retaining only the unexpired record tied to that exact death instance until the original third-start deadline; missed pulses are consumed, never backlogged. A legal revival closes that corpse-specific resurrection rider and retains only any still-future living pulse schedule until cured/expired. This grants no resurrection block or permission. Secondary ticks cannot create further Agony, copies, lifesteal or resource procs. Any independent Necrotic Affinity seal needs its own real fatal-root predicate.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "The first 1d4 pulse resolves at the target’s regular start; a successful CON save at its regular end removes the remaining pulses.",
    "A normal heal with no save gains no new saving throw. Death skips living pulses without extending the original deadline or granting resurrection permission."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After your personally cast noncopy spell deals positive resolved damage, optionally apply one Agony record to one living damaged target, once per owner/target/numbered round. Reapplication refreshes one profile without stacked dice. It deals 1d4 necrotic at the next three original target regular-start markers; a CON save against the generating cast DC at each affected regular end, including a current turn if applicable, ends it. The final third scheduled pulse ends the record after damage; no extra ending save afterward. It is a magical ongoing wound, not Core Wound, maximum HP injury or Bleeding by name. NEW a legal positive-potential magical heal or Action Medicine vs source DC ends it; suppressed records remain curable. While active, disadvantage applies only to actual existing CON saves to regain HP and actual saves against resurrection effects; no such save is invented. Death suspends living damage, retaining only the unexpired record tied to that exact death instance until the original third-start deadline; missed pulses are consumed, never backlogged. A legal revival closes that corpse-specific resurrection rider and retains only any still-future living pulse schedule until cured/expired. This grants no resurrection block or permission. Secondary ticks cannot create further Agony, copies, lifesteal or resource procs. Any independent Necrotic Affinity seal needs its own real fatal-root predicate.

### Original-position authored review references

```json
[
  {
    "id": "MX-58-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/34"
  },
  {
    "id": "MX-58-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json",
      "bytes": 807419,
      "sha256": "d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92"
    },
    "pointer": "/originalCaseReviews/35"
  }
]
```
