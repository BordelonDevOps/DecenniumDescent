# Recovery and consolidation audit

Date: 2026-10-08. Scope: the entire original `C:\Github\DecenniumDescent` folder. This report records the filesystem recovery and source reconciliation; it does not certify every rule or every imported asset as release-ready.

## What was preserved

The original folder contained **225,276 files, 27,420,695,264 bytes**. Of these, 10,430 files were classified as project content, 153,393 as imported/third-party assets and 61,453 as dependencies/generated output. Those classifications are for audit scope, not deletion approval.

All 225,276 inventoried files were found after consolidation with their original sizes. SHA-256 verification passed for all 10,430 project files. Asset and dependency bytes were not individually rehashed. No original file was deleted. The verification ran before the explicitly backed-up derivative repairs described below.

Project content had 4,664 distinct hashes; 3,740 duplicate groups accounted for 5,766 duplicate instances. Identical bytes establish duplication, not permission to delete a source with a useful provenance role.

All 219 DOCX/XLSX/ZIP packages (98 distinct packages) passed ZIP CRC integrity checks. Readable project content was extracted and indexed: 10,323 text records representing 4,598 distinct extracted texts. This is not equivalent to visually reviewing every page or reading every imported asset.

Evidence: [inventory](inventory.json), [project hashes](project_inventory.json), [duplicate groups](duplicates.json), [package checks](package_integrity.json), [verification](move_verification.json).

ZIP contents were also inspected: 6,811 file members across 12 archives. Fifty members (39 distinct contents) have no identical loose-file hash in the original project inventory. These include historical report/configuration variants and generated site artifacts; all archives remain preserved. See [archive contents](ARCHIVE_CONTENTS.md).

## Consolidation performed

The old outer root was an earlier July snapshot. The approved August working tree was buried at `Descent assets/DecenniumDescent-main`. The recovery:

1. Preserved the old outer root in `_preserved/2026-10-08/outer-root`.
2. Moved the actual working tree to `C:\Github\DecenniumDescent`.
3. Left the large independent imported-assets tree under `Descent assets`.
4. Verified all original files and project hashes.
5. Regenerated two stale `rulebook_output.txt` derivatives from the approved V6 DOCX, added a UTF-8 reference extract, and corrected absolute working-folder paths in the continuity protocol. Originals are under `_preserved/2026-10-08/pre-edit`.

There was no Git repository at the original target or nested working tree. Recovery relies on preserved files and the audit ledger, not an invented Git checkpoint. Preservation is on the same disk; it is not an independent off-device backup.

Evidence: [153 move operations](move_plan.json), [executed ledger](move_ledger.jsonl), [old-to-new path map](path_map.json), [derivative changes](reference_changes.json). Inventory paths and hashes describe the pre-recovery state; use the path map and later change records to resolve subsequent edits.

## Recovered authority

The [canon manifest](../../canon/CANON_MANIFEST.json) records owner-approved V6 promotion on 5 August 2026. V7, V7.1 and V7.2 are explicitly pending review. V7.2 is the latest completed calibration branch. Main, ReviewBible, incoming deliveries and historical snapshots therefore have different roles.

All manifest-authoritative paths were found. Current Player Rulebook V6 is byte-identical across main, ReviewBible, V6 and the V7.1/V7.2 labs. The July outer-root book differs. The extracted text files were stale across generations and were not reliable evidence of the approved book's contents.

Core Systems V2 owns combat, spellcasting, Gate scaling and economy. The Player Rulebook and class registries own class identities and paths. `src/data/feats.js` owns feats; generated books are outputs. Keep the 17 protected class engines distinct.

## Findings that change the work plan

