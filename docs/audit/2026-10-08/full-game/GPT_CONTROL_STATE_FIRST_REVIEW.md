# GPT control-state first review

Captured from the visible rendered Calibration Review reply.

The 179-source packet supports a source-qualified control registry, not a universal dictionary of capitalized words. I would implement the common rules below first, then bind the supplied sources exactly as classified in the tables. This remains a bounded DD16/control-state pass; the packet itself explicitly says the lexical scan is not proof of exhaustive semantic coverage. 
Pasted text

Common operational decisions
1. Speed-control records: NEW non-additive hostile-control model

Keep four mechanically distinct things:

soft flat reduction · soft fractional/custom reduction · Speed 0 control · Core Grappled/Restrained.

Terrain is never a Speed record; it changes movement cost, not Speed.

Every hostile soft Speed effect gets a source-qualified record containing its owner, source, duration, stackGroupId, magnitude/transform and suppression state.

NEW stacking rule: same-group records obey their printed refresh/cap rules. Across different hostile soft-Speed groups, retain all records and clocks, but do not add the reductions together unless a source explicitly says they stack. Instead:

Calculate preControlSpeed after the creature's ordinary Speed bonuses/penalties such as serum Strain, expedition Strain, cargo, stances and other already-approved flat modifiers.
Evaluate each unsuppressed hostile soft-control record independently against that same value.
flat -10 → max(0, preControlSpeed - 10)
half Speed → floor(preControlSpeed / 2)
custom transform → its exact formula
Use the lowest resulting Speed. All losing records remain active with their own expiry.
Apply separately established global multipliers afterward, such as Exhaustion's half-Speed.
Any active effect that actually sets Speed to 0 then overrides the result.

Thus two unrelated -10 slows do not become -20 merely because namespacing preserved both sources. A -10 and half-Speed on Speed 30 produce 15, not 10. Exhaustion 2 would then halve 15 to 7. Independent serum/expedition penalties still combine because those were separately reviewed systemic penalties, not members of this hostile-control arbitration.

Any explicit adverse soft Speed reduction or source-specific Speed-0 control receives eligibility.slowed-foe. Core Grappled/Restrained alone do not, preserving the already-approved Snow Leopard boundary. A suppressed record does not qualify; a merely numerically overshadowed record remains active and can still qualify. 
Pasted text

Mage Cold Focus

Use one owner stack group such as:

mage.cold-focus:<ownerCharacterId>

A single hit that invokes both the Fire/Cold Focus passive and a Focus card's Cold rider creates one Cold-Focus slow record, not two penalties.

Elemental Mastery makes an ordinary Focus -10 ft reduction become -15 ft.

For Glacier Spike, I would use this NEW fractional bridge if its active card is confirmed Focus-tagged:

max(0, floor(preControlSpeed / 2) - 5)

That treats Mastery's “another 5 feet” as part of Glacier Spike's single slow profile rather than creating a second stacking record.

However, the attached 179-object packet does not contain the active Mage Cold Focus/Glacier Spike object; its Mage records here are the Lich-risk engine, Purifying Beam and Undead Immunities. So this rule can be agreed provisionally, but the Glacier binding itself cannot yet be marked SOURCE-AUDITED from this packet. Cascade Storm remains excluded from Mastery unless an actual active source gives it the Focus tag.

2. Speed 0 / Root

Root remains a semantic family only when the operative source actually calls the effect Root/rooted.

Its mechanical payload remains:

Speed = 0

and nothing else.

It does not inherently:

Restrict;
Grapple;
remove Actions;
remove Reactions;
prevent teleportation.

Other sources that set Speed 0 without calling it Root get their own source-qualified speed.zero record but no invented Root label.

Multiple Speed-0 records coexist independently. Speed remains 0 until no unsuppressed record that sets it to 0 remains.

3. Restrained/Grappled and physical escape fallback

Card-specific application/save/escape rules always win.

The following NEW fallback should exist only for a genuine physical Restrained source that:

supplies no escape method;
supplies no sufficient fixed endpoint;
is not marked special-cure-only.

Fallback:

The affected creature may spend an Action and make STR (Athletics) or DEX (Acrobatics) against the applying source DC; if no DC exists, use DC 10. Success ends that selected restraint record only.

An adjacent helper may spend an Action and attempt STR (Athletics) against that same DC. A helper does not generically use Acrobatics to free somebody else.

Cutting/breaking a net, chain, tether or object requires an actual durability/object rule. If none exists, do not invent one.

Teleportation uses the relationship actually printed:

a reach/tether restraint ends if teleportation breaks a required reach relationship;
an attached net/shackle normally travels with the target;
a magical restraint does not automatically disappear from teleportation unless its source relation is actually broken.

No generic anatomy or size restriction is added beyond the source and actual creature immunity.

None of the supplied Restrained applications needs this fallback right now; every relevant active source here already has a duration, repeat save, escape Action, breakable object, or other endpoint.

4. Marks are never generic by name

Every actual mark gets its own ID and metadata:

ownerCharacterId, target type, maximum active targets, duration clock, consumed riders, eligibility hooks.

A custom mark does not automatically apply Core Marked and never satisfies another class's mark prerequisite merely because both display “Mark.”

Trigger semantics:

“next attack” → that rider is spent when the qualifying attack roll occurs;
“next hit” → spent only on a qualifying hit;
“when damaged” → requires actual positive damage unless the source expressly says otherwise;
consuming one rider does not erase other riders or the mark itself unless the source says the mark ends.

Bare hostile N rounds marks use the already-closed target-turn clock. Explicit source/user endpoints remain source clocks.

Important bindings:

Mechanical ID	Exact binding
cleric.balanced-scales.mark	One allied record per healed ally; expires source's next regular start. First enemy that actually damages the ally triggers the retaliation once. Rehealing refreshes, not duplicates.
cleric.divine-judgment.mark	Target record under concentration/max 3 rounds; first actual damaging event on each target regular turn reflects half actual damage within printed bounds; target regular-end WIS save ends it.
crimson-agent.blood-mark	Already reviewed: one living target; 5 owner regular turns; technical Crimson-engine mark only.
crimson-agent.carrion-conductor.corpse-mark	Corpse-only marker, not creature Marked. Reaction burst consumes it. NEW: once a corpse receives this marker, that corpse is ineligible for another Carrion Conductor use even if the marker expires unburst, matching “corpse cannot be reused.”
dragoon.drake-mark	One target; new one replaces old; source-clock endpoint. First subsequent direct polearm hit consumes the mark and adds S. Triggering leap itself cannot consume it.
oracle.mark-of-the-doomed	Already reviewed; one active. Critical rider is separate from the persistent attack bonus/concealment rider.
oracle.wrathful-brand	One active Brand. Owner's next damaging attack hit consumes only its fire-damage rider. First ally-damage trigger consumes only its once-per-Brand healing/save rider. Brand itself may remain until expiry.
oracle.guiding-bolt.star-mark	One per creature per owner; max 2 target rounds. NEW: the first qualifying ally attack receives +2. That attack consumes the +2 opportunity whether it hits or misses. If it hits, add S radiant and consume the mark; on a miss the mark may remain until expiry but its attack-bonus rider is spent.
oracle.constellation-mark	Up to 2 targets, 3 with the printed mastery; recast ends the previous set. +1d6 is once per numbered round across the whole marked set, not once per target.
oracle.omen-reader.star-ash	One nominated enemy; -2 is applied to the triggering attack once, then star-ash remains through target next turn granting allies +1 attacks.
Paladin Vengeance family	Keep the three already-reviewed application IDs; shared owner-qualified Vengeance eligibility only. Judgment Brand's bare 3 rounds use target-end markers.
paladin.linked-ward.link	Willing-ally concentration link, not generic Marked.
paladin.chain-of-duty.link	Willing-ally concentration link, not generic Marked.
paladin.grief-mark	Already reviewed source identity.
ranger.track-target.quarry	One quarry at a time, 1 minute; new quarry replaces old.
ranger.pathfinders-mark.location	One fixed point, 24 hours; non-creature navigational state.
ranger.predators-mark.upgrade	Upgrade on the existing quarry; not a second independent target mark. Ending concentration leaves the underlying quarry mark.
soldier.marked-for-death	One active target. Save penalty persists to expiry; first-hit damage reduction rider is spent separately.
tinker.target-scanner.mark	First ally attack roll before source next turn gains +1; consume that scanner record after that attack roll, hit or miss. No generic Marked.
wizard.binding-sigil.mark	One active target, source-next-turn clock; advantage only on Wizard spell attacks.
wizard.gravebrand	Source-qualified necrotic mark/DoT, not generic Marked and not automatically a curse.
Mirrorsage archive “marks”	Source bookkeeping only, never creature conditions.
Monk hard-denial “marks”	Encounter-history bookkeeping per Monk/target, not target conditions.
Warrior Vulnerable	Already-reviewed eligibility flag, not damage vulnerability or Core Marked.
5. Curse and disease classification

