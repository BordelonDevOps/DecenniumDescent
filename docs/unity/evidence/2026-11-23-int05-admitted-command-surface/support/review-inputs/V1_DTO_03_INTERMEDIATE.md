# Version 1 projection types proposed for review

**Structural direction concurred in actual GPT response `f4e4a9c0-81a2-5ac1-9578-c8d8ef626d07`; full contract and implementation remain open.** These are immutable C# projection contracts, not save records, new mechanics or a new production profile. They supplement HC-01-05 and DETAILED_RESULT_CONTRACT.md. Every operation still needs its exact field-key/native-source/disclosure/witness mapping; this structural concurrence does not close that work.

## Shared response envelope

Every public response contains `ApiVersion` (exactly1), `ObservedRevision`, the existing selected profile identifier and TEST_ONLY classification, and a safe response status/code. A read's `ExpectedObservationRevision` is independent of the original command's `ExpectedRevision`. Response collections are non-null immutable copies; optional scalar absence is explicit. Legacy response null/empty behavior is untouched.

Do not include an Authority, origin/checkpoint, full Snapshot, canonical bytes, raw fingerprint, raw request history or policy object. A source reference is an already permitted public source/definition identity with its status (original rule, adopted provisional decision or explicit fixture fact); it is not an entitlement or permission to expose private source content.

| Type | Required content |
| --- | --- |
| `ExpeditionCommandCatalogV1` | Envelope; requested actor; ordered operation descriptions; current unsupported dispositions. Separate ordinary descriptions from currently materialized examples. |
| `ExpeditionCommandDescriptionV1` | Existing CommandKind; stable source-qualified variant key (for example cache versus trap Interact); dispatch route; support disposition; parameter descriptors; known costs/reservations/durations; conditional continuation facts; public source references. |
| `ExpeditionAssessmentV1` | Envelope; exact attempted kind/actor under safe projection; supported; disposition (`Available`, `AlreadyCommitted`, `Unavailable`, `NotAuthorized`, `StaleObservation`, `VerificationUnavailable`, `ProjectionUnavailable`); safe actual stage/code; optional matching receipt revision; ordered known facts and conditional obligations. Admissibility is not a forecast of rolls, deadlines or post-time success. |
| `ExpeditionDiscoveryV1` | Envelope; operation descriptions; finite illustrative exact Commands paired with their assessments; domain-completeness metadata. No implication that examples exhaust rational quantities or are reserved permission tokens. |
| `ExpeditionChoiceCatalogV1` | Envelope; actual authorized pending decisions in native priority order; embedded elections for the requested operation/context separately. Empty current choices does not erase a supported operation's parameter domain. |
| `ExpeditionChoiceV1` | Stable actual offer/decision identity; existing kind; controlled owner; observation revision; native priority/context; alternatives or constrained domain; known costs and conditional effects. A choice token must come from the real pending state, not an example command. |
| `ExpeditionSubmissionV1` | Exact immutable legacy result; actual attempt disposition; before/after observed revisions; safe actual stage/code; whether core execution was reached; optional native result revision and matching receipt revision; native clock-suspension field; separately authorized pending continuation; detail availability; ordered actual facts. |
| `ExpeditionAutomaticSubmissionV1` | Native terminal dispatch status plus bounded ordered actual primary/fallback assessment records (0-2), identity of the candidate whose admission determined that status, and the actually executed command/result if any (0-1). Candidate details obey current disclosure. No second Plan/Assess/Execute. |
| `ExpeditionResultExplanationV1` | Envelope; exact matching principal-bound receipt metadata; retained facts with original/resolving causes; current facts explicitly labeled; fixed applicable detail limitations. No historical re-execution or failed-attempt backfill. |

## Parameter domains

`ExpeditionParameterDomainV1` has `ParameterPath` (an existing Command/payload field), `ValueKind`, `Requirement` (required, optional or native-conditional), `DomainKind`, ordered visible alternatives/examples, optional exact rational lower/upper bounds with inclusivity, optional registered unit, and ordered source-qualified constraint codes. No arbitrary expression interpreter or client-side rules engine is proposed.

Domain kinds are `FiniteComplete`, `Constrained`, and `IllustrativeOnly`. `FiniteComplete` is permitted only for the full currently authorized domain actually enumerated (for example two eligible selected mutation IDs or actual pending point IDs). An interval plus native constraints is `Constrained`, never a claim that every number inside it is presently admissible. Unknown/hidden targets are not manufactured examples. No positive quantum is inferred for rational inventory, water, labor or clock values.

Typed values use a closed discriminated representation: Boolean, signed Integer, exact nonnegative Quantity (numerator/denominator plus native unit), exact Time, public Identity, enum/diagnostic Code, or integer GridCell. Lists contain one declared type; no `object`, arbitrary JSON fragment or raw native record is a field value. Quantities/times use the original normalized rational values with no floating conversion or truncation. Signed HP differences use Integer and retain their AttemptInterval scope. A domain's offered public identity never carries control or inventory authority.

Conditional requirements preserve the actual native relationships: take-OA selects the admitted owned attack source; decline has the exact empty/default payload; Press follows the fixed vacated cell; spell Focus/WillingTarget/Focused-DC predicates stay spell-specific; Guidance is an eligible tactical election only; cure preferences retain actual recipient/source rules; mining preferences retain hidden-information limits. Descriptions must not reveal a value-ranking or damaged-unit shortlist just because native admission can inspect it.

