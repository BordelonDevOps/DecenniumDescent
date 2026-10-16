# Epilogue Character Interfaces — Player Rules
**Status:** NEW PROVISIONAL AUTHORSHIP for EPI-01 through EPI-07. This module does not select a campaign epoch, approve EPI-08–17, or change spell/class status.

## 1. Home Affiliation, Inspiration, and Disquiet
Choose one philosophical home affiliation at character creation or module adoption. It does not change ancestry, birthplace, languages, resistances, travel, or factual planar knowledge.

- **Bastion of Flame:** disciplined passion tempered before it becomes destructive.
- **Veiled Expanse:** privacy and secrecy yield when honest motion and engagement are necessary.
- **Radiant Currents:** law is responsive to perspective and must remain fluid enough to meet reality.
- **Boundless Void:** questions puncture complacency; uncertainty should be examined rather than hidden.

At the end of a beneficial Long Rest, if your established location is away from your chosen realm, examine the preceding 24 elapsed hours. Only qualifying aligned choices: gain one Epilogue Inspiration die. Only knowingly contrary qualifying choices: gain one Disquiet. If both occurred, gain neither. No relevant choice, or genuinely unknown location: neither.

**Epilogue Inspiration:** d6; capacity two slots. Spend one before one eligible ability check and add it to the total. Never attack rolls or saving throws. At most one per check and never on the same check as a Conflict Die. Spending changes a ready slot to spent-recoverable. A normal gain restores a spent slot first; otherwise it creates a ready slot only if fewer than two total slots exist.

**Disquiet:** at most one pending d6. On your next ability check before its 24-hour expiry, subtract 1d6 after other numeric modifiers and before degree comparison. It is consumed by that check. While Disquiet affects that check you cannot spend Epilogue Inspiration or Conflict Die.

## 2. Seven Choir Motifs
The Expedition begins this module with one finite Seven-Motif Folio. Learning one motif requires one uninterrupted hour from the folio, a faithful copy, or the onboarding Witness, and proficiency with the instrument used or an applicable Performance skill.

The Expedition has one shared motif allowance. It begins at one. A qualifying beneficial Long Rest can refresh it to one only if at least 24 elapsed hours passed since the last refresh. Splitting, renaming, adding members, or later re-merging does not create a second pool; split descendants retain the same ledger history. Independent Expeditions that truly existed separately when the module was adopted begin with their own ledgers until they merge.

### Ordinary motif activation
Except **Law**, motif activation is outside an encounter:
1. At start, preflight the motif, performer, fixed candidate listeners, 30-foot range/hearing, effect, work order if relevant, and shared allowance.
2. Perform audibly for **60 uninterrupted seconds**.
3. At completion remove any candidate who was not willing, within 30 feet, and able to hear throughout. Recheck legality.
4. Only a valid completed performance commits. Spend the shared allowance immediately before resolving effects.
5. Interruption before completion spends elapsed time but **no allowance**.

**Motif save DC:** `8 + activating performer's proficiency bonus + Charisma modifier`, used only where that motif calls for a save. Saves are binary.

- **Courage:** each legal listener may change one spent-recoverable Epilogue Inspiration slot to ready. It never creates a first never-earned slot and does not restore class engines.
- **Balance:** one willing listener swaps one legal prepared/loadout option they already own. Druids may swap one prepared ordinary druid spell or one unlocked Arch attunement among **Dire Wolf, Earth Warden (Dire Bear), Sky Serpent**; changing Arch attunement does not activate a form or clear Refrain. Wizards may swap one ordinary prepared matrix for a legal spell already in their accessible spellbook; the replacement receives no transferred Matrix Mastery modification, and any link using the removed matrix becomes inactive while history remains. Already-cast spells continue under their own rules; removed Stability Reinforcement stops supplying its +2 bonus. Warriors may swap one legal equipped mutation; Flesh Warden removal reduces max HP and clamps current HP to the new max, and re-equipping capacity never heals.
- **Law:** combat exception, one Action. Choose one revealed hostile creature within 30 feet that can hear you and willing protected listeners within 30 feet who can hear, including yourself if desired. After legal preflight, spend allowance before denial/immunity/save. On failed Wisdom save, for one round the target cannot voluntarily attack, use hostile targeted abilities against, or deliberately include a protected listener in a hostile area effect. A protected listener directly attacking the target, hit or miss, or deliberately including it in a hostile area effect ends Law immediately before that hostile effect resolves.
- **Sorrow:** each listener gains one pending reroll for 24 elapsed hours. After that listener fails a Wisdom saving throw, but before the failed consequence commits, they may consume Sorrow and reroll with the same procedure/modifiers; the reroll replaces the original even if worse. One pending Sorrow maximum; another grant neither stacks nor extends expiry.
- **Pattern:** one pending 24-hour benefit: advantage on the next ability check whose primary purpose is study, research, deciphering, analysis, or recall.
- **Contradiction:** one pending 24-hour benefit: advantage on the next Wisdom (Insight) check to discover hidden motive/internal inconsistency. It is not truth detection.
- **Transition:** at preflight fix one existing workOrderId, task, materials/prerequisites, mandatory worker roles and up to four named beneficiaries. At valid completion, each beneficiary's eligible remaining active work is reduced after exact source time modifiers. For remaining minutes `r >= 1`, new remaining time is `min(r, max(1, ceil(r/2)))`; positive sub-minute remainder is unchanged; zero remains zero. A beneficiary must begin affected work within 24 hours. Once begun, the reduction belongs only to that work order and does not reset its deadlines. Rests, travel, waits, observation windows, effect durations, Knowledge Transfer duration and missing-prerequisite tasks do not qualify. Required joint participation remains required for the entire actual common phase.

