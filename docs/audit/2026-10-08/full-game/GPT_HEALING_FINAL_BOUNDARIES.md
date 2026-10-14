# Healing final boundary conference

Captured from the visible completed Calibration Review reply; implementation review remains required.

These seven boundaries can be fixed now. I would implement them as follows.

1. Positive damage event vs. numeric actual damage — confirm

Keep the two inputs separate:

positiveDamageEvent = resolvedDamage > 0
actualDamageDealt = tempAbsorbed + actualHpDamage

For Divine Judgment, use the positive packet as the trigger predicate, then use actualDamageDealt only to calculate the reflected amount.

So:

If a marked creature deals a positive resolved-damage packet to another creature on its turn, that turn's Divine Judgment entitlement is consumed. Reflection is max(1, floor(actualDamageDealt / 2)), capped by Cleric level.

Therefore:

HP 1 target, protected by a 1-HP floor, takes resolved damage 5.
positiveDamageEvent = true.
actualDamageDealt = 0.
Divine Judgment triggers and reflects 1.
Its once-this-actual-turn entitlement is consumed.

If defenses reduce the packet to resolvedDamage = 0, there is no damage event and the entitlement is not consumed.

This is the narrow consequence of the printed “deals damage” trigger plus “half actual damage, minimum 1”; it should not redefine other numeric damage-derived effects. Wrathful Brand/Balanced Scales likewise use the positive damage predicate where their text says the creature was damaged, while drains explicitly based on actual damage use the numeric metric. 
Pasted text

2. Ward damage metrics — confirm with the proposed freeze

Yes. A would-die replacement can alter the final life/HP state without retroactively rewriting the amount of damage the packet actually inflicted.

Use:

packetHpLossBeforeReplacement

as the HP loss produced by the damage packet after temp HP and applicable pre-death HP floors, but before the would-die replacement.

Then when the replacement changes final HP:

actualHpDamage = min(packetHpLossBeforeReplacement, max(0, preEventHP - replacementHP))

Never count HP removed solely because the death replacement assigns a lower state value.

Examples:

HP 20, takes 10, then fatal Wound failure. Packet HP loss = 10, provisional HP = 10. Ritual Ward replaces death and assigns HP 1.
actualHpDamage = min(10, 19) = 10, not 19.

HP 5, takes 100, Core Instant Death. Packet would lose 5 normal HP. Ward replaces death with HP 1.
actualHpDamage = min(5, 4) = 4.
postTempDamage remains 100.

Already HP 0, Ward intercepts death and results in HP 1 or Stable 0.
actualHpDamage = 0.

HP 12 with a pre-existing 1-HP damage floor, packet would otherwise remove all 12 but floor leaves 1. If a later fatal Wound result invokes Ward, packet HP loss was already 11. Ward does not rewrite it.

This matches the NEW anti-overkill bridge.

It also means post-packet emergency healing never changes the damage metrics of the packet that triggered it.

3. Spiral-Touched Boon III — accept the source-specific pre-Wound recovery exception

Use the exceptional sequence you proposed.

Spiral III says the damage would reduce the Oracle to 0 and it instead regains quarter maximum HP and phases out. 
Pasted text

Operational sequence:

Resolve defenses/temp HP/post-temp damage.
Test Core Instant Death. If Instant Death succeeds, Spiral III cannot trigger.
Resolve any true pre-zero damage floor already applicable.
If a positive→0 crossing still exists:
consume/mark the Spiral III 1/LR use;
preserve the raw drop-to-zero Wound trigger;
attempt max(1, floor(effectiveMaxHP/4)) HP recovery;
apply phase-out.
Then resolve the required Wound save using the original packet's post-temp damage and pre-event Wounds.
If that Wound save is fatal:
creature dies;
Spiral III remains spent;
phase-out ends;
only an independently legal would-die replacement can intercept that death.

So Spiral III is the explicit exception to the general “Wound resolution before post-zero healing” rule.

