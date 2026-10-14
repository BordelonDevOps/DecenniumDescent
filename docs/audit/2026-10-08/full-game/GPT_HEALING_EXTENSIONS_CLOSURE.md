# GPT exact healing-extension closure

The three primitives are sound. I found no code-level contradiction requiring another rewrite, but Crown's Burn needs one exact caller-contract clarification so fixed-at-activation targeting cannot be accidentally reinterpreted later.

1. oracle.supplement.flame.crown-s-burn
Recipient timing — confirm predeclaration

Yes. Oracle engine [26] controls the generic Oracle area/zone target-selection interface here:

allied recipients must be selected before Crown's Burn resolves its hostile damage, saves, or shared healing-cap roll.

For this primitive, recipient_ids means:

declaredRecipientIdsAtActivation

not “currently preferred recipients after seeing the damage.”

Operational order:

Declare burst center.
Declare up to three legal living allied recipients in the burst.
Lock that recipient set.
Resolve enemy saves/fire damage.
Sum qualifying numeric actualDamageDealt.
Roll the one shared S d6+M healing cap.
Divide by the locked declared-recipient count, floor once.
Generate each declared recipient's source healing application.
Each target runs its own ordinary healing pipeline.

Enhanced Crown's Burn mastery changes only where recipients may legally be selected; it does not reopen target selection after damage.

If a declared recipient later becomes ineligible

Use the locked denominator.

NEW clarification: if a declared recipient ceases to be a legal living healing target before its healing application resolves, that application fails/skips, but:

no replacement ally may be selected;
the denominator is not recomputed;
the other allies do not receive a larger share.

This prevents opportunistic redistribution.

The helper is compatible with this because it expects the already-declared ID set. The caller must not reconstruct recipient_ids from only surviving/legal recipients after damage.

I would add one regression eventually:

three recipients declared; one becomes ineligible before healing → division still uses 3 and no replacement target.

That is useful hardening, but not a defect in the supplied primitive.

Shared cap implementation

crown_burn_healing() is correct:

numeric qualifying damage, not positive-packet existence;
zero recipients safely returns no applications;
one shared cap result;
floor(total / declaredRecipientCount);
source minimum 1 only if numeric total >0;
diceCount=S and one shared rollInstanceId;
each target then gets an independent healing pipeline.

The source minimum remains pre-reduction, so Decay or another prohibition can still make actual HP gained 0.

Disposition: REVIEWED / reference-VALIDATED for the Crown's Burn pooled/shared-healing primitive, with the fixed-recipient caller contract above.

2. oracle.supplement.flame.zealot-s-renewal

The implementation now matches the exact card.

zealot_backlash() correctly models:

a separate fire damage packet after the healing attempt, with a minimum resolved damage of 1 unless an expressly authorized source suppresses the backlash entirely.

The important stage boundary should be recorded as:

Determine whether an explicit Convergence/Prophecy suppression cancels the backlash.
If suppressed: no backlash packet exists.
Otherwise roll 1d4.
Apply every legal ordinary damage reduction/defense/prevention that is permitted to affect this backlash.
Then enforce:
resolvedBacklashDamage = max(1, defendedResult).
From that point onward, do not apply another damage-reduction/prevention stage.
Apply temp HP.
Apply normal HP loss.
Resolve Wounds, Instant Death, zero-HP and death consequences normally.

That means even immunity producing a defended result of 0 becomes resolved damage 1 because this source expressly says it cannot be reduced below 1.

The only way to get zero backlash is an effect expressly authorized to suppress the backlash component, rather than merely reduce its damage.

The tests correctly demonstrate:

immunity/0 defended damage → resolved1;
explicit suppression →0;
1-HP ally can be dropped to0;
temp HP can absorb the resulting resolved damage;
blocked healing does not cancel the later backlash.

The Poisoned/disease option remains independent of actual HP restoration as previously decided.

Disposition: REVIEWED / reference-VALIDATED for the Zealot's Renewal backlash primitive.

3. mirrorsage.arch.dual-echo-cast

The helper correctly removes the previously imported Echo Fusion restriction.

Dual Echo Cast permits:

exactly two distinct captured records;
captured from two different source creatures;
both may be Mend;
both RP costs paid externally;
both records consumed externally;
one combined release/action;
each component resolves at floor(rolledProfileAmount / 2) independently.

There is no source basis for restricting Dual Echo to one healing profile.

Dice provenance

Correct:

the half result is a copied numeric amount, not newly rolled healing dice.

Therefore:

sourceBase = floor(originalRolledAmount / 2);
diceCount = 0;
retain the original sourceRollId only as provenance;
Desecrated Ground/per-healing-die adjustments cannot invent dice in the copied half;
a separately authorized +1d6 later is a real added die and gets its own actual die provenance.

The test proving 9→4 and 7→3 with no per-die penalty is correct.

Both Mend components on one ally

Also confirm.

Two distinct legal Mend records may both target the same ally. Neither disappears solely because both are Mend.

For this bounded primitive, treat them as:

one healingRootId / combined release;
two distinct numeric healing components.

What downstream same-target effects do with those two components—e.g. whether a particular trigger says “once per release,” “once per healing event,” or “each time HP is restored”—remains governed by that downstream source's own wording and the broader copy/provenance package. This primitive does not need to collapse them into one amount or declare two independent release actions.

The common copy restrictions still apply:

no resource duplication;
no copied passive/proc;
no copy of a copy;
no extra release.

Disposition: REVIEWED / reference-VALIDATED for the Dual Echo Cast two-Mend numeric-component primitive.

Bounded closure

I would now record:

Interface	Status
oracle.supplement.flame.zealot-s-renewal backlash	REVIEWED / reference-VALIDATED
oracle.supplement.flame.crown-s-burn pooled/shared healing	REVIEWED / reference-VALIDATED
mirrorsage.arch.dual-echo-cast two-Mend numeric components	REVIEWED / reference-VALIDATED

The submitted 20 extension checks PASS and cover the important arithmetic/provenance boundaries.

One documentation hardening should accompany closure:

Crown's Burn recipient_ids are the fixed predeclared activation set. Loss of eligibility before healing does not permit replacement or denominator recomputation.

No broader claim follows. The remaining 131-source card integrations, Oracle scheduler, max-HP composition, companion/device/temp-HP lifecycle, complete copy/trigger provenance, the in-progress 39-source redirection implementation, and the full game remain open.
