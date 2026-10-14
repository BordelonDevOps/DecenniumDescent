"""Author the twelve agreed social/faction directions without altering sources."""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
import json
import re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'ex58-final-gpt-verdict'

def read(p): return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}
def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

SECTIONS = []
def section(n, title, player, director):
    SECTIONS.append({'id': f'SO-{n:02d}', 'title': title, 'player': player, 'director': director})

section(1, 'Ask for a concrete outcome',
'''State what your character wants and how they try to obtain it. You can describe the approach in ordinary words; you do not need to perform a voice, accent or persuasive speech.

Before a consequential check, establish this scene frame:

| Field | What to establish |
|---|---|
| Want | The specific change each side wants before the scene ends |
| Leverage | The offer, evidence, threat or withholding each side can actually use |
| Limit | What the decision-maker cannot or will not concede under current conditions |
| Clock | The real deadline and time needed for this exchange |
| Witness | Who can perceive the exchange or later receive a report |

Identify the people involved, the resource or information requested, its owner/controller, and who can authorize the concession. A person may possess a key without permission to sell the building. A clerk may permit supervised viewing without permission to give away the record.

The Director states the obtainable success and its terms, failure, any optional costly alternative, any available extra on Critical Success, and any extra consequence on Critical Failure. Agree the approach, ability/skill, resolution method, difficulty, duration and costs before committing the work and rolling. The Director can preserve secrets while explaining an observable obstacle or that this request cannot currently succeed. A promised ordinary Success cannot secretly require Critical Success or acquire a new price after the die.

If willingness, authority and prerequisites already settle a routine request, record the agreement and carry it out without a check. If the requested outcome is impossible or presently unavailable, no check can create it. You may seek a different feasible outcome. Roll when a meaningful, possible uncertainty remains.

Close the approach when its agreement, refusal or interruption is recorded. Later performance can still be pending. A new request follows the changed-circumstances rules below.''',
'''Give the actual decision-maker a bounded want, leverage and limit before selecting a DC. Separate true scene facts from each participant's current knowledge and beliefs. Neither a role title nor a faction score proves access, funds, legal powers or knowledge. Do not offer a successful information result whose source cannot contain the answer.

Expose the stakes needed for an informed choice without publishing private motives. If the current approach cannot work, identify the observable obstacle or state that no roll is available for that concession. A successful roll delivers the feasible concession declared, even if an undisclosed personal motive makes the NPC dislike agreeing.

Maintain one scene identity and linked approach history. A closed negotiation does not require waiting for its future delivery or every later consequence. Those obligations retain their own deadlines and records.''')

section(2, 'Resolve the declared uncertainty',
'''Choose the procedure before seeing any dice. A social concession or bounded inference normally uses a task against a fixed DC. Two actors making genuinely opposed attempts can use opposed totals. An explicit feature using a saving throw or passive Insight keeps its own procedure.

These are new ordinary references where no more specific source supplies the DC:

| DC | Negotiable concession |
|---:|---|
| 10 | Plausible, modest and within the person's authority |
| 13 | The person has a substantial reservation |
| 16 | Difficult, but genuinely negotiable |
| 19 | Exceptional leverage for an actually possible outcome |

Do not add a general route-tier or standing modifier to these DCs. Use only adjustments an applicable rule actually grants.

For a fixed task, compare the total with the DC: at least DC+10 is Critical Success; at least DC is Success; at most DC−10 is Critical Failure; the remaining totals below DC are Failure. Then a natural 20 improves one degree and a natural 1 worsens one, bounded at the ends. An impossible action does not acquire a roll or a fabricated failure margin.

| Final degree | Result |
|---|---|
| Critical Success | The promised success on its stated terms, plus only the declared available extra |
| Success | The promised success on its stated terms |
| Failure | The declared refusal/failure; a costly alternative exists only if offered beforehand and feasible |
| Critical Failure | That failure plus only the declared actual extra consequence; a costly alternative exists only if expressly offered for this branch |

An optional costly agreement is separate from the failed check. Accept its stated terms if willing and able, or decline and keep the unspent payment along with the refusal. Accepting needs no new roll merely to enact a feasible offer. Its performance still takes time, and the original roll remains failed. No outcome degree automatically supplies obedience, truth, standing, consent or resources.

For opposed checks, compare the two declared final totals: higher wins; a tie leaves the existing situation unchanged. Task degree shifts for natural 1/20 do not apply, and there is no general opposed critical reward. Ordinary saves remain binary under Core. Apply an operative source's reroll only in its exact window and with its exact replacement rule.''',
'''The manual's full success, costly success and refusal/reversal are narrative possibilities. The four task degrees do not create a fourth secret price schedule. At a stated DC of 13, a final Success grants the promised concession; do not reserve it for a total of 23.

Record both an initial task failure and any separately accepted costly bargain. Require the actual payer, funds, authority and delivery. A failed task cannot automatically deduct the price of a declined alternative. An extraordinary die cannot bind an absent owner or establish a player's belief.

Use opposed checks for actual opposing attempts, not as a second defensive roll after a fixed-DC result. A feature's passive test or save is not replaced because another method would give a preferred outcome. Specific source exceptions remain attached to their exact feature.''')

