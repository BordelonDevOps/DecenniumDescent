Review reply: 22b80a0a-b974-4088-8ca8-5dcc4975ea33

## EXP-04 ordinary-exploration Search — source/API contract approved

**Approve both proposals as NEW bounded TEST_ONLY integration decisions:** one explicitly authored visual-sign opportunity, and one whole existing off-calendar activity interval paid through the searcher’s ordinary Action ledger.

**Reviewed packet:** `2316c10f9c5481f37a35a63ccee6b652346f706d`
**Governing source:** `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`

**Approve schema91 for this selected observation-host composition. No additional hearing, exploration Hide or general investigation subsystem is required.** The requirements below settle the remaining boundaries; no further preliminary source/API review is needed.

The repository comparison contains evidence/documentation changes only, with no gameplay-source change after accepted schema90.

## 1. The sensory binding is sufficient within this scope

Approve the prospective faint-visual-sign opportunity, provided its fingerprint identifies the Director authority, searcher, stationary anchor, candidate cell, designated creature, relevant occlusion boundary and qualifying sensory conditions.

The binding supplies **a physically available but uncertain sign of presence**, not direct sight of the creature or automatic knowledge. It must describe what is perceptible from that anchor without seeing through the blocker. The creature’s actual presence, observer-relative Hidden state and current sensory conditions are evaluated privately at completion.

This fits the governing sensory Search procedure: Wisdom (Perception) against the creature’s actual recorded Stealth total, with observer-only disclosure on success. It does not authorize Investigation-by-substitution, an invented DC, hearing, universal detection through barriers or an automatic surprise determination.

The baseline supplies genuine concealment: Hide `observation.6.hide`, final Stealth **18**, remains independently effective against the companion and living witness after actual exit at **30 seconds**. It also demonstrates lawful unseen relocation away from the candidate. Those are suitable implementation inputs, not yet a Search execution.

**Public admission must not require the cue or creature to exist.** Every otherwise legal candidate within the selected public bounds has the same admission and cost. Unsupported sensory circumstances are resolved as no finding, not exposed through a target-dependent query rejection.

## 2. Approve the whole-interval payment and lifecycle

The existing off-calendar ledger already owns an ordinary six-second allowance anchored to the shared calendar. Selecting one complete interval for this Search is a **local scheduling decision**, not a conclusion that all ordinary Searches universally take six seconds.

Reuse `Search` with an authenticated actor, the exact current activity marker and candidate coordinates. Admit only at that interval’s actual Start, with an unspent Action, the required stationary anchor, adequate capability and no conflicting traversal, work, rest or pending decision.

For the witness, this means **declare at 30, perform during `[30,36)`, resolve at 36**.

Declaration is zero-time and performs no Search roll. It commits the ordinary Action once through a receipt-bound Search commitment in the **existing** ledger. The pending attempt supplies the stationary/busy claim; it reserves neither the target nor the candidate cell and consumes no physical stock.

Approve `CancelExplorationSearch`, targeting the pending attempt. Cancellation is zero-time, releases the busy claim and records the actual reason/boundary, but preserves the paid Action until its ordinary authorized refresh. No resume or prepaid retry is supplied. A later attempt requires a new legal interval and payment.

While pending, reject conflicting voluntary movement, Dash, active work and other incompatible activity by the searcher. Independent incapacity, loss of the required visual capability, actual displacement or an admitted mode transition interrupts the Search at its real boundary. Recovery does not restart it. Compatible activity by other actors continues.

**Concrete API requirement:** `CommitActiveLabor` currently protects against Dash but otherwise can replace the commitment. Adding a Search enum alone is insufficient: shared work/payment checks must also prevent overwriting Search, including after cancellation while its Action remains spent. Older schemas must reject the new commitment during encoding validation, not only after decoding.

## 3. Completion ordering and enclosing clock commands

Select this **NEW deterministic boundary order**:

1. Advance actual movement and compatible work to the next due boundary.
2. Settle due conditions, physical consequences and mandatory mode/decision transitions using their existing order.
3. Reconcile Search interruption. A Search already interrupted earlier cannot become complete merely because the actor has recovered.
4. At the surviving attempt’s endpoint, revalidate the searcher, anchor and sensory method; then privately select any currently qualifying target and resolve once.
5. Refresh the ordinary activity interval exactly once, without losing the old payment’s historical proof.

Completion uses the paid attempt’s original interval and receipt. It must not demand or spend a second Action from the newly refreshed interval.

**Yield at Search completion or interruption.** A longer enclosing `AdvanceClock` reports the reached boundary and leaves its remaining requested time unapplied. Use the same behavior for finding and no-finding results; hidden occupancy must not determine how far the public clock advances. No remaining-time request executes automatically.

