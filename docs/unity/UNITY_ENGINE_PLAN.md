# C# gameplay simulation: architecture boundaries and historical Stage 0 assessment

**Historical C# checkpoint, 2026-11-05 (superseded):** the project was already on Engine and contained the shared simulation layers. The known schema42 harvest-manifest failures at that checkpoint were subsequently addressed; they are not current failures.

**Persisted baseline:** schema61. **Latest C# correction (schema61 layout unchanged, TEST_ONLY):** the opt-in expedition profile registers controlled workers at existing Camp Greens, mining, and one physical tool-repair site. The repair path uses `IsRepairWorker` eligibility and `SharedRepairFixture.Trained`, plus the existing repair handler and physical toolkit/material checks; assignment registration grants neither. GPT found the custom worker-only hash could exceed the 96-character snapshot header. Custom profiles now hash seed/water quantities and a length-prefixed roster behind a short fixed prefix, while exact default and established actor/companion identities remain unchanged. A direct custom crop simulation initialization and codec roundtrip now passes. No snapshot fields, codecs or historical save layouts changed. Validation passes **1,242/1,242** C# 9 warnings-as-errors cases, **4/4** focused cases, **18/18** static package checks (**271 assets / 271 unique GUIDs**), and **5 source snapshots / 17 profiles / 340 RP cells / 4 named tests**. See [tool-repair assignment evidence](evidence/2026-11-08-expedition-tool-repair/README.md), [worker/site binding evidence](evidence/2026-11-08-expedition-worker-site-bindings/README.md), and the [implementation trace](IMPLEMENTATION_TRACE.md#2026-11-08--registered-physical-tool-repair-assignment-schema61-layout-unchanged-test_only). General repair sites, scheduling, recruitment, autonomous travel, production site authority, and the full engine remain unfinished.

**Previous schema60 C# increment (TEST_ONLY):** `CharacterStateFacts` joins existing actor character, optional skill-training, and life records without creating runtime or persisted copies. Injury-aware checks use one actor-bound view across exploration observation/routes, tactical Medicine, and management work/locks. Connected assigned mining is saved/restored, advanced in two identical restored simulations, and compared byte-for-byte before duplicate-command replay and continued exploration. No rule or save fields changed. See [actor-state evidence](evidence/2026-11-07-character-state-facts/README.md), [shared skill-training evidence](evidence/2026-11-07-shared-skill-training/README.md), and [shared numeric character-state evidence](evidence/2026-11-07-shared-character-state/README.md). Character creation, grants, generalized progression, class rules and production character content remain incomplete.

**Previous persisted increment (schema60, TEST_ONLY):** adds scoped route reconnaissance feasibility on top of schema59 Map Route work/check. A singleton traveler approaches a fingerprinted Unknown/Risk-0/Secured/two-Progress route mouth, reserves 480 active minutes, and resolves the existing WIS (Survival) route-tier check. The inspection profile binds its method, visible facts, and sight/walkability access. A successful result authorizes only the exact route/traveler/starting-progress segment; travel remains in the existing `ExpeditionRouteTravelRecord`. Its source decisions and evidence are in [schema60 reconnaissance evidence](evidence/2026-11-07-route-reconnaissance/README.md). Moving reconnaissance, general cohorts, positive Pressure/capacity settlement, production routes, and the complete engine remain unfinished.

**Earlier architecture checkpoint, 2026-11-07 (schema55):** on `Engine`, schema55 appends TEST_ONLY hunting-trap deployment, action, trigger and tether records after schema54 route knowledge. Portable equipment remains authoritative for each physical item’s identity, custody and mass; route travel, world/tactical movement, shared clock/work, RNG/life, receipts and canonical persistence remain shared authorities. Real checkpoint arrivals queue exactly-once trap occurrences through recorded movement ordering. The accepted 3-foot constraint is enforced without adding Restrained; a pending overlength Push is gated before its rider save, and established tethers retain a separate displacement gate. The full suite passes **1,204/1,204** under C# 9 warnings-as-errors and static package validation passes **18/18 checks (253 assets / 253 unique GUIDs)**. GPT's summary-based implementation review found no confirmed blocker and suggested three optional focused regressions. Schema55 behavior remains explicit TEST_ONLY content. Arbitrary hazard geometry, trap discovery, mid-leg route triggering, unsupported movement modes, production profiles and the complete rules engine remain unfinished. See the [current handoff](DEVELOPMENT_HANDOFF.md), [hunting-trap decisions](HUNTING_TRAP_RULE_DECISIONS.md), [implementation trace](IMPLEMENTATION_TRACE.md#2026-11-07--ordinary-hunting-trap-lifecycle-schema55-test_only) and [schema55 evidence](evidence/2026-11-07-hunting-trap/README.md).

