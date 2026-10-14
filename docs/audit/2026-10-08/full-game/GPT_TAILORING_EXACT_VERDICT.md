# Captured GPT exact Tailoring verdict

Thread: 6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b
Turn: b6984844-5544-4ff0-9624-50bab432dbb2
Reply: 54b2b40e-cce6-48c4-8aa6-51ea7c535f0c

Capture: MCP literal Markdown up to the paragraph preceding “My routing check”; the remaining visible response was transcribed from the existing Chrome notebook. Browser formatting is normalized to plain paragraphs, with the download-button filename added in brackets. The separate MCP prefix preserves the exact truncated transport response. This is a complete readable verdict, not a byte-identical Markdown export. Downloaded evidence remains in this internal audit directory.

---

# Exact Tailoring review — verdict

**Conditional approval for all 43 authored operational PLAYTEST cards, subject to TA-ER01–TA-ER04 below. Do not promote the submitted revision yet.**

The required corrections concern **item-specific task qualification, actual-operator routing, validation fixtures, and explicit physical-tool requirements for repair**. They do not require changing the 43 recipe effects, fifteen body profiles, seven resistance assignments, carrying-relief arithmetic, source visibility, or source economy fields.

**Implementing these four finite repairs, passing the corrected validation and existing preservation/projection checks, and recording the final evidence permits promotion without another generic Tailoring conference or resubmission of unchanged cards.** Changes beyond this scope reopen only the affected scope.

Until those conditions are fulfilled, totals remain **262/687 reviewed, 425 remaining; public 168/433**. After lawful promotion, they become **305/687 reviewed, 382 remaining; public 197/433**.

## 1. TA-ER01 — Make task qualification item-specific before choosing the strongest bonus

### Finding

The source conference requires the **particular garment** to contribute to the actual task. The shared guide also excludes hidden clothing from visible presentation.

However, `tailoring_task_bonus` evaluates these premises once for the entire task:

```python
task.get('actualContribution')
task.get('visibleAttire')
task.get('coverageSufficient')
```

It then considers every otherwise eligible worn item whose family admits that domain. Consequently, a contributing item can supply the circumstances that allow an unrelated, stronger item into the comparison.

I reproduced this with two source-valid items in different legal benefit positions:

| Item | Actual circumstances | Eligible presentation modifier |
|---|---|---:|
| Recipe-682 Cloak | Visible and materially contributes to the declared presentation | +2 |
| Recipe-584 outfit | Correctly worn, but concealed and not contributing to that presentation | None |

With the task-wide contribution and visibility flags set for the Cloak, the supplied helper returns **+3**. The correct task result is **+2**.

The outfit’s otherwise eligible radiant resistance remains active. Being irrelevant to a presentation check does not suppress its independent resistance.

### Required finite repair

Associate contribution, relevant coverage, visibility, and any other item-dependent task premises with **each physical candidate**, rather than borrowing them from another item.

Either of these bounded interfaces is acceptable:

- Pass item-specific eligibility premises keyed by physical item ID.
- Pass an explicitly prefiltered task-candidate list, with the filtering contract and its application demonstrated in validation.

The second option must actually filter candidates before comparison; merely documenting a precondition while the cross-trade wrapper continues passing an unfiltered equipment list is insufficient.

Keep equipment-state and shared-slot validation separate. Filtering out an item that does not help this check must not legalize two simultaneously designated competing items.

Add an explicit shared-guide clarification that **each candidate must independently satisfy its own task relationship before the strongest-value comparison**. This restates TA-D05; it creates no new task domain.

The corrected evidence must establish that a hidden or noncontributing stronger garment cannot override a qualifying weaker one, that two genuinely qualifying items use the stronger value once, and that losing task eligibility does not remove an independently active resistance. Apply the same item-specific distinction to Bag operation and cross-trade candidates.

**No general-purpose task detector or companion equipment resolver is required. Actual circumstances may remain governing-system premises, but they must identify the item to which they apply.**

## 2. TA-ER02 — Route Leatherworking container benefits to the actual operator

### Finding

The new cross-trade wrapper uses:

```python
r.get('wearer', r.get('operator')) == task.get('actor')
```

When a container record has both fields, `wearer` always takes precedence. That is incorrect for a container’s operator-dependent benefit.

I reproduced a functioning, accessible Leatherworking Backpack with a printed +2 task bonus, worn by **A** but actually operated by **B** during a qualifying cargo-handling check. The wrapper returns **0** for B instead of **+2**.

The existing Leatherworking rule is correct: its qualifying container bonus belongs to the actual operator, not automatically its wearer, owner, or bearer.

### Required finite repair

Choose the actor field according to the item’s benefit:

```python
container = r["family"] in {
    "Backpack", "Pouch", "Quiver", "Belt", "Harness"
}

benefit_actor = r.get("operator") if container else r.get("wearer")
```

Then compare that actor with the check’s actual actor and apply the item’s own eligibility and task scope. Do not use wearer or ownership as an operator fallback.

Retain Tailoring’s existing distinction between wearer-dependent garment benefits and operator-dependent Bag benefits.

Validate a container operated by someone other than its wearer, a wearer operating their own container, and a nonoperator who receives no bonus merely by wearing or owning it. Existing access, functional-state, hand, action, and task requirements still apply.

**Repair the new cross-trade wrapper and its evidence. Do not rewrite the reviewed Leatherworking task rules.**

## 3. TA-ER03 — Replace unsupported fixtures with source-valid, physically lawful cases

The supplied report passes its assertions, but several fixtures do not represent the source-valid equipment states their labels suggest. Correct the fixtures rather than changing cards to match them.

### A. Correct the nested-container fixture

The submitted nested case creates both `inner` and `outer` from the same **10-lb Bag** fixture.

Under the submitted body profiles:

| Quantity | Dimensions |
|---|---|
| Outer Bag’s usable interior | 12 × 8 × 6 inches |
| Inner Bag’s occupied exterior | 13 × 9 × 7 inches |

The inner envelope occupies **819 cubic inches**, while the outer compartment provides **576 cubic inches**. No orthogonal orientation fits. The fixture supplies no separately authorized folding or changed-configuration premise.

The helper may accept packing legality as an external premise, but this particular fixture does not establish it.

Use the already authorized positive example: a small Tailoring Bag inside a reviewed Leatherworking Backpack. The inner envelope fits the Backpack’s **18 × 12 × 8-inch** interior, with its **9 × 7-inch** cross-section passing through the **12 × 8-inch** opening.

For an explicit fixture containing no other equipment:

| Record | Physical pounds | Canonical Load |
|---|---:|---:|
| Active Leatherworking Backpack, R10 | 5 | 0.5 |
| Enclosed Tailoring `bag-10` body | 1 | 0.1 |
| The declared fitting 1-lb/3-Load object | 1 | 3 |
| **Total** | **7** | **3.6** |

The outer allowance covers the inner body and object once:

```text
Covered pounds = 2
Load credit = 0.1 + 0.1 = 0.2
Counted carrying pounds = 5
Effective Inventory Load = 3.4
```

The enclosed Bag supplies no independent relief.

I tested this replacement accounting and immediate-subtree release. Retain explicit fit, access, support, and placement premises when regenerating the nested/Broken cases. Suppression preserves the same physical inventory and restores its unrelieved **7 lb / 3.6 Load**.

**Do not enlarge `bag-10`, shrink its exterior, or introduce implicit compression to rescue the old fixture.**

### B. Correct the source-specific effect fixtures

| Submitted fixture | Problem | Finite correction |
|---|---|---|
| `acid = item(resistance='acid')` | The factory defaults to a Tailoring Cloak. No Tailoring Cloak has printed acid resistance. | Use recipe-577 or recipe-580 with its actual Garment body and body-clothing position. |
| `tablebag` copied from the 10-lb Bag, then assigned `bonus:2` | Recipes 546 and 552 have +1. | Test a source-valid small Bag at +1, or use a correctly modeled recipe-573 Bag at +2. |
| `leather_glove` assigned `bonus:3` | The reviewed Leatherworking Gloves controls do not supply a +3 Gloves profile. | Use a source-valid qualifying Leatherworking item and its actual printed modifier. For example, recipe-306 Gloves use +2, not +3. |
| Recipe-548 reconstruction context supplied DC12 | Its original recipe DC is 11. | Supply **11**, and assert the returned reconstruction DC. |
| Recipe-584 reconstruction context supplied DC30 | Its original recipe DC is 28. | Supply **28**, and assert the returned reconstruction DC. |

