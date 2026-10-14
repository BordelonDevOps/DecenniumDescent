# Magic Extended feats

**Source-authored exact candidate; separate exact review pending. Selection/runtime disabled. Original catalogs unchanged.**

[Complete shared rules](SHARED_RULES.md) · [Finite supplements](SUPPLEMENTS.md) · [Spell payloads](SPELL_PAYLOADS.md)

Read every procedure with the complete shared rules. NEW identifies authored completions; old source alternatives remain preserved. The two deferred payloads are unavailable.

## Arcane Armor (`arcane_armor`)

**Prerequisite:** Level 4

Require character level 4. NEW the qualifier governs BOTH+1 AC and+1 saving throws: they apply only against a Reaction whose actual printed trigger is your casting or continuing concentration on a spell. Begin eligibility at commitment of that cast, before interruption; end when its casting/held concentration/ordinary concentration ends. Merely attacking a concentrating caster is insufficient. The relevant Reaction must itself cause an attack against you or a save you make; Counterspell’s caster-side ability check is neither and receives no penalty. A triggered attack still uses ordinary critical rules. The bonus is passive, grants no Reaction, and cannot protect unrelated attacks or ongoing damage. Distinct eligible flat feat bonuses add under FS-03 after existing non-feat families resolve; duplicate Arcane Armor contributes only once. Preserve the alternative broad AC reading and old 5% resistance as inactive source alternatives.

### Worked examples

An actual on-cast Reaction attacks AC 14: eligible+1 makes AC 15, unless a stronger same-stat bonus already governs.

An enemy’s ordinary attack during your ongoing concentration receives no Arcane Armor modifier.

## Arcane Flexibility (`arcane_flexibility`)

**Prerequisite:** Intelligence 15+

At completion of each beneficial Short Rest, optionally replace exactly one currently prepared spell in one actual class preparation list with another spell of the same rank in that same class. It must already be a legal known/book/repertoire choice under that class’s preparation procedure and current class level/school limits. Decide after ordinary rest endpoints/recovery; record the previous and replacement preparation. No extra prepared capacity, learned spell, copied grant or class alias. A class without a preparation list gains no new list. NEW unpreparing does not retroactively dispel a legally ongoing spell; maintain its actual concentration/deadline, but no new cast through the removed preparation. One exchange per rest event across classes, not one per class or duplicate feat representation.

### Worked examples

A Wizard exchanges one prepared Wizard-rank 2 spell for another already eligible Wizard-rank 2 spell after SR.

Knowing the replacement through another class at rank 2 does not establish Wizard preparation eligibility.

## Arcane Pulse (`arcane_pulse`)

**Prerequisite:** Level 7

At character level 7, use an Action and pay 3 actual shared RP. NEW this is a magical feat technique, not an ordinary spell: no rank, spell components, Counterspell window or Dissonance/Refrain from this activation. At acquisition choose INT, WIS or CHA permanently for this feat’s DC=8+PB+that current modifier; this supplies neither spellcasting qualification norRPcapacity. Center a 10 ft radius on your own occupied space under ordinary area geometry. Choose perceived creatures with line of effect in it, including yourself if desired, before rolling. Roll 3d6 force once. Each makesSTRsave: failure full damage then push up to 10 ft directly away from the origin along a legal unobstructed route; success half damage rounded down, no push. Self can take damage but has no away-from-self push. Stop at obstruction/occupied destination; no collision damage, opportunity attack or unstated prone. Large bodies retain real fitting requirements. Immunity to forced movement blocks only push.

### Worked examples

A level 7 Warrior with noRPpool cannot pay 3 RP, even though acquiring this feat was legal.

A shared roll 11 produces 11 on failure or 5 on success; a wall 3 ft behind the victim limits actual push.

## Arcane Recall (`arcane_recall`)

**Prerequisite:** Level 10

After a completed personal rank 1–9 cast, optionally consume the once LR use to recover min(actual rank,5, RP headroom, unrefunded RP actually paid for that cast). NEW the funding ceiling counts only actual personal RP expenditure, including legal surcharges; it cannot refund charges, HP, other pools, free price or an ally’s contribution. Register the cast’s paid RP and every direct refund/recovery against the same expense once, across this feat and other refund sources; choose a legal order without exceeding that expense. A legal fully saved/missed cast qualifies; countered/interrupted, copied or released-again casts do not. A readied cast qualifies once when successfully prepared, never at release. If the computed recovery is 0, decline before committing the use; no newRPpool/cap. Ordinary ongoing effects need not finish their entire duration.

### Worked examples

Rank 3 paid 5 RP with enough headroom returns 3; a previous 4 RP refund leaves at most 1 for Recall.

A free charged rank 3 cast cannot produce 3 RP through this proposed funding rule.

## Arcane Transfusion (`arcane_transfusion`)

**Prerequisite:** Level 9

Once LR as a Bonus Action, choose integerN from 1 through min(current PB, actualRPheadroom) and preflight the shared normal HP funding rule for 2 Nnecrotic damage. Commit BA/use, then resolve that cost as one packet with normal Wound/death/concentration consequences. If still alive after the complete packet, restore exactlyNactual RP, capped by then-current capacity; later headroom loss does not refund HP. NEW this explicitly bypasses temp HP, resistance, redirection and floors for funding while retaining damage consequences. No use at 0 HP without an exact independent BA permission and sufficient actual funding, which the at-least 1 HP requirement normally forbids. No heal, charge creation, maximum RP increase or incidental resource trigger from self-damage. Ordinary later paid healing remains possible; it does not reset this LR use.

### Worked examples

PB 3 and 2 missing RP allowN 2: lose 4 normal HP and, if surviving, regain 2 RP.

HP 4 cannot fundN 2 even with 20 temp HP; the illegal attempt spends nothing.

## Blood Magic (`blood_magic`)

**Prerequisite:** Level 9

Once per beneficial SR or LR, when committing an actual spell, declare either+1 to that cast’s spell-save DC or one extra native damage die under the shared added-die procedure. Pay the spell’s actual ordinary costs plus 2×its actual rank as the shared unreducible-necrotic normal HP cost, before establishing its new concentration and opening interruption. Existing concentration must face the self-damage normally before displacement; death/action loss aborts the unfinished spell without refund. Rank 0 explicitly costs 0 HP but still spends the feat use; a cantrip is not excluded by the source. DC mode changes all actual saves caused by that same cast, including its legal repeats, while that cast lasts; it supplies no saves to automatic effects and no inherited DC for unrelated children. Damage mode cannot modify a flat-only or nondamaging spell. No two modes, doubled cast orHPrefund; copying never regrants the modifier.

### Worked examples

Rank 2 spell DC 14 becomes 15 after 4 normal HP cost; an ordinary area save for each target uses 15.

A flat damage effect has no eligible die for die mode; choose a legal DC mode or decline before payment.

## Channeled Flow (`channeled_flow`)

**Prerequisite:** Level 10

Once per beneficial SR or LR, on your own actual later turn, replace one Action explicitly required solely to maintain one of your already established spells with one Bonus Action. Declare and consume at that maintenance commitment. Preserve concentration, RP/material upkeep, targeting, existing pulse/command limits and the original spell deadline. It cannot shorten initial casting, Ready setup, a ritual, an attack granted by the spell, or an optional Action to issue a new damaging command unless that exact source identifies it as required maintenance. An Action that combines required maintenance with another benefit retains the combined printed payload but still supplies no second occurrence. One actual BA must be available; Incapacitated/other restrictions still apply. The source’s prior 50% duration wording remains an inactive alternative.

### Worked examples

Maintaining an existing spell with an explicit Action upkeep uses BA once, retaining its required 2 RP upkeep.

A summoned creature’s optional attack command is not automatically qualifying maintenance.

## Concentrated Will (`concentrated_will`)

**Prerequisite:** Level 5

At character level 5, gain+2 on actualCONsaving throws made to maintain concentration, including nonspell concentration that explicitly uses the same save. Apply current same-stat flat-bonus arbitration; ordinary advantage/disadvantage and proficiency remain independent. Each genuinely separate damage packet generates only its actual required save, not one per damage type or extra feat test. No modifier to unrelated CON, Wound or death saves, automatic concentration loss from incapacity/death, or a special source’s non-CON test. This creates neither concentration capacity nor permission to act at 0 HP. A legally held Ready spell has actual concentration and qualifies.

### Worked examples

A real damage concentrationCONsave gets the feat bonus and can also have existing advantage.

Becoming Incapacitated ends ordinary concentration without a save; the feat cannot invent a roll.

## Counterspell Adept (`counterspell_adept`)

**Prerequisite:** Level 6

