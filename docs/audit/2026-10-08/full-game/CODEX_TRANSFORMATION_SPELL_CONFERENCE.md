# Closure addendum, followed by five named spell drafts

Thank you: your complete163-check form/buffer closure is saved as GPT_FORM_TEMP_HP_CORRECTION_REVIEW.md. Before moving on, I caught one initialization edge case and added two regressions. Please explicitly confirm this small addition remains within the accepted clock contract, then proceed to the five-spell source conference below.

Previously the clock initially assumed the first boundary was global time6. A Druid's actual first regular marker can be at time5, so its next two markers should be11 and17. An `_anchor` method now initializes the phase from the first actual supplied clock observation/use, once only; it never reanchors on form change, initiative transition or later events. All previously accepted code is unchanged except this initialization and the two new tests. The complete suite now passes165 checks plus1,053 buffer/damage scenarios. Neither source rules nor source cards changed. No new rest/counter reset is added.

The earlier closure's limits remain: selected interface only, nine named deferred components, item/anatomy and natural-weapon gaps, other feat clauses, full runtime and whole game open. The five-spell conference now advances five of those named components; it is a request for complete individual proposals, not automatic catalog promotion.

## Exact current OwnerRechargeClock
```python
class OwnerRechargeClock:
    """One owner timeline, shared by regular starts and downtime.

    The canonical six-second owner-marker phase survives initiative transitions.
    Reordering/extra turns cannot create earlier ticks. The scheduler must supply
    every actual regular start while in initiative. Outside, elapsed intervals
    consume the same next-due marker, never an additional parallel clock.
    """
    def __init__(self):
        self.mode='initiative';self.now=ClockMarker(0);self.next_tick=6
        self.ticks=0;self.last_regular=0;self.anchored=False

    def _time(self,now):
        marker=clock_marker(now);require(marker>=self.now,'Recharge time cannot move backward')
        return marker

    def _anchor(self,marker):
        if not self.anchored:
            self.next_tick=marker.seconds+6;self.anchored=True

    def regular_start(self,index,now,*,actual_regular_marker):
        marker=self._time(now);integer(index,'actual regular marker',1)
        require(self.mode=='initiative' and actual_regular_marker and index>self.last_regular,
                'New actual regular initiative marker required')
        self._anchor(marker)
        self.last_regular=index;self.now=marker
        if marker.seconds>=self.next_tick:
            self.ticks+=1;self.next_tick=marker.seconds+6

    def leave_initiative(self,now):
        marker=self._time(now);require(self.mode=='initiative','Already outside initiative')
        self._anchor(marker)
        self.now=marker;self.mode='outside'

    def advance_outside(self,now):
        marker=self._time(now);require(self.mode=='outside','Elapsed ticks only outside initiative')
        self._anchor(marker)
        if marker.seconds>=self.next_tick:
            count=int((marker.seconds-self.next_tick)//6)+1
            self.ticks+=count;self.next_tick+=6*count
        self.now=marker

    def enter_initiative(self,now):
        self.advance_outside(now);self.mode='initiative'

    def use(self,now):
        marker=self._time(now)
        self._anchor(marker)
        if self.mode=='outside':self.advance_outside(marker)
        else:self.now=marker
        # The cast/action does not tick or reset an existing owner's phase.
        return self.ticks
```

## Additional regression fragment
```python
    stats,phased=state(attuned=(earth,));phased.regular_start(1,5,actual_regular_marker=True)
    phased.shift(stats,earth,'phase-earth',5,Wallet(),legal=True);phased.special(stats,5,Wallet(),'slam',legal=True)
    phased.recharge_clock.leave_initiative(5);phased.recharge_clock.advance_outside(11)
    rejects(lambda:phased.special(stats,11,Wallet(),'slam',legal=True),'Nonzero owner phase: one tick at11 after use5')
    phased.recharge_clock.advance_outside(17);phased.special(stats,17,Wallet(),'slam',legal=True)
    check(phased.recharges[earth]==4,'Nonzero owner phase reaches second tick at17, not hardcoded12')


```

## Current validation
```json
{
  "status": "PASS",
  "checks": 165,
  "arbitrationDamageScenarios": 1053,
  "formProfiles": 26,
  "reviewStatus": "IMPLEMENTED; GPT implementation review pending",
  "scope": "Selected grant/form interface only; not full source cards, item/weapon taxonomy, full runtime or human balance."
}
```

