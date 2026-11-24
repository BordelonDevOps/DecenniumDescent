# Current-condition read dependency

**Architecture concurred by actual GPT response c36c4641-a600-5d3c-91eb-043cc9347da5; concrete carrier/access and full transitive contract remain OPEN.** Codex concurs. No runtime change or implementation permission is claimed.

The existing current-condition helpers are not a trivial record lookup. ConditionCombatPolicy.cs:10-14 calls ConditionResolutionScope.Project. ConditionHistory.cs:29-37 reconstructs a ledger by resolving every retained operation; :106-122 may project that ledger to current RuleClock through ConditionLedger.AdvanceTo. ConditionLedger.cs:215-231 traverses expiries and constructs immutable transitions/consequence objects. This does not mutate the authoritative snapshot or draw RNG, but it does perform historical lifecycle resolution and deadline traversal on temporary state. Calling it indirectly through sight, hands or Action admission must not evade the HC no-replay/no-settlement read contract.

Agreed correction: the owning simulation establishes an immutable current condition projection only during verified construction/strict restore and successful authoritative transitions. Bind it to current owner/policy, revision, selected schema, exact condition journals and current rule-clock marker. All new V1 reads consume that established projection through a scoped lookup. Missing or mismatched projection fails safely; no read-time Restore, AdvanceTo, repair, initial-state reconstruction or fallback is allowed.

The proposal adds no saved ledger, changes no condition rule and never commits reconstructed historical consequences. Legacy queries/execution and validation retain their original behavior. The projection needs a concrete owner/capability arrangement and complete call graph before implementation; read-only return types alone do not establish purity. An implementation must also avoid mutable aliases, stale inherited scopes, cross-simulation cache reuse or exceptions contaminating the ambient scope.

Required source decisions and prospective evidence:
- Identify all current-condition consumers, including sight, life/capability, hands, concentration, target admission, healing modifiers, costs, discovery and rich result disclosure.
- Prove the established projection matches native current semantics, including version-selected projection to RuleClock and expiry/onset/suppression/inherited components.
- Distinguish verified transition-time creation from prohibited read-time lifecycle resolution. Read instrumentation must count Restore/Resolve/AdvanceTo calls, not only RNG/live-state changes.
- Repeated reads and rejected commands cannot advance/replace the capability. Strict restore constructs a fresh capability after original validation.
- Verify owner, revision, journal identity/content, rule-clock marker, immutable-copy boundaries and disposal/error paths. Equal state from another simulation is not transferable proof.
- Keep policy-private effects and application identities filtered; possessing a current condition projection is not permission to reveal it.

## Required corrections from actual GPT review

Prepare the projection for the final validated state after all condition/life/concentration/clock processing, for ordinary-validation profiles as well as verified-checkpoint profiles. It is not dependent on planning passage authority. Publish on construction/restore and successful transition only; rejection and exact duplicate retain the existing projection.

Preserve two distinct native modes. Before ExpeditionRouteSchema, ConditionsFor uses the journal-time ledger. Later schemas request RuleClock at its exact phase; At advances only if that marker is later and does not rewind a later-phase ledger. Preserve journal policy/target/origin and complete content, owner/policy/revision/schema/profile and exact requested marker/mode. Snapshot.Copy retains immutable journal objects but copies the array: journal reference identity alone cannot substitute for the other bindings.

Materialize journal-time and needed projected ledgers, not only ConditionView/active bits. Consumers can need application identities, intervals, ended/suppressed state, immunity sources, inherited components and history capacity; audit direct ConditionResolutionScope.Read and historical-prefix consumers too. Cached conditions are never cached life, equipment, permission, relationship or actor-control grants. Current condition data cannot answer historical event-time questions without a separately retained native source.

A successful legacy command or authenticated restore must not fail merely because V1 derived projection construction fails. Publish the truthful state with an explicit unavailable projection for that new revision, never the old revision's projection. No retry, false rejection or corrupted-save diagnosis. This failure isolation does not waive any supported V1 qualification requirement.