section(3, 'Choose a skill for the approach',
'''| Skill | What the approach can resolve |
|---|---|
| CHA (Persuasion) | A genuinely negotiable decision on stated terms |
| CHA (Deception) | Belief in a particular communicated claim |
| CHA (Intimidation) | A decision influenced by a credible perceived risk |
| CHA (Performance) | The declared audience response to an actual performance |
| CHA (Reputation) | An appeal to credentials or standing actually known or credibly demonstrated to the recipient |
| WIS (Insight) | A supported inference about observed motive, hesitation or leverage |
| INT (Investigation), History or an appropriate tool/skill | Its actual evidence or knowledge task, such as examining a document |

Add one applicable proficiency contribution, or expertise replacing it where granted. Several persuasive proficiencies do not add several bonuses. Neither a numeric trade level nor the saved standing score adds another bonus unless a specific operative rule says so.

Deception can change a belief without changing history. Insight cannot read an inaccessible document, detect every lie, read minds or force a player to believe a diagnosis. A sound answer can be that the observed evidence cannot distinguish two motives. Translation establishes received meaning, not truth.

A particular lie confronted by active scrutiny can use CHA (Deception) opposed by WIS (Insight). A bounded inference without an active opponent normally uses a fixed DC. Physical forgery examination uses its declared Investigation/tool procedure. A credible threat does not automatically require a saving throw or impose Frightened. A genuine competing social strategy can be an opposed attempt when declared that way beforehand.

Useful true information may settle a routine request without rolling. A successful Performance grants its stated audience response, not a license, access to property or magical crowd control. A Reputation appeal must have evidence the recipient can actually receive. The result does not automatically change permanent standing.''',
'''Choose from the current twenty-skill foundation. Do not introduce a new universal Streetwise, Banking, Lore or faction-proficiency skill through this chapter. Existing narrowly reviewed aliases and knowledge methods keep their exact scope.

Keep fact, communicated claim, translation and inference distinct. A true statement may be unpersuasive for a real reason; a believed false report is still false. Failure need not create false certainty. Any critical extra information must be supported and declared.

Thief Feint's source-specific CHA or DEX+PB versus passive Insight is a combat procedure, not a general negotiation. Do not give it a second PB or substitute active opposed Insight. An actual spell or knowledge feature supplies only its own bounded information, including an unknown result when appropriate.''')

section(4, 'Use standing as a relationship',
'''This chapter uses the new ordinary standing scale taught in the Haven module:

| Score | Band |
|---:|---|
| −3 or −2 | Hated |
| −1 | Disliked |
| 0 | Neutral |
| +1 | Liked |
| +2 or +3 | Honored |

Standing can influence whether an institution will consider a request and what terms are plausible. It does not itself create permission, credit, an appointment, available stock or authority. It adds no automatic bonus, penalty, advantage or disadvantage to a social check under this procedure.

CHA (Reputation) remains a separate skill: add its one eligible proficiency/expertise contribution to an appropriate appeal. A known score of +2 does not add another +2. Specific acquired item, class and background modifiers retain their actual conditions and stacking rules. Reviewed equipment sale fractions still use the buyer's known relationship where that particular schedule applies; they are not a universal price modifier.

When bringing forward an older character, preserve the original score and its version. A companion record marked +2 and an older Loop record marked +2 did not use the same labels. Unknown versions need interpretation before use; absence is not a recorded neutral score. Keep genuinely earned access, titles and obligations even when deriving a new display.''',
'''The older Player seven-band table (Revered +5 through Hated −5) and Loop eleven-band access table remain complete source receipts. This is an explicit new choice to give neither table an automatic current d20 modifier, not a silent numeric conversion.

An evidenced companion-score-v1 +2 means current +2/Honored. The old Loop +2 meant Favored; an explicitly recorded RP-A01 mapping derives +1/Liked without overwriting the raw source or earned privileges. Unknown versions remain unresolved. A +3/Honored display does not reduce the score to +2.

The reputation module will bind all original faction/background records and save probes. This general player chapter exposes current policy and known relationships, not private faction descriptions, unknown save keys or hidden memberships. Do not use a category name as proof of an actual alliance or a particular institution's authority.''')

section(5, 'Keep alignment-dependent questions separate',
'''Ordinary social checks in this candidate receive no automatic alignment-derived advantage or disadvantage. Shared goals, stated values, promises and trustworthy conduct can provide genuine leverage in the scene; they do not establish a cosmic classification or add a numerical modifier.

An acquired oath or class feature still follows its exact stated restrictions. If a particular use depends on a deep meaning not yet defined, record that specific unresolved requirement. It does not prevent ordinary conversation, trade, travel or a standing record.

The older alignment-modifier wording is preserved for the later cosmology review. This chapter does not establish its compatibility chart or activate that general modifier.''',
'''Preserve the entire original Player alignment passage, its identical/compatible/opposing categories and advantage/normal/disadvantage wording, including its incompatible and Harmony/Discord terminology. The full exact paragraphs remain in this module's internal source envelope. Do not resolve their meaning through an ordinary scene example.

The deferred questions are finite: the identity and meaning of the named axes; compatibility/opposition; the controlling source/version for any eventual modifier; whether ordinary policy should change; and literal deep-language, currency or faction links. Carry these to the agreed review after the verified GitHub push.

This is a temporary explicit no-automatic-modifier rule, not proof that all characters share an alignment or that all class predicates are now resolved. Apply a source-specific unresolved predicate only to its actual use, and do not invent a compatibility chart to unblock it.''')

section(6, 'Keep one clock and a working channel',
'''Everyone participates on the same fictional clock. A ten-minute negotiation involving four people normally advances ten minutes, provided their actual exchanges fit that time. A person's contribution can occupy that interval without adding another ten minutes to the world.

Declare these new ordinary time references before work:

| Exchange | Actual time |
|---|---|
| Short request and answer | 1 minute |
| Negotiated concession or evidence presentation | 10 minutes |
| Formal complex negotiation/hearing | Its scheduled time; an ordinary disputed Haven hearing is 2 hours |

Simple routine consent can be immediate within real brief communication. These references do not replace a printed Action, casting time, five-exchange limit or other specific procedure. Add time for actual extra exchanges or delays, not for how quickly a player speaks at the table.

In initiative, each creature has at most six seconds of aggregate free ordinary speech/signs per numbered round. Replies, warnings and extra turns share it. Each additional six-second segment requires an available Action on a legal turn or an actual off-turn permission. Communication does not create an interruption, Reaction or additional Action. Use the fulfilled language rules for ten-minute rehearsal of up to six simple cues and each cue's actual hands, sight and distance.

An interpreter first receives a comprehensible message, then conveys it through a channel the next person can receive. A three-second warning followed by a three-second rendition arrives at the second listener at six seconds. A ten-minute original speech plus its rendition needs time for both; relays do not happen instantly. Late information cannot backdate a decision, modifier, consent or saving-throw requirement.

An interpreter does not supply a caster's verbal component, new fluency, a mental link, the meaning of an unknown proper name or proof the message is true. Use each participant's actual language, mode and script knowledge. A closed soundproof compartment cannot receive an oral instruction through a high check.

Deafened does not itself prevent speaking or verbal components. Silenced prevents ordinary deliberate speech and actual verbal components, Chants and command words, while separately legal signs, thoughts or mental effects retain their own rules. An effect ending does not remove another overlapping prohibition. Form-specific limits and exact Oracle/Paladin exceptions remain in force.

Player explanations and accessibility accommodations cost no fictional Action and produce no fictional speech or component.''',
'''Record the source, recipient, channel, language/mode, perception, delivery interval and receipt time for information that matters to a deadline. Concurrent listening can fit one interval; serial relaying must have time. Do not backdate interpretation to the original speaker's start.

Silence the Caster has its own narrow reaction/component window; it is not a universal Silenced condition. Voluntary-silence oath histories follow LAX's distinct windows. A blocked deliberate speaking attempt can still count as a vocal act for that history while failing an audible-component requirement.

Source-specific bounded meaning bridges convey only what the exact effect grants. Tongues III does not gain an invented hearing prerequisite absent from its card, while effects that do require hearing still require it. Speech, received meaning, known language, component performance and truthful knowledge are separate facts.''')

