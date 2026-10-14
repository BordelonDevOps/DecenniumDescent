# Delivery inventory and preservation boundaries

Read-only checkpoint, 11 October 2026. This records files and existing repository history; final joint package selection and whole-game flow review remain open.

The [complete non-asset inventory](GITHUB_GAME_CONTENT_INVENTORY_2026-10-11.json) fingerprints **14,509 files / 1,278,532,411 bytes** outside `Descent assets` and the eight generated/dependency directory names listed in the report. Every enumerated file was read successfully, including Windows long paths. No file in this scoped inventory exceeds 100 MiB. These are checkpoint counts, not a final publication manifest. New audit files and subsequent edits require a final delivery manifest.

There are 4,067 groups of byte-identical files. Identical bytes do not establish obsolescence: a source book, historical snapshot and current candidate can have different roles. No duplicate was removed. The inventory retains all paths and fingerprints.

The [detailed boundary report](GITHUB_DELIVERY_CONTENT_BOUNDARIES_2026-10-11.json) verifies the clean delivery checkout against remote `main` at `57bb6d86e0e06d5e4f1e24a6e39a6a7ddb26a2cc`. Its tree has **109 file blobs and one repository pointer**. Compared with the recovered working root, 84 tracked files are byte-identical and 25 differ; none is missing at the same path. Those differences require reconciliation during assembly, with the existing Git history preserved.

The `DecenniumDescent` repository pointer names commit `a958d14f70c05a91f3779f680919167e5b9d01d1`, which exists locally and is an ancestor of the current delivery commit. There is no `.gitmodules` entry at that commit. Preserve the pointer and tracked cache until their roles are explicitly reconciled; do not silently remove them while copying the recovered tree.

The separate `Descent assets` workbench is absent from the current tracked repository. Its own README describes imported disc assets, and the existing game continuity notes keep those assets outside the product path. The earlier size inventory records 150,115 files / 26,082,997,108 bytes in that tree; this audit did not repeat a full asset-tree scan. Proposed delivery handling is to preserve it locally, account for it separately, and confer on the final package without copying the imported packs and bundled software into the game release by default. No files were deleted, and this is not a rights determination.

The main product literal-reference search found existing continuity/toolkit metadata only. Comparing four game banner files with 42 workbench images found no exact byte matches. Neither result establishes artwork ownership or proves a full build dependency boundary. The main README's License section contains a project description; this audit does not select a license. Rights/credits review remains open as its own ledger criterion.

Nine browser proof images are identified for separate local preservation and release screening because UI captures can contain unrelated sidebar information. Task-only text verdicts remain part of the review provenance; the word `BROWSER` in a filename alone is not an exclusion rule. Public and Director materials retain their audience labels. A Git package does not establish correct audience filtering in the companion application.

No authoring files were copied into the delivery checkout, no history was rewritten, and no commit or push was made. No cosmology text was interpreted or revised: its files were fingerprinted as opaque bytes. Follow the [owner-authorized delivery sequence](FINAL_FLOW_AND_GITHUB_DELIVERY.md): finish the authored candidate, obtain actual joint whole-game flow agreement, push and verify the remote commit, then review cosmology carefully.
