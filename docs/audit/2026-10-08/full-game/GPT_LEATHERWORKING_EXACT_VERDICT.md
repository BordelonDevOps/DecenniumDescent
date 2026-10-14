# Exact Leatherworking review — Calibration Review Part 2

Thread: `6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b`  
Turn: `2a3db078-0ab3-411a-a9d2-aeb19da8765e`  
Reply: `1f8a8f86-3d64-4665-8d7f-cd315727a240`  
Captured from the completed thread response. The reviewer archive link is preserved as returned; the archive has not been downloaded or independently inspected locally.

# Leatherworking exact-review verdict

**Conditional approval for all 44 authored operational PLAYTEST cards, subject to two finite validation-evidence repairs. Do not promote the submitted revision yet.**

The required repairs concern the **unselected-suit grade fixture** and the **rescuer’s casualty-Load fixture**. They do not require changing the recipe effects, nineteen body profiles, source-precedence decisions, carrying-relief model, or completed Blacksmithing rules.

**Implementing LW-ER01 and LW-ER02, passing the corrected validation and existing preservation/projection checks, and recording the final evidence permits promotion without another generic Leatherworking source conference or resubmission of unchanged cards.** A change beyond those repairs would reopen only the affected scope.

Until those conditions are satisfied, totals remain **218/687 reviewed, 469 remaining; public 138/433**. After lawful promotion of this set, they become **262/687 reviewed, 425 remaining; public 168/433**.

## 1. LW-ER01 — Correct the unselected-suit grade fixture and document the helper’s eligibility contract

### Finding

The shared guide correctly restricts the suit-grade candidate to the **selected, functioning, actually worn suit supplying the armor formula**. Recipe-319’s card also correctly distinguishes its formula-dependent AC enhancement from its separately wearing-dependent resistance.

However, the supplied validation contains:

```python
a = ref.defense(
    -1,
    [
        worn('Armor', 2, selectedArmorFormula=False, resistance='cold'),
        worn(bonus=2, suppressed=True),
    ],
)
```

It expects:

```python
{'enhancement': -1, 'resistances': ['cold']}
```

The helper inserts its first argument into the candidate list unconditionally:

```python
candidates = [] if suit_grade is None else [suit_grade]
```

Consequently, this example does **not** establish correct suit-grade eligibility. Under its apparent single-unselected-suit setup, the −1 grade should not enter the family. The test supplies no other selected suit that could lawfully provide that modifier.

This is an **evidence/interface defect**, not a reason to rewrite the guide’s correct rule.

### Required finite repair

The helper may remain a bounded calculation function. Document its first argument as:

> The already-validated grade modifier of the complete, functional, actually worn suit whose armor formula is selected, or `None` when no such modifier is eligible.

Then correct the unselected-suit fixture to supply `None`:

```python
a = ref.defense(
    None,
    [
        worn('Armor', 2, selectedArmorFormula=False, resistance='cold'),
        worn(bonus=2, suppressed=True),
    ],
)

assert a == {
    'enhancement': None,
    'resistances': ['cold'],
}
```

The fixture must explicitly assume that using the alternative AC formula while wearing this suit is otherwise legal. It must not invent that permission.

Retain separate assertions for the genuine negative-modifier cases:

| Actual eligible state | Expected family result |
|---|---:|
| Selected Crude suit; no positive eligible enhancement | −1 |
| Selected Crude suit plus a wearable with source `armorBonus:0` | −1 |
| Selected Crude suit plus an eligible +1 recipe enhancement | +1 |
| Unselected suit; suppressed accessory; no other eligible enhancement | No candidate |
| Unselected suit with an otherwise active printed resistance | Resistance remains, independently of AC |

“No candidate” means that this family contributes nothing to the final AC calculation. It does **not** mean inserting a phantom +0 into a comparison containing an actual negative modifier.

Alternatively, the helper may derive grade eligibility from an explicit suit-state object. That is acceptable but **not required**; this review does not demand a runtime equipment resolver.

**No recipe, Blacksmithing rule, equipment-grade table, or original source field needs alteration for LW-ER01.**

## 2. LW-ER02 — Replace the unsupported casualty Load in the rescuer example

### Finding

