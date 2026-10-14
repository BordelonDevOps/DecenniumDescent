# Recovery review candidate — 8 October 2026

**Status: assembled procedure candidate with a complete Bard performance draft; other class mechanics incomplete.** This is the existing ReviewBible review workspace. Main remains the recovered approved V6 baseline.

## Ready to review

- [Gameplay procedures](docs/mechanics/GAMEPLAY_LOOP_CANON.md), recovered from the preserved V7.2 lab.
- [Level 1 quick reference](docs/mechanics/QUICKSTART_LEVEL_1.md) and its existing [Word edition](books/player/Decennium_Descent_Quickstart_Reference_v1.docx).
- [Gameplay data](data/public/Decennium_Descent_Gameplay_Loop_v1_2.json), with the extraction modifiers made explicit from the existing prose and helper. Runtime JSON matches it.
- [Class-source matrix](../../docs/audit/2026-10-08/ADVANCEMENT_MATRIX.md), covering all 17 classes and levels 1–20.
- [Advancement proposal](docs/mechanics/ADVANCEMENT_PLAYTEST_PROPOSAL.md), with explicit gates, class exceptions and a Bard example. The owner supports developing that Bard direction.
- [Bard playtest v0.1](docs/mechanics/BARD_PLAYTEST_v0_1.md): all 50 ability cards, three Hero paths, level 1–20 choices, original-source mapping and table-test log. New numbers remain provisional.
- [Recovered Director lore](../../docs/director-only/RECOVERED_THEME_ADDENDUM.md), with exact source paragraphs and both original books retained.

## What changed

The extraction formula now explicitly represents Attention +1, Burden +1, unsecured Volatile/Cursed/Living lots +1 each capped at +3, pursuit +2 and Secured route −2. Extraction Class/Attention/Burden/unsecured-lot contributions share the existing +7 cap; pursuit and route adjustments are outside that cap. Count a dangerous lot once even if it has more than one dangerous tag. No existing numeric coefficient was rebalanced.

The V7.2 helper and tracker were copied as a related unit for review. This does not certify the tracker or the whole companion app. It retains known follow-up issues: the tracker counts return progress downward while its extraction-cadence helper assumes forward progress; exit tests can repeat at unchanged progress. Use the written procedure when testing this candidate until those behaviors are repaired.

All earlier ReviewBible files replaced by this assembly are preserved under `_preserved/2026-10-08/pre-edit/DescentReviewChanges/ReviewBible` in the project root. Frozen incoming labs were not edited. See the [change ledger](../../docs/audit/2026-10-08/candidate_changes.json).

## Validation and limits

Run `python tools/validate_gameplay_loop.py` for existing structural and boundary checks. With Node 24 or a runtime that supports TypeScript stripping, run `node --no-warnings tools/validate_recovery_candidate.mjs` for extraction data/helper parity and hand-worked cap cases.

Passing these checks validates those specific procedures. It does not complete the 645 path entries, resolve the 140 draft level features, prove balance, inspect book layout, or validate every app workflow. See the [completion checklist](../../docs/audit/2026-10-08/READINESS.md).

Main and this ReviewBible both passed a non-incremental TypeScript check after recovery. See the [validation record](../../docs/audit/2026-10-08/VALIDATION.md) for coverage and limits.

## Bard validation and remaining integration

Run `node --no-warnings tools/validate_bard_playtest.mjs` with Node24 for the Bard's selection/resource/Echo/reset checks. [Results](docs/mechanics/BARD_PLAYTEST_VALIDATION.json) cover the 50-card schema, 27-feature example and 300 sampled legal build orders. The new helper is a reference implementation, not connected to saved characters. The guide records the existing RP-table mismatch and broader ordinary-spell/Dissonance reconciliation still required.

Pre-existing navigation/proposal documents modified for this follow-up were preserved under `_preserved/2026-10-08/bard-pass` in the project root. No original ability descriptions or approved Word books were deleted or overwritten.
