# GPT control counterexample review

Captured from the visible rendered Calibration Review reply.

The supplement is sufficient to bind all 40 attached normalized IDs without changing the original cards. The decisions below extend the existing source-qualified control registry; they do not close DD16 or claim exhaustive semantic coverage. 
Pasted text

Attached-source dispositions
Supplied source	Operational binding / disposition
crimson-agent.hero.shadow-operative.veinjammer	STATE crimson-agent.veinjammer.slow: hostile soft -5 ft, minimum 0, through target's next regular-turn end. Same-source reapplication refreshes, never adds another -5. Separate rider veinjammer.concentration-penalty: next concentration save -1, then consumed. A later legal Veinjammer application may create a new pending save rider after the old one was consumed; never more than one pending at once.
dragoon.hero.drake-rider.drakestorm-dive	Cold failure → STATE dragoon.drakestorm-dive.cold-slow, -10 ft through target next-turn end. Lightning failure → source-qualified Reaction denial through same target clock. Fire failure invokes its reviewed Burn profile, not a new generic Burning record.
dragoon.hero.drake-rider.elemental-lance	Cold hit → STATE dragoon.elemental-lance.cold-slow, -5 ft through target next-turn end; same-source refresh/no addition. Lightning is opportunity-attack denial until target next start, not universal Reaction denial. Fire's +1 is immediate damage, not Burn.

Those three source objects supply their explicit magnitudes and endpoints. 
Pasted text

Mage source	Operational binding / disposition
mage.base.elemental-bolt	Cold on-hit rider creates/refreshes mage.cold-focus:<owner> Bolt candidate, flat -10, or -15 with Arch Elemental Mastery. It applies on a legal hit even if cold damage is reduced to 0. It does not create a second candidate merely because the passive Cold Focus also triggered.
mage.base.cold.cold	Current-Cold-Focus engine. Passive candidate: actual positive damage from a qualifying Cold Mage spell → flat -10, Arch Mastery -15. Glacier failed save creates independent Glacier candidate in the same owner Focus group: half Speed; with Arch Mastery use NEW floor(preControlSpeed/2) - 5, floor 0. Glacier success does not create the Glacier candidate, but positive cold damage can still create passive candidate.
mage.arch.elemental-mastery	HOOK/modifier, not state. Upgrades Cold Focus flat reductions by another 5 and Glacier's Focus slow via the half-then-5 bridge. Does not affect non-Focus secondary slows.
mage.arch.elemental-surge	Cold hit explicitly applies the Focus reduction; same owner Focus group, -10/-15, even if actual damage becomes 0.
mage.hero.elementalist.elemental-fusion	Printed Fire+Cold or Cold+Lightning -10 is STATE mage.elemental-fusion.slow, separate from the Focus group and not Arch-Mastery upgraded. If current Focus is Cold and the spell deals positive cold damage, the Cold passive may separately produce its Focus-group candidate. Global soft-control arbitration picks the stronger result; they do not add.
mage.hero.elementalist.cascade-storm	Second-hit printed -10 = STATE mage.cascade-storm.cold-slow, separate/non-Mastery. If current Focus is Cold and that cold attack deals positive damage, Cold passive can additionally create its Focus candidate.
mage.hero.elementalist.elemental-mastery	HOOK only for Nuke Chain/off-Focus finisher permission. It does not grant another Focus passive, increase Cold reductions, or apply Arch Elemental Mastery's +5.
mage.hero.lich.undying-spellform	STATE/death-interface dependency. mage.undying-spellform.mobility-cap: while active at 0 HP, voluntary movement cannot exceed half Speed. This is a source-local self restriction, not hostile-soft arbitration. Remaining-conscious/death-save behavior stays in death-interface review.

The exact Cold Focus object distinguishes damage-triggered passive Slow from Bolt/Surge on-hit application, while the Hero Elemental Mastery limits itself to Nuke Chain eligibility. 
Pasted text

Monk source	Operational binding
monk.arch.tortoise.echoing-guard	NEW STATE monk.echoing-guard.stagger: -1 attacks, -5 ft Speed, target-next-turn clock. Same-source reapplication refreshes. Does not apply Core Staggered mechanics. Add metadata classification.staggered solely for actual readers.
monk.arch.pressure-point-strike	Failure creates one chosen component: monk.pressure-point.arm = -1 attacks, or monk.pressure-point.leg = hostile soft -10 ft; both through target next-turn end. A single use never applies both.