section(7, 'Help with the work; retry when something changes',
'''In initiative, Help uses its actual Action and expires at the helper's next regular start. The contribution must be possible with the helper's real position, channel, tools and information. Social play does not extend the expiry to a convenient later check. The attack-assistance branch still requires a foe within 5 feet and benefits the helped ally's first attack before that deadline.

Outside initiative, this new procedure grants advantage on one check when a helper participates usefully throughout the relevant work interval through its resolution. The helper needs the actual language, access, knowledge or tools their contribution requires. There is no new universal proficiency requirement where ordinary Help has none. Mere presence, payment or ownership of a better tool is not Help.

A helper's time is occupied. They cannot also guard a different room, rest, travel elsewhere or fully help a simultaneous separate negotiation. If an exact long task defines its own trained assistants and numeric cap, use that procedure without adding this general Help benefit. Multiple sources of advantage do not stack; any advantage and any disadvantage cancel to a normal roll under Core.

Resolve one committed approach to the same uncertainty once. Rotating speakers, repeating the sentence or renaming the scene does not grant more attempts. A new offer, authentic new evidence, an audience with different real authority, a changed deadline or a meaningfully different method can create a new uncertainty. Identify that change and declare the new stakes, time and costs before rolling.

Earlier refusal, spent time, payments, consumed evidence and other consequences remain. A source-granted reroll follows its exact cost, timing and new-result rule; it is not permission for unlimited retries.''',
'''Before granting Help, identify what the helper does and reserve their actual interval. In an encounter keep the initiative marker rather than converting it to a whole social scene. A physically separate or uninformed ally cannot contribute merely because they share a roster.

Record why a new approach is different. A letter can matter because it contains new authentic authority or evidence, not because it has a new document ID. Another speaker alone does not erase an earlier approach. Resolve a new feasible proposal on its own terms without secretly refunding earlier costs.

Shattered Mind Boon IV's failed INT/WIS reroll remains its actual acquired feature with its own restrictions. It does not authorize a CHA retry, another scene cap, an unspent resource refund or a replacement of an already closed event.''')

section(8, 'Apply the exact magical effect',
'''Charmed is a relationship to an identified charmer. It prevents choices the affected creature knows would willingly harm that charmer and gives that charmer advantage on social ability checks against it. It does not compel affection, obedience, belief, allegiance, surrender, protection, self-harm, consent, ownership or truthful speech. Unexpected collateral harm is not retroactively a willing violation.

Frightened gives disadvantage on checks and attacks while the creature can see its fear source. Its restriction against willingly moving closer to that source continues while the condition lasts, even when the visibility-based disadvantage no longer applies. Forced movement is not willing approach. Successful ordinary Intimidation grants only its declared concession and does not automatically apply this condition.

Use the complete procedure of an effect the character has legitimately acquired and can currently use. Pay its activation and resources, check range and target eligibility, apply its actual save, resistance/immunity, concentration, duration, awareness and ending rules. A social check cannot replace a spell save or recreate a resisted payload. An immunity to charm or a named control effect does not by itself prevent ordinary persuasion.

No general language requirement is added where an effect has none; printed hearing, sight and component requirements still apply. A feature that offers refusal or backlash keeps that choice. A title or a familiar spell name does not grant an unavailable effect or merge ordinary, class, innate and recipe versions.

Knowledge features reveal only information supported by their exact source and subject. Unknown remains possible. They do not establish ownership, invent a buyer or route, supply an absent cure or resolve deferred cosmology.''',
'''Retain the complete actual sources alongside these interface limits. These are reminders for applying acquired features, not replacement cards or new selections:

| Interface | Keep its exact boundary |
|---|---|
| Oracle Tongues I | Receptive spoken-mortal comprehension and the bonus for actually hearing eligible allies; no universal fluency/literacy |
| Tongues III / IV / V | III's yes/no/unknown and player refusal; IV's genuine meaningful-exchange time and targets; V's command, hearing, save, restrictions and success-damage branch |
| Tongues overlapping voices | Its exact social −2 and Action suppression for ten minutes when the source conditions apply |
| Heaven's Decree / Sovereign's Ascendance | The target retains obey-in-the-safest-way **or** backlash; no forced confession, belief or allegiance |
| Aura of Authority | Obstructing a lie neither forces truthful speech nor supplies translation |
| False Life | Its Insight intervention is the particular healing gate, not general social suspicion or a universal restriction on care |
| Paladin Wave | The later fulfilled long-rest amendment remains controlling |
| Mage/Wizard Arcane Insight, Cleric Divine Insight, Oracle knowledge/omen/scout features | Their bounded supported subject, exact costs and possible unknown result |
| Ranger Pathfinder's Mark / Swift Traverse | A bearing is not a clear route or teleport; paid tactical Dash does not double a travel day |
| Ranger quiet footsteps | No automatic silence for companions, gear or speech, and no blanket removal of tracking |
| Soldier Quick Deploy | Its limited cover does not become transferable camp lumber or a palisade |
| Druid forms | Own body history and actual limited movement/attacks; no permanent resources manufactured by transforming |
| Thief Feint | Its literal passive-Insight combat procedure, not a negotiation |
| Warrior Intimidation / morale hooks | Actual source windows; a morale penalty is not automatically Pressure, a save modifier or an Escape/Pursuit penalty |
| Tinker, AEX and haulers | Distinct commands, one-command budgets, servicing and repairs; TEX Efficient Recycling retains its no-enemy-cause rule; the 43 crafted devices gain no invented deployment RP cost |

The internal envelope preserves all seventeen complete class datasets, 1,223 cards and the 94 selected comparison records with their existing statuses. Comparing a card does not activate it. The ordinary authored index remains 412 reviewed and 436 pending; the 136 standalone procedures retain their complete operational records rather than a lossy legacy conversion. Pending spells and feats are not enabled by this chapter.

A secret meaning, unavailable active spell or missing world record restricts only the particular use needing it. It is not permission to invent the missing feature or reopen every source decision.''')

