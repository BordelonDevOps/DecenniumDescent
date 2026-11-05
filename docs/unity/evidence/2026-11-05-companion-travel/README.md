# Off-calendar companion traversal checkpoint

This TEST_ONLY increment lets one authored companion walk toward an existing work site on the shared world clock while remaining outside tactical initiative. It reuses the existing ActorState, WorldTraversalRecord, traversal codec and snapshot path; it adds no persisted fields or schema version.

The full headless regression verifies that running remains rejected without a paid off-calendar Dash budget, incompatible work blocks travel, a partial route position survives save/restore, travel and work cannot overlap for this actor, and the companion does not gain a tactical turn. The existing unattended Trap integration also sends a capable second worker to retrieve the same physical catch after saving mid-route.

- [Source bindings](SOURCE_BINDINGS.json)
- [Movement decision record](../../EXPLORATION_MOVEMENT_RULE_DECISIONS.md)
- [Full headless suite](HEADLESS_RESULTS.json)
- [C# compile](COMPILE_RESULTS.json)
- [Static package checks](PACKAGE_RESULTS.json)
- [Source-binding validation](RULE_BINDINGS_VALIDATION.json)

This does not implement general expedition assignments, autonomous route selection, concurrent companion movement, production gameplay authority, or Unity integration. Broader engine work remains active.