Pasted text

Oracle source	Operational binding
oracle.supplement.bones.ledger-s-command	STATE/control package. Initial failed save creates oracle.ledger-command.control for max 2 rounds. One commanded hostile Action can consume that Oracle/target hard-denial allowance. Once that allowance has been used, subsequent qualifying failed saves use the printed soft fallback only: Reaction loss + Speed0; no second commanded Action. Target-end saves are regular-turn saves.
oracle.supplement.bones.bones-revelation-mastery	HOOK. Enhanced Marrow Drain creates a -5 ft soft-control application when its underlying Marrow Drain qualifies. Does not itself create a slow without that Revelation.
oracle.supplement.cataclysm.tremor-sense	Failed STR → Core Prone only. Successful STR → oracle.tremor-sense.slow, -5 ft until source's next-turn end, because source says “your next turn.” No hidden slow on failure.
oracle.supplement.cataclysm.shardburst	Failed DEX → oracle.shardburst.slow, -5 ft target-next-turn clock; wall/rubble secondary STR failure may separately apply Core Prone.
oracle.supplement.cataclysm.gale-of-unmaking	Failed STR → push + oracle.gale-of-unmaking.slow, -5 ft target-next-turn clock. Difficult terrain is terrain cost, never part of the Speed record.
oracle.supplement.cataclysm.seal-s-fracture	Zone difficult terrain is not Speed. Ending Revelation backlash is a systemic self penalty oracle.seals-fracture.backlash: -1 attacks/saves, -5 ft, through source next-turn end. It does not enter hostile-soft arbitration.
oracle.supplement.dream.slumber-glimpse	Failed save: hard Action-loss component subject to Oracle guard + Reaction loss. Initiative -2 is a future-roll adjustment only. If guard already used, use printed fallback Reaction loss + Speed0 through target next-turn end. +2 next attack is its own consumable attack-roll rider.
oracle.supplement.life.resonant-seed	Undead failed STR on that entry/start pulse → oracle.resonant-seed.slow, -5 ft through that same regular turn end. Pulse max once/creature/numbered round.
oracle.supplement.time.moment-s-pause	Failed save: hard next-Action loss + Reaction denial, subject to hard guard. Guard-used fallback = Reaction loss + Speed0. Also source-specific one-step initiative delay next round, operationalized below.
oracle.supplement.time.the-spiral-opens	ECHO REVELATION is copy bookkeeping, not control state. FORCED ECHO against a non-player enemy is a source-qualified compelled-action hard-control event and consumes the hard-denial allowance; if that allowance was already consumed, that hard component fails because the card prints no NPC soft fallback. The player-controlled branch uses its own printed Reaction-loss + player choice/reduced-Speed procedure and is not replaced with an invented result.

Pasted text

Paladin source	Operational binding
paladin.supplement.oathbreaker-shared.black-manifestation	Failed WIS → paladin.black-manifestation.slow -10 ft + Reaction loss, ending at source's next regular start because “start next turn” is unqualified.
paladin.supplement.oath-of-dominion.law-s-weight	Failed save creates paladin.laws-weight.control: half-Speed + -2 AC + cannot benefit from Dash/Haste-like extra movement, through target's next start. Entry/start-of-turn saves are zone application pulses, not an invented end-turn repeat-save cycle.
paladin.supplement.oath-of-dominion.decree-of-submission	Submission mode = Core Charmed + one first-affected-turn command hard component. Later failed target-end repeat saves cannot command another Action; printed fallback = no Reactions + half-Speed until next turn. Dread mode = Core Frightened plus cannot willingly approach; no Oracle Dread binding.
paladin.supplement.oath-of-the-ancients.echo-of-ages	Initial qualifying hostile save failure → source-local attack denial, subject to common hard-denial guard. It does not remove movement/Actions generally. After this source-character has already hard-denied that target, a later actual qualifying failed save uses the printed Reaction-loss + half-Speed fallback. Do not invent a save each round; the source only triggers when first entering/being selected under the spell's actual trigger.
paladin.supplement.oath-of-the-ancients.standing-stone	Each hostile fey/elemental regular-start pulse may apply paladin.standing-stone.slow: half-Speed until its next regular start. No Action/Reaction loss.
paladin.supplement.oathbreaker-oath-of-the-chain.iron-leash-aura	Selected target has paladin.iron-leash-aura.slow: transform min(preControlSpeed, max(5, preControlSpeed-10)). Never raises a creature already below 5. Separate once/round voluntary-away movement rider can end that movement after 5 actual feet on failed STR; grants no free movement.
paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes	Failure → paladin.reign-of-ashes.ash-bound: half-Speed + no Dash + no voluntary teleport. “Until end of next turn” is unqualified, therefore source next regular-turn end under the combat convention. Not Restrained/Root.
paladin.supplement.oath-of-the-martyr-king.royal-decree	STATE one-turn compulsion, target clock. Target itself chooses Prone-kneel or safe movement toward source; retains Action and target choice. This does not consume the whole-Action hard-denial allowance because it neither removes nor replaces the Action. Ally morale/Frightened-save buff is a separate beneficial source-clock rider.

