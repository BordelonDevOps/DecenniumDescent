# GPT rank-three Enchantment authoring clarification

Source: Calibration Review, conversation `6a7a0fa2-eee0-83ea-92e9-6723a9f67ede`.
Actual turn: `33bf6fab-17fa-493e-98d6-c2804d2c4793`; agent message: `0cf858db-32b0-4fe8-8581-3b4ff925e8cf`.
Complete app-reader reply. This resolves authoring interfaces; it does not approve or promote exact cards.

---

These are **authoring clarifications only**. No rank-three card is promoted; catalog remains **229 reviewed / 619 unfinished**. Prior source rulings remain in force except where refined below.

## 1. Dominate Beast and bound companion chassis

A bound companion with no independent regular turn **does not gain one from Dominate Beast**.

### NEW CROSS-SYSTEM RULE — Dominated Companion Execution

For a Beast using the reviewed companion attached-phase chassis, Dominate Beast redirects the companion's **existing owner-linked companion execution opportunity** rather than creating a normal creature turn.

During each numbered round in which the companion's owner's ordinary companion attached phase occurs:

- the dominator may provide the spell's mental order for that companion;
- this substitutes for the ordinary owner-issued command for that attached phase;
- the companion then moves/performs the compelled command in the **same existing attached phase**;
- no separate regular START/END, Reaction refresh, recharge, death save, duration tick or independent turn is created.

The dominator pays **no additional Action/BA** for this ongoing mental order beyond the spell's established control interface.

### Command/offensive ledgers

The forced execution uses the companion's **existing owner's shared companion ledgers**, because those are structural caps on that companion chassis:

- one companion-command allowance per owner/numbered round;
- one offensive-companion allowance per owner/numbered round.

A dominated execution therefore **occupies** the owner's command allowance for that round, and if damaging, also occupies the owner's offensive allowance.

This is not treated as the unwilling owner voluntarily spending their Bonus Action or choosing to expend a resource. The owner's BA is **not charged** merely because the domination commandeered the companion.

Consequences:

- if the relevant shared command allowance is already consumed, Dominate Beast cannot create another commanded companion Action that round;
- if the offensive allowance is already consumed, the dominator may not force another damaging companion Action, but may issue a legal non-offensive command;
- if domination consumes those structural allowances first, the owner cannot later obtain a second companion/offensive execution that round.

No separate dominator companion ledger is invented.

### Stats

The companion uses its **actual companion profile and existing attack/save/DC/stat rules**. Dominate Beast does not substitute the dominator's spell attack/DC into the companion's attacks merely because the dominator controls the choice.

The spell's INT save uses the caster's spell DC as already ruled.

### Owner commands versus domination

An ordinary owner command is **not another magical mandatory compulsion** and therefore does not receive a Compelled Budget Arbitration priority timestamp.

While Dominate Beast supplies a valid order for that attached phase, the magical control governs the companion's behavior and supersedes a contradictory ordinary owner instruction.

If the owner already paid a BA to issue a command before that order is superseded, that BA is not refunded.

If the dominator issues **no valid order**, the companion chassis operates normally: an already-valid owner command may execute; otherwise the companion has its ordinary uncommanded defensive behavior.

Bond, ownership, slots, HP, Load, upkeep, summon duration and all other companion records remain unchanged.

### Wild/NPC Beasts

A Beast with an actual independent regular turn uses the original Dominate Beast ruling normally: order at its future regular START, movement + one ordinary Action.

This companion bridge applies only where the actual creature lifecycle explicitly replaces independent turns with an owner-attached companion phase.

---

## 2. Hypnotic Pattern

### a. Cube placement and LoE

Yes: the selected point is the **center of the 30-ft cube**.

For both modes:

- Enchantment: center must be a point the caster can perceive within **60 ft + LoE**.
- Illusion: center must be perceived within **30 ft + LoE**.

The actual cube then extends 15 ft from that center along each axis.

A creature is initially eligible only if all are true:

1. physically inside the cube;
2. has **LoE from the cube's center**;
3. can actually see the visible pattern.

So an opaque solid barrier between creature and pattern center blocks application even if grid geometry technically places the creature inside the cube.

This is a casting/effect LoE requirement, not wall vision.

### b. Caster self-inclusion and concentration collapse

Use a **NEW spell-specific atomic initial-resolution batch**.

Procedure:

1. establish the fixed eligible target snapshot;
2. resolve all initial WIS saves;
3. determine each target's independently legal Charmed and Incapacitated components;
4. apply every target's initial components and their immediate consequences;
5. any Incapacitated that ends existing concentration does so normally for that affected creature;
6. if the caster's own Incapacitated ends concentration on Hypnotic Pattern, queue that spell's concentration teardown until **after every target in this same initial Pattern batch has received its initial application**;
7. then end Hypnotic Pattern and remove all still-maintained components from this cast.

Thus caster self-failure does **not** abort later members of the initial target snapshot based on arbitrary iteration order.

However, immediate consequences still matter. For example, another target Incapacitated during the batch can lose its own unrelated concentration before Pattern subsequently ends.

This is **not a universal simultaneous-area rule**; it is an exact Hypnotic Pattern initial-resolution completion required to avoid iteration-order artifacts.

### c. Rousing and repeated Pattern applications

A helper's rousing Action ends **one actual Hypnotic Pattern cast's application** on that creature, removing both that cast's Charmed and Incapacitated components still present.

It does **not** automatically remove every Hypnotic Pattern source the way ordinary Sleep's explicit shared waking rule does.

If multiple Pattern applications exist and the helper cannot distinguish their source applications, the helper does not gain a diagnostic. Use stable application order to select one valid Pattern application to rouse, without revealing hidden caster/source metadata.

### Recasts

Hypnotic Pattern applications are independent sources.

Normally, the same caster cannot maintain two because beginning the new concentration already ends their previous Pattern before resolution. If an exact feature legally permits multiple concentrations, the second Pattern creates another independent application rather than “refreshing” the first.

Each new Incapacitated component independently checks its source-character/target hard-control allowance. A blocked new Incapacitated component may still leave a legal new Charmed component.

A Charmed-only Pattern application receives **no repeat save** merely because its hard component failed or was later removed. It ends through that application's concentration, rousing/damage procedure where applicable, removal, or expiry.

---

## 3. Slow Transmutation Reaction timing

### Voluntary-movement trigger

“Begins voluntary movement” means the start of a **distinct voluntary movement segment**, not each 5-ft step.

A new segment occurs when the creature transitions from not currently resolving voluntary movement to spending movement again.

Examples:

- starts moving at turn beginning → trigger;
- moves 10 ft, attacks, then resumes movement → new trigger;
- pauses only to choose the next square while continuously resolving movement → not a new trigger;
- every individual tile/foot → never a separate trigger.

A creature may therefore create multiple legal movement-start trigger windows in one turn, though actual Reaction availability still limits each observer/caster.

### Triggering creature must be included

**Refinement:** the creature whose Action/movement creates the Reaction window **must be one of Slow's selected targets**.

It may select up to five additional legal creatures.

This prevents using an unrelated creature's movement as an arbitrary timing window to Slow six different creatures, which would broaden the invented Reaction interface beyond its purpose.

### Extra turns

Any actual turn, including an **extra turn**, can create the Action/movement Reaction trigger.

Repeat saves remain **regular-turn END only**. Extra turns grant no additional Slow save.

### Parent Action removed by nested interruption

Once the Slow Reaction was legally committed against a qualifying pending Action/movement start, it is an independent paid spell on the interrupt stack.

If Counterspell, Distract or another legal nested interruption later removes the original triggering Action before Slow resolves:

- Slow still resolves against its independently legal selected targets;
- it does not refund;
- it does not cancel or revive the parent;
- no selected target is lost merely because the original parent ceased to exist.

The trigger established legal casting permission; continued parent existence is not an ongoing tether.

### Already-committed Reactions

A newly established Transmutation Slow `no Reactions` rider prevents **future Reaction commitments**.

It does not erase or cancel a Reaction already legally committed and currently unresolved in the LIFO stack unless another exact effect separately cancels it.

---

## 4. Slow numeric and Action scope

Confirmed.

### Half Speed

All competing hostile flat/fractional Speed reductions are evaluated against the same appropriate **pre-control Speed**, using the already-reviewed hostile slow arbitration.

Do not repeatedly halve an already-halved result merely because another half-Speed source exists.

After that adverse-slow result is selected, apply the actual later systemic multipliers/modifiers in their existing order.

### Enchantment `−2 DEX`

Remains exactly:

- `−2 Dexterity ability checks`;
- `−2 Dexterity saving throws`;
- **not initiative**.

It is not an ability-score change and does not alter:

- Dexterity attack rolls;
- damage;
- spell DC;
- AC beyond Slow's separately printed `−2 AC`;
- derived statistics not explicitly named.

