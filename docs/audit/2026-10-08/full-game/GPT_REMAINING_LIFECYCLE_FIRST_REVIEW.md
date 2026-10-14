# GPT remaining lifecycle first review

Complete visible notebook reply paired with CODEX_REMAINING_LIFECYCLE_CONFERENCE.md. Source-audited/draftable; no implementation closure.

ChatGPT said:

This 80+5 slice is coherent enough for implementation after the source-specific integrations below. It should remain SOURCE-AUDITED / DRAFTABLE, not closed, until implementation/tests return. The previously closed creature100+5 and device74+3 interfaces remain bounded and are reused only where their exact contracts apply. 
Pasted text

Classification of all 80 supplied IDs

Legend: LC lifecycle/command; OBJ physical object lifecycle; MOD modifier; GUARD eligibility/anti-farm/agency; PREV previously reviewed healing/control/redirection/death interface; DEFER incidental temp-HP/form/Time-Loop/full-card material; ZONE non-HP effect.

Family	IDs	Classification
Cleric	cleric.hero.cultist.rite-of-the-crimson-choir; cleric.hero.cultist.ritual-of-undeath	LC + PREV companion/reanimation; retain reviewed healing/death components
Cleric	cleric.hero.saint.divine-rebirth; cleric.hero.saint.resurrection	PREV resurrection/death; THP details remain later corpus
Cleric	cleric.engine[2]; cleric.engine[7]; cleric.hero.cultist.dark-conviction; cleric.engine[10]	GUARD resource/corpse/agency/acquisition
Crimson Agent	crimson-agent.engine[5]; crimson-agent.base.blood-tithe; crimson-agent.hero.bloodweaver.bloodbond; crimson-agent.hero.bloodweaver.crimson-pact; crimson-agent.hero.thirstborn.crimson-harvest	PREV healing/direct-HP/redirection + anti-farm
Crimson Agent	crimson-agent.engine[0]	GUARD BG gain/anti-farm
Crimson Agent	crimson-agent.arch.veinweave-bloodshield	DEFER THP/defense
Dragoon	dragoon.engine[0]; dragoon.hero.dragon-tyrant.momentum-feeder	GUARD Momentum/kill farming
Dragoon	dragoon.hero.dragon-guardian.momentum-shield; ...bastion-descent; ...momentum-barrier	DEFER THP/full effect
Monk	monk.base.discipline-initiate	DEFER incidental THP/discipline choice
Oracle	oracle.supplement.haunted.haunted-boon-v; oracle.supplement.bones.ledger-s-command; oracle.supplement.bones.ledger-unbound	LC scout/control/servants
Oracle	oracle.supplement.bones.unfinished-chorus; ...bones-revelation-mastery; ...flame-revelation-mastery; ...life-revelation-mastery; ...stars.clarity	MOD/PREV periodic/control/healing; not lifecycle-complete cards
Oracle	oracle.supplement.wound-eater.wound-eater-boon-iii; ...boon-v; oracle.supplement.life.overflowing-light	PREV death/direct-HP/healing
Oracle	oracle.engine[6]; oracle.engine[13]; ...battle-prophecy-trigger; ...bones-prophecy-trigger; oracle.engine[19]; oracle.engine[29]	GUARD resources/agency/copy/redirection
Oracle	oracle.supplement.spiral-touched.spiral-touched-boon-v	DEFER Time Loop snapshot interface
Paladin	paladin.supplement.oath-of-grief.echo-of-the-fallen	LC source-native spirit manifestation, explicitly not resurrection
Paladin	...channel-life; ...healing-suppression; ...linked-ward; ...final-stand; ...unbroken-covenant; ...dirge-of-ruin; ...king-s-smite; ...last-king-s-gift; ...crownshatter-decree-aura	PREV healing/redirection/death
Paladin	paladin.base.divine-strike; paladin.hero.divine-sense; ...verdict-absolute	GUARD/MOD no companion proc / perception / resource-trigger
Paladin	paladin.engine[5]; paladin.base.bolstering-presence; ...dread-shelter; ...black-manifestation; ...primordial-surge; ...noble-bearing	DEFER THP/full aura/control details
Soldier	soldier.engine[2]; soldier.base.quick-deploy; soldier.arch.palisade-deployment; soldier.hero.artillerist.turret-deployment	OBJ/LC structures and finite turrets
Soldier	soldier.hero.artillerist.palisade-synergy; soldier.engine[3]	MOD actual Palisade modifiers
Soldier	soldier.hero.artillerist.bubble-of-discipline; soldier.arch.fortify-zone; soldier.hero.champion.wall-of-aegis	ZONE/effect, not HP objects
Soldier	soldier.base.rally-point; soldier.hero.champion.rallying-cry; soldier.supplement.final-command	DEFER/GUARD THP/resource refresh
Thief	thief.engine[0]; thief.base.disable-device; thief.hero.arcane-trickster.arcane-theft	GUARD/check; no lifecycle creation rights
Warrior	warrior.engine[10]; warrior.engine[15]; warrior.arch.brutality-momentum; warrior.hero.wardborn.aegis-incarnate; warrior.supplement.bone-hardened; warrior.supplement.hemophage-core	GUARD/PREV resource/healing/redirection/DR
Warrior	warrior.base.mutation-surge	DEFER incidental THP

