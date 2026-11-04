# Movement and ordinary unarmed completion proposals

Status: **PROPOSED, NOT ADOPTED**. These are two separate owner decisions. Existing sourced rules and earlier owner approvals remain in force. No implementation may treat silence as adoption.

Codex and [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206) agree that the following completions are coherent for the bounded prototype, but could not recover these precise policies from the inspected rules. GPT response `132991f7-2ede-53ad-9063-0b473ee73ba7` is preserved in [the review receipt](evidence/2026-11-03-movement-guidance/GPT_COMPLETION_PROPOSALS.json). Agreement is design guidance, not owner approval or release promotion.

## Decision 1: movement, opportunity attacks and Press

Proposed scope: the fixed-roster host's individual five-foot voluntary steps and ordinary opportunity attacks (OAs).

1. Capture every initially eligible ordinary OA reactor in existing encounter initiative order. Offer each controller the choice for its own creature, revalidating eligibility before the offer and accepted commitment. Do not add newly eligible reactors to this captured window. After the first offer, the mover cannot voluntarily cancel, change destination or substitute another movement mode. State changes may invalidate the step; discard remaining offers without spending unused Reactions. Already resolved attacks, dice, spent Reactions and consequences remain committed. After responses, revalidate permissions, occupancy, current Speed and remaining movement. Debit movement only when the announced step actually completes. With no eligible offers, complete directly after validation.
2. Press's retreat trigger requires a completed voluntary step from adjacent to no longer adjacent to the Press holder. A lateral step that remains adjacent does not qualify. Use actual before/after positions following pre-exit reactions; an interrupted departure creates no vacated-space trigger.
3. Validate a Press follow's destination, body permissions and separate five-foot movement-cost allowance before acceptance. Acceptance immediately consumes that regular-turn interval's follow entitlement. Its own pre-exit OA may prevent travel without refunding the entitlement. No travel means no physical distance, movement-cost debit or Mobile-distance consumption. A completed follow spends Press's separate allowance, never ordinary movement. Declining does not consume the entitlement.

Initiative priority here applies only to ordinary OA offers, not Ready, Interpose or other effect windows. Preserve existing application ordering for competing recorded Press effects. Every potentially eligible reactor must be represented; a nearby eligible creature outside the fixed roster is unsupported, not silently denied its OA.

Examples: an OA that knocks the mover unconscious leaves the attack and spent Reaction committed but spends no movement for the uncompleted step. An accepted Press interrupted in the same way still spends its one-follow entitlement. Moving around an enemy while remaining adjacent does not trigger that enemy's Press.

The source already supplies pre-exit ordinary OA, voluntary departure distinctions, movement costs and Press's separate allowance. Captured offer ordering, commitment/cancellation, the precise retreat predicate and interrupted Press entitlement handling above are **new provisional policy**. Exact movement guidance and source pointers are preserved in [the earlier review](evidence/2026-11-03-movement-guidance/GPT_GUIDANCE.json).

## Decision 2: ordinary unarmed damage classification and body use

Proposed ordinary profile: STR for attack and damage; before defenses, `max(0, 1 + STR modifier + applicable flat damage modifiers)` bludgeoning. Ordinary unarmed strikes count as melee weapon attacks for Aggressive and the ordinary ability-to-damage rule, while remaining attack options rather than held inventory weapons. This grants no proficiency, equipment properties, class features or other weapon-only riders.

A supported ordinary humanoid may strike with an actually usable fist, elbow, knee, foot or head. A free hand is unnecessary when another permitted striking body part is usable. Actual conditions and specific body restrictions still apply. This grants no anatomy, extra reach or permission for arbitrary transformed bodies.

The inspected V6 text supplies flat 1 bludgeoning, melee classification, ordinary five-foot reach, STR melee attacks and critical doubling of dice only. Flat damage has no die to roll or double. The Simple-melee training entry can receive proficiency from an actual covering grant; it does not grant everyone proficiency. Its later weapon-profile bridge is expressly limited to Weapon Focus and Weapon Mastery. Thus Aggressive applicability, the general ability-to-damage classification and body-use contract above are **new provisional completions**.

For the existing STR 10 numerical actors with no proficiency grant: an ordinary hit or critical deals 1 bludgeoning; an Aggressive hit or critical deals 3. The critical flag still matters to consequences such as damage at zero HP.

Primary pointers at inspected revision `4ba6b4ca095dc2f78323ca26198570812eaeef56`: `docs/reference/Player_Rulebook_v6_source_text.txt` lines 6776, 8177-8199 and 8229 onward; `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/shared_rules.json` FS-02 `/rules/1/wording` (FAA-03); and `DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md`, first-class training. Their exact interpretation and limits are recorded in the review receipt above.

## Owner receipt

Pending. Neither proposal has been adopted as of this document's creation.
