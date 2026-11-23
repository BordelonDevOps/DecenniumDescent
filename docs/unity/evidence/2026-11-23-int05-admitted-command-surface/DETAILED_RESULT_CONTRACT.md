# Proposed V1 transaction and result interface

**Design revision after actual GPT response `e9ba59d7-ba74-59dc-9f2f-0a5cc2d7ac31`; not accepted for implementation.** This completes the architectural proposal, not the still-open operation/field matrix. The original review is retained verbatim in GPT_ARCHITECTURE_REVIEW_01.json.

## Exact proposed endpoint responsibilities

All methods belong to the existing trusted `ConnectedExpeditionSession`. `Command` retains its existing constructor, payload and fingerprint. Read calls take `long expectedObservationRevision`; this is independent of the command's original ExpectedRevision. All projections are immutable, version 1, with the observed revision and existing TEST_ONLY identity.

| Method | Arguments | Result |
| --- | --- | --- |
| `SubmitCommandV1` | `ExpeditionSeat seat, Command command` | `ExpeditionSubmissionV1` |
| `SubmitSessionCommandV1` | `Command command` | `ExpeditionSubmissionV1`; only existing AdvanceClock/EndFixedEncounter operator route |
| `SubmitDefenderIntimidatingPresenceV1` | `Authority grant, Command command` | `ExpeditionSubmissionV1`; exact existing trusted Presence route |
| `SubmitDefenderSanctuaryV1` | `Authority grant, Command command` | `ExpeditionSubmissionV1`; exact existing trusted Sanctuary route |
| `AdvanceAutomaticDefenderV1` | none | `ExpeditionAutomaticSubmissionV1`; one native plan and one dispatch, existing trusted controller selection |
| `ExplainResultV1` | `ExpeditionSeat seat, Command exactCommand, long expectedObservationRevision` | `ExpeditionResultExplanationV1` |
| `ExplainSessionResultV1` | `Command exactCommand, long expectedObservationRevision` | same; SessionPrincipal and exact existing operator grant |
| `ExplainDefenderResultV1` | `Authority grant, Command exactCommand, long expectedObservationRevision` | same; actual trusted LaterDefender grant/principal, covering both explicit Presence/Sanctuary and existing automatic-controller command kinds |
| `DescribeSessionCommandsV1` | `long expectedObservationRevision` | `ExpeditionCommandCatalogV1`; existing operator kinds only |
| `AssessSessionCommandV1` | `Command command, long expectedObservationRevision` | `ExpeditionAssessmentV1` |
| `DescribeDefenderCommandsV1` | `Authority grant, long expectedObservationRevision` | `ExpeditionCommandCatalogV1`; existing explicit defender kinds and automatic capabilities, with their distinct dispatch routes |
| `AssessDefenderCommandV1` | `Authority grant, Command command, long expectedObservationRevision` | `ExpeditionAssessmentV1` |
| `DescribeDefenderChoicesV1` | `Authority grant, long expectedObservationRevision` | `ExpeditionChoiceCatalogV1`; only decisions owned by the authorized defender |

Player description/discovery/choices/assessment remain as specified in SOURCE_API_CONTRACT.md. A separate operator choice catalog is unnecessary because no player choice is owned by SessionPrincipal; its suspended command reports a current continuation requirement and only disclosable participant identities. This does not grant the operator an extra gameplay response command.

The embedding host binds these methods to trusted callers, as it already does for `SubmitSessionCommand`, save/restore, seat enablement and defender submissions. Console dispatch may choose these existing trusted host operations, but serialized JSON must never construct an Authority, principal, inventory grant or seat privilege. An explanation searches exactly the bound principal's receipt. Command ID alone never authorizes searching another principal's receipts. Automatic defender results identify the actual selected route/principal internally; the authorized public explanation uses that route, with Ferry requiring its current creature seat and LaterDefender requiring its actual trusted grant.

## One authoritative attempt

Refactor the existing session's submission dispatch into an internal result carrier shared by legacy and V1 wrappers. Keep the exact existing order of seat/enabled/control checks, exposed kind, narrowly selected grants, malformed payload, prior-ID conflict, fresh revision/known-target admission and `Simulation.Execute`. The core separately checks current actor/inventory authority before accepting a duplicate. This is not one newly reordered universal chain.

The internal carrier holds the legacy response, actual native CommandResult when execution was reached, host rejection stage when it was not, and bounded facts observed from the real pre/post state under the same gate. It invokes `Simulation.Execute` at most once. No preceding assessment supplies the alleged execution result. No second query, replay, resolver, RNG draw, copied-state simulation or speculative settlement fills missing details. A failing host/core attempt has no new receipt or gameplay mutation; its actual safely disclosable reason is returned immediately. Existing exception and rollback behavior remains intact.

The V1 result includes the exact legacy response as an immutable compatibility projection. Legacy methods use that projection and retain response meanings, visibility, ordering and null/empty behavior. Native-code exposure is allowlisted per failure/source family; a protected rejection becomes `Withheld` or the appropriate safe host diagnostic in the new projection, without changing which check ran or what the legacy endpoint returns. Details cannot expose hidden IDs, private stock, DC, RNG state or an unobserved target through a reason-code oracle.

For automatic control, planning and dispatch remain the existing controller operations under the same gate. Both controllers bypass the session Execute helper and call Simulation.Execute in their own private Execute methods. The internal carrier must therefore pass through `LaterDefenderController.Dispatch/Execute` and `FerryWraithController.Dispatch/Execute` as well as the session helper. Preserve each controller's distinct primary/fallback admission order, stale duplicate handling and status mapping. Capture the actual selected command, which can be the fallback, and the one actual native result if execution is reached. If dispatch stops at admission, capture the actual safe admission/status instead. Do not run Plan, Assess or Execute again to recover information discarded by the legacy wrapper. Unused primary/fallback requests are not represented as executed commands.

