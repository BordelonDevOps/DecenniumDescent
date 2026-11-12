# Unity Rules Engine Development focused EXP-04 review

Response `602c5361-5a05-4a8e-ba01-b5676e4c7363` reviewed source `8701b2abc7ecec5e1188c1d0da4f6981c8215396` and evidence `5279c3876ded7d58a31d1987e546722010d079b7`. [Review chat](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6af31754-d1bc-83ea-aa5c-d5e33cc9258c)

## EXP-04 public ordinary Hide/Search — focused review passes

**Reviewed source:** `8701b2abc7ecec5e1188c1d0da4f6981c8215396`
**Reviewed evidence:** `5279c3876ded7d58a31d1987e546722010d079b7`
**Controlling authorization:** `091c7292-93e1-41b0-aac0-a2e1d458f24e`

**The bounded adapter satisfies the focused correctness review. I found no concrete implementation blocker and request no code correction or additional focused scenario. Final acceptance remains pending only the completed exact 1,484-case regression.** The pinned bindings correctly leave `regressionCases` null rather than claiming that the unfinished run has passed.

### 1. Scope, authority and command admission — met

The implementation diff is confined to the session model, session view, existing test-case file and console help. The source-to-evidence comparison adds only the evidence packet; it contains no intervening engine or console-source changes. The adapter exposes the four authorized command families without changing their underlying procedures.

Fresh ordinary declarations have the correct restrictions:

- **Hide:** hero only, at an authored stationary Hide anchor, using the hero’s current personal Start token.
- **Search:** companion only, at its authored stationary Search anchor, using its current off-calendar activity token.
- **Cancellation:** the appropriate actor’s actual pending attempt ID.

The token helpers account for existing payment, pending attempts, traversal and exact start time. They do not inspect private target occupancy or cue qualification. Search candidate coordinates remain subject to the existing engine procedure rather than a new adapter-side “eligible target” filter. Mixed observation payloads containing inventory, combat or mining requests are rejected.

The ordinary stage remains **after the actual first exit and returned-complete charter, but before genuine later entry**. Ending the later fight cannot reopen it because the retained entry record still makes `StageOpen` false. This is the existing stage contract, not a new post-combat observation window.

**Receipt handling is correctly ordered.** The current seat grant and actor control are checked before execution. An existing matching receipt passes through the engine with that current grant without being rejected by fresh stage or target checks. A conflicting command ID is not treated as a duplicate; genuinely new commands still require the current revision and permitted target. No alternate retry mechanism was introduced.

### 2. Paid lifecycle, public continuation and actual RNG — met

The public walkthrough reaches the legal window by replaying the accepted first 108 commands from a newly started session, then performing actual movement and clock advancement. It does not manufacture an observation-ready snapshot or reopen the accepted r183 state.

The retained route covers the relevant adapter behavior:

| Operation | Focused evidence |
|---|---|
| Paid Hide and cancellation | Hero Hide commits at r120; cancellation commits at r121; repeating that cancellation returns `Duplicate`. |
| Independent Search payment | Companion Search commits at r122 while using its own activity allowance, then is cancelled after two elapsed seconds. |
| Genuine Hide resolution | Two later Hide attempts complete using actual natural rolls **4 and 2**, with real relocation between them. |
| Pending Search restoration | Search commits at r134; the saved r135 state retains the same pending attempt with **four seconds remaining**. |
| Safe retry and completion | The restored submission returns `Duplicate` at r135; advancing the remaining four seconds completes it at r136 with `NoFinding`. |

The input history, console output and connected report agree on these transitions.

The walkthrough’s saved-state assertions specifically check that both cancellations retain their original payment commitments, create no observation action and leave RNG unchanged. Its later-entry assertion checks that initiative starts from the actual post-observation RNG state and preserves the independent **Warned** binding. The resulting initiative order is genuinely **defender first, then hero**.

**The No Finding outcome is valid evidence.** This adapter review does not require replacing those actual rolls with a successful Hide or forcing a successful Search. The existing success-resolution rules were not changed, and the completed regression remains responsible for their inherited coverage.

### 3. Observer isolation and public information — met

`ProjectObservation` uses the existing `Simulation.ObserveExplorationHide` and `Simulation.ObserveExplorationSearch` lifecycle projections with the current grant. It separately obtains location evidence for the hero and companion. It does not combine their knowledge, project the buyer’s private knowledge, or expose raw observation records. The first-opponent view receives no observation projection, and a disabled seat returns before that projection is constructed.

