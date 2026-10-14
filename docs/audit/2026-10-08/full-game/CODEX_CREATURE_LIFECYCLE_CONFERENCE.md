# Creature companions, undead and form dependencies: source conference

Codex → Calibration Review. Next bounded source slice: 100 exact passages from Druid, Mage, Mirrorsage, Ranger and Wizard, plus three frozen shared paragraphs. This includes all 83 passages for those families in the original broad 230-row inventory and 17 semantic supplements that the original keyword scan missed. The original inventory remains preserved; candidate count is not a completeness claim.

Please keep the reply below 18,000 characters. Give every supplied ID a concise classification: operational creature lifecycle/command role, modifier, guard/exclusion, previously reviewed interface or deferred form/temp-HP rule. Do not blanket-close the five classes. No new named abilities, spells or monster stat blocks: use exact supplied procedures and identify NEW integration rulings explicitly.

Source precedence: exact source, applicable reviewed shared rule, narrow source interpretation, then explicitly labeled NEW integration only where needed. Existing maximum-HP review already covers Conjuration and Flesh Ascendant snapshot/dynamic contribution, same-effect alias identity and capacity-only increases; preserve it. Existing healing, control and periodic interfaces also stay in force. The human-readable procedure and engine contract must describe one ruleset.

Resolve these exact boundaries before implementation:

1. **Different kinds of zero HP and return.** Frozen standard summoned companions disappear at zero. Ranger's Beast is a permanent bond with persistent injury and death requiring a new bond after long rest. Mage Lich elites explicitly return at full HP after completed long rest, with Soulbound Ritual for earlier half-HP return. Wizard elite text supplies caps/profiles but no explicit acquisition or return procedure. Which kinds use living HP/Wounds/death saves, immediate disappearance/death, recoverable assets or no return permission? Do not import Tinker reconstruction into living companions.

2. **Creation and lifetime.** Specify source snapshots versus current owner level/PB/ability/S/DC for base HP, AC, saves and attacks; persistent Beast differs from finite familiar/swarm. Healing does not refill expiry, command uses, recharge or spent effects. Clarify duration, concentration, dismissal/replacement and controller incapacity/death only when the supplied sources establish it. Missing Wizard elite binding method/time/cost must remain an evidence gap rather than an invented power.

3. **Outer command ledger.** One owner, including multiclass companions, shares the reviewed BA command and damaging-action limit by numbered round. Mage/Wizard impose narrower regular-turn command eligibility. Their wording includes damaging OR control command: does a non-damaging control command spend the shared damaging/control allowance, preventing a later Gadget Sync attack? Which support commands leave damage allowance unspent? Ghoul Lash's two printed attacks are one exact exception within one command, not two commands.

4. **Source-native triggers from companions.** Standard uncommanded companions move defensively/Dodge but may not independently deal damage or impose control. Do persistent Miasma zones created by a paid command keep their scheduled entry/start damage without another command? Does their damage debit a new round's damaging allowance or only the originating command? Wraithbound invisibility/recharge clocks need an owner-relative regular virtual marker even if companions have no independent damaging turn. Apply existing hard-denial/no-recursion limits.

5. **Undead capacity and corpses.** Wizard standard cap three and elite cap one each/three total; Mage Lich elites have their own printed cap. For multiclass Mage/Wizard access to the same three named elites, are the assets/caps shared or separate? No duplicate free bodies without an explicit ruling. Corpse Harvest consumes one eligible humanoid corpse (Fiends with Pact; Goblin Thrall only goblinoid); how do removal, dismissal, duplicate fragments and destruction affect re-use? Do summoned/raised remains ever become eligible corpses? Earlier source explicitly bans corpse/resource farming.

6. **Auto-Raise queue.** Once per round, standard minion personally lands eligible killing blow while below cap; rise at current-turn end as same type if physically possible, cannot act that round. Define reservation/payment-free slot checks at trigger and resolution, simultaneous deaths, corpse consumed by another event, source minion destroyed before resolution, cap filled meanwhile, turn-end expiry ordering and invalid bodies. No dismissal to force an automatic over-cap raise. Ghoul Lash may supply two hits but only the printed single Auto-Raise opportunity. Resolve Goblin Thrall killing a non-goblinoid and ordinary humanoid versus Fiend with Pact.

7. **Mage familiar and elites.** One familiar matching current Focus at creation; changing Focus later must not silently transform/refill it unless source says so. Lich readiness gates are guards, not instructions for this agent to perform any ritual/retirement. Soulbound half-HP return and tempHP remain subject to legal target/state, command ledger and exact cost/frequency. Return must not reset already-spent independent abilities unless a real rest reset says so. Does Soulbound preserve current eligible effects/recharge clocks, and does completed-LR full return reset them only through the real rest rules?

8. **Ranger Beast bond.** One willing/tamed noncorrupted beast, INT<7, CR<=class level, bounded companion profile plus Wisdom HP; one retained movement mode capped40 and keen-sense advantage. No CR-stat-block import. Establish whether HP bonus uses actual WIS or M, minimum viable max, dynamic/snapshot stats, healing/rest procedure, death timing and new-bond aftermath. A wounded beast cannot be resummoned/rebonded to refill itself. Exact acquisition action/time/cost absent from the card should be identified.

9. **Mirror Beast versus Reflective Companion.** One or the other, never both. Mirrorcall gives +M maximum/current HP on summon; appearance changes do not heal or reset. Reflective Companion is the original creature under temporary control, not a new healing/reconstruction profile; control end restores disposition with actual state preserved. Its ordinary attack is capped S d6, no unique powers. How does it fit prior initiative, commands, hostile/friendly targeting and repeated-save timing without duplicate turns? Existing control rules should govern, not new hidden permanent ownership.

10. **Mirror-origin Echo.** The owner's Action plus a BA command and normal RP/record consumption are needed; Beast may attack OR originate the release. Radiant Beast attack, paid heal or paid Echo are exclusive that round. A source-origin point does not transfer casting ownership, concentration, Dissonance/Refrain or release-cap identity to the Beast. Confirm targeting distance/line-of-effect origin versus owner-required visibility and atomic failure behavior.

11. **Druid swarm dependencies.** Shared single-companion profiles have printed overrides. Carrion Rat King replaces its prior form swarm. Broodmother creates two on entry using the stated Form Surge, but one combined damaging command and both end with form. Does ordinary Rotshaper Swarm Summoning end when the Druid changes form, or only form-granted summons? engine[3] says changing form ends old form features/summons; distinguish source origin. Master of Vermin's substitution changes a paid spell's creature profile without multiplying creatures or casts.

12. **Form/temporary-HP exclusions.** Many supplied candidates are incidental form, resource or tempHP mentions. Classify them without pretending full transformation reserves, all form cards, repeated tempHP auras or class resources are closed. Source engine[0]/[1] supplements establish retained character stats and acquisition, so forms cannot be mistaken for independent companions or extra HP pools. The next form/tempHP audit can supply the remaining exact cards.

Please identify missing adjacent source passages required to settle these questions. All decisions will be saved in a separate overlay, then implemented, tested and returned for exact disposition. No historical source text will be deleted or rewritten.

### druid.engine[3]

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "text": "Shifting: Bonus Action, one long-rest shift use, 10 minutes, early reversion Bonus Action. Reaching 0 HP or incapacitation ends form; excess damage stays on your own HP. Shift uses follow detailed book table:2 at 1, 3 at 4, 4 at 7, 5 at 10, 6 at 13, 7 at 16, 8 at 19. Supplemental runtime alternative 2/3/4/5/6 at 1/4/8/12/16 remains preserved. At 20 changing form is unlimited but does not refill finite form benefits. Speech unavailable in Base forms, available in Arch/Hero. No spellcasting in form until Beast Spells 18 except an explicit form permission. Maintaining an existing spell concentration is allowed, still only one concentration. Changing form spends a use and ends old form features/summons; it does not reset once/rest abilities."
}

### druid.engine[4]

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "text": "Transformation reserves prevent unlimited replacement HP: at long rest record Buffer Reserve=2 L+M and Form Surge Reserve=PB. A form giving temporary HP draws that many from Buffer Reserve, up to remaining amount, with normal nonstacking; never real healing. A form special described once/transformation also spends 1 Form Surge and cannot be refreshed by resuming the form. Form Surge refills only long rest. Forms cannot grant free casts, RP or shift uses. Auras affect at most 3 enemies and once per enemy per round; retaliation once/round total; ongoing riders refresh, never stack. Entering a legal Shapeshift clears the Refrain counter and remembered repeated-spell name, as the protected source contract requires. It does not reduce accumulated Dissonance. Natural attacks do not clear Refrain."
}

