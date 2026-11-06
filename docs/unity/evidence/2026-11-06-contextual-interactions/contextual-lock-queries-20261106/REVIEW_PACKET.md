# Review packet: contextual cache and receptacle queries

Please review the current C# increment against the existing supply-cache and ordinary-receptacle procedures and shared command-query architecture. Do not infer new rules beyond the pinned procedures and owner-adopted timing policy.

## Summary

The existing supply-cache resolver supported `Interact`, but the shared query dispatcher routed it to generic fishing-trap preflight and command discovery omitted both cache and ordinary-receptacle lock options. The increment adds a pure `AssessSupplyCacheCommand` reused by query and resolution, routes cache/receptacle commands to their existing preflight logic, and offers reachable physical key/tools actions plus active attempt interruption through contextual discovery. Queries remain read-only and return the existing Action/work costs. No schema or gameplay rule changed.

## Changed C# excerpts

### Shared query routing

```csharp
if (IsSupplyCacheCommand(c)) return QuerySupplyCacheCommand(s,c);
if (IsOrdinaryReceptacleCommand(s,c)) return QueryOrdinaryReceptacleCommand(s,c);
if (c.Kind == CommandKind.Interact) return QueryFishingTrapControl(s, c);
```

### Authority-gated discovery

```csharp
private IEnumerable<Command> DiscoverContextualInteractions(Snapshot s,Authority authority,string actor)
{
    if(!authority.MayUseInventory(actor))yield break;
    foreach(var command in DiscoverSupplyCacheCommands(s,actor))yield return command;
    foreach(var command in DiscoverOrdinaryReceptacleCommands(s,actor))yield return command;
}
```

### Shared cache preflight

```csharp
private string ResolveSupplyCache(Snapshot s,Command c)
{
    string failure=AssessSupplyCacheCommand(s,c,out var cache,out var method,out var equipment);
    if(failure!=null)return failure;
    // Existing interrupt, open, tactical-attempt and timed-attempt resolution follows.
}
```

Changed source hashes are recorded in [`SOURCE_BINDINGS.json`](SOURCE_BINDINGS.json). The test file is `engine/com.decennium.foundation/Tests/EditMode/OrdinaryReceptacleCases.cs`.

## Validation and known gaps

Focused acceptance passes **1/1**; full C# 9 warnings-as-errors suite passes **1,178/1,178**; static package checks pass **18/18**, with **237 assets / 237 GUIDs**. Reports and earlier diagnosed failures are attached to this packet.

Please check that routing cache commands ahead of the generic `Interact` fallback is complete, assessment reuse preserves resolver behavior, authority-gated discovery respects access/credentials, query costs match existing resolution, and the test adequately covers query purity and interruption. Arbitrary production objects, examination, digging, marking, route discovery and excavation are intentionally outside this slice.

This packet is prepared for **Unity Rules Engine Development**. It has not yet been transmitted or reviewed.