Pasted text

Shaman source	Operational binding
shaman.base.elemental-affinity	If Ice selected, actual positive cold damage to the first target on that owner's turn creates shaman.elemental-affinity.ice-slow: -5 ft, replaced by -10 ft with the already-reviewed Enhanced Elemental Attunement. Same-group refresh/no addition.
shaman.hero.theurgist.elemental-chorus	Each commanded pulse may choose one failed target to receive shaman.elemental-chorus.slow, -10 ft target-next-turn clock. Four spirits do not create four records.
shaman.hero.soothsayer.balanced-elements	HOOK/modifier. Once/turn choose one eligible owned shaman.elemental-slow record and extend its endpoint to the end of the target's following regular turn. It does not add magnitude or create a second record and cannot extend the explicitly excluded denial/silence/Stunned/concentration effects. Do not infer every Shaman Speed0 effect as “elemental” merely from ownership.

Pasted text

Thief source	Operational binding
thief.hero.shadowblade.vein-cutter	Preserve existing reviewed Bleed profile. Add separate thief.vein-cutter.slow -10 ft through target next-turn end and one -1 next attack damage rider expiring at same endpoint. Reapplication refreshes these components, never adds them.
thief.hero.blackguard.crippling-lash	Failed CON → thief.crippling-lash.slow -10 ft and one -1 damage on next weapon hit rider through target-next-turn end. It is not thief.crippled absent explicit source text.

Pasted text

Warrior source	Operational binding
warrior.base.brutal-strike	NEW STATE warrior.brutal-strike.stagger: -1 attacks, -5 ft Speed, target-next-turn clock. No Core Staggered mechanics imported. Add classification-only classification.staggered.
warrior.arch.mutation-overload	Backlash is a systemic self penalty, not hostile-control arbitration: -1 attacks, -1 saves, -5 ft through source's following regular-turn end.
warrior.supplement.stonecore	Serum-profile side effect -10 ft is a systemic profile penalty, suppressed by Serum Tolerance. It does not become a hostile slow merely because it is numerically negative.
warrior.supplement.hypermutation-spike	STATE/protection rule warrior.hypermutation-spike.speed-floor, operationalized below. Does not itself grant immunity to Grappled, Restrained, Root, terrain, or no-movement states.

Pasted text

Focused resolutions
1. Mage Cold Focus / Glacier / Fusion / Cascade

Confirm the proposed architecture.

One owner Focus group, multiple candidate subrecords

Use:

stackGroup = mage.cold-focus:<ownerCharacterId>

and retain magnitude-specific candidate records rather than destructively replacing one candidate with the most recent one.

Candidates can include:

cold-passive
elemental-bolt
elemental-surge
glacier-spike

At any evaluation, calculate each unsuppressed candidate's resulting Speed and use the lowest result. A weaker reapplication cannot make the target faster while a stronger unexpired candidate remains. When the stronger expires, an independently unexpired weaker candidate becomes effective again.

This is the same principle as retaining different-source clocks in the broader hostile-soft model.

Arch Mastery only

Yes:

Arch mage.arch.elemental-mastery modifies Cold Focus reductions.
Hero mage.hero.elementalist.elemental-mastery does not.

The Hero feature expressly changes Nuke Chain eligibility and off-Focus finisher choice, not Focus secondary magnitudes. 
Pasted text

Glacier formula

NEW confirmed:

Glacier candidate = max(0, floor(preControlSpeed / 2) - 5) with Arch Mastery.

Without Arch Mastery:

floor(preControlSpeed / 2).

