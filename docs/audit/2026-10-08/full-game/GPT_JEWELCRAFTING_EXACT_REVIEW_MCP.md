**Conditional approval with three required repairs before promotion.**

:chatgpt-content-reference{index="0"}[Complete UTF-8 Markdown verdict](sandbox:/mnt/data/jewelcrafting_exact_review_verdict.md) · :chatgpt-content-reference{index="1"}[Internal reviewer evidence, including reconstructed cards](sandbox:/mnt/data/jewelcrafting_exact_review_evidence.zip)

:::writing{variant="document" id="56942" title="Jewelcrafting exact-card review — conditional operational approval"}
# Jewelcrafting exact-card review — conditional operational approval

## Verdict

**CONDITIONALLY APPROVED for authored operational PLAYTEST, subject to JC-ER01–JC-ER03 below. Do not promote the submitted revision yet.**

This verdict covers all **43 internal cards, the 26-card public projection, both shared guides, the supplied operational profiles and body models, and the bounded reference evidence**. It does not reopen JC-D01–JC-D16 or authorize different effects, bodies, charges, quality improvements or cosmology.

**Completing these three repairs and the specified regression checks permits promotion of all 43 cards without another generic source/interface conference or an unchanged-card resubmission.** The conditions are finite; their completion must be documented against the corrected artifacts.

Until those conditions are fulfilled, totals remain **305/687 reviewed, 382 remaining; public 197/433**. All 43 Jewelcrafting cards remain pending promotion.

## Review findings and verified scope

I reconstructed the complete internal and public card manuscripts in separate reviewer copies. Both match the SHA-256 digests supplied in this packet:

| Reconstructed manuscript | Cards | UTF-8 bytes | SHA-256 |
|---|---:|---:|---|
| Internal | 43 | 365,630 | `097b406eccfd76548971351592b60f928d39a115570fda4823b933e061bdcf2a` |
| Public | 26 | 215,312 | `e1b771a57bdf71a8e8827706d111292c580ae0094675b7a164bd5edfa2f98ee3` |

This establishes agreement between my reconstructed manuscript copies and the packet’s reported digests. It is **not** a claim that I opened Codex’s local manuscript paths or independently fetched its saved files.

I also independently recomputed all **86 ordinary/Large finished references**, all **43 eligible Forge Dwarf creation-time calculations**, and the **486 structural-state cases**. Those checks passed. The submitted distributions remain 24 bonuses of +1, 12 of +2 and seven of +3; charge maxima remain distributed 15/9/7/5/6/1 across maxima 1–6.

The following dispositions remain accepted, subject only to the interface and evidence repairs identified below:

| Area | Exact-review disposition |
|---|---|
| Source identity and public routing | The supplied assignments retain 43 recipes, 200 component occurrences and eleven catalyst occurrences. Public routing remains recipes 241–265 and 268; recipe-270 is restricted; the other sixteen are Director-only. The public manuscript has no private card blocks. Nine public bodies and twelve public operative-tag entries are the correct selection. |
| Fourteen causal domains | Stealth, Flora, Poison, Unholy, Earth, Strength, Psychic, Arcane, Cold, Vitality, Lightning, Fire, Water and Acid retain JC-D03’s bounded predicates. The printed card predicates agree with the disposition. Theme, proximity, donor names and secondary tags do not create eligibility. |
| Roll exclusions and passive benefits | The modifier applies once to each independently qualifying roll by the actual wearer, including at zero charges. Concentration, death saves, attacks, damage, initiative, crafting, formal formula research, harvesting, repair and maneuver checks remain excluded. No AC candidate, resistance, proficiency or extra spell access is created. |
| Combination | The named shared check family and separate Jewelcrafting save family are correct. Independent item qualification precedes maximum selection. A weaker qualifying jewel may supply the single charge expenditure while another qualifying item supplies the flat modifier. JC-ER02 repairs the reference’s identification of that one actual check. |
| Bodies, slots and hands | The ten assigned bodies, Standard-only grade, Large scaling, single-piece Earring, mounted-Gem assembly, seven-position ceiling, two different Ring hands, head conflicts and actual supporting-host requirements remain accepted. Jewelry does not create hand, focus or transformation permissions. |
| Activation and control | The before-dice checkpoint, capable wearer’s voluntary choice, no separate action/Reaction/hand cost, ordinary advantage cancellation, no post-commit refund and same-event expenditure limit remain correct. Ownership does not lock passive benefits or authorize compelled finite-resource spending. |
| Dawn and custody | The fixed campaign dawn series, per-item initialization, same-timestamp creation checkpoint, missed suppressed/Broken/incomplete dawns and internal meld recharge follow the disposition. Melding suspends use; external equipment retains return priority. JC-ER01 repairs ordering between charge expenditure and dawn processing. |
| Creation and quality | Ordered complete-body reserves, latest lawful damage, first-N transformation, retained unused bodies, structural-only quality and persistent noncompounding flaws remain accepted. No charge improvement is authorized. Recipe-245’s seven-reserve case and recipe-242’s possible Broken singleton output remain valid. |
| Components, tools and work | Catalyst roles and the one-unit Masterwork limit remain intact, including the two distinct recipe-279 candidates. Actual tools/station, preservation and incorporation requirements remain necessary. The shared guide preserves otherwise legal untrained level-1–4 creation attempts; repair remains trained-only. False field flags, exact assistant caps and capped triviality thresholds control. |
| Repair and value | The actual-kit and original-primary-assembly requirements, limited subordinate-part replacement, unchanged charge ledger, binary repair outcomes and source batch/Q plus body references are correct. The recipe-268 card already prints DC19 correctly; JC-ER03 corrects its inconsistent test fixtures, not the recipe. |

