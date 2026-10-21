# Decennium Descent — Unity Development Directions for Codex

**Purpose:** Execution brief for the Unity game framework and its continuing AI-assisted engineering review.
**Prepared:** October 20, 2026.
**Status:** Proposed development instructions. Supplying this brief as an execution task authorizes its bounded first assignment, not new gameplay canon or release promotion.

## 1. Mission and first-run scope

Develop Decennium Descent as an SNES-style CRPG in Unity. Implement one persistent game simulation with three connected experiences: direct-control exploration, tactical party combat, and expedition resource management.

Work as the implementation agent and ongoing engineering assistant. Do not merely provide advice or create a large collection of unconnected scripts. Produce small, runnable increments, investigate failures, maintain regression tests, and preserve evidence that the next development session can use.

**First assignment: complete Stage 0, then the smallest safe Stage 1 increment.** If an existing foundation already satisfies Stage 1, verify and extend it rather than replace it. Later stages are a roadmap, not authorization to build everything in one run. Do not stop at a planning document when a bounded implementation is possible. When execution is blocked by missing tools or authority, complete the independent work, document the exact blocker, and report unexecuted checks honestly.

The owner determines game intent and approves consequential design changes. Do not require the owner to independently audit every implementation detail. Supply understandable decisions, reproducible examples, and verification evidence instead.

## 2. Product direction and boundaries

### Established direction

- Unity and C#; SNES-style visual presentation rather than an initial full-3D MMO.
- Exploration with direct movement, running, jumping, and mapped/contextual interactions such as examining, digging, marking, opening doors, and opening containers.
- Tactical CRPG depth inspired by the owner's Owlcat comparison, using Decennium Descent rules rather than importing another game's mechanics.
- Resource management encompassing existing crafting and research systems and companion assignments, including the owner's examples of fishing, mining, and farming.
- Ongoing AI-assisted implementation, rules review, debugging, and maintenance.
- Video-game development; do not restore tabletop compatibility as a mandatory new delivery requirement. Preserve historical tabletop sources rather than rewriting them.
- Preserve the previously stated cooperative expedition goal: one host and up to four additional human participants. Verify the current project decision record and any existing implementation. Do not reduce that to four participants total or expand it into MMO infrastructure.

### Unresolved choices must not become hidden defaults

Turn-based combat was recommended in the preceding architecture discussion; it was not, by that recommendation alone, an owner-approved replacement for any earlier combat cadence. Locate the latest explicit decision before implementing production timing. Do not infer turn-based combat, real-time-with-pause, or support for both merely from “Owlcat.”

Likewise, verify combat grid/continuous geometry, world distance units, exploration-to-combat position conversion, jump legality, party traversal, encounter entry/exit, time conversion, pause behavior, job interruption/cancellation, and save restrictions. A visual tile does not automatically equal a combat square or a specified number of feet.

Where a choice is missing, isolate that policy and continue independent work. A developer-only manual-step harness may exercise technical plumbing, but it must be visibly labeled as a test harness, not a canonical combat mode.

Windows desktop is the initial proposed verification target, subject to any established platform decision found in the repository. Do not add console, mobile, monetization, live-service, or continuous model-service dependencies to the initial scope.

## 3. Repository and source authority

Expected local repository: `C:\Github\DecenniumDescent`.
Known repository identity: `BordelonDevOps/DecenniumDescent`.

Verify the actual workspace, branch, HEAD, dirty state, worktrees, and remotes. These identifiers do not prove that local work matches remote `main`. Do not fetch, pull, switch branches, merge, or overwrite local changes merely to make them match.

Read applicable `AGENTS.md` and `AGENTS.override.md` guidance before modifying a subtree. Keep durable agent instructions concise; store this longer brief separately and reference it. Do not overwrite existing agent guidance wholesale. Codex instruction discovery and size limits are documented in [S1].

Verified repository entry points, to re-read locally:

- `CANON_MANIFEST.md`
- `docs/canon/CANON_MANIFEST.json`
- `docs/canon/REPOSITORY_PROMOTION.md`
- The current continuity/owner-decision records and handoff discovered through those pointers.