The initiative exclusion is an explicit NEW source-completion exception.

### One-Action ceiling applied midturn

Enchantment Slow means:

> at most one ordinary full Action may be **committed** on each actual turn while the rider applies.

If the target has already completed one Action before Slow applies, it cannot commit another Action during that turn.

If a second Action was **already legally committed and pending** before Slow applies, that Action finishes normally. Slow does not rewind/cancel it.

After it resolves, no further Action can be newly committed that turn.

Each actual turn—including an extra turn—has its own one-Action ceiling. This does not:

- restrict attacks inherent inside one Attack Action;
- remove BA;
- remove Reaction;
- erase movement.

An exact separate extra-Action source can still create an extra Action resource, but Slow prevents committing it if one Action has already been committed that actual turn.

### Independent component suppression

Yes. Slow's components remain independently suppressible/blockable by actual defenses where those defenses have sufficiently narrow scope:

- half Speed;
- `−2 AC`;
- DEX check/save penalty;
- one-Action ceiling;
- no-Reactions.

Blocking one does not automatically remove the others absent a broader defense.

---

## 5. Suggestion hard-control integration

### a. Reserve hard allowance at initial establishment

Confirmed.

If the successfully failed-save Suggestion's defined task **necessarily requires one or more ordinary full Actions to carry out**, establish/claim the shared hard-control allowance **once at initial Suggestion application**.

Do not defer a new hard claim until each later Action occurs.

If the hard component is blocked, determine whether the suggestion still contains an **independently meaningful legal soft task** achievable through movement/interactions that do not require commandeering a whole Action.

If yes, that soft remainder can genuinely establish and therefore **replace a prior Suggestion**.

If no meaningful compliant task remains, no new Suggestion establishes and an older valid Suggestion remains.

### b. Task later unexpectedly needs an Action

A Suggestion established without a hard component may **not later acquire one dynamically**.

If later circumstances mean completion now necessarily requires commandeering an ordinary Action that was not reserved at establishment:

- the spell cannot force that Action;
- seek any ordinary legal completion path still available within the originally established soft scope.

If no reasonably achievable compliant path remains without adding that hard component, the remaining compulsion **ends** rather than claiming a fresh hard allowance.

A temporary ordinary delay alone does not end the suggestion.

Examples:

- locked door, but target can reasonably wait for someone else to open it within the remaining duration → may persist;
- only possible continuation requires target itself to perform an unreserved Action to operate machinery → cannot newly compel that Action; if no alternative remains, end.

This prevents an apparently soft 8-hour instruction from becoming a delayed hard-control loophole.

### c. Hostile tasks, attacks and resources

Confirmed.

Where a hostile Suggestion is actually **reasonable to the target given its existing beliefs, loyalties, knowledge and circumstances**, it can compel an ordinary Attack Action under the approved compelled-Attack rule:

- inherent Extra Attack/native ordinary Multiattack included when actually part of that Action;
- ordinary required ammunition spent normally;
- no additional Action;
- no spellcasting/RP;
- no charges/recharge/per-rest resources;
- no consumables;
- no optional finite riders;
- no special limited ammunition.

The target/controller chooses legal attack method/details where the suggestion does not specify them.

Reasonableness is resolved from **actual target state after paid casting**. The caster receives no hidden-belief/loyalty diagnostic from a successful or failed establishment.

New information/circumstances can make the remaining task materially unreasonable, prohibited or impossible and therefore end the compulsion.

Ordinary temporary delay, inconvenience, travel time or a temporary obstruction does **not** by itself end a still-reasonable finite task that remains achievable before the 8-hour endpoint.

---

### Shared additions to carry into exact authoring

Mark these explicitly **NEW** in the exact-review packet:

- **Dominated Companion Execution** bridge for owner-attached companion chassis.
- **Hypnotic Pattern atomic initial-resolution batch**.
- Hypnotic Pattern one-application-at-a-time helper rousing.
- Transmutation Slow distinct-movement-segment trigger and mandatory inclusion of triggering creature.
- Slow no-Reactions affects future commitments, not already-stacked Reactions.
- Suggestion reserves any necessary hard component at initial establishment and cannot dynamically acquire a new hard component later.

Everything else from the rank-three source conference remains unchanged.

No rank-three Enchantment card is promoted by this clarification; catalog remains **229 / 619**. Cosmology remains deferred until after the authorized GitHub push and remote-commit verification.