That covers all 80 IDs exactly once.

1. Rite of the Crimson Choir

This is an explicit exception to the ordinary one-damaging-companion-action chassis. One BA/offensive command may authorize up to four surviving fanatics, each moving and making one independently rolled attack. It is still one owner command and one offensive allowance, not four commands. The printed per-hit 1 HP recovery remains capped at 4 HP/round and stays inside the already-reviewed healing gates. 
Pasted text

NEW lifecycle integration: each fanatic has one explosionSettled opportunity.

Explosion triggers exactly once when that fanatic:

reaches 0 HP;
is still present when Choir concentration actually ends; or
is still present when the third-round ending occurs.

At a source-wide ending, snapshot surviving fanatics and positions, then resolve each unsettled explosion in stable creation order, then remove the Choir bodies. A fanatic that already exploded at 0 does not explode again.

The explosion:

is source-native damage, not a companion command;
generates no Choir healing;
creates no corpse/XP/loot/Conviction;
creates no recursive Choir explosion/resource/copy chain.

No individual voluntary dismissal procedure is supplied. Do not invent one. If a broader concentration rule permits the Cleric to voluntarily end concentration, that actual concentration ending triggers surviving explosions. Mere suppression of outputs while concentration remains active does not.

Fanatics are finite HP-only summoned entities: no Wounds, Stable or death saves; no Reactions as printed.

2. Ritual of Undeath: Corpse Servant

Choose one mode when the single Action/cost/use resolves; Corpse Servant and Death Ward are not simultaneous. Death Ward remains under its already reviewed would-die replacement interface. 
Pasted text

For Corpse Servant:

NEW physical-body integration: the qualifying real humanoid corpse is consumed into the animated servant state at successful creation. It is no longer independently available as a corpse/anchor/resurrection target.

The thrall:

AC13, HP10, Speed30;
finite HP-only;
lasts 3 rounds;
uses the owner-wide BA/offensive companion command;
one independently rolled attack using current Cleric technique attack and current S d6 necrotic;
disappears at 0 or expiry.

Its end does not recreate the source corpse. That follows the source's explicit “no new corpse/resurrection target” language and closes the corpse-loop cleanly.

3. Ledger's Command

Preserve original creature identity/stat provenance. Control never rewrites its native HP, AC, attack profile, source owner, body or normal initiative. The already-reviewed hard/soft split remains authoritative. 
Pasted text
 
Pasted text

Use two command paths.

Willing undead: it may waive each required save. A BA command authorizes one consensual extra commanded move/ordinary attack using the shared command/offensive allowance and universal extra-Action ceiling. Resolve in the normal attached companion phase. It does not consume hard denial.

Hostile/unwilling undead after failed save: the first actual forced attack must replace its next future regular Action, using the same future-order reservation model established for Reflective Companion:

BA paid on issuance;
offensive allowance reserved in resolution round;
no duplicate turn;
hard-denial allowance spent only when its Action is actually replaced.

After that Oracle→target hard-denial allowance has been spent, Ledger can never force another Action from that target this encounter.

At every actual target regular-turn end while control remains, perform the printed WIS save. Success ends that target's Ledger control. On a later failure after hard denial has already been spent, apply only the printed soft fallback:

no Reactions + Speed 0

until that target's next regular-turn end or Ledger ends, whichever comes first. No forced Dodge/movement/attack fallback.

Ledger interception

This is not an ordinary reviewed damage transfer.

NEW source-specific attack interception: once per Ledger application, after a legal single-target attack against the Oracle has hit but before its damage/on-hit effects resolve, choose an active controlled expendable undead.

no Reaction cost is added; the source prints none;
the attack is intercepted and produces no damage/on-hit effect on the Oracle;
no second attack roll is made;
do not replay the attack packet against the undead;
instead set the intercepting undead to 0 HP by source assignment after absorption;
this assignment is not damage and cannot generate RC/resource/retaliation/copy loops.

Its native 0-HP lifecycle then applies. No new/duplicate corpse entitlement is generated by Ledger; an actual preexisting physical body remains governed by its native/global body rules.

The source supplies no interception-distance requirement beyond being an active controlled undead. Do not invent adjacency or carry the original 4-tile acquisition range forward as an ongoing tether.

4. Ledger Unbound

