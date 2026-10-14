# GPT redirection boundaries — complete visible notebook reply

Missing tail from prior redirection proposal

2. Root attribution flags. Implement branch provenance with rootDamageEventId, transfer-operation identity, terminal branch IDs, and source-specific flags such as no-resource/no-reflection/no-retaliation/no-healing-generation. Test physical root totals separately from source-specific eligible totals.

3. Free/counterattack chaining. Guardian Pulse and Redirecting Palm need regression against the existing free-attack/action-chain guards so neither can recursively manufacture further free attacks or copies.

4. Device damage consequences. Emergency Protocols needs the common device damage/destruction procedure when its drone reaches 0. Do not infer organic Wounds, death saves, or resurrection rules for devices.

Disposition: the 39-source set remains SOURCE-AUDITED / DRAFTABLE, not REVIEWED. It is ready for a bounded helper/binding/test implementation, but not for whole-game redirection closure.

1. Mandatory transfers, zero transfers, and root chaining
Final Stand

Confirm the proposed overlay.

paladin.supplement.oath-of-the-chain.final-stand is mandatory while active:

The first eligible positive post-defense damage packet to the protected ally in a numbered round is redirected automatically while that Paladin's shared redirection allowance remains available.

The Paladin cannot decline that eligible event to save Final Stand for a later hit.

If the post-defense remaining damage is 0:

no transfer occurs;
no redirection allowance is spent;
no event is recorded.
Competing mandatory transfers

NEW deterministic rule: if two or more mandatory transfer operations would claim the same original branch, the original damage target selects one legal operation. Unselected operations remain unused.

One transfer operation per root branch

Confirm:

Once a pre-mitigation sharing/redirection operation is selected for a root damage branch, neither its transferred branch nor its retained original branch may later undergo another damage-transfer operation.

This is the root no-chain guard.

Pure prevention and temp HP are not “another transfer,” subject to the source's mitigation restrictions.

Per-owner Paladin allowance

Paladin shared redirection limits are tracked per Paladin owner, not globally across the party.

The root no-chain rule is cross-owner: another character cannot redirect a branch that has already been produced by a transfer operation.

Optional zero transfer

An optional transfer Reaction/feature requires a positive amount capable of being transferred to activate.

Thus:

packet 0 → cannot spend Reaction/resource on “redirect 0”;
packet >0 but chosen amount 0 → illegal activation;
no resource/use/Reaction consumed.

A separate preventive component can still resolve if its own trigger is legal. Example: Crown of Embers' S damage reduction can occur even when no later Crown redirect is available.

2. Exact per-source transfer flags

Do not use a universal “redirected damage has no triggers” flag.

Use independent branch flags:

noSecondMitigation
noRetransfer
noReflection
noRetaliation
noDamageTriggers
noResourceGeneration
noHealingGeneration
noRecoveryGeneration
noPassiveTriggers
noConditionTriggers
noActionGeneration
noCopyGeneration

noReflection is narrower than noRetaliation. Reflection is one retaliation family; a source can prohibit reflection without prohibiting every “when damaged” response.

Matrix
Source	Required transfer-branch restrictions
paladin.engine[10]	noSecondMitigation, noRetransfer, noReflection, noResourceGeneration
paladin.base.protective-stance	engine[10] flags + noDamageTriggers
paladin...burden-shared	engine[10] flags + noHealingGeneration; source separately says no healing/resources
oracle.engine[14]	noResourceGeneration, noPassiveTriggers, noConditionTriggers, noActionGeneration, noCopyGeneration for redirected component unless explicit
oracle.engine[29]	noSecondMitigation, noRetransfer, noReflection, Oracle RC generation blocked
oracle...life-linked	Oracle flags + noRecoveryGeneration, noRetaliation
warrior...guardian-tissue	noSecondMitigation, noRetransfer, BT generation only blocked
warrior...aegis-incarnate	noSecondMitigation, noRetransfer, BT generation only blocked
monk...shared-breath	noSecondMitigation, noRetransfer only
soldier...selfless-guardian	noSecondMitigation, noRetransfer, noRetaliation
tinker.arch.emergency-protocols	noSecondMitigation, noRetransfer, noRetaliation for retaliation loops
ordinary Paladin post-defense redirects without stronger text	engine[10] flags only