### druid.base.shapeshifting

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Shapeshifting",
  "activation": "Bonus Action",
  "cost": "One shift use",
  "rangeAndTarget": "Self",
  "duration": "10 minutes",
  "frequency": "Long-rest uses in engine",
  "effect": "Assume an unlocked prepared form or revert early. Apply engine HP, equipment, concentration and reserve rules. This is not a spell and cannot copy monster stat blocks."
}

### druid.base.bear-form-tank

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Bear Form (Tank)",
  "activation": "Action attack; passive form traits",
  "cost": "One shift; buffer drawn from reserve",
  "rangeAndTarget": "Self; claw 5 ft",
  "duration": "While in Bear",
  "frequency": "One claw/Action",
  "effect": "Gain up to 20 temporary HP from reserve; AC max(normal, 14). Claw 2d6 slashing+WIS+1. Buffer disappears on reversion and cannot be refilled through free shifting."
}

### druid.hero.archdruid

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Archdruid",
  "activation": "Bonus Action",
  "cost": "0 shift uses; other costs remain",
  "rangeAndTarget": "Self",
  "duration": "10 minutes/form",
  "frequency": "Automatic capstone",
  "effect": "Unlimited legal form changes. Buffer Reserve and Form Surges remain finite; per-rest powers, spell costs and uses never refresh on changing form. Ignore verbal/somatic and noncostly unconsumed material components for Druid spells, including in form."
}

### druid.arch.dire-wolf

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Dire Wolf",
  "activation": "Action attack or Howl",
  "cost": "One shift; Howl 1 Form Surge",
  "rangeAndTarget": "Self; bite 5 ft; Howl 30 ft",
  "duration": "Form 10 minutes; fear up to 3 rounds",
  "frequency": "Howl 1/shift and finite reserve",
  "effect": "Arch attunement required. Speed 40 ft, bite 2d6 piercing+WIS; advantage when active ally threatens target 5 ft. Howl Action up to 3 enemies WIS save or Frightened, repeat end each turn, maximum 3 rounds. No free bite with Howl."
}

### druid.arch.earth-warden-dire-bear

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Earth Warden (Dire Bear)",
  "activation": "Action Slam",
  "cost": "One shift; buffer reserve",
  "rangeAndTarget": "Self; 10 ft radius up to 3 creatures",
  "duration": "While in Earth Warden",
  "frequency": "Slam recharge 2",
  "effect": "Arch attunement required. Gain up to 30 temp HP from reserve, nonmagical physical resistance. Slam DEX save 2d6 bludgeoning+WIS and Prone on failure, half damage no Prone success. Ordinary claw 1d8+WIS when Slam unavailable."
}

### druid.arch.sky-serpent

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Sky Serpent",
  "activation": "Action bite; passive traits",
  "cost": "One shift",
  "rangeAndTarget": "Self; bite 5 ft",
  "duration": "While in Sky Serpent",
  "frequency": "One bite/Action",
  "effect": "Arch attunement required. Flight 80 ft with hover, +2 DEX saves. Bite 2d8 lightning+WIS. Once/shift may spend 1 Form Surge to add 1d4 against wet target; no repeated electrical propagation."
}

### druid.arch.shadow-lynx

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Shadow Lynx",
  "activation": "Reaction Blink; Action claw",
  "cost": "One shift; Blink 1 Form Surge",
  "rangeAndTarget": "Self; claw 5 ft",
  "duration": "Blink instant; form 10 minutes",
  "frequency": "Blink 1/shift and finite reserve",
  "effect": "Arch attunement required. Claw 2d4+WIS magical slashing; +2 Stealth while motionless. When attack would hit, Reaction teleport 30 ft to visible empty space, causing triggering attack to miss if you leave its reach/range. Next claw before end next turn advantage. No blanket immunity to magical damage."
}

### druid.base.moon.combat-shapeshifting

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Combat Shapeshifting",
  "activation": "Bonus Action",
  "cost": "1 to S RP",
  "rangeAndTarget": "Moon Circle self in form",
  "duration": "Instant",
  "frequency": "Once/own turn",
  "effect": "Restore 1d8 real HP per RP paid, never beyond maximum. Does not restore temporary buffer or shift uses. No Dissonance as class technique; cannot heal after form ended/incapacitated."
}

### druid.hero.moon.beastlord-alpha-animal-hybrid

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Beastlord (Alpha Animal Hybrid)",
  "activation": "Action bite or Howl",
  "cost": "One shift; Howl 1 Form Surge",
  "rangeAndTarget": "Moon Hero; bite 5 ft/Howl 15 ft",
  "duration": "While in Beastlord; fear 1 turn",
  "frequency": "Howl 1/shift and finite reserve",
  "effect": "Bite 2d6+WIS piercing; first hit/turn adds 1d4 of one chosen fire/cold/lightning, not all three. Up to 2 beast allies 30 ft gain+1 first attack/turn. Howl Action up to 3 enemies WIS save or Frightened until end next turn."
}

### druid.hero.moon.mooncursed

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Mooncursed",
  "activation": "Action bite or Howl",
  "cost": "One shift; Howl 1 Form Surge",
  "rangeAndTarget": "Moon Hero; bite 5 ft/Howl 30 ft",
  "duration": "While in Mooncursed",
  "frequency": "Howl 1/shift and finite reserve",
  "effect": "Resistance to nonmagical physical damage except silver; other types unchanged. Bite 2d6+WIS piercing, +1d8 once/turn under real full moon. Howl Action choose up to 3 allies gain 2d8 temp HP total roll, or 3 enemies WIS save or Frightened through end next turn. Temp HP draws from Buffer Reserve per recipient."
}

### druid.hero.moon.elemental-shapeshifting

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Elemental Shapeshifting",
  "activation": "Bonus Action",
  "cost": "One shift and one elemental use",
  "rangeAndTarget": "Moon Circle self",
  "duration": "10 minutes",
  "frequency": "2/long rest",
  "effect": "Choose bounded elemental form: AC 16, natural attack 2d8+WIS chosen element, one/Action. Air flight 60 lightning resistance; Earth burrow 20 through loose soil physical DR 2; Fire fire resistance and melee attacker 1d4 fire once/round; Water swim 60 water breathing cold resistance. Retain own HP/abilities, no external stat blocks."
}

### druid.hero.storm.tempest-raptor

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Tempest Raptor",
  "activation": "Action claw; passive traits",
  "cost": "One shift",
  "rangeAndTarget": "Storm Hero; claw 5 ft",
  "duration": "While in Tempest Raptor",
  "frequency": "One claw/Action; retaliation once/round",
  "effect": "Flight 60 ft, advantage on saves against wind/lightning while airborne. Claw 2d6+WIS lightning; wet target adds 1d4 once/shift for 1 Form Surge. After melee hit on you, attacker takes 1d6 lightning once/round; no repeated disarm chains."
}

### druid.hero.storm.thunderhorn-stag

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Thunderhorn Stag",
  "activation": "Action antlers or Thunder Step",
  "cost": "One shift; Step 1 Form Surge",
  "rangeAndTarget": "Storm Hero; antlers 5 ft; teleport 30 ft",
  "duration": "While in Thunderhorn Stag",
  "frequency": "Step 1/shift and finite reserve",
  "effect": "Antlers 1d8+WIS piercing; after 20 ft approach first hit/turn also 2d8 thunder and CON save or Deafened through end next turn. Step Action teleport 30 ft, departure 10 ft radius up to 3 creatures CON save 2d8 thunder, half success. Sense natural storm approach 24 hours, no exact prediction of magical weather."
}

### druid.hero.winterfang.frost-wyrmling

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Frost Wyrmling",
  "activation": "Action breath or claw",
  "cost": "One shift; breath one short-rest use",
  "rangeAndTarget": "Winterfang Hero; 30 ft cone up to 3 creatures",
  "duration": "While in Frost Wyrmling",
  "frequency": "Breath 1/short rest, shared across shifts",
  "effect": "AC normal+2, cold immunity. Claw 1d8+WIS cold. Breath 4d6 cold DEX half. One breath target may have cold resistance ignored once/shift for 1 Form Surge; immunity remains. No general physical resistance from cold terrain in this draft."
}

