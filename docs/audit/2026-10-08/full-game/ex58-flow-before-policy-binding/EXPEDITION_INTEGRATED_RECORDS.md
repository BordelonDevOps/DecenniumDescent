# Expedition walkthrough — complete synthetic records

These are authored record instances, not a production save schema or executed campaign. The public walkthrough is independently readable. Original GPT facts and times are retained in the internal JSON; FLOW-C01 explicitly proposes the feeding-stop correction for exact review.

## Source comparison

| Quantity | Original outline | Current instantiated candidate |
|---|---:|---:|
| Haven entry, elapsed seconds | 59052 | 62592 |
| First Rest completion | 101052 | 104592 |
| Return deadline | 172800 | 172800 |
| Cash at next departure, cp | 4480 | 4480 |
| Oil consumed, pints | 8 | 8 |

The 3,540-second difference is two explicit 1,800-second supported meal stops, less the 60-second refill already inside the second stop. The canonical Watch boundaries remain fixed; they do not move to preserve the old example totals.

## Record instances

### EC-01 — Expedition, charter and roster

```json
{
  "id": "FLOW-EC-01",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-01",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "expeditionId": "Expedition-1",
    "charterVersion": {
      "id": "charter-1",
      "next": "charter-2",
      "acceptedBy": [
        "Arin",
        "Bea",
        "Cora",
        "Dane"
      ]
    },
    "roster": [
      "Arin",
      "Bea",
      "Cora",
      "Dane"
    ],
    "teams": {
      "Combat": [
        "Arin",
        "Bea",
        "Cora",
        "Dane"
      ],
      "Reconnaissance": [
        "Bea"
      ],
      "Research": [],
      "Resource": [
        "Cora"
      ],
      "Support": [
        "Dane"
      ],
      "assignmentOverlap": "Job labels are not concurrent task credit"
    },
    "offices": {
      "Expedition Leader": "Arin",
      "Quartermaster": "Arin",
      "Routekeeper": "Bea",
      "Surgeon": "Dane",
      "Claimant of Record": "Cora"
    },
    "objective": {
      "id": "licensed-crate-retrieval",
      "evidence": "same licensed crate delivered"
    },
    "thresholds": {
      "returnBySeconds": 172800,
      "grossAtLeastCp": 10000,
      "netAtLeastCp": 8000,
      "profitAtLeastCp": 6000,
      "nextReserveCp": 2000,
      "casualtyAbort": "any member missing or incapacitated; never triggered"
    },
    "finance": {
      "startingCapitalCp": 3000,
      "transactions": [
        {
          "transactionId": "buy-human-0",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 52400,
            "departurePreparationOffsetSeconds": -34000
          },
          "relativeTime": -34000,
          "payer": "Expedition cash",
          "payee": "Provisioner",
          "exactCp": {
            "numerator": 504,
            "denominator": 1
          },
          "settledCp": 504,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "operating cost",
          "episode": "first"
        },
        {
          "transactionId": "buy-animal-0",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 52500,
            "departurePreparationOffsetSeconds": -33900
          },
          "relativeTime": -33900,
          "payer": "Expedition cash",
          "payee": "Provisioner",
          "exactCp": {
            "numerator": 16,
            "denominator": 1
          },
          "settledCp": 16,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "operating cost",
          "episode": "first"
        },
        {
          "transactionId": "premium-0",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 53400,
            "departurePreparationOffsetSeconds": -33000
          },
          "relativeTime": -33000,
          "payer": "Expedition cash",
          "payee": "Underwriter",
          "exactCp": {
            "numerator": 600,
            "denominator": 1
          },
          "settledCp": 600,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "operating cost",
          "episode": "first"
        },
        {
          "transactionId": "room-fee",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 148992,
            "departurePreparationOffsetSeconds": 62592
          },
          "relativeTime": 62592,
          "payer": "Expedition cash",
          "payee": "Sera",
          "exactCp": {
            "numerator": 800,
            "denominator": 1
          },
          "settledCp": 800,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "operating cost",
          "episode": "first"
        },
        {
          "transactionId": "stable-fee",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 148992,
            "departurePreparationOffsetSeconds": 62592
          },
          "relativeTime": 62592,
          "payer": "Expedition cash",
          "payee": "Toma",
          "exactCp": {
            "numerator": 100,
            "denominator": 1
          },
          "settledCp": 100,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "operating cost",
          "episode": "first"
        },
        {
          "transactionId": "mandatory-inspection",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 150192,
            "departurePreparationOffsetSeconds": 63792
          },
          "relativeTime": 63792,
          "payer": "Expedition cash",
          "payee": "Haven inspector",
          "exactCp": {
            "numerator": 200,
            "denominator": 1
          },
          "settledCp": 200,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "mandatory",
          "episode": "first"
        },
        {
          "transactionId": "sale-crate",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 155592,
            "departurePreparationOffsetSeconds": 69192
          },
          "relativeTime": 69192,
          "payer": "Pera",
          "payee": "Expedition cash",
          "exactCp": {
            "numerator": 12000,
            "denominator": 1
          },
          "settledCp": 12000,
          "rounding": "sale floor once",
          "status": "paid",
          "kind": "sale",
          "episode": "first"
        },
        {
          "transactionId": "levy",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 157392,
            "departurePreparationOffsetSeconds": 70992
          },
          "relativeTime": 70992,
          "payer": "Expedition cash",
          "payee": "Haven treasury",
          "exactCp": {
            "numerator": 600,
            "denominator": 1
          },
          "settledCp": 600,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "tax",
          "episode": "first"
        },
        {
          "transactionId": "guild-share",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 157392,
            "departurePreparationOffsetSeconds": 70992
          },
          "relativeTime": 70992,
          "payer": "Expedition cash",
          "payee": "Local guild",
          "exactCp": {
            "numerator": 2240,
            "denominator": 1
          },
          "settledCp": 2240,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "sponsor",
          "episode": "first"
        },
        {
          "transactionId": "distribution-Arin",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 226800,
            "departurePreparationOffsetSeconds": 140400
          },
          "relativeTime": 140400,
          "payer": "Expedition cash",
          "payee": "Arin",
          "exactCp": {
            "numerator": 1235,
            "denominator": 1
          },
          "settledCp": 1235,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "profit distribution",
          "episode": "first"
        },
        {
          "transactionId": "distribution-Bea",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 226800,
            "departurePreparationOffsetSeconds": 140400
          },
          "relativeTime": 140400,
          "payer": "Expedition cash",
          "payee": "Bea",
          "exactCp": {
            "numerator": 1235,
            "denominator": 1
          },
          "settledCp": 1235,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "profit distribution",
          "episode": "first"
        },
        {
          "transactionId": "distribution-Cora",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 226800,
            "departurePreparationOffsetSeconds": 140400
          },
          "relativeTime": 140400,
          "payer": "Expedition cash",
          "payee": "Cora",
          "exactCp": {
            "numerator": 1235,
            "denominator": 1
          },
          "settledCp": 1235,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "profit distribution",
          "episode": "first"
        },
        {
          "transactionId": "distribution-Dane",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 226800,
            "departurePreparationOffsetSeconds": 140400
          },
          "relativeTime": 140400,
          "payer": "Expedition cash",
          "payee": "Dane",
          "exactCp": {
            "numerator": 1235,
            "denominator": 1
          },
          "settledCp": 1235,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "profit distribution",
          "episode": "first"
        },
        {
          "transactionId": "next-stock",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 228600,
            "departurePreparationOffsetSeconds": 142200
          },
          "relativeTime": 142200,
          "payer": "Expedition cash",
          "payee": "Provisioner",
          "exactCp": {
            "numerator": 520,
            "denominator": 1
          },
          "settledCp": 520,
          "rounding": "purchase/fee ceil once",
          "status": "paid",
          "kind": "next inventory purchase",
          "episode": "next"
        }
      ],
      "sponsor": {
        "id": "SPONSOR-1",
        "rate": {
          "numerator": 1,
          "denominator": 5
        },
        "base": "gross less one applicable tax and mandatory rescue/quarantine",
        "signedBeforeDeparture": true,
        "grossGrantOrLoan": false
      },
      "policy": {
        "id": "INSURANCE-1",
        "insuredLot": "crate-1",
        "insuredValueCp": 12000,
        "premiumRate": {
          "numerator": 1,
          "denominator": 20
        },
        "premiumPayment": "premium-0",
        "term": {
          "startSeconds": 86400,
          "endSeconds": 148992,
          "activeSeconds": 62592,
          "halfOpen": true
        },
        "ordinaryLossFraction": {
          "numerator": 3,
          "denominator": 5
        },
        "episodeDeductibleCp": 2400,
        "lossEvents": [],
        "claims": [],
        "payoutCp": 0,
        "status": "closed without claim"
      },
      "settlement": {
        "grossCp": 12000,
        "taxCp": 600,
        "mandatoryCp": 200,
        "sponsorBaseCp": 11200,
        "sponsorCp": 2240,
        "netCp": 8960,
        "uniqueOtherOperatingCostsCp": 2020,
        "trueProfitCp": 6940,
        "nextReserveCp": 2000,
        "distributionCp": 4940,
        "eachCharacterCp": 1235,
        "cashBeforeDistributionCp": 9940,
        "cashAfterDistributionCp": 5000,
        "nextProcurementCp": 520,
        "finalCashCp": 4480,
        "capitalStillCashCp": 3000,
        "unspentEarmarkCp": 1480,
        "nextInventoryPaidCostCp": 520,
        "unpaidLiabilitiesCp": 0
      }
    },
    "participants": [
      {
        "id": "Arin",
        "kind": "Expedition character",
        "level": 3,
        "size": "Medium",
        "bodyMassLb": 150,
        "STR": 14,
        "walkingSpeedFt": 30,
        "personalGearMassLb": 24,
        "personalGearLoad": {
          "numerator": 12,
          "denominator": 5
        },
        "currentHP": 20,
        "maximumHP": 20,
        "Wounds": 0,
        "Strain": 0,
        "conditions": [],
        "lastBeneficialLongRest": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 86400,
          "departurePreparationOffsetSeconds": 0
        },
        "sourceStatus": "Synthetic fixture values; not a complete or approved character build",
        "acquiredOptionsAdded": [],
        "gear": [
          {
            "id": "Arin-closed-gear",
            "massLb": 22,
            "description": "Owned clothing, bedding and closed personal kit; physical contents stipulated, no combat or magical effect invoked"
          },
          {
            "id": "Lantern-A",
            "emptyMassLb": 2,
            "description": "Owned hooded lantern, compatible with the purchased oil; fuel counted separately"
          }
        ]
      },
      {
        "id": "Bea",
        "kind": "Expedition character",
        "level": 3,
        "size": "Medium",
        "bodyMassLb": 150,
        "STR": 14,
        "walkingSpeedFt": 30,
        "personalGearMassLb": 24,
        "personalGearLoad": {
          "numerator": 12,
          "denominator": 5
        },
        "currentHP": 20,
        "maximumHP": 20,
        "Wounds": 0,
        "Strain": 0,
        "conditions": [],
        "lastBeneficialLongRest": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 86400,
          "departurePreparationOffsetSeconds": 0
        },
        "sourceStatus": "Synthetic fixture values; not a complete or approved character build",
        "acquiredOptionsAdded": [],
        "gear": [
          {
            "id": "Bea-closed-gear",
            "massLb": 24,
            "description": "Owned clothing, bedding and closed personal kit; physical contents stipulated, no combat or magical effect invoked"
          }
        ]
      },
      {
        "id": "Cora",
        "kind": "Expedition character",
        "level": 3,
        "size": "Medium",
        "bodyMassLb": 150,
        "STR": 14,
        "walkingSpeedFt": 30,
        "personalGearMassLb": 24,
        "personalGearLoad": {
          "numerator": 12,
          "denominator": 5
        },
        "currentHP": 20,
        "maximumHP": 20,
        "Wounds": 0,
        "Strain": 0,
        "conditions": [],
        "lastBeneficialLongRest": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 86400,
          "departurePreparationOffsetSeconds": 0
        },
        "sourceStatus": "Synthetic fixture values; not a complete or approved character build",
        "acquiredOptionsAdded": [],
        "gear": [
          {
            "id": "Cora-closed-gear",
            "massLb": 22,
            "description": "Owned clothing, bedding and closed personal kit; physical contents stipulated, no combat or magical effect invoked"
          },
          {
            "id": "Lantern-B",
            "emptyMassLb": 2,
            "description": "Owned hooded lantern, compatible with the purchased oil; fuel counted separately"
          }
        ]
      },
      {
        "id": "Dane",
        "kind": "Expedition character",
        "level": 3,
        "size": "Medium",
        "bodyMassLb": 150,
        "STR": 14,
        "walkingSpeedFt": 30,
        "personalGearMassLb": 24,
        "personalGearLoad": {
          "numerator": 12,
          "denominator": 5
        },
        "currentHP": 20,
        "maximumHP": 20,
        "Wounds": 0,
        "Strain": 0,
        "conditions": [],
        "lastBeneficialLongRest": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 86400,
          "departurePreparationOffsetSeconds": 0
        },
        "sourceStatus": "Synthetic fixture values; not a complete or approved character build",
        "acquiredOptionsAdded": [],
        "gear": [
          {
            "id": "Dane-closed-gear",
            "massLb": 24,
            "description": "Owned clothing, bedding and closed personal kit; physical contents stipulated, no combat or magical effect invoked"
          }
        ]
      },
      {
        "id": "Mule-1",
        "kind": "significant registered animal",
        "profile": {
          "id": "mounts-vehicles-and-services.donkey-or-mule",
          "name": "Donkey or mule",
          "kind": "living-mount",
          "operationalStatus": "NEW SOURCE-AUTHORING PROFILE; exact candidate not yet approved",
          "operational": {
            "provenance": "All size, mass, abilities, natural AC, HP/Hit Dice, senses, behavior, supply quantities, draw capability and reference level below are NEW provisional game values, not inferred anatomy/Strength or external bestiary statistics. Source purchase price, walking Speed and carry pounds alone are retained numbers.",
            "priceCp": 800,
            "size": "Large",
            "spaceFt": 10,
            "baseBodyMassLb": 400,
            "abilities": {
              "STR": 13,
              "DEX": 11,
              "CON": 13,
              "INT": 2,
              "WIS": 12,
              "CHA": 5
            },
            "proficiencyBonus": 2,
            "naturalAC": 11,
            "naturalACIncludesDexterity": true,
            "maximumHP": 20,
            "hitDice": {
              "count": 3,
              "die": 8,
              "restUse": "real remaining dice and ordinary creature rest/healing limits; fixed maximumHP is this NEW profile, not regenerated from a class table"
            },
            "saveProficiencies": [],
            "skillProficiencies": [],
            "saves": "ability modifier only unless an actual later source grants proficiency; current Wounds/conditions apply",
            "initiative": "DEX modifier plus actual lawful modifiers",
            "passivePerception": 11,
            "senses": "ordinary sight, hearing and smell subject to actual light, line, distance/noise; no darkvision, blindsight, special detection or automatic advantage",
            "languages": [],
            "trainedCuesAreFluency": false,
            "immunities": [],
            "resistances": [],
            "innateSpells": [],
            "classResources": null,
            "walkingSpeedFt": 40,
            "travelMphBeforePenalties": 4.0,
            "carryPounds": 420,
            "cargoLoadCapacity": 42.0,
            "cargoLoadProvenance": "NEW explicit profile Load cap independent of Strength; not claimed source value",
            "burdenedAtLoadOrPounds": "positive supported load at least half the respective limit; one Burdened speed penalty, not two for the same state",
            "hardCarryAdmission": "must meet both pounds/Load and physical fit; no routine movement above either full cap",
            "riderSeats": 1,
            "riderSizeRule": "at least one size smaller; saddle and actual body compatible; both personal gear and rider equipment count",
            "grossDrawLimitLb": 600,
            "drawLimitProvenance": "NEW separate trained-harness capability on firm rolling surface or appropriate ice/snow runners; never a five-times Strength inference",
            "drawMovement": "minimum actual puller speed and vehicle cap; a gross draw above half the combined draw rating also causes the one Burdened speed penalty. Loads on a puller and towing constraints are separately checked; the same named penalty is not doubled. No slopes, broken axles or impassable terrain waived.",
            "attack": {
              "name": "Kick",
              "activation": "Action on its own independent regular turn only; one attack",
              "attackBonus": 3,
              "reachFt": 5,
              "damageDice": "1d4",
              "damageModifier": 1,
              "damageType": "bludgeoning",
              "rider": "none",
              "critical": "Core natural20 doubles damage dice only; natural1 misses"
            },
            "otherActions": "independent actual creature may use physically compatible Core Actions; controlled ridden Action list is Dash, Disengage, Dodge only; no Multiattack or automatic opportunity attack while controlled",
            "deathRule": "NEW default registered Expedition mount is significant and uses ordinary Core Wounds/dying/death saves. Mark significance before an encounter; no retrospective designation to dodge death. A later actual Ranger Beast bond uses its expressly different HP-only/immediate-death lifecycle instead.",
            "training": "Actual ride/cargo/harness/armor training recorded separately under TR-02/07. Purchase name/price is not proof of present training, willingness or health. War-named template may be sold with documented combat habituation but gains no new controlled attack.",
            "dailyFeed": {
              "sourceItemId": "mounts-vehicles-and-services.feed-per-day",
              "priceCp": 5,
              "feedMassLb": 10,
              "speciesCompatible": true,
              "meaning": "NEW one animal-day sold feed quantity for this template at the printed5cp daily reference. Actual species-compatible stock must be supplied; no fodder-to-meat conversion or infinite vendor stock."
            },
            "dailyWaterPints": 24,
            "foodCare": "Use these NEW animal quantities instead of the human Small/Medium/Large Supply basket, with actual safe water and continued rest. Do not add human lamp oil demand to an animal. Unmet daily food/water gives at most1 ordinary expedition Strain for that day; no additional duplicate failure per missing component. No automatic desert-fasting trait.",
            "threatReferenceLevel": 1,
            "threatReferenceProvenance": "NEW encounter-budget comparison only, not a CR, character class level, Ranger acquisition authorization or XP award",
            "sourceCR": "absent; retain absence, and any actual CR-gated ability needs its genuine source/profile predicate rather than treating referenceLevel as CR",
            "custody": "actual individual creature ID and original body history; Donkey or mule is one selected individual, not two. Purchase, hire, boarding, battle loss, rescue, bond and sale preserve that history."
          }
        },
        "currentHP": 20,
        "maximumHP": 20,
        "remainingHitDice": 3,
        "Wounds": 0,
        "Strain": 0,
        "training": [
          "harness",
          "Bea audible stop/walk cues",
          "calm feeding"
        ],
        "willing": true,
        "carriedHarnessLb": 8,
        "carriedHarnessLoad": {
          "numerator": 4,
          "denominator": 5
        },
        "diet": {
          "feedLbPerDay": 10,
          "waterPintsPerDay": 24
        },
        "classBond": {
          "presence": "absent"
        },
        "rider": {
          "presence": "absent"
        }
      },
      {
        "id": "Cart-1",
        "kind": "owned drawn frame",
        "profile": {
          "id": "mounts-vehicles-and-services.cart",
          "name": "Cart",
          "kind": "drawn-vehicle",
          "operationalStatus": "NEW SOURCE-AUTHORING PROFILE; exact candidate not yet approved",
          "operational": {
            "provenance": "Price retained; Cart maximumHP30 binds the reviewed ordinary cart body. Every other listed body quantity/geometry/handling number is NEW. No passengers, animals, harnesses, operators or contents are included in price.",
            "priceCp": 1500,
            "emptyMassLb": 200,
            "outerFeet": [
              8,
              5,
              4
            ],
            "usableBedFeet": [
              6,
              4,
              3
            ],
            "bodyMaterial": "wood with ordinary metal fittings",
            "structuralAC": 15,
            "maximumHP": 30,
            "payloadPounds": 300,
            "payloadLoads": 30,
            "cargoSublimitPounds": 300,
            "cargoSublimitLoads": 30,
            "maximumSeatedOccupantsIncludingDriver": 1,
            "requiredDrivers": 1,
            "minimumFittedPullers": 1,
            "tacticalSpeedCapFt": 40,
            "speedRule": "minimum current fitted puller Speed and cap. Each actual puller draw rating, combined gross vehicle+payload draw limit, route fit, stability and terrain must pass. One named Burdened penalty applies when either carried or gross-draw threshold qualifies; no duplicate penalty for the same mount.",
            "terrain": "firm wheel-supporting route; no ordinary climbing, stairs, ladders, swimming or unsupported gaps",
            "operatingFootprint": "vehicle envelope plus actual puller footprint and at least5ft forward harness gap; route must contain all real widths/heights/turning space",
            "turning": "one90-degree turn needs traveled distance at least the vehicle length and a clear swept envelope; sharper/blocked maneuver needs an actual separate route/work plan, not an automatic check",
            "controls": "driver uses one Action per regular turn in tactical operation to guide/brake using the actual reins/lever and one hand; NEW manual brakes are included. Pullers expend actual movement in the linked drive event. Driver cannot claim a separate mounted turn for a pulling animal or duplicate movement by changing drivers. Outside initiative driving is continuous actual work, not rest.",
            "movementEvent": "one linked vehicle/puller movement event per numbered round; resolve after required current driver Action and puller movement budgets are available. No future crew Action is presumed. All contributing budgets spent once. No vehicle Dash/Disengage/Reaction/attack; actual pullers have only their legal creature Actions.",
            "setupMinutes": 5,
            "setupActors": 1,
            "loadingRule": "TR-12, real necessary handling; setup harness is additional, no free load/receivers",
            "brake": "actual controlled stop at end of paid move; uncrewed/unhitched vehicle at rest stays at rest unless terrain/force actually moves it; no generic magical parking",
            "primaryConstituents": "original main frame, principal axle/runner set and bed structure; subordinate wheels, pins, harness fittings or brake pads can be replaced by actual compatible stock",
            "zeroHP": "Broken, stops useful self/drawn transport; retains wreck, mass, passengers and custody. No automatic occupant damage from mere HP0. Real collision/fall/dislodgement is a separately declared event. Reaching0 does not erase salvage or restore original frame.",
            "repair": "TR-14 ordinary structural repair with source-specific cost/time and original main body; not creature healing. No equipment Integrity track in parallel."
          }
        },
        "currentHP": 30,
        "occupants": [],
        "driver": "Bea",
        "driverWalking": true,
        "originalPrimaryMembers": [
          "frame-1",
          "axle-1",
          "bed-1"
        ],
        "repairEvents": [],
        "nativeCreatureTurn": false
      }
    ],
    "closure": {
      "realHavenEntry": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 148992,
        "departurePreparationOffsetSeconds": 62592
      },
      "nextDeparture": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 259200,
        "departurePreparationOffsetSeconds": 172800
      },
      "unresolvedObligations": []
    }
  }
}
```

