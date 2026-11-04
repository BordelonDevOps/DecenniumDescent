# Command query and discovery

## Purpose

The presentation layer needs to ask which existing commands are available and what they would cost, without simulating a command to find out. This is technical infrastructure over the existing authoritative command path. It does not add gameplay rules or save data.

`ICommandQueryPolicy` is optional. A policy lists the command kinds it can query, provides finite candidate commands for a controlled actor, and assesses one command against a detached snapshot. `Simulation` applies the same payload, authority, inventory permission, duplicate, revision, actor, and receipt-capacity gates used by `Execute`, then delegates to that policy. The observed revision is always the current authoritative revision.

An `Admissible` result means the command may be attempted with the current state. It does not predict an attack hit, damage result, random outcome, or later state. Costs are descriptive and transient; they reserve or spend nothing. A caller submits an accepted option through ordinary `Simulation.Execute`, where authority and state are checked again.

## Side-effect boundary

Queries must not mutate authoritative or detached state, consume RNG, create receipts, reserve resources, advance time, resolve pending choices, or expose a snapshot or future random state. Candidate commands and results are not persisted. Queries for unsupported command kinds return unsupported; other command kinds remain unchanged.

## First bounded implementation

The schema22 TEST_ONLY Repeating crossbow profile exposes the finite legal reload quantities and its authored target attack. Both query and execution use `AssessRepeatingCrossbow`; the ranged weapon layer supplies a pure pre-roll legality check. A known but unseen target location remains attackable under the existing disadvantage behavior. The query reports the Action and ammunition cost only when the command is admissible.

`RepeatingCrossbowHeadlessController` is a harness, not game AI. It chooses an admissible shot first, otherwise the largest admissible reload, and submits that command through `Simulation.Execute`. It adds no targeting, planning, or combat rules.

## Reuse boundary

Keep authoritative rules, source-bound calculations, saved world state, and transaction semantics in the existing plain C# core. Use Unity or external tactical frameworks later for presentation, editors, grid authoring, and other bounded conveniences when their licensing, compatibility, and behavior match. See [the 2026 reuse review](REFERENCE_REUSE_REVIEW_2026-11-04.md). No external runtime dependency or Unity integration is introduced by this query layer.