### druid.base.rotshaper.swarm-summoning

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Swarm Summoning",
  "activation": "Action",
  "cost": "One short-rest use",
  "rangeAndTarget": "Rotshaper Circle; empty space 30 ft",
  "duration": "Concentration, 10 minutes",
  "frequency": "1/short rest",
  "effect": "Summon one swarm using shared companion profile: AC 12+floor(PB/2), HP 2 L, Speed 30, melee attack PB+WIS for S d6 piercing. Bonus Action command, one damaging action across all pets. Tiny-body movement through 1 inchgaps; no separate attacks per insect."
}

### druid.hero.rotshaper.carrion-rat-king

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Carrion Rat King",
  "activation": "Action bite or summon",
  "cost": "One shift; summon 1 Form Surge",
  "rangeAndTarget": "Rotshaper Hero; bite 5 ft/swarm 30 ft",
  "duration": "While in Carrion Rat King",
  "frequency": "Summon 1/shift and finite reserve",
  "effect": "Bite 1d8+WIS piercing+2d6 poison; CON save or Poisoned through end next turn. Immune disease/Poisoned, not poison damage. Summon Action creates one bounded engine swarm 1 minute, same command budget; replaces previous form swarm."
}

### druid.hero.rotshaper.insect-broodmother

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Insect Broodmother",
  "activation": "Action bite; passive traits",
  "cost": "One shift; spawning 1 Form Surge",
  "rangeAndTarget": "Rotshaper Hero; up to 2 swarms adjacent",
  "duration": "While in Insect Broodmother",
  "frequency": "Spawn once/shift and finite reserve",
  "effect": "AC normal+3, climb 30 walls/ceilings, bite 1d8+WIS piercing. On entry optional spend surge spawn 2 bounded shared profile swarms, both end with form, combined one commanded attack/turn. Once/shift for another Form Surge turn one crit against you into normal hit; no infinite insects."
}

### druid.hero.rotshaper.master-of-vermin

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Master of Vermin",
  "activation": "Bonus Action",
  "cost": "One shift",
  "rangeAndTarget": "Rotshaper Circle self",
  "duration": "10 minutes",
  "frequency": "Normal shift limit",
  "effect": "Swarm form: own HP/AC, physical resistance, Speed 30, fit Tinygaps, natural attack S d6+WIS piercing. No flight unless choosing bats (flight 30), which forfeits physical resistance. Replacing a summoning spell's beast with swarm uses same single companion budget and paid spell, never multiplied dice/creatures."
}

### druid.base.ashen-grove.blazing-rebirth

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Blazing Rebirth",
  "activation": "Reaction",
  "cost": "One long-rest use",
  "rangeAndTarget": "Ashen Grove; ally/self 30 ft taking fire damage",
  "duration": "After damage",
  "frequency": "1/long rest",
  "effect": "Grant L+M temporary HP after real hostile/environmental fire damage. Cannot reduce triggering hit retroactively or trigger from deliberate ally/self-farming. Normal temporary HP nonstacking; no buffer reserve payment because finite feature use."
}

### druid.hero.ashen-grove.charbear

data/public/class_playtests/druid.json

Original broad lifecycle inventory

{
  "name": "Charbear",
  "activation": "Action claw or Smoke",
  "cost": "One shift; Smoke 1 Form Surge",
  "rangeAndTarget": "Ashen Hero; claw 5 ft/aura 5 ft/smoke 10 ft",
  "duration": "While in Charbear; smoke 3 rounds",
  "frequency": "Smoke 1/shift; aura/retaliation caps",
  "effect": "Claw 2d8+WIS fire; first hit/turn Burn 1d4 next turn. Up to 3 enemies starting 5 ft CON save or 1d6 fire. Smoke Action opaque 10 ft radius sphere centered fixed point you occupy, concentration 3 rounds; all vision blocked, no poison in this draft. Wind 20 mph disperses."
}

### mage.engine[9]

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "text": "All sources share a maximum of one additional full Action per creature per round. Additional Actions cannot grant additional Actions, Bonus Actions or Reactions. Mage summons and companions do not receive independent damaging turns: all Mage-controlled conjured companions share one Companion Command per Mage regular turn. Spend one Bonus Action to command exactly one companion to move up to its Speed and use one damaging or control action from its stat block. Uncommanded companions may move to remain near you and take Dodge but cannot deal damage or impose control."
}

### mage.engine[11]

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "text": "LICH COMPANION SYSTEM. A successful Lich transformation unlocks three unique bound elite companions: Boneflayer, Dreadblade and Wraithbound. You can maintain at most one of each, maximum three total. They return at full HP after a completed long rest unless a campaign consequence expressly prevents it. A destroyed elite leaves no usable corpse and cannot generate XP, loot, RP, Nuke Chain credit, Soul Reservoir or kill-based resources. Soulbound Ritual can return one before a long rest."
}

### mage.engine[17]

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "text": "LICH RITUAL CHECK. After all readiness gates and the divine-echo encounter are completed, roll d20 + Intelligence modifier + Constitution modifier against DC 20, applying the third-guardian +2 and willing-participant advantage where applicable. Success completes the Lich transformation and unlocks its cards and elite companions. Failure after explicit consent applies the historical failure state and the Director pauses for the agreed player-to-NPC handoff before continuing play. No silent PC deletion is permitted."
}

### mage.base.resonance-shield

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Resonance Shield",
  "activation": "Bonus Action",
  "cost": "Spend X RP, where X is 1, 2 or 3",
  "rangeAndTarget": "Self",
  "duration": "1 minute or until temporary HP are lost",
  "frequency": "Recharge 2 rounds",
  "effect": "Resonance Shield. Tags: mage-spell, abjuration, protection. Spend 1-3 RP and gain temporary HP equal to X × (S + M). Temporary HP do not stack. This spell is non-elemental and therefore clears an active Elemental Nuke Chain. Its RP payment cannot be reduced below 1 by Spell Efficiency."
}

### mage.arch.conjure-elemental-familiar

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Conjure Elemental Familiar",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "One unoccupied space within 30 feet",
  "duration": "10 minutes",
  "frequency": "1/long rest",
  "effect": "Conjure Elemental Familiar. Tags: mage-spell, arcanist, summon, elemental. Summon one elemental familiar matching your current Focus using the common familiar stat block. Only one elemental familiar from this feature may exist at once; summoning another dismisses the first. It obeys the shared Companion Command rule. It disappears at 0 HP or when duration ends and leaves no corpse, XP, loot or resource trigger."
}

### mage.hero.archmage.empowered-link

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Empowered Link",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Up to M allies within 25 feet",
  "duration": "Matches the shared benefit, maximum until end of your next regular turn",
  "frequency": "At most once per turn",
  "effect": "Empowered Link. Tags: archmage, buff. When one of your Mage cards grants you temporary HP, a Speed bonus or a numeric attack/save bonus, choose up to M allies within 25 feet. They gain the same non-resource benefit at half its numeric amount rounded down, minimum 1 where applicable. It never shares Actions, RP, Focus, concentration, invisibility, summons or class resources. Resistance is not a numeric bonus and is not shared by this card."
}

### mage.hero.archmage.harmonized-core

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Harmonized Core",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "One ally within 30 feet",
  "duration": "Temporary HP until lost or replaced",
  "frequency": "At most once per turn",
  "effect": "Harmonized Core. Tags: archmage, support. After one of your damaging Mage spells deals damage, choose one ally within 30 feet. It gains temporary HP equal to 10% of one target's unmodified rolled damage dice total from that spell, rounded down, minimum 1 and maximum S+M. This is not HP healing and cannot trigger healing features or Echo-style repetitions."
}

### mage.hero.archmage.arcane-sanctuary

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Arcane Sanctuary",
  "activation": "Action",
  "cost": "6 RP to start; 1 RP maintenance",
  "rangeAndTarget": "15-foot-radius fixed zone centered within 30 feet",
  "duration": "Concentration, maximum 3 Mage turns",
  "frequency": "Recharge 4 rounds",
  "effect": "Arcane Sanctuary. Tags: mage-spell, archmage, zone, concentration. On start and each paid Bonus Action maintenance pulse, allies in the zone gain S+M temporary HP until the start of your next regular turn or effect end, whichever is first and +1 to Mage or spell attack rolls while inside. The zone grants no save-DC increase and no additional Actions. Maximum 3 pulses."
}

