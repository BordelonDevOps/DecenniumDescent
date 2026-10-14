Periodic exact-review disposition: implemented both material blockers and all cleanup items. New source-component binding selects the specific reviewed identity OR explicit Core fallback, never both; initial condition immunity prevents creation. New per-application marker arbitration consumes all due clocks (including suppressed), excludes condition-suppressed groups from damage selection, keeps damage-type-immune records eligible until ordinary post-selection mitigation, applies Mage strongest-due vs Crimson permitted-instance sum before global comparison, and rejects duplicate application IDs/cross-target mixing. It does not turn a family tag into a condition application.

Bloodleech occupancy now ends when its last ongoing component ends; resolved critical healing does not occupy a slot, while an existing suppressed ongoing component still does. Blood Curse's display name does not create a second curse state. Ashblood's stale arbitration prose is removed. Every fire cure object now preserves exact explicit one/all/owner removal separately from generic Action/immersion. No original source was changed. The registry still says IN_PROGRESS.

Current meaningful reference checks: PASS84 custom-interface checks,57definitions,14hooks,114 exact source refs. New checks cover specific-vs-Core exclusivity, no-name-only creation, initial condition immunity, suppressed tick consumption, suppressed high group not starving legal Core fire, damage immunity still winning before mitigation, separate markers, two Crimson instances vsPB4, duplicate IDs, and empty/suppressed poison slot cleanup. Generic28 remains PASS82checks/4200Exhaustion states. Thirty-two periodic profiles are in this bounded package. No full runtime migration or balance claim.

Please give the final bounded periodic-family disposition with those corrections. Then proceed directly to the combat/time/action source conference below so we keep progressing through the whole game. DD16 remains open for other states and exhaustive semantic coverage. I also found separate Warrior serumStrain0–3 versus expeditionStrain0–6 sources; they are preserved for a dedicated reconciliation and not merged.

Next shared-rules pass: combat actions, turn timing and movement, covering DD03/DD17/DD18/DD19/DD20/DD21. Periodic condition alignment is a bounded pass; DD16 remains open for remaining roots/slows/marks/curse metadata and all-source semantic coverage. We should resolve these timing dependencies before finalizing all remaining riders. Core V2 remains authoritative; compatible V6 details can fill gaps. The exact paragraphs below include heading/definition context and original SHA. Do not import outside-game mechanics as if sourced.

Please propose a complete operational playtest procedure for the supplied actions/stances/maneuvers and highlight conflicts. Label NEW gap-fill choices explicitly. Address these concrete issues with deterministic examples, not just a checklist:

1. One round is ~6 seconds; regular initiative slots, ties, initial/reinforcement entry, surprised first turn, and opportunity to act. V6 surprise denies move/Action and Reactions until first-turn end: clarify Bonus Action/free interactions/concentration/periodic clocks without inventing unconsciousness. Extra-turn rules must preserve no extra periodic ticks/resource recovery/reaction reset unless expressly printed.
2. Reaction timing conflict: Core says one per round; V6 says one per round refresh start own turn. Choose an explicit interpretation and test reaction before first own turn + after own turn within same numbered round, delayed entry, extra turn, ready expiration and round-boundary hazards. Either literal global-round budget or regular-own-turn interval must be stated, not both contradictory counters. Existing falling marker uses regular slots, not bonus/extra turns.
3. Define round-duration endpoints for hostile target riders vs self buffs/auras, explicit next-turn phrases vs N rounds, effects applied midturn, skipped turns, out-of-initiative time and exact ties. No duration extension solely from changing initiative or adding extra turns. This will resolve existing Judged2rounds and Warrior Weakened2rounds among others. Proposed bridge: if target-bound hostile rider says N rounds without another endpoint, end of Nth future regular target turn; source/self sustained feature uses N source turns where printed, but need precise convention for bare N rounds without accelerating/shortening by order.
4. Ready: paid now or trigger, trigger-after resolution vs interrupts, legal target at release, expiration, forfeited costs, held spell concentration, RP/Dissonance/Refrain once, replacement of current concentration. Attack count for readied Attack needs explicit source-backed decision: several normalized class engines say ordinary Attack makes2; don't silently assume an off-turn one-attack restriction absent an adopted NEW guard. Movement Ready likewise action+reaction and no free action.
5. Actions: Attack/Cast/Dash/Disengage/Dodge/Guard/Brace/Aim/Help/Hide/Ready/Rally/Search/Use Object/Improvise, one normal object interaction. Aim is literally in Core Action table, but benefit lasts only own turn; clarify that paying Action leaves no ordinary attack unless another legal BA/action attack exists, or propose an explicit NEW rewrite if otherwise unusable. Do not silently make Aim a free +2. Brace and Rally lack DC/effect detail; provide bounded new procedures. Guard first attack consumes +2 even on miss? Interpose relation must be precise; do not create extra Reaction or negate attack targeting legality.
6. Stances: choose once before making an attack, durationstartnextturn, no retrospective switch. Clarify whether a turn with no attack may choose stance; stacking with Guard; Focused +1spellDCorattack appliesone spell then its reaction restriction remains until expiry; Counterspell exception doesnot grant that spell or bypasscost/Reaction. Mobile die-step sequence and minimum die; first5ft doesn't grantfree movement. Carrying ignoresone actual cargo penalty, not infinite capacity/noequipmentlimits. Guarded adverseSpeed clamp.
7. Disarm/Trip/Shove/Grapple opposed checks, hand/reach/size constraints, ties statusquo. Disarm landingtile and cursed/bondeditems, Sunder itemdurability crossreferencewithoutinventingdestruction, Feint one nextmeleeattack. Pin has no cost/save/DC in Core; Silence the Caster couldcreate automatic infinite concentration attacks without cost. Propose finite optional maneuvers declared beforeattack with tradeoff/usagecap rather than everyhit getsallriders. Press timing/movement and BreakFormation whoseadjacentGuardbonuses clear, no arbitraryenemyself-confusion. OverwatchordinaryReady vsSoldierengine distinct.
8. Movement multiplemodes/distance budgets, Dash, standing/crawl/squeeze/severeterrain costcomposition, occupiedspaces, forcedmovementwithoutOA, inabilitytomovewhileSpeed0, flightfall/hover, teleport. Existing CoreProne ruling overridesV6near-rangedadvantage; no reintroducing oldconflict. Squeezing and other dice modifiers use existing oneadv/disadvcancellation.
9. Cover half+2/threequarters+5bestonly, AC/DEXsave origin, areaeffect lineofeffect, totalcover, unseenknownlocation vs hiddenunknownlocation. CoreInvisible ends its own attack modifiers perobserverwhenpositionknown, previously agreed not immediately regrant sameV6unseenbonus solely becauseInvisible. Need coherent Hide/Search/passiveperception/removement/attackreveal rules and rangedclosecombat vsunseenhostile. Separate sight from positionknowledge and lineofeffect.
10. Retain playeragency and sourceauthority. No new classfeatures, freeequipment, spellknowledge, automaticcapture, mindcontrol, or secretlorefromcombat actions. Use mundane 5ft grid rules where needed, mark diagonalmetricnewchoice and explain movement/area choice.

I will turn your proposed rules into an explicit source-conflict table and bounded rule reference, then test counterexamples and return an exact review. Please focus this answer on the operational rules above and their decision points, without claiming all affected game areas are complete.