Also inspect `DescentReviewChanges/ReviewBible/` and applicable staging/incoming material according to the registry. Locate the video-game-only directive and latest calibration handoff; report missing records rather than assuming their content.

The remote manifest pointer explicitly forbids a second parallel source of truth. The promotion policy distinguishes approved release, ReviewBible, staging, and incoming packs; ReviewBible does not automatically promote into `main`. Follow the locally verified current policy and explicit owner amendments. [R1–R2]

Do not assume that the newest filename, largest document, current branch, accepted review candidate, or passing validation suite is runtime authorization. Preserve the project's separate domain gates and exact approval vocabulary. Do not flatten authored, schema-validated, provisionally accepted, runtime-verified, balance-tested, and publication-approved statuses into “done.”

For each implemented gameplay behavior, record its stable identifier, source path and section/record, source revision/hash, applicable owner amendment, approval scope, implementation location, and test references. This is a traceability index, not a second owner of the rule text. Reuse existing registries and reports where available.

Never invent missing abilities, spells, recipes, drop rates, costs, formulas, stacking rules, durations, cooldowns, resource caps, or lore. Do not fill gaps with D&D, Pathfinder, or generic RPG conventions. Preserve names and identifiers unless an approved migration explicitly changes them.

Technical fixtures are allowed only as clearly segregated `TEST_ONLY` data with synthetic identities. They may prove command handling or persistence but cannot satisfy gameplay-parity approval. Production/release content validation must reject them. Missing or unapproved content must yield a visible diagnostic, not plausible fallback gameplay.

## 4. Stage 0 — inspect before implementation

Perform a bounded inspection of the relevant repository rather than repeatedly reading every manuscript.

Record:

1. Actual project roots, applicable agent instructions, Git state, authority pointers, and current open decisions.
2. Existing Unity projects, `ProjectSettings/ProjectVersion.txt`, package manifests/locks, render pipeline, assemblies, scenes, tests, build scripts, and runtime code.
3. Existing non-Unity rule implementations, schemas, validators, fixtures, and harnesses that should be reused or compared against. Do not equate a Python/data harness with a working Unity runtime.
4. Available Unity Editor executable, matching version, valid license availability, target build module, compatible .NET tooling, and supported test execution method. Do not bypass licensing or sandbox restrictions.
5. Baseline compilation/test results where executable, separating pre-existing failures from new failures.
6. A small reuse/change/new-work map, the selected first increment, and its acceptance tests.

Do not conclude “no engine exists” from inspecting only a remote root directory. Conversely, do not claim the game runs merely because scripts or assets exist.

Do not upgrade an existing project without a specific compatibility need and migration authorization. For a truly new project, select a currently supported stable/LTS editor after checking official compatibility information, then pin the exact editor and package versions. Do not hard-code a version from an old chat.

## 5. Architecture — one simulation, multiple interfaces

Use a small modular application, not microservices or a new general-purpose game engine.

```text
Player input / companion AI / authorized guest commands
                         |
              Validated command boundary
                         |
       Authoritative C# simulation and game state
          |           |            |          |
        World       Combat      Expedition  Inventory
          |           |         jobs/time   research
          +-----------+------------+----------+
                         |
             Events and permitted read models
                         |
          Unity scenes, sprites, audio, and UI

Approved content -> validated definitions -> simulation
Simulation <-> versioned snapshots, command traces, save/load
```

Keep domain rules free of `UnityEngine`, `UnityEditor`, scene objects, rendering, device input, wall-clock access, and network SDKs. Unity assembly definitions can enforce the lack of engine references; use the relevant configuration and verify dependency boundaries. [S2]

Keep Unity adapters responsible for input, loading scenes, authoring/baking geometry, rendering state, animation, effects, audio, and interface behavior. An animation callback must not independently deal damage, finish a crafting job, or award loot.

Use ordinary C# classes and explicit dependencies. Start with a few meaningful assemblies; add boundaries when needed. Avoid an oversized `GameManager`, reflection-heavy ability frameworks, or an ECS/DOTS rewrite without measured need.

