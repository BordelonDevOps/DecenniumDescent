# Extended magic feats: proposed operating procedures

**UNADOPTED AND UNSENT.** All58 full source feats remain pending joint review. These procedures and116 examples are authored proposals, not full runtime implementations or numerical balance approval. Original descriptions, detailed effects, legacy fields and all eight identified conflicts remain preserved.

[Structured procedures and complete dependencies](../../data/director/magic_extended_feat_operating_proposal_internal.json) · [Original source questions](../../../../docs/audit/2026-10-08/full-game/MAGIC_EXTENDED_FEAT_SOURCE_AUDIT.md) · [Preservation checks](../../../../docs/audit/2026-10-08/full-game/MAGIC_EXTENDED_58_OPERATING_PROPOSAL_CHECK.json)

## Shared proposed rules

### Authority

UNADOPTED AND UNSENT. Preserve all 58 full original objects/questions, fourteen counterpart records, eight description/effect conflicts, current reviewed interfaces and five Mirrorsage comparisons. Every completion below is a proposed adjudication for joint review. A proposed feat does not activate its spell, class, temporal or cosmology dependencies. No source deletion, public registry change, human balance approval or whole-game closure is implied.

### Acquisition and resources

Use a real feat opportunity, the printed permanent prerequisite, actual repertoire, class-specific spell rank/ability and actual body/component permissions. Level without a class name means total character level. Prerequisites are checked on acquisition; temporary score loss does not remove an acquired feat. These feats grant no RP pool, class levels, Echo archive or alternate resource unless an explicit profile below says so. No RP capacity means RP recovery is 0 and RP-priced activations remain unaffordable. SR/LR mean actual beneficial completed rests; initial acquisition starts finite uses available, but cannot reset an already recorded same-identity use through reacquisition.

### Clocks

Use canonical actor, source, target, application, cast, encounter, numbered round and beneficial-rest identities. Next turn means the next future regular turn; original virtual duration markers remain through initiative changes. Once-round allowances do not reset on extra turns or initiative entry/exit. Outside initiative preserve the world six-second phase. Real encounters require meaningful opposition; staged allies, conjured farming bodies and artificial repeated initiative do not reset combat benefits. A spent use remains spent after failure, replacement, suppression or interruption.

### Casting and arithmetic

Actual casts retain access, RP/material costs, components, shared concentration and Dissonance/Refrain, followed by the legal Counterspell window. Ready casts at preparation, releases without a second cast. A completed cast below means one that survived interruption and resolved its immediate payload or successfully established its held/ongoing effect; targets may still save or take 0. Select the actual class/school/rank per cast. Same-stat flat bonuses use the current strongest eligible bonus unless an explicitly approved exception permits addition; this proposal creates no blanket stacking exception. Resistance of the same type never compounds. Round fractions down. Native damage/healing is the spell’s own formula before external feat/class bonuses, defenses and recipient caps; preserve separate typed components and actual packet boundaries.

### Copies and redirects

Retain root/source provenance. A copy, stored repeat, redirection or reflected packet is not another ordinary cast and creates no further copies, cast procs, resource outputs, item production or captured records. The specific original caster pays once; ownership does not silently migrate. Explicitly permitted secondary healing still respects current causal ledgers and source flags. Numeric actual damage includes real temp HP absorption and actual normal HP lost, excludes overkill and state assignments. No staged/cooperative threat qualifies for resource farming.

### Independent blood-cost proposal

NEW for Arcane Transfusion and Blood Magic, retain their printed damage type and unreducible DAMAGE classification, but explicitly require normal HP funding: declared 2×amount must be affordable while leaving at least 1 normal HP, bypass temp HP and cannot be reduced, transferred or paid by a floor. This is not the reviewed Blood Ritual, which has no HP payment. Resolve normal Wound/death/concentration consequences of the full self-damage packet; a fatal Wound can still kill the payer. Such cost damage is not an enemy attack, does not generate resources, damage reflection, lifesteal or excess conversion, and cannot pay itself. All costs/use commit before resolution; death or independent action loss prevents an unfinished dependent activation without refund. Overchannel instead uses its expressly distinct post-resolution backlash rule.

### Added dice

Unless a feat below expressly says otherwise, an extra damage die changes one selected native immediate damage packet, chosen at declaration, not every ray, target or future tick. For a genuine shared area roll it changes that one roll for all original eligible recipients. Choose one existing native damage die/type; a flat-only spell has no die to copy. Apply the added die before the spell’s save fraction and recipient defenses; an actual critical doubles damage dice normally, including added dice. It adds no new hit, damage root, target or on-hit entitlement. Maximize/reroll mechanics retain their actual source scope.

### No cosmology decision

Pact descriptions, named planes and temporal flavor are preserved as source text. The proposed mechanical permissions below do not establish the existence, structure, inhabitants or origin of any plane, patron or soul. Actual existing source travel rules retain their scope. Careful cosmology review remains after the authorized push and verified remote commit.

## MX-01 — Arcane Armor

Identity: `arcane_armor`. Original prerequisite: **Level 4**.

**Original effect, unchanged**

While you are casting or concentrating on a spell, gain a +1 bonus to AC and saving throws against reactions triggered by that casting.

**Proposed operating procedure**

Require character level 4. NEW the qualifier governs BOTH+1 AC and+1 saving throws: they apply only against a Reaction whose actual printed trigger is your casting or continuing concentration on a spell. Begin eligibility at commitment of that cast, before interruption; end when its casting/held concentration/ordinary concentration ends. Merely attacking a concentrating caster is insufficient. The relevant Reaction must itself cause an attack against you or a save you make; Counterspell’s caster-side ability check is neither and receives no penalty. A triggered attack still uses ordinary critical rules. The bonus is passive, grants no Reaction, and cannot protect unrelated attacks or ongoing damage. Current same-stat bonus arbitration applies. Preserve the alternative broad AC reading and old 5% resistance as inactive source alternatives.

**Explicit NEW choices:** Both bonuses are narrowly trigger-qualified, including an expressly concentration-triggered Reaction; no general AC or resistance.

**Authored adjudications**

- An actual on-cast Reaction attacks AC 14: eligible+1 makes AC 15, unless a stronger same-stat bonus already governs.

- An enemy’s ordinary attack during your ongoing concentration receives no Arcane Armor modifier.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "arcane_armor",
  "name": "Arcane Armor",
  "description": "A caster reinforces their defenses with a brief arcane ward while shaping a spell.",
  "prerequisite": "Level 4",
  "effect": "While you are casting or concentrating on a spell, gain a +1 bonus to AC and saving throws against reactions triggered by that casting.",
  "type": "Magic",
  "legacyEffect": "+5% resistance while casting",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve whether the reaction-trigger qualifier limits both AC and saves, or only saves, and what concentrating contributes after casting ends. Identify casting-triggered reactions, onset before interruption, exact expiry, stacking and level4 gate. Preserve inactive+5-percent legacy text without turning the ward into general resistance.

</details>

## MX-02 — Arcane Flexibility

Identity: `arcane_flexibility`. Original prerequisite: **Intelligence 15+**.

**Original effect, unchanged**

When you finish a short rest, exchange one prepared spell for another spell of the same tier that your class can prepare.

**Proposed operating procedure**

At completion of each beneficial Short Rest, optionally replace exactly one currently prepared spell in one actual class preparation list with another spell of the same rank in that same class. It must already be a legal known/book/repertoire choice under that class’s preparation procedure and current class level/school limits. Decide after ordinary rest endpoints/recovery; record the previous and replacement preparation. No extra prepared capacity, learned spell, copied grant or class alias. A class without a preparation list gains no new list. NEW unpreparing does not retroactively dispel a legally ongoing spell; maintain its actual concentration/deadline, but no new cast through the removed preparation. One exchange per rest event across classes, not one per class or duplicate feat representation.

**Explicit NEW choices:** One character-wide exchange and preservation of already established effects, without inventing preparation access.

**Authored adjudications**

- A Wizard exchanges one prepared Wizard-rank 2 spell for another already eligible Wizard-rank 2 spell after SR.

- Knowing the replacement through another class at rank 2 does not establish Wizard preparation eligibility.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "arcane_flexibility",
  "name": "Arcane Flexibility",
  "description": "Careful preparation leaves room to exchange one readied spell when the party rests.",
  "prerequisite": "Intelligence 15+",
  "effect": "When you finish a short rest, exchange one prepared spell for another spell of the same tier that your class can prepare.",
  "type": "Magic",
  "legacyEffect": "Swap one prepared spell per rest",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind prepared spells to an actual class repertoire and same class-specific rank; specify completed Short Rest, replacement timing, losing a currently maintained spell and temporary/copied grants. Does this permit a class without prepared spells to prepare one? Preserve the existing acquisition limits and no imported preparation subsystem.

</details>

## MX-03 — Arcane Pulse

Identity: `arcane_pulse`. Original prerequisite: **Level 7**.

**Original effect, unchanged**

As an action, spend 3 RP to release force in a 10-foot radius. Creatures of your choice make a Strength save against your spell save DC, taking 3d6 force damage and being pushed 10 feet on a failure, or half damage without the push on a success.

**Proposed operating procedure**

At character level 7, use an Action and pay 3 actual shared RP. NEW this is a magical feat technique, not an ordinary spell: no rank, spell components, Counterspell window or Dissonance/Refrain from this activation. At acquisition choose INT, WIS or CHA permanently for this feat’s DC=8+PB+that current modifier; this supplies neither spellcasting qualification norRPcapacity. Center a 10 ft radius on your own occupied space under ordinary area geometry. Choose perceived creatures with line of effect in it, including yourself if desired, before rolling. Roll 3d6 force once. Each makesSTRsave: failure full damage then push up to 10 ft directly away from the origin along a legal unobstructed route; success half damage rounded down, no push. Self can take damage but has no away-from-self push. Stop at obstruction/occupied destination; no collision damage, opportunity attack or unstated prone. Large bodies retain real fitting requirements. Immunity to forced movement blocks only push.

**Explicit NEW choices:** Explicit nonspell classification and permanent mental-stat choice fill the missing noncaster DC without creating RP.

**Authored adjudications**

- A level 7 Warrior with noRPpool cannot pay 3 RP, even though acquiring this feat was legal.

- A shared roll 11 produces 11 on failure or 5 on success; a wall 3 ft behind the victim limits actual push.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "arcane_pulse",
  "name": "Arcane Pulse",
  "description": "Condensed force erupts around the caster, driving nearby foes away from the blast.",
  "prerequisite": "Level 7",
  "effect": "As an action, spend 3 RP to release force in a 10-foot radius. Creatures of your choice make a Strength save against your spell save DC, taking 3d6 force damage and being pushed 10 feet on a failure, or half damage without the push on a success.",
  "type": "Magic",
  "legacyEffect": "AoE force blast knocks back enemies",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define spell versus nonspell classification, casting ability/DC for a level7 character without casting, actual shared RP access and payment. Specify self-centered10-foot geometry, sight/line, chosen targets including self, one damage roll, Strength save, push direction/collision and half rounding. No resource pool is created by an unstated prerequisite.

</details>

## MX-04 — Arcane Recall

Identity: `arcane_recall`. Original prerequisite: **Level 10**.

**Original effect, unchanged**

After casting a ranked spell, recover RP equal to that spell’s tier, to a maximum of 5 RP. You regain this use after a long rest.

**Proposed operating procedure**

After a completed personal rank 1–9 cast, optionally consume the once LR use to recover min(actual rank,5, RP headroom, unrefunded RP actually paid for that cast). NEW the funding ceiling counts only actual personal RP expenditure, including legal surcharges; it cannot refund charges, HP, other pools, free price or an ally’s contribution. Register the cast’s paid RP and every direct refund/recovery against the same expense once, across this feat and other refund sources; choose a legal order without exceeding that expense. A legal fully saved/missed cast qualifies; countered/interrupted, copied or released-again casts do not. A readied cast qualifies once when successfully prepared, never at release. If the computed recovery is 0, decline before committing the use; no newRPpool/cap. Ordinary ongoing effects need not finish their entire duration.

**Explicit NEW choices:** Completed-cast timing and shared actual-expense ceiling resolve zero-cost/refund loops.

**Authored adjudications**

- Rank 3 paid 5 RP with enough headroom returns 3; a previous 4 RP refund leaves at most 1 for Recall.

- A free charged rank 3 cast cannot produce 3 RP through this proposed funding rule.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "arcane_recall",
  "name": "Arcane Recall",
  "description": "Practiced recall recovers a spent spell through a deliberate return to its familiar pattern.",
  "prerequisite": "Level 10",
  "effect": "After casting a ranked spell, recover RP equal to that spell’s tier, to a maximum of 5 RP. You regain this use after a long rest.",
  "type": "Magic",
  "legacyEffect": "Regain used spell once per day",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define actual completed ranked cast, tier/rank, min(rank,5) recovery, RP ceiling, zero-cost or interrupted casts, rest use and timing relative to other refunds. Decide paid-cost/funding safeguards with current recovery rules; preserve current effect separately from regain-used-spell legacy.

</details>

## MX-05 — Arcane Transfusion

Identity: `arcane_transfusion`. Original prerequisite: **Level 9**.

**Original effect, unchanged**

As a bonus action, take necrotic damage equal to twice the RP restored; this damage cannot be reduced. Restore up to your proficiency bonus in RP. You regain this use after a long rest.

**Proposed operating procedure**

Once LR as a Bonus Action, choose integerN from 1 through min(current PB, actualRPheadroom) and preflight the shared normal HP funding rule for 2 Nnecrotic damage. Commit BA/use, then resolve that cost as one packet with normal Wound/death/concentration consequences. If still alive after the complete packet, restore exactlyNactual RP, capped by then-current capacity; later headroom loss does not refund HP. NEW this explicitly bypasses temp HP, resistance, redirection and floors for funding while retaining damage consequences. No use at 0 HP without an exact independent BA permission and sufficient actual funding, which the at-least 1 HP requirement normally forbids. No heal, charge creation, maximum RP increase or incidental resource trigger from self-damage. Ordinary later paid healing remains possible; it does not reset this LR use.

**Explicit NEW choices:** DeclaredN/headroom, normal HP funding and survival-before-credit are explicit NEW safeguards.

**Authored adjudications**

- PB 3 and 2 missing RP allowN 2: lose 4 normal HP and, if surviving, regain 2 RP.

- HP 4 cannot fundN 2 even with 20 temp HP; the illegal attempt spends nothing.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "arcane_transfusion",
  "name": "Arcane Transfusion",
  "description": "The caster trades endurance for magical reserve, drawing power from their own vitality.",
  "prerequisite": "Level 9",
  "effect": "As a bonus action, take necrotic damage equal to twice the RP restored; this damage cannot be reduced. Restore up to your proficiency bonus in RP. You regain this use after a long rest.",
  "type": "Magic",
  "legacyEffect": "Convert HP to mana at 2:1",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Specify declared restoration amount and actual RP headroom before paying2 necrotic damage per RP; define unreducible damage versus true-HP funding, temporary HP, zeroHP/incapacity, Wounds, concentration and interrupts. Bind proficiency cap, Bonus Action and Long Rest ledger; prevent recovery/healing loops without silently importing Blood Ritual costs.

</details>

## MX-06 — Blood Magic

Identity: `blood_magic`. Original prerequisite: **Level 9**.

**Original effect, unchanged**

When casting a spell, you may take necrotic damage equal to twice the spell tier to increase its save DC by 1 or add one damage die. This damage cannot be reduced. Once used, you cannot use this feat again until a short rest.

**Proposed operating procedure**

Once per beneficial SR or LR, when committing an actual spell, declare either+1 to that cast’s spell-save DC or one extra native damage die under the shared added-die procedure. Pay the spell’s actual ordinary costs plus 2×its actual rank as the shared unreducible-necrotic normal HP cost, before establishing its new concentration and opening interruption. Existing concentration must face the self-damage normally before displacement; death/action loss aborts the unfinished spell without refund. Rank 0 explicitly costs 0 HP but still spends the feat use; a cantrip is not excluded by the source. DC mode changes all actual saves caused by that same cast, including its legal repeats, while that cast lasts; it supplies no saves to automatic effects and no inherited DC for unrelated children. Damage mode cannot modify a flat-only or nondamaging spell. No two modes, doubled cast orHPrefund; copying never regrants the modifier.

**Explicit NEW choices:** Rank 0 allowed at 0 HP cost; one native packet for die mode and one whole cast’s genuine saves for DC mode.

**Authored adjudications**

- Rank 2 spell DC 14 becomes 15 after 4 normal HP cost; an ordinary area save for each target uses 15.

- A flat damage effect has no eligible die for die mode; choose a legal DC mode or decline before payment.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "blood_magic",
  "name": "Blood Magic",
  "description": "An experienced caster draws on their own vitality to boost a spell.",
  "prerequisite": "Level 9",
  "effect": "When casting a spell, you may take necrotic damage equal to twice the spell tier to increase its save DC by 1 or add one damage die. This damage cannot be reduced. Once used, you cannot use this feat again until a short rest.",
  "type": "Magic",
  "legacyEffect": "Boost spell using own HP",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve spell tier0, actual paid casting route, declaration and the choice of+1 DC or one damage die. Define die type/packet/targets/critical/maximized cases, all-save versus one-save scope and the2xTier unreducible-necrotic payment at zeroHP. Use Short Rest ledger; no double dipping with reviewed Blood Ritual or copied results.

</details>

## MX-07 — Channeled Flow

Identity: `channeled_flow`. Original prerequisite: **Level 10**.

**Original effect, unchanged**

When a spell requires you to spend an action on later turns to maintain it, you may maintain it once as a bonus action instead. You regain this use after a short rest.

**Proposed operating procedure**

Once per beneficial SR or LR, on your own actual later turn, replace one Action explicitly required solely to maintain one of your already established spells with one Bonus Action. Declare and consume at that maintenance commitment. Preserve concentration, RP/material upkeep, targeting, existing pulse/command limits and the original spell deadline. It cannot shorten initial casting, Ready setup, a ritual, an attack granted by the spell, or an optional Action to issue a new damaging command unless that exact source identifies it as required maintenance. An Action that combines required maintenance with another benefit retains the combined printed payload but still supplies no second occurrence. One actual BA must be available; Incapacitated/other restrictions still apply. The source’s prior 50% duration wording remains an inactive alternative.

**Explicit NEW choices:** Only one actual later maintenance commitment changes action type; no duration or extra activation.

**Authored adjudications**

- Maintaining an existing spell with an explicit Action upkeep uses BA once, retaining its required 2 RP upkeep.

- A summoned creature’s optional attack command is not automatically qualifying maintenance.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "channeled_flow",
  "name": "Channeled Flow",
  "description": "Sustained focus carries a channel spell beyond its usual duration.",
  "prerequisite": "Level 10",
  "effect": "When a spell requires you to spend an action on later turns to maintain it, you may maintain it once as a bonus action instead. You regain this use after a short rest.",
  "type": "Magic",
  "legacyEffect": "Extend channel spells by 50%",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve current one maintained Action replaced by one Bonus Action per Short Rest, not the legacy50-percent duration extension. Define qualifying actual later-turn maintenance, costs/concentration, prohibited actions, which turn spends the use and whether other commands share the same action budget.

