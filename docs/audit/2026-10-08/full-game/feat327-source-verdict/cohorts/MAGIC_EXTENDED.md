# Magic Extended — final source-authoring directions

FEAT327-SOURCE-2026-10-11; internal review document. No exact-card promotion. Read with FS-01–16 and the final supplement register. Original data and legacy alternatives are retained in the JSON register.

## MX-01 — Arcane Armor (`arcane_armor`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/0`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve whether the reaction-trigger qualifier limits both AC and saves, or only saves, and what concentrating contributes after casting ends. Identify casting-triggered reactions, onset before interruption, exact expiry, stacking and level4 gate. Preserve inactive+5-percent legacy text without turning the ward into general resistance.

**Decision:** Adopt the narrow grammatical scope on both AC and saves: only casting-triggered Reactions, not all attacks during concentration; keep+1, not legacy percentage resistance.

### Complete authoring text

Require character level 4. NEW the qualifier governs BOTH+1 AC and+1 saving throws: they apply only against a Reaction whose actual printed trigger is your casting or continuing concentration on a spell. Begin eligibility at commitment of that cast, before interruption; end when its casting/held concentration/ordinary concentration ends. Merely attacking a concentrating caster is insufficient. The relevant Reaction must itself cause an attack against you or a save you make; Counterspell’s caster-side ability check is neither and receives no penalty. A triggered attack still uses ordinary critical rules. The bonus is passive, grants no Reaction, and cannot protect unrelated attacks or ongoing damage. Distinct eligible flat feat bonuses add under FS-03 after existing non-feat families resolve; duplicate Arcane Armor contributes only once. Preserve the alternative broad AC reading and old 5% resistance as inactive source alternatives.

### Worked boundaries

**MX-01-E01.** An actual on-cast Reaction attacks AC 14: eligible+1 makes AC 15, unless a stronger same-stat bonus already governs.

**MX-01-E02.** An enemy’s ordinary attack during your ongoing concentration receives no Arcane Armor modifier.


## MX-02 — Arcane Flexibility (`arcane_flexibility`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/1`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Bind prepared spells to an actual class repertoire and same class-specific rank; specify completed Short Rest, replacement timing, losing a currently maintained spell and temporary/copied grants. Does this permit a class without prepared spells to prepare one? Preserve the existing acquisition limits and no imported preparation subsystem.

**Decision:** Keep one actual same-rank owned repertoire substitution at a beneficial short rest; no class-list union, free knowledge or duplicate selection.

### Complete authoring text

At completion of each beneficial Short Rest, optionally replace exactly one currently prepared spell in one actual class preparation list with another spell of the same rank in that same class. It must already be a legal known/book/repertoire choice under that class’s preparation procedure and current class level/school limits. Decide after ordinary rest endpoints/recovery; record the previous and replacement preparation. No extra prepared capacity, learned spell, copied grant or class alias. A class without a preparation list gains no new list. NEW unpreparing does not retroactively dispel a legally ongoing spell; maintain its actual concentration/deadline, but no new cast through the removed preparation. One exchange per rest event across classes, not one per class or duplicate feat representation.

### Worked boundaries

**MX-02-E01.** A Wizard exchanges one prepared Wizard-rank 2 spell for another already eligible Wizard-rank 2 spell after SR.

**MX-02-E02.** Knowing the replacement through another class at rank 2 does not establish Wizard preparation eligibility.


## MX-03 — Arcane Pulse (`arcane_pulse`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/2`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define spell versus nonspell classification, casting ability/DC for a level7 character without casting, actual shared RP access and payment. Specify self-centered10-foot geometry, sight/line, chosen targets including self, one damage roll, Strength save, push direction/collision and half rounding. No resource pool is created by an unstated prerequisite.

**Decision:** Adopt3RP Action, own10ft radius and3d6force/STR push resolution as NEW; actual RP capacity required, no Warrior pool invented.

### Complete authoring text

At character level 7, use an Action and pay 3 actual shared RP. NEW this is a magical feat technique, not an ordinary spell: no rank, spell components, Counterspell window or Dissonance/Refrain from this activation. At acquisition choose INT, WIS or CHA permanently for this feat’s DC=8+PB+that current modifier; this supplies neither spellcasting qualification norRPcapacity. Center a 10 ft radius on your own occupied space under ordinary area geometry. Choose perceived creatures with line of effect in it, including yourself if desired, before rolling. Roll 3d6 force once. Each makesSTRsave: failure full damage then push up to 10 ft directly away from the origin along a legal unobstructed route; success half damage rounded down, no push. Self can take damage but has no away-from-self push. Stop at obstruction/occupied destination; no collision damage, opportunity attack or unstated prone. Large bodies retain real fitting requirements. Immunity to forced movement blocks only push.

### Worked boundaries

**MX-03-E01.** A level 7 Warrior with noRPpool cannot pay 3 RP, even though acquiring this feat was legal.

**MX-03-E02.** A shared roll 11 produces 11 on failure or 5 on success; a wall 3 ft behind the victim limits actual push.


## MX-04 — Arcane Recall (`arcane_recall`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/3`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define actual completed ranked cast, tier/rank, min(rank,5) recovery, RP ceiling, zero-cost or interrupted casts, rest use and timing relative to other refunds. Decide paid-cost/funding safeguards with current recovery rules; preserve current effect separately from regain-used-spell legacy.

**Decision:** Keep one bounded return after a completed ranked cast with actual unrefunded payment/headroom, not rank-based free RP from a waived cast.

### Complete authoring text

After a completed personal rank 1–9 cast, optionally consume the once LR use to recover min(actual rank,5, RP headroom, unrefunded RP actually paid for that cast). NEW the funding ceiling counts only actual personal RP expenditure, including legal surcharges; it cannot refund charges, HP, other pools, free price or an ally’s contribution. Register the cast’s paid RP and every direct refund/recovery against the same expense once, across this feat and other refund sources; choose a legal order without exceeding that expense. A legal fully saved/missed cast qualifies; countered/interrupted, copied or released-again casts do not. A readied cast qualifies once when successfully prepared, never at release. If the computed recovery is 0, decline before committing the use; no newRPpool/cap. Ordinary ongoing effects need not finish their entire duration.

### Worked boundaries

**MX-04-E01.** Rank 3 paid 5 RP with enough headroom returns 3; a previous 4 RP refund leaves at most 1 for Recall.

**MX-04-E02.** A free charged rank 3 cast cannot produce 3 RP through this proposed funding rule.


## MX-05 — Arcane Transfusion (`arcane_transfusion`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/4`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Specify declared restoration amount and actual RP headroom before paying2 necrotic damage per RP; define unreducible damage versus true-HP funding, temporary HP, zeroHP/incapacity, Wounds, concentration and interrupts. Bind proficiency cap, Bonus Action and Long Rest ledger; prevent recovery/healing loops without silently importing Blood Ritual costs.

**Decision:** Adopt explicit normal-HP-funded necrotic damage cost, leaving at least1 before Wound consequences; it is not Temp HP or a refundable resource loop.

### Complete authoring text

Once LR as a Bonus Action, choose integerN from 1 through min(current PB, actualRPheadroom) and preflight the shared normal HP funding rule for 2 Nnecrotic damage. Commit BA/use, then resolve that cost as one packet with normal Wound/death/concentration consequences. If still alive after the complete packet, restore exactlyNactual RP, capped by then-current capacity; later headroom loss does not refund HP. NEW this explicitly bypasses temp HP, resistance, redirection and floors for funding while retaining damage consequences. No use at 0 HP without an exact independent BA permission and sufficient actual funding, which the at-least 1 HP requirement normally forbids. No heal, charge creation, maximum RP increase or incidental resource trigger from self-damage. Ordinary later paid healing remains possible; it does not reset this LR use.

### Worked boundaries

**MX-05-E01.** PB 3 and 2 missing RP allowN 2: lose 4 normal HP and, if surviving, regain 2 RP.

**MX-05-E02.** HP 4 cannot fundN 2 even with 20 temp HP; the illegal attempt spends nothing.


## MX-06 — Blood Magic (`blood_magic`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/5`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve spell tier0, actual paid casting route, declaration and the choice of+1 DC or one damage die. Define die type/packet/targets/critical/maximized cases, all-save versus one-save scope and the2xTier unreducible-necrotic payment at zeroHP. Use Short Rest ledger; no double dipping with reviewed Blood Ritual or copied results.

**Decision:** Adopt normal-HP-funded typed damage cost and one DC/die option, preserving real Wound/concentration consequences; not the already reviewed Blood Ritual.

### Complete authoring text

Once per beneficial SR or LR, when committing an actual spell, declare either+1 to that cast’s spell-save DC or one extra native damage die under the shared added-die procedure. Pay the spell’s actual ordinary costs plus 2×its actual rank as the shared unreducible-necrotic normal HP cost, before establishing its new concentration and opening interruption. Existing concentration must face the self-damage normally before displacement; death/action loss aborts the unfinished spell without refund. Rank 0 explicitly costs 0 HP but still spends the feat use; a cantrip is not excluded by the source. DC mode changes all actual saves caused by that same cast, including its legal repeats, while that cast lasts; it supplies no saves to automatic effects and no inherited DC for unrelated children. Damage mode cannot modify a flat-only or nondamaging spell. No two modes, doubled cast orHPrefund; copying never regrants the modifier.

### Worked boundaries

**MX-06-E01.** Rank 2 spell DC 14 becomes 15 after 4 normal HP cost; an ordinary area save for each target uses 15.

**MX-06-E02.** A flat damage effect has no eligible die for die mode; choose a legal DC mode or decline before payment.


## MX-07 — Channeled Flow (`channeled_flow`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/6`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Preserve current one maintained Action replaced by one Bonus Action per Short Rest, not the legacy50-percent duration extension. Define qualifying actual later-turn maintenance, costs/concentration, prohibited actions, which turn spends the use and whether other commands share the same action budget.

**Decision:** Keep conversion of one genuinely required upkeep Action only, with original maintenance costs and concentration; no conversion of initial casting or optional attacks.

### Complete authoring text

Once per beneficial SR or LR, on your own actual later turn, replace one Action explicitly required solely to maintain one of your already established spells with one Bonus Action. Declare and consume at that maintenance commitment. Preserve concentration, RP/material upkeep, targeting, existing pulse/command limits and the original spell deadline. It cannot shorten initial casting, Ready setup, a ritual, an attack granted by the spell, or an optional Action to issue a new damaging command unless that exact source identifies it as required maintenance. An Action that combines required maintenance with another benefit retains the combined printed payload but still supplies no second occurrence. One actual BA must be available; Incapacitated/other restrictions still apply. The source’s prior 50% duration wording remains an inactive alternative.

### Worked boundaries

**MX-07-E01.** Maintaining an existing spell with an explicit Action upkeep uses BA once, retaining its required 2 RP upkeep.

**MX-07-E02.** A summoned creature’s optional attack command is not automatically qualifying maintenance.


## MX-08 — Concentrated Will (`concentrated_will`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/7`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Bind+2 to actual Constitution concentration saves, spell and nonspell concentration scope, multi-packet damage timing, advantage/disadvantage and stacking with Combat Casting/War Caster. Level5 is a prerequisite, not a caster level or new ability modifier.

**Decision:** Keep+2 on actual concentration Constitution saves, including qualifying nonspell concentration; distinct applicable feat bonuses add, no generic Wound/save bonus.

### Complete authoring text

At character level 5, gain+2 on actualCONsaving throws made to maintain concentration, including nonspell concentration that explicitly uses the same save. Apply current same-stat flat-bonus arbitration; ordinary advantage/disadvantage and proficiency remain independent. Each genuinely separate damage packet generates only its actual required save, not one per damage type or extra feat test. No modifier to unrelated CON, Wound or death saves, automatic concentration loss from incapacity/death, or a special source’s non-CON test. This creates neither concentration capacity nor permission to act at 0 HP. A legally held Ready spell has actual concentration and qualifies.

### Worked boundaries

**MX-08-E01.** A real damage concentrationCONsave gets the feat bonus and can also have existing advantage.

**MX-08-E02.** Becoming Incapacitated ends ordinary concentration without a save; the feat cannot invent a roll.


## MX-09 — Counterspell Adept (`counterspell_adept`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/8`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** The description/legacy say+4 while active effect says+2 checks or+1 counterspell DC. Resolve that source conflict explicitly against the actual Counterspell procedure, what interrupt checks include, and whether the alternative DC clause has any current target. Do not apply both branches or grant Counterspell access.

