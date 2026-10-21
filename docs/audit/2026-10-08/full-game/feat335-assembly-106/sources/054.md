# Combat feats

**Source-authored exact candidate; separate exact review pending. Selection/runtime disabled. Original catalogs unchanged.**

[Complete shared rules](SHARED_RULES.md) · [Finite supplements](SUPPLEMENTS.md) · [Spell payloads](SPELL_PAYLOADS.md)

Read every procedure with the complete shared rules. NEW identifies authored completions; old source alternatives remain preserved. The two deferred payloads are unavailable.

## Armor Crusher (`armor_crusher`)

**Prerequisite:** Level 7

After one of your own direct damage events deals positive resolved bludgeoning, piercing or slashing damage to a creature, you may apply Armor Crusher once that turn. NEW: any actual creature defense qualifies, including natural armor and unarmored defense; the feat does not require a removable suit. The triggering event finishes against its original AC. Apply a separate −1 AC layer through your next original regular start. Further applications from any owner never sum below −1; retain independent expiry records, so the penalty persists while at least one remains. Fully prevented damage does not trigger; temp-HP absorption of a positive resolved packet still does. Copied, reflected, transferred and ongoing periodic damage do not generate applications. Do not damage or regrade armor.

### Worked examples

An AC17 creature takes 4 piercing damage: the triggering attack used17; later attacks use16 until expiry.

Two owners apply the feat: AC falls only1. The later record can keep that same −1 after the first expires.

## Battlefield Commander (`battlefield_commander`)

**Prerequisite:** Charisma 15+, Level 12

Action, once per short rest: choose one to three willing allied creatures, including yourself, within30ft who can hear and understand the brief directive. Lock recipients and their order, spend the use, then resolve each sequentially. Each may spend its own available Reaction immediately for a separate floor(current relevant Speed/2)-ft movement-cost budget. Recheck hearing, willingness, position and capability at that recipient's resolution. Terrain and hazards apply; movement from this instruction provokes no opportunity attacks. Speed0 gives no movement. Declining or losing eligibility grants no replacement recipient and does not refund the commander; a recipient that does not move need not spend a Reaction. No ordinary movement/Action/BA resource is restored.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.

### Worked examples

The commander selects themselves and two willing hearing allies, spends the Action and short-rest use, then resolves their chosen order. Each moving recipient pays their own Reaction for half-current-Speed movement; the commander has no extra Reaction.

The second ally is incapacitated by a hazard while the first moves: skip that ally; the third may still react if legal.

## Berserker Rage (`berserker_rage`)

**Prerequisite:** Strength 16+, Level 9

Bonus Action, once per short rest: enter this distinct feat rage through your second future original regular-start marker; outside initiative12elapsed seconds. Each qualifying weapon attack hit during it adds one base weapon damage die, doubled as part of a critical. Melee and ranged weapon attacks qualify because the current effect says weapon attacks; unarmed attacks do not, and natural attacks require an actual weapon profile. Apply its −2 AC continuously. Repeated same identity cannot stack; independently active Aggressive stance's −2 AC also applies. NEW the rage ends early if you become Incapacitated. This is a rage for Frenzied Rage's operating trigger, but acquiring this feat alone does not satisfy Frenzied Rage's separately printed Berserker-feat-or-class-rage prerequisite. It supplies no +2 rage damage to replace and no resistance or spell ban.

### Worked examples

A 2d6 greatsword hit gains1d6; a critical rolls6d6 in total, plus unchanged flat modifiers.

Activation on own turn4 expires at start6, even if turn5 is skipped; an extra turn does not extend it.

## Bleeding Edge (`bleeding_edge`)

**Prerequisite:** Dexterity 14+, Melee

When your actual melee weapon attack critically hits a living non-bloodless creature, after the hit resolves apply feat.bleeding-edge in family.bleeding, stack group feat.bleeding-edge:<owner>. NEW physical type is slashing. It deals1d4 at each of the next three future target regular starts, then ends; applying during a start never adds an immediate tick. Same-owner reapplication refreshes three remaining ticks without adding a second instance; different owners retain competing groups under the existing highest-expected-damage/earliest-application arbitration. Losing due groups still spend ticks. Snapshot the ending Medicine DC10+your PB at application. Victim or adjacent helper may spend an Action with one usable hand and access to the injury, selecting this record before WIS Medicine; success ends that record only. No kit charge is required by this feat. Retain generic positive-potential magical-healing automatic cure for this ordinary Bleeding record. Critical dice do not double later periodic damage; no resource/attack procs from ticks. No positive-damage prerequisite is added beyond actual hit and bleedable body.

### Worked examples

At PB3, an adjacent Medicine total13 ends one selected owner's record; another owner's independent record remains.

A concurrent stronger Bleed wins two due starts. Bleeding Edge still uses those two ticks and has only one left.

## Brace for Impact (`brace_for_impact`)

**Prerequisite:** Constitution 14+

If you have undergone no actual positional displacement since your most recent original regular-turn start, spend Reaction when a direct damage event would damage you. NEW all voluntary, forced, carried and teleport displacement counts, even returning to the same square; standing, turning in place and a failed move do not. Before your first encounter turn, count displacement since encounter entry. Reduce one whole resolved incoming event by max(0,PB+CON modifier), after ordinary passive defenses and before temporary HP. Allocate reduction across components in their stable order, never below0; one attack's fire and slashing are one event, separate attacks are not. Do not re-mitigate a transferred packet that explicitly forbids recipient mitigation. This affects damage only, not attached conditions, sacrificed HP or state assignment. Paying with a zero reduction is allowed but does not create healing.

### Worked examples

PB3/CON2 reduces resolved8 to3 before tempHP; it does not subtract5 independently from each component.

You were pushed5ft and then returned5ft after your start. You cannot use the feat before the next regular start.

## Break Line (`break_line`)

**Prerequisite:** Dexterity 15+, Level 10

Once per turn during your own legal voluntary movement, declare crossing one hostile creature's occupied space whose size is no more than one category larger. You must have enough ordinary remaining movement cost and a visible or known legal unoccupied exit to traverse its entire occupied footprint; occupied terrain costs at least difficult. Before first entry, that creature may spend its Reaction for one legal melee opportunity attack against you, even though you are entering rather than leaving. All actual reaction, sight, reach and opportunity-immunity restrictions apply. If it hits, this passage fails: remain in your last legal outside space, spend the first attempted entry step's cost and the feat use. The hit's other consequences resolve normally. If it misses, declines, cannot attack or its opportunity attack is suppressed, proceed, paying actual traversal costs. Recheck the exit after interruptions; if traversal becomes impossible before entry, stay outside and spend the committed use. Do not willingly start a traversal without a complete legal route. Other creatures may make normal opportunity attacks. This does not shove or phase through a creature.

### Worked examples

A Medium rogue has20 movement cost left and crosses one Medium hostile square for10 then exits for5. The guard has no Reaction, so passage succeeds.

The guard's legal special attack hits. The rogue remains before the occupied square and spends10 cost for the attempted difficult entry; damage and the once-turn use remain.