### EC-02 — Clock, assignment, work and rest

```json
{
  "id": "FLOW-EC-02",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-02",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "interval": {
      "startSeconds": 86400,
      "endSeconds": 259200,
      "activeSeconds": 172800,
      "halfOpen": true
    },
    "actorId": [
      "Arin",
      "Bea",
      "Cora",
      "Dane"
    ],
    "activityId": "full-expedition-timeline",
    "reservedResources": {
      "retreat": [
        {
          "round": 1,
          "interval": {
            "startSeconds": 118260,
            "endSeconds": 118266,
            "activeSeconds": 6,
            "halfOpen": true
          },
          "initiative": [
            "Arin",
            "Bea",
            "Mule-1",
            "Cora",
            "Dane",
            "Opponent-1"
          ],
          "driverContributionReservedBeforeMule": true,
          "drive": {
            "id": "drive-1",
            "mover": "Mule-1",
            "carrier": "Cart-1",
            "initiator": "Bea",
            "distanceFt": 30,
            "selfPowered": true,
            "pullerMoveSpentFt": 30,
            "pullerAction": "Dodge",
            "resolvesAfterRequiredContributions": true,
            "vehicleDriveCount": 1
          },
          "actorBudgets": {
            "Arin": {
              "stance": "Mobile",
              "movementSpentFt": 30,
              "ActionSpent": true,
              "BonusActionSpent": false,
              "ReactionSpent": false,
              "Action": "one escape check while carrying A in the other available hand"
            },
            "Bea": {
              "stance": "Mobile",
              "movementSpentFt": 30,
              "ActionSpent": true,
              "BonusActionSpent": false,
              "ReactionSpent": false,
              "Action": "driver command/brake contribution; walks with reins, no cart seat"
            },
            "Cora": {
              "stance": "Mobile",
              "movementSpentFt": 30,
              "ActionSpent": true,
              "BonusActionSpent": false,
              "ReactionSpent": false,
              "Action": "Dodge"
            },
            "Dane": {
              "stance": "Mobile",
              "movementSpentFt": 30,
              "ActionSpent": true,
              "BonusActionSpent": false,
              "ReactionSpent": false,
              "Action": "Dodge while carrying crate in both hands; no weapon attack"
            }
          },
          "leadDie": 11,
          "leadTotal": 16,
          "numericalDegree": "Success",
          "naturalShift": "none",
          "EscapeAdded": 1,
          "PursuitAdded": 0,
          "threat": {
            "actor": "Opponent-1",
            "attackBonus": 3,
            "naturalDie": 2,
            "total": 5,
            "target": "Arin",
            "AC": 13,
            "nativeResult": "miss",
            "actualReachFt": 5,
            "actualTargetDistanceFt": 5,
            "movementAvailableFt": 30,
            "damage": 0,
            "otherThreats": 0
          },
          "otherGenericEscapeAwards": 0,
          "endingRectanglesFt": {
            "Cart-1": {
              "x": [
                7,
                15
              ],
              "y": [
                {
                  "numerator": 15,
                  "denominator": 2
                },
                {
                  "numerator": 25,
                  "denominator": 2
                }
              ]
            },
            "Mule-1": {
              "x": [
                20,
                30
              ],
              "y": [
                5,
                15
              ]
            },
            "harness-gap": {
              "x": [
                15,
                20
              ],
              "y": [
                9,
                11
              ]
            },
            "Arin": {
              "x": [
                5,
                10
              ],
              "y": [
                0,
                5
              ]
            },
            "Bea": {
              "x": [
                10,
                15
              ],
              "y": [
                {
                  "numerator": 25,
                  "denominator": 2
                },
                {
                  "numerator": 35,
                  "denominator": 2
                }
              ]
            },
            "Cora": {
              "x": [
                5,
                10
              ],
              "y": [
                15,
                20
              ]
            },
            "Dane": {
              "x": [
                10,
                15
              ],
              "y": [
                0,
                5
              ]
            },
            "Opponent-1": {
              "x": [
                0,
                5
              ],
              "y": [
                0,
                5
              ]
            }
          }
        },
        {
          "round": 2,
          "interval": {
            "startSeconds": 118266,
            "endSeconds": 118272,
            "activeSeconds": 6,
            "halfOpen": true
          },
          "initiative": [
            "Arin",
            "Bea",
            "Mule-1",
            "Cora",
            "Dane",
            "Opponent-1"
          ],
          "driverContributionReservedBeforeMule": true,
          "drive": {
            "id": "drive-2",
            "mover": "Mule-1",
            "carrier": "Cart-1",
            "initiator": "Bea",
            "distanceFt": 30,
            "selfPowered": true,
            "pullerMoveSpentFt": 30,
            "pullerAction": "Dodge",
            "resolvesAfterRequiredContributions": true,
            "vehicleDriveCount": 1
          },
          "actorBudgets": {
            "Arin": {
              "stance": "Mobile",
              "movementSpentFt": 30,
              "ActionSpent": true,
              "BonusActionSpent": false,
              "ReactionSpent": false,
              "Action": "one escape check while carrying A in the other available hand"
            },
            "Bea": {
              "stance": "Mobile",
              "movementSpentFt": 30,
              "ActionSpent": true,
              "BonusActionSpent": false,
              "ReactionSpent": false,
              "Action": "driver command/brake contribution; walks with reins, no cart seat"
            },
            "Cora": {
              "stance": "Mobile",
              "movementSpentFt": 30,
              "ActionSpent": true,
              "BonusActionSpent": false,
              "ReactionSpent": true,
              "Action": "Ready manual gate closure after the one enemy attack"
            },
            "Dane": {
              "stance": "Mobile",
              "movementSpentFt": 30,
              "ActionSpent": true,
              "BonusActionSpent": false,
              "ReactionSpent": false,
              "Action": "Dodge while carrying crate in both hands; no weapon attack"
            }
          },
          "leadDie": 20,
          "leadTotal": 25,
          "numericalDegree": "Success",
          "naturalShift": "up one to Critical Success",
          "EscapeAdded": 2,
          "PursuitAdded": 0,
          "threat": {
            "actor": "Opponent-1",
            "attackBonus": 3,
            "naturalDie": 3,
            "total": 6,
            "target": "Arin",
            "AC": 13,
            "nativeResult": "miss",
            "actualReachFt": 5,
            "actualTargetDistanceFt": 5,
            "movementAvailableFt": 30,
            "damage": 0,
            "otherThreats": 0
          },
          "otherGenericEscapeAwards": 0,
          "endingRectanglesFt": {
            "Cart-1": {
              "x": [
                37,
                45
              ],
              "y": [
                {
                  "numerator": 15,
                  "denominator": 2
                },
                {
                  "numerator": 25,
                  "denominator": 2
                }
              ]
            },
            "Mule-1": {
              "x": [
                50,
                60
              ],
              "y": [
                5,
                15
              ]
            },
            "harness-gap": {
              "x": [
                45,
                50
              ],
              "y": [
                9,
                11
              ]
            },
            "Arin": {
              "x": [
                35,
                40
              ],
              "y": [
                0,
                5
              ]
            },
            "Bea": {
              "x": [
                40,
                45
              ],
              "y": [
                {
                  "numerator": 25,
                  "denominator": 2
                },
                {
                  "numerator": 35,
                  "denominator": 2
                }
              ]
            },
            "Cora": {
              "x": [
                35,
                40
              ],
              "y": [
                15,
                20
              ]
            },
            "Dane": {
              "x": [
                40,
                45
              ],
              "y": [
                0,
                5
              ]
            },
            "Opponent-1": {
              "x": [
                30,
                35
              ],
              "y": [
                0,
                5
              ]
            }
          }
        }
      ],
      "refills": [
        {
          "id": "refill-1",
          "interval": {
            "startSeconds": 108000,
            "endSeconds": 108060,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 21600,
          "relativeEnd": 21660,
          "mainWorker": "Arin",
          "backupWorker": "Cora",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 60,
          "reason": "Independent route pause"
        },
        {
          "id": "refill-2",
          "interval": {
            "startSeconds": 129660,
            "endSeconds": 129720,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 43260,
          "relativeEnd": 43320,
          "mainWorker": "Arin",
          "backupWorker": "Cora",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Inside the existing meal stop"
        },
        {
          "id": "refill-3",
          "interval": {
            "startSeconds": 151320,
            "endSeconds": 151380,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 64920,
          "relativeEnd": 64980,
          "mainWorker": "Iris",
          "backupWorker": "June",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        },
        {
          "id": "refill-4",
          "interval": {
            "startSeconds": 172980,
            "endSeconds": 173040,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 86580,
          "relativeEnd": 86640,
          "mainWorker": "Iris",
          "backupWorker": "June",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        },
        {
          "id": "refill-5",
          "interval": {
            "startSeconds": 194640,
            "endSeconds": 194700,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 108240,
          "relativeEnd": 108300,
          "mainWorker": "Iris",
          "backupWorker": "June",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        },
        {
          "id": "refill-6",
          "interval": {
            "startSeconds": 216300,
            "endSeconds": 216360,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 129900,
          "relativeEnd": 129960,
          "mainWorker": "Leto",
          "backupWorker": "Mara",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        },
        {
          "id": "refill-7",
          "interval": {
            "startSeconds": 237960,
            "endSeconds": 238020,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 151560,
          "relativeEnd": 151620,
          "mainWorker": "Leto",
          "backupWorker": "Mara",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        }
      ],
      "Haven": [
        {
          "id": "haven-intake",
          "activity": "intake",
          "actors": [
            "Arin",
            "Ione"
          ],
          "interval": {
            "startSeconds": 148992,
            "endSeconds": 149592,
            "activeSeconds": 600,
            "halfOpen": true
          },
          "relativeStart": 62592,
          "relativeEnd": 63192,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        },
        {
          "id": "haven-quarantine-inspection",
          "activity": "quarantine inspection",
          "actors": [
            "Dane",
            "Oren"
          ],
          "interval": {
            "startSeconds": 149592,
            "endSeconds": 150192,
            "activeSeconds": 600,
            "halfOpen": true
          },
          "relativeStart": 63192,
          "relativeEnd": 63792,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        },
        {
          "id": "haven-provenance",
          "activity": "provenance",
          "actors": [
            "Cora",
            "Ione"
          ],
          "interval": {
            "startSeconds": 150192,
            "endSeconds": 151992,
            "activeSeconds": 1800,
            "halfOpen": true
          },
          "relativeStart": 63792,
          "relativeEnd": 65592,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        },
        {
          "id": "haven-known-finite-appraisal-and-quote",
          "activity": "known finite appraisal and quote",
          "actors": [
            "Cora",
            "Pera"
          ],
          "interval": {
            "startSeconds": 151992,
            "endSeconds": 153792,
            "activeSeconds": 1800,
            "halfOpen": true
          },
          "relativeStart": 65592,
          "relativeEnd": 67392,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        },
        {
          "id": "haven-buyer-agreement",
          "activity": "buyer agreement",
          "actors": [
            "Arin",
            "Pera"
          ],
          "interval": {
            "startSeconds": 153792,
            "endSeconds": 155592,
            "activeSeconds": 1800,
            "halfOpen": true
          },
          "relativeStart": 67392,
          "relativeEnd": 69192,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        },
        {
          "id": "haven-ledger-and-claims",
          "activity": "ledger and claims",
          "actors": [
            "Arin",
            "Ione"
          ],
          "interval": {
            "startSeconds": 155592,
            "endSeconds": 157392,
            "activeSeconds": 1800,
            "halfOpen": true
          },
          "relativeStart": 69192,
          "relativeEnd": 70992,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        },
        {
          "id": "haven-standing-notice",
          "activity": "standing notice",
          "actors": [
            "Arin",
            "Bea",
            "Cora",
            "Dane",
            "Ione"
          ],
          "interval": {
            "startSeconds": 157392,
            "endSeconds": 157992,
            "activeSeconds": 600,
            "halfOpen": true
          },
          "relativeStart": 70992,
          "relativeEnd": 71592,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        },
        {
          "id": "haven-advancement-record",
          "activity": "advancement record",
          "actors": [
            "Arin",
            "Dane"
          ],
          "interval": {
            "startSeconds": 157992,
            "endSeconds": 158592,
            "activeSeconds": 600,
            "halfOpen": true
          },
          "relativeStart": 71592,
          "relativeEnd": 72192,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        },
        {
          "id": "haven-prospective-next-charter",
          "activity": "prospective next charter",
          "actors": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "interval": {
            "startSeconds": 158592,
            "endSeconds": 162192,
            "activeSeconds": 3600,
            "halfOpen": true
          },
          "relativeStart": 72192,
          "relativeEnd": 75792,
          "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
        }
      ],
      "mealIntervals": [
        {
          "id": "meal-Arin-0-food",
          "lotId": "food-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-0-water",
          "lotId": "water-human-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-1-food",
          "lotId": "food-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 130620,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43320,
          "relativeEnd": 44220,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-1-water",
          "lotId": "water-human-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 130620,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43320,
          "relativeEnd": 44220,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-2-food",
          "lotId": "food-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-2-water",
          "lotId": "water-human-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-3-food",
          "lotId": "food-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-3-water",
          "lotId": "water-human-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-0-food",
          "lotId": "food-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-0-water",
          "lotId": "water-human-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-1-food",
          "lotId": "food-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 129600,
            "endSeconds": 130500,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43200,
          "relativeEnd": 44100,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-1-water",
          "lotId": "water-human-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 129600,
            "endSeconds": 130500,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43200,
          "relativeEnd": 44100,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-2-food",
          "lotId": "food-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-2-water",
          "lotId": "water-human-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-3-food",
          "lotId": "food-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-3-water",
          "lotId": "water-human-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-0-food",
          "lotId": "food-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-0-water",
          "lotId": "water-human-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-1-food",
          "lotId": "food-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 130620,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43320,
          "relativeEnd": 44220,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-1-water",
          "lotId": "water-human-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 130620,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43320,
          "relativeEnd": 44220,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-2-food",
          "lotId": "food-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-2-water",
          "lotId": "water-human-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-3-food",
          "lotId": "food-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-3-water",
          "lotId": "water-human-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-0-food",
          "lotId": "food-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-0-water",
          "lotId": "water-human-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-1-food",
          "lotId": "food-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 129600,
            "endSeconds": 130500,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43200,
          "relativeEnd": 44100,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-1-water",
          "lotId": "water-human-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 129600,
            "endSeconds": 130500,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43200,
          "relativeEnd": 44100,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-2-food",
          "lotId": "food-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-2-water",
          "lotId": "water-human-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-3-food",
          "lotId": "food-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-3-water",
          "lotId": "water-human-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-0-feed",
          "lotId": "feed-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 87300,
            "endSeconds": 88200,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 900,
          "relativeEnd": 1800,
          "amount": {
            "numerator": 5,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-0-water",
          "lotId": "water-mule-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 87300,
            "endSeconds": 88200,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 900,
          "relativeEnd": 1800,
          "amount": {
            "numerator": 12,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-1-feed",
          "lotId": "feed-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 130500,
            "endSeconds": 131400,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 44100,
          "relativeEnd": 45000,
          "amount": {
            "numerator": 5,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-1-water",
          "lotId": "water-mule-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 130500,
            "endSeconds": 131400,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 44100,
          "relativeEnd": 45000,
          "amount": {
            "numerator": 12,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-2-feed",
          "lotId": "feed-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 5,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-2-water",
          "lotId": "water-mule-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 12,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-3-feed",
          "lotId": "feed-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 5,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-3-water",
          "lotId": "water-mule-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 12,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "cleaning-0",
          "lotId": "sundries-0",
          "recipient": "Expedition shared cleanup",
          "interval": {
            "startSeconds": 87300,
            "endSeconds": 87360,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 900,
          "relativeEnd": 960,
          "amount": {
            "numerator": 1,
            "denominator": 2
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": false
        },
        {
          "id": "cleaning-1",
          "lotId": "sundries-0",
          "recipient": "Expedition shared cleanup",
          "interval": {
            "startSeconds": 130620,
            "endSeconds": 130680,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 44220,
          "relativeEnd": 44280,
          "amount": {
            "numerator": 1,
            "denominator": 2
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": false
        },
        {
          "id": "cleaning-2",
          "lotId": "sundries-0",
          "recipient": "Expedition shared cleanup",
          "interval": {
            "startSeconds": 173700,
            "endSeconds": 173760,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 87300,
          "relativeEnd": 87360,
          "amount": {
            "numerator": 1,
            "denominator": 2
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": false
        },
        {
          "id": "cleaning-3",
          "lotId": "sundries-0",
          "recipient": "Expedition shared cleanup",
          "interval": {
            "startSeconds": 216900,
            "endSeconds": 216960,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 130500,
          "relativeEnd": 130560,
          "amount": {
            "numerator": 1,
            "denominator": 2
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": false
        }
      ]
    },
    "activeProgressSeconds": {
      "travel": 57600,
      "Haven": 13200,
      "extraStops": 3600,
      "overlapAlreadyCounted": 60
    },
    "rest": {
      "prospectiveDay0Slot": {
        "startSeconds": 144000,
        "endSeconds": 172800,
        "activeSeconds": 28800,
        "halfOpen": true
      },
      "actualFirst": {
        "startSeconds": 162192,
        "endSeconds": 190992,
        "activeSeconds": 28800,
        "halfOpen": true
      },
      "debtEvents": [
        {
          "id": "missed-rest-0",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 172800,
            "departurePreparationOffsetSeconds": 86400
          },
          "actors": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "deadline": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 230400,
            "departurePreparationOffsetSeconds": 144000
          },
          "StrainAtOpening": 0
        },
        {
          "id": "clear-debt",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 190992,
            "departurePreparationOffsetSeconds": 104592
          },
          "actors": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "debtRemaining": false,
          "deadlineStrain": 0
        }
      ],
      "firstRestLightActivity": [
        {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        {
          "startSeconds": 173700,
          "endSeconds": 173760,
          "activeSeconds": 60,
          "halfOpen": true
        }
      ],
      "firstRestSleepSeconds": 27840,
      "firstBeneficial": true,
      "previousBeneficialCompletion": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 86400,
        "departurePreparationOffsetSeconds": 0
      },
      "secondActual": {
        "startSeconds": 230400,
        "endSeconds": 259200,
        "activeSeconds": 28800,
        "halfOpen": true
      },
      "secondBeneficial": false,
      "secondsBetweenCompletions": 68208,
      "noNewHPNeeded": true,
      "HPAfter": {
        "Arin": 20,
        "Bea": 20,
        "Cora": 20,
        "Dane": 20
      },
      "classResourceChanges": [],
      "simultaneousCraftTrainingResearchSeconds": 0,
      "extraWork": "Return travel and required Haven operations replace part of scheduled Rest; no third productive crafting/research/training Watch is awarded."
    },
    "restDebt": [
      {
        "id": "missed-rest-0",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 172800,
          "departurePreparationOffsetSeconds": 86400
        },
        "actors": [
          "Arin",
          "Bea",
          "Cora",
          "Dane"
        ],
        "deadline": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 230400,
          "departurePreparationOffsetSeconds": 144000
        },
        "StrainAtOpening": 0
      },
      {
        "id": "clear-debt",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 190992,
          "departurePreparationOffsetSeconds": 104592
        },
        "actors": [
          "Arin",
          "Bea",
          "Cora",
          "Dane"
        ],
        "debtRemaining": false,
        "deadlineStrain": 0
      }
    ],
    "completion": "one continuing clock; detailed event states supplied"
  }
}
```

