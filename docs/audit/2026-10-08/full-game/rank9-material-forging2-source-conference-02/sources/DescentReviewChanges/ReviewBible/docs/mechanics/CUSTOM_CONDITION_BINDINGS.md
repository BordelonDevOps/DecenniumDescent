# Custom condition and rider bindings — working playtest reference

**Status: IN PROGRESS.** These source-qualified rules are provisional integration decisions. They preserve the original class and spell cards; they do not establish that all 1,223 class cards, all spells, or all game systems have completed semantic review.

This reference currently contains **57 definitions and 14 feature interfaces**. Machine checks verify source references and selected interactions, not encounter balance or human table readiness.

Use the [generic conditions](CONDITIONS_PLAYTEST.md) and [recovery procedures](CONDITION_RECOVERY_PLAYTEST.md) alongside this reference. Source text, timing, costs, targets and concentration remain applicable. A family tag supplies only its explicitly documented recognition/cure/immunity interface. It never imports every member's effects.

## Bounded reviewed scopes

**Periodic family integration: REVIEWED / reference-VALIDATED.** The 32 registered periodic profiles and their shared family, cure, immunity, refresh and source-qualified hook interfaces. The registry as a whole, full-engine application and human balance remain open.

Review: [GPT disposition](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md).

**Strain namespaces (separate reference): REVIEWED / reference-VALIDATED.** See STRAIN_PLAYTEST.md for the separate serum0–3 and expedition0–6 systems. These are not additional periodic-family records or generic Exhaustion.

Review: [GPT disposition](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_FINAL_REVIEW.md).

**Suppressed-record cure correction: REVIEWED / reference-VALIDATED.** Present Bleed/fire records remain curable while suppressed; source-specific methods, immunity prevention and active hooks unchanged. 98 current custom-interface checks pass, including14 added cases.

Review: [GPT disposition](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_CLOSURE.md).

## Shared interpretation

**family.bleeding.** Explicit hostile Bleed classification for immunity, curing and stated eligibility. Class/owner/source timing and caps remain separate. No inherited damage package.

**family.ongoing-fire.** Only explicitly registered creature-attached Burn-style periodic fire. Excludes direct fire, areas, hazards, environmental flames, object ignition, Resonance Burn and names alone.

**periodic.arbitration.** Generic Core and custom groups enter ONE family arbitration at an identical target marker. Within each family at one identical target timing marker, select one stack group by highest expected unmitigated damage then earliest application. Apply source instance caps before comparing. All due groups consume their tick, including non-damaging losers. Different markers and families resolve separately. Stable unique application sequence breaks simultaneous applications in resolution order; lexical group ID is a final implementation tie-break only.

**ownership.** Ordinary your means ownerCharacterId. Explicit class phrases restrict sourceClass. Crimson technical Bleed engine hooks require owned Crimson instances. Suppressed, immune, inactive or expired effects do not satisfy active-effect hooks.

**hp-cure-separation.** HP prohibition prevents regained HP. Legal positive-potential magical healing can still invoke a registered Bleed cure, including Blood Curse CON save; a remover explicitly requiring actual HP gained retains that prerequisite.

**exclusive-periodic-binding.** A textual effect component with a reviewed source-qualified profile creates only that record. Core Bleeding/Burning are fallback identities only for explicit Core applications lacking a more-specific profile. A family tag or display word never also creates a generic record. Two records require two effects explicitly imposed by the operative source.

**immunity-and-periodic-arbitration.** Condition/family immunity prevents initial application. Gained condition/family immunity suppresses an existing record: clocks and due ticks continue, but suppressed records are excluded from damage arbitration and active-effect hooks. Damage-type immunity/resistance does not suppress the record or exclude it from arbitration; choose using unmitigated expectation, then apply defenses.

**recipe-occupancy.** A poison recipe occupies an ongoing-instance slot only while at least one ongoing component remains. Suppression does not erase an existing component; curing/expiry can end it. Resolved one-time critical healing does not occupy a slot. Ending Bloodleech's sole remaining Bleed ends its occupancy without purging other poison or curse records.

**cure-presence-suppression.** SUPERSESSION: Cure/removal tests existing unexpired presence, not current effect activity. Medicine selects one present eligible Bleed; positive-potential legal magical healing invokes each present eligible endpoint (Blood Curse retains CON save); Action/full immersion ends all present ordinary-extinguishable fires. Suppression/acquired condition immunity does not bar these cures or existing permitted ending saves. Damage arbitration and active-effect hooks still exclude suppressed/immune records. Initial immunity prevents new application; ended records cannot resume.

**Application records.** Preserve application ID, owner character, source class/engine, target, DC, damage type, start, remaining ticks or expiry, source stack group, and cure exceptions. “Immune” in an active-effect eligibility check means immunity to the condition/application, not merely immunity to its damage type. Damage immunity does not by itself erase an effect.

**Timing.** Explicit start/end timing wins. An omitted next-turn periodic marker is provisionally end of the next regular target turn. Extra turns add no periodic ticks or ending saves. Outside initiative preserve the clock and consume one due step per complete six seconds; initiative transitions do not duplicate events.

**Bleed treatment.** A WIS (Medicine) Action by self or an adjacent helper selects one ordinary Bleed record before rolling: printed cure DC, otherwise recorded applying effect/class/spell DC, otherwise 10. Success ends that record. One legal magical-healing event with positive pre-cap/pre-prohibition potential ends every eligible automatic-healing-cure record; each Blood Curse instead receives its own CON save. An explicit remover keeps its stated one/all/owner scope.

**Cure presence.** Treatment, magical-healing cure and permitted per-record ending saves can remove a still-present suppressed or condition-immune Bleed/fire record. Cure scope and special prerequisites remain unchanged. Effect eligibility and damage arbitration still exclude suppressed records. Successful removal ends the record permanently; immunity ending cannot restore it.