**Decision:** Select current+2 interrupt checks and conditional+1 counter-save DC over legacy+4. Ordinary Counterspell is its actual task; no saving throw is invented.

### Complete authoring text

At character level 6, NEW select the active effect’s+2 over preserved description/legacy+4. Add+2 to an actual ability/task check whose operative source directly counters or interrupts a pending spell, with FS-03 distinct flat feat bonuses additive after each existing non-feat family resolves. Ordinary Counterspell remains actual casting ability+PB versus 10+2×trigger rank, with task degrees/natural shifts collapsed to success/failure. The alternative+1 DC branch applies only if a separately operational counter source truly uses its own save DC; current ordinary and cited class Counterspells use checks, so noDCbranch applies to them. Never apply both to one attempt. This feat grants no spell, Reaction, extra attempt, automatic low-rank success, spell attack bonus or check to identify magic.

### Worked boundaries

**MX-09-E01.** Against rank 3, Counterspell DC 16 and ability+PB 5 become check+7 before rolling.

**MX-09-E02.** Mystic Focus’s spell-attack bonus does not apply to that task check; neither feat invents a penetration check.


## MX-10 — Dispel Precision (`dispel_precision`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/9`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Use actual Dispel Magic selection/check rules. Determine whether selecting the effect is already standard and whether+1 affects each actual eligible dispel check. Resolve one target with several spells, automatic endings, Dispel Mastery extra target and no invented random selector or generic antimagic permission.

**Decision:** Keep+1 only where a genuine dispelling check exists; current ordinary Dispel Magic has no check. Preserve exact selected-effect/multieffect scope.

### Complete authoring text

When a legal dispelling source would randomly select among individually eligible effects, choose its one eligible effect instead; identify an effect only to the extent the source permits. Ordinary reviewed Dispel Magic already chooses one perceptible ongoing spell rank 0–3 and ends it automatically: this feat changes neither its target count nor its rank/protection limits. Add+1 only to a real dispel check explicitly required by a different operative source. No check is invented for an automatic success, and no roll can exceed a source’s allowed scope. If the separate proposed Dispel Mastery is adopted, each of its legal targets retains its own existing procedure; Precision does not duplicate attempts. Hidden/protected curses, permanent magic items and class engines remain outside ordinary Dispel Magic.

### Worked boundaries

**MX-10-E01.** Choose one visible rank 2 spell among three on a creature; ordinary Dispel Magic ends it without a+1 roll.

**MX-10-E02.** A rank 5 effect remains ineligible for that ordinary spell despite this feat.


## MX-11 — Echo Spell (`echo_spell`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/10`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define creation timing, use/cost, next regular start, selected numerical effect and half rounding. Bound damage/healing/buff/area packets, targets moving or becoming illegal, saves/attacks, concentration, ownership and no recursive echo/cast/resource/action generation. Preserve Tier1–3 and compare Spell Echo Chamber without merging identities.

**Decision:** Adopt one bounded delayed half-native secondary result, not a cast, resource refund, extra body or general duplicated spell; recheck genuine original targets and expiry.

### Complete authoring text

Once LR immediately after a personal rank 1–3 spell completes its initial payload, select one numeric damage, HP healing, temp HP or flat stat-bonus component and its original eligible recipients. NEW no echo from Ready preparation until actual release, copies, summons, creation, resource/action grants, movement, hard control or maxima-changing effects. Snapshot that component’s native roll/flat value before external bonuses, original attack/save rules, type, origin and source DC. At your next future regular start, if alive/conscious and any source-required concentration still holds, repeat only that component at half native value floored;0 gives no effect. Recheck original recipients’ actual range/perception/line of effect from the recorded origin, which must still exist; no replacement target. Make fresh original attack/save tests, then ordinary defenses/healing caps, without new critical dice or external damage/heal add-ons. A selected shared area retains only original recipients still in the original area. Temp HP uses the single grant ledger; a flat bonus uses strongest-family arbitration and expires at the earlier of original deadline or your next regular end. Echo heals block healing-copy/resource outputs and create no convertible excess. No new cast, RP, components or duration for the parent; an invalid echo expires without refund.
FS-08 secondary-echo flag applies: this delayed result is not another cast. Its flat bonus is a continuation of the original bonus identity/family, not a distinct feat-stacking source; the strongest original-family rule remains. No new resource, copy, hit-trigger chain or source-specific no-resource exception is created.

### Worked boundaries

**MX-11-E01.** An original native 11 force area creates a 5 force echo against original still-legal recipients, each with a fresh original save.

**MX-11-E02.** A summoned creature’s HP, attacks and future turns are not a repeatable numerical spell component.


## MX-12 — Efficient Caster (`efficient_caster`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/11`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Bind once-per-round to the existing regular-turn clock, proficiency uses per Long Rest and ranked spell eligibility. Place−1/min1 in the actual RP cost order, accounting for ancestry charges, zero-price casts, armor additions, other reductions and final Resonance Influence. Resolve use expenditure if no reduction can occur.

**Decision:** Keep finite PB uses, actual price stage and minimum1; no discount on a genuinely free cast or conversion of an independent cost into a free waiver.

### Complete authoring text

Gain PB uses per completed LR, with current PB as maximum and no mid-epoch replenishment from growth. Once per numbered round, at a personal ranked cast’s declaration, optionally reduce its otherwise payable RP by 1, minimum 1. NEW apply after existing eligible base discounts and printed extra costs including component and strain/armor additions, but before final Resonance Influence; this is a discrete reduction, not a new base-rank price. A charged/free normal-price route still pays its independent costs; use is allowed only when this stage’s actualRPprice is at least 2. A genuine reduction commits both use and round entitlement with the cast, even if a later permitted final adjustment or interruption changes the outcome. Cannot reduce charges, HP, specialresources or manufacture a 1 RP charge on a 0 RP cast. Current rank/repertoire/strain cutoff remain.

### Worked boundaries

**MX-12-E01.** A rank 1 cast’s eligible price 2 becomes 1 before a separately applicable final Influence adjustment.

**MX-12-E02.** A charged spell with only 1 independent RP surcharge offers no reducible price and spends no feat use.


## MX-13 — Energy Sink (`energy_sink`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/12`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define success-on-save OR no-damage trigger for one actual spell event, including harmless, friendly, prevented, immune, missed, ongoing and multi-target effects. Bind Reaction, PB uses, RP ceiling, actual caster attribution and zeroHP restrictions; decide anti-farming and refund limits explicitly, not by deleting one printed trigger.

**Decision:** Keep Reaction to an original hostile spell event with actual source conditions; actual Temp HP damage counts, and all source-specific no-resource flags remain.

### Complete authoring text

PB uses per completed LR; no mid-epoch refill fromPBgrowth. After one actual hostile spell event targeting/affecting you resolves, if you either succeeded on its real save OR received no positive resolved damage from that event, you may spend a Reaction/use to recover 1 RP up to your real maximum. NEW require meaningful unwilling opposition: harmless, allied, cooperative, self-authored or farming spells do not qualify. A spell attack that legally targeted you but missed, immunity, or complete prevention can satisfy the no-damage branch; temp HP absorption is damage and alone cannot. A failed save against a hostile nondamaging control spell still satisfies literal no-damage, but only if its result leaves you able to react. One grant per actual cast identity across later ticks/events; no fan-out or repeating-zone farm. Positive saved-against damage may qualify through success. Resolve full damage/control/death first; no ordinary Reaction at 0 HP. Decline before spending if noRPheadroom. This is recovery, not transfer from the attacker or a new pool.
For this trigger, actual damage includes damage absorbed by Temp HP, so a spell that damages only Temp HP is not a no-damage event. A genuine ward that prevents all damage may leave a qualifying original hostile spell event; the ward does not itself generate a second event. Every explicit no-resource source flag remains controlling; see FS-07.

### Worked boundaries

**MX-13-E01.** Successful save halves a hostile spell to 5 damage: the success branch permits oneReaction for 1 RP.

**MX-13-E02.** A missed hostile spell attack can qualify; receiving a friendly harmless cantrip cannot.


## MX-14 — Ether Anchor (`ether_anchor`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/13`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Preserve advantage plus one optional auto-success per Long Rest, not legacy immunity. Define an actual allowed save against banishment/forced teleport/displacement, declaration and no-save effects. Keep movement/space rules and do not invent planes, destinations or cosmological eligibility.

**Decision:** Keep existing forced-teleport/banishment saves and one post-failure autosuccess; no save or general relocation immunity is created.

### Complete authoring text

At character level 12, gain advantage on actual saving throws against an effect that would banish, forcibly teleport or displace you between planes. Once LR, after such a save fails but before consequences, optionally replace that failure with success; use the source’s actual success outcome, which may retain other effects. No Action or Reaction is required. It does not create a save against a save-less effect, convert willing travel to hostility, anchor nearby creatures, reveal destinations or permit an otherwise illegal movement. A save against damage accompanying independent displacement qualifies only if that same save actually determines the unwanted displacement. Existing explicit unpreventable/no-replacement rules control. No permanent immunity or new cosmological fact is implied.

### Worked boundaries

**MX-14-E01.** A failed actual banishment save becomes success and consumes theLRuse.

**MX-14-E02.** A source with automatic displacement and no save supplies no roll for this feat to improve.


## MX-15 — Flash Cast (`flash_cast`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/14`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define normal one-Action casting, one Bonus Action, Long Rest use, costs/components and the whole-turn ban on another ranked spell before or after use. Resolve reaction casts on that turn, cantrips, extra turns, copied releases and interruption without importing a universal bonus-action spell restriction.

**Decision:** Adopt one Action-to-BA conversion and the whole-actual-turn ranked-spell restriction, including earlier casts and later Reactions; no second Action grant.

### Complete authoring text

Once LR, declare an actually known/prepared spell with printed normal casting time oneAction as a Bonus Action instead; maintain every other access, component, RP, concentration and strain rule. NEW the whole actual turn, including any on-turn Reaction casts, may contain no other ranked cast before or after this cast. Preflight the turn’s existing cast history; committing this feat establishes the restriction even if countered. The chosen spell may be rank 0; other cantrips remain legal with their actual action resources. A later genuine extra turn is a distinct turn for this prohibition but does not refresh theLRuse or other regular-turn budgets. Ready release/copy with no new cast is not another ranked cast, while preparing a readied ranked spell is. No long-cast compression, Reaction conversion, free BA or universal restriction on unrelated turns.

### Worked boundaries

**MX-15-E01.** After casting a ranked spell as anAction this turn, Flash Cast is ineligible even for a cantrip.

**MX-15-E02.** Flash-casting a rank 2 spell allows a later legalAction cantrip but forbids an on-turn ranked Counterspell.


## MX-16 — Foresight Surge (`foresight_surge`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/15`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Preserve both+2 future initiative for one hour and one-place movement when already rolled. Define actual Divination cast, repeated applications, round-boundary update, top slot/ties, pending turn cursor and extra-turn conservation. A move in order must not create or delete a regular turn, refresh or pulse.

**Decision:** Adopt+2 initiative and one bounded next-round baseline ordering advance; integrate actual Future Echo permutation restoration without removing incapacitated actors or granting turns.

### Complete authoring text

After a completed actual Divination cast, gain a nonstacking+2 to future initiative rolls for one elapsed hour, refreshing that deadline on later eligible casts. The selected casting class must use Divination for this identity. If already participating in rolled initiative, also queue one move up one baseline place at the next numbered-round boundary. NEW one queued move per owner per boundary; repeated casts cannot accumulate jumps. At that boundary finish previous-round events, restore temporary permutations, then process pending advances in stable activation order by swapping the owner with the immediately preceding still-participating baseline actor; top actor stays. Apply later reviewed temporary permutations, such as Future Echo, to the resulting baseline. Every participant still receives one regular slot. A departed actor without a retained initiative slot loses its pending advance without makeup. Incapacitation alone does not remove an actor’s regular slot or this pending ordering change. Existing virtual deadlines, recharge, periodic clocks and spent budgets do not move or refresh; no reroll or extra turn.
For actual Future Echo, restore an expiring permutation first, apply this feat’s pending baseline advances once in the stated stable order, then apply a newly established Future Echo permutation to the resulting baseline. Preserve actual slots and spent turns; no extra turn or resource refresh occurs.