</details>

## MX-08 — Concentrated Will

Identity: `concentrated_will`. Original prerequisite: **Level 5**.

**Original effect, unchanged**

Gain a +2 bonus to Constitution saving throws made to maintain concentration.

**Proposed operating procedure**

At character level 5, gain+2 on actualCONsaving throws made to maintain concentration, including nonspell concentration that explicitly uses the same save. Apply current same-stat flat-bonus arbitration; ordinary advantage/disadvantage and proficiency remain independent. Each genuinely separate damage packet generates only its actual required save, not one per damage type or extra feat test. No modifier to unrelated CON, Wound or death saves, automatic concentration loss from incapacity/death, or a special source’s non-CON test. This creates neither concentration capacity nor permission to act at 0 HP. A legally held Ready spell has actual concentration and qualifies.

**Explicit NEW choices:** Actual CON concentration scope with current strongest-bonus stacking.

**Authored adjudications**

- A real damage concentrationCONsave gets the feat bonus and can also have existing advantage.

- Becoming Incapacitated ends ordinary concentration without a save; the feat cannot invent a roll.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "concentrated_will",
  "name": "Concentrated Will",
  "description": "At level 5, sustained focus receives the listed +2 bonus on concentration checks.",
  "prerequisite": "Level 5",
  "effect": "Gain a +2 bonus to Constitution saving throws made to maintain concentration.",
  "type": "Magic",
  "legacyEffect": "+2 to concentration checks",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind+2 to actual Constitution concentration saves, spell and nonspell concentration scope, multi-packet damage timing, advantage/disadvantage and stacking with Combat Casting/War Caster. Level5 is a prerequisite, not a caster level or new ability modifier.

</details>

## MX-09 — Counterspell Adept

Identity: `counterspell_adept`. Original prerequisite: **Level 6**.

**Original effect, unchanged**

Gain a +2 bonus to checks made to counter or interrupt a spell. If your system uses a save DC instead, increase your counterspell DC by 1.

**Proposed operating procedure**

At character level 6, NEW select the active effect’s+2 over preserved description/legacy+4. Add+2 to an actual ability/task check whose operative source directly counters or interrupts a pending spell, using current strongest same-stat bonus rules. Ordinary Counterspell remains actual casting ability+PB versus 10+2×trigger rank, with task degrees/natural shifts collapsed to success/failure. The alternative+1 DC branch applies only if a separately operational counter source truly uses its own save DC; current ordinary and cited class Counterspells use checks, so noDCbranch applies to them. Never apply both to one attempt. This feat grants no spell, Reaction, extra attempt, automatic low-rank success, spell attack bonus or check to identify magic.

**Explicit NEW choices:** Active+2 selected; conditionalDCbranch dormant where no actual DC-based source exists.

**Authored adjudications**

- Against rank 3, Counterspell DC 16 and ability+PB 5 become check+7 before rolling.

- Mystic Focus’s spell-attack bonus does not apply to that task check; neither feat invents a penetration check.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "counterspell_adept",
  "name": "Counterspell Adept",
  "description": "At level 6, practiced countering receives the listed +4 bonus on interrupt checks.",
  "prerequisite": "Level 6",
  "effect": "Gain a +2 bonus to checks made to counter or interrupt a spell. If your system uses a save DC instead, increase your counterspell DC by 1.",
  "type": "Magic",
  "legacyEffect": "+4 to interrupt checks",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

The description/legacy say+4 while active effect says+2 checks or+1 counterspell DC. Resolve that source conflict explicitly against the actual Counterspell procedure, what interrupt checks include, and whether the alternative DC clause has any current target. Do not apply both branches or grant Counterspell access.

</details>

## MX-10 — Dispel Precision

Identity: `dispel_precision`. Original prerequisite: **Intelligence 15+**.

**Original effect, unchanged**

When dispelling an effect from a target affected by multiple spells, choose the effect you attempt to end rather than determining it randomly. Gain +1 on the dispel check.

**Proposed operating procedure**

When a legal dispelling source would randomly select among individually eligible effects, choose its one eligible effect instead; identify an effect only to the extent the source permits. Ordinary reviewed Dispel Magic already chooses one perceptible ongoing spell rank 0–3 and ends it automatically: this feat changes neither its target count nor its rank/protection limits. Add+1 only to a real dispel check explicitly required by a different operative source. No check is invented for an automatic success, and no roll can exceed a source’s allowed scope. If the separate proposed Dispel Mastery is adopted, each of its legal targets retains its own existing procedure; Precision does not duplicate attempts. Hidden/protected curses, permanent magic items and class engines remain outside ordinary Dispel Magic.

**Explicit NEW choices:** Preserves already-standard selection and conditional+1 without inventing randomness or checks.

**Authored adjudications**

- Choose one visible rank 2 spell among three on a creature; ordinary Dispel Magic ends it without a+1 roll.

- A rank 5 effect remains ineligible for that ordinary spell despite this feat.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "dispel_precision",
  "name": "Dispel Precision",
  "description": "Precise arcane study improves the chance to remove the intended effect.",
  "prerequisite": "Intelligence 15+",
  "effect": "When dispelling an effect from a target affected by multiple spells, choose the effect you attempt to end rather than determining it randomly. Gain +1 on the dispel check.",
  "type": "Magic",
  "legacyEffect": "+20% chance to remove intended effect",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Use actual Dispel Magic selection/check rules. Determine whether selecting the effect is already standard and whether+1 affects each actual eligible dispel check. Resolve one target with several spells, automatic endings, Dispel Mastery extra target and no invented random selector or generic antimagic permission.

</details>

## MX-11 — Echo Spell

Identity: `echo_spell`. Original prerequisite: **Intelligence 15+**.

**Original effect, unchanged**

After casting a spell of Tier 1–3, you may create an echo. At the start of your next turn, repeat one numerical effect at half value without spending RP or changing targets. You regain this use after a long rest.

**Proposed operating procedure**

Once LR immediately after a personal rank 1–3 spell completes its initial payload, select one numeric damage, HP healing, temp HP or flat stat-bonus component and its original eligible recipients. NEW no echo from Ready preparation until actual release, copies, summons, creation, resource/action grants, movement, hard control or maxima-changing effects. Snapshot that component’s native roll/flat value before external bonuses, original attack/save rules, type, origin and source DC. At your next future regular start, if alive/conscious and any source-required concentration still holds, repeat only that component at half native value floored;0 gives no effect. Recheck original recipients’ actual range/perception/line of effect from the recorded origin, which must still exist; no replacement target. Make fresh original attack/save tests, then ordinary defenses/healing caps, without new critical dice or external damage/heal add-ons. A selected shared area retains only original recipients still in the original area. Temp HP uses the single grant ledger; a flat bonus uses strongest-family arbitration and expires at the earlier of original deadline or your next regular end. Echo heals block healing-copy/resource outputs and create no convertible excess. No new cast, RP, components or duration for the parent; an invalid echo expires without refund.

**Explicit NEW choices:** Finite numeric categories, explicit stored native magnitude, current defenses and nonrecursive single-start repeat; excludes state/resource production.

**Authored adjudications**

- An original native 11 force area creates a 5 force echo against original still-legal recipients, each with a fresh original save.

- A summoned creature’s HP, attacks and future turns are not a repeatable numerical spell component.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "echo_spell",
  "name": "Echo Spell",
  "description": "A prepared casting leaves an echo to repeat its effect next round at half power.",
  "prerequisite": "Intelligence 15+",
  "effect": "After casting a spell of Tier 1–3, you may create an echo. At the start of your next turn, repeat one numerical effect at half value without spending RP or changing targets. You regain this use after a long rest.",
  "type": "Magic",
  "legacyEffect": "Repeat spell effect next round at half power",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define creation timing, use/cost, next regular start, selected numerical effect and half rounding. Bound damage/healing/buff/area packets, targets moving or becoming illegal, saves/attacks, concentration, ownership and no recursive echo/cast/resource/action generation. Preserve Tier1–3 and compare Spell Echo Chamber without merging identities.

</details>

## MX-12 — Efficient Caster

Identity: `efficient_caster`. Original prerequisite: **Wisdom 13+**.

**Original effect, unchanged**

Once per round when you cast a ranked spell, reduce its RP cost by 1 (minimum 1). After using this feat a number of times equal to your proficiency bonus, regain all uses after a long rest.

**Proposed operating procedure**

Gain PB uses per completed LR, with current PB as maximum and no mid-epoch replenishment from growth. Once per numbered round, at a personal ranked cast’s declaration, optionally reduce its otherwise payable RP by 1, minimum 1. NEW apply after existing eligible base discounts and printed extra costs including component and strain/armor additions, but before final Resonance Influence; this is a discrete reduction, not a new base-rank price. A charged/free normal-price route still pays its independent costs; use is allowed only when this stage’s actualRPprice is at least 2. A genuine reduction commits both use and round entitlement with the cast, even if a later permitted final adjustment or interruption changes the outcome. Cannot reduce charges, HP, specialresources or manufacture a 1 RP charge on a 0 RP cast. Current rank/repertoire/strain cutoff remain.

**Explicit NEW choices:** Defined price-order placement and only actual positive reductions consume entitlement.

**Authored adjudications**

- A rank 1 cast’s eligible price 2 becomes 1 before a separately applicable final Influence adjustment.

- A charged spell with only 1 independent RP surcharge offers no reducible price and spends no feat use.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "efficient_caster",
  "name": "Efficient Caster",
  "description": "Measured spellwork lowers the RP cost of every spell.",
  "prerequisite": "Wisdom 13+",
  "effect": "Once per round when you cast a ranked spell, reduce its RP cost by 1 (minimum 1). After using this feat a number of times equal to your proficiency bonus, regain all uses after a long rest.",
  "type": "Magic",
  "legacyEffect": "-10% mana cost to all spells",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind once-per-round to the existing regular-turn clock, proficiency uses per Long Rest and ranked spell eligibility. Place−1/min1 in the actual RP cost order, accounting for ancestry charges, zero-price casts, armor additions, other reductions and final Resonance Influence. Resolve use expenditure if no reduction can occur.

</details>

## MX-13 — Energy Sink

Identity: `energy_sink`. Original prerequisite: **Wisdom 15+**.

**Original effect, unchanged**

When you succeed on a saving throw against a spell or take no damage from it, use your reaction to recover 1 RP. You can do so a number of times equal to your proficiency bonus per long rest.

**Proposed operating procedure**

PB uses per completed LR; no mid-epoch refill fromPBgrowth. After one actual hostile spell event targeting/affecting you resolves, if you either succeeded on its real save OR received no positive resolved damage from that event, you may spend a Reaction/use to recover 1 RP up to your real maximum. NEW require meaningful unwilling opposition: harmless, allied, cooperative, self-authored or farming spells do not qualify. A spell attack that legally targeted you but missed, immunity, or complete prevention can satisfy the no-damage branch; temp HP absorption is damage and alone cannot. A failed save against a hostile nondamaging control spell still satisfies literal no-damage, but only if its result leaves you able to react. One grant per actual cast identity across later ticks/events; no fan-out or repeating-zone farm. Positive saved-against damage may qualify through success. Resolve full damage/control/death first; no ordinary Reaction at 0 HP. Decline before spending if noRPheadroom. This is recovery, not transfer from the attacker or a new pool.

**Explicit NEW choices:** Hostile-threat and one-cast identity bounds preserve both printed branches while blocking harmless farming.

**Authored adjudications**

- Successful save halves a hostile spell to 5 damage: the success branch permits oneReaction for 1 RP.

- A missed hostile spell attack can qualify; receiving a friendly harmless cantrip cannot.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "energy_sink",
  "name": "Energy Sink",
  "description": "Hard-won magical resilience restores RP after a spell strikes.",
  "prerequisite": "Wisdom 15+",
  "effect": "When you succeed on a saving throw against a spell or take no damage from it, use your reaction to recover 1 RP. You can do so a number of times equal to your proficiency bonus per long rest.",
  "type": "Magic",
  "legacyEffect": "Restore mana when hit by spells",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define success-on-save OR no-damage trigger for one actual spell event, including harmless, friendly, prevented, immune, missed, ongoing and multi-target effects. Bind Reaction, PB uses, RP ceiling, actual caster attribution and zeroHP restrictions; decide anti-farming and refund limits explicitly, not by deleting one printed trigger.

</details>

## MX-14 — Ether Anchor

Identity: `ether_anchor`. Original prerequisite: **Level 12**.

**Original effect, unchanged**

You have advantage on saving throws against banishment, forced teleportation, and planar displacement. Once per long rest, you may choose to succeed on one such save.

**Proposed operating procedure**

At character level 12, gain advantage on actual saving throws against an effect that would banish, forcibly teleport or displace you between planes. Once LR, after such a save fails but before consequences, optionally replace that failure with success; use the source’s actual success outcome, which may retain other effects. No Action or Reaction is required. It does not create a save against a save-less effect, convert willing travel to hostility, anchor nearby creatures, reveal destinations or permit an otherwise illegal movement. A save against damage accompanying independent displacement qualifies only if that same save actually determines the unwanted displacement. Existing explicit unpreventable/no-replacement rules control. No permanent immunity or new cosmological fact is implied.

**Explicit NEW choices:** After-failure optional success on an existing displacement save only.

**Authored adjudications**

- A failed actual banishment save becomes success and consumes theLRuse.

- A source with automatic displacement and no save supplies no roll for this feat to improve.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "ether_anchor",
  "name": "Ether Anchor",
  "description": "At level 12, an anchored presence resists banishment effects.",
  "prerequisite": "Level 12",
  "effect": "You have advantage on saving throws against banishment, forced teleportation, and planar displacement. Once per long rest, you may choose to succeed on one such save.",
  "type": "Magic",
  "legacyEffect": "Immune to banishment effects",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve advantage plus one optional auto-success per Long Rest, not legacy immunity. Define an actual allowed save against banishment/forced teleport/displacement, declaration and no-save effects. Keep movement/space rules and do not invent planes, destinations or cosmological eligibility.

</details>

## MX-15 — Flash Cast

Identity: `flash_cast`. Original prerequisite: **Dexterity 14+**.

**Original effect, unchanged**

Once per long rest, cast a spell with a normal casting time of one action as a bonus action. You cannot cast another ranked spell during the same turn.

**Proposed operating procedure**

Once LR, declare an actually known/prepared spell with printed normal casting time oneAction as a Bonus Action instead; maintain every other access, component, RP, concentration and strain rule. NEW the whole actual turn, including any on-turn Reaction casts, may contain no other ranked cast before or after this cast. Preflight the turn’s existing cast history; committing this feat establishes the restriction even if countered. The chosen spell may be rank 0; other cantrips remain legal with their actual action resources. A later genuine extra turn is a distinct turn for this prohibition but does not refresh theLRuse or other regular-turn budgets. Ready release/copy with no new cast is not another ranked cast, while preparing a readied ranked spell is. No long-cast compression, Reaction conversion, free BA or universal restriction on unrelated turns.

**Explicit NEW choices:** Whole actual-turn ranked-cast history and optional rank 0 target preserve printed timing.

**Authored adjudications**

- After casting a ranked spell as anAction this turn, Flash Cast is ineligible even for a cantrip.

- Flash-casting a rank 2 spell allows a later legalAction cantrip but forbids an on-turn ranked Counterspell.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "flash_cast",
  "name": "Flash Cast",
  "description": "Quick spellwork grants the listed one instant-cast spell per day.",
  "prerequisite": "Dexterity 14+",
  "effect": "Once per long rest, cast a spell with a normal casting time of one action as a bonus action. You cannot cast another ranked spell during the same turn.",
  "type": "Magic",
  "legacyEffect": "1 instant-cast spell per day",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define normal one-Action casting, one Bonus Action, Long Rest use, costs/components and the whole-turn ban on another ranked spell before or after use. Resolve reaction casts on that turn, cantrips, extra turns, copied releases and interruption without importing a universal bonus-action spell restriction.

</details>

## MX-16 — Foresight Surge

Identity: `foresight_surge`. Original prerequisite: **Wisdom 13+**.

**Original effect, unchanged**

After you cast a divination spell, gain +2 initiative for the next hour. If initiative is already rolled, move up one place in the order at the start of the next round.

**Proposed operating procedure**

After a completed actual Divination cast, gain a nonstacking+2 to future initiative rolls for one elapsed hour, refreshing that deadline on later eligible casts. The selected casting class must use Divination for this identity. If already participating in rolled initiative, also queue one move up one baseline place at the next numbered-round boundary. NEW one queued move per owner per boundary; repeated casts cannot accumulate jumps. At that boundary finish previous-round events, restore temporary permutations, then process pending advances in stable activation order by swapping the owner with the immediately preceding still-participating baseline actor; top actor stays. Apply later reviewed temporary permutations, such as Future Echo, to the resulting baseline. Every participant still receives one regular slot. A departed/disabled pending record expires without makeup. Existing virtual deadlines, recharge, periodic clocks and spent budgets do not move or refresh; no reroll or extra turn.

**Explicit NEW choices:** One nonstacking hour bonus and bounded baseline swap with conserved regular turns.

**Authored adjudications**

- OrderA, B, C withCqueued becomesA, C, B next round;Cdoes not act again in the current round.

- Three Divination casts before that boundary still queue only one advance forC.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "foresight_surge",
  "name": "Foresight Surge",
  "description": "After casting divination, foresight grants the listed initiative increase.",
  "prerequisite": "Wisdom 13+",
  "effect": "After you cast a divination spell, gain +2 initiative for the next hour. If initiative is already rolled, move up one place in the order at the start of the next round.",
  "type": "Magic",
  "legacyEffect": "+10 initiative after casting divination",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve both+2 future initiative for one hour and one-place movement when already rolled. Define actual Divination cast, repeated applications, round-boundary update, top slot/ties, pending turn cursor and extra-turn conservation. A move in order must not create or delete a regular turn, refresh or pulse.

</details>

## MX-17 — Illusionist’s Trick

Identity: `illusionist_s_trick`. Original prerequisite: **Charisma 14+**.

**Original effect, unchanged**

The first time an illusory creature or object you create would be ended by an attack or interaction, it persists until the end of the current turn, allowing observers to make the normal investigation save afterward.

**Proposed operating procedure**

For each actual illusory creature/object you personally create, the first attack or interaction that would end that particular illusion’s existence instead delays only that ending until the current actual turn ends. NEW outside initiative use the end of the current canonical six-second window. It remains nonphysical and observers retain information already obtained; known illusions do not regain concealment, cover, belief or control. Losing required concentration, natural expiry, dispel, source death or another independent ending still ends it immediately. The feat does not postpone an observer’s ordinary Investigation check or direct physical proof unless that source’s actual rule specifically ends the illusion itself. At the deferred endpoint end the illusion as originally required; where the source only grants a disbelief test rather than termination, use its actual Investigation check/save at its printed timing, with no free new save type. Current Minor Illusion/Silent Image physical interaction reveals to observers but does not end the global image, so normally does not trigger this delay.

**Explicit NEW choices:** Per-illusion first actual destruction, preserving immediate evidence and source-specific Investigation.

**Authored adjudications**

- A source illusion explicitly destroyed by a hit can remain visibly present until this turn ends, with no substance.

