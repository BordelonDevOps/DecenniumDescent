# Heritage Mutation — source reconciliation

Derived complete-text assembly 106; exact parent review and integration pending.

Original source decisions below are historical receipts. The complete current candidate procedure and linked complete case review control this derived reading.

## HM-01 — Aberrant Mind

### Complete original object

```json
{
  "id": "aberrant_mind",
  "name": "Aberrant Mind",
  "description": "Your mind has been touched by alien intelligence.",
  "prerequisite": "Intelligence 15+",
  "effect": "You can communicate telepathically with aberrations and have resistance to psychic damage.",
  "type": "Aberrant_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve telepathy with aberrations and psychic resistance under Intelligence15. Define actual creature-type eligibility,range,senses,language,directionality,consent/actions and informational limits. Source category does not by itself require Warrior or change creature type. No alien origin, universal cognition or cosmology decision is inferred."
```

### Preserved original source direction (historical)

```json
{
  "featId": "aberrant_mind",
  "name": "Aberrant Mind",
  "cohort": "heritage_mutation",
  "questionId": "HM-01",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/0",
  "originalQuestion": "Preserve telepathy with aberrations and psychic resistance under Intelligence15. Define actual creature-type eligibility,range,senses,language,directionality,consent/actions and informational limits. Source category does not by itself require Warrior or change creature type. No alien origin, universal cognition or cosmology decision is inferred.",
  "originalSourceObject": {
    "id": "aberrant_mind",
    "name": "Aberrant Mind",
    "description": "Your mind has been touched by alien intelligence.",
    "prerequisite": "Intelligence 15+",
    "effect": "You can communicate telepathically with aberrations and have resistance to psychic damage.",
    "type": "Aberrant_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "7386902925250557e5363c6a06bab1722696834905af32d8e7b3028c0a953176",
  "submittedProcedure": "Retain permanentINT15 prerequisite and resistance to psychic damage, subject to one same-type resistance. NEW while conscious, initiate one two-way telepathic conversation with one actual Aberration you perceive within60ft and line of effect. A brief message uses the ordinary free communication allowance on your own regular turn; an invited willing recipient may reply briefly without Action, including off-turn, without gaining another action. Both must know at least one language, but need not share one. No automatic type detection: choosing a non-Aberration produces no channel, not a diagnosis of why it failed. Recipient may refuse/end communication; you cannot read thoughts, memories, emotions or intentions, compel responses, or impersonate a voice. Maintain actual range/line of effect; loss ends the link. Silence/Deafened alone does not block purely mental speech, but Unconscious or explicit telepathy/mental-communication protection does. One channel at a time, no relay or shared senses. This grants no Aberration creature type, mutation activation or alien-origin fact.",
  "submittedNewChoices": "60ft single willing channel, language capacity without shared language, free brief exchange and strict information limits.",
  "submittedWorkedCases": [
    "A willing Aberration knowing a different language may converse mentally within60ft; the feat reveals only its voluntary message.",
    "A wall giving total cover ends the channel. Psychic resistance still applies to an otherwise legal psychic packet."
  ],
  "decision": "Keep actual INT15 and bounded Aberration communication/sense scope without a Warrior gate, free common language, coercion or taxonomy revelation.",
  "completeAuthoringProcedure": "Retain permanentINT15 prerequisite and resistance to psychic damage, subject to one same-type resistance. NEW while conscious, initiate one two-way telepathic conversation with one actual Aberration you perceive within60ft and line of effect. A brief message uses the ordinary free communication allowance on your own regular turn; an invited willing recipient may reply briefly without Action, including off-turn, without gaining another action. Both must know at least one language, but need not share one. No automatic type detection: choosing a non-Aberration produces no channel, not a diagnosis of why it failed. Recipient may refuse/end communication; you cannot read thoughts, memories, emotions or intentions, compel responses, or impersonate a voice. Maintain actual range/line of effect; loss ends the link. Silence/Deafened alone does not block purely mental speech, but Unconscious or explicit telepathy/mental-communication protection does. One channel at a time, no relay or shared senses. This grants no Aberration creature type, mutation activation or alien-origin fact.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A willing Aberration knowing a different language may converse mentally within60ft; the feat reveals only its voluntary message.",
    "A wall giving total cover ends the channel. Psychic resistance still applies to an otherwise legal psychic packet."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Retain permanentINT15 prerequisite and resistance to psychic damage, subject to one same-type resistance. NEW while conscious, initiate one two-way telepathic conversation with one actual Aberration you perceive within60ft and line of effect. A brief message uses the ordinary free communication allowance on your own regular turn; an invited willing recipient may reply briefly without Action, including off-turn, without gaining another action. Both must know at least one language, but need not share one. No automatic type detection: choosing a non-Aberration produces no channel, not a diagnosis of why it failed. Recipient may refuse/end communication; you cannot read thoughts, memories, emotions or intentions, compel responses, or impersonate a voice. Maintain actual range/line of effect; loss ends the link. Silence/Deafened alone does not block purely mental speech, but Unconscious or explicit telepathy/mental-communication protection does. One channel at a time, no relay or shared senses. This grants no Aberration creature type, mutation activation or alien-origin fact.

### Original-position authored review references

```json
[
  {
    "id": "HM-01-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/0"
  },
  {
    "id": "HM-01-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/1"
  }
]
```

## HM-02 — Backlash Engine

### Complete original object

```json
{
  "id": "backlashEngine",
  "name": "Backlash Engine",
  "description": "Taking damage while mutated builds up energy.",
  "prerequisite": "Adrenal Backlash Core mutation",
  "effect": "Each time you're hit while mutated, gain +1 BT",
  "type": "Combat_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile standalone each hit while mutated with the full Warrior counterpart: Warrior8,Adrenal Backlash Core equipped/active,actual damage and once per round. Resolve source-defined BT cap/generation exceptions,hostile-threat rules,damage packets and zeroHP. Do not approve broader hit farming or grant this twice through class and feat catalogs."
```

### Preserved original source direction (historical)

```json
{
  "featId": "backlashEngine",
  "name": "Backlash Engine",
  "cohort": "heritage_mutation",
  "questionId": "HM-02",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/1",
  "originalQuestion": "Reconcile standalone each hit while mutated with the full Warrior counterpart: Warrior8,Adrenal Backlash Core equipped/active,actual damage and once per round. Resolve source-defined BT cap/generation exceptions,hostile-threat rules,damage packets and zeroHP. Do not approve broader hit farming or grant this twice through class and feat catalogs.",
  "originalSourceObject": {
    "id": "backlashEngine",
    "name": "Backlash Engine",
    "description": "Taking damage while mutated builds up energy.",
    "prerequisite": "Adrenal Backlash Core mutation",
    "effect": "Each time you're hit while mutated, gain +1 BT",
    "type": "Combat_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "c0cb517f57611ce33aae02daf6ed4e78615ed7e6e2d290562e3c52d9914e9487",
  "submittedProcedure": "NEW select the actual Warrior8 counterpart over unlimited each-hit generation: require Adrenal Backlash Core equipped and active. The first qualifying actual-damage event in a numbered round may grant1BT, no Action, subject to current BT cap3 or actual Stack Overflow4. Use positive numeric actualDamageDealt to you, so real temporaryHP absorption counts; a zero-damage hit, floor-prevented loss with no temp absorption or direct HP sacrifice does not. Recheck survival and active mutation after the full damage/death sequence; no gain after actual death or ended mutation. Current hostile-threat anti-farming restrictions apply; environmental damage without a meaningful hostile cause grants noBT under this NEW feat completion. This explicit card gain bypasses the normal combined2BT-generation ceiling but not its own once-round cap or stored maximum. It adds no Brutality Progress and remains the same gain whether selected from the feat registry or Warrior supplement. Ordinary qualifying damage-taken BT may also resolve once under its own threshold/cap; neither effect duplicates the other.",
  "submittedNewChoices": "Warrior8, active Adrenal, once-round numeric actual damage and explicit generation-ceiling exception.",
  "submittedWorkedCases": [
    "A hostile hit removes2tempHP: Backlash may add1BT despite no normalHP loss, if its round allowance and current cap permit.",
    "AtBT3 without Stack Overflow the grant adds0. Another hit that round cannot create a second Backlash gain."
  ],
  "decision": "Unify the standalone/class-counterpart identity; use actual Warrior8 and active Adrenal Backlash Core, first eligible actual hostile damage/round, BT cap and no resource-free copies.",
  "completeAuthoringProcedure": "NEW select the actual Warrior8 counterpart over unlimited each-hit generation: require Adrenal Backlash Core equipped and active. The first qualifying actual-damage event in a numbered round may grant1BT, no Action, subject to current BT cap3 or actual Stack Overflow4. Use positive numeric actualDamageDealt to you, so real temporaryHP absorption counts; a zero-damage hit, floor-prevented loss with no temp absorption or direct HP sacrifice does not. Recheck survival and active mutation after the full damage/death sequence; no gain after actual death or ended mutation. Current hostile-threat anti-farming restrictions apply; environmental damage without a meaningful hostile cause grants noBT under this NEW feat completion. This explicit card gain bypasses the normal combined2BT-generation ceiling but not its own once-round cap or stored maximum. It adds no Brutality Progress and remains the same gain whether selected from the feat registry or Warrior supplement. Ordinary qualifying damage-taken BT may also resolve once under its own threshold/cap; neither effect duplicates the other.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A hostile hit removes2tempHP: Backlash may add1BT despite no normalHP loss, if its round allowance and current cap permit.",
    "AtBT3 without Stack Overflow the grant adds0. Another hit that round cannot create a second Backlash gain."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW select the actual Warrior8 counterpart over unlimited each-hit generation: require Adrenal Backlash Core equipped and active. The first qualifying actual-damage event in a numbered round may grant1BT, no Action, subject to current BT cap3 or actual Stack Overflow4. Use positive numeric actualDamageDealt to you, so real temporaryHP absorption counts; a zero-damage hit, floor-prevented loss with no temp absorption or direct HP sacrifice does not. Recheck survival and active mutation after the full damage/death sequence; no gain after actual death or ended mutation. Current hostile-threat anti-farming restrictions apply; environmental damage without a meaningful hostile cause grants noBT under this NEW feat completion. This explicit card gain bypasses the normal combined2BT-generation ceiling but not its own once-round cap or stored maximum. It adds no Brutality Progress and remains the same gain whether selected from the feat registry or Warrior supplement. Ordinary qualifying damage-taken BT may also resolve once under its own threshold/cap; neither effect duplicates the other.

### Original-position authored review references

```json
[
  {
    "id": "HM-02-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/2"
  },
  {
    "id": "HM-02-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/3"
  }
]
```

## HM-03 — Bio-Stabilizer

### Complete original object

```json
{
  "id": "bioStabilizer",
  "name": "Bio-Stabilizer",
  "description": "Your mutations have stabilized, providing enhanced regeneration.",
  "prerequisite": "Bloodthick Node mutation",
  "effect": "+1 regeneration while under the effect of 2+ mutations",
  "type": "Vital_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile standalone+1 regeneration with Warrior4/Bloodthick equipped and the reviewed scheduling-only modifier. Require actual Bloodthick activation and two active mutations; define one added HP on the same pulse,shared Mutation Recovery Reserve,zeroHP/Wound gates and finite healing. No second pulse or free reserve refill."
```

### Preserved original source direction (historical)

```json
{
  "featId": "bioStabilizer",
  "name": "Bio-Stabilizer",
  "cohort": "heritage_mutation",
  "questionId": "HM-03",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/2",
  "originalQuestion": "Reconcile standalone+1 regeneration with Warrior4/Bloodthick equipped and the reviewed scheduling-only modifier. Require actual Bloodthick activation and two active mutations; define one added HP on the same pulse,shared Mutation Recovery Reserve,zeroHP/Wound gates and finite healing. No second pulse or free reserve refill.",
  "originalSourceObject": {
    "id": "bioStabilizer",
    "name": "Bio-Stabilizer",
    "description": "Your mutations have stabilized, providing enhanced regeneration.",
    "prerequisite": "Bloodthick Node mutation",
    "effect": "+1 regeneration while under the effect of 2+ mutations",
    "type": "Vital_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "43b4d41b4f89ee73d74d8dbdaf6710ec41ff16076253ba78b9e135dcfe5905b3",
  "submittedProcedure": "NEW adopt Warrior4 and actual equipped Bloodthick Node. At each valid original Bloodthick regular-start pulse, if Bloodthick and at least one other mutation are actually active, add1 to that same pulse base before ordinary healing modifiers/caps. Bloodthick base remains currentBT capped3, or4 with actual Stack Overflow; the extra1 can make base4 or5. NEW a lawful Bloodthick pulse atBT0 may have base1 from this modifier, but there is no independent pulse and no healing outside a real encounter. Every HP actually restored spends1 from the same Mutation Recovery Reserve (3×Warrior level+M after LR); no reserve refill from SR, encounter, form or bonus. Apply broad/passive-regeneration prohibitions, source eligibility, current maximum and Critical3-Wound healing ceiling max(1,maxHP−1). It does not remove Wounds, cure death or manufacture zeroHP action permission. NEW an already active Bloodthick pulse may heal a living0HP owner after that start's prior death-save processing if the owner survives and no actual source prohibition blocks it; incapacitation alone does not retroactively cancel this non-concentration passive mutation. A dead owner receives nothing. No excess-healing conversion from this unpaid regeneration, even at fullHP.",
  "submittedNewChoices": "One pulse, active-count snapshot, explicit BT0/zeroHP completion, shared finite reserve and unchanged reviewed exclusions.",
  "submittedWorkedCases": [
    "BT2 plus this modifier gives base3; with only1Reserve remaining and sufficient missingHP, restore1 and spend1.",
    "At fullHP the pulse spends0Reserve and cannot convert its mathematical excess to another resource."
  ],
  "decision": "Unify Warrior4/Bloodthick/other active mutation gates and finite source recovery reserve; the+1 pulse at0BT is an explicit feat exception, not automatic0HP revival or new serum.",
  "completeAuthoringProcedure": "NEW adopt Warrior4 and actual equipped Bloodthick Node. At each valid original Bloodthick regular-start pulse, if Bloodthick and at least one other mutation are actually active, add1 to that same pulse base before ordinary healing modifiers/caps. Bloodthick base remains currentBT capped3, or4 with actual Stack Overflow; the extra1 can make base4 or5. NEW a lawful Bloodthick pulse atBT0 may have base1 from this modifier, but there is no independent pulse and no healing outside a real encounter. Every HP actually restored spends1 from the same Mutation Recovery Reserve (3×Warrior level+M after LR); no reserve refill from SR, encounter, form or bonus. Apply broad/passive-regeneration prohibitions, source eligibility, current maximum and Critical3-Wound healing ceiling max(1,maxHP−1). It does not remove Wounds, cure death or manufacture zeroHP action permission. NEW an already active Bloodthick pulse may heal a living0HP owner after that start's prior death-save processing if the owner survives and no actual source prohibition blocks it; incapacitation alone does not retroactively cancel this non-concentration passive mutation. A dead owner receives nothing. No excess-healing conversion from this unpaid regeneration, even at fullHP.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "BT2 plus this modifier gives base3; with only1Reserve remaining and sufficient missingHP, restore1 and spend1.",
    "At fullHP the pulse spends0Reserve and cannot convert its mathematical excess to another resource."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW adopt Warrior4 and actual equipped Bloodthick Node. At each valid original Bloodthick regular-start pulse, if Bloodthick and at least one other mutation are actually active, add1 to that same pulse base before ordinary healing modifiers/caps. Bloodthick base remains currentBT capped3, or4 with actual Stack Overflow; the extra1 can make base4 or5. NEW a lawful Bloodthick pulse atBT0 may have base1 from this modifier, but there is no independent pulse and no healing outside a real encounter. Every HP actually restored spends1 from the same Mutation Recovery Reserve (3×Warrior level+M after LR); no reserve refill from SR, encounter, form or bonus. Apply broad/passive-regeneration prohibitions, source eligibility, current maximum and Critical3-Wound healing ceiling max(1,maxHP−1). It does not remove Wounds, cure death or manufacture zeroHP action permission. NEW an already active Bloodthick pulse may heal a living0HP owner after that start's prior death-save processing if the owner survives and no actual source prohibition blocks it; incapacitation alone does not retroactively cancel this non-concentration passive mutation. A dead owner receives nothing. No excess-healing conversion from this unpaid regeneration, even at fullHP.

### Original-position authored review references

```json
[
  {
    "id": "HM-03-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/4"
  },
  {
    "id": "HM-03-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/5"
  }
]
```

## HM-04 — Born to Horrify

### Complete original object

```json
{
  "id": "bornToHorrify",
  "name": "Born to Horrify",
  "description": "Your apex mutations grant enhanced resilience.",
  "prerequisite": "Any Apex Mutation",
  "effect": "While your Apex mutation is active, you may reroll 1 save per turn",
  "type": "Aberrant_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile per-turn standalone wording with Warrior16 counterpart limiting failure rerolls to the owner regular turn while Apex active. Define optional declaration after die/result,advantage/disadvantage dice,new result,one ledger and off-turn saves; do not silently treat every enemy turn as another use."
```

### Preserved original source direction (historical)

```json
{
  "featId": "bornToHorrify",
  "name": "Born to Horrify",
  "cohort": "heritage_mutation",
  "questionId": "HM-04",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/3",
  "originalQuestion": "Reconcile per-turn standalone wording with Warrior16 counterpart limiting failure rerolls to the owner regular turn while Apex active. Define optional declaration after die/result,advantage/disadvantage dice,new result,one ledger and off-turn saves; do not silently treat every enemy turn as another use.",
  "originalSourceObject": {
    "id": "bornToHorrify",
    "name": "Born to Horrify",
    "description": "Your apex mutations grant enhanced resilience.",
    "prerequisite": "Any Apex Mutation",
    "effect": "While your Apex mutation is active, you may reroll 1 save per turn",
    "type": "Aberrant_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "39d2f558f2f1c77848ef67a04f67ee1b4c4f89b71af4700b9a8716a05906180f",
  "submittedProcedure": "NEW use the Warrior16 counterpart with any actual Apex mutation equipped and active: once on your own original regular turn, after your saving throw has failed but before consequences, optionally reroll the whole save and use the new result. Preserve its actual advantage/disadvantage configuration, rolling the appropriate new d20 set, not choosing freely among old and new dice. No Action/Reaction is required. The new result may be worse; a failed reroll cannot invoke this feat again on the same event. It can affect ordinary or death saves actually rolled on that turn if Apex remains active and source-specific zeroHP restrictions permit the passive reroll; it cannot replace an automatic failure without a roll. Off-turn saves and extra turns grant no entitlement, even if the standalone source says per turn. No banking. Applicable other reroll features retain their real limits; choose a legal order, never revisit a consumed stage.",
  "submittedNewChoices": "Owner-regular-turn failed-save restriction and whole-roll mandatory replacement; preserves broader standalone alternative.",
  "submittedWorkedCases": [
    "On your own turn a failedCONsave with advantage rerolls two newd20s and keeps their higher result, discarding both old dice.",
    "A failedWISsave during an enemy turn cannot use this feat, despite an active Apex mutation."
  ],
  "decision": "Unify Warrior16 actual active Apex gate and once-own-regular-turn failed-save reroll; preserve kept new result and source endpoint, not every off-turn save.",
  "completeAuthoringProcedure": "NEW use the Warrior16 counterpart with any actual Apex mutation equipped and active: once on your own original regular turn, after your saving throw has failed but before consequences, optionally reroll the whole save and use the new result. Preserve its actual advantage/disadvantage configuration, rolling the appropriate new d20 set, not choosing freely among old and new dice. No Action/Reaction is required. The new result may be worse; a failed reroll cannot invoke this feat again on the same event. It can affect ordinary or death saves actually rolled on that turn if Apex remains active and source-specific zeroHP restrictions permit the passive reroll; it cannot replace an automatic failure without a roll. Off-turn saves and extra turns grant no entitlement, even if the standalone source says per turn. No banking. Applicable other reroll features retain their real limits; choose a legal order, never revisit a consumed stage.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "On your own turn a failedCONsave with advantage rerolls two newd20s and keeps their higher result, discarding both old dice.",
    "A failedWISsave during an enemy turn cannot use this feat, despite an active Apex mutation."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW use the Warrior16 counterpart with any actual Apex mutation equipped and active: once on your own original regular turn, after your saving throw has failed but before consequences, optionally reroll the whole save and use the new result. Preserve its actual advantage/disadvantage configuration, rolling the appropriate new d20 set, not choosing freely among old and new dice. No Action/Reaction is required. The new result may be worse; a failed reroll cannot invoke this feat again on the same event. It can affect ordinary or death saves actually rolled on that turn if Apex remains active and source-specific zeroHP restrictions permit the passive reroll; it cannot replace an automatic failure without a roll. Off-turn saves and extra turns grant no entitlement, even if the standalone source says per turn. No banking. Applicable other reroll features retain their real limits; choose a legal order, never revisit a consumed stage.

### Original-position authored review references

```json
[
  {
    "id": "HM-04-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/6"
  },
  {
    "id": "HM-04-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/7"
  }
]
```

## HM-05 — Contraption Crafter

### Complete original object

```json
{
  "id": "contraption_crafter",
  "name": "Contraption Crafter",
  "description": "Racial feat tied to Gnome heritage.",
  "prerequisite": "Gnome heritage",
  "effect": "Construct and deploy a temporary gadget with random utility (1/day).",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind actual Gnome heritage eligibility and one/day recovery clock. Define a finite random-utility gadget table with creation/deployment actions,actual tools/materials,physical profile,duration,ownership,usage and end disposition. Compare Tinker Gnome ancestry and pending Tinker class/recipes without free permanent products,random undefined powers or automatic class access."
```

### Preserved original source direction (historical)

```json
{
  "featId": "contraption_crafter",
  "name": "Contraption Crafter",
  "cohort": "heritage_mutation",
  "questionId": "HM-05",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/4",
  "originalQuestion": "Bind actual Gnome heritage eligibility and one/day recovery clock. Define a finite random-utility gadget table with creation/deployment actions,actual tools/materials,physical profile,duration,ownership,usage and end disposition. Compare Tinker Gnome ancestry and pending Tinker class/recipes without free permanent products,random undefined powers or automatic class access.",
  "originalSourceObject": {
    "id": "contraption_crafter",
    "name": "Contraption Crafter",
    "description": "Racial feat tied to Gnome heritage.",
    "prerequisite": "Gnome heritage",
    "effect": "Construct and deploy a temporary gadget with random utility (1/day).",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "dcd6e76fb4909d12bc2b9498895b81e809a6cf758cd698ec0e676cc84ac276e5",
  "submittedProcedure": "Require actual Gnome heritage. NEW once per24 elapsed hours, spend10 uninterrupted minutes with actual usable tinkers tools and5gp of suitable owned mundane parts; commit the use and parts at construction start. The feat grants construction permission with these tools but no general tool proficiency. On completion roll1d4 openly on the four complete profiles below; no choice, reroll, duplicate product or refund for an unwanted result. One active feat gadget at a time; beginning a new legal construction ends the old gadget. Interrupted work loses the committed parts/use and yields no working gadget. The Tiny mundane object is1lb, AC10, HP1, has no creature turn/actions, and stops after1hour from completion or destruction. Place it in a reachable legal space or activate it with the profile's Action; moving/holding uses actual hands/object rules. Ownership can pass with the real object; its expiry/remaining uses travel with it and never reset. At expiry/dismantling it becomes inert spent parts with no reusable credited crafting value; no purchased tool/supply/consumable is replenished. Explicitly NEW economics, not a claim that original source named a price. It does not inherit Tinker Gnome's separate four clockwork profiles,10gp reclaim or maintenance loop, and creates no Tinker class device/attack/companion.",
  "submittedNewChoices": "Finite1d4 utility menu,10minute/5gp manufacture,24elapsed-hour cadence, real object and1hour expiry.",
  "submittedWorkedCases": [
    "Construction completes with a3 on the table: it produces the clamp profile only; the creator cannot reroll into a lantern.",
    "Giving the gadget to an ally passes the same object with its existing deadline; midnight or a rest does not refresh the feat."
  ],
  "decision": "Adopt four NEW1lb/AC10/HP1/hour-life gadget profiles with actual5gp materials and10-minute work; separate from Tinker Gnome ancestry and43 crafted devices.",
  "completeAuthoringProcedure": "Require actual Gnome heritage. NEW once per24 elapsed hours, spend10 uninterrupted minutes with actual usable tinkers tools and5gp of suitable owned mundane parts; commit the use and parts at construction start. The feat grants construction permission with these tools but no general tool proficiency. On completion roll1d4 openly on the four complete profiles below; no choice, reroll, duplicate product or refund for an unwanted result. One active feat gadget at a time; beginning a new legal construction ends the old gadget. Interrupted work loses the committed parts/use and yields no working gadget. The Tiny mundane object is1lb, AC10, HP1, has no creature turn/actions, and stops after1hour from completion or destruction. Place it in a reachable legal space or activate it with the profile's Action; moving/holding uses actual hands/object rules. Ownership can pass with the real object; its expiry/remaining uses travel with it and never reset. At expiry/dismantling it becomes inert spent parts with no reusable credited crafting value; no purchased tool/supply/consumable is replenished. Explicitly NEW economics, not a claim that original source named a price. It does not inherit Tinker Gnome's separate four clockwork profiles,10gp reclaim or maintenance loop, and creates no Tinker class device/attack/companion.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Construction completes with a3 on the table: it produces the clamp profile only; the creator cannot reroll into a lantern.",
    "Giving the gadget to an ally passes the same object with its existing deadline; midnight or a rest does not refresh the feat."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Gnome heritage. NEW once per24 elapsed hours, spend10 uninterrupted minutes with actual usable tinkers tools and5gp of suitable owned mundane parts; commit the use and parts at construction start. The feat grants construction permission with these tools but no general tool proficiency. On completion roll1d4 openly on the four complete profiles below; no choice, reroll, duplicate product or refund for an unwanted result. One active feat gadget at a time; beginning a new legal construction ends the old gadget. Interrupted work loses the committed parts/use and yields no working gadget. The Tiny mundane object is1lb, AC10, HP1, has no creature turn/actions, and stops after1hour from completion or destruction. Place it in a reachable legal space or activate it with the profile's Action; moving/holding uses actual hands/object rules. Ownership can pass with the real object; its expiry/remaining uses travel with it and never reset. At expiry/dismantling it becomes inert spent parts with no reusable credited crafting value; no purchased tool/supply/consumable is replenished. Explicitly NEW economics, not a claim that original source named a price. It does not inherit Tinker Gnome's separate four clockwork profiles,10gp reclaim or maintenance loop, and creates no Tinker class device/attack/companion.

FT84 source-follow-through selection (proposed; the following explicit interaction controls only this named composition):
FT84-Q03 / FT84-CLOSED-CREATION-01 — Craftsman applies to actual authorized creation, not names or all fixed-duration work.
INTERPRETATION SELECTED: personally leading an independently authorized closed feat process that makes/assembles a new usable physical body or prepared kit is eligible creation even when it is non-artisan, lacks a catalog recipe ID or prints a fixed base duration. Craftsman supplies only its half-active-time factor; it supplies no process, skill, formula, assistants, work opportunity, materials, use or output. Use the strongest genuinely applicable creation reduction once. An explicit source exclusion or distinct alteration/preparation/service category still controls. Keep actual physical minimum phases only where the source requires them; do not manufacture an advanced-recipe incorporation phase for every short feat process.
Contraption Crafter's ten minutes are the ordinary base for its real gadget construction. With actual personally leading Craftsman ownership the complete job is five uninterrupted active minutes, not ten with a final five-minute discount and not two-and-a-half from a second equivalent half. The whole adjusted job must be uninterrupted; phase logging, assistant handoff, pauses, rest or partially completed earlier attempts cannot satisfy it. Keep actual Gnome heritage, usable tinker's tools, the same five-gp suitable owned parts and the same once-per-24-elapsed-hours use committed at start. A new lawful construction still ends its old gadget at start. Interruption spends the committed parts/use and yields no working gadget, no completion roll, no refundable tail and no resumable partial product. Completion rolls the same one d4 openly, once; it grants no chosen profile, duplicate gadget, general proficiency, quality, recipe XP or parts recovery. The same one-hour gadget lifetime starts at actual completion, not at the undiscounted hypothetical finish. Transfer/deployment/activation/recharge rules are unchanged. The time benefit is prospective and cannot manufacture a mid-job feat acquisition opportunity; if a real change interrupts the required work, the ordinary failure consequence applies.
Trapsetter's independently authorized thirty-active-minute kit assembly is likewise eligible creation: fifteen active minutes with Craftsman. This includes only its actual prepared-kit assembly from the real source parts; it cannot manufacture an ordinary twenty-caltrop stock bag out of an arbitrary substitute or count buying/deploying one as new creation. Keep the one completion DC12 INT/Engineering or DEX/thieves-tools check, ordinary task degree/natural shifts collapsed to binary, actual parts, failure consumption and recoverable remaining metal/frame. No manufacturing quality/yield/XP or general recipe is added. NEW NARROW WORK-CREDIT COMPLETION for this otherwise unphased kit assembly: track actual active work in seconds against the adjusted required total; pauses do not by themselves erase already completed usable physical assembly work. A pause earns no credit, protection or rest entitlement. Preserve the actual partial body and committed stock under their ordinary custody, deterioration and loss rules; work that a genuine physical event destroys cannot remain credited. The unfinished kit has no function. Resume only the remaining actual work with the real usable/replacement parts; do not duplicate stock, credit or partial bodies. No completion roll occurs until the whole adjusted job is actually complete. Neither Contraption's uninterrupted-work/use forfeiture nor advanced manufacture's incorporation/stabilization is imported. A more-specific explicitly authorized phase/loss rule still controls.
Kit assembly does not spend or refresh Trapsetter's three source-specific quick-placement allowances, arm a trap, clear an old active slot, reset hard-denial history or reduce placement, arming, disarming, collection or trigger/Reaction costs. Those remain separately paid physical events.
Apply the same predicate to Bowyer's actual bounded mundane bow/arrow creation and Master Smithing's authorized weapon/armor creation: their actual creation work qualifies, with full bridge credentials, stock, DC, phases and waits. Combat Engineering's actual barricade creation also qualifies but its own half factor and Craftsman compare once (60 to30, not15). Master Smithing's expressly nondiscounted eight-hour temper and Combat Engineering's expressly fixed ten-minute kill-zone preparation remain unchanged. Separate encoding, repair, maintenance, harvesting, copying, ritual casting and rest remain outside Craftsman. Actual advanced recipe121 still keeps its own required included incorporation/phase/stock/assistant rules; the short feat processes do not rewrite them. Merely printing a fixed duration neither exempts genuine creation nor makes a noncreation activity eligible.

### Original-position authored review references

```json
[
  {
    "id": "HM-05-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/8"
  },
  {
    "id": "HM-05-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/9"
  }
]
```

## HM-06 — Crushing Advance

### Complete original object

```json
{
  "id": "crushing_advance",
  "name": "Crushing Advance",
  "description": "Racial feat tied to Ogre heritage.",
  "prerequisite": "Ogre heritage",
  "effect": "Your melee hits knock targets back 5 feet if you're moving.",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind actual Ogre heritage,melee hit and precise moving requirement: own movement distance,straight path,timing,one hit versus every hit and cooldown. Define5ft push direction,target-size/save/space/collision,forced movement,reach and no source-implied bonus damage or extra attacks."
```

### Preserved original source direction (historical)

```json
{
  "featId": "crushing_advance",
  "name": "Crushing Advance",
  "cohort": "heritage_mutation",
  "questionId": "HM-06",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/5",
  "originalQuestion": "Bind actual Ogre heritage,melee hit and precise moving requirement: own movement distance,straight path,timing,one hit versus every hit and cooldown. Define5ft push direction,target-size/save/space/collision,forced movement,reach and no source-implied bonus damage or extra attacks.",
  "originalSourceObject": {
    "id": "crushing_advance",
    "name": "Crushing Advance",
    "description": "Racial feat tied to Ogre heritage.",
    "prerequisite": "Ogre heritage",
    "effect": "Your melee hits knock targets back 5 feet if you're moving.",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "ded762c93d756b68e012ec6558b46983396d3e02ab1b02fbeebc5e777881e235",
  "submittedProcedure": "Require actual Ogre heritage. NEW once on your own original regular turn, after moving at least5ft of voluntary continuous movement directly toward a target immediately before your next personal melee attack against it, a hit may push it5ft directly away. The approach must use a real movement mode and paid path with no intervening action/attack/teleport/forced displacement; the attack itself is the endpoint. The melee attack can be weapon, unarmed or spell if otherwise legal. No extra movement, attack or damage. NEW no saving throw and target at most one size larger than your actual body, not Powerful Build; choose use after hit before resolving push. Resolve damage/immediate riders first; target must still exist and be legally movable. Push uses ordinary forced-movement collision, occupies legal space and stops before a barrier, never adds collision damage or ordinary opportunity attacks. If no legal positive displacement remains, no movement occurs and the chosen attempt remains used. Other independently qualified source pushes retain their exact stacking rules; this is no once-per-hit loop.",
  "submittedNewChoices": "5ft direct approach, one own-turn trigger, one-size limit and no-save post-hit5ft push.",
  "submittedWorkedCases": [
    "A Large Ogre approaches5ft, hits a Huge target and may push it5ft if the path is clear.",
    "An ally shoving the Ogre toward a foe does not meet voluntary approach; striking a wall-backed target adds no impact damage."
  ],
  "decision": "Keep actual Ogre body size, voluntary five-foot approach and one melee-hit push/own turn; no Powerfully Built size inflation or unsupported displacement.",
  "completeAuthoringProcedure": "Require actual Ogre heritage. NEW once on your own original regular turn, after moving at least5ft of voluntary continuous movement directly toward a target immediately before your next personal melee attack against it, a hit may push it5ft directly away. The approach must use a real movement mode and paid path with no intervening action/attack/teleport/forced displacement; the attack itself is the endpoint. The melee attack can be weapon, unarmed or spell if otherwise legal. No extra movement, attack or damage. NEW no saving throw and target at most one size larger than your actual body, not Powerful Build; choose use after hit before resolving push. Resolve damage/immediate riders first; target must still exist and be legally movable. Push uses ordinary forced-movement collision, occupies legal space and stops before a barrier, never adds collision damage or ordinary opportunity attacks. If no legal positive displacement remains, no movement occurs and the chosen attempt remains used. Other independently qualified source pushes retain their exact stacking rules; this is no once-per-hit loop.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A Large Ogre approaches5ft, hits a Huge target and may push it5ft if the path is clear.",
    "An ally shoving the Ogre toward a foe does not meet voluntary approach; striking a wall-backed target adds no impact damage."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Ogre heritage. NEW once on your own original regular turn, after moving at least5ft of voluntary continuous movement directly toward a target immediately before your next personal melee attack against it, a hit may push it5ft directly away. The approach must use a real movement mode and paid path with no intervening action/attack/teleport/forced displacement; the attack itself is the endpoint. The melee attack can be weapon, unarmed or spell if otherwise legal. No extra movement, attack or damage. NEW no saving throw and target at most one size larger than your actual body, not Powerful Build; choose use after hit before resolving push. Resolve damage/immediate riders first; target must still exist and be legally movable. Push uses ordinary forced-movement collision, occupies legal space and stops before a barrier, never adds collision damage or ordinary opportunity attacks. If no legal positive displacement remains, no movement occurs and the chosen attempt remains used. Other independently qualified source pushes retain their exact stacking rules; this is no once-per-hit loop.

### Original-position authored review references

```json
[
  {
    "id": "HM-06-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/10"
  },
  {
    "id": "HM-06-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/11"
  }
]
```

## HM-07 — Cultural Legacy

### Complete original object

```json
{
  "id": "cultural_legacy",
  "name": "Cultural Legacy",
  "description": "Racial feat tied to Goblin heritage.",
  "prerequisite": "Goblin heritage",
  "effect": "You gain +10% effectiveness with your race’s favored skills.",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind Goblin heritage and identify an actual finite favored-skill list from supplied base/variant traits. Define10percent effectiveness against d20 check totals,task degrees or another explicit numerical result,including rounding/stacking. Do not invent culture/lore,apply a universal multiplier or silently replace the current percentage."
```

### Preserved original source direction (historical)

```json
{
  "featId": "cultural_legacy",
  "name": "Cultural Legacy",
  "cohort": "heritage_mutation",
  "questionId": "HM-07",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/6",
  "originalQuestion": "Bind Goblin heritage and identify an actual finite favored-skill list from supplied base/variant traits. Define10percent effectiveness against d20 check totals,task degrees or another explicit numerical result,including rounding/stacking. Do not invent culture/lore,apply a universal multiplier or silently replace the current percentage.",
  "originalSourceObject": {
    "id": "cultural_legacy",
    "name": "Cultural Legacy",
    "description": "Racial feat tied to Goblin heritage.",
    "prerequisite": "Goblin heritage",
    "effect": "You gain +10% effectiveness with your race’s favored skills.",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "f1a7722cfedceaf7849838ceb1a0b65c50b132ee618991994dd70257e66e1933",
  "submittedProcedure": "Require actual Goblin heritage. NEW favored-skill scope is fixed from its actual chosen variant evidence: all Goblins gain Stealth checks through base Nimble Escape; Boom adds INT checks specifically concerning alchemy/explosives/incendiaries under Demolition Expert; Scrap adds WIS Perception to find useful junk or hidden objects and DEX Sleight of Hand to find hidden objects under its printed scavenging clauses; Shadow retains Stealth only. This is a task list derived for the feat, not a cultural truth or a new proficiency grant. On a qualifying actually rolled check, compute ordinary totalT after other legal modifiers, add floor(max(0,T)/10), then compare toDC/opposed total and apply normal task natural-result shifts. This is an explicit NEW10%-of-nonnegative-check-total interpretation of effectiveness, preserving the original percentage rather than substituting a flat bonus. No recursive multiplication, passive-perception multiplier, extra loot, reduced cost/time, spell/save/attack bonus or unprinted explosive creation. On opposed checks only your own eligible total changes. A natural1/20 retains its normal task shift; the bonus cannot abolish it. No re-roll or extra proficiency; zero/negative totals add0.",
  "submittedNewChoices": "Finite variant/task list and explicit10%-of-check-total arithmetic; no invented lore or blanket reward.",
  "submittedWorkedCases": [
    "An eligible Stealth check total19 adds1, becoming20 before task-degree/natural-shift resolution.",
    "A Scrap Goblin's unrelatedMedicine check gets no bonus. An eligible check total−2 remains−2."
  ],
  "decision": "Use actual Goblin variant-favored checks, including Boom/Scrap/Shadow records, with floor10% final nonnegative task total; no extra proficiency or demographic/cosmology claim.",
  "completeAuthoringProcedure": "Require actual Goblin heritage. NEW favored-skill scope is fixed from its actual chosen variant evidence: all Goblins gain Stealth checks through base Nimble Escape; Boom adds INT checks specifically concerning alchemy/explosives/incendiaries under Demolition Expert; Scrap adds WIS Perception to find useful junk or hidden objects and DEX Sleight of Hand to find hidden objects under its printed scavenging clauses; Shadow retains Stealth only. This is a task list derived for the feat, not a cultural truth or a new proficiency grant. On a qualifying actually rolled check, compute ordinary totalT after other legal modifiers, add floor(max(0,T)/10), then compare toDC/opposed total and apply normal task natural-result shifts. This is an explicit NEW10%-of-nonnegative-check-total interpretation of effectiveness, preserving the original percentage rather than substituting a flat bonus. No recursive multiplication, passive-perception multiplier, extra loot, reduced cost/time, spell/save/attack bonus or unprinted explosive creation. On opposed checks only your own eligible total changes. A natural1/20 retains its normal task shift; the bonus cannot abolish it. No re-roll or extra proficiency; zero/negative totals add0.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An eligible Stealth check total19 adds1, becoming20 before task-degree/natural-shift resolution.",
    "A Scrap Goblin's unrelatedMedicine check gets no bonus. An eligible check total−2 remains−2."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Goblin heritage. NEW favored-skill scope is fixed from its actual chosen variant evidence: all Goblins gain Stealth checks through base Nimble Escape; Boom adds INT checks specifically concerning alchemy/explosives/incendiaries under Demolition Expert; Scrap adds WIS Perception to find useful junk or hidden objects and DEX Sleight of Hand to find hidden objects under its printed scavenging clauses; Shadow retains Stealth only. This is a task list derived for the feat, not a cultural truth or a new proficiency grant. On a qualifying actually rolled check, compute ordinary totalT after other legal modifiers, add floor(max(0,T)/10), then compare toDC/opposed total and apply normal task natural-result shifts. This is an explicit NEW10%-of-nonnegative-check-total interpretation of effectiveness, preserving the original percentage rather than substituting a flat bonus. No recursive multiplication, passive-perception multiplier, extra loot, reduced cost/time, spell/save/attack bonus or unprinted explosive creation. On opposed checks only your own eligible total changes. A natural1/20 retains its normal task shift; the bonus cannot abolish it. No re-roll or extra proficiency; zero/negative totals add0.

### Original-position authored review references

```json
[
  {
    "id": "HM-07-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/12"
  },
  {
    "id": "HM-07-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/13"
  }
]
```

## HM-08 — Distorted Dominance

### Complete original object

```json
{
  "id": "distortedDominance",
  "name": "Distorted Dominance",
  "description": "Your aberrant nature overwhelms enemy actions.",
  "prerequisite": "Any Aberrant Mutation",
  "effect": "Enemies who fail saves vs your effects also lose 1 action",
  "type": "Aberrant_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile standalone loss of one action on failed saves versus provisional Warrior4 Aberrant-only Reaction denial. Preserve both texts and any already-reviewed component scope. Resolve target/range/duration/encounter ledger,actual mutation activation and hard-control guard; any retained Action denial requires an explicit bounded decision."
```

### Preserved original source direction (historical)

```json
{
  "featId": "distortedDominance",
  "name": "Distorted Dominance",
  "cohort": "heritage_mutation",
  "questionId": "HM-08",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/7",
  "originalQuestion": "Reconcile standalone loss of one action on failed saves versus provisional Warrior4 Aberrant-only Reaction denial. Preserve both texts and any already-reviewed component scope. Resolve target/range/duration/encounter ledger,actual mutation activation and hard-control guard; any retained Action denial requires an explicit bounded decision.",
  "originalSourceObject": {
    "id": "distortedDominance",
    "name": "Distorted Dominance",
    "description": "Your aberrant nature overwhelms enemy actions.",
    "prerequisite": "Any Aberrant Mutation",
    "effect": "Enemies who fail saves vs your effects also lose 1 action",
    "type": "Aberrant_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "7711b4ea1ada63bf5c62216ba8966638faa0d30694058c453ea7ef45f42c8782",
  "submittedProcedure": "NEW select the Warrior4 counterpart's Reaction denial, explicitly replacing the standalone oneAction loss for this proposal. Require an Aberrant mutation equipped and at least the actual generating Aberrant mutation active. When an actual hostile fails a save against your directly applied Aberrant mutation effect, it loses its Reaction through the end of its next future regular turn. This is triggered, costs no extra action, and is once per actual target per encounter across both catalog representations. Range/target legality comes from that mutation, not an additional universal aura. Source immunity/prevention blocks the applicable rider; do not add Charmed, Stunned, silence, Speed0 or new hard denial. Reaction denial affects ordinary and extra Reaction tokens but does not spend or create them; expiry reveals any other still-operative restriction. A failed save against an unrelated spell, ally effect, periodic damage without a save or equipped-but-dormant mutation does not qualify. No loss of normalAction or guarantee of surrender. Retain the broader original wording as the explicit rejected alternative pending joint decision.",
  "submittedNewChoices": "Named counterpart normalization: qualifying active Aberrant save, once-target-encounter Reaction loss only.",
  "submittedWorkedCases": [
    "A legal active Aberrant effect causes a failedsave; the hostile loses Reactions but still acts/moves on its turn.",
    "A failed save against the Warrior's unrelated ordinary spell does not trigger Distorted Dominance."
  ],
  "decision": "Explicitly select the bounded actual Aberrant mutation-save Reaction denial over broader standalone full-Action denial; preserve historical alternatives and class labels.",
  "completeAuthoringProcedure": "NEW select the Warrior4 counterpart's Reaction denial, explicitly replacing the standalone oneAction loss for this proposal. Require an Aberrant mutation equipped and at least the actual generating Aberrant mutation active. When an actual hostile fails a save against your directly applied Aberrant mutation effect, it loses its Reaction through the end of its next future regular turn. This is triggered, costs no extra action, and is once per actual target per encounter across both catalog representations. Range/target legality comes from that mutation, not an additional universal aura. Source immunity/prevention blocks the applicable rider; do not add Charmed, Stunned, silence, Speed0 or new hard denial. Reaction denial affects ordinary and extra Reaction tokens but does not spend or create them; expiry reveals any other still-operative restriction. A failed save against an unrelated spell, ally effect, periodic damage without a save or equipped-but-dormant mutation does not qualify. No loss of normalAction or guarantee of surrender. Retain the broader original whole-Action-denial wording as the explicitly rejected historical alternative. Adopt this bounded Reaction-denial procedure for the feat candidate; no class record is promoted or overwritten.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A legal active Aberrant effect causes a failedsave; the hostile loses Reactions but still acts/moves on its turn.",
    "A failed save against the Warrior's unrelated ordinary spell does not trigger Distorted Dominance."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW select the Warrior4 counterpart's Reaction denial, explicitly replacing the standalone oneAction loss for this proposal. Require an Aberrant mutation equipped and at least the actual generating Aberrant mutation active. When an actual hostile fails a save against your directly applied Aberrant mutation effect, it loses its Reaction through the end of its next future regular turn. This is triggered, costs no extra action, and is once per actual target per encounter across both catalog representations. Range/target legality comes from that mutation, not an additional universal aura. Source immunity/prevention blocks the applicable rider; do not add Charmed, Stunned, silence, Speed0 or new hard denial. Reaction denial affects ordinary and extra Reaction tokens but does not spend or create them; expiry reveals any other still-operative restriction. A failed save against an unrelated spell, ally effect, periodic damage without a save or equipped-but-dormant mutation does not qualify. No loss of normalAction or guarantee of surrender. Retain the broader original whole-Action-denial wording as the explicitly rejected historical alternative. Adopt this bounded Reaction-denial procedure for the feat candidate; no class record is promoted or overwritten.

### Original-position authored review references

```json
[
  {
    "id": "HM-08-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/14"
  },
  {
    "id": "HM-08-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/15"
  }
]
```

## HM-09 — Elven Grace

### Complete original object

```json
{
  "id": "elven_grace",
  "name": "Elven Grace",
  "description": "Racial feat tied to Elf heritage.",
  "prerequisite": "Elf heritage",
  "effect": "Once per combat, evade any one AoE or ranged attack completely.",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Define Elf heritage,once-per-real-combat ledger,voluntary declaration before/after attack/save,actual action/Reaction and eligible AoE or ranged event. Resolve multiple packets/ongoing zones/automatic damage,damage versus conditions/displacement and zeroHP permissions. No fabricated movement or broad immunity from evade."
```

### Preserved original source direction (historical)

```json
{
  "featId": "elven_grace",
  "name": "Elven Grace",
  "cohort": "heritage_mutation",
  "questionId": "HM-09",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/8",
  "originalQuestion": "Define Elf heritage,once-per-real-combat ledger,voluntary declaration before/after attack/save,actual action/Reaction and eligible AoE or ranged event. Resolve multiple packets/ongoing zones/automatic damage,damage versus conditions/displacement and zeroHP permissions. No fabricated movement or broad immunity from evade.",
  "originalSourceObject": {
    "id": "elven_grace",
    "name": "Elven Grace",
    "description": "Racial feat tied to Elf heritage.",
    "prerequisite": "Elf heritage",
    "effect": "Once per combat, evade any one AoE or ranged attack completely.",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "a026db4cb9e7e2dd9f27e9b57a78b823b36ac8258917252e9a99ebec550a5d2e",
  "submittedProcedure": "Require actual Elf heritage. NEW once per real encounter, while conscious and able to take a Reaction, after one ranged attack result or one instantaneous area-effect/save result against you is known but before any of its consequences commit, spend Reaction/use to evade that one event completely. It can prevent the automatic hit/damage of a legal ranged effect only if the source actually calls it a ranged attack; a save-only single-target spell is not an area attack. A qualifying area event has one simultaneous affected-area resolution, including a breath or explosion. Against you that event deals0damage and applies none of its attached conditions, forced movement or other direct adverse riders; other targets resolve normally. No movement is created and the area/source is not erased. A continuing zone remains: this can evade one eligible initial/tick event, not later independent ticks, entry consequences or the entire duration. Separate missiles/attacks are separate events; one Reaction prevents one. An existing condition, direct HP sacrifice/death without an eligible event or self-chosen cost is not evaded. No use at0HP if ordinary zeroHP Reaction loss applies; no postdeath revival.",
  "submittedNewChoices": "Reaction after result before consequences; complete one-event immunity with finite encounter ledger, no zone deletion.",
  "submittedWorkedCases": [
    "Grace evades one incoming critical arrow and its attachedpoison before damage; another arrow still resolves normally.",
    "Evading an explosion prevents its damage and push on the Elf; the burning ground it leaves can still harm the Elf on a later event."
  ],
  "decision": "Adopt one actual-encounter paid Reaction against its specified ranged attack/area spell event; no movement, independent reroll or later replay, and source defenses remain separate.",
  "completeAuthoringProcedure": "Require actual Elf heritage. NEW once per real encounter, while conscious and able to take a Reaction, after one ranged attack result or one instantaneous area-effect/save result against you is known but before any of its consequences commit, spend Reaction/use to evade that one event completely. It can prevent the automatic hit/damage of a legal ranged effect only if the source actually calls it a ranged attack; a save-only single-target spell is not an area attack. A qualifying area event has one simultaneous affected-area resolution, including a breath or explosion. Against you that event deals0damage and applies none of its attached conditions, forced movement or other direct adverse riders; other targets resolve normally. No movement is created and the area/source is not erased. A continuing zone remains: this can evade one eligible initial/tick event, not later independent ticks, entry consequences or the entire duration. Separate missiles/attacks are separate events; one Reaction prevents one. An existing condition, direct HP sacrifice/death without an eligible event or self-chosen cost is not evaded. No use at0HP if ordinary zeroHP Reaction loss applies; no postdeath revival.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Grace evades one incoming critical arrow and its attachedpoison before damage; another arrow still resolves normally.",
    "Evading an explosion prevents its damage and push on the Elf; the burning ground it leaves can still harm the Elf on a later event."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Elf heritage. NEW once per real encounter, while conscious and able to take a Reaction, after one ranged attack result or one instantaneous area-effect/save result against you is known but before any of its consequences commit, spend Reaction/use to evade that one event completely. It can prevent the automatic hit/damage of a legal ranged effect only if the source actually calls it a ranged attack; a save-only single-target spell is not an area attack. A qualifying area event has one simultaneous affected-area resolution, including a breath or explosion. Against you that event deals0damage and applies none of its attached conditions, forced movement or other direct adverse riders; other targets resolve normally. No movement is created and the area/source is not erased. A continuing zone remains: this can evade one eligible initial/tick event, not later independent ticks, entry consequences or the entire duration. Separate missiles/attacks are separate events; one Reaction prevents one. An existing condition, direct HP sacrifice/death without an eligible event or self-chosen cost is not evaded. No use at0HP if ordinary zeroHP Reaction loss applies; no postdeath revival.

### Original-position authored review references

```json
[
  {
    "id": "HM-09-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/16"
  },
  {
    "id": "HM-09-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/17"
  }
]
```

## HM-10 — Eviscerator Protocol

### Complete original object

```json
{
  "id": "evisceratorProtocol",
  "name": "Eviscerator Protocol",
  "description": "Your enhanced attacks apply debilitating effects.",
  "prerequisite": "Echo Knuckles + Talons mutations",
  "effect": "Free offhand hits now apply Bleed or Weakened (player choice)",
  "type": "Combat_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile Echo Knuckles plus Talons with actual Warpgrip Talons counterpart and Warrior8 gate. Define equipped versus active requirements,one real offhand hit,choice of Bleed/Weakened,source ownership,pulse/expiry/cure/stacking. Preserve reviewed free-attack limits and no recursive on-hit/free-attack generation."
```

### Preserved original source direction (historical)

```json
{
  "featId": "evisceratorProtocol",
  "name": "Eviscerator Protocol",
  "cohort": "heritage_mutation",
  "questionId": "HM-10",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/9",
  "originalQuestion": "Reconcile Echo Knuckles plus Talons with actual Warpgrip Talons counterpart and Warrior8 gate. Define equipped versus active requirements,one real offhand hit,choice of Bleed/Weakened,source ownership,pulse/expiry/cure/stacking. Preserve reviewed free-attack limits and no recursive on-hit/free-attack generation.",
  "originalSourceObject": {
    "id": "evisceratorProtocol",
    "name": "Eviscerator Protocol",
    "description": "Your enhanced attacks apply debilitating effects.",
    "prerequisite": "Echo Knuckles + Talons mutations",
    "effect": "Free offhand hits now apply Bleed or Weakened (player choice)",
    "type": "Combat_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "4509d346eedf1056344dd493cb251f75fe2c520cc9f2d5360fa61b17423cc6d0",
  "submittedProcedure": "NEW require Warrior8, exact Echo Knuckles and Warpgrip Talons equipped and both active when the real Echo Knuckles offhand slam hits. Talons in the standalone source binds only to that actual named card, not every claw. Once per numbered round, immediately on that hit choose one reviewed rider: Mutation Bleed1d4physical at starts of the next two regular target turns, or warrior.weakened−1total damage per weapon/natural-weapon hit, minimum0, until the end of its second future regular turn. NEW use slashing for the otherwise unspecified Bleed physical type; snapshot Warrior techniqueDC for its Medicine cure. Bleed joins current unified family arbitration; losing or suppressed due ticks are consumed normally. Same owner/profile refreshes without extra dice; ordinary positive-potential magical healing ends all eligible automatic-cure Bleeds, and ActionWISMedicine by self/adjacent helper ends one chosen record on success. Weakened does not stack its magnitude with Warpgrip or another warrior.weakened application; independent deadlines remain. No new saving throw or additional free hit. Actual immunity/source restrictions apply. Echo remains once-round, same target/reach and no recursive free attacks; this feat cannot turn the derived hit into another attack grant. Later mutation expiry does not erase an already applied rider unless its own source says so.",
  "submittedNewChoices": "Exact Talons identity, both active, one Echo-hit rider and current reviewed Bleed/Weakened lifecycle.",
  "submittedWorkedCases": [
    "One qualifying offhand hit may apply1d4Bleed for two due starts; it never supplies a second Echo attack.",
    "Applying Weakened to an already−1 warrior.weakened target preserves legal deadlines but never makes−2 from this same profile."
  ],
  "decision": "Unify Warrior8 actual Echo Knuckles/Warpgrip Talons with existing Eviscerator Bleed/Weakened definitions, source cadence and cures; no extra attack or stacking penalty.",
  "completeAuthoringProcedure": "NEW require Warrior8, exact Echo Knuckles and Warpgrip Talons equipped and both active when the real Echo Knuckles offhand slam hits. Talons in the standalone source binds only to that actual named card, not every claw. Once per numbered round, immediately on that hit choose one reviewed rider: Mutation Bleed1d4physical at starts of the next two regular target turns, or warrior.weakened−1total damage per weapon/natural-weapon hit, minimum0, until the end of its second future regular turn. NEW use slashing for the otherwise unspecified Bleed physical type; snapshot Warrior techniqueDC for its Medicine cure. Bleed joins current unified family arbitration; losing or suppressed due ticks are consumed normally. Same owner/profile refreshes without extra dice; ordinary positive-potential magical healing ends all eligible automatic-cure Bleeds, and ActionWISMedicine by self/adjacent helper ends one chosen record on success. Weakened does not stack its magnitude with Warpgrip or another warrior.weakened application; independent deadlines remain. No new saving throw or additional free hit. Actual immunity/source restrictions apply. Echo remains once-round, same target/reach and no recursive free attacks; this feat cannot turn the derived hit into another attack grant. Later mutation expiry does not erase an already applied rider unless its own source says so.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "One qualifying offhand hit may apply1d4Bleed for two due starts; it never supplies a second Echo attack.",
    "Applying Weakened to an already−1 warrior.weakened target preserves legal deadlines but never makes−2 from this same profile."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW require Warrior8, exact Echo Knuckles and Warpgrip Talons equipped and both active when the real Echo Knuckles offhand slam hits. Talons in the standalone source binds only to that actual named card, not every claw. Once per numbered round, immediately on that hit choose one reviewed rider: Mutation Bleed1d4physical at starts of the next two regular target turns, or warrior.weakened−1total damage per weapon/natural-weapon hit, minimum0, until the end of its second future regular turn. NEW use slashing for the otherwise unspecified Bleed physical type; snapshot Warrior techniqueDC for its Medicine cure. Bleed joins current unified family arbitration; losing or suppressed due ticks are consumed normally. Same owner/profile refreshes without extra dice; ordinary positive-potential magical healing ends all eligible automatic-cure Bleeds, and ActionWISMedicine by self/adjacent helper ends one chosen record on success. Weakened does not stack its magnitude with Warpgrip or another warrior.weakened application; independent deadlines remain. No new saving throw or additional free hit. Actual immunity/source restrictions apply. Echo remains once-round, same target/reach and no recursive free attacks; this feat cannot turn the derived hit into another attack grant. Later mutation expiry does not erase an already applied rider unless its own source says so.

### Original-position authored review references

```json
[
  {
    "id": "HM-10-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/18"
  },
  {
    "id": "HM-10-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/19"
  }
]
```

## HM-11 — Evolution Under Fire

### Complete original object

```json
{
  "id": "evolutionUnderFire",
  "name": "Evolution Under Fire",
  "description": "Severe damage triggers rapid adaptation.",
  "prerequisite": "Any Apex Mutation",
  "effect": "When you take >15 damage from a single hit, reduce cooldowns by 1 round",
  "type": "Vital_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile single hit>15 versus counterpart actual damage event>15,Warrior16,one positive Warrior recharge counter and once-per-round shortening cap. Specify mitigation/tempHP/ward quantities,threshold exactness,which counter,active Apex requirement and no spent rest-use restoration."
```

### Preserved original source direction (historical)

```json
{
  "featId": "evolutionUnderFire",
  "name": "Evolution Under Fire",
  "cohort": "heritage_mutation",
  "questionId": "HM-11",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/10",
  "originalQuestion": "Reconcile single hit>15 versus counterpart actual damage event>15,Warrior16,one positive Warrior recharge counter and once-per-round shortening cap. Specify mitigation/tempHP/ward quantities,threshold exactness,which counter,active Apex requirement and no spent rest-use restoration.",
  "originalSourceObject": {
    "id": "evolutionUnderFire",
    "name": "Evolution Under Fire",
    "description": "Severe damage triggers rapid adaptation.",
    "prerequisite": "Any Apex Mutation",
    "effect": "When you take >15 damage from a single hit, reduce cooldowns by 1 round",
    "type": "Vital_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "44a9ae55dec6ecb64242bab25064033c4dbbd91ac72c4b607ee65dbde77e5326",
  "submittedProcedure": "NEW adopt Warrior16, an actual Apex equipped and active, and the counterpart one damage-event definition in place of single-hit-only wording. After one hostile-caused event deals numeric actualDamageDealt greater than15 to you and you survive with the Apex still active, you may shorten one positive Warrior round-recharge counter by1, minimum0, at most once per numbered round. TempHP actually absorbed counts; uncapped resolved/post-temp amounts and overkill do not. Sixteen qualifies, fifteen does not. Mixed types from one event add once; separate hits never combine. Choose an actual acquired Warrior ability with a positive counter that has not already received its one reset/shortening this round; this consumes that ability's shared shortening allowance. A zero counter, RP, serum dose, Mutation Reserve, BT, SR/LR use or another class's counter is ineligible. Recheck after fatal/threshold consequences; Butcherform ending belowquarter prevents its use as the required activeApex. Friendly/staged/self damage and HP sacrifice cannot farm recharge. Outside a real encounter there is no hostile round-shortening loop.",
  "submittedNewChoices": "ActiveApex and hostile numeric actual damage>15, one counter and one round cap; counterpart event scope explicit.",
  "submittedWorkedCases": [
    "An enemy event absorbs10tempHP and removes6normalHP:16actual permits shorteningRecharge2 to1.",
    "AtHP3 with no tempHP a20damage hit has at most3actualHPdamage before other replacement limits; it does not meet16, even though raw damage was20."
  ],
  "decision": "Unify Warrior16 active Apex and>15 actual-damage packet predicate; shorten one positive Warrior Recharge once, not RP, serum, rest or every counter.",
  "completeAuthoringProcedure": "NEW adopt Warrior16, an actual Apex equipped and active, and the counterpart one damage-event definition in place of single-hit-only wording. After one hostile-caused event deals numeric actualDamageDealt greater than15 to you and you survive with the Apex still active, you may shorten one positive Warrior round-recharge counter by1, minimum0, at most once per numbered round. TempHP actually absorbed counts; uncapped resolved/post-temp amounts and overkill do not. Sixteen qualifies, fifteen does not. Mixed types from one event add once; separate hits never combine. Choose an actual acquired Warrior ability with a positive counter that has not already received its one reset/shortening this round; this consumes that ability's shared shortening allowance. A zero counter, RP, serum dose, Mutation Reserve, BT, SR/LR use or another class's counter is ineligible. Recheck after fatal/threshold consequences; Butcherform ending belowquarter prevents its use as the required activeApex. Friendly/staged/self damage and HP sacrifice cannot farm recharge. Outside a real encounter there is no hostile round-shortening loop.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An enemy event absorbs10tempHP and removes6normalHP:16actual permits shorteningRecharge2 to1.",
    "AtHP3 with no tempHP a20damage hit has at most3actualHPdamage before other replacement limits; it does not meet16, even though raw damage was20."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW adopt Warrior16, an actual Apex equipped and active, and the counterpart one damage-event definition in place of single-hit-only wording. After one hostile-caused event deals numeric actualDamageDealt greater than15 to you and you survive with the Apex still active, you may shorten one positive Warrior round-recharge counter by1, minimum0, at most once per numbered round. TempHP actually absorbed counts; uncapped resolved/post-temp amounts and overkill do not. Sixteen qualifies, fifteen does not. Mixed types from one event add once; separate hits never combine. Choose an actual acquired Warrior ability with a positive counter that has not already received its one reset/shortening this round; this consumes that ability's shared shortening allowance. A zero counter, RP, serum dose, Mutation Reserve, BT, SR/LR use or another class's counter is ineligible. Recheck after fatal/threshold consequences; Butcherform ending belowquarter prevents its use as the required activeApex. Friendly/staged/self damage and HP sacrifice cannot farm recharge. Outside a real encounter there is no hostile round-shortening loop.

### Original-position authored review references

```json
[
  {
    "id": "HM-11-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/20"
  },
  {
    "id": "HM-11-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/21"
  }
]
```

## HM-12 — Glamourborn

### Complete original object

```json
{
  "id": "glamourborn",
  "name": "Glamourborn",
  "description": "Racial feat tied to Feykin heritage.",
  "prerequisite": "Feykin heritage",
  "effect": "Enemies attacking you for the first time have a 20% miss chance.",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind Feykin heritage,each enemy first attack timing and what resets that record. Define actual20percent miss roll,order versus attack/critical/advantage,ranged/melee/spell attacks,unseen enemies,multiple attacks and invalid declarations. No spell-save immunity,invisibility or Fey cosmology inference."
```

### Preserved original source direction (historical)

```json
{
  "featId": "glamourborn",
  "name": "Glamourborn",
  "cohort": "heritage_mutation",
  "questionId": "HM-12",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/11",
  "originalQuestion": "Bind Feykin heritage,each enemy first attack timing and what resets that record. Define actual20percent miss roll,order versus attack/critical/advantage,ranged/melee/spell attacks,unseen enemies,multiple attacks and invalid declarations. No spell-save immunity,invisibility or Fey cosmology inference.",
  "originalSourceObject": {
    "id": "glamourborn",
    "name": "Glamourborn",
    "description": "Racial feat tied to Feykin heritage.",
    "prerequisite": "Feykin heritage",
    "effect": "Enemies attacking you for the first time have a 20% miss chance.",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "aa5718e459649c40b43c21d3d9fde48f83a87ae4071812a61308d8de28725d92",
  "submittedProcedure": "Require actual Feykin heritage. NEW for each actual hostile identity in one real encounter, its first legally declared attack against you faces a20% miss check: roll1d100 once,1–20 makes that attack miss,21–100 proceeds normally. Commit the attacker's action, ammunition and source costs first, then roll this check before its ordinary attack die or automatic-hit resolution. The first legal attack consumes that attacker's encounter record even if the percentage check succeeds or its later attack roll would miss. No record is spent by an illegal/out-of-range declaration. It applies to real melee/ranged weapon, unarmed and spell attacks, including a source-qualified automatic-hit attack; an automatic damaging effect without attack classification, save-only effect, ongoing tick or environmental damage is not an attack. A blocked first attack has no on-hit/critical result, but actual miss riders can operate. For a multiattack sequence only its first attack faces this roll; one attack with several components faces one check. No sight requirement on either combatant is invented. Leaving/reentering, disguise, charm changes or a new form of the same attacker never resets the record. This is a supernatural feat defense with no creature-type, invisibility or cosmology grant.",
  "submittedNewChoices": "Exactd10020% stage, first legal attack per hostile identity per encounter, no saving-effect immunity.",
  "submittedWorkedCases": [
    "The first enemy arrow rolls17 on the miss check and misses; its ammunition is spent and its second arrow rolls normally.",
    "An enemy first uses a save-only spell, then a sword attack: the sword is still its first qualifying attack against you."
  ],
  "decision": "Adopt first actual enemy attack/encounter20% miss procedure with preserved hostile attempt cost; no automatic later immunity, extra illusion body or rerolled first opportunity.",
  "completeAuthoringProcedure": "Require actual Feykin heritage. NEW for each actual hostile identity in one real encounter, its first legally declared attack against you faces a20% miss check: roll1d100 once,1–20 makes that attack miss,21–100 proceeds normally. Commit the attacker's action, ammunition and source costs first, then roll this check before its ordinary attack die or automatic-hit resolution. The first legal attack consumes that attacker's encounter record even if the percentage check succeeds or its later attack roll would miss. No record is spent by an illegal/out-of-range declaration. It applies to real melee/ranged weapon, unarmed and spell attacks, including a source-qualified automatic-hit attack; an automatic damaging effect without attack classification, save-only effect, ongoing tick or environmental damage is not an attack. A blocked first attack has no on-hit/critical result, but actual miss riders can operate. For a multiattack sequence only its first attack faces this roll; one attack with several components faces one check. No sight requirement on either combatant is invented. Leaving/reentering, disguise, charm changes or a new form of the same attacker never resets the record. This is a supernatural feat defense with no creature-type, invisibility or cosmology grant.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "The first enemy arrow rolls17 on the miss check and misses; its ammunition is spent and its second arrow rolls normally.",
    "An enemy first uses a save-only spell, then a sword attack: the sword is still its first qualifying attack against you."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Feykin heritage. NEW for each actual hostile identity in one real encounter, its first legally declared attack against you faces a20% miss check: roll1d100 once,1–20 makes that attack miss,21–100 proceeds normally. Commit the attacker's action, ammunition and source costs first, then roll this check before its ordinary attack die or automatic-hit resolution. The first legal attack consumes that attacker's encounter record even if the percentage check succeeds or its later attack roll would miss. No record is spent by an illegal/out-of-range declaration. It applies to real melee/ranged weapon, unarmed and spell attacks, including a source-qualified automatic-hit attack; an automatic damaging effect without attack classification, save-only effect, ongoing tick or environmental damage is not an attack. A blocked first attack has no on-hit/critical result, but actual miss riders can operate. For a multiattack sequence only its first attack faces this roll; one attack with several components faces one check. No sight requirement on either combatant is invented. Leaving/reentering, disguise, charm changes or a new form of the same attacker never resets the record. This is a supernatural feat defense with no creature-type, invisibility or cosmology grant.

### Original-position authored review references

```json
[
  {
    "id": "HM-12-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/22"
  },
  {
    "id": "HM-12-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/23"
  }
]
```

## HM-13 — Hypermutation Spike

### Complete original object

```json
{
  "id": "hypermutationSpike",
  "name": "Hypermutation Spike",
  "description": "Extend your apex transformation beyond normal limits.",
  "prerequisite": "Butcherform Chassis (Apex) mutation",
  "effect": "Once per long rest, extend Butcherform to 5 rounds and become immune to stun/slow during duration",
  "type": "Combat_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile source stun/slow immunity with Warrior16 five-round Butcherform and the reviewed per-mode Speed-floor procedure. Define one activation,Long Rest expenditure,currentHP quarter-threshold ending,loss/suppression/return and Stunned scope. Keep existing physical restraint and root rules; no broad immunity created from slow wording."
```

### Preserved original source direction (historical)

```json
{
  "featId": "hypermutationSpike",
  "name": "Hypermutation Spike",
  "cohort": "heritage_mutation",
  "questionId": "HM-13",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/12",
  "originalQuestion": "Reconcile source stun/slow immunity with Warrior16 five-round Butcherform and the reviewed per-mode Speed-floor procedure. Define one activation,Long Rest expenditure,currentHP quarter-threshold ending,loss/suppression/return and Stunned scope. Keep existing physical restraint and root rules; no broad immunity created from slow wording.",
  "originalSourceObject": {
    "id": "hypermutationSpike",
    "name": "Hypermutation Spike",
    "description": "Extend your apex transformation beyond normal limits.",
    "prerequisite": "Butcherform Chassis (Apex) mutation",
    "effect": "Once per long rest, extend Butcherform to 5 rounds and become immune to stun/slow during duration",
    "type": "Combat_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "ef0301d7d1b55d27c7f4156f8d24bc05d0d2c47cf80b63cfeae280fb3ccede06",
  "submittedProcedure": "NEW use Warrior16, actual equipped Butcherform Chassis and its legal activation. At that activation, optionally spend this feat's1/LR use to set that activation's maximum duration to five rounds instead of three, retaining its original owner regular-start expiry clock and all shorter ending conditions. It is one enhanced activation, not five additional rounds, a later free extension or a refreshed serum dose. CurrentHP strictly below one-quarter effective maximum ends Butcherform and this enhancement immediately; exact quarter remains legal. Increasing maximum can end it. During that same active unsuppressed activation, immune to Stunned and apply the already reviewed Hypermutation per-mode Speed floor: snapshot ordinary permanent/qualifying-persistent sheet modes at activation, excluding temporary buffs, stances, Strain, cargo, Exhaustion and the feat; floor for each is floor(snapshot/2). Apply after numeric changes/multipliers, but never defeat explicit Speed0, Root, Grappled/Restrained, Exhaustion5, absent modes, terrain costs or separate voluntary-movement prohibition. The standalone broad slow immunity is explicitly normalized to this reviewed narrower floor. Temporary suppression disables both new benefits while clocks continue; unsuppression before true expiry returns the same snapshot/use, never a fresh five rounds. Actual ended mutation cannot return without new paid activation. Stunned records follow current immunity/suppression rules; the feat does not erase unrelated conditions.",
  "submittedNewChoices": "One1/LR activation and five-round maximum, active Stun immunity plus exact reviewed Speed snapshot/floor rather than generic slow immunity.",
  "submittedWorkedCases": [
    "An ordinary capturedwalk30 has floor15, but a realGrappled record still makes movement unavailable.",
    "HP10/max40 remains exactlyquarter; max rising to41 ends Butcherform without damage and loses the enhancement."
  ],
  "decision": "Unify Warrior16 active Butcherform, one LR extension3→5 rounds and bounded Stun/Speed floor; actual below-quarter endpoint and other immobility remain.",
  "completeAuthoringProcedure": "NEW use Warrior16, actual equipped Butcherform Chassis and its legal activation. At that activation, optionally spend this feat's1/LR use to set that activation's maximum duration to five rounds instead of three, retaining its original owner regular-start expiry clock and all shorter ending conditions. It is one enhanced activation, not five additional rounds, a later free extension or a refreshed serum dose. CurrentHP strictly below one-quarter effective maximum ends Butcherform and this enhancement immediately; exact quarter remains legal. Increasing maximum can end it. During that same active unsuppressed activation, immune to Stunned and apply the already reviewed Hypermutation per-mode Speed floor: snapshot ordinary permanent/qualifying-persistent sheet modes at activation, excluding temporary buffs, stances, Strain, cargo, Exhaustion and the feat; floor for each is floor(snapshot/2). Apply after numeric changes/multipliers, but never defeat explicit Speed0, Root, Grappled/Restrained, Exhaustion5, absent modes, terrain costs or separate voluntary-movement prohibition. The standalone broad slow immunity is explicitly normalized to this reviewed narrower floor. Temporary suppression disables both new benefits while clocks continue; unsuppression before true expiry returns the same snapshot/use, never a fresh five rounds. Actual ended mutation cannot return without new paid activation. Stunned records follow current immunity/suppression rules; the feat does not erase unrelated conditions.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An ordinary capturedwalk30 has floor15, but a realGrappled record still makes movement unavailable.",
    "HP10/max40 remains exactlyquarter; max rising to41 ends Butcherform without damage and loses the enhancement."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW use Warrior16, actual equipped Butcherform Chassis and its legal activation. At that activation, optionally spend this feat's1/LR use to set that activation's maximum duration to five rounds instead of three, retaining its original owner regular-start expiry clock and all shorter ending conditions. It is one enhanced activation, not five additional rounds, a later free extension or a refreshed serum dose. CurrentHP strictly below one-quarter effective maximum ends Butcherform and this enhancement immediately; exact quarter remains legal. Increasing maximum can end it. During that same active unsuppressed activation, immune to Stunned and apply the already reviewed Hypermutation per-mode Speed floor: snapshot ordinary permanent/qualifying-persistent sheet modes at activation, excluding temporary buffs, stances, Strain, cargo, Exhaustion and the feat; floor for each is floor(snapshot/2). Apply after numeric changes/multipliers, but never defeat explicit Speed0, Root, Grappled/Restrained, Exhaustion5, absent modes, terrain costs or separate voluntary-movement prohibition. The standalone broad slow immunity is explicitly normalized to this reviewed narrower floor. Temporary suppression disables both new benefits while clocks continue; unsuppression before true expiry returns the same snapshot/use, never a fresh five rounds. Actual ended mutation cannot return without new paid activation. Stunned records follow current immunity/suppression rules; the feat does not erase unrelated conditions.

### Original-position authored review references

```json
[
  {
    "id": "HM-13-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/24"
  },
  {
    "id": "HM-13-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/25"
  }
]
```

## HM-14 — Juggernaut's Core

### Complete original object

```json
{
  "id": "juggernautCore",
  "name": "Juggernaut's Core",
  "description": "Your ossified core provides protection against precision attacks.",
  "prerequisite": "Ossified Core mutation",
  "effect": "If you are immune to critical hits, gain resistance to sneak attack damage",
  "type": "Vital_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile critical immunity condition with actual Ossified Core suppression of extra critical dice and Warrior8 precision-damage halving. Define active mutation,actual Sneak Attack/other precision scope,only the extra component,rounding/order versus resistance and mixed types. Ordinary weapon damage and critical-trigger effects remain distinct."
```

### Preserved original source direction (historical)

```json
{
  "featId": "juggernautCore",
  "name": "Juggernaut's Core",
  "cohort": "heritage_mutation",
  "questionId": "HM-14",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/13",
  "originalQuestion": "Reconcile critical immunity condition with actual Ossified Core suppression of extra critical dice and Warrior8 precision-damage halving. Define active mutation,actual Sneak Attack/other precision scope,only the extra component,rounding/order versus resistance and mixed types. Ordinary weapon damage and critical-trigger effects remain distinct.",
  "originalSourceObject": {
    "id": "juggernautCore",
    "name": "Juggernaut's Core",
    "description": "Your ossified core provides protection against precision attacks.",
    "prerequisite": "Ossified Core mutation",
    "effect": "If you are immune to critical hits, gain resistance to sneak attack damage",
    "type": "Vital_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "cb0bdd2c20d23150ad6c849d2134e033c09140af9355f4ea2acb50afb77a577f",
  "submittedProcedure": "NEW require Warrior8 and equipped/active Ossified Core. Its existing extra-critical-dice prevention is the qualifying critical-protection state; the feat does not declare every critical hit a normal hit or prevent critical-triggered riders. Adopt the counterpart scope: halve only bonus damage explicitly identified by an actual source as Sneak Attack or equivalent precision damage. A critical, poison, elemental infusion, spell rider or ordinary ability modifier is not automatically precision. NEW this halving is a source-specific precision resistance layer: halve each typed precision component once, rounding down; an existing same-type damage resistance also covering that component does not halve it again. Other nonprecision damage remains subject to its own ordinary defenses; vulnerability/immunity and fixed reduction use current damage ordering. If mixed precision types have already been separated, apply their own immunity/resistance once each; do not halve the entire weapon packet because one part is precision. Ossified's separate post-resistance piercing−2 applies once by its own event contract. Benefits stop when Ossified is not active. No new resistance to every critical or all physical damage.",
  "submittedNewChoices": "Ossified-specific qualification, explicit source-tagged precision component and one same-component resistance calculation.",
  "submittedWorkedCases": [
    "A piercing hit has8ordinary plus7Sneak Attack: the feat makes precision3, producing11 before other applicable fixed defenses.",
    "If piercing resistance already halves both parts, the7precision becomes3 once; Juggernaut's Core does not quarter it to1."
  ],
  "decision": "Unify Warrior8 active Ossified Carapace with native critical-die/PierceDR and half separately identified sneak-like extras; no whole-hit halving or duplicate crit immunity.",
  "completeAuthoringProcedure": "NEW require Warrior8 and equipped/active Ossified Core. Its existing extra-critical-dice prevention is the qualifying critical-protection state; the feat does not declare every critical hit a normal hit or prevent critical-triggered riders. Adopt the counterpart scope: halve only bonus damage explicitly identified by an actual source as Sneak Attack or equivalent precision damage. A critical, poison, elemental infusion, spell rider or ordinary ability modifier is not automatically precision. NEW this halving is a source-specific precision resistance layer: halve each typed precision component once, rounding down; an existing same-type damage resistance also covering that component does not halve it again. Other nonprecision damage remains subject to its own ordinary defenses; vulnerability/immunity and fixed reduction use current damage ordering. If mixed precision types have already been separated, apply their own immunity/resistance once each; do not halve the entire weapon packet because one part is precision. Ossified's separate post-resistance piercing−2 applies once by its own event contract. Benefits stop when Ossified is not active. No new resistance to every critical or all physical damage.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A piercing hit has8ordinary plus7Sneak Attack: the feat makes precision3, producing11 before other applicable fixed defenses.",
    "If piercing resistance already halves both parts, the7precision becomes3 once; Juggernaut's Core does not quarter it to1."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW require Warrior8 and equipped/active Ossified Core. Its existing extra-critical-dice prevention is the qualifying critical-protection state; the feat does not declare every critical hit a normal hit or prevent critical-triggered riders. Adopt the counterpart scope: halve only bonus damage explicitly identified by an actual source as Sneak Attack or equivalent precision damage. A critical, poison, elemental infusion, spell rider or ordinary ability modifier is not automatically precision. NEW this halving is a source-specific precision resistance layer: halve each typed precision component once, rounding down; an existing same-type damage resistance also covering that component does not halve it again. Other nonprecision damage remains subject to its own ordinary defenses; vulnerability/immunity and fixed reduction use current damage ordering. If mixed precision types have already been separated, apply their own immunity/resistance once each; do not halve the entire weapon packet because one part is precision. Ossified's separate post-resistance piercing−2 applies once by its own event contract. Benefits stop when Ossified is not active. No new resistance to every critical or all physical damage.

### Original-position authored review references

```json
[
  {
    "id": "HM-14-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/26"
  },
  {
    "id": "HM-14-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/27"
  }
]
```

## HM-15 — Kill-Chain Adaptation

### Complete original object

```json
{
  "id": "killChainAdaptation",
  "name": "Kill-Chain Adaptation",
  "description": "Successful kills enhance your combat capabilities.",
  "prerequisite": "2 Combat Mutations",
  "effect": "After a melee kill, gain +10 ft movement and +1 to hit",
  "type": "Combat_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile melee kill with Warrior4 counterpart meaningful-hostile zeroHP,once per round,next-melee-attack+1 and Speed+10 until next regular-turn end. Define dying/dead distinction,ownership,refresh/stacking,actual mutation activation and movement already spent. Preserve anti-farming and no additional full Action."
```

### Preserved original source direction (historical)

```json
{
  "featId": "killChainAdaptation",
  "name": "Kill-Chain Adaptation",
  "cohort": "heritage_mutation",
  "questionId": "HM-15",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/14",
  "originalQuestion": "Reconcile melee kill with Warrior4 counterpart meaningful-hostile zeroHP,once per round,next-melee-attack+1 and Speed+10 until next regular-turn end. Define dying/dead distinction,ownership,refresh/stacking,actual mutation activation and movement already spent. Preserve anti-farming and no additional full Action.",
  "originalSourceObject": {
    "id": "killChainAdaptation",
    "name": "Kill-Chain Adaptation",
    "description": "Successful kills enhance your combat capabilities.",
    "prerequisite": "2 Combat Mutations",
    "effect": "After a melee kill, gain +10 ft movement and +1 to hit",
    "type": "Combat_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "7209e94e343e4b4666a39978e86e2f8f5981fd1537ff5b9d4db9aeaea17e2e89",
  "submittedProcedure": "NEW require Warrior4 and two actual Combat mutations equipped and active at the trigger. Once per numbered round, after your personal direct melee attack reduces an independent meaningful hostile from positiveHP to0, gain+10ft to each existing usable Speed mode and one+1 entitlement on your next melee attack roll, both ending at the end of your next future original regular turn. This intentionally selects the counterpart zeroHP trigger rather than requiring actual death; resolve floors/knockout/death replacements first. The trigger grants no attack or fullAction. Copies, owned companion damage, ongoing ticks, captives, harmless targets and recycled bodies do not qualify. Modes derived from another Speed include this bonus once, not twice; previously spent movement remains spent. The attack entitlement consumes on the next legal melee attack roll, hit or miss; a save-only melee effect does not consume it. Same-family new trigger may refresh an unexpired record under the once-round cap but never gives+20ft or queued+1s. It ends if required equipped or active mutation eligibility is lost, even before its deadline. Encounter transitions do not extend or refresh either benefit.",
  "submittedNewChoices": "Warrior4 and two activeCombat, genuine positive-to-zero trigger, one round grant with bounded Speed and nextattack effects.",
  "submittedWorkedCases": [
    "A qualifying melee down adds10 towalk30, but moving30 earlier still leaves only10 ordinary movement after the newSpeed40.",
    "A second down in the same round adds nothing. The next legal melee attack consumes+1 even if it misses."
  ],
  "decision": "Unify Warrior4/two active Combat mutations and genuine positive-to-zero trigger; death not required, one per round and no copied or staged rewards.",
  "completeAuthoringProcedure": "NEW require Warrior4 and two actual Combat mutations equipped and active at the trigger. Once per numbered round, after your personal direct melee attack reduces an independent meaningful hostile from positiveHP to0, gain+10ft to each existing usable Speed mode and one+1 entitlement on your next melee attack roll, both ending at the end of your next future original regular turn. This intentionally selects the counterpart zeroHP trigger rather than requiring actual death; resolve floors/knockout/death replacements first. The trigger grants no attack or fullAction. Copies, owned companion damage, ongoing ticks, captives, harmless targets and recycled bodies do not qualify. Modes derived from another Speed include this bonus once, not twice; previously spent movement remains spent. The attack entitlement consumes on the next legal melee attack roll, hit or miss; a save-only melee effect does not consume it. Same-family new trigger may refresh an unexpired record under the once-round cap but never gives+20ft or queued+1s. It ends if required equipped or active mutation eligibility is lost, even before its deadline. Encounter transitions do not extend or refresh either benefit.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A qualifying melee down adds10 towalk30, but moving30 earlier still leaves only10 ordinary movement after the newSpeed40.",
    "A second down in the same round adds nothing. The next legal melee attack consumes+1 even if it misses."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW require Warrior4 and two actual Combat mutations equipped and active at the trigger. Once per numbered round, after your personal direct melee attack reduces an independent meaningful hostile from positiveHP to0, gain+10ft to each existing usable Speed mode and one+1 entitlement on your next melee attack roll, both ending at the end of your next future original regular turn. This intentionally selects the counterpart zeroHP trigger rather than requiring actual death; resolve floors/knockout/death replacements first. The trigger grants no attack or fullAction. Copies, owned companion damage, ongoing ticks, captives, harmless targets and recycled bodies do not qualify. Modes derived from another Speed include this bonus once, not twice; previously spent movement remains spent. The attack entitlement consumes on the next legal melee attack roll, hit or miss; a save-only melee effect does not consume it. Same-family new trigger may refresh an unexpired record under the once-round cap but never gives+20ft or queued+1s. It ends if required equipped or active mutation eligibility is lost, even before its deadline. Encounter transitions do not extend or refresh either benefit.

### Original-position authored review references

```json
[
  {
    "id": "HM-15-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/28"
  },
  {
    "id": "HM-15-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/29"
  }
]
```

## HM-16 — Living Fortress

### Complete original object

```json
{
  "id": "livingFortress",
  "name": "Living Fortress",
  "description": "Multiple vital mutations make you nearly impregnable.",
  "prerequisite": "3 Vital Mutations active",
  "effect": "Gain immunity to flanking",
  "type": "Vital_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind three actually active Vital mutations against real slot/active limits and temporary exceptions; resolve equipped-only prerequisite versus active benefit and Warrior8 gate. Identify actual flanking rule before denying its sole advantage. Do not erase other advantage sources,nearby allies or tactical positioning effects by an undefined blanket immunity."
```

### Preserved original source direction (historical)

```json
{
  "featId": "livingFortress",
  "name": "Living Fortress",
  "cohort": "heritage_mutation",
  "questionId": "HM-16",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/15",
  "originalQuestion": "Bind three actually active Vital mutations against real slot/active limits and temporary exceptions; resolve equipped-only prerequisite versus active benefit and Warrior8 gate. Identify actual flanking rule before denying its sole advantage. Do not erase other advantage sources,nearby allies or tactical positioning effects by an undefined blanket immunity.",
  "originalSourceObject": {
    "id": "livingFortress",
    "name": "Living Fortress",
    "description": "Multiple vital mutations make you nearly impregnable.",
    "prerequisite": "3 Vital Mutations active",
    "effect": "Gain immunity to flanking",
    "type": "Vital_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "f1f8c7514cb89be321856a95c372b3b7a6c2311c6e21d50d443c80c65620294b",
  "submittedProcedure": "NEW require Warrior8 and three actual Vital mutations equipped for acquisition; the benefit operates only while at least three distinct Vital mutations are actually active. No feat adds slots or active limits: the Warrior must have actual unlocked slots and an expressly acquired temporary active-count exception where needed. A Warrior8 normally cannot equip three mutations, so the printed level is a minimum rather than proof of present eligibility. Selected doctrine is the counterpart precise protection: opponents receive no advantage solely from a source explicitly granting advantage for flanking you. Reviewed ordinary combat has no global flanking advantage; this feat does not invent one. Independent unseen/Restrained/other advantage survives. It does not erase nearby bodies, ally assistance, legal target geometry, Tactical Flanker's separately proposed damage die, attacks or cover. When any required active state ends/suppresses, protection immediately stops; restoration within existing durations can restore protection without new actions or resources. No numericalAC/DR or immunity to all positioning effects.",
  "submittedNewChoices": "Actual three-equipped/three-active feasibility and sole flanking-advantage protection; no fictitious slot unlock.",
  "submittedWorkedCases": [
    "Three Vital mutations active through a real temporary exception protect against an actual flanking-advantage feature.",
    "With only two active mutations, having the third equipped dormant grants no benefit; unrelated attack advantage is never removed."
  ],
  "decision": "Unify Warrior8/three Vital equipped acquisition with three genuinely active at use; do not unlock slots/activation capacity or suppress unrelated Tactical Flanker riders.",
  "completeAuthoringProcedure": "NEW require Warrior8 and three actual Vital mutations equipped for acquisition; the benefit operates only while at least three distinct Vital mutations are actually active. No feat adds slots or active limits: the Warrior must have actual unlocked slots and an expressly acquired temporary active-count exception where needed. A Warrior8 normally cannot equip three mutations, so the printed level is a minimum rather than proof of present eligibility. Selected doctrine is the counterpart precise protection: opponents receive no advantage solely from a source explicitly granting advantage for flanking you. Reviewed ordinary combat has no global flanking advantage; this feat does not invent one. Independent unseen/Restrained/other advantage survives. It does not erase nearby bodies, ally assistance, legal target geometry, Tactical Flanker's separately proposed damage die, attacks or cover. When any required active state ends/suppresses, protection immediately stops; restoration within existing durations can restore protection without new actions or resources. No numericalAC/DR or immunity to all positioning effects.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Three Vital mutations active through a real temporary exception protect against an actual flanking-advantage feature.",
    "With only two active mutations, having the third equipped dormant grants no benefit; unrelated attack advantage is never removed."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW require Warrior8 and three actual Vital mutations equipped for acquisition; the benefit operates only while at least three distinct Vital mutations are actually active. No feat adds slots or active limits: the Warrior must have actual unlocked slots and an expressly acquired temporary active-count exception where needed. A Warrior8 normally cannot equip three mutations, so the printed level is a minimum rather than proof of present eligibility. Selected doctrine is the counterpart precise protection: opponents receive no advantage solely from a source explicitly granting advantage for flanking you. Reviewed ordinary combat has no global flanking advantage; this feat does not invent one. Independent unseen/Restrained/other advantage survives. It does not erase nearby bodies, ally assistance, legal target geometry, Tactical Flanker's separately proposed damage die, attacks or cover. When any required active state ends/suppresses, protection immediately stops; restoration within existing durations can restore protection without new actions or resources. No numericalAC/DR or immunity to all positioning effects.

### Original-position authored review references

```json
[
  {
    "id": "HM-16-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/30"
  },
  {
    "id": "HM-16-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/31"
  },
  {
    "id": "FA-23",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/additionalBoundaryReviews/2"
  }
]
```

## HM-17 — Nightfang Training

### Complete original object

```json
{
  "id": "nightfang_training",
  "name": "Nightfang Training",
  "description": "Racial feat tied to Umbrin heritage.",
  "prerequisite": "Umbrin heritage",
  "effect": "You gain +10% damage and +2 stealth in total darkness.",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind Umbrin heritage,total darkness and actual senses without granting sight. Define10percent damage sources,packets/critical/rounding/resistance and+2 Stealth ability checks; require legal hiding. Preserve bright/dim versus total-dark boundaries and do not change ancestry/origin."
```

### Preserved original source direction (historical)

```json
{
  "featId": "nightfang_training",
  "name": "Nightfang Training",
  "cohort": "heritage_mutation",
  "questionId": "HM-17",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/16",
  "originalQuestion": "Bind Umbrin heritage,total darkness and actual senses without granting sight. Define10percent damage sources,packets/critical/rounding/resistance and+2 Stealth ability checks; require legal hiding. Preserve bright/dim versus total-dark boundaries and do not change ancestry/origin.",
  "originalSourceObject": {
    "id": "nightfang_training",
    "name": "Nightfang Training",
    "description": "Racial feat tied to Umbrin heritage.",
    "prerequisite": "Umbrin heritage",
    "effect": "You gain +10% damage and +2 stealth in total darkness.",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "957a886781d983fde31235df60589280ab12669ccf39e516e292b65f2ba0ac7e",
  "submittedProcedure": "Require actual Umbrin heritage. While your actual occupied space is in total darkness, gain+2 to actualDEXStealth checks and add floor(native damage/10) to each eligible personal direct attack/spell damage event. NEW your whole occupied footprint must be dark, not dim or partly illuminated; determine this independently from darkvision, which changes perception rather than illumination. It grants no ability to see targets, Hide automatically or ignore your actual Sunlight Sensitivity. Damage bonus uses the already proposed common pre-percentage base after critical dice/flat additions and before defenses; allocate increment across native typed components by proportional largest remainder with stable ties. Count direct initial attacks/spell resolutions, not copies, companion attacks, transfers or later ongoing ticks; one area event uses each target's actual native packet after its save as usual. No new attack/damage event or added damage type. Check darkness at the attack/spell's actual damage resolution and at the Stealth check; a light-generating effect can remove eligibility before damage. Distinct percentage sources do not compound and the flatStealth bonus never grants a proficiency credential.",
  "submittedNewChoices": "Full-footprint total darkness, exact10% native direct damage arithmetic and legalStealth+2.",
  "submittedWorkedCases": [
    "A qualifying native19damage packet adds1 before defenses; later darkness-independent poison ticks do not inherit the feat bonus.",
    "Darkvision lets the Umbrin perceive a dark square but does not turn it bright. A square actually lit dimly no longer qualifies."
  ],
  "decision": "Keep actual Umbrin whole-footprint total darkness, not darkvision-as-light; calculate native10% before save/defenses and exclude ongoing/copy/companion damage.",
  "completeAuthoringProcedure": "Require actual Umbrin heritage. While your actual occupied space is in total darkness, gain+2 to actualDEXStealth checks and add floor(native damage/10) to each eligible personal direct attack/spell damage event. NEW your whole occupied footprint must be dark, not dim or partly illuminated; determine this independently from darkvision, which changes perception rather than illumination. It grants no ability to see targets, Hide automatically or ignore your actual Sunlight Sensitivity. Damage bonus uses the already proposed common pre-percentage base after native critical-dice adjustment and native ordinary ability modifier, before other feat/class riders, saving-throw reduction and defenses; allocate increment across native typed components by proportional largest remainder with stable ties. Count direct initial attacks/spell resolutions, not copies, companion attacks, transfers or later ongoing ticks; one genuine shared area roll receives its one native increment before each recipient's saving-throw reduction and defenses. No new attack/damage event or added damage type. Check darkness at the attack/spell's actual damage resolution and at the Stealth check; a light-generating effect can remove eligibility before damage. Distinct percentage sources do not compound and the flatStealth bonus never grants a proficiency credential.\nNEW damage-stage correction: calculate floor(10% of the eligible initial native personally owned attack/spell packet after native critical adjustment but before saving-throw reduction and defenses). Do not calculate it after the save, include external riders/percentages, or apply it to copied/companion results. Add distinct percentage feat riders without compounding under FS-04.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A qualifying native19damage packet adds1 before defenses; later darkness-independent poison ticks do not inherit the feat bonus.",
    "Darkvision lets the Umbrin perceive a dark square but does not turn it bright. A square actually lit dimly no longer qualifies."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Umbrin heritage. While your actual occupied space is in total darkness, gain+2 to actualDEXStealth checks and add floor(native damage/10) to each eligible personal direct attack/spell damage event. NEW your whole occupied footprint must be dark, not dim or partly illuminated; determine this independently from darkvision, which changes perception rather than illumination. It grants no ability to see targets, Hide automatically or ignore your actual Sunlight Sensitivity. Damage bonus uses the already proposed common pre-percentage base after native critical-dice adjustment and native ordinary ability modifier, before other feat/class riders, saving-throw reduction and defenses; allocate increment across native typed components by proportional largest remainder with stable ties. Count direct initial attacks/spell resolutions, not copies, companion attacks, transfers or later ongoing ticks; one genuine shared area roll receives its one native increment before each recipient's saving-throw reduction and defenses. No new attack/damage event or added damage type. Check darkness at the attack/spell's actual damage resolution and at the Stealth check; a light-generating effect can remove eligibility before damage. Distinct percentage sources do not compound and the flatStealth bonus never grants a proficiency credential.
NEW damage-stage correction: calculate floor(10% of the eligible initial native personally owned attack/spell packet after native critical adjustment but before saving-throw reduction and defenses). Do not calculate it after the save, include external riders/percentages, or apply it to copied/companion results. Add distinct percentage feat riders without compounding under FS-04.

### Original-position authored review references

```json
[
  {
    "id": "HM-17-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/32"
  },
  {
    "id": "HM-17-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/33"
  },
  {
    "id": "FA-06",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/additionalBoundaryReviews/0"
  },
  {
    "id": "FA-22",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/additionalBoundaryReviews/1"
  }
]
```

## HM-18 — Orcish Warpath

### Complete original object

```json
{
  "id": "orcish_warpath",
  "name": "Orcish Warpath",
  "description": "Racial feat tied to Orc heritage.",
  "prerequisite": "Orc heritage",
  "effect": "You gain +2 strength temporarily after defeating an enemy (stacks up to 3).",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind Orc heritage and personally defeating a meaningful enemy,not arbitrary party kills. Define temporary+2 Strength score versus modifier,maximum3 stacks,duration/refresh/reset and ordinary or explicit score cap. Recompute actual attacks,checks,carrying/prerequisites consistently without permanently learning gated choices or creating repeated kill buffs."
```

### Preserved original source direction (historical)

```json
{
  "featId": "orcish_warpath",
  "name": "Orcish Warpath",
  "cohort": "heritage_mutation",
  "questionId": "HM-18",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/17",
  "originalQuestion": "Bind Orc heritage and personally defeating a meaningful enemy,not arbitrary party kills. Define temporary+2 Strength score versus modifier,maximum3 stacks,duration/refresh/reset and ordinary or explicit score cap. Recompute actual attacks,checks,carrying/prerequisites consistently without permanently learning gated choices or creating repeated kill buffs.",
  "originalSourceObject": {
    "id": "orcish_warpath",
    "name": "Orcish Warpath",
    "description": "Racial feat tied to Orc heritage.",
    "prerequisite": "Orc heritage",
    "effect": "You gain +2 strength temporarily after defeating an enemy (stacks up to 3).",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "5c539be517d4b46a29fa44b513588114806b4a775adee2980dbd7a7777db249d",
  "submittedProcedure": "Require actual Orc heritage. NEW after your personal direct attack or personally resolved immediate spell/feature damage reduces a meaningful hostile from positiveHP to0, gain one temporary+2STR-score stack, maximum three. Death is not required; floors/replacements preventing the drop and staged/cooperative targets do not qualify. One actual target identity can yield at most one stack per encounter, and copied/periodic/companion damage yields none. Each stack lasts through the end of your next future regular turn; additional eligible distinct targets add independent stacks up to three, and at cap a new genuine trigger may refresh only the earliest-expiring stack. No rest/refill/initiative transition resets their deadlines. NEW apply up to+6STR without raising a score below20 past20; a separately legitimate underlying score above20 remains unchanged rather than reduced and gains no increase from this feat. Recompute the actual STR modifier for attacks, damage, saves, checks and carrying at each relevant moment; never add2 directly to the modifier. Derived maximumHP does not change from STR. Temporary increases cannot satisfy permanent acquisition/multiclass/feat prerequisites or create lasting learned choices. Expiry removes only its own layer and can cause ordinary encumbrance; it creates no damage or new movement.",
  "submittedNewChoices": "Three independent bounded+2score stacks, distinct meaningful targets, cap20 and no permanent-prerequisite exploit.",
  "submittedWorkedCases": [
    "STR15 with two live stacks becomes19, changing modifier+2 to+4; a third reaches20, not21.",
    "Dropping the same revived/cycled foe again cannot grant another stack that encounter. Expiry restores the underlying score."
  ],
  "decision": "Adopt finite3 temporary STR stacks with distinct real hostile drops, cap20 and original deadlines; temporary strength does not satisfy permanent acquisition or heal capacities.",
  "completeAuthoringProcedure": "Require actual Orc heritage. NEW after your personal direct attack or personally resolved immediate spell/feature damage reduces a meaningful hostile from positiveHP to0, gain one temporary+2STR-score stack, maximum three. Death is not required; floors/replacements preventing the drop and staged/cooperative targets do not qualify. One actual target identity can yield at most one stack per encounter, and copied/periodic/companion damage yields none. Each stack lasts through the end of your next future regular turn; additional eligible distinct targets add independent stacks up to three, and at cap a new genuine trigger may refresh only the earliest-expiring stack. No rest/refill/initiative transition resets their deadlines. NEW apply up to+6STR without raising a score below20 past20; a separately legitimate underlying score above20 remains unchanged rather than reduced and gains no increase from this feat. Recompute the actual STR modifier for attacks, damage, saves, checks and carrying at each relevant moment; never add2 directly to the modifier. Derived maximumHP does not change from STR. Temporary increases cannot satisfy permanent acquisition/multiclass/feat prerequisites or create lasting learned choices. Expiry removes only its own layer and can cause ordinary encumbrance; it creates no damage or new movement.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "STR15 with two live stacks becomes19, changing modifier+2 to+4; a third reaches20, not21.",
    "Dropping the same revived/cycled foe again cannot grant another stack that encounter. Expiry restores the underlying score."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Orc heritage. NEW after your personal direct attack or personally resolved immediate spell/feature damage reduces a meaningful hostile from positiveHP to0, gain one temporary+2STR-score stack, maximum three. Death is not required; floors/replacements preventing the drop and staged/cooperative targets do not qualify. One actual target identity can yield at most one stack per encounter, and copied/periodic/companion damage yields none. Each stack lasts through the end of your next future regular turn; additional eligible distinct targets add independent stacks up to three, and at cap a new genuine trigger may refresh only the earliest-expiring stack. No rest/refill/initiative transition resets their deadlines. NEW apply up to+6STR without raising a score below20 past20; a separately legitimate underlying score above20 remains unchanged rather than reduced and gains no increase from this feat. Recompute the actual STR modifier for attacks, damage, saves, checks and carrying at each relevant moment; never add2 directly to the modifier. Derived maximumHP does not change from STR. Temporary increases cannot satisfy permanent acquisition/multiclass/feat prerequisites or create lasting learned choices. Expiry removes only its own layer and can cause ordinary encumbrance; it creates no damage or new movement.

### Original-position authored review references

```json
[
  {
    "id": "HM-18-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/34"
  },
  {
    "id": "HM-18-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/35"
  }
]
```

## HM-19 — Primal Recovery

### Complete original object

```json
{
  "id": "primal_recovery",
  "name": "Primal Recovery",
  "description": "Racial feat tied to Troll heritage.",
  "prerequisite": "Troll heritage",
  "effect": "Once per combat, instantly recover from a debuff or status condition.",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind Troll heritage and once-per-real-combat use with declaration/action timing,zeroHP/incapacity restrictions and an explicit eligible condition/debuff scope. Distinguish cure,suppression,ongoing sources,physical restraints,Wounds/disease/curses/death and ability availability. Do not reduce any-status source promise silently; decide necessary exceptions with evidence."
```

### Preserved original source direction (historical)

```json
{
  "featId": "primal_recovery",
  "name": "Primal Recovery",
  "cohort": "heritage_mutation",
  "questionId": "HM-19",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/18",
  "originalQuestion": "Bind Troll heritage and once-per-real-combat use with declaration/action timing,zeroHP/incapacity restrictions and an explicit eligible condition/debuff scope. Distinguish cure,suppression,ongoing sources,physical restraints,Wounds/disease/curses/death and ability availability. Do not reduce any-status source promise silently; decide necessary exceptions with evidence.",
  "originalSourceObject": {
    "id": "primal_recovery",
    "name": "Primal Recovery",
    "description": "Racial feat tied to Troll heritage.",
    "prerequisite": "Troll heritage",
    "effect": "Once per combat, instantly recover from a debuff or status condition.",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "1ea3b2be4924d3cec0a5940afc7703a5fe4316128163384d86f5089f7ff042e5",
  "submittedProcedure": "Require actual Troll heritage. NEW once per real encounter, when one eligible adverse condition record would apply to you, or at the start of your own original regular turn, voluntarily end that one selected record immediately without Action/BA/Reaction. On-application choice occurs before its consequences and may avert its resulting incapacity. At your start you must still be alive and conscious; this specific non-action choice may be made while Incapacitated, Stunned or Paralyzed, but supplies no other actions. Select one ordinary source-applied Blinded, Deafened, Charmed, Frightened, Poisoned, Staggered, Stunned, Paralyzed, Silenced, Slowed, Root, Shaken, Disoriented, Weakened, Dazed, Bleeding, ongoing-fire or magical-sleep record with an ordinary removal endpoint. Pending Disoriented can be ended before transition. Explicit protected/artifact/special-cure-only records remain protected. This is a NEW finite interpretation of any debuff/status, not silent proof of the broad source promise. No cure of death, zeroHP Unconscious/dying state, Wounds/Injuries, disease/curses, exhaustion, serum/expedition Strain, class-resource costs, physical restraints/Grappled/Restrained, actual blindness from absent eyes, or environmental cause. Root qualifies only if magical/control, not physical ties. It ends one effect record, not its parent area/poison/disease, and may be reapplied by a later legal exposure. Removing Poisoned does not cancel a separate damage schedule. A current engulfingfire may create a new burn; the cure creates no lasting immunity. NoHP or regeneration pulse; acid/fire inhibition of Troll regeneration remains.",
  "submittedNewChoices": "One non-action voluntary condition cure, explicit incapacitation window, finite condition list and real-cause/protected-source exclusions.",
  "submittedWorkedCases": [
    "A conscious Troll may use the feat at its start to end oneStunned record, then acts only if no other restriction remains.",
    "It may remove ordinaryBleeding without healingHP, but cannot remove aWound or loosen the actual ropes causingRestrained."
  ],
  "decision": "Adopt one bounded Troll self-condition clearance and exact applicable timing, not wounds/debt/death or automatic removal of a continuing physical cause.",
  "completeAuthoringProcedure": "Require actual Troll heritage. NEW once per real encounter, when one eligible adverse condition record would apply to you, or at the start of your own original regular turn, voluntarily end that one selected record immediately without Action/BA/Reaction. On-application choice occurs before its consequences and may avert its resulting incapacity. At your start you must still be alive and conscious; this specific non-action choice may be made while Incapacitated, Stunned or Paralyzed, but supplies no other actions. Select one ordinary source-applied Blinded, Deafened, Charmed, Frightened, Poisoned, Staggered, Stunned, Paralyzed, Silenced, Slowed, Root, Shaken, Disoriented, Weakened, Dazed, Bleeding, ongoing-fire or magical-sleep record with an ordinary removal endpoint. Pending Disoriented can be ended before transition. Explicit protected/artifact/special-cure-only records remain protected. This is a NEW finite interpretation of any debuff/status, not silent proof of the broad source promise. No cure of death, zeroHP Unconscious/dying state, Wounds/Injuries, disease/curses, exhaustion, serum/expedition Strain, class-resource costs, physical restraints/Grappled/Restrained, actual blindness from absent eyes, or environmental cause. Root qualifies only if magical/control, not physical ties. It ends one effect record, not its parent area/poison/disease, and may be reapplied by a later legal exposure. Removing Poisoned does not cancel a separate damage schedule. A current engulfingfire may create a new burn; the cure creates no lasting immunity. NoHP or regeneration pulse; acid/fire inhibition of Troll regeneration remains.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A conscious Troll may use the feat at its start to end oneStunned record, then acts only if no other restriction remains.",
    "It may remove ordinaryBleeding without healingHP, but cannot remove aWound or loosen the actual ropes causingRestrained."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Troll heritage. NEW once per real encounter, when one eligible adverse condition record would apply to you, or at the start of your own original regular turn, voluntarily end that one selected record immediately without Action/BA/Reaction. On-application choice occurs before its consequences and may avert its resulting incapacity. At your start you must still be alive and conscious; this specific non-action choice may be made while Incapacitated, Stunned or Paralyzed, but supplies no other actions. Select one ordinary source-applied Blinded, Deafened, Charmed, Frightened, Poisoned, Staggered, Stunned, Paralyzed, Silenced, Slowed, Root, Shaken, Disoriented, Weakened, Dazed, Bleeding, ongoing-fire or magical-sleep record with an ordinary removal endpoint. Pending Disoriented can be ended before transition. Explicit protected/artifact/special-cure-only records remain protected. This is a NEW finite interpretation of any debuff/status, not silent proof of the broad source promise. No cure of death, zeroHP Unconscious/dying state, Wounds/Injuries, disease/curses, exhaustion, serum/expedition Strain, class-resource costs, physical restraints/Grappled/Restrained, actual blindness from absent eyes, or environmental cause. Root qualifies only if magical/control, not physical ties. It ends one effect record, not its parent area/poison/disease, and may be reapplied by a later legal exposure. Removing Poisoned does not cancel a separate damage schedule. A current engulfingfire may create a new burn; the cure creates no lasting immunity. NoHP or regeneration pulse; acid/fire inhibition of Troll regeneration remains.

### Original-position authored review references

```json
[
  {
    "id": "HM-19-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/36"
  },
  {
    "id": "HM-19-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/37"
  }
]
```

## HM-20 — Synaptic Rot

### Complete original object

```json
{
  "id": "synapticRot",
  "name": "Synaptic Rot",
  "description": "Mental attacks disrupt enemy spellcasting.",
  "prerequisite": "Wailing Eye or Viral Core mutation",
  "effect": "If an enemy fails a WIS or INT save near you, they cannot cast spells next round",
  "type": "Aberrant_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile nearby any enemy WIS/INT failure with Warrior8/15ft/your-feature/once-target-round counterpart and actual Silenced rules. Define verbal-only versus all-spell denial,save sources,active Wailing Eye Cluster/Viral Core Sacs binding and end-of-next-turn clock. Preserve nonspell abilities and source conflicts for explicit decision."
```

### Preserved original source direction (historical)

```json
{
  "featId": "synapticRot",
  "name": "Synaptic Rot",
  "cohort": "heritage_mutation",
  "questionId": "HM-20",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/19",
  "originalQuestion": "Reconcile nearby any enemy WIS/INT failure with Warrior8/15ft/your-feature/once-target-round counterpart and actual Silenced rules. Define verbal-only versus all-spell denial,save sources,active Wailing Eye Cluster/Viral Core Sacs binding and end-of-next-turn clock. Preserve nonspell abilities and source conflicts for explicit decision.",
  "originalSourceObject": {
    "id": "synapticRot",
    "name": "Synaptic Rot",
    "description": "Mental attacks disrupt enemy spellcasting.",
    "prerequisite": "Wailing Eye or Viral Core mutation",
    "effect": "If an enemy fails a WIS or INT save near you, they cannot cast spells next round",
    "type": "Aberrant_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "2a6e791ac5a73a6dfa659c5b931bbb9c89822880ef7947169362b97d21a221ae",
  "submittedProcedure": "NEW select the Warrior8 counterpart over nearby-any-save/all-spell-shutdown wording. Require Wailing Eye Cluster or Viral Core Sacs equipped and at least one of those exact mutations active. When an actual hostile within15ft and line of effect fails anINT orWIS save against your own direct Warrior feature, apply actualSilenced until the end of its next future regular turn, once per target per numbered round. The generating Warrior feature need not be the equipped prerequisite itself, but must be actually acquired/active/legal; an ally spell or unrelated ordinary spell does not qualify. Source names Wailing Eye and Viral Core bind only to the named actual cards. ActualSilenced prevents verbal components, command words, Chants and audible coordination; nonverbal spells and nonspell abilities remain possible if otherwise legal. No new universal spell ban or action loss. Same-profile reapplication may preserve later expiry without stacking, but the round ledger and source immunity apply. Gaining a nonverbal casting permission is not retroactively denied. No automatic target identification, sound-detection channel or ongoing15ft tether after application; later range loss does not erase the legal record.",
  "submittedNewChoices": "Exact active prerequisite,15ft actual ownWarriorINT/WISfailure and reviewed verbal-onlySilenced.",
  "submittedWorkedCases": [
    "A nearby hostile failsWIS against an acquired Warrior feature while Wailing Eye is active: its verbal spell is blocked through the deadline.",
    "A legally nonverbal spell remains usable; the original all-spells wording is preserved as the explicit alternative for review."
  ],
  "decision": "Unify Warrior8 active Eye Cluster/Viral Core and owner INT/WIS mutation-save failure; apply actual Silenced V restriction, not universal spell shutdown.",
  "completeAuthoringProcedure": "NEW select the Warrior8 counterpart over nearby-any-save/all-spell-shutdown wording. Require Wailing Eye Cluster or Viral Core Sacs equipped and at least one of those exact mutations active. When an actual hostile within15ft and line of effect fails anINT orWIS save against your own direct Warrior feature, apply actualSilenced until the end of its next future regular turn, once per target per numbered round. The generating Warrior feature need not be the equipped prerequisite itself, but must be actually acquired/active/legal; an ally spell or unrelated ordinary spell does not qualify. Source names Wailing Eye and Viral Core bind only to the named actual cards. ActualSilenced prevents verbal components, command words, Chants and audible coordination; nonverbal spells and nonspell abilities remain possible if otherwise legal. No new universal spell ban or action loss. Same-profile reapplication may preserve later expiry without stacking, but the round ledger and source immunity apply. Gaining a nonverbal casting permission is not retroactively denied. No automatic target identification, sound-detection channel or ongoing15ft tether after application; later range loss does not erase the legal record.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A nearby hostile failsWIS against an acquired Warrior feature while Wailing Eye is active: its verbal spell is blocked through the deadline.",
    "A legally nonverbal spell remains usable; the original all-spells wording is preserved as the explicit alternative for review."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW select the Warrior8 counterpart over nearby-any-save/all-spell-shutdown wording. Require Wailing Eye Cluster or Viral Core Sacs equipped and at least one of those exact mutations active. When an actual hostile within15ft and line of effect fails anINT orWIS save against your own direct Warrior feature, apply actualSilenced until the end of its next future regular turn, once per target per numbered round. The generating Warrior feature need not be the equipped prerequisite itself, but must be actually acquired/active/legal; an ally spell or unrelated ordinary spell does not qualify. Source names Wailing Eye and Viral Core bind only to the named actual cards. ActualSilenced prevents verbal components, command words, Chants and audible coordination; nonverbal spells and nonspell abilities remain possible if otherwise legal. No new universal spell ban or action loss. Same-profile reapplication may preserve later expiry without stacking, but the round ledger and source immunity apply. Gaining a nonverbal casting permission is not retroactively denied. No automatic target identification, sound-detection channel or ongoing15ft tether after application; later range loss does not erase the legal record.

### Original-position authored review references

```json
[
  {
    "id": "HM-20-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/38"
  },
  {
    "id": "HM-20-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/39"
  }
]
```

## HM-21 — Terror Engine

### Complete original object

```json
{
  "id": "terrorEngine",
  "name": "Terror Engine",
  "description": "Fear effects provide defensive benefits.",
  "prerequisite": "Carrion Signal Gland mutation",
  "effect": "If 2+ enemies are Shaken or Disoriented, gain +2 DR",
  "type": "Aberrant_mutation",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Reconcile source two Shaken/Disoriented enemies+2DR with Warrior8 counterpart adding Frightened,30ft,your-feature attribution and first damage each round. Define actual active Carrion prerequisite,counting distinct hostiles,damage-reduction order/packet,expiry and changed counts. No universal armor,all-hit reduction or stacking inferred."
```

### Preserved original source direction (historical)

```json
{
  "featId": "terrorEngine",
  "name": "Terror Engine",
  "cohort": "heritage_mutation",
  "questionId": "HM-21",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/20",
  "originalQuestion": "Reconcile source two Shaken/Disoriented enemies+2DR with Warrior8 counterpart adding Frightened,30ft,your-feature attribution and first damage each round. Define actual active Carrion prerequisite,counting distinct hostiles,damage-reduction order/packet,expiry and changed counts. No universal armor,all-hit reduction or stacking inferred.",
  "originalSourceObject": {
    "id": "terrorEngine",
    "name": "Terror Engine",
    "description": "Fear effects provide defensive benefits.",
    "prerequisite": "Carrion Signal Gland mutation",
    "effect": "If 2+ enemies are Shaken or Disoriented, gain +2 DR",
    "type": "Aberrant_mutation",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "63c059e65732be0c35a85f6464c487e82b1cc09ca6589862a41e125bc5acf259",
  "submittedProcedure": "NEW select Warrior8 and actual Carrion Signal Gland equipped/active. At each incoming direct damage event, count distinct meaningful hostiles within30ft and line of effect currently carrying an active unsuppressed Shaken, Frightened or activeDisoriented record caused by your own Warrior features. Two or more qualify; pendingDisoriented does not, and multiple records on one creature count as one creature. NEW the first positive resolved event in the numbered round while this predicate holds receives2whole-event damage reduction, minimum0, after passive typed defenses and before temporaryHP. Consume the feat's round entitlement when applied even if the reduction makes damage0; an event already at0 does not consume it. Stable component order allocates the2 once, not2 per type. No mitigation of HP sacrifice, direct death/state assignment or a transfer expressly forbidding recipient mitigation. The precise class wording addsFrightened and confines the original+2DR to one qualifying event; both differences remain explicit. Losing range, source eligibility or an active qualifying state removes readiness for later events but does not undo resolved damage. It grants no armor, universal resistance or new fear application.",
  "submittedNewChoices": "ActiveCarrion, real own-source distinct hostiles, pending-state exclusion and one2point whole-event reduction per round.",
  "submittedWorkedCases": [
    "One Shaken hostile and one activeDisoriented hostile in range qualify; a6damage event becomes4 beforetempHP.",
    "TwoShaken records on the same creature count as one hostile. A future scheduledDisoriented state counts as none until active."
  ],
  "decision": "Unify Warrior8 active Carrion Distortion and two distinct currently qualified hostile conditions; pending Disoriented is not active, and DR2 is once per round.",
  "completeAuthoringProcedure": "NEW select Warrior8 and actual Carrion Signal Gland equipped/active. At each incoming direct damage event, count distinct meaningful hostiles within30ft and line of effect currently carrying an active unsuppressed Shaken, Frightened or activeDisoriented record caused by your own Warrior features. Two or more qualify; pendingDisoriented does not, and multiple records on one creature count as one creature. NEW the first positive resolved event in the numbered round while this predicate holds receives2whole-event damage reduction, minimum0, after passive typed defenses and before temporaryHP. Consume the feat's round entitlement when applied even if the reduction makes damage0; an event already at0 does not consume it. Stable component order allocates the2 once, not2 per type. No mitigation of HP sacrifice, direct death/state assignment or a transfer expressly forbidding recipient mitigation. The precise class wording addsFrightened and confines the original+2DR to one qualifying event; both differences remain explicit. Losing range, source eligibility or an active qualifying state removes readiness for later events but does not undo resolved damage. It grants no armor, universal resistance or new fear application.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "One Shaken hostile and one activeDisoriented hostile in range qualify; a6damage event becomes4 beforetempHP.",
    "TwoShaken records on the same creature count as one hostile. A future scheduledDisoriented state counts as none until active."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW select Warrior8 and actual Carrion Signal Gland equipped/active. At each incoming direct damage event, count distinct meaningful hostiles within30ft and line of effect currently carrying an active unsuppressed Shaken, Frightened or activeDisoriented record caused by your own Warrior features. Two or more qualify; pendingDisoriented does not, and multiple records on one creature count as one creature. NEW the first positive resolved event in the numbered round while this predicate holds receives2whole-event damage reduction, minimum0, after passive typed defenses and before temporaryHP. Consume the feat's round entitlement when applied even if the reduction makes damage0; an event already at0 does not consume it. Stable component order allocates the2 once, not2 per type. No mitigation of HP sacrifice, direct death/state assignment or a transfer expressly forbidding recipient mitigation. The precise class wording addsFrightened and confines the original+2DR to one qualifying event; both differences remain explicit. Losing range, source eligibility or an active qualifying state removes readiness for later events but does not undo resolved damage. It grants no armor, universal resistance or new fear application.

### Original-position authored review references

```json
[
  {
    "id": "HM-21-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/40"
  },
  {
    "id": "HM-21-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/41"
  },
  {
    "id": "FA-24",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/additionalBoundaryReviews/3"
  }
]
```

## HM-22 — Versatile Mastery

### Complete original object

```json
{
  "id": "versatile_mastery",
  "name": "Versatile Mastery",
  "description": "Racial feat tied to Human heritage.",
  "prerequisite": "Human heritage",
  "effect": "Once per rest, use a class skill or ability from another party member.",
  "type": "Racial",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind Human heritage and once-per-rest clock. Define an explicit finite borrowing procedure for an actual party member class skill/ability,consent/availability,character/class-level gates,activation/RP/other resources,DC/scaling,duration and restrictions. No copied permanent progression,free resources/companions,signature identity or automatic full class access."
```

### Preserved original source direction (historical)

```json
{
  "featId": "versatile_mastery",
  "name": "Versatile Mastery",
  "cohort": "heritage_mutation",
  "questionId": "HM-22",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/heritage_mutation_feat_operating_proposal_internal.json",
  "sourceFileSha256": "cd7e83ebcf0cbbbcf71b9c60a6ca2bdb3204769d3afafd2d86a4b15e85bd5147",
  "sourcePointer": "/records/21",
  "originalQuestion": "Bind Human heritage and once-per-rest clock. Define an explicit finite borrowing procedure for an actual party member class skill/ability,consent/availability,character/class-level gates,activation/RP/other resources,DC/scaling,duration and restrictions. No copied permanent progression,free resources/companions,signature identity or automatic full class access.",
  "originalSourceObject": {
    "id": "versatile_mastery",
    "name": "Versatile Mastery",
    "description": "Racial feat tied to Human heritage.",
    "prerequisite": "Human heritage",
    "effect": "Once per rest, use a class skill or ability from another party member.",
    "type": "Racial",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "1cb3d01ddd00e51067e180c60eb2458693428230183dba3a183a2e4840913965",
  "submittedProcedure": "Require actual Human heritage. NEW once per completed beneficialSR orLR, borrow one permitted class skill for one check OR one class ability activation from a real willing current party member. Before use, spend one uninterrupted minute together within5ft communicating through an actual shared language/channel; choose the exact currently acquired donor skill/card and record donor consent. This preparation changes no resources and does not spend the use; one prepared choice at a time, ending at the next completedrest or replacement. Donor must have it through actual class training/acquisition, not a copied, borrowed or suppressed grant; you must meet actual body/equipment and the menu's total-level gate. You may then consume the feat use on your own legal check/activation while donor is conscious within30ft and can perceive/understand your signal; donor spends noAction, use or resource. A skill choice uses your own ability+normalPB for one real check, replacing lower proficiency, never donor ability, expertise or passive bonus; the task must actually use that donor's class-granted skill. An ability choice uses one of the twelve exact permitted cards/procedures below, your own stats/PB/materials and actual activation cost. These finite NEW borrowing limits deliberately narrow the source's otherwise unbounded class-ability promise for joint decision. No extra feat use after failure, no copied class levels/engines, passive/Arch/Hero/finale ability, transformation, companion, summon, item production, resource generation, permanent learning or further borrowing. The menu grants a one-use ability permission, never its independent class resource pool; actual1RP cost must be paid from your existing personal legalRPpool. Shared spell/Weave restrictions still apply where printed. An already-known same card shares its own recharge/use ledger, so borrowing cannot bypass a spent natural entitlement; an unknown menu card gets only this one borrowed activation and its future recharge history is retained. Existing ordinary resources and restrictions persist after the temporary permission ends. Lasting riders keep their original deadlines and source identity, with you as actor and donor provenance retained.",
  "submittedNewChoices": "Consent/minute preparation, one check or exact twelve-card activation, own actual costs, bounded statistics and no permanent/copy/resource engine.",
  "submittedWorkedCases": [
    "A willing Soldier teaches Tactical Reposition; the Human spends its ownBA and feat use to move half its ownSpeed along a legal route.",
    "Borrowing Nature's Whisper still costs1realRP. A Human with noRPpool cannot pay and must choose a different legal option before committing."
  ],
  "decision": "Adopt12 closed borrowed stunts with real minute teaching, conscious30ft donor window, own stats/cost and preserved shared identity; no borrowed full class engine or resources.",
  "completeAuthoringProcedure": "Require actual Human heritage. NEW once per completed beneficialSR orLR, borrow one permitted class skill for one check OR one class ability activation from a real willing current party member. Before use, spend one uninterrupted minute together within5ft communicating through an actual shared language/channel; choose the exact currently acquired donor skill/card and record donor consent. This preparation changes no resources and does not spend the use; one prepared choice at a time, ending at the next completedrest or replacement. Donor must have it through actual class training/acquisition, not a copied, borrowed or suppressed grant; you must meet actual body/equipment and the menu's total-level gate. You may then consume the feat use on your own legal check/activation while donor is conscious within30ft and can perceive/understand your signal; donor spends noAction, use or resource. A skill choice uses your own ability+normalPB for one real check, replacing lower proficiency, never donor ability, expertise or passive bonus; the task must actually use that donor's class-granted skill. An ability choice uses one of the twelve exact permitted cards/procedures below, your own stats/PB/materials and actual activation cost. These finite NEW borrowing limits deliberately narrow the source's otherwise unbounded class-ability promise for joint decision. No extra feat use after failure, no copied class levels/engines, passive/Arch/Hero/finale ability, transformation, companion, summon, item production, resource generation, permanent learning or further borrowing. The menu grants a one-use ability permission, never its independent class resource pool; actual1RP cost must be paid from your existing personal legalRPpool. Shared spell/Weave restrictions still apply where printed. An already-known same card shares its own recharge/use ledger, so borrowing cannot bypass a spent natural entitlement; an unknown menu card gets only this one borrowed activation and its future recharge history is retained. Existing ordinary resources and restrictions persist after the temporary permission ends. Lasting riders keep their original deadlines and source identity, with you as actor and donor provenance retained.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A willing Soldier teaches Tactical Reposition; the Human spends its ownBA and feat use to move half its ownSpeed along a legal route.",
    "Borrowing Nature's Whisper still costs1realRP. A Human with noRPpool cannot pay and must choose a different legal option before committing."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual Human heritage. NEW once per completed beneficialSR orLR, borrow one permitted class skill for one check OR one class ability activation from a real willing current party member. Before use, spend one uninterrupted minute together within5ft communicating through an actual shared language/channel; choose the exact currently acquired donor skill/card and record donor consent. This preparation changes no resources and does not spend the use; one prepared choice at a time, ending at the next completedrest or replacement. Donor must have it through actual class training/acquisition, not a copied, borrowed or suppressed grant; you must meet actual body/equipment and the menu's total-level gate. You may then consume the feat use on your own legal check/activation while donor is conscious within30ft and can perceive/understand your signal; donor spends noAction, use or resource. A skill choice uses your own ability+normalPB for one real check, replacing lower proficiency, never donor ability, expertise or passive bonus; the task must actually use that donor's class-granted skill. An ability choice uses one of the twelve exact permitted cards/procedures below, your own stats/PB/materials and actual activation cost. These finite NEW borrowing limits deliberately narrow the source's otherwise unbounded class-ability promise for joint decision. No extra feat use after failure, no copied class levels/engines, passive/Arch/Hero/finale ability, transformation, companion, summon, item production, resource generation, permanent learning or further borrowing. The menu grants a one-use ability permission, never its independent class resource pool; actual1RP cost must be paid from your existing personal legalRPpool. Shared spell/Weave restrictions still apply where printed. An already-known same card shares its own recharge/use ledger, so borrowing cannot bypass a spent natural entitlement; an unknown menu card gets only this one borrowed activation and its future recharge history is retained. Existing ordinary resources and restrictions persist after the temporary permission ends. Lasting riders keep their original deadlines and source identity, with you as actor and donor provenance retained.

### Original-position authored review references

```json
[
  {
    "id": "HM-22-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/42"
  },
  {
    "id": "HM-22-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json",
      "bytes": 895079,
      "sha256": "5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071"
    },
    "pointer": "/originalCaseReviews/43"
  }
]
```