### Worked boundaries

**MX-16-E01.** OrderA, B, C withCqueued becomesA, C, B next round;Cdoes not act again in the current round.

**MX-16-E02.** Three Divination casts before that boundary still queue only one advance forC.


## MX-17 — Illusionist’s Trick (`illusionist_s_trick`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/16`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Identify actual illusory creature/object sources and their normal ending/investigation procedure; investigation save is not automatically a core save type. Define first hit/interaction, simultaneous invalidation, persistence through current turn, observers knowing the truth, concentration and nonphysical blocking. No real HP, extra creature or automatic belief.

**Decision:** Keep narrow delay of a genuine interaction-caused illusion ending only; disbelief, visible contradictions, concentration loss and independent expiry remain.

### Complete authoring text

For each actual illusory creature/object you personally create, the first attack or interaction that would end that particular illusion’s existence instead delays only that ending until the current actual turn ends. NEW outside initiative use the end of the current canonical six-second window. It remains nonphysical and observers retain information already obtained; known illusions do not regain concealment, cover, belief or control. Losing required concentration, natural expiry, dispel, source death or another independent ending still ends it immediately. The feat does not postpone an observer’s ordinary Investigation check or direct physical proof unless that source’s actual rule specifically ends the illusion itself. At the deferred endpoint end the illusion as originally required; where the source only grants a disbelief test rather than termination, use its actual Investigation check/save at its printed timing, with no free new save type. Current Minor Illusion/Silent Image physical interaction reveals to observers but does not end the global image, so normally does not trigger this delay.

### Worked boundaries

**MX-17-E01.** A source illusion explicitly destroyed by a hit can remain visibly present until this turn ends, with no substance.

**MX-17-E02.** Walking through Silent Image reveals it immediately; this feat cannot make the witness believe the wall is solid.


## MX-18 — Lingering Magic (`lingering_magic`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/17`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Use active+1 round once per nonconcentration spell, not description/legacy20percent. Define round-to-seconds/end-marker conversion for minute/hour spells, delayed riders, initial/recurring pulses, until-discharged effects and explicit caps. No extra charge, summon use or extension after an independent ending condition.

**Decision:** Select current one-round extension over legacy20%, retaining non-concentration and actual independent endpoints; it creates no additional fixed-count pulses.

### Complete authoring text

NEW select the active+1 round wording over preserved 20%. At a completed nonconcentration spell’s creation, extend its finite stated duration of at least one round by exactly one six-second/regular-marker interval, once per original cast. Round effects add one original regular marker; minute/hour deadlines add 6 elapsed seconds. A Ready spell’s temporary held concentration does not disqualify a normally nonconcentration payload; extend its payload at release, never its Ready deadline. Independently capped charges, target counts, specified number of pulses, item stock and discharge/consumption endpoints remain. An ongoing effect whose ordinary pulse exists solely while its duration persists may get the one naturally reached extra pulse; an explicit three-pulse effect remains three. No extension of instantaneous/permanent effects, resurrection windows classified separately from spell duration, concentration spells, linked separate conditions, or an independent end such as destroyed support. No stacking with itself or repeated recasting of the same instance.

### Worked boundaries

**MX-18-E01.** A nonconcentration 60 second effect lasts 66 seconds unless independently discharged earlier.

**MX-18-E02.** A printed three-pulse effect still has three pulses even if its remaining cosmetic duration extends.


## MX-19 — Magical Fortitude (`magical_fortitude`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/18`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define+2 on actual saving throws caused by spells, including repeat/concentration/death saves where applicable, and spell versus magical class/item effects. Constitution13 does not grant proficiency or spellcasting. Resolve stacking with other feats and jewelry without changing source save DCs.

**Decision:** Keep+2 actual saves against direct spell effects, including source repeats; adopt distinct-flat-feat addition without extending it to indirect Wound or concentration saves.

### Complete authoring text

Gain+2 to your actual saving throws directly required by an operative spell’s payload, including later repeat saves and a spell explicitly requiring a save to maintain another effect. NEW FS-03 applies: a distinct eligible+2 save feat adds to this+2, giving+4; duplicate copies of this feat do not. Existing non-feat families retain their own arbitration. Ordinary damage-induced concentrationCONsaves, Core Wound saves and death saves are consequences of shared life/concentration rules rather than the damaging spell’s printed payload and receive no bonus from this feat; Concentrated Will has its own exact concentration scope. A spell that directly calls for a death-effect saving throw can qualify, but ordinary death saves do not. Magical nonspell class/item/feat effects are not spells unless their actual source classifies the activation as one. CON 13 is acquisition only; no new proficiency, casting ability or defense against a Counterspell task check.

### Worked boundaries

**MX-19-E01.** A repeatWISsave explicitly supplied by an ongoing spell gains+2.

**MX-19-E02.** TheCONsave to maintain concentration after taking a spell’s damage uses Concentrated Will if owned, not this feat.


## MX-20 — Mana Burn (`mana_burn`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/19`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Bind actual failed save against your damaging spell, including successful damage prevention, repeated saves, RP-less creatures and minimum0. Define one recipient-wide once-per-round ledger across multiple users, phase timing, no RP transfer to caster and no charge/slot pool substitution.

**Decision:** Keep at most1 actual RP lost per target/numbered round on the relevant failed damaging-spell save; no RC/slot conversion, RP creation or transfer.

### Complete authoring text

After a creature fails an actual save against your personally cast damaging spell, remove 1 from its realRPpool, minimum 0. NEW damaging means that same spell application has a native damage component governed by that save; full prevention/immunity may leave 0 damage without negating the failed-save trigger. A repeat save solely ending nondamaging control after earlier damage does not qualify. Commit one recipient-wide Mana Burn entitlement per numbered round across all owners/casts on the first qualifying failure with anRPpool, even at RP 0; no further loss that round. Resolve native damage and immediate survival replacements first, then loss if the target still exists as a living resource holder. No transfer to you, charge/RC/slot substitution, maximum reduction or loss from RP-less creatures. Copies, echoes and reflected packets cannot create a fresh proc.

### Worked boundaries

**MX-20-E01.** Two casters trigger Mana Burn against the same RP 4 foe this round: total loss is 1, leaving 3.

**MX-20-E02.** A target immune to the damage can still lose 1 RP after failing the associated save; an RP-less monster loses nothing.


## MX-21 — Mental Buffer (`mental_buffer`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/20`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define the exact source control components called confused/dominated/mistaken-allies and automatic versus voluntary use. Specify prevention versus suppression until end of next regular turn, underlying duration/save clocks, recurrence, multiple components and reactivation. Do not turn one-turn relief into a cure or unrestricted control immunity.

**Decision:** Adopt one bounded delayed application interval for supported confusion/misidentification control; no arbitrary condition cure or replay of suppressed pulses.

### Complete authoring text

Once LR, when a new source application would impose confusion/randomized action selection, a dominated/commanded Action or turn, or an explicit inability to distinguish friend from foe, voluntarily suppress only that application’s eligible control components through the end of your next future regular turn. No Action/Reaction is required; choose before those components first take effect. NEW qualify by actual written behavior, not a condition’s suggestive name. Ordinary Charmed/Frightened alone, illusion disbelief, blindness, truthful uncertainty and incapacity without such a component do not qualify. Preserve unrelated damage/slow and the original source, duration, concentration, repeat saves and spent hard-control entitlement. Suppressed clocks continue; legal ending saves still occur. If the original component has already expired or been cured by the boundary it never returns; otherwise it resumes for its remaining duration without replaying a past commanded turn. One application only, not immunity to later separate sources.

### Worked boundaries

**MX-21-E01.** A dominated Action scheduled inside the protected interval is skipped, not stored for a later extra command.

**MX-21-E02.** Another source’s independent Stunned effect remains operative.


## MX-22 — Mirror Cast (`mirror_cast`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/21`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define a real visible reflective surface within60ft, selecting the origin at cast time, its space/size, range/line/sight requirements, Self/Touch/cones, hostile-held surfaces, moving/destroyed mirrors and ongoing effects. Preserve caster ownership, actions, components, RP and Long Rest use; no duplicate caster or remote senses.

**Decision:** Adopt finite real mirror-origin redirection with actual visibility, line of effect and caster targeting; no remote Touch, mirror-created sight or continuing tether.

### Complete authoring text

Once LR at cast declaration choose a real reflective surface you can see within 60 ft of your actual body. NEW require an unobstructed line of effect from you to that surface, at least hand-sized, sufficiently exposed to form a recognizable reflection; a drawn picture of a mirror is insufficient. Choose an unoccupied origin point immediately at its visible face. Measure spell range/line of effect and area orientation from that point; you still must personally perceive targets where the spell requires it, receiving no remote senses. Self-area/cone origins can relocate, but a Self-only body buff still affects you and Touch spells still require actual touch; no remote grasp. Hostile-held surfaces may serve if visibly legal; no possession or movement of the object. Commit ordinary costs/components/feat use at your body, preserving its interruption window. The origin is snapshotted for immediate resolution; destruction before resolution fails the changed origin with no refund. Ongoing created areas retain their actual fixed/moving rules and deadlines; the mirror is neither a second caster nor an unprinted tether.

### Worked boundaries

**MX-22-E01.** A cone can originate at a visible mirror 40 ft away and point along a chosen legal direction.

**MX-22-E02.** An unseen creature behind the mirror gains no free visibility; a Touch heal cannot cross 40 ft through it.


## MX-23 — Mystic Focus (`mystic_focus`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/22`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve active+1 spell attacks and checks versus description/legacy+2 spell penetration. Define actual magical-resistance checks from sourced mechanics and stacking with Spell Penetration. No invented resistance statistic, Spell Focus identity or universal spell-save-DC bonus.

**Decision:** Select current+1 spell attacks/real resistance checks over legacy+2 penetration; distinct feat bonuses add, but absent checks are not created.

### Complete authoring text

At character level 6, NEW choose active+1 rather than legacy/description+2 penetration. Gain+1 on actual spell attack rolls and actual checks explicitly required to overcome magical resistance. NEW distinct applicable flat feat bonuses add under FS-03; resolve existing class/spell/item families first without changing their rules. No generic resistance check exists: ordinary damage resistance still halves its eligible damage and spell resistance that grants save advantage is not a caster check. Apply the second branch only to an operative source’s real test. This is not Spell Focus, supplies no saveDCbonus, spell access, damage increase or extra Counterspell/Dispel check. A Counterspell check is interruption, not overcoming magical resistance unless its exact source separately establishes that predicate.

### Worked boundaries

**MX-23-E01.** A legal spell attack+6 becomes+7 if no stronger applicable flat bonus replaces it.

**MX-23-E02.** A creature with fire resistance retains that resistance; there is no new+1 penetration roll.


## MX-24 — Mystic Recoil (`mystic_recoil`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/23`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define countered versus all targets succeed, including no-save/mixed-target/automatic-success spells and invalid targets. Specify use declaration, next regular turn extra Bonus Action, expiration and restrictions on ranked spells/commands. Preserve once per Short Rest and prevent repeated failure/echo events from generating extra actions.

**Decision:** Adopt extra bounded non-ranked-spell BA only after actual countering or all initial recipients genuinely saving; no empty-set trigger or extra full Action.

### Complete authoring text

Once SR/LR after your own actual spell is countered, or after every originally legal recipient of its initial save-based payload actually succeeds on every required initial save, optionally commit the use and queue one extra BA for your next future regular turn. NEW require at least one actual initial save and all original recipients resolved legally; a no-save, mixed attack/save or lost-target cast cannot qualify by vacuous success. An automatic successful save counts where a real save was called for. No copying/echoing or each-tick retrigger. The BA becomes available on that one regular turn, even if other BA is spent, and expires unused at its end; incapacity creates no makeup. It may perform an actually acquired legal BA, including ordinary command, but cannot prepare/cast a ranked spell or create more actions/banked allowances. It does not bypass shared companion offense, concentration, RP or other use caps. No extra fullAction, Reaction or duration-clock tick.

### Worked boundaries

**MX-24-E01.** Both targets succeed on the spell’s only two initial saves: next regular turn gains one restricted BA.

**MX-24-E02.** One target failed but was immune to damage: the all-success branch does not trigger.


