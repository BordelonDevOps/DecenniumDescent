# Conditions — integrated playtest reference

**Status:** reviewed and reference-validated within generic Core condition/recovery scope. All28 Core condition identities preserved. New generic procedures are explicit playtest proposals, not edits to approved books or a claim of game-wide balance.

[Core resolution and Wounds](CORE_RESOLUTION_PLAYTEST.md) · [Recovery and exposure procedures](CONDITION_RECOVERY_PLAYTEST.md) · [Custom rider bindings](CUSTOM_CONDITION_BINDINGS.md) · [Development coverage](GAME_DEVELOPMENT_COVERAGE.md)

The Core catalog contains all 28 conditions. The older shared class reference listed 15 of them; that was a reference omission, not lost source data. This overlay supplies the complete reference without modifying the books or that preserved class file.

## Shared handling

This overlay governs generic conditions in the combined candidate. A reviewed card overrides a generic clause only where it prints the specific exception. An unreviewed historical summary never grants an extra ability or bypasses a gate. The existing combined source-character/target/encounter hard-denial cap still applies to class/spell/companion applications.

Record each condition source, affected creature, applying DC, magnitude, start, duration and ending method. Same-name nonnumeric penalties apply once; independent sources continue until each ends. A generic cure naming a condition clears its source records unless a reviewed procedure specifies one-record scope. Bleeding Medicine and Burning DEX saves use the specific procedures below. Track Charmed, Frightened, Marked and Grappled relationships separately. Exhaustion, Intoxication, Unity and Wounds use their explicit tracks.

Immunity to a named condition prevents that condition, including an inherited component, but does not silently grant immunity to every parent condition that can cause it. For example, Prone immunity prevents the Prone component of Unconscious, not its other effects. Immunity to an inflicted condition never erases the underlying zero-HP or dead state. Gaining immunity suppresses applicable existing effects while immunity lasts; their clocks continue unless explicitly paused. Removing immunity does not reapply a one-time consequence or restart an old duration.

Advantages and disadvantages never multiply dice: any advantage and any disadvantage cancel to one normal d20 roll, regardless of the number of sources. Automatic failure of a required check/save is resolved without a roll. A condition does not give a save where its source grants none. A critical-if-hit rider never makes a missed attack hit. Automatic failure has no rolled total: use ordinary Failure, not Critical Failure or an invented failure margin, unless the source explicitly supplies one.

Generic Core Bleeding and Burning join family.bleeding and family.ongoing-fire respectively, with source-owner stack groups. At one identical target timing marker, all due generic and custom groups in that family compete: highest expected unmitigated damage, then earliest application. Only the winning group's source-permitted instances deal damage. All due groups consume that tick; losers do not defer or bank it. Different printed markers resolve separately. No record also receives a duplicate generic tick. Core generic timing is end of regular target turn; extra turns do not tick. Outside initiative preserve one periodic step per complete six seconds with no duplicate interval across initiative transitions.

Strain is not globally unique: expedition.strain and warrior.serum-strain are separate source-qualified tracks, both distinct from the six-level Exhaustion condition. See the Strain namespace reference for the current candidate. Oracle one-turn Revelation backlash is also separate from global Exhaustion; its printed penalties and endpoint remain unchanged. Wound Eater feeding failures explicitly use global Exhaustion. Never silently convert similarly named tracks.

See CONDITION_RECOVERY_PLAYTEST.md for finite recovery, cleansing, substance, Intoxication and Unity procedures. These new proposals are labeled separately from recovered source rules. Conditions do not reveal Director secrets or force player beliefs or decisions.

SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review.

## Quick index