section(9, 'Record agreements and respect table choices',
'''Record an agreement's actual parties and authority, property or service, deliverable, consideration, time, communication, witnesses and remedies. A clerk's promise of supervised access is not a transfer of the employer's ledger. A guard's key does not authorize selling the absent owner's property. Later breach is a new event; it does not change the earlier die result.

The Session Zero agreement governs player consent and table boundaries. A skill check cannot assign a player's belief, require acting, override agreed PvP limits or grant their willingness to an effect that requires it. A player can pause, skip or request an accessible way to participate without explaining personal circumstances or receiving a character penalty. Apply any explicit magical control procedure with its own actual agency and refusal limits.

Accepting a costly alternative requires the real payer's choice and funds. Failure alone does not deduct the payment. An unavailable object, absent person or forged receipt cannot provide missing performance.

Consent to an audience or carriage does not imply consent to spellcasting, surgery, restraint, property transfer, dangerous labor or disclosure of protected history. Establish each relevant permission when that operation needs it. A later agreement cannot retroactively supply a missing action prerequisite or turn counterfeit provenance into genuine evidence.''',
'''Keep practical table agreements in the shared Session Zero record. Do not put personal reasons for boundaries or accommodations in a fictional ledger. The ordinary scene record stores only the relevant permission and its scope.

An NPC may face fictional pressure while still having the stated limits and actual powers of that NPC. Winning a feasible concession does not create a legal power to perform a different one. Keep an offered agreement, accepted agreement and completed performance as separate states.

An effect's willing-target predicate must be satisfied as that source requires at the required time. A social success, admission to a meeting or ride in a cart cannot be reused as blanket consent for unrelated procedures.''')

section(10, 'Let consequences reach the people who react',
'''Standing changes follow significant attributable acts and a real way for the institution to learn about them. Record what happened, who acted, witnesses or documents, what each recipient actually learned, and when. A privately rescued person's relationship may change before any institution hears the story.

Public means exposed or documented to a relevant audience; it does not mean every faction instantly knows. One deed reported five times remains one underlying cause for that institution. Different institutions can react differently when their interests and information actually differ.

Separate established facts from reports and beliefs. An institution can act on a lie it believes; that belief does not rewrite the historical event. A later correction creates a new evidence/response record, not silent erasure or an automatic equal-and-opposite score change.

For ordinary standing, start from the subject's score at the opening of that institution/scene record. Sum the signed proposed changes from distinct eligible events, limit that sum to −2 through +2, then apply the −3 through +3 scale. Keep proposed change, applied change and any overflow. Overflow is historical information, not future credit. Recompute from the scene opening as additional events arrive; do not saturate each event separately and lose an offsetting change.

A successful social check does not automatically award standing, renown or a license. A genuinely performed, attributable public outcome can support the declared event. Existing titles, access, obligations and privileges remain separate records with their own terms. Delayed notice cannot backdate permission to an earlier purchase.''',
'''Link each receiving institution's reaction to the originating act and its actual receipt event. Repeated messengers can strengthen knowledge without manufacturing additional underlying deeds. Separate an individual's relationship from their institution's standing.

For a scene opening at +2, a proposed +2 yields +3 after the scale cap: applied +1, overflow +1. A distinct −2 proposal in that same scene makes the algebraic proposed sum zero, so recomputation from opening +2 returns +2. The earlier overflow cannot be spent in another scene.

Do not compensate a failed persuasion roll with invented reputation. A independently meaningful witnessed good deed can still matter, but needs its own established significance and attribution. Unknown institutional goals or a shared registry label do not justify a universal allied/enemy reaction. Preserve raw source versions and earned history under the reputation contract.''')

section(11, 'Faction activity takes real work',
'''Other groups act on the campaign clock using the people, resources and information they actually possess. Their work can continue while your expedition is away.

After a genuine expedition return, the Director reviews up to three watched factions and one eligible action for each. A return closes a real episode with an objective and outcome, including abandonment or extraction. Repeatedly crossing the boundary during the same return does not create more activity. A split party's arrivals stay linked to their actual episode.

The new regular review also occurs at each completed campaign 24-hour boundary. A return at exactly the same time and that scheduled review form one checkpoint. A checkpoint records and reports work; it does not itself advance the world by 24 hours or give free labor, goods, recruits or success.

| Action | Actual ordinary work when no more specific procedure applies |
|---|---|
| Recruit | 8 active staff hours seeking/interviewing one available candidate |
| Denounce | 1 active hour preparing/delivering one attributable statement to an actual audience |
| Buy | 1 active hour arranging/executing an available bill with real goods, funds and authority |
| Raid | Actual preparation, route, encounter and resolution |
| Research | The particular research process; a generic original-evidence question requires 8 active hours and its declared knowledge task |
| Fortify | Actual construction under the camp procedure |
| Bargain | 1 active hour of concrete negotiation |
| Conceal | 8 active hours working on finite evidence, an asset or a route |
| Wait | The actual interval and status, with no automatic money, healing or knowledge |

Specific procedures keep their actual duration and costs, even when shorter. Do not add a second free faction outcome to them. An ongoing project keeps its identity and accumulated work. A return cannot replace it with an instantly completed action.

When real work finishes between checkpoints, its consequences occur then. A later report acknowledges them once. People who witness the result can react immediately without waiting for the administrative review. News still needs a real messenger, rumor, changed offer, guard presence or other observable event to reach you.''',
'''Before resolving a checkpoint, nominate at most three distinct watched factions. Do not swap in a fourth mid-checkpoint for another slot. The next watch list can change, but no new name creates retroactive staff or work. Keep the canonical day origin from the expedition clock; do not restart a 24-hour timer on each arrival.

For each action record: persistent action/objective IDs; named responsible actors; starting knowledge and its source; location, route and access; actual tools, materials, money and permissions; committed staff intervals; positive duration; the governing resolution rule; success/failure consequences; and completion prerequisites. An in-progress action continues under its existing ID. A checkpoint acknowledges actual work, not a transferable Action token.

Routine feasible, uncontested work needs no invented roll. Contested or dangerous work uses the actual social, task, route or encounter procedure. A raid does not resolve an absent battle with one generic die. Research cannot ignore its actual formula, language, subject or evidence requirements. Concealment can hide finite evidence or access without deleting true history.

One actor cannot work two incompatible fronts or treat someone while claiming the same time as rest. Independent staff can work in parallel only if really assigned and supplied. A faction's advertised backer is not unlimited funds or secret intelligence.

Keep completion time separate from report time and mark each result as reported once. Publish only information the actual audience can receive. A private project can have a visible consequence without revealing its whole plan or dossier. These procedures are authored Director tools; they do not claim that companion software simulates offscreen behavior.''')

