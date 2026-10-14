# Fishing exact operational verdict

**Disposition: finite corrections required. The submitted candidate is not approved unchanged. Completing FI-E01–FI-E11 below, with their specified checks, authorizes operational PLAYTEST promotion of all 44 Fishing cards without another generic conference or another full exact-card review.**

Until that completion is recorded, Fishing remains **0/44 promoted**. Reviewed totals remain **348/687, with 339 remaining; public 223/433**. This is not publication, human-balance, runtime, whole-game, vehicle, bestiary, economy, Supply, or cosmology approval.

## Review basis and independent execution

I reviewed the supplied FI-D01–FI-D24 decisions, both shared guides, the 44 card sections and operational records, the audience-factoring instructions, all 24 written scenarios, and the helper and validation code together. The older preliminary reports are historical evidence, not contradictory claims of current approval.

I verified that the mounted source-verdict file has **75,298 characters** and matches the submitted SHA-256. I independently recalculated the **44 finished references, 528 quality calculations, 156 structural calculations, and 76 repair quotations**, using a compact transcription of the supplied source numbers. Those calculations passed. I also ran **37 targeted probes**, including ordinary-operation and rejection controls, against a local transcription of the submitted helper and Fixture class using source-derived mechanical inputs.

These were not reruns of the original repository's 220-check suite. I did not independently verify the six candidate artifact hashes or the 63 protected repository-file hashes. Those remain submitted evidence. The probe inputs are deliberately incomplete mechanical test records, not purported reconstructions of the full source cards.

**No recipe-specific numerical rebalance is required by this verdict.** The source quantities, bonuses, extraYield values, primary affinities, fixed body profiles, non-artisan boundary, quality arithmetic, repair-price formulas, and food/Supply exclusions can remain. The blocking defects concern event admission, record binding, lifecycle transitions, and evidence sufficiency. A cited record need not be authenticated by this helper, but it must still be the record for the same item, creature, event, and historical state being used.

## FI-E01 — Reject invalid catch events, not merely their equipment modifiers

**Basis:** Part A, FI-D01, FI-D07–08 and FI-D20; Part C, `effect_candidates`, `FishingLedger.apply`, and `_effects`.

The selector correctly returns zero equipment modifiers for an attack, DEX check, Survival check, automatic result, non-roll, or harvesting task. The journal nevertheless accepts those descriptors when the corresponding resolution is supplied as Success with equipmentBonus 0. My probes reached `captured` and created a first-recovery evaluation in all six cases.

The journal also accepts two different catches using the same canonical roll ID. The existing `seen` list protects transition IDs, not global reuse of a resolved roll.

**Required repair:** At catch-event admission, require an actual WIS/Fishing-tackle ability check in the ordinary-provision-catch category, with `actualRoll=true` and `automaticResult=false`. Bind its canonical roll ID to one attempt and prevent reuse across attempts. Keep a zero-returning selector for unrelated checks where useful, but its zero result must not authorize this catch procedure.

Bind the resolved Core check to the catch profile and DC declared before commitment, rather than just accepting a degree label. Ordinary DC 12/15/18 or an independently reviewed override remains the rule. Bind training and the single PB/expertise contribution to governing credential evidence, including untrained disadvantage. Trap configuration must not accept arbitrary additional personal-bonus fields merely because the same dictionary appears twice. This requires record validation, not reimplementation of Core dice resolution.

**Required checks:** Reject all six non-catch descriptors through the journal, reject reused canonical roll IDs, reject a resolution using a different declared DC, and retain valid trained, untrained, and expertise cases with no duplicated PB.

## FI-E02 — Separate attempt start, commitment, exposure, and work phases

**Basis:** Part A, FI-D01–02, FI-D05, FI-D08, FI-D12 and FI-D21; Part C, `commit`, `_schedule`, and the Trap work check.

`commit` currently becomes `startedAt`, schedules the catch check 3,300 seconds later, and schedules Bait expiry 3,600 seconds later. That conflates the beginning of setup with the actual exposure checkpoint.

A source-permitted timeline is dry setup beginning at minute 0, first deployment/exposure at minute 5, catch check at minute 55, ordinary secure retrieval at minute 60, and Bait expiry at minute 65. The current journal rejects that timeline rather than representing its separate clocks.