EXACT SOURCES
books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx SHA256 53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433; zero-based all w:p descendants
373: 5. Combat Sequence and Action Economy
374: Establish the field: determine terrain, light, hazards, objectives, exits, and cargo.
375: Determine awareness: compare Stealth, Perception, scouting, faction knowledge, and magical detection.
376: Roll initiative: d20 + Dexterity modifier + any class or preparation bonuses.
377: Resolve turns: movement, one action, one bonus action when granted, one free interaction, and one reaction per round.
378: Advance the encounter clock: hazards, reinforcements, morale, objectives, and boss phases act at the end of the round.
379: Conclude: resolve surrender, capture, pursuit, harvesting access, and noise consequences.
380: Actions
381: Action
382: Function
383: Attack
384: Make attacks allowed by your class and weapon.
385: Cast
386: Cast a spell or activate a Resonance technique.
387: Dash
388: Gain movement equal to Speed.
389: Disengage
390: Movement does not provoke opportunity attacks this turn.
391: Dodge
392: Visible attacks against you have disadvantage; Dexterity saves have advantage.
393: Guard
394: Gain +2 AC against the first attack before your next turn and enable Interpose.
395: Brace
396: Prepare against a charge, leap, forced movement, or door breach.
397: Aim
398: Do not move; gain +2 to one ranged or spell attack before the end of the turn.
399: Help
400: Grant advantage to an ally within a plausible working distance.
401: Hide
402: Attempt to become unseen.
403: Ready
404: Specify a perceivable trigger and prepare an action as a reaction.
405: Rally
406: Make a Charisma check to restore morale or end Frightened in an ally.
407: Search
408: Use Perception, Investigation, Arcana, or Engineering under pressure.
409: Use Object
410: Operate equipment, a consumable, cargo rig, lever, or artifact.
411: Improvise
412: Attempt a stunt; Director sets ability, proficiency, and DC.
413: Combat Stances
414: Once on your turn, before making an attack, choose a stance. The stance lasts until the start of your next turn. A class feature may improve or replace these options.
415: Stance
416: Benefit
417: Cost
418: Aggressive
419: +2 damage on weapon attacks.
420: -2 AC.
421: Guarded
422: +1 AC and advantage against shove.
423: -5 ft. Speed.
424: Mobile
425: The first 5 ft. of movement does not provoke.
426: -1 damage die step on opportunity attacks you make.
427: Focused
428: +1 spell save DC or attack for one spell.
429: Cannot take reactions except Counterspell.
430: Carrying
431: Ignore one cargo penalty.
432: Disadvantage on Dexterity saves.
433: 6. Movement, Position, and Terrain
434: Combat uses feet or 5-foot spaces. Movement can be split around actions and attacks. Difficult terrain costs 2 feet per foot. Severe terrain costs 3 feet per foot and may require a check.
435: Forced movement does not provoke opportunity attacks unless a feature explicitly says it does. Falling, flowing water, conveyor mechanisms, gravity changes, and living dungeon surfaces are common sources of forced movement.
436: Cargo matters. A creature carrying more Extraction Load than its safe capacity loses 10 feet of Speed, cannot Dash without a check, and has disadvantage on Acrobatics. Dropping a cargo harness is a free interaction if it was prepared for release.
437: Terrain Tags
438: Tag
439: Effect
440: Narrow
441: Large weapons and broad formations are hindered; creatures may be unable to pass.
442: Unstable
443: A hard impact or failed Dexterity save changes or collapses the terrain.
444: Resonant
445: Spells of one school cost 1 less RP; an opposed school costs 1 more.
446: Corrupted
447: Failed saves or overcasting can add Corruption.
448: Silent
449: Verbal components and audible commands fail or require a check.
450: Flooded
451: Swimming, buoyancy, current, and fire resistance rules apply.
452: Vertical
453: Height, falling, climbing, and aerial control dominate.
454: Living
455: The terrain reacts at the end of the round and can be wounded, fed, or pacified.
456: Claimed
457: A faction, guardian, or dungeon-authority effect can issue commands through the area.
458: 7. Attacks, Defense, and Tactical Actions
459: An attack roll is d20 + ability modifier + proficiency when proficient. A natural 1 misses. A natural 20 hits and doubles damage dice. Armor Class remains the primary defense, but cover, stance, shields, conditions, and reactions determine whether a target can survive concentrated attacks.
460: Tactical Maneuvers
461: Maneuver
462: Rule
463: Disarm
464: Replace one attack; Athletics or weapon check vs Athletics/Acrobatics. On success, held item falls in an adjacent space.
465: Feint
466: Bonus action Deception vs Insight. On success, gain advantage on the next melee attack this turn.
467: Interpose
468: Reaction while Guarding; move 5 ft. and become the target of an attack against an adjacent ally.
469: Overwatch
470: Ready a ranged attack against movement through a named lane; the attack does not consume ammunition until triggered.
471: Pin
472: On a successful ranged hit, reduce target Speed by 10 ft. until it spends an action or succeeds on a Strength check.
473: Press
474: After hitting in melee, move 5 ft. into the target’s vacated space if it retreats before your next turn.
475: Sunder
476: Attack an object, shield, armor component, or construct joint. Damage applies to item durability rather than HP.
477: Trip
478: Replace one attack; Athletics vs Athletics/Acrobatics. On success, target falls Prone.
479: Withdraw
480: Action; move up to half Speed without provoking and gain +2 AC until movement ends.
481: Secure Cargo
482: Action; attach, lift, transfer, or protect up to one Extraction Load class of cargo.
483: Silence the Caster
484: A melee hit can force an immediate concentration check and prevents reactions with verbal components until target’s next turn.
485: Break Formation
486: Shove with disadvantage; on success push 10 ft. and remove Guard bonuses from adjacent allies.

