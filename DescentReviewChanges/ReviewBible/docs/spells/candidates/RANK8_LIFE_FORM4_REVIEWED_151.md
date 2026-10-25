# Life/Form4 — Director Return151

Static authored review only. Input authority709 applied-reviewed /139 pending /0 accepted-unapplied. Canonical files unchanged. Each procedure includes immutable native card/access data, common operating rules and its spell-local decisions. Retained holds and exact source records travel with this return.

## Animal Shapes

Procedure identity: animal-shapes. Canonical native status remains blocked-pending-operational-review; proposed procedure is separate.

### Native source and access (unchanged)

```json
{
  "id": "animal-shapes",
  "name": "Animal Shapes",
  "schools": [
    "Transmutation"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Transmutation",
      "baseRpCost": 21
    },
    "Mage": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Transmutation",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Transmutation",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "animal-shapes",
    "original": {
      "name": "Animal Shapes",
      "level": 8,
      "resonanceRank": 8,
      "school": "Transmutation",
      "schools": [
        "Transmutation"
      ],
      "placements": [
        {
          "name": "Animal Shapes",
          "school": "Transmutation",
          "level": 8,
          "summary": "Transform willing creatures into chosen beasts."
        }
      ],
      "classLevels": {
        "Druid": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Druid": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Druid": 15,
        "Mage": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Druid": "Transmutation",
        "Mage": "Transmutation",
        "Wizard": "Transmutation"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Transform willing creatures into chosen beasts.",
      "alternateSummaries": [],
      "classes": [
        "Druid",
        "Mage",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 815,
        "original": {
          "school": "Transmutation",
          "level": 8,
          "name": "Animal Shapes",
          "effect": "Transform willing creatures into chosen beasts.",
          "source_paragraph": 9989,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Core resolution requires an explicit operational interpretation",
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### scope

NEW spell-local operational authorship only. Native source envelopes are immutable; they still say blocked-pending-operational-review and operational=null. The isolated proposal is not installed in the live catalog. Exact accepted interfaces are reproduced in ORIGINAL_SOURCE_RECORDS.json; no later backing-file changes become accepted merely by presence.

### access

Use the native classAccess rows exactly, actual class level, actual known/book/prepared entry, class prerequisites and available rank. Rank8 costs21RP before actual source-specific adjustments; no Overcast, invented acquisition, global discounts, slots or imported costly components. V/S/F, ordinary Action, one perceived target or declared target set within120ft and unobstructed line of effect at commitment and application. A focus is an actual accessible item; no material cost is added. Missing access or known physical illegality prevents commitment. Hidden disqualification after a lawful commitment spends the cast without an oracle or substitute target.

### commitment

Resolve actual current defenses, legal ability to act, anatomy/components and perception before committing. Spend Action and actual21RP; record exact family, base strain, Refrain, Dissonance and any source-specific hooks. Wizard first prepared family in encounter has0 base strain; rank8 repeated family uses base2 plus actual Refrain. Other ordinary classes use rank8 base2 plus Refrain. Read Dissonance before casting: limit=max(4,2+PB+max(0,casting modifier)); ranked surcharge at limit/limit+3/limit+6 is+1/+2/+3RP, and ordinary rank1+ casting is blocked at limit+6 absent an actual expressly granted traumatic exception. Refrain for consecutive same-name casts is+1/+2/+3 capped3; a different name resets it to0, idle/weapon turns do not. Track all actual threshold consequences if reached. Nondamaging Life/Form spells are not damaging Mage Focus casts: clear Nuke Chain; no Surge damage or chain award. Animal Shapes is not Druid Shapeshift and clears no Refrain or reserves.

### timing

Use elapsed seconds plus original regular-slot marker and phase. Absolute expiry at phase0 wins before new events at that timestamp. Complete an already resolving packet under its actual source ordering; no extra turns tick clocks. Ready uses its own actual Action commitment, components,21RP/strain and concentration hold, then one eligible Reaction release before its deadline; it gives no free cast or renewed duration. Ready selects the legal target set/area and any required body/form/anchor choices at release, not at preparation, as the accepted Ready exception. Revalidate every prerequisite and all-outcome fit before spending the release Reaction; invalid/declined occurrence may await another valid trigger until next regular own-turn START, with setup cost retained. Counterspell is at preparation only. Effect duration/maturity starts at successful release/application, not preparation. For Animal Shapes a concentration hold becomes the shared effect on successful release; loss/failure does not restore prior concentration. Other effects end the Ready hold after resolution.

### defenses

Use actual acquired Counterspell, reflection, immunity, antimagic, dispel and concentration records within exact scope, not spell names or guessed ranks. All four are rank8 for applicable checks. A class Wizard Dispel is rank3 at its printed3RP/check10+target rank; it is never Greater Dispel rank5. Source-specific counter success is necessary; a suppressed effect is not terminated unless its source says so. New Animal concentration ends old same-caster concentration at commitment, before counter/save/failure. Nonconcentration Clone/Flesh/Perfect do not end other concentration unless Ready does.

### returnsAndOwnership

Preserve actors, real body and item IDs, personal HP/max ledger, temporaryHP, Wounds/injuries, actual conditions, paid resources, spent turn markers, debts, death and return histories. Do not infer ownership, loyalty, soul geography, CR, content permission, creature roster or preparation from a title. Actual death ends concentration and only the effects whose sources end on death; completed memory losses and other persistent personal consequences are retained. Every fixture is synthetic data for a static rule trace, not an acquired campaign character or physical-world proof.

### holds

Source/access/content/form/body geometry/identity topology/runtime/human-play/balance/release holds survive this return. A missing prerequisite holds the whole dependent case or branch; it cannot be narrated as a positive actual campaign result. All changed rules below are NEW only for these four spells.

### selection

NEW for an ordinary cast select1–10 distinct willing perceived physical creature-origin recipients and one of the seven complete animal mappings per recipient before commitment. The common accepted Ready exception instead selects this set at release after paid preparation; fit is then checked before the release Reaction. No mass opt-in later, arbitrary bestiary, CR filtering, hidden target replacement or switching forms during the effect. Form names denote actual chosen spell-local beast anatomy, not a change of origin taxonomy. Object-origin transformed objects, summon bodies with incompatible lifecycle, unknown anatomy/mass and undocumented origin require their own established source; otherwise that dependent branch is held. Actual willing withdrawal before resolution makes only that recipient fail, with cost retained.

### duration

NEW one shared rank8 concentration record expires exactly60elapsedseconds after successful application; individual target links may end separately. Caster concentration loss/death ends all links; ending the final target link ends this now-empty shared concentration. Range120 is acquisition/application only, not a maintained tether. No extra body, turn, HP pool, concentration slot or form-switch Action is granted.

### geometry

NEW reuse accepted all-outcome fit: before ordinary payment (or before an already-paid Ready release Reaction) every target origin O and proposed transformed T must fit simultaneously for every pair O/O,O/T,T/O,T/T, other creatures, occupied matter and height. Reproject roots when this caster must drop an earlier concentration. Recheck at resolution; hidden newly blocked recipient fails, no displacement of another actor. Mandatory reversion ends the form even if placement becomes difficult: source-scoped BODY same anchor, actual legal squeeze, then nearest legal adjacent in the same unobstructed region, minimum displacement/greatest overlap/fixed neutral board tie; no farther search or barrier crossing. If none, record placementConflict and hold geometry-dependent continuation. Banishment-specific conflict rules are not globalized.

### identityAndGear

NEW explicitly reuse accepted creature transformation conservation. Scores, PB, HP/max/tempHP, class resources, Wounds, injuries, identity, species/ancestry, conditions and initiative remain real. Only listed anatomy/movement/AC/natural attack changes. Base body weight unchanged even across sizes; actual cargo still weighs including melded items; BODY carry/load and actual anatomy restrictions apply. Earliest root carried gear becomes melded, inaccessible, custody unchanged; incompatible armor/features cease expression. Existing external cargo stays external. Successful legal replacement closes previous anatomy atomically and recaptures actual extant gear once, never restores consumed items, charges or healing. No displaced form stack. Druid class Shapeshift cannot enter while a spell-form record remains, including suppressed.

### attacks

NEW use current original caster attack bonus/M for the mapped natural attack; original caster statistics must be actually resolvable. Subject is the attacker/damage owner for Null, kill credit and reactions; no caster cast-proc on a natural attack. One attack per ordinary Attack Action, reach5, listed dice+M; no Multiattack, spells, magic attacks, class beast benefits or senses beyond mapped/existing compatible source. Missing caster-stat provenance holds the attack branch; other links do not disappear.

### endings

Temporary form ends for that target on actual normalHP0, actual death or external Incapacitated after same-packet survival replacements. A real remain-at1 intervention prevents that zero ending. Each willing recipient may reject using one ordinary Action on its own regular turn if actually able, even while suppressed. New rank8 temporary anatomy may replace actual temporary ranks≤8 on success, not permanent True Polymorph absent its exact exception. A failed new cast leaves another caster’s prior form; same-caster concentration already ended is never restored.

### suppression

Suppression expresses earliest root anatomy while original melded gear remains inaccessible; it does not recapture gear, refund RP, end concentration, pause deadline or restore a displaced form. Unsuppression restores only a surviving unexpired link. Loss of actual flight begins accepted Falling now, first descent at END of the enclosing original regular slot NEXT round, then6second steps≤300ft. No instant ground teleport; actual landing damage min(10,floor(uncontrolledFeet/20))d6, positive damage causes Prone. Regaining adequate flight ends Falling without impact.

### forms

```json
[
  {
    "animal": "wolf",
    "profile": "Predator",
    "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion",
    "size": "Medium",
    "horizontalFeet": [
      5,
      5
    ],
    "requiredHeightFeet": 4,
    "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.",
    "baseBodyMass": "unchanged actual origin pounds",
    "walk": 40,
    "fly": 0,
    "swim": 0,
    "burrowLooseSoil": 0,
    "hover": false,
    "AC": "max(actual compatible ordinary AC,13)",
    "hands": false,
    "speech": false,
    "senses": [
      "ordinary sight",
      "ordinary hearing"
    ],
    "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.",
    "attack": {
      "countPerAttackAction": 1,
      "reachFeet": 5,
      "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses",
      "damageDice": "1d8",
      "damageModifier": "max(1,current original caster casting ability modifier)",
      "type": "slashing",
      "magicalByDefault": false,
      "damageOwner": "subject"
    }
  },
  {
    "animal": "brown bear",
    "profile": "Brute",
    "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion",
    "size": "Large",
    "horizontalFeet": [
      10,
      10
    ],
    "requiredHeightFeet": 8,
    "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.",
    "baseBodyMass": "unchanged actual origin pounds",
    "walk": 30,
    "fly": 0,
    "swim": 0,
    "burrowLooseSoil": 0,
    "hover": false,
    "AC": "max(actual compatible ordinary AC,15)",
    "hands": false,
    "speech": false,
    "senses": [
      "ordinary sight",
      "ordinary hearing"
    ],
    "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.",
    "attack": {
      "countPerAttackAction": 1,
      "reachFeet": 5,
      "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses",
      "damageDice": "2d6",
      "damageModifier": "max(1,current original caster casting ability modifier)",
      "type": "bludgeoning",
      "magicalByDefault": false,
      "damageOwner": "subject"
    }
  },
  {
    "animal": "hawk",
    "profile": "Avian",
    "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion",
    "size": "Small",
    "horizontalFeet": [
      5,
      5
    ],
    "requiredHeightFeet": 3,
    "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.",
    "baseBodyMass": "unchanged actual origin pounds",
    "walk": 10,
    "fly": 50,
    "swim": 0,
    "burrowLooseSoil": 0,
    "hover": false,
    "AC": "max(actual compatible ordinary AC,13)",
    "hands": false,
    "speech": false,
    "senses": [
      "ordinary sight",
      "ordinary hearing"
    ],
    "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.",
    "attack": {
      "countPerAttackAction": 1,
      "reachFeet": 5,
      "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses",
      "damageDice": "1d6",
      "damageModifier": "max(1,current original caster casting ability modifier)",
      "type": "slashing",
      "magicalByDefault": false,
      "damageOwner": "subject"
    }
  },
  {
    "animal": "dolphin",
    "profile": "Aquatic",
    "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion",
    "size": "Medium",
    "horizontalFeet": [
      5,
      5
    ],
    "requiredHeightFeet": 3,
    "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.",
    "baseBodyMass": "unchanged actual origin pounds",
    "walk": 20,
    "fly": 0,
    "swim": 50,
    "burrowLooseSoil": 0,
    "hover": false,
    "AC": "max(actual compatible ordinary AC,14)",
    "hands": false,
    "speech": false,
    "senses": [
      "ordinary sight",
      "ordinary hearing"
    ],
    "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.",
    "attack": {
      "countPerAttackAction": 1,
      "reachFeet": 5,
      "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses",
      "damageDice": "1d8",
      "damageModifier": "max(1,current original caster casting ability modifier)",
      "type": "piercing",
      "magicalByDefault": false,
      "damageOwner": "subject"
    }
  },
  {
    "animal": "badger",
    "profile": "Burrower",
    "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion",
    "size": "Medium",
    "horizontalFeet": [
      5,
      5
    ],
    "requiredHeightFeet": 3,
    "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.",
    "baseBodyMass": "unchanged actual origin pounds",
    "walk": 30,
    "fly": 0,
    "swim": 0,
    "burrowLooseSoil": 15,
    "hover": false,
    "AC": "max(actual compatible ordinary AC,14)",
    "hands": false,
    "speech": false,
    "senses": [
      "ordinary sight",
      "ordinary hearing"
    ],
    "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.",
    "attack": {
      "countPerAttackAction": 1,
      "reachFeet": 5,
      "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses",
      "damageDice": "1d8",
      "damageModifier": "max(1,current original caster casting ability modifier)",
      "type": "bludgeoning",
      "magicalByDefault": false,
      "damageOwner": "subject"
    }
  },
  {
    "animal": "elephant",
    "profile": "Greater brute",
    "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion",
    "size": "Large",
    "horizontalFeet": [
      10,
      10
    ],
    "requiredHeightFeet": 10,
    "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.",
    "baseBodyMass": "unchanged actual origin pounds",
    "walk": 40,
    "fly": 0,
    "swim": 0,
    "burrowLooseSoil": 0,
    "hover": false,
    "AC": "max(actual compatible ordinary AC,17)",
    "hands": false,
    "speech": false,
    "senses": [
      "ordinary sight",
      "ordinary hearing"
    ],
    "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.",
    "attack": {
      "countPerAttackAction": 1,
      "reachFeet": 5,
      "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses",
      "damageDice": "2d8",
      "damageModifier": "max(1,current original caster casting ability modifier)",
      "type": "bludgeoning",
      "magicalByDefault": false,
      "damageOwner": "subject"
    }
  },
  {
    "animal": "giant condor",
    "profile": "Greater winged",
    "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion",
    "size": "Large",
    "horizontalFeet": [
      10,
      10
    ],
    "requiredHeightFeet": 8,
    "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.",
    "baseBodyMass": "unchanged actual origin pounds",
    "walk": 20,
    "fly": 60,
    "swim": 0,
    "burrowLooseSoil": 0,
    "hover": false,
    "AC": "max(actual compatible ordinary AC,16)",
    "hands": false,
    "speech": false,
    "senses": [
      "ordinary sight",
      "ordinary hearing"
    ],
    "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.",
    "attack": {
      "countPerAttackAction": 1,
      "reachFeet": 5,
      "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses",
      "damageDice": "2d8",
      "damageModifier": "max(1,current original caster casting ability modifier)",
      "type": "slashing",
      "magicalByDefault": false,
      "damageOwner": "subject"
    }
  }
]
```

## Clone

Procedure identity: clone. Canonical native status remains blocked-pending-operational-review; proposed procedure is separate.

### Native source and access (unchanged)

```json
{
  "id": "clone",
  "name": "Clone",
  "schools": [
    "Necromancy"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    },
    "Druid": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "clone",
    "original": {
      "name": "Clone",
      "level": 8,
      "resonanceRank": 8,
      "school": "Necromancy",
      "schools": [
        "Necromancy"
      ],
      "placements": [
        {
          "name": "Clone",
          "school": "Necromancy",
          "level": 8,
          "summary": "Grow duplicate of a creature as insurance against death."
        }
      ],
      "classLevels": {
        "Cleric": 8,
        "Druid": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Cleric": 8,
        "Druid": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Cleric": 15,
        "Druid": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Cleric": "Necromancy",
        "Druid": "Necromancy",
        "Wizard": "Necromancy"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Grow duplicate of a creature as insurance against death.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 708,
        "original": {
          "school": "Necromancy",
          "level": 8,
          "name": "Clone",
          "effect": "Grow duplicate of a creature as insurance against death.",
          "source_paragraph": 9857,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Core resolution requires an explicit operational interpretation",
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### scope

NEW spell-local operational authorship only. Native source envelopes are immutable; they still say blocked-pending-operational-review and operational=null. The isolated proposal is not installed in the live catalog. Exact accepted interfaces are reproduced in ORIGINAL_SOURCE_RECORDS.json; no later backing-file changes become accepted merely by presence.

### access

Use the native classAccess rows exactly, actual class level, actual known/book/prepared entry, class prerequisites and available rank. Rank8 costs21RP before actual source-specific adjustments; no Overcast, invented acquisition, global discounts, slots or imported costly components. V/S/F, ordinary Action, one perceived target or declared target set within120ft and unobstructed line of effect at commitment and application. A focus is an actual accessible item; no material cost is added. Missing access or known physical illegality prevents commitment. Hidden disqualification after a lawful commitment spends the cast without an oracle or substitute target.

### commitment

Resolve actual current defenses, legal ability to act, anatomy/components and perception before committing. Spend Action and actual21RP; record exact family, base strain, Refrain, Dissonance and any source-specific hooks. Wizard first prepared family in encounter has0 base strain; rank8 repeated family uses base2 plus actual Refrain. Other ordinary classes use rank8 base2 plus Refrain. Read Dissonance before casting: limit=max(4,2+PB+max(0,casting modifier)); ranked surcharge at limit/limit+3/limit+6 is+1/+2/+3RP, and ordinary rank1+ casting is blocked at limit+6 absent an actual expressly granted traumatic exception. Refrain for consecutive same-name casts is+1/+2/+3 capped3; a different name resets it to0, idle/weapon turns do not. Track all actual threshold consequences if reached. Nondamaging Life/Form spells are not damaging Mage Focus casts: clear Nuke Chain; no Surge damage or chain award. Animal Shapes is not Druid Shapeshift and clears no Refrain or reserves.

### timing

Use elapsed seconds plus original regular-slot marker and phase. Absolute expiry at phase0 wins before new events at that timestamp. Complete an already resolving packet under its actual source ordering; no extra turns tick clocks. Ready uses its own actual Action commitment, components,21RP/strain and concentration hold, then one eligible Reaction release before its deadline; it gives no free cast or renewed duration. Ready selects the legal target set/area and any required body/form/anchor choices at release, not at preparation, as the accepted Ready exception. Revalidate every prerequisite and all-outcome fit before spending the release Reaction; invalid/declined occurrence may await another valid trigger until next regular own-turn START, with setup cost retained. Counterspell is at preparation only. Effect duration/maturity starts at successful release/application, not preparation. For Animal Shapes a concentration hold becomes the shared effect on successful release; loss/failure does not restore prior concentration. Other effects end the Ready hold after resolution.

### defenses

Use actual acquired Counterspell, reflection, immunity, antimagic, dispel and concentration records within exact scope, not spell names or guessed ranks. All four are rank8 for applicable checks. A class Wizard Dispel is rank3 at its printed3RP/check10+target rank; it is never Greater Dispel rank5. Source-specific counter success is necessary; a suppressed effect is not terminated unless its source says so. New Animal concentration ends old same-caster concentration at commitment, before counter/save/failure. Nonconcentration Clone/Flesh/Perfect do not end other concentration unless Ready does.

### returnsAndOwnership

Preserve actors, real body and item IDs, personal HP/max ledger, temporaryHP, Wounds/injuries, actual conditions, paid resources, spent turn markers, debts, death and return histories. Do not infer ownership, loyalty, soul geography, CR, content permission, creature roster or preparation from a title. Actual death ends concentration and only the effects whose sources end on death; completed memory losses and other persistent personal consequences are retained. Every fixture is synthetic data for a static rule trace, not an acquired campaign character or physical-world proof.

### holds

Source/access/content/form/body geometry/identity topology/runtime/human-play/balance/release holds survive this return. A missing prerequisite holds the whole dependent case or branch; it cannot be narrated as a positive actual campaign result. All changed rules below are NEW only for these four spells.

### eligibility

NEW one willing living physical creature-origin identity with a documented reproducible persistent root body. Perceive the source within120ft/LoE and designate a legal unoccupied growth envelope adjacent to it and also within120ft/LoE, same established plane. No printed vessel, blood sample, gem or extra price is added. Physical Constructs are not automatically excluded if actually living/reproducible by their own source; HP-only animations, transformed objects and temporary summoned bodies gain no Clone eligibility by appearance. Unknown reproduction/physiology holds the whole dependent branch. Validate the entire root body envelope, mass and missing parts, excluding temporary form anatomy and gear.

### growth

NEW the paid instantaneous cast produces one full-size inert immature physical duplicate at that anchor; it never acts, has no personal identity, inventory, class resources or companion slot. Maturity at createdAt+86400elapsedseconds, phase0 before a new death check at equality. No concentration; clock continues in antimagic. The magical rank8 insurance link persists until consumed, replaced, destroyed with the body, or actually ended by a source-qualified dispel. Caster death alone does not end it. Physical matter is not a maintained magical body and does not vanish in suppression.

### body

NEW dormant replacement body uses object-like structural AC10 and20structuralHP, no resistance, immunity, regeneration or separate personal HP pool. At structural0 it is destroyed and its entitlement ends. The intact viable-return gate requires structuralHP20 and no new anatomy/storage damage; partial damage blocks return until actual applicable repair restores structural20 and anatomy. Structural repair never heals the source character. Dormancy supplies only no metabolic air/food/water consumption while uninhabited, an explicit Clone-local completion; temperature, fire, pressure, decay, crushing and physical movement use actual applicable sources. No implicit safe vessel, preservation against environmental harm or free moving body. Repeated paid casts can leave multiple inert physical bodies; the finite cap is one live entitlement, not a world population limit. Missing hazard/storage content holds the affected branch. Detached matter or replaced bodies do not acquire autonomous life, XP, harvest awards or new spell fuel by this procedure.

### entitlement

NEW at most one live insurance entitlement per source identity across all casters. Only successful valid new establishment replaces the old link, not its physical body. Failed/blocked/countered attempt leaves the older link. Store unique entitlementId, bodyId, sourceIdentity, creator, body snapshot, timestamps, suppression, condition and attempted death IDs. Consumed/replaced bodies have no duplicate entitlement; their physical provenance remains.

### trigger

NEW actual completed death, after applicable would-die replacements and actual death triggers, opens one immediate optional return attempt. Earlier survival means no death ID and no Clone attempt. Require actual identity dead, actual willingness, mature/intact eligible unclaimed body, unsuppressed/unended link, legal destination and real return permissions. Another already successful return/claim wins; there can be only one living personal identity. Check identity-level barriers such as actual Soul Bind globally by their exact scope. Clone uses the stored body as its local return anchor: corpse-local Mass Resurrection Denial at the old corpse alone does not block a different stored anchor outside it; a matching actual barrier at the stored body does. Old corpse remains is not the paid return body. Cross-plane routing and unknown soul/topology facts are held, not granted by range120.

### claim

NEW resolve one atomic claim of the eligible body and identity, consume entitlement once, retire the dormant structuralHP pool (retain its historical damage record but it is no longer an active pool), then assign life1normalHP with present lawful maximum and protected lethal-track handling from the later healing/death closure. No HP-healing multiplier or living cannot-regain-HP effect converts this life assignment to healing or0HP. Actual life/identity barrier prevents claim before assignment. Record this death ID attempted even on decline/immaturity/suppression/occupation/barrier failure; no queued resurrection, delayed eligibility, repeat or replay. An intact unconsumed link may remain for a later genuinely distinct death after an actual intervening return, not continued retry of this death. Destroyed/replaced/ended links cannot.

### conservation

Return relocates the one personal identity into the actual clone body; physical old remains and their actual gear persist at their old positions but all other remains lose duplicate-return eligibility. No cloned gear, RP, spellbook, slots, daily uses, Wounds, injuries, exhaustion, debt or memory reset. Present personal scores/progression and HP ledger apply, not the creation snapshot. Concentration ended on death stays ended. Current personal injuries remain functional restrictions on the stored body; an older intact limb is not permission to cure a current missing-limb injury. Actual clone damage imposes its own restrictions too. Unsupported anatomy reconciliation is held; no mass/limb restoration is inferred. Protected Exhaustion6 returns alive and collapsed under later healing/death, not immediately re-killed by maximum recomputation.

### suppressionAndTermination

Actual antimagic suppresses only the magical link/attempt, not physical stored matter or maturation time. Ending suppression never replays old death. A source-qualified successful rank8 dispel ends the link permanently but leaves the body inert. Moving/damaging/storage acts require actual actors/actions/material predicates. No indestructible remote soul container or soul-sensing information is granted.

## Flesh to Grave

Procedure identity: flesh-to-grave. Canonical native status remains blocked-pending-operational-review; proposed procedure is separate.

### Native source and access (unchanged)

```json
{
  "id": "flesh-to-grave",
  "name": "Flesh to Grave",
  "schools": [
    "Necromancy"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    },
    "Druid": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Necromancy",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "flesh-to-grave",
    "original": {
      "name": "Flesh to Grave",
      "level": 8,
      "resonanceRank": 8,
      "school": "Necromancy",
      "schools": [
        "Necromancy"
      ],
      "placements": [
        {
          "name": "Flesh to Grave",
          "school": "Necromancy",
          "level": 8,
          "summary": "Target with <100 HP must CON save or die and rise as undead."
        }
      ],
      "classLevels": {
        "Cleric": 8,
        "Druid": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Cleric": 8,
        "Druid": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Cleric": 15,
        "Druid": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Cleric": "Necromancy",
        "Druid": "Necromancy",
        "Wizard": "Necromancy"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Target with <100 HP must CON save or die and rise as undead.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 707,
        "original": {
          "school": "Necromancy",
          "level": 8,
          "name": "Flesh to Grave",
          "effect": "Target with <100 HP must CON save or die and rise as undead.",
          "source_paragraph": 9856,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Constitution save",
          "tags": [
            "Utility"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### scope

NEW spell-local operational authorship only. Native source envelopes are immutable; they still say blocked-pending-operational-review and operational=null. The isolated proposal is not installed in the live catalog. Exact accepted interfaces are reproduced in ORIGINAL_SOURCE_RECORDS.json; no later backing-file changes become accepted merely by presence.

### access

Use the native classAccess rows exactly, actual class level, actual known/book/prepared entry, class prerequisites and available rank. Rank8 costs21RP before actual source-specific adjustments; no Overcast, invented acquisition, global discounts, slots or imported costly components. V/S/F, ordinary Action, one perceived target or declared target set within120ft and unobstructed line of effect at commitment and application. A focus is an actual accessible item; no material cost is added. Missing access or known physical illegality prevents commitment. Hidden disqualification after a lawful commitment spends the cast without an oracle or substitute target.

### commitment

Resolve actual current defenses, legal ability to act, anatomy/components and perception before committing. Spend Action and actual21RP; record exact family, base strain, Refrain, Dissonance and any source-specific hooks. Wizard first prepared family in encounter has0 base strain; rank8 repeated family uses base2 plus actual Refrain. Other ordinary classes use rank8 base2 plus Refrain. Read Dissonance before casting: limit=max(4,2+PB+max(0,casting modifier)); ranked surcharge at limit/limit+3/limit+6 is+1/+2/+3RP, and ordinary rank1+ casting is blocked at limit+6 absent an actual expressly granted traumatic exception. Refrain for consecutive same-name casts is+1/+2/+3 capped3; a different name resets it to0, idle/weapon turns do not. Track all actual threshold consequences if reached. Nondamaging Life/Form spells are not damaging Mage Focus casts: clear Nuke Chain; no Surge damage or chain award. Animal Shapes is not Druid Shapeshift and clears no Refrain or reserves.

### timing

Use elapsed seconds plus original regular-slot marker and phase. Absolute expiry at phase0 wins before new events at that timestamp. Complete an already resolving packet under its actual source ordering; no extra turns tick clocks. Ready uses its own actual Action commitment, components,21RP/strain and concentration hold, then one eligible Reaction release before its deadline; it gives no free cast or renewed duration. Ready selects the legal target set/area and any required body/form/anchor choices at release, not at preparation, as the accepted Ready exception. Revalidate every prerequisite and all-outcome fit before spending the release Reaction; invalid/declined occurrence may await another valid trigger until next regular own-turn START, with setup cost retained. Counterspell is at preparation only. Effect duration/maturity starts at successful release/application, not preparation. For Animal Shapes a concentration hold becomes the shared effect on successful release; loss/failure does not restore prior concentration. Other effects end the Ready hold after resolution.

### defenses

Use actual acquired Counterspell, reflection, immunity, antimagic, dispel and concentration records within exact scope, not spell names or guessed ranks. All four are rank8 for applicable checks. A class Wizard Dispel is rank3 at its printed3RP/check10+target rank; it is never Greater Dispel rank5. Source-specific counter success is necessary; a suppressed effect is not terminated unless its source says so. New Animal concentration ends old same-caster concentration at commitment, before counter/save/failure. Nonconcentration Clone/Flesh/Perfect do not end other concentration unless Ready does.

### returnsAndOwnership

Preserve actors, real body and item IDs, personal HP/max ledger, temporaryHP, Wounds/injuries, actual conditions, paid resources, spent turn markers, debts, death and return histories. Do not infer ownership, loyalty, soul geography, CR, content permission, creature roster or preparation from a title. Actual death ends concentration and only the effects whose sources end on death; completed memory losses and other persistent personal consequences are retained. Every fixture is synthetic data for a static rule trace, not an acquired campaign character or physical-world proof.

### holds

Source/access/content/form/body geometry/identity topology/runtime/human-play/balance/release holds survive this return. A missing prerequisite holds the whole dependent case or branch; it cannot be narrated as a positive actual campaign result. All changed rules below are NEW only for these four spells.

### eligibility

NEW one perceived living physical creature within120ft/LoE. Actual current normalHP must be strictly<100 at application; temporaryHP never enters the threshold. Living dying0 qualifies; already dead/nonliving HP-only animation does not. This is an explicit living target completion, not an inferred universal Necromancy immunity. Known impossible target rejects before pay; hidden100+, hidden nonliving identity or changed eligibility spends a lawful commitment without numeric disclosure, no retarget. Eligible target makes one binary CON save against actual caster DC; success prevents both death and rising.

### death

On failure and after actual applicable defenses, resolve a nondamage would-die event. No necrotic damage, damage root, Wound save, zero-HP damage threshold or death-save failure is fabricated. TemporaryHP, resistances, caster Null Veil damage nonlethality and ordinary Death Ward positive-to-zero floor do not themselves prevent this event. A real applicable would-die replacement (e.g. actually acquired Cleric16 Ritual of Undeath Ward, already paid and active) can prevent death; then no rising. Finish actual death and its sourced triggers/claims before attempting body allocation.

### rising

NEW physical Ghoul-derived animation, explicitly not a same-person undead resurrection. Only this spell’s actual completed death can supply its same usable body. If a prior actual death-trigger return such as Clone succeeds for this death, cancel this spell’s rising even if old remains still exist; do not create a simultaneous living original and newly animated old body from this event. Otherwise require connected usable actual body/anatomy and unclaimed matter. Missing/destroyed/disintegrated/already allocated body blocks rising without rewinding death or selecting another corpse. Unknown physical premises hold the rising branch. The local adaptation permits actual Tiny through Large creature bodies rather than importing Create Undead’s Small/Medium Humanoid gate; fixed stats do not guess a creature CR or restore missing parts.

### statistics

```json
{
  "origin": "NEW Flesh-to-Grave local adaptation of exact accepted Companion10 Ghoul comparison; no global Create Undead amendment",
  "size": "actual source body Tiny/Small/Medium/Large; any other or undocumented anatomy branch held",
  "spaceHeightMass": "actual source body envelope and mass; no growth, repaired limbs or relocated anchor",
  "AC": 13,
  "baseHP": 40,
  "scores": {
    "STR": 14,
    "DEX": 14,
    "CON": 12,
    "INT": 6,
    "WIS": 10,
    "CHA": 6
  },
  "walk": 40,
  "climb": 20,
  "anatomyGate": "actual locomotor/striking/climbing parts must support the chosen action",
  "senses": [
    "ordinary sight",
    "ordinary hearing",
    "Darkvision60feet"
  ],
  "saveBonus": "creation snapshot of original caster PB, all six saves",
  "checks": "ordinary profile ability modifier unless actual independent proficiency source",
  "attack": {
    "count": 1,
    "reachFeet": 5,
    "bonus": "creation snapshot original caster spell attack",
    "dice": "2d6",
    "type": "slashing",
    "additiveModifier": 0,
    "magicalPhysicalAttack": false
  },
  "slow": {
    "trigger": "positive resolved damage packet from this physical hit, including temporaryHP loss; not a zero-damage hit",
    "save": "CON versus creation snapshot original caster spell DC",
    "failure": "Speed−10 until target next future regular END (exclude already resolving END); outside initiative6seconds",
    "stacking": "strongest compatible slow, never additive same rider",
    "magical": true,
    "spell": false
  },
  "CR": null,
  "resistances": [],
  "immunities": [],
  "classResources": {},
  "control": null
}
```

### statisticsJustification

NEW choose only the accepted Ghoul comparison’s fixed40HP/13AC/six scores/movement/attack/rider, never the strongest four-profile result. NEW snapshot original caster attack/DC/PB at creation instead of that comparison’s continuing caster-stat dependency, so permanent independent body needs no dead creator lookup. Copy exact numbers into the new actor. Original person remains dead; memories, personality, classes, magical training, resources, ownership and soul are not transferred. Unrated mechanical Undead is not a cosmological soul assertion.

### agency

NEW no automatic caster control, loyalty, hostility, work order, wages or companion command allowance. Independent actor has no turn in creation round; first independent opportunity is the next numbered round at a fixed virtual slot immediately after the original caster’s captured regular slot, then once each numbered round, regardless of creator initiative change/death. It receives ordinary Action/movement/Bonus Action/Reaction only when a source grants usable actions; no Extra Attack or special reaction. Actual goals/content/needs must be supplied before campaign use, otherwise the agency-dependent branch is held. Explicit fixture goal is test input, not granted by the spell.

### persistence

Physical conversion is permanent and survives original caster loss, ordinary antimagic and link dispel. Only the slow rider is magical/nonspell and suppressible; generic spell-only dispel does not erase the physical body or a nonspell rider. Completed0structuralHP destroys the HP-only animation and leaves consumed unusable-for-new-animation remains and real gear; no Wounds/death-save or ordinary living healing engine unless another exact source grants it. No new corpse, XP, resource, harvest or resurrection-target farm follows. Actual applicable physical damage/healing/repair/needs require sources; Undead does not imply no food/air/water/sleep.

### nullAndReturn

NEW explicitly extend the named animation NullDisabled rule: a qualifying damage-root Nonlethal effect on this HP-only animation leaves it inert at0, not destroyed; identity-specific disabling and recovery require the actual Null source. No generic nondamage prevention follows. Future attacks use the animation as damage owner; original caster Null is not inherited. Later true resurrection is governed by its exact identity/body requirements and current claims; no body can be allocated twice. This spell gives no new personal soul binding, compelled service, CR-based command access or cosmology.

## Perfect Form

Procedure identity: perfect-form. Canonical native status remains blocked-pending-operational-review; proposed procedure is separate.

### Native source and access (unchanged)

```json
{
  "id": "perfect-form",
  "name": "Perfect Form",
  "schools": [
    "Transmutation"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Transmutation",
      "baseRpCost": 21
    },
    "Mage": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Transmutation",
      "baseRpCost": 21
    },
    "Wizard": {
      "rank": 8,
      "minimumClassLevel": 15,
      "school": "Transmutation",
      "baseRpCost": 21
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "perfect-form",
    "original": {
      "name": "Perfect Form",
      "level": 8,
      "resonanceRank": 8,
      "school": "Transmutation",
      "schools": [
        "Transmutation"
      ],
      "placements": [
        {
          "name": "Perfect Form",
          "school": "Transmutation",
          "level": 8,
          "summary": "Ally gains +4 to all physical stats and ignores exhaustion effects for 1 min."
        }
      ],
      "classLevels": {
        "Druid": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classRanks": {
        "Druid": 8,
        "Mage": 8,
        "Wizard": 8
      },
      "classLearnLevels": {
        "Druid": 15,
        "Mage": 15,
        "Wizard": 15
      },
      "classSchools": {
        "Druid": "Transmutation",
        "Mage": "Transmutation",
        "Wizard": "Transmutation"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Ally gains +4 to all physical stats and ignores exhaustion effects for 1 min.",
      "alternateSummaries": [],
      "classes": [
        "Druid",
        "Mage",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 811,
        "original": {
          "school": "Transmutation",
          "level": 8,
          "name": "Perfect Form",
          "effect": "Ally gains +4 to all physical stats and ignores exhaustion effects for 1 min.",
          "source_paragraph": 9985,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 21
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Core resolution requires an explicit operational interpretation",
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

### scope

NEW spell-local operational authorship only. Native source envelopes are immutable; they still say blocked-pending-operational-review and operational=null. The isolated proposal is not installed in the live catalog. Exact accepted interfaces are reproduced in ORIGINAL_SOURCE_RECORDS.json; no later backing-file changes become accepted merely by presence.

### access

Use the native classAccess rows exactly, actual class level, actual known/book/prepared entry, class prerequisites and available rank. Rank8 costs21RP before actual source-specific adjustments; no Overcast, invented acquisition, global discounts, slots or imported costly components. V/S/F, ordinary Action, one perceived target or declared target set within120ft and unobstructed line of effect at commitment and application. A focus is an actual accessible item; no material cost is added. Missing access or known physical illegality prevents commitment. Hidden disqualification after a lawful commitment spends the cast without an oracle or substitute target.

### commitment

Resolve actual current defenses, legal ability to act, anatomy/components and perception before committing. Spend Action and actual21RP; record exact family, base strain, Refrain, Dissonance and any source-specific hooks. Wizard first prepared family in encounter has0 base strain; rank8 repeated family uses base2 plus actual Refrain. Other ordinary classes use rank8 base2 plus Refrain. Read Dissonance before casting: limit=max(4,2+PB+max(0,casting modifier)); ranked surcharge at limit/limit+3/limit+6 is+1/+2/+3RP, and ordinary rank1+ casting is blocked at limit+6 absent an actual expressly granted traumatic exception. Refrain for consecutive same-name casts is+1/+2/+3 capped3; a different name resets it to0, idle/weapon turns do not. Track all actual threshold consequences if reached. Nondamaging Life/Form spells are not damaging Mage Focus casts: clear Nuke Chain; no Surge damage or chain award. Animal Shapes is not Druid Shapeshift and clears no Refrain or reserves.

### timing

Use elapsed seconds plus original regular-slot marker and phase. Absolute expiry at phase0 wins before new events at that timestamp. Complete an already resolving packet under its actual source ordering; no extra turns tick clocks. Ready uses its own actual Action commitment, components,21RP/strain and concentration hold, then one eligible Reaction release before its deadline; it gives no free cast or renewed duration. Ready selects the legal target set/area and any required body/form/anchor choices at release, not at preparation, as the accepted Ready exception. Revalidate every prerequisite and all-outcome fit before spending the release Reaction; invalid/declined occurrence may await another valid trigger until next regular own-turn START, with setup cost retained. Counterspell is at preparation only. Effect duration/maturity starts at successful release/application, not preparation. For Animal Shapes a concentration hold becomes the shared effect on successful release; loss/failure does not restore prior concentration. Other effects end the Ready hold after resolution.

### defenses

Use actual acquired Counterspell, reflection, immunity, antimagic, dispel and concentration records within exact scope, not spell names or guessed ranks. All four are rank8 for applicable checks. A class Wizard Dispel is rank3 at its printed3RP/check10+target rank; it is never Greater Dispel rank5. Source-specific counter success is necessary; a suppressed effect is not terminated unless its source says so. New Animal concentration ends old same-caster concentration at commitment, before counter/save/failure. Nonconcentration Clone/Flesh/Perfect do not end other concentration unless Ready does.

### returnsAndOwnership

Preserve actors, real body and item IDs, personal HP/max ledger, temporaryHP, Wounds/injuries, actual conditions, paid resources, spent turn markers, debts, death and return histories. Do not infer ownership, loyalty, soul geography, CR, content permission, creature roster or preparation from a title. Actual death ends concentration and only the effects whose sources end on death; completed memory losses and other persistent personal consequences are retained. Every fixture is synthetic data for a static rule trace, not an acquired campaign character or physical-world proof.

### holds

Source/access/content/form/body geometry/identity topology/runtime/human-play/balance/release holds survive this return. A missing prerequisite holds the whole dependent case or branch; it cannot be narrated as a positive actual campaign result. All changed rules below are NEW only for these four spells.

### eligibilityAndDuration

NEW one actually allied living physical creature, including self, within120ft/LoE for60elapsedseconds, nonconcentration. Amend recommended P01’s added willingness requirement: the printed native card says Ally, not willing. No additional consent or save gate is imposed, so an actual unconscious ally can receive this benign benefit; this does not imply unconscious consent for another spell or force allegiance. Already dead target gains no revival. Core Instantaneous remains verbatim as a source conflict; printed minute governs the authored continuing effect.

### scores

NEW physical stats means STR,DEX,CON scores each+4, not+4 modifiers/rolls. Apply actual score-setting layers then this compatible bonus according to actual sources. Same-spell component bonus is at most+4 per ability, irrespective of multiple records; strongest same-name wins while every record keeps independent duration/suppression. No advancement20cap is silently imported; an actual explicit absolute cap retains its own scope. Floor((score−10)/2) is the resulting ordinary modifier. No changes to INT,WIS,CHA, proficiency, classes or armor permissions.

### capacity

NEW this spell specifically authorizes its temporary CON component to recompute attained-level baseHP: sum(max(1,stored level base result + current authorized HP-CON modifier)) across actual attained levels, including the actual first-level Hit Die maximum. Do not use level×2 when per-level floors bind. Other temporary CON sources do not receive this authorization. Combine actual independently authorized permanent/temporary HP-CON layers, then add compatible max bonuses, subtract strongest actual max trauma, floor subtotal to1, multiply exact systemic rational factors together and floor once/min1. Exhaustion4 factor1/2 is omitted only while mask active; expedition4+factor3/4 remains. Capacity rise gives no healing; decrease clamps normalHP only, no damage/Wound/fall/proc/death-save event; tempHP unchanged. Recompute ordinary STR melee attack/damage and checks, DEX attack/check/save and actual AC formula, CON saves/checks, and actual carrying/movement from current anatomy; do not substitute recipient modifiers for an Animal Shapes attack that explicitly uses its caster. Unarmored AC10+DEX changes by the actual modifier delta; worn armor caps and finite-form max(ordinary AC,profile AC) remain exact. BODY pounds capacity Tiny STR*7.5, Small/Medium STR*15, Large STR*30; Load Tiny STR/2, Small max(0,STR−2), Medium STR, Large2STR. No extra attack, proficiency or action arises.

### mask

NEW active Exhaustion component masks every effect of the actual six-level Exhaustion track, including half maximumHP, Speed0 and lethal6 endpoint. Retain levels, provenance, every unprevented gain and all costs/recovery prerequisites; this is not level-gain immunity. Only Exhaustion-derived disadvantage/Speed/max/collapse/Unconscious is removed; independent zeroHP unconsciousness, restraints, expedition/serum/Revelation strain and other source penalties remain. Never revive a creature already dead.

### lethalLifecycle

Store protectedStaticEndpoint from an actual earlier lawful death-prevention/return and a separate pendingFreshEndpoint. Gaining6 or a new positive unprevented gain while already6 during masking records a single pendingFreshEndpoint; no death resolves while masked. At last mask loss at6, if pendingFreshEndpoint or no protectedStaticEndpoint, open exactly one fresh would-die event and offer actual finite protection; if prevented, clear pending and install protected collapse at6. If protectedStaticEndpoint and no new gain, merely restore protected collapse alive/Unconscious, never re-kill through HP recomputation. An existing protected collapse may be temporarily masked at positiveHP, but independent Unconscious remains. Actual recovery below6 clears obsolete pending/protected endpoint, not an old past death. Overlapping active masks prevent premature endpoint evaluation. Simultaneous mask expiry is one effective transition, not several deaths.

### componentOrder

NEW each source has STR/DEX/CON and Exhaustion components separately active/suppressed/ended. At actual change: expire due records phase0; arbitrate active components; compute actual scores and authorized baseHP; apply present rational maximum factors; clamp normalHP; then process actual source-specific collapse/lethal transition. A maxHP helper itself never kills. Partial CON suppression may clamp without mask loss, and mask suppression may reinstate Exhaustion while scores stay+4. No prior attack/save replay, RP refund or deadline pause. Death ends this living-recipient effect; later return cannot restore it from a body snapshot.

### recovery

Ordinary qualifying8hour long rest can remove1Exhaustion only with actual food/water, inactive cause, legal care and once-per24hour gate; masking grants none of these. An unconscious protected collapsed creature may complete actual qualifying care/rest under later healing/death. A60second cast does not manufacture8hours or remove levels. Real work/travel gains remain, and mask loss is evaluated from present levels, not original levels.

### formInteraction

Same-identity transformations preserve real scores/HP ledger; this bonus applies only if target still living and actual compatible sources permit it, no second form HP pool or flesh repair. It never changes Beast/Undead taxonomy, gear compatibility, existing injury or the actual caster-stat owner of Animal Shapes attacks.

## Every conference disposition

### LF8-Q01

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

{"scope": "NEW spell-local operational authorship only. Native source envelopes are immutable; they still say blocked-pending-operational-review and operational=null. The isolated proposal is not installed in the live catalog. Exact accepted interfaces are reproduced in ORIGINAL_SOURCE_RECORDS.json; no later backing-file changes become accepted merely by presence.", "access": "Use the native classAccess rows exactly, actual class level, actual known/book/prepared entry, class prerequisites and available rank. Rank8 costs21RP before actual source-specific adjustments; no Overcast, invented acquisition, global discounts, slots or imported costly components. V/S/F, ordinary Action, one perceived target or declared target set within120ft and unobstructed line of effect at commitment and application. A focus is an actual accessible item; no material cost is added. Missing access or known physical illegality prevents commitment. Hidden disqualification after a lawful commitment spends the cast without an oracle or substitute target.", "commitment": "Resolve actual current defenses, legal ability to act, anatomy/components and perception before committing. Spend Action and actual21RP; record exact family, base strain, Refrain, Dissonance and any source-specific hooks. Wizard first prepared family in encounter has0 base strain; rank8 repeated family uses base2 plus actual Refrain. Other ordinary classes use rank8 base2 plus Refrain. Read Dissonance before casting: limit=max(4,2+PB+max(0,casting modifier)); ranked surcharge at limit/limit+3/limit+6 is+1/+2/+3RP, and ordinary rank1+ casting is blocked at limit+6 absent an actual expressly granted traumatic exception. Refrain for consecutive same-name casts is+1/+2/+3 capped3; a different name resets it to0, idle/weapon turns do not. Track all actual threshold consequences if reached. Nondamaging Life/Form spells are not damaging Mage Focus casts: clear Nuke Chain; no Surge damage or chain award. Animal Shapes is not Druid Shapeshift and clears no Refrain or reserves.", "timing": "Use elapsed seconds plus original regular-slot marker and phase. Absolute expiry at phase0 wins before new events at that timestamp. Complete an already resolving packet under its actual source ordering; no extra turns tick clocks. Ready uses its own actual Action commitment, components,21RP/strain and concentration hold, then one eligible Reaction release before its deadline; it gives no free cast or renewed duration. Ready selects the legal target set/area and any required body/form/anchor choices at release, not at preparation, as the accepted Ready exception. Revalidate every prerequisite and all-outcome fit before spending the release Reaction; invalid/declined occurrence may await another valid trigger until next regular own-turn START, with setup cost retained. Counterspell is at preparation only. Effect duration/maturity starts at successful release/application, not preparation. For Animal Shapes a concentration hold becomes the shared effect on successful release; loss/failure does not restore prior concentration. Other effects end the Ready hold after resolution.", "defenses": "Use actual acquired Counterspell, reflection, immunity, antimagic, dispel and concentration records within exact scope, not spell names or guessed ranks. All four are rank8 for applicable checks. A class Wizard Dispel is rank3 at its printed3RP/check10+target rank; it is never Greater Dispel rank5. Source-specific counter success is necessary; a suppressed effect is not terminated unless its source says so. New Animal concentration ends old same-caster concentration at commitment, before counter/save/failure. Nonconcentration Clone/Flesh/Perfect do not end other concentration unless Ready does.", "returnsAndOwnership": "Preserve actors, real body and item IDs, personal HP/max ledger, temporaryHP, Wounds/injuries, actual conditions, paid resources, spent turn markers, debts, death and return histories. Do not infer ownership, loyalty, soul geography, CR, content permission, creature roster or preparation from a title. Actual death ends concentration and only the effects whose sources end on death; completed memory losses and other persistent personal consequences are retained. Every fixture is synthetic data for a static rule trace, not an acquired campaign character or physical-world proof.", "holds": "Source/access/content/form/body geometry/identity topology/runtime/human-play/balance/release holds survive this return. A missing prerequisite holds the whole dependent case or branch; it cannot be narrated as a positive actual campaign result. All changed rules below are NEW only for these four spells."}

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-Q01.

### LF8-A01

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW for an ordinary cast select1–10 distinct willing perceived physical creature-origin recipients and one of the seven complete animal mappings per recipient before commitment. The common accepted Ready exception instead selects this set at release after paid preparation; fit is then checked before the release Reaction. No mass opt-in later, arbitrary bestiary, CR filtering, hidden target replacement or switching forms during the effect. Form names denote actual chosen spell-local beast anatomy, not a change of origin taxonomy. Object-origin transformed objects, summon bodies with incompatible lifecycle, unknown anatomy/mass and undocumented origin require their own established source; otherwise that dependent branch is held. Actual willing withdrawal before resolution makes only that recipient fail, with cost retained.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-A01.

### LF8-A02

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

[{"animal": "wolf", "profile": "Predator", "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion", "size": "Medium", "horizontalFeet": [5, 5], "requiredHeightFeet": 4, "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.", "baseBodyMass": "unchanged actual origin pounds", "walk": 40, "fly": 0, "swim": 0, "burrowLooseSoil": 0, "hover": false, "AC": "max(actual compatible ordinary AC,13)", "hands": false, "speech": false, "senses": ["ordinary sight", "ordinary hearing"], "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.", "attack": {"countPerAttackAction": 1, "reachFeet": 5, "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses", "damageDice": "1d8", "damageModifier": "max(1,current original caster casting ability modifier)", "type": "slashing", "magicalByDefault": false, "damageOwner": "subject"}}, {"animal": "brown bear", "profile": "Brute", "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion", "size": "Large", "horizontalFeet": [10, 10], "requiredHeightFeet": 8, "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.", "baseBodyMass": "unchanged actual origin pounds", "walk": 30, "fly": 0, "swim": 0, "burrowLooseSoil": 0, "hover": false, "AC": "max(actual compatible ordinary AC,15)", "hands": false, "speech": false, "senses": ["ordinary sight", "ordinary hearing"], "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.", "attack": {"countPerAttackAction": 1, "reachFeet": 5, "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses", "damageDice": "2d6", "damageModifier": "max(1,current original caster casting ability modifier)", "type": "bludgeoning", "magicalByDefault": false, "damageOwner": "subject"}}, {"animal": "hawk", "profile": "Avian", "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion", "size": "Small", "horizontalFeet": [5, 5], "requiredHeightFeet": 3, "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.", "baseBodyMass": "unchanged actual origin pounds", "walk": 10, "fly": 50, "swim": 0, "burrowLooseSoil": 0, "hover": false, "AC": "max(actual compatible ordinary AC,13)", "hands": false, "speech": false, "senses": ["ordinary sight", "ordinary hearing"], "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.", "attack": {"countPerAttackAction": 1, "reachFeet": 5, "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses", "damageDice": "1d6", "damageModifier": "max(1,current original caster casting ability modifier)", "type": "slashing", "magicalByDefault": false, "damageOwner": "subject"}}, {"animal": "dolphin", "profile": "Aquatic", "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion", "size": "Medium", "horizontalFeet": [5, 5], "requiredHeightFeet": 3, "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.", "baseBodyMass": "unchanged actual origin pounds", "walk": 20, "fly": 0, "swim": 50, "burrowLooseSoil": 0, "hover": false, "AC": "max(actual compatible ordinary AC,14)", "hands": false, "speech": false, "senses": ["ordinary sight", "ordinary hearing"], "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.", "attack": {"countPerAttackAction": 1, "reachFeet": 5, "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses", "damageDice": "1d8", "damageModifier": "max(1,current original caster casting ability modifier)", "type": "piercing", "magicalByDefault": false, "damageOwner": "subject"}}, {"animal": "badger", "profile": "Burrower", "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion", "size": "Medium", "horizontalFeet": [5, 5], "requiredHeightFeet": 3, "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.", "baseBodyMass": "unchanged actual origin pounds", "walk": 30, "fly": 0, "swim": 0, "burrowLooseSoil": 15, "hover": false, "AC": "max(actual compatible ordinary AC,14)", "hands": false, "speech": false, "senses": ["ordinary sight", "ordinary hearing"], "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.", "attack": {"countPerAttackAction": 1, "reachFeet": 5, "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses", "damageDice": "1d8", "damageModifier": "max(1,current original caster casting ability modifier)", "type": "bludgeoning", "magicalByDefault": false, "damageOwner": "subject"}}, {"animal": "elephant", "profile": "Greater brute", "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion", "size": "Large", "horizontalFeet": [10, 10], "requiredHeightFeet": 10, "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.", "baseBodyMass": "unchanged actual origin pounds", "walk": 40, "fly": 0, "swim": 0, "burrowLooseSoil": 0, "hover": false, "AC": "max(actual compatible ordinary AC,17)", "hands": false, "speech": false, "senses": ["ordinary sight", "ordinary hearing"], "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.", "attack": {"countPerAttackAction": 1, "reachFeet": 5, "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses", "damageDice": "2d8", "damageModifier": "max(1,current original caster casting ability modifier)", "type": "bludgeoning", "magicalByDefault": false, "damageOwner": "subject"}}, {"animal": "giant condor", "profile": "Greater winged", "authorship": "NEW finite spell-local beast-shaped anatomy mapping; no monster, Beast taxonomy or CR assertion", "size": "Large", "horizontalFeet": [10, 10], "requiredHeightFeet": 8, "stance": "Authored occupied envelope includes limbs and extended wings; no smaller squeezed pose is assumed. Use BODY legal squeeze only if actual geometry proves it.", "baseBodyMass": "unchanged actual origin pounds", "walk": 20, "fly": 60, "swim": 0, "burrowLooseSoil": 0, "hover": false, "AC": "max(actual compatible ordinary AC,16)", "hands": false, "speech": false, "senses": ["ordinary sight", "ordinary hearing"], "breathing": "Adds water breathing for dolphin; retains actual original air-breathing needs otherwise. No no-air/food/sleep immunity.", "attack": {"countPerAttackAction": 1, "reachFeet": 5, "attackBonus": "current original caster PB + casting ability modifier plus actual applicable source bonuses", "damageDice": "2d8", "damageModifier": "max(1,current original caster casting ability modifier)", "type": "slashing", "magicalByDefault": false, "damageOwner": "subject"}}]

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-A02.

### LF8-A03

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW one shared rank8 concentration record expires exactly60elapsedseconds after successful application; individual target links may end separately. Caster concentration loss/death ends all links; ending the final target link ends this now-empty shared concentration. Range120 is acquisition/application only, not a maintained tether. No extra body, turn, HP pool, concentration slot or form-switch Action is granted.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-A03.

### LF8-A04

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW explicitly reuse accepted creature transformation conservation. Scores, PB, HP/max/tempHP, class resources, Wounds, injuries, identity, species/ancestry, conditions and initiative remain real. Only listed anatomy/movement/AC/natural attack changes. Base body weight unchanged even across sizes; actual cargo still weighs including melded items; BODY carry/load and actual anatomy restrictions apply. Earliest root carried gear becomes melded, inaccessible, custody unchanged; incompatible armor/features cease expression. Existing external cargo stays external. Successful legal replacement closes previous anatomy atomically and recaptures actual extant gear once, never restores consumed items, charges or healing. No displaced form stack. Druid class Shapeshift cannot enter while a spell-form record remains, including suppressed.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-A04.

### LF8-A05

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW use current original caster attack bonus/M for the mapped natural attack; original caster statistics must be actually resolvable. Subject is the attacker/damage owner for Null, kill credit and reactions; no caster cast-proc on a natural attack. One attack per ordinary Attack Action, reach5, listed dice+M; no Multiattack, spells, magic attacks, class beast benefits or senses beyond mapped/existing compatible source. Missing caster-stat provenance holds the attack branch; other links do not disappear.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-A05.

### LF8-C01

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW one willing living physical creature-origin identity with a documented reproducible persistent root body. Perceive the source within120ft/LoE and designate a legal unoccupied growth envelope adjacent to it and also within120ft/LoE, same established plane. No printed vessel, blood sample, gem or extra price is added. Physical Constructs are not automatically excluded if actually living/reproducible by their own source; HP-only animations, transformed objects and temporary summoned bodies gain no Clone eligibility by appearance. Unknown reproduction/physiology holds the whole dependent branch. Validate the entire root body envelope, mass and missing parts, excluding temporary form anatomy and gear.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-C01.

### LF8-C02

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW dormant replacement body uses object-like structural AC10 and20structuralHP, no resistance, immunity, regeneration or separate personal HP pool. At structural0 it is destroyed and its entitlement ends. The intact viable-return gate requires structuralHP20 and no new anatomy/storage damage; partial damage blocks return until actual applicable repair restores structural20 and anatomy. Structural repair never heals the source character. Dormancy supplies only no metabolic air/food/water consumption while uninhabited, an explicit Clone-local completion; temperature, fire, pressure, decay, crushing and physical movement use actual applicable sources. No implicit safe vessel, preservation against environmental harm or free moving body. Repeated paid casts can leave multiple inert physical bodies; the finite cap is one live entitlement, not a world population limit. Missing hazard/storage content holds the affected branch. Detached matter or replaced bodies do not acquire autonomous life, XP, harvest awards or new spell fuel by this procedure.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-C02.

### LF8-C03

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW at most one live insurance entitlement per source identity across all casters. Only successful valid new establishment replaces the old link, not its physical body. Failed/blocked/countered attempt leaves the older link. Store unique entitlementId, bodyId, sourceIdentity, creator, body snapshot, timestamps, suppression, condition and attempted death IDs. Consumed/replaced bodies have no duplicate entitlement; their physical provenance remains.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-C03.

### LF8-C04

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW actual completed death, after applicable would-die replacements and actual death triggers, opens one immediate optional return attempt. Earlier survival means no death ID and no Clone attempt. Require actual identity dead, actual willingness, mature/intact eligible unclaimed body, unsuppressed/unended link, legal destination and real return permissions. Another already successful return/claim wins; there can be only one living personal identity. Check identity-level barriers such as actual Soul Bind globally by their exact scope. Clone uses the stored body as its local return anchor: corpse-local Mass Resurrection Denial at the old corpse alone does not block a different stored anchor outside it; a matching actual barrier at the stored body does. Old corpse remains is not the paid return body. Cross-plane routing and unknown soul/topology facts are held, not granted by range120.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-C04.

### LF8-C05

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

Return relocates the one personal identity into the actual clone body; physical old remains and their actual gear persist at their old positions but all other remains lose duplicate-return eligibility. No cloned gear, RP, spellbook, slots, daily uses, Wounds, injuries, exhaustion, debt or memory reset. Present personal scores/progression and HP ledger apply, not the creation snapshot. Concentration ended on death stays ended. Current personal injuries remain functional restrictions on the stored body; an older intact limb is not permission to cure a current missing-limb injury. Actual clone damage imposes its own restrictions too. Unsupported anatomy reconciliation is held; no mass/limb restoration is inferred. Protected Exhaustion6 returns alive and collapsed under later healing/death, not immediately re-killed by maximum recomputation.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-C05.

### LF8-C06

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW resolve one atomic claim of the eligible body and identity, consume entitlement once, retire the dormant structuralHP pool (retain its historical damage record but it is no longer an active pool), then assign life1normalHP with present lawful maximum and protected lethal-track handling from the later healing/death closure. No HP-healing multiplier or living cannot-regain-HP effect converts this life assignment to healing or0HP. Actual life/identity barrier prevents claim before assignment. Record this death ID attempted even on decline/immaturity/suppression/occupation/barrier failure; no queued resurrection, delayed eligibility, repeat or replay. An intact unconsumed link may remain for a later genuinely distinct death after an actual intervening return, not continued retry of this death. Destroyed/replaced/ended links cannot.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-C06.

### LF8-F01

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW one perceived living physical creature within120ft/LoE. Actual current normalHP must be strictly<100 at application; temporaryHP never enters the threshold. Living dying0 qualifies; already dead/nonliving HP-only animation does not. This is an explicit living target completion, not an inferred universal Necromancy immunity. Known impossible target rejects before pay; hidden100+, hidden nonliving identity or changed eligibility spends a lawful commitment without numeric disclosure, no retarget. Eligible target makes one binary CON save against actual caster DC; success prevents both death and rising.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-F01.

### LF8-F02

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

On failure and after actual applicable defenses, resolve a nondamage would-die event. No necrotic damage, damage root, Wound save, zero-HP damage threshold or death-save failure is fabricated. TemporaryHP, resistances, caster Null Veil damage nonlethality and ordinary Death Ward positive-to-zero floor do not themselves prevent this event. A real applicable would-die replacement (e.g. actually acquired Cleric16 Ritual of Undeath Ward, already paid and active) can prevent death; then no rising. Finish actual death and its sourced triggers/claims before attempting body allocation.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-F02.

### LF8-F03

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW choose only the accepted Ghoul comparison’s fixed40HP/13AC/six scores/movement/attack/rider, never the strongest four-profile result. NEW snapshot original caster attack/DC/PB at creation instead of that comparison’s continuing caster-stat dependency, so permanent independent body needs no dead creator lookup. Copy exact numbers into the new actor. Original person remains dead; memories, personality, classes, magical training, resources, ownership and soul are not transferred. Unrated mechanical Undead is not a cosmological soul assertion.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-F03.

### LF8-F04

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW physical Ghoul-derived animation, explicitly not a same-person undead resurrection. Only this spell’s actual completed death can supply its same usable body. If a prior actual death-trigger return such as Clone succeeds for this death, cancel this spell’s rising even if old remains still exist; do not create a simultaneous living original and newly animated old body from this event. Otherwise require connected usable actual body/anatomy and unclaimed matter. Missing/destroyed/disintegrated/already allocated body blocks rising without rewinding death or selecting another corpse. Unknown physical premises hold the rising branch. The local adaptation permits actual Tiny through Large creature bodies rather than importing Create Undead’s Small/Medium Humanoid gate; fixed stats do not guess a creature CR or restore missing parts.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-F04.

### LF8-F05

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

Physical conversion is permanent and survives original caster loss, ordinary antimagic and link dispel. Only the slow rider is magical/nonspell and suppressible; generic spell-only dispel does not erase the physical body or a nonspell rider. Completed0structuralHP destroys the HP-only animation and leaves consumed unusable-for-new-animation remains and real gear; no Wounds/death-save or ordinary living healing engine unless another exact source grants it. No new corpse, XP, resource, harvest or resurrection-target farm follows. Actual applicable physical damage/healing/repair/needs require sources; Undead does not imply no food/air/water/sleep.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-F05.

### LF8-P01

Option1 amended explicitly: preserve native Ally, do not add willingness; apply STR/DEX/CON scores+4 and nonconcentration60seconds.

NEW one actually allied living physical creature, including self, within120ft/LoE for60elapsedseconds, nonconcentration. Amend recommended P01’s added willingness requirement: the printed native card says Ally, not willing. No additional consent or save gate is imposed, so an actual unconscious ally can receive this benign benefit; this does not imply unconscious consent for another spell or force allegiance. Already dead target gains no revival. Core Instantaneous remains verbatim as a source conflict; printed minute governs the authored continuing effect.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-P01.

### LF8-P02

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW this spell specifically authorizes its temporary CON component to recompute attained-level baseHP: sum(max(1,stored level base result + current authorized HP-CON modifier)) across actual attained levels, including the actual first-level Hit Die maximum. Do not use level×2 when per-level floors bind. Other temporary CON sources do not receive this authorization. Combine actual independently authorized permanent/temporary HP-CON layers, then add compatible max bonuses, subtract strongest actual max trauma, floor subtotal to1, multiply exact systemic rational factors together and floor once/min1. Exhaustion4 factor1/2 is omitted only while mask active; expedition4+factor3/4 remains. Capacity rise gives no healing; decrease clamps normalHP only, no damage/Wound/fall/proc/death-save event; tempHP unchanged. Recompute ordinary STR melee attack/damage and checks, DEX attack/check/save and actual AC formula, CON saves/checks, and actual carrying/movement from current anatomy; do not substitute recipient modifiers for an Animal Shapes attack that explicitly uses its caster. Unarmored AC10+DEX changes by the actual modifier delta; worn armor caps and finite-form max(ordinary AC,profile AC) remain exact. BODY pounds capacity Tiny STR*7.5, Small/Medium STR*15, Large STR*30; Load Tiny STR/2, Small max(0,STR−2), Medium STR, Large2STR. No extra attack, proficiency or action arises.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-P02.

### LF8-P03

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

Store protectedStaticEndpoint from an actual earlier lawful death-prevention/return and a separate pendingFreshEndpoint. Gaining6 or a new positive unprevented gain while already6 during masking records a single pendingFreshEndpoint; no death resolves while masked. At last mask loss at6, if pendingFreshEndpoint or no protectedStaticEndpoint, open exactly one fresh would-die event and offer actual finite protection; if prevented, clear pending and install protected collapse at6. If protectedStaticEndpoint and no new gain, merely restore protected collapse alive/Unconscious, never re-kill through HP recomputation. An existing protected collapse may be temporarily masked at positiveHP, but independent Unconscious remains. Actual recovery below6 clears obsolete pending/protected endpoint, not an old past death. Overlapping active masks prevent premature endpoint evaluation. Simultaneous mask expiry is one effective transition, not several deaths.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-P03.

### LF8-P04

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW active Exhaustion component masks every effect of the actual six-level Exhaustion track, including half maximumHP, Speed0 and lethal6 endpoint. Retain levels, provenance, every unprevented gain and all costs/recovery prerequisites; this is not level-gain immunity. Only Exhaustion-derived disadvantage/Speed/max/collapse/Unconscious is removed; independent zeroHP unconsciousness, restraints, expedition/serum/Revelation strain and other source penalties remain. Never revive a creature already dead.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-P04.

### LF8-P05

Option1 selected as explicit NEW spell-local authorship or exact-source reuse, with the full linked procedure qualifications.

NEW each source has STR/DEX/CON and Exhaustion components separately active/suppressed/ended. At actual change: expire due records phase0; arbitrate active components; compute actual scores and authorized baseHP; apply present rational maximum factors; clamp normalHP; then process actual source-specific collapse/lethal transition. A maxHP helper itself never kills. Partial CON suppression may clamp without mask loss, and mask suppression may reinstate Exhaustion while scores stay+4. No prior attack/save replay, RP refund or deadline pause. Death ends this living-recipient effect; later return cannot restore it from a body snapshot.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-P05.

### LF8-X01

Option1 corrected to live709 index: Companion10, BodyDefense, VitalityMatter10, Resource6 and MemoryControl4 already applied. Preserve exact recorded accepted comparison scope, no re-opening or importing later edits.

NEW spell-local operational authorship only. Native source envelopes are immutable; they still say blocked-pending-operational-review and operational=null. The isolated proposal is not installed in the live catalog. Exact accepted interfaces are reproduced in ORIGINAL_SOURCE_RECORDS.json; no later backing-file changes become accepted merely by presence.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-X01.

### LF8-X02

Both options: complete deterministic static cases for known authored fixtures, explicit held dependent branches for absent actual premises; never count a held branch as a positive campaign example.

Source/access/content/form/body geometry/identity topology/runtime/human-play/balance/release holds survive this return. A missing prerequisite holds the whole dependent case or branch; it cannot be narrated as a positive actual campaign result. All changed rules below are NEW only for these four spells.

Exact original question/options, case links and the complete hold union: QUESTION_DISPOSITIONS.json, id LF8-X02.