Separately, a Trap work record containing its only five setup minutes at minutes 50–55 is accepted for capture at minute 55. A configuration timestamp at minute 5 does not establish that setup actually occurred then.

**Required repair:** Record the attempt/setup start independently of commitment and first exposure. Preserve the check at attempt minute 55, the fifty-minute Trap soak after completed five-minute setup, the five actual retrieval minutes, the attended closure checkpoint ten elapsed minutes after the check, and the sixty-minute receipt measured from actual exposure. Do not restart one clock to accommodate another.

Represent pre-setup reservation and pre-exposure cancellation in the bounded journal, or require a bound reservation receipt from the governing inventory/work ledger. Cancellation must preserve worked time while releasing only still-unspent reservations. Validate setup and soak as distinct phases; five arbitrary minutes somewhere before the check are insufficient.

**Required checks:** Accept the minute-5 exposure timeline; reject minutes-50–55 Trap setup for a minute-55 catch; cover precommit cancellation, postcommit no-refund interruption, and both expressly ordered same-timestamp expiry/capture cases. Keep Rig mounting outside the main five-minute deployment.

## FI-E03 — Bind physical admission and every item view at every relevant checkpoint

**Basis:** Part A, FI-D03–04, FI-D07, FI-D12 and FI-D16; Part C, `_assembly`, `physical_admission`, `_effects`, and `_capture`.

The complete required apparatus is checked at commitment, but the later check and capture paths call `physical_admission` without repeating the complete assembly binding. I set Line641 to HP0 and omitted it from the later admission's apparatus list. The journal still captured the fish using a weaker magical contribution.

A twelve-pound body manifest also passed against an unrelated six-pound admission. Admissions have no required selected-creature identity binding. Omitting an otherwise qualifying Line641 from the check's item views silently reduced the accepted maximum from +2 to +1. Finally, attended retrieval accepted another worker's five minutes without checking that they belonged to the lead.

**Required repair:** Bind admission to the actual attempt, method, registered indispensable apparatus, and selected physical creature. At the catch and secure-capture checkpoints, verify that every indispensable member has its own corresponding current state. Cross-check body mass and geometry against that same creature's governing profile, rather than accepting unrelated numerical admissions.

Require complete coverage of registered magical candidates: each must have current evidence or a supported ineligibility result. An omitted view is not proof that a stronger registered item stopped qualifying. Define the handling of ordinary, unenchanted members explicitly; they remain physical requirements without generating magic.

Bind attended retrieval work to the lead and the lead's required hands. Assistance cannot substitute for missing lead hands. Suppressed but otherwise functional ordinary apparatus must remain physically usable; suppression alone is not breakage.

**Required checks:** Reject omitted Broken members at both checkpoints, mismatched creature/admission mass, missing candidate views, and another worker substituting for the lead. Retain valid suppressed-gear fishing, weaker surviving recovery sources, and interrupted-but-timely retrieval.

## FI-E04 — A Bait receipt must correspond to this journal's actual expenditure

**Basis:** Part A, FI-D02, FI-D05 and FI-D07; Part C, the Bait branch of `effect_candidates`, `_effects`, and `commit`.

A registered Bait item can contribute even when the commitment's `baitId` is null. With its recipe binding changed consistently to the supplied +3 Bait198, the journal accepted the +3 contribution while recording **no Bait expenditure and no expiry event**. A supplied item-state receipt bypassed the intended debit.

Presentation validation also accepts `forms=['Lure']` when the referenced physical source is actually Rod179. It checks membership of the ID, but not whether that ID supplies the declared form.

**Required repair:** Every contributing finished Bait must resolve to the one dose actually consumed for that attempt. Require agreement among its physical identity, source recipe, exposure receipt, assembly, journal debit, expiry, and current suppression state. A null `baitId` means no finished-Bait contribution. Reject an unregistered, copied, expired, or differently bound receipt.

Bind presentation forms to their actual source items or ordinary bait lots. A Rod cannot become a Lure through a separate forms list. An ordinary portion must be a real, eligible portion in the required physical location, with its governing inventory/use record; the source recipe's consumed bait-role component is not that portion.