### mage.hero.archmage.spell-sharing

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Spell Sharing",
  "activation": "Action",
  "cost": "4 RP plus the shared card's printed RP cost",
  "rangeAndTarget": "One willing ally within 30 feet",
  "duration": "Until end of ally's next regular turn",
  "frequency": "1/short rest",
  "effect": "Spell Sharing. Tags: archmage, spell-sharing. Choose one Base or Arch Mage spell card you know with an Action activation and printed base RP cost 4 or less. Pay both costs now. The ally may cast that card once before the end of its next turn without paying RP, using your Mage spell attack and DC. It cannot share summons, Counterspell, Hero cards, finishers, Resonance Surge or another Spell Sharing."
}

### mage.hero.elementalist.elemental-supremacy

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Elemental Supremacy",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Self and current Focus finisher",
  "duration": "Permanent",
  "frequency": "Always; reset at most once per round",
  "effect": "Elemental Supremacy. Tags: elementalist, focus, vulnerability. Once on each of your turns when a Mage spell deals a damage type to which its target is vulnerable, add S damage of that type after vulnerability is applied. Additionally, when a hostile non-summoned creature that meaningfully threatened the party dies from one of your Focus-eligible spells, you may reset your current Focus finisher's positive recharge counter to 0, subject to the universal reset limit."
}

### mage.hero.elementalist.primal-channeling

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Primal Channeling",
  "activation": "Bonus Action",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Instantaneous",
  "frequency": "1/short rest",
  "effect": "Primal Channeling. Tags: elementalist, resonance. During a real encounter, draw ambient elemental energy and restore 2 RP, never above your maximum. You cannot use Primal Channeling outside a real encounter, during a rest, through a summoned proxy or more than once per short rest. It does not count as a spell cast, does not advance Nuke Chain and does not alter Dissonance."
}

### mage.hero.lich.soul-reservoir

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Soul Reservoir",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Instantaneous",
  "frequency": "At most once per turn and at most S times per encounter",
  "effect": "Soul Reservoir. Tags: lich, resonance, damage-over-time. During a real encounter, when a hostile creature takes damage from a damage-over-time effect created by one of your Mage spells, restore 1 RP, never above maximum. The same damage event cannot restore more than 1 RP. Damage to allies, summons, trivial creatures or your own companions does not qualify."
}

### mage.hero.lich.necromantic-mastery

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Necromantic Mastery",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your necrotic Mage spells",
  "duration": "Permanent",
  "frequency": "Always",
  "effect": "Necromantic Mastery. Tags: lich, necromancy. Once on each of your turns when a Mage spell deals necrotic damage, add S necrotic damage to one damaged target. Your necrotic Mage spells also ignore resistance to necrotic damage; immunity remains immunity. This feature does not convert another spell's damage type and cannot apply to companion attacks unless a card explicitly identifies them as your spell."
}

### mage.hero.lich.lingering-malice

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Lingering Malice",
  "activation": "Action",
  "cost": "5 RP to start; 1 RP maintenance",
  "rangeAndTarget": "15-foot-radius fixed zone centered within 60 feet",
  "duration": "Concentration, maximum 3 Mage turns",
  "frequency": "Recharge 4 rounds",
  "effect": "Lingering Malice. Tags: mage-spell, lich, necrotic, zone, concentration. Choose Fear or Drain when cast. On start and each paid Bonus Action maintenance pulse, enemies in the zone make Wisdom saves. Failure takes S d6 necrotic. Fear mode also Frightens until the start of your next turn. Drain mode lets you gain temporary HP equal to M once per pulse if at least one enemy fails. Maximum 3 pulses; each pulse grants a new save."
}

### mage.hero.lich.resonance-to-flesh

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Resonance to Flesh",
  "activation": "Action",
  "cost": "Variable conversion",
  "rangeAndTarget": "Self",
  "duration": "Instantaneous",
  "frequency": "1/short rest",
  "effect": "Resonance to Flesh. Tags: lich, resonance, blood. Choose one direction. RP to Flesh: spend 1-5 RP and regain 2 HP per RP spent. Flesh to RP: lose 2-10 HP in even increments and restore 1 RP per 2 HP lost. HP loss cannot be reduced, redirected or transferred and cannot reduce you below 1 HP. RP cannot exceed maximum. This feature cannot be repeated through Echoes or companions."
}

### mage.hero.lich.corpse-gateway

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Corpse Gateway",
  "activation": "Bonus Action",
  "cost": "2 RP",
  "rangeAndTarget": "One visible corpse within 60 feet and one unoccupied space within 5 feet of it",
  "duration": "Instantaneous",
  "frequency": "Recharge 2 rounds",
  "effect": "Corpse Gateway. Tags: mage-spell, lich, teleportation, corpse. Teleport to the chosen unoccupied space adjacent to a visible corpse. The corpse is not consumed or altered. Summoned-companion remains, repeated fragments of the same destroyed creature and illusory corpses are not legal anchors. This non-elemental spell clears an active Nuke Chain."
}

### mage.hero.lich.soulbound-ritual

data/public/class_playtests/mage.json

Original broad lifecycle inventory

{
  "name": "Soulbound Ritual",
  "activation": "Action",
  "cost": "5 RP",
  "rangeAndTarget": "One of your destroyed bound elite undead companions within 30 feet or its inert binding token",
  "duration": "Instantaneous",
  "frequency": "1/long rest",
  "effect": "Soulbound Ritual. Tags: mage-spell, lich, companion, resurrection. Return one destroyed Boneflayer, Dreadblade or Wraithbound to an unoccupied space within 30 feet at half its maximum HP. It gains S+M temporary HP for 1 minute. The returned companion remains subject to the shared Companion Command limit and cannot create a corpse, XP, loot or resource event if destroyed again."
}

### mirrorsage.engine[1]

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "text": "Mirrorbind is an Action, once per encounter, against a creature within 60 ft whose eligible ability you saw resolve since the start of your previous turn. Target must have INT 6 or lower, not be a boss or possess unique/legendary status unless an encounter script explicitly permits copying. It makes WIS save versus class DC; failure captures one witnessed ability into an empty slot. No copying from allies, your companions, another copy, a corpse, a recharge-limited legendary power or an at-will source that itself restores resources. You can voluntarily erase a slot without an action on your turn, permanently losing its record."
}

### mirrorsage.engine[2]

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "text": "Record source creature/name, witnessed ability, category, damage type, allowed rank, capture encounter and whether first release has occurred. For this pilot, capture copies the observed role into ONE bounded profile: Strike=one target 60 ft class spell attack S d8 observed damage type; Burst=up to 3 enemies in 10 ft radius within 30 ft DEX save S d6, half on success; Mend=one living ally 30 ft S d6+M HP; Ward=one ally 30 ft S d6+M temporary HP for 1 minute; Hindrance=one enemy 30 ft WIS save or Speed-10 ft and no Reactions until end its next turn. Choose only a profile actually expressed by the observed source; physical attack cannot become healing. Rank is max(1, ceil(source challenge rating/2)); if source lacks a rating the Director assigns a rank before the encounter, not after seeing a desirable ability. Rank cannot exceed your Mirrorsage learnable rank; no copying character levels from a creature. Damage/targets/control are capped by these profiles, not source boss dice."
}

### mirrorsage.engine[4]

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "text": "One Mirror Beast OR Reflective Companion, never both. Mirror Beast uses standard companion stats, initially copies appearance only, and costs a Bonus Action to command. You may command it to make its normal attack OR originate your round's Echo Release from its position, paying RP and consuming the record normally; not both. You still supply an Action for release unless a feature specifically changes that action cost. A shifted appearance grants no extra actions/stats. Destroying/dismissing it grants no capture, corpse, XP or recovery. Charm Bind is 1/long rest, 3 rounds, concentration, INT 6-or-lower target WIS save and repeat at each turn end/when harmed by your side; never a player character or boss without explicit encounter permission. A charmed companion uses its own ordinary attack with damage capped at standard companion S d6; unique spells/powers remain unavailable."
}

### mirrorsage.engine[6]

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "text": "Standard acquisition applies; baseline Mirrorbind, Echo Release and summon procedure become usable by selecting their cards. Echo Channeling and Mirrorcall are upgrades, not duplicate mandatory unlocks. The contradiction between source initial 3 slots and Expansion I 2→3 is reconciled as an archive-safety upgrade below. Perfect Reflection automatic 9, Hero choice 10, corresponding Final 20. The finale does not override copy eligibility or the shared release cap."
}

