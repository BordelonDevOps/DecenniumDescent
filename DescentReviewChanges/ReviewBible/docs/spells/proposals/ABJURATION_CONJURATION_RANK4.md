# Rank-four Abjuration and Conjuration: operating proposals

**UNADOPTED AND UNSENT.** Fifteen proposed mechanical spell procedures and 30 authored examples. Banishment is preserved as an unchanged post-push receipt, with no new procedure. These drafts have no runtime, balance or joint approval.

[Full structured source/procedure evidence](../../../data/director/spell_proposals/abjuration_conjuration_rank4.json) · [Original source questions](../../../../../docs/audit/2026-10-08/full-game/ABJURATION_CONJURATION_RANK4_SOURCE_AUDIT.md) · [Preservation checks](../../../../../docs/audit/2026-10-08/full-game/ABJURATION_CONJURATION_RANK4_OPERATING_PROPOSAL_CHECK.json)

## Shared rules

### status

UNADOPTED AND UNSENT. Fifteen complete proposed mechanical procedures, not spell approval. Banishment is a literal unchanged post-push receipt with no authored destination, return or cosmological interpretation. Both Alignment Anchor placements are addressed within one original identity; rank7 is never repriced as rank4. No public catalog, class access, ordinary authored-review count or source file is changed.

### casting

Every active proposal uses its actual class access row, minimum class level, independently known/prepared repertoire, school, rank and base RP. All printed activations are Action; components are V/S/F, with Greater Warding’s M/F satisfied by the existing normal focus convention and no invented costly material. Actual surcharges/discounts, sharedRP, Dissonance/Refrain, concentration transitions and legal nested Counterspell windows apply. Commit all costs before effect resolution; interruption, resistance and legal failure do not refund or restore displaced concentration. No generic upcast, automatic scaling, extra action or inferred class-card access.

### clocks

Any proposed minute-long application ends at the caster’s tenth future original regular-start marker, excluding a start already underway, or after 60 elapsed seconds if begun outside initiative. Preserve that original virtual marker/absolute deadline through reorder, extra turns, absence and travel; entering initiative never renews a timer. Other explicit hours/days use actual elapsed time. Suppression does not cure, pause or refill an application; eligibility is reevaluated when it resumes, with no replayed ticks or past failed transitions.

### geometry

Use the current five-foot grid, actual occupied footprints and exact line of effect/cover. No target/location knowledge beyond the source permission. Unless an explicit teleport exception below allows a known unseen destination, creation/direct targeting requires actual perception and line of effect. Hidden eligibility is resolved by the Director after legal commitment and grants no automatic diagnostic. A newly blocked/occupied destination after commitment fails without refund; a known illegal declared choice is rejected before payment.

### arbitration

Current strongest same-stat flat bonuses, one same-type resistance, strongest hostile slow, single tempHP ledger, damage/transfer order, Wound/death rules and one newly established hard whole-Action/turn component per source-character/target/encounter remain. Reviewed Sleep and Hypnotic Pattern establish that a continuing valid hard component does not claim the allowance again each turn; individual durations and repeat saves still govern. A spell does not acquire a pending feat just because their names resemble each other. Copies/reflections preserve causal root and do not generate copies, resources, class procs or a new casting identity.

### audienceAndLore

Faction identity, membership, standing and invocation permission remain distinct actual records. Undefined/null values are preserved, never defaulted or migrated. Alignment and Corruption use only already established mechanical records; no moral doctrine, new axis, origin, plane, soul taxonomy or sealed interpretation is authored. The actual expedition/reputation verdict remains pending, so none of these drafts decides a saved-score migration. New summon profiles are explicit provisional mechanical creations, not imported or certified bestiary facts.

## AC4-02 — Greater Warding

**Original placements, unchanged**

- Abjuration rank 4: Target gains +2 to AC and saves, resistance to spells.

**Proposed procedure**

Action; range 60 feet; V/S/F; concentration up to one minute. Choose one willing creature you perceive with line of effect, including yourself. It receives +2 AC and +2 to ordinary saving throws, plus resistance to damage originating from spells. NEW: interpret resistance to spells as damage resistance, without advantage on saves, effect immunity, absorption or reflection. It covers each spell-origin damage component, including an ongoing spell pulse, but not an ordinary weapon attack enabled by a magical buff or a nonspell technique that spends RP. Generic save bonuses do not modify unmodified death saves. Resolve one applicable resistance per component before a lawful Warding Bond transfer and temporary HP; a transferred packet that forbids second mitigation cannot be halved again through this ward. Same-stat bonuses use the strongest: Warding Bond’s +1 and this +2 give +2. The initial 60-foot range is not an ongoing tether. Suppression removes benefits without pausing the deadline, healing, refilling resources or triggering a new application on return.

**Explicit NEW choices:** NEW: willing recipient and spell-origin damage resistance supply the missing recipient and resistance definition.

**Authored examples**

- A warded ally receives 11 fire damage from a spell. Resistance leaves 5 before a legal Warding Bond split; the transferred share receives no second resistance.

- An ordinary sword attack under a spell buff remains a weapon attack. This ward alone does not halve its ordinary physical damage.

<details><summary>Original question and complete source/access record</summary>

Preserve +2 AC and saves, resistance to spells, Action/60ft and concentration up to1minute. Define recipient/willingness and the exact resistance scope: spell-origin damage, effects or another finite meaning must be decided explicitly. Distinguish flat save modifier from advantage; apply current strongest-stat families and damage ordering with Warding Bond, Shield and Elemental Resistance. It grants no automatic immunity, extra armor formula or absorption/reflection unless expressly authored as NEW. Specify suppress/return/end and multiple-source handling without healing or resource refresh.

