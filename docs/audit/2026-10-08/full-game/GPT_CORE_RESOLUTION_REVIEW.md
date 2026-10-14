The source hierarchy supports using **Core V2 for attacks, Wounds, death, and stabilization**, with the Gameplay Loop used only as a clearly labeled integration overlay where Core is silent. Pasted text

## 1. Attack resolution — **ACCEPT**

Core explicitly establishes:

- `d20 + ability modifier + proficiency when proficient`
- natural 1 always misses
- natural 20 always hits
- natural 20 doubles **damage dice** Pasted text

Nothing supplied makes `AC + 10` a critical hit.

**Use:**

> Attack succeeds when the final attack total meets or exceeds AC. Natural 1 always misses. Natural 20 always hits and is a critical hit, doubling damage dice only. Exceeding AC by 10 has no generic additional effect. An explicitly reviewed critical-range feature may broaden the natural critical range; critical-range expansions do not stack.

That matches the current class interface.

---

## 2. Task degrees vs saves — **QUALIFY**

The proposed separation is correct.

The four Gameplay degrees and natural-result shifts are explicitly documented for the general task resolution system. Pasted text

But neither the supplied Core save rules nor spell/class save interface establishes generic natural-1/20 behavior for saving throws. The class integration currently says simply that a save succeeds at DC. Pasted text

### Replacement

> **Task, skill, and tool checks:** use the four Gameplay degrees. Natural 20 improves the result by one degree; natural 1 worsens it by one degree, bounded at Critical Success/Critical Failure.
>
> If a task rule defines only Success/Failure, treat Critical Success as Success and Critical Failure as Failure unless that rule explicitly provides an additional consequence.
>
> **Saving throws:** are binary unless the specific effect prints degrees or a margin such as failure by 5/10. A final save total meeting or exceeding DC succeeds. There is **no generic automatic success/failure or degree shift on a natural 20/1**.
>
> Death saves use their own explicit natural-20/natural-1 rules.
>
> Attack rolls use the separate Core attack rule.

This avoids silently extending the task natural-roll system into saves.

---

## 3. Static ties and opposed checks — **QUALIFY**

Static DC tie = success is sourced twice:

- Gameplay: total meets or exceeds DC = Success.
- Shared class interface: save succeeds at DC. Pasted text

Opposed ties are not resolved in the supplied text.

### Minimal NEW provisional closure

> **Static DC:** meeting the DC succeeds.
>
> **Opposed check:** each side rolls its applicable check; higher final total wins. On an exact tie, the existing state remains unchanged, meaning the initiating creature fails to alter the opponent or situation.
>
> The generic task natural-20/natural-1 degree shift does not modify an opposed roll unless the particular opposed action explicitly defines degree outcomes. Do not convert one participant's natural result into a mechanical bonus or penalty to the other's roll.

This works cleanly for Disarm, Trip and similar Core maneuvers. Pasted text Pasted text

---

## 4. 0 HP and death saves — **QUALIFIED ACCEPT**

Core wins the timing conflict:

> At 0 HP, character is Unconscious and makes death saves at the **start** of each turn. Pasted text

So Gameplay's end-of-turn version is inactive for this candidate. Pasted text

Gameplay's **Prone** addition does not contradict Core, but it must be identified as an integration addition rather than Core wording.

### Replacement

> At 0 HP, a living character becomes **Unconscious** and, for this playtest overlay, **Prone**.
>
> It makes one death save at the **start of each regular initiative turn** while dying. Extra turns and extra Actions do not generate additional death saves.
>
> - 10+ = one success.
> - 9 or lower = one failure.
> - Natural 20 = regain 1 HP.
> - Natural 1 = two failures.
> - Three successes = Stable.
> - Three failures = Dead.
>
> Damage suffered **while already at 0 HP** causes one death-save failure, or two if that damage is from a critical hit.
>
> A hit that reduces a creature from positive HP to 0 does **not** also count as “damage at 0 HP.”
>
> Actual healing that raises HP above 0 ends the dying/Downed state.

The last two sentences are integration clarifications, not quoted Core rules.

---

# 5. Core Wounds own the candidate — **QUALIFIED ACCEPT**

Core explicitly gives all three Wound triggers:

1. drop to 0 HP;
2. suffer one source of damage equal to at least half maximum HP;
3. Maiming effect. Pasted text

Core also owns:

- Wound save = Constitution, `max(10, half triggering damage)`;
- failure = one Wound;
- failure by 5+ = one Wound + Injury table;
- each Wound = `-1 Constitution saves` and reduces maximum Hit Dice recovered per long rest;
- three Wounds = Critically Wounded, `Speed -10 ft`, cannot regain full HP, dies on next failed Wound save. Pasted text

Therefore the Gameplay alternatives—

- automatic Wound from crit-to-zero,
- two death failures,
- resurrection,
- Hit Dice **healing per die** penalty,
- half Speed,
- Strain lock—

