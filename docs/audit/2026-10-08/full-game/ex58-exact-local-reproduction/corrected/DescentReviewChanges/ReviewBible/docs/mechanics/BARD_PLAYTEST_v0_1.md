# Bard — Crescendo playtest draft v0.1

**Playable performance module for a focused table test; numerical balance is provisional.** Developed with the Calibration Review notebook on 8 October 2026 after the owner said, “I like your bard example.” This adopts scheduled feature choices for the Bard pilot. It does not replace the approved books or finish the other sixteen classes.

The complete set has 50 specified abilities: 10 Base, 10 Arch, and 10 in each Hero path. You learn a subset through the schedule below. All original descriptions remain verbatim in the [card data](../../data/public/Decennium_Descent_Bard_Playtest_v0_1.json), with source lines and stable IDs. Exact quantities, restrictions and timing in this module are new design unless identified as recovered below.

## At the table

Track **HP, RP, Dissonance, Crescendo (0–5), last performance started, one concentration effect, one pending Echo, and recharge counters**. Use the printed cards and this module together.

- **Bard kit:** Charisma is primary; Dexterity and Intelligence secondary. Hit Die d8; first character level HP 8 + Constitution modifier. Light armor, simple weapons and three musical instruments. The book also lists instruments as weapons; use existing improvised-weapon rules, not an invented weapon damage die. Keep ordinary ancestry, background, equipment, skill and saving-throw rules from character creation.
- **S (song dice):** 1 at Bard levels 1–4, 2 at 5–10, 3 at 11–16, 4 at 17–20. “S d6” means that many six-sided dice. **C = max(1, Charisma modifier)** for printed effects; attack rolls and DCs use the actual modifier, even if negative.
- **Performance attack:** d20 + normal character proficiency bonus + Charisma modifier against AC. Natural 1 misses; natural 20 hits and doubles damage dice, not flat bonuses. Verses Unbound adds its printed natural-19 exception.
- **Performance save DC:** 8 + normal character proficiency bonus + Charisma modifier. A save succeeds when its total reaches DC. “Fails by 10” means total at most DC −10; a natural 1 alone does not supply that margin. These card-specific riders do not replace other Core Systems degree rules.
- **Voice and targets:** starting or maintaining a performance requires consciousness, freedom to act and an audible voice or instrument. Silence prevents it. Unless a card states an exception, affected creatures must hear you and be within its range when affected. Choose creatures/points you can perceive with an unobstructed line of effect; total cover blocks the effect. “Ally” can include you unless it says OTHER. A creature cannot count twice in one target list. Zones remain at their chosen point; creatures inside must also hear you. Range for a zone means range to its center.
- **Tags govern interactions:** verse, chant, echo, healing, sustained and so on are printed on cards. Names do not create tags. A Symphony is not automatically a Chant. Death-triggered Crescendo of Hope has its own explicit exception to normal activation requirements.

## Crescendo and rhythm

Begin and end each encounter with 0 Crescendo and no last performance. Only started abilities tagged **performance** can generate or spend it. The Director identifies a real encounter; rehearsing against willing targets or performing outside an encounter cannot stockpile Crescendo. Performances outside encounters still cost RP and obey other limits.

Starting a different named performance from your last started performance gains 1 Crescendo, up to 5, at most once on your own regular turn. The first performance of an encounter qualifies. Ordinary spells, weapon attacks and turns without performing leave the identity of the last started performance unchanged. Consequently Verse → ordinary spell → same Verse does not count as variety. Maintenance, Echo resolution, items and passive triggers grant no stacks. Explicit accelerators raise the gain ceiling to 2 on that turn; multiple accelerators never stack beyond 2. Extra turns do not provide another gain allowance.

**At 5 stacks:** your next started performance spends all 5, vents 2 Dissonance (minimum 0), and applies its printed Crescendo rider. It grants no replacement stack. An explicit spend-all cost replaces this automatic expenditure: never pay twice. Spending only 3 or 4 on Harmonic Convergence does not vent or activate a five-stack rider. The consuming performance becomes the last performance started. Costs and stack spending occur before attack/save resolution; a miss or successful save does not refund them.

**Before paying anything, validate the complete activation:** you know the feature; meet its level/path and source conditions; have legal targets, voice, the required Action/Bonus Action, recharge readiness, available per-rest uses, RP and required Crescendo. An illegal attempt spends nothing and vents nothing. A paid legal attempt sets its recharge and spends its per-rest use even if its targets resist.

Taking damage resets Crescendo and last performance after the damage resolves, unless you know Fluid Tempo. Silence, incapacitation or a failed concentration save resets them even with Fluid Tempo. Declaring the end of an encounter never restores RP, Dissonance, HP or limited uses. Pending Echoes and sustained performances still resolve or expire normally; they cannot restart encounter rhythm.

## RP, ordinary spells and recovery

Every printed performance RP cost comes from the **same Resonance Point pool used by your ordinary spells**. Performances are magical class techniques; they are not spell-rank casts. They cannot use Overcast, automatic spell discounts or spell-casting triggers. They generate no Dissonance unless expressly stated. None of these 50 cards adds Dissonance. An audible performance is still a Weave ability, so performing or maintaining one does not qualify for a quiet turn's passive Dissonance reduction.

The progression table uses Core Systems Known Descent V2's Bard capacity. Ordinary spell rank costs from that source are 0/2/3/5/7/10/13/17/21/26 RP for ranks 0–9; Grand costs 32. This lists the global cost table, **not permission for a Bard to learn every rank**. Ordinary spells neither gain nor spend Crescendo and cannot become Echo sources. Use the character's separately reconciled spell repertoire; this module grants no spells or extra spell selections.

For this focused test, retain the recovered Player Rulebook rest formula: Retune restores one-quarter maximum RP plus actual casting modifier, capped at maximum; use the existing helper's nearest-integer rounding of the quarter and a minimum recovery of 0. Retune resets Dissonance. A long rest restores all RP and clears Dissonance. Short-rest uses refresh after a completed short or long rest; long-rest uses only after a completed long rest. Use the expedition's rest opportunities and time costs. Do not treat a pause between fights as a free rest. Optional meditation and external RP effects follow their own existing rules.

**Known integration conflict:** the old companion helper derives a smaller Bard pool and uses rank ×2 spell costs. The older Resonance prose also differs from Core V2's spellcasting/Burn presentation. This pilot uses Core V2's explicit capacity/cost tables, retains the protected five-stack Dissonance vent, and does not silently rewrite the game's full ordinary-spell risk system. Resolve that broader conflict before merging into the app or using an unrestricted mixed-class campaign. To isolate this module in a first test, use performances and ordinary weapon actions, and log any ordinary spells separately.

