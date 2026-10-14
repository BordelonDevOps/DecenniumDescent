# When a character goes Downed — damage, aid and recovery

**Reviewed authored teaching/presentation — TEX-EXACT-2026-10-11.** This example follows the reviewed [Core damage, Wound and death procedure](../mechanics/CORE_RESOLUTION_PLAYTEST.md) and [item-use rules](../mechanics/EQUIPMENT_ITEM_PROCEDURES.md). Use their full text for eligibility and exceptions. The example adds no injury, death rule, equipment grant or resurrection permission.

The patient is **Mira, the level-1 Bard** from the [first-character walkthrough](FIRST_BARD_WALKTHROUGH.md). Begin this separate scene at **10/10 HP, no temporary HP, no Wounds, CON save +2**, with no concentration or independent condition. Her existing load makes her Burdened, with Speed 20 feet when otherwise able to move. She holds nothing that changes that load when dropped. The damage below is already resolved after attacks, saves and defenses; no prevention or special survival feature applies.

## 1. The first hit causes a Wound

Mira takes **6 resolved damage**. With no temporary HP, all 6 is post-temp damage. Her normal HP falls from 10 to **4**.

She has not reached zero, so this is not Instant Death. It nevertheless triggers one Wound save because **2 × 6 = 12**, at least her maximum HP of 10. The Wound DC is **max(10, floor(6/2)) = 10**.

Her natural roll is **6**. With CON +2 and no pre-existing Wounds, the total is **8**: failure by 2. Add **Wound W1**, with no linked Injury because the failure was less than 5. Her future Constitution saves now suffer −1, giving a current CON save modifier of **+1**. The new Wound did not penalize the roll that caused it.

Record **HP 4/10; W1; no Injury**. This Wound does not itself reduce her maximum HP, halve her Speed, cause extra damage or impose disadvantage.

## 2. A second hit drops her to zero

A separate hit deals **4 resolved damage**, again with no temporary HP. Mira falls from 4 to **0 HP**. Instant Death does not apply: **4 post-temp damage − 4 previous HP = 0**, below her maximum of 10.

Dropping from positive HP to zero triggers one Wound save even though the four damage is below half her maximum. Its DC is 10. This time Mira's natural roll is **3**, and W1 already existed:

**3 + CON 2 − 1 existing Wound = 4: failure by 6.**

Add **Wound W2**, then roll one Injury for W2. The example's d6 result is **3: Mobility Trauma**, reducing non-teleport Speeds by 5 feet. Link that Injury to W2. It is not a third Wound.

Mira survives at zero HP and begins **dying**, with **zero death-save successes and zero failures**. The hit that first reduced her to zero does not also add a death-save failure. She becomes Unconscious, including Incapacitated and Prone under the condition's actual rules. She cannot move merely because a Speed number remains on her sheet.

Her sheet now shows two Wounds and a CON save modifier of **+0**. When otherwise able to move, her Burdened Speed 20 is reduced to **15 feet** by Mobility Trauma. Two Wounds do not yet create the separate three-Wound Critical penalty.

## 3. Make the death save, then receive aid

At Mira's next **regular-turn start**, she rolls a natural **8** for her death save. In this scene no feature specifically modifies death saves. She adds neither CON nor PB, and her Wound penalty does not apply to this special roll. Record **one failure, zero successes**.

An ally then reaches her with a physically accessible healer's kit, one available hand and an Action. The ally has no feature changing stabilization into healing. One Action and one kit charge automatically stabilize the adjacent living dying Mira; a full kit falls from **10 charges to 9**. No Medicine roll is needed for that kit use.

At **12:00**, record Mira as **Stable at 0 HP**, clear both death-save counters, and roll the Stable recovery d4 once. The example result is **2**, setting an absolute recovery deadline of **14:00**. Mira remains Unconscious and Prone. Both Wounds and Mobility Trauma remain. The kit's spent charge does not restore HP, remove a Wound or shorten that deadline.

Stable creatures do not make death saves. A new damage packet reaching normal HP would end Stable and cancel this deadline, applying its own damage/death procedure. Do not keep the old deadline as a second recovery benefit if that happens.

## 4. Put treatment and recovery on one clock

For this example, Mira is now in a location where the following treatment can actually be carried out. A qualified helper has **Wisdom (Medicine) +3**, a usable medical kit and **one actual Supply** allocated to the procedure. These are scene requirements, not free equipment or a conversion of rations into Supply. The earlier stabilization charge does not pay this treatment's separate costs. The Director has established **tier I**, with Medicine DC 12, as the applicable treatment tier.

