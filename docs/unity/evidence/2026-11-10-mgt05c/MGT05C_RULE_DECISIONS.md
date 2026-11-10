# MGT-05C — agreed schema76 preservation exposure and controlled-opening contract

**Status:** GPT/Codex source/API alignment complete; implementation authorized under the owner’s standing engine-development authorization. GPT’s actual review and limits are recorded in [GPT_REVIEW.md](GPT_REVIEW.md). This contract extends the already accepted MGT-05A/schema74 and MGT-05B/schema75 slices without changing their behavior.

## Responsibilities and authoritative records

This bounded TEST_ONLY increment admits controlled access to the existing successfully treated harvested-fish lot and vessel, one in-place portion per qualifying opening, later physical retrieval, and actual protection-ending events.

| Fact | Authority |
| --- | --- |
| Natural protection interval and original material age | Existing successful treatment history, harvest origin/interval, and shared `RuleClock`; protection remains derived, half-open, and never stored as a current Boolean or mutable age. |
| Effective open, close, and retrieval completion | Existing `PortableHandlingRecord.StartedAt`/`EndedAt` and command transaction. Opening becomes effective at `Open.EndedAt`; closing and physical removal become effective at their corresponding `EndedAt`. |
| Inventory identity and quantity | Existing `InventoryLotRecord` ancestry, `OrdinaryInventory.Descendant`, and `WorkLedger`; no duplicate quantity or location is stored. |
| Command identity and causal order | Existing command receipts/revisions and shared simulation transaction. |
| Clean-tool qualification | A new trusted, explicit TEST_ONLY fixture fact bound per opening to the existing physical Cook’s-utensils item. Presence, name, owner, skill, or player-supplied `clean=true` is not authority. |
| Admitted in-vessel portion | New immutable evidence associating the qualifying opening with the actual child lot and its causal portion command/receipt. The child’s amount, current location/custodian, age, and parent identity remain authoritative in existing records. |
| Actual protection-ending event | New immutable, typed TEST_ONLY evidence with trusted occurrence identity, treatment/vessel scope, effective shared-clock time, and causal command ordering. Causes are breach, contamination, and incompatible heat. |

The opening, portion, and exposure facts may be variants of one new schema76 evidence record. They must be validated as chronological cross-references and committed atomically with their causal physical commands. Do not add a second location ledger, a current-age/condition field, a protection Boolean, or a countdown timer.

## Adopted timing and protection rules

For a successful treatment, let:

- `C` = the existing treatment `CompletedAt`;
- `E = C + 86,400 seconds` = natural protection expiry, exclusive;
- `O` = the qualifying portable `Open` handling record’s `EndedAt`;
- `D = O + 60 seconds` = clean-opening limit;
- `K` = corresponding `Close` handling record’s `EndedAt`;
- `R` = a portion’s successful physical `Retrieve` handling record’s `EndedAt`;
- `X` = an applicable actual exposure event’s effective `RuleClock` time.

The pinned rule says a clean-tool opening to portion for **less than one minute** does not end protection. GPT/Codex adopted these integration details:

1. The one-second open operation leaves the vessel closed during the operation; it becomes open at `O`, when handling completes. The one-second close operation leaves it open during the operation; the whole closing second counts. A close preserves the brief-opening exception only if `K < D`.
2. If no close completes strictly before `D`, protection ends prospectively at `D`, unless natural expiry or an actual event ends it earlier. Protection already experienced in `[O,D)` stays earned; do not retroactively revoke it when the opening reaches one minute. A later close cannot restore protection or create another 24-hour period.
3. Natural treatment coverage remains `[C,E)`. Opening, closing, portioning, and exposure cannot extend `E`. At exact `E`, treatment protection is absent.
4. An actual breach, contamination, or incompatible-heat event at `X` ends coverage for then-covered vessel contents at `X`, even during a brief clean opening. It has no one-minute grace period and is distinct from ordinary `Open` state. The smallest profile rejects a protected opening that lacks a trusted clean-tool binding before mutation; it never invents contamination from opening alone.
5. Use exact `RuleTime` comparisons, including fractional times. The shared clock recognizes `D` as a relevant deadline. A clock advance or handling operation crossing `D`/`E` settles the boundary before the handling completion. A legal close may still complete after protection has ended. An opening completing at or after `E` is ordinary handling and creates no active-protection exception.

## Portion lineage and removal

