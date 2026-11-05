# Expedition work assignment integration

**Status:** TEST_ONLY C# integration checkpoint, recorded 2026-11-05. This records an assignment workflow over existing source procedures. It does not establish production site authority or invent a new repair or fishing procedure.

## Source boundary

The Expedition Player Book FL-01–03 describes expedition membership, work assignments, location, elapsed time and actual travel; FL-18 supplies the ordinary structural repair requirements used by the existing repair handler. The pinned Fishing Recipe Playtest supplies the existing physical Trap, retrieval and receiving-location requirements. The pinned Bodies, Equipment and Carrying Playtest supplies separate body-use and equipment-access context; it does not supply repair pricing or labor. Exact source copies and hashes are in the [checkpoint evidence](evidence/2026-11-05-expedition-assignments/SOURCE_BINDINGS.json).

The prototype now connects those facts to the existing `WorldTraversalRecord`, shared `RuleClock`, `RepairWorkRecord`, `FishingTrapRetrievalRecord`, `WorkLedger`, `Simulation` transaction boundary and snapshot codec. Procedure qualifications, tools, hands, material claims, path/load/capacity checks and job work remain in the existing repair and retrieval handlers.

## Assignment contract

- An explicit request names a worker, procedure, target and, for Trap retrieval, receiving location. The engine derives the site from the authored repair fixture or the physical Trap record; the request cannot choose a different site.
- The selected TEST_ONLY fixture accepts one open assignment per worker. Assignment records persist the intended worker/procedure/target, derived site, current Travel/Ready/Started/Cancelled state and a linked procedure job ID after work begins.
- Assignment does not add time, an Action, a work interval, resource reservation, material debit, proficiency, inventory custody or tactical participation.
- The player directs travel with existing cardinal world-step commands. Travel uses actual traversal state and the shared clock. An assignment becomes Ready only when the worker reaches its site and has no active traversal. Partial progress and readiness survive save/restore.
- Starting work is a separate command. It invokes the existing procedure handler, so all source-specific qualification and access checks are repeated at the moment work starts. The assignment stores the resulting job ID; the existing procedure record remains authoritative for pause, resume, completion and cancellation.
- The start command still requires the current inventory-owner grant for a Trap the retrieval will transfer into the worker's custody. Controlling the worker alone does not grant that access.
- Cancellation is available only before work starts and does not cancel movement already under way. Once a procedure has started, use its existing controls.

## Persistence and validation

Schema39 appends the assignment collection after the schema38 Trap stock projection. Schemas1–38 keep their original encoded layout. There is no implicit migration. The source fingerprint includes the selected assignment fixture. Snapshot validation checks unique assignments, one open assignment per worker, actor/site readiness, timestamps and links from started assignments to their actual repair or retrieval record. The 64-record bound counts closed history as well as open assignments. Command receipts reconstruct assignment requests and replay through the same dispatcher.

The first fixture combines a finite physical Trap world with either the Trap retrieval or the repair procedure so the schema remains a valid extension of schema38. That is a TEST_ONLY versioned fixture composition, not a production requirement that all camps contain a fishing Trap.

## Verification and limits

The deterministic C# suite passes **1,106/1,106**. The repair case saves during a partial route, restores, reaches the authored site, and then starts the existing repair. The Trap case travels to the physical Trap and starts the existing retrieval for the same catch; an unauthorized owner grant rejects without mutation, and an authorized retry succeeds. Separate cancellation and full-history capacity cases verify no assignment side effects and correct counting of closed records. Core/Persistence/LabModel compile under C# 9 with warnings as errors; static package checks pass **14/14**. Exact source/test/code hashes and results are in [the evidence folder](evidence/2026-11-05-expedition-assignments/README.md).

This does not add a general site directory, assistant assignments, autonomous or overland route planning, simultaneous off-calendar movers, encounter transitions, network ownership or production site authority. The records currently cover one worker's explicit assignment to the two existing TEST_ONLY procedures. Unity integration and gameplay qualification remain deferred.