At **12:30**, choose **W2 with Mobility Trauma** as the Wound to treat. Begin the eight-hour treatment and **consume one Supply immediately**. This example assumes no interruption, new damage, recovery prohibition or other complication. The helper's active work is not automatically an eight-hour rest.

| Time | Event | Mira's state afterward |
|---|---|---|
| 12:00 | Stabilization; d4 result 2 | Stable, 0 HP; counters clear; W1 and W2 remain |
| 12:30 | Begin treating W2; commit the Supply | Still Stable at 0 HP; no early Wound removal |
| 14:00 | The recorded Stable deadline arrives | Regain **1 HP**; Stable ends and counters remain clear; both Wounds remain |
| 20:30 | Eight treatment hours finish; resolve the Medicine check | Apply the treatment outcome below |

At 14:00, zero-HP Unconsciousness ends because it was the only cause in this scene. Mira is still **Prone** until she legally deals with that position; recovery does not stand her up. Her Mobility Trauma persists while W2 remains. The treatment continues with its required access and care.

At 20:30, the helper rolls **10 + Medicine 3 = 13** against DC 12: **Success**. Remove the chosen **W2** and its linked Mobility Trauma. W1 remains. Mira's CON save modifier returns to **+1**, and her Speed when able to move returns to the existing Burdened value of **20 feet**. Her HP remains **1/10**: removing a Wound is not HP healing.

The clock has advanced from 12:00 to 20:30, a total of **8½ elapsed hours**. The two-hour Stable interval overlaps treatment; it is not added again to make a ten-hour treatment. No later rest may replay that same Stable recovery event. Whether Mira or the helper also qualifies for any actual rest benefit is a separate rest-rule decision, not an award made by this example.

If the treatment had failed, the spent Supply would still be spent and neither Wound would be removed. A Critical Failure would additionally give the **patient one expedition Strain**, according to the [reviewed Strain binding](../mechanics/STRAIN_PLAYTEST.md). A Critical Success could remove W2 and one other existing Wound chosen by the patient. These are alternative outcomes, not additional rolls after the Success above.

## 5. Keep the dangerous alternatives distinct

These are independent boundary examples with their stated starting states. They do not change the completed scene.

| Situation | Resolution |
|---|---|
| At 10/10 HP, no Wounds, **3 temporary HP**, then 6 resolved damage without Maiming | Temporary HP absorbs 3; normal HP becomes 7. Post-temp damage is only 3, so no half-maximum or zero-HP Wound trigger occurs. Temporary HP changes the damage calculation; it is not normal healing. |
| Already dying at 0/10 HP with **one death failure**, then a genuinely legal critical hit deals 1 post-temp damage, without Maiming | No half-maximum Wound trigger; the critical hit adds **two failures**, reaching three and causing death. Ordinary kit use or HP healing cannot restore a Dead creature. |
| At **4/10 HP**, no temporary HP, then **14 post-temp damage**, with no qualifying survival exception | The excess is 14 − 4 = 10, meeting maximum HP: **Instant Death**. This branch stops before a Wound save or new death-save failure. |
| Dying with two Wounds and no HP-gain blocker, then a **natural 20 death save** | Regain **1 HP**, clear counters and end zero-HP Unconsciousness. Wounds, their Injuries and Prone remain unless separately removed. |
| Alive at **3/10 HP with three Wounds**, then receive 20 points of otherwise legal ordinary healing | Critical's healing ceiling is max(1, 10 − 1) = **9 HP**. Regain 6 HP; maximum HP is still 10, and all three Wounds remain. The next failed **Wound save**, not merely the next damage packet, is fatal. |

For the three-Wound case, Critical also reduces Speed by 10 feet, to a minimum of zero. That can coexist with a linked Mobility Trauma penalty. The failure that first raised two Wounds to three did not itself count as the later fatal failure.

## Leave a usable patient record

The continuing scene ends with **Mira at 1/10 HP, one Wound W1 without a linked Injury, CON save +1, no Stable deadline and clear death-save counters**. Her existing Burdened Speed is 20 feet when movement is otherwise legal. Record Prone until she actually stands or another legal effect changes it. Also retain the spent healer's-kit charge, the consumed Supply and the helper's eight treatment hours.

Positive HP, stability, Wounds, linked Injuries and position are separate entries. Keeping each one visible lets the group apply aid without accidentally erasing another consequence.
