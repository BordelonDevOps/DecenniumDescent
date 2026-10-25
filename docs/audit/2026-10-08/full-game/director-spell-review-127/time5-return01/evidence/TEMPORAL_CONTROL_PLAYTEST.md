# Time Loop: control and healing-pulse integration

**Bounded live control/pulse transaction interface jointly reviewed and reference-validated. Full Time Loop remains unavailable.**

The [actual nine-part conference](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_CONTROL_PULSE_BOUNDARIES.md) supplements the [twelve world-conservation decisions](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_WORLD_BOUNDARIES.md). The existing [control](CONTROL_STATES_PLAYTEST.md) and [pulse](HEALING_PULSE_PLAYTEST.md) guides continue to own ordinary source behavior. No original card was changed.

## Agreed temporal behavior

| State | Temporal rule |
| --- | --- |
| Explicit source/target regular endpoints | Restore remaining logical progress with authentic new-iteration regular markers. World elapsed time does not move backward, and restoration creates no marker event. |
| Current actual-turn endings | Remain attached to the actual application turn. The initiative-start snapshot has no active turn; a pending in-turn attachment there is invalid. Outside-turn +6-second endpoints retain their absolute deadline. |
| Outside-origin pulse schedules | Keep their original virtual markers and absolute deadlines. Entering initiative or using Time Loop does not restart them. Origin must be recorded explicitly. |
| Speed records | Same application, exact source/component/profile and valid endpoint. Do not reapply or refresh. Current external suppression remains authoritative. Aura, net, form, serum and creature children require their actual parent adapters. Hypermutation's floor is systemic parent state, not a hostile slow. |
| Guiding Bolt's Star mark | Restore its two separate entitlements. Keep the same mark identity and monotonic attack-token history; pending attacks block capture and preflight. |
| Wrathful Brand | Restore the separate owner/ally riders and snapshot timed parent. No new damage, healing or save event occurs at restore. |
| One-shot riders | Use exact parent/application/source/component identities and a finite trigger table. Vein Cutter consumes on its qualifying attack hit; Crippling Lash specifically requires a weapon hit. Omen Reader's once/encounter attack adjustment is distinct from the resulting timed star-ash. |
| Divine Judgment reflection | Retain historical actual-turn consumption. A genuinely new iteration turn can qualify, including a separately authenticated extra turn. Ordinary repeat saves and expiry still use regular markers. |
| PulseSeries | Restore snapshot pending/funded/consumed state under the same valid parent and fixed roster. No cast pulse or consumed-at-snapshot opportunity replays. A later pending paid pulse pays its current printed cost when actually due. |
| Recipient budgets | Retain history with domain, target and iteration-round identity. Circle of Harmony remains shared across owners in the same iteration-round. |
| Eternal Bloom | Preserve the original missing-HP capture and shares. Restore only snapshot installment availability; retain old consumption history. Do not grow the reserve from later damage. Its survival floor is separate. |
| First-contact cures | Restore snapshot instance/recipient entitlements. Garden uses entry/start; Enhanced Garden and Seed use their reviewed pulse event. Restore itself is none of these events. Real-rest recipient histories remain conserved. |
| Native healing | One evaluated opportunity at a genuine regular start during a real encounter. Decline, ineligibility or unavailable payment loses that start opportunity. Extra turns and downtime create no tick. A new iteration can supply a new genuine start, with current RP/reserves. |

**Resource-output conservation:** Transcendent Meditation's second pulse can supply1Ki only once for the same effect instance. Sacred Chant's third pulse can supply1Conviction only once for that instance. Reaching the occurrence while capped or while the whole effect is suppressed still consumes that resource opportunity. Healing may later replay under an authorized restored source without generating the same resource again. A never-reached opportunity remains eligible. Restoration itself grants neither resource.

For example, a Monk receives the second pulse's1Ki, then spends it. Rewinding to a snapshot where that pulse was pending can permit its healing again when legally due, but it cannot return that same1Ki. Sacred Chant uses the same conservation rule for Conviction.

The immutable snapshot is at initiative start. A source first created afterward is not silently added to that snapshot. An origin label cannot manufacture preexisting pulse state. Any logical-clock restoration must demonstrate that the actual source instance was already present in the captured state.

The conference's maintenance wording is read with its express instruction not to reopen ordinary mechanics: an early failed ordinary turn-window payment remains pending until the source's real turn-end deadline. Exact-due paid sequences/windows end immediately on failed upkeep. The notebook explicitly [confirmed this distinction and immutable snapshot membership](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md). No currently supplied pulse profile needs a fabricated at-initiative creation exception; native passive abilities instead await their future genuine regular-start events.

## Current code and checks

`tools/temporal_control_playtest_rules.py` currently implements two limited bridges:

- `CanonicalPulseWallet` lets existing pulse helpers spend the real actor Wallet's RP/Bonus Action and the canonical Scheduler's RC. It owns no duplicate balances and rejects changed aliases before spending.
- `ConservedPulseOutputs` wraps actual `PulseSeries.resolve()` calls for the two resource-producing profiles. It retains unique occurrence IDs and conserved instance/index/component opportunities; it replaces the helper's raw Ki flag with the guarded allowance. Suppressed or capped resolved occurrences cannot be banked. Sacred Chant cannot generate Conviction outside a real encounter.

The returned resource allowance must be applied once by the host in the same atomic event, subject to the actual resource cap. These helpers do not themselves own, increment or restore Ki/Conviction. Source acquisition, legal recipients, actual parent concentration and authenticated due-event scheduling remain host/source-adapter responsibilities. The output guard cannot certify them.

[Validation](TEMPORAL_CONTROL_VALIDATION.json):22 focused methods pass. They exercise the actual existing maintenance, Song, Meditation, Chant and native payment interfaces, plus duplicate output, cap, suppression, early/duplicate occurrence and canonical-alias cases. A replay test deliberately resets only an isolated series view; it demonstrates the output guard, not a complete Time Loop source restoration. The [actual independent review](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PULSE_BRIDGE_CLOSURE.md) approves only these payment/resolved-output bridges. The [review manifest](TEMPORAL_PULSE_BRIDGE_REVIEW_STATUS.json) binds that approval to the exact unchanged helper. The validation JSON retains its original submitted pre-review scope label as evidence; the separate review manifest records the later disposition.

## Still required

The `tools/temporal_control_world.py` integration passes 50 methods, alongside the 76 foundation and 22 payment/output methods. The [actual notebook closure](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_CONTROL_WORLD_CLOSURE.md) confirms the bounded interface after four review rounds. Its [review manifest](TEMPORAL_CONTROL_WORLD_REVIEW_STATUS.json) binds the exact helper, tests and foundation extension; it does not transfer this approval to future edits. It restores selected same-object fields, watches aliases and current concentration callbacks, preserves original outside-origin pulse clocks, and uses authenticated regular-start phases. Hemostasis uses the target's start; other admitted sequences use the source's. Bloom installments and pulse-triggered contacts require current parent occurrence receipts. Native optional healing records an evaluated start even when declined, ineligible or unaffordable.

The repaired world requires the host's existing `ConservedPulseOutputs` guard as an explicit constructor argument. It delegates resource-producing pulses to that same guard and watches its canonical bindings, consumption and event history in the restore transaction. There is no second independent-output ledger. Child operations reject a parent whose clock projection reveals missed upkeep. Capture rejects participant recipient-round claims until a real outside-round import adapter exists. Unclassified Speed suppression blocks capture/restore. Prepared plans also watch the concentration object's complete schema. Eternal Bloom and Crown Restored require concentration through the existing `oracle.engine[26]` zone rule; prepaid Final pulses do not waive that requirement.

Capture now checks that an active pulse already existed and remains live at the actual snapshot marker, without mutating it. Every pulse, installment, contact and native component has an exact admitted identifier. The adapter validates mutable collection types before resource/occurrence writes. When original outside-clock Bloom opportunities are already past, their shares are lost without healing; the installment cursor advances past them so a later authentic due installment can still resolve. No original missing-HP reserve or share is recomputed.

Snapshot concentration bindings include the actual owner, concentration ID, slot object and callback object. Retained references prevent identity-token reuse. A same-ID replacement, even with the same callback or subsequently registered components, rejects before writes. This preserves the original later-ending callback; it does not restore ended/replaced concentration.

This is still bounded component code. Exact supplied source/target schedules and source eligibility remain host inputs; original outside-initiative round-ledger import is not implemented. The new integration does not execute complete cards or apply HP/Ki/Conviction output to final life/resource holders. It admits only the explicit control policy rows and three paid native sources. Omen Reader, extra turns, movement/entry receipts, mutation reserves, shared multi-parent contact holders, device/stasis/copy parents and complete source sibling lifecycles remain unsupported. Missing or ended required concentration rejects restoration. Parent retirement/restoration beyond the existing exact callback is not implemented.

Complete nine-family/source restoration remains in progress. No supported-adapter count or ordinary catalog status has been promoted. Required work includes complete source clock/parent adapters, final resource/output application, complete shared recipient history across initiative boundaries, and the outstanding lifecycles above. [Validation](TEMPORAL_CONTROL_WORLD_VALIDATION.json) and the bounded approval do not certify full Time Loop.

Rapid Coagulation additionally needs the canonical previous-turn movement baseline from the initiative snapshot. It remains unsupported until that state exists. Net Bolt, Totem/Echo, Nano-Aegis, auras and other dependent sources remain unavailable to Time Loop without their physical/device/parent adapters. The seven major integrations and final whole-game/GitHub gate remain open.
