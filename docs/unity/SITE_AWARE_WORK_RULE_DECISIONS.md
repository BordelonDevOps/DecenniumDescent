# Site-aware work integration decisions

**Status:** TEST_ONLY C# integration checkpoint, recorded 2026-11-05. This extends existing tool repair to an authored work-site position; it is not the general expedition assignment system.

## Source and boundary

The Expedition Player Book's repair procedure (FL-18) provides the existing repair's toolkit, material, active-labor, tool-task and recoverable-body requirements. FL-01–03 supplies activity/location/time tracking and actual travel. The pinned [Body Equipment Playtest](evidence/2026-11-05-site-aware-repair/sources/BODY_EQUIPMENT_PLAYTEST.md) supplies separate body-use and equipment-access context; it does not supply repair price or labor. The repair rules remain unchanged.

The previous repair fixture treated `(3,3)` as a hidden constant. `SharedRepairFixture` now supplies a work-site coordinate, and the fixture fingerprint includes non-default coordinates. `RepairAccess` compares the worker's actual `ActorState` position to that site while retaining the existing training, tool, target, materials, station, hands, capability, condition, combat and work-window checks. The original `(3,3)` layout keeps its earlier fingerprint and save meaning.

The site at `(1,3)` in the new regression is a synthetic layout choice. It does not add a general grid, route planner, new range rule, assignment entitlement or production location. Travel still uses the existing explicit cardinal `WorldTraversalRecord` path and shared clock. Reaching the work site does not start repair automatically; the existing explicit repair command is still required. Repair's own job and reservation records remain authoritative.

## Verification

`tool_repair_site_access_uses_world_position_and_partial_travel_restore` checks that a remote repair start rejects without mutation, that the worker travels by two real steps, that a partial step and elapsed time survive snapshot restore, and that repair starts only after the worker reaches the authored position. The complete deterministic suite passes **1,102/1,102**; Core, Persistence and LabModel compile under C# 9 with warnings as errors; static package checks pass **14/14**. Exact code, source and result hashes are in the [site-aware repair evidence](evidence/2026-11-05-site-aware-repair/README.md).

**Source-scope correction:** the older checkpoint's binding manifest described `BODY_EQUIPMENT_PLAYTEST.md` too broadly as supplying the repair procedure. The repair requirements are in Expedition Player Book FL-18. The historical manifest and its validator receipt are kept unchanged; the corrected binding scope is in the [schema39 assignment checkpoint](evidence/2026-11-05-expedition-assignments/SOURCE_BINDINGS.json).

## Still open

At this checkpoint, no persisted assignment intent or readiness record existed. The later [schema39 assignment checkpoint](evidence/2026-11-05-expedition-assignments/README.md) adds a bounded persisted dispatcher for this repair and existing Trap retrieval while retaining their procedure-specific admission checks. A general work-site directory, lead/assistant plan, assistant assignment, autonomous travel, concurrent movement and production site authority remain open.
