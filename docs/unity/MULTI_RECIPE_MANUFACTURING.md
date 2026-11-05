# Multi-recipe manufacturing profile

## Scope

The shared manufacturing fixture can now admit Recipe 4, Recipe 14, or both. The two-recipe mode requires an explicit content manifest that supports each formula-research, copy, manufacturing, and produced-item operation. A manifest with only Recipe 4 rejects the two-recipe fixture; an unbound multi-recipe fixture cannot construct a simulation.

Each admitted recipe keeps its own formula selector, knowledge identity, component lot IDs, packaging lot, order `RecipeId`, source recipe definition, and dose provenance. A worker can have knowledge of one formula without the other. The apparatus still allows only one open manufacturing order at a time, so admitted recipes run sequentially over the existing shared clock and `WorkLedger`.

The default Recipe 4 fixture key and the single-Recipe 14 fixture key retain their prior serialized fingerprint inputs. The two-recipe profile uses a new explicit multi-recipe fingerprint. No record or snapshot schema fields were added; formula work, manufacturing orders, lots/reservations, trade history, doses, RNG, pending continuation, and command receipts remain the authoritative state.

## Runnable acceptance

`manufacturing_two_source_recipes_coexist_with_recipe_keyed_knowledge_stock_and_replay` constructs the trusted expansion manifest and one fixture with both source recipe IDs. It copies Recipe 4 and proves Recipe 14 is still unknown; an attempted Recipe 14 order is rejected without changing state. It copies Recipe 14, completes and settles Recipe 4, restores the world, then starts Recipe 14 from its separate lots and packaging. Recipe 14 reaches the shared eight-hour work boundary, retains completed labor, loses only the incomplete phase according to the existing interruption rule, saves/restores while paused, resumes, and settles. The test checks both recipe identities, outputs, retained catalysts, packaging balances, save bytes, and duplicate replay.

The same acceptance verifies that a legacy Recipe 4-only manifest cannot admit Recipe 14 and that multi-recipe content without a bound manifest is rejected. Existing single-recipe Recipe 4 and Recipe 14 cases remain part of the full suite.

## Boundaries

This is still a two-recipe TEST_ONLY fixture, not a general recipe authoring or acquisition system. Definitions are selected from the two currently source-bound profiles. It does not admit arbitrary recipes, generate manufacturing definitions from arbitrary source data, change trade-level crafting restrictions, or promote either profile to release content. The accepted Recipe 14 bulk divisibility and failure-recovery completion remains occurrence-scoped as recorded in [Recipe 14 decisions](MANUFACTURING_RECIPE14_RULE_DECISIONS.md).

No gameplay rule gap was introduced by allowing the two already admitted profiles to coexist. Existing source facts and the accepted Recipe 14 completion policy are unchanged.

Implementation and validation evidence: [multi-recipe checkpoint](evidence/2026-11-05-multi-recipe-manufacturing/README.md).
