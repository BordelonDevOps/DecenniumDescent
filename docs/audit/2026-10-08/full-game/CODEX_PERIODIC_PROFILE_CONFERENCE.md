The explicit fire-family arbitration and healing/cure separation are adopted. Next binding pass recovered additional exact sources below. Please resolve these proposed NEW integration bridges; challenge any source conflict.

1. Missing cure metadata: each registered ordinary hostile Bleed without its own cure text explicitly adopts Core WIS Medicine Action (self/adjacent helper) against applying class DC, fallback10 only if no DC, and legal positive-potential magical healing ends it. This is a declared NEW overlay, not automatic mechanics inherited from a family tag. Crimson and Dragoon retain printed kit Actions as additional endpoints; NEW consume one kit use. Crimson kit Action ends all that owner's Crimson instances; Dragoon kit Action ends that Dragoon record. Shaman Blood Curse retains Medicine class DC and healing-triggered CON save. Explicit end-one/end-all removal works as written. No current class Bleed is artifact-level or special-cure-only merely because magical. Confirm counts for generic Medicine/healing when multiple independent Bleed records coexist: propose Medicine one selected record, positive-potential magical healing all ordinary applicable Bleeds; each Blood Curse gets its own CON save. 

2. Missing extinguish metadata: explicitly registered attached Burn-style fire adopts ordinary self/adjacent-helper Action extinguish or full immersion; Core end-turn DEX save applies at its source DC, after any end-turn tick, even for start-turn tick profiles. Printed no-mundane-extinguishing exceptions override only mundane endpoints. This is NEW and must not generate extra generic damage. Is that appropriate for unnamed magical attached fires as well? Exact list: Cleric Flame Invocation and Divine Invocation Flame; Mage Elemental Bolt Fire, Fusion Fire+Cold, Cascade first fire hit; Wizard Combo Surge Fire+Cold. Propose classify all these as attached ongoing-fire with own profiles. Mage Bolt uses Focus passive profile/stack group? Propose own application identity in same Mage Fire stack group (shared marker cannot add anyway); Fusion/Cascade keep own groups because not Focus cards. Elemental Mastery Arch +one tick only affects Focus passive/Inferno and explicit Focus-Burn reference, not every fire spell rider. 

3. Thief Ashblood is an internal poison recipe that deals 1 fire at start next2turns, but never says Burn or ignition. Propose its own periodic-poison rider, NOT ongoing-fire family, no extinguish action; poison-removal metadata requires discussion. Poison immunity should block a failed-CON poison recipe application, but it is not automatically the Core Poisoned condition. Separately Paladin Purifying Crown's selected hostile periodic fire+radiant is divine damaging aura/mark, not attached Burn; exclude from family unless its actual source says otherwise.

4. Vein Cutter contradicts itself: effect says Bleed next2turns, duration says until end nextturn. Propose preserve two Bleed ticks (NEW end target next2regularturns fallback); Speed-10 and -1 next attack damage end nextturn/consumption separately. Two-turn Bleed remains poison-fueled but consumes poison without normal recipe effect, so not one of the two recipe-instance slots. Prolonged Suffering applies once to owned base2-turn Bleeds including another legal class because no class restriction; makes4ticks, no addition with other extensions; Persistent Bleed refreshes permitted duration, preserving remaining caps/engine-specific maximum and not duplicating instances. Need deterministic precedence if Crimson3ticks with Persistent says2, or Arterial5 with Prolonged4: propose never shorten current remaining duration; max(currentRemaining, refreshDuration) bounded by true hard cap, with extensions nonadditive. Explicitly reject re-extending an expiring record without a new qualifying source trigger.

5. Bloodroot Bleed lacks type: agreed physical-hit-or-slashing fallback implies slashing even though initial zone damage is necrotic. Confirm preserve fallback instead of guessing necrotic. Tyrant Impale says Bleeding while engine says Bleed: same Dragoon engine profile, independent from ending pin. All periodic clocks use regular target turns only and exact start/end markers; extra turns do not accelerate. Outside initiative consume once every6seconds on preserved clock.

Please return dispositions and exact minimal corrections. The original cards remain unchanged; these are provisional integration overlays.

