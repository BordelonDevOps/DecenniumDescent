# Unity Rules Engine Development correction review

Response `98339499-82e2-403d-a8b8-c8e534d53319` reviewed corrective source `3d866e6fa8e2996a6799b1a1f51a05b735b70b45` and evidence `20ffbd264f873f01900276296279a9cc43b0171f`. [Review chat](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

## Focused disposition: B1 and B2 resolved

**Corrective source:** `3d866e6fa8e2996a6799b1a1f51a05b735b70b45`
**Evidence packet:** `20ffbd264f873f01900276296279a9cc43b0171f`
**Prior hold:** `6dbac0a2-455e-45a0-a204-5ada740fff94`

**Close B1 and B2 for this exact correction. No further B1/B2 code changes are requested.** The implementation and retained public C#/console evidence address both defects identified in the focused hold.

**E1 remains open. Final bounded-session acceptance also remains pending the corrected unfiltered execution and isolated 30-sample benchmark.** This is defect closure—not P1/INT-03 completion or authorization to begin a successor.

| Review item | Disposition |
|---|---|
| **B1 — admitted attacks create unavailable knockout/Press continuations** | **Resolved** |
| **B2 — human off-turn responder lacks required turn context** | **Resolved** |
| **E1 — exact corrected unfiltered regression** | **Pending: expected 1,482 cases** |
| **Corrected isolated reference-performance evidence** | **Pending** |
| **Previously identified broader P1 latency costs** | **Unchanged; still open** |

## 1. B1 — the existing continuations are now reachable and correctly ordered

The correction adds `ResolveKnockout` and `RespondPress` to the exposed combat commands. Admission is tied to the **actual pending attack’s attacker** or the **current Press offer’s actor**, rather than merely accepting a command because its actor belongs to the submitting seat. Both continue through the existing authority, payload, receipt and `Simulation.Execute` path.

The pending-decision projection now follows the required order: **knockout, actual indexed opportunity, current Press, manufacturing quality, then regular turn**. Crucially, knockout is checked before indexing a suspended move, and opportunity projection/admission both check `ResponseIndex < Reactors.Count`. This addresses the concrete state where the last reaction has already committed but its knockout decision still suspends movement.

### Deferred knockout evidence

The new C# control reaches this state through actual public commands, saves it, and explicitly asserts that the suspended move has **`ResponseIndex == Reactors.Count`**. It restores into a fresh session, obtains the knockout identity from the player’s view, rejects the wrong seat, retries the original reaction as `Duplicate`, and resolves the pending decision through `ResolveKnockout`. The new registered case has a recorded passing execution.

The console transcript independently exercises the adapter path: the restored opportunity is `move.8` at revision 8; the player’s attack commits revision 9 with `PendingDecision: Knockout` and decision `attack.9`. After restoration, the reaction retry remains `Duplicate` at revision 9, wrong-seat resolution is `NotAuthorized`, and the correct resolution commits revision 10 with no pending decision.

That closes the original knockout finding without suppressing the attack option, choosing an outcome automatically, or bypassing the normal resolver.

### Press evidence

The separate branch uses a real first-opponent attack, player departure and declined ordinary opportunity to create the Press offer. The restored director view identifies `press.12.TEST_ONLY.third-combatant` and the player’s current turn context. The wrong seat is rejected; the director’s acceptance commits revision 13, performs the follow to **X = 2**, and returns control to the player. The exact retry remains `Duplicate` at revision 13, with the final view still at X = 2 and no pending decision.

**The explicit original turn argument on the Press retry is correct.** The initial request resolves its omitted turn through the owning view; an exact retry must retain those resolved arguments, not recompute them from a later view after the decision has disappeared. The retained inputs show precisely that distinction.

## 2. B2 — human off-turn responses now have sufficient public context

`View` now exposes the current `TurnId` when the seat either controls the regular-turn actor **or owns the actual pending opportunity, knockout or Press response**. The additional condition is limited to those tactical decisions; it does not confer general control over the regular-turn actor. `ActingActorId` and `DecisionId` remain filtered by ownership.

The evidence exercises this in both human-seat directions:

- The **player** receives `world.fixed-conflict.turn.1` for its opportunity during the first opponent’s turn.
- The **first opponent** receives `world.fixed-conflict.turn.2` for its opportunity and subsequent Press during the player’s turn.

The initial console submissions omit `combat.turn`. The harness launches the actual `Open-ConnectedExpedition.ps1` process and exchanges JSON requests and responses; the responder’s own public view supplies the required context. Although the harness also reads the other seat to assert projection restrictions, it does not use that other view to construct the responder’s command.

One important distinction is preserved: **the regular-turn owner may still see its own turn token while another actor responds**. That does not authorize it to answer the other actor’s decision. The decision identity and acting actor remain scoped, and wrong-seat submissions still fail. After the director’s off-turn Press resolves, its final view again has empty acting, turn and decision fields.

## 3. Scope, compiled evidence and original-route preservation

The source comparison confirms the bounded change: **two session model files and the existing registered case file**, with no core combat, persistence, save-schema or console implementation change. The evidence commit follows the correction without further package-source changes. The correction implements the existing responses rather than introducing new gameplay rules.

The passing controls are recorded in **two separate reports**: `compile/headless.json` records the new pending-choice case as **one discovered, one passed, zero failed**; `compile/scope-control.json` separately records the original scoped-view/delivery/recovery case as passed. `BINDINGS.json` associates both with the corrected implementation and retained assembly set. This supports two passing registered controls, not a completed unfiltered run.

The standalone C# 9 compilation report passes Core, Persistence and LabModel. Static validation records all 18 checks passing, with 396 package assets and 396 unique GUIDs. These remain standalone/static results, not Unity gameplay validation.

The corrected connected report and console report preserve the original **165 commitments**, pending revision-113 digest and final revision-165 digest:

```text
Pending: 724f6b4b6e4001f5d848e7a84eda39bd8439901d669a7bde3f56743b7554bea7
Final:   6f1bc7afa0f5727e76dccc26d0d33911682f791a3ca3e971ca1350c64dcdd521
```

The corrected connected results also retain the ordinary recipe-4 fingerprint, receipt split, two encounter closures, research/manufacturing outcomes and healing from 23 to 26 HP.

## 4. Performance disposition remains separate

**The corrected packet is not a performance pass.** Its report explicitly says `TIMING BUDGET MISSED` with `WarmSamplesPerInput: 1`. Specifically, stabilization at resulting revision 105 records **1,133.642 ms against the 350 ms reference budget**. With one observation, the reported median, p95 and maximum are the same measurement—not an isolated 30-sample distribution.

The packet documents concurrent regression load. That explains why these results are being submitted as correctness evidence, but it does **not** establish the cause of the miss or waive the benchmark. The same run discloses **14,619.955 ms full restore** and **8,210.284 ms for the revision-106 advance**; those observations should remain retained rather than being replaced by the earlier isolated measurements.

My prior broader P1 ruling is unchanged: the slow charter-plan submission and long calendar advances remain unresolved responsiveness work. Strict external restore remains separately measured; validation must not be weakened to reduce its apparent cost. Closing B1/B2 neither clears those costs nor creates another gameplay-correction requirement.

## 5. Remaining acceptance requirements

**E1:** retain and submit the completed **1,482-case unfiltered execution on the corrected assembly set**, with case results and source/assembly bindings. The earlier 1,481-case run belongs to the original implementation and remains separate historical evidence; it cannot substitute for corrected execution.

**Corrected reference timing:** submit the isolated **30-warm-samples-per-input** run on the corrected assemblies using the existing eight workloads, unchanged budgets and actual submission-through-commitment-plus-permitted-view boundary. Retain all route samples and separately reported file-operation costs. A reference-budget miss remains unresolved until specifically dispositioned.

No additional B1/B2 implementation return is required on the evidence reviewed here. **Successor work remains gated until actual acceptance.**

### Inspection boundary

This was a read-only review of the exact source diff, corrected session logic, C# control, interactive console harness and transcript, build/static reports, bindings and connected results. I did not execute programs, load the saves independently, recompute artifact hashes or rerun the measurements.

**Final disposition: B1 closed; B2 closed; E1 and corrected performance verification pending. Final bounded-session acceptance, broader P1/INT-03 completion and successor authorization remain withheld.**
