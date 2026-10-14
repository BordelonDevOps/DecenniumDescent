# GPT creature lifecycle first review

Complete visible notebook reply to CODEX_CREATURE_LIFECYCLE_CONFERENCE.md. Source-audited/draftable, not closure.

ChatGPT said:

This packet is suitable for a bounded implementation conference, but not yet for closure. The 100 passages divide cleanly into creature lifecycle/command rules, modifiers/guards, already-reviewed interfaces, and form/temp-HP material that should stay deferred.

Classification

Codes: LC lifecycle/command; MOD creature modifier; GUARD exclusion/eligibility; PREV use an already reviewed interface; FORM defer full form rules; THP defer general temp-HP rules; CTRL use reviewed control interface.

Family	Supplied IDs	Classification
Druid	druid.base.rotshaper.swarm-summoning	LC standard swarm
	druid.hero.rotshaper.carrion-rat-king, druid.hero.rotshaper.insect-broodmother	LC + FORM-dependent summons
	druid.hero.rotshaper.master-of-vermin	MOD summon substitution + FORM
	druid.engine[3]	FORM lifecycle + summon-dependency rule
	druid.engine[0], druid.engine[1]	FORM GUARD/progression
	druid.base.shapeshifting, druid.base.bear-form-tank, druid.hero.archdruid, druid.arch.dire-wolf, druid.arch.earth-warden-dire-bear, druid.arch.sky-serpent, druid.arch.shadow-lynx, druid.hero.moon.beastlord-alpha-animal-hybrid, druid.hero.moon.mooncursed, druid.hero.moon.elemental-shapeshifting, druid.hero.storm.tempest-raptor, druid.hero.storm.thunderhorn-stag, druid.hero.winterfang.frost-wyrmling, druid.hero.ashen-grove.charbear	FORM deferred
	druid.engine[4]	FORM/THP reserve deferred
	druid.base.moon.combat-shapeshifting	PREV healing + FORM gate
	druid.base.ashen-grove.blazing-rebirth	THP deferred
Mage	mage.engine[9]	LC command engine
	mage.engine[10], mage.arch.conjure-elemental-familiar	LC familiar
	mage.engine[11], mage.engine[12], mage.engine[13], mage.engine[14], mage.hero.lich.soulbound-ritual	LC bound elites
	mage.engine[17], mage.engine[16]	GUARD Lich acquisition/readiness only
	mage.hero.lich.corpse-gateway	GUARD corpse identity
	mage.hero.elementalist.elemental-supremacy, mage.hero.elementalist.primal-channeling, mage.hero.lich.soul-reservoir, mage.hero.lich.necromantic-mastery, mage.hero.archmage.spell-sharing	GUARD companion/proxy/summon exclusions
	mage.base.resonance-shield, mage.hero.archmage.empowered-link, mage.hero.archmage.harmonized-core	THP/MOD deferred
	mage.hero.archmage.arcane-sanctuary, mage.hero.lich.lingering-malice	PREV periodic + THP
	mage.hero.lich.resonance-to-flesh	PREV healing/direct HP
	mage.hero.lich.undying-spellform	PREV death interface, self only
	mage.hero.lich.undead-immunities	GUARD self-state
Mirrorsage	mirrorsage.engine[4], mirrorsage.base.mirror-beast-summon, mirrorsage.base.charm-creature	LC/CTRL Beast vs Reflective Companion
	mirrorsage.base.mirrorcall, mirrorsage.arch.advanced-mirrorcall, mirrorsage.arch.mirror-shift, mirrorsage.hero.shattered-one.corrupted-mirrorcall	MOD Mirror Beast
	mirrorsage.hero.light-weaver.radiant-mirror-beast, mirrorsage.hero.shattered-one.shattered-mirror-beast	LC specialized Beast
	mirrorsage.hero.light-weaver.luminant-bond	MOD companion aura
	mirrorsage.engine[3]	PREV Echo release/action/cost
	mirrorsage.engine[1], mirrorsage.engine[2], mirrorsage.engine[6], mirrorsage.hero.shattered-one.shatterbind	GUARD/MOD Echo records
	mirrorsage.hero.light-weaver.radiant-archive, mirrorsage.hero.light-weaver.blessing-echo	PREV healing/THP Echo
	mirrorsage.hero.light-weaver.light-binding	PREV CTRL/THP
	mirrorsage.hero.shattered-one.echo-leech	GUARD companion/copy exclusion