## Bull Rush (`bull_rush`)

**Prerequisite:** Strength 14+

Once per turn, after you hit with a melee attack immediately following at least10ft of your own continuous voluntary movement in a straight line directly toward that target, choose this rider. NEW the approach must occur on that same actual turn, without intervening attack, action, turn or teleport; forced/carried displacement does not count. Melee weapon, natural, unarmed and actual melee spell attacks qualify. Target makes STR save DC8+PB+your current STR modifier. On failure push it5ft directly away and separately apply Prone. NEW no additional size cap is added because the feat omits one; actual immovability, anatomy/support and condition immunities still apply. A wall can stop the push without preventing Prone. A hit dealing0 damage can trigger. Resolve normal damage before this rider; if no creature remains, no further effect. No additional Action cost.

### Worked examples

A hit after10ft straight approach produces a failed save. A wall blocks displacement but the target still falls Prone if eligible.

A teleport of10ft followed by a hit does not meet the approach; neither does being carried forward by another actor.

## Cleaving Momentum (`cleaving_momentum`)

**Prerequisite:** Strength 16+, 2H Weapon

Acquire with STR16 and actual proficiency in a Two-Handed weapon. NEW triggering and follow-up attacks must both use an actual melee weapon wielded with two hands; a legal Versatile two-hand attack can operate the acquired feat. During your own turn, after your attack reduces a genuine hostile creature from positiveHP to0 after floors/replacements, you may spend your still-available Bonus Action before that turn ends for one melee weapon attack against a different creature in legal reach. Death is unnecessary; a surviving downed opponent qualifies. The second target need not be hostile under the printed another-creature wording. Normal damage, ammunition if relevant, hands and perception apply. No banked off-turn use and no additional Bonus Action; multiple drops only provide alternative triggers for that same wallet. Copied/periodic damage and reducing an already0 creature do not qualify.

### Worked examples

A greatsword drops a hostile to0 but the creature survives dying. One available BA can attack a second target.

The follow-up also drops its target. There is no second Bonus Action and thus no chain of free attacks.

## Close Quarters Combat (`close_quarters_combat`)

**Prerequisite:** Dexterity 14+

Your ranged attacks ignore disadvantage caused specifically by a seeing, non-Incapacitated hostile creature within5ft of you. This covers ranged weapon and ranged spell attacks. It does not remove long-range, unseen-target, Prone, restrained or other independent disadvantage. If any other disadvantage remains, apply ordinary cancellation. Making that ranged attack does not itself provoke an opportunity attack from any source that explicitly uses making the ranged attack as its trigger; it does not suppress a separate spellcasting, movement or other legal trigger. Current generic combat creates no opportunity attack just for making a ranged attack; do not add such a penalty for other characters.

### Worked examples

A nearby guard imposes the usual proximity disadvantage on a ray; this feat removes it.

A long-range bow shot with an adjacent hostile still has long-range disadvantage, even though proximity disadvantage is removed.

## Combat Intuition (`combat_intuition`)

**Prerequisite:** Wisdom 13+

While conscious, you cannot be surprised. NEW this suppresses any still-active surprise action/reaction prohibition while consciousness lasts, without granting lost actions or retroactive turns; other conditions still restrict you. The underlying first-turn surprise schedule is retained if consciousness changes again. Gain+1 AC during the encounter's first numbered round only. A late entrant in that round gains it only for the remainder; entering in round2 does not create a personal first round. The +1 is one feat modifier and needs no action; no extra Reaction is granted when surprise is prevented, only access to the normal resource if otherwise available.

### Worked examples

A conscious owner in round1 is not surprised and has+1AC. An extra turn during round1 still has the same bonus.

Joining combat in round3 grants no first-round AC, though conscious surprise prevention still applies.

## Combat Slide (`combat_slide`)

**Prerequisite:** Dexterity 13+

Once on your own turn, immediately before or after one weapon attack, move using a separate5ft movement-cost budget. NEW choose and declare the attack target before a pre-attack slide; ordinary attack range and other legality must hold after movement. You still pay the attack's normal Action/BA/Reaction source; the slide grants no attack. For pre-slide, reserve that attack, and if an interruption prevents it the slide and use remain spent. For post-slide, a hit or miss both qualify. Only the declared target cannot make opportunity attacks provoked by this movement; other foes may. Terrain costs, usable Speed, legal endpoints and inability to occupy another creature still apply. At Speed0 you may attack if otherwise legal but cannot slide. No banking or splitting the5ft into separate later moves.

### Worked examples

After missing a guard with a spear, move5ft on normal ground without that guard's opportunity attack.

A difficult5ft grid square costs10. The slide's5-point budget cannot enter it, and the feat does not double its budget.

## Crippling Strike (`crippling_strike`)

**Prerequisite:** Dexterity 14+, Melee

Once per turn when your attack hits using a weapon with Finesse OR a weapon classified as melee, reduce the target's current applicable Speed modes by10ft, minimum0, through your next original regular start. NEW a thrown dagger qualifies by both its melee classification and Finesse, even though its attack is ranged; a thrown nonfinesse melee weapon also qualifies by the literal melee-weapon branch. A longbow does not. Do not require positive damage. Same-identity applications across owners do not sum; retain independent expiries for one −10 layer. Other distinct Speed modifiers follow their actual stacking rules; apply numeric changes before halving and retain spent movement cost. This is not the Thief's Slow condition and grants none of that source's other effects.

### Worked examples

A thrown dagger hit lowers walking30 and flying40 to20 and30 until the owner's next regular start.

Two owners hit with the feat: Speed30 becomes20, not10; separate expiry records preserve the one penalty.

## Defensive Stance (`defensive_stance`)

**Prerequisite:** Level 6

NEW complete activation: when choosing your stance at the start of a regular own turn before using any stance benefit or moving voluntarily, choose Defensive Stance instead of a normal stance. No Action; one stance choice. Through your next original regular start, add floor(15% of your otherwise-current AC), minimum0, to AC. Compute the base after actual armor/shield/DEX/flat bonuses/penalties but before this or any other percentage-AC bonus; no percent-on-percent multiplication. Recompute when that underlying base changes, including conditional Guard. You cannot voluntarily change position by Speed expenditure, teleport or a feature while the current regular turn lasts; linked extra turns also retain the movement restriction. Standing/dropping Prone is allowed if ordinary budget/capability permits. Forced displacement remains possible and does not end the stance. Off-turn voluntary Reaction movement after that turn is allowed; AC lasts to expiry. It cannot coexist with Aggressive, Guarded, Mobile, Focused or Carrying because it occupies their stance choice, not a free extra buff.

### Worked examples

Underlying AC17 gains floor2.55=2, total19. The feat does not round to a3-point bonus.

A forced push during the stance moves the owner normally. They cannot then voluntarily teleport during their turn, but the push does not remove AC.

## Disarming Blow (`disarming_blow`)

**Prerequisite:** Strength 14+, Melee

