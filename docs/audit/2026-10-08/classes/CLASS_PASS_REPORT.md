# All-class playtest pass — 8 October 2026

The owner asked to extend the Bard treatment to every class and clarified that the 17 identities are **Base classes**, with **Arch and Hero afterwards**. The resulting draft library preserves that distinction.

Start with the [Base-class guide](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/BASE_CLASSES_START_HERE.md), then open the [complete library](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_INDEX.md). The library contains **17 class families and 1,223 operational cards**, including later paths and exceptional progression. Cards include action, cost, targets, duration, frequency, effect, level gate and original-source evidence.

## Delivered

- The existing 50-card Bard packet remains intact.
- Sixteen additional class packets cover the other Base families and their later progression, including Druid’s 24 named forms and seven Circles, Oracle’s ten Mysteries and ten Curses with 50 separately gated Boons, and Paladin’s ten Oaths with 50 Revelation spells and 30 inverted mechanics.
- [Shared test rules](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md) explicitly select the RP/strain configuration, action limits, healing/copy restrictions and class-level gates.
- [Legal build examples](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_BUILD_EXAMPLES.md) and a [session log](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_SESSION_LOG.md) support actual table testing.
- Class data and preserved sources remain available alongside the readable guides. New numerical completions are labelled provisional, not recovered canon.

## Collaboration and preservation

Codex supplied local book, registry and supplement evidence to the Calibration Review Chrome notebook. GPT authored and reviewed class material; the file-side pass checked source counts, class gates, protected interfaces, resource/action interactions and worked examples. Notebook answers are retained in this audit folder. The full adversarial review input is [preserved here](CODEX_ADVERSARIAL_REVIEW_PACKET.json).

The second Paladin response stopped partway through Noble Bearing. Its original text was preserved, 51 complete objects were recovered, and Codex explicitly authored the missing nine Martyr King cards from the supplied source objects. That completion was included in the final notebook review. An interrupted response was never counted as a complete package.

No original files were deleted. All eight main Word books still match the original audit hashes. Prior navigation/proposal documents were copied to `_preserved/2026-10-08/all-class-pass` before updates. Source descriptions, unused alternatives, old milestones and original notebook answers remain recoverable.

## Verification and limits

The [class validator](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_VALIDATION.json) passes 151 checks for source preservation, required fields, source references, stage gates, legal acquisitions and selected resource invariants. It samples 3,900 ordinary builds; the separate Bard validator passes its 300 sampled builds and reference mechanics. Exceptional progression checks cover 1,800 Oracle combinations, 70 Druid configurations and 120 Paladin configurations. These configuration checks are structural; they do not simulate every combat interaction.

The notebook’s [15 adversarial findings](GPT_ALL_CLASS_ADVERSARIAL_REVIEW.txt) were applied: Blood Mark eligibility, save timing, shared Stun ownership, Druid use counts, Echo archive/copy limits, Ranger expiry and unlock level, granted-action accounting, Tinker repair, path-specific Thief finales, Paladin transfer/Smite rules and Oracle’s exceptional ASI schedule. The [disposition](REVIEW_DISPOSITION.md) records each correction. File-side review also aligned Thief’s Poisoned condition with the actual Core V2 definition and made four shared level-20 grants explicit in card metadata.

The [delivery audit](CLASS_PASS_VALIDATION.json) records book hashes, navigation backups, local links and artifact hashes. Reproduction tools live under `DescentReviewChanges/ReviewBible/tools`: build the packets, validate them, then regenerate the readable build examples. The original Bard reference helper remains separate.

This completes the requested class-drafting scope. It does not certify numerical balance or publication readiness. Remaining game-wide work includes the complete ordinary-spell catalog, live companion/character-sheet integration, public/Director separation, campaign materials, human playtesting and final book production. Use the drafts for focused tests and record their failures before promoting numerical changes into approved books.