### Shared hard-denial mark
Law control and Living/Cracked Mask reveal use one mark keyed by **source character + target + actual encounter**. Each legal activation still pays its own cost before immunity/guard/save. If that mark already exists, these EPI effects apply no new control and gain no replacement rider. A mark is created only when one of those effects actually applies its control. Initiative changes do not reset it. Existing class features retain their own printed guards and fallbacks.

## 3. Unfinished Vow
Every player character begins this module with exactly **one active unfinished fictional vow**: one sentence describing an ideal action not yet fulfilled. You can have only one active unfinished vow.

Outside an encounter, you may spend 10 uninterrupted minutes to revise it, communicating the replacement to an understanding ally or Sentinel. The previous vow becomes superseded. You may instead retire it. When the table agrees the ideal action was genuinely fulfilled, mark it fulfilled. These state changes do not themselves award XP or clear conditions/resources.

A mask bound to a fulfilled, retired, or superseded vow becomes dormant immediately. A dormant physical mask can be rebound to the current active vow with one uninterrupted hour; quality, class/key, wearer identity, physical condition and wearer-owned reveal ledger persist.

## 4. Living and Cracked Masks
At adoption each PC receives one finite class-reflective blank keyed to the class selected for this module, and one reserve replacement keyed to that same class. Later multiclassing does not transmute them.

A project:
- binds the active vow and mask class at project start;
- requires **8 active hours personal shaping**;
- pauses only after completed one-hour blocks;
- has an absolute deadline of projectStart + 168 elapsed hours;
- receives no assistant time or bonus;
- requires the vow to be communicated before shaping;
- records 0–3 knowingly withheld fictional facts, giving crafting DC `10 + secret count`;
- uses one **bare ability check** with the fixed key ability. Proficiency bonus applies only if an exact feature applies to that ability check; tool proficiency alone does not add PB.
- Success/Critical Success => Living Mask. Failure/Critical Failure => Cracked Mask.

If the vow changes before the crafting check, the project pauses. You may cancel, spoiling the committed blank, or finish a **cosmetic dormant mask** under the original project record and original deadline; later rebind is still possible.

| Class | Mask key | Reflective material |
|---|---:|---|
| Bard | CHA | silvered resonant glass scored with the character's own performance marks |
| Cleric | WIS | polished devotional mirror-metal bearing the cleric's chosen sacred symbol |
| Crimson Agent | INT | polished crimson hematite-glass with a fine capillary pattern |
| Dragoon | STR | mirror-polished lance-steel scale |
| Druid | WIS | reflective resin cast over shed bark or stone from a personally tended natural place |
| Mage | INT | smoked prism-glass that catches the mage's chosen elemental hue |
| Mirrorsage | INT | true mirror-silver backed by a hand-marked reflection grid |
| Monk | DEX | water-polished mirrorstone thin enough to wear as a face plate |
| Oracle | CHA | polished scrying glass marked with the Oracle's Mystery sign |
| Paladin | CHA | mirror-polished oathsteel carrying a nonbinding personal-vow inscription |
| Ranger | WIS | still water frozen beneath moonlight |
| Shaman | WIS | mica-backed spirit glass framed in polished bone or wood |
| Soldier | CON | mirror-polished shield steel cut from a retired defensive plate |
| Thief | DEX | polished shards of black glass |
| Tinker | INT | polished brass-and-glass lens plate with visible maker marks |
| Warrior | recorded permanent Warrior ability (STR or DEX) | mirror-finished alchemical steel blank |
| Wizard | INT | liquid silver condensed from Arcane Crucible fumes |

For Warrior, the key uses the Warrior's already-recorded permanent level-1 Strength-or-Dexterity class ability choice; no new choice is made for the mask.

A completed mask weighs **2 lb**. One mask per wearer can be operative. If no operative mask exists, an eligible completed/rebound mask may become operative immediately. Otherwise a new one remains dormant until a beneficial rest, when you may designate one owned eligible mask operative. Vow fulfillment/retirement/supersession immediately dormants its mask. Designation never refreshes reveal charge.