### EC-03 — Physical lots, Supply and daily support

```json
{
  "id": "FLOW-EC-03",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-03",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "lotId": "physical-manifest-1",
    "identity": [
      {
        "id": "food-0",
        "item": "sealed ration-equivalent food",
        "amount": {
          "numerator": 16,
          "denominator": 1
        },
        "unit": "lb",
        "massLb": {
          "numerator": 16,
          "denominator": 1
        },
        "packedAt": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 50400,
          "departurePreparationOffsetSeconds": -36000
        },
        "expiresAt": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 2642400,
          "departurePreparationOffsetSeconds": 2556000
        },
        "costCp": 400,
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "water-human-0",
        "item": "potable water",
        "amount": {
          "numerator": 64,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 64,
          "denominator": 1
        },
        "costCp": 8,
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "feed-0",
        "item": "species-compatible mule feed",
        "amount": {
          "numerator": 20,
          "denominator": 1
        },
        "unit": "lb",
        "massLb": {
          "numerator": 20,
          "denominator": 1
        },
        "costCp": 10,
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "water-mule-0",
        "item": "potable water",
        "amount": {
          "numerator": 48,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 48,
          "denominator": 1
        },
        "costCp": 6,
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "sundries-0",
        "item": "ordinary expendable cleaning cloth and twine",
        "amount": {
          "numerator": 2,
          "denominator": 1
        },
        "unit": "lb",
        "massLb": {
          "numerator": 2,
          "denominator": 1
        },
        "costCp": 16,
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "oil-1",
        "item": "compatible lamp oil",
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 3,
          "denominator": 4
        },
        "containerId": "flask-1",
        "costCp": 10,
        "fullInclusiveMassLb": {
          "numerator": 1,
          "denominator": 1
        },
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "oil-2",
        "item": "compatible lamp oil",
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 3,
          "denominator": 4
        },
        "containerId": "flask-2",
        "costCp": 10,
        "fullInclusiveMassLb": {
          "numerator": 1,
          "denominator": 1
        },
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "oil-3",
        "item": "compatible lamp oil",
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 3,
          "denominator": 4
        },
        "containerId": "flask-3",
        "costCp": 10,
        "fullInclusiveMassLb": {
          "numerator": 1,
          "denominator": 1
        },
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "oil-4",
        "item": "compatible lamp oil",
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 3,
          "denominator": 4
        },
        "containerId": "flask-4",
        "costCp": 10,
        "fullInclusiveMassLb": {
          "numerator": 1,
          "denominator": 1
        },
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "oil-5",
        "item": "compatible lamp oil",
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 3,
          "denominator": 4
        },
        "containerId": "flask-5",
        "costCp": 10,
        "fullInclusiveMassLb": {
          "numerator": 1,
          "denominator": 1
        },
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "oil-6",
        "item": "compatible lamp oil",
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 3,
          "denominator": 4
        },
        "containerId": "flask-6",
        "costCp": 10,
        "fullInclusiveMassLb": {
          "numerator": 1,
          "denominator": 1
        },
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "oil-7",
        "item": "compatible lamp oil",
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 3,
          "denominator": 4
        },
        "containerId": "flask-7",
        "costCp": 10,
        "fullInclusiveMassLb": {
          "numerator": 1,
          "denominator": 1
        },
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      },
      {
        "id": "oil-8",
        "item": "compatible lamp oil",
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "pint",
        "massLb": {
          "numerator": 3,
          "denominator": 4
        },
        "containerId": "flask-8",
        "costCp": 10,
        "fullInclusiveMassLb": {
          "numerator": 1,
          "denominator": 1
        },
        "owner": "Expedition-1",
        "origin": "actual finite stock sold before this descent, synthetic seller receipt",
        "creationByRule": false,
        "transfersResetAge": false,
        "restrictions": [
          "ordinary nonmagical stock; no recipe/harvest output implied"
        ]
      }
    ],
    "amount": "See exact per-lot rational quantities",
    "massAndGeometry": {
      "initialPreallocationPayloadLb": 188,
      "initialGrossDrawLb": 388,
      "contentsFit": {
        "bedFt": [
          6,
          4,
          3
        ],
        "allocatedStorageFt3": 24,
        "longestPackedBundleFt": 3,
        "crateFt": [
          2,
          1,
          1
        ],
        "closure": "sealed skins and flasks; lashed food/feed bags and closed crate"
      },
      "noDoubleTare": "8 full 1-lb flasks already include 2 lb of flask bodies; water is separate from the 28 one-pound skins."
    },
    "clockAndCondition": {
      "sameOriginalLots": true,
      "newProcurement": {
        "id": "next-procurement",
        "payment": "next-stock",
        "start": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 228600,
          "departurePreparationOffsetSeconds": 142200
        },
        "completion": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 229920,
          "departurePreparationOffsetSeconds": 143520
        },
        "newOriginLots": [
          {
            "id": "food-next",
            "lb": 16
          },
          {
            "id": "water-human-next",
            "pints": 64
          },
          {
            "id": "feed-next",
            "lb": 20
          },
          {
            "id": "water-mule-next",
            "pints": 48
          },
          {
            "id": "sundries-next",
            "lb": 2
          },
          {
            "id": "oil-next-1",
            "pints": 1,
            "container": "next-flask-1"
          },
          {
            "id": "oil-next-2",
            "pints": 1,
            "container": "next-flask-2"
          },
          {
            "id": "oil-next-3",
            "pints": 1,
            "container": "next-flask-3"
          },
          {
            "id": "oil-next-4",
            "pints": 1,
            "container": "next-flask-4"
          },
          {
            "id": "oil-next-5",
            "pints": 1,
            "container": "next-flask-5"
          },
          {
            "id": "oil-next-6",
            "pints": 1,
            "container": "next-flask-6"
          },
          {
            "id": "oil-next-7",
            "pints": 1,
            "container": "next-flask-7"
          },
          {
            "id": "oil-next-8",
            "pints": 1,
            "container": "next-flask-8"
          }
        ],
        "waterFilling": {
          "interval": {
            "startSeconds": 228600,
            "endSeconds": 229020,
            "activeSeconds": 420,
            "halfOpen": true
          },
          "workers": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "assignment": {
            "Arin": [
              "skin-01",
              "skin-02",
              "skin-03",
              "skin-04",
              "skin-05",
              "skin-06",
              "skin-07"
            ],
            "Bea": [
              "skin-08",
              "skin-09",
              "skin-10",
              "skin-11",
              "skin-12",
              "skin-13",
              "skin-14"
            ],
            "Cora": [
              "skin-15",
              "skin-16",
              "skin-17",
              "skin-18",
              "skin-19",
              "skin-20",
              "skin-21"
            ],
            "Dane": [
              "skin-22",
              "skin-23",
              "skin-24",
              "skin-25",
              "skin-26",
              "skin-27",
              "skin-28"
            ]
          },
          "minutesPerSkin": 1,
          "totalWorkerMinutes": 28,
          "elapsedMinutes": 7
        },
        "remainingPacking": {
          "interval": {
            "startSeconds": 229020,
            "endSeconds": 229920,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "workers": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "method": "Receive sealed fitting bundles, place/secure disjoint bundles with actual access; no new harness or vehicle is purchased"
        },
        "oldContainerHistoryRetained": true,
        "nextPreallocationPayloadUpperBoundLb": 190,
        "newFuelAlreadyInLanternBAtDeparturePints": 1,
        "oldOilAtDeparturePints": 0,
        "costChargedToCompletedEpisodeAgain": 0
      }
    },
    "custody": [
      {
        "id": "skin-01",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-02",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-03",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-04",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-05",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-06",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-07",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-08",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-09",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-10",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-11",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-12",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-13",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-14",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-15",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-16",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-human-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-17",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-18",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-19",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-20",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-21",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-22",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-23",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-24",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-25",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-26",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-27",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "skin-28",
        "emptyMassLb": 1,
        "capacityPints": 4,
        "openingContents": {
          "lot": "water-mule-0",
          "pints": 4
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true,
        "cleanAndCompatible": true
      },
      {
        "id": "flask-1",
        "emptyMassLb": {
          "numerator": 1,
          "denominator": 4
        },
        "capacityPints": 1,
        "openingContents": {
          "lot": "oil-1",
          "pints": 1
        },
        "location": "Cart-1",
        "retainedWhenEmpty": true,
        "cleanAndCompatible": true
      },
      {
        "id": "flask-2",
        "emptyMassLb": {
          "numerator": 1,
          "denominator": 4
        },
        "capacityPints": 1,
        "openingContents": {
          "lot": "oil-2",
          "pints": 1
        },
        "location": "Cart-1",
        "retainedWhenEmpty": true,
        "cleanAndCompatible": true
      },
      {
        "id": "flask-3",
        "emptyMassLb": {
          "numerator": 1,
          "denominator": 4
        },
        "capacityPints": 1,
        "openingContents": {
          "lot": "oil-3",
          "pints": 1
        },
        "location": "Cart-1",
        "retainedWhenEmpty": true,
        "cleanAndCompatible": true
      },
      {
        "id": "flask-4",
        "emptyMassLb": {
          "numerator": 1,
          "denominator": 4
        },
        "capacityPints": 1,
        "openingContents": {
          "lot": "oil-4",
          "pints": 1
        },
        "location": "Cart-1",
        "retainedWhenEmpty": true,
        "cleanAndCompatible": true
      },
      {
        "id": "flask-5",
        "emptyMassLb": {
          "numerator": 1,
          "denominator": 4
        },
        "capacityPints": 1,
        "openingContents": {
          "lot": "oil-5",
          "pints": 1
        },
        "location": "Cart-1",
        "retainedWhenEmpty": true,
        "cleanAndCompatible": true
      },
      {
        "id": "flask-6",
        "emptyMassLb": {
          "numerator": 1,
          "denominator": 4
        },
        "capacityPints": 1,
        "openingContents": {
          "lot": "oil-6",
          "pints": 1
        },
        "location": "Cart-1",
        "retainedWhenEmpty": true,
        "cleanAndCompatible": true
      },
      {
        "id": "flask-7",
        "emptyMassLb": {
          "numerator": 1,
          "denominator": 4
        },
        "capacityPints": 1,
        "openingContents": {
          "lot": "oil-7",
          "pints": 1
        },
        "location": "Cart-1",
        "retainedWhenEmpty": true,
        "cleanAndCompatible": true
      },
      {
        "id": "flask-8",
        "emptyMassLb": {
          "numerator": 1,
          "denominator": 4
        },
        "capacityPints": 1,
        "openingContents": {
          "lot": "oil-8",
          "pints": 1
        },
        "location": "Cart-1",
        "retainedWhenEmpty": true,
        "cleanAndCompatible": true
      },
      {
        "id": "feedbag-1",
        "emptyMassLb": 1,
        "capacityLb": 10,
        "openingContents": {
          "lot": "feed-0",
          "lb": 10
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true
      },
      {
        "id": "feedbag-2",
        "emptyMassLb": 1,
        "capacityLb": 10,
        "openingContents": {
          "lot": "feed-0",
          "lb": 10
        },
        "location": "Cart-1",
        "ownedBeforeEpisode": true
      }
    ],
    "originRestrictions": "Ordinary purchased stock only; no new magical, harvest or crafting output",
    "allocation": [
      {
        "id": "meal-Arin-0-food",
        "lotId": "food-0",
        "recipient": "Arin",
        "interval": {
          "startSeconds": 86400,
          "endSeconds": 87300,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 0,
        "relativeEnd": 900,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Arin-0-water",
        "lotId": "water-human-0",
        "recipient": "Arin",
        "interval": {
          "startSeconds": 86400,
          "endSeconds": 87300,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 0,
        "relativeEnd": 900,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Arin-1-food",
        "lotId": "food-0",
        "recipient": "Arin",
        "interval": {
          "startSeconds": 129720,
          "endSeconds": 130620,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 43320,
        "relativeEnd": 44220,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Arin-1-water",
        "lotId": "water-human-0",
        "recipient": "Arin",
        "interval": {
          "startSeconds": 129720,
          "endSeconds": 130620,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 43320,
        "relativeEnd": 44220,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Arin-2-food",
        "lotId": "food-0",
        "recipient": "Arin",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Arin-2-water",
        "lotId": "water-human-0",
        "recipient": "Arin",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Arin-3-food",
        "lotId": "food-0",
        "recipient": "Arin",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Arin-3-water",
        "lotId": "water-human-0",
        "recipient": "Arin",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Bea-0-food",
        "lotId": "food-0",
        "recipient": "Bea",
        "interval": {
          "startSeconds": 86400,
          "endSeconds": 87300,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 0,
        "relativeEnd": 900,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Bea-0-water",
        "lotId": "water-human-0",
        "recipient": "Bea",
        "interval": {
          "startSeconds": 86400,
          "endSeconds": 87300,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 0,
        "relativeEnd": 900,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Bea-1-food",
        "lotId": "food-0",
        "recipient": "Bea",
        "interval": {
          "startSeconds": 129600,
          "endSeconds": 130500,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 43200,
        "relativeEnd": 44100,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Bea-1-water",
        "lotId": "water-human-0",
        "recipient": "Bea",
        "interval": {
          "startSeconds": 129600,
          "endSeconds": 130500,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 43200,
        "relativeEnd": 44100,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Bea-2-food",
        "lotId": "food-0",
        "recipient": "Bea",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Bea-2-water",
        "lotId": "water-human-0",
        "recipient": "Bea",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Bea-3-food",
        "lotId": "food-0",
        "recipient": "Bea",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Bea-3-water",
        "lotId": "water-human-0",
        "recipient": "Bea",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Cora-0-food",
        "lotId": "food-0",
        "recipient": "Cora",
        "interval": {
          "startSeconds": 86400,
          "endSeconds": 87300,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 0,
        "relativeEnd": 900,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Cora-0-water",
        "lotId": "water-human-0",
        "recipient": "Cora",
        "interval": {
          "startSeconds": 86400,
          "endSeconds": 87300,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 0,
        "relativeEnd": 900,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Cora-1-food",
        "lotId": "food-0",
        "recipient": "Cora",
        "interval": {
          "startSeconds": 129720,
          "endSeconds": 130620,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 43320,
        "relativeEnd": 44220,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Cora-1-water",
        "lotId": "water-human-0",
        "recipient": "Cora",
        "interval": {
          "startSeconds": 129720,
          "endSeconds": 130620,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 43320,
        "relativeEnd": 44220,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Cora-2-food",
        "lotId": "food-0",
        "recipient": "Cora",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Cora-2-water",
        "lotId": "water-human-0",
        "recipient": "Cora",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Cora-3-food",
        "lotId": "food-0",
        "recipient": "Cora",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Cora-3-water",
        "lotId": "water-human-0",
        "recipient": "Cora",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Dane-0-food",
        "lotId": "food-0",
        "recipient": "Dane",
        "interval": {
          "startSeconds": 86400,
          "endSeconds": 87300,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 0,
        "relativeEnd": 900,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Dane-0-water",
        "lotId": "water-human-0",
        "recipient": "Dane",
        "interval": {
          "startSeconds": 86400,
          "endSeconds": 87300,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 0,
        "relativeEnd": 900,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Dane-1-food",
        "lotId": "food-0",
        "recipient": "Dane",
        "interval": {
          "startSeconds": 129600,
          "endSeconds": 130500,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 43200,
        "relativeEnd": 44100,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Dane-1-water",
        "lotId": "water-human-0",
        "recipient": "Dane",
        "interval": {
          "startSeconds": 129600,
          "endSeconds": 130500,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 43200,
        "relativeEnd": 44100,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Dane-2-food",
        "lotId": "food-0",
        "recipient": "Dane",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Dane-2-water",
        "lotId": "water-human-0",
        "recipient": "Dane",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Dane-3-food",
        "lotId": "food-0",
        "recipient": "Dane",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 1,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "meal-Dane-3-water",
        "lotId": "water-human-0",
        "recipient": "Dane",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 4,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "mule-meal-0-feed",
        "lotId": "feed-0",
        "recipient": "Mule-1",
        "interval": {
          "startSeconds": 87300,
          "endSeconds": 88200,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 900,
        "relativeEnd": 1800,
        "amount": {
          "numerator": 5,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "mule-meal-0-water",
        "lotId": "water-mule-0",
        "recipient": "Mule-1",
        "interval": {
          "startSeconds": 87300,
          "endSeconds": 88200,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 900,
        "relativeEnd": 1800,
        "amount": {
          "numerator": 12,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "mule-meal-1-feed",
        "lotId": "feed-0",
        "recipient": "Mule-1",
        "interval": {
          "startSeconds": 130500,
          "endSeconds": 131400,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 44100,
        "relativeEnd": 45000,
        "amount": {
          "numerator": 5,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "mule-meal-1-water",
        "lotId": "water-mule-0",
        "recipient": "Mule-1",
        "interval": {
          "startSeconds": 130500,
          "endSeconds": 131400,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 44100,
        "relativeEnd": 45000,
        "amount": {
          "numerator": 12,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "mule-meal-2-feed",
        "lotId": "feed-0",
        "recipient": "Mule-1",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 5,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "mule-meal-2-water",
        "lotId": "water-mule-0",
        "recipient": "Mule-1",
        "interval": {
          "startSeconds": 172800,
          "endSeconds": 173700,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 86400,
        "relativeEnd": 87300,
        "amount": {
          "numerator": 12,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "mule-meal-3-feed",
        "lotId": "feed-0",
        "recipient": "Mule-1",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 5,
          "denominator": 1
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "mule-meal-3-water",
        "lotId": "water-mule-0",
        "recipient": "Mule-1",
        "interval": {
          "startSeconds": 216000,
          "endSeconds": 216900,
          "activeSeconds": 900,
          "halfOpen": true
        },
        "relativeStart": 129600,
        "relativeEnd": 130500,
        "amount": {
          "numerator": 12,
          "denominator": 1
        },
        "unit": "pint",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": true
      },
      {
        "id": "cleaning-0",
        "lotId": "sundries-0",
        "recipient": "Expedition shared cleanup",
        "interval": {
          "startSeconds": 87300,
          "endSeconds": 87360,
          "activeSeconds": 60,
          "halfOpen": true
        },
        "relativeStart": 900,
        "relativeEnd": 960,
        "amount": {
          "numerator": 1,
          "denominator": 2
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": false
      },
      {
        "id": "cleaning-1",
        "lotId": "sundries-0",
        "recipient": "Expedition shared cleanup",
        "interval": {
          "startSeconds": 130620,
          "endSeconds": 130680,
          "activeSeconds": 60,
          "halfOpen": true
        },
        "relativeStart": 44220,
        "relativeEnd": 44280,
        "amount": {
          "numerator": 1,
          "denominator": 2
        },
        "unit": "lb",
        "canonicalRelativeDay": 0,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": false
      },
      {
        "id": "cleaning-2",
        "lotId": "sundries-0",
        "recipient": "Expedition shared cleanup",
        "interval": {
          "startSeconds": 173700,
          "endSeconds": 173760,
          "activeSeconds": 60,
          "halfOpen": true
        },
        "relativeStart": 87300,
        "relativeEnd": 87360,
        "amount": {
          "numerator": 1,
          "denominator": 2
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": false
      },
      {
        "id": "cleaning-3",
        "lotId": "sundries-0",
        "recipient": "Expedition shared cleanup",
        "interval": {
          "startSeconds": 216900,
          "endSeconds": 216960,
          "activeSeconds": 60,
          "halfOpen": true
        },
        "relativeStart": 130500,
        "relativeEnd": 130560,
        "amount": {
          "numerator": 1,
          "denominator": 2
        },
        "unit": "lb",
        "canonicalRelativeDay": 1,
        "evidence": "authored actual supported interval",
        "creditsNutritionOnce": false
      }
    ],
    "dailyDemand": {
      "humanEach": {
        "foodLb": 2,
        "waterPints": 8
      },
      "Mule-1": {
        "feedLb": 10,
        "waterPints": 24
      }
    },
    "support": {
      "burns": [
        {
          "id": "burn-A-1",
          "lantern": "Lantern-A",
          "lotId": "oil-1",
          "relativeStart": 0,
          "relativeEnd": 21600,
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 108000,
            "activeSeconds": 21600,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 1
          },
          "lightCoverage": "declared safe occupied area and route, not unlimited radius"
        },
        {
          "id": "burn-B-1",
          "lantern": "Lantern-B",
          "lotId": "oil-8",
          "relativeStart": 21600,
          "relativeEnd": 21660,
          "interval": {
            "startSeconds": 108000,
            "endSeconds": 108060,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 360
          },
          "lightCoverage": "same supported area for this minute"
        },
        {
          "id": "burn-A-2",
          "lantern": "Lantern-A",
          "lotId": "oil-2",
          "relativeStart": 21660,
          "relativeEnd": 43260,
          "interval": {
            "startSeconds": 108060,
            "endSeconds": 129660,
            "activeSeconds": 21600,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 1
          },
          "lightCoverage": "declared safe occupied area and route, not unlimited radius"
        },
        {
          "id": "burn-B-2",
          "lantern": "Lantern-B",
          "lotId": "oil-8",
          "relativeStart": 43260,
          "relativeEnd": 43320,
          "interval": {
            "startSeconds": 129660,
            "endSeconds": 129720,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 360
          },
          "lightCoverage": "same supported area for this minute"
        },
        {
          "id": "burn-A-3",
          "lantern": "Lantern-A",
          "lotId": "oil-3",
          "relativeStart": 43320,
          "relativeEnd": 64920,
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 151320,
            "activeSeconds": 21600,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 1
          },
          "lightCoverage": "declared safe occupied area and route, not unlimited radius"
        },
        {
          "id": "burn-B-3",
          "lantern": "Lantern-B",
          "lotId": "oil-8",
          "relativeStart": 64920,
          "relativeEnd": 64980,
          "interval": {
            "startSeconds": 151320,
            "endSeconds": 151380,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 360
          },
          "lightCoverage": "same supported area for this minute"
        },
        {
          "id": "burn-A-4",
          "lantern": "Lantern-A",
          "lotId": "oil-4",
          "relativeStart": 64980,
          "relativeEnd": 86580,
          "interval": {
            "startSeconds": 151380,
            "endSeconds": 172980,
            "activeSeconds": 21600,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 1
          },
          "lightCoverage": "declared safe occupied area and route, not unlimited radius"
        },
        {
          "id": "burn-B-4",
          "lantern": "Lantern-B",
          "lotId": "oil-8",
          "relativeStart": 86580,
          "relativeEnd": 86640,
          "interval": {
            "startSeconds": 172980,
            "endSeconds": 173040,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 360
          },
          "lightCoverage": "same supported area for this minute"
        },
        {
          "id": "burn-A-5",
          "lantern": "Lantern-A",
          "lotId": "oil-5",
          "relativeStart": 86640,
          "relativeEnd": 108240,
          "interval": {
            "startSeconds": 173040,
            "endSeconds": 194640,
            "activeSeconds": 21600,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 1
          },
          "lightCoverage": "declared safe occupied area and route, not unlimited radius"
        },
        {
          "id": "burn-B-5",
          "lantern": "Lantern-B",
          "lotId": "oil-8",
          "relativeStart": 108240,
          "relativeEnd": 108300,
          "interval": {
            "startSeconds": 194640,
            "endSeconds": 194700,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 360
          },
          "lightCoverage": "same supported area for this minute"
        },
        {
          "id": "burn-A-6",
          "lantern": "Lantern-A",
          "lotId": "oil-6",
          "relativeStart": 108300,
          "relativeEnd": 129900,
          "interval": {
            "startSeconds": 194700,
            "endSeconds": 216300,
            "activeSeconds": 21600,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 1
          },
          "lightCoverage": "declared safe occupied area and route, not unlimited radius"
        },
        {
          "id": "burn-B-6",
          "lantern": "Lantern-B",
          "lotId": "oil-8",
          "relativeStart": 129900,
          "relativeEnd": 129960,
          "interval": {
            "startSeconds": 216300,
            "endSeconds": 216360,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 360
          },
          "lightCoverage": "same supported area for this minute"
        },
        {
          "id": "burn-A-7",
          "lantern": "Lantern-A",
          "lotId": "oil-7",
          "relativeStart": 129960,
          "relativeEnd": 151560,
          "interval": {
            "startSeconds": 216360,
            "endSeconds": 237960,
            "activeSeconds": 21600,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 1
          },
          "lightCoverage": "declared safe occupied area and route, not unlimited radius"
        },
        {
          "id": "burn-B-7",
          "lantern": "Lantern-B",
          "lotId": "oil-8",
          "relativeStart": 151560,
          "relativeEnd": 151620,
          "interval": {
            "startSeconds": 237960,
            "endSeconds": 238020,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "pints": {
            "numerator": 1,
            "denominator": 360
          },
          "lightCoverage": "same supported area for this minute"
        },
        {
          "id": "burn-A-8",
          "lantern": "Lantern-A",
          "lotId": "oil-8",
          "relativeStart": 151620,
          "relativeEnd": 172800,
          "interval": {
            "startSeconds": 238020,
            "endSeconds": 259200,
            "activeSeconds": 21180,
            "halfOpen": true
          },
          "pints": {
            "numerator": 353,
            "denominator": 360
          },
          "lightCoverage": "declared safe occupied area and route, not unlimited radius"
        }
      ],
      "refills": [
        {
          "id": "refill-1",
          "interval": {
            "startSeconds": 108000,
            "endSeconds": 108060,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 21600,
          "relativeEnd": 21660,
          "mainWorker": "Arin",
          "backupWorker": "Cora",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 60,
          "reason": "Independent route pause"
        },
        {
          "id": "refill-2",
          "interval": {
            "startSeconds": 129660,
            "endSeconds": 129720,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 43260,
          "relativeEnd": 43320,
          "mainWorker": "Arin",
          "backupWorker": "Cora",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Inside the existing meal stop"
        },
        {
          "id": "refill-3",
          "interval": {
            "startSeconds": 151320,
            "endSeconds": 151380,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 64920,
          "relativeEnd": 64980,
          "mainWorker": "Iris",
          "backupWorker": "June",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        },
        {
          "id": "refill-4",
          "interval": {
            "startSeconds": 172980,
            "endSeconds": 173040,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 86580,
          "relativeEnd": 86640,
          "mainWorker": "Iris",
          "backupWorker": "June",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        },
        {
          "id": "refill-5",
          "interval": {
            "startSeconds": 194640,
            "endSeconds": 194700,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 108240,
          "relativeEnd": 108300,
          "mainWorker": "Iris",
          "backupWorker": "June",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        },
        {
          "id": "refill-6",
          "interval": {
            "startSeconds": 216300,
            "endSeconds": 216360,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 129900,
          "relativeEnd": 129960,
          "mainWorker": "Leto",
          "backupWorker": "Mara",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        },
        {
          "id": "refill-7",
          "interval": {
            "startSeconds": 237960,
            "endSeconds": 238020,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 151560,
          "relativeEnd": 151620,
          "mainWorker": "Leto",
          "backupWorker": "Mara",
          "hands": {
            "mainWorker": 2,
            "backupWorker": 1
          },
          "method": "Extinguish empty A; B supplies light while the actual worker opens, pours and secures the next real flask. Return empty flask to the original container register.",
          "travelPauseAddedSeconds": 0,
          "reason": "Actual Haven provider work; no travel underway"
        }
      ],
      "transfers": [
        {
          "id": "initial-A",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 56400,
            "departurePreparationOffsetSeconds": -30000
          },
          "from": "flask-1",
          "to": "Lantern-A",
          "lotId": "oil-1",
          "pints": {
            "numerator": 1,
            "denominator": 1
          }
        },
        {
          "id": "initial-B",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 56460,
            "departurePreparationOffsetSeconds": -29940
          },
          "from": "flask-8",
          "to": "Lantern-B",
          "lotId": "oil-8",
          "pints": {
            "numerator": 7,
            "denominator": 360
          }
        },
        {
          "id": "pour-A-1",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 108060,
            "departurePreparationOffsetSeconds": 21660
          },
          "from": "flask-2",
          "to": "Lantern-A",
          "lotId": "oil-2",
          "pints": {
            "numerator": 1,
            "denominator": 1
          }
        },
        {
          "id": "pour-A-2",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 129720,
            "departurePreparationOffsetSeconds": 43320
          },
          "from": "flask-3",
          "to": "Lantern-A",
          "lotId": "oil-3",
          "pints": {
            "numerator": 1,
            "denominator": 1
          }
        },
        {
          "id": "pour-A-3",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 151380,
            "departurePreparationOffsetSeconds": 64980
          },
          "from": "flask-4",
          "to": "Lantern-A",
          "lotId": "oil-4",
          "pints": {
            "numerator": 1,
            "denominator": 1
          }
        },
        {
          "id": "pour-A-4",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 173040,
            "departurePreparationOffsetSeconds": 86640
          },
          "from": "flask-5",
          "to": "Lantern-A",
          "lotId": "oil-5",
          "pints": {
            "numerator": 1,
            "denominator": 1
          }
        },
        {
          "id": "pour-A-5",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 194700,
            "departurePreparationOffsetSeconds": 108300
          },
          "from": "flask-6",
          "to": "Lantern-A",
          "lotId": "oil-6",
          "pints": {
            "numerator": 1,
            "denominator": 1
          }
        },
        {
          "id": "pour-A-6",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 216360,
            "departurePreparationOffsetSeconds": 129960
          },
          "from": "flask-7",
          "to": "Lantern-A",
          "lotId": "oil-7",
          "pints": {
            "numerator": 1,
            "denominator": 1
          }
        },
        {
          "id": "pour-A-7",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 238020,
            "departurePreparationOffsetSeconds": 151620
          },
          "from": "flask-8",
          "to": "Lantern-A",
          "lotId": "oil-8",
          "pints": {
            "numerator": 353,
            "denominator": 360
          }
        }
      ],
      "rate": "1 pint per 21600 actual lit seconds",
      "noFreeBackupFuel": true,
      "totalOriginalOilPints": {
        "numerator": 8,
        "denominator": 1
      },
      "totalEmptyFlaskMassLb": {
        "numerator": 2,
        "denominator": 1
      },
      "nextOilPreparation": {
        "interval": {
          "startSeconds": 238020,
          "endSeconds": 238080,
          "activeSeconds": 60,
          "halfOpen": true
        },
        "actor": "Mara",
        "from": "next-flask-1",
        "to": "Lantern-B",
        "pints": {
          "numerator": 1,
          "denominator": 1
        },
        "lotId": "oil-next-1",
        "ignitionAt": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 259200,
          "departurePreparationOffsetSeconds": 172800
        },
        "oldBurnsUnchanged": true,
        "costIncludedInNextProcurement": true
      }
    }
  }
}
```