- Walking through Silent Image reveals it immediately; this feat cannot make the witness believe the wall is solid.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "illusionist_s_trick",
  "name": "Illusionist’s Trick",
  "description": "Charisma 14+ gives an illusion the listed extra hit before it vanishes.",
  "prerequisite": "Charisma 14+",
  "effect": "The first time an illusory creature or object you create would be ended by an attack or interaction, it persists until the end of the current turn, allowing observers to make the normal investigation save afterward.",
  "type": "Magic",
  "legacyEffect": "Illusions take 1 extra hit before vanishing",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Identify actual illusory creature/object sources and their normal ending/investigation procedure; investigation save is not automatically a core save type. Define first hit/interaction, simultaneous invalidation, persistence through current turn, observers knowing the truth, concentration and nonphysical blocking. No real HP, extra creature or automatic belief.

</details>

## MX-18 — Lingering Magic

Identity: `lingering_magic`. Original prerequisite: **Wisdom 13+**.

**Original effect, unchanged**

When you cast a spell with a duration of at least 1 round and no concentration, extend its duration by 1 round. Once per spell.

**Proposed operating procedure**

NEW select the active+1 round wording over preserved 20%. At a completed nonconcentration spell’s creation, extend its finite stated duration of at least one round by exactly one six-second/regular-marker interval, once per original cast. Round effects add one original regular marker; minute/hour deadlines add 6 elapsed seconds. A Ready spell’s temporary held concentration does not disqualify a normally nonconcentration payload; extend its payload at release, never its Ready deadline. Independently capped charges, target counts, specified number of pulses, item stock and discharge/consumption endpoints remain. An ongoing effect whose ordinary pulse exists solely while its duration persists may get the one naturally reached extra pulse; an explicit three-pulse effect remains three. No extension of instantaneous/permanent effects, resurrection windows classified separately from spell duration, concentration spells, linked separate conditions, or an independent end such as destroyed support. No stacking with itself or repeated recasting of the same instance.

**Explicit NEW choices:** Exact 6 second extension, source caps preserved and Ready hold distinguished from payload concentration.

**Authored adjudications**

- A nonconcentration 60 second effect lasts 66 seconds unless independently discharged earlier.

- A printed three-pulse effect still has three pulses even if its remaining cosmetic duration extends.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "lingering_magic",
  "name": "Lingering Magic",
  "description": "Wisdom 13+ sustains spell effects for the listed 20% longer duration.",
  "prerequisite": "Wisdom 13+",
  "effect": "When you cast a spell with a duration of at least 1 round and no concentration, extend its duration by 1 round. Once per spell.",
  "type": "Magic",
  "legacyEffect": "Spell effects last 20% longer",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Use active+1 round once per nonconcentration spell, not description/legacy20percent. Define round-to-seconds/end-marker conversion for minute/hour spells, delayed riders, initial/recurring pulses, until-discharged effects and explicit caps. No extra charge, summon use or extension after an independent ending condition.

</details>

## MX-19 — Magical Fortitude

Identity: `magical_fortitude`. Original prerequisite: **Constitution 13+**.

**Original effect, unchanged**

Gain +2 to saving throws against spells.

**Proposed operating procedure**

Gain+2 to your actual saving throws directly required by an operative spell’s payload, including later repeat saves and a spell explicitly requiring a save to maintain another effect. Current strongest same-stat bonus arbitration applies, so another+2 save feat is not automatic+4. Ordinary damage-induced concentrationCONsaves, Core Wound saves and death saves are consequences of shared life/concentration rules rather than the damaging spell’s printed payload and receive no bonus from this feat; Concentrated Will has its own exact concentration scope. A spell that directly calls for a death-effect saving throw can qualify, but ordinary death saves do not. Magical nonspell class/item/feat effects are not spells unless their actual source classifies the activation as one. CON 13 is acquisition only; no new proficiency, casting ability or defense against a Counterspell task check.

**Explicit NEW choices:** Direct spell-save causation excludes ordinary damage concentration/Wound/death saves.

**Authored adjudications**

- A repeatWISsave explicitly supplied by an ongoing spell gains+2.

- TheCONsave to maintain concentration after taking a spell’s damage uses Concentrated Will if owned, not this feat.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "magical_fortitude",
  "name": "Magical Fortitude",
  "description": "A Constitution-trained caster or defender gains the listed +2 protection on saves against spells.",
  "prerequisite": "Constitution 13+",
  "effect": "Gain +2 to saving throws against spells.",
  "type": "Magic",
  "legacyEffect": "+2 saves vs spells",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define+2 on actual saving throws caused by spells, including repeat/concentration/death saves where applicable, and spell versus magical class/item effects. Constitution13 does not grant proficiency or spellcasting. Resolve stacking with other feats and jewelry without changing source save DCs.

</details>

## MX-20 — Mana Burn

Identity: `mana_burn`. Original prerequisite: **Intelligence 13+**.

**Original effect, unchanged**

When a creature fails a save against your damaging spell, it loses 1 RP if it has an RP pool. A creature can lose RP this way only once per round.

**Proposed operating procedure**

After a creature fails an actual save against your personally cast damaging spell, remove 1 from its realRPpool, minimum 0. NEW damaging means that same spell application has a native damage component governed by that save; full prevention/immunity may leave 0 damage without negating the failed-save trigger. A repeat save solely ending nondamaging control after earlier damage does not qualify. Commit one recipient-wide Mana Burn entitlement per numbered round across all owners/casts on the first qualifying failure with anRPpool, even at RP 0; no further loss that round. Resolve native damage and immediate survival replacements first, then loss if the target still exists as a living resource holder. No transfer to you, charge/RC/slot substitution, maximum reduction or loss from RP-less creatures. Copies, echoes and reflected packets cannot create a fresh proc.

**Explicit NEW choices:** One target-wide round record, failed damaging-save predicate and no resource substitution.

**Authored adjudications**

- Two casters trigger Mana Burn against the same RP 4 foe this round: total loss is 1, leaving 3.

- A target immune to the damage can still lose 1 RP after failing the associated save; an RP-less monster loses nothing.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "mana_burn",
  "name": "Mana Burn",
  "description": "Intelligence-trained offensive spellwork carries the feat's listed drain against an enemy's RP.",
  "prerequisite": "Intelligence 13+",
  "effect": "When a creature fails a save against your damaging spell, it loses 1 RP if it has an RP pool. A creature can lose RP this way only once per round.",
  "type": "Magic",
  "legacyEffect": "Offensive spells drain enemy mana",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind actual failed save against your damaging spell, including successful damage prevention, repeated saves, RP-less creatures and minimum0. Define one recipient-wide once-per-round ledger across multiple users, phase timing, no RP transfer to caster and no charge/slot pool substitution.

</details>

## MX-21 — Mental Buffer

Identity: `mental_buffer`. Original prerequisite: **Wisdom 15+**.

**Original effect, unchanged**

Once per long rest, when you would become confused, dominated, or unable to distinguish allies from enemies, ignore that condition until the end of your next turn.

**Proposed operating procedure**

Once LR, when a new source application would impose confusion/randomized action selection, a dominated/commanded Action or turn, or an explicit inability to distinguish friend from foe, voluntarily suppress only that application’s eligible control components through the end of your next future regular turn. No Action/Reaction is required; choose before those components first take effect. NEW qualify by actual written behavior, not a condition’s suggestive name. Ordinary Charmed/Frightened alone, illusion disbelief, blindness, truthful uncertainty and incapacity without such a component do not qualify. Preserve unrelated damage/slow and the original source, duration, concentration, repeat saves and spent hard-control entitlement. Suppressed clocks continue; legal ending saves still occur. If the original component has already expired or been cured by the boundary it never returns; otherwise it resumes for its remaining duration without replaying a past commanded turn. One application only, not immunity to later separate sources.

**Explicit NEW choices:** Voluntary temporary component suppression, with unchanged original clocks and no replayed command.

**Authored adjudications**

- A dominated Action scheduled inside the protected interval is skipped, not stored for a later extra command.

- Another source’s independent Stunned effect remains operative.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "mental_buffer",
  "name": "Mental Buffer",
  "description": "Wisdom 15+ supports the feat's listed once-per-day defense against confusion.",
  "prerequisite": "Wisdom 15+",
  "effect": "Once per long rest, when you would become confused, dominated, or unable to distinguish allies from enemies, ignore that condition until the end of your next turn.",
  "type": "Magic",
  "legacyEffect": "Negate confusion once per day",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define the exact source control components called confused/dominated/mistaken-allies and automatic versus voluntary use. Specify prevention versus suppression until end of next regular turn, underlying duration/save clocks, recurrence, multiple components and reactivation. Do not turn one-turn relief into a cure or unrestricted control immunity.

</details>

## MX-22 — Mirror Cast

Identity: `mirror_cast`. Original prerequisite: **Intelligence 16+**.

**Original effect, unchanged**

Once per long rest, cast a spell as though originating from a reflective surface you can see within 60 feet. Range and line of effect are measured from that surface.

**Proposed operating procedure**

Once LR at cast declaration choose a real reflective surface you can see within 60 ft of your actual body. NEW require an unobstructed line of effect from you to that surface, at least hand-sized, sufficiently exposed to form a recognizable reflection; a drawn picture of a mirror is insufficient. Choose an unoccupied origin point immediately at its visible face. Measure spell range/line of effect and area orientation from that point; you still must personally perceive targets where the spell requires it, receiving no remote senses. Self-area/cone origins can relocate, but a Self-only body buff still affects you and Touch spells still require actual touch; no remote grasp. Hostile-held surfaces may serve if visibly legal; no possession or movement of the object. Commit ordinary costs/components/feat use at your body, preserving its interruption window. The origin is snapshotted for immediate resolution; destruction before resolution fails the changed origin with no refund. Ongoing created areas retain their actual fixed/moving rules and deadlines; the mirror is neither a second caster nor an unprinted tether.

**Explicit NEW choices:** Visible substantial surface, body-to-surface line and explicit Self/Touch limits.

**Authored adjudications**

- A cone can originate at a visible mirror 40 ft away and point along a chosen legal direction.

- An unseen creature behind the mirror gains no free visibility; a Touch heal cannot cross 40 ft through it.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "mirror_cast",
  "name": "Mirror Cast",
  "description": "Intelligence 16+ permits the feat's listed once-per-day spell cast from a reflection.",
  "prerequisite": "Intelligence 16+",
  "effect": "Once per long rest, cast a spell as though originating from a reflective surface you can see within 60 feet. Range and line of effect are measured from that surface.",
  "type": "Magic",
  "legacyEffect": "Cast spell from reflection (once per day)",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define a real visible reflective surface within60ft, selecting the origin at cast time, its space/size, range/line/sight requirements, Self/Touch/cones, hostile-held surfaces, moving/destroyed mirrors and ongoing effects. Preserve caster ownership, actions, components, RP and Long Rest use; no duplicate caster or remote senses.

</details>

## MX-23 — Mystic Focus

Identity: `mystic_focus`. Original prerequisite: **Level 6**.

**Original effect, unchanged**

Gain +1 to spell attack rolls and to checks made to overcome magical resistance.

**Proposed operating procedure**

At character level 6, NEW choose active+1 rather than legacy/description+2 penetration. Gain+1 on actual spell attack rolls and actual checks explicitly required to overcome magical resistance. Current strongest same-stat bonuses apply. No generic resistance check exists: ordinary damage resistance still halves its eligible damage and spell resistance that grants save advantage is not a caster check. Apply the second branch only to an operative source’s real test. This is not Spell Focus, supplies no saveDCbonus, spell access, damage increase or extra Counterspell/Dispel check. A Counterspell check is interruption, not overcoming magical resistance unless its exact source separately establishes that predicate.

**Explicit NEW choices:** Active+1 and actual-test predicate preserve both clauses without inventing penetration stats.

**Authored adjudications**

- A legal spell attack+6 becomes+7 if no stronger applicable flat bonus replaces it.

- A creature with fire resistance retains that resistance; there is no new+1 penetration roll.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "mystic_focus",
  "name": "Mystic Focus",
  "description": "At level 6, focused spellwork receives the feat's listed +2 spell penetration.",
  "prerequisite": "Level 6",
  "effect": "Gain +1 to spell attack rolls and to checks made to overcome magical resistance.",
  "type": "Magic",
  "legacyEffect": "+2 spell penetration",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve active+1 spell attacks and checks versus description/legacy+2 spell penetration. Define actual magical-resistance checks from sourced mechanics and stacking with Spell Penetration. No invented resistance statistic, Spell Focus identity or universal spell-save-DC bonus.

</details>

## MX-24 — Mystic Recoil

Identity: `mystic_recoil`. Original prerequisite: **Level 7**.

**Original effect, unchanged**

Once per short rest, when a spell you cast is countered or all its targets succeed on their saves, gain one additional bonus action on your next turn. This bonus action cannot cast a ranked spell.

**Proposed operating procedure**

Once SR/LR after your own actual spell is countered, or after every originally legal recipient of its initial save-based payload actually succeeds on every required initial save, optionally commit the use and queue one extra BA for your next future regular turn. NEW require at least one actual initial save and all original recipients resolved legally; a no-save, mixed attack/save or lost-target cast cannot qualify by vacuous success. An automatic successful save counts where a real save was called for. No copying/echoing or each-tick retrigger. The BA becomes available on that one regular turn, even if other BA is spent, and expires unused at its end; incapacity creates no makeup. It may perform an actually acquired legal BA, including ordinary command, but cannot prepare/cast a ranked spell or create more actions/banked allowances. It does not bypass shared companion offense, concentration, RP or other use caps. No extra fullAction, Reaction or duration-clock tick.

**Explicit NEW choices:** One queued regular-turn BA and explicit all-initial-target success predicate.

**Authored adjudications**

- Both targets succeed on the spell’s only two initial saves: next regular turn gains one restricted BA.

- One target failed but was immune to damage: the all-success branch does not trigger.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "mystic_recoil",
  "name": "Mystic Recoil",
  "description": "When a spell fails at level 7, mystic recoil leaves you ready to take the feat's listed extra action next turn.",
  "prerequisite": "Level 7",
  "effect": "Once per short rest, when a spell you cast is countered or all its targets succeed on their saves, gain one additional bonus action on your next turn. This bonus action cannot cast a ranked spell.",
  "type": "Magic",
  "legacyEffect": "If spell fails, gain +1 action next turn",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define countered versus all targets succeed, including no-save/mixed-target/automatic-success spells and invalid targets. Specify use declaration, next regular turn extra Bonus Action, expiration and restrictions on ranked spells/commands. Preserve once per Short Rest and prevent repeated failure/echo events from generating extra actions.

</details>

## MX-25 — Overchannel

Identity: `overchannel`. Original prerequisite: **Level 10**.

**Original effect, unchanged**

Once per long rest, add one additional damage die per spell tier to a damaging spell. After it resolves, take force damage equal to twice the spell tier; this damage cannot be reduced.

**Proposed operating procedure**

Once LR at damaging spell declaration, add one existing native damage die per actual spell rank to one immediate native packet under the shared added-die rule. NEW choose this active rule over legacy 25%. Commit use with the cast. After its immediate attempted resolution, including a miss, all saves or Counterspell, take 2×rank force backlash as one self-damage event. This damage cannot be reduced or redirected; NEW it does pass through real temp HP before normal HP, unlike the explicitly proposed normal HP-funded blood costs. Resolve ordinary Wound/death/concentration consequences and no incidental reflection/resource/lifesteal triggers from this self-authored cost. It requires noHPprepayment and can kill the caster. A readied cast takes backlash after preparation/interruption, not after eventual release; its added dice attach once to the eventual immediate payload. Rank 0 legally adds 0 dice and 0 damage but still spends the use if chosen. Flat-only/no-native-die spells are ineligible.

**Explicit NEW choices:** One native packet, post-attempt backlash including counters, and explicit temp HP-compatible damage rather than HP funding.

**Authored adjudications**

- Rank 3 native 4d6 becomes 7d6 in the selected shared area roll, followed by 6 unreducible force backlash.

- If Counterspell negates that spell, the committedLRuse and 6 backlash still occur.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "overchannel",
  "name": "Overchannel",
  "description": "At level 10, an overchanneled spell takes the listed backlash to boost its damage by 25%.",
  "prerequisite": "Level 10",
  "effect": "Once per long rest, add one additional damage die per spell tier to a damaging spell. After it resolves, take force damage equal to twice the spell tier; this damage cannot be reduced.",
  "type": "Magic",
  "legacyEffect": "Boost spell damage by 25%, take backlash",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Use active one extra damage die per spell tier and2xTier force backlash after resolution, not legacy25percent. Specify dice type/packets/targets/critical interactions, rank0, miss/no damage/counterspell, concentration and zeroHP. Preserve unreducible backlash and Long Rest use without manufacturing healing or refund loops.

</details>

## MX-26 — Planar Knowledge

Identity: `planar_knowledge`. Original prerequisite: **Intelligence 14+**.

**Original effect, unchanged**

As a bonus action, make an Arcana check against DC 10 + the creature’s challenge rating. On a success, learn one resistance, immunity, vulnerability, or planar trait. Once per creature.

**Proposed operating procedure**

Once per actual creature identity, as a Bonus Action examine one creature you can perceive within 60 ft and line of effect. NEW commit the per-creature attempt before rolling INT(Arcana) against DC 10+its actual printedCR, rounding the finalDCdown by current fraction rules. If noCR is assigned, Director must establish the encounter’s rating before attempts; absence is notCR 0 and an unsupported target is ineligible without spending. Success lets the Director truthfully disclose one existing damage resistance, immunity, vulnerability or explicitly established planar-trait fact; you may name a category, but no nonexistent fact is invented. If that category has none, report that absence only, not all other hidden data. Failure gives no fact and no retry through alias/form/encounter reset. Existing source disguises/protected information still apply. Planar traits requiring the deferred cosmology review remain unasserted; other recorded defenses are still usable.

**Explicit NEW choices:** 60 ft examination, once-attempt identity and actualCR/one-fact disclosure without new ontology.

**Authored adjudications**

- CR 1/2 gives DC 10 after rounding; success can reveal one actual cold resistance.

- An unrated story entity is not automatically DC 10, and success cannot invent its planar origin.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "planar_knowledge",
  "name": "Planar Knowledge",
  "description": "Intelligence 14+ supports recognizing an enemy's resistances in the middle of a fight.",
  "prerequisite": "Intelligence 14+",
  "effect": "As a bonus action, make an Arcana check against DC 10 + the creature’s challenge rating. On a success, learn one resistance, immunity, vulnerability, or planar trait. Once per creature.",
  "type": "Magic",
  "legacyEffect": "Know enemy resistances mid-fight",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define Bonus Action range/senses, actual creature CR including fractional/missing values, DC10+CR rounding, choosing one existing fact, retries and once-per-creature identity. Read actual resistance/immunity/vulnerability records; planar-trait content remains deferred where cosmology would be required. No invented trait or origin.

</details>

## MX-27 — Protective Casting

Identity: `protective_casting`. Original prerequisite: **Level 6**.

**Original effect, unchanged**

After casting a ranked spell, gain +1 AC until the start of your next turn.

**Proposed operating procedure**