books/player/Decennium_Descent_Player_Rulebook_v6.docx SHA256 a753da2ce935ed29e4f3f14575f3785140821c3f0c43adb760da6149b12e295e; zero-based all w:p descendants
8066: Chapter 8: Combat in Aethel
8068: THE SHARP RING OF STEEL ON STEEL, THE CRACKLE OF ARCANE ENERGY, THE GUTTURAL ROAR OF A MUTATED BEAST, combat in the fractured world of Aethel is a brutal dance between survival and oblivion. Whether facing down corrupted monstrosities in forgotten ruins, navigating treacherous political skirmishes in Ironhaven, or battling rival expeditions in the wildlands, the rules of engagement are vital for any adventurer seeking to carve out a destiny, or simply live to see another dawn.
8070: This chapter provides the framework for resolving conflicts in Decennium Descent. It covers the flow of battle, the actions characters can take, and the consequences of injury, integrating Aethel’s unique mechanics like Reputation, Alignment, and Corruption into the familiar rhythm of rounds and turns.
8072: The Order of Combat
8074: A combat encounter unfolds in a structured sequence, breaking down the chaos into manageable steps. A round represents approximately 6 seconds of intense action. During a round, every participant takes a turn in a specific order determined by initiative.
8076: Combat Step by Step
8078: 1.  Determine Surprise: The Director (Director) decides if anyone is caught unaware. This often involves comparing Dexterity (Stealth) checks against passive Wisdom (Perception) scores, but high Reputation or specific faction knowledge might grant bonuses against being surprised by certain groups.
8079: Establish Positions: The Director determines the location of all combatants based on the narrative context, marching order, or stated positions.
8080: 3.  Roll Initiative: Every participant rolls a d20 and adds their Dexterity modifier. The Director may roll once for groups of identical creatures. Combatants act in order from highest roll to lowest. Ties between players are resolved by the players; ties involving NPCs/monsters are resolved by the Director, potentially influenced by Reputation scores in social-combat scenarios.
8081: Take Turns: Each combatant takes their turn, performing movement and actions.
8082: Begin the Next Round: Once every combatant has acted, the round ends. Repeat step 4 until the conflict concludes.
8084: Surprise
8086: If you are surprised, you cannot move or take an action on your first turn, and you cannot take a reaction until that turn ends. A creature might be surprised even if others in its group are not.
8088: Initiative
8090: Your initiative roll determines your place in the combat order for the entire encounter. This order remains consistent from round to round.
8092: Your Turn
8094: On your turn, you can perform the following:
8096: *   Move: Move up to your speed.
8097: *   Action: Take one action (see "Actions in Combat").
8098: *   Bonus Action: If a feature or spell grants one, take one bonus action.
8099: *   Reaction: If triggered, potentially use your reaction (though usually not on your own turn).
8100: *   Free Interaction: Interact with one object or feature of the environment for free.
8102: You decide the order of your move and action. You can forgo any or all of these activities.
8104: Bonus Actions
8106: Many class features (like the Dragoon's Momentum abilities or the Thief's Cunning Action), spells, or special abilities grant the option to take a bonus action. You can only take one bonus action per turn, even if multiple options are available.
8108: Reactions
8110: Reactions are instant responses to triggers, such as an enemy moving out of reach (provoking an opportunity attack). You get one reaction per round, which refreshes at the start of your turn. If a reaction interrupts another creature's turn, that creature continues its turn after the reaction.
8112: Other Activity on Your Turn
8114: You can communicate briefly (speech, gestures) and interact with one object for free (drawing a weapon, opening a door). Interacting with a second object requires your action. Complex interactions (disarming a complex trap, deciphering a rune under pressure) might also require an action at the Director's discretion.
8116: Movement and Position
8118: Effective positioning is key to survival. Your speed determines how far you can move.
8120: Breaking Up Your Move
8122: You can split your movement, moving some distance before your action and some after. If a class feature grants multiple attacks, you can even move between those attacks.
8124: Using Different Speeds
8126: If you have multiple movement types (walking, flying, swimming), you can switch between them. Subtract the distance already moved from the new speed to determine remaining movement.
8128: Difficult Terrain
8130: Rubble, thick undergrowth, steep stairs, shallow bogs, crowded spaces, and areas tainted by Corruption can be difficult terrain. Every foot of movement in difficult terrain costs 1 extra foot (e.g., moving 5 feet costs 10 feet of speed).
8132: Being Prone
8134: You can drop prone without using speed. Standing up costs half your speed. Moving while prone requires crawling (each foot costs 1 extra foot, 3 feet total in difficult terrain). Attack rolls against prone creatures have advantage if the attacker is within 5 feet, otherwise they have disadvantage. A prone creature has disadvantage on its own attack rolls.
8136: Moving Around Other Creatures
8138: You can move through a nonhostile creature's space (it's difficult terrain). You can only move through a hostile creature's space if it's at least two sizes larger or smaller than you. You cannot willingly end your move in another creature's space.
8140: Flying Movement
8142: If a flying creature is knocked prone, has its speed reduced to 0, or is otherwise unable to move, it falls unless it can hover or is held aloft by magic.
8144: Creature Size
8146: Creatures occupy space from Tiny (2.5x2.5 ft) to Gargantuan (20x20 ft or larger). Most player races are Medium (5x5 ft). A creature's space is the area it controls in combat.
8148: Squeezing
8150: A creature can squeeze into a space one size smaller than itself. While squeezing, movement costs 1 extra foot per foot moved, attack rolls and Dexterity saves have disadvantage, and attacks against the creature have advantage.
8152: Actions in Combat
8154: Choose one action from this list, one granted by your class or features, or improvise an action (subject to Director approval).
8156: *   Attack: Make one melee or ranged attack. Features like Extra Attack allow multiple attacks.
8157: *   Cast a Spell: Use your action to cast a spell with a casting time of 1 action.
8158: *   Dash: Gain extra movement equal to your speed.
8159: *   Disengage: Your movement doesn't provoke opportunity attacks for the rest of the turn.
8160: *   Dodge: Until the start of your next turn, attacks against you have disadvantage if you can see the attacker, and you make Dexterity saves with advantage. You lose this benefit if incapacitated or your speed is 0.
8161: *   Help: Grant advantage to an ally on their next ability check (if made before your next turn) or their first attack roll against a creature within 5 feet of you (if made before your next turn).
8162: *   Hide: Make a Dexterity (Stealth) check to hide. Success grants benefits (see "Unseen Attackers and Targets").
8163: *   Ready: Prepare an action (or movement up to your speed) to use as a reaction in response to a perceivable trigger. If readying a spell, you cast it and hold the energy, requiring concentration.
8164: *   Search: Make a Wisdom (Perception) or Intelligence (Investigation) check to find something.
8165: *   Use an Object: Interact with an object that requires an action (like activating some magic items) or interact with a second object on your turn.
8166: *   Use Class Feature: Many class features require an action, bonus action, or reaction, as specified in their descriptions (see Chapter 3).
8168: Making an Attack
8170: Whether using a weapon or a spell, attacks follow these steps:
8172: Choose a Target: Select a target within range.
8173: Determine Modifiers: The Director determines cover, advantage/disadvantage, and other situational modifiers (like those from Corruption or Reputation effects).
8174: Resolve the Attack: Roll a d20 + relevant ability modifier + proficiency bonus (if proficient). If the total equals or exceeds the target's Armor Class (AC), the attack hits. Roll damage on a hit.
8176: Attack Rolls
8178: *   Ability Modifier: Strength for melee (unless Finesse), Dexterity for ranged. Spell attacks use your spellcasting ability.
8179: *   Proficiency Bonus: Added if proficient with the weapon or when making a spell attack.
8180: *   Rolling 1 or 20: A 1 always misses. A 20 always hits and is a critical hit.
8182: Unseen Attackers and Targets
8184: *   Attacking a target you can't see: Disadvantage on the attack roll.
8185: *   Attacking while unseen: Advantage on the attack roll. You reveal your location upon attacking.
8187: Ranged Attacks
8189: *   Range: Attacks have normal and long ranges. Attacks beyond normal range have disadvantage. Attacks beyond long range are impossible.
8190: *   Close Combat: Making a ranged attack while within 5 feet of a hostile creature that can see you and isn't incapacitated imposes disadvantage on the attack roll.
8192: Melee Attacks
8194: Attack a target within your reach (usually 5 feet). Unarmed strikes count as melee attacks.
8196: Opportunity Attacks
8198: If a hostile creature you can see moves out of your reach, you can use your reaction to make one melee attack against it. This occurs just before it leaves your reach. Teleporting or being moved involuntarily doesn't provoke opportunity attacks. The Disengage action prevents provoking them.
8200: Two-Weapon Fighting
8202: When taking the Attack action with a light melee weapon in one hand, you can use a bonus action to attack with a different light melee weapon in the other hand. You don't add your ability modifier to the bonus attack's damage (unless the modifier is negative).
8204: Grappling
8206: Use the Attack action (replaces one attack if you have multiple) to make a special melee attack. Target must be within reach and no more than one size larger. Make a Strength (Athletics) check contested by the target's Strength (Athletics) or Dexterity (Acrobatics). On success, the target is grappled (condition details in Appendix). Escaping requires an action and winning the contested check. Moving a grappled creature halves your speed (unless it's two+ sizes smaller).
8208: Shoving a Creature
8210: Use the Attack action (replaces one attack) to make a special melee attack. Target must be within reach and no more than one size larger. Make a Strength (Athletics) check contested by the target's Strength (Athletics) or Dexterity (Acrobatics). On success, you either knock the target prone or push it 5 feet away.
8212: Cover
8214: Obstacles provide cover:
8216: *   Half Cover (+2 AC/Dex saves): Obstacle blocks at least half the body (low wall, creature).
8217: *   Three-Quarters Cover (+5 AC/Dex saves): Obstacle blocks about three-quarters (arrow slit, thick tree).
8218: *   Total Cover: Cannot be targeted directly by attacks or spells (though area effects might still reach).
8220: Damage and Healing
8222: Combat involves dealing and recovering from harm.
8224: Hit Points (HP)
8226: Represent durability and luck. Damage reduces current HP. Effects are only felt when HP drops to 0.
8228: Damage Rolls
8230: Roll specified dice + modifiers. Weapon attacks add the same ability modifier used for the attack roll. Spells specify damage dice and modifiers. Roll once for area effects hitting multiple targets.
8232: Critical Hits
8234: On an attack roll of 20, roll all damage dice twice, then add modifiers.
8236: Damage Types
8238: Acid, Bludgeoning, Cold, Fire, Force, Lightning, Necrotic, Piercing, Poison, Psychic, Radiant, Slashing, Thunder. Some Aethel-specific effects might deal Corruption damage (often Necrotic or Psychic with additional debilitating effects determined by the Director or source).
8240: Damage Resistance and Vulnerability
8242: *   Resistance: Halves damage of that type.
8243: *   Vulnerability: Doubles damage of that type.