Examples:

preSpeed 30, mastered passive = 15; mastered Glacier = 10 → Glacier wins.
preSpeed 10, mastered passive = 0; mastered Glacier = 0 → tie, no additive reduction.
preSpeed 5, unmastered passive = 0; Glacier = 2 → passive wins.
Positive-damage distinction

Cold Focus passive says a Cold Mage spell damages a creature. Therefore it requires positive actual damage.

Elemental Bolt says the Cold rider applies on a hit. It applies even if immunity reduces the actual cold damage to zero.

Elemental Surge likewise explicitly applies Focus reduction on a hit, so its reduction does not require positive actual damage.

Glacier Spike's failed-save half-Speed is save-based and does not depend on actual cold damage.

Fusion / Cascade and Cold passive

Yes, but only while Cold is actually the currently selected Focus.

A non-Focus-tagged Mage spell that itself includes a Cold damage component can trigger the Cold passive if:

Cold is the character's current Focus;
that spell is genuinely a Cold Mage spell/component under its printed card;
that target takes positive actual Cold damage.

Thus Fusion/Cascade can trigger the Cold passive when current Focus is Cold even though their own printed secondary slows remain separate non-Focus records.

The Hero Elemental Mastery statement that off-element spells “count as matching your current Focus for Nuke Chain eligibility” does not manufacture Cold-passive triggers when Cold is not actually the selected Focus. It grants chain eligibility only.

2. Hostile-soft arbitration, Iron Leash and Hypermutation

Confirm that hostile-soft means an adverse control record, not “an enemy applied it.”

A friendly creature, ally or the victim itself could originate an adverse-control record; ownership alignment is irrelevant.

Remain outside hostile-soft arbitration:

serum-profile side effects;
Mutation Overload backlash;
Oracle Revelation backlash;
serum/expedition Strain;
cargo penalties;
form-local mobility caps;
terrain movement cost.
Iron Leash

Use exactly:

result = min(preControlSpeed, max(5, preControlSpeed - 10))

Examples:

30 → 20
12 → 5
6 → 5
5 → 5
3 → 3, never 5.
Hypermutation Spike

Use a nonrecursive snapshot baseline.

NEW definition:

normalSpeedBaseline is captured when that Butcherform activation begins:

use the active form's printed base walking Speed if the form explicitly replaces walking Speed;
otherwise use the creature's ordinary base walking Speed;
include permanent base-Speed replacements that genuinely define that form/creature's normal Speed;
exclude temporary buffs, temporary penalties, Strain, cargo, terrain, conditions and control records.

Then:

hypermutationFloor = floor(normalSpeedBaseline / 2)

minimum 0 under normal fraction rules.

Resolve numeric Speed normally, including:

temporary Speed bonuses;
serum/expedition flats;
cargo;
hostile soft controls;
Exhaustion multiplier;
other compatible numeric reductions.

After those numeric changes, raise the numeric Speed to at least the Hypermutation floor.

It does not bypass:

an explicit Speed0 Root/state;
Grappled;
Restrained;
a rule saying voluntary movement is prohibited;
Incapacitated/other action-state restrictions;
terrain movement costs;
teleportation restrictions;
a mode the creature does not possess.

So it is protection against numeric slowing, not immunity to physical/magical immobilization.

This resolves the binding rather than deferring it.

3. Monk/Warrior “Staggered”

Confirm the two source-qualified identities:

monk.echoing-guard.stagger
warrior.brutal-strike.stagger

Neither applies core.staggered.

Each has:

-1 attack rolls
-5 ft Speed
target-next-turn endpoint
same-source refresh/no stack.

The attack penalty does not add across these two same-named custom Staggered records; use the strongest applicable Stagger-style attack penalty. Their Speed pieces already use hostile-soft arbitration.

There is an actual reader: Paladin Sanctify Ground can cleanse “Staggered.” 
Pasted text

Therefore add classification metadata:

classification.staggered

to:

Core Staggered;
Monk Echoing Guard Stagger;
Warrior Brutal Strike Stagger.

That classification exists only for readers/removers explicitly written to affect Staggered. It imports none of Core Staggered's Guard-removal/forced-movement mechanics into the custom records.

4. Divine Judgment and extra turns

Correct the prior overbroad regular-turn interpretation.

Divine Judgment says:

“The first time on each of its turns that it deals damage…” 
Pasted text

Therefore:

Every actual turn, including a legally granted extra turn, has its own Divine Judgment reflection opportunity.

It is not restricted to regular turns.

The regular-turn normalization remains limited to:

repeat saves;
duration expiry;
periodic/control clocks;
recharge/recovery systems already specifically reviewed.

It must not be generalized to every “once on your turn” or “each turn” feature.

Trigger

Divine Judgment triggers only when the marked creature causes positive actual damage to another creature on that turn.

Actual damage 0 → no reflection despite the printed minimum-1 reflected amount.

Multiple creatures damaged simultaneously

NEW deterministic rule:

For a single simultaneous attack/effect damaging several creatures:

use the source effect's printed target-resolution order if one exists;
otherwise use target declaration/list order fixed before resolution;
for an unordered area, establish stable target application sequence before applying damage;
the first recipient in that order to take positive actual damage supplies the reflection magnitude;
do not sum damage across victims.

The mark then records that turn's reflection opportunity as spent.

Off-turn damage creates no reflection because it is not occurring on the marked creature's turn.

5. Guiding Bolt, Wrathful Brand, Drake Mark, Soldier mark, scanner
Guiding Bolt — accept two-rider model

NEW clarification:

oracle.guiding-bolt.star-mark has:

nextAllyAttackBonusAvailable = true
nextAllyHitDamageAvailable = true.

First qualifying attack by an ally other than the Oracle:

receives +2;
consumes only the attack-bonus rider whether hit or miss.

If it misses:

the mark remains;
the next qualifying ally hit before expiry adds S radiant;
that hit consumes the hit-damage rider and ends the mark.

If the +2 attack itself hits, it receives the +2 and S damage and consumes the mark in that one resolution.

Reapplication creates a fresh paid star-mark and resets both riders; no stacking/backfill. The source supplies the attack/hit distinction. 
Pasted text

Wrathful Brand

Accept one shared ally-trigger entitlement per Brand.

The first ally event that deals positive actual damage to the branded target:

consumes the ally-trigger entitlement;
the ally attempts the printed 1d6 healing;
the target makes the one WIS save;
failure creates the -1 attacks rider.

If actual healing is prevented, capped at full HP, or reduced to 0, the entitlement remains consumed. It is not refunded.

The owner's separate “next damaging attack you hit” rider requires the owner's attack to deal positive actual attack damage before the bonus fire is added. A hit whose base attack packet is completely negated does not unlock the bonus.

Drake Mark

Its wording is “first subsequent direct polearm hit.”

Therefore that hit consumes the mark even if actual damage after mitigation is zero. The S bonus is then part of resolving that qualifying hit.

Soldier Marked for Death

“First hit” damage reduction is consumed on the first qualifying hit against another ally, even if the resulting damage becomes 0.

Tinker Target Scanner

“First ally attack” means the first qualifying attack roll:

grants +1;
consumes the scanner mark on that roll;
hit/miss does not change consumption.
6. Carrion corpse lock and disease immunity

Confirm.

Carrion Conductor

Use two distinct records:

temporary carrion-conductor.corpse-mark
persistent source-specific history carrion-conductor.used-corpse:<corpseIdentity>.

The used-corpse history survives:

mark consumption;
mark expiry;
suppression.

It means only “this corpse cannot be used again by Carrion Conductor.” It creates no universal corpse-reuse rule for resurrection, harvesting or other abilities.

Disease immunity

Disease immunity is not cure.

For an already-present covered disease:

mechanical penalties/components covered by that immunity are suppressed;
the disease record persists;
its ordinary duration/progression clocks continue unless that disease specifically says immunity pauses progression.

Do not universally suppress a lethal disease endpoint merely because symptoms are currently suppressed.

Each lethal/progressive disease therefore needs source metadata describing whether immunity:

blocks progression;
blocks its endpoint;
merely suppresses active penalties.

No immunity can resurrect a creature after a lethal endpoint.

Detection/classification likewise comes from actual metadata, never the word “disease,” “plague,” “infectious,” “curse,” “hex,” etc. in names/flavor.

7. Physical restraint fallback / suppression / teleport

Confirm the stricter fallback gate:

A fixed sufficient endpoint by itself excludes the NEW physical-restraint escape fallback.

That is intentional.

Do not add:

helper escape;
cutting;
generic object HP;
repeated saves

to a source that already supplies a complete magical endpoint and does not authorize those methods.

