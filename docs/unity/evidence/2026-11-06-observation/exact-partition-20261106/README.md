# Exact path observation and historical replay — 2026-11-06

## Increment scope

This TEST_ONLY C# increment makes exact visibility interval handling symmetric when either actor moves. The shared `ObservationRules` path classifies stable intervals with interior points, records actual visible boundaries and stores the excluded point where sight ends as `DirectSightLimit=4`. A moving target produces stale location knowledge; a moving observer does not make a stationary target's known position stale. Hidden is cleared only when that observer actually had sight.

Schema51's serialized observation layout remains unchanged. `ExactPathIntervalsV2` is the default fingerprinted profile. `LegacySampledV1` retains the original algorithm and fingerprint for historical command receipts; it is an explicit profile, not an automatic migration. The saved `ObserverKnowledgeRecord` evidence revision continues to reflect the command history, so partition-equivalence comparisons compare every knowledge field except that provenance revision.

## Responsibilities, records and dependencies

- Authoritative position and partial movement: existing `ActorState` and `WorldTraversalRecord`.
- Observer-specific current/stale location, evidence and Hidden/revelation state: existing `ObserverKnowledgeRecord` and hide/result records.
- Clock, RNG, condition lifecycle, receipts, and persistence: existing shared simulation, condition journals, command receipt history, `RuleClock`, and `SnapshotCodec`.
- Exact geometry: `ObservationGeometry.VisibilityBreakpoints` over the existing authored cell map and per-actor sight profiles.
- Profile selection and replay: `TestOnlySharedWorldPolicy.EnableObservation` binds the chosen algorithm into `ContentFingerprint`; no global rule state is used.

The remaining rule gap is sensory information outside this authored planar sight model: sound/event evidence, other Invisible episode edges, and attack/reaction disclosure remain separate work.

## Runnable acceptance

- `observation_exact_intervals_cover_moving_observer_and_blocked_continuation`: exact moving-observer sight loss, stationary target remains known, partial save/restore, whole versus split knowledge-set comparison, and stale evidence survives a wholly blocked continuation.
- `observation_exact_path_retains_latest_of_multiple_exposure_intervals`: moves a target along authored adjacent route legs with two opaque sight windows; blocked legs retain prior evidence and later direct exposure replaces it.
- `observation_tactical_hide_survives_exit_then_legal_exploration_sighting_is_observer_specific`: legal tactical Hide, encounter exit, whole/split traversal, and save/restore immediately at target sight loss.
- `observation_legacy_schema51_sampled_profile_replays_pushed_save`: decodes a save created by the pushed pre-change implementation, replays its receipts under v1 and verifies byte-identical restoration; v2 rejects the old fingerprint.

The geometry-only route fixture explicitly relocates its actor and holds the test clock fixed so condition-journal clock invariants remain intact. It isolates the path observation procedure; it does not claim a new traversal command, production map or general content rule. The separate Hide/exit test exercises the real command path and clock.

## Historical save provenance

`LEGACY_SCHEMA51_SAVE.bin` is a 5,520-byte snapshot produced by `a2701c20a28e642c6f2d920982211b1426875e5c` from a `git archive` of the pushed source. Only a temporary copy of that commit's `ObservationCases.cs` was instrumented to write the test's returned final bytes; the repository source for the old implementation was not changed. Its SHA-256 is `648b91683a742bf03807b0d945a29563eba88a112e41ce0c75f2dbdbb4354a35`. The test embeds the same payload in [ObservationLegacySaveFixtureCases.cs](../../../../../engine/com.decennium.foundation/Tests/EditMode/ObservationLegacySaveFixtureCases.cs).

## Validation

| Check | Result |
| --- | --- |
| Focused observer-motion case | PASS, 1/1 |
| Focused multi-exposure case | PASS, 1/1 |
| Focused pushed-save legacy replay | PASS, 1/1 |
| Focused legal target-boundary partition and restore | PASS, 1/1 |
| Full C# 9 warnings-as-errors suite | PASS, 1,182/1,182; Core, Persistence, LabModel and headless tests compiled |
| Static package validation | PASS, 18/18 checks, 238 assets and 238 unique GUIDs |
| `git diff --check` | PASS, clean after LF normalization and final evidence refresh |

The failed package check and unchanged reproduction are retained as `FAILED_PACKAGE_METADATA.json` and `FAILED_PACKAGE_METADATA_REPRODUCTION.json`. Both identified the new test source's missing metadata sidecar; adding its fresh GUID made package validation pass. The source hashes for the full successful compile are embedded in `FULL_TEST_RESULTS.json`.

## Changed source hashes

```text
13d6f2c1ef459ccc294d335948b77abc40e1af0276fae06f3960ca87695c1786  ObservationRecords.cs
7d1854a675749dfa49608890d3b69e66eadd31a5d2bf6070ea0bc1281bea03c9  ObservationGeometry.cs
dd74faab67ee8c035a8e8c846779dcc8d128318fc96fb7f95804528d9f546f6c  ObservationRules.cs
33155fa7e690ff81d53205d989dd6fb991be312f0b2df73310675c5e75e18b1f  SharedWorldCombatPolicy.cs
c7423a8353bb1260aa5a03a968293dd4ca6c1490b70e46ab8b09a97435a74f12  TestOnlySharedWorldPolicy.cs
09ca41fc1c27605803ac0bc103d5dcbcc629b08955b58abd025de8262a7bad96  ObservationCases.cs
d805acd40bfdee51314ffb8cca1d4d1146d0f01c5154c002d3448b8139f286e8  ObservationLegacySaveFixtureCases.cs
```

## Independent review

The review packet is being sent to **Unity Rules Engine Development** after these results were collected. Update this section with GPT's findings when returned; GPT does not run the local validation commands.
