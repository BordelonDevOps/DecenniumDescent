# Schema50 ordinary physical receptacles

This is a bounded **TEST_ONLY** implementation of ordinary lock attempts on authored stationary portable receptacles. It does not promote fixture content or close the whole EXP-03 exploration work item.

## Responsibilities and authoritative records

| Concern | Authority |
| --- | --- |
| Lock state and binding to one container, owner and exact physical credentials | `OrdinaryReceptacleLockRecord` |
| Working and completed key/pick attempts, check result and timestamps | `OrdinaryReceptacleAttemptRecord` |
| Container closure, physical item identity, placement, custody, mass, capacity and access | Existing `PortableEquipmentRecord` and portable-equipment rules |
| Finite receptacle contents, location and inventory history | Existing `ResourceLot`, `InventoryLotRecord` and `WorkLedger` |
| Paid Action, six-second exploration work, interruption and shared-clock scheduling | Existing world Action intervals, `WorkLedger` and `RuleClock` |
| Pick check, conditions and random state | Existing character/life records, `PlaytestRolls`, shared RNG and condition view |
| Command admission, detached transaction, receipts, replay and save encoding | Existing shared simulation and canonical snapshot codec |

Ordinary keys have no source-specified mass in the pinned rules. Their fixture records preserve unknown mass (`PortableMassBasis.Unmodeled`); no zero-weight value is invented, and carried-burden calculations fail closed. Opening and retrieving contents still use the existing portable-equipment procedures.

The existing source-bound procedure and approved provisional timing policy are documented in [SUPPLY_CACHE_RULE_DECISIONS.md](../../SUPPLY_CACHE_RULE_DECISIONS.md): a physical key or actual thieves' tools, DEX check against DC15 when picking, the relevant proficiency bonus only when trained, six active exploration seconds, and opening as a separate one-second operation. Tactical unlocking uses the existing Action path without exploration labor.

## Reusable behavior versus fixture assumptions

The new lock and attempt records and their validation support multiple lock/container identities, distinct physical keys, actual thieves' tools, deterministic interruption/completion and exact links to existing portable containers. Scheduling, inventory movement, closure and replay stay in shared systems.

The runnable fixture supplies two stationary 25 lb chests with 300 lb / 12 cubic foot capacities, two finite 2 lb ration lots, coordinates, ownership and whether each exact key is present. One thieves' tools item is available. The chest dimensions, placements, contents and key availability are fixture facts; the source does not establish a general chest template, arbitrary item fit, item volumes or key mass. The handler does not yet provide production content authoring or a general object factory.

## Runnable acceptance

Run the full shared C# suite:

```powershell
pwsh -NoProfile -File engine/tools/Test-Foundation.ps1
```

The schema50 cases verify closed-container access rejection, exact-key query purity, a successful six-second pick, save/restore while a companion crop advances, deterministic check settlement once, lock independence, separately timed opening, finite content retrieval, custody/access synchronization, completed replay and interruption that keeps paid time but releases future labor correctly. A focused interruption run is also archived.

| Validation | Result |
| --- | --- |
| `ordinary_receptacle_interruption_retains_paid_time_and_claims_credential` | **PASS — 1/1** |
| `pwsh -NoProfile -File engine/tools/Test-Foundation.ps1` | **PASS — 1,167/1,167**, C# 9 warnings as errors |
| `pwsh -NoProfile -File engine/tools/Validate-Package.ps1` | **PASS — 18 checks, 229 assets, 229 unique GUIDs** |

Exact reports are [focused](FOCUSED_INTERRUPTION.json), [full suite](HEADLESS_RESULTS.json) and [package checks](PACKAGE_RESULTS.json). Source-file SHA-256 values and the pinned source revision are in [SOURCE_HASHES.json]; the full-suite report also records hashes for every compiled source file.

## Gaps and delivery state

This increment does not implement doors, forced entry, lock damage, traps, searching, examination, digging, marking, route discovery, general world-object authoring, arbitrary container fitting or production content. Earlier snapshot versions keep their previous payload branches. The full engine is not complete.

The local `Engine` branch has not been pushed, and this increment has not been sent to GPT for review. The repository handoff records the branch and working-tree state.
