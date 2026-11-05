# Tactical framework and AI reference study

**Reviewed:** 2026-11-04  
**Purpose:** Identify where Decennium can reuse established tactical-game tooling without replacing its source-driven, shared C# rules simulation.

## Recommendation

Keep the existing C# simulation as the sole authority for rules, time, inventory, character state, persistence, and command outcomes. The game needs its own integration of Exploration, Tactical Combat, and Resource Management; none of the inspected tactical frameworks covers that shared rules scope.

The **Turn-Based Strategy Framework (TBSF)** is the strongest candidate to evaluate later for Unity-side grid authoring, path/target presentation, and tactical UI. Do not make it authoritative for Decennium's combat turns, character values, action costs, or outcomes. Its default model is player turns over sets of units; Decennium already has per-actor initiative and a six-second round schedule. A custom adapter and turn resolver may bridge that difference, but that fit has not been proven.

Do not add any of these frameworks to the C# rules project now. EmblemForge and the tutorial battle system are learning examples, not suitable engine foundations. Turnable is an unfinished general C# library without an evident reuse license. Game AI Pro is a source of design techniques, not a software dependency.

## Reference comparison

| Reference | What it offers | Fit for Decennium | Decision |
| --- | --- | --- | --- |
| [TBSF Unity documentation](https://github.com/mzetkowski/tbsf-unity-docs) | Grid scene/editor tooling; square and hex cells; pathfinding; turn resolution; ability selection and highlighting; behavior-tree AI; optional multiplayer. The docs describe a Unity package distributed through the Asset Store and a shared core plus Unity-specific layer. | Best potential time-saver for Unity presentation and board tooling. The default subsequent-player turn resolver, Unity `Unit` objects, ability interaction flow, and peer-to-peer synchronization are not a drop-in match for Decennium's C# command, clock, and persistence model. The actual framework package was not inspected, and its current licensing, price, API compatibility, and source quality still need review. | Candidate for a bounded compatibility spike during Unity integration. Keep rules/results in the shared C# core. Do not purchase or adopt on documentation alone. |
| [EmblemForge](https://github.com/DallenLarson/EmblemForge) | Small Unity tactical-grid sample with unit data, grid creation, tile selection/highlighting, and player/enemy turn flow. The repository is MIT-licensed. | Its README describes a framework, but the inspected scripts are a simple prototype: a global singleton, scene-wide object searches, radius-based movement, and UI/turn logic coupled to `MonoBehaviour` scripts. | Useful only as a small learning sample. Do not base Decennium's tactical layer on it. |
| [Turnable](https://github.com/angyan/Turnable) | Unity/Godot-compatible C# project with immutable record-based character/stat and map primitives, pathfinding, timekeeping, and a test project. Its README says development has restarted. | Pure C# modules are conceptually close to the engine boundary, but the project is unfinished: its planner `Action.Do`/`Undo` throw `NotImplementedException`, its inspected graph path cost is uniform, and its `.NET 6` project includes a machine-specific output-copy target. No license file was present in the inspected repository root. | Study its small abstractions and tests. Do not depend on or copy code without a clear license and a maturity review. |
| [Unity Tactical RPG Battle System](https://github.com/colinbellino/unity-tactical-rpg-battle-system) | Educational Unity prototype with an explicit battle state machine, turn-order controller, actor/ability/effect components, and tactical UI. | The README calls it a bare-bones project built while following a tutorial and says it was tested on Unity 2021.3.3f1. It is archived. The inspected combat objects are Unity `MonoBehaviour` components, so they would couple rules to the presentation layer. No license file was present in the inspected repository root. | Read for examples of battle-state flow and effect composition only. Do not incorporate its code. |
| [Game AI Pro](https://www.gameaipro.com/) | Free online chapters by game-AI practitioners; not a runtime framework. | Useful for AI planning, simulation, pathfinding, debugging, and testing ideas. The chapters do not replace the project's domain rules or command model. | Use selected chapters as design references and record applicable techniques; do not implement their unrelated systems wholesale. |

## What is applicable

### Grid and tactical presentation

TBSF documents a useful separation between cell/unit state, grid control, turn resolution, ability targeting, and highlighters. Its square/hex topology, weighted movement, reachable-cell/path presentation, and editor brushes are the strongest opportunities to reuse. Decennium's simulation should provide canonical positions and the result of a movement/action query; a Unity-side adapter can translate those into cells, highlights, animations, and input. A click or UI selection must still submit a normal Decennium command rather than mutate a TBSF unit as a second source of truth.

TBSF's default turn resolver advances among players and their unit collections. Decennium's accepted prototype instead places individual actors in equal initiative slots inside a six-second round. TBSF documents a custom resolver extension point, but the fit needs a small integration spike against that exact schedule before adoption. Keep the grid topology configurable until the project explicitly settles square versus hex cells.

### AI and authored behavior

The Game AI Pro chapter on *Gears Tactics* describes planning actions against a simulated `WorldState`, applying each chosen action to that planning state, then executing a presentation plan while preserving the actor's action order. It also emphasizes that visual clarity constrains how actions are grouped. This is a good future pattern for enemy planning and animated turn presentation: query or clone the authoritative C# state for planning, then commit validated commands through the same shared simulation.

The *Days Gone* squad-coordination chapter separates group goals and role assignment from each actor's behavior, allowing an actor to override an assigned role when a higher-priority situation demands it. This may help later with companion AI and coordinated enemies. It is an AI design technique, not a requirement to add a large behavior framework before the simulation and player-facing tactical loop need one.

The *Template Tricks for Data-Driven Behavior Trees* chapter favors a simple declarative representation and contained factories over an overbuilt generic parser. For Decennium, the safer boundary is to keep rule procedures and validation in C#, with data assets describing authored content and AI behavior only where the content has become stable. Avoid introducing a second general-purpose rules language.

### Shared time and long-lived jobs

The *Efficient, Event-Based Simulations* chapter recommends scheduling sparse time-based work by deadline rather than polling every object every frame. Decennium already has a shared simulation clock and sparse activity calendar for long jobs. Continue that model for crop growth, freshness deadlines, companion assignments, and other delayed effects; use a deadline queue only if profiling or design complexity warrants it. Preserve deterministic event ordering, cancellation identity, save/replay behavior, and pause semantics.

The *Planning Movement on Player-Modifiable Maps* chapter shows that route search can grow rapidly when movement planning also changes the map. It supports bounding or pruning searches if Decennium later adds tactical map modification. It does not justify a custom pathfinding algorithm before the selected map rules require one.

## Explicit non-goals for this study

- No framework was installed, bought, imported, or copied into the repository.
- No turn-order, grid-topology, or AI design rule was changed by reading these references.
- No claim is made that TBSF is compatible with the current Unity Editor or the existing C# package. Its package and licensing need direct evaluation first.
- No tests were added or run for this research pass.

## Sources inspected

- [EmblemForge README](https://github.com/DallenLarson/EmblemForge/blob/main/README.md), [GameManager.cs](https://github.com/DallenLarson/EmblemForge/blob/main/Assets/Scripts/GameManager.cs), [GridManager.cs](https://github.com/DallenLarson/EmblemForge/blob/main/Assets/Scripts/GridManager.cs), [Tile.cs](https://github.com/DallenLarson/EmblemForge/blob/main/Assets/Scripts/Tile.cs), [UnitController.cs](https://github.com/DallenLarson/EmblemForge/blob/main/Assets/Scripts/UnitController.cs), [MIT license](https://github.com/DallenLarson/EmblemForge/blob/main/LICENSE).
- [TBSF Unity documentation](https://github.com/mzetkowski/tbsf-unity-docs/blob/master/README.md), including its project structure, cell/unit customization, ability system, AI, turn resolver, and networking sections. The framework itself is distributed through the Unity Asset Store, which the docs link as its installation path.
- [Turnable README](https://github.com/angyan/Turnable/blob/dev/README.md), [`Stat`](https://github.com/angyan/Turnable/blob/dev/Source/Characters/Stat.cs), [`Stage`](https://github.com/angyan/Turnable/blob/dev/Source/Places/Stage.cs), [`Graph`](https://github.com/angyan/Turnable/blob/dev/Source/AI/Pathfinding/Graph.cs), [`Action`](https://github.com/angyan/Turnable/blob/dev/Source/AI/Planning/Action.cs), and [project file](https://github.com/angyan/Turnable/blob/dev/Source/Turnable.csproj).
- [Unity Tactical RPG Battle System README](https://github.com/colinbellino/unity-tactical-rpg-battle-system/blob/main/README.md), [`BattleController`](https://github.com/colinbellino/unity-tactical-rpg-battle-system/blob/main/Assets/Scripts/Tactical/Battle/Controller/BattleController.cs), [`TurnOrderController`](https://github.com/colinbellino/unity-tactical-rpg-battle-system/blob/main/Assets/Scripts/Tactical/Battle/Controller/TurnOrderController.cs), and [`Ability`](https://github.com/colinbellino/unity-tactical-rpg-battle-system/blob/main/Assets/Scripts/Tactical/Actor/Component/Ability/Ability.cs). GitHub marks the repository archived.
- [Game AI Pro online edition](https://www.gameaipro.com/), especially [Automated AI Testing](https://www.gameaipro.com/GameAIProOnlineEdition2021/GameAIProOnlineEdition2021_Chapter01_Automated_AI_Testing_Simple_tests_will_save_you_time.pdf), [Efficient, Event-Based Simulations](https://www.gameaipro.com/GameAIProOnlineEdition2021/GameAIProOnlineEdition2021_Chapter02_Efficient_Event_Based_Simulations.pdf), [Gearing the Tactics Genre: Simultaneous AI Actions in Gears Tactics](https://www.gameaipro.com/GameAIProOnlineEdition2021/GameAIProOnlineEdition2021_Chapter03_Gearing_the_Tactics_Genre_Simultaneous_AI_Actions_in_Gears_Tactics.pdf), [Squad Coordination in Days Gone](https://www.gameaipro.com/GameAIProOnlineEdition2021/GameAIProOnlineEdition2021_Chapter12_Squad_Coordination_in_Days_Gone.pdf), [Template Tricks for Data-Driven Behavior Trees](https://www.gameaipro.com/GameAIProOnlineEdition2021/GameAIProOnlineEdition2021_Chapter13_Template_Tricks_for_Data-Driven_Behavior_Trees.pdf), and [Planning Movement on Player-Modifiable Maps](https://www.gameaipro.com/GameAIProOnlineEdition2021/GameAIProOnlineEdition2021_Chapter14_Planning_Movement_on_Player-Modifiable_Maps.pdf).
