# MGT-04 recipe-347 implementation evidence

**Historical candidate:** This evidence is for the pre-correction source commit `fd561c5e8b08e915b3d79ca952a16db04da3e36e`. GPT reviewed it and held acceptance on six findings. The current correction candidate, its exact changed files, updated validations and pending review are in [the correction packet](../2026-11-10-mgt04-gpt-corrections/README.md). The full-suite result below applies only to this historical candidate. Neither this historical packet nor the correction packet marks MGT-04 or the engine complete.

**Implementation commit:** `fd561c5e8b08e915b3d79ca952a16db04da3e36e` on `Engine`. The exact parent and 45-file change list are in [IMPLEMENTATION_COMMIT.md](IMPLEMENTATION_COMMIT.md).

## Responsibilities and authoritative records

This increment connects the reviewed recipe-347 card to one real, reusable physical Mining Tool body.

- `Recipe347WorkOrderRecord` records the worker, selected Strength/Wisdom check, recipe/formula/specialty/workshop identities, separate body and component reservations, required implements, `ActiveWorkProgress`, check/RNG facts, quality choice, disposition and output reference.
- Existing `WorkLedger` records reservations and worker intervals. `RuleClock` and the existing continuation path credit work. Source-qualified Watch use is derived from interval and procedure records, without a second mutable counter.
- Once-only settlement retains the extraction-tools lot, settles consumed occurrences through existing inventory/work authorities, and transforms the exact reserved body's linked structure. `Recipe347OutputProvenanceRecord` and `Recipe347MiningToolProfileRecord` link the output to that same item and structure.
- `Recipe347MiningToolUseEvidenceRecord` binds each mining attempt to its deposit/version, selection and physical body at use. `Recipe347MiningToolWorkSegmentRecord` records eligible removal work. Existing mining attempts, finite deposit stock, shared RNG, receipts and save records remain authoritative.
- Recipe-347 records are gated at schema72. The composed counted-lot simulation selects schema73. The append-only codec path preserves prior layouts, including Alchemy schema18/20 and deposit-bound mining schema49.

## Agreed scope and source

The pinned source blobs and hashes are in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). The accepted source/API contract and GPT's actual design response are [MGT04_RECIPE347_RULE_DECISIONS.md](../../MGT04_RECIPE347_RULE_DECISIONS.md) and [GPT_CONSENSUS.md](GPT_CONSENSUS.md).

The implemented profile is `TEST_ONLY`: one recipe, an explicitly authored workshop and stock set, one worker profile, and existing mining content. It does not grant production content authority, recipe discovery, general recipe execution, general workshop/stock authoring, trade advancement, or general formula acquisition.

## Connected behavior demonstrated

The focused suite includes acquisition of a real counted component lot from the existing physical crate and transfer to the qualified worker; staging the separate body and required tools at the authored workshop; reservation and multi-day recipe work; all six result bands and once-only settlement; and use of the transformed body through shared mining records.

`recipe347_same_tool_works_at_two_deposits_and_only_when_physically_deployed` uses one physical output at two authored deposits. It verifies no candidate benefit while the body is elsewhere, preserves the completed first mining result after moving the item and restoring, creates a second deposit-specific use binding, preserves finite stock identities, and produces byte-identical restored continuations.

Other focused cases cover counted-lot split/transfer/storage and physical mass, query/commit parity for access gates and workshop claims, default and alternate Rest Watches, cross-order booking of recipe and mining work, mid-Watch rejection, interrupted phase alignment, pending-choice restoration, and distinct concurrent work by a second actor.

## Validation evidence

- Full C# 9 warnings-as-errors regression suite: **PASS 1,314/1,314**, zero failures, **276 source hashes**. [Full report](final-full-suite-after-rest-watch-fix/run-20261110T072657128Z-d0682274/results.json)
- Standalone C# 9 warnings-as-errors compilation: **PASS** for Core, Persistence and LabModel, **201 source hashes**. [Compilation report](final-assembly-compilation-after-rest-watch-fix/compile-20261110T074206511Z-bc20a1f8/results.json)
- Static package structure and GUID validation: **PASS 18/18**, **302 assets / 302 unique GUIDs**. [Package report](final-package-validation-after-rest-watch-fix/static-20261110T074206559Z-89732e3d/results.json)
- Corrected mining-output focused reruns: **PASS 1/1 each**. [First-deposit result](review-fixes/rest-watch-corrected/run-20261110T072031905Z-de77564c/results.json), [two-deposit result](review-fixes/rest-watch-corrected/run-20261110T072316709Z-a3660239/results.json)

The first full run after adding shared Watch enforcement passed **1,312/1,314**. The two mining-output cases started in the Companion's scheduled Rest Watch and were rejected with `Recipe347ScheduledRestWatch`. Both focused cases reproduced the failure independently. The correction advances each test scenario to its next legal work Watch; it does not weaken or change the Watch gate. The original [full-run failure report](final-full-suite-rerun/run-20261110T070232405Z-b1aeb32a/results.json) and [focused reproductions](review-fixes/reproduce-rest-watch/) are retained.

## Compatibility and limitations

The current full suite exercises the existing schema18 Alchemy, schema20 portable-equipment, and schema49 Mining paths. This packet does not add an authenticated pre-increment schema18 or schema49 golden save. The separate accepted MGT-01 evidence does retain an authentic pre-storage schema70 save. GPT should assess whether the existing versioned codec tests meet this increment's historical-save acceptance or whether a source-era schema18/49 fixture is a blocker.

This is a bounded TEST_ONLY recipe and mining-tool profile, not general recipe execution or production authority. No successor module may start until GPT has reviewed this exact implementation evidence, concrete blockers are resolved, and Codex/GPT agree the current acceptance and next mapped dependency.

No Unity import, game build, or observed player session is claimed. The C# simulation and its test harness remain the validated boundary; the engine is unfinished.