`Waiting` is distinct from a rejected command. It can follow no planned command or a native rule-denied admission; retain whether a candidate was assessed and whether authoritative execution was reached. When no command was executed, a new execution receipt is NotApplicable. Preserve current defender and Ferry grant/revocation behavior. Do not fabricate a command merely to make every control call look like a receipt-bearing attempt. Automatic command descriptions/assessment and receipt explanations do not add a new manual submission route for those kinds.

## Submission result semantics

`ExpeditionSubmissionV1` carries API version, actual legacy response, attempt disposition (`Committed`, `Duplicate`, `Rejected`), before/after observation revisions, safely disclosed actual stage/code, optional matching receipt revision, facts and current continuation description. `ExpeditionAutomaticSubmissionV1` additionally permits `Waiting` with no authoritative execution, retaining an optional actually assessed candidate and admission stage. This vocabulary does not add a native gameplay outcome.

Keep the actual native result revision separate: on Duplicate, `CommandResult.Revision` is the original receipt revision, while legacy `ExpeditionActionResult.Revision` is the current snapshot revision. Do not overwrite either field with the other. A committed failed contact may have paid elapsed movement without entering combat; Committed is not a promise that every requested gameplay consequence succeeded.

Commit/duplicate/rejection and suspension are separate axes: a committed clock request can suspend for a choice. On a fresh commit, immediate continuation status is the actual status at the end of that attempt; on a duplicate it is the current continuation observation. A duplicate is not a new application of damage, payment or time. Facts must say whether they concern the original commit, a later resolving operation, or the current observation.

Native `CommandResult.IsSuspended` only represents its manufacturing/recovery pending-clock convention. Sanctuary, knockout, Opportunity or Press may be pending while that flag is false; preserve it as the native clock field and expose actual authorized tactical pending status separately. Core AcceptedResult is not an exhaustive contact projection for PostRecovery or Ferry, whose own retained records must supply their facts.

An actual bounded pre/post change may be an immediate fact only where the fact matrix authorizes it and its temporal scope is explicit. For example, an authorized character's HP difference across the actual attempted transaction may summarize that interval; it cannot attribute every due effect to the initiating attack. Prefer native retained causal records for individual outcomes. Do not compute game rules, predicted deltas, prices, damage, cures or future work settlements in the host. Rolled-back candidate effects are never reported as committed facts.

The returned immutable object may be retained by the caller. It is not added to the snapshot, save format or engine ledger. A rejected attempt has no receipt and cannot later be recovered by `ExplainResultV1`; the immediate response remains mandatory. If an accepted operation's immediate detail is not natively retained, a later explanation explicitly says NotRetained for that field. Existing supported saves need no new record or backfill.

## Per-field result contract

Each entry in the result matrix must specify all of: operation/semantic branch, fact key, exact native record or immediate observation source, initiating principal/ID/revision, any later resolving command, temporal meaning, disclosure predicate and availability. Native reference chains must be checked; equality of time, actor or target is not sufficient causal binding.

| Disposition | Meaning |
| --- | --- |
| `Immediate` | Safely observed from this actual submission transaction; no promise of later restoration. |
| `Retained` | Native causally bound state can supply the fact after save/restore under current disclosure rights. |
| `NotRetained` | The historical fact is not stored; no recomputation/backfill. This is not a replacement for required immediate explanation. |
| `NotApplicable` | The field has no meaning for this operation/disposition (for example, no payment on a rejected or duplicate attempt). |
| `Withheld` | A fact may exist but current authorization/visibility does not permit disclosure; do not reveal its private existence/value. |

Temporal meaning is separately `OriginalCommit`, `ResolvingCommit`, `AttemptInterval`, `CurrentObservation` or `CurrentContinuation`. A retained record can change status after its originating command; label that status as current unless the record retains the historical event separately. `AcceptedClockAwaitingChoice` is a current-pending predicate. A later lack of pending state cannot prove the original clock never suspended. Likewise, a knockout response can resolve an earlier attack without becoming that attack's origin.

Authorized receipt metadata excludes the raw fingerprint and internal serialized payload. Exact match is checked internally. Current actor/inventory authority and the exact narrow transaction grant are required; historical access does not survive revocation automatically. Current target visibility may suppress details even when native exact-retry authority still recognizes the receipt. Read freshness is checked against expectedObservationRevision without rewriting the submitted command or re-running its original eligibility.

Authority is evaluated per fact, not just per endpoint. ClockGrant authorizes the operator's clock command and applicable clock/receipt facts; it does not confer unrestricted actor, inventory, mining, damage, target or Director disclosure. A trusted defender grant likewise does not become the party's inventory grant. Rich facts without an applicable current disclosure predicate remain Withheld.

Specific projection constraints from the independent native audit: a melee attack's ID is derived from revision, so bind its Revision to the receipt and its ResolvedRevision separately to a later knockout response. Its effective Damage.Total is not an actual-HP-loss ledger. A Press move's CostPaid is not universally ordinary movement spent; preserve move kind and its separate entitlement/resource semantics. Press-offer Accepted is not proof of completed travel: the linked child movement may still await reactions or be interrupted. None of these constraints changes the accepted mechanic.

The complete operation matrix and disclosure tests remain required before source/API acceptance. This document does not close HC-D6 or HC-D7 by itself.