## MX-25 — Overchannel (`overchannel`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/24`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Use active one extra damage die per spell tier and2xTier force backlash after resolution, not legacy25percent. Specify dice type/packets/targets/critical interactions, rank0, miss/no damage/counterspell, concentration and zeroHP. Preserve unreducible backlash and Long Rest use without manufacturing healing or refund loops.

**Decision:** Select current one native damage die per rank and2×rank unreducible post-attempt force backlash over legacy25%; actual Temp HP can absorb this distinct backlash.

### Complete authoring text

Once LR at damaging spell declaration, add one existing native damage die per actual spell rank to one immediate native packet under the shared added-die rule. NEW choose this active rule over legacy 25%. Commit use with the cast. After its immediate attempted resolution, including a miss, all saves or Counterspell, take 2×rank force backlash as one self-damage event. This damage cannot be reduced or redirected; NEW it does pass through real temp HP before normal HP, unlike the explicitly proposed normal HP-funded blood costs. Resolve ordinary Wound/death/concentration consequences and no incidental reflection/resource/lifesteal triggers from this self-authored cost. It requires noHPprepayment and can kill the caster. A readied cast takes backlash after preparation/interruption, not after eventual release; its added dice attach once to the eventual immediate payload. Rank 0 legally adds 0 dice and 0 damage but still spends the use if chosen. Flat-only/no-native-die spells are ineligible.

### Worked boundaries

**MX-25-E01.** Rank 3 native 4d6 becomes 7d6 in the selected shared area roll, followed by 6 unreducible force backlash.

**MX-25-E02.** If Counterspell negates that spell, the committedLRuse and 6 backlash still occur.


## MX-26 — Planar Knowledge (`planar_knowledge`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/25`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define Bonus Action range/senses, actual creature CR including fractional/missing values, DC10+CR rounding, choosing one existing fact, retries and once-per-creature identity. Read actual resistance/immunity/vulnerability records; planar-trait content remains deferred where cosmology would be required. No invented trait or origin.

**Decision:** Keep bounded observable ordinary defensive information and explicit no-cosmology scope; NEW DC15 fallback for otherwise eligible genuinely unrated creatures, never invented CR.

### Complete authoring text

Once per actual creature identity, as a Bonus Action examine one creature you can perceive within 60 ft and line of effect. NEW commit the per-creature attempt before rolling INT(Arcana) against DC 10+its actual printedCR, rounding the finalDCdown by current fraction rules. NEW for an otherwise genuinely eligible creature with no assigned CR, use DC15; preserve the missing/null CR rather than inventing a rating. A missing creature identity, ordinary information payload or permission is still not supplied by this fallback. Success lets the Director truthfully disclose one existing damage resistance, immunity, vulnerability or explicitly established planar-trait fact; you may name a category, but no nonexistent fact is invented. If that category has none, report that absence only, not all other hidden data. Failure gives no fact and no retry through alias/form/encounter reset. Existing source disguises/protected information still apply. Planar traits requiring the deferred cosmology review remain unasserted; other recorded defenses are still usable.

### Worked boundaries

**MX-26-E01.** CR 1/2 gives DC 10 after rounding; success can reveal one actual cold resistance.

**MX-26-E02.** An unrated story entity is not automatically DC 10, and success cannot invent its planar origin.


## MX-27 — Protective Casting (`protective_casting`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/26`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Use+1 AC until next regular start after a real ranked cast, not legacy10percent/5seconds. Define successful versus interrupted/countered casting, repeated nonstacking applications and combination with Arcane Armor/other AC families. No retroactive protection for the triggering cast unless explicitly decided.

**Decision:** Select current ranked-cast+1AC until next start over legacy10%/five seconds; completed failed-target casts qualify, countered casts do not, and distinct flat feats add.

### Complete authoring text

At character level 6, after a completed personal ranked cast gain+1 AC until your next future regular start. NEW select active+1/regular-start over preserved 10%/5 seconds. It begins after the cast’s immediate resolution or successful Ready preparation, so does not protect against that cast’s earlier interruption attacks. Miss/all-save still qualify; a countered cast does not. Repeated legal casts refresh one same-family record without stacking magnitude; distinct eligible flat feat AC bonuses add under FS-03, after existing AC formula/item/class/spell arbitration. Ready release does not grant again. Incapacity does not itself end this nonconcentration buff; ordinary expiry/source-suppression does. No additional armor, resistance, spell use or cast trigger from copies.

### Worked boundaries

**MX-27-E01.** A saved-against rank 2 spell still grants+1 AC after resolution.

**MX-27-E02.** Two ranked casts create one+1 record; a reaction attack during the first cast resolves before it begins.


## MX-28 — Quick Ritualist (`quick_ritualist`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/27`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Apply half to additional ritual casting time only, minimum5minutes; preserve base casting time and exact rounding. Bind actual ritual access, long rituals, interruption and other reductions. Ritual Caster/Ritual Channeler are pending dependencies, not automatic access or multiplicative approvals.

**Decision:** Adopt half the added ritual labor, not base cast time, with a non-worsening five-minute floor and explicit composition with Ritual Channeler.

### Complete authoring text

For a spell you can actually cast through a legal ritual route, halve only the route’s additional ritual time, with resulting additional time at least 5 minutes; retain the base printed casting time in full. NEW measure the result in elapsed seconds and round up to the next whole second so fractions never shorten a required interval. An original 10 minute addition becomes 5 minutes, not half the whole cast. An original shorter addition is not increased: use min(original additional time, max(300, ceil(original/2))). This explicit non-worsening interpretation preserves the minimum for reductions without penalizing a preexisting faster route. Components, formula/repertoire, costs, concentration, helpers and interruptions remain. It grants no Ritual tag or access; the separate proposed Ritual Caster overlay needs its own approval. Apply this additional-time change before any separately legal group active-time adjustment, whose minimum rule remains.
NEW common ritual arithmetic: let B be the spell’s actual base casting labor and A its separately required added ritual labor, in whole seconds. Quick Ritualist changes A to min(A,max(300,ceil(A/2))), leaving B unchanged. This never lengthens an already shorter source procedure. Literal source-required elapsed waiting is not active labor to halve.

### Worked boundaries

**MX-28-E01.** For a rank1 ritual with base Action6seconds plus600seconds added ritual labor, Quick Ritualist gives6+300=306seconds. It does not halve the base casting Action.

**MX-28-E02.** With Ritual Channeler as well,ceil(306×0.75)=230 would breach the6+300floor, so the result remains306seconds. No helper creates another spell, omitted component or concentration slot.


## MX-29 — Ritual Channeler (`ritual_channeler`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/28`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define a real group ritual and ordinary assistant procedure before applying25percent active-time reduction and two-assistant contribution. Specify assistant caps, multiple feat users, overlapping work, base versus additional time, rounding, interruptions and material/formula costs. Do not silently treat every crafting work order as a ritual.

**Decision:** Adopt one25% group-labor reduction and double ordinary assistant contribution only for the actual assistant role; no extra physical bodies, fabricated check or per-helper compounding.

### Complete authoring text

NEW a group ritual is one actual legally available ritual spell with a designated lead and at least one physically present willing assistant continuously performing that same ritual’s active work; it is not simultaneous crafting, travel or independent casts. Use the exact source’s assistant qualifications/cap. If it supplies none, the proposed default assistant must know that ritual or have proficiency in the lead’s actual relevant Arcana/Religion/Nature skill; count at most two ordinary assistant contributions, with no numeric roll bonus when the source has no assistant benefit. This feat-holder contributes as two ordinary assistants within that cap, never as two leads or two physical bodies for a separate location requirement. One or more holders reduce the group’s total active casting time once by 25%, rounding up seconds; passive waiting is unchanged. Apply after Quick Ritualist’s additional-time reduction, but never reduce that remaining additional ritual portion below 5 minutes unless it was already shorter. Source-required simultaneous people, costs, lead concentration, interruptions and minimum times remain. No multiplicative 25%stack or free spell/resource. NEW the double-assistant contribution applies only while actually serving as an assistant. A lead who owns this feat can supply the time reduction but cannot simultaneously count as two assistants; one person never performs both assigned jobs at once.
NEW apply the one25% helper reduction to the actual total ritual labor after any Quick Ritualist reduction, never once per helper. For the standard added-ritual route, final total=min(previous total,max(B+300,ceil(previous total×3/4))). No reduction removes the actual base casting work or the five-minute added-ritual floor, and a source already shorter is not lengthened. Every required helper attends the full resulting procedure. No check or numeric helper bonus is invented where the actual source has none.

### Worked boundaries

**MX-29-E01.** A source with600seconds base labor plus600seconds added ritual labor takes900seconds with the25% group reduction alone, respecting its600+300floor. Each actual helper works all900seconds.

**MX-29-E02.** Two Channelers do not apply25% twice or count as two physically separate station operators. A source with no check receives no invented numeric helper bonus.


## MX-30 — Runic Shield (`runic_shield`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/29`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve description50 versus active15 ward HP and start-of-combat versus Short Rest refresh. Define ward versus temporary HP, one physical owner/source identity, spell-only damage interception order, damage event and concentration/Wound thresholds, depletion, encounter farming and transfer. Preserve both activation and recovery clauses explicitly.

**Decision:** Select15 ward HP over legacy50, armed once by an actual beneficial rest and consumed across later encounters until refreshed; no encounter-entry refill farming.

### Complete authoring text

NEW select 15 ward HP over preserved 50. The feat has one armed grant per beneficial SR/LR; acquisition arms it. At the first real encounter start after arming, automatically create one personal runic ward with 15 points and spend that entitlement, even if surprised/incapacitated; a dead creature receives none. It persists between encounters until depleted or the next beneficial SR/LR, when any old ward ends and entitlement rearms for the next combat, not immediate refill in combat. Repeated initiative does not refill it. This is a distinct spell-only ward, not temp HP: after ordinary defenses and before temp HP, intercept up to its remaining points of actual incoming spell damage in stable component order. Nonspell damage bypasses it. Record ward absorption separately, excluded from actual damage received by the body, Wound/death thresholds and concentration checks; any surviving packet resolves once normally. No transfer, double ledger, HP healing, return on revival or resource proc from ward absorption. Counterspell/dispel cannot target this nonspell passive ward without explicit applicable source permission.

### Worked boundaries

**MX-30-E01.** A post-defense 20 spell-damage packet consumes 15 ward then passes 5 to temp HP/normal HP.

**MX-30-E02.** A sword’s 8 nonspell damage ignores the ward entirely; starting another encounter does not restore spent ward points.


## MX-31 — Silent Casting (`silent_casting`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/30`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define+1 RP surcharge for removing V at declaration, price ordering, rank0 and charge-only casts without an RP interface/pool. Preserve command-word exclusion and S/material requirements; identify what a stated magical command word means from actual spell text. No universal undetectable casting.

**Decision:** Keep+1 real independent RP to remove V only; no removal of F/S, actual command channels or source-required spoken effects.

### Complete authoring text

At declaration of a spell actually requiringV, remove only that verbal component by adding 1 actual RP to its price before ordinary final cost adjustments. NEW the independent 1 RP payment cannot itself be waived by a charged/free normal-rank route; an actualRPpool and sufficient final payment are required. Rank 0 can use the feat and still pays the independent surcharge; cantrip strain rules remain. A component or exact activation explicitly demanding a magical command word cannot be removed. Ordinary audibleV alone is not a protected command word unless identified as such by the operative source. PreserveS, F/materials, physical access and action permissions. Silence no longer blocks the removedV, but Incapacitated/other restrictions remain. It creates neither undetectable casting nor automatic concealment; other visible components/effects and observers’ real senses still determine interruption eligibility.

### Worked boundaries

**MX-31-E01.** A V, S cantrip may be cast silently with S and 1 real RP, provided every other permission holds.

**MX-31-E02.** A charged spell cast by someone with noRPpool cannot pay the extra 1 RP through its charge.


## MX-32 — Spell Deflection (`spell_deflection`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/31`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Use actual d20≥16, not legacy10percent. Define optional Long Rest declaration, action/Reaction, hostile single-target spell, legal new target from original origin, save/attack handling and no-legal-target outcome. Preserve fallback advantage, prevent reflection recursion and distinguish redirects from new casts.

**Decision:** Select one-LR unmodified d20≥16 redirection over legacy10%; actual sole-target eligibility, paid Reaction and fallback saving advantage create no new save.

### Complete authoring text