At character level 6, NEW select the active effect’s+2 over preserved description/legacy+4. Add+2 to an actual ability/task check whose operative source directly counters or interrupts a pending spell, with FS-03 distinct flat feat bonuses additive after each existing non-feat family resolves. Ordinary Counterspell remains actual casting ability+PB versus 10+2×trigger rank, with task degrees/natural shifts collapsed to success/failure. The alternative+1 DC branch applies only if a separately operational counter source truly uses its own save DC; current ordinary and cited class Counterspells use checks, so noDCbranch applies to them. Never apply both to one attempt. This feat grants no spell, Reaction, extra attempt, automatic low-rank success, spell attack bonus or check to identify magic.

### Worked examples

Against rank 3, Counterspell DC 16 and ability+PB 5 become check+7 before rolling.

Mystic Focus’s spell-attack bonus does not apply to that task check; neither feat invents a penetration check.

## Dispel Precision (`dispel_precision`)

**Prerequisite:** Intelligence 15+

When a legal dispelling source would randomly select among individually eligible effects, choose its one eligible effect instead; identify an effect only to the extent the source permits. Ordinary reviewed Dispel Magic already chooses one perceptible ongoing spell rank 0–3 and ends it automatically: this feat changes neither its target count nor its rank/protection limits. Add+1 only to a real dispel check explicitly required by a different operative source. No check is invented for an automatic success, and no roll can exceed a source’s allowed scope. If the separate proposed Dispel Mastery is adopted, each of its legal targets retains its own existing procedure; Precision does not duplicate attempts. Hidden/protected curses, permanent magic items and class engines remain outside ordinary Dispel Magic.

### Worked examples

Choose one visible rank 2 spell among three on a creature; ordinary Dispel Magic ends it without a+1 roll.

A rank 5 effect remains ineligible for that ordinary spell despite this feat.

## Echo Spell (`echo_spell`)

**Prerequisite:** Intelligence 15+

Once LR immediately after a personal rank 1–3 spell completes its initial payload, select one numeric damage, HP healing, temp HP or flat stat-bonus component and its original eligible recipients. NEW no echo from Ready preparation until actual release, copies, summons, creation, resource/action grants, movement, hard control or maxima-changing effects. Snapshot that component’s native roll/flat value before external bonuses, original attack/save rules, type, origin and source DC. At your next future regular start, if alive/conscious and any source-required concentration still holds, repeat only that component at half native value floored;0 gives no effect. Recheck original recipients’ actual range/perception/line of effect from the recorded origin, which must still exist; no replacement target. Make fresh original attack/save tests, then ordinary defenses/healing caps, without new critical dice or external damage/heal add-ons. A selected shared area retains only original recipients still in the original area. Temp HP uses the single grant ledger; a flat bonus uses strongest-family arbitration and expires at the earlier of original deadline or your next regular end. Echo heals block healing-copy/resource outputs and create no convertible excess. No new cast, RP, components or duration for the parent; an invalid echo expires without refund.
FS-08 secondary-echo flag applies: this delayed result is not another cast. Its flat bonus is a continuation of the original bonus identity/family, not a distinct feat-stacking source; the strongest original-family rule remains. No new resource, copy, hit-trigger chain or source-specific no-resource exception is created.

### Worked examples

An original native 11 force area creates a 5 force echo against original still-legal recipients, each with a fresh original save.

A summoned creature’s HP, attacks and future turns are not a repeatable numerical spell component.

## Efficient Caster (`efficient_caster`)

**Prerequisite:** Wisdom 13+

Gain PB uses per completed LR, with current PB as maximum and no mid-epoch replenishment from growth. Once per numbered round, at a personal ranked cast’s declaration, optionally reduce its otherwise payable RP by 1, minimum 1. NEW apply after existing eligible base discounts and printed extra costs including component and strain/armor additions, but before final Resonance Influence; this is a discrete reduction, not a new base-rank price. A charged/free normal-price route still pays its independent costs; use is allowed only when this stage’s actualRPprice is at least 2. A genuine reduction commits both use and round entitlement with the cast, even if a later permitted final adjustment or interruption changes the outcome. Cannot reduce charges, HP, specialresources or manufacture a 1 RP charge on a 0 RP cast. Current rank/repertoire/strain cutoff remain.

### Worked examples

A rank 1 cast’s eligible price 2 becomes 1 before a separately applicable final Influence adjustment.

A charged spell with only 1 independent RP surcharge offers no reducible price and spends no feat use.

## Energy Sink (`energy_sink`)

**Prerequisite:** Wisdom 15+

PB uses per completed LR; no mid-epoch refill fromPBgrowth. After one actual hostile spell event targeting/affecting you resolves, if you either succeeded on its real save OR received no positive resolved damage from that event, you may spend a Reaction/use to recover 1 RP up to your real maximum. NEW require meaningful unwilling opposition: harmless, allied, cooperative, self-authored or farming spells do not qualify. A spell attack that legally targeted you but missed, immunity, or complete prevention can satisfy the no-damage branch; temp HP absorption is damage and alone cannot. A failed save against a hostile nondamaging control spell still satisfies literal no-damage, but only if its result leaves you able to react. One grant per actual cast identity across later ticks/events; no fan-out or repeating-zone farm. Positive saved-against damage may qualify through success. Resolve full damage/control/death first; no ordinary Reaction at 0 HP. Decline before spending if noRPheadroom. This is recovery, not transfer from the attacker or a new pool.
For this trigger, actual damage includes damage absorbed by Temp HP, so a spell that damages only Temp HP is not a no-damage event. A genuine ward that prevents all damage may leave a qualifying original hostile spell event; the ward does not itself generate a second event. Every explicit no-resource source flag remains controlling; see FS-07.

### Worked examples

Successful save halves a hostile spell to 5 damage: the success branch permits oneReaction for 1 RP.

A missed hostile spell attack can qualify; receiving a friendly harmless cantrip cannot.

## Ether Anchor (`ether_anchor`)

**Prerequisite:** Level 12

At character level 12, gain advantage on actual saving throws against an effect that would banish, forcibly teleport or displace you between planes. Once LR, after such a save fails but before consequences, optionally replace that failure with success; use the source’s actual success outcome, which may retain other effects. No Action or Reaction is required. It does not create a save against a save-less effect, convert willing travel to hostility, anchor nearby creatures, reveal destinations or permit an otherwise illegal movement. A save against damage accompanying independent displacement qualifies only if that same save actually determines the unwanted displacement. Existing explicit unpreventable/no-replacement rules control. No permanent immunity or new cosmological fact is implied.

### Worked examples

A failed actual banishment save becomes success and consumes theLRuse.

A source with automatic displacement and no save supplies no roll for this feat to improve.

## Flash Cast (`flash_cast`)

**Prerequisite:** Dexterity 14+

Once LR, declare an actually known/prepared spell with printed normal casting time oneAction as a Bonus Action instead; maintain every other access, component, RP, concentration and strain rule. NEW the whole actual turn, including any on-turn Reaction casts, may contain no other ranked cast before or after this cast. Preflight the turn’s existing cast history; committing this feat establishes the restriction even if countered. The chosen spell may be rank 0; other cantrips remain legal with their actual action resources. A later genuine extra turn is a distinct turn for this prohibition but does not refresh theLRuse or other regular-turn budgets. Ready release/copy with no new cast is not another ranked cast, while preparing a readied ranked spell is. No long-cast compression, Reaction conversion, free BA or universal restriction on unrelated turns.

### Worked examples

After casting a ranked spell as anAction this turn, Flash Cast is ineligible even for a cantrip.

Flash-casting a rank 2 spell allows a later legalAction cantrip but forbids an on-turn ranked Counterspell.

## Foresight Surge (`foresight_surge`)

**Prerequisite:** Wisdom 13+

After a completed actual Divination cast, gain a nonstacking+2 to future initiative rolls for one elapsed hour, refreshing that deadline on later eligible casts. The selected casting class must use Divination for this identity. If already participating in rolled initiative, also queue one move up one baseline place at the next numbered-round boundary. NEW one queued move per owner per boundary; repeated casts cannot accumulate jumps. At that boundary finish previous-round events, restore temporary permutations, then process pending advances in stable activation order by swapping the owner with the immediately preceding still-participating baseline actor; top actor stays. Apply later reviewed temporary permutations, such as Future Echo, to the resulting baseline. Every participant still receives one regular slot. A departed actor without a retained initiative slot loses its pending advance without makeup. Incapacitation alone does not remove an actor’s regular slot or this pending ordering change. Existing virtual deadlines, recharge, periodic clocks and spent budgets do not move or refresh; no reroll or extra turn.
For actual Future Echo, restore an expiring permutation first, apply this feat’s pending baseline advances once in the stated stable order, then apply a newly established Future Echo permutation to the resulting baseline. Preserve actual slots and spent turns; no extra turn or resource refresh occurs.

### Worked examples

OrderA, B, C withCqueued becomesA, C, B next round;Cdoes not act again in the current round.

Three Divination casts before that boundary still queue only one advance forC.

## Illusionist’s Trick (`illusionist_s_trick`)

**Prerequisite:** Charisma 14+