While an operative mask is worn:
- Living or Cracked: advantage on saves explicitly against fear effects and Null lullabies.
- Cracked: disadvantage on a social ability check involving deception when that deception would materially impede the active vow.
- **Reveal:** wearer owns one reveal charge, refreshed to one by a beneficial Short or Long Rest under the real rest limits. As an Action target one creature within 20 feet that you can perceive, that can perceive the mask, with line of effect. Spend charge before its Charisma save against `8 + PB + fixed mask-key modifier`. Failed save applies actual **Stunned** for exactly one round; initiative expiry is the same initiative marker next round, outside initiative six elapsed seconds. The shared hard-denial mark above applies. Immunity blocks Stunned. No project/vow/mask switch refreshes the wearer ledger.

Donning is an Action. On your own turn you can safely remove the mask as a Free Action while audibly stating one truthful current emotional-state statement; outside your turn use a Reaction if available. If unable to speak but able to sign/write and be understood, use an Action. You can always remove it ordinarily as an Action with no invented curse.

## 5. Virtues and the Conflict Die
Natural source resonance pairings:

| Virtue | Classes |
|---|---|
| Courage | Bard, Warrior, Paladin |
| Balance | Druid, Ranger, Dragoon |
| Law | Cleric, Soldier, Mage |
| Sorrow | Oracle, Shaman |
| Pattern | Wizard, Tinker, Mirrorsage |
| Contradiction | Thief, Crimson Agent |
| Transition | Monk, Mirrorsage, Paladin |

A class not listed with a virtue is not automatically opposed.

At the start of each session, select one actual class you possess, state one concrete strength supported by its mechanics, choose one virtue, and state the fictional tension between them. Player and Director agree whether it is meaningful. It lasts that session.

Once per session, before an eligible **ability check**, declare a Conflict Die and roll **d20 + d12** together, adding the d12 to the total. It never applies to attacks or saving throws and cannot combine with Epilogue Inspiration. Fixed-DC checks use normal four-degree rules and bounded natural-20/1 shift. Opposed check: higher total wins; tie leaves existing state unchanged, so an initiating user fails to change it.

If the final outcome succeeds, resolve the success fully and then gain **1 current core Exhaustion**. Failure/tie spends the Conflict use but gains no Exhaustion. At Exhaustion 5, apply current cumulative disadvantage to the d20, then add d12/modifiers; if success occurs, resolve it first, then gain Exhaustion 6 and its current lethal rule. A creature immune to Exhaustion at declaration cannot use Conflict Die. If a successful outcome is already known to grant Exhaustion immunity before the cost would be paid, that check is ineligible. An unforeseen independent immunity arising after legal declaration follows its real rule; no hidden deferred Exhaustion is invented.

## 6. Archon Petition
Eligible petitioners: Cleric, Monk, or another character with a pre-existing spiritualMentor record. A qualified Witness first performs a 10-minute consultation. Then complete one uninterrupted hour of meditation and the **10-minute symbolic act** for the chosen virtue:

- Courage: name one feared but voluntary task and take one concrete preparatory step.
- Balance: balance two unequal physical loads so neither support bears more than half the combined weight.
- Law: write one rule for the current problem and one explicit exception condition.
- Sorrow: memorialize a real in-fiction loss without inventing history.
- Pattern: arrange seven marked tiles into a repeatable documented sequence.
- Contradiction: state two apparently conflicting true propositions and the context in which both can be true.
- Transition: disassemble/reassemble a simple nonmagical marker/tool into a different useful configuration.

After all three stages, roll **1d12**. Once rolled, that character cannot complete another petition for 7 elapsed days.

### Result 1–4: Guidance
One 24-hour boon; only one Guidance active at once:
- Courage: advantage on STR (Athletics) confronting immediate physical danger, or CHA (Persuasion) rallying someone to face immediate danger.
- Balance: advantage on WIS (Survival) stabilizing natural/environmental situation, or WIS (Animal Handling) calming a beast.
- Law: advantage on INT (Investigation) examining rules/contracts/records, or CHA (Persuasion) in formal negotiation governed by stated rules.
- Sorrow: advantage on WIS (Medicine), or WIS (Insight) concerning grief/pain/loss.
- Pattern: advantage on INT (Arcana) involving magical patterns, or INT (Investigation) involving formulae/sequences.
- Contradiction: advantage on WIS (Insight) for inconsistency/motive, or INT (Investigation) for conflicting records.
- Transition: advantage on DEX (Acrobatics) involving controlled change of position, or INT (Engineering) involving controlled mechanical transformation.

