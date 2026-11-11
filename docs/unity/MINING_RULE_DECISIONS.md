# MGT-07 mining rule implementation boundary

**Status:** TEST_ONLY MGT-07 implementation across schemas43–49: finite exposed-node extraction (43), prospecting (44), nondestructive assay (45), destructive sample assay (46), companion assignment dispatch into extraction (47), mundane whole-unit mineral dressing (48), and one recipe-347 mining-tool integration (49). The governing source is reviewed operational playtest material. This record tracks implementation boundaries; it does not promote candidate text to release canon.

## Governing source

Pinned source revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

| Source | Relevant material | SHA-256 of checked-in bytes |
| --- | --- | --- |
| [Mining candidate field guide](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/MINING_CANDIDATE_GUIDE.md) | Choose the procedure; Record and resolve the deposit; Mineral preparation | `726cb84a1104901f5b05b412039b458af5bb5168e4482fb9e9844b1b42b697c3` |
| [Gathering tools candidate guide](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md) | Set up one real task; Operate the tools; Preserve the history | `9b1e4defcd18569ad8d8305552ad740e62be1faea3e1de448e364bd7536215bc` |
| [Gathering tool body catalogue](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/GATHERING_TOOL_CANDIDATE_BODY_CATALOGUE.md) | Exact mining-tool and prospecting-tool entries | `23fb5db0282881499abcddaa3cd259bab4262a34c884e5a80c1de8a894c5dd99` |

The first two guides are reviewed authored-operational playtest sources. Their status is not the same as approved release content. The internal body catalogue is not a public gameplay source and is not bound by this fixture. The operational completion above was discussed in [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206); it does not change the source classification.

Schema49 additionally pins [mining recipe cards](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/MINING_CANDIDATE_RECIPE_CARDS.md) (`c83b14b7df8475a1bdba05a69785e90dabcec5a12bb81cb722fa7737ab444a12`) and [public gathering-tool recipe data](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/data/crafting/gathering_tool_recipe_candidate_public.json) (`121a396e18e7e294e26a469a42e434f70c24816659bc05c77f094fcbd9e06510`).

## Responsibilities and authoritative records

Schema43 resolves explicitly authored exposed mineral deposits through command validation, active work, outcome resolution and finite receipt. The original fixture supplied one parcel; the 2026-11-06 content-reuse acceptance proves two materially different definitions through the same handler. The system does not discover or generate a deposit.

| Concern | Authoritative state / implementation |
| --- | --- |
| Deposit version, site, owner, tools, receiver and work surface | `MiningDepositRecord` |
| Exposed categories and finite physical stock | `MiningCategoryRecord`, `MiningMaterialUnitRecord` |
| Selected lead, categories, time, status and check audit | `MiningAttemptRecord`, `MiningSelectionRequest` |
| Labor interval and physical-unit claims | Shared `WorkLedger` worker intervals and reservations |
| Clock, RNG, actor abilities, life/conditions, inventory provenance and receipts | Existing shared `Snapshot` and command pipeline |
| Durable representation | `MiningCodec` through `SnapshotCodec` schema43; `CommandHistory` reconstructs the mining start request |
| Rule and fixture handlers | `SharedMining.cs` and `TestOnlySharedWorldPolicy.cs`, behind the existing LabModel gate |
| Standalone mineral dressing content and attempt | `MineralPreparationProfileRecord`, `MineralPreparationAttemptRecord`, `MineralPreparationCodec`, appended at schema48 |
| Dressing labor, unit reservation, physical output and provenance | Existing `WorkLedger`, `RuleClock`, inventory ancestry, `PortableEquipmentRecord` and command receipts |

Dependencies are the shared command authority and rollback path, exact `RuleTime`, deterministic dice stream, actor/skill records, condition/life handling, inventory lots, portable-equipment fit checks, work reservations, snapshot codec and receipt replay. No mining-specific clock, random source, inventory, job scheduler or global mutable state was added.