EXISTING SHARED CLASS INTEGRATION (already operational draft; preserve or explicitly supersede, never ignore)
# Shared rules for the class playtest drafts

**Provisional design integration, 8 October 2026.** These rules make the class drafts usable together for testing. They preserve each protected class engine while specifying missing timing and replacing conflicting old percentages. They do not rewrite the approved Word books. Original descriptions and alternate registry entries remain in `data/playtest/class_sources`.

## Reading a class card

Use the class's own level, never total character level, for gates and effects. **L** means that class level; **S** is 1/2/3/4 at class levels 1/5/11/17. **M** means max(1, the class ability modifier), for effect a mounts only. Attacks use d20 + normal character proficiency + the actual appropriate ability modifier. Class save DC is 8 + normal proficiency + actual class ability modifier. Negative modifiers still apply to attacks and DCs. One tile is 5 ft. Fractions round down unless specified. Distances cannot be negative.

A weapon attack uses its usual ability, weapon die and damage type. A technique that says “make one weapon attack” replaces your Action with that attack; it does not also grant a normal Attack Action or Extra Attack. Generic attack-speed language has no effect beyond the exact attacks printed in the draft. A spell attack uses the class's stated casting ability. Natural 1 misses and natural 20 hits/critically doubles damage dice; flat bonuses do not double. A save succeeds at DC; “fails by 10” means the total is at least 10 below DC. Critical-range improvements never stack; use the broadest one.

