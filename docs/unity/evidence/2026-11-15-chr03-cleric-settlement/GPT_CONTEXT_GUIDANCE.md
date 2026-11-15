# Actual CHR-03 Radiance context guidance

Actual response `68898ea2-4ba8-52e5-afe9-ac081a2dbd12`; request turn `54d65719-c0e8-4bc4-8e2e-e34a67c075d1` in [Unity Rules Engine Development Part 2](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af8ba86-20cc-83e9-bed0-c2d616fefcdf). Inspected baseline: `459b8bf54ea46ecf45a0622ce99d5f18a77bd57f`.

## Actual GPT response

**Approve the proposed post-closure Healing Rite context and the separate RP-preserving branch for inclusion in the complete CHR-03 contract.** Record this as a **NEW bounded TEST_ONLY consensus admission**. Runtime implementation still requires review of that complete contract.

Healing Rite’s printed Action/2-RP cost permits finite use without an express encounter restriction. Radiance’s “on each of your turns” needs the explicit calendar interpretation proposed here. The adopted calendar already supports continuing ordinary Action intervals outside tactical mode. [Cleric source](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json) · [Adopted calendar policy](https://github.com/BordelonDevOps/DecenniumDescent/blob/459b8bf54ea46ecf45a0622ce99d5f18a77bd57f/docs/unity/SHARED_WORLD_RULE_DECISIONS.md)

Carry these precise boundaries into the contract:

1. **Admit the context only after genuine closure and lawful advancement.** The new profile may execute the owned Healing Rite during the Cleric’s actual current calendar slot, using its existing unspent Action. Retain authority, revision, living-allied-target, stationary position, range, sight, line-of-effect, bodily capability, busy-state, pending-choice and supported-interaction checks.

2. **Use the actor’s retained calendar, with the correct marker identity.** Resolve it through `WorldTiming.ForActor`. Closure clears `Encounter`; `ForEncounter` then falls back to the original calendar. Neither is suitable for identifying this post-closure Cleric turn. Bind Radiance cadence to the actor, owning epoch and actual local regular-start marker. Account explicitly for the reinforcement ledger’s globally numbered `LastStart`; do not interpret that value as an epoch-local ordinal.

3. **Preserve spending and event order.** All due boundary consequences resolve before voluntary activation. Advancement and activation grant no fresh Action or Radiance allowance. The Rite spends one existing Action and 2 RP, uses shared RNG, and adds no elapsed time itself. Reaching another slot requires ordinary world advancement or movement. Pause, restore and mode changes cannot refresh or bank uses. This admission applies specifically to this Healing Rite/Radiance context.

4. **Demonstrate actual Radiance healing.** Resolve the base Rite first; it must actually restore HP before Radiance triggers. Apply the additional `S=1` through shared healing limits to its healed beneficiary, with the source-faithful optional cure and persisted once-per-turn settlement. The positive witness must leave recoverable HP after the base heal so the extra point actually lands. A capped bonus does not independently invalidate an otherwise eligible cure; a base Rite restoring zero HP supplies no trigger.

Both connected branches remain required:

| Branch | Before advancement | After advancement | Subsequent witness |
|---|---:|---:|---|
| Primary depletion | RP 1/3 | RP 1/4 | No recovery; another 2-RP Rite remains unaffordable |
| Active Radiance | RP 3/3 | RP 3/4 | Actual Rite pays 2 RP, leaving 1/4; positive Radiance healing |

The alternate branch must preserve genuine combat injury and earn the same announced objective. Retain save/replay, paid continuation, wrong-slot and spent-Action denials, cadence-forgery controls, and no-refresh checks. A third encounter is unnecessary.

I inspected the pinned cards and timing rules, current Healing Rite code, closure handling and retained-calendar helpers; a separate static review agreed. No runtime execution occurred. **All other settlement obligations remain in force, and complete-contract review still precedes implementation.**

## Codex agreement

Codex agrees with the exact new bounded TEST_ONLY consensus admission and both genuine connected branches. Use `WorldTiming.ForActor`, the owning epoch and actual local current/regular-start marker; verify the separately global reinforcement interval number. Never use a cleared Encounter or the fallback original calendar to invent a Cleric turn. Keep all costs, due-event order, no-refresh behavior and source/physical/authority checks. This is context guidance for the complete contract, not runtime implementation approval. The complete contract still requires actual review and agreement before engine changes.