section(12, 'Rival objectives leave a history',
'''Rival groups have bounded goals, strengths, weaknesses and information. They travel real routes, need support, and can offer useful cooperation as well as opposition. Their successes can change the situation without erasing your expedition's choices.

The Director tracks four kinds of objective clock:

| Clock | Length fixed when opened | Qualifying progress |
|---|---:|---|
| Depth | 4–8 | Actual travel or support that materially advances its named route objective |
| Claim | 4 | Genuinely obtained relevant proof, witnesses or legal support |
| Grudge | 4 | Attributable humiliation, loss, betrayal or public accusation actually learned by the rival |
| Collapse | 4–6 | Actual casualty, debt, internal conflict or exposure materially advancing the named crisis |

One distinct qualifying event advances that clock by one segment. Several labels for the same deed or repeated reports do not add segments. A knowledge-dependent trigger qualifies when the rival first credibly receives it, not when an unknown event happens elsewhere. One event can affect different clocks only through independently real consequences.

The Director declares the finite completion consequence and its prerequisites when opening the clock. Reaching its threshold resolves it once only when those prerequisites exist. Otherwise it remains at its threshold with the specific missing requirement recorded. A clock does not teleport travelers, authenticate a false witness, create title or grant an extra attack.

An objective already actually completed needs no meaningless extra ticks. A resolved objective keeps its event history; a new clock needs a distinct objective or crisis. A genuine reversal is another recorded event, not erasure or an automatic refund. Players learn only the rival identity, events and consequences their characters can actually know.''',
'''Keep every field in the original rival sheet:

| Source field | Record |
|---|---|
| Public identity | Name and identity available to the stated audience |
| Backer | Actual patron/source of support, with its knowledge boundary |
| Current depth | Actual position in the relevant route |
| Primary objective | The specific goal being pursued |
| Preferred method | The means the group tends to use |
| Professed limit | The line they claim they will not cross |
| Need from the party | A concrete potential exchange or dependency |
| Feared disclosure | What they fear the party will learn; keep private until actually learned |
| Current relationship | The source-qualified relationship and relevant history |

Add, rather than replace these fields with, actor IDs, real assets, location/route, known information and its source, resources/obligations, ongoing action IDs and audience permissions. Give the rival a practical strength and weakness. Do not use it as an omniscient counter to player plans. A generic standing category among the 44 source records is not a fully staffed expedition. New campaign institution IDs require the reputation binding, not a history invented from their names.

For every clock retain its objective ID, chosen length, trigger, starting time, all qualifying event IDs and receipt times, current segments, finite consequence, prerequisites and actual resolution. A Depth threshold cannot bypass an impassable route. A Claim threshold cannot replace authentic proof or an authorized hearing. Grudge schedules its real hostile action; it grants no immediate extra attack. Collapse can cause the declared real withdrawal, fracture or desperate bargain without deleting actors or property.

When a threshold is blocked, state the actual missing prerequisite and retain the clock's history. A new genuine event can supply it; repeated reports cannot. A real reversal can change the current objective through a new event, but negative progress does not erase an earlier deed or refund resources.

All 24 original social proposal scenarios and GPT's individual final dispositions are preserved in this module. They are source-bound examples, not evidence of actual campaign events or software execution. Keep private backer and feared-disclosure fields out of the public projection.''')

CASES = []
def case(n, q, given, expected):
    CASES.append({'id': f'EX04-{n:02d}', 'questions': q, 'given': given, 'expected': expected,
                  'evidenceClass': 'Authored synthetic expected outcome; not executed gameplay'})
