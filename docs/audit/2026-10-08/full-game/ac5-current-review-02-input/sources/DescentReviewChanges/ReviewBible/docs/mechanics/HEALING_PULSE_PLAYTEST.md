# Healing pulses, sustained zones and upkeep

**REVIEWED / reference-VALIDATED in the supplied100+6-source scope.** The100 source candidates have individual roles in the [source register](HEALING_PULSE_SOURCE_BINDINGS.md); many are guards, one-time effects or already reviewed modifiers. The [boundary conference](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_BOUNDARIES.md) corrects the first proposals; the [exact final closure](../../../../docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_FINAL_CLOSURE.md) accepts89 targeted checks,301 reserve partitions and33 source-linked profile aliases. Original cards, books and the frozen class guide remain unchanged.

This overlay defines the supplied recurring-healing schedules. Each legal healing application still uses the [healing interface](HEALING_DEATH_PLAYTEST.md). Resource cost, pulse occurrence, actual HP restored and independent cure/resource components are different events.

Every internal schedule, native recurrence and cure-variant label has an [explicit source mapping](../../data/playtest/healing_pulse_profiles.json), checked by the [profile provenance report](HEALING_PULSE_PROFILE_PROVENANCE.json). These labels add no new spells or abilities. New integration decisions remain labeled separately from preserved source text.

## Keep the original clock

Use the original source or target regular-turn markers. Extra turns do not advance periodic healing, refill opportunities, generate upkeep, or reset these deadlines. Leaving/reentering initiative, reordering and source removal do not restart clocks.

Outside initiative preserve existing virtual markers. For activation at second2 with source starts0/6/12/18, later starts are6/12, not8/14. Establish one coherent six-second virtual schedule only when none exists. Bare outside-initiative round durations still use their separately reviewed absolute deadline; do not run both timing models for one component.

Ordinary start-expiry precedes start triggers. Explicit finite sequences own their printed due opportunities: Hemostasis's third target-start tick and Wound Eater IV's third source-start tick resolve before their sequence ends. A three-round target-start aura instead expires at its normal source deadline even if a creature received fewer than three pulses.

## Source schedules

Activation costs below are paid before the series exists; quoted later costs never refund an activation, limited use, BG, Ki, slot or Conviction.

| Source | First opportunity | Later opportunities and cost | End |
|---|---|---|---|
| Lifewell | Action4RP + all BG (at least3) establishes it; first same-turn heal still needs BA+1RP | Next2 regular source turns, each BA+1RP; fixed≤3 allies | Missed maintenance: that source turn end; otherwise startturn4 |
| Healing Briar | Action4RP includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies in fixed natural-ground zone | Same |
| Circle of Harmony | Action2Ki+3RP includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies in fixed zone | Same |
| Restoration Field | Action3RP + slot includes first heal | Next2 regular turns BA+1RP; repick≤3 living allies/functional devices | Same; this exact lifetime is a labeled default integration |
| Renewal Totem | Action2RP includes first heal | Next2 regular turns BA+1RP; repick≤3 allies | Same; Extended Totem adds one paid fourth turn and expires startturn5 |
| Sacred Chant | Action1RP includes nonhealing pulse1 | Next2 regular turns BA,0RP | Same; printed Conviction only, no invented healing |
| Sacrament / Dark Sacrament | Printed Action/Conviction/RP includes first pulse | Next2 regular turns BA+1RP, supplied by Cleric engine5 | Same; up to3 allies and3 qualifying enemies separately |
| Desecrated Ground | Action7RP includes first damage pulse | Next2 regular turns BA+1RP,≤3 enemies | Same; no healing output |
| Song of Mending | Action3RC includes pulse1, fixed≤3 allies | Source-next-regular-start pulse2 costs1RC; Enhanced adds second-later-start pulse3 for another1RC | Unpaid due pulse ends immediately; normal2/3-round duration otherwise |
| Unfinished Chorus | Action3RC includes first source-turn drain | One later regular source-turn drain costs1RC, no invented upkeep action; choose from the fixed zone set | Two-round deadline; missed upkeep ends that source turn |
| Transcendent Meditation | Action3Ki+4RP/short-rest use includes pulse1 | Next2 source regular starts, prepaid, fixed self+≤3 allies | Normal3-source-turn duration; concentration required |
| Eternal Bloom | Final Action/long-rest use; activation installment1 | Next2 source regular starts; prepaid installments2/3 | Normal3-round duration; no extraRC |
| Wound Eater IV | BA2RC establishes aura; first drain at next source regular start | Following2 source starts cost1RC each | After third pulse; unpaid later pulse ends at its due marker |
| Hemostasis | Pay printed additional1RP with eligible application | Next3 target regular starts, prepaid | After third opportunity |
| Cellular Reconstruction / Cleric Echoes | Printed activation/trigger stores one delayed event | Next source regular start, prepaid | After that opportunity; full stasis/copy rules are separately owned |
| Nano-Aegis Drone | Action2RP enters support mode; no immediate heal | Each legal BA command costs1RP; choose heal OR temporaryHP; at most3 total | Three-round mode; skipping command does not end mode |

