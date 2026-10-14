1. **Bleed stacking groups — AGREE, with a global family arbitration rule rather than unlimited cross-owner ticking.**

Namespacing must not turn the old “same-named conditions do not stack” rule into a loophole. I would use this **NEW provisional reconciliation**:

> Every Bleed application has both a source-qualified `mechanicalId` and a `stackGroupId`. Records inside one stack group obey that engine's printed refresh/cap rule. Different application text from the same owner/engine does not create additional slots unless the source explicitly permits them.
>
> All hostile Bleed stack groups on one target remain independently recorded for ownership, duration, cures, hooks and source interactions.
>
> **At any one identical periodic timing marker, only one Bleed stack group deals periodic damage to that target**, chosen by highest expected unmitigated damage for that marker, then earliest application on a tie. Other groups reaching that same marker consume that scheduled tick but deal no damage; they are not deferred or banked.
>
> A printed exception allowing multiple simultaneous instances inside the selected group still operates. Thus Crimson Blood Echo may resolve its expressly permitted two independent Crimson instances.
>
> Bleeds with genuinely different printed timing markers may each resolve: for example a start-of-regular-turn custom Bleed and an end-of-regular-turn Core/generic Bleeding record can coexist because they are not the same periodic marker.
>
> A record with replacement timing never also participates in the generic Bleeding tick.

So I recommend **no unlimited cross-owner same-marker Bleed stacking**. Cross-owner applications remain meaningful because they retain ownership, cures, timers and hooks, and one may become the active damaging group when another expires.

Flat/nonperiodic duplicate penalties continue to use the strongest unless their source explicitly allows stacking.

This should be recorded as an explicit provisional clarification/exception to the older loose same-name rule, not as an automatic consequence of qualified IDs.

---

2. **Meaning of “your” — AGREE WITH YOUR CORRECTION.**

My earlier Thief wording was too narrow.

The default interpretation should be:

> **“Your” refers to the owning character/source owner, not automatically to the class that supplied the effect.**

Registry records therefore need at least:

- `ownerCharacterId`
- `sourceClass`
- `sourceEngine`
- `mechanicalId`

For **Thief Sneak Attack**:

- `your Bleed` = an active Bleed owned/applied by that character, including one acquired through another class in a future legal multiclass build;
- `your Poisoned` = Core Poisoned currently caused by that character;
- `your Crippled` = specifically the active `thief.crippled` identity, because Crippled is not a generic cross-class family.

That is the most source-faithful interpretation absent an explicit class-origin restriction.

By contrast, **Crimson's technical “your Bleed” references its named Crimson Bleed engine** when a feature counts instances, extends ticks, spreads, detonates, grants BG, enables Blood Mark, etc. Another class's Bleed owned by the same character does not become a Crimson Bleed instance.

Likewise, Terror Engine explicitly says the qualifying state must be caused **“by your Warrior features,”** so that hook really is class/source restricted.

This distinction should be validator-visible:

- ordinary possessive → `ownerCharacterId`
- explicit “your [Class] feature/engine” → owner + source engine/class
- exact condition identity → exact mechanical ID

No new multiclass restriction should be inferred from a possessive alone.

---

3. **Brutality Sense snapshot — ACCEPT.**

Use a pre-event eligibility snapshot.

For Brutality Momentum, immediately before the triggering melee attack's damage is applied, require all of:

```text
perceived hostile
within 60 ft
4 × currentHP <= maximumHP
Brutality Sense otherwise operative
```

If false at that moment, the killing hit cannot qualify itself by reducing the creature to 0.

So:

- 30/100 HP before hit → qualifies.
- 26/100 before hit, killed by hit → does **not** qualify.
- 25/100 before hit → qualifies.

The resulting 0 HP is irrelevant to that trigger's prerequisite.

This is the correct event snapshot for a feature that says the creature was already marked Vulnerable when personally reduced to 0.

### Vengeful Smite

Also agree:

> Snapshot Vengeance-mark eligibility **when the Smite begins**, exactly as the card says.

A mark applied by that same Smite cannot retroactively satisfy its own bonus-damage prerequisite.

### Mark of Retribution

Its state should contain separate components:

- `vengeanceEligibility = active`
- `nextSmiteBonus = 1d8, unspent/spent`
- `opportunityAttackAdvantage = active`

Spending the `1d8` sets only `nextSmiteBonus = spent`.

The mark and its opportunity-attack advantage continue until the printed expiry unless another rule ends the mark itself.

---

4. **Decay versus natural-20 / Stable recovery — ACCEPT AS NEW INTEGRATION.**

Decay is materially stronger than Corrupted here.

Corrupted says healing is reduced. Decay says the target **cannot regain HP**. That should include state-recovery HP while Decay remains active.

I agree with your proposed bridge, with explicit state handling:

> **NEW:** While `oracle.decay` is active, no effect or state procedure can increase the creature's current HP unless that effect explicitly overrides Decay.
>
> A natural 20 on a death save still receives its exceptional survival benefit, but the prohibited 1 HP increase does not occur. Instead:
> - clear both death-save counters;
> - the creature becomes **Stable at 0 HP**;
> - create the normal Stable recovery deadline.
>
> This is a substitute integration consequence only when Decay blocks the natural-20 HP gain; it does not create an additional benefit when HP recovery is legal.

### Stable timer while Decayed

Keep one absolute recovery deadline.

At that deadline:

- if Decay has ended and the creature is still Stable at 0, regain the normal 1 HP;
- if Decay remains active, mark the Stable recovery as **due but blocked**;
- do not roll another `1d4`;
- do not move or restart the deadline.

When Decay later ends:

> If the recovery is already due, the creature is alive, still Stable, and still at 0 HP, it immediately regains that one deferred HP once.

If Decay ends before the deadline, the original deadline remains unchanged.

If the creature becomes unstable or dies before the deferred recovery resolves, cancel that pending Stable recovery exactly as the ordinary Stable procedure would; later stabilization creates a new normal deadline.

This gives every pending timer a finite identity:

- one start;
- one absolute due time;
- at most one blocked/due state;
- one eventual resolution or cancellation;
- never a repeated reroll or sliding deadline.

### Other Decay healing

Ordinary magical healing, class healing, regeneration, Hit-Dice healing, and similar HP recovery produce **0 HP regained** while Decay persists unless they explicitly say they function despite an HP-recovery prohibition.

Temporary HP is not current HP recovery and should remain a separate question only if an actual Decay interaction references it; don't silently treat temp HP as regained HP.

---

## Implementation rules I would freeze

These four principles can now become registry-wide invariants:

1. **Qualified IDs preserve mechanics; stack groups govern stacking.** Namespacing never creates permission to evade a source stacking limit.
2. **Possessive ownership and engine identity are separate dimensions.** “Your” defaults to owner-character unless text narrows it to a class/engine.
3. **Prerequisites snapshot at the timing the source states.** Later consequences cannot manufacture an earlier prerequisite.
4. **Blocked recovery keeps one existing timer; it does not create a new timer loop.**

I see no remaining blocker in these narrow cross-source rules. They are suitable to implement as explicit **NEW provisional integration rules**, while DD16 itself remains open for the remaining active rider binding/validation pass.