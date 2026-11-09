# Camp use and Expedition Pressure contract

**Status:** Codex/GPT agreement reached on 2026-11-09 for the next bounded MGT-03 implementation increment. GPT agreed that this camp-use/Pressure slice is next and that a Temporary Camp build is not a prerequisite. No owner decision is needed. This agreement authorizes only the TEST_ONLY slice below; it does not close MGT-03 or the engine.

## Source authority

- ReviewBible revision: `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`.
- Player Book blob: `466871fc128dc5f06043a874da2b9c1d94ed80a5`; pinned file SHA-256: `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`.
- [FL-07 — Building and using a camp](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-07) permits an exposed bivouac without a build task or certified storage and specifies actual site requirements.
- [FL-08 — Pressure follows the expedition’s real exposure](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-08) defines the camp-use increase, full-Watch concealed-camp reduction, shared two-credit cap, Watch settlement and safe-Haven boundary.
- [FL-09 — Complications have a declared cause and a finite response](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-09) defines camp complication stakes and the bounded Patrol response. Patrol itself is outside this increment.
- [TR-13](https://github.com/BordelonDevOps/DecenniumDescent/blob/46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#tr-13) limits its modifier to an ordinary travel complication check.

GPT inspected those pinned rows, the map and handoff at commit `3670596ff84354f635aa1a8cf0f77f9e83741511`, and current Pressure, route-travel, physical-position and WorkLedger code. GPT made no repository changes and ran no compilation or tests. Its actual review ended: “Agreement is reached on this bounded contract, including the explicitly identified prototype completions. No owner decision is needed.”

## Responsibilities and authorities

1. **Author the test site.** Add an immutable, fingerprinted `TEST_ONLY` camp-site profile linked to the existing route fixture and one exact authored route checkpoint. Its fixed facts cover legal access, a stable 20×20-foot footprint, actual drainage, weather protection, sufficient inhabitant/gear space, exposure, concealment and enemy knowledge. Keep these facts independent: concealment does not imply safety, enemy ignorance, storage, sleeping shelter or Haven status. A naturally screened site may be authored concealed without claiming a construction result. The exposed-bivouac path requires no build task and grants no storage.
2. **Record real camp use.** Actual use is established by committed begin/end activity commands, the existing cohort member's physical presence and elapsed `RuleClock` intervals. It cannot be a profile flag. Bind the camp to an existing route/checkpoint. Require route travel paused, no ordinary traversal pending or suspended, and exact physical position verified with `WorldPositionResolver`. Do not add an off-route detach/rejoin system.
3. **Track activity separately from occupancy.** Ordinary camp occupancy/use and `LyingLow` are distinct modes. Lying low is a non-Rest activity in this profile; it grants no sleep, recovery or Rest Debt benefit. Existing compatible work by actors outside the cohort may continue. Actual combat, travel, guard duty or incompatible work breaks lying-low coverage, but does not erase continued physical camp use. Work admission and active lying-low state must assess one another through shared query/execution assessment.
4. **Derive source-linked Pressure changes.** Use the existing cohort/exposure, typed Pressure changes, immutable checkpoints, deterministic RNG, command receipts and `RuleClock`. Do not add another mutable Pressure counter. Do not merge camp use into the OpenCombat category.
5. **Preserve save/replay authorities.** Existing `WorkLedger`, route geometry/progress, spatial position, command history, RNG and snapshot transaction remain authoritative. The crop-farming `CampGreens` records do not represent FL-07 camps. Preserve schema67/68 bytes and replay behavior; add a new versioned schema only for new camp records or checkpoint context.

## Agreed bounded rule completions

These are explicit prototype policies where the source is silent; they are not quotations or production rules.

- Any **positive-duration** actual camp use overlapping an active canonical Watch creates the exposed/known-camp category when either the site is authored exposed or known to enemies. Repeated use, both flags together and multiple intervals still count once per cohort/Watch. Zero-time start/end creates no category.
- A lying-low reduction requires uninterrupted coverage of the entire canonical Watch, at the same concealed site. Partial intervals cannot be combined or carried forward. A credit recorded exactly at the closing endpoint belongs to the Watch just completed; validation checks the actual interval without moving its timestamp.
- A checkpoint that settles an active Watch uses **camp complication context** only if actual camp use covers the instant immediately before that scheduled boundary. Otherwise it keeps route context. An earlier Haven checkpoint keeps its existing context and is never rerolled. Camp checks use stored Pressure without TR-13's travel modifier; route Risk-floor rules still apply. Compatible real stakes are established before any draw. The mixed-Watch context selection is prototype policy.
- A complete lying-low Watch yields one reduction credit, which shares the existing maximum of two reduction credits per Watch. It does not receive a separate allowance. If several qualifying reductions exist, the existing source ordering/cap remains authoritative.
- Late evidence keeps the accepted schema68 rule: preserve an earlier checkpoint and its roll; derive any newly eligible category once from the original PressureBefore, actual category union, already-accounted reductions and captured floor at the due boundary or earlier genuine Haven admission. Do not create a second checkpoint or roll.

## Exact implementation scope

**Responsibilities:** add a fixed-cohort `TEST_ONLY` camp profile and persisted actual-use history; admit/close camp activity through shared commands; bind use to the route checkpoint and physical position; classify interruptions and work conflicts; create source-linked camp increase/reduction rows; extend settlement, historical validation, late-cause reconciliation, checkpoint context and codec branching without weakening schema67/68 validation.

**Expected authoritative records:** the new immutable camp profile fingerprint; new persisted camp-use intervals with cohort, exposure/site links, mode, start/end, causal receipt/revision and termination reason; existing route travel and spatial records; `WorldPositionResolver`; active cohort/exposure; `WorkLedger` and actual combat/movement receipts; typed `ExpeditionPressureChangeRecord` rows; existing checkpoint/RNG/receipt history. The exact persisted shape may follow existing record conventions but cannot duplicate route progress, actor position, worker bookings or current Pressure.

**Dependencies:** `SharedExpeditionPressure`, `ExpeditionPressureRecords` validation/settlement, `TestOnlySharedWorldPolicy` and route-travel command/query integration, `WorldPositionResolver`, existing work admission/intervals, `RuleClock`, deterministic RNG, `Snapshot.Copy`, `SnapshotCodec`/`ExpeditionPressureCodec`, and the Expedition Pressure case suite. The existing map identifies this as the next MGT-03 camp dependency after the GPT-accepted Pressure correction.

**Remaining source gaps for this slice:** how much activity constitutes “actual use” (completed here as any positive duration); precise activity definitions for lying low and its interruption by combat, travel, guard duty and incompatible work (completed here as explicit non-Rest mode with those interruption sources); exact closing-boundary attribution (completed here as the prior Watch); stationary camp complication context and TR-13 applicability (completed here as above). Site facts and enemy knowledge are fixed `TEST_ONLY` authoring inputs, not inferred mechanics. Construction success/material handling, dynamic discovery, guard scheduling, general party eligibility and safe-site adjudication remain unresolved/out of scope rather than implicitly completed.

## Runnable acceptance scenario

Use the existing route traveler and cohort to reach the authored camp checkpoint, pause route travel, and begin committed camp use. Keep a real companion Camp Greens assignment advancing independently.

1. **Exposed/known branch:** run repeated positive-duration camp-use intervals in one Watch, with actual OpenCombat evidence also present. Assert exactly one camp category plus the separate combat category, no duplicate for repeat use, a camp-context checkpoint when use reaches the boundary, compatible predeclared and enforced access obstruction, and independent companion work progress. Compare one-command and split advancement and a save/restore branch.
2. **Concealed branch:** begin lying low exactly at a canonical Watch boundary, save during the interval, then complete the full Watch at the same concealed site. Assert one reduction under the shared cap, no Rest/recovery benefit, and the closing-endpoint source row belongs to the Watch just completed. Repeat with an interruption and a slightly short interval; neither earns a credit.
3. Compare Pressure, typed source rows and links, checkpoint context, RNG, outcomes, consequences, final clock, canonical snapshot and command replay. Include multiple Watch boundaries in one command, actual early-Haven settlement without duplicate source/checkpoint, query/execution parity, and schema67/68 continuation compatibility. Predeclare physically applicable Standard obstruction and Severe closure/retreat consequences; a camp profile cannot manufacture an encounter or bypass retreat restrictions.

## Out of scope and completion status

No Temporary Camp construction prerequisite; build checks, marks, tiers, upgrades, storage, Fortified perimeter, Research Station, Forward Base, Patrol effects, dynamic concealment/discovery, off-route camps, general party/recovery profiles, actual guard scheduling, production camp authority and unrelated Pressure causes are not included. The new slice remains explicitly `TEST_ONLY`. MGT-03 and the full engine remain incomplete; Unity gameplay integration remains deferred.


## Implementation status — schema69 candidate, 2026-11-09

The agreed bounded slice is implemented on branch `Engine`. Schema69 persists fixed TEST_ONLY camp-site facts, actual camp-use/lying-low intervals, their causal command evidence, and the camp checkpoint context. The implementation uses existing route/checkpoint, physical position, clock, RNG, receipts, WorkLedger, Pressure causes/cap, encounter consequences and retreat. It does not add duplicate position, route progress, worker assignments or mutable Pressure totals.

The four connected regression cases are:

- `expedition_camp_known_use_and_actual_combat_are_distinct_pressure_categories`
- `expedition_camp_exposed_pressure_context_and_companion_farming_connect`
- `expedition_camp_early_haven_uses_route_context_and_does_not_settle_twice`
- `expedition_camp_concealed_full_watch_lie_low_saves_replays_and_requires_unbroken_coverage`

Current exact-source results after the GPT-review corrections: C# 9 warnings-as-errors suite **1,289/1,289** (264 hashes), standalone Core/Persistence/LabModel compilation **PASS** (193 hashes), and static package validation **18/18** (290 assets/GUIDs). The concealed-camp regression retains a mid-Watch save and tests save/restore, replay, exact closing boundary, interruptions, no credit for incomplete coverage, and multi-Watch clock progression. See [the evidence packet](evidence/2026-11-09-camp-use/README.md).

This code is still a bounded TEST_ONLY profile. Guard scheduling has no authoritative command/record and is not simulated; only existing combat, travel and incompatible-work interruptions are implemented. General construction, safe-site adjudication, dynamic concealment, general roster eligibility, remaining Pressure sources and other MGT-03 procedures remain outside scope. GPT accepted correction commit `af0954bf90b94032709380477ff5d142a88c1cca`, closed all three recorded blockers, and found no remaining concrete acceptance blocker; see [the actual review](evidence/2026-11-09-camp-use/GPT_REVIEW.md). GPT selected FL-07 Temporary Camp construction as the next mapped dependency; its separate source contract is in [CAMP_CONSTRUCTION_RULE_DECISIONS.md](CAMP_CONSTRUCTION_RULE_DECISIONS.md).