Use:

classification.curse
classification.disease

as metadata on actual affliction records, not conditions with an inherent penalty.

This packet contains no new source that actually inflicts a generic curse or disease.

Notably:

Oracle's selected Curse is oracle.intrinsic-curse, explicitly protected from ordinary curse removal. It is not classification.curse. 
Pasted text
Soul-Cracked/False Life and Curse Boons remain Oracle class-engine states.
Wizard Infernal Pact is a pact/quest unlock; Gravebrand is its own mark, not automatically a curse.
Shaman's word hex in “necrotic/hex damage” is a Shaman source-category hook, not a curse application.
Plague Bearer explicitly says it is not a transmissible permanent disease.
Infectious Mutation explicitly says it is not a disease.
Blood Curse's name still does not create classification.curse.

Disease records should eventually expose:

magical, ordinaryMagicallyCurable, specialCureRequired, allowsSave, repeatSaveProcedure, treatmentDC.

A feature saying “repeat one disease save” grants no new save if the disease itself has none.

NEW disease-immunity bridge: an explicit disease immunity blocks covered new disease applications and suppresses the mechanical effects of covered existing disease records while immunity lasts; their clocks continue. It does not delete/cure the record unless the feature says it does. Source scope matters: Ranger Toxic Affinity covers nonmagical disease only; Purifying Crown covers ordinary disease; Lich/Nature's Ward state broader disease immunity.

Wizard detection:

Analyze Magic: on successful analysis may report that a magical effect is cursed only if the inspected effect actually exposes curse metadata and that information is not protected.
Arcane Sight: later focused examination may likewise report cursed/linked status on an eligible visible aura.
Identify expressly does not automatically reveal curses.
Detect Magic and Aura Glimpse reveal aura presence/category only within their printed information ceilings.
Oracle intrinsic Curse protections remain controlling; generic Wizard detection does not silently overcome them. 
Pasted text
 
Pasted text

A real remaining dependency is curse tier/removability. Cleansing Brand references an ordinary curse-removal effect “of this tier,” but this packet does not establish a universal tier for every non-spell curse. Spell-created curses may use an explicit spell rank; other curses need source metadata. Do not invent a tier just to make the cleanse succeed.

6. Suppression and multi-component effects

Immunity/suppression acts only on the component it actually covers.

Example: Word of Binding contains:

Core Silenced + Speed 0

If a creature becomes immune to silence, the Speed-0 component can continue. A speed-control immunity does not automatically remove Silenced.

Suppressed control records:

keep their original clocks;
do not apply penalties;
do not satisfy active hooks such as slowed-foe;
resume if suppression ends before the source record expires.

Ending/suppressing a Grapple or Restrained condition does not erase unrelated damage or marks from the same card.

7. Repeat-save and source-control timing

NEW normalization: a class/spell control effect saying “at the start/end of each turn” for the affected creature means its regular turn for repeat-save/control-clock purposes. Extra turns do not manufacture extra saves, pulses, control expiry, or resource opportunities unless the source explicitly says they do.

Zones with an explicit once per creature per round use their printed numbered-round cadence. A creature overlapping two different source records is not globally immune to both; apply each source's actual cadence and any same-source cap.