On a hit with a melee weapon attack, before rolling damage, select one held reachable object and forgo one actual base-weapon damage die to attempt disarming it. NEW remove one die before critical doubling; a critical1d8 weapon forgoes its entire doubled base2d8, retaining lawful flat damage and independent riders. Never pay with a rider die, a die already spent on another feat, or a fixed-damage expression. The target chooses STR or DEX save against DC8+PB+the actual attack ability modifier. Resolve remaining hit damage, then the save if the creature still holds the object. Failure drops it into an adjacent legal unoccupied space you choose, otherwise its own space. No extra damage to object, severed curse or bond; actual non-droppable bonds prevent dropping. An object wielded with two hands is still one object. No new once-turn cap: each separately paid qualifying hit can attempt, but the chosen die is spent even if immunity prevents the result.

### Worked examples

A1d8 sword critical spends its one base die, leaving zero sword dice rather than one; STR modifier and a separately paid legal rider remain.

A target's bonded blade cannot drop. The attacker's declared damage die is still forgone; the bond is not broken.

## Double Tap (`double_tap`)

**Prerequisite:** Dexterity 14+, Ranged

After you take the Attack Action on your turn and make at least one attack with a weapon classified as ranged, spend your available Bonus Action that turn for one additional attack with a legal ranged weapon. NEW it may be a different ranged weapon and a different target; thrown melee weapons do not meet ranged-weapon classification. Supply actual ammunition, loaded state, reload/loading cadence and usable hands. Omit a positive ability damage modifier but retain a negative one, matching current two-weapon arithmetic; only a feature expressly restoring this attack's modifier can restore it. A two-weapon-only exception is insufficient. No attack is granted off-turn by a readied Attack; a linked extra turn may supply the trigger only if it has a legal Attack Action and Bonus Action, without refreshing any consumed shared allowances. This never grants an extra BA.

### Worked examples

A bow attack followed by a legal BA bow attack consumes two arrows; with DEX+3 the second damage omits+3.

DEX−1 still reduces the second attack's damage. Loading that permits only one shot in the relevant period is not bypassed.

## Draw Cut (`draw_cut`)

**Prerequisite:** Dexterity 15+

Once per encounter, when you legally draw a genuinely sheathed melee weapon as part of making a weapon attack with it, declare Draw Cut before the attack roll. NEW drawing uses the normal free object interaction or another explicitly granted draw permission; this feat grants no extra hand or interaction. The weapon must actually be secured in a sheath/scabbard, not merely dropped, held or conjured. A hit adds one actual base weapon die before critical doubling. A miss spends the declaration and encounter use. Resheathing, switching weapons, initiative exits and new turns do not refresh it. The attack may be a thrown attack with that melee weapon if drawing and throwing are otherwise legal. No attack Action or BA is supplied by the feat.

### Worked examples

Drawing a1d6 shortsword into a critical adds one base d6 and doubles both base dice for4d6.

After a missed Draw Cut, sheathing and drawing a second weapon during the same fight cannot restore the use.

## Exploit Weakness (`exploit_weakness`)

**Prerequisite:** Level 7

At attack-roll resolution, before that attack's damage, check whether the actual target's normalHP is strictly below half its current effective maximum:2×HP<maximum. TemporaryHP does not count as normalHP and does not change the comparison. If true, your weapon attack critically hits on a kept natural19 or20; a19 must still meet AC. Choose the broadest actually applicable critical range among this and other features; never add their range expansions. The Director can resolve this hidden predicate without disclosing numericHP or granting a diagnostic scan. A target that falls below half only from the current attack does not retroactively make that hit critical. A legal critical-if-hit feature can still apply independently; critical dice double once.

### Worked examples

HP10/max21 qualifies; HP11/max21 does not. Ten temporaryHP does not change either result.

A natural19 totals18 against AC20: it still misses, even when the target is below half.

## Feint (`feint`)

**Prerequisite:** Dexterity 14+, Charisma 13+

NEW complete procedure: Bonus Action, one perceived hostile creature within30ft that can perceive your deliberate threatening movement; oppose your CHA Deception with its WIS Insight. Higher total wins; ties preserve state, with no task-degree/natural shift. On success, apply−2AC against your next attack on that creature before your next original regular start. Declare the affected attack before rolling; it consumes the feint hit or miss. Failure has no effect. Only one unspent Feint per owner; a new successful Feint replaces your prior mark. Multiple owners can each set their own next-attack records, but one attack never receives more than one−2 Feint layer. Feint does not compel beliefs, create a universal off-guard condition or lower AC against other attackers. No rest use cap; the real BA and opposed check fund each attempt. If a target cannot perceive the act, it is ineligible rather than automatically beaten.

### Worked examples

Deception17 defeats Insight14. The owner's next attack checks AC16 instead of18 and consumes the mark even on a miss.

An ally attacks first: that attack gains no Feint bonus and does not consume the owner's mark.

## Grappler (`grappler`)

**Prerequisite:** Strength 14+

Add+4 to your actual STR Athletics checks initiating or maintaining an ordinary grapple you control. A creature using the ordinary opposed Escape Action to escape your grapple takes−4 on its chosen Athletics/Acrobatics roll. Your opposed maintaining roll also gets+4; these are different sides of the expressly printed contest. NEW this gives no+4 to your own escape from someone else's hold, no penalty to a defender's initial resistance, and no effect on spell saves or teleports that legally escape without that opposed contest. Reach, one-size-larger cap, actual grasping hand, attack replacement and Escape Action remain unchanged. Multiple grapplers have separate holds and contests; do not multiply−4 from another grapple that is not the selected escape. PB/expertise is included normally once; opposed ties preserve the hold and have no critical task effects.

### Worked examples

Initiation Athletics12 becomes16; defender Acrobatics15 remains15, so the hold is established.

For escape, defender total18 becomes14 while the owner's maintenance13 becomes17. An unrelated second grappler adds no further−4.

## Lunge (`lunge`)

**Prerequisite:** Strength 13+, Weapon Proficiency

Once on your own turn before selecting the target of one melee weapon attack, increase that attack's reach by5ft. Use its actual weapon reach and body profile, then restore ordinary reach immediately after the attack resolves or is interrupted. The declaration consumes the allowance even on a miss. It grants no attack, extra movement, general threatened space, grapple reach or persistent opportunity reach. A later off-turn opportunity attack uses ordinary reach unless its own source specifically grants an exception. A natural weapon only qualifies if actually a weapon attack. You must possess an actual weapon proficiency to acquire the feat, but use with another unproficient legal weapon does not grant PB.

### Worked examples

A5ft sword can attack one target10ft away; afterward it still threatens only5ft.

A10ft reach weapon can make one15ft attack. The target moving from15 to20ft afterward does not trigger that weapon's normal opportunity reach.

## Overrun (`overrun`)

**Prerequisite:** Strength 15+