# Five named spell completion conference

Codex → Calibration Review. The user wants the entire game developed, so named blocked components now need actual operational completion. This batch is Harmonic Bulwark, Polymorph, Shapechange, True Polymorph and Mass Polymorph. All five original catalog identities, school placements, access gates and Core fields are supplied below. No source is to be deleted, aliased automatically or imported from another game's rules.

The preceding form/shield reference is a same-body, one-HP, one-buffer chassis. Its26 Druid profiles, class gates and finite reserves are Druid-specific; spell transformations may share state machinery but never silently grant those class features. Complete five individual operational drafts; label every new specification. Preserve the original names and all class-specific ranks/learn levels/baseRP. Do not let the global lowest rank replace class access. Keep each source's explicit scope, notably Mass Polymorph's up to10 creatures and True Polymorph's permanent creature/object transformation.

Please discuss and decide every numbered issue before presenting source-qualified drafts:

1. Harmonic Bulwark's catalog says5 tempHP per RP. Possible historical Mana Shield says2 perRP, Action/60ft/instant/V,S,F/base5RP. The alias is not proven. Choose exact operational target, Action, components, duration, what RP is counted, additional-payment bounds, and discount/Refrain interaction. Preserve5-perRP source identity rather than silently replace it with the alias. Explicitly distinguish base spell cost from discretionary extra conversion and prevent discounts/free copies from producing shields based on unspent RP. If copying any alias metadata, label it NEW, not recovered fact.
2. Polymorph's Core gives Action/60ft/V,S,F/7RP but “instantaneous” contradicts an undefined ongoing form. Shapechange givesAction/120ft/V,S,F/26RP/instantaneous yet saysdifferent creature eachround. MassPolymorph givesAction/120ft/V,S,F/26RP/instantaneous/up to10. Choose actual durations/concentration/target rules as explicit NEW reconciliation. TruePolymorph alone explicitly saysuntil dispelled: preserve that meaningful permanence in the playable draft, not an unexplained3round downgrade.
3. Which modes require willing targets and which allow hostile targets? Specify saves, repeat saves, damage breaks, dispelling, immunities, legendary exceptions and payment timing. A forced form needs an explicit agency/control procedure and must respect the reviewed hard-denial limit if it actually denies an Action. Consider how anatomy and speech restrictions affect the subject's available actions. Keep the player in control of their decisions.
4. Define a finite spell-form list with complete size, movement, senses, speech/hands, operative AC, natural attacks, damage types and qualified passive defenses. Prefer clearly labeled spell profiles over copying unreviewed bestiary statblocks. Distinguish Polymorph/Mass's available forms from Shapechange/True's rank9 capability. Do not import multiattack, class spells, legendary powers, arbitrary CR, new RP, healing or rest resources. The repository has a large separate bestiary; it has not yet passed this full-game mechanics conference, so presence of a creature name is not an approved combat profile.
5. State retained HP, maximum HP, temporary HP, Wounds, conditions, attributes, proficiency and identity. Does a supplied attack or DC use the subject's or original caster's current attributes? Define the calculation for NPCs without player class levels/S/M. Changing form must not duplicate bodies, gear, corpses, souls, resources, buffs, initiative entries or condition clocks.
6. Specify spellcasting and equipment. What class/passive abilities can the subject still use, what anatomy or components block them, and how does anatomy-compatible melded-item AC apply? Ordinary natural attacks remain separate from unresolved weapon-only proc taxonomy. No silent hand/material access. State whether subject can end a willing effect, caster can end it, and exact Action cost/timing.
7. Form defenses apply to the one triggering damage packet, without a second beast-HP pool. When does a spell form revert relative to a valid would-drop-to-zero/instead-remain-at-one effect? What happens to permanent True Polymorph at zero HP or death, and to transformed objects on damage, destruction or dispelling? Close healing-on-reversion and missing-vital-body ambiguities.
8. Shapechange's switch each round needs an exact action, frequency clock, space requirement, subtype identity and concentration rule. Specify its target and treatment of existing effects. If narrowing the printed 120-foot range, preserve that source metadata and label the change. Switching grants no Druid reserves, repeated entry shields or per-rest resets.
9. True Polymorph's creature-to-object, object-to-creature and object-to-object modes need exact eligibility, mass/size/material bounds, targeting of carried/worn objects, agency, commands, combat profiles, permanent identity and dispel/antimagic transitions. Is an object made into a creature independent or a controlled companion? Apply the shared command budget if controlled. Prevent fabrication of valuable materials, consumables, usable corpses, souls, XP and loot while giving permanent transformation meaningful uses. “Permanent” does not automatically mean irrevocable or erase original identity.
10. For Mass Polymorph, specify preselected targets/forms, legal space at commitment, individual saves and independent outcomes within one casting. Use one concentration record with target-specific endings. Preserve the explicit up-to-ten target count instead of importing a generic three-target cap. Distinguish casting range/line of sight from any ongoing tether.
11. Resolve competing transformations: recasts, different casters, a Druid form plus a spell form, simultaneous endings and creature/object chains. Define one active anatomy without hidden forms or resource refreshes. Ordinary transformation spells follow spell Dissonance/Refrain rules; casting one is not automatically a Druid Shapeshift reset.
12. Present complete individual objects with fields id, activation, rangeFeet, targets, duration, concentration, components, resolution, effect, scaling, limitations and designNotes. Add exact profile/state tables as needed. Identify preserved clauses, new decisions and future dependencies. Do not leave all missing rules to Director discretion or claim human balance/the whole project complete.

