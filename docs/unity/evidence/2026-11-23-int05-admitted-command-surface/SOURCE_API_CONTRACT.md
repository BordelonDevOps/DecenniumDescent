# INT-05 source and API contract proposal

**PROPOSED; HC-01–05 and the inventory/evidence plan are not yet accepted.** The actual recommendation selects this module for design, not implementation. Preserve the baseline and all previous exact acceptances in MODULE_DEFINITION.md. This contract changes no gameplay rule or source authority.

## HC-01 — Complete admission inventory and additive compatibility

Use a new additive, explicitly versioned headless surface, proposed version `1`, available on every supported `ConnectedExpeditionSession` factory. Keep existing `View`, casting/work query/discovery, work/terrain/seal/Ferry views, manufacturing-quality explanation and submission endpoints with their published signatures and historical ordering. The new API must not require the newest work-control composition merely to inspect an older supported session.

Proposed public entry points on the existing trusted session:

| Entry point | Input | Immutable result |
| --- | --- | --- |
| `DescribeCommandsV1` | seat, actor, expected revision | Applicable operation descriptions, parameter domains, known unsupported dispositions and deterministic example requests; examples explicitly are not exhaustive rational domains or permission tokens. |
| `AssessCommandV1` | seat, exact command | Versioned supported/admissible/disposition result, observed revision, source-bound known costs, prerequisites and conditional consequences. Duplicate receipt disposition is distinct from fresh admissibility. |
| `DiscoverCommandsV1` | seat, actor, expected revision | Deterministically ordered native candidates and their assessments, plus descriptions for lawful domains that cannot be exhaustively enumerated. |
| `DescribeChoicesV1` | seat, actor, expected revision | Actual pending decisions and embedded elections, stable decision/offer identity, native priority, alternatives/domains and visible consequences. |
| `ExplainResultV1` | seat, exact submitted command, expected observation revision | Authorized matching receipt and native retained outcome facts, each with causal origin; explicit limitations for facts never retained. No historical re-execution. |
| Separate operator assessment/description | exact operator command, expected revision | The existing clock/close authority only; not a player-seat privilege. |

Final type/method names may be adjusted during design, but not their coverage or authority. A version field identifies the host representation, not a gameplay fingerprint. No new authoritative state, save schema, fingerprint, migration, command kind, resource grant or historical backfill is proposed. A real need for one must be returned for source/API review before implementation. Existing submission remains the sole mutation path.

The operation matrix must cover all 78 candidate kinds, all 24 exact startup declarations and their selected parameters, and the intersection of host and native admission. Two session-operator kinds (`AdvanceClock`, `EndFixedEncounter`) remain separate. Save/restore/recovery, seat enablement, automatic defender dispatch, explicit defender Presence/Sanctuary submissions and read views are host capabilities, not added player commands. `AcquireEarnedSpell` retains its existing advancement-transaction denial; repertoire knowledge alone must never admit casting or acquisition.

## HC-02 — Pure assessment shared with execution

Build reusable native assessment facts consumed by both the new queries and existing execution handlers. Extract eligibility from the actual resolver before side effects; do not copy the rules into a presentation switch. Preserve native gate order, payment point, time, continuation and outcome. Existing core identity/authority/preflight code must be reused. State may be detached defensively for inspection, but the new assessment/explanation path must not execute a command, draw RNG, settle deadlines, create receipts, reserve stock or resolve a choice even on a copy.

Existing queries that execute `ResolveCore(s.Copy(), ...)` do not mutate the live session. They nevertheless need explicit replacement or isolation when used by the new surface. The inventory records rest, meal, turn/close, physical inventory/portable equipment and other relevant paths. Do not feed the new surface through legacy speculative queries just because canonical state is unchanged.

The knockout branch is a concrete extraction hazard: `TestOnlyClubAttackPolicy.Resolve` calls `Complete` and `AdvanceTacticalFlow` for an existing pending attack before any `assessTactical` return. Adding the command to `SupportsCommand` and reusing that flag is insufficient. Extract a pure knockout response assessment shared with `Complete`; independently assess any permitted continuation constraints without resolving or revealing its future randomness. Apply the same scrutiny to all helper flags; a name such as `assessTactical` is not a purity proof.

The same audit applies to `TacticalMovementPolicy.ResolveTacticalChoice`: its Press branch changes the offer, tactical state and movement continuation without an assessment return. Extract pure Press eligibility/destination facts shared with that branch. Existing Consecration, Invocation, Rite and Short Rest dispatch also cannot be presumed pure merely by passing a general tactical-assessment flag.

Global host/policy conflicts must retain their real precedence: current authority, identity/payload, receipt matching, revision/known target, native pending/life/context/condition/work/resource gates as applicable. A generic all-commands precheck must not move an existing family gate ahead of another. If extraction reveals an existing gameplay defect or a query/execution inconsistency requiring a rule/compatibility change, retain the evidence and obtain a precise GPT/Codex disposition before changing that semantic branch.

## HC-03 — Parameters and actual choices

Every description binds API version, actual profile, actor, observed revision and source operation. Enumerated domains use the exact registered enums/identities admitted by host and native policy. Rational domains retain numerator/denominator and actual units, bounds, resource/booking exclusions and accessibility; no invented quantity quantum. Command IDs for examples are unused, deterministic and non-reserving; execution still accepts ordinary valid caller IDs under existing collision rules.

Separate operation support, current usability and discoverable finite examples. Do not hide a supported operation merely because no target is currently visible; its public description may explain the non-target-specific prerequisite without identifying hidden targets. Conversely, no guessed target, private stock, hidden creature or unknown source identity is included in examples/domains.