At character level 6, after a completed personal ranked cast gain+1 AC until your next future regular start. NEW select active+1/regular-start over preserved 10%/5 seconds. It begins after the cast’s immediate resolution or successful Ready preparation, so does not protect against that cast’s earlier interruption attacks. Miss/all-save still qualify; a countered cast does not. Repeated legal casts refresh one same-family record without stacking magnitude; current strongest same-statACbonus applies with other sources. Ready release does not grant again. Incapacity does not itself end this nonconcentration buff; ordinary expiry/source-suppression does. No additional armor, resistance, spell use or cast trigger from copies.

**Explicit NEW choices:** Completed-cast timing, one nonstacking+1 record and original regular-start expiry.

**Authored adjudications**

- A saved-against rank 2 spell still grants+1 AC after resolution.

- Two ranked casts create one+1 record; a reaction attack during the first cast resolves before it begins.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "protective_casting",
  "name": "Protective Casting",
  "description": "At level 6, casting grants the listed +10% AC for 5 seconds.",
  "prerequisite": "Level 6",
  "effect": "After casting a ranked spell, gain +1 AC until the start of your next turn.",
  "type": "Magic",
  "legacyEffect": "+10% AC for 5s after casting",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Use+1 AC until next regular start after a real ranked cast, not legacy10percent/5seconds. Define successful versus interrupted/countered casting, repeated nonstacking applications and combination with Arcane Armor/other AC families. No retroactive protection for the triggering cast unless explicitly decided.

</details>

## MX-28 — Quick Ritualist

Identity: `quick_ritualist`. Original prerequisite: **Wisdom 14+**.

**Original effect, unchanged**

Halve the additional casting time required to cast a spell as a ritual, to a minimum of 5 minutes.

**Proposed operating procedure**

For a spell you can actually cast through a legal ritual route, halve only the route’s additional ritual time, with resulting additional time at least 5 minutes; retain the base printed casting time in full. NEW measure the result in elapsed seconds and round up to the next whole second so fractions never shorten a required interval. An original 10 minute addition becomes 5 minutes, not half the whole cast. An original shorter addition is not increased: use min(original additional time, max(300, ceil(original/2))). This explicit non-worsening interpretation preserves the minimum for reductions without penalizing a preexisting faster route. Components, formula/repertoire, costs, concentration, helpers and interruptions remain. It grants no Ritual tag or access; the separate proposed Ritual Caster overlay needs its own approval. Apply this additional-time change before any separately legal group active-time adjustment, whose minimum rule remains.

**Explicit NEW choices:** Additional-time-only arithmetic, no worsening of already-shorter routes and second rounding.

**Authored adjudications**

- A 1 Action base plus 10 minutes ritual addition becomes the same 1 Action base plus 5 minutes.

- A source’s 2 minute special addition stays 2 minutes, and this feat creates no ritual permission.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "quick_ritualist",
  "name": "Quick Ritualist",
  "description": "Wisdom 14+ supports halving the listed ritual casting time.",
  "prerequisite": "Wisdom 14+",
  "effect": "Halve the additional casting time required to cast a spell as a ritual, to a minimum of 5 minutes.",
  "type": "Magic",
  "legacyEffect": "Ritual casting time halved",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Apply half to additional ritual casting time only, minimum5minutes; preserve base casting time and exact rounding. Bind actual ritual access, long rituals, interruption and other reductions. Ritual Caster/Ritual Channeler are pending dependencies, not automatic access or multiplicative approvals.

</details>

## MX-29 — Ritual Channeler

Identity: `ritual_channeler`. Original prerequisite: **Intelligence 14+**.

**Original effect, unchanged**

When participating in a group ritual, reduce its required active casting time by 25 percent and count as two ordinary assistants.

**Proposed operating procedure**

NEW a group ritual is one actual legally available ritual spell with a designated lead and at least one physically present willing assistant continuously performing that same ritual’s active work; it is not simultaneous crafting, travel or independent casts. Use the exact source’s assistant qualifications/cap. If it supplies none, the proposed default assistant must know that ritual or have proficiency in the lead’s actual relevant Arcana/Religion/Nature skill; count at most two ordinary assistant contributions, with no numeric roll bonus when the source has no assistant benefit. This feat-holder contributes as two ordinary assistants within that cap, never as two leads or two physical bodies for a separate location requirement. One or more holders reduce the group’s total active casting time once by 25%, rounding up seconds; passive waiting is unchanged. Apply after Quick Ritualist’s additional-time reduction, but never reduce that remaining additional ritual portion below 5 minutes unless it was already shorter. Source-required simultaneous people, costs, lead concentration, interruptions and minimum times remain. No multiplicative 25%stack or free spell/resource. NEW the double-assistant contribution applies only while actually serving as an assistant. A lead who owns this feat can supply the time reduction but cannot simultaneously count as two assistants; one person never performs both assigned jobs at once.

**Explicit NEW choices:** Finite default group/assistant procedure and single 25%time reduction with preserved minimums.

**Authored adjudications**

- A 20 minute fully active ritual with no stronger minimum takes 15 minutes with one qualified Channeler.

- Two Channelers do not halve that time again and cannot replace two required bodies at distant ritual stations.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "ritual_channeler",
  "name": "Ritual Channeler",
  "description": "Intelligence 14+ supports the listed 25% faster group rituals.",
  "prerequisite": "Intelligence 14+",
  "effect": "When participating in a group ritual, reduce its required active casting time by 25 percent and count as two ordinary assistants.",
  "type": "Magic",
  "legacyEffect": "Group rituals 25% faster",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define a real group ritual and ordinary assistant procedure before applying25percent active-time reduction and two-assistant contribution. Specify assistant caps, multiple feat users, overlapping work, base versus additional time, rounding, interruptions and material/formula costs. Do not silently treat every crafting work order as a ritual.

</details>

## MX-30 — Runic Shield

Identity: `runic_shield`. Original prerequisite: **Wisdom 14+**.

**Original effect, unchanged**

At the start of combat, gain a runic ward with 15 hit points. The ward absorbs spell damage first and vanishes when depleted. It refreshes after a short rest.

**Proposed operating procedure**

NEW select 15 ward HP over preserved 50. The feat has one armed grant per beneficial SR/LR; acquisition arms it. At the first real encounter start after arming, automatically create one personal runic ward with 15 points and spend that entitlement, even if surprised/incapacitated; a dead creature receives none. It persists between encounters until depleted or the next beneficial SR/LR, when any old ward ends and entitlement rearms for the next combat, not immediate refill in combat. Repeated initiative does not refill it. This is a distinct spell-only ward, not temp HP: after ordinary defenses and before temp HP, intercept up to its remaining points of actual incoming spell damage in stable component order. Nonspell damage bypasses it. Record ward absorption separately, excluded from actual damage received by the body, Wound/death thresholds and concentration checks; any surviving packet resolves once normally. No transfer, double ledger, HP healing, return on revival or resource proc from ward absorption. Counterspell/dispel cannot target this nonspell passive ward without explicit applicable source permission.

**Explicit NEW choices:** Separate 15 point spell-only pre-temp ward, one armed combat grant per rest and no encounter refills.

**Authored adjudications**

- A post-defense 20 spell-damage packet consumes 15 ward then passes 5 to temp HP/normal HP.

- A sword’s 8 nonspell damage ignores the ward entirely; starting another encounter does not restore spent ward points.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "runic_shield",
  "name": "Runic Shield",
  "description": "Wisdom 14+ supports the listed absorption of the first 50 spell damage per combat.",
  "prerequisite": "Wisdom 14+",
  "effect": "At the start of combat, gain a runic ward with 15 hit points. The ward absorbs spell damage first and vanishes when depleted. It refreshes after a short rest.",
  "type": "Magic",
  "legacyEffect": "Absorbs first 50 spell damage per combat",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve description50 versus active15 ward HP and start-of-combat versus Short Rest refresh. Define ward versus temporary HP, one physical owner/source identity, spell-only damage interception order, damage event and concentration/Wound thresholds, depletion, encounter farming and transfer. Preserve both activation and recovery clauses explicitly.

</details>

## MX-31 — Silent Casting

Identity: `silent_casting`. Original prerequisite: **Level 7**.

**Original effect, unchanged**

You may cast a spell without its verbal component by increasing its RP cost by 1. This cannot bypass components with a stated magical command word.

**Proposed operating procedure**

At declaration of a spell actually requiringV, remove only that verbal component by adding 1 actual RP to its price before ordinary final cost adjustments. NEW the independent 1 RP payment cannot itself be waived by a charged/free normal-rank route; an actualRPpool and sufficient final payment are required. Rank 0 can use the feat and still pays the independent surcharge; cantrip strain rules remain. A component or exact activation explicitly demanding a magical command word cannot be removed. Ordinary audibleV alone is not a protected command word unless identified as such by the operative source. PreserveS, F/materials, physical access and action permissions. Silence no longer blocks the removedV, but Incapacitated/other restrictions remain. It creates neither undetectable casting nor automatic concealment; other visible components/effects and observers’ real senses still determine interruption eligibility.

**Explicit NEW choices:** Only explicitV removal with real independentRPprice and exact command-word exclusion.

**Authored adjudications**

- A V, S cantrip may be cast silently with S and 1 real RP, provided every other permission holds.

- A charged spell cast by someone with noRPpool cannot pay the extra 1 RP through its charge.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "silent_casting",
  "name": "Silent Casting",
  "description": "Level 7 supports the listed casting without a verbal component.",
  "prerequisite": "Level 7",
  "effect": "You may cast a spell without its verbal component by increasing its RP cost by 1. This cannot bypass components with a stated magical command word.",
  "type": "Magic",
  "legacyEffect": "Cast without verbal component",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define+1 RP surcharge for removing V at declaration, price ordering, rank0 and charge-only casts without an RP interface/pool. Preserve command-word exclusion and S/material requirements; identify what a stated magical command word means from actual spell text. No universal undetectable casting.

</details>

## MX-32 — Spell Deflection

Identity: `spell_deflection`. Original prerequisite: **Intelligence 16+**.

**Original effect, unchanged**

Once per long rest, when targeted by a single-target hostile spell, roll a d20. On 16 or higher, redirect it to another legal target within its original range; otherwise gain advantage on the saving throw.

**Proposed operating procedure**

Once LR, NEW spend a Reaction when a hostile pending spell has selected you as its sole creature target, after ordinary cast interruptions but before its attack/save/effect resolution. It must be an actual single-target payload, not one target remaining from an area or multi-target mode. Roll an unmodifiedd 20;16–20 redirects, preserving this explicit 25%procedure over legacy 10%. On success choose a different legal creature under the original spell’s actual target restrictions, range/line measured from the original origin, personally perceived by you where necessary; the original caster remains owner and supplies all stats/choices. Recheck legality, then use fresh original attack/save procedure against that new target; nothing resolves against you. If no legal new target exists, or on 1–15, the spell continues against you with advantage on each actual initial save it requires; no save is invented for an attack/automatic spell. Use/Reaction remain spent. A redirected/reflected/copy packet cannot be redirected again by this family or Spell Reflection. Protected/self-only/source-specific exclusions remain.

**Explicit NEW choices:** Reaction window, d20 threshold, no-target fallback and shared redirect-once provenance.

**Authored adjudications**

- Roll 17 redirects an eligible hostile ray to another legal creature within the original caster’s range.

- Roll 9 against an attack spell grants no save orACbonus; the original attack proceeds normally.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "spell_deflection",
  "name": "Spell Deflection",
  "description": "Intelligence 16+ supports the listed 10% chance to redirect hostile spell.",
  "prerequisite": "Intelligence 16+",
  "effect": "Once per long rest, when targeted by a single-target hostile spell, roll a d20. On 16 or higher, redirect it to another legal target within its original range; otherwise gain advantage on the saving throw.",
  "type": "Magic",
  "legacyEffect": "10% chance to redirect hostile spell",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Use actual d20≥16, not legacy10percent. Define optional Long Rest declaration, action/Reaction, hostile single-target spell, legal new target from original origin, save/attack handling and no-legal-target outcome. Preserve fallback advantage, prevent reflection recursion and distinguish redirects from new casts.

</details>

## MX-33 — Spell Reservoir

Identity: `spell_reservoir`. Original prerequisite: **Intelligence 14+**.

**Original effect, unchanged**

Once per long rest after finishing a short rest, recover RP equal to your proficiency bonus.

**Proposed operating procedure**

Once LR, immediately after completing a beneficial SR and its ordinary recovery, optionally restore currentPBactual RP capped by remaining merged-pool headroom. Commit theLRuse and that actual rest-event claim together; another listener, duplicate receipt or resumed rest completion cannot claim again. If no headroom, you may decline without spending, but cannot bank that past rest’s trigger for later; a later beneficial SR can supply a new opportunity while theLRuse remains. It creates no maximumRPincrease, charge, slot, second classpool or independent Retune. A long rest alone does not count as the printedSRtrigger. PB changes before a future legal use affect that use’s amount but never refresh spent entitlement.

**Explicit NEW choices:** Post-normalSRrecovery timing and no banked completion claim.

**Authored adjudications**

- PB 4 with 2 RP missing after normalSRrecovery restores 2 and spends theLRuse.

- At full RP you may decline; spending RP later does not reopen that already-finished rest.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "spell_reservoir",
  "name": "Spell Reservoir",
  "description": "Intelligence 14+ supports the listed gain of 1 additional ranked-spell recovery per day.",
  "prerequisite": "Intelligence 14+",
  "effect": "Once per long rest after finishing a short rest, recover RP equal to your proficiency bonus.",
  "type": "Magic",
  "legacyEffect": "Gain 1 additional spell slot per day",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Specify completion of an actual Short Rest within one Long Rest use ledger, PB amount, RP cap and timing with ordinary rest recovery. No new spell slot, maximum RP increase, charge conversion or repeated claim from one rest event; source description and old slot wording stay separately preserved.

</details>

## MX-34 — Spellweave

Identity: `spellweave`. Original prerequisite: **Wisdom 14+**.

**Original effect, unchanged**

When you cast a spell that grants a minor buff, you may hold that buff until the end of your next turn and apply it to the next spell you cast instead. Only one buff may be held.

**Proposed operating procedure**

NEW use the finite three-spell minor-buff table below: personally cast Guidance, Resistance or True Strike with yourself as the otherwise legal recipient. At its completion hold that entire one-use buff instead of receiving it normally; only one held record, replacing loses the old. Original costs, cast history and earlier deadline remain, with an additional deadline at your next future regular end. The next actual spell you commit consumes/attaches the record automatically, even if countered or unsuitable; no indefinite skipping. Guidance adds its one 1d4 only to one actual ability/task check made by that next spell, declared before rolling; Resistance adds its one 1d4 only to one actual concentration save maintaining that next spell; True Strike grants advantage only on that next spell’s first actual spell attack. They create no check/save/attack. The attachment expires at the original held deadline or actual spell end, whichever first, even if unused. Current one-bonus-die/advantage rules apply. A copied buff, borrowed duplicate or another Spellweave cannot be held; no duration/resource/HP/stat transfer or new cast.

**Explicit NEW choices:** Explicit NEW whitelist and typed transfer meanings replace the undefined minor-buff promise without claiming recovered canon.

**Authored adjudications**

- Held Guidance attaches to a legal next Counterspell and can add 1d4 to its actual counter check.

- Held True Strike consumed by a next spell with no attack produces no benefit and cannot wait for a third cast.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "spellweave",
  "name": "Spellweave",
  "description": "Wisdom 14+ supports the listed stacking of minor buffs onto the next spell.",
  "prerequisite": "Wisdom 14+",
  "effect": "When you cast a spell that grants a minor buff, you may hold that buff until the end of your next turn and apply it to the next spell you cast instead. Only one buff may be held.",
  "type": "Magic",
  "legacyEffect": "Stack minor buffs onto next spell",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define a finite meaning of minor buff and eligible transfer rather than arbitrary Director improvisation. Specify original recipient/payment, one held record, expiry, concentration, next actual cast attachment and components/scaling. Preserve every source clause while preventing duplicated buffs, resources or impossible effect-type conversions.

</details>

## MX-35 — Still Casting

Identity: `still_casting`. Original prerequisite: **Level 7**.

**Original effect, unchanged**

You may cast a spell without its somatic component by increasing its RP cost by 1. This does not function while fully restrained.

**Proposed operating procedure**

At declaration of a spell requiringS, remove only that somatic component by adding 1 actual RP before final pricing; use Silent Casting’s independent-surcharge convention, including actualRPrequirement for rank 0/charged routes. NEW fully restrained means actual hands/arms physically or explicitly magically immobilized so no usable casting gesture exists; CoreRestrained alone imposes its printed penalties and does not prove that anatomy restriction. This feat expressly fails under such complete physical/explicit gesture immobilization, despite removing ordinaryS. It also supplies no Action under Incapacitated, no freedom from binding, and no hand for actualF/material manipulation. RemovingS andV with two feats pays both independent surcharges; each protected command/material requirement remains. Spell perception/counterability follows real remaining cues.

**Explicit NEW choices:** Exact physical/explicit gesture restraint boundary, avoiding invented universal CoreRestrained casting ban.

**Authored adjudications**

- A net’s actual full arm binding blocks this feat; a source’s mere Speed 0/Restrained penalty need not.

- RemovingS still leaves a required held focus that the caster must legally handle.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "still_casting",
  "name": "Still Casting",
  "description": "Level 7 supports the listed casting without somatic gestures.",
  "prerequisite": "Level 7",
  "effect": "You may cast a spell without its somatic component by increasing its RP cost by 1. This does not function while fully restrained.",
  "type": "Magic",
  "legacyEffect": "Cast without somatic gestures",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define+1 RP surcharge for removing S and actual fully-restrained boundary against current Restrained/hand rules. Specify charge-only/cantrip casts, price order, material/focus handling and V. Removing somatic gestures does not supply hands for other components or permit actions under Incapacitated.

</details>

## MX-36 — Temporal Flux

Identity: `temporal_flux`. Original prerequisite: **Level 8**.

**Original effect, unchanged**

When a creature fails a save against one of your time-tagged spells, reduce its speed by 10 feet and prevent reactions until the start of its next turn.

**Proposed operating procedure**

At character level 8, when a creature fails an actual save against your personally cast time-tagged spell, apply one softSpeed−10 ft record and one no-new-Reactions component until its next future regular start. NEW finite feat-tag overlay: Slow’s two actual modes, Haste and Future Echo only; current source tags do not supply an explicitTime tag. Their full current spell procedures remain unchanged, and a save-less buff creates no trigger. Wider tags require separate review; spell names or narrative time flavor alone do not qualify. Speed records compete under current strongest-adverse-control arithmetic rather than add;0 floor, real modes and existing movement spent remain. Already committed Reactions finish. Same owner/target/profile refreshes one record without extra magnitude; different sources retain their real deadlines. No new save, hardActiondenial, extra turn, state restoration or enabledTime Loop.

**Explicit NEW choices:** Explicit NEW three-identity tag overlay and exact target-start soft-control expiry.

**Authored adjudications**

- A failed Slow save on Speed 30 already produces halfSpeed 15; Flux−10 competes as 20, so effectiveSpeed stays 15.

