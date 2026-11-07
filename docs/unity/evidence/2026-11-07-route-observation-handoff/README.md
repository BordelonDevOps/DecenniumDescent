# Route-to-observation handoff — schema53 TEST_ONLY

This checkpoint adds an explicitly authored, fingerprinted route-motion profile that composes directed route travel with the existing observation system. Route Progress controls an attached exact position projection; observer sightings use the existing shared-clock movement-segment processor. Paused route travel can hand physical authority to the existing partial `WorldTraversalRecord` and rejoin only at the frozen exact route point. Mid-edge tactical entry and unsupported route departures remain rejected. Route-only schema52 behavior is retained.

The main runnable regression covers route progress 1/4, direct sight at the exact fractional position, atomic detach without spending, the existing 5-foot traversal seeded at 5/4 feet, paid detour, failed return to the old integer anchor, paid/suspended exact return at 15/4 feet, reattachment without snap or endpoint movement, immediate save/restore, deterministic replay, and forged-offset rejection. A separate case verifies checkpoint tactical entry detaches the route position. These fixtures remain TEST_ONLY and do not certify production route geometry or complete tactical continuity.

## Validation

- Headless C# 9 warnings-as-errors suite: **PASS, 1,193/1,193**.
- Focused fractional detach/rejoin/save/replay: **PASS, 1/1**.
- Focused checkpoint tactical entry: **PASS, 1/1**.
- Static package validator: **PASS, 18 checks, 245 assets, 245 unique GUIDs**.
- Unity compilation, Editor tests, Play Mode, standalone build and gameplay: **not run**.

`FULL_TEST_RESULTS.json` and `PACKAGE_RESULTS.json` contain source hashes and exact run data. `FOCUSED_HANDOFF_RESULTS.json` and `CHECKPOINT_TACTICAL_RESULTS.json` retain the targeted acceptances. The excerpt-based GPT review found no push blocker in its reviewed scope; it did not inspect the full diff or run the recorded checks. See [the review record](INDEPENDENT_REVIEW.md).