Ranger	ranger.engine[7], ranger.hero.warder.beast-companion	LC persistent Beast
	ranger.hero.warder.beast-empathy	GUARD no automatic control
	ranger.engine[1], ranger.engine[3], ranger.hero.outrider.predator-s-grin	GUARD companion/summon exclusions
	ranger.engine[5], ranger.supplement.master-of-the-hunt-new-hero-capstone	PREV zone/THP Arrow modifiers
	ranger.hero.warder.healing-touch	PREV healing + companion exclusion
	ranger.hero.warder.nature-s-blessing	THP deferred
	ranger.base.weapon-bond	GUARD unrelated persistent object
Wizard	wizard.engine[18]	LC command + anti-farm
	wizard.engine[19], wizard.hero.necromancer.corpse-harvest, wizard.engine[20], wizard.hero.necromancer.ghoul-lash	LC standard undead/Auto-Raise
	wizard.engine[21], wizard.engine[22], wizard.engine[23]	LC elite profiles/caps; acquisition gap
	wizard.engine[24], wizard.hero.necromancer.flesh-ascendant	PREV max-HP integration
	wizard.engine[10]	PREV Conjuration max-HP + THP school riders
	wizard.hero.necromancer.infernal-pact-quest-based-unlock	MOD corpse eligibility + PREV periodic/healing
	wizard.hero.necromancer.arcane-leech, wizard.hero.spellbinder.knowledge-shield, wizard.hero.spellbinder.spell-absorption	THP/GUARD deferred
	wizard.hero.necromancer.binding-sigil, wizard.supplement.arcane-feedback	GUARD companion exclusions
	wizard.hero.spellbinder.matrix-sharing, wizard.hero.elementalist.arcane-fusion, wizard.supplement.dual-cast	GUARD no summon duplication
	wizard.arch.arcane-sight	GUARD magical-state inspection
	wizard.engine[25]	GUARD dark-content/control boundary

The three frozen paragraphs remain SHARED-LC command/lifecycle, SHARED action economy, and SHARED copy/provenance respectively.

1. Zero HP and return categories

Use four distinct creature-life categories.

A. Finite standard summons/companions. Druid Swarm, Mage Familiar, Mirror Beast variants and other sources explicitly using the standard-companion chassis have HP only for this bounded interface. At 0 they disappear/end immediately under the frozen rule. They do not acquire Wounds, Stable state or death saves unless a later exact source explicitly opts them into the organic life layer.

B. Ranger Beast. This is a persistent living bond, not a resummonable token. NEW integration: at 0 HP it dies immediately; no free disappearance/resummon and no companion death-save procedure is invented. Injury before death persists and must be healed normally. A dead Beast requires a new legal bond after a completed long rest.

C. Mage Lich elites. At 0 they become destroyed bound assets, nonfunctional and non-commandable. They produce no usable corpse/resource event. Engine[11] expressly permits full return after completed long rest; Soulbound Ritual permits earlier half-HP return.

D. Wizard undead. Standard raised minions end on destruction and create no reusable corpse/resource chain. Wizard elites become destroyed at 0, but the supplied Wizard passages give no return procedure. Do not import Mage Soulbound/LR return into Wizard. Their acquisition/return lifecycle remains incomplete evidence.

Reflective Companion is different: it remains the original creature, so its preexisting creature-life rules remain intact. Druid forms likewise use the Druid's own HP/life system, not a companion pool.

2. Creation snapshots versus current stats

NEW shared integration for finite created companions: snapshot base maximum HP and printed AC at creation. Current-owner attack bonus, save bonus, class DC, S, and other resolution statistics are read when the action actually resolves unless the source expressly snapshots them.