Actual pending-choice precedence stays with native state. Current session scheduling is Sanctuary, pending knockout, Opportunity reactor, Press, manufacturing quality, then ordinary turn; strain-recovery offers have their own existing command-conflict and suspended-clock rules and must be included without flattening those rules into that five-kind enum. Bind choices to pending identity, owner and revision. After a response, recompute the next choice from actual state. Do not cache an alternative as authority.

Required embedded elections include all admitted stance values and their unsupported cases, attack knockout and Press instructions, Opportunity take/decline and owned weapon, Press follow/decline into the actual provoker's vacated square (no arbitrary destination election), Sanctuary retarget/forgo, quality FullYield/Durability (and any native nonexceptional representation), tactical Guidance effect selection/decline, Healing Rite/Invocation cure preferences, strain point removal, admitted mining category sets/STR-or-WIS/hurried flag/version and conditional failure-victim/recovery preferences, spell/target/focus/willingness/Focused-DC elections and ordinary versus tactical context, Consecration center, item handling/placement and exact rational amounts. The matrix must disposition each actual semantic branch, including distinct cache and seven admitted Fishing Trap interactions and zero/positive-work cancellation.

Preserve specific limits: trap Abandon is not host-admitted; nonempty mining AssistantId requires schema77, absent from these factories; Guidance election is limited to eligible tactical Hide/Search/Stabilize; Sanctuary cannot retarget an Opportunity to a different creature; spell WillingTarget is not consent authority; Invocation accepts 1–3 recipients but at most one selected cure recipient; recovery targets the selected point ID, not the enclosing offer ID. Mining choice descriptions must not serialize hidden values, tier, DC or RNG from the raw attempt record.

## HC-04 — Known costs, conditional consequences and actual results

Before execution, report only facts currently available to the principal. Separate immediate action/reaction/interaction/resource costs, reserved quantities, labor/duration, and conditional future outcomes. A pending roll is described by its sourced rule, never by a predicted natural roll, success, damage, cure or yield. Resource amounts remain rational where native rules are rational; the old integer-only `CommandCost` representation must not force truncation or fictional rounding in the new DTOs.

After execution, match the exact principal/command fingerprint to its receipt under current authority. A receipt stores principal, command ID/fingerprint and revision; it is not a historical damage or inventory delta ledger. Project retained native records only when their causal receipt/revision/identity and the current principal's disclosure rights permit it. Distinguish receipt facts, persistent native outcome facts and present-state observations. Present state must never be relabelled as the state at the old command. Missing historical details receive an explicit unavailable/not-retained disposition rather than recomputation, replay or fabricated explanation. This is a proposed finite result contract for actual review, not an unreviewed waiver of required explanations.

No public explanation exports private source clauses, hidden target identifiers, global RNG or full snapshots. Source references identify only already-permitted public source/definition information, preserving TEST_ONLY/provisional/release distinctions. Reuse accepted manufacturing-quality calculation and authorized result data where appropriate; do not recalculate potions, healing, costs or save outcomes in host code.

## HC-05 — Authority, retry and console parity

The trusted embedding application still binds seats and host privileges. Current seat/actor/inventory authority is required before a prior receipt can disclose an outcome or be recognized as an exact retry. Narrow companion Haven sale/meal grants, milestone world-modification grants and focus/flask willing-handover grants must be selected with the same exact predicates as submission. Never broaden discovery's grant to buyer inventory or world modification. Stale revision, conflicting ID, revoked seat and not-owned decision remain distinct where safely disclosable.

At the baseline, `SeatCommandGrant` alone is not the complete submission grant selection: `Submit` applies the two exact Companion Haven transaction exceptions across all profiles and the pre-Bishop Cleric settlement milestone exception after its initial host admission. The helper currently contains the work-control Haven exception and the Bishop milestone exception. The new API must account for all these exact predicates while preserving enabled-seat checks. A shared extraction must preserve the predecessor submission's ordering, rather than silently moving those grants or widening them. Host malformed/conflicting/stale/unknown-target handling and core current-inventory-authority preflight are distinct layers; the new DTO must identify the boundary it describes.

Core `AcceptedResult` additionally retains distinctions such as `AcceptedSuspended`, `CommittedAtTacticalDecision` and reached clock, while legacy host results collapse some of them. New explanations may expose permitted authoritative distinctions through an additive projection; they must not alter legacy results or fabricate absent damage/quantity deltas.

An exact persisted retry must survive disappearance or changed visibility of a target when current native authority still permits duplicate recognition. It must not rerun current gameplay eligibility or pay again. Current inventory revocation can still reject it. Fresh commands retain current visibility, range, target and resource validation. Native result explanations are separately filtered by current disclosure authority.

Add explicit console operations for the versioned description/assessment/discovery/choice/result surfaces, preserving legacy operations. Round-trip every meaningful payload, including Consecration's embedded request, rational values, Guidance, cure preference, pending IDs, targets, stance/Press/knockout elections and manufacturing choice. Typed and console paths must use the same C# API and stable ordering. Caller-supplied JSON must not create authority. No shell-only rules or client-invented default choice is permitted.

## Required design closure

Before runtime work: finish and pin the exact operation/profile/payload/source matrix, distinguish native supported branches from host restrictions and missing assessments, reconcile all resolver-on-copy paths within scope, and agree a finite semantic-witness plan. Independent source audit and actual GPT review must resolve HC-01–05 and every concrete blocker. A census or a list of intended tests does not close this gate.