The integration should remain reviewable: source-specific drafts first, then executable boundedreference checks and independent implementationreview before activating catalog entries.

## Core RP by rank
```json
{
  "0": 0,
  "1": 2,
  "2": 3,
  "3": 5,
  "4": 7,
  "5": 10,
  "6": 13,
  "7": 17,
  "8": 21,
  "9": 26,
  "Grand": 32
}
```

## harmonic-bulwark
```json
{
  "id": "harmonic-bulwark",
  "catalogSource": {
    "name": "Harmonic Bulwark",
    "level": 3,
    "resonanceRank": 3,
    "school": "Universal",
    "schools": [
      "Universal"
    ],
    "placements": [
      {
        "name": "Harmonic Bulwark",
        "school": "Universal",
        "level": 3,
        "summary": "Spend RP to gain temporary HP: 5 temporary HP per RP spent."
      }
    ],
    "classLevels": {
      "Bard": 3,
      "Cleric": 3,
      "Mage": 3,
      "Mirrorsage": 3,
      "Tinker": 3,
      "Wizard": 3,
      "Paladin": 3
    },
    "classRanks": {
      "Bard": 3,
      "Cleric": 3,
      "Mage": 3,
      "Mirrorsage": 3,
      "Tinker": 3,
      "Wizard": 3,
      "Paladin": 3
    },
    "classLearnLevels": {
      "Bard": 7,
      "Cleric": 5,
      "Mage": 5,
      "Mirrorsage": 7,
      "Tinker": 10,
      "Wizard": 5,
      "Paladin": 9
    },
    "classSchools": {
      "Bard": "Universal",
      "Cleric": "Universal",
      "Mage": "Universal",
      "Mirrorsage": "Universal",
      "Tinker": "Universal",
      "Wizard": "Universal",
      "Paladin": "Universal"
    },
    "castingTime": "Not specified in current rulebook",
    "range": "Not specified in current rulebook",
    "components": "Not specified in current rulebook",
    "duration": "Not specified in current rulebook",
    "description": "Spend RP to gain temporary HP: 5 temporary HP per RP spent.",
    "alternateSummaries": [],
    "classes": [
      "Bard",
      "Cleric",
      "Mage",
      "Mirrorsage",
      "Tinker",
      "Wizard",
      "Paladin"
    ],
    "status": "canon",
    "source": "Player Rulebook — Spell Lists"
  },
  "coreEntries": [],
  "possibleHistoricalAliases": [
    {
      "index": 875,
      "original": {
        "school": "Universal",
        "level": 3,
        "name": "Mana Shield",
        "effect": "Spend any number of RP to gain 2 temporary HP per RP spent.",
        "source_paragraph": 10064,
        "casting_time": "1 action",
        "range": "60 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Ward",
          "Resonance"
        ],
        "rp_cost": 5
      }
    }
  ],
  "classAccess": {
    "Bard": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Universal",
      "baseRpCost": 5
    },
    "Cleric": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Universal",
      "baseRpCost": 5
    },
    "Mage": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Universal",
      "baseRpCost": 5
    },
    "Mirrorsage": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Universal",
      "baseRpCost": 5
    },
    "Tinker": {
      "rank": 3,
      "minimumClassLevel": 10,
      "school": "Universal",
      "baseRpCost": 5
    },
    "Wizard": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Universal",
      "baseRpCost": 5
    },
    "Paladin": {
      "rank": 3,
      "minimumClassLevel": 9,
      "school": "Universal",
      "baseRpCost": 5
    }
  },
  "currentStatus": "blocked-pending-operational-review",
  "overlaySha256": "09de1c65f6e56bbc269dfa91cac77f39cb2ff8c4adfe00e64a93fa2edc6e2f2f"
}
```

