# AC5 Rank-5 Abjuration/Conjuration — Repair 04 Player Chapter

## Local05 corrections awaiting exact GPT acceptance

The preceding returned Repair04 material is preserved in the audit archive. The current files correct three precisely identified issues below. Prior GPT disposition text is retained as historical evidence and does not constitute acceptance of these local edits. The original sixteen procedures, seventeen placements and source/access objects remain exact; only the shared portal cost wording is clarified against the accepted additive movement rule. Full current case data and previous versions remain in CASEBOOK.json.

**AC5-L05-01** Repair04 X25 erroneously places A and W1 inside its added F2, then calls A outside all Antimagic. It also says a radius10 field centered15 covers point0 despite distance15. Use independent single-field incoming/self-dispel fixture and a separate mutually covering pair with8ft anchor separation. All coordinates, costs, clocks and termination outcomes are explicit in revised X25.

**AC5-L05-02** Repair04 X12 calls an actual sphere an exactly rectangular six-panel suppressed region. No actual sphere geometry is provided. Use radius10 center(-1,0,5), retain actual sphere/panel intersections, and distinguish the six occupied pending full panels from the additional clear suppressed portions that resume.

**AC5-L05-03** Portal shared rule says movement multipliers even though COMBAT_ACTION_PLAYTEST specifies terrain rate plus crawl/squeeze additions. Write exact additive formula and show difficult+squeeze15ft/crawl+difficult+squeeze20ft for a5ft crossing in X27.

## Status and authority
All sixteen source identities/access records remain frozen evidence. The procedures below are the complete current **NEW provisional authored-playtest replacement candidate** after AC5-R04-01..04. None is adopted by this file. Accepted AC4 Dampening, Dimensional Anchor, ordinary Banishment, body/life rules and other frozen interfaces are not rewritten.

## Repair04 dispositions
- **AC5-R04-01 — AGREE (correction plus NEW narrow operation-snapshot clarification):** The prior X25 Burning Hands geometry was illegal. Repair04 uses a real 15-foot west-facing cone from caster (20,0), A centered (15,0) wholly outside the 10-foot field, and B centered (7.5,0) with a Medium 5x5 footprint intersecting the field. AC5-ANTIMAGIC-IO-04 also makes Greater Dispel's self-dispel exception operation-specific: snapshot suppression for every captured termination operation before any removal; a captured Antimagic application ignores only suppression from itself, not from another field, and operations suppressed in that snapshot do not spring back after an earlier field ends.
- **AC5-R04-02 — AGREE (correction plus NEW exact fixed-panel pending semantics):** The prior X12 body could not legally occupy a 6-foot-tall opening when only z0..5 was suppressed. Repair04 suppresses six complete 2.5x2.5 panels spanning y[-2.5,+2.5],z[0,7.5]. On suppression removal, a previously suppressed portion of a fixed panel that intersects an occupant remains absent as that same stored portion until clear; wall portions that were never suppressed remain solid.
- **AC5-R04-03 — AGREE (correction):** The prior X03 omitted the target's death-save classification, regular START order, Stable recovery roll/deadline and the second/third Magma ticks. Repair04 uses a designated significant NPC with death saves, target regular starts t6/t12/t18/t24, Stable recovery d4=2 hours at t6, cancellation of that deadline by later ordinary damage, explicit death-save rolls at t18/t24, all three Living Magma opportunities, and actual death on the third ordinary failure.
- **AC5-R04-04 — AGREE (correction plus NEW portal-local geometry clarification):** Accepted AC4 Dimensional Anchor allows a portal to remain present and blocks actual transport transactions. Repair04 therefore removes Anchor from Alignment Portal formation preflight and applies it at each crossing. Portal geometry now records real body height/pose and full destination footprint; the forced-crossing proof uses a fitting Medium body and an actual successful 5-foot Shove rather than inventing permission to force an oversized body through a squeeze. New AC5-X31 proves a live portal under Anchor, blocked known crossing, Anchor ending, later legal crossing, and eventual portal closure.

## Shared current rules

### AC5-PRICE-01
```json
{
  "classification": "NEW scoped AC5 price ordering; preserves accepted AC4 Dampening and existing final Influence",
  "rule": [
    "Validate that the activation is an actual spell cast and determine the actual casting body at commitment.",
    "Create pricing buckets. creditableBase starts as the actual ordinary base RP amount after exact base-only reductions/waivers/minima. preNexusExtras contains printed ordinary RP extras and Dissonance/strain surcharges that remain discountable but are never Barrier-pool credit. Protected principal such as Resonance Barrier X, materials, HP, ammunition, charges and uses stay outside these buckets.",
    "If at least one operative Resonance Nexus contains the caster at commitment, apply one total -2 to the combined discountable pre-Dampening buckets, minimum0: reduce creditableBase first, then preNexusExtras. Overlapping Nexuses never stack.",
    "If accepted Resonance Dampening Field applies, add its mandatory +2 RP only after Nexus/ordinary reductions. Dampening is noncreditable and Nexus never subtracts it. A genuine charge/use-only spell with no ordinary RP-price interface still receives this accepted +2 interface; Nexus has no earlier RP bucket to reduce.",
    "Apply one pending final Resonance Influence Ease/Burden to the resulting RP-priced spell amount, minimum0. For Barrier accounting only, Ease reduces creditableBase first, then remaining preNexusExtras, then Dampening/other noncreditable final components; Burden adds only noncreditable cost.",
    "Commit the final affordable RP amount together with Action/components/concentration transition. Countering, suppression, save/failure or replacement gives no refund."
  ],
  "barrierCreditAllocation": "Resonance Barrier pool credit = 5 × (final creditableBasePaid + protectedX). No Dissonance, printed surcharge, Dampening, Burden or other nonbase extra becomes pool credit even if paid. Base-only waivers can reduce creditableBase to0; Nexus/Ease allocations above may also reduce it. Protected X is fully paid separately and fully creditable.",
  "chargeOnlyBoundary": "An ancestry/use-only spell spends its actual use and has no ordinary RP bucket unless another exact interface creates one. Nexus therefore cannot manufacture or discount a price. Accepted AC4 Dampening alone can add its +2 RP interface; final Influence may then modify that +2. A positive RP amount requires an existing lawful personal RP pool. Paying RP for a nonspell still does not make it a spell."
}
```

### AC5-SUMMON-TARGET-01
```json
{
  "classification": "NEW extension limited to Greater Fire Pet and Faction Champion; does not alter AC4 Water Pet/Envoy scope",
  "rule": "While either AC5 finite summoned body actually exists, treat it mechanically as an active creature and as a living ally for ordinary HP-healing/living-creature targeting, including Cleric Healing Rite. This does not establish natural biology, native plane, soul, corpse, breeding, nourishment, faction personhood or loot. A Null Disabled 0 body remains the same target while its original source persists and can be legally healed above 0. If the source has already ended/expired/replaced/dismissed the body, there is no target to heal.",
  "nullLifecycle": "Bind both profiles to the accepted finiteSummonFamiliarMirrorBeast Null recipient branch: qualifying Null damage to 0 replaces only damage-caused disappearance with Disabled 0 while original source duration persists; later qualifying Null hits do not create organic death/Wounds; independent expiry/dismissal/concentration/replacement still ends the body. Ordinary non-Null damage reaching 0 uses the body's normal finite-summon disappearance."
}
```

### AC5-ROOT-01
```json
{
  "classification": "NEW AC5 damage-root checkpoints consistent with accepted Null root ownership",
  "livingMagma": "On a failed initial CON save that successfully establishes the recurring Living Magma rider, create one damage root immediately even though no initial damage packet occurs. Dealer is the caster. Record the caster's then-current unsuppressed Null Veil flag on that root. The three later tick packets are descendants and inherit the creation-time flag; later Veil changes do not rewrite it. A suppressed scheduled tick creates no child packet and is consumed with no makeup.",
  "greaterFirePetAttack": "Each commanded Fire Pet attack that reaches its actual damage checkpoint creates a distinct root with dealer = Fire Pet body, not owner/controller.",
  "greaterFirePetAura": "Each qualifying recipient's aura START checkpoint creates its own damage root with dealer = Fire Pet body. One shared d6 roll may feed several recipients but does not merge root identity or copy another actor's Veil. Evaluate the pet body's own Veil at each recipient root creation.",
  "massiveBlast": "At instantaneous damage resolution create one root per original recipient, all with dealer = caster and the same cast ID. A shared 5d8 roll does not merge recipient roots.",
  "barrier": "Damage prevention creates no damage root."
}
```

