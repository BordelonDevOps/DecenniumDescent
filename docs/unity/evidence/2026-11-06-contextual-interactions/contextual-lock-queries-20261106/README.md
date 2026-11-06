# Contextual cache and receptacle queries — 2026-11-06

## Responsibility and boundary

This increment connects existing authored TEST_ONLY supply-cache and ordinary-receptacle lock commands to the shared read-only command query and discovery surface. Query and resolution reuse the same preflight decisions, and discovery only offers reachable interactions supported by the existing physical credentials and records. No schema, rule, timing, RNG, save or replay format was added.

Authoritative state remains in `SupplyCacheRecord` / `SupplyCacheAttemptRecord` for supply caches, and `OrdinaryReceptacleLockRecord` / `OrdinaryReceptacleAttemptRecord` for receptacles. The linked `PortableEquipmentRecord` owns container state, physical credential, custody and access facts. Existing host-derived inventory authority, capability checks, available hands, Action intervals, `WorkLedger`, `RuleClock`, RNG, command receipts and `SnapshotCodec` own authorization, costs, staged attempts, deterministic resolution, idempotency and persistence.

The acceptance uses the bounded authored fixtures. It verifies cache and receptacle query support/admissibility and existing costs without mutating serialized snapshot bytes, discovers available key/tools actions, executes the existing pick operation, advances shared time, discovers and queries interruption without mutation, then executes interruption through the existing resolver. Tactical options are exposed only to the active actor. This does not provide arbitrary production object authoring, examination, digging, marking, route discovery or excavation.

## Failure diagnosis

The first test-first run showed that a supported cache pick command could not be queried: the shared dispatcher sent non-receptacle `Interact` commands to `QueryFishingTrapControl`, which returned `UnsupportedOperation`. The supply-cache resolver already supported the interaction, but its query and discovery routes were missing.

After adding a pure cache assessment and routing, compilation first failed because `IEnumerable<Command>` lacked `System.Collections.Generic`. The next compile failed with `CS1628`: the preflight LINQ predicate captured its `out SupplyCacheRecord cache` parameter. Adding the import and copying the cache ID to a local removed those compile errors.

The acceptance then failed with `SupplyCacheOutOfReach`. Inspection of the fixture showed the actor began outside the cache's authored reach; the test had omitted the existing `SupplyApproach` setup. Adding that setup fixed the fixture. No gameplay range rule or resolver behavior was changed to make the test pass. All failed and corrected reports are retained in the `FAILED_*_RESULTS.json` files.

## Validation

- Focused contextual query/discovery acceptance: **PASS 1/1**, [`FOCUSED_RESULTS.json`](FOCUSED_RESULTS.json).
- Full C# 9 warnings-as-errors suite: **PASS 1,178/1,178**, zero failures, [`HEADLESS_RESULTS.json`](HEADLESS_RESULTS.json).
- Static package validation: **PASS 18/18 checks; 237 assets; 237 unique GUIDs**, [`PACKAGE_RESULTS.json`](PACKAGE_RESULTS.json). This validator checks package structure and pinned manifests.
- [`SOURCE_BINDINGS.json`](SOURCE_BINDINGS.json) records the exact changed source hashes and report paths.

This TEST_ONLY query/discovery increment is one part of EXP-03; the exploration system and full engine remain incomplete.
