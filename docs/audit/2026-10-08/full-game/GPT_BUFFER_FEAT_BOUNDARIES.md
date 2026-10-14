# GPT eight-feat dependency reconciliation — captured completed reply

ChatGPT said:

The 15 boundaries can be reconciled without changing the eight feat IDs or reopening the promoted five-spell package. The attached evidence changes two parts of my prior feat draft materially: Necrotic Affinity’s death seal must use the broader printed “you kill with necrotic damage” scope, and Lifeleech needs an explicit finite feat-specific recovery budget to satisfy the frozen permanent-healing rule. The frozen rule requires repeated permanent HP recovery to consume RP, a per-rest use, or another finite resource. 
Pasted text

1. Necrotic Affinity: broaden the death seal

The prior requirement that Necrotic Affinity's own +1d6 contribute was too narrow. The source says:

“Creatures you kill with necrotic damage…” 
Pasted text

Use this corrected rule:

PRESERVED scope: any qualifying necrotic damage event genuinely owned by the Necrotic Affinity holder can establish the 24-hour seal. It does not have to come from the feat's melee bonus die.

Qualifying examples include the holder's:

necrotic spell damage;
Necrotic Affinity 1d6;
Agony Lance, because its damage belongs to that feat owner;
another exact personal necrotic source whose event ownership is that character.

It does not include an attack merely because the holder supplied statistics to another creature. The transformation package already establishes that transformed subjects own their attacks/damage.

For a mixed-damage fatal root, the seal applies when the holder owns a positive resolved necrotic component of that fatal root and that root actually causes the death. No counterfactual “would it still die without the necrotic point?” test is needed.

Also qualify:

a necrotic packet that directly causes Instant Death;
a necrotic packet against a 0-HP target that directly causes the fatal death-failure consequence;
a later fatal consequence only where the canonical death event preserves the qualifying necrotic causal root, such as an explicitly source-linked fatal Wound consequence.

Temp-HP-only necrotic absorption with no harmful consequence cannot establish it.

So the candidate clause should read:

Necrotic Death Seal: When a creature actually dies from a damage/death root containing positive qualifying necrotic harm owned by you, attach a Necrotic Affinity seal to that death instance for 24 elapsed hours.

That is the source-faithful interpretation, not a NEW narrowing.

2. Lifeleech: finite Recovery Reserve

Yes. The frozen recovery rule applies to the feat too. Free necrotic cantrips otherwise make the printed recovery permanently farmable. 
Pasted text

Add this explicitly NEW feat resource:

Lifeleech Recovery Reserve

Capacity at each completed long rest: 2 × character level.
Snapshot capacity at that completed rest.
Reset to that capacity on the next completed long rest.
It is neither RP nor Mutation Recovery Reserve and does not interact with those resource pools.

For each legal Lifeleech healing event:

determine qualifying actual necrotic damage;
raw Lifeleech healing = floor(actual necrotic damage / 2);
run ordinary healing reductions/prohibitions to determine legal healing potential;
cap that potential by remaining Lifeleech Recovery Reserve;
that capped amount is the funded Lifeleech heal;
when the healing event commits, spend that funded amount from the reserve;
actual HP restoration and genuine excess are then calculated from that funded amount under the existing healing rules.

This choice is important: the finite budget spends funded healing potential, not merely HP actually restored. Otherwise a full-HP character could generate unlimited excess-healing conversions without consuming the finite resource.

A broad HP prohibition makes legal healing potential 0, so it spends 0 reserve and produces 0 excess.

At reserve 0:

the damage trigger may still occur and consume its round/root entitlement;
the resulting funded healing is 0;
it cannot generate excess.

This preserves Lifeleech's printed spell-damage identity while satisfying the game's finite permanent-recovery invariant.

3. Chef: one batch per completed long rest

Use one feat batch per Chef per actual completed long rest, not multiple one-hour batches within the same rest.

The source says the special food is cooked “during a long rest”; the gear source supplies ordinary rations and cook's utensils but no alternate feat production economy. Rations are 5 sp/2 lb and cook's utensils are 1 gp/8 lb. 
Pasted text

