PART 2 OF 4. Concatenate parts in numerical order after removing this first line; all four belong to one exact manuscript packet.
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
