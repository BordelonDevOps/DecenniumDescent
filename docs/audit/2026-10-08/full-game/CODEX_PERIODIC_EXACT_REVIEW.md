Please perform an adversarial exact review of the implemented bounded periodic package below. There are 32 periodic definitions among57 total definitions,14 source-qualified hooks,114 source references and69 interface checks passing; generic28 tests pass82checks/4200states. Source books and active class/spell objects remain unchanged. This does NOT close allDD16: remaining root/slow/curse/disease/mark binding and exhaustive semantic review remain open.

All latest accepted refinements have been applied: core/custom same-family arbitration unified with explicit supersession; highest expected group damage then earliest, no DC tie; source-group cap before global arbitration; one Medicine record vs all eligible magical-healing cures; all ordinary fires per Action/immersion but DEX per surviving record; actual-HP prerequisite respected if printed; Blood Curse special save; Mage Bolt tagged-focus duration upgrade; Ashblood recipe excluded from ongoing fire; base2 vs explicit hard cap separated; Prolonged applies to later qualifying refresh4, including legal same-owner multiclass; Vein Cutter Bleed2 separate from one-turn slow/damage penalty; Bloodroot typefallbackslashing; generic/Core source quotes unchanged.

Please look for mechanical contradictions, unintended stacked ticks, incorrect cure scope, missing required source constraints, death/heal loopholes, or active source mismatches in THIS package. Separate material blockers from editorial issues. For source-group arithmetic, maxDamagingInstances is potential ceiling: Crimson default1, BloodEcho2; Mage shared group keeps distinct schedules but only highestexpected due application damages. Expected damage is unmitigated BEFORE resistance/immunity and includes a real due bonus such as BloodEcho+1; do not drop an active condition solely because its damage type is immune. Registry active/immune flags refer to effect/condition immunity. Do not invent new prerequisites from display names. The ordinary spell Elemental Bolt remains separate from Mage class Elemental Bolt.

Also specifically assess Seal Minor Wound and Bloodleech/Blood Curse: our binding removes only the eligible Bleed component/record, not an independently present poison or curse; the spell prohibition on removing poison/curse does not erase its explicit ability to end one ordinary Bleed. If a future source expressly makes the Bleed special-cure-only, metadata must instead respect that.

Return exact fixes or bounded closure. We will still keepDD16 open and continue its remaining named conditions afterward.

