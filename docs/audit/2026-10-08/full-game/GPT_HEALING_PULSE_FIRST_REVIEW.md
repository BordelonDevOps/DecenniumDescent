# GPT healing pulse first source review

Complete visible notebook reply captured from Calibration Review. Discussion only; exact implementation pending.

The 100 lexical candidates separate cleanly into maintained pulses, funded target-start windows, finite installments, native recurrence, modifiers/guards, and exclusions. No general “three pulses” rule should apply outside sources that actually establish one.

Shared pulse / zone rulings

1. Activation versus later payment

Use the printed source first, then class-engine defaults.

Lifewell: Action + 4 RP + all BG establishes the effect, but does not provide free healing. The first same-turn pulse requires its printed Bonus Action + 1 RP. The next two source regular turns require BA + 1 RP each. If that maintenance is not performed, Lifewell ends at that source turn's end.
Renewal Totem: placement Action + 2 RP includes pulse 1. Next two source regular turns require BA + 1 RP. Extended Totem permits one fourth BA + 1 RP pulse.
Healing Briar: Action + 4 RP includes pulse 1. The next two regular turns each offer BA + 1 RP for another pulse.
Circle of Harmony: Action/start cost includes pulse 1; later maintenance pulses are BA + 1 RP.
Restoration Field: Action + 3 RP includes pulse 1; later pulses are BA + 1 RP.
Dark Sacrament: start includes pulse 1; later pulse requires 1 RP. The supplied source does not state the maintenance action type. Do not invent a Bonus Action unless another Cleric engine passage supplies it.
Paladin engine[11]: first sustained Oath-zone pulse is included; later pulses require 1 RP unless the card gives another cadence/action. Desecrated Ground explicitly uses BA maintenance.
Oracle engine[26]: first zone window/pulse is funded by activation; each later window requires 1 RC. It supplies no action cost for that upkeep.

NEW maintenance distinction: if a source calls the later payment/action maintenance/upkeep or says failure ends the effect, failure to maintain ends it by that source regular-turn end and it cannot resume. If a card merely offers later paid pulses without maintenance language, a missed pulse is lost but does not by itself invent early termination.

2. Oracle target-start funded windows

For Oracle engine[26] target-start zones such as Garden/Resonant Seed:

window 1 opens on activation and lasts until source-next-regular-start;
at source-next-regular-start, pay 1 RC once to open window 2;
repeat once for window 3;
payment is per source-owned window, not per target;
only regular turns count; extra turns create no additional target-start pulse;
each eligible fixed target can receive at most one application in a window/round;
a missed window is lost, never banked.

Crown Restored and Eternal Bloom use their printed limited-use pulses with no generic extra RC upkeep.

Song of Mending is not a target-start zone: pulse on activation and source-next-regular-start; Enhanced Song adds source-second-next-regular-start. No engine[26] target-start upkeep.

Wound Eater IV uses its own explicit schedule: activate BA + 2 RC; first drain pulse is at the next source regular start, funded by activation; two later source-start pulses require 1 RC each.

3. Opportunity consumption

A scheduled pulse/window is consumed when its opportunity is committed even if:

target is full HP;
healing is blocked;
healing is reduced to 0;
dice produce a low result;
a rider rather than HP gain is the only surviving component.

No replacement recipient may be chosen after dice or healing restrictions are known.

Scheduled opportunities do not extend because nobody benefited.

4. Targets

Oracle engine[26] persistent-zone beneficiary/enemy identities are fixed at activation, within its target caps.
Lifewell targets are fixed at activation.
Transcendent Meditation's target set is fixed at activation.
Eternal Bloom's healing-reserve identities are fixed when Bloom appears.
If a source says “up to N” each pulse without fixed/chosen continuity, recipients may be repicked each pulse before rolling. This applies to Dark Sacrament, Circle of Harmony, Renewal Totem, Healing Briar and Restoration Field.
Leaving a zone makes a fixed target temporarily ineligible; re-entry can restore eligibility for a later still-open opportunity, but missed windows do not return.
Death or loss of required ally/enemy/living status makes that application fail without replacement.

