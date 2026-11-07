# GPT implementation review — schema59 Map Route work/check

**Date:** 2026-11-07

**Reviewer:** Unity Rules Engine Development

**Review scope:** Codex-supplied source summary, implementation facts and regression behavior. GPT did not inspect the checkout or independently run tests.

## Verdict

GPT found **no concrete blocker** in the causal condition-history correction under the current append-only condition-journal and command-history model. It agreed that persisting the exact journal operation count at check resolution prevents later operations at the same clock timestamp from changing the historical check mode, dice or RNG consumption. Reconstructing the prefix and advancing it to the check timestamp preserves condition expiry ordering.

The earlier source review remains in scope: the stationary Map Route method, WIS (Survival) check binding and retry terms are adopted TEST_ONLY completion policy because the pinned Player Book does not fully specify them. Mapping knowledge does not establish Unknown-route passage feasibility.

## Review qualifications and Codex response

- The prefix count must satisfy `0 <= ConditionOperationCount <= current journal operation count`. The check-record constructor already enforced the lower bound and the global operation cap; schema59 state validation now also explicitly rejects a negative count before calling LINQ `Take`. `route_mapping_work_check_rejects_negative_condition_prefix` locks this down.
- Prefix shape and timestamp checks alone cannot prove when the count was captured. Canonical command replay regenerates the check and count from the causal command sequence and compares the encoded state; the same-time Poisoned regression verifies save/restore and replay.
- No history-truncation problem exists in the stated append-only model. Future journal compaction must retain or migrate the stored prefix reference.
- The new field changes the in-development schema59 binary layout. The pre-correction schema59 layout is not a supported save contract; schemas through 58 retain their existing codec branches.
- GPT found no source-bound conflict and no need for another gameplay decision or required regression before committing this bounded slice. This is an excerpt-based design review, not independent code execution.

## Validation reported by Codex

- Full headless C# 9 warnings-as-errors suite: **PASS, 1,225/1,225**.
- Focused negative-prefix regression: **PASS, 1/1**.
- Static package validation: **PASS, 18/18**, 265 assets and 265 unique GUIDs.

See [README.md](README.md) for all run reports and the [rule decision record](../../ROUTE_MAPPING_WORK_RULE_DECISIONS.md) for source and prototype boundaries.