An ability is known only if granted or selected by the draft schedule. Satisfy all printed prerequisites, target legality, action availability, recharge and resource costs before spending anything. A failed legal attack/save attempt still pays; an illegal activation spends nothing. No resource goes below 0 or above its cap. A class feature name shared with a spell does not grant both versions; use the version selected, with its own cost and timing. Names and source text are preserved; the current card is the operational draft.

## Action and timing limits

One regular Action, one Bonus Action if a feature permits it, normal movement and one Reaction between starts of your turns. A free trigger costs no Action only if expressly stated. All grants share **one extra full Action per creature per round**. An extra Action cannot grant another Action, recharge itself, or start another extra-Action grant. It supplies no extra Bonus Action or Reaction. A card granting additional attacks is not permission to repeat all class riders on every hit: obey each rider's frequency.

Recharge N sets a counter to N after use; reduce once at the start of the owner's regular initiative turn, whether able to act or not. Extra turns/Actions do not tick it. Outside combat tick once per 6 elapsed seconds, without double counting. Recharge 2 used on turn 1 is ready on turn 3. A positive counter can be reset/shortened at most once per ability per round. Zero counters are not legal reset targets and expend no reset use. Resets never restore RP or per-rest uses or grant an immediate activation.

An encounter is a genuine scene of uncertain opposition chosen by the Director, not a player declaration used to reset resources. No encounter gain from attacking allies, one's summons, harmless animals, helpless captives or reused corpses. Out-of-combat abilities retain all printed costs and time. Short-rest means a completed uninterrupted hour of permitted recovery; long-rest means a completed 8-hour Rest Watch. This time convention is a draft integration. Expedition pressure, supplies, safe locations and rest debt still matter. A long rest also refreshes short-rest uses; a short rest never refreshes long-rest uses. Weekly uses refresh after seven full in-world days, not repeated rests.