### mirrorsage.base.mirrorcall

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Mirrorcall",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your Mirror Beast",
  "duration": "While it exists",
  "frequency": "Continuous",
  "effect": "Beast gains+M maximum/current HP when summoned and+5 ft Speed. Echo Release or Mirror Beast Summon already provides its base procedure; this is an optional enhancement, not a second required unlock."
}

### mirrorsage.base.mirror-beast-summon

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Mirror Beast Summon",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "One empty space within 15 ft",
  "duration": "1 minute",
  "frequency": "Recharge 3",
  "effect": "Summon one standard Mirror Beast; replaces any prior Beast/Reflective Companion. Choose appearance of a stored source. It attacks only on Bonus Action command or originates your paid release with Action+command, never both. No copied anatomy, regeneration or immortality."
}

### mirrorsage.base.charm-creature

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Charm Creature",
  "activation": "Action",
  "cost": "3 RP; 1 long-rest use",
  "rangeAndTarget": "One eligible INT 6-or-lower creature within 30 ft",
  "duration": "Concentration, at most 3 rounds",
  "frequency": "1/long rest",
  "effect": "WIS save or become Reflective Companion under engine restrictions. It repeats save at turn end and when harmed by your side. Replaces Mirror Beast; on end original disposition returns. Requires no suicidal orders; cannot force beliefs or permanently enslave."
}

### mirrorsage.arch.advanced-mirrorcall

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Advanced Mirrorcall",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your Mirror Beast",
  "duration": "While summoned",
  "frequency": "Once/encounter",
  "effect": "You may change Beast appearance to another stored source as a Bonus Action without resummoning or restoring HP. It gains either+10 ft swim or climb Speed until it ends. No new release, attack or capture."
}

### mirrorsage.arch.mirror-shift

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Mirror Shift",
  "activation": "Bonus Action",
  "cost": "1 RP",
  "rangeAndTarget": "Your Mirror Beast within 60 ft",
  "duration": "Remaining summon duration",
  "frequency": "Recharge 2",
  "effect": "Switch its appearance to a stored source and choose swim 30 ft or climb 30 ft until next shift. Restore no HP or attacks; no flight, incorporeality or copied creature special actions. Does not release or consume the Echo."
}

### mirrorsage.hero.light-weaver.luminant-bond

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Luminant Bond",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Allies/enemies within 10 ft of your Beast/Companion",
  "duration": "While companion exists",
  "frequency": "Continuous",
  "effect": "Allies gain+1 to WIS saves. Invisible enemies in aura shed faint outlines and cannot gain advantage solely from invisibility, but concealment/cover still apply. This grants neither full True Sight nor targeting through walls."
}

### mirrorsage.hero.light-weaver.radiant-archive

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Radiant Archive",
  "activation": "Action",
  "cost": "RP for 3 support Echoes; consume all 3; 1 long-rest use",
  "rangeAndTarget": "Up to 3 legal allies within 30 ft",
  "duration": "Instant/shield 1 minute",
  "frequency": "1/long rest",
  "effect": "Release three stored Mend/Ward records as ONE package; assign each to one ally. No ally receives more than two components and temporary HP never stack. All costs paid; no extra release or resurrection. Missing records cannot be invented."
}

### mirrorsage.hero.light-weaver.radiant-mirror-beast

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Radiant Mirror Beast",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "Empty space within 15 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 4",
  "effect": "Summon radiant standard Beast. Bonus Action command chooses normal attack or healing S d4 to one living ally within 5 ft, paying 1 RP per heal. It may instead originate your paid Echo release under common limits. Cannot perform two options in one round."
}

### mirrorsage.hero.light-weaver.blessing-echo

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Blessing Echo",
  "activation": "Action",
  "cost": "Recorded RP cost+1; consume offensive Echo",
  "rangeAndTarget": "One living ally within 30 ft",
  "duration": "Instant or 1 minute shield",
  "frequency": "Recharge 3",
  "effect": "Convert a stored Strike/Burst record to Mend/Ward for this release, chosen on activation; heal S d6+M or grant same temporary HP. This explicit conversion cannot also deal offensive damage or copy a condition."
}

### mirrorsage.hero.light-weaver.light-binding

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Light Binding",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "Up to 2 creatures within 30 ft",
  "duration": "Until end your next turn",
  "frequency": "Recharge 3",
  "effect": "Choose mode: enemies make STR save or Restrained; they repeat save at turn end. OR up to 2 allies gain S d6+M temporary HP. No mixed modes; bonds are magical and not permanent objects."
}

### mirrorsage.hero.shattered-one.corrupted-mirrorcall

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Corrupted Mirrorcall",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Your Beast on summoning",
  "duration": "Summon duration",
  "frequency": "Once/summon",
  "effect": "Roll d2:1 Ember grants its one commanded attack+1d4 fire; 2 Barbs grants+1d4 piercing. Extra dice apply once/round only. Mutation grants no aura damage, poison supply, resource gain or separate creature."
}

### mirrorsage.hero.shattered-one.shattered-mirror-beast

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Shattered Mirror Beast",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "Empty space within 15 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 4",
  "effect": "Summon standard corrupted Beast. On commanded hit add 1d6 necrotic once/round; after that hit, each other creature within 5 ft of Beast, including allies, takes 1 psychic damage. This splash has no procs and cannot trigger another splash. Normal companion cap applies."
}

### mirrorsage.hero.shattered-one.echo-leech

data/public/class_playtests/mirrorsage.json

Original broad lifecycle inventory

{
  "name": "Echo Leech",
  "activation": "Triggered",
  "cost": "1 RP",
  "rangeAndTarget": "Self after direct Echo damages a hostile creature",
  "duration": "Instant",
  "frequency": "Once/round",
  "effect": "Pay 1 RP to regain HP equal to min(M, actual damage dealt to one target). Copies, Do Ts and companion attacks do not trigger it. Healing has no secondary healing/resource procs; no damage means no heal."
}

### ranger.engine[1]

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "text": "Weapon Synergy tracks last successful direct weapon hit on your own turns. Changing melee→ranged grants+1 to that ranged attack roll if it is your first attack of the turn; changing ranged→melee makes the hit apply Bleed 1d4 on target's next 2 turns. Once/turn synergy; Do Ts, copies, companions, forced attacks and misses do not advance it. At 5 ordinary Attack Action makes two attacks; techniques use only printed counts. You may draw/stow one weapon as normal object interaction; Dual Style later improves this."
}

### ranger.engine[3]

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "text": "Druidic Arrow Combo starts at Ranger 11, not at Base 1. Each direct successful weapon hit adds 1 Hit Chain, maximum 2 gained per regular turn and cap 3. Completing 3 primes one Arrow until end next turn; using it consumes the chain, even on miss. Efficient Killer lowers threshold 2. Chain starts/ends encounters 0, cannot be stocked against allies/captives/summons and is cleared by incapacitation. The Arrow is one Action with a ranged weapon attack or the stated save, costs 0 RP when primed, and is a magical class technique rather than an ordinary spell cast. At most one Arrow per round; it cannot advance its own chain. It requires a wielded bow and ammunition. Ordinary attack/damage riders apply once as printed, never another free arrow."
}

### ranger.engine[5]

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "text": "Chosen Hero grants a sixth Arrow at 11. Warder Nature's Wrath: ranged attack weapon+S d6 piercing; up to 2 allies within 10 ft gain M temporary HP (finite mitigation, not repeatable real healing). Stalker Phantom: two ranged attacks against different aligned targets within 60 ft, each weapon damage, no extra dice; one Arrow activation. Outrider Corruption: place 10 ft-radius zone within 60 ft, concentration until start next turn; up to 3 enemies entering/starting there take S d4 necrotic once each, CON half. Arrow copies cannot generate extra attacks, resources or permanent terrain changes."
}

### ranger.engine[7]

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "text": "Base choices 1–2, Pathfinder Arch 3–9, and chosen Warder/Stalker/Outrider Hero 10–20 are distinct stages. No source Arch capstone/Finale exists: level 9 receives its normal eligible choice, while 20 automatically improves your Hero Arrow once/long rest (new capstone below). Do not acquire a Hero by spending Base choices. Beast Companion is one permanent bond; it must be a willing/tamed noncorrupted beast with INT<7 and CR no greater than your class level. Its combat profile uses the bounded companion below rather than importing a full CR 20 monster."
}

