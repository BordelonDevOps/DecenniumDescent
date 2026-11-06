# MGT-07 mineral assay implementation boundary

**Status:** schema45 introduced a TEST_ONLY nondestructive manifest assay; schema46 adds a separate TEST_ONLY destructive assay for an already-authored physical sample portion. The governing text is reviewed authored operational playtest material, not release-approved canon.

## Governing source and stable binding

Stable binding: `MGT-07.ASSAY.MANIFEST`.

Pinned source revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

| Source | Applicable section | SHA-256 of checked-in bytes |
| --- | --- | --- |
| [Mining candidate field guide](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/MINING_CANDIDATE_GUIDE.md) | Choose the procedure; operational-assay results and repeat evidence | `726cb84a1104901f5b05b412039b458af5bb5168e4482fb9e9844b1b42b697c3` |
| [Gathering tools candidate guide](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md) | Set up one real task; untrained ordinary information tasks; tool operation | `9b1e4defcd18569ad8d8305552ad740e62be1faea3e1de448e364bd7536215bc` |

The schema46 operational policy is also recorded in the machine-readable [assay policy contract](MINERAL_ASSAY_POLICY.json), SHA-256 `3b39253d850ffebd752c452ddbdefb7f4e7b25d6dda5d49046755d4ddead555f`. Assay-bearing TEST_ONLY content fingerprints bind the pinned source revision, both source hashes and this exact policy-contract hash. Changing any of those inputs changes the save's content identity; update the implementation binding deliberately when the adopted policy changes.

The source says assay takes **one active minute**, uses **WIS/Mining**, and examines one exposed mineral manifest or actual sample. Use the exact source DC or the highest assessed tier DC. Supported results are mineral categories, suitability and known handling requirements. Untrained ordinary information work has no relevant tool proficiency contribution and uses disadvantage. Core task degrees and natural shifts apply; information failure gives no reliable new finding. A critical result creates no extra quantity, preparation, deposit or hidden detection. Repeating unchanged evidence or changing only the worker does not grant another roll; genuinely different evidence or method can support a separate attempt. A destructive assay needs an actual sample debit; nondestructive examination creates no inventory.

These sources and bindings remain playtest sources. This implementation does not promote them to release rules.

## Responsibilities and authoritative records

| Concern | Authority |
| --- | --- |
| Exposed deposit, categories and finite mineral units | Existing `MiningDepositRecord`, `MiningCategoryRecord` and `MiningMaterialUnitRecord` |
| Assay profile identity, assessed categories, source DC, required hands/implements and authored findings | `MiningAssayProfileRecord` |
| One attempt's active work, worker/check inputs, resolution and learned finding IDs | `MiningAssayAttemptRecord` |
| Worker eligibility and shared labor intervals | Existing shared world policy and `WorkLedger` |
| Command authority, revisions, RNG, receipts, snapshot transaction and replay | Existing `Simulation`, `CommandReceipt` and `Snapshot` |
| Durable encoding | `MiningAssayCodec`, appended after schema44 in snapshot schema45 |
| TEST_ONLY authored setup and execution | `SharedMiningFixture` and `TestOnlySharedWorldPolicy` in `SharedMining.cs` and `SharedMiningAssay.cs` |

Core owns durable assay records and invariants. Persistence owns schema45 encoding. LabModel owns only the TEST_ONLY profile authoring and resolver. Work uses the existing shared clock and worker intervals; no independent clock, RNG, inventory, or scheduler was added. Assaying a manifest is nondestructive and leaves mineral units, physical items and inventory lots unchanged.

## Implemented source behavior

- A valid attempt takes 60 active seconds and checks WIS/Mining against the exact authored DC, or the highest tier among its assessed categories when no exact DC is authored.
- Untrained attempts have no Mining-tools proficiency contribution and use the shared disadvantage resolution.
- Success and Critical Success reveal exactly the profile's authored category, suitability and handling fact IDs. Failure and Critical Failure reveal none. Critical Success adds no other result.
- Learned-fact queries bind each result to the profile of that worker's successful attempt. Reusing a finding ID in another profile does not disclose that profile's fact.
- The profile must bind to an existing exposed deposit version and accessible authored categories. Required hands and physical implements are explicit fixture data and are checked at start, during work, and before resolution.
- Pause, save/restore, resume, shared labor credit, deterministic check audit, command discovery and duplicate replay use existing simulation paths.
- The attempt does not create, consume, move or value a mineral unit. The one profile/one attempt limit prevents repeating an unchanged profile in this bounded fixture.

## Fixture assumptions and unsupported behavior

The synthetic two-category mineral deposit, tier values, one-hand requirement, mining-tools item, facts about example suitability/handling, coordinates and worker are TEST_ONLY content. They do not establish production minerals, implement requirements, prices, suitability or handling facts. The physical item is a fixture prerequisite; this slice grants no assistant or magical tool bonus.