All listed concentration requirements remain. Starting replacement concentration or becoming Incapacitated ends those effects immediately. An effect with no concentration requirement does not gain one merely because it is in this table. Incapacity still prevents required actions. A suppressed maintenance activation is illegal if the actual suppression says so; output suppression alone need not prevent an otherwise legal payment.

For ordinary paid three-pulse effects, maintenance must occur by the end of the corresponding regular source turn. Missing it ends the effect at that turn's end, with no later resumption. Lifewell also checks its activation turn. Paying early for a future turn is not permitted. A legal empty pulse can maintain a source that permits up toN targets; it consumes its cost and opportunity.

Song, Enhanced Song, Wound Eater IV and Oracle funded windows require later payment at their exact registered due marker. If that payment is unavailable or the upkeep is illegal then, the effect ends immediately at that marker. Later resources cannot retry it at the same marker. An early failed attempt at ordinary turn-window maintenance instead leaves that opportunity pending until its actual turn-end deadline. An extra-turn call is not a due regular marker and grants no payment, opportunity or automatic termination.

**Worked Lifewell example:** starting with12RP and3BG, activation plus first BA pulse spends5RP and all3BG, leaving7RP. Turn2 maintenance leaves6RP; turn3 leaves5RP. Losing the turn2 maintenance ends Lifewell that turn; neither the daily use nor first payments return.

## Oracle target-start windows

Garden, Resonant Seed and Burning Blood V have activation-funded window1. At each of the next two original source regular starts, pay1RC once to fund the next window, or end the effect. No upkeep action is invented. Each window ends at the following source regular start. Their persistent zones require concentration and fixed sets of at most3 allies and3 enemies, as applicable to each source.

Burning Blood V is a Curse Boon, separately gained alongside the Mystery Final; it receives no Final payment exemption. Its enemy-start damage does not turn its once-on-your-turn self-healing trigger into a heal on every enemy turn.

Crown Restored is a Final: its finite windows are prepaid, with no generic extraRC. Its fixed ally set contains at most3 including the Oracle if selected. A BA self-cast after that turn's start can give the Oracle only2 subsequent self-start heals before startturn4 expiry. Maximum3 per creature is a cap, not a promise.

Evaluate target-start effects on that target's original regular marker while it is eligible and inside the live zone. Both the funded window and numbered-round budget must be available. Entry/reentry or moving a Totem does not create entry healing. An ally that missed a start while outside loses that opportunity; it does not bank healing.

Oracle zone benefits use one fixed set across healing, floors, immunity and other aura benefits unless a source explicitly separates sets. Eternal Bloom's chosen≤3 living allies must be inside at activation; new entrants gain no reserve, floor or necrotic immunity. Selected targets regain applicable continuous benefits on legal reentry while the source remains active.

## Targets, payments and separate budgets

Declare legal recipients before rolling or learning outcomes. Fixed targets cannot be replaced. For repicked sources, select a new legal set for each pulse before its outcomes. Loss of eligibility after declaration skips that application without replacing it or refunding payment.

Where a source says each fixed target receives a pulse, resolve it for every currently eligible fixed target. The caller cannot arbitrarily omit one merely because the helper accepts a subset; subsets represent actual eligibility, not new selection permission.

Commit the legal upkeep action/resource and opportunity before HP resolution. Full HP, Decay and zero actual healing do not refund costs, restore a pulse, or allow a replacement target. Healing prohibition does not automatically suppress an independent printed cure. All source target restrictions, ally/enemy subcaps and clear line of effect remain caller responsibilities.