## Actions, recharge and concentration

Take your normal Action and only one Bonus Action when a feature permits it. Maintenance or an Echo can compete for that Bonus Action. An extra full Action never provides another Bonus Action or Reaction. All sources share a maximum of one additional full Action per creature per round. Additional Actions cannot generate further Actions; grants expire at their stated deadline and never queue across rounds.

After a performance resolves, set its round-recharge counter to the printed N. Decrease it once at the start of your regular initiative turn, even if Stunned or incapacitated; extra turns and extra Actions do not tick it. Counter 0 means available. Recharge 2 used on turn 1 becomes ready on turn 3. Outside initiative, each elapsed 6 seconds decreases the counter by 1; do not double-count elapsed time and turn ticks. Ending an encounter does not clear it immediately.

Only a positive counter can be reset or shortened. Each ability can receive at most one reset/shortening per round across all sources. An invalid zero-counter target does not expend the reset feature. A reset grants no Action, RP or restored per-rest use.

All **sustained** Bard effects share the ordinary single concentration slot with spells. Starting a new sustained effect ends the old one immediately. Damage prompts a Constitution save against max(10, damage divided by 2). For this pilot, round that half down to a whole-number DC; this makes the rounding explicit rather than claiming the source specified it. Failure ends the effect and breaks rhythm. Silence or incapacitation ends an audible sustained effect. You may voluntarily end it at any time, without a residual benefit unless a known feature explicitly grants one.

The initial activation is turn 1. On turns 2 and 3, pay the printed maintenance RP and a Bonus Action by the end of your turn; pulse effects resolve immediately on payment. You can maintain only once per regular turn. Missing that payment ends the effect at the end of that turn. It otherwise ends at the start of turn 4, with no fourth pulse. Individual printed bonuses may expire earlier. Maintenance never counts as starting a performance or retriggers start-only effects. Song of Serenity and Dissonant Pulse are explicit maintenance exceptions, each with its own limit.

Symphony of Mastery's special Bonus Action can keep its acceleration through that performance, then ends the Symphony if used on a later turn before maintenance. Starting a different concentration effect still ends it first. The Symphony's own start never receives its own acceleration.

## Healing, damage and Echoes

Roll damage or healing **once per effect/pulse** and apply that roll to each eligible target, unless a card calls for separate attacks/rolls. Separate performance attacks roll their damage separately. Apply each target's save, resistance, immunity and missing-HP limit separately. Round halved damage down. No healing exceeds maximum HP; temporary HP do not stack or remove Wounds. Same-stat bonuses from Bard performances use the strongest rather than adding together. Each creature receives a named healing Chant's healing at most once per round across all Bards. All sustained healing is finite and paid.

An Echo stores one explicitly **Echo-eligible** performance's unmodified immediate damage or healing dice, before Charisma, flat bonuses, extra critical dice, Signature Sound or Crescendo riders. On a critical hit, identify and record the ordinary base dice separately from the extra critical dice before rolling. The source must actually damage or heal a target. Record the chosen target and raw dice total; actual HP recovered may have been lower. Multi-target sources still provide only one target's numerical source per Echo component, never the entire target list. A single use of a multi-target performance is one source record, not several independent records. Sustained maintenance pulses are never eligible sources.

Default source memory is this turn or the previous regular Bard turn; Echo Harmonization extends that by one turn. Medley has its own previous-two-turn window, which the passive does not further extend. Sources retain a use ID to distinguish separate actual performances. Medley needs two distinct source records, each independently eligible; its wording also requires two different named performances.

Starting an Echo performance follows normal Crescendo rules; resolving it never does. Only one pending Echo package may exist; a new one replaces the old without refund. Resolve it automatically at the start of the next regular Bard turn, after recharge ticks. Explicit Echo-resolution exception: although resolution is not a started performance, you must remain conscious and capable of audible performance when it resolves. If you are silenced/incapacitated or no required target is eligible at that time, it fizzles without refund; it does not wait for a favorable target later. Its absolute expiry is the end of that turn. Default target is one original affected creature still within 30 feet, able to hear you, with line of effect. Discordant Echo explicitly allows a new enemy and conversion to psychic damage.

Add all copied fractions for each source, cap their sum at 100%, then round down **once**, with minimum 1 for a positive source/fraction. Thus a raw roll of 7 copied at 50%+25% produces 5, not two separately rounded packets. Reverb and Crescendo enhancements use that same cap. Medley's two sources are calculated separately but remain one pending package. Apply defenses and Discordant Echo's save after computing the copied amount.

Echoes copy no conditions, buffs, duration, movement, Actions, resources, cooldowns, finale effects, passives or other Echoes. They do not critically hit or start Bard/spell proc chains. Their damage still has ordinary consequences: concentration checks, damage reduction, Downed/death and rhythm interruption apply normally. Healing still follows ordinary living-target and maximum-HP rules.

## Acquisition and the level 1–20 example

Gain the core engine and starting kit automatically. At each scheduled choice, select a feature you do not already know, from the indicated band and at or below your **Bard class level**. Choose at least two actives at L1 and at least one at L3 and L10. You cannot bank or transfer a choice. No Skill Point currency is introduced. Do not also grant the older draft table's features.

At Bard 3 enter the **Virtuoso Arch**. At Bard 10 choose one Hero path: **Harmony** supports recovery/protection; **Virtuoso Hero** develops Echoes/tempo; **Discord** develops interference/control. Arch Virtuoso and Hero Virtuoso are different tiers. Hero selections must belong to your chosen path. There is no general retraining in this draft. Perfect Pitch is automatic at Bard 9; your chosen path's Finale is automatic at Bard 20 and cannot be selected early. ASI/feat milestones are separate from performance choices.

A Wizard 19/Bard 1 gets only Bard 1 acquisition/scaling, despite using normal total-character proficiency for attacks/DCs. It does not gain the Bard 5 Dissonant Note stun rider, Arch or Hero options. The RP table below is the single-class Bard table; do not add complete caster pools together for a multiclass character.

