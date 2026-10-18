# Damage sharing, prevention and interception

**REVIEWED / reference-VALIDATED —39 exact source passages and two supporting Tinker engine passages.** [Final notebook review](../../../../docs/audit/2026-10-08/full-game/GPT_REDIRECTION_FINAL_CLOSURE.md) closes this bounded damage-sharing interface with94 checks and186 conservation states. It does not establish every item/spell defense, companion lifecycle, all-source attack chain or numerical balance. Original source cards remain unchanged.

Read the [source register](REDIRECTION_SOURCE_BINDINGS.md), [source checks](REDIRECTION_SOURCE_VALIDATION.json), [reference checks](REDIRECTION_PLAYTEST_VALIDATION.json), [first notebook proposal](../../../../docs/audit/2026-10-08/full-game/GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md) and [complete corrections](../../../../docs/audit/2026-10-08/full-game/GPT_REDIRECTION_BOUNDARIES.md). Later corrections supersede the retained first proposal.

## Resolve the kind of protection first

Guardian Pulse changes the target of an attack before comparing its original roll with AC. The Guardian becomes the actual hit/miss and on-hit-rider target. One attack can be retargeted once. Multiple offers are chosen by the original intended target; only the selected Guardian spends its Reaction/use. After the incoming attack fully resolves, a surviving, eligible Guardian may make the printed counterattack against an attacker in reach whether the original attack hit or missed. This free attack cannot grant another free attack or Action. Retargeting does not spend the later damage-transfer opportunity.

Bloodbond and Veinlock Tether divide the finalized raw damage before either recipient's mitigation. Attack/save success, save-halving and critical dice have already determined that amount. Bloodbond transfers one quarter, rounded down; Veinlock instead chooses up to S+M. Each recipient applies its own eligible defenses once to its own share.

Other supplied damage transfers divide damage after the original target's defenses and legal pure prevention, before temporary HP. Their transferred portions keep damage type and skip another DR/resistance/immunity/prevention stage. Temporary HP, applicable HP floors, would-die replacements, Wounds, concentration and ordinary life consequences still apply. “Unmitigated damage” does not mean “death cannot be prevented.”

Pure prevention removes damage without creating a second recipient. Elemental Absorption adds its resistance during ordinary defenses. Aura of Bonds and Crown reductions use the strongest applicable class flat reduction, then resistance/immunity. Finite/reactive prevention such as Bloom and Ancestral Guardian follows those defenses before post-defense transfer and temporary HP. Verify additional item/spell sources before treating this as universal defense ordering.

Redirecting Palm prevents half the Monk's post-defense damage, rounded down. The Monk keeps the remainder. A second enemy distinct from the triggering melee attacker, within5feet, can receive new force damage equal to the prevented amount, capped at Monk level. That new damage gets its own defenses; it is not a transferred attack or critical hit. With no second enemy, the Monk still receives the reduction.

Direct HP payments from Blood Sacrifice, Flesh-to-RP, Profane Exchange and Channel Life stay outside the damage sequence. They bypass temporary HP, obey their own legal minimum HP and do not create damage/Wound/resource triggers from paying the cost. Healing-recipient substitution and excess-healing conversion also remain distinct operations.

## One transfer operation and exact amounts

A root here means one original recipient's damage packet. A shared area cast has a separate root for each original recipient, under the same cast/roll identity.

One such root accepts one damage-sharing operation across all owners. A pre-mitigation split locks both its retained original portion and transferred portions against later transfer. Burden Shared can divide one operation among up to two other explicitly willing recipients. It does not create two redirection events. No transferred recipient may be the original damage target.

**New stage-precedence integration:** consider pre-mitigation offers before applying defenses, and post-defense offers afterward. Within the same stage, select eligible positive mandatory/automatic protection before optional offers; competing mandatory claims are chosen by the original damage target. A legally chosen Bloodbond/Veinlock operation can therefore preempt later Aegis/Final Stand because that root is already claimed. Do not preview or consume defenses/Bloom to decide a later-stage preference. The helper accepts an already selected legal operation; it does not select Reactions or schedule automatic offers.

Optional transfer requires a positive chosen amount and available damage. Zero transfer cannot spend an optional Reaction/resource/use. A mandatory rounded-zero share does nothing and spends no transfer allowance. An independently legal prevention component can still occur.

| Source | Transferred amount |
|---|---|
| Bloodbond | floor(raw damage/4), fixed |
| Veinlock Tether / Shared Breath / Selfless Guardian | chosen up to S+M |
| Protective Stance / Emergency Protocols | min(S+M, available damage), fixed |
| Life Linked | chosen up to floor(available damage/2) |
| Guardian Tissue | floor(available damage/3), fixed |
| Aegis Incarnate / Martyr's Share | floor(available damage/2), fixed |
| Chainbound Smite | chosen up to max(3, actual CHA modifier) |
| Linked Ward | chosen up to max(2, twice actual CHA modifier) |
| King's Smite protection | chosen up to5 |
| Aura of the Crown | chosen up to M |
| Crown of Embers / Burden Shared | chosen up to level+M |
| Crown Undying | chosen up to remaining level+M round allowance |
| Final Stand | all available damage, subject to shared allowance |

Every amount is capped by the available packet at its source's stage. Fixed fractions/fixed protection cannot voluntarily choose a smaller amount. Original actions, range, willingness, costs, active-state requirements, cadence and source-specific use limits still apply.

## Hit identity and final damage accounting