### Result 5–8: Temporary blessing
Until next module dawn, gain the exact card envelope for the virtue below. It bypasses only normal acquisition; it grants no class level, engine, pool, equipment or other card. Duplicate exact card gives no extra effect and no reroll.

| Virtue | Temporary feature | Activation | Target | Card duration | Frequency | Effect |
|---|---|---|---|---|---|---|
| Courage | Combat Instinct | Passive | Self | Permanent | Always | Combat Instinct. Gain +1 on initiative rolls. You cannot be Surprised while conscious unless the opposing creature's Stealth check exceeds your passive Perception by 5 or more. This does not grant extra Actions or movement before combat. |
| Balance | Natural Explorer | Passive | Self | While known | Continuous | Advantage on Survival checks in natural terrain; ignore nonmagical difficult terrain caused by vegetation, loose earth, mud or snow. Magical terrain, climbing and hazards still require their own rules. |
| Law | Tactical Awareness | Passive | Self | During combat | Continuous | Gain+2 Perception and initiative. Does not reveal unseen creatures automatically or allow attacks without line of fire. |
| Sorrow | Alchemical Knowledge | Passive | One potion/substance examined for 1 minute | Check only | At will | Gain advantage on INT(Arcana) or alchemist-tool checks to identify a substance's mundane ingredients and likely purpose. Identification does not guarantee safety or supply a recipe/materials; failure yields uncertainty, not false certainty. |
| Pattern | Scholarly Mind | Passive | Self | Permanent | Always | Scholarly Mind. Tags: base, passive, knowledge. You have advantage on Intelligence checks whose primary purpose is recalling, researching or analyzing arcane theory, magical history, planar magical principles or constructed spell formulae. It does not grant advantage on spell attacks, Counterspell checks or general Investigation unrelated to arcane scholarship. |
| Contradiction | Trap Intuition | Passive | Self | While searching for traps | Continuous | Advantage on Perception/Investigation to notice physical traps and their triggers. Does not reveal every trap automatically or defeat concealed magic. |
| Transition | Unarmored Speed | Passive | Self | Permanent while unarmored | Always | Unarmored Speed. Tags: base, passive, mobility. While wearing no armor and using no shield, increase walking Speed by 5 feet and gain +1 on initiative rolls. At Monk 11 the Speed increase becomes 10 feet. This bonus does not multiply other Speed increases and is suppressed while armored. |

### Result 9–11: Archon Test
The Director runs the finite symbolic challenge for the petition virtue. The player knows it is a challenge with a finite clock, but puzzle answers belong in Director rules. Success sets both Epilogue Inspiration slots ready and clears spent-recoverable slots; it never creates a third slot. Failure creates VowReviewPending and blocks another petition until resolved. You may revise/retire the vow normally, or reaffirm unchanged after 10 uninterrupted minutes; reaffirmation creates one Disquiet at that completion time.

### Result 12: Concord Step Sigil
Petitioner receives one petitioner-bound inter-session travel sigil. It can activate only after the granting session closes and before the next scheduled session opens. Outbound channel is **10 uninterrupted minutes** from the designated existing Aethel Concord threshold to one of four enabled visitor alcoves, with up to five total living/conscious/willing travelers. Each actual outbound traveler receives one personal return right expiring at `outboundAt + 8h`.

A return is another 10-minute channel from the same destination alcove to the same Aethel threshold. Latest legal start is exactly +7h50m. A valid return completing exactly at +8h resolves first, then remaining flags expire. Opening the next session cancels an uncommitted outbound activation but does **not** erase already-issued return rights. Recheck living/conscious/willing/present status, legal spaces and stronger travel denials at completion. Invalid companions are omitted; a solo invalid returner fails. Missing the deadline can strand a traveler: the visitor room remains lit, breathable and temperate, with finite supplies, but this module provides no free onward/return route and no Haven.

The four destinations are Ember Record Room (Bastion), Quiet Ledger Alcove (Veiled Expanse), Current Table Room (Radiant Currents), and Question Lantern Room (Boundless Void). Their activities produce only finite mundane records/story consequences, never recovered Equation text or hidden cosmological truth.

## 7. Sentinel Encounters
A Sentinel encounter can grant at most one finite information boon to the Expedition. Ask one concrete in-fiction question relevant to a current problem. The Sentinel has a predefined knowledge record and is not omniscient. If out of scope, it says so; one immediate follow-up within one minute may narrow the same subject. After the boon/final out-of-scope answer, that encounter is spent.

Allowed boon types: a puzzle solution, local map fragment, or contingent future vision. These cannot supply Equation fragments, certainty about unresolved identities, teleport/floor shortcuts, guaranteed fate, retcons, permanent class features, or travel permission.

This module's finite examples are: the Three Lamps puzzle, a four-room local map fragment, and a contingent sluice-flood forecast. Information learned belongs to the Expedition and does not retroactively become public knowledge.
