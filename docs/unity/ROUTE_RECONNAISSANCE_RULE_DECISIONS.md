# Route reconnaissance prototype decisions (schema60)

**Status:** Owner-authorized TEST_ONLY implementation policy for one bounded C# prototype. It is not a promotion of the pinned rules candidate and is not a complete implementation of FL-10 reconnaissance.

## Source authority

The pinned authority is `EX58-EXACT-2026-10-11`, `DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md`, revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, SHA-256 `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`.

FL-10 establishes that route Mapping and physical quality are separate; route effort is 480 nominal minutes per segment; an Unknown route has no base Progress until its actual traverse is made feasible by successful reconnaissance, after which it gets base 1; reconnaissance success can add one group/segment +1 Progress or −1 Pressure, critical success can grant both, and total shared benefits are capped at one of each. Compatible moving reconnaissance can share a traverse; stationary research or crafting does not move it. EX02-08's corrected worked example confirms that an Unknown traverse made feasible by its own reconnaissance receives base 1 plus at most one shared +1 before capacity settlement, never a retroactive base 2. FL-08 defines the Pressure range and route Risk floor, and permits a genuinely Secured route's floor to be zero. FL-11 Forced March is a separate procedure; its +6 DC is not used here.

These clauses do **not** fully define the ordinary reconnaissance task's work location, participants, check method/DC, interruption/retry policy, how an initially stationary pre-travel check relates to FL-10's moving-scout language, or how a general expedition cohort identity is persisted. The schema60 decisions below fill only the minimum gaps needed for a runnable, fixed test profile.

## Adopted bounded policy

| Concern | Schema60 policy | Boundary |
|---|---|---|
| Content eligibility | A fingerprinted TEST_ONLY route must be Unknown, Risk 0, Secured, two Progress long, physically authored and walkable. | No positive Risk, non-Secured quality, capacity overage, route hazards or production route authoring. |
| Cohort | One lead/traveler represents a fixed singleton cohort for one directed route segment beginning at Progress 0. | No assistants, cohort join/split, actor substitution or general expedition-group identity. |
| Procedure | The lead must physically approach the authored route mouth. Reconnaissance is a stationary pre-travel task there; ordinary route travel cannot begin before success. | This deliberately serializes Recon then travel. It does not claim to implement the source's simultaneous moving scout/convoy case. |
| Inspection basis and access | The route-mouth survey uses the authored facts `visible-full-route-and-authored-tread`; for this safe fixture, `clear-visible-walkable-path-establishes-feasibility`. The inspection profile fingerprints its method, facts, basis and target. Existing route walkability, actor awareness/condition and geometric sight checks gate work, interruption and check resolution; each attempt stores the profile ID and fingerprint. | The sufficiency statement is an authored TEST_ONLY fact, not a general rule that sight to a destination proves a whole route. A geometry-conformance check for full-route visibility is optional follow-up. No new observation ledger is introduced. |
| Work/check | Reserve 480 active minutes through shared `WorkLedger`; pause/resume preserves completed work. At completion make a WIS (Survival) check using the existing check, conditions and RNG records against the route-tier standard DC. | The choice of a stationary 480-minute task, this skill binding and the route-tier DC are TEST_ONLY policy, not recovered ordinary Recon rules. The task has one lead and no assistants. |
| Failure/retry | Either failure degree records the check and spends completed work; it grants no feasibility or travel access. A retry reserves a fresh full 480 active minutes. No extra complication or injury is invented. | Interruption and retry semantics are scoped to this fixture. |
| Successful Unknown traverse | Success or critical success creates feasibility only for the exact route/traveler/starting-Progress segment. The subsequent travel record captures Unknown starting Mapping and a total award of 2 Progress: Unknown base 1 plus the one successful Recon +1. | The fixture has only one segment. Mapping stays Unknown, and the result creates no Map Route marks. |
| Critical Pressure benefit | A critical also records its sourced −1 Pressure benefit as blocked at the fixture's current zero Pressure floor. | The fixture does not model positive Pressure or general Pressure settlement. |
| Persistence/replay | Schema60 appends segment, attempt and check records. Existing receipts, shared clock, work intervals, condition journal, DiceStream, route travel record and canonical snapshot codec remain authoritative. | Schemas 1–59 retain their existing encoding branches. Schema60 is TEST_ONLY and release-disabled. |

## Responsibilities and authoritative records

- `ExpeditionRouteSegmentRecord` is the durable identity of one TEST_ONLY segment and its state (`ReconnaissanceRequired`, `Feasible`, `Traveling`, `Complete`). It binds the route, singleton traveler and starting Progress; links the successful feasibility check and eventual travel; and stores the permitted Progress award and the zero-floor critical-benefit accounting.
- `ExpeditionRouteReconnaissanceAttemptRecord` owns lead, segment, required/completed work, attempt lifecycle, and the immutable inspection profile ID/fingerprint. `ExpeditionRouteReconnaissanceCheckRecord` owns the causal completion receipt, ability/proficiency/DC, condition prefix, roll, degree and RNG evidence.
- `TestOnlyRouteReconnaissanceInspectionProfile` authors the method, available facts, sufficiency basis and target. Its content participates in task identity; existing observation geometry, walkability and condition records establish live access.
- `WorkLedger` owns labor reservations and actual intervals; `RuleClock` owns elapsed shared time. Existing condition history, check/RNG services, commands/receipts and `SnapshotCodec` remain authoritative.
- `ExpeditionRouteTravelRecord` remains the sole owner of route movement, elapsed effort and position. Schema60 adds only a guarded authorization path for the exact successful segment and snapshots its Progress award; it does not introduce parallel travel state.
- Route fixture/task/skill bindings are immutable TEST_ONLY inputs with a fingerprint. No mutable global state or separate clock/RNG was introduced.

## Delegation and review

Codex/GPT consensus for the first implementable step was to persist a scoped segment/cohort identity, run Recon and travel sequentially, and defer compatible simultaneous moving Recon/convoy until its spatial and timing contract is specified. The consensus also rejected borrowing Forced March's +6 DC, synthetic Mapping, fabricated failure complications, and general Pressure/capacity behavior. The post-change excerpt review found no blocker; GPT accepted the inspection contract for this bounded profile and identified full-route geometry conformance as optional follow-up. See [the review](evidence/2026-11-07-route-reconnaissance/GPT_REVIEW.md).

## Runnable acceptance

- `unknown_route_requires_scoped_reconnaissance_then_shared_travel` verifies fail-closed travel before Recon; physical route-mouth approach; pure 28,800-second cost query; shared work pause/save/restore/resume; exact completion check and condition/RNG evidence; scoped feasibility; zero-floor critical accounting; successful shared travel to the endpoint; save/restore byte identity; and deterministic replay.
- `failed_route_reconnaissance_keeps_work_but_retry_rebooks_all_eight_hours` verifies failed work does not open the route, persists its check, and retry cannot finish before a newly booked full 28,800 active seconds.
- `route_reconnaissance_requires_and_pauses_on_inspection_access_loss` verifies initial rejection when sight to the authored inspection target is blocked, and interruption after 120 seconds when the lead becomes Blinded; no more work is credited and Unknown travel remains blocked.

This acceptance demonstrates one connected route scenario, not all FL-10 route behavior. See [the route source trace](ROUTE_DISCOVERY_RULE_TRACE.md) and [schema60 evidence](evidence/2026-11-07-route-reconnaissance/README.md).
