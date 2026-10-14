# Crafting history reconciliation

**The existing work is preserved: all 623 legacy recipe identities, names and effects are accounted for in the expanded 687-recipe catalog.** The expanded set adds four recipes to each of sixteen trades. The current 175 reviewed count describes the new operational manuscript pass; it does not mean only 175 recipes were previously written or approved.

The [August cutover record](../../../crafting/CRAFTING_V4_MAIN_CUTOVER_2026-08-05.md) and [canon manifest](../../../canon/CANON_MANIFEST.json) record the earlier owner-authorized release. This audit verifies local file contents; it does not reconstruct every prior GPT conversation or revoke earlier decisions.

## Verified source coverage

- 39 original source files were read without changes, grouped into 7 distinct byte contents.
- Five workbook copies are byte-identical. All 20 sheets were inspected: 16 recipe sheets, Dashboard, Recipe Template, Bestiary Cross-Reference and Validation Report. No hidden sheets, formulas or supplementary comment/external/drawing/VBA parts were found.
- All 623 workbook recipe rows map uniquely by trade and legacy name to retained IDs. The row-by-row map and field differences are preserved in the [machine-readable evidence](CRAFTING_HISTORY_RECONCILIATION.json).
- All 623 legacy names and effects are retained exactly in the V4 legacyName and legacyEffect fields. Older component definitions remain in the intact archive and workbook; these versions are not interchangeable.
- The live 433-recipe public JSON is exactly the public projection of the 687-recipe mechanical catalog. The other 254 identities remain present as restricted or Director-only records.

## Preserved differences

Workbook-to-legacy differences by field: `{"baseIngredients": 135, "monsterParts": 623}`. All of these component-field differences are names: ordered component counts, printed quantities and tier labels remain equal. The evidence records 59 observed name correspondences (14 base-ingredient names and 45 monster-part names), including Mithral ingot → Brightsteel Ingot. This is a textual correspondence, not a new ruling that differently named materials can be substituted in play. The workbook also retains its separate 50-row Bestiary Cross-Reference and validation notes; those are historical evidence, not current creature-stat approval.

The full internal V4 file has the same 687 identities but differs from the mechanical V4 in 21 tool-list records and eight component records. Every one of these differences is Focusing crystal/Crystal → Resonance lens/Lens; other fields in those mechanical records match. The exact changes are recorded in the evidence JSON. V2 also retains different publication/access metadata and Director guidance. All variants remain intact; this comparison makes no cosmology ruling.

## Counts by trade

| Trade | Legacy/workbook | Expanded | Public | Reviewed this pass | Draft this pass |
|---|---:|---:|---:|---:|---:|
| Alchemy | 41 | 45 | 27 | 45 | 0 |
| Blacksmithing | 39 | 43 | 27 | 0 | 43 |
| Cooking | 40 | 44 | 30 | 44 | 0 |
| Enchanting | 39 | 43 | 25 | 0 | 0 |
| Fishing | 40 | 44 | 28 | 0 | 0 |
| Herbalism | 41 | 45 | 29 | 45 | 0 |
| Jewelcrafting | 39 | 43 | 26 | 0 | 0 |
| Leatherworking | 40 | 44 | 30 | 0 | 0 |
| Mining | 39 | 43 | 29 | 0 | 0 |
| Poisoncrafting | 37 | 41 | 25 | 41 | 0 |
| Rune Carving | 37 | 41 | 21 | 0 | 0 |
| Salvaging | 38 | 42 | 25 | 0 | 0 |
| Scribing | 36 | 40 | 28 | 0 | 0 |
| Skinning | 39 | 43 | 28 | 0 | 0 |
| Tailoring | 39 | 43 | 29 | 0 | 0 |
| Tinkering | 39 | 43 | 26 | 0 | 0 |

The 43 Blacksmithing drafts have source/interface decisions and local validation, but no completed exact-manuscript verdict. Calibration Review reached its conversation-length limit. Its attempted exact submission is preserved; a replacement review chat awaits owner authorization. See the [prepared handoff](GPT_REVIEW_CONTINUATION_HANDOFF.md).

Validation: 15 checks passed. No original workbook, recipe source or prior reviewed rule was edited. No file was deleted. GitHub delivery and the careful post-push cosmology review remain pending.
