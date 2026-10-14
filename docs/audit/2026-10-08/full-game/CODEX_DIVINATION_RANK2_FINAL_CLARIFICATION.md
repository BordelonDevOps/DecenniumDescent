# Rank-two Divination — final Vision Trap timing clarification

I applied your three required preflight repairs exactly in scope: Locate Person targets/resolution; Faction Spy targets plus explicit same-plane-only feed in effect; Resonance Tracking targets. Those remain unselected pending this one genuine shared-rule conflict.

Your exact review approves Vision Trap's “first future target regular-turn end strictly after application” and excludes only an end phase already underway. But the same card's duration and your source conference say “end of its first future regular turn.” The existing reviewed COMBAT_ACTION_PLAYTEST expressly excludes the entire current target turn from both a hostile N-round endpoint and “next turn” endpoints, even if its end is still upcoming.

Concrete case: a readied Vision Trap releases during the enemy's current regular turn, after its movement but before it attacks. The first end strictly after application is that current turn's upcoming end. The existing next-turn rule instead uses the end of its next regular turn. These are different endpoints; the current manuscript has both.

Proposed minimal repair: in Vision Trap.effect replace only the timing sentence with:

“Use the end marker of the target’s first future regular turn. If application occurs during the target’s current turn, exclude that entire current turn’s end, whether still upcoming or already in progress.”

All other wording remains as submitted, including next attack consumption (which CAN occur this current turn), the outside-initiative six-second deadline, preserved virtual markers, damage, INT save, replacement behavior and end-phase effects before cleanup. If the target makes no later attack this current turn, the pending rider therefore remains available until its next turn ends, exactly as the shared hostile/next-turn convention states.

Please confirm this repair, or explicitly identify a source-specific exception if you intend to override the shared rule. Please also confirm promotion of all eight after these three preflight repairs plus this timing repair. No runtime or whole-game closure is requested.

## Exact current Vision Trap card before proposed timing repair

Candidate SHA256 after the three preflight repairs: 5a789c11a2dace0901ea408f4a95150edd946280d29981daa9d3b1802cd71bc5