## Targets, concentration and control

Unless expressly stated, perceive the target, remain within range and have line of effect; total cover blocks targeting. “Ally” includes self unless it says OTHER. A list cannot contain a creature twice. Select up to the printed limit; an empty target list is not a valid way to farm activation benefits. Zones remain at their chosen point unless described as an aura; allies can leave and lose their benefits. An aura requires its owner conscious unless the card supplies a bounded exception. An effect ending at “end next turn” means the affected creature's next turn only when the card says target's; otherwise the user's.

One concentration slot for all spells, Chants, Veinweaves, forms or zones that require concentration. Starting another ends the old before the new effect resolves, except for an explicit limited linked-effect rule. Damage prompts CON save against max(10, floor(damage/2)); incapacitation or a failed save ends concentration. The round-down convention is a deliberate pilot interpretation. Concentration does not demand a Bonus Action unless maintenance says so. For a paid 3-pulse effect, start is pulse 1; pay maintenance on each of the next 2 regular turns by turn end for pulses 2/3. Missing payment ends it at that turn's end; otherwise it ends at start of turn 4. No repeated start triggers on maintenance.

Forced movement does not provoke opportunity attacks unless explicitly stated, cannot place a creature inside solid matter, and stops at an obstacle. Grapples use the card's save/DC, can be escaped with an Action and STR(Athletics) or DEX(Acrobatics) against that DC, and end beyond reach. A root sets Speed 0 but does not remove Actions. Slows reduce Speed to minimum 0. Silence blocks verbal spells/audible abilities, not all thought or all class features. Charmed effects never determine a player's beliefs; use only the printed action restrictions.

