# Unholy Ascendance — accepted static authored procedure 275

GPT explicitly accepted Unholy Ascendance / CC194-B04 after Return275 corrected the two current-source hash fields and preserved all reviewed procedure and replay state content. This application updates one authored-review index entry; the native catalog, runtime selection and downstream gates remain unchanged.

## Preserved native card

{
  "id": "unholy-ascendance",
  "name": "Unholy Ascendance",
  "schools": [
    "Necromancy"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Necromancy",
      "baseRpCost": 26
    },
    "Druid": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Necromancy",
      "baseRpCost": 26
    },
    "Wizard": {
      "rank": 9,
      "minimumClassLevel": 17,
      "school": "Necromancy",
      "baseRpCost": 26
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "unholy-ascendance",
    "original": {
      "name": "Unholy Ascendance",
      "level": 9,
      "resonanceRank": 9,
      "school": "Necromancy",
      "schools": [
        "Necromancy"
      ],
      "placements": [
        {
          "name": "Unholy Ascendance",
          "school": "Necromancy",
          "level": 9,
          "summary": "Become a demi-lich for 1 minute: resistance to all, flight, necrotic spells free."
        }
      ],
      "classLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Wizard": 9
      },
      "classRanks": {
        "Cleric": 9,
        "Druid": 9,
        "Wizard": 9
      },
      "classLearnLevels": {
        "Cleric": 17,
        "Druid": 17,
        "Wizard": 17
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
      "description": "Become a demi-lich for 1 minute: resistance to all, flight, necrotic spells free.",
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
        "index": 715,
        "original": {
          "school": "Necromancy",
          "level": 9,
          "name": "Unholy Ascendance",
          "effect": "Become a demi-lich for 1 minute: resistance to all, flight, necrotic spells free.",
          "source_paragraph": 9866,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Movement",
            "Ward"
          ],
          "rp_cost": 26
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

## Accepted procedure and spell-local choices

KEEP Action26RP,V/S/F,one minute,resistance to all,flight and free necrotic spells. NEW Self nonconcentration; actual demi-lich form is a spell-local SAME-IDENTITY body overlay, not a separate monster or the Mage Lich class. NEW complete profile: same Medium5×5foot space, height and mass as the recorded underlying humanoid, skeletal Undead body, two articulated usable hands, ordinary speech and senses, original ability scores/AC/attacks/HPmaximum/currentHP/Wounds/temporaryHP/death tracks. It supplies no monster attack, extra Action, phylactery, soul vessel, touch-death, immortality, revival, spell knowledge, class feature, new inventory or cosmological identity. These anatomy/type choices are newly authored and not recovered source facts. An incompatible or absent underlying geometry/gear record is held, not filled by an imported bestiary.
Existing wearable equipment remains externally worn/held with exact ownership/identity, actual fit and accessible components; no duplication, free equip/stow or meld is granted. Other actual forms are not stacked: NEW suspend the prior body overlay's physical expression while its own original clock/state continue, retaining its source identity; on end restore whichever real prior body remains legally operative, otherwise the recorded base body. No HP reset or healing, separate formHP pool or Wound clearing occurs. Form's Undead type affects actual type predicates while operative; ordinary living-only healing does not become valid. Death/removal ends this overlay with the actual death/body state retained, not a new corpse/extra soul. Hunt, soul/return and other unavailable cosmology remain held.
Resistance to all means all actual damage types, including mixed components, each halved with the accepted floor/order and no double resistance with an existing ward. It is not immunity to conditions, direct HP prices, non-damage death, control, material consumption, support loss or typed targeting. Apply real temporaryHP then normalHP/Wounds/death/concentration after damage. Do not turn price payment into damage to gain prevention or resources.
NEW flight30feet with hover, using the actual shared movement budget and current movement restrictions; no extra30feet after land movement. Hover avoids support-loss falling from Speed0/Prone while this flight actually operates. Losing the overlay's flight through actual suppression/removal/expiry while unsupported immediately starts the accepted fixed-marker Falling bridge. Track total/uncontrolled descent, source-relative enclosing regular slot, future marker, support/impact, real raw dice and defenses at impact. No immediate invented damage or hanging in midair. Reappearance before impact may end Falling only if actual operative flight now supports the same body; original spell deadline never resets.
NEW UA194-FREE predicate: a selected spell's own declared direct damage profile contains necrotic damage at quote/commit. A mixed fire+necrotic Soul Pyre qualifies as one spell; pure poison Ray of Sickness and non-damaging Necromancy Soulburn do not. A later save, resistance, miss or zero damage does not retroactively change price. An actually authorized precommit type change is considered; no unowned Elementalist ability is granted, and a companion's later damage or weapon buff is not the spell's direct damage profile. Pending undefined payloads remain content holds.
Free waives that qualifying spell's entire discountable castingRP base/extras/surcharge before final Influence, but preserves protected actual-output principal, HP sacrifices, real consumed materials/finite uses, source access/components/actions/strain and ongoing upkeep. It does not waive an actual corpse TARGET or supply one; Soul Pyre atomically consumes the same genuine principal remains only on its legal successful effect, leaving real gear and consumed lineage. These explicit distinctions are NEW local authorship, not a global definition of free. Non-damaging Unholy itself is not self-free. Under operative Perfection, Perfection's A replacement follows this0 before final Influence; both original clocks remain. Countering gives no effect, no resource refund and no new body. Saved body/gear/price/flight/fall/death states must remain reversible and source-bound.
NEW proposed suppression expression: while the attached form is actually suppressed, express its recorded underlying body and gear, remove only this source's flight/resistance/free-price benefit, and retain the suspended form/source and original deadline. Resumption before that deadline restores its same overlay without HP/gear/movement refresh. This positive above-zero bridge is demonstrated. The new Undead form's zero-HP/Null-recipient lifecycle remains unresolved under CC194-B04, so the identity is not accepted; no standard-undead-minion rule is silently applied to this caster.

NEW spell-local UA270-LIFE (explicitly authorized by GPT in Return270; proposal only, not source-recovered): preserve one original character/body identity and all HP/maxHP/Wounds/injuries/death counters/resources/equipment. Operative targeting type is Undead, so living-only targets fail. Ordinary damage follows that character's Core/Healing damage, Wound and death-save procedures through this adapter. No automatic destruction, immunity, separate HP or special zero-HP action. For this recipient only, a qualifying same-dealer Null root suppresses damage-caused Instant Death, Wound/Maiming saves and damage-caused death failures. New positive-to-zero becomes Stable0 with cleared counters and one stipulated d4-hour recovery deadline; already-Dying0/Stable0 preserves current counters/schedule/deadline. Zero HP causes ordinary unconsciousness; it does not end the nonconcentration UA overlay. Actual death ends UA; original expiry and independent removal remain. Suppression returns the legally expressed underlying type/body while all original clocks continue. Each later event snapshots then-current state; reversion never resurrects. Scope is Unholy Ascendance only.

NEW spell-local UA270-HEAL (explicitly authorized by GPT in Return270; proposal only): while UA is operative, the continuing caster may receive its own already-accepted Vampiric Touch self-heal. Preserve Action/Touch/V/S/F, one attack, actual damage and floor(actualDamageDealt/2). The UA waiver changes only eligible casting payment; suppressed/reverted casts use ordinary quote. No new spell, unconscious casting or generic Undead healing. Preserve all existing CC194-H qualifications and downstream gates.

All clauses marked NEW and all local completions above are proposed spell-local authorship, not global authority.

## Accepted witnesses

- RANK9CASTINGCOST5-275-UA-ACTUAL-DEATH: 3 events; archive member `cases/RANK9CASTINGCOST5-275-UA-ACTUAL-DEATH.json`.
- RANK9CASTINGCOST5-275-UA-AMF-RESUMPTION: 2 events; archive member `cases/RANK9CASTINGCOST5-275-UA-AMF-RESUMPTION.json`.
- RANK9CASTINGCOST5-275-UA-EARLY-ARCH-DISPEL: 8 events; archive member `cases/RANK9CASTINGCOST5-275-UA-EARLY-ARCH-DISPEL.json`.
- RANK9CASTINGCOST5-275-UA-FORM-LIFECYCLE: 13 events; archive member `cases/RANK9CASTINGCOST5-275-UA-FORM-LIFECYCLE.json`.
- RANK9CASTINGCOST5-275-UA-HEAL-OPERATIVE: 2 events; archive member `cases/RANK9CASTINGCOST5-275-UA-HEAL-OPERATIVE.json`.
- RANK9CASTINGCOST5-275-UA-HEAL-SUPPRESSED: 8 events; archive member `cases/RANK9CASTINGCOST5-275-UA-HEAL-SUPPRESSED.json`.
- RANK9CASTINGCOST5-275-UA-NULL-NEWZERO: 7 events; archive member `cases/RANK9CASTINGCOST5-275-UA-NULL-NEWZERO.json`.
- RANK9CASTINGCOST5-275-UA-NULL-WOULD-DIE: 1 events; archive member `cases/RANK9CASTINGCOST5-275-UA-NULL-WOULD-DIE.json`.
- RANK9CASTINGCOST5-275-UA-ORDINARY-NEWZERO: 4 events; archive member `cases/RANK9CASTINGCOST5-275-UA-ORDINARY-NEWZERO.json`.
- RANK9CASTINGCOST5-275-UA-ORDINARY-WOULD-DIE: 1 events; archive member `cases/RANK9CASTINGCOST5-275-UA-ORDINARY-WOULD-DIE.json`.
- RANK9CASTINGCOST5-275-UA-PRIOR-EXPIRY: 2 events; archive member `cases/RANK9CASTINGCOST5-275-UA-PRIOR-EXPIRY.json`.

## Retained qualifications

- Acceptance is limited to the exact static authored Unholy Ascendance procedure, its 11 reviewed cases and the bound UA270-LIFE/UA270-HEAL contracts.
- The demi-lich body overlay, acquired spell identity and actor clocks remain limited to the written procedure and witnessed traces; no generic monster abilities or new inventory are granted.
- The null, healing, death, suppression/resumption, form lifecycle, recharge, action-budget and ordinary casting branches retain the reviewed source and timing boundaries.
- All other qualifications and CC194-H01–H08, unrelated holds, runtime, implementation, playtest, balance, cosmology, domain-closure, completion and release gates remain intact.