During a qualifying opening, admit **one** in-place portion from the directly treated lot, using available, unreserved mass and the existing split primitive. The child must be physically contained in the same treatment vessel when created. Portion creation itself adds no new handling duration; retain `PortionInventory`’s existing timing and quantity semantics.

The child and remaining parent continue to receive the original treatment’s coverage while they remain eligible for that vessel coverage. The child’s future coverage ends at the earliest applicable natural expiry, actual exposure, unresolved-opening timeout, or successful physical retrieval completion `R`. Its removal cutoff is permanent for this treatment: closing the vessel, transferring the removed child, or later returning it to the vessel cannot reactivate protection. Recursively portioning an already-created protected child and generalized repackaging remain unsupported and must reject.

Keep MGT-05B’s inherited ancestry cutoff: pre-existing material branches do not gain an ancestor treatment they did not experience. For schema76, add continued coverage after an admitted in-vessel split only when immutable evidence links the actual child to the qualifying opening and causal portion command. Combine inherited and continued intervals by **union**, not double-counted addition. Preserve the original biological origin, `FreshUntil`, ownership, and existing unprotected age.

## Trusted TEST_ONLY occurrence boundary

The fixture binds the existing physical Cook’s-utensils item and an explicit cleanliness fact for this scenario. Normal actor access and handling requirements still apply. No general cleaning procedure, proficiency grant, skill check, extra supply cost, or one-minute labor job is introduced.

Actual exposure enters only through a trusted TEST_ONLY occurrence adapter with an admitted concrete occurrence identity. It records the occurrence at current `RuleClock`; callers cannot backdate it, invent unknown occurrences, choose arbitrary vessel/treatment scope, or freely assert environmental causes. Reusing an occurrence identity under another command ID cannot append another event; conflicting payload reuse rejects. Exact retries use the existing receipt/idempotency path without a second event, mutation, clock advance, or RNG draw. Exposure itself does not consume the fish, rewrite treatment outcome, or imply poison, disease, damage, or edible status.

The first schema76 profile covers the treatment vessel and its covered contents. Generalized fragment-level contamination and environmental simulation are not included. Exposure does not rewrite a previously removed child’s history.

## Schema, tactical scope, and compatibility

Add an explicit schema76 TEST_ONLY profile and append its evidence section only for schema76. Add 76 to the explicit schema allow-lists. Preserve schema74 and schema75 codec bytes, fingerprints, profiles, validation, and runtime behavior; reject nonempty schema76 evidence below76. Do not retag, downgrade, silently migrate, or discard evidence. Keep the MGT-05A Fresh-work adapter unselected in the treatment/exposure profile, as in schema75.

The new controlled-opening, protected portion/retrieval, and fixture-exposure paths are exploration-only. Reject those new paths in tactical mode and prevent a mode transition from carrying an unresolved controlled opening into an unsupported tactical lifecycle. Preserve unrelated tactical handling and all supported schema74/75 behavior.

## Runnable acceptance scenario

Use only the existing TEST_ONLY fish, treatment, and vessel fixture. Demonstrate:

1. Successful shared treatment and a qualifying open/close with the bound physical tool; closing at 59 seconds preserves remaining-content coverage without extending `E`.
2. One actual conserved portion, created inside the vessel; the child and remainder retain original origin and experienced protection. Save/restore after the split and before retrieval.
3. Successful retrieval ends the child’s future protection exactly at `R`; the remainder stays covered. The child continues aging with no inherited vessel lifetime and cannot regain coverage after later descendants or return attempts.
4. Exact `D` cases, close completion at 59 versus 60 seconds, a clock advance and a handling operation crossing the timeout, and exact `E` ordering.
5. An actual exposure branch during a brief opening where protection ends immediately without grace; focused authority/scope and duplicate-occurrence checks for breach, contamination, and incompatible heat.
6. Save/restore while open, after split/before retrieval, and after removal/exposure; deterministic replay; whole versus partitioned advances; unchanged amounts, `WorkLedger` mass, ownership/custody, `FreshUntil`, treatment/check history, and `NutritionKind.None`.
7. Genuine schema74/schema75 roundtrip and continuation behavior with their original bytes/fingerprints/handlers unchanged; schema76 evidence is rejected below76.

No new RNG draw belongs to opening qualification, portioning, or exposure. Randomized stress coverage beyond these cases is optional. Re-treatment, recursive protected subdivision, repackaging, production food/recipes, other materials, general environmental simulation, and Unity remain deferred.