When you legally take Dash, activate Overrun for that turn's subsequent ordinary movement; Dash supplies its normal increased cap, not a second separate movement grant. You may attempt passage through actual creatures at most one size larger, allied or hostile. NEW each distinct creature may be challenged once that turn, with no duplicate attempt from extra Dashes. Before entering its first occupied space, it makes STR save DC8+PB+your STR; a willing ally may elect failure as this feat's explicit exception. On failure push it5ft to a legal adjacent side destination you choose that clears the necessary passage. Success, anchoring, or no legal clearing destination blocks this special passage; remain outside and spend the attempted first entry step's ordinary cost. Do not start without enough budget for a complete legal path/end. The feat does not suppress opportunity attacks. A creature already passable under ordinary size rules can instead be crossed normally without invoking the feature. It grants no Prone, damage or ability to remain in occupied space.

### Worked examples

A Medium runner Dashes and a Large guard fails; a legal5ft side space clears the route, so the runner proceeds using ordinary cost.

A guard fills a narrow passage with no side destination. Failure alone cannot teleport it through the wall; Overrun passage stays blocked.

## Power Attack (`power_attack`)

**Prerequisite:** Strength 14+

NEW complete procedure: before each melee weapon attack roll using STR for that roll, you may take−2 to that roll. If it hits, add floor20% of that attack's eligible native weapon damage as defined in shared arithmetic. This is an optional per-attack trade, no Action or rest charge. Actual weapon proficiency is not granted; finesse choosingDEX, ranged attacks and melee spell/unarmed attacks do not qualify. Preserve critical dice before calculating the percent bonus; no benefit on a miss. Power Attack and Precision Strike's attack trade are mutually exclusive choices on the same attack, not cumulative penalties for stacking both percent bonuses. Giant Slayer or another genuinely independent eligible percent source adds its separately rounded bonus from the same base, without multiplication. Original−2/+20% stays preserved.

### Worked examples

Eligible native weapon damage19 yields+3, total22 before defenses. The attack roll still suffers−2.

Against a Large creature, native20 with both Power Attack20% and Giant Slayer20% totals28, not28.8 or29.

## Precise Shot (`precise_shot`)

**Prerequisite:** Dexterity 14+

The current combat guide imposes no general disadvantage just because an ally is adjacent to the target; retain that printed historical removal as a compatibility clause if a specifically enabled source ever supplies it. NEW useful completion for this candidate: your ranged weapon or ranged spell attack ignores half cover when that half cover is supplied solely by one or more allied creature bodies in the shot's actual path. It ignores neither terrain cover, three-quarters/total cover, hostile-body cover, nearby-hostile disadvantage, nor long-range disadvantage. Compute remaining actual cover normally after disregarding those allied bodies; never lower a real wall's cover. This does not make firing through solid or untargetable positions legal and does not acquire a class Sharpshooter feature.

### Worked examples

An allied frontliner is the only cause of half cover: the shot ignores that+2AC.

The target stands behind a low stone wall and beside an ally. The wall's half cover remains.

## Precision Throw (`precision_throw`)

**Prerequisite:** Dexterity 13+

When you make a ranged attack by actually throwing a weapon whose current profile has Thrown, gain+1 attack and double its printed normal range, capped at its actual printed long range. Preserve long range unchanged. NEW no-long-range profiles retain their hard maximum; the feat cannot invent a missing legal interval. Melee use of the same weapon gains nothing. Improvised objects require an actual Thrown weapon profile supplied by another rule; merely hurling an object does not acquire the property. Distinct eligible Weapon Focus+1 may add under its separate feat family; duplicate Precision Throw never stacks. Physical quantities, recovery, hands and ammunition remain actual.

### Worked examples

A20/60 dagger becomes40/60 for throwing and gains+1attack; a melee stab does not.

A hypothetical40/60 Thrown profile becomes60/60, with no attacks beyond60.

## Punishing Blow (`punishing_blow`)

**Prerequisite:** Strength 13+

Once per turn, on one of your own direct attacks that hits a genuine enemy already Stunned or Prone immediately before damage, add your current PB as a flat damage component of that hit's native type. Choose one native type if the attack has several; if it deals no native damage, no additional damage is created. NEW all actual attack types qualify, including spell, natural and unarmed, because source says deal additional damage without weapon restriction. No application from a save-only effect, periodic tick, transfer, copy or rider that does not itself attack. The same hit cannot first inflict Prone/Stunned and retroactively qualify. The bonus is part of the hit before defenses, cannot double on a critical, and applies once across multi-type components.

### Worked examples

PB4 adds4 to a critical against a creature already Prone; it does not become8.

Bull Rush knocks the standing target Prone after damage. That same attack does not receive Punishing Blow retroactively.

## Reckless Swing (`reckless_swing`)

**Prerequisite:** Strength 15+

Before any melee weapon attack roll, you may declare Reckless Swing. That one attack gains advantage and adds one base weapon damage die if it hits; critical doubles that additional attack die. Regardless of hit, miss or advantage cancellation, all attacks against you have advantage through your next original regular start. Repeated declarations on separately legal attacks can each supply their one die but do not stack attacker advantage or create attacks; overlapping vulnerability records retain the same next-start deadline. This is not a rage and has no resistance or ability-score substitution. Spell, thrown ranged and unarmed attacks do not qualify; actual natural weapon melee attacks do. Ordinary costs, conditions and damage-source restrictions remain.

### Worked examples

A longsword1d8 attack gains1d8; if critical, roll4d8 plus flat modifiers.

You attack an unseen target: advantage and disadvantage cancel, but the extra die on a hit and attacks-against advantage still apply.

## Riposte (`riposte`)

**Prerequisite:** Agility 15+, Melee Proficiency

NEW acquisition bridge: the legacy Agility15 means DEX15 for this feat only; Melee Proficiency means actual proficiency with at least one melee weapon. After a hostile melee attack against you misses while your active Dodge actually applies to it, OR after an actual sourced Parry/Deflect effect expressly turns that attack into a miss, you may spend your available Reaction to make one legal melee weapon attack against that same attacker in reach. No movement or extra Reaction is granted. A parry that merely reduces damage is insufficient; missing for ordinary AC without qualifying Dodge/Parry is insufficient. If the defensive effect already used your only Reaction, you cannot also riposte. A permitted additional Reaction must explicitly allow an attack; defensive-only grants cannot pay. Apply shared causal-root prohibition on counterattack chains. Once per original regular-start interval even if another source grants extra attack-capable Reactions.

### Worked examples

While Dodging with Speed30, a seen adjacent enemy misses; spend the available Reaction for one weapon attack.

A paid parry used the only Reaction to cause a miss. No Reaction remains for Riposte; reducing a hit to0damage would not qualify anyway.

## Savage Momentum (`savage_momentum`)

**Prerequisite:** Strength 14+, Melee

Track a consecutive direct melee-attack hit chain for each owner during one encounter. Every actual melee attack you make advances the event sequence: a hit on the same current target increases the count; a miss or attack directed at a different target ends the old chain, and a hit on the new target starts a new count1. NEW any intervening nonmelee attack also breaks the chain; movement, spellcasting without attacks and nonattack actions do not. Own/off-turn melee attacks participate, but copies/periodic events do not. Once per turn, before rolling a qualifying hit's damage, add min(PB, prior consecutive hits on that target) as a flat native-type bonus. Only declare when at least one prior hit exists; spending on this hit prevents spending on a later hit that turn. The chain persists across regular turn boundaries but ends on target death/removal, encounter conclusion, or loss of that actual creature identity. Transformation of the same surviving identity retains it if target continuity is real.