- Haste ordinarily has no recipient save, so its new feat tag alone does not trigger Flux.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "temporal_flux",
  "name": "Temporal Flux",
  "description": "Level 8 supports the listed slowing of enemies hit by time spells.",
  "prerequisite": "Level 8",
  "effect": "When a creature fails a save against one of your time-tagged spells, reduce its speed by 10 feet and prevent reactions until the start of its next turn.",
  "type": "Magic",
  "legacyEffect": "Slow all enemies hit by time spells",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Identify exact time-tagged spell authority and failed-save trigger. Bind−10ft Speed with current strongest/stacking floors and no-Reaction component until target next regular start, repeated/multiple-source effects and cure/suppression. No legacy all-hits trigger or enabling unfinished Time Loop.

</details>

## MX-37 — Twin Cast

Identity: `twin_cast`. Original prerequisite: **Level 8**.

**Original effect, unchanged**

Once per long rest, after casting a single-target spell of Tier 1–3, target a second legal creature within range without paying additional RP.

**Proposed operating procedure**

Once LR after a personal rank 1–3 single-creature spell completes its initial payload, choose one additional different creature currently legal under that same mode, range, sight, line of effect and willingness/type restrictions. NEW only an originally exactly-one-creature payload qualifies; no area, multi-ray/multi-target, Self-only, summon/object creation, resource/action-grant, resurrection, maximumHPchange or copied payload. Consume the feat use and extend that same cast’s original immediate damage/heal/condition/buff to the second recipient. Roll a fresh actual attack/save and native dice for that recipient; no newRPprice, cast, components, Dissonance/Refrain or class/featproc. Independent per-recipient material/HP/finite reserve requirements remain actual costs and must be affordable before choosing. One concentration ID governs both; original deadline and source target-ending rules remain. This is an explicit two-target exception only for this cast, not another spell identity or separate duration. Preserve old 5%autodouble wording as inactive alternative.

**Explicit NEW choices:** One bounded additional original-payload recipient under one cast/concentration, with explicit nonduplicable categories.

**Authored adjudications**

- A legal rank 1 one-creature damage spell resolves anew against one second eligible creature without another baseRPcost.

- A spell already selecting up to two creatures cannot qualify merely because the caster chose only one.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "twin_cast",
  "name": "Twin Cast",
  "description": "Level 8 supports the listed 5% chance to auto-cast a spell twice.",
  "prerequisite": "Level 8",
  "effect": "Once per long rest, after casting a single-target spell of Tier 1–3, target a second legal creature within range without paying additional RP.",
  "type": "Magic",
  "legacyEffect": "5% chance to auto-cast spell twice",
  "status": "provisional-complete",
  "balanceReview": true,
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Use once-per-Long-Rest second legal creature after a Tier1–3 single-target cast, not legacy5percent double cast. Define attack/save results, concentration, components, range/sight recheck, origin, already-multitarget/upcast spells and one source identity. No duplicate refund, extra summon or copied paid resource.

</details>

## MX-38 — Arcane Adaptation

Identity: `arcane_adaptation`. Original prerequisite: **Spellcasting ability, Intelligence 13+**.

**Original effect, unchanged**

When you successfully reflect or copy a spell or supernatural ability, you gain resistance to that damage type until the end of your next turn. Once per short rest, you may treat a copied effect as if you had always known it for 2 rounds.

**Proposed operating procedure**

After an actual successful legal reflection or capture of a spell/supernatural effect through a separately owned source, gain resistance to the one real damage type expressed by its selected copied/reflected component until your next future regular end. NEW choose one observed type for a mixed packet; nondamaging effects grant no damage resistance. It begins after capture/redirect, does not retroactively mitigate earlier damage, and grants no copying permission by itself. Once SR/LR at that event, also mark the one legal captured profile as temporarily known through your second future regular start. During that interval you may activate that exact bounded profile using its actual action, RP, components, rank ceiling and concentration, even if its original one-use record was consumed; no other original spell/monster ability is learned. Each activation is a copy retaining the original no-proc/no-copy/resource flags and the shared one-copy-release/round cap below. Existing Mirrorsage records retain their actual release costs/caps and printed bounded profile. No restoration of archive slots or legacy boss power. Expiry removes permission but not legitimately established effects before their own deadlines.

**Explicit NEW choices:** One observed damage type and finite temporary known-profile route with paid repeat activations, no permanent repertoire.

**Authored adjudications**

- Capturing a fire Strike grants fire resistance through next end; adapting it permits paid bounded releases within two regular-start intervals.

- Copying a harmless warning reveals no damage type and grants no invented resistance.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "arcane_adaptation",
  "name": "Arcane Adaptation",
  "description": "Your magic bends to mirror what strikes you, letting you reshape your defenses after every reflected blow. Prestige lineage: Echomancer. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, Intelligence 13+",
  "effect": "When you successfully reflect or copy a spell or supernatural ability, you gain resistance to that damage type until the end of your next turn. Once per short rest, you may treat a copied effect as if you had always known it for 2 rounds.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you successfully reflect or copy a spell or supernatural ability, you gain resistance to that damage type until the end of your next turn. Once per short rest, you may treat a copied effect as if you had always known it for 2 rounds.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define actual successful reflection/copy event, which real damage type(s) grant resistance and end-of-next-turn duration. Separately bind Short Rest treat-as-known effect for2rounds: permitted repertoire/rank/costs/actions/copy profile. No permanent learning, boss/legendary access, recursive copying or borrowing of Mirrorsage class eligibility.

</details>

## MX-39 — Arcane Calculus

Identity: `arcane_calculus`. Original prerequisite: **Intelligence 15+, proficiency in Arcana**.

**Original effect, unchanged**

You gain +2 to initiative while concentrating on a spell. Once per short rest, you may store one prepared spell's timing: cast it on a later turn without using an action, as if you had readied it mathematically. When you cast a stored spell this way, one creature of your choice within 30 feet must succeed on a Dexterity save or take force damage equal to your spellcasting modifier (minimum 1).

**Proposed operating procedure**

Gain+2 to an actual initiative roll only while concentrating on a spell when that roll occurs; losing concentration later does not rewrite initiative. Once SR/LR use an Action to prepare one currently legally prepared normalActionspell through the exact Ready casting procedure, paying costs/components/history and opening interruption at preparation. NEW it shares the one pendingReady slot and concentration requirement, but its hold lasts through your next future regular end, and release is a voluntary non-action on that next regular turn only. Choose/recheck original legal targets then; no Reaction or second cast. Expiry, replacement or lostconcentration wastes paid costs. On successful release, choose one perceived creature within 30 ft of your body and line of effect:DEX save against the stored cast’s actual DC or take force equal to max(1, its actual casting modifier snapshotted at preparation),0 on success. One immediate noncopyable feat rider, no added release/action/castproc. Readied spells lacking a preparation route remain ineligible; the feat grants no preparation list.

**Explicit NEW choices:** Action/cost-paid extendedReady with next-regular-turn free release and one finite DC-bound rider.

**Authored adjudications**

- Prepare a legal spell now, then release next regular turn without spendingAction; one nearby creature may face the separateDEXsave.

- A Counterspell at preparation prevents storage and the later rider; there is no second Counterspell window at release.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "arcane_calculus",
  "name": "Arcane Calculus",
  "description": "You solve combat like an equation—measuring intervals, vectors, and the precise moment a spell must land. Prestige lineage: Chronomancer. completed from the existing development record.)",
  "prerequisite": "Intelligence 15+, proficiency in Arcana",
  "effect": "You gain +2 to initiative while concentrating on a spell. Once per short rest, you may store one prepared spell's timing: cast it on a later turn without using an action, as if you had readied it mathematically. When you cast a stored spell this way, one creature of your choice within 30 feet must succeed on a Dexterity save or take force damage equal to your spellcasting modifier (minimum 1).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You gain +2 to initiative while concentrating on a spell. Once per short rest, you may store one prepared spell's timing: cast it on a later turn without using an action, as if you had readied it mathematically. When you cast a stored spell this way, one creature of your choice within 30 feet must succeed on a Dexterity save or take force damage equal to your spellcasting modifier (minimum 1).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind+2 initiative only while actually concentrating, timing of the check and later loss. Define storing one prepared spell, setup action/RP/components/concentration, lifetime, free release on a later turn, counterability and legal targets. Define the separate30ft Dexterity-save force rider/DC/one spellcasting modifier and no action-generation loop.

</details>

## MX-40 — Arcane Momentum

Identity: `arcane_momentum`. Original prerequisite: **Power Attack or Combat Casting, spellcasting ability**.

**Original effect, unchanged**

When you hit with a melee weapon attack, gain 1 Momentum stack (max 3). Spend 1 stack to reduce the casting time of your next spell by one step, or spend all stacks to add +10% force damage per stack to a spell you cast before the end of your turn.

**Proposed operating procedure**

Require actual Power Attack OR Combat Casting plus actual spellcasting ability. NEW each personal direct melee-weapon hit against meaningful opposition gives one featMomentum, max 3, with a once-per-attack identity and no gain from copies/companions/retaliation. This separate pool starts 0, ends at encounter end or one minute without a qualifying hostile hit; no alias to any class Momentum. At spell declaration choose ONE mode. Spend 1 to shorten a printed normalActionspell to BA; no other casting time has a shorter step in this explicit finite ladder, so no BA-to-free, Reaction-to-Action or ritual compression. OR spend all current 1–3 stacks to add floor(native immediate damage×stacks/10) as force to one selected native packet/shared area roll before this actual turn ends, after native critical/flat formula but before defenses. It adds damage rather than converts the original type, and does not compound other percentage bonuses. No damage means 0, no future periodic/ray replication; a miss/counter wastes stacks. Cannot combine both modes on one cast or bank the declared enhancement for a later turn.

**Explicit NEW choices:** Distinct finite pool/lifetime, singleAction-to BA ladder and one pre-defense additiveforce component.

**Authored adjudications**

- Native 19 damage with 3 stacks adds 5 force; native damage keeps its original type.

- A printedBAspell cannot be made free by spending a stack.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "arcane_momentum",
  "name": "Arcane Momentum",
  "description": "Each sword stroke feeds your spellcraft. In Aethel's battlefields, steel and sigil are one rhythm. Prestige lineage: Battlemage. completed from the existing development record.)",
  "prerequisite": "Power Attack or Combat Casting, spellcasting ability",
  "effect": "When you hit with a melee weapon attack, gain 1 Momentum stack (max 3). Spend 1 stack to reduce the casting time of your next spell by one step, or spend all stacks to add +10% force damage per stack to a spell you cast before the end of your turn.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you hit with a melee weapon attack, gain 1 Momentum stack (max 3). Spend 1 stack to reduce the casting time of your next spell by one step, or spend all stacks to add +10% force damage per stack to a spell you cast before the end of your turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve actual Power Attack OR Combat Casting prerequisites. Define melee-hit stack gain, maximum3, lifetime/reset, per-hit cadence and one-step casting-time ladder. Separately define spending all stacks for+10percent force damage per stack: base, packet/area/critical rounding, duration and whether damage is added or converted. No arbitrary free cast or imported class Momentum pool.

</details>

## MX-41 — Conjure Flora

Identity: `conjure_flora`. Original prerequisite: **Spellcasting ability, proficiency in Nature**.

**Original effect, unchanged**

Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).

**Proposed operating procedure**

Once per beneficial SR/LR use an Action to create one of the three complete NEW seedling profiles below on visible supported ground within 30 ft and line of effect. It lasts one minute on original source-start markers, needs no concentration, and is a magical nonspell conjured body. Capacity is 1, or 2 at total level 10. NEW to make the second-capacity clause usable, at level 10 this same committed use permits one additional Action before the first plant expires to create one second plant; no second rest use, no later replacement of that spent creation. This is an explicit proposed addition to the printed one-seedling creation, not a recovered rule. Each plant gets its own minute. Choose its mode/burst type at creation. One BA may command all active plants within 60 ft able to perceive you, but produces only ONE selected mode outcome per round under the shared offensive-companion allowance. Lash chooses one creature within 10 ft of any participating plant for 1d6 piercing, DEX save half. Spore and entangle use their full profiles. No autonomous turn, opportunity attacks, harvest, loot, Supply, corpse or resource-generating death. Destruction/expiry permanently consumes the body.

**Explicit NEW choices:** Explicit NEW second Action at level 10 reconciles otherwise unusable capacity with once-rest creation; full bodies/modes and one coordinated offense.

**Authored adjudications**

- Two active plants can extend where the single 1d6 lash originates; they do not produce 2d6 or two attacks.

- At level 10, a second Action during the first plant’s lifetime can consume the one proposed additional-creation entitlement; it does not allow repeated replacement plants.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "conjure_flora",
  "name": "Conjure Flora",
  "description": "Seeds answer your call, rooting as guardians, lashing as spears, blooming as verdict. Prestige lineage: Verdant Animist. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, proficiency in Nature",
  "effect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Once per short rest, you conjure one immobile plant spirit (seedling) within 30 feet for 1 minute. It can lash for thorn damage, release spores, or entangle a 10-foot square. You may maintain one additional seedling at level 10+. As a bonus action, you may command all active seedlings to lash one creature within 10 feet of any seedling for 1d6 piercing damage (save for half).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve lash, spores and10ft-square entangle modes, one seedling/second atlevel10 and all-seedling Bonus Action command. Define creation action, separate Short Rest use and capacity, one-minute expiry, HP/AC/size/placement, each mode stats/save/DC, targets and shared damage-command cap. No unbounded seed, loot, independent turn or cosmology inference from plant spirit.

</details>

## MX-42 — Curse Channeling

Identity: `curse_channeling`. Original prerequisite: **Spellcasting ability or proficiency in Arcana, level 6+**.

**Original effect, unchanged**

When you hit a creature with a weapon attack, you can apply a Hex Mark. Marked creatures take +1d6 necrotic damage the next time they are hit before the start of your next turn. You can maintain one mark at a time; at level 10+, two. When a marked creature drops to 0 hit points, you regain 1d6 hit points or gain advantage on your next attack before the end of your next turn (your choice).

**Proposed operating procedure**

Require character 6 plus actual spellcasting OR Arcana proficiency. After a personal direct weapon hit, optionally place oneHexMark on that creature; the triggering hit cannot consume it. Capacity 1, or 2 at total 10; new beyond cap replaces oldest. Each record expires at your next future regular start and has two distinct one-use riders. The next genuinely separate hit against that target adds 1d6 necrotic to that hit’s packet, critical-doubled if that hit truly crits, then consumes only the damage rider; attribution remains to your feat, not the attacker’s spell for proc purposes. While the record remains, the first drop from positiveHPto 0 by genuine hostile conflict lets you choose 1d6 ordinary self-healing or advantage on your next actual attack roll through next regular end. Commit that drop rider even if blocked/full HP; no floor-prevented drop, staged victims or repeated same-target cycling within the encounter. NEW one drop benefit per owner/target/encounter; healing is finite paid-feat trigger, no healing-copy/resource output or convertible excess. Mark ends early only on replacement/cure/source rule; separate source marks do not stack the same damage rider on one hit.

**Explicit NEW choices:** Two independently consumed riders preserve the later drop benefit; one target/encounter recovery boundary.

**Authored adjudications**

- An ally’s later hit spends the mark’s 1d6, but a subsequent lawful drop before expiry can still grant the one self-heal.

- Your original marking hit supplies neither its own bonus die nor a drop reward if the target was already 0 before the mark existed.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "curse_channeling",
  "name": "Curse Channeling",
  "description": "Doom flows through your blade like ink through water—every cut writes a sentence the target cannot unread. Prestige lineage: Hexblade. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability or proficiency in Arcana, level 6+",
  "effect": "When you hit a creature with a weapon attack, you can apply a Hex Mark. Marked creatures take +1d6 necrotic damage the next time they are hit before the start of your next turn. You can maintain one mark at a time; at level 10+, two. When a marked creature drops to 0 hit points, you regain 1d6 hit points or gain advantage on your next attack before the end of your next turn (your choice).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you hit a creature with a weapon attack, you can apply a Hex Mark. Marked creatures take +1d6 necrotic damage the next time they are hit before the start of your next turn. You can maintain one mark at a time; at level 10+, two. When a marked creature drops to 0 hit points, you regain 1d6 hit points or gain advantage on your next attack before the end of your next turn (your choice).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define optional Hex Mark application on a weapon hit, one/two capacity, expiry/replacement, next-hit+1d6 ownership and whether triggering hit qualifies. Resolve next-hit consumption versus later zeroHP benefit, which marked death/zeroHP event grants1d6 healing or next-attack advantage, true-healing gates and anti-farming. Keep unrelated generic Marked condition separate.

</details>

## MX-43 — Curse Weaving

Identity: `curse_weaving`. Original prerequisite: **Spellcasting ability, Charisma 13+**.

**Original effect, unchanged**

When you cast a spell that forces a saving throw, you may weave a curse: on a failed save, the target suffers an additional escalating debuff each round (–1 to attacks, then –1 to saves, then disadvantage on concentration) until they succeed on a save at the end of their turn.

**Proposed operating procedure**

At a personal actual spell declaration that forces an initial save, select at most one original creature recipient for this NEW curse rider. Once per owner/target/numbered round, if it fails that actual initial save, establish an inflicted removablemagicalcurse with that save’s ability/DC and maximum one minute. Tier/rank for an actual rank-limited cure is the generating cast’s rank. Immediate stage 1 is−1 attack rolls; at the target’s next future regular start add stage 2−1 saves; at its following regular start add stage 3 disadvantage on actual concentration saves. Cap at 3; components accumulate within this record, not as repeated−1 stacks. At every affected regular end, including a current turn where applicable, repeat the original save; success ends the record. Original spell concentration loss/termination ends this attached curse; instantaneous spells leave its bounded independent minute. Suppression preserves stage clock and legal cures/saves without backlogged effects. Reapplication does not reset stage/extend beyond the later legal deadline or duplicate magnitude; different sources retain identity but same penalties use strongest. No forcedAction, deniedturn or hidden perpetual escalation.

**Explicit NEW choices:** One chosen recipient, explicit three-stage removablecurse and repeated actual source save with minute cap.

**Authored adjudications**

- Failing initialWISsave gives−1 attacks; next regular start adds−1 saves, then the regular-endWISsave can end both.

- A second copy of the same stage cannot create−2 attacks or a fourth escalation.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "curse_weaving",
  "name": "Curse Weaving",
  "description": "You knot malice into syllables, letting debuffs compound like threads pulled tight. Prestige lineage: Warlock. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, Charisma 13+",
  "effect": "When you cast a spell that forces a saving throw, you may weave a curse: on a failed save, the target suffers an additional escalating debuff each round (–1 to attacks, then –1 to saves, then disadvantage on concentration) until they succeed on a save at the end of their turn.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you cast a spell that forces a saving throw, you may weave a curse: on a failed save, the target suffers an additional escalating debuff each round (–1 to attacks, then –1 to saves, then disadvantage on concentration) until they succeed on a save at the end of their turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define optional curse on a failed save, eligible targets, per-cast use/cost/cadence and escalating components. Specify whether−1 attacks,−1 saves,concentration disadvantage accumulate, round/turn order, end-turn save ability/DC, maximum duration, independent spell end/cure/suppression and multiple applications. No indefinite undefined debuff ladder.