If Decay blocks its quarter-HP recovery, the use is still spent and phase-out still applies, but the Oracle remains at 0 before the Wound save.

Other Phoenix/Unyielding-style post-zero healing remains after Wound/death adjudication.

4. Conscious-at-zero action permissions
Mage Undying Spellform

The operative Mage text specifically says the Mage remains conscious and “able to take Actions.” 
Pasted text

Implement a partial zero-HP override:

While Spellform is active, ordinary zero-HP consequences do not impose the Unconscious/Incapacitated restrictions that would prevent:

normal speech;
voluntary movement up to the printed half-Speed cap;
taking one normal Action;
using that Action to cast a legal spell;
starting or maintaining concentration.

It grants no independent Bonus Action or Reaction permission.

Separate restrictions still apply normally:

Stunned;
another Unconscious source;
Expedition 5/6;
Silence/components;
action denial;
movement prohibition;
etc.
Concentration on the triggering damage

Important precision:

Spellform prevents the zero-HP state itself from automatically ending concentration while its exception applies.

But the triggering damage still causes any ordinary damage-based concentration save. If that save fails, concentration ends.

So existing concentration is not automatically lost merely because HP became 0 under Spellform.

This is the cleaner reading of “remain conscious and able to take Actions” and avoids making a Mage survival feature unable to function as a Mage feature.

The Mage may also start a new concentration spell with its permitted Action; normal one-concentration rules apply.

Oracle False Life Boon III

Different exception.

During the permitted zero-HP turn choose exactly one:

move up to Speed;
speak normally;
activate one Revelation.

If Revelation is chosen, that single permission allows the Revelation's own normal activation form:

Action;
Bonus Action;
or a triggered activation whose trigger actually occurs during that turn,

with all normal RC/cost/component/concentration requirements.

This does not grant a free additional Action/Bonus Action/Reaction beyond the chosen Revelation activation.

For example:

choose a Bonus Action Revelation → that is the one chosen option;
cannot then also take an ordinary Action;
choose movement → cannot also activate a Revelation.

Existing zero-HP concentration was already lost unless another effect expressly preserved it; selecting a concentration Revelation can establish new concentration as part of that legal Revelation activation.

5. Next-healing reductions — confirm

Use a pure preview, then one commit.

Eligibility

A next healing reducer is eligible to consume when:

its record is present;
it is operative and unsuppressed;
it applies to this target/event;
the healing event has positive pre-reduction HP-healing potential.

Zero-potential/non-healing events do not consume it.

Two-pass preview

The preview used to resolve restoration-conditioned bonuses must be pure:

no reducer is consumed;
no once/event trigger is spent;
no pool changes.

After eligibility has been established and the final packet is committed:

consume every operative next-positive-healing entitlement applicable to that event exactly once, even if another mutually exclusive reduction branch ultimately produces the lower healing result.

Thus if:

Talon Strike,
Withering Shot,
Blight Infusion

all legally apply, they are consumed by that healing event.

If Blight Totem's nonstacking branch produces the winning lower result, those next-heal entitlements are still spent because their “next healing” occurred.

A later broad prohibition such as Decay reducing actual gain to 0 does not refund them.

Suppressed reducers:

do not participate;
do not consume.

This avoids preserving one-shot debuffs merely because another reduction happened to dominate the arithmetic.

6. Channel Life excess temp HP — confirm the stronger source-local prohibition

Agreed.

Channel Life expressly says the transfer:

“cannot ... create excess temporary HP.” 
Pasted text

Tag the resulting healing packet with:

forbidExcessTempHpConversion = true

That prohibition follows the healing packet, not the owner of a later converter.

Therefore no effect, including an external feature, may convert Channel Life excess into temporary HP.

It still:

receives otherwise legal healing bonuses;
suffers reductions/prohibitions;
can trigger legitimate restoration-conditioned effects after actual HP restoration.
Cosmic Equilibrium