### EC-04 — Opportunity and camp

```json
{
  "id": "FLOW-EC-04",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-04",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "opportunityId": {
      "applicable": false,
      "reason": "No forage or camp construction is performed"
    },
    "ordinaryAllocation": [],
    "site": {
      "rooms": {
        "id": "ROOM-1",
        "owner": "Sera",
        "recipients": [
          "Arin",
          "Bea",
          "Cora",
          "Dane"
        ],
        "term": {
          "startSeconds": 148992,
          "endSeconds": 264192,
          "activeSeconds": 115200,
          "halfOpen": true
        },
        "priceCp": 800,
        "realFacilities": [
          "four safe beds",
          "secure dry gear storage",
          "potable-service access"
        ],
        "includedWork": "Staff keep the party-owned lamps fueled using party-owned finite oil; no new party provisions or training credit."
      },
      "stable": {
        "id": "STABLE-1",
        "owner": "Toma",
        "animal": "Mule-1",
        "term": {
          "startSeconds": 148992,
          "endSeconds": 321792,
          "activeSeconds": 172800,
          "halfOpen": true
        },
        "priceCp": 100,
        "facilities": "fitting Large stall, safe water/feed access, actual staff",
        "partyStockUsed": true,
        "automaticHealing": false
      },
      "lampShifts": [
        {
          "actors": [
            "Iris",
            "June"
          ],
          "interval": {
            "startSeconds": 148992,
            "endSeconds": 201600,
            "activeSeconds": 52608,
            "halfOpen": true
          }
        },
        {
          "actors": [
            "Leto",
            "Mara"
          ],
          "interval": {
            "startSeconds": 201600,
            "endSeconds": 259200,
            "activeSeconds": 57600,
            "halfOpen": true
          }
        },
        {
          "actors": [
            "Iris",
            "June"
          ],
          "interval": {
            "startSeconds": 259200,
            "endSeconds": 264192,
            "activeSeconds": 4992,
            "halfOpen": true
          }
        }
      ],
      "providerRest": [
        {
          "actors": [
            "Iris",
            "June"
          ],
          "interval": {
            "startSeconds": 201600,
            "endSeconds": 230400,
            "activeSeconds": 28800,
            "halfOpen": true
          }
        },
        {
          "actors": [
            "Leto",
            "Mara"
          ],
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 201600,
            "activeSeconds": 28800,
            "halfOpen": true
          }
        }
      ],
      "muleCare": [
        {
          "actor": "Nell",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          }
        },
        {
          "actor": "Orin",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          }
        }
      ],
      "authority": "All provider bodies, own support, wages, permissions and facility capacities are explicit synthetic premises. A payment alone is not used as proof of a worker.",
      "externalNotRoster": true
    },
    "campTierAndMarks": {
      "applicable": false
    },
    "materialBill": [],
    "functionalFacts": "Actual contracted Haven beds/stall, not a camp-tier benefit",
    "storage": "Rooms and stall physically fit listed occupants and gear",
    "supplyLine": {
      "applicable": false
    }
  }
}
```

### EC-05 — Route and travel tranche

```json
{
  "id": "FLOW-EC-05",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-05",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "routeId": "route-known-1",
    "lengthProgress": 2,
    "riskMappingQuality": {
      "Risk": 1,
      "Mapping": "Mapped",
      "routeQuality": "Known",
      "qualityFactor": {
        "numerator": 1,
        "denominator": 1
      }
    },
    "capacityAndAccess": {
      "capacityLoad": {
        "numerator": 60,
        "denominator": 1
      },
      "capacityConvention": "This fixture counts freight, personal gear, empty frame and harness once. Self-moving bodies use separate floor/bridge support facts, not passenger burden.",
      "support": {
        "combinedSelfMovingBodiesLb": 1000,
        "freightUpperBoundLb": 512,
        "continuousSupportedFloorRatingLb": 2000,
        "minimumWidthFt": 12,
        "minimumHeightFt": 12,
        "terrain": "firm level rolling surface; no gap, stairs, slope or closed obstacle",
        "turns": "straight lane or actual swept turning areas at least 30 by 30 feet"
      }
    },
    "pace": {
      "charactersFt": 30,
      "muleBaseFt": 40,
      "drawBurdenPenaltyFt": 10,
      "currentMuleFt": 30,
      "cartCapFt": 40,
      "convoyMph": 3,
      "nominalSecondsEachDirection": 28800,
      "movingSecondsEachDirection": 28800
    },
    "tranche": [
      {
        "startSeconds": 88200,
        "endSeconds": 108000,
        "activeSeconds": 19800,
        "halfOpen": true
      },
      {
        "startSeconds": 108060,
        "endSeconds": 117060,
        "activeSeconds": 9000,
        "halfOpen": true
      },
      {
        "startSeconds": 118332,
        "endSeconds": 129600,
        "activeSeconds": 11268,
        "halfOpen": true
      },
      {
        "startSeconds": 131400,
        "endSeconds": 148932,
        "activeSeconds": 17532,
        "halfOpen": true
      }
    ],
    "mappingAndRecon": "Existing genuine mapped route, no new Recon bonus",
    "forcedMarch": {
      "performed": false
    },
    "result": {
      "outboundProgress": 2,
      "returnProgress": 2,
      "HavenEntry": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 148992,
        "departurePreparationOffsetSeconds": 62592
      }
    }
  }
}
```

