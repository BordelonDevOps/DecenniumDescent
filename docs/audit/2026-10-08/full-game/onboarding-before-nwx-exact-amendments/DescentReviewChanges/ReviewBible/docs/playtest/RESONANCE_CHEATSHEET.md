# Resonance and Revelation — current playtest reference

Use [shared class rules](../mechanics/CLASS_PLAYTEST_RULES.md), [spell integration](../mechanics/SPELL_INTEGRATION_RULES.md), and the [character foundation](../mechanics/CHARACTER_CREATION_PLAYTEST.md). This sheet summarizes their active candidate configuration. Individual cards keep their exact prerequisites, costs and exceptions.

## Before casting

Declare the casting class. Check its own class level, school/rank access and known/prepared or spellbook requirements. Select an operational spell, then check components, target, range, action availability and payable cost. Sufficient RP does not unlock access. A class feature with the same name remains a separate feature.

## Base RP prices

| Rank | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | Grand |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RP | 0 | 2 | 3 | 5 | 7 | 10 | 13 | 17 | 21 | 26 | 32 |

Apply the current Dissonance surcharge and only actual card-authorized modifiers. Generic Overcast options are excluded from this configuration. A named class feature such as Overchannel follows its own card.

## Dissonance and Refrain

`Limit = max(4, 2 + total-character PB + max(0, casting-class ability modifier))`.

Evaluate the current strain before a ranked cast:

| Current Dissonance | Surcharge | Ordinary ranked casting |
|---|---:|---|
| Below Limit | 0 RP | Permitted if otherwise legal |
| Limit through Limit+2 | +1 RP | Permitted if otherwise legal |
| Limit+3 through Limit+5 | +2 RP | Permitted if otherwise legal |
| Limit+6 or higher | +3 RP for an expressly permitted exception | Ordinary rank-1-or-higher casting is unavailable |

A cast then adds base Dissonance: 0 for rank 0, 1 for ranks 1–5, and 2 for ranks 6–9. Immediately repeating the same named spell adds Refrain of +1, then +2, then +3 maximum on subsequent repeats; repeated cantrips also count. Apply the class's exact cadence reductions or vents.

Casting a different named spell resets the repetition counter but leaves accumulated Dissonance. Idle or weapon turns preserve Refrain unless an actual class rule clears it. Switching casting class clears neither history. Printed class techniques pay their printed costs and generate no automatic spell strain unless expressly covered by the casting rules.

Lich/Necromancer have an explicit ranked-casting exception through Fracture. They still need access and RP; direct Traumatic Casting uses their printed procedure and the pre-cast strain state. This exception does not reintroduce the excluded generic Overcast menu.

## Recovery

| Event | Candidate procedure |
|---|---|
| Regular turn without a spell or magical class ability | Lose 1 Dissonance. |
| Action spent Grounding without casting | Lose PB Dissonance instead of the idle-turn reduction. |
| Beneficial completed short rest | Retune once: recover `max(0, round-half-up(maximum RP / 4) + primary RP class casting modifier)`, capped at maximum; clear Dissonance. Preserve the remembered spell name and Refrain counter unless an actual class feature says otherwise. |
| Beneficial completed long rest | Restore RP to maximum, clear Dissonance, and reset the remembered spell name and Refrain counter. |
| Optional ten-minute meditation, once per day | Recover the primary RP class's positive casting modifier in RP; reduce Dissonance by PB plus that positive modifier. |

The [rest rules](../mechanics/STRAIN_PLAYTEST.md) require one hour for a short rest, eight hours for a long rest, at most two beneficial short rests between beneficial long rests and one beneficial long rest per 24 elapsed hours. Interruption and campaign requirements still apply. Ending an encounter alone does not clear Dissonance. Do not infer a separate class-resource recovery from Retune.

## Multiclass characters

Use one merged RP pool: the selected primary class's full pool plus `ceil(secondary pool / 4)` from at most one secondary class. Select contributors by the foundation's tier, class-level, pool and acquisition-order rules; do not choose a different primary per cast. Oracle, Soldier and Warrior contribute no RP pool. Each casting class still satisfies its own repertoire and rank gate. Keep one character-wide Dissonance/Refrain history and one ordinary concentration slot, with only explicit exceptions.

## Oracle Revelations

The [Oracle engine](../mechanics/classes/oracle.md) uses RC for Revelations: capacities 3 at Oracle levels 1–2, 4 at 3–5, 5 at 6–8, 6 at 9–10 and 7 at 11+. A beneficial short rest restores 1 spent RC; a beneficial long rest restores RC to maximum. Combat-generated refunds share at most 1 RC per round and require genuine qualifying events. Follow the engine for its encounter-start floor and limited special refills.

Revelations use their printed RC costs and do not generate ordinary Weave Dissonance or clear another class's existing strain/Refrain. Increasing a resource maximum through advancement does not refill current resources. The [previous reference](../../../../docs/audit/2026-10-08/full-game/onboarding-before-reconciliation/DescentReviewChanges/ReviewBible/docs/playtest/RESONANCE_CHEATSHEET.md) preserves the earlier alternative pricing and Overcast text.