case(1, ['SO-01'], 'An authorized clerk willingly offers a routine viewing appointment.', 'No roll is needed. Record the appointment and actual viewing time; no extra benefit appears from asking to roll.')
case(2, ['SO-01'], 'A guard has the warehouse key but no authority to sell its stock.', 'Explain the missing authority before a sale check. Access to a key does not make the sale feasible.')
case(3, ['SO-01','SO-02'], 'A promised DC13 concession is met with final total13 and no natural degree change.', 'Grant the announced success; no hidden DC23, additional fee or second defensive check.')
case(4, ['SO-02'], 'A fixed task has DC13, total3 and natural1.', 'It is Critical Failure at the margin and remains at that bounded degree after the shift. Apply only its declared consequence.')
case(5, ['SO-02'], 'A possible fixed task has DC35, natural20 and final total20.', 'The margin starts at Critical Failure; natural20 improves it to Failure. It does not compel obedience.')
case(6, ['SO-02'], 'A deception and actual scrutiny both total17; the initiating die is natural20.', 'The opposed tie preserves the prior state. No task degree shift changes the total or adds an opposed critical outcome.')
case(7, ['SO-03'], 'An actual CHA/Reputation appeal has CHA+2, applicable PB+2 and known standing+2.', 'The eligible ordinary modifier is+4, not+6. Recognized standing is evidence for the approach, not another numeric bonus.')
case(8, ['SO-03'], 'A successful Insight test observes hesitation but the private letter is inaccessible.', 'Give the predeclared supported inference. Do not reveal the letter or claim certainty that the available evidence cannot support.')
case(9, ['SO-03'], 'A Performance succeeds at entertaining an actual audience.', 'Deliver the audience response. A separate property transfer or permit still needs actual authority and its own feasible approach.')
case(10, ['SO-04'], 'One old save says companion-score-v1+2; another says Loop eleven-band+2.', 'Preserve both raw scores and versions. The first is+2/Honored; an explicitly accepted Loop mapping derives+1/Liked, retaining its historical Favored meaning and earned privileges.')
case(11, ['SO-04'], 'A saved faction key is absent while another is explicitly numeric zero.', 'Keep those distinct. Only the real zero is a recorded neutral score; do not fabricate an absent entry.')
case(12, ['SO-04'], 'A current+3/Honored actor displays only the label Honored.', 'The underlying current score stays+3. It is not normalized to+2 or added to the social die.')
case(13, ['SO-05'], 'Two negotiators publicly share a civic goal.', 'That communicated goal can be leverage. It establishes no cosmic alignment identity and adds no automatic advantage.')
case(14, ['SO-05'], 'An older paragraph lists alignment compatibility bonuses with unresolved meanings.', 'Retain the complete paragraph as a receipt; use the explicit no-automatic-alignment-modifier rule in this ordinary chapter.')
case(15, ['SO-05'], 'One acquired oath use depends on an undefined deep predicate.', 'Record that particular dependency without inventing its meaning or blocking unrelated ordinary trade and conversation.')
case(16, ['SO-06'], 'Four participants conduct an exchange whose complete interpretation fits ten minutes.', 'Advance the shared clock600seconds, not2400. Each actual participant interval is still occupied.')
case(17, ['SO-06'], 'A3-second warning is followed by a3-second rendition.', 'The final listener receives it at6seconds. It cannot affect a decision already resolved at4seconds.')
case(18, ['SO-06'], 'A creature uses4seconds of free speech, then has an extra turn in the same numbered round.', 'Only2seconds of the six-second free allowance remain. Further six-second segments need actual available Actions/permissions.')
case(19, ['SO-07'], 'The helper’s next regular start passes before the relevant check.', 'The initiative Help expires. A later social check cannot retain it merely because the conversation continues.')
case(20, ['SO-07'], 'One helper is requested for two simultaneous ten-minute negotiations in separate rooms.', 'They cannot qualify for both full intervals. Schedule separate work or use another actual helper.')
case(21, ['SO-07'], 'Five party members repeat the same refused appeal; afterward an authentic new authority letter arrives.', 'The repeated unchanged appeals create no retries. The new letter may justify a distinct feasible approach with new declared time/stakes.')
case(22, ['SO-08'], 'A Charmed clerk still lacks authority to surrender the employer’s archive.', 'Charm can supply its actual social advantage only for a possible check. It does not create authority or obedience.')
case(23, ['SO-08'], 'A Frightened creature loses sight of its still-active fear source.', 'Its visibility-dependent disadvantage ceases. It still cannot willingly move closer while Frightened.')
case(24, ['SO-08'], 'A target resists an actual magical control payload.', 'A social roll cannot recreate that payload. An independently feasible ordinary request retains its ordinary limits.')
case(25, ['SO-09'], 'A failed check offers a predeclared feasible1gp alternative; the player declines.', 'Keep the failed result and refusal. Do not deduct the100cp or invent a debt.')
case(26, ['SO-09'], 'A player agreed to a character’s carriage but not to surgery.', 'The ride does not satisfy surgery’s actual permission. Establish the separate predicate when needed.')
case(27, ['SO-09'], 'A player invokes the agreed pause signal during a coercion scene.', 'Pause/revise under Session Zero with no fictional punishment or demand for a personal explanation.')
case(28, ['SO-10'], 'An institution/scene opens at+2 and receives a distinct ordinary+2 proposal.', 'End at+3 with applied+1 and overflow+1. Replaying the same underlying event changes nothing; overflow cannot be banked.')
case(29, ['SO-10'], 'The same scene later also has an independent qualifying−2 proposal.', 'Recompute signed+2−2 from opening+2. The resulting score is+2, not+1 from sequential saturation.')
case(30, ['SO-10'], 'A private rescue reaches a relevant institution by messenger at noon.', 'The institution cannot act on it at11:00. Record actual receipt, attribution and that institution’s own response; other groups do not automatically learn it.')
case(31, ['SO-11'], 'A genuine return occurs at the campaign’s completed24-hour boundary.', 'Coalesce the two reasons into one checkpoint, with at most three preselected watched factions and one eligible action each.')
case(32, ['SO-11'], 'An eight-hour recruitment project has completed two hours when the party briefly recrosses Haven’s boundary.', 'Six active hours remain. The crossing grants neither a new episode checkpoint nor a completed substitute recruit.')
case(33, ['SO-11'], 'A funded project actually finishes at08:00; its messenger arrives09:00; the checkpoint is24:00.', 'The consequence exists at08:00, recipients learn it at09:00, and the checkpoint acknowledges the same completion once without recreating it.')
case(34, ['SO-12'], 'A Claim clock at2/4 receives one genuinely new qualifying document and three reports of it.', 'Advance to3/4 once. Preserve the reports as information history, not three more segments.')
case(35, ['SO-12'], 'A Depth clock reaches its declared threshold while the required route remains impassable.', 'Retain threshold reached and the actual missing passage prerequisite. Do not teleport the rival or roll an invented completion check.')
case(36, ['SO-12'], 'A Grudge clock reaches4/4 with a declared future ambush response.', 'Schedule that real action with actors, resources and travel. It does not grant an immediate attack or resolve the encounter.')