| Bard level | RP maximum | New choices | Harmony example | Separate grant |
|---:|---:|---|---|---|
| 1 | 2 | 4 from Base | Verse of Courage, Chant of Renewal, Dissonant Note, Echo of Inspiration | Core engine and starting kit |
| 2 | 3 | 2 from Base | Verse Mastery, Lingering Notes | — |
| 3 | 5 | 2 from Arch | Virtuoso's Verse, Resonant Chant | Virtuoso Arch |
| 4 | 7 | 1 from Base / Arch | Signature Sound | ASI or eligible feat |
| 5 | 9 | 1 from Arch | Cascading Echo | — |
| 6 | 11 | 1 from Base / Arch | Chorus Shield | — |
| 7 | 14 | 1 from Arch | Tempo Control | — |
| 8 | 17 | 1 from Base / Arch | Verses Unbound | ASI or eligible feat |
| 9 | 20 | 1 from Arch | Harmonic Convergence | Perfect Pitch |
| 10 | 23 | 2 from Hero | Healing Harmony, Protective Verse | Choose one Hero path |
| 11 | 26 | 1 from Base / Arch | Melodic Instinct | — |
| 12 | 29 | 1 from Hero | Chorus of Renewal | ASI or eligible feat |
| 13 | 32 | 1 from Base / Arch | Echo Harmonization | — |
| 14 | 35 | 1 from Hero | Inspiring Performance | — |
| 15 | 38 | 1 from Base / Arch | Bardic Knowledge | — |
| 16 | 41 | 1 from Hero | Symphony of Serenity | ASI or eligible feat |
| 17 | 44 | 1 from Base / Arch | Fluid Tempo | — |
| 18 | 47 | 1 from Hero | Song of Serenity | — |
| 19 | 50 | 1 from Base / Arch | Performance Focus | ASI or eligible feat |
| 20 | 54 | None | — | Chosen Hero finale |

This example reaches 25 selected features plus Perfect Pitch and Crescendo of Hope: **27 known features**, not all 50. It intentionally illustrates legal choices rather than an optimized build. Fluid Tempo may be taken much earlier if you value damage protection.

## All 50 ability cards

### Base Bard

#### Verse Mastery

**Bard 1 · passive · selection** | `bard.base.verse-mastery`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Once on each of your turns, add 1 to the damage dealt to one target by a directly performed Verse. This is a flat bonus, not a damage die; Echoes never inherit it.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Lingering Notes

**Bard 1 · passive · selection** | `bard.base.lingering-notes`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

When a sustained Chant ends before its final scheduled pulse, mark one ally affected by its last pulse. At the start of your next turn, if that ally is within 30 feet and can hear you, it gains C temporary HP for 1 round. This residual note restores no HP, uses no concentration, and triggers no other Bard effects. Silence or incapacitation cancels it; only one residual note can wait at a time.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Melodic Instinct

**Bard 1 · passive · selection** | `bard.base.melodic-instinct`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Gain +1 initiative and +5 feet walking Speed. Multiple copies of this feature do not stack.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Echo Harmonization

**Bard 1 · passive · selection** | `bard.base.echo-harmonization`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

An eligible source performance remains available to your Echo features for one additional Bard turn: this turn or either of your previous two turns. This extends source memory, not copied conditions, packet expiry or the duration of any effect.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Performance Focus

**Bard 1 · passive · selection** | `bard.base.performance-focus`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Once per round, after you spend 5 Crescendo, reduce the positive round-recharge counter of one OTHER Bard performance by 1, minimum 0. This counts as that ability's one allowed reset/shortening for the round. It cannot restore per-rest uses, RP, an Action or the performance just used.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Bardic Knowledge

**Bard 1 · passive · selection** | `bard.base.bardic-knowledge`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Choose History or Performance. Gain proficiency in that skill, or expertise if already proficient. When examining a song, oral tradition or historic performance for 10 minutes, you may make an Intelligence (History) check even without a library. The Director sets the ordinary knowledge DC; failure grants no invented fact.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Verse of Courage

**Bard 1 · active · selection** | `bard.base.verse-of-courage`

**Activation:** Action. **Cost:** 0 RP. **Frequency:** At will, subject to costs.
**Range:** 60 ft (self/trigger where stated). **Target:** One enemy; one other ally within 30 feet. **Duration:** Instantaneous.
**Resolution:** Performance attack vs AC. **Tags:** verse, damage, support, performance. **Echo source:** initial dice only.

Make a performance attack against one enemy. On a hit, deal S d6 psychic damage. Whether you hit or miss, choose one other ally within 30 feet; its next successful weapon attack before the end of your next turn deals +1 damage. The encouragement does not stack with itself.

**Five-stack rider:** The encouraged ally also gains advantage on its next saving throw before the end of your next turn. No additional damage is copied by an Echo.

#### Chant of Renewal

**Bard 1 · active · selection** | `bard.base.chant-of-renewal`

**Activation:** Action. **Cost:** 2 RP; maintenance 1 RP + Bonus Action. **Frequency:** At will, subject to costs.
**Range:** 15 ft (self/trigger where stated). **Target:** One living ally per pulse, including yourself. **Duration:** Concentration, at most 3 Bard turns.
**Resolution:** None. **Tags:** chant, healing, sustained, performance. **Echo source:** initial dice only.

On starting and on each paid maintenance pulse, one living ally within 15 feet regains 1d6+C HP. You may choose a different ally each pulse. There are at most 3 pulses, including the initial pulse. A creature can benefit from this named Chant only once per round across all Bards. This never removes Wounds or restores life.

**Five-stack rider:** The initial recipient also gains C temporary HP for 1 round; subsequent pulses are unchanged.

#### Echo of Inspiration

**Bard 1 · active · selection** | `bard.base.echo-of-inspiration`

**Activation:** Bonus Action. **Cost:** 1 RP. **Frequency:** Recharge 2 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** One original target of one eligible source. **Duration:** Instantaneous.
**Resolution:** None. **Tags:** echo, performance. **Echo source:** no.

Create one pending Echo package using the immediate, unmodified damage OR healing dice of one eligible performance you resolved this turn or on your previous turn. At the start of your next turn, repeat 50% of that stored dice total, rounded down, to one of its original affected targets still within 30 feet. A positive fraction has minimum 1. Apply current resistance/immunity to damage and the ordinary missing-HP limit to healing.

**Five-stack rider:** Increase the copied fraction by 25 percentage points, subject to the 100% package cap. This copies no Crescendo rider or other trigger.

#### Dissonant Note

**Bard 1 · active · selection** | `bard.base.dissonant-note`

**Activation:** Action. **Cost:** 1 RP. **Frequency:** Recharge 2 rounds.
**Range:** 60 ft (self/trigger where stated). **Target:** One enemy. **Duration:** Instantaneous.
**Resolution:** Wisdom; then Constitution concentration if applicable. **Tags:** control, performance. **Echo source:** no.