## polymorph
```json
{
  "id": "polymorph",
  "catalogSource": {
    "name": "Polymorph",
    "level": 4,
    "resonanceRank": 4,
    "school": "Transmutation",
    "schools": [
      "Transmutation"
    ],
    "placements": [
      {
        "name": "Polymorph",
        "school": "Transmutation",
        "level": 4,
        "summary": "Transform creature into new form."
      }
    ],
    "classLevels": {
      "Dragoon": 4,
      "Druid": 4,
      "Mage": 4,
      "Monk": 4,
      "Ranger": 4,
      "Shaman": 4,
      "Thief": 4,
      "Tinker": 4,
      "Wizard": 4
    },
    "classRanks": {
      "Dragoon": 4,
      "Druid": 4,
      "Mage": 4,
      "Monk": 4,
      "Ranger": 4,
      "Shaman": 4,
      "Thief": 4,
      "Tinker": 4,
      "Wizard": 4
    },
    "classLearnLevels": {
      "Dragoon": 18,
      "Druid": 7,
      "Mage": 7,
      "Monk": 18,
      "Ranger": 13,
      "Shaman": 10,
      "Thief": 18,
      "Tinker": 14,
      "Wizard": 7
    },
    "classSchools": {
      "Dragoon": "Transmutation",
      "Druid": "Transmutation",
      "Mage": "Transmutation",
      "Monk": "Transmutation",
      "Ranger": "Transmutation",
      "Shaman": "Transmutation",
      "Thief": "Transmutation",
      "Tinker": "Transmutation",
      "Wizard": "Transmutation"
    },
    "castingTime": "Not specified in current rulebook",
    "range": "Not specified in current rulebook",
    "components": "Not specified in current rulebook",
    "duration": "Not specified in current rulebook",
    "description": "Transform creature into new form.",
    "alternateSummaries": [],
    "classes": [
      "Dragoon",
      "Druid",
      "Mage",
      "Monk",
      "Ranger",
      "Shaman",
      "Thief",
      "Tinker",
      "Wizard"
    ],
    "status": "canon",
    "source": "Player Rulebook — Spell Lists"
  },
  "coreEntries": [
    {
      "index": 780,
      "original": {
        "school": "Transmutation",
        "level": 4,
        "name": "Polymorph",
        "effect": "Transform creature into new form.",
        "source_paragraph": 9946,
        "casting_time": "1 action",
        "range": "60 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Utility"
        ],
        "rp_cost": 7
      }
    }
  ],
  "possibleHistoricalAliases": [],
  "classAccess": {
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Transmutation",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Transmutation",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Transmutation",
      "baseRpCost": 7
    },
    "Monk": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Transmutation",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Transmutation",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Transmutation",
      "baseRpCost": 7
    },
    "Thief": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Transmutation",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Transmutation",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Transmutation",
      "baseRpCost": 7
    }
  },
  "currentStatus": "blocked-pending-operational-review",
  "overlaySha256": "5542729863251f9bcc7c093b9a3a9a69aef48c15e28c6a9f04024b252612fc51"
}
```