Do not convert Warrior's “no BT” into “no resources of any kind.”

Physical versus consumer-specific totals

rootPhysicalActualDamage = sum all terminal branches' actualDamageDealt once.

A source-specific consumer gets:

eligibleActualDamage = sum(terminal actualDamageDealt where that consumer is not prohibited by branch flags)

So an initiating Cleric damage-to-healing consumer does not count a branch marked noHealingGeneration, but physical audit totals still do.

Meaning of noHealingGeneration

It means:

this transferred damage cannot itself generate a derived healing packet.

It does not mean the transfer recipient cannot later receive unrelated ordinary healing.

Explicit source riders

Do not “turn off” a source's own explicit rider with its generic branch restrictions.

Examples:

Linked Ward's temp HP on Paladin reaching 0;
Unbroken Covenant's temp HP “whenever you redirect”;
Crown Undying's explicit finite heal.

These are source-native redirection riders, not generic damage-trigger chains.

Protective Stance + Unbroken Covenant

Protective Stance's noDamageTriggers prevents generic “when you take damage” or “damage creates X” triggers from its transferred branch.

But Unbroken Covenant triggers on the redirection operation itself:

“Whenever you redirect damage…”

Therefore it remains eligible.

Its amount uses the final Paladin branch's actualDamageDealt, but its trigger is redirectionOccurred, not damageTrigger.

No broad exception is needed.

3. Attack identity and Guardian Pulse retargeting

Confirm:

Ordinary transfer

The retained original branch keeps:

original attack target identity;
hit identity;
critical identity;
on-hit riders,

even if all numeric damage is later transferred and its final damage becomes 0.

The transferred recipient gains a damage branch only. It does not become “hit by the attack.”

Guardian Pulse

warrior.hero.wardborn.guardian-pulse is different because it retargets before AC resolution.

Use the original attack roll result.
Compare it against the Guardian's AC.
The Guardian is now the actual attack target.
If it hits, attack-hit/on-hit/critical identity belongs to the Guardian.
The originally intended ally is no longer hit or targeted for attack-hit riders.
Multiple Guardian Pulse retargets

Adopt the NEW one-retarget-per-attack rule.

One attack may be retargeted once. It cannot bounce:

ally → Guardian A → Guardian B → Guardian C.

If multiple eligible Guardian Pulse reactions are offered simultaneously, the original intended target chooses one legal retarget. Only the chosen Guardian spends the Reaction/use.

Attack retargeting is not damage transfer, so it does not consume the later one-transfer-operation opportunity for damage that results from the retargeted attack.

4. Pure prevention on transferred branches

Confirm Bloom is:

finite pure prevention;
1-minute duration;
ending rider target-next-end;
not temporary HP.
Post-defense unmitigated transfer

If a transferred branch says:

“cannot be reduced again,”
“unmitigated,”
or equivalent,

then the recipient skips both:

ordinary defenses; and
additional damage-reduction/prevention effects that reduce that transferred damage.

Therefore these cannot reduce such a branch:

Bloom Ward;
Redirecting Palm's reduction;
Ancestral Guardian;
ordinary flat DR;
resistance/immunity.

But the later life-layer still functions:

temporary HP;
HP floors;
Ritual Ward/would-die replacement;
Core Wounds;
Instant Death;
zero-HP consequences.

“Cannot be reduced” is not “death cannot be prevented.”

Pre-mitigation transfer

A recipient of Bloodbond/Veinlock receives an independent pre-mitigation branch.

It may use:

its normal DR/resistance/immunity once;
legal pure prevention once;

before temp HP/life resolution.

It still cannot transfer that branch again.

Trigger eligibility on transferred damage

Use this distinction:

Result-recipient damage trigger

“when you take damage,” “when you would take damage,” etc.

