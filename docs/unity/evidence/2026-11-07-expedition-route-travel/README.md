# EXP-05 schema52 route travel evidence

This checkpoint adds a bounded, source-pinned TEST_ONLY executor for one directed expedition route segment. The candidate source is `EX58-EXACT-2026-10-11`, FL-10/TR-13, SHA-256 `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`. It remains outside the release authority registry. Exact policy and remaining limits are described in [`IMPLEMENTATION_TRACE.md`](../../IMPLEMENTATION_TRACE.md).

## Validation

- Full shared C# 9 warnings-as-errors Roslyn compile/regression suite: **PASS, 1,191/1,191**. The report contains exact source hashes and runner metadata in [`FULL_TEST_RESULTS.json`](FULL_TEST_RESULTS.json).
- Package static structure/dependency validation: **PASS, 18 checks, 242 assets and 242 unique GUIDs**. This is not Unity compilation or a player build. See [`PACKAGE_RESULTS.json`](PACKAGE_RESULTS.json).
- Tactical route pause, displacement, physical return, current-clock condition application and byte-preserving restore: **PASS, 1/1**. See [`TACTICAL_REJOIN_FOCUS_RESULTS.json`](TACTICAL_REJOIN_FOCUS_RESULTS.json).
- `git diff --check`: **PASS** after the documentation and evidence updates, before commit.
- GPT pre-push excerpt review: **No blocker found**. It confirmed the short-terminal and pre-schema52 journal fixes, endorsed committing this bounded increment, and did not inspect the complete local diff or run the reported checks. It suggested one optional regression for a route-position crossing coincident with an immunity expiry that removes movement permission.
- Unity compilation, Edit Mode, Play Mode, player build, visual playability and performance: **NOT RUN**.

The full suite includes these route cases:

- `expedition_route_rate_and_mapping_arithmetic_are_exact`
- `expedition_route_shared_clock_save_pause_pace_change_and_management`
- `expedition_route_rejects_unresolved_risk_quality_mapping_and_capacity`
- `expedition_route_rejects_partial_terminal_progress_before_play`
- `expedition_route_tactical_entry_pauses_and_preserves_off_anchor_rejoin`
- `expedition_route_and_observation_profile_composition_fails_closed`
- `condition_combat_pre_route_schema_reads_keep_their_original_journal_clock`

The connected route acceptance verifies shared-clock effort while an existing companion movement and crop task proceed; condition expiry without per-tick journal growth; actor-specific movement restrictions and future path reservation; pause without progress; paused off-route save/restore and rejected off-anchor resume; physical return to the route anchor; burden-derived pace change affecting only future effort; tactical entry pausing travel; exact Progress-to-position binding; segment completion; idempotent start; and save-byte stability. Risk, quality, Unknown mapping, insufficient capacity, and profiles with a short terminal Progress segment are rejected without state mutation. Whole-multiple terminal lengths avoid inventing whether a partial final Progress award should pay for a full 480-minute segment. Sparse condition projection is enabled only at schema52 and later; schemas1–51 retain the old condition-read behavior.

## Key source hashes

The full suite report is authoritative for every compiled input. Selected hashes at this checkpoint:

| File | SHA-256 |
| --- | --- |
| `Laboratory/Model/SharedExpeditionRouteTravel.cs` | `b6b7f1e6a859acadc63c584defb1a00a491e0a21dee40e18171715936499dde4` |
| `Runtime/Core/ExpeditionRouteTravelRecord.cs` | `ca1e7a1c4651f22f6947b5a84583242531f9dd1733cabb2b10c7c3fad124b867` |
| `Runtime/Persistence/ExpeditionRouteTravelCodec.cs` | `267fbb6fdc6dc635beb878401a0418cfb2a0d4afa143f3874327c3c9ed18338b` |
| `Tests/EditMode/SharedExpeditionRouteTravelCases.cs` | `19103557171448c5d81482f43f61430d603e41b9c402e269f9bdc4bb1781c809` |
| `Laboratory/Model/ConditionCombatPolicy.cs` | `5ebe8084c4606ee0cdcd7b28438600c5ee58b51db78be03aca586e53823edd30` |
| `Runtime/Core/ActorConditionRecord.cs` | `a58b8ceb15fe17cab04958da380a186725d2860b86edbf5057d8ce6a8f802384` |
| `Tests/EditMode/ConditionCombatCases.cs` | `ca42aee45380d94060aef3445b169a3dd2d82ae66c36c0ed034cd93d7685b9fe` |
| `Runtime/Core/Simulation.cs` | `88d64286583b28aa66ba8b4748d41da0e5c18fb45a5ec03ea85f548abb1824cf` |

These hashes identify the tested checkpoint after terminal-segment and pre-schema52 condition-read review fixes.

The next C# dependency is route-to-Observation integration using explicitly authored physical path/time bindings. The connected acceptance should cover observer-specific sighting, tactical pause/displacement, paid physical return, explicit route resume, destination work, and split-time/save-restore equivalence. Keep route/Observation composition rejected until that path is implemented; do not infer intermediate geometry from abstract Progress.
