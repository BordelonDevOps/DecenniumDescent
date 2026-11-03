# Fate Rewrite / Eternal Prophecy Interface Specification 05

**Status:** preparation only; proposed, unadopted TEST_ONLY premises. This successor addresses GPT Director REVISE on Proposal 04 and requests a focused readiness recheck. It is not a witness, owner adoption, canon rule, seal, identity acceptance, application, or campaign claim. Proposals 02–04 and Specifications 01–04 remain immutable history; Proposal 04 received REVISE.

## Current state and exact source

Base commit: 36319ab7904454ab468f2917aa52adc5cf4a88d5. Queue481 remains 836 applied / 12 pending / 0 accepted-unapplied; Fate Rewrite is next with TF192-B04 and TF192-B02 dependency. Eternal Prophecy is accepted/applied only for STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY; its native promise is unchanged, guaranteeProved=false, T1–T4 evidence is unsealed, and TF192-B02 remains open. EP480 Proposal 03 adoption and the T1–T4 packet already exist in the base commit; this packet does not repeat them.

The parent raw-byte SHA-256 is corrected to 1f71f14dbb63947dba11a5cfde26a3677fbbfb9ead24bced606bdcd0f8977188 (64 hex characters). The /events/2/after state remains 55de6c13…0347c. Both branches fork from T1 final state 49d94d12e54fbd36d36a0cf3f69803f6de1b0f903557804c02dbd41f1a2ae7c3, with obligation version 2f6c8956d26cecd196523eba61cf777a983217a4d4ab0505ec36960753c0c862, terminal after-state b9b48d2e…b456172d, and unique book version 16ab195897e69ea3f693e7afaf85bfcdf1947ba78a5823e3cabde227e1e58c9a.

The fulfilled book-W remains owned by W at supported cache [15,0,0] under receipt EP480-WITNESS-OBLIGATION-BOOK-W-01-T1-receipt. Its 26 RP cast at 100 ms, original deadline 34,560,000,100 ms, and fulfillment at 34,560,000,099 ms remain unchanged. This is conditional static evidence, not native guarantee certification.

T1 processed W END1900, T START2000, T END3900, W START6000, then closed initiative at 6101. Dispatch is disabled and historical markers remain. Frozen T/W budgets each have Action 1, Bonus 1, Reaction 1, Interaction 1, and movement 30 ft. No later turn, reset, rest, or recovery is assumed.

## Expiry, inherited gate, and loadout

At 34,560,000,101 ms, four prevention operands expire after their inclusive deadline: EP480-PREVENT-ALLY-DELIVERY, EP480-PREVENT-CARRY-ROUTE, EP480-PREVENT-OTHER-DELIVERY, and EP480-SUPPRESS-ORDINARY-EXPRESSION. Preserve their records and refusal history, set these operands inactive, and re-enable ordinary magical interventions and spell expression. Do not change the fulfilled obligation/receipt or reactivate the consumed terminal scheduler.

A new proposed local premise permits only one-time spending of the nonzero budgets frozen in T1 final after initiative closure. Deduct every point; add no turn, refill, rest, recovery, or administrative refresh. This is TEST_ONLY and awaits Director review.

The source scene is a supported flat 120×120 ft room with no hidden actors or solids, and it includes the ordinary operable gate at [10,0,0]. Return323 A /events/2/after/items/gate records open=false, destroyed=false, geometry “blocks direct5ft lane; supported5ft-wide bypass at y5 is clear”; EP480 T1 does not change it. Proposal 03's “no gate/obstacle” statement was wrong and is withdrawn. To make sweeps testable, Proposal 04 offers a new TEST_ONLY geometry model: opaque, collision-blocking rectangular gate volume x=[9.75,10.25], y=[-2.25,2.25], z=[0,6]. Those dimensions and opacity are proposed inputs, not source facts. Rays that intersect this volume are blocked. The inherited y=5 bypass and proposed y=-5 bypass both give a 5×5 ft body 0.25 ft clearance; the southern clearance and exact panel volume are additional TEST_ONLY premises. Coordinates are x east, y north, z up. Actor anchors are centers of 5×5 ft foot-contact boxes at z=0; bodies are six ft high. Book-W has a 1×1×0.1 ft envelope at [15,0,0], with the existing support plate/cache marker.

An isolated fixture overlay proposes ordinary nonmagical back slings for T and W, plus one exact ordinary Wizard class focus FR-EP480-FOCUS-T-01 for T. These are branch-local test objects, not additions to T1 history, campaign inventory, rewards, or canon. At cast, T stores book-W in the sling, holds the focus in the left hand, and keeps the right hand free for Somatic.

## Compatible post-fulfillment event

W grants permission at 34,560,000,102 ms while W and T remain at [0,0,0] and [5,0,0], 5 ft apart. The record costs no RP, Action, or Interaction and changes no item.