Once LR, NEW spend a Reaction when a hostile pending spell has selected you as its sole creature target, after ordinary cast interruptions but before its attack/save/effect resolution. It must be an actual single-target payload, not one target remaining from an area or multi-target mode. Roll an unmodifiedd 20;16–20 redirects, preserving this explicit 25%procedure over legacy 10%. On success choose a different legal creature under the original spell’s actual target restrictions, range/line measured from the original origin, personally perceived by you where necessary; the original caster remains owner and supplies all stats/choices. Recheck legality, then use fresh original attack/save procedure against that new target; nothing resolves against you. If no legal new target exists, or on 1–15, the spell continues against you with advantage on each actual initial save it requires; no save is invented for an attack/automatic spell. Use/Reaction remain spent. A redirected/reflected/copy packet cannot be redirected again by this family or Spell Reflection. Protected/self-only/source-specific exclusions remain.

### Worked boundaries

**MX-32-E01.** Roll 17 redirects an eligible hostile ray to another legal creature within the original caster’s range.

**MX-32-E02.** Roll 9 against an attack spell grants no save orACbonus; the original attack proceeds normally.


## MX-33 — Spell Reservoir (`spell_reservoir`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/32`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Specify completion of an actual Short Rest within one Long Rest use ledger, PB amount, RP cap and timing with ordinary rest recovery. No new spell slot, maximum RP increase, charge conversion or repeated claim from one rest event; source description and old slot wording stay separately preserved.

**Decision:** Keep one LR-bounded recovery at a genuine beneficial short-rest completion, capped by actual PB and headroom; no old-rest trigger banking.

### Complete authoring text

Once LR, immediately after completing a beneficial SR and its ordinary recovery, optionally restore currentPBactual RP capped by remaining merged-pool headroom. Commit theLRuse and that actual rest-event claim together; another listener, duplicate receipt or resumed rest completion cannot claim again. If no headroom, you may decline without spending, but cannot bank that past rest’s trigger for later; a later beneficial SR can supply a new opportunity while theLRuse remains. It creates no maximumRPincrease, charge, slot, second classpool or independent Retune. A long rest alone does not count as the printedSRtrigger. PB changes before a future legal use affect that use’s amount but never refresh spent entitlement.

### Worked boundaries

**MX-33-E01.** PB 4 with 2 RP missing after normalSRrecovery restores 2 and spends theLRuse.

**MX-33-E02.** At full RP you may decline; spending RP later does not reopen that already-finished rest.


## MX-34 — Spellweave (`spellweave`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/33`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define a finite meaning of minor buff and eligible transfer rather than arbitrary Director improvisation. Specify original recipient/payment, one held record, expiry, concentration, next actual cast attachment and components/scaling. Preserve every source clause while preventing duplicated buffs, resources or impossible effect-type conversions.

**Decision:** Adopt the closed Guidance/Resistance/True Strike transfer table using the actual current non-concentration payloads; one real held buff, no invented check/save or generic Insight exchange.

### Complete authoring text

NEW use the finite three-spell minor-buff table below: personally cast Guidance, Resistance or True Strike with yourself as the otherwise legal recipient. At its completion hold that entire one-use buff instead of receiving it normally; only one held record, replacing loses the old. Original costs, cast history and earlier deadline remain, with an additional deadline at your next future regular end. The next actual spell you commit consumes/attaches the record automatically, even if countered or unsuitable; no indefinite skipping. Guidance adds its one 1d4 only to one actual ability/task check made by that next spell, declared before rolling; Resistance adds its one 1d4 only to one actual concentration save maintaining that next spell; True Strike grants advantage only on that next spell’s first actual spell attack. They create no check/save/attack. The attachment expires at the original held deadline or actual spell end, whichever first, even if unused. Current one-bonus-die/advantage rules apply. A copied buff, borrowed duplicate or another Spellweave cannot be held; no duration/resource/HP/stat transfer or new cast.
The three selected current buffs are non-concentration spells. Holding/attaching their one-use benefit adds no concentration requirement and does not change that source fact. There is still only one held Spellweave record and each original deadline/cost/history; no newly invented check or save may redeem it.

### Worked boundaries

**MX-34-E01.** Held Guidance attaches to a legal next Counterspell and can add 1d4 to its actual counter check.

**MX-34-E02.** Held True Strike consumed by a next spell with no attack produces no benefit and cannot wait for a third cast.


## MX-35 — Still Casting (`still_casting`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/34`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define+1 RP surcharge for removing S and actual fully-restrained boundary against current Restrained/hand rules. Specify charge-only/cantrip casts, price order, material/focus handling and V. Removing somatic gestures does not supply hands for other components or permit actions under Incapacitated.

**Decision:** Keep+1 real independent RP to remove S only with genuine remaining component access; no assumption every restraint disables hands or focus, and no V waiver.

### Complete authoring text

At declaration of a spell requiringS, remove only that somatic component by adding 1 actual RP before final pricing; use Silent Casting’s independent-surcharge convention, including actualRPrequirement for rank 0/charged routes. NEW fully restrained means actual hands/arms physically or explicitly magically immobilized so no usable casting gesture exists; CoreRestrained alone imposes its printed penalties and does not prove that anatomy restriction. This feat expressly fails under such complete physical/explicit gesture immobilization, despite removing ordinaryS. It also supplies no Action under Incapacitated, no freedom from binding, and no hand for actualF/material manipulation. RemovingS andV with two feats pays both independent surcharges; each protected command/material requirement remains. Spell perception/counterability follows real remaining cues.

### Worked boundaries

**MX-35-E01.** A net’s actual full arm binding blocks this feat; a source’s mere Speed 0/Restrained penalty need not.

**MX-35-E02.** RemovingS still leaves a required held focus that the caster must legally handle.


## MX-36 — Temporal Flux (`temporal_flux`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/35`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Identify exact time-tagged spell authority and failed-save trigger. Bind−10ft Speed with current strongest/stacking floors and no-Reaction component until target next regular start, repeated/multiple-source effects and cure/suppression. No legacy all-hits trigger or enabling unfinished Time Loop.

**Decision:** Adopt feat-only Time membership for Slow/Haste/Future Echo, but require an actual failed save; no Save appears on the save-less comparison cards.

### Complete authoring text

At character level 8, when a creature fails an actual save against your personally cast time-tagged spell, apply one softSpeed−10 ft record and one no-new-Reactions component until its next future regular start. NEW finite feat-tag overlay: Slow’s two actual modes, Haste and Future Echo only; current source tags do not supply an explicitTime tag. Their full current spell procedures remain unchanged, and a save-less buff creates no trigger. Wider tags require separate review; spell names or narrative time flavor alone do not qualify. Speed records compete under current strongest-adverse-control arithmetic rather than add;0 floor, real modes and existing movement spent remain. Already committed Reactions finish. Same owner/target/profile refreshes one record without extra magnitude; different sources retain their real deadlines. No new save, hardActiondenial, extra turn, state restoration or enabledTime Loop.

### Worked boundaries

**MX-36-E01.** A failed Slow save on Speed 30 already produces halfSpeed 15; Flux−10 competes as 20, so effectiveSpeed stays 15.

**MX-36-E02.** Haste ordinarily has no recipient save, so its new feat tag alone does not trigger Flux.


## MX-37 — Twin Cast (`twin_cast`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/36`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Use once-per-Long-Rest second legal creature after a Tier1–3 single-target cast, not legacy5percent double cast. Define attack/save results, concentration, components, range/sight recheck, origin, already-multitarget/upcast spells and one source identity. No duplicate refund, extra summon or copied paid resource.

**Decision:** Select one LR-bounded second legal target for rank1–3 over legacy5% repeated cast; native secondary result only, no extra cast/history/concentration or production.

### Complete authoring text

Once LR after a personal rank 1–3 single-creature spell completes its initial payload, choose one additional different creature currently legal under that same mode, range, sight, line of effect and willingness/type restrictions. NEW only an originally exactly-one-creature payload qualifies; no area, multi-ray/multi-target, Self-only, summon/object creation, resource/action-grant, resurrection, maximumHPchange or copied payload. Consume the feat use and extend that same cast’s original immediate damage/heal/condition/buff to the second recipient. Roll a fresh actual attack/save and native dice for that recipient; no newRPprice, cast, components, Dissonance/Refrain or class/featproc. Independent per-recipient material/HP/finite reserve requirements remain actual costs and must be affordable before choosing. One concentration ID governs both; original deadline and source target-ending rules remain. This is an explicit two-target exception only for this cast, not another spell identity or separate duration. Preserve old 5%autodouble wording as inactive alternative.

### Worked boundaries

**MX-37-E01.** A legal rank 1 one-creature damage spell resolves anew against one second eligible creature without another baseRPcost.

**MX-37-E02.** A spell already selecting up to two creatures cannot qualify merely because the caster chose only one.


## MX-38 — Arcane Adaptation (`arcane_adaptation`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/37`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define actual successful reflection/copy event, which real damage type(s) grant resistance and end-of-next-turn duration. Separately bind Short Rest treat-as-known effect for2rounds: permitted repertoire/rank/costs/actions/copy profile. No permanent learning, boss/legendary access, recursive copying or borrowing of Mirrorsage class eligibility.

**Decision:** Adopt bounded witnessed-type resistance and temporary access to one supported paid copy profile; no Mirrorsage archive, rank ceiling or release allowance is duplicated.

### Complete authoring text

After an actual successful legal reflection or capture of a spell/supernatural effect through a separately owned source, gain resistance to the one real damage type expressed by its selected copied/reflected component until your next future regular end. NEW choose one observed type for a mixed packet; nondamaging effects grant no damage resistance. It begins after capture/redirect, does not retroactively mitigate earlier damage, and grants no copying permission by itself. Once SR/LR at that event, also mark the one legal captured profile as temporarily known through your second future regular start. During that interval you may activate that exact bounded profile using its actual action, RP, components, rank ceiling and concentration, even if its original one-use record was consumed; no other original spell/monster ability is learned. Each activation is a copy retaining the original no-proc/no-copy/resource flags and the shared one-copy-release/round cap below. Existing Mirrorsage records retain their actual release costs/caps and printed bounded profile. No restoration of archive slots or legacy boss power. Expiry removes permission but not legitimately established effects before their own deadlines.

### Worked boundaries

**MX-38-E01.** Capturing a fire Strike grants fire resistance through next end; adapting it permits paid bounded releases within two regular-start intervals.

**MX-38-E02.** Copying a harmless warning reveals no damage type and grants no invented resistance.


## MX-39 — Arcane Calculus (`arcane_calculus`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/38`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Bind+2 initiative only while actually concentrating, timing of the check and later loss. Define storing one prepared spell, setup action/RP/components/concentration, lifetime, free release on a later turn, counterability and legal targets. Define the separate30ft Dexterity-save force rider/DC/one spellcasting modifier and no action-generation loop.

**Decision:** Adopt the explicit next-own-regular-turn non-Action Ready release extension, maintaining one Ready/concentration slot, original price/history and shared free-release cap.

### Complete authoring text

Gain+2 to an actual initiative roll only while concentrating on a spell when that roll occurs; losing concentration later does not rewrite initiative. Once SR/LR use an Action to prepare one currently legally prepared normalActionspell through the exact Ready casting procedure, paying costs/components/history and opening interruption at preparation. NEW it shares the one pendingReady slot and concentration requirement, but its hold lasts through your next future regular end, and release is a voluntary non-action on that next regular turn only. Choose/recheck original legal targets then; no Reaction or second cast. Expiry, replacement or lostconcentration wastes paid costs. On successful release, choose one perceived creature within 30 ft of your body and line of effect:DEX save against the stored cast’s actual DC or take force equal to max(1, its actual casting modifier snapshotted at preparation),0 on success. One immediate noncopyable feat rider, no added release/action/castproc. Readied spells lacking a preparation route remain ineligible; the feat grants no preparation list.

### Worked boundaries

**MX-39-E01.** Prepare a legal spell now, then release next regular turn without spendingAction; one nearby creature may face the separateDEXsave.

**MX-39-E02.** A Counterspell at preparation prevents storage and the later rider; there is no second Counterspell window at release.


## MX-40 — Arcane Momentum (`arcane_momentum`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/39`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve actual Power Attack OR Combat Casting prerequisites. Define melee-hit stack gain, maximum3, lifetime/reset, per-hit cadence and one-step casting-time ladder. Separately define spending all stacks for+10percent force damage per stack: base, packet/area/critical rounding, duration and whether damage is added or converted. No arbitrary free cast or imported class Momentum pool.

