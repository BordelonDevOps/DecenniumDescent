# Combat — source reconciliation

Derived complete-text assembly 106; exact parent review and integration pending.

Original source decisions below are historical receipts. The complete current candidate procedure and linked complete case review control this derived reading.

## CF-01 — Armor Crusher

### Complete original object

```json
{
  "id": "armor_crusher",
  "name": "Armor Crusher",
  "description": "Repeated, well-placed blows find the seams in an enemy's armor and press the advantage.",
  "prerequisite": "Level 7",
  "effect": "Once per turn when you deal bludgeoning, piercing, or slashing damage, reduce the target’s AC by 1 until the start of your next turn. This does not stack with itself.",
  "type": "Combat",
  "legacyEffect": "Ignore 10% enemy armor",
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
"Define damage-packet eligibility, target/armor requirements, zero damage, application after the triggering damage, once-per-turn cadence and nonstacking across multiple owners. Does it alter an AC formula or a separate debuff layer, and what expires at the next regular start?"
```

### Preserved original source direction (historical)

```json
{
  "featId": "armor_crusher",
  "name": "Armor Crusher",
  "cohort": "combat",
  "questionId": "CF-01",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/0",
  "originalQuestion": "Define damage-packet eligibility, target/armor requirements, zero damage, application after the triggering damage, once-per-turn cadence and nonstacking across multiple owners. Does it alter an AC formula or a separate debuff layer, and what expires at the next regular start?",
  "originalSourceObject": {
    "id": "armor_crusher",
    "name": "Armor Crusher",
    "description": "Repeated, well-placed blows find the seams in an enemy's armor and press the advantage.",
    "prerequisite": "Level 7",
    "effect": "Once per turn when you deal bludgeoning, piercing, or slashing damage, reduce the target’s AC by 1 until the start of your next turn. This does not stack with itself.",
    "type": "Combat",
    "legacyEffect": "Ignore 10% enemy armor",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "1ee5ab207846c56ee92a8922a85ea4594ab850157cb032b05abb456dcbcd3a20",
  "submittedProcedure": "After one of your own direct damage events deals positive resolved bludgeoning, piercing or slashing damage to a creature, you may apply Armor Crusher once that turn. NEW: any actual creature defense qualifies, including natural armor and unarmored defense; the feat does not require a removable suit. The triggering event finishes against its original AC. Apply a separate −1 AC layer through your next original regular start. Further applications from any owner never sum below −1; retain independent expiry records, so the penalty persists while at least one remains. Fully prevented damage does not trigger; temp-HP absorption of a positive resolved packet still does. Copied, reflected, transferred and ongoing periodic damage do not generate applications. Do not damage or regrade armor.",
  "submittedNewChoices": "Creature-wide scope, direct-event eligibility, single identity family across owners, and expiry arbitration.",
  "submittedWorkedCases": [
    "An AC17 creature takes 4 piercing damage: the triggering attack used17; later attacks use16 until expiry.",
    "Two owners apply the feat: AC falls only1. The later record can keep that same −1 after the first expires."
  ],
  "decision": "Retain the full CF-01 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Creature-wide scope, direct-event eligibility, single identity family across owners, and expiry arbitration.",
  "completeAuthoringProcedure": "After one of your own direct damage events deals positive resolved bludgeoning, piercing or slashing damage to a creature, you may apply Armor Crusher once that turn. NEW: any actual creature defense qualifies, including natural armor and unarmored defense; the feat does not require a removable suit. The triggering event finishes against its original AC. Apply a separate −1 AC layer through your next original regular start. Further applications from any owner never sum below −1; retain independent expiry records, so the penalty persists while at least one remains. Fully prevented damage does not trigger; temp-HP absorption of a positive resolved packet still does. Copied, reflected, transferred and ongoing periodic damage do not generate applications. Do not damage or regrade armor.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An AC17 creature takes 4 piercing damage: the triggering attack used17; later attacks use16 until expiry.",
    "Two owners apply the feat: AC falls only1. The later record can keep that same −1 after the first expires."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After one of your own direct damage events deals positive resolved bludgeoning, piercing or slashing damage to a creature, you may apply Armor Crusher once that turn. NEW: any actual creature defense qualifies, including natural armor and unarmored defense; the feat does not require a removable suit. The triggering event finishes against its original AC. Apply a separate −1 AC layer through your next original regular start. Further applications from any owner never sum below −1; retain independent expiry records, so the penalty persists while at least one remains. Fully prevented damage does not trigger; temp-HP absorption of a positive resolved packet still does. Copied, reflected, transferred and ongoing periodic damage do not generate applications. Do not damage or regrade armor.

### Original-position authored review references

```json
[
  {
    "id": "CF-01-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/0"
  },
  {
    "id": "CF-01-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/1"
  }
]
```

## CF-02 — Battlefield Commander

### Complete original object

```json
{
  "id": "battlefield_commander",
  "name": "Battlefield Commander",
  "description": "A commanding voice directs three nearby allies into more favorable positions when the line must shift.",
  "prerequisite": "Charisma 15+, Level 12",
  "effect": "As an action, choose up to three willing allies within 30 feet who can hear you. Each may use its reaction to move up to half its speed without provoking opportunity attacks. You regain this use after a short rest.",
  "type": "Combat",
  "legacyEffect": "Reposition 3 allies within 30ft",
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
"Bind Action, hearing/willingness, three unique allies, Reaction expenditure, half-current-Speed separate budget, terrain costs, sequential placement, interruption and opportunity immunity. Define short-rest recovery and no movement at Speed0."
```

### Preserved original source direction (historical)

```json
{
  "featId": "battlefield_commander",
  "name": "Battlefield Commander",
  "cohort": "combat",
  "questionId": "CF-02",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/1",
  "originalQuestion": "Bind Action, hearing/willingness, three unique allies, Reaction expenditure, half-current-Speed separate budget, terrain costs, sequential placement, interruption and opportunity immunity. Define short-rest recovery and no movement at Speed0.",
  "originalSourceObject": {
    "id": "battlefield_commander",
    "name": "Battlefield Commander",
    "description": "A commanding voice directs three nearby allies into more favorable positions when the line must shift.",
    "prerequisite": "Charisma 15+, Level 12",
    "effect": "As an action, choose up to three willing allies within 30 feet who can hear you. Each may use its reaction to move up to half its speed without provoking opportunity attacks. You regain this use after a short rest.",
    "type": "Combat",
    "legacyEffect": "Reposition 3 allies within 30ft",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "151c49a40df01958c7b696c226a58669b7ba254d2f92a3eab1e208e292944911",
  "submittedProcedure": "Action, once per short rest: choose one to three other willing allied creatures within30ft who can hear and understand the brief directive. Lock recipients and their order, spend the use, then resolve each sequentially. Each may spend its own available Reaction immediately for a separate floor(current relevant Speed/2)-ft movement-cost budget. Recheck hearing, willingness, position and capability at that recipient's resolution. Terrain and hazards apply; movement from this instruction provokes no opportunity attacks. Speed0 gives no movement. Declining or losing eligibility grants no replacement recipient and does not refund the commander; a recipient that does not move need not spend a Reaction. No ordinary movement/Action/BA resource is restored.",
  "submittedNewChoices": "Understanding requirement, ordered locked recipients, half-Speed cost budget and skip rules.",
  "submittedWorkedCases": [
    "Speed30 on normal ground allows15ft. On difficult ground the same15-point budget allows only one complete5ft square on a grid.",
    "The second ally is incapacitated by a hazard while the first moves: skip that ally; the third may still react if legal."
  ],
  "decision": "Keep actual source ally wording including self, with original target/sensory/budget conditions; no generalized automatic self-target for inherently two-person effects.",
  "completeAuthoringProcedure": "Action, once per short rest: choose one to three willing allied creatures, including yourself, within30ft who can hear and understand the brief directive. Lock recipients and their order, spend the use, then resolve each sequentially. Each may spend its own available Reaction immediately for a separate floor(current relevant Speed/2)-ft movement-cost budget. Recheck hearing, willingness, position and capability at that recipient's resolution. Terrain and hazards apply; movement from this instruction provokes no opportunity attacks. Speed0 gives no movement. Declining or losing eligibility grants no replacement recipient and does not refund the commander; a recipient that does not move need not spend a Reaction. No ordinary movement/Action/BA resource is restored.\nSOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "The commander selects themselves and two willing hearing allies, spends the Action and short-rest use, then resolves their chosen order. Each moving recipient pays their own Reaction for half-current-Speed movement; the commander has no extra Reaction.",
    "The second ally is incapacitated by a hazard while the first moves: skip that ally; the third may still react if legal."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Action, once per short rest: choose one to three willing allied creatures, including yourself, within30ft who can hear and understand the brief directive. Lock recipients and their order, spend the use, then resolve each sequentially. Each may spend its own available Reaction immediately for a separate floor(current relevant Speed/2)-ft movement-cost budget. Recheck hearing, willingness, position and capability at that recipient's resolution. Terrain and hazards apply; movement from this instruction provokes no opportunity attacks. Speed0 gives no movement. Declining or losing eligibility grants no replacement recipient and does not refund the commander; a recipient that does not move need not spend a Reaction. No ordinary movement/Action/BA resource is restored.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.

### Original-position authored review references

```json
[
  {
    "id": "CF-02-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/2"
  },
  {
    "id": "CF-02-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/3"
  },
  {
    "id": "FA-07",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/additionalBoundaryReviews/0"
  }
]
```

## CF-03 — Berserker Rage

### Complete original object

```json
{
  "id": "berserker_rage",
  "name": "Berserker Rage",
  "description": "A powerful fighter accepts a brief loss of defense to drive a ten-second burst of damage.",
  "prerequisite": "Strength 16+, Level 9",
  "effect": "As a bonus action, enter a rage for 2 rounds. Your weapon attacks deal one additional weapon damage die, but your AC is reduced by 2. You regain this use after a short rest.",
  "type": "Combat",
  "legacyEffect": "+25% damage for 10s, -10% AC",
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
"Define activation and exact two-round clock, weapon-die selection for multi-die/versatile/natural attacks, critical doubling and AC penalty arbitration. Establish whether this counts as the separate Berserker feat's rage for Frenzied Rage, without aliasing their sources."
```

### Preserved original source direction (historical)

```json
{
  "featId": "berserker_rage",
  "name": "Berserker Rage",
  "cohort": "combat",
  "questionId": "CF-03",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/2",
  "originalQuestion": "Define activation and exact two-round clock, weapon-die selection for multi-die/versatile/natural attacks, critical doubling and AC penalty arbitration. Establish whether this counts as the separate Berserker feat's rage for Frenzied Rage, without aliasing their sources.",
  "originalSourceObject": {
    "id": "berserker_rage",
    "name": "Berserker Rage",
    "description": "A powerful fighter accepts a brief loss of defense to drive a ten-second burst of damage.",
    "prerequisite": "Strength 16+, Level 9",
    "effect": "As a bonus action, enter a rage for 2 rounds. Your weapon attacks deal one additional weapon damage die, but your AC is reduced by 2. You regain this use after a short rest.",
    "type": "Combat",
    "legacyEffect": "+25% damage for 10s, -10% AC",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "a0ff95f3780aa097778d72e4a8bd81f409b84ba5e599abbd4948912957b17405",
  "submittedProcedure": "Bonus Action, once per short rest: enter this distinct feat rage through your second future original regular-start marker; outside initiative12elapsed seconds. Each qualifying weapon attack hit during it adds one base weapon damage die, doubled as part of a critical. Melee and ranged weapon attacks qualify because the current effect says weapon attacks; unarmed attacks do not, and natural attacks require an actual weapon profile. Apply its −2 AC continuously. Repeated same identity cannot stack; independently active Aggressive stance's −2 AC also applies. NEW the rage ends early if you become Incapacitated. This is a rage for Frenzied Rage's operating trigger, but acquiring this feat alone does not satisfy Frenzied Rage's separately printed Berserker-feat-or-class-rage prerequisite. It supplies no +2 rage damage to replace and no resistance or spell ban.",
  "submittedNewChoices": "Exact self-buff clock, all weapon scope, die selection, incapacitation endpoint and explicit distinction between operational rage and acquisition gate.",
  "submittedWorkedCases": [
    "A 2d6 greatsword hit gains1d6; a critical rolls6d6 in total, plus unchanged flat modifiers.",
    "Activation on own turn4 expires at start6, even if turn5 is skipped; an extra turn does not extend it."
  ],
  "decision": "Retain the full CF-03 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Exact self-buff clock, all weapon scope, die selection, incapacitation endpoint and explicit distinction between operational rage and acquisition gate.",
  "completeAuthoringProcedure": "Bonus Action, once per short rest: enter this distinct feat rage through your second future original regular-start marker; outside initiative12elapsed seconds. Each qualifying weapon attack hit during it adds one base weapon damage die, doubled as part of a critical. Melee and ranged weapon attacks qualify because the current effect says weapon attacks; unarmed attacks do not, and natural attacks require an actual weapon profile. Apply its −2 AC continuously. Repeated same identity cannot stack; independently active Aggressive stance's −2 AC also applies. NEW the rage ends early if you become Incapacitated. This is a rage for Frenzied Rage's operating trigger, but acquiring this feat alone does not satisfy Frenzied Rage's separately printed Berserker-feat-or-class-rage prerequisite. It supplies no +2 rage damage to replace and no resistance or spell ban.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A 2d6 greatsword hit gains1d6; a critical rolls6d6 in total, plus unchanged flat modifiers.",
    "Activation on own turn4 expires at start6, even if turn5 is skipped; an extra turn does not extend it."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Bonus Action, once per short rest: enter this distinct feat rage through your second future original regular-start marker; outside initiative12elapsed seconds. Each qualifying weapon attack hit during it adds one base weapon damage die, doubled as part of a critical. Melee and ranged weapon attacks qualify because the current effect says weapon attacks; unarmed attacks do not, and natural attacks require an actual weapon profile. Apply its −2 AC continuously. Repeated same identity cannot stack; independently active Aggressive stance's −2 AC also applies. NEW the rage ends early if you become Incapacitated. This is a rage for Frenzied Rage's operating trigger, but acquiring this feat alone does not satisfy Frenzied Rage's separately printed Berserker-feat-or-class-rage prerequisite. It supplies no +2 rage damage to replace and no resistance or spell ban.

### Original-position authored review references

```json
[
  {
    "id": "CF-03-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/4"
  },
  {
    "id": "CF-03-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/5"
  }
]
```

## CF-04 — Bleeding Edge

### Complete original object

```json
{
  "id": "bleeding_edge",
  "name": "Bleeding Edge",
  "description": "A precise melee critical opens a wound that carries the feat's listed bleed effect.",
  "prerequisite": "Dexterity 14+, Melee",
  "effect": "When you score a critical hit with a melee weapon, the target bleeds for 1d4 damage at the start of each of its turns for 3 rounds. A creature can use an action to stop the bleeding with a successful Medicine check against DC 10 + your proficiency bonus.",
  "type": "Combat",
  "legacyEffect": "Adds bleed effect on crit",
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
"Assign an explicit periodic identity/family, damage type, three-round/tick clock, repeated applications and multiple owners. Resolve bleedable-body permission, Medicine action/range/hands and whether stopping this rider also affects unrelated Bleeding families."
```

### Preserved original source direction (historical)

```json
{
  "featId": "bleeding_edge",
  "name": "Bleeding Edge",
  "cohort": "combat",
  "questionId": "CF-04",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/3",
  "originalQuestion": "Assign an explicit periodic identity/family, damage type, three-round/tick clock, repeated applications and multiple owners. Resolve bleedable-body permission, Medicine action/range/hands and whether stopping this rider also affects unrelated Bleeding families.",
  "originalSourceObject": {
    "id": "bleeding_edge",
    "name": "Bleeding Edge",
    "description": "A precise melee critical opens a wound that carries the feat's listed bleed effect.",
    "prerequisite": "Dexterity 14+, Melee",
    "effect": "When you score a critical hit with a melee weapon, the target bleeds for 1d4 damage at the start of each of its turns for 3 rounds. A creature can use an action to stop the bleeding with a successful Medicine check against DC 10 + your proficiency bonus.",
    "type": "Combat",
    "legacyEffect": "Adds bleed effect on crit",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "f16e77a7825403a983424e87863cfa041b1df6c69df73a002672754e67c79c63",
  "submittedProcedure": "When your actual melee weapon attack critically hits a living non-bloodless creature, after the hit resolves apply feat.bleeding-edge in family.bleeding, stack group feat.bleeding-edge:<owner>. NEW physical type is slashing. It deals1d4 at each of the next three future target regular starts, then ends; applying during a start never adds an immediate tick. Same-owner reapplication refreshes three remaining ticks without adding a second instance; different owners retain competing groups under the existing highest-expected-damage/earliest-application arbitration. Losing due groups still spend ticks. Snapshot the ending Medicine DC10+your PB at application. Victim or adjacent helper may spend an Action with one usable hand and access to the injury, selecting this record before WIS Medicine; success ends that record only. No kit charge is required by this feat. Retain generic positive-potential magical-healing automatic cure for this ordinary Bleeding record. Critical dice do not double later periodic damage; no resource/attack procs from ticks. No positive-damage prerequisite is added beyond actual hit and bleedable body.",
  "submittedNewChoices": "Registered family/type/three-start clock, refresh, body gate and ordinary magical-healing endpoint.",
  "submittedWorkedCases": [
    "At PB3, an adjacent Medicine total13 ends one selected owner's record; another owner's independent record remains.",
    "A concurrent stronger Bleed wins two due starts. Bleeding Edge still uses those two ticks and has only one left."
  ],
  "decision": "Retain the full CF-04 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Registered family/type/three-start clock, refresh, body gate and ordinary magical-healing endpoint.",
  "completeAuthoringProcedure": "When your actual melee weapon attack critically hits a living non-bloodless creature, after the hit resolves apply feat.bleeding-edge in family.bleeding, stack group feat.bleeding-edge:<owner>. NEW physical type is slashing. It deals1d4 at each of the next three future target regular starts, then ends; applying during a start never adds an immediate tick. Same-owner reapplication refreshes three remaining ticks without adding a second instance; different owners retain competing groups under the existing highest-expected-damage/earliest-application arbitration. Losing due groups still spend ticks. Snapshot the ending Medicine DC10+your PB at application. Victim or adjacent helper may spend an Action with one usable hand and access to the injury, selecting this record before WIS Medicine; success ends that record only. No kit charge is required by this feat. Retain generic positive-potential magical-healing automatic cure for this ordinary Bleeding record. Critical dice do not double later periodic damage; no resource/attack procs from ticks. No positive-damage prerequisite is added beyond actual hit and bleedable body.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "At PB3, an adjacent Medicine total13 ends one selected owner's record; another owner's independent record remains.",
    "A concurrent stronger Bleed wins two due starts. Bleeding Edge still uses those two ticks and has only one left."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

When your actual melee weapon attack critically hits a living non-bloodless creature, after the hit resolves apply feat.bleeding-edge in family.bleeding, stack group feat.bleeding-edge:<owner>. NEW physical type is slashing. It deals1d4 at each of the next three future target regular starts, then ends; applying during a start never adds an immediate tick. Same-owner reapplication refreshes three remaining ticks without adding a second instance; different owners retain competing groups under the existing highest-expected-damage/earliest-application arbitration. Losing due groups still spend ticks. Snapshot the ending Medicine DC10+your PB at application. Victim or adjacent helper may spend an Action with one usable hand and access to the injury, selecting this record before WIS Medicine; success ends that record only. No kit charge is required by this feat. Retain generic positive-potential magical-healing automatic cure for this ordinary Bleeding record. Critical dice do not double later periodic damage; no resource/attack procs from ticks. No positive-damage prerequisite is added beyond actual hit and bleedable body.

### Original-position authored review references

```json
[
  {
    "id": "CF-04-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/6"
  },
  {
    "id": "CF-04-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/7"
  }
]
```

## CF-05 — Brace for Impact

### Complete original object

```json
{
  "id": "brace_for_impact",
  "name": "Brace for Impact",
  "description": "A resilient combatant who holds position braces for the listed damage resistance.",
  "prerequisite": "Constitution 14+",
  "effect": "If you have not moved since the start of your turn, use a reaction when you take damage to reduce it by your proficiency bonus + Constitution modifier.",
  "type": "Combat",
  "legacyEffect": "+20% damage resistance if stationary",
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
"Define moved-since-start across forced movement, teleport and extra turns; reaction timing before/after mitigation; PB+CON minimum; one packet versus area or split damage; actual damaged recipient; and interaction with transfer/prevention rules."
```

### Preserved original source direction (historical)

```json
{
  "featId": "brace_for_impact",
  "name": "Brace for Impact",
  "cohort": "combat",
  "questionId": "CF-05",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/4",
  "originalQuestion": "Define moved-since-start across forced movement, teleport and extra turns; reaction timing before/after mitigation; PB+CON minimum; one packet versus area or split damage; actual damaged recipient; and interaction with transfer/prevention rules.",
  "originalSourceObject": {
    "id": "brace_for_impact",
    "name": "Brace for Impact",
    "description": "A resilient combatant who holds position braces for the listed damage resistance.",
    "prerequisite": "Constitution 14+",
    "effect": "If you have not moved since the start of your turn, use a reaction when you take damage to reduce it by your proficiency bonus + Constitution modifier.",
    "type": "Combat",
    "legacyEffect": "+20% damage resistance if stationary",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "9cff29ca5e6cdf569d0ba4c5fe110333462520ef30db3fe844b49671b8fee882",
  "submittedProcedure": "If you have undergone no actual positional displacement since your most recent original regular-turn start, spend Reaction when a direct damage event would damage you. NEW all voluntary, forced, carried and teleport displacement counts, even returning to the same square; standing, turning in place and a failed move do not. Before your first encounter turn, count displacement since encounter entry. Reduce one whole resolved incoming event by max(0,PB+CON modifier), after ordinary passive defenses and before temporary HP. Allocate reduction across components in their stable order, never below0; one attack's fire and slashing are one event, separate attacks are not. Do not re-mitigate a transferred packet that explicitly forbids recipient mitigation. This affects damage only, not attached conditions, sacrificed HP or state assignment. Paying with a zero reduction is allowed but does not create healing.",
  "submittedNewChoices": "Displacement receipt, whole-event post-defense timing, nonnegative reduction and stable split allocation.",
  "submittedWorkedCases": [
    "PB3/CON2 reduces resolved8 to3 before tempHP; it does not subtract5 independently from each component.",
    "You were pushed5ft and then returned5ft after your start. You cannot use the feat before the next regular start."
  ],
  "decision": "Retain the full CF-05 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Displacement receipt, whole-event post-defense timing, nonnegative reduction and stable split allocation.",
  "completeAuthoringProcedure": "If you have undergone no actual positional displacement since your most recent original regular-turn start, spend Reaction when a direct damage event would damage you. NEW all voluntary, forced, carried and teleport displacement counts, even returning to the same square; standing, turning in place and a failed move do not. Before your first encounter turn, count displacement since encounter entry. Reduce one whole resolved incoming event by max(0,PB+CON modifier), after ordinary passive defenses and before temporary HP. Allocate reduction across components in their stable order, never below0; one attack's fire and slashing are one event, separate attacks are not. Do not re-mitigate a transferred packet that explicitly forbids recipient mitigation. This affects damage only, not attached conditions, sacrificed HP or state assignment. Paying with a zero reduction is allowed but does not create healing.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "PB3/CON2 reduces resolved8 to3 before tempHP; it does not subtract5 independently from each component.",
    "You were pushed5ft and then returned5ft after your start. You cannot use the feat before the next regular start."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

If you have undergone no actual positional displacement since your most recent original regular-turn start, spend Reaction when a direct damage event would damage you. NEW all voluntary, forced, carried and teleport displacement counts, even returning to the same square; standing, turning in place and a failed move do not. Before your first encounter turn, count displacement since encounter entry. Reduce one whole resolved incoming event by max(0,PB+CON modifier), after ordinary passive defenses and before temporary HP. Allocate reduction across components in their stable order, never below0; one attack's fire and slashing are one event, separate attacks are not. Do not re-mitigate a transferred packet that explicitly forbids recipient mitigation. This affects damage only, not attached conditions, sacrificed HP or state assignment. Paying with a zero reduction is allowed but does not create healing.

### Original-position authored review references

```json
[
  {
    "id": "CF-05-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/8"
  },
  {
    "id": "CF-05-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/9"
  }
]
```

## CF-06 — Break Line

### Complete original object

```json
{
  "id": "break_line",
  "name": "Break Line",
  "description": "An agile veteran slips through the enemy's frontline zone without treating it as an obstacle.",
  "prerequisite": "Dexterity 15+, Level 10",
  "effect": "Once per turn, you may move through the space of one hostile creature no more than one size larger than you. That creature may make an opportunity attack; on a miss, you complete the movement.",
  "type": "Combat",
  "legacyEffect": "Ignore enemy frontline zone",
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
"Define ordinary movement cost, occupied-space entry/exit and size limit; when the special opportunity attack occurs, who can make it, Reaction cost, declined/unavailable attack, hit consequence and legal stopping space. Do not leave passage dependent on an attack that cannot occur."
```

### Preserved original source direction (historical)

```json
{
  "featId": "break_line",
  "name": "Break Line",
  "cohort": "combat",
  "questionId": "CF-06",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/5",
  "originalQuestion": "Define ordinary movement cost, occupied-space entry/exit and size limit; when the special opportunity attack occurs, who can make it, Reaction cost, declined/unavailable attack, hit consequence and legal stopping space. Do not leave passage dependent on an attack that cannot occur.",
  "originalSourceObject": {
    "id": "break_line",
    "name": "Break Line",
    "description": "An agile veteran slips through the enemy's frontline zone without treating it as an obstacle.",
    "prerequisite": "Dexterity 15+, Level 10",
    "effect": "Once per turn, you may move through the space of one hostile creature no more than one size larger than you. That creature may make an opportunity attack; on a miss, you complete the movement.",
    "type": "Combat",
    "legacyEffect": "Ignore enemy frontline zone",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "a99d645d60e3e449a5e02b1129a9bc743f29695ca622ab6f9350e1f365cb7615",
  "submittedProcedure": "Once per turn during your own legal voluntary movement, declare crossing one hostile creature's occupied space whose size is no more than one category larger. You must have enough ordinary remaining movement cost and a visible or known legal unoccupied exit to traverse its entire occupied footprint; occupied terrain costs at least difficult. Before first entry, that creature may spend its Reaction for one legal melee opportunity attack against you, even though you are entering rather than leaving. All actual reaction, sight, reach and opportunity-immunity restrictions apply. If it hits, this passage fails: remain in your last legal outside space, spend the first attempted entry step's cost and the feat use. The hit's other consequences resolve normally. If it misses, declines, cannot attack or its opportunity attack is suppressed, proceed, paying actual traversal costs. Recheck the exit after interruptions; if traversal becomes impossible before entry, stay outside and spend the committed use. Do not willingly start a traversal without a complete legal route. Other creatures may make normal opportunity attacks. This does not shove or phase through a creature.",
  "submittedNewChoices": "Pre-entry special opportunity trigger, declined/unavailable success, hit stops passage, full-footprint route and committed step cost.",
  "submittedWorkedCases": [
    "A Medium rogue has20 movement cost left and crosses one Medium hostile square for10 then exits for5. The guard has no Reaction, so passage succeeds.",
    "The guard's legal special attack hits. The rogue remains before the occupied square and spends10 cost for the attempted difficult entry; damage and the once-turn use remain."
  ],
  "decision": "Retain the full CF-06 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Pre-entry special opportunity trigger, declined/unavailable success, hit stops passage, full-footprint route and committed step cost.",
  "completeAuthoringProcedure": "Once per turn during your own legal voluntary movement, declare crossing one hostile creature's occupied space whose size is no more than one category larger. You must have enough ordinary remaining movement cost and a visible or known legal unoccupied exit to traverse its entire occupied footprint; occupied terrain costs at least difficult. Before first entry, that creature may spend its Reaction for one legal melee opportunity attack against you, even though you are entering rather than leaving. All actual reaction, sight, reach and opportunity-immunity restrictions apply. If it hits, this passage fails: remain in your last legal outside space, spend the first attempted entry step's cost and the feat use. The hit's other consequences resolve normally. If it misses, declines, cannot attack or its opportunity attack is suppressed, proceed, paying actual traversal costs. Recheck the exit after interruptions; if traversal becomes impossible before entry, stay outside and spend the committed use. Do not willingly start a traversal without a complete legal route. Other creatures may make normal opportunity attacks. This does not shove or phase through a creature.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A Medium rogue has20 movement cost left and crosses one Medium hostile square for10 then exits for5. The guard has no Reaction, so passage succeeds.",
    "The guard's legal special attack hits. The rogue remains before the occupied square and spends10 cost for the attempted difficult entry; damage and the once-turn use remain."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per turn during your own legal voluntary movement, declare crossing one hostile creature's occupied space whose size is no more than one category larger. You must have enough ordinary remaining movement cost and a visible or known legal unoccupied exit to traverse its entire occupied footprint; occupied terrain costs at least difficult. Before first entry, that creature may spend its Reaction for one legal melee opportunity attack against you, even though you are entering rather than leaving. All actual reaction, sight, reach and opportunity-immunity restrictions apply. If it hits, this passage fails: remain in your last legal outside space, spend the first attempted entry step's cost and the feat use. The hit's other consequences resolve normally. If it misses, declines, cannot attack or its opportunity attack is suppressed, proceed, paying actual traversal costs. Recheck the exit after interruptions; if traversal becomes impossible before entry, stay outside and spend the committed use. Do not willingly start a traversal without a complete legal route. Other creatures may make normal opportunity attacks. This does not shove or phase through a creature.

### Original-position authored review references

```json
[
  {
    "id": "CF-06-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/10"
  },
  {
    "id": "CF-06-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/11"
  }
]
```

## CF-07 — Bull Rush

### Complete original object

```json
{
  "id": "bull_rush",
  "name": "Bull Rush",
  "description": "A strong combatant drives into a target, forcing the listed short displacement and knockdown.",
  "prerequisite": "Strength 14+",
  "effect": "When you hit with a melee attack after moving at least 10 feet straight toward the target, force it to make a Strength save (DC 8 + proficiency bonus + Strength modifier) or be pushed 5 feet and knocked prone. Once per turn.",
  "type": "Combat",
  "legacyEffect": "Knock target prone and move them 5ft",
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
"Bind qualifying melee attack types, straight continuous ten-foot movement, actual hit versus damage, cadence and save timing. Decide push and Prone independently where displacement is blocked, and any size/anchor limits not supplied by the feat."
```

### Preserved original source direction (historical)

```json
{
  "featId": "bull_rush",
  "name": "Bull Rush",
  "cohort": "combat",
  "questionId": "CF-07",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/6",
  "originalQuestion": "Bind qualifying melee attack types, straight continuous ten-foot movement, actual hit versus damage, cadence and save timing. Decide push and Prone independently where displacement is blocked, and any size/anchor limits not supplied by the feat.",
  "originalSourceObject": {
    "id": "bull_rush",
    "name": "Bull Rush",
    "description": "A strong combatant drives into a target, forcing the listed short displacement and knockdown.",
    "prerequisite": "Strength 14+",
    "effect": "When you hit with a melee attack after moving at least 10 feet straight toward the target, force it to make a Strength save (DC 8 + proficiency bonus + Strength modifier) or be pushed 5 feet and knocked prone. Once per turn.",
    "type": "Combat",
    "legacyEffect": "Knock target prone and move them 5ft",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "be0b0d320287f849cc3ec72cb765674427b851cff7cdbe23a17c39052b5767a2",
  "submittedProcedure": "Once per turn, after you hit with a melee attack immediately following at least10ft of your own continuous voluntary movement in a straight line directly toward that target, choose this rider. NEW the approach must occur on that same actual turn, without intervening attack, action, turn or teleport; forced/carried displacement does not count. Melee weapon, natural, unarmed and actual melee spell attacks qualify. Target makes STR save DC8+PB+your current STR modifier. On failure push it5ft directly away and separately apply Prone. NEW no additional size cap is added because the feat omits one; actual immovability, anatomy/support and condition immunities still apply. A wall can stop the push without preventing Prone. A hit dealing0 damage can trigger. Resolve normal damage before this rider; if no creature remains, no further effect. No additional Action cost.",
  "submittedNewChoices": "Continuous approach and turn scope, all melee attacks, no imported size ceiling, independent push/Prone.",
  "submittedWorkedCases": [
    "A hit after10ft straight approach produces a failed save. A wall blocks displacement but the target still falls Prone if eligible.",
    "A teleport of10ft followed by a hit does not meet the approach; neither does being carried forward by another actor."
  ],
  "decision": "Retain the full CF-07 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Continuous approach and turn scope, all melee attacks, no imported size ceiling, independent push/Prone.",
  "completeAuthoringProcedure": "Once per turn, after you hit with a melee attack immediately following at least10ft of your own continuous voluntary movement in a straight line directly toward that target, choose this rider. NEW the approach must occur on that same actual turn, without intervening attack, action, turn or teleport; forced/carried displacement does not count. Melee weapon, natural, unarmed and actual melee spell attacks qualify. Target makes STR save DC8+PB+your current STR modifier. On failure push it5ft directly away and separately apply Prone. NEW no additional size cap is added because the feat omits one; actual immovability, anatomy/support and condition immunities still apply. A wall can stop the push without preventing Prone. A hit dealing0 damage can trigger. Resolve normal damage before this rider; if no creature remains, no further effect. No additional Action cost.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A hit after10ft straight approach produces a failed save. A wall blocks displacement but the target still falls Prone if eligible.",
    "A teleport of10ft followed by a hit does not meet the approach; neither does being carried forward by another actor."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per turn, after you hit with a melee attack immediately following at least10ft of your own continuous voluntary movement in a straight line directly toward that target, choose this rider. NEW the approach must occur on that same actual turn, without intervening attack, action, turn or teleport; forced/carried displacement does not count. Melee weapon, natural, unarmed and actual melee spell attacks qualify. Target makes STR save DC8+PB+your current STR modifier. On failure push it5ft directly away and separately apply Prone. NEW no additional size cap is added because the feat omits one; actual immovability, anatomy/support and condition immunities still apply. A wall can stop the push without preventing Prone. A hit dealing0 damage can trigger. Resolve normal damage before this rider; if no creature remains, no further effect. No additional Action cost.

### Original-position authored review references

```json
[
  {
    "id": "CF-07-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/12"
  },
  {
    "id": "CF-07-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/13"
  }
]
```

## CF-08 — Cleaving Momentum

### Complete original object

```json
{
  "id": "cleaving_momentum",
  "name": "Cleaving Momentum",
  "description": "A heavy two-handed finishing blow carries its momentum into the listed follow-up attack.",
  "prerequisite": "Strength 16+, 2H Weapon",
  "effect": "When you reduce a hostile creature to 0 hit points with a melee weapon, make one melee weapon attack against another creature within reach as a bonus action.",
  "type": "Combat",
  "legacyEffect": "Free follow-up attack on kill",
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
"Bind the 2H Weapon prerequisite and whether the triggering/bonus attack must use it. Define hostile drop event, ordinary Bonus Action cost, same-turn window, another target, reach, death versus0HP and prevention of chained extra bonus actions."
```

### Preserved original source direction (historical)

```json
{
  "featId": "cleaving_momentum",
  "name": "Cleaving Momentum",
  "cohort": "combat",
  "questionId": "CF-08",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/7",
  "originalQuestion": "Bind the 2H Weapon prerequisite and whether the triggering/bonus attack must use it. Define hostile drop event, ordinary Bonus Action cost, same-turn window, another target, reach, death versus0HP and prevention of chained extra bonus actions.",
  "originalSourceObject": {
    "id": "cleaving_momentum",
    "name": "Cleaving Momentum",
    "description": "A heavy two-handed finishing blow carries its momentum into the listed follow-up attack.",
    "prerequisite": "Strength 16+, 2H Weapon",
    "effect": "When you reduce a hostile creature to 0 hit points with a melee weapon, make one melee weapon attack against another creature within reach as a bonus action.",
    "type": "Combat",
    "legacyEffect": "Free follow-up attack on kill",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "e25d090132b20c8782c770c342205e91e0b152a6bf66740572cea78806f71a3f",
  "submittedProcedure": "Acquire with STR16 and actual proficiency in a Two-Handed weapon. NEW triggering and follow-up attacks must both use an actual melee weapon wielded with two hands; a legal Versatile two-hand attack can operate the acquired feat. During your own turn, after your attack reduces a genuine hostile creature from positiveHP to0 after floors/replacements, you may spend your still-available Bonus Action before that turn ends for one melee weapon attack against a different creature in legal reach. Death is unnecessary; a surviving downed opponent qualifies. The second target need not be hostile under the printed another-creature wording. Normal damage, ammunition if relevant, hands and perception apply. No banked off-turn use and no additional Bonus Action; multiple drops only provide alternative triggers for that same wallet. Copied/periodic damage and reducing an already0 creature do not qualify.",
  "submittedNewChoices": "Two-hand operating restriction, positive-to-zero event and same-own-turn Bonus Action window.",
  "submittedWorkedCases": [
    "A greatsword drops a hostile to0 but the creature survives dying. One available BA can attack a second target.",
    "The follow-up also drops its target. There is no second Bonus Action and thus no chain of free attacks."
  ],
  "decision": "Retain the full CF-08 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Two-hand operating restriction, positive-to-zero event and same-own-turn Bonus Action window.",
  "completeAuthoringProcedure": "Acquire with STR16 and actual proficiency in a Two-Handed weapon. NEW triggering and follow-up attacks must both use an actual melee weapon wielded with two hands; a legal Versatile two-hand attack can operate the acquired feat. During your own turn, after your attack reduces a genuine hostile creature from positiveHP to0 after floors/replacements, you may spend your still-available Bonus Action before that turn ends for one melee weapon attack against a different creature in legal reach. Death is unnecessary; a surviving downed opponent qualifies. The second target need not be hostile under the printed another-creature wording. Normal damage, ammunition if relevant, hands and perception apply. No banked off-turn use and no additional Bonus Action; multiple drops only provide alternative triggers for that same wallet. Copied/periodic damage and reducing an already0 creature do not qualify.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A greatsword drops a hostile to0 but the creature survives dying. One available BA can attack a second target.",
    "The follow-up also drops its target. There is no second Bonus Action and thus no chain of free attacks."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Acquire with STR16 and actual proficiency in a Two-Handed weapon. NEW triggering and follow-up attacks must both use an actual melee weapon wielded with two hands; a legal Versatile two-hand attack can operate the acquired feat. During your own turn, after your attack reduces a genuine hostile creature from positiveHP to0 after floors/replacements, you may spend your still-available Bonus Action before that turn ends for one melee weapon attack against a different creature in legal reach. Death is unnecessary; a surviving downed opponent qualifies. The second target need not be hostile under the printed another-creature wording. Normal damage, ammunition if relevant, hands and perception apply. No banked off-turn use and no additional Bonus Action; multiple drops only provide alternative triggers for that same wallet. Copied/periodic damage and reducing an already0 creature do not qualify.

### Original-position authored review references

```json
[
  {
    "id": "CF-08-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/14"
  },
  {
    "id": "CF-08-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/15"
  }
]
```

## CF-09 — Close Quarters Combat

### Complete original object

```json
{
  "id": "close_quarters_combat",
  "name": "Close Quarters Combat",
  "description": "Quick control of a cramped melee keeps a ranged attack from drawing the listed opportunity attack.",
  "prerequisite": "Dexterity 14+",
  "effect": "Making a ranged attack while a hostile creature is within 5 feet does not impose disadvantage, and the attack does not provoke an opportunity attack.",
  "type": "Combat",
  "legacyEffect": "No AoO when using ranged in melee",
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
"Resolve ranged weapon versus spell attacks and which disadvantage sources are removed. Identify any actual attack-generated opportunity trigger in current combat rules; do not invent a universal ranged-attack opportunity penalty just to remove it."
```

### Preserved original source direction (historical)

```json
{
  "featId": "close_quarters_combat",
  "name": "Close Quarters Combat",
  "cohort": "combat",
  "questionId": "CF-09",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/8",
  "originalQuestion": "Resolve ranged weapon versus spell attacks and which disadvantage sources are removed. Identify any actual attack-generated opportunity trigger in current combat rules; do not invent a universal ranged-attack opportunity penalty just to remove it.",
  "originalSourceObject": {
    "id": "close_quarters_combat",
    "name": "Close Quarters Combat",
    "description": "Quick control of a cramped melee keeps a ranged attack from drawing the listed opportunity attack.",
    "prerequisite": "Dexterity 14+",
    "effect": "Making a ranged attack while a hostile creature is within 5 feet does not impose disadvantage, and the attack does not provoke an opportunity attack.",
    "type": "Combat",
    "legacyEffect": "No AoO when using ranged in melee",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "9c8ed96bb98bf736358d8f62f125a55a8a08d792450b1ee4ea40f6c0589cc15e",
  "submittedProcedure": "Your ranged attacks ignore disadvantage caused specifically by a seeing, non-Incapacitated hostile creature within5ft of you. This covers ranged weapon and ranged spell attacks. It does not remove long-range, unseen-target, Prone, restrained or other independent disadvantage. If any other disadvantage remains, apply ordinary cancellation. Making that ranged attack does not itself provoke an opportunity attack from any source that explicitly uses making the ranged attack as its trigger; it does not suppress a separate spellcasting, movement or other legal trigger. Current generic combat creates no opportunity attack just for making a ranged attack; do not add such a penalty for other characters.",
  "submittedNewChoices": "All ranged attack scope and narrow attack-trigger immunity without inventing a general penalty.",
  "submittedWorkedCases": [
    "A nearby guard imposes the usual proximity disadvantage on a ray; this feat removes it.",
    "A long-range bow shot with an adjacent hostile still has long-range disadvantage, even though proximity disadvantage is removed."
  ],
  "decision": "Retain the full CF-09 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. All ranged attack scope and narrow attack-trigger immunity without inventing a general penalty.",
  "completeAuthoringProcedure": "Your ranged attacks ignore disadvantage caused specifically by a seeing, non-Incapacitated hostile creature within5ft of you. This covers ranged weapon and ranged spell attacks. It does not remove long-range, unseen-target, Prone, restrained or other independent disadvantage. If any other disadvantage remains, apply ordinary cancellation. Making that ranged attack does not itself provoke an opportunity attack from any source that explicitly uses making the ranged attack as its trigger; it does not suppress a separate spellcasting, movement or other legal trigger. Current generic combat creates no opportunity attack just for making a ranged attack; do not add such a penalty for other characters.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A nearby guard imposes the usual proximity disadvantage on a ray; this feat removes it.",
    "A long-range bow shot with an adjacent hostile still has long-range disadvantage, even though proximity disadvantage is removed."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Your ranged attacks ignore disadvantage caused specifically by a seeing, non-Incapacitated hostile creature within5ft of you. This covers ranged weapon and ranged spell attacks. It does not remove long-range, unseen-target, Prone, restrained or other independent disadvantage. If any other disadvantage remains, apply ordinary cancellation. Making that ranged attack does not itself provoke an opportunity attack from any source that explicitly uses making the ranged attack as its trigger; it does not suppress a separate spellcasting, movement or other legal trigger. Current generic combat creates no opportunity attack just for making a ranged attack; do not add such a penalty for other characters.

### Original-position authored review references

```json
[
  {
    "id": "CF-09-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/16"
  },
  {
    "id": "CF-09-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/17"
  }
]
```

## CF-10 — Combat Intuition

### Complete original object

```json
{
  "id": "combat_intuition",
  "name": "Combat Intuition",
  "description": "Alert instincts give a combatant the listed chance to evade an opponent's opening attack.",
  "prerequisite": "Wisdom 13+",
  "effect": "You cannot be surprised while conscious. During the first round of combat, gain +1 AC.",
  "type": "Combat",
  "legacyEffect": "+10% chance to dodge opening attack",
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
"Bind consciousness, surprise handling, first-round identity for late entrants/extra turns and the+1 AC layer. Resolve changing consciousness and already-existing surprise without granting extra turns or reactions."
```

### Preserved original source direction (historical)

```json
{
  "featId": "combat_intuition",
  "name": "Combat Intuition",
  "cohort": "combat",
  "questionId": "CF-10",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/9",
  "originalQuestion": "Bind consciousness, surprise handling, first-round identity for late entrants/extra turns and the+1 AC layer. Resolve changing consciousness and already-existing surprise without granting extra turns or reactions.",
  "originalSourceObject": {
    "id": "combat_intuition",
    "name": "Combat Intuition",
    "description": "Alert instincts give a combatant the listed chance to evade an opponent's opening attack.",
    "prerequisite": "Wisdom 13+",
    "effect": "You cannot be surprised while conscious. During the first round of combat, gain +1 AC.",
    "type": "Combat",
    "legacyEffect": "+10% chance to dodge opening attack",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "294742dcca678fbf0e7633ea72ad02d5d743152c04d0d63f13f279d1deb3d2d9",
  "submittedProcedure": "While conscious, you cannot be surprised. NEW this suppresses any still-active surprise action/reaction prohibition while consciousness lasts, without granting lost actions or retroactive turns; other conditions still restrict you. The underlying first-turn surprise schedule is retained if consciousness changes again. Gain+1 AC during the encounter's first numbered round only. A late entrant in that round gains it only for the remainder; entering in round2 does not create a personal first round. The +1 is one feat modifier and needs no action; no extra Reaction is granted when surprise is prevented, only access to the normal resource if otherwise available.",
  "submittedNewChoices": "Conscious suppression of existing surprise, encounter-wide round identity and ordinary resource preservation.",
  "submittedWorkedCases": [
    "A conscious owner in round1 is not surprised and has+1AC. An extra turn during round1 still has the same bonus.",
    "Joining combat in round3 grants no first-round AC, though conscious surprise prevention still applies."
  ],
  "decision": "Retain the full CF-10 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Conscious suppression of existing surprise, encounter-wide round identity and ordinary resource preservation.",
  "completeAuthoringProcedure": "While conscious, you cannot be surprised. NEW this suppresses any still-active surprise action/reaction prohibition while consciousness lasts, without granting lost actions or retroactive turns; other conditions still restrict you. The underlying first-turn surprise schedule is retained if consciousness changes again. Gain+1 AC during the encounter's first numbered round only. A late entrant in that round gains it only for the remainder; entering in round2 does not create a personal first round. The +1 is one feat modifier and needs no action; no extra Reaction is granted when surprise is prevented, only access to the normal resource if otherwise available.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A conscious owner in round1 is not surprised and has+1AC. An extra turn during round1 still has the same bonus.",
    "Joining combat in round3 grants no first-round AC, though conscious surprise prevention still applies."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

While conscious, you cannot be surprised. NEW this suppresses any still-active surprise action/reaction prohibition while consciousness lasts, without granting lost actions or retroactive turns; other conditions still restrict you. The underlying first-turn surprise schedule is retained if consciousness changes again. Gain+1 AC during the encounter's first numbered round only. A late entrant in that round gains it only for the remainder; entering in round2 does not create a personal first round. The +1 is one feat modifier and needs no action; no extra Reaction is granted when surprise is prevented, only access to the normal resource if otherwise available.

### Original-position authored review references

```json
[
  {
    "id": "CF-10-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/18"
  },
  {
    "id": "CF-10-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/19"
  }
]
```

## CF-11 — Combat Slide

### Complete original object

```json
{
  "id": "combat_slide",
  "name": "Combat Slide",
  "description": "An agile fighter shifts five feet and attacks as part of the same listed action.",
  "prerequisite": "Dexterity 13+",
  "effect": "Once on your turn, move 5 feet before or after a weapon attack without provoking an opportunity attack from the target of that attack.",
  "type": "Combat",
  "legacyEffect": "Move 5ft and attack as one action",
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
"Decide whether5ft is a separate budget or uses ordinary remaining movement; bind before/after one weapon attack, declared target, misses/cancellation, terrain, Speed0 and immunity from only that target. Define own-turn cadence across extra turns."
```

### Preserved original source direction (historical)

```json
{
  "featId": "combat_slide",
  "name": "Combat Slide",
  "cohort": "combat",
  "questionId": "CF-11",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/10",
  "originalQuestion": "Decide whether5ft is a separate budget or uses ordinary remaining movement; bind before/after one weapon attack, declared target, misses/cancellation, terrain, Speed0 and immunity from only that target. Define own-turn cadence across extra turns.",
  "originalSourceObject": {
    "id": "combat_slide",
    "name": "Combat Slide",
    "description": "An agile fighter shifts five feet and attacks as part of the same listed action.",
    "prerequisite": "Dexterity 13+",
    "effect": "Once on your turn, move 5 feet before or after a weapon attack without provoking an opportunity attack from the target of that attack.",
    "type": "Combat",
    "legacyEffect": "Move 5ft and attack as one action",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "3dfeaf635cbbece2dad12bc92799297b96eeb9778ce866421320941b0a75ef69",
  "submittedProcedure": "Once on your own turn, immediately before or after one weapon attack, move using a separate5ft movement-cost budget. NEW choose and declare the attack target before a pre-attack slide; ordinary attack range and other legality must hold after movement. You still pay the attack's normal Action/BA/Reaction source; the slide grants no attack. For pre-slide, reserve that attack, and if an interruption prevents it the slide and use remain spent. For post-slide, a hit or miss both qualify. Only the declared target cannot make opportunity attacks provoked by this movement; other foes may. Terrain costs, usable Speed, legal endpoints and inability to occupy another creature still apply. At Speed0 you may attack if otherwise legal but cannot slide. No banking or splitting the5ft into separate later moves.",
  "submittedNewChoices": "Separate5-point budget, reservation before attack, target-only immunity and interruption commitment.",
  "submittedWorkedCases": [
    "After missing a guard with a spear, move5ft on normal ground without that guard's opportunity attack.",
    "A difficult5ft grid square costs10. The slide's5-point budget cannot enter it, and the feat does not double its budget."
  ],
  "decision": "Retain the full CF-11 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Separate5-point budget, reservation before attack, target-only immunity and interruption commitment.",
  "completeAuthoringProcedure": "Once on your own turn, immediately before or after one weapon attack, move using a separate5ft movement-cost budget. NEW choose and declare the attack target before a pre-attack slide; ordinary attack range and other legality must hold after movement. You still pay the attack's normal Action/BA/Reaction source; the slide grants no attack. For pre-slide, reserve that attack, and if an interruption prevents it the slide and use remain spent. For post-slide, a hit or miss both qualify. Only the declared target cannot make opportunity attacks provoked by this movement; other foes may. Terrain costs, usable Speed, legal endpoints and inability to occupy another creature still apply. At Speed0 you may attack if otherwise legal but cannot slide. No banking or splitting the5ft into separate later moves.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "After missing a guard with a spear, move5ft on normal ground without that guard's opportunity attack.",
    "A difficult5ft grid square costs10. The slide's5-point budget cannot enter it, and the feat does not double its budget."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once on your own turn, immediately before or after one weapon attack, move using a separate5ft movement-cost budget. NEW choose and declare the attack target before a pre-attack slide; ordinary attack range and other legality must hold after movement. You still pay the attack's normal Action/BA/Reaction source; the slide grants no attack. For pre-slide, reserve that attack, and if an interruption prevents it the slide and use remain spent. For post-slide, a hit or miss both qualify. Only the declared target cannot make opportunity attacks provoked by this movement; other foes may. Terrain costs, usable Speed, legal endpoints and inability to occupy another creature still apply. At Speed0 you may attack if otherwise legal but cannot slide. No banking or splitting the5ft into separate later moves.

### Original-position authored review references

```json
[
  {
    "id": "CF-11-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/20"
  },
  {
    "id": "CF-11-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/21"
  }
]
```

## CF-12 — Crippling Strike

### Complete original object

```json
{
  "id": "crippling_strike",
  "name": "Crippling Strike",
  "description": "A Dexterity-trained melee combatant applies the listed movement reduction to an enemy.",
  "prerequisite": "Dexterity 14+, Melee",
  "effect": "Once per turn when you hit with a finesse or melee weapon, reduce the target’s speed by 10 feet until the start of your next turn.",
  "type": "Combat",
  "legacyEffect": "Reduces enemy movement by 50%",
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
"Resolve the printed finesse OR melee-weapon scope, including thrown finesse weapons. Define speed modes/floor, repeated/multiple-owner applications, once-per-turn cadence and expiry; do not silently replace with the Thief class's source-specific Slow."
```

### Preserved original source direction (historical)

```json
{
  "featId": "crippling_strike",
  "name": "Crippling Strike",
  "cohort": "combat",
  "questionId": "CF-12",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/11",
  "originalQuestion": "Resolve the printed finesse OR melee-weapon scope, including thrown finesse weapons. Define speed modes/floor, repeated/multiple-owner applications, once-per-turn cadence and expiry; do not silently replace with the Thief class's source-specific Slow.",
  "originalSourceObject": {
    "id": "crippling_strike",
    "name": "Crippling Strike",
    "description": "A Dexterity-trained melee combatant applies the listed movement reduction to an enemy.",
    "prerequisite": "Dexterity 14+, Melee",
    "effect": "Once per turn when you hit with a finesse or melee weapon, reduce the target’s speed by 10 feet until the start of your next turn.",
    "type": "Combat",
    "legacyEffect": "Reduces enemy movement by 50%",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "607400a76693a74f7b1bb40e71ade337081fc9cf8c3d00cf69e7e1509de4e178",
  "submittedProcedure": "Once per turn when your attack hits using a weapon with Finesse OR a weapon classified as melee, reduce the target's current applicable Speed modes by10ft, minimum0, through your next original regular start. NEW a thrown dagger qualifies by both its melee classification and Finesse, even though its attack is ranged; a thrown nonfinesse melee weapon also qualifies by the literal melee-weapon branch. A longbow does not. Do not require positive damage. Same-identity applications across owners do not sum; retain independent expiries for one −10 layer. Other distinct Speed modifiers follow their actual stacking rules; apply numeric changes before halving and retain spent movement cost. This is not the Thief's Slow condition and grants none of that source's other effects.",
  "submittedNewChoices": "Literal weapon-class OR property scope, all Speed modes, one family and modifier ordering.",
  "submittedWorkedCases": [
    "A thrown dagger hit lowers walking30 and flying40 to20 and30 until the owner's next regular start.",
    "Two owners hit with the feat: Speed30 becomes20, not10; separate expiry records preserve the one penalty."
  ],
  "decision": "Retain the full CF-12 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Literal weapon-class OR property scope, all Speed modes, one family and modifier ordering.",
  "completeAuthoringProcedure": "Once per turn when your attack hits using a weapon with Finesse OR a weapon classified as melee, reduce the target's current applicable Speed modes by10ft, minimum0, through your next original regular start. NEW a thrown dagger qualifies by both its melee classification and Finesse, even though its attack is ranged; a thrown nonfinesse melee weapon also qualifies by the literal melee-weapon branch. A longbow does not. Do not require positive damage. Same-identity applications across owners do not sum; retain independent expiries for one −10 layer. Other distinct Speed modifiers follow their actual stacking rules; apply numeric changes before halving and retain spent movement cost. This is not the Thief's Slow condition and grants none of that source's other effects.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A thrown dagger hit lowers walking30 and flying40 to20 and30 until the owner's next regular start.",
    "Two owners hit with the feat: Speed30 becomes20, not10; separate expiry records preserve the one penalty."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per turn when your attack hits using a weapon with Finesse OR a weapon classified as melee, reduce the target's current applicable Speed modes by10ft, minimum0, through your next original regular start. NEW a thrown dagger qualifies by both its melee classification and Finesse, even though its attack is ranged; a thrown nonfinesse melee weapon also qualifies by the literal melee-weapon branch. A longbow does not. Do not require positive damage. Same-identity applications across owners do not sum; retain independent expiries for one −10 layer. Other distinct Speed modifiers follow their actual stacking rules; apply numeric changes before halving and retain spent movement cost. This is not the Thief's Slow condition and grants none of that source's other effects.

### Original-position authored review references

```json
[
  {
    "id": "CF-12-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/22"
  },
  {
    "id": "CF-12-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/23"
  }
]
```

## CF-13 — Defensive Stance

### Complete original object

```json
{
  "id": "defensive_stance",
  "name": "Defensive Stance",
  "description": "You can adopt a defensive posture that greatly improves your protection.",
  "prerequisite": "Level 6",
  "effect": "+15% AC, can't move this turn",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Supply activation, duration, frequency and legal timing for the retained+15% AC and cannot-move-this-turn clause. Define percentage base, rounding and AC-family interaction, plus forced movement/teleport and stance competition. Any numeric conversion must be explicitly NEW."
```

### Preserved original source direction (historical)

```json
{
  "featId": "defensive_stance",
  "name": "Defensive Stance",
  "cohort": "combat",
  "questionId": "CF-13",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/12",
  "originalQuestion": "Supply activation, duration, frequency and legal timing for the retained+15% AC and cannot-move-this-turn clause. Define percentage base, rounding and AC-family interaction, plus forced movement/teleport and stance competition. Any numeric conversion must be explicitly NEW.",
  "originalSourceObject": {
    "id": "defensive_stance",
    "name": "Defensive Stance",
    "description": "You can adopt a defensive posture that greatly improves your protection.",
    "prerequisite": "Level 6",
    "effect": "+15% AC, can't move this turn",
    "type": "Combat",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "26972f24247d864e6492c39856400cea10241d3079f3d3669e111cab78894d4d",
  "submittedProcedure": "NEW complete activation: when choosing your stance at the start of a regular own turn before using any stance benefit or moving voluntarily, choose Defensive Stance instead of a normal stance. No Action; one stance choice. Through your next original regular start, add floor(15% of your otherwise-current AC), minimum0, to AC. Compute the base after actual armor/shield/DEX/flat bonuses/penalties but before this or any other percentage-AC bonus; no percent-on-percent multiplication. Recompute when that underlying base changes, including conditional Guard. You cannot voluntarily change position by Speed expenditure, teleport or a feature while the current regular turn lasts; linked extra turns also retain the movement restriction. Standing/dropping Prone is allowed if ordinary budget/capability permits. Forced displacement remains possible and does not end the stance. Off-turn voluntary Reaction movement after that turn is allowed; AC lasts to expiry. It cannot coexist with Aggressive, Guarded, Mobile, Focused or Carrying because it occupies their stance choice, not a free extra buff.",
  "submittedNewChoices": "Entire activation/stance slot/duration and percentage base; voluntary-only this-turn movement restriction, including teleport; retained15% numeric value.",
  "submittedWorkedCases": [
    "Underlying AC17 gains floor2.55=2, total19. The feat does not round to a3-point bonus.",
    "A forced push during the stance moves the owner normally. They cannot then voluntarily teleport during their turn, but the push does not remove AC."
  ],
  "decision": "Retain the full CF-13 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Entire activation/stance slot/duration and percentage base; voluntary-only this-turn movement restriction, including teleport; retained15% numeric value.",
  "completeAuthoringProcedure": "NEW complete activation: when choosing your stance at the start of a regular own turn before using any stance benefit or moving voluntarily, choose Defensive Stance instead of a normal stance. No Action; one stance choice. Through your next original regular start, add floor(15% of your otherwise-current AC), minimum0, to AC. Compute the base after actual armor/shield/DEX/flat bonuses/penalties but before this or any other percentage-AC bonus; no percent-on-percent multiplication. Recompute when that underlying base changes, including conditional Guard. You cannot voluntarily change position by Speed expenditure, teleport or a feature while the current regular turn lasts; linked extra turns also retain the movement restriction. Standing/dropping Prone is allowed if ordinary budget/capability permits. Forced displacement remains possible and does not end the stance. Off-turn voluntary Reaction movement after that turn is allowed; AC lasts to expiry. It cannot coexist with Aggressive, Guarded, Mobile, Focused or Carrying because it occupies their stance choice, not a free extra buff.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Underlying AC17 gains floor2.55=2, total19. The feat does not round to a3-point bonus.",
    "A forced push during the stance moves the owner normally. They cannot then voluntarily teleport during their turn, but the push does not remove AC."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW complete activation: when choosing your stance at the start of a regular own turn before using any stance benefit or moving voluntarily, choose Defensive Stance instead of a normal stance. No Action; one stance choice. Through your next original regular start, add floor(15% of your otherwise-current AC), minimum0, to AC. Compute the base after actual armor/shield/DEX/flat bonuses/penalties but before this or any other percentage-AC bonus; no percent-on-percent multiplication. Recompute when that underlying base changes, including conditional Guard. You cannot voluntarily change position by Speed expenditure, teleport or a feature while the current regular turn lasts; linked extra turns also retain the movement restriction. Standing/dropping Prone is allowed if ordinary budget/capability permits. Forced displacement remains possible and does not end the stance. Off-turn voluntary Reaction movement after that turn is allowed; AC lasts to expiry. It cannot coexist with Aggressive, Guarded, Mobile, Focused or Carrying because it occupies their stance choice, not a free extra buff.

### Original-position authored review references

```json
[
  {
    "id": "CF-13-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/24"
  },
  {
    "id": "CF-13-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/25"
  }
]
```

## CF-14 — Disarming Blow

### Complete original object

```json
{
  "id": "disarming_blow",
  "name": "Disarming Blow",
  "description": "A Strength-trained melee combatant gains the listed chance to knock away a weapon.",
  "prerequisite": "Strength 14+, Melee",
  "effect": "When you hit a creature holding an object, forgo one damage die to force a Strength or Dexterity save (target’s choice) against DC 8 + proficiency bonus + your attack ability modifier. On a failure, it drops one held object.",
  "type": "Combat",
  "legacyEffect": "Chance to knock weapon out",
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
"Specify legal attack types, declaration/payment of one actual damage die, critical/multi-die/rider eligibility and inability to pay. Bind save/DC ability, held reachable object, selection/drop placement, non-droppable bonds and damage resolution order."
```

### Preserved original source direction (historical)

```json
{
  "featId": "disarming_blow",
  "name": "Disarming Blow",
  "cohort": "combat",
  "questionId": "CF-14",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/13",
  "originalQuestion": "Specify legal attack types, declaration/payment of one actual damage die, critical/multi-die/rider eligibility and inability to pay. Bind save/DC ability, held reachable object, selection/drop placement, non-droppable bonds and damage resolution order.",
  "originalSourceObject": {
    "id": "disarming_blow",
    "name": "Disarming Blow",
    "description": "A Strength-trained melee combatant gains the listed chance to knock away a weapon.",
    "prerequisite": "Strength 14+, Melee",
    "effect": "When you hit a creature holding an object, forgo one damage die to force a Strength or Dexterity save (target’s choice) against DC 8 + proficiency bonus + your attack ability modifier. On a failure, it drops one held object.",
    "type": "Combat",
    "legacyEffect": "Chance to knock weapon out",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "7c97540c19fb84593c257a09daef85be4b7532302bf571fc6604c9e16edb01a4",
  "submittedProcedure": "On a hit with a melee weapon attack, before rolling damage, select one held reachable object and forgo one actual base-weapon damage die to attempt disarming it. NEW remove one die before critical doubling; a critical1d8 weapon forgoes its entire doubled base2d8, retaining lawful flat damage and independent riders. Never pay with a rider die, a die already spent on another feat, or a fixed-damage expression. The target chooses STR or DEX save against DC8+PB+the actual attack ability modifier. Resolve remaining hit damage, then the save if the creature still holds the object. Failure drops it into an adjacent legal unoccupied space you choose, otherwise its own space. No extra damage to object, severed curse or bond; actual non-droppable bonds prevent dropping. An object wielded with two hands is still one object. No new once-turn cap: each separately paid qualifying hit can attempt, but the chosen die is spent even if immunity prevents the result.",
  "submittedNewChoices": "Melee-weapon scope; pre-critical base-die payment and save order; actual held-object drop geometry.",
  "submittedWorkedCases": [
    "A1d8 sword critical spends its one base die, leaving zero sword dice rather than one; STR modifier and a separately paid legal rider remain.",
    "A target's bonded blade cannot drop. The attacker's declared damage die is still forgone; the bond is not broken."
  ],
  "decision": "Retain the full CF-14 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Melee-weapon scope; pre-critical base-die payment and save order; actual held-object drop geometry.",
  "completeAuthoringProcedure": "On a hit with a melee weapon attack, before rolling damage, select one held reachable object and forgo one actual base-weapon damage die to attempt disarming it. NEW remove one die before critical doubling; a critical1d8 weapon forgoes its entire doubled base2d8, retaining lawful flat damage and independent riders. Never pay with a rider die, a die already spent on another feat, or a fixed-damage expression. The target chooses STR or DEX save against DC8+PB+the actual attack ability modifier. Resolve remaining hit damage, then the save if the creature still holds the object. Failure drops it into an adjacent legal unoccupied space you choose, otherwise its own space. No extra damage to object, severed curse or bond; actual non-droppable bonds prevent dropping. An object wielded with two hands is still one object. No new once-turn cap: each separately paid qualifying hit can attempt, but the chosen die is spent even if immunity prevents the result.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A1d8 sword critical spends its one base die, leaving zero sword dice rather than one; STR modifier and a separately paid legal rider remain.",
    "A target's bonded blade cannot drop. The attacker's declared damage die is still forgone; the bond is not broken."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

On a hit with a melee weapon attack, before rolling damage, select one held reachable object and forgo one actual base-weapon damage die to attempt disarming it. NEW remove one die before critical doubling; a critical1d8 weapon forgoes its entire doubled base2d8, retaining lawful flat damage and independent riders. Never pay with a rider die, a die already spent on another feat, or a fixed-damage expression. The target chooses STR or DEX save against DC8+PB+the actual attack ability modifier. Resolve remaining hit damage, then the save if the creature still holds the object. Failure drops it into an adjacent legal unoccupied space you choose, otherwise its own space. No extra damage to object, severed curse or bond; actual non-droppable bonds prevent dropping. An object wielded with two hands is still one object. No new once-turn cap: each separately paid qualifying hit can attempt, but the chosen die is spent even if immunity prevents the result.

### Original-position authored review references

```json
[
  {
    "id": "CF-14-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/26"
  },
  {
    "id": "CF-14-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/27"
  }
]
```

## CF-15 — Double Tap

### Complete original object

```json
{
  "id": "double_tap",
  "name": "Double Tap",
  "description": "Practiced ranged technique fires two shots in quick succession.",
  "prerequisite": "Dexterity 14+, Ranged",
  "effect": "When you take the Attack action with a ranged weapon, make one additional attack as a bonus action. This attack does not add your ability modifier to damage unless another feature allows it.",
  "type": "Combat",
  "legacyEffect": "Fire two shots in quick succession",
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
"Bind Attack-action qualification, one Bonus Action attack, weapon/ammunition/loading/hands and target choice. Resolve negative ability modifiers, an explicit modifier-restoring feature, off-turn/extra-turn timing and coexistence with other bonus-attack feats."
```

### Preserved original source direction (historical)

```json
{
  "featId": "double_tap",
  "name": "Double Tap",
  "cohort": "combat",
  "questionId": "CF-15",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/14",
  "originalQuestion": "Bind Attack-action qualification, one Bonus Action attack, weapon/ammunition/loading/hands and target choice. Resolve negative ability modifiers, an explicit modifier-restoring feature, off-turn/extra-turn timing and coexistence with other bonus-attack feats.",
  "originalSourceObject": {
    "id": "double_tap",
    "name": "Double Tap",
    "description": "Practiced ranged technique fires two shots in quick succession.",
    "prerequisite": "Dexterity 14+, Ranged",
    "effect": "When you take the Attack action with a ranged weapon, make one additional attack as a bonus action. This attack does not add your ability modifier to damage unless another feature allows it.",
    "type": "Combat",
    "legacyEffect": "Fire two shots in quick succession",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "67bbf7642b2842e1a56731eaae2ee71b48d00740eb840b5f04417bfdbf84b1e8",
  "submittedProcedure": "After you take the Attack Action on your turn and make at least one attack with a weapon classified as ranged, spend your available Bonus Action that turn for one additional attack with a legal ranged weapon. NEW it may be a different ranged weapon and a different target; thrown melee weapons do not meet ranged-weapon classification. Supply actual ammunition, loaded state, reload/loading cadence and usable hands. Omit a positive ability damage modifier but retain a negative one, matching current two-weapon arithmetic; only a feature expressly restoring this attack's modifier can restore it. A two-weapon-only exception is insufficient. No attack is granted off-turn by a readied Attack; a linked extra turn may supply the trigger only if it has a legal Attack Action and Bonus Action, without refreshing any consumed shared allowances. This never grants an extra BA.",
  "submittedNewChoices": "Ranged-weapon classification, positive-only omission, explicit restoring feature, same-turn use.",
  "submittedWorkedCases": [
    "A bow attack followed by a legal BA bow attack consumes two arrows; with DEX+3 the second damage omits+3.",
    "DEX−1 still reduces the second attack's damage. Loading that permits only one shot in the relevant period is not bypassed."
  ],
  "decision": "Retain the full CF-15 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Ranged-weapon classification, positive-only omission, explicit restoring feature, same-turn use.",
  "completeAuthoringProcedure": "After you take the Attack Action on your turn and make at least one attack with a weapon classified as ranged, spend your available Bonus Action that turn for one additional attack with a legal ranged weapon. NEW it may be a different ranged weapon and a different target; thrown melee weapons do not meet ranged-weapon classification. Supply actual ammunition, loaded state, reload/loading cadence and usable hands. Omit a positive ability damage modifier but retain a negative one, matching current two-weapon arithmetic; only a feature expressly restoring this attack's modifier can restore it. A two-weapon-only exception is insufficient. No attack is granted off-turn by a readied Attack; a linked extra turn may supply the trigger only if it has a legal Attack Action and Bonus Action, without refreshing any consumed shared allowances. This never grants an extra BA.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A bow attack followed by a legal BA bow attack consumes two arrows; with DEX+3 the second damage omits+3.",
    "DEX−1 still reduces the second attack's damage. Loading that permits only one shot in the relevant period is not bypassed."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After you take the Attack Action on your turn and make at least one attack with a weapon classified as ranged, spend your available Bonus Action that turn for one additional attack with a legal ranged weapon. NEW it may be a different ranged weapon and a different target; thrown melee weapons do not meet ranged-weapon classification. Supply actual ammunition, loaded state, reload/loading cadence and usable hands. Omit a positive ability damage modifier but retain a negative one, matching current two-weapon arithmetic; only a feature expressly restoring this attack's modifier can restore it. A two-weapon-only exception is insufficient. No attack is granted off-turn by a readied Attack; a linked extra turn may supply the trigger only if it has a legal Attack Action and Bonus Action, without refreshing any consumed shared allowances. This never grants an extra BA.

### Original-position authored review references

```json
[
  {
    "id": "CF-15-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/28"
  },
  {
    "id": "CF-15-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/29"
  }
]
```

## CF-16 — Draw Cut

### Complete original object

```json
{
  "id": "draw_cut",
  "name": "Draw Cut",
  "description": "Quick blade work increases damage when a weapon is unsheathed.",
  "prerequisite": "Dexterity 15+",
  "effect": "Once per encounter, when you draw a sheathed melee weapon as part of an attack, add one weapon damage die on a hit.",
  "type": "Combat",
  "legacyEffect": "+25% damage when unsheathing blade",
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
"Define the once-per-encounter boundary, lawful drawing interaction within an attack, sheathed weapon eligibility and hit/miss spending. Select one base weapon die and critical interaction without multiplying riders or laundering repeated sheath/draw events."
```

### Preserved original source direction (historical)

```json
{
  "featId": "draw_cut",
  "name": "Draw Cut",
  "cohort": "combat",
  "questionId": "CF-16",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/15",
  "originalQuestion": "Define the once-per-encounter boundary, lawful drawing interaction within an attack, sheathed weapon eligibility and hit/miss spending. Select one base weapon die and critical interaction without multiplying riders or laundering repeated sheath/draw events.",
  "originalSourceObject": {
    "id": "draw_cut",
    "name": "Draw Cut",
    "description": "Quick blade work increases damage when a weapon is unsheathed.",
    "prerequisite": "Dexterity 15+",
    "effect": "Once per encounter, when you draw a sheathed melee weapon as part of an attack, add one weapon damage die on a hit.",
    "type": "Combat",
    "legacyEffect": "+25% damage when unsheathing blade",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "03cb838ff9578d491afdc0f06f0519808f9c03ad476a1bf22744820a34a68f46",
  "submittedProcedure": "Once per encounter, when you legally draw a genuinely sheathed melee weapon as part of making a weapon attack with it, declare Draw Cut before the attack roll. NEW drawing uses the normal free object interaction or another explicitly granted draw permission; this feat grants no extra hand or interaction. The weapon must actually be secured in a sheath/scabbard, not merely dropped, held or conjured. A hit adds one actual base weapon die before critical doubling. A miss spends the declaration and encounter use. Resheathing, switching weapons, initiative exits and new turns do not refresh it. The attack may be a thrown attack with that melee weapon if drawing and throwing are otherwise legal. No attack Action or BA is supplied by the feat.",
  "submittedNewChoices": "Declaration spends on miss, actual sheath and ordinary interaction cost, explicit encounter boundary.",
  "submittedWorkedCases": [
    "Drawing a1d6 shortsword into a critical adds one base d6 and doubles both base dice for4d6.",
    "After a missed Draw Cut, sheathing and drawing a second weapon during the same fight cannot restore the use."
  ],
  "decision": "Retain the full CF-16 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Declaration spends on miss, actual sheath and ordinary interaction cost, explicit encounter boundary.",
  "completeAuthoringProcedure": "Once per encounter, when you legally draw a genuinely sheathed melee weapon as part of making a weapon attack with it, declare Draw Cut before the attack roll. NEW drawing uses the normal free object interaction or another explicitly granted draw permission; this feat grants no extra hand or interaction. The weapon must actually be secured in a sheath/scabbard, not merely dropped, held or conjured. A hit adds one actual base weapon die before critical doubling. A miss spends the declaration and encounter use. Resheathing, switching weapons, initiative exits and new turns do not refresh it. The attack may be a thrown attack with that melee weapon if drawing and throwing are otherwise legal. No attack Action or BA is supplied by the feat.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Drawing a1d6 shortsword into a critical adds one base d6 and doubles both base dice for4d6.",
    "After a missed Draw Cut, sheathing and drawing a second weapon during the same fight cannot restore the use."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per encounter, when you legally draw a genuinely sheathed melee weapon as part of making a weapon attack with it, declare Draw Cut before the attack roll. NEW drawing uses the normal free object interaction or another explicitly granted draw permission; this feat grants no extra hand or interaction. The weapon must actually be secured in a sheath/scabbard, not merely dropped, held or conjured. A hit adds one actual base weapon die before critical doubling. A miss spends the declaration and encounter use. Resheathing, switching weapons, initiative exits and new turns do not refresh it. The attack may be a thrown attack with that melee weapon if drawing and throwing are otherwise legal. No attack Action or BA is supplied by the feat.

### Original-position authored review references

```json
[
  {
    "id": "CF-16-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/30"
  },
  {
    "id": "CF-16-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/31"
  }
]
```

## CF-17 — Exploit Weakness

### Complete original object

```json
{
  "id": "exploit_weakness",
  "name": "Exploit Weakness",
  "description": "At level 7, a combatant seeks wounded enemies for the listed critical chance.",
  "prerequisite": "Level 7",
  "effect": "Your weapon attacks score a critical hit on a roll of 19–20 against creatures below half their hit point maximum.",
  "type": "Combat",
  "legacyEffect": "+15% crit on wounded enemies",
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
"Define when actual target HP below half maximum is checked, temporary HP/temporary maxima and unknown information handling. Resolve nineteen-to-twenty critical range against other range modifiers and automatic-critical effects without unsupported stacking."
```

### Preserved original source direction (historical)

```json
{
  "featId": "exploit_weakness",
  "name": "Exploit Weakness",
  "cohort": "combat",
  "questionId": "CF-17",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/16",
  "originalQuestion": "Define when actual target HP below half maximum is checked, temporary HP/temporary maxima and unknown information handling. Resolve nineteen-to-twenty critical range against other range modifiers and automatic-critical effects without unsupported stacking.",
  "originalSourceObject": {
    "id": "exploit_weakness",
    "name": "Exploit Weakness",
    "description": "At level 7, a combatant seeks wounded enemies for the listed critical chance.",
    "prerequisite": "Level 7",
    "effect": "Your weapon attacks score a critical hit on a roll of 19–20 against creatures below half their hit point maximum.",
    "type": "Combat",
    "legacyEffect": "+15% crit on wounded enemies",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "2dabdb3bf5bb5af2217e9c90262d0f9878b7c73506d00aef9eefcd2493783396",
  "submittedProcedure": "At attack-roll resolution, before that attack's damage, check whether the actual target's normalHP is strictly below half its current effective maximum:2×HP<maximum. TemporaryHP does not count as normalHP and does not change the comparison. If true, your weapon attack critically hits on a kept natural19 or20; a19 must still meet AC. Choose the broadest actually applicable critical range among this and other features; never add their range expansions. The Director can resolve this hidden predicate without disclosing numericHP or granting a diagnostic scan. A target that falls below half only from the current attack does not retroactively make that hit critical. A legal critical-if-hit feature can still apply independently; critical dice double once.",
  "submittedNewChoices": "Pre-damage actual-state snapshot and private adjudication; retained reviewed nonstacking critical-range rule.",
  "submittedWorkedCases": [
    "HP10/max21 qualifies; HP11/max21 does not. Ten temporaryHP does not change either result.",
    "A natural19 totals18 against AC20: it still misses, even when the target is below half."
  ],
  "decision": "Retain the full CF-17 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Pre-damage actual-state snapshot and private adjudication; retained reviewed nonstacking critical-range rule.",
  "completeAuthoringProcedure": "At attack-roll resolution, before that attack's damage, check whether the actual target's normalHP is strictly below half its current effective maximum:2×HP<maximum. TemporaryHP does not count as normalHP and does not change the comparison. If true, your weapon attack critically hits on a kept natural19 or20; a19 must still meet AC. Choose the broadest actually applicable critical range among this and other features; never add their range expansions. The Director can resolve this hidden predicate without disclosing numericHP or granting a diagnostic scan. A target that falls below half only from the current attack does not retroactively make that hit critical. A legal critical-if-hit feature can still apply independently; critical dice double once.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "HP10/max21 qualifies; HP11/max21 does not. Ten temporaryHP does not change either result.",
    "A natural19 totals18 against AC20: it still misses, even when the target is below half."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At attack-roll resolution, before that attack's damage, check whether the actual target's normalHP is strictly below half its current effective maximum:2×HP<maximum. TemporaryHP does not count as normalHP and does not change the comparison. If true, your weapon attack critically hits on a kept natural19 or20; a19 must still meet AC. Choose the broadest actually applicable critical range among this and other features; never add their range expansions. The Director can resolve this hidden predicate without disclosing numericHP or granting a diagnostic scan. A target that falls below half only from the current attack does not retroactively make that hit critical. A legal critical-if-hit feature can still apply independently; critical dice double once.

### Original-position authored review references

```json
[
  {
    "id": "CF-17-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/32"
  },
  {
    "id": "CF-17-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/33"
  }
]
```

## CF-18 — Feint

### Complete original object

```json
{
  "id": "feint",
  "name": "Feint",
  "description": "You can mislead opponents with deceptive movements.",
  "prerequisite": "Dexterity 14+, Charisma 13+",
  "effect": "Enemy loses AC vs next attack",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Complete the absent Action/Bonus Action, target/range, check/save, AC amount/layer, next-attack beneficiary, deadline, use frequency and replacement behavior. Preserve the original short clause separately; do not adopt an external game's Feint by name."
```

### Preserved original source direction (historical)

```json
{
  "featId": "feint",
  "name": "Feint",
  "cohort": "combat",
  "questionId": "CF-18",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/17",
  "originalQuestion": "Complete the absent Action/Bonus Action, target/range, check/save, AC amount/layer, next-attack beneficiary, deadline, use frequency and replacement behavior. Preserve the original short clause separately; do not adopt an external game's Feint by name.",
  "originalSourceObject": {
    "id": "feint",
    "name": "Feint",
    "description": "You can mislead opponents with deceptive movements.",
    "prerequisite": "Dexterity 14+, Charisma 13+",
    "effect": "Enemy loses AC vs next attack",
    "type": "Combat",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "47c32fd53c0e7db48ea38526b4c812b3cb005c5564cd1b5f2a4f48d0d885c658",
  "submittedProcedure": "NEW complete procedure: Bonus Action, one perceived hostile creature within30ft that can perceive your deliberate threatening movement; oppose your CHA Deception with its WIS Insight. Higher total wins; ties preserve state, with no task-degree/natural shift. On success, apply−2AC against your next attack on that creature before your next original regular start. Declare the affected attack before rolling; it consumes the feint hit or miss. Failure has no effect. Only one unspent Feint per owner; a new successful Feint replaces your prior mark. Multiple owners can each set their own next-attack records, but one attack never receives more than one−2 Feint layer. Feint does not compel beliefs, create a universal off-guard condition or lower AC against other attackers. No rest use cap; the real BA and opposed check fund each attempt. If a target cannot perceive the act, it is ineligible rather than automatically beaten.",
  "submittedNewChoices": "Entire BA/range/contest/−2/owner-only next-attack/deadline/frequency completion.",
  "submittedWorkedCases": [
    "Deception17 defeats Insight14. The owner's next attack checks AC16 instead of18 and consumes the mark even on a miss.",
    "An ally attacks first: that attack gains no Feint bonus and does not consume the owner's mark."
  ],
  "decision": "Retain the full CF-18 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Entire BA/range/contest/−2/owner-only next-attack/deadline/frequency completion.",
  "completeAuthoringProcedure": "NEW complete procedure: Bonus Action, one perceived hostile creature within30ft that can perceive your deliberate threatening movement; oppose your CHA Deception with its WIS Insight. Higher total wins; ties preserve state, with no task-degree/natural shift. On success, apply−2AC against your next attack on that creature before your next original regular start. Declare the affected attack before rolling; it consumes the feint hit or miss. Failure has no effect. Only one unspent Feint per owner; a new successful Feint replaces your prior mark. Multiple owners can each set their own next-attack records, but one attack never receives more than one−2 Feint layer. Feint does not compel beliefs, create a universal off-guard condition or lower AC against other attackers. No rest use cap; the real BA and opposed check fund each attempt. If a target cannot perceive the act, it is ineligible rather than automatically beaten.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Deception17 defeats Insight14. The owner's next attack checks AC16 instead of18 and consumes the mark even on a miss.",
    "An ally attacks first: that attack gains no Feint bonus and does not consume the owner's mark."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW complete procedure: Bonus Action, one perceived hostile creature within30ft that can perceive your deliberate threatening movement; oppose your CHA Deception with its WIS Insight. Higher total wins; ties preserve state, with no task-degree/natural shift. On success, apply−2AC against your next attack on that creature before your next original regular start. Declare the affected attack before rolling; it consumes the feint hit or miss. Failure has no effect. Only one unspent Feint per owner; a new successful Feint replaces your prior mark. Multiple owners can each set their own next-attack records, but one attack never receives more than one−2 Feint layer. Feint does not compel beliefs, create a universal off-guard condition or lower AC against other attackers. No rest use cap; the real BA and opposed check fund each attempt. If a target cannot perceive the act, it is ineligible rather than automatically beaten.

### Original-position authored review references

```json
[
  {
    "id": "CF-18-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/34"
  },
  {
    "id": "CF-18-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/35"
  }
]
```

## CF-19 — Grappler

### Complete original object

```json
{
  "id": "grappler",
  "name": "Grappler",
  "description": "You have developed the skills necessary to hold your own in close-quarters grappling.",
  "prerequisite": "Strength 14+",
  "effect": "+4 to grapple rolls; enemies -4 to escape",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Bind+4 to actual initiating/maintaining/escape contests and whose roll receives the-4. Resolve multiple grapplers, size/reach/hands limits, four-degree checks, magical escape and stacking with proficiency/expertise without granting new grapple actions."
```

### Preserved original source direction (historical)

```json
{
  "featId": "grappler",
  "name": "Grappler",
  "cohort": "combat",
  "questionId": "CF-19",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/18",
  "originalQuestion": "Bind+4 to actual initiating/maintaining/escape contests and whose roll receives the-4. Resolve multiple grapplers, size/reach/hands limits, four-degree checks, magical escape and stacking with proficiency/expertise without granting new grapple actions.",
  "originalSourceObject": {
    "id": "grappler",
    "name": "Grappler",
    "description": "You have developed the skills necessary to hold your own in close-quarters grappling.",
    "prerequisite": "Strength 14+",
    "effect": "+4 to grapple rolls; enemies -4 to escape",
    "type": "Combat",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "d76f83d7af628b60ad6a8f84e877ba8d5694b2fdfce47edbb1f0e828e8067183",
  "submittedProcedure": "Add+4 to your actual STR Athletics checks initiating or maintaining an ordinary grapple you control. A creature using the ordinary opposed Escape Action to escape your grapple takes−4 on its chosen Athletics/Acrobatics roll. Your opposed maintaining roll also gets+4; these are different sides of the expressly printed contest. NEW this gives no+4 to your own escape from someone else's hold, no penalty to a defender's initial resistance, and no effect on spell saves or teleports that legally escape without that opposed contest. Reach, one-size-larger cap, actual grasping hand, attack replacement and Escape Action remain unchanged. Multiple grapplers have separate holds and contests; do not multiply−4 from another grapple that is not the selected escape. PB/expertise is included normally once; opposed ties preserve the hold and have no critical task effects.",
  "submittedNewChoices": "Initiating/maintaining scope versus escape, initial defense exclusion and per-hold contest.",
  "submittedWorkedCases": [
    "Initiation Athletics12 becomes16; defender Acrobatics15 remains15, so the hold is established.",
    "For escape, defender total18 becomes14 while the owner's maintenance13 becomes17. An unrelated second grappler adds no further−4."
  ],
  "decision": "Retain the full CF-19 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Initiating/maintaining scope versus escape, initial defense exclusion and per-hold contest.",
  "completeAuthoringProcedure": "Add+4 to your actual STR Athletics checks initiating or maintaining an ordinary grapple you control. A creature using the ordinary opposed Escape Action to escape your grapple takes−4 on its chosen Athletics/Acrobatics roll. Your opposed maintaining roll also gets+4; these are different sides of the expressly printed contest. NEW this gives no+4 to your own escape from someone else's hold, no penalty to a defender's initial resistance, and no effect on spell saves or teleports that legally escape without that opposed contest. Reach, one-size-larger cap, actual grasping hand, attack replacement and Escape Action remain unchanged. Multiple grapplers have separate holds and contests; do not multiply−4 from another grapple that is not the selected escape. PB/expertise is included normally once; opposed ties preserve the hold and have no critical task effects.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Initiation Athletics12 becomes16; defender Acrobatics15 remains15, so the hold is established.",
    "For escape, defender total18 becomes14 while the owner's maintenance13 becomes17. An unrelated second grappler adds no further−4."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Add+4 to your actual STR Athletics checks initiating or maintaining an ordinary grapple you control. A creature using the ordinary opposed Escape Action to escape your grapple takes−4 on its chosen Athletics/Acrobatics roll. Your opposed maintaining roll also gets+4; these are different sides of the expressly printed contest. NEW this gives no+4 to your own escape from someone else's hold, no penalty to a defender's initial resistance, and no effect on spell saves or teleports that legally escape without that opposed contest. Reach, one-size-larger cap, actual grasping hand, attack replacement and Escape Action remain unchanged. Multiple grapplers have separate holds and contests; do not multiply−4 from another grapple that is not the selected escape. PB/expertise is included normally once; opposed ties preserve the hold and have no critical task effects.

### Original-position authored review references

```json
[
  {
    "id": "CF-19-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/36"
  },
  {
    "id": "CF-19-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/37"
  }
]
```

## CF-20 — Lunge

### Complete original object

```json
{
  "id": "lunge",
  "name": "Lunge",
  "description": "Strength and weapon training extend the reach of the feat's listed melee attacks.",
  "prerequisite": "Strength 13+, Weapon Proficiency",
  "effect": "Once on your turn, increase your reach by 5 feet for one melee weapon attack.",
  "type": "Combat",
  "legacyEffect": "Melee attacks gain +5ft range",
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
"Bind one selected melee weapon attack, declaration before targeting, own-turn cadence, current weapon reach and reversion. Explicitly distinguish attack reach from persistent control/opportunity reach and grapple reach."
```

### Preserved original source direction (historical)

```json
{
  "featId": "lunge",
  "name": "Lunge",
  "cohort": "combat",
  "questionId": "CF-20",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/19",
  "originalQuestion": "Bind one selected melee weapon attack, declaration before targeting, own-turn cadence, current weapon reach and reversion. Explicitly distinguish attack reach from persistent control/opportunity reach and grapple reach.",
  "originalSourceObject": {
    "id": "lunge",
    "name": "Lunge",
    "description": "Strength and weapon training extend the reach of the feat's listed melee attacks.",
    "prerequisite": "Strength 13+, Weapon Proficiency",
    "effect": "Once on your turn, increase your reach by 5 feet for one melee weapon attack.",
    "type": "Combat",
    "legacyEffect": "Melee attacks gain +5ft range",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "c304b2eba19fcc4a58b51fe1bae9e4ab36cf5e708b7c5976447bfc67e980411f",
  "submittedProcedure": "Once on your own turn before selecting the target of one melee weapon attack, increase that attack's reach by5ft. Use its actual weapon reach and body profile, then restore ordinary reach immediately after the attack resolves or is interrupted. The declaration consumes the allowance even on a miss. It grants no attack, extra movement, general threatened space, grapple reach or persistent opportunity reach. A later off-turn opportunity attack uses ordinary reach unless its own source specifically grants an exception. A natural weapon only qualifies if actually a weapon attack. You must possess an actual weapon proficiency to acquire the feat, but use with another unproficient legal weapon does not grant PB.",
  "submittedNewChoices": "Attack-scoped pre-target declaration, spent-on-miss and no persistent reach.",
  "submittedWorkedCases": [
    "A5ft sword can attack one target10ft away; afterward it still threatens only5ft.",
    "A10ft reach weapon can make one15ft attack. The target moving from15 to20ft afterward does not trigger that weapon's normal opportunity reach."
  ],
  "decision": "Retain the full CF-20 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Attack-scoped pre-target declaration, spent-on-miss and no persistent reach.",
  "completeAuthoringProcedure": "Once on your own turn before selecting the target of one melee weapon attack, increase that attack's reach by5ft. Use its actual weapon reach and body profile, then restore ordinary reach immediately after the attack resolves or is interrupted. The declaration consumes the allowance even on a miss. It grants no attack, extra movement, general threatened space, grapple reach or persistent opportunity reach. A later off-turn opportunity attack uses ordinary reach unless its own source specifically grants an exception. A natural weapon only qualifies if actually a weapon attack. You must possess an actual weapon proficiency to acquire the feat, but use with another unproficient legal weapon does not grant PB.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A5ft sword can attack one target10ft away; afterward it still threatens only5ft.",
    "A10ft reach weapon can make one15ft attack. The target moving from15 to20ft afterward does not trigger that weapon's normal opportunity reach."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once on your own turn before selecting the target of one melee weapon attack, increase that attack's reach by5ft. Use its actual weapon reach and body profile, then restore ordinary reach immediately after the attack resolves or is interrupted. The declaration consumes the allowance even on a miss. It grants no attack, extra movement, general threatened space, grapple reach or persistent opportunity reach. A later off-turn opportunity attack uses ordinary reach unless its own source specifically grants an exception. A natural weapon only qualifies if actually a weapon attack. You must possess an actual weapon proficiency to acquire the feat, but use with another unproficient legal weapon does not grant PB.

### Original-position authored review references

```json
[
  {
    "id": "CF-20-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/38"
  },
  {
    "id": "CF-20-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/39"
  }
]
```

## CF-21 — Overrun

### Complete original object

```json
{
  "id": "overrun",
  "name": "Overrun",
  "description": "With Strength 15+, you press through movement by pushing enemies aside as the feat lists.",
  "prerequisite": "Strength 15+",
  "effect": "When you Dash, you may move through spaces occupied by creatures no more than one size larger. Each may make a Strength save against DC 8 + proficiency bonus + Strength modifier or be pushed 5 feet aside.",
  "type": "Combat",
  "legacyEffect": "Push enemies aside while moving",
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
"Complete Dash-linked movement budget, per-creature encounter limits, ally/enemy scope, save/DC and success/failure passage. Resolve no legal five-foot side destination, blocked endpoints, opportunity attacks and size/anatomy restrictions."
```

### Preserved original source direction (historical)

```json
{
  "featId": "overrun",
  "name": "Overrun",
  "cohort": "combat",
  "questionId": "CF-21",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/20",
  "originalQuestion": "Complete Dash-linked movement budget, per-creature encounter limits, ally/enemy scope, save/DC and success/failure passage. Resolve no legal five-foot side destination, blocked endpoints, opportunity attacks and size/anatomy restrictions.",
  "originalSourceObject": {
    "id": "overrun",
    "name": "Overrun",
    "description": "With Strength 15+, you press through movement by pushing enemies aside as the feat lists.",
    "prerequisite": "Strength 15+",
    "effect": "When you Dash, you may move through spaces occupied by creatures no more than one size larger. Each may make a Strength save against DC 8 + proficiency bonus + Strength modifier or be pushed 5 feet aside.",
    "type": "Combat",
    "legacyEffect": "Push enemies aside while moving",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "926cb532c3017b3bf4667aca274a0020228c1658cbcc326972e00673e6767287",
  "submittedProcedure": "When you legally take Dash, activate Overrun for that turn's subsequent ordinary movement; Dash supplies its normal increased cap, not a second separate movement grant. You may attempt passage through actual creatures at most one size larger, allied or hostile. NEW each distinct creature may be challenged once that turn, with no duplicate attempt from extra Dashes. Before entering its first occupied space, it makes STR save DC8+PB+your STR; a willing ally may elect failure as this feat's explicit exception. On failure push it5ft to a legal adjacent side destination you choose that clears the necessary passage. Success, anchoring, or no legal clearing destination blocks this special passage; remain outside and spend the attempted first entry step's ordinary cost. Do not start without enough budget for a complete legal path/end. The feat does not suppress opportunity attacks. A creature already passable under ordinary size rules can instead be crossed normally without invoking the feature. It grants no Prone, damage or ability to remain in occupied space.",
  "submittedNewChoices": "Once-per-creature challenge, ally voluntary failure exception, side-destination requirement and blocked-passage consequence.",
  "submittedWorkedCases": [
    "A Medium runner Dashes and a Large guard fails; a legal5ft side space clears the route, so the runner proceeds using ordinary cost.",
    "A guard fills a narrow passage with no side destination. Failure alone cannot teleport it through the wall; Overrun passage stays blocked."
  ],
  "decision": "Retain the full CF-21 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Once-per-creature challenge, ally voluntary failure exception, side-destination requirement and blocked-passage consequence.",
  "completeAuthoringProcedure": "When you legally take Dash, activate Overrun for that turn's subsequent ordinary movement; Dash supplies its normal increased cap, not a second separate movement grant. You may attempt passage through actual creatures at most one size larger, allied or hostile. NEW each distinct creature may be challenged once that turn, with no duplicate attempt from extra Dashes. Before entering its first occupied space, it makes STR save DC8+PB+your STR; a willing ally may elect failure as this feat's explicit exception. On failure push it5ft to a legal adjacent side destination you choose that clears the necessary passage. Success, anchoring, or no legal clearing destination blocks this special passage; remain outside and spend the attempted first entry step's ordinary cost. Do not start without enough budget for a complete legal path/end. The feat does not suppress opportunity attacks. A creature already passable under ordinary size rules can instead be crossed normally without invoking the feature. It grants no Prone, damage or ability to remain in occupied space.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A Medium runner Dashes and a Large guard fails; a legal5ft side space clears the route, so the runner proceeds using ordinary cost.",
    "A guard fills a narrow passage with no side destination. Failure alone cannot teleport it through the wall; Overrun passage stays blocked."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

When you legally take Dash, activate Overrun for that turn's subsequent ordinary movement; Dash supplies its normal increased cap, not a second separate movement grant. You may attempt passage through actual creatures at most one size larger, allied or hostile. NEW each distinct creature may be challenged once that turn, with no duplicate attempt from extra Dashes. Before entering its first occupied space, it makes STR save DC8+PB+your STR; a willing ally may elect failure as this feat's explicit exception. On failure push it5ft to a legal adjacent side destination you choose that clears the necessary passage. Success, anchoring, or no legal clearing destination blocks this special passage; remain outside and spend the attempted first entry step's ordinary cost. Do not start without enough budget for a complete legal path/end. The feat does not suppress opportunity attacks. A creature already passable under ordinary size rules can instead be crossed normally without invoking the feature. It grants no Prone, damage or ability to remain in occupied space.

### Original-position authored review references

```json
[
  {
    "id": "CF-21-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/40"
  },
  {
    "id": "CF-21-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/41"
  }
]
```

## CF-22 — Power Attack

### Complete original object

```json
{
  "id": "power_attack",
  "name": "Power Attack",
  "description": "You can sacrifice accuracy for devastating damage.",
  "prerequisite": "Strength 14+",
  "effect": "Trade -2 accuracy for +20% damage",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Complete declaration, eligible attacks, frequency, exact-2 attack penalty and+20% damage base/rounding/order. Resolve multi-type packets, criticals, resistance and combination with Precision Strike/Giant Slayer without silently substituting a flat damage bonus."
```

### Preserved original source direction (historical)

```json
{
  "featId": "power_attack",
  "name": "Power Attack",
  "cohort": "combat",
  "questionId": "CF-22",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/21",
  "originalQuestion": "Complete declaration, eligible attacks, frequency, exact-2 attack penalty and+20% damage base/rounding/order. Resolve multi-type packets, criticals, resistance and combination with Precision Strike/Giant Slayer without silently substituting a flat damage bonus.",
  "originalSourceObject": {
    "id": "power_attack",
    "name": "Power Attack",
    "description": "You can sacrifice accuracy for devastating damage.",
    "prerequisite": "Strength 14+",
    "effect": "Trade -2 accuracy for +20% damage",
    "type": "Combat",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "cb386da047a686455fa3f92c368f3b1f544f44972a4b6cc33130fb23407036f6",
  "submittedProcedure": "NEW complete procedure: before each melee weapon attack roll using STR for that roll, you may take−2 to that roll. If it hits, add floor20% of that attack's eligible native weapon damage as defined in shared arithmetic. This is an optional per-attack trade, no Action or rest charge. Actual weapon proficiency is not granted; finesse choosingDEX, ranged attacks and melee spell/unarmed attacks do not qualify. Preserve critical dice before calculating the percent bonus; no benefit on a miss. Power Attack and Precision Strike's attack trade are mutually exclusive choices on the same attack, not cumulative penalties for stacking both percent bonuses. Giant Slayer or another genuinely independent eligible percent source adds its separately rounded bonus from the same base, without multiplication. Original−2/+20% stays preserved.",
  "submittedNewChoices": "STR melee-weapon scope and per-attack timing; mutually exclusive precision/power trade; noncompounding percent contract.",
  "submittedWorkedCases": [
    "Eligible native weapon damage19 yields+3, total22 before defenses. The attack roll still suffers−2.",
    "Against a Large creature, native20 with both Power Attack20% and Giant Slayer20% totals28, not28.8 or29."
  ],
  "decision": "Retain the full CF-22 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. STR melee-weapon scope and per-attack timing; mutually exclusive precision/power trade; noncompounding percent contract.",
  "completeAuthoringProcedure": "NEW complete procedure: before each melee weapon attack roll using STR for that roll, you may take−2 to that roll. If it hits, add floor20% of that attack's eligible native weapon damage as defined in shared arithmetic. This is an optional per-attack trade, no Action or rest charge. Actual weapon proficiency is not granted; finesse choosingDEX, ranged attacks and melee spell/unarmed attacks do not qualify. Preserve critical dice before calculating the percent bonus; no benefit on a miss. Power Attack and Precision Strike's attack trade are mutually exclusive choices on the same attack, not cumulative penalties for stacking both percent bonuses. Giant Slayer or another genuinely independent eligible percent source adds its separately rounded bonus from the same base, without multiplication. Original−2/+20% stays preserved.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Eligible native weapon damage19 yields+3, total22 before defenses. The attack roll still suffers−2.",
    "Against a Large creature, native20 with both Power Attack20% and Giant Slayer20% totals28, not28.8 or29."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW complete procedure: before each melee weapon attack roll using STR for that roll, you may take−2 to that roll. If it hits, add floor20% of that attack's eligible native weapon damage as defined in shared arithmetic. This is an optional per-attack trade, no Action or rest charge. Actual weapon proficiency is not granted; finesse choosingDEX, ranged attacks and melee spell/unarmed attacks do not qualify. Preserve critical dice before calculating the percent bonus; no benefit on a miss. Power Attack and Precision Strike's attack trade are mutually exclusive choices on the same attack, not cumulative penalties for stacking both percent bonuses. Giant Slayer or another genuinely independent eligible percent source adds its separately rounded bonus from the same base, without multiplication. Original−2/+20% stays preserved.

### Original-position authored review references

```json
[
  {
    "id": "CF-22-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/42"
  },
  {
    "id": "CF-22-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/43"
  }
]
```

## CF-23 — Precise Shot

### Complete original object

```json
{
  "id": "precise_shot",
  "name": "Precise Shot",
  "description": "Dexterity 14+ supports a ranged attack into melee without the feat's listed penalty.",
  "prerequisite": "Dexterity 14+",
  "effect": "Your ranged attacks ignore the disadvantage normally imposed by an ally being adjacent to the target.",
  "type": "Combat",
  "legacyEffect": "No penalty for ranged into melee",
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
"The supplied current combat guide imposes nearby-hostile disadvantage, not a general ally-adjacent-to-target disadvantage. Locate source authority for the assumed penalty or choose an explicit finite new overlay; do not invent that penalty globally or silently turn this into Sharpshooter."
```

### Preserved original source direction (historical)

```json
{
  "featId": "precise_shot",
  "name": "Precise Shot",
  "cohort": "combat",
  "questionId": "CF-23",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/22",
  "originalQuestion": "The supplied current combat guide imposes nearby-hostile disadvantage, not a general ally-adjacent-to-target disadvantage. Locate source authority for the assumed penalty or choose an explicit finite new overlay; do not invent that penalty globally or silently turn this into Sharpshooter.",
  "originalSourceObject": {
    "id": "precise_shot",
    "name": "Precise Shot",
    "description": "Dexterity 14+ supports a ranged attack into melee without the feat's listed penalty.",
    "prerequisite": "Dexterity 14+",
    "effect": "Your ranged attacks ignore the disadvantage normally imposed by an ally being adjacent to the target.",
    "type": "Combat",
    "legacyEffect": "No penalty for ranged into melee",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "b6dc99bb130bb3c8439cd499232bbf0a126e740398c809f0450c2ae226becbd3",
  "submittedProcedure": "The current combat guide imposes no general disadvantage just because an ally is adjacent to the target; retain that printed historical removal as a compatibility clause if a specifically enabled source ever supplies it. NEW useful completion for this candidate: your ranged weapon or ranged spell attack ignores half cover when that half cover is supplied solely by one or more allied creature bodies in the shot's actual path. It ignores neither terrain cover, three-quarters/total cover, hostile-body cover, nearby-hostile disadvantage, nor long-range disadvantage. Compute remaining actual cover normally after disregarding those allied bodies; never lower a real wall's cover. This does not make firing through solid or untargetable positions legal and does not acquire a class Sharpshooter feature.",
  "submittedNewChoices": "Explicit allied-body half-cover overlay because the named original disadvantage is absent; no new global penalty.",
  "submittedWorkedCases": [
    "An allied frontliner is the only cause of half cover: the shot ignores that+2AC.",
    "The target stands behind a low stone wall and beside an ally. The wall's half cover remains."
  ],
  "decision": "Retain the full CF-23 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Explicit allied-body half-cover overlay because the named original disadvantage is absent; no new global penalty.",
  "completeAuthoringProcedure": "The current combat guide imposes no general disadvantage just because an ally is adjacent to the target; retain that printed historical removal as a compatibility clause if a specifically enabled source ever supplies it. NEW useful completion for this candidate: your ranged weapon or ranged spell attack ignores half cover when that half cover is supplied solely by one or more allied creature bodies in the shot's actual path. It ignores neither terrain cover, three-quarters/total cover, hostile-body cover, nearby-hostile disadvantage, nor long-range disadvantage. Compute remaining actual cover normally after disregarding those allied bodies; never lower a real wall's cover. This does not make firing through solid or untargetable positions legal and does not acquire a class Sharpshooter feature.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "An allied frontliner is the only cause of half cover: the shot ignores that+2AC.",
    "The target stands behind a low stone wall and beside an ally. The wall's half cover remains."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

The current combat guide imposes no general disadvantage just because an ally is adjacent to the target; retain that printed historical removal as a compatibility clause if a specifically enabled source ever supplies it. NEW useful completion for this candidate: your ranged weapon or ranged spell attack ignores half cover when that half cover is supplied solely by one or more allied creature bodies in the shot's actual path. It ignores neither terrain cover, three-quarters/total cover, hostile-body cover, nearby-hostile disadvantage, nor long-range disadvantage. Compute remaining actual cover normally after disregarding those allied bodies; never lower a real wall's cover. This does not make firing through solid or untargetable positions legal and does not acquire a class Sharpshooter feature.

### Original-position authored review references

```json
[
  {
    "id": "CF-23-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/44"
  },
  {
    "id": "CF-23-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/45"
  }
]
```

## CF-24 — Precision Throw

### Complete original object

```json
{
  "id": "precision_throw",
  "name": "Precision Throw",
  "description": "Dexterity 13+ supports thrown weapons gaining the listed +10% accuracy.",
  "prerequisite": "Dexterity 13+",
  "effect": "Gain +1 to attack rolls with thrown weapons and double their normal range.",
  "type": "Combat",
  "legacyEffect": "Thrown weapons gain +10% accuracy",
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
"Define thrown-property melee/ranged weapon use, actual attack qualifier, normal versus long range caps and legal cases where doubled normal exceeds long. Resolve+1 bonus-family stacking and improvised thrown objects."
```

### Preserved original source direction (historical)

```json
{
  "featId": "precision_throw",
  "name": "Precision Throw",
  "cohort": "combat",
  "questionId": "CF-24",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/23",
  "originalQuestion": "Define thrown-property melee/ranged weapon use, actual attack qualifier, normal versus long range caps and legal cases where doubled normal exceeds long. Resolve+1 bonus-family stacking and improvised thrown objects.",
  "originalSourceObject": {
    "id": "precision_throw",
    "name": "Precision Throw",
    "description": "Dexterity 13+ supports thrown weapons gaining the listed +10% accuracy.",
    "prerequisite": "Dexterity 13+",
    "effect": "Gain +1 to attack rolls with thrown weapons and double their normal range.",
    "type": "Combat",
    "legacyEffect": "Thrown weapons gain +10% accuracy",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "90062637597727515952751d7ae0232b5ea0c5b0b3ce3c7e2e08e05740c8ba88",
  "submittedProcedure": "When you make a ranged attack by actually throwing a weapon whose current profile has Thrown, gain+1 attack and double its printed normal range, capped at its actual printed long range. Preserve long range unchanged. NEW no-long-range profiles retain their hard maximum; the feat cannot invent a missing legal interval. Melee use of the same weapon gains nothing. Improvised objects require an actual Thrown weapon profile supplied by another rule; merely hurling an object does not acquire the property. Distinct eligible Weapon Focus+1 may add under its separate feat family; duplicate Precision Throw never stacks. Physical quantities, recovery, hands and ammunition remain actual.",
  "submittedNewChoices": "Property/use distinction, normal-range cap and separate feat attack-bonus families.",
  "submittedWorkedCases": [
    "A20/60 dagger becomes40/60 for throwing and gains+1attack; a melee stab does not.",
    "A hypothetical40/60 Thrown profile becomes60/60, with no attacks beyond60."
  ],
  "decision": "Retain the full CF-24 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Property/use distinction, normal-range cap and separate feat attack-bonus families.",
  "completeAuthoringProcedure": "When you make a ranged attack by actually throwing a weapon whose current profile has Thrown, gain+1 attack and double its printed normal range, capped at its actual printed long range. Preserve long range unchanged. NEW no-long-range profiles retain their hard maximum; the feat cannot invent a missing legal interval. Melee use of the same weapon gains nothing. Improvised objects require an actual Thrown weapon profile supplied by another rule; merely hurling an object does not acquire the property. Distinct eligible Weapon Focus+1 may add under its separate feat family; duplicate Precision Throw never stacks. Physical quantities, recovery, hands and ammunition remain actual.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A20/60 dagger becomes40/60 for throwing and gains+1attack; a melee stab does not.",
    "A hypothetical40/60 Thrown profile becomes60/60, with no attacks beyond60."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

When you make a ranged attack by actually throwing a weapon whose current profile has Thrown, gain+1 attack and double its printed normal range, capped at its actual printed long range. Preserve long range unchanged. NEW no-long-range profiles retain their hard maximum; the feat cannot invent a missing legal interval. Melee use of the same weapon gains nothing. Improvised objects require an actual Thrown weapon profile supplied by another rule; merely hurling an object does not acquire the property. Distinct eligible Weapon Focus+1 may add under its separate feat family; duplicate Precision Throw never stacks. Physical quantities, recovery, hands and ammunition remain actual.

### Original-position authored review references

```json
[
  {
    "id": "CF-24-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/46"
  },
  {
    "id": "CF-24-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/47"
  }
]
```

## CF-25 — Punishing Blow

### Complete original object

```json
{
  "id": "punishing_blow",
  "name": "Punishing Blow",
  "description": "Strength 13+ supports the listed +10% bonus against a stunned enemy.",
  "prerequisite": "Strength 13+",
  "effect": "Once per turn, deal additional damage equal to your proficiency bonus to a stunned or prone enemy.",
  "type": "Combat",
  "legacyEffect": "+10% bonus if enemy is stunned",
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
"Define eligible damage events/attacks, hostile versus any target, actual Stunned/Prone timing, once-per-turn cadence and damage type. Avoid copying the PB rider through each damage component or transfer operation."
```

### Preserved original source direction (historical)

```json
{
  "featId": "punishing_blow",
  "name": "Punishing Blow",
  "cohort": "combat",
  "questionId": "CF-25",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/24",
  "originalQuestion": "Define eligible damage events/attacks, hostile versus any target, actual Stunned/Prone timing, once-per-turn cadence and damage type. Avoid copying the PB rider through each damage component or transfer operation.",
  "originalSourceObject": {
    "id": "punishing_blow",
    "name": "Punishing Blow",
    "description": "Strength 13+ supports the listed +10% bonus against a stunned enemy.",
    "prerequisite": "Strength 13+",
    "effect": "Once per turn, deal additional damage equal to your proficiency bonus to a stunned or prone enemy.",
    "type": "Combat",
    "legacyEffect": "+10% bonus if enemy is stunned",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "a81c1fcbb12975a3249cfa691927140ca3524f5c986d7c94ea70ba2983d90243",
  "submittedProcedure": "Once per turn, on one of your own direct attacks that hits a genuine enemy already Stunned or Prone immediately before damage, add your current PB as a flat damage component of that hit's native type. Choose one native type if the attack has several; if it deals no native damage, no additional damage is created. NEW all actual attack types qualify, including spell, natural and unarmed, because source says deal additional damage without weapon restriction. No application from a save-only effect, periodic tick, transfer, copy or rider that does not itself attack. The same hit cannot first inflict Prone/Stunned and retroactively qualify. The bonus is part of the hit before defenses, cannot double on a critical, and applies once across multi-type components.",
  "submittedNewChoices": "Direct-attack completion, pre-damage existing condition, flat single component and broad actual attack scope.",
  "submittedWorkedCases": [
    "PB4 adds4 to a critical against a creature already Prone; it does not become8.",
    "Bull Rush knocks the standing target Prone after damage. That same attack does not receive Punishing Blow retroactively."
  ],
  "decision": "Retain the full CF-25 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Direct-attack completion, pre-damage existing condition, flat single component and broad actual attack scope.",
  "completeAuthoringProcedure": "Once per turn, on one of your own direct attacks that hits a genuine enemy already Stunned or Prone immediately before damage, add your current PB as a flat damage component of that hit's native type. Choose one native type if the attack has several; if it deals no native damage, no additional damage is created. NEW all actual attack types qualify, including spell, natural and unarmed, because source says deal additional damage without weapon restriction. No application from a save-only effect, periodic tick, transfer, copy or rider that does not itself attack. The same hit cannot first inflict Prone/Stunned and retroactively qualify. The bonus is part of the hit before defenses, cannot double on a critical, and applies once across multi-type components.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "PB4 adds4 to a critical against a creature already Prone; it does not become8.",
    "Bull Rush knocks the standing target Prone after damage. That same attack does not receive Punishing Blow retroactively."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Once per turn, on one of your own direct attacks that hits a genuine enemy already Stunned or Prone immediately before damage, add your current PB as a flat damage component of that hit's native type. Choose one native type if the attack has several; if it deals no native damage, no additional damage is created. NEW all actual attack types qualify, including spell, natural and unarmed, because source says deal additional damage without weapon restriction. No application from a save-only effect, periodic tick, transfer, copy or rider that does not itself attack. The same hit cannot first inflict Prone/Stunned and retroactively qualify. The bonus is part of the hit before defenses, cannot double on a critical, and applies once across multi-type components.

### Original-position authored review references

```json
[
  {
    "id": "CF-25-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/48"
  },
  {
    "id": "CF-25-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/49"
  }
]
```

## CF-26 — Reckless Swing

### Complete original object

```json
{
  "id": "reckless_swing",
  "name": "Reckless Swing",
  "description": "Strength 15+ supports the listed +50% damage with -10% defense.",
  "prerequisite": "Strength 15+",
  "effect": "Before making a melee weapon attack, choose to attack recklessly. Gain advantage on the attack and add one weapon damage die on a hit; attacks against you have advantage until the start of your next turn.",
  "type": "Combat",
  "legacyEffect": "+50% damage, but -10% to defense",
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
"Bind declaration and eligible melee weapon, advantage cancellation, selection of one weapon die and critical doubling. Resolve repeated use, missed attacks, extra turns, expiry and all attacks against the user without replacing source with a class Rage rule."
```

### Preserved original source direction (historical)

```json
{
  "featId": "reckless_swing",
  "name": "Reckless Swing",
  "cohort": "combat",
  "questionId": "CF-26",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/25",
  "originalQuestion": "Bind declaration and eligible melee weapon, advantage cancellation, selection of one weapon die and critical doubling. Resolve repeated use, missed attacks, extra turns, expiry and all attacks against the user without replacing source with a class Rage rule.",
  "originalSourceObject": {
    "id": "reckless_swing",
    "name": "Reckless Swing",
    "description": "Strength 15+ supports the listed +50% damage with -10% defense.",
    "prerequisite": "Strength 15+",
    "effect": "Before making a melee weapon attack, choose to attack recklessly. Gain advantage on the attack and add one weapon damage die on a hit; attacks against you have advantage until the start of your next turn.",
    "type": "Combat",
    "legacyEffect": "+50% damage, but -10% to defense",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "617e9cea06bc5de4300608c569857cc65b855be3c6a390d07933ad163dbab268",
  "submittedProcedure": "Before any melee weapon attack roll, you may declare Reckless Swing. That one attack gains advantage and adds one base weapon damage die if it hits; critical doubles that additional attack die. Regardless of hit, miss or advantage cancellation, all attacks against you have advantage through your next original regular start. Repeated declarations on separately legal attacks can each supply their one die but do not stack attacker advantage or create attacks; overlapping vulnerability records retain the same next-start deadline. This is not a rage and has no resistance or ability-score substitution. Spell, thrown ranged and unarmed attacks do not qualify; actual natural weapon melee attacks do. Ordinary costs, conditions and damage-source restrictions remain.",
  "submittedNewChoices": "Per-attack availability, vulnerability even on miss/cancellation, exact next-start persistence.",
  "submittedWorkedCases": [
    "A longsword1d8 attack gains1d8; if critical, roll4d8 plus flat modifiers.",
    "You attack an unseen target: advantage and disadvantage cancel, but the extra die on a hit and attacks-against advantage still apply."
  ],
  "decision": "Retain the full CF-26 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Per-attack availability, vulnerability even on miss/cancellation, exact next-start persistence.",
  "completeAuthoringProcedure": "Before any melee weapon attack roll, you may declare Reckless Swing. That one attack gains advantage and adds one base weapon damage die if it hits; critical doubles that additional attack die. Regardless of hit, miss or advantage cancellation, all attacks against you have advantage through your next original regular start. Repeated declarations on separately legal attacks can each supply their one die but do not stack attacker advantage or create attacks; overlapping vulnerability records retain the same next-start deadline. This is not a rage and has no resistance or ability-score substitution. Spell, thrown ranged and unarmed attacks do not qualify; actual natural weapon melee attacks do. Ordinary costs, conditions and damage-source restrictions remain.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A longsword1d8 attack gains1d8; if critical, roll4d8 plus flat modifiers.",
    "You attack an unseen target: advantage and disadvantage cancel, but the extra die on a hit and attacks-against advantage still apply."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Before any melee weapon attack roll, you may declare Reckless Swing. That one attack gains advantage and adds one base weapon damage die if it hits; critical doubles that additional attack die. Regardless of hit, miss or advantage cancellation, all attacks against you have advantage through your next original regular start. Repeated declarations on separately legal attacks can each supply their one die but do not stack attacker advantage or create attacks; overlapping vulnerability records retain the same next-start deadline. This is not a rage and has no resistance or ability-score substitution. Spell, thrown ranged and unarmed attacks do not qualify; actual natural weapon melee attacks do. Ordinary costs, conditions and damage-source restrictions remain.

### Original-position authored review references

```json
[
  {
    "id": "CF-26-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/50"
  },
  {
    "id": "CF-26-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/51"
  }
]
```

## CF-27 — Riposte

### Complete original object

```json
{
  "id": "riposte",
  "name": "Riposte",
  "description": "You can quickly counterattack after successfully defending.",
  "prerequisite": "Agility 15+, Melee Proficiency",
  "effect": "Free attack after dodge/parry",
  "type": "Combat",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

### Original question

```json
"Resolve Agility15+ against the actual ability taxonomy and Melee Proficiency against existing credentials. Define dodge/parry success, trigger timing, legal target/reach, Action/Reaction cost, frequency and recursive counterattack prevention. 'Free attack' is not a completed action rule."
```

### Preserved original source direction (historical)

```json
{
  "featId": "riposte",
  "name": "Riposte",
  "cohort": "combat",
  "questionId": "CF-27",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/26",
  "originalQuestion": "Resolve Agility15+ against the actual ability taxonomy and Melee Proficiency against existing credentials. Define dodge/parry success, trigger timing, legal target/reach, Action/Reaction cost, frequency and recursive counterattack prevention. 'Free attack' is not a completed action rule.",
  "originalSourceObject": {
    "id": "riposte",
    "name": "Riposte",
    "description": "You can quickly counterattack after successfully defending.",
    "prerequisite": "Agility 15+, Melee Proficiency",
    "effect": "Free attack after dodge/parry",
    "type": "Combat",
    "draft": false,
    "deprecated": false,
    "needsReview": false
  },
  "originalSourceObjectSha256AsSubmitted": "0e038f863262d755cafb22aaf670b2175b7eef9faaa2f36798bcbe280a664d4f",
  "submittedProcedure": "NEW acquisition bridge: the legacy Agility15 means DEX15 for this feat only; Melee Proficiency means actual proficiency with at least one melee weapon. After a hostile melee attack against you misses while your active Dodge actually applies to it, OR after an actual sourced Parry/Deflect effect expressly turns that attack into a miss, you may spend your available Reaction to make one legal melee weapon attack against that same attacker in reach. No movement or extra Reaction is granted. A parry that merely reduces damage is insufficient; missing for ordinary AC without qualifying Dodge/Parry is insufficient. If the defensive effect already used your only Reaction, you cannot also riposte. A permitted additional Reaction must explicitly allow an attack; defensive-only grants cannot pay. Apply shared causal-root prohibition on counterattack chains. Once per original regular-start interval even if another source grants extra attack-capable Reactions.",
  "submittedNewChoices": "Explicit Agility→DEX bridge, qualifying miss, Reaction instead of unspecified free action, interval and causal cap.",
  "submittedWorkedCases": [
    "While Dodging with Speed30, a seen adjacent enemy misses; spend the available Reaction for one weapon attack.",
    "A paid parry used the only Reaction to cause a miss. No Reaction remains for Riposte; reducing a hit to0damage would not qualify anyway."
  ],
  "decision": "Retain the full CF-27 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Explicit Agility→DEX bridge, qualifying miss, Reaction instead of unspecified free action, interval and causal cap.",
  "completeAuthoringProcedure": "NEW acquisition bridge: the legacy Agility15 means DEX15 for this feat only; Melee Proficiency means actual proficiency with at least one melee weapon. After a hostile melee attack against you misses while your active Dodge actually applies to it, OR after an actual sourced Parry/Deflect effect expressly turns that attack into a miss, you may spend your available Reaction to make one legal melee weapon attack against that same attacker in reach. No movement or extra Reaction is granted. A parry that merely reduces damage is insufficient; missing for ordinary AC without qualifying Dodge/Parry is insufficient. If the defensive effect already used your only Reaction, you cannot also riposte. A permitted additional Reaction must explicitly allow an attack; defensive-only grants cannot pay. Apply shared causal-root prohibition on counterattack chains. Once per original regular-start interval even if another source grants extra attack-capable Reactions.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "While Dodging with Speed30, a seen adjacent enemy misses; spend the available Reaction for one weapon attack.",
    "A paid parry used the only Reaction to cause a miss. No Reaction remains for Riposte; reducing a hit to0damage would not qualify anyway."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW acquisition bridge: the legacy Agility15 means DEX15 for this feat only; Melee Proficiency means actual proficiency with at least one melee weapon. After a hostile melee attack against you misses while your active Dodge actually applies to it, OR after an actual sourced Parry/Deflect effect expressly turns that attack into a miss, you may spend your available Reaction to make one legal melee weapon attack against that same attacker in reach. No movement or extra Reaction is granted. A parry that merely reduces damage is insufficient; missing for ordinary AC without qualifying Dodge/Parry is insufficient. If the defensive effect already used your only Reaction, you cannot also riposte. A permitted additional Reaction must explicitly allow an attack; defensive-only grants cannot pay. Apply shared causal-root prohibition on counterattack chains. Once per original regular-start interval even if another source grants extra attack-capable Reactions.

### Original-position authored review references

```json
[
  {
    "id": "CF-27-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/52"
  },
  {
    "id": "CF-27-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/53"
  }
]
```

## CF-28 — Savage Momentum

### Complete original object

```json
{
  "id": "savage_momentum",
  "name": "Savage Momentum",
  "description": "Strength 14+ and melee training support the listed +5% damage per consecutive hit.",
  "prerequisite": "Strength 14+, Melee",
  "effect": "Once per turn, after hitting the same creature with consecutive melee attacks, add +1 damage for each prior consecutive hit, to a maximum equal to your proficiency bonus. The chain ends when you miss or change targets.",
  "type": "Combat",
  "legacyEffect": "+5% dmg per consecutive hit",
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
"Define consecutive hit chain scope, turns/encounters/off-turn attacks, target changes, misses and nonattack interruptions. Resolve when the once-per-turn bonus is chosen and prior hits counted, PB cap and chain state through target death/transformation."
```

### Preserved original source direction (historical)

```json
{
  "featId": "savage_momentum",
  "name": "Savage Momentum",
  "cohort": "combat",
  "questionId": "CF-28",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/27",
  "originalQuestion": "Define consecutive hit chain scope, turns/encounters/off-turn attacks, target changes, misses and nonattack interruptions. Resolve when the once-per-turn bonus is chosen and prior hits counted, PB cap and chain state through target death/transformation.",
  "originalSourceObject": {
    "id": "savage_momentum",
    "name": "Savage Momentum",
    "description": "Strength 14+ and melee training support the listed +5% damage per consecutive hit.",
    "prerequisite": "Strength 14+, Melee",
    "effect": "Once per turn, after hitting the same creature with consecutive melee attacks, add +1 damage for each prior consecutive hit, to a maximum equal to your proficiency bonus. The chain ends when you miss or change targets.",
    "type": "Combat",
    "legacyEffect": "+5% dmg per consecutive hit",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "bf337afcc868a6ef9fa32e3e7ae219cb37dd8db948349b5a815942c940d1df40",
  "submittedProcedure": "Track a consecutive direct melee-attack hit chain for each owner during one encounter. Every actual melee attack you make advances the event sequence: a hit on the same current target increases the count; a miss or attack directed at a different target ends the old chain, and a hit on the new target starts a new count1. NEW any intervening nonmelee attack also breaks the chain; movement, spellcasting without attacks and nonattack actions do not. Own/off-turn melee attacks participate, but copies/periodic events do not. Once per turn, before rolling a qualifying hit's damage, add min(PB, prior consecutive hits on that target) as a flat native-type bonus. Only declare when at least one prior hit exists; spending on this hit prevents spending on a later hit that turn. The chain persists across regular turn boundaries but ends on target death/removal, encounter conclusion, or loss of that actual creature identity. Transformation of the same surviving identity retains it if target continuity is real.",
  "submittedNewChoices": "Persistent encounter chain, ranged-attack break, state versus bonus budget and zero-prior-hit rule.",
  "submittedWorkedCases": [
    "Three consecutive hits on one foe at PB3 permit choosing+1 on hit2 or+2 on hit3 that turn, not both.",
    "After two hits, a missed opportunity attack breaks the chain. The next melee hit starts at1 and has no prior-hit bonus."
  ],
  "decision": "Retain the full CF-28 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Persistent encounter chain, ranged-attack break, state versus bonus budget and zero-prior-hit rule.",
  "completeAuthoringProcedure": "Track a consecutive direct melee-attack hit chain for each owner during one encounter. Every actual melee attack you make advances the event sequence: a hit on the same current target increases the count; a miss or attack directed at a different target ends the old chain, and a hit on the new target starts a new count1. NEW any intervening nonmelee attack also breaks the chain; movement, spellcasting without attacks and nonattack actions do not. Own/off-turn melee attacks participate, but copies/periodic events do not. Once per turn, before rolling a qualifying hit's damage, add min(PB, prior consecutive hits on that target) as a flat native-type bonus. Only declare when at least one prior hit exists; spending on this hit prevents spending on a later hit that turn. The chain persists across regular turn boundaries but ends on target death/removal, encounter conclusion, or loss of that actual creature identity. Transformation of the same surviving identity retains it if target continuity is real.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Three consecutive hits on one foe at PB3 permit choosing+1 on hit2 or+2 on hit3 that turn, not both.",
    "After two hits, a missed opportunity attack breaks the chain. The next melee hit starts at1 and has no prior-hit bonus."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Track a consecutive direct melee-attack hit chain for each owner during one encounter. Every actual melee attack you make advances the event sequence: a hit on the same current target increases the count; a miss or attack directed at a different target ends the old chain, and a hit on the new target starts a new count1. NEW any intervening nonmelee attack also breaks the chain; movement, spellcasting without attacks and nonattack actions do not. Own/off-turn melee attacks participate, but copies/periodic events do not. Once per turn, before rolling a qualifying hit's damage, add min(PB, prior consecutive hits on that target) as a flat native-type bonus. Only declare when at least one prior hit exists; spending on this hit prevents spending on a later hit that turn. The chain persists across regular turn boundaries but ends on target death/removal, encounter conclusion, or loss of that actual creature identity. Transformation of the same surviving identity retains it if target continuity is real.

### Original-position authored review references

```json
[
  {
    "id": "CF-28-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/54"
  },
  {
    "id": "CF-28-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/55"
  }
]
```

## CF-29 — Shattering Smash

### Complete original object

```json
{
  "id": "shattering_smash",
  "name": "Shattering Smash",
  "description": "Strength 16+ supports the listed ability to break an enemy shield or block.",
  "prerequisite": "Strength 16+",
  "effect": "When you hit a creature using a shield or maintaining a physical block, forgo one damage die to force a Strength save. On a failure, its shield bonus or block benefit is suppressed until the start of its next turn.",
  "type": "Combat",
  "legacyEffect": "Break enemy shield or block",
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
"Complete missing save DC and attack scope. Define actual physical block, one damage-die cost, declaration, save timing and suppression of ordinary shield AC versus magical enhancement/other block benefits. Do not damage/destroy equipment by implication."
```

### Preserved original source direction (historical)

```json
{
  "featId": "shattering_smash",
  "name": "Shattering Smash",
  "cohort": "combat",
  "questionId": "CF-29",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/28",
  "originalQuestion": "Complete missing save DC and attack scope. Define actual physical block, one damage-die cost, declaration, save timing and suppression of ordinary shield AC versus magical enhancement/other block benefits. Do not damage/destroy equipment by implication.",
  "originalSourceObject": {
    "id": "shattering_smash",
    "name": "Shattering Smash",
    "description": "Strength 16+ supports the listed ability to break an enemy shield or block.",
    "prerequisite": "Strength 16+",
    "effect": "When you hit a creature using a shield or maintaining a physical block, forgo one damage die to force a Strength save. On a failure, its shield bonus or block benefit is suppressed until the start of its next turn.",
    "type": "Combat",
    "legacyEffect": "Break enemy shield or block",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "6d2ee9476cdb43d8abaad9df62fc6e48788d602c3d14fa3a9cecf2f1002938e9",
  "submittedProcedure": "On a melee weapon attack hit against a creature receiving an actual wielded shield AC contribution or a sourced current physical-block benefit, before rolling damage forgo one base weapon die under the same pre-critical payment contract as Disarming Blow. NEW save is STR DC8+PB+the actual attack ability modifier. Resolve remaining damage, then on failed save suppress either the chosen shield's entire AC contribution (including its own enhancement) or one selected block benefit through the target's next original regular start. No destruction, durability loss, forced drop or suppression of unrelated item traits; independent magical barriers/unarmored formulas remain. A shield-dependent feat AC bonus is suppressed while its shield cannot supply defensive contribution. Physical block means a named sourced defense actually interposing a held body/object; ordinary armor, cover terrain and taking Dodge do not alone qualify. Same-identity suppression does not multiply, and separate expiries remain. You cannot spend the same die on another rider.",
  "submittedNewChoices": "Melee scope, missing save DC, pre-critical payment and entire chosen shield AC contribution with dependency suppression.",
  "submittedWorkedCases": [
    "A shield contributes2 plus1enhancement. Failure suppresses those3 until the target's next regular start; the shield is not broken.",
    "A one-die sword cannot pay both Shattering Smash and Disarming Blow from the same die. A two-die weapon may pay distinct dice if both targets/effects qualify."
  ],
  "decision": "Retain the full CF-29 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Melee scope, missing save DC, pre-critical payment and entire chosen shield AC contribution with dependency suppression.",
  "completeAuthoringProcedure": "On a melee weapon attack hit against a creature receiving an actual wielded shield AC contribution or a sourced current physical-block benefit, before rolling damage forgo one base weapon die under the same pre-critical payment contract as Disarming Blow. NEW save is STR DC8+PB+the actual attack ability modifier. Resolve remaining damage, then on failed save suppress either the chosen shield's entire AC contribution (including its own enhancement) or one selected block benefit through the target's next original regular start. No destruction, durability loss, forced drop or suppression of unrelated item traits; independent magical barriers/unarmored formulas remain. A shield-dependent feat AC bonus is suppressed while its shield cannot supply defensive contribution. Physical block means a named sourced defense actually interposing a held body/object; ordinary armor, cover terrain and taking Dodge do not alone qualify. Same-identity suppression does not multiply, and separate expiries remain. You cannot spend the same die on another rider.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A shield contributes2 plus1enhancement. Failure suppresses those3 until the target's next regular start; the shield is not broken.",
    "A one-die sword cannot pay both Shattering Smash and Disarming Blow from the same die. A two-die weapon may pay distinct dice if both targets/effects qualify."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

On a melee weapon attack hit against a creature receiving an actual wielded shield AC contribution or a sourced current physical-block benefit, before rolling damage forgo one base weapon die under the same pre-critical payment contract as Disarming Blow. NEW save is STR DC8+PB+the actual attack ability modifier. Resolve remaining damage, then on failed save suppress either the chosen shield's entire AC contribution (including its own enhancement) or one selected block benefit through the target's next original regular start. No destruction, durability loss, forced drop or suppression of unrelated item traits; independent magical barriers/unarmored formulas remain. A shield-dependent feat AC bonus is suppressed while its shield cannot supply defensive contribution. Physical block means a named sourced defense actually interposing a held body/object; ordinary armor, cover terrain and taking Dodge do not alone qualify. Same-identity suppression does not multiply, and separate expiries remain. You cannot spend the same die on another rider.

### Original-position authored review references

```json
[
  {
    "id": "CF-29-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/56"
  },
  {
    "id": "CF-29-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/57"
  }
]
```

## CF-30 — Shield Bash

### Complete original object

```json
{
  "id": "shield_bash",
  "name": "Shield Bash",
  "description": "Strength 13+ supports the listed shield stun against an enemy.",
  "prerequisite": "Strength 13+",
  "effect": "After taking the Attack action while wielding a shield, make a shield bash as a bonus action. On a hit, deal 1d4 + Strength bludgeoning damage; once per short rest, force a Constitution save or stun the target until the start of its next turn.",
  "type": "Combat",
  "legacyEffect": "Stun enemy with shield",
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
"Supply attack ability/proficiency/weapon classification, range, shield-hand use and missing stun DC. Bind Attack-action prerequisite, Bonus Action, one-short-rest use declaration/payment and Stunned expiry; distinguish the shield from a new priced weapon."
```

### Preserved original source direction (historical)

```json
{
  "featId": "shield_bash",
  "name": "Shield Bash",
  "cohort": "combat",
  "questionId": "CF-30",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/29",
  "originalQuestion": "Supply attack ability/proficiency/weapon classification, range, shield-hand use and missing stun DC. Bind Attack-action prerequisite, Bonus Action, one-short-rest use declaration/payment and Stunned expiry; distinguish the shield from a new priced weapon.",
  "originalSourceObject": {
    "id": "shield_bash",
    "name": "Shield Bash",
    "description": "Strength 13+ supports the listed shield stun against an enemy.",
    "prerequisite": "Strength 13+",
    "effect": "After taking the Attack action while wielding a shield, make a shield bash as a bonus action. On a hit, deal 1d4 + Strength bludgeoning damage; once per short rest, force a Constitution save or stun the target until the start of its next turn.",
    "type": "Combat",
    "legacyEffect": "Stun enemy with shield",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "c7a519bfb45ac6ee9acec502ada6291cea5646ec704510a9a8f7e2f307bfe721",
  "submittedProcedure": "After you take the Attack Action on your own turn while actually wielding a usable shield, you may spend BA that turn to bash a creature within5ft. NEW this is a melee weapon attack using STR, adding PB if you are proficient with shields; the shield remains an armor/shield object, not a new purchasable weapon identity. It deals1d4+STR bludgeoning, minimum0, with ordinary critical doubling. A buckler counts only if its actual profile allows a striking shield body; this feat does not conjure a free weapon or bypass the shield hand. Once per short rest, after a bash hits and before damage, spend the stun use; target CON save DC8+PB+STR after damage. Failure applies Stunned until the target's next original regular start. Immunity and the source-character hard-denial cap apply; spent use is not refunded. This endpoint deliberately does not steal the target's whole next regular turn. No grant of another BA or off-turn bash.",
  "submittedNewChoices": "Actual shield proficiency attack bridge,5ft/STR/DC, hit-stage stun payment and shared hard-denial cap.",
  "submittedWorkedCases": [
    "STR+3/PB3 bash attacks at+6 for1d4+3; the optional stun save isDC14.",
    "A stun applied just after the enemy's turn can block intervening Reactions, but expires at that enemy's next start before voluntary decisions."
  ],
  "decision": "Retain the full CF-30 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Actual shield proficiency attack bridge,5ft/STR/DC, hit-stage stun payment and shared hard-denial cap.",
  "completeAuthoringProcedure": "After you take the Attack Action on your own turn while actually wielding a usable shield, you may spend BA that turn to bash a creature within5ft. NEW this is a melee weapon attack using STR, adding PB if you are proficient with shields; the shield remains an armor/shield object, not a new purchasable weapon identity. It deals1d4+STR bludgeoning, minimum0, with ordinary critical doubling. A buckler counts only if its actual profile allows a striking shield body; this feat does not conjure a free weapon or bypass the shield hand. Once per short rest, after a bash hits and before damage, spend the stun use; target CON save DC8+PB+STR after damage. Failure applies Stunned until the target's next original regular start. Immunity and the source-character hard-denial cap apply; spent use is not refunded. This endpoint deliberately does not steal the target's whole next regular turn. No grant of another BA or off-turn bash.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "STR+3/PB3 bash attacks at+6 for1d4+3; the optional stun save isDC14.",
    "A stun applied just after the enemy's turn can block intervening Reactions, but expires at that enemy's next start before voluntary decisions."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

After you take the Attack Action on your own turn while actually wielding a usable shield, you may spend BA that turn to bash a creature within5ft. NEW this is a melee weapon attack using STR, adding PB if you are proficient with shields; the shield remains an armor/shield object, not a new purchasable weapon identity. It deals1d4+STR bludgeoning, minimum0, with ordinary critical doubling. A buckler counts only if its actual profile allows a striking shield body; this feat does not conjure a free weapon or bypass the shield hand. Once per short rest, after a bash hits and before damage, spend the stun use; target CON save DC8+PB+STR after damage. Failure applies Stunned until the target's next original regular start. Immunity and the source-character hard-denial cap apply; spent use is not refunded. This endpoint deliberately does not steal the target's whole next regular turn. No grant of another BA or off-turn bash.

### Original-position authored review references

```json
[
  {
    "id": "CF-30-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/58"
  },
  {
    "id": "CF-30-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/59"
  }
]
```

## CF-31 — Shield Expert

### Complete original object

```json
{
  "id": "shield_expert",
  "name": "Shield Expert",
  "description": "Shield Proficiency supports the listed +2 AC and +10% block chance.",
  "prerequisite": "Shield Proficiency",
  "effect": "Gain +1 AC while wielding a shield. When a Dexterity save would deal half damage, use your reaction to take no damage on a success while your shield can interpose.",
  "type": "Combat",
  "legacyEffect": "+2 AC and +10% block chance",
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
"Bind the+1 AC as a separate actual eligible modifier and worn/wielded shield requirements. Define interposition, Reaction timing on a successful Dexterity half-damage save, area/cover geometry, rerolls and no change to failed saves."
```

### Preserved original source direction (historical)

```json
{
  "featId": "shield_expert",
  "name": "Shield Expert",
  "cohort": "combat",
  "questionId": "CF-31",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/30",
  "originalQuestion": "Bind the+1 AC as a separate actual eligible modifier and worn/wielded shield requirements. Define interposition, Reaction timing on a successful Dexterity half-damage save, area/cover geometry, rerolls and no change to failed saves.",
  "originalSourceObject": {
    "id": "shield_expert",
    "name": "Shield Expert",
    "description": "Shield Proficiency supports the listed +2 AC and +10% block chance.",
    "prerequisite": "Shield Proficiency",
    "effect": "Gain +1 AC while wielding a shield. When a Dexterity save would deal half damage, use your reaction to take no damage on a success while your shield can interpose.",
    "type": "Combat",
    "legacyEffect": "+2 AC and +10% block chance",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "c3b170d50690910dbf6b463c33db0513a887c857f59679acc1fee6a8b5f6ae75",
  "submittedProcedure": "While proficiently wielding a usable actual shield that supplies its defensive contribution, gain+1AC as this feat's separate modifier; duplicate copies do not stack. If you succeed on a DEX save whose printed ordinary success would deal half damage, you may spend Reaction before damage to take0 from that save's damage event. NEW your shield must physically interpose against the effect's actual incoming origin/line; it cannot block an effect originating inside your body or bypass an express shield-ignoring clause. Area eligibility follows actual origin-to-target line and the same cover geometry; an all-around explosion is not automatically unblockable if a real incoming line can be interposed. Other conditions or nondamage consequences remain. Failed saves receive no reduction; a successful reroll can qualify before damage, consuming only one Reaction. If another feature already made the damage0, spending this Reaction is unnecessary.",
  "submittedNewChoices": "AC dependence and successful-save timing; concrete interposition scope without universal area immunity.",
  "submittedWorkedCases": [
    "A successful DEX save would halve12fire to6; a legal shield interposition Reaction changes that damage to0.",
    "A failed save still deals normal failure damage; this feat does not turn failure into a success or remove an attached condition."
  ],
  "decision": "Retain the full CF-31 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. AC dependence and successful-save timing; concrete interposition scope without universal area immunity.",
  "completeAuthoringProcedure": "While proficiently wielding a usable actual shield that supplies its defensive contribution, gain+1AC as this feat's separate modifier; duplicate copies do not stack. If you succeed on a DEX save whose printed ordinary success would deal half damage, you may spend Reaction before damage to take0 from that save's damage event. NEW your shield must physically interpose against the effect's actual incoming origin/line; it cannot block an effect originating inside your body or bypass an express shield-ignoring clause. Area eligibility follows actual origin-to-target line and the same cover geometry; an all-around explosion is not automatically unblockable if a real incoming line can be interposed. Other conditions or nondamage consequences remain. Failed saves receive no reduction; a successful reroll can qualify before damage, consuming only one Reaction. If another feature already made the damage0, spending this Reaction is unnecessary.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A successful DEX save would halve12fire to6; a legal shield interposition Reaction changes that damage to0.",
    "A failed save still deals normal failure damage; this feat does not turn failure into a success or remove an attached condition."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

While proficiently wielding a usable actual shield that supplies its defensive contribution, gain+1AC as this feat's separate modifier; duplicate copies do not stack. If you succeed on a DEX save whose printed ordinary success would deal half damage, you may spend Reaction before damage to take0 from that save's damage event. NEW your shield must physically interpose against the effect's actual incoming origin/line; it cannot block an effect originating inside your body or bypass an express shield-ignoring clause. Area eligibility follows actual origin-to-target line and the same cover geometry; an all-around explosion is not automatically unblockable if a real incoming line can be interposed. Other conditions or nondamage consequences remain. Failed saves receive no reduction; a successful reroll can qualify before damage, consuming only one Reaction. If another feature already made the damage0, spending this Reaction is unnecessary.

### Original-position authored review references

```json
[
  {
    "id": "CF-31-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/60"
  },
  {
    "id": "CF-31-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/61"
  }
]
```

## CF-32 — Sure Shot

### Complete original object

```json
{
  "id": "sure_shot",
  "name": "Sure Shot",
  "description": "Dexterity 14+ and Ranged Proficiency support the listed armor ignore on ranged attacks.",
  "prerequisite": "Dexterity 14+, Ranged Proficiency",
  "effect": "Your ranged weapon attacks ignore 2 points of AC granted by armor or cover. This does not ignore magical barriers.",
  "type": "Combat",
  "legacyEffect": "Ranged attacks ignore 25% armor",
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
"Define attribution of up to2 AC to armor or cover across suit formulas, natural/unarmored defenses, shields, negative grades and magical enhancement. Identify what counts as a magical barrier and preserve total-cover targeting limits."
```

### Preserved original source direction (historical)

```json
{
  "featId": "sure_shot",
  "name": "Sure Shot",
  "cohort": "combat",
  "questionId": "CF-32",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/31",
  "originalQuestion": "Define attribution of up to2 AC to armor or cover across suit formulas, natural/unarmored defenses, shields, negative grades and magical enhancement. Identify what counts as a magical barrier and preserve total-cover targeting limits.",
  "originalSourceObject": {
    "id": "sure_shot",
    "name": "Sure Shot",
    "description": "Dexterity 14+ and Ranged Proficiency support the listed armor ignore on ranged attacks.",
    "prerequisite": "Dexterity 14+, Ranged Proficiency",
    "effect": "Your ranged weapon attacks ignore 2 points of AC granted by armor or cover. This does not ignore magical barriers.",
    "type": "Combat",
    "legacyEffect": "Ranged attacks ignore 25% armor",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "e402bb794f8f9b9883f0f593ff6f8ccca9361e299bae3cb6dbb88216b07dbe85",
  "submittedProcedure": "For your ranged weapon attacks, ignore up to2 points of actual target AC attributable to worn physical armor or ordinary cover, combined rather than2 from each. NEW compute physical armor contribution as max(0, the actual suit base AC including its grade minus10), excluding all DEX contribution and magic enhancement; do not count an unarmored/natural-armor formula, shield, independent feat AC or magical enhancement as suit contribution. An actual magical armor enhancement is not removable here; physical base armor still is. Ordinary half/three-quarters cover can supply removable points; a magical barrier's cover/AC cannot. Choose eligible cover contribution first, then suit, up to2 total. This is a target-specific attack comparison, not a lasting AC reduction. Total cover remains untargetable even if physically supplied. Spell attacks and a thrown melee-class weapon are not ranged-weapon attacks for this classification unless its actual profile also says ranged.",
  "submittedNewChoices": "Explicit suit-baseline attribution, combined2-point budget, exclusion of shield/natural/enchanted contribution and range classification.",
  "submittedWorkedCases": [
    "A chain-armored target with actualAC16 is compared at14 for a legal ranged weapon attack.",
    "Leather base11 plusDEX5 givesAC16 but only1 point of physical armor: compareAC15, preservingDEX5. Ordinary half cover can instead supply2; total cover still blocks, and a magical barrier's+2 stays."
  ],
  "decision": "Retain the full CF-32 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Explicit suit-baseline attribution, combined2-point budget, exclusion of shield/natural/enchanted contribution and range classification.",
  "completeAuthoringProcedure": "For your ranged weapon attacks, ignore up to2 points of actual target AC attributable to worn physical armor or ordinary cover, combined rather than2 from each. NEW compute physical armor contribution as max(0, the actual suit base AC including its grade minus10), excluding all DEX contribution and magic enhancement; do not count an unarmored/natural-armor formula, shield, independent feat AC or magical enhancement as suit contribution. An actual magical armor enhancement is not removable here; physical base armor still is. Ordinary half/three-quarters cover can supply removable points; a magical barrier's cover/AC cannot. Choose eligible cover contribution first, then suit, up to2 total. This is a target-specific attack comparison, not a lasting AC reduction. Total cover remains untargetable even if physically supplied. Spell attacks and a thrown melee-class weapon are not ranged-weapon attacks for this classification unless its actual profile also says ranged.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A chain-armored target with actualAC16 is compared at14 for a legal ranged weapon attack.",
    "Leather base11 plusDEX5 givesAC16 but only1 point of physical armor: compareAC15, preservingDEX5. Ordinary half cover can instead supply2; total cover still blocks, and a magical barrier's+2 stays."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

For your ranged weapon attacks, ignore up to2 points of actual target AC attributable to worn physical armor or ordinary cover, combined rather than2 from each. NEW compute physical armor contribution as max(0, the actual suit base AC including its grade minus10), excluding all DEX contribution and magic enhancement; do not count an unarmored/natural-armor formula, shield, independent feat AC or magical enhancement as suit contribution. An actual magical armor enhancement is not removable here; physical base armor still is. Ordinary half/three-quarters cover can supply removable points; a magical barrier's cover/AC cannot. Choose eligible cover contribution first, then suit, up to2 total. This is a target-specific attack comparison, not a lasting AC reduction. Total cover remains untargetable even if physically supplied. Spell attacks and a thrown melee-class weapon are not ranged-weapon attacks for this classification unless its actual profile also says ranged.

### Original-position authored review references

```json
[
  {
    "id": "CF-32-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/62"
  },
  {
    "id": "CF-32-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/63"
  }
]
```

## CF-33 — Tactical Flanker

### Complete original object

```json
{
  "id": "tactical_flanker",
  "name": "Tactical Flanker",
  "description": "Intelligence 12+ and Melee support the listed ally damage while flanking with you.",
  "prerequisite": "Intelligence 12+, Melee",
  "effect": "Once per turn when you and an ally flank a creature, one of you adds 1d6 damage to a successful melee attack against it.",
  "type": "Combat",
  "legacyEffect": "Allies gain +1d6 dmg when flanking with you",
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
"Supply or locate the exact current flanking geometry. Define which owner's once-per-turn budget funds which ally attack, designation timing, same-hit collisions across owners, damage type and no duplicated1d6 from one triggering application."
```

### Preserved original source direction (historical)

```json
{
  "featId": "tactical_flanker",
  "name": "Tactical Flanker",
  "cohort": "combat",
  "questionId": "CF-33",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/32",
  "originalQuestion": "Supply or locate the exact current flanking geometry. Define which owner's once-per-turn budget funds which ally attack, designation timing, same-hit collisions across owners, damage type and no duplicated1d6 from one triggering application.",
  "originalSourceObject": {
    "id": "tactical_flanker",
    "name": "Tactical Flanker",
    "description": "Intelligence 12+ and Melee support the listed ally damage while flanking with you.",
    "prerequisite": "Intelligence 12+, Melee",
    "effect": "Once per turn when you and an ally flank a creature, one of you adds 1d6 damage to a successful melee attack against it.",
    "type": "Combat",
    "legacyEffect": "Allies gain +1d6 dmg when flanking with you",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "c815d330d29a6c4f9c52eb582a3e634a5be202def2ddc68b6a343bb0ebaa8cbb",
  "submittedProcedure": "NEW feat-only geometry: you and one other willing allied, non-Incapacitated creature each threaten the same enemy with an actual legal melee attack, and the straight segment joining your occupied-space centers crosses the interior of that enemy's occupied footprint, placing you on opposite sides. Measure actual occupied bodies on the current map; a large creature needs opposite sides of its whole footprint, not merely two nearby squares. Both participants must perceive the target and be able to attack it; total cover or unusable reach prevents flanking. This geometry itself grants no universal advantage. Once per turn, when either participant hits that enemy with a melee attack, you may assign your feat allowance to add1d6 of one native damage type to that hit before damage is rolled. No Action/Reaction is required, but you must be conscious and able to coordinate. One successful attack may receive only one Tactical Flanker die across all owners; choose its funding owner before rolling. A critical doubles this attack rider die. Misses spend nothing; using your allowance on an ally prevents using it again on your own hit that actual turn. Perception/reach/geometry must hold at the hit.",
  "submittedNewChoices": "Opposite-side geometry, active coordination, owner-funded allied hit and one family die per attack.",
  "submittedWorkedCases": [
    "Two conscious allies threaten opposite sides of a Medium foe. One owner funds1d6 on the other's hit; a critical makes that rider2d6.",
    "Three feat owners surround a foe. The same hit still receives only one Tactical Flanker die, with one chosen owner's allowance spent."
  ],
  "decision": "Retain the full CF-33 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Opposite-side geometry, active coordination, owner-funded allied hit and one family die per attack.",
  "completeAuthoringProcedure": "NEW feat-only geometry: you and one other willing allied, non-Incapacitated creature each threaten the same enemy with an actual legal melee attack, and the straight segment joining your occupied-space centers crosses the interior of that enemy's occupied footprint, placing you on opposite sides. Measure actual occupied bodies on the current map; a large creature needs opposite sides of its whole footprint, not merely two nearby squares. Both participants must perceive the target and be able to attack it; total cover or unusable reach prevents flanking. This geometry itself grants no universal advantage. Once per turn, when either participant hits that enemy with a melee attack, you may assign your feat allowance to add1d6 of one native damage type to that hit before damage is rolled. No Action/Reaction is required, but you must be conscious and able to coordinate. One successful attack may receive only one Tactical Flanker die across all owners; choose its funding owner before rolling. A critical doubles this attack rider die. Misses spend nothing; using your allowance on an ally prevents using it again on your own hit that actual turn. Perception/reach/geometry must hold at the hit.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Two conscious allies threaten opposite sides of a Medium foe. One owner funds1d6 on the other's hit; a critical makes that rider2d6.",
    "Three feat owners surround a foe. The same hit still receives only one Tactical Flanker die, with one chosen owner's allowance spent."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW feat-only geometry: you and one other willing allied, non-Incapacitated creature each threaten the same enemy with an actual legal melee attack, and the straight segment joining your occupied-space centers crosses the interior of that enemy's occupied footprint, placing you on opposite sides. Measure actual occupied bodies on the current map; a large creature needs opposite sides of its whole footprint, not merely two nearby squares. Both participants must perceive the target and be able to attack it; total cover or unusable reach prevents flanking. This geometry itself grants no universal advantage. Once per turn, when either participant hits that enemy with a melee attack, you may assign your feat allowance to add1d6 of one native damage type to that hit before damage is rolled. No Action/Reaction is required, but you must be conscious and able to coordinate. One successful attack may receive only one Tactical Flanker die across all owners; choose its funding owner before rolling. A critical doubles this attack rider die. Misses spend nothing; using your allowance on an ally prevents using it again on your own hit that actual turn. Perception/reach/geometry must hold at the hit.

### Original-position authored review references

```json
[
  {
    "id": "CF-33-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/64"
  },
  {
    "id": "CF-33-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/65"
  }
]
```

## CF-34 — Target Mark

### Complete original object

```json
{
  "id": "target_mark",
  "name": "Target Mark",
  "description": "Wisdom 14+ and Ranged support the listed mark that increases damage taken by the target.",
  "prerequisite": "Wisdom 14+, Ranged",
  "effect": "As a bonus action, mark a creature you can see within weapon range for 1 minute. The first attack by each ally against it gains +1 to hit. You may maintain only one mark and regain this use after a short rest.",
  "type": "Combat",
  "legacyEffect": "Mark target to take 10% more dmg",
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
"Define weapon range as normal/long and the actual selected weapon; target legality, sight/cover and mark ending/replacement. Resolve first attack by each ally per mark versus per turn, whether self qualifies, application after misses, alliance changes and short-rest recovery."
```

### Preserved original source direction (historical)

```json
{
  "featId": "target_mark",
  "name": "Target Mark",
  "cohort": "combat",
  "questionId": "CF-34",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/33",
  "originalQuestion": "Define weapon range as normal/long and the actual selected weapon; target legality, sight/cover and mark ending/replacement. Resolve first attack by each ally per mark versus per turn, whether self qualifies, application after misses, alliance changes and short-rest recovery.",
  "originalSourceObject": {
    "id": "target_mark",
    "name": "Target Mark",
    "description": "Wisdom 14+ and Ranged support the listed mark that increases damage taken by the target.",
    "prerequisite": "Wisdom 14+, Ranged",
    "effect": "As a bonus action, mark a creature you can see within weapon range for 1 minute. The first attack by each ally against it gains +1 to hit. You may maintain only one mark and regain this use after a short rest.",
    "type": "Combat",
    "legacyEffect": "Mark target to take 10% more dmg",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "13de770f04a50c0d1fdecc80d5a7e1dd1a29325625d95ddfcfbf1af81a6dfcb2",
  "submittedProcedure": "Bonus Action, once per short rest: while holding an actual usable ranged weapon, choose a creature you can see within that weapon's printed maximum legal long range (normal range if no long value) and with line of effect. NEW a thrown weapon with an actual range also qualifies. Record the chosen weapon only to establish activation range; stowing it later does not end the mark. For1minute, the first attack against the marked creature by each other creature currently allied to you gains+1 to hit. This is once per ally identity for the entire mark, not per turn, and is consumed by that attack even if it misses. You are not your own ally for this feat. A creature's later alliance change does not reset its used identity; a newly arriving genuine ally can use its own first attack. Only one mark per owner; replacement, owner death or expiry ends the old record. NEW owner incapacitation does not end an existing mark. No continuous range/tether after activation and no vision/targeting permission is granted. Multiple marks never give more than+1 to the same attack; all applicable unspent first-attack entitlements for that attacker consume on that first event.",
  "submittedNewChoices": "Activation range, no self, whole-mark identity budget, overlap consumption and ending.",
  "submittedWorkedCases": [
    "An ally misses its first attack and later hits in round2. Only the miss received the mark's+1.",
    "Two commanders mark the same target. An ally's first attack gains+1, not+2, and consumes that ally's first-attack entitlement in both marks."
  ],
  "decision": "Keep actual source ally wording including self, with original target/sensory/budget conditions; no generalized automatic self-target for inherently two-person effects.",
  "completeAuthoringProcedure": "Bonus Action, once per short rest: while holding an actual usable weapon, choose a creature you can see within its current melee reach or printed maximum ranged range, with line of effect. A thrown weapon uses its actual range; ordinary long-range disadvantages remain. Record the chosen weapon only to establish activation range; stowing it later does not end the mark. For1minute, the first attack against the marked creature by each creature currently allied to you, including yourself, gains+1 to hit. This is once per ally identity for the entire mark, not per turn, and is consumed by that attack even if it misses. You are an eligible ally for your own mark. A creature's later alliance change does not reset its used identity; a newly arriving genuine ally can use its own first attack. Only one mark per owner; replacement, owner death or expiry ends the old record. NEW owner incapacitation does not end an existing mark. No continuous range/tether after activation and no vision/targeting permission is granted. Multiple marks never give more than+1 to the same attack; all applicable unspent first-attack entitlements for that attacker consume on that first event.\nSOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.\nNEW weapon-range completion: at activation use an actually held, usable weapon’s current reach or printed ranged range, including a melee weapon’s reach; a ranged weapon is not mandatory. Long range does not remove its ordinary disadvantage. Marking does not grant an attack, visibility or line of effect. The mark’s +1 applies to each qualifying ally’s first attack against that target, including the owner’s. Multiple marks of this same feat give one+1 and consume all applicable first-attack entitlements on that event.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Holding a usable melee weapon with5ft reach, the owner can mark a visible legal creature5ft away. Their own first attack against it gains+1 and spends their mark entitlement; stowing the weapon later creates no new activation range or attack.",
    "Two commanders mark the same target. An ally's first attack gains+1, not+2, and consumes that ally's first-attack entitlement in both marks."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Bonus Action, once per short rest: while holding an actual usable weapon, choose a creature you can see within its current melee reach or printed maximum ranged range, with line of effect. A thrown weapon uses its actual range; ordinary long-range disadvantages remain. Record the chosen weapon only to establish activation range; stowing it later does not end the mark. For1minute, the first attack against the marked creature by each creature currently allied to you, including yourself, gains+1 to hit. This is once per ally identity for the entire mark, not per turn, and is consumed by that attack even if it misses. You are an eligible ally for your own mark. A creature's later alliance change does not reset its used identity; a newly arriving genuine ally can use its own first attack. Only one mark per owner; replacement, owner death or expiry ends the old record. NEW owner incapacitation does not end an existing mark. No continuous range/tether after activation and no vision/targeting permission is granted. Multiple marks never give more than+1 to the same attack; all applicable unspent first-attack entitlements for that attacker consume on that first event.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.
NEW weapon-range completion: at activation use an actually held, usable weapon’s current reach or printed ranged range, including a melee weapon’s reach; a ranged weapon is not mandatory. Long range does not remove its ordinary disadvantage. Marking does not grant an attack, visibility or line of effect. The mark’s +1 applies to each qualifying ally’s first attack against that target, including the owner’s. Multiple marks of this same feat give one+1 and consume all applicable first-attack entitlements on that event.

### Original-position authored review references

```json
[
  {
    "id": "CF-34-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/66"
  },
  {
    "id": "CF-34-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/67"
  }
]
```

## CF-35 — Unstoppable Force

### Complete original object

```json
{
  "id": "unstoppable_force",
  "name": "Unstoppable Force",
  "description": "Strength 14+ and Level 8 support the listed +10% knockback chance.",
  "prerequisite": "Strength 14+, Level 8",
  "effect": "When you push or knock a creature, increase the distance by 5 feet. Once per turn, a creature that fails the save by 5 or more is also knocked prone.",
  "type": "Combat",
  "legacyEffect": "+10% knockback chance",
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
"Define push/knock scope including mundane/spell/class effects, whether pulls qualify, bonus displacement limits and blocked movement. Resolve prone on fail-by5 where the original effect uses a contest or no save, cadence and interaction with Bull Rush."
```

### Preserved original source direction (historical)

```json
{
  "featId": "unstoppable_force",
  "name": "Unstoppable Force",
  "cohort": "combat",
  "questionId": "CF-35",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/34",
  "originalQuestion": "Define push/knock scope including mundane/spell/class effects, whether pulls qualify, bonus displacement limits and blocked movement. Resolve prone on fail-by5 where the original effect uses a contest or no save, cadence and interaction with Bull Rush.",
  "originalSourceObject": {
    "id": "unstoppable_force",
    "name": "Unstoppable Force",
    "description": "Strength 14+ and Level 8 support the listed +10% knockback chance.",
    "prerequisite": "Strength 14+, Level 8",
    "effect": "When you push or knock a creature, increase the distance by 5 feet. Once per turn, a creature that fails the save by 5 or more is also knocked prone.",
    "type": "Combat",
    "legacyEffect": "+10% knockback chance",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "9b60ddf1cf5b452b17defd306dac39256be253e9f7a7465ba9bed1c4a1719f30",
  "submittedProcedure": "Whenever your own direct legal effect pushes or knocks a creature a positive specified distance away from you or along its printed outward direction, increase that displacement by5ft. It can modify a weapon, ordinary maneuver, spell or class effect if you are the actual source; not a companion's own effect, pull, teleport, fall, current, carried movement or copy/transfer. Preserve its original size/eligibility/path. Add the5 once per displacement event; same-family copies do not add further5. The final movement still stops at walls, anchors and illegal positions. Once per turn, if that same displacement-producing effect has an actual STR/DEX/other save which the target fails by5 or more, also apply Prone independently of blocked displacement. No save is invented for an ordinary opposed Shove; its numerical contest difference is not a save failure margin. Automatic failure has no numerical margin unless its source explicitly says otherwise. If an original effect already applies Prone, do not duplicate it.",
  "submittedNewChoices": "Positive outward displacement predicate, once-per-event extension and literal saved failure margin.",
  "submittedWorkedCases": [
    "Bull Rush's failed save pushes10ft instead of5; a wall at5 stops it there, but the original Prone still applies.",
    "An ordinary Shove contest succeeds by7. Its push grows to10ft, but no fail-by5 save exists to add Prone."
  ],
  "decision": "Retain the full CF-35 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Positive outward displacement predicate, once-per-event extension and literal saved failure margin.",
  "completeAuthoringProcedure": "Whenever your own direct legal effect pushes or knocks a creature a positive specified distance away from you or along its printed outward direction, increase that displacement by5ft. It can modify a weapon, ordinary maneuver, spell or class effect if you are the actual source; not a companion's own effect, pull, teleport, fall, current, carried movement or copy/transfer. Preserve its original size/eligibility/path. Add the5 once per displacement event; same-family copies do not add further5. The final movement still stops at walls, anchors and illegal positions. Once per turn, if that same displacement-producing effect has an actual STR/DEX/other save which the target fails by5 or more, also apply Prone independently of blocked displacement. No save is invented for an ordinary opposed Shove; its numerical contest difference is not a save failure margin. Automatic failure has no numerical margin unless its source explicitly says otherwise. If an original effect already applies Prone, do not duplicate it.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Bull Rush's failed save pushes10ft instead of5; a wall at5 stops it there, but the original Prone still applies.",
    "An ordinary Shove contest succeeds by7. Its push grows to10ft, but no fail-by5 save exists to add Prone."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Whenever your own direct legal effect pushes or knocks a creature a positive specified distance away from you or along its printed outward direction, increase that displacement by5ft. It can modify a weapon, ordinary maneuver, spell or class effect if you are the actual source; not a companion's own effect, pull, teleport, fall, current, carried movement or copy/transfer. Preserve its original size/eligibility/path. Add the5 once per displacement event; same-family copies do not add further5. The final movement still stops at walls, anchors and illegal positions. Once per turn, if that same displacement-producing effect has an actual STR/DEX/other save which the target fails by5 or more, also apply Prone independently of blocked displacement. No save is invented for an ordinary opposed Shove; its numerical contest difference is not a save failure margin. Automatic failure has no numerical margin unless its source explicitly says otherwise. If an original effect already applies Prone, do not duplicate it.

### Original-position authored review references

```json
[
  {
    "id": "CF-35-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/68"
  },
  {
    "id": "CF-35-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/69"
  }
]
```

## CF-36 — Volley

### Complete original object

```json
{
  "id": "volley",
  "name": "Volley",
  "description": "Level 8 supports the listed rain of arrows in a small area.",
  "prerequisite": "Level 8",
  "effect": "Rain arrows in small area.",
  "type": "Combat",
  "legacyEffect": "Rain arrows in small area",
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
"Complete weapon/ammunition requirements, Action and frequency, area shape/size/origin/range/line, attacks versus saves/DC, target selection, damage, miss outcomes and ammunition expenditure. The retained 'small area' is not an operational template."
```

### Preserved original source direction (historical)

```json
{
  "featId": "volley",
  "name": "Volley",
  "cohort": "combat",
  "questionId": "CF-36",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/35",
  "originalQuestion": "Complete weapon/ammunition requirements, Action and frequency, area shape/size/origin/range/line, attacks versus saves/DC, target selection, damage, miss outcomes and ammunition expenditure. The retained 'small area' is not an operational template.",
  "originalSourceObject": {
    "id": "volley",
    "name": "Volley",
    "description": "Level 8 supports the listed rain of arrows in a small area.",
    "prerequisite": "Level 8",
    "effect": "Rain arrows in small area.",
    "type": "Combat",
    "legacyEffect": "Rain arrows in small area",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "df1c2d11d1a8c2f4980bbd3a79ac57a6c5eb1c07ce51ecd5a952802bf0cdd466",
  "submittedProcedure": "NEW full completion: Action, once per short rest, wield a loaded/properly supplied bow using arrows and choose a visible point within that bow's actual normal range and line of effect. Select up to PB distinct perceived creatures in a10ft-radius area around that point, each independently in normal range and with a legal shot. You may exclude allies; no hidden-target scan or compulsory friendly fire is added. Lock targets/order, spend the use and one actual arrow per selected target, then make one separate normal ranged weapon attack against each. Apply actual AC, cover, proficiency, crits and ordinary native bow damage to each; there is no area save/DC or shared damage roll. Extra Attack does not multiply this special Action. Each target at most once; newly entering creatures cannot replace lost targets. A target becoming illegal before its shot is skipped and its committed arrow remains spent. Interrupted remaining shots lose the use and committed ammunition. Loading/reload and all other item restrictions remain, so a weapon that cannot fire the necessary arrows cannot declare that many shots. It is a special Volley Action, not Attack Action for Double Tap or Eldritch Combat.",
  "submittedNewChoices": "Entire bow/Action/SR/PB-target/10ft-radius/normal-range/individual-attacks/committed-ammunition completion.",
  "submittedWorkedCases": [
    "PB3 with a bow selects three enemies and commits3arrows; roll three separate attacks and damage only actual hits.",
    "A wall gives one target total cover before its shot. Skip it without a replacement target or arrow refund; the other legal shots remain."
  ],
  "decision": "Retain the full CF-36 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Entire bow/Action/SR/PB-target/10ft-radius/normal-range/individual-attacks/committed-ammunition completion.",
  "completeAuthoringProcedure": "NEW full completion: Action, once per short rest, wield a loaded/properly supplied bow using arrows and choose a visible point within that bow's actual normal range and line of effect. Select up to PB distinct perceived creatures in a10ft-radius area around that point, each independently in normal range and with a legal shot. You may exclude allies; no hidden-target scan or compulsory friendly fire is added. Lock targets/order, spend the use and one actual arrow per selected target, then make one separate normal ranged weapon attack against each. Apply actual AC, cover, proficiency, crits and ordinary native bow damage to each; there is no area save/DC or shared damage roll. Extra Attack does not multiply this special Action. Each target at most once; newly entering creatures cannot replace lost targets. A target becoming illegal before its shot is skipped and its committed arrow remains spent. Interrupted remaining shots lose the use and committed ammunition. Loading/reload and all other item restrictions remain, so a weapon that cannot fire the necessary arrows cannot declare that many shots. It is a special Volley Action, not Attack Action for Double Tap or Eldritch Combat.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "PB3 with a bow selects three enemies and commits3arrows; roll three separate attacks and damage only actual hits.",
    "A wall gives one target total cover before its shot. Skip it without a replacement target or arrow refund; the other legal shots remain."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW full completion: Action, once per short rest, wield a loaded/properly supplied bow using arrows and choose a visible point within that bow's actual normal range and line of effect. Select up to PB distinct perceived creatures in a10ft-radius area around that point, each independently in normal range and with a legal shot. You may exclude allies; no hidden-target scan or compulsory friendly fire is added. Lock targets/order, spend the use and one actual arrow per selected target, then make one separate normal ranged weapon attack against each. Apply actual AC, cover, proficiency, crits and ordinary native bow damage to each; there is no area save/DC or shared damage roll. Extra Attack does not multiply this special Action. Each target at most once; newly entering creatures cannot replace lost targets. A target becoming illegal before its shot is skipped and its committed arrow remains spent. Interrupted remaining shots lose the use and committed ammunition. Loading/reload and all other item restrictions remain, so a weapon that cannot fire the necessary arrows cannot declare that many shots. It is a special Volley Action, not Attack Action for Double Tap or Eldritch Combat.

### Original-position authored review references

```json
[
  {
    "id": "CF-36-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/70"
  },
  {
    "id": "CF-36-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/71"
  }
]
```

## CF-37 — Weapon Finesse

### Complete original object

```json
{
  "id": "weapon_finesse",
  "name": "Weapon Finesse",
  "description": "Dexterity 15+ supports using Dexterity for melee attack rolls.",
  "prerequisite": "Dexterity 15+",
  "effect": "Use Dexterity for melee attack rolls.",
  "type": "Combat",
  "legacyEffect": "Use Dexterity for melee attack rolls",
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
"Bind eligible melee attack types, actual weapon/natural/unarmed distinctions and attack-only versus damage ability. Preserve Strength-dependent prerequisites and weapon properties unless an explicit completion changes them."
```

### Preserved original source direction (historical)

```json
{
  "featId": "weapon_finesse",
  "name": "Weapon Finesse",
  "cohort": "combat",
  "questionId": "CF-37",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/36",
  "originalQuestion": "Bind eligible melee attack types, actual weapon/natural/unarmed distinctions and attack-only versus damage ability. Preserve Strength-dependent prerequisites and weapon properties unless an explicit completion changes them.",
  "originalSourceObject": {
    "id": "weapon_finesse",
    "name": "Weapon Finesse",
    "description": "Dexterity 15+ supports using Dexterity for melee attack rolls.",
    "prerequisite": "Dexterity 15+",
    "effect": "Use Dexterity for melee attack rolls.",
    "type": "Combat",
    "legacyEffect": "Use Dexterity for melee attack rolls",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "85b42094189bf2563c8ffe35aca725a3094968306f06ff3ab8023b3d2bada34d",
  "submittedProcedure": "For a melee attack normally using STR, you may use DEX instead for the attack roll only. NEW this includes actual melee weapon, natural and unarmed attacks, but does not replace a spell's designated casting ability or a special attack expressly locked to another stat. Damage still uses its original ability unless the weapon's actual Finesse property or another feature independently changes damage too. ChoosingDEX here does not grant the Finesse property, change weapon weight/hands/reach, make a Heavy weapon light, waive STR/size requirements, or qualify for a STR-attack-only Power Attack. Actual PB requires actual proficiency as before. Source attack-modifier-dependent save DCs, such as Disarming Blow, use the actual DEX attack modifier when this swap applied; STR-fixed feats retain STR.",
  "submittedNewChoices": "STR melee attack-only substitution, natural/unarmed inclusion and no Finesse-property or casting-stat grant.",
  "submittedWorkedCases": [
    "A longsword attack may useDEX+4 to hit while damage still addsSTR+1.",
    "A dagger already possessing Finesse can independently useDEX for both; the feat is not the reason that dagger's damage changes."
  ],
  "decision": "Retain the full CF-37 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. STR melee attack-only substitution, natural/unarmed inclusion and no Finesse-property or casting-stat grant.",
  "completeAuthoringProcedure": "For a melee attack normally using STR, you may use DEX instead for the attack roll only. NEW this includes actual melee weapon, natural and unarmed attacks, but does not replace a spell's designated casting ability or a special attack expressly locked to another stat. Damage still uses its original ability unless the weapon's actual Finesse property or another feature independently changes damage too. ChoosingDEX here does not grant the Finesse property, change weapon weight/hands/reach, make a Heavy weapon light, waive STR/size requirements, or qualify for a STR-attack-only Power Attack. Actual PB requires actual proficiency as before. Source attack-modifier-dependent save DCs, such as Disarming Blow, use the actual DEX attack modifier when this swap applied; STR-fixed feats retain STR.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A longsword attack may useDEX+4 to hit while damage still addsSTR+1.",
    "A dagger already possessing Finesse can independently useDEX for both; the feat is not the reason that dagger's damage changes."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

For a melee attack normally using STR, you may use DEX instead for the attack roll only. NEW this includes actual melee weapon, natural and unarmed attacks, but does not replace a spell's designated casting ability or a special attack expressly locked to another stat. Damage still uses its original ability unless the weapon's actual Finesse property or another feature independently changes damage too. ChoosingDEX here does not grant the Finesse property, change weapon weight/hands/reach, make a Heavy weapon light, waive STR/size requirements, or qualify for a STR-attack-only Power Attack. Actual PB requires actual proficiency as before. Source attack-modifier-dependent save DCs, such as Disarming Blow, use the actual DEX attack modifier when this swap applied; STR-fixed feats retain STR.

### Original-position authored review references

```json
[
  {
    "id": "CF-37-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/72"
  },
  {
    "id": "CF-37-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/73"
  }
]
```

## CF-38 — Weapon Mastery

### Complete original object

```json
{
  "id": "weapon_mastery",
  "name": "Weapon Mastery",
  "description": "Proficient, Level 6 supports the listed +1 crit range with a chosen weapon.",
  "prerequisite": "Proficient, Level 6",
  "effect": "+1 crit range with chosen weapon.",
  "type": "Combat",
  "legacyEffect": "+1 crit range with chosen weapon",
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
"Define chosen weapon type, actual proficiency, character-level prerequisite and whether repeatable. Specify+1 critical range semantics, floor/limit and arbitration with Exploit Weakness and other critical features; no imported external Weapon Mastery system."
```

### Preserved original source direction (historical)

```json
{
  "featId": "weapon_mastery",
  "name": "Weapon Mastery",
  "cohort": "combat",
  "questionId": "CF-38",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/37",
  "originalQuestion": "Define chosen weapon type, actual proficiency, character-level prerequisite and whether repeatable. Specify+1 critical range semantics, floor/limit and arbitration with Exploit Weakness and other critical features; no imported external Weapon Mastery system.",
  "originalSourceObject": {
    "id": "weapon_mastery",
    "name": "Weapon Mastery",
    "description": "Proficient, Level 6 supports the listed +1 crit range with a chosen weapon.",
    "prerequisite": "Proficient, Level 6",
    "effect": "+1 crit range with chosen weapon.",
    "type": "Combat",
    "legacyEffect": "+1 crit range with chosen weapon",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "a77feb76e43e377a5bfb5c307522e5df8d569ab2859e3a1976adca8850278741",
  "submittedProcedure": "At acquisition, choose one actual weapon profile/type in which you are proficient; permanent choice, nonrepeatable. At total character level6+, attacks with that type have critical range19–20 instead of the ordinary20. NEW the printed+1 range is one downward threshold step from the ordinary20, not an additive modifier on another expanded range. Compare all applicable actual critical ranges and use the broadest, consistent with reviewed Core. Natural19 must still meetAC; natural20 retains its automatic-hit rule. Melee or thrown use of the chosen weapon type qualifies, but improvised use without that profile does not. A specific natural weapon may be chosen only if it is a genuine proficient weapon profile, not all natural/unarmed attacks by umbrella label. No external weapon-mastery maneuver system is imported.",
  "submittedNewChoices": "Permanent weapon-type selection,19–20 standalone range and no additive critical stacking.",
  "submittedWorkedCases": [
    "Chosen longsword natural19 totaling21 againstAC20 is critical; totaling18 misses.",
    "Weapon Mastery plus Exploit Weakness still yields19–20. An independently granted18–20 range stays18–20, not17–20."
  ],
  "decision": "Retain the full CF-38 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Permanent weapon-type selection,19–20 standalone range and no additive critical stacking.",
  "completeAuthoringProcedure": "At acquisition, choose one actual weapon profile/type in which you are proficient; permanent choice, nonrepeatable. At total character level6+, attacks with that type have critical range19–20 instead of the ordinary20. NEW the printed+1 range is one downward threshold step from the ordinary20, not an additive modifier on another expanded range. Compare all applicable actual critical ranges and use the broadest, consistent with reviewed Core. Natural19 must still meetAC; natural20 retains its automatic-hit rule. Melee or thrown use of the chosen weapon type qualifies, but improvised use without that profile does not. A specific natural weapon may be chosen only if it is a genuine proficient weapon profile, not all natural/unarmed attacks by umbrella label. No external weapon-mastery maneuver system is imported.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Chosen longsword natural19 totaling21 againstAC20 is critical; totaling18 misses.",
    "Weapon Mastery plus Exploit Weakness still yields19–20. An independently granted18–20 range stays18–20, not17–20."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

At acquisition, choose one actual weapon profile/type in which you are proficient; permanent choice, nonrepeatable. At total character level6+, attacks with that type have critical range19–20 instead of the ordinary20. NEW the printed+1 range is one downward threshold step from the ordinary20, not an additive modifier on another expanded range. Compare all applicable actual critical ranges and use the broadest, consistent with reviewed Core. Natural19 must still meetAC; natural20 retains its automatic-hit rule. Melee or thrown use of the chosen weapon type qualifies, but improvised use without that profile does not. A specific natural weapon may be chosen only if it is a genuine proficient weapon profile, not all natural/unarmed attacks by umbrella label. No external weapon-mastery maneuver system is imported.

### Original-position authored review references

```json
[
  {
    "id": "CF-38-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/74"
  },
  {
    "id": "CF-38-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/75"
  }
]
```

## CF-39 — Whip Control

### Complete original object

```json
{
  "id": "whip_control",
  "name": "Whip Control",
  "description": "Dexterity 15+ and Whip support the listed disarm or trip with a whip.",
  "prerequisite": "Dexterity 15+, Whip",
  "effect": "Disarm or trip with whip.",
  "type": "Combat",
  "legacyEffect": "Disarm or trip with whip",
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
"Bind actual Whip proficiency/use, one attack replacement or on-hit trigger, disarm versus trip choice, checks/saves/DC, reach, target size, damage/payment, frequency and legal dropped-object/push placement."
```

### Preserved original source direction (historical)

```json
{
  "featId": "whip_control",
  "name": "Whip Control",
  "cohort": "combat",
  "questionId": "CF-39",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/38",
  "originalQuestion": "Bind actual Whip proficiency/use, one attack replacement or on-hit trigger, disarm versus trip choice, checks/saves/DC, reach, target size, damage/payment, frequency and legal dropped-object/push placement.",
  "originalSourceObject": {
    "id": "whip_control",
    "name": "Whip Control",
    "description": "Dexterity 15+ and Whip support the listed disarm or trip with a whip.",
    "prerequisite": "Dexterity 15+, Whip",
    "effect": "Disarm or trip with whip.",
    "type": "Combat",
    "legacyEffect": "Disarm or trip with whip",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "8216d8491c6c3e22cc045c8595f17b6e9992a6ae6a414d85114dbe92c95de4e7",
  "submittedProcedure": "With actual Whip proficiency, wielding a usable whip, replace one attack of your Attack Action with one control attempt against a creature within the whip's actual melee reach. Choose disarm or trip before the roll. NEW make one weapon check d20+the whip's actual attack ability modifier+PB against the target's chosen STR Athletics orDEX Acrobatics total; opposed ties preserve state. This deals no damage, cannot crit, and is not a hit for on-hit riders. Trip requires target no more than one size larger and on success applies Prone subject to immunity/support. Disarm requires one actual reachable held object; on success choose a legal adjacent unoccupied drop space, otherwise the target's space, respecting real non-droppable bonds. No rest cap, but each attempt spends one actual Attack Action attack. Whip reach does not create a grapple or long-term restraint. Lunge modifies one melee weapon attack, not this check, so does not extend the control reach.",
  "submittedNewChoices": "Attack replacement, opposed weapon check, no damage, trip size cap and exact drop geometry.",
  "submittedWorkedCases": [
    "A whip at10ft reaches a Large enemy. Weapon check18 beats Acrobatics15 and trips it without damage.",
    "An opposed tie leaves a held sword in place. The attack replacement was spent and no hit-trigger damage occurs."
  ],
  "decision": "Retain the full CF-39 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Attack replacement, opposed weapon check, no damage, trip size cap and exact drop geometry.",
  "completeAuthoringProcedure": "With actual Whip proficiency, wielding a usable whip, replace one attack of your Attack Action with one control attempt against a creature within the whip's actual melee reach. Choose disarm or trip before the roll. NEW make one weapon check d20+the whip's actual attack ability modifier+PB against the target's chosen STR Athletics orDEX Acrobatics total; opposed ties preserve state. This deals no damage, cannot crit, and is not a hit for on-hit riders. Trip requires target no more than one size larger and on success applies Prone subject to immunity/support. Disarm requires one actual reachable held object; on success choose a legal adjacent unoccupied drop space, otherwise the target's space, respecting real non-droppable bonds. No rest cap, but each attempt spends one actual Attack Action attack. Whip reach does not create a grapple or long-term restraint. Lunge modifies one melee weapon attack, not this check, so does not extend the control reach.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A whip at10ft reaches a Large enemy. Weapon check18 beats Acrobatics15 and trips it without damage.",
    "An opposed tie leaves a held sword in place. The attack replacement was spent and no hit-trigger damage occurs."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

With actual Whip proficiency, wielding a usable whip, replace one attack of your Attack Action with one control attempt against a creature within the whip's actual melee reach. Choose disarm or trip before the roll. NEW make one weapon check d20+the whip's actual attack ability modifier+PB against the target's chosen STR Athletics orDEX Acrobatics total; opposed ties preserve state. This deals no damage, cannot crit, and is not a hit for on-hit riders. Trip requires target no more than one size larger and on success applies Prone subject to immunity/support. Disarm requires one actual reachable held object; on success choose a legal adjacent unoccupied drop space, otherwise the target's space, respecting real non-droppable bonds. No rest cap, but each attempt spends one actual Attack Action attack. Whip reach does not create a grapple or long-term restraint. Lunge modifies one melee weapon attack, not this check, so does not extend the control reach.

### Original-position authored review references

```json
[
  {
    "id": "CF-39-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/76"
  },
  {
    "id": "CF-39-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/77"
  }
]
```

## CF-40 — Whirlwind Striker

### Complete original object

```json
{
  "id": "whirlwind_striker",
  "name": "Whirlwind Striker",
  "description": "Level 10 supports the listed +5% evasion and +10% cleave when surrounded.",
  "prerequisite": "Level 10",
  "effect": "+5% evasion and +10% cleave when surrounded.",
  "type": "Combat",
  "legacyEffect": "+5% evasion and +10% cleave when surrounded",
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
"Complete surrounded geometry, meaning of evasion and cleave, exact percentage bases/rounding, triggers, targets, costs, frequency and ending. Preserve the+5%/+10% originals and label any conversion as NEW."
```

### Preserved original source direction (historical)

```json
{
  "featId": "whirlwind_striker",
  "name": "Whirlwind Striker",
  "cohort": "combat",
  "questionId": "CF-40",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/39",
  "originalQuestion": "Complete surrounded geometry, meaning of evasion and cleave, exact percentage bases/rounding, triggers, targets, costs, frequency and ending. Preserve the+5%/+10% originals and label any conversion as NEW.",
  "originalSourceObject": {
    "id": "whirlwind_striker",
    "name": "Whirlwind Striker",
    "description": "Level 10 supports the listed +5% evasion and +10% cleave when surrounded.",
    "prerequisite": "Level 10",
    "effect": "+5% evasion and +10% cleave when surrounded.",
    "type": "Combat",
    "legacyEffect": "+5% evasion and +10% cleave when surrounded",
    "status": "provisional-complete",
    "balanceReview": true,
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "7684589550be789d1d22e9dc7acf01689ca72cf61420e3de540f6513f37a9d0b",
  "submittedProcedure": "NEW complete interpretation: surrounded means at least two different conscious hostile creatures within5ft of you, on opposite sides under Tactical Flanker's center-segment geometry, each currently able to attack you in melee. While that predicate holds, gain+1AC as an explicit conversion of the source's undefined+5% evasion; this is not literal5%damage reduction or a separate avoidance roll. Once on your own turn, after your melee weapon attack hits a creature while surrounded, you may deal a cleave packet to one different perceived hostile creature within the actual reach of that same weapon. Amount is floor10% of that hit's eligible native weapon damage before percentages/defenses; allocate native types as shared arithmetic. No second attack roll, no new critical and no on-hit riders/resources from this derived packet; ordinary recipient defenses apply. The primary attack can be fully mitigated and still supply its legal pre-defense native amount, but a missed attack cannot. Cleave needs real reach/line, deals0 if the rounded amount is0, and cannot itself cleave or trigger a drop-generated attack/heal. Losing surrounded geometry ends AC immediately.",
  "submittedNewChoices": "Explicit+5% evasion→+1AC conversion, opposite-hostile geometry and finite10% derived cleave rather than imported class ability.",
  "submittedWorkedCases": [
    "Two opposite adjacent melee foes qualify; a native19-damage hit yields a1-damage cleave packet to one other legal foe.",
    "One surrounding enemy becomes Incapacitated. The+1AC ends immediately; a later hit cannot use this feat's cleave until the predicate returns."
  ],
  "decision": "Retain the full CF-40 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Explicit+5% evasion→+1AC conversion, opposite-hostile geometry and finite10% derived cleave rather than imported class ability.",
  "completeAuthoringProcedure": "NEW complete interpretation: surrounded means at least two different conscious hostile creatures within5ft of you, on opposite sides under Tactical Flanker's center-segment geometry, each currently able to attack you in melee. While that predicate holds, gain+1AC as an explicit conversion of the source's undefined+5% evasion; this is not literal5%damage reduction or a separate avoidance roll. Once on your own turn, after your melee weapon attack hits a creature while surrounded, you may deal a cleave packet to one different perceived hostile creature within the actual reach of that same weapon. Amount is floor10% of that hit's eligible native weapon damage before percentages/defenses; allocate native types as shared arithmetic. No second attack roll, no new critical and no on-hit riders/resources from this derived packet; ordinary recipient defenses apply. The primary attack can be fully mitigated and still supply its legal pre-defense native amount, but a missed attack cannot. Cleave needs real reach/line, deals0 if the rounded amount is0, and cannot itself cleave or trigger a drop-generated attack/heal. Losing surrounded geometry ends AC immediately.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Two opposite adjacent melee foes qualify; a native19-damage hit yields a1-damage cleave packet to one other legal foe.",
    "One surrounding enemy becomes Incapacitated. The+1AC ends immediately; a later hit cannot use this feat's cleave until the predicate returns."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

NEW complete interpretation: surrounded means at least two different conscious hostile creatures within5ft of you, on opposite sides under Tactical Flanker's center-segment geometry, each currently able to attack you in melee. While that predicate holds, gain+1AC as an explicit conversion of the source's undefined+5% evasion; this is not literal5%damage reduction or a separate avoidance roll. Once on your own turn, after your melee weapon attack hits a creature while surrounded, you may deal a cleave packet to one different perceived hostile creature within the actual reach of that same weapon. Amount is floor10% of that hit's eligible native weapon damage before percentages/defenses; allocate native types as shared arithmetic. No second attack roll, no new critical and no on-hit riders/resources from this derived packet; ordinary recipient defenses apply. The primary attack can be fully mitigated and still supply its legal pre-defense native amount, but a missed attack cannot. Cleave needs real reach/line, deals0 if the rounded amount is0, and cannot itself cleave or trigger a drop-generated attack/heal. Losing surrounded geometry ends AC immediately.

### Original-position authored review references

```json
[
  {
    "id": "CF-40-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/78"
  },
  {
    "id": "CF-40-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/79"
  }
]
```

## CF-41 — Eldritch Combat

### Complete original object

```json
{
  "id": "eldritch_combat",
  "name": "Eldritch Combat",
  "description": "Your strikes carry whispers from beyond the veil—steel and sigil in a single motion. Prestige lineage: Hexblade. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, proficiency with martial weapons",
  "effect": "When you take the Attack action, you can cast a cantrip or 1st-level spell with a range of touch or self as part of the same action without provoking opportunity attacks. The spell must target the same creature you hit or yourself. Once per short rest, when you hit with a melee weapon attack, you may cast a touch-range spell as a free action on that target even if you did not take the full Attack action.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you take the Attack action, you can cast a cantrip or 1st-level spell with a range of touch or self as part of the same action without provoking opportunity attacks. The spell must target the same creature you hit or yourself. Once per short rest, when you hit with a melee weapon attack, you may cast a touch-range spell as a free action on that target even if you did not take the full Attack action.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Resolve legacy1st-level against this game's rank system; actual repertoire/casting-class access, RP/components/concentration/Dissonance and independent casting-time eligibility. Define ordering with Attack action, hit prerequisite, touch/self target clauses, reaction-triggered free casts, cadence and separate short-rest use without granting free costs."
```

### Preserved original source direction (historical)

```json
{
  "featId": "eldritch_combat",
  "name": "Eldritch Combat",
  "cohort": "combat",
  "questionId": "CF-41",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/40",
  "originalQuestion": "Resolve legacy1st-level against this game's rank system; actual repertoire/casting-class access, RP/components/concentration/Dissonance and independent casting-time eligibility. Define ordering with Attack action, hit prerequisite, touch/self target clauses, reaction-triggered free casts, cadence and separate short-rest use without granting free costs.",
  "originalSourceObject": {
    "id": "eldritch_combat",
    "name": "Eldritch Combat",
    "description": "Your strikes carry whispers from beyond the veil—steel and sigil in a single motion. Prestige lineage: Hexblade. completed from the existing development record.)",
    "prerequisite": "Spellcasting ability, proficiency with martial weapons",
    "effect": "When you take the Attack action, you can cast a cantrip or 1st-level spell with a range of touch or self as part of the same action without provoking opportunity attacks. The spell must target the same creature you hit or yourself. Once per short rest, when you hit with a melee weapon attack, you may cast a touch-range spell as a free action on that target even if you did not take the full Attack action.",
    "type": "Combat",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you take the Attack action, you can cast a cantrip or 1st-level spell with a range of touch or self as part of the same action without provoking opportunity attacks. The spell must target the same creature you hit or yourself. Once per short rest, when you hit with a melee weapon attack, you may cast a touch-range spell as a free action on that target even if you did not take the full Attack action.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "18e09cfe7acef373937d281428b3330acb9d67a145f3f8d769b24c552dc9b9c0",
  "submittedProcedure": "Acquire only with a real spellcasting route and actual martial-weapon proficiency. NEW read1st-level as rank1 for this feat only. Once on your own regular-turn interval, when you take Attack Action and complete its attack sequence, append one actually available Action-time rank0 or rank1 spell with literal Touch or Self range as part of that same Action. You must have hit a creature with at least one of those attacks if choosing an external Touch target; that exact hit creature must also be a legal sole recipient of the spell. A Self spell must actually target only you, not a cone/area originating from Self that independently targets others. Spell must be acquired/prepared on a legitimate route with real level/rank access, RP or finite charge, components/hands/focus, target consent where required, concentration, Dissonance/Refrain, casting prohibitions and interruption. No normal casting cost is waived. An attack hit does not substitute for a spell's own required attack/save. Longer spells, BA spells and Reaction spells are not compressed by this grant. Separately, once per SR after your melee weapon attack hits, you may append one legitimately available Action-time Touch spell of any legally accessible rank to that same sole target without an extra Action; this can occur off-turn. NEW both modes share at most one embedded cast per actual regular creature turn and cannot be combined on the same hit/Action. Spend SR use at casting commitment, even if countered. These appended castings do not provoke opportunity attacks solely for casting/performing the appended attack-spell operation, but movement has ordinary triggers. Neither casting may create a further Eldritch append from attacks in its own causal root. Actual source-specific secondary/resource restrictions remain; no prestige class is acquired.",
  "submittedNewChoices": "Rank translation, Action-time only, one-self/one-touch recipient, timing, shared one embedded cast per actual turn and paid independent casting.",
  "submittedWorkedCases": [
    "After a successful sword Attack, a legitimately prepared Touch rank1 spell can target that hit creature, paying actualRP/components; the sword hit does not make its spell attack automatically hit.",
    "An opportunity sword hit may use the separate SR Touch cast if legal and unspent. A Touch spell with a1minute casting time remains ineligible."
  ],
  "decision": "Retain the full CF-41 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Rank translation, Action-time only, one-self/one-touch recipient, timing, shared one embedded cast per actual turn and paid independent casting.",
  "completeAuthoringProcedure": "Acquire only with a real spellcasting route and actual martial-weapon proficiency. NEW read1st-level as rank1 for this feat only. Once on your own regular-turn interval, when you take Attack Action and complete its attack sequence, append one actually available Action-time rank0 or rank1 spell with literal Touch or Self range as part of that same Action. You must have hit a creature with at least one of those attacks if choosing an external Touch target; that exact hit creature must also be a legal sole recipient of the spell. A Self spell must actually target only you, not a cone/area originating from Self that independently targets others. Spell must be acquired/prepared on a legitimate route with real level/rank access, RP or finite charge, components/hands/focus, target consent where required, concentration, Dissonance/Refrain, casting prohibitions and interruption. No normal casting cost is waived. An attack hit does not substitute for a spell's own required attack/save. Longer spells, BA spells and Reaction spells are not compressed by this grant. Separately, once per SR after your melee weapon attack hits, you may append one legitimately available Action-time Touch spell of any legally accessible rank to that same sole target without an extra Action; this can occur off-turn. NEW both modes share at most one embedded cast per actual regular creature turn and cannot be combined on the same hit/Action. Spend SR use at casting commitment, even if countered. These appended castings do not provoke opportunity attacks solely for casting/performing the appended attack-spell operation, but movement has ordinary triggers. Neither casting may create a further Eldritch append from attacks in its own causal root. Actual source-specific secondary/resource restrictions remain; no prestige class is acquired.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "After a successful sword Attack, a legitimately prepared Touch rank1 spell can target that hit creature, paying actualRP/components; the sword hit does not make its spell attack automatically hit.",
    "An opportunity sword hit may use the separate SR Touch cast if legal and unspent. A Touch spell with a1minute casting time remains ineligible."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Acquire only with a real spellcasting route and actual martial-weapon proficiency. NEW read1st-level as rank1 for this feat only. Once on your own regular-turn interval, when you take Attack Action and complete its attack sequence, append one actually available Action-time rank0 or rank1 spell with literal Touch or Self range as part of that same Action. You must have hit a creature with at least one of those attacks if choosing an external Touch target; that exact hit creature must also be a legal sole recipient of the spell. A Self spell must actually target only you, not a cone/area originating from Self that independently targets others. Spell must be acquired/prepared on a legitimate route with real level/rank access, RP or finite charge, components/hands/focus, target consent where required, concentration, Dissonance/Refrain, casting prohibitions and interruption. No normal casting cost is waived. An attack hit does not substitute for a spell's own required attack/save. Longer spells, BA spells and Reaction spells are not compressed by this grant. Separately, once per SR after your melee weapon attack hits, you may append one legitimately available Action-time Touch spell of any legally accessible rank to that same sole target without an extra Action; this can occur off-turn. NEW both modes share at most one embedded cast per actual regular creature turn and cannot be combined on the same hit/Action. Spend SR use at casting commitment, even if countered. These appended castings do not provoke opportunity attacks solely for casting/performing the appended attack-spell operation, but movement has ordinary triggers. Neither casting may create a further Eldritch append from attacks in its own causal root. Actual source-specific secondary/resource restrictions remain; no prestige class is acquired.

### Original-position authored review references

```json
[
  {
    "id": "CF-41-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/80"
  },
  {
    "id": "CF-41-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/81"
  }
]
```

## CF-42 — Favored Enemy (Dragon)

### Complete original object

```json
{
  "id": "favored_enemy_dragon",
  "name": "Favored Enemy (Dragon)",
  "description": "You have studied scaled tyrants—their breath, their pride, the tell before the roar. Prestige lineage: Wyrmslayer. completed from the existing development record.)",
  "prerequisite": "Proficiency in Survival, level 5+",
  "effect": "You deal +2 damage to dragons and dragonkin. You have advantage on Survival and Lore checks to identify dragon ancestry, breath type, and lair habits. When you succeed on such a check against a dragon you can see, you and allies within 30 feet gain +1 to saving throws against that dragon's breath weapon until the end of the encounter. You cannot be frightened by a dragon's presence for more than 1 round, and once per short rest you may ignore difficult terrain caused by a dragon's lair hazards (molten glass, acidic pools, or shattered stone) while pursuing that wyrm.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You deal +2 damage to dragons and dragonkin. You have advantage on Survival and Lore checks to identify dragon ancestry, breath type, and lair habits. When you succeed on such a check against a dragon you can see, you and allies within 30 feet gain +1 to saving throws against that dragon's breath weapon until the end of the encounter. You cannot be frightened by a dragon's presence for more than 1 round, and once per short rest you may ignore difficult terrain caused by a dragon's lair hazards (molten glass, acidic pools, or shattered stone) while pursuing that wyrm.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind current bestiary dragon/dragonkin tags without cosmology or ancestry retcons; damage event scope, Survival/Lore skill mapping and genuine information checks. Define ally+1 breath-save radius/timing/duration, Frightened one-round limit, difficult-terrain use/duration and continuing lair hazard damage."
```

### Preserved original source direction (historical)

```json
{
  "featId": "favored_enemy_dragon",
  "name": "Favored Enemy (Dragon)",
  "cohort": "combat",
  "questionId": "CF-42",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/41",
  "originalQuestion": "Bind current bestiary dragon/dragonkin tags without cosmology or ancestry retcons; damage event scope, Survival/Lore skill mapping and genuine information checks. Define ally+1 breath-save radius/timing/duration, Frightened one-round limit, difficult-terrain use/duration and continuing lair hazard damage.",
  "originalSourceObject": {
    "id": "favored_enemy_dragon",
    "name": "Favored Enemy (Dragon)",
    "description": "You have studied scaled tyrants—their breath, their pride, the tell before the roar. Prestige lineage: Wyrmslayer. completed from the existing development record.)",
    "prerequisite": "Proficiency in Survival, level 5+",
    "effect": "You deal +2 damage to dragons and dragonkin. You have advantage on Survival and Lore checks to identify dragon ancestry, breath type, and lair habits. When you succeed on such a check against a dragon you can see, you and allies within 30 feet gain +1 to saving throws against that dragon's breath weapon until the end of the encounter. You cannot be frightened by a dragon's presence for more than 1 round, and once per short rest you may ignore difficult terrain caused by a dragon's lair hazards (molten glass, acidic pools, or shattered stone) while pursuing that wyrm.",
    "type": "Combat",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You deal +2 damage to dragons and dragonkin. You have advantage on Survival and Lore checks to identify dragon ancestry, breath type, and lair habits. When you succeed on such a check against a dragon you can see, you and allies within 30 feet gain +1 to saving throws against that dragon's breath weapon until the end of the encounter. You cannot be frightened by a dragon's presence for more than 1 round, and once per short rest you may ignore difficult terrain caused by a dragon's lair hazards (molten glass, acidic pools, or shattered stone) while pursuing that wyrm.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "f13fac72ee2b54032e2232b7c48791ff64334867014bf0469d60bd0394207732",
  "submittedProcedure": "Use actual supplied creature-type/tag facts: Dragon and expressly recorded dragonkin qualify for the+2damage and knowledge clauses; do not infer these tags from a humanoid ancestry name or settle origins. Add+2flat once per own direct damage event against a qualifying creature, of one native type, before defenses; no copied, periodic, reflected or controller-owned companion event. Advantage applies to genuine Survival tracking/ecology checks and NEW INT Nature checks representing the source's undefined Lore for physical draconic ancestry traits, breath type and lair habits; Arcana/History can use their actual separate task if relevant but receive no automatic substitute proficiency. NEW in initiative spend Action to observe a visible dragon within60ft, outside initiative1minute; DC=10+ceil(actualCR), or15 when noCR exists, adjusted only for explicitly established concealment of facts. Success gives one useful actually available requested fact, not sealed origins. On such success against a visible actual Dragon, brief other willing allies within30ft who can perceive/understand you; you and those fixed recipients gain+1 to saves against that individual dragon's breath through encounter end. Same feat family does not stack and later entrants require a new successful actual read/brief. Fear caused specifically by a dragon's presence lasts at most through your next future original regular start, then that source record ends; other fear remains. Once per SR, no Action during your movement while actually pursuing that dragon, ignore difficult-terrain movement surcharge caused by its real lair hazards through the current turn's end (outside initiative6seconds). Hazard damage/saves and impassability remain. No real bestiary record is retyped by this proposal.",
  "submittedNewChoices": "Literal tags, own-event+2, Nature/Lore bridge, finite observationDC/time/briefing, one-round presence fear and one-turn terrain use.",
  "submittedWorkedCases": [
    "A CR7 Dragon observationDC17 succeeds; three briefed allies within30 gain+1 against that dragon's breath for the encounter.",
    "Ignoring acidic-pool difficult terrain while pursuing the dragon removes movement surcharge only. Acid damage and other actual pool checks still resolve."
  ],
  "decision": "Retain the full CF-42 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Literal tags, own-event+2, Nature/Lore bridge, finite observationDC/time/briefing, one-round presence fear and one-turn terrain use.",
  "completeAuthoringProcedure": "Use actual supplied creature-type/tag facts: Dragon and expressly recorded dragonkin qualify for the+2damage and knowledge clauses; do not infer these tags from a humanoid ancestry name or settle origins. Add+2flat once per own direct damage event against a qualifying creature, of one native type, before defenses; no copied, periodic, reflected or controller-owned companion event. Advantage applies to genuine Survival tracking/ecology checks and NEW INT Nature checks representing the source's undefined Lore for physical draconic ancestry traits, breath type and lair habits; Arcana/History can use their actual separate task if relevant but receive no automatic substitute proficiency. NEW in initiative spend Action to observe a visible dragon within60ft, outside initiative1minute; DC=10+ceil(actualCR), or15 when noCR exists, adjusted only for explicitly established concealment of facts. Success gives one useful actually available requested fact, not sealed origins. On such success against a visible actual Dragon, brief other willing allies within30ft who can perceive/understand you; you and those fixed recipients gain+1 to saves against that individual dragon's breath through encounter end. Same feat family does not stack and later entrants require a new successful actual read/brief. Fear caused specifically by a dragon's presence lasts at most through your next future original regular start, then that source record ends; other fear remains. Once per SR, no Action during your movement while actually pursuing that dragon, ignore difficult-terrain movement surcharge caused by its real lair hazards through the current turn's end (outside initiative6seconds). Hazard damage/saves and impassability remain. No real bestiary record is retyped by this proposal.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A CR7 Dragon observationDC17 succeeds; three briefed allies within30 gain+1 against that dragon's breath for the encounter.",
    "Ignoring acidic-pool difficult terrain while pursuing the dragon removes movement surcharge only. Acid damage and other actual pool checks still resolve."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Use actual supplied creature-type/tag facts: Dragon and expressly recorded dragonkin qualify for the+2damage and knowledge clauses; do not infer these tags from a humanoid ancestry name or settle origins. Add+2flat once per own direct damage event against a qualifying creature, of one native type, before defenses; no copied, periodic, reflected or controller-owned companion event. Advantage applies to genuine Survival tracking/ecology checks and NEW INT Nature checks representing the source's undefined Lore for physical draconic ancestry traits, breath type and lair habits; Arcana/History can use their actual separate task if relevant but receive no automatic substitute proficiency. NEW in initiative spend Action to observe a visible dragon within60ft, outside initiative1minute; DC=10+ceil(actualCR), or15 when noCR exists, adjusted only for explicitly established concealment of facts. Success gives one useful actually available requested fact, not sealed origins. On such success against a visible actual Dragon, brief other willing allies within30ft who can perceive/understand you; you and those fixed recipients gain+1 to saves against that individual dragon's breath through encounter end. Same feat family does not stack and later entrants require a new successful actual read/brief. Fear caused specifically by a dragon's presence lasts at most through your next future original regular start, then that source record ends; other fear remains. Once per SR, no Action during your movement while actually pursuing that dragon, ignore difficult-terrain movement surcharge caused by its real lair hazards through the current turn's end (outside initiative6seconds). Hazard damage/saves and impassability remain. No real bestiary record is retyped by this proposal.

### Original-position authored review references

```json
[
  {
    "id": "CF-42-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/82"
  },
  {
    "id": "CF-42-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/83"
  }
]
```

## CF-43 — Frenzied Rage

### Complete original object

```json
{
  "id": "frenzied_rage",
  "name": "Frenzied Rage",
  "description": "Rage becomes avalanche—each kill feeds the next swing until the world is only red and thunder. Prestige lineage: Berserker. completed from the existing development record.)",
  "prerequisite": "Constitution 15+, Berserker feat or class rage ability",
  "effect": "While raging, you deal +3 damage with melee weapon attacks (instead of +2). When you reduce a creature to 0 hit points with a melee attack, you can make one additional melee attack or extend your rage duration by 1 round. Once per rage, you can charge through enemies, dazing those you pass.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "While raging, you deal +3 damage with melee weapon attacks (instead of +2). When you reduce a creature to 0 hit points with a melee attack, you can make one additional melee attack or extend your rage duration by 1 round. Once per rage, you can charge through enemies, dazing those you pass.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Preserve all three clauses: replacement+3 instead of+2, drop-trigger extra attack OR one-round extension, and once-per-rage charge with Dazed. Bind valid rage sources and acquisition prerequisites, action/cadence/caps, movement/save/DC/targets/duration, avoiding unlimited kill/extension loops or name-only class eligibility."
```

### Preserved original source direction (historical)

```json
{
  "featId": "frenzied_rage",
  "name": "Frenzied Rage",
  "cohort": "combat",
  "questionId": "CF-43",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/42",
  "originalQuestion": "Preserve all three clauses: replacement+3 instead of+2, drop-trigger extra attack OR one-round extension, and once-per-rage charge with Dazed. Bind valid rage sources and acquisition prerequisites, action/cadence/caps, movement/save/DC/targets/duration, avoiding unlimited kill/extension loops or name-only class eligibility.",
  "originalSourceObject": {
    "id": "frenzied_rage",
    "name": "Frenzied Rage",
    "description": "Rage becomes avalanche—each kill feeds the next swing until the world is only red and thunder. Prestige lineage: Berserker. completed from the existing development record.)",
    "prerequisite": "Constitution 15+, Berserker feat or class rage ability",
    "effect": "While raging, you deal +3 damage with melee weapon attacks (instead of +2). When you reduce a creature to 0 hit points with a melee attack, you can make one additional melee attack or extend your rage duration by 1 round. Once per rage, you can charge through enemies, dazing those you pass.",
    "type": "Combat",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "While raging, you deal +3 damage with melee weapon attacks (instead of +2). When you reduce a creature to 0 hit points with a melee attack, you can make one additional melee attack or extend your rage duration by 1 round. Once per rage, you can charge through enemies, dazing those you pass.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "cb7f70d0ba1368abfd67fb23101f357b5ad9bc3e7b31a8a089e69508660466b2",
  "submittedProcedure": "Acquire with CON15 and the actual Berserker feat or an actual class feature expressly granting a rage state. No name-only qualification from Berserker Brew, Mooncursed, a prestige lineage or a damage buff. While in an actual acquired Berserker rage, replace its+2 melee bonus with+3 on melee weapon attacks; for any other qualifying rage lacking that+2, NEW grant+3flat melee-weapon damage as this feat's own family, without replacing separately rolled dice. Do not add+3 on top of the same Berserker+2. Berserker Rage CF-03 is an operating rage once this feat was legally acquired by its printed prerequisite, but not an acquisition substitute. Once per turn after your melee attack reduces an independent meaningful hostile from positiveHP to0, choose EITHER one immediate additional melee attack (NEW only on your own turn) OR extend that same currently active rage's time endpoint by one original6second round. Extra attack requires real reach/target/weapon/capability and creates no Action/BA; shared causal limits prevent drop-trigger attack chains. NEW at most three time extensions per single rage use; non-time endings such as incapacitation or missing upkeep remain. Once per rage, on your turn spend BA to charge along a declared straight legal route with a separate current walking-Speed movement-cost budget, through at most three hostile creatures no more than one size larger. Recheck a complete legal unoccupied endpoint before starting, pay occupied-space difficult cost and normal hazards/opportunity attacks. Each crossed creature once makesCON save DC8+PB+STR; failure applies Dazed until its next future original regular end. No damage/Prone/push is implied. If the route is interrupted, stop in the last legal space; already crossed targets remain affected and use stays spent. It cannot force passage when there is no legal complete crossing route.",
  "submittedNewChoices": "Explicit rage-source distinction, replacement damage, hostile reward gate, once-turn extra attack/extension choice, three-extension cap and full BA charge procedure.",
  "submittedWorkedCases": [
    "Berserker's+2 becomes+3, not+5. A drop can fund one extra own-turn attack; a drop from that extra attack cannot spawn another.",
    "After three accepted extensions (+18seconds), a fourth drop cannot extend that same rage further. Incapacitation still ends a rage that has that endpoint."
  ],
  "decision": "Retain the full CF-43 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Explicit rage-source distinction, replacement damage, hostile reward gate, once-turn extra attack/extension choice, three-extension cap and full BA charge procedure.",
  "completeAuthoringProcedure": "Acquire with CON15 and the actual Berserker feat or an actual class feature expressly granting a rage state. No name-only qualification from Berserker Brew, Mooncursed, a prestige lineage or a damage buff. While in an actual acquired Berserker rage, replace its+2 melee bonus with+3 on melee weapon attacks; for any other qualifying rage lacking that+2, NEW grant+3flat melee-weapon damage as this feat's own family, without replacing separately rolled dice. Do not add+3 on top of the same Berserker+2. Berserker Rage CF-03 is an operating rage once this feat was legally acquired by its printed prerequisite, but not an acquisition substitute. Once per turn after your melee attack reduces an independent meaningful hostile from positiveHP to0, choose EITHER one immediate additional melee attack (NEW only on your own turn) OR extend that same currently active rage's time endpoint by one original6second round. Extra attack requires real reach/target/weapon/capability and creates no Action/BA; shared causal limits prevent drop-trigger attack chains. NEW at most three time extensions per single rage use; non-time endings such as incapacitation or missing upkeep remain. Once per rage, on your turn spend BA to charge along a declared straight legal route with a separate current walking-Speed movement-cost budget, through at most three hostile creatures no more than one size larger. Recheck a complete legal unoccupied endpoint before starting, pay occupied-space difficult cost and normal hazards/opportunity attacks. Each crossed creature once makesCON save DC8+PB+STR; failure applies Dazed until its next future original regular end. No damage/Prone/push is implied. If the route is interrupted, stop in the last legal space; already crossed targets remain affected and use stays spent. It cannot force passage when there is no legal complete crossing route.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "Berserker's+2 becomes+3, not+5. A drop can fund one extra own-turn attack; a drop from that extra attack cannot spawn another.",
    "After three accepted extensions (+18seconds), a fourth drop cannot extend that same rage further. Incapacitation still ends a rage that has that endpoint."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Acquire with CON15 and the actual Berserker feat or an actual class feature expressly granting a rage state. No name-only qualification from Berserker Brew, Mooncursed, a prestige lineage or a damage buff. While in an actual acquired Berserker rage, replace its+2 melee bonus with+3 on melee weapon attacks; for any other qualifying rage lacking that+2, NEW grant+3flat melee-weapon damage as this feat's own family, without replacing separately rolled dice. Do not add+3 on top of the same Berserker+2. Berserker Rage CF-03 is an operating rage once this feat was legally acquired by its printed prerequisite, but not an acquisition substitute. Once per turn after your melee attack reduces an independent meaningful hostile from positiveHP to0, choose EITHER one immediate additional melee attack (NEW only on your own turn) OR extend that same currently active rage's time endpoint by one original6second round. Extra attack requires real reach/target/weapon/capability and creates no Action/BA; shared causal limits prevent drop-trigger attack chains. NEW at most three time extensions per single rage use; non-time endings such as incapacitation or missing upkeep remain. Once per rage, on your turn spend BA to charge along a declared straight legal route with a separate current walking-Speed movement-cost budget, through at most three hostile creatures no more than one size larger. Recheck a complete legal unoccupied endpoint before starting, pay occupied-space difficult cost and normal hazards/opportunity attacks. Each crossed creature once makesCON save DC8+PB+STR; failure applies Dazed until its next future original regular end. No damage/Prone/push is implied. If the route is interrupted, stop in the last legal space; already crossed targets remain affected and use stays spent. It cannot force passage when there is no legal complete crossing route.

### Original-position authored review references

```json
[
  {
    "id": "CF-43-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/84"
  },
  {
    "id": "CF-43-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/85"
  }
]
```

## CF-44 — Giant Slayer

### Complete original object

```json
{
  "id": "giant_slayer",
  "name": "Giant Slayer",
  "description": "Colossi fall when the small learn where the giant bleeds. Prestige lineage: Giant Killer. completed from the existing development record.)",
  "prerequisite": "Precision Strike or level 8+",
  "effect": "You deal +20% damage against Large or larger creatures. Once per short rest, when you hit a Huge or larger creature with a melee attack, you can cripple its movement, reducing speed by half until the end of its next turn. When a colossal foe (Huge or larger) misses you with a melee attack, you may use your reaction to step into its reach and strike a tendon or joint: the attacker takes 1d6 damage and has disadvantage on its next attack against you before the end of its next turn.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You deal +20% damage against Large or larger creatures. Once per short rest, when you hit a Huge or larger creature with a melee attack, you can cripple its movement, reducing speed by half until the end of its next turn. When a colossal foe (Huge or larger) misses you with a melee attack, you may use your reaction to step into its reach and strike a tendon or joint: the attacker takes 1d6 damage and has disadvantage on its next attack against you before the end of its next turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind Size thresholds and the+20% damage base/order, successful melee-hit speed-halving timing/recovery and short-rest use. Complete miss-trigger Reaction movement budget/reach, direct1d6 versus an attack, type, geometry and disadvantage deadline. Preserve all three effects."
```

### Preserved original source direction (historical)

```json
{
  "featId": "giant_slayer",
  "name": "Giant Slayer",
  "cohort": "combat",
  "questionId": "CF-44",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/43",
  "originalQuestion": "Bind Size thresholds and the+20% damage base/order, successful melee-hit speed-halving timing/recovery and short-rest use. Complete miss-trigger Reaction movement budget/reach, direct1d6 versus an attack, type, geometry and disadvantage deadline. Preserve all three effects.",
  "originalSourceObject": {
    "id": "giant_slayer",
    "name": "Giant Slayer",
    "description": "Colossi fall when the small learn where the giant bleeds. Prestige lineage: Giant Killer. completed from the existing development record.)",
    "prerequisite": "Precision Strike or level 8+",
    "effect": "You deal +20% damage against Large or larger creatures. Once per short rest, when you hit a Huge or larger creature with a melee attack, you can cripple its movement, reducing speed by half until the end of its next turn. When a colossal foe (Huge or larger) misses you with a melee attack, you may use your reaction to step into its reach and strike a tendon or joint: the attacker takes 1d6 damage and has disadvantage on its next attack against you before the end of its next turn.",
    "type": "Combat",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You deal +20% damage against Large or larger creatures. Once per short rest, when you hit a Huge or larger creature with a melee attack, you can cripple its movement, reducing speed by half until the end of its next turn. When a colossal foe (Huge or larger) misses you with a melee attack, you may use your reaction to step into its reach and strike a tendon or joint: the attacker takes 1d6 damage and has disadvantage on its next attack against you before the end of its next turn.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "8ae2a531517aed02a32a16014735dc1a82781765e069e798c0d0f3db345d2905",
  "submittedProcedure": "Acquire with actual Precision Strike OR total level8. Against actual Large-or-larger creatures, add floor20% of each own direct damage event's eligible native amount before defenses, using shared noncompounding percent arithmetic. This broad damage clause includes own actual spell and weapon components but not periodic/copy/reflection/transfer or companion-owned attacks. Once per SR after a melee attack hits a Huge-or-larger creature, before damage declare the cripple use; after damage halve all its current Speed modes through its next future regular end, retaining spent movement cost. NEW no additional save is invented; same feat family halves once and actual immunities/specific movement protections apply. When a Huge-or-larger enemy misses you with a melee attack, you may spend Reaction for a separate5ft movement-cost step, then, only if that creature is within your own actual melee weapon/natural/unarmed reach and line, deal1d6 direct damage of that legal attack profile's native physical type (bludgeoning for unarmed) without an attack roll. You may step0 if already in reach; normal terrain/opportunity attacks/Speed restrictions apply. If the step cannot bring it into your reach, do not start this Reaction. The original source wording about stepping into its reach does not let you strike from beyond your own reach. It then has disadvantage on its next attack against you before its next future regular end, consumed hit or miss. Direct reaction damage is not a hit/critical, cannot start attack/heal/resource chains, and receives no added Giant Slayer percent because it is this feat's derived reaction packet.",
  "submittedNewChoices": "Broad percent event scope, no-save cripple, complete5ft reaction step/own-reach/direct-damage contract and no recursion.",
  "submittedWorkedCases": [
    "A native27-damage hit against Large adds5 for32 before defenses, independently of other eligible percent sources.",
    "A Huge enemy misses from15ft away while your reach is5. A5ft step cannot reach it, so this Reaction is unavailable; its own15ft reach is not yours."
  ],
  "decision": "Retain the full CF-44 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Broad percent event scope, no-save cripple, complete5ft reaction step/own-reach/direct-damage contract and no recursion.",
  "completeAuthoringProcedure": "Acquire with actual Precision Strike OR total level8. Against actual Large-or-larger creatures, add floor20% of each own direct damage event's eligible native amount before defenses, using shared noncompounding percent arithmetic. This broad damage clause includes own actual spell and weapon components but not periodic/copy/reflection/transfer or companion-owned attacks. Once per SR after a melee attack hits a Huge-or-larger creature, before damage declare the cripple use; after damage halve all its current Speed modes through its next future regular end, retaining spent movement cost. NEW no additional save is invented; same feat family halves once and actual immunities/specific movement protections apply. When a Huge-or-larger enemy misses you with a melee attack, you may spend Reaction for a separate5ft movement-cost step, then, only if that creature is within your own actual melee weapon/natural/unarmed reach and line, deal1d6 direct damage of that legal attack profile's native physical type (bludgeoning for unarmed) without an attack roll. You may step0 if already in reach; normal terrain/opportunity attacks/Speed restrictions apply. If the step cannot bring it into your reach, do not start this Reaction. The original source wording about stepping into its reach does not let you strike from beyond your own reach. It then has disadvantage on its next attack against you before its next future regular end, consumed hit or miss. Direct reaction damage is not a hit/critical, cannot start attack/heal/resource chains, and receives no added Giant Slayer percent because it is this feat's derived reaction packet.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A native27-damage hit against Large adds5 for32 before defenses, independently of other eligible percent sources.",
    "A Huge enemy misses from15ft away while your reach is5. A5ft step cannot reach it, so this Reaction is unavailable; its own15ft reach is not yours."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Acquire with actual Precision Strike OR total level8. Against actual Large-or-larger creatures, add floor20% of each own direct damage event's eligible native amount before defenses, using shared noncompounding percent arithmetic. This broad damage clause includes own actual spell and weapon components but not periodic/copy/reflection/transfer or companion-owned attacks. Once per SR after a melee attack hits a Huge-or-larger creature, before damage declare the cripple use; after damage halve all its current Speed modes through its next future regular end, retaining spent movement cost. NEW no additional save is invented; same feat family halves once and actual immunities/specific movement protections apply. When a Huge-or-larger enemy misses you with a melee attack, you may spend Reaction for a separate5ft movement-cost step, then, only if that creature is within your own actual melee weapon/natural/unarmed reach and line, deal1d6 direct damage of that legal attack profile's native physical type (bludgeoning for unarmed) without an attack roll. You may step0 if already in reach; normal terrain/opportunity attacks/Speed restrictions apply. If the step cannot bring it into your reach, do not start this Reaction. The original source wording about stepping into its reach does not let you strike from beyond your own reach. It then has disadvantage on its next attack against you before its next future regular end, consumed hit or miss. Direct reaction damage is not a hit/critical, cannot start attack/heal/resource chains, and receives no added Giant Slayer percent because it is this feat's derived reaction packet.

### Original-position authored review references

```json
[
  {
    "id": "CF-44-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/86"
  },
  {
    "id": "CF-44-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/87"
  }
]
```

## CF-45 — Life Drinker

### Complete original object

```json
{
  "id": "life_drinker",
  "name": "Life Drinker",
  "description": "Every wound you open is a cup. You drink and stand taller. Prestige lineage: Bloodbound. completed from the existing development record.)",
  "prerequisite": "Dark Affinity or Hemocraft",
  "effect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind actual Dark Affinity/Hemocraft prerequisite IDs without approving them. Resolve critical-hit healing from final paid HP damage versus tempHP/overkill/copied damage, hostile0HP healing identity/cadence and simultaneous triggers; define below-half/creatures-with-blood rider using reviewed healing ledgers."
```

### Preserved original source direction (historical)

```json
{
  "featId": "life_drinker",
  "name": "Life Drinker",
  "cohort": "combat",
  "questionId": "CF-45",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/44",
  "originalQuestion": "Bind actual Dark Affinity/Hemocraft prerequisite IDs without approving them. Resolve critical-hit healing from final paid HP damage versus tempHP/overkill/copied damage, hostile0HP healing identity/cadence and simultaneous triggers; define below-half/creatures-with-blood rider using reviewed healing ledgers.",
  "originalSourceObject": {
    "id": "life_drinker",
    "name": "Life Drinker",
    "description": "Every wound you open is a cup. You drink and stand taller. Prestige lineage: Bloodbound. completed from the existing development record.)",
    "prerequisite": "Dark Affinity or Hemocraft",
    "effect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.",
    "type": "Combat",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "When you score a critical hit with a melee attack, you regain hit points equal to half the damage dealt. When you reduce a hostile creature to 0 hit points with a melee attack, you regain hit points equal to your character level. While you are below half your hit point maximum, your melee weapon attacks deal +1d4 necrotic damage against creatures that have blood.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "e8a531887762cf4732572c9b124ea71580fda2ca81a5b54080613549f3bb5e05",
  "submittedProcedure": "Acquisition requires the exact source feat dark_affinity OR hemocraft, legitimately acquired under its eventual reviewed procedure; neither is silently granted or approved here. NEW finite Life Drinker Recovery Reserve=2×total character level, initially full on feat acquisition and refilled only by a completed LR. Level increases raise capacity without refilling current reserve; capacity reductions clamp without damage. This is a distinct personal feat reserve, not Mutation Recovery Reserve. After your direct melee critical against an independent meaningful hostile resolves, one healing event has base floor(actualDamageDealt/2), using the reviewed metric tempAbsorbed+actualHpDamage with no overkill, floor-protected or state-assignment loss. After your direct melee attack reduces such a hostile from positiveHP to0, a separate healing event has base current total level. NEW resolve critical healing then drop healing if both trigger, spending actualHP restored from the same finite reserve; available reserve caps each after ordinary healing modifiers/prohibitions/max/Critical ceiling. No healing on dead self, no Wound cure, resurrection, copied-damage reward or artificial resource farm. Suppress secondary healing/resource/excess-conversion triggers from these recovery events as an explicit anti-loop choice. Blocked/fullHP healing spends0 reserve but grants no stored heal. While your actual normalHP is strictly below half your current effective maximum before an attack's damage (tempHP excluded), melee weapon attacks against creatures with actual blood add1d4 necrotic before defenses and critical doubling. Actual blood fact, not type-name inference; no rider against known bloodless bodies. The extra die may contribute to that same legitimate critical's numeric damage, never copied again. Healing after the hit cannot retroactively remove its already-qualified die.",
  "submittedNewChoices": "Finite2×level LR reserve, current reviewed temp-inclusive numeric drain metric, meaningful-hostile reward gate, ordered same-hit heals and no secondary conversion; blood/threshold snapshot.",
  "submittedWorkedCases": [
    "A critical deals12resolved to HP3/temp4: actualDamageDealt7, so critical healing base3. The drop also offers level healing; both share remaining reserve.",
    "At level8 with2reserve and missing10HP, a legal base8 drop heal restores at most2 and exhausts reserve. A later critical that day cannot heal until a completed LR."
  ],
  "decision": "Retain the full CF-45 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Finite2×level LR reserve, current reviewed temp-inclusive numeric drain metric, meaningful-hostile reward gate, ordered same-hit heals and no secondary conversion; blood/threshold snapshot.",
  "completeAuthoringProcedure": "Acquisition requires the exact source feat dark_affinity OR hemocraft, legitimately acquired under its eventual reviewed procedure; neither is silently granted or approved here. NEW finite Life Drinker Recovery Reserve=2×total character level, initially full on feat acquisition and refilled only by a completed LR. Level increases raise capacity without refilling current reserve; capacity reductions clamp without damage. This is a distinct personal feat reserve, not Mutation Recovery Reserve. After your direct melee critical against an independent meaningful hostile resolves, one healing event has base floor(actualDamageDealt/2), using the reviewed metric tempAbsorbed+actualHpDamage with no overkill, floor-protected or state-assignment loss. After your direct melee attack reduces such a hostile from positiveHP to0, a separate healing event has base current total level. NEW resolve critical healing then drop healing if both trigger, spending actualHP restored from the same finite reserve; available reserve caps each after ordinary healing modifiers/prohibitions/max/Critical ceiling. No healing on dead self, no Wound cure, resurrection, copied-damage reward or artificial resource farm. Suppress secondary healing/resource/excess-conversion triggers from these recovery events as an explicit anti-loop choice. Blocked/fullHP healing spends0 reserve but grants no stored heal. While your actual normalHP is strictly below half your current effective maximum before an attack's damage (tempHP excluded), melee weapon attacks against creatures with actual blood add1d4 necrotic before defenses and critical doubling. Actual blood fact, not type-name inference; no rider against known bloodless bodies. The extra die may contribute to that same legitimate critical's numeric damage, never copied again. Healing after the hit cannot retroactively remove its already-qualified die.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A critical deals12resolved to HP3/temp4: actualDamageDealt7, so critical healing base3. The drop also offers level healing; both share remaining reserve.",
    "At level8 with2reserve and missing10HP, a legal base8 drop heal restores at most2 and exhausts reserve. A later critical that day cannot heal until a completed LR."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Acquisition requires the exact source feat dark_affinity OR hemocraft, legitimately acquired under its eventual reviewed procedure; neither is silently granted or approved here. NEW finite Life Drinker Recovery Reserve=2×total character level, initially full on feat acquisition and refilled only by a completed LR. Level increases raise capacity without refilling current reserve; capacity reductions clamp without damage. This is a distinct personal feat reserve, not Mutation Recovery Reserve. After your direct melee critical against an independent meaningful hostile resolves, one healing event has base floor(actualDamageDealt/2), using the reviewed metric tempAbsorbed+actualHpDamage with no overkill, floor-protected or state-assignment loss. After your direct melee attack reduces such a hostile from positiveHP to0, a separate healing event has base current total level. NEW resolve critical healing then drop healing if both trigger, spending actualHP restored from the same finite reserve; available reserve caps each after ordinary healing modifiers/prohibitions/max/Critical ceiling. No healing on dead self, no Wound cure, resurrection, copied-damage reward or artificial resource farm. Suppress secondary healing/resource/excess-conversion triggers from these recovery events as an explicit anti-loop choice. Blocked/fullHP healing spends0 reserve but grants no stored heal. While your actual normalHP is strictly below half your current effective maximum before an attack's damage (tempHP excluded), melee weapon attacks against creatures with actual blood add1d4 necrotic before defenses and critical doubling. Actual blood fact, not type-name inference; no rider against known bloodless bodies. The extra die may contribute to that same legitimate critical's numeric damage, never copied again. Healing after the hit cannot retroactively remove its already-qualified die.

### Original-position authored review references

```json
[
  {
    "id": "CF-45-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/88"
  },
  {
    "id": "CF-45-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/89"
  }
]
```

## CF-46 — Precision Strike

### Complete original object

```json
{
  "id": "precision_strike",
  "name": "Precision Strike",
  "description": "One opening. One breath. One strike where the giant's armor forgot to cover bone. Prestige lineage: Giant Killer. completed from the existing development record.)",
  "prerequisite": "Dexterity 13+ or Weapon Focus",
  "effect": "Once per turn when you make a weapon attack, you may take –2 to the attack roll to deal +50% damage on a hit. Against a restrained, grappled, or identified weak point (via Anatomy Lore), you may instead treat a hit as a critical hit once per short rest.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Once per turn when you make a weapon attack, you may take –2 to the attack roll to deal +50% damage on a hit. Against a restrained, grappled, or identified weak point (via Anatomy Lore), you may instead treat a hit as a critical hit once per short rest.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind the explicit Dexterity OR Weapon Focus prerequisite, once-per-turn choice and-2/+50% arithmetic. Resolve whether automatic-critical mode replaces both penalty and percent bonus, restrained/grappled/Anatomy Lore qualification, timing, short-rest charge and immunity/critical-range interfaces."
```

### Preserved original source direction (historical)

```json
{
  "featId": "precision_strike",
  "name": "Precision Strike",
  "cohort": "combat",
  "questionId": "CF-46",
  "disposition": "AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/45",
  "originalQuestion": "Bind the explicit Dexterity OR Weapon Focus prerequisite, once-per-turn choice and-2/+50% arithmetic. Resolve whether automatic-critical mode replaces both penalty and percent bonus, restrained/grappled/Anatomy Lore qualification, timing, short-rest charge and immunity/critical-range interfaces.",
  "originalSourceObject": {
    "id": "precision_strike",
    "name": "Precision Strike",
    "description": "One opening. One breath. One strike where the giant's armor forgot to cover bone. Prestige lineage: Giant Killer. completed from the existing development record.)",
    "prerequisite": "Dexterity 13+ or Weapon Focus",
    "effect": "Once per turn when you make a weapon attack, you may take –2 to the attack roll to deal +50% damage on a hit. Against a restrained, grappled, or identified weak point (via Anatomy Lore), you may instead treat a hit as a critical hit once per short rest.",
    "type": "Combat",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "Once per turn when you make a weapon attack, you may take –2 to the attack roll to deal +50% damage on a hit. Against a restrained, grappled, or identified weak point (via Anatomy Lore), you may instead treat a hit as a critical hit once per short rest.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "6b40598ac4611e9453b5a01aad0db900ce8bf96d864b9be75b7200698bea66d4",
  "submittedProcedure": "Acquire with permanentDEX13 OR the exact Weapon Focus feat. Once per turn before one weapon attack roll choose one mode. Ordinary mode takes−2 on that roll and, on hit, adds floor50% of its eligible native weapon damage before percentages/defenses; actual critical dice are included before this computation. NEW alternative critical mode is available when the actual target is currently Restrained, Grappled, or carries your actual active Anatomy Lore identified-weak-point record. Spend the once-per-SR critical use on declaration; take no−2 and no+50% from this feat for this attack. If it hits, treat it as critical; a miss remains a miss and spends the use and turn allowance. Condition/mark eligibility is rechecked at resolution; losing it leaves an ordinary hit with the use spent. Actual critical immunity remains; no additional critical multiplier. Either mode is mutually exclusive with Power Attack's trade on this same attack. Anatomy Lore's own separately legal bonus can coexist under its precise native-damage scope, with percentages from the same base; the weak-point prerequisite does not grant that feat or let another owner's undisclosed read qualify. A grapple by another creature suffices because that alternative predicate has no ownership restriction.",
  "submittedNewChoices": "Pre-roll mode and SR declaration, replacement of both penalty and percent, own Anatomy Lore record, miss spending and noncompounding interactions.",
  "submittedWorkedCases": [
    "A native21 weapon packet in ordinary mode adds10 for31 before defenses, after taking−2 to hit.",
    "Against a Grappled foe, critical mode rolls normally. On a hit dice double without+50%; on a miss the SR use is still spent."
  ],
  "decision": "Retain the full CF-46 completion and its two boundaries, subject to the named common cadence, targeting, stacking and causal-root corrections. Pre-roll mode and SR declaration, replacement of both penalty and percent, own Anatomy Lore record, miss spending and noncompounding interactions.",
  "completeAuthoringProcedure": "Acquire with permanentDEX13 OR the exact Weapon Focus feat. Once per turn before one weapon attack roll choose one mode. Ordinary mode takes−2 on that roll and, on hit, adds floor50% of its eligible native weapon damage before percentages/defenses; actual critical dice are included before this computation. NEW alternative critical mode is available when the actual target is currently Restrained, Grappled, or carries your actual active Anatomy Lore identified-weak-point record. Spend the once-per-SR critical use on declaration; take no−2 and no+50% from this feat for this attack. If it hits, treat it as critical; a miss remains a miss and spends the use and turn allowance. Condition/mark eligibility is rechecked at resolution; losing it leaves an ordinary hit with the use spent. Actual critical immunity remains; no additional critical multiplier. Either mode is mutually exclusive with Power Attack's trade on this same attack. Anatomy Lore's own separately legal bonus can coexist under its precise native-damage scope, with percentages from the same base; the weak-point prerequisite does not grant that feat or let another owner's undisclosed read qualify. A grapple by another creature suffices because that alternative predicate has no ownership restriction.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A native21 weapon packet in ordinary mode adds10 for31 before defenses, after taking−2 to hit.",
    "Against a Grappled foe, critical mode rolls normally. On a hit dice double without+50%; on a miss the SR use is still spent."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Acquire with permanentDEX13 OR the exact Weapon Focus feat. Once per turn before one weapon attack roll choose one mode. Ordinary mode takes−2 on that roll and, on hit, adds floor50% of its eligible native weapon damage before percentages/defenses; actual critical dice are included before this computation. NEW alternative critical mode is available when the actual target is currently Restrained, Grappled, or carries your actual active Anatomy Lore identified-weak-point record. Spend the once-per-SR critical use on declaration; take no−2 and no+50% from this feat for this attack. If it hits, treat it as critical; a miss remains a miss and spends the use and turn allowance. Condition/mark eligibility is rechecked at resolution; losing it leaves an ordinary hit with the use spent. Actual critical immunity remains; no additional critical multiplier. Either mode is mutually exclusive with Power Attack's trade on this same attack. Anatomy Lore's own separately legal bonus can coexist under its precise native-damage scope, with percentages from the same base; the weak-point prerequisite does not grant that feat or let another owner's undisclosed read qualify. A grapple by another creature suffices because that alternative predicate has no ownership restriction.

### Original-position authored review references

```json
[
  {
    "id": "CF-46-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/90"
  },
  {
    "id": "CF-46-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/91"
  }
]
```

## CF-47 — Slayer’s Resolve

### Complete original object

```json
{
  "id": "slayer_s_resolve",
  "name": "Slayer’s Resolve",
  "description": "You have buried friends under dragonfire. Their memory is armor the wyrms cannot melt. Prestige lineage: Wyrmslayer. completed from the existing development record.)",
  "prerequisite": "Favored Enemy (Dragon) or level 8+",
  "effect": "You are immune to the Frightful Presence of dragons. Allies within 30 feet of you have advantage on saving throws against fear effects while you are conscious. You gain +2 AC against attacks made by dragons. Once per short rest, when a dragon you can see targets you with a breath weapon or melee attack, you may use your reaction to impose disadvantage on that attack or force a new breath save at advantage for yourself only.",
  "type": "Combat",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You are immune to the Frightful Presence of dragons. Allies within 30 feet of you have advantage on saving throws against fear effects while you are conscious. You gain +2 AC against attacks made by dragons. Once per short rest, when a dragon you can see targets you with a breath weapon or melee attack, you may use your reaction to impose disadvantage on that attack or force a new breath save at advantage for yourself only.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

### Original question

```json
"Bind Favored Enemy OR level prerequisite, actual dragon source tags, Frightful Presence versus broader fear immunity, conscious ally aura/line and+2 AC eligibility. Resolve Reaction declaration for attack disadvantage or personal breath-save reroll, information window, mandatory reroll choice and short-rest payment."
```

### Preserved original source direction (historical)

```json
{
  "featId": "slayer_s_resolve",
  "name": "Slayer’s Resolve",
  "cohort": "combat",
  "questionId": "CF-47",
  "disposition": "AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES",
  "sourcePath": "DescentReviewChanges/ReviewBible/data/director/combat_feat_operating_proposal_internal.json",
  "sourceFileSha256": "1ff06bd2b4445178ea08f2ad8a5c4d301cdc51ea3eb763fc8668273f9267aa7b",
  "sourcePointer": "/records/46",
  "originalQuestion": "Bind Favored Enemy OR level prerequisite, actual dragon source tags, Frightful Presence versus broader fear immunity, conscious ally aura/line and+2 AC eligibility. Resolve Reaction declaration for attack disadvantage or personal breath-save reroll, information window, mandatory reroll choice and short-rest payment.",
  "originalSourceObject": {
    "id": "slayer_s_resolve",
    "name": "Slayer’s Resolve",
    "description": "You have buried friends under dragonfire. Their memory is armor the wyrms cannot melt. Prestige lineage: Wyrmslayer. completed from the existing development record.)",
    "prerequisite": "Favored Enemy (Dragon) or level 8+",
    "effect": "You are immune to the Frightful Presence of dragons. Allies within 30 feet of you have advantage on saving throws against fear effects while you are conscious. You gain +2 AC against attacks made by dragons. Once per short rest, when a dragon you can see targets you with a breath weapon or melee attack, you may use your reaction to impose disadvantage on that attack or force a new breath save at advantage for yourself only.",
    "type": "Combat",
    "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
    "legacyEffect": "You are immune to the Frightful Presence of dragons. Allies within 30 feet of you have advantage on saving throws against fear effects while you are conscious. You gain +2 AC against attacks made by dragons. Once per short rest, when a dragon you can see targets you with a breath weapon or melee attack, you may use your reaction to impose disadvantage on that attack or force a new breath save at advantage for yourself only.",
    "status": "provisional-complete",
    "balanceReview": true,
    "draft": false,
    "deprecated": false,
    "needsReview": true
  },
  "originalSourceObjectSha256AsSubmitted": "43b4bb0d64e6f7b4cb154cdd50cb8385f7c904d6f1ce00ec8fbe173606dcdfe3",
  "submittedProcedure": "Acquire with actual Favored Enemy (Dragon) OR total level8. You are immune specifically to actual Dragons' Frightful Presence effects; unrelated dragon fear/spell effects are not automatically that identity. Existing source-qualified Frightful Presence records are suppressed while immunity applies, with clocks retained. While you are conscious, other allied creatures within30ft and with line of effect to you have advantage on saves against effects that actually impose fear/Frightened; no hearing or common-language gate is added. This is current-position aura, checked at each save, not a permanent recipient list and not self-benefit. Gain+2AC against actual attacks made by a creature explicitly typed Dragon; dragonkin alone does not satisfy this feat. Once per SR, when a Dragon you can see makes a melee attack targeting you, spend Reaction before the attack roll to impose disadvantage on that one attack. Alternatively, when such a Dragon's actual breath weapon requires your save, after the initial result but before consequences, spend Reaction and the same shared SR use to reroll your whole save with advantage; independent disadvantage cancels normally and the new result is mandatory. It does not reroll anyone else or waive a no-save breath effect. A breath that instead makes an attack roll is eligible only for the attack mode if it is actually melee; the source's breath-save language creates no new save. Immunities, sight, Reaction prohibitions and actual source tags remain.",
  "submittedNewChoices": "Source-qualified immunity, conscious other-ally aura/line, Dragon-onlyAC, two exact declaration windows and mandatory save reroll.",
  "submittedWorkedCases": [
    "A visible Dragon melee attack prompts the pre-roll Reaction, consuming the shared SR use even if it misses.",
    "A breath DEX save initially fails. The owner rerolls with advantage before damage and must keep the new result; nearby allies keep their own original saves."
  ],
  "decision": "Keep actual source ally wording including self, with original target/sensory/budget conditions; also restore ranged breath-weapon attack rolls.",
  "completeAuthoringProcedure": "Acquire with actual Favored Enemy (Dragon) OR total level8. You are immune specifically to actual Dragons' Frightful Presence effects; unrelated dragon fear/spell effects are not automatically that identity. Existing source-qualified Frightful Presence records are suppressed while immunity applies, with clocks retained. While you are conscious, allied creatures within30ft and with line of effect to you have advantage on saves against effects that actually impose fear/Frightened; no hearing or common-language gate is added. This is current-position aura, checked at each save, not a permanent recipient list; you qualify as your own ally while conscious. Gain+2AC against actual attacks made by a creature explicitly typed Dragon; dragonkin alone does not satisfy this feat. Once per SR, when a Dragon you can see makes a melee attack or an attack-roll breath weapon targeting you, spend Reaction before the attack roll to impose disadvantage on that one attack. Alternatively, when such a Dragon's actual breath weapon requires your save, after the initial result but before consequences, spend Reaction and the same shared SR use to reroll your whole save with advantage; independent disadvantage cancels normally and the new result is mandatory. It does not reroll anyone else or waive a no-save breath effect. A breath weapon with an attack roll qualifies for the attack branch whether melee or ranged; no saving throw is invented for it. Non-breath ranged attacks do not qualify. Immunities, sight, Reaction prohibitions and actual source tags remain.\nSOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.\nEXACT BREATH-ATTACK CORRECTION: the once-short-rest Reaction may impose disadvantage, before its roll, on one attack roll of a perceived Dragon breath weapon, whether melee or ranged, or on a perceived Dragon melee attack. A non-breath ranged attack does not qualify. A saving-throw breath weapon instead uses the personal breath-save reroll branch after the initial result, whether it succeeded or failed, and before consequences, rerolling with advantage and using the new result. No attack or save is invented for a payload that has neither.",
  "newRuleProvenance": "All submitted NEW/proposed completions retained by this decision and all departures below are authoring decisions of FEAT327-SOURCE-2026-10-11, not recovered source wording. The original object remains immutable.",
  "sharedContract": "FEAT_SHARED_DIRECTIONS.json: FS-01–16",
  "supplementContract": "FEAT_SUPPLEMENT_DIRECTIONS.json: explicit source path/pointer mappings",
  "workedCases": [
    "A conscious holder within their own aura qualifies for its fear-save advantage. A Dragon melee attack against them gets the stated+2AC; dragonkin without the actual Dragon type does not.",
    "A perceived Dragon breath weapon makes a ranged attack roll. A legal pre-roll Reaction spends the shared short-rest use and imposes disadvantage. A saving-throw breath uses the personal breath-save reroll branch, after success or failure but before consequences, instead; a non-breath ranged attack does not qualify for either branch merely because its attacker is a Dragon."
  ],
  "payloadOperational": "full authored procedure; not a runtime adapter",
  "selectionEnabled": false,
  "exactApproved": false,
  "runtimeApproved": false
}
```

### Complete current candidate procedure

Acquire with actual Favored Enemy (Dragon) OR total level8. You are immune specifically to actual Dragons' Frightful Presence effects; unrelated dragon fear/spell effects are not automatically that identity. Existing source-qualified Frightful Presence records are suppressed while immunity applies, with clocks retained. While you are conscious, allied creatures within30ft and with line of effect to you have advantage on saves against effects that actually impose fear/Frightened; no hearing or common-language gate is added. This is current-position aura, checked at each save, not a permanent recipient list; you qualify as your own ally while conscious. Gain+2AC against actual attacks made by a creature explicitly typed Dragon; dragonkin alone does not satisfy this feat. Once per SR, when a Dragon you can see makes a melee attack or an attack-roll breath weapon targeting you, spend Reaction before the attack roll to impose disadvantage on that one attack. Alternatively, when such a Dragon's actual breath weapon requires your save, after the initial result but before consequences, spend Reaction and the same shared SR use to reroll your whole save with advantage; independent disadvantage cancels normally and the new result is mandatory. It does not reroll anyone else or waive a no-save breath effect. A breath weapon with an attack roll qualifies for the attack branch whether melee or ranged; no saving throw is invented for it. Non-breath ranged attacks do not qualify. Immunities, sight, Reaction prohibitions and actual source tags remain.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.
EXACT BREATH-ATTACK CORRECTION: the once-short-rest Reaction may impose disadvantage, before its roll, on one attack roll of a perceived Dragon breath weapon, whether melee or ranged, or on a perceived Dragon melee attack. A non-breath ranged attack does not qualify. A saving-throw breath weapon instead uses the personal breath-save reroll branch after the initial result, whether it succeeded or failed, and before consequences, rerolling with advantage and using the new result. No attack or save is invented for a payload that has neither.

### Original-position authored review references

```json
[
  {
    "id": "CF-47-E01",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/92"
  },
  {
    "id": "CF-47-E02",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/originalCaseReviews/93"
  },
  {
    "id": "FA-08",
    "report": {
      "path": "docs/audit/2026-10-08/full-game/FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json",
      "bytes": 713560,
      "sha256": "4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8"
    },
    "pointer": "/additionalBoundaryReviews/1"
  }
]
```