Can qualify on a transferred branch if:

the branch's flags do not prohibit it; and
the source's effect is otherwise legal.

Attack-conditioned trigger

“when an attack hits you,” “attacker that hit you,” “when critically hit,” etc.

Does not qualify on an ordinary transferred branch because attack identity was not transferred.

Thus a transferred recipient can potentially trigger a generic damage retaliation, but not an attack-hit retaliation, unless the source explicitly says transferred damage counts as a hit.

5. Crown Undying exact ledger
Same ally may be redirected twice

Confirm your reading.

paladin.supplement.oath-of-the-martyr-king.crown-undying permits two different ally-damage events per numbered round.

Those two events may involve the same selected ally.

Do not invent a distinct-ally requirement.

Constraints remain:

ally must be one of the up-to-three selected allies;
max two Crown-authorized damage events per round;
events must be distinct roots;
total Crown-transferred amount ≤ Paladin level + M that round.
Second shared slot belongs to Crown Undying

The extra redirection event is a Crown Undying exception, not a general second Paladin-redirection slot.

So while Crown Undying is active:

total Paladin redirection events for that owner in the numbered round: max 2;
only one may be an ordinary/non-Crown Paladin redirection;
the second, if used, must be Crown Undying.

Crown cannot enable two other Paladin redirection features in one round.

Activation after a prior redirection

If the Paladin already used a normal redirection earlier that numbered round, then activates Crown Undying:

that earlier event remains recorded;
Crown permits at most one additional Crown event that round.

It does not reset the round ledger.

If two redirection events already somehow occurred under a prior legal Crown state, later activation/reapplication cannot create another.

Ledger model

Per Paladin owner + numbered round record:

Plain text
paladinRedirectionEventsUsed: 0..2
ordinaryRedirectionUsed: bool
crownEventIds: set, max size 2
crownTransferredTotal: int, max L+M
crownHealUsedByAlly: map<allyId,int>, each max S+M

Rules:

ordinary feature allowed only if ordinaryRedirectionUsed == false and total events < permitted cap;
Crown event allowed while active if total events < 2 and crownTransferredTotal has room;
one event cannot be both ordinary and Crown;
root no-chain prevents two redirections on same damage event.
Crown healing

For each Crown redirection event:

eventHealPotential = floor(PaladinBranch.actualDamageDealt / 2)

Then:

eventHeal = min(eventHealPotential, remainingPerAllyRoundCap)

where:

remainingPerAllyRoundCap = S+M - crownHealUsedByAlly[ally]

Round per event, then enforce the cumulative per-ally/round cap.

Blocked/capped healing:

does not refund redirected amount;
does not refund event slot;
does not restore Crown's L+M transfer allowance.
6. Redirecting Palm counter target

Correct my prior reading.

The exact card's range says:

triggering melee attacker and one other enemy within 5 feet

and later says:

“If no second enemy is present … redirect no damage.”

Therefore the force-damage target must be an enemy distinct from the triggering attacker.

Operationally:

Triggering melee attack damages Monk.
Monk spends Reaction/Ki.
Reduce qualifying post-defense damage by half, rounded down.
Monk retains the remainder.
If a second enemy distinct from the triggering attacker is within 5 feet, it takes new force damage equal to:
min(preventedDamage, Monk level).
If no such second enemy exists, the Monk still receives the reduction, but no force packet is created.

That new force packet is separately defendable and carries no attack/critical/on-hit identity from the original attack.

This interpretation follows the more specific range-and-target text and “second enemy” wording; no NEW exception is required.

Implementation disposition

These clarifications are sufficient for the bounded implementation packet.

Record as:

39-source redirection conference: SOURCE-AUDITED / DRAFTABLE.

Not yet REVIEWED/reference-VALIDATED until Codex returns:

branch/root provenance helper;
exact per-source flag bindings;
Paladin/Crown ledger;
attack-retarget guard;
prevention/transfer sequencing;
device transfer handling;
adversarial tests.

No whole-game redirection or combat closure is implied.