Use the standard-companion chassis for omitted ordinary servant fields, with explicit source overrides:

HP = 1;
duration = 3 rounds;
Revelation attack bonus;
damage = 1d8+S necrotic;
no XP/loot/harvestable corpse/RC;
shared BA/offensive command;
only one servant attacks per round. 
Pasted text

Thus AC defaults to 12+floor(PB/2), Speed30 and saves use owner PB.

One narrow evidence gap remains: the source does not specify whether the overridden servant attack is melee or ranged. The frozen chassis distinguishes melee reach5/ranged30 but does not establish which delivery mode this card chose. Do not silently grant both. The lifecycle can be implemented now, but attack range/mode should remain an explicit profile gap until source/owner clarification.

Eligible corpses are actual, nonsummoned, presently available bodies. Preserve the previous anti-fragment/raised/summoned corpse exclusions. NEW: each selected body is consumed into its servant instance and does not reappear when that servant ends.

Attack versus sacrifice

Per servant, per numbered round:

attacking locks that servant out of sacrifice;
sacrificing locks that servant out of attacking.

Because the text says “no attack is made by that servant that round,” servant A may attack while servant B is later sacrificed if the other action resources allow it.

Ledger Unbound sacrifice spends the Oracle's printed Reaction but does not consume the companion offensive allowance. Use the same source-native interception contract above: attack against Oracle is absorbed; servant is source-sacrificed to 0/ended; no new attack roll/damage packet/corpse-resource chain.

Existing-undead buff

NEW membership integration: snapshot up to three undead IDs the Oracle already controlled before Ledger Unbound creates its new bone servants. Newly created servants do not qualify for “already control.”

Those IDs remain the only possible recipients for three rounds. Each benefit operates only while that same creature is currently controlled by the Oracle:

+S to its one shared commanded attack;
first damage received each round reduced by1.

Loss of control suspends the benefit; regaining control during the original duration can restore it for the same snapshotted ID. No replacement recipient may be chosen.

5. Haunted Boon V

Treat the spirit scout as a bounded narrative scout manifestation, not a standard combat companion. The source provides no AC, HP, attack, command procedure or combat targetability. Do not invent them. 
Pasted text

It:

lasts at most 10 minutes;
travels only along a same-plane route the Oracle personally traveled;
remains within one mile;
has ordinary sight/hearing only;
can speak only with willing dead spirits encountered;
reports only on return;
provides no real-time remote senses;
does not transmit the Oracle's senses;
cannot cross sealed planar barriers;
cannot read minds or produce unknowable facts.

Its report may include the printed short prophecy/name only if grounded in what it actually encountered.

Genuine evidence gap: no movement speed or abstract travel-time formula is supplied. Implementation should require the caller/Director to certify that the out-and-back route can be completed inside the 10-minute duration; do not assume instantaneous one-mile travel.

6. Echo of the Fallen

This is a source-native spirit manifestation, not a summonable body or resurrection. It has:

no HP;
no AC;
no targetability;
no companion turn;
no BA command;
no corpse;
no follow-on action.

The Paladin's Action resolves the chosen mode immediately. 
Pasted text

Strike additionally consumes that owner's offensive-companion allowance for the numbered round. Guard does not.

Eligibility requires an actual recorded death event for that allied creature occurring inside the Paladin's aura during the current encounter. A finite summon that merely disappeared under its non-death lifecycle does not qualify.

Use key:

Paladin owner + fallen creature identity + long-rest epoch

so repeated death events of one ally do not manufacture extra uses.

No corpse is required. The exact text says “who died,” so this packet does not add a requirement that the ally must still be dead when the Echo is invoked.

Strike profile

Require a real recorded ordinary weapon profile:

attack modifier;
base weapon damage formula;
original weapon damage type.

If no such profile exists, Strike is unavailable; Guard remains legal. Do not invent a sword or generic weapon.

Attack modifier:

min(recorded ordinary attack modifier, PB + actual CHA)

NEW damage-cap integration: compare the recorded ordinary base weapon profile against S d8+M using maximum possible noncritical damage (dice maxima + flat modifier). If the recorded profile's maximum exceeds the cap profile's maximum, substitute S d8+M; otherwise use the recorded base profile. Preserve original weapon damage type. Then ordinary attack/critical rules apply to the selected profile. No class riders, Smite, Sneak Attack, extra attacks, resources or procs.

This gives the card a deterministic cap without inventing a base weapon or rolling two competing damage packets.

7. Soldier Palisade

This is a genuine physical Soldier object, but not automatically a Tinker device.

NEW creation snapshot:

baseWallMax = max(1, 5 + actual CON modifier at deployment)

Tier II wall at creation:

wallMax = 2 × baseWallMax