**Kit exceptions.** A Crimson kit Action consumes one use and ends that source owner's Crimson Bleeds on the victim. A Dragoon kit Action consumes one use and ends the selected Dragoon Bleed. Other records do not silently acquire these kit endpoints.

**Attached fire treatment.** One self/helper extinguish Action or full immersion ends all ordinary-extinguishable attached fires on that creature. Explicit protected-fire exceptions survive. At the end of each regular target turn, after due ticks are consumed, each still-active fire record with future ticks remaining receives its own ending DEX save at its source DC or 10. An indefinite generic fire has future ticks. No ending save is needed after a record's final tick expires.

**Duration changes.** Printed base duration is distinct from an express hard cap. A qualifying refresh never shortens remaining duration. Persistent Bleed normally supplies two turns; Prolonged Suffering changes application/refresh to four only for owned profiles whose printed base is exactly two. Use the greatest legal replacement, not a sum; obey actual hard caps. No source trigger means no refresh, and expired records cannot be refreshed.

## Periodic effect lookup

| Mechanical identity | Damage | Regular target marker | Base ticks | Source stack group |
|---|---|---|---:|---|
| `mage.fire-focus.burn` | 1d4 fire | start | 1 | `mage.fire-focus-burn:<ownerCharacterId>` |
| `mage.inferno-lance.burn` | 1d6 fire | start | 2 | `mage.fire-focus-burn:<ownerCharacterId>` |
| `crimson-agent.bleed` | 1d4 applying-physical-hit-or-slashing | start | 3 | `crimson-agent.bleed:<ownerCharacterId>` |
| `dragoon.bleed` | 1d4 applying-physical-hit-or-slashing | start | 2 | `dragoon.bleed:<ownerCharacterId>` |
| `dragoon.burn` | 1d4 fire | start | 2 | `dragoon.burn:<ownerCharacterId>` |
| `ranger.synergy.bleed` | 1d4 applying-physical-hit-or-slashing | end | 2 | `ranger.synergy.bleed:<ownerCharacterId>` |
| `ranger.imbue.burn` | 1d4 fire | end | 1 | `ranger.imbue.burn:<ownerCharacterId>` |
| `ranger.emberroot.burn` | 1d4 fire | end | 1 | `ranger.emberroot.burn:<ownerCharacterId>` |
| `shaman.blood-curse.bleed` | 1d4 necrotic | start | 3 | `shaman.blood-curse.bleed:<ownerCharacterId>` |
| `shaman.bloodroot.bleed` | 1d4 slashing | end | 1 | `shaman.bloodroot.bleed:<ownerCharacterId>` |
| `shaman.flame-totem.burn` | 1d4 fire | end | 1 | `shaman.flame-totem.burn:<ownerCharacterId>` |
| `shaman.flask.burn` | 1d4 fire | end | 1 | `shaman.flask.burn:<ownerCharacterId>` |
| `shaman.cinderflame.burn` | 1d4 fire | end | 1 | `shaman.cinderflame.burn:<ownerCharacterId>` |
| `soldier.overwatch.bleed` | 1d4 applying-physical-hit-or-slashing | start | 1 | `soldier.overwatch.bleed:<ownerCharacterId>` |
| `thief.bloodleech.bleed` | 1d4 applying-physical-hit-or-slashing | start | 2 | `thief.bloodleech.bleed:<ownerCharacterId>` |
| `thief.shadow-stab.bleed` | 1d4 applying-physical-hit-or-slashing | end | 2 | `thief.shadow-stab.bleed:<ownerCharacterId>` |
| `thief.vein-cutter.bleed` | 1d4 applying-physical-hit-or-slashing | end | 2 | `thief.vein-cutter.bleed:<ownerCharacterId>` |
| `thief.ashblood.periodic` | 1 fire | start | 2 | `thief.ashblood.periodic:<ownerCharacterId>` |
| `warrior.splinter-bone-fangs.bleed` | 1d4 applying-physical-hit-or-slashing | start | 2 | `warrior.splinter-bone-fangs.bleed:<ownerCharacterId>` |
| `warrior.gore-maw.bleed` | 1d4 applying-physical-hit-or-slashing | start | 2 | `warrior.gore-maw.bleed:<ownerCharacterId>` |
| `warrior.eviscerator-protocol.bleed` | 1d4 applying-physical-hit-or-slashing | start | 2 | `warrior.eviscerator-protocol.bleed:<ownerCharacterId>` |
| `druid.charbear.burn` | 1d4 fire | end | 1 | `druid.charbear.burn:<ownerCharacterId>` |
| `mage.elemental-bolt.burn` | 1d4 fire | start | 1 | `mage.fire-focus-burn:<ownerCharacterId>` |
| `mage.elemental-fusion.burn` | 1d4 fire | start | 1 | `mage.elemental-fusion.burn:<ownerCharacterId>` |
| `mage.cascade-storm.burn` | 1d4 fire | end | 1 | `mage.cascade-storm.burn:<ownerCharacterId>` |
| `cleric.flame.burn` | 1d6 fire | start | 2 | `cleric.flame.burn:<ownerCharacterId>` |
| `cleric.divine-invocation.burn` | 1d6 fire | start | 1 | `cleric.divine-invocation.burn:<ownerCharacterId>` |
| `wizard.combo-surge.burn` | 1d6 fire | start | 1 | `wizard.combo-surge.burn:<ownerCharacterId>` |
| `tinker.burn-injector.burn` | 1d4 fire | end | 2 | `tinker.burn-injector.burn:<ownerCharacterId>` |
| `tinker.fire-bomb.burn` | 1d4 fire | end | 1 | `tinker.fire-bomb.burn:<ownerCharacterId>` |
| `core.bleeding` | affected creature PB source physical type or slashing | end | indefinite | `core.bleeding:<sourceIdentity>:<ownerCharacterId>` |
| `core.burning` | 1d4 fire | end | indefinite | `core.burning:<sourceIdentity>:<ownerCharacterId>` |