def render(env, audience):
    lines = [f'# {audience.title()} expedition procedures — social scenes and faction activity', '', env['notice'], '',
             'Use with [Core resolution](../CORE_RESOLUTION_PLAYTEST.md), [language and communication](../LANGUAGE_COMMUNICATION_PLAYTEST.md), [Haven and standing](EXPEDITION_PART03_PLAYER.md), and [Session Zero](../../playtest/SESSION_ZERO_PLAYTEST.md).', '']
    if audience == 'director': lines += ['Read the complete [player social chapter](EXPEDITION_PART04_PLAYER.md) alongside this chapter.', '']
    for s in env['sections']: lines += ['## ' + s['title'], '', s['text'], '']
    if audience == 'director':
        lines += ['## Recording a social scene', '',
                  'Record scene ID and approach history; Want/Leverage/Limit/Clock/Witness; decision authority; source and received communication; declared stakes and optional offer; fixed/opposed/specific procedure and modifiers; participant intervals; Help and expiry; actual result; acceptance and payment; delivery/obligation; and the genuine change permitting any retry.', '',
                  '## Recording faction activity', '',
                  'Record the actual institution and source binding, all nine rival fields, audience permissions, named actors/resources/information, unique action and objective, work intervals and governing procedure, fixed checkpoint/watch list, clock events/prerequisites, actual completion and later report. The complete EC-11/EC-13 contracts are preserved in the internal envelope.', '',
                  '## Authored boundary examples', '', 'These examples are stated synthetic expectations, not runtime or human-playtest results.', '']
        for c in env['workedCases']: lines += ['### ' + c['id'], '', c['given'], '', c['expected'], '']
        lines += ['## Original proposal scenarios and final dispositions', '', 'All 24 original scenarios remain intact, with their source decision applied individually.', '']
        for c in env['originalProposalScenarios']:
            lines += ['### ' + c['id'] + ' — ' + c['sourceQuestion'], '', c['originalScenario'], '', '**Final expected outcome:** ' + c['finalExpected'], '']
    return '\n'.join(lines)