For each actual illusory creature/object you personally create, the first attack or interaction that would end that particular illusion’s existence instead delays only that ending until the current actual turn ends. NEW outside initiative use the end of the current canonical six-second window. It remains nonphysical and observers retain information already obtained; known illusions do not regain concealment, cover, belief or control. Losing required concentration, natural expiry, dispel, source death or another independent ending still ends it immediately. The feat does not postpone an observer’s ordinary Investigation check or direct physical proof unless that source’s actual rule specifically ends the illusion itself. At the deferred endpoint end the illusion as originally required; where the source only grants a disbelief test rather than termination, use its actual Investigation check/save at its printed timing, with no free new save type. Current Minor Illusion/Silent Image physical interaction reveals to observers but does not end the global image, so normally does not trigger this delay.

### Worked examples

A source illusion explicitly destroyed by a hit can remain visibly present until this turn ends, with no substance.

Walking through Silent Image reveals it immediately; this feat cannot make the witness believe the wall is solid.

## Lingering Magic (`lingering_magic`)

**Prerequisite:** Wisdom 13+

NEW select the active+1 round wording over preserved 20%. At a completed nonconcentration spell’s creation, extend its finite stated duration of at least one round by exactly one six-second/regular-marker interval, once per original cast. Round effects add one original regular marker; minute/hour deadlines add 6 elapsed seconds. A Ready spell’s temporary held concentration does not disqualify a normally nonconcentration payload; extend its payload at release, never its Ready deadline. Independently capped charges, target counts, specified number of pulses, item stock and discharge/consumption endpoints remain. An ongoing effect whose ordinary pulse exists solely while its duration persists may get the one naturally reached extra pulse; an explicit three-pulse effect remains three. No extension of instantaneous/permanent effects, resurrection windows classified separately from spell duration, concentration spells, linked separate conditions, or an independent end such as destroyed support. No stacking with itself or repeated recasting of the same instance.

### Worked examples

A nonconcentration 60 second effect lasts 66 seconds unless independently discharged earlier.

A printed three-pulse effect still has three pulses even if its remaining cosmetic duration extends.

## Magical Fortitude (`magical_fortitude`)

**Prerequisite:** Constitution 13+

Gain+2 to your actual saving throws directly required by an operative spell’s payload, including later repeat saves and a spell explicitly requiring a save to maintain another effect. NEW FS-03 applies: a distinct eligible+2 save feat adds to this+2, giving+4; duplicate copies of this feat do not. Existing non-feat families retain their own arbitration. Ordinary damage-induced concentrationCONsaves, Core Wound saves and death saves are consequences of shared life/concentration rules rather than the damaging spell’s printed payload and receive no bonus from this feat; Concentrated Will has its own exact concentration scope. A spell that directly calls for a death-effect saving throw can qualify, but ordinary death saves do not. Magical nonspell class/item/feat effects are not spells unless their actual source classifies the activation as one. CON 13 is acquisition only; no new proficiency, casting ability or defense against a Counterspell task check.

### Worked examples

A repeatWISsave explicitly supplied by an ongoing spell gains+2.

TheCONsave to maintain concentration after taking a spell’s damage uses Concentrated Will if owned, not this feat.

## Mana Burn (`mana_burn`)

**Prerequisite:** Intelligence 13+

After a creature fails an actual save against your personally cast damaging spell, remove 1 from its realRPpool, minimum 0. NEW damaging means that same spell application has a native damage component governed by that save; full prevention/immunity may leave 0 damage without negating the failed-save trigger. A repeat save solely ending nondamaging control after earlier damage does not qualify. Commit one recipient-wide Mana Burn entitlement per numbered round across all owners/casts on the first qualifying failure with anRPpool, even at RP 0; no further loss that round. Resolve native damage and immediate survival replacements first, then loss if the target still exists as a living resource holder. No transfer to you, charge/RC/slot substitution, maximum reduction or loss from RP-less creatures. Copies, echoes and reflected packets cannot create a fresh proc.

### Worked examples

Two casters trigger Mana Burn against the same RP 4 foe this round: total loss is 1, leaving 3.

A target immune to the damage can still lose 1 RP after failing the associated save; an RP-less monster loses nothing.

## Mental Buffer (`mental_buffer`)

**Prerequisite:** Wisdom 15+

Once LR, when a new source application would impose confusion/randomized action selection, a dominated/commanded Action or turn, or an explicit inability to distinguish friend from foe, voluntarily suppress only that application’s eligible control components through the end of your next future regular turn. No Action/Reaction is required; choose before those components first take effect. NEW qualify by actual written behavior, not a condition’s suggestive name. Ordinary Charmed/Frightened alone, illusion disbelief, blindness, truthful uncertainty and incapacity without such a component do not qualify. Preserve unrelated damage/slow and the original source, duration, concentration, repeat saves and spent hard-control entitlement. Suppressed clocks continue; legal ending saves still occur. If the original component has already expired or been cured by the boundary it never returns; otherwise it resumes for its remaining duration without replaying a past commanded turn. One application only, not immunity to later separate sources.

### Worked examples

A dominated Action scheduled inside the protected interval is skipped, not stored for a later extra command.

Another source’s independent Stunned effect remains operative.

## Mirror Cast (`mirror_cast`)

**Prerequisite:** Intelligence 16+

Once LR at cast declaration choose a real reflective surface you can see within 60 ft of your actual body. NEW require an unobstructed line of effect from you to that surface, at least hand-sized, sufficiently exposed to form a recognizable reflection; a drawn picture of a mirror is insufficient. Choose an unoccupied origin point immediately at its visible face. Measure spell range/line of effect and area orientation from that point; you still must personally perceive targets where the spell requires it, receiving no remote senses. Self-area/cone origins can relocate, but a Self-only body buff still affects you and Touch spells still require actual touch; no remote grasp. Hostile-held surfaces may serve if visibly legal; no possession or movement of the object. Commit ordinary costs/components/feat use at your body, preserving its interruption window. The origin is snapshotted for immediate resolution; destruction before resolution fails the changed origin with no refund. Ongoing created areas retain their actual fixed/moving rules and deadlines; the mirror is neither a second caster nor an unprinted tether.

### Worked examples

A cone can originate at a visible mirror 40 ft away and point along a chosen legal direction.

An unseen creature behind the mirror gains no free visibility; a Touch heal cannot cross 40 ft through it.

## Mystic Focus (`mystic_focus`)

**Prerequisite:** Level 6

At character level 6, NEW choose active+1 rather than legacy/description+2 penetration. Gain+1 on actual spell attack rolls and actual checks explicitly required to overcome magical resistance. NEW distinct applicable flat feat bonuses add under FS-03; resolve existing class/spell/item families first without changing their rules. No generic resistance check exists: ordinary damage resistance still halves its eligible damage and spell resistance that grants save advantage is not a caster check. Apply the second branch only to an operative source’s real test. This is not Spell Focus, supplies no saveDCbonus, spell access, damage increase or extra Counterspell/Dispel check. A Counterspell check is interruption, not overcoming magical resistance unless its exact source separately establishes that predicate.

### Worked examples

A legal spell attack+6 becomes+7 if no stronger applicable flat bonus replaces it.

A creature with fire resistance retains that resistance; there is no new+1 penetration roll.

## Mystic Recoil (`mystic_recoil`)

**Prerequisite:** Level 7

Once SR/LR after your own actual spell is countered, or after every originally legal recipient of its initial save-based payload actually succeeds on every required initial save, optionally commit the use and queue one extra BA for your next future regular turn. NEW require at least one actual initial save and all original recipients resolved legally; a no-save, mixed attack/save or lost-target cast cannot qualify by vacuous success. An automatic successful save counts where a real save was called for. No copying/echoing or each-tick retrigger. The BA becomes available on that one regular turn, even if other BA is spent, and expires unused at its end; incapacity creates no makeup. It may perform an actually acquired legal BA, including ordinary command, but cannot prepare/cast a ranked spell or create more actions/banked allowances. It does not bypass shared companion offense, concentration, RP or other use caps. No extra fullAction, Reaction or duration-clock tick.

### Worked examples

Both targets succeed on the spell’s only two initial saves: next regular turn gains one restricted BA.

One target failed but was immune to damage: the all-success branch does not trigger.

## Overchannel (`overchannel`)

**Prerequisite:** Level 10

Once LR at damaging spell declaration, add one existing native damage die per actual spell rank to one immediate native packet under the shared added-die rule. NEW choose this active rule over legacy 25%. Commit use with the cast. After its immediate attempted resolution, including a miss, all saves or Counterspell, take 2×rank force backlash as one self-damage event. This damage cannot be reduced or redirected; NEW it does pass through real temp HP before normal HP, unlike the explicitly proposed normal HP-funded blood costs. Resolve ordinary Wound/death/concentration consequences and no incidental reflection/resource/lifesteal triggers from this self-authored cost. It requires noHPprepayment and can kill the caster. A readied cast takes backlash after preparation/interruption, not after eventual release; its added dice attach once to the eventual immediate payload. Rank 0 legally adds 0 dice and 0 damage but still spends the use if chosen. Flat-only/no-native-die spells are ineligible.