**Required checks:** Reject undeclared-dose contribution, duplicate use, receipt/assembly mismatches, and false presentation forms. Preserve unwrapping without exposure, valid receipt survival after swallowing, no refund after exposure, and continued age on rewrapping or transfer.

## FI-E05 — Require the Rig's own operational evidence before admitting its benefits

**Basis:** Part A, FI-D03, FI-D05, FI-D07 and FI-D21; Part B, recipe642; Part C, `_assembly` and the fixture coverage.

Adding Rig642 to a Rod fixture whose other pieces offer only +1 produces the Rig's +2 benefit without any Rig load, support, proximity, tether, mounting-work, or retrieval-work record. None of the six saved fixture families demonstrates a fully bound Rig operation.

**Required repair:** Require a Rig deployment record bound to this attempt and dispenser. It must establish the existing one-pound compatible chum allotment within the one-pint limit, actual support, tether path, proximity to the registered assembly, and five additional mounting minutes before main deployment. Bind its opening/dispersal to a single committed chum-use record.

A finished Bait substitution remains exactly 0.10 pound plus 0.90 pound of ordinary chum, with the wrapper excluded from chum mass. The same material cannot simultaneously fill a separate Trap holder or hook. Subsequent Rig retrieval requires its own five actual minutes and disposition; closing the catch does not make that handling free.

These can be resolved governing records. No fluid simulation, merchant inventory generator, or companion runtime is required.

**Required checks:** Add a valid Rig-only strongest-contributor case, then missing load, insufficient chum, excess volume, excessive tether/proximity, missing mount work, double-used bait locations, missing retrieval work, and Broken/suppressed Rig cases. Suppression removes benefits without inventing a refill or deleting the body.

## FI-E06 — Separate closing a claim from retrieving or handing over a Trap

**Basis:** Part A, FI-D05, FI-D08, FI-D10, FI-D12 and FI-D16; Part C, the `close` branch.

The current branch clears reservations and all scheduled events for any allowed closure reason. I reproduced a captured Trap closing as retrieved without five retrieval work minutes, a failed but still-deployed Trap freeing its lead for another deployment, and a pending lawful handover deleting its scheduled catch check.

Those are different physical and procedural outcomes under FI-D05.

**Required repair:** A failed or finished but unreconciled Trap continues to occupy its deployment allowance until actual retrieval, lawful handover with the existing record, or express abandonment. A retrieved disposition needs the capable retriever's five work minutes, hands, path, handling capacity, and actual apparatus/catch locations. A bare reason string is insufficient.

Handover must retain the same attempt, spent opportunity, selected creature, original setter configuration, and any pending one-shot check. Transfer responsibility for the unresolved deployment without changing the configured setter or creating a new roll; the receiving person's allowance must remain legal. Abandonment, unlike handover, cancels a not-yet-resolved check and closes future Fishing claims while preserving real apparatus and creature locations.

Do not interpret releasing an attempt reservation as proof that its equipment has returned to carried inventory.

**Required checks:** Failed/unretrieved Trap still blocks another deployment; actual retrieval frees it; pending handover preserves and resolves the original check once; handover to an already-occupied holder fails atomically; abandonment cancels the pending check without refunds or deletion of an already captured animal.

## FI-E07 — Enforce the stated response region, not only a weighting radius

**Basis:** Part A, FI-D13–15; Part C, `weighted_response` and the test named “outside 30-foot preference gives no doubled weight.”

FI-D14 states a maximum response region of thirty feet along the qualifying connected-water path. The helper instead retains a candidate at thirty-one feet with weight 1, and the journal can select and capture it through the selected-attraction allocation. The named positive test therefore encodes a different boundary from the supplied source verdict.

**Required repair:** For this candidate's selected-attraction allocation, exclude candidates beyond the thirty-foot response region. Do not reinterpret the limit as merely the range of doubled weighting. Bind the response path to the actual bait/Lure point or Rig dispenser and this opportunity's recorded candidate set.

This does not shorten the Rod's separate fifty-foot angler-to-hook deployment path. An independently governed ordinary response outside this attraction procedure is not a borrowed permission to enlarge this allocation.

**Required checks:** Thirty feet qualifies when all other predicates hold; thirty-one feet does not enter the attraction allocation. Preserve receptive nonmatching candidates within the region at weight 1, the 2/1/2 distribution, one draw, no replacement draw, and no compelled response.

