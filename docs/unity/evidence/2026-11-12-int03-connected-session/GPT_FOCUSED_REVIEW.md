# Unity Rules Engine Development focused review

Response `6dbac0a2-455e-45a0-a204-5ada740fff94` reviewed source `3c7b13728d13bfddbf47976220cd867652d4762d` and evidence `e08efd29e3354d473f432c58f5cb4c9a1fdbc49f`. [Review chat](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

## Thin public C# session — focused hold for two pending-decision gaps

**Source reviewed:** `3c7b13728d13bfddbf47976220cd867652d4762d`
**Evidence reviewed:** `e08efd29e3354d473f432c58f5cb4c9a1fdbc49f`
**Controlling contract:** `7e7a9141-78c3-4dcb-923b-7ea779e7eab2`

**The recorded walkthrough is supported, but the public session is not yet acceptable. I found two concrete adapter defects: it can admit attacks that create pending decisions it cannot answer, and a human off-turn opportunity responder is not given the turn token required to respond.**

These are bounded session-interface corrections. They do not reopen the accepted combat rules, manufacturing implementation or verified-prefix validation.

**The newly exposed latency costs remain material to broader P1. They do not create an additional correctness hold on this bounded adapter, but the evidence does not establish session-wide responsiveness.** The exact regression also remains pending.

The implementation-to-evidence comparison contains documentation and artifacts without subsequent package-source changes.

## 1. B1 — admitted attacks can create unanswerable pending choices

### Deferred knockout

The session permits `AttackClub`, passes its `CombatRequest` through, and does not exclude the existing deferred-knockout instruction. The console also accepts a caller-supplied knockout selection. However:

- `CombatCommands` does **not** expose `ResolveKnockout`.
- `ActingActor` and `ExpeditionDecisionKind` do **not** identify the pending knockout or its owner.
- Once the engine records that continuation, its resolver rejects unrelated commands with `KnockoutChoicePending`.

Consequently, a legitimate eligible attack can commit an outcome that the public session cannot complete. Saving and restoring preserves that pending state; it does not supply the missing response path.

**Reproduction sequence:** use the exposed first-fight commands to make an eligible melee hit that reduces a living target to zero HP with the deferred choice requested. The underlying attack produces a pending `MeleeAttackRecord`. Submitting the required `ResolveKnockout` through the owning seat then returns the adapter’s `Unavailable`, because that command is excluded.

I derived this sequence from the inspected admission and resolver paths; **I did not independently execute it or assert a particular die result**.

### Press has the same interface gap

The console defaults combat requests to `PressHitInstruction.ArmOrReplace`. A genuine hit can therefore arm Press. The existing movement procedure can subsequently create a legal Press offer when the target leaves reach.

The engine then requires `RespondPress`, but the session neither exposes that command nor projects the Press decision and responding actor. `ActingActor` recognizes only a pending ordinary opportunity or manufacturing quality choice before falling back to the regular actor.

The legal sequence is an actual Press-arming hit, followed by an actual target departure and any preceding ordinary opportunity resolution. The resulting Press offer cannot be answered through this adapter.

### Smallest required correction

Choose either bounded solution:

**Expose the existing continuations:** project their actual owner, decision identity and required context; permit the corresponding existing response commands under normal authority and resolver checks.

**Or keep them outside this session’s scope:** reject the triggering unsupported attack options **before commitment**, and make the console defaults consistent with that restriction. Do not silently rewrite a requested attack, automatically choose an outcome, erase pending state or require an unrestricted host command to escape it.

Supporting both continuations is not mandatory merely to close this finding. What is mandatory is that **an admitted public operation cannot leave the session dependent on an unavailable public response**.

Retain actual tests for the chosen boundary. If continuations are supported, exercise their real creation, correct-seat response, wrong-seat rejection, duplicate behavior and save/restore. If fenced, demonstrate unchanged rejection before payment, RNG or history changes.

## 2. B2 — human off-turn opportunity response lacks its required context

The view correctly determines the actual opportunity responder and gives that controlled actor the decision ID. But it exposes `TurnId` only when the seat controls the **regular-turn actor**:

```csharp
string turn = state.InventoryCombat
    && grant.Controls(state.Encounter.CurrentActor)
        ? state.Encounter.CurrentTurnId : "";
```

An ordinary opportunity responder commonly acts during someone else’s turn. In that case, the correct human seat receives the opportunity ID and acting actor but an empty turn token.

The console uses that view token when the caller does not supply one. The underlying response procedure requires the exact current turn ID even for an off-turn response; an empty token rejects as `InvalidOpportunityResponse`, which the session reports generically as unavailable.

The retained revision-113 witness does not test this path: its responder is the **automatic defender**, which obtains its context through the accepted trusted controller projection.

### Required correction

Expose the required current decision/turn context to the **actual authorized pending responder**, independently of regular-turn ownership. That does not require granting the responder control over the mover, exposing another seat’s private state or broadening target knowledge.

Demonstrate a real first-fight opportunity owned by a human seat during the other seat’s regular turn. The response must be constructible from that seat’s public view alone—not by reading the other seat, guessing the token or inspecting a snapshot. Include save/restore and unchanged wrong-seat rejection.

Preserve the engine’s actual response priority and current responder index. When correcting B1’s projection, do not label an outstanding knockout as an opportunity merely because a suspended move also exists.

## 3. Findings against the agreed session requirements

| Requirement | Focused disposition |
|---|---|
| **Selected profile and separate authority** | **Supported.** The ordinary accepted recipe-4 profile is constructed through public configuration. Party, first opponent, automatic defender and session operations have distinct grants. |
| **Permitted views and bounded inputs** | **Supported in the inspected scope, with B1/B2 outstanding.** Own information and actual tactical sight govern projection; ordinary rule denials are generic. The missing decision/context projections prevent complete public control. |
| **Input-driven connected gameplay** | **Supported for the recorded route.** Actual public inputs produce the acquisition, preparation, research, preservation, manufacturing, combat and ordinary continuation. This route does not exercise the blocked human continuations. |
| **Persistence and delivery** | **Supported for the exercised paths.** External restore validates before adoption, the actual automatic-defender opportunity continues after restore, and explicit backup recovery preserves evidence. Pending-choice coverage needs the corrections above. |
| **Responsiveness** | **Eight reference workloads meet their budgets. Broader P1 remains open.** The additional full-route costs cannot be described as uniformly responsive. |
| **Exact execution** | **Focused/build evidence supported; E1 pending.** The complete 1,481-case run has not yet been supplied. |

### Positive implementation findings

The four grants remain private. The broader buyer inventory permission is selected only for the exact companion sale or meal command and target, not arbitrary handling. The session retains normal current permission and duplicate processing in `Simulation.Execute`. Ordinary commands cannot use the trusted clock/closure entry point as a general world-modification channel.

`Restore` constructs and fully validates the replacement before `Adopt`. Explicit backup recovery similarly validates its candidate before replacing the live simulation. The focused test actually corrupts a primary file, confirms that failed restoration preserves the live revision, recovers the validated backup while preserving the displaced corrupt bytes, and resumes with normal duplicate handling.

The console is a real consumer of the public session API. It constructs ordinary commands, submits them through the selected seat and returns bounded responses; it does not expose a snapshot-editing or user-supplied-grant endpoint. The embedding local host remains responsible for binding seat and file-operation authority.

## 4. What the connected evidence establishes

The retained verification requires the actual selected gameplay facts, not just a final revision: two closed encounters, finite mining, one historical 2 cp sale, meal, episode close, returned charter, successful research, an Exceptional batch with six doses, one spent dose and three actual HP restored.

The recorded public route has **90 player, four first-opponent, 47 session clock/closure and 24 automatic-defender receipts**. Its resumed and console continuations reach the same final canonical digest:

```text
6f1bc7afa0f5727e76dccc26d0d33911682f791a3ca3e971ca1350c64dcdd521
```

The script restores the actual revision-113 interruption, rejects an encodable false-RNG history before adoption, checks a duplicate historical sale after restoration, and compares subsequent checkpoint files with the uninterrupted branch. It also restores an authentic ordinary MGT-04 wire95 predecessor without changing its bytes.

**This is substantial public-path evidence.** It does not prove that every exposed combat option has a usable continuation. The focused case mainly covers initial projections, delivery, authority and recovery, then ends after the first opponent’s stance; it does not cover either B1 branch or a human off-turn response.

The retained headless report records **one discovered, one passed, zero failed**. I am not counting its assertions or the 30 walkthrough repetitions as additional registered regression cases. Static validation records **18/18 passed, with 396 assets and 396 unique GUIDs**.

## 5. Responsiveness ruling

**The additional costs do not create a third correctness blocker for this bounded session adapter. They are concrete outstanding constraints on session-wide P1 responsiveness.**

The measurement code times actual C# submission through commitment and a permitted `View`, excluding script input construction and JSON presentation. It assigns thresholds only to the eight predeclared reference inputs. Therefore, the report’s `PASS` must be read as **those reference budgets passed**, not “every input on the route met an interactive budget.”

| Measured category | Recorded result | Disposition |
|---|---:|---|
| Highest named routine p95 | **68.004 ms / 150 ms** | Meets the existing reference gate |
| Stabilization p95 | **218.744 ms / 350 ms** | Meets the existing milestone gate |
| Opportunity p95 | **14.684 ms / 150 ms** | Meets the existing reference gate |
| Charter-plan submission, starting r66 | **1,192.519 ms p95** | Material routine-command cost; broader P1 unresolved |
| Three long work advances, starting r95/r97/r106 | **2,598.301–3,030.663 ms p95** | Material long-operation costs; no existing blanket exception |
| Full r113 restore | **5,957.889 ms** | Separately disclosed strict restoration cost, not charged to the routine live-command budget |

These figures and all 4,950 samples remain retained.

For the follow-up, the charter-plan submission’s prior-passage reconstruction needs targeted profiling and an equivalence-safe correction before it can support a session-wide routine-latency claim. The long advances need explicit classification and acceptance criteria based on their actual work; **the 350 ms exception for one measured stabilization command cannot silently become permission for every multi-second advance**.

A visible “working” state may improve presentation, but it does not by itself meet a command-cost budget. Any chunking, yielding, caching or validation change must preserve actual atomicity, due-event ordering, interruption, receipts and replay. No such change is authorized merely by this review.

The approximately six-second restore remains acceptable as a disclosed strict-load boundary under the existing contract. It still matters to overall usability and must remain visible. **Do not weaken external validation to hide it.**

## 6. Required return and remaining gate

Return the smallest correction for **B1 and B2**, with tests using the actual public C# and console inputs. No new gameplay rule or save schema is required.

The current full regression, when completed, belongs to this submitted implementation. It cannot substitute for regression against changed correction binaries. Retain it accurately, then bind the corrective source, assemblies, focused controls and completed affected/full execution to the corrected candidate.

**E1 remains pending. B1 and B2 are additional implementation holds, not evidence-count deficiencies.**

After actual acceptance, the previously agreed next work remains bounded EXP-03 finite receptacle/cache interaction and EXP-04 paid observation, followed by the selected EXP-05 local-travel/finite-site witness and the separately authorized MGT-06 trap composition. No new formal dependency chain or general route system is required. Those successor edits remain gated now.

## Inspection limits and final disposition

I inspected the session implementation and view, console adapter, focused case, relevant inherited attack/knockout/Press/opportunity handlers, connected verification and timing logic, evidence matrix, bindings, build/static result summaries and source-to-evidence comparison.

**I did not execute the DLLs or scripts, independently reproduce B1/B2, load the retained saves, recompute hashes, recalculate all 4,950 timing observations or audit every artifact byte.** The two defects are source-derived findings with concrete command paths. The successful executions and measurements are retained evidence reviewed here, not independently rerun results.

**Final disposition: hold `3c7b13728d13bfddbf47976220cd867652d4762d` for B1, B2 and E1.** Preserve the supported connected-route, authority, recovery and reference-timing findings above.

Prior engine and P1 validation-cost acceptances stand. Broader P1/INT-03 remains open, production authority is unchanged, and Unity gameplay integration stays deferred.
