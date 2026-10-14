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
 {
  "id": "confusing-flash",
  "activation": "Action",
  "targets": "One creature you perceive within 30 feet and line of effect.",
  "duration": "Pending until the target’s next regular turn; a single commanded behavior during that turn, then ends. Exclude any current in-progress target turn. Extra turns do not execute it. If no initiative exists when a compelled combat act matters, establish ordinary initiative; if no action sequence is needed, resolve the same one ordinary action/movement opportunity within six elapsed seconds. No indefinite pending command.",
  "concentration": false,
  "resolution": "The target makes a Wisdom save. Success: no command. On failure, roll a neutral1d2 immediately:1=Attack,2=Flee. Determine the branch before any caster/controller choice. Attack reserves/spends the shared hard-control allowance when its future command is established; if blocked, apply no Attack command and no substitute Flee. Flee is movement compulsion, not a whole-Action denial.",
  "effect": "At the next regular turn after required start-phase events and before voluntary actions/movement, resolve the branch. Attack: if the creature can take its ordinary Action, neutrally select with equal probability among other creatures it can presently perceive and legally attack with at least one available ordinary weapon, natural or unarmed attack. The target/controller chooses one legal ordinary attack method against that victim and spends its normal Action on exactly that one attack; no Multiattack, extra attack, spell, charged technique or optional resource expenditure is compelled. Normal finite ammunition for its chosen attack is still required and spent. If no legal victim/method or no ordinary Action is available, no attack occurs and the command ends; it never turns an unavailable Action into an available one. Flee: spend as much of its ordinary available movement as reasonably possible increasing distance from the caster along a legal route it knows is not immediately self-destructive; the target/controller chooses the route. No automatic Dash; other Actions, BA and Reactions remain available. A blocked route allows only the actual safe meaningful movement possible. Compelled use of its movement can provoke ordinary opportunity attacks; it is not a push/pull displacement.",
  "limitations": "No deliberately self-directed attack, known lethal route, remote victim discovery or caster-selected random victim. Mandatory movement/attack occurs once, not on every extra turn or repeated save. One pending Confusing Flash per target across casters; a later successfully established branch replaces the prior pending behavior, but no spent hard-control history is refunded. A saved-against or guard-blocked new branch creates no replacement. A legal attack remains genuinely compelled and is not made voluntary merely by another Charmed relation; actual absolute prohibitions still govern. Other independent compulsion rules retain scope and cannot supply extra action budgets. Hard whole-Action/turn components use the existing combined source-character/target/encounter allowance across class features, spells and companions. A blocked hard component gains no invented fallback; independent printed components retain their own defense checks. A successfully established hard component claims the allowance once, not again each turn; ending, dispelling, replacing or suppressing it does not refund the encounter history. Actual boss/control immunities remain effective",
  "designNotes": "PRESERVED: Action/30feet/V,S,F, WIS and random attack-or-flee result. NEW: neutral branch/victim procedure, future-turn scheduling and attack hard-control reservation. Exact completions specify first voluntary opportunity, one ordinary attack, ammunition, failed-execution expiry and nonbanking replacement; runtime scheduling remains unimplemented.",
  "sourcePlacements": [
   {
    "name": "Confusing Flash",
    "school": "Enchantment",
    "level": 1,
    "summary": "Target makes WIS save or randomly attacks or flees."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 332,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Confusing Flash",
     "effect": "Target makes WIS save or randomly attacks or flees.",
     "source_paragraph": 9392,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Wisdom save",
     "tags": [
      "Utility"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "distract",
  "activation": "Reaction — when a perceived enemy begins an Action in numbered initiative, after commitment but before its first main outcome",
  "targets": "One creature you perceive and ordinarily identify as an enemy within30feet and line of effect, with a qualifying Action currently beginning in established numbered initiative.",
  "duration": "Triggering-Action interruption is immediate; opportunity-attack restriction ends at the END of the current numbered round, even if little of that round remains. No extension to the target’s next turn, added round or out-of-initiative window.",
  "concentration": false,
  "resolution": "After the triggering Action’s actual commitments/beginning hooks but before its first main outcome, cast this Reaction. Only an Action qualifies, including a separately authorized extra Action; not a Bonus Action, Reaction, individual later attack within an already-resolving Attack Action or held-spell release that is merely a Reaction. The creature makes an Intelligence save. Success: neither new component. Failure: cancel the still-pending whole Action if the shared hard-control allowance and actual defenses permit, and independently prevent its opportunity attacks through the numbered-round endpoint.",
  "effect": "For Attack, interrupt before any attack outcome and cancel that whole pending Action. For a spell Action, normal costs, components, concentration transition, Dissonance/Refrain and beginning hooks are already committed; they remain. Distract is itself a counterable spell; nested interruption uses normal last-in/first-out order, resuming surviving parents once without repaying or replaying hooks. One creature may attempt ordinary/same-named Distract at most once against one pending Action unless an exact source grants another attempt; claim that attempt at legal Distract cast commitment, including if this cast is later countered. Another Reaction alone supplies no extra attempt. If the parent Action is no longer pending when this legal Distract resolves, it cancels nothing and claims no hard-denial allowance for a nonexistent cancellation; its failed-save opportunity-attack rider can still apply.",
  "limitations": "Completed outcomes, beginning-hook consequences and costs cannot be undone. A blocked hard cancellation still permits the independent failed-save OA restriction unless a defense actually blocks that rider. No general Reaction loss, cancellation of every action on a turn, or free target/rank identification. Ordinary Counterspell remains a different source and its ordinary spell-negation does not spend the hard-denial allowance. An unused or already-canceled Action supplies no new trigger; there is no qualifying Distract trigger outside established numbered initiative. Hard whole-Action/turn components use the existing combined source-character/target/encounter allowance across class features, spells and companions. A blocked hard component gains no invented fallback; independent printed components retain their own defense checks. A successfully established hard component claims the allowance once, not again each turn; ending, dispelling, replacing or suppressing it does not refund the encounter history. Actual boss/control immunities remain effective",
  "designNotes": "PRESERVED: Reaction/30feet/V,S,F, interrupt enemy action and no opportunity attacks this round. NEW: INT save, precisely pending full-Action scope, guard and numbered-round endpoint. Exact completions bind attempt commitment, nested interruptions and a formerly valid but subsequently canceled parent without refunds.",
  "sourcePlacements": [
   {
    "name": "Distract",
    "school": "Enchantment",
    "level": 1,
    "summary": "Interrupt enemy action (no opportunity attacks this round)."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 334,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Distract",
     "effect": "Interrupt enemy action (no opportunity attacks this round).",
     "source_paragraph": 9394,
     "casting_time": "1 reaction",
     "range": "30 feet",
     "duration": "Instantaneous",
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
  "id": "voice-of-peace",
  "activation": "Action",
  "targets": "One creature you perceive within30feet and line of effect and ordinarily treat as an enemy. Use an audible language you can speak; its actual hearing/understanding is checked at paid resolution without a diagnostic.",
  "duration": "Up to1minute, no concentration. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": false,
  "resolution": "If the chosen creature cannot hear and understand your words at resolution, no ceasefire applies. Otherwise it makes a Wisdom save. Success: none. Failure: establish a ceasefire toward you and the creatures it then actually recognizes as your participating allies; record those participants at application.",
  "effect": "The target cannot voluntarily initiate an attack or knowingly harmful effect against those recorded participants. It can act, move, speak, decline negotiation, defend through nonharmful choices and act against nonparticipants normally. End the ceasefire immediately if you or a recorded participating ally commits an attack or knowingly harmful effect against the target or someone the target actually recognizes at that event as its ally. Commitment breaks it even on a later miss/prevented effect. Mere insult, argument, approach, suspicion or unsupported threat does not count. Already committed outcomes are not reversed. Participants are fixed for this application: later allies are not silently enrolled; a new paid successful cast can establish a new set.",
  "limitations": "Initial hearing, shared language, range and line of effect are not ongoing tethers. No forced treaty, agreement, Diplomacy success, permanent alliance, faction standing or Charmed condition. Recognized relationships use actual established knowledge, not a hidden membership/allegiance scan. One ceasefire per caster/target; new failed save replaces that caster’s old application/participant set/deadline, successful save or ineligible application leaves a valid old one intact. Other-caster ceasefires retain separate participants and endpoints. This limited harm restriction is not whole-Action denial",
  "designNotes": "PRESERVED: Action/30feet/V,S,F, one enemy’s ceasefire unless provoked. NEW: WIS, minute, initial hearing/language and participant/provocation scope. Exact completion snapshots the protected participating group while checking actual recognition of the target’s allies at a provoking event.",
  "sourcePlacements": [
   {
    "name": "Voice of Peace",
    "school": "Enchantment",
    "level": 1,
    "summary": "Negotiate ceasefire; 1 enemy will not attack unless provoked."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 335,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Voice of Peace",
     "effect": "Negotiate ceasefire; 1 enemy will not attack unless provoked.",
     "source_paragraph": 9395,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
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
  "id": "command",
  "activation": "Action",
  "targets": "One creature you perceive within30feet and line of effect; speak one word in a language you know. Actual hearing/understanding and hidden impossibility/prohibited conduct are resolved after payment, not through a free targeting oracle.",
  "duration": "One commanded regular turn, no concentration; ends at the target’s first future regular-turn END, excluding the current turn if underway. Extra turns do not execute the order. Outside initiative, resolve one ordinary behavior opportunity within6elapsed seconds; establish initiative if combat timing matters.",
  "concentration": false,
  "resolution": "If it cannot hear/understand the word, no command applies. Otherwise it makes a Wisdom save. Success: no new command. Failure: it must perform a legal bounded interpretation on its next regular turn, using only its actual existing permissions. An impossible or prohibited command creates no behavior; no replacement word is chosen. Reserve the shared hard-control allowance when establishing any actual whole-Action/turn component. If blocked, only independently satisfiable non-hard movement/interaction portions may apply; do not invent another command.",
  "effect": "After ordinary start-phase events, obey before contradictory voluntary choices. Approach: spend ordinary available movement toward you by a safe legal route, stopping on reaching an adjacent legal space or exhausting safe meaningful progress. Flee: spend ordinary available movement away by a safe legal route. Neither forces Dash or grants movement. Drop: ordinarily release one releasable held object chosen by the target/controller, using its actual ordinary release permission; ownership never transfers and normal later recovery remains possible. Halt: refrain from voluntary movement for that turn, without imposing Speed0 or preventing actual involuntary transport. Grovel: become/remain Prone for that turn if capable, without automatically losing Actions or legal crawling. Other one-word commands may require at most one coherent ordinary action/movement/interaction within this same turn and the limitations below; the word never grants an otherwise unavailable action or named condition. The target/controller chooses lawful details, safe route and object where the word leaves choices.",
  "limitations": "No compelled attack/knowingly harmful act, direct self-harm, known serious hazard, protected/private secret disclosure, permanent surrender/ownership transfer, knowing binding-oath/duty violation, spell or optional limited-resource expenditure. If circumstances make the commanded behavior prohibited or impossible before execution, that portion fails rather than rewriting the word or extending the deadline. One pending Command application per target across casters; a later legally established failed-save application replaces it. No restoration of an older replaced command or spent hard-control allowance. A saved-against/wholly invalid new command creates no replacement. Simultaneous unresolved decisions use ordinary initiative order, else a fixed neutral order, never a caster’s after-the-fact preference. Unaffected Actions/BA/Reactions and movement remain; one-time Drop/Approach/Flee instructions finish once satisfied, while Halt/Grovel persist for the affected turn. Compelled movement uses the target’s movement and can provoke normal opportunity attacks. Hard whole-Action/turn components use the existing combined source-character/target/encounter allowance across class features, spells and companions. A blocked hard component gains no invented fallback; independent printed components retain their own defense checks. A successfully established hard component claims the allowance once, not again each turn; ending, dispelling, replacing or suppressing it does not refund the encounter history. Actual boss/control immunities remain effective",
  "designNotes": "PRESERVED: Action/30feet/V,S,F, actual one-word compulsion for1round. NEW: WIS/hearing/language and bounded safe-command procedure. Exact completions retain other bounded words, define ordinary action costs, nonbanking competition and one-time versus turn-long instructions; they do not turn compulsion into voluntary advice.",
  "sourcePlacements": [
   {
    "name": "Command",
    "school": "Enchantment",
    "level": 1,
    "summary": "Force target to follow one-word command for 1 round."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 336,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Command",
     "effect": "Force target to follow one-word command for 1 round.",
     "source_paragraph": 9396,
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
  "id": "hideous-laughter",
  "activation": "Action",
  "targets": "One creature you perceive within30feet and line of effect; no biological, Humanoid or minimum-Intelligence predicate.",
  "duration": "Concentration, up to1minute, or earlier ending below. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": true,
  "resolution": "The target makes a Wisdom save. Success: no new application. Failure: immediately apply Prone and attempt a separate continuing Incapacitated component. The Incapacitated component claims the shared hard-control allowance when successfully applied; blocked hard control does not by itself block the independently printed Prone application. Actual Prone and Incapacitated immunities each retain their own scope.",
  "effect": "An actually Incapacitated target loses Action/BA/Reaction and ends actual concentration through its normal callbacks, including exact class exceptions. Incapacitated alone does not reduce Speed or prohibit speech. At the end of each affected regular turn, including the current turn if the application was established during it, repeat the WIS save; success ends the ongoing laughter application. Extra turns grant no additional repeat save. A positive damage packet after defenses and before temporary HP also ends the ongoing laughter application; a fully prevented0packet does not. Resolve already determined attack/hit/critical consequences normally before damage-triggered ending.",
  "limitations": "Prone is an immediate actual condition application, not a maintained forced posture: normal legal standing remains possible even while Incapacitated if it requires only movement. Crawling and speech follow actual conditions, without invented paralysis. Ending laughter never automatically stands the creature or restores concentration. If Incapacitated was blocked at application, no deferred hard component waits to activate later; the paid spell only inflicted whatever independent component could actually apply. For an existing valid hard application later suppressed by immunity, keep its clock and prior guard history; lifting suppression never creates a fresh use or replays Prone. Independent other sources remain. A new concentration cast still displaces incompatible old concentration before its save. Hard whole-Action/turn components use the existing combined source-character/target/encounter allowance across class features, spells and companions. A blocked hard component gains no invented fallback; independent printed components retain their own defense checks. A successfully established hard component claims the allowance once, not again each turn; ending, dispelling, replacing or suppressing it does not refund the encounter history. Actual boss/control immunities remain effective",
  "designNotes": "PRESERVED: Action/30feet/V,S,F, WIS, falls Prone and Incapacitated. NEW: concentration minute, repeat regular-end saves and positive-packet ending. Exact completion distinguishes immediate Prone from sustained Incapacitated, initial prevention from later suppression, and a current-turn repeat save from the maximum-duration clock.",
  "sourcePlacements": [
   {
    "name": "Hideous Laughter",
    "school": "Enchantment",
    "level": 1,
    "summary": "Target falls prone, incapacitated by laughter (WIS save)."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 337,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Hideous Laughter",
     "effect": "Target falls prone, incapacitated by laughter (WIS save).",
     "source_paragraph": 9397,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Wisdom save",
     "tags": [
      "Control"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "faction-charm",
  "activation": "Action",
  "targets": "One creature you perceive within30feet and line of effect; choose one exact canonical faction with which you actually currently have affiliation/membership.",
  "duration": "1hour/3,600elapsed seconds from application, no concentration; clocks continue through initiative/scene/plane changes.",
  "concentration": false,
  "resolution": "After commitment, confirm your actual current affiliation with the chosen faction. Established canonical campaign fiction can supply it; reputation, costume, logo, asserted title or possession of an emblem alone does not. If absent, no affinity applies and no hidden-membership diagnostic is returned. Otherwise the creature makes a Wisdom save. Success: no new effect. Failure: genuine strong favorable affinity toward the selected faction for the duration.",
  "effect": "The target ordinarily regards that faction favorably rather than neutrally/negatively where no stronger actual fact overrides that feeling. You gain advantage on actual Persuasion checks directed to this target specifically concerning that faction, its interests or cooperation with it. Ordinary beliefs, evidence, risk judgment, task legality and agency remain. End the application when you, or a creature the target actually recognizes as acting for this faction, commits an attack or knowingly harmful effect against the target, before the outcome; a later miss/prevention does not restore it. Unknown affiliation alone is not an omniscient ending trigger.",
  "limitations": "The faction is snapshotted at application; your later membership/leadership changes do not retarget or automatically end it. This is not Core Charmed, a command, numeric reputation, membership, credential, authority, legal rights, permanent loyalty or erasure of grievances. Each caster/target/faction has one affinity record; later failed save refreshes that matching record, success leaves an existing one unchanged. Different factions/casters may have independent feelings and deadlines; advantage still never stacks and conflicting interests grant no compelled choice. No ongoing30foot or communication tether; actual Persuasion still needs an ordinary interaction",
  "designNotes": "PRESERVED: Action/30feet/V,S,M/F as focus, strong faction affinity1hour, no source concentration. NEW: WIS, actual-affiliation predicate, genuine but bounded attitude, related Persuasion advantage and recognized-harm ending. Exact completion allows independent different faction relations without granting allegiance or stacked advantage.",
  "sourcePlacements": [
   {
    "name": "Faction Charm",
    "school": "Enchantment",
    "level": 1,
    "summary": "Target feels strong affinity toward your faction for 1 hour."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 339,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Faction Charm",
     "effect": "Target feels strong affinity toward your faction for 1 hour.",
     "source_paragraph": 9399,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "1 hour",
     "components": "V, S, M/F",
     "resolution": "Automatic or opposed as described",
     "tags": [
      "Ward",
      "Control",
      "Faction"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "alignment-suggestion",
  "activation": "Action",
  "targets": "One creature you perceive within30feet and line of effect. No requirement that its alignment be known; hidden canonical axes are resolved after paid casting.",
  "duration": "Concentration, up to1minute. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": true,
  "resolution": "The target makes a Wisdom save. Success: no new overlay. Failure: snapshot your actual current alignment orientation. For each axis defined both for you and for the target, compute one step toward your snapshotted value along Lawful–Neutral–Chaotic and Good–Neutral–Evil. Compute the target baseline without any previous Alignment Suggestion overlay on that target, retaining all independent actual alignment effects/records. An already matching or undefined axis gains no changed-value overlay. If at least one axis changes, replace the prior same-spell overlay with the new recorded axis values/deadline. A failed-save cast that changes no defined axis creates no new overlay and does not itself replace a valid older one; mandatory concentration transitions remain independent.",
  "effect": "The changed values are the target’s actual effective canonical alignment for rules that query those axes during the overlay, including real alignment-gated spells/items. Example: baseline Chaotic Evil targeted by a Lawful Good caster becomes Neutral Neutral; one such overlay never jumps two steps. Its values remain fixed until expiry/removal/replacement and do not recompute every time another underlying record changes. Unchanged/unoverlaid axes follow their actual underlying records. An independent effect such as Corrupted can change underlying alignment while this spell persists; that change remains and is exposed when the applicable overlay ends. One Alignment Suggestion overlay per target across casters; recasting cannot use its old overlay as a staircase for another same-spell step.",
  "limitations": "The spell grants no automatic knowledge of either character’s axes, including whether a value changed. Actual information protections still govern observations. It never compels matching behavior, belief, confession, loyalty, PvP, personality or oathbreaking; conduct clauses still judge actual conduct. Ending removes only this overlay, without restoring an old alignment snapshot, deleting independent changes or reviving a replaced overlay. Caster orientation is fixed at application, not tracked through later caster changes. Ward tag creates no ward. More specific alignment-changing effects retain their actual interaction rules; this card does not invent a general priority engine for every unrelated overlay",
  "designNotes": "PRESERVED: Action/30feet/V,S,M/F as focus, WIS, concentration minute and actual push toward caster alignment. NEW: temporary canonical one-step overlay on both eligible axes. Exact-review proposals: compute without previous same-spell overlay to prevent recast ratcheting, overlay only genuinely changed axes, fixed values, and no new application when no defined axis changes; independent base changes survive ending.",
  "sourcePlacements": [
   {
    "name": "Alignment Suggestion",
    "school": "Enchantment",
    "level": 1,
    "summary": "Subtly push target toward your alignment (WIS save)."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 340,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Alignment Suggestion",
     "effect": "Subtly push target toward your alignment (WIS save).",
     "source_paragraph": 9400,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Concentration, up to 1 minute",
     "components": "V, S, M/F",
     "resolution": "Wisdom save",
     "tags": [
      "Ward",
      "Alignment"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "resonance-influence",
  "activation": "Action",
  "targets": "One creature you perceive within30feet and line of effect. Choose Ease or Burden at casting; Ease requires actual willingness at application.",
  "duration": "Until the next qualifying spell commits or up to1minute, no concentration. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": false,
  "resolution": "Ease: automatic on a willing target; establish a pending−1RP final-price modifier. Burden: target makes a Wisdom save even if willing unless an independent rule grants a save waiver; failure establishes pending+1RP, success creates no replacement. One pending Resonance Influence record per target across casters; a successful eligible application replaces the previous mode/deadline. Invalid or saved-against application does not erase a valid old record.",
  "effect": "For the target’s next actual spell cast whose procedure has an RP-price interface, compute the ordinary legal RP price first: actual class/source rank/base, mandatory printed spell extras, applicable Dissonance surcharge, and only the exact eligible class/source reductions or waivers with their scopes/minimums. Then apply this spell’s final±1, minimum0, with no credit/refund. An ordinary0RP cantrip qualifies: Burden prices it at1; Ease leaves it0 and is still consumed. A genuine RP-priced spell reduced/waived to0 also qualifies; this final modifier can make its payment1. A charge-only item spell or free technique with no RP-price interface does not qualify and consumes nothing. An RP-priced actual class/item spell can qualify; paying RP for a nonspell technique alone does not. Validate adjusted affordability and all other preflight rules, then consume the record atomically at legal cast commitment with payment. Later failure/countering does not refund the rider. An illegal/unaffordable attempted cast never commits and leaves it available.",
  "limitations": "Ready pays/consumes at spell preparation, not release. This new application cannot retroactively alter its own already-paid casting price; a previously existing Influence may price that cast normally. Ordinary class minimums govern their own discount calculations first; the final Ease may then reduce an otherwise1RP result to0. Mandatory extras remain in that ordinary price, not omitted, though Ease can offset1RP of the resulting total. Other non-RP costs, charges, limited uses, rank/access/repertoire, components, Fractured restriction, Dissonance and Refrain are unchanged. A pending hostile+1 requires real adjusted affordability but does not grant the caster hidden knowledge of RP pools or pricing failures. Current quote_cast helper lacks this stateful modifier and class-discount integration; this card is a tabletop interface, not a runtime implementation",
  "designNotes": "PRESERVED: Action/30feet/V,S,F and next-spell RP cost±1. NEW: modes, willingness/WIS, minute, final-price ordering, replacement and cast-commit consumption. Exact-review proposal explicitly includes a normally RP-priced cast made free by another source, while excluding a source with no RP-price interface; final modifier follows source-specific minimum calculations.",
  "sourcePlacements": [
   {
    "name": "Resonance Influence",
    "school": "Enchantment",
    "level": 1,
    "summary": "Target's next spell costs +1 or -1 Resonance Points."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 341,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Resonance Influence",
     "effect": "Target's next spell costs +1 or -1 Resonance Points.",
     "source_paragraph": 9401,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Automatic or opposed as described",
     "tags": [
      "Resonance"
     ],
     "rp_cost": 2
    }
   }
  ]
 },
 {
  "id": "enthrall",
  "activation": "Action",
  "targets": "Choose up to3 distinct creatures you perceive within30feet and line of effect that can hear your casting words/tone at application.",
  "duration": "Concentration, up to1minute. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": true,
  "resolution": "Each eligible target independently makes a Wisdom save. Success: no effect on that target. Failure: captivate it, imposing disadvantage on all actual Perception checks for the duration, including checks about you or your tone.",
  "effect": "This affects actual rolled Perception checks under normal advantage/disadvantage rules; it neither creates a check nor changes its task permissions. Hearing is needed only at application. No continuing song, performance, instrument, sound, hearing or30foot tether is added. You still provide the audible V component and normal S/F. The three-target set is fixed on casting; no later replacement target can be added without another paid spell. Independent Enthrall sources have their own durations and concentration, but repeated disadvantage never stacks.",
  "limitations": "No automatic Search failure, passive-Perception−5, Hidden state, Stunned, Charmed, awareness deletion, forced movement or Action loss. Loss of this caster’s concentration ends this cast’s applications; another caster’s valid application remains. The source Enchantment rank2/Core349/3RP placement is preserved but unassigned and not selectable: it grants no all-hearers mode, extra-RP upgrade or additional class access. Current class access selects only this reviewed-candidate rank1 mode",
  "designNotes": "PRESERVED: rank1 Action/30feet/V,S,F, plural captivated creatures and Perception disadvantage. NEW: three targets, hearing, WIS and concentration minute. Rank2 all-hearers/WIS source remains intact as an unassigned variant pending a separate access/identity decision; no historical information is discarded.",
  "sourcePlacements": [
   {
    "name": "Enthrall",
    "school": "Enchantment",
    "level": 1,
    "summary": "Captivate nearby creatures; they have disadvantage on Perception checks."
   },
   {
    "name": "Enthrall",
    "school": "Enchantment",
    "level": 2,
    "summary": "Captivate all creatures that can hear you (WIS save negates)."
   }
  ],
  "sourceCoreEntries": [
   {
    "index": 343,
    "original": {
     "school": "Enchantment",
     "level": 1,
     "name": "Enthrall",
     "effect": "Captivate nearby creatures; they have disadvantage on Perception checks.",
     "source_paragraph": 9403,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Automatic or opposed as described",
     "tags": [
      "Utility"
     ],
     "rp_cost": 2
    }
   },
   {
    "index": 349,
    "original": {
     "school": "Enchantment",
     "level": 2,
     "name": "Enthrall",
     "effect": "Captivate all creatures that can hear you (WIS save negates).",
     "source_paragraph": 9411,
     "casting_time": "1 action",
     "range": "30 feet",
     "duration": "Instantaneous",
     "components": "V, S, F",
     "resolution": "Wisdom save",
     "tags": [
      "Utility"
     ],
     "rp_cost": 3
    }
   }
  ]
 }
]

## Explicit questions

Especially assess: Alignment Suggestion ignores its previous same-spell overlay to prevent recast ratcheting; only changed axes overlaid, no-change cast establishes/replaces nothing, independent underlying changes persist. Resonance Influence applies final±1 after actual source discount/minimum/waiver and can offset mandatory Resonance Shield1; does Burden make Mage Spell Sharing free cast cost1? Please explicitly resolve this exception. Also review Sleep all-applications physical waking, pending Flash/Command replacement, Command one-time Drop vs turn-long Halt/Grovel, Voice of Peace participant snapshot, Faction Charm independent faction records, Distract already-cancelled parent handling, Laughter current-turn repeat save vs never-deferred prevention. Rank2 Enthrall remains preserved unassigned. All provisional manuscript work, no runtime/balance/full-game certification.

## Exact relevant existing class source cards

DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json SHA256 25387b0dcfae0d53d689486d4b05d8ef5b24bed1b70f0baab970a82dbd370f89

{"id": "cleric.hero.saint.merciful-sacrament", "name": "Merciful Sacrament", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your Sacrament", "duration": "For that activation", "frequency": "1/short rest", "effect": "Merciful Sacrament. Tags: saint, sacrament. When you start Sacrament and at least one living ally inside its initial zone is at or below one-quarter maximum HP, you may reduce that Sacrament's Conviction cost to 0. Its RP cost and all other requirements remain. Because no Conviction is spent, this waived cost does not vent Dissonance.", "spellRank": null}

{"field": "engine", "index": 3, "text": "Cleric techniques use only their printed RP and Conviction costs. All RP is paid from the Cleric's Core Systems V 2 Resonance Point pool. A Cleric technique is not automatically an ordinary spell-rank cast and does not receive Overcast, spell-slot, cost-discount or spell-proc benefits unless a feature explicitly says otherwise. Ordinary spells continue to use Core V 2 spellcasting rules."}

DescentReviewChanges/ReviewBible/data/public/class_playtests/mage.json SHA256 c64782e192e2e63e5abed5728f9213c9d4cf956bce1a75da7a156dbfd1141e0b

{"id": "mage.arch.spell-efficiency", "name": "Spell Efficiency", "activation": "Passive", "cost": "0", "rangeAndTarget": "Self", "duration": "Until end of your next regular turn", "frequency": "At most once per turn", "effect": "Spell Efficiency. Tags: arcanist, resonance, focus. After you legally cast a Focus-eligible spell, your next differently named Focus-eligible spell of the same current element before the end of your next regular turn costs 1 less RP, minimum 1 RP. This reduction cannot apply to Focus finishers, Resonance Surge's additional cost or a spell already reduced to 0 by another explicit feature.", "spellRank": null}

{"id": "mage.hero.archmage.spell-sharing", "name": "Spell Sharing", "activation": "Action", "cost": "4 RP plus the shared card's printed RP cost", "rangeAndTarget": "One willing ally within 30 feet", "duration": "Until end of ally's next regular turn", "frequency": "1/short rest", "effect": "Spell Sharing. Tags: archmage, spell-sharing. Choose one Base or Arch Mage spell card you know with an Action activation and printed base RP cost 4 or less. Pay both costs now. The ally may cast that card once before the end of its next turn without paying RP, using your Mage spell attack and DC. It cannot share summons, Counterspell, Hero cards, finishers, Resonance Surge or another Spell Sharing.", "spellRank": null}

{"id": "mage.supplement.resonance-apex-new-playtest-capstone", "name": "Resonance Apex — NEW Playtest Capstone", "activation": "Triggered", "cost": "0 additional RP", "rangeAndTarget": "One Mage spell you are beginning to cast", "duration": "For that cast", "frequency": "1/long rest", "effect": "Before paying for one Mage spell, reduce that spell's printed RP cost by up to 10 RP, minimum final cost 0. This capstone is new playtest design and is not claimed as a recovered historical feature. The cast cannot also use Resonance Surge or generic Overcast. It remains one spell cast, follows ordinary Focus/Nuke Chain rules, and alters Dissonance only through rules that would already apply to that cast.", "spellRank": null}

DescentReviewChanges/ReviewBible/data/public/class_playtests/mirrorsage.json SHA256 9179729dd39e0a81f4f6d78b9fbb0c7fb296fb5d418aaa238d7ff6aa02b2bd3a

{"id": "mirrorsage.hero.light-weaver.sacred-echo-slot", "name": "Sacred Echo Slot", "activation": "Passive", "cost": "0", "rangeAndTarget": "One restricted archive slot", "duration": "While known", "frequency": "Continuous", "effect": "Add one slot usable only for Mend or Ward, total storage cap 6. If already at 6, designate one existing slot sacred instead; once/short rest its release costs 1 less RP, minimum 1. No duplicate slot or free record.", "spellRank": null}

DescentReviewChanges/ReviewBible/data/public/class_playtests/shaman.json SHA256 c88fcad8c14734cc852a95aee7b3686fd64ea2a8cfb9d014f4297b7efec94a62

{"id": "shaman.supplement.elder-spirit-accord-new-hero-capstone", "name": "Elder Spirit Accord — new Hero capstone", "activation": "Triggered", "cost": "1 long-rest use", "rangeAndTarget": "Your chosen Hero ultimate", "duration": "One activation", "frequency": "1/long rest", "effect": "When starting Elemental Chorus, Omen Loop or Bloodroot Trail, reduce its RP cost by 3, minimum 1, and add M to one damage/healing roll from that use. You must know that ability and still spend its own limited use. If you do not know it, instead reduce one known Hero technique's RP cost by 3, minimum 1. No extra duration, flask, totem, command or repeated cast.", "spellRank": null}

DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json SHA256 8ab2f4f43bcbced418fb266e5bd3216cff491b0c442c16f93438bd3556672c8b

{"id": "wizard.arch.spell-efficiency", "name": "Spell Efficiency", "activation": "Passive", "cost": "0", "rangeAndTarget": "Repeated prepared matrices", "duration": "Until end of your next regular turn", "frequency": "At most once per turn", "effect": "Spell Efficiency. Tags: arch, passive, resonance. After you cast a prepared matrix, the next cast of that SAME matrix family before the end of your next regular turn costs 1 less RP, minimum 1. This cost reduction does not suppress Refrain, cannot reduce Overcast or additional feature costs and cannot combine with itself.", "spellRank": null}

{"id": "wizard.hero.elementalist.core-sync", "name": "Core Sync", "activation": "Passive", "cost": "0", "rangeAndTarget": "Your current Elemental Affinity", "duration": "Permanent", "frequency": "Always", "effect": "Core Sync. Tags: hero, elementalist, passive, elemental. Rank-1 and rank-2 Wizard spells whose primary damage type matches your current Elemental Affinity cost 1 less RP, minimum 1. Once per long rest as a Bonus Action you may change your Elemental Affinity to Fire, Cold, Lightning or Earth; changing it does not alter currently active spell effects.", "spellRank": null}

{"field": "engine", "index": 13, "text": "RITUAL CASTING is automatic at Wizard 2. A Wizard spell in your spellbook with the Ritual tag can be cast from the book without being prepared by increasing its casting time by at least 10 minutes. A ritual cast costs 0 RP unless that ritual explicitly lists a consumed RP cost, cannot be used during an encounter and cannot generate or vent Dissonance through ordinary casting strain."}

{"field": "engine", "index": 15, "text": "MATRIX MASTERY MODIFICATIONS. After acquiring Matrix Mastery, each prepared ordinary spell matrix may carry at most one modification chosen during preparation. QUICK SUBSTITUTION: once per short rest, replace one matrix marked Quick Substitution with another spellbook spell of exactly the same rank using a 1-minute ritual instead of the normal 10-minute midday swap; the replacement loses the modification until the next long rest. COMPONENT ENHANCEMENT: when casting a damaging or healing matrix, spend 1 additional RP to add one extra die of the spell's primary damage or healing die to one roll; if the spell has no such die this modification has no effect. MATRIX LINKING: pair two different prepared matrix families during preparation; after legally casting one, the other costs 1 less RP, minimum 1, if cast before the end of your next regular turn, at most once per pair per round. STABILITY REINFORCEMENT: gain +2 on concentration saves caused by damage while maintaining that matrix. A matrix modification never creates another spell cast or proc event."}
