# Tactical framework reuse review — 2026-11-04

## Decision

Do not add an external runtime dependency to the current plain C# rules-engine phase. Keep Decennium's source-bound rules, authoritative state, deterministic resolution, persistence, and command validation in its existing C# core. Reuse third-party tooling when it removes real Unity presentation or authoring work and its license, runtime behavior, and compatibility have been verified.

The reviewed projects do not provide a drop-in replacement for the project's source-bound rules or its shared exploration, tactical combat, and resource-management simulation. This is a scoped decision, not a claim that every framework has been exhaustively compared.

## References

| Reference | Useful material | Fit and decision |
| --- | --- | --- |
| [EmblemForge](https://github.com/DallenLarson/EmblemForge) | Small Unity tactics project; useful to inspect scene and presentation patterns. | MIT-licensed, but its sample manager mixes UI, turns, and gameplay mutation. Keep as a reference; do not use it as the authoritative rules core. |
| [TBSF Unity documentation](https://github.com/mzetkowski/tbsf-unity-docs) | Grid, targeting, ability, and behavior-tree concepts for a Unity tactics framework. | This repository contains documentation rather than the runtime package. Consider its Unity-side features later only after reviewing the actual package, license terms, and turn model. Do not purchase or integrate it as part of the C# phase. |
| [Turnable](https://github.com/angyan/Turnable) | Standalone .NET tactical simulation, tests, state, scheduling, and pathfinding concepts. | Closest architectural reference, but the repository has no root license file and its Release project contains a machine-specific path. Do not import or depend on it without resolving licensing and build portability. |
| [Unity Tactical RPG Battle System](https://github.com/colinbellino/unity-tactical-rpg-battle-system) | Minimal Unity encounter and interaction example. | The project describes itself as a barebones learning prototype and is archived. Useful only as a small interaction reference; not a foundation. |
| [Game AI Pro](http://www.gameaipro.com/) | Articles and implementation patterns for game AI. | A reading resource, not a runtime framework. Apply relevant patterns when a real AI need exists; keep AI decisions separate from authoritative simulation and RNG. |

## Reuse criteria for later Unity work

Before adopting a library or package, verify its actual license, Unity/C# target compatibility, maintenance state, ability to submit normal Decennium commands, and whether it duplicates a source-bound rule. Prefer packages for editor workflow, grid visualization, input, navigation, and presentation where they remain outside authoritative rule resolution. Keep framework turn defaults from silently replacing Decennium's calendar, initiative, reaction, or shared-clock rules.

This review does not authorize a purchase, import, license change, or production rule selection. The current technical query layer uses no external package and adds no saved schema or gameplay rule.