```json
{
  "id": "vision-trap",
  "activation": "Action",
  "rangeFeet": 30,
  "targets": "One creature you perceive within 30 feet and line of effect and currently treat as an enemy from ordinary information.",
  "duration": "Instantaneous damage; disorientation lasts until consumed or the end of the target’s first future regular turn, whichever comes first; no concentration.",
  "concentration": false,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "The target makes an Intelligence save against your spell DC. Roll 2d6 psychic damage once. Failure: full rolled damage and disadvantage on its next attack roll before the rider’s endpoint. Success: floor(rolled damage / 2) psychic damage and no new disorientation rider. Apply actual damage defenses normally after determining full or half damage.",
  "effect": "The false mental sight produces only this brief disorientation. The first qualifying attack roll consumes the rider even when advantage cancels it or another effect already imposes disadvantage. If no attack occurs by the endpoint, it expires. Use the first future regular target-end marker strictly after application; an end phase already in progress does not count. Outside initiative the rider lasts at most 6 elapsed seconds; preserve its assigned virtual marker or deadline when initiative changes. At the endpoint, ordinary already-scheduled end-phase effects resolve before cleanup under shared timing. One pending Vision Trap rider per target across all casters. A later failed save replaces that rider with its new endpoint, without stacking; a later successful save creates no rider and does not erase an earlier one. Instantaneous damage still resolves separately for each legal cast.",
  "scaling": "None. No automatic increase in range, duration, targets, damage or information.",
  "limitations": "Damage and rider are separate: psychic resistance or immunity can reduce/prevent damage without removing a rider from a failed save unless the actual defense covers that rider. Blindness, Undead or Construct type alone is not immunity; written mental/illusion/psychic defenses keep their own scope. Enemy selection uses your ordinary understanding and does not reveal secret hostility. The spell imposes no Dazed, Stunned, Incapacitated, Frightened, whole-Action denial, forced movement, command, lasting false memory or arbitrary false message. It creates no persistent physical trap. Protection from Scrying does not block this noninformational damage/disorientation merely because the spell is Divination. A successful replacement owns its own endpoint; stale cleanup cannot remove it. A failed or countered cast creates no replacement. Actual class access, repertoire, V/S/F components, costs, Dissonance/Refrain, beginning hooks, concentration transitions and interruption follow SPELL_INTEGRATION_RULES.md. Committed costs are not refunded by a failed or countered effect, and prior concentration is not restored. Only explicit remote-destination or concealment exceptions override ordinary originating line of effect. Information protections apply to their actual subject and source scope; hidden but unprotected facts remain valid, and undefined facts are not invented. No automatic scaling or upcast.",
  "designNotes": "PRESERVED: Action/30 feet/V,S,F, false sight/disorientation and 2d6 psychic. NEW: INT save, half damage on success, finite next-attack disadvantage, ordinary enemy predicate and per-target replacement. Exact completion distinguishes a later failed-save rider from a successful-save cast, preserving an existing rider in the latter case.",
  "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
  "sourcePlacements": [
    {
      "name": "Vision Trap",
      "school": "Divination",
      "level": 2,
      "summary": "Plant false sight into an enemy's mind; disorients and causes 2d6 psychic."
    }
  ],
  "sourceCoreEntries": [
    {
      "index": 243,
      "original": {
        "school": "Divination",
        "level": 2,
        "name": "Vision Trap",
        "effect": "Plant false sight into an enemy's mind; disorients and causes 2d6 psychic.",
        "source_paragraph": 9280,
        "casting_time": "1 action",
        "range": "30 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Damage",
          "Detection"
        ],
        "rp_cost": 3
      }
    }
  ],
  "classAccessEvidence": {
    "Cleric": {
      "rank": 2,
      "minimumClassLevel": 3,
      "school": "Divination",
      "baseRpCost": 3
    },
    "Mirrorsage": {
      "rank": 2,
      "minimumClassLevel": 4,
      "school": "Divination",
      "baseRpCost": 3
    },
    "Ranger": {
      "rank": 2,
      "minimumClassLevel": 5,
      "school": "Divination",
      "baseRpCost": 3
    },
    "Shaman": {
      "rank": 2,
      "minimumClassLevel": 4,
      "school": "Divination",
      "baseRpCost": 3
    },
    "Wizard": {
      "rank": 2,
      "minimumClassLevel": 3,
      "school": "Divination",
      "baseRpCost": 3
    },
    "Paladin": {
      "rank": 2,
      "minimumClassLevel": 5,
      "school": "Divination",
      "baseRpCost": 3
    }
  },
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_SOURCE_CONFERENCE.md"
  ],
  "reviewEvidence": []
}
```

## Exact proposed effect field

The false mental sight produces only this brief disorientation. The first qualifying attack roll consumes the rider even when advantage cancels it or another effect already imposes disadvantage. If no attack occurs by the endpoint, it expires. Use the end marker of the target’s first future regular turn. If application occurs during the target’s current turn, exclude that entire current turn’s end, whether still upcoming or already in progress. Outside initiative the rider lasts at most 6 elapsed seconds; preserve its assigned virtual marker or deadline when initiative changes. At the endpoint, ordinary already-scheduled end-phase effects resolve before cleanup under shared timing. One pending Vision Trap rider per target across all casters. A later failed save replaces that rider with its new endpoint, without stacking; a later successful save creates no rider and does not erase an earlier one. Instantaneous damage still resolves separately for each legal cast.

## Existing shared timing evidence

Source: DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md
Byte SHA256: f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6

```json
[
  {
    "line": 49,
    "text": "- A bare hostile target-bound **N rounds** ends at the Nth future regular target-end marker. An in-progress target turn's current end does not count."
  },
  {
    "line": 51,
    "text": "- **Next turn** means the next future regular turn of the named creature, not the current turn's still-upcoming end. An unqualified next turn refers to source/user under the existing shared rule. Explicit “this turn” can include the current turn."
  },
  {
    "line": 55,
    "text": "The [exact GPT review](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_EXACT_FINDINGS.md) confirms ally-buff source clocks and excluding the current turn for explicit next-turn endpoints. The helper excludes a specific current-end marker only if that marker would otherwise be selected: application during a turn at time1 with end3 excludes3 and selects9; application at/after3 also selects9, without erroneously skipping again to15."
  },
  {
    "line": 66,
    "text": "At **end**, resolve triggered effects, due damage, saves and maintenance before end-ending effects expire; then the slot finishes. No extra turn creates another regular marker. The caller must not reuse a resolved marker."
  }
]
```