**Decision:** Adopt separate finite3-stack melee momentum, not Dragoon Momentum; spend on one legal Action conversion or separately floored native damage rider, never both.

### Complete authoring text

Require actual Power Attack OR Combat Casting plus actual spellcasting ability. NEW each personal direct melee-weapon hit against meaningful opposition gives one featMomentum, max 3, with a once-per-attack identity and no gain from copies/companions/retaliation. This separate pool starts 0, ends at encounter end or one minute without a qualifying hostile hit; no alias to any class Momentum. At spell declaration choose ONE mode. Spend 1 to shorten a printed normalActionspell to BA; no other casting time has a shorter step in this explicit finite ladder, so no BA-to-free, Reaction-to-Action or ritual compression. OR spend all current 1–3 stacks to add floor(native immediate damage×stacks/10) as force to one selected native packet/shared area roll before this actual turn ends, after native critical/flat formula but before defenses. It adds damage rather than converts the original type, and does not compound other percentage bonuses. No damage means 0, no future periodic/ray replication; a miss/counter wastes stacks. Cannot combine both modes on one cast or bank the declared enhancement for a later turn.

### Worked boundaries

**MX-40-E01.** Native 19 damage with 3 stacks adds 5 force; native damage keeps its original type.

**MX-40-E02.** A printedBAspell cannot be made free by spending a stack.


## MX-41 — Conjure Flora (`conjure_flora`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/40`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Preserve lash, spores and10ft-square entangle modes, one seedling/second atlevel10 and all-seedling Bonus Action command. Define creation action, separate Short Rest use and capacity, one-minute expiry, HP/AC/size/placement, each mode stats/save/DC, targets and shared damage-command cap. No unbounded seed, loot, independent turn or cosmology inference from plant spirit.

**Decision:** Adopt three closed finite plant profiles with actual attached command phases and capacity/creation entitlements; no anonymous autonomous attack, corpse, harvest or class minion grant.

### Complete authoring text

Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW to make the second-capacity clause usable, at level 10 this same committed use permits one additional Action before the first plant expires to create one second plant; no second rest use, no later replacement of that spent creation. This is an explicit proposed addition to the printed one-seedling creation, not a recovered rule. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.
NEW ordinary command scheduling: each plant has one attached phase immediately after its owner’s regular turn, not an independent initiative turn. Its ordinary commanded action requires the owner’s shared Bonus Action within60ft through the specified perceivable command channel and spends the one offensive companion allowance per owner per numbered round if offensive. With no legal command it has no autonomous attack. Trapcasting’s explicitly adopted entry-trigger or burst is a separate narrow exception spending that same shared offensive allowance, never another free attack.

### Worked boundaries

**MX-41-E01.** Two active plants can extend where the single 1d6 lash originates; they do not produce 2d6 or two attacks.

**MX-41-E02.** At level 10, a second Action during the first plant’s lifetime can consume the one proposed additional-creation entitlement; it does not allow repeated replacement plants.


## MX-42 — Curse Channeling (`curse_channeling`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/41`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define optional Hex Mark application on a weapon hit, one/two capacity, expiry/replacement, next-hit+1d6 ownership and whether triggering hit qualifies. Resolve next-hit consumption versus later zeroHP benefit, which marked death/zeroHP event grants1d6 healing or next-attack advantage, true-healing gates and anti-farming. Keep unrelated generic Marked condition separate.

**Decision:** Keep owned finite mark, later distinct hit rider and bounded actual positive-to-zero reward; actual death is not required and copying/refreshing cannot duplicate entitlements.

### Complete authoring text

Require character 6 plus actual spellcasting OR Arcana proficiency. After a personal direct weapon hit, optionally place oneHexMark on that creature; the triggering hit cannot consume it. Capacity 1, or 2 at total 10; new beyond cap replaces oldest. Each record expires at your next future regular start and has two distinct one-use riders. The next genuinely separate hit against that target adds 1d6 necrotic to that hit’s packet, critical-doubled if that hit truly crits, then consumes only the damage rider; attribution remains to your feat, not the attacker’s spell for proc purposes. While the record remains, the first drop from positiveHPto 0 by genuine hostile conflict lets you choose 1d6 ordinary self-healing or advantage on your next actual attack roll through next regular end. Commit that drop rider even if blocked/full HP; no floor-prevented drop, staged victims or repeated same-target cycling within the encounter. NEW one drop benefit per owner/target/encounter; healing is finite paid-feat trigger, no healing-copy/resource output or convertible excess. Mark ends early only on replacement/cure/source rule; separate source marks do not stack the same damage rider on one hit.

### Worked boundaries

**MX-42-E01.** An ally’s later hit spends the mark’s 1d6, but a subsequent lawful drop before expiry can still grant the one self-heal.

**MX-42-E02.** Your original marking hit supplies neither its own bonus die nor a drop reward if the target was already 0 before the mark existed.


## MX-43 — Curse Weaving (`curse_weaving`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/42`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define optional curse on a failed save, eligible targets, per-cast use/cost/cadence and escalating components. Specify whether−1 attacks,−1 saves,concentration disadvantage accumulate, round/turn order, end-turn save ability/DC, maximum duration, independent spell end/cure/suppression and multiple applications. No indefinite undefined debuff ladder.

**Decision:** Adopt explicit staged curse clocks and saves; same target/source refresh preserves stage and one magnitude, no reset farming or automatic parent spell promotion.

### Complete authoring text

At a personal actual spell declaration that forces an initial save, select at most one original creature recipient for this NEW curse rider. Once per owner/target/numbered round, if it fails that actual initial save, establish an inflicted removablemagicalcurse with that save’s ability/DC and maximum one minute. Tier/rank for an actual rank-limited cure is the generating cast’s rank. Immediate stage 1 is−1 attack rolls; at the target’s next future regular start add stage 2−1 saves; at its following regular start add stage 3 disadvantage on actual concentration saves. Cap at 3; components accumulate within this record, not as repeated−1 stacks. At every affected regular end, including a current turn where applicable, repeat the original save; success ends the record. Original spell concentration loss/termination ends this attached curse; instantaneous spells leave its bounded independent minute. Suppression preserves stage clock and legal cures/saves without backlogged effects. Reapplication does not reset stage/extend beyond the later legal deadline or duplicate magnitude; different sources retain identity but same penalties use strongest. No forcedAction, deniedturn or hidden perpetual escalation.

### Worked boundaries

**MX-43-E01.** Failing initialWISsave gives−1 attacks; next regular start adds−1 saves, then the regular-endWISsave can end both.

**MX-43-E02.** A second copy of the same stage cannot create−2 attacks or a fourth escalation.


## MX-44 — Dark Affinity (`dark_affinity`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/43`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Retain necrotic resistance,60ft darkvision or+30ft extension, undead-charm save advantage, dim/dark Stealth advantage and15ft Bonus Action shadow teleport once per Short Rest. Define actual light/sight/space/line, legal hiding, source-undead/charm predicate and darkvision stacking. No invisibility, creature conversion or soul/origin inference.

**Decision:** Adopt necrotic resistance, actual Undead charm-save predicate and real dim-light step; correct darkvision to a fixed acquisition branch rather than a dynamic free fallback.

### Complete authoring text

Gain necrotic resistance once. NEW darkvision branch is fixed at acquisition as specified below; an extension does not revert to a60ft base when its underlying source ends. It does not see through magicaldarkness unless separately allowed. Advantage applies to actual saves against a Charmed/explicitcharm component sourced by a creature actuallyUndead at application; no free type detection or general mind immunity. While your occupied space is actually dim/dark, gainStealthadvantage subject to ordinary hiding/perception; NEW whole footprint must qualify. Once SR/LR use BA from such a space to teleport up to 15 ft into an unoccupied fitting space you can see that is also dim/dark. No traversed path, but NEW line of effect to destination required; obey actual teleport/consent/restraint restrictions. Costs/use commit normally; no invisibility, freeHide, ancestry conversion or soul/origin claim.
NEW exact darkvision branch, replacing any dynamic fallback reading: snapshot whether an independent darkvision source exists at acquisition. No source then gives a60ft base; an existing source then gives a+30ft extension to the current strongest independent operative range. Losing/suppressing every underlying source makes that extension inoperative, not a new60ft base. Record the branch permanently; unrelated future base ranges use normal strongest-base arbitration.

### Worked boundaries

**MX-44-E01.** Existing 60 ftdarkvision becomes 90 ft; Darkness that defeats that sense remains opaque.

**MX-44-E02.** A lit destination cannot receive the shadow step even if it is within 15 ft.


## MX-45 — Dark Binding (`dark_binding`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/44`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve Curse Channeling OR level8 gate, one actual cursed weapon, one-hour ritual/tools/payment, rebind/unbind and original identity. Define cannot-be-disarmed versus forced dropping/incapacity, actual wielding+1d4 necrotic, thrown/ammunition/multi-hit limits and destruction2d10 psychic timing. This blood ritual is not automatically the reviewed Blood Ritual feat or free cursed-item creation.

**Decision:** Adopt finite real weapon ritual/bond and destruction consequence with continuing body/custody; not possession of a free cursed weapon, soul lore or refillable RP.

### Complete authoring text

Require Curse Channeling OR character 8. Spend one uninterrupted hour in contact with one actual owned/willingly entrusted weapon carrying an established curse record; no feat-created curse, weapon or hidden curse diagnosis. NEW ritual needs your voluntary symbolic drop of blood but no numeric HP/material charge, and is unrelated to Blood Ritual. Completion replaces your old binding; interrupted work creates none and leaves the old. While personally wielding the bound original weapon, you cannot be involuntarily disarmed by an actual disarm effect; mandatory dropping from Unconscious/incapacity, loss of body/hand, voluntary release and physical destruction still apply. Each actual direct hit you make with that weapon adds 1d4 necrotic, critical-doubled normally. Thrown original weapon qualifies on its hit but does not return; ammunition launched by a bound bow qualifies as its weapon hit without becoming a bound item. No copying or companion use. Actual destruction ends the bond and causes one 2d10 psychic damage packet to you under ordinary defenses, at any distance; repair never rebinds. A fresh fullhour ritual is required for a new bond.

### Worked boundaries

**MX-45-E01.** An enemy disarm cannot take a consciously wielded bound sword; becomingUnconscious still drops it.

**MX-45-E02.** Destroying a bound thrown weapon causes one 2d10 psychic packet, with ordinary psychic resistance if present.


## MX-46 — Eldritch Echo (`eldritch_echo`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/45`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve prerequisite grouping and missing Eldritch Blast definition/level scaling. Separately bound witnessing a cast within60ft, Short Rest echo trigger, next-turn release action/RP/rank/profile and half-level rounding. Preserve adjudication text but require finite playable choices; no arbitrary monster powers, copying a copy or invented Warlock class access.

**Decision:** Adopt the separate feat-only CHA Eldritch Blast plus one bounded captured profile; release is an actual paid feat-copy cast, not an ordinary spell grant or free class Echo.

### Complete authoring text

Require character 3 AND (Forbidden Pact OR actual spellcasting). Gain the exact NEW Eldritch Blast cantrip profile below once; duplicate grant through Forbidden Pact shares one identity. Once SR/LR when you actually perceive a creature within 60 ft/line of effect completing an eligible noncopyspell, use a Reaction to capture one matching bounded copy profile below. NEW the source may be ally or foe, but cannot be a resource/copy/production effect or protected boss/legendary ability. Record original rank and the profile’s half-rankq; it must fit your actual qualifying casting route’s learnable ceiling, with Forbidden Pact’s explicit rank 0 grant supplying no ranked ceiling by itself. On your next future regular turn use anAction, actualRPprice and V/S and any additional actual copied-profile component requirement to release that one profile; otherwise it expires at that turn’s end. It is a copied spell activation with actual Dissonance/Refrain/history and interruption at release, no new proc/capture. No free original full spell, copied casterstatistics or Warlockclass.
NEW classification reconciliation, FS-08: releasing this captured spell is a paid feat-copy cast, using the releaser’s specified ability/PB, actual components, current RP price, rank and ordinary Dissonance/Refrain. It is not a resource-free nonspell release. It grants no ordinary repertoire/class feature or further capture, echo, reflection, external feat amplification, class resource/proc or reward chain. The concrete copy profile and its independent component/range/target/deadline limits still apply. This is deliberately different from Echo Spell/Twin Cast secondary results and from an actual Mirrorsage class Echo Release.

