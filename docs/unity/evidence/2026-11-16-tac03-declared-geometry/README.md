# TAC-03 shared declared-geometry source/API review packet

**Prepared proposal; actual review required before runtime.** Read [the complete contract](SOURCE_API_CONTRACT.md). This is the separate prerequisite selected by actual TAC-10 response `2d01541e-6b9d-54c0-88a7-0db0f65bc6af`, retained in the [preceding packet](../2026-11-16-tac10-undead-contract/SOURCE_API_DECISIONS.md).

The proposal reuses one persisted observation-backed map, shared destination terrain, exact movement/channel rules and existing actors in a fresh12x5 TEST_ONLY composition. It preserves authentic old saves and requires actual beyond-boundary ordinary/tactical travel, finite connected gameplay, save/restore, replay and final review. The complete contract specifies the authored cells, API dispositions and requested evidence allocation. No creature, seal, new encounter, production promotion or Unity work is included.

`Verify-SourceAudit.py` checks131 pinned Git blobs at their exact revisions, searches457 tracked C# files, and passes30 source/API assertions. Inventories contain12 fixed-floor files/15 lines,14 explicit-bound files/38 lines,49 spatial-consumer files/148 lines and52 profile/save-gate files/179 lines. These lexical inventories and assertions support review; they do not prove implementation completeness or playable behavior.

- [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json): revision, Git blob, byte count, SHA256 and checkout relation for every pinned source.
- [SOURCE_EXTRACTS.json](SOURCE_EXTRACTS.json): exact selected source documents and the authenticated accepted public-view observation.
- [API_CONSUMERS.json](API_CONSUMERS.json): reproducible search patterns and matching file/line evidence, including deferred legacy Unity rows.
- [SOURCE_AUDIT.json](SOURCE_AUDIT.json): actual source-audit results and explicit unexecuted runtime gates.

Reproduce from the repository root with `python -B -X utf8 docs/unity/evidence/2026-11-16-tac03-declared-geometry/Verify-SourceAudit.py`. During verifier authoring, the first run found a missing explicit `SharedWorldCombatPolicy.cs` pin and stopped before reports were written; the pin was added and the complete audit rerun successfully. No runtime failure or pass is inferred from that support-script correction.

Baseline `fd422433bb83b72bed88e6e62c98fe2c901c659b`; accepted engine `2733b9fd75e2159ad73312b9583311693b925598`; selected source `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`. Tracked engine diff against the accepted source is empty. No new C# compilation, static package qualification, gameplay, restore or regression execution was performed for this documentation-only packet. Existing Bishop1,570-case evidence remains its own accepted historical qualification.

Whole-engine completion, broader P1 and production authority remain open. Unity remains deferred. Storage cleanup and GitHub Support remain held.
