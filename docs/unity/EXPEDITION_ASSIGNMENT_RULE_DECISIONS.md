# Expedition work assignment integration

**Status:** TEST_ONLY C# integration, extended by schema47 on 2026-11-06. This records assignment workflows over existing source procedures. It does not establish production site authority or invent a new repair, fishing or mining procedure.

## Source boundary

The Expedition Player Book FL-01–03 describes expedition membership, work assignments, location, elapsed time and actual travel; FL-18 supplies the ordinary structural repair requirements used by the existing repair handler. The pinned Fishing Recipe Playtest supplies the existing physical Trap, retrieval and receiving-location requirements. The pinned Mining and Gathering Tools guides supply the existing exposed-mineral procedure and its qualifications. The pinned Bodies, Equipment and Carrying Playtest supplies separate body-use and equipment-access context; it does not supply repair pricing or labor. Exact schema47 source snapshots are in the [mining-assignment evidence](evidence/2026-11-06-expedition-mining-assignment/SOURCE_BINDINGS.json); schema39 bindings remain in the [original assignment checkpoint](evidence/2026-11-05-expedition-assignments/SOURCE_BINDINGS.json).

The prototype connects those facts to the existing `WorldTraversalRecord`, shared `RuleClock`, repair, retrieval and mining procedure records, `WorkLedger`, `Simulation` transaction boundary and snapshot codec. Procedure qualifications, tools, hands, material claims, path/load/capacity checks and job work remain in the existing procedure handlers.

## Assignment contract

- An explicit request names a worker, procedure, target and, for Trap retrieval, receiving location. The engine derives the site from the authored repair fixture or the physical Trap record; the request cannot choose a different site.
- A schema47 mining assignment also stores the explicit deposit version and extraction selection (categories, ability, hurry and any result preferences). Its work site comes from the selected `MiningDepositRecord`; the assignment cannot supply or override coordinates. Starting delegates to the existing mining resolver, and its `MiningAttemptRecord` remains authoritative for the extraction.
- The selected TEST_ONLY fixture accepts one open assignment per worker. Assignment records persist the intended worker/procedure/target, derived site, current Travel/Ready/Started/Cancelled state and a linked procedure job ID after work begins.
- Assignment does not add time, an Action, a work interval, resource reservation, material debit, proficiency, inventory custody or tactical participation.
- The player directs travel with existing cardinal world-step commands. Travel uses actual traversal state and the shared clock. An assignment becomes Ready only when the worker reaches its site and has no active traversal. Partial progress and readiness survive save/restore.
- Starting work is a separate command. It invokes the existing procedure handler, so all source-specific qualification and access checks are repeated at the moment work starts. The assignment stores the resulting job ID; the existing procedure record remains authoritative for pause, resume, completion and cancellation.
- The start command still requires the current inventory-owner grant for a Trap the retrieval will transfer into the worker's custody. Controlling the worker alone does not grant that access.
- Cancellation is available only before work starts and does not cancel movement already under way. Once a procedure has started, use its existing controls.

## Persistence and validation

Schema39 appends the assignment collection after the schema38 Trap stock projection. Schema47 appends mining-selection fields to assignment records; schemas39–46 retain their prior assignment wire layout, and schemas1–38 remain unchanged. There is no implicit migration. Snapshot validation checks unique assignments, one open assignment per worker, actor/site readiness, timestamps and links from started assignments to their actual repair, retrieval or mining record. The 64-record bound counts closed history as well as open assignments. Command receipts reconstruct the full mining selection and replay through the same dispatcher.

The first fixture combines a finite physical Trap world with either the Trap retrieval or the repair procedure so the schema remains a valid extension of schema38. That is a TEST_ONLY versioned fixture composition, not a production requirement that all camps contain a fishing Trap.

## Verification and limits

The schema39 suite passed **1,106/1,106**; the schema47 integration passes in the current **1,159/1,159** full suite. The repair case saves during a partial route, restores, reaches the authored site, and starts the existing repair. The Trap case travels to the physical Trap and starts retrieval for the same catch; an unauthorized owner grant rejects without mutation. The schema47 mining case persists partial travel and in-progress extraction, restores both, settles finite stock through the shared mining resolver and protects duplicate replay. Exact schema39 evidence remains in the [original checkpoint](evidence/2026-11-05-expedition-assignments/README.md); schema47 reports and source hashes are in the [mining-assignment evidence](evidence/2026-11-06-expedition-mining-assignment/README.md).

This does not add a general site directory, assistant assignments, autonomous or overland route planning, simultaneous off-calendar movers, encounter transitions, network ownership or production site authority. The records currently cover one worker's explicit assignment to the two existing TEST_ONLY procedures. Unity integration and gameplay qualification remain deferred.