</details>

## MX-44 — Dark Affinity

Identity: `dark_affinity`. Original prerequisite: **Charisma 13+**.

**Original effect, unchanged**

You have resistance to necrotic damage, darkvision out to 60 feet (or +30 feet if you already have it), and advantage on saving throws against charm effects from undead creatures. While in dim light or darkness, you have advantage on Stealth checks and once per short rest you may step into shadow as a bonus action, teleporting up to 15 feet to an unoccupied space you can see that is also in dim light or darkness.

**Proposed operating procedure**

Gain necrotic resistance once and darkvision 60 ft, or add 30 ft to one actual independently granted darkvision range if already possessed; NEW compute from other valid sources without recursively counting this feat, reverting to 60 if that other source ends. It does not see through magicaldarkness unless separately allowed. Advantage applies to actual saves against a Charmed/explicitcharm component sourced by a creature actuallyUndead at application; no free type detection or general mind immunity. While your occupied space is actually dim/dark, gainStealthadvantage subject to ordinary hiding/perception; NEW whole footprint must qualify. Once SR/LR use BA from such a space to teleport up to 15 ft into an unoccupied fitting space you can see that is also dim/dark. No traversed path, but NEW line of effect to destination required; obey actual teleport/consent/restraint restrictions. Costs/use commit normally; no invisibility, freeHide, ancestry conversion or soul/origin claim.

**Explicit NEW choices:** Nonrecursive darkvision extension, actual light/Undead predicates and bounded legal destination.

**Authored adjudications**

- Existing 60 ftdarkvision becomes 90 ft; Darkness that defeats that sense remains opaque.

- A lit destination cannot receive the shadow step even if it is within 15 ft.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "dark_affinity",
  "name": "Dark Affinity",
  "description": "Shadow clings to you willingly. The night recognizes its own. Prestige lineage: Bloodbound. completed from the existing development record.)",
  "prerequisite": "Charisma 13+",
  "effect": "You have resistance to necrotic damage, darkvision out to 60 feet (or +30 feet if you already have it), and advantage on saving throws against charm effects from undead creatures. While in dim light or darkness, you have advantage on Stealth checks and once per short rest you may step into shadow as a bonus action, teleporting up to 15 feet to an unoccupied space you can see that is also in dim light or darkness.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You have resistance to necrotic damage, darkvision out to 60 feet (or +30 feet if you already have it), and advantage on saving throws against charm effects from undead creatures. While in dim light or darkness, you have advantage on Stealth checks and once per short rest you may step into shadow as a bonus action, teleporting up to 15 feet to an unoccupied space you can see that is also in dim light or darkness.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Retain necrotic resistance,60ft darkvision or+30ft extension, undead-charm save advantage, dim/dark Stealth advantage and15ft Bonus Action shadow teleport once per Short Rest. Define actual light/sight/space/line, legal hiding, source-undead/charm predicate and darkvision stacking. No invisibility, creature conversion or soul/origin inference.

</details>

## MX-45 — Dark Binding

Identity: `dark_binding`. Original prerequisite: **Curse Channeling or level 8+**.

**Original effect, unchanged**

You bind to one cursed weapon over a blood ritual (1 hour). While bound, the weapon cannot be disarmed against your will and deals an additional 1d4 necrotic damage on hit. If the weapon is destroyed, you take 2d10 psychic damage and cannot rebind until you complete a new ritual.

**Proposed operating procedure**

Require Curse Channeling OR character 8. Spend one uninterrupted hour in contact with one actual owned/willingly entrusted weapon carrying an established curse record; no feat-created curse, weapon or hidden curse diagnosis. NEW ritual needs your voluntary symbolic drop of blood but no numeric HP/material charge, and is unrelated to Blood Ritual. Completion replaces your old binding; interrupted work creates none and leaves the old. While personally wielding the bound original weapon, you cannot be involuntarily disarmed by an actual disarm effect; mandatory dropping from Unconscious/incapacity, loss of body/hand, voluntary release and physical destruction still apply. Each actual direct hit you make with that weapon adds 1d4 necrotic, critical-doubled normally. Thrown original weapon qualifies on its hit but does not return; ammunition launched by a bound bow qualifies as its weapon hit without becoming a bound item. No copying or companion use. Actual destruction ends the bond and causes one 2d10 psychic damage packet to you under ordinary defenses, at any distance; repair never rebinds. A fresh fullhour ritual is required for a new bond.

**Explicit NEW choices:** Actual curseditem/onehour bond, exact disarm boundary and destruction once per original identity.

**Authored adjudications**

- An enemy disarm cannot take a consciously wielded bound sword; becomingUnconscious still drops it.

- Destroying a bound thrown weapon causes one 2d10 psychic packet, with ordinary psychic resistance if present.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "dark_binding",
  "name": "Dark Binding",
  "description": "You and your cursed weapon share one hunger. Neither leaves the other's grasp easily. Prestige lineage: Hexblade. completed from the existing development record.)",
  "prerequisite": "Curse Channeling or level 8+",
  "effect": "You bind to one cursed weapon over a blood ritual (1 hour). While bound, the weapon cannot be disarmed against your will and deals an additional 1d4 necrotic damage on hit. If the weapon is destroyed, you take 2d10 psychic damage and cannot rebind until you complete a new ritual.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You bind to one cursed weapon over a blood ritual (1 hour). While bound, the weapon cannot be disarmed against your will and deals an additional 1d4 necrotic damage on hit. If the weapon is destroyed, you take 2d10 psychic damage and cannot rebind until you complete a new ritual.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve Curse Channeling OR level8 gate, one actual cursed weapon, one-hour ritual/tools/payment, rebind/unbind and original identity. Define cannot-be-disarmed versus forced dropping/incapacity, actual wielding+1d4 necrotic, thrown/ammunition/multi-hit limits and destruction2d10 psychic timing. This blood ritual is not automatically the reviewed Blood Ritual feat or free cursed-item creation.

</details>

## MX-46 — Eldritch Echo

Identity: `eldritch_echo`. Original prerequisite: **Forbidden Pact or spellcasting ability, level 3+**.

**Original effect, unchanged**

You gain Eldritch Blast as a known cantrip if you do not already have it; it scales with your level. Once per short rest, when a creature within 60 feet casts a spell, you may echo a simplified version of that spell on your next turn (DM adjudicates equivalent level, usually half the original).

**Proposed operating procedure**

Require character 3 AND (Forbidden Pact OR actual spellcasting). Gain the exact NEW Eldritch Blast cantrip profile below once; duplicate grant through Forbidden Pact shares one identity. Once SR/LR when you actually perceive a creature within 60 ft/line of effect completing an eligible noncopyspell, use a Reaction to capture one matching bounded copy profile below. NEW the source may be ally or foe, but cannot be a resource/copy/production effect or protected boss/legendary ability. Record original rank and the profile’s half-rankq; it must fit your actual qualifying casting route’s learnable ceiling, with Forbidden Pact’s explicit rank 0 grant supplying no ranked ceiling by itself. On your next future regular turn use anAction, actualRPprice and V/S to release that one profile; otherwise it expires at that turn’s end. It is a copied spell activation with actual Dissonance/Refrain/history and interruption at release, no new proc/capture. No free original full spell, copied casterstatistics or Warlockclass.

**Explicit NEW choices:** Grouping, missingcantrip, Reactioncapture and finite paid next-turn copy profile replace open adjudication.

**Authored adjudications**

- Observe rank 4 damage: half-rankq 2 Strike may be captured if your real route can learn rank 2, then costs 3 RP next turn.

- Forbidden Pact alone supplies the cantrip, not a rank 2 spell repertoire orRPpool for that copied release.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "eldritch_echo",
  "name": "Eldritch Echo",
  "description": "Your patron's voice returns through you, repeating power that was never meant for mortal throats. Prestige lineage: Warlock. completed from the existing development record.)",
  "prerequisite": "Forbidden Pact or spellcasting ability, level 3+",
  "effect": "You gain Eldritch Blast as a known cantrip if you do not already have it; it scales with your level. Once per short rest, when a creature within 60 feet casts a spell, you may echo a simplified version of that spell on your next turn (DM adjudicates equivalent level, usually half the original).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You gain Eldritch Blast as a known cantrip if you do not already have it; it scales with your level. Once per short rest, when a creature within 60 feet casts a spell, you may echo a simplified version of that spell on your next turn (DM adjudicates equivalent level, usually half the original).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve prerequisite grouping and missing Eldritch Blast definition/level scaling. Separately bound witnessing a cast within60ft, Short Rest echo trigger, next-turn release action/RP/rank/profile and half-level rounding. Preserve adjudication text but require finite playable choices; no arbitrary monster powers, copying a copy or invented Warlock class access.

</details>

## MX-47 — Forbidden Pact

Identity: `forbidden_pact`. Original prerequisite: **Charisma 13+, level 3+**.

**Original effect, unchanged**

You forge a soul pact with an entity beyond the known planes. You gain Eldritch Blast and one pact sigil (e.g., shadowstep, hex bonus, or energy resistance) chosen with your DM. Once per encounter, you may spend hit points equal to twice the spell's level instead of a ranked-spell recovery.

**Proposed operating procedure**

Require CHA 13 and character 3. Preserve the original beyond-known-planes soul-pact wording as unreviewed setting provenance; this procedure grants no soul transfer, patron demands or cosmological claim. Mechanically gain the exact NEW Eldritch Blast profile and choose permanently one of three finite sigils below with the Director. This feat’s casting ability is CHA and grants rank 0 access only, not anRPpool or ranked repertoire. NEW reconcile “instead of a ranked-spell recovery” and old “instead of a spell slot” as once per real encounter substituting 2×actualrank normal HP sacrifice for the ordinary baseRPprice of one independently known/prepared rank 1–9 spell. Commit true HP loss while retaining at least 1 normal HP; temp HP, mitigation, floors/refunds cannot fund it. It is sacrifice, not damage, so no Wound/concentration/damageproc from the payment. AdditionalRPcosts, strain/armor/component surcharges, materials and action remain actual payments; final price calculation waives only original rankbase before those additions. NoRPis restored, no chargeuse bypassed, no separate ranked grant and no incidental resource output. Interrupted spell keeps all costs/use spent.

**Explicit NEW choices:** Finitecantrip/sigil grants plus explicit NEW base RP substitution resolve the inconsistent recovery/slot phrase without new ontology.

**Authored adjudications**

- An independently legal rank 2 cast may substitute 4 normal HP for base 3 RP once this encounter, still paying an actual extra 1 RP surcharge.

- A pact-holder who knows only Eldritch Blast gains no ranked spell to pay for this way.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "forbidden_pact",
  "name": "Forbidden Pact",
  "description": "You signed in blood and silence. Something old signed back. Prestige lineage: Warlock. completed from the existing development record.)",
  "prerequisite": "Charisma 13+, level 3+",
  "effect": "You forge a soul pact with an entity beyond the known planes. You gain Eldritch Blast and one pact sigil (e.g., shadowstep, hex bonus, or energy resistance) chosen with your DM. Once per encounter, you may spend hit points equal to twice the spell's level instead of a ranked-spell recovery.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You forge a soul pact with an entity beyond the known planes. You gain Eldritch Blast and one pact sigil (e.g., shadowstep, hex bonus, or energy resistance) chosen with your DM. Once per encounter, you may spend hit points equal to twice the spell's level instead of a spell slot.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve exact pact/origin wording without reviewing or revising cosmology before push. Mechanically resolve missing Eldritch Blast, a finite pact-sigil menu with actual stats/cadence and once-per-encounter2xRank HP substitution for ranked recovery. Specify true-HP funding, RP route, zeroHP, interruption and encounter ledger; no unstated entity powers, spell-slot pool or permanent soul transaction procedure.

</details>

## MX-48 — Hemocraft

Identity: `hemocraft`. Original prerequisite: **Intelligence or Charisma 13+**.

**Original effect, unchanged**

When you score a critical hit with a melee attack, the target gains a Bleed stack (1d4 ongoing damage at the start of its turns). You can consume one Bleed stack from a creature within 30 feet to heal 1d8 hit points or deal 1d8 necrotic damage to that creature.

**Proposed operating procedure**

After a personal genuine melee critical hit against meaningful opposition, apply one NEW Hemocraft Bleed record to the still-living eligible target. It pulses 1d4 slashing at each of its next three regular starts; source immunity/anatomy restrictions and the existing Bleeding-family arbitration/cures remain. NEW max 3 own records per target; at cap refresh the earliest deadline without adding a fourth. Same-family parallel records do not all deal damage: existing strongest-die arbitration selects one, but distinct consumable records retain identity. Once per numbered round use BA to consume one present unexpired own Hemocraft record on a creature you perceive within 30 ft/line of effect, including one temporarily suppressed record, choosing 1d8 ordinary self-healing OR one 1d8 necrotic packet to that creature withCONsave against DC 8+PB+your chosenINTor CHA modifier for half. Choose stat permanently at feat acquisition. Pay by ending that exact record before outcome; no refund or consumption of another source’s Bleed. Healing spends a NEW finite Hemocraft Reserve of 2×character level set only at beneficial LR, paying actual restored HP, no excess/copy/resource outputs. Reserve starts 0 on acquisition. No consuming historical/already-cured Bleed or staged victims. The record’s ordinary Medicine-ending DC is the same chosen feat DC; actual positive-potential magical healing ends eligible Bleed through the existing cure procedure.

**Explicit NEW choices:** Three bounded ownBleedrecords, BA/cadence, complete damage/save/cures and finite healing reserve.

**Authored adjudications**

- Consume one actual record to roll 7 healing with 2 Reserve and sufficient missing HP: restore 2 and spend 2.

- A suppressed still-present record can be consumed, but an ended record cannot return for another heal.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "hemocraft",
  "name": "Hemocraft",
  "description": "Blood is ink, blade is quill—you write power in crimson script across flesh and air. Prestige lineage: Bloodbound. completed from the existing development record.)",
  "prerequisite": "Intelligence or Charisma 13+",
  "effect": "When you score a critical hit with a melee attack, the target gains a Bleed stack (1d4 ongoing damage at the start of its turns). You can consume one Bleed stack from a creature within 30 feet to heal 1d8 hit points or deal 1d8 necrotic damage to that creature.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you score a critical hit with a melee attack, the target gains a Bleed stack (1d4 ongoing damage at the start of its turns). You can consume one Bleed stack from a creature within 30 feet to heal 1d8 hit points or deal 1d8 necrotic damage to that creature.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Bind real melee critical, Bleed-stack identity/ownership/cap/duration/cure and1d4 target-start pulse. Define action/cadence/range/sight for consuming one actually existing stack, choice of1d8 healing versus necrotic damage, which creature receives healing, save/attack and true-healing gates. Prevent free repeated consumption, copied Bleed and recursive zeroHP/resource events.

</details>

## MX-49 — Lightning Affinity

Identity: `lightning_affinity`. Original prerequisite: **Spellcasting ability or proficiency in Nature**.

**Original effect, unchanged**

You have resistance to lightning damage. Your lightning spells deal +1 damage per die and ignore half cover when the target is outdoors or under open sky. You have advantage on saving throws against electrical and paralyzing effects. When you take lightning damage, you can use your reaction to store the excess (after resistance) as Storm Charge (max 2); spend 1 charge to add 1d6 lightning to your next spell or weapon attack before the end of your next turn.

**Proposed operating procedure**

Gain lightning resistance and+1 damage per actual native lightning die in your personally cast spells, including native critical dice, as a flat adjustment before save/defense; no bonus per flatpoint, added nonlightning die or copied packet. Against a target actually outdoors/open-sky, your lightning spell attack/save geometry ignores halfcover only; threequarters/total cover remain. Gainadvantage on actual saves against a lightning/electrical payload or a component imposingParalyzed, not everyCONsave. After a hostile meaningful lightning packet deals positive actual numeric damage to you, spendReaction to gain oneStormCharge, max 2. NEW no charge per damagepoint; genuine tempHPabsorption qualifies, fully prevented/floor-only numeric 0 doesnot. Each charge lasts one minute from gain; no maximum cap refresh from a rejected gain. On your own turn, spend one charge withoutAction to prime your next personal weapon attack or immediate damaging spell before next regular end: add 1d6 lightning to one selected hit/packet/shared area roll under added-die rules. Attackmiss consumes the primed rider; no stacking multiplecharges on oneactivation. No charge from self/cooperative/copy/retaliationdamage.

**Explicit NEW choices:** Native lightningdice, oneReactioncharge/event, one-minute stored lifetime and one primed packet.

**Authored adjudications**

- A native 3d6 lightningspell adds 3 before saves; a reaction to 8 actual lightningdamage gains 1 charge, not 8.

- A miss wastes the primed die; a later attack cannot recover that spent charge.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "lightning_affinity",
  "name": "Lightning Affinity",
  "description": "Storm-blood runs quiet in you until the sky asks it to speak. Prestige lineage: Storm Lord. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability or proficiency in Nature",
  "effect": "You have resistance to lightning damage. Your lightning spells deal +1 damage per die and ignore half cover when the target is outdoors or under open sky. You have advantage on saving throws against electrical and paralyzing effects. When you take lightning damage, you can use your reaction to store the excess (after resistance) as Storm Charge (max 2); spend 1 charge to add 1d6 lightning to your next spell or weapon attack before the end of your next turn.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You have resistance to lightning damage. Your lightning spells deal +1 damage per die and ignore half cover when the target is outdoors or under open sky. You have advantage on saving throws against electrical and paralyzing effects. When you take lightning damage, you can use your reaction to store the excess (after resistance) as Storm Charge (max 2); spend 1 charge to add 1d6 lightning to your next spell or weapon attack before the end of your next turn.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve resistance, lightning spell+1/die, conditional half-cover ignoring, electrical/paralysis save advantage and reactive Storm Charges. Define post-resistance received damage versus charges gained,max2/lifetime, Reaction, spending timing/cadence, next spell/weapon+1d6 packet and expiry. Resolve multi-die/area/critical/zero-damage cases without converting every damage point into a charge.

</details>

## MX-50 — Mimicry

Identity: `mimicry`. Original prerequisite: **Spellcasting ability, Intelligence 15+**.

**Original effect, unchanged**

When you witness a spell or monster ability used against you or within 30 feet, you can mimic a simplified version once before your next short rest. The mimicked effect lasts up to 2 rounds and is usually at half potency (DM adjudicates).

**Proposed operating procedure**

Once between beneficial SR/LR completions, when you perceive an eligible real spell/monster ability used against you at its lawful range OR resolving within 30 ft of you and line of effect, capture one matching finite copy profile below withoutAction. NEW one record and one release entitlement per rest epoch; cannot erase/replace to gain repeated uses. No copy from a copy, protectedunique/legendary/boss feature, classengine, resource/action/creation effect or an unobserved component. Actual targeted-at-you clause may exceed 30 ft only if you genuinely perceive the source and effect. The stored profile expires at the next beneficial SR/LR; release before then usesAction, V/S, actualRPprice and its actual qualifying casting ability/rank ceiling. Its numeric native ceiling is half the observed eligible component as detailed below and duration at most two future regular intervals; no original source stats/unboundedDirector invention. Successful capture alone is not a cast; release commits ordinary spell history/interruption and the one-copy-release/round allowance. Failed/countered release consumes record/use, and a later rest never refills a missing copy.