### ranger.base.weapon-bond

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "name": "Weapon Bond",
  "activation": "Ritual",
  "cost": "0; 1 hour during rest",
  "rangeAndTarget": "One bow or pair of blades touched",
  "duration": "Until rebonded",
  "frequency": "One bond",
  "effect": "Bond weapons. Bonus Action summons one bonded weapon to your hand from within 30 ft if not held by another creature and no total cover. Cannot disarm someone or cross planar boundaries; bond no additional items."
}

### ranger.hero.warder.beast-empathy

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "name": "Beast Empathy",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Natural beasts within 30 ft that hear you",
  "duration": "While communicating",
  "frequency": "Continuous",
  "effect": "Communicate simple emotions/directions. They are not automatically friendly or controlled, cannot answer beyond their experience, and may need normal Animal Handling. No language-based compulsion or extra companion slot."
}

### ranger.hero.warder.healing-touch

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "name": "Healing Touch",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "One other ally healed by your paid spell/item",
  "duration": "Instant",
  "frequency": "Once/turn",
  "effect": "Add M HP to actual healing. Do not multiply potion dice or duplicate consumed items; cannot apply to regeneration, companions' healing, copies or another Ranger's same bonus."
}

### ranger.hero.warder.nature-s-blessing

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "name": "Nature's Blessing",
  "activation": "Action",
  "cost": "3 RP",
  "rangeAndTarget": "One willing ally within 30 ft",
  "duration": "Concentration, 3 of your turns",
  "frequency": "Recharge 3",
  "effect": "Ally gains+10 ft Speed and S d6+M temporary HP on start. While effect lasts it has advantage on saves against forced movement. Temporary HP are not refreshed each turn."
}

### ranger.hero.warder.beast-companion

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "name": "Beast Companion",
  "activation": "Ritual",
  "cost": "4 RP; 1 hour with a willing/tamed eligible beast",
  "rangeAndTarget": "One beast touched",
  "duration": "Bond persists; one companion",
  "frequency": "1/long rest",
  "effect": "Bond eligible beast using standard companion stats plus Wisdom modifier HP; preserve one movement mode up to 40 ft and keen-sense advantage. Bonus Action command gives one attack, no imported boss powers. Injury persists; heal normally. Death requires a new bond after long rest, not free resummoning."
}

### ranger.hero.outrider.predator-s-grin

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "name": "Predator's Grin",
  "activation": "Triggered",
  "cost": "1 short-rest use",
  "rangeAndTarget": "Self after directly reducing quarry to 0",
  "duration": "Your next regular turn",
  "frequency": "1/short rest",
  "effect": "Gain one extra full Action next turn within the shared cap. It cannot grant another Action or trigger another Predator's Grin. Allies, summons, helpless creatures and ongoing copied damage do not qualify."
}

### ranger.supplement.master-of-the-hunt-new-hero-capstone

data/public/class_playtests/ranger.json

Original broad lifecycle inventory

{
  "name": "Master of the Hunt — new Hero capstone",
  "activation": "Triggered",
  "cost": "1 long-rest use",
  "rangeAndTarget": "One legal chosen Hero Arrow",
  "duration": "That Arrow",
  "frequency": "1/long rest",
  "effect": "New playtest Hero capstone. Once per long rest when using your Hero Arrow, pay its normal Hit Chain/action requirements, then enhance only that activation: Warder grants 2 M temporary HP instead of M; Stalker adds S d6 piercing to one of its two hits; Outrider adds S d4 necrotic to one target on its single pulse. No extra Arrow, Hit Chain, action or copied proc."
}

### wizard.engine[10]

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "text": "ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn."
}

### wizard.engine[18]

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "text": "SUMMON COMMAND LIMIT. All Wizard-controlled conjured, raised and bound companions share one damaging/control Companion Command per Wizard regular turn. Spend one Bonus Action to command exactly one such creature to move up to its Speed and use one damaging or control action from its stat block. Uncommanded creatures may reposition defensively and take Dodge but cannot deal damage or impose conditions. No summoned or raised creature can create XP, treasure, RP, Dissonance relief, additional corpses or kill-resource farms."
}

### wizard.engine[21]

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "text": "ELITE UNDEAD PETS. Necromancers may bind Boneflayer, Dreadblade and Wraithbound, at most one of each and three elite pets total. They use the same shared Companion Command limit as standard undead. Boneflayer: AC 14, HP 12 + 2 × Wizard level, Speed 30. Bone Shards: range 60, Wizard spell attack, 2d6+S necrotic. Fear Pulse replaces its attack: enemies within 10 feet make Wisdom saves; failure Frightened until end of next turn; recharge 3. Grave Miasma replaces its attack: 10-foot-radius point within 30 feet until start of your next turn; enemies entering or starting there take 1d6 necrotic once; recharge 3."
}

### wizard.engine[24]

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "text": "Flesh Ascendant's bonus applies after the listed base statistics: every undead creature you control gains +2 maximum HP per Wizard level. If at least two of your undead creatures are active, each gains +1 AC and +1 on saving throws. This does not increase the standard-minion or elite-pet caps."
}

### wizard.arch.arcane-sight

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Arcane Sight",
  "activation": "Action",
  "cost": "2 RP",
  "rangeAndTarget": "Self; 60-foot sight",
  "duration": "Concentration, maximum 10 minutes",
  "frequency": "Recharge 2 rounds",
  "effect": "Arcane Sight. Tags: arch, active, wizard-spell, divination, concentration. While active you perceive magical auras within 60 feet and automatically know each visible aura's school or broad magical category. As an Action on a later turn, examine one aura to learn whether it is concentrated, summoned, cursed, warded or linked to another visible magical effect. Total cover blocks sight."
}

### wizard.hero.spellbinder.knowledge-shield

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Knowledge Shield",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Allies directly protected by one of your Abjuration Wizard spells",
  "duration": "Until start of your next regular turn",
  "frequency": "At most once per ally per round",
  "effect": "Knowledge Shield. Tags: hero, spellbinder, passive, protection. When you cast an Abjuration spell that grants AC, temporary HP, resistance or a saving-throw benefit to an ally, that ally also gains +2 on its next saving throw before the start of your next regular turn. Multiple Knowledge Shields do not stack."
}

### wizard.hero.spellbinder.matrix-sharing

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Matrix Sharing",
  "activation": "Action",
  "cost": "2 RP plus the shared spell's normal RP cost",
  "rangeAndTarget": "One willing ally within 30 feet",
  "duration": "Until end of ally's next regular turn",
  "frequency": "1/short rest",
  "effect": "Matrix Sharing. Tags: hero, spellbinder, passive-upgrade, matrix. Choose one prepared Wizard spell of rank 3 or lower with an Action casting time. Pay both costs now. The ally may cast that spell once before the end of its next turn without paying RP, using your spell attack and DC. The shared spell cannot summon creatures, create additional Actions, use Overcast, be Shared again or bypass concentration limits. Granting this permission takes your Action; the ally spends its own normal Action to cast. The ally owns concentration and strain for the cast, and it does not update your matrix-family history or grant you cast-trigger resources."
}

### wizard.hero.spellbinder.spell-absorption

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Spell Absorption",
  "activation": "Reaction",
  "cost": "4 RP",
  "rangeAndTarget": "One hostile spell that directly targets you",
  "duration": "Instantaneous",
  "frequency": "1/short rest",
  "effect": "Spell Absorption. Tags: hero, spellbinder, wizard-spell, abjuration. Trigger after you become the target of a hostile spell but before it resolves. Make an Intelligence check adding proficiency against DC 10 + twice the spell rank. On success that spell has no effect on you, though it resolves normally against other targets, and you gain temporary HP equal to spell rank + M. On failure it resolves normally and the use is spent."
}

### wizard.hero.elementalist.arcane-fusion

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Arcane Fusion",
  "activation": "Action",
  "cost": "Combined normal RP costs of both spells + 2 RP",
  "rangeAndTarget": "As the two selected spells",
  "duration": "Instantaneous or as individual legal effects",
  "frequency": "1/long rest",
  "effect": "Arcane Fusion. Tags: hero, elementalist, fusion, matrix. Choose two DIFFERENT prepared Wizard spells of rank 5 or lower, neither of which summons a creature or grants an additional Action. Pay both full RP costs plus 2 and resolve both spells sequentially as one Action. They may share or have different legal targets. They cannot both require concentration. Each matrix separately updates protected first-cast/Refrain state, but features triggered by 'casting a spell' may trigger only once from the Fusion, chosen by you. Fusion itself cannot be copied, Shared or used inside Dual Cast."
}

