# Exact V1 value and console encoding proposal

**Bounded technical representation concurred by actual GPT05 and Codex; full HC acceptance remains open.** This normalizes the native widths named by the family field registries. No implementation or new game rule is claimed.

The C# fact/parameter value is a closed immutable discriminated value. Its public kind is Boolean, Integer, Quantity, Time, Identity, Code or GridCell. A registry declares the exact native width and optionality; values cannot silently change type between fresh, duplicate, restored and later explanation.

| Kind | C# meaning | Proposed new V1 response JSON |
| --- | --- | --- |
| Boolean | System.Boolean | `{"kind":"Boolean","value":true}` |
| Integer | Native Int32 or Int64, preserved by a declared width; no floating conversion | `{"kind":"Integer","width":64,"decimal":"-3"}` |
| Quantity | Native normalized RuleQuantity: nonnegative Int64 numerator, positive Int64 denominator; native unit/quantity dimension from the field registry | `{"kind":"Quantity","numerator":"3","denominator":"2","unit":"<registered-unit>"}` |
| Time | Native normalized RuleTime, exact rational seconds, absolute or duration semantics fixed by the key | `{"kind":"Time","numerator":"13","denominator":"2","unit":"second"}` |
| Identity | Exact currently permitted native identity text, never an authority token | `{"kind":"Identity","value":"<authorized-id>"}` |
| Code | Exact allowlisted source enum/diagnostic code, with its registered code family | `{"kind":"Code","family":"<registered-family>","value":"<registered-code>"}` |
| GridCell | Native signed Int32 X/Y | `{"kind":"GridCell","x":1,"y":-1}` |

Integer decimal strings use invariant canonical decimal: zero is0, no plus sign, whitespace, exponent, thousands separator, leading zeros or negative zero. Bounds remain exact Int32/Int64 as declared. Quantity/time components use the same canonical nonnegative decimal spelling with denominator greater than0. The native normalized representation is preserved; a host does not silently round or change an authoritative command amount. Using strings for exact integer components prevents a JSON consumer from losing Int64 precision through binary64.

Null is not zero, empty identity, missing optional die or a successful no-op. Fact availability determines whether a value exists. If Withheld, NotApplicable, NotRetained or ProjectionUnavailable, omit the value and protected cause data according to the fixed safe field schema. Native sentinel fields require the registry's applicability rule before value construction. Domain descriptors can expressly permit an empty request string/default payload, but must describe it as that parameter's native empty sentinel; it is not an existing entity identity.

A Quantity has exactly one registered representation: native `unit` or technical `dimension`. A unit is the exact native identity when one exists; display labels do not replace prototype.potable-water.pint or TEST_ONLY.ration-pound. Actual GPT05 approves `CopperValue` as the technical dimension for monetary RuleQuantity valuations without a physical currency-lot unit. For example `{"kind":"Quantity","numerator":"15","denominator":"2","dimension":"CopperValue"}` expresses valuation, not a physical coin count, conversion or reservation. Preserve native integer fields as Integer; no invented unit or lot.

Actual GPT05 approves typed repeated-instance context with native relative order and public ordinals assigned after authorization filtering. Never export raw native indices whose gaps reveal hidden rows. Each subject identity has its independent predicate. Fixed keys distinguish repeated authorized values through context; protected family placeholders have schema-defined presence independent of hidden records. Exact per-field normalization remains part of the full review.

Console encoding of new V1 responses uses these exact public projections. Legacy response and command input encodings remain unchanged. New submission wrappers consume the existing native Command through the existing exact constructor/parser, preserving all payloads and embedded Consecrate request; no separate JSON rules implementation or caller-supplied Authority is allowed. Full payload round-trip checks must use an integer-preserving parser, retain original ExpectedRevision independently of observation revision, and compare exact Commands/fingerprints internally without exporting fingerprints.

Required prospective representation checks: native signed bounds; exact fractional food/water/labor/time; absent versus zero; unknown enum and out-of-range values rejected at the applicable boundary; ordered current/read/duplicate/restore output; and meaningful payload round trips. These are design obligations, not executed tests. Per-operation public keys, unit dimensions, parameter paths and instance contexts still require final agreement.