The table gives base profiles. Printed eligibility, saves, instance exceptions and reviewed duration upgrades still apply. Ashblood is deliberately outside the ongoing-fire family. The ordinary spell named Elemental Bolt is separate from the Mage class card and gains no class-card rider merely from a matching name.

## Feature interfaces

### cleric.judging-light

Active, unsuppressed eligibility.weakened or classification.curse qualifies; no owner restriction. A Curse class engine name or unclassified flavor text does not qualify. One added dice packet per qualifying Smite, not per condition.

Sources: [cleric.base.judging-light](../../data/public/class_playtests/cleric.json).

### thief.sneak-condition

Owned active family.bleeding, core.poisoned or thief.crippled can satisfy the condition route. Own legal multiclass effects qualify; the remaining weapon, turn, disadvantage and trigger requirements still apply.

Sources: [thief engine[0]](../../data/public/class_playtests/thief.json).

### thief.vile-tactics

Active Bleeding, Poisoned or Crippled target as stated in the card trigger. No invented owner restriction; several conditions do not multiply bonus.

Sources: [thief.hero.blackguard.vile-tactics](../../data/public/class_playtests/thief.json).

### warrior.terror-engine

Only this owner's Warrior-feature Shaken, Frightened or ACTIVE Disoriented. Count creatures, not effect records. At least two hostile creatures within 30 feet; pending Disoriented does not qualify.

Sources: [warrior.supplement.terror-engine](../../data/public/class_playtests/warrior.json).

### druid.snow-leopard

Explicit hostile Speed reduction or root tagged eligibility.slowed-foe qualifies. Prone, difficult terrain, cargo, Exhaustion, Grappled or Restrained alone do not.

Sources: [druid.hero.winterfang.snow-leopard](../../data/public/class_playtests/druid.json).

### warrior.mythic-carapace

Blocks family.bleeding, core.poisoned and family.ongoing-fire. This does not grant fire-damage immunity or blanket poison-effect immunity. Damage reduction and mutation refresh keep exact card limits.

Sources: [warrior.supplement.mythic-carapace](../../data/public/class_playtests/warrior.json).

### dragoon.wyrmhide

Advantage only on CON saves against registered Bleed, ongoing fire or Core Poisoned. It does not convert DEX extinguishing saves into CON saves or grant condition immunity.

Sources: [dragoon.hero.dragon-guardian.wyrmhide](../../data/public/class_playtests/dragoon.json).

### crimson.bleed-engine

Technical Crimson Bleed counters, spreading, detonations, Blood Mark prerequisites and named engine benefits require this owner's Crimson-engine instances. Broad end-all wording is separately bound. No allied healing replacement is hostile Bleed.

Sources: [crimson-agent engine[2]](../../data/public/class_playtests/crimson-agent.json), [crimson-agent engine[3]](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.base.blood-tithe](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.arch.bloodbound-edge](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.hero.thirstborn.blood-frenzy](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.hero.thirstborn.hemorrhagic-plague](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.hero.thirstborn.exsanguinate](../../data/public/class_playtests/crimson-agent.json).

### crimson.hemostasis

Arch Hemostasis ends all Bleed on the target irrespective of owner, subject to an expressly stated protected cure exception. Healing remains its printed fixed roll even with no Bleed. Bloodweaver Hemostasis instead replaces a new allied application with one bounded healing effect, never a hostile Bleed.

Sources: [crimson-agent.arch.hemostasis](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.hero.bloodweaver.hemostasis](../../data/public/class_playtests/crimson-agent.json).

### thief.persistent-bleed

Actual qualifying trigger refreshes one existing owned record, max(current remaining,2); if owner has Prolonged and underlying base duration is exactly2, replace2 with4. Do not revive expired records, change dice, create instances or exceed an express hard cap.

Sources: [thief.hero.shadowblade.persistent-bleed](../../data/public/class_playtests/thief.json).

### thief.prolonged-suffering

Owner-created Bleeds with printed base duration exactly2 use4 on application and qualifying refresh. Includes another legal class owned by same character; excludes base3 Crimson and Blood Curse. Base duration is not a hard cap; duration modifiers do not add unless explicit.

Sources: [thief.hero.blackguard.prolonged-suffering](../../data/public/class_playtests/thief.json).

### mage.arch-elemental-mastery

Adds one tick to a reviewed Fire Burn from a Mage card explicitly tagged focus, or an explicit Focus-Burn reference. Includes Focus passive, Inferno Lance, Elemental Bolt and Elemental Surge reference. Excludes Fusion and Cascade. Group arbitration still applies.

Sources: [mage.arch.elemental-mastery](../../data/public/class_playtests/mage.json), [mage.base.fire.fire](../../data/public/class_playtests/mage.json), [mage.base.elemental-bolt](../../data/public/class_playtests/mage.json), [mage.arch.elemental-surge](../../data/public/class_playtests/mage.json).

### oracle.burning-blood-boon-ii

An eligible ongoing fire rider from that paid Revelation use cannot be ended by mundane extinguishing. This does not create a new ongoing fire rider, convert other damage to a Burn, or protect unrelated effects.

Sources: [oracle.supplement.burning-blood.burning-blood-boon-ii](../../data/public/class_playtests/oracle.json).

### spell.seal-minor-wound

Select one eligible ordinary Bleed record and end that record. Shaman Blood Curse currently qualifies as Bleed; this does not remove an independently present curse, poison package, Wound or other affliction. The alternate stabilization choice restores no HP.

Sources: [ordinary spell: seal-minor-wound](../../data/public/spell_playtests/catalog.json).

## Bound definitions