### wizard.hero.necromancer.flesh-ascendant

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Flesh Ascendant",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Undead creatures you control",
  "duration": "Permanent while active",
  "frequency": "Always",
  "effect": "Flesh Ascendant. Tags: hero, necromancer, passive, undead. Each undead creature you control gains +2 maximum HP per Wizard class level. While at least two of your undead creatures are active, each also gains +1 AC and +1 on saving throws. These bonuses apply after the common standard-minion and elite-pet statistics and do not increase companion caps or command frequency."
}

### wizard.hero.necromancer.arcane-leech

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Arcane Leech",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Until temporary HP are lost",
  "frequency": "At most once per turn",
  "effect": "Arcane Leech. Tags: hero, necromancer, passive. When at least one hostile creature fails a saving throw against one of your Wizard spells, gain temporary HP equal to S+M. Multiple failed targets from the same spell do not multiply the amount. This does not drain actual HP, generate RP or trigger from your companions' abilities."
}

### wizard.hero.necromancer.binding-sigil

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Binding Sigil",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "One creature directly affected by your Wizard spell",
  "duration": "Until end of your next regular turn",
  "frequency": "At most one marked creature at a time",
  "effect": "Binding Sigil. Tags: hero, necromancer, passive, mark. After one creature takes damage from or fails a save against your Wizard spell, you may mark it. Until the end of your next regular turn you have advantage on Wizard spell attacks against that creature. Marking another creature ends the previous mark. Echoes, companions and environmental damage cannot apply it."
}

### wizard.hero.necromancer.corpse-harvest

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Corpse Harvest",
  "activation": "Action",
  "cost": "4 RP",
  "rangeAndTarget": "One eligible humanoid corpse within 30 feet",
  "duration": "Until destroyed, dismissed or your next long rest",
  "frequency": "Recharge 2 rounds; standard-minion cap 3",
  "effect": "Corpse Harvest. Tags: hero, necromancer, wizard-spell, undead, summon. Raise the corpse as a Skeleton or Zombie using the common standard-undead statistics; a goblinoid corpse may instead become a Goblin Thrall. The corpse is consumed into that minion state. The creature obeys the shared Bonus Action Companion Command rule. Creating a fourth standard minion requires dismissing one existing standard minion first."
}

### wizard.hero.necromancer.ghoul-lash

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Ghoul Lash",
  "activation": "Bonus Action",
  "cost": "2 RP",
  "rangeAndTarget": "One of your standard undead minions with another allied undead within 5 feet",
  "duration": "For this command",
  "frequency": "At most once per round",
  "effect": "Ghoul Lash. Tags: hero, necromancer, undead, command. Use your shared Companion Command on the chosen standard minion. If another undead you control is within 5 feet of it when commanded, it makes TWO copies of its normal damaging attack instead of one. Both attacks are part of the same single shared damaging command and cannot create additional commands, Actions or auto-raise events beyond the common once-per-round Auto-Raise limit."
}

### wizard.supplement.dual-cast

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Dual Cast",
  "activation": "Action",
  "cost": "Pay the complete RP costs of both spells",
  "rangeAndTarget": "As each spell",
  "duration": "As each spell",
  "frequency": "1/short rest",
  "effect": "Source progression line 5188. Choose two DIFFERENT prepared Wizard spells of rank 1 or 2, neither of which summons a creature or grants an additional Action. Cast both sequentially as one Action, paying both RP costs. They cannot both require concentration. Each matrix separately updates first-cast/Refrain history. Features that trigger merely from 'casting a spell' may trigger once for each actual matrix unless that feature itself says once per turn; no trigger may create another Dual Cast or additional full Action."
}

### wizard.supplement.arcane-feedback

data/public/class_playtests/wizard.json

Original broad lifecycle inventory

{
  "name": "Arcane Feedback",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Instantaneous",
  "frequency": "At most once per round",
  "effect": "Source progression line 5191, converted from historical slot wording to RP. After your Counterspell successfully negates a spell, restore 1 RP, never above your normal maximum. A counter produced by a companion, reflected spell or copied Counterspell does not trigger this feature."
}

### druid.engine[0]

data/public/class_playtests/druid.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "Wisdom governs spells, form attacks and class DC/M. Hit Die d8; book armor, weapons, saves and skills remain. Retain your own ability scores, HP, saves, proficiency and personality in all forms; form traits replace only the stated anatomy, movement and attacks. No additional monster stat block or separate beast HP pool. One natural attack per Attack Action unless a form explicitly states otherwise, attack PB+WIS, printed dice+WIS damage. Missing natural attack is 1d6 bludgeoning; default walking Speed 30 ft, normal AC, Medium size. Hawk is Tiny, Bear/Earth Warden/hero forms may be Large when space permits. Equipment melds and cannot be used while melded; magical numeric bonuses persist only if compatible with form anatomy and never duplicate armor."
}

### druid.engine[1]

data/public/class_playtests/druid.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "This class follows its explicit book progression instead of the ordinary 25-choice template. Base 1 grants Druidic, spellcasting, all five Base forms and 2 shifts/long rest. Choose one of seven Circles at 2; its level 2 features are a Base-stage exception. Enter the chosen Circle Arch path at 3, gain its 6 feature, then Circle Hero forms at 10 and its 14 feature. Arch Forms unlock 11 despite the historical word Arch; these are forms, not a second promotion. At 11 attune up to 2 Arch forms during long rest. Base forms remain available at higher levels. All features below are automatic at their gate for the chosen Circle; no generic extra class-card choices are added."
}

### mage.engine[10]

data/public/class_playtests/mage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "ELEMENTAL FAMILIAR. Conjure Elemental Familiar creates one familiar matching your current Focus; you may have only one elemental familiar. AC = 12 + PB; HP = 5 + Mage level + M; Speed 30 feet; Lightning familiar additionally has Fly 30 feet, Fire has resistance to fire, Cold has resistance to cold. It uses your saves and PB where required. Elemental Dart: ranged spell attack using your Mage spell attack, range 30 feet, hit S d4 damage of its element. It cannot generate RP, Dissonance, Focus casts, corpses, XP, loot or kill-trigger resources."
}

### mage.engine[12]

data/public/class_playtests/mage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "BONEFLAYER. Medium undead; AC 14; HP = 12 + 2 × Mage level; Speed 30 feet. Bone Shards: range 60 feet, your Mage spell attack, hit 2d6 + S necrotic. Fear Pulse: instead of Bone Shards, enemies of your choice within 10 feet make Wisdom saves against your Mage DC; failure causes Frightened until the end of their next turn; recharge 3 rounds. Grave Miasma: instead of Bone Shards, one 10-foot-radius point within 30 feet persists until the start of your next turn; enemies entering or starting there take 1d6 necrotic once; recharge 3 rounds."
}

### mage.engine[13]

data/public/class_playtests/mage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "DREADBLADE. Medium undead; AC 16; HP = 16 + 3 × Mage level; Speed 30 feet. Disrupting Blade: melee spell attack using your Mage attack bonus, reach 5 feet, hit 1d8 + S necrotic. If the target is concentrating it immediately makes its concentration save with disadvantage. On a natural 20, the target is Weakened until the end of its next turn, taking -1 to attack rolls. Dreadblade has advantage on saves against forced movement."
}

### mage.engine[14]

data/public/class_playtests/mage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "WRAITHBOUND. Medium undead; AC 14; HP = 10 + 2 × Mage level; Fly 40 feet and can hover. While it has not attacked or imposed control since the end of its previous turn, it is Invisible; attacking ends that state until the end of its next turn. Wraith Strike: melee spell attack using your Mage attack bonus, reach 5 feet, hit 1d8 + S necrotic. On a natural 20, the target makes a Constitution save against your Mage DC; failure Stuns it until the end of its next turn."
}

### mage.engine[16]

data/public/class_playtests/mage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "Before the irreversible Lich roll, the Director must explicitly tell the player the historical failure stakes: permanent loss of spellcasting, transformation into a cursed melee undead NPC, hostile faction consequences, cursed-gear restriction and no further XP as that retired PC. The player must explicitly opt into that retirement risk before rolling. If the player declines, the ritual stops before the roll and the character must choose another Hero path for this playtest; no irreversible consequence is applied."
}

### mage.hero.lich.undying-spellform