### Worked examples

Rank 3 native 4d6 becomes 7d6 in the selected shared area roll, followed by 6 unreducible force backlash.

If Counterspell negates that spell, the committedLRuse and 6 backlash still occur.

## Planar Knowledge (`planar_knowledge`)

**Prerequisite:** Intelligence 14+

Once per actual creature identity, as a Bonus Action examine one creature you can perceive within 60 ft and line of effect. NEW commit the per-creature attempt before rolling INT(Arcana) against DC 10+its actual printedCR, rounding the finalDCdown by current fraction rules. NEW for an otherwise genuinely eligible creature with no assigned CR, use DC15; preserve the missing/null CR rather than inventing a rating. A missing creature identity, ordinary information payload or permission is still not supplied by this fallback. Success lets the Director truthfully disclose one existing damage resistance, immunity, vulnerability or explicitly established planar-trait fact; you may name a category, but no nonexistent fact is invented. If that category has none, report that absence only, not all other hidden data. Failure gives no fact and no retry through alias/form/encounter reset. Existing source disguises/protected information still apply. Planar traits requiring the deferred cosmology review remain unasserted; other recorded defenses are still usable.

### Worked examples

CR 1/2 gives DC 10 after rounding; success can reveal one actual cold resistance.

An unrated story entity is not automatically DC 10, and success cannot invent its planar origin.

## Protective Casting (`protective_casting`)

**Prerequisite:** Level 6

At character level 6, after a completed personal ranked cast gain+1 AC until your next future regular start. NEW select active+1/regular-start over preserved 10%/5 seconds. It begins after the cast’s immediate resolution or successful Ready preparation, so does not protect against that cast’s earlier interruption attacks. Miss/all-save still qualify; a countered cast does not. Repeated legal casts refresh one same-family record without stacking magnitude; distinct eligible flat feat AC bonuses add under FS-03, after existing AC formula/item/class/spell arbitration. Ready release does not grant again. Incapacity does not itself end this nonconcentration buff; ordinary expiry/source-suppression does. No additional armor, resistance, spell use or cast trigger from copies.

### Worked examples

A saved-against rank 2 spell still grants+1 AC after resolution.

Two ranked casts create one+1 record; a reaction attack during the first cast resolves before it begins.

## Quick Ritualist (`quick_ritualist`)

**Prerequisite:** Wisdom 14+

For a spell you can actually cast through a legal ritual route, halve only the route’s additional ritual time, with resulting additional time at least 5 minutes; retain the base printed casting time in full. NEW measure the result in elapsed seconds and round up to the next whole second so fractions never shorten a required interval. An original 10 minute addition becomes 5 minutes, not half the whole cast. An original shorter addition is not increased: use min(original additional time, max(300, ceil(original/2))). This explicit non-worsening interpretation preserves the minimum for reductions without penalizing a preexisting faster route. Components, formula/repertoire, costs, concentration, helpers and interruptions remain. It grants no Ritual tag or access; the separate proposed Ritual Caster overlay needs its own approval. Apply this additional-time change before any separately legal group active-time adjustment, whose minimum rule remains.
NEW common ritual arithmetic: let B be the spell’s actual base casting labor and A its separately required added ritual labor, in whole seconds. Quick Ritualist changes A to min(A,max(300,ceil(A/2))), leaving B unchanged. This never lengthens an already shorter source procedure. Literal source-required elapsed waiting is not active labor to halve.

### Worked examples

For a rank1 ritual with base Action6seconds plus600seconds added ritual labor, Quick Ritualist gives6+300=306seconds. It does not halve the base casting Action.

With Ritual Channeler as well,ceil(306×0.75)=230 would breach the6+300floor, so the result remains306seconds. No helper creates another spell, omitted component or concentration slot.

## Ritual Channeler (`ritual_channeler`)

**Prerequisite:** Intelligence 14+

NEW a group ritual is one actual legally available ritual spell with a designated lead and at least one physically present willing assistant continuously performing that same ritual’s active work; it is not simultaneous crafting, travel or independent casts. Use the exact source’s assistant qualifications/cap. If it supplies none, the proposed default assistant must know that ritual or have proficiency in the lead’s actual relevant Arcana/Religion/Nature skill; count at most two ordinary assistant contributions, with no numeric roll bonus when the source has no assistant benefit. This feat-holder contributes as two ordinary assistants within that cap, never as two leads or two physical bodies for a separate location requirement. One or more holders reduce the group’s total active casting time once by 25%, rounding up seconds; passive waiting is unchanged. Apply after Quick Ritualist’s additional-time reduction, but never reduce that remaining additional ritual portion below 5 minutes unless it was already shorter. Source-required simultaneous people, costs, lead concentration, interruptions and minimum times remain. No multiplicative 25%stack or free spell/resource. NEW the double-assistant contribution applies only while actually serving as an assistant. A lead who owns this feat can supply the time reduction but cannot simultaneously count as two assistants; one person never performs both assigned jobs at once.
NEW apply the one25% helper reduction to the actual total ritual labor after any Quick Ritualist reduction, never once per helper. For the standard added-ritual route, final total=min(previous total,max(B+300,ceil(previous total×3/4))). No reduction removes the actual base casting work or the five-minute added-ritual floor, and a source already shorter is not lengthened. Every required helper attends the full resulting procedure. No check or numeric helper bonus is invented where the actual source has none.

### Worked examples

A source with600seconds base labor plus600seconds added ritual labor takes900seconds with the25% group reduction alone, respecting its600+300floor. Each actual helper works all900seconds.

Two Channelers do not apply25% twice or count as two physically separate station operators. A source with no check receives no invented numeric helper bonus.

## Runic Shield (`runic_shield`)

**Prerequisite:** Wisdom 14+

NEW select 15 ward HP over preserved 50. The feat has one armed grant per beneficial SR/LR; acquisition arms it. At the first real encounter start after arming, automatically create one personal runic ward with 15 points and spend that entitlement, even if surprised/incapacitated; a dead creature receives none. It persists between encounters until depleted or the next beneficial SR/LR, when any old ward ends and entitlement rearms for the next combat, not immediate refill in combat. Repeated initiative does not refill it. This is a distinct spell-only ward, not temp HP: after ordinary defenses and before temp HP, intercept up to its remaining points of actual incoming spell damage in stable component order. Nonspell damage bypasses it. Record ward absorption separately, excluded from actual damage received by the body, Wound/death thresholds and concentration checks; any surviving packet resolves once normally. No transfer, double ledger, HP healing, return on revival or resource proc from ward absorption. Counterspell/dispel cannot target this nonspell passive ward without explicit applicable source permission.

### Worked examples

A post-defense 20 spell-damage packet consumes 15 ward then passes 5 to temp HP/normal HP.

A sword’s 8 nonspell damage ignores the ward entirely; starting another encounter does not restore spent ward points.

## Silent Casting (`silent_casting`)

**Prerequisite:** Level 7

At declaration of a spell actually requiringV, remove only that verbal component by adding 1 actual RP to its price before ordinary final cost adjustments. NEW the independent 1 RP payment cannot itself be waived by a charged/free normal-rank route; an actualRPpool and sufficient final payment are required. Rank 0 can use the feat and still pays the independent surcharge; cantrip strain rules remain. A component or exact activation explicitly demanding a magical command word cannot be removed. Ordinary audibleV alone is not a protected command word unless identified as such by the operative source. PreserveS, F/materials, physical access and action permissions. Silence no longer blocks the removedV, but Incapacitated/other restrictions remain. It creates neither undetectable casting nor automatic concealment; other visible components/effects and observers’ real senses still determine interruption eligibility.

### Worked examples

A V, S cantrip may be cast silently with S and 1 real RP, provided every other permission holds.

A charged spell cast by someone with noRPpool cannot pay the extra 1 RP through its charge.

## Spell Deflection (`spell_deflection`)

**Prerequisite:** Intelligence 16+

Once LR, NEW spend a Reaction when a hostile pending spell has selected you as its sole creature target, after ordinary cast interruptions but before its attack/save/effect resolution. It must be an actual single-target payload, not one target remaining from an area or multi-target mode. Roll an unmodifiedd 20;16–20 redirects, preserving this explicit 25%procedure over legacy 10%. On success choose a different legal creature under the original spell’s actual target restrictions, range/line measured from the original origin, personally perceived by you where necessary; the original caster remains owner and supplies all stats/choices. Recheck legality, then use fresh original attack/save procedure against that new target; nothing resolves against you. If no legal new target exists, or on 1–15, the spell continues against you with advantage on each actual initial save it requires; no save is invented for an attack/automatic spell. Use/Reaction remain spent. A redirected/reflected/copy packet cannot be redirected again by this family or Spell Reflection. Protected/self-only/source-specific exclusions remain.