The enemy makes a Wisdom save. On failure it loses its Reaction until the start of your next turn. If it is concentrating, it also makes a Constitution concentration save against your performance DC; failure ends its sustained effect. Success on the Wisdom save prevents both effects.

**Five-stack rider:** Beginning at Bard class level 5, if the Wisdom save fails by 10 or more, the target is also Stunned until the end of its next turn. A natural 1 alone does not substitute for this margin.

### Arch Virtuoso

#### Fluid Tempo

**Bard 3 · passive · selection** | `bard.arch.fluid-tempo`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Taking damage alone no longer resets your Crescendo. You still make concentration saves for sustained effects; failing one ends that effect and resets Crescendo. Silence and incapacitation still break rhythm.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Verses Unbound

**Bard 3 · passive · selection** | `bard.arch.verses-unbound`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Once on each of your turns, a natural 19 that hits with a Verse performance attack is a critical hit. Natural 20s already follow Core Systems critical rules. Double the rolled damage dice once, never multiply a critical again; flat bonuses are unchanged.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Chorus Shield

**Bard 3 · passive · selection** | `bard.arch.chorus-shield`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

When you START a Chant, you and one other ally within 15 feet each gain C temporary HP until the start of your next turn. Maintenance, residual notes and Echoes cannot trigger it. Temporary HP never stack.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Signature Sound

**Bard 3 · passive · selection** | `bard.arch.signature-sound`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Choose Fire, Cold or Lightning when acquiring this feature. Once on each of your turns, after a Verse hits a target, deal 1d4 additional damage of that type to that target. This bonus is not part of an Echo source. The element is fixed unless a later retraining rule permits a change.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Perfect Pitch

**Bard 9 · passive · automatic** | `bard.arch.perfect-pitch`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

After spending 5 Crescendo on a Verse, choose one creature directly hit by it. Until the end of your next turn, your own directly performed Verses ignore that creature's resistance to psychic damage and your Signature Sound element, if any. Immunity remains immunity. Echoes and ordinary spells do not benefit.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Virtuoso's Verse

**Bard 3 · active · selection** | `bard.arch.virtuoso-s-verse`

**Activation:** Action. **Cost:** 2 RP. **Frequency:** Recharge 2 rounds.
**Range:** 60 ft (self/trigger where stated). **Target:** One enemy. **Duration:** Instantaneous.
**Resolution:** Performance attack vs AC. **Tags:** verse, damage, performance. **Echo source:** initial dice only.

Make a performance attack against one enemy. On a hit deal (S+1)d6 psychic damage. If you know Signature Sound, add its ordinary once-per-turn bonus and apply the chosen element rider until the start of your next turn: Fire prevents reactions; Cold reduces Speed by 10 feet, minimum 0; Lightning prevents opportunity attacks. No element rider applies without Signature Sound.

**Five-stack rider:** Add 1d6 psychic damage on a hit. This bonus is excluded from the Echo source.

#### Resonant Chant

**Bard 3 · active · selection** | `bard.arch.resonant-chant`

**Activation:** Action. **Cost:** 3 RP; maintenance 2 RP + Bonus Action. **Frequency:** Recharge 3 rounds.
**Range:** 15 ft (self/trigger where stated). **Target:** Up to two living allies per pulse. **Duration:** Concentration, at most 3 Bard turns.
**Resolution:** None. **Tags:** chant, healing, sustained, performance. **Echo source:** initial dice only.

On starting and each paid maintenance pulse, choose up to two living allies within 15 feet. Each regains 1d6+C HP and gains +1 AC until the start of your next turn. At most 3 pulses total. The AC bonus does not stack with another Bard performance AC bonus; each creature receives this named Chant's healing at most once per round.

**Five-stack rider:** One initial recipient may immediately end the Frightened condition on itself.

#### Cascading Echo

**Bard 5 · active · selection** | `bard.arch.cascading-echo`

**Activation:** Action. **Cost:** 3 RP. **Frequency:** Recharge 3 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** One original target. **Duration:** Instantaneous.
**Resolution:** None. **Tags:** echo, performance. **Echo source:** no.

Create one pending package from one eligible performance resolved this turn or your previous turn. At the start of your next turn, copy an aggregate 75% of its unmodified immediate dice total, rounding down once with minimum 1 for a positive total. The result affects one original target within 30 feet and counts as one Echo event. No new attack roll, critical or Bard/spell proc trigger occurs.

**Five-stack rider:** Increase the total fraction by 25 percentage points, up to the common 100% cap. Resolve additional fractions within the same package and expiry.

#### Tempo Control

**Bard 7 · active · selection** | `bard.arch.tempo-control`

**Activation:** Action. **Cost:** 2 RP. **Frequency:** Recharge 3 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** One ally and one enemy. **Duration:** Instantaneous.
**Resolution:** Enemy Wisdom save. **Tags:** tempo, control, performance. **Echo source:** no.

Choose one ally and one enemy within 30 feet. The ally gains +10 feet Speed until the end of your next turn. The enemy makes a Wisdom save; on failure it loses 10 feet Speed, minimum 0, for the same duration. This grants no extra action, attack, Bonus Action or Reaction.

**Five-stack rider:** The ally may immediately move up to 10 feet without provoking opportunity attacks. This movement is not an Action.

#### Harmonic Convergence

**Bard 9 · active · selection** | `bard.arch.harmonic-convergence`

**Activation:** Action. **Cost:** 3 RP; spend all Crescendo (minimum 3). **Frequency:** Recharge 3 rounds.
**Range:** 15 ft (self/trigger where stated). **Target:** Up to three enemies and three living allies. **Duration:** Instantaneous.
**Resolution:** Enemy Wisdom saves, half damage on success. **Tags:** burst, healing, performance. **Echo source:** no.

Requires at least 3 Crescendo; spend all current stacks, K. Up to three enemies within 15 feet make Wisdom saves, taking S d6 psychic damage on failure or half on success. Up to three living allies within 15 feet regain C+K HP. No creature is both an enemy and an ally for this use. This is not Echo-eligible.

**Five-stack rider:** At exactly 5 spent, add 1d6 to the damage roll. The universal 2-Dissonance vent occurs once; the cost is not paid twice.

### Hero — Harmony

#### Song of Serenity

**Bard 10 · passive · selection** | `bard.harmony.song-of-serenity`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

When you START a healing Chant, mark one of its initial recipients. Immediately after you pay maintenance on either of your next two turns, that creature regains 2 HP, provided it is living, within 15 feet and can hear you. Each named Chant can mark only one creature per use. This rider cannot Echo or trigger further healing effects.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Cleansing Verse