Maintain one implementation of a rule. If a headless test project is useful, compile the same core sources through a shared project/package arrangement rather than copying them. Match C# language and runtime APIs to the actual Unity version; do not assume the newest installed .NET SDK is compatible.

Keep UI focus, encounter state, and world scheduling distinct. A single global mode enum must not accidentally suspend every companion job because one player opened an inventory screen. Define simultaneous activities through the approved clock policy.

## 6. Commands, events, and authoritative state

Route player and AI decisions through the same legality checks. Suggested technical command categories include move, interact, use ability, assign worker, start project, advance permitted game time, and save. They are interfaces, not new gameplay actions.

A discrete command should carry a unique command ID, actor/principal identity, target or task references, relevant expected state revision, and explicit player choices. Validate ownership, permissions, references, lifecycle, costs, and applicable spatial requirements. Determine the authenticated principal outside untrusted client payloads.

A rejected command must not partly mutate the state, spend resources, advance time, or consume authoritative random values. A committed effect that later fails under an approved rule is different from rejection; honor that rule's cost/refund behavior.

Use staged resolution where reactions or other decisions interrupt an action. Save enough state to resume those stages. Revalidate affected assumptions after an intervening action. Do not force every ability into one universal “pay, roll, damage” ordering.

Apply state changes through controlled transactions or explicit resumable stages. Repeated submission of an already processed discrete command must not repeat its effects. For movement input, use a suitable sequence/tick policy rather than a full snapshot transaction per rendered frame.

Publish typed results/events after committing the relevant state. Give the UI read-only views and safe rejection reasons. Previews must not alter the authoritative state or its random stream. Filter player-facing previews, logs, and guest snapshots so they do not expose hidden entities or Director-only information.

## 7. Determinism, time, and spatial rules

Use an explicit simulation clock. Document precisely how exploration updates, combat steps, travel, work, rest, pause, and time-skipping advance it. Do not use `DateTime.Now`, render frames, or animation duration as rules timing.

Where cadence is unresolved, implement the clock interface and a test-only explicit advance operation; do not invent a conversion. In cooperative play, opening one user's menu must not silently pause the host session for everyone. Apply the verified shared-session pause policy.

For authoritative randomness, use an explicitly selected, versioned algorithm with serializable state. Record enough seed/state and command information to reproduce a failure. Separate cosmetic randomness from gameplay randomness. Define stable event ordering, tie-breaking, and entity ordering. Do not rely on dictionary iteration, runtime object IDs, unstable `GetHashCode()` values, or incidental thread scheduling.

Preserve exact approved arithmetic, units, rounding, and modifier order. Propose an explicit representation when missing; do not silently introduce rounding through a float-to-integer conversion. Keep visual interpolation separate. Claim reproducibility only across configurations actually tested; a fixed seed alone is not proof of cross-platform determinism.

Maintain shared authoritative geometry for exploration and combat: occupancy, blocking, distance, visibility, elevation, and traversal. Bake or adapt Unity authoring data into that representation. If a physics result affects rules, explicitly resolve the determinism boundary; do not present Unity collision callback order as portable deterministic logic.

Process off-screen jobs at relevant milestones. When advancing over several milestones, resolve them in defined chronological order rather than awarding everything at the end. Chunked and single-step advancement should agree wherever the approved rules permit equivalent advancement.

## 8. Exploration subsystem

Implement responsive direct movement, running, a jump representation, contextual interaction, and a readable camera using placeholder art initially. Unity Tilemaps provide map-authoring and collision tools; use existing tools instead of writing a replacement map editor. [S3]

Use Input System action maps for exploration, tactical commands, and UI, enabling only the appropriate controls. Support keyboard/mouse first and a rebinding-ready design; verify controller behavior when it enters the milestone. Do not allow UI clicks or held inputs to leak into the world during transitions. [S4]

Separate ground position, supporting elevation, jump state, and sprite/shadow presentation. Jumping cannot automatically bypass walls, ceilings, hazards, or occupied landing areas. Verify interruption and encounter-entry behavior. Undefined jump costs or capabilities stay isolated rather than becoming production rules.

