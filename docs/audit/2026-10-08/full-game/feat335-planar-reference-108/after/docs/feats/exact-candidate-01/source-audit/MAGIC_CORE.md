# Magic Core — source reconciliation

Derived complete-text assembly 106; exact parent review and integration pending.

Original source decisions below are historical receipts. The complete current candidate procedure and linked complete case review control this derived reading.

## MF-01 — Arcane Resonance

### Complete original object

```json
{
  "id": "arcaneResonance",
  "name": "Arcane Resonance",
  "description": "Your magical abilities resonate with ambient magical energy.",
  "prerequisite": "Spellcasting ability, Level 3",
  "effect": "Regain one ranked-spell recovery of 1st level or lower on a natural 20 attack roll",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Define ranked-spell recovery against the actual shared RP engine: recoverable amount, paid-cost ceiling, timing, natural20 attack eligibility, attack type, frequency and rest/event ledger. Preserve the level3 gate and avoid unlimited RP from harmless attacks, cantrips, extra attacks or repeated/copied results. No spell-slot system is inferred."
```

### Preserved original source direction (historical)

```json
{
  "featId": "arcaneResonance",
  "name": "Arcane Resonance",
  "cohort": "magic_core",
  "questionId": "MF-01",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/0",
  "originalQuestion": "Define ranked-spell recovery against the actual shared RP engine: recoverable amount, paid-cost ceiling, timing, natural20 attack eligibility, attack type, frequency and rest/event ledger. Preserve the level3 gate and avoid unlimited RP from harmless attacks, cantrips, extra attacks or repeated/copied results. No spell-slot system is inferred.",
  "originalSourceObject": {
    "id": "arcaneResonance",
    "name": "Arcane Resonance",
    "description": "Your magical abilities resonate with ambient magical energy.",
    "prerequisite": "Spellcasting ability, Level 3",
    "effect": "Regain one ranked-spell recovery of 1st level or lower on a natural 20 attack roll",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "75a28ee88baf2ed26838548e2e39c0ca5751d6fcedde907be95a6efa6fd0aed1",
  "submittedProcedure": "Keep spellcasting ability and total character level3. NEW finite recovery interpretation: once per beneficial Long Rest, after your own genuine attack resolves with a kept natural20, recover up to2RP into an existing actual pool, capped by missing RP and an eligible previously paid rank1 spell cost from this same rest epoch. Choose one committed rank1 cast receipt that actually spent RP before this attack and still has at least1unrecovered paid RP. Refund at most the lesser of2, its remaining paid amount and missing pool capacity; mark exactly that paid amount recovered so it cannot fund this feat again or a second refund of the same expense. A discounted1RP cast funds at most1; a free innate cast funds0. You may decline and keep the use; a declaration with no eligible paid receipt or no missing capacity is ineligible.\n\nThe qualifying attack may be a weapon or spell attack, including a genuine cantrip attack, but must be yours against a conscious, independently acting actual hostile opponent presenting a real encounter threat. NEW anti-farming exclusions: no object, self, willing training partner, compliant captive, your own controlled/summoned creature, copied/reflected roll or fabricated repeat of a natural20. A legitimate hostile opponent’s immunity does not erase its actual natural20 attack trigger; damage is not a printed requirement. An expanded critical on19, automatic hit, hypothetical die or replaced natural20 that was not kept does not qualify. Companions using your spell attack bonus are still different attackers. Resolve any triggering attack’s consequences first; recovery cannot retroactively pay an unaffordable cast or prevent that event’s death. No spell slot or “ranked recovery” pool is created.",
  "submittedNewChoices": "One LR use;2RP/actual unrecovered rank1-cost ceiling; legitimate personal natural20 trigger and finite expense ledger.",
  "submittedWorkedCases": [
    "You paid1RP for a legal discounted rank1cast and later roll a kept natural20 against an active hostile foe. With3RP missing, this feat can restore only1RP and spends its use, not2.",
    "After using the feat, additional natural20cantrip attacks recover nothing until the next beneficial Long Rest. Attacking your own familiar cannot trigger it even while the use is available."
  ],
  "decision": "Retain the MF-01 complete grant/procedure and boundaries. One LR use;2RP/actual unrecovered rank1-cost ceiling; legitimate personal natural20 trigger and finite expense ledger. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Keep spellcasting ability and total character level3. NEW finite recovery interpretation: once per beneficial Long Rest, after your own genuine attack resolves with a kept natural20, recover up to2RP into an existing actual pool, capped by missing RP and an eligible previously paid rank1 spell cost from this same rest epoch. Choose one committed rank1 cast receipt that actually spent RP before this attack and still has at least1unrecovered paid RP. Refund at most the lesser of2, its remaining paid amount and missing pool capacity; mark exactly that paid amount recovered so it cannot fund this feat again or a second refund of the same expense. A discounted1RP cast funds at most1; a free innate cast funds0. You may decline and keep the use; a declaration with no eligible paid receipt or no missing capacity is ineligible.\n\nThe qualifying attack may be a weapon or spell attack, including a genuine cantrip attack, but must be yours against a conscious, independently acting actual hostile opponent presenting a real encounter threat. NEW anti-farming exclusions: no object, self, willing training partner, compliant captive, your own controlled/summoned creature, copied/reflected roll or fabricated repeat of a natural20. A legitimate hostile opponent’s immunity does not erase its actual natural20 attack trigger; damage is not a printed requirement. An expanded critical on19, automatic hit, hypothetical die or replaced natural20 that was not kept does not qualify. Companions using your spell attack bonus are still different attackers. Resolve any triggering attack’s consequences first; recovery cannot retroactively pay an unaffordable cast or prevent that event’s death. No spell slot or “ranked recovery” pool is created.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "You paid1RP for a legal discounted rank1cast and later roll a kept natural20 against an active hostile foe. With3RP missing, this feat can restore only1RP and spends its use, not2.",
    "After using the feat, additional natural20cantrip attacks recover nothing until the next beneficial Long Rest. Attacking your own familiar cannot trigger it even while the use is available."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Keep spellcasting ability and total character level3. NEW finite recovery interpretation: once per beneficial Long Rest, after your own genuine attack resolves with a kept natural20, recover up to2RP into an existing actual pool, capped by missing RP and an eligible previously paid rank1 spell cost from this same rest epoch. Choose one committed rank1 cast receipt that actually spent RP before this attack and still has at least1unrecovered paid RP. Refund at most the lesser of2, its remaining paid amount and missing pool capacity; mark exactly that paid amount recovered so it cannot fund this feat again or a second refund of the same expense. A discounted1RP cast funds at most1; a free innate cast funds0. You may decline and keep the use; a declaration with no eligible paid receipt or no missing capacity is ineligible.

The qualifying attack may be a weapon or spell attack, including a genuine cantrip attack, but must be yours against a conscious, independently acting actual hostile opponent presenting a real encounter threat. NEW anti-farming exclusions: no object, self, willing training partner, compliant captive, your own controlled/summoned creature, copied/reflected roll or fabricated repeat of a natural20. A legitimate hostile opponent’s immunity does not erase its actual natural20 attack trigger; damage is not a printed requirement. An expanded critical on19, automatic hit, hypothetical die or replaced natural20 that was not kept does not qualify. Companions using your spell attack bonus are still different attackers. Resolve any triggering attack’s consequences first; recovery cannot retroactively pay an unaffordable cast or prevent that event’s death. No spell slot or “ranked recovery” pool is created.

### Original-position authored review references

```json
[
  {
    "id": "MF-01-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/0"
  },
  {
    "id": "MF-01-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/1"
  }
]
```

## MF-02 — Astral Projection

### Complete original object

```json
{
  "id": "astral_projection",
  "name": "Astral Projection",
  "description": "You can project your consciousness to other planes.",
  "prerequisite": "Wisdom 17+, level 15+",
  "effect": "Once per long rest, you can cast astral projection without expending a ranked-spell recovery.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Resolve Wisdom17 and character-level15 versus the ordinary rank9/class-level17 route; define only the feat grant, casting ability/DC, charge and Long Rest recovery, components and interruption/payment. The named ordinary spell remains blocked. Do not develop planes, destinations, souls, projection ontology or deferred cosmology to complete this feat; retain that dependency explicitly."
```

### Preserved original source direction (historical)

```json
{
  "featId": "astral_projection",
  "name": "Astral Projection",
  "cohort": "magic_core",
  "questionId": "MF-02",
  "disposition": "DEFER_PAYLOAD_KEEP_FINITE_GRANT_WRAPPER",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/1",
  "originalQuestion": "Resolve Wisdom17 and character-level15 versus the ordinary rank9/class-level17 route; define only the feat grant, casting ability/DC, charge and Long Rest recovery, components and interruption/payment. The named ordinary spell remains blocked. Do not develop planes, destinations, souls, projection ontology or deferred cosmology to complete this feat; retain that dependency explicitly.",
  "originalSourceObject": {
    "id": "astral_projection",
    "name": "Astral Projection",
    "description": "You can project your consciousness to other planes.",
    "prerequisite": "Wisdom 17+, level 15+",
    "effect": "Once per long rest, you can cast astral projection without expending a ranked-spell recovery.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "f68fb87e05a8b70c06d10173a02ae26c0d416b244c997220ac88d286c3ba2d91",
  "submittedProcedure": "Retain WIS17 and total character level15. NEW mechanical grant interface only: acquire one feat-scoped Astral Projection entitlement at its named rank9, using WIS, with one charge per beneficial Long Rest and no ordinary class-level17 prerequisite for this specific grant. It grants no ordinary rank9 repertoire or class advancement. Once the named spell has its own complete approved payload, apply that payload’s exact action, components, target eligibility, costs other than normal rank price, concentration, interruption and ending, using the shared feat casting route. The rank9 feat cast would build base2Dissonance plus actual Refrain and is blocked at its actual Limit+6. Reserve the charge at legal cast start; an interrupted legal cast does not refund it. Before the deferred payload is authored and reviewed there is no legal activation, no charge payment and no invented destination, projection body, soul rule or plane access. This grant record is not full-feat readiness and remains a post-push dependency.",
  "submittedNewChoices": "WIS/rank9/level15 isolated grant wrapper and one-LR charge; payload deliberately remains deferred.",
  "submittedWorkedCases": [
    "A level15character meeting WIS17 can record this proposed entitlement without becoming an ordinary level17Wizard or learning other rank9spells. Its unreviewed projection payload still cannot be activated.",
    "A prospective rank9casting ledger would add base2Dissonance rather than the rank1value. No charge is spent attempting an undefined destination while the whole payload remains deferred."
  ],
  "decision": "Retain the MF-02 complete grant/procedure and boundaries. WIS/rank9/level15 isolated grant wrapper and one-LR charge; payload deliberately remains deferred. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Retain WIS17 and total character level15. NEW mechanical grant interface only: acquire one feat-scoped Astral Projection entitlement at its named rank9, using WIS, with one charge per beneficial Long Rest and no ordinary class-level17 prerequisite for this specific grant. It grants no ordinary rank9 repertoire or class advancement. Once the named spell has its own complete approved payload, apply that payload’s exact action, components, target eligibility, costs other than normal rank price, concentration, interruption and ending, using the shared feat casting route. The rank9 feat cast would build base2Dissonance plus actual Refrain and is blocked at its actual Limit+6. Reserve the charge at legal cast start; an interrupted legal cast does not refund it. Before the deferred payload is authored and reviewed there is no legal activation, no charge payment and no invented destination, projection body, soul rule or plane access. This grant record is not full-feat readiness and remains a post-push dependency.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A level15character meeting WIS17 can record this proposed entitlement without becoming an ordinary level17Wizard or learning other rank9spells. Its unreviewed projection payload still cannot be activated.",
    "A prospective rank9casting ledger would add base2Dissonance rather than the rank1value. No charge is spent attempting an undefined destination while the whole payload remains deferred."
  ],
  "payloadOperational": null,
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Retain WIS17 and total character level15. NEW mechanical grant interface only: acquire one feat-scoped Astral Projection entitlement at its named rank9, using WIS, with one charge per beneficial Long Rest and no ordinary class-level17 prerequisite for this specific grant. It grants no ordinary rank9 repertoire or class advancement. Once the named spell has its own complete approved payload, apply that payload’s exact action, components, target eligibility, costs other than normal rank price, concentration, interruption and ending, using the shared feat casting route. The rank9 feat cast would build base2Dissonance plus actual Refrain and is blocked at its actual Limit+6. Reserve the charge at legal cast start; an interrupted legal cast does not refund it. Before the deferred payload is authored and reviewed there is no legal activation, no charge payment and no invented destination, projection body, soul rule or plane access. This grant record is not full-feat readiness and remains a post-push dependency.

### Original-position authored review references

```json
[
  {
    "id": "MF-02-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/2"
  },
  {
    "id": "MF-02-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/3"
  },
  {
    "id": "FA-28",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/additionalBoundaryReviews/1"
  }
]
```

## MF-03 — Battle Mage

### Complete original object

```json
{
  "id": "battleMage",
  "name": "Battle Mage",
  "description": "You blend magic and martial combat.",
  "prerequisite": "Spellcasting ability, proficiency with martial weapons",
  "effect": "You can cast spells with somatic components while holding weapons and shields.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind spellcasting and martial-weapon prerequisites to actual grants, then specify somatic hand permissions while holding weapons/shields. Keep verbal components, priced/consumed materials, focus eligibility, nonproficient-armor costs and genuine hand availability separate. Do not import unprinted War Caster reaction-spell benefits."
```

### Preserved original source direction (historical)

```json
{
  "featId": "battleMage",
  "name": "Battle Mage",
  "cohort": "magic_core",
  "questionId": "MF-03",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/2",
  "originalQuestion": "Bind spellcasting and martial-weapon prerequisites to actual grants, then specify somatic hand permissions while holding weapons/shields. Keep verbal components, priced/consumed materials, focus eligibility, nonproficient-armor costs and genuine hand availability separate. Do not import unprinted War Caster reaction-spell benefits.",
  "originalSourceObject": {
    "id": "battleMage",
    "name": "Battle Mage",
    "description": "You blend magic and martial combat.",
    "prerequisite": "Spellcasting ability, proficiency with martial weapons",
    "effect": "You can cast spells with somatic components while holding weapons and shields.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "cdec3be435a94fa7f8ca8840d963bb6e6e893e9c88c422f3da7ca94d07cb37f3",
  "submittedProcedure": "Require actual personal spellcasting and a genuine martial-weapon proficiency grant; NEW one specified martial weapon proficiency is sufficient, without inventing proficiency with all martial weapons. For a spell you personally cast, one hand otherwise legally holding a weapon or shield may perform that spell’s S gestures while retaining that object. The hand and limb must still be capable of the required motion; restraints, missing anatomy or a feature explicitly forbidding gestures are not bypassed. NEW a buckler-occupied hand can use this same narrow S exception despite its ordinary lack of a free S hand. This gives no extra hands for loading, material manipulation, grappling, tools or wielding. A two-handed weapon can be held through the gestures, but its actual attack still requires its normal grip. F must independently be supplied by a legal focus; holding a sword does not make it a focus. V, priced/consumed materials, actual source access and nonproficient armor casting/concentration consequences remain. No advantage on concentration or Reaction spell is granted by this feat.",
  "submittedNewChoices": "One actual martial proficiency suffices; narrow occupied-weapon/shield/buckler S exception only.",
  "submittedWorkedCases": [
    "A caster with an actual martial sword proficiency holds sword and shield and can supply S through one hand under this feat. A spell also requiring F still needs an independently legal focus arrangement.",
    "Binding both hands so gestures cannot be made still prevents S. The feat does not remove a nonproficient armor RP surcharge or concentration disadvantage."
  ],
  "decision": "Retain the MF-03 complete grant/procedure and boundaries. One actual martial proficiency suffices; narrow occupied-weapon/shield/buckler S exception only. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require actual personal spellcasting and a genuine martial-weapon proficiency grant; NEW one specified martial weapon proficiency is sufficient, without inventing proficiency with all martial weapons. For a spell you personally cast, one hand otherwise legally holding a weapon or shield may perform that spell’s S gestures while retaining that object. The hand and limb must still be capable of the required motion; restraints, missing anatomy or a feature explicitly forbidding gestures are not bypassed. NEW a buckler-occupied hand can use this same narrow S exception despite its ordinary lack of a free S hand. This gives no extra hands for loading, material manipulation, grappling, tools or wielding. A two-handed weapon can be held through the gestures, but its actual attack still requires its normal grip. F must independently be supplied by a legal focus; holding a sword does not make it a focus. V, priced/consumed materials, actual source access and nonproficient armor casting/concentration consequences remain. No advantage on concentration or Reaction spell is granted by this feat.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A caster with an actual martial sword proficiency holds sword and shield and can supply S through one hand under this feat. A spell also requiring F still needs an independently legal focus arrangement.",
    "Binding both hands so gestures cannot be made still prevents S. The feat does not remove a nonproficient armor RP surcharge or concentration disadvantage."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual personal spellcasting and a genuine martial-weapon proficiency grant; NEW one specified martial weapon proficiency is sufficient, without inventing proficiency with all martial weapons. For a spell you personally cast, one hand otherwise legally holding a weapon or shield may perform that spell’s S gestures while retaining that object. The hand and limb must still be capable of the required motion; restraints, missing anatomy or a feature explicitly forbidding gestures are not bypassed. NEW a buckler-occupied hand can use this same narrow S exception despite its ordinary lack of a free S hand. This gives no extra hands for loading, material manipulation, grappling, tools or wielding. A two-handed weapon can be held through the gestures, but its actual attack still requires its normal grip. F must independently be supplied by a legal focus; holding a sword does not make it a focus. V, priced/consumed materials, actual source access and nonproficient armor casting/concentration consequences remain. No advantage on concentration or Reaction spell is granted by this feat.

### Original-position authored review references

```json
[
  {
    "id": "MF-03-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/4"
  },
  {
    "id": "MF-03-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/5"
  }
]
```

## MF-04 — Cantrip Mastery

### Complete original object

```json
{
  "id": "cantrip_mastery",
  "name": "Cantrip Mastery",
  "description": "Your cantrips become more powerful.",
  "prerequisite": "Ability to cast cantrips",
  "effect": "Choose one cantrip you know. It deals maximum damage when you roll a natural 20 on the attack roll or the target rolls a natural 1 on their saving throw.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Define the single permanent cantrip choice, replacement rules, natural20 attack versus target-natural1 save, critical dice before maximization, multiple targets/packets, delayed/repeated damage and added rider dice. Ordinary saves have no generic natural1 failure: resolve this feat trigger separately from success and damage entitlement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "cantrip_mastery",
  "name": "Cantrip Mastery",
  "cohort": "magic_core",
  "questionId": "MF-04",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/3",
  "originalQuestion": "Define the single permanent cantrip choice, replacement rules, natural20 attack versus target-natural1 save, critical dice before maximization, multiple targets/packets, delayed/repeated damage and added rider dice. Ordinary saves have no generic natural1 failure: resolve this feat trigger separately from success and damage entitlement.",
  "originalSourceObject": {
    "id": "cantrip_mastery",
    "name": "Cantrip Mastery",
    "description": "Your cantrips become more powerful.",
    "prerequisite": "Ability to cast cantrips",
    "effect": "Choose one cantrip you know. It deals maximum damage when you roll a natural 20 on the attack roll or the target rolls a natural 1 on their saving throw.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "c4d4905142fc0bd3baafd89e60a9c194d257edfec5434f529e45c602384b89a7",
  "submittedProcedure": "Choose one exact known cantrip identity and its rank0casting modes permanently; the feat grants neither that spell nor a free replacement. When your actual attack for that chosen rank0spell keeps a natural20, maximize that attack’s eligible direct spell damage dice after its normal critical dice doubling. When an actual target’s saving throw against a particular damage event of that cantrip keeps a natural1, maximize that target’s eligible damage dice for that event. NEW a saved natural1 remains a successful save if its actual total meets DC: this trigger does not turn success into failure or create damage where the card gives none; if success gives half damage, halve the maximized lawful amount normally.\n\nMaximize the chosen spell’s own dice plus dice explicitly added to that spell’s damage roll, not independent weapon, class/feat or item damage riders. Keep flat bonuses unchanged. Resolve each actual attack/save event separately; a natural20on one ray does not maximize a different ray, all area targets or later ongoing damage. A target-specific natural1on a shared area save uses the maximum native-dice value for that target only; other targets retain the ordinary shared rolled value. A later genuine damage-triggering save can qualify independently, but an earlier failed save supplies no permanent maximum-damage state. A no-roll automatic hit/failure or critical-range19is not a natural20/1. NEW a would-be damage die replaced with its maximum is not actually rolled for Evocation Focus; do not roll meaningless dice merely to obtain that other feat’s bonus. No ordinary cantrip scaling is added.",
  "submittedNewChoices": "Per-event/target maximization; critical dice first; native versus independent rider boundary; successful natural1does not change save outcome.",
  "submittedWorkedCases": [
    "A chosen cantrip attack normally deals1d6+3. Its genuine natural20critical maximizes2d6to12and retains+3, for15before defenses; an independent1d4poison rider is rolled normally.",
    "A target’s natural1plus14meetsDC15. If the cantrip gives no damage on success it takes0despite the natural1; if the exact card gives half, apply half to its lawful maximized native damage instead."
  ],
  "decision": "Retain the MF-04 complete grant/procedure and boundaries. Per-event/target maximization; critical dice first; native versus independent rider boundary; successful natural1does not change save outcome. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose one exact known cantrip identity and its rank0casting modes permanently; the feat grants neither that spell nor a free replacement. When your actual attack for that chosen rank0spell keeps a natural20, maximize that attack’s eligible direct spell damage dice after its normal critical dice doubling. When an actual target’s saving throw against a particular damage event of that cantrip keeps a natural1, maximize that target’s eligible damage dice for that event. NEW a saved natural1 remains a successful save if its actual total meets DC: this trigger does not turn success into failure or create damage where the card gives none; if success gives half damage, halve the maximized lawful amount normally.\n\nMaximize the chosen spell’s own dice plus dice explicitly added to that spell’s damage roll, not independent weapon, class/feat or item damage riders. Keep flat bonuses unchanged. Resolve each actual attack/save event separately; a natural20on one ray does not maximize a different ray, all area targets or later ongoing damage. A target-specific natural1on a shared area save uses the maximum native-dice value for that target only; other targets retain the ordinary shared rolled value. A later genuine damage-triggering save can qualify independently, but an earlier failed save supplies no permanent maximum-damage state. A no-roll automatic hit/failure or critical-range19is not a natural20/1. NEW a would-be damage die replaced with its maximum is not actually rolled for Evocation Focus; do not roll meaningless dice merely to obtain that other feat’s bonus. No ordinary cantrip scaling is added.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A chosen cantrip attack normally deals1d6+3. Its genuine natural20critical maximizes2d6to12and retains+3, for15before defenses; an independent1d4poison rider is rolled normally.",
    "A target’s natural1plus14meetsDC15. If the cantrip gives no damage on success it takes0despite the natural1; if the exact card gives half, apply half to its lawful maximized native damage instead."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose one exact known cantrip identity and its rank0casting modes permanently; the feat grants neither that spell nor a free replacement. When your actual attack for that chosen rank0spell keeps a natural20, maximize that attack’s eligible direct spell damage dice after its normal critical dice doubling. When an actual target’s saving throw against a particular damage event of that cantrip keeps a natural1, maximize that target’s eligible damage dice for that event. NEW a saved natural1 remains a successful save if its actual total meets DC: this trigger does not turn success into failure or create damage where the card gives none; if success gives half damage, halve the maximized lawful amount normally.

Maximize the chosen spell’s own dice plus dice explicitly added to that spell’s damage roll, not independent weapon, class/feat or item damage riders. Keep flat bonuses unchanged. Resolve each actual attack/save event separately; a natural20on one ray does not maximize a different ray, all area targets or later ongoing damage. A target-specific natural1on a shared area save uses the maximum native-dice value for that target only; other targets retain the ordinary shared rolled value. A later genuine damage-triggering save can qualify independently, but an earlier failed save supplies no permanent maximum-damage state. A no-roll automatic hit/failure or critical-range19is not a natural20/1. NEW a would-be damage die replaced with its maximum is not actually rolled for Evocation Focus; do not roll meaningless dice merely to obtain that other feat’s bonus. No ordinary cantrip scaling is added.

### Original-position authored review references

```json
[
  {
    "id": "MF-04-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/6"
  },
  {
    "id": "MF-04-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/7"
  }
]
```

## MF-05 — Dispel Mastery

### Complete original object

```json
{
  "id": "dispel_mastery",
  "name": "Dispel Mastery",
  "description": "You excel at dispelling magic.",
  "prerequisite": "Ability to cast dispel magic",
  "effect": "When you cast dispel magic, you can target one additional magical effect.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Use the actual Dispel Magic operational card; define selecting one additional effect, same/different carrier, range/visibility, each effect eligibility and separate checks, rank thresholds and interruption. The feat does not automatically dispel a second item, creature, spell or innate magic merely by calling it an effect."
```

### Preserved original source direction (historical)

```json
{
  "featId": "dispel_mastery",
  "name": "Dispel Mastery",
  "cohort": "magic_core",
  "questionId": "MF-05",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/4",
  "originalQuestion": "Use the actual Dispel Magic operational card; define selecting one additional effect, same/different carrier, range/visibility, each effect eligibility and separate checks, rank thresholds and interruption. The feat does not automatically dispel a second item, creature, spell or innate magic merely by calling it an effect.",
  "originalSourceObject": {
    "id": "dispel_mastery",
    "name": "Dispel Mastery",
    "description": "You excel at dispelling magic.",
    "prerequisite": "Ability to cast dispel magic",
    "effect": "When you cast dispel magic, you can target one additional magical effect.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "100150f51865e1499f561eec6e7bea1efa78b4f07b30b176bd764c9f1fb1960f",
  "submittedProcedure": "Require actual access to the exact ordinary Dispel Magic spell. When you legally cast it, you may choose one additional distinct individually perceptible ongoing magical effect within its actual60-foot range and line of effect. NEW the two effects may have the same carrier or different carriers; each must independently satisfy the full reviewed Dispel Magic card. Both must be generated by actual recorded spell rank0–3, selectable as individual effects and not protected against this dispel. The existing card resolves eligible effects automatically, with no check or save; do not import a higher-rank check from another game. Declare both targets before committing costs. One cast, one RP payment, one Dissonance/Refrain update and one interruption window covers both. Resolve their ordinary ending procedures in a declared stable order, rechecking actual existence/eligibility for the second; if ending the first genuinely ends the second already, there is no new replacement target or second reward. Negating the cast ends neither effect and refunds nothing. This feat does not add an item purge, innate-trait removal, a rank4target, unknown-rank inference or extra target to a differently named dispel spell/class technique.",
  "submittedNewChoices": "Same/different carrier option and stable ending order; preserves actual automatic rank0–3card with no invented check.",
  "submittedWorkedCases": [
    "Two individually perceived rank2effects on different creatures within60feet can both end from one legal Dispel Magic cast. The feat does not require or authorize two additional casting rolls.",
    "One eligible rank3ward and one rank4ward are present. Only the rank3effect qualifies; the feat does not legalize the rank4one by spending moreRP or treating it as the extra target."
  ],
  "decision": "Retain the MF-05 complete grant/procedure and boundaries. Same/different carrier option and stable ending order; preserves actual automatic rank0–3card with no invented check. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require actual access to the exact ordinary Dispel Magic spell. When you legally cast it, you may choose one additional distinct individually perceptible ongoing magical effect within its actual60-foot range and line of effect. NEW the two effects may have the same carrier or different carriers; each must independently satisfy the full reviewed Dispel Magic card. Both must be generated by actual recorded spell rank0–3, selectable as individual effects and not protected against this dispel. The existing card resolves eligible effects automatically, with no check or save; do not import a higher-rank check from another game. Declare both targets before committing costs. One cast, one RP payment, one Dissonance/Refrain update and one interruption window covers both. Resolve their ordinary ending procedures in a declared stable order, rechecking actual existence/eligibility for the second; if ending the first genuinely ends the second already, there is no new replacement target or second reward. Negating the cast ends neither effect and refunds nothing. This feat does not add an item purge, innate-trait removal, a rank4target, unknown-rank inference or extra target to a differently named dispel spell/class technique.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Two individually perceived rank2effects on different creatures within60feet can both end from one legal Dispel Magic cast. The feat does not require or authorize two additional casting rolls.",
    "One eligible rank3ward and one rank4ward are present. Only the rank3effect qualifies; the feat does not legalize the rank4one by spending moreRP or treating it as the extra target."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual access to the exact ordinary Dispel Magic spell. When you legally cast it, you may choose one additional distinct individually perceptible ongoing magical effect within its actual60-foot range and line of effect. NEW the two effects may have the same carrier or different carriers; each must independently satisfy the full reviewed Dispel Magic card. Both must be generated by actual recorded spell rank0–3, selectable as individual effects and not protected against this dispel. The existing card resolves eligible effects automatically, with no check or save; do not import a higher-rank check from another game. Declare both targets before committing costs. One cast, one RP payment, one Dissonance/Refrain update and one interruption window covers both. Resolve their ordinary ending procedures in a declared stable order, rechecking actual existence/eligibility for the second; if ending the first genuinely ends the second already, there is no new replacement target or second reward. Negating the cast ends neither effect and refunds nothing. This feat does not add an item purge, innate-trait removal, a rank4target, unknown-rank inference or extra target to a differently named dispel spell/class technique.

### Original-position authored review references

```json
[
  {
    "id": "MF-05-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/8"
  },
  {
    "id": "MF-05-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/9"
  }
]
```

## MF-06 — Divine Favor

### Complete original object

```json
{
  "id": "divine_favor",
  "name": "Divine Favor",
  "description": "You have earned the favor of a deity.",
  "prerequisite": "Charisma 15+, worship a deity",
  "effect": "Once per long rest, you can call upon divine aid to automatically succeed on one saving throw or ability check.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Resolve Charisma15 and existing worship credential without inventing a deity or doctrine. Define eligible save/ability check, declaration window, opposed ties, degrees and critical outcomes, information available, action/cadence and Long Rest ledger. Automatic success grants no new roll, physical possibility or permission to alter cosmology."
```

### Preserved original source direction (historical)

```json
{
  "featId": "divine_favor",
  "name": "Divine Favor",
  "cohort": "magic_core",
  "questionId": "MF-06",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/5",
  "originalQuestion": "Resolve Charisma15 and existing worship credential without inventing a deity or doctrine. Define eligible save/ability check, declaration window, opposed ties, degrees and critical outcomes, information available, action/cadence and Long Rest ledger. Automatic success grants no new roll, physical possibility or permission to alter cosmology.",
  "originalSourceObject": {
    "id": "divine_favor",
    "name": "Divine Favor",
    "description": "You have earned the favor of a deity.",
    "prerequisite": "Charisma 15+, worship a deity",
    "effect": "Once per long rest, you can call upon divine aid to automatically succeed on one saving throw or ability check.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "132665fc74aa664e696fc3abdaef70eed70f3fad84759930c8664878cdf0a6ba",
  "submittedProcedure": "Retain CHA15 and an actual already established worship-of-a-deity credential without selecting a new deity or interpreting doctrine here. NEW once per beneficial Long Rest, after your own actual saving throw or ability check is called for, or after its result is known but before its consequences commit, declare this feat to replace that one outcome with ordinary Success. No Action, component or new roll is required; it can protect a living incapacitated creature making an actual save, including a death save. It cannot act after death or reverse committed harm. Fixed-DC task outcome becomes Success, not Critical Success; saves become successful without a natural face or a success-by-margin value. A death save gains one ordinary success, not natural20healing. For a genuinely authorized crafting completion check, this means Standard success in that craft procedure, retaining all work/material/access requirements and any independently reviewed quality adjustment.\n\nFor your side of an actual opposed ability check, NEW it wins against an ordinary rolled opponent regardless of total. If both sides commit an explicit automatic-success effect to the same opposition, resolve their incompatible claims by preserving the existing state, as with the Core initiating-tie rule; no retroactive transfer of an already resolved result. This declared conflict rule needs joint review. The feat does not create an ability check when none is allowed, overcome physical impossibility, convert an attack into a check, grant NPC consent outside a legitimately established social success outcome, or grant knowledge unavailable to the legal task. Only one check/save is affected; another save from the same damage event remains separate. Other outcome-triggered rules see ordinary Success, no natural20/1 and no invented numerical margin.",
  "submittedNewChoices": "After-result/preconsequence window; ordinary success/death-save/craft interpretation; explicit dual-auto-success opposition boundary.",
  "submittedWorkedCases": [
    "A living dying character is about to record its third death-save failure. Spending this feat before that failure commits replaces it with one success; it does not restore1HP or erase earlier counters.",
    "A qualified craft completion would fail after all its real work. The feat gives Standard success, not automatic Masterwork or free ingredients. An impossible request with no authorized check cannot be made possible by spending it."
  ],
  "decision": "Retain the MF-06 complete grant/procedure and boundaries. After-result/preconsequence window; ordinary success/death-save/craft interpretation; explicit dual-auto-success opposition boundary. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Retain CHA15 and an actual already established worship-of-a-deity credential without selecting a new deity or interpreting doctrine here. NEW once per beneficial Long Rest, after your own actual saving throw or ability check is called for, or after its result is known but before its consequences commit, declare this feat to replace that one outcome with ordinary Success. No Action, component or new roll is required; it can protect a living incapacitated creature making an actual save, including a death save. It cannot act after death or reverse committed harm. Fixed-DC task outcome becomes Success, not Critical Success; saves become successful without a natural face or a success-by-margin value. A death save gains one ordinary success, not natural20healing. For a genuinely authorized crafting completion check, this means Standard success in that craft procedure, retaining all work/material/access requirements and any independently reviewed quality adjustment.\n\nFor your side of an actual opposed ability check, NEW it wins against an ordinary rolled opponent regardless of total. If both sides commit an explicit automatic-success effect to the same opposition, resolve their incompatible claims by preserving the existing state, as with the Core initiating-tie rule; no retroactive transfer of an already resolved result. This declared conflict rule needs joint review. The feat does not create an ability check when none is allowed, overcome physical impossibility, convert an attack into a check, grant NPC consent outside a legitimately established social success outcome, or grant knowledge unavailable to the legal task. Only one check/save is affected; another save from the same damage event remains separate. Other outcome-triggered rules see ordinary Success, no natural20/1 and no invented numerical margin.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A living dying character is about to record its third death-save failure. Spending this feat before that failure commits replaces it with one success; it does not restore1HP or erase earlier counters.",
    "A qualified craft completion would fail after all its real work. The feat gives Standard success, not automatic Masterwork or free ingredients. An impossible request with no authorized check cannot be made possible by spending it."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Retain CHA15 and an actual already established worship-of-a-deity credential without selecting a new deity or interpreting doctrine here. NEW once per beneficial Long Rest, after your own actual saving throw or ability check is called for, or after its result is known but before its consequences commit, declare this feat to replace that one outcome with ordinary Success. No Action, component or new roll is required; it can protect a living incapacitated creature making an actual save, including a death save. It cannot act after death or reverse committed harm. Fixed-DC task outcome becomes Success, not Critical Success; saves become successful without a natural face or a success-by-margin value. A death save gains one ordinary success, not natural20healing. For a genuinely authorized crafting completion check, this means Standard success in that craft procedure, retaining all work/material/access requirements and any independently reviewed quality adjustment.

For your side of an actual opposed ability check, NEW it wins against an ordinary rolled opponent regardless of total. If both sides commit an explicit automatic-success effect to the same opposition, resolve their incompatible claims by preserving the existing state, as with the Core initiating-tie rule; no retroactive transfer of an already resolved result. This declared conflict rule needs joint review. The feat does not create an ability check when none is allowed, overcome physical impossibility, convert an attack into a check, grant NPC consent outside a legitimately established social success outcome, or grant knowledge unavailable to the legal task. Only one check/save is affected; another save from the same damage event remains separate. Other outcome-triggered rules see ordinary Success, no natural20/1 and no invented numerical margin.

### Original-position authored review references

```json
[
  {
    "id": "MF-06-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/10"
  },
  {
    "id": "MF-06-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/11"
  }
]
```

## MF-07 — Elemental Adept

### Complete original object

```json
{
  "id": "elementalAdept",
  "name": "Elemental Adept",
  "description": "You have mastery over elemental magic.",
  "prerequisite": "Ability to cast at least one spell",
  "effect": "Choose an element. Spells you cast ignore resistance to that damage type and treat 1s as 2s on damage dice.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Give a finite eligible damage-type choice and its acquisition/replacement rule. Define resistance bypass without immunity bypass, damage1-to2 ordering with critical/maximized/rerolled dice, multiple packets and nonspell riders; preserve real spellcasting prerequisite and no new damage entitlement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "elementalAdept",
  "name": "Elemental Adept",
  "cohort": "magic_core",
  "questionId": "MF-07",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/6",
  "originalQuestion": "Give a finite eligible damage-type choice and its acquisition/replacement rule. Define resistance bypass without immunity bypass, damage1-to2 ordering with critical/maximized/rerolled dice, multiple packets and nonspell riders; preserve real spellcasting prerequisite and no new damage entitlement.",
  "originalSourceObject": {
    "id": "elementalAdept",
    "name": "Elemental Adept",
    "description": "You have mastery over elemental magic.",
    "prerequisite": "Ability to cast at least one spell",
    "effect": "Choose an element. Spells you cast ignore resistance to that damage type and treat 1s as 2s on damage dice.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "e7766345b14438353a3f085bf7bb633220121ba10bc5c3559e62d0e26f559ccd",
  "submittedProcedure": "Choose one of acid,cold,fire,lightning or thunder permanently. Only your actual personally cast spell-damage components of that chosen type ignore resistance to that type. NEW this bypass covers normal half resistance and an explicit percentage reduction actually identified as resistance, but not immunity, vulnerability, damage thresholds, cover, generic flat prevention, target ineligibility or a protection not classed as resistance. No extra damage entitlement is created. For each genuine damage die of that type belonging to the spell’s own roll, treat a final rolled face1as2after authorized rerolls. Critical dice qualify as actual spell damage dice; each die identity is adjusted once. A maximum substituted without a roll has no rolled1to change. Flat1damage is not a damage die. Mixed components of other types are unchanged. Independent weapon/item riders and summoned-creature attacks do not become spell damage from this feat. No automatic conversion of the spell’s damage type or effect on spells cast by allies.",
  "submittedNewChoices": "Closed5-type choice; explicitly typed resistance bypass scope; final actual face and component ownership.",
  "submittedWorkedCases": [
    "A chosen-fire spell rolls1and4on2d6; its native fire total becomes6before other bonuses and ignores the target’s fire resistance. Fire immunity still gives0.",
    "A spell with4cold and1flat fire does not change the flat fire1to2. An independent flaming weapon rider added to a melee attack does not qualify merely because its wielder knows this feat."
  ],
  "decision": "Retain the MF-07 complete grant/procedure and boundaries. Closed5-type choice; explicitly typed resistance bypass scope; final actual face and component ownership. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose one of acid,cold,fire,lightning or thunder permanently. Only your actual personally cast spell-damage components of that chosen type ignore resistance to that type. NEW this bypass covers normal half resistance and an explicit percentage reduction actually identified as resistance, but not immunity, vulnerability, damage thresholds, cover, generic flat prevention, target ineligibility or a protection not classed as resistance. No extra damage entitlement is created. For each genuine damage die of that type belonging to the spell’s own roll, treat a final rolled face1as2after authorized rerolls. Critical dice qualify as actual spell damage dice; each die identity is adjusted once. A maximum substituted without a roll has no rolled1to change. Flat1damage is not a damage die. Mixed components of other types are unchanged. Independent weapon/item riders and summoned-creature attacks do not become spell damage from this feat. No automatic conversion of the spell’s damage type or effect on spells cast by allies.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A chosen-fire spell rolls1and4on2d6; its native fire total becomes6before other bonuses and ignores the target’s fire resistance. Fire immunity still gives0.",
    "A spell with4cold and1flat fire does not change the flat fire1to2. An independent flaming weapon rider added to a melee attack does not qualify merely because its wielder knows this feat."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose one of acid,cold,fire,lightning or thunder permanently. Only your actual personally cast spell-damage components of that chosen type ignore resistance to that type. NEW this bypass covers normal half resistance and an explicit percentage reduction actually identified as resistance, but not immunity, vulnerability, damage thresholds, cover, generic flat prevention, target ineligibility or a protection not classed as resistance. No extra damage entitlement is created. For each genuine damage die of that type belonging to the spell’s own roll, treat a final rolled face1as2after authorized rerolls. Critical dice qualify as actual spell damage dice; each die identity is adjusted once. A maximum substituted without a roll has no rolled1to change. Flat1damage is not a damage die. Mixed components of other types are unchanged. Independent weapon/item riders and summoned-creature attacks do not become spell damage from this feat. No automatic conversion of the spell’s damage type or effect on spells cast by allies.

### Original-position authored review references

```json
[
  {
    "id": "MF-07-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/12"
  },
  {
    "id": "MF-07-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/13"
  }
]
```

## MF-08 — Elemental Affinity

### Complete original object

```json
{
  "id": "elemental_affinity",
  "name": "Elemental Affinity",
  "description": "You have a natural connection to elemental forces.",
  "prerequisite": "Level 5",
  "effect": "+10% damage with chosen element",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Resolve level5, finite elemental choice, which actual damage sources qualify, the exact10-percent arithmetic/rounding stage and stacking with resistance, criticals, extra dice, multi-hit/area/ongoing effects. Current percentage text is active source, not a discarded legacy clause."
```

### Preserved original source direction (historical)

```json
{
  "featId": "elemental_affinity",
  "name": "Elemental Affinity",
  "cohort": "magic_core",
  "questionId": "MF-08",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/7",
  "originalQuestion": "Resolve level5, finite elemental choice, which actual damage sources qualify, the exact10-percent arithmetic/rounding stage and stacking with resistance, criticals, extra dice, multi-hit/area/ongoing effects. Current percentage text is active source, not a discarded legacy clause.",
  "originalSourceObject": {
    "id": "elemental_affinity",
    "name": "Elemental Affinity",
    "description": "You have a natural connection to elemental forces.",
    "prerequisite": "Level 5",
    "effect": "+10% damage with chosen element",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "fd4189600a2bca83635c9f8ba86d3bf99026acdc5f206b376829fc5406f7d4b8",
  "submittedProcedure": "At total character level5or later choose acid,cold,fire,lightning or thunder permanently. NEW the source is not restricted to spells: your actual personally caused damage of that type qualifies, including a legal weapon elemental component and an attributable deployed trap, but not a companion’s separate attack, another operator’s damage, reflected/copied damage or a resource/HP payment. For each genuine damage event, total the chosen-type components after normal dice/critical resolution and eligible flat bonuses but before percentage bonuses/target defenses. Add floor(that total×10/100) damage of the same type once to that event. Where another genuine percentage feat also applies, both calculate from the same pre-percentage baseline in their actual scopes; neither compounds the other’s bonus. A shared area damage result supplies the same base to each legitimate target’s event and defenses, not a multiplied total based on target count. Distinct actual repeated hits/ticks may each qualify; replaying one event or splitting one component cannot generate another bonus. The damage is still the same event for Wounds, concentration and resource triggers.",
  "submittedNewChoices": "Closed5-type choice; all personally attributable actual damage; one10%bonus per event before defenses and without percentage compounding.",
  "submittedWorkedCases": [
    "An event has19fire and6piercing before percentage bonuses. Fire Affinity adds1fire, giving20fire/6piercing before defenses, not a10%increase to all25.",
    "Three separate legal fire hits of9each each gain0from floor(0.9); they cannot be combined into27to claim2extra damage. A genuine one-event27fire packet gains2."
  ],
  "decision": "Retain the MF-08 complete grant/procedure and boundaries. Closed5-type choice; all personally attributable actual damage; one10%bonus per event before defenses and without percentage compounding. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "At total character level5or later choose acid,cold,fire,lightning or thunder permanently. NEW the source is not restricted to spells: your actual personally caused damage of that type qualifies, including a legal weapon elemental component and an attributable deployed trap, but not a companion’s separate attack, another operator’s damage, reflected/copied damage or a resource/HP payment. For each genuine damage event, total the chosen-type components after normal dice/critical resolution and eligible flat bonuses but before percentage bonuses/target defenses. Add floor(that total×10/100) damage of the same type once to that event. Where another genuine percentage feat also applies, both calculate from the same pre-percentage baseline in their actual scopes; neither compounds the other’s bonus. A shared area damage result supplies the same base to each legitimate target’s event and defenses, not a multiplied total based on target count. Distinct actual repeated hits/ticks may each qualify; replaying one event or splitting one component cannot generate another bonus. The damage is still the same event for Wounds, concentration and resource triggers.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An event has19fire and6piercing before percentage bonuses. Fire Affinity adds1fire, giving20fire/6piercing before defenses, not a10%increase to all25.",
    "Three separate legal fire hits of9each each gain0from floor(0.9); they cannot be combined into27to claim2extra damage. A genuine one-event27fire packet gains2."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At total character level5or later choose acid,cold,fire,lightning or thunder permanently. NEW the source is not restricted to spells: your actual personally caused damage of that type qualifies, including a legal weapon elemental component and an attributable deployed trap, but not a companion’s separate attack, another operator’s damage, reflected/copied damage or a resource/HP payment. For each genuine damage event, total the chosen-type components after normal dice/critical resolution and eligible flat bonuses but before percentage bonuses/target defenses. Add floor(that total×10/100) damage of the same type once to that event. Where another genuine percentage feat also applies, both calculate from the same pre-percentage baseline in their actual scopes; neither compounds the other’s bonus. A shared area damage result supplies the same base to each legitimate target’s event and defenses, not a multiplied total based on target count. Distinct actual repeated hits/ticks may each qualify; replaying one event or splitting one component cannot generate another bonus. The damage is still the same event for Wounds, concentration and resource triggers.

### Original-position authored review references

```json
[
  {
    "id": "MF-08-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/14"
  },
  {
    "id": "MF-08-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/15"
  }
]
```

## MF-09 — Elemental Mastery

### Complete original object

```json
{
  "id": "elemental_mastery",
  "name": "Elemental Mastery",
  "description": "You have mastered elemental magic.",
  "prerequisite": "Ability to cast 3rd level spells",
  "effect": "Choose an element. You can change the damage type of your spells to that element.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Resolve the3rd-level-spell prerequisite by actual casting route/rank. Define element choice, declaration, partial/mixed damage conversion and whether nondamage riders, school, creature exclusions and condition types stay unchanged. No generic upcasting, free cast or environmental transformation."
```

### Preserved original source direction (historical)

```json
{
  "featId": "elemental_mastery",
  "name": "Elemental Mastery",
  "cohort": "magic_core",
  "questionId": "MF-09",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/8",
  "originalQuestion": "Resolve the3rd-level-spell prerequisite by actual casting route/rank. Define element choice, declaration, partial/mixed damage conversion and whether nondamage riders, school, creature exclusions and condition types stay unchanged. No generic upcasting, free cast or environmental transformation.",
  "originalSourceObject": {
    "id": "elemental_mastery",
    "name": "Elemental Mastery",
    "description": "You have mastered elemental magic.",
    "prerequisite": "Ability to cast 3rd level spells",
    "effect": "Choose an element. You can change the damage type of your spells to that element.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "a49de4af107e8825f8fe0ee406b940715040f2bda755e0a50faeca036ba919f0",
  "submittedProcedure": "Require an actual acquired route to cast at least one rank3spell; total level or sufficientRP alone does not qualify. Choose acid,cold,fire,lightning or thunder permanently. NEW at legal cast commitment, choose whether to convert all of that spell’s own damage, or all components of one or more declared original damage types, to your chosen type for that entire cast. Record the mapping before attacks/saves; no reactive switching after learning a defense or rolling damage. Its later genuine spell-native pulses use the same mapping, while independent riders, summoned-creature/weapon attacks and other creatures’ effects retain their own types unless the original spell itself expressly calls those packets its own spell damage.\n\nConversion changes damage type only. Dice,amount,school,rank,range,actions,target exclusions,components,concentration and conditions keep their exact rules. A condition named Burning, Chilled or Shocked is not renamed or removed merely because a damage component changes; actual immunity to that condition still applies. Healing/tempHP/resource costs cannot become damage. Changing necrotic damage tofire does not grant a new healing rider, and a spell’s existing “heal equal to actual damage” clause still uses its own lawful recorded amount. No freecast, generic upcast, environmental transformation or resistance bypass follows; Elemental Adept is a separate qualifying modifier.",
  "submittedNewChoices": "Per-cast declared whole-type mapping; delayed packet consistency; independent-rider and nondamage boundaries.",
  "submittedWorkedCases": [
    "Before casting a spell with cold andforce native components, you choose to convert only its cold components tolightning. Its force component and later cold-derived condition remain governed by their own text.",
    "A spell creates a companion that later attacks. Converting the summoning spell’s nonexistent direct damage creates no lightning attacks for that separate creature."
  ],
  "decision": "Retain the MF-09 complete grant/procedure and boundaries. Per-cast declared whole-type mapping; delayed packet consistency; independent-rider and nondamage boundaries. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require an actual acquired route to cast at least one rank3spell; total level or sufficientRP alone does not qualify. Choose acid,cold,fire,lightning or thunder permanently. NEW at legal cast commitment, choose whether to convert all of that spell’s own damage, or all components of one or more declared original damage types, to your chosen type for that entire cast. Record the mapping before attacks/saves; no reactive switching after learning a defense or rolling damage. Its later genuine spell-native pulses use the same mapping, while independent riders, summoned-creature/weapon attacks and other creatures’ effects retain their own types unless the original spell itself expressly calls those packets its own spell damage.\n\nConversion changes damage type only. Dice,amount,school,rank,range,actions,target exclusions,components,concentration and conditions keep their exact rules. A condition named Burning, Chilled or Shocked is not renamed or removed merely because a damage component changes; actual immunity to that condition still applies. Healing/tempHP/resource costs cannot become damage. Changing necrotic damage tofire does not grant a new healing rider, and a spell’s existing “heal equal to actual damage” clause still uses its own lawful recorded amount. No freecast, generic upcast, environmental transformation or resistance bypass follows; Elemental Adept is a separate qualifying modifier.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Before casting a spell with cold andforce native components, you choose to convert only its cold components tolightning. Its force component and later cold-derived condition remain governed by their own text.",
    "A spell creates a companion that later attacks. Converting the summoning spell’s nonexistent direct damage creates no lightning attacks for that separate creature."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require an actual acquired route to cast at least one rank3spell; total level or sufficientRP alone does not qualify. Choose acid,cold,fire,lightning or thunder permanently. NEW at legal cast commitment, choose whether to convert all of that spell’s own damage, or all components of one or more declared original damage types, to your chosen type for that entire cast. Record the mapping before attacks/saves; no reactive switching after learning a defense or rolling damage. Its later genuine spell-native pulses use the same mapping, while independent riders, summoned-creature/weapon attacks and other creatures’ effects retain their own types unless the original spell itself expressly calls those packets its own spell damage.

Conversion changes damage type only. Dice,amount,school,rank,range,actions,target exclusions,components,concentration and conditions keep their exact rules. A condition named Burning, Chilled or Shocked is not renamed or removed merely because a damage component changes; actual immunity to that condition still applies. Healing/tempHP/resource costs cannot become damage. Changing necrotic damage tofire does not grant a new healing rider, and a spell’s existing “heal equal to actual damage” clause still uses its own lawful recorded amount. No freecast, generic upcast, environmental transformation or resistance bypass follows; Elemental Adept is a separate qualifying modifier.

### Original-position authored review references

```json
[
  {
    "id": "MF-09-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/16"
  },
  {
    "id": "MF-09-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/17"
  }
]
```

## MF-10 — Enchantment Focus

### Complete original object

```json
{
  "id": "enchantment_focus",
  "name": "Enchantment Focus",
  "description": "Your enchantment spells are more effective.",
  "prerequisite": "Ability to cast enchantment spells",
  "effect": "Creatures have disadvantage on saving throws against your enchantment spells.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind actual Enchantment school and current repertoire, initial and repeated saving throws, spells with multiple schools/placements and copied or item casts. Define ordinary advantage cancellation and source-specific control protections; do not extend disadvantage to opposed ability checks or all social influence."
```

### Preserved original source direction (historical)

```json
{
  "featId": "enchantment_focus",
  "name": "Enchantment Focus",
  "cohort": "magic_core",
  "questionId": "MF-10",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/9",
  "originalQuestion": "Bind actual Enchantment school and current repertoire, initial and repeated saving throws, spells with multiple schools/placements and copied or item casts. Define ordinary advantage cancellation and source-specific control protections; do not extend disadvantage to opposed ability checks or all social influence.",
  "originalSourceObject": {
    "id": "enchantment_focus",
    "name": "Enchantment Focus",
    "description": "Your enchantment spells are more effective.",
    "prerequisite": "Ability to cast enchantment spells",
    "effect": "Creatures have disadvantage on saving throws against your enchantment spells.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "12b1b4d3e923d0e00cfd6f3fc1a8809d814ba1ba4652f3d3f1c3c2fc4080d5c7",
  "submittedProcedure": "Require actual access to a spell cast through an Enchantment placement. Creatures have disadvantage on actual saving throws against spells you personally cast through their Enchantment school/mode. NEW this includes initial and later repeat saves belonging to that same Enchantment cast, for its actual duration; it includes a qualifying spell-cast item/feat route whose actual recorded school is Enchantment. A same-name Illusion or Universal placement is not Enchantment merely because another class has that school. Apply ordinary advantage/disadvantage cancellation, not an extra die per feat or repeated disadvantage. Actual control immunity, target restrictions, voluntary-save rules, information protection and automatic ending remain. A separate CONconcentration save caused by an Enchantment spell’s damage is a save to maintain the target’s own concentration, not a save against your spell, and receives no disadvantage from this feat. Ability checks, opposed social rolls and nonspell class techniques are outside its scope.",
  "submittedNewChoices": "Actual casting-placement school and all native save timings; excludes consequential concentration saves and ability checks.",
  "submittedWorkedCases": [
    "An actual Enchantment control spell’s initial and later escape saves have disadvantage. A target with general advantage on saves against spells rolls one ordinary die after cancellation.",
    "Charm Person cast using a documented Illusion placement receives no Enchantment Focus disadvantage even though another class’s same-name version is Enchantment."
  ],
  "decision": "Retain the MF-10 complete grant/procedure and boundaries. Actual casting-placement school and all native save timings; excludes consequential concentration saves and ability checks. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require actual access to a spell cast through an Enchantment placement. Creatures have disadvantage on actual saving throws against spells you personally cast through their Enchantment school/mode. NEW this includes initial and later repeat saves belonging to that same Enchantment cast, for its actual duration; it includes a qualifying spell-cast item/feat route whose actual recorded school is Enchantment. A same-name Illusion or Universal placement is not Enchantment merely because another class has that school. Apply ordinary advantage/disadvantage cancellation, not an extra die per feat or repeated disadvantage. Actual control immunity, target restrictions, voluntary-save rules, information protection and automatic ending remain. A separate CONconcentration save caused by an Enchantment spell’s damage is a save to maintain the target’s own concentration, not a save against your spell, and receives no disadvantage from this feat. Ability checks, opposed social rolls and nonspell class techniques are outside its scope.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An actual Enchantment control spell’s initial and later escape saves have disadvantage. A target with general advantage on saves against spells rolls one ordinary die after cancellation.",
    "Charm Person cast using a documented Illusion placement receives no Enchantment Focus disadvantage even though another class’s same-name version is Enchantment."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual access to a spell cast through an Enchantment placement. Creatures have disadvantage on actual saving throws against spells you personally cast through their Enchantment school/mode. NEW this includes initial and later repeat saves belonging to that same Enchantment cast, for its actual duration; it includes a qualifying spell-cast item/feat route whose actual recorded school is Enchantment. A same-name Illusion or Universal placement is not Enchantment merely because another class has that school. Apply ordinary advantage/disadvantage cancellation, not an extra die per feat or repeated disadvantage. Actual control immunity, target restrictions, voluntary-save rules, information protection and automatic ending remain. A separate CONconcentration save caused by an Enchantment spell’s damage is a save to maintain the target’s own concentration, not a save against your spell, and receives no disadvantage from this feat. Ability checks, opposed social rolls and nonspell class techniques are outside its scope.

### Original-position authored review references

```json
[
  {
    "id": "MF-10-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/18"
  },
  {
    "id": "MF-10-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/19"
  }
]
```

## MF-11 — Evocation Focus

### Complete original object

```json
{
  "id": "evocation_focus",
  "name": "Evocation Focus",
  "description": "Your evocation spells deal more damage.",
  "prerequisite": "Ability to cast evocation spells",
  "effect": "Your evocation spells deal +1 damage per die rolled.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Define+1 per actual eligible damage die, school/placement, critical bonus dice, maximized/nonrolled dice, rerolls, shared area rolls, delayed/ongoing packets and added nonspell riders. Flat damage and repeated references to one rolled result must not manufacture extra dice."
```

### Preserved original source direction (historical)

```json
{
  "featId": "evocation_focus",
  "name": "Evocation Focus",
  "cohort": "magic_core",
  "questionId": "MF-11",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/10",
  "originalQuestion": "Define+1 per actual eligible damage die, school/placement, critical bonus dice, maximized/nonrolled dice, rerolls, shared area rolls, delayed/ongoing packets and added nonspell riders. Flat damage and repeated references to one rolled result must not manufacture extra dice.",
  "originalSourceObject": {
    "id": "evocation_focus",
    "name": "Evocation Focus",
    "description": "Your evocation spells deal more damage.",
    "prerequisite": "Ability to cast evocation spells",
    "effect": "Your evocation spells deal +1 damage per die rolled.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "0c354780d700e1216a9b622a3473561c21968200b79acaa9ce18e0f2cb8b4148",
  "submittedProcedure": "Require actual acquired Evocation spellcasting. On each genuine damage roll of a spell you personally cast through an Evocation placement, add+1for each actual eligible spell damage die rolled for that final result. NEW count each die identity once, including extra critical spell dice and explicit dice added to that spell’s own roll; a reroll replaces the same die rather than adding another+1. Add the flat total after its dice and before percentage modifiers/defenses. Independent item/weapon/class riders keep their own scope and do not increase the count. A fixed damage amount or a die fully replaced by a maximum without rolling contributes0eligible rolled dice. Do not roll meaningless dice just to claim the bonus. An eligible shared area roll receives one+Nresult, then each actual target resolves that result through its own defenses; do not add another+Nfor every extra target to the shared value. Later actual Evocation damage rolls can qualify independently. No+1to healing, tempHP, summons’ own attacks, ordinary action damage after conjuring a weapon, saveDC or another school’s placement.",
  "submittedNewChoices": "Actual distinct rolled-die count; critical and reroll treatment; maximization/fixed-result boundary.",
  "submittedWorkedCases": [
    "A real2d6Evocation damage roll of2and5gets+2for9before defenses. Rerolling the2to4still gives+2, not+3.",
    "A natural20chosen cantrip whose2critical dice are wholly maximized through Cantrip Mastery has no actually rolled damage dice for this feat; its maximum remains the dice maximum plus other applicable flat bonuses."
  ],
  "decision": "Retain the MF-11 complete grant/procedure and boundaries. Actual distinct rolled-die count; critical and reroll treatment; maximization/fixed-result boundary. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require actual acquired Evocation spellcasting. On each genuine damage roll of a spell you personally cast through an Evocation placement, add+1for each actual eligible spell damage die rolled for that final result. NEW count each die identity once, including extra critical spell dice and explicit dice added to that spell’s own roll; a reroll replaces the same die rather than adding another+1. Add the flat total after its dice and before percentage modifiers/defenses. Independent item/weapon/class riders keep their own scope and do not increase the count. A fixed damage amount or a die fully replaced by a maximum without rolling contributes0eligible rolled dice. Do not roll meaningless dice just to claim the bonus. An eligible shared area roll receives one+Nresult, then each actual target resolves that result through its own defenses; do not add another+Nfor every extra target to the shared value. Later actual Evocation damage rolls can qualify independently. No+1to healing, tempHP, summons’ own attacks, ordinary action damage after conjuring a weapon, saveDC or another school’s placement.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A real2d6Evocation damage roll of2and5gets+2for9before defenses. Rerolling the2to4still gives+2, not+3.",
    "A natural20chosen cantrip whose2critical dice are wholly maximized through Cantrip Mastery has no actually rolled damage dice for this feat; its maximum remains the dice maximum plus other applicable flat bonuses."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual acquired Evocation spellcasting. On each genuine damage roll of a spell you personally cast through an Evocation placement, add+1for each actual eligible spell damage die rolled for that final result. NEW count each die identity once, including extra critical spell dice and explicit dice added to that spell’s own roll; a reroll replaces the same die rather than adding another+1. Add the flat total after its dice and before percentage modifiers/defenses. Independent item/weapon/class riders keep their own scope and do not increase the count. A fixed damage amount or a die fully replaced by a maximum without rolling contributes0eligible rolled dice. Do not roll meaningless dice just to claim the bonus. An eligible shared area roll receives one+Nresult, then each actual target resolves that result through its own defenses; do not add another+Nfor every extra target to the shared value. Later actual Evocation damage rolls can qualify independently. No+1to healing, tempHP, summons’ own attacks, ordinary action damage after conjuring a weapon, saveDC or another school’s placement.

### Original-position authored review references

```json
[
  {
    "id": "MF-11-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/20"
  },
  {
    "id": "MF-11-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/21"
  }
]
```

## MF-12 — Familiar Bond

### Complete original object

```json
{
  "id": "familiar_bond",
  "name": "Familiar Bond",
  "description": "Your bond with your familiar is stronger.",
  "prerequisite": "Ability to cast find familiar",
  "effect": "Your familiar gains hit points equal to your level and can attack using your spell attack bonus.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Use the full Find Familiar card and actual companion command/stat rules. Define maximum versus current HP change, level scaling/damage deficit, one physical familiar identity, eligible attack profile, action/command cost and casting ability. Spell attack bonus supplies no missing attack damage, reach, weapon, extra turn or resurrection."
```

### Preserved original source direction (historical)

```json
{
  "featId": "familiar_bond",
  "name": "Familiar Bond",
  "cohort": "magic_core",
  "questionId": "MF-12",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/11",
  "originalQuestion": "Use the full Find Familiar card and actual companion command/stat rules. Define maximum versus current HP change, level scaling/damage deficit, one physical familiar identity, eligible attack profile, action/command cost and casting ability. Spell attack bonus supplies no missing attack damage, reach, weapon, extra turn or resurrection.",
  "originalSourceObject": {
    "id": "familiar_bond",
    "name": "Familiar Bond",
    "description": "Your bond with your familiar is stronger.",
    "prerequisite": "Ability to cast find familiar",
    "effect": "Your familiar gains hit points equal to your level and can attack using your spell attack bonus.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "bea9d7f867e8c31c4b4e5d07a8db262037fbfa3cdc4843d136e120322d685114",
  "submittedProcedure": "Require actual ability to cast the exact Find Familiar identity. Carry its already reviewed maximum-HP integration unchanged: your current eligible Find Familiar has+your current total character level maximumHP; include the bonus in a genuine new creation’s startingHP, but later acquisition/level increase adds capacity only and a decrease clamps without damage/healing. One feat identity applies once to the current actual familiar body. Changing a label, transfer, resummoning or an old snapshot does not duplicate one creature or its modifier.\n\nThe current reviewed Find Familiar already attacks using the summoning casting route’s spell attack bonus, with its fixed-on-cast melee/ranged mode,type and actual S d6profile. This feat’s attack sentence confirms that entitlement; it supplies no second attack, additional die, new mode or extra command. Keep the source’s Bonus Action command,60-foot/perception requirement, acts-immediately-after-owner timing and one damaging companion action total per owner per round. Without the actual command it moves/Dodges as printed. NEW if the spell was supplied through an explicitly approved feat casting route, use that route’s recorded ability and its agreed payload-level rule, never an arbitrary highest class modifier. Concentration,max1minute,0HPdisappearance,full-cost replacement and no resource-generating corpse remain. The feat does not convert a real pet or a differently named Summon Familiar into this spell’s familiar automatically.",
  "submittedNewChoices": "Full feat acquisition/one-body binding; attack clause retains already existing source permission rather than granting another attack.",
  "submittedWorkedCases": [
    "A Wizard3/other-class4has total level7. A new ordinary Wizard Find Familiar has its base6HP plus Familiar Bond7for13maximum/startingHP before other legitimate creation modifiers.",
    "The same familiar at currentHP5later gains one owner level. Its Familiar Bond capacity rises by1but currentHPstays5. A second commanded companion cannot also damage that round merely because this familiar’s attack bonus is the owner’s."
  ],
  "decision": "Retain the MF-12 complete grant/procedure and boundaries. Full feat acquisition/one-body binding; attack clause retains already existing source permission rather than granting another attack. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require actual ability to cast the exact Find Familiar identity. Carry its already reviewed maximum-HP integration unchanged: your current eligible Find Familiar has+your current total character level maximumHP; include the bonus in a genuine new creation’s startingHP, but later acquisition/level increase adds capacity only and a decrease clamps without damage/healing. One feat identity applies once to the current actual familiar body. Changing a label, transfer, resummoning or an old snapshot does not duplicate one creature or its modifier.\n\nThe current reviewed Find Familiar already attacks using the summoning casting route’s spell attack bonus, with its fixed-on-cast melee/ranged mode,type and actual S d6profile. This feat’s attack sentence confirms that entitlement; it supplies no second attack, additional die, new mode or extra command. Keep the source’s Bonus Action command,60-foot/perception requirement, acts-immediately-after-owner timing and one damaging companion action total per owner per round. Without the actual command it moves/Dodges as printed. NEW if the spell was supplied through an explicitly approved feat casting route, use that route’s recorded ability and its agreed payload-level rule, never an arbitrary highest class modifier. Concentration,max1minute,0HPdisappearance,full-cost replacement and no resource-generating corpse remain. The feat does not convert a real pet or a differently named Summon Familiar into this spell’s familiar automatically.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A Wizard3/other-class4has total level7. A new ordinary Wizard Find Familiar has its base6HP plus Familiar Bond7for13maximum/startingHP before other legitimate creation modifiers.",
    "The same familiar at currentHP5later gains one owner level. Its Familiar Bond capacity rises by1but currentHPstays5. A second commanded companion cannot also damage that round merely because this familiar’s attack bonus is the owner’s."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual ability to cast the exact Find Familiar identity. Carry its already reviewed maximum-HP integration unchanged: your current eligible Find Familiar has+your current total character level maximumHP; include the bonus in a genuine new creation’s startingHP, but later acquisition/level increase adds capacity only and a decrease clamps without damage/healing. One feat identity applies once to the current actual familiar body. Changing a label, transfer, resummoning or an old snapshot does not duplicate one creature or its modifier.

The current reviewed Find Familiar already attacks using the summoning casting route’s spell attack bonus, with its fixed-on-cast melee/ranged mode,type and actual S d6profile. This feat’s attack sentence confirms that entitlement; it supplies no second attack, additional die, new mode or extra command. Keep the source’s Bonus Action command,60-foot/perception requirement, acts-immediately-after-owner timing and one damaging companion action total per owner per round. Without the actual command it moves/Dodges as printed. NEW if the spell was supplied through an explicitly approved feat casting route, use that route’s recorded ability and its agreed payload-level rule, never an arbitrary highest class modifier. Concentration,max1minute,0HPdisappearance,full-cost replacement and no resource-generating corpse remain. The feat does not convert a real pet or a differently named Summon Familiar into this spell’s familiar automatically.

### Original-position authored review references

```json
[
  {
    "id": "MF-12-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/22"
  },
  {
    "id": "MF-12-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/23"
  }
]
```

## MF-13 — Fey Touched

### Complete original object

```json
{
  "id": "feyTouched",
  "name": "Fey Touched",
  "description": "Your exposure to the Feywild has changed you.",
  "prerequisite": "None",
  "effect": "You learn misty step and one 1st-level divination or enchantment spell. You can cast each once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve both spell grants and separate once-per-Long-Rest casts. Misty Step exists only as an ancestry-grant supplemental card, not an ordinary-class spell: decide an explicit feat route without silently changing the ordinary catalog. Resolve rank1 school choices, ability/DC, components, charges versus RP/repertoire and all spell-review dependencies. Preserve flavor; no Feywild cosmology review."
```

### Preserved original source direction (historical)

```json
{
  "featId": "feyTouched",
  "name": "Fey Touched",
  "cohort": "magic_core",
  "questionId": "MF-13",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/12",
  "originalQuestion": "Preserve both spell grants and separate once-per-Long-Rest casts. Misty Step exists only as an ancestry-grant supplemental card, not an ordinary-class spell: decide an explicit feat route without silently changing the ordinary catalog. Resolve rank1 school choices, ability/DC, components, charges versus RP/repertoire and all spell-review dependencies. Preserve flavor; no Feywild cosmology review.",
  "originalSourceObject": {
    "id": "feyTouched",
    "name": "Fey Touched",
    "description": "Your exposure to the Feywild has changed you.",
    "prerequisite": "None",
    "effect": "You learn misty step and one 1st-level divination or enchantment spell. You can cast each once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "70f9fe7a0419ae63c972975b25e9ec6b87d37f126abb234c896c3459bb94c3fd",
  "submittedProcedure": "At acquisition choose INT,WIS orCHA permanently for this feat. Learn the exact supplemental Misty Step procedure as a NEW feat-only rank2Conjuration route and one actual rank1Divination orEnchantment placement from the ordinary catalog. Record that selected identity,school and rank1placement; the same name’s higher-rank/different-school mode is not included. The complete choice pool is supplied with current review status; playable use requires the exact payload’s completed review. These are additional feat entitlements, not ordinary class spells learned/prepared for free. Each has its own one-per-beneficial-Long-Rest use under the shared feat casting route. No ability-score increase is printed or granted.\n\nMisty Step retains the reviewed Bonus Action,V,Self teleport to a visible unoccupied fitting destination within30feet, self and normally carried compatible gear, no passenger/plane travel, actual blockers/hazards and instantaneous ending. This explicit feat route does not add the spell to any ordinary class catalog. The chosen rank1spell retains its actual components/action/concentration and source-specific limits. Neither choice may be freely replaced after a rest. The Feywild description is preserved as flavor without establishing its geography, origins or cosmological relationships.",
  "submittedNewChoices": "Permanent mental ability; explicit nonclass Misty Step grant; rank1school/placement choices and separate LRcharges.",
  "submittedWorkedCases": [
    "A Soldier with this feat can use its Misty Step charge with the stated Bonus Action and Vcomponent; it gains no RPpool or ordinary Conjuration list.",
    "Using the chosen rank1spell does not expend Misty Step’s separate charge. A later class-cast of the same named spell must meet that class’s own learned/prepared/access rules and actual cost."
  ],
  "decision": "Retain the MF-13 complete grant/procedure and boundaries. Permanent mental ability; explicit nonclass Misty Step grant; rank1school/placement choices and separate LRcharges. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "At acquisition choose INT,WIS orCHA permanently for this feat. Learn the exact supplemental Misty Step procedure as a NEW feat-only rank2Conjuration route and one actual rank1Divination orEnchantment placement from the ordinary catalog. Record that selected identity,school and rank1placement; the same name’s higher-rank/different-school mode is not included. The complete choice pool is supplied with current review status; playable use requires the exact payload’s completed review. These are additional feat entitlements, not ordinary class spells learned/prepared for free. Each has its own one-per-beneficial-Long-Rest use under the shared feat casting route. No ability-score increase is printed or granted.\n\nMisty Step retains the reviewed Bonus Action,V,Self teleport to a visible unoccupied fitting destination within30feet, self and normally carried compatible gear, no passenger/plane travel, actual blockers/hazards and instantaneous ending. This explicit feat route does not add the spell to any ordinary class catalog. The chosen rank1spell retains its actual components/action/concentration and source-specific limits. Neither choice may be freely replaced after a rest. The Feywild description is preserved as flavor without establishing its geography, origins or cosmological relationships.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A Soldier with this feat can use its Misty Step charge with the stated Bonus Action and Vcomponent; it gains no RPpool or ordinary Conjuration list.",
    "Using the chosen rank1spell does not expend Misty Step’s separate charge. A later class-cast of the same named spell must meet that class’s own learned/prepared/access rules and actual cost."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At acquisition choose INT,WIS orCHA permanently for this feat. Learn the exact supplemental Misty Step procedure as a NEW feat-only rank2Conjuration route and one actual rank1Divination orEnchantment placement from the ordinary catalog. Record that selected identity,school and rank1placement; the same name’s higher-rank/different-school mode is not included. The complete choice pool is supplied with current review status; playable use requires the exact payload’s completed review. These are additional feat entitlements, not ordinary class spells learned/prepared for free. Each has its own one-per-beneficial-Long-Rest use under the shared feat casting route. No ability-score increase is printed or granted.

Misty Step retains the reviewed Bonus Action,V,Self teleport to a visible unoccupied fitting destination within30feet, self and normally carried compatible gear, no passenger/plane travel, actual blockers/hazards and instantaneous ending. This explicit feat route does not add the spell to any ordinary class catalog. The chosen rank1spell retains its actual components/action/concentration and source-specific limits. Neither choice may be freely replaced after a rest. The Feywild description is preserved as flavor without establishing its geography, origins or cosmological relationships.

### Original-position authored review references

```json
[
  {
    "id": "MF-13-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/24"
  },
  {
    "id": "MF-13-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/25"
  }
]
```

## MF-14 — Greater Spell Focus

### Complete original object

```json
{
  "id": "greater_spell_focus",
  "name": "Greater Spell Focus",
  "description": "Your spells are harder to resist.",
  "prerequisite": "Spell Focus feat",
  "effect": "The DC for your spells increases by an additional +1.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"No exact Spell Focus feat occurs among335 source names. Identify a real prerequisite dependency or propose an explicitly NEW bounded completion; do not alias Mystic Focus, spellPenetration or school-focus feats by similar names. Define additional+1 DC scope and stacking without assuming a missing earlier+1."
```

### Preserved original source direction (historical)

```json
{
  "featId": "greater_spell_focus",
  "name": "Greater Spell Focus",
  "cohort": "magic_core",
  "questionId": "MF-14",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/13",
  "originalQuestion": "No exact Spell Focus feat occurs among335 source names. Identify a real prerequisite dependency or propose an explicitly NEW bounded completion; do not alias Mystic Focus, spellPenetration or school-focus feats by similar names. Define additional+1 DC scope and stacking without assuming a missing earlier+1.",
  "originalSourceObject": {
    "id": "greater_spell_focus",
    "name": "Greater Spell Focus",
    "description": "Your spells are harder to resist.",
    "prerequisite": "Spell Focus feat",
    "effect": "The DC for your spells increases by an additional +1.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "80e2e81da20cb55477f48846476e85b8a50a5d01766b29dd0c7fdfe009021f55",
  "submittedProcedure": "The source’s exact “Spell Focus feat” prerequisite is missing from the335-entry registry. Preserve that fact; Mystic Focus, Spell Penetration and school-focus feats are not aliases. NEW proposed complete dependency is the separately defined supplementary Spell Focus feat in this manuscript: one chosen actual spell school, personal spellcasting prerequisite, and+1to saving-throw DCs of your spells cast through that school. It costs its own legal feat selection and has no implicit free acquisition. If GPT rejects or replaces this proposed additional feat, Greater Spell Focus remains dependent on an actual accepted resolution; a similar name alone cannot qualify.\n\nAfter genuinely acquiring that proposed base feat, Greater Spell Focus adds a further+1to the same chosen school’s actual spell saving-throw DCs, for+2total from this pair. NEW “additional” extends the base’s school scope rather than secretly granting the missing first+1to all spells. The bonuses apply to actual initial and later spell saves using that cast’s snapshotted DC, not spell attack rolls, concentration saves you make, a class-technique DC or a flat printed independent itemDC. Distinct source DC modifiers combine only as their actual families permit. Neither feat is repeatable and the school cannot be freely retargeted. The supplementary record is not inserted into the source335or a public operational manifest by this proposal.",
  "submittedNewChoices": "Explicit NEW separate prerequisite feat, own selection cost and one-school scope; no false alias or phantom original record.",
  "submittedWorkedCases": [
    "A caster chooses the proposed Spell Focus(Evocation) with one legal selection and Greater Spell Focus with another. Its qualifying baseDC15Evocation spell uses17before other legitimate modifiers.",
    "Owning Enchantment Focus alone does not satisfy the literal prerequisite or add an assumed+1DC. Its separate disadvantage effect remains its own proposal."
  ],
  "decision": "Retain the MF-14 complete grant/procedure and boundaries. Explicit NEW separate prerequisite feat, own selection cost and one-school scope; no false alias or phantom original record. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "The source’s exact “Spell Focus feat” prerequisite is missing from the335-entry registry. Preserve that fact; Mystic Focus, Spell Penetration and school-focus feats are not aliases. NEW proposed complete dependency is the separately defined supplementary Spell Focus feat in this manuscript: one chosen actual spell school, personal spellcasting prerequisite, and+1to saving-throw DCs of your spells cast through that school. It costs its own legal feat selection and has no implicit free acquisition. If GPT rejects or replaces this proposed additional feat, Greater Spell Focus remains dependent on an actual accepted resolution; a similar name alone cannot qualify.\n\nAfter genuinely acquiring that proposed base feat, Greater Spell Focus adds a further+1to the same chosen school’s actual spell saving-throw DCs, for+2total from this pair. NEW “additional” extends the base’s school scope rather than secretly granting the missing first+1to all spells. The bonuses apply to actual initial and later spell saves using that cast’s snapshotted DC, not spell attack rolls, concentration saves you make, a class-technique DC or a flat printed independent itemDC. Distinct source DC modifiers combine only as their actual families permit. Neither feat is repeatable and the school cannot be freely retargeted. The supplementary record is not inserted into the source335or a public operational manifest by this proposal.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A caster chooses the proposed Spell Focus(Evocation) with one legal selection and Greater Spell Focus with another. Its qualifying baseDC15Evocation spell uses17before other legitimate modifiers.",
    "Owning Enchantment Focus alone does not satisfy the literal prerequisite or add an assumed+1DC. Its separate disadvantage effect remains its own proposal."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

The source’s exact “Spell Focus feat” prerequisite is missing from the335-entry registry. Preserve that fact; Mystic Focus, Spell Penetration and school-focus feats are not aliases. NEW proposed complete dependency is the separately defined supplementary Spell Focus feat in this manuscript: one chosen actual spell school, personal spellcasting prerequisite, and+1to saving-throw DCs of your spells cast through that school. It costs its own legal feat selection and has no implicit free acquisition. If GPT rejects or replaces this proposed additional feat, Greater Spell Focus remains dependent on an actual accepted resolution; a similar name alone cannot qualify.

After genuinely acquiring that proposed base feat, Greater Spell Focus adds a further+1to the same chosen school’s actual spell saving-throw DCs, for+2total from this pair. NEW “additional” extends the base’s school scope rather than secretly granting the missing first+1to all spells. The bonuses apply to actual initial and later spell saves using that cast’s snapshotted DC, not spell attack rolls, concentration saves you make, a class-technique DC or a flat printed independent itemDC. Distinct source DC modifiers combine only as their actual families permit. Neither feat is repeatable and the school cannot be freely retargeted. The supplementary record is not inserted into the source335or a public operational manifest by this proposal.

### Original-position authored review references

```json
[
  {
    "id": "MF-14-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/26"
  },
  {
    "id": "MF-14-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/27"
  }
]
```

## MF-15 — Heighten Spell

### Complete original object

```json
{
  "id": "heighten_spell",
  "name": "Heighten Spell",
  "description": "You can cast spells at higher levels.",
  "prerequisite": "Ability to cast 3rd level spells",
  "effect": "You can expend a ranked-spell recovery one level higher to increase the spell's DC by +1.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Map expending one-level-higher ranked recovery to actual rank/RP pricing, known spell access and maximum legal rank. Define declaration/payment, duration of+1 DC, multi-save spells and stacking; do not infer general upcasting, extra damage or a spell-slot pool."
```

### Preserved original source direction (historical)

```json
{
  "featId": "heighten_spell",
  "name": "Heighten Spell",
  "cohort": "magic_core",
  "questionId": "MF-15",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/14",
  "originalQuestion": "Map expending one-level-higher ranked recovery to actual rank/RP pricing, known spell access and maximum legal rank. Define declaration/payment, duration of+1 DC, multi-save spells and stacking; do not infer general upcasting, extra damage or a spell-slot pool.",
  "originalSourceObject": {
    "id": "heighten_spell",
    "name": "Heighten Spell",
    "description": "You can cast spells at higher levels.",
    "prerequisite": "Ability to cast 3rd level spells",
    "effect": "You can expend a ranked-spell recovery one level higher to increase the spell's DC by +1.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "c8ba5b416aa49eb9dc387059dc50f20bbf26034c26d0530f7bf9aa05d27da494",
  "submittedProcedure": "Require an actual acquired ability to cast rank3spells. NEW apply only when casting through an existing actual RP-priced source that already permits both the spell’s real rankr and the next rankr+1; rmust be1–8. Before legal cast commitment, declare Heighten and substitute the next rank’s Core baseRPprice for this cast’s ordinary rank price:0/2/3/5/7/10/13/17/21/26 remains the price table. Then apply the source’s actual additional costs, legal discounts and ordinary Dissonance surcharge in their normal order. No negative cost or cheaper-than-source exception is added. Pay once at cast start, with no refund on interruption or failure.\n\nThat cast’s actual saving-throw DC increases by+1for all initial/repeated saves that use its snapshotted spellDC for its lifetime. The original spell rank,school,repertoire/preparation,casting time,effect,dice,Counterspell/Dispel rank,baseDissonance and cadence remain unchanged. Paying the next rank price is not a general upcast, extra spell-known grant or slot. Heighten is applied once to a cast, never repeatedly for multiple+1s. A charge-only feat/ancestry source has no normal rankRPprice to substitute and cannot use this route by voluntarily inventing an RPpayment; a separately eligible class cast can. Rank9and cantrips are ineligible under this NEW bounded interpretation.",
  "submittedNewChoices": "One higher Core baseprice with actual next-rank source access; original rank/effect retained; no cantrip/rank9/charge-only use.",
  "submittedWorkedCases": [
    "A class caster legally accessing rank4casts a rank3spell with Heighten. Before other actual adjustments its baseprice is7rather than5, itsDCgains1, and its generating rank remains3for Dispel Magic.",
    "A character with only a one-charge rank3feat spell and an unrelated RPpool cannot pay a made-up higher recovery to Heighten that charge route. The exact ordinary class route must independently exist."
  ],
  "decision": "Retain the MF-15 complete grant/procedure and boundaries. One higher Core baseprice with actual next-rank source access; original rank/effect retained; no cantrip/rank9/charge-only use. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require an actual acquired ability to cast rank3spells. NEW apply only when casting through an existing actual RP-priced source that already permits both the spell’s real rankr and the next rankr+1; rmust be1–8. Before legal cast commitment, declare Heighten and substitute the next rank’s Core baseRPprice for this cast’s ordinary rank price:0/2/3/5/7/10/13/17/21/26 remains the price table. Then apply the source’s actual additional costs, legal discounts and ordinary Dissonance surcharge in their normal order. No negative cost or cheaper-than-source exception is added. Pay once at cast start, with no refund on interruption or failure.\n\nThat cast’s actual saving-throw DC increases by+1for all initial/repeated saves that use its snapshotted spellDC for its lifetime. The original spell rank,school,repertoire/preparation,casting time,effect,dice,Counterspell/Dispel rank,baseDissonance and cadence remain unchanged. Paying the next rank price is not a general upcast, extra spell-known grant or slot. Heighten is applied once to a cast, never repeatedly for multiple+1s. A charge-only feat/ancestry source has no normal rankRPprice to substitute and cannot use this route by voluntarily inventing an RPpayment; a separately eligible class cast can. Rank9and cantrips are ineligible under this NEW bounded interpretation.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A class caster legally accessing rank4casts a rank3spell with Heighten. Before other actual adjustments its baseprice is7rather than5, itsDCgains1, and its generating rank remains3for Dispel Magic.",
    "A character with only a one-charge rank3feat spell and an unrelated RPpool cannot pay a made-up higher recovery to Heighten that charge route. The exact ordinary class route must independently exist."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require an actual acquired ability to cast rank3spells. NEW apply only when casting through an existing actual RP-priced source that already permits both the spell’s real rankr and the next rankr+1; rmust be1–8. Before legal cast commitment, declare Heighten and substitute the next rank’s Core baseRPprice for this cast’s ordinary rank price:0/2/3/5/7/10/13/17/21/26 remains the price table. Then apply the source’s actual additional costs, legal discounts and ordinary Dissonance surcharge in their normal order. No negative cost or cheaper-than-source exception is added. Pay once at cast start, with no refund on interruption or failure.

That cast’s actual saving-throw DC increases by+1for all initial/repeated saves that use its snapshotted spellDC for its lifetime. The original spell rank,school,repertoire/preparation,casting time,effect,dice,Counterspell/Dispel rank,baseDissonance and cadence remain unchanged. Paying the next rank price is not a general upcast, extra spell-known grant or slot. Heighten is applied once to a cast, never repeatedly for multiple+1s. A charge-only feat/ancestry source has no normal rankRPprice to substitute and cannot use this route by voluntarily inventing an RPpayment; a separately eligible class cast can. Rank9and cantrips are ineligible under this NEW bounded interpretation.

### Original-position authored review references

```json
[
  {
    "id": "MF-15-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/28"
  },
  {
    "id": "MF-15-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/29"
  }
]
```

## MF-16 — Magic Initiate (Bard)

### Complete original object

```json
{
  "id": "magic_initiate_bard",
  "name": "Magic Initiate (Bard)",
  "description": "You have learned some bard magic.",
  "prerequisite": "None",
  "effect": "You learn two cantrips and one 1st-level spell from the bard spell list. You can cast the spell once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve two bard-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. Blocked spell cards remain dependencies and this feat grants no class-level advancement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "magic_initiate_bard",
  "name": "Magic Initiate (Bard)",
  "cohort": "magic_core",
  "questionId": "MF-16",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/15",
  "originalQuestion": "Preserve two bard-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. Blocked spell cards remain dependencies and this feat grants no class-level advancement.",
  "originalSourceObject": {
    "id": "magic_initiate_bard",
    "name": "Magic Initiate (Bard)",
    "description": "You have learned some bard magic.",
    "prerequisite": "None",
    "effect": "You learn two cantrips and one 1st-level spell from the bard spell list. You can cast the spell once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "00ab2ea8b02c4860c48d72eb911727c0831851b7aeb3a11f2d340ae71efd1860",
  "submittedProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Bard classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "submittedNewChoices": "CHA feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy",
  "submittedWorkedCases": [
    "A character with no Bard class level spends a genuine feat selection on this route and makes the three legal choices. It uses CHA and total PB for those spell attacks/saves but gains no Bard class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "decision": "Retain the MF-16 complete grant/procedure and boundaries. CHA feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Bard classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A character with no Bard class level spends a genuine feat selection on this route and makes the three legal choices. It uses CHA and total PB for those spell attacks/saves but gains no Bard class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Bard classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.

NEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.

### Original-position authored review references

```json
[
  {
    "id": "MF-16-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/30"
  },
  {
    "id": "MF-16-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/31"
  }
]
```

## MF-17 — Magic Initiate (Cleric)

### Complete original object

```json
{
  "id": "magic_initiate_cleric",
  "name": "Magic Initiate (Cleric)",
  "description": "You have learned some cleric magic.",
  "prerequisite": "None",
  "effect": "You learn two cantrips and one 1st-level spell from the cleric spell list. You can cast the spell once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve two cleric-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. Blocked spell cards remain dependencies and this feat grants no class-level advancement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "magic_initiate_cleric",
  "name": "Magic Initiate (Cleric)",
  "cohort": "magic_core",
  "questionId": "MF-17",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/16",
  "originalQuestion": "Preserve two cleric-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. Blocked spell cards remain dependencies and this feat grants no class-level advancement.",
  "originalSourceObject": {
    "id": "magic_initiate_cleric",
    "name": "Magic Initiate (Cleric)",
    "description": "You have learned some cleric magic.",
    "prerequisite": "None",
    "effect": "You learn two cantrips and one 1st-level spell from the cleric spell list. You can cast the spell once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "6de5d39dbf112115be44837e9864d5209cd1e5aa4c3efa7c625c2fbae8c0dff7",
  "submittedProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Cleric classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use WIS as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "submittedNewChoices": "WIS feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy",
  "submittedWorkedCases": [
    "A character with no Cleric class level spends a genuine feat selection on this route and makes the three legal choices. It uses WIS and total PB for those spell attacks/saves but gains no Cleric class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "decision": "Retain the MF-17 complete grant/procedure and boundaries. WIS feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Cleric classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use WIS as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A character with no Cleric class level spends a genuine feat selection on this route and makes the three legal choices. It uses WIS and total PB for those spell attacks/saves but gains no Cleric class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Cleric classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use WIS as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.

NEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.

### Original-position authored review references

```json
[
  {
    "id": "MF-17-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/32"
  },
  {
    "id": "MF-17-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/33"
  }
]
```

## MF-18 — Magic Initiate (Druid)

### Complete original object

```json
{
  "id": "magic_initiate_druid",
  "name": "Magic Initiate (Druid)",
  "description": "You have learned some druid magic.",
  "prerequisite": "None",
  "effect": "You learn two cantrips and one 1st-level spell from the druid spell list. You can cast the spell once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve two druid-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. Blocked spell cards remain dependencies and this feat grants no class-level advancement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "magic_initiate_druid",
  "name": "Magic Initiate (Druid)",
  "cohort": "magic_core",
  "questionId": "MF-18",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/17",
  "originalQuestion": "Preserve two druid-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. Blocked spell cards remain dependencies and this feat grants no class-level advancement.",
  "originalSourceObject": {
    "id": "magic_initiate_druid",
    "name": "Magic Initiate (Druid)",
    "description": "You have learned some druid magic.",
    "prerequisite": "None",
    "effect": "You learn two cantrips and one 1st-level spell from the druid spell list. You can cast the spell once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "98363060816f8c949299b8b446ca36d7a0e96bc7372e9efff7082a72b88cbda8",
  "submittedProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Druid classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use WIS as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "submittedNewChoices": "WIS feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy",
  "submittedWorkedCases": [
    "A character with no Druid class level spends a genuine feat selection on this route and makes the three legal choices. It uses WIS and total PB for those spell attacks/saves but gains no Druid class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "decision": "Retain the MF-18 complete grant/procedure and boundaries. WIS feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Druid classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use WIS as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A character with no Druid class level spends a genuine feat selection on this route and makes the three legal choices. It uses WIS and total PB for those spell attacks/saves but gains no Druid class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Druid classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use WIS as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.

NEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.

### Original-position authored review references

```json
[
  {
    "id": "MF-18-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/34"
  },
  {
    "id": "MF-18-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/35"
  }
]
```

## MF-19 — Magic Initiate (Sorcerer)

### Complete original object

```json
{
  "id": "magic_initiate_sorcerer",
  "name": "Magic Initiate (Sorcerer)",
  "description": "You have learned some sorcerer magic.",
  "prerequisite": "None",
  "effect": "You learn two cantrips and one 1st-level spell from the sorcerer spell list. You can cast the spell once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve two sorcerer-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. No Sorcerer/Warlock class exists in the17-class foundation or supplied spell-progression map; do not silently alias this list to Mage/Wizard or import external rules. Blocked spell cards remain dependencies and this feat grants no class-level advancement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "magic_initiate_sorcerer",
  "name": "Magic Initiate (Sorcerer)",
  "cohort": "magic_core",
  "questionId": "MF-19",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/18",
  "originalQuestion": "Preserve two sorcerer-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. No Sorcerer/Warlock class exists in the17-class foundation or supplied spell-progression map; do not silently alias this list to Mage/Wizard or import external rules. Blocked spell cards remain dependencies and this feat grants no class-level advancement.",
  "originalSourceObject": {
    "id": "magic_initiate_sorcerer",
    "name": "Magic Initiate (Sorcerer)",
    "description": "You have learned some sorcerer magic.",
    "prerequisite": "None",
    "effect": "You learn two cantrips and one 1st-level spell from the sorcerer spell list. You can cast the spell once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "f8dd5cb594d0078f932f8590a941444b1c2a95c34b1e18ebc5deb39fb1f19a13",
  "submittedProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. No current Sorcerer class/list exists. NEW explicit proposal: use only the separately enumerated six-cantrip/six-rank1 Sorcerer feat curriculum below, whose individual payloads and chosen placements come from exact current source rows. This is a new limited grant list, not a renamed class, a claim about historical canon or an import from another game. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "submittedNewChoices": "CHA feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy; entirely NEW finite legacy-name curriculum",
  "submittedWorkedCases": [
    "A character with no Sorcerer class level spends a genuine feat selection on this route and makes the three legal choices. It uses CHA and total PB for those spell attacks/saves but gains no Sorcerer class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "decision": "Retain the MF-19 complete grant/procedure and boundaries. CHA feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy; entirely NEW finite legacy-name curriculum Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. No current Sorcerer class/list exists. NEW explicit proposal: use only the separately enumerated six-cantrip/six-rank1 Sorcerer feat curriculum below, whose individual payloads and chosen placements come from exact current source rows. This is a new limited grant list, not a renamed class, a claim about historical canon or an import from another game. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A character with no Sorcerer class level spends a genuine feat selection on this route and makes the three legal choices. It uses CHA and total PB for those spell attacks/saves but gains no Sorcerer class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. No current Sorcerer class/list exists. NEW explicit proposal: use only the separately enumerated six-cantrip/six-rank1 Sorcerer feat curriculum below, whose individual payloads and chosen placements come from exact current source rows. This is a new limited grant list, not a renamed class, a claim about historical canon or an import from another game. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.

NEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.

### Original-position authored review references

```json
[
  {
    "id": "MF-19-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/36"
  },
  {
    "id": "MF-19-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/37"
  }
]
```

## MF-20 — Magic Initiate (Warlock)

### Complete original object

```json
{
  "id": "magic_initiate_warlock",
  "name": "Magic Initiate (Warlock)",
  "description": "You have learned some warlock magic.",
  "prerequisite": "None",
  "effect": "You learn two cantrips and one 1st-level spell from the warlock spell list. You can cast the spell once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve two warlock-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. No Sorcerer/Warlock class exists in the17-class foundation or supplied spell-progression map; do not silently alias this list to Mage/Wizard or import external rules. Blocked spell cards remain dependencies and this feat grants no class-level advancement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "magic_initiate_warlock",
  "name": "Magic Initiate (Warlock)",
  "cohort": "magic_core",
  "questionId": "MF-20",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/19",
  "originalQuestion": "Preserve two warlock-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. No Sorcerer/Warlock class exists in the17-class foundation or supplied spell-progression map; do not silently alias this list to Mage/Wizard or import external rules. Blocked spell cards remain dependencies and this feat grants no class-level advancement.",
  "originalSourceObject": {
    "id": "magic_initiate_warlock",
    "name": "Magic Initiate (Warlock)",
    "description": "You have learned some warlock magic.",
    "prerequisite": "None",
    "effect": "You learn two cantrips and one 1st-level spell from the warlock spell list. You can cast the spell once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "04284ca0bd0c14e70eb03b7a17519e2b230e2c6c28ade97f76f24d913da5c916",
  "submittedProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. No current Warlock class/list exists. NEW explicit proposal: use only the separately enumerated six-cantrip/six-rank1 Warlock feat curriculum below, whose individual payloads and chosen placements come from exact current source rows. This is a new limited grant list, not a renamed class, a claim about historical canon or an import from another game. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "submittedNewChoices": "CHA feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy; entirely NEW finite legacy-name curriculum",
  "submittedWorkedCases": [
    "A character with no Warlock class level spends a genuine feat selection on this route and makes the three legal choices. It uses CHA and total PB for those spell attacks/saves but gains no Warlock class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "decision": "Retain the MF-20 complete grant/procedure and boundaries. CHA feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy; entirely NEW finite legacy-name curriculum Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. No current Warlock class/list exists. NEW explicit proposal: use only the separately enumerated six-cantrip/six-rank1 Warlock feat curriculum below, whose individual payloads and chosen placements come from exact current source rows. This is a new limited grant list, not a renamed class, a claim about historical canon or an import from another game. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A character with no Warlock class level spends a genuine feat selection on this route and makes the three legal choices. It uses CHA and total PB for those spell attacks/saves but gains no Warlock class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. No current Warlock class/list exists. NEW explicit proposal: use only the separately enumerated six-cantrip/six-rank1 Warlock feat curriculum below, whose individual payloads and chosen placements come from exact current source rows. This is a new limited grant list, not a renamed class, a claim about historical canon or an import from another game. Choices are permanent and grant only their chosen rank/mode. Use CHA as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.

NEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.

### Original-position authored review references

```json
[
  {
    "id": "MF-20-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/38"
  },
  {
    "id": "MF-20-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/39"
  }
]
```

## MF-21 — Magic Initiate (Wizard)

### Complete original object

```json
{
  "id": "magic_initiate_wizard",
  "name": "Magic Initiate (Wizard)",
  "description": "You have learned some wizard magic.",
  "prerequisite": "None",
  "effect": "You learn two cantrips and one 1st-level spell from the wizard spell list. You can cast the spell once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve two wizard-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. Blocked spell cards remain dependencies and this feat grants no class-level advancement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "magic_initiate_wizard",
  "name": "Magic Initiate (Wizard)",
  "cohort": "magic_core",
  "questionId": "MF-21",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/20",
  "originalQuestion": "Preserve two wizard-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. Blocked spell cards remain dependencies and this feat grants no class-level advancement.",
  "originalSourceObject": {
    "id": "magic_initiate_wizard",
    "name": "Magic Initiate (Wizard)",
    "description": "You have learned some wizard magic.",
    "prerequisite": "None",
    "effect": "You learn two cantrips and one 1st-level spell from the wizard spell list. You can cast the spell once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "8589faabe9c7a1cbdd68fa0bb50180f74580ceb2c7e5d352668716d41b75862b",
  "submittedProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Wizard classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use INT as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "submittedNewChoices": "INT feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy",
  "submittedWorkedCases": [
    "A character with no Wizard class level spends a genuine feat selection on this route and makes the three legal choices. It uses INT and total PB for those spell attacks/saves but gains no Wizard class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "decision": "Retain the MF-21 complete grant/procedure and boundaries. INT feat casting ability; explicit named choice-pool/charge route; shared Magic Initiate curriculum-family duplicate policy Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Wizard classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use INT as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.\n\nNEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A character with no Wizard class level spends a genuine feat selection on this route and makes the three legal choices. It uses INT and total PB for those spell attacks/saves but gains no Wizard class card, RPpool or automatic Extra Attack.",
    "The ranked charge is spent at legal cast commitment even if countered. A chosen cantrip that independently costs1RP still needs a real payable RPpool; neither the charge route nor cantrip label manufactures one."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose two distinct cantrip identities and one rank1spell from this feat’s actual named choice pool. The preserved Wizard classAccess rows supply the actual rank0and rank1choice lists below; keep that row’s school/mode even when another class gives the same identity a different placement. Choices are permanent and grant only their chosen rank/mode. Use INT as the feat casting ability. The two cantrips are repeatable with their actual card actions and cadence; the one ranked spell has one charge per beneficial Long Rest. Apply the full proposed feat casting route: actual components and independent costs remain, no normal rankRPprice, no new RPpool/class levels/preparation, shared Dissonance/Refrain and rank1strain block, and no generic scaling. Current reviewed payload status is separate from grant eligibility; an unfinished chosen payload cannot be activated. A qualifying cantrip with its own character-wide Long-Rest limit retains that limit despite the word cantrip.

NEW duplicate policy across the general Magic Initiate record and the six named records: one selected curriculum label per character in this family; the general feat can supply that same named grant but cannot be taken alongside its named version to double the same curriculum. Distinct curricula are separate feat selections and may coexist; they grant no multiclass level. A repeated spell name can have distinct source entitlements, but its own genuine character-wide caps and one shared same-name strain history remain. Record duplicates rather than granting replacement spells automatically. This family decision must be confirmed alongside GC’s general Magic Initiate source. A separate ordinary class may cast a feat-learned identity only after that class independently meets its actual learning/preparation/access requirements; the feat alone does not make it a free known spell on every paid route.

### Original-position authored review references

```json
[
  {
    "id": "MF-21-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/40"
  },
  {
    "id": "MF-21-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/41"
  }
]
```

## MF-22 — Metamagic Adept

### Complete original object

```json
{
  "id": "metamagicAdept",
  "name": "Metamagic Adept",
  "description": "You have learned to modify your spells in subtle ways.",
  "prerequisite": "Spellcasting ability, Level 4",
  "effect": "Learn 2 metamagic options, gain 2 sorcery points",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve two selected metamagic options and two sorcery points, but neither a point-to-RP exchange nor an imported external option list is authorized. Compare the complete provisional Mage Metaspell Access card; explicitly resolve feat option identities, costs, recovery, timing and combining modes. A matching metamagic tag does not grant class acquisition or convert one-per-rest uses into points."
```

### Preserved original source direction (historical)

```json
{
  "featId": "metamagicAdept",
  "name": "Metamagic Adept",
  "cohort": "magic_core",
  "questionId": "MF-22",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/21",
  "originalQuestion": "Preserve two selected metamagic options and two sorcery points, but neither a point-to-RP exchange nor an imported external option list is authorized. Compare the complete provisional Mage Metaspell Access card; explicitly resolve feat option identities, costs, recovery, timing and combining modes. A matching metamagic tag does not grant class acquisition or convert one-per-rest uses into points.",
  "originalSourceObject": {
    "id": "metamagicAdept",
    "name": "Metamagic Adept",
    "description": "You have learned to modify your spells in subtle ways.",
    "prerequisite": "Spellcasting ability, Level 4",
    "effect": "Learn 2 metamagic options, gain 2 sorcery points",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "6789eefb5394fffc5e00aeb163e3ca3428ba6332670027c2c426648730fcf615",
  "submittedProcedure": "Keep personal spellcasting and total character level4. NEW grant a separate pool of two feat sorcery points, maximum2, initially full and restored to2only by a beneficial Long Rest. There is no RP/RC/HP/charge exchange, class-resource conversion, overcap or refill from ordinary spell refunds. At acquisition permanently choose two distinct modes from the finite three-mode menu below, based explicitly on the actual Mage Metaspell Access card; this does not acquire that Mage card or its Long-Rest use.\n\nReach: spend1point when committing a personal spell cast to add30feet to its finite positive numeric casting range. Self,Touch,unlimited and a separate effect/command radius do not gain range. Widen: spend1point at commitment to add5feet to one circular/spherical area radius or one cone length of that actual spell; choose the one eligible dimension in advance, not all independent areas/parameters. It does not create an area on a single-target spell. Sculpt: spend1point at commitment to choose up to max(1,actual casting ability modifier) eligible creatures in that spell’s initial area; they automatically succeed on its initial save and take no damage if that success would normally halve damage. Their later saves/ticks and nondamage successful-save consequences follow the original spell; there is no permanent friendly-fire immunity.\n\nNEW one metamagic mode total per cast across this feat and Mage Metaspell Access; declare which actual source pays. You cannot use two points for two modes or duplicate a class mode on the same cast. Other separately applicable feats keep their exact scopes. Spell Sniper doubles the printed numeric range first, then Reach adds30; it does not double Reach’s30. The chosen mode adds no spell rank, RPdiscount, Action, concentration slot or second cast. Commit the point with the legal spell; a later miss, save, counter or interruption refunds neither. Illegal mode/target declarations spend nothing. The spell still needs all its own resources, components and access.",
  "submittedNewChoices": "2-point LRpool; two permanent choices from actual three-mode comparison;1point/cast and one mode across class/feat; precise timing/range order.",
  "submittedWorkedCases": [
    "A caster with Reach and Sculpt spends1point to extend a60-foot ranged spell to90feet. If Spell Sniper legally applies too, range is150feet:120from doubled printed range plus30.",
    "After spending its second point, the caster cannot convertRPinto more sorcery points. Having the Mage card’s own use does not allow an additional mode on a cast already modified through this feat."
  ],
  "decision": "Retain the MF-22 complete grant/procedure and boundaries. 2-point LRpool; two permanent choices from actual three-mode comparison;1point/cast and one mode across class/feat; precise timing/range order. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Keep personal spellcasting and total character level4. NEW grant a separate pool of two feat sorcery points, maximum2, initially full and restored to2only by a beneficial Long Rest. There is no RP/RC/HP/charge exchange, class-resource conversion, overcap or refill from ordinary spell refunds. At acquisition permanently choose two distinct modes from the finite three-mode menu below, based explicitly on the actual Mage Metaspell Access card; this does not acquire that Mage card or its Long-Rest use.\n\nReach: spend1point when committing a personal spell cast to add30feet to its finite positive numeric casting range. Self,Touch,unlimited and a separate effect/command radius do not gain range. Widen: spend1point at commitment to add5feet to one circular/spherical area radius or one cone length of that actual spell; choose the one eligible dimension in advance, not all independent areas/parameters. It does not create an area on a single-target spell. Sculpt: spend1point at commitment to choose up to max(1,actual casting ability modifier) eligible creatures in that spell’s initial area; they automatically succeed on its initial save and take no damage if that success would normally halve damage. Their later saves/ticks and nondamage successful-save consequences follow the original spell; there is no permanent friendly-fire immunity.\n\nNEW one metamagic mode total per cast across this feat and Mage Metaspell Access; declare which actual source pays. You cannot use two points for two modes or duplicate a class mode on the same cast. Other separately applicable feats keep their exact scopes. Spell Sniper doubles the printed numeric range first, then Reach adds30; it does not double Reach’s30. The chosen mode adds no spell rank, RPdiscount, Action, concentration slot or second cast. Commit the point with the legal spell; a later miss, save, counter or interruption refunds neither. Illegal mode/target declarations spend nothing. The spell still needs all its own resources, components and access.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A caster with Reach and Sculpt spends1point to extend a60-foot ranged spell to90feet. If Spell Sniper legally applies too, range is150feet:120from doubled printed range plus30.",
    "After spending its second point, the caster cannot convertRPinto more sorcery points. Having the Mage card’s own use does not allow an additional mode on a cast already modified through this feat."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Keep personal spellcasting and total character level4. NEW grant a separate pool of two feat sorcery points, maximum2, initially full and restored to2only by a beneficial Long Rest. There is no RP/RC/HP/charge exchange, class-resource conversion, overcap or refill from ordinary spell refunds. At acquisition permanently choose two distinct modes from the finite three-mode menu below, based explicitly on the actual Mage Metaspell Access card; this does not acquire that Mage card or its Long-Rest use.

Reach: spend1point when committing a personal spell cast to add30feet to its finite positive numeric casting range. Self,Touch,unlimited and a separate effect/command radius do not gain range. Widen: spend1point at commitment to add5feet to one circular/spherical area radius or one cone length of that actual spell; choose the one eligible dimension in advance, not all independent areas/parameters. It does not create an area on a single-target spell. Sculpt: spend1point at commitment to choose up to max(1,actual casting ability modifier) eligible creatures in that spell’s initial area; they automatically succeed on its initial save and take no damage if that success would normally halve damage. Their later saves/ticks and nondamage successful-save consequences follow the original spell; there is no permanent friendly-fire immunity.

NEW one metamagic mode total per cast across this feat and Mage Metaspell Access; declare which actual source pays. You cannot use two points for two modes or duplicate a class mode on the same cast. Other separately applicable feats keep their exact scopes. Spell Sniper doubles the printed numeric range first, then Reach adds30; it does not double Reach’s30. The chosen mode adds no spell rank, RPdiscount, Action, concentration slot or second cast. Commit the point with the legal spell; a later miss, save, counter or interruption refunds neither. Illegal mode/target declarations spend nothing. The spell still needs all its own resources, components and access.

### Original-position authored review references

```json
[
  {
    "id": "MF-22-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/42"
  },
  {
    "id": "MF-22-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/43"
  }
]
```

## MF-23 — Planar Binding

### Complete original object

```json
{
  "id": "planar_binding",
  "name": "Planar Binding",
  "description": "You can bind extraplanar creatures to your service.",
  "prerequisite": "Charisma 15+, ability to cast 5th level spells",
  "effect": "You can cast planar binding once per long rest without expending a ranked-spell recovery.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Resolve Charisma15 and rank5 casting access, actual feat casting route/ability, once-per-Long-Rest ledger and waived recovery versus components and concentration. The ordinary Planar Binding card remains blocked. Do not invent creature origins, planes, souls or binding ontology; record deferred dependencies separately from the mechanical grant."
```

### Preserved original source direction (historical)

```json
{
  "featId": "planar_binding",
  "name": "Planar Binding",
  "cohort": "magic_core",
  "questionId": "MF-23",
  "disposition": "DEFER_PAYLOAD_KEEP_FINITE_GRANT_WRAPPER",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/22",
  "originalQuestion": "Resolve Charisma15 and rank5 casting access, actual feat casting route/ability, once-per-Long-Rest ledger and waived recovery versus components and concentration. The ordinary Planar Binding card remains blocked. Do not invent creature origins, planes, souls or binding ontology; record deferred dependencies separately from the mechanical grant.",
  "originalSourceObject": {
    "id": "planar_binding",
    "name": "Planar Binding",
    "description": "You can bind extraplanar creatures to your service.",
    "prerequisite": "Charisma 15+, ability to cast 5th level spells",
    "effect": "You can cast planar binding once per long rest without expending a ranked-spell recovery.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "3feefd2c70a7c9db737dc744f4e64367d38f0dc575a0906f9cbe3edcc87931da",
  "submittedProcedure": "Retain CHA15and actual acquired rank5spellcasting ability. NEW mechanical grant interface only: one feat-scoped Planar Binding entitlement at the actual named rank5, using CHA, with one charge per beneficial Long Rest. It waives the normal rankRPprice only, retaining any actual nonprice cost, components, concentration and all access/target conditions defined by the eventual completed spell. It grants no broader class repertoire or rank access. A future legal cast would spend the charge at commitment, add base1Dissonance plus actual Refrain and obey the actual Limit+6block; interruption would not refund costs.\n\nThe named ordinary payload remains deferred and has no legal activation in this proposal. No creature-origin taxonomy, planar destination, soul rule, pact, binding ontology, duration of service or automatic consent is authored here. Record only the acquired prerequisite/grant interface and its explicit pending dependency, preserving the complete original spell source separately. A creature described as extraplanar is not made an operational target by guessing what the missing spell would do. This is not a complete usable feat and must remain visibly separated from the29fully proposed procedures until after the owner-ordered post-push work.",
  "submittedNewChoices": "CHA/rank5finite grant wrapper; unresolved payload is retained rather than invented.",
  "submittedWorkedCases": [
    "A CHA15caster with genuine rank5access can satisfy this proposal’s acquisition gate, but cannot compel a creature through an undefined binding payload.",
    "An ordinary rank5slot metaphor creates no separate recovery pool. If the later completed spell requires a real expensive component, the feat’s waived normalRPprice would not waive that component."
  ],
  "decision": "Retain the MF-23 complete grant/procedure and boundaries. CHA/rank5finite grant wrapper; unresolved payload is retained rather than invented. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Retain CHA15and actual acquired rank5spellcasting ability. NEW mechanical grant interface only: one feat-scoped Planar Binding entitlement at the actual named rank5, using CHA, with one charge per beneficial Long Rest. It waives the normal rankRPprice only, retaining any actual nonprice cost, components, concentration and all access/target conditions defined by the eventual completed spell. It grants no broader class repertoire or rank access. A future legal cast would spend the charge at commitment, add base1Dissonance plus actual Refrain and obey the actual Limit+6block; interruption would not refund costs.\n\nThe named ordinary payload remains deferred and has no legal activation in this proposal. No creature-origin taxonomy, planar destination, soul rule, pact, binding ontology, duration of service or automatic consent is authored here. Record only the acquired prerequisite/grant interface and its explicit pending dependency, preserving the complete original spell source separately. A creature described as extraplanar is not made an operational target by guessing what the missing spell would do. This is not a complete usable feat and must remain visibly separated from the29fully proposed procedures until after the owner-ordered post-push work.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A CHA15caster with genuine rank5access can satisfy this proposal’s acquisition gate, but cannot compel a creature through an undefined binding payload.",
    "An ordinary rank5slot metaphor creates no separate recovery pool. If the later completed spell requires a real expensive component, the feat’s waived normalRPprice would not waive that component."
  ],
  "payloadOperational": null,
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Retain CHA15and actual acquired rank5spellcasting ability. NEW mechanical grant interface only: one feat-scoped Planar Binding entitlement at the actual named rank5, using CHA, with one charge per beneficial Long Rest. It waives the normal rankRPprice only, retaining any actual nonprice cost, components, concentration and all access/target conditions defined by the accepted ordinary spell, if separately authorized for this feat grant. It grants no broader class repertoire or rank access. A future legal cast would spend the charge at commitment, add base1Dissonance plus actual Refrain and obey the actual Limit+6block; interruption would not refund costs.

CURRENT DEPENDENCY STATUS: the ordinary Planar Binding spell has an accepted authored procedure in DD-AC5-EXACT-ACCEPTANCE-05. Its complete current card and source access are retained separately. That ordinary-spell acceptance does not itself activate this separate feat grant: this candidate retains payloadOperational=null and selectionEnabled=false under its original deferred-wrapper boundary. No cast, charge debit, target eligibility or service record is produced through this feat while that boundary remains. Retain the original feat source verdict and post-push dependency as historical/authorization evidence; exact parent review must expressly resolve the feat wrapper before any later integration. This status correction authors no planar taxonomy, native or soul origin, destination, consent rule, cosmology canon or new ordinary-spell procedure.

### Original-position authored review references

```json
[
  {
    "id": "MF-23-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/44"
  },
  {
    "id": "MF-23-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/45"
  }
]
```

## MF-24 — Ritual Caster

### Complete original object

```json
{
  "id": "ritual_caster",
  "name": "Ritual Caster",
  "description": "You have learned to cast spells as rituals.",
  "prerequisite": "Intelligence or Wisdom 13 or higher",
  "effect": "You can cast spells with the ritual tag without expending ranked-spell recoverys, but it takes 10 minutes longer.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Define eligible learned/recorded rituals, actual ritual tags, access/preparation/components, Intelligence-or-Wisdom13, base casting time plus10minutes and interruption/concentration. Bind no-recovery wording to RP precisely, preserving typo in source. Quick Ritualist/Ritual Channeler are pending counterparts, not approved multipliers or free formula access."
```

### Preserved original source direction (historical)

```json
{
  "featId": "ritual_caster",
  "name": "Ritual Caster",
  "cohort": "magic_core",
  "questionId": "MF-24",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/23",
  "originalQuestion": "Define eligible learned/recorded rituals, actual ritual tags, access/preparation/components, Intelligence-or-Wisdom13, base casting time plus10minutes and interruption/concentration. Bind no-recovery wording to RP precisely, preserving typo in source. Quick Ritualist/Ritual Channeler are pending counterparts, not approved multipliers or free formula access.",
  "originalSourceObject": {
    "id": "ritual_caster",
    "name": "Ritual Caster",
    "description": "You have learned to cast spells as rituals.",
    "prerequisite": "Intelligence or Wisdom 13 or higher",
    "effect": "You can cast spells with the ritual tag without expending ranked-spell recoverys, but it takes 10 minutes longer.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "a02b3002100ce2e7808e4d6e02bb133b55beed00bb56c6dea9473ed696b38893",
  "submittedProcedure": "Keep INT13orWIS13; choose one qualifying ability permanently as this feat’s casting ability. The current848ordinary-card scan finds no explicit Ritual tag in their preserved Core-source tag arrays; neither a familiar external spell name nor a class procedure called ritual proves such a tag. NEW proposed Ritual-tag overlay below explicitly supplies seven existing reviewed rank1payload placements: Detect Magic,Identify,Comprehend Languages,Alarm,Unseen Servant,Find Familiar andIllusory Script, each using its exact Wizard source placement solely to fix rank/school/effect provenance. This new tag is a separate candidate overlay and needs joint approval, including its effect on the actual Wizard Ritual Casting feature. It changes neither those spell effects nor their ordinary class membership.\n\nNEW feat learning route: with an actual complete legitimate formula/text or a willing qualified teacher who genuinely knows the exact ritual, spend8active hours per rank and10gp per rank of real practice/writing materials to record it in your actual usable ritual book. Rank0, if ever separately admitted, uses one rank for this learning cost. A suitable blank book, ink/tools, language access and actual instructor/facility costs remain real. Study uses completed15-minute phases under the language/research clock; it is spell learning/copying, not ordinary research for Diligent Researcher’s discount. There is no random completion roll, free formula, duplicate-learning benefit or tradeXP. The feat grants no free starting ritual or physical book. Its maximum recorded/cast ritual rank is min(9,floor((total character level+1)/2)); this explicit feat-only gate grants no class advancement. The present proposed tag set has only rank1entries, and future entries need their own exact review.\n\nTo cast a legitimately learned recorded ritual, use its actual book and all components, spend its ordinary casting time plus ten actual minutes of uninterrupted active casting, and meet its complete targets/action-trigger rules. This route cannot complete during an encounter; interruption ends the attempt with real time and committed consumables spent. NEW maintain concentration during the long casting procedure, ending incompatible prior concentration at commitment; at resolution continue only the resulting spell’s own concentration if any. Do not choose a Reaction-triggered spell and manufacture its trigger through slow preparation. Ordinary rankRPprice and price-only surcharge are0; an expressly printed consumedRPconversion or other independent cost still applies and needs an actual pool. No ordinary Dissonance generation or vent, no Refrain addition/reset or history alteration, and no resource recovery from merely completing the casting time; a spell’s explicitly bounded actual effect remains its own effect. This follows the intended ordinary ritual separation rather than creating an at-will strain reset. Actual Counterspell eligibility, one-attempt-per-pending-cast guards, components and range apply. Source-specific per-rest limits remain. Other pending ritual feats cannot reduce this time or multiply output until their own interactions are decided.",
  "submittedNewChoices": "NEW finite7-tag overlay and actual learning/book route; total-level rank cap; long-cast/strain/independent-cost contract.",
  "submittedWorkedCases": [
    "A level1character meetingINT13can study an actually available rank1ritual for8active hours with10gppractice materials and the actual book. It gains no automatic knowledge of all seven merely by selecting Ritual Caster.",
    "Casting the proposed ritual Find Familiar uses its real baseAction plus ten minutes, then the reviewed1-minute concentration familiar payload. The ritual does not make that familiar permanent, free of commands or immune to0HPdisappearance."
  ],
  "decision": "Retain the MF-24 complete grant/procedure and boundaries. NEW finite7-tag overlay and actual learning/book route; total-level rank cap; long-cast/strain/independent-cost contract. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Keep INT13orWIS13; choose one qualifying ability permanently as this feat’s casting ability. The current848ordinary-card scan finds no explicit Ritual tag in their preserved Core-source tag arrays; neither a familiar external spell name nor a class procedure called ritual proves such a tag. NEW proposed Ritual-tag overlay below explicitly supplies seven existing reviewed rank1payload placements: Detect Magic,Identify,Comprehend Languages,Alarm,Unseen Servant,Find Familiar andIllusory Script, each using its exact Wizard source placement solely to fix rank/school/effect provenance. This conference adopts these seven NEW tags in a separate feat/Wizard-ritual interface overlay, leaving all original spell objects and class acquisition/status labels unchanged. The existing Wizard Ritual Casting feature can use the tags only with its own actual level, known-book spell, preparation, component, time and encounter predicates. It changes neither those spell effects nor their ordinary class membership.\n\nNEW feat learning route: with an actual complete legitimate formula/text or a willing qualified teacher who genuinely knows the exact ritual, spend8active hours per rank and10gp per rank of real practice/writing materials to record it in your actual usable ritual book. Rank0, if ever separately admitted, uses one rank for this learning cost. A suitable blank book, ink/tools, language access and actual instructor/facility costs remain real. Study uses completed15-minute phases under the language/research clock; it is spell learning/copying, not ordinary research for Diligent Researcher’s discount. There is no random completion roll, free formula, duplicate-learning benefit or tradeXP. The feat grants no free starting ritual or physical book. Its maximum recorded/cast ritual rank is min(9,floor((total character level+1)/2)); this explicit feat-only gate grants no class advancement. The present proposed tag set has only rank1entries, and future entries need their own exact review.\n\nTo cast a legitimately learned recorded ritual, use its actual book and all components, spend its ordinary casting time plus ten actual minutes of uninterrupted active casting, and meet its complete targets/action-trigger rules. This route cannot complete during an encounter; interruption ends the attempt with real time and committed consumables spent. NEW maintain concentration during the long casting procedure, ending incompatible prior concentration at commitment; at resolution continue only the resulting spell’s own concentration if any. Do not choose a Reaction-triggered spell and manufacture its trigger through slow preparation. Ordinary rankRPprice and price-only surcharge are0; an expressly printed consumedRPconversion or other independent cost still applies and needs an actual pool. No ordinary Dissonance generation or vent, no Refrain addition/reset or history alteration, and no resource recovery from merely completing the casting time; a spell’s explicitly bounded actual effect remains its own effect. This follows the intended ordinary ritual separation rather than creating an at-will strain reset. Actual Counterspell eligibility, one-attempt-per-pending-cast guards, components and range apply. Source-specific per-rest limits remain. The adopted Quick Ritualist and Ritual Channeler rules may reduce actual ritual labor only as specified in this conference; neither changes output, eligibility or independent costs.\nKEEP the reviewed Wizard ritual boundary for this NEW feat-only ritual route: it cannot be used during an active encounter. Ritual execution changes neither ordinary Dissonance nor ordinary Refrain memory/counter and supplies no vent/reset. The actual ritual-tagged spell, book/learned record, components, additional effect costs and concentration remain required. The source’s separate eight-hour-per-rank learning and ten-gp-per-rank transcription procedure is not itself a ritual cast or generic research discount.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A level1character meetingINT13can study an actually available rank1ritual for8active hours with10gppractice materials and the actual book. It gains no automatic knowledge of all seven merely by selecting Ritual Caster.",
    "Casting the proposed ritual Find Familiar uses its real baseAction plus ten minutes, then the reviewed1-minute concentration familiar payload. The ritual does not make that familiar permanent, free of commands or immune to0HPdisappearance."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Keep INT13orWIS13; choose one qualifying ability permanently as this feat’s casting ability. The current848ordinary-card scan finds no explicit Ritual tag in their preserved Core-source tag arrays; neither a familiar external spell name nor a class procedure called ritual proves such a tag. NEW proposed Ritual-tag overlay below explicitly supplies seven existing reviewed rank1payload placements: Detect Magic,Identify,Comprehend Languages,Alarm,Unseen Servant,Find Familiar andIllusory Script, each using its exact Wizard source placement solely to fix rank/school/effect provenance. This conference adopts these seven NEW tags in a separate feat/Wizard-ritual interface overlay, leaving all original spell objects and class acquisition/status labels unchanged. The existing Wizard Ritual Casting feature can use the tags only with its own actual level, known-book spell, preparation, component, time and encounter predicates. It changes neither those spell effects nor their ordinary class membership.

NEW feat learning route: with an actual complete legitimate formula/text or a willing qualified teacher who genuinely knows the exact ritual, spend8active hours per rank and10gp per rank of real practice/writing materials to record it in your actual usable ritual book. Rank0, if ever separately admitted, uses one rank for this learning cost. A suitable blank book, ink/tools, language access and actual instructor/facility costs remain real. Study uses completed15-minute phases under the language/research clock; it is spell learning/copying, not ordinary research for Diligent Researcher’s discount. There is no random completion roll, free formula, duplicate-learning benefit or tradeXP. The feat grants no free starting ritual or physical book. Its maximum recorded/cast ritual rank is min(9,floor((total character level+1)/2)); this explicit feat-only gate grants no class advancement. The present proposed tag set has only rank1entries, and future entries need their own exact review.

To cast a legitimately learned recorded ritual, use its actual book and all components, spend its ordinary casting time plus ten actual minutes of uninterrupted active casting, and meet its complete targets/action-trigger rules. This route cannot complete during an encounter; interruption ends the attempt with real time and committed consumables spent. NEW maintain concentration during the long casting procedure, ending incompatible prior concentration at commitment; at resolution continue only the resulting spell’s own concentration if any. Do not choose a Reaction-triggered spell and manufacture its trigger through slow preparation. Ordinary rankRPprice and price-only surcharge are0; an expressly printed consumedRPconversion or other independent cost still applies and needs an actual pool. No ordinary Dissonance generation or vent, no Refrain addition/reset or history alteration, and no resource recovery from merely completing the casting time; a spell’s explicitly bounded actual effect remains its own effect. This follows the intended ordinary ritual separation rather than creating an at-will strain reset. Actual Counterspell eligibility, one-attempt-per-pending-cast guards, components and range apply. Source-specific per-rest limits remain. The adopted Quick Ritualist and Ritual Channeler rules may reduce actual ritual labor only as specified in this conference; neither changes output, eligibility or independent costs.
KEEP the reviewed Wizard ritual boundary for this NEW feat-only ritual route: it cannot be used during an active encounter. Ritual execution changes neither ordinary Dissonance nor ordinary Refrain memory/counter and supplies no vent/reset. The actual ritual-tagged spell, book/learned record, components, additional effect costs and concentration remain required. The source’s separate eight-hour-per-rank learning and ten-gp-per-rank transcription procedure is not itself a ritual cast or generic research discount.

FT84 source-follow-through selection (proposed; the following explicit interaction controls only this named composition):
FT84-Q01 / FT84-WRITTEN-RITUAL-01 — scoped selection for Ritual Caster learning and Spell Scribe.
INTERPRETATION SELECTED: the actual Ritual Caster written-learning route is an authorized spell-copying procedure when the learner personally uses an already complete, legitimately accessible written version of the exact eligible ritual, can actually use its language/notation, and records the learned ritual in the learner's real usable ritual book. The written source must supply the complete instruction, not merely a title, unfinished notes or text whose missing content must be taught. This predicate is about how the real work is done; the presence of a tutor does not disqualify otherwise genuine written copying, and writing lecture notes does not convert teacher-led learning into copying.
For that written-copy work, an actually acquired Spell Scribe halves the ordinary eight-active-hours-per-rank learning requirement; take the strongest eligible time factor once, then apply Spell Scribe's final whole-minute upward rounding. A current rank-one ritual therefore requires 240 active minutes. Retain every completed 15-minute learning phase and its governing interruption/final-remainder rule. No reading, comprehension, recording, rank, tag, consent, facility, tool or source requirement disappears. Diligent Researcher, Craftsman, Quick Ritualist and Ritual Channeler do not reduce this learning transaction. No new starting ritual or physical book, Wizard spellbook entitlement, ordinary scroll-production permission, check, trade XP or automatic class acquisition is granted.
Teacher-led learning without the qualifying complete written source remains 480 active minutes per rank. A later lawful switch to written-copy work can affect only actually remaining unworked learning at a completed phase boundary; log the old and new basis and retain all actual time/materials. Do not retroactively relabel completed teaching or an interrupted uncredited segment as discounted copying. Only one route credits each actual minute. Wizard Spell Scribing keeps its own legal-found-Wizard-spell/spellbook predicate and its own bill; merely being a Wizard or having the same physical book does not substitute its class route for this feat route. When two reductions genuinely cover the same procedure and material category, take the strongest once, not their product.
NEW LIMITED BILL COMPLETION: before claiming a material reduction, record the real ten-gp-per-rank practice/writing bill as actual stock quantities and identified categories; it is not a new currency-only substitute for materials. Ordinary blank writing stock, ordinary nonrare ink and ordinary practice supplies are discountable only when their actual source/provider identifies them as such. Rare inks and unique or specifically required components remain full quantity; copying rights, instructor/facility services, reusable tools and the separate blank book are not made discountable by calling them consumables. There is no universal numeric split of the ten gp. A stated mixed bill must retain its undiscounted total and each actual lot's identity, availability and legal precision. Apply Spell Scribe's 3/4 mundane factor separately from time; preserve divisible quantities, ceil required indivisible units once, and ceil the final actual purchase once to copper. Known protected items remain unchanged.
An unitemized or ambiguous bill has no justified material discount. The otherwise legal learner may still use the qualifying half-time route and supply the complete genuine undiscounted materials/bill; missing classification does not ban copying or its independent time benefit. Missing actual required materials still prevents work. No guessed rarity classification, refund for supplies already used, duplication of the source, free rare ink or teaching-cost waiver follows. Real consumption, deterioration and fees are recorded as they occur; interruption loses only its actual phase credit and actual resources, never refills stock.

### Original-position authored review references

```json
[
  {
    "id": "MF-24-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/46"
  },
  {
    "id": "MF-24-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/47"
  }
]
```

## MF-25 — Shadow Touched

### Complete original object

```json
{
  "id": "shadow_touched",
  "name": "Shadow Touched",
  "description": "Your exposure to the Shadowfell has changed you.",
  "prerequisite": "None",
  "effect": "You learn invisibility and one 1st-level necromancy or illusion spell. You can cast each once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve Invisibility and one rank1 Necromancy/Illusion choice, each once per Long Rest. The ordinary Invisibility card is still blocked. Define casting ability, spell-access route, charge and RP separation, components and replacement rules; preserve Shadowfell flavor without reviewing or extending cosmology."
```

### Preserved original source direction (historical)

```json
{
  "featId": "shadow_touched",
  "name": "Shadow Touched",
  "cohort": "magic_core",
  "questionId": "MF-25",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/24",
  "originalQuestion": "Preserve Invisibility and one rank1 Necromancy/Illusion choice, each once per Long Rest. The ordinary Invisibility card is still blocked. Define casting ability, spell-access route, charge and RP separation, components and replacement rules; preserve Shadowfell flavor without reviewing or extending cosmology.",
  "originalSourceObject": {
    "id": "shadow_touched",
    "name": "Shadow Touched",
    "description": "Your exposure to the Shadowfell has changed you.",
    "prerequisite": "None",
    "effect": "You learn invisibility and one 1st-level necromancy or illusion spell. You can cast each once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "b1d96146f93eceff60211d2b121b13ffbbb3ac614660cf795287e3313b340ac2",
  "submittedProcedure": "Choose INT,WIS orCHA permanently as this feat’s casting ability. Learn Invisibility through its actual reviewed rank2Illusion payload and one actual ordinary rank1Necromancy orIllusion placement from the finite current pool. Each has its own one-per-beneficial-Long-Rest use through the shared feat casting route. Record selected identity,rank,school and source provenance; a different school/placement on another class is not a free alternative mode. No ability-score increase, class repertoire/level, RPpool or unrestricted paid casting is granted. Components,nonprice costs and actual strain/interruption remain. Choices cannot be freely replaced at rest.\n\nCurrent Invisibility is the completed LRX card: Action,V/S/F,one willing creature within30feet,one minute with no concentration, ending immediately before that recipient commits any legal Action,Bonus Action orReaction, hostile or harmless. Keep its exact equipment-following/transfer boundaries; invisibility is not automatic Hidden, silence or odor suppression. The feat does not import a longer or concentration-based familiar external version. Shadowfell flavor remains preserved without explaining planes/origins or granting shadow travel.",
  "submittedNewChoices": "Permanent mental ability; separate rank2/rank1charges; carries current LRX broad-action Invisibility ending.",
  "submittedWorkedCases": [
    "The feat’s Invisibility recipient moves behind a pillar without spending an Action; movement alone does not end it. Committing Hide as an Action ends it before that Hide attempt.",
    "Using the separate rank1Necromancy choice does not refresh or spend Invisibility’s charge. Both casts still update the same character’s chronological spell-name history."
  ],
  "decision": "Retain the MF-25 complete grant/procedure and boundaries. Permanent mental ability; separate rank2/rank1charges; carries current LRX broad-action Invisibility ending. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose INT,WIS orCHA permanently as this feat’s casting ability. Learn Invisibility through its actual reviewed rank2Illusion payload and one actual ordinary rank1Necromancy orIllusion placement from the finite current pool. Each has its own one-per-beneficial-Long-Rest use through the shared feat casting route. Record selected identity,rank,school and source provenance; a different school/placement on another class is not a free alternative mode. No ability-score increase, class repertoire/level, RPpool or unrestricted paid casting is granted. Components,nonprice costs and actual strain/interruption remain. Choices cannot be freely replaced at rest.\n\nCurrent Invisibility is the completed LRX card: Action,V/S/F,one willing creature within30feet,one minute with no concentration, ending immediately before that recipient commits any legal Action,Bonus Action orReaction, hostile or harmless. Keep its exact equipment-following/transfer boundaries; invisibility is not automatic Hidden, silence or odor suppression. The feat does not import a longer or concentration-based familiar external version. Shadowfell flavor remains preserved without explaining planes/origins or granting shadow travel.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "The feat’s Invisibility recipient moves behind a pillar without spending an Action; movement alone does not end it. Committing Hide as an Action ends it before that Hide attempt.",
    "Using the separate rank1Necromancy choice does not refresh or spend Invisibility’s charge. Both casts still update the same character’s chronological spell-name history."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose INT,WIS orCHA permanently as this feat’s casting ability. Learn Invisibility through its actual reviewed rank2Illusion payload and one actual ordinary rank1Necromancy orIllusion placement from the finite current pool. Each has its own one-per-beneficial-Long-Rest use through the shared feat casting route. Record selected identity,rank,school and source provenance; a different school/placement on another class is not a free alternative mode. No ability-score increase, class repertoire/level, RPpool or unrestricted paid casting is granted. Components,nonprice costs and actual strain/interruption remain. Choices cannot be freely replaced at rest.

Current Invisibility is the completed LRX card: Action,V/S/F,one willing creature within30feet,one minute with no concentration, ending immediately before that recipient commits any legal Action,Bonus Action orReaction, hostile or harmless. Keep its exact equipment-following/transfer boundaries; invisibility is not automatic Hidden, silence or odor suppression. The feat does not import a longer or concentration-based familiar external version. Shadowfell flavor remains preserved without explaining planes/origins or granting shadow travel.

### Original-position authored review references

```json
[
  {
    "id": "MF-25-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/48"
  },
  {
    "id": "MF-25-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/49"
  },
  {
    "id": "FA-19",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/additionalBoundaryReviews/0"
  }
]
```

## MF-26 — Spell Echo Chamber

### Complete original object

```json
{
  "id": "spell_echo_chamber",
  "name": "Spell Echo Chamber",
  "description": "Your spells can affect a wider area through magical resonance.",
  "prerequisite": "Level 10",
  "effect": "Next spell affects area twice",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"The source only states next spell affects area twice. Define activation, cost, cadence, duration/expiry, qualifying area spell, two areas versus two resolutions, placement/overlap, saves/damage/control/concentration and delayed packets as explicit NEW decisions. Compare pending Echo Spell without adopting its half-effect rule by name."
```

### Preserved original source direction (historical)

```json
{
  "featId": "spell_echo_chamber",
  "name": "Spell Echo Chamber",
  "cohort": "magic_core",
  "questionId": "MF-26",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/25",
  "originalQuestion": "The source only states next spell affects area twice. Define activation, cost, cadence, duration/expiry, qualifying area spell, two areas versus two resolutions, placement/overlap, saves/damage/control/concentration and delayed packets as explicit NEW decisions. Compare pending Echo Spell without adopting its half-effect rule by name.",
  "originalSourceObject": {
    "id": "spell_echo_chamber",
    "name": "Spell Echo Chamber",
    "description": "Your spells can affect a wider area through magical resonance.",
    "prerequisite": "Level 10",
    "effect": "Next spell affects area twice",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "75ac190d7b479a2c20558b5345f63a33f49a10e03cc9ec4eac59e537132d0686",
  "submittedProcedure": "Keep total character level10. The original sentence “Next spell affects area twice” has no complete trigger,budget or geometry, so all following limits are NEW. Once per beneficial Long Rest, use a Bonus Action to prime one Echo Chamber for one minute. It applies to the next eligible spell you legally commit in that interval; a spell with no qualifying area does not consume the priming but the clock continues. Repriming is impossible until the use returns. An eligible spell directly establishes a finite,explicit cone,line,cube,circle or sphere of spell effects, instantaneous or sustained; it does not create extra creatures,objects,portals,physical inventory or paid item bodies merely because their spell has a listed area. A solely single-target,touch-only or indeterminate-area spell is ineligible.\n\nAt that eligible cast’s commitment, declare two full placements of the same actual area geometry, each independently legal under the original casting range/origin/line rules. Self-origin cones/lines must both originate at the actual caster; choose their separate orientations, not a second caster. A self-centered emanation retains its one actual center, so a coincident duplicate grants no wider footprint. A point-area spell may use two legal points. Spend only the spell’s ordinary cast costs, with one Dissonance/Refrain update, interruption window and concentration obligation; the feat use was already spent at priming and its prime is consumed at commitment even if countered.\n\nBoth placements have full native size/effect; NEW a creature or physical target included by both is resolved only once for each actual native spell trigger event. Roll shared native damage once for the combined simultaneous application, then resolve each distinct target’s save/defenses. No overlapping double damage, duplicate save or control record. For sustained zones, keep one actual spell identity and its existing per-target trigger budget across both areas; moving through both cannot reset a same-turn/round/cast allowance. Later pulses occur at the original spell’s real deadlines, and a genuine different native trigger remains distinct only where the original card already permits it. Concentration loss or ordinary ending ends both. If the source allows one area-movement command, NEW move at most one placement with that one command, not both for free; each remains subject to all actual control ranges. A dispel selecting this single ongoing cast ends its whole duplicated area application unless the original spell explicitly defines independently separable effects. The feat adds no second spell, second payload budget or half-strength Echo Spell rule.",
  "submittedNewChoices": "BA/1LR/1-minute prime; two independently legal full areas; no overlap duplication and shared sustained-trigger identity.",
  "submittedWorkedCases": [
    "A qualifying20-foot-radius spell is placed at two legal origins. A creature in both rolls its one native save and receives the shared damage result once; a creature only in the second is also a normal eligible target.",
    "A sustained damaging area’s native once-per-turn entry limit remains one across both placements. Losing the one concentration ends both, and moving one area with an Action does not move the other for free."
  ],
  "decision": "Retain the MF-26 complete grant/procedure and boundaries. BA/1LR/1-minute prime; two independently legal full areas; no overlap duplication and shared sustained-trigger identity. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Keep total character level10. The original sentence “Next spell affects area twice” has no complete trigger,budget or geometry, so all following limits are NEW. Once per beneficial Long Rest, use a Bonus Action to prime one Echo Chamber for one minute. It applies to the next eligible spell you legally commit in that interval; a spell with no qualifying area does not consume the priming but the clock continues. Repriming is impossible until the use returns. An eligible spell directly establishes a finite,explicit cone,line,cube,circle or sphere of spell effects, instantaneous or sustained; it does not create extra creatures,objects,portals,physical inventory or paid item bodies merely because their spell has a listed area. A solely single-target,touch-only or indeterminate-area spell is ineligible.\n\nAt that eligible cast’s commitment, declare two full placements of the same actual area geometry, each independently legal under the original casting range/origin/line rules. Self-origin cones/lines must both originate at the actual caster; choose their separate orientations, not a second caster. A self-centered emanation retains its one actual center, so a coincident duplicate grants no wider footprint. A point-area spell may use two legal points. Spend only the spell’s ordinary cast costs, with one Dissonance/Refrain update, interruption window and concentration obligation; the feat use was already spent at priming and its prime is consumed at commitment even if countered.\n\nBoth placements have full native size/effect; NEW a creature or physical target included by both is resolved only once for each actual native spell trigger event. Roll shared native damage once for the combined simultaneous application, then resolve each distinct target’s save/defenses. No overlapping double damage, duplicate save or control record. For sustained zones, keep one actual spell identity and its existing per-target trigger budget across both areas; moving through both cannot reset a same-turn/round/cast allowance. Later pulses occur at the original spell’s real deadlines, and a genuine different native trigger remains distinct only where the original card already permits it. Concentration loss or ordinary ending ends both. If the source allows one area-movement command, NEW move at most one placement with that one command, not both for free; each remains subject to all actual control ranges. A dispel selecting this single ongoing cast ends its whole duplicated area application unless the original spell explicitly defines independently separable effects. The feat adds no second spell, second payload budget or half-strength Echo Spell rule.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A qualifying20-foot-radius spell is placed at two legal origins. A creature in both rolls its one native save and receives the shared damage result once; a creature only in the second is also a normal eligible target.",
    "A sustained damaging area’s native once-per-turn entry limit remains one across both placements. Losing the one concentration ends both, and moving one area with an Action does not move the other for free."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Keep total character level10. The original sentence “Next spell affects area twice” has no complete trigger,budget or geometry, so all following limits are NEW. Once per beneficial Long Rest, use a Bonus Action to prime one Echo Chamber for one minute. It applies to the next eligible spell you legally commit in that interval; a spell with no qualifying area does not consume the priming but the clock continues. Repriming is impossible until the use returns. An eligible spell directly establishes a finite,explicit cone,line,cube,circle or sphere of spell effects, instantaneous or sustained; it does not create extra creatures,objects,portals,physical inventory or paid item bodies merely because their spell has a listed area. A solely single-target,touch-only or indeterminate-area spell is ineligible.

At that eligible cast’s commitment, declare two full placements of the same actual area geometry, each independently legal under the original casting range/origin/line rules. Self-origin cones/lines must both originate at the actual caster; choose their separate orientations, not a second caster. A self-centered emanation retains its one actual center, so a coincident duplicate grants no wider footprint. A point-area spell may use two legal points. Spend only the spell’s ordinary cast costs, with one Dissonance/Refrain update, interruption window and concentration obligation; the feat use was already spent at priming and its prime is consumed at commitment even if countered.

Both placements have full native size/effect; NEW a creature or physical target included by both is resolved only once for each actual native spell trigger event. Roll shared native damage once for the combined simultaneous application, then resolve each distinct target’s save/defenses. No overlapping double damage, duplicate save or control record. For sustained zones, keep one actual spell identity and its existing per-target trigger budget across both areas; moving through both cannot reset a same-turn/round/cast allowance. Later pulses occur at the original spell’s real deadlines, and a genuine different native trigger remains distinct only where the original card already permits it. Concentration loss or ordinary ending ends both. If the source allows one area-movement command, NEW move at most one placement with that one command, not both for free; each remains subject to all actual control ranges. A dispel selecting this single ongoing cast ends its whole duplicated area application unless the original spell explicitly defines independently separable effects. The feat adds no second spell, second payload budget or half-strength Echo Spell rule.

### Original-position authored review references

```json
[
  {
    "id": "MF-26-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/50"
  },
  {
    "id": "MF-26-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/51"
  }
]
```

## MF-27 — Spell Penetration

### Complete original object

```json
{
  "id": "spellPenetration",
  "name": "Spell Penetration",
  "description": "Your spells are particularly effective against magical defenses.",
  "prerequisite": "Spellcasting ability, Level 5",
  "effect": "+2 bonus to spell attack rolls against targets with spell resistance",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Define an actual spell-resistance predicate from sourced mechanics, including the supplied Shaman Spell Resistance card, versus resistance to damage or save advantage. Preserve+2 to spell attack only, level5 and spellcasting; resolve target qualification and stacking without inventing a resistance stat or granting bypass."
```

### Preserved original source direction (historical)

```json
{
  "featId": "spellPenetration",
  "name": "Spell Penetration",
  "cohort": "magic_core",
  "questionId": "MF-27",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/26",
  "originalQuestion": "Define an actual spell-resistance predicate from sourced mechanics, including the supplied Shaman Spell Resistance card, versus resistance to damage or save advantage. Preserve+2 to spell attack only, level5 and spellcasting; resolve target qualification and stacking without inventing a resistance stat or granting bypass.",
  "originalSourceObject": {
    "id": "spellPenetration",
    "name": "Spell Penetration",
    "description": "Your spells are particularly effective against magical defenses.",
    "prerequisite": "Spellcasting ability, Level 5",
    "effect": "+2 bonus to spell attack rolls against targets with spell resistance",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "e6493c1e65b1d292d68d63656b7dfafae9730106428ac41de88006b6487f9ba1",
  "submittedProcedure": "Retain total character level5and actual personal spellcasting. NEW bounded target predicate: at the instant of your personal spell attack roll, the target must have a real currently active source explicitly named Spell Resistance or Magic Resistance, or a rule granting general advantage on saves against spells as a category. The supplied Shaman Bloodcaller Spell Resistance qualifies through its actual active save-advantage card; its lack of an attack-defense number does not erase the feat’s printed attack bonus. Specific fire resistance,highAC,cover,condition-only save advantage or War Caster’s concentration advantage does not qualify by itself. An inactive,suppressed or exhausted conditional defense does not qualify.\n\nAgainst such a target, add+2to your genuine spell attack roll, once for this feat identity. This does not negate its defense,lowerAC,change saveDC,aid a Counterspell/Dispel ability check,turn a save into an attack or ignore immunity. A separately actual general flat spell-attack feat bonus can combine under the proposed feat family unless its own source says otherwise. Apply the predicate from real game state without giving the player an extra identification scan: the Director can adjudicate a hidden qualifying record without disclosing its name or inferential reason. Companion attacks merely using your spell attack modifier are not your personal spell attack for this feat.",
  "submittedNewChoices": "Explicit real resistance/save-advantage predicate including actual Shaman card; no invented spell-resistance statistic.",
  "submittedWorkedCases": [
    "A Shaman with active Spell Resistance is targeted by your actual spell attack. Add2to your attack; its ordinary save advantage remains relevant to other actual saves and is not removed.",
    "A target resistant only tofire grants no Spell Penetration bonus. A Counterspell check against an actual spell from a resistant caster is still an ability check and gains no+2."
  ],
  "decision": "Retain the MF-27 complete grant/procedure and boundaries. Explicit real resistance/save-advantage predicate including actual Shaman card; no invented spell-resistance statistic. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Retain total character level5and actual personal spellcasting. NEW bounded target predicate: at the instant of your personal spell attack roll, the target must have a real currently active source explicitly named Spell Resistance or Magic Resistance, or a rule granting general advantage on saves against spells as a category. The supplied Shaman Bloodcaller Spell Resistance qualifies through its actual active save-advantage card; its lack of an attack-defense number does not erase the feat’s printed attack bonus. Specific fire resistance,highAC,cover,condition-only save advantage or War Caster’s concentration advantage does not qualify by itself. An inactive,suppressed or exhausted conditional defense does not qualify.\n\nAgainst such a target, add+2to your genuine spell attack roll, once for this feat identity. This does not negate its defense,lowerAC,change saveDC,aid a Counterspell/Dispel ability check,turn a save into an attack or ignore immunity. A separately actual general flat spell-attack feat bonus can combine under the proposed feat family unless its own source says otherwise. Apply the predicate from real game state without giving the player an extra identification scan: the Director can adjudicate a hidden qualifying record without disclosing its name or inferential reason. Companion attacks merely using your spell attack modifier are not your personal spell attack for this feat.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A Shaman with active Spell Resistance is targeted by your actual spell attack. Add2to your attack; its ordinary save advantage remains relevant to other actual saves and is not removed.",
    "A target resistant only tofire grants no Spell Penetration bonus. A Counterspell check against an actual spell from a resistant caster is still an ability check and gains no+2."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Retain total character level5and actual personal spellcasting. NEW bounded target predicate: at the instant of your personal spell attack roll, the target must have a real currently active source explicitly named Spell Resistance or Magic Resistance, or a rule granting general advantage on saves against spells as a category. The supplied Shaman Bloodcaller Spell Resistance qualifies through its actual active save-advantage card; its lack of an attack-defense number does not erase the feat’s printed attack bonus. Specific fire resistance,highAC,cover,condition-only save advantage or War Caster’s concentration advantage does not qualify by itself. An inactive,suppressed or exhausted conditional defense does not qualify.

Against such a target, add+2to your genuine spell attack roll, once for this feat identity. This does not negate its defense,lowerAC,change saveDC,aid a Counterspell/Dispel ability check,turn a save into an attack or ignore immunity. A separately actual general flat spell-attack feat bonus can combine under the proposed feat family unless its own source says otherwise. Apply the predicate from real game state without giving the player an extra identification scan: the Director can adjudicate a hidden qualifying record without disclosing its name or inferential reason. Companion attacks merely using your spell attack modifier are not your personal spell attack for this feat.

### Original-position authored review references

```json
[
  {
    "id": "MF-27-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/52"
  },
  {
    "id": "MF-27-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/53"
  }
]
```

## MF-28 — Spell Sniper

### Complete original object

```json
{
  "id": "spell_sniper",
  "name": "Spell Sniper",
  "description": "You have learned techniques to enhance your spells.",
  "prerequisite": "Ability to cast at least one spell",
  "effect": "When you cast a spell that requires a ranged attack roll, the spell's range is doubled.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Define actual ranged-spell-attack qualification, double printed range versus radius, Self/Touch/unlimited ranges, maintained-control distances and source placement differences. No unprinted cover ignoring, critical expansion or extra cantrip grant. Cast and attack must remain legally possible."
```

### Preserved original source direction (historical)

```json
{
  "featId": "spell_sniper",
  "name": "Spell Sniper",
  "cohort": "magic_core",
  "questionId": "MF-28",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/27",
  "originalQuestion": "Define actual ranged-spell-attack qualification, double printed range versus radius, Self/Touch/unlimited ranges, maintained-control distances and source placement differences. No unprinted cover ignoring, critical expansion or extra cantrip grant. Cast and attack must remain legally possible.",
  "originalSourceObject": {
    "id": "spell_sniper",
    "name": "Spell Sniper",
    "description": "You have learned techniques to enhance your spells.",
    "prerequisite": "Ability to cast at least one spell",
    "effect": "When you cast a spell that requires a ranged attack roll, the spell's range is doubled.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "cd347bacd08685b9eee64a7f7af08c73e67eae6a397e00003838f77284ce69ce",
  "submittedProcedure": "Require an actual acquired ability to cast a spell. When you personally cast a spell whose own procedure requires a ranged spell attack, double its finite positive printed casting range for that cast. NEW this is a casting-range modifier, not a doubling of radius,cone,length,speed,companion command range,secondary-target spacing or maintained-control distance. Self,Touch,unlimited and a creature’s independent ranged attack after summoning do not qualify. A spell requiring only a save or a melee spell attack does not qualify merely because its narration travels through the air. A spell granting a separate ordinary weapon attack is not converted into a ranged spell attack by this feat.\n\nThe actual target/origin must remain legal within that doubled casting range and under line,visibility and source exclusions. A spell with an independently stated shorter later control/attack distance retains that distance; this feat changes only its initial range. Use the actual chosen placement’s printed range, not the catalog’s maximum header from another mode. Apply the doubling once; proposed Metamagic Reach adds its30feet afterward. No cover ignoring,extra cantrip,expanded critical or generic accuracy bonus is granted.",
  "submittedNewChoices": "Finite printed casting range only; actual ranged-spell-attack requirement and explicit later-distance boundary.",
  "submittedWorkedCases": [
    "A genuine ranged spell attack with printed60-foot casting range can target at120feet if ordinary line/target rules permit. A20-foot effect radius remains20feet.",
    "A summoned creature’s30-foot ranged attack stays30feet. Casting a self-origin beam whose range isSelfdoes not invent a numeric range to double."
  ],
  "decision": "Retain the MF-28 complete grant/procedure and boundaries. Finite printed casting range only; actual ranged-spell-attack requirement and explicit later-distance boundary. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require an actual acquired ability to cast a spell. When you personally cast a spell whose own procedure requires a ranged spell attack, double its finite positive printed casting range for that cast. NEW this is a casting-range modifier, not a doubling of radius,cone,length,speed,companion command range,secondary-target spacing or maintained-control distance. Self,Touch,unlimited and a creature’s independent ranged attack after summoning do not qualify. A spell requiring only a save or a melee spell attack does not qualify merely because its narration travels through the air. A spell granting a separate ordinary weapon attack is not converted into a ranged spell attack by this feat.\n\nThe actual target/origin must remain legal within that doubled casting range and under line,visibility and source exclusions. A spell with an independently stated shorter later control/attack distance retains that distance; this feat changes only its initial range. Use the actual chosen placement’s printed range, not the catalog’s maximum header from another mode. Apply the doubling once; proposed Metamagic Reach adds its30feet afterward. No cover ignoring,extra cantrip,expanded critical or generic accuracy bonus is granted.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A genuine ranged spell attack with printed60-foot casting range can target at120feet if ordinary line/target rules permit. A20-foot effect radius remains20feet.",
    "A summoned creature’s30-foot ranged attack stays30feet. Casting a self-origin beam whose range isSelfdoes not invent a numeric range to double."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require an actual acquired ability to cast a spell. When you personally cast a spell whose own procedure requires a ranged spell attack, double its finite positive printed casting range for that cast. NEW this is a casting-range modifier, not a doubling of radius,cone,length,speed,companion command range,secondary-target spacing or maintained-control distance. Self,Touch,unlimited and a creature’s independent ranged attack after summoning do not qualify. A spell requiring only a save or a melee spell attack does not qualify merely because its narration travels through the air. A spell granting a separate ordinary weapon attack is not converted into a ranged spell attack by this feat.

The actual target/origin must remain legal within that doubled casting range and under line,visibility and source exclusions. A spell with an independently stated shorter later control/attack distance retains that distance; this feat changes only its initial range. Use the actual chosen placement’s printed range, not the catalog’s maximum header from another mode. Apply the doubling once; proposed Metamagic Reach adds its30feet afterward. No cover ignoring,extra cantrip,expanded critical or generic accuracy bonus is granted.

### Original-position authored review references

```json
[
  {
    "id": "MF-28-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/54"
  },
  {
    "id": "MF-28-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/55"
  }
]
```

## MF-29 — Telekinetic

### Complete original object

```json
{
  "id": "telekinetic",
  "name": "Telekinetic",
  "description": "You have learned to move things with your mind.",
  "prerequisite": "None",
  "effect": "You learn the mage hand cantrip and can cast it without verbal or somatic components. You can use it to shove creatures.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Mage Hand exists as an ordinary blocked spell; preserve learning it and waived V/S while keeping any other components. Define an explicit shove action/target/range/size/ability/DC, push/pull distance, resistance and repeated-use cadence. No invisible hand, free attack or extra command budget inferred from outside rules."
```

### Preserved original source direction (historical)

```json
{
  "featId": "telekinetic",
  "name": "Telekinetic",
  "cohort": "magic_core",
  "questionId": "MF-29",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/28",
  "originalQuestion": "Mage Hand exists as an ordinary blocked spell; preserve learning it and waived V/S while keeping any other components. Define an explicit shove action/target/range/size/ability/DC, push/pull distance, resistance and repeated-use cadence. No invisible hand, free attack or extra command budget inferred from outside rules.",
  "originalSourceObject": {
    "id": "telekinetic",
    "name": "Telekinetic",
    "description": "You have learned to move things with your mind.",
    "prerequisite": "None",
    "effect": "You learn the mage hand cantrip and can cast it without verbal or somatic components. You can use it to shove creatures.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "7c0fb782b6ee542e88f4d36811753b35bd96cd7e1bf5b62949ccdf3c1254739b",
  "submittedProcedure": "Choose INT,WIS orCHA permanently for this feat. Learn the exact ordinary Mage Hand identity (`mage-hand`,Universal rank0), using a NEW feat route with that chosen casting ability. Waive only its V/Scomponents for casts through this feat; a genuinely added other requirement remains. It is a real cast with its actual Action,shared Refrain/strain and interruption eligibility; absence of V/Sdoes not itself grant invisibility or hide an observable manifestation. Keep the current LRXvisible hand,no creature/objectHP,concentration up to1minute,30-foot control range,10lb/1-foot-cube unattended-object capacity,10-foot movement per caster Action and cargo-release rules. It does not become the different Transmutation Magehand identity.\n\nNEW explicit creature-shove exception: as the one manipulation of the creation Action or a later Action commanding this actual hand, you may move the hand up to its ordinary10feet along a visible unobstructed path and attempt to shove one visible Large-or-smaller creature within5feet of the hand and within30feet of you. The target makes STRsave against8+PB+your feat ability modifier. On failure choose before resolution to push it5feet directly away from you along a legal supported path, or knock itProne; on success neither. This replaces the ordinary physical opposed-Shove roll only for this feat; no body-size growth,damage,pull,grapple or extra attack. Actual forced-movement/Prone immunities and geometry apply. No free object manipulation accompanies the shove. Each attempt uses its own legal Action; extra Actions do not refresh other resources, and there is no Bonus Action or autonomous-hand turn. If range/path/concentration is lost, the hand cannot shove and its normal ending/release rules apply. It supplies no ordinary spell-component hand or attended-object theft.",
  "submittedNewChoices": "Permanent feat ability; exact Mage Hand route with V/Swaiver; Action/STRsave/Large cap/5-foot push-or-Prone exception.",
  "submittedWorkedCases": [
    "Creating the visible hand can include one legal shove attempt instead of lifting an object. The target passes itsSTRsave, so no movement orProne occurs; the casting Action and chronological strain record remain spent.",
    "A later shove command is an Action using the existing hand, not another cast and not free telepathic manipulation. A creature beyond30feet cannot be shoved by claiming the hand has a separate unrestricted reach."
  ],
  "decision": "Retain the MF-29 complete grant/procedure and boundaries. Permanent feat ability; exact Mage Hand route with V/Swaiver; Action/STRsave/Large cap/5-foot push-or-Prone exception. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose INT,WIS orCHA permanently for this feat. Learn the exact ordinary Mage Hand identity (`mage-hand`,Universal rank0), using a NEW feat route with that chosen casting ability. Waive only its V/Scomponents for casts through this feat; a genuinely added other requirement remains. It is a real cast with its actual Action,shared Refrain/strain and interruption eligibility; absence of V/Sdoes not itself grant invisibility or hide an observable manifestation. Keep the current LRXvisible hand,no creature/objectHP,concentration up to1minute,30-foot control range,10lb/1-foot-cube unattended-object capacity,10-foot movement per caster Action and cargo-release rules. It does not become the different Transmutation Magehand identity.\n\nNEW explicit creature-shove exception: as the one manipulation of the creation Action or a later Action commanding this actual hand, you may move the hand up to its ordinary10feet along a visible unobstructed path and attempt to shove one visible Large-or-smaller creature within5feet of the hand and within30feet of you. The target makes STRsave against8+PB+your feat ability modifier. On failure choose before resolution to push it5feet directly away from you along a legal supported path, or knock itProne; on success neither. This replaces the ordinary physical opposed-Shove roll only for this feat; no body-size growth,damage,pull,grapple or extra attack. Actual forced-movement/Prone immunities and geometry apply. No free object manipulation accompanies the shove. Each attempt uses its own legal Action; extra Actions do not refresh other resources, and there is no Bonus Action or autonomous-hand turn. If range/path/concentration is lost, the hand cannot shove and its normal ending/release rules apply. It supplies no ordinary spell-component hand or attended-object theft.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Creating the visible hand can include one legal shove attempt instead of lifting an object. The target passes itsSTRsave, so no movement orProne occurs; the casting Action and chronological strain record remain spent.",
    "A later shove command is an Action using the existing hand, not another cast and not free telepathic manipulation. A creature beyond30feet cannot be shoved by claiming the hand has a separate unrestricted reach."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose INT,WIS orCHA permanently for this feat. Learn the exact ordinary Mage Hand identity (`mage-hand`,Universal rank0), using a NEW feat route with that chosen casting ability. Waive only its V/Scomponents for casts through this feat; a genuinely added other requirement remains. It is a real cast with its actual Action,shared Refrain/strain and interruption eligibility; absence of V/Sdoes not itself grant invisibility or hide an observable manifestation. Keep the current LRXvisible hand,no creature/objectHP,concentration up to1minute,30-foot control range,10lb/1-foot-cube unattended-object capacity,10-foot movement per caster Action and cargo-release rules. It does not become the different Transmutation Magehand identity.

NEW explicit creature-shove exception: as the one manipulation of the creation Action or a later Action commanding this actual hand, you may move the hand up to its ordinary10feet along a visible unobstructed path and attempt to shove one visible Large-or-smaller creature within5feet of the hand and within30feet of you. The target makes STRsave against8+PB+your feat ability modifier. On failure choose before resolution to push it5feet directly away from you along a legal supported path, or knock itProne; on success neither. This replaces the ordinary physical opposed-Shove roll only for this feat; no body-size growth,damage,pull,grapple or extra attack. Actual forced-movement/Prone immunities and geometry apply. No free object manipulation accompanies the shove. Each attempt uses its own legal Action; extra Actions do not refresh other resources, and there is no Bonus Action or autonomous-hand turn. If range/path/concentration is lost, the hand cannot shove and its normal ending/release rules apply. It supplies no ordinary spell-component hand or attended-object theft.

### Original-position authored review references

```json
[
  {
    "id": "MF-29-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/56"
  },
  {
    "id": "MF-29-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/57"
  }
]
```

## MF-30 — Telepathic

### Complete original object

```json
{
  "id": "telepathic",
  "name": "Telepathic",
  "description": "You can reach out to others with your mind.",
  "prerequisite": "None",
  "effect": "You can communicate telepathically with creatures and cast detect thoughts once per long rest.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"No exact Detect Thoughts definition was found in the848 ordinary plus10 ancestry catalogs. Define telepathy range, willing/aware recipients, senses/languages, directionality and actions; separately resolve once-per-Long-Rest spell grant and actual dependency. Do not invent mind-reading content, a spell profile or creature cognition taxonomy from the feat name."
```

### Preserved original source direction (historical)

```json
{
  "featId": "telepathic",
  "name": "Telepathic",
  "cohort": "magic_core",
  "questionId": "MF-30",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/29",
  "originalQuestion": "No exact Detect Thoughts definition was found in the848 ordinary plus10 ancestry catalogs. Define telepathy range, willing/aware recipients, senses/languages, directionality and actions; separately resolve once-per-Long-Rest spell grant and actual dependency. Do not invent mind-reading content, a spell profile or creature cognition taxonomy from the feat name.",
  "originalSourceObject": {
    "id": "telepathic",
    "name": "Telepathic",
    "description": "You can reach out to others with your mind.",
    "prerequisite": "None",
    "effect": "You can communicate telepathically with creatures and cast detect thoughts once per long rest.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "6174829f48c3b5121cc2b2ed7c71ad074307d95d0ed0e50e824e8b787bf937d2",
  "submittedProcedure": "Choose INT,WIS orCHA permanently as this feat’s casting ability. NEW communication procedure: while conscious, you may direct one brief intentional message at a time to one perceived willing conscious creature within60feet and line of effect, with the same ordinary conversational timing as speech and no extra Action. A willing recipient may reply through that same temporary channel while eligibility continues. Shared language permits normal phrases; absent a shared language, only a simple voluntarily conveyed image,emotion or basic idea is received, not automatic precise translation. The recipient may refuse or end the exchange; silence supplies no diagnosis of presence,thought,consent or mind protection. This grants no reading,compulsion,command authority,remote tracking,hidden-creature search or ability to use telepathy as a spell’s Vcomponent. Loss of range,line or consciousness ends the channel. It supplies no simultaneous group channel or extra reaction-time instructions beyond actual turn rules.\n\nThe named Detect Thoughts has no exact entry in the848ordinary plus10supplemental ancestry source catalogs. NEW proposed feat-only spell payload, explicitly not an alias for Read Surface Thoughts: rank2Divination,Action,V/S/F,one perceived creature within30feet and line of effect,concentration up to1minute. The feat gives one cast per beneficial Long Rest through the common charge route. At initial resolution and on a later Action spent on this one same target while it remains in range/line, request one sample and make a fresh targetWISsave against the featDC. A failed save reveals one actual current conscious surface thought under the already reviewed Read Surface Thoughts information limits; success reveals none. The initial cast Action includes at most one sample. No new sample occurs without its real Action, and repeated sampling does not recast or replay Dissonance. NEW the target becomes aware of an attempted mental intrusion at the first sample, regardless of its save, without automatically identifying a hidden caster.\n\nAn absent conscious thought,protection or failed information access supplies no reason-diagnosis; ordinary dreams are not conscious thoughts without a specific exception. Preserve verbal thoughts’ actual language and nonverbal impressions without inventing meaning. There is no memory search,truth enforcement,forced subject,biography,creature-type cognition assumption or automatic translation. Specific information protections,including actual Divination/Scrying protection,apply. No target switch within the one cast; loss of its range/line prevents sampling while the original deadline continues, and ending concentration ends the attempt. The new supplemental profile must be accepted/replaced by GPT before any use; it does not add ordinary class access or silently claim a missing original definition was recovered.",
  "submittedNewChoices": "Finite consensual two-way communication; NEW isolated Detect Thoughts recurring surface-sample profile with actual saves,Actions,notification and information protections.",
  "submittedWorkedCases": [
    "Two willing creatures sharing no language can exchange a simple image of an open door through the channel; this does not translate an unknown legal contract or read unspoken motives.",
    "A legal Detect Thoughts cast is followed by two later sampling Actions. The target makes three distinct saves total; only actual failed samples expose the thought currently present then, and none compels it to think about the caster’s preferred question."
  ],
  "decision": "Retain the MF-30 complete grant/procedure and boundaries. Finite consensual two-way communication; NEW isolated Detect Thoughts recurring surface-sample profile with actual saves,Actions,notification and information protections. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Choose INT,WIS orCHA permanently as this feat’s casting ability. NEW communication procedure: while conscious, you may direct one brief intentional message at a time to one perceived willing conscious creature within60feet and line of effect, with the same ordinary conversational timing as speech and no extra Action. A willing recipient may reply through that same temporary channel while eligibility continues. Shared language permits normal phrases; absent a shared language, only a simple voluntarily conveyed image,emotion or basic idea is received, not automatic precise translation. The recipient may refuse or end the exchange; silence supplies no diagnosis of presence,thought,consent or mind protection. This grants no reading,compulsion,command authority,remote tracking,hidden-creature search or ability to use telepathy as a spell’s Vcomponent. Loss of range,line or consciousness ends the channel. It supplies no simultaneous group channel or extra reaction-time instructions beyond actual turn rules.\n\nThe named Detect Thoughts has no exact entry in the848ordinary plus10supplemental ancestry source catalogs. NEW proposed feat-only spell payload, explicitly not an alias for Read Surface Thoughts: rank2Divination,Action,V/S/F,one perceived creature within30feet and line of effect,concentration up to1minute. The feat gives one cast per beneficial Long Rest through the common charge route. At initial resolution and on a later Action spent on this one same target while it remains in range/line, request one sample and make a fresh targetWISsave against the featDC. A failed save reveals one actual current conscious surface thought under the already reviewed Read Surface Thoughts information limits; success reveals none. The initial cast Action includes at most one sample. No new sample occurs without its real Action, and repeated sampling does not recast or replay Dissonance. NEW the target becomes aware of an attempted mental intrusion at the first sample, regardless of its save, without automatically identifying a hidden caster.\n\nAn absent conscious thought,protection or failed information access supplies no reason-diagnosis; ordinary dreams are not conscious thoughts without a specific exception. Preserve verbal thoughts’ actual language and nonverbal impressions without inventing meaning. There is no memory search,truth enforcement,forced subject,biography,creature-type cognition assumption or automatic translation. Specific information protections,including actual Divination/Scrying protection,apply. No target switch within the one cast; loss of its range/line prevents sampling while the original deadline continues, and ending concentration ends the attempt. The new supplemental profile must be accepted/replaced by GPT before any use; it does not add ordinary class access or silently claim a missing original definition was recovered.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Two willing creatures sharing no language can exchange a simple image of an open door through the channel; this does not translate an unknown legal contract or read unspoken motives.",
    "A legal Detect Thoughts cast is followed by two later sampling Actions. The target makes three distinct saves total; only actual failed samples expose the thought currently present then, and none compels it to think about the caster’s preferred question."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Choose INT,WIS orCHA permanently as this feat’s casting ability. NEW communication procedure: while conscious, you may direct one brief intentional message at a time to one perceived willing conscious creature within60feet and line of effect, with the same ordinary conversational timing as speech and no extra Action. A willing recipient may reply through that same temporary channel while eligibility continues. Shared language permits normal phrases; absent a shared language, only a simple voluntarily conveyed image,emotion or basic idea is received, not automatic precise translation. The recipient may refuse or end the exchange; silence supplies no diagnosis of presence,thought,consent or mind protection. This grants no reading,compulsion,command authority,remote tracking,hidden-creature search or ability to use telepathy as a spell’s Vcomponent. Loss of range,line or consciousness ends the channel. It supplies no simultaneous group channel or extra reaction-time instructions beyond actual turn rules.

The named Detect Thoughts has no exact entry in the848ordinary plus10supplemental ancestry source catalogs. NEW proposed feat-only spell payload, explicitly not an alias for Read Surface Thoughts: rank2Divination,Action,V/S/F,one perceived creature within30feet and line of effect,concentration up to1minute. The feat gives one cast per beneficial Long Rest through the common charge route. At initial resolution and on a later Action spent on this one same target while it remains in range/line, request one sample and make a fresh targetWISsave against the featDC. A failed save reveals one actual current conscious surface thought under the already reviewed Read Surface Thoughts information limits; success reveals none. The initial cast Action includes at most one sample. No new sample occurs without its real Action, and repeated sampling does not recast or replay Dissonance. NEW the target becomes aware of an attempted mental intrusion at the first sample, regardless of its save, without automatically identifying a hidden caster.

An absent conscious thought,protection or failed information access supplies no reason-diagnosis; ordinary dreams are not conscious thoughts without a specific exception. Preserve verbal thoughts’ actual language and nonverbal impressions without inventing meaning. There is no memory search,truth enforcement,forced subject,biography,creature-type cognition assumption or automatic translation. Specific information protections,including actual Divination/Scrying protection,apply. No target switch within the one cast; loss of its range/line prevents sampling while the original deadline continues, and ending concentration ends the attempt. The new supplemental profile must be accepted/replaced by GPT before any use; it does not add ordinary class access or silently claim a missing original definition was recovered.

### Original-position authored review references

```json
[
  {
    "id": "MF-30-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/58"
  },
  {
    "id": "MF-30-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/59"
  }
]
```

## MF-31 — War Caster

### Complete original object

```json
{
  "id": "war_caster",
  "name": "War Caster",
  "description": "You have practiced casting spells in the midst of combat.",
  "prerequisite": "Ability to cast at least one spell",
  "effect": "You have advantage on Constitution saving throws to maintain concentration on spells.",
  "type": "Magic",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Preserve its sole printed effect: advantage on Constitution saves maintaining concentration on spells. Bind current concentration/strain procedure, damage-event timing, normal advantage cancellation and nonproficient-armor disadvantage. Do not import somatic exceptions, reaction spells or nonspell concentration benefits."
```

### Preserved original source direction (historical)

```json
{
  "featId": "war_caster",
  "name": "War Caster",
  "cohort": "magic_core",
  "questionId": "MF-31",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/magic_core_feat_operating_proposal_internal.json",
  "sourceFileSha256": "b80dafd11b8f340d068e1daccb1b945ff5deaffcb85e1dc93df19884d6c28b95",
  "sourcePointer": "/records/30",
  "originalQuestion": "Preserve its sole printed effect: advantage on Constitution saves maintaining concentration on spells. Bind current concentration/strain procedure, damage-event timing, normal advantage cancellation and nonproficient-armor disadvantage. Do not import somatic exceptions, reaction spells or nonspell concentration benefits.",
  "originalSourceObject": {
    "id": "war_caster",
    "name": "War Caster",
    "description": "You have practiced casting spells in the midst of combat.",
    "prerequisite": "Ability to cast at least one spell",
    "effect": "You have advantage on Constitution saving throws to maintain concentration on spells.",
    "type": "Magic",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "4c0ec68c006cb3546d64a2f58d84295a1ebc3db347492a7b5a29be0b4e416ad1",
  "submittedProcedure": "Require actual acquired spellcasting. You have advantage on CONsaving throws whose actual purpose is maintaining concentration on a spell you are sustaining. This includes a real damage-triggered concentration save or another explicit CONsave to retain that spell, and no other roll merely because losing it might later break concentration. Use the existing damage-event timing and one-save procedure; temporaryHP absorption and actual damage consequences retain their governing definitions. Ordinary nonproficient-armor disadvantage or another actual disadvantage cancels the advantage normally; neither produces additional dice. A source-specific flat concentration bonus such as the proposed Resilient Mind applies separately if genuinely eligible under its own rule. WoundCONsaves,death saves,ordinary Strain/Exhaustion saves and nonspell concentration checks do not qualify simply because this creature also casts spells. The sole printed effect grants no occupied-hand Spermission,Reaction spell,reaction attack,automatic success or second concentration slot.",
  "submittedNewChoices": "Exact concentration-spell CONpredicate, including actual disadvantage cancellation; no imported same-name extra clauses.",
  "submittedWorkedCases": [
    "Damage causes one CONsave to maintain a real spell concentration. War Caster grants advantage, but nonproficient worn armor’s actual concentration disadvantage cancels it to one die.",
    "The same damage event causes a WoundCONsave as well. That separate save gains no War Caster advantage, even if becoming incapacitated from its consequences would end concentration."
  ],
  "decision": "Retain the MF-31 complete grant/procedure and boundaries. Exact concentration-spell CONpredicate, including actual disadvantage cancellation; no imported same-name extra clauses. Final named supplementary menus and shared spellcasting rules are part of this source decision; no pending payload or class is promoted.",
  "completeAuthoringProcedure": "Require actual acquired spellcasting. You have advantage on CONsaving throws whose actual purpose is maintaining concentration on a spell you are sustaining. This includes a real damage-triggered concentration save or another explicit CONsave to retain that spell, and no other roll merely because losing it might later break concentration. Use the existing damage-event timing and one-save procedure; temporaryHP absorption and actual damage consequences retain their governing definitions. Ordinary nonproficient-armor disadvantage or another actual disadvantage cancels the advantage normally; neither produces additional dice. A source-specific flat concentration bonus such as the proposed Resilient Mind applies separately if genuinely eligible under its own rule. WoundCONsaves,death saves,ordinary Strain/Exhaustion saves and nonspell concentration checks do not qualify simply because this creature also casts spells. The sole printed effect grants no occupied-hand Spermission,Reaction spell,reaction attack,automatic success or second concentration slot.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Damage causes one CONsave to maintain a real spell concentration. War Caster grants advantage, but nonproficient worn armor’s actual concentration disadvantage cancels it to one die.",
    "The same damage event causes a WoundCONsave as well. That separate save gains no War Caster advantage, even if becoming incapacitated from its consequences would end concentration."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Require actual acquired spellcasting. You have advantage on CONsaving throws whose actual purpose is maintaining concentration on a spell you are sustaining. This includes a real damage-triggered concentration save or another explicit CONsave to retain that spell, and no other roll merely because losing it might later break concentration. Use the existing damage-event timing and one-save procedure; temporaryHP absorption and actual damage consequences retain their governing definitions. Ordinary nonproficient-armor disadvantage or another actual disadvantage cancels the advantage normally; neither produces additional dice. A source-specific flat concentration bonus such as the proposed Resilient Mind applies separately if genuinely eligible under its own rule. WoundCONsaves,death saves,ordinary Strain/Exhaustion saves and nonspell concentration checks do not qualify simply because this creature also casts spells. The sole printed effect grants no occupied-hand Spermission,Reaction spell,reaction attack,automatic success or second concentration slot.

### Original-position authored review references

```json
[
  {
    "id": "MF-31-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/60"
  },
  {
    "id": "MF-31-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json",
      "bytes": 1210639,
      "sha256": "acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2"
    },
    "pointer": "/originalCaseReviews/61"
  }
]
```