```json
{
  "id": "greater-warding",
  "name": "Greater Warding",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Monk": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Paladin": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "greater-warding",
    "original": {
      "name": "Greater Warding",
      "level": 4,
      "resonanceRank": 4,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Greater Warding",
          "school": "Abjuration",
          "level": 4,
          "summary": "Target gains +2 to AC and saves, resistance to spells."
        }
      ],
      "classLevels": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classRanks": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classLearnLevels": {
        "Cleric": 7,
        "Druid": 7,
        "Mage": 7,
        "Monk": 18,
        "Tinker": 14,
        "Wizard": 7,
        "Paladin": 13
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Monk": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Target gains +2 to AC and saves, resistance to spells.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
        "Monk",
        "Tinker",
        "Wizard",
        "Paladin"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 49,
        "original": {
          "school": "Abjuration",
          "level": 4,
          "name": "Greater Warding",
          "effect": "Target gains +2 to AC and saves, resistance to spells.",
          "source_paragraph": 9040,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, M/F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Ward"
          ],
          "rp_cost": 7
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

</details>

## AC4-03 — Spell Shield

**Original placements, unchanged**

- Abjuration rank 4: Reflect spells of 3rd level or lower back at caster.

**Proposed procedure**

Action; range 60 feet; V/S/F. NEW: replace Instantaneous protection metadata with one minute, without concentration, on one willing perceived creature with line of effect. Only one pending Spell Shield can protect a recipient across casters; a successful replacement ends the prior one. Interpret 3rd level and Tier 3 as the triggering spell’s actual generating rank 0–3. Caster level, discounted RP price and target class do not determine eligibility. After ordinary interruption and before any original attack, save or payload resolution, the recipient may spend its Reaction to reflect a hostile pending spell whose only selected creature target is that recipient. The reflected path originates at the protected recipient and ends at the original caster, who must fit the original spell’s creature-type, willingness, range and line-of-effect requirements measured from that return origin. Hidden eligibility is adjudicated without disclosing protected information. Revalidate, then spend the Reaction and consume the shield. Redirect the one payload, retaining the original caster’s ownership, statistics, costs, concentration and causal identity. Resolve its normal attack or save against that caster, with no automatic self-hit or duplicate roll against the former target. Areas, multiple targets, nonspells, copies and already reflected packets are ineligible. A declined or ineligible event leaves the shield available until its original deadline. No legal return target means no reflection. Suppression disables triggering while its timer continues. It cannot reflect its own creation or initiate another reflection/copy chain.

**Explicit NEW choices:** NEW: one-minute, one-use Reaction protection; rank 0–3 translation; return origin at the protected recipient. These explicitly resolve the Action/Instantaneous and level/Tier conflicts.

**Authored examples**

- A rank-3 spell with one hostile creature target can return to its caster if the return target and path are legal. A rank-4 spell remains ineligible even when discounted to 3 RP.

- Two protected creatures cannot bounce one spell indefinitely: the first redirected packet is already reflected and cannot trigger another shield.

<details><summary>Original question and complete source/access record</summary>

Preserve reflection of spells of3rd level or lower in the catalog and Tier3 or lower in Core, with printed Action/60ft/Instantaneous. Resolve that exact terminology conflict and whether an Action establishes protection, readies a later reflection or has another finite source-compatible operation. Define eligible actual spell events, protected recipient, lifetime, trigger/commit timing, destination/range, attack/save/caster ownership, concentration and effect identity. Reflection must preserve real costs and a finite causal history; no new free cast, arbitrary nonspell-power reflection, area immunity or endless mirror loop. Compare Counterspell and pending Soul Mirror/Spell Mirror without merging their identities.

```json
{
  "id": "spell-shield",
  "name": "Spell Shield",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Monk": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Paladin": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "spell-shield",
    "original": {
      "name": "Spell Shield",
      "level": 4,
      "resonanceRank": 4,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Spell Shield",
          "school": "Abjuration",
          "level": 4,
          "summary": "Reflect spells of 3rd level or lower back at caster."
        }
      ],
      "classLevels": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classRanks": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classLearnLevels": {
        "Cleric": 7,
        "Druid": 7,
        "Mage": 7,
        "Monk": 18,
        "Tinker": 14,
        "Wizard": 7,
        "Paladin": 13
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Monk": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Reflect spells of 3rd level or lower back at caster.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
        "Monk",
        "Tinker",
        "Wizard",
        "Paladin"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 50,
        "original": {
          "school": "Abjuration",
          "level": 4,
          "name": "Spell Shield",
          "effect": "Reflect spells of Tier 3 or lower back at caster.",
          "source_paragraph": 9041,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Ward"
          ],
          "rp_cost": 7
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

</details>

## AC4-04 — Dimensional Anchor

**Original placements, unchanged**

- Abjuration rank 4: Prevent teleportation and planar travel in 60-ft radius.

**Proposed procedure**

Action; range 60 feet; V/S/F. NEW: create a fixed 60-foot-radius sphere centered on a perceived point within range and line of effect, with concentration up to one minute. It prevents an actual teleportation or planar-transition transaction when any transported body’s origin or destination footprint intersects the area. Cargo travels with its actual body; an object transported independently uses its own endpoints. Do not test an imaginary path between two outside endpoints. Ordinary travel through the area remains possible. The rule applies to willing, hostile and self transport using established location records; it creates no destination or plane. A portal can remain present, but transit using a blocked endpoint cannot complete. A known obstruction fails preflight before payment; hidden obstruction or a field established after commitment can defeat a paid transit, leaving the entire transaction at its origin. Atomic group travel fails together, without splitting bodies or inventory. Ending or suppressing the field allows future otherwise legal transactions but does not retry or refund past attempts. The field does not suppress summons, images, mundane movement, physical forced displacement, spells generally, or effects merely because they once crossed space. There is no save or physical cage. An explicit source exception can bypass only the prevention it actually names.

**Explicit NEW choices:** NEW: fixed sphere, minute concentration and endpoint-based prevention, with atomic group failure and separate casting range and radius.

**Authored examples**

- Both teleport endpoints outside the sphere permit transit even if a straight line between them crosses the sphere.

- A portal can remain visible while its endpoint is blocked. A transit defeated after commitment leaves the traveler and real gear at the origin, with costs spent.

<details><summary>Original question and complete source/access record</summary>

Preserve prevention of teleportation and planar travel in a60ft radius, Action/60ft/Instantaneous. Resolve radius versus casting range, actual center/shape and duration/concentration for this prevention. Define origin,destination,path/boundary eligibility, preflight and committed failures, willing/hostile travel, ongoing portals and suppression/ending under existing spell-event ownership. Do not invent a new plane or alter existing topology; only evaluate already established location/transport records. It supplies no physical cage, movement prohibition, resource refund or generic immunity to unrelated displacement by its name.

```json
{
  "id": "dimensional-anchor",
  "name": "Dimensional Anchor",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Monk": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Paladin": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "dimensional-anchor",
    "original": {
      "name": "Dimensional Anchor",
      "level": 4,
      "resonanceRank": 4,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Dimensional Anchor",
          "school": "Abjuration",
          "level": 4,
          "summary": "Prevent teleportation and planar travel in 60-ft radius."
        }
      ],
      "classLevels": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classRanks": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classLearnLevels": {
        "Cleric": 7,
        "Druid": 7,
        "Mage": 7,
        "Monk": 18,
        "Tinker": 14,
        "Wizard": 7,
        "Paladin": 13
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Monk": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Prevent teleportation and planar travel in 60-ft radius.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
        "Monk",
        "Tinker",
        "Wizard",
        "Paladin"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 51,
        "original": {
          "school": "Abjuration",
          "level": 4,
          "name": "Dimensional Anchor",
          "effect": "Prevent teleportation and planar travel in 60-ft radius.",
          "source_paragraph": 9042,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Movement",
            "Planar"
          ],
          "rp_cost": 7
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

</details>

## AC4-05 — Corruption Barrier

**Original placements, unchanged**

- Abjuration rank 4: Create a wall that blocks and damages corrupted creatures.

**Proposed procedure**

Action; range 60 feet; V/S/F; concentration up to one minute. NEW: create a visible nonphysical warding plane up to 30 feet long, 10 feet high and 1 foot thick on supported ground. Every point must be within range and line of effect when created. Its thickness cannot overlap an occupied body or forcibly relocate one. Only an actual active Corrupted condition, or a source record explicitly granting equivalent mechanical eligibility, makes a creature affected. Appearance, ancestry, faction, alignment, spell tags and unrelated disease do not establish that predicate. Suppressed eligibility does not qualify while suppressed. The plane blocks affected creatures’ voluntary or forced physical crossing, including carriage, stopping that movement at the boundary. A teleport destination overlapping its thickness is blocked; a fitting destination beyond it does not cross a physical path and is allowed unless another rule prevents transport. It supplies no support against unsupported Falling; such falling can cross with the same contact damage and continues normally. The first attempted physical crossing or blocked destination contact per creature per numbered round deals 2d6 radiant, with a CON save for half rounded down; passing does not bypass the barrier. Across overlapping barriers use the earliest eligible active application for that event and one spell-family contact packet per creature per round. Exposure is spent even if defenses prevent all damage. Outside initiative use consecutive six-second intervals anchored to the first contact, preserving the open interval on entering initiative. A simultaneous group contact shares one damage roll, with separate saves and defenses. Nonmatching creatures, objects and attacks pass. There is no sight obstruction, cover, universal physical wall, diagnostic report or harvestable substance. Going around an edge remains possible; standing near the wall adds no tick. The caster is affected if eligible.

**Explicit NEW choices:** NEW: finite selective plane, actual Corrupted predicate, bounded 2d6 contact across overlapping sources, endpoint-only teleport contact and no support against falling.

**Authored examples**

- A Corrupted creature fails its CON save on its first crossing attempt: it takes the rolled 2d6 and stops before the wall. Success halves damage but still blocks crossing.

- A creature without actual Corrupted eligibility can cross. A fitting teleport destination beyond the wall also avoids contact; neither grants hidden moral or origin information.

<details><summary>Original question and complete source/access record</summary>

Preserve a wall that both blocks and damages corrupted creatures, Action/60ft and concentration up to1minute. Supply finite geometry, eligible support/placement, sight/line/cover, damage/type/resolution, trigger cadence and entry/forced-movement cases. Corrupted eligibility must reference current mechanically established corruption records, not donor names, appearance, morality or a new cosmological category. Determine nonmatching creatures, objects, attacks and caster crossing without silently making a universal solid wall or automatic corruption detector. Preserve both printed functions and actual material/creature identity.

```json
{
  "id": "corruption-barrier",
  "name": "Corruption Barrier",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Monk": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Paladin": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "corruption-barrier",
    "original": {
      "name": "Corruption Barrier",
      "level": 4,
      "resonanceRank": 4,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Corruption Barrier",
          "school": "Abjuration",
          "level": 4,
          "summary": "Create a wall that blocks and damages corrupted creatures."
        }
      ],
      "classLevels": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classRanks": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classLearnLevels": {
        "Cleric": 7,
        "Druid": 7,
        "Mage": 7,
        "Monk": 18,
        "Tinker": 14,
        "Wizard": 7,
        "Paladin": 13
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Monk": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Create a wall that blocks and damages corrupted creatures.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
        "Monk",
        "Tinker",
        "Wizard",
        "Paladin"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 52,
        "original": {
          "school": "Abjuration",
          "level": 4,
          "name": "Corruption Barrier",
          "effect": "Create a wall that blocks and damages corrupted creatures.",
          "source_paragraph": 9043,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Ward",
            "Corruption"
          ],
          "rp_cost": 7
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

</details>

## AC4-06 — Resonance Dampening Field

**Original placements, unchanged**

- Abjuration rank 4: All spellcasting in area costs +2 Resonance Points.

**Proposed procedure**

Action; range 60 feet; V/S/F. NEW: create a fixed 20-foot-radius sphere at a perceived point with line of effect, with concentration up to one minute. All actual spellcasting by a creature whose occupied space intersects the active area costs an additional 2 RP. Determine caster position at legal cast commitment, not a projection’s origin or a later release. Apply this mandatory surcharge after ordinary source/base waivers and reductions, before the reviewed final Resonance Influence adjustment. Overlapping instances add only one +2, retaining each source and deadline. Cantrips, Reaction spells and normally free or charged spell activations also incur it. NEW: for this field only, a spell route with no normal RP price acquires an additional 2-RP payment requirement; it does not acquire an RP pool. A creature with no pool cannot afford a positive final RP payment. Final Influence can modify this actual new price once. Nonspell techniques, Oracle RC abilities not classified as spells, ongoing concentration, creature attacks and a readied spell’s release are not new casts. Rituals pay at actual casting commitment, not each work interval. Preflight the full final price, action, components and other costs together. Suppression, exit, resistance or countering after commitment gives no refund. The field does not retroactively surcharge the cast that created it.

**Explicit NEW choices:** NEW: finite area/duration, additional RP interface for normally free or charged spells, and ordering before final Influence.

**Authored examples**

- A 0-RP cantrip inside costs 2 RP; an applicable final Ease adjustment of −1 makes 1 RP. A caster without an RP pool cannot commit it.

- Two overlapping fields still add only 2 RP. Releasing a spell already prepared with Ready does not pay again.

<details><summary>Original question and complete source/access record</summary>

Preserve all spellcasting in the area costing +2 RP, Action/60ft/Instantaneous. Define finite area/center/lifetime/concentration, qualifying caster position and final-price checkpoint, including cantrips, reactions, rituals, item activations and effects that merely continue. Resolve duplicate fields and interaction with reviewed Resonance Influence without silently dropping the printed surcharge. Apply current affordability-before-payment and actual-cast identity; no partial payments, repeated child-effect charges, retroactive drain/refund or extra cost on noncasting powers inferred from a tag.

```json
{
  "id": "resonance-dampening-field",
  "name": "Resonance Dampening Field",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Monk": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Paladin": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "resonance-dampening-field",
    "original": {
      "name": "Resonance Dampening Field",
      "level": 4,
      "resonanceRank": 4,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Resonance Dampening Field",
          "school": "Abjuration",
          "level": 4,
          "summary": "All spellcasting in area costs +2 Resonance Points."
        }
      ],
      "classLevels": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classRanks": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classLearnLevels": {
        "Cleric": 7,
        "Druid": 7,
        "Mage": 7,
        "Monk": 18,
        "Tinker": 14,
        "Wizard": 7,
        "Paladin": 13
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Monk": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "All spellcasting in area costs +2 Resonance Points.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
        "Monk",
        "Tinker",
        "Wizard",
        "Paladin"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 53,
        "original": {
          "school": "Abjuration",
          "level": 4,
          "name": "Resonance Dampening Field",
          "effect": "All spellcasting in area costs +2 Resonance Points.",
          "source_paragraph": 9044,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Resonance"
          ],
          "rp_cost": 7
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

</details>

## AC4-07 — Faction Sanctuary

**Original placements, unchanged**

- Abjuration rank 4: Area becomes sacred to a faction; members gain benefits while inside.

**Proposed procedure**

Action; range 60 feet; V/S/F. NEW: create a fixed 20-foot-radius, 10-foot-high area on immobile supported ground you perceive with line of effect, with concentration up to ten minutes. Choose an actual canonical faction for which you already have invocation permission. Choose one benefit: Protection gives +2 AC; Resolve gives +2 to ordinary saves; Steadiness gives advantage on actual checks or saves to resist an effect explicitly inflicting Frightened, or to end that condition through a check or save its source already allows. No new escape check is created. Recipients must actually be members of that faction, occupy the area and have line of effect to its center at the relevant event. Standing, affiliation, disguise and missing membership records do not substitute. Hidden membership is resolved without public disclosure. Ordinary strongest-stat and advantage rules apply. Entering, leaving, membership changes and suppression change eligibility immediately, without new uses or grace periods. Visitors can freely enter or leave; attacks are not blocked. The visible emblem grants no law, ownership, rest success, healing, resources or allegiance. The source’s word sacred is preserved without adding theology. Ten minutes uses 100 future regular-start markers or 600 elapsed seconds under the shared clock; extra turns do not shorten it.

**Explicit NEW choices:** NEW: three finite benefits, actual invocation and membership requirements, and a ten-minute area without institutional or cosmological grants.

**Authored examples**

- Protection overlaps a +1 AC ward. A qualifying member receives +2, rather than +3.

- Favorable standing does not establish membership and supplies no sanctuary bonus by itself.

<details><summary>Original question and complete source/access record</summary>

Preserve an area sacred to a faction with benefits for members, Action/60ft/Instantaneous. Author a finite mechanical benefit menu and area/lifetime/concentration, actual faction choice and membership evidence, entry/exit/suppression, overlap and visitors. Distinguish membership from reputation and from opposing alignment; compare Faction Ward, Faction Seal and Greater Faction Emblem. The word sacred supplies no new deity, ownership, legal immunity, cosmology or automatic change in allegiance/reputation. Retain any unresolved faction identity/membership facts as explicit dependencies rather than fabricating a roster.

```json
{
  "id": "faction-sanctuary",
  "name": "Faction Sanctuary",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Monk": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Paladin": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "faction-sanctuary",
    "original": {
      "name": "Faction Sanctuary",
      "level": 4,
      "resonanceRank": 4,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Faction Sanctuary",
          "school": "Abjuration",
          "level": 4,
          "summary": "Area becomes sacred to a faction; members gain benefits while inside."
        }
      ],
      "classLevels": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classRanks": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classLearnLevels": {
        "Cleric": 7,
        "Druid": 7,
        "Mage": 7,
        "Monk": 18,
        "Tinker": 14,
        "Wizard": 7,
        "Paladin": 13
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Monk": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Area becomes sacred to a faction; members gain benefits while inside.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
        "Monk",
        "Tinker",
        "Wizard",
        "Paladin"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 54,
        "original": {
          "school": "Abjuration",
          "level": 4,
          "name": "Faction Sanctuary",
          "effect": "Area becomes sacred to a faction; members gain benefits while inside.",
          "source_paragraph": 9045,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Ward",
            "Faction"
          ],
          "rp_cost": 7
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

</details>

## AC4-08 — Alignment Lock

**Original placements, unchanged**

- Abjuration rank 4: Prevent target from changing alignment for 24 hours.

**Proposed procedure**

Action; range 60 feet; V/S/F. One perceived creature with line of effect makes a CHA save. NEW: a willing creature can elect failure before the roll. Success causes no application; failure establishes a nonconcentration lock lasting 24 elapsed hours. Record each currently defined effective canonical alignment axis; undefined axes remain undefined and unprotected. While operative, the lock prevents a recorded effective value from being replaced by a different one. It neither reveals values nor compels conduct. Underlying progression, Corrupted and other independent records continue to change and remain recorded, but a locked axis exposes its fixed value to mechanical alignment queries until the lock ends. Display-only masks retain their own rules and do not become actual state changes. NEW: use the earliest active eligible lock for each axis; later conflicting applications retain their own snapshots and deadlines but are suppressed for that axis. Ending exposes the current underlying state without restoring an old baseline or erasing another source’s record. Suppression retains the clock and can expose underlying changes without replaying them when the lock resumes. A prevented transition does not refund a paid cost or queue a later free attempt. Explicit absolute-source exceptions and information protections retain their scope. This grants no moral judgment, oath override or personality restriction.

**Explicit NEW choices:** NEW: CHA save with voluntary failure, effective-axis snapshots, retained underlying records and deterministic per-axis priority.

**Authored examples**

- A locked axis stays at its recorded effective value while an independent underlying change is retained. Expiry exposes that current underlying record.

- An undefined axis is not assigned Neutral. An observer does not automatically learn a hidden locked value.

<details><summary>Original question and complete source/access record</summary>

Preserve preventing a target from changing alignment for24hours, Action/60ft. Resolve target/save/willingness, scope of prevented transitions, existing masks versus true underlying records, suppression and ending. Use current alignment record distinctions and reviewed Alignment Suggestion/Revelation/Sanctuary. No new axis, moral doctrine, cosmic influence or prediction of player choices is requested. Preventing a state change does not itself grant behavioral compulsion, reveal alignment or erase an existing effect; specify the actual rule at each attempted transition without refund/reset.

```json
{
  "id": "alignment-lock",
  "name": "Alignment Lock",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Monk": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Abjuration",
      "baseRpCost": 7
    },
    "Paladin": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "alignment-lock",
    "original": {
      "name": "Alignment Lock",
      "level": 4,
      "resonanceRank": 4,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Alignment Lock",
          "school": "Abjuration",
          "level": 4,
          "summary": "Prevent target from changing alignment for 24 hours."
        }
      ],
      "classLevels": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classRanks": {
        "Cleric": 4,
        "Druid": 4,
        "Mage": 4,
        "Monk": 4,
        "Tinker": 4,
        "Wizard": 4,
        "Paladin": 4
      },
      "classLearnLevels": {
        "Cleric": 7,
        "Druid": 7,
        "Mage": 7,
        "Monk": 18,
        "Tinker": 14,
        "Wizard": 7,
        "Paladin": 13
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Monk": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Prevent target from changing alignment for 24 hours.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
        "Monk",
        "Tinker",
        "Wizard",
        "Paladin"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 55,
        "original": {
          "school": "Abjuration",
          "level": 4,
          "name": "Alignment Lock",
          "effect": "Prevent target from changing alignment for 24 hours.",
          "source_paragraph": 9046,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "24 hours",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Alignment"
          ],
          "rp_cost": 7
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

</details>

## AC4-09 — Alignment Anchor

**Original placements, unchanged**

- Abjuration rank 7: Fix a creature's alignment for 7 days; they cannot act against it.

- Conjuration rank 4: Create a zone where creatures cannot change alignment.

**Proposed procedure**

Keep both actual placements separate. Conjuration rank 4, base 7 RP, range 60 feet: NEW Action, V/S/F creates a fixed 15-foot-radius sphere at a perceived point with line of effect, with concentration up to one minute. Snapshot each creature’s defined effective axes when it first occupies the area with line of effect to the center, including eligible occupants at creation. While eligible inside, those axes use Alignment Lock’s proposed prevention and underlying-history rules. No save or entry bar applies. Leaving removes the constraint immediately; reentry reuses that application’s first snapshot. Store priority when the application first qualifies on that creature/axis. Exit or suppression makes it inactive for priority selection without changing the original timestamp on resumption. Abjuration rank 7, base 17 RP, range 120 feet, currently Cleric: NEW Action, V/S/F targets one perceived creature with line of effect for a CHA save; a willing target can elect failure. Failure applies the effective-axis lock for seven elapsed days without concentration. Preserve cannot act against it as a bounded conduct restriction: only deliberate conduct explicitly incompatible with the locked record under an already established source predicate can be vetoed. A player chooses another legal action without spending the rejected choice’s costs; no beliefs, self-harm, confession, allegiance or new moral standard is compelled. Without an established incompatibility predicate, the clause has no invented test. A veto that would leave no legal ordinary Action or deny the whole turn additionally requires and spends the shared hard-denial allowance; after it is spent, such a whole-Action/turn veto cannot recur that encounter. The axis lock and independently legal narrower restriction continue. This NEW limiting interpretation is a proposal beside the broader original, not recovered doctrine. Neither placement grants the other’s mode, rank, price or class access.

**Explicit NEW choices:** NEW: two placement-specific procedures, explicit zone snapshot/priority handling, and conduct restrictions using existing predicates and shared control history.

**Authored examples**

- The Cleric placement remains rank 7 and base 17 RP. A Druid’s rank-4 zone does not lower that price or grant its own seven-day single-target mode.

- A Director cannot invent a moral requirement forcing a player to attack an ally. No established incompatibility predicate means no conduct veto.

<details><summary>Original question and complete source/access record</summary>

Preserve both placements: Abjuration rank7/17RP/120ft/seven days fixes one creature alignment and prevents acting against it; Conjuration rank4/7RP/60ft/Instantaneous creates a zone preventing alignment change. Decide identity and placement-specific procedures explicitly; never grant Cleric the global minimum rank/cost or silently merge the two promises. Define target/zone/save/willingness, finite duration for the zone, actual recorded alignment, masks versus underlying changes, and handling of the rank7 behavior clause under current compulsion rules. Preserve player agency boundaries without deleting the printed clause. This is a mechanical source question, not a new moral axis, cosmological force or theology review.

```json
{
  "id": "alignment-anchor",
  "name": "Alignment Anchor",
  "schools": [
    "Abjuration",
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 17
    },
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "alignment-anchor",
    "original": {
      "name": "Alignment Anchor",
      "level": 4,
      "resonanceRank": 4,
      "school": "Abjuration",
      "schools": [
        "Abjuration",
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Alignment Anchor",
          "school": "Abjuration",
          "level": 7,
          "summary": "Fix a creature's alignment for 7 days; they cannot act against it."
        },
        {
          "name": "Alignment Anchor",
          "school": "Conjuration",
          "level": 4,
          "summary": "Create a zone where creatures cannot change alignment."
        }
      ],
      "classLevels": {
        "Cleric": 7,
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classRanks": {
        "Cleric": 7,
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classLearnLevels": {
        "Cleric": 13,
        "Dragoon": 18,
        "Druid": 7,
        "Mage": 7,
        "Ranger": 13,
        "Shaman": 10,
        "Tinker": 14,
        "Wizard": 7
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Dragoon": "Conjuration",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Fix a creature's alignment for 7 days; they cannot act against it.",
      "alternateSummaries": [
        "Create a zone where creatures cannot change alignment."
      ],
      "classes": [
        "Cleric",
        "Dragoon",
        "Druid",
        "Mage",
        "Ranger",
        "Shaman",
        "Tinker",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 78,
        "original": {
          "school": "Abjuration",
          "level": 7,
          "name": "Alignment Anchor",
          "effect": "Fix a creature's alignment for 7 days; they cannot act against it.",
          "source_paragraph": 9075,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "7 days",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Alignment"
          ],
          "rp_cost": 17
        }
      },
      {
        "index": 159,
        "original": {
          "school": "Conjuration",
          "level": 4,
          "name": "Alignment Anchor",
          "effect": "Create a zone where creatures cannot change alignment.",
          "source_paragraph": 9175,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Alignment"
          ],
          "rp_cost": 7
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Class-specific ranks differ; never use global minimum rank for every class",
    "Core resolution requires an explicit operational interpretation",
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

</details>

## AC4-10 — Summon Water Pet

**Original placements, unchanged**

- Conjuration rank 4: HP 35, AC 14, can heal allies for 2d6 or attack for 1d10 cold.

**Proposed procedure**

Action; range 60 feet; V/S/F; concentration up to one minute. Create one Medium Elemental companion in a perceived fitting unoccupied supported space with line of effect. Preserve printed AC 14, HP 35, 2d6 healing and 1d10 cold attack. NEW profile: walking Speed 30 feet, body mass 150 pounds, all six ability scores 10, saves equal to your PB, other checks +0, ordinary sight/hearing. It understands your spoken commands without speech or telepathy. No swimming, amphibious trait, fluid passage, immunity or free water follows from its name. It acts immediately after your regular turn. A Bonus Action command while within 60 feet and able to perceive you permits movement and one attack, heal, Dodge, Dash, Disengage or Search. Without a command it can move defensively and Dodge. No free Help, grapple, shove, item activation or opportunity attack is granted. Attack: one melee spell attack using your actual casting ability + PB, reach 5 feet, 1d10 cold without a modifier. Heal: one willing living creature it perceives within 5 feet and line of effect regains 2d6 ordinary HP without a modifier. A Downed recipient is eligible under its actual healing rules. NEW: either attack or heal consumes the owner’s one shared companion offensive/support activation for that numbered round. One companion therefore cannot heal while another uses that same offensive allowance. Each command still costs its actual Bonus Action; extra turns or repeated commands add no activations. Healing belongs to the pet, without triggering the owner’s personal spell, lifesteal or class hooks; no healing copy, resource conversion or overflow is added. One Water Pet per caster; successful replacement ends the old body. At 0 HP or source end it vanishes without a corpse, loot, death reward or material water. It can carry genuinely entrusted existing gear within its actual capacity; real cargo drops legally on ending. Suppression preserves the existing body/HP and deadline without movement, attack, healing or a fresh summon trigger until resumption.

**Explicit NEW choices:** NEW: complete finite body/command profile, melee/healing ranges, and one owner-wide activation shared by attack and healing. Printed healing and attack remain alternatives.

**Authored examples**

- A commanded 2d6 heal can restore a living ally at 0 HP if no actual restriction blocks healing. It spends the round’s shared companion activation.

- The pet has no swim mode simply because it looks like water. Its disappearance produces no harvestable water.

<details><summary>Original question and complete source/access record</summary>

Preserve HP35, AC14 and a choice of healing an ally for2d6 or attacking for1d10 cold, Action/60ft and concentration up to1minute. Supply finite body/size/speed/senses/saves, attack modifier/reach and healing range/target requirements, placement, initiative/commands and the shared offensive-action budget. Resolve whether heal and attack are mutually exclusive uses of its ordinary action and healing of Downed targets using current procedures. Preserve one body, damage/custody history, ending/return placement and no-resource remains. No aquatic adaptation, free water, unlimited independent actions or cosmetic elemental name expands its profile without explicit NEW authoring.

```json
{
  "id": "summon-water-pet",
  "name": "Summon Water Pet",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "summon-water-pet",
    "original": {
      "name": "Summon Water Pet",
      "level": 4,
      "resonanceRank": 4,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Summon Water Pet",
          "school": "Conjuration",
          "level": 4,
          "summary": "HP 35, AC 14, can heal allies for 2d6 or attack for 1d10 cold."
        }
      ],
      "classLevels": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classRanks": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classLearnLevels": {
        "Dragoon": 18,
        "Druid": 7,
        "Mage": 7,
        "Ranger": 13,
        "Shaman": 10,
        "Tinker": 14,
        "Wizard": 7
      },
      "classSchools": {
        "Dragoon": "Conjuration",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "HP 35, AC 14, can heal allies for 2d6 or attack for 1d10 cold.",
      "alternateSummaries": [],
      "classes": [
        "Dragoon",
        "Druid",
        "Mage",
        "Ranger",
        "Shaman",
        "Tinker",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 152,
        "original": {
          "school": "Conjuration",
          "level": 4,
          "name": "Summon Water Pet",
          "effect": "HP 35, AC 14, can heal allies for 2d6 or attack for 1d10 cold.",
          "source_paragraph": 9168,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Damage",
            "Healing",
            "Summoning"
          ],
          "rp_cost": 7
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

</details>

## AC4-11 — Crystalline Barrier

**Original placements, unchanged**

- Conjuration rank 4: Wall of elemental glass (AC 18, HP 40), blocks line of sight.

**Proposed procedure**

Action; range Sight; V/S/F; concentration up to one minute. NEW: choose a clear visible supported location with line of effect, without an invented numeric range cap. Create one opaque wall of elemental glass along a contiguous straight segment, up to 30 feet long, 10 feet high and 1 foot thick. At least one full face of every section must be visible at placement. The thickness cannot bisect, contain or lift a body or object; correct known illegal geometry before payment. AC 18 and 40 HP belong to one whole wall, not each section. Its intact footprint blocks ordinary passage, sight and line of effect, supplying total cover. Glass appearance does not negate printed sight blocking. It is a magical object, not a creature. Damage must legally affect objects; no resistance, threshold or immunity is invented. Damage to any part reduces the same pool; at 0 HP the entire wall vanishes. Targeting a selected 5-foot section uses the actual ordinary attack/action procedure and damages the whole pool; it gives no extra attack or independent hole. Creation inflicts no attack or save. Creatures can go around or over legal edges. The wall cannot carry a building or bridge load, creates no permanent glass or harvest stock, and leaves no damaging shards on ending. Suppression removes its blocking presence while retaining spent HP and the original deadline. If its former footprint is occupied on resumption, it stays suppressed until the whole footprint is clear or it expires; it never evicts, crushes or duplicates an occupant.

**Explicit NEW choices:** NEW: finite opaque geometry, one 40-HP pool, source-specific suppression/resumption occupancy, and no permanent structural or material output.

**Authored examples**

- Hits dealing 23 and 17 damage to different sections deplete the same 40-HP pool and remove the entire wall.

- Sight range permits a distant visible legal segment. It does not reveal placement behind existing total cover.

<details><summary>Original question and complete source/access record</summary>

Preserve a wall of elemental glass with AC18, HP40 and blocked line of sight, Core Action/range Sight/concentration up to1minute. Define finite dimensions/sections, orientation/support, sight to the casting location, occupancy/escape, line of effect/cover, passage, structural damage and section loss. Resolve whether HP40 applies to one whole wall or sections explicitly; do not silently multiply the pool. Appearance as glass does not erase printed sight blocking. No unbounded length, indestructible force-wall traits, duplicated cargo, permanent raw materials or unsupported building support follows from the name.

```json
{
  "id": "crystalline-barrier",
  "name": "Crystalline Barrier",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "crystalline-barrier",
    "original": {
      "name": "Crystalline Barrier",
      "level": 4,
      "resonanceRank": 4,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Crystalline Barrier",
          "school": "Conjuration",
          "level": 4,
          "summary": "Wall of elemental glass (AC 18, HP 40), blocks line of sight."
        }
      ],
      "classLevels": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classRanks": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classLearnLevels": {
        "Dragoon": 18,
        "Druid": 7,
        "Mage": 7,
        "Ranger": 13,
        "Shaman": 10,
        "Tinker": 14,
        "Wizard": 7
      },
      "classSchools": {
        "Dragoon": "Conjuration",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Wall of elemental glass (AC 18, HP 40), blocks line of sight.",
      "alternateSummaries": [],
      "classes": [
        "Dragoon",
        "Druid",
        "Mage",
        "Ranger",
        "Shaman",
        "Tinker",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 153,
        "original": {
          "school": "Conjuration",
          "level": 4,
          "name": "Crystalline Barrier",
          "effect": "Wall of elemental glass (AC 18, HP 40), blocks line of sight.",
          "source_paragraph": 9169,
          "casting_time": "1 action",
          "range": "Sight",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Ward",
            "Detection"
          ],
          "rp_cost": 7
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

</details>

## AC4-12 — Elemental Drain

**Original placements, unchanged**

- Conjuration rank 4: Target loses 2 Resonance Points and takes 3d6 damage (random element).

**Proposed procedure**

Action; range 60 feet; V/S/F; instantaneous. Target one perceived creature with line of effect. NEW: choose Core’s loss of 5 RP over the catalog’s 2 RP, retaining both originals. After interruption, draw 1d6 once: 1 acid, 2 cold, 3 fire, 4 lightning, 5 thunder, 6 poison. Roll 3d6 damage once. The target makes a CON save: failure takes full damage and separately loses up to 5 current RP; success takes half damage rounded down and loses no RP. Apply damage, defenses and survival consequences first. Then, on a failed save, remove min(5, current RP) if the target is still a living holder of an actual RP pool. Damage immunity alone does not cancel this separate failed-save loss. A target without RP still receives eligible damage, with no RC, slot or charge substitution. The caster gains no RP. Save rerolls affect only the permitted save; they never redraw the element or create extra damage rolls. No drain from an ended/dead holder, negative RP, maximum-RP reduction or resource proc is created. Recasting requires a new paid spell. Later suppression cannot reverse resolved damage or RP loss.

**Explicit NEW choices:** NEW: explicit Core 5-RP choice, finite six-element draw, CON save, and separate damage/resource-loss branches.

**Authored examples**

- On a failed save, a surviving target with 3 RP loses 3 and reaches 0. The caster gains 0 RP.

- If fire damage is prevented by immunity but the CON save failed, a living target’s actual RP pool still loses up to 5.

<details><summary>Original question and complete source/access record</summary>

Preserve the exact conflict: catalog target loses2 RP, Core target loses5 RP; both retain3d6 damage of a random element, Action/60ft/Instantaneous. Resolve the drain amount explicitly without rewriting either original. Define attack/save and branch ordering, finite random-element table and one committed draw, current RP floor/target eligibility, damage resolution, suppression and repeat casting. Losing RP does not say the caster gains it. Do not silently create a transfer, draw extra elements on rerolls, let prevention of one component erase the other, or import familiar external-game damage types.

```json
{
  "id": "elemental-drain",
  "name": "Elemental Drain",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "elemental-drain",
    "original": {
      "name": "Elemental Drain",
      "level": 4,
      "resonanceRank": 4,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Elemental Drain",
          "school": "Conjuration",
          "level": 4,
          "summary": "Target loses 2 Resonance Points and takes 3d6 damage (random element)."
        }
      ],
      "classLevels": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classRanks": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classLearnLevels": {
        "Dragoon": 18,
        "Druid": 7,
        "Mage": 7,
        "Ranger": 13,
        "Shaman": 10,
        "Tinker": 14,
        "Wizard": 7
      },
      "classSchools": {
        "Dragoon": "Conjuration",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Target loses 2 Resonance Points and takes 3d6 damage (random element).",
      "alternateSummaries": [],
      "classes": [
        "Dragoon",
        "Druid",
        "Mage",
        "Ranger",
        "Shaman",
        "Tinker",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 154,
        "original": {
          "school": "Conjuration",
          "level": 4,
          "name": "Elemental Drain",
          "effect": "Target loses 5 RP and takes 3d6 damage of a random element.",
          "source_paragraph": 9170,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Damage"
          ],
          "rp_cost": 7
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

</details>

## AC4-13 — Bind Element

**Original placements, unchanged**

- Conjuration rank 4: Trap one elemental creature in place (WIS save or paralyzed 2 rounds).

**Proposed procedure**

Action; range 60 feet; V/S/F. Target one perceived creature with line of effect whose actual current creature-type/profile record is Elemental. Hidden type eligibility is resolved after legal commitment; a spell tag, costume or ingredient is insufficient. The target makes a WIS save. Success causes no application. Failure attempts actual Paralyzed through the end of its second future regular turn, excluding a turn already in progress when applied; no concentration. NEW: repeat the WIS save at the first such turn’s end and end the effect on success. At the second scheduled end it expires without a useless extra save. If begun outside initiative, repeat after six elapsed seconds and expire after twelve; retain that absolute deadline on entering initiative without replaying a save. This preserves the printed two-round clause. Actual paralysis immunity and the shared source-character/target/encounter hard-denial guard apply. Following the reviewed Sleep and Hypnotic Pattern convention, establishing one hard component spends the guard once, not on every affected turn. A spent guard blocks a new Paralyzed application without an invented soft fallback. Recasting, replacement, suppression and ending never refund the mark or extend the old application. Paralyzed retains its full current meaning: Incapacitated, no movement or speech, automatic STR/DEX save failures, advantage on attacks against it, and critical hits for attacks hitting from within 5 feet. Concentration ending and action-type losses follow that condition. No additional damage, strangulation or physical restraint is added. Later suppression retains clocks and history; initial prevention never banks a future application. The spell does not move the body or create support, and ordinary Falling remains possible.

**Explicit NEW choices:** NEW: exact two-turn endpoints, one early repeat save, outside-initiative timing and explicit binding to reviewed once-per-established-application control accounting.

**Authored examples**

- An actual Elemental fails WIS while the source’s shared guard is unused. Paralyzed spends that guard and may end at the first repeat save; persistence through a second turn does not spend another mark.

- A humanoid casting elemental spells is not an Elemental. A real Elemental already hard-controlled by this source character receives no invented fallback from a later failed save.

<details><summary>Original question and complete source/access record</summary>

Preserve one elemental creature, WIS save or Paralyzed for2rounds, Action/60ft/Instantaneous. Bind elemental eligibility to an actual established creature-type/profile record, not any elemental-tagged spell or ingredient. Specify initial success/failure, source-clock endpoints, any repeat saves, parent lifetime/concentration and interaction with the current hard-denial cap and Paralyzed condition. Keep the two-round source clause visible while resolving any cap conflict explicitly; no silent replacement with Restrained, Stunned or arbitrary immunity. Physical position, support and actual custody remain separately governed.

```json
{
  "id": "bind-element",
  "name": "Bind Element",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "bind-element",
    "original": {
      "name": "Bind Element",
      "level": 4,
      "resonanceRank": 4,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Bind Element",
          "school": "Conjuration",
          "level": 4,
          "summary": "Trap one elemental creature in place (WIS save or paralyzed 2 rounds)."
        }
      ],
      "classLevels": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classRanks": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classLearnLevels": {
        "Dragoon": 18,
        "Druid": 7,
        "Mage": 7,
        "Ranger": 13,
        "Shaman": 10,
        "Tinker": 14,
        "Wizard": 7
      },
      "classSchools": {
        "Dragoon": "Conjuration",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Trap one elemental creature in place (WIS save or paralyzed 2 rounds).",
      "alternateSummaries": [],
      "classes": [
        "Dragoon",
        "Druid",
        "Mage",
        "Ranger",
        "Shaman",
        "Tinker",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 155,
        "original": {
          "school": "Conjuration",
          "level": 4,
          "name": "Bind Element",
          "effect": "Trap one elemental creature in place (WIS save or paralyzed 2 rounds).",
          "source_paragraph": 9171,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Wisdom save",
          "tags": [
            "Control"
          ],
          "rp_cost": 7
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

</details>

## AC4-14 — Dimensional Door

**Original placements, unchanged**

- Conjuration rank 4: Teleport up to 500 ft to a known location.

**Proposed procedure**

Action; range 500 feet; V/S/F; instantaneous. Teleport yourself and your actually worn/carried legal gear to one known fitting unoccupied destination on the same established plane. NEW: known means personally perceived now or personally occupied/examined before, with an accurate fixed location relative to your current position. Rumor, approximate direction, imagined layout or a map alone is insufficient. This expressly permits an unseen known destination without line of effect or a traversed path, but grants no remote senses or new place knowledge. Choose one exact footprint and orientation before payment. Recheck occupancy, actual transport prohibitions and custody at resolution. A hidden or newly invalid destination leaves you and all gear at the origin with costs spent, without damage, partial arrival or an automatic nearest-safe substitute. No passenger is granted: a willing or unwilling carried creature is not gear. A genuinely carried unattended object can travel within actual carrying limits, keeping its identity and ownership. Unsupported free space is permitted if the body fits, then ordinary Falling begins immediately; there is no hover. Transit does not end unrelated conditions unless their actual source or physical relationship ends. This Conjuration identity remains distinct from Universal Dimension Door and borrows none of its unreviewed rules.

**Explicit NEW choices:** NEW: self and actual gear, direct destination knowledge, explicit unseen-destination permission and atomic failure, without an imported passenger allowance.

**Authored examples**

- You can return with your real backpack to a personally examined balcony 450 feet away if its arrival space is still legal.

- If that space is secretly occupied, the paid spell fails at the origin. It gives neither an adjacent substitute nor a duplicated backpack.

<details><summary>Original question and complete source/access record</summary>

Preserve teleporting up to500ft to a known location, Core Action/range500ft/Instantaneous. Define who travels, what knowledge establishes the destination, legal space/support, source/destination geometry, actual gear/cargo and willingness/contested cases. Distinguish this Conjuration identity from the separate Universal Dimension Door record. Actual clocks, falling, custody, existing transport-prevention effects and spent resources survive the transit. No bonus passenger, off-map knowledge, interplanar destination or missing-item recreation is inferred from a familiar external spell.

```json
{
  "id": "dimensional-door",
  "name": "Dimensional Door",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "dimensional-door",
    "original": {
      "name": "Dimensional Door",
      "level": 4,
      "resonanceRank": 4,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Dimensional Door",
          "school": "Conjuration",
          "level": 4,
          "summary": "Teleport up to 500 ft to a known location."
        }
      ],
      "classLevels": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classRanks": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classLearnLevels": {
        "Dragoon": 18,
        "Druid": 7,
        "Mage": 7,
        "Ranger": 13,
        "Shaman": 10,
        "Tinker": 14,
        "Wizard": 7
      },
      "classSchools": {
        "Dragoon": "Conjuration",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Teleport up to 500 ft to a known location.",
      "alternateSummaries": [],
      "classes": [
        "Dragoon",
        "Druid",
        "Mage",
        "Ranger",
        "Shaman",
        "Tinker",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 156,
        "original": {
          "school": "Conjuration",
          "level": 4,
          "name": "Dimensional Door",
          "effect": "Teleport up to 500 ft to a known location.",
          "source_paragraph": 9172,
          "casting_time": "1 action",
          "range": "500 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Movement"
          ],
          "rp_cost": 7
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

</details>

## AC4-15 — Resonance Beacon

**Original placements, unchanged**

- Conjuration rank 4: Create a point that allies can teleport to using Resonance Points.

**Proposed procedure**

Action; range 60 feet; V/S/F. NEW: create a visible immobile luminous sigil, 1 foot across, on a perceived supported surface with line of effect, with concentration up to ten minutes. It marks one fitting 5-foot destination square immediately above the surface. At creation enroll yourself and up to PB other willing allies you perceive within 60 feet who can perceive the beacon and consent. Affiliation is not consent. Record exact recipients; later PB changes or remote permission add none. An enrolled living creature on the same plane and within 500 feet of the beacon can spend an Action and 2 of its own actual RP to teleport itself and legally carried gear into that fitting unoccupied square. It need not see the beacon again but gains no updated senses. This is a nonspell activation of the existing spell, with no new cast, Dissonance, Refrain or Counterspell event. Spellcasting-only surcharges and discounts do not modify that payment; a broader actual ability-payment rule applies only if its scope expressly permits. Actual transport prohibitions remain. Preflight known affordability, range and legality; hidden or new obstruction after commitment leaves body and gear at the origin with costs spent. No passenger, creature-as-gear, forced ownership transfer or eviction is granted. Resolve one traveler at a time; another cannot arrive until the square is free. Initial base 7 RP is distinct from each later traveler’s 2 RP. Moving or destroying the marked support ends this fixed beacon. Suppression blocks new transit without queuing attempts or pausing its deadline. One beacon per caster; successful replacement ends the old one. No portal network, refund, RP transfer or item duplication is created.

**Explicit NEW choices:** NEW: finite enrollment, ten-minute concentration, 500-foot self-only use, one arrival square and a separate nonspell Action/2-RP traveler payment.

**Authored examples**

- An enrolled ally spends an Action and 2 RP to arrive in the free square. A second ally must wait until that square is clear.

- Lifting the marked paving stone ends the fixed beacon. It cannot become a free movable destination.

<details><summary>Original question and complete source/access record</summary>

Preserve a created point that allies can teleport to using RP, Action/60ft/Instantaneous. Define the actual point/body, finite lifetime/concentration, destination capacity, eligible allies, access/range, trigger action, participant RP cost and one transfer transaction. Distinguish initial7RP casting cost from any explicit later traveler payment. Decide anchoring/movement, occupancy, obstruction, hostile custody, suppression/destruction/ending and whether multiple travelers can use it, without free repeated movement, duplicate payment, child-triggered refill or invented planar connections. Compare existing Resonance Conduit/Well and Faction Portal, not an automatic stronger copy.

```json
{
  "id": "resonance-beacon",
  "name": "Resonance Beacon",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "resonance-beacon",
    "original": {
      "name": "Resonance Beacon",
      "level": 4,
      "resonanceRank": 4,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Resonance Beacon",
          "school": "Conjuration",
          "level": 4,
          "summary": "Create a point that allies can teleport to using Resonance Points."
        }
      ],
      "classLevels": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classRanks": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classLearnLevels": {
        "Dragoon": 18,
        "Druid": 7,
        "Mage": 7,
        "Ranger": 13,
        "Shaman": 10,
        "Tinker": 14,
        "Wizard": 7
      },
      "classSchools": {
        "Dragoon": "Conjuration",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Create a point that allies can teleport to using Resonance Points.",
      "alternateSummaries": [],
      "classes": [
        "Dragoon",
        "Druid",
        "Mage",
        "Ranger",
        "Shaman",
        "Tinker",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 157,
        "original": {
          "school": "Conjuration",
          "level": 4,
          "name": "Resonance Beacon",
          "effect": "Create a point that allies can teleport to using Resonance Points.",
          "source_paragraph": 9173,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Movement",
            "Resonance"
          ],
          "rp_cost": 7
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

</details>

## AC4-16 — Faction Ally

**Original placements, unchanged**

- Conjuration rank 4: Summon a CR 3 creature aligned with your faction.

**Proposed procedure**

Action; range 60 feet; V/S/F; concentration up to one minute. Require actual membership in a recorded faction and actual invocation permission; favorable standing alone is insufficient. NEW: summon one willing temporary faction-affiliated ally using the complete Faction Envoy profile below, in a perceived fitting unoccupied supported space with line of effect. The profile is designed for the source’s nominal CR 3 role; balance and CR certification remain open. The current public CR-3 entries do not establish both finished mechanics and this caster’s faction relationship; their original profiles remain comparison evidence. Temporary affiliation grants no institutional membership, credentials, secrets, reputation or alignment. Member-only benefits require actual separate membership evidence. The Envoy acts immediately after your regular turn under the actual Bonus Action command and shared offensive-action allowance, using only the profile’s listed actions. Without a command it can move defensively and Dodge. One Envoy per caster; successful replacement, 0 HP or concentration/source ending removes the old body. Real borrowed cargo drops legally without duplication; its conjured blade vanishes. Suppression preserves the same body, HP and deadline without actions, healing or a fresh summon event until resumption. No autonomous attack, loot, corpse, soul/resource reward, free Help or unknown faction information is granted. This summons one finite body; it does not requisition a real NPC or publish Director-only traits.

**Explicit NEW choices:** NEW: finite nominal-CR-3 Envoy for the missing qualified roster, without invented institutional membership or balance certification.

**Authored examples**

- The Envoy’s two attack components use one commanded offensive Action, leaving no shared offensive allowance for another companion that round.

- Favorable reputation alone does not authorize this cast without actual faction membership and invocation permission.

<details><summary>Original question and complete source/access record</summary>

Preserve summoning one CR3 creature aligned with the caster faction, Action/60ft/concentration up to1minute. Define an actual finite eligible source roster or explicit missing-profile dependency, faction evidence, body, initiative/commands/offense budget, summon count/replacement and ending. CR3 alone is not a complete combat profile and must not authorize arbitrary unpublished traits, copied Director secrets or a free adaptable stat block. Faction alignment is not automatically moral alignment. Preserve actual cargo and no-resource summon history, and do not grant faction knowledge, legal access or reputation through the temporary body.

```json
{
  "id": "faction-ally",
  "name": "Faction Ally",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Dragoon": {
      "rank": 4,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Druid": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Mage": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Ranger": {
      "rank": 4,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Shaman": {
      "rank": 4,
      "minimumClassLevel": 10,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Tinker": {
      "rank": 4,
      "minimumClassLevel": 14,
      "school": "Conjuration",
      "baseRpCost": 7
    },
    "Wizard": {
      "rank": 4,
      "minimumClassLevel": 7,
      "school": "Conjuration",
      "baseRpCost": 7
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "faction-ally",
    "original": {
      "name": "Faction Ally",
      "level": 4,
      "resonanceRank": 4,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Faction Ally",
          "school": "Conjuration",
          "level": 4,
          "summary": "Summon a CR 3 creature aligned with your faction."
        }
      ],
      "classLevels": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classRanks": {
        "Dragoon": 4,
        "Druid": 4,
        "Mage": 4,
        "Ranger": 4,
        "Shaman": 4,
        "Tinker": 4,
        "Wizard": 4
      },
      "classLearnLevels": {
        "Dragoon": 18,
        "Druid": 7,
        "Mage": 7,
        "Ranger": 13,
        "Shaman": 10,
        "Tinker": 14,
        "Wizard": 7
      },
      "classSchools": {
        "Dragoon": "Conjuration",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Summon a CR 3 creature aligned with your faction.",
      "alternateSummaries": [],
      "classes": [
        "Dragoon",
        "Druid",
        "Mage",
        "Ranger",
        "Shaman",
        "Tinker",
        "Wizard"
      ],
      "status": "canon",
      "source": "Player Rulebook — Spell Lists"
    },
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "coreEntries": [
      {
        "index": 158,
        "original": {
          "school": "Conjuration",
          "level": 4,
          "name": "Faction Ally",
          "effect": "Summon a CR 3 creature aligned with your faction.",
          "source_paragraph": 9174,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Summoning",
            "Faction"
          ],
          "rp_cost": 7
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

</details>

## Banishment — unchanged post-push receipt

POST-PUSH RECEIPT ONLY. Preserve the source promise of temporary transport to another plane, Core Action/60ft/Instantaneous and all access records without inventing a destination, planar relation, return procedure or new cosmic origin. Carry this unchanged source to the owner-directed careful cosmology review after the successful authorized GitHub push and verified remote commit. Exclude it from present mechanical authoring and approval.

```json
{
  "spellId": "banishment",
  "questionId": "AC4-01",
  "scope": "post-push receipt only",
  "fullSourceAndCurrentAccessRecord": {
    "id": "banishment",
    "name": "Banishment",
    "schools": [
      "Abjuration"
    ],
    "status": "blocked-pending-operational-review",
    "visibility": "public-source-review",
    "classAccess": {
      "Cleric": {
        "rank": 4,
        "minimumClassLevel": 7,
        "school": "Abjuration",
        "baseRpCost": 7
      },
      "Druid": {
        "rank": 4,
        "minimumClassLevel": 7,
        "school": "Abjuration",
        "baseRpCost": 7
      },
      "Mage": {
        "rank": 4,
        "minimumClassLevel": 7,
        "school": "Abjuration",
        "baseRpCost": 7
      },
      "Monk": {
        "rank": 4,
        "minimumClassLevel": 18,
        "school": "Abjuration",
        "baseRpCost": 7
      },
      "Tinker": {
        "rank": 4,
        "minimumClassLevel": 14,
        "school": "Abjuration",
        "baseRpCost": 7
      },
      "Wizard": {
        "rank": 4,
        "minimumClassLevel": 7,
        "school": "Abjuration",
        "baseRpCost": 7
      },
      "Paladin": {
        "rank": 4,
        "minimumClassLevel": 13,
        "school": "Abjuration",
        "baseRpCost": 7
      }
    },
    "operational": null,
    "additionalRpCost": 0,
    "source": {
      "catalogPath": "src/data/spells.js",
      "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
      "catalogKey": "banishment",
      "original": {
        "name": "Banishment",
        "level": 4,
        "resonanceRank": 4,
        "school": "Abjuration",
        "schools": [
          "Abjuration"
        ],
        "placements": [
          {
            "name": "Banishment",
            "school": "Abjuration",
            "level": 4,
            "summary": "Send a creature to another plane temporarily."
          }
        ],
        "classLevels": {
          "Cleric": 4,
          "Druid": 4,
          "Mage": 4,
          "Monk": 4,
          "Tinker": 4,
          "Wizard": 4,
          "Paladin": 4
        },
        "classRanks": {
          "Cleric": 4,
          "Druid": 4,
          "Mage": 4,
          "Monk": 4,
          "Tinker": 4,
          "Wizard": 4,
          "Paladin": 4
        },
        "classLearnLevels": {
          "Cleric": 7,
          "Druid": 7,
          "Mage": 7,
          "Monk": 18,
          "Tinker": 14,
          "Wizard": 7,
          "Paladin": 13
        },
        "classSchools": {
          "Cleric": "Abjuration",
          "Druid": "Abjuration",
          "Mage": "Abjuration",
          "Monk": "Abjuration",
          "Tinker": "Abjuration",
          "Wizard": "Abjuration",
          "Paladin": "Abjuration"
        },
        "castingTime": "Not specified in current rulebook",
        "range": "Not specified in current rulebook",
        "components": "Not specified in current rulebook",
        "duration": "Not specified in current rulebook",
        "description": "Send a creature to another plane temporarily.",
        "alternateSummaries": [],
        "classes": [
          "Cleric",
          "Druid",
          "Mage",
          "Monk",
          "Tinker",
          "Wizard",
          "Paladin"
        ],
        "status": "canon",
        "source": "Player Rulebook — Spell Lists"
      },
      "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
      "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
      "coreEntries": [
        {
          "index": 48,
          "original": {
            "school": "Abjuration",
            "level": 4,
            "name": "Banishment",
            "effect": "Send a creature to another plane temporarily.",
            "source_paragraph": 9039,
            "casting_time": "1 action",
            "range": "60 feet",
            "duration": "Instantaneous",
            "components": "V, S, F",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Planar"
            ],
            "rp_cost": 7
          }
        }
      ],
      "possibleHistoricalAliases": []
    },
    "reviewFlags": [
      "Core resolution requires an explicit operational interpretation",
      "Not selectable in this spell playtest packet until individual operational review"
    ]
  },
  "recordSha256": "6f033826209686de6d256a1f6473230563f356e879b6fb083641140b3e4515b5",
  "individualQuestion": "POST-PUSH RECEIPT ONLY. Preserve the source promise of temporary transport to another plane, Core Action/60ft/Instantaneous and all access records without inventing a destination, planar relation, return procedure or new cosmic origin. Carry this unchanged source to the owner-directed careful cosmology review after the successful authorized GitHub push and verified remote commit. Exclude it from present mechanical authoring and approval."
}
```

## NEW Faction Envoy profile

This is a provisional summon-only design. It does not certify CR 3 balance or replace either original public CR-3 creature. Their complete source records remain in the structured comparison evidence.

```json
{
  "id": "proposal.faction-envoy-cr3",
  "status": "NEW summon-only profile for the source’s nominal CR 3 role; no human CR/balance certification.",
  "size": "Medium",
  "type": "Humanoid for mechanical targeting only; no new ancestry or setting origin.",
  "nominalChallengeRating": 3,
  "armorClass": 15,
  "hitPoints": 50,
  "bodyMassPounds": 170,
  "walkingSpeedFeet": 30,
  "abilities": {
    "STR": 16,
    "DEX": 14,
    "CON": 14,
    "INT": 10,
    "WIS": 12,
    "CHA": 10
  },
  "savingThrows": {
    "STR": 3,
    "DEX": 2,
    "CON": 2,
    "INT": 0,
    "WIS": 1,
    "CHA": 0
  },
  "checks": "Use the actual ability modifier without additional proficiency. Ordinary sight/hearing; understands the caster’s spoken commands through this spell only, without other languages, telepathy or faction intelligence. No resistances, immunities, spells, slots, class features or special senses.",
  "attack": "One commanded offensive Action makes two melee weapon attacks, +5 to hit, reach 5 feet, each dealing 1d8+3 slashing. Each target must be legal when attacked. Movement between attacks uses the same actual 30-foot movement budget. A critical doubles only the die. No ranged attack or ammunition is supplied. The temporary one-handed blade is nontransferable: separation makes it vanish without supplying another wielder, material or value.",
  "actions": "A Bonus Action command from the owner, within 60 feet and perceived through actual senses, permits movement and the two-attack offensive Action OR one ordinary Dodge, Dash, Disengage or Search. No item activation, casting, Help, grapple, shove, healing or independent opportunity attack. Without a command it may move defensively and Dodge. It shares the owner’s command/offense allowance; extra turns create no additional offense.",
  "lifecycle": "One entity and HP pool, without refresh from transformation, commands, transfer or suppression. Ends at 0 HP, concentration/source ending or the original minute deadline. It can carry genuinely entrusted existing gear under ordinary capacity using STR 16; this creates no cargo and ending drops real items legally. No conjured stock, corpse, reward, harvest, permanent recruitment or faction standing."
}
```

## Required joint decisions

Discuss all fifteen original mechanical questions with GPT using these exact proposals, source conflicts and current dependencies. Confirm separate spell-rank placements, reflection ownership and range, endpoint-based transport prevention, Corrupted eligibility and contact cadence, the additional RP-price interface, faction membership, alignment records versus conduct restrictions, finite companion healing, one wall HP pool, the proposed 5-RP drain, two-round paralysis under the reviewed application guard, atomic 500-foot travel and beacon payment/custody. Sleep and Hypnotic Pattern are supplied in full as current control comparisons. Banishment and the other named post-push receipts remain outside this mechanical authoring. Indexing does not adopt a draft.
