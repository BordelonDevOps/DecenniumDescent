# TAC-05 conditional closure guidance

Implementation checkpoint: `f5800818bfadb7c51865c96a6058f9af2deb75a3`.
Actual review chat: [Unity Rules Engine Development Part 2](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af8ba86-20cc-83e9-bed0-c2d616fefcdf).
Request turn: `b2555a3b-56eb-4d2d-87ca-11650c384c8d`. Actual GPT response: `bd6e3553-7534-5fdb-9883-e2426d85c097`.

## Actual GPT response

**Approve a narrow scope exception: the still-present-fear-across-normal-closure connected witness may remain un demonstrated without blocking this bounded TAC-05 review.** Record it as **“not demonstrated; reviewed scope exception,”** not as passed or proven unreachable. Further speculative route searching is not required.

The reported fourth-use branch does not establish a continuation that satisfies it:

- At revision206, the defender is alive at 0 HP. The existing `ResolvedConflict` check correctly rejects closure.
- Closing advances the hero’s outgoing slot. At the first relevant end, the repeat save either ends the relationship or preserves it until the following hero-end deadline. A closure on that following turn processes final expiry before returning its completed state. Fear immediately before the command therefore does not establish fear after closure.
- Another paid attack against an unconscious defender can add death failures, but dropping it from positive HP adds none; one subsequent critical hit adds two, not an automatic kill. The controller also ends after Presence spends its Action, so its current tactic supplies no post-use movement shortcut for an opportunity attack. [Closure implementation](https://github.com/BordelonDevOps/DecenniumDescent/blob/f5800818bfadb7c51865c96a6058f9af2deb75a3/engine/com.decennium.foundation/Laboratory/Model/SharedWorldCombatPolicy.cs#L384) · [Life resolution](https://github.com/BordelonDevOps/DecenniumDescent/blob/f5800818bfadb7c51865c96a6058f9af2deb75a3/engine/com.decennium.foundation/Laboratory/Model/PlaytestLife.cs#L127)

This is not a universal impossibility finding. Different genuinely accumulated life histories might change the outcome, but I have no demonstrated public-host sequence to prescribe. The `ClericGuard` naming disclosure is sufficient: its actual Aggressive command controls the evidence.

For final acceptance, retain the genuine connected routes and the fourth-use attempt through its unchanged closure denial. Replace **only this conditional connected intersection** with a clearly labeled detached control exercising the **actual shared closure path**:

1. Use an explicitly documented detached setup with a dead source, a present relationship and its retained calendar/endpoints.
2. Execute `EndFixedEncounter` and its normal outgoing-slot processing. Show that a failed due repeat preserves the same application after closure, without refreshing its deadline.
3. Show that reaching the final endpoint during closure or subsequent ordinary clock advancement expires it normally, without another save.

Your existing [clock study](https://github.com/BordelonDevOps/DecenniumDescent/blob/f5800818bfadb7c51865c96a6058f9af2deb75a3/docs/unity/evidence/2026-11-15-tac05-frightened/development-checkpoint/clock-components.json) explicitly constructs an outside-combat envelope; it supports clock behavior but does not itself exercise the closure transition. The additional control can use the frozen assemblies through an external harness. Keep its constructed state and detached status explicit; it establishes no connected acquisition or defeat history.

I inspected the relevant checkpoint source and reports and independently verified all **41 manifest source entries and 17 retained-report hashes**. I did not execute the engine, reproduce the fourth branch, or rerun the reported tests.

Record this disposition with Codex agreement and continue completing the evidence packet. **Final TAC-05 acceptance still requires the completed regression, consumer audit, compatibility and retained-evidence review. CHR-03 remains held.**

## Codex agreement and remaining work

Codex agrees. The conditional connected intersection is **not demonstrated; reviewed scope exception**. The genuine connected routes remain required; this disposition neither asserts universal unreachability nor grants source, death, closure or timing changes. Retain the fourth-use actual branch and unchanged closure denial, and add an explicitly detached control of the actual shared `EndFixedEncounter` path using a dead source and retained target calendar/endpoints. Demonstrate failed due repeat preserving the same application after closure and normal final expiry during closure or subsequent ordinary advancement without a third save. The existing outside-envelope clock study does not substitute for this transition control.

The frozen checkpoint assemblies may run the external harness. Full regression, final consumer audit, compatibility evidence retention and actual final GPT review remain required. TAC-05 is not accepted; CHR-03 is held; Unity integration remains deferred.