### Worked examples

Roll 17 redirects an eligible hostile ray to another legal creature within the original caster’s range.

Roll 9 against an attack spell grants no save orACbonus; the original attack proceeds normally.

## Spell Reservoir (`spell_reservoir`)

**Prerequisite:** Intelligence 14+

Once LR, immediately after completing a beneficial SR and its ordinary recovery, optionally restore currentPBactual RP capped by remaining merged-pool headroom. Commit theLRuse and that actual rest-event claim together; another listener, duplicate receipt or resumed rest completion cannot claim again. If no headroom, you may decline without spending, but cannot bank that past rest’s trigger for later; a later beneficial SR can supply a new opportunity while theLRuse remains. It creates no maximumRPincrease, charge, slot, second classpool or independent Retune. A long rest alone does not count as the printedSRtrigger. PB changes before a future legal use affect that use’s amount but never refresh spent entitlement.

### Worked examples

PB 4 with 2 RP missing after normalSRrecovery restores 2 and spends theLRuse.

At full RP you may decline; spending RP later does not reopen that already-finished rest.

## Spellweave (`spellweave`)

**Prerequisite:** Wisdom 14+

NEW use the finite three-spell minor-buff table below: personally cast Guidance, Resistance or True Strike with yourself as the otherwise legal recipient. At its completion hold that entire one-use buff instead of receiving it normally; only one held record, replacing loses the old. Original costs, cast history and earlier deadline remain, with an additional deadline at your next future regular end. The next actual spell you commit consumes/attaches the record automatically, even if countered or unsuitable; no indefinite skipping. Guidance adds its one 1d4 only to one actual ability/task check made by that next spell, declared before rolling; Resistance adds its one 1d4 only to one actual concentration save maintaining that next spell; True Strike grants advantage only on that next spell’s first actual spell attack. They create no check/save/attack. The attachment expires at the original held deadline or actual spell end, whichever first, even if unused. Current one-bonus-die/advantage rules apply. A copied buff, borrowed duplicate or another Spellweave cannot be held; no duration/resource/HP/stat transfer or new cast.
The three selected current buffs are non-concentration spells. Holding/attaching their one-use benefit adds no concentration requirement and does not change that source fact. There is still only one held Spellweave record and each original deadline/cost/history; no newly invented check or save may redeem it.

### Worked examples

Held Guidance attaches to a legal next Counterspell and can add 1d4 to its actual counter check.

Held True Strike consumed by a next spell with no attack produces no benefit and cannot wait for a third cast.

## Still Casting (`still_casting`)

**Prerequisite:** Level 7

At declaration of a spell requiringS, remove only that somatic component by adding 1 actual RP before final pricing; use Silent Casting’s independent-surcharge convention, including actualRPrequirement for rank 0/charged routes. NEW fully restrained means actual hands/arms physically or explicitly magically immobilized so no usable casting gesture exists; CoreRestrained alone imposes its printed penalties and does not prove that anatomy restriction. This feat expressly fails under such complete physical/explicit gesture immobilization, despite removing ordinaryS. It also supplies no Action under Incapacitated, no freedom from binding, and no hand for actualF/material manipulation. RemovingS andV with two feats pays both independent surcharges; each protected command/material requirement remains. Spell perception/counterability follows real remaining cues.

### Worked examples

A net’s actual full arm binding blocks this feat; a source’s mere Speed 0/Restrained penalty need not.

RemovingS still leaves a required held focus that the caster must legally handle.

## Temporal Flux (`temporal_flux`)

**Prerequisite:** Level 8

At character level 8, when a creature fails an actual save against your personally cast time-tagged spell, apply one softSpeed−10 ft record and one no-new-Reactions component until its next future regular start. NEW finite feat-tag overlay: Slow’s two actual modes, Haste and Future Echo only; current source tags do not supply an explicitTime tag. Their full current spell procedures remain unchanged, and a save-less buff creates no trigger. Wider tags require separate review; spell names or narrative time flavor alone do not qualify. Speed records compete under current strongest-adverse-control arithmetic rather than add;0 floor, real modes and existing movement spent remain. Already committed Reactions finish. Same owner/target/profile refreshes one record without extra magnitude; different sources retain their real deadlines. No new save, hardActiondenial, extra turn, state restoration or enabledTime Loop.

### Worked examples

A failed Slow save on Speed 30 already produces halfSpeed 15; Flux−10 competes as 20, so effectiveSpeed stays 15.

Haste ordinarily has no recipient save, so its new feat tag alone does not trigger Flux.

## Twin Cast (`twin_cast`)

**Prerequisite:** Level 8

Once LR after a personal rank 1–3 single-creature spell completes its initial payload, choose one additional different creature currently legal under that same mode, range, sight, line of effect and willingness/type restrictions. NEW only an originally exactly-one-creature payload qualifies; no area, multi-ray/multi-target, Self-only, summon/object creation, resource/action-grant, resurrection, maximumHPchange or copied payload. Consume the feat use and extend that same cast’s original immediate damage/heal/condition/buff to the second recipient. Roll a fresh actual attack/save and native dice for that recipient; no newRPprice, cast, components, Dissonance/Refrain or class/featproc. Independent per-recipient material/HP/finite reserve requirements remain actual costs and must be affordable before choosing. One concentration ID governs both; original deadline and source target-ending rules remain. This is an explicit two-target exception only for this cast, not another spell identity or separate duration. Preserve old 5%autodouble wording as inactive alternative.

### Worked examples

A legal rank 1 one-creature damage spell resolves anew against one second eligible creature without another baseRPcost.

A spell already selecting up to two creatures cannot qualify merely because the caster chose only one.

## Arcane Adaptation (`arcane_adaptation`)

**Prerequisite:** Spellcasting ability, Intelligence 13+

After an actual successful legal reflection or capture of a spell/supernatural effect through a separately owned source, gain resistance to the one real damage type expressed by its selected copied/reflected component until your next future regular end. NEW choose one observed type for a mixed packet; nondamaging effects grant no damage resistance. It begins after capture/redirect, does not retroactively mitigate earlier damage, and grants no copying permission by itself. Once SR/LR at that event, also mark the one legal captured profile as temporarily known through your second future regular start. During that interval you may activate that exact bounded profile using its actual action, RP, components, rank ceiling and concentration, even if its original one-use record was consumed; no other original spell/monster ability is learned. Each activation is a copy retaining the original no-proc/no-copy/resource flags and the shared one-copy-release/round cap below. Existing Mirrorsage records retain their actual release costs/caps and printed bounded profile. No restoration of archive slots or legacy boss power. Expiry removes permission but not legitimately established effects before their own deadlines.

### Worked examples

Capturing a fire Strike grants fire resistance through next end; adapting it permits paid bounded releases within two regular-start intervals.

Copying a harmless warning reveals no damage type and grants no invented resistance.

## Arcane Calculus (`arcane_calculus`)

**Prerequisite:** Intelligence 15+, proficiency in Arcana

Gain+2 to an actual initiative roll only while concentrating on a spell when that roll occurs; losing concentration later does not rewrite initiative. Once SR/LR use an Action to prepare one currently legally prepared normalActionspell through the exact Ready casting procedure, paying costs/components/history and opening interruption at preparation. NEW it shares the one pendingReady slot and concentration requirement, but its hold lasts through your next future regular end, and release is a voluntary non-action on that next regular turn only. Choose/recheck original legal targets then; no Reaction or second cast. Expiry, replacement or lostconcentration wastes paid costs. On successful release, choose one perceived creature within 30 ft of your body and line of effect:DEX save against the stored cast’s actual DC or take force equal to max(1, its actual casting modifier snapshotted at preparation),0 on success. One immediate noncopyable feat rider, no added release/action/castproc. Readied spells lacking a preparation route remain ineligible; the feat grants no preparation list.

### Worked examples

Prepare a legal spell now, then release next regular turn without spendingAction; one nearby creature may face the separateDEXsave.

A Counterspell at preparation prevents storage and the later rider; there is no second Counterspell window at release.

## Arcane Momentum (`arcane_momentum`)

**Prerequisite:** Power Attack or Combat Casting, spellcasting ability

Require actual Power Attack OR Combat Casting plus actual spellcasting ability. NEW each personal direct melee-weapon hit against meaningful opposition gives one featMomentum, max 3, with a once-per-attack identity and no gain from copies/companions/retaliation. This separate pool starts 0, ends at encounter end or one minute without a qualifying hostile hit; no alias to any class Momentum. At spell declaration choose ONE mode. Spend 1 to shorten a printed normalActionspell to BA; no other casting time has a shorter step in this explicit finite ladder, so no BA-to-free, Reaction-to-Action or ritual compression. OR spend all current 1–3 stacks to add floor(native immediate damage×stacks/10) as force to one selected native packet/shared area roll before this actual turn ends, after native critical/flat formula but before defenses. It adds damage rather than converts the original type, and does not compound other percentage bonuses. No damage means 0, no future periodic/ray replication; a miss/counter wastes stacks. Cannot combine both modes on one cast or bank the declared enhancement for a later turn.