**Preceding schema54 architecture checkpoint, 2026-11-07:** on `Engine`, schema54 appends TEST_ONLY route-mapping result records to the shared snapshot after existing schema53 motion/observation state. Per-route knowledge derives from immutable authored Mapping plus accepted result history; a fingerprinted trusted fixture supplies synthetic pre-resolved outcomes. The shared query/resolver, command receipts, replay, and canonical codec own acceptance and persistence. Schema54 release snapshots are rejected, and schemas 1–53 retain their prior codec branches. The result ledger does not execute Map Route checks, claim labor, consume RNG/inventory/time, mutate authored route Mapping, or unlock Unknown travel. Three focused mapping/compatibility cases pass; the full C# 9 warnings-as-errors suite passes **1,198/1,198**; static package validation passes **18/18 checks (249 assets / 249 unique GUIDs)**. An authentic pre-schema54 schema53 moving-route save now roundtrips byte-identically and reproduces its archived next-interval bytes for this single history. The route fixture remains TEST_ONLY, and actual Map Route checks, reconnaissance/feasibility, risk/hazards, capacity settlement, convoy behavior, production routes and the complete engine remain unfinished. See the [current handoff](DEVELOPMENT_HANDOFF.md), [source trace](ROUTE_DISCOVERY_RULE_TRACE.md), [prototype decision](ROUTE_MAPPING_RESULT_RULE_DECISIONS.md), [implementation trace](IMPLEMENTATION_TRACE.md#2026-11-07--fl-10-map-route-result-accounting-schema54-test_only) and [compatibility evidence](evidence/2026-11-07-schema53-route-save-compatibility/README.md).

**Current rule map:** [IMPLEMENTATION_TRACE.md](IMPLEMENTATION_TRACE.md) routes all 75 existing source areas into 49 work items against source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. The map covers rule conversion and dependencies; it does not claim that all source rules or systems are implemented. Continue across the mapped exploration, tactical, and resource-management dependencies without promoting TEST_ONLY content.

Assessment date: 2026-10-20 America/Chicago. Execution evidence timestamps use UTC. This is a historical Stage 0/Stage 1 assessment; current implementation status is maintained in the handoff and trace.

## Product direction

The owner direction is a tactical CRPG with direct-control exploration, tactical combat and companion-driven resource management over one shared simulation. Turn-based combat is selected for the first prototype; the final game's combat mode remains reserved. The owner explicitly directed a C#-first engine, with presentation integration only after the C# engine is complete. Existing laboratory controls and authored fixtures remain TEST_ONLY; they are not production game content.

The supplied [development brief](DEVELOPMENT_BRIEF.md) is preserved byte-for-byte. Its execution instruction authorizes this bounded technical increment even though older authoring handoffs reserved implementation. That does not promote any gameplay rule or authorize later stages.

## Verified repository and reuse

| Item | Observed result |
| --- | --- |
| Expected source location | `C:\Github\DecenniumDescent` exists but is not a Git repository. It contains newer, ongoing authoring work. |
| Implementation checkout | `C:\Users\cbord\Documents\ChatGPT\Decennium Descent\github-delivery` |
| Identity | `https://github.com/BordelonDevOps/DecenniumDescent.git` |
| Branch / HEAD | `main` / `9367b319e460134a3fc35b530da29ecbe6224b6a` |
| Initial state | No tracked or untracked changes with `git -c core.longpaths=true status --porcelain=v1 -uall`. Default Windows long-path handling gave false deletions; no files were restored or deleted. |
| Remote currency | Unverified. No fetch, pull, push, merge or source synchronization. |
| Existing Unity foundation | No first-party Unity project, scenes or asmdefs found in the inspected source/workspace trees. Unrelated asset-extractor C# is not game engine code. |
| Existing rule models | Python core/combat/temporal models and validators retained. Six selected pre-existing core-model expectations passed; no production C# rule port was made. |
| Existing schemas/saves | Character playtest JSON and status registries retained. Browser `character-storage.js` remains its own localStorage migration path; it is not a full engine save format. |
| New work boundary | New `engine/` and `docs/unity/` files only. Existing authority, historical reports, source data and root pointers were not rewritten. |

