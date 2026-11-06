# Review packet: tactical Search query and discovery

This no-schema-change implementation excerpt and behavior summary were reviewed against the prior Search query/discovery consensus. GPT found no blocking defect in the supplied material and confirmed the information boundary, deterministic discovery, Action cost, and unchanged resolver. It recommended coverage for a spent Action, invalid query bounds/range, no admissible option after spending, and rejection purity; those checks have since been added and rerun locally. GPT did not independently run the local checks. Do not reopen the settled Search execution semantics or propose exploration costs.

## Implementation

`SupportsCommand` now admits `Search`, and `QuerySharedWorldCommand` explicitly routes it to `QueryObservationSearchCommand`; this prevents fallback to the unrelated ranged-combat query. The shared assessment validates the tactical Action prerequisites and the explicit candidate request, but does not inspect Hidden occupancy, target identities or a Hide total:

```csharp
private string AssessSearchRequest(Snapshot s, Command c, out ObservationPoint candidateCell)
{
    candidateCell = default;
    if (c.Target != s.Encounter.CurrentTurnId || c.X < 0 || c.Y < 0
        || c.X >= s.ObservationMapWidth || c.Y >= s.ObservationMapHeight) return "InvalidSearchRequest";
    var profile = s.ObservationProfiles.Single(x => x.ActorId == c.Actor);
    var searcher = ObservationGeometry.Position(s, c.Actor);
    candidateCell = new ObservationPoint(new RuleQuantity(c.X), new RuleQuantity(c.Y));
    return WithinRange(searcher, candidateCell, profile.SearchRangeFeet) ? null : "SearchCellOutOfRange";
}

private CommandQueryResult QueryObservationSearchCommand(Snapshot s, Command c)
{
    string failure = AssessObservationAction(s, c, out _);
    if (failure == null) failure = AssessSearchRequest(s, c, out _);
    var costs = failure == null ? new[] { new CommandCost("action", "", 1) }
        : Array.Empty<CommandCost>();
    return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
}
```

Tactical discovery enumerates every in-range authored grid cell, in row-major order, independently of hidden occupancy:

```csharp
for (int y = 0; y < s.ObservationMapHeight; y++)
for (int x = 0; x < s.ObservationMapWidth; x++)
{
    var candidateCell = new ObservationPoint(new RuleQuantity(x), new RuleQuantity(y));
    if (!WithinRange(searcher, candidateCell, profile.SearchRangeFeet)) continue;
    string id = "option." + s.Revision.ToString(CultureInfo.InvariantCulture)
        + ".observation.search." + x.ToString(CultureInfo.InvariantCulture)
        + "." + y.ToString(CultureInfo.InvariantCulture);
    yield return new Command(id, actor, s.Revision, CommandKind.Search, turnId, x, y);
}
```

The existing `ResolveSearch` still resolves zero-or-one hidden occupant, spends the existing Action on a valid Search, and reveals location only to the searcher. The prior GPT/Codex review confirmed the multiple-occupant case is unreachable in validated snapshots and legal movement for this host; `SearchCandidateAmbiguous` remains defensive code.

## Acceptance and results

The existing `observation_shared_hide_search_save_replay_and_observer_isolation` case now also checks that a public Search query returns an Action cost without mutating snapshot bytes; after Hide and turn handoff, discovery includes both the hidden target's cell and an empty in-range cell with equal availability and cost, without mutation. Its existing trace then executes successful Search and verifies location-only observer disclosure, save/restore and deterministic replay.

- Focused case: **PASS 1/1**, [`FOCUSED_RESULTS.json`](FOCUSED_RESULTS.json).
- Complete C# 9 warnings-as-errors suite: **PASS 1,178/1,178**, [`HEADLESS_RESULTS.json`](HEADLESS_RESULTS.json).
- Static package checks: **PASS 18/18; 237 assets / 237 unique GUIDs**, [`PACKAGE_RESULTS.json`](PACKAGE_RESULTS.json).
- The first compile run failed before test discovery (`CS0246`, missing `System.Collections.Generic`, **0/0** cases). The import was added and all listed passes were rerun successfully. See [`FAILED_COMPILE_RESULTS.json`](FAILED_COMPILE_RESULTS.json).

The follow-up review case now also queries `X == map width` and an in-bounds cell beyond SearchRange, then confirms both fail without costs or mutation. After a successful Search spends the Action, a fresh query returns `ActionAlreadySpent` with no costs; discovery returns no admissible Search options; direct execution rejects with the same code and preserves bytes.

Changed-source SHA-256 bindings are in [`SOURCE_BINDINGS.json`](SOURCE_BINDINGS.json). Please identify only a concrete defect or a regression that materially improves confidence in the implemented contract.