Implement interactions through stable world-object IDs. Start with a small selection of doors, containers, examination points, markers, and explicitly permitted digging locations. Check distance, character requirements, tools, world state, and repeat-use eligibility. Do not introduce arbitrary terrain destruction.

Followers must use permitted routes and traversal. Do not grant silent teleportation, combat movement, or special traversal to resolve pathfinding failure. Surface a blocked follower or use only an explicitly approved regrouping policy. Never create an extra character instance when changing the selected leader.

Persist opened/depleted objects, markers, and relevant discoveries independently of loaded scenes. Test leaving and returning to an area.

## 9. Tactical subsystem

Implement the verified combat cadence, spatial rules, and action economy, not an assumed genre convention. Initially use the smallest explicitly authorized encounter and ability subset whose dependent rules are resolved. A synthetic combat laboratory remains a technical test, not a finished Decennium encounter.

The resolver must account for whatever the selected approved content requires: legal targets, costs, movement, reactions, damage/healing, conditions, resistance/mitigation order, stacking, durations, resources, defeat, summons/deployables, and encounter lifecycle. Unsupported operations must be rejected clearly rather than silently ignored.

Reuse the exploration area where feasible, but preserve positions, occupancy, hazards, resource state, and active effects through transitions. Do not snap characters through barriers or grant free movement on encounter entry. Do not reset cooldowns/resources simply because the UI changed modes.

Create movement/target previews, action availability explanations, inspectable conditions, and a combat log with a concise explanation and expandable calculations. Query the actual resolver; do not maintain a second simplified legality implementation in the UI.

AI chooses legal actions using only the information its policy is allowed to know. Resolve them through the same command path as human actions. Use conventional game AI initially; do not install a live language model into combat adjudication.

## 10. Expedition jobs, crafting, and research

Represent assignments as persistent job records containing worker IDs, task definition, location, resource/tool reservations, progress, schedule milestones, outcome state, and result transaction identity.

Use explicit lifecycles such as assigned/traveling/working/returning/completed/blocked/canceled when those states are required. These names are software structure; the source rules determine durations, yields, risks, availability, cancellation costs, refunds, and delivery timing.

Implement one supported gathering job, one approved recipe, and one approved research project before expanding every profession. Keep fishing, mining, and farming in the product backlog; do not fabricate rules merely to demonstrate all three immediately.

A worker cannot occupy incompatible roles simultaneously. Tools, ingredients, storage capacity, and outputs must be tracked consistently. Material reservation is not necessarily material consumption; use the approved timing. Repeated completion notifications or reloads must not duplicate output.

Visible work animations and off-screen progress must read the same job state. Loading a work location must not restart the job or award an additional result. Resource depletion, interrupted travel, absent tools, full storage, unavailable workers, and invalid projects need defined blocked/failure behavior.

Research unlocks only approved knowledge/content. Do not expose Director-only source material through tooltips, exported content packs, debug interfaces in release builds, or guest messages. Provide assignment status and actionable explanations instead of requiring the owner to inspect scripts.

## 11. Content pipeline and approval controls

Keep immutable content definitions distinct from mutable character/item/job instances. Choose one authoritative authoring path per domain. Unity assets may hold presentation references or generated definitions; they must not become independently edited copies of canonical rules.

Reuse approved source schemas and stable IDs. Generate validated runtime data deterministically, with provenance and fingerprints. Do not parse arbitrary manuscript prose to decide gameplay at runtime. New behavior needs an implemented handler and tests; data-driven design does not make unknown behavior executable.

Validate identifiers, references, required fields, units, enum values, handler support, lifecycle definitions, approval scope, and public/private visibility. Track exactly which source records each playable slice includes and why. A technical fixture may be included only in an explicitly marked laboratory build and must be excluded from release content.

A passing importer establishes that the importer passed its checks, not that a rule is balanced or authorized. Keep source approval, implementation parity, integration, gameplay evaluation, and publication gates separate. Preserve all existing domain gate identities instead of replacing them with a global green status.