### Shaken — `warrior.shaken`

-1 on attack rolls.

**Ending:** End of target next regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `warrior.terror-engine-state`

Sources: [warrior.supplement.carrion-signal-gland](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Shaken — `thief.shaken`

Disadvantage on next fear save. Shiver critical Reaction denial is separate.

**Ending:** Consumed by the next fear save or end of next target regular turn, whichever first.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [thief engine[2]](../../data/public/class_playtests/thief.json), [thief engine[3]](../../data/public/class_playtests/thief.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Weakened — `mage.dreadblade.weakened`

-1 on attack rolls.

**Ending:** End of target next regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `eligibility.weakened`

Sources: [mage engine[13]](../../data/public/class_playtests/mage.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Weakened — `wizard.dreadblade.weakened`

-1 on attack rolls.

**Ending:** End of target next regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `eligibility.weakened`

Sources: [wizard engine[22]](../../data/public/class_playtests/wizard.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Weakened — `warrior.weakened`

-1 damage on weapon/natural-weapon hits, minimum 0.

**Ending:** End of the second future regular target turn after application; an in-progress target turn is excluded. Preserve the original virtual marker across initiative changes. A legal reapplication refreshes without increasing the penalty.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `eligibility.weakened`

The reviewed combat timing overlay resolves the formerly ambiguous bare two-round hostile duration. Explicit source endpoints still take precedence.

Sources: [warrior.supplement.warpgrip-talons](../../data/public/class_playtests/warrior.json), [warrior.supplement.eviscerator-protocol](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md), [GPT_COMBAT_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_EXACT_FINDINGS.md), [GPT_STRAIN_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_FIRST_REVIEW.md).

### Crippled — `thief.crippled`

The active Crippler package: unspent -1 next attack; critical also half Speed. No arbitrary slow qualifies.

**Ending:** Normal ends on consuming next-attack penalty or printed expiry; critical lasts while either component remains.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

NEW binding links the otherwise undefined Crippled hook to the Crippler poison package.

Sources: [thief engine[3]](../../data/public/class_playtests/thief.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Slow — `thief.crippling-strike.slow`

Half Speed on failed CON save; no teleport denial.

**Ending:** End of next target regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `eligibility.slowed-foe`

Crippling Strike is not Crippled merely because of its name.

Sources: [thief.arch.crippling-strike](../../data/public/class_playtests/thief.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Dread — `oracle.dread`

-1 attack rolls and saving throws. Any Reaction denial is a separately timed rider.

**Ending:** Each listed source supplies duration, repeat saves and zone/concentration endpoint.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Only explicitly fear-based applications receive fear immunity; no universal fear tag from the word Dread.

Sources: [oracle.supplement.haunted.haunted-boon-iv](../../data/public/class_playtests/oracle.json), [oracle.supplement.ancestor.ghost-chant](../../data/public/class_playtests/oracle.json), [oracle.supplement.bones.unfinished-chorus](../../data/public/class_playtests/oracle.json), [oracle.supplement.dream.nightmare-lash](../../data/public/class_playtests/oracle.json), [oracle.supplement.dream.unreality](../../data/public/class_playtests/oracle.json), [oracle.supplement.dream.dream-prophecy](../../data/public/class_playtests/oracle.json), [oracle.supplement.shadow.psychic-lash](../../data/public/class_playtests/oracle.json), [oracle.supplement.shadow.mind-spike](../../data/public/class_playtests/oracle.json), [oracle.supplement.shadow.silent-hunter](../../data/public/class_playtests/oracle.json), [oracle.supplement.shadow.hush-descends](../../data/public/class_playtests/oracle.json), [oracle.supplement.shadow.shadow-prophecy](../../data/public/class_playtests/oracle.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Grief Mark — `paladin.grief-mark`

-1 attack rolls.

**Ending:** End of target next regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [paladin.supplement.oath-of-grief.mourning-smite](../../data/public/class_playtests/paladin.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Grief — `paladin.grief`

-1 attack rolls and saving throws against Fear.

**Ending:** End of target next regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [paladin.supplement.oathbreaker-oath-of-grief.death-touch-gravetongue](../../data/public/class_playtests/paladin.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Doomed — `cleric.doomed`

HP healing reduced by S+M, minimum 0. Finite positive buff deadlines on this target accelerate one round per regular target turn end.

**Ending:** Next Sacrament pulse or source Sacrament ending, whichever first.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

NEW: timestamp expiry subtracts6 seconds; initiative expiry moves one round toward present; overdue expires immediately. Never changes recharge, per-rest uses, permanent/class-path states or another creature timer. One acceleration per buff per regular target turn.

Sources: [cleric.hero.cultist.blasphemous-tongue](../../data/public/class_playtests/cleric.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Judged — `cleric.judged`

-1 AC.

**Ending:** End of the second future regular target turn after application; an in-progress target turn is excluded. Preserve the original virtual marker across initiative changes. A legal reapplication refreshes without increasing the penalty.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

The reviewed combat timing overlay resolves the formerly ambiguous bare two-round hostile duration. Explicit source endpoints still take precedence.

Sources: [cleric.base.judgment.judgment](../../data/public/class_playtests/cleric.json), [cleric.arch.divine-invocation](../../data/public/class_playtests/cleric.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md), [GPT_COMBAT_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_EXACT_FINDINGS.md), [GPT_STRAIN_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_FIRST_REVIEW.md).

### Fire Focus Burn — `mage.fire-focus.burn`

1d4 fire damage at start of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

Elemental Surge explicitly applies this profile. Arch Elemental Mastery grants one additional tick.
Independent Inferno schedule remains; only highest expected application in this group damages at a shared marker.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [mage.base.fire.fire](../../data/public/class_playtests/mage.json), [mage.arch.elemental-surge](../../data/public/class_playtests/mage.json), [mage.arch.elemental-mastery](../../data/public/class_playtests/mage.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Inferno Lance Burn — `mage.inferno-lance.burn`

1d6 fire damage at start of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

Requires failed initial save. Arch Elemental Mastery grants one additional tick.
Passive Fire Focus can legally apply on the same finisher; group arbitration prevents added shared ticks.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [mage.base.fire.fire](../../data/public/class_playtests/mage.json), [mage.arch.elemental-mastery](../../data/public/class_playtests/mage.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Shadow Rot — `monk.shadow-rot`

At start of each regular target turn, 1d4 psychic per stack. One stack penalizes first save that turn by 1; two penalize all saves that turn by 1. Maximum 2 stacks.

**Ending:** One WIS save at each regular target turn end ends all on success. Ends after second regular target turn following most recent application regardless.

**Stacking:** First stack starts two-turn shared clock; second adds stack and refreshes clock; further paid legal applications at cap refresh without creating a third.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

NEW regular-turn schedule and shared two-turn refresh; no additional ticks or saves on extra turns.

Sources: [monk.hero.way-of-shadow.nerve-fade-technique](../../data/public/class_playtests/monk.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Decay — `oracle.decay`

No HP recovery, -1 saves; +S flat allied attack damage once per attacker per turn and at most 3 allied hits/round; corpses within 2 tiles cannot be raised. Not doubled vulnerability.

**Ending:** Initial failed CON save begins; repeat CON save end each regular target turn; success ends all; third such endpoint ends regardless.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

NEW precise three-turn schedule; interaction with natural20/Stable recovery still under conference.
Blocks all HP increases, including natural-20 death recovery. Blocked natural 20 clears death counters and stabilizes at zero with one ordinary d4-hour deadline.
An already-due Stable recovery retains its absolute deadline while prohibited; ending prohibition resolves one HP only if still living, Stable and at zero. Damage/death cancels normally.
Legal positive-potential magical healing can trigger an applicable Bleed cure even with zero actual HP regained. Separately printed condition removal remains legal.

Sources: [oracle.supplement.bones.rotting-touch](../../data/public/class_playtests/oracle.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md).

### Vengeance Mark — `paladin.vengeance-mark.smite`

Owner Vengeance eligibility. S flat Smite bonus only if marked by same owner when Smite began.

**Ending:** End of owner next regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `eligibility.paladin-vengeance-marked`

Sources: [paladin.supplement.oath-of-vengeance.vengeful-smite](../../data/public/class_playtests/paladin.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Judgment Brand — `paladin.vengeance-mark.judgment-brand`

Owner Vengeance eligibility;19-20 melee critical range against target, difficult-terrain pursuit and once/round Reaction pursuit as printed.

**Ending:** Third future target regular-turn end, excluding an in-progress current target end. Preserve virtual marker; outside initiative bare3 rounds is application+18 elapsed seconds.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `eligibility.paladin-vengeance-marked`

Sources: [paladin.supplement.oath-of-vengeance.judgment-brand](../../data/public/class_playtests/paladin.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md), [GPT_CONTROL_STATE_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CONTROL_STATE_FIRST_REVIEW.md).

### Mark of Retribution — `paladin.vengeance-mark.retribution`

Owner Vengeance eligibility; next Smite adds 1d8; advantage opportunity attacks against target.

**Ending:** End of owner next regular turn. Spending the next-Smite die does not end this mark, its opportunity-attack advantage, or its shared Vengeance eligibility.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `eligibility.paladin-vengeance-marked`

Sources: [paladin.supplement.oath-of-vengeance.mark-of-retribution](../../data/public/class_playtests/paladin.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md).

### Blood Mark — `crimson-agent.blood-mark`

One owner target; enables only printed Blood Mark interactions. No automatic damage, vision or cover/planar bypass.

**Ending:** Five owner regular turns, encounter end, target death, replacement or printed consumption.

**Stacking:** One target per owner; replacement does not detonate old mark.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [crimson-agent.base.blood-mark](../../data/public/class_playtests/crimson-agent.json), [crimson-agent engine[3]](../../data/public/class_playtests/crimson-agent.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Vulnerable — `warrior.brutality-vulnerable`

Owner eligibility flag: perceived hostile within 60 feet, with 4 × current HP <= maximum HP. Never damage vulnerability.

**Ending:** Only while operative. Brutality Momentum uses the pre-damage snapshot; a killing hit cannot qualify itself by reducing the target to zero.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [warrior.base.brutality-sense](../../data/public/class_playtests/warrior.json), [warrior.arch.brutality-momentum](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md).

### Turned — `paladin.last-rites.turned`

Available voluntary movement must follow safest legal route away from protected creature; cannot willingly move closer. No Frightened or Action denial.

**Ending:** End of target next regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

NEW no displacement if Speed0/no legal route; retain other legal options.

Sources: [paladin.supplement.oath-of-grief.last-rites](../../data/public/class_playtests/paladin.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Disoriented (pending) — `warrior.disoriented.pending`

Scheduled transition only; does not yet qualify Terror Engine.

**Ending:** Start of target next regular turn transitions to active.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [warrior.supplement.wailing-eye-cluster](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Disoriented — `warrior.disoriented.active`

No Reactions. First voluntary movement, if elected, goes up to 5 feet in uniformly random legal horizontal direction; never free movement.

**Ending:** End of that target regular turn.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** `warrior.terror-engine-state`

NEW pending/operative split; actual movement mode/cost determine legality; no movement if no legal option.

Sources: [warrior.supplement.wailing-eye-cluster](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Stasis — `warrior.cellular-reconstruction.stasis`

Speed 0; no Actions/Bonus Actions/Reactions; attacks against have advantage. No automatic Incapacitated/Unconscious/Prone/death-save inheritance.

**Ending:** Start of owner next regular turn, then printed healing and cure if alive.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [warrior.hero.ironskin.cellular-reconstruction](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Bloodbond — `crimson-agent.bloodbond`

Only the printed damage-redirection/temp-HP relationship.

**Ending:** Concentration, three owner turns, range 30 feet and printed link limits.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [crimson-agent.hero.bloodweaver.bloodbond](../../data/public/class_playtests/crimson-agent.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Mirrorbind — `mirrorsage.mirrorbind`

Ability-capture Action and archive procedure, not a condition applied by the word bind.

**Ending:** Printed capture/slot procedure.

**Stacking:** No numerical stacking; independent source records retain their printed endpoints.

**Immunity:** Only explicit applicable immunity or this definition/application's reviewed tag; do not infer from display name.

**Tags:** No shared family tag.

Sources: [mirrorsage engine[1]](../../data/public/class_playtests/mirrorsage.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SECOND_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SECOND_REVIEW.md).

### Crimson Bleed — `crimson-agent.bleed`

1d4 physical damage at start of each of the next 3 regular target turns.

**Ending:** After 3 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

Default instance cap is one. Blood Echo permits two independent instances; third refreshes oldest.
Arterial Cut extends one existing instance by two ticks to maximum five remaining.
Blood Echo adds one to one instance next tick once on an owner turn; include that actual due bonus in group expectation.
No BG or proc generation from periodic damage. A spread instance cannot spread again.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "kitAction": {
    "uses": 1,
    "actor": "self or adjacent helper",
    "automatic": true,
    "scope": "all Crimson-engine Bleed instances from one source owner on this victim",
    "provenance": "Printed automatic kit endpoint; NEW one-use consumption."
  },
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [crimson-agent engine[2]](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.base.arterial-cut](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.base.hemorrhage-slash](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.arch.blood-echo](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.arch.rupture-trigger](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.hero.thirstborn.hemorrhagic-plague](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.hero.thirstborn.pain-to-power-conduction](../../data/public/class_playtests/crimson-agent.json), [crimson-agent.hero.thirstborn.bloodstorm](../../data/public/class_playtests/crimson-agent.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Dragoon Bleed — `dragoon.bleed`

1d4 physical damage at start of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

Impale Bleeding binds this engine profile; pin and Bleed have independent endings.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "kitAction": {
    "uses": 1,
    "actor": "self or adjacent helper",
    "automatic": true,
    "scope": "selected Dragoon Bleed record",
    "provenance": "Printed kit endpoint; NEW one-use consumption."
  },
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [dragoon engine[4]](../../data/public/class_playtests/dragoon.json), [dragoon.hero.dragon-tyrant.sovereign-descent](../../data/public/class_playtests/dragoon.json), [dragoon.hero.dragon-tyrant.tyrant-s-impale](../../data/public/class_playtests/dragoon.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Dragoon Burn — `dragoon.burn`

1d4 fire damage at start of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [dragoon engine[4]](../../data/public/class_playtests/dragoon.json), [dragoon.hero.drake-rider.drakestorm-dive](../../data/public/class_playtests/dragoon.json), [dragoon.hero.dragon-tyrant.sovereign-descent](../../data/public/class_playtests/dragoon.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Weapon Synergy Bleed — `ranger.synergy.bleed`

1d4 physical damage at end of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [ranger engine[1]](../../data/public/class_playtests/ranger.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Fire Imbue Burn — `ranger.imbue.burn`

1d4 fire damage at end of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [ranger engine[2]](../../data/public/class_playtests/ranger.json), [ranger.arch.elemental-imbue](../../data/public/class_playtests/ranger.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Emberroot Burn — `ranger.emberroot.burn`

1d4 fire damage at end of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [ranger engine[4]](../../data/public/class_playtests/ranger.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Blood Curse Bleed — `shaman.blood-curse.bleed`

1d4 necrotic damage at start of each of the next 3 regular target turns.

**Ending:** After 3 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "saveToEnd",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "applying Shaman class DC"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "Printed Medicine/healing-save endpoints; reviewed ordinary explicit-removal eligibility.",
  "magicalHealingSave": {
    "ability": "CON",
    "dc": "applying Shaman class DC",
    "scope": "one save per active Blood Curse record"
  },
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [shaman.hero.bloodcaller.blood-curse](../../data/public/class_playtests/shaman.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Bloodroot Trail Bleed — `shaman.bloodroot.bleed`

1d4 slashing damage at end of target next regular turn. Initial zone damage remains necrotic.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

Initial zone damage remains necrotic. The separately untyped Bleed uses the explicit type bridge; not inferred from the zone.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [shaman.hero.bloodcaller.bloodroot-trail](../../data/public/class_playtests/shaman.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Flame Totem Burn — `shaman.flame-totem.burn`

1d4 fire damage at end of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [shaman engine[1]](../../data/public/class_playtests/shaman.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Burn Flask — `shaman.flask.burn`

1d4 fire damage at end of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [shaman engine[4]](../../data/public/class_playtests/shaman.json), [shaman.base.flask-use](../../data/public/class_playtests/shaman.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Cinderflame Burn — `shaman.cinderflame.burn`

1d4 fire damage at end of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [shaman.hero.theurgist.summon-cinderflame](../../data/public/class_playtests/shaman.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Overwatch Bleed — `soldier.overwatch.bleed`

1d4 physical damage at start of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [soldier engine[1]](../../data/public/class_playtests/soldier.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Bloodleech Bleed — `thief.bloodleech.bleed`

1d4 physical damage at start of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

Requires failed poison save; critical healing is a separate once-per-dose consequence.
One recipe instance per target/owner; maximum two different active poison recipes from this owner.
Ending the sole ongoing Bleed component ends this recipe instance occupancy; resolved critical healing never keeps an empty recipe slot occupied.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [thief engine[2]](../../data/public/class_playtests/thief.json), [thief engine[3]](../../data/public/class_playtests/thief.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Shadow Stab Bleed — `thief.shadow-stab.bleed`

1d4 physical damage at end of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [thief.arch.shadow-stab](../../data/public/class_playtests/thief.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Vein Cutter Bleed — `thief.vein-cutter.bleed`

1d4 physical damage at end of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

Specific effect preserves two Bleed ticks despite shorter general duration field.
Speed -10 lasts through end next regular target turn; -1 next attack damage is consumed or expires at that same endpoint.
Consumes a prepared poison without its normal recipe effect and does not occupy a normal recipe-instance slot.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [thief.hero.shadowblade.vein-cutter](../../data/public/class_playtests/thief.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Ashblood periodic poison — `thief.ashblood.periodic`

1 fire damage at start of each of the next 2 regular target turns.

**Ending:** After two due ticks, or when an explicitly reviewed poison-effect removal ends the remaining recipe rider.

**Stacking:** One Ashblood recipe instance per owner/target; reapplication refreshes under Thief poison-engine rules. No Bleeding or ongoing-fire family arbitration.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** No shared family tag.

Internal poison-recipe delayed fire; explicitly excluded from family.ongoing-fire. Can coexist with a Burn-family tick.
Poison damage immunity blocks poison damage only; Core Poisoned immunity blocks only actual Poisoned components. Explicit immunity to poison effects/toxins is checked separately against the application.
Failed recipe save still required; critical no-HP-recovery ends end next regular turn separately from the two-tick fire.
One recipe instance per owner/target and maximum two different ongoing poison recipes from that owner.

**Exact cure metadata:**

```json
{
  "ordinaryExtinguishable": false,
  "corePoisonedRemovalApplies": false,
  "underlyingPoisonRemoval": "Only an explicitly reviewed cure covering active poison recipe effects can remove remaining recipe riders.",
  "expiry": "Two scheduled ticks; recipe can be refreshed under Thief engine rules.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [thief engine[2]](../../data/public/class_playtests/thief.json), [thief engine[3]](../../data/public/class_playtests/thief.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Mutation Bleed — Splinter Bone Fangs — `warrior.splinter-bone-fangs.bleed`

1d4 physical damage at start of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [warrior.supplement.splinter-bone-fangs](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Mutation Bleed — Gore Maw — `warrior.gore-maw.bleed`

1d4 physical damage at start of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [warrior.supplement.gore-maw](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Mutation Bleed — Eviscerator Protocol — `warrior.eviscerator-protocol.bleed`

1d4 physical damage at start of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.bleeding`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [warrior.supplement.eviscerator-protocol](../../data/public/class_playtests/warrior.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Charbear Burn — `druid.charbear.burn`

1d4 fire damage at end of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

Nearby aura damage and smoke are separate effects; family immunity does not negate their unrelated components.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [druid.hero.ashen-grove.charbear](../../data/public/class_playtests/druid.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Elemental Bolt Fire rider — `mage.elemental-bolt.burn`

1d4 fire damage at start of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

Explicit new attached-fire classification in the Mage Fire Focus stack group.
Its card is explicitly tagged focus: Arch Elemental Mastery adds one tick. Elemental Fusion and Cascade lack that tag and do not receive this upgrade.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [mage.base.elemental-bolt](../../data/public/class_playtests/mage.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Elemental Fusion Fire + Cold rider — `mage.elemental-fusion.burn`

1d4 fire damage at start of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

Only Fire+Cold pair applies this rider; separate Speed reduction retains its own endpoint.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [mage.hero.elementalist.elemental-fusion](../../data/public/class_playtests/mage.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Cascade Storm first fire hit rider — `mage.cascade-storm.burn`

1d4 fire damage at end of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

Only first fire target gets this rider. NEW missing-marker fallback is end next regular target turn.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [mage.hero.elementalist.cascade-storm](../../data/public/class_playtests/mage.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Flame Invocation fire — `cleric.flame.burn`

1d6 fire damage at start of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [cleric.base.flame.flame](../../data/public/class_playtests/cleric.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Divine Invocation Flame fire — `cleric.divine-invocation.burn`

1d6 fire damage at start of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [cleric.arch.divine-invocation](../../data/public/class_playtests/cleric.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Combo Surge Fire + Cold fire — `wizard.combo-surge.burn`

1d6 fire damage at start of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

Fire damage rider and failed-STR Restrained component are separate; ending one does not silently end the other.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [wizard.hero.elementalist.combo-surge](../../data/public/class_playtests/wizard.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Burn Injector — `tinker.burn-injector.burn`

1d4 fire damage at end of each of the next 2 regular target turns.

**Ending:** After 2 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [tinker engine[3]](../../data/public/class_playtests/tinker.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Fire Bomb Burn — `tinker.fire-bomb.burn`

1d4 fire damage at end of each of the next 1 regular target turns.

**Ending:** After 1 due ticks, or an applicable ending method. Losing arbitration consumes a due tick.

**Stacking:** Same owner/source profile refreshes without adding dice; source-group caps apply before family arbitration. Independent records retain their endpoints.

**Immunity:** Explicit family immunity applies only to the registered family. Damage resistance/immunity uses the actual damage type. An immune or suppressed record cannot satisfy active-effect hooks.

**Tags:** `family.ongoing-fire`

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [tinker engine[4]](../../data/public/class_playtests/tinker.json).

Review: [GPT_CUSTOM_RIDER_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRST_REVIEW.md), [GPT_CUSTOM_RIDER_SCOPE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_SCOPE_REVIEW.md), [GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_CUSTOM_RIDER_FIRE_CURE_REVIEW.md), [CODEX_PERIODIC_PROFILE_CONFERENCE](../../../../docs/audit/2026-10-08/full-game/CODEX_PERIODIC_PROFILE_CONFERENCE.md), [GPT_PERIODIC_PROFILE_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_PROFILE_REVIEW.md), [GPT_PERIODIC_REFRESH_CLOSURE](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_REFRESH_CLOSURE.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Core Bleeding — `core.bleeding`

At the end of the affected creature's regular turn, take damage equal to its current PB, unless the selected reviewed application prints a different magnitude. Use that application's specified physical type; if none, slashing.

**Ending:** Persists until its source or applicable cure ends it. Self or adjacent helper spends an Action selecting one present eligible Bleed record before a WIS (Medicine) check: printed cure DC, otherwise recorded applying effect/class/spell DC, otherwise 10. Success or Critical Success ends that record only. One legal magical healing event with positive pre-cap/pre-prohibition potential ends all ordinary records with an automatic-healing endpoint, even at full HP or while Corrupted/Decay prevents actual HP gain. Each Shaman Blood Curse instead gets its own printed CON save. Explicit end-one/end-all removers retain exact scope and protected-source exceptions.

**Stacking:** Independent source-owner records enter unified family arbitration at their actual marker. No DC tie-break or separate generic damage layer. Medicine ends one selected record; positive-potential magical healing ends all eligible automatic-cure records.

**Immunity:** Creatures explicitly immune to bleeding/blood-loss effects cannot gain it. Specific spell/class/item Bleeding numbers replace the generic PB magnitude only when printed.

**Tags:** `family.bleeding`

SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "specialCureRequired": false,
  "artifactLevel": false,
  "magicalHealingEndpoint": "end",
  "magicalHealingScope": "every eligible present record on recipient",
  "positivePotentialRequired": true,
  "actualHpGainRequired": false,
  "medicine": {
    "activation": "Action",
    "actor": "self or adjacent helper",
    "ability": "WIS",
    "skill": "Medicine",
    "dcPrecedence": [
      "printed cure DC",
      "recorded applying effect/class/spell DC",
      "10"
    ],
    "scope": "one eligible record selected before roll"
  },
  "explicitRemoval": "Use remover exact one/all/owner restrictions.",
  "provenance": "NEW explicit gap-fill endpoints from periodic-profile conference; not inherited from family membership.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [Core condition: bleeding](../../data/playtest/condition_playtests.json).

Review: [GPT_GENERIC_CUSTOM_ALIGNMENT](../../../../docs/audit/2026-10-08/full-game/GPT_GENERIC_CUSTOM_ALIGNMENT.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

### Core Burning — `core.burning`

At end of the affected creature's regular turn its generic record offers 1d4 fire damage to unified family arbitration, unless its source specifies another magnitude. Only the winning stack group deals damage. Damage immunity does not by itself remove Burning.

**Ending:** Self or adjacent helper may spend one Action to end all active ordinary-extinguishable attached fires on this creature. Full immersion of all burning portions does the same. Explicit protected-source exceptions survive. At each regular target turn end, after due ticks are consumed, each surviving active ongoing-fire record with future damage remaining makes its own binary DEX save against its own source DC or 10. Success ends only that record. An indefinite generic fire counts as having future damage; a finite record with its final tick consumed expires without another save.

**Stacking:** Independent records enter unified ongoing-fire family arbitration. One Action/full immersion clears all ordinary-extinguishable records; DEX saves operate per surviving eligible record, not one selected-source save for all fires.

**Immunity:** Fire immunity prevents the damage but does not automatically end Burning unless the source or immunity says so. An effect explicitly immune to Burning blocks application.

**Tags:** `family.ongoing-fire`

SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review.

**Exact cure metadata:**

```json
{
  "ordinaryConditionRemoval": true,
  "ordinaryExtinguishable": true,
  "mundaneMethods": [
    "Action by self or adjacent helper",
    "full immersion of all burning portions"
  ],
  "mundaneScope": "all eligible ordinary-extinguishable attached-fire records on chosen creature; explicit exceptions survive",
  "endingSave": {
    "ability": "DEX",
    "dcPrecedence": [
      "printed ending DC",
      "recorded source DC",
      "10"
    ],
    "marker": "end of regular target turn after any end-turn tick",
    "eligibility": "record still present, including suppressed/condition-immune, with at least one future scheduled tick remaining",
    "scope": "this record only"
  },
  "sourceException": "A printed prohibition on mundane extinguishing disables those mundane methods only.",
  "provenance": "NEW explicit periodic-profile overlay; magical origin alone does not prohibit extinguishing.",
  "explicitRemoval": "Use remover exact one/all/owner restrictions; explicit removal is distinct from generic Action/full-immersion extinguishing.",
  "presenceRule": "Existing unexpired/not-ended record, including suppressed/condition-immune records. Actual cure method/endpoint/prerequisites still required."
}
```

Sources: [Core condition: burning](../../data/playtest/condition_playtests.json).

Review: [GPT_GENERIC_CUSTOM_ALIGNMENT](../../../../docs/audit/2026-10-08/full-game/GPT_GENERIC_CUSTOM_ALIGNMENT.md), [GPT_PERIODIC_EXACT_FINDINGS](../../../../docs/audit/2026-10-08/full-game/GPT_PERIODIC_EXACT_FINDINGS.md), [GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [GPT_HEALING_DEATH_FIRST_REVIEW](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_DEATH_FIRST_REVIEW.md).

## Open integration work

- Complete source-qualified hook references and remaining root/slow/curse/disease/mark metadata.
- Apply reviewed common round-marker defaults to every remaining source; resolve mark effects whose source/target clock is still ambiguous.
- Semantically classify all active class/spell rider references; reference integrity does not prove exhaustive semantic coverage.

The [machine report](CUSTOM_CONDITION_BINDING_VALIDATION.json) explicitly separates source integrity from selected interface checks and preserves this unfinished registry status.
