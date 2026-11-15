# Shared capacity integration audit

Inspected against implementation `0742794a7c1f8e15dd4e38ff72ae21dd61762b4a`. This is a code-path audit; execution evidence is reported separately.

| Concern | Existing/new path and bounded result |
| --- | --- |
| Base authority | `ActorCharacterRecord` retains actual Warrior levels and CON. `SharedFleshWarden.ApplyMutationCapacity` calls `PlaytestCharacters.BaseMaximumHp`; it never feeds the modified life maximum back as base. |
| Actual source | Shared feature grants carry the exact two `TestOnlyFixtureEntitlement` entries. `FleshWardenProfile` validates the hero, numeric Warrior3 profile, actual levels, CON, pinned source and Basic Vital qualification before the narrow Hit Dice exclusion. |
| Completed-rest authority | `ShortRestBerth.Validate` reconstructs either the exact original rest receipt or the exact mutation-plan receipt and counts both. The plan is immutable; `ReconcileShortRest` rechecks access and qualification. `EndShortRest` settles the loadout and shared life in the same candidate transaction. |
| Effect identity | A new actual equip derives one application identity from the successful rest. Same-card completion retains identity/start. Replacement ends that exact record at the second actual completion. Initial dormant Spinal Buffer supplies no fabricated prior rest. |
| Shared life | `ActorLifeRecord.MaximumHp` stores admitted pre-systemic capacity, with current normal/temporary HP and life facts still in the same record. The original character base remains separate. |
| Damage | `TestOnlyClubAttackPolicy` and shared ranged resolution use `ActorLifeRules.ReadForResolution`. Damage/Wound/Instant Death thresholds therefore use the effective capacity; `RecordFromResolution` preserves pre-systemic capacity when recording the result. Historical damage records retain their event maximum. |
| Finite healing | `SharedManufacturing.UseAlchemy` retains its own-tactical-turn, Action, real held dose and ingestion checks. It calls `ReadForResolution`, then `PlaytestLife.Heal`; the existing Critical ceiling uses effective maximum minus one. No ordinary vial use is added. |
| Stable recovery | `ActorLifeRules.RecoverDue` resolves the existing absolute deadline through `ReadForResolution`, then records the result through `RecordFromResolution`. Capacity recomputation does not change Stable state, its deadline or death counters. |
| Expedition Strain | `ApplyMutationCapacity` supplies the current shared Strain level to `PlaytestMaximumHp.Recompute`, stores pre-systemic capacity, and clamps to the effective ceiling. Later life resolution and `ExpeditionStrainRules.ClampLife` each project from pre-systemic capacity, so the multiplier is not compounded. |
| Temporary HP | `SharedConsumeDecay` retains source and expiry separately and preserves the same life maximum on its updates. The capacity operation preserves temporary HP and the existing grant object. Connected expiry remains independent of rest settlement. |
| Public view | The selected wire104 actor view reads effective maximum through the shared resolver. The mutation view is restricted to the current controlling player. Console output omits the new property on old profiles to preserve their transcripts. |
| Persistence/replay | Wire104 adds a distinct marker/tail and fingerprint. Strict decode validates grants, qualification, real rest links, application identity/magnitude/endpoints, loadout and shared capacity; canonical command replay validates history and settled metrics. Existing layouts and enum values retain their old encodings. |

Core Exhaustion composition, other connected capacity sources, general Warrior progression/acquisition, empty-slot removal and third-rest mutation changes remain unadmitted. A numerical helper accepting a combination does not provide its connected source authority. Detached tests of the shared operation are labeled as such and do not manufacture those capabilities for the public route.
