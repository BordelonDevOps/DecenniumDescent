# Schema53 route-save compatibility evidence

This test-only follow-up checks one authentic pre-schema54 route-travel history. It changes no production code or snapshot schema.

## Fixture provenance and acceptance

`RouteTravelLegacySaveFixtureCases.cs` embeds two saves produced from pre-schema54 Engine checkpoint `8377ea265b0d3fcdb9a6a3308489911173d48e63`:

- Before the next clock interval: SHA-256 `a7ce6b080784440c829afb4a28786ae490dcee9196fd33863311203ed9d1ac3d`.
- After the next 5,400-second clock interval: SHA-256 `1b07ec56715e8f7823c8c3719e3f84b40e7b8c53f409e0eea9d39b28774dc7bd`.

The named case checks both saves retain schema53 and the original route-observation profile fingerprint. It verifies the pre-save contains one Moving route with attached spatial authority, restores and re-encodes that save byte-identically, advances the shared clock by 5,400 seconds, and requires the output bytes to match the archived pre-schema54 after-save. This establishes compatibility for that specific state and continuation, not all schema53 saves.

## Validation

- Focused compatibility case: **PASS, 1/1**, `route_travel_legacy_schema53_save_roundtrips_and_replays_pushed_fixture`.
- Full headless C# 9 warnings-as-errors suite: **PASS, 1,198/1,198**, PowerShell 7.6.9 / .NET 10.0.14.
- Static package structure: **PASS, 18/18 checks, 249 package assets and 249 unique GUIDs**. This is not Unity import, compilation or build validation.
- `git diff --check`: **PASS**.
- GPT excerpt-based review: no concrete push-blocker. The highest-value optional next case is an authentic schema53 save with a paused, detached route and suspended fractional traversal, followed by exact rejoin and continuation. GPT did not inspect the checkout or run the reported checks.
- Unity compilation, Edit Mode, Play Mode, standalone build and gameplay were **NOT RUN**.

The validation reports and their source hashes are retained beside this file as `FOCUSED_RESULTS.json`, `FULL_TEST_RESULTS.json` and `PACKAGE_RESULTS.json`.