Allowed V1 reads are strict lookup, exact structural comparison and audited selection/aggregation over already materialized immutable facts. No semantic journal fold, expiry processing, consequence creation, lazy reconstruction or repair is approved. Preparing the projection at trusted boundaries must never call CommitCondition, append journal operations or execute historical drop/concentration consequences.

## Concrete access proposal still requiring review

Use a separate optional Core policy capability for current read projections, applying to all admitted profiles. Proposed Core-only types:

- `ReadStateStampV1`: sealed, internally constructed by its owning Simulation for each final validated state; contains an unforgeable-by-payload owner/generation identity and exact selected policy/revision/schema/profile/clock binding. No public constructor or serialized representation.
- `IReadStateProjectionPolicyV1.CreateReadProjection(ReadStateStampV1 stamp, Snapshot detachedValidatedCurrent)`: called only at trusted state-establishment points. Receives a detached copy of the final validated state, never the mutable authoritative Simulation.state. Copy alias safety must be audited. A provider that mutates its input, throws or returns an invalid projection cannot mutate the committed state or publish a prior stamp. Returns an opaque `IReadStateProjectionV1`; no Core reference to LabModel condition types.
- `NativeReadContextV1`: internally constructed by Simulation, pairing its exact current stamp and projection, handed only to trusted native V1 projection/assessment helpers within one observation. It is not a public result/authority or a caller-provided proof.
- The LabModel implementation retains immutable journal-time and projected ledgers keyed by native target/journal/marker/mode, plus exact stamp identity. Lookup verifies those bindings and the owning current snapshot's immutable journal references/content; absent/mismatched entries return a technical unavailable result. It never uses the legacy lazy ConditionResolutionScope as fallback.

Extend both proposed assessment interface signatures with this trusted read context. Description, discovery, choices, cost, disclosure and result helpers receive the same current context through explicit parameters. An adapter, if needed for existing pure predicate bodies, must require exact owner/stamp binding and fail closed on every attempted legacy Restore/AdvanceTo path; thread-static ambient state alone is insufficient. Prefer explicit context propagation and retain all old signatures/behavior for legacy entry points.

Simulation holds the stamp/projection privately. Existing Simulation has no internal lock: connected construction establishes state before the session is published; all subsequent connected restore/submit/read publication uses the same existing session gate, and direct Core use retains the single-owner synchronous calling contract. No new cross-thread Core safety is claimed. Capture current state, generation and projection under that same owner boundary; never acquire them in separate observations. Actual authoritative execution publishes the final state and the matching projection result together within that boundary. Ordinary validation/checkpoint success remains the commit criterion; derived-data exceptions are isolated afterward without replay/retry, and are retained as defects. No new save schema, public unchecked data, global cache or caller mutation is introduced. The exact carrier shape and exception boundaries still need independent and actual final contract review; the names above are not implemented APIs.

## Member and publication decisions from actual GPT05

Actual response `e70be17d-6889-5e41-a22c-4a8dbe4b15b6` accepts this direction with the following concrete corrections; Codex concurs. Types in public cross-assembly signatures have compatible public CLR accessibility, while `ReadStateStampV1` and `NativeReadContextV1` retain internal constructors and minimal read-only accessors. They are never gameplay DTOs or console values. Owner/generation identities remain private. No public constructor, setter, deserializer, arbitrary-snapshot factory or session accessor can mint or expose a usable current context.

`IReadStateProjectionV1` exposes a read-only `ReadStateStampV1 Stamp`. Simulation requires reference identity with the exact stamp supplied to its trusted policy provider; null, foreign or earlier stamps publish technical unavailability for the current generation. The provider is non-reentrant with respect to Simulation/session operations. A callback cannot observe new state paired with an old projection. Final state plus matching projection or current-generation unavailability publish together within the established owner boundary.

The provider is trusted policy code: stamp identity binds its output but does not prove its calculation correct. Source review, all-profile copy/alias checks and native parity evidence remain required. The finite planning alias audit does not cover every all-profile builder snapshot. No saved projection, new Core lock, Core-to-LabModel dependency or read-time repair is introduced.

All referenced runtime sources remain unchanged. This note records agreed architecture and open qualification obligations, not a passing purity test or full implementation authorization.