### EC-06 — Pressure, complications and extraction queue

```json
{
  "id": "FLOW-EC-06",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-06",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "cohortId": "Expedition-1 together",
    "pressure": [
      {
        "id": "initial-risk",
        "relativeTime": 0,
        "before": 0,
        "delta": 1,
        "after": 1,
        "cause": "actual Risk 1 floor"
      },
      {
        "id": "class-highwater",
        "relativeTime": 31860,
        "before": 1,
        "delta": 1,
        "after": 2,
        "cause": "Class 2 extraction first surcharge",
        "highwater": 1
      },
      {
        "id": "successful-retreat",
        "relativeTime": 31872,
        "before": 2,
        "delta": 1,
        "after": 3,
        "cause": "successful retreat once"
      },
      {
        "id": "watch1-open-combat",
        "relativeTime": 57600,
        "before": 3,
        "delta": 1,
        "after": 4,
        "cause": "one open combat category, both rounds same Watch"
      },
      {
        "id": "actual-secured-entry",
        "relativeTime": 62592,
        "before": 4,
        "delta": -1,
        "after": 3,
        "cause": "move onto genuinely secured route",
        "WatchReductionCreditsUsed": 1
      }
    ],
    "causeEvents": [
      "initial-risk",
      "class-highwater",
      "successful-retreat",
      "watch1-open-combat",
      "actual-secured-entry"
    ],
    "extractionEpisode": {
      "id": "extract-1",
      "start": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 118260,
        "departurePreparationOffsetSeconds": 31860
      },
      "destination": "Haven inspection point",
      "crate": {
        "id": "crate-1",
        "massLb": 20,
        "Load": {
          "numerator": 2,
          "denominator": 1
        },
        "outerFeet": [
          2,
          1,
          1
        ],
        "Class": 2,
        "priority": 1,
        "tags": [],
        "closed": true,
        "condition": "unchanged sound ordinary material",
        "title": "licensed assignment verified from actual stipulated release record",
        "custody": [
          {
            "from": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 118260,
              "departurePreparationOffsetSeconds": 31860
            },
            "to": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 118332,
              "departurePreparationOffsetSeconds": 31932
            },
            "custodian": "Dane"
          },
          {
            "from": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 118332,
              "departurePreparationOffsetSeconds": 31932
            },
            "to": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 155592,
              "departurePreparationOffsetSeconds": 69192
            },
            "custodian": "Expedition in Cart-1"
          },
          {
            "from": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 155592,
              "departurePreparationOffsetSeconds": 69192
            },
            "custodian": "Pera, actual paid buyer"
          }
        ]
      },
      "surchargeHighwater": 1,
      "checkpoints": [
        {
          "id": "route-known-return-exit",
          "position": {
            "numerator": 2,
            "denominator": 1
          },
          "interval": {
            "startSeconds": 148932,
            "endSeconds": 148992,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "actor": "Arin",
          "nativeRoute": "Core fixed DC task",
          "DCInputs": {
            "tier": 13,
            "Class": 2,
            "Attention": 0,
            "Burden": 1,
            "unsecuredDangerous": 0,
            "pursuit": 0,
            "Secured": 0
          },
          "DC": 16,
          "natural": 11,
          "modifier": 5,
          "total": 16,
          "degree": "Success",
          "processedCount": 1,
          "cargoLoss": [],
          "addedPressure": 0
        }
      ],
      "pendingQueue": [],
      "terminal": "arrived with crate, closed once"
    },
    "checkpoints": [
      {
        "id": "route-known-return-exit",
        "position": {
          "numerator": 2,
          "denominator": 1
        },
        "interval": {
          "startSeconds": 148932,
          "endSeconds": 148992,
          "activeSeconds": 60,
          "halfOpen": true
        },
        "actor": "Arin",
        "nativeRoute": "Core fixed DC task",
        "DCInputs": {
          "tier": 13,
          "Class": 2,
          "Attention": 0,
          "Burden": 1,
          "unsecuredDangerous": 0,
          "pursuit": 0,
          "Secured": 0
        },
        "DC": 16,
        "natural": 11,
        "modifier": 5,
        "total": 16,
        "degree": "Success",
        "processedCount": 1,
        "cargoLoss": [],
        "addedPressure": 0
      }
    ],
    "test": {
      "id": "route-known-return-exit",
      "position": {
        "numerator": 2,
        "denominator": 1
      },
      "interval": {
        "startSeconds": 148932,
        "endSeconds": 148992,
        "activeSeconds": 60,
        "halfOpen": true
      },
      "actor": "Arin",
      "nativeRoute": "Core fixed DC task",
      "DCInputs": {
        "tier": 13,
        "Class": 2,
        "Attention": 0,
        "Burden": 1,
        "unsecuredDangerous": 0,
        "pursuit": 0,
        "Secured": 0
      },
      "DC": 16,
      "natural": 11,
      "modifier": 5,
      "total": 16,
      "degree": "Success",
      "processedCount": 1,
      "cargoLoss": [],
      "addedPressure": 0
    },
    "complication": [
      {
        "id": "watch0",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 115200,
          "departurePreparationOffsetSeconds": 28800
        },
        "Pressure": 1,
        "naturalD6": 5,
        "result": "none"
      },
      {
        "id": "watch1",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 144000,
          "departurePreparationOffsetSeconds": 57600
        },
        "Pressure": 4,
        "naturalD6": 5,
        "result": "none"
      },
      {
        "id": "partial-watch2",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 148992,
          "departurePreparationOffsetSeconds": 62592
        },
        "Pressure": 4,
        "naturalD6": 6,
        "result": "none",
        "phase": "before secured-entry reduction",
        "laterWatch2Repeat": false
      }
    ],
    "response": "No complication triggered; no invented delay/loss",
    "queue": []
  }
}
```

### EC-07 — Encounter participants and retreat

```json
{
  "id": "FLOW-EC-07",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-07",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "encounterId": "retreat-1",
    "participants": [
      "Arin",
      "Bea",
      "Cora",
      "Dane",
      "Mule-1",
      "Opponent-1"
    ],
    "estimate": {
      "status": "authored bounded attack context only; not a calibrated full enemy build",
      "actualCharacters": 4,
      "characterLevels": [
        3,
        3,
        3,
        3
      ],
      "absentRosterMembers": 0,
      "opponentCR": {
        "presence": "absent"
      },
      "separateCalibrationBoundariesStillRequired": true
    },
    "retreat": {
      "lengthFt": 60,
      "minimumWidthFt": 12,
      "startingPositions": "all withdrawing bodies and whole cart can clear the real gate after two 30-foot coherent movements",
      "gate": "actual manual lever next to Cora at final position; closes after the second opposing attack; no new magical barrier",
      "actualChamberWidthFt": 20,
      "gatePlaneXFt": 35,
      "gateLeverPointFt": [
        39,
        {
          "numerator": 35,
          "denominator": 2
        }
      ],
      "startingRectanglesFt": {
        "Cart-1": {
          "x": [
            -23,
            -15
          ],
          "y": [
            {
              "numerator": 15,
              "denominator": 2
            },
            {
              "numerator": 25,
              "denominator": 2
            }
          ]
        },
        "Mule-1": {
          "x": [
            -10,
            0
          ],
          "y": [
            5,
            15
          ]
        },
        "harness-gap": {
          "x": [
            -15,
            -10
          ],
          "y": [
            9,
            11
          ]
        },
        "Arin": {
          "x": [
            -25,
            -20
          ],
          "y": [
            0,
            5
          ]
        },
        "Bea": {
          "x": [
            -20,
            -15
          ],
          "y": [
            {
              "numerator": 25,
              "denominator": 2
            },
            {
              "numerator": 35,
              "denominator": 2
            }
          ]
        },
        "Cora": {
          "x": [
            -25,
            -20
          ],
          "y": [
            15,
            20
          ]
        },
        "Dane": {
          "x": [
            -20,
            -15
          ],
          "y": [
            0,
            5
          ]
        },
        "Opponent-1": {
          "x": [
            -30,
            -25
          ],
          "y": [
            0,
            5
          ]
        }
      },
      "geometryMeaning": "Actual authored rectangles in feet. Each actor advances 30 feet per round; the harness and cart translate with the mule. Side lanes keep walkers clear of the vehicle and puller. Gate closure at x=35 separates the opponent from the whole friendly convoy after round 2.",
      "opponentContext": {
        "walkingSpeedFt": 30,
        "attackBonus": 3,
        "reachFt": 5,
        "ActionsPerRound": 1,
        "opportunityAttacksTaken": 0,
        "singleThreatChoice": "Opponent uses its predeclared one attack on its regular turn, declining extra opportunity attacks. No second abstract threat is imposed."
      }
    },
    "roundBudgets": [
      {
        "round": 1,
        "interval": {
          "startSeconds": 118260,
          "endSeconds": 118266,
          "activeSeconds": 6,
          "halfOpen": true
        },
        "initiative": [
          "Arin",
          "Bea",
          "Mule-1",
          "Cora",
          "Dane",
          "Opponent-1"
        ],
        "driverContributionReservedBeforeMule": true,
        "drive": {
          "id": "drive-1",
          "mover": "Mule-1",
          "carrier": "Cart-1",
          "initiator": "Bea",
          "distanceFt": 30,
          "selfPowered": true,
          "pullerMoveSpentFt": 30,
          "pullerAction": "Dodge",
          "resolvesAfterRequiredContributions": true,
          "vehicleDriveCount": 1
        },
        "actorBudgets": {
          "Arin": {
            "stance": "Mobile",
            "movementSpentFt": 30,
            "ActionSpent": true,
            "BonusActionSpent": false,
            "ReactionSpent": false,
            "Action": "one escape check while carrying A in the other available hand"
          },
          "Bea": {
            "stance": "Mobile",
            "movementSpentFt": 30,
            "ActionSpent": true,
            "BonusActionSpent": false,
            "ReactionSpent": false,
            "Action": "driver command/brake contribution; walks with reins, no cart seat"
          },
          "Cora": {
            "stance": "Mobile",
            "movementSpentFt": 30,
            "ActionSpent": true,
            "BonusActionSpent": false,
            "ReactionSpent": false,
            "Action": "Dodge"
          },
          "Dane": {
            "stance": "Mobile",
            "movementSpentFt": 30,
            "ActionSpent": true,
            "BonusActionSpent": false,
            "ReactionSpent": false,
            "Action": "Dodge while carrying crate in both hands; no weapon attack"
          }
        },
        "leadDie": 11,
        "leadTotal": 16,
        "numericalDegree": "Success",
        "naturalShift": "none",
        "EscapeAdded": 1,
        "PursuitAdded": 0,
        "threat": {
          "actor": "Opponent-1",
          "attackBonus": 3,
          "naturalDie": 2,
          "total": 5,
          "target": "Arin",
          "AC": 13,
          "nativeResult": "miss",
          "actualReachFt": 5,
          "actualTargetDistanceFt": 5,
          "movementAvailableFt": 30,
          "damage": 0,
          "otherThreats": 0
        },
        "otherGenericEscapeAwards": 0,
        "endingRectanglesFt": {
          "Cart-1": {
            "x": [
              7,
              15
            ],
            "y": [
              {
                "numerator": 15,
                "denominator": 2
              },
              {
                "numerator": 25,
                "denominator": 2
              }
            ]
          },
          "Mule-1": {
            "x": [
              20,
              30
            ],
            "y": [
              5,
              15
            ]
          },
          "harness-gap": {
            "x": [
              15,
              20
            ],
            "y": [
              9,
              11
            ]
          },
          "Arin": {
            "x": [
              5,
              10
            ],
            "y": [
              0,
              5
            ]
          },
          "Bea": {
            "x": [
              10,
              15
            ],
            "y": [
              {
                "numerator": 25,
                "denominator": 2
              },
              {
                "numerator": 35,
                "denominator": 2
              }
            ]
          },
          "Cora": {
            "x": [
              5,
              10
            ],
            "y": [
              15,
              20
            ]
          },
          "Dane": {
            "x": [
              10,
              15
            ],
            "y": [
              0,
              5
            ]
          },
          "Opponent-1": {
            "x": [
              0,
              5
            ],
            "y": [
              0,
              5
            ]
          }
        }
      },
      {
        "round": 2,
        "interval": {
          "startSeconds": 118266,
          "endSeconds": 118272,
          "activeSeconds": 6,
          "halfOpen": true
        },
        "initiative": [
          "Arin",
          "Bea",
          "Mule-1",
          "Cora",
          "Dane",
          "Opponent-1"
        ],
        "driverContributionReservedBeforeMule": true,
        "drive": {
          "id": "drive-2",
          "mover": "Mule-1",
          "carrier": "Cart-1",
          "initiator": "Bea",
          "distanceFt": 30,
          "selfPowered": true,
          "pullerMoveSpentFt": 30,
          "pullerAction": "Dodge",
          "resolvesAfterRequiredContributions": true,
          "vehicleDriveCount": 1
        },
        "actorBudgets": {
          "Arin": {
            "stance": "Mobile",
            "movementSpentFt": 30,
            "ActionSpent": true,
            "BonusActionSpent": false,
            "ReactionSpent": false,
            "Action": "one escape check while carrying A in the other available hand"
          },
          "Bea": {
            "stance": "Mobile",
            "movementSpentFt": 30,
            "ActionSpent": true,
            "BonusActionSpent": false,
            "ReactionSpent": false,
            "Action": "driver command/brake contribution; walks with reins, no cart seat"
          },
          "Cora": {
            "stance": "Mobile",
            "movementSpentFt": 30,
            "ActionSpent": true,
            "BonusActionSpent": false,
            "ReactionSpent": true,
            "Action": "Ready manual gate closure after the one enemy attack"
          },
          "Dane": {
            "stance": "Mobile",
            "movementSpentFt": 30,
            "ActionSpent": true,
            "BonusActionSpent": false,
            "ReactionSpent": false,
            "Action": "Dodge while carrying crate in both hands; no weapon attack"
          }
        },
        "leadDie": 20,
        "leadTotal": 25,
        "numericalDegree": "Success",
        "naturalShift": "up one to Critical Success",
        "EscapeAdded": 2,
        "PursuitAdded": 0,
        "threat": {
          "actor": "Opponent-1",
          "attackBonus": 3,
          "naturalDie": 3,
          "total": 6,
          "target": "Arin",
          "AC": 13,
          "nativeResult": "miss",
          "actualReachFt": 5,
          "actualTargetDistanceFt": 5,
          "movementAvailableFt": 30,
          "damage": 0,
          "otherThreats": 0
        },
        "otherGenericEscapeAwards": 0,
        "endingRectanglesFt": {
          "Cart-1": {
            "x": [
              37,
              45
            ],
            "y": [
              {
                "numerator": 15,
                "denominator": 2
              },
              {
                "numerator": 25,
                "denominator": 2
              }
            ]
          },
          "Mule-1": {
            "x": [
              50,
              60
            ],
            "y": [
              5,
              15
            ]
          },
          "harness-gap": {
            "x": [
              45,
              50
            ],
            "y": [
              9,
              11
            ]
          },
          "Arin": {
            "x": [
              35,
              40
            ],
            "y": [
              0,
              5
            ]
          },
          "Bea": {
            "x": [
              40,
              45
            ],
            "y": [
              {
                "numerator": 25,
                "denominator": 2
              },
              {
                "numerator": 35,
                "denominator": 2
              }
            ]
          },
          "Cora": {
            "x": [
              35,
              40
            ],
            "y": [
              15,
              20
            ]
          },
          "Dane": {
            "x": [
              40,
              45
            ],
            "y": [
              0,
              5
            ]
          },
          "Opponent-1": {
            "x": [
              30,
              35
            ],
            "y": [
              0,
              5
            ]
          }
        }
      }
    ],
    "counters": {
      "Escape": 3,
      "Pursuit": 0,
      "winner": "retreat before Pursuit 3",
      "sameEncounterResourcesRetained": true,
      "enemyDeath": false,
      "lootCreated": false
    },
    "consequences": {
      "HPChanges": [],
      "StrainChanges": [],
      "PressureEvent": "successful-retreat",
      "enemyLoot": []
    }
  }
}
```

### EC-08 — Transport body, control and movement