Magical restraints

No generic helper/cutting endpoint for purely magical restraints.

Earthen Grip

The operational spell says:

ground contact is required to be a legal initial target;
on failure it becomes Restrained;
concentration/end-time/Action escape are explicit. 
Pasted text

It does not say:

leaving that original square ends the spell;
breaking contact with the original patch of earth ends it;
teleportation automatically breaks it.

Therefore do not invent such a relation. A legal teleport does not automatically end Earthen Grip; if the creature teleports while the Restrained condition is otherwise still legally present, the magical restraint persists until an actual printed endpoint occurs.

Reach-dependent restraints

Where a source expressly requires reach/attachment maintenance—Tyrant's Impale is the clear example—suppression does not freeze relation validation.

If suppression permits movement and the target moves beyond required reach:

source relationship becomes invalid;
restraint source ends permanently;
it does not resume when suppression ends.
Physical attached nets

A suppressed physical net stays attached unless:

destroyed;
removed;
its printed duration expires;
another actual endpoint ends it.

If suppression ends while it is still attached and within duration, the Restrained component can resume.

8. Hard-control composites and omitted command sources

Yes:

A consumed source-character/target hard-denial allowance prevents only a future hard component. Apply an expressly printed soft fallback if one exists. If the source prints no fallback, do not invent one.

That principle resolves the omitted sources as follows.

Ledger's Command

Initial hostile control may command one Action and consume the Oracle hard-denial allowance.

After that allowance is spent, later failed saves use its explicit:

Reaction denial;
Speed0;

instead of another commanded Action.

No invented second denial.

Slumber Glimpse

First legal hard failure:

next Action loss;
Reaction loss;
initiative rider;
attack-bonus vulnerability rider.

After guard consumed, future failure uses only the printed:

Reaction loss;
Speed0.
Moment's Pause

Same hard/fallback split.

NEW initiative-step implementation: when the effect successfully applies its delay, snapshot the current ordered initiative list. For the next numbered round only, move that target one active slot later by swapping it with the next active participant in that ordered list. If it is already last, it remains last. After that round it returns to its ordinary established slot.

This temporary reorder does not rewrite pre-existing virtual duration/falling/recovery markers; those keep their preserved clocks.

The Spiral Opens

For FORCED ECHO against an NPC:

failed save's forced-action pattern is an equivalent hard-control event;
it uses the hard-denial allowance;
if that allowance is already spent, the forced-action component fails because no NPC soft fallback is printed.

For player-controlled targets, use the card's explicit player branch exactly; do not replace it with the NPC procedure.

Decree of Submission

Submission:

Core Charmed remains an ongoing condition;
only the first affected-turn commanded Action is the hard component;
later failed target-end saves use the printed Reaction-loss + half-Speed fallback, not another command.

Dread:

Core Frightened;
no-approach restriction;
repeat target-end save.

Do not bind Dread to Oracle Dread.

Echo of Ages

An actual qualifying save can impose attack denial once under the shared hard guard.

After that target has already suffered that source-character's hard denial, a later actual failed trigger/save uses the printed Reaction-loss + half-Speed fallback.

Do not invent a start/end-turn repeated save merely because concentration continues.

Reign of Ashes

Ash-bound is wholly soft:

half-Speed;
no benefit from Dash;
no voluntary teleport.

It does not consume the hard-denial allowance and does not become Restrained/Root.

Per-round zone pulses vs repeat saves

Keep these event types distinct:

“enter/start each round/turn and save” = new source pulse/application check;
“repeat the save at end of turn” = existing-record ending check.

Extra turns do not manufacture extra regular-clock repeat saves, but a source explicitly written to trigger on each actual turn can trigger on an extra turn unless that source or a reviewed cap says “regular turn” or “once per round.”

The registry therefore records trigger cadence per source; it is not a universal command/spell automation engine.

Remaining bounded dependencies

The supplement resolves the requested 40 attached IDs, but several broader dependencies remain intentionally open: actual disease-producing source catalog and lethal-disease endpoint metadata; non-spell curse rank/tier metadata; complete physical-object/tether durability outside already printed nets; Death Ward/Undying Spellform/resurrection interaction with the closed death and Strain-6 rules; and the remaining all-source semantic scan.

No original normalized card needs to be altered for these dispositions. DD16 remains open pending Codex's implemented registry, counterexample tests, and the semantic remainder.