# GPT control clock corrections

Captured from the visible rendered Calibration Review reply.

Yes. These are source corrections, not new broad rules. I would revise the implementation exactly as follows.

Reign of Ashes uses the target's next regular-turn end. The operative text controls over the shorter summary field: “a failing target becomes ash-bound until the end of its next turn.” Therefore paladin.reign-of-ashes.ash-bound expires at the target's next regular-turn end, excluding an already-in-progress current target turn under the established next-turn convention. 
Pasted text

For teleportation, adopt the proposed NEW interpretation: ash-bound prevents the target from willingly benefiting from teleportation. It therefore cannot self-teleport, choose to teleport, or consent to another creature teleporting it. A genuinely involuntary hostile teleport/displacement can still affect it unless that teleport source requires a willing recipient. This is stronger than “cannot personally cast teleport” but does not turn ash-bound into universal planar anchoring. Dash remains unusable for benefit while ash-bound.

Use the closed unqualified-next-turn source clock for the ambiguous elemental riders. My earlier target-clock assignments were wrong where the operative source does not name the target.

dragoon.drakestorm-dive.cold-slow: source next regular-turn end.
Drakestorm lightning Reaction denial: same source-next-end clock because “until then” refers to that preceding endpoint.
dragoon.elemental-lance.cold-slow: source next regular-turn end.
Elemental Lance lightning opportunity-attack denial: explicitly target next regular-turn start because it says “start its next turn.” 
Pasted text
shaman.elemental-chorus.slow: source next regular-turn end.
shaman.elemental-affinity.ice-slow: source next regular-turn end. 
Pasted text

These clocks remain source-specific; they are not normalized merely because all are Speed penalties.

“End of that turn” / bare “end turn” means the actual triggering turn, not a fabricated next regular turn. For oracle.resonant-seed, the failed-save slow expires at the end of the actual turn containing the entry/start trigger. If no turn is currently underway, use a six-elapsed-second fallback. If application occurs during an end-turn trigger sequence, the slow applies during resolution and then expires at that same turn end; it does not survive into another turn. 
Pasted text

Apply the same NEW ambiguity bridge to supplied sources whose effect says merely “until end turn” without next:

Druid Winter's Embrace;
Shaman Frost Totem;
Tinker Glue.

Thus an off-turn entry trigger does not silently become “until the target's next regular turn.” One creature/round application caps still apply. This bridge does not override explicit “its next turn,” “target's next turn,” or source-next-turn wording.

Balanced Elements is owner-based and semantic, not Shaman-class-only. Correct the prior overly narrow scope. The target record is eligible when all of these are true:

the speed/Burn application is owned by the character using Balanced Elements;
the specific applied component is explicitly classified as elemental by its reviewed source;
it is a Speed reduction or eligible Burn;
it is not merely Strain, cargo, terrain, form limitation, Exhaustion, or another systemic modifier.

Balanced Elements therefore targets classification.elemental-control, not shaman.elemental-slow.

For the supplied/reviewed records:

Yes: Shaman Ice Elemental Affinity.
Yes: Shaman Frost Totem slow.
Yes: Shaman Elemental Chorus slow.
Yes: Shaman Ice Wisp's cold-linked Speed0 rider. Speed0 is still a Speed reduction for this feature.
Yes: Mage Cold Focus/Bolt/Surge records when owned by the same multiclass character.
Yes: Mage Elemental Fusion/Cascade's explicitly cold elemental slow components when owned by that character.
Yes: Dragoon Drakestorm Dive/Elemental Lance cold riders because those cards explicitly select elemental fire/cold/lightning modes.
No from the supplied evidence: Shaman Flask Root. It is a Root payload, but nothing in the operative Flask source establishes that specific root as an elemental application. Do not infer elemental status from “stone,” “root,” or Shaman ownership alone.
Ordinary spells qualify only after their source/registry explicitly classifies that application as elemental; cold damage by itself should not silently manufacture the metadata if the spell source has not been audited for that tag.

Extension rule:

newEndpoint = max(existingEndpoint, targetFollowingRegularEndMeasuredNow)

where “following” excludes the current in-progress target end.