| Finding | Evidence and disposition |
|---|---|
| Stale rulebook text | Confirmed and repaired with originals preserved. The actual approved DOCX contains no capitalized obsolete Fighter class. Its two spell-slot phrases explicitly explain that Resonance replaces slots. A wholesale Fighter/slot rewrite would have targeted old content. |
| Character advancement | Real unresolved integration work. Generic skill-point promises have no acquisition economy; class-specific structures differ. Druid, Oracle and Paladin must not be flattened into a uniform tree without review. Existing structured ability rules must be compared first. |
| Class runtime drift | Main class-details differs from the V6 delivery and V7.2. Main draft-level data still contains slot-era wording. Presence of a promoted book does not prove every companion module was updated. |
| Table usability | The book has vague effect sizes, percentage modifiers, cooldown language and tile references. Counts flag review candidates, not automatic defects: legitimate economic percentages must remain. |
| Curated Director lore | ReviewBible DM-01 has additions documented by its July theme-propagation changelog. Main and review are both preserved. A source-linked reconciliation is required, not newest-file overwrite. See [text diff](director_main_vs_review.diff.txt). |
| Public bestiary runtime | Main contains 707 full records; V6/lab public runtime contains 65 Known Descent records. This is a visibility/domain issue, not 642 missing monsters. Preserve full Director material and validate player-facing imports. |
| Gameplay calibration claims | Forced March for Unknown routes, rest-debt countdown, counterfeit handling, reputation access gates and cooldown reset limits already exist in V7.2. Earlier alleged omissions are disputed/stale harness findings. |
| Extraction parity | V7.2 prose specifies Burden, unsecured lots, pursuit and secured-route adjustments that are not all explicit in its JSON. Close representation parity without changing approved numeric intent. |
| Automated balance | Twenty packs completed, but encounter budgets and proxy combat assumptions remain provisional. The reported holdout signal does not establish human balance or fun. |

See [version hashes](version_matrix.json), [main/review comparison](review_main_comparison.json), [deep audit summary](deep_audit_summary.json).

## Known damaged or inaccessible historical material

Two preserved historical JSON files are truncated at 262,144 bytes: `archive/main-pre-v6-cutover-2026-08-05/src/bestiary_data_full.json` and `src/data/legacy/bestiary_data_full.truncated-262144.pre-v6-cutover.json`. The live bestiary parses. Do not use these truncated copies to regenerate it.

One pre-existing broken directory link was reported under the V7 playtest workspace's `docs/director-only/continuity`. It was not a newly lost file. Inventory covers accessible files; an inaccessible link's absent target cannot be reconstructed merely from the link.

## Collaboration record

The existing [Calibration Review notebook](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6a7a0fa2-eee0-83ea-92e9-6723a9f67ede) was consulted at the owner's request. GPT agreed to the V6/V7 distinction, preservation-first relocation and correction of stale findings after receiving on-disk evidence. Its new advancement ideas are proposals, not prior owner decisions. Neither model approved deletion of original material; none occurred.

The [review packet](director_review_packet.txt) gathers exact player-class, multiclass and Director-diff excerpts. It is Director-only working material and is not a player handout.

## Completion work after recovery

- Created a [Director-only addendum](../../director-only/RECOVERED_THEME_ADDENDUM.md) with the differing curated source passages and a two-way paragraph comparison. Both original Word books remain unchanged.
- Assembled the existing V7.2 gameplay procedures in the existing ReviewBible, then completed the extraction JSON fields to match its prose and helper. Eight hand-worked boundary cases and 672 JSON/helper combinations pass; public/runtime JSON match. The existing gameplay validator passes. This does not certify the full app or class rules.
- Extracted every class-level table and path list from main and V7.2. Main has 642 path entries, V7.2 has 645; both still merge 140 draft level features. The detailed [matrix](ADVANCEMENT_MATRIX.md) replaces assumptions that a complete operational ability registry existed.
- Main TypeScript check passed after excluding the newly adjacent preserved and imported-asset trees from compilation. This was a no-output, non-incremental check; no production deployment occurred.
- Added current navigation to the root README and a historical-status notice to the old July content-gap report. Originals are preserved. See [navigation changes](navigation_changes.json) and [candidate changes](candidate_changes.json).

GPT withdrew its first universal skill-point idea after the registry evidence. Its [revised feature-selection proposal](GPT_ADVANCEMENT_PROPOSAL.txt) remains a new design proposal. The owner has been asked which advancement direction to finish; the historical books have not been rewritten around that unanswered choice.