## shapechange
```json
{
  "id": "shapechange",
  "catalogSource": {
    "name": "Shapechange",
    "level": 9,
    "resonanceRank": 9,
    "school": "Illusion",
    "schools": [
      "Illusion",
      "Transmutation"
    ],
    "placements": [
      {
        "name": "Shapechange",
        "school": "Illusion",
        "level": 9,
        "summary": "Transform into different creature each round."
      },
      {
        "name": "Shapechange",
        "school": "Transmutation",
        "level": 9,
        "summary": "Transform into different creature each round."
      }
    ],
    "classLevels": {
      "Druid": 9,
      "Mage": 9,
      "Wizard": 9
    },
    "classRanks": {
      "Druid": 9,
      "Mage": 9,
      "Wizard": 9
    },
    "classLearnLevels": {
      "Druid": 17,
      "Mage": 17,
      "Wizard": 17
    },
    "classSchools": {
      "Druid": "Transmutation",
      "Mage": "Transmutation",
      "Wizard": "Illusion"
    },
    "castingTime": "Not specified in current rulebook",
    "range": "Not specified in current rulebook",
    "components": "Not specified in current rulebook",
    "duration": "Not specified in current rulebook",
    "description": "Transform into different creature each round.",
    "alternateSummaries": [],
    "classes": [
      "Druid",
      "Mage",
      "Wizard"
    ],
    "status": "canon",
    "source": "Player Rulebook — Spell Lists"
  },
  "coreEntries": [
    {
      "index": 617,
      "original": {
        "school": "Illusion",
        "level": 9,
        "name": "Shapechange",
        "effect": "Transform into different creature each round.",
        "source_paragraph": 9743,
        "casting_time": "1 action",
        "range": "120 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Utility"
        ],
        "rp_cost": 26
      }
    },
    {
      "index": 824,
      "original": {
        "school": "Transmutation",
        "level": 9,
        "name": "Shapechange",
        "effect": "Transform into different creature each round.",
        "source_paragraph": 10000,
        "casting_time": "1 action",
        "range": "120 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Utility"
        ],
        "rp_cost": 26
      }
    }
  ],
  "possibleHistoricalAliases": [],
  "classAccess": {
    "Druid": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Transmutation",
      "baseRpCost": 26
    },
    "Mage": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Transmutation",
      "baseRpCost": 26
    },
    "Wizard": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Illusion",
      "baseRpCost": 26
    }
  },
  "currentStatus": "blocked-pending-operational-review",
  "overlaySha256": "1ed808fb4abf2da12d1d6e8f5fbee4766d14364e7056e88ed3aa53d374c7d360"
}
```

## true-polymorph
```json
{
  "id": "true-polymorph",
  "catalogSource": {
    "name": "True Polymorph",
    "level": 9,
    "resonanceRank": 9,
    "school": "Transmutation",
    "schools": [
      "Transmutation",
      "Universal"
    ],
    "placements": [
      {
        "name": "True Polymorph",
        "school": "Transmutation",
        "level": 9,
        "summary": "Permanently transform creature or object."
      },
      {
        "name": "True Polymorph",
        "school": "Universal",
        "level": 9,
        "summary": "Permanently transform creature or object."
      }
    ],
    "classLevels": {
      "Cleric": 9,
      "Druid": 9,
      "Mage": 9,
      "Wizard": 9
    },
    "classRanks": {
      "Cleric": 9,
      "Druid": 9,
      "Mage": 9,
      "Wizard": 9
    },
    "classLearnLevels": {
      "Cleric": 17,
      "Druid": 17,
      "Mage": 17,
      "Wizard": 17
    },
    "classSchools": {
      "Cleric": "Universal",
      "Druid": "Transmutation",
      "Mage": "Transmutation",
      "Wizard": "Transmutation"
    },
    "castingTime": "Not specified in current rulebook",
    "range": "Not specified in current rulebook",
    "components": "Not specified in current rulebook",
    "duration": "Not specified in current rulebook",
    "description": "Permanently transform creature or object.",
    "alternateSummaries": [],
    "classes": [
      "Cleric",
      "Druid",
      "Mage",
      "Wizard"
    ],
    "status": "canon",
    "source": "Player Rulebook — Spell Lists"
  },
  "coreEntries": [
    {
      "index": 825,
      "original": {
        "school": "Transmutation",
        "level": 9,
        "name": "True Polymorph",
        "effect": "Permanently transform creature or object.",
        "source_paragraph": 10001,
        "casting_time": "1 action",
        "range": "120 feet",
        "duration": "Until dispelled",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Utility"
        ],
        "rp_cost": 26
      }
    },
    {
      "index": 935,
      "original": {
        "school": "Universal",
        "level": 9,
        "name": "True Polymorph",
        "effect": "Permanently transform creature or object.",
        "source_paragraph": 10136,
        "casting_time": "1 action",
        "range": "120 feet",
        "duration": "Until dispelled",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Utility"
        ],
        "rp_cost": 26
      }
    }
  ],
  "possibleHistoricalAliases": [],
  "classAccess": {
    "Cleric": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Universal",
      "baseRpCost": 26
    },
    "Druid": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Transmutation",
      "baseRpCost": 26
    },
    "Mage": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Transmutation",
      "baseRpCost": 26
    },
    "Wizard": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Transmutation",
      "baseRpCost": 26
    }
  },
  "currentStatus": "blocked-pending-operational-review",
  "overlaySha256": "03ed1b467c0cfc689d45471efd50318b8b3dfaaa345d1790ab43faad9a200abf"
}
```