I reviewed the complete supplied guide texts and logical public-envelope routing. The packet’s **saved guide/JSON-envelope equalities, complete original-object equality against its local source files, and 54-protected-file hash results remain reported local evidence**. I did not rerun the full submission validator against unavailable Codex-local inputs. The reviewer probes below are separately executed checks of the supplied function excerpts, not companion-runtime tests.

## JC-ER01. Enforce chronology across expenditures and dawns

**Affected interface:** `initialize`, `commit_charge`, `dawn`, their shared ledger contract and the corresponding evidence. Authority: JC-D07–JC-D09.

### Confirmed defect

`dawn()` orders dawn indices relative to other dawns, but `commit_charge()` records no chronological marker and does not require preceding due dawns to have been processed. A truthful historical dawn snapshot can therefore be applied after a later expenditure and overwrite its balance.

I reproduced this with the source-valid recipe-258 Earring, whose maximum is two charges, on an explicitly synthetic campaign timeline:

| Processing sequence | Final current charges |
|---|---:|
| Initialize at time 0; process dawn at time 10; commit an eligible spend at time 11 | **1 — correct** |
| Initialize at time 0; commit that time-11 spend; then process the time-10 dawn | **2 — incorrectly accepted** |

No source bonus, charge maximum or causal qualification was changed. The defect is acceptance of the second processing order. Recording actual state at the dawn does not, by itself, preserve a later charge transaction.

**The existing same-timestamp creation checkpoint is correct and should remain.** It prevents one particular replay; it does not close this expenditure/dawn ordering gap.

### Required repair

Give charge commitments and dawn updates an authoritative **ordered campaign-event checkpoint**, and retain the item’s processed ledger position. That checkpoint must distinguish scheduler order at a shared timestamp, rather than relying on seconds alone.

Before committing a charge, require all dawn events that precede that commitment to be resolved from their actual historical states. The adapter may process those events first, or reject the commitment pending that processing. It must not silently spend against an unresolved chronological state.

Reject a subsequently submitted earlier dawn or expenditure that would revise an already committed later ledger state. Preserve the existing rules for same-event debit rejection, initial creation, processed ineligible dawns and fixed epoch identity. Apply transitions to one authoritative ledger state; a copied return value is not a second inventory or an independent resource history.

This is enforcement of the already-authorized event-ordering rules, **not** a new cooldown, clock, recharge opportunity or Time Loop permission. The bounded helper may continue to receive scheduler checkpoints and historical state as external premises; it need not implement the campaign scheduler.

### Required checks

Demonstrate that the correctly ordered trace ends at one charge, while the spend-before-unprocessed-dawn trace is rejected or correctly normalized before expenditure. A late earlier dawn must not overwrite the subsequent spend.

Also retain and exercise creation immediately before and after a same-timestamp dawn in the scheduler’s actual order; legal spending on opposite sides of a real dawn; a missed suppressed/Broken/incomplete dawn; chronological multi-day processing; and rejection without ledger mutation for an invalid replay. Shared-timestamp ordering must not create additional actions or roll opportunities.

## JC-ER02. Bind cross-trade views to the same actual roll event

**Affected interface:** `combined_check_bonus` and its caller/fixture contract. Authority: JC-D03–JC-D04 and the reviewed item-specific Tailoring qualification rules.

### Confirmed defect

The adapter currently compares only actor, ability and proficiency before combining the Jewelcrafting event with `older_trade_task`. Those fields do not establish that two records describe the same check.

Using recipe-241’s +1 Bracelet and recipe-584’s +3 Garment, I supplied two individually meaningful DEX (Stealth) task records for wearer A: a current check where the Bracelet qualifies, and a different earlier check where the Garment contributed. The function accepted their combination and returned **+3**. Correct current-check evidence with no Garment contribution returned **+1**.

The same adapter also returned the older trade’s +3 when the Jewelcrafting event declared `actualRoll=False`, and when it declared `automaticResult=True`, because the separate older descriptor still said `actualCheck=True`.

These are interface-consistency defects. They do not require the helper to infer physical contribution or prove a world premise.

### Required repair

Use a shared canonical roll-event identity, or derive both views from one authoritative event object. Require agreement on the actual roll’s existence, kind, actor, ability, proficiency and automatic-result status before invoking either trade’s bonus calculation. Missing or inconsistent event identity must not be treated as proof of sameness.

Tie each item’s qualifying premises to that event. Do **not** require identical domain or predicate names between trades: a rock-climbing check can legitimately have different Earth and Leatherworking descriptions. What must match is the underlying check, not the descriptive vocabulary.

Continue validating all designations before candidate filtering. Preserve each trade’s actor, contribution, coverage, access and task restrictions. No new save route may reach the older trades, and this repair must not become a universal strongest-bonus rule for unrelated class, spell or tool benefits.

Implement the correction in the Jewelcrafting adapter or its new wrapper. Do not modify protected Tailoring or Leatherworking source/reviewed artifacts to accommodate it.

### Required checks

Reject different event IDs even when actor, ability and proficiency are identical. Reject missing identity and inconsistent roll-existence or automatic-result descriptors. Confirm that independent current-event premises still yield +3 for a genuinely contributing recipe-584 Garment and +1 when only recipe-241 qualifies.

Retain the source-valid recipe-306/649 climbing comparison. Add a same-event check showing the weaker eligible jewel spending its own charge while the stronger eligible older-trade item supplies the flat modifier, with exactly one debit and ordinary advantage cancellation. An unrelated or noncontributing stronger item must remain ineligible.

## JC-ER03. Correct the source-bound mounted-Gem repair fixtures

**Affected evidence:** the two recipe-268 missing-constituent assertions and their repair-profile setup. Authority: JC-D14–JC-D16.

### Confirmed mismatch

The submitted validator creates `gem = jewel(268, hp=0)` but passes **23** as `recipe_dc` in both missing-original-crystal and missing-primary-mount calls.

Recipe-268’s source and authored card specify **DC19**. DC23 belongs to recipe-275. Because the tests reject a missing constituent before returning the quotation, both can pass while concealing the incorrect recipe/DC combination.

The quotation helper accepts its supplied numerical terms. With the constituents present, the same erroneous argument produces a DC23 quotation for recipe-268. This is why the fixture must bind those terms correctly rather than relying on an unrelated negative gate.

### Required repair

Derive the test’s recipe DC and reference values from the selected actual source/card/model, or assert that exact binding before invoking the quotation. Change the recipe-268 fixture’s DC to **19**, and add a positive quotation using the same source-valid profile.

For the ordinary fitted, Broken recipe-268 mounted Gem at recorded maximum HP5, the expected terms are:

| Term | Correct value |
|---|---:|
| Original recipe DC | **19** |
| Active reconstruction work | **8 hours** |
| Undamaged mundane body reference | **2 gp** |
| Undamaged finished unit reference | **4,509 gp** |
| Reconstruction materials | **1,127.25 gp / 112,725 cp** |

Then rerun the two missing-primary-constituent negatives with those same correct terms. Keep all other actual tool/training/assembly premises satisfied so that each negative isolates the intended missing constituent.

Retain the distinction between a replaceable subordinate pin and an irreplaceable original primary mounting under this repair route. Neither the quotation nor successful structural repair refills charges, resets dawn history or removes a persistent flaw.

**Do not change recipe-268’s card DC, source record, body value or finished reference. Those are already correct.**

## Regression requirements and promotion authorization

After JC-ER01–JC-ER03, rerun the existing suite and the added targeted cases. Preserve the previously submitted revision and reports as historical evidence; issue corrected results and hashes rather than replacing the historical evidence with a claim that it never contained these defects.

The corrected evidence must retain all 43 complete source records, 200 component occurrences, eleven catalyst occurrences and 26 public paragraph bindings; the 26/1/16 visibility split; ten/nine body models; fourteen/twelve tag entries; all 86 references; the structural-only quality results; actual-tool and original-assembly gates; and all 54 protected-input checks.

Reconstruct and compare the **complete public manuscripts, guide and JSON envelope** after the repairs. Apply any shared interface wording or operational-metadata changes consistently to both audience projections. Do not leak private bodies, private operative-tag entries, private recipes or nested guidance through a shared envelope or example.

A corrected receipt should identify each JC-ER repair, its regression results, corrected artifact hashes and the unchanged protected-input result. Any promotion metadata must cite this exact verdict and its completed conditions; preserve the original recipe objects and their historical `status`/`needsReview` fields unchanged.

**Once those finite conditions pass, this verdict authorizes promotion of all 43 Jewelcrafting cards to REVIEWED — authored operational PLAYTEST without another generic conference or unchanged-card resubmission.** If a condition remains unmet, retain pending status for this promotion. An unrelated mechanical change is outside this authorization and requires review of that change.

Completed promotion yields **348/687 reviewed, 339 remaining; public 223/433**. This verdict itself has performed no promotion, repository write, deletion or push.

Human balance, actual ingredient and market availability, companion-runtime implementation and parity, whole-game final flow, publication and GitHub delivery remain separate gates. **Cosmology remains deferred until the successful authorized GitHub push and verification of its remote commit.**
:::

The Markdown download preserves this verdict unchanged for transport.
