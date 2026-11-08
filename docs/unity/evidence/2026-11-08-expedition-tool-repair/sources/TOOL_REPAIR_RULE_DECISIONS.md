# Physical tool repair

Date: 2026-11-03 owner session; receipts extend into November4 UTC. Source-bound PLAYTEST plus delegated prototype completions; C# first, no release promotion.

## Source and supplied task

Equipment §Repair and Expedition FL-18 require relevant trained tools, compatible materials worth25% of baseline, active labor of max(1hour, maximumHP/10hours), and a DC10 tool task. Core natural shifts collapse to binary success. Success restores the existing maximumHP; failure spends labor/materials. A recoverable main body can be repaired from Broken. Exact sources remain pinned to main46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4 in inherited evidence.

Schema17 supplies one narrow physical-case repair. The target is the existing50gp/8lb/5HP Alchemist's kit, with its wooden body recoverable and glass/metal implements intact. A distinct functional ordinary Carpenter's toolkit is8gp/6lb/5HP. Its iron-bearing structure is an authored fact. The worker is explicitly trained for this case repair and uses DEX+PB once, not a granted manufacturing trade or universal carpentry ability. Two actual wood/glue/fastener allotments each worth12gp5sp are supplied at the station; nothing is purchased automatically. Each attempt takes1active hour. Spatial reach, current capability/sight/available hand, inventory grants and legal work windows remain required.

The shared affected bench has two explicitly compatible work areas for different workers copying and repairing concurrently. This capacity is a fixture fact, not an implied benefit of independent writing supplies. A spill affects both. The two legal work Watches are the existing [0,8h) and [8h,16h); no general day/rest scheduler is claimed.

## Delegated lifecycle and access

GPT01b3471c-36c1-5954-b0ca-28a7512625ea accepted the lifecycle, adopted by Codex6c84ed0d-e9f9-4912-b9c9-042e6ad846d5. GPT77b4ae6d-1c83-547b-9e28-7f1fd9321406 supplied access distinctions, adopted79db7e08-72a2-401d-9b74-95dd99db53bd. [Exact messages](evidence/2026-11-03-tool-repair/GPT_REPAIR_GUIDANCE.json).

- Starting repair is an immediate instruction to work, after full validation; there is no separate queued assignment command. Reserve one finite allotment and an exclusive same-target repair claim. Debit the whole allotment on first positive eligible labor, once.
- Pause, incapacity, Watch end and combat participation retain actual labor and release future worker bookings. Resume is explicit. No partial HP restoration, automatic restart or refund occurs.
- At full labor, process the established expiry/recovery/life boundary sequence, then resolve the check using actual current conditions. If incapable, retain fully worked AwaitingCheck and the target claim, with no extra worker booking, RNG or HP. Explicit eligible check needs no new labor window, time or material payment.
- Cancel before labor releases materials. Cancel after labor refunds none. A new attempt starts at zero labor and pays its own allotment. Success/failure/cancellation releases the repair claim.
- Active physical repair excludes productive use of that actual target. Validate before atomically pausing conflicting primary-tool research and recalibration. Paused/AwaitingCheck claims exclude another repair but do not themselves disable a still-functional target. Broken remains unusable. Final explicit check reacquires exclusive target access atomically, without extra time. Interrupted work never resumes automatically.
- Spill blocks this repair because it uses the actual affected bench. Manufacturing-specific fouling, target miscalibration and lost-log debt do not by themselves prohibit the separate physically feasible repair. Successful structural repair preserves those obligations, identity, mass, owner, custodian and location.

## Source corrections and historical replay

GPT21e240c5-2c7a-5dbe-8af3-b654e00d2d14 confirmed that ordinary legible-formula copying needs its formula, capability, access, writing supplies and1hour, not Alchemist's supplies. Codex adopted this in5a46272f-d36c-420f-b952-180441b25e25. Schema17 distinguishes copying from the selected tool-dependent research. Broken/active-repair kit blocks research; copying remains eligible if actual bench access is compatible. A worker must explicitly pause their independent copying before repairing; a rejected repair leaves it unchanged.

Source-linked Injury penalties apply once at actual checks: Fine Motor or Exertion for this DEX tool repair; Fine Motor or Cognitive for the selected INT tool research. Different applicable Injuries use only the strongest(-1), with no generic Wound penalty. Poisoned still contributes its separate disadvantage. These are source fidelity corrections, not new balance penalties.

Legacy schema16 retains its original kit-triggered copying pauses and research modifiers under its historical fingerprint. The corrected semantics belong to explicit schema17; no old work, expenditure, outcomes or bytes are silently rewritten.

## Implementation boundary

Immutable repair records, codec, generated job IDs, finite material reservations, current owner checks before idempotency, exact labor, canonical command replay and real disk continuation are implemented. Thirty new cases include independent-review regressions for recalibration overlap and omitted Injury penalties. This is a narrow authored repair procedure. General manufacturing, recipe outputs, product use, tradeXP, portable kits, multi-day schedules and the complete engine remain unfinished. Unity integration remains deferred.