## mass-polymorph
```json
{
  "id": "mass-polymorph",
  "catalogSource": {
    "name": "Mass Polymorph",
    "level": 9,
    "resonanceRank": 9,
    "school": "Transmutation",
    "schools": [
      "Transmutation"
    ],
    "placements": [
      {
        "name": "Mass Polymorph",
        "school": "Transmutation",
        "level": 9,
        "summary": "Transform up to 10 creatures into new forms."
      }
    ],
    "classLevels": {
      "Druid": 9,
      "Mage": 9,
      "Wizard": 9
    },
    "classRanks": {
      "Druid": 9,
      "Mage": 9,
      "Wizard": 9
    },
    "classLearnLevels": {
      "Druid": 17,
      "Mage": 17,
      "Wizard": 17
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
    "description": "Transform up to 10 creatures into new forms.",
    "alternateSummaries": [],
    "classes": [
      "Druid",
      "Mage",
      "Wizard"
    ],
    "status": "canon",
    "source": "Player Rulebook — Spell Lists"
  },
  "coreEntries": [
    {
      "index": 830,
      "original": {
        "school": "Transmutation",
        "level": 9,
        "name": "Mass Polymorph",
        "effect": "Transform up to 10 creatures into new forms.",
        "source_paragraph": 10006,
        "casting_time": "1 action",
        "range": "120 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Utility"
        ],
        "rp_cost": 26
      }
    }
  ],
  "possibleHistoricalAliases": [],
  "classAccess": {
    "Druid": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Transmutation",
      "baseRpCost": 26
    },
    "Mage": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Transmutation",
      "baseRpCost": 26
    },
    "Wizard": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Transmutation",
      "baseRpCost": 26
    }
  },
  "currentStatus": "blocked-pending-operational-review",
  "overlaySha256": "c0e148a1ccc5b1f18ca81fbff7a7216fd7a8b85411b42ca7c868d0f389c7e755"
}
```

## Existing separate operational buffer comparison: resonance-shield
```json
{
  "id": "resonance-shield",
  "classAccess": {
    "Cleric": {
      "rank": 0,
      "minimumClassLevel": 1,
      "school": "Abjuration",
      "baseRpCost": 0
    },
    "Druid": {
      "rank": 0,
      "minimumClassLevel": 1,
      "school": "Abjuration",
      "baseRpCost": 0
    },
    "Mage": {
      "rank": 0,
      "minimumClassLevel": 1,
      "school": "Abjuration",
      "baseRpCost": 0
    },
    "Monk": {
      "rank": 0,
      "minimumClassLevel": 1,
      "school": "Abjuration",
      "baseRpCost": 0
    },
    "Tinker": {
      "rank": 0,
      "minimumClassLevel": 1,
      "school": "Abjuration",
      "baseRpCost": 0
    },
    "Wizard": {
      "rank": 0,
      "minimumClassLevel": 1,
      "school": "Abjuration",
      "baseRpCost": 0
    },
    "Paladin": {
      "rank": 0,
      "minimumClassLevel": 2,
      "school": "Abjuration",
      "baseRpCost": 0
    }
  },
  "additionalRpCost": 1,
  "operational": {
    "id": "resonance-shield",
    "activation": "Action",
    "rangeFeet": 30,
    "targets": "One willing creature you can perceive within 30 feet",
    "duration": "Until the temporary HP are lost or you complete a long rest",
    "concentration": false,
    "components": [
      "V",
      "S"
    ],
    "resolution": "None.",
    "effect": "In addition to the class-specific rank cost and any Dissonance surcharge, spend 1 RP. Roll 1d4; the chosen creature gains that many temporary HP. It keeps the higher of these or its existing temporary HP; they never add together.",
    "scaling": "None. Damage dice, target count, range and duration do not automatically increase with character or class level.",
    "limitations": "The additional 1 RP conversion cost is mandatory. Temporary HP never restore real HP and cannot generate resources when gained or lost. Recasting requires a new paid cast and roll; keep the higher remaining amount. Rank is class-specific, so this spell is not necessarily a cantrip for every class. If the Core source placement matching the class-specific school and rank includes F, an existing class casting focus is additionally required.",
    "designNotes": "Conference decision: use the rank-0 1d4 effect plus mandatory1RP as the provisional single-ID rule. Retain all variants: rank0 catalog/Core1d4; rank2 catalog5tempHP perRP; rank2 Core2tempHP perRP. Rank2 alternatives are preserved as evidence, not cumulative effects or optional upgrades. Use Core30ft range and placement-specific focus requirement. Temporary HP end on next long rest; no fixed5 buff.",
    "previousDraftDesignNotes": "NEW provisional reconciliation of conflicting source placements. The source contains both 'convert 1 RP into 1d4 temporary HP' and '5 temporary HP per RP spent.' This unified playtest record uses the explicit +1 RP interface requested for the tranche and the fixed 5-HP value from the stronger detailed summary; the 1d4 variant remains preserved in the source ledger.",
    "authoringFile": "data/playtest/spell_drafts/batch_1.json"
  }
}
```