Thus:

Druid swarm: creation HP/AC; attacks use current PB+WIS.
Mirror Beast: creation standard HP/AC; attacks use current class attack values.
Mage Familiar: creation 5 + Mage level + M, AC 12+PB, Focus-element profile fixed at creation; Elemental Dart uses current Mage spell attack.
Wizard Corpse Harvest minion: creation base profile; Conjuration snapshot applies only when the creature was created by the Wizard spell. Auto-Raise is not a Wizard spell, so it does not gain a new Conjuration snapshot. Flesh Ascendant remains the already-reviewed dynamic current-controller modifier.

Persistent assets differ.

NEW: Ranger Beast maximum HP is dynamic:

max(1, 2 × current Ranger level + actual WIS modifier)

not M, because the card says Wisdom modifier. Current PB drives its standard AC/saves/attack scaling. Maximum increases add capacity only; decreases clamp without damage.

Mage Lich elite printed HP formulas use current Mage level; attack/DC references use current Mage statistics. Their fixed AC remains fixed. Wizard elite formulas likewise refer to current Wizard level if/when an actual binding source creates one.

Healing never refreshes duration, recharge, command usage or independent spent abilities.

No owner-incapacity/death termination is invented except where concentration/action rules or an exact source already cause it.

3. Outer command ledger

Keep one owner-wide BA command ledger across multiclass companions.

Add an owner-wide offensive companion allowance per numbered round.

It is spent by:

any damaging companion action;
Mage/Wizard explicit non-damaging control actions, because their engines expressly define one “damaging or control action” as the offensive command choice.

Therefore a Wizard Boneflayer Fear Pulse consumes:

the BA command;
the offensive companion allowance.

That prevents a later Gadget Sync attack in the same numbered round even though Fear Pulse dealt no damage.

Pure support actions do not consume the offensive allowance unless their source says otherwise. They still consume the BA command.

Ghoul Lash is the exact exception: its two attacks are one command and one offensive allowance, not two commands.

Mage/Wizard additionally require their command on the owner's regular turn. Extra turns do not reset either allowance.

4. Companion-created persistent effects

A paid command may create a source-native persistent effect.

Boneflayer Grave Miasma is the important example.

NEW integration: the command that creates Miasma consumes the offensive allowance once. Its scheduled entry/start damage until the printed expiry:

requires no second command;
does not debit the next numbered round's offensive allowance;
does not become autonomous companion turns;
retains all anti-farm/no-recursion restrictions.

Otherwise a command near a round boundary would improperly consume two rounds of companion offense for one printed action.

Wraithbound/recharge timing uses an owner-linked regular companion marker immediately after the owner's regular turn. Extra turns do not create extra regular companion markers. “Previous/next turn” and round recharge are measured against that coherent marker.

Uncommanded companions may move defensively/Dodge only; they cannot originate damage/control absent an already-created source-native ongoing effect.

5. Mage/Wizard elite identity and corpse rules

The same three names appear in both systems.

NEW shared-identity integration: per owner, Boneflayer, Dreadblade and Wraithbound are unique elite identities across Mage/Wizard access:

at most one of each;
maximum three total across those same named assets;
no Mage Boneflayer plus separate Wizard Boneflayer duplicate.

The actual binding source controls the asset's stat provenance. Mage Lich has an explicit unlock/binding lifecycle. Wizard currently has profiles/caps but no supplied acquisition procedure, so this rule does not create Wizard pets by itself.

Corpse identity is consumable.

Corpse Harvest/Auto-Raise consume the original eligible body into the undead minion state. Destroying or dismissing that minion does not recreate the original corpse. Summoned/raised remains, repeated fragments and copied/illusory remains do not become new corpse fuel.

Corpse Gateway does not consume its legal corpse.

Infernal Pact expands Harvest/Auto-Raise eligibility to Fiends only.

Goblin Thrall remains stricter: it requires a goblinoid corpse.

Therefore:

Goblin Thrall kills ordinary non-goblinoid humanoid → no Goblin-Thrall Auto-Raise.
Goblin Thrall kills eligible goblinoid → may Auto-Raise Goblin Thrall.
Skeleton/Zombie kills ordinary eligible humanoid → may raise same mechanical type.
With Pact, Skeleton/Zombie may raise from eligible Fiend corpse.
Pact does not erase Goblin Thrall's goblinoid-body requirement.
6. Auto-Raise queue

Use one owner-wide Auto-Raise opportunity per numbered round.

At the qualifying killing blow:

verify killer is one of the owner's standard undead;
verify actual eligible corpse;
verify current standard count plus existing reserved Auto-Raise slot is below 3;
verify this round's Auto-Raise opportunity unused;
reserve one capacity slot and that corpse ID;
record the killer's mechanical minion type.

No Action/RP is paid.

NEW reservation rule: the reserved slot counts against the three-minion cap until the end-turn resolution. This prevents manually filling the slot and then demanding an over-cap raise.

At the current turn's end, after immediate death reactions/corpse consumers but before ordinary administrative turn cleanup:

corpse still exists and remains eligible → continue;
physical placement possible → continue;
reserved capacity still valid → create the recorded type;
consume corpse;
new minion cannot deal damage/control until the next numbered round.

If corpse was consumed/removed, resolution fails and reservation ends. If the killing minion was destroyed before turn end, the already-triggered raise still resolves; the source does not require killer survival.

Ghoul Lash can land two killing blows, but only one Auto-Raise may be selected that round.

No dismissal is automatically performed to force a raise.

7. Mage familiar and Lich elites

Mage Familiar:

one at a time;
profile matches Focus at creation;
changing Focus later does not alter element, resistance, flight, HP or refill it;
summoning another normally dismisses the old familiar;
0 HP/duration end → disappears, no corpse/resource event.

Lich readiness/consent passages are guards only. They do not instruct this lifecycle helper to run a ritual.

Soulbound Ritual returns the same bound elite asset:

half current maximum HP;
printed S+M temp HP;
no new asset identity;
no reset of recharge, limited uses, independent effects or command history.

Unexpired legal effects/clocks remain unless their own state predicates ended them on destruction. A completed long rest returns the elite at full HP because engine[11] says so; any recharge/use resets come from the actual canonical rest rules, not from the return operation itself.

8. Ranger Beast bond

Exact bond procedure is already supplied:

Ritual;
4 RP;
1 hour;
willing/tamed eligible Beast touched;
frequency 1/long rest.

What is not supplied is the campaign procedure for finding/taming/making a Beast willing. Do not invent it.

Bound profile:

standard companion chassis;
dynamic HP formula above using actual WIS modifier;
one retained movement mode, maximum 40 ft;
keen-sense advantage as printed;
one commanded standard attack;
no imported CR stat block powers.

The chosen movement mode/keen-sense identity is fixed when bonded; changing the fictional animal or rebonding is not a healing mechanism.

Injury persists through retraction/travel/rest unless ordinary healing/rest rules actually restore it. A wounded Beast cannot be “resummoned” because there is no summon procedure.

At 0 it dies. After a completed long rest the Ranger may perform a new full bond ritual with an eligible Beast. The card supplies no free replacement animal.

9. Mirror Beast versus Reflective Companion

Exactly one exists/operates under this slot at once.

Mirror Beast:

standard companion lifecycle;
Mirrorcall adds +M maximum and current HP only on summon;
appearance/locomotion shifts do not heal/reset it.

Reflective Companion:

remains the original creature;
no new HP pool;
no reconstruction;
no duplicate token/turn;
original conditions, HP, effects and provenance remain.

Use the existing control scheduler: retain the creature's original regular-turn marker/initiative. The owner command does not grant a second turn. Repeat saves occur at that creature's actual turn end and when harmed as printed.

While controlled it participates in the owner's companion command budget, but this is temporary control, not permanent ownership. When control ends, actual state persists and original disposition returns.