```json
{
  "id": "FLOW-EC-08",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-08",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "sourceRow": [
      "mounts-vehicles-and-services.donkey-or-mule",
      "mounts-vehicles-and-services.cart"
    ],
    "body": [
      {
        "id": "Mule-1",
        "kind": "significant registered animal",
        "profile": {
          "id": "mounts-vehicles-and-services.donkey-or-mule",
          "name": "Donkey or mule",
          "kind": "living-mount",
          "operationalStatus": "NEW SOURCE-AUTHORING PROFILE; exact candidate not yet approved",
          "operational": {
            "provenance": "All size, mass, abilities, natural AC, HP/Hit Dice, senses, behavior, supply quantities, draw capability and reference level below are NEW provisional game values, not inferred anatomy/Strength or external bestiary statistics. Source purchase price, walking Speed and carry pounds alone are retained numbers.",
            "priceCp": 800,
            "size": "Large",
            "spaceFt": 10,
            "baseBodyMassLb": 400,
            "abilities": {
              "STR": 13,
              "DEX": 11,
              "CON": 13,
              "INT": 2,
              "WIS": 12,
              "CHA": 5
            },
            "proficiencyBonus": 2,
            "naturalAC": 11,
            "naturalACIncludesDexterity": true,
            "maximumHP": 20,
            "hitDice": {
              "count": 3,
              "die": 8,
              "restUse": "real remaining dice and ordinary creature rest/healing limits; fixed maximumHP is this NEW profile, not regenerated from a class table"
            },
            "saveProficiencies": [],
            "skillProficiencies": [],
            "saves": "ability modifier only unless an actual later source grants proficiency; current Wounds/conditions apply",
            "initiative": "DEX modifier plus actual lawful modifiers",
            "passivePerception": 11,
            "senses": "ordinary sight, hearing and smell subject to actual light, line, distance/noise; no darkvision, blindsight, special detection or automatic advantage",
            "languages": [],
            "trainedCuesAreFluency": false,
            "immunities": [],
            "resistances": [],
            "innateSpells": [],
            "classResources": null,
            "walkingSpeedFt": 40,
            "travelMphBeforePenalties": 4.0,
            "carryPounds": 420,
            "cargoLoadCapacity": 42.0,
            "cargoLoadProvenance": "NEW explicit profile Load cap independent of Strength; not claimed source value",
            "burdenedAtLoadOrPounds": "positive supported load at least half the respective limit; one Burdened speed penalty, not two for the same state",
            "hardCarryAdmission": "must meet both pounds/Load and physical fit; no routine movement above either full cap",
            "riderSeats": 1,
            "riderSizeRule": "at least one size smaller; saddle and actual body compatible; both personal gear and rider equipment count",
            "grossDrawLimitLb": 600,
            "drawLimitProvenance": "NEW separate trained-harness capability on firm rolling surface or appropriate ice/snow runners; never a five-times Strength inference",
            "drawMovement": "minimum actual puller speed and vehicle cap; a gross draw above half the combined draw rating also causes the one Burdened speed penalty. Loads on a puller and towing constraints are separately checked; the same named penalty is not doubled. No slopes, broken axles or impassable terrain waived.",
            "attack": {
              "name": "Kick",
              "activation": "Action on its own independent regular turn only; one attack",
              "attackBonus": 3,
              "reachFt": 5,
              "damageDice": "1d4",
              "damageModifier": 1,
              "damageType": "bludgeoning",
              "rider": "none",
              "critical": "Core natural20 doubles damage dice only; natural1 misses"
            },
            "otherActions": "independent actual creature may use physically compatible Core Actions; controlled ridden Action list is Dash, Disengage, Dodge only; no Multiattack or automatic opportunity attack while controlled",
            "deathRule": "NEW default registered Expedition mount is significant and uses ordinary Core Wounds/dying/death saves. Mark significance before an encounter; no retrospective designation to dodge death. A later actual Ranger Beast bond uses its expressly different HP-only/immediate-death lifecycle instead.",
            "training": "Actual ride/cargo/harness/armor training recorded separately under TR-02/07. Purchase name/price is not proof of present training, willingness or health. War-named template may be sold with documented combat habituation but gains no new controlled attack.",
            "dailyFeed": {
              "sourceItemId": "mounts-vehicles-and-services.feed-per-day",
              "priceCp": 5,
              "feedMassLb": 10,
              "speciesCompatible": true,
              "meaning": "NEW one animal-day sold feed quantity for this template at the printed5cp daily reference. Actual species-compatible stock must be supplied; no fodder-to-meat conversion or infinite vendor stock."
            },
            "dailyWaterPints": 24,
            "foodCare": "Use these NEW animal quantities instead of the human Small/Medium/Large Supply basket, with actual safe water and continued rest. Do not add human lamp oil demand to an animal. Unmet daily food/water gives at most1 ordinary expedition Strain for that day; no additional duplicate failure per missing component. No automatic desert-fasting trait.",
            "threatReferenceLevel": 1,
            "threatReferenceProvenance": "NEW encounter-budget comparison only, not a CR, character class level, Ranger acquisition authorization or XP award",
            "sourceCR": "absent; retain absence, and any actual CR-gated ability needs its genuine source/profile predicate rather than treating referenceLevel as CR",
            "custody": "actual individual creature ID and original body history; Donkey or mule is one selected individual, not two. Purchase, hire, boarding, battle loss, rescue, bond and sale preserve that history."
          }
        },
        "currentHP": 20,
        "maximumHP": 20,
        "remainingHitDice": 3,
        "Wounds": 0,
        "Strain": 0,
        "training": [
          "harness",
          "Bea audible stop/walk cues",
          "calm feeding"
        ],
        "willing": true,
        "carriedHarnessLb": 8,
        "carriedHarnessLoad": {
          "numerator": 4,
          "denominator": 5
        },
        "diet": {
          "feedLbPerDay": 10,
          "waterPintsPerDay": 24
        },
        "classBond": {
          "presence": "absent"
        },
        "rider": {
          "presence": "absent"
        }
      },
      {
        "id": "Cart-1",
        "kind": "owned drawn frame",
        "profile": {
          "id": "mounts-vehicles-and-services.cart",
          "name": "Cart",
          "kind": "drawn-vehicle",
          "operationalStatus": "NEW SOURCE-AUTHORING PROFILE; exact candidate not yet approved",
          "operational": {
            "provenance": "Price retained; Cart maximumHP30 binds the reviewed ordinary cart body. Every other listed body quantity/geometry/handling number is NEW. No passengers, animals, harnesses, operators or contents are included in price.",
            "priceCp": 1500,
            "emptyMassLb": 200,
            "outerFeet": [
              8,
              5,
              4
            ],
            "usableBedFeet": [
              6,
              4,
              3
            ],
            "bodyMaterial": "wood with ordinary metal fittings",
            "structuralAC": 15,
            "maximumHP": 30,
            "payloadPounds": 300,
            "payloadLoads": 30,
            "cargoSublimitPounds": 300,
            "cargoSublimitLoads": 30,
            "maximumSeatedOccupantsIncludingDriver": 1,
            "requiredDrivers": 1,
            "minimumFittedPullers": 1,
            "tacticalSpeedCapFt": 40,
            "speedRule": "minimum current fitted puller Speed and cap. Each actual puller draw rating, combined gross vehicle+payload draw limit, route fit, stability and terrain must pass. One named Burdened penalty applies when either carried or gross-draw threshold qualifies; no duplicate penalty for the same mount.",
            "terrain": "firm wheel-supporting route; no ordinary climbing, stairs, ladders, swimming or unsupported gaps",
            "operatingFootprint": "vehicle envelope plus actual puller footprint and at least5ft forward harness gap; route must contain all real widths/heights/turning space",
            "turning": "one90-degree turn needs traveled distance at least the vehicle length and a clear swept envelope; sharper/blocked maneuver needs an actual separate route/work plan, not an automatic check",
            "controls": "driver uses one Action per regular turn in tactical operation to guide/brake using the actual reins/lever and one hand; NEW manual brakes are included. Pullers expend actual movement in the linked drive event. Driver cannot claim a separate mounted turn for a pulling animal or duplicate movement by changing drivers. Outside initiative driving is continuous actual work, not rest.",
            "movementEvent": "one linked vehicle/puller movement event per numbered round; resolve after required current driver Action and puller movement budgets are available. No future crew Action is presumed. All contributing budgets spent once. No vehicle Dash/Disengage/Reaction/attack; actual pullers have only their legal creature Actions.",
            "setupMinutes": 5,
            "setupActors": 1,
            "loadingRule": "TR-12, real necessary handling; setup harness is additional, no free load/receivers",
            "brake": "actual controlled stop at end of paid move; uncrewed/unhitched vehicle at rest stays at rest unless terrain/force actually moves it; no generic magical parking",
            "primaryConstituents": "original main frame, principal axle/runner set and bed structure; subordinate wheels, pins, harness fittings or brake pads can be replaced by actual compatible stock",
            "zeroHP": "Broken, stops useful self/drawn transport; retains wreck, mass, passengers and custody. No automatic occupant damage from mere HP0. Real collision/fall/dislodgement is a separately declared event. Reaching0 does not erase salvage or restore original frame.",
            "repair": "TR-14 ordinary structural repair with source-specific cost/time and original main body; not creature healing. No equipment Integrity track in parallel."
          }
        },
        "currentHP": 30,
        "occupants": [],
        "driver": "Bea",
        "driverWalking": true,
        "originalPrimaryMembers": [
          "frame-1",
          "axle-1",
          "bed-1"
        ],
        "repairEvents": [],
        "nativeCreatureTurn": false
      }
    ],
    "payload": {
      "supply": {
        "basketCountForPurchase": 8,
        "abstractSupplyBalanceExists": false,
        "basketPurchaseCp": 504,
        "animalFeedWaterPurchaseCp": 16,
        "lots": [
          {
            "id": "food-0",
            "item": "sealed ration-equivalent food",
            "amount": {
              "numerator": 16,
              "denominator": 1
            },
            "unit": "lb",
            "massLb": {
              "numerator": 16,
              "denominator": 1
            },
            "packedAt": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 50400,
              "departurePreparationOffsetSeconds": -36000
            },
            "expiresAt": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 2642400,
              "departurePreparationOffsetSeconds": 2556000
            },
            "costCp": 400,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "water-human-0",
            "item": "potable water",
            "amount": {
              "numerator": 64,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 64,
              "denominator": 1
            },
            "costCp": 8,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "feed-0",
            "item": "species-compatible mule feed",
            "amount": {
              "numerator": 20,
              "denominator": 1
            },
            "unit": "lb",
            "massLb": {
              "numerator": 20,
              "denominator": 1
            },
            "costCp": 10,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "water-mule-0",
            "item": "potable water",
            "amount": {
              "numerator": 48,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 48,
              "denominator": 1
            },
            "costCp": 6,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "sundries-0",
            "item": "ordinary expendable cleaning cloth and twine",
            "amount": {
              "numerator": 2,
              "denominator": 1
            },
            "unit": "lb",
            "massLb": {
              "numerator": 2,
              "denominator": 1
            },
            "costCp": 16,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-1",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-1",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-2",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-2",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-3",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-3",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-4",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-4",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-5",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-5",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-6",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-6",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-7",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-7",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-8",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-8",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          }
        ],
        "containers": [
          {
            "id": "skin-01",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-02",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-03",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-04",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-05",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-06",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-07",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-08",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-09",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-10",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-11",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-12",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-13",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-14",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-15",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-16",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-17",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-18",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-19",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-20",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-21",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-22",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-23",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-24",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-25",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-26",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-27",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-28",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-1",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-1",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-2",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-2",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-3",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-3",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-4",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-4",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-5",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-5",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-6",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-6",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-7",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-7",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-8",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-8",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "feedbag-1",
            "emptyMassLb": 1,
            "capacityLb": 10,
            "openingContents": {
              "lot": "feed-0",
              "lb": 10
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true
          },
          {
            "id": "feedbag-2",
            "emptyMassLb": 1,
            "capacityLb": 10,
            "openingContents": {
              "lot": "feed-0",
              "lb": 10
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true
          }
        ],
        "packing": {
          "initialPreallocationPayloadLb": 188,
          "initialGrossDrawLb": 388,
          "contentsFit": {
            "bedFt": [
              6,
              4,
              3
            ],
            "allocatedStorageFt3": 24,
            "longestPackedBundleFt": 3,
            "crateFt": [
              2,
              1,
              1
            ],
            "closure": "sealed skins and flasks; lashed food/feed bags and closed crate"
          },
          "noDoubleTare": "8 full 1-lb flasks already include 2 lb of flask bodies; water is separate from the 28 one-pound skins."
        }
      },
      "crate": {
        "id": "crate-1",
        "massLb": 20,
        "Load": {
          "numerator": 2,
          "denominator": 1
        },
        "outerFeet": [
          2,
          1,
          1
        ],
        "Class": 2,
        "priority": 1,
        "tags": [],
        "closed": true,
        "condition": "unchanged sound ordinary material",
        "title": "licensed assignment verified from actual stipulated release record",
        "custody": [
          {
            "from": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 118260,
              "departurePreparationOffsetSeconds": 31860
            },
            "to": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 118332,
              "departurePreparationOffsetSeconds": 31932
            },
            "custodian": "Dane"
          },
          {
            "from": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 118332,
              "departurePreparationOffsetSeconds": 31932
            },
            "to": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 155592,
              "departurePreparationOffsetSeconds": 69192
            },
            "custodian": "Expedition in Cart-1"
          },
          {
            "from": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 155592,
              "departurePreparationOffsetSeconds": 69192
            },
            "custodian": "Pera, actual paid buyer"
          }
        ]
      },
      "riders": [],
      "walkingDriver": "Bea"
    },
    "controller": {
      "actor": "Bea",
      "channel": "trained audible cues plus fitting reins",
      "hands": 1,
      "riding": false
    },
    "turnSchedule": [
      [
        "Arin",
        "Bea",
        "Mule-1",
        "Cora",
        "Dane",
        "Opponent-1"
      ],
      [
        "Arin",
        "Bea",
        "Mule-1",
        "Cora",
        "Dane",
        "Opponent-1"
      ]
    ],
    "movement": [
      {
        "id": "drive-1",
        "mover": "Mule-1",
        "carrier": "Cart-1",
        "initiator": "Bea",
        "distanceFt": 30,
        "selfPowered": true,
        "pullerMoveSpentFt": 30,
        "pullerAction": "Dodge",
        "resolvesAfterRequiredContributions": true,
        "vehicleDriveCount": 1
      },
      {
        "id": "drive-2",
        "mover": "Mule-1",
        "carrier": "Cart-1",
        "initiator": "Bea",
        "distanceFt": 30,
        "selfPowered": true,
        "pullerMoveSpentFt": 30,
        "pullerAction": "Dodge",
        "resolvesAfterRequiredContributions": true,
        "vehicleDriveCount": 1
      }
    ],
    "crewReservations": [
      {
        "stance": "Mobile",
        "movementSpentFt": 30,
        "ActionSpent": true,
        "BonusActionSpent": false,
        "ReactionSpent": false,
        "Action": "driver command/brake contribution; walks with reins, no cart seat"
      },
      {
        "stance": "Mobile",
        "movementSpentFt": 30,
        "ActionSpent": true,
        "BonusActionSpent": false,
        "ReactionSpent": false,
        "Action": "driver command/brake contribution; walks with reins, no cart seat"
      }
    ],
    "operation": {
      "nutrition": [
        {
          "id": "meal-Arin-0-food",
          "lotId": "food-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-0-water",
          "lotId": "water-human-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-1-food",
          "lotId": "food-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 130620,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43320,
          "relativeEnd": 44220,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-1-water",
          "lotId": "water-human-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 130620,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43320,
          "relativeEnd": 44220,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-2-food",
          "lotId": "food-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-2-water",
          "lotId": "water-human-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-3-food",
          "lotId": "food-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Arin-3-water",
          "lotId": "water-human-0",
          "recipient": "Arin",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-0-food",
          "lotId": "food-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-0-water",
          "lotId": "water-human-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-1-food",
          "lotId": "food-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 129600,
            "endSeconds": 130500,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43200,
          "relativeEnd": 44100,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-1-water",
          "lotId": "water-human-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 129600,
            "endSeconds": 130500,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43200,
          "relativeEnd": 44100,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-2-food",
          "lotId": "food-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-2-water",
          "lotId": "water-human-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-3-food",
          "lotId": "food-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Bea-3-water",
          "lotId": "water-human-0",
          "recipient": "Bea",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-0-food",
          "lotId": "food-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-0-water",
          "lotId": "water-human-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-1-food",
          "lotId": "food-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 130620,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43320,
          "relativeEnd": 44220,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-1-water",
          "lotId": "water-human-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 129720,
            "endSeconds": 130620,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43320,
          "relativeEnd": 44220,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-2-food",
          "lotId": "food-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-2-water",
          "lotId": "water-human-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-3-food",
          "lotId": "food-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Cora-3-water",
          "lotId": "water-human-0",
          "recipient": "Cora",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-0-food",
          "lotId": "food-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-0-water",
          "lotId": "water-human-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 86400,
            "endSeconds": 87300,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 0,
          "relativeEnd": 900,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-1-food",
          "lotId": "food-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 129600,
            "endSeconds": 130500,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43200,
          "relativeEnd": 44100,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-1-water",
          "lotId": "water-human-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 129600,
            "endSeconds": 130500,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 43200,
          "relativeEnd": 44100,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-2-food",
          "lotId": "food-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-2-water",
          "lotId": "water-human-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-3-food",
          "lotId": "food-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 1,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "meal-Dane-3-water",
          "lotId": "water-human-0",
          "recipient": "Dane",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 4,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-0-feed",
          "lotId": "feed-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 87300,
            "endSeconds": 88200,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 900,
          "relativeEnd": 1800,
          "amount": {
            "numerator": 5,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-0-water",
          "lotId": "water-mule-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 87300,
            "endSeconds": 88200,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 900,
          "relativeEnd": 1800,
          "amount": {
            "numerator": 12,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-1-feed",
          "lotId": "feed-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 130500,
            "endSeconds": 131400,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 44100,
          "relativeEnd": 45000,
          "amount": {
            "numerator": 5,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-1-water",
          "lotId": "water-mule-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 130500,
            "endSeconds": 131400,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 44100,
          "relativeEnd": 45000,
          "amount": {
            "numerator": 12,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-2-feed",
          "lotId": "feed-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 5,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-2-water",
          "lotId": "water-mule-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 86400,
          "relativeEnd": 87300,
          "amount": {
            "numerator": 12,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-3-feed",
          "lotId": "feed-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 5,
            "denominator": 1
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "mule-meal-3-water",
          "lotId": "water-mule-0",
          "recipient": "Mule-1",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "relativeStart": 129600,
          "relativeEnd": 130500,
          "amount": {
            "numerator": 12,
            "denominator": 1
          },
          "unit": "pint",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": true
        },
        {
          "id": "cleaning-0",
          "lotId": "sundries-0",
          "recipient": "Expedition shared cleanup",
          "interval": {
            "startSeconds": 87300,
            "endSeconds": 87360,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 900,
          "relativeEnd": 960,
          "amount": {
            "numerator": 1,
            "denominator": 2
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": false
        },
        {
          "id": "cleaning-1",
          "lotId": "sundries-0",
          "recipient": "Expedition shared cleanup",
          "interval": {
            "startSeconds": 130620,
            "endSeconds": 130680,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 44220,
          "relativeEnd": 44280,
          "amount": {
            "numerator": 1,
            "denominator": 2
          },
          "unit": "lb",
          "canonicalRelativeDay": 0,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": false
        },
        {
          "id": "cleaning-2",
          "lotId": "sundries-0",
          "recipient": "Expedition shared cleanup",
          "interval": {
            "startSeconds": 173700,
            "endSeconds": 173760,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 87300,
          "relativeEnd": 87360,
          "amount": {
            "numerator": 1,
            "denominator": 2
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": false
        },
        {
          "id": "cleaning-3",
          "lotId": "sundries-0",
          "recipient": "Expedition shared cleanup",
          "interval": {
            "startSeconds": 216900,
            "endSeconds": 216960,
            "activeSeconds": 60,
            "halfOpen": true
          },
          "relativeStart": 130500,
          "relativeEnd": 130560,
          "amount": {
            "numerator": 1,
            "denominator": 2
          },
          "unit": "lb",
          "canonicalRelativeDay": 1,
          "evidence": "authored actual supported interval",
          "creditsNutritionOnce": false
        }
      ],
      "harness": "owned fitted 8-lb harness; same throughout"
    },
    "repair": [],
    "hireContract": {
      "id": "STABLE-1",
      "owner": "Toma",
      "animal": "Mule-1",
      "term": {
        "startSeconds": 148992,
        "endSeconds": 321792,
        "activeSeconds": 172800,
        "halfOpen": true
      },
      "priceCp": 100,
      "facilities": "fitting Large stall, safe water/feed access, actual staff",
      "partyStockUsed": true,
      "automaticHealing": false
    }
  }
}
```

### EC-09 — Haven intake, claim and quote

```json
{
  "id": "FLOW-EC-09",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-09",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "arrival": {
      "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
      "elapsedSeconds": 148992,
      "departurePreparationOffsetSeconds": 62592
    },
    "lot": {
      "id": "crate-1",
      "massLb": 20,
      "Load": {
        "numerator": 2,
        "denominator": 1
      },
      "outerFeet": [
        2,
        1,
        1
      ],
      "Class": 2,
      "priority": 1,
      "tags": [],
      "closed": true,
      "condition": "unchanged sound ordinary material",
      "title": "licensed assignment verified from actual stipulated release record",
      "custody": [
        {
          "from": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 118260,
            "departurePreparationOffsetSeconds": 31860
          },
          "to": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 118332,
            "departurePreparationOffsetSeconds": 31932
          },
          "custodian": "Dane"
        },
        {
          "from": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 118332,
            "departurePreparationOffsetSeconds": 31932
          },
          "to": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 155592,
            "departurePreparationOffsetSeconds": 69192
          },
          "custodian": "Expedition in Cart-1"
        },
        {
          "from": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 155592,
            "departurePreparationOffsetSeconds": 69192
          },
          "custodian": "Pera, actual paid buyer"
        }
      ]
    },
    "claimants": [
      "Expedition under licensed release; no dispute"
    ],
    "inspection": [
      {
        "id": "haven-intake",
        "activity": "intake",
        "actors": [
          "Arin",
          "Ione"
        ],
        "interval": {
          "startSeconds": 148992,
          "endSeconds": 149592,
          "activeSeconds": 600,
          "halfOpen": true
        },
        "relativeStart": 62592,
        "relativeEnd": 63192,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-quarantine-inspection",
        "activity": "quarantine inspection",
        "actors": [
          "Dane",
          "Oren"
        ],
        "interval": {
          "startSeconds": 149592,
          "endSeconds": 150192,
          "activeSeconds": 600,
          "halfOpen": true
        },
        "relativeStart": 63192,
        "relativeEnd": 63792,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-provenance",
        "activity": "provenance",
        "actors": [
          "Cora",
          "Ione"
        ],
        "interval": {
          "startSeconds": 150192,
          "endSeconds": 151992,
          "activeSeconds": 1800,
          "halfOpen": true
        },
        "relativeStart": 63792,
        "relativeEnd": 65592,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-known-finite-appraisal-and-quote",
        "activity": "known finite appraisal and quote",
        "actors": [
          "Cora",
          "Pera"
        ],
        "interval": {
          "startSeconds": 151992,
          "endSeconds": 153792,
          "activeSeconds": 1800,
          "halfOpen": true
        },
        "relativeStart": 65592,
        "relativeEnd": 67392,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      }
    ],
    "valuationDomain": "unpriced ordinary finite lot, actual buyer offer",
    "offer": {
      "id": "QUOTE-1",
      "buyer": "Pera",
      "quantity": "one complete crate-1",
      "priceCp": 12000,
      "issuedAt": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 153792,
        "departurePreparationOffsetSeconds": 67392
      },
      "acceptedAt": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 155592,
        "departurePreparationOffsetSeconds": 69192
      },
      "expiresAt": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 158400,
        "departurePreparationOffsetSeconds": 72000
      },
      "authority": "actual licensed buyer and seller; verified original release",
      "chargesIncluded": []
    },
    "artifactInputs": {
      "applicable": false,
      "reason": "No artifact valuation formula invoked"
    },
    "quarantine": {
      "reason": "required incoming licensed-material inspection, no inferred contamination",
      "interval": {
        "startSeconds": 149592,
        "endSeconds": 150192,
        "activeSeconds": 600,
        "halfOpen": true
      },
      "worker": "Oren",
      "paidTransaction": "mandatory-inspection",
      "release": "sound matching sealed crate"
    }
  }
}
```

