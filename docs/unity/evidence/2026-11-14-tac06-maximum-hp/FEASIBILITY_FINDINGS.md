# TAC-06 connected-route feasibility findings

Status: diagnosed predecessor capability boundaries; no Flesh Warden implementation or new capacity behavior. The bounded wire103 Short Rest implementation remains accepted at `44837a2ed2be8a558ca6d37544621dac6400ab9d`, final review `6d19f40f-94d7-5f70-8f52-26a18a90f7a2`. These probes identify a composition gap for its proposed successor, not a replacement for that accepted evidence.

## Reproduction and authority

Both raw JSONL histories ran through the accepted `-ShortRest` public console and its unchanged Core/Persistence/LabModel assemblies. The diagnostic script restores their authentic saves through `ConnectedExpeditionSession.StartWithShortRest`, then inspects a detached snapshot and invokes the policy resolver to name the denied capability. It does not edit the snapshot or save. `feasibility/diagnostics.json` binds implementation, assembly SHA-256/MVID, checkpoint hashes, public encounter mode, actor state and exact denial reason. `FEASIBILITY_BINDINGS.json` binds every retained file and relevant source blobs.

Run `Inspect-Feasibility.ps1 -AssemblyRoot <accepted-headless-directory> -OrdinaryRun <packet>/feasibility/feasibility -CalendarRun <packet>/feasibility/rest-before-later-encounter -Output <new-diagnostic-path>` against the accepted assemblies. The retained JSONL and all produced save checkpoints supply the full public input history. These are diagnostic runs with expected denials, not passing successor scenarios.

## 1. Existing vial healing requires a tactical turn

The first probe moves the existing manufactured-vial use from the later tactical encounter to after a genuine completed Short Rest. It preserves the real injury and finite vial: at the berth the hero has 18/26 normal HP and three temporary HP. The full hour expires the temporary grant and completes the rest. The subsequent `UseAlchemyDose` is `Unavailable`; the exact resolver reason is `AlchemyOwnTacticalTurnRequired`. The canonical before/after saves are identical at revision203, time120681/2, HP18/26. All233 inputs and responses are retained in `feasibility/feasibility`.

`SharedManufacturing.cs` explicitly requires `InventoryCombat` and the actor's own current tactical turn, then a lawful Action and access to the actual dose. An ordinary-use procedure is therefore unsupported. This finding does not authorize adding one, assigning an invented duration, injecting damage, or replenishing a vial.

## 2. A historical sparse calendar rejects an ordinary berth visit

The second probe inserts six paid world steps and a proposed first rest into the existing route before its later encounter. The hero lawfully arrives at berth(0,1), revision120, time56681, HP26/26. Both `InventoryCombat` and public `InEncounter` are false, but the earlier encounter's historical sparse calendar still exists (`world.fixed-conflict`, `Sparse=true`). `BeginShortRest` returns `Unavailable`, with exact reason `ShortRestRequiresOrdinaryExploration`.

`SharedShortRest.ShortRestAccess` treats any non-null Encounter as disqualifying admission, and `ShortRestEncounter` treats a historical calendar roster containing the hero as an encounter. Thus simply removing the initial non-null test would still fail. The existing ordinary clock retains and advances this sparse calendar; its presence alone is not live combat authority.

All277 inputs/responses and produced checkpoints are retained in `feasibility/rest-before-later-encounter`. The unaccepted first-rest request creates no rest record; the following hour is ordinary clock advancement. The real later encounter, genuine injury, tactical vial use, later completed rest and paid continuation still execute. The input generator expected14 extra committed commands and shifted one historical duplicate request's explicit revision accordingly; because the rest is denied, only13 commit, and that duplicate returns CommandIdConflict. This is a probe offset consequence, not an independent engine defect. No claim is made that this run satisfies successor acceptance.

## Proposed decision for GPT

Codex recommends preserving tactical-only vial use and resolving the Short Rest/calendar composition gap before implementing Flesh Warden. Please choose and define the bounded sequencing: a separately reviewed MGT-03 admission correction first, or an explicitly versioned child contract. In either case, actual admitted combat must still prohibit or interrupt the resting actor, and historical calendar identity, shared scheduling, replay and supported saves must remain intact. No encounter state should be cleared merely to make rest possible.

Please also review a revised connected witness: first lawful rest before the later encounter, raising capacity26 to32 while retaining normal HP26; then genuine later injury and existing finite tactical vial healing; second lawful completed rest replacing Flesh Warden with authorized dormant Spinal Buffer, recomputing to26 and clamping only if actual current HP exceeds26; then paid continuation. This demonstrates equip without healing, actual healing into additional capacity, and removal without damage. The parent vial's potential9 is a feasibility lead only; the new timing/inputs must independently prove actual dice and HP. It changes the previously suggested injury-before-first-rest order, so it is not silently adopted.

No ordinary healing, new encounter, loadout API, schema104, mutation entitlement or engine changes have been implemented. The source/API contract remains the current gate. Production authority, broader MGT-03, whole-engine completion and Unity integration remain open/deferred as previously recorded.