AC12. Tier II also grants the printed area-damage resistance. Existing walls do not retroactively recompute or heal when CON/class tier later changes; new construction uses current values. This physical-construction snapshot is source-specific. 
Pasted text
 
Pasted text

Wall states:

INTACT | DESTROYED | DISMANTLED

Only intact walls count against intact-wall cap and enable Hold Position, Brace Line and Palisade Synergy.

Repair:

Action;
once/encounter;
actual spare parts required;
current M HP restored;
positive-HP damaged wall only;
cannot exceed max;
cannot reconstruct at 0;
does not restore deployment uses or kits.
Kit/material accounting

NEW physical-material integration:

deployment commits one carried kit into the intact wall;
one-minute dismantling returns one reusable kit to carried inventory, capped2;
dismantling does not refund the encounter deployment use;
destruction releases intact-wall capacity but does not refund the kit or deployment use;
destroyed remains grant no salvage/sale/reconstruction entitlement from this packet;
completed LR with carpentry replenishes up to 2 carried kits, never above2, exactly as printed.

This prevents free replacement loops while giving “reusable parts/dismantle” mechanical meaning.

8. Soldier Turret Deployment

The source's rangeAndTarget = Up to 2 empty squares controls the conflict with “Deploy 2 turrets.”

Narrow source reconciliation: choose one or two legal empty squares. Deploy one turret in each chosen square. An empty list is illegal under the frozen targeting rule.

choosing one intentionally spends the full short-rest use;
no second turret can be added later from that use;
requesting two validates both spaces atomically before spending the use.

Each turret snapshots creation HP 2×Soldier level and AC 12+PB. Attacks use current original Soldier PB+DEX and current M at resolution. Only one turret may attack from the shared BA/offensive command; no autonomous fire. Three-round expiry ends it administratively. 
Pasted text

“Reclaimed after use, no resale” is bookkeeping only: it creates no saleable inventory, salvage resource, extra deployment or recharge reset.

Do not import Tinker permissions merely because these are turrets:

no Tinker Field Repair;
no protected Dissonance routing;
no Snap;
no Volatile Components;
no Recycling/Salvage;
no Tinker deployable slots.

An exact future cross-class source could add one of those rights individually.

9. Quick Deploy and the three named Soldier protections

Quick Deploy is a real temporary HP-bearing object:

AC12;
HP5;
3 rounds or destroyed;
one at a time;
half cover + difficult terrain;
actual field supplies.

It is not a Palisade and receives no Tier II, Hold Position, Brace Line, Palisade Synergy or Palisade repair rights. It also gains no Tinker reconstruction rights by analogy. 
Pasted text

The others are not HP objects:

Bubble of Discipline: bounded protective zone/effect despite the word “cover”; only its printed AC/save/reaction reduction exists.
Fortify Zone: designated firing-lane zone, source-dependent on Soldier consciousness/range.
Wall of Aegis: creature buff granting flat DR; “Wall” is only the ability name.

Therefore none can be:

attacked as an object;
destroyed by HP;
repaired;
dismantled;
Snap Rebuilt;
salvaged;
used for Palisade Synergy.

Their exact text supports effects, not physical anchors. 
Pasted text
 
Pasted text

10. Incidental guards, Time Loop and temp HP

No lifecycle expansion should occur from the anti-farm candidates. BG, Momentum, Conviction, RC, BT, Blood Tithe, Hemophage, Brutality Momentum, kill triggers and companion exclusions remain guards on their own reviewed systems, not new corpse/companion permissions.

Spiral-Touched — Boon V remains deferred to its complete Time Loop integration. This packet does not broaden what encounter snapshot rewinding restores. 
Pasted text

Likewise every incidental THP source above remains classified but not globally closed. That includes the Cleric, Crimson, Dragoon, Monk, Oracle, Paladin, Soldier and Warrior THP references. The dedicated form/temp-HP corpus remains necessary.

Genuine remaining evidence gaps

The bounded lifecycle implementation can proceed with three explicit gaps left outside its executable attack/transport details:

Ledger Unbound bone-servant attack delivery: source gives attack bonus/damage but not melee-versus-ranged mode/range. Do not grant both silently.
Haunted Boon V travel speed/time: route and duration are defined, movement rate is not.
Global corpse cleanup/decay and unrelated natural-body rules: continue to use the already-reviewed physical-body identity model where applicable, but this packet does not create a universal corpse engine.

Everything else listed above has a source-backed or explicitly NEW bounded integration decision.

Conference disposition

SOURCE-AUDITED / DRAFTABLE — selected lifecycle/command/object/guard interfaces for the supplied 80 exact passages + 5 frozen shared supports; implementation and adversarial validation pending.

This does not close the nine source families, full cards, the general temp-HP/form corpus, Time Loop, Wizard/other companion gaps, all structure interactions, balance, human testing, or the complete tabletop/video-game runtime.
