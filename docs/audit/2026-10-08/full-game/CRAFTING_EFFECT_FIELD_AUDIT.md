# Crafting effect-field source audit

Status: local source comparison only. The focused GPT conference is prepared but **not sent**. No formula, source text or reviewed operational rule was changed.

The audit indexes all **687 recipe identities across 16 trades** and binds all **433 public effects** to exact paragraphs in the V5 player crafting book. It inspects 1,268 selected numeric fields, distinguishing corresponding prose matches, omissions, prior decisions and fields not compared. This is a bounded comparison, not a complete semantic or playability review.

| Selected field result | Count |
|---|---:|
| Same number in the corresponding prose clause | 1057 |
| Zero-valued fields retained; no prose comparison performed | 146 |
| Source discrepancies already settled by recorded exact reviews | 7 |
| Positive data values with no corresponding prose benefit | 36 |
| Scribing use counts without a prose consumption rule | 22 |

## Unresolved source omissions

The 36 findings cover seven public, four restricted and 25 Director-only formulas. All retain the same effect and mechanics in the mechanical V4, full-internal V4 and V2 data. The seven public variants also match public runtime data and actual V5 book paragraphs. Thus these are preserved source disagreements; selecting a different copy does not resolve them.

| Trade | Field | Count | Exact recipe IDs |
|---|---|---:|---|
| Leatherworking | `armorBonus` | 11 | recipe-306, recipe-308, recipe-309, recipe-312, recipe-314, recipe-315, recipe-317, recipe-318, recipe-319, recipe-653, recipe-655 |
| Mining | `extraYield` | 13 | recipe-345, recipe-346, recipe-347, recipe-348, recipe-349, recipe-350, recipe-351, recipe-352, recipe-353, recipe-354, recipe-355, recipe-656, recipe-657 |
| Skinning | `extraYield` | 12 | recipe-532, recipe-533, recipe-534, recipe-535, recipe-536, recipe-537, recipe-538, recipe-539, recipe-540, recipe-541, recipe-676, recipe-679 |

Leatherworking has eight +1 and three +2 armorBonus values omitted from effects that describe mobility/handling benefits and, for some formulas, resistance. These are the same eleven findings already recorded in the Leatherworking conference preparation, not eleven additional cases.

Mining and Skinning contribute **25 additional findings**. Their data records extraYield: 1, while the prose grants +2 to the relevant check and one quality step on a successful harvest. Quality and quantity remain distinct. The audit neither grants a free extra unit nor deletes the data value. Higher-tier clauses that explicitly grant two additional units/parts on a critical success are not these omissions.

## Existing decisions remain in force

Alchemy recipes 11, 12 and 16 retain source attackBonus: 1, but their exact-reviewed operational effects give Strength-check and melee-damage bonuses with attackRollBonus: 0. Herbalism recipes 200, 220, 238 and 646 retain source numeric bonus fields, while their exact-reviewed operational effects use poison-save advantage and numericSaveBonus: 0. The audit verifies both review manifests, the artifact hashes and all seven actual operational projections. It does not reopen these decisions.

## Operational questions distinguished from numeric conflicts

- All 22 Scribing script formulas have uses: 1. Storing one spell or ritual describes capacity; it does not alone define consumption, activation or access. These 15 public and seven Director-only formulas need a source conference before a usable procedure can be authored.
- Eighteen Tinkering automatons use the field charges for the prose count of encounters before servicing. Matching those numbers does not turn them into per-activation charges or define encounter boundaries and servicing.
- Twenty-four Leatherworking containers grant secure/retrieve-check bonuses; five Tailoring containers grant conceal/organize-check bonuses. Both sets have matching capacity/bonus numbers, but their task scopes remain distinct. Neither number comparison resolves physical capacity, carried weight relief, nesting, Load or custody.
- Two Scribing reference records use languages: 1 for prose that grants one Language Insight. This is not automatically one learned language.

All unexamined mechanics keys are listed per recipe in the JSON report. Dice expressions, duration strings, resistance, triggers, targets, material tags and other text were not semantically adjudicated. Zero-valued fields were retained without a prose comparison. No matching number establishes action economy, eligibility, clocks, stacking, balance or runtime readiness. Existing cosmology-related labels are retained without interpretation; cosmology review remains after verified GitHub delivery.

## Evidence and reproducibility

- [Machine-readable comparison](CRAFTING_EFFECT_FIELD_AUDIT.json): every identity, selected field result, source-version evidence, public book paragraph binding and hash.
- [Prepared focused conference](CODEX_CRAFTING_EFFECT_CONFLICT_CONFERENCE_PREPARED.txt): actual relevant source text, full mechanics objects, unresolved questions and existing decision evidence. This is not a complete recipe-authoring packet and has not been sent.
- [Preparation status](CRAFTING_EFFECT_CONFLICT_CONFERENCE_STATUS.json): prepared packet hash, comparison controls and explicit no-promotion status.
- Reproduce with `DescentReviewChanges/ReviewBible/tools/audit_crafting_effect_fields.py`.

Six source controls pass. These check identity coverage, exact public book bindings, agreement among stored data variants, retained prior decisions and unchanged source/reviewed-artifact hashes. The comparison does not approve the unresolved findings. Current-pass totals remain 175 reviewed recipes, 512 remaining and 43 drafted Blacksmithing recipes awaiting an exact verdict.