### EC-10 — Money, sponsor and insurance settlement

```json
{
  "id": "FLOW-EC-10",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-10",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "transactionId": [
      "buy-human-0",
      "buy-animal-0",
      "premium-0",
      "room-fee",
      "stable-fee",
      "mandatory-inspection",
      "sale-crate",
      "levy",
      "guild-share",
      "distribution-Arin",
      "distribution-Bea",
      "distribution-Cora",
      "distribution-Dane",
      "next-stock"
    ],
    "payerPayee": [
      {
        "transactionId": "buy-human-0",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 52400,
          "departurePreparationOffsetSeconds": -34000
        },
        "relativeTime": -34000,
        "payer": "Expedition cash",
        "payee": "Provisioner",
        "exactCp": {
          "numerator": 504,
          "denominator": 1
        },
        "settledCp": 504,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "operating cost",
        "episode": "first"
      },
      {
        "transactionId": "buy-animal-0",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 52500,
          "departurePreparationOffsetSeconds": -33900
        },
        "relativeTime": -33900,
        "payer": "Expedition cash",
        "payee": "Provisioner",
        "exactCp": {
          "numerator": 16,
          "denominator": 1
        },
        "settledCp": 16,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "operating cost",
        "episode": "first"
      },
      {
        "transactionId": "premium-0",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 53400,
          "departurePreparationOffsetSeconds": -33000
        },
        "relativeTime": -33000,
        "payer": "Expedition cash",
        "payee": "Underwriter",
        "exactCp": {
          "numerator": 600,
          "denominator": 1
        },
        "settledCp": 600,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "operating cost",
        "episode": "first"
      },
      {
        "transactionId": "room-fee",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 148992,
          "departurePreparationOffsetSeconds": 62592
        },
        "relativeTime": 62592,
        "payer": "Expedition cash",
        "payee": "Sera",
        "exactCp": {
          "numerator": 800,
          "denominator": 1
        },
        "settledCp": 800,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "operating cost",
        "episode": "first"
      },
      {
        "transactionId": "stable-fee",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 148992,
          "departurePreparationOffsetSeconds": 62592
        },
        "relativeTime": 62592,
        "payer": "Expedition cash",
        "payee": "Toma",
        "exactCp": {
          "numerator": 100,
          "denominator": 1
        },
        "settledCp": 100,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "operating cost",
        "episode": "first"
      },
      {
        "transactionId": "mandatory-inspection",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 150192,
          "departurePreparationOffsetSeconds": 63792
        },
        "relativeTime": 63792,
        "payer": "Expedition cash",
        "payee": "Haven inspector",
        "exactCp": {
          "numerator": 200,
          "denominator": 1
        },
        "settledCp": 200,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "mandatory",
        "episode": "first"
      },
      {
        "transactionId": "sale-crate",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 155592,
          "departurePreparationOffsetSeconds": 69192
        },
        "relativeTime": 69192,
        "payer": "Pera",
        "payee": "Expedition cash",
        "exactCp": {
          "numerator": 12000,
          "denominator": 1
        },
        "settledCp": 12000,
        "rounding": "sale floor once",
        "status": "paid",
        "kind": "sale",
        "episode": "first"
      },
      {
        "transactionId": "levy",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 157392,
          "departurePreparationOffsetSeconds": 70992
        },
        "relativeTime": 70992,
        "payer": "Expedition cash",
        "payee": "Haven treasury",
        "exactCp": {
          "numerator": 600,
          "denominator": 1
        },
        "settledCp": 600,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "tax",
        "episode": "first"
      },
      {
        "transactionId": "guild-share",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 157392,
          "departurePreparationOffsetSeconds": 70992
        },
        "relativeTime": 70992,
        "payer": "Expedition cash",
        "payee": "Local guild",
        "exactCp": {
          "numerator": 2240,
          "denominator": 1
        },
        "settledCp": 2240,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "sponsor",
        "episode": "first"
      },
      {
        "transactionId": "distribution-Arin",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 226800,
          "departurePreparationOffsetSeconds": 140400
        },
        "relativeTime": 140400,
        "payer": "Expedition cash",
        "payee": "Arin",
        "exactCp": {
          "numerator": 1235,
          "denominator": 1
        },
        "settledCp": 1235,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "profit distribution",
        "episode": "first"
      },
      {
        "transactionId": "distribution-Bea",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 226800,
          "departurePreparationOffsetSeconds": 140400
        },
        "relativeTime": 140400,
        "payer": "Expedition cash",
        "payee": "Bea",
        "exactCp": {
          "numerator": 1235,
          "denominator": 1
        },
        "settledCp": 1235,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "profit distribution",
        "episode": "first"
      },
      {
        "transactionId": "distribution-Cora",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 226800,
          "departurePreparationOffsetSeconds": 140400
        },
        "relativeTime": 140400,
        "payer": "Expedition cash",
        "payee": "Cora",
        "exactCp": {
          "numerator": 1235,
          "denominator": 1
        },
        "settledCp": 1235,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "profit distribution",
        "episode": "first"
      },
      {
        "transactionId": "distribution-Dane",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 226800,
          "departurePreparationOffsetSeconds": 140400
        },
        "relativeTime": 140400,
        "payer": "Expedition cash",
        "payee": "Dane",
        "exactCp": {
          "numerator": 1235,
          "denominator": 1
        },
        "settledCp": 1235,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "profit distribution",
        "episode": "first"
      },
      {
        "transactionId": "next-stock",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 228600,
          "departurePreparationOffsetSeconds": 142200
        },
        "relativeTime": 142200,
        "payer": "Expedition cash",
        "payee": "Provisioner",
        "exactCp": {
          "numerator": 520,
          "denominator": 1
        },
        "settledCp": 520,
        "rounding": "purchase/fee ceil once",
        "status": "paid",
        "kind": "next inventory purchase",
        "episode": "next"
      }
    ],
    "currencyAndExactAmount": "cp, exact rational per entry",
    "rounding": "one final direction-specific cp rounding per real payment",
    "paymentStatus": "all listed paid",
    "sponsor": {
      "id": "SPONSOR-1",
      "rate": {
        "numerator": 1,
        "denominator": 5
      },
      "base": "gross less one applicable tax and mandatory rescue/quarantine",
      "signedBeforeDeparture": true,
      "grossGrantOrLoan": false
    },
    "insurance": {
      "id": "INSURANCE-1",
      "insuredLot": "crate-1",
      "insuredValueCp": 12000,
      "premiumRate": {
        "numerator": 1,
        "denominator": 20
      },
      "premiumPayment": "premium-0",
      "term": {
        "startSeconds": 86400,
        "endSeconds": 148992,
        "activeSeconds": 62592,
        "halfOpen": true
      },
      "ordinaryLossFraction": {
        "numerator": 3,
        "denominator": 5
      },
      "episodeDeductibleCp": 2400,
      "lossEvents": [],
      "claims": [],
      "payoutCp": 0,
      "status": "closed without claim"
    },
    "settlement": {
      "grossCp": 12000,
      "taxCp": 600,
      "mandatoryCp": 200,
      "sponsorBaseCp": 11200,
      "sponsorCp": 2240,
      "netCp": 8960,
      "uniqueOtherOperatingCostsCp": 2020,
      "trueProfitCp": 6940,
      "nextReserveCp": 2000,
      "distributionCp": 4940,
      "eachCharacterCp": 1235,
      "cashBeforeDistributionCp": 9940,
      "cashAfterDistributionCp": 5000,
      "nextProcurementCp": 520,
      "finalCashCp": 4480,
      "capitalStillCashCp": 3000,
      "unspentEarmarkCp": 1480,
      "nextInventoryPaidCostCp": 520,
      "unpaidLiabilitiesCp": 0
    }
  }
}
```

### EC-11 — Ordinary social scene and communication

```json
{
  "id": "FLOW-EC-11",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-11",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "sceneId": "licensed-return-1",
    "frame": {
      "Want": "sell the licensed lot",
      "Leverage": "actual title, sound crate and buyer need",
      "Limit": "only this buyer and this lot",
      "Clock": "offer expires at hour 20",
      "Witness": [
        "Ione",
        "Pera"
      ],
      "authority": "Pera can spend the stated funds; Arin may accept for this charter"
    },
    "channel": "shared spoken language; all actual participants hear and understand; no spell used",
    "stakes": {
      "promisedResult": "accepted finite 120-gp sale",
      "costlyAgreement": "none"
    },
    "resolutionRoute": "noCheck",
    "timing": [
      {
        "id": "haven-known-finite-appraisal-and-quote",
        "activity": "known finite appraisal and quote",
        "actors": [
          "Cora",
          "Pera"
        ],
        "interval": {
          "startSeconds": 151992,
          "endSeconds": 153792,
          "activeSeconds": 1800,
          "halfOpen": true
        },
        "relativeStart": 65592,
        "relativeEnd": 67392,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-buyer-agreement",
        "activity": "buyer agreement",
        "actors": [
          "Arin",
          "Pera"
        ],
        "interval": {
          "startSeconds": 153792,
          "endSeconds": 155592,
          "activeSeconds": 1800,
          "halfOpen": true
        },
        "relativeStart": 67392,
        "relativeEnd": 69192,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      }
    ],
    "help": [],
    "outcome": "agreed paid sale at stated price",
    "retries": []
  }
}
```

### EC-12 — Lossless reputation source envelope

```json
{
  "id": "FLOW-EC-12",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-12",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "rawSource": "{\"FX-LOCAL-GUILD\":0}",
    "sourceVersion": "standing-v1 synthetic campaign state",
    "presence": "value",
    "subjectAndBinding": {
      "subject": "Expedition-1 members as recorded counterparties",
      "institution": "FX-LOCAL-GUILD",
      "synthetic": true
    },
    "interpretation": "standing-v1",
    "initialContribution": {
      "origin": "declared existing neutral relationship",
      "backgroundContributionApplied": false
    },
    "events": [
      {
        "id": "licensed-recovery-delivered",
        "causeId": "crate-1-return",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 157392,
          "departurePreparationOffsetSeconds": 70992
        },
        "knownBy": [
          "Ione",
          "Pera"
        ],
        "evidence": [
          "actual original license",
          "same crate inspected",
          "buyer transfer witnessed"
        ],
        "proposedDelta": 1,
        "signedSceneSum": 1,
        "sceneCappedDelta": 1,
        "appliedDelta": 1,
        "overflow": 0,
        "endingScore": 1
      }
    ],
    "derivedView": {
      "score": 1,
      "band": "Liked"
    },
    "history": {
      "originalRawUnchanged": true,
      "overflow": 0,
      "duplicateReportsDelta": 0
    }
  }
}
```

### EC-13 — Institution, faction action and rival clock

```json
{
  "id": "FLOW-EC-13",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-13",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "institution": "FX-LOCAL-GUILD",
    "sourceRecord": {
      "publicBinding": "synthetic local guild example only; exact private original binding preserved internally"
    },
    "rivalFrame": {
      "applicable": false,
      "reason": "No rival is introduced by this fixture"
    },
    "action": {
      "id": "proof-review-1",
      "type": "Research",
      "actor": "Rhea",
      "interval": {
        "startSeconds": 136800,
        "endSeconds": 165600,
        "activeSeconds": 28800,
        "halfOpen": true
      },
      "activeSeconds": 28800,
      "tools": [
        "actual local title archive",
        "written charter",
        "received intake copies"
      ],
      "stock": "ordinary owned writing stock; no party ingredients or magical output",
      "permissions": "actual synthetic local archive authority",
      "result": "confirm existing release and receipt, no new ownership or secret lore",
      "additionalGenericRoll": "none; genuine known paperwork is not an uncertain new claim"
    },
    "checkpoint": [
      {
        "id": "actual-return",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 148992,
          "departurePreparationOffsetSeconds": 62592
        },
        "actionId": "proof-review-1",
        "activeSecondsSoFar": 12192,
        "status": "still in progress; no extra action"
      },
      {
        "id": "canonical-day0",
        "time": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 172800,
          "departurePreparationOffsetSeconds": 86400
        },
        "actionId": "proof-review-1",
        "completedAt": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 165600,
          "departurePreparationOffsetSeconds": 79200
        },
        "status": "report already completed real work once"
      }
    ],
    "clocks": {
      "id": "claim-proof",
      "kind": "Claim",
      "length": 4,
      "opening": 2,
      "segments": [
        {
          "id": "actual-proof-accepted",
          "causeId": "proof-review-1",
          "time": {
            "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
            "elapsedSeconds": 165600,
            "departurePreparationOffsetSeconds": 79200
          },
          "delta": 1
        }
      ],
      "ending": 3,
      "thresholdTriggered": false,
      "duplicateNoticeDelta": 0
    },
    "publication": "Only the synthetic public desk relationship is shown. No original private faction dossier or resonance data is projected."
  }
}
```

### EC-14 — Service, instruction and advancement