## 12. Save/load and recovery

Use versioned serialized data with stable IDs, not raw scene-object references. Record the save schema, compatible build/rules/content versions or fingerprints, world changes, character/inventory state, clock, random-generator state, jobs/reservations, and pending decisions for the supported save boundary.

Define whether saving is allowed mid-resolution. Either serialize the required staged state or restrict saving to a documented safe boundary with an understandable message. Do not silently discard pending effects or choices.

Write to a temporary file, validate, then replace the intended save using a tested same-volume strategy. Retain a last-known-good backup and handle interruption/corruption explicitly. Do not promise crash safety without testing the actual platform behavior.

Detect incompatible schema/content versions and missing IDs. Migrate with an explicit tested migration, preserving the original, or reject with a useful explanation. Never load an unknown ability as a different one or reset a campaign silently.

Test that restoring a save and applying the same subsequent commands reproduces the supported outcomes. Include jobs completing near a save, repeated commands, resource reservations, scene unload/reload, and different approved content versions. Checksums detect accidental corruption; they are not a claim of tamper-proof saves.

## 13. Cooperative readiness, without MMO scope

Keep a host-authoritative command boundary from the beginning. Solo player commands should use the same validation path intended for guests, while actual network transport may be deferred until the local loop is stable.

Preserve host plus up to four guests as the target requirement. Inspect the delegated-control decisions rather than assuming each guest necessarily controls one character. Separate player identity, controlled entities, permissions, and local UI focus.

The host validates guest permissions, command freshness, state revision, and cost. Never accept client-calculated damage, loot, completion time, or claimed identity as authoritative. Include command sequencing, duplicate suppression, bounded input validation, and synchronized state revision.

Prototype two connected participants before claiming broader multiplayer support; test the full target later. Reconnection, permission revocation, incompatible content versions, dropped/duplicated messages, and host disconnect need explicit handling. Do not promise seamless host migration. Do not add accounts, matchmaking, paid hosting, or an MMO backend in the initial assignment.

## 14. Ongoing AI-assisted oversight

Treat engineering oversight as a continuing responsibility, not a one-time “AI approved” label.

For each bounded change:

1. Establish the governing source and acceptance examples before coding. Identify affected rules, dependent systems, saves, and content.
2. Implement the smallest coherent change with tests.
3. Perform an adversarial review against the original source: event ordering, repeated triggers, resource duplication, invalid transitions, hidden-information exposure, save restoration, and unsupported assumptions.
4. Run the relevant automated checks; investigate and preserve failing sequences. Convert confirmed failures into regressions.
5. Update the implementation trace and handoff with evidence and unresolved questions.

Where a separate reviewer/agent is available, supply the actual source and patch independently. If review was self-review, label it self-review; do not claim independent verification. Limit parallel agents to disjoint work and avoid concurrent writes to the same scenes, prefabs, package files, or saves.

Expected test outcomes must come from approved examples or independently derived invariants, not simply from the implementation under test. Differential comparison with an older harness is useful but cannot prove both implementations are correct. Do not weaken assertions, rewrite expected results, or delete difficult scenarios merely to obtain green output.

Use bounded simulations and record sampled combinations. Prioritize high-risk interactions; do not claim exhaustive coverage of the entire rules space. Report performance and coverage measurements with their workload and environment. Do not launch indefinite multi-agent reviews or unbounded combinatorial tests.

The owner's role is to resolve meaningful game-design choices and evaluate the experience. Supply technical analysis rather than transferring every engineering uncertainty back to the owner.

## 15. Verification requirements

Use the existing test framework where suitable. Unity supports Edit Mode and Play Mode test execution, including command-line runs and XML result files. Verify arguments against the installed package/editor rather than copying an unrelated version's flags. [S5]

Separate results for content validation, pure rules tests, Unity compilation, Edit Mode tests, Play Mode integration, standalone build, and human-observed gameplay. A .NET test pass is not a Unity compilation pass; a Unity import is not a successful player build. A headless test is not visual inspection.

Minimum regression families, as relevant features are implemented:

| Area | Required evidence |
|---|---|
| Commands | Invalid command leaves authoritative state/RNG unchanged; repeated discrete command cannot repeat effects; stale/unauthorized commands are handled. |
| Rules | Approved examples, event order, boundaries, stacking/expiration, resource accounting, and selected cross-system interactions agree. |
| Preview | Querying a preview changes neither state nor authoritative randomness and exposes no unauthorized information. |
| Spatial | Walls, occupancy, traversal, range, and encounter transitions agree across the implemented modes. |
| World | A container cannot award twice; depleted/interacted objects persist through scene reloads. |
| Jobs | No incompatible double assignment, double spending, double completion, or visible/off-screen double progress. |
| Time | Equivalent allowed time-advance sequences produce equivalent state; menus and render rate do not change outcomes outside policy. |
| Saves | Supported round trips preserve state/RNG/jobs; incompatible/corrupt data and interrupted writes are handled. |
| Unity lifecycle | Reentering Play Mode and repeated area load/unload do not duplicate services, events, or input handlers. |
| Build | Intended scenes and content are present; editor-only code and test-only data are absent from a release-profile build. |

Write Windows-friendly verification scripts where appropriate. Discover or accept an explicit Unity executable path, preserve logs, isolate each run's result directory, handle timeout/nonzero exits, and verify actual test discovery and completion. Zero discovered tests, missing XML, stale output, skipped checks, and licensing failure are not passes. Do not run competing Unity processes against the same project or terminate an existing user editor session without authorization.

Keep lightweight checks frequent; run wider affected regression suites at integration boundaries. Build a standalone development player early enough to detect editor-only dependencies. Name remaining human visual/feel checks explicitly.

## 16. Unity and repository hygiene

Preserve `.meta` files and asset GUIDs. Unity documents that `.meta` files carry references and should remain paired with their assets. Track the relevant `Assets`, `Packages`, and `ProjectSettings` contents; keep generated caches and local build output out of normal source commits. Inspect existing ignore/LFS conventions before changing them. [S6]

Use explicit editor-only assembly boundaries. Prefer deterministic, idempotent editor construction tools or established scene-authoring practices over large handwritten scene/prefab YAML. Re-running a setup tool must not duplicate objects or overwrite hand-authored work.

Do not delete legacy folders, manuscripts, fixtures, or assets as “cleanup.” Do not reset the working tree, force-push, merge, publish, change repository permissions, or silently migrate branches. Any authorized commit must include only the intended changes. Preserve unrelated owner edits and clearly distinguish newly introduced warnings from baseline issues.

Avoid unnecessary packages, render-pipeline migrations, broad reserialization, global setting changes, and paid dependencies. Keep assets replaceable and record their origin/license information. Use original simple placeholders or assets with verified permitted use; do not ship extracted commercial-game assets merely because they are available locally.

Do not embed secrets, upload private source material to unapproved services, disable security controls, or execute downloaded code to make the workflow easier. Treat external files as data unless their executable use is intentionally authorized.

## 17. Staged delivery and acceptance gates

### Stage 0 — baseline and readiness

Deliver the bounded audit, authority/reuse map, baseline evidence, decision blockers, and selected Stage 1 task. Preserve existing work.

### Stage 1 — runnable foundation

Establish or extend the simulation/Unity boundary, stable identity, a minimal command path, a small developer test area, placeholder movement/rendering, one safe interaction or synthetic transaction, and an initial snapshot round trip. Add automated rejection/idempotency/persistence checks. Wire an actual usable scene or idempotent scene builder, not scripts that require unexplained setup.

Any provisional movement or interaction behavior is labeled `TEST_ONLY`, with production hookup blocked until supported by the source. Report the exact scene, controls, test commands, and verification status. When Unity is unavailable, provide compilable/testable non-Unity work and setup tooling where feasible, but keep Unity compilation, playability, and build checks explicitly BLOCKED/NOT RUN.

### Stage 2 — connected exploration slice

Demonstrate a small hub and connected area with movement, approved traversal, contextual interactions, persistent world objects, and supported followers. Reload the area and save without duplicating or losing state.