Fixed zones do not move unless the source permits movement. Totem movement does not create entry healing.

5. Turn clocks

Regular turns only advance pulse schedules. Extra turns do not advance, duplicate, refresh, or generate upkeep.

Concentration loss ends a concentration-dependent effect immediately.

For nonconcentration effects, incapacity does not automatically end them unless their source says so; however an incapacitated source cannot take a required BA/Action maintenance. If that maintenance is required, the normal missed-maintenance rule applies.

Suppression does not pause duration or restore missed opportunities. If suppression blocks only output, legal upkeep may still be paid; if suppression prevents the maintenance activation itself, the opportunity is missed.

NEW outside-initiative bridge: use 6-second virtual regular-turn windows from the existing clock system. Activation pulses remain immediate; later source-start opportunities occur at +6s, +12s, etc. Target-start effects receive one virtual target-start evaluation per source-funded 6-second window. This is only a timing bridge, not new encounter/resource farming permission.

6. Renewal + Echo Totem

Treat parent Renewal and its Echo as one pulse family:

one concentration;
one upkeep payment;
one pulse ID;
one once-per-round ledger;
NEW: one shared up-to-3-beneficiary budget across parent + Echo coverage.

For each selected creature, apply the strongest legal same-name Renewal amount available from its position:

parent coverage = full amount;
Echo-only coverage = half, floor once;
overlap never heals twice.

Echo expands coverage; it does not create another healing pulse or another target budget.

Open evidence: the source does not say whether destroying the parent automatically destroys/ends the Echo anchor. Do not guess that lifecycle in this package. Caller must provide whether each anchor remains active.

7. Eternal Bloom

At appearance, for each qualifying living ally inside:

reserve = missing HP at activation

Split reserve into exactly three integer installments as evenly as possible, remainder assigned to earlier installments. Example 10 → 4/3/3.

At activation, +source-next-start, +second-next-start:

if that recorded ally is alive and inside, attempt the next installment;
if absent/dead/ineligible, that installment is lost, not banked;
later damage never increases the reserve;
suppression does not pause clocks.

Its once-per-ally 1-HP floor is a separate entitlement, not an installment and not healing.

NEW: track that floor separately per creature per Bloom while that creature is legally inside; do not consume reserve or installment state when it fires.

Garden's first-contact cure is likewise independent of actual HP gain. A legal first Garden pulse/contact can cure/retry disease even if HP restoration is 0.

8. Native recurrence stays native

Aura of Grace, Living Pulse, Thief Exsanguinate, Regenerative Mutation, Bloodthick Node, Rapid Coagulation and similar sources retain their own once-turn/start-turn/resource cadence. They do not acquire a generic three-pulse limit.

Efficient Power Cells and Mech Overdrive extend legal duration only. They never increase a healing effect's pulse cap, refund maintenance, or pause a disabled device's clock.

Compact classification of all 100 supplied IDs

Legend: MP maintained pulse; TW target-start funded window; FI finite installment; NR native recurring heal; TH triggered/damage-derived heal; MOD healing modifier/rider; G healing guard/reduction/prohibition; I instantaneous/single heal; X non-healing/excluded; DEV device repair/heal.

