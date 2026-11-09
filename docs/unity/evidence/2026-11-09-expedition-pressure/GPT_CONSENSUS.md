# Pre-implementation Codex/GPT contract: expedition Pressure (schema67)

This is the Codex/GPT agreement reached before the implementation increment. It sets the bounded adapter scope; it does not certify the code. The implementation review is recorded separately after GPT inspects the exact commit and evidence.

## Shared simulation contract

- Index eight-hour Watches from the shared `RuleClock` origin. Watch `n` is the half-open interval `[n × 28,800, (n + 1) × 28,800)`, independent of the six-second tactical-round schedule.
- Keep one fixed traveler/cohort and an exposure tied to the actual selected route. Do not add an independently mutable Pressure counter: derive stored Pressure from the initial cohort value and ordered settlement checkpoints.
- Reuse the route record and selected route fixture as the authority for Progress, position, Mapping, physical quality, Risk floor, Capacity and safe-Haven destination.
- Link each actual attack involving a cohort member during the active route exposure to its attack ID, revision and time. Several actual attacks contribute one open-combat category for the Watch. Encounter creation or an attack that was never committed is not a cause.
- A qualifying secured-route entry is a reduction credit. Enforce the shared limit of two credits per Watch, apply the route Risk floor and clamp stored Pressure to 0–6. Route quality modifies only Effective Pressure for the check under TR-13.
- Pressure 0 makes no die draw; Pressure 6 makes one automatic Severe result without a draw. At 1–5, draw the existing natural d6 and apply FL-09 without invented modifiers or rerolls. With this bounded unmodified profile, natural equality is Standard and Minor is unreachable.
- A Standard route obstruction pauses the affected route for 60 elapsed minutes while independent work can continue. Severe closes the existing passage; the traveler may retreat only over the prior physical route path. Do not create an enemy, damage, loot or other undeclared consequence.
- An early safe-Haven arrival settles the unprocessed Watch once and ends exposure. Arrival exactly at the Watch boundary creates one `HavenArrivalAtWatchEnd` settlement, never a second Watch-end result. Arrival does not reset stored Pressure. Do not allow same-Watch route re-entry after settlement.

## Bounded producers and explicit gaps

The first adapter supports actual open-combat attacks and actual secured-route entry only. It gates capacity exceedance, casualties/capture, pursuit, abort triggers, exposed camps, Attention cargo, Counter-Ambush, concealed-camp and pursuit-ending reductions, reconnaissance rewards, extraction, and unsupported route/control compositions. These source rows remain documented but are not silently treated as zero or inferred from unrelated state.

The test fixture marks `TestOnlyCropPolicy.PlotId` as its safe-Haven endpoint only to exercise the settlement boundary; it does not make that crop plot a canonical Haven.

## Acceptance agreed before implementation

One connected scenario must record actual tactical attacks against the route-bound cohort; save before the Watch resolves; restore and replay the same source evidence; resume the existing route after resolved tactical control; settle the same Watch from whole and split clock advances with identical random state, outcome and receipts; apply a bounded Standard obstruction while the companion performs real Camp Greens work; resume route exploration at the exact obstruction deadline; demonstrate pressure-six automatic Severe closure and physical retreat on the existing route; exercise pressure-zero/no-draw and the one-second boundary guard; and cover early and exact-boundary Haven settlement, save/restore and once-only history.
