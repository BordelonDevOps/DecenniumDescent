# MGT-07 prospecting rule implementation boundary

**Status:** schema44 TEST_ONLY prospecting and observable-evidence slice. The governing sources are reviewed authored operational playtest material, not release-approved canon.

## Governing sources

Pinned revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.

| Source | Relevant material | SHA-256 of checked-in bytes |
| --- | --- | --- |
| [Mining candidate field guide](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/MINING_CANDIDATE_GUIDE.md) | Choose the procedure; prospecting outcome and repetition rules | `726cb84a1104901f5b05b412039b458af5bb5168e4482fb9e9844b1b42b697c3` |
| [Gathering tools candidate guide](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md) | Untrained information tasks; actual implements and task operation | `9b1e4defcd18569ad8d8305552ad740e62be1faea3e1de448e364bd7536215bc` |
| [Gathering tool body catalogue](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/GATHERING_TOOL_CANDIDATE_BODY_CATALOGUE.md) | Prospecting-tool entry and physical limits | `23fb5db0282881499abcddaa3cd259bab4262a34c884e5a80c1de8a894c5dd99` |

The pinned source snapshots are archived with the [schema43 mining extraction evidence](evidence/2026-11-05-exposed-mineral-extraction/README.md). The first two guides are operational playtest sources; the internal body catalogue is not independently approved gameplay content. Their text is not promoted by this implementation.

## Responsibilities and authoritative records

| Concern | Authority |
| --- | --- |
| Canonical patch identity, site/owner/coordinates, current exposure pointer | `ProspectingPatchRecord` |
| Immutable, linked exposure facts, method, actual access, requirements, authored findings, asserted cause and shared-clock time | `ProspectingExposureRecord` |
| One worker's attempt, exact work/status, WIS and proficiency inputs, DC, deterministic check audit, outcome, invalidation reason, and findings learned | `ProspectingAttemptRecord` |
| Supported content for the TEST_ONLY world: authored patch profiles, possible observable statements and physical implements | `ProspectingPatchFixtureContent`, `ProspectingExposureProfile`, `ProspectingObservationProfile` in `SharedProspecting.cs` |
| Active labor and clock advancement | Existing shared `WorkerInterval`, activity procedure and simulation clock |
| Command authority, event ordering, RNG state, duplicate-command idempotency and snapshot transaction | Existing `Simulation`, `CommandReceipt`, and `Snapshot` pipeline |
| Durable encoding | `ProspectingCodec` appended to `SnapshotCodec` schema44; `CommandHistory` reconstructs canonical exposure requests |

Core owns the persisted records, invariants, and schema migration boundary. Persistence owns wire encoding. LabModel owns only TEST_ONLY scenario authoring and execution. No global RNG, clock, inventory, or job scheduler was added. Schema44 appends its section after the schema43 mining payload; legacy schema bytes are preserved.

## Source-authored rules represented

- Prospecting takes **10 active minutes**, uses **Wisdom/Mining**, and concerns one exposed, accessible patch no larger than **100 square feet**.
- The source sets DC **12** for clear signs, **15** for obscured signs, and **18** for severe but feasible signs.
- Untrained prospecting has no Miner's-tools proficiency contribution and uses disadvantage. The ordinary information task has no recipe/formula gate.
- Success returns real observable evidence and possible access for that patch. Core task degrees and natural shifts apply. Success and Critical Success disclose the same authored facts; neither creates a deposit, extra quantity, preparation, or hidden detection. Failure supplies no reliable new finding. Critical Failure adds only a hazard declared before work.
- Repeating unchanged evidence, renaming the patch, or changing the worker grants no new roll. A genuinely new exposure or concretely different evidence-bearing method can support a new attempt.
- Actual access, physical suitability, required implements, and the lead's genuine operation remain necessary. Tool possession alone does not grant proficiency or other benefits.

## Adopted bounded completion and fixture limits

The implementation binds each exposure version to one explicit method and its authored requirements. A successful attempt records only the fact IDs on that exposure. `PossibleAccess` remains an observation distinct from the exposure's actual `Accessible` state. Observation queries return facts learned by the worker; party-wide knowledge propagation is not added.

Voluntary pause, interruption, and save/restore retain prospecting labor in the shared work ledger. When the 600-second endpoint is reached, shared automatic events are processed first, then current eligibility is checked. A temporarily ineligible completed job remains `AwaitingCheck`; a later eligible resume resolves the saved check once without additional labor or a reroll. This is an operational completion agreed for the prototype, not added source wording.

A trusted host `RecordProspectingExposure` command appends a linked exposure at the current rule time. A changed ID alone is insufficient: the new version must materially change authored evidence or method facts. An exposure change invalidates open attempts against the former version, records the cause and time, and preserves completed labor without checking or transferring that work to the new version. The host-supplied cause ID is a trusted assertion. This fixture cannot authenticate that an external world event actually occurred.

The TEST_ONLY content admits only `TEST_ONLY.prospecting.hazard.none`; unknown and non-none hazard profiles fail closed. It does not apply prospecting-tool bonuses, assistant bonuses, or every catalogue body's operational/qualification rules. Fixture record limits and synthetic observations are technical test bounds, not game balance or production world facts. `PossibleAccess` is not permission to enter; the host authors actual accessibility separately.

## Unsupported behavior and open gaps

- The separate schema45 slice implements only nondestructive assay against an already-authored exposed manifest; see [mineral assay decisions](MINERAL_ASSAY_RULE_DECISIONS.md). Destructive assay still requires a real, debited sample. Prospecting never synthesizes either a manifest or sample.
- General hazard declarations and hazard consequences are not implemented. Only the explicit no-hazard test profile is runnable.
- Assistant work and the source-specific +1, magical gathering-tool benefits, candidate registration/comparison, and the full qualifying-operation protocol remain outside this slice.
- Production-authoritative geological state, externally verified exposure causes, shared party knowledge, broad site geometry/permission, new deposits, hidden reserves, mineral quantities, and all remaining MGT-07 procedures remain unsupported.

## Runnable acceptance and evidence

Run from the repository root:

```powershell
pwsh -NoProfile -File engine/tools/Test-Foundation.ps1
```

The focused cases cover authored DCs and observable-only success facts; untrained disadvantage and failure disclosure; pause, save/resume, shared labor and repeat prevention; materially new exposure and invalidation without a check; and actual authored implements and hands. The full deterministic suite passes **1,148/1,148** after this increment. C# 9 warnings-as-errors compilation passes for Core, Persistence, and LabModel; static package validation passes **18 checks, 217 assets, and 217 GUIDs**. Exact reports and implementation limits are in [the schema44 prospecting evidence](evidence/2026-11-06-mining-prospecting/README.md).

This validates a narrow TEST_ONLY workflow and its existing shared-system integration. It does not establish complete MGT-07 coverage, release-rule approval, or a complete game engine.