No repeated hard denial without a new save and cost. For this class suite, a creature can suffer **Stunned, compelled loss of its whole Action/turn, or equivalent hard denial from a given character at most once per encounter**, across that character's class features; later such riders fail while damage and soft riders resolve normally. Record source and target. This draft guard is broader than the older Oracle-only ceiling and is an explicit balance proposal. Reaction denial, Speed reduction, penalties and Frightened do not count as whole-turn loss. Do not silently waive boss immunities, legendary defenses or anatomy.

## Damage, healing, stacking and companions

Roll once for each shared area/pulse and apply saves/defenses to each target separately; separate attacks roll separately. Halve once for a successful save and apply resistance/immunity normally. Same-named conditions/bonuses do not stack unless a printed cap allows it; same-stat flat bonuses from these class techniques use the strongest. Different resources remain separate. Damage reduction from these class features uses the strongest flat reduction, then applies resistance; it cannot create negative damage or healing. Temporary HP never stack; choose the larger remaining amount. Immunity is not reduced resistance.

Repeated permanent HP recovery must consume finite RP, a per-rest use or another finite resource; a combat-generated gauge alone never enables unlimited healing. Healing cannot exceed maximum HP or erase Wounds, death consequences, debt or Corruption unless explicit. Downed is living at 0 HP; dead is different. Resurrection requires a willing soul and sufficiently intact body, obeys its time window, cannot create a duplicate and never refunds the feature on failure to meet known prerequisites. Sacrificial HP is actual unpreventable loss, cannot be redirected or paid with temporary HP, and is not damage for resource triggers. It cannot reduce the donor below 1 unless a card expressly grants a death-triggered effect.

No damage/healing copy repeats the source's costs, procs, resource generation, critical bonus dice, buffs, actions, cooldown resets or duration. Compute fractions once, capped at 100% of one stored source unless an explicit card states a separately priced higher amount. Copies still cause ordinary damage consequences, concentration checks and death. A copy cannot copy another copy. A target/source record must refer to an actual resolved event, not merely a known ability name.

Where a class card calls for a **standard companion** without a more specific profile, use: Small or Medium; AC 12+floor(PB/2); HP 2 L; walking Speed 30 ft; saves equal owner's PB; one melee or ranged attack (reach 5 ft/range 30 ft) at owner's class attack bonus, damage S d6 of the printed type. It has no independent class features, resources, loot, death triggers or extra turns. All companions belonging to one character share one Bonus Action command and **one damaging attack/action total per round** unless a specifically priced feature grants more. Without a command they move and Dodge. Act immediately after owner. A standard companion lasts 1 minute, disappears at 0 HP and cannot be healed for free by dismissing/resummoning. The creation cost must be paid again. Creature-specific stat blocks override this profile only where explicitly printed.


The existing one-Reaction-between-starts clause is therefore the current class candidate, not a blank decision. Prefer retaining that regular-own-turn interval unless a concrete Core conflict requires explicit supersession. Existing one-extra-Action/global-round cap is separate. Generic Grapple and Core condition variants already supersede conflicting shared-reference generic clauses where our later condition guide says so. Please state all new precedence clearly.