The original damage target retains its original hit, failed-save, critical and on-hit-rider identity even if all damage is transferred. A rider that requires positive damage must recheck the actual remaining packet. A transferred recipient was not hit by that attack and did not fail its save; it receives no attached poison/control/maiming/knockout rider merely because damage moved.

Accordingly, transferred damage from a critical attack gives an already0HP recipient the ordinary one damage failure, not two critical-hit failures. Concentration still sees the transferred recipient's resolved packet even if temporary HP absorbs all of it.

Use the [reviewed life-state interface](HEALING_DEATH_PLAYTEST.md) after resolving each final recipient. Numeric actual damage is temporary HP absorbed plus actual normal HP lost, excluding overkill and damage prevented by an HP floor. Sum each terminal recipient once. Do not also count the unsplit parent or unrelated counterdamage.

Physical root totals include every recipient. A healing/resource/reflection consumer sums only branches permitted for that consumer and qualifying for its own source's target predicate. For example, a meaningful-hostile-only drain does not automatically count damage transferred onto a friendly protector. Check all applicable flags for a compound trigger, such as a passive healing proc.

## Source-specific restrictions

All transfers prohibit another transfer. All supplied post-defense transfers prohibit another mitigation/prevention stage. Further restrictions differ:

| Source family | Additional restrictions on transferred damage |
|---|---|
| Paladin engine | No reflection or resource generation; does not universally prohibit other retaliation or healing |
| Protective Stance | Also no generic damage-trigger chains |
| Burden Shared | Also no derived healing |
| Oracle Life Linked | No reflection, resource/RC, passive, condition, action or copy generation; no recovery or retaliation |
| Guardian Tissue / Aegis | No BT generation; no invented ban on every other resource |
| Shared Breath | No additional generic trigger prohibition |
| Selfless Guardian / Emergency Protocols | No retaliation chain |
| Bloodbond / Veinlock | Each recipient still has its one defense stage; no additional blanket prohibition |

A no-derived-healing flag does not prevent unrelated later healing of the recipient.

The source's explicit redirection riders remain narrowly available. Unbroken Covenant triggers on the redirection operation, even when Protective Stance prohibits generic damage triggers; use half the final protector actual damage, capped at S+M. These self-absorption riders require damage actually transferred to the redirecting owner, not to another ally under Burden Shared. Linked Ward's own transfer granting temporary HP on reducing the Paladin to0 uses final actual damage, capped at level+M. Final Stand also gives the protected ally temporary HP equal to Paladin level and resistance to all damage through that ally's next turn end; the numeric helper handles only temporary HP, and the caller must create the resistance record. None grants a generic permission to ignore other source restrictions. Temporary HP still uses the larger remaining amount and does not stack.

## Paladin round ledger

Track each Paladin owner's numbered-round events. Ordinarily, one redirection event is available, using exactly one Paladin redirection feature. Final Stand is automatic on the first eligible positive post-defense packet while its allowance remains; the Paladin cannot save it for a later hit. Its “all damage” text does not override the explicit engine ceiling. It may redirect again in a later numbered round if still active before its source-next-start deadline.

Crown Undying can raise the owner's total to two different damage events, with at most one ordinary/non-Crown feature. The additional permission belongs to Crown Undying. A prior ordinary redirection remains recorded if Crown activates later in the same round; only one further Crown event is then possible. Reapplication does not clear history.

The two Crown events may protect the same selected ally. Sum Crown-transferred amounts against level+M per round. Its heal is floor(final Paladin branch actual damage/2) for each event, then capped by the remaining S+M per protected ally that round. Commit that nominal source entitlement before target healing restrictions; blocked or capped healing refunds no event, transfer amount or healing entitlement. The heal cannot heal the Paladin or start another redirection/heal-copy chain.

## Bloom and devices

Bloom Ward is a finite10+Oracle-level prevention pool across packets. Apply its legal prevention after ordinary defenses. Subtract only the prevented amount. The bloom ends on depletion, its1minute expiry, or actual legal removal. Suppression alone does not end it. Ending grants the printed +1 Frightened-save rider through the target's next end. A late clock observation must retain the endpoint calculated from the actual expiry, not create a fresh duration. An unmitigated transferred branch cannot consume this prevention pool.

Emergency Protocols requires an active/conscious drone within its printed range. The transfer occurs after the Tinker's defenses and before temporary HP. The drone receives the bounded transferred amount without mitigation; legally granted temporary HP can absorb it. At0HP the drone is destroyed and receives no organic Wound or death-save procedure.

Tinker engine[2] retains the destroyed drone at0 until its explicit repair/rebuild procedure. Ordinary functional repair cannot reconstruct a destroyed drone or reset ammunition, uses, duration or command budget. This package's device helper only resolves damage/destruction; it does not implement reconstruction or grant a destruction reward. The broader companion/device lifecycle remains open.

## Reference boundary

The helper validates arithmetic, stages, branch identity, replay protection and round entitlements. Callers establish legal sources, target relationships, exact source cadence, action/resource payment, clock endpoints and source-native riders. No helper imports card ownership merely from a string identifier. The source register preserves every exact original procedure alongside the overlay.

Guardian Pulse's new counterattack carries its explicit no-further-free-attack/no-Action limits, without inheriting unrelated incoming healing/resource/reflection restrictions. Palm's force damage has no invented copy/action/resource prohibition; each downstream source determines eligibility. It cannot trigger another Palm because it is not a melee attack.

Validation currently covers94 targeted checks and186 conservation states. Full-game completion, human balance and all-source combat/device execution remain separate unfinished work.
