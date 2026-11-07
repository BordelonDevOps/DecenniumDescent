# Route mapping result ledger — prototype policy

**Status:** Delegated Codex/GPT completion for a bounded TEST_ONLY adapter. This policy is not verbatim source text, a completed Map Route procedure, or release approval.

## Responsibilities and authority

This increment persists an already-resolved synthetic mapping outcome against a directed route. It does not perform the check, charge labor, roll dice, establish reconnaissance, or establish that an Unknown route is traversable. A finite fingerprinted TEST_ONLY result fixture supplies the route, actor, evidence identity, completion timestamp and result degree. The command can consume that exact result once; its payload cannot claim a degree or fabricate evidence.

The authoritative physical route properties remain immutable fixture content. Per-route knowledge is derived from initial Mapping plus append-only `ExpeditionRouteMappingResultRecord` history. `ExpeditionRouteTravelRecord.StartingMapping` and its segment Progress are unchanged. The shared command receipt/revision, `RuleClock`, RNG, inventory, route records and `SnapshotCodec` remain authoritative; no second clock or global mutable map was added.

Schema54 appends mapping-result records after schema53 data. Schemas 1–53 retain their prior codec branches. Core validation rejects schema54 when `TestOnly` is false; the command exists only in the gated laboratory host. The route mapping fixture and every outcome are included in the TEST_ONLY content fingerprint.

## Pinned source and unresolved procedure

The source authority is `EX58-EXACT-2026-10-11`, pinned Player Book SHA-256 `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`, especially FL-02/03/10/11 and TR-13, with `GAMEPLAY_LOOP_CANON.md` §§2/8, `CORE_RESOLUTION_PLAYTEST.md`, corrected EX58 FL-10 disposition, EX02-08, and the candidate-only EC-05 record contract. See [the clause trace](ROUTE_DISCOVERY_RULE_TRACE.md).

The generic sources supply up to three meaningful trained assistants at +1 each; a generic Watch task of 480 actual active minutes before its completion check, carrying feasible unfinished work forward; a lead/approach/relevant-skill/team-check shape against a route or tier DC; and four task degrees with natural shifts. They do not fully specify Map Route's method or approach, route-versus-tier DC selection, failure/retry consequence, completion linkage, or whether/how 480 active work minutes compose with 480 nominal travel minutes. None of these gaps is filled by borrowing FL-11 Forced March.

## Delegated completion for mark accounting

- A successful resolved result awards one mark; a critical success awards two.
- The promotion threshold is `max(1, recorded Risk)` from the immutable route profile.
- A distinct successful result can promote Mapping at most one level. Consume one threshold and retain any excess marks for a later distinct success.
- Surplus marks alone never promote Mapping. A later successful result is required. Failure and critical failure add no marks and cannot activate retained surplus.
- Mapping never advances past Secured. Secured has no further Mapping reward. A mapping result never alters route Risk, quality, capacity, geometry or a segment's captured StartingMapping/Progress.
- Duplicate result identity cannot award again; missing, wrong-actor, future, conflicting, invalid or unsupported state rejects atomically.

One-promotion-per-result and surplus retention are explicit prototype completion choices where the source leaves repeated advancement from one result ambiguous. GPT found no FL-10 contradiction and agreed with this bounded policy; GPT did not run local tests.

## Runnable acceptance

`route_mapping_results_persist_without_claiming_a_check_or_passage` checks an Unknown Risk-2 route: one success retains one mark; save/restore preserves it; a second distinct success advances knowledge to Sketched; duplicate, unknown, future and wrong-actor results reject; replay is canonical; and clock, RNG, inventory and actor positions remain unchanged.

`route_mapping_surplus_waits_for_a_distinct_success_and_does_not_survey` checks a Risk-1 critical success, retained surplus across a failure, and one promotion from a later distinct success. Its separate Risk-0 Unknown-route profile proves that synthetic knowledge remains separate from immutable authored Mapping and travel still rejects with `RouteRequiresReconnaissance`.

These acceptances prove persistence and delegated result accounting only. They do not prove the full Map Route check, actual work completion, reconnaissance feasibility, Pressure effects or production behavior.