**Bard 10 · passive · selection** | `bard.harmony.cleansing-verse`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

After a performance spends 5 Crescendo, choose up to two living allies within 30 feet. Each immediately ends either Frightened or Charmed. It does not remove curses, Wounds, disease or poison. The cleanse occurs once per expenditure, not once per target of the performance.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Echo of Light

**Bard 10 · passive · selection** | `bard.harmony.echo-of-light`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

When you START an Echo performance, choose one living ally within 30 feet. The next non-Echo healing performance you directly use on that ally before the end of your next turn restores 2 extra HP. This benefit does not stack and cannot be part of an Echo source.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Divine Chorus

**Bard 14 · passive · selection** | `bard.harmony.divine-chorus`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Count Bard turns on which you start a qualifying performance and finish that turn with at least 1 Crescendo; count at most once per Bard turn. On the third such turn, reset the count and you may spend 3 RP to grant one OTHER ally within 30 feet one additional full Action usable on its next turn. It expires at the end of that turn. All grants share the one-additional-Action-per-round limit and never queue or stack. The additional Action cannot grant another Action. Reset the counter at encounter end or when rhythm breaks.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Crescendo of Hope

**Bard 20 · active · automatic** | `bard.harmony.crescendo-of-hope`

**Activation:** Triggered. **Cost:** 0 RP. **Frequency:** 1/long rest.
**Range:** 30 ft (self/trigger where stated). **Target:** Up to six OTHER living allies. **Duration:** Instantaneous.
**Resolution:** None. **Tags:** finale, healing. **Echo source:** no.

Once per long rest, immediately when you die, your final note lets up to six living allies within 30 feet regain 4d8+Bard level HP. This can lift Downed allies but cannot restore the dead, remove Wounds, prevent your death or affect you. It is not triggered merely by reaching 0 HP. This death-triggered exception needs no Action, RP, voice or consciousness and cannot Echo, generate resources or trigger other Bard effects.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Healing Harmony

**Bard 10 · active · selection** | `bard.harmony.healing-harmony`

**Activation:** Action. **Cost:** 4 RP. **Frequency:** Recharge 2 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** Up to two living allies. **Duration:** Instantaneous.
**Resolution:** None. **Tags:** healing, performance. **Echo source:** initial dice only.

Choose up to two living allies within 30 feet. Each regains S d8+C HP and may end Frightened. This never removes Wounds or restores the dead. Only the unmodified dice rolled for one recipient can be an Echo source.

**Five-stack rider:** One recipient also ends Charmed.

#### Protective Verse

**Bard 10 · active · selection** | `bard.harmony.protective-verse`

**Activation:** Action. **Cost:** 3 RP. **Frequency:** Recharge 2 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** One living ally. **Duration:** 1 minute or until expended.
**Resolution:** None. **Tags:** verse, ward, performance. **Echo source:** no.

One living ally gains (S+1)d6+C temporary HP for 1 minute and advantage on the next saving throw it makes against Frightened, Charmed or Stunned during that minute. The saving-throw benefit then ends. Temporary HP follow the normal non-stacking rule.

**Five-stack rider:** A second living ally within 30 feet gains C temporary HP for 1 minute, but not the saving-throw benefit.

#### Chorus of Renewal

**Bard 12 · active · selection** | `bard.harmony.chorus-of-renewal`

**Activation:** Action. **Cost:** 8 RP; spend all Crescendo (minimum 5). **Frequency:** Recharge 4 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** Up to six living allies. **Duration:** Instantaneous.
**Resolution:** None. **Tags:** healing, burst, performance. **Echo source:** no.

Requires and spends 5 Crescendo. Up to six living allies within 30 feet each regain S d8+C+5 HP. It never removes Wounds or restores life and cannot Echo.

**Five-stack rider:** The required expenditure funds the listed healing and the universal Dissonance vent; there is no additional rider or second expenditure.

#### Inspiring Performance

**Bard 14 · active · selection** | `bard.harmony.inspiring-performance`

**Activation:** Action. **Cost:** 4 RP; maintenance 1 RP + Bonus Action. **Frequency:** Recharge 4 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** Up to three allies chosen on start. **Duration:** Concentration, at most 3 Bard turns.
**Resolution:** None. **Tags:** sustained, support, performance. **Echo source:** no.

Choose up to three allies within 30 feet. For up to 3 Bard turns while sustained, each gains +1 to attack rolls, AC and saving throws while within 30 feet and able to hear you. Bonuses from multiple Bard performances of the same type do not stack. Pay 1 RP and a Bonus Action on each later turn to maintain it; there is no extra Action grant.

**Five-stack rider:** The chosen allies also gain C temporary HP until the start of your next turn.

#### Symphony of Serenity

**Bard 16 · active · selection** | `bard.harmony.symphony-of-serenity`

**Activation:** Action. **Cost:** 10 RP; maintenance 2 RP + Bonus Action. **Frequency:** 1/long rest.
**Range:** 30 ft (self/trigger where stated). **Target:** 15-foot-radius zone; four allies and three enemies per pulse. **Duration:** Concentration, at most 3 Bard turns.
**Resolution:** Enemy Wisdom saves. **Tags:** sustained, zone, healing, performance. **Echo source:** no.

Create a fixed 15-foot-radius zone centered at a point within 30 feet. On starting and each paid maintenance pulse, up to four living allies in the zone regain 1d8+C HP. At each pulse choose up to three enemies in the zone; each makes a Wisdom save. A failure prevents that enemy from making opportunity attacks until the start of your next turn. The zone lasts at most 3 pulses. This does not stop ordinary attacks or erase Wounds.

**Five-stack rider:** The initial healing recipients also gain advantage on their next saving throw before the start of your next turn.

### Hero — Virtuoso

#### Echo Reverb

**Bard 10 · passive · selection** | `bard.virtuoso.echo-reverb`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

When you create an Echo package, add one 25% portion of the source's unmodified stored dice total. This stays in the same package, resolves with it and respects the 100% total cap per source. It never creates an Echo from an Echo or changes expiry.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Chant Cascade

**Bard 10 · passive · selection** | `bard.virtuoso.chant-cascade`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Once per round when you START a Chant, you may reset the positive round-recharge counter of one OTHER Verse you used since the start of your previous turn to 0. It counts as that ability's one reset/shortening for the round. It restores no per-rest use or resource and grants no Action. Maintenance cannot trigger it.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Encore

**Bard 10 · passive · selection** | `bard.virtuoso.encore`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** 1/short rest.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Once per short rest, you may, after resolving a Bard performance whose round-recharge counter is positive, reset that counter to 0 if it has not been reset or shortened this round. No per-rest use, Action or resource is refunded. Cannot affect a Finale.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Tempo Theft