A mandatory decision reached at the endpoint retains priority. Preserve the existing continuation mechanism and do not roll Search while that decision is unresolved. A later same-time command is not retroactively inserted before an already committed completion.

Equivalent clock partitions must produce the same mechanical outcome, elapsed work and knowledge. Command/receipt revisions may legitimately differ; require byte-identical replay for **identical command histories**, not identical bytes across different histories.

## 4. Candidate movement and information boundaries

**Resolve actual presence at completion, not declaration.** Use the real partial-position resolver, not an old actor anchor.

| Completion state | Search result |
|---|---|
| Designated creature remains at the candidate, Hidden to this observer, with the qualified sign available | One actual Perception check against its genuine current Hide result |
| Candidate empty, creature moved elsewhere or is only partially traversing away, or no supported sign qualifies | No creature check; no finding |
| Valid check fails | Paid completed Search; no finding |
| Valid check succeeds | Disclose the actual location to this searcher and end Hidden only for this observer |

Departure of the hidden creature does **not** interrupt the search early or reveal a reason. The searcher finishes inspecting the chosen place. A return before completion may qualify if the final state genuinely satisfies the same binding; no continuous-presence requirement is inferred.

Use live actor ability, applicable training, injuries and admitted conditions at the check boundary. Preserve the genuine Stealth result rather than recomputing it from the target’s later statistics. Reuse the existing roll/disclosure procedure, not a parallel Search calculator. The current resolver already supplies the relevant arithmetic and observer-only disclosure path.

### No-finding must actually conceal the distinction

Empty, unsupported and failed searches must expose the same no-finding shape: no target identity, Hidden status, private cue, DC, degree, die, draw count or diagnostic identifying which branch occurred.

**An empty `TargetId` is not enough.** `ObservationActionRecord` also contains roll and RNG audit fields that distinguish unrolled from failed searches. Keep those authoritative fields private and provide an appropriately filtered result. Do not add dummy rolls to conceal a leak in the read model.

A successful disclosure grants neither sight nor line of effect and does not communicate to the witness. Later unseen movement invalidates current knowledge while preserving the last-known coordinate and evidence time. **It must not restore the old Hidden latch automatically or update the stale coordinate to track the creature.** The existing observation model already separates those states. A no-finding result must not erase knowledge legitimately obtained elsewhere.

## 5. Minimal persistence and schema91 boundary

Keep **`ObservationActionRecord` as the completed observation-result authority** and `ObserverKnowledgeRecord` as the knowledge authority. Add one bounded attempt history for declaration, paid interval, anchor/candidate, pending/terminal status, actual completion/interruption and the link to its observation result.

The private completion evidence must additionally identify the applicable cue and genuine Hide reference—even on a failed qualified check—so replay can reconstruct why a roll occurred. Do not duplicate the dice, current position or current knowledge into another mutable authority.

Declaration and completion have different causing receipts. Preserve both. A cancelled/interrupted attempt has no fabricated completed observation or Search roll.

**The schema91 layout must explicitly support this observation-host composition.** The current codec cumulatively writes later components by schema thresholds; merely changing the schema51 number to 91 would not establish their authority. Use a narrow versioned selected-layout/component branch and absent-state validation, without inventing later encounters, charters or Pressure contexts. Do not require a general serialization-framework rewrite.

Preserve authentic schema51 and schema90 profiles, their bytes, tactical Search behavior and the corrected legacy cardinality restrictions. The new activity commitment and attempt records must reject under older envelopes. Do not retag predecessor saves.

## 6. Six implementation acceptance groups

| Group | Required retained evidence |
|---|---|
| **1. Genuine concealment and authority** | Actual Hide, resolved exit and two living observers; exact cue/anchor/source binding; real interval-bound declaration and genuine Hide DC. No fabricated concealment or proficiency. |
| **2. Admission, payment and privacy** | Occupied, empty and unsupported candidates have equal public eligibility/cost. Unauthorized/stale/conflicting activity rejects unchanged. Payment survives cancellation; no overwritten commitment or extra Action. Compare the public no-finding projections, not only `TargetId`. |
| **3. Actual resolution and observer isolation** | Real paid success, qualified failure, empty/unqualified completion and later separately paid repeat. Only the searcher learns location; sight/effect channels and the witness’s knowledge remain unchanged. |
| **4. Shared boundaries and interruption** | Cancellation, actual condition interruption, existing-lawful mode change, competing activity and remote work. Test target departure before completion, exact endpoint ordering, long-advance yielding and unseen movement after disclosure. No roll after interruption or automatic tracking. |
| **5. Save/replay and provenance** | Before/pending/completed/interrupted/continued saves; identical-trace replay and mechanical partition equivalence. Isolate forged authority, payment, interval, completion, Hide/cue reference and knowledge. Duplicate/conflicting commands cannot repeat the roll or reveal. |
| **6. Compatibility and exact execution** | Authentic schema51 and schema90 controls, unchanged tactical Search and relevant historical activity/observation tests. Wrong-profile/Release rejection, exact bindings, focused and completed historical results, standalone compilation and static checks. |