Its permitted attack uses the capped standard S d6; unique powers remain unavailable.

10. Mirror-origin Echo

Confirmed ownership split:

Mirrorsage owns the cast;
owner spends Action;
owner spends BA companion command;
owner pays RP;
owner consumes record;
owner owns Dissonance/Refrain;
owner owns concentration;
owner owns the once-round release cap.

The Beast is only the origin point.

NEW geometry integration: measure Echo range and line-of-effect from the Beast's position when the source says it originates there. Any non-geometric caster requirement remains on the Mirrorsage. Do not invent an owner-visibility requirement where the ordinary Echo profile/general targeting rules do not require one.

Preflight atomically:

active eligible Beast;
release record/legal profile;
owner's Action;
owner's BA command;
RP;
shared release cap;
legal origin/target geometry.

If preflight fails, consume none of those.

Once committed, normal saves/misses do not refund costs.

Radiant Beast has a source-local one-option lock that round:

attack or
paid heal or
paid Echo origin.

Echo damage remains the owner's spell damage, not a companion attack.

11. Druid swarm dependencies

Swarm Summoning is an independent concentration summon, not a form-granted summon.

Therefore changing form does not end it merely because engine[3] says old-form summons end. Maintaining existing concentration while shifted is expressly allowed.

Engine[3]'s old-form dependency applies to summons whose existence comes from the form itself:

Carrion Rat King form swarm;
Broodmother form swarms.

Those end when that form ends/changes.

Carrion Rat King replaces its previous form swarm, not an unrelated paid Swarm Summoning.

Broodmother's two swarms:

one Form Surge on entry;
two bodies;
one combined damaging command;
both end with the form.

Master of Vermin modifies the creature profile of an otherwise paid summoning spell. It does not multiply casts, creatures or command allowance. Because the summon originates from the paid spell rather than the form itself, changing form does not automatically end it; its actual spell duration/concentration controls.

12. Forms and temporary HP

Do not pull the incidental form/THP passages into the creature lifecycle engine.

Druid forms remain the same character:

own HP;
own ability scores;
own saves;
own proficiency;
no monster stat block;
no separate companion/entity life pool.

Form reserve arithmetic, all form-specific attacks, retaliation, form temp HP and remaining form cards stay open for the later form/temp-HP audit.

Likewise this packet does not globally close:

Resonance Shield;
Arcane Sanctuary temp HP;
Lingering Malice temp HP;
Knowledge Shield;
Arcane Leech;
Nature's Blessing;
Mooncursed/other form buffers;
every temporary-HP aura.

They retain their existing interfaces but are not made globally complete here.

Additional exact evidence still needed

Before implementation can claim broader creature completeness, I would specifically request:

Wizard elite acquisition/binding procedure: action, cost, timing, prerequisites, replacement/dismissal and whether destroyed Wizard elites have any return mechanism.
Core living-companion rest/healing paragraph used by “heal normally,” if you want Ranger Beast natural rest recovery encoded rather than caller-owned.
Existing control/initiative source IDs governing controlled creatures, so Reflective Companion can bind directly to the reviewed scheduler rather than merely referencing it.
General spell/ability line-of-effect and visibility procedure used by Echo Release, for exact Beast-origin geometry.
If one exists, the corpse identity/cleanup procedure defining when a normal corpse ceases to exist independently of Harvest/Auto-Raise/Gateway.
Any source that defines the Ranger Beast's exact keen-sense selection beyond the phrase supplied here. Do not import a CR stat block to infer it.
Conference disposition

SOURCE-AUDITED / DRAFTABLE — bounded 100-passage creature-companion/undead/dependency conference.

The source set is sufficient to implement the standard summon, Mage familiar/Lich elite, Ranger Beast, Mirror Beast/control dependency, Druid swarm, Wizard standard-undead/Auto-Raise, outer command and corpse-consumption interfaces above.

It is not sufficient to instantiate Wizard elite pets from scratch, nor does it close full Druid forms, all temp HP, all five classes, the remaining companion families, balance or the complete runtime.