{
  "scope": "Exact periodic family integration and linked hooks; NOT full DD16 closure",
  "familyRules": [
    {
      "id": "family.bleeding",
      "rule": "Explicit hostile Bleed classification for immunity, curing and stated eligibility. Class/owner/source timing and caps remain separate. No inherited damage package.",
      "sameMarkerArbitration": true
    },
    {
      "id": "family.ongoing-fire",
      "rule": "Only explicitly registered creature-attached Burn-style periodic fire. Excludes direct fire, areas, hazards, environmental flames, object ignition, Resonance Burn and names alone.",
      "sameMarkerArbitration": true
    },
    {
      "id": "periodic.arbitration",
      "rule": "Generic Core and custom groups enter ONE family arbitration at an identical target marker. Within each family at one identical target timing marker, select one stack group by highest expected unmitigated damage then earliest application. Apply source instance caps before comparing. All due groups consume their tick, including non-damaging losers. Different markers and families resolve separately. Stable unique application sequence breaks simultaneous applications in resolution order; lexical group ID is a final implementation tie-break only.",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_GENERIC_CUSTOM_ALIGNMENT.md"
      ]
    },
    {
      "id": "ownership",
      "rule": "Ordinary your means ownerCharacterId. Explicit class phrases restrict sourceClass. Crimson technical Bleed engine hooks require owned Crimson instances. Suppressed, immune, inactive or expired effects do not satisfy active-effect hooks."
    },
    {
      "id": "hp-cure-separation",
      "rule": "HP prohibition prevents regained HP. Legal positive-potential magical healing can still invoke a registered Bleed cure, including Blood Curse CON save; a remover explicitly requiring actual HP gained retains that prerequisite."
    }
  ],
  "supersessions": [
    {
      "reviewEvidence": "docs/audit/2026-10-08/full-game/GPT_GENERIC_CUSTOM_ALIGNMENT.md",
      "rule": "SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review."
    }
  ],
  "periodicDefinitions": [
    {
      "mechanicalId": "mage.fire-focus.burn",
      "displayName": "Fire Focus Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at start of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "mage.fire-focus-burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "archElementalMasteryAdditionalTicks": 1,
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": [
        "Elemental Surge explicitly applies this profile. Arch Elemental Mastery grants one additional tick.",
        "Independent Inferno schedule remains; only highest expected application in this group damages at a shared marker."
      ]
    },
    {
      "mechanicalId": "mage.inferno-lance.burn",
      "displayName": "Inferno Lance Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d6 fire damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d6",
        "damageType": "fire",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "mage.fire-focus-burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "archElementalMasteryAdditionalTicks": 1,
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": [
        "Requires failed initial save. Arch Elemental Mastery grants one additional tick.",
        "Passive Fire Focus can legally apply on the same finisher; group arbitration prevents added shared ticks."
      ]
    },
    {
      "mechanicalId": "crimson-agent.bleed",
      "displayName": "Crimson Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at start of each of the next 3 regular target turns.",
      "ending": "After 3 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 3,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "crimson-agent.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 2,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "defaultInstanceCap": 1,
        "exceptionInstanceCap": {
          "feature": "crimson-agent.arch.blood-echo",
          "cap": 2
        },
        "hardRemainingTickCap": 5,
        "baseDurationTicks": 3,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "sum of permitted independent instances"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
        "kitAction": {
          "uses": 1,
          "actor": "self or adjacent helper",
          "automatic": true,
          "scope": "all Crimson-engine Bleed instances from one source owner on this victim",
          "provenance": "Printed automatic kit endpoint; NEW one-use consumption."
        }
      },
      "integrationDecisions": [
        "Default instance cap is one. Blood Echo permits two independent instances; third refreshes oldest.",
        "Arterial Cut extends one existing instance by two ticks to maximum five remaining.",
        "Blood Echo adds one to one instance next tick once on an owner turn; include that actual due bonus in group expectation.",
        "No BG or proc generation from periodic damage. A spread instance cannot spread again."
      ]
    },
    {
      "mechanicalId": "dragoon.bleed",
      "displayName": "Dragoon Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "dragoon.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
        "kitAction": {
          "uses": 1,
          "actor": "self or adjacent helper",
          "automatic": true,
          "scope": "selected Dragoon Bleed record",
          "provenance": "Printed kit endpoint; NEW one-use consumption."
        }
      },
      "integrationDecisions": [
        "Impale Bleeding binds this engine profile; pin and Bleed have independent endings."
      ]
    },
    {
      "mechanicalId": "dragoon.burn",
      "displayName": "Dragoon Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "dragoon.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "ranger.synergy.bleed",
      "displayName": "Weapon Synergy Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at end of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 2,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "ranger.synergy.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "ranger.imbue.burn",
      "displayName": "Fire Imbue Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "ranger.imbue.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "ranger.emberroot.burn",
      "displayName": "Emberroot Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "ranger.emberroot.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "shaman.blood-curse.bleed",
      "displayName": "Blood Curse Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 necrotic damage at start of each of the next 3 regular target turns.",
      "ending": "After 3 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "necrotic",
        "ticks": 3,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "shaman.blood-curse.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 3,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "saveToEnd",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "applying Shaman class DC"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "Printed Medicine/healing-save endpoints; reviewed ordinary explicit-removal eligibility.",
        "magicalHealingSave": {
          "ability": "CON",
          "dc": "applying Shaman class DC",
          "scope": "one save per active Blood Curse record"
        }
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "shaman.bloodroot.bleed",
      "displayName": "Bloodroot Trail Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 slashing damage at end of target next regular turn. Initial zone damage remains necrotic.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "slashing",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "shaman.bloodroot.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": [
        "Initial zone damage remains necrotic. The separately untyped Bleed uses the explicit type bridge; not inferred from the zone."
      ]
    },
    {
      "mechanicalId": "shaman.flame-totem.burn",
      "displayName": "Flame Totem Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "shaman.flame-totem.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "shaman.flask.burn",
      "displayName": "Burn Flask",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "shaman.flask.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "shaman.cinderflame.burn",
      "displayName": "Cinderflame Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "shaman.cinderflame.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "soldier.overwatch.bleed",
      "displayName": "Overwatch Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at start of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 1,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "soldier.overwatch.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "thief.bloodleech.bleed",
      "displayName": "Bloodleech Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "thief.bloodleech.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": [
        "Requires failed poison save; critical healing is a separate once-per-dose consequence.",
        "One recipe instance per target/owner; maximum two different active poison recipes from this owner."
      ]
    },
    {
      "mechanicalId": "thief.shadow-stab.bleed",
      "displayName": "Shadow Stab Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at end of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 2,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "thief.shadow-stab.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "thief.vein-cutter.bleed",
      "displayName": "Vein Cutter Bleed",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at end of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 2,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "thief.vein-cutter.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": [
        "Specific effect preserves two Bleed ticks despite shorter general duration field.",
        "Speed -10 lasts through end next regular target turn; -1 next attack damage is consumed or expires at that same endpoint.",
        "Consumes a prepared poison without its normal recipe effect and does not occupy a normal recipe-instance slot."
      ]
    },
    {
      "mechanicalId": "thief.ashblood.periodic",
      "displayName": "Ashblood periodic poison",
      "familyTags": [],
      "effect": "1 fire damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1",
        "damageType": "fire",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "thief.ashblood.periodic:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryExtinguishable": false,
        "corePoisonedRemovalApplies": false,
        "underlyingPoisonRemoval": "Only an explicitly reviewed cure covering active poison recipe effects can remove remaining recipe riders.",
        "expiry": "Two scheduled ticks; recipe can be refreshed under Thief engine rules."
      },
      "integrationDecisions": [
        "Internal poison-recipe delayed fire; explicitly excluded from family.ongoing-fire. Can coexist with a Burn-family tick.",
        "Poison damage immunity blocks poison damage only; Core Poisoned immunity blocks only actual Poisoned components. Explicit immunity to poison effects/toxins is checked separately against the application.",
        "Failed recipe save still required; critical no-HP-recovery ends end next regular turn separately from the two-tick fire.",
        "One recipe instance per owner/target and maximum two different ongoing poison recipes from that owner."
      ]
    },
    {
      "mechanicalId": "warrior.splinter-bone-fangs.bleed",
      "displayName": "Mutation Bleed — Splinter Bone Fangs",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "warrior.splinter-bone-fangs.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "warrior.gore-maw.bleed",
      "displayName": "Mutation Bleed — Gore Maw",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "warrior.gore-maw.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "warrior.eviscerator-protocol.bleed",
      "displayName": "Mutation Bleed — Eviscerator Protocol",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "1d4 physical damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "applying-physical-hit-or-slashing",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "warrior.eviscerator-protocol.bleed:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "druid.charbear.burn",
      "displayName": "Charbear Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "druid.charbear.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": [
        "Nearby aura damage and smoke are separate effects; family immunity does not negate their unrelated components."
      ]
    },
    {
      "mechanicalId": "mage.elemental-bolt.burn",
      "displayName": "Elemental Bolt Fire rider",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at start of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "mage.fire-focus-burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "archElementalMasteryAdditionalTicks": 1,
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": [
        "Explicit new attached-fire classification in the Mage Fire Focus stack group.",
        "Its card is explicitly tagged focus: Arch Elemental Mastery adds one tick. Elemental Fusion and Cascade lack that tag and do not receive this upgrade."
      ]
    },
    {
      "mechanicalId": "mage.elemental-fusion.burn",
      "displayName": "Elemental Fusion Fire + Cold rider",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at start of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "mage.elemental-fusion.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": [
        "Only Fire+Cold pair applies this rider; separate Speed reduction retains its own endpoint."
      ]
    },
    {
      "mechanicalId": "mage.cascade-storm.burn",
      "displayName": "Cascade Storm first fire hit rider",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "mage.cascade-storm.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": [
        "Only first fire target gets this rider. NEW missing-marker fallback is end next regular target turn."
      ]
    },
    {
      "mechanicalId": "cleric.flame.burn",
      "displayName": "Flame Invocation fire",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d6 fire damage at start of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d6",
        "damageType": "fire",
        "ticks": 2,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "cleric.flame.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "cleric.divine-invocation.burn",
      "displayName": "Divine Invocation Flame fire",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d6 fire damage at start of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d6",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "cleric.divine-invocation.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "wizard.combo-surge.burn",
      "displayName": "Combo Surge Fire + Cold fire",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d6 fire damage at start of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d6",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.start",
        "stackGroupTemplate": "wizard.combo-surge.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": [
        "Fire damage rider and failed-STR Restrained component are separate; ending one does not silently end the other."
      ]
    },
    {
      "mechanicalId": "tinker.burn-injector.burn",
      "displayName": "Burn Injector",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 2 regular target turns.",
      "ending": "After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 2,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "tinker.burn-injector.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 2,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "tinker.fire-bomb.burn",
      "displayName": "Fire Bomb Burn",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "1d4 fire damage at end of each of the next 1 regular target turns.",
      "ending": "After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.",
      "stacking": "Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.",
      "immunityRule": "Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": 1,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "tinker.fire-bomb.burn:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": true,
        "extraTurnTicks": false,
        "outsideInitiative": "Preserve clock; one due step per complete 6 elapsed seconds, without duplicate ticks when entering/leaving initiative.",
        "baseDurationTicks": 1,
        "refreshNeverShortens": true,
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": []
    },
    {
      "mechanicalId": "core.bleeding",
      "displayName": "Core Bleeding",
      "familyTags": [
        "family.bleeding"
      ],
      "effect": "At the end of the affected creature's regular turn, take damage equal to its current PB, unless the selected reviewed application prints a different magnitude. Use that application's specified physical type; if none, slashing.",
      "ending": "Persists until its source or applicable cure ends it. Self or adjacent helper spends an Action selecting one active eligible Bleed record before a WIS (Medicine) check: printed cure DC, otherwise recorded applying effect/class/spell DC, otherwise 10. Success or Critical Success ends that record only. One legal magical healing event with positive pre-cap/pre-prohibition potential ends all ordinary records with an automatic-healing endpoint, even at full HP or while Corrupted/Decay prevents actual HP gain. Each Shaman Blood Curse instead gets its own printed CON save. Explicit end-one/end-all removers retain exact scope and protected-source exceptions.",
      "stacking": "Independent source-owner records enter unified family arbitration at their actual marker. No DC tie-break or separate generic damage layer. Medicine ends one selected record; positive-potential magical healing ends all eligible automatic-cure records.",
      "immunityRule": "Creatures explicitly immune to bleeding/blood-loss effects cannot gain it. Specific spell/class/item Bleeding numbers replace the generic PB magnitude only when printed.",
      "periodic": {
        "dice": "affected creature PB",
        "damageType": "source physical type or slashing",
        "ticks": null,
        "baseDurationTicks": null,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "core.bleeding:<sourceIdentity>:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": false,
        "extraTurnTicks": false,
        "refreshNeverShortens": true,
        "outsideInitiative": "Preserve clock, one step per complete six seconds; no duplicated transition ticks.",
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "specialCureRequired": false,
        "artifactLevel": false,
        "magicalHealingEndpoint": "end",
        "magicalHealingScope": "every eligible active record on recipient",
        "positivePotentialRequired": true,
        "actualHpGainRequired": false,
        "medicine": {
          "activation": "Action",
          "actor": "self or adjacent helper",
          "ability": "WIS",
          "skill": "Medicine",
          "dcPrecedence": [
            "printed cure DC",
            "recorded applying effect/class/spell DC",
            "10"
          ],
          "scope": "one eligible record selected before roll"
        },
        "explicitRemoval": "Use remover exact one/all/owner restrictions.",
        "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership."
      },
      "integrationDecisions": [
        "SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review."
      ]
    },
    {
      "mechanicalId": "core.burning",
      "displayName": "Core Burning",
      "familyTags": [
        "family.ongoing-fire"
      ],
      "effect": "At end of the affected creature's regular turn its generic record offers 1d4 fire damage to unified family arbitration, unless its source specifies another magnitude. Only the winning stack group deals damage. Damage immunity does not by itself remove Burning.",
      "ending": "Self or adjacent helper may spend one Action to end all active ordinary-extinguishable attached fires on this creature. Full immersion of all burning portions does the same. Explicit protected-source exceptions survive. At each regular target turn end, after due ticks are consumed, each surviving active ongoing-fire record with future damage remaining makes its own binary DEX save against its own source DC or 10. Success ends only that record. An indefinite generic fire counts as having future damage; a finite record with its final tick consumed expires without another save.",
      "stacking": "Independent records enter unified ongoing-fire family arbitration. One Action/full immersion clears all ordinary-extinguishable records; DEX saves operate per surviving eligible record, not one selected-source save for all fires.",
      "immunityRule": "Fire immunity prevents the damage but does not automatically end Burning unless the source or immunity says so. An effect explicitly immune to Burning blocks application.",
      "periodic": {
        "dice": "1d4",
        "damageType": "fire",
        "ticks": null,
        "baseDurationTicks": null,
        "marker": "target.regular-turn.end",
        "stackGroupTemplate": "core.burning:<sourceIdentity>:<ownerCharacterId>",
        "maximumDamagingInstancesPerGroup": 1,
        "replacementTiming": false,
        "extraTurnTicks": false,
        "refreshNeverShortens": true,
        "outsideInitiative": "Preserve clock, one step per complete six seconds; no duplicated transition ticks.",
        "withinGroupDamagePolicy": "one strongest expected due application; ties earliest"
      },
      "cure": {
        "ordinaryConditionRemoval": true,
        "ordinaryExtinguishable": true,
        "mundaneMethods": [
          "Action by self or adjacent helper",
          "full immersion of all burning portions"
        ],
        "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
        "endingSave": {
          "ability": "DEX",
          "dcPrecedence": [
            "printed ending DC",
            "recorded source DC",
            "10"
          ],
          "marker": "end of regular target turn after any end-turn tick",
          "eligibility": "record still active with at least one future scheduled tick remaining",
          "scope": "this record only"
        },
        "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
        "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing."
      },
      "integrationDecisions": [
        "SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review."
      ]
    }
  ],
  "hooks": [
    {
      "id": "cleric.judging-light",
      "rule": "Active, unsuppressed eligibility.weakened or classification.curse qualifies; no owner restriction. A Curse class engine name or unclassified flavor text does not qualify. One added dice packet per qualifying Smite, not per condition.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/cleric.json",
          "cardId": "cleric.base.judging-light",
          "originalDisplayName": "Judging Light",
          "effect": "Judging Light. Tags: smite, passive. When your Divine Smite damages a creature currently affected by a Cursed or Weakened condition, add S d4 radiant damage to that Smite. Roll these dice once as part of the Smite; they do not create a second hit or trigger.",
          "duration": "Passive",
          "activation": "Passive",
          "cost": "0",
          "rangeAndTarget": "Self",
          "frequency": "Always",
          "sourceObjectSha256": "96d760c5dd15f8605dac966187d9def1501e8e320a2afe5292ea729a187bf45a"
        }
      ]
    },
    {
      "id": "thief.sneak-condition",
      "rule": "Owned active family.bleeding, core.poisoned or thief.crippled can satisfy the condition route. Own legal multiclass effects qualify; the remaining weapon, turn, disadvantage and trigger requirements still apply.",
      "sources": [
        {
          "kind": "engine",
          "path": "data/public/class_playtests/thief.json",
          "engineIndex": 0,
          "text": "Dexterity governs weapons and class DC/M. Choose Intelligence or Wisdom for noncombat class tool/sense checks at 1. Hit Die d8; light armor, daggers, shortswords, thrown weapons and hand crossbows; thieves tools and poison kit. Sneak Attack is automatic at 1: once on your regular turn, add ceil(class level/2)d6 to one finesse/ranged weapon hit if you had advantage, an active ally threatens target within 5 ft, or target is suffering your Bleed/Poisoned/Crippled. Disadvantage prevents Sneak Attack even if canceled into a straight roll. A feature can explicitly grant Sneak Attack on a different qualifying hit but never more than once/regular turn. Copies, poison ticks and companions cannot Sneak Attack.",
          "textSha256": "a5351d054b7591c02249049b8ffa97596d63be6f7520922d11a6856d5ca23920"
        }
      ]
    },
    {
      "id": "thief.vile-tactics",
      "rule": "Active Bleeding, Poisoned or Crippled target as stated in the card trigger. No invented owner restriction; several conditions do not multiply bonus.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/thief.json",
          "cardId": "thief.hero.blackguard.vile-tactics",
          "originalDisplayName": "Vile Tactics",
          "effect": "Add 1d6 weapon damage. Separate from Sneak but neither repeats on poison ticks nor copied attacks; multiple conditions do not multiply the bonus.",
          "duration": "Instant",
          "activation": "Triggered",
          "cost": "0",
          "rangeAndTarget": "One weapon hit against Bleeding/Poisoned/Crippled enemy",
          "frequency": "Once/own turn",
          "sourceObjectSha256": "e724a872b5a9e76cd223658f0bdd917fe77eb1c97ea03ee1316ca55ff74b7424"
        }
      ]
    },
    {
      "id": "warrior.terror-engine",
      "rule": "Only this owner's Warrior-feature Shaken, Frightened or ACTIVE Disoriented. Count creatures, not effect records. At least two hostile creatures within 30 feet; pending Disoriented does not qualify.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/warrior.json",
          "cardId": "warrior.supplement.terror-engine",
          "originalDisplayName": "Terror Engine",
          "effect": "While at least two hostile creatures within 30 feet are currently Shaken, Frightened or Disoriented by your Warrior features, reduce the first damage you take each round by 2.",
          "duration": "While condition is met",
          "activation": "Passive",
          "cost": "Feat choice",
          "rangeAndTarget": "Self",
          "frequency": "Always",
          "sourceObjectSha256": "18a819abbe1be664d52248d1109169cce92635c9ecf2f3e2edbada11e9908ea7"
        }
      ]
    },
    {
      "id": "druid.snow-leopard",
      "rule": "Explicit hostile Speed reduction or root tagged eligibility.slowed-foe qualifies. Prone, difficult terrain, cargo, Exhaustion, Grappled or Restrained alone do not.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/druid.json",
          "cardId": "druid.hero.winterfang.snow-leopard",
          "originalDisplayName": "Snow Leopard",
          "effect": "Claw 2d6+WIS cold, +1d4 once/turn against slowed foe. +5 Stealth on ice/snow and advantage on legal Hide there; source+10 reduced provisionally. Ignore ordinary ice/snow movement penalties, not magical restraining ice.",
          "duration": "While in Snow Leopard",
          "activation": "Action claw; passive traits",
          "cost": "One shift",
          "rangeAndTarget": "Winterfang Hero; claw 5 ft",
          "frequency": "One claw/Action",
          "sourceObjectSha256": "5b97e082b5e18608d7755b13fcc66635a23acdb2ca28c1b45d0531e932793bc4"
        }
      ]
    },
    {
      "id": "warrior.mythic-carapace",
      "rule": "Blocks family.bleeding, core.poisoned and family.ongoing-fire. This does not grant fire-damage immunity or blanket poison-effect immunity. Damage reduction and mutation refresh keep exact card limits.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/warrior.json",
          "cardId": "warrior.supplement.mythic-carapace",
          "originalDisplayName": "Mythic Carapace",
          "effect": "Gain DR 3 against all damage and immunity to Bleed, Poisoned and Burn-style ongoing fire effects. Once per encounter when one hit deals more than 20 actual damage after mitigation, gain 1 BT and refresh the remaining duration of your other active mutations to 3 rounds. It grants no serum-profile refresh.",
          "duration": "Until encounter ends, mutation ends or you fall below one-quarter maximum HP",
          "activation": "Passive while active",
          "cost": "One mutation slot; serum activation",
          "rangeAndTarget": "Self",
          "frequency": "Apex mutation",
          "sourceObjectSha256": "bd324a2eb115086a10dd9763b2d1847c547a4f239c60cf8e8fc465ac79bd8a2e"
        }
      ]
    },
    {
      "id": "dragoon.wyrmhide",
      "rule": "Advantage only on CON saves against registered Bleed, ongoing fire or Core Poisoned. It does not convert DEX extinguishing saves into CON saves or grant condition immunity.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/dragoon.json",
          "cardId": "dragoon.hero.dragon-guardian.wyrmhide",
          "originalDisplayName": "Wyrmhide",
          "effect": "Reduce each damage instance by 2 and gain advantage on CON saves against Bleed, Burn and Poisoned. No blanket condition immunity; effects already present persist and ordinary nonstacking reduction applies.",
          "duration": "While threshold met",
          "activation": "Passive",
          "cost": "0",
          "rangeAndTarget": "Self while above half maximum HP",
          "frequency": "Continuous",
          "sourceObjectSha256": "834b05a5f70a20bd83906930f2bb130da6574885c7a40076fcd633688d5831fa"
        }
      ]
    },
    {
      "id": "crimson.bleed-engine",
      "rule": "Technical Crimson Bleed counters, spreading, detonations, Blood Mark prerequisites and named engine benefits require this owner's Crimson-engine instances. Broad end-all wording is separately bound. No allied healing replacement is hostile Bleed.",
      "sources": [
        {
          "kind": "engine",
          "path": "data/public/class_playtests/crimson-agent.json",
          "engineIndex": 2,
          "text": "Your Bleed is a physical ongoing effect on a living, non-bloodless creature: 1d4 damage at the start of each of its next 3 turns, then ends. It is not a new attack and generates no BG or procs. Refresh duration instead of stacking; Blood Echo expressly allows two independent instances, maximum. An Action by the victim or an adjacent creature using a healer's kit ends all your Bleeds on that victim. Apply physical resistance/immunity normally. Track remaining ticks and creator per instance. Allied healing versions from Bloodweaver cost RP and never count as hostile Bleeds for detonation, spreading or generation.",
          "textSha256": "44a38acbffca3c994c2444d9f9183f7d8013ddda451f37182a4c2c25150755ea"
        },
        {
          "kind": "engine",
          "path": "data/public/class_playtests/crimson-agent.json",
          "engineIndex": 3,
          "text": "One Blood Mark at a time on a living target with your Bleed, except Phantom Strike, which explicitly may apply the mark without Bleed. It does not add a free Bleed. Marks last 5 of your regular turns, expire on encounter end or if the target dies, and never create damage by themselves. Rupture requires the target still within 60 ft and line of effect; it spends the mark. A mark does not defeat cover, planar boundaries or bloodlessness. Bloodtrail has its own tracking limits.",
          "textSha256": "cce77684b7ff646edb46587485d50ee3a89424262dc5711129a5baffc22e0ce6"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/crimson-agent.json",
          "cardId": "crimson-agent.base.blood-tithe",
          "originalDisplayName": "Blood Tithe",
          "effect": "Regain HP equal to M+class level after a creature bearing your Bleed dies. It must have been an active hostile combatant; no ally, summon, captive or corpse farming.",
          "duration": "Instant",
          "activation": "Triggered",
          "cost": "1 short-rest use",
          "rangeAndTarget": "Self after a hostile bleeding creature dies within 30 ft",
          "frequency": "1/short rest",
          "sourceObjectSha256": "f45186f24591e8f4044afb2c4bd9ab7fb667eaae4e4042cc444d6ad2e55d6aeb"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/crimson-agent.json",
          "cardId": "crimson-agent.arch.bloodbound-edge",
          "originalDisplayName": "Bloodbound Edge",
          "effect": "End up to 2 of your Bleed instances per target. Each takes 1d4 per remaining tick, maximum S d4 per creature, ignoring resistance but respecting immunity. This replaces their future ticks and grants no BG, healing or kill-trigger benefit.",
          "duration": "Instant",
          "activation": "Action",
          "cost": "3 BG; 1 short-rest use",
          "rangeAndTarget": "Up to 3 enemies with your Bleed within 30 ft",
          "frequency": "1/short rest",
          "sourceObjectSha256": "69161c88eb0e21401c7093403e89468bbf519194514f3db1c75814436ad4baf5"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/crimson-agent.json",
          "cardId": "crimson-agent.hero.thirstborn.blood-frenzy",
          "originalDisplayName": "Blood Frenzy",
          "effect": "Add 1 to direct weapon damage per hostile creature bearing your Bleed, maximum 3. Applies once per hit, not per Bleed instance. Secondary Bleed, copies and explosions gain no bonus.",
          "duration": "While hostile Bleeds persist",
          "activation": "Passive",
          "cost": "0",
          "rangeAndTarget": "Self",
          "frequency": "Continuous",
          "sourceObjectSha256": "8fa708e90ef5f4aac19de8401aa91684e8894578bc9c5810898d0b4e10d3f2b1"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/crimson-agent.json",
          "cardId": "crimson-agent.hero.thirstborn.hemorrhagic-plague",
          "originalDisplayName": "Hemorrhagic Plague",
          "effect": "After one of your Bleeds ticks, pay 1 BG; new target makes CON save. Failure applies one Bleed. A spread instance cannot spread again. This grants no BG and does not duplicate marks or immediate damage.",
          "duration": "Bleed 3 turns",
          "activation": "Triggered",
          "cost": "1 BG",
          "rangeAndTarget": "One new living enemy within 5 ft of a Bleed victim",
          "frequency": "Once every 3 of your turns",
          "sourceObjectSha256": "b24b1d08614bf6b0557dfd6ce9c4628f3b4b16ba7cb78513c0ad989351224b84"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/crimson-agent.json",
          "cardId": "crimson-agent.hero.thirstborn.exsanguinate",
          "originalDisplayName": "Exsanguinate",
          "effect": "CON save: (S+1)d8 necrotic, half on success; add 1d8 if it has your Bleed. If it fails and actually takes damage, regain 1 BG within the common gain cap. The refund cannot pay activation costs retroactively.",
          "duration": "Instant",
          "activation": "Action",
          "cost": "2 BG",
          "rangeAndTarget": "One living creature within 30 ft",
          "frequency": "Recharge 2",
          "sourceObjectSha256": "c0a45e7989c5c4f30ae52485cbb4b1303311bf5e711376dbfdbe23301685c5e4"
        }
      ]
    },
    {
      "id": "crimson.hemostasis",
      "rule": "Arch Hemostasis ends all Bleed on the target irrespective of owner, subject to an expressly stated protected cure exception. Healing remains its printed fixed roll even with no Bleed. Bloodweaver Hemostasis instead replaces a new allied application with one bounded healing effect, never a hostile Bleed.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/crimson-agent.json",
          "cardId": "crimson-agent.arch.hemostasis",
          "originalDisplayName": "Hemostasis",
          "effect": "End all Bleed on the target and restore S d6+M HP, regardless of number of ticks removed. You cannot create extra healing by inflicting extra Bleed. Works even if no Bleed is present, at the same RP cost.",
          "duration": "Instant",
          "activation": "Action",
          "cost": "2 RP",
          "rangeAndTarget": "One living creature touched",
          "frequency": "Recharge 2",
          "sourceObjectSha256": "2bf85b9f07acef890c6689ad383eedd19e5e219edf07376df24605e9b4b0f9b1"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/crimson-agent.json",
          "cardId": "crimson-agent.hero.bloodweaver.hemostasis",
          "originalDisplayName": "Hemostasis",
          "effect": "You may replace a new Bleed application on that ally with healing 1d4 at start of its next 3 turns. Pay extra RP even if original application was free. One such healing effect per target; it cannot spread, detonate, generate BG or trigger healing loops.",
          "duration": "3 target turns",
          "activation": "Passive",
          "cost": "1 additional RP per application",
          "rangeAndTarget": "One willing living ally in range of your Bleed application",
          "frequency": "Once/own turn",
          "sourceObjectSha256": "34d323e3effe5c0533760e277691a1b99e8a0eb0ee27905a6f1a99fd45e72275"
        }
      ]
    },
    {
      "id": "thief.persistent-bleed",
      "rule": "Actual qualifying trigger refreshes one existing owned record, max(current remaining,2); if owner has Prolonged and underlying base duration is exactly2, replace2 with4. Do not revive expired records, change dice, create instances or exceed an express hard cap.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/thief.json",
          "cardId": "thief.hero.shadowblade.persistent-bleed",
          "originalDisplayName": "Persistent Bleed",
          "effect": "Refresh one of your existing Bleed effects to 2 target turns. Cannot increase its dice, duplicate instances or extend a capped poison effect beyond its poison rules.",
          "duration": "Bleed extension",
          "activation": "Triggered",
          "cost": "0",
          "rangeAndTarget": "One enemy hit by your weapon",
          "frequency": "Once/own turn",
          "sourceObjectSha256": "e57918b455868ab546909c156209497661e8a1a6e266d7258159dbc35d466468"
        }
      ]
    },
    {
      "id": "thief.prolonged-suffering",
      "rule": "Owner-created Bleeds with printed base duration exactly2 use4 on application and qualifying refresh. Includes another legal class owned by same character; excludes base3 Crimson and Blood Curse. Base duration is not a hard cap; duration modifiers do not add unless explicit.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/thief.json",
          "cardId": "thief.hero.blackguard.prolonged-suffering",
          "originalDisplayName": "Prolonged Suffering",
          "effect": "When you apply Bleed with base 2-turn duration it lasts 4 turns instead. Never doubles dice or stacks with another extension; subsequent refresh sets to 4, not adds 4.",
          "duration": "Up to 4 target turns",
          "activation": "Passive",
          "cost": "0",
          "rangeAndTarget": "Your Bleed application",
          "frequency": "Continuous",
          "sourceObjectSha256": "f56220749f456a1621bc3d0bad2c0a6ace255dbb14e4d581394d98458f3df32d"
        }
      ]
    },
    {
      "id": "mage.arch-elemental-mastery",
      "rule": "Adds one tick to a reviewed Fire Burn from a Mage card explicitly tagged focus, or an explicit Focus-Burn reference. Includes Focus passive, Inferno Lance, Elemental Bolt and Elemental Surge reference. Excludes Fusion and Cascade. Group arbitration still applies.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/mage.json",
          "cardId": "mage.arch.elemental-mastery",
          "originalDisplayName": "Elemental Mastery",
          "effect": "Elemental Mastery. Tags: arcanist, focus. Improve the secondary effect of your current Focus. Fire Burns from your Focus cards last one additional turn but never stack. Cold Focus Speed reductions increase by another 5 feet, minimum 0. Lightning Focus's once-per-turn secondary arc increases from S flat lightning damage to S d4 lightning damage. Pivoted Focus uses the corresponding upgraded rider.",
          "duration": "Permanent",
          "activation": "Passive",
          "cost": "0",
          "rangeAndTarget": "Your current Elemental Focus spells",
          "frequency": "Always",
          "sourceObjectSha256": "ae201c6712d24adf2fd159717bcadeb2670f4238552a3787bcf4637a233d8be2"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/mage.json",
          "cardId": "mage.base.fire.fire",
          "originalDisplayName": "Fire",
          "effect": "Elemental Focus — Fire. Tags: focus, fire. Once on each of your turns when a Fire Mage spell deals damage, add S fire damage to one damaged target. That target also takes 1d4 fire at the start of its next turn; repeated Burns refresh rather than stack. FINISHER — Inferno Lance: after a completed Fire Nuke Chain, Bonus Action, 2 RP. Creatures in the 20-foot line make Dexterity saves, taking (S+1)d8 fire on failure or half on success. Failed targets also take 1d6 fire at the start of each of their next 2 turns.",
          "duration": "Permanent Focus; finisher instantaneous plus Burn",
          "activation": "Passive",
          "cost": "0; Inferno Lance costs 2 RP when primed",
          "rangeAndTarget": "Self; finisher uses a 20-foot-long, 5-foot-wide line originating from you",
          "frequency": "Choose at Mage 2; finisher recharge 3 rounds",
          "sourceObjectSha256": "672b096523204a34ad689eda8e6d3b28452ad8f2174e866eae03e22fe7c0102a"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/mage.json",
          "cardId": "mage.base.elemental-bolt",
          "originalDisplayName": "Elemental Bolt",
          "effect": "Elemental Bolt. Tags: mage-spell, elemental, focus, damage. Make a Mage spell attack. On a hit deal S d8 + M damage of your current Focus. Fire: target takes 1d4 fire at the start of its next turn. Cold: Speed -10 feet until the end of its next turn. Lightning: one different enemy within 10 feet takes S lightning damage. Secondary damage creates no new spell cast or chain credit.",
          "duration": "Instantaneous",
          "activation": "Action",
          "cost": "1 RP",
          "rangeAndTarget": "One creature within 60 feet",
          "frequency": "At will while RP remains",
          "sourceObjectSha256": "53e4cb8a853ebb6b0050cb85057ed70778daefcc71994dbe10f3ed79045c6f89"
        },
        {
          "kind": "card",
          "path": "data/public/class_playtests/mage.json",
          "cardId": "mage.arch.elemental-surge",
          "originalDisplayName": "Elemental Surge",
          "effect": "Elemental Surge. Tags: mage-spell, arcanist, elemental, focus, damage. Make a Mage spell attack. On a hit deal (S+1)d8 + M damage of your current Focus. Fire also applies the Focus Burn; Cold applies the Focus Speed reduction; Lightning applies the Focus secondary arc. This is Focus-eligible and can occupy one slot in a Nuke Chain.",
          "duration": "Instantaneous",
          "activation": "Action",
          "cost": "3 RP",
          "rangeAndTarget": "One creature within 60 feet",
          "frequency": "Recharge 2 rounds",
          "sourceObjectSha256": "867c57f627028cf1581a682574deedeec39e9b50f95c34fae003b9ac978bcaef"
        }
      ]
    },
    {
      "id": "oracle.burning-blood-boon-ii",
      "rule": "An eligible ongoing fire rider from that paid Revelation use cannot be ended by mundane extinguishing. This does not create a new ongoing fire rider, convert other damage to a Burn, or protect unrelated effects.",
      "sources": [
        {
          "kind": "card",
          "path": "data/public/class_playtests/oracle.json",
          "cardId": "oracle.supplement.burning-blood.burning-blood-boon-ii",
          "originalDisplayName": "Burning Blood — Boon II",
          "effect": "before activating a damaging Revelation, spend 1 RC to ignite it. Add fire damage equal to half that Revelation's unmodified rolled damage dice total, rounded down, minimum 1; mundane extinguishing cannot remove ongoing fire riders from that use. Until the Revelation resolves, your curse blood ignition does not damage allies.",
          "duration": "Until Revelation resolves",
          "activation": "Triggered before damaging Revelation",
          "cost": "1 RC plus Revelation’s cost",
          "rangeAndTarget": "One Revelation damage roll",
          "frequency": "Once per Revelation; no recursive riders",
          "sourceObjectSha256": "c036810faed1ac01bbf1f20083ee292b45b5c2bf4b489627a30c79553059ca6d"
        }
      ]
    },
    {
      "id": "spell.seal-minor-wound",
      "rule": "Select one eligible ordinary Bleed record and end that record. Shaman Blood Curse currently qualifies as Bleed; this does not remove an independently present curse, poison package, Wound or other affliction. The alternate stabilization choice restores no HP.",
      "sources": [
        {
          "kind": "operational-spell",
          "path": "data/public/spell_playtests/catalog.json",
          "spellId": "seal-minor-wound",
          "operational": {
            "id": "seal-minor-wound",
            "activation": "Action",
            "rangeFeet": 30,
            "targets": "One living creature you can perceive within 30 feet",
            "duration": "Instantaneous",
            "concentration": false,
            "components": [
              "V",
              "S"
            ],
            "resolution": "None.",
            "effect": "Choose one: stabilize a living creature at 0 HP without restoring HP, or end one ordinary Bleed/minor ongoing bleeding effect on the target.",
            "scaling": "None. Damage dice, target count, range and duration do not automatically increase with character or class level.",
            "limitations": "Restores no HP, removes no Wound, disease, poison, curse, death consequence, internal injury, or non-bleeding damage-over-time effect. A stabilized creature remains at 0 HP. Repeated cantrip casts use shared Refrain rules.",
            "designNotes": "Core V2 blocks and catalog summaries are preserved alongside this card. Components use the existing class focus where Core says F or M/F; this focus interpretation is provisional. Exact target eligibility, duration endpoints, saves where absent, concentration where unclear and anti-loop limits are provisional integration decisions. ",
            "previousDraftDesignNotes": "NEW provisional definition of 'minor bleeding'; healing was intentionally not added because the source specified stabilization or stopping minor bleeding only.",
            "authoringFile": "data/playtest/spell_drafts/batch_1.json"
          },
          "operationalSha256": "af5fe2b2d962bfa513e366ce0595fe3dab1b7ee8add6a7dbedf9bafada6819d0"
        }
      ]
    }
  ]
}