Embedded elections are parameter-domain descriptors and carry no fabricated offer/decision ID. They are not `ExpeditionChoiceV1` unless an actual pending choice exists. Embedded election alternatives are not necessarily pending decisions. `OrdinaryOutcome/KnockOutIfEligible/AskIfEligible` in an attack and the two alternatives of a later real knockout offer have different identities and meanings. Mutation choice at rest start is likewise not a later instant equip command.

## Facts, availability and privacy

`ExpeditionFactV1` has a stable allowlisted `Key`, typed value only when available, `Availability`, `TemporalMeaning`, safe causal references and public source reference if applicable. Availability uses `Immediate`, `Retained`, `NotRetained`, `NotApplicable`, `Withheld`, `ProjectionUnavailable`, and the now structurally agreed `ObservedCurrent`. Temporal meanings are `OriginalCommit`, `ResolvingCommit`, `AttemptInterval`, `CurrentObservation` and `CurrentContinuation`. Future consequences are excluded from this fact collection.

| Availability | Allowed temporal meaning | Value/cause rule |
| --- | --- | --- |
| Immediate | AttemptInterval; OriginalCommit or ResolvingCommit only when an actual retained causal event is captured in that submission | Actual submission observation; never a forecast or rolled-back candidate effect. |
| Retained | OriginalCommit, ResolvingCommit, CurrentObservation, CurrentContinuation | Exact native causal record; a retained mutable status is current, not an invented earlier status. |
| ObservedCurrent | CurrentObservation, CurrentContinuation | One coherent authorized current read; no historical retention claim. |
| NotRetained | OriginalCommit, ResolvingCommit, AttemptInterval | No value or fabricated cause. Used only after disclosure permits the requested historical field. |
| NotApplicable | The field's otherwise registered temporal meaning | No value; applicability itself must be disclosable. |
| Withheld | The fixed public field's registered temporal meaning | No value, hidden count, private identity or causal reference; no private existence claim. |
| ProjectionUnavailable | The field's otherwise registered temporal meaning | No value; preserve the independently captured truthful transaction outcome. |

`ExpeditionConditionalObligationV1` is a separate immutable descriptor used by descriptions, choices and assessments. Its registered key, native stage, source-bound condition code, conditional consequence code and authorized parameter references describe a requirement; they do not assert an event, receipt, cost payment or elapsed time. It has no observed-fact Availability or TemporalMeaning. Protected applicability and parameters use the same non-disclosure rules. Existing initial timing/freshness fences remain current admission checks, not generic future obligations.

Assessment distinguishes `InitialEligibility`, `CommitFeasibility` and `NativeEnforcementStage`. A pure, definite capacity impossibility may produce Unavailable with a V1 constraint diagnostic even when initial eligibility passes. This is not an actual execution failure code. Predict a native code only if all preceding native failure paths are established; otherwise omit that prediction. A capacity constraint that depends on later native settlement remains a conditional obligation. Pure counts, overlaps and quantities account for actual additions/releases and applicable family/snapshot limits without Reserve, clone mutation, validation or execution. Authoritative enforcement stays at its original stage, with exact legacy code/order and rollback semantics; see GPT_ARCHITECTURE_REVIEW_03.json.

Causal references contain only authorized operation/record identity and revision. Initiating receipt and later resolving receipt stay separate. A present record's overwritten status/progress is current; the receipt itself does not supply historical quantities, HP, modifiers, private targets or outcomes. A true causal chain is required; matching only actor, time or nearby revision is insufficient.

The field registry must assign each key its exact native source and access predicate. Evaluate disclosure before revealing record existence, applicability, cardinality, cause or value. For a protected family, use a fixed safe field shape and `Withheld` where needed; do not disclose a variable number of hidden effects, reactors, sources or targets through the result structure. Caller-provided target text is not confirmation that an authoritative target exists. Original source IDs, random seeds/words, private DC/AC, unknown values and hidden source associations stay protected unless an existing explicit public source rule/view authorizes that particular fact.

Current actor control does not imply operator observation, inventory access or current target visibility. For example, own rest settlement fields can use the actual player long-rest view predicate; mining outcomes and trap retrieval contents retain local observation predicates; visible torn seal status cannot expose the Wraith association or suppression timer. A shared `Controls(actor)` check is not sufficient for all fields.

## Stable order and limits

Operation catalogs order by existing numeric CommandKind, then a fixed ordinal variant key. Parameter/fact keys follow a published per-operation registry order; identity alternatives use ordinal identity order except where the native source specifies priority (captured OA reactors, pending choices, ordered healing stages, causally ordered events). Discovery examples use stable unused IDs for the observed revision, without writing receipts or reserving them. The final example-ID algorithm must be collision-safe under the existing ID-length/fingerprint limits.

Public results are bounded by the existing native history capacities and the chosen source-qualified field/domain contracts. Do not solve a large domain by silently omitting admissible values: retain a constrained domain and label finite examples. No unreviewed hard truncation can turn a partial domain into `FiniteComplete`. Console serialization must retain these enum, rational, optional-value and ordering distinctions and invoke the same C# methods.

## Remaining review decisions

1. Review the exact type/field and public failure vocabulary above against host compatibility and privacy. No existing native error code is renamed or reordered by this proposal.
2. Complete the allowlisted per-operation fact keys/native causal sources/access predicates, parameter paths, finite-example IDs and five-path evidence allocation across all78 kinds plus the2 operator kinds and host capabilities.
3. Resolve deterministic immediate capacity versus post-time/conditional failure mapping without copied execution or changed legacy behavior.
4. Independently verify, then obtain actual GPT/Codex HC-01-05 concurrence before adding these types or any runtime implementation.
