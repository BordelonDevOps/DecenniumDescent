# Herbalism source and exact manuscript review

Actual notebook: [Calibration Review](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6a7a0fa2-eee0-83ea-92e9-6723a9f67ede). Source conference `c79c204e-c973-4340-a590-7aae79c1110c`, reply `cbbb06fe-f365-4437-8b62-69f6a8768980`; exact review `45dfe30e-6f5a-4efd-adaf-5fea18fbfd6f`, reply `63005e51-58e4-4bc4-a08e-e3841d6ba105`. The full [source conference](GPT_HERBALISM_SOURCE_CONFERENCE.txt) and [exact review](GPT_HERBALISM_EXACT_REVIEW.txt) are preserved.

The exact reply approves all 45 formulas once four finite repairs are applied. All are applied:

- Operational recipe tags use only explicit current mechanics.tag; original tags preserved separately.
- All cards require full maximum-Masterwork packaging/carrier reservation before the check.
- Timed application resolves at first instant both time and Action count complete, without an extra Action.
- Local Treatment prohibits a duplicate attempt per same actual Bleeding record.

Three explicit clarifications were also approved:

- Panacea actual-benefit entitlement with one concurrent attempt; no eligible cure does not block independent healing.
- Both Actions and elapsed time required.
- Open potency deadline applies to legal administration start, not completion.

The active recipe-tag array is named `operational.effect.recipeTags`; original source `tags` remain separately preserved as `sourceRecipeTags` and in full source evidence. This removes the operational/source ambiguity without discarding ingredient metadata.

The final [manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/HERBALISM_REVIEW_STATUS.json) pins all six artifacts. There are 29 public, three restricted and 13 Director-only formulas; all 29 public effects match their V5 book paragraphs. 43 source/projection checks pass and 19 protected source/prior-rule files remain byte-identical. This is authored operational review, not numerical balance, runtime execution, full-game approval or delivery. No source deletion or GitHub push; cosmology stays deferred.
