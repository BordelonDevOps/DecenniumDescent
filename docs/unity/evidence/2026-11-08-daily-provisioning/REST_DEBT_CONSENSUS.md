# GPT consensus — Rest Debt Strain integration

## Question and outcome

The schema62 implementation records every `ExpeditionStrainGainRecord` with a required `SettlementId`. Core validation requires that link to a `DailyProvisioningSettlementRecord`, and the Laboratory validator enforces the daily-provisioning source profile. Pinned FL-03 also requires Rest Debt causes to add to the same `expedition.strain` track. A synthetic food settlement would misstate cause; a second gain history would duplicate the track.

GPT agreed to generalize the **one** `ExpeditionStrainGainRecord` history with typed `CauseKind` and `CauseId` in schema63. Schema62 retains its exact wire layout and fingerprint; its existing `SettlementId` decodes as a `DailyProvisioning` cause. `SettlementId` remains a compatibility accessor/constructor for daily causes instead of a second independently stored reference. Rest Debt causes reference their individual qualifying event, not only the debt episode.

The already-pinned namespace identity is `campaign.rest-debt` → `expedition.strain` in `strain_bindings.json` binding 27. It is a namespace reference only; FL-03 remains the operative source for actual gain conditions. Use this same source identity for both unpaid-deadline and subsequent-missed-Rest gains, with distinct cause kinds/IDs.

## Required ordering and validation

GPT identified that current history validation computes a cause's prior Strain level only from earlier timestamps or revisions. A daily-provisioning gain and Rest Debt gain can occur at the same timestamp and command revision, so that test would omit the earlier gain.

Schema63 must persist a per-actor within-command gain sequence when no existing durable event sequence identifies order. It records execution order only; it does not add a new source-level priority. Resolver, codec, Core structural validation, Laboratory cause validation, and `ExpeditionStrainRules.Project` must agree on `(At, Revision, GainSequence)` ordering. Both Rest Debt cause records and daily settlements must cross-reference one gain exactly once, verify actor/time/revision/source/outcome, and use the same cumulative level, cap, and endpoint calculation. The initial Rest miss that merely opens debt does not itself create Strain.

Required regressions:

- An authentic schema62 snapshot with existing gains roundtrips and continues unchanged.
- Each qualifying Rest Debt trigger produces exactly one linked gain; duplicate processing produces none.
- Forged cause kind/ID, wrong actor, or nonqualifying event is rejected on restore.
- Same-time, same-command daily and Rest Debt gains preserve cumulative levels, cap/endpoint attribution, save and replay.
- A qualifying Rest clears debt without deleting accrued Strain or granting Long Rest benefits.

## Follow-up source question — watch anchor and recovery metadata

Codex asked GPT whether FL-03 or the pinned Expedition Strain recovery text classifies Rest Debt points for recovery, and whether the fixture could reuse the existing zero-based provisioning epoch for canonical Watches. GPT's actual answer:

- Store Rest Debt-caused gains with `SourceId = campaign.rest-debt`, `OrdinaryRemovable = null`, and `RemovalGateMet = null`. The pinned sources authorize the gains and debt-clearance procedure but do not classify these points or impose a debt-specific recovery gate. Null means unclassified, not blocked or permanently unremovable. The point still contributes to Strain and its effects. Clearing debt neither deletes the point nor changes those fields. Do not copy FL-04's supply-shortfall block onto Rest Debt.
- Reuse the already selected `CanonicalDayOrigin = RuleTime.Zero` as the fingerprinted TEST_ONLY calendar. Derive half-open Morning `[0h,8h)`, Afternoon `[8h,16h)`, and Evening `[16h,24h)` Watches within each day. Do not add another epoch or use initiative origin. Rest-slot changes remain prospective actor schedule changes, not changes to canonical Watch boundaries.
- For a missed 16–24h Rest, debt opens at hour 24 and the second following canonical Watch ends at hour 40. EX-W02's hour-32 event is completion of a debt-clearing Rest, not the debt deadline.

GPT inspected the pinned Player Book, Strain reference and bindings, and ran no code or tests. It said these bounded representations can proceed without owner escalation. Recovery classification, Rest benefits and Strain removal remain outside this slice.

## GPT inspection record

GPT inspected the `e399a214` handoff, gain record, codec, validators, pinned bindings, and source clauses. It ran no tests or builds. It agreed that this representation is within the existing MGT-03 scope and requires no owner decision. The review is in the Unity Rules Engine Development chat; this file records its specific implementation guidance for the next slice.
