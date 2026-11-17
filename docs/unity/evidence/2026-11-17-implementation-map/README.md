# Current implementation-map reconciliation

Subsequent planning update (2026-11-17): the [pre-Unity completion contract](../../PRE_UNITY_COMPLETION_CONTRACT.md) now specifies capability coverage and performance criteria, accepted by GPT/Codex ([actual review](../2026-11-17-pre-unity-contract/GPT_FINAL_REVIEW.json)). UR-01/UR-04 remain unqualified. The earlier findings below describe the preceding map review; the renderer/report now also validate the 100 criterion links. No implementation resumes.

Status: **documentation reconciliation accepted by GPT and Codex**. Actual response `d295363c-eda4-5830-8726-bc32efacdbf3` accepts candidate `1bcd551fee331c55da44e4d2969642fdaa2947d7` with one evidence-link closeout correction, now applied. No engine module is started by this work.

The owner asked Codex to confer with GPT and update the implementation map to show completed work and what remains before Unity, explicitly holding the next module. The implementation baseline is Engine `9f6db082990be8a96cc38a77863f93a4b2d38d93`, the final accepted TAC-10 record. Frozen C# remains `c8ffee78d5047131317ff923c8e3a575b6c51f3a`; qualified console host remains `3d0afc12d2444d2d6d77e3ff3729f2ff8236be3d`.

## Current deliverables

- [Readable implementation map](../../IMPLEMENTATION_MAP.md): accepted or implemented scope and concrete known remainder for every workstream, plus eight explicit pre-Unity gates and separately deferred Unity/product work.
- [Machine-readable status](../../IMPLEMENTATION_STATUS.json): all 49 original IDs, all 120 dependency edges and original acceptance criteria preserved exactly, with current status in separate fields.
- [Exact GPT consultation](GPT_CONSULTATION.json): actual response 2251212d-458d-5800-afe0-e9c7fa7e657a and Codex disposition. GPT reviewed the documents/graph only; no runtime execution or repository write is attributed to it.
- [Pinned baseline evidence index](BASELINE_SOURCE_INDEX.json): exact Git blob/length/SHA256 bindings for the 87 referenced baseline documents/evidence records. Accepted source/evidence revisions and exclusions remain in their original records.
- [Reproducible renderer/validator](Update-ImplementationMap.py) and [actual documentation checks](VALIDATION.json).

The first consultation attempt showed a connector service error without a new verdict. A retry produced the retained actual response. The final thread observation still carried a systemError flag; that flag is not treated as acceptance or rejection. Only the exact actual response supports the consultation findings. The actual final review is retained in [GPT_FINAL_MAP_REVIEW.json](GPT_FINAL_MAP_REVIEW.json), including the complete request/response turn and Codex agreement. GPT compared all 49 IDs/titles, 120 edges and 49 original criteria, reproduced the rendered Markdown and checked the three reported digests, and inspected selected acceptance records. It did not rerun Codex's full source/link validator or execute gameplay. Its only closeout correction changes MGT-04's recipe347 link to the accepted correction packet at 381942726e470d283fad16dfb061f792da184b56. The capability summary, original graph and runtime remain unchanged.

## Findings and scope

The historical map has stale NOT PORTED labels for later accepted repertoire/casting/creature work, stale test totals, and a stale two-recipe summary despite the named recipe347 integration. Current fields reconcile these without editing historical acceptance artifacts. The current map has three established technical baselines, one support fixture row, 38 partial workstreams, six rows with no accepted runtime identified in the reviewed map/evidence, and one mixed C#/later-Unity row. These counts describe unequal workstreams, not a completion percentage; no whole workstream is newly accepted by this document.

The accepted connected minimum and all exact bounded module acceptances remain closed. Broader C# coverage, independent required interactions, supported-profile expansion, responsiveness/scaling and a final whole-engine completion review remain. The finite required coverage/content envelope and operating envelope are not yet complete signed-off contracts. The map exposes those planning gaps rather than inventing a percentage, shrinking the full goal to the current loop, or requiring every catalogue identity to execute without source authority.

The owner's existing Codex/GPT rule-completion delegation remains applicable. Routine source/technical questions are addressed through that process; material product-scope reductions and production promotion require actual owner direction. This documentation review grants neither.

The known held next gate remains the complete amended Consecrate/Consecrated Ground source/API review, after the already accepted declared geometry and Ferry-Wraith prerequisites. Its settled decisions and formal CHR-05 dependencies are preserved. No contract preparation, runtime implementation, Unity integration, storage cleanup or Support work is performed in this task.

## Validation and limits

Run from the repository root:

```powershell
python -B -X utf8 docs/unity/evidence/2026-11-17-implementation-map/Update-ImplementationMap.py --write
python -B -X utf8 docs/unity/evidence/2026-11-17-implementation-map/Update-ImplementationMap.py
```

The validator checks 49 unique IDs, 120 exact edges, all 49 original criteria, an acyclic graph, current status completeness, real evidence paths, frozen baseline Git blob/size/hash bindings and rendered-map equality. It checks local documentation links, not remote website availability. It does not establish source-clause exhaustiveness, whole-domain coverage or new gameplay success. No C# build, test suite, gameplay command, save restore or Unity run is needed or claimed for these documentation-only changes.