[STAGE0.json](evidence/STAGE0.json) contains command outputs, exact source paths, SHA-256 bindings, tool versions, the reuse map and the six baseline assertions. Authoring-tree hashes are a time-specific observation; ongoing authoring may advance after the audit.

The sole domain authority routing remains [CANON_MANIFEST.md](../../CANON_MANIFEST.md) → [docs/canon/CANON_MANIFEST.json](../canon/CANON_MANIFEST.json), with [promotion policy](../canon/REPOSITORY_PROMOTION.md) and [continuity policy](../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md). This document and the implementation trace are engineering records, not a competing content registry.

Current amendments were inspected in the authoring tree: `DEVELOPMENT_DIRECTION.md`, `UNITY_DEVELOPMENT_DIRECTIONS_INTAKE_75.json`, `PERTINENT_GPT_DECISIONS_2026_10_20_02.json`, `FULL_GAME_CURRENT_REVIEW_MAP_82.md`, and `ACTIVE_AUTHORING_CHECKPOINT_GENERAL_COMBAT_CASEBOOK_99.json`; full paths and hashes are in Stage 0 evidence. Host plus up to four guests is retained from the current supplied brief. An older direct-owner record confirming that exact count was not located in the inspected records; no multiplayer implementation or peer-capacity validation is claimed.

## Technical boundary now implemented

```mermaid
flowchart LR
    UI[TEST_ONLY Unity buttons] --> Adapter[Trusted local authority adapter]
    Adapter --> Gateway[Validate command and revision]
    Gateway --> Core[Detached candidate transaction]
    Policy[Isolated TEST_ONLY policy] --> Core
    Core --> Snapshot[Committed snapshot and receipts]
    Snapshot --> View[Unity squares and labels]
    Snapshot --> Save[Versioned snapshot codec and local store]
    Save --> Restore[Validate schema and content before restore]
    Restore --> Core
```

The Core assembly owns snapshots and command validation. It uses no Unity objects, frame deltas, wall clock, animation callbacks or device input. Host-derived authority is a separate argument, never a client-claimed field. Every rejected command preserves the owned state, revision, RNG and receipts. A successful command validates a detached candidate before replacing state. Duplicate IDs are scoped by trusted principal and retain their original fingerprint/revision across save/load. Current authorization is checked even on retries.

**Current C# read path (2026-11-05):** authoritative procedure records, `WorkLedger`, `WorldTraversalRecord`s and the snapshot feed transient `WorldActivityProjection` views. Same-revision `Simulation.DiscoverCommands` results supply admissible controls; the projection does not authorize or execute them. `CurrentWork` remains the active-labor conflict view, while `OpenProcedures` adds stored working/paused/awaiting states and `Traversals` describes persisted partial routes. Manufacturing quality choices and Pause/Resume/Cancel queries share assessment with the existing resolver, and discovery exposes only the controls that assessment permits for the order owner. This arrangement adds no second activity store or schema and keeps settlement, clock continuation, reservations and replay in their existing authoritative paths.

```mermaid
flowchart LR
    Snapshot[Snapshot + procedure records + WorkLedger + traversal records] --> Projection[Transient activity projection]
    Discovery[Same-revision command discovery/query] --> Projection
    Projection --> Reader[Read-only caller]
    Manufacturing[Manufacturing choice or control command] --> Assess[Shared resolver assessment]
    Assess --> Transaction[Existing detached transaction and resolver]
    Transaction --> Snapshot
```

