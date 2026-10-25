# Maximum HP, stat changes and HP thresholds

**REVIEWED / reference-VALIDATED —58 exact passages:51 class records and7 feats.** The [source register](MAXIMUM_HP_SOURCE_BINDINGS.md) preserves the original procedures; [source validation](MAXIMUM_HP_SOURCE_VALIDATION.json) verifies equality and hashes. The [first captured notebook reply](../../../../docs/audit/2026-10-08/full-game/GPT_MAXIMUM_HP_FIRST_REVIEW_PARTIAL.md) is incomplete and must be read with the [complete tail and boundary corrections](../../../../docs/audit/2026-10-08/full-game/GPT_MAXIMUM_HP_BOUNDARIES.md) and [exact implementation closure](../../../../docs/audit/2026-10-08/full-game/GPT_MAXIMUM_HP_FINAL_CLOSURE.md).

These rules cover the maximum-HP and threshold components supplied here. They do not promote whole feats, create companion actions, decide character advancement, or certify every monster/item/spell maximum-HP modifier.

## Recompute capacity from separate records

Keep base maximum, bonuses, reductions and systemic multipliers separate. Base maximum excludes all modifiers represented separately in this ledger. Never feed a previously modified maximum back into the formula.

First calculate the otherwise-applicable maximum:

    preSystemicMaximum = max(1, baseMaximum + compatibleBonuses − strongestMonkTrauma)

Then apply the reviewed systemic factors against that same value:

    effectiveMaximum = max(1, floor(preSystemicMaximum × systemicFactors))

Expedition Strain4+ contributes3/4 and Exhaustion4+ contributes1/2. Multiply compatible rational factors before rounding once. Base101, Flesh Warden+20, Monk trauma−9 and both factors produce42. Suppressing that trauma produces45; do not subtract the trauma again afterward.

The numerical modifier calculation does not perform lethal-track transitions. Use the separate reviewed life-state procedure when a track actually changes. Merely recomputing maximum HP must not re-kill a living collapsed survivor at track6.

Each application retains its own ID, source, owner, target, magnitude, start/end markers, presence and suppression state, arbitration group and any acquisition/creation snapshot needed for its formula. Keep records even when another stronger application wins. Suppression does not stop clocks.

## Bonuses and source identities

| Source | Bonus and update rule |
|---|---|
| Flesh Warden | +2 per Warrior level while legally equipped; capacity only |
| Wizard Conjuration specialization | +Wizard level captured when that Wizard spell creates the summon |
| Flesh Ascendant | +2 per current Wizard level of the eligible controller supplying the feature |
| Familiar Bond | Provisional +current eligible owner's character level to familiar maximum HP |
| Tenacity | +current character level |
| Tough | +twice character level when the feat was acquired; retain this snapshot |
| Tough as Nails | +2 per character level at acquisition, then +2 for each later level |
| Dark Fortitude | +2 per current character level |

**New feat integration:** distinct feat identities granting maximum HP add together unless an explicit source says otherwise. Duplicate copies of the same feat do not add. Their original acquisition/prerequisite, retraining and other-effect rules still need their separate review.

**New Wizard-specific stacking exception:** Conjuration and Flesh Ascendant add when the same undead summon qualifies for both, overriding the frozen strongest same-stat class-technique bonus default for this pair only. Flesh Ascendant's engine[24] and named card describe one modifier identity; do not count both.

When later companion lifecycle code constructs records, the engine/card aliases must share one actual effect identity, including suppression and removal. Numerical non-stacking alone must not leave a second textual alias operative after that effect is suppressed.

Conjuration's amount and caster provenance stay tied to creation. A later caster level or controller change does not recompute that snapshot. Flesh Ascendant instead follows the current eligible controller; changing control ends the old controller's eligibility and can create the new controller's eligible bonus, without healing.

**New Familiar Bond interpretation:** its ambiguous “gains hit points” wording supplies maximum capacity. Initial creation under that bonus can include it in starting HP; later level increases add capacity only. Familiar ownership/replacement and attack/command rules remain in the future companion package.

When a creature is initially created, construct its starting state from its final creation maximum unless its source expressly enters it damaged. Base20 plus Conjuration10 plus Flesh Ascendant20 gives50/50 at creation. Acquiring either bonus later does not fill missing HP. No bonus changes creature or command caps.

## Monk trauma uses one global strongest reduction

**Explicit correction of the earlier per-owner proposal:** Monk engine[9]'s categorical non-stacking clause controls. Use the largest currently operative Monk maximum-HP reduction on the target across all owners.

Ribcrusher applies S+M, Bone-Breaking Strike2S+M, and Deathless Silence4S+M. Preserve each successful application separately, including repeated applications of the same card. Do not combine the strongest magnitude with another record's longer duration. If−9 is suppressed, an operative−5 can become effective; when−5 expires, it stops contributing even while−9 remains suppressed.

Default Monk trauma ends when the target completes a short or long rest. This is effect removal, independent of how many numerical rest rewards the target already earned. Interrupted rest ends none. A genuinely explicit earlier/different endpoint controls its own record; the existence of an endpoint parameter does not grant permission to invent one.

Deathless Silence has three independent components: the Monk's protection from Reactions/opportunity attacks through source-next-regular-start; target defensive-passive suppression through that target's next-turn end; and maximum-HP trauma through the target's completed rest. Preserve the already reviewed control clocks.

## Capacity changes are not HP damage or healing

