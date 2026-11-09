# GPT implementation review — schema69 camp use and Pressure

## First review: commit `706a129808443c028d1d063f59f1911c1c164473`

**Actual verdict:** “Hold acceptance of 706a129: three concrete integration blockers remain.”

GPT inspected the commit diff, runtime paths and retained reports. GPT did not execute the tests or compile, decode the binary save, or independently recompute the reported source hashes.

GPT identified these blockers:

1. **Unrelated traversal blocked camp use.** Both admission and final active-use validation treated any `WorldTraversalRecord` as belonging to the camp cohort. An unrelated companion's valid traversal therefore made a valid candidate fail as `InvalidResult`. GPT requested that both checks scope the presence rule to the cohort member, with a save/restore/replay regression.
2. **Tactical turn closure rejected.** A Severe Watch checkpoint reached by `EndRegularTurn` or `EndFixedEncounter` can close active camp use with that exact command receipt. The validator accepted only `AdvanceClock`. GPT requested validation against the exact authorized clock-advancing receipt and checkpoint, including tactical turn/exit advancement and supported continuations.
3. **Movement-triggered combat left lying-low active.** `BeginWorldStep` can enter calendar combat while the outer receipt remains `BeginWorldStep`; camp transitions recognized only direct `BeginFixedEncounter` or `EnterInventoryCombat`. The still-active lying-low record then invalidated the result. GPT requested same-command tactical-entry detection and evidence that verifies the actual transition.

GPT did not treat the absent guard-duty subsystem as a blocker because that capability is disclosed as unsupported. It found the camp/combat Pressure categories, full-Watch attribution, camp context's TR-13 exclusion, companion labor and TEST_ONLY scope aligned with the agreed contract. It found no schema67/68 codec regression. An authentic pre-schema69 save with archived continuation was optional hardening, not an acceptance condition.

## Reproduction and correction

Codex added one regression for each finding and ran those exact scenarios against the reviewed `706a129` source in a detached baseline checkout. The reports reproduce:

- Companion traversal: query `Available`, execution rejected with `InvalidResult`.
- Tactical turn closure: `EndRegularTurn` rejected with `InvalidResult` at rule clock `28798/1`; no Severe checkpoint was committed.
- Movement-triggered combat: query `EncounterTransition`, execution rejected with `InvalidResult`.

The correction scopes traversal checks to the cohort member, whitelists shared-clock command kinds for Pressure closure and retains exact checkpoint/receipt identity, and ends lying-low when a `BeginWorldStep` receipt starts the encounter at that same revision. The Combat end validator independently verifies the encounter start revision.

Final validation on the correction source passes **1,289/1,289** C# 9 warnings-as-errors cases (264 source hashes), standalone Core/Persistence/LabModel compilation (193 hashes), and **18/18** static package checks (290 assets/GUIDs). Exact reports, source hashes and replay saves are indexed in [the evidence README](README.md).

The tactical-turn regression initially exposed one additional interface gap: the resolver committed `EndRegularTurn`, but the shared combat host returned `UnsupportedOperation` from its supported-command gate. Codex added `EndRegularTurn`/`EndFixedEncounter` to that gate when connected combat is active and evaluates the query through the existing detached-copy resolver path. The final regression now requires the query to be supported/admissible and verifies the same turn commits, closes against the exact Pressure checkpoint and replays after save/restore.

**Correction-commit review:** pending. The current implementation is not accepted until GPT reviews the exact correction commit and evidence and confirms the three blockers are closed and the next mapped dependency remains aligned.