The supplied LW-12 assertion calculates:

```python
a['pounds'] + 140 == 155
a['load'] + 4 == F(11, 2)
```

The equipment subtotal is correctly **15 lb and 1.5 Load**. The additional **4 Load**, however, is not a casualty-Load value in the supplied governing body table:

| Expressed body size | Existing casualty Load |
|---|---:|
| Tiny | 1.5 |
| Small | 3 |
| Medium | 6 |
| Large | 12 |

The fixture does not identify a body size or document another contribution explaining the 4. Therefore, **155 lb / 5.5 Load is not a supported worked result as currently presented**.

The cards and shared guide already say the correct thing: the rescuer counts the body’s effective physical weight, its applicable casualty Load, and all equipment, without inheriting the transformed bearer’s container relief.

### Required finite repair

Use an explicit supported example. For the Tiny transformed-body case:

- Effective body weight: **140 lb**.
- Expressed size: **Tiny**.
- Existing Tiny casualty Load: **1.5**.
- Melded equipment: **15 lb and 1.5 canonical Load**.
- Other carried equipment: **none in this fixture**.
- Container relief: **inactive while melded**.

The correct totals are:

```python
assert total_pounds == 140 + 15 == 155
assert total_load == F(3, 2) + F(3, 2) == 3
```

The retained 140-lb body weight is consistent with the supplied transformation rule; Tiny size does not itself recalculate physical body mass.

A Medium-body variant would instead total **155 lb and 7.5 Load**. Additional rescuer equipment must be added explicitly, with its own pounds and Load, rather than concealed inside an unexplained casualty term.

The corrected example should also state that these totals must pass the rescuer’s actual handling limits and anatomy requirements. Numerical bookkeeping does not supply hands, a harness, or permission to carry that creature.

**Do not change the reviewed casualty-Load table to accommodate the old test. Correct the fixture, assertion, and generated report.**

## 3. Accepted exact-card scope

The following findings apply to the actual submitted cards, their shared paragraphs, operational projections, and the governing guides supplied in Part A.

### Numerical AC overlays and defensive arbitration

The eleven positive AC fields are correctly implemented as **separate authored overlays**, not falsely represented as wording recovered from the effect prose.

The accepted assignments remain:

**+1:** 306, 308, 309, 312, 314, 315, 653, 655.  
**+2:** 317, 318, 319.

The two public omissions remain individually traceable to **recipe-308, V5 ¶1731**, and **recipe-653, V5 ¶1717**. Their preserved effect paragraphs do not mention AC; their operational paragraphs separately declare the numerical-field overlay.

The nine zero-AC wearables correctly supply no recipe enhancement candidate. In particular, **289 and 301 remain zero; 319 remains +2**.

The submitted rules correctly retain one `equipment.defense-enhancement` family. They do not create additive Leatherworking and Blacksmithing families. One selected shield’s ordinary bonus remains separate. Accessory eligibility requires its complete functioning item in the appropriate worn benefit slot, and the Gloves/Gauntlets handwear-slot exclusion remains intact.

The seven resistances are correctly retained:

**Force:** 312, 314.  
**Thunder:** 315, 317.  
**Cold:** 318, 319, 655.

They protect the wearer, not automatically the equipment or contents, and they remain independent of which eligible AC enhancement wins. The unselected-suit distinction is correctly written in the manuscript; LW-ER01 repairs its test.

### Complete coverage of all 44 recipes

| Family | Recipes covered | Accepted binding |
|---|---|---|
| Backpack | 280, 286, 287, 293, 297, 303, 652 | Existing 30-lb/1-ft³ body; separately retained R10, R20, or R30 |
| Pouch | 281, 285, 290, 295, 302, 311 | Exact 10-, 20-, or 30-lb cargo-pouch body |
| Quiver | 283, 292, 305, 313 | Exact 10-, 30-, or 40-lb body with independent sleeves |
| Belt | 291, 300, 304, 307, 310, 316 | Exact 10-, 20-, 30-, or 50-lb body with independent pockets |
| Harness | 654 | The defined 50-lb retaining cradle, not a Climber’s kit |
| Boots | 282, 308, 309, 312, 314, 318, 653 | One matched pair, footwear slot, exact bounded task/AC/resistance fields |
| Gloves | 284, 294, 298, 299, 306 | One matched pair, shared handwear slot, exact handling scope |
| Leather Gear | 288, 296, 315, 317 | One mobility vest, not a saddle or collection |
| Armor | 289, 301, 319 | Leather, Studded leather, or Hide; Padded excluded |
| Coat | 655 | One lined leather/hide coat, outerwear-benefit slot |

