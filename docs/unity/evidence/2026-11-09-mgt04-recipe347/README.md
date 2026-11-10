# MGT-04 recipe-347 implementation increment

**Status:** Implementation evidence is ready for GPT review. The bounded schema72 path is executable and its validation passes, but the accepted MGT-04 contract has outstanding acceptance cases listed below. Do not treat this increment as full MGT-04 acceptance or engine completion.

## Responsibilities and authoritative records

This increment connects one reviewed recipe-347 card to one real reusable physical Mining Tool body.

- `Recipe347WorkOrderRecord` records the worker, selected Strength/Wisdom check, recipe/formula/specialty/workshop identities, separately reserved body and component lots, required implements, `ActiveWorkProgress`, check/RNG facts, quality choice, disposition and output reference.
- `WorkLedger` remains the authority for resource reservations and worker intervals. `RuleClock` and the existing continuation path credit work; source-qualified Watch counting is derived from persisted interval/procedure records rather than a second mutable counter.
- Once-only settlement preserves the retained extraction-tools lot, settles consumed occurrences through the existing inventory/work authorities, and transforms the exact reserved body's linked structure. `Recipe347OutputProvenanceRecord` and `Recipe347MiningToolProfileRecord` bind the output to that same item and structure.
- `Recipe347MiningToolUseEvidenceRecord` binds each mining attempt to its deposit/version, selection and physical body at use. `Recipe347MiningToolWorkSegmentRecord` records eligible removal work. Existing mining attempts, finite deposit stock, shared RNG, receipts and save records remain authoritative.
- Schema72 appends these records through `Snapshot`, `SnapshotCodec`, validation and command handling. Earlier Alchemy/schema18/20 and legacy deposit-bound schema49 paths are retained.

## Source and scope

The exact source bindings and pinned blob hashes are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The source/API contract and GPT's actual design response are in [MGT04_RECIPE347_RULE_DECISIONS.md](../../MGT04_RECIPE347_RULE_DECISIONS.md) and [GPT_CONSENSUS.md](GPT_CONSENSUS.md).

The implemented bounded profile is `TEST_ONLY`, fixed to one recipe, one explicitly authored workshop/stock set, one worker profile and existing mining content. It does not grant production content authority, recipe discovery, general recipe execution, general workshop/stock authoring or Unity gameplay integration.

## Current acceptance evidence

The final [full-suite report](final-full-suite/run-20261110T015923929Z-15aece1b/results.json) includes a passing `recipe347_same_tool_works_at_two_deposits_and_only_when_physically_deployed` scenario against the final source hashes. It completes source work over legal watches, transforms the reserved body into the same item with a mining profile, saves/restores the completed work, and uses that item at two distinct authored deposits. It also moves the item away from the first deposit and verifies no candidate evidence or +2 bonus, then saves the second attempt and verifies two independently bound uses and byte-identical restored continuations.

The full C# 9 suite passes **1,302/1,302** in [final full-suite results](final-full-suite/run-20261110T015923929Z-15aece1b/results.json), with **276 source hashes**. Dedicated warnings-as-errors C# 9 compilation passes for **Core, Persistence and LabModel** in [final assembly compilation results](final-assembly-compilation/compile-20261110T020716546Z-55c5d943/results.json), with **201 source hashes**. Static Unity package structure validation passes **18/18**, covering **302 assets and 302 unique GUIDs**, in [final package validation results](final-package-validation/static-20261110T020716539Z-d0fa9a1c/results.json).

The focused case initially failed with `OffCalendarActionAlreadySpent` because two one-second handling actions were issued inside the same six-second off-calendar activity window. The failing report is retained at [two-deposit-1 results](two-deposit-1/run-20261110T013308332Z-e6fd54b3/results.json). The scenario now waits for the next legal interval between actions; the source-defined one-second handling cost is unchanged. Earlier compile and composition failures, each retained with reports, are also preserved in this directory.

## Remaining contract acceptance work

The following required cases from the accepted MGT-04 contract are not yet demonstrated by this increment's focused tests:

- Full result/settlement coverage for all six quality bands, including Flawed body maxima, Exceptional/Masterwork quality choices, Masterwork without a catalyst, Failed recovery and Mishap consequences.
- Explicit recipe-order tests for workshop/formula/training/specialty/implement gates, claim conflicts, query/commit parity, duplicate/once-only settlement, and pending-choice continuation.
- Recipe-profile Watch-policy coverage for the default and alternate Rest slots, third-Work-Watch rejection across participating jobs, midpoint admission rejection, endpoint-only overlap, no passive credit, and post-interruption phase alignment.
- A connected acquisition scenario that retrieves actual recipe inputs/body/implements through existing exploration/cache/storage commands, includes another compatible actor/job, and verifies the transferred inventory/custody facts used by crafting.
- A post-completion movement and restore assertion proving the first mining result remains valid after the same item is relocated, plus explicit stock non-renewal and historical Alchemy/schema49 save coverage attributable to this integration.

These are remaining acceptance tasks, not newly invented mechanics. No successor module has begun.

## Validation boundary

Unity import/compilation, Editor tests, Play Mode, standalone game builds and observed player gameplay were **not run**. The approved scope is the C# simulation and static package structure. The implementation remains TEST_ONLY; the full engine remains unfinished.