Exact ID	Role	Disposition
cleric.base.consecrated-ground	MOD	+S once/creature/Rite pulse after actual restoration; not child heal.
cleric.base.radiance.radiance	MOD	Once/own turn after Rite actually restores HP.
cleric.base.echoes.echoes	FI/COPY	One delayed source-next-start numeric repeat; no triggers/resources.
cleric.base.sacred-chant	X/MP	Nonhealing sustained 3-pulse chant; start + later BA maintenance.
cleric.arch.aura-of-faith	MOD	+1 after actual Rite HP restoration in aura.
cleric.arch.divine-invocation	I/COPY	Instant modes; Renewal/Radiance heal, Echoes numeric repeat; no sustained schedule.
cleric.hero.saint.aura-of-grace	NR	Source regular-start; optional 1 RP; once/own regular turn, no 3-cap.
cleric.hero.priest.balanced-scales	MOD	Actual-gain mark; no healing pulse.
cleric.hero.priest.word-of-power	I	Mercy single heal only.
cleric.hero.priest.cosmic-equilibrium	TH/G	Trigger conversions once/round; no autonomous pulse.
cleric.hero.cultist.sanguine-rite	TH	Once/own turn damage-derived finite heal.
cleric.hero.cultist.blasphemous-tongue	G	Healing reduction applied by Sacrament pulses.
cleric.hero.cultist.zealot-s-touch	MOD	Converts qualifying HoT pulse dice to damage; inherits source pulse cadence.
cleric.hero.cultist.dark-sacrament	MP	Start pulse included; later 1 RP maintenance; max3. Maintenance action unspecified here.
cleric.hero.cultist.zealot-s-fervor	MOD	+S to one healing roll/own turn for 3 rounds.
crimson-agent.engine[2]	G	Bleed/healing-version distinction; no healing scheduler.
crimson-agent.hero.bloodweaver.hemostasis	FI	Prepaid 1d4 at target-next 3 regular starts; no upkeep.
crimson-agent.hero.bloodweaver.lifewell	MP	First same-turn BA+1RP; next2 BA+1RP; fixed targets; missed maintenance ends.
dragoon.engine[4]	X	Burn/Bleed periodic damage only.
druid.engine[4]	X/G	Temp-HP reserve and aura guards; not real recurring healing.
mirrorsage.hero.mirror-mage.reality-fracture	MOD	Once/turn optional +1d6 to existing Echo heal; no pulse creation.
mirrorsage.hero.shattered-one.fractured-dominion	X	Damage copy only; healing excluded.
monk.base.crane-stance-support	MOD/TH	Incoming-heal +S once/round; paid hit rider heal once/turn.
monk.hero.enlightened-master.breath-of-the-thousand-petals	I	One Final heal/resurrection event; no recurring pulse.
monk.hero.enlightened-master.circle-of-harmony	MP	Start included; later BA+1RP; max3; repick≤3/pulse.
monk.hero.enlightened-master.transcendent-meditation	FI	Start + next2 source regular-start automatic pulses; fixed targets; concentration.
oracle.engine[26]	G/TW	Generic Oracle persistent-zone schedule: fixed sets, concentration, ≤3 funded windows.
oracle.supplement.spiral-touched.spiral-touched-boon-iii	I	One direct recovery; not pulse.
oracle.supplement.wound-eater.wound-eater-boon-iv	MP	First drain next source start; two later 1RC source-start pulses.
oracle.supplement.burning-blood.burning-blood-boon-v	TW/TH	Target-start damaging aura + once/own-turn heal trigger; engine26 applies unless later source marks Final exception.
oracle.supplement.consumed.consumed-boon-v	MOD	+S to one Revelation heal/turn; no pulse itself.
oracle.supplement.bones.rotting-touch	TH/G	Initial undead damage-derived heal; Decay blocks healing; no healing pulse.
oracle.supplement.bones.unfinished-chorus	MP/TH	First source-turn drain included; later engine26 upkeep; 2-round cadence, fixed candidate sets.
oracle.supplement.flame.zealot-s-renewal	I	Single healing event + independent cure/backlash.
oracle.supplement.flame.first-flame-convergence	TH	Once/turn damage-triggered heal; no generic zone pulse.
oracle.supplement.flame.crown-restored	FI/TW	Limited Final target-start pulses, max3/creature; no generic upkeep.
oracle.supplement.life.resonant-seed	TW	Activation-funded window1; later engine26 1RC windows2/3; fixed Oracle set.
oracle.supplement.life.garden-of-restoration	TW	Same funded-window model; first-contact cure independent of HP gain.
oracle.supplement.life.verdant-pulse	MOD	Triggered after actual finite HP restoration; emergency floor separate.
oracle.supplement.life.song-of-mending	FI	Activation + next source regular-start; Enhanced adds second-later start; no target-start upkeep.
oracle.supplement.life.life-revelation-mastery	MOD	Modifies Garden/Song; creates no pulse alone.
oracle.supplement.life.eternal-bloom	FI	Three fixed reserve installments; activation + next2 source starts; no upkeep.
oracle.supplement.time.rewind-wound	I	One historical-damage heal; no recurring pulse.
oracle.supplement.time.the-spiral-opens	COPY/FI	Up to one healing echo option; requires 1RC or unused healing use; no free reserve.
paladin.engine[11]	G/MP	Sustained Oath zones: first included, later1RP upkeep, ≤3; Finals/native auras exempt.
paladin.hero.lay-on-hands	I	Single pool-spend heal; corrected Wave cadence belongs elsewhere.
paladin.supplement.oathbreaker-shared.dread-shelter	X	One temp-HP grant; explicitly no recurring heal.
paladin.supplement.oathbreaker-shared.desecrated-ground	X/MP	Nonhealing damage zone; initial + paid BA pulses under engine11.
paladin.supplement.oathbreaker-shared.last-reproach	I/TH	One reaction heal after damage; no pulse.
paladin.supplement.oath-of-mercy.aura-of-mercy	MOD	First finite/paid heal per selected ally/round gets +S.
paladin.supplement.oath-of-mercy.blessing-of-the-meek	I	Single heal.
paladin.supplement.oath-of-mercy.grace-eternal	I/MOD	Finite floor+heal per ally; one actionless LoH permission; no pulse schedule.
paladin.supplement.oathbreaker-oath-of-mercy.healing-suppression	G	Incoming HP healing halved; no pulse.
paladin.supplement.oathbreaker-oath-of-mercy.exsanguinate	TH	Single damage-derived heal.
paladin.supplement.oath-of-flame.phoenix-rebirth	I	Single zero-HP recovery; no recurring heal.
paladin.supplement.oathbreaker-oath-of-flame.death-touch-blighting-blood	X	Damage/terrain only; explicitly no healing trigger.
paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified	G	Blocks passive regeneration only.
paladin.supplement.oathbreaker-oath-of-flame.scorch-the-sanctified-blasphemous-word	G/X	Damage + temporary regeneration-effect suppression.
paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom-aura	G	Blocks passive regeneration; not all finite healing.
paladin.supplement.oathbreaker-oath-of-the-ancients.lifeleech-bloom	TH	Single damage-derived heal.
paladin.supplement.oath-of-grief.dirge-of-passage	G/X	Prevents hostile-undead HP regain; no healing pulse.
paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin-aura	G	Flat healing reduction + resurrection denial.
paladin.supplement.oathbreaker-oath-of-grief.dirge-of-ruin	G/X	Damage plus temporary no-HP-regain.
paladin.supplement.oath-of-the-martyr-king.crown-of-embers	X	Prevention/redirection only; expressly no healing.
paladin.supplement.oath-of-the-martyr-king.burden-shared	X	Redirection only; transferred branch cannot trigger healing.
paladin.supplement.oath-of-the-martyr-king.throne-s-grace	MOD	Modifies other Paladin heals; itself restores none.
paladin.supplement.oath-of-the-martyr-king.crown-undying	TH	Finite redirection-derived healing; redirection ledger governs cadence.
paladin.supplement.oathbreaker-oath-of-the-martyr-king.crownshatter-decree-aura	G	Conditional incoming-heal permission; source costs still spent when blocked.
ranger.engine[5]	X	Temp HP / damage-zone interfaces; no recurring real heal.
ranger.hero.warder.living-pulse	NR	Once source regular-start/turn, optional1RP, self2HP.
ranger.hero.warder.healing-briar	FI/paid	Start included; next2 source turns BA+1RP; max3; repick≤3.
shaman.engine[1]	MP	Renewal start included; next2 BA+1RP; ≤3 beneficiaries/pulse.
shaman.engine[2]	G	Movement competes with upkeep; movement creates no extra pulse.
shaman.arch.extended-totem-duration	MOD/MP	One fourth Renewal opportunity only with BA+1RP.
shaman.arch.spirit-cache	COPY	Recast profile later with full costs/new stock; not active pulse copy.
shaman.arch.totem-pulse	X	Nonhealing placement pulse; no extra Renewal heal.
shaman.arch.spirit-saturation	X/G	Cannot waive/create Renewal healing totem.
shaman.hero.theurgist.echo-totem	MOD/MP	Shares parent pulse/upkeep; half amount; NEW shared target budget/no double heal.
shaman.hero.bloodcaller.blight-totem	G	Healing-halving aura only.
shaman.hero.bloodcaller.blood-curse	G	Magical healing permits cure save; healing itself not scheduled.
shaman.supplement.elder-spirit-accord-new-hero-capstone	MOD	Adds M to one healing roll/use; no duration/pulse increase.
soldier.engine[4]	G	Anti-infinite-healing guard only.
thief.hero.blackguard.exsanguinate	NR	Source regular-start/turn, optional1RP, once/own turn.
tinker.engine[7]	G	Healing pulse caps/costs remain; disabled duration continues.
tinker.base.field-repair	DEV/X	Instant functional-device repair; not organic healing pulse.
tinker.hero.artificer.efficient-power-cells	X/G	Nonhealing duration extension only; healing pulse count unchanged.
tinker.hero.artificer.nano-aegis-drone	FI/command	Up to3 paid BA-command healing/tempHP pulses during3 rounds.
tinker.hero.artificer.repair-pulse	DEV/X	Instant device repair; no organic healing.
tinker.hero.artificer.restoration-field	MP	Initial pulse + later BA+1RP maintenance; max3; organic/device applications distinct.
tinker.supplement.mech-overdrive	G	Duration extension only; never increases healing pulses.
warrior.hero.ironskin.regenerative-mutation	NR	Start each source regular turn; reserve-paid actual restoration; no3-cap.
warrior.hero.ironskin.cellular-reconstruction	FI	Delayed one-time source-next-start recovery after stasis.
warrior.hero.dreadspawn.pain-empowerment	X	Threshold damage passive, not healing recurrence.
warrior.supplement.primed	MOD	+1 to one mutation heal roll/turn; no new pulse.
warrior.supplement.transcendent	X	Explicitly no immediate healing trigger.
warrior.supplement.bloodthick-node	NR	Start each regular turn, reserve-limited; no3-cap.
warrior.supplement.rapid-coagulation	NR	Start each regular turn if prior-turn no movement; reserve-limited.
warrior.supplement.bio-stabilizer	MOD	+1 to valid Bloodthick pulse; no independent heal.
wizard.engine[10]	X	Temp HP/max-HP school effects; Necromancy tempHP is not healing.
wizard.hero.necromancer.infernal-pact-quest-based-unlock	TH/FI	Target-start damage; heal from actual damage, max3-round source; not a healing pulse itself.
Missing evidence before implementation

Four points should remain explicitly open rather than guessed:

Dark Sacrament maintenance action type: source gives 1 RP maintenance but not BA/Action.
Echo Totem parent destruction: exact source does not say whether parent destruction automatically destroys/ends the Echo.
Burning Blood Boon V and engine[26]: under the supplied generic Oracle engine it qualifies as a persistent damaging aura, so concentration/upkeep appears to apply; if Boon V is intended to receive the same “limited Final includes its pulses” exception as Crown Restored/Eternal Bloom, that needs explicit source/engine evidence.
Restoration Field lifetime between pulses: source gives max3 pulses but no explicit “3 of your turns” duration. I recommend a NEW bounded implementation of activation + next two source-regular-turn maintenance opportunities, but this should remain labeled an integration rule unless another Tinker engine passage supplies the cadence.

Everything else above is SOURCE-AUDITED / DRAFTABLE, not yet REVIEWED/reference-VALIDATED. The implementation should center on per-instance pulse/window IDs, source regular-turn clocks, per-target/round ledgers, payment commitment before outcomes, and explicit fixed-vs-repicked target policies without disturbing the already-reviewed healing graph.