### Worked boundaries

**MX-46-E01.** Observe rank 4 damage: half-rankq 2 Strike may be captured if your real route can learn rank 2, then costs 3 RP next turn.

**MX-46-E02.** Forbidden Pact alone supplies the cantrip, not a rank 2 spell repertoire orRPpool for that copied release.


## MX-47 — Forbidden Pact (`forbidden_pact`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/46`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Preserve exact pact/origin wording without reviewing or revising cosmology before push. Mechanically resolve missing Eldritch Blast, a finite pact-sigil menu with actual stats/cadence and once-per-encounter2xRank HP substitution for ranked recovery. Specify true-HP funding, RP route, zeroHP, interruption and encounter ledger; no unstated entity powers, spell-slot pool or permanent soul transaction procedure.

**Decision:** Adopt one of three closed sigils and the distinct normal-HP sacrifice substitution; sacrifice is a state payment, not Arcane Transfusion damage, and creates no patron/class ontology.

### Complete authoring text

Require CHA 13 and character 3. Preserve the original beyond-known-planes soul-pact wording as unreviewed setting provenance; this procedure grants no soul transfer, patron demands or cosmological claim. Mechanically gain the exact NEW Eldritch Blast profile and choose permanently one of three finite sigils below with the Director. This feat’s casting ability is CHA and grants rank 0 access only, not anRPpool or ranked repertoire. NEW reconcile “instead of a ranked-spell recovery” and old “instead of a spell slot” as once per real encounter substituting 2×actualrank normal HP sacrifice for the ordinary baseRPprice of one independently known/prepared rank 1–9 spell. Commit true HP loss while retaining at least 1 normal HP; temp HP, mitigation, floors/refunds cannot fund it. It is sacrifice, not damage, so no Wound/concentration/damageproc from the payment. AdditionalRPcosts, strain/armor/component surcharges, materials and action remain actual payments; final price calculation waives only original rankbase before those additions. NoRPis restored, no chargeuse bypassed, no separate ranked grant and no incidental resource output. Interrupted spell keeps all costs/use spent.

### Worked boundaries

**MX-47-E01.** An independently legal rank 2 cast may substitute 4 normal HP for base 3 RP once this encounter, still paying an actual extra 1 RP surcharge.

**MX-47-E02.** A pact-holder who knows only Eldritch Blast gains no ranked spell to pay for this way.


## MX-48 — Hemocraft (`hemocraft`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/47`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Bind real melee critical, Bleed-stack identity/ownership/cap/duration/cure and1d4 target-start pulse. Define action/cadence/range/sight for consuming one actually existing stack, choice of1d8 healing versus necrotic damage, which creature receives healing, save/attack and true-healing gates. Prevent free repeated consumption, copied Bleed and recursive zeroHP/resource events.

**Decision:** Adopt finite3-record Bleed handling, one consumption per round and2×level healing reserve starting0 until a beneficial LR; no healing from cured/foreign/staged records.

### Complete authoring text

After a personal genuine melee critical hit against meaningful opposition, apply one NEW Hemocraft Bleed record to the still-living eligible target. It pulses 1d4 slashing at each of its next three regular starts; source immunity/anatomy restrictions and the existing Bleeding-family arbitration/cures remain. NEW max 3 own records per target; at cap refresh the earliest deadline without adding a fourth. Same-family parallel records do not all deal damage: existing strongest-die arbitration selects one, but distinct consumable records retain identity. Once per numbered round use BA to consume one present unexpired own Hemocraft record on a creature you perceive within 30 ft/line of effect, including one temporarily suppressed record, choosing 1d8 ordinary self-healing OR one 1d8 necrotic packet to that creature withCONsave against DC 8+PB+your chosenINTor CHA modifier for half. Choose stat permanently at feat acquisition. Pay by ending that exact record before outcome; no refund or consumption of another source’s Bleed. Healing spends a NEW finite Hemocraft Reserve of 2×character level set only at beneficial LR, paying actual restored HP, no excess/copy/resource outputs. Reserve starts 0 on acquisition. No consuming historical/already-cured Bleed or staged victims. The record’s ordinary Medicine-ending DC is the same chosen feat DC; actual positive-potential magical healing ends eligible Bleed through the existing cure procedure.

### Worked boundaries

**MX-48-E01.** Consume one actual record to roll 7 healing with 2 Reserve and sufficient missing HP: restore 2 and spend 2.

**MX-48-E02.** A suppressed still-present record can be consumed, but an ended record cannot return for another heal.


## MX-49 — Lightning Affinity (`lightning_affinity`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/48`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Preserve resistance, lightning spell+1/die, conditional half-cover ignoring, electrical/paralysis save advantage and reactive Storm Charges. Define post-resistance received damage versus charges gained,max2/lifetime, Reaction, spending timing/cadence, next spell/weapon+1d6 packet and expiry. Resolve multi-die/area/critical/zero-damage cases without converting every damage point into a charge.

**Decision:** Adopt native lightning-die+1, actual half-cover scope and two separately expiring charges; respect source no-resource flags and do not refresh old charges at capacity.

### Complete authoring text

Gain lightning resistance and+1 damage per actual native lightning die in your personally cast spells, including native critical dice, as a flat adjustment before save/defense; no bonus per flatpoint, added nonlightning die or copied packet. Against a target actually outdoors/open-sky, your lightning spell attack/save geometry ignores halfcover only; threequarters/total cover remain. Gainadvantage on actual saves against a lightning/electrical payload or a component imposingParalyzed, not everyCONsave. After a hostile meaningful lightning packet deals positive actual numeric damage to you, spendReaction to gain oneStormCharge, max 2. NEW no charge per damagepoint; genuine tempHPabsorption qualifies, fully prevented/floor-only numeric 0 doesnot. Each charge lasts one minute from gain; no maximum cap refresh from a rejected gain. On your own turn, spend one charge withoutAction to prime your next personal weapon attack or immediate damaging spell before next regular end: add 1d6 lightning to one selected hit/packet/shared area roll under added-die rules. Attackmiss consumes the primed rider; no stacking multiplecharges on oneactivation. No charge from self/cooperative/copy/retaliationdamage.
Preserve per-charge origin and expiry: receiving a further charge at capacity does not refresh an older charge. FS-07 respects each underlying spell’s no-resource/trigger flags. The native lightning-die+1 excludes external riders and secondary/copy results; it can add to an independently eligible Evocation Focus bonus on an actually rolled kept die, not on a fictitious maximized face.

### Worked boundaries

**MX-49-E01.** A native 3d6 lightningspell adds 3 before saves; a reaction to 8 actual lightningdamage gains 1 charge, not 8.

**MX-49-E02.** A miss wastes the primed die; a later attack cannot recover that spent charge.


## MX-50 — Mimicry (`mimicry`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/49`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define witnessed/targeted spell or monster ability,30ft senses, one stored simplified profile and acquisition/cast costs/cadence. Replace usually-half/Director-adjudicates ambiguity with explicit finite playable rules while preserving originals. Specify next Short Rest expiry,two-round effect cap,rank/DC/targets and exclusions for resources,actions,copy recursion and unsupported abilities.

**Decision:** Adopt actual observed/targeted capture into a finite profile and paid feat-copy cast; preserve rank, RP, visibility and once-rest limits without copying class engines or unknown powers.

### Complete authoring text

Once between beneficial SR/LR completions, when you perceive an eligible real spell/monster ability used against you at its lawful range OR resolving within 30 ft of you and line of effect, capture one matching finite copy profile below withoutAction. NEW one record and one release entitlement per rest epoch; cannot erase/replace to gain repeated uses. No copy from a copy, protectedunique/legendary/boss feature, classengine, resource/action/creation effect or an unobserved component. Actual targeted-at-you clause may exceed 30 ft only if you genuinely perceive the source and effect. The stored profile expires at the next beneficial SR/LR; release before then usesAction, V/S, actualRPprice and its actual qualifying casting ability/rank ceiling. Its numeric native ceiling is half the observed eligible component as detailed below and duration at most two future regular intervals; no original source stats/unboundedDirector invention. Successful capture alone is not a cast; release commits ordinary spell history/interruption and the one-copy-release/round allowance. Failed/countered release consumes record/use, and a later rest never refills a missing copy.
NEW classification reconciliation, FS-08: releasing this captured spell is a paid feat-copy cast, using the releaser’s specified ability/PB, actual components, current RP price, rank and ordinary Dissonance/Refrain. It is not a resource-free nonspell release. It grants no ordinary repertoire/class feature or further capture, echo, reflection, external feat amplification, class resource/proc or reward chain. The concrete copy profile and its independent component/range/target/deadline limits still apply. This is deliberately different from Echo Spell/Twin Cast secondary results and from an actual Mirrorsage class Echo Release.

### Worked boundaries

**MX-50-E01.** A perceived attack spell directed at you from 60 ft may qualify through the targeted clause despite the ordinary 30 ftwitness radius.

**MX-50-E02.** Observing a monster restore RP cannot produce a copied recovery profile.


## MX-51 — Quickened Thought (`quickened_thought`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/50`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve Arcane Calculus OR Temporal Theory, readied-spell+2 initiative and concentration advantage. Define rank≤2 Bonus Action cast once per Short Rest, no-Reaction debt and expiry. Separately define initiative-banked cantrip setup/payment/one record/release on any later turn, target recheck and no free-copy or extra-turn loop.

**Decision:** Keep the source later-any-turn banked cantrip release rather than own-turn-only; it is between events, concentration-bound and shared-cap, not a free interrupt or extra turn.

### Complete authoring text

Require INT 15 and (Arcane Calculus OR Temporal Theory). NEW resolve the grammatical scope as+2 initiative AND concentration-saveadvantage only while actually holding a readied spell; initiative is not recomputed later. Once SR/LR change an actually available normalActionspell of actualrank 0–2 to BA, paying every normal cost. From commitment until your next regular start you cannot commit anyReaction, even if the spell is countered; existing stacked Reactions finish. Separately, at first legitimate initiative roll of a real encounter, you may immediately prepare one legal normalActioncantrip as a non-action: pay components/independent RP/history, establish held concentration, open interruption, and use the same single pendingReady slot. NEW release that cantrip once without an Action on any later actual turn in that encounter, between completed events, retaining actual concentration until then; target legality rechecks at release. This replaces any oldReady, ends at encounter end or lostconcentration, cannot be banked again by reroll/reentry, and shares the free-stored-release cap of one per owner/numbered round with Arcane Calculus. No extra cast/copy/proc at release.
NEW exact banked-cantrip release window supersedes a narrower own-turn-only draft: the held cantrip may be voluntarily released without an Action or Reaction on any later actual turn before its preserved Ready deadline, between completed events, not retroactively or as an interruption. Use the shared one free release per owner per numbered round; no extra turn is created. Holding still consumes the one actual concentration/Ready slot and its original costs/history. Arcane Calculus retains its expressly narrower next-own-regular-turn release window.

### Worked boundaries

**MX-51-E01.** A banked cantrip paid at initiative can release on your second regular turn withoutAction if concentration survives.

**MX-51-E02.** Using theBAspell branch then leaves noReaction for Counterspell until the real next regular start.


## MX-52 — Spell Reflection (`spell_reflection`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/51`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define once-per-Short-Rest single-target redirect as an actual Reaction, caster target legality, original attack versus save/DC and recursion prevention. Separately define half-actual-spell-damage psychic retaliation once per round: attribution,range,rounding,resistance,zeroHP and repeated packets. Source text cannot automatically copy class/monster powers or all target riders.

**Decision:** Keep original caster ownership on redirection and bounded actual spell-damage reflection; no reflected copy, recursive retaliation, free spell or resource farming.

### Complete authoring text

Once SR/LR spendReaction in Spell Deflection’s same pre-payload window when you are the sole creature target of an actual single-target spell. NEW redirect to the original caster only if that caster is a legal recipient under its own spell’s target/range/line rules; preserve original owner, rank, attackbonus, DC, payment and concentration. Resolve its original attack/save against itself; no automatic self-hit or invented save. Noarea, multi-target, copied/alreadyredirected or protectedpayload; an illegal caster-recipient makes this activation unavailable withoutpayment. Redirecting does not teach/capture the spell. Separately, once per numbered round after an owned hostile spell deals positive actualnumericdamage to you, the living personally perceived caster within 60 ft/line of effect takes psychicdamage=floor(actualDamageDealt/2). NEW this passive retaliation requires you stillalive after the complete packet, noReaction, excludes overkill and self/friendly/copy/reflection roots, and consumes at first qualifying packet even if half rounds 0. Ordinary psychicdefenses apply. It cannot itself reflect, capture, heal, generate RP or restart a damageproc; no summing multiple area victims.