### Worked examples

Three consecutive hits on one foe at PB3 permit choosing+1 on hit2 or+2 on hit3 that turn, not both.

After two hits, a missed opportunity attack breaks the chain. The next melee hit starts at1 and has no prior-hit bonus.

## Shattering Smash (`shattering_smash`)

**Prerequisite:** Strength 16+

On a melee weapon attack hit against a creature receiving an actual wielded shield AC contribution or a sourced current physical-block benefit, before rolling damage forgo one base weapon die under the same pre-critical payment contract as Disarming Blow. NEW save is STR DC8+PB+the actual attack ability modifier. Resolve remaining damage, then on failed save suppress either the chosen shield's entire AC contribution (including its own enhancement) or one selected block benefit through the target's next original regular start. No destruction, durability loss, forced drop or suppression of unrelated item traits; independent magical barriers/unarmored formulas remain. A shield-dependent feat AC bonus is suppressed while its shield cannot supply defensive contribution. Physical block means a named sourced defense actually interposing a held body/object; ordinary armor, cover terrain and taking Dodge do not alone qualify. Same-identity suppression does not multiply, and separate expiries remain. You cannot spend the same die on another rider.

### Worked examples

A shield contributes2 plus1enhancement. Failure suppresses those3 until the target's next regular start; the shield is not broken.

A one-die sword cannot pay both Shattering Smash and Disarming Blow from the same die. A two-die weapon may pay distinct dice if both targets/effects qualify.

## Shield Bash (`shield_bash`)

**Prerequisite:** Strength 13+

After you take the Attack Action on your own turn while actually wielding a usable shield, you may spend BA that turn to bash a creature within5ft. NEW this is a melee weapon attack using STR, adding PB if you are proficient with shields; the shield remains an armor/shield object, not a new purchasable weapon identity. It deals1d4+STR bludgeoning, minimum0, with ordinary critical doubling. A buckler counts only if its actual profile allows a striking shield body; this feat does not conjure a free weapon or bypass the shield hand. Once per short rest, after a bash hits and before damage, spend the stun use; target CON save DC8+PB+STR after damage. Failure applies Stunned until the target's next original regular start. Immunity and the source-character hard-denial cap apply; spent use is not refunded. This endpoint deliberately does not steal the target's whole next regular turn. No grant of another BA or off-turn bash.

### Worked examples

STR+3/PB3 bash attacks at+6 for1d4+3; the optional stun save isDC14.

A stun applied just after the enemy's turn can block intervening Reactions, but expires at that enemy's next start before voluntary decisions.

## Shield Expert (`shield_expert`)

**Prerequisite:** Shield Proficiency

While proficiently wielding a usable actual shield that supplies its defensive contribution, gain+1AC as this feat's separate modifier; duplicate copies do not stack. If you succeed on a DEX save whose printed ordinary success would deal half damage, you may spend Reaction before damage to take0 from that save's damage event. NEW your shield must physically interpose against the effect's actual incoming origin/line; it cannot block an effect originating inside your body or bypass an express shield-ignoring clause. Area eligibility follows actual origin-to-target line and the same cover geometry; an all-around explosion is not automatically unblockable if a real incoming line can be interposed. Other conditions or nondamage consequences remain. Failed saves receive no reduction; a successful reroll can qualify before damage, consuming only one Reaction. If another feature already made the damage0, spending this Reaction is unnecessary.

### Worked examples

A successful DEX save would halve12fire to6; a legal shield interposition Reaction changes that damage to0.

A failed save still deals normal failure damage; this feat does not turn failure into a success or remove an attached condition.

## Sure Shot (`sure_shot`)

**Prerequisite:** Dexterity 14+, Ranged Proficiency

For your ranged weapon attacks, ignore up to2 points of actual target AC attributable to worn physical armor or ordinary cover, combined rather than2 from each. NEW compute physical armor contribution as max(0, the actual suit base AC including its grade minus10), excluding all DEX contribution and magic enhancement; do not count an unarmored/natural-armor formula, shield, independent feat AC or magical enhancement as suit contribution. An actual magical armor enhancement is not removable here; physical base armor still is. Ordinary half/three-quarters cover can supply removable points; a magical barrier's cover/AC cannot. Choose eligible cover contribution first, then suit, up to2 total. This is a target-specific attack comparison, not a lasting AC reduction. Total cover remains untargetable even if physically supplied. Spell attacks and a thrown melee-class weapon are not ranged-weapon attacks for this classification unless its actual profile also says ranged.

### Worked examples

A chain-armored target with actualAC16 is compared at14 for a legal ranged weapon attack.

Leather base11 plusDEX5 givesAC16 but only1 point of physical armor: compareAC15, preservingDEX5. Ordinary half cover can instead supply2; total cover still blocks, and a magical barrier's+2 stays.

## Tactical Flanker (`tactical_flanker`)

**Prerequisite:** Intelligence 12+, Melee

NEW feat-only geometry: you and one other willing allied, non-Incapacitated creature each threaten the same enemy with an actual legal melee attack, and the straight segment joining your occupied-space centers crosses the interior of that enemy's occupied footprint, placing you on opposite sides. Measure actual occupied bodies on the current map; a large creature needs opposite sides of its whole footprint, not merely two nearby squares. Both participants must perceive the target and be able to attack it; total cover or unusable reach prevents flanking. This geometry itself grants no universal advantage. Once per turn, when either participant hits that enemy with a melee attack, you may assign your feat allowance to add1d6 of one native damage type to that hit before damage is rolled. No Action/Reaction is required, but you must be conscious and able to coordinate. One successful attack may receive only one Tactical Flanker die across all owners; choose its funding owner before rolling. A critical doubles this attack rider die. Misses spend nothing; using your allowance on an ally prevents using it again on your own hit that actual turn. Perception/reach/geometry must hold at the hit.

### Worked examples

Two conscious allies threaten opposite sides of a Medium foe. One owner funds1d6 on the other's hit; a critical makes that rider2d6.

Three feat owners surround a foe. The same hit still receives only one Tactical Flanker die, with one chosen owner's allowance spent.

## Target Mark (`target_mark`)

**Prerequisite:** Wisdom 14+, Ranged