## Source-authored behavior represented

- Exposed-node extraction is a 60-minute default operation using Strength or Wisdom/Mining, chosen before work. The source gives the tier DC ladder I–VI as 12, 13, 15, 16, 18 and 19 unless an exact extraction DC governs.
- Partial selection takes `ceil(60 × selected accessible categories / all accessible categories)` minutes, minimum one. Hurry halves that duration, rounds up and imposes disadvantage only if the real work fits.
- The complete ordinary extraction profile is bounded to a predeclared exposed parcel of at most 50 lb and 1 ft³. It allocates finite authored units and uses actual access, tools, physical suitability and a receiving plan.
- The full 60-minute default identifies five minutes setup, fifty removal and five sorting/receipt. The source says a partial duration includes setup but does not specify how those three stages scale for a partial task. **New provisional completion:** after applying the source's rounded total duration, scale the default stages in a 1:10:1 ratio. Codex and Unity Rules Engine Development agreed on this narrow engineering policy under the owner's standing authorization to adopt their consensus. It adds no labor or independent stage rounding and remains provisional rather than release-approved.
- Selection commits on first positive removal work. Unselected accessible categories are forfeited; pausing preserves work and claims. Resolution is one-shot.
- Success recovers eligible selected undamaged baseline. Critical Success may also recover at most one actual selected damaged baseline unit. A separate critical-only reserve is valid only when the particular source card independently supplies an eligible reserve allowance.
- Failure recovers nothing and ruins the highest-value selected ordinary unit; a known tie is selected before work, while unknown values use a stable neutral identity order. Critical Failure ruins the selected allocation and applies the declared hazard, or 1d4 bludgeoning when there is no declared hazard.
- Untrained work has no Mining-tools proficiency contribution and uses disadvantage. The selected Strength or Wisdom ability is read from the documented STR/DEX/CON/INT/WIS/CHA order.
- Recipe-347's printed mining effects are represented together on one actual candidate instance: +2 to the Mining check after at least 60 seconds of qualifying lead work; one separately predeclared, ordinary, unselected reserve unit on Critical Success; and preparation of one selected eligible ordinary unit up to 1 lb during ten feasible active minutes within extraction. Ordinary mining tools and the pick remain required independently.

## Delegated interruption and resolution completion

The shared gathering source says pauses preserve the claim and recorded progress unless an actual event undoes work. It does not assign mining the unfinished-phase loss rule for enchanted-tool creation. Codex and Unity Rules Engine Development agree that mining retains earned feasible labor across voluntary pause, tactical interruption and save/restore. Only the affected worker pauses when their Action, hands, access or other work requirements cease; the shared world continues for other feasible work. Resume is explicit and revalidates current access, tools, worker, selection and receiver. Setup alone does not commit the selected stock: first positive removal work commits it.

They also agree that the shared timeline processes automatic boundary events through the endpoint, then rechecks the attempt's resolution eligibility. An eligible attempt rolls once and atomically settles; a temporarily blocked attempt keeps all labor in `AwaitingCheck` and resolves on a later eligible resume without more work or a reroll. These are provisional operational completions, not additional source wording. The current acceptance covers retained pause/save progress and once-only check/output. Terminal no-check settlement after the entire selection becomes unavailable remains unimplemented because this fixture has no admitted event that can remove those reserved units; do not invent an external-loss command to demonstrate it.

## Explicitly excluded source-dependent behavior

Schema49 represents only the exact recipe-347 candidate card and its independently predeclared reserve. Without that matching, physically eligible profile and actual candidate instance, no candidate benefit or reserve is available. General candidate catalogues, multiple candidates/families, and reserve effects for cards that do not print them remain unsupported.

