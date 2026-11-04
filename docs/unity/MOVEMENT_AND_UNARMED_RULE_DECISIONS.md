# Movement and ordinary unarmed completion policies

Status: **OWNER-ADOPTED PROVISIONAL PROTOTYPE POLICY**, 2026-11-03. Both decisions below were explicitly adopted. Existing sourced rules and earlier owner approvals remain in force; this is not release promotion.

Codex and [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206) agree that the following completions are coherent for the bounded prototype, but could not recover these precise policies from the inspected rules. GPT response `132991f7-2ede-53ad-9063-0b473ee73ba7` is preserved in [the review receipt](evidence/2026-11-03-movement-guidance/GPT_COMPLETION_PROPOSALS.json). Agreement is design guidance, not owner approval or release promotion.

## Decision 1: movement, opportunity attacks and Press

Adopted scope: the fixed-roster host's individual five-foot voluntary steps and ordinary opportunity attacks (OAs).

1. Capture every initially eligible ordinary OA reactor in existing encounter initiative order. Offer each controller the choice for its own creature, revalidating eligibility before the offer and accepted commitment. Do not add newly eligible reactors to this captured window. After the first offer, the mover cannot voluntarily cancel, change destination or substitute another movement mode. State changes may invalidate the step; discard remaining offers without spending unused Reactions. Already resolved attacks, dice, spent Reactions and consequences remain committed. After responses, revalidate permissions, occupancy, current Speed and remaining movement. Debit movement only when the announced step actually completes. With no eligible offers, complete directly after validation.
2. Press's retreat trigger requires a completed voluntary step from adjacent to no longer adjacent to the Press holder. A lateral step that remains adjacent does not qualify. Use actual before/after positions following pre-exit reactions; an interrupted departure creates no vacated-space trigger.
3. Validate a Press follow's destination, body permissions and separate five-foot movement-cost allowance before acceptance. Acceptance immediately consumes that regular-turn interval's follow entitlement. Its own pre-exit OA may prevent travel without refunding the entitlement. No travel means no physical distance, movement-cost debit or Mobile-distance consumption. A completed follow spends Press's separate allowance, never ordinary movement. Declining does not consume the entitlement.

Initiative priority here applies only to ordinary OA offers, not Ready, Interpose or other effect windows. Preserve existing application ordering for competing recorded Press effects. Every potentially eligible reactor must be represented; a nearby eligible creature outside the fixed roster is unsupported, not silently denied its OA.

Examples: an OA that knocks the mover unconscious leaves the attack and spent Reaction committed but spends no movement for the uncompleted step. An accepted Press interrupted in the same way still spends its one-follow entitlement. Moving around an enemy while remaining adjacent does not trigger that enemy's Press.

The source already supplies pre-exit ordinary OA, voluntary departure distinctions, movement costs and Press's separate allowance. Captured offer ordering, commitment/cancellation, the precise retreat predicate and interrupted Press entitlement handling above are **new provisional policy**. Exact movement guidance and source pointers are preserved in [the earlier review](evidence/2026-11-03-movement-guidance/GPT_GUIDANCE.json).

## Decision 2: ordinary unarmed damage classification and body use

Adopted ordinary profile: STR for attack and damage; before defenses, `max(0, 1 + STR modifier + applicable flat damage modifiers)` bludgeoning. Ordinary unarmed strikes count as melee weapon attacks for Aggressive and the ordinary ability-to-damage rule, while remaining attack options rather than held inventory weapons. This grants no proficiency, equipment properties, class features or other weapon-only riders.

A supported ordinary humanoid may strike with an actually usable fist, elbow, knee, foot or head. A free hand is unnecessary when another permitted striking body part is usable. Actual conditions and specific body restrictions still apply. This grants no anatomy, extra reach or permission for arbitrary transformed bodies.

The inspected V6 text supplies flat 1 bludgeoning, melee classification, ordinary five-foot reach, STR melee attacks and critical doubling of dice only. Flat damage has no die to roll or double. The Simple-melee training entry can receive proficiency from an actual covering grant; it does not grant everyone proficiency. Its later weapon-profile bridge is expressly limited to Weapon Focus and Weapon Mastery. Thus Aggressive applicability, the general ability-to-damage classification and body-use contract above are **new provisional completions**.

For the existing STR 10 numerical actors with no proficiency grant: an ordinary hit or critical deals 1 bludgeoning; an Aggressive hit or critical deals 3. The critical flag still matters to consequences such as damage at zero HP.

Primary pointers at inspected revision `4ba6b4ca095dc2f78323ca26198570812eaeef56`: `docs/reference/Player_Rulebook_v6_source_text.txt` lines 6776, 8177-8199 and 8229 onward; `DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/shared_rules.json` FS-02 `/rules/1/wording` (FAA-03); and `DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md`, first-class training. Their exact interpretation and limits are recorded in the review receipt above.

## Owner receipt

On 2026-11-03 the owner answered **Adopt the movement proposal** and **Adopt ordinary unarmed completion** to the two questions linking this full document. These receipts adopt both contracts above, including their stated scope and boundaries.

The owner then directed: **if you and gpt agree, then im good with it. You dont need to keep me informed of that.** Codex and the designated Unity Rules Engine Development chat may resolve subsequent rule gaps by consensus and record the exact resulting policy without repeated owner approval requests or agreement notifications. Ask the owner when the two agents cannot resolve a question together. Source-backed rules, new provisional decisions and actual runtime coverage remain separately labeled; this delegation does not promote content to release or change the C#-first development phase.

## Delegated completion: choosing whether a hit arms or replaces Press

The inspected combat procedure says that a later qualifying hit **may replace** an unconsumed Press target. Its reviewed clarification also permits declining the first arming. Schema11 therefore accepts the attacker's controller's `PressHitInstruction`: `ArmOrReplace` (the command default) or `KeepExisting`. The latter preserves the current record and its application-order identity, including an empty state. Misses, nonqualifying attacks and a consumed entitlement leave Press unchanged. Neither instruction grants a new entitlement or extends an existing endpoint.

For this bounded host, the controller submits this conditional instruction with the attack before dice are drawn. **That decision timing is a new provisional consensus policy**, not recovered source text. The selector is retained in command identity, receipts and the immutable attack record, including a pending knockout; the knockout response cannot change it. This applies to a qualifying own-turn OA as well as an ordinary Action attack. It does not authorize Press arming during another creature's regular turn.

Codex and Unity Rules Engine Development agreed under the owner's delegation; GPT response `249a8594-5278-52a1-9246-bd8e44f1e896` is preserved in [the decision review](evidence/2026-11-03-movement-guidance/GPT_PRESS_CHOICE.json). The exact combat source and reviewed clarification are included in the schema11 source bindings. Legacy schemas9/10 retain their existing command/codec contract; this increment introduces no implicit migration.

The [integration review](evidence/2026-11-03-movement-guidance/GPT_TACTICAL_INTEGRATION.json) separately confirms source interpretations: Focused prohibits ordinary reactions immediately; Mobile counts actual travel, including completed Press follows; own regular Start refreshes Reaction; and finite consumed Press entitlements bound nested follows. These interpretations are not additional owner balance proposals.