### Worked examples

Native 19 damage with 3 stacks adds 5 force; native damage keeps its original type.

A printedBAspell cannot be made free by spending a stack.

## Conjure Flora (`conjure_flora`)

**Prerequisite:** Spellcasting ability, proficiency in Nature

Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW to make the second-capacity clause usable, at level 10 this same committed use permits one additional Action before the first plant expires to create one second plant; no second rest use, no later replacement of that spent creation. This is an explicit proposed addition to the printed one-seedling creation, not a recovered rule. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.
NEW ordinary command scheduling: each plant has one attached phase immediately after its owner’s regular turn, not an independent initiative turn. Its ordinary commanded action requires the owner’s shared Bonus Action within60ft through the specified perceivable command channel and spends the one offensive companion allowance per owner per numbered round if offensive. With no legal command it has no autonomous attack. Trapcasting’s explicitly adopted entry-trigger or burst is a separate narrow exception spending that same shared offensive allowance, never another free attack.
KEEP the already-operative SUP-07 floraBody/dc acquisition requirement: at acquisition permanently select and record one actual possessed spellcasting route as this feat's DC provider. Use DC 8 + current PB + that route's current casting-ability modifier; do not invent Wisdom, Spellcraft or another default. This source choice is separate from the later seedling mode/burst-type choice. Ownership initializes only the finite creation allowance and body capacity, with no plant, pending additional creation, command or active effect. All printed acquisition predicates and the actual earned feat opportunity remain required.

### Worked examples

Two active plants can extend where the single 1d6 lash originates; they do not produce 2d6 or two attacks.

At level 10, a second Action during the first plant’s lifetime can consume the one proposed additional-creation entitlement; it does not allow repeated replacement plants.

## Curse Channeling (`curse_channeling`)

**Prerequisite:** Spellcasting ability or proficiency in Arcana, level 6+

Require character 6 plus actual spellcasting OR Arcana proficiency. After a personal direct weapon hit, optionally place oneHexMark on that creature; the triggering hit cannot consume it. Capacity 1, or 2 at total 10; new beyond cap replaces oldest. Each record expires at your next future regular start and has two distinct one-use riders. The next genuinely separate hit against that target adds 1d6 necrotic to that hit’s packet, critical-doubled if that hit truly crits, then consumes only the damage rider; attribution remains to your feat, not the attacker’s spell for proc purposes. While the record remains, the first drop from positiveHPto 0 by genuine hostile conflict lets you choose 1d6 ordinary self-healing or advantage on your next actual attack roll through next regular end. Commit that drop rider even if blocked/full HP; no floor-prevented drop, staged victims or repeated same-target cycling within the encounter. NEW one drop benefit per owner/target/encounter; healing is finite paid-feat trigger, no healing-copy/resource output or convertible excess. Mark ends early only on replacement/cure/source rule; separate source marks do not stack the same damage rider on one hit.

### Worked examples

An ally’s later hit spends the mark’s 1d6, but a subsequent lawful drop before expiry can still grant the one self-heal.

Your original marking hit supplies neither its own bonus die nor a drop reward if the target was already 0 before the mark existed.

## Curse Weaving (`curse_weaving`)

**Prerequisite:** Spellcasting ability, Charisma 13+

At a personal actual spell declaration that forces an initial save, select at most one original creature recipient for this NEW curse rider. Once per owner/target/numbered round, if it fails that actual initial save, establish an inflicted removablemagicalcurse with that save’s ability/DC and maximum one minute. Tier/rank for an actual rank-limited cure is the generating cast’s rank. Immediate stage 1 is−1 attack rolls; at the target’s next future regular start add stage 2−1 saves; at its following regular start add stage 3 disadvantage on actual concentration saves. Cap at 3; components accumulate within this record, not as repeated−1 stacks. At every affected regular end, including a current turn where applicable, repeat the original save; success ends the record. Original spell concentration loss/termination ends this attached curse; instantaneous spells leave its bounded independent minute. Suppression preserves stage clock and legal cures/saves without backlogged effects. Reapplication does not reset stage/extend beyond the later legal deadline or duplicate magnitude; different sources retain identity but same penalties use strongest. No forcedAction, deniedturn or hidden perpetual escalation.

### Worked examples

Failing initialWISsave gives−1 attacks; next regular start adds−1 saves, then the regular-endWISsave can end both.

A second copy of the same stage cannot create−2 attacks or a fourth escalation.

## Dark Affinity (`dark_affinity`)

**Prerequisite:** Charisma 13+

Gain necrotic resistance once. NEW darkvision branch is fixed at acquisition as specified below; an extension does not revert to a60ft base when its underlying source ends. It does not see through magicaldarkness unless separately allowed. Advantage applies to actual saves against a Charmed/explicitcharm component sourced by a creature actuallyUndead at application; no free type detection or general mind immunity. While your occupied space is actually dim/dark, gainStealthadvantage subject to ordinary hiding/perception; NEW whole footprint must qualify. Once SR/LR use BA from such a space to teleport up to 15 ft into an unoccupied fitting space you can see that is also dim/dark. No traversed path, but NEW line of effect to destination required; obey actual teleport/consent/restraint restrictions. Costs/use commit normally; no invisibility, freeHide, ancestry conversion or soul/origin claim.
NEW exact darkvision branch, replacing any dynamic fallback reading: snapshot whether an independent darkvision source exists at acquisition. No source then gives a60ft base; an existing source then gives a+30ft extension to the current strongest independent operative range. Losing/suppressing every underlying source makes that extension inoperative, not a new60ft base. Record the branch permanently; unrelated future base ranges use normal strongest-base arbitration.

### Worked examples

Existing 60 ftdarkvision becomes 90 ft; Darkness that defeats that sense remains opaque.

A lit destination cannot receive the shadow step even if it is within 15 ft.

## Dark Binding (`dark_binding`)

**Prerequisite:** Curse Channeling or level 8+

Require Curse Channeling OR character 8. Spend one uninterrupted hour in contact with one actual owned/willingly entrusted weapon carrying an established curse record; no feat-created curse, weapon or hidden curse diagnosis. NEW ritual needs your voluntary symbolic drop of blood but no numeric HP/material charge, and is unrelated to Blood Ritual. Completion replaces your old binding; interrupted work creates none and leaves the old. While personally wielding the bound original weapon, you cannot be involuntarily disarmed by an actual disarm effect; mandatory dropping from Unconscious/incapacity, loss of body/hand, voluntary release and physical destruction still apply. Each actual direct hit you make with that weapon adds 1d4 necrotic, critical-doubled normally. Thrown original weapon qualifies on its hit but does not return; ammunition launched by a bound bow qualifies as its weapon hit without becoming a bound item. No copying or companion use. Actual destruction ends the bond and causes one 2d10 psychic damage packet to you under ordinary defenses, at any distance; repair never rebinds. A fresh fullhour ritual is required for a new bond.

### Worked examples

An enemy disarm cannot take a consciously wielded bound sword; becomingUnconscious still drops it.

Destroying a bound thrown weapon causes one 2d10 psychic packet, with ordinary psychic resistance if present.

## Eldritch Echo (`eldritch_echo`)

**Prerequisite:** Forbidden Pact or spellcasting ability, level 3+

Require character 3 AND (Forbidden Pact OR actual spellcasting). Gain the exact NEW Eldritch Blast cantrip profile below once; duplicate grant through Forbidden Pact shares one identity. Once SR/LR when you actually perceive a creature within 60 ft/line of effect completing an eligible noncopyspell, use a Reaction to capture one matching bounded copy profile below. NEW the source may be ally or foe, but cannot be a resource/copy/production effect or protected boss/legendary ability. Record original rank and the profile’s half-rankq; it must fit your actual qualifying casting route’s learnable ceiling, with Forbidden Pact’s explicit rank 0 grant supplying no ranked ceiling by itself. On your next future regular turn use anAction, actualRPprice and V/S and any additional actual copied-profile component requirement to release that one profile; otherwise it expires at that turn’s end. It is a copied spell activation with actual Dissonance/Refrain/history and interruption at release, no new proc/capture. No free original full spell, copied casterstatistics or Warlockclass.
NEW classification reconciliation, FS-08: releasing this captured spell is a paid feat-copy cast, using the releaser’s specified ability/PB, actual components, current RP price, rank and ordinary Dissonance/Refrain. It is not a resource-free nonspell release. It grants no ordinary repertoire/class feature or further capture, echo, reflection, external feat amplification, class resource/proc or reward chain. The concrete copy profile and its independent component/range/target/deadline limits still apply. This is deliberately different from Echo Spell/Twin Cast secondary results and from an actual Mirrorsage class Echo Release.