Two separate supported movements precede the target event in six-second windows, spending only inherited movement. T travels [5,0,0] → [6,-5,0] → [13,-5,0] → [14,-3.5,0], 13.901795 ft, leaving 16.098205 ft. W then travels [0,0,0] → [0,5,0] → [19.2,5,0] → [19.2,0,0], 29.2 ft, leaving 0.8 ft. T crosses x=[9.75,10.25] at center y=-5 (body edge y=-2.5; 0.25 ft clear); its final diagonal begins at x=13, so its body stays at least 0.25 ft east of the gate volume while moving north. W crosses the gate's x-range at center y=5 (body edge y=2.5; 0.25 ft clear). The southern clearance is a new TEST_ONLY premise. Neither sweep intersects the gate or overlaps the other actor's occupied body volume. All pickup rays and the Counterspell ray stay east of x=10.25. Final T body bounds are x [11.5,16.5], y [-6,-1]; W bounds x [16.7,21.7], y [-2.5,2.5], with 0.2 ft clearance. Both actors are within the proposed 5 ft pickup reach. The book/support stay clear.

At 34,560,012,105 ms, one atomic custody transaction occurs. In the original history T spends one inherited Interaction to move the same book-W from cache into T's sling. The independent movements are already complete. The event checks the exact branch, obligation/version, terminal, book hash, support/marker, actor poses and budgets; any mismatch aborts without writes. The earlier fulfilled first-arrival predicate remains true.

The alternative preserves both movement events and costs. W spends his inherited Interaction to take the same book into W's sling. T's original interaction remains sunk and is not refunded; W pays one additional interaction from his inherited budget. For the successful alternative, reserve W's inherited Interaction before settlement; within the single transaction, debit W's reserved cost before writing custody/carrier and dependent versions, then commit all writes together exactly once. A failed/countered cast does not charge W's Interaction; a transaction version failure cancels its uncommitted reservation without custody writes, while T's original Interaction and already-committed cast Action/RP/history remain sunk. The release is 1 ms after this new custody event; the 400-day-old prophecy creation is not targeted.

T is Wizard 17 with Fate Rewrite known and prepared at the bound profile pointers. Frozen T1 state has limit 13, Dissonance/Refrain 0, no prior spell family, and Action 1. Proposed test payment is base 26 RP; the first prepared Fate Rewrite family waives base strain; surcharge 0. At commitment, before W's counter response, spend Action 1→0 and 26 RP once (64→38), set pending cast, and record Dissonance=0, Refrain=0, seenFamilies=[fate-rewrite], lastSpell=fate-rewrite, and spellsThisTurn=1. Then record W's response and resolve. Clear pending cast after resolution. An interruption preserves the committed Action, payment, and history; successful resolution does not charge or write them again.

After movement W is 6.268174 ft from T in the open same-plane scene. W's bound Counterspell is 60 ft range, Reaction, 3 RP, two-round recharge, and +11 vs rank-9 DC28. W voluntarily declines; no Reaction/RP cost, recharge, or feedback. T is the living direct actor/observer and anchor.

## Conflicting admission request

On the independent branch, fork exactly at 34,560,000,100 ms; do not add any observation or knowledge event before this point. Expire the prevention operands at 34,560,000,101 ms. W then spends 20 ft of inherited movement from [0,0,0] via [0,5,0] to [15,5,0] in a six-second window ending at 34,560,006,102 ms. This route uses the north bypass and has 0.25 ft body-to-gate clearance; T remains at [5,0,0], with no volume overlap. At 34,560,006,103 ms, W directly sees and recognizes W's own book at [15,0,0], five feet away; the sight ray stays at x=15 and never crosses the gate. A reversible branch-local knowledge overlay at 34,560,006,104 ms records only W's own first-person cast/predicate/deadline knowledge and this current direct sighting. It is a new TEST_ONLY input, not part of the T1 trace. W submits the request from the visible cache anchor at 34,560,006,105 ms. The fulfilled target event is 6,006 ms old. Character knowledge comes from W's own cast and the post-fork observation; event IDs, hashes and exact reviewer bindings are not exposed as character knowledge.

W requests removal of the fulfilled terminal outcome against the exact obligation version. The age check passes, but ordered-execution step 3 rejects before new Action/RP commitment or a Counterspell window. The original 26 RP remains sunk. Obligation, receipt, event and physical site remain unchanged. The branch expires, moves, observes, records knowledge and requests in that order; reversing it deletes those branch-local writes and restores the exact fork.

## Holds and requested decision

Both branches are independent, proposed, unadopted and unconstructed. Any later authorized witness must bind ordered forward/inverse transitions, state hashes and read/write versions, same-key idempotency, cost/custody deltas, and exact inverse restoration to its branch start. Any unknown external descendant holds the case.

Preserve all 17 historical cases, question dispositions, H-HISTORY/H-DEATH, qualifications, TF192-B02/B04, Queue481 836/12/0, and unsealed EP480 evidence. No canon/runtime/index/catalog/queue change, seal, closure, spell application, or campaign claim is requested.

Please return PASS_FOR_OWNER_ADOPTION, REVISE, or HOLD. A pass is readiness only; a separate owner adoption must name FR-EP480-INTERFACE-PROPOSAL-05 and cite its exact SHA-256 from PACKET_MANIFEST_05.json before witness construction.
