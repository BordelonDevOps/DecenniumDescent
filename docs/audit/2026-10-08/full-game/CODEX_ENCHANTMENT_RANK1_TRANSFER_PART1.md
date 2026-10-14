PART 1 OF 4. Concatenate parts in numerical order after removing this first line; all four belong to one exact manuscript packet.
# Exact manuscript: twelve rank-one Enchantment spells

Candidate SHA256 212687265c7f5de5653ad10d728512f0bf234f1c7c3e18a8a2668224d851687c. All twelve cards below are exact authored values. Shared fields apply identically to each. Expand {HARD_GUARD} literally and append LIMITATIONS_SUFFIX literally to every limitations field. Lossless reconstruction checked locally against all candidate fields. Source conference already approved draftability, not these cards. Catalog remains210 reviewed/638 unfinished. Please approve manuscript promotion or identify exact repairs. Reply ideally under17,000chars.

Shared fields: {"rangeFeet": 30, "components": ["V", "S", "F"], "scaling": "None. No automatic increase in range, targets, duration, magnitude or uses.", "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable", "classAccessEvidence": {"Bard": {"rank": 1, "minimumClassLevel": 1, "school": "Enchantment", "baseRpCost": 2}, "Crimson Agent": {"rank": 1, "minimumClassLevel": 2, "school": "Enchantment", "baseRpCost": 2}, "Mirrorsage": {"rank": 1, "minimumClassLevel": 1, "school": "Enchantment", "baseRpCost": 2}, "Thief": {"rank": 1, "minimumClassLevel": 3, "school": "Enchantment", "baseRpCost": 2}, "Wizard": {"rank": 1, "minimumClassLevel": 1, "school": "Enchantment", "baseRpCost": 2}, "Paladin": {"rank": 1, "minimumClassLevel": 2, "school": "Enchantment", "baseRpCost": 2}}, "sourceReview": ["docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK1_SOURCE_CONFERENCE.md"], "reviewEvidence": []}

HARD_GUARD: Hard whole-Action/turn components use the existing combined source-character/target/encounter allowance across class features, spells and companions. A blocked hard component gains no invented fallback; independent printed components retain their own defense checks. A successfully established hard component claims the allowance once, not again each turn; ending, dispelling, replacing or suppressing it does not refund the encounter history. Actual boss/control immunities remain effective.

LIMITATIONS_SUFFIX: . Actual class access/repertoire, costs, components, Dissonance/Refrain, concentration transitions and cast/counter order follow SPELL_INTEGRATION_RULES.md. Pay a legal cast before effect resolution; failure/countering refunds nothing and restores no displaced concentration. V is audible, S requires the ordinary usable hand, and F is the normal class focus. Saves use the actual casting class's spell DC and binary save rules. Creature type alone supplies no mental immunity; Charmed-only immunity does not block effects that never impose Charmed. Actual broader defenses retain their written scope. No automatic scaling, generic upcast or free identification of hidden eligibility.

## Exact per-card fields

