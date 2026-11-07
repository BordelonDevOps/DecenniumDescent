# Route mapping result ledger — schema54 evidence

This increment persists synthetic pre-resolved Map Route result accounting under schema54. It does not execute Map Route checks or establish actual reconnaissance/traverse feasibility. Its profile, evidence and behavior remain TEST_ONLY.

## Responsibilities and acceptance

The records retain directed route/result/actor identity, command receipt, operation/evidence identity, profile fingerprint, completion time, result degree, and before/after Mapping and mark counts. Knowledge derives from the route's immutable initial Mapping plus append-only records. Query and resolver use the same assessment. No second clock, RNG draw, inventory effect, or route-quality/Risk/geometry mutation is introduced.

Focused cases included in the full suite:

- `route_mapping_results_persist_without_claiming_a_check_or_passage`: Risk-2 success, retained mark, save/restore, second distinct success, duplicate/unknown/future/wrong-actor rejection, unchanged unrelated state, and canonical replay.
- `route_mapping_surplus_waits_for_a_distinct_success_and_does_not_survey`: one-level promotion with retained surplus, failure not activating it, later distinct success, immutable authored Unknown Mapping, and continued `RouteRequiresReconnaissance` rejection.

## Validation

- Full headless C# 9 warnings-as-errors suite: **PASS, 1,197/1,197**. Core, Persistence, LabModel and headless test sources compiled with PowerShell 7.6.9 / .NET 10.0.14.
- Static package validation: **PASS, 18/18 checks, 248 assets and 248 unique GUIDs**. This is structural package validation, not Unity import/compilation or a player build.
- `git diff --check`: **PASS**.
- The default `Validate-RuleBindings.ps1` audit was attempted and is retained as `STALE_RULE_BINDINGS_AUDIT.json`. It stops before evaluating bindings because the default Nov 5 headless evidence pins an older `ActorConditionRecord.cs` source hash. The historical binding manifest and its source snapshots were left unchanged; this is not current schema54 binding certification.
- GPT review: excerpt-based review found no concrete push-blocker; GPT did not inspect the checkout or run these checks. It recommended an authentic pre-change schema53 save regression for byte-identical re-encoding and replay as the highest-value optional follow-up. Fixture and record constructors validate result degree/mapping enums and mark ranges; the route fixture validates nonnegative Risk; `Apply` validates nonnegative Risk and defined result degree; state replay recomputes each transition from prior accepted knowledge.

The JSON reports contain exact timestamps and source hashes. The complete rules engine remains unfinished; actual Map Route method/DC/work/failure procedure and reconnaissance passage-feasibility producer are still gated.
