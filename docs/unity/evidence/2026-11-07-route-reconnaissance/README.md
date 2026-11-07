# Schema60 route reconnaissance evidence (in progress)

This folder records the bounded TEST_ONLY route reconnaissance increment on the `Engine` branch. Schema59 (`b67c7f47`) is its preceding base checkpoint. Schema60 is not a complete or production-ready route subsystem.

## Current verification

- Full C# 9 warnings-as-errors suite: **1,228/1,228 PASS**. The current run is [FULL_RESULTS.json](FULL_RESULTS.json).
- `route_reconnaissance_requires_and_pauses_on_inspection_access_loss`: **1/1 PASS**, including the sight-blocker subcase. The exact runner report is [FOCUSED_RESULTS.json](FOCUSED_RESULTS.json).
- Static package validation: **18/18 PASS**, 269 assets and 269 unique GUIDs. The current report is [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json).
- `git diff --check`: **PASS** at this checkpoint.
- An earlier interrupted invocation left 1,007 per-case save directories and no results report. Those files were retained; they do not count as validation. The archived [HEADLESS_RESULTS.json](HEADLESS_RESULTS.json) is also historical: its 1,227/1,227 result predates the inspection-profile changes and must not be treated as the current run.
- GPT's post-change excerpt review found no confirmed blocker. It judged the sufficiency statement acceptable as an authored fact of this safe TEST_ONLY route and suggested an optional conformance test that the authored geometry supports the full-route-visibility claim. GPT did not inspect the checkout or execute tests. The review is recorded in [GPT_REVIEW.md](GPT_REVIEW.md).

The profile is limited to one stationary pre-travel lead on one fingerprinted Unknown, Risk-0, Secured, two-Progress route. It does not implement FL-10's moving scout/convoy procedure, general cohort identity, positive Pressure/capacity settlement, or production route content. See [the decisions](../../ROUTE_RECONNAISSANCE_RULE_DECISIONS.md), [the source trace](../../ROUTE_DISCOVERY_RULE_TRACE.md), and [the implementation trace](../../IMPLEMENTATION_TRACE.md#2026-11-07--scoped-route-reconnaissance-feasibility-schema60-test_only).