Exact transaction:

At most one pending Chef batch may be designated for a given Chef/rest attempt.
Spend 1 hour cooking during that rest.
This can count as permitted light activity only if the canonical long-rest procedure permits that hour; Chef does not enlarge the rest's permitted activity allowance.
Consume one standard ration/meal-equivalent ingredient per intended serving when the cooking hour successfully completes.
The cooked food physically exists at that point.
The Chef feat potency is not created unless the long rest successfully completes.
If the rest fails/aborts, the consumed ingredients remain spent and the prepared food is ordinary food with no Chef temp-HP property.

At successful rest completion snapshot that Chef's:

current PB = number of servings;
current PB = basis for shield amount 2 × PB.

Each serving gets its own persistent item ID.

Feat-potency expiry:

min(batchCreationTimestamp + 24h, Chef's next completed long rest after the creation rest)

The creation rest does not immediately expire the batch because it is created only after that rest has completed and advanced the Chef's epoch.

At the shared rest-completion timestamp:

clean up effects expiring on the just-completed old LR epoch;
advance LR epochs/reset appropriate resources;
finalize the successful Chef batch using the new epoch.

Consumed, discarded and expired serving IDs remain consumed/discarded/expired and cannot be replayed.

4. Chef versus crafted Feasts

Chef's special servings are not members of the crafted Feast recipe family unless an actual recipe says so.

The recipe catalog independently defines 10-minute consumption, recipe ingredients/checks and a “one feast at a time” rule, including recipes that restore RP or grant other traits. 
Pasted text

Therefore:

Chef does not occupy the recipe system's one feast at a time slot.
A separate active recipe Feast rider and a Chef rider may coexist if their own rules allow it.
Their temp HP still use the global strongest-only rule.
Non-temp-HP recipe riders remain independent.
One physical food item/consumption cannot claim both Chef potency and a recipe's crafted effect unless an exact recipe explicitly says it is also a Chef serving.
Chef never substitutes ordinary rations for recipe-specific materials/checks/crafting time.
Chef potency adds no market markup. Once the feat potency expires, it remains ordinary food.

This preserves recipes such as the 2-hour Refined Caustic Feast and multi-day Resonant Meal as distinct crafting outputs. 
Pasted text

5. Recipient limits and snapshots
Chef and Inspiring Leader

A recipient's source-family entitlement is spent by a legal completed offer, even when a stronger/equal existing temp-HP grant wins arbitration.

For Chef:

consuming the legal serving and resolving its offer spends that recipient's Chef entitlement for the current recipient LR epoch.

For Inspiring Leader:

select all recipients at speech start;
count limit uses speaker PB at start;
shield amount uses speaker character level and actual CHA modifier snapshotted at start;
no mid-speech retargeting.

Temporary CHA falling below 13 after feat acquisition does not disable the owned feat. The prerequisite is checked when the feat is acquired; there is no supplied general ongoing-prerequisite-loss or retraining rule.

An interrupted Inspiring Leader speech:

spends no recipient entitlements;
has no owner per-rest use to spend;
may be started again.
Blood Ritual

At ritual start snapshot:

character level;
PB;
leader;
exact selected other allies.

No replacements/retargets mid-ritual.

Blood Ritual's 1/LR use commits at ritual start, so interruption does not permit restarting until the use actually resets.

6. Ally/self, acquisition and spellcasting ability

Frozen rules say ally includes self unless it says OTHER. 
Pasted text

Therefore:

Inspiring Leader: keep the prior NEW self-exclusion because this candidate deliberately interprets “companions” as up to PB other creatures.
Blood Ritual: leader is the self recipient exactly once; select up to PB other allies.
Soul Cage shield: “ally” includes self.

Feat acquisition uses actual class feat/ASI milestones, not a new universal feat progression. The frozen schedule establishes 4/8/12/16/19 by default, Oracle's exception, and class-specific schedules where applicable. 
Pasted text

All eight are nonrepeatable.

“Spellcasting ability” means an actual source grants the character spellcasting and identifies a legal casting ability. It is not inferred merely from:

possessing RP;
Oracle Revelation Charges;
another magical resource.

For Soul Cage, when the feat is acquired, lock one actually possessed qualifying spellcasting source/ability as its DC provider. No general retraining mechanism is invented.

7. Empowered Summoning identity

Use:

SummonLineageKey = sourceRootId + creationSlot/bodyLineage

Each distinct creature genuinely created by the original source receives its own creation grant.

A recreation/reissue of the same lineage:

does not regain the 2PB creation shield;
retains that lineage's existing numbered-round Empowered Summoning damage-use state.

A new actual source activation can generate a new summon root when that source is genuinely paid/used under its own rules. It does not have to spend RP. An ability that costs a limited use, Action, ritual use, item charge, etc. can still create a qualifying new summon. No artificial RP requirement is added.

Creation temp HP snapshots PB at creation:

2 × PB_at_creation

The damage rider uses the owner's current PB when the qualifying damage roll occurs.

For the “first damage roll each round” clock:

in initiative: canonical numbered round;
outside initiative: canonical six-second round-equivalent window supplied by the world scheduler;
entering/leaving initiative preserves that phase and cannot refresh the rider.

For a shared/area roll:

add PB once to the shared roll;
not once per affected target.

The feat creates no commands, Actions, initiative entries or ownership changes.

8. Field Medic stabilization

Yes. A real dying → Stable transition caused by this owner triggers Field Medic even if a separate legal effect subsequently restores HP in the same overall sequence.

The Battlefield Medic background is a separate source: healer's-kit stabilization immediately restores 1 HP. 
Pasted text

Order for a character with both:

healer's kit legally stabilizes the dying creature;
record the actual stabilization transition and Field Medic entitlement;
Battlefield Medic's Trauma Response independently restores 1 HP;
Field Medic grants the PB temp-HP offer.

No conflict: the feat trigger already occurred when the target actually became Stable.

Field Medic's episode guard is:

targetId + dyingEpisodeId + featOwnerId

because the source says when you stabilize the creature. There is no reason to impose a cross-owner Field Medic family lock.

Event idempotency also stores the actual stabilization event ID so replaying the same event cannot grant again.

A new dying episode requires the target to genuinely leave the prior dying episode and later become dying again.

Damage absorbed entirely by temp HP does not create a new dying episode.

For healer's kits, consume exactly one actual item use/recorded use according to the inventory system. Do not invent a kit charge count where none is supplied.

9. Necrotic Affinity's rank-5 resurrection seal

Keep the predicate exactly bounded:

blocks an applicable resurrection effect whose actual spellRank/effectiveRank <= 5.

Do not invent effective ranks for unranked class features.

The attached evidence means this currently has a real reviewed target: Paladin Grace Reversal has spellRank: 5, so it is blocked by the seal. The ordinary Resurrection spell is Rank 7 and True Resurrection Rank 9, so those are above the seal. Other class resurrection cards shown with spellRank: null are not silently treated as Rank 5 or lower. 
Pasted text
 
Pasted text

Multiple Necrotic Affinity holders may create independent seal records on the same death instance.

Same owner, same death instance: no duplicate stacking; a second qualifying application is redundant.
Different owners: separate records/endpoints.
Boolean blocking does not compound.

Removal:

natural expiry;
or a source explicitly capable of removing that resurrection blocker.
Generic cure does not erase it.

Attach seals to deathInstanceId, not permanently to the immortal identity.

If a legal Rank 6+ resurrection returns the creature before the seal expires:

that death instance is over;
its seal records remain historical but no longer apply to the living identity.
A later death creates a new death instance and can receive new seals independently.
10. Lifeleech causal cap and clock

Before a qualifying spell damage event resolves, designate one hostile target for Lifeleech.

The spellRootId + roundWindowId entitlement commits on the first positive actual necrotic damage dealt to that designated target by that spell root during that window.

It commits even when:

floor(D/2) is 0;
healing is capped;
healing is blocked;
the Recovery Reserve is empty.

That prevents retarget/reroll fishing after observing the healing result.

Use only the actual necrotic component of mixed damage.

actualNecroticDamageDealt is bounded by the existing actual-damage rules; overkill is not counted as additional drain value. The healing/death interface already distinguishes actual damage from raw packets. 
Pasted text

Clock:

numbered round in initiative;
one authoritative six-second round-equivalent outside initiative;
same phase preserved across initiative transitions;
no enter/leave reset.

Excluded:

transformation natural attacks;
Agony Lance;
Necrotic Affinity melee die by itself;

because none of those is “necrotic damage with a spell.”

Lifeleech child healing should carry narrow causal flags:

noLifeleechRetrigger
noHealingCopy
noResourceGeneration

It may still supply genuine excess to an otherwise legal outside excess converter, but only from the funded finite Lifeleech healing amount after the Recovery Reserve cap. One excess point can still fund only one converter. 
Pasted text

11. Shared Soul Charge death checkpoint

There is exactly one owner pool:

SoulCharges = 0..3

shared by Lifeleech and the Soul Cage feat.

One owner + deathEventId + bodyId entitlement can produce at most one charge.

Apply the ordinary targeting rule: 30 ft, perception and line of effect unless the source expressly overrides it. The frozen class rule supplies that default. 
Pasted text

So Lifeleech's automatic soul-spark trigger also requires the feat owner to perceive the qualifying death within 30 ft and have legal line of effect.

When an eligible death is evaluated, reserve:

owner + bodyId + ownerLongRestEpoch

and permanently mark that exact death event as evaluated for that owner.

If pool = 3:

no charge is added;
the death entitlement is still consumed;
there is no latent fourth charge.

Soul Cage-only optional capture:

accept: add charge if capacity permits, then mark evaluated/reserved.
decline: mark that death event declined/evaluated for that owner; no later corpse scan.
full pool: evaluated with no charge.

A new owner long rest can permit a future new death event of that same body to qualify again after legal resurrection/redeath, but it never permits rescanning the old corpse/death event.

Multiple owners evaluate independently.

12. Soul Cage feat versus spell, Soulrender and Soul Bind

They remain completely distinct source identities.

The ordinary Soul Cage spell is Rank 6, 13 RP, Action/60 ft and remains separately blocked pending its own operational review. The feat grants no spell access. 
Pasted text

The Soulrender prestige unlock separately requires:

specified base class 10+;
Lifeleech;
Soul Cage;
Wounding Magic;
listed skills;
and actually stealing the soul of a living named enemy into a black crystal during a ritual event. 
Pasted text

The feat's Soul Charge is merely the residue/spark resource we defined.

Therefore it:

does not satisfy Soulrender's whole-soul ritual unlock;
does not grant the Soul Cage spell;
does not substitute for Soul Bind;
does not cancel Soul Bind.

Soul Bind remains its own identity-bound 24-hour resurrection restriction after its pending tether converts. 
Pasted text

Similar names confer no compatibility.

13. Black crystal and soul-bearing legality

Do not invent price, HP or durability.

A legal Soul Cage conduit is simply:

one discrete physical black crystal object currently possessed by the feat owner and available for use.

No attunement, price or charge capacity is invented.

A crystal can be handed/transferred normally as an item, but:

Soul Charges are stored on the feat owner;
transferring the crystal transfers zero charges;
another Soul Cage owner may use that physical crystal as their conduit for their own owner-level pool;
losing/destroying it prevents Soul Cage capture/spending until another legal black crystal is possessed;
replacement requires obtaining another actual black crystal, with no invented feat-specific purchase price.

Lifeleech does not require the crystal to accumulate its own soul sparks; its source does not mention one.

Lifeleech alone cannot spend charges. “Charges can power Soul Cage abilities” means the owner must actually possess the Soul Cage feat to use those abilities.

Soul-bearing eligibility remains source-qualified:

immutable object-origin transformed creatures: ineligible;
manufactured/created summons used as generated bodies: ineligible under the anti-farm rule;
do not globally declare all undead, constructs or other categories soulless.

Where the creature's soul status is not established by source/canon, leave it to the future creature/soul taxonomy or Director adjudication rather than inventing a type-wide rule.

14. Agony healing suppression

Use one active AgonyHealingSuppression source-family record per target.

Multiple Agony Lances do not multiply:

no 1/4;
no 1/8.

A new legal Lance against a target already carrying the record:

still spends the full 2 Soul Charges;
still resolves damage/save normally;
does not create a second multiplier;
refreshes the single record to the later absolute endpoint:

newExpiry = max(oldExpiry, newApplicationTimestamp + 60s)

The multiplier remains exactly ×1/2.

For provenance, store the latest source owner plus contributor history if desired, but arithmetic is still one family record.

Consumption:

next committed HP-healing event with positive pre-reduction healing potential;
consume exactly once under the reviewed next-healing-reducer procedure even if actual healing is later blocked/capped. 
Pasted text

Successful CON save or necrotic immunity changes the Lance's damage result but does not remove this separate rider.

It does not affect:

temp HP;
stabilization;
resurrection;
prevention;
maximum HP.

Removal requires an effect explicitly capable of removing this kind of magical healing suppression/debuff. No generic cure is assumed.

15. Blood Ritual advantage and long-activation timing

Confirm: the curse/disease advantage is an independent timed rider, not attached to the self temp-HP grant.

Therefore it exists even if:

the ritual's self temp-HP offer is rejected;
the shield is later replaced;
it is depleted.

It ends on the earlier of:

the owner's next completed long rest;
the first actual saving throw the owner makes against an effect explicitly tagged/classified as a curse or disease.

The entitlement is consumed when that qualifying save is rolled, regardless of:

success/failure;
other advantage/disadvantage sources;
cancellation into a straight roll.

It does not remove or waive Oracle's intrinsic Curse.

Long activation / interruption

Blood Ritual

1/LR use commits at ritual start.
Actual interruption before 10 minutes: no completed benefits; use remains spent.
Selected allies do not retarget.
No HP payment.

Inspiring Leader

no owner use commits at start;
interrupted speech yields no benefit;
may restart normally.

Chef

ingredients consumed when its cooking work successfully completes;
Chef potency finalizes only after successful LR completion as described above.
Shared timestamp ordering

At an exact long-rest completion timestamp use:

finish any already-started event/ritual whose completion timestamp is strictly before rest completion;
process effects whose deadline is that completed long rest, including default-LR temp-HP/rider cleanup;
increment the long-rest epoch and perform rest resets;
finalize Chef's pending successful-rest batch;
resolve an activation whose completion is defined at exactly that same post-rest boundary.

For Blood Ritual specifically:

if its 10-minute completion happened before the LR endpoint, its default-lifetime self temp HP expires at that LR normally;
if the ritual's completion is intentionally scheduled at the exact LR-completion boundary, process the LR transition first and then the completed ritual, so its new default-LR shield belongs to the new epoch rather than instantly expiring.

That tie rule prevents timestamp ambiguity without changing the feat's 10-minute duration.

Corrected candidate changes

The major changes from the previous eight-feat drafts are:

Necrotic Affinity: broaden seal provenance from “feat 1d6 contributed” to any qualifying necrotic kill owned by the feat holder.
Lifeleech: add NEW 2 × character level Recovery Reserve per completed LR, spent from funded healing potential so excess cannot be farmed at full HP.
Chef: exactly one feat batch per completed LR; potency appears only after successful rest completion.
Soul Charge: death event is consumed/evaluated even at full capacity or explicit Soul Cage decline.
Agony Lance: same-family healing suppression refreshes duration but never multiplies.
Blood Ritual: save advantage is an independent rider, not buffer-linked.

Everything else above is either preservation of the exact source or a labeled NEW integration bridge required to make the source executable.

The eight feats should remain:

SOURCE-DISCUSSED / RECONCILED CANDIDATE DESIGN — implementation and adversarial validation pending; no feat promoted.

The separate Soul Cage spell, full Soulrender ritual mechanics, broad soul taxonomy, recipe system beyond the supplied interactions, whole-game geometry/items and human numerical balance remain separate work.
