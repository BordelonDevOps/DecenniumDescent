# Run the connected work session

This is the source-bound **TEST_ONLY C# console session**, with filling, exposed-node mining, recipe4 research and recipe4 manufacturing connected to the existing exploration, encounters and inventory. Unity remains deferred. The module's final acceptance status is recorded in [the packet README](README.md).

From the repository root, use PowerShell 7:

```powershell
pwsh -NoProfile -File engine/tools/Open-ConnectedExpedition.ps1 -ConnectedWorkControl
```

The launcher compiles the current source when no `-AssemblyRoot` is supplied. To use the exact locally retained qualification DLLs, add:

```powershell
-AssemblyRoot engine/artifacts/connected-work-control/development-10/run-20261123T200453593Z-83a83fc6
```

Enter one JSON request per line. These requests inspect current state and available work without spending time or resources:

```json
{"op":"view","seat":"Player"}
{"op":"work","seat":"Player","actor":"TEST_ONLY.companion"}
{"op":"discover","seat":"Player","actor":"TEST_ONLY.companion"}
{"op":"work","seat":"Player","actor":"TEST_ONLY.actor"}
{"op":"discover","seat":"Player","actor":"TEST_ONLY.actor"}
```

Discovery supplies the actual command parameters and current query result. Submit through the console's `submit` operation; use `query` first to check the same request. Read the current work record for job identifiers and allowed controls. Actor authority, position, stock, capacity, tools, knowledge and work windows still govern each command. An unavailable operation supplies no replacement rule or free resource.

Filling, research and manufacturing expose pause, resume and cancellation. Mining exposes pause and resume only. Manufacturing's quality decision remains explicit, and cancelling its selected batch permanently closes that order. The session preserves these native differences.

Use an unused path for a new save:

```json
{"op":"save","path":"work-control-session.ddsave"}
{"op":"load","path":"work-control-session.ddsave"}
```

Type `help` for the inherited movement, clock, combat and handling inputs; type `quit` to leave the console. Genuine execution requests and responses for the complete route are retained under `five-paths-02/ConsoleUninterrupted/inputs.jsonl` and `responses.jsonl` in `QUALIFICATION_SUPPLEMENT_04.zip`. The archive also contains the separate cancellation/resumption branches. These histories document the exercised route; importing an older-profile save into this fresh profile is not supported.
