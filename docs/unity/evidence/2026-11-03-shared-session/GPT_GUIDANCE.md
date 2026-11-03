# Guidance from Unity Rules Engine Development

Owner-requested discussion: https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206. Architecture response `b69eab08-4ab5-5dbf-ad5c-28cf268d2a4f`; owner-approval acknowledgment and further proposals `76afe920-a4ea-5bd5-a2b4-4619d56b0f40`. GPT did not execute the C# suite. The save-destination guard recommended below was implemented and regression-tested. Pending proposals remain separate from the approved initial policies.

**No architectural or source-policy objection. I found no agreed constraint requiring a different integration order.** Persisting the ledger through the existing authoritative transaction path is a sound next increment.

I inspected `c52d2a3` and its code parent. The [current handoff’s “Next implementation dependency”](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/docs/unity/DEVELOPMENT_HANDOFF.md#next-implementation-dependency) explicitly calls for shared-state integration using the ledger, exact timestamps and existing persistence foundation. It does not require a finished gameplay scheduler or Chris’s pending policies first.

The following are **engineering recommendations**, not recovered Decennium mechanics:

- **Make the snapshot version explicit.** The current `Snapshot.Schema` is a constant. Avoid simply changing it to `2`: retain the exact schema-1 encoder/decoder and select schema 2 explicitly. Do not reinterpret legacy synthetic `Clock` values as seconds. Schema 2 should have one authoritative exact `RuleTime`, without a second independently advancing clock.
- **Keep one commit boundary.** Replace the immutable ledger only within the detached candidate snapshot. World changes, ledger settlement, time, RNG and the command receipt must commit together under one revision—or all remain unchanged. Sharing an immutable ledger reference between snapshot copies is acceptable.
- **Validate the aggregate, not just the component.** [`WorkLedger`](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/engine/com.decennium.foundation/Runtime/Core/WorkLedger.cs) checks internal consistency; it does not establish real worker/job/location references, custody permissions or lawful work. The fixture policy must validate those relationships. Its resource lots must not duplicate another authoritative inventory balance.
- **Preserve command identity and compatibility checks.** Fingerprints must include all new command payload fields. Replays must still check current authority. Bind schema, content scope and dice-mapping version explicitly or through a verified versioned fingerprint; retaining the RNG state alone does not identify its mapping.
- **Protect existing save destinations.** In [`SnapshotCodec.cs`, including `FileSaveStore`](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/engine/com.decennium.foundation/Runtime/Persistence/SnapshotCodec.cs), `Save` structurally validates an existing destination but does not compare its schema/content with the replacement. Use a separate development-fixture path or reject an incompatible destination. Supporting schema-1 reads alone does not prevent overwriting a schema-1 file.
- **Keep the existing supported save boundary.** Completed-command saves are sufficient for this fixture. Later interruptible jobs must persist their continuation state before claiming mid-resolution resume. Retain bounded decoding and an aggregate save-size limit.

The useful acceptance evidence is: unchanged schema-1 golden bytes; schema-2 fractional-time/ledger round trips; reserve and settle restored alongside world state; replay after reload without another debit or revision; conflicting payload rejection; and a deliberately failing combined mutation leaving world, ledger, receipt history and RNG unchanged.

That would establish **atomic shared persistence for the bounded work fixture**, not a complete job lifecycle or whole-game save. Nothing in this increment needs to adopt exploration cadence, traversal or farming rules. This was a read-only architecture review; I did not rerun the suite.

---

**Recorded in this handoff: all three decisions are now owner-approved PROTOTYPE policies.** This supersedes their previous pending status:

| Decision | Approved scope |
|---|---|
| Clock/pause | 1:1 exploration; shared solo pause for menus/dialogue; tactical decisions pause; six seconds per full combat round; wait/rest fast-forward; no offline progress. |
| Traversal | The specified Dash-based running, strength-based jumping, standing-half, and ordinary climb/swim surcharge. These are newly adopted prototype rules. |
| Camp Greens | The linked full crop profile, including its inputs, labor, growth, care, interruption, failure and freshness provisions. |

These decisions do **not** promote old canon or approve release. Initial initiative phases remain undecided. The checked-in [proposal document](https://github.com/BordelonDevOps/DecenniumDescent/blob/c52d2a365b18d05e6b7e333ca8e9e20bb03954b5/docs/unity/PROTOTYPE_RULE_DECISIONS.md) still has the earlier pending labels; this message records their successor status, rather than claiming that file has been edited.

**Recommended Camp Greens boundary completion — not yet approved**

Use exact timestamps and credit growth/work over the elapsed interval **before** resolving its endpoint. Do not round a nearly completed hour or day into completion.

| Coincident boundary | Recommended outcome |
|---|---|
| Growth reaches 168 hours exactly when care expires | Credit the valid growth interval and transition to **Mature**. No additional tending is required to earn maturity. |
| Tending completes exactly when existing care expires | For a still-growing, otherwise eligible crop, renew care without an uncovered interval. No neglect time accrues. |
| Care or suitable conditions return exactly at the 48-hour failure deadline | **Failure wins.** Recovery must occur strictly before that deadline. This makes the previously ambiguous endpoint explicit. |
| Maturity coincides with a season becoming unsuitable | Previously earned growth still counts. The crop becomes Mature; the season change does not retroactively remove growth. Actual destruction or loss of access remains effective under its own rules. |
| The full harvest hour completes exactly at `maturity + 48 hours` | Treat completion as timely and resolve it before the unharvested-crop deadline closes the batch. |
| Freshness expires at that same timestamp | The produce is already **non-edible** at its freshness endpoint. Timely harvest does not extend freshness or create a momentary edible award. |
| Harvest remains incomplete at its deadline | Close the crop as failed/unharvested. Retained labor does not create proportional food. |

**After maturity, stop requiring daily growth care.** The fixed harvest window replaces the growth/neglect clocks. Tending cannot extend that window. Cancel unnecessary future tending; retain labor and inputs already spent on an overlapping task.

For a concrete edge case: maturity occurs at **M**, harvest first begins at **M**, and interruptions delay completion until **M + 48 hours**. Completion is timely, but freshness also expires then: **zero edible food is awarded**. Preserve the batch’s physical disposition and terminal outcome.

These are crop-local rules. They do not override a separately sourced destructive hazard or establish universal event priority for combat.

**Recommended failure disposition — also a proposed completion**

- **Spent inputs stay spent:** seeds, committed water and completed labor are not refunded. Commit tending water when its first active work begins; grant renewed care only upon completion.
- **Unspent reservations are released:** retain intact tools and unused supplies at their actual locations. Remove unused future worker bookings, preserving historical work.
- **The failed crop remains recorded at the plot as nonharvestable biomass.** It grants no automatic food, seeds, compost, crafting material or resale value.
- **Partial harvest means retained labor progress, not proportional inventory.** Award the eight-pound food lot only upon valid full completion. If the batch fails first, close it without an edible output or a restart that restores its entitlement.
- **For this prototype, include clearing an ordinary failed Camp Greens crop in the next planting’s existing one-hour task.** Require fresh planting inputs and a new batch ID; retain the failed batch’s history. This avoids introducing another arbitrary cleanup duration.
- After successful harvest, close the crop and track the resulting food lot independently. Subsequent crop cleanup cannot delete or duplicate that lot.

Persist these transitions and settlement receipts atomically. Reloading must preserve the exact boundary outcome.

**Initial initiative phases remain a separate decision**

The approved six-second round does not determine where each actor’s start/end falls within it.

My recommendation remains an explicit prototype convention for **N initial actors**, indexed from zero:

- Start: `T₀ + 6i/N`
- End: `T₀ + 6(i+1)/N`
- At a shared timestamp, finish the outgoing slot before beginning the incoming slot.
- Preserve existing absolute deadlines and captured virtual markers.

For three actors, that produces **0–2, 2–4 and 4–6 seconds**. These are scheduling checkpoints, not two-second action durations.

**That allocation is still a proposal.** Membership changes also need a stated future-schedule policy without rewriting existing markers. Codex can continue testing caller-supplied phases and completing schema-2 integration without adopting either scheduling choice.