should remain inactive evidence, not stack with Core. Pasted text

### Wound treatment

The Gameplay kit + Supply + 8 hours + Medicine procedure is mechanically compatible with the supplied Core excerpt because Core here provides no treatment procedure.

I would classify it as:

**NEW ACTIVE INTEGRATION RULE DERIVED FROM REVIEW GAMEPLAY, NOT CORE V2 CANON.**

Do not call it Core wording.

Before freezing it, Codex should search the approved Core book for any other `Wound treatment`, `treat wound`, `Medicine`, `injury recovery`, or similar section. If Core supplies one elsewhere, Core wins.

---

# 6. Damage → Wound → death ordering — **ACCEPT THE NEED; ADD EXACT PROCEDURE**

The source defines all the components but not their simultaneous-event order.

This is a true integration gap.

## Minimal NEW provisional event sequence

Use this:

> ### Damage, Wound, and 0-HP ordering
>
> 1. Resolve the attack/save and determine the final damage packet after applicable defenses.
> 2. Apply that damage to temporary HP and HP under the normal damage procedure.
> 3. Determine whether this **single damage event** triggers a Wound save:
>    - the creature dropped from above 0 HP to 0 HP;
>    - the actual damage suffered from this source was at least half its maximum HP;
>    - the effect was Maiming.
>
>    Multiple qualifying conditions from the same damage event produce **one Wound save only**.
> 4. Make that Wound save immediately. Existing Wounds from before this event apply their Constitution-save penalty. A Wound gained from this save does not penalize the save that created it.
> 5. Resolve the Wound result completely.
> 6. If the creature is still alive and is now at 0 HP, establish or continue its dying state.
> 7. If the creature was **already at 0 HP before this damage event**, after resolving any triggered Wound save apply one death-save failure, or two if the damaging hit was critical.
> 8. If either system kills the creature, stop processing later living-creature consequences that require it to remain alive.

This prevents duplicate Wounds from one hit and distinguishes **dropping to zero** from **being damaged at zero**.

---

# Critical-state edge rules

Two points still require explicit closure.

### Reaching three Wounds

Core says:

> “Three Wounds — Character is Critically Wounded … and dies on the **next failed Wound save**.” Pasted text

That strongly supports:

> A failed save that increases the character from two Wounds to three does **not** kill them. After that save resolves, they become Critically Wounded. If they begin a later Wound save already at three Wounds and fail it, they die instead of gaining a fourth Wound.

That is the cleanest source reading.

### “Cannot regain full HP”

This is operationally incomplete.

Minimal provisional interpretation:

> While Critically Wounded, current HP cannot be restored to maximum HP; its healing ceiling is **maximum HP - 1**. This does not reduce the actual maximum-HP statistic. Removing enough Wounds to leave the Critical state removes this ceiling.

The `-1` is newly specified solely because “cannot regain full HP” needs an executable boundary.

---

# Stable and Dead states are underspecified

The source tells us how they are reached but not enough about their ongoing mechanics.

I recommend this explicitly **NEW provisional closure**:

> **Stable:** living, 0 HP, Unconscious, not making death saves. Clear accumulated death-save successes and failures when Stable is reached. Healing above 0 ends Stable. If a Stable creature takes damage while still at 0 HP, it becomes dying again and that damage applies the normal at-0 death-failure rule.
>
> **Dead:** no longer a living target, makes no death saves, cannot receive ordinary healing or stabilization. Resurrection is required to restore life.

This is consistent with Core's separate resurrection statement, which says resurrection restores life and does not automatically clear Wounds or other consequences. Pasted text

---

# Injury table

Do **not** invent this yet.

Core explicitly requires an Injury-table roll on Wound-save failure by 5+. Pasted text

That is a **source lookup**, not a confirmed gap.

Codex should search the approved Core book and its approved supporting tables for:

- `Injury table`
- `Injury`
- `Maiming`
- `Critical Injury`
- table entries associated with Wounds.

If no actual table exists after source audit, then we should jointly author a provisional Injury table rather than silently dropping the Failure-by-5 consequence.

---

## Conference disposition

1. **Attack resolution:** ACCEPT.
2. **Task degrees / binary saves:** QUALIFY, with explicit separation above.
3. **Ties/opposed checks:** QUALIFY; add the new tie rule.
4. **Death-save timing/state:** QUALIFY; Core start-of-turn wins, Gameplay Prone is an explicit overlay.
5. **Wounds:** QUALIFY; Core triggers/penalties/Critical state win; Gameplay treatment may fill recovery only after confirming no Core recovery rule elsewhere.
6. **Simultaneous damage/Wound/death ordering:** ACCEPT need and adopt the explicit provisional sequence above.

The major unresolved source item is now the **actual Injury table**. Everything else in this packet can be made deterministic with the small, clearly labeled integration rules above without rewriting the approved sources.