**Explicit NEW choices:** One capture/release perrest, targeted range branch and explicit half-potency profile rules.

**Authored adjudications**

- A perceived attack spell directed at you from 60 ft may qualify through the targeted clause despite the ordinary 30 ftwitness radius.

- Observing a monster restore RP cannot produce a copied recovery profile.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "mimicry",
  "name": "Mimicry",
  "description": "See it once, steal its thunder—your mirror learns faster than pride allows. Prestige lineage: Echomancer. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, Intelligence 15+",
  "effect": "When you witness a spell or monster ability used against you or within 30 feet, you can mimic a simplified version once before your next short rest. The mimicked effect lasts up to 2 rounds and is usually at half potency (DM adjudicates).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you witness a spell or monster ability used against you or within 30 feet, you can mimic a simplified version once before your next short rest. The mimicked effect lasts up to 2 rounds and is usually at half potency (DM adjudicates).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define witnessed/targeted spell or monster ability,30ft senses, one stored simplified profile and acquisition/cast costs/cadence. Replace usually-half/Director-adjudicates ambiguity with explicit finite playable rules while preserving originals. Specify next Short Rest expiry,two-round effect cap,rank/DC/targets and exclusions for resources,actions,copy recursion and unsupported abilities.

</details>

## MX-51 — Quickened Thought

Identity: `quickened_thought`. Original prerequisite: **Intelligence 15+, Arcane Calculus or Temporal Theory**.

**Original effect, unchanged**

You gain +2 to initiative and advantage on concentration saves while holding a readied spell. Once per short rest, you may cast a spell of 2nd level or lower as a bonus action; if you do, you cannot take a reaction until the start of your next turn. When you roll initiative, you may bank one cantrip cast—release it on any later turn in the encounter without spending an action.

**Proposed operating procedure**

Require INT 15 and (Arcane Calculus OR Temporal Theory). NEW resolve the grammatical scope as+2 initiative AND concentration-saveadvantage only while actually holding a readied spell; initiative is not recomputed later. Once SR/LR change an actually available normalActionspell of actualrank 0–2 to BA, paying every normal cost. From commitment until your next regular start you cannot commit anyReaction, even if the spell is countered; existing stacked Reactions finish. Separately, at first legitimate initiative roll of a real encounter, you may immediately prepare one legal normalActioncantrip as a non-action: pay components/independent RP/history, establish held concentration, open interruption, and use the same single pendingReady slot. NEW release that cantrip once withoutAction on one of your later own regular turns in that encounter, retaining actual concentration until then; target legality rechecks at release. This replaces any oldReady, ends at encounter end or lostconcentration, cannot be banked again by reroll/reentry, and shares the free-stored-release cap of one per owner/numbered round with Arcane Calculus. No extra cast/copy/proc at release.

**Explicit NEW choices:** Both passivebonuses scoped to actual hold, one initial cantrip preparation and persistent no Reaction debt.

**Authored adjudications**

- A banked cantrip paid at initiative can release on your second regular turn withoutAction if concentration survives.

- Using theBAspell branch then leaves noReaction for Counterspell until the real next regular start.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "quickened_thought",
  "name": "Quickened Thought",
  "description": "Your mind outpaces the tick of Aethel's clocks—ideas arrive finished in the Temporal Tower's shadow, as if tomorrow's spell were already written in today's breath. Prestige lineage: Chronomancer. completed from the existing development record.)",
  "prerequisite": "Intelligence 15+, Arcane Calculus or Temporal Theory",
  "effect": "You gain +2 to initiative and advantage on concentration saves while holding a readied spell. Once per short rest, you may cast a spell of 2nd level or lower as a bonus action; if you do, you cannot take a reaction until the start of your next turn. When you roll initiative, you may bank one cantrip cast—release it on any later turn in the encounter without spending an action.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You gain +2 to initiative and advantage on concentration saves while holding a readied spell. Once per short rest, you may cast a spell of 2nd level or lower as a bonus action; if you do, you cannot take a reaction until the start of your next turn. When you roll initiative, you may bank one cantrip cast—release it on any later turn in the encounter without spending an action.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve Arcane Calculus OR Temporal Theory, readied-spell+2 initiative and concentration advantage. Define rank≤2 Bonus Action cast once per Short Rest, no-Reaction debt and expiry. Separately define initiative-banked cantrip setup/payment/one record/release on any later turn, target recheck and no free-copy or extra-turn loop.

</details>

## MX-52 — Spell Reflection

Identity: `spell_reflection`. Original prerequisite: **Spellcasting ability, level 8+**.

**Original effect, unchanged**

Once per short rest, when you are targeted by a single-target spell, you may reflect it back at the caster as an immediate reaction (they make saving throws as if they had cast it on themselves). When you take spell damage, the attacker takes psychic damage equal to half the damage you received (once per round).

**Proposed operating procedure**

Once SR/LR spendReaction in Spell Deflection’s same pre-payload window when you are the sole creature target of an actual single-target spell. NEW redirect to the original caster only if that caster is a legal recipient under its own spell’s target/range/line rules; preserve original owner, rank, attackbonus, DC, payment and concentration. Resolve its original attack/save against itself; no automatic self-hit or invented save. Noarea, multi-target, copied/alreadyredirected or protectedpayload; an illegal caster-recipient makes this activation unavailable withoutpayment. Redirecting does not teach/capture the spell. Separately, once per numbered round after an owned hostile spell deals positive actualnumericdamage to you, the living personally perceived caster within 60 ft/line of effect takes psychicdamage=floor(actualDamageDealt/2). NEW this passive retaliation requires you stillalive after the complete packet, noReaction, excludes overkill and self/friendly/copy/reflection roots, and consumes at first qualifying packet even if half rounds 0. Ordinary psychicdefenses apply. It cannot itself reflect, capture, heal, generate RP or restart a damageproc; no summing multiple area victims.

**Explicit NEW choices:** Legal original-caster redirect plus bounded 60 ft nonrecursive half-actual-damage retaliation.

**Authored adjudications**

- A hostile spell removes 3 HP from HP 3 despite 12 rawdamage: if you survive, retaliation is 1 psychic, not 6.

- A willing-only allybuff cannot be reflected into an unwilling original caster merely because it selected you.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "spell_reflection",
  "name": "Spell Reflection",
  "description": "What was sent returns wearing your sigil—mirrors do not forgive. Prestige lineage: Echomancer. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, level 8+",
  "effect": "Once per short rest, when you are targeted by a single-target spell, you may reflect it back at the caster as an immediate reaction (they make saving throws as if they had cast it on themselves). When you take spell damage, the attacker takes psychic damage equal to half the damage you received (once per round).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Once per short rest, when you are targeted by a single-target spell, you may reflect it back at the caster as an immediate reaction (they make saving throws as if they had cast it on themselves). When you take spell damage, the attacker takes psychic damage equal to half the damage you received (once per round).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define once-per-Short-Rest single-target redirect as an actual Reaction, caster target legality, original attack versus save/DC and recursion prevention. Separately define half-actual-spell-damage psychic retaliation once per round: attribution,range,rounding,resistance,zeroHP and repeated packets. Source text cannot automatically copy class/monster powers or all target riders.

</details>

## MX-53 — Stormcaller

Identity: `stormcaller`. Original prerequisite: **Spellcasting ability, proficiency in Nature or Spellcraft**.

**Original effect, unchanged**

You can create a 15-foot Static Field as an action (once per short rest): creatures entering or starting their turn there take 1d6 lightning damage and have disadvantage on Dexterity saves until they leave the field. Once per short rest, you may Stormstep up to 30 feet to a target you can see, dealing 1d8 thunder damage to adjacent creatures and leaving a crackling afterimage that grants you half cover until the start of your next turn. While outdoors during a storm, your Static Field radius increases to 20 feet and lightning spells you cast ignore the first instance of half cover between you and the target.

**Proposed operating procedure**

Require actual spellcasting AND (Nature proficiency OR a separately established Spellcraft credential). Spellcraft is not an Arcana alias; if absent, use the Nature alternative. Once per beneficial SR/LR, an Action places a fixed 15 ft radius Static Field at a perceived point within 60 ft and line of effect, requiring concentration for up to one minute. It affects all creatures, including allies: first actual entry or regular start inside per target per numbered round deals 1d6 lightning automatically. Placement covering a creature counts as entry once. While inside an active field, creatures have disadvantage on DEX saves, ending immediately on exit; actual immunities/suppression apply. Outdoors during an established storm, choose a 20 ft radius at creation. A separate once-SR/LR Action, Stormstep, teleports you up to 30 ft to a visible fitting unoccupied space with line of effect. Every other creature within 5 ft of arrival makes a DEX save against your actual casting DC for 1d8 thunder, half on success. NEW select the actual owned casting route at acquisition for both feat activations. Your afterimage supplies half cover until your next regular start only when the geometric ray from the incoming effect origin to your new position passes through your previous occupied space; it is not a solid object or general AC bonus. During an actual outdoor storm, your lightning spells also ignore half cover, but not stronger cover. These activations are nonspell magical feat techniques; they do not create weather, RP or extra casting resources.

**Explicit NEW choices:** TwoAction activations/ledgers, fixedconcentrationfield, explicit automaticpulse and directionalafterimage.

**Authored adjudications**

- Entering then exiting/reentering thefield inoneround deals onlyonepulse tothatcreature.

- A normalrainstorm canqualifyif theDirector’s actualweatherrecord saysstorm; thefeat doesnotdeclareone.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "stormcaller",
  "name": "Stormcaller",
  "description": "You whistle up weather like a shepherd calls dogs—clouds come hungry. Prestige lineage: Storm Lord. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability, proficiency in Nature or Spellcraft",
  "effect": "You can create a 15-foot Static Field as an action (once per short rest): creatures entering or starting their turn there take 1d6 lightning damage and have disadvantage on Dexterity saves until they leave the field. Once per short rest, you may Stormstep up to 30 feet to a target you can see, dealing 1d8 thunder damage to adjacent creatures and leaving a crackling afterimage that grants you half cover until the start of your next turn. While outdoors during a storm, your Static Field radius increases to 20 feet and lightning spells you cast ignore the first instance of half cover between you and the target.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You can create a 15-foot Static Field as an action (once per short rest): creatures entering or starting their turn there take 1d6 lightning damage and have disadvantage on Dexterity saves until they leave the field. Once per short rest, you may Stormstep up to 30 feet to a target you can see, dealing 1d8 thunder damage to adjacent creatures and leaving a crackling afterimage that grants you half cover until the start of your next turn. While outdoors during a storm, your Static Field radius increases to 20 feet and lightning spells you cast ignore the first instance of half cover between you and the target.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve Nature OR undefined Spellcraft credential. Define15ft Static Field radius/placement/duration/concentration, entry/start cadence, damage/save and DEX-save-disadvantage ending, plus storm20ft variant. Separately define30ft Stormstep action/legal space,1d8 adjacent-thunder targets/save and afterimage half-cover geometry; two Short Rest ledgers and cover bypass stay distinct.

</details>

## MX-54 — Temporal Theory

Identity: `temporal_theory`. Original prerequisite: **Intelligence 15+, proficiency in Arcana, level 8+**.

**Original effect, unchanged**

At the end of your turn, you may bank one unused action (move, object interaction, or bonus action if available), storing up to 2 banked actions. Spend banked actions on later turns. After spending 2 banked actions in one encounter, you gain one level of fatigue when combat ends.

**Proposed operating procedure**

At your original regular-turn end, bank at most one genuinely unused NORMAL allowance: your wholly unspent movement budget, ordinary free object interaction, or unused ordinary Bonus Action. You must be conscious, able to act and actually possess it; prohibited, extra, borrowed, banked, readied or generated allowances cannot fund a token. Movement requires zero movement spent this turn; snapshot actual legal distance and modes. Consume the chosen allowance into one typed token; hold at most two, expiring at encounter end. On a later own regular turn, spend at most one token of each type without Action for its exact purpose: move up to min(stored feet, current legal normal Speed), one ordinary interaction, or one currently legal BA ability. Pay current terrain; modes must still exist. No conversion to full Action, Reaction, work time or new token, and no refresh of feature uses/cadences. After the second token spent in the real encounter, record one irrevocable fatigue cost due at encounter end: NEW one Core Exhaustion level, with actual immunity/recovery and lethal level 6 rules. Further spending creates no extra fatigue under this source but cannot erase the cost. No Time Loop, rewind or resource restoration.

**Explicit NEW choices:** Typed ordinary allowances, regular-turn banking, finite expiry and explicit Core Exhaustion translation.

**Authored adjudications**

- Store a wholly unused 30 ft movement allowance. If current Speed is 20 when later spent, it supplies at most 20 additional feet, with current terrain costs.

- A Bonus Action supplied by Mystic Recoil cannot be banked into a persistent token.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "temporal_theory",
  "name": "Temporal Theory",
  "description": "Time is not a river—it is a ledger. You have learned to borrow from tomorrow and repay in fatigue. Prestige lineage: Chronomancer. completed from the existing development record.)",
  "prerequisite": "Intelligence 15+, proficiency in Arcana, level 8+",
  "effect": "At the end of your turn, you may bank one unused action (move, object interaction, or bonus action if available), storing up to 2 banked actions. Spend banked actions on later turns. After spending 2 banked actions in one encounter, you gain one level of fatigue when combat ends.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "At the end of your turn, you may bank one unused action (move, object interaction, or bonus action if available), storing up to 2 banked actions. Spend banked actions on later turns. After spending 2 banked actions in one encounter, you gain one level of fatigue when combat ends.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define unused move/object-interaction/Bonus Action as actual existing separate budgets, not an interchangeable Action. Specify end-turn banking,max2,expiry/type-preserving spending on later turns,no overlap/double-spend and real movement units. Resolve after2spent-per-encounter fatigue as an actual condition, timing and recovery. No action generation, extra turns or unfinished Time Loop activation.

</details>

## MX-55 — Trapcasting

Identity: `trapcasting`. Original prerequisite: **Conjure Flora or Verdant Bond**.

**Original effect, unchanged**

Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot area, 2d6 damage, type chosen at conjuring).

**Proposed operating procedure**

Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants. NEW only actual Conjure Flora profiles below qualify until another source is reviewed. At creation optionally arm a plant’s square as a magical trap using its fixed mode/burst type. Each meaningful hostile’s first actual entry in that square per numbered round, including forced entry but not plant placement, makes DEX save against flora DC; failure applies the profile’s trap result, success none. A legal trigger commits the owner’s shared offensive-companion allowance even on a save; if already spent by a command/other trap, no new trap activation occurs that round. One entrance cannot multiply across plants. Plants are visible, not automatically hidden: Action INT(Investigation) vs flora DC identifies an armed mode; Action DEX with actual thieves’ tools vs same DC disarms one trap without destroying its body, failure gives no automatic explosion. Alternatively, BA consumes one active plant within 60 ft you perceive with line of effect for a 10 ft-radius Bloom Burst at its space: all creatures DEX save,2d6 fixed piercing/poison damage, half success. Same offensive allowance; body ends before burst, cannot also command, and never refunds creation.

**Explicit NEW choices:** Exact plant eligibility, one shared offensive allowance, entry/disarm procedure and body-consuming burst.

**Authored adjudications**

- Forced hostile entry can trigger a plant, but another plant cannot produce a second offensive outcome after the group allowance is spent that round.

- Detonation consumes the actual plant even if every creature saves. An expired plant cannot be detonated.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "trapcasting",
  "name": "Trapcasting",
  "description": "Roots, thorns, and spore-mines—you sow violence that waits patiently to bloom. Prestige lineage: Verdant Animist. completed from the existing development record.)",
  "prerequisite": "Conjure Flora or Verdant Bond",
  "effect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot area, 2d6 damage, type chosen at conjuring).",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Your conjured flora count as magical traps. Enemies moving through a seedling's square must succeed on a Dexterity save or suffer its effect (damage, restraint, or poison). You can detonate one seedling as a bonus action for a Bloom Burst (10-foot AoE, 2d6 damage, type chosen at conjuring).",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve Conjure Flora OR Verdant Bond gate without granting seedlings by implication. Define source seedling trap mode, real hostile entry/forced movement, save/DC/cadence/damage/restraint/poison duration and detection/disarm. Bind Bonus Action detonation consuming exactly one seedling,10ft geometry,2d6 chosen type,targets/save and conservation with existing commands/expiry.

</details>

## MX-56 — Verdant Bond

Identity: `verdant_bond`. Original prerequisite: **Proficiency in Nature, spellcasting ability**.

**Original effect, unchanged**

You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.

**Proposed operating procedure**

While conscious, exchange brief simple ideas with actual plants within 60 ft you perceive and have line of effect to, using ordinary communication; receive only coarse current fear, hunger, dormancy, not language, intelligence, visions, identity records or omniscient history. A plant may be unresponsive; compel nothing. Gain advantage on actual Nature checks in wilderness terrain, with normal work/senses. While at least one Conjure Flora seedling remains active, gain+1 spell attack/DC under the NEW finite Nature predicate: spells actually cast through your Druid, Ranger or Shaman route, excluding copied profiles; no alias from a plant-themed name. Current strongest same-stat bonus applies. In that same active-flora state, difficult terrain caused solely by nonmagical plants costs normal movement; other causes/hazards remain. Once LR spend one uninterrupted minute at a real rooted stand within reach to store a brief message of at most 25 words and one designated known ally identity. For 24 elapsed hours, the first time that ally passes within 10 ft the stand whispers it audibly once and ends the record. Others can hear normally; no remote confirmation or extracted plant memory. Destroying the stand ends the message; no new sentience or cosmology is asserted.

**Explicit NEW choices:** Explicit class-route Nature predicate and one-shot 25 word stored message.

**Authored adjudications**

- With an active plant, a spell actually cast through the Ranger route may receive the proposed +1 DC, subject to strongest-bonus arbitration.

- The stored message is audible to anyone close enough to hear when the designated ally triggers it.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "verdant_bond",
  "name": "Verdant Bond",
  "description": "The green speaks to you in sap and silence. You answer with growth. Prestige lineage: Verdant Animist. completed from the existing development record.)",
  "prerequisite": "Proficiency in Nature, spellcasting ability",
  "effect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "You can communicate simple ideas to plants within 60 feet and sense coarse emotions from rooted life (fear, hunger, dormancy). While you have at least one conjured flora active, you gain +1 to spell save DC and attack rolls for nature spells, and difficult terrain from nonmagical plants does not cost you extra movement. You have advantage on Nature checks in wilderness terrain. Once per long rest, you may ask a stand of plants to hold a memory for 24 hours—a whispered name, direction, or warning that replays when an ally you designate passes within 10 feet.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Preserve simple plant communication/coarse sensations within60ft, Nature advantage in wilderness, active-flora+1 nature spell DC/attacks, plant-terrain movement and24-hour stored warning. Define finite eligible natural-spell predicate,actual senses/knowledge,one stand/message/ally trigger and costs. No universal sentience, omniscient plants, new conjuration or cosmology review.

</details>

## MX-57 — Voltyros Pact

