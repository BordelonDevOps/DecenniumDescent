# PG328-W13 nested-space owner proposal 446 (TEST_ONLY)

Status: **proposal only; not adopted; no witness constructed.** The exact parent is unchanged W01-403 Repack02 `S030` at time `12.9`, pinned at commit `4546a7c967422ef4f3285f19d912445d37181eb5`. Proposal JSON SHA-256: `61b559867d7a5ccc49c3a03f92be173a4e02a946a8c2d7194a6cb2674df4a717`.

## Proposed branch

This branch tests one complete ordering: B creates a single, independently identified Demiplane room inside the existing Fortress; B enters alone; while inside, B successfully Dispels the child room; P5-CLOSE ends and settles that child while the Fortress still exists; only later does A separately Dispel the Fortress and Q27 settle its occupants and items. No child source survives parent termination, and no child anchor relocation is assumed.

The native Demiplane catalog record is still `blocked-pending-operational-review` with `operational: null`. The exact Planar5 Model166 procedure was accepted and applied as static authored material with retained holds, while runtime selection remains disabled. W13 proposes instantiating that procedure only in an owner-adopted TEST_ONLY branch; it does not enable runtime selection, alter the catalog, make Fortress accepted/applied, or change canon/queue state.

B's Demiplane acquisition/preparation bind to Wizard20 `ordinaryLearning/14/selected/0`, `prepared/16`, and `spellbook/51`; both Wizards' Arch Dispel selection and always-prepared access are bound separately. B commits rank8 Demiplane for 21 RP at `13.1`; A's `13.2` Counterspell is component-ineligible because both hands are occupied. The room has a fixed `[35,15,0]` entry anchor in the parent's open courtyard and admits B only. B uses 25 of the 30 movement feet available on B's `13.0` turn and arrives in the child at `[5,15,0]`.

At `19.1`, B commits rank3 Arch Dispel against a perceived point inside the child room. The exterior door is opaque, so A cannot perceive or Counterspell through it. The stipulated check `12 + 5 + 6 = 23` succeeds against DC18. At `19.31`, P5-CLOSE returns B and actually carried focus/pack to the parent anchor `[35,15,0]`; the parent remains active.

A sets down the existing tile at `18.05`, freeing the right hand and retaining its original `3606.13` expiry. At `24.1`, A moves within the parent to the reviewed `[15,10,0]` casting pose and commits a separate rank3 Arch Dispel against the Fortress. B can perceive and legally Counterspell but declares a TEST_ONLY decline. The stipulated `23` succeeds against DC19 at `24.3`; Q27 settles the parent at `24.31`.

## Boundaries and review

The proposal binds exact source contents at the pinned commit in its manifest. The package supplies actor schedules through the `24.31` terminal point, resource and recharge bookkeeping, child and parent support/custody, and all 15 origin-plane exterior body/item pair checks. No W05/W10 outcome is imported. Queue authority remains 830 applied / 18 pending / 0 accepted-unapplied.

GPT review requested: confirm the source bindings, child ending order, interior Dispel, Counterspell eligibility, turn schedule, resource ledger, and geometry. A PASS will establish readiness for exact owner adoption only. It does not authorize witness execution, sealing, Fortress acceptance/application, canonical changes, or queue mutation.