| Budget | Domain |
|---|---|
| Circle of Harmony | NEW global named effect + target + numbered round, across owners |
| Restoration Field | Field instance + target + numbered round |
| Oracle engine26 | Zone instance + target + numbered round, plus one application per funded window |
| Renewal + its Echo | One parent-family instance, one pulse ID, one up-to3 recipient budget and target/round ledger |
| Separate Renewal instances | No invented global once/round ceiling; simultaneous same-opportunity overlap uses the strongest legal branch |
| Nano-Aegis | Printed max3 commands per mode; caller enforces the applicable shared companion command limit |

A paid pulse at a distinct scheduled time from another independent Renewal can heal in the same round. Same-opportunity overlapping Renewal auras never add together.

Parent/Echo Renewal shares one upkeep payment, concentration and opportunity. From legal coverage, parent source base is2 and Echo source base is1. Construct the separate legal branches with correct modifier placement, select the stronger preview, then commit one healing application. Never add both or halve the already modified parent final heal. This is a source-specific new scheduling/arbitration integration; the existing Blight Totem reduction comparison is a different rule.

The scheduler takes each anchor's active/coverage state from the [reviewed device/Totem lifecycle](DEVICE_LIFECYCLE_PLAYTEST.md). The parent ending, including destruction, ends its dependent Echo administratively; ending Echo alone leaves the parent. Both anchors still share the original recipient/pulse budget and never supply six targets. Restoration Field is a slot effect with no fabricated HP-bearing machine anchor.

## Finite installments and independent components

Eternal Bloom records each chosen ally's missingHP at activation. Divide into3 integer installments; assign remainder to earlier pulses:10 becomes4/3/3,1 becomes1/0/0. At each scheduled opportunity consume the next installment. Outside, dead or suppressed targets lose it. Returning later never recovers the lost share, and new damage never grows the original reserve.

Bloom's once-per-selected-ally 1HP floor is separately tracked by the already reviewed survival interface. It neither consumes nor replenishes installments. The target must still be eligible and inside; full healing prohibition does not turn prevention into healing.

Garden gives a first-entry-or-start cure opportunity independent of HP gain. Seed's cure belongs to its first healing pulse, not entry. **New source-specific mastery integration, confirmed in exact review:** Enhanced Garden replaces this with its printed first-pulse cure-both opportunity, using one entitlement rather than granting both an entry cure and a second enhanced cure.

Transcendent Meditation's second pulse supplies its printed1Ki even if every HP gain is blocked. Suppressing the whole effect also suppresses Ki for that occurrence; suppressing only healing does not. No missed independent component is banked.

Hemostasis and other prepaid effects preserve each target/source clock. A late observation records missed opportunities without performing catch-up recovery.

Hemostasis permits only one such healing effect per target. Creating a separate series does not authorize stacking a second instance; the caller enforces active-effect eligibility. For Unfinished Chorus the fixed zone roster remains≤3 allies/3 enemies, but a drain chooses only one eligible enemy and one healing destination (self or one eligible ally) per pulse.

## Native recurrence and device limits

Aura of Grace, Living Pulse and Thief Exsanguinate retain their optional1RP regular-start heal and their printed eligibility gates. Regenerative Mutation, Bloodthick Node and Rapid Coagulation retain their real-encounter, mutation and movement gates and spend Mutation Recovery Reserve per actual HP restored. Bio-Stabilizer modifies Bloodthick; it is not another pulse.

These native effects have no generic three-pulse ceiling. Extra turns provide no new periodic recovery tick. Explicit restrictions on Downed, Incapacitated, enemy proximity or natural terrain remain source-specific.

Efficient Power Cells extends eligible nonhealing deployments only. Mech Overdrive extends eligible device duration, never healing capacity, charges, ammunition or resource recovery. A disabled device's duration continues. Whether it can accept a support command or maintenance depends on the actual disabled-state rule; the scheduler grants no permission.

## Reference boundary

The reference helper accepts already paid legal activation, exact original clock markers, a canonical wallet/action state and a shared recipient ledger. It does not itself pay initial BG/Conviction/Ki, enforce acquisition, choose targets, roll/heal, compute Echo final previews, implement object destruction, or execute the entire companion command engine.

Profile target caps of6 for mixed Oracle/Cleric effects mean3 allies plus3 eligible enemies, not6 of one side. The caller must validate these subcaps before creating a fixed roster or committing recipients. The helper's generic recipient count does not grant broader targeting.

Source-qualified independent components and remaining guard/exclusion records retain their separate guides. The supplied100 class passages and the negative scan of78 operational spell drafts do not cover770 unfinished spells or unsupplied items/monsters.