After any maximum change, clamp current normal HP down only if it exceeds the new maximum. Adding/restoring maximum HP gives no current HP. This clamp is not damage, sacrifice or healing; it creates no Wound save, death-save failure, resource trigger, redirection or first-fall event. Decay does not prevent capacity restoration.

Temporary HP is independent and remains unchanged. Maximum reduced to10 does not remove an existing25 temporary HP.

Dead, Stable and dying0 creatures retain their life state, counters and Stable deadline. A minimum maximum of1 never revives a corpse. Critical's healing ceiling recomputes afterward as max(1,effectiveMaximum−1); it is not another maximum-HP reduction.

## Exact thresholds and recorded events

Use effective maximum and integer comparison, without rounding a percentage threshold first:

| Wording | Comparison |
|---|---|
| At/below one-quarter | 4×HP ≤ maximum |
| Below one-quarter | 4×HP < maximum |
| At/below half | 2×HP ≤ maximum |
| Below half | 2×HP < maximum |
| Above half | 2×HP > maximum |

Continuous predicates update whenever HP or maximum changes: Wyrmhide, Brutality Sense, Pain Empowerment, Dark Fortitude's poison resistance, Life Drinker's conditional damage, and “below maximum” regeneration eligibility. Pain Empowerment uses full10% missing-HP bands, capped at+5, at its printed pre-roll moment.

**New first-fall interpretation:** Anointed Guardian, Burning Blood IV, Death's Threshold and Adrenal Floodgate require a genuine downward crossing. At/below-quarter triggers require HP moving from above quarter to at/below quarter. Burning Blood IV requires moving from at/above half to strictly below half. Actual damage or direct HP loss can establish a crossing unless a source specifically restricts it to damage. Capacity changes and clamps cannot.

If a rest refreshes a first-fall use while its subject is already below the threshold, neither the refresh nor another1HP loss fires it. The subject must return to the non-trigger side and cross again. Source frequency/history remains a separate eligibility gate; a crossing alone grants no new use.

Death's Threshold's exit requires actual HP restoration leaving the creature above half. A maximum reduction that makes unchanged HP above half does not end it. A later actual heal can satisfy that exit even if the creature was already above half before that heal.

**New continuous duration interpretation:** Mythic Carapace and Butcherform Chassis end when active and strictly below quarter. A maximum increase can therefore end them without damage. Exact quarter remains legal. Other duration endpoints still apply.

Record pre/post normal HP and the event-effective maximum for historical checks. Rewind Wound uses the maximum stored with its referenced damage event, never a later maximum. Freeze same-event HP crossings before a later stat clamp.

Rewind Wound requires genuine damage causing actual normal-HP decrease and leaving the target below half; it does not require a first crossing. HP40→30 at maximum100 qualifies even though both values are below half. An event entirely absorbed by temporary HP does not qualify.

Selection/rider timing follows each card: Mass Healing Light when its target is chosen; Merciful Sacrament at initial activation; Flesh to Ash before rolling damage; Death Touch at strike start; Blessing of the Meek/ Verdant Pulse before healing; Final Verdict at legal targeting; Fearbrand/Malicious Execution before their damage/rider; Echo Strike after its copied damage. Brutality Progress's already reviewed snapshot rules remain unchanged.

## Percentage recovery and damage

Use effective maximum when the amount resolves unless the source explicitly references an earlier snapshot. Floor the percentage amount, with minimum1 only where printed or already supplied by the reviewed viable-resurrection bridge.

Wound Eater III can heal0 at maximum3. Spiral III and False Life V explicitly retain minimum1 for quarter recovery. Unyielding Light uses one third with minimum1. Divine Rebirth uses the reviewed viable-return max(1,floor(maximum/2)). Wound Eater V's quarter target-HP loss and half self-heal cap retain their direct-loss classification. Ledger Unbound caps its raw damage at a quarter of target maximum before its save-halving.

Repair Pulse and Snap Rebuild use half device maximum under their own functional/destroyed target rules. A tiny-maximum reconstruction's viability belongs to the device lifecycle and is not silently converted into a general minimum1 here.

## Attack damage before Monk trauma

**New integration for the supplied Monk trauma cards:** choose/pay an after-hit option at its legal hit window. Resolve the ordinary attack's damage, Wounds, Instant Death and any survival replacement against the pre-trauma maximum; freeze its metrics. If the target remains an eligible living creature, resolve the trauma CON save using its then-current save modifier, including applicable Wound consequences. On failure, create the trauma record and recompute capacity.

If the attack leaves the target Dead, no combat-trauma record is needed and the paid cost is not refunded. A legal same-resolution death replacement preserving life can leave the target eligible.

Example: maximum30, HP30; damage4 leaves26 and records4 actual damage. A later−15 maximum reduction gives maximum15 and clamps current HP26→15. The11-point clamp causes no second damage/Wound/threshold event and cannot rewrite the attack's Instant Death threshold or concentration packet.

## Validation and remaining scope

The current reference passes60 targeted checks and909 systemic parity states. It accepts already legal source records and event snapshots; it does not decide source acquisition, perform companion creation, pay Ki, schedule turns or consume first-fall uses.

Still open: unsupplied item/spell/monster/disease/curse maximum modifiers; non-Monk reductions; exceptions applying after systemic multipliers; full feat acquisition/retraining; familiar and summon/control lifecycle; unusual device reconstruction; human balance. The58-source discussion does not close these larger domains.