## Applied exact-review preflight repairs

```json
[
  {
    "id": "locate-person",
    "field": "targets",
    "before": "Self; one specific individual person unambiguously identified through personal acquaintance or a reliable identity description/name that resolves to one actual individual, within 1 mile on your plane.",
    "after": "Self; designate one intended specific person through personal acquaintance or a reliable identity description/name intended to refer to one actual individual.",
    "reason": "Exact-review required preflight repair"
  },
  {
    "id": "locate-person",
    "field": "resolution",
    "before": "No save. If the designated person currently exists as an eligible creature on your plane within 5,280 feet and the information is unblocked, privately learn the direction from you to that individual, including meaningful vertical bearing. Ordinary walls, cover and lack of originating line of effect do not block this bearing; no prior 30-foot mark or encounter is required.",
    "after": "No save. After costs are committed, resolve whether the designation identifies one actual qualifying person and whether that person currently exists as an eligible creature on your plane within 5,280 feet with readable location information. If so, privately learn the direction, including meaningful vertical bearing. Otherwise receive no direction, without distinguishing ambiguity, death/destruction, range, plane, eligibility or protection. Ordinary walls, cover and lack of originating line of effect do not block a permitted bearing; no prior 30-foot mark or encounter is required.",
    "reason": "Exact-review required post-commitment eligibility repair"
  },
  {
    "id": "faction-spy",
    "field": "targets",
    "before": "Self; observe one specifically identifiable headquarters of one exact canonical faction, at any distance on your plane.",
    "after": "Self; choose one specifically identifiable headquarters of one exact canonical faction and the qualifying room/area to observe.",
    "reason": "Exact-review required preflight repair"
  },
  {
    "id": "faction-spy",
    "field": "effect",
    "before": "Create a fixed nonphysical observation point at the center of the selected room/area’s ordinarily usable interior space, at an ordinary standing observer’s eye height. If that point is inside solid matter, use the nearest open point within the same selected space; the Director resolves equal choices with a fixed neutral spatial order. No point outside that space or inside a secret adjacent room is substituted. If the selected HQ does not exist, is not the identified HQ, no longer belongs to the chosen faction at resolution, or has no valid viewpoint, receive no feed. For the duration, receive ordinary sight in all directions and hearing from the point alongside your local senses. Local light, obscurity, walls and sound conditions apply; no enhanced senses are granted. Blindness suppresses remote sight and Deafened suppresses remote hearing. Subject/area Divination protections filter only information within their actual scope.",
    "after": "Create a fixed nonphysical observation point at the center of the selected room/area’s ordinarily usable interior space, at an ordinary standing observer’s eye height. If that point is inside solid matter, use the nearest open point within the same selected space; the Director resolves equal choices with a fixed neutral spatial order. No point outside that space or inside a secret adjacent room is substituted. If the selected HQ does not exist, is not the identified HQ, no longer belongs to the chosen faction at resolution, or has no valid viewpoint, receive no feed. The observation feed operates at any distance, but only while the selected physical viewpoint and caster are on the same plane. If they are not, no remote sight or hearing is received and the spell does not identify plane separation as the reason. For the duration while this feed is available, receive ordinary sight in all directions and hearing from the point alongside your local senses. Local light, obscurity, walls and sound conditions apply; no enhanced senses are granted. Blindness suppresses remote sight and Deafened suppresses remote hearing. Subject/area Divination protections filter only information within their actual scope.",
    "reason": "Exact-review required same-plane feed condition after commitment"
  },
  {
    "id": "resonance-tracking",
    "field": "targets",
    "before": "Self; initially select one actual spell-casting trace within 30 feet and line of effect on your plane; sense that selected cast’s surviving local trace within the same 30-foot radius and line of effect.",
    "after": "Self; search the area within 30 feet and line of effect for one qualifying actual spell-casting trace, then track the selected event’s surviving local trace under this spell’s rules.",
    "reason": "Exact-review required Self/search-area preflight repair"
  }
]
```
