# Review packet: Invisible location latch

Please review this source-bound increment against the pinned `CONDITIONS_PLAYTEST.md` Invisible rule and the current implementation. Do not infer missing sensory or release rules.

## Summary

When an observer already has current location knowledge and the target becomes Invisible, the implementation correctly stops direct sight and retains that current location, but it previously failed to latch the newly active Invisible episode. The change sets the existing per-observer `RevealedInvisibleEpisodeId` to the active episode while that same location remains current. A legal unseen tactical move then invalidates current location, preserves its last-known coordinates and keeps the latch for the same episode. Existing condition journals, observer-knowledge records, movement commands and snapshot codec remain authoritative; no schema changed.

## Changed C# excerpt — `ObservationRules.Refresh`

```csharp
bool stillAtLastKnown = prior.CurrentLocationKnown && prior.LastKnownX == targetPosition.X
    && prior.LastKnownY == targetPosition.Y;
bool current = prior.CurrentLocationKnown && stillAtLastKnown;
string revealed = episode == "" ? "" : prior.RevealedInvisibleEpisodeId;
if (current && episode != "") revealed = episode;
if (current != prior.CurrentLocationKnown || revealed != prior.RevealedInvisibleEpisodeId)
    Set(s, Copy(prior, currentLocationKnown: current, revealedEpisode: revealed));
```

Changed implementation file: `engine/com.decennium.foundation/Laboratory/Model/ObservationRules.cs` (SHA-256 `0e908786c5b898b24ca764a8ac7cc725554fe49e11a99b3a0b2d315c8b2222dd`).

## Changed C# acceptance excerpt

`observation_invisible_latches_location_known_before_episode` uses actual shared-world `BeginFixedEncounter`, `DispatchConditionEvent`, `TacticalStep`, snapshot save/restore and command replay. It asserts the pre-known location is preserved while sight is removed, the current episode is latched, unseen movement invalidates current location but preserves the stale coordinate and same episode latch, both save states round-trip byte-for-byte, and replay reproduces the same initial post-Invisible bytes.

Changed test file: `engine/com.decennium.foundation/Tests/EditMode/ObservationCases.cs` (SHA-256 `3e612756c362a868513be9edd1ad5f19c554d5c1b3ff7f233d074efdaceb3997`).

## Validation

- Focused regression: **PASS 1/1**, [`FOCUSED_RESULTS.json`](FOCUSED_RESULTS.json).
- Complete C# 9 warnings-as-errors suite: **PASS 1,177/1,177**, [`HEADLESS_RESULTS.json`](HEADLESS_RESULTS.json).
- Static package checks: **PASS 18/18; 237 assets; 237 unique GUIDs**, [`PACKAGE_RESULTS.json`](PACKAGE_RESULTS.json).
- Two earlier focused failures reproduced the missing latch. An expanded test then exposed an invalid test destination, corrected and rerun successfully. All reports and diagnoses are retained alongside the passes.

## Questions for review

1. Does the refresh transition correctly latch a new active Invisible episode only when the previously current location still identifies the target's current position?
2. Does the test adequately protect persistence and same-episode continuity after unseen movement, while keeping new-episode boundary behavior explicitly outside this acceptance?
3. Do you see any interaction with Hidden state, observer isolation or existing snapshot/replay behavior that this increment should cover before moving to the next mapped C# dependency?

This packet does not claim that GPT has reviewed the current source. It is prepared for transmission to **Unity Rules Engine Development** after the current browser-capture timeout restriction allows another attempt.