**Bard 10 · passive · selection** | `bard.virtuoso.tempo-theft`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Once on each of your turns, if at least one enemy fails a save against a Chant you started or maintained that turn, gain +10 feet Speed until the end of that turn. The number of enemies does not multiply it; it grants no Action, attack or Reaction.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Grand Performance

**Bard 20 · active · automatic** | `bard.virtuoso.grand-performance`

**Activation:** Action. **Cost:** 8 RP; spend all Crescendo (minimum 5). **Frequency:** 1/long rest.
**Range:** 30 ft (self/trigger where stated). **Target:** Up to six OTHER allies. **Duration:** Instantaneous.
**Resolution:** None. **Tags:** finale, additional-action, performance. **Echo source:** no.

Requires and spends 5 Crescendo, your NORMAL Action, and 8 RP. Choose up to six OTHER allies within 30 feet. Each may take one additional full Action on its next turn, expiring at the end of that turn. Shared additional-Action limits apply; grants do not stack or queue. An additional Action cannot trigger this performance or grant another Action. No target immediately acts out of turn.

**Five-stack rider:** The required 5-stack expenditure funds the listed effect and vents 2 Dissonance once; no additional rider.

#### Masterful Verse

**Bard 10 · active · selection** | `bard.virtuoso.masterful-verse`

**Activation:** Action. **Cost:** 4 RP. **Frequency:** Recharge 2 rounds.
**Range:** 60 ft (self/trigger where stated). **Target:** Up to two distinct enemies. **Duration:** Instantaneous.
**Resolution:** Separate performance attacks vs AC. **Tags:** verse, damage, performance. **Echo source:** initial dice only.

Make a separate performance attack against each of up to two distinct enemies within 60 feet. Each hit deals (S+1)d6 psychic damage. If both hit and this is a different named performance from your last started performance, increase its normal Crescendo gain by 1, to a maximum of 2 total gained on your turn. It gains no stacks if it consumed Crescendo. An Echo may store the unmodified dice of only one hit.

**Five-stack rider:** Add 1d6 psychic damage to one hit; do not also gain Crescendo.

#### Tempo Manipulation

**Bard 10 · active · selection** | `bard.virtuoso.tempo-manipulation`

**Activation:** Action. **Cost:** 4 RP. **Frequency:** Recharge 3 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** Up to two allies and two enemies. **Duration:** Instantaneous.
**Resolution:** Enemy Wisdom saves. **Tags:** tempo, control, performance. **Echo source:** no.

Choose up to two allies and two enemies within 30 feet. Allies gain +10 feet Speed until the end of your next turn. Each enemy makes a Wisdom save; failure reduces its Speed by 10 feet, minimum 0, and prevents reactions for the same duration. No additional Action or attack is granted.

**Five-stack rider:** One chosen ally may immediately move up to its Speed without provoking opportunity attacks; this movement is not an Action.

#### Virtuoso's Medley

**Bard 12 · active · selection** | `bard.virtuoso.virtuoso-s-medley`

**Activation:** Action. **Cost:** 5 RP. **Frequency:** Recharge 3 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** One original target per eligible source. **Duration:** Instantaneous.
**Resolution:** None. **Tags:** echo, performance. **Echo source:** no.

Select two different eligible source performances you resolved during this turn or your previous two turns. This two-turn memory is an explicit Medley exception, independent of Echo Harmonization; that passive does not extend it further. Create ONE pending package that repeats 50% of each source's immediate unmodified damage OR healing dice at the start of your next turn. Each source affects one of its own original targets within 30 feet. Per-source 100% caps, common expiry and all Echo prohibitions still apply. You need two actual eligible sources; naming abilities you have not used is insufficient.

**Five-stack rider:** Increase each source's copied fraction by 25 percentage points, up to 100% per source.

#### Harmonic Resonance

**Bard 14 · active · selection** | `bard.virtuoso.harmonic-resonance`

**Activation:** Action. **Cost:** 5 RP; maintenance 2 RP + Bonus Action. **Frequency:** Recharge 4 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** 10-foot-radius fixed zone, up to three creatures per pulse. **Duration:** Concentration, at most 3 Bard turns.
**Resolution:** Discordant mode: Wisdom saves. **Tags:** sustained, zone, performance. **Echo source:** no.

Create one fixed 10-foot-radius zone within 30 feet, choosing Ward or Discordant mode on start. At the initial pulse and each paid maintenance pulse, Ward grants up to three allies in the zone C+S temporary HP until the start of your next turn; Discordant makes up to three enemies attempt Wisdom saves, taking S d6 psychic damage on failure or half on success. Mode is fixed for the use. At most 3 pulses; this is not a Chant and is not Echo-eligible.

**Five-stack rider:** On the initial pulse only, Ward adds C temporary HP or Discordant adds 1d6 damage to the roll. This rider does not repeat.

#### Symphony of Mastery

**Bard 16 · active · selection** | `bard.virtuoso.symphony-of-mastery`

**Activation:** Action. **Cost:** 8 RP; maintenance 1 RP + Bonus Action. **Frequency:** 1/long rest.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** Concentration, at most 3 Bard turns.
**Resolution:** None. **Tags:** sustained, tempo, performance. **Echo source:** no.

For up to 3 Bard turns while sustained, your first qualifying, non-consuming performance started AFTER this Symphony on your own turn gains 2 Crescendo instead of 1. Starting the Symphony itself follows the ordinary one-stack rule. Total Crescendo gain remains capped at 2 per Bard turn, even with Masterful Verse. Once during the duration, you may start one non-Finale performance that normally takes an Action as a Bonus Action, paying its full RP and recharge costs. Using that Bonus Action leaves none to maintain this Symphony that turn; if it is a later turn before maintenance, the Symphony remains active through that performance (including its accelerated gain), then immediately ends. Starting another concentration effect still ends the Symphony immediately, before the new effect resolves. It never grants an extra Action.

**Five-stack rider:** Reduce one OTHER performance's positive round-recharge counter by 1, subject to the single reset/shortening cap. Per-rest uses remain spent.

### Hero — Discord

#### Dissonant Pulse

**Bard 10 · passive · selection** | `bard.discord.dissonant-pulse`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Once on each of your turns after you START or pay to maintain a Chant, one enemy within 15 feet takes 1d6 psychic damage. It must be able to hear you. This separate rider cannot critically hit, Echo or trigger further Bard effects; apply resistance and immunity normally.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Cacophony