Identity: `voltyros_pact`. Original prerequisite: **Stormcaller or Lightning Affinity, level 6+**.

**Original effect, unchanged**

Your lightning spells chain to one additional target within 15 feet for half damage. While you remain stationary for a full round, you gain resistance to all damage until the start of your next turn and +2 to spell damage (Eye of the Tempest). Once per long rest, you may call a stormform burst: 30-foot line of lightning for 4d6 damage.

**Proposed operating procedure**

Require character 6 AND (Stormcaller OR Lightning Affinity); preserve the named pact/plane story undecided. Once per personal noncopy lightning spell’s initial resolution, choose one additional creature within 15 ft of one original recipient, perceived with line of effect from that recipient. It must satisfy original creature eligibility and not already be targeted by that cast. Deal only half the selected original native lightning packet before defenses, rounded down; use the original DC/save ability for a fresh save or original attack bonus for a fresh attack, with original half/none on success. No other riders, new cast or chain from a chain. After one entire original start-to-next-start interval without any position change, gain Eye of the Tempest: resistance to all damage and+2 to one immediate native packet/shared roll of each personal spell until the following regular start. Any movement, teleport or forced displacement ends Eye immediately; riding a moving mount counts as movement. Repeated stationary intervals may renew without stacking. Separately, once LR use Action for a 30 ft-long 5 ft-wide lightning line: all creatures DEX save,4d6 lightning half success. DC=8+PB+one actual casting ability selected at acquisition, or INT if no casting source. The line is a magical nonspell feat technique, with noRPpool or weather creation.

**Explicit NEW choices:** One lightning-only chain, exact stationary interval and complete nonspell line profile.

**Authored adjudications**

- Native 17 lightning damage gives a chain base of 8 before the new target’s save and defenses; that child cannot chain again.

- Forced movement prevents the stationary interval. Riding a moving mount is not stationary.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "voltyros_pact",
  "name": "Voltyros Pact",
  "description": "You bargained with the Plane of Storms itself—Voltyros marks you with copper taste and crown-light. Prestige lineage: Storm Lord. completed from the existing development record.)",
  "prerequisite": "Stormcaller or Lightning Affinity, level 6+",
  "effect": "Your lightning spells chain to one additional target within 15 feet for half damage. While you remain stationary for a full round, you gain resistance to all damage until the start of your next turn and +2 to spell damage (Eye of the Tempest). Once per long rest, you may call a stormform burst: 30-foot line of lightning for 4d6 damage.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "Your lightning spells chain to one additional target within 15 feet for half damage. While you remain stationary for a full round, you gain resistance to all damage until the start of your next turn and +2 to spell damage (Eye of the Tempest). Once per long rest, you may call a stormform burst: 30-foot line of lightning for 4d6 damage.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Resolve Stormcaller OR Lightning Affinity pluslevel6 mechanically while preserving the named pact/plane text for post-push review. Define one extra target15ft/half-lightning damage,actual chain eligibility and no recursion. Define a stationary full-round marker, forced movement, all-damage resistance endpoint,+2 spell damage packet; define30ft4d6 line activation,save/DC,width and Long Rest use.

</details>

## MX-58 — Wounding Magic

Identity: `wounding_magic`. Original prerequisite: **Spellcasting ability**.

**Original effect, unchanged**

When you deal damage with a spell, you may leave an Agony wound: the target takes 1d4 necrotic damage at the start of each of its turns for 3 rounds (save ends). Wounded targets have disadvantage on Constitution saves to regain hit points and on saves against resurrection effects.

**Proposed operating procedure**

After your personally cast noncopy spell deals positive resolved damage, optionally apply one Agony record to one living damaged target, once per owner/target/numbered round. Reapplication refreshes one profile without stacked dice. It deals 1d4 necrotic at the next three original target regular-start markers; a CON save against the generating cast DC at each affected regular end, including a current turn if applicable, ends it. The final third scheduled pulse ends the record after damage; no extra ending save afterward. It is a magical ongoing wound, not Core Wound, maximum HP injury or Bleeding by name. NEW a legal positive-potential magical heal or Action Medicine vs source DC ends it; suppressed records remain curable. While active, disadvantage applies only to actual existing CON saves to regain HP and actual saves against resurrection effects; no such save is invented. Death suspends living damage, retaining only the unexpired record tied to that exact death instance until the original third-start deadline; missed pulses are consumed, never backlogged. A legal revival closes that corpse-specific resurrection rider and retains only any still-future living pulse schedule until cured/expired. This grants no resurrection block or permission. Secondary ticks cannot create further Agony, copies, lifesteal or resource procs. Any independent Necrotic Affinity seal needs its own real fatal-root predicate.

**Explicit NEW choices:** Three actual scheduled pulses, bounded death-instance rider, explicit cure and actual-save-only disadvantage.

**Authored adjudications**

- The first 1d4 pulse resolves at the target’s regular start; a successful CON save at its regular end removes the remaining pulses.

- A normal heal with no save gains no new saving throw. Death skips living pulses without extending the original deadline or granting resurrection permission.

<details><summary>Full original record and original conference question</summary>

```json
{
  "id": "wounding_magic",
  "name": "Wounding Magic",
  "description": "Your spells leave wounds that resist closure—pain that outlasts the casting. Prestige lineage: Soulrender. completed from the existing development record.)",
  "prerequisite": "Spellcasting ability",
  "effect": "When you deal damage with a spell, you may leave an Agony wound: the target takes 1d4 necrotic damage at the start of each of its turns for 3 rounds (save ends). Wounded targets have disadvantage on Constitution saves to regain hit points and on saves against resurrection effects.",
  "type": "Magic",
  "source": "Completed from the existing feat draft corpus on 2026-08-05; playable wording supplied, final balance pass still required.",
  "legacyEffect": "When you deal damage with a spell, you may leave an Agony wound: the target takes 1d4 necrotic damage at the start of each of its turns for 3 rounds (save ends). Wounded targets have disadvantage on Constitution saves to regain hit points and on saves against resurrection effects.",
  "status": "provisional-complete",
  "balanceReview": true,
  "draft": false,
  "deprecated": false,
  "needsReview": true
}
```

Define optional spell-damage Agony application,frequency,target/source ledger,1d4 necrotic start pulses,3round duration,save ability/DC and cure/suppression. Define disadvantage only on actual existing CON healing/resurrection saves and compatibility with Wounded/true-healing gates. No invented healing save, resurrection permission or soul taxonomy; secondary damage cannot recursively create wounds.

</details>

## Complete NEW supplements

These are explicit proposals needed to make the formerly undefined clauses playable. They are not recovered source facts. The source remains335feats/848ordinary spells. Eldritch Blast is a proposed feat-only supplement, outside that ordinary catalog.

### copyProfileContract

```json
{
  "status": "NEW proposed finite feat-copy interface; the five actual Mirrorsage cards/engine are comparisons, not automatic grants.",
  "capture": "Capture only one directly witnessed resolved component that actually expresses one profile below. Record canonical source/event, actual original spell rank or pre-encounter monster effective rank, native magnitude before external bonuses/defenses, selected type/profile and qualifying own casting route. For monster abilities without a spell rank, use max(1, min(9, ceil(actualCR/2))); missing CR needs a rating assigned before the encounter, never a favorable after-the-fact guess. No unique/legendary/boss feature without an independently reviewed exception; no copying copies, class engines, actions, resources, permanent changes, resurrection, creation, items or protected information. An unsupported role is ineligible, not a blank Director permission.",
  "rankAndPayment": "For original rank 0, q=0; otherwise q=max(1, floor(originalRank/2)). The chosen actual owned spellcasting route must independently support learning q; merely owning a pool or feat prerequisite does not. Use that route’s real ability for attack/DC and spell components V/S, normal rank price 0/2/3/5/7/10/13/17/21/26 plus actual adjustments. It grants a temporary feat-copy route only, never the original full spell. Spellcasting time is oneAction. At release pay/cast/history/interrupt once, with copy-provenance flags disabling copy/resource/class-proc chains. An explicit source such as Mirrorsage retains its own actual profile/rank/payment instead of being silently converted.",
  "numericBound": "For numeric damage/heal/ward select one witnessed native component/type and record its rolled or fixed magnitude B before external bonuses, saves, defenses and recipient caps. If that magnitude was hidden, the Director records it privately; no free identification is given. At feat-copy release roll (q+1)d6, then bound the native numeric result to min(roll, floor(B/2)). No copied critical multiplier, external damage/heal modifier, converted excess or extra recipients. Actual recipient defenses and healing limits still apply. A zero ceiling cannot produce a numeric benefit. This is an explicit NEW meaning of half potency, not an assertion about original undefined wording.",
  "lifecycle": "At most one feat-copy release per owner per numbered round across Eldritch Echo, Mimicry and adapted copies. A Mirrorsage owner also spends its existing shared release allowance; an unowned Mirrorsage engine is not granted. Strike/Burst/Mend are immediate. Ward/Hindrance/Boon/Step use their stated maximum two-interval duration; source-specific shorter hold deadlines still govern. Only one pending feat-copy record across Eldritch Echo/Mimicry; before a new capture choose whether to replace the old, losing its paid capture/use without refund. Adaptation may retain permission but creates no second release allowance. No copied effect grants extra Action/BA/Reaction, persistent body, loot, learning or concentration capacity.",
  "profiles": [
    {
      "id": "strike",
      "role": "Direct single-target damage",
      "activation": "Action",
      "range": "60 ft, one perceived creature with line of effect",
      "resolution": "Actual own casting ability+PB spell attack; on hit bounded numeric damage of one observed native type. No added critical dice. No original riders. Instant."
    },
    {
      "id": "burst",
      "role": "Area damage",
      "activation": "Action",
      "range": "Point within 30 ft;10 ft radius, at most 3 originally declared perceived creatures in area with line of effect",
      "resolution": "DEX save vs own DC for bounded numeric observed-type damage, half on success; one shared roll. No original riders. Instant."
    },
    {
      "id": "mend",
      "role": "Actual normal HP healing",
      "activation": "Action",
      "range": "30 ft one perceived willing living creature with line of effect",
      "resolution": "Restore bounded numeric HP under actual prohibitions/maximum/Critical caps. No reviving, healing dice add-ons, Wound cure, heal-copy/resource trigger or excess conversion. Instant."
    },
    {
      "id": "ward",
      "role": "Temporary HP",
      "activation": "Action",
      "range": "30 ft one perceived willing living creature with line of effect",
      "resolution": "Offer bounded numerictemp HP into the actual single grant ledger, ending at the source’s second future regular start. Rejected offer wastes the copy. No linked riders."
    },
    {
      "id": "hindrance",
      "role": "Actual slow or action/reaction control",
      "activation": "Action",
      "range": "30 ft one perceived creature with line of effect",
      "resolution": "WIS save vs own DC or Speed−10 ft and no new Reactions until its next future regular end, never later than the source’s second future regular start. Strongest slow arbitration; no wholeAction/turn denial, repeated save or original hard-control rider."
    },
    {
      "id": "boon",
      "role": "A source actually granting a positive attack, save or AC modifier",
      "activation": "Action",
      "range": "30 ft one perceived willing creature with line of effect",
      "resolution": "Choose one statistic actually benefited by the witnessed source: +1 AC OR+1 to one next actual attack roll OR+1 to one next actual save, through source’s next future regular end. Current strongest bonus arbitration; no new roll or cloned concentration."
    },
    {
      "id": "step",
      "role": "Actual short personal movement/teleport",
      "activation": "Action",
      "range": "Self to visible unoccupied fitting space within min(15 ft, floor(observed distance/2))",
      "resolution": "If original component was teleport, teleport with actual line of effect and ordinary teleport restrictions; otherwise move that distance over an actual legal path paying terrain and provoking normally. No passenger, planar travel, new locomotion mode or movement into an unseen space. Instant."
    }
  ]
}
```

### eldritchBlast

```json
{
  "id": "feat-supplement.eldritch-blast",
  "name": "Eldritch Blast",
  "status": "NEW cantrip payload absent from the ordinary 848 and existing ancestry supplement; proposed feat-only grant, not a new ordinary class row.",
  "rank": 0,
  "castingAbility": "CHA; both feat grants share this one source ability/identity, not two selectable histories.",
  "castingTime": "Action",
  "components": [
    "V",
    "S"
  ],
  "rangeFeet": 60,
  "effect": "Make one spell attack for 1d10 force. Explicit total-character-level scaling supplies 2 beams at 5,3 at 11,4 at 17; declare each target before its attack, each must be perceived within 60 ft/line of effect. Different legal recipients allowed; each beam is a separate hit/damage event. Ordinary critical doubles that beam’s die only. No CHA damage modifier, pushing or automatic extra effect. Normal cantrip RP 0, actual independent costs, Dissonance/Refrain and interruption apply once for the cast, not once per beam. No generic ordinary catalog access or Warlock class is inferred.",
  "grant": "Forbidden Pact or Eldritch Echo supplies one actual cantrip spellcasting route. Duplicate grant creates no duplicate spell, price waiver, resource pool, known-spell count or separate Refrain."
}
```

### pactSigils

```json
[
  {
    "id": "shadowstep",
    "effect": "Once SR/LR use BA to teleport up to 15 ft from actualdim/dark occupiedspace to a visible fitting unoccupieddim/dark destination withlineofeffect. Whole footprints qualify. This use is a separate exact sigil source, not free Dark Affinity acquisition; ordinary teleport prohibitions remain."
  },
  {
    "id": "hex",
    "effect": "Once SR/LR use BA to mark one perceived hostile within 30 ft/lineofeffect until your next future regular start. Your next personal direct weapon hit against it before expiry adds 1d4 necrotic, then ends the mark; critical doubles the die. No curse classification, drop reward, ongoing damage or Curse Channeling grant."
  },
  {
    "id": "energyResistance",
    "effect": "At acquisition choose one permanent damage resistance: acid, cold, fire, lightning or thunder. It never stacks with another resistance to the same type. No immunity, absorption, charge generation or creature/plane affiliation."
  }
]
```

### floraBody

```json
{
  "status": "NEW finite conjured body for the feat; no origin/spirit ontology decided.",
  "size": "Tiny, occupies a supported 5 ft square as a low plant; does not block traversal or grant cover; zeroSpeed and no voluntary movement. Can be carried only as an ordinary object-body interaction; lifting/uprooting ends it immediately without harvest.",
  "statistics": "Plant creature; no assumed language, mind immunity or world-origin claim. AC 12, HP 5+owner PB snapshotted at creation; saves +owner PB, other checks +0. No damage/condition immunities or special senses unless an actual source grants them. It perceives commands within 60 ft through ordinary sight/hearing; Silence matters for spoken commands. It has no independent initiative, Action, Bonus Action or Reaction, and no attack outside the commanded profiles. Zero HP permanently destroys it instead of creating a dying body. No corpse, reward, harvest, resource/soul collection, loot or Supply credit. Ordinary legal damage and healing may affect the actual creature but cannot recreate a destroyed plant, refill its creation entitlement or extend its deadline.",
  "dc": "At acquisition select one actual possessed spellcasting route; use DC 8+current PB+that route’s current ability modifier. No phantom Wisdom/Spellcraft statistic. Actual source-specific component/target defenses still apply.",
  "cadence": "Action creates;1/SR or LR, capacity 1 or 2 at 10. NEW level 10 completion: after the first creation, one additionalAction before that first seedling expires may create the second without a second rest use. This one extra creation entitlement is bound to that original committed use and is consumed once; if missed/lost it is not banked. Each plant has its own original minute deadline. No replacement/revival can restore the entitlement. Any command, trap orBurst with a hostile result uses the owner’s one shared offensive-companion allowance per numbered round; one selected mode outcome for the coordinated group.",
  "modes": [
    {
      "id": "lash",
      "command": "One creature within 10 ft of any commandedplant makesDEXsave;1d6 piercing, half on success. One shared attack outcome, not a die perplant.",
      "trap": "Entering creatureDEXsave;failure 1d6 piercing, success 0.",
      "burstType": "piercing"
    },
    {
      "id": "spore",
      "command": "One creature within 10 ft of any commandedplant makesCONsave orPoisoned until its next future regular end. No damage; actual poison/Poisoned immunities apply.",
      "trap": "Entering creatureDEXsave;failurePoisoned until its next future regular end, successnone.",
      "burstType": "poison"
    },
    {
      "id": "entangle",
      "command": "Choose one 10 ft square within 10 ft of a commandedplant, withsupportedground/lineofeffect. Each creature in it makesSTRsave orRestrained until its next future regular end. On its turn an affected creature may spendAction for STR(Athletics) or DEX(Acrobatics) vsflora DC to end its ownrecord. No damaginggrowth or freewall.",
      "trap": "Entering creatureDEXsave;failureRestrained until its next future regular end with sameActionescape, successnone.",
      "burstType": "piercing"
    }
  ],
  "endpoints": "Poisoned/Restrained records also end if the generating plant ends; no concentration is required. Reapplying same profile follows ordinary nonstacking rules. Burst consumes one body before resolving a 10 ft-radius area, all creaturesDEXsave,2d6 selectedtype half on success. Chosenmode/type doesnotchange aftercreation. No destroyed body can command or trap during the resolving event.",
  "commandChoice": "Every seedling may use the printed Lash command. Its selected creation mode additionally determines its Spore or Entangle option and its Trapcasting result/burst type; selecting Lash leaves that basic profile. A coordinated command chooses only one permitted outcome from one actual participating plant. Other plants extend the legal Lash origin as printed but never multiply damage, control areas or offense allowances."
}
```

### minorBuffTransfer

```json
{
  "status": "NEW finite Spellweave interpretations; original spells remain unchanged outside this feat route.",
  "guidance": "One 1d4 actual task/ability check of next spell.",
  "resistance": "One 1d4 actual concentration save maintaining next spell.",
  "true-strike": "Advantage on first actual spell attack of next spell."
}
```

### timeTagOverlay

```json
{
  "status": "NEW feat-only Time tags, not recovered source tags and not a public catalog mutation.",
  "spellIds": [
    "slow",
    "haste",
    "future-echo"
  ],
  "condition": "Only an actual failed save can trigger Temporal Flux; existing save-less payloads gain no save."
}
```

### naturePredicate

```json
{
  "status": "NEW Verdant Bond feat predicate, not an ancestry/planar identity.",
  "castingClassRoutes": [
    "Druid",
    "Ranger",
    "Shaman"
  ],
  "exclusions": "Copied/borrowed profile aliases; actual independent route access/rank/school still required."
}
```

## Joint decisions still required

Review all58 original questions and these exact procedures with GPT. In particular: the eight field conflicts; damage versus trueHP costs; refund funding; copied profiles and Eldritch Blast; second-plant creation at level10; additional ritual-time minima; separate Runic Shield ward; finite Spellweave and Time/Nature predicates; typed action banking and fatigue; reflection ownership; bleeding/healing reserves; and resurrection-save wording. Preserved source alternatives are not deleted when a proposal is selected.

Together with earlier cohorts there are325 complete proposed feat procedures and2 expressly deferred grant outlines for the327 pending source feats, plus the8 already reviewed feats. This is proposal coverage, not review closure. The actual expedition verdict, exact-candidate review, full game flow review and later GitHub delivery remain outstanding. Cosmology review follows the verified push.