### Worked boundaries

**MX-52-E01.** A hostile spell removes 3 HP from HP 3 despite 12 rawdamage: if you survive, retaliation is 1 psychic, not 6.

**MX-52-E02.** A willing-only allybuff cannot be reflected into an unwilling original caster merely because it selected you.


## MX-53 — Stormcaller (`stormcaller`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/52`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve Nature OR undefined Spellcraft credential. Define15ft Static Field radius/placement/duration/concentration, entry/start cadence, damage/save and DEX-save-disadvantage ending, plus storm20ft variant. Separately define30ft Stormstep action/legal space,1d8 adjacent-thunder targets/save and afterimage half-cover geometry; two Short Rest ledgers and cover bypass stay distinct.

**Decision:** Adopt finite static field/Stormstep nonspell techniques with actual owned casting route and Nature-or-real-Spellcraft prerequisite; explicitly fix20ft storm radius at creation.

### Complete authoring text

Require actual spellcasting AND (Nature proficiency OR a separately established Spellcraft credential). Spellcraft is not an Arcana alias; if absent, use the Nature alternative. Once per beneficial SR/LR, an Action places a fixed 15 ft radius Static Field at a perceived point within 60 ft and line of effect, requiring concentration for up to one minute. It affects all creatures, including allies: first actual entry or regular start inside per target per numbered round deals 1d6 lightning automatically. Placement covering a creature counts as entry once. While inside an active field, creatures have disadvantage on DEX saves, ending immediately on exit; actual immunities/suppression apply. Outdoors during an established storm, choose a 20 ft radius at creation. A separate once-SR/LR Action, Stormstep, teleports you up to 30 ft to a visible fitting unoccupied space with line of effect. Every other creature within 5 ft of arrival makes a DEX save against your actual casting DC for 1d8 thunder, half on success. NEW select the actual owned casting route at acquisition for both feat activations. Your afterimage supplies half cover until your next regular start only when the geometric ray from the incoming effect origin to your new position passes through your previous occupied space; it is not a solid object or general AC bonus. During an actual outdoor storm, your lightning spells also ignore half cover, but not stronger cover. These activations are nonspell magical feat techniques; they do not create weather, RP or extra casting resources.
NEW storm-size choice is fixed at creation, as this proposal specifies:20ft requires actual outdoor-storm premises at that placement. A later weather change does not enlarge or shrink the placed field; suppression, concentration and its original minute deadline still end it. The separate half-cover benefit checks the actual outdoor-storm predicate when each lightning spell attack resolves. These are source-authoring completions, not permission to interpret the named storm’s setting origin.

### Worked boundaries

**MX-53-E01.** Entering then exiting/reentering thefield inoneround deals onlyonepulse tothatcreature.

**MX-53-E02.** A normalrainstorm canqualifyif theDirector’s actualweatherrecord saysstorm; thefeat doesnotdeclareone.


## MX-54 — Temporal Theory (`temporal_theory`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/53`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define unused move/object-interaction/Bonus Action as actual existing separate budgets, not an interchangeable Action. Specify end-turn banking,max2,expiry/type-preserving spending on later turns,no overlap/double-spend and real movement units. Resolve after2spent-per-encounter fatigue as an actual condition, timing and recovery. No action generation, extra turns or unfinished Time Loop activation.

**Decision:** Adopt two recorded unused native-budget tokens and one end-encounter Exhaustion cost after spending two; no generated budget rebanking, erased spent movement or Strain alias.

### Complete authoring text

At your original regular-turn end, bank at most one genuinely unused NORMAL allowance: your wholly unspent movement budget, ordinary free object interaction, or unused ordinary Bonus Action. You must be conscious, able to act and actually possess it; prohibited, extra, borrowed, banked, readied or generated allowances cannot fund a token. Movement requires zero movement spent this turn; snapshot actual legal distance and modes. Consume the chosen allowance into one typed token; hold at most two, expiring at encounter end. On a later own regular turn, spend at most one token of each type without Action for its exact purpose: move up to min(stored feet, current legal normal Speed), one ordinary interaction, or one currently legal BA ability. Pay current terrain; modes must still exist. No conversion to full Action, Reaction, work time or new token, and no refresh of feature uses/cadences. After the second token spent in the real encounter, record one irrevocable fatigue cost due at encounter end: NEW one Core Exhaustion level, with actual immunity/recovery and lethal level 6 rules. Further spending creates no extra fatigue under this source but cannot erase the cost. No Time Loop, rewind or resource restoration.

### Worked boundaries

**MX-54-E01.** Store a wholly unused 30 ft movement allowance. If current Speed is 20 when later spent, it supplies at most 20 additional feet, with current terrain costs.

**MX-54-E02.** A Bonus Action supplied by Mystic Recoil cannot be banked into a persistent token.


## MX-55 — Trapcasting (`trapcasting`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/54`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Preserve Conjure Flora OR Verdant Bond gate without granting seedlings by implication. Define source seedling trap mode, real hostile entry/forced movement, save/DC/cadence/damage/restraint/poison duration and detection/disarm. Bind Bonus Action detonation consuming exactly one seedling,10ft geometry,2d6 chosen type,targets/save and conservation with existing commands/expiry.

**Decision:** Adopt entry-trigger/burst exceptions explicitly spending the same one owner-round offensive-companion allowance as ordinary plant commands; no simultaneous free offense or recreated plants.

### Complete authoring text

Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.
NEW phase exception is explicit: its first eligible hostile-entry attack may occur on that actual entry outside the ordinary attached phase, but spends the same owner-round offensive companion allowance immediately. Its paid burst likewise spends that allowance; neither can occur when it is already spent. Placement itself is not an entry-trigger unless this exact procedure expressly says so. General Conjure Flora commands retain their attached phase, shared Bonus Action and sensory channel.

### Worked boundaries

**MX-55-E01.** Forced hostile entry can trigger a plant, but another plant cannot produce a second offensive outcome after the group allowance is spent that round.

**MX-55-E02.** Detonation consumes the actual plant even if every creature saves. An expired plant cannot be detonated.


## MX-56 — Verdant Bond (`verdant_bond`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/55`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Preserve simple plant communication/coarse sensations within60ft, Nature advantage in wilderness, active-flora+1 nature spell DC/attacks, plant-terrain movement and24-hour stored warning. Define finite eligible natural-spell predicate,actual senses/knowledge,one stand/message/ally trigger and costs. No universal sentience, omniscient plants, new conjuration or cosmology review.

**Decision:** Adopt actual plant-linked Druid/Ranger/Shaman route bonus and one finite real audible message; include owner as an eligible ally, preserve LAX evidence and original spell access.

### Complete authoring text

While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Distinct eligible flat feat bonuses add under FS-03; this same feat contributes only once. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.
SOURCE ally scope: the owner may be the one chosen message recipient. It triggers on that recipient’s first genuinely future qualifying passage after recording, not immediate creation beside the tree; the audible stored message is not private telepathy or general tree fluency.

### Worked boundaries

**MX-56-E01.** With an active qualifying plant, a spell actually cast through the Ranger route gains the stated+1DC. An independently acquired eligible Spell Focus+1 adds, for+2total; duplicate Verdant Bond does not.

**MX-56-E02.** The stored message is audible to anyone close enough to hear when the designated ally triggers it.


## MX-57 — Voltyros Pact (`voltyros_pact`)

**Disposition:** AUTHOR_FROM_EXACT_REPLACEMENT_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/56`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Resolve Stormcaller OR Lightning Affinity pluslevel6 mechanically while preserving the named pact/plane text for post-push review. Define one extra target15ft/half-lightning damage,actual chain eligibility and no recursion. Define a stationary full-round marker, forced movement, all-damage resistance endpoint,+2 spell damage packet; define30ft4d6 line activation,save/DC,width and Long Rest use.

**Decision:** Adopt bounded one additional lightning recipient, actual stationary Eye interval and separate finite line; keep the printed+2 personal spell scope, no weather, RP or plane-origin grant.

### Complete authoring text

Require character 6 AND (Stormcaller OR Lightning Affinity); preserve the named pact/plane story undecided. Once per personal noncopy lightning spell’s initial resolution, choose one additional creature within 15 ft of one original recipient, perceived with line of effect from that recipient. It must satisfy original creature eligibility and not already be targeted by that cast. Deal only half the selected original native lightning packet before defenses, rounded down; use the original DC/save ability for a fresh save or original attack bonus for a fresh attack, with original half/none on success. No other riders, new cast or chain from a chain. After one entire original start-to-next-start interval without any position change, gain Eye of the Tempest: resistance to all damage and+2 to one immediate native packet/shared roll of each personal spell until the following regular start. Any movement, teleport or forced displacement ends Eye immediately; riding a moving mount counts as movement. Repeated stationary intervals may renew without stacking. Separately, once LR use Action for a 30 ft-long 5 ft-wide lightning line: all creatures DEX save,4d6 lightning half success. DC=8+PB+one actual casting ability selected at acquisition, or INT if no casting source. The line is a magical nonspell feat technique, with noRPpool or weather creation.
The Eye bonus is+2 to one immediate native packet/shared roll of each personal spell as printed here; it is not limited to lightning spells. Half-damage chaining uses a resolved native lightning packet, not an attack that missed, a reflected/copy result, external rider or new target-independent resource event. Existing stance, terrain, body and actual stationary interval rules remain.

### Worked boundaries

**MX-57-E01.** Native 17 lightning damage gives a chain base of 8 before the new target’s save and defenses; that child cannot chain again.

**MX-57-E02.** Forced movement prevents the stationary interval. Riding a moving mount is not stationary.


## MX-58 — Wounding Magic (`wounding_magic`)

**Disposition:** AUTHOR_FROM_SUBMITTED_PROCEDURE_WITH_FINAL_SHARED_RULES.

**Source:** `DescentReviewChanges/ReviewBible/data/director/magic_extended_feat_operating_proposal_internal.json` `/records/57`; file SHA-256 `e8fdd919d8ffab3a01e7ff494edee3a45141375383ec4ec9f7c4224e1f250380`.

**Original question:** Define optional spell-damage Agony application,frequency,target/source ledger,1d4 necrotic start pulses,3round duration,save ability/DC and cure/suppression. Define disadvantage only on actual existing CON healing/resurrection saves and compatibility with Wounded/true-healing gates. No invented healing save, resurrection permission or soul taxonomy; secondary damage cannot recursively create wounds.

**Decision:** Adopt separate three-tick spell Agony with exact immunity/cure/deadline metadata, not Core Wounds, extra spell casts or an invented healing saving throw.

### Complete authoring text

After your personally cast noncopy spell deals positive resolved damage, optionally apply one Agony record to one living damaged target, once per owner/target/numbered round. Reapplication refreshes one profile without stacked dice. It deals 1d4 necrotic at the next three original target regular-start markers; a CON save against the generating cast DC at each affected regular end, including a current turn if applicable, ends it. The final third scheduled pulse ends the record after damage; no extra ending save afterward. It is a magical ongoing wound, not Core Wound, maximum HP injury or Bleeding by name. NEW a legal positive-potential magical heal or Action Medicine vs source DC ends it; suppressed records remain curable. While active, disadvantage applies only to actual existing CON saves to regain HP and actual saves against resurrection effects; no such save is invented. Death suspends living damage, retaining only the unexpired record tied to that exact death instance until the original third-start deadline; missed pulses are consumed, never backlogged. A legal revival closes that corpse-specific resurrection rider and retains only any still-future living pulse schedule until cured/expired. This grants no resurrection block or permission. Secondary ticks cannot create further Agony, copies, lifesteal or resource procs. Any independent Necrotic Affinity seal needs its own real fatal-root predicate.

### Worked boundaries

**MX-58-E01.** The first 1d4 pulse resolves at the target’s regular start; a successful CON save at its regular end removes the remaining pulses.

**MX-58-E02.** A normal heal with no save gains no new saving throw. Death skips living pulses without extending the original deadline or granting resurrection permission.