It never adds another turn to the old endpoint recursively. It never increases magnitude. It cannot extend beyond an express source/concentration maximum that actually governs that rider. Balanced Elements remains once/turn and must pay/obey its own source rules. 
Pasted text

Hypermutation Spike snapshots each possessed movement mode independently. Correct my earlier walking-only formulation. At Butcherform activation, capture a baseline for every movement mode the character actually possesses at that moment.

Define normalModeSpeedBaseline as the mode's ordinary sheet Speed at activation from:

ancestry/creature base Speed;
form base Speed, if the form replaces that mode;
permanent innate Speed increases;
persistent passive Speed modifiers whose requirements are currently satisfied and which normally belong in the creature's ordinary sheet Speed.

Exclude:

temporary buffs/debuffs;
stances;
timed spells/features;
hostile control;
Strain;
cargo;
Exhaustion;
Hypermutation Spike itself.

A conditional but persistent passive such as an unarmored-Speed feature does count if its condition is satisfied at the snapshot moment, because it is currently part of normal sheet Speed. If the condition later changes, the snapshot does not recalculate. An activated/timed movement buff does not count.

For each captured mode:

modeFloor = floor(normalModeSpeedBaseline / 2)

Apply compatible numeric bonuses, penalties and multipliers normally, then enforce that mode floor. It may therefore protect against numeric slows and Exhaustion 2's ordinary halving.

It does not defeat:

source Speed0/root;
Grappled/Restrained movement prohibition;
Exhaustion 5 Speed0;
Incapacitated or another voluntary-movement prohibition;
terrain movement costs;
absent movement modes.

A movement mode gained after the snapshot receives no Hypermutation floor. Butcherform itself supplies no replacement Speed here, so use the character's normal possessed-mode baselines. The common spent-movement ledger still applies when switching modes. 
Pasted text

Moment's Pause next-round displacement gets one stable, nonstacking initiative adjustment. Use the encounter's canonical initiative order as the snapshot, excluding temporary delay modifications.

On successful application:

record the target;
record its canonical snapshot order;
mark one pending one-step delay for the next numbered round;
multiple Moment's Pause delays on the same creature for that same next round do not stack.

At next-round construction, process pending delays in stable application sequence. For each delay:

find the first still-participating creature that followed the target in that captured snapshot;
ignore dead/removed participants while searching forward;
ignore new entrants that were not in the captured snapshot;
move the delayed target immediately after that surviving snapshot neighbor;
if no later snapshot participant survives, leave the target in its existing final position;
a creature may itself be delayed only once for that round.

Chained delays are processed in stable application order. A creature serving as another's snapshot neighbor may itself later move from its own pending delay; that is allowed and deterministic. No transformation can duplicate a turn, remove a turn, or alter preserved virtual duration/falling/recovery markers.

After that numbered round, all Moment's Pause slot modifications disappear and canonical initiative resumes unless another effect creates a new pending delay.

Slumber Glimpse's -2 initiative rider does not move an already-established slot. Store it as a one-use modifier to the next eligible initiative roll/initiative check before encounter end; if no such roll/check occurs, it expires at encounter end. 
Pasted text

Sanctify Ground's “end Staggered” removes the condition identity, not one arbitrarily selected source record. The card gives one cleansing choice between named conditions rather than “one source of” that condition. 
Pasted text

Therefore, with the new classification bridge:

Choosing Staggered ends all currently present records on that creature carrying classification.staggered, including Core Staggered, Monk Echoing Guard Stagger, and Warrior Brutal Strike Stagger.

This includes suppressed-but-still-present Staggered records, because a cure/removal operation is not an active-effect eligibility hook. Removing them deletes those records; they do not resume when suppression ends.

It does not remove unrelated records that merely impose -1 attacks or -5 Speed without classification.staggered.

A later new Staggered application after the cleansing can apply normally. There is no persistent immunity generated by the cure.

This differs deliberately from Bleed's reviewed “one selected record” Medicine/removal semantics because Bleed's source rules explicitly established record-scoped removal, whereas Sanctify Ground says to end Staggered as a named condition choice.

These corrections should replace the conflicting clock/binding statements in the addendum before review. Disease endpoints, resurrection/death replacement, and unsupplied object-durability dependencies remain open exactly as stated.