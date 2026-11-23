# Genuine Strain recovery witness plan

**SOURCE-FEASIBLE PROPOSAL; NOT EXECUTED OR ACCEPTED EVIDENCE.** Independent read-only investigation by `/root/review_consecration` at `6e70f4491b967fa71917544a606f7e2985664818` identified this route using existing `StartWithConnectedWorkControl` commands. It does not close the previously accepted Long Rest evidence gap. Implementation and the new V1 evidence run remain behind INT-05's complete source/API review.

| Phase | Proposed existing route and evidence to retain |
| --- | --- |
| Earn eligibility | Reuse `ConnectedClericSettlementCases.EarnClericObjective(true, ..., selectedSession)`, the genuine completed reinforcement encounter, milestone and Cleric2 advancement. Preserve actual earned abilities, positive HP and the stationary Cleric at the berth `(1,3)`. |
| First rest | Begin at `57,600`, complete at `86,400`. The inherited route consumed only `2/3 lb` food during Day0 and insufficient water. Native Day0 provisioning should create a point with its removal gate closed. Preserve the actual settlement, point, closed gate and completed rest; do not manufacture an offer. |
| Day1 food | After `86,400`, Hero portions `2 lb` from the actual retrieved `TEST_ONLY.pack-rations`. Use the generated child identity: Hero drops it (native handling amount `1`); adjacent Cleric picks it up and consumes `2 lb`. Ownership remains Hero's; custody changes lawfully under the existing player inventory grant. Direct ration handover is not admitted and is not part of this route. Intake requires `1,800` productive seconds. |
| Day1 water | Move Cleric lawfully from `(1,3)` to an accessible pool-adjacent anchor such as `(2,3)`. Use the actual carried Companion waterskin, with grounded Club/worn focus leaving two usable hands. Fill `4 pints`, consume the actual produced lot, fill another `4`, then consume it. Each fill requires `60` active seconds and each intake `240`: `600` productive seconds. Do not use the contaminated flask or infer that held stock counts as consumption. |
| Second rest | Complete all provisioning and return to `(1,3)` before `144,000`, with no conflicting work, traversal, concentration or choice. Begin at `144,000`; request clock advancement through `172,806`. |
| Offer and continuation | At `172,800`, the successful later provisioning day should open the prior point's gate before tied rest/debt completion. The second rest is exactly `86,400` seconds after the first beneficial completion. Retain the real offer and suspended clock, strict-save/restore it, then submit Cleric `ResolveExpeditionStrainRecovery` against its actual offered **PointId**. Observe one actual removal and continuation to `172,806`; do not substitute an offer ID or infer success from the source plan. |

The proposed added resource debit is `2 lb` food and `8 pints` water. Authored stocks are `20 lb` pack rations and a `32-pint` clean pool; the inspected inherited route does not consume these. Expected residuals are `18 lb` and `24 pints`, subject to actual run verification. The three intakes and two fills require `2,400` productive seconds; movement, handling and waits for native ordinary allowances are additional. Existing authorizations, history capacities, bodily eligibility and stock/access checks still apply.

## Exact source route

Paths below are under `engine/com.decennium.foundation/` and pinned in `STRAIN_RECOVERY_SOURCE_PINS.json`.

| Obligation | Native source |
| --- | --- |
| Genuine prerequisite and existing cadence | `Tests/EditMode/ConnectedClericSettlementCases.cs:47-110`; `ConnectedClericLongRestCases.cs:165-209,236-249` |
| Already retrieved rations and Day0 intake | `Tests/EditMode/ConnectedExpeditionQualityCases.cs:227-255,283-288` |
| Portion, physical child and custody | `Laboratory/Model/OrdinaryInventory.cs:27-38`; `SharedPortableEquipment.cs:239-252,318-336`; `ConnectedExpeditionSession.cs:53,705-714,738-742` |
| Intake and fill duration | `Laboratory/Model/TestOnlyInventoryPolicy.cs:155-167`; `TestOnlyFillingPolicy.cs:119-132`; `OrdinaryInventory.cs:13-15,40-47` |
| Finite water and physical access | `Laboratory/Model/PortableEquipment.cs:76-77`; `Laboratory/Model/WaterFilling.cs:11,19-32,53-75`; `Laboratory/Model/TestOnlyFillingPolicy.cs:67-75` |
| Actual recipient consumption and daily settlement | `Laboratory/Model/SharedDailyProvisioning.cs:417-443,446-499` |
| Gate opening and actual offer | `Laboratory/Model/SharedStrainRecovery.cs:131-157,178-244` |
| Tied event ordering | `Laboratory/Model/TestOnlySharedWorldPolicy.cs:749-751,842-850`; `SharedClericLongRest.cs:159-170`; `SharedRestDebt.cs:256-307` |
| Real response and resumed clock | `Laboratory/Model/ConnectedExpeditionSession.cs:550,778-780`; `SharedStrainRecovery.cs:248-329` |

Original clauses remain `DescentReviewChanges/ReviewBible/docs/mechanics/STRAIN_PLAYTEST.md:84-88` and `expedition/EXPEDITION_PLAYER_BOOK.md:64-77`, with the accepted Long Rest integration decisions. This route creates no new source or authority.

## Required INT-05 evidence allocation

At minimum, retain actual V1 descriptions, pure assessment and point alternatives before and during the offer; original clock and recovery-command results; rejected wrong-point, wrong-owner, stale observation and conflicting-ID probes; exact retry without a second removal; pre/post canonical equality for all reads and rejections; and supported uninterrupted/restored/replayed whole/split paths around provisioning, rest completion, pending offer, removal and continuation. Historical result explanation must distinguish the initiating clock receipt, completed rest, offered point, resolving command and current continuation. All new read paths must satisfy the no-resolver/no-RNG/no-settlement purity contract.

This proposes one positive route on the work-control factory. Older Cleric Long Rest and OMA factories do not expose water filling; it does not prove equivalent positive reachability there. Preserve their exact admission and documented limits. An execution failure must be retained and diagnosed from native state; no injected food, Strain, offer, time or schema64 replacement is permitted. Passing this route alone would not complete INT-05.
