# Your first craft — Mira makes an antidote

**Authored teaching draft; presentation review pending.** This walkthrough uses the reviewed crafting framework and Herbalism recipe-200. It adds no recipe, proficiency or starting equipment. Keep the [recipe card](../mechanics/HERBALISM_PUBLIC_RECIPE_CARDS.md#recipe-200--refined-frost-antidote), [Herbalism procedures](../mechanics/HERBALISM_RECIPE_PLAYTEST.md) and [crafting framework](../mechanics/CRAFTING_HARVEST_PLAYTEST.md) available for their complete rules.

Mira is the same level-1 Bard from the [first-character walkthrough](FIRST_BARD_WALKTHROUGH.md): WIS +0, PB +2, with Herbalism-kit proficiency from Battlefield Medic. This is a separate teaching scene in a suitable, safe work area. The party has already obtained the ingredients, seven intact empty Glass vials and permission to use the physical station and tools listed below. Their acquisition and any payment must appear in the campaign's inventory and money records. These supplies do not appear in Mira's starting package, and this example does not deduct their cost from her original 10 gp.

## 1. Open one work order

Mira initializes **Herbalism level 1, 0 trade XP**, using her existing Herbalism-kit proficiency. That grants no second proficiency or extra PB. Character level, trade level and recipe skill level are separate numbers.

| Field | This order |
|---|---|
| Recipe | **recipe-200 — Refined Frost Antidote**, one batch |
| Eligibility | Recipe skill level 4; Mira's trained limit is max(4, 1) = **4** |
| Formula | This recipe does not require a separate formula; public visibility alone would not waive a different recipe's formula requirement |
| Work area | Suitable **Herbalist's Table**; this field-capable recipe still needs its actual station and tools |
| Physical tools | **Herbalism kit, Mortar and pestle, Drying rack**, actually available for the work |
| Lead/check | Mira; WIS +0 and one PB +2 contribution |
| Other bonuses | Ordinary functional tools +0, ordinary suitable facility +0; no special feature or specialty |
| Assistance | Maximum **0** for this recipe |
| Time | **2 active hours**, including the first 15-minute binding phase |
| Difficulty | **DC 10** |
| Standard batch | **5 doses** |

Mira's Medicine or Survival training does not add another proficiency bonus. Her numerical trade level does not add +1. She cannot use the safe-workshop option to take 10: this recipe is not at least five skill levels below her trade level. Missing physical tools would prevent work, even though she has the proficiency.

## 2. Reserve actual materials and packaging

Keep the component occurrence, tier and physical identity on the order. Another item called water or a petal with a similar name is not automatically the required ingredient.

| Reserved input | Exact quantity | Weight | Disposition on the Standard result below |
|---|---:|---:|---|
| Purified water, component `ing-200-0-purified_water`, tier 2 | 4 source units | 4 × 0.5 = **2 lb** | Consumed as ingredients |
| sparkling petal, component `drop-sparkling_petal`, tier 1 | 1 source unit | **0.36 lb** | Consumed as an ingredient |
| Ordinary empty Glass vials, `alchemical-containers.glass-vial` | 7 actual intact vials | 7 × 0.1 = **0.7 lb** | Five hold the product; two remain unused |

Reserve **seven vials before the completion check**, even if Mira plans to choose Standard quantity with improved containers. The requirement covers floor(1.5 × 5) = 7 possible doses. There is no post-roll opportunity to buy or retrieve missing vials to validate that check.

This recipe needs **no supplementary clean carrier water**: its 2.36 lb of consumed ingredients can supply the maximum 0.7 lb of finished compound, and neither component is an eligible catalyst. Ordinary clean carrier water would not replace the four tier-2 Purified-water units. The kit, station and auxiliary tools are separate from these consumed inputs.

For purchasing context, the component reference values total **4 × 8 + 10 = 42 gp**. Seven new empty vials have a combined **7-gp reference**, giving 49 gp before any actual station, rental or other costs. Those are references, not an automatic purchase or a promise that a supplier has stock. Already-owned intact vials can be reused without repurchasing them.

## 3. Spend the two hours

For this scene, the Director confirms an eligible two-hour work period beginning at **09:00**, within Mira's actual activity schedule. She works continuously; no rest, guarding, travel or other simultaneous activity claims those same minutes. This time contributes to the crafting framework's active-work limit.

All inputs are legal when work starts and remain so through **09:15**, when the first binding phase finishes. That phase is part of the two hours, so uninterrupted work reaches completion at **11:00**, not 11:15. Binding stabilizes these inputs only inside this particular order; it does not turn the mixture into reusable fresh ingredients or a separate preservation product.

The scene assumes no interruption. If an interruption does occur, record completed work and the actual material state under the crafting framework before resuming the same order. It does not grant a completion roll, another first-craft award or a fresh batch of ingredients.

## 4. Roll once and finish the batch

At 11:00, with work and reservations satisfied, Mira rolls **10** on the d20:

**10 + WIS 0 + PB 2 + tools 0 + facility 0 + assistants 0 = 12.**

The margin is **12 − DC 10 = +2: Standard**. Use crafting's own outcome table. Make one roll for the batch, not one roll for each dose.

Record the resulting inventory changes once:

- Consume the four Purified-water units and the one sparkling petal. Neither is a catalyst, so no catalyst returns.
- Create **five sealed doses**, each with 0.1 lb compound in one 0.1-lb vial: **1 lb total**. Each vial has AC 13 and current/max structural HP 1.
- Release the **two unused empty vials**, totaling 0.2 lb, to ordinary inventory. The finished doses plus those unused vials weigh **1.2 lb**.
- Keep the actual borrowed or owned tools in their existing ownership and condition. Excess process mass is waste, with no automatic ingredient, food, salvage or resale identity.

This is Mira's first successful craft of recipe-200. Her Herbalism level 1 is below the recipe's trivial threshold 9, so she gains **4 trade XP**, reaching **Herbalism 1, 4 XP**. Advancing from trade level 1 requires 11 XP; she does not advance. This award supplies no character level or class selection.

Write the work-order ID and `recipe-200` in her first-success history. A later nontrivial successful batch of the same recipe normally grants 2 XP, not another first-success award. Changing vials, ingredients through a legal substitution, or quality does not reset that history.

## 5. Compare possible outcomes

Each row is an alternative to the same completion roll above. These are not additional attempts, products or XP awards in the continuing scene. The seven-vial reservation is already satisfied in every row.

| Natural die / total | Margin | Result and choice |
|---|---:|---|
| 5 / 7 | −3 | **Flawed:** floor(5/2) = **2 ordinary-strength doses**; five empty vials remain unused. Their poison-save benefit still lasts the normal ten minutes. |
| 13 / 15 | +5 | **Exceptional:** choose **6 doses**, or **5 doses with every finished vial at current/max HP 2**. Never combine the choices. |
| 20 / 22 | +12 | **Masterwork:** choose **7 doses**, or **5 doses with every finished vial at current/max HP 2**. The natural 20 supplies no extra outcome-band shift. No catalyst can return because this batch contains none. |
| 3 / 5 | −5 | **Failed:** no doses. Recover 25% of the non-catalyst inputs under their unit rules: **1 Purified-water unit** and **0 whole sparkling petals**. All seven independently reserved empty vials remain unused. Recovered water retains its identity, condition and age. |

All successful doses have the same printed effect. Exceptional or Masterwork quality does not strengthen the cure, lengthen its duration or create equipment-grade bonuses. Improved vial HP protects the container; it is not an extra dose. A natural 1 would instead be a **Mishap**, requiring that procedure rather than the ordinary Failed recovery above.

A failed or Flawed attempt does not automatically earn success XP. The framework's one-XP research option requires its actual recipe/trade-level condition, consumed materials and work, a concrete usable finding, and the once-per-recipe-per-trade-level limit.

## 6. Administer one of the five doses

Continue from the **Standard result**, with five sealed doses. Later, Mira has one dose already accessible, one free hand and an available Action. A willing living companion within 5 feet can swallow it. For this example the companion has one removable Poisoned application, no prohibition on this remedy, and no continuing exposure that would reapply it. The legal administration below resolves at **12:00**.

Mira spends **one Action** to feed the dose to that companion. The entire dose is committed to that recipient at legal administration start. On resolution, the removable Poisoned application ends and the recipient gains **advantage on saving throws against poison for ten elapsed minutes**, expiring at **12:10**. No crafting check, Herbalism check, RP, spell rank or concentration is required to administer it. Administration grants no manufacturing XP, adds no ordinary-spell repetition, and does not reset remembered spell history.

The party now has **four sealed doses** (0.8 lb), **the two unused empty vials** (0.2 lb), and **one intact spent-dose vial in Mira's hand** (0.1 lb): **1.1 lb** across those objects. The spent vial has no magical use or recovered ingredient value; its actual structural HP remains. It can serve as ordinary supplementary packaging again if intact. The container does not move into the patient's inventory merely because the patient drank the contents.

For a different patient with an ongoing poison, ending removable Poisoned applications would leave the underlying cause intact; a later reapplication needs that cause's own real trigger. The antidote supplies neither poison immunity nor poison resistance, and its Cold recipe tag supplies no cold protection. Multiple advantage sources do not stack.

Opening a vial earlier would start its separate **one-hour open-container potency clock**; resealing it would not reset that deadline. The ten-minute benefit begins when administration resolves, not when the vial is opened or crafted. An intact sealed dose keeps its potency indefinitely under ordinary storage. Use the full Herbalism procedure for suppression, interruption, incompatible recipients and source-specific restrictions.

## Keep the record between scenes

The continuing example ends with Herbalism 1 / 4 XP, recipe-200 marked as successfully made, four unused doses, three ordinary empty vials in their actual locations, the consumed ingredient entries, and two hours of recorded work. Transfer shared stock to a carrier explicitly and recalculate that character's real load. This inventory change does not refill HP/RP, supply a rest, reset spell history, or create complete expedition Supply.

For another craft, begin with the actual recipe's skill level, formula access, station, component identities, time and reviewed output card. Mira's eligibility for this level-4 recipe does not let her attempt the next level-5 formula without its higher trade eligibility and formula access.