This increment admits one nondestructive manifest-assay profile per deposit. It does not implement sample preparation or residue disposition. It also does not yet allow a different evidence-bearing method or newly changed sample to create another assay profile/attempt. The source permits changed evidence to support another attempt, so the fixture's bounded authored profiles must not become a general gameplay retry rule. Assistant work, source-specific tool benefits, production geological authority and the broader mining system remain incomplete.

At schema45, sample amount, portion identity and debit timing were deliberately left open. Codex and GPT have since agreed on the provisional schema46 prototype policy below. These operational choices are not source-derived and do not promote the playtest source to release rules.

## Runnable acceptance

Run from the repository root:

```powershell
pwsh -NoProfile -File engine/tools/Test-Foundation.ps1
```

Focused cases:

- `mining_assay_uses_shared_work_save_resume_and_only_authored_findings`
- `mining_assay_uses_exact_source_dc_and_untrained_disadvantage_without_consumption`
- `mining_assay_findings_are_scoped_to_the_successful_profile`
- `mining_assay_codec_rejects_noncanonical_exact_dc_flag`

The cases exercise schema45 discovery and work cost; fallback tier and exact source DC; trained and untrained checks; pause/save/resume; exactly authored information; no stock mutation; repeat prevention within the one-profile fixture; deterministic replay; and strict decoding. Full results and hashes are archived in [mining assay evidence](evidence/2026-11-06-mining-assay/README.md).

## Schema46 destructive assay of an existing sample

**Status:** implemented as a bounded TEST_ONLY procedure using the shared simulation. The following operational gaps are resolved by Codex/GPT agreement for the prototype only; the pinned rule text does not specify sample quantity or debit timing.

### Source rules

The sample assay takes one active minute, uses WIS/Mining and the exact source DC or highest assessed tier DC, and can reveal only supported authored categories, suitability and known handling facts. Untrained ordinary information work uses no relevant tool proficiency contribution and disadvantage. Failure gives no reliable new finding; Critical Success grants no extra quantity or properties. An actual sample is required and a destructive assay debits it. Unchanged evidence, sample renaming/splitting or worker changes do not authorize a second resolved check; genuinely changed evidence or an evidence-bearing method can support another finite attempt.

### Codex/GPT provisional prototype policy

Codex and **Unity Rules Engine Development** agreed on the following operational completion. It is recorded as provisional game behavior, not recovered source text:

- Bind an assay to a physically existing sample with stable inventory identity/provenance and an exact positive quantity **Q**. The sample record must explicitly author that the whole portion is sufficient and compatible with the method. This increment accepts a prepared portion; it does not create or subdivide one. The runtime portion amount equals the inventory lot's authored created amount. It is never inferred from mass, price, tier or stack size.
- Starting reserves the entire portion and exclusive worker time. The shared WorkLedger reservation also locks the physical evidence opportunity against concurrent attempts. The portion is atomically debited with the first positive credited second. Zero-work cancellation consumes nothing. Consumed material cannot reappear as a new sample; no residue/output is invented when no disposition is authored.
- Pause or interruption preserves credited labor and the unresolved attempt. Resume is explicit and revalidates worker/tool access and continuing evidence. If the full 60 seconds are complete but the worker is temporarily unable to resolve, keep `AwaitingCheck`; eligible resume rolls once without extra work or a new sample. Save/restore is exact and grants no offline progress.
- Cancellation before positive labor releases the unused reservation. Cancellation after positive labor closes without a check, refund, finding or transferable labor. Labor from a cancelled attempt never shortens a later attempt.
- Track sample lot identity, canonical inventory-lineage evidence basis, source exposure and method profile separately. Splitting a lot, replacing a sample from the same root, renaming identities or changing the worker does not create evidence. A resolved check is unique per evidence basis and authored method profile across all workers. Method-profile content excludes its label when compared, so an identical renamed procedure does not grant a reroll. A new root sample or substantively different authored method may support another attempt, while finite unconsumed inventory still exists.
- Commit the check, findings, RNG and receipt atomically through the existing shared Simulation. Failure/critical failure produces no findings; success/critical success returns exactly the method's authored facts.

The runtime stores sample profiles, attempts and check audit in schema46 after the schema45 payload. The actual physical amount and remaining quantity live in the existing inventory lot and WorkLedger; no parallel stock ledger or clock was added.

### Scope limits

The accepted fixture has one prepared TEST_ONLY mineral portion at one authored site. It does not implement sample preparation, residue disposition, environmental evidence changes, new-sample acquisition, a general method-authoring workflow, assistants, source-specific tool benefits, general hazard invalidation or other MGT-07 procedures. Changed evidence is represented only by a distinct inventory lineage root; a new method is represented by a non-duplicate authored assay profile. Production authority and release approval remain outstanding.

### Runnable acceptance

Run `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` from the repository root. Two schema46 cases verify exact reservation and first-positive-work debit; 20-second work, pause, save/restore, 40-second resume and one deterministic finding; resolved-evidence retry prevention; pre-work reservation release; post-work nonrefundable debit; and duplicate-command idempotency. Results, source hashes, package validation and captured Codex/GPT policy are archived in [destructive assay evidence](evidence/2026-11-06-destructive-mineral-assay/README.md).
