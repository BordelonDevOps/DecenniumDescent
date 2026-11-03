# Decennium foundation laboratory

**Development branch: [`Engine`](https://github.com/BordelonDevOps/DecenniumDescent/tree/Engine).** The owner requested a dedicated branch from `main` for all engine work. Source code, tests, Unity host source/settings and the related `docs/unity/` records belong on this branch. Generated caches, user settings and temporary build output remain ignored. The branch retains the rules repository inherited from `main`; no rules-source promotion is implied.

Technical foundation plus source-bound C# character, damage/life, combat-budget, duration and dice procedures. Shared worker/resource reservations now join the existing transaction and save path in an explicit schema2 technical fixture. Owner-approved prototype clock/traversal arithmetic is available; the adopted Camp Greens lifecycle now runs through schema3 commands and saves. General job/worker access and spatial execution remain unfinished. **Current owner direction: develop the complete engine in plain C# across exploration, tactical combat and resource management first; integrate with Unity afterward.** The full engine is incomplete. Current counts, source bindings and review findings are in the [handoff](../docs/unity/DEVELOPMENT_HANDOFF.md) and [current evidence](../docs/unity/evidence/2026-11-03-carrying/SOURCE_BINDINGS.json). Unity package import, scenes, Play Mode and builds remain deferred.

Unity **6000.3.28f1 LTS** is installed at `C:\Program Files\Unity\Hub\Editor\6000.3.28f1\Editor\Unity.exe`. After owner license activation, template creation at `UnityLaboratory/` completed with exit 0. This is environment preparation only: the foundation package has not been imported, and no Decennium scene has been generated. The earlier license failure is retained in [historical environment evidence](../docs/unity/evidence/2026-11-03-rolls/UNITY_ENVIRONMENT.json); the successful attempt is recorded in `engine/artifacts/unity-qualification-20261103T174953/01-create.json` and its adjacent log. Preserve this unused template while C# work continues.

Read [the handoff](../docs/unity/DEVELOPMENT_HANDOFF.md), [design and architecture boundaries](../docs/unity/UNITY_ENGINE_PLAN.md), and [requirements trace](../docs/unity/IMPLEMENTATION_TRACE.md). Unity is settled; production design choices remain under evaluation.

The [current conversion map](../docs/unity/IMPLEMENTATION_TRACE.md) accounts for all75 source areas and49 work items at pinned source revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Current partial statuses are in the human trace; frozen JSON remains historical. Consult [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206) for product/source guidance, then the owner if both remain stuck. The next integration target is the owner-adopted ordinary handling, portioning and self-consumption profile, using explicit versioned inventory records and the persisted crop lifecycle.

`Laboratory/Model/PlaytestCharacters.cs` supplies ability modifiers, total-level proficiency, chronological base maximum HP and capacity-only clamping. It binds all 17 class Hit Dice, accepts recorded rolls or an explicitly chosen fixed average, and returns immutable calculation details. Hit Dice counts describe attained levels, not currently unspent dice. HP effects, character commands, grants and save integration remain separate work. The kernel accepts `int` ability scores and uses `long` HP totals/current values to prevent overflow; arithmetic support does not establish character-generation legality.

For example, `BaseMaximumHp(new[] { new CharacterLevelRecord("Bard", 8), new CharacterLevelRecord("Bard", 5) }, 14)` returns base maximum 17. `ClampAfterCapacityChange(6, 17)` returns 6: a larger maximum does not heal. Call these static methods on `PlaytestCharacters` in the opt-in headless model. The ordinary test command below exercises the same implementation.

The owner selected **turn-based combat for the first prototype**. The first playable milestone must connect direct exploration, a tactical encounter and resource management through shared state. `Laboratory/Model/PlaytestRolls.cs` currently resolves declared attacks, task checks, ordinary saves and opposed checks only. It takes already-selected d20 results; it neither authorizes actions nor consumes RNG or applies effects. The exact provisional sources and independent expected examples are bound in [SOURCE_BINDINGS.json](../docs/unity/evidence/2026-11-03-rolls/SOURCE_BINDINGS.json). Its `int` inputs produce `long` totals/margins to avoid overflow; unsupported Python integers outside the C# input range are not accepted by this API. The legacy fixture retains schema1 and its existing behavior; a separately selected schema2 work fixture is described below.

## Run the checks available now

From the repository root, in a fresh PowerShell 7 process:

```powershell
pwsh -NoProfile -File engine/tools/Test-Foundation.ps1
pwsh -NoProfile -File engine/tools/Validate-Package.ps1
pwsh -NoProfile -File engine/tools/Validate-RuleBindings.ps1
```

The first compiles the same Core, Persistence, LabModel and regression sources into separate assemblies using PowerShell's bundled Roslyn and reference assemblies. It needs no downloaded SDK, Unity installation or network. It uses C#9 and treats warnings as errors; this is not a Unity compatibility test. The second checks package structure, GUID pairing and assembly boundaries. The third validates retained source bytes, all17 profile/340 RP cells, bound named cases and recorded tested-code hashes. Commands return nonzero on failure and retain JSON under ignored `engine/artifacts/`. Do not reuse a loaded PowerShell process after editing assemblies.

## Future Unity integration (deferred during the C# phase)

1. When Unity integration becomes the active phase, reuse the existing 6000.3.28f1 template project. The package's `unity: 6000.0` remains a minimum API declaration. Record actual project packages, target and scripting backend. The template's URP/2D renderer is a laboratory choice pending the game's visual evaluation; successful template creation does not validate the foundation package.
2. Use Package Manager's **Install package from disk** and select `engine/com.decennium.foundation/package.json`. Keep this repository location stable. Record the resulting project manifest and lock file; do not overwrite an existing project manifest. [Unity local package instructions](https://docs.unity3d.com/6000.0/Documentation/Manual/upm-ui-local.html).
3. Use **Decennium > TEST_ONLY > Enable laboratory for active target**. Wait for compilation. This adds only `DECENNIUM_TEST_ONLY` to the active target's existing defines.
4. Use **Decennium > TEST_ONLY > Create or open foundation laboratory**. The builder creates `Assets/DecenniumTestOnly/FoundationLab.unity` and `LaboratoryPanel.asset`. Running it again opens the existing scene without rewriting it. It asks Unity to handle unsaved scenes before switching. It does not add scenes to a build profile.
5. For tests, install/resolve an Editor-compatible Unity Test Framework in the host project and merge `"com.decennium.foundation"` into the project manifest's `testables` array. Do not guess a package version or replace other dependencies. Run Edit Mode `Decennium.Foundation.Tests.UnityFoundationTests`; expect the current shared suite count from the handoff, not zero. Preserve XML and Editor logs. [Unity package test discovery](https://docs.unity3d.com/6000.0/Documentation/Manual/cus-tests.html).
6. Enter Play Mode and perform the smoke sequence below. Record actual observations and new Console messages, including failures. These steps have **not** been executed in Unity here.

The package has seven asmdefs. Core and Persistence enforce No Engine References. Laboratory code requires the explicit define plus Editor or Development Build. Editor tooling and NUnit bridge are editor-only. New assets include `.meta` GUIDs; the USS metadata deliberately leaves importer-specific settings for the first real Unity import. Preserve GUIDs when that occurs.

## Scene and controls

Expected generated scene: `Assets/DecenniumTestOnly/FoundationLab.unity`.

Use the on-screen UI Toolkit **buttons with a mouse**. There are no keyboard, gamepad or production direct-control input maps yet.

| Control | Expected laboratory result |
| --- | --- |
| Left / Up / Down / Right | One abstract orthogonal step for the blue actor; walls and the orange companion block movement. |
| Open TEST_ONLY container | At the starting location, opens the adjacent gold square and transfers exactly one synthetic token. A second attempt rejects without changing state. |
| Advance one TEST_ONLY tick | Advances the integer fixture clock by one. Movement and interaction do not advance it. |
| Save fixture / Load fixture | Saves or restores snapshot, revision, receipts, clock and RNG state. |
| Recover primary from backup | Explicitly restores `.bak` after validation, retains `.bak`, and preserves the displaced primary as `.recovery-evidence-<id>`. Successful recovery allows saving again. |
| Start new TEST_ONLY fixture | Resets memory only. It does not delete or repair a disk save; Save remains blocked if the primary is corrupt. |

Blue is the actor; orange is the companion; gold is the container; gray is a wall. These squares are generated from Unity's white texture, with no imported game art.

Suggested smoke sequence: at startup open container, open again, attempt Right into the wall, move Left, advance a tick, Save, move again, Load, then leave/re-enter Play Mode. Verify expected rejection, position/state restoration, one token, and no duplicate UI/view objects. Disable/re-enable the laboratory component and reload the scene; inspect Console before and after. Test recovery using copies of laboratory saves only and record the preserved evidence path. Check UI readability at 1280x720 and resizing; visual correctness is currently unverified.

## Persistence limits

The laboratory saves to `Application.persistentDataPath/DecenniumTestOnly/foundation.ddsave`; UI diagnostics show the actual path. The previous successful snapshot is `.bak`. The first save has no backup. Loading a corrupt primary reports a failure, never silently resets or selects a backup.

The original Unity fixture retains schema1, content fingerprint `TEST_ONLY.lab-v1` and RNG identifier `xorshift32-v1`. The headless `TestOnlyWorkPolicy.Initial()` explicitly selects schema2 and `TEST_ONLY.work-session-v1`, with exact `RuleClock`, immutable work ledger and the versioned dice mapping. Its legacy tick field must stay zero. Schema1 golden bytes are preserved; no clock conversion or migration occurs. The same codec/store handles either format and refuses to overwrite a different schema/content/scope. Use a distinct save path for each fixture. Both have SHA-256 corruption detection, bounded fields and a maximum size of1MiB; schema2 allows at most256 records in each ledger collection as a technical bound. These are incomplete game-state models. Writes flush a sibling temporary file, decode it, then use same-volume replacement. This was exercised on this Windows host. Checksums are not authentication; filesystem crash durability, other platforms and hostile-save security have not been certified. The store requires one writer and a stable local path. No old browser-save migration or production save compatibility is promised.

Command receipts are scoped by trusted principal and command ID, persisted with state, and bounded at 1,024. On reaching capacity the lab fails closed until an explicitly new fixture; it does not evict receipts and risk awarding twice. The current implementation copies bounded snapshots for transactions and is not a production performance claim.

## Quantity and carrying C# helpers

`RuleQuantity` preserves exact nonnegative rational amounts without implicit units or rounding. `PlaytestCarrying` implements the reviewed provisional size/Strength table, independent pounds and Load, Burden/push-drag speed arithmetic and body/casualty weights. Known overload rejects; an unknown measure never becomes zero. Load-derived hauling pounds are labeled estimates and cannot supply documented physical mass.

`BurdenItem` records the exact contents covered by each inclusive quantity independently. Nested containers count each physical object once per unit. The bounded helper accepts up to256 objects; cross-unit fallback is atomic only. If an inclusive aggregate lacks the other unit, that unresolved total remains unknown. Partial overlap requiring empty-item decomposition rejects; documented whole-root totals may still cover consistent crossing child aggregates. These are numeric helpers, not an inventory owner, transformation system or permission to move/consume goods.

## Camp Greens C# prototype

`TestOnlyCropPolicy.Initial()` explicitly selects schema3 and a distinct fingerprint. `CampGreens` executes the approved one-hour planting,15-minute tending, seven days of suitable/cared growth and one-hour harvest procedure. Seed/water spend once, interrupted active work retains progress, passive growth releases the worker, and advances stop at the earliest crop milestone. Exact maturity, neglect, harvest and freshness boundaries follow [owner decisions](../docs/unity/PROTOTYPE_RULE_DECISIONS.md).

The bounded host supplies one prepared10x10-foot plot, a capable companion and compatible tools. Production acquisition, routes, seasons, carrying, food use and autonomous assignments are not supplied. Use its trusted host grant for crop commands and condition changes; the command payload cannot grant world authority. Save schema3 to its own path. History bounds are8 crops/plots/foods,32 tasks per crop and128 ledger records per collection, with no silent eviction or migration. The shared test suite exercises this host headlessly; the existing Unity scene still runs the original schema1 fixture.

## Release exclusion

For a non-development build, remove `DECENNIUM_TEST_ONLY` from that target and exclude all laboratory scenes from its build profile. The unconditional Editor gate rejects a release build retaining that define or a `DecenniumTestOnly` scene / `TEST_ONLY` root. The laboratory asmdefs and source guards exclude fixture implementation from release compilation; the core also rejects TEST_ONLY snapshots in Release profile.

The guards exist and the core rejection is tested headlessly. **Actual development/release builds, stripping and scene exclusion have not been exercised.** Before any release claim, verify both a rejected contaminated build and a clean build with no laboratory assembly/content. This package is not release content approval.