### Worked examples

Observe rank 4 damage: half-rankq 2 Strike may be captured if your real route can learn rank 2, then costs 3 RP next turn.

Forbidden Pact alone supplies the cantrip, not a rank 2 spell repertoire orRPpool for that copied release.

## Forbidden Pact (`forbidden_pact`)

**Prerequisite:** Charisma 13+, level 3+

Require CHA 13 and character 3. Preserve the original beyond-known-planes soul-pact wording as unreviewed setting provenance; this procedure grants no soul transfer, patron demands or cosmological claim. Mechanically gain the exact NEW Eldritch Blast profile and choose permanently one of three finite sigils below with the Director. This feat’s casting ability is CHA and grants rank 0 access only, not anRPpool or ranked repertoire. NEW reconcile “instead of a ranked-spell recovery” and old “instead of a spell slot” as once per real encounter substituting 2×actualrank normal HP sacrifice for the ordinary baseRPprice of one independently known/prepared rank 1–9 spell. Commit true HP loss while retaining at least 1 normal HP; temp HP, mitigation, floors/refunds cannot fund it. It is sacrifice, not damage, so no Wound/concentration/damageproc from the payment. AdditionalRPcosts, strain/armor/component surcharges, materials and action remain actual payments; final price calculation waives only original rankbase before those additions. NoRPis restored, no chargeuse bypassed, no separate ranked grant and no incidental resource output. Interrupted spell keeps all costs/use spent.

### Worked examples

An independently legal rank 2 cast may substitute 4 normal HP for base 3 RP once this encounter, still paying an actual extra 1 RP surcharge.

A pact-holder who knows only Eldritch Blast gains no ranked spell to pay for this way.

## Hemocraft (`hemocraft`)

**Prerequisite:** Intelligence or Charisma 13+

After a personal genuine melee critical hit against meaningful opposition, apply one NEW Hemocraft Bleed record to the still-living eligible target. It pulses 1d4 slashing at each of its next three regular starts; source immunity/anatomy restrictions and the existing Bleeding-family arbitration/cures remain. NEW max 3 own records per target; at cap refresh the earliest deadline without adding a fourth. Same-family parallel records do not all deal damage: existing strongest-die arbitration selects one, but distinct consumable records retain identity. Once per numbered round use BA to consume one present unexpired own Hemocraft record on a creature you perceive within 30 ft/line of effect, including one temporarily suppressed record, choosing 1d8 ordinary self-healing OR one 1d8 necrotic packet to that creature withCONsave against DC 8+PB+your chosenINTor CHA modifier for half. Choose stat permanently at feat acquisition. Pay by ending that exact record before outcome; no refund or consumption of another source’s Bleed. Healing spends a NEW finite Hemocraft Reserve of 2×character level set only at beneficial LR, paying actual restored HP, no excess/copy/resource outputs. Reserve starts 0 on acquisition. No consuming historical/already-cured Bleed or staged victims. The record’s ordinary Medicine-ending DC is the same chosen feat DC; actual positive-potential magical healing ends eligible Bleed through the existing cure procedure.

### Worked examples

Consume one actual record to roll 7 healing with 2 Reserve and sufficient missing HP: restore 2 and spend 2.

A suppressed still-present record can be consumed, but an ended record cannot return for another heal.

## Lightning Affinity (`lightning_affinity`)

**Prerequisite:** Spellcasting ability or proficiency in Nature

Gain lightning resistance and+1 damage per actual native lightning die in your personally cast spells, including native critical dice, as a flat adjustment before save/defense; no bonus per flatpoint, added nonlightning die or copied packet. Against a target actually outdoors/open-sky, your lightning spell attack/save geometry ignores halfcover only; threequarters/total cover remain. Gainadvantage on actual saves against a lightning/electrical payload or a component imposingParalyzed, not everyCONsave. After a hostile meaningful lightning packet deals positive actual numeric damage to you, spendReaction to gain oneStormCharge, max 2. NEW no charge per damagepoint; genuine tempHPabsorption qualifies, fully prevented/floor-only numeric 0 doesnot. Each charge lasts one minute from gain; no maximum cap refresh from a rejected gain. On your own turn, spend one charge withoutAction to prime your next personal weapon attack or immediate damaging spell before next regular end: add 1d6 lightning to one selected hit/packet/shared area roll under added-die rules. Attackmiss consumes the primed rider; no stacking multiplecharges on oneactivation. No charge from self/cooperative/copy/retaliationdamage.
Preserve per-charge origin and expiry: receiving a further charge at capacity does not refresh an older charge. FS-07 respects each underlying spell’s no-resource/trigger flags. The native lightning-die+1 excludes external riders and secondary/copy results; it can add to an independently eligible Evocation Focus bonus on an actually rolled kept die, not on a fictitious maximized face.

### Worked examples

A native 3d6 lightningspell adds 3 before saves; a reaction to 8 actual lightningdamage gains 1 charge, not 8.

A miss wastes the primed die; a later attack cannot recover that spent charge.

## Mimicry (`mimicry`)

**Prerequisite:** Spellcasting ability, Intelligence 15+

Once between beneficial SR/LR completions, when you perceive an eligible real spell/monster ability used against you at its lawful range OR resolving within 30 ft of you and line of effect, capture one matching finite copy profile below withoutAction. NEW one record and one release entitlement per rest epoch; cannot erase/replace to gain repeated uses. No copy from a copy, protectedunique/legendary/boss feature, classengine, resource/action/creation effect or an unobserved component. Actual targeted-at-you clause may exceed 30 ft only if you genuinely perceive the source and effect. The stored profile expires at the next beneficial SR/LR; release before then usesAction, V/S, actualRPprice and its actual qualifying casting ability/rank ceiling. Its numeric native ceiling is half the observed eligible component as detailed below and duration at most two future regular intervals; no original source stats/unboundedDirector invention. Successful capture alone is not a cast; release commits ordinary spell history/interruption and the one-copy-release/round allowance. Failed/countered release consumes record/use, and a later rest never refills a missing copy.
NEW classification reconciliation, FS-08: releasing this captured spell is a paid feat-copy cast, using the releaser’s specified ability/PB, actual components, current RP price, rank and ordinary Dissonance/Refrain. It is not a resource-free nonspell release. It grants no ordinary repertoire/class feature or further capture, echo, reflection, external feat amplification, class resource/proc or reward chain. The concrete copy profile and its independent component/range/target/deadline limits still apply. This is deliberately different from Echo Spell/Twin Cast secondary results and from an actual Mirrorsage class Echo Release.

### Worked examples

A perceived attack spell directed at you from 60 ft may qualify through the targeted clause despite the ordinary 30 ftwitness radius.

Observing a monster restore RP cannot produce a copied recovery profile.

## Quickened Thought (`quickened_thought`)

**Prerequisite:** Intelligence 15+, Arcane Calculus or Temporal Theory

Require INT 15 and (Arcane Calculus OR Temporal Theory). NEW resolve the grammatical scope as+2 initiative AND concentration-saveadvantage only while actually holding a readied spell; initiative is not recomputed later. Once SR/LR change an actually available normalActionspell of actualrank 0–2 to BA, paying every normal cost. From commitment until your next regular start you cannot commit anyReaction, even if the spell is countered; existing stacked Reactions finish. Separately, at first legitimate initiative roll of a real encounter, you may immediately prepare one legal normalActioncantrip as a non-action: pay components/independent RP/history, establish held concentration, open interruption, and use the same single pendingReady slot. NEW release that cantrip once without an Action on any later actual turn in that encounter, between completed events, retaining actual concentration until then; target legality rechecks at release. This replaces any oldReady, ends at encounter end or lostconcentration, cannot be banked again by reroll/reentry, and shares the free-stored-release cap of one per owner/numbered round with Arcane Calculus. No extra cast/copy/proc at release.
NEW exact banked-cantrip release window supersedes a narrower own-turn-only draft: the held cantrip may be voluntarily released without an Action or Reaction on any later actual turn before its preserved Ready deadline, between completed events, not retroactively or as an interruption. Use the shared one free release per owner per numbered round; no extra turn is created. Holding still consumes the one actual concentration/Ready slot and its original costs/history. Arcane Calculus retains its expressly narrower next-own-regular-turn release window.

### Worked examples

A banked cantrip paid at initiative can release on your second regular turn withoutAction if concentration survives.

Using theBAspell branch then leaves noReaction for Counterspell until the real next regular start.

## Spell Reflection (`spell_reflection`)

**Prerequisite:** Spellcasting ability, level 8+