EXACT ACTIVE SOURCE OBJECTS
[
  {
    "id": "cleric.base.flame.flame",
    "name": "Flame",
    "className": "Cleric",
    "band": "Base",
    "path": "Flame",
    "sourceKind": "supplement",
    "minimumClassLevel": 2,
    "acquisition": "automatic",
    "activation": "Triggered",
    "cost": "1 Conviction",
    "rangeAndTarget": "One creature damaged by your Smite or Rite",
    "duration": "2 rounds",
    "frequency": "At most once on each of your turns",
    "effect": "Invocation Path — Flame. Tags: invocation, flame. Immediately after your Smite or Rite damages a creature, you may spend 1 Conviction. The target ignites and takes 1d6 fire damage at the start of each of its next 2 turns. Reapplying Flame refreshes the duration; the burning damage does not stack.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 1977,
      "originalText": "Flame: Conviction can be consumed to ignite targets for 2 turns (fire DoT)."
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "id": "cleric.arch.divine-invocation",
    "name": "Divine Invocation",
    "className": "Cleric",
    "band": "Arch",
    "path": null,
    "sourceKind": "active",
    "minimumClassLevel": 3,
    "acquisition": "selection",
    "activation": "Action",
    "cost": "2 Conviction + 3 RP",
    "rangeAndTarget": "Mode-dependent; maximum 60 feet",
    "duration": "Instantaneous unless mode states otherwise",
    "frequency": "Recharge 3 rounds",
    "effect": "Divine Invocation. Tags: invocation, bishop. Use only your selected Invocation Path. Radiance: up to 3 allies within 30 feet each regain S d8+M HP; one may end Frightened or Poisoned. Judgment: one enemy within 60 feet makes a Wisdom save, taking (S+1)d8 radiant on failure or half on success; failure also applies Judged for 2 rounds. Renewal: up to 2 allies within 30 feet each regain S d8+M HP and 5 Stamina. Flame: creatures in a 15-foot cone make Dexterity saves, taking (S+1)d8 fire on failure or half on success; failed targets also take 1d6 fire at the start of their next turn. Veil: up to 3 allies within 30 feet can see invisible/ethereal creatures within 30 feet and gain advantage on saves against illusions for 3 rounds. Echoes: choose one eligible Smite or Rite you resolved this turn or previous regular turn and one original target within 30 feet; repeat 50% of its immediate unmodified rolled damage or healing dice, rounded down once, minimum 1 for a positive source, with no copied conditions, resources or triggers.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 2001,
      "originalText": "Divine Invocation: Channel a powerful prayer based on your chosen Invocation Path, with effects ranging from mass healing to divine fire or protective barriers."
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "id": "dragoon.hero.dragon-tyrant.tyrant-s-impale",
    "name": "Tyrant's Impale",
    "className": "Dragoon",
    "band": "Hero",
    "path": "Dragon Tyrant",
    "sourceKind": "active",
    "minimumClassLevel": 10,
    "acquisition": "selection",
    "activation": "Action",
    "cost": "2 Momentum",
    "rangeAndTarget": "One enemy in polearm reach",
    "duration": "Instant; pin until end next turn",
    "frequency": "Recharge 3",
    "effect": "Weapon attack; hit adds S d6 piercing. A hit creature no more than one size larger makes STR save or is Restrained and Bleeding. It may use Action STR(Athletics) or DEX(Acrobatics) versus class DC to end restraint. You must stay in reach to maintain pin.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 2357,
      "originalText": "Tyrant's Impale: A devastating attack that can pin weaker enemies to the ground, preventing movement and causing bleeding damage."
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "id": "mage.base.elemental-bolt",
    "name": "Elemental Bolt",
    "className": "Mage",
    "band": "Base",
    "path": null,
    "sourceKind": "active",
    "minimumClassLevel": 2,
    "acquisition": "selection",
    "activation": "Action",
    "cost": "1 RP",
    "rangeAndTarget": "One creature within 60 feet",
    "duration": "Instantaneous",
    "frequency": "At will while RP remains",
    "effect": "Elemental Bolt. Tags: mage-spell, elemental, focus, damage. Make a Mage spell attack. On a hit deal S d8 + M damage of your current Focus. Fire: target takes 1d4 fire at the start of its next turn. Cold: Speed -10 feet until the end of its next turn. Lightning: one different enemy within 10 feet takes S lightning damage. Secondary damage creates no new spell cast or chain credit.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 2898,
      "originalText": "Elemental Bolt: Cast a bolt of your chosen element (once selected) that deals additional effects based on the element."
    },
    "designStatus": "provisional-playtest",
    "spellRank": 1
  },
  {
    "id": "mage.arch.elemental-mastery",
    "name": "Elemental Mastery",
    "className": "Mage",
    "band": "Arch",
    "path": null,
    "sourceKind": "passive",
    "minimumClassLevel": 7,
    "acquisition": "selection",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Your current Elemental Focus spells",
    "duration": "Permanent",
    "frequency": "Always",
    "effect": "Elemental Mastery. Tags: arcanist, focus. Improve the secondary effect of your current Focus. Fire Burns from your Focus cards last one additional turn but never stack. Cold Focus Speed reductions increase by another 5 feet, minimum 0. Lightning Focus's once-per-turn secondary arc increases from S flat lightning damage to S d4 lightning damage. Pivoted Focus uses the corresponding upgraded rider.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 2916,
      "originalText": "Elemental Mastery: Increase the effectiveness of your chosen element's secondary effects."
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "id": "mage.hero.elementalist.elemental-fusion",
    "name": "Elemental Fusion",
    "className": "Mage",
    "band": "Hero",
    "path": "Elementalist",
    "sourceKind": "active",
    "minimumClassLevel": 10,
    "acquisition": "selection",
    "activation": "Action",
    "cost": "4 RP",
    "rangeAndTarget": "One creature within 60 feet",
    "duration": "Instantaneous",
    "frequency": "Recharge 2 rounds",
    "effect": "Elemental Fusion. Tags: mage-spell, elementalist, elemental, damage. Choose your current Focus and one other element among Fire, Cold and Lightning. Make a Mage spell attack. On hit deal S d8 of each chosen element. Pair rider: Fire+Cold reduces Speed by 10 feet and applies 1d4 fire at start of target's next turn; Fire+Lightning removes Reaction until start of target's next turn; Cold+Lightning reduces Speed by 10 feet and prevents opportunity attacks until end of target's next turn. For Nuke Chain purposes this spell counts only as your current Focus element.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 2955,
      "originalText": "Elemental Fusion: Combine two elements to create a hybrid spell with unique effects."
    },
    "designStatus": "provisional-playtest",
    "spellRank": 5
  },
  {
    "id": "mage.hero.elementalist.cascade-storm",
    "name": "Cascade Storm",
    "className": "Mage",
    "band": "Hero",
    "path": "Elementalist",
    "sourceKind": "active",
    "minimumClassLevel": 12,
    "acquisition": "selection",
    "activation": "Action",
    "cost": "6 RP",
    "rangeAndTarget": "Up to three different creatures within 60 feet",
    "duration": "Instantaneous",
    "frequency": "Recharge 3 rounds",
    "effect": "Cascade Storm. Tags: mage-spell, elementalist, fire, cold, lightning, damage. Choose up to three creatures. Resolve one separate Mage spell attack against each: first hit deals S d6 fire and 1d4 fire next turn; second hit deals S d6 cold and Speed -10 feet until end next turn; third hit deals S d6 lightning and removes Reaction until start next turn. If fewer than three targets are chosen, unused elements are lost. For Nuke Chain purposes choose one of the three elements before casting; Cascade Storm counts only as that element.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 2956,
      "originalText": "Cascade Storm: Trigger a sequence of elemental effects that build upon each other."
    },
    "designStatus": "provisional-playtest",
    "spellRank": 6
  },
  {
    "id": "paladin.supplement.oath-of-flame.purifying-crown",
    "name": "Purifying Crown",
    "className": "Paladin",
    "band": "Hero",
    "path": "Oath of Flame",
    "sourceKind": "finalOathGift",
    "minimumClassLevel": 20,
    "acquisition": "automatic for chosen Oath",
    "activation": "Bonus Action",
    "cost": "0 RP",
    "rangeAndTarget": "Up to 3 chosen creatures in your Oath aura",
    "duration": "3 rounds",
    "frequency": "1/long rest",
    "effect": "For 3 rounds, a selected allied creature is immune to Poisoned and ordinary disease. A selected hostile undead or fiend takes S d6 fire plus S d6 radiant damage at the start of its turn, at most once per round. When the Crown activates, restore one expended use of Holy Inferno, even if it was used since the last short rest. This restoration occurs once and cannot recurse.",
    "prerequisite": "Paladin 20; Oath of Flame",
    "source": {
      "line": null,
      "reference": "SACRED_OATHS[3].finalOathGift",
      "originalText": "",
      "status": "source-derived",
      "originalObjects": [
        {
          "reference": "SACRED_OATHS[3].finalOathGift",
          "value": "Purifying Crown — once per day, manifest sanctified fire for 3 rounds: undead and fiends in your aura take radiant+fire damage each turn, allies gain immunity to disease and poison, and Holy Inferno immediately recharges once."
        }
      ]
    },
    "designStatus": "provisional-playtest",
    "spellRank": null,
    "oathId": "flame",
    "oathName": "Oath of Flame",
    "oathbreakerName": "Inferno",
    "displayPath": "Oath of Flame"
  },
  {
    "id": "shaman.hero.bloodcaller.bloodroot-trail",
    "name": "Bloodroot Trail",
    "className": "Shaman",
    "band": "Hero",
    "path": "Bloodcaller",
    "sourceKind": "active",
    "minimumClassLevel": 16,
    "acquisition": "selection",
    "activation": "Bonus Action",
    "cost": "6 RP; 1 long-rest use",
    "rangeAndTarget": "Up to 30 ft of ground traversed this turn, 5 ft wide",
    "duration": "Concentration, 3 of your turns",
    "frequency": "1/long rest",
    "effect": "Leave a visible bloodroot trail, no solid wall. Each enemy first entering/starting on it per round makes DEX save for S d6 necrotic, half on success; failure Bleed 1d4 next turn. Maximum 3 creatures damaged/round chosen in entry order; no persistent corruption after expiry.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 4092,
      "originalText": "Bloodroot Trail: Ultimate ability that leaves a cursed line wherever you move; enemies crossing it take damage and start bleeding."
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "id": "thief.hero.shadowblade.persistent-bleed",
    "name": "Persistent Bleed",
    "className": "Thief",
    "band": "Hero",
    "path": "Shadowblade",
    "sourceKind": "passive",
    "minimumClassLevel": 10,
    "acquisition": "selection",
    "activation": "Triggered",
    "cost": "0",
    "rangeAndTarget": "One enemy hit by your weapon",
    "duration": "Bleed extension",
    "frequency": "Once/own turn",
    "effect": "Refresh one of your existing Bleed effects to 2 target turns. Cannot increase its dice, duplicate instances or extend a capped poison effect beyond its poison rules.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 4426,
      "originalText": "Persistent Bleed: Bleeds you cause refresh on hit instead of expiring."
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "id": "thief.hero.shadowblade.vein-cutter",
    "name": "Vein Cutter",
    "className": "Thief",
    "band": "Hero",
    "path": "Shadowblade",
    "sourceKind": "active",
    "minimumClassLevel": 12,
    "acquisition": "selection",
    "activation": "Triggered",
    "cost": "One dose",
    "rangeAndTarget": "Enemy critically hit by your weapon",
    "duration": "Until end next target turn",
    "frequency": "Once/round",
    "effect": "Consume prepared poison without its normal recipe effect; target CON save or Bleed 1d4 next 2 turns, Speed-10 ft and-1 next attack damage. Reapplication refreshes; source stack 3 replaced by one bounded package.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 4432,
      "originalText": "Vein Cutter: On critical hit, apply Bleed, Slow, and Weakened effects that can stack up to 3 times."
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "id": "thief.hero.blackguard.prolonged-suffering",
    "name": "Prolonged Suffering",
    "className": "Thief",
    "band": "Hero",
    "path": "Blackguard",
    "sourceKind": "passive",
    "minimumClassLevel": 10,
    "acquisition": "selection",
    "activation": "Passive",
    "cost": "0",
    "rangeAndTarget": "Your Bleed application",
    "duration": "Up to 4 target turns",
    "frequency": "Continuous",
    "effect": "When you apply Bleed with base 2-turn duration it lasts 4 turns instead. Never doubles dice or stacks with another extension; subsequent refresh sets to 4, not adds 4.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 4441,
      "originalText": "Prolonged Suffering: Bleeds you cause last twice as long."
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "id": "wizard.hero.elementalist.combo-surge",
    "name": "Combo Surge",
    "className": "Wizard",
    "band": "Hero",
    "path": "Elementalist",
    "sourceKind": "active",
    "minimumClassLevel": 10,
    "acquisition": "selection",
    "activation": "Triggered",
    "cost": "2 RP",
    "rangeAndTarget": "One target damaged by the second qualifying spell",
    "duration": "Until end of target's next turn plus listed damage",
    "frequency": "At most once per round",
    "effect": "Combo Surge. Tags: hero, elementalist, elemental, combo. When you damage the same creature on consecutive regular turns with the required pair in either order, you may trigger one combo. Fire + Cold: the target takes 1d6 fire at the start of its next turn and makes a Strength save; failure Restrains it until the end of that turn. Lightning + Earth: the target is knocked Prone and makes a Constitution save; failure Stuns it until the end of its next turn, subject to one successful Combo-Surge Stun per target per encounter. Other element pairs have no Combo Surge in this pilot.",
    "source": {
      "extract": "docs/reference/Player_Rulebook_v6_source_text.txt",
      "line": 5277,
      "originalText": "Combo Surge: Casting two different elements in sequence triggers a combo effect"
    },
    "designStatus": "provisional-playtest",
    "spellRank": null
  },
  {
    "class": "thief",
    "engineIndex": 2,
    "text": "At 1 know all four Tier I recipes, at 7 add Tier II, at 14 Tier III. Poison saving throws use Thief DC except preserved source fixed DC 12 becomes max(12, Thief DC) for Mindburn/Venombite. Unless stated damage/conditions require a failed CON save; initial weapon damage is unaffected. Critical riders also need this failed save. One ongoing instance of each recipe per target; another application refreshes rather than stacks. Maximum 2 simultaneous different poison recipes from you per target. Bleed never stops all healing by default, Poisoned uses the Core V 2 condition: disadvantage on attacks and ability checks (not saving throws), and Shaken means disadvantage on next fear save. Neither is a hidden full-turn disable."
  },
  {
    "class": "thief",
    "engineIndex": 3,
    "text": "Tier I: Bloodleech gives Bleed 1d4 at start next 2 target turns; critical restores 1d4 of your HP, once per dose. Crippler gives-1 on next attack before end next turn; critical also half Speed for that duration. Mindburn uses WIS save: -1 spell-attack rolls until end next turn, critical also no Reactions. Venombite gives Poisoned until end next turn; critical also-1 on next save. Tier II: Ashblood adds 2d6 poison now and 1 fire at start next 2 turns; critical prevents HP recovery through end next turn. Silencer prevents verbal spellcasting through end next turn, critical also drops one held nonbonded item into its space; it can retrieve normally. Shiver gives Shaken through end next turn; critical also no Reactions. Hexroot gives-1 saves for 2 target turns; critical lets next weapon hit ignore resistance, never immunity, before end next turn."
  },
  {
    "class": "crimson-agent",
    "engineIndex": 2,
    "text": "Your Bleed is a physical ongoing effect on a living, non-bloodless creature: 1d4 damage at the start of each of its next 3 turns, then ends. It is not a new attack and generates no BG or procs. Refresh duration instead of stacking; Blood Echo expressly allows two independent instances, maximum. An Action by the victim or an adjacent creature using a healer's kit ends all your Bleeds on that victim. Apply physical resistance/immunity normally. Track remaining ticks and creator per instance. Allied healing versions from Bloodweaver cost RP and never count as hostile Bleeds for detonation, spreading or generation."
  },
  {
    "class": "dragoon",
    "engineIndex": 4,
    "text": "Spending Momentum pays before resolution; a hit refund cannot pay its own activation. Burn means 1d4 fire at start of target's next 2 turns, nonstacking. Bleed means 1d4 physical at start of next 2 turns; an Action with a healer's kit ends it. Do Ts give no Momentum or critical triggers. Hard denial uses the shared once-per-target/encounter guard."
  },
  {
    "class": "ranger",
    "engineIndex": 1,
    "text": "Weapon Synergy tracks last successful direct weapon hit on your own turns. Changing melee→ranged grants+1 to that ranged attack roll if it is your first attack of the turn; changing ranged→melee makes the hit apply Bleed 1d4 on target's next 2 turns. Once/turn synergy; Do Ts, copies, companions, forced attacks and misses do not advance it. At 5 ordinary Attack Action makes two attacks; techniques use only printed counts. You may draw/stow one weapon as normal object interaction; Dual Style later improves this."
  },
  {
    "class": "shaman",
    "engineIndex": 4,
    "text": "Flask tier uses S. Mundane Base modes: Burn=one enemy 30 ft DEX save S d6 fire half, failure 1d4 fire next turn; Root=one ground enemy 30 ft STR save Speed 0 until end its next turn; Weaken=one enemy 30 ft CON save or-1 attack damage until end its next turn. Advanced Hero modes additionally: Stun=one enemy 30 ft CON save or no Reactions, failure by 10 Stunned until end its next turn; Heal=one living ally 30 ft S d6+M HP; Restore=end Frightened or Poisoned on one ally 30 ft. Every thrown flask consumes one prepared unit and 2 RP for advanced magic (Base mundane flasks cost 0 RP). Changing payload requires no separate crafting action when throwing. No flask leaves harvestable poison or another flask."
  }
]