### Stage 3 — tactical integration

Use an approved small encounter and sufficient source-backed rules to enter combat, make meaningful actions, explain results, and return to exploration. Test lifecycle, position, resource, and effect continuity. Do not call a synthetic battle approved gameplay.

### Stage 4 — expedition-management integration

Add one approved gathering task, one recipe, and one research project. Demonstrate assignment, permitted time progression, resource handling, off-screen consistency, and persistence. Report blocked content honestly rather than fabricate it.

### Stage 5 — complete vertical slice

Demonstrate: prepare an expedition, explore, resolve a tactical encounter, return with a permitted result, progress companion work, complete supported crafting/research, save, reload, and continue. Produce a standalone development build with a known content subset and remaining limitations.

### Stage 6 — cooperative proof and measured expansion

Test host/guest delegation through the same rules path, then expand toward the stated participant target. Expand classes, professions, content, and art incrementally after the connected loop is stable. Use profiling and playtests to prioritize work. Passing this stage does not automatically establish balance or publication readiness.

## 18. Deliverables and completion report

Reuse existing documentation locations and schemas. Suggested new filenames below are outputs to create only if equivalents do not exist, not claims that these files are already present:

- `docs/unity/UNITY_ENGINE_PLAN.md`: verified environment, reuse map, architecture, stages, and first task.
- `docs/unity/IMPLEMENTATION_TRACE.md`: pointers from implemented behavior to source and verification; no duplicated rule authority.
- `docs/unity/DEVELOPMENT_HANDOFF.md`: exact current state, reproducible commands, next bounded task, and unresolved decisions.
- Test/build scripts and task-specific result directories following established repository conventions.

Each completion report must state:

**Implemented:** The actual behavior delivered and how to exercise it.
**Changed:** Exact files, source/domain references, and dependency changes.
**Verified:** Commands actually run, tool versions, test counts, results, and evidence paths.
**Not verified:** Missing tools, unexecuted tests, omitted content, known failures, and human checks.
**Approval impact:** What remains proposed, test-only, blocked, or awaiting its existing gate.
**Next task:** One bounded implementation target, not an open-ended backlog dump.

Use explicit statuses such as PASS, FAIL, BLOCKED, and NOT RUN for individual checks. Reserve “playable” for an actually exercised loop and “build passed” for a completed build. Never translate a provisional review or written test into release approval.

**Start now with Stage 0. Then execute only the smallest safe Stage 1 increment. Do not redesign the rules, rewrite the repository, or build all stages at once.**

---

## Reference notes for this brief

These references support tool behavior and source routing; they do not decide gameplay. Use documentation matching the actual installed versions. The preparation checked remote repository pointers, not the owner's local working tree, and did not modify the repository or execute Unity.

**[R1] Repository canon entry point:** `CANON_MANIFEST.md`, remote default branch at inspection; blob `0d41c4bc6f6031c4e1a371a9f83b8af2332de5c3`. Points to `docs/canon/CANON_MANIFEST.json` and forbids a parallel source of truth.

**[R2] Repository promotion policy:** `docs/canon/REPOSITORY_PROMOTION.md`, remote default branch at inspection; blob `15c9fbc9553ec3f04f6f5ad032bdef96d41b65a3`. Review the actual local/current policy before implementation.

Official documentation entry points consulted on October 20, 2026:

```text
[S1] Codex project instructions / AGENTS.md
https://developers.openai.com/codex/guides/agents-md

[S2] Unity Assembly Definition Inspector / No Engine References
https://docs.unity3d.com/6000.0/Documentation/Manual/class-AssemblyDefinitionImporter.html

[S3] Unity Tilemaps
https://docs.unity3d.com/6000.0/Documentation/Manual/tilemaps/tilemaps-landing.html

[S4] Unity Input System actions and action maps
https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/Actions.html

[S5] Unity Test Framework command-line execution
https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html

[S6] Unity scene/prefab version-control guidance and .meta files
https://unity.com/blog/author-scenes-and-prefabs-with-verson-control
```