No family requires another generic source decision before these exact cards can be promoted under the stated conditions.

### Physical geometry, relief, and custody

The submitted model correctly separates **mundane physical capacity** from **magical encumbrance relief**. Suppression therefore changes burden, not the available storage dimensions.

The twelve container profiles retain finite weight, volume, opening, exterior-envelope, and compartment requirements. The quiver and belt cannot borrow another compartment’s unused space to admit an oversized object. The pouch-body enlargement is explicit rather than silently restricting a promised 20-lb allowance to an ordinary 6-lb pouch.

The five relief positions are correctly bounded by actual fit and anatomy. An externally lashed second backpack is neither a second active back-cargo item nor interior contents of the first.

The accepted arithmetic remains:

```text
counted carrying pounds = actual carried pounds − covered pounds

Load credit per canonical record =
    min(canonical Load, covered pounds / 10)
```

Actual mass and canonical Load are preserved. The active container does not relieve its own body. An enclosed enchanted container supplies no independent relief, while an eligible outer container may cover its inner body and descendants once.

The printed-Load exception is correctly handled: a **1-lb item with 3 Load retains at least 2.9 Load** after relief of that pound. Inclusive waterskin weights are not charged again as separate water.

This accounting permission does not authorize replacing unrelated physical records with a newly invented aggregate record to change their Load credits. Source-authorized inclusive quantities and their actual coverage remain controlling.

### Suppression, Broken containment, melding, and return

The manuscript correctly distinguishes the two loss-of-function cases:

**Suppression** removes the recipe benefits without shrinking the body, spilling contents, repairing damage, or deleting inventory. Excess burden becomes overloaded custody.

**Broken containment** releases immediate contents through actual support and placement resolution. An intact inner bag remains one subtree; its descendants do not also spill independently. The Broken outer body remains a physical possession until removed.

The intact-support exception must remain a real premise, not an arbitrary relocation parameter. The bounded helper may receive that premise from the governing placement system; it does not itself prove which container or restraint physically supports the released cargo.

Voluntary meld preflight correctly uses **full physical pounds and canonical Load**, not relieved values, against the fixed ordinary ceilings. Mandatory transformation retains the existing overflow procedure and supplies no overload-based immunity. On return, existing external equipment keeps priority, and a returned stowed container does not reactivate merely because it formerly occupied a relief slot.

The no-pass-through rule for a rescuer is correctly authored. LW-ER02 corrects the worked number, not that rule.

### Task scope, operators, and action costs

The wearable task scopes remain finite and match the conference decisions. The container bonus correctly belongs to the **actual operator performing the qualifying handling task**, including an ally or a thief, without creating an ownership lock.

The shared `equipment.leather-task-enhancement` family applies the strongest qualifying Leatherworking bonus once. It does not erase independently applicable reviewed class or tool rules, double proficiency, or convert the bonus into a saving-throw, attack, initiative, general Stealth, or Perception modifier.

Routine retrieval does not acquire a check. Ordinary interactions, second-interaction Actions, explicit activations, Secure Cargo Actions, actual hands, and access remain required.

### Crafting, durability, repair, and economics

The ordered maximum-yield reserve correctly requires complete supplemental bodies before work. Failed and Mishap outcomes do not transform those bodies or also return them as fractional ingredient recovery. Latest lawful completion HP controls, rather than freezing the reservation snapshot.

All **201 component occurrences remain consumed**, with no catalyst or tool-role substitution. Masterwork therefore has no eligible catalyst return in this set.

The noncompounding durability procedure is correct: ordinary B first, strongest positive workmanship percentage next, one persistent flaw last, then preservation of the latest damage deficit. Neither repair nor suppression erases the flaw. A singleton can lawfully emerge Broken with a dormant imprint.