**Bard 10 · passive · selection** | `bard.discord.cacophony`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

Once on each of your turns, after a directly performed Verse damages an enemy, give it a -1 penalty to attack rolls until the end of your next turn. A later direct Verse can increase this to -2 and refresh the duration. Maximum -2 from all instances of Cacophony; Echoes cannot apply or refresh it.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Maddening Echo

**Bard 10 · passive · selection** | `bard.discord.maddening-echo`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** Wisdom save. **Tags:** passive. **Echo source:** no.

Once on each of your turns when you START an Echo performance, choose one enemy within 30 feet. It makes a Wisdom save. On failure it has disadvantage on its next attack before the end of its next turn. Resolving the Echo does not trigger this feature. Multiple instances do not stack.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Twisted Chorus

**Bard 10 · passive · selection** | `bard.discord.twisted-chorus`

**Activation:** Passive. **Cost:** 0 RP. **Frequency:** Continuous/triggered as stated.
**Range:** 0 ft (self/trigger where stated). **Target:** Self. **Duration:** While known; individual riders last as stated.
**Resolution:** None. **Tags:** passive. **Echo source:** no.

After a performance spends 5 Crescendo and finishes resolving, choose up to three enemies within 30 feet. Each has -1 to saving throws until the end of your next turn. This cannot affect the triggering performance's saves, cannot stack with itself and cannot be applied by an Echo.

**Five-stack rider:** Not a started Performance; no Crescendo rider.

#### Dirge of Madness

**Bard 20 · active · automatic** | `bard.discord.dirge-of-madness`

**Activation:** Action. **Cost:** 8 RP; spend all Crescendo (minimum 5). **Frequency:** 1/long rest.
**Range:** 30 ft (self/trigger where stated). **Target:** Up to six enemies. **Duration:** Instantaneous.
**Resolution:** Wisdom saves; half damage and no Stunned on success. **Tags:** finale, control, damage, performance. **Echo source:** no.

Requires and spends 5 Crescendo and 8 RP. Up to six enemies within 30 feet make Wisdom saves. On failure each takes S d8+5d6 psychic damage and is Stunned until the end of its next turn. Success halves the damage and prevents Stunned. An immunity to Stunned does not remove the damage. This cannot Echo or extend an existing stun.

**Five-stack rider:** The required stack expenditure funds the printed damage and vents 2 Dissonance once; no additional rider.

#### Verse of Agony

**Bard 10 · active · selection** | `bard.discord.verse-of-agony`

**Activation:** Action. **Cost:** 3 RP. **Frequency:** Recharge 2 rounds.
**Range:** 60 ft (self/trigger where stated). **Target:** One enemy. **Duration:** Instantaneous.
**Resolution:** Performance attack vs AC. **Tags:** verse, damage, performance. **Echo source:** initial dice only.

Make a performance attack against one enemy. On a hit it takes S d6 psychic damage and, at the start of its next turn, 1d6 additional psychic damage. Until the end of that turn, the next HP healing it receives is reduced by C, minimum 0; then the reduction ends. Repeated uses refresh rather than stack the delayed damage and healing reduction. Only the initial unmodified damage dice are Echo-eligible.

**Five-stack rider:** On a hit, increase the delayed damage by 1d6. It remains excluded from Echoes.

#### Chant of Fear

**Bard 10 · active · selection** | `bard.discord.chant-of-fear`

**Activation:** Action. **Cost:** 3 RP; maintenance 2 RP + Bonus Action. **Frequency:** Recharge 3 rounds.
**Range:** 15 ft (self/trigger where stated). **Target:** Up to three enemies per pulse. **Duration:** Concentration, at most 3 Bard turns.
**Resolution:** Wisdom saves each pulse. **Tags:** chant, sustained, fear, performance. **Echo source:** no.

On starting and each paid maintenance pulse, choose up to three enemies within 15 feet. Each makes a Wisdom save. Failure makes it Frightened of you until the start of your next turn; success ends fear from this Chant. Each pulse is a new save, not an extension without a save. At most 3 pulses. It grants no forced movement and removes no whole turn.

**Five-stack rider:** One enemy that fails the initial save also loses reactions until the start of your next turn.

#### Discordant Echo

**Bard 12 · active · selection** | `bard.discord.discordant-echo`

**Activation:** Action. **Cost:** 3 RP. **Frequency:** Recharge 2 rounds.
**Range:** 30 ft (self/trigger where stated). **Target:** One enemy chosen on Echo resolution. **Duration:** Instantaneous.
**Resolution:** Wisdom save on resolution; half damage on success. **Tags:** echo, performance. **Echo source:** no.

Create one pending package from the immediate unmodified damage OR healing dice of one eligible performance from this turn or your previous turn. At the start of your next turn, choose one enemy within 30 feet. It makes a Wisdom save, taking 50% of the stored dice total as psychic damage on failure or half that result on success. This expressly permits a new enemy target and converts copied healing to damage, but copies no other effect or trigger. Standard package fractions and expiry apply.

**Five-stack rider:** Increase the copied fraction by 25 percentage points, subject to the 100% cap; it still allows a Wisdom save.

#### Mind-Rending Performance

**Bard 14 · active · selection** | `bard.discord.mind-rending-performance`

**Activation:** Action. **Cost:** 6 RP. **Frequency:** Recharge 3 rounds.
**Range:** 60 ft (self/trigger where stated). **Target:** One enemy. **Duration:** Instantaneous.
**Resolution:** Wisdom save; explicit failure-margin rider. **Tags:** control, damage, performance. **Echo source:** no.

One enemy makes a Wisdom save. On failure it takes (S+2)d6 psychic damage, loses reactions, and has disadvantage on its next attack before the end of its next turn. Success halves the damage and prevents both riders. On a failure by 10 or more, it is also Stunned until the end of its next turn. This is not Echo-eligible.

**Five-stack rider:** Add 1d6 to the damage roll before applying the saving-throw result; do not extend Stunned.

#### Symphony of Madness

**Bard 16 · active · selection** | `bard.discord.symphony-of-madness`

**Activation:** Action. **Cost:** 10 RP; maintenance 2 RP + Bonus Action. **Frequency:** 1/long rest.
**Range:** 30 ft (self/trigger where stated). **Target:** 15-foot-radius fixed zone; up to three enemies per pulse. **Duration:** Concentration, at most 3 Bard turns.
**Resolution:** Wisdom saves each pulse. **Tags:** sustained, zone, control, performance. **Echo source:** no.

