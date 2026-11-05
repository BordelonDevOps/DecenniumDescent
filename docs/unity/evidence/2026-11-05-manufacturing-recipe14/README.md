# Recipe 14 manufacturing profile — 2026-11-05

## Increment

Added one opt-in, source-bound Recipe 14 profile to the existing C# simulation. It uses the current command pipeline, shared clock and RNG, formula-work procedure, finite `WorkLedger` lots and reservations, manufacturing order record, saved continuation, command receipts, output-dose record, and tactical use path. It does not introduce a second simulation, inventory, clock, RNG, or save mechanism.

Responsibilities are limited to selecting the recipe-specific definition, exact source occurrences, formula DC, active work phases, supplementary packaging limits, failure recovery flags, and output batch. The authoritative state remains:

- `FormulaWorkRecord` for recipe-specific formula knowledge and copy/research progress;
- `ManufacturingOrderRecord` for recipe, set, reserved-vial quantity, work/check result, and settlement choice;
- `WorkLedger` resource lots, worker intervals, and exact reservations for ingredients, labor, and vials;
- `TradeProgressRecord` for the existing trade progression;
- `AlchemyDoseRecord` for each physical output and its use history;
- `Snapshot` content fingerprint, RNG state, and command receipts for compatibility, deterministic continuation, and replay.

The profile depends on the existing `Simulation` command/transaction loop, test-only content manifest, formula research, manufacturing resolver, shared clock/RNG, inventory ownership, crafting consequences, actor life path, and snapshot codec. Recipe 4 remains the default and its fingerprint key is unchanged. Schema 20 is unchanged. A test world selects one manufacturing recipe profile at a time.

## Runnable acceptance scenario

`manufacturing_recipe14_copy_pause_resume_save_completion_and_duplicate_replay` constructs the explicit recipe-14 content profile, copies only its supplied formula, starts a six-vial order, pauses after 450 seconds, saves and restores, resumes, completes the four-hour recipe using the shared deterministic check, saves and restores the pending choice, settles masterwork full yield once, and verifies six source-bound doses, exact catalyst retention, vial consumption, and duplicate-command idempotence. It then uses a dose through the existing tactical Action and healing path.

`manufacturing_recipe14_failed_batch_recovers_only_declared_bulk_lots` resolves an ordinary failure and checks exact 1.25 salts, 0.50 spirits, zero black-blood recovery, retained unused packaging, and no output. The definition acceptance verifies only salts and spirits are divisible and guards recipe 4's existing component flags. The formula test proves DC 11 and no recipe-4 knowledge grant. The content test verifies the separate profile digest and unchanged legacy profile.

## Rule boundary and remaining gaps

The divisibility and 0.01 unit rule is a new accepted prototype decision attached only to the two exact Recipe 14 bulk occurrences; ordinary failure amounts follow from that declaration and the existing one-quarter recovery procedure. Source-backed values and the separate Codex/GPT consensus are recorded in [the rule decision](../../MANUFACTURING_RECIPE14_RULE_DECISIONS.md) and [consensus receipt](GPT_CONSENSUS.md).

The profile is `TEST_ONLY`, is not release-approved, grants no player knowledge, and is not a general recipe loader. Recipe 4 and recipe 14 cannot coexist as selectable recipes in a single world yet. Acquisition, material procurement, specialty-level crafting, arbitrary recipes, category-wide divisibility, authored content promotion, and production content loading remain unimplemented.

## Validation

- C# 9 warnings-as-errors headless compilation: **PASS**.
- Complete deterministic suite: **1,124/1,132 passed**. Its eight failures have exactly the same names and exception texts as the saved preceding baseline (1,119/1,127); each fails during schema42 harvest-manifest validation before this manufacturing code runs. Exact results are in [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json).
- Static package validation: **18/18 checks passed**, 213 package assets and 213 unique metadata GUIDs. This validates static package structure, bindings, pinned source blobs, and manifest digest only. See [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json).
- Focused post-review divisibility/legacy-compatibility acceptance: **1/1 passed**. See [FOCUSED_DEFINITION_RESULTS.json](FOCUSED_DEFINITION_RESULTS.json).
- Unity import, compilation, play, and build checks were not performed.

The source snapshot and implementation hashes are listed in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). Generated `engine/artifacts` directories are temporary outputs; the linked result files here are the retained evidence.