Composite control states remain separate internally:

Word of Binding: Silenced + Speed 0, one repeat save ends both.
Nerve Strike: choose Speed 0 or Reaction + Bonus Action denial.
Bone Whisper fallback: Reaction denial + Speed 0, not Incapacitated.
Iron Leash: Speed 0 + Reaction denial; optional one-target Action denial only where the hard-denial allowance is legal.
Mental Binding: Charmed persists separately from its first-turn command.
Arcane Domination: Charmed, no-Reactions, and its one commanded-turn rider are distinct.
Mind Prison: first-turn Incapacitated is the hard denial; later half-Speed/no-Reactions are soft riders.

The shared source-character/target/encounter hard-denial guard remains controlling and does not get reset by giving a rider another name. 
Pasted text

Classification of all 179 supplied references

Legend: STATE = bind source-qualified state/control record; APPLY = applies an already-defined Core condition; HOOK = reader/modifier/cure/immunity only; BOOK = subsystem/history bookkeeping, not a creature condition; NONSTATE = lexical false positive; DEFER = a separate unresolved system owns it; ALREADY = previously reviewed binding.

Owner	Supplied IDs / engine indices and disposition
Cleric	cleric.base.judging-light — HOOK for classification.curse / weakened eligibility. cleric.base.judgment.judgment — ALREADY cleric.judged. cleric.hero.saint.celestial-resurgence — DEFER resurrection/death; “curse” is non-removal text only. cleric.hero.priest.balanced-scales — STATE cleric.balanced-scales.mark. cleric.hero.priest.word-of-binding — STATE composite Core Silenced + source-qualified Speed0. cleric.hero.priest.divine-judgment — STATE mark. cleric.hero.cultist.ritual-of-undeath — DEFER Death Ward/death-replacement plus companion mode; its “mark” is not generic Marked.
Crimson Agent	engine[3] — ALREADY Blood Mark engine. engine[6] — BOOK acquisition only. crimson-agent.base.blood-mark — ALREADY. crimson-agent.arch.rupture-trigger — ALREADY Bleed application. crimson-agent.arch.rupture — HOOK/consumer of Blood Mark. crimson-agent.hero.bloodweaver.purify-blood — HOOK Poisoned/disease cure. crimson-agent.hero.shadow-operative.phantom-strike — ALREADY Blood Mark exception. crimson-agent.hero.thirstborn.hemorrhagic-plague — ALREADY Crimson Bleed. crimson-agent.hero.thirstborn.carrion-conductor — STATE corpse marker.
Dragoon	dragoon.base.draconic-discipline — HOOK save advantage vs Prone/forced movement. dragoon.hero.dragon-guardian.aegis-leap — NONSTATE intercept movement. dragoon.hero.drake-rider.drake-mark — STATE source-qualified mark. dragoon.hero.dragon-tyrant.tyrant-s-impale — STATE Core Restrained with printed escape/reach ending + ALREADY Dragoon Bleed.
Druid	engine[6] — BOOK circle summary, no state. druid.base.panther-form-stealth — STATE card-specific Grappled; one held target, Action escape vs Druid DC, separation/reversion endpoints. druid.hero.timeless-body — NONSTATE disease explicitly not prevented. druid.hero.land.nature-s-ward — HOOK Charmed/Frightened/Poisoned/disease immunity. druid.hero.land.tanglemaw — STATE Core Restrained with source escape/endpoint. druid.hero.thorns.tanglemaw — STATE Core Restrained plus its printed damage rider. druid.arch.winterfang.winter-s-embrace — STATE soft -10 ft record. druid.hero.winterfang.snow-leopard — HOOK eligibility.slowed-foe. druid.hero.rotshaper.carrion-rat-king — APPLY Core Poisoned; its disease immunity is a separate self hook.
Mage	engine[16] — NONSTATE/DEFER irreversible Lich transformation stakes; “cursed” wording is not classification.curse. mage.hero.archmage.purifying-beam — HOOK cleanses listed Core conditions only and explicitly not curse/disease. mage.hero.lich.undead-immunities — HOOK poison/Poisoned/disease/Frightened/Charmed/magical-sleep immunities.
Mirrorsage	mirrorsage.hero.light-weaver.light-binding — STATE magical Core Restrained; target repeat save, source-next-turn maximum. mirrorsage.hero.light-weaver.purifying-reflection — HOOK reroll existing save, no state record. mirrorsage.hero.mirror-mage.reflected-repertoire — BOOK archive-record retention markers only.
Monk	engine[8], engine[18] — BOOK per-Monk hard-denial history marks. monk.base.stunning-strike — APPLY Core Stunned or printed reaction-loss fallback. monk.hero.enlightened-master.serenity-breaker-palm — HOOK condition cleanse. monk.hero.enlightened-master.healing-touch — HOOK healing/repeat existing Poisoned-or-disease save. monk.hero.enlightened-master.purifying-palm — HOOK cleanse. monk.hero.way-of-shadow.nerve-strike — STATE choice: source-qualified Speed0 or Reaction+Bonus Action denial.
Oracle engines/shared	engine[2], [15], [16], [17], [21], [22], [24] — BOOK progression/resources. engine[3] — BOOK protected one-Curse rule. engine[20] — STATE self-only Curse Manifestation buff/debuff, not classification.curse. oracle.supplement.shared.oracle-s-curse, oracle.supplement.shared.oracle-s-burden, curse-boon-i, curse-boon-ii, curse-boon-iii, curse-boon-iv, curse-boon-v — BOOK intrinsic Oracle Curse progression, not ordinary curse. ability-score-improvement-oracle-4 — NONSTATE. curse-manifestation — STATE self class-state, not generic curse.
Oracle curse cards	spiral-touched-boon-ii — HOOK advantage vs aging/slow/time plus explicit extra Action; no Slow state. oracle.supplement.curse.soul-cracked — BOOK intrinsic Oracle Curse, not ordinary curse. soul-cracked-boon-v — HOOK external curse/geas/possession removal. burning-blood-boon-i — NONSTATE immediate retaliation/resistance. burning-blood-boon-ii — ALREADY periodic-fire extinguish modifier. oracle.supplement.curse.false-life — BOOK protected intrinsic Curse/healing gate, not ordinary curse.
Oracle Battle/Bones/Flame/Life	mark-of-the-doomed — ALREADY source mark. bone-whisper — STATE hard Incapacitated attempt with guard; fallback Reaction denial+Speed0. ledger-s-memory — HOOK identification only. wrathful-brand — STATE Brand mark with two separately consumed riders. purging-flame — STATE undead -1 attacks rider + HOOK Poisoned/disease handling. zealot-s-renewal — HOOK Poisoned/disease repeat + fire ward. thorned-shelter — STATE beneficial shelter plus retaliatory source-qualified Speed0. garden-of-restoration — STATE zone; undead -1 attacks soft rider + HOOK Poisoned/disease. bloom-oracle — HOOK diagnosis only. life-revelation-mastery — HOOK disease-curing upgrade.
Oracle Shadow/Stars/Time	marquis-s-glimpse — STATE hard denial attempt; later fallback Reaction loss+Speed0. guiding-bolt — STATE star-mark. constellation-mark — STATE owner mark set. omen-reader — STATE star-ash mark. concord-alignment — beneficial source aura/HOOK affecting mark ranges, not a target mark itself. stars-revelation-mastery — HOOK mark upgrades; Enhanced Guiding Bolt creates a source-qualified -5 ft slow record. rewind-wound — HOOK exact-event finite-condition remover, excludes curse/Wound/death/permanent transformation. paradox-skin — HOOK save advantage/reroll against actual Slow/time effects.
Paladin base/common	engine[2] — HOOK disease-save advantage, not immunity. lay-on-hands — HOOK Poisoned end / repeat legal disease save. sacred-touch — HOOK presence detection for ordinary curse/disease records; no origin/cure. divine-health — HOOK disease-save advantage. sanctify-ground — HOOK listed Core cleanses or repeat legal finite disease/curse save.
Paladin Vengeance	vengeful-smite, judgment-brand, mark-of-retribution — ALREADY three Vengeance mark IDs. aura-of-judgment, relentless-pursuit, sentence-of-doom, no-escape, final-verdict — HOOK/STATE dependent on an existing owner-qualified Vengeance mark; none creates a new generic mark. judgment-brand bare 3 rounds uses target-end clock. sentence-of-doom is a consumable empowerment record, not Marked. final-verdict HP-recovery prohibition is its own timed rider.
Paladin Dominion/Flame	binding-word — STATE magical Core Restrained with its own repeat-save/max-2-round procedure. purifying-smite — HOOK dispels removable beneficial magical states; not curse classification. aura-of-purification — HOOK disease saves + source pulse. holy-inferno — HOOK cure. cleansing-brand — HOOK ordinary/tier-eligible curse removal; curse-tier metadata remains dependency. zealot-s-flame — HOOK disease cleanse. sanctified-immolation — HOOK removable curse/disease cleanse. purifying-crown — HOOK Poisoned/ordinary-disease immunity plus damage pulse.
Paladin Ancients	ancient-smite — STATE Root/Speed0. thorn-crown — HOOK reflection of the exact eligible finite condition; does not create a universal reflected-condition definition. roots-of-memory — STATE Core Restrained with fixed endpoint; no fallback escape added. primordial-surge — STATE Root/Speed0. primordial-crown — HOOK/STATE spreads the Ancients Root profile; hostile attack-target restriction is a separate source-local control rider, not Charmed.
Paladin Chain / Grief / Chains Broken	linked-ward — STATE ally link, not generic mark. chain-of-duty — STATE ally link, not generic mark. iron-leash — STATE Speed0 + Reaction loss; optional one-target Action denial under hard-denial guard. mourning-smite — ALREADY Grief Mark. sorrow-s-weight — STATE half-Speed soft record. liberating-smite, aura-of-liberation, righteous-quake, break-bonds, shatter-shackles, revolution-s-cry, unbound-host, liberty-unbound — HOOK source-specific Grapple/Restrained suppression, escape, removal or immunity; do not create a new generic condition. reign-of-ashes-aura — STATE hostile -5 ft soft Speed record plus source-specific suppression of newly applied movement/escape buffs.
Ranger	engine[0] — STATE quarry mark engine. engine[4] — binds source-specific Arrow riders; Glacial Thorn is a Speed0 control record, not generic Restrained. ranger.base.track-target — HOOK benefits of existing quarry. pathfinder-s-mark — STATE one location mark, non-creature. predator-s-mark — STATE upgrade on current quarry, not a new target mark. rootcall-quake — STATE Speed0 with printed target-end repeat save and Action Athletics escape. toxic-affinity — HOOK Poisoned/nonmagical-disease immunity. venom-rain, plague-bearer — APPLY Core Poisoned; neither creates disease.
Shaman	engine[1] — STATE Frost soft slow; hex there is a Shaman source/damage hook, not classification.curse. engine[4] — source profiles for Burn, Root/Speed0, Weaken, Reaction denial/Stunned etc. shaman.base.flask-use — BOOK invokes those exact engine profiles; no duplicate state. enhanced-elemental-attunement — HOOK modifies the existing affinity slow, does not add another record. summon-ice-wisp — STATE source-qualified Speed0 on failed STR save.
Soldier	engine[1] — STATE Snare -10 ft; periodic Bleed remains in closed registry. suppression-fire — STATE -10 ft. hold-the-line — STATE Speed0. guardian-s-rush — NONSTATE supplied movement/DR reaction. divine-lockdown — STATE failure Speed0+Reaction loss, success -10 ft. net-bolt — STATE physical Core Restrained with printed Action/durability ending; Huge+ gets soft -10 instead. marked-for-death — STATE one source-qualified mark.
Thief	thief.arch.crippling-strike — STATE half-Speed soft slow; explicitly not thief.crippled.
Tinker	engine[3] — source profiles including STATE Target Scanner mark, Target Taunter targeting penalty, Poison Vents attack penalty and Core Stunned application; Burn already handled separately. engine[5] — STATE Cryo Speed0, Shock verbal-casting block/construct Reaction loss, Glue soft slow; immediate push is not persistent state. engine[6] — STATE Net Trap Restrained profile; other deployables retain their own object/zone rules. bomb-specialization — HOOK increases Glue's existing slow, not a second slow. deploy-net-trap — STATE the same Net Trap profile, not a duplicate record beside engine[6]. overpressure-bombs — NONSTATE immediate push/Prone rider.
Warrior	brutality-sense, brutality-momentum — ALREADY Warrior Vulnerable eligibility/snapshot. stabilizing-injection — HOOK cure/repeat legal disease save. cellular-reconstruction — ALREADY source stasis plus printed disease cure. infectious-mutation — STATE one-use -1 next attack OR saving throw; explicitly not disease. shoulder-spike-cluster — HOOK grapple-establishment/maintenance damage trigger, no new grapple state.
Wizard	engine[15] — BOOK matrix preparation/linking markers, not target states. analyze-magic, arcane-sight — HOOK magical metadata detection under the curse/link boundaries above. sigil-authority — HOOK existing Core conditions, does not create them. runic-snare — STATE magical Core Restrained with printed end-turn STR repeat. will-domination — APPLY Core Stunned, with hard-denial fallback Reaction loss. binding-sigil — STATE one source-qualified mark. infernal-pact-quest-based-unlock — STATE Gravebrand mark/periodic necrotic effect; Pact itself is not ordinary curse metadata. mental-binding — STATE Charmed + one first-turn command rider. arcane-domination — STATE Charmed + persistent Reaction denial + once-per-effect commanded-turn rider. mind-prison — STATE first-turn Incapacitated hard denial, then half-Speed + no Reactions while concentration continues.
Ordinary spells	dispel-minor — HOOK eligible rank-0/cosmetic effect removal; mentioning marks does not create Marked. seal-minor-wound — ALREADY one eligible ordinary Bleed removal. earthen-grip — APPLY Core Restrained with its explicit Action escape. elemental-bolt — NONSTATE here: damage choice only; this ordinary spell is separate from Mage class Elemental Bolt and creates no slow/Burn. aura-glimpse — HOOK aura presence only. identify — HOOK public magical properties and explicitly not hidden curses. detect-magic — HOOK aura/category detection only. ray-of-frost, frost-arrow — STATE independent -10 ft soft Speed records, self-refreshing and nonstacking with themselves. feather-fall — ALREADY falling subsystem, not Slow/control.