data/public/class_playtests/mage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "name": "Undying Spellform",
  "activation": "Triggered",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Until end of your next regular turn",
  "frequency": "1/long rest",
  "effect": "Undying Spellform. Tags: lich, undead, death. When damage reduces you to 0 HP without killing you outright, remain conscious and able to take Actions until the end of your next regular turn. You remain at 0 HP, cannot benefit from voluntary movement faster than half Speed, and still suffer ordinary consequences of further damage. If still at 0 HP when the effect ends, become unconscious and suffer one failed death save. Healing above 0 ends this feature early."
}

### mage.hero.lich.undead-immunities

data/public/class_playtests/mage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "name": "Undead Immunities",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Self",
  "duration": "Permanent after successful Lich transformation",
  "frequency": "Always",
  "effect": "Undead Immunities. Tags: lich, undead. You are immune to poison damage, the Poisoned condition, disease, Frightened, Charmed and magical sleep. You no longer need to breathe. You still require the normal rest schedule for mechanical recovery and can still be affected by abilities that specifically target undead unless another feature says otherwise."
}

### mirrorsage.engine[3]

data/public/class_playtests/mirrorsage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "Echo Release costs the Core V 2 RP cost of the recorded rank, minimum 2, consumes its record and counts as a spell for Dissonance and Refrain. Spell attack/DC use your own stats. First release of a newly captured record ignores Refrain addition only; base strain remains. Any preserved subsequent release uses ordinary repeated-spell strain. All released Echoes, pet replays, fusions and reflections share ONE release action per round; a specifically combined package counts once but pays for every component and has its printed damage cap. Copies cannot create resources or recursive Echoes."
}

### mirrorsage.hero.shattered-one.shatterbind

data/public/class_playtests/mirrorsage.json

Semantic companion supplement to original broad lifecycle inventory

{
  "name": "Shatterbind",
  "activation": "Passive",
  "cost": "0",
  "rangeAndTarget": "Record captured from undead/demon/aberration",
  "duration": "That release",
  "frequency": "Once/round",
  "effect": "You may change its damage type to necrotic or psychic on release. Category/eligibility/rank stay unchanged; high-INT undead and bosses remain excluded unless an encounter explicitly permits them."
}

### wizard.engine[19]

data/public/class_playtests/wizard.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "NECROMANCER STANDARD UNDEAD. Corpse Harvest and Auto-Raise share a maximum of three standard raised minions. Skeleton: AC 14, HP 6 + 2 × Wizard level, Speed 30; Bone Shot, range 30 feet, Wizard spell attack, 1d6+S necrotic. Zombie: AC 12, HP 10 + 3 × Wizard level, Speed 20; Slam, reach 5 feet, Wizard spell attack, 1d8+S necrotic. Goblin Thrall, available only from a goblinoid corpse: AC 13, HP 8 + 2 × Wizard level, Speed 30; Shiv, reach 5 feet, Wizard spell attack, 1d6+S necrotic. These are pre-Flesh-Ascendant statistics."
}

### wizard.engine[20]

data/public/class_playtests/wizard.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "NECROMANCER AUTO-RAISE. Once per round when one of your standard undead minions personally lands the killing blow on an eligible humanoid and your standard-minion count is below three, its corpse rises at the end of the current turn as the same mechanical minion type that scored the kill, if physically possible. A new minion cannot act during that same round. Auto-Raise costs no Action or RP but can never exceed the three-minion cap or generate a new resource, corpse chain, XP or treasure event. Without Infernal Pact only humanoids qualify."
}

### wizard.engine[22]

data/public/class_playtests/wizard.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "Dreadblade: AC 16, HP 16 + 3 × Wizard level, Speed 30. Disrupting Blade: reach 5 feet, Wizard spell attack, 1d8+S necrotic; a concentrating target immediately makes its concentration save with disadvantage. On a natural 20 the target is Weakened until the end of its next turn, taking -1 on attack rolls. Dreadblade has advantage on saves against forced movement."
}

### wizard.engine[23]

data/public/class_playtests/wizard.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "Wraithbound: AC 14, HP 10 + 2 × Wizard level, Fly 40 and hover. While it has not attacked or imposed control since the end of its previous turn it is Invisible; attacking ends that state until the end of its next turn. Wraith Strike: reach 5 feet, Wizard spell attack, 1d8+S necrotic. On natural 20 the target makes a Constitution save against your Wizard DC; failure Stuns until the end of its next turn."
}

### wizard.engine[25]

data/public/class_playtests/wizard.json

Semantic companion supplement to original broad lifecycle inventory

{
  "text": "DARK-TRAUMA INTERFACE. Necromancer features involving corpse desecration, infernal bargains, domination, body control or Mind Prison remain subject to the project's existing dark-content and trauma boundaries. A table may fade description to black without changing mechanics. No feature changes a player's real belief, permanently transfers ownership of a player character or silently retires a PC."
}

### wizard.hero.necromancer.infernal-pact-quest-based-unlock

data/public/class_playtests/wizard.json

Semantic companion supplement to original broad lifecycle inventory

{
  "name": "Infernal Pact (Quest-based unlock)",
  "activation": "Bonus Action",
  "cost": "3 RP",
  "rangeAndTarget": "One creature within 60 feet",
  "duration": "Maximum 3 rounds",
  "frequency": "1/long rest; quest-gated",
  "effect": "Infernal Pact — Gravebrand. Tags: hero, necromancer, infernal, necrotic, dark-content. This card can be selected only after completing the campaign's Infernal Pact quest and its dark-trauma check-in. Mark one creature. At the start of each of its turns it makes a Constitution save; on failure it takes 1d6 necrotic damage and you regain HP equal to the actual damage dealt, maximum S+M; success ends Gravebrand. Gravebrand ignores necrotic resistance but not immunity. While you possess this Pact, Corpse Harvest and Auto-Raise may also treat Fiend corpses as eligible; other creature types remain ineligible."
}

### Shared rule: Where a class card calls for a

Where a class card calls for a **standard companion** without a more specific profile, use: Small or Medium; AC 12+floor(PB/2); HP 2 L; walking Speed 30 ft; saves equal owner's PB; one melee or ranged attack (reach 5 ft/range 30 ft) at owner's class attack bonus, damage S d6 of the printed type. It has no independent class features, resources, loot, death triggers or extra turns. All companions belonging to one character share one Bonus Action command and **one damaging attack/action total per round** unless a specifically priced feature grants more. Without a command they move and Dodge. Act immediately after owner. A standard companion lasts 1 minute, disappears at 0 HP and cannot be healed for free by dismissing/resummoning. The creation cost must be paid again. Creature-specific stat blocks override this profile only where explicitly printed.

### Shared rule: One regular Action,

One regular Action, one Bonus Action if a feature permits it, normal movement and one Reaction between starts of your turns. A free trigger costs no Action only if expressly stated. All grants share **one extra full Action per creature per round**. An extra Action cannot grant another Action, recharge itself, or start another extra-Action grant. It supplies no extra Bonus Action or Reaction. A card granting additional attacks is not permission to repeat all class riders on every hit: obey each rider's frequency.

### Shared rule: No damage/healing copy

No damage/healing copy repeats the source's costs, procs, resource generation, critical bonus dice, buffs, actions, cooldown resets or duration. Compute fractions once, capped at 100% of one stored source unless an explicit card states a separately priced higher amount. Copies still cause ordinary damage consequences, concentration checks and death. A copy cannot copy another copy. A target/source record must refer to an actual resolved event, not merely a known ability name.

## Previously reviewed maximum-HP integration (not new source candidates)

**New Wizard-specific stacking exception:** Conjuration and Flesh Ascendant add when the same undead summon qualifies for both, overriding the frozen strongest same-stat class-technique bonus default for this pair only. Flesh Ascendant's engine[24] and named card describe one modifier identity; do not count both.

Conjuration's amount and caster provenance stay tied to creation. A later caster level or controller change does not recompute that snapshot. Flesh Ascendant instead follows the current eligible controller; changing control ends the old controller's eligibility and can create the new controller's eligible bonus, without healing.

**New Familiar Bond interpretation:** its ambiguous “gains hit points” wording supplies maximum capacity. Initial creation under that bonus can include it in starting HP; later level increases add capacity only. Familiar ownership/replacement and attack/command rules remain in the future companion package.

When a creature is initially created, construct its starting state from its final creation maximum unless its source expressly enters it damaged. Base20 plus Conjuration10 plus Flesh Ascendant20 gives50/50 at creation. Acquiring either bonus later does not fill missing HP. No bonus changes creature or command caps.

Evidence: GPT_MAXIMUM_HP_FINAL_CLOSURE.md. Preserve these creation-versus-later-capacity distinctions.
