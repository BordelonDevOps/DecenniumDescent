# External engine and tactics reuse review

**Reviewed:** 2026-11-05  
**Purpose:** Apply the owner's instruction to reuse suitable existing systems rather than build an engine from scratch. This is an architectural review, not a dependency approval or code import.

## Findings

| Reference | What it provides | Fit for Decennium | Decision |
| --- | --- | --- | --- |
| [Emblem Forge](https://github.com/DallenLarson/EmblemForge) | A Unity C# tactics project organized around `GameManager`, `Unit`, `Tile`, and `GridManager`. Its repository declares MIT licensing. | A useful small example of separating board, unit, and turn responsibilities. Its Unity-bound manager/unit loop does not supply Decennium's shared clock, source-authored Actions, persistent command receipts, three gameplay layers, or existing combat rules. | Keep as a reference. Reuse a narrow utility only after checking its exact code and retaining the MIT notice. Do not transplant its game loop. |
| [TBS Framework Unity documentation](https://github.com/mzetkowski/tbsf-unity-docs) | Documentation for a turn-based framework with square/hex grids, units, movement, abilities, AI, turn management, and multiplayer. It describes a shared `tbsf-common` core with engine-specific Unity scripts and includes an in-memory cell plus Tilemap adapter pattern. Its installation path points to the Unity Asset Store. | The common-core/host-adapter boundary fits the C#-first plan. The framework's AP/MP unit model, turn resolver, and game-state ownership would overlap with Decennium's canonical action, movement, and schedule ledgers. The documentation repository is not the framework source package. | Adopt the architectural lesson: keep rules engine independent and bind Unity as a host. Reassess a specific grid or authoring component later; do not replace the simulation or assume the asset is available under an open-source license. |
| [Turnable](https://github.com/angyan/Turnable) | An engine-portable C# turn-based framework repository with source and tests. Its README lists pathfinding, line of sight, AI approaches, stats, and inventory as planned framework capabilities and says development has restarted. | Portable C# is directionally compatible, but its own README describes an unfinished framework. No root `LICENSE` file was found at the inspected default-branch path, and no stable package/release was identified in the repository view. | Do not adopt as a dependency. Revisit only if a concrete missing algorithm appears, then verify implementation maturity, license, tests, and integration boundary first. |
| [Unity tactical RPG battle-system tutorial](https://github.com/colinbellino/unity-tactical-rpg-battle-system) | A Unity learning prototype based on a tutorial, with sample data parsing and scene setup. The GitHub repository is archived. | Helpful for learning/editor workflow; it is a starter battle scene rather than a rules engine. Its Unity scene architecture is outside the current phase. | Reference only; not a production dependency. |
| [Game AI Pro](https://www.gameaipro.com/) | Free-to-read chapters covering modular AI, event-based updates, AI testing, movement, and tactics. The site notes that chapter copyrights remain with their authors/publisher. | The strongest source here for transferable engineering patterns rather than a drop-in combat framework. Event scheduling matches the engine's existing deterministic clock approach; modular behaviors and focused two-actor tests are useful for a later companion/enemy AI layer. | Apply the patterns when implementing AI and runtime tooling. Do not redistribute chapter text or copy large code excerpts. |

## Reuse decision

Keep the current authority path: headless C# owns commands, validation, world state, scheduling, random outcomes, persistence, and replay. A future Unity host should submit those commands and present the same resolved state. Do not add another turn resolver, action-point economy, unit-health model, or independent inventory ledger from a tactical framework.

This does not rule out a dependency for a clearly missing, isolated capability such as grid authoring or a verified pathfinding primitive. Before adding one, compare its license, Unity/package requirements, supported grid and movement semantics, deterministic behavior, maintenance status, test surface, and data-ownership boundary against the existing implementation. Do not buy an Asset Store product or import Unity code during the C#-first phase.

## Source notes

- Emblem Forge README describes the four Unity components above; its repository includes a root MIT license.
- TBSF's documentation describes both the Asset Store installation and the shared-core / engine-adapter layout, including a virtual-cell Tilemap example.
- Turnable's default-branch README describes a Unity/Godot-compatible C# framework and future AI/pathfinding features; the inspected repository root did not expose a `LICENSE` file or release package.
- The tactical battle prototype's README calls it a bare-bones learning project and the repository is archived.
- The Game AI Pro review focused on *Efficient, Event-Based Simulations* (2021), *Automated AI Testing* (2021), and *Modular AI* (2017). These discuss event-queued updates, small reproducible tests, and reusable behavior modules with explicit interfaces.
