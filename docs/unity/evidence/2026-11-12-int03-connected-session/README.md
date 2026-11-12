# INT-03 connected C# session

`ConnectedExpeditionSession.Start()` starts the ordinary recipe-4 TEST_ONLY profile at revision zero. The four local grants cover the party, the first opponent, the automatic later defender, and session operations. The player uses hero and companion commands. The director uses only the first opponent's ordinary tactical commands and equipment. The accepted controller chooses each later defender action. The trusted local host can advance the shared clock, request a resolver-validated encounter exit, and save, restore or recover a file. A local operator can switch between the two labelled human seats.

The view contains owned actors and applicable conditions, inventory and work, per-actor sight of tactical opponents, and the seat that owns a pending response. Only the responding human seat gets the opportunity token or manufacturing order for the pending choice. Historical Haven sale proceeds have their own field. General rule denials use `Unavailable`. Command IDs and expected revisions preserve stale, conflicting and duplicate delivery behavior. The host can revoke either human seat. Save and restore use the existing wire95 codec and complete external validation before replacing the live session. The session uses opt-in verified-prefix execution after validated startup or restore. It validates saves for its selected profile. Other fixture compositions continue to use their existing loaders.

## Run the session

Use PowerShell 7 in the repository root.

```powershell
pwsh -NoProfile -File engine/tools/Open-ConnectedExpedition.ps1
```

Enter `help` for the local operations and `quit` to exit. Each input is a single JSON line. Start with `{"op":"view"}` and use `{"op":"view","seat":"FirstOpponent"}` during the first opponent's turn. Walking uses an adjacent cell delta and a subsequent clock advance. Tactical steps use absolute cell coordinates and the active turn ID. `SelectCombatStance` and `AttackClub` take a `combat` payload with the current turn ID. The player or director can take the current acting actor from its own view. Supply `actor` for ordinary activity outside combat. For a deliberate retry, supply the original `id`, `revision` and resolved arguments, including the original `combat.turn` for a tactical input. The console generates an ID and reads the current revision when those fields are omitted.

The retained `walkthrough.jsonl` contains every input and the real pending save and load. Run it from an empty working directory so its relative `pending.ddsave` points at a fresh file. Pass absolute paths to the launcher and walkthrough. Supply `-AssemblyRoot` to reuse a C# 9 build from `engine/tools/Compile-Foundation.ps1` or the exact retained assemblies. The walkthrough submits actual choices from revision zero, then lets the accepted automatic controller select and commit each of its own decisions.

The selected TEST_ONLY scenario demonstrates ordinary traversal, two tactical encounters, mining and physical ore handling, sale and provisioning, charter departure and return, preservation, research, native recipe-4 manufacturing, a real interrupted tactical move, dose use and continued ordinary travel. Its authored setup uses the ordinary MGT-04 profile. The earlier TAC-10 timing and controller witness used dormant condition fixtures for separate control branches. The walkthrough uses its command inputs as a reproducible choice sequence and compares the new session's own uninterrupted and restored bytes.

## Scope and source

The session changes the local input, observation and file adapter. It calls the existing resolvers and selected TEST_ONLY scenario. The supported operations and selected service identities are in the C# API. Static service identities are known scenario inputs, and the resolver checks current legal access and timing. Production authority, wire layout and Unity gameplay integration remain at their prior gates.

The subsequent INT-03 requirements still need their own bounded evidence. EXP-03 needs a finite receptacle depletion and revisit. EXP-04 needs actual paid Hide and Search through the session. EXP-05 needs a paid local route, fractional restore and finite-site revisit. MGT-06 needs the admitted finite physical trap lifecycle. The current API returns the generic response for unsupported input. [Approved sequence](../2026-11-12-int03-playability/GPT_REVIEW.md) · [Session map](../2026-11-12-int03-playability/SESSION_SCOPE.md)
