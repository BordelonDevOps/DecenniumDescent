# Planar combat constraint review

2026-11-03. The separate `/root/source_review` agent read PlanarCombatGeometry.cs and thirteen geometry regressions against COMBAT_ACTION_PLAYTEST §§Movement and geometry; Cover, sight, Hide and Search, with the existing Python best_cover/ranged_range reference.

No actionable findings. Equal five-foot orthogonal/diagonal distance, complete two-side corner blocking, strongest-only cover, inclusive range endpoints and close-hostile sight/incapacity constraints match the cited scope. Widened subtraction and multiplication cover every int coordinate without overflow.

The reviewer verified all63 compiled hashes against `run-20261103T235228801Z-bf15cea8/results.json` (516/516 PASS). It did not edit files or rerun the full suite. The parent ran the shared suite, package/source-binding checks and persisted-output parity.

The helpers deliberately do not establish actual visibility, line of effect, traversability, body volumes or complete attack legality. They do not reinterpret synthetic world coordinates or implement an authoritative attack command. No new rule, Unity qualification or release approval is claimed.
