# Reviewed transport consolidation

The owner requested a repository file-necessity review with GPT and consultation before deleting unnecessary files. GPT and Codex agreed that the eight outbound review ZIPs enumerated in `TRANSPORT_MEMBER_INDEX.json` need not occupy active `Engine` HEAD. This record concerns repository housekeeping; EXP-07 acceptance, rule authority, engine completion and the development pause are unchanged.

The eight wrappers occupied 2,518,971,539 bytes. Every one of their 2,592 members is retained: existing Git/LFS objects preserve matching bytes, and `unique-transport-members.zip` preserves the 319 distinct unmatched members once. That bundle contains 75,592,983 uncompressed bytes in 9,632,438 bytes. The member index maps each original member to its exact retained bytes. The original outer ZIPs remain at the unchanged historical commit and `origin/main`; their bytes are not reconstructed by repacking this bundle.

## Necessary repository contents

- Keep all tracked `engine/` source, Lab, tests, fixtures, tools, metadata and existing host configuration. At the reviewed checkpoint this was 978 files totaling 13,536,611 bytes.
- Keep the canon registry, its registered authorities, reviewed source records and source bindings. Review material, TEST_ONLY content and production authority remain distinct.
- Keep accepted decisions, contracts, actual review receipts, compilation/source identity, authentic historical saves and deterministic replay/connected-scenario evidence.
- Keep received Director returns, sole source or evidence copies, and unresolved historical artifacts unless individually proven redundant. Directory age, a temporary name, or a ZIP hash alone does not settle necessity.
- The approved 28 cache removals are listed separately in `CACHE_REMOVALS.json`. All retained sources match their cached code objects; 17 held caches and three referenced temporary copies remain unchanged.

The repository had 787 unique LFS ZIP objects totaling 18,971,535,730 bytes at the reviewed checkpoint; 77 `CurrentSource` objects accounted for 6,856,896,717 bytes. This first batch reviews only the eight listed wrappers, not the other archives. Those figures describe stored review content, not the size of a finished game.

## Verification and review

`GPT_APPROVALS.json` records actual GPT decisions and their limits. GPT independently inspected the eight pinned delivery records; Codex performed the member hashing, source comparison, consumer search and restoration tests. GPT did not independently run those local checks.

`ARCHIVE_REFERENCES.json` records literal filename/hash references. No references were found in active engine, Unity development, application, or ordinary script/tool paths. Historical packaging and return-verification scripts do reference the removed ZIPs. They are unchanged and require restoration of their exact original archive before rerunning, along with whatever original source-revision requirements their own records specify. A `PREPARED_UNSENT` delivery label is not a claim that the package was never later used.

Run the retained-member check from the repository root:

```powershell
python -B docs/maintenance/2026-11-16-transport-consolidation/Verify-PreservedMembers.py --repo .
```

## Exact historical archive retrieval

Base commit: `85957982d45d3f76c6e5f3243ae6e10b46407b83`.

`Restore-HistoricalTransport.py` verifies the historical Git LFS pointer and original payload hash. It defaults to verification only. It refuses to overwrite an existing output and never repacks content or automatically downloads an entire history. All eight local original payloads were verified, one full 239,606,205-byte archive was restored and verified, and overwrite refusal was tested.

A fresh Engine checkout may not have these old LFS payloads locally. The unchanged `main`/historical references and remote LFS objects are the retrieval dependency; a local LFS cache is not a permanent independent archive. If necessary, fetch the exact historical Git revision, then fetch only the archive path from the index:

```powershell
git fetch origin 85957982d45d3f76c6e5f3243ae6e10b46407b83
git lfs fetch --include="EXACT_REPOSITORY_RELATIVE_ZIP_PATH_FROM_INDEX" --exclude= origin 85957982d45d3f76c6e5f3243ae6e10b46407b83
python -B docs/maintenance/2026-11-16-transport-consolidation/Restore-HistoricalTransport.py --repo . --archive EXACT_ZIP_BASENAME --write --output-root .
```

The helper restores the original repository-relative pathname beneath the chosen existing output root. Exact ignore entries prevent accidentally recommitting restored obsolete wrappers. Original outer ZIP hashes and receipt identities remain unchanged. Remote payloads were not redownloaded solely for this audit; local original bytes and historical/main pointers were verified.

## Storage boundary

This ordinary commit reduces active Engine checkout material by about 2.51 GB. It does **not** reclaim historical GitHub LFS storage: `main`, Git history and remote LFS objects remain unchanged. No history rewrite, purge, billing change, Unity integration or successor gameplay module is part of this cleanup. Before any future remote purge, preserve and test independent retrieval of exact original archives and all required provenance under a separately authorized plan.