Once SR/LR spendReaction in Spell Deflection’s same pre-payload window when you are the sole creature target of an actual single-target spell. NEW redirect to the original caster only if that caster is a legal recipient under its own spell’s target/range/line rules; preserve original owner, rank, attackbonus, DC, payment and concentration. Resolve its original attack/save against itself; no automatic self-hit or invented save. Noarea, multi-target, copied/alreadyredirected or protectedpayload; an illegal caster-recipient makes this activation unavailable withoutpayment. Redirecting does not teach/capture the spell. Separately, once per numbered round after an owned hostile spell deals positive actualnumericdamage to you, the living personally perceived caster within 60 ft/line of effect takes psychicdamage=floor(actualDamageDealt/2). NEW this passive retaliation requires you stillalive after the complete packet, noReaction, excludes overkill and self/friendly/copy/reflection roots, and consumes at first qualifying packet even if half rounds 0. Ordinary psychicdefenses apply. It cannot itself reflect, capture, heal, generate RP or restart a damageproc; no summing multiple area victims.

### Worked examples

A hostile spell removes 3 HP from HP 3 despite 12 rawdamage: if you survive, retaliation is 1 psychic, not 6.

A willing-only allybuff cannot be reflected into an unwilling original caster merely because it selected you.

## Stormcaller (`stormcaller`)

**Prerequisite:** Spellcasting ability, proficiency in Nature or Spellcraft

Require actual spellcasting AND (Nature proficiency OR a separately established Spellcraft credential). Spellcraft is not an Arcana alias; if absent, use the Nature alternative. Once per beneficial SR/LR, an Action places a fixed 15 ft radius Static Field at a perceived point within 60 ft and line of effect, requiring concentration for up to one minute. It affects all creatures, including allies: first actual entry or regular start inside per target per numbered round deals 1d6 lightning automatically. Placement covering a creature counts as entry once. While inside an active field, creatures have disadvantage on DEX saves, ending immediately on exit; actual immunities/suppression apply. Outdoors during an established storm, choose a 20 ft radius at creation. A separate once-SR/LR Action, Stormstep, teleports you up to 30 ft to a visible fitting unoccupied space with line of effect. Every other creature within 5 ft of arrival makes a DEX save against your actual casting DC for 1d8 thunder, half on success. NEW select the actual owned casting route at acquisition for both feat activations. Your afterimage supplies half cover until your next regular start only when the geometric ray from the incoming effect origin to your new position passes through your previous occupied space; it is not a solid object or general AC bonus. During an actual outdoor storm, your lightning spells also ignore half cover, but not stronger cover. These activations are nonspell magical feat techniques; they do not create weather, RP or extra casting resources.
NEW storm-size choice is fixed at creation, as this proposal specifies:20ft requires actual outdoor-storm premises at that placement. A later weather change does not enlarge or shrink the placed field; suppression, concentration and its original minute deadline still end it. The separate half-cover benefit checks the actual outdoor-storm predicate when each lightning spell attack resolves. These are source-authoring completions, not permission to interpret the named storm’s setting origin.

### Worked examples

Entering then exiting/reentering thefield inoneround deals onlyonepulse tothatcreature.

A normalrainstorm canqualifyif theDirector’s actualweatherrecord saysstorm; thefeat doesnotdeclareone.

## Temporal Theory (`temporal_theory`)

**Prerequisite:** Intelligence 15+, proficiency in Arcana, level 8+

At your original regular-turn end, bank at most one genuinely unused NORMAL allowance: your wholly unspent movement budget, ordinary free object interaction, or unused ordinary Bonus Action. You must be conscious, able to act and actually possess it; prohibited, extra, borrowed, banked, readied or generated allowances cannot fund a token. Movement requires zero movement spent this turn; snapshot actual legal distance and modes. Consume the chosen allowance into one typed token; hold at most two, expiring at encounter end. On a later own regular turn, spend at most one token of each type without Action for its exact purpose: move up to min(stored feet, current legal normal Speed), one ordinary interaction, or one currently legal BA ability. Pay current terrain; modes must still exist. No conversion to full Action, Reaction, work time or new token, and no refresh of feature uses/cadences. After the second token spent in the real encounter, record one irrevocable fatigue cost due at encounter end: NEW one Core Exhaustion level, with actual immunity/recovery and lethal level 6 rules. Further spending creates no extra fatigue under this source but cannot erase the cost. No Time Loop, rewind or resource restoration.

### Worked examples

Store a wholly unused 30 ft movement allowance. If current Speed is 20 when later spent, it supplies at most 20 additional feet, with current terrain costs.

A Bonus Action supplied by Mystic Recoil cannot be banked into a persistent token.

## Trapcasting (`trapcasting`)

**Prerequisite:** Conjure Flora or Verdant Bond

Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.
NEW phase exception is explicit: its first eligible hostile-entry attack may occur on that actual entry outside the ordinary attached phase, but spends the same owner-round offensive companion allowance immediately. Its paid burst likewise spends that allowance; neither can occur when it is already spent. Placement itself is not an entry-trigger unless this exact procedure expressly says so. General Conjure Flora commands retain their attached phase, shared Bonus Action and sensory channel.

### Worked examples

Forced hostile entry can trigger a plant, but another plant cannot produce a second offensive outcome after the group allowance is spent that round.

Detonation consumes the actual plant even if every creature saves. An expired plant cannot be detonated.

## Verdant Bond (`verdant_bond`)

**Prerequisite:** Proficiency in Nature, spellcasting ability

While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Distinct eligible flat feat bonuses add under FS-03; this same feat contributes only once. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.
SOURCE ally scope: the owner may be the one chosen message recipient. It triggers on that recipient’s first genuinely future qualifying passage after recording, not immediate creation beside the tree; the audible stored message is not private telepathy or general tree fluency.

### Worked examples

With an active qualifying plant, a spell actually cast through the Ranger route gains the stated+1DC. An independently acquired eligible Spell Focus+1 adds, for+2total; duplicate Verdant Bond does not.

The stored message is audible to anyone close enough to hear when the designated ally triggers it.

## Voltyros Pact (`voltyros_pact`)

**Prerequisite:** Stormcaller or Lightning Affinity, level 6+

Require character 6 AND (Stormcaller OR Lightning Affinity); preserve the named pact/plane story undecided. Once per personal noncopy lightning spell’s initial resolution, choose one additional creature within 15 ft of one original recipient, perceived with line of effect from that recipient. It must satisfy original creature eligibility and not already be targeted by that cast. Deal only half the selected original native lightning packet before defenses, rounded down; use the original DC/save ability for a fresh save or original attack bonus for a fresh attack, with original half/none on success. No other riders, new cast or chain from a chain. After one entire original start-to-next-start interval without any position change, gain Eye of the Tempest: resistance to all damage and+2 to one immediate native packet/shared roll of each personal spell until the following regular start. Any movement, teleport or forced displacement ends Eye immediately; riding a moving mount counts as movement. Repeated stationary intervals may renew without stacking. Separately, once LR use Action for a 30 ft-long 5 ft-wide lightning line: all creatures DEX save,4d6 lightning half success. DC=8+PB+one actual casting ability selected at acquisition, or INT if no casting source. The line is a magical nonspell feat technique, with noRPpool or weather creation.
The Eye bonus is+2 to one immediate native packet/shared roll of each personal spell as printed here; it is not limited to lightning spells. Half-damage chaining uses a resolved native lightning packet, not an attack that missed, a reflected/copy result, external rider or new target-independent resource event. Existing stance, terrain, body and actual stationary interval rules remain.

### Worked examples

Native 17 lightning damage gives a chain base of 8 before the new target’s save and defenses; that child cannot chain again.

Forced movement prevents the stationary interval. Riding a moving mount is not stationary.

## Wounding Magic (`wounding_magic`)

**Prerequisite:** Spellcasting ability

After your personally cast noncopy spell deals positive resolved damage, optionally apply one Agony record to one living damaged target, once per owner/target/numbered round. Reapplication refreshes one profile without stacked dice. It deals 1d4 necrotic at the next three original target regular-start markers; a CON save against the generating cast DC at each affected regular end, including a current turn if applicable, ends it. The final third scheduled pulse ends the record after damage; no extra ending save afterward. It is a magical ongoing wound, not Core Wound, maximum HP injury or Bleeding by name. NEW a legal positive-potential magical heal or Action Medicine vs source DC ends it; suppressed records remain curable. While active, disadvantage applies only to actual existing CON saves to regain HP and actual saves against resurrection effects; no such save is invented. Death suspends living damage, retaining only the unexpired record tied to that exact death instance until the original third-start deadline; missed pulses are consumed, never backlogged. A legal revival closes that corpse-specific resurrection rider and retains only any still-future living pulse schedule until cured/expired. This grants no resurrection block or permission. Secondary ticks cannot create further Agony, copies, lifesteal or resource procs. Any independent Necrotic Affinity seal needs its own real fatal-root predicate.

### Worked examples

The first 1d4 pulse resolves at the target’s regular start; a successful CON save at its regular end removes the remaining pulses.

A normal heal with no save gains no new saving throw. Death skips living pulses without extending the original deadline or granting resurrection permission.