Bonus Action, once per short rest: while holding an actual usable weapon, choose a creature you can see within its current melee reach or printed maximum ranged range, with line of effect. A thrown weapon uses its actual range; ordinary long-range disadvantages remain. Record the chosen weapon only to establish activation range; stowing it later does not end the mark. For1minute, the first attack against the marked creature by each creature currently allied to you, including yourself, gains+1 to hit. This is once per ally identity for the entire mark, not per turn, and is consumed by that attack even if it misses. You are an eligible ally for your own mark. A creature's later alliance change does not reset its used identity; a newly arriving genuine ally can use its own first attack. Only one mark per owner; replacement, owner death or expiry ends the old record. NEW owner incapacitation does not end an existing mark. No continuous range/tether after activation and no vision/targeting permission is granted. Multiple marks never give more than+1 to the same attack; all applicable unspent first-attack entitlements for that attacker consume on that first event.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.
NEW weapon-range completion: at activation use an actually held, usable weapon’s current reach or printed ranged range, including a melee weapon’s reach; a ranged weapon is not mandatory. Long range does not remove its ordinary disadvantage. Marking does not grant an attack, visibility or line of effect. The mark’s +1 applies to each qualifying ally’s first attack against that target, including the owner’s. Multiple marks of this same feat give one+1 and consume all applicable first-attack entitlements on that event.

### Worked examples

Holding a usable melee weapon with5ft reach, the owner can mark a visible legal creature5ft away. Their own first attack against it gains+1 and spends their mark entitlement; stowing the weapon later creates no new activation range or attack.

Two commanders mark the same target. An ally's first attack gains+1, not+2, and consumes that ally's first-attack entitlement in both marks.

## Unstoppable Force (`unstoppable_force`)

**Prerequisite:** Strength 14+, Level 8

Whenever your own direct legal effect pushes or knocks a creature a positive specified distance away from you or along its printed outward direction, increase that displacement by5ft. It can modify a weapon, ordinary maneuver, spell or class effect if you are the actual source; not a companion's own effect, pull, teleport, fall, current, carried movement or copy/transfer. Preserve its original size/eligibility/path. Add the5 once per displacement event; same-family copies do not add further5. The final movement still stops at walls, anchors and illegal positions. Once per turn, if that same displacement-producing effect has an actual STR/DEX/other save which the target fails by5 or more, also apply Prone independently of blocked displacement. No save is invented for an ordinary opposed Shove; its numerical contest difference is not a save failure margin. Automatic failure has no numerical margin unless its source explicitly says otherwise. If an original effect already applies Prone, do not duplicate it.

### Worked examples

Bull Rush's failed save pushes10ft instead of5; a wall at5 stops it there, but the original Prone still applies.

An ordinary Shove contest succeeds by7. Its push grows to10ft, but no fail-by5 save exists to add Prone.

## Volley (`volley`)

**Prerequisite:** Level 8

NEW full completion: Action, once per short rest, wield a loaded/properly supplied bow using arrows and choose a visible point within that bow's actual normal range and line of effect. Select up to PB distinct perceived creatures in a10ft-radius area around that point, each independently in normal range and with a legal shot. You may exclude allies; no hidden-target scan or compulsory friendly fire is added. Lock targets/order, spend the use and one actual arrow per selected target, then make one separate normal ranged weapon attack against each. Apply actual AC, cover, proficiency, crits and ordinary native bow damage to each; there is no area save/DC or shared damage roll. Extra Attack does not multiply this special Action. Each target at most once; newly entering creatures cannot replace lost targets. A target becoming illegal before its shot is skipped and its committed arrow remains spent. Interrupted remaining shots lose the use and committed ammunition. Loading/reload and all other item restrictions remain, so a weapon that cannot fire the necessary arrows cannot declare that many shots. It is a special Volley Action, not Attack Action for Double Tap or Eldritch Combat.

### Worked examples

PB3 with a bow selects three enemies and commits3arrows; roll three separate attacks and damage only actual hits.

A wall gives one target total cover before its shot. Skip it without a replacement target or arrow refund; the other legal shots remain.

## Weapon Finesse (`weapon_finesse`)

**Prerequisite:** Dexterity 15+

For a melee attack normally using STR, you may use DEX instead for the attack roll only. NEW this includes actual melee weapon, natural and unarmed attacks, but does not replace a spell's designated casting ability or a special attack expressly locked to another stat. Damage still uses its original ability unless the weapon's actual Finesse property or another feature independently changes damage too. ChoosingDEX here does not grant the Finesse property, change weapon weight/hands/reach, make a Heavy weapon light, waive STR/size requirements, or qualify for a STR-attack-only Power Attack. Actual PB requires actual proficiency as before. Source attack-modifier-dependent save DCs, such as Disarming Blow, use the actual DEX attack modifier when this swap applied; STR-fixed feats retain STR.

### Worked examples

A longsword attack may useDEX+4 to hit while damage still addsSTR+1.

A dagger already possessing Finesse can independently useDEX for both; the feat is not the reason that dagger's damage changes.

## Weapon Mastery (`weapon_mastery`)

**Prerequisite:** Proficient, Level 6

At acquisition, choose one actual weapon profile/type in which you are proficient; permanent choice, nonrepeatable. At total character level6+, attacks with that type have critical range19–20 instead of the ordinary20. NEW the printed+1 range is one downward threshold step from the ordinary20, not an additive modifier on another expanded range. Compare all applicable actual critical ranges and use the broadest, consistent with reviewed Core. Natural19 must still meetAC; natural20 retains its automatic-hit rule. Melee or thrown use of the chosen weapon type qualifies, but improvised use without that profile does not. A specific natural weapon may be chosen only if it is a genuine proficient weapon profile, not all natural/unarmed attacks by umbrella label. No external weapon-mastery maneuver system is imported.

### Worked examples

Chosen longsword natural19 totaling21 againstAC20 is critical; totaling18 misses.

Weapon Mastery plus Exploit Weakness still yields19–20. An independently granted18–20 range stays18–20, not17–20.

## Whip Control (`whip_control`)

**Prerequisite:** Dexterity 15+, Whip

With actual Whip proficiency, wielding a usable whip, replace one attack of your Attack Action with one control attempt against a creature within the whip's actual melee reach. Choose disarm or trip before the roll. NEW make one weapon check d20+the whip's actual attack ability modifier+PB against the target's chosen STR Athletics orDEX Acrobatics total; opposed ties preserve state. This deals no damage, cannot crit, and is not a hit for on-hit riders. Trip requires target no more than one size larger and on success applies Prone subject to immunity/support. Disarm requires one actual reachable held object; on success choose a legal adjacent unoccupied drop space, otherwise the target's space, respecting real non-droppable bonds. No rest cap, but each attempt spends one actual Attack Action attack. Whip reach does not create a grapple or long-term restraint. Lunge modifies one melee weapon attack, not this check, so does not extend the control reach.

### Worked examples

A whip at10ft reaches a Large enemy. Weapon check18 beats Acrobatics15 and trips it without damage.

An opposed tie leaves a held sword in place. The attack replacement was spent and no hit-trigger damage occurs.

## Whirlwind Striker (`whirlwind_striker`)

**Prerequisite:** Level 10

