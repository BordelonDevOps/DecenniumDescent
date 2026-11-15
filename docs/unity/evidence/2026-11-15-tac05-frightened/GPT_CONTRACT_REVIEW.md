# Actual TAC-05 Frightened contract review

Actual response `226d668a-fd32-51b3-b64c-bbd74b67e64c`; request turn `86e1519a-35f4-4d65-b42d-ff4fb451353c` in [Unity Rules Engine Development Part 2](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af8ba86-20cc-83e9-bed0-c2d616fefcdf). Reviewed corrected contract commit `278c94163f980572b7a68b611c75aaaf70691f5e` following proposal `76c6c500e7b92720b66a515728ec45fcff3cf9ae`.

## Actual GPT response

**I approve the bounded TAC-05 implementation attempt, with two required contract amendments and the timing/geometry clarifications below.** This decision applies to the [corrected contract at `278c941`](https://github.com/BordelonDevOps/DecenniumDescent/blob/278c94163f980572b7a68b611c75aaaf70691f5e/docs/unity/evidence/2026-11-15-tac05-frightened/SOURCE_API_CONTRACT.md) together with this review. It is not runtime acceptance.

1. **Source access and revision-0 provenance: approved.**

   The initializer correction is correct: `Initial()` calls `InitializeLaterEncounter(s)` before returning. The defender already exists; encounter entry is a separate event.

   Approve one source-bound `TestOnlyFixtureEntitlement` and permanent STR choice at revision 0 in the explicit wire107/base90 profile. Keep the exception restricted to that profile, actor and card. This establishes neither earned acquisition nor a complete Warrior build. Preserve the existing Cleric/repertoire/RP state.

   The selected operational card and Warrior DC rule support **DC10**, using `8 + PB2 + STR modifier0`.

2. **Activation context: approved with a required targeting amendment.**

   The reinforced-encounter restriction, actual own-slot Action payment, canonical target ordering, initial saves followed by immunity prevention, atomic settlement and explicit unsupported hearing-only branch are approved.

   **The contract currently omits a separate shared targeting requirement.** The pinned [common class rules](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md#targets-concentration-and-control) require the user to perceive each selected target and have line of effect. `CanSee(target, user)` establishes only the card’s target-side visual predicate.

   For this admitted visual branch, preflight every target with **both** `CanSee(target, user)` and `CanSee(user, target)`, plus authoritative `LineOfEffectClear(user, target)` and range. Sight is directional, and the baseline explicitly separates sight blockers from effect blockers. Reject before payment or RNG when any required predicate fails. Unimplemented alternative perception remains explicitly unsupported; this does not rewrite the source’s see-OR-hear clause.

3. **Timing and geometry: approved with these binding clarifications.**

   Preserve the captured target-owned future regular-end marker and exact time across closure, retreat and reindexing. Resolve the repeat save **before end-phase expiry**, including while suppressed. Success ends that application; failure continues the same application until the final endpoint six seconds later. Do not expire it first and then recreate it: the baseline condition presence check excludes an application at its expiry marker.

   Recharge must use the actual owning calendar through `WorldTiming.ForActor`, with correct epoch-local markers and global conversions. The existing `SharedCharacterAdvancement.RegularStart` uses the original `WorldSchedule` roster and would reject this defender; merely attaching its existing runtime record is insufficient. Generalize that cadence while preserving Soldier behavior and old serialization.

   Approve exact rational Chebyshev distance and checking the entire willing path against every operative feared entity, including unseen ones. Assess **the affected actor’s own displacement**, re-evaluating authoritative positions as either actor moves. Source movement toward the target must not turn stationary or lawful retreating behavior into a violation; source movement away must not conceal an otherwise prohibited approach. Preserve exact suspension boundaries, paid progress and the distinction between authoritative forced movement and willing movement.

4. **Lifecycle, cure boundary and acceptance: approved with a required replay amendment.**

   Approve the versioned shared relationship lifecycle, unchanged legacy 14-kind policy, independent applications, continuing suppression clocks and internal source-qualified cure of all present eligible records—including suppressed records—while preserving protected and unrelated records. No unrestricted public cure is authorized.

   The consumer audit matrix, genuine connected application/attack/check/movement/end witnesses, labeled detached controls, authentic wire95–106 continuation, all 1,509 predecessors and full build/static/evidence requirements remain mandatory.

   **Restore independent receipt replay explicitly.** Section 6 currently substitutes uninterrupted/restored typed execution for the established four paths. Require uninterrupted console, restored console, receipt replay and independent typed dispatch at byte-identical checkpoints. Retain restored typed execution as an additional control.

My independent checks covered the corrected contract, selected gameplay source and relevant baseline code. I verified all **53 bound files’ Git blob identities, byte lengths and SHA-256 hashes**, all **three selected canonical records**, the six-file correction diff, unchanged engine, and the prior aggregate’s exact ordered 1,509-name inventory. I inspected `Verify-Audit.py` and its recorded 31 PASS checks; **I did not run that verifier, compilation, regression or gameplay.**

Record these amendments and clarifications with Codex agreement before implementation. No additional design blocker remains for the bounded attempt under those terms. After actual TAC-05 implementation/evidence acceptance, return to the **complete CHR-03 contract review**. Its settled milestone, selected build, both genuine RP branches, atomic Detect Magic acquisition and post-closure Radiance context remain intact.

## Codex agreement and implementation boundary

Codex agrees with the approval, both mandatory amendments and every binding clarification. The amended SOURCE_API_CONTRACT.md requires both directional sight predicates and actual line of effect/range before any payment or RNG; alternative perception remains unsupported. Its four required independent paths are uninterrupted console, restored console, receipt replay and independent typed dispatch, with restored typed dispatch additional.

Preserve captured actual target-owned endpoints and process the repeat save before end-phase expiry without reapplication. Generalize recharge using WorldTiming.ForActor and epoch-local/global conversion instead of attaching a defender row to the original-calendar-only Soldier helper. Assess each affected actor's own displacement against current authoritative feared-entity positions, so simultaneous source motion neither creates a stationary/retreat violation nor masks prohibited approach. Keep exact suspension, paid progress and forced movement distinctions.

The exact revision0 fixture entitlement, STR/DC10, bounded reinforced visual activation, shared versioned relationships and internal all-eligible cure are approved for this implementation attempt. No additional design blocker remains under these terms; engine implementation may start after this record/amended contract is committed. Source audit approval is not runtime acceptance. Retain all required source/build/full regression/connected/save/replay evidence and obtain actual final GPT acceptance before the successor.

Reviewer scope is recorded exactly above: it independently rehashed all53 bound files and three selected records and inspected source/code/diffs/inventory, but did not run the31-check verifier or compilation/gameplay/regression. CHR-03 stays held until implemented TAC-05 is accepted, then returns to complete contract review with its settled decisions intact.