At the schema43 extraction checkpoint, prospecting and assay were still future work. Schema44 now covers authored prospecting evidence, schema45 covers nondestructive assay against an existing authored manifest, and schema46 covers destructive assay of an explicitly authored existing sample; see [prospecting](PROSPECTING_RULE_DECISIONS.md) and [mineral assay](MINERAL_ASSAY_RULE_DECISIONS.md). Schema48 implements separate ten-minute dressing for one whole extracted ordinary unit up to 1 lb; schema49 integrates recipe-347 preparation, its check bonus and critical-only reserve into the same extraction. See [schema48 evidence](evidence/2026-11-06-mineral-dressing/README.md) and [schema49 evidence](evidence/2026-11-06-recipe347-mining-tool/README.md). Portions, assistant work, general candidate catalogues, cancellation before extraction commitment, terminal no-check loss, renewal from newly accessible disjoint parcels, refining, exceptional drops and excavation remain incomplete. Authored-content reuse is demonstrated across multiple definitions; no procedure invents a deposit or mineral unit.

## Schema49 recipe-347 mining-tool integration

The pinned recipe card prints three separate effects. Schema49 binds them to one immutable recipe-347 profile, one actual 3 lb item body, its linked 5 HP wooden structure, explicit required/optional body members, one authored mineral-preparation profile and one optional predeclared reserve unit. Missing primary members, suppression, melding, zero structural HP, wrong custody/location/access, broken support, excess selected tray load or absent candidate equipment make the candidate ineligible. Ordinary mining tools and the pick remain required independently.

Candidate participation is persisted against the existing mining attempt. At least 60 active seconds of feasible lead mining work qualify the +2 Mining check; equipment must also remain eligible at the result checkpoint. The one predeclared unselected ordinary reserve is separately reserved through `WorkLedger` and is recovered only on Critical Success with a qualifying candidate. It is excluded from baseline failure forfeiture, is never part of ordinary/damaged recovery, and is released on all non-awarding results.

For this card, one selected intact target up to 1 lb is dressed during the final 600 feasible active seconds of the removal stage. The original extraction duration and 1:10:1 setup/removal/sorting schedule remain unchanged. On the 600th feasible preparation second, independently of the later extraction check, the original physical lot is atomically reduced to zero and measured retained/gangue child lots are created; no partial split is inferred. The TEST_ONLY profile authors 0.1 lb gangue from a 0.5 lb ordinary unit, retaining 0.4 lb. The two children conserve the source mass and retain its inventory ancestry.

On Success or Critical Success with a qualifying candidate, the retained child—not the gross parent mass—is received and marked with the card's dressed profile. Ordinary failure awards nothing. If the prepared target is the selected failure victim, its mining unit becomes ruined while its retained and gangue matter remains physically present at the ground; otherwise the unawarded residue remains there under the closed attempt. Critical Failure also preserves the completed split. Pause, save/restore and resume preserve the same participation, reservations and completed split. No free tool, proficiency, crafting authorization, assay/prospecting bonus or general candidate-family behavior is added.

The 600-second placement, failure disposition and conservation edges are operational completions agreed by Codex and Unity Rules Engine Development under the owner's standing consensus authorization. They fill gaps in the authored card/guide rather than quote source wording; see [schema49 evidence](evidence/2026-11-06-recipe347-mining-tool/README.md) for exact source snapshots, hashes and tests.

## Schema48 mundane whole-unit dressing

The pinned mining guide supports a separate ten-active-minute, no-roll dressing operation using compatible Miner's tools, two hands, a capable worker and a stable accessible surface. It allows one ordinary unit or a real predeclared portion up to 1 lb and requires the actual gangue waste and retained mass to be recorded. Schema48 deliberately implements one already-extracted whole unit only. The source does not supply a mass-loss rate, so TEST_ONLY content authors the measured waste amount; retained mass is its exact remainder. No value, tier, grade, condition, freshness, hazard or ingredient-identity change is inferred.