### AC5-BANISH-EXT-01
```json
{
  "classification": "NEW scope extension only for Banish Elemental and Elemental Banishment; ordinary Banishment remains unchanged",
  "reuse": [
    "BAN-CELL-03 finite generated spell-cell topology/environment",
    "BAN-ADMIT-03 current-space preflight, internal creation and legal visitor admission",
    "ordinary Banishment custody/separate-creature and mandatory-body-ending rules",
    "ordinary Banishment agency/real-clock rules",
    "BAN-TRANSPORT-CLASS-02 planar/extradimensional nonteleport classification, copied only for these two AC5 exile applications",
    "BAN-CLOSE-03 terminal origin-plane closure",
    "BAN-PLACEMENT-HANDOFF-03 and BAN-CONFLICT-04 placement/conflict handling",
    "ordinary Banishment terminal endpoint-blocker exception"
  ],
  "notReused": [
    "ordinary Banishment target eligibility",
    "ordinary Banishment spell identity/rank/access",
    "ordinary Banishment concentration when the AC5 spell authors another duration"
  ],
  "suppression": "Actual suppression of the exile application closes/ends that application through reused closure; it never pauses and resumes exile.",
  "bodySourceEnding": "If the primary finite creature source ends first, that body ends under its source, then the AC5 exile immediately closes. BAN-CLOSE-03 settles every remaining extant independently legal secondary body/corpse/object once; ended/absent bodies remain absent. Never settle only cargo when another extant identity exists, and never recreate the ended primary.",
  "intent": "Before the printed CHA save record ACCEPT or RESIST exactly as ordinary Banishment. ACCEPT remains voluntary even if the target rolls and fails; RESIST+failed save is forced. For these two AC5 exiles, No Escape blocks ACCEPT because it names voluntary extradimensional travel; Verdict Absolute and Reign of Ashes do not block because these applications are not teleportation. This is spell-local classification only."
}
```

### AC5-PLANAR-META-01
```json
{
  "classification": "NEW spell/campaign metadata for Planar Protection, Planar Binding and Alignment Portal only; not a master cosmology",
  "planeKey": "An opaque stable ID for an actual plane record already established by campaign/source authority. The key carries no automatic alignment, deity, native-species, soul-destination, Wheel, dominion or tributary meaning.",
  "siteId": "A stable known physical destination site on one planeKey with actual location/footprint/support data.",
  "travelProvenance": "On a successful cross-plane body transition using a reviewed source, the Director may record currentBody.lastArrivedFromPlaneKey = the actual origin planeKey and the transport event ID. A creation source may instead explicitly provide createdFromPlaneKey. These are operational travel/source provenance only and do not establish native origin or soul identity.",
  "unknown": "If a required planeKey/provenance fact is not established, it remains Indeterminate. Spells do not secretly discover or fabricate it.",
  "prospectiveArrival": "For a particular cross-plane transition, snapshot prospectiveOriginPlaneKey = the actual planeKey containing the body immediately before that transit. Destination-side Planar Protection and other arrival predicates evaluate this immutable prospective value before placement. Only a successful atomic transition commits currentBody.lastArrivedFromPlaneKey = prospectiveOriginPlaneKey and the event ID. Failed/countered/blocked transit leaves prior provenance unchanged. createdFromPlaneKey remains creation provenance and is used for ordinary physical ward entry only when no current cross-plane transition supplies a prospective origin.",
  "partialFootprint": "A destination/entry is ward-eligible if any part of the body/group terminal footprint would enter the protected sphere. All bodies in one carried/group transit are checked independently before atomic placement."
}
```

### AC5-CHAMPION-ALLY-01
```json
{
  "classification": "NEW Faction Champion source-specific 'allied faction' gate",
  "rule": "Before payment choose one canonical factionId. Formation requires: (1) an actual spell-specific alliedStatus=true record for this caster/faction; (2) current standing > 0; (3) actual invocation permission under the current faction system; and (4) no explicit aid prohibition. Membership remains a separate credential and is not inferred from alliedStatus or standing. Faction Ally's membership+permission gate and Faction Portal's positive-standing+known-HQ gate remain distinct and are not imported."
}
```

### AC5-ALIGN-PORTAL-META-01
```json
{
  "classification": "NEW Alignment Portal-specific compatibility metadata, not objective plane taxonomy",
  "rule": "An actual plane record may carry alignmentPortalCompatibility = a set of canonical nine-point alignment keys and one or more known Alignment-Portal siteIds. This is travel compatibility for this spell only. It does not assert that the plane is objectively 'Lawful Good', that a mortal Wheel label equals it, that inhabitants are native there, or that souls/deities map to it."
}
```

### AC5-ANTIMAGIC-SUMMON-01
```json
{
  "classification": "NEW suppression profile limited to Greater Fire Pet and Faction Champion",
  "rule": "While any part of one of these bodies intersects operative Lesser Antimagic, keep the same body identity, HP, source deadline, Null Disabled state and genuine cargo. Speed becomes 0 and the body cannot take Actions, companion commands, attacks or Fire-Pet aura checkpoints. Intrinsic manifested gear grants no separate function while suppressed. Genuine carried items remain the same items; if actual physical custody becomes impossible under ordinary item rules, place/drop them normally. Leaving suppression restores only still-live source permissions with the same HP/deadline and no refill/resummon."
}
```

### AC5-PLANAR-ARRIVAL-03
```json
{
  "classification": "NEW AC5 prospective-arrival provenance timing; operational metadata only",
  "rule": "For every cross-plane transit into a Planar Protection destination, snapshot prospectiveOriginPlaneKey from the body’s actual plane immediately before the transit. Evaluate the destination ward against that value before placement, regardless of stale lastArrivedFromPlaneKey. On success commit lastArrivedFromPlaneKey=prospective origin; on failure keep the prior record unchanged. No failure reveals hidden provenance/cosmology beyond ordinary observed failure."
}
```

### AC5-PLANAR-FALL-03
```json
{
  "classification": "NEW Planar Protection unsupported-fall boundary",
  "rule": "Planar Protection supplies no support. If an eligible creature’s continuous ordinary Falling would cross inward and the last exterior boundary point is unsupported, the ward does not arrest or suspend that Fall Marker; the continuous fall may carry the body inside. Once inside, it is treated as already inside for this ward and may leave but cannot reenter after leaving while still eligible. Grounded/otherwise supported forced or voluntary crossings remain blocked at the last legal exterior position."
}
```

### AC5-BINDING-ORDER-03
```json
{
  "classification": "NEW Planar Binding pending-order lifecycle only",
  "rule": [
    "Each live binder→target record holds at most one pending service order. Issuance requires the binder and target on the same plane, a valid one-way command-intent channel, the binder’s real Bonus Action in initiative or one order opportunity per6 elapsed seconds outside initiative, and a currently source-legal simple order. Invalid issuance spends no order record; normal action-cost commitment follows the actual declaration rules.",
    "A valid order receives its issue timestamp and binds the target’s next regular behavior opportunity after issue: next regular target turn/opportunity in initiative, or next six-second behavior pulse outside initiative. It expires at the end of that one opportunity whether executed, impossible, suppressed or budget-starved. No order is banked/replayed.",
    "A later valid Binding order from the same binder before execution replaces that binder’s older pending Binding order; it does not erase other control effects. Plane change after a valid order does not erase the already-heard instruction, but plane separation prevents new issuance. Lesser Antimagic suppressing the Binding compulsion at the execution opportunity makes that order ineffective for the opportunity and it expires; the 24-hour service clock continues.",
    "Companion/source gates remain prerequisites. Binding never creates the owner’s Companion Command, Action, Bonus Action, Reaction or offense token. If an owner legally opens one commanded companion damaging action and a pending Binding Attack order is compatible with that action but conflicts only on target choice, use Compelled Budget Arbitration/priority to constrain the one available action. If no source-gated action becomes available during the bound opportunity, the order expires without inventing one."
  ]
}
```

### AC5-BARRIER-RECAST-03
```json
{
  "classification": "NEW Resonance Barrier same-name application/concentration lifecycle clarification",
  "rule": [
    "Ordinary concentration transition occurs at the new cast’s legal commitment before Counterspell or fresh Barrier formation. Therefore a same-caster old Barrier that depended on that caster’s concentration ends at commitment and cannot survive a countered, failed, zero-pool or weaker replacement cast unless a future exact source expressly grants that exception.",
    "If a still-live Barrier from a different caster protects the target, compare the fresh offered pool only at successful resolution. Stronger fresh pool replaces the retained application and ends the old Barrier application/concentration. Equal or weaker fresh offer does not replace/refresh the retained pool; the fresh Barrier application ends immediately at resolution and its new caster’s concentration on that application ends, with no refund.",
    "Pool comparisons use remaining retained pool versus fresh offered initial pool. No two pools add."
  ]
}
```

### AC5-ANTIMAGIC-IO-04
```json
{
  "classification": "NEW Repair04 refinement of Lesser Antimagic input/output and dispel-operation capture; supersedes AC5-ANTIMAGIC-IO-03 where inconsistent",
  "rule": [
    "At legal spell/effect commitment, actual costs/components/concentration/cadence resolve before suppression. Ongoing local expressions remain suppressed only where their real body/anchor/area intersects the operative field.",
    "For an instantaneous spell or magical nonspell originating outside, inspect its actual recipient, affected area and/or destination manifestation checkpoint. A local payload that would manifest in the field is suppressed at resolution. Damage/healing there creates no packet/root/rider; an indivisible relocation whose destination footprint intersects fails atomically at origin. Outside-to-outside nonpath travel is unaffected by an imaginary line through the sphere.",
    "For Greater Dispel or another exact multi-effect dispel, first capture the immutable effect set under that source, then snapshot whether each individual captured termination operation is locally suppressed before performing any removal. A termination operation targeting one Lesser Antimagic application ignores suppression from that same target field only. Another independently active Antimagic field may still suppress that termination operation if its operative volume covers the relevant application/operation locus.",
    "Do not re-evaluate a captured termination operation after earlier removals in the same dispel. Thus an inside captured buff whose termination operation was suppressed at the operation snapshot remains live even if the Antimagic field suppressing that operation is ended by another captured operation. There is no second scan or spring-back termination.",
    "This self-dispel exception is operation-local. It neither makes unrelated payloads immune to Antimagic nor lets a dispeller ignore a different suppressing field.",
    "No fictional projectile/path is invented for nonprojectile effects. Genuine projectiles/paths retain their source semantics.",
    "Wizard Spell Preservation remains an intrinsic class protection of the primary spellbook: field suppression can make magical use/access unavailable locally but cannot create a non-artifact ordinary destruction loophole."
  ]
}
```