def main():
    paths = {'public': R/'data/public/expedition_candidate/part04.json', 'internal': R/'data/director/expedition_candidate/part04.json',
             'player': R/'docs/mechanics/expedition/EXPEDITION_PART04_PLAYER.md', 'director': R/'docs/mechanics/expedition/EXPEDITION_PART04_DIRECTOR.md',
             'receipt': A/'EX58_CANDIDATE_PART04_CHECK.json'}
    assert not any(p.exists() for p in paths.values()), 'Preserve previous outputs before revision'
    checks = []
    def ck(n, v):
        checks.append({'name': n, 'pass': bool(v)})
        assert v, n
    original_manifest = read(P/'FILE_MANIFEST.json')
    for x in original_manifest['files']: ck('Original verdict preserved: '+x['path'], info(P/x['path']) == {k:x[k] for k in ['bytes','sha256']})
    for correction in ['EX58_EDIT_01_FULFILLMENT.json','EX58_EDIT_02_FULFILLMENT.json']:
        for rel, expected in read(A/correction)['descendants'].items(): ck('Confirmed correction descendant: '+rel, info(G/rel) == expected)
    directions = read(R/'data/director/expedition_candidate/source_register_corrected.json')['directions']
    original_directions = read(P/'EX58_AUTHORING_REGISTER.json')['directions']
    by = {d['id']: d for d in directions}; original_by = {d['id']:d for d in original_directions}
    ids = [s['id'] for s in SECTIONS]
    ck('All twelve social directions in order', ids == [f'SO-{i:02d}' for i in range(1,13)])
    prior = read(R/'data/director/expedition_candidate/part03.json')['cumulativeAuthoredQuestionIds']
    ck('All 26 prior expedition directions', prior == [f'FL-{i:02d}' for i in range(1,27)])
    for q in ids: ck('Social direction unchanged by scoped amendments '+q, by[q] == original_by[q])
    preparation = read(A/'SOCIAL_FACTION_SOURCE_PREPARATION.json')
    class_comparisons = read(P/'EX58_CLASS_INTERFACE_DISPOSITIONS.json')
    full_classes = []
    for c in class_comparisons['classFiles']:
        p = G/c['path']; ck('Complete class dataset unchanged '+c['path'], info(p)['sha256'] == c['fileSha256'])
        full_classes.append({'path':c['path'], **info(p), 'completeEnvelope':read(p)})
    ck('Seventeen class collections retained', len(full_classes) == 17)
    ck('1223 comparison card count unchanged', sum(c['cardCount'] for c in class_comparisons['classFiles']) == 1223)
    ck('94 selected full card records retained', sum(len(c['selectedFullCards']) for c in class_comparisons['classFiles']) == 94)
    names = ['CORE_RESOLUTION_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md',
             'LANGUAGE_COMMUNICATION_PLAYTEST.md','LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md','SPELL_INTEGRATION_RULES.md',
             'CREATURE_LIFECYCLE_PLAYTEST.md','REPUTATION.md','CLASS_PLAYTEST_RULES.md','CRAFTING_HARVEST_PLAYTEST.md','GAMEPLAY_LOOP_CANON.md']
    sources = [R/'docs/mechanics'/n for n in names] + [R/'docs/playtest/SESSION_ZERO_PLAYTEST.md',R/'data/playtest/character_foundation.json']
    full_sources = []
    for p in sources:
        ck('Full governing source available '+p.name, p.is_file())
        full_sources.append({'path':p.relative_to(G).as_posix(),**info(p),'completeText':p.read_text('utf-8-sig')})
    source_blocks = preparation['selectedSourceBlocks']
    for d in preparation['sourceDocuments']:
        ck('Original social source book unchanged '+d['file'], info(G/d['file']) == {k:d[k] for k in ['bytes','sha256']})
    original_scenarios = read(P/'EX58_WORKED_SEQUENCES.json')['originalProposalScenarios']
    ck('All 24 original social scenarios retained', len(original_scenarios) == 24)
    ck('Original scenarios cover each social direction twice', all(sum(s['sourceQuestion']==q for s in original_scenarios)==2 for q in ids))
    public = {'schemaVersion':1,'moduleId':'EX58-PART04','status':'authored-partial-candidate-awaiting-exact-review',
              'notice':'Working chapter module 4, authored from the agreed source decisions. Complete expedition assembly and exact candidate review remain open.',
              'questionIds':ids,'completeExpeditionCandidate':False,'selectionEnabled':False,
              'sections':[{'id':s['id'],'title':s['title'],'text':s['player']} for s in SECTIONS]}
    director = {'notice':public['notice'],'sections':[{'id':s['id'],'title':s['title'],'text':s['director']} for s in SECTIONS],
                'workedCases':CASES,'originalProposalScenarios':original_scenarios}
    contracts = read(R/'data/director/expedition_candidate/source_contracts_corrected.json')['contracts']
    internal = {'schemaVersion':1,'moduleId':public['moduleId'],'status':public['status'],'sourceReview':'EX58-SOURCE-2026-10-11',
                'completeExpeditionCandidate':False,'authoredQuestionIds':ids,'cumulativeAuthoredQuestionIds':prior+ids,
                'remainingSourceDirections':[d['id'] for d in directions if d['id'] not in prior+ids],
                'publicEnvelope':public,'directorModule':director,'completeOriginalDirections':[original_by[q] for q in ids],
                'completeCurrentDirections':[by[q] for q in ids],
                'completeCurrentContracts':[c for c in contracts if c['id'] in ['EC-02','EC-11','EC-12','EC-13','EC-15']],
                'fullGoverningSources':full_sources,'completeSelectedSourceBlocks':source_blocks,'sourceDocuments':preparation['sourceDocuments'],
                'completeClassInterfaceDisposition':class_comparisons,'completeClassDatasetEnvelopes':full_classes,
                'audienceBoundary':'Public chapter includes general current procedures, not private institution dossiers, source alignment receipts, backers, feared disclosures or unknown saved keys.',
                'semanticCoverageNote':'Authored prose against all twelve complete directions, exact source blocks and governing procedures. Checks cover preservation, representation parity and bounded reference cases; no claim of complete game balance or software implementation.',
                'newPromotions':0,'runtimeImplemented':False,'examplesAreRuntimeTests':False}
    ck('All social directions have three authored boundary examples', all(sum(q in c['questions'] for c in CASES)>=3 for q in ids))
    for rel, expected in read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
        if rel != 'README_EXPEDITION_INTEGRATED_V3.md': ck('Original submission current file preserved: '+rel, info(G/rel) == expected)
    # Bounded reference examples; this is not an implementation of social scenes.
    def degree(total, dc, natural):
        base = 3 if total>=dc+10 else 2 if total>=dc else 0 if total<=dc-10 else 1
        return max(0,min(3,base+(1 if natural==20 else -1 if natural==1 else 0)))
    for label, actual, expected in [
        ('meet promised DC',degree(13,13,9),2),('ten above DC',degree(23,13,19),3),
        ('exact minus-ten margin',degree(3,13,3),0),('one below DC',degree(12,13,8),1),
        ('natural20 can still fail',degree(20,35,20),1),('natural1 sufficiently high total',degree(23,13,1),2),
        ('natural1 lower bound',degree(3,13,1),0),('natural20 upper bound',degree(25,13,20),3),
        ('ordinary Reputation modifier',2+2,4),('one shared scene',10*60,600),('serial interpretation',3+3,6),
        ('free round speech remaining',6-4,2),('declined alternative debit',500-0,500),('accepted alternative debit',500-100,400),
        ('standing upper cap',min(3,2+min(2,2)),3),('standing actual applied',3-2,1),('unbanked overflow',2-(3-2),1),
        ('standing signed recomputation',max(-3,min(3,2+max(-2,min(2,2-2)))),2),
        ('day seconds',24*60*60,86400),('remaining staff hours',8-2,6),('eight active hours',8*3600,28800),
        ('one event despite three reports',2+len({'document-a','document-a','document-a'}),3),
        ('unique simultaneous checkpoint',len({86400,86400}),1),('at most three distinct watches',len({'a','b','c'}),3),
    ]: ck('Bounded reference: '+label, actual==expected)
    save(paths['public'],public);save(paths['internal'],internal)
    for audience,env in [('player',public),('director',director)]:
        paths[audience].parent.mkdir(parents=True,exist_ok=True)
        paths[audience].write_text(render(env,audience),encoding='utf-8',newline='\n')
    ck('Complete public envelope equals internal projection',read(paths['public'])==read(paths['internal'])['publicEnvelope'])
    ck('Complete player chapter parity',paths['player'].read_text('utf-8')==render(read(paths['public']),'player'))
    ck('Complete Director chapter parity',paths['director'].read_text('utf-8')==render(read(paths['internal'])['directorModule'],'director'))
    ck('Original proposal scenarios reproduced without loss',read(paths['internal'])['directorModule']['originalProposalScenarios']==original_scenarios)
    ck('Full original social source blocks preserved',read(paths['internal'])['completeSelectedSourceBlocks']==source_blocks)
    links=[]
    for audience in ['player','director']:
        for target in re.findall(r'\]\(([^)]+)\)',paths[audience].read_text('utf-8')):
            ck('Real local link '+target,(paths[audience].parent/target).resolve().is_file());links.append(target)
    for x in original_manifest['files']:ck('Original verdict unchanged after authoring '+x['path'],info(P/x['path'])=={k:x[k] for k in ['bytes','sha256']})
    receipt={'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'moduleId':public['moduleId'],
             'status':'All 12 social directions drafted; 38 of 58 directions authored across four modules. Complete exact candidate remains incomplete and unreviewed.',
             'questionIds':ids,'cumulativeQuestionIds':prior+ids,'remainingDirections':len(internal['remainingSourceDirections']),
             'workedCases':len(CASES),'originalProposalScenariosPreserved':24,'referenceChecks':24,'fullClassDatasetsPreserved':17,'fullClassCardsPreserved':1223,'selectedClassRecordsPreserved':94,
             'localLinkChecks':len(links),'checks':len(checks),'failures':[c for c in checks if not c['pass']],
             'outputs':{p.relative_to(G).as_posix():info(p) for k,p in paths.items() if k!='receipt'},
             'builder':{'path':Path(__file__).resolve().relative_to(G).as_posix(),**info(Path(__file__))},
             'scope':'Source/book/class preservation, full public/Director representation parity, local links and finite arithmetic/degree examples. No real social-scene execution, faction simulation, save migration or human balance.',
             'runtimeTestsExecuted':0,'newPromotions':0,'realSavesReadOrWritten':0,'sourceInformationDeleted':0,'details':checks}
    save(paths['receipt'],receipt)
    print(json.dumps({k:receipt[k] for k in ['moduleId','remainingDirections','workedCases','checks','failures','outputs']},indent=2))

if __name__ == '__main__': main()
