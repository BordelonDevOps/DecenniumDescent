# MGT-05B — bounded harvest preservation treatment contract

## Approved module boundary

Implement one closed-container preservation-treatment slice as schema75, explicitly `TEST_ONLY`, over the existing harvested-material, inventory, work, character, clock, RNG, command, and snapshot authorities. This is the next mapped MGT-05 dependency after GPT accepted bounded schema74 MGT-05A at `1e0bbc1168808686cec20a1d52ffa33284550646`.

### Responsibilities

- Admit one treatment for one actual, whole available harvested inventory lot whose mass is at most 10 lb and whose derived preservation state is Fresh or Degraded.
- Bind the attempt to the exact inventory descendant, a capable scheduled Cooking/Wisdom worker, physical Cook’s utensils, a suitable sealable container with explicit TEST_ONLY fit/capacity facts, and one real 0.5 lb preservative-supply lot.
- Reserve the target and supply through `WorkLedger`, book the worker through the shared active-time ledger, and record exact active work using the existing work-progress authority.
- At exactly 1,800 active seconds, resolve one ordinary DC 10 check from the selected character/training and shared deterministic RNG. A successful result creates a 24-hour elapsed-time protection interval and the terminal seal at the same RuleClock instant. Failure spends the same work and the full supply, with no protection.
- Derive current state/value from original harvest origin, lot ancestry, successful treatment history, and shared `RuleClock`. Do not save a mutable current age, state, deadline, or value.
- Persist this contract only in schema75. Keep schema74 bytes, fingerprint, validation, and Fresh-work adapter behavior unchanged. Schema75 rejects nonempty MGT-05A `HarvestRequirementWorks`.

### Authoritative records and dependencies

- Existing `HarvestMaterialUnitRecord.OriginAt` and `PreservationIntervalSeconds` remain the biological origin and interval authority.
- Existing `InventoryLotRecord` ancestry/creation facts select the exact treated lot and govern later descendant inheritance.
- Existing `WorkLedger` owns target/supply reservations, supply settlement, and worker intervals; `ActiveWorkProgress` owns active labor.
- Existing character, training, `AbilityCheckRules`, `RuleResolution`, `DiceStream`, and `RuleClock` own eligibility, check derivation, deterministic roll, and elapsed time.
- A new immutable treatment-attempt history binds the treated inventory lot, worker, physical equipment, material reservation, work lifecycle, terminal outcome/check, and successful completion instant. It must not duplicate quantity stock or store derived age/expiry.
- `PortableEquipmentRecord` and the existing handling/storage resolver own actual item placement, access, closure, fit, and physical mass. Treatment history must prevent unsupported changes while protected.
- Snapshot copy, validation, codec, policy fingerprint, and deterministic command receipts remain the existing persistence/replay boundary.

### Pinned facts and fixture bindings

The source authority is `DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md` at source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, SHA-256 `b8adb3ac6eb51f333fdb8f2d68ecc7e9c6511e7ee3aded1bfe54cd4728c93479`. It defines preservation intervals/categories and origin, one interval to Degraded and two to Spoiled, the 10 lb limit, 30 active minutes, a suitable trade kit and sealable fitting container, 1 gp worth of supplies per 0.5 lb, one DC10 check, and 24 elapsed hours of successful protection. Reservations do not suspend aging; failure grants no extension; already-Spoiled material cannot be rescued. See pinned source lines 152–166.

`DescentReviewChanges/ReviewBible/data/playtest/crafting_engine_candidate.json`, SHA-256 `6aa9b36a53bfac8c927ef2e3689c0475aaeadf8e26ce4c9acbcb1eba08076ff4`, is candidate fixture data only: it supplies the numeric `10 lb`, `30 minutes`, `0.5 lb`, and `24 hours` values, plus the Cooking/Cook’s-utensils binding. Its embedded source hash does not verify the Markdown rule document and must not be represented as doing so. For this first slice, use only the existing harvested `generic.ordinary-fish-meat` lot (0.25 lb, 8-hour interval, `NutritionKind.None`) and one completed attempt per simulation fixture run. Cook’s utensils, the supply stock, worker/training selection, and a separate preservation-container profile are exact TEST_ONLY fixture bindings, not production catalogue or rule content. The candidate’s `preservationSuppliesCp` is not an added currency debit for already-owned supplies.

## Acceptance scenario

The runnable schema75 LabModel scenario must use a real harvested fish-meat inventory lot and actual physical equipment/stock; validate admission atomically; demonstrate the 1,800-second work boundary and one shared DC10 check; distinguish Fresh-success, Degraded-success, and failure; prove no protection before completion, no rescue at Spoiled, and expiry at completion+86,400 seconds; preserve original origin and sibling isolation; block opening/splitting/repacking or other unsupported exposure-causing changes while protected; permit intact closed-container movement; demonstrate post-expiry descendant history inheritance and conserved mass; and compare mid-work, protected, and post-expiry save/restore plus one-piece versus partitioned clock advancement and deterministic replay. Schema74 serialization/behavior and prior-schema validation must remain unchanged.

## Explicitly unsupported in this slice

No treatment exposure-event system, clean-tool opening exception, active-protection content splitting/repacking/removal, re-treatment, interruption/cancellation settlement, additional materials, cooked/edible output, production recipes, generic preservation catalogue, price debit, assistant, quality table, or new character-creation/advancement rule. Unsupported operations must reject before mutation. If a source/API conflict prevents an acceptance behavior, stop at that specific conflict and bring it through the existing GPT delegation rather than inventing a rule.