The classification above addresses all 179 supplied entries; it does not claim the underlying lexical scan found every possible state in the repository. 
Pasted text

Remaining substantive dependencies
Issue	Status before implementation
Mage Glacier Spike / Cold Focus exact source object	Missing from this attached 179-object list. Use the NEW half-then-5 Mastery rule provisionally if desired, but do not mark Glacier binding SOURCE-AUDITED until the actual normalized object is supplied/verified.
Curse tier for Cleansing Brand	Needs explicit rank/tier/removability metadata on the curse source. No universal non-spell curse tier is established here.
Actual disease catalog	This packet supplies readers, cures and immunities but no disease-producing state objects. Disease-specific saves, special cures and durations still need their source pass.
Generic physical-restraint fallback	Rule can be authored now, but none of the supplied active restraint records actually needs it; do not accidentally attach it to sources with printed endpoints.
Object/tether durability beyond Net Bolt	Requires the equipment/object-durability pass; no invented cut/break HP.
Mage Glacier/Cascade source linkage	Cascade remains non-Focus based on the previously reviewed card; Glacier needs exact object verification before final source binding.
Death Ward / Celestial Resurgence / resurrection vs lethal track states	Remains the separate death/replacement/resurrection interface, not solved through mark metadata.

This is sufficient for Codex to implement the next source-qualified control-state registry candidate and test speed arbitration, mark ownership/consumption, curse/disease readers, restraint suppression and regular-turn repeat-save clocks. DD16 should remain open until that implementation and the still-unscanned semantic remainder are adversarially reviewed. 