Persistence is a separate engine-free assembly. Its binary format includes schema/content/RNG versions and a checksum, rejects unsupported data, and atomically replaces a validated local snapshot while retaining the preceding good save. Explicit backup recovery preserves the old primary as evidence. The initial format deliberately rejects incompatible schemas rather than pretending to migrate them.

Unity presentation only submits commands and reads detached snapshots. One local adapter currently supplies laboratory authority for two actor IDs. No transport, account authentication, guest ownership synchronization, prediction, reconciliation or reconnect protocol exists. A typed `CommandResult` and snapshot are sufficient for this increment; a general event bus and production content loader are deferred until an actual approved feature needs them.

Core and Persistence have `noEngineReferences: true`. Unity documents that this setting prevents automatic UnityEngine/UnityEditor references. This is an assembly boundary, not proof that an Editor successfully compiled the package. [Unity assembly definition reference](https://docs.unity3d.com/6000.0/Documentation/Manual/class-AssemblyDefinitionImporter.html).

## What the fixture proves, and its limits

The synthetic policy owns the 5-by-5 grid, one wall, two actor identities, one adjacent container and one token. Those are TEST_ONLY data. Manual integer ticks have no seconds, rounds, feet, costs or elapsed-offline meaning. Moving the square is a command-path exercise; it does not implement the required production direct-control exploration, running or jumping. The companion is an occupancy/authority fixture without AI or management jobs. The laboratory UI framework is not a production UI-framework decision.

The package provides an idempotent scene builder because no Editor was available to serialize or run a scene. New package metadata is paired and has stable GUIDs; importer-specific initialization still requires Unity. No commercial disc assets, external services or new packages were installed.

## Decisions that remain open

| Decision | Evidence or evaluation needed | What remains independent |
| --- | --- | --- |
| Combat cadence and exploration transition | Owner decision and gameplay evaluation of tactical command timing, pause behavior and transitions. Do not equate tactical with turn-based. | Command validation, persistence and authority checks. |
| Camera, geometry and visual production method | Compare SNES-style views and 2D/2.5D approaches against readability, navigation, animation and content-production cost. | Core identities and interfaces. Laboratory squares are not art direction approval. |
| Movement/collision/jumping | Current source resolution for world units, continuous/discrete movement, range, speed, jump rules and input feel. | Lab movement remains isolated policy. |
| Time and work progression | Approved conversions, interruptions, partial work, resting and offline advancement rules. | Integer clock serialization and rejection invariants. |
| Combat/resource formulas and outcomes | Verify domain bindings, current owner amendments and implementation permission per rule. Research/crafting rewards cannot be guessed. | Infrastructure tests use no production rewards. |
| Target platforms, render pipeline and Editor version | Choose a supported installed Editor and intended first build target; profile the eventual slice. No concrete Editor version or production pipeline is pinned yet. | Package boundary and headless verification. |
| Production save lifecycle and co-op protocol | Resolve content compatibility, receipt retention/session epochs, migration, peer ownership and host disconnect handling. | Bounded local fixture save/retry proof. |

## Delivery gates

Authored, implemented, tested and publication-approved remain separate. The [implementation trace](IMPLEMENTATION_TRACE.md) records technical evidence without changing canon statuses. The C# engine has a connected headless exploration/combat/management acceptance, but broad system coverage and production-rule promotion remain incomplete.

The current C# checkpoint is schema70: the bounded Temporary Camp construction increment composes with existing exploration, shared-clock work, inventory, combat, camp use and Pressure authorities. GPT's review of `e1bf33c3a52c4ccd365c8a5ff70880464e91a92e` found a residual pre-attempt movement defect; the follow-up correction now passes the focused save/restore case and the 1,298-case full suite, with GPT re-review pending. The next dependency remains gated until GPT reviews the pushed evidence and agrees the module is accepted and the successor follows the approved dependency map. Keep authoritative records, source pins, unsupported behavior and validation evidence explicit in the [handoff](DEVELOPMENT_HANDOFF.md) and [implementation trace](IMPLEMENTATION_TRACE.md). Continue substantial source-bound gameplay work toward the connected exploration/combat/resource-management objective; a fixture or schema bump alone does not establish engine completion.