Its conversion is not temporary HP. It turns genuine excess into bounded radiant damage.

Channel Life does not prohibit that.

So if:

Channel Life's healing is otherwise legal;
actual missing HP is exceeded;
no broad healing prohibition makes the packet zero;
Cosmic Equilibrium is active/eligible;

then genuine remaining excess may feed Cosmic Equilibrium's damage conversion under its own once/round and S+M limits.

The common excess ledger still prevents the same point of excess from being converted twice.

The Channel Life packet simply has:

tempHpConversionEligible = false

not:

allExcessConversionEligible = false.

7. Cross-source secondary-heal cycles — accept provenance-set model

Yes. This is the cleanest general solution.

Every root healing resolution gets a causal identifier:

healingRootId

and a provenance structure containing at least:

visitedHealingApplicationIds

When a healing effect produces a new secondary healing packet:

inherit the root ID;
copy the visited set;
add the producing link/application ID;
evaluate potential downstream triggers.

A link/application may fire at most once in that root causal chain.

Example

Root heal triggers:

SharedBreath-A

Secondary heal travels to creature B.

B is also linked by:

SharedBreath-B

That second distinct link may fire once.

If that secondary heal would come back through SharedBreath-A, reject it because A is already in the visited set.

This prevents:

A → B → C → A loops

without globally disabling valid cross-source first-generation behavior.

Stronger source restrictions override provenance allowance

If a source says:

“does not trigger another link”;
“no secondary healing procs”;
“no resource procs”;
“cannot trigger healing loops”;

attach the appropriate prohibition flags to its child packet.

Examples:

Vitality Link: its secondary heal cannot trigger any another link, not merely itself. So child packet carries blockLinkTriggers=true. 
Pasted text
Echo Leech: child healing carries blockSecondaryHealingTriggers=true and blockResourceTriggers=true as its source says. 
Pasted text
Blood Feast: its secondary heal cannot generate damage/resource triggers per source.
Merciful Smite: cannot create Smite or heal-copy chains.
Crown Undying: cannot create another redirection or heal-copy chain.
Numeric healing add-ons

A numeric add-on such as:

+S;
+M;
+1 per die;
Garden +1;

remains part of the same healing packet.

It:

does not create a child healing packet;
does not start a new causal chain;
does not receive a new root ID;
cannot recursively trigger itself.
First-generation finite healing

A normal paid/finite primary heal still begins an ordinary root chain and may trigger unrelated legal first-generation features unless the source specifically forbids them.

So the anti-loop mechanism is provenance, not a blanket “triggered healing never triggers anything” rule.

Exact implementation contract

The seven decisions can be reduced to these invariants:

Damage predicate and damage amount are separate. A positive packet may trigger a minimum-1 effect even when numeric actualDamageDealt=0.
Death replacement never becomes retroactive damage. Damage metrics are frozen from the packet and may only be reduced by HP actually preserved, never increased by a replacement assigning a lower HP state.
Spiral III is a specific pre-Wound recovery exception after Instant Death fails; its raw Wound trigger remains.
Spellform explicitly lifts zero-HP Unconscious/Incapacitated restrictions only far enough to permit speech, half-Speed movement, Actions and concentration; no free BA/Reaction. Oracle III permits exactly one printed choice, with Revelation activation using that Revelation's own action type.
All operative next-heal entitlements consume on the committed positive-potential healing event, regardless of which reduction branch wins or a later prohibition causing zero actual gain.
Channel Life excess can never become temporary HP from any source, but genuine excess may feed a non-temp-HP converter such as Cosmic Equilibrium.
Secondary heals carry causal provenance. Each link/application can participate once per root chain; stronger printed no-proc/no-link restrictions override the generic provenance allowance.

These are ready for Codex to encode into the candidate guide/helpers and adversarial tests. They do not alter the decision to keep the six ordinary death/resurrection spells inactive pending the next exact implementation review.