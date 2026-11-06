# Tactical Search query and discovery — 2026-11-06

## Scope and authority

This no-schema-change increment connects tactical Search to the existing public command-query and command-discovery APIs. `ObservationActionRecord` and observer-knowledge records remain authoritative for results and disclosure. Existing actor positions, authored observation profiles, encounter turn, Action interval, shared clock, RNG, transaction/receipt path, snapshot codec and replay retain their existing responsibilities. The query assesses public prerequisites only; it does not read hidden occupancy, concealed actor identities or the Hide roll total. Discovery lists all in-range authored cells in deterministic row-major order, including empty cells.

Search execution is unchanged. Search remains tactical Action-only; no exploration-time duration or new gameplay outcome was added. `SearchCandidateAmbiguous` remains defensive protection for invalid/unreachable duplicate occupancy under the current validated host, as reviewed with Unity Rules Engine Development.

## Validation

- Focused C# 9 warnings-as-errors case: **PASS 1/1**, [`FOCUSED_RESULTS.json`](FOCUSED_RESULTS.json).
- Full C# 9 warnings-as-errors suite: **PASS 1,178/1,178**, [`HEADLESS_RESULTS.json`](HEADLESS_RESULTS.json).
- Static package validation: **PASS 18/18 checks; 237 package assets and 237 unique GUIDs**, [`PACKAGE_RESULTS.json`](PACKAGE_RESULTS.json). This is static package validation, not Unity compilation or runtime validation.
- [`FAILED_COMPILE_RESULTS.json`](FAILED_COMPILE_RESULTS.json) records the first attempt's compile failure (`CS0246`, missing `System.Collections.Generic` for `IEnumerable<Command>`) and `0/0` cases. The missing import was added; the focused and full suites then passed.
- [`SOURCE_BINDINGS.json`](SOURCE_BINDINGS.json) lists changed-source SHA-256 hashes, report hashes and review status.

## GPT review

The authorized implementation packet, containing the changed excerpt and behavior description, was sent to **Unity Rules Engine Development**. GPT found no blocking defect in the submitted material and confirmed explicit Search routing, hidden-state-independent assessment, deterministic occupancy-independent discovery, Action cost and unchanged execution semantics. It recommended testing Search after the Action is spent, query-side upper-bound/out-of-range rejection, no admissible discovered option, and unchanged state after rejected execution. Those regressions were added to the same acceptance and rerun successfully. GPT did not independently run the local checks. No new rule or schema decision was needed.