## Supplement and inspection limits

**Accept the schema90 full-run supplement:** the report records **1,442 passed, zero failed**, on accepted source `216217d0dfa1781ea1b3ab41c3ba1d4a5e089ec7`. Its four assembly digests agree with the proposal baseline; the manifest records the supplied report digest `904755c1…e3bb01`. This is predecessor evidence, not Search implementation evidence.

I inspected the exact proposal/bindings, complete baseline verifier and result, observation decision record, pinned Combat Search clauses, current activity ledger/validation, Search resolver, knowledge refresh, observation records/validation and codec composition.

**I did not execute C#, run the verifier, load binary saves, recompute hashes, freshly extract the V6 DOCX, change repository files or run Unity.** The listed V6 paragraph hashes were inspected as bindings, not independently re-extracted text.

**Final disposition: approved for bounded implementation.** The cue qualification, interval payment, endpoint precedence, filtered result and schema91 composition above are the contract. Earlier acceptances stand; broader sensory systems and production authority remain open, and Unity gameplay integration stays deferred.

---

Review reply: 75091c70-6da6-45c8-b7ed-2dfe392f332a

## Confirmed — independent wire version 91 and the existing mode-change witness

**Approve your precise proposal: one version-91 TEST_ONLY save envelope, using the schema51 base feature layout plus the new private Search component. Keep in-memory base feature selection at 51 and expose the actual wire version separately.**

This supersedes the composed-schema90 route described in `SCHEMA_COMPOSITION.md`. Preserve that document and its successful baseline as historical investigation; record the independent-envelope choice as the controlling clarification. **No resubmission or further preliminary approval is required.**

### Wire/layout boundary

The implementation must preserve these distinctions:

| Concern | Agreed treatment |
|---|---|
| **Wire identity** | Version **91**, retained through decode, snapshot copy/capture, restoration and re-encoding |
| **Base features** | Schema51 layout and behavior; no implicit charter, Pressure, later-encounter or surprise authority |
| **New component** | Required Search definition and valid history collection, initially empty when appropriate |
| **Profile authority** | Explicit TEST_ONLY selection and distinct fingerprint; wrong-profile and Release rejection |
| **Legacy formats** | Original bytes and behavior unchanged; new Search commitments/history rejected rather than silently discarded |

Use **one envelope and checksum**, not a complete nested schema51 save with another header/checksum. The version-to-layout mapping must be explicit and validated—not caller-selectable arbitrary schema remapping.

Validate the complete selected composition **before encoding and after decoding**. In particular, a base-feature value of 51 must not accidentally authorize the Search extension in an authentic wire-51 payload, and wire91 must not silently omit unrelated records that should be absent. No general serialization-framework rewrite is required.

The filtered Search projection remains as agreed: own pending state and permitted outcome/location, without private cue, target, DC, die or RNG-audit leakage. Internal authoritative records are not the player-facing result.

### Fixed-calendar tactical-control re-entry

**Approve this existing transition as the mode-change interruption witness.** The inspected `EnterCalendarCombat` path preserves the existing encounter/calendar where present and explicitly avoids replaying already-processed Starts. This is sufficient to test ordinary-to-tactical control interruption without claiming a new encounter, resurrected opponent or new initiative grant.

One integration detail matters: **the companion searcher remains off the fixed roster.** Existing participant-only work pausing therefore does not, by itself, satisfy this control. When the lawful transition commits, explicitly interrupt this ordinary-only Search, retain its paid off-calendar Action and elapsed history, release its stationary claim, and produce no Search roll or disclosure. Leave unrelated compatible work alone.

A rejected re-entry must leave the pending Search unchanged. At an exact completion tie, apply the already-approved transition-before-Search ordering. Tactical exit must not resume the interrupted attempt automatically.

### Evidence and scope

I inspected the composition note, observed result, bindings and relevant existing entry handler. The composed baseline’s four recorded assembly digests agree with its bindings; its observed window remains **30→36**, with actual Hide 18 and two independent living observers. That establishes the alternate predecessor composition—not execution of the proposed wire91 format or interruption hook.

**I did not execute code, load saves, recompute hashes or change files.**

**Disposition: approved as clarified.** The prior Search timing, sensory authority, information limits, lifecycle and six acceptance groups remain unchanged. Proceed to bounded implementation and its retained evidence; Unity gameplay integration remains deferred.