### AC5-WALL-PANELS-04
```json
{
  "classification": "NEW Repair04 Wall of Force suppression/resumption geometry; supersedes AC5-WALL-PANELS-03 where inconsistent",
  "rule": [
    "Tessellate the authored wall from its fixed lower-left/local anchor into 2.5-foot by 2.5-foot logical panels; exact edge remainders keep their smaller size.",
    "While Antimagic or another exact suppressor overlaps the wall, suppress only the exact intersecting portion of each fixed panel and record that suppressed portion geometry. A portion of a panel that was not suppressed remains solid and cannot be entered merely because another portion is absent.",
    "When suppression ends, process each recorded suppressed portion at its original fixed coordinates. If any part of that recorded portion's 1-inch wall volume intersects a creature or independent object, hold that entire recorded suppressed portion absent until clear. Do not generate a new body-shaped cutout and do not deactivate neighboring wall portions that remained solid.",
    "Once the recorded portion is clear, that exact portion resumes. No push, cut, crush, tactical hole selection, free squeeze or movement is created."
  ]
}
```

### AC5-PORTAL-GEOMETRY-04
```json
{
  "classification": "NEW Repair04 refinement of Alignment Portal physical aperture/crossing; supersedes AC5-PORTAL-GEOMETRY-03 where inconsistent",
  "rule": [
    "Alignment Portal creates two fixed linked vertical apertures, each 5 feet wide by 8 feet high. At cast time record each aperture base-center, floor elevation and outward normal. Origin pose must be perceived, clear and supported within 60 feet/LoE. Destination site metadata must already supply a known portalPose with clear supported staging space sufficient for the intended known portal opening; portal creation itself transports no body or object.",
    "A current Dimensional Anchor does not prevent the linked apertures from forming. Anchor is checked on each actual planar-transition transaction whose transported origin or destination footprint intersects the field; a known blocked crossing commits no movement, while a blocker appearing after legal crossing commitment yields atomic failure at origin under accepted Anchor.",
    "The gateway is bidirectional while active. Voluntary crossing is planar/extradimensional physical-gateway travel and is NOT teleportation. No Escape blocks voluntary crossing; Verdict Absolute and Reign of Ashes do not. This classification is Alignment-Portal-only.",
    "Entering an aperture requires 5 feet of actual path through the gateway and ordinarily costs 5 feet of base movement. Use the accepted additive per-foot cost: terrain rate1 normal,2 difficult or3 severe (strongest terrain only), then add1 for crawling and1 for squeezing. A5ft traversal therefore costs5 times that sum; difficult+squeeze costs15ft, not20ft. A body must fit both the 5-foot width and 8-foot height under current posture/clearance rules. A Large 10x10 body may use ordinary one-size-smaller squeeze only when its stated height/pose and the actual aperture permit it; squeezing adds +1 movement cost per foot and keeps its real penalties.",
    "Forced movement may cross only when the forcing source itself supplies a legal path and enough actual forced distance through the aperture. Do not infer that a Shove can force a body through a squeeze it could not otherwise physically clear. A fitting Medium body successfully Shoved 5 feet directly through the aperture is a sufficient forced-crossing fixture; forced movement is not voluntary, so No Escape's voluntary wording does not block that transit. All arrival gates still apply.",
    "Crossing maps facing relative to entry normal to destination exit normal. Destination placement must fit the whole body in the actual supported staging space; fixed neutral board order breaks equivalent placements. No search through barriers and no body bisection."
  ]
}
```

## Complete AC5 authored profiles
```json
{
  "AC5-PROFILE-GREATER-FIRE-PET-01": {
    "id": "AC5-PROFILE-GREATER-FIRE-PET-01",
    "classification": "NEW finite summoned profile; mechanical type Elemental only for targeting; no native-plane/soul inference",
    "size": "Medium",
    "creatureType": "Elemental",
    "weightLb": 100,
    "hpMax": 60,
    "ac": 17,
    "speedFt": 30,
    "abilities": {
      "STR": 14,
      "DEX": 14,
      "CON": 16,
      "INT": 4,
      "WIS": 10,
      "CHA": 6
    },
    "saves": "Each saving throw uses original owner's current PB as the total modifier; no ability modifier is added unless another exact source says so.",
    "checks": "Raw current ability modifier only; no proficiency.",
    "senses": "Ordinary sight/hearing; no inherent darkvision or special sense.",
    "defenses": "No inherent resistance/immunity from this profile.",
    "command": "Shared Companion Command: owner Bonus Action while conscious, perceiving the body within 60 ft and line of effect; attached phase immediately after owner's whole turn. One global command and one offensive companion Action per owner/numbered round across eligible companions. Without command: defensive Move/Dodge only.",
    "attack": {
      "name": "Fire Strike",
      "activation": "commanded Action",
      "reachFt": 5,
      "targets": 1,
      "attackModifier": "original owner's current spell attack modifier",
      "damage": "2d10 fire",
      "critical": "double attack dice only"
    },
    "aura": {
      "radiusFt": 5,
      "lineOfEffect": true,
      "trigger": "qualifying hostile perceived recipient future regular START",
      "save": "DEX vs original owner's current spell DC",
      "damage": "1d6 fire fail; half floor success",
      "frequency": "max one attempt per owner/target/Greater-Fire-Pet family/numbered round; outside initiative one per 6 sec",
      "roll": "one shared d6 per owner aura cycle, separate recipient saves/roots",
      "entry": "no entry tick",
      "offenseBudget": "passive source exception; does not consume or grant offensive companion Action"
    },
    "ending": "One Greater Fire Pet per owner. Successful replacement, concentration/source end, expiry/dismissal or ordinary non-Null damage reaching 0 ends body. Intrinsic manifestation leaves no corpse/loot/fuel. Genuine independently supplied objects remain real and drop/settle normally.",
    "nullHealing": "AC5-SUMMON-TARGET-01 + accepted finite-summon Null branch",
    "suppression": "AC5-ANTIMAGIC-SUMMON-01"
  },
  "AC5-PROFILE-FACTION-CHAMPION-01": {
    "id": "AC5-PROFILE-FACTION-CHAMPION-01",
    "classification": "NEW finite summoned representative; mechanical type Humanoid for targeting only; no real NPC transport, membership, native origin or soul inference",
    "size": "Medium",
    "creatureType": "Humanoid",
    "weightLb": 180,
    "hpMax": 70,
    "ac": 18,
    "speedFt": 30,
    "abilities": {
      "STR": 18,
      "DEX": 12,
      "CON": 16,
      "INT": 10,
      "WIS": 12,
      "CHA": 12
    },
    "saves": "Each saving throw uses original owner's current PB as total modifier.",
    "checks": "Raw ability modifier only; no proficiency.",
    "senses": "Ordinary sight/hearing only.",
    "defenses": "No inherent resistance/immunity.",
    "command": "Same shared Companion Command/global offense rules as Greater Fire Pet.",
    "attack": {
      "name": "Champion Strike",
      "activation": "commanded Action",
      "reachFt": 5,
      "targets": 1,
      "attackModifier": "original owner's current spell attack modifier",
      "damage": "2d8 + original owner's current PB slashing",
      "critical": "double 2d8 dice only; PB flat is not doubled"
    },
    "intrinsicGear": "Apparent armor/weapon/shield are intrinsic manifestation comprising AC/attack profile, not detachable inventory or faction stock.",
    "ending": "One Champion per owner across all factions. Replacement/concentration/source end/expiry/dismissal or ordinary non-Null 0 HP ends body. Genuine borrowed items remain real and drop/settle normally; intrinsic gear vanishes.",
    "nullHealing": "AC5-SUMMON-TARGET-01 + accepted finite-summon Null branch",
    "suppression": "AC5-ANTIMAGIC-SUMMON-01"
  }
}
```

## Complete sixteen spell procedures

### 1. Antimagic Field (Lesser) (`antimagic-field-lesser`)