The operation reuses the existing worker intervals, `RuleClock`, whole-unit WorkLedger reservation, inventory ancestry, physical item records, command transaction, snapshot persistence and replay. It retains the original mining unit as the ingredient identity, creates retained and waste child lots atomically, keeps the retained material in the authored receiver and places measured gangue at the worksite. The fixture assumes the open receiver, extracted unit and stable surface already share that worksite; it does not model general item-on-surface geometry or moving a unit onto a surface. Portions and exceptional/incompatible material remain unsupported. Recipe-integrated preparation is implemented separately for one exact card in schema49. Full boundaries and runnable evidence are in [the schema48 record](evidence/2026-11-06-mineral-dressing/README.md).

## Schema49 actual-candidate records and fixture boundary

Schema49 appends the immutable candidate profile, candidate instance state and one use/audit record per mining attempt after schema48. The candidate's actual `PortableEquipmentRecord` and `ObjectStructureRecord`, existing `MiningAttemptRecord`, `WorkLedger` claims/worker intervals, inventory descendants, shared clock, RNG and command receipt remain authoritative in their established stores. `MiningToolCandidateRules` is the shared pure eligibility predicate used by command assessment, check resolution and snapshot validation. No second clock, RNG, inventory, job store or mutable global state is added.

The TEST_ONLY fixture pre-authors one candidate instance and its current member/suppression/melding state. There is not yet a command lifecycle for losing or restoring members or toggling suppression/melding during play. Those states are validated at admission and at the result checkpoint; this slice does not claim a complete dynamic equipment lifecycle, general candidate catalogue or release content.

## Authored content generalization (schema43, 2026-11-06)

The schema43 records now initialize from `MiningDepositFixtureContent` collections. This changes TEST_ONLY authoring and validation only; it does not alter the persisted schema or extraction procedure. `MiningDepositRecord`, `MiningCategoryRecord` and `MiningMaterialUnitRecord` remain the authoritative simulation facts. The existing inventory/work lots, physical equipment, structures, reservations, clock, RNG, receipts and snapshot codec remain authoritative for their domains.

The mining resolver no longer recognizes a particular receiver fit-rule ID. It requires the receiver's authored fit marker and validates each selected unit against the existing explicit `FitMemberIds` contract. Fit-rule IDs themselves have no general semantic registry yet; the implementation relies on explicit membership and the portable-equipment validator, not on interpreting an ID string.

The registered acceptance `mining_shared_resolver_handles_distinct_authored_deposits_through_save_and_replay` runs two separately authored definitions through the same command assessment, check, settlement and persistence path. They differ in material category, tier/DC, unit identity and mass/volume/value, receiver profile and fit-rule ID, and adjacent worksite coordinates. Each completes to its own authored receiver, round-trips through the schema43 codec, and rejects duplicate replay without changing bytes. No deposit/category/material identity branch is added to the resolver. These are deliberately synthetic fixture facts; they do not establish production mineral content or simultaneous multi-worker mining.

This increment introduces no persisted fact and no schema bump. It generalizes content initialization/validation and exercises reuse against the existing snapshot arrays. `SharedMiningFixture` copies the authored content collection and returns copies, so subsequent caller array mutation cannot change the fixture fingerprint or initial snapshot.

## Fixture assumptions and technical limits

The legacy `SharedMiningFixture` profile authors two synthetic one-pound mineral units at a fixed site, with test values used only to exercise highest-value failure allocation. `MiningDepositFixtureContent` also admits multiple independently authored TEST_ONLY definitions with their own categories/tiers, physical item identities, receiver membership, surfaces and coordinates. Numeric values and equipment profiles remain fixture facts, not production defaults. Optional Intelligence/Wisdom overrides exist only to prove the ability-index mapping and are included in the fixture fingerprint.

The current handler delivers recovered output to the deposit's fixed authored receiver. It does not provide portable equipment movement or later retrieval. Record limits are fail-closed technical bounds, not gameplay capacity rules. Schema43 strict boolean decoding accepts only the canonical bytes 0 and 1.

## Runnable acceptance

Run `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` from the repository root. The registered `MiningCases` exercise:

- partial selection, first-removal commitment, pause/save/resume, finite receipt and duplicate replay;
- success, Critical Success with one authored damaged unit, failure, Critical Failure and associated shared life consequences;
- Wisdom distinct from Intelligence, deterministic check audit and state provenance;
- shared-clock credit during one-second inventory handling, with exact completion-boundary rejection and subsequent resolution;
- source-access and unsupported-hurry rejection without mutation;
- `mining_shared_resolver_handles_distinct_authored_deposits_through_save_and_replay`: two different authored contents exercise the same assessment/check/settlement/save/duplicate-replay path and each outputs to its own receiver;
- `recipe347_mining_tool_applies_check_reserve_and_integrated_dressing_through_shared_extraction`: verifies the unchanged 2,400-second schedule, mid-preparation save/restore, 600-second completion at removal end, conserved 0.4 lb/0.1 lb descendants, +2 check, distinct Critical Success reserve, separate damaged recovery, completed save and duplicate replay;
- `recipe347_failed_extraction_preserves_unawarded_prepared_mass_and_releases_reserve`: verifies ordinary failure after physical preparation awards no output, ruins the selected target, retains both physical descendants at the worksite and releases the unawarded reserve;
- `recipe347_ineligible_candidate_has_no_effect_and_falls_back_to_base_mining`: rejects missing, broken, suppressed, melded, inaccessible and absent candidate bodies, and proves ordinary extraction still succeeds without candidate effects;
- canonical save/load and rejection of a noncanonical mining boolean after checksum recomputation.

This acceptance proves the bounded TEST_ONLY slice and its integration contracts. It does not prove complete MGT-07 coverage, source parity outside the listed procedures or release eligibility.

## Schema77 extraction assistance contract (GPT-approved 2026-11-10)

GPT approved a bounded TEST_ONLY increment for direct exposed-node extraction: one predeclared trained assistant completes the entire existing task with the lead and adds exactly +1 to the lead's single check. The actual in-app GPT response, source pins, APIs, operational completions and runnable criteria are preserved in [the source/API review](evidence/2026-11-10-mgt07-assistant/SOURCE_API_REVIEW.md).

Bind assistant training to the existing `SkillTrainingRecord` lookup for `mining-tools` with proficiency rank greater than zero. Rank 1 and 2 each qualify for the same +1. The lead retains its own selected ability, proficiency, tools and work eligibility; assistant training, ability, level, item magic, and equipment benefits do not transfer. Both participants must pass existing physical, access, hands, capability, work and receiver checks. The trusted authority must control both workers when starting or resuming the paired labor; this is a TEST_ONLY authorization binding, not source wording.

Select one fixed assistant at task start. Book the lead and assistant in matching `WorkLedger` intervals under one mining job. The pair's active seconds credit `MiningAttemptRecord.WorkDone` once. Full task includes setup, removal, and sorting/receipt. If either participant loses work eligibility, pause the attempt and truncate both future intervals at the same boundary; retain earned work and reservations. Resume only with the same eligible pair. This fixed-team interruption policy and retention of full-task qualification while `AwaitingCheck` are explicit operational TEST_ONLY completions.

Use an optional `AssistantId` in `MiningSelectionRequest`, immutable `AssistantId` on the attempt, and settled 0/1 `AssistantBonus` on the resolved check evidence. Preserve solo `mining-selection-v1` command fingerprints exactly; use an explicit v2 fingerprint/parser only for nonempty assistant requests. Reject assisted mining nested inside expedition-assignment commands. Schema77 appends assistant identity/result only in the new Mining codec branch; older schemas decode empty identity and zero bonus, without migration or changed replay semantics.

The approved first slice does not implement assistance for prospecting, nondestructive/destructive assay, standalone mineral preparation or expedition mining assignments. Late joining, helper replacement/drop-to-solo, generic hiring/consent, production qualification and any wider assistant system remain unsupported.