## FI-E08 — Carry origin restrictions, irreversible loss, and chronology through recovery

**Basis:** Part A, FI-D08–11 and FI-D23; Part C, `_capture`, `validate_material_manifest`, and `resolve_ordinary_harvest_units`.

I changed the pre-attempt manifest to `summoned-no-resources` while leaving the later manifests permitted. The journal authorized Fishing reserve units, and the harvest helper subsequently authorized baseline plus reserve extraction. The pre-attempt prohibition was lost.

Other probes restored an initially lost reserve unit or a lost captured baseline unit by changing a later snapshot to available. The harvest helper also accepted harvesting before the capture record that authorized it, and a death/removal time in the future relative to extraction.

Conversely, a valid post-capture loss reducing an already authorized one-pound meat portion to 0.75 pound was rejected because the initial whole-extra-unit rule is reapplied to the later remaining mass.

**Required repair:** Preserve immutable source-origin prohibitions separately from current access permission. Later snapshots cannot remove a no-resource origin. Preserve unit identity, nonincreasing recoverable mass, and irreversible lost, destroyed, removed, spent, or forfeited states. A new manifest alone cannot restore material. Any separately allowed condition change must carry its actual governing transition, without reopening the Fishing evaluation.

Require historical ordering: the recovery/capture evidence must exist no later than the extraction that consumes it, and actual removal/death timestamps cannot lie after the corresponding extraction. Preserve the established timestamps rather than accepting replacements without a governing lifecycle record.

Make mass checks phase-aware. A new Fishing meat-reserve entitlement needs its original whole pound. Subsequent real loss may reduce that authorized portion's remaining extractable mass; it does not restore the pound, create a new unit, or invalidate the entire body's unrelated recovery.

**Required checks:** Initial-origin laundering fails; lost/spent units cannot reappear; early harvest and future removal timestamps fail; a post-capture 0.75-pound remainder stays at most 0.75 pound. Retain first evaluation including zero, partial forfeiture, distinct damaged-baseline critical recovery, and no meat inventory at living capture.

## FI-E09 — Require actual stock-allocation and renewal relationships

**Basis:** Part A, FI-D08, FI-D10 and FI-D23; Part C, `forage-route`, stock-allocation handling, and the recapture/partition fixtures.

The supposed disjoint-stock positive test changes only the opportunity's partition name and the matching allocation record's partition name. Neither record identifies the excluded physical resources or a relationship proving separation from the earlier whole-pool Forage allocation. The helper accepts both routes. That demonstrates a name-based bypass, not the authorized exception.

The recapture fixture likewise does not supply the intervening release/reavailability history claimed in the written scenario. A future-dated prey profile can also be used for an earlier response allocation because its historical applicability is not checked.

**Required repair:** Bind opportunities to the governing finite site/stock manifest and applicable version. A disjointness exception needs actual physical membership or an explicit governing disjoint-allocation record relating both allocations and their resource footprints. A renamed partition is insufficient; a whole-pool allocation must not silently coexist with an overlapping subpartition.

Renewed or recapture opportunities must reference the real release, escape, arrival, newly accessible stock, or materially new approach that authorizes them, with its cause and time. Keep the same creature identity and prior recovery history. Profiles and allocations must be applicable as of the event, or carry a properly defined effective interval; future records are not earlier evidence by default.

This is not a demand for the helper to authenticate a Director or simulate ecology. It is a requirement to consume the specific governing relationship instead of treating unrelated names as that relationship.

**Required checks:** Reject partition-only renaming and future-effective evidence. Accept a genuinely disjoint documented allocation and a same-creature recapture supported by actual intervening custody/reavailability records. Preserve no automatic hourly, Watch, rest, or site-name renewal.

## FI-E10 — Bind crafting reserves and repair quotations to the actual body records

**Basis:** Part A, FI-D17 and FI-D19–22; Part C, `ordered_output`, `structural_hp`, and `repair_quote`.

The numerical formulas pass, but the qualification checks are not sufficiently source-bound. A Trap order accepted seven reserve IDs describing incomplete Hook bodies sharing one original constituent. A Rod repair accepted Hook pricing and an arbitrary required-parts list containing only a clip. An inconsistent unmodified B5 record at 1/1 was normalized to 5/5, and a Bait carrier marked destroyed passed because it was not spelled Spoiled.