[
 {
  "id": "mesmerize",
  "activation": "Action",
  "targets": "One creature you perceive within 30 feet and line of effect.",
  "duration": "One target round, no concentration. Ends at the target's first future regular-turn END, excluding the entire current target turn if already underway. Outside initiative, the deadline is six elapsed seconds after application. Preserve the original virtual marker/absolute deadline through initiative changes, extra turns, absence and planar travel; end-phase effects precede cleanup.",
  "concentration": false,
  "resolution": "The target makes a Charisma save. Success: no new effect. Failure: apply Stunned and a separate unaware rider for the duration. The shared hard-control guard prevents the Stunned package if its allowance is unavailable; it does not itself prevent the separately printed unaware rider. Stunned immunity blocks Stunned, while immunity to an inherited component prevents that component under CONDITIONS_PLAYTEST.md rather than silently blocking every remaining part of Stunned.",
  "effect": "While unaware, the creature does not consciously register new ordinary sensory events. When an actual rule asks whether it currently perceives or is aware of a creature/event, treat it as unaware unless an exact sense/effect expressly supplies an exception. This rider neither deletes older memories nor invents sensory knowledge when it ends. Actual Stunned imposes its existing movement, saving-throw, incoming-attack and Incapacitated consequences; an actually applied Incapacitated component ends concentration normally.",
  "limitations": "Unaware adds no Unconscious, Prone, dropped items, adjacent automatic criticals, Blindness/Deafness condition or extra attack modifier of its own. The creature may act to the extent its actual remaining conditions permit, using retained knowledge and legal nonsensory choices. One unaware record per source caster/target; a later failed save refreshes that record without stacking penalties. A hard-denial history never refreshes with it. Independently valid sources/causes remain until each ends; ending Mesmerize restores neither concentration nor missed events. Hard whole-Action/turn components use the existing combined source-character/target/encounter allowance across class features, spells and companions. A blocked hard component gains no invented fallback; independent printed components retain their own defense checks. A successfully established hard component claims the allowance once, not again each turn; ending, dispelling, replacing or suppressing it does not refund the encounter history. Actual boss/control immunities remain effective",
  "designNotes": "PRESERVED: Action/30feet/V,S,F, CHA save, Stunned and unaware for1round. NEW: single perceived creature, operational unaware definition, exact future-end clock and independently scoped components. Exact-review completion distinguishes a guard-blocked Stunned package from narrower inherited-component immunity; unaware is not a second invented Action-denial condition.",
  "sourcePlacements": [
   {
    "name": "Mesmerize",
    "school": "Enchantment",
    "level": 1,
    "summary": "Target creature is stunned and unaware for 1 round (CHA save)."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 329,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Mesmerize",
     "effect": "Target creature is stunned and unaware for 1 round (CHA save).",
     "source_paragraph": 9389,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "1 round",
     "components": "V, S, F",
     "resolution": "Charisma save",
     "tags": [
      "Utility"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "pacify",
  "activation": "Action",
  "targets": "One creature you perceive within 30 feet and line of effect and presently treat as an enemy using ordinary information; this declaration reveals no hidden hostility.",
  "duration": "One target round, no concentration. Ends at the target's first future regular-turn END, excluding the entire current target turn if already underway. Outside initiative, the deadline is six elapsed seconds after application. Preserve the original virtual marker/absolute deadline through initiative changes, extra turns, absence and planar travel; end-phase effects precede cleanup.",
  "concentration": false,
  "resolution": "The target makes a Wisdom save. Success: no new restriction. Failure: it cannot voluntarily initiate an attack or begin/cast a spell whose selected mode includes a damage-dealing payload during the duration.",
  "effect": "The prohibition applies across Actions, Bonus Actions, Reactions and other actual attack/cast permissions. A spell with multiple modes can be cast through a genuinely nondamaging mode. Deliberately established delayed or ongoing damage from that selected cast counts; a miss, successful victim save, immunity or hoped-for zero damage does not turn a damage payload into a nondamaging mode. Existing attacks/spells whose commitments already occurred are not undone or stopped retroactively by this application. The creature retains movement, interactions, non-damaging spells/control and other legal choices.",
  "limitations": "This is not a blanket ban on every harmful nonattack technique and does not forbid harm merely because it is harmful: use the printed attack/damaging-spell categories. Truly involuntary acts retain their separate rules. No harm-ending clause is added; being attacked does not remove Pacify. This limited prohibition does not consume the whole-Action hard-control allowance merely because the creature lacks attractive alternatives. One Pacify restriction per caster/target; later failed save refreshes it, successful save does not remove it; independent other-caster records keep their own deadlines",
  "designNotes": "PRESERVED: Action/30feet/V,S,F, enemy cannot attack or cast damaging spells for1round. NEW: WIS save, ordinary enemy designation and voluntary initiation/selected-damage-mode scope. Damage capability is determined from the selected effect, not a future hit or HP-loss prediction.",
  "sourcePlacements": [
   {
    "name": "Pacify",
    "school": "Enchantment",
    "level": 1,
    "summary": "Enemy cannot attack or cast damaging spells for 1 round."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 330,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Pacify",
     "effect": "Enemy cannot attack or cast damaging spells for 1 round.",
     "source_paragraph": 9390,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "1 round",
     "components": "V, S, F",
     "resolution": "Automatic or opposed as described",
     "tags": [
      "Utility"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "sleep",
  "activation": "Action",
  "targets": "Declare an ordered list of distinct creatures you perceive within 30 feet and line of effect before hidden HP or defense resolution. A creature appears at most once in this cast’s list.",
  "duration": "Independent Sleep-caused Unconscious on each affected creature, up to1minute, no concentration. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": false,
  "resolution": "No saving throw. After casting commits and survives interruption, start one fixed budget of24. In declared order, each creature costs max(1, its current ordinary HP) at this resolution; temporary HP are ignored. If that cost exceeds the remaining budget, stop without attempting that creature or later entries. Otherwise deduct that cost before testing defenses/guard and attempt the Unconscious application. An attempted immune, protected or hard-guard-blocked creature still spends its HP cost. Budget/allocation/hidden defenses receive no special diagnostic disclosure; ordinary visible results remain observable.",
  "effect": "A successful application imposes the actual Unconscious condition, including its inherited Incapacitated, awareness, movement, speech, held-item, Prone, save and attack consequences subject to actual component immunities. Each target uses its own shared source-character/target hard-control history. A0HP creature costs1 and retains its separate0HP state and Unconscious source. End a Sleep application when its target receives a positive damage packet after defenses and before temporary HP, when another creature within physical reach spends an Action rousing it, on its deadline, or through an applicable removal rule. Physical rousing by that Action ends all applications of this ordinary Sleep spell on that creature, but does not cure unrelated Unconscious causes. All Sleep applications independently see a qualifying damage event. The waking damage attack resolves using the conditions present for its roll/hit, then the damage event ends Sleep; no retroactive critical/hit reversal.",
  "limitations": "A fully prevented zero packet does not wake by damage; positive packet can wake even if an HP floor prevents actual numeric HP loss. No self-awakening while Unconscious, automatic stabilization, healing, death-save reset or removal of other causes. No rolled HP budget, creature-type sleep immunity or concentration is imported. Recasts pay again and cannot refresh the shared guard; an unsuccessful new application leaves old valid sources intact. Suppression clocks continue and never replay the original drop/Prone event when suppression ends. Hard whole-Action/turn components use the existing combined source-character/target/encounter allowance across class features, spells and companions. A blocked hard component gains no invented fallback; independent printed components retain their own defense checks. A successfully established hard component claims the allowance once, not again each turn; ending, dispelling, replacing or suppressing it does not refund the encounter history. Actual boss/control immunities remain effective",
  "designNotes": "PRESERVED: Action/30feet/V,S,F, fixed24HP and explicitly no save. NEW: ordered current-HP/minimum1 budgeting, finite minute, waking and helper Action. Exact completion: helper rousing ends this named spell’s Sleep applications, not every cause of Unconscious; damage timing preserves an already determined hit/critical.",
  "sourcePlacements": [
   {
    "name": "Sleep",
    "school": "Enchantment",
    "level": 1,
    "summary": "Up to 24 HP worth of creatures fall unconscious (no save)."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 331,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Sleep",
     "effect": "Up to 24 HP worth of creatures fall unconscious (no save).",
     "source_paragraph": 9391,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Automatic or opposed as described",
     "tags": [
      "Control"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