Create a fixed 15-foot-radius zone within 30 feet. On starting and each paid maintenance pulse choose up to three enemies in it. Each makes a Wisdom save, taking S d6 psychic damage on failure or half on success. A failed target with an available Reaction must immediately use it to make one ordinary weapon attack against the closest OTHER creature that it can perceive and legally attack with a currently wielded weapon, within melee reach or normal ranged-weapon range (not long range); the Director breaks distance ties by a die roll. If no target is in range, it loses its Reaction until its next turn instead. The target keeps its ordinary turn; no forced spellcasting, movement or full Action occurs. At most 3 pulses, each with a new save.

**Five-stack rider:** One enemy failing the initial save also has disadvantage on its first attack on its next turn. This does not affect the immediate forced Reaction attack.

## Worked rhythm sequence

This is a deterministic timing example, not a combat simulation or a claim about hit rates. Use the printed Harmony example at **Bard 5**, CHA 16 (C3), PB3, attack +6, save DC14, S2, RP9. Suppose Dissonance begins at4, all listed targets are legal, the required attacks hit, and the Bard takes no damage or other interruption.

| Turn | Action / Bonus Action | Crescendo after turn | RP remaining | What happens |
|---:|---|---:|---:|---|
| 1 | Verse of Courage / Echo of Inspiration | 1 | 8 | Verse raw dice total7; Echo prepares 50%. Starting two different performances still gains only one normal stack. Last started is Echo. |
| 2 | Echo resolves; Verse of Courage | 2 | 8 | Echo deals3 before defenses. It gains nothing and does not repeat Verse Mastery or the encouragement. Verse differs from last started Echo. |
| 3 | Dissonant Note | 3 | 7 | New performance. It is not yet enhanced, so even a badly failed save supplies no Crescendo stun. |
| 4 | Verse of Courage | 4 | 7 | Verse differs from Note; source raw dice total9 recorded. |
| 5 | Dissonant Note | 5 | 6 | Reaching5 does not enhance this use. |
| 6 | Verse of Courage | 0 | 6 | Starting at5 consumes5 once, vents Dissonance4→2 and grants the encouraged ally the printed save advantage. No replacement stack. |
| 7 | Chant of Renewal | 1 | 4 | New performance, initial healing roll4+C3=7. Shared concentration begins. |
| 8 | Maintain Chant with Bonus Action; ordinary weapon Action | 1 | 3 | Paid second pulse; maintenance does not generate a stack or change last started Chant. |
| 9 | Maintain Chant with Bonus Action; ordinary weapon Action | 1 | 2 | Third and final paid pulse. Chant ends at start of turn10. |

If this Bard takes damage before learning Fluid Tempo, Crescendo resets even when a concentration check succeeds. If it fails the check, the Chant also ends. Spending the Bonus Action on Echo instead of maintenance ends the Chant at turn end. These are meaningful choices to test at the table.

## First table test and issue log

Use the [blank session log](BARD_PLAYTEST_SESSION_LOG.md) to record actual play.

Test one Hero build at a time with the same party, opponents and rest opportunities. Begin with L1 for basic costs; L5 for Echo/interruptions; L10 for path identity; L16 for sustained Symphonies; L20 for Finales. Build each character through the schedule, not by granting all cards. Use an encounter with mobile enemies, one with concentration/silence pressure, and a sequence of encounters without an intervening rest. Record actual play; automated checks do not establish balance.

| Record per session | What to capture |
|---|---|
| Setup | Date, players, Director, module version, Bard level/path, known features, CHA/PB, party, opposition, rest schedule |
| Each Bard turn | Action, Bonus Action, RP before/after, Crescendo before/after, last started performance, concentration, Echo source/amount, recharge changes |
| Results | Damage/healing/temp HP actually applied, prevented actions, failed/successful saves, ally extra Actions, five-stack uses, interruptions |
| Friction | Forgotten costs, disputed timing, dominant or unused choices, turns with no satisfying action |
| Decision | Keep, revise or retest; quote the exact card/rule and preserve old wording |

Priority balance questions: Can a low-level Bard reach five stacks often enough without Fluid Tempo? Are paid Chants worthwhile at the small initial RP pool? Does level16 Symphony of Mastery repay its setup/maintenance costs? Is Virtuoso Hero's extra-Action Finale too dominant compared with Harmony's death-triggered Finale? Do Discord's reaction denial and repeat saves leave opponents meaningful choices? Does a full day's recovery budget trivialize attrition? These remain questions, not passed tests.

## Sources, changes and validation

- **Recovered identity and original abilities:** approved [Player Rulebook V6](../../../../books/player/Decennium_Descent_Player_Rulebook_v6.docx); [UTF-8 extract](../../../../docs/reference/Player_Rulebook_v6_source_text.txt), Bard section lines1791–1940. The JSON retains every original description.
- **Capacity and ordinary spell costs:** [Core Systems Known Descent V2 data](../../../../data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json), as assigned by the [canon manifest](../../../../docs/canon/CANON_MANIFEST.json). Existing companion pool/cost drift remains an integration issue.
- **Scheduled acquisition direction:** [advancement proposal](ADVANCEMENT_PLAYTEST_PROPOSAL.md), advanced to this concrete Bard pilot after the owner's response. Bardic Knowledge is classified as passive; it was explicitly called passive under an Active heading.
- **New design:** all exact performance costs, die amounts, gates, finite durations, Echo restrictions, natural-19 crit extension and bounded Action/reset effects are draft decisions, not recovered historical approvals. Percentages and undefined effects were translated into explicit table rules while retaining source text.
- **Joint review:** [GPT's full-card review](../../../../docs/audit/2026-10-08/GPT_BARD_CARD_REVIEW.txt). Codex applied the timing, rounding, recharge, short-rest metadata, source-window and Bard-dip fixes. Tags already existed in data and are now visible on every card.
- **Executable checks:** [validation result](BARD_PLAYTEST_VALIDATION.json), [validator](../../tools/validate_bard_playtest.mjs), [reference helper](../../src/lib/bard-playtest.ts). They cover source mapping, selection paths, progression gates, resource transitions, Echo arithmetic and reset caps. They are not a full combat engine, balance simulation or live character-sheet integration.
- **Rebuild:** edit [the authoring source](../../tools/build_bard_playtest.py), then run it with Python; run the validator with Node24 or a runtime supporting TypeScript stripping. The guide and JSON are generated together. Approved books and frozen delivery packs remain unchanged.

Broader completion work remains in the [project readiness checklist](../../../../docs/audit/2026-10-08/READINESS.md): ordinary spell/risk reconciliation, the other classes, companion integration, public/Director boundaries and human campaign playtesting.