The last two errors do not invalidate the material-cost arithmetic already demonstrated. They mean those named fixtures have not established the correct recipe-specific reconstruction DC.

The same principle applies to fixtures described as actual Hat, Helm, Gloves, or Gauntlets examples: use the correct family metadata and source profile rather than relying on an unrelated factory default.

Purely synthetic arithmetic tests may remain separately labeled as such. They must not substitute for the source-bound behavior cases or imply that the invented combination is an available item.

**The manuscript’s recipe DCs and resistance assignments are correct. Change the evidence, not those source/card fields.**

## 4. TA-ER04 — State the actual Weaver’s toolkit requirement in the repair procedure

### Finding

TA-D14 explicitly requires **actual Weaver’s tools**, the Loom and Cutting Table, Needles, and Shears for both repair routes.

The submitted shared guides and card Repair paragraphs name **Weaver’s-tools proficiency**, the station, Needles, and Shears, but omit the separate physical toolkit from their repair-specific requirement.

A proficiency credential is not possession of the toolkit. The creation paragraph’s toolkit requirement should not have to supply this missing repair prerequisite by implication.

### Required finite repair

Update both shared guides and the shared/card Repair paragraphs to explicitly require:

**Actual Weaver’s tools, using the Tailor’s-tools binding; an actual Loom and Cutting Table; and the required Needles and Shears.**

Preserve the reviewed rule allowing the same actual implement to satisfy compatible overlapping requirements. This correction does not require buying duplicate ordinary implements.

Also preserve the distinction that the original rare reusable recipe-tool rows are **creation requirements**, not additional generic repair or reconstruction requirements.

Record the physical toolkit prerequisite in the repair validation contract. A trained character without the required actual toolkit cannot begin the procedure merely because the numerical quotation can be calculated.

**`repair_terms` may remain a bounded quotation/calculation helper. It need not become a complete repair-permission resolver.**

## 5. Accepted exact-card scope

Subject to those finite corrections, the submitted authored rules implement the source conference without requiring another source decision.

### All 43 identities and fifteen body models

| Family | Recipes covered | Accepted body binding |
|---|---|---|
| Bag | 546, 552, 573, 578, 583 | The corresponding 10-, 30-, 40-, or 50-lb fitted textile Bag |
| Cloak | 547, 550, 553, 567, 682 | One Hooded cloak |
| Gloves | 548, 557, 558, 559, 561 | One complete matched textile pair |
| Hat | 549, 554, 566, 574 | One fitted textile Hat |
| Garment | 551, 555, 556, 560, 563, 568, 569, 571, 572, 575, 576, 577, 579, 580, 582, 584 | One of the four complete outfit models |
| Robe | 562, 564, 565, 570, 581 | One fitted textile Robe |
| Cord | 680 | The defined clothing girdle |
| Veil | 681 | The defined face Veil |
| Mantle | 683 | One short textile shoulder Mantle |

The **15 internal / 11 public** model membership is correct. The Tailoring-specific Large garment overlay doubles only body price, weight, and ordinary HP. Bags retain their fixed profiles. Original referenced equipment sizing fields remain separate from that overlay.

The source garment modifier distribution is correctly retained: **23 at +1, eleven at +2, and four at +3**.

### AC, resistance, and wearing layers

Tailoring correctly supplies **no AC candidate**, including no phantom +0 capable of canceling a selected Crude suit’s −1. Cloth structural AC11 is an object defense, not a creature armor formula.

All seven resistance assignments are correct:

| Type | Recipes |
|---|---|
| Acid | 577, 580 |
| Poison | 579, 683 |
| Thunder | 581 |
| Bludgeoning | 582 |
| Radiant | 584 |

Recipe-582 correctly includes **magical bludgeoning damage**. It grants neither additional damage types nor immunity to nondamage pressure, restraint, or displacement. Poison resistance remains distinct from Poisoned immunity.

The shared positions correctly exclude simultaneous designated benefits from Hat/Helm, the three handwear alternatives, Garment/Robe, and Cloak/Mantle/Coat. Veil and Cord do not create additional cargo positions. Compatible armor, clothing, vest, and outerwear retain their actual fit and use restrictions.

The minute-based outfit/Robe donning and doffing, Action-based accessory handling, and Action-based refitting of already-worn compatible competing layers are retained. Refitting does not bypass an obstructing item’s removal requirements.

### Task scope and the four specifically named items

The authored family domains are appropriately bounded. They do not create universal Persuasion, Stealth, Survival, or exposure bonuses; saving throws remain excluded.

The distinction between the wearer, a separate disguise-maker, and an observer is correct in the prose. Bag organization and concealment remain actual-operator tasks rather than ownership benefits or Leatherworking retrieval aliases. TA-ER01 and TA-ER02 repair their calculation interfaces.

Recipe-680 remains a clothing girdle, not a climbing line, casualty hoist, restraint, or Climber’s kit. Recipe-681 supplies actual facial coverage, not a complete disguise or gas filter. Recipe-682 creates no darkness, invisibility, or acid resistance. Recipe-683 remains equipment, with no companion status, regeneration, harvesting, independent action, or Poisoned immunity.

### Carrying, custody, suppression, and transformation

The manuscript correctly separates physical capacity from relief allowance and retains:

```text
Load credit per canonical record =
    min(canonical Load, covered pounds / 10)
```

Actual pounds and canonical Load remain unchanged. Container bodies do not relieve themselves; an enclosed enchantment supplies no second allowance; external lashings are not interior contents. Unknown or merely estimated physical mass does not establish pound-relief eligibility.

The shared five-position limit, direct-bearer requirement, actual holding hands, transfer behavior, and lack of stored or rechargeable relief are correct.

Suppression preserves containment and produces any resulting overloaded custody. Broken containment instead releases immediate contents through actual support and placement. An intact inner Bag remains one subtree. Pending placement, elevation, falling, and the retained Broken body are correctly distinguished.

Voluntary meld preflight uses full physical pounds and canonical Load, without either trade’s relief. Mandatory transformations retain the existing overflow procedure. Melded items remain inaccessible, return-slot priority is preserved, and rescuer accounting receives no pass-through relief.

### Ordered bodies, ingredients, tools, and durability

Maximum-yield reserves, their stable ordering, pre-roll replacement positions, and use of the latest lawful completion state are correct.

Recipe-548 correctly requires seven complete pairs in reserve, transforms five at Standard or seven at Masterwork yield, and does not turn its 1.68 lb of consumed process inputs into additional body stock.

All **190 displayed component occurrences** reconcile to **165 consumed occurrences and 25 reusable tool occurrences**. The reusable tools retain their actual 1-lb weights and price references, including the four 54,000-gp occurrences. They do not become consumed reinforcement, output mass, recovered duplicates, or catalysts.

The noncompounding durability procedure is correct: ordinary B first, strongest positive percentage next, one persistent flaw last, then preservation of the latest damage deficit. A source-Q≥2 Flawed result does not acquire a new singleton flaw merely because the reduced output is one item.

A B5 body at 1/5 HP may correctly emerge singleton-Flawed at **0/2 HP**, with a dormant imprint. Repair and suppression do not erase the flaw. Pair and outfit reconstruction correctly require the necessary original members or constituents.

### Work and economic references

All eleven preserved `timeMode:"field"` records remain blocked from portable field crafting by their false `fieldCraftable` flags. Exact assistant caps, access fields, work totals, and capped triviality thresholds are retained.

Recipe-584 preserves its source null, literal year, and zero labor field while separately using **1,920 active hours**, or **1,440 hours / 86,400 active minutes** for eligible Forge Dwarf creation. The phase and replacement-lot wording does not retroactively stabilize ingredients or shorten repair, rest, preservation clocks, or independent calendar waits.

All **91 ordinary** and **91 Large-profile** finished-reference examples agree with:

```text
source Standard batch reference / source Q
+ actual undamaged mundane body reference
```

These are 91 combinations evaluated at each fitting treatment, not 182 distinct body models.

Functional repair correctly uses the mundane body reference; reconstruction uses the undamaged finished-unit reference. Recipe-584’s common-outfit reconstruction materials are exactly **124,640.625 gp**, purchased at **124,640.63 gp** after the reviewed rounding. Its correct reconstruction DC remains **28**.

Finite buyers and actual quotes remain necessary. No automatic artifact multiplier, quality premium, reusable-tool reimbursement, or mundane-table magic-item buyback has been introduced.

## 6. Independent checks performed here

I kept these separate from your reported local 120-check pass.

| Check performed here | Result |
|---|---|
| Source/control and submitted work/quantity calculations | 43 recipes; no discrepancies in the transcribed controls |
| Finished-reference calculations | All 91 ordinary and 91 Large-profile examples agree |
| Displayed component arithmetic | 190 rows; all 43 consumed-value and consumed-weight totals agree |
| Internal/public model membership | 15 internal; 11 public |
| Public paragraph routing | 550 references plus one final literal metadata paragraph; no field-routing mismatches |
| Internal/public paragraph structure | 819 internal paragraphs; 554 public paragraphs |
| Durability sweep against a separately tabulated maximum-HP oracle | 558 states; no durability failures |
| Complete-order quantity/option enumeration | 40 combinations; ordered identity, unused bodies, and singleton-flaw behavior agree |
| Supporting predicate/fixture assertions | 396 pass; the two helper counterexamples above were separately reproduced |

The 396 assertion count includes summary assertions for the sweep and order enumeration; these counts are not disjoint totals to add together.

Seven public references reuse generic paragraphs first occurring on private cards. Their content matches the receiving public cards. For example, `I233` and `I234` correctly supply the ordinary +2 Garment effect and operational paragraph for public recipes 575 and 576. They do not import recipe-571’s private identity, ingredients, value, or guidance.

My routing check used paragraph field/content signatures. It is not a claim that I reconstructed and independently hashed your saved manuscripts byte-for-byte.

Likewise, the original-file hashes, full working-copy source equality, reported version comparisons, and 53 protected-file comparisons remain your local evidence. I did not execute the complete working-copy validator with its unavailable builder and repository files.

Internal reviewer calculations, counterexamples, and projection evidence
[Browser download button: tailoring_exact_review_evidence.zip]

This archive contains restricted/Director-only control fields and must remain outside the player-facing projection.

7. Promotion authorization and release conditions

TA-ER01–TA-ER04 are the complete required correction list from this exact review.

Preserve the submitted revision and this verdict as separate audit evidence. Apply the scoped helper, fixture, and repair-wording corrections; regenerate affected validation results and manuscript references.

Before changing the aggregate index, verify the complete source records, all 190 component occurrences, the unchanged 53-file protected baseline, the exact 29/4/10 visibility split, the 15/11 model membership, and public/internal operational equality. Regenerate and verify any paragraph projection affected by the edits, then record the fulfilled-repair receipt and final artifact/evidence hashes.

Once those conditions pass, promotion of all 43 cards is authorized to:

REVIEWED — authored operational PLAYTEST Tailoring recipe set.

Update only operational review status, approval flags, and associated exact-review provenance. Preserve original source status, needsReview, needsReviewReason, nulls, absent fields, legacy fields, visibility, component records, and economy fields. The historical TA-D01–TA-D16 conference remains source/interface direction, not retroactively rewritten as exact-card approval.

No further generic Tailoring conference or re-review of unchanged cards is required after those repairs and checks.

This grants no human balance approval, ingredient/tool-availability certification, companion runtime parity, whole-game flow approval, publication authorization, or GitHub push. Final joint flow review remains a later gate. Cosmology remains deferred until the authorized GitHub push succeeds and its remote commit is verified.
