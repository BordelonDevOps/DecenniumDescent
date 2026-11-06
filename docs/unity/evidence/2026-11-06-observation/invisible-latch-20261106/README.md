# Invisible location latch — 2026-11-06

## Responsibility and boundary

This increment corrects observer-knowledge refresh when a target becomes Invisible after its location is already known. `ConditionJournal` remains authoritative for active Invisible applications and the current continuous episode. `ObserverKnowledgeRecord` remains authoritative for each observer's current/last-known position and revealed-episode latch. `ActorState`, tactical movement, shared commands, `RuleClock`, RNG, receipts and `SnapshotCodec` remain authoritative for position, costs, deterministic execution, replay and persistence. No saved schema or global state changed.

The bounded TEST_ONLY acceptance uses the existing shared-world fixture. It does not define new Invisible rules; it implements the pinned continuous-episode disclosure rule. The test does not cover all episode boundaries, such as ending an episode and beginning a later one, or overlapping applications.

## Failure diagnosis

The first focused command trace established that the observer knew the target's location before Invisible. Applying Invisible correctly removed direct sight and preserved current location, but `ObservationRules.Refresh` left `RevealedInvisibleEpisodeId` empty. The isolated regression failed on that latch assertion. The code now copies the current episode ID into the existing observer record only when the previously known location still matches the target's current position. Unknown or stale locations do not get newly latched by this branch.

The expanded regression initially failed with `InvalidTacticalStep`: the fixture used absolute destination `(0,1)` although the target starts at `(4,0)`. The failure was in the test's nonadjacent destination. Changing it to `(4,1)` made the step legal; the final acceptance confirms unseen movement invalidates current knowledge while preserving old coordinates and the episode latch.

Both failure classes were retained in [`FAILED_LATCH_COMBINED_RESULTS.json`](FAILED_LATCH_COMBINED_RESULTS.json), [`FAILED_LATCH_ISOLATED_RESULTS.json`](FAILED_LATCH_ISOLATED_RESULTS.json), and [`FAILED_COORDINATE_REGRESSION_RESULTS.json`](FAILED_COORDINATE_REGRESSION_RESULTS.json). The initial narrow code-fix pass and final expanded pass are retained separately.

## Validation

- Focused C# 9 warnings-as-errors acceptance: [`FOCUSED_RESULTS.json`](FOCUSED_RESULTS.json), **PASS 1/1**.
- Full shared C# 9 warnings-as-errors suite: [`HEADLESS_RESULTS.json`](HEADLESS_RESULTS.json), **PASS 1,177/1,177**, zero failed.
- Static package validation: [`PACKAGE_RESULTS.json`](PACKAGE_RESULTS.json), **PASS 18/18; 237 assets; 237 unique GUIDs**. This is a static package check, not Unity compilation or runtime validation.
- [`SOURCE_BINDINGS.json`](SOURCE_BINDINGS.json) records tested source hashes, report links and the pending review status.