NEW complete interpretation: surrounded means at least two different conscious hostile creatures within5ft of you, on opposite sides under Tactical Flanker's center-segment geometry, each currently able to attack you in melee. While that predicate holds, gain+1AC as an explicit conversion of the source's undefined+5% evasion; this is not literal5%damage reduction or a separate avoidance roll. Once on your own turn, after your melee weapon attack hits a creature while surrounded, you may deal a cleave packet to one different perceived hostile creature within the actual reach of that same weapon. Amount is floor10% of that hit's eligible native weapon damage before percentages/defenses; allocate native types as shared arithmetic. No second attack roll, no new critical and no on-hit riders/resources from this derived packet; ordinary recipient defenses apply. The primary attack can be fully mitigated and still supply its legal pre-defense native amount, but a missed attack cannot. Cleave needs real reach/line, deals0 if the rounded amount is0, and cannot itself cleave or trigger a drop-generated attack/heal. Losing surrounded geometry ends AC immediately.

### Worked examples

Two opposite adjacent melee foes qualify; a native19-damage hit yields a1-damage cleave packet to one other legal foe.

One surrounding enemy becomes Incapacitated. The+1AC ends immediately; a later hit cannot use this feat's cleave until the predicate returns.

## Eldritch Combat (`eldritch_combat`)

**Prerequisite:** Spellcasting ability, proficiency with martial weapons

Acquire only with a real spellcasting route and actual martial-weapon proficiency. NEW read1st-level as rank1 for this feat only. Once on your own regular-turn interval, when you take Attack Action and complete its attack sequence, append one actually available Action-time rank0 or rank1 spell with literal Touch or Self range as part of that same Action. You must have hit a creature with at least one of those attacks if choosing an external Touch target; that exact hit creature must also be a legal sole recipient of the spell. A Self spell must actually target only you, not a cone/area originating from Self that independently targets others. Spell must be acquired/prepared on a legitimate route with real level/rank access, RP or finite charge, components/hands/focus, target consent where required, concentration, Dissonance/Refrain, casting prohibitions and interruption. No normal casting cost is waived. An attack hit does not substitute for a spell's own required attack/save. Longer spells, BA spells and Reaction spells are not compressed by this grant. Separately, once per SR after your melee weapon attack hits, you may append one legitimately available Action-time Touch spell of any legally accessible rank to that same sole target without an extra Action; this can occur off-turn. NEW both modes share at most one embedded cast per actual regular creature turn and cannot be combined on the same hit/Action. Spend SR use at casting commitment, even if countered. These appended castings do not provoke opportunity attacks solely for casting/performing the appended attack-spell operation, but movement has ordinary triggers. Neither casting may create a further Eldritch append from attacks in its own causal root. Actual source-specific secondary/resource restrictions remain; no prestige class is acquired.

### Worked examples

After a successful sword Attack, a legitimately prepared Touch rank1 spell can target that hit creature, paying actualRP/components; the sword hit does not make its spell attack automatically hit.

An opportunity sword hit may use the separate SR Touch cast if legal and unspent. A Touch spell with a1minute casting time remains ineligible.

## Favored Enemy (Dragon) (`favored_enemy_dragon`)

**Prerequisite:** Proficiency in Survival, level 5+

Use actual supplied creature-type/tag facts: Dragon and expressly recorded dragonkin qualify for the+2damage and knowledge clauses; do not infer these tags from a humanoid ancestry name or settle origins. Add+2flat once per own direct damage event against a qualifying creature, of one native type, before defenses; no copied, periodic, reflected or controller-owned companion event. Advantage applies to genuine Survival tracking/ecology checks and NEW INT Nature checks representing the source's undefined Lore for physical draconic ancestry traits, breath type and lair habits; Arcana/History can use their actual separate task if relevant but receive no automatic substitute proficiency. NEW in initiative spend Action to observe a visible dragon within60ft, outside initiative1minute; DC=10+ceil(actualCR), or15 when noCR exists, adjusted only for explicitly established concealment of facts. Success gives one useful actually available requested fact, not sealed origins. On such success against a visible actual Dragon, brief other willing allies within30ft who can perceive/understand you; you and those fixed recipients gain+1 to saves against that individual dragon's breath through encounter end. Same feat family does not stack and later entrants require a new successful actual read/brief. Fear caused specifically by a dragon's presence lasts at most through your next future original regular start, then that source record ends; other fear remains. Once per SR, no Action during your movement while actually pursuing that dragon, ignore difficult-terrain movement surcharge caused by its real lair hazards through the current turn's end (outside initiative6seconds). Hazard damage/saves and impassability remain. No real bestiary record is retyped by this proposal.

### Worked examples

A CR7 Dragon observationDC17 succeeds; three briefed allies within30 gain+1 against that dragon's breath for the encounter.

Ignoring acidic-pool difficult terrain while pursuing the dragon removes movement surcharge only. Acid damage and other actual pool checks still resolve.

## Frenzied Rage (`frenzied_rage`)

**Prerequisite:** Constitution 15+, Berserker feat or class rage ability

Acquire with CON15 and the actual Berserker feat or an actual class feature expressly granting a rage state. No name-only qualification from Berserker Brew, Mooncursed, a prestige lineage or a damage buff. While in an actual acquired Berserker rage, replace its+2 melee bonus with+3 on melee weapon attacks; for any other qualifying rage lacking that+2, NEW grant+3flat melee-weapon damage as this feat's own family, without replacing separately rolled dice. Do not add+3 on top of the same Berserker+2. Berserker Rage CF-03 is an operating rage once this feat was legally acquired by its printed prerequisite, but not an acquisition substitute. Once per turn after your melee attack reduces an independent meaningful hostile from positiveHP to0, choose EITHER one immediate additional melee attack (NEW only on your own turn) OR extend that same currently active rage's time endpoint by one original6second round. Extra attack requires real reach/target/weapon/capability and creates no Action/BA; shared causal limits prevent drop-trigger attack chains. NEW at most three time extensions per single rage use; non-time endings such as incapacitation or missing upkeep remain. Once per rage, on your turn spend BA to charge along a declared straight legal route with a separate current walking-Speed movement-cost budget, through at most three hostile creatures no more than one size larger. Recheck a complete legal unoccupied endpoint before starting, pay occupied-space difficult cost and normal hazards/opportunity attacks. Each crossed creature once makesCON save DC8+PB+STR; failure applies Dazed until its next future original regular end. No damage/Prone/push is implied. If the route is interrupted, stop in the last legal space; already crossed targets remain affected and use stays spent. It cannot force passage when there is no legal complete crossing route.

### Worked examples

Berserker's+2 becomes+3, not+5. A drop can fund one extra own-turn attack; a drop from that extra attack cannot spawn another.

After three accepted extensions (+18seconds), a fourth drop cannot extend that same rage further. Incapacitation still ends a rage that has that endpoint.

## Giant Slayer (`giant_slayer`)

**Prerequisite:** Precision Strike or level 8+