| Condition | Configuration |
|---|---|
| [Addicted](#addicted) | active provisional overlay |
| [Bleeding](#bleeding) | active provisional overlay |
| [Blinded](#blinded) | active provisional overlay |
| [Burning](#burning) | active provisional overlay |
| [Charmed](#charmed) | active provisional overlay |
| [Corrupted](#corrupted) | active provisional overlay |
| [Dazed](#dazed) | active provisional overlay |
| [Deafened](#deafened) | active provisional overlay |
| [Exhausted](#exhausted) | active provisional overlay |
| [Frightened](#frightened) | active provisional overlay |
| [Grappled](#grappled) | active provisional overlay |
| [Incapacitated](#incapacitated) | active provisional overlay |
| [Intoxicated](#intoxicated) | active provisional overlay |
| [Invisible](#invisible) | active provisional overlay |
| [Marked](#marked) | active provisional overlay |
| [Paralyzed](#paralyzed) | active provisional overlay |
| [Petrified](#petrified) | active provisional overlay |
| [Poisoned](#poisoned) | active provisional overlay |
| [Prone](#prone) | active provisional overlay |
| [Resonance Burn](#resonance-burn) | preserved; inactive in this Dissonance configuration |
| [Restrained](#restrained) | active provisional overlay |
| [Silenced](#silenced) | active provisional overlay |
| [Staggered](#staggered) | active provisional overlay |
| [Stunned](#stunned) | active provisional overlay |
| [Unconscious](#unconscious) | active provisional overlay |
| [Unity Exposure](#unity-exposure) | active provisional overlay |
| [Withdrawal](#withdrawal) | active provisional overlay |
| [Wounded](#wounded) | active provisional overlay |

<a id="addicted"></a>
## Addicted

**Preserved Core text:** The creature has dependence on a named substance. Without a maintenance dose after a long rest, it gains Withdrawal.

**Effect:** Record dependence on one named substance. After each completed long rest, if the creature has not taken the required maintenance dose for that substance, apply Withdrawal for that substance. Existing source procedures for repeated doses, dependence DC, tolerance and overdose continue to operate.

**Application:** Applied only by a substance or dependence procedure that explicitly creates or advances dependence. Merely consuming a substance does not automatically grant Addicted unless its procedure says so.

**Duration and ending:** A new maintenance dose is due immediately after each completed long rest. Until taken, apply that substance's Withdrawal; a pre-rest dose cannot satisfy this new interval. A dose suppresses symptoms until the next maintenance interval, but dependence persists. A seven-day no-dose recovery project or an explicit dependence-removal effect can remove it; see CONDITION_RECOVERY_PLAYTEST.md.

**Stacking:** Track one Addicted record per named substance. Separate substance dependencies coexist; duplicate dependence on the same substance does not create multiple copies unless a source defines severity.

**Immunities and specific exceptions:** A feature explicitly preventing dependence blocks application. Magic that only removes symptoms does not automatically remove dependence, consistent with the source treatment text.

**Explicit integration decisions:**

- NEW: maintenance dose may relieve that substance's current Withdrawal symptoms without removing Addicted; exact dependence cure procedure remains deferred.

**Remaining wider integration work:**

- Audit individual substance cards, dose escalation wording, equipment availability and specific cure effects during item integration.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 727, definition paragraph 728; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="bleeding"></a>
## Bleeding

**Preserved Core text:** Take damage equal to proficiency bonus at the end of each turn. An action and Medicine check or magical healing ends it.

**Effect:** At the end of the affected creature's regular turn, take damage equal to its current PB, unless the selected reviewed application prints a different magnitude. Use that application's specified physical type; if none, slashing.

**Application:** Only explicit Bleeding applications create a source record. Record DC (or 10), magnitude, type and endpoint.

**Duration and ending:** Persists until its source or applicable cure ends it. Self or adjacent helper spends an Action selecting one active eligible Bleed record before a WIS (Medicine) check: printed cure DC, otherwise recorded applying effect/class/spell DC, otherwise 10. Success or Critical Success ends that record only. One legal magical healing event with positive pre-cap/pre-prohibition potential ends all ordinary records with an automatic-healing endpoint, even at full HP or while Corrupted/Decay prevents actual HP gain. Each Shaman Blood Curse instead gets its own printed CON save. Explicit end-one/end-all removers retain exact scope and protected-source exceptions.

**Stacking:** Independent source-owner records enter unified family arbitration at their actual marker. No DC tie-break or separate generic damage layer. Medicine ends one selected record; positive-potential magical healing ends all eligible automatic-cure records.

**Immunities and specific exceptions:** Creatures explicitly immune to bleeding/blood-loss effects cannot gain it. Specific spell/class/item Bleeding numbers replace the generic PB magnitude only when printed.

**Explicit integration decisions:**

- NEW: affected-creature PB; explicit physical type or slashing fallback; source DC or 10; one regular-turn tick and strongest-record selection.
- Source-faithful clarification: magical healing need not increase current HP to end Bleeding.
- SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 729, definition paragraph 730; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="blinded"></a>
## Blinded

**Preserved Core text:** Cannot see; automatically fails sight checks; attacks have disadvantage and attacks against it have advantage.

**Effect:** The creature cannot see, automatically fails checks that require sight, has disadvantage on attack rolls, and attack rolls against it have advantage.

**Application:** Only an effect that explicitly inflicts Blinded applies it.

**Duration and ending:** Use the applying effect's printed duration, save, cure or endpoint.

**Stacking:** Multiple Blinded applications do not increase the penalties; track independent durations only when needed to know when all sources have ended.

**Immunities and specific exceptions:** A sense that does not require sight may still function. A feature explicitly allowing sight while Blinded overrides only its printed scope.

**Compatible V6/source details:**

- V6 matches: cannot see, automatically fails sight-required checks, own attacks have disadvantage, attacks against have advantage.

**Remaining wider integration work:**

- Full special-senses and vision interaction belongs to the stealth/vision pass.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 731, definition paragraph 732; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="burning"></a>
## Burning

**Preserved Core text:** Take fire damage at end of turn. An action, immersion, or successful Dexterity save ends it.

**Effect:** At end of the affected creature's regular turn its generic record offers 1d4 fire damage to unified family arbitration, unless its source specifies another magnitude. Only the winning stack group deals damage. Damage immunity does not by itself remove Burning.

**Application:** Applied only by an effect that explicitly inflicts Burning. Record the applying effect's DC; if none exists, use DC 10.

**Duration and ending:** Self or adjacent helper may spend one Action to end all active ordinary-extinguishable attached fires on this creature. Full immersion of all burning portions does the same. Explicit protected-source exceptions survive. At each regular target turn end, after due ticks are consumed, each surviving active ongoing-fire record with future damage remaining makes its own binary DEX save against its own source DC or 10. Success ends only that record. An indefinite generic fire counts as having future damage; a finite record with its final tick consumed expires without another save.

**Stacking:** Independent records enter unified ongoing-fire family arbitration. One Action/full immersion clears all ordinary-extinguishable records; DEX saves operate per surviving eligible record, not one selected-source save for all fires.

**Immunities and specific exceptions:** Fire immunity prevents the damage but does not automatically end Burning unless the source or immunity says so. An effect explicitly immune to Burning blocks application.

**Explicit integration decisions:**

- NEW: 1d4 fire fallback, source DC or 10, damage then free ending save; Action/immersion can end before damage.
- NEW: shared periodic timing and strongest-record precedence; adjacent helper and immersion boundaries.
- SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 733, definition paragraph 734; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="charmed"></a>
## Charmed

**Preserved Core text:** Cannot willingly harm the charmer; charmer has advantage on social checks against it.

**Effect:** The creature cannot willingly take an action or make a choice it knows would harm the charmer: this includes attacks, harmful targeting, and knowingly placing the charmer in a harmful area or indirect effect. Unforeseeable or genuinely unknown collateral harm is not retroactively a willing violation. The charmer has advantage on social ability checks against it. Charmed itself never compels affection, obedience, beliefs, allegiance, affirmative protection or self-harm.

**Application:** Each application identifies the charmer/source.

**Duration and ending:** Use the applying effect's printed duration and repeat-save/ending procedure.

**Stacking:** A creature may be Charmed by more than one source; each source relation is tracked independently. Advantage does not stack.

**Immunities and specific exceptions:** Charm immunity prevents application. Forced actions from another effect are not made voluntary merely because the creature is Charmed.

**Compatible V6/source details:**

- V6 specifies the creature cannot attack the charmer or target the charmer with harmful abilities or magical effects, and gives the charmer advantage on social interaction checks.

**Explicit integration decisions:**

- Agency clarification: Charmed never by itself grants control over beliefs, targets or decisions beyond the explicit harm restriction.
- Source-faithful correction reviewed in GPT_CUSTOM_RIDER_SECOND_REVIEW.md: Core's unwilling-to-harm restriction is broader than direct targeting; preserve its area/indirect-harm scope without importing mind control.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 735, definition paragraph 736; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="corrupted"></a>
## Corrupted

**Preserved Core text:** Healing is reduced, corruption-sensitive effects worsen, and long rests may shift behavior or form until cleansed.

**Effect:** Halve each healing effect's final potential HP once, rounded down, before the HP ceiling. Saves against spells/abilities from individually recorded Evil creatures have disadvantage; its aura can be detected by effects revealing evil. At each completed long rest make DC 15 WIS save or move one moral step Good to Neutral to Evil, leaving law/chaos unchanged. Already Evil remains Evil. Alignment does not compel conduct, party separation, PvP or automatic oathbreaking.

**Application:** Only effects that explicitly inflict Corrupted apply it.

**Duration and ending:** Persists until an explicit cleansing effect or the eight-hour cleansing project in CONDITION_RECOVERY_PLAYTEST.md succeeds. Long rest alone does not cleanse it. At a simultaneous cleansing/rest endpoint, resolve cleansing first and make the Corrupted rest save only if it remains.

**Stacking:** Corrupted does not stack with itself. Apply the generic half-healing reduction once; an effect does not halve again merely because it restates the same Corrupted penalty.

**Immunities and specific exceptions:** Natural-20 death-save recovery and recovered Stable 1-HP recovery are state-recovery rules rather than healing effects and still restore exactly 1 HP. Explicit cleansing or protection may override within scope.

**Compatible V6/source details:**

- V6: healing effects restore half normal HP; disadvantage on saves against spells/abilities from evil creatures; faint aura detectable by magic revealing evil; at end of each long rest make DC 15 Wisdom save or alignment shifts one step toward evil.

**Explicit integration decisions:**

- NEW: round half healing down once; guaranteed death-save/Stable one-HP state recovery is not a healing effect.
- Source-grounded: individual recorded alignment or Evil tag only; no ancestry/faction inference, forced behavior or automatic conduct violation.
- NEW: generic cleansing project supplies a finite recovery route.

**Remaining wider integration work:**

- Cross-check separately reviewed corruption-sensitive transformations and specific restoration effects.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 737, definition paragraph 738; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="dazed"></a>
## Dazed

**Preserved Core text:** Choose either action or movement on the turn, not both; no bonus action.

**Effect:** On every affected turn, including extra turns, choose Action-mode (at most one Action total and no voluntary Speed expenditure or Dash) or Movement-mode (ordinary movement, no Action). Movement expressly included in the permitted Action still resolves. No Bonus Action; Reactions and concentration are unaffected.

**Application:** Only an effect that explicitly inflicts Dazed applies it.

**Duration and ending:** Use the applying effect's endpoint. Applies immediately: earlier voluntary movement that turn forbids further Actions; an earlier Action forbids further voluntary Speed expenditure; if both already occurred, neither may occur again. Do not undo completed events. Extra-Action grants cannot bypass the one-Action ceiling.

**Stacking:** Multiple Dazed applications do not further reduce the turn; track only the longest/independent ending sources.

**Immunities and specific exceptions:** An immunity to Dazed blocks application. Forced movement is not voluntary movement and remains possible.

**Explicit integration decisions:**

- NEW: immediate mid-turn handling, each extra turn gets its own mode, one-Action ceiling, explicit action-contained movement exception.

**Remaining wider integration work:**

- Interaction with future nonstandard action types if any are introduced.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 739, definition paragraph 740; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="deafened"></a>
## Deafened

**Preserved Core text:** Cannot hear and fails hearing checks; verbal coordination may fail.

**Effect:** The creature cannot hear and automatically fails checks that require hearing. It cannot satisfy a rule that specifically requires hearing another creature's command, warning, chant or audible signal.

**Application:** Only effects that explicitly inflict Deafened apply it.

**Duration and ending:** Use the applying effect's duration/end condition.

**Stacking:** Multiple applications do not compound.

**Immunities and specific exceptions:** Deafened does not prevent the creature from speaking or supplying its own verbal components unless another condition such as Silenced applies.

**Compatible V6/source details:**

- V6 matches inability to hear and automatic failure of hearing-required checks.

**Explicit integration decisions:**

- Operational clarification: 'verbal coordination may fail' means hearing-dependent coordination requirements fail; no generic roll is added.

**Remaining wider integration work:**

- Future command/audible-coordination features must state whether hearing is required.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 741, definition paragraph 742; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="exhausted"></a>
## Exhausted

**Preserved Core text:** Use the six-level exhaustion track; effects are cumulative and level 6 is death.

**Effect:** Track 0–6 cumulative levels: 1 disadvantage ability checks; 2 half Speed after flat changes; 3 disadvantage attacks and saves; 4 maximum HP max(1,floor(otherwise-applicable maximum/2)); 5 Speed zero; 6 death.

**Application:** An effect that grants one or more Exhaustion levels increases the track by that amount, maximum 6, unless it explicitly sets a level instead.

**Duration and ending:** Eligible beneficial eight-hour long rest removes one level under CONDITION_RECOVERY_PLAYTEST.md, at most one generic removal per 24 hours. Source-specific prerequisites can block removal. Meeting a prerequisite such as Moisture Dependency immersion does not itself remove a level unless printed.

**Stacking:** Levels add, maximum 6. Derive level-4 maximum from the otherwise-applicable current maximum, never a previously halved value. Clamp HP down when maximum decreases; raising maximum does not heal. Level-5 zero Speed overrides halving.

**Immunities and specific exceptions:** An explicit Exhaustion immunity blocks levels. Removing Exhaustion from a dead level-6 creature does not restore life; resurrection is still required.

**Compatible V6/source details:**

- Level 1: disadvantage on ability checks.
- Level 2: Speed halved.
- Level 3: disadvantage on attack rolls and saving throws.
- Level 4: hit point maximum halved.
- Level 5: Speed reduced to 0.
- Level 6: death.

**Explicit integration decisions:**

- NEW: maximum-HP floor 1, recomputation/clamping and flat-Speed-before-halving order.
- NEW: finite generic long-rest recovery; source-specific removal blocks remain.
- Recovered V6: six cumulative level effects.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 743, definition paragraph 744; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="frightened"></a>
## Frightened

**Preserved Core text:** Disadvantage while source is visible and cannot willingly move closer.

**Effect:** While the source of fear is visible/in line of sight, the creature has disadvantage on ability checks and attack rolls. While Frightened it cannot willingly move closer to that source.

**Application:** Each application records its fear source.

**Duration and ending:** Use the applying effect's duration and repeat-save procedure.

**Stacking:** Separate fear sources are tracked independently. Disadvantage does not stack.

**Immunities and specific exceptions:** Fear immunity blocks application. Forced movement may move the creature closer because the prohibition is on willing movement.

**Compatible V6/source details:**

- V6 specifies disadvantage on ability checks and attack rolls while the source of fear is within line of sight, and prohibits willingly moving closer.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 745, definition paragraph 746; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="grappled"></a>
## Grappled

**Preserved Core text:** Speed 0; ends if grappler is incapacitated or reach is broken.

**Effect:** Speed becomes 0 and cannot be increased by bonuses while Grappled.

**Application:** A Grappled application records the grappler/source and its reach.

**Duration and ending:** Ends if the grappler is Incapacitated, reach breaks, or the applying effect ends/its escape succeeds. A class/spell card with a fixed save DC uses an Action and STR (Athletics) or DEX (Acrobatics) against that DC. An ordinary V6 grapple uses an Action to escape with STR (Athletics) or DEX (Acrobatics) opposed by the grappler's STR (Athletics); higher total wins, ties retain the grapple. Multiple grapplers require ending each relationship.

**Stacking:** Multiple grapplers may maintain separate Grappled records; Speed remains 0 until all relevant grapples end.

**Immunities and specific exceptions:** A creature immune to Grappled cannot receive it. Teleportation or forced movement that breaks reach ends that grapple unless a specific effect says otherwise.

**Compatible V6/source details:**

- V6 adds that the creature cannot benefit from bonuses to Speed and confirms ending when the grappler is incapacitated or an effect removes the target from reach.
- V6 all-XML paragraph 8206 gives ordinary grapple application and opposed escape; fixed-DC card escapes remain specific class/spell rules.

**Remaining wider integration work:**

- Final generic grapple/shove procedure remains part of the combat maneuver audit.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 747, definition paragraph 748; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="incapacitated"></a>
## Incapacitated

**Preserved Core text:** Cannot take actions or reactions.

**Effect:** The creature cannot take an Action, Bonus Action or Reaction. Passive effects continue unless their own rules require consciousness or another condition disables them. Incapacitated by itself does not reduce Speed or prohibit speech.

**Application:** Applied by a condition or effect that explicitly says the creature is Incapacitated.

**Duration and ending:** Use the parent condition/effect's duration.

**Stacking:** Does not stack.

**Immunities and specific exceptions:** Current shared concentration rules end concentration immediately when the creature becomes Incapacitated. A specific effect may preserve a passive benefit through Incapacitation if explicitly stated.

**Compatible V6/source details:**

- V6 matches: cannot take actions or reactions.

**Explicit integration decisions:**

- NEW integration: Bonus Actions are included in unavailable actions.
- Already explicit in CLASS_PLAYTEST_RULES.md: becoming Incapacitated ends concentration.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 749, definition paragraph 750; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="intoxicated"></a>
## Intoxicated

**Preserved Core text:** Disadvantage on precise Dexterity and Intelligence checks; advantage on one save against fear. Stacks worsen into Dazed and Unconscious.

**Effect:** Use the single 0–5 Intoxication track and procedures in CONDITION_RECOVERY_PLAYTEST.md. Level 1 grants one fear-save advantage use per continuous nonzero episode and disadvantage precise-memory checks; level 2 additionally gives disadvantage precise DEX/INT checks; level 3 additionally Dazed and Speed-10; levels 4/5 additionally Unconscious and their poisoning/emergency procedures.

**Application:** Explicit Intoxication gains advance the dose-driven track. An effect saying Intoxicated without a numeric level creates a separate minimum effective score of 2 for its printed duration, or NEW two hours if it prints no duration. It adds no dose-driven points. Generic direct applications never create floors 3–5. A source setting level 3–5 must individually state its dose-driven points or exact recovery exception.

**Duration and ending:** Use the hourly sobriety, level 4 timer or level 5 emergency procedure, or an explicit reviewed cure. Full details including direct timed applications are in CONDITION_RECOVERY_PLAYTEST.md. Each no-duration floor-2 application expires exactly two elapsed hours after application. Multiple floors do not stack, but the floor persists while any is active; ending one does not remove independent dose-driven points.

**Stacking:** One track. One fear-save advantage use for the entire episode until level 0, never refreshed by moving between positive levels. Other independent Dazed/Unconscious/Poisoned sources remain after intoxication recovers.

**Immunities and specific exceptions:** An effect explicitly preventing intoxication blocks track gain. Unconscious at level 4 uses the normal Unconscious condition.

**Compatible V6/source details:**

- Existing Intoxication Track: 0 Sober; 1 Relaxed with advantage on one fear save and disadvantage on precise memory checks; 2 Intoxicated condition; 3 Dazed and Speed -10 ft; 4 Unconscious for 1d4 hours plus Constitution save against poisoning; 5 medical emergency, gain a Wound or die without treatment at Director discretion.

**Explicit integration decisions:**

- NEW: cumulative condition thresholds, direct-application floor and continuous-episode fear-save limit.
- NEW: finite sobriety, poisoning and medical-emergency procedures; source values/conditions preserved.

**Remaining wider integration work:**

- Individual brew/substance cards still need their complete dose, access and balance audit.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 751, definition paragraph 752; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="invisible"></a>
## Invisible

**Preserved Core text:** Cannot be seen normally; attacks against it have disadvantage and its attacks have advantage until location is revealed.

**Effect:** Cannot be seen normally. Until an observer knows its location, that observer attacks it with disadvantage and it attacks that observer with advantage. Once location is revealed, these Invisible-specific modifiers end for that observer. Do not re-grant them through V6 generic unseen rules solely because it is still Invisible. A special sense actually seeing it bypasses these modifiers. Knowing location is not seeing; effects requiring sight still need sight.

**Application:** Only an effect explicitly granting Invisible applies it.

**Duration and ending:** Use the granting effect's duration. V6 attacks reveal location upon attacking; resolve the revealing attack first, then observers able to perceive evidence know the location. Independent hiding/concealment uses its own procedure; later broad vision integration must specify losing and regaining location knowledge. Invisible remains visually effective after revelation.

**Stacking:** Multiple Invisible effects do not stack.

**Immunities and specific exceptions:** A special sense or magic that actually sees the creature removes Invisible's unseen benefits for that observer within that sense's scope. Knowing location is not the same as seeing.

**Compatible V6/source details:**

- V6: impossible to see without special senses or magic; heavily obscured for hiding; location may be detected by noises or tracks; attacks against have disadvantage and own attacks have advantage.

**Source conflicts:**

- Core explicitly ends the generic attack advantage/disadvantage when location is revealed; V6 states those attack modifiers without that endpoint. Core controls the conflict.

**Explicit integration decisions:**

- Operational distinction: visibility state and known location are separate.
- No generic detection DC, automatic attack-reveal rule or movement-rehide rule is invented here.
- Recovered V6: attacking reveals location. NEW timing clarification: resolve that attack before its revelation; Core location endpoint specifically overrides the otherwise-conflicting unseen attack modifiers.

**Remaining wider integration work:**

- Stealth, sound, tracks, hiding and location-reveal procedure in the vision/stealth pass.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 753, definition paragraph 754; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="marked"></a>
## Marked

**Preserved Core text:** A named creature or faction can track, target, or trigger abilities against the marked creature.

**Effect:** Marked establishes a source-specific relationship between the marked creature and one named creature, faction or effect. It makes the target eligible only for tracking, targeting or trigger rights explicitly printed by that reviewed source.

**Application:** Every application records marker source/faction, the granting ability or rule, and any rights/duration printed there.

**Duration and ending:** Use the applying source's duration/end rule. If none is supplied, that Marked application remains incomplete and should not be activated until its source is reviewed.

**Stacking:** Marks from different named sources may coexist. Reapplying the same mark refreshes/replaces according to that source. Generic Marked supplies no additive numerical bonus.

**Immunities and specific exceptions:** An effect preventing marks blocks application within scope.

**Explicit integration decisions:**

- NEW integration: Marked alone grants no universal location knowledge, global tracking bonus, damage bonus or permission to bypass cover/planar boundaries.

**Remaining wider integration work:**

- Individual mark-producing features must define their specific rights.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 755, definition paragraph 756; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="paralyzed"></a>
## Paralyzed

**Preserved Core text:** Incapacitated, cannot move or speak, fails Strength/Dexterity saves, adjacent hits are critical.

**Effect:** The creature is Incapacitated, cannot move or speak, automatically fails Strength and Dexterity saving throws, attack rolls against it have advantage, and any attack that hits it from within 5 feet is a critical hit.

**Application:** Only an effect explicitly inflicting Paralyzed applies it.

**Duration and ending:** Use the applying effect's duration and repeat-save/ending procedure.

**Stacking:** Does not stack.

**Immunities and specific exceptions:** Paralysis immunity blocks application. Incapacitated consequences, including loss of Bonus Action/Reaction and concentration ending under the shared rule, apply.

**Compatible V6/source details:**

- V6 adds attack rolls against the creature have advantage and specifies attacks that hit from within 5 feet are critical.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 757, definition paragraph 758; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="petrified"></a>
## Petrified

**Preserved Core text:** Incapacitated stone-like state; resistance to damage, immunity to poison/disease, weight ×10.

**Effect:** The creature becomes an inanimate stone-like substance, weight ×10, ceases aging, is Incapacitated, cannot move or speak, is unaware, automatically fails Strength and Dexterity saves, and attacks against it have advantage. It has resistance to all damage except Corruption damage, and immunity to poison and disease; existing poison/disease effects are suspended rather than removed.

**Application:** Only an effect explicitly inflicting Petrified applies it.

**Duration and ending:** Use the applying effect's duration/removal rule. Suspended poison/disease resumes if Petrified ends and the underlying effect has not otherwise expired or been cured.

**Stacking:** Does not stack.

**Immunities and specific exceptions:** Petrification immunity blocks application. Corruption resistance is not granted because the special Core Corruption rule requires explicit Corruption protection.

**Compatible V6/source details:**

- V6: transformed into inanimate substance, weight ×10, cease aging, Incapacitated, cannot move/speak, unaware, attacks against have advantage, automatically fails Strength/Dexterity saves, resistance to all damage, immunity to poison and disease, existing poison/disease suspended rather than neutralized.

**Source conflicts:**

- Core damage rules separately state Corruption damage cannot be resisted unless an effect explicitly protects against Corruption. Petrified does not explicitly name Corruption.

**Explicit integration decisions:**

- Integration ruling: generic all-damage resistance from Petrified does not satisfy Core's explicit-protection requirement for Corruption.

**Remaining wider integration work:**

- Interaction with aging clocks and object-targeting effects belongs to later environment/item passes.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 759, definition paragraph 760; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="poisoned"></a>
## Poisoned

**Preserved Core text:** Disadvantage on attacks and ability checks.

**Effect:** The creature has disadvantage on attack rolls and ability checks.

**Application:** Only an effect explicitly inflicting Poisoned applies it.

**Duration and ending:** Use the applying effect's duration/removal rule.

**Stacking:** Multiple Poisoned applications do not stack disadvantage; independent durations may coexist.

**Immunities and specific exceptions:** Poisoned immunity blocks application. Poison damage resistance alone does not imply Poisoned immunity unless stated.

**Compatible V6/source details:**

- V6 matches exactly.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 761, definition paragraph 762; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="prone"></a>
## Prone

**Preserved Core text:** Crawl or stand; melee attackers within 5 ft. have advantage; ranged attackers have disadvantage.

**Effect:** Own attacks have disadvantage. Melee attacks against it within 5 feet have advantage; ranged attacks against it have disadvantage at every distance; other attacks beyond 5 feet have disadvantage. Movement requires crawling or standing. Drop Prone without Speed expenditure; standing costs half current Speed, rounded down, requires nonzero Speed and sufficient movement. Crawl costs 2 feet per foot, or 3 in difficult terrain.

**Application:** Applied when an effect explicitly knocks a creature Prone or another rule such as Unconscious causes it.

**Duration and ending:** Ends when the creature successfully stands or an explicit effect ends Prone.

**Stacking:** Does not stack.

**Immunities and specific exceptions:** Prone immunity blocks application. A feature may explicitly ignore Prone attack penalties.

**Compatible V6/source details:**

- V6: only movement is crawl unless standing; own attack rolls have disadvantage; attacks from within 5 feet have advantage, otherwise disadvantage.

**Source conflicts:**

- For a ranged attack made from within 5 feet, V6 distance-only wording would grant advantage while Core specifically says ranged attackers have disadvantage. Core controls.

**Explicit integration decisions:**

- Core-vs-V6 conflict resolved in favor of Core for ranged attacks within 5 feet.
- Recovered V6 movement: half-Speed standing and 2/3-for-1 crawling. NEW explicit zero-Speed standing prohibition, preventing zero-cost standing while Grappled.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 763, definition paragraph 764; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="resonance-burn"></a>
## Resonance Burn

**Preserved Core text:** Maximum RP reduced and spell failure risk increases until a long rest or treatment.

**Effect:** Preserved source condition only. It is inactive in the current Dissonance-only playtest configuration and therefore applies no numeric RP-cap reduction or spell-failure procedure until separately reviewed.

**Application:** A feature whose only unresolved consequence is Resonance Burn remains blocked/non-operational in this configuration unless that feature separately defines all needed numbers without invoking the historical Burn engine.

**Duration and ending:** Source says until a long rest or treatment when active; exact treatment remains part of the historical Burn review.

**Stacking:** No stacking procedure is active in the current configuration.

**Immunities and specific exceptions:** A reviewed configuration may explicitly enable Resonance Burn instead of or alongside another strain model, but that requires a separate decision.

**Source conflicts:**

- The current spell pilot explicitly uses Dissonance/Refrain and excludes the historical Burn/fizzle system to avoid stacking two strain engines.

**Explicit integration decisions:**

- Pilot decision: preserve but do not execute Resonance Burn while Dissonance/Refrain is the active strain system.

**Remaining wider integration work:**

- An individual card invoking unresolved historical Burn is not operational until separately adapted and reviewed; no universal second failure engine is active.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 765, definition paragraph 766; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="restrained"></a>
## Restrained

**Preserved Core text:** Speed 0; attacks against have advantage, own attacks and Dexterity saves have disadvantage.

**Effect:** Speed becomes 0 and cannot benefit from Speed bonuses. Attack rolls against the creature have advantage; its own attack rolls and Dexterity saving throws have disadvantage.

**Application:** Only an effect explicitly inflicting Restrained applies it.

**Duration and ending:** Use the applying effect's printed duration, save or escape rule. If an effect creates a physical restraint and provides no escape procedure, use the existing shared playtest escape procedure only if that source is eligible for it.

**Stacking:** Multiple Restrained applications do not compound penalties, but all independently maintained sources must end before the creature is no longer Restrained.

**Immunities and specific exceptions:** Restrained immunity blocks application. Teleportation does not automatically end a restraint unless it breaks the source relationship or the applying effect says so.

**Compatible V6/source details:**

- V6 adds that the creature cannot benefit from bonuses to Speed.

**Remaining wider integration work:**

- Final generic physical-restraint escape procedure in combat rules.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 767, definition paragraph 768; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="silenced"></a>
## Silenced

**Preserved Core text:** Cannot use verbal components, command words, Chants, or audible coordination.

**Effect:** The creature cannot use spell/ability verbal components, command words, Chants, or any feature requiring audible coordination. It may still think, perceive, move, use somatic/nonverbal abilities and use effects that explicitly function without sound.

**Application:** Only effects explicitly inflicting Silenced apply it.

**Duration and ending:** Use the applying effect's duration/end rule.

**Stacking:** Does not stack.

**Immunities and specific exceptions:** An ability explicitly usable without speech or audible sound is unaffected. Silence immunity blocks application only if explicitly defined.

**Explicit integration decisions:**

- Clarification: Silenced is not universal mental or magical shutdown.

**Remaining wider integration work:**

- Specific audible-command features must state whether they require being heard by recipients.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 769, definition paragraph 770; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="staggered"></a>
## Staggered

**Preserved Core text:** Cannot react, loses Guard, and the next forced movement gains +5 ft. Ends at start of next turn.

**Effect:** Cannot take Reactions. Remove current Guard: its unused +2 AC against the first attack and enabled Interpose end. Guard cannot be gained while Staggered. The next otherwise-legal forced-movement event before expiry gains 5 feet in the same direction, once; solid obstacles still stop it.

**Application:** Only an effect explicitly inflicting Staggered applies it.

**Duration and ending:** Ends at the start of the affected creature's next regular turn. The +5-foot rider is consumed by the first qualifying forced movement or expires unused.

**Stacking:** Duplicate applications do not add multiple 5-foot riders. Later application can refresh the endpoint but cannot refresh a consumed rider while continuously Staggered. A new condition episode after it fully ends may grant a new rider.

**Immunities and specific exceptions:** Forced movement still obeys obstacle, solid-matter and legality rules. A feature explicitly preventing forced movement can negate the movement despite Staggered.

**Explicit integration decisions:**

- NEW endpoint clarification: 'next turn' means the affected creature's next regular turn.
- NEW: +5 feet is consumed once.
- Core Guard paragraph 394: +2 AC against first attack before next turn and enable Interpose. NEW: Guard removed rather than paused, cannot regain during Staggered; consumed rider not refreshed by reapplication.

**Remaining wider integration work:**

- Full Guard/Interpose action review remains in combat; this condition now names the existing Guard benefits it removes.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 771, definition paragraph 772; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="stunned"></a>
## Stunned

**Preserved Core text:** Incapacitated, cannot move, fails Strength/Dexterity saves, attacks against have advantage.

**Effect:** The creature is Incapacitated, cannot move, automatically fails Strength and Dexterity saving throws, attack rolls against it have advantage, and it can speak only falteringly.

**Application:** Only an effect explicitly inflicting Stunned applies it; source-character hard-denial limits remain separate application rules.

**Duration and ending:** Use the applying effect's duration/repeat-save procedure.

**Stacking:** Does not stack.

**Immunities and specific exceptions:** Stun immunity blocks application. Incapacitated consequences apply, including no Bonus Action/Reaction and concentration ending under the shared rule.

**Compatible V6/source details:**

- V6 adds that the creature can speak only falteringly.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 773, definition paragraph 774; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="unconscious"></a>
## Unconscious

**Preserved Core text:** Incapacitated, unaware, drops held items, falls Prone, adjacent hits are critical.

**Effect:** The creature is Incapacitated, unaware of surroundings, cannot move or speak, drops held items, falls Prone, automatically fails Strength and Dexterity saving throws, attack rolls against it have advantage, and any attack that hits from within 5 feet is a critical hit.

**Application:** Applied by effects explicitly causing Unconscious, including the active 0-HP rules.

**Duration and ending:** Use the causing rule's endpoint. Healing above 0 ends only Unconscious caused solely by the 0-HP state; it does not remove an independent Unconscious effect.

**Stacking:** Multiple causes may coexist; the creature remains Unconscious until all relevant causes end.

**Immunities and specific exceptions:** An immunity to Unconscious blocks applicable external effects but does not necessarily override death/0-HP rules unless explicitly stated. Incapacitated consequences apply.

**Compatible V6/source details:**

- V6 adds cannot move or speak, automatically fails Strength/Dexterity saves, attacks against have advantage, and any hit from within 5 feet is critical.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 775, definition paragraph 776; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="unity-exposure"></a>
## Unity Exposure

**Preserved Core text:** Track exposure from 0-6. At thresholds, distinctions, memories, loyalties, and eventually identity begin to erode.

**Effect:** Use the provisional public score 0–6 table in CONDITION_RECOVERY_PLAYTEST.md:0/1 no generic penalty;2 -1 specific distinction Perception/Investigation;3 -1 INT/WIS checks;4 -1 INT/WIS/CHA checks;5 disadvantage those checks;6 disadvantage those checks and saves. Use current row only. Player agency remains.

**Application:** Only explicit effects such as reviewed substances, hazards or Director mechanics may alter Unity Exposure.

**Duration and ending:** Persists; only an explicit reviewed effect or successful three-day Anchor Project changes the score. Ordinary rest does not clear it.

**Stacking:** Exposure changes modify the single 0–6 track; cap at 6 unless an authoritative source explicitly allows another state.

**Immunities and specific exceptions:** An effect explicitly preventing Unity Exposure blocks only the exposure it covers.

**Explicit integration decisions:**

- NEW provisional public threshold/recovery mechanics, discussed with GPT; not recovered canon.
- Public score does not imply knowledge of hidden causes, truths, involuntary beliefs or identity deletion. Director handling remains separately packaged.

**Remaining wider integration work:**

- Review all Unity application sources and Director narrative threshold material separately; no source-approved numeric threshold table was recovered in the bounded searches.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 777, definition paragraph 778; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="withdrawal"></a>
## Withdrawal

**Preserved Core text:** Disadvantage on ability checks and RP recovery; severity depends on substance and duration of dependence.

**Effect:** The creature has disadvantage on ability checks. If an RP-recovery procedure actually calls for a roll, that recovery roll has disadvantage. The current deterministic Retune formula receives no invented numeric penalty from this wording. Oracle Revelation Charges are not RP and are unaffected.

**Application:** Applied for a named substance when its Addicted maintenance requirement is missed or another source explicitly inflicts Withdrawal. Record the substance/source separately.

**Duration and ending:** A legal maintenance dose suppresses that substance's symptoms for its current maintenance interval without removing Addicted. Reviewed symptom relief follows its printed duration. A successful dependence recovery project removes both named dependence and its Withdrawal. The generic condition has no extra numerical severity levels; a substance adds severity only where its reviewed card defines it.

**Stacking:** Separate substance Withdrawal records may coexist, but disadvantage on ability checks applies only once. Severity does not numerically stack unless a substance-specific rule defines it.

**Immunities and specific exceptions:** An effect explicitly preventing Withdrawal symptoms suppresses the condition within its scope but need not remove Addicted.

**Compatible V6/source details:**

- Dependence source: user needs a dose after each long rest or gains Withdrawal; treatment may use Medicine, Religion, Alchemy or a recovery project, while magic can remove symptoms without necessarily removing dependence.

**Source conflicts:**

- Current Retune is deterministic and has no RP-recovery roll on which disadvantage can operate.

**Explicit integration decisions:**

- NEW: a maintenance dose can end current Withdrawal symptoms while dependence persists.
- Integration decision: deterministic Retune is not numerically altered because 'disadvantage' has no roll to modify.
- Oracle RC explicitly remains outside an RP-only condition.

**Remaining wider integration work:**

- Review substance-specific additions individually; do not infer penalties for deterministic RP recovery or Oracle RC.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 779, definition paragraph 780; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).


<a id="wounded"></a>
## Wounded

**Preserved Core text:** Each Wound imposes -1 Constitution saves and reduces Hit Dice recovery; three Wounds is Critical.

**Effect:** Use the existing Core Wound records from the reviewed HP/Wound overlay. Each Wound gives -1 Constitution saving throws and reduces maximum Hit Dice recovered per long rest by 1. At three Wounds the creature is Critically Wounded under that overlay's Speed, healing-ceiling and failed-Wound-save rules.

**Application:** Wounds are gained only through the active Wound-trigger/save system or an effect explicitly granting a Wound. Do not separately add a second condition penalty merely because a source labels the creature Wounded.

**Duration and ending:** Each Wound persists until a reviewed treatment or effect removes that Wound. Removing a Wound also removes its linked Injury. Leaving three Wounds ends Critical state under the existing overlay.

**Stacking:** Wound records stack numerically according to Core. The current overlay allows 0-3 living Wounds; a failed Wound save begun at three Wounds is fatal instead of creating a fourth.

**Immunities and specific exceptions:** An effect explicitly preventing Wounds blocks only qualifying Wound gain within scope. Ordinary HP healing does not remove Wounds unless it explicitly says so.

**Source conflicts:**

- V6 Appendix has a separate temporary Wounded condition: cannot regain HP except magical healing/long rest, disadvantage Constitution saves, damage at 0 causes one death-save failure, ends on magical healing/long rest. Core owns this conflict for the current candidate, so that V6 temporary package is preserved but inactive.

**Explicit integration decisions:**

- Integration decision already reviewed: Core Wound records are the active meaning of Wounded in this candidate; the conflicting V6 temporary Wounded package is inactive and does not double-apply penalties.

**Remaining wider integration work:**

- Specific restoration effects that remove Wounds will be cross-checked during spell/item/condition integration.

Provenance: Core V2 `books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`, zero-based all-XML heading paragraph 781, definition paragraph 782; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).

## Verification limits

`tools/condition_playtest_rules.py` computes selected action restrictions, attack modifiers, Exhaustion maximum HP/Speed, Corrupted healing, Petrified resistance and Prone movement. It does not decide legal applications, actual visibility, immunities, all source durations, treatment inventory or every spell/class interaction. Run `tools/validate_condition_playtests.py` for scoped regression evidence. An absent automated helper does not make a written table procedure absent, and a passing helper test does not prove game-wide balance.
