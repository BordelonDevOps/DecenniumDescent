# EX58-EDIT-01 — Five source offices

**FINAL controlling addendum to EX58-SOURCE-2026-10-11.** One source-conformity correction, represented in two package locations. No other EX58 decision is reopened; no exact candidate is approved.

## Controlling source and disposition

KEEP FL-02. Frozen `DescentReviewChanges/ReviewBible/docs/mechanics/GAMEPLAY_LOOP_CANON.md`, §3, lines 101–109, lists **Expedition Leader, Quartermaster, Routekeeper, Surgeon, and Claimant of Record**. It permits one character to hold more than one office and states that no office changes class abilities. [Verified source excerpt](EX58_EDIT_01_SOURCE_EXCERPT.md).

The EC-01 office enumeration was my transcription error. **Lorekeeper is not one of these five offices.** Remove it from this current contract enumeration, restore Surgeon and Claimant of Record, and use the full source title Expedition Leader. Do not create a sixth office through “other source offices.” This is not NEW gameplay authoring and does not alter any office's source duties.

## Exact replacement field wording

> Expedition Leader, Quartermaster, Routekeeper, Surgeon, and Claimant of Record, each bound to a real person; one person may hold multiple offices but not incompatible simultaneous work.

## Exhaustive affected package representations

| Operation | File and exact location | Required change |
|---|---|---|
| EX58-EDIT-01.1 | `EX58_FIELD_CONTRACTS.json`, EC-01, `/contracts/0/requiredFields/offices`, submitted line 30 | Replace only this string with the wording above; require `/contracts/0/id == "EC-01"`. |
| EX58-EDIT-01.2 | `EX58_CONTRACTS_AND_EXACT_REVIEW.md`, “EC-01 — Expedition, charter and roster,” `offices` table row, submitted line 35 | Replace only the meaning cell with the identical wording. |

Original string, for exact-match application:

```text
Leader, Quartermaster, Routekeeper, Lorekeeper and other source offices bound to real people; one person may hold multiple offices but not incompatible simultaneous work.
```

Full replacement Markdown row:

```markdown
| `offices` | Expedition Leader, Quartermaster, Routekeeper, Surgeon, and Claimant of Record, each bound to a real person; one person may hold multiple offices but not incompatible simultaneous work. |
```

A search of all 17 payloads plus the original manifest found the erroneous enumeration in exactly these two locations. `EX58_AUTHORING_VERDICT.md` FL-02, `EX58_AUTHORING_REGISTER.json` FL-02, and the FL-02 wording in `EX58_CONFLICT_DISPOSITIONS.json` already retain the source's five named offices and require no replacement. All other representations and procedures stay unchanged. No unrelated use of an office-like name elsewhere in the project is renamed by this addendum.

## History and application

Preserve the original 439,330-byte package and all its entries unchanged: SHA-256 `98444b380e08aba6f3848cd2824245b52c8428e6a1b913907567dceeee04470e`. Its manifest, original receipt, source provenance, and 2,316-check report remain historical records, not rewritten reports for a corrected derivative. Apply the two replacements to the current authoring copy and record this addendum and measured descendant hashes separately.

`EX58_EDIT_01_CORRECTIONS.json` supplies both exact operations, parent-file hashes, and hashes expected from byte-minimal replacement. Those derivative hashes are in-memory reference calculations, not claims that the user's repository has been changed. No unrelated chapter or original source is regenerated here.

## Finite acceptance expectations

**EX58-EDIT-01-A1:** The corrected EC-01 field names exactly Expedition Leader, Quartermaster, Routekeeper, Surgeon, and Claimant of Record, with no Lorekeeper or open-ended additional-office grant.

**EX58-EDIT-01-A2:** The EC-01 JSON value and Markdown meaning cell contain the exact same replacement wording.

**EX58-EDIT-01-A3:** One person may hold multiple offices, but receives no extra simultaneous labor, skills, Actions, class abilities, or authority beyond FL-02. No requirement for five distinct characters is introduced.

**EX58-EDIT-01-A4:** All five source duties, FL-02, all other EX58 decisions, record fields, source values, and review boundaries remain unchanged.

**EX58-EDIT-01-A5:** Keep the original package, manifest, 2,316-check report, receipt, source hashes, and sources immutable. Record this correction and any measured descendant hashes separately; do not overwrite historical provenance.

The focused checks in this addendum verify the frozen source, affected representations, exact JSON/Markdown parity, and lossless two-field replacement. They are static/source checks, not gameplay or human testing, and do not rerun or broaden the historical 2,316-check conference.

**Author the candidate with these five source offices. No further source conference is required for this correction.** All other fulfilled scopes and EX58 exact-review requirements remain unchanged. The delivery sequence remains actual final joint whole-game flow agreement, the already-authorized GitHub push, verified remote commit, then careful cosmology review.