Pair reconstruction correctly requires both original members. Functional repair uses the mundane base reference; HP0 reconstruction uses the undamaged finished unit reference. Neither teaches the formula or awards crafting XP.

The work mappings, assistant caps, false field-crafting flags, and exact triviality thresholds are retained. Recipe-319 preserves its source null and zero labor field while separately using the 1,920-hour overlay, or **86,400 active minutes for an eligible Forge Dwarf**.

All fifty submitted per-model finished-value examples agree with the source batch reference divided by Q once, plus the applicable ordinary body reference. Repair-material quotations still receive the existing transaction rounding at purchase. For example, **93/8 gp is an exact reference calculation; an actual purchase at that amount rounds upward to 11.63 gp**, not downward.

Recipe-653 gains no acid resistance from its title. Recipe-655 gains no climate immunity or automatic temperature-endurance success.

## 4. Independent checks performed here

I kept these checks separate from the reported local 89-check pass.

| Check performed here | Result |
|---|---|
| Re-execution of the supplied durability sweep | **2,832 states; no failures** |
| Re-execution of the supplied burden sweep | **1,065 states; no failures** |
| Separate rational durability comparison including Crude Hide’s B=7 | **3,090 total states; no failures** |
| Source-control and finished-reference calculations | **44 recipes; all 50 per-model value examples agree** |
| Internal/public model membership | **19 internal models; 14 public models** |
| Public paragraph-reference routing | **570 references across 30 cards; no field-routing mismatches** |
| Additional explicit-premise checks | Corrected grade eligibility, all four casualty sizes, nested support retention, immediate-subtree release, return-slot priority, and inclusive waterskin accounting passed |

The **3,090-state** enumeration includes the original 2,832 states; it is not an additional disjoint set of that size.

The public reference map is internally consistent with the **837-paragraph internal structure**. In particular, `I442 → 836` resolves to the reusable `{"wholeCreatureUse": true}` metadata paragraph. Its use on public recipe-653 does not import recipe-655’s private card.

The public routing check used per-card field/category signatures. It is distinct from your local assertion that the reconstructed manuscripts equal their saved files byte-for-byte.

Likewise, the supplied working-copy hashes and the **42 protected-file comparisons remain your local evidence**. I did not reopen or independently hash those working-copy files here. The conditional verdict does not misattribute those checks to this review.

The calculation helpers remain bounded evidence. They are not a companion implementation, a universal packing algorithm, an equipment-permission resolver, or proof of whole-game flow.

:chatgpt-content-reference{index="0"}[Internal reviewer scripts and evidence](sandbox:/mnt/data/leatherworking_exact_review_evidence.zip)

This archive contains internal recipe control fields and must remain outside the player-facing projection.

## 5. Promotion authorization and release conditions

**The only required corrections from this exact review are LW-ER01 and LW-ER02.** Existing preservation, projection, and release gates still apply.

Preserve the submitted revision and this final verdict as separate audit evidence. Correct the two fixtures and their generated results, document the `suit_grade` precondition or implement its finite eligibility check, and rerun validation.

Before the aggregate index changes, verify the complete source records, the unchanged protected-file baseline, the exact 30/1/13 visibility split, the fourteen-model public projection, and public/internal operational equality. Regenerate any paragraph-reference material affected by edits. Do not substitute a broad assertion that old tests passed for the corrected results.

Once those checks pass, record the fulfilled repair receipt and final artifact/evidence hashes, and update only the operational review status and associated review records to:

**REVIEWED — authored operational PLAYTEST Leatherworking recipe set.**

Original `status`, `needsReview`, `needsReviewReason`, legacy fields, visibility, source nulls, and source economy fields remain untouched. Historical source-conference text remains historical direction, not retroactively rewritten as exact-card approval.

**Promotion of all 44 cards is then authorized without another generic conference or re-review of unchanged content.** The aggregate may advance to **262/687**, with **425 remaining**, and the public aggregate to **168/433**.

This grants no human balance approval, ingredient-availability certification, companion runtime parity, whole-game flow approval, or publication authorization. Final joint flow review still precedes GitHub delivery. Cosmology remains deferred until the authorized push succeeds and its remote commit is verified.
