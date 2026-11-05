# Alchemy recipe 14 manufacturing decisions

## Source-backed definition

The pinned reviewed playtest card defines **Recipe 14, Stabilizing Salts** as a Tier 3 Common Alchemy recipe. It requires Alchemy 5, a DC 11 check, knowledge of the formula, four hours of active work, and produces four standard doses. The process uses five 0.05 lb lots of stabilizing salts, two 0.50 lb lots of distilled spirits, and one 0.38 lb black-blood sample. It uses no source vials: standard yield requires four supplementary glass vials, and masterwork yield requires six. The operational dose effect is `2d4+2` healing.

The card gives the first stabilization phase as 15 minutes. The remaining 3 hours 45 minutes is the recipe's four-hour total. Exceptional yield of five is derived from the established 25% quality yield rule; masterwork yield of six is the established 50% rule. The recipe card directly specifies four standard and six masterwork supplementary vials. A five-dose exceptional batch therefore consumes five of the reserved vials.

The source lists zero minimum research hours. The existing shared formula workflow still enforces its eight-hour minimum; copying a supplied legible formula uses the existing one-hour copy procedure. Formula knowledge is stored for the exact recipe identity and does not grant knowledge of recipe 4.

## Accepted prototype completion

The source does not define whether these exact source occurrences can be divided. Material role, category, and mass do not settle divisibility. Under the Codex/GPT consensus, only Recipe 14's five stabilizing-salts units and two distilled-spirits units are treated as measurable loose bulk, divisible to 0.01 of their source quantity unit. The one black-blood occurrence is a catalyst and is indivisible. This declaration is limited to the Recipe 14 occurrences in this profile. It does not establish a default for any material category or other recipe.

On an ordinary `Failed` result, one quarter of each declared divisible bulk input is recovered, rounded down to 0.01 source unit. The resulting quantities are 1.25 salts (0.0625 lb), 0.50 spirits (0.25 lb), and zero black blood. Mishap settlement continues to consume its inputs through the existing shared crafting consequence path. Masterwork catalyst retention uses the existing choice and settlement path.

The recipe reserves supplementary vials before work. At settlement it consumes only the quantity required by the produced batch and releases unused reserved vials. Vials are packaging, not fractional ingredient recovery. The output is created as separate ordinary doses and uses the existing tactical dose action, shared RNG, healing, and life-state resolution.

## Implementation boundary

Recipe 14 is an opt-in `TEST_ONLY` content profile. Recipe 4 remains the default profile, with its pre-existing fixture key and behavior unchanged. A test world selects one recipe profile at construction; recipe 4 and recipe 14 are not yet available together in a single world. The source manifest and manufacturing fingerprint distinguish the recipe-14 profile, exact source occurrences, and the 0.01 bulk declaration.

No snapshot schema field was added. Existing manufacturing order, work ledger, resource reservation, formula work, dose, trade, RNG, command receipt, and save/restore records remain authoritative. The widened supplementary-vial record limit is checked against the selected recipe profile, so recipe 4 continues to accept only its existing range.

This is a prototype implementation decision, not a claim that Recipe 14 or its divisibility policy is release-approved or canonically promoted. Recipe acquisition, a general recipe registry, multiple recipes in one world, authored recipe import, category-wide quantity semantics, and release content authority remain out of scope.

## Pinned inputs

- Candidate recipe data: `DescentReviewChanges/ReviewBible/data/playtest/alchemy_recipe_candidate.json`, Git blob `67d2bbc5ead75f331a2c99f41a75941f03fe431f` at source commit `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.
- Public recipe card: `DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md`, blob `a71c2e54ad86a8b35377323f16a9f4ff7df986e0`.
- Recipe playtest rules: `DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md`, blob `a253486adc64daaaa9d105f8911dcd267c971e06`.
- Shared crafting material identity and consumption rules: `DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md`, blob `b2c15e1bd56bb62e0f1729f4f6d68413e62f9be9`.
- Recipe review catalog: `DescentReviewChanges/ReviewBible/data/director/crafting_recipe_review_catalog.json`, blob `8d4acc4a13d42ff299b19116f6e70a34e79f2c6d`.
- Authority route: `docs/canon/CANON_MANIFEST.json`, blob `003b9c45d3b36be43a16c431fe341de725f7f406`.

The complete delegated consensus, exact acceptance cases, validation output, and source/code hashes are recorded in [Recipe 14 implementation evidence](evidence/2026-11-05-manufacturing-recipe14/README.md).
