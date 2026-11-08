# GPT implementation review: schema63 Rest Watch and Rest Debt

## Review of pushed commit `ecfc8dea34a6bab27a661261e65d96289859b70e`

GPT inspected the exact commit diff, the relevant implementation and validation code, both new acceptance cases, pinned FL-03/Strain/binding sources, the consensus record, README, retained report JSONs, implementation trace, and handoff. GPT reviewed the retained evidence and did not run C# compilation/tests, package validation, or Unity checks.

GPT's result:

> I would hold acceptance for two concrete corrections. The retained tests pass, but they do not cover these paths.
>
> 1. **Rest can qualify from a stale position anchor.** `SharedRestDebt.cs` checks `ActorState.X/Y` against the safe site and explicitly permits a suspended traversal. After leaving the berth, moving partway along an edge, and suspending, the integer actor anchor still names the departure site while `WorldPositionResolver` places the actor elsewhere. `BeginRest` can therefore complete and clear debt without the actor occupying the authored berth. Canonical replay reproduces the admission error; it does not prevent it.
>
>    Minimal correction: use the shared physical-position authority for site admission. For this bounded stationary procedure, rejecting any outstanding traversal, including suspended traversal, is also a defensible conservative gate. Do not snap the actor to the berth.
>
>    Required regression: suspend after positive movement away from the berth; verify query/execution reject Rest without mutation, including after save/restore. Returning physically to the berth should permit Rest.
>
> 2. **Queries can offer movement that execution rejects during Rest.** `ResolveCore` rejects non-exempt commands with `ActorCurrentlyResting`, but movement query branches call assessments without that guard. Rest creates no worker interval or `CurrentWork` entry that would otherwise make `OrdinaryInventory.Busy` reject movement. An otherwise legal walk can be discovered as admissible while execution rejects it.
>
>    Minimal correction: share the active-Rest admission guard between query and execution, preserving the existing Rest-command and `AdvanceClock` exceptions.
>
>    Required regression: during active Rest, query and execute an otherwise legal walk and compare rejection reasons; discovery must not label it admissible. Queries and rejected execution must preserve snapshot bytes. After explicit interruption, reassess normally.
>
> The remaining inspected design is consistent with the agreed boundary: typed causal links use the single Strain history; nullable recovery flags preserve the unresolved classification; qualifying completion precedes debt assessment; the coincident due/miss ordering implements the adopted prototype policy; and schema62 retains its separate serialization branch. GPT found no additional confirmed source, duplicate-accounting, or compatibility defect in those inspected paths.
>
> The connected acceptance meaningfully tests crop work, debt, clearance and replay. Its clearance and unpaid-deadline scenarios are separate branches, as the code correctly shows.
>
> Optional hardening: add an authentic pre-change schema62 save containing Strain gains, then require byte-identical roundtrip and continuation against its archived expected result.
>
> The current handoff explicitly leaves successor selection gated on this review; it does not name an approved next module. The immediate next step is therefore these two corrections, targeted regressions and refreshed evidence for review—not moving to another dependency yet.

This response is the actual implementation-review result. It is distinct from the earlier pre-implementation design consensus in `REST_DEBT_CONSENSUS.md`.
