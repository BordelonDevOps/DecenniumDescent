# Independent review

Read-only review of the Prowl/OpenRA extraction slice and its final current source. The reviewer did not edit files or run tests.

## Finding and resolution

- **P2, resolved:** run command previews charged an Action every time, although execution only charges Dash once per interval. `SharedWorldCommandQueries.AssessWorldStep` now records whether Dash is already paid, and preview adds the Action cost only when it is not. Regression `shared_world_run_query_charges_dash_only_once_per_interval` checks the first run cost, completes the edge, previews a second run in the same interval without a second Action cost, and commits it.

## Scope limits accepted for this milestone

The configured actor profile is currently restricted to one `TEST_ONLY.numeric-warrior3` numerical profile/speed baseline, and actor state is cloned from the existing companion fixture. The two-configuration case varies stable identities, placement and finite-lot identity while retaining that supported profile. This is documented in the handoff; it is not evidence for a general character/profile catalog. Fish harvest is the only site handler exercised by the two-configuration acceptance case. The read-only activity projection still lacks progress, full procedure-specific claims/status, next boundary and the available lifecycle commands. These are recorded as remaining work.

## Reviewer conclusion

After the Action-cost correction, the reviewer found no remaining actionable issue in the reviewed extraction slice. This conclusion is limited to architecture wiring and preview correctness; it does not certify gameplay rules, source completeness, general actor capability breadth, Unity integration, or full-engine completion.

The current source hashes and execution receipts are in [the evidence README](README.md). The current full suite is **1,117/1,125** with eight schema42 harvest failure names matching the older baseline; the compile and static package receipts pass. The reviewer did not independently execute those checks.