The underlying `KnownLocations` method returns a detached, read-only collection for the specified observer. It distinguishes current sight from other permitted location evidence and excludes hidden or invalidated location entries. The adapter therefore does not turn a historical finding into automatic tracking through unseen movement.

The actual console excerpts confirm that:

**While pending**, the player receives the attempt ID, lifecycle status and deadline needed to continue or cancel. There is no private roll, difficulty, observer-eligibility or cue-qualification field. The opposing seat’s `Observation` is null.

**On completion**, Search reports `NoFinding` with `FoundLocation: null`. The separate hero and companion knowledge collections do not acquire a Search finding from that outcome. Hide remains a public lifecycle result, not a disclosure of whether particular observers were successfully deceived.

**After later entry**, the stage and fresh tokens remain closed. Historical attempt summaries survive, while this bounded ordinary projection no longer returns the two location-evidence collections. The r206 console view demonstrates that state during the depleted-cache revisit.

No privacy correction is requested.

### 4. Connected continuation, restoration and compatibility — met

The connected report records **248 console inputs**, restored and uninterrupted continuation to **r208**, and the supplied pending and final hashes. The retention code checks equality between the C# and console pending saves and among the restored C#, uninterrupted C# and console final saves.

The recorded checkpoint identities are:

```text
Pending Search:
f88706f1e32ff95ee99a2aeb7a5d5ce9b1e49c98a91b5657f529135acb9fd883

Final r208:
484c52179f7788ff456d3a2b318f1be6872f649e696f0bdd062317b23d712228

Authentic accepted r183:
5ec854b393c09fbf8da8ad15433d41a582ae12efe2629456af5e2606b40483dc
```

These values agree across the relevant report and bindings. The compatibility report records `PASS` at r183 with the accepted cache digest. **I compared the recorded identities; I did not independently recompute the binary hashes.**

The later continuation is not merely an observation-only endpoint. The console shows the same cache open and depleted at r206, its two-pound carried descendant present, ordinary observation still closed, and subsequent committed movement reaching r208 at clock `113653/2`, followed by a successful save response.

The changed final digest is expected for this different, legitimately paid command history. **The accepted EXP-03 r183 checkpoint remains a compatibility obligation, not an outcome the new observation route must reproduce.**

### 5. Compilation, static checks and performance disposition

The exact focused report records **C# 9**, one discovered case, one pass and zero failures for:

`exp04_session_ordinary_observation_scope_before_charter`

The standalone report records successful Core, Persistence and LabModel compilation. The static report passes its package, dependency, opt-in and source-binding checks. These reports explicitly do **not** establish Unity compilation, import, Play Mode or release-build validation.

The input timings remain individual measurements. In particular, the measured genuine Hide completion advances are approximately **25.061 ms and 29.798 ms**, separate from the roughly 10–16 ms declaration/cancellation submissions. The authentic compatibility restore is separately recorded at **16,579.1505 ms**. None of these measurements closes broader P1.

## Sole remaining acceptance gate: EXP-04 E1

**E1 is evidence-only: finish and retain the already-running exact unfiltered regression. It is not a requested implementation correction.**

The existing launcher and finalizer already express the appropriate closure requirements: **1,484 unique cases**, preserving the ordered **1,483 accepted predecessor names** plus the one new scoped observation case; six completed assignment/journal sets; passing rows with empty errors; and agreement between the journals, focused row, inventory and final report. The report must remain bound to the same reviewed source and retained four-assembly set.

The 1,484 total **includes** the new focused case. No separate additional historical run, replacement gameplay witness or duplicate source/API packet is requested.

For closure, return the completed report, ordered inventory, six journals and completion markers, and updated exact bindings. Provided the implementation remains unchanged and those results support it, the next review can be limited to **E1 completion and source/assembly continuity**, without reopening the focused findings above.

### Final disposition

**Focused correctness: met. No code correction requested. Final bounded acceptance: pending only EXP-04 E1.**

The direct **TAC-03, RUL-01 and FND-05** prerequisites remain unchanged. The previously closed EXP-03 E1 stays closed. This review does not authorize EXP-05 or later implementation, promote production authority, close broader P1/INT-03, or change the deferred Unity integration disposition.

This was a read-only review of the pinned source, comparison, evidence-generation code, reports, bindings and selected actual console records. I did not execute scripts or tests, compile, load DLLs or binary saves, recompute digests, or modify repository files.
