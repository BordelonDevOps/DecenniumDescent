# Agreed list, request-scalar and example-order contracts

Actual GPT response `91c9d89f-6e42-5937-a56a-9744e3ec0d4d`, retained in GPT_ARCHITECTURE_REVIEW_06.json, and Codex concur. These precise decisions override earlier proposed list/order/CommandScalar wording. They do not accept the complete HC contract or authorize runtime implementation.

## Fixed fact cardinality

Each registry key declares `Cardinality=Scalar|List` permanently, independently of availability or execution mode. An available Scalar has exactly one `Value` and no `Values`. An available List has immutable ordered `Values` of the one declared closed scalar kind, with its declared width, code family and unit/dimension rules, and no `Value`. No nested lists, null elements or arbitrary objects are allowed. IdentityList and CodeList therefore use cardinality List and scalar kinds Identity and Code; the scalar kind union does not grow.

A legitimate empty list is `Values=[]`. For an authorized-subset projection it means no values in that authorized projection, not necessarily an empty native collection. Declare that scope statically per key. No dynamic hidden-entry/filtered/count flag is added. Unavailable facts omit both Value and Values and protected causes. Fixed protected placeholders remain independent of hidden existence. Native relative order and post-filter public ordinals are preserved. Repeated subject-specific scalar rows keep their separately typed instance context; they are not automatically list-valued facts.

## Exact CommandScalar scope

Quantity uses exactly one native unit or technical dimension. `CommandScalar` is agreed only for these exact request uses, each bound to its native ParameterPath, operation/variant/source check and fixed value:

| Native request use | Exact required value |
| --- | --- |
| Whole portable-item handling | 1/1 |
| Whole vessel handling | 1/1 |
| Fishing-trap retrieval request | 0/1 |

Zero is a present required scalar, not absence, zero mass or permission to omit the request. This is not blanket approval for other Amount fields or projected item counts. Native resource quantities retain their real UnitId, including whole resources with a native count/drop unit; copper valuation retains CopperValue. No legacy request encoding changes.

## Exact example ordering and Core access

Within each frozen native kind/variant, construct the finite currently authorized payload candidates through existing native constructors. Compare their existing canonical `Command.Fingerprint` text with `StringComparer.Ordinal`. This is lexical technical ordering, not numeric quantity order, preference or gameplay priority. A separate general tuple sorter is not required; earlier tuple orders describe source candidate enumeration only.

Command.Id is excluded from the fingerprint; ExpectedRevision is the same coherent current revision. A fixed internal non-executable temporary ID can construct candidates for ordering. After ordering, assign example ordinals and actual hc1 IDs, then check the actual derived-ID/payload constraints and pure admission. Never execute the temporary candidate. Preserve existing native constructor ordering inside payload lists; do not reorder pending decisions or result instances by command fingerprint.

Coalesce genuinely identical canonical payload candidates and retain all recipe/axis associations in the contract. Distinct effective payloads with an equal key are a concrete discrepancy that must be resolved before qualification. Dictionary order, unstable sorting and generated IDs are not tie breakers.

Fingerprint remains internal to Core. The proposed additive Core-owned comparison mechanism accepts already-constructed Command values and returns only comparison order; it must not export fingerprint text, add a friend assembly or duplicate serialization in LabModel. It reads no simulation/principal state and supplies no grant. Hidden candidates and other principals' receipts cannot influence candidate rank or ID allocation. Full getter-purity and per-variant derived-ID checks remain required.