## Existing separate operational buffer comparison: heroism
```json
{
  "id": "heroism",
  "classAccess": {
    "Bard": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Crimson Agent": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Mirrorsage": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Thief": {
      "rank": 1,
      "minimumClassLevel": 3,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Wizard": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Paladin": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Enchantment",
      "baseRpCost": 2
    }
  },
  "additionalRpCost": 0,
  "operational": {
    "id": "heroism",
    "activation": "Action",
    "rangeFeet": 30,
    "targets": "One willing living creature you can perceive within range",
    "duration": "Concentration, up to 1 minute",
    "concentration": true,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "None; a willing target receives the effect automatically.",
    "effect": "The target gains S+M temporary HP when the spell is cast and is immune to Frightened while the spell lasts. Temporary HP remaining from this spell disappear when the spell ends. S is 1/2/3/4 at the casting class levels 1/5/11/17; M=max(1, that class casting ability modifier).",
    "scaling": "Temporary HP equals S+M, using the caster's class-level S and casting-ability M.",
    "limitations": "Temporary HP are granted once on cast, not every round, and never stack with other temporary HP. Recasting Heroism replaces the existing Heroism temporary HP only if the new value is higher. The spell does not remove non-fear conditions, heal real HP, or restore resources. Ranked casting causes normal Dissonance and Refrain.",
    "designNotes": "Core V2 Action, 30-foot range, V/S/F components, and source fear immunity are retained. Core lists Instantaneous duration and source gives no temporary-HP amount; concentration up to 1 minute and S+M temporary HP are NEW provisional mechanics chosen to make the effect finite and playable.",
    "authoringFile": "data/playtest/spell_drafts/batch_2.json"
  }
}
```

## Existing separate operational buffer comparison: false-life
```json
{
  "id": "false-life",
  "classAccess": {
    "Cleric": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Necromancy",
      "baseRpCost": 2
    },
    "Crimson Agent": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Necromancy",
      "baseRpCost": 2
    },
    "Druid": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Necromancy",
      "baseRpCost": 2
    },
    "Shaman": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Necromancy",
      "baseRpCost": 2
    },
    "Thief": {
      "rank": 1,
      "minimumClassLevel": 3,
      "school": "Necromancy",
      "baseRpCost": 2
    },
    "Wizard": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Necromancy",
      "baseRpCost": 2
    }
  },
  "additionalRpCost": 0,
  "operational": {
    "id": "false-life",
    "activation": "Action",
    "rangeFeet": 30,
    "targets": "One willing living creature you can perceive within 30 feet",
    "duration": "Until the temporary HP are lost or you complete a long rest",
    "concentration": false,
    "components": [
      "V",
      "S",
      "F"
    ],
    "resolution": "None.",
    "effect": "The chosen creature gains 1d4+4 temporary HP.",
    "scaling": "None; remains 1d4+4 temporary HP.",
    "limitations": "Temporary HP do not stack; keep the higher remaining amount. They are not healing, cannot exceed this spell's rolled amount from one cast, and cannot generate damage, healing, resource, or death-prevention triggers when lost. Ranked casting causes normal Dissonance and Refrain.",
    "designNotes": "Core V2 Action, 30-foot range, V/S/F components, and source 1d4+4 temporary HP are preserved. The continuing temporary-HP lifetime is specified because Core lists only Instantaneous casting duration. Conference decision: one willing living target is the explicit provisional recipient.",
    "authoringFile": "data/playtest/spell_drafts/batch_3.json"
  }
}
```