**Required repair:** Bind the order, body model, physical identity, current inventory/reservation state, and original-constituent manifest. Require the admitted family and fixed body profile, completeness, valid condition, and nonduplicated physical constituents. Bait stock needs real eligible carriers and wrappers, with their separate identities or a governed exclusive packaged-stock identity.

Validate recorded ordinary maximum, strongest improvement, flaw, and current HP consistently before applying the existing damage-deficit formula. Do not normalize contradictory records into a healed body.

For repairs, obtain the required original assembly from that item's creation/body record, not a freshly supplied arbitrary list. Bind the mundane reference to its admitted body model and the finished reference to its actual recipe. A pure quotation calculator may remain a calculator, but its output cannot substitute for the missing qualification checks or be reported as a validated repair route.

**Required checks:** Actual modeled missing-primary negatives, wrong-family reserves, shared constituents, destroyed carriers/wrappers, inconsistent HP, and wrong-body repair pricing. Retain the existing 528/156/76 arithmetic coverage, positive damaged reserves, recovered-original Line splices, persistent flaws, and no Bait repair.

## FI-E11 — Close the evidence and projection gate on the repaired artifacts

**Basis:** Part A, FI-D06, FI-D18 and FI-D24; Parts B–C, the projection reports, historical backlog, manuscripts, and validation programs.

The public set remains recipes160–184 and640–642, with nine models and thirteen operative affinities. Internal remains all44 cards, nine models, and fourteen affinities. The three historical boat concepts remain history rather than vehicles.

The submitted Sporefolk backlog entry contains `literalReferencePreserved:true`, but not the actual printed Sporefolk Adult crafting-reference line. That is not evidence of deletion; it is a missing literal-preservation check in this packet.

**Required repair and verification:** Preserve the historical reports and original submission hashes. Create a new, version-bound completion report for the repaired candidate. Rerun the original valid source/projection/arithmetic and sequence coverage, replace the incorrect positive expectations identified above, and add the finite regressions specified in FI-E01–10. Counts may change; the assertions, records, and outcomes are the evidence.

Regenerate or update both audience envelopes and manuscripts consistently. Verify that each operational JSON effect text equals its own exact manuscript paragraph; compare the whole public envelope and independently reconstructed public manuscript; retain all28 full six-paragraph V5 bindings; and reject private cards, private nested guidance, private links, and the unused Cold registry row in public outputs.

Include the exact existing Sporefolk line, its source locator, and an equality check in the internal audit. Do not invent or reconcile its other names. Reconfirm the 44 originals, 212 consumed component occurrences, zero catalysts, exact work/access fields, three historical boat links, and the protected-input hashes against the real repository records.

The completion receipt must identify the repaired artifacts by fresh hashes and record this verdict as separate operational authority. Do not overwrite historical source flags or pretend a changed artifact still has its original submission hash.

## Promotion authorization and retained gates

**Yes: completion of these eleven repairs and their specified checks authorizes promotion without another generic conference or another full exact-card review.** The authorization applies to the supplied 44 cards plus these bounded corrections, not to whatever broader redesign might accompany them.

The completion receipt must show that the repaired prose, JSON, helper contract, and worked cases agree, and that the specified positive and negative cases were actually revalidated against the repaired full candidate. Passing tests alone do not create authority; this verdict supplies the bounded authorization and defines its conditions.

Before that receipt, totals do not change. After the gate is actually satisfied and all44 cards are promoted, totals become **392/687 reviewed, 295 remaining; public 251/433 reviewed, 182 remaining**. Source `developed` and `needsReview` fields remain historical and unchanged.

No unchanged earlier trade card is reopened by this verdict. No new creature, spell, affinity, catalyst, vehicle, Supply conversion, merchant availability, or donor trait is authorized. Core, actual custody/placement, preservation, lawful extraction, ecology, market availability, companion runtime, human balance, publication, and final whole-game integration retain their separate gates.

**No source deletion or GitHub push is authorized here. Cosmology remains strictly after a successful separately authorized push and verification of the remote commit.**