**Source/access evidence**
```json
{
  "id": "antimagic-field-lesser",
  "name": "Antimagic Field (Lesser)",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Abjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "antimagic-field-lesser",
    "original": {
      "name": "Antimagic Field (Lesser)",
      "level": 5,
      "resonanceRank": 5,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Antimagic Field (Lesser)",
          "school": "Abjuration",
          "level": 5,
          "summary": "10-ft sphere suppresses magic effects and spells."
        }
      ],
      "classLevels": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "10-ft sphere suppresses magic effects and spells.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
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
        "index": 56,
        "original": {
          "school": "Abjuration",
          "level": 5,
          "name": "Antimagic Field (Lesser)",
          "effect": "10-ft sphere suppresses magic effects and spells.",
          "source_paragraph": 9049,
          "casting_time": "1 action",
          "range": "10 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 10 feet; V/S/F; base 10 RP. Preserve the source's 10-foot sphere and suppression promise. NEW: choose one perceived fixed point within 10 feet and line of effect; create a fixed 10-foot-radius sphere with concentration up to 60 elapsed seconds, explicitly replacing the source's insufficient Instantaneous field duration for this authored procedure. The volume is clipped by actual solid total-cover barriers from the center and never follows a creature.

The field suppresses the local expression of actual ongoing spells and explicitly magical nonspell technique expressions only where their real body/effect/anchor intersects the operative volume. It supplies no rank ceiling. It does not retroactively undo completed damage, healing, movement, transmutation, consumed items, permanent ordinary matter, HP loss or source history. It does not erase class engines, learned facts, RP pools, injuries or intrinsic nonmagical traits. A magic item keeps its mundane body/ownership/contents while its magical enhancements/actions are unavailable. A creature-attached spell buff is wholly unavailable while the creature intersects; a large wall/field loses only its intersecting portion unless its own indivisible source says otherwise.

An otherwise legal spell cast may still be committed inside: pay its real final price, Action/components/cadence and concentration transition. If the spell's relevant manifestation originates inside the field, suppress that payload at resolution; there is no queued later release and no refund. Do not invent an imaginary straight-line beam/path for teleportation or nonprojectile magic. For current Dimensional Door, an origin and endpoint both outside the field are unaffected even if a drawn line crosses it; an origin actually inside the field has its spell payload suppressed after legal commitment. A remote ongoing effect outside is not canceled merely because its concentrating caster enters the field.

Ranger Nature's Whisper is an explicitly magical NONSPELL technique. Inside the field its Action+1 RP+Recharge 3 commitment remains a nonspell event; the magical payload/rider is unavailable with no rank, Counterspell window or Nexus/Dampening price. A still-live Nature's Whisper rider on an actor inside the field is unusable while suppressed but its clock continues.

Oracle's Burden prevents generic remove/suspend of the intrinsic Oracle Curse, so this field does not erase or suspend the Curse engine. Curse Manifestation, Tongues and Consumed retain only their own exact suppression/appearance permissions and timers.

Instances of Lesser Antimagic do not suppress one another; overlapping instances form the union of active volumes. This same-family exception only prevents oscillation and grants no ability to cast a new field from inside another without paying/satisfying the new cast, whose payload is itself exempt only because it is this family.

For Greater Fire Pet and Faction Champion use AC5-ANTIMAGIC-SUMMON-01. For accepted ordinary Banishment, only actual suppression of the application itself invokes its own accepted closure/end rule; merely suppressing its distant caster does not reach the generated cell/application. For Banish Elemental and Elemental Banishment, AC5-BANISH-EXT-01 expressly gives the same close-on-actual-suppression behavior.

Suppression never pauses absolute/source clocks and does not bank missed attacks, aura starts, periodic damage, saves or commands. On exit/end, only still-live source expressions resume with the same remaining HP/pools/deadlines. Wall of Force uses its own safe segment-resumption rule.

Repair04 incoming/output completion: use AC5-ANTIMAGIC-IO-04. An instantaneous effect cast outside is not immune merely because its source is outside: inspect the actual recipient/area/destination manifestation. Local damage/healing inside is suppressed with no packet/root; an outside-origin Dimensional Door whose destination footprint is inside fails atomically after cost, while outside→outside remains unaffected regardless of an imaginary line. A legal Greater Dispel or exact class Dispel resolves captured termination operations under AC5-ANTIMAGIC-IO-04; the target Antimagic application ignores only its own suppression, while a different Antimagic field can still suppress that termination operation; ordinary Counterspell remains only a cast-time response before the field exists. Spell Preservation’s primary-book anti-destruction remains source-intrinsic even while magical book usability is suppressed.

### 2. Banish Elemental (`banish-elemental`)

**Source/access evidence**
```json
{
  "id": "banish-elemental",
  "name": "Banish Elemental",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Abjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "banish-elemental",
    "original": {
      "name": "Banish Elemental",
      "level": 5,
      "resonanceRank": 5,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Banish Elemental",
          "school": "Abjuration",
          "level": 5,
          "summary": "Instantly banish an elemental or outsider (CHA save negates)."
        }
      ],
      "classLevels": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Instantly banish an elemental or outsider (CHA save negates).",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
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
        "index": 57,
        "original": {
          "school": "Abjuration",
          "level": 5,
          "name": "Banish Elemental",
          "effect": "Instantly banish an elemental or outsider (CHA save negates).",
          "source_paragraph": 9050,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Charisma save",
          "tags": [
            "Utility"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; source Charisma save/Instantaneous metadata retained. Target one perceived creature within 60 feet and line of effect. It is eligible only if current authoritative creature data explicitly says creatureType=Elemental OR explicitly supplies an `outsider` classification/tag for that body. Summoned, extraplanar, foreign, fiendish-looking or unknown-provenance are not synonyms. If eligibility is hidden/unknown, a legal cast may commit and later fail without revealing which fact failed.

Commit ordinary spell costs/concentration transition/counter window, then make the printed CHA save vs actual spell DC. Success: no exile. Failure: require and spend the existing shared hard-control allowance for this source-character/target/encounter; if unavailable, no exile and no soft fallback.

NEW source completion: successful failure creates a nonconcentration exile application lasting 60 elapsed seconds. The source's Instantaneous metadata is preserved as the cast/resolution metadata; the continuing exile deadline is explicit NEW authorship rather than a source rewrite. Use AC5-BANISH-EXT-01 for the generated BAN-CELL-03 cell, same-identity/custody rules, separate-creature handling, legal independent escape, all real clocks, BAN-CLOSE-03 return, canonical placement/BAN-CONFLICT-04 and the narrow terminal endpoint-blocker exception. This spell does not send the target to a named/native/home plane and learns no origin fact.

If the target's independent finite creature source ends in the cell, the body ends normally; close this application immediately and settle only genuine surviving loose cargo. Actual suppression of this exile application closes/ends it rather than pausing it. Death/corpse/body changes inside retain their real rules.

### 3. Greater Dispel (`greater-dispel`)

**Source/access evidence**
```json
{
  "id": "greater-dispel",
  "name": "Greater Dispel",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Abjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "greater-dispel",
    "original": {
      "name": "Greater Dispel",
      "level": 5,
      "resonanceRank": 5,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Greater Dispel",
          "school": "Abjuration",
          "level": 5,
          "summary": "End multiple magical effects in 30-ft radius."
        }
      ],
      "classLevels": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "End multiple magical effects in 30-ft radius.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
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
        "index": 58,
        "original": {
          "school": "Abjuration",
          "level": 5,
          "name": "Greater Dispel",
          "effect": "End multiple magical effects in 30-ft radius.",
          "source_paragraph": 9051,
          "casting_time": "1 action",
          "range": "30 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; casting-point range 30 feet; V/S/F; base 10 RP; Instantaneous. Choose one perceived center within 30 feet. At resolution take one immutable snapshot of every ongoing independently addressable magical effect application having an affected body, discrete anchor/object effect, or freestanding area portion inside the 30-foot-radius sphere and center line of effect. Allies are included. Individual effect perception is not required; no numerical cap or selective post-result omission exists.

Eligible ordinary spell applications retain their original generating rank. Rank 0-5 ends automatically. Rank 6-9 requires one check per original generating cast using the caster's actual spellcasting ability + PB against DC 10 + 2×recorded rank. Reuse that one roll for all captured applications from the same generating cast. Apply current Core task degrees/natural shifts. A nonspell magical component is eligible only if its own source explicitly supplies a dispel interface/rank/DC; never assign rank 0 by appearance or RP cost.

Capture is fixed before any endings. If a captured Wall of Force ends and reveals another effect behind it, that effect is not added. A captured indivisible wall/field ends as one effect on successful/automatic dispel; recipient-specific applications from one cast end only where captured unless their real parent dependency says ending one ends all. Suppressed-but-still-existing records can be dispelled if this cast itself can reach them. Completed instantaneous consequences, permanent matter, class engines, permanent item enchantments and explicitly nondispellable effects are outside scope.

This is distinct from Wizard class Dispel Magic `/cards/19`: that class spell costs 3 RP, range 60, Recharge 2, auto through rank 3, and uses INT+PB vs DC 10+rank above 3. Sigil Authority `/cards/22` names Counterspell and Dispel Magic only and does not modify Greater Dispel. Xi remains its own consent-based branch-ending source and grants no Greater Dispel permission.

### 4. Spell Resistance (`spell-resistance`)

**Source/access evidence**
```json
{
  "id": "spell-resistance",
  "name": "Spell Resistance",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Abjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "spell-resistance",
    "original": {
      "name": "Spell Resistance",
      "level": 5,
      "resonanceRank": 5,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Spell Resistance",
          "school": "Abjuration",
          "level": 5,
          "summary": "Target gains advantage on saves against spells for 1 hour."
        }
      ],
      "classLevels": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Target gains advantage on saves against spells for 1 hour.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
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
        "index": 59,
        "original": {
          "school": "Abjuration",
          "level": 5,
          "name": "Spell Resistance",
          "effect": "Target gains advantage on saves against spells for 1 hour.",
          "source_paragraph": 9052,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "1 hour",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Ward"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; one willing perceived creature with line of effect; duration 3600 elapsed seconds, no concentration. For the duration, the target has ordinary advantage on every saving throw directly required by an actual spell or that spell's still-dependent ongoing/periodic rider, including a printed repeat/ending save and an item/ancestry cast that is genuinely a spell. Spell provenance, not RP payment or appearance, controls.

No save is invented for an automatic spell. This grants no attack disadvantage, AC, damage resistance, immunity or rank ceiling. It does not apply to Counterspell/Dispel ability checks, generic concentration saves caused by damage, Wound/death saves, mundane aftermath, or nonspell class/monster/item techniques.

Advantage does not stack. A Shaman whose `/cards/41` Spell Resistance already grants advantage still rolls one advantaged save. Thief Arcane Resistance `/cards/21` is a separate +2 to spell saves and can combine with the one advantage. Druid Nature's Ward applies only its printed immunities and does not turn every Elemental/Fey/planar effect into automatic success.

Suppression makes this advantage unavailable while the target/application is suppressed, but its one-hour clock continues; missed saves are not rerolled later. Recasting creates a separate paid application with its own expiry but still only one ordinary advantage at a given save.

### 5. Wall of Force (`wall-of-force`)

**Source/access evidence**
```json
{
  "id": "wall-of-force",
  "name": "Wall of Force",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Abjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "wall-of-force",
    "original": {
      "name": "Wall of Force",
      "level": 5,
      "resonanceRank": 5,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Wall of Force",
          "school": "Abjuration",
          "level": 5,
          "summary": "Create an invisible, impenetrable wall."
        }
      ],
      "classLevels": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Create an invisible, impenetrable wall.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
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
        "index": 60,
        "original": {
          "school": "Abjuration",
          "level": 5,
          "name": "Wall of Force",
          "effect": "Create an invisible, impenetrable wall.",
          "source_paragraph": 9053,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Utility"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds. Create one fixed invisible flat rectangular plane up to 30 feet long × 15 feet high × 1 inch thick in any chosen orientation. Every part must lie within 60 feet and the intended near surface must be perceivable with line of effect. The wall may meet existing supports but cannot overlap a creature or independent object at creation; hidden occupancy can defeat the paid placement without diagnostic or automatic reshaping.

The wall supports itself and ordinary loads on either side, including horizontal platform use. It has no AC/HP and is impenetrable to ordinary physical bodies, projectiles, liquids, gas and sound. Ordinary light/vision passes through it; it remains visually invisible, though touch or an applicable magical sense can reveal the boundary. It blocks ordinary spell/effect line of effect and other effects requiring a physical path. Its finite edges remain open routes.

Do not infer a teleport path. Accepted Dimensional Door has no traversed path and may move from one legal endpoint to another even if a drawn line would intersect the wall, provided its own endpoint/knowledge rules pass. Resonance Beacon likewise uses its own teleport endpoint, not an imagined wall crossing. Dimensional Anchor remains an independent endpoint blocker. A destination footprint cannot overlap the wall itself.

The wall creates no oxygen deletion or automatic breathable volume. It never pushes/crushes at creation/end. Suppression removes only intersecting wall portions while concentration/deadline continues. On resumption recreate only clear portions; an occupied closing segment remains locally pending until clear, without severing/shoving. Expiry/removal ends support immediately and actual unsupported bodies begin ordinary Falling from their current location, one real Fall Marker.

Repair04 resumption geometry uses AC5-WALL-PANELS-04: fixed 2.5-foot panels/edge remainders retain exact suppressed-portion geometry. A previously suppressed portion whose 1-inch volume is occupied remains wholly absent until clear; wall portions that were never suppressed remain solid. No push, cut, crush or arbitrary hole.

### 6. Resonance Barrier (`resonance-barrier`)

**Source/access evidence**
```json
{
  "id": "resonance-barrier",
  "name": "Resonance Barrier",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Abjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "resonance-barrier",
    "original": {
      "name": "Resonance Barrier",
      "level": 5,
      "resonanceRank": 5,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Resonance Barrier",
          "school": "Abjuration",
          "level": 5,
          "summary": "Convert Resonance Points into a damage-absorbing shield."
        }
      ],
      "classLevels": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Convert Resonance Points into a damage-absorbing shield.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
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
        "index": 61,
        "original": {
          "school": "Abjuration",
          "level": 5,
          "name": "Resonance Barrier",
          "effect": "Convert Resonance Points into a damage-absorbing shield.",
          "source_paragraph": 9054,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Ward",
            "Resonance"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds; one willing perceived creature with line of effect. Before commitment choose protected conversion principal X from 0..actual caster PB. X is separately paid RP, cannot be discounted/waived by Nexus, Dampening or Influence, and is not part of ordinary spell pricing.

Price the spell through AC5-PRICE-01. For pool credit, compute `creditableBasePaid`: the actual ordinary base component paid after exact base/source reductions and Nexus; Dissonance, Dampening +2, Burden and other surcharges are noncreditable. If final Ease reduces the RP-priced spell amount, allocate Ease against creditable base first, floor 0, then any remaining reduction against noncreditable components. Protected X is separately creditable. Initial prevention pool = 5 × (creditableBasePaid + X). If this is 0, the fresh application cannot form even if some noncreditable surcharge was paid.

This is pure finite damage prevention, not temp HP, AC, armor, a physical object or maximum HP. For an eligible incoming damage packet, apply ordinary type defenses first, then this pool before post-defense damage transfer and temp HP. Spend only actual prevented points. A transferred branch explicitly skipping another prevention/mitigation stage cannot consume this pool. Prevented points are not actualDamageDealt and cannot trigger drain/heal/reflection/recovery.

Same-name pools never add: compare offered pool to currently retained remaining pool. Stronger replaces; equal/weaker paid offer does not refresh retained expiry/source. Suppression makes remaining pool unavailable without spending/refilling it; clocks continue. Pool ends at 0, concentration loss, expiry, recipient death or eligible removal. No refund/cash-out.

Example current price: base10, Dampening +2, pending Ease -1, X2, no Nexus. RP-priced amount 10+2-1=11; Ease reduces creditable base10→9; then separately pay X2 = total13; pool =5×(9+2)=55. With Nexus, base10→8, +2 Dampening→10, Ease→9, X2 total11; creditable base8→7; pool45.

Repair03 lifecycle/price completion: AC5-BARRIER-RECAST-03 controls same-name recasts and concentration. Same-caster recast ends the old concentration/application at new commitment before comparison. Different-caster equal/weaker fresh offer ends only the fresh application/concentration at resolution; stronger replaces the retained pool. AC5-PRICE-01 now uses explicit buckets: creditable base, noncreditable pre-Nexus extras, post-Nexus Dampening/final Influence, and protected X. No surcharge is pool credit.

### 7. Planar Protection (`planar-protection`)

**Source/access evidence**
```json
{
  "id": "planar-protection",
  "name": "Planar Protection",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Abjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "planar-protection",
    "original": {
      "name": "Planar Protection",
      "level": 5,
      "resonanceRank": 5,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Planar Protection",
          "school": "Abjuration",
          "level": 5,
          "summary": "Area is warded against creatures from a specific plane."
        }
      ],
      "classLevels": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Area is warded against creatures from a specific plane.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
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
        "index": 62,
        "original": {
          "school": "Abjuration",
          "level": 5,
          "name": "Planar Protection",
          "effect": "Area is warded against creatures from a specific plane.",
          "source_paragraph": 9055,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, M/F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Planar",
            "Ward"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/M/F; base 10 RP; concentration up to 60 elapsed seconds. Before payment choose one actual opaque `planeKey` already established in campaign/source records and one perceived center within 60 feet and line of effect. Create a fixed 15-foot-radius spherical ward, clipped by actual solid center line of effect.

Eligibility for ordinary physical entry uses committed operational provenance: `lastArrivedFromPlaneKey == chosenPlaneKey` or, where no travel record exists, exact `createdFromPlaneKey == chosenPlaneKey`. Creature type, Elemental/outsider label, mortal Wheel name, soul/native origin and current location are insufficient. Indeterminate provenance remains Indeterminate.

For an incoming cross-plane transition do NOT read stale committed history. Use AC5-PLANAR-ARRIVAL-03: snapshot immutable `prospectiveOriginPlaneKey` from the body’s actual origin plane immediately before that transition and evaluate this destination ward before placement. Any part of the body/group terminal footprint entering the sphere makes that body eligible for the ward check. A successful atomic transition then commits `lastArrivedFromPlaneKey = prospectiveOriginPlaneKey`; failed transit leaves prior history unchanged and gives no free provenance report.

An eligible creature already inside when the ward forms is not expelled, suppressed or damaged. It may move within and leave; after leaving it cannot cross inward while still eligible. Supported walking/carried/forced inward movement stops at the last legal exterior position, with no free shove/damage. A carried creature remains a separate body. An actual teleport/portal destination whose footprint would enter fails atomically for that body/group under its own cost rules. Outside-to-outside teleport beyond the sphere is unaffected; no imaginary path is tested.

The ward creates no support. Under AC5-PLANAR-FALL-03, continuous unsupported ordinary Falling is never suspended at the boundary: if the last exterior point is unsupported, the Fall Marker continues through the sphere; the body then counts as already inside. This exception applies only to unsupported continuous Falling, not grounded/otherwise supported crossing.

Suppression opens the boundary and clocks continue. Bodies entering during suppression are already-inside on resumption: no ejection/crush. Ending grants no damage, concealment, attack immunity, information disclosure or native-plane determination.

### 8. Reputation Shield (`reputation-shield`)

**Source/access evidence**
```json
{
  "id": "reputation-shield",
  "name": "Reputation Shield",
  "schools": [
    "Abjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Abjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "reputation-shield",
    "original": {
      "name": "Reputation Shield",
      "level": 5,
      "resonanceRank": 5,
      "school": "Abjuration",
      "schools": [
        "Abjuration"
      ],
      "placements": [
        {
          "name": "Reputation Shield",
          "school": "Abjuration",
          "level": 5,
          "summary": "Target's reputation cannot be lowered for 24 hours."
        }
      ],
      "classLevels": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Cleric": "Abjuration",
        "Druid": "Abjuration",
        "Mage": "Abjuration",
        "Tinker": "Abjuration",
        "Wizard": "Abjuration",
        "Paladin": "Abjuration"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Target's reputation cannot be lowered for 24 hours.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Druid",
        "Mage",
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
        "index": 63,
        "original": {
          "school": "Abjuration",
          "level": 5,
          "name": "Reputation Shield",
          "effect": "Target's reputation cannot be lowered for 24 hours.",
          "source_paragraph": 9056,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "24 hours",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Ward"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; one willing perceived creature with line of effect; 86400 elapsed seconds; no concentration. Protect all of that creature's actual institutional standing-v1 records from genuine new negative signed contributions while the shield is operative. A newly encountered faction can initialize ordinary baseline 0 and is then protected.

At each distinct EX58/reputation consequence assignment, keep the full event/provenance/signed proposed amount. Replace an otherwise valid negative contribution with 0 and record `preventedByReputationShield`; do not defer it as debt. Positive contributions remain and use ordinary per-scene signed cap and absolute bounds. Current standing is not frozen at cast-time floor; later gains remain gains and later negative contributions are still prevented.

This does not rewrite a negative event that actually occurred before the shield began, and does not block correction of an erroneous stored score, deduplication or provenance repair. A genuine voluntary transaction requiring payment/surrender of standing cannot receive its benefit while the shield prevents that negative payment; the target can voluntarily end its own shield on its turn without an Action if it wants to pay. Suppression allows new negative consequences normally; resumption does not repair them.

No memories/evidence/law/contracts/fees/allegiance/hostility/consent or NPC agency are changed. Multiple shields still provide only one prevention while any is active, with separate clocks. Expiry creates no deferred penalty and restores no past standing.

### 9. Summon Greater Fire Pet (`summon-greater-fire-pet`)

**Source/access evidence**
```json
{
  "id": "summon-greater-fire-pet",
  "name": "Summon Greater Fire Pet",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Ranger": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Shaman": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "summon-greater-fire-pet",
    "original": {
      "name": "Summon Greater Fire Pet",
      "level": 5,
      "resonanceRank": 5,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Summon Greater Fire Pet",
          "school": "Conjuration",
          "level": 5,
          "summary": "HP 60, AC 17, 2d10 fire, aura burns adjacent foes."
        }
      ],
      "classLevels": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classRanks": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classLearnLevels": {
        "Druid": 9,
        "Mage": 9,
        "Ranger": 17,
        "Shaman": 13,
        "Tinker": 18,
        "Wizard": 9
      },
      "classSchools": {
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
      "description": "HP 60, AC 17, 2d10 fire, aura burns adjacent foes.",
      "alternateSummaries": [],
      "classes": [
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
        "index": 160,
        "original": {
          "school": "Conjuration",
          "level": 5,
          "name": "Summon Greater Fire Pet",
          "effect": "HP 60, AC 17, 2d10 fire, aura burns adjacent foes.",
          "source_paragraph": 9178,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Damage",
            "Summoning"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds. Create one Greater Fire Pet in one perceived supported unoccupied footprint that fits its Medium body and has line of effect. Use AC5-PROFILE-GREATER-FIRE-PET-01 exactly: HP60, AC17, Speed30, commanded 5-ft Fire Strike for 2d10 fire using original owner's current spell attack, and the passive 5-ft aura.

The aura is not an entry trigger. At each perceived hostile recipient's future regular START while within 5 feet and body-to-recipient line of effect, make DEX vs original owner's current spell DC; failure takes 1d6 fire, success half floor. Max one aura attempt per owner/target/Greater-Fire-Pet family/numbered round, outside initiative once per six seconds. One d6 may be shared across the cycle but saves/defenses/damage roots are per recipient. The owner cannot use the aura as hidden allegiance detection: only creatures the conscious owner actually perceives/regards as hostile qualify.

Use shared Companion Command/global offense budget for Fire Strike; aura is the printed passive exception and does not grant another offensive Action. One Greater Fire Pet per owner, distinct from lower Fire Pet body cap but not from the owner-wide command/offense allowance.

Damage-root identity follows AC5-ROOT-01: commanded attack dealer=pet; each aura recipient root dealer=pet at that START. Owner Null Veil never automatically converts pet damage. Apply AC5-SUMMON-TARGET-01/accepted Null lifecycle: qualifying Null damage to 0 keeps this same finite body Disabled 0 while concentration/source remains, including subsequent Null hits; legal Healing Rite/ordinary living-ally HP healing can restore above 0. Ordinary non-Null damage to 0 removes the body normally. Independent expiry/concentration/replacement still ends it.

Under Lesser Antimagic use AC5-ANTIMAGIC-SUMMON-01. No fire immunity, extra light, fuel, generic Burning condition, corpse or harvestable elemental material is inferred.

### 10. Massive Elemental Blast (`massive-elemental-blast`)

**Source/access evidence**
```json
{
  "id": "massive-elemental-blast",
  "name": "Massive Elemental Blast",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Ranger": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Shaman": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "massive-elemental-blast",
    "original": {
      "name": "Massive Elemental Blast",
      "level": 5,
      "resonanceRank": 5,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Massive Elemental Blast",
          "school": "Conjuration",
          "level": 5,
          "summary": "All enemies in 20 ft radius: 5d8 elemental damage."
        }
      ],
      "classLevels": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classRanks": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classLearnLevels": {
        "Druid": 9,
        "Mage": 9,
        "Ranger": 17,
        "Shaman": 13,
        "Tinker": 18,
        "Wizard": 9
      },
      "classSchools": {
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
      "description": "All enemies in 20 ft radius: 5d8 elemental damage.",
      "alternateSummaries": [],
      "classes": [
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
        "index": 161,
        "original": {
          "school": "Conjuration",
          "level": 5,
          "name": "Massive Elemental Blast",
          "effect": "All enemies in 20 ft radius: 5d8 elemental damage.",
          "source_paragraph": 9179,
          "casting_time": "1 action",
          "range": "20 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Damage"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; casting-point range 20 feet; V/S/F; base 10 RP; Instantaneous. Before payment choose one perceived center within 20 feet and center line of effect, and choose exactly one damage type for the whole cast from acid, cold, fire or lightning. This finite menu is NEW and source-compatible; it does not create a generic `elemental` damage type.

At resolution snapshot every creature in the 20-foot-radius sphere that the caster currently perceives and affirmatively regards as an enemy from available information and that is reached by center line of effect. There is no target-count cap and no hidden allegiance/Invisible-enemy detection. Each target makes DEX vs actual spell DC. Roll 5d8 once; failed save takes full chosen type, success takes half floor, then apply each target's real defenses independently. Each recipient receives a separate damage root under AC5-ROOT-01 with dealer=caster; shared dice do not merge recipient roots.

No objects/allies outside the stated enemy-creature predicate receive this spell packet. No lingering terrain, slow, Burning, corrosion, conductivity chain, fuel/material stock or summoned Elemental is created. Mage Arcane Bypass can be declared for this damaging Mage spell and ignores printed resistance to the chosen type only; immunity remains. Tinker Malfunction Field does not apply because this spell uses saves, not spell attacks.

### 11. Living Magma (`living-magma`)

**Source/access evidence**
```json
{
  "id": "living-magma",
  "name": "Living Magma",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Ranger": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Shaman": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "living-magma",
    "original": {
      "name": "Living Magma",
      "level": 5,
      "resonanceRank": 5,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Living Magma",
          "school": "Conjuration",
          "level": 5,
          "summary": "Target must CON save or suffer 1d10/round for 3 rounds."
        }
      ],
      "classLevels": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classRanks": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classLearnLevels": {
        "Druid": 9,
        "Mage": 9,
        "Ranger": 17,
        "Shaman": 13,
        "Tinker": 18,
        "Wizard": 9
      },
      "classSchools": {
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
      "description": "Target must CON save or suffer 1d10/round for 3 rounds.",
      "alternateSummaries": [],
      "classes": [
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
        "index": 162,
        "original": {
          "school": "Conjuration",
          "level": 5,
          "name": "Living Magma",
          "effect": "Target must CON save or suffer 1d10/round for 3 rounds.",
          "source_paragraph": 9180,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "3 rounds",
          "components": "V, S, F",
          "resolution": "Constitution save",
          "tags": [
            "Damage"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; one perceived creature with line of effect; source duration 3 rounds. NEW damage type is fire. At resolution target makes the printed CON save vs spell DC. Success prevents this new application. Failure establishes one target-bound recurring magical rider and, under AC5-ROOT-01, creates its damage root immediately at establishment even though no immediate damage packet occurs.

The rider has exactly three future target regular-START damage opportunities. An already underway START is not counted. Each opportunity rolls 1d10 fire separately and resolves ordinary defenses/HP/life consequences. No repeat save and no concentration are added. Outside initiative schedule at application+6,+12,+18 seconds; preserve these ordinal deadlines through initiative transitions/extra turns.

All three ticks descend from the root created on failed-save establishment and inherit that root's creation-time Null flag. Later caster Veil changes do not rewrite them. If a scheduled tick is actually suppressed, consume that ordinal without a damage packet/root child and do not bank/make it up. Fire immunity/prevention can make a tick 0 without ending remaining opportunities. Death/body removal ends the rider; merely reaching 0 while still an active creature does not invent early ending.

One Living Magma application per target across casters. A newly paid cast that successfully fails the target save replaces the still-live older rider; a successful save leaves the old rider intact. The name creates no magma creature/pool/terrain/light/entrapment/generic Burning and ordinary water does not remove it unless an exact source removes ongoing magic.

### 12. Elemental Banishment (`elemental-banishment`)

**Source/access evidence**
```json
{
  "id": "elemental-banishment",
  "name": "Elemental Banishment",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Ranger": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Shaman": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "elemental-banishment",
    "original": {
      "name": "Elemental Banishment",
      "level": 5,
      "resonanceRank": 5,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Elemental Banishment",
          "school": "Conjuration",
          "level": 5,
          "summary": "Remove 1 summoned enemy from battlefield (CHA save)."
        }
      ],
      "classLevels": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classRanks": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classLearnLevels": {
        "Druid": 9,
        "Mage": 9,
        "Ranger": 17,
        "Shaman": 13,
        "Tinker": 18,
        "Wizard": 9
      },
      "classSchools": {
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
      "description": "Remove 1 summoned enemy from battlefield (CHA save).",
      "alternateSummaries": [],
      "classes": [
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
        "index": 163,
        "original": {
          "school": "Conjuration",
          "level": 5,
          "name": "Elemental Banishment",
          "effect": "Remove 1 summoned enemy from battlefield (CHA save).",
          "source_paragraph": 9181,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Charisma save",
          "tags": [
            "Summoning"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds; printed CHA save. Target exactly one perceived creature within range/line of effect that (a) the caster currently regards as an enemy from available information and (b) has an actual active summon-source identity proving this body was created/summoned by a still-recognizable source. Elemental type, outsider label and extraplanar provenance are irrelevant. A natural Elemental is not eligible merely for being Elemental; an eligible summoned non-Elemental can qualify. Hidden/unknown summon provenance may defeat a paid cast without diagnostic.

Commit ordinary costs/concentration/counter timing, then target makes CHA save. Success: no removal. Failure: require/spend the shared hard-control allowance; if unavailable no exile. On successful failed-save establishment, remove that same summoned enemy to an AC5-BANISH-EXT-01 cell for this spell's own concentration duration. Do not desummon it or send it to a home/native plane.

Use the accepted Banishment custody/real-clock/legal-escape/closure/body-placement interfaces only through AC5-BANISH-EXT-01. A separate carried creature is not gear and does not travel automatically. Genuine noncreature gear/cargo that legally accompanies the target remains the same inventory.

If the summon source itself ends/expires/dismisses/replaces the body while exiled, the body ends under that source; Elemental Banishment ends immediately and closes the cell, returning only surviving genuine loose cargo. Actual suppression of this exile application closes/ends it rather than pausing. Current endpoint blockers apply at establishment; terminal closure keeps the narrow accepted Banishment-only blocker exception through this explicit extension.

### 13. Planar Binding (`planar-binding`)

**Source/access evidence**
```json
{
  "id": "planar-binding",
  "name": "Planar Binding",
  "schools": [
    "Conjuration",
    "Universal"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Bard": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Universal",
      "baseRpCost": 10
    },
    "Cleric": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Universal",
      "baseRpCost": 10
    },
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mirrorsage": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Universal",
      "baseRpCost": 10
    },
    "Ranger": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Shaman": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Paladin": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Universal",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "planar-binding",
    "original": {
      "name": "Planar Binding",
      "level": 5,
      "resonanceRank": 5,
      "school": "Conjuration",
      "schools": [
        "Conjuration",
        "Universal"
      ],
      "placements": [
        {
          "name": "Planar Binding",
          "school": "Conjuration",
          "level": 5,
          "summary": "Force an extraplanar creature to serve you for 24 hours."
        },
        {
          "name": "Planar Binding",
          "school": "Universal",
          "level": 5,
          "summary": "Bind extraplanar creature to service."
        }
      ],
      "classLevels": {
        "Bard": 5,
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Mirrorsage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classRanks": {
        "Bard": 5,
        "Cleric": 5,
        "Druid": 5,
        "Mage": 5,
        "Mirrorsage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5,
        "Paladin": 5
      },
      "classLearnLevels": {
        "Bard": 13,
        "Cleric": 9,
        "Druid": 9,
        "Mage": 9,
        "Mirrorsage": 13,
        "Ranger": 17,
        "Shaman": 13,
        "Tinker": 18,
        "Wizard": 9,
        "Paladin": 17
      },
      "classSchools": {
        "Bard": "Universal",
        "Cleric": "Universal",
        "Druid": "Conjuration",
        "Mage": "Conjuration",
        "Mirrorsage": "Universal",
        "Ranger": "Conjuration",
        "Shaman": "Conjuration",
        "Tinker": "Conjuration",
        "Wizard": "Conjuration",
        "Paladin": "Universal"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Force an extraplanar creature to serve you for 24 hours.",
      "alternateSummaries": [
        "Bind extraplanar creature to service."
      ],
      "classes": [
        "Bard",
        "Cleric",
        "Druid",
        "Mage",
        "Mirrorsage",
        "Ranger",
        "Shaman",
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
        "index": 164,
        "original": {
          "school": "Conjuration",
          "level": 5,
          "name": "Planar Binding",
          "effect": "Force an extraplanar creature to serve you for 24 hours.",
          "source_paragraph": 9182,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "24 hours",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Planar"
          ],
          "rp_cost": 10
        }
      },
      {
        "index": 895,
        "original": {
          "school": "Universal",
          "level": 5,
          "name": "Planar Binding",
          "effect": "Bind extraplanar creature to service.",
          "source_paragraph": 10088,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Planar"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP. Preserve both printed placements/access records. The Conjuration source promises 24-hour service; Universal Instantaneous remains establishment metadata. NEW reconciliation: successful binding establishment is instantaneous and creates a nonconcentration service record lasting 86,400 elapsed seconds.

Target one perceived active creature within60/LoE whose current body has explicit operational extraplanar evidence under AC5-PLANAR-META-01: exact current source marks it extraplanar relative to current plane, or committed travel/source provenance proves arrival/creation from a different actual planeKey. Type/outsider/Elemental/summoned labels, Wheel names and supposed native/soul origin are insufficient. Unknown evidence can defeat a paid cast without disclosure.

NEW save: CHA vs actual spell DC; willing target may elect failure. On failure require/spend the shared hard-control allowance. Success creates no service record. Failure creates one live binder→target record until t+86,400 seconds, target death/body-source ending, eligible removal/dispel or replacement of that same binder→target record. It never extends the target’s own source life.

Use AC5-BINDING-ORDER-03. One pending order maximum per binder→target record. Issuance requires same-plane command-intent and the real Bonus Action/6-second order cadence. A pending order binds the next regular target behavior opportunity after issue and expires at the end of that opportunity whether obeyed, impossible, suppressed or budget-starved. A later valid same-Binding order replaces the prior pending order. Plane separation blocks new issuance but does not erase an already-heard pending order. Suppression at execution makes the order ineffective and expired; the 24-hour clock continues.

Orders may require ordinary movement, basic Attack, Dodge, Disengage, Help, Interact or an at-will action the creature genuinely possesses. They cannot compel RP/spells, charges, recharge/per-rest abilities, consumables/special expendables, permanent property transfer, protected secrets, knowingly binding-oath violation, direct self-harm or knowingly suicidal routes. Orders arbitrate through accepted Compelled Budget Arbitration and never create another Action/turn/Reaction/Bonus Action/resource.

For companions, the owner’s exact command/offense gate remains prerequisite. Binding cannot manufacture that gate. If an owner legally opens one companion damaging action and a pending Binding Attack order conflicts only on target selection, priority/arbitration constrains that one available action; no second attack exists. If no source-gated action becomes available in the order’s execution opportunity, it expires.

Finite summon concentration/expiry/replacement/0HP remain real. Lesser Antimagic suppresses local compulsion expression on an intersecting target without pausing the service clock.

### 14. Resonance Nexus (`resonance-nexus`)

**Source/access evidence**
```json
{
  "id": "resonance-nexus",
  "name": "Resonance Nexus",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Ranger": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Shaman": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "resonance-nexus",
    "original": {
      "name": "Resonance Nexus",
      "level": 5,
      "resonanceRank": 5,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Resonance Nexus",
          "school": "Conjuration",
          "level": 5,
          "summary": "Create a field where all spells cost 2 fewer Resonance Points."
        }
      ],
      "classLevels": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classRanks": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classLearnLevels": {
        "Druid": 9,
        "Mage": 9,
        "Ranger": 17,
        "Shaman": 13,
        "Tinker": 18,
        "Wizard": 9
      },
      "classSchools": {
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
      "description": "Create a field where all spells cost 2 fewer Resonance Points.",
      "alternateSummaries": [],
      "classes": [
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
        "index": 165,
        "original": {
          "school": "Conjuration",
          "level": 5,
          "name": "Resonance Nexus",
          "effect": "Create a field where all spells cost 2 fewer Resonance Points.",
          "source_paragraph": 9183,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Resonance"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; source Instantaneous metadata preserved. NEW: create a fixed 10-foot-radius nonphysical sphere at a perceived point within 60 feet/line of effect, concentration up to 60 elapsed seconds. It grants no support/cover, stores no RP and is clipped by actual center line of effect.

An actual spell cast qualifies once, at legal cast commitment, when its original caster's occupied body intersects the operative sphere. Target/area may be outside. Familiar/Echo/projection origin does not substitute for caster location. Actual Reaction spells qualify. Paying RP for a nonspell technique does not. A readied spell is priced at original cast commitment, not release.

Use AC5-PRICE-01 exactly. Nexus is one ordinary -2 reduction after exact class/source reductions/waivers/minima and before AC4 Dampening +2 and final Influence. Overlapping Nexuses provide one -2 total. Nexus cannot reduce protected Resonance Barrier X, HP/material/charge/use costs or standalone nonspell transfers. A route with no ordinary RP-price interface has no Nexus amount to reduce; accepted Dampening may independently create its +2 interface.

A Nexus never retroactively prices its own creation. If beginning a new Nexus ends the caster's prior concentration Nexus, the old field cannot discount the replacement because concentration transition occurs at new commitment; another owner's already-operative field can. Movement/suppression after commitment does not alter/refund the paid price. Suppression simply removes eligibility for future commitments while the original deadline continues.

Repair03 allocation note: Nexus reduces the pre-Dampening discountable bucket by2, taking creditable base first then other pre-Nexus extras. It never reduces protected Barrier X or accepted Dampening’s later +2. Final Influence applies afterward under AC5-PRICE-01.

### 15. Faction Champion (`faction-champion`)

**Source/access evidence**
```json
{
  "id": "faction-champion",
  "name": "Faction Champion",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Ranger": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Shaman": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "faction-champion",
    "original": {
      "name": "Faction Champion",
      "level": 5,
      "resonanceRank": 5,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Faction Champion",
          "school": "Conjuration",
          "level": 5,
          "summary": "Summon a powerful warrior from your allied faction."
        }
      ],
      "classLevels": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classRanks": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classLearnLevels": {
        "Druid": 9,
        "Mage": 9,
        "Ranger": 17,
        "Shaman": 13,
        "Tinker": 18,
        "Wizard": 9
      },
      "classSchools": {
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
      "description": "Summon a powerful warrior from your allied faction.",
      "alternateSummaries": [],
      "classes": [
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
        "index": 166,
        "original": {
          "school": "Conjuration",
          "level": 5,
          "name": "Faction Champion",
          "effect": "Summon a powerful warrior from your allied faction.",
          "source_paragraph": 9184,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Concentration, up to 1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Summoning",
            "Faction"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; concentration up to 60 elapsed seconds. Before payment choose one canonical factionId and satisfy AC5-CHAMPION-ALLY-01: actual alliedStatus=true, current standing >0, actual invocation permission, and no explicit aid prohibition. Positive standing alone, faction membership alone, Faction Ally membership+permission, or Faction Portal standing+HQ are not substitutes. Hidden loss of eligibility can prevent formation after a paid cast without revealing secret institutional facts.

NEW interpretation of `summon a powerful warrior from your allied faction`: create one bounded temporary Faction Champion representative using AC5-PROFILE-FACTION-CHAMPION-01, rather than transporting/copying a named real NPC. It has no private faction memories, real official identity/rank, contracting authority, secrets or institutional command. Intrinsic martial gear is profile manifestation, not faction inventory/loot.

Place the Medium body in one perceived supported unoccupied fitting footprint within 60 feet/LoE. Use shared Companion Command/global offense rules and its one Champion Strike. One Champion per owner across all factions. A later standing change does not remotely end an already admitted body; the source continues until concentration/expiry/replacement/dismissal/ordinary non-Null 0 HP or real removal.

Apply AC5-SUMMON-TARGET-01/accepted Null lifecycle: qualifying Null damage reaching 0 gives Disabled 0 while source persists; repeated Null hits do not create ordinary death; legal ordinary living-ally HP healing can restore above 0. Under Lesser Antimagic use AC5-ANTIMAGIC-SUMMON-01. Genuine borrowed items remain real/drop normally; intrinsic gear vanishes. No automatic reputation gain, expedition seat, hireling, formula teaching, faction credential, soul/native origin or distant-NPC injury exists.

### 16. Alignment Portal (`alignment-portal`)

**Source/access evidence**
```json
{
  "id": "alignment-portal",
  "name": "Alignment Portal",
  "schools": [
    "Conjuration"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Druid": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Mage": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Ranger": {
      "rank": 5,
      "minimumClassLevel": 17,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Shaman": {
      "rank": 5,
      "minimumClassLevel": 13,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Tinker": {
      "rank": 5,
      "minimumClassLevel": 18,
      "school": "Conjuration",
      "baseRpCost": 10
    },
    "Wizard": {
      "rank": 5,
      "minimumClassLevel": 9,
      "school": "Conjuration",
      "baseRpCost": 10
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "alignment-portal",
    "original": {
      "name": "Alignment Portal",
      "level": 5,
      "resonanceRank": 5,
      "school": "Conjuration",
      "schools": [
        "Conjuration"
      ],
      "placements": [
        {
          "name": "Alignment Portal",
          "school": "Conjuration",
          "level": 5,
          "summary": "Create a gateway to a plane aligned with your alignment."
        }
      ],
      "classLevels": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classRanks": {
        "Druid": 5,
        "Mage": 5,
        "Ranger": 5,
        "Shaman": 5,
        "Tinker": 5,
        "Wizard": 5
      },
      "classLearnLevels": {
        "Druid": 9,
        "Mage": 9,
        "Ranger": 17,
        "Shaman": 13,
        "Tinker": 18,
        "Wizard": 9
      },
      "classSchools": {
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
      "description": "Create a gateway to a plane aligned with your alignment.",
      "alternateSummaries": [],
      "classes": [
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
        "index": 167,
        "original": {
          "school": "Conjuration",
          "level": 5,
          "name": "Alignment Portal",
          "effect": "Create a gateway to a plane aligned with your alignment.",
          "source_paragraph": 9185,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Planar",
            "Alignment"
          ],
          "rp_cost": 10
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

**Current operative procedure**

Action; range 60 feet; V/S/F; base 10 RP; source Instantaneous metadata preserved. Preserve the printed effect: a genuine gateway to a plane compatible with the caster’s alignment. NEW finite completion: concentration up to 60 elapsed seconds and two fixed linked 5-foot-wide ×8-foot-high vertical apertures.

Before payment: (1) compute the caster’s current effective canonical nine-point alignment only when both axes are defined, applying underlying records/AP-AS-01 then AC4 Lock/Anchor snapshots under AC4-ALIGN-01; (2) choose a different actual destination `planeKey` and genuinely known `siteId`; (3) that plane/site record must carry Alignment-Portal compatibility for the effective alignment; (4) use AC5-PORTAL-GEOMETRY-04 to choose a perceived clear supported origin pose and the site’s already-recorded destination `portalPose`. Portal formation itself moves no body/object, so Dimensional Anchor is not a formation blocker. Mortal Wheel labels/rumor do not supply a plane/site mapping.

Successful resolution snapshots the compatibility alignment key and both aperture poses. Later alignment changes do not close the gate. Apertures remain fixed. The gateway is bidirectional while active. Ordinary sight may see through only where geometry permits, but the portal grants no cross-plane spell/attack/remote-sense line of effect; its permission is physical crossing.

Transport classification for this spell only: crossing is planar/extradimensional physical-gateway travel and is NOT teleportation. Therefore No Escape blocks a voluntary crossing; Verdict Absolute and Reign of Ashes do not. Forced movement can carry a body through only under AC5-PORTAL-GEOMETRY-04 and is not voluntary.

Crossing one aperture costs 5 feet base ordinary movement, modified by actual difficult terrain/crawling/squeezing. Large through the 5-foot aperture requires legal one-size-smaller squeeze and pays the real squeeze movement/penalties. Carried creatures are separate travelers; all bodies must fit/support and pass blockers. Use prospective arrival provenance from AC5-PLANAR-ARRIVAL-03 for destination Planar Protection before placement. At each crossing, revalidate the actual origin/destination body footprints, occupancy/support, current Dimensional Anchor and destination ward. A known Anchor-blocked crossing commits no movement; a live portal can remain present until its normal deadline. Known illegal crossing commits no 5-foot movement; legality changing after a legal crossing commitment yields atomic failure at origin with no split/bisection.

Successful transit commits `lastArrivedFromPlaneKey` to the actual origin planeKey only. Transit completed before deadline completes; at deadline no new crossing begins. Suppression makes apertures unusable without pausing deadline and never ejects a traveler. No return exists after closure, but while active either aperture can be used in either direction under the same real gates. No cosmological/native/soul/deity fact is inferred.

## Scope limits
These procedures do not select named cosmological identities, native-plane/soul provenance, deity identity, campaign era, runtime implementation, numerical balance, whole-game completion or publication status. Authoring examples are not executed tests.