Acquire with actual Precision Strike OR total level8. Against actual Large-or-larger creatures, add floor20% of each own direct damage event's eligible native amount before defenses, using shared noncompounding percent arithmetic. This broad damage clause includes own actual spell and weapon components but not periodic/copy/reflection/transfer or companion-owned attacks. Once per SR after a melee attack hits a Huge-or-larger creature, before damage declare the cripple use; after damage halve all its current Speed modes through its next future regular end, retaining spent movement cost. NEW no additional save is invented; same feat family halves once and actual immunities/specific movement protections apply. When a Huge-or-larger enemy misses you with a melee attack, you may spend Reaction for a separate5ft movement-cost step, then, only if that creature is within your own actual melee weapon/natural/unarmed reach and line, deal1d6 direct damage of that legal attack profile's native physical type (bludgeoning for unarmed) without an attack roll. You may step0 if already in reach; normal terrain/opportunity attacks/Speed restrictions apply. If the step cannot bring it into your reach, do not start this Reaction. The original source wording about stepping into its reach does not let you strike from beyond your own reach. It then has disadvantage on its next attack against you before its next future regular end, consumed hit or miss. Direct reaction damage is not a hit/critical, cannot start attack/heal/resource chains, and receives no added Giant Slayer percent because it is this feat's derived reaction packet.

### Worked examples

A native27-damage hit against Large adds5 for32 before defenses, independently of other eligible percent sources.

A Huge enemy misses from15ft away while your reach is5. A5ft step cannot reach it, so this Reaction is unavailable; its own15ft reach is not yours.

## Life Drinker (`life_drinker`)

**Prerequisite:** Dark Affinity or Hemocraft

Acquisition requires the exact source feat dark_affinity OR hemocraft, legitimately acquired under its eventual reviewed procedure; neither is silently granted or approved here. NEW finite Life Drinker Recovery Reserve=2×total character level, initially full on feat acquisition and refilled only by a completed LR. Level increases raise capacity without refilling current reserve; capacity reductions clamp without damage. This is a distinct personal feat reserve, not Mutation Recovery Reserve. After your direct melee critical against an independent meaningful hostile resolves, one healing event has base floor(actualDamageDealt/2), using the reviewed metric tempAbsorbed+actualHpDamage with no overkill, floor-protected or state-assignment loss. After your direct melee attack reduces such a hostile from positiveHP to0, a separate healing event has base current total level. NEW resolve critical healing then drop healing if both trigger, spending actualHP restored from the same finite reserve; available reserve caps each after ordinary healing modifiers/prohibitions/max/Critical ceiling. No healing on dead self, no Wound cure, resurrection, copied-damage reward or artificial resource farm. Suppress secondary healing/resource/excess-conversion triggers from these recovery events as an explicit anti-loop choice. Blocked/fullHP healing spends0 reserve but grants no stored heal. While your actual normalHP is strictly below half your current effective maximum before an attack's damage (tempHP excluded), melee weapon attacks against creatures with actual blood add1d4 necrotic before defenses and critical doubling. Actual blood fact, not type-name inference; no rider against known bloodless bodies. The extra die may contribute to that same legitimate critical's numeric damage, never copied again. Healing after the hit cannot retroactively remove its already-qualified die.

### Worked examples

A critical deals12resolved to HP3/temp4: actualDamageDealt7, so critical healing base3. The drop also offers level healing; both share remaining reserve.

At level8 with2reserve and missing10HP, a legal base8 drop heal restores at most2 and exhausts reserve. A later critical that day cannot heal until a completed LR.

## Precision Strike (`precision_strike`)

**Prerequisite:** Dexterity 13+ or Weapon Focus

Acquire with permanentDEX13 OR the exact Weapon Focus feat. Once per turn before one weapon attack roll choose one mode. Ordinary mode takes−2 on that roll and, on hit, adds floor50% of its eligible native weapon damage before percentages/defenses; actual critical dice are included before this computation. NEW alternative critical mode is available when the actual target is currently Restrained, Grappled, or carries your actual active Anatomy Lore identified-weak-point record. Spend the once-per-SR critical use on declaration; take no−2 and no+50% from this feat for this attack. If it hits, treat it as critical; a miss remains a miss and spends the use and turn allowance. Condition/mark eligibility is rechecked at resolution; losing it leaves an ordinary hit with the use spent. Actual critical immunity remains; no additional critical multiplier. Either mode is mutually exclusive with Power Attack's trade on this same attack. Anatomy Lore's own separately legal bonus can coexist under its precise native-damage scope, with percentages from the same base; the weak-point prerequisite does not grant that feat or let another owner's undisclosed read qualify. A grapple by another creature suffices because that alternative predicate has no ownership restriction.

### Worked examples

A native21 weapon packet in ordinary mode adds10 for31 before defenses, after taking−2 to hit.

Against a Grappled foe, critical mode rolls normally. On a hit dice double without+50%; on a miss the SR use is still spent.

## Slayer’s Resolve (`slayer_s_resolve`)

**Prerequisite:** Favored Enemy (Dragon) or level 8+

Acquire with actual Favored Enemy (Dragon) OR total level8. You are immune specifically to actual Dragons' Frightful Presence effects; unrelated dragon fear/spell effects are not automatically that identity. Existing source-qualified Frightful Presence records are suppressed while immunity applies, with clocks retained. While you are conscious, allied creatures within30ft and with line of effect to you have advantage on saves against effects that actually impose fear/Frightened; no hearing or common-language gate is added. This is current-position aura, checked at each save, not a permanent recipient list; you qualify as your own ally while conscious. Gain+2AC against actual attacks made by a creature explicitly typed Dragon; dragonkin alone does not satisfy this feat. Once per SR, when a Dragon you can see makes a melee attack or an attack-roll breath weapon targeting you, spend Reaction before the attack roll to impose disadvantage on that one attack. Alternatively, when such a Dragon's actual breath weapon requires your save, after the initial result but before consequences, spend Reaction and the same shared SR use to reroll your whole save with advantage; independent disadvantage cancels normally and the new result is mandatory. It does not reroll anyone else or waive a no-save breath effect. A breath weapon with an attack roll qualifies for the attack branch whether melee or ranged; no saving throw is invented for it. Non-breath ranged attacks do not qualify. Immunities, sight, Reaction prohibitions and actual source tags remain.
SOURCE SCOPE CORRECTION: “allies” includes the feat owner unless the actual clause says “other.” The owner must still meet the same hearing/perception, range, willing-target and action/resource predicates. No second body, observer or extra action is created by self-eligibility. This sentence supersedes any narrower owner-exclusion in the submitted proposal, not the preserved original.
EXACT BREATH-ATTACK CORRECTION: the once-short-rest Reaction may impose disadvantage, before its roll, on one attack roll of a perceived Dragon breath weapon, whether melee or ranged, or on a perceived Dragon melee attack. A non-breath ranged attack does not qualify. A saving-throw breath weapon instead uses the personal breath-save reroll branch after the initial result, whether it succeeded or failed, and before consequences, rerolling with advantage and using the new result. No attack or save is invented for a payload that has neither.

### Worked examples

A conscious holder within their own aura qualifies for its fear-save advantage. A Dragon melee attack against them gets the stated+2AC; dragonkin without the actual Dragon type does not.

A perceived Dragon breath weapon makes a ranged attack roll. A legal pre-roll Reaction spends the shared short-rest use and imposes disadvantage. A saving-throw breath uses the personal breath-save reroll branch, after success or failure but before consequences, instead; a non-breath ranged attack does not qualify for either branch merely because its attacker is a Dragon.