```json
{
  "id": "FLOW-EC-14",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-14",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "serviceOrder": {
      "rooms": {
        "id": "ROOM-1",
        "owner": "Sera",
        "recipients": [
          "Arin",
          "Bea",
          "Cora",
          "Dane"
        ],
        "term": {
          "startSeconds": 148992,
          "endSeconds": 264192,
          "activeSeconds": 115200,
          "halfOpen": true
        },
        "priceCp": 800,
        "realFacilities": [
          "four safe beds",
          "secure dry gear storage",
          "potable-service access"
        ],
        "includedWork": "Staff keep the party-owned lamps fueled using party-owned finite oil; no new party provisions or training credit."
      },
      "stable": {
        "id": "STABLE-1",
        "owner": "Toma",
        "animal": "Mule-1",
        "term": {
          "startSeconds": 148992,
          "endSeconds": 321792,
          "activeSeconds": 172800,
          "halfOpen": true
        },
        "priceCp": 100,
        "facilities": "fitting Large stall, safe water/feed access, actual staff",
        "partyStockUsed": true,
        "automaticHealing": false
      },
      "lampShifts": [
        {
          "actors": [
            "Iris",
            "June"
          ],
          "interval": {
            "startSeconds": 148992,
            "endSeconds": 201600,
            "activeSeconds": 52608,
            "halfOpen": true
          }
        },
        {
          "actors": [
            "Leto",
            "Mara"
          ],
          "interval": {
            "startSeconds": 201600,
            "endSeconds": 259200,
            "activeSeconds": 57600,
            "halfOpen": true
          }
        },
        {
          "actors": [
            "Iris",
            "June"
          ],
          "interval": {
            "startSeconds": 259200,
            "endSeconds": 264192,
            "activeSeconds": 4992,
            "halfOpen": true
          }
        }
      ],
      "providerRest": [
        {
          "actors": [
            "Iris",
            "June"
          ],
          "interval": {
            "startSeconds": 201600,
            "endSeconds": 230400,
            "activeSeconds": 28800,
            "halfOpen": true
          }
        },
        {
          "actors": [
            "Leto",
            "Mara"
          ],
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 201600,
            "activeSeconds": 28800,
            "halfOpen": true
          }
        }
      ],
      "muleCare": [
        {
          "actor": "Nell",
          "interval": {
            "startSeconds": 172800,
            "endSeconds": 173700,
            "activeSeconds": 900,
            "halfOpen": true
          }
        },
        {
          "actor": "Orin",
          "interval": {
            "startSeconds": 216000,
            "endSeconds": 216900,
            "activeSeconds": 900,
            "halfOpen": true
          }
        }
      ],
      "authority": "All provider bodies, own support, wages, permissions and facility capacities are explicit synthetic premises. A payment alone is not used as proof of a worker.",
      "externalNotRoster": true
    },
    "labor": [
      {
        "id": "haven-intake",
        "activity": "intake",
        "actors": [
          "Arin",
          "Ione"
        ],
        "interval": {
          "startSeconds": 148992,
          "endSeconds": 149592,
          "activeSeconds": 600,
          "halfOpen": true
        },
        "relativeStart": 62592,
        "relativeEnd": 63192,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-quarantine-inspection",
        "activity": "quarantine inspection",
        "actors": [
          "Dane",
          "Oren"
        ],
        "interval": {
          "startSeconds": 149592,
          "endSeconds": 150192,
          "activeSeconds": 600,
          "halfOpen": true
        },
        "relativeStart": 63192,
        "relativeEnd": 63792,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-provenance",
        "activity": "provenance",
        "actors": [
          "Cora",
          "Ione"
        ],
        "interval": {
          "startSeconds": 150192,
          "endSeconds": 151992,
          "activeSeconds": 1800,
          "halfOpen": true
        },
        "relativeStart": 63792,
        "relativeEnd": 65592,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-known-finite-appraisal-and-quote",
        "activity": "known finite appraisal and quote",
        "actors": [
          "Cora",
          "Pera"
        ],
        "interval": {
          "startSeconds": 151992,
          "endSeconds": 153792,
          "activeSeconds": 1800,
          "halfOpen": true
        },
        "relativeStart": 65592,
        "relativeEnd": 67392,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-buyer-agreement",
        "activity": "buyer agreement",
        "actors": [
          "Arin",
          "Pera"
        ],
        "interval": {
          "startSeconds": 153792,
          "endSeconds": 155592,
          "activeSeconds": 1800,
          "halfOpen": true
        },
        "relativeStart": 67392,
        "relativeEnd": 69192,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-ledger-and-claims",
        "activity": "ledger and claims",
        "actors": [
          "Arin",
          "Ione"
        ],
        "interval": {
          "startSeconds": 155592,
          "endSeconds": 157392,
          "activeSeconds": 1800,
          "halfOpen": true
        },
        "relativeStart": 69192,
        "relativeEnd": 70992,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-standing-notice",
        "activity": "standing notice",
        "actors": [
          "Arin",
          "Bea",
          "Cora",
          "Dane",
          "Ione"
        ],
        "interval": {
          "startSeconds": 157392,
          "endSeconds": 157992,
          "activeSeconds": 600,
          "halfOpen": true
        },
        "relativeStart": 70992,
        "relativeEnd": 71592,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-advancement-record",
        "activity": "advancement record",
        "actors": [
          "Arin",
          "Dane"
        ],
        "interval": {
          "startSeconds": 157992,
          "endSeconds": 158592,
          "activeSeconds": 600,
          "halfOpen": true
        },
        "relativeStart": 71592,
        "relativeEnd": 72192,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      },
      {
        "id": "haven-prospective-next-charter",
        "activity": "prospective next charter",
        "actors": [
          "Arin",
          "Bea",
          "Cora",
          "Dane"
        ],
        "interval": {
          "startSeconds": 158592,
          "endSeconds": 162192,
          "activeSeconds": 3600,
          "halfOpen": true
        },
        "relativeStart": 72192,
        "relativeEnd": 75792,
        "completion": "Actual known paperwork/quote; no uncertainty check is required in this stipulated fixture"
      }
    ],
    "inputs": {
      "partyStock": {
        "basketCountForPurchase": 8,
        "abstractSupplyBalanceExists": false,
        "basketPurchaseCp": 504,
        "animalFeedWaterPurchaseCp": 16,
        "lots": [
          {
            "id": "food-0",
            "item": "sealed ration-equivalent food",
            "amount": {
              "numerator": 16,
              "denominator": 1
            },
            "unit": "lb",
            "massLb": {
              "numerator": 16,
              "denominator": 1
            },
            "packedAt": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 50400,
              "departurePreparationOffsetSeconds": -36000
            },
            "expiresAt": {
              "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
              "elapsedSeconds": 2642400,
              "departurePreparationOffsetSeconds": 2556000
            },
            "costCp": 400,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "water-human-0",
            "item": "potable water",
            "amount": {
              "numerator": 64,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 64,
              "denominator": 1
            },
            "costCp": 8,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "feed-0",
            "item": "species-compatible mule feed",
            "amount": {
              "numerator": 20,
              "denominator": 1
            },
            "unit": "lb",
            "massLb": {
              "numerator": 20,
              "denominator": 1
            },
            "costCp": 10,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "water-mule-0",
            "item": "potable water",
            "amount": {
              "numerator": 48,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 48,
              "denominator": 1
            },
            "costCp": 6,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "sundries-0",
            "item": "ordinary expendable cleaning cloth and twine",
            "amount": {
              "numerator": 2,
              "denominator": 1
            },
            "unit": "lb",
            "massLb": {
              "numerator": 2,
              "denominator": 1
            },
            "costCp": 16,
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-1",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-1",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-2",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-2",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-3",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-3",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-4",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-4",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-5",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-5",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-6",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-6",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-7",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-7",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          },
          {
            "id": "oil-8",
            "item": "compatible lamp oil",
            "amount": {
              "numerator": 1,
              "denominator": 1
            },
            "unit": "pint",
            "massLb": {
              "numerator": 3,
              "denominator": 4
            },
            "containerId": "flask-8",
            "costCp": 10,
            "fullInclusiveMassLb": {
              "numerator": 1,
              "denominator": 1
            },
            "owner": "Expedition-1",
            "origin": "actual finite stock sold before this descent, synthetic seller receipt",
            "creationByRule": false,
            "transfersResetAge": false,
            "restrictions": [
              "ordinary nonmagical stock; no recipe/harvest output implied"
            ]
          }
        ],
        "containers": [
          {
            "id": "skin-01",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-02",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-03",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-04",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-05",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-06",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-07",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-08",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-09",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-10",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-11",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-12",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-13",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-14",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-15",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-16",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-human-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-17",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-18",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-19",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-20",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-21",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-22",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-23",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-24",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-25",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-26",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-27",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "skin-28",
            "emptyMassLb": 1,
            "capacityPints": 4,
            "openingContents": {
              "lot": "water-mule-0",
              "pints": 4
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-1",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-1",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-2",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-2",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-3",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-3",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-4",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-4",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-5",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-5",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-6",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-6",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-7",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-7",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "flask-8",
            "emptyMassLb": {
              "numerator": 1,
              "denominator": 4
            },
            "capacityPints": 1,
            "openingContents": {
              "lot": "oil-8",
              "pints": 1
            },
            "location": "Cart-1",
            "retainedWhenEmpty": true,
            "cleanAndCompatible": true
          },
          {
            "id": "feedbag-1",
            "emptyMassLb": 1,
            "capacityLb": 10,
            "openingContents": {
              "lot": "feed-0",
              "lb": 10
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true
          },
          {
            "id": "feedbag-2",
            "emptyMassLb": 1,
            "capacityLb": 10,
            "openingContents": {
              "lot": "feed-0",
              "lb": 10
            },
            "location": "Cart-1",
            "ownedBeforeEpisode": true
          }
        ],
        "packing": {
          "initialPreallocationPayloadLb": 188,
          "initialGrossDrawLb": 388,
          "contentsFit": {
            "bedFt": [
              6,
              4,
              3
            ],
            "allocatedStorageFt3": 24,
            "longestPackedBundleFt": 3,
            "crateFt": [
              2,
              1,
              1
            ],
            "closure": "sealed skins and flasks; lashed food/feed bags and closed crate"
          },
          "noDoubleTare": "8 full 1-lb flasks already include 2 lb of flask bodies; water is separate from the 28 one-pound skins."
        }
      },
      "newStock": {
        "id": "next-procurement",
        "payment": "next-stock",
        "start": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 228600,
          "departurePreparationOffsetSeconds": 142200
        },
        "completion": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 229920,
          "departurePreparationOffsetSeconds": 143520
        },
        "newOriginLots": [
          {
            "id": "food-next",
            "lb": 16
          },
          {
            "id": "water-human-next",
            "pints": 64
          },
          {
            "id": "feed-next",
            "lb": 20
          },
          {
            "id": "water-mule-next",
            "pints": 48
          },
          {
            "id": "sundries-next",
            "lb": 2
          },
          {
            "id": "oil-next-1",
            "pints": 1,
            "container": "next-flask-1"
          },
          {
            "id": "oil-next-2",
            "pints": 1,
            "container": "next-flask-2"
          },
          {
            "id": "oil-next-3",
            "pints": 1,
            "container": "next-flask-3"
          },
          {
            "id": "oil-next-4",
            "pints": 1,
            "container": "next-flask-4"
          },
          {
            "id": "oil-next-5",
            "pints": 1,
            "container": "next-flask-5"
          },
          {
            "id": "oil-next-6",
            "pints": 1,
            "container": "next-flask-6"
          },
          {
            "id": "oil-next-7",
            "pints": 1,
            "container": "next-flask-7"
          },
          {
            "id": "oil-next-8",
            "pints": 1,
            "container": "next-flask-8"
          }
        ],
        "waterFilling": {
          "interval": {
            "startSeconds": 228600,
            "endSeconds": 229020,
            "activeSeconds": 420,
            "halfOpen": true
          },
          "workers": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "assignment": {
            "Arin": [
              "skin-01",
              "skin-02",
              "skin-03",
              "skin-04",
              "skin-05",
              "skin-06",
              "skin-07"
            ],
            "Bea": [
              "skin-08",
              "skin-09",
              "skin-10",
              "skin-11",
              "skin-12",
              "skin-13",
              "skin-14"
            ],
            "Cora": [
              "skin-15",
              "skin-16",
              "skin-17",
              "skin-18",
              "skin-19",
              "skin-20",
              "skin-21"
            ],
            "Dane": [
              "skin-22",
              "skin-23",
              "skin-24",
              "skin-25",
              "skin-26",
              "skin-27",
              "skin-28"
            ]
          },
          "minutesPerSkin": 1,
          "totalWorkerMinutes": 28,
          "elapsedMinutes": 7
        },
        "remainingPacking": {
          "interval": {
            "startSeconds": 229020,
            "endSeconds": 229920,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "workers": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "method": "Receive sealed fitting bundles, place/secure disjoint bundles with actual access; no new harness or vehicle is purchased"
        },
        "oldContainerHistoryRetained": true,
        "nextPreallocationPayloadUpperBoundLb": 190,
        "newFuelAlreadyInLanternBAtDeparturePints": 1,
        "oldOilAtDeparturePints": 0,
        "costChargedToCompletedEpisodeAgain": 0
      }
    },
    "result": "actual accepted sale, paid services and completed rest; no training or craft completion",
    "advancement": {
      "mode": "milestone",
      "achievement": "licensed-crate-retrieval",
      "contributingCharacters": [
        "Arin",
        "Bea",
        "Cora",
        "Dane"
      ],
      "largerMilestoneCompleted": false,
      "XP": 0,
      "newLevels": 0,
      "recordedProgress": true
    },
    "stateCarry": {
      "time": {
        "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
        "elapsedSeconds": 259200,
        "departurePreparationOffsetSeconds": 172800
      },
      "cashCp": 4480,
      "Pressure": 3,
      "oldPhysicalStockRemaining": {
        "humanFoodLb": {
          "numerator": 0,
          "denominator": 1
        },
        "humanWaterPints": {
          "numerator": 0,
          "denominator": 1
        },
        "muleFeedLb": {
          "numerator": 0,
          "denominator": 1
        },
        "muleWaterPints": {
          "numerator": 0,
          "denominator": 1
        },
        "sundriesLb": {
          "numerator": 0,
          "denominator": 1
        },
        "oilPints": {
          "numerator": 0,
          "denominator": 1
        }
      },
      "oldOilUsedPints": {
        "numerator": 8,
        "denominator": 1
      },
      "retainedFlaskBodyMassLb": {
        "numerator": 2,
        "denominator": 1
      },
      "newStockPurchased": true,
      "newStockIsOldStockRefill": false,
      "crateCustodian": "Pera",
      "humanHP": {
        "Arin": 20,
        "Bea": 20,
        "Cora": 20,
        "Dane": 20
      },
      "muleHP": 20,
      "cartHP": 30,
      "humanStrain": {
        "Arin": 0,
        "Bea": 0,
        "Cora": 0,
        "Dane": 0
      },
      "RestDebtOwed": {
        "Arin": false,
        "Bea": false,
        "Cora": false,
        "Dane": false
      },
      "guildStanding": 1,
      "newLevelsAwarded": 0,
      "beneficialLongRestsSinceDeparture": 1,
      "newSpellClassFeatPromotions": 0
    },
    "continuation": {
      "nextCharter": "charter-2",
      "newInsuranceAssumed": false,
      "Pressure": 3,
      "stock": {
        "id": "next-procurement",
        "payment": "next-stock",
        "start": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 228600,
          "departurePreparationOffsetSeconds": 142200
        },
        "completion": {
          "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
          "elapsedSeconds": 229920,
          "departurePreparationOffsetSeconds": 143520
        },
        "newOriginLots": [
          {
            "id": "food-next",
            "lb": 16
          },
          {
            "id": "water-human-next",
            "pints": 64
          },
          {
            "id": "feed-next",
            "lb": 20
          },
          {
            "id": "water-mule-next",
            "pints": 48
          },
          {
            "id": "sundries-next",
            "lb": 2
          },
          {
            "id": "oil-next-1",
            "pints": 1,
            "container": "next-flask-1"
          },
          {
            "id": "oil-next-2",
            "pints": 1,
            "container": "next-flask-2"
          },
          {
            "id": "oil-next-3",
            "pints": 1,
            "container": "next-flask-3"
          },
          {
            "id": "oil-next-4",
            "pints": 1,
            "container": "next-flask-4"
          },
          {
            "id": "oil-next-5",
            "pints": 1,
            "container": "next-flask-5"
          },
          {
            "id": "oil-next-6",
            "pints": 1,
            "container": "next-flask-6"
          },
          {
            "id": "oil-next-7",
            "pints": 1,
            "container": "next-flask-7"
          },
          {
            "id": "oil-next-8",
            "pints": 1,
            "container": "next-flask-8"
          }
        ],
        "waterFilling": {
          "interval": {
            "startSeconds": 228600,
            "endSeconds": 229020,
            "activeSeconds": 420,
            "halfOpen": true
          },
          "workers": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "assignment": {
            "Arin": [
              "skin-01",
              "skin-02",
              "skin-03",
              "skin-04",
              "skin-05",
              "skin-06",
              "skin-07"
            ],
            "Bea": [
              "skin-08",
              "skin-09",
              "skin-10",
              "skin-11",
              "skin-12",
              "skin-13",
              "skin-14"
            ],
            "Cora": [
              "skin-15",
              "skin-16",
              "skin-17",
              "skin-18",
              "skin-19",
              "skin-20",
              "skin-21"
            ],
            "Dane": [
              "skin-22",
              "skin-23",
              "skin-24",
              "skin-25",
              "skin-26",
              "skin-27",
              "skin-28"
            ]
          },
          "minutesPerSkin": 1,
          "totalWorkerMinutes": 28,
          "elapsedMinutes": 7
        },
        "remainingPacking": {
          "interval": {
            "startSeconds": 229020,
            "endSeconds": 229920,
            "activeSeconds": 900,
            "halfOpen": true
          },
          "workers": [
            "Arin",
            "Bea",
            "Cora",
            "Dane"
          ],
          "method": "Receive sealed fitting bundles, place/secure disjoint bundles with actual access; no new harness or vehicle is purchased"
        },
        "oldContainerHistoryRetained": true,
        "nextPreallocationPayloadUpperBoundLb": 190,
        "newFuelAlreadyInLanternBAtDeparturePints": 1,
        "oldOilAtDeparturePints": 0,
        "costChargedToCompletedEpisodeAgain": 0
      }
    }
  }
}
```

### EC-15 — Source preservation, candidate projection and review evidence

```json
{
  "id": "FLOW-EC-15",
  "schemaVersion": "EX58-contract-instance-v1",
  "version": 1,
  "expectedPredecessorVersion": 0,
  "time": {
    "epochId": "EX-FLOW-SYNTHETIC-EPOCH",
    "elapsedSeconds": 259200,
    "departurePreparationOffsetSeconds": 172800,
    "phase": "compiled from history",
    "sequence": 0
  },
  "status": "resolved synthetic record",
  "audience": "public synthetic fixture",
  "evidence": "authored expectation; specific arithmetic checks separately labeled",
  "sourceBindings": [
    {
      "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
      "contractId": "EC-15",
      "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
    }
  ],
  "fields": {
    "sourceManifest": [
      {
        "path": "docs/audit/2026-10-08/full-game/ex58-final-gpt-verdict/EX58_WORKED_SEQUENCES.json",
        "bytes": 73808,
        "sha256": "f668c9aff1c836f61e5766db3eed49d62ba2f1a6d638959157e5551223aa2c80"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/source_contracts_corrected.json",
        "bytes": 32008,
        "sha256": "ff2213df5867e7ec47c22f8cce2ea1a1dfc95a959b7ee11ee6da822eb991a43c"
      },
      {
        "path": "docs/audit/2026-10-08/full-game/EX58_EDIT_01_FULFILLMENT.json",
        "bytes": 5367,
        "sha256": "90db3fc921cb4d5b13cf487e73864c070175bb7b61d0628792e79e70ff72f20a"
      },
      {
        "path": "docs/audit/2026-10-08/full-game/EX58_EDIT_02_FULFILLMENT.json",
        "bytes": 4097,
        "sha256": "a51c4cc61550d63537f42954f2ea587339be2175cf9d5340a7ec3d310f0660aa"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/expedition_candidate/transport_profiles.json",
        "bytes": 120625,
        "sha256": "d2e4a86e66b50f8bc299803838917471997b14040a330bb6d5a1979fd5c35171"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/expedition_candidate/part01.json",
        "bytes": 16955,
        "sha256": "637142593446b495987d610c1c6bfe6dbd45de3ccd3afc90db3d91da7d35d032"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/part01.json",
        "bytes": 81911,
        "sha256": "d017a1f1c8d4852decf20e6d00d7753f3aac925bb69f9ab1d5cf32221e616389"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/expedition_candidate/part02.json",
        "bytes": 23163,
        "sha256": "3f60f72e0a9b9a0e149d717f6faf5b2a49e4796b90247887630b42c66f4457b2"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/part02.json",
        "bytes": 360899,
        "sha256": "01cb20d9f2c92b051f673f098a1cc87bc92613600d3b6eb4b056c86422647c22"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/expedition_candidate/part03.json",
        "bytes": 30125,
        "sha256": "60ba115c981e16b726c932b5b554c25bf0fc7dc43a7b693e2f62799f963911cd"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/part03.json",
        "bytes": 470385,
        "sha256": "4b1a8a40f3e0bfe35a772aa883be0cc98f03d8416e04870b420d9039a048c4e6"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/expedition_candidate/part04.json",
        "bytes": 23675,
        "sha256": "b188a338731af0fc75cab6d95173bbcfdcb0ec831b15674908127e2645688585"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/part04.json",
        "bytes": 3041589,
        "sha256": "772708c2813edc1877ada19894293ef2258efc9e8db1346b1fa9544364d10908"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/expedition_candidate/part05.json",
        "bytes": 43425,
        "sha256": "233d67c982726960aa937db351664420cd4dfad8173653494d47dabe3cb28917"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/part05.json",
        "bytes": 1335367,
        "sha256": "3e67d9f332c6345d3fd3b2fd6a62ea1c9e0168b179b4509fdd5d7d6a1c02e0cc"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/public/expedition_candidate/part06.json",
        "bytes": 21941,
        "sha256": "5bbdf8aa48e0f69fc6e84e598f18f85818d83fed8ce353ad388c8e1ff09422a2"
      },
      {
        "path": "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/part06.json",
        "bytes": 220343,
        "sha256": "6caeb1ab1740c6148148c0cf49220dd6e640256c4c23c410c181f901f9b5218c"
      }
    ],
    "directionBindings": [
      "FL-01",
      "FL-02",
      "FL-03",
      "FL-04",
      "FL-05",
      "FL-08",
      "FL-09",
      "FL-10",
      "FL-12",
      "FL-13",
      "FL-15",
      "FL-16",
      "FL-17",
      "FL-19",
      "FL-20",
      "FL-21",
      "FL-22",
      "FL-23",
      "FL-24",
      "FL-26",
      "TR-01",
      "TR-02",
      "TR-03",
      "TR-07",
      "TR-08",
      "TR-10",
      "TR-12",
      "TR-13",
      "SO-01",
      "SO-02",
      "SO-10",
      "SO-11",
      "RP-A06"
    ],
    "candidateTexts": [
      "DescentReviewChanges/ReviewBible/data/public/expedition_candidate/integrated_flow.json",
      "DescentReviewChanges/ReviewBible/data/director/expedition_candidate/integrated_flow.json",
      "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_INTEGRATED_WALKTHROUGH.md",
      "DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_INTEGRATED_RECORDS.md"
    ],
    "audienceProjection": "Entire public synthetic envelope explicitly authored from public blocks; no original faction dossiers. Saved equality is checked here; independent whole-candidate reconstruction remains an assembly requirement.",
    "evidenceClass": "executed reference arithmetic and source equality; qualitative facts remain authored synthetic expectations",
    "status": "unadopted integrated example; 28 boundaries and 24 social instances still to assemble",
    "deliveryGate": "actual final joint whole-game agreement, already-authorized push, remote verification, then careful cosmology review"
  }
}
```

## Evidence limits

Executed checks cover exact arithmetic, finite origin quantities, explicit actor-interval conflicts, input-byte preservation, source-event retention and public/internal projection equality. They do not authenticate a real route, worker, body, buyer or institution; those are synthetic premises. EC-04 is explicitly unused, and encounter calibration, all cross-domain boundaries and all original social scenario instances remain separate work. No card is promoted, live save migrated, source deleted or GitHub push performed.
