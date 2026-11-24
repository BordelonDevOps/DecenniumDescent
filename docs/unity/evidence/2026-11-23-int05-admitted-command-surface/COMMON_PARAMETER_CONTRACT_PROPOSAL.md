# Common native command parameter contract

**PROPOSED shared descriptor binding.** The per-operation parameter contracts must supply the exact selected domains and native guard order. This document adds no command field, default mechanic or permission.

| Native path | Exact type | Shared descriptor meaning |
| --- | --- | --- |
| Command.Id | System.String | Required exact native ID. Validation.ValidId permits1 through96 ASCII letters/digits/underscore/hyphen/period. Discovery uses the separately proposed deterministic unused-example algorithm, with every derived-ID constraint still checked. A suggested ID is not reserved. |
| Command.Actor | System.String | Required native actor identity, constrained to the actual trusted route and currently authorized command domain. Player control, operator Hero binding and trusted defender identity remain separate. |
| Command.ExpectedRevision | System.Int64 | Original command revision. Preserve it exactly for submission, duplicate matching and later explanation. A read's expectedObservationRevision is separate and cannot rewrite this value. |
| Command.Kind | Existing CommandKind enum | Existing numeric identity. The selected catalog exposes the registered operation/variant and its actual support disposition. Static census membership is not permission. |
| Command.Target | System.String, constructor default empty | Meaning is operation-specific: actual entity, selected service, native work/offer/turn token or required empty sentinel. Never manufacture an identity from an absent target. |
| Command.X / Command.Y | System.Int32, constructor default0 | Meaning is operation-specific. These are not universally positions, direction vectors, distances or seconds. Preserve exact native ratio/grid/literal interpretation and any zero/one defaults. |

The existing optional payload members are Inventory, Combat, Advancement, Ranged, SuppressionFire, DefensiveFormation, ExpeditionAssignment, HarvestSelection, MiningSelection, ProspectingExposure, RouteMappingWork, IntimidatingPresence, HealingRite, SpellCast, Guidance, SanctuaryResponse and DivineInvocation. Each is its actual native request type and defaults to null in Command's constructor. OverwatchRider is its actual enum and defaults to None. The Consecrate request is retained privately and exposed through Command.GetConsecrateRequest(); a descriptor must bind that actual getter and the existing console input explicitly, not invent a public Command.Consecrate property.

Constructor defaults do not prove that an omitted, extra or unrelated payload is rejected by every native operation. Per-operation rows must name the actual host shape checks and native validators, including any accepted-but-unused legacy field behavior. Do not impose a new universal all-other-payloads-null check, silently discard supplied fields, or change fingerprints to simplify the new surface. New assessment follows actual submission precedence; old query ordering remains unchanged.

Native Command.Fingerprint excludes Id, but includes Kind, Actor, Target, ExpectedRevision, X/Y and the selected versioned payload encodings. Exact retry still requires actual principal+ID and internal fingerprint matching. Fingerprints and raw receipt payloads are not public DTO values or authentication credentials. Caller JSON cannot create Authority, inventory ownership, consent, seat enablement or operator/defender privilege.

The descriptor's required/optional/native-conditional classification is separate from its native type. A nullable request can be required for one operation variant and absent for another. Empty IDs, zero dice sentinels and zero rational defaults are not all interchangeable. Preserve native constructor and host validation behavior; the actual operation registry names every applicable condition.

Domains use FiniteComplete only for a genuinely exhaustive currently visible selected set. Rational bounds plus additional native constraints are Constrained; illustrative examples do not enumerate a continuum or establish a smallest positive quantum. Embedded elections stay parameter descriptors without fake offer IDs. Actual pending decisions retain their native offer identity, owner, alternatives and priority.

Current source-derived costs/reservations/durations are separate from conditional continuation obligations and observed results. Admission that passes now may still require later native capability, access or freshness checks; existing initial timing fences must remain initial guards. Predictable capacity failure is an assessed constraint, not proof that an execution reached its native stage.

Read methods' expectedObservationRevision is a signed64 argument checked against the coherent current observation. On exact duplicate commands, use the original receipt disposition without rerunning original gameplay eligibility. Current endpoint authority, current per-field disclosure and observation freshness remain required. Unknown/hidden targets cannot be confirmed merely because the request supplied their text.

Source basis: Runtime/Core/Simulation.cs Command and Validation.ValidId, existing ConnectedExpeditionSession submit/query/exposed-payload/target/grant paths, SOURCE_API_CONTRACT.md and actual GPT03/04. Exact per-operation payload paths, visible domain choices, derived-ID constraints and five-path serialization witnesses remain the family contracts' responsibility. No runtime or tests were performed for this document.
