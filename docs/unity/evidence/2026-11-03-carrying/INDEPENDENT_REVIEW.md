# Quantity and carrying review

The existing separate `/root/source_review` agent reviewed the new exact-quantity primitive, carrying calculations, container aggregation and32 tests against BODY_EQUIPMENT_PLAYTEST.md. Review was read-only. It performed one focused in-memory probe using the326-case compiled assemblies; no files changed and no full test suite or Unity execution was performed independently.

Confirmed and corrected findings:

- Cross-unit conversion of an inclusive gross container amount could suppress a child's printed Load or documented weight. Each unit now retains independent coverage. Fallback conversions apply only to atomic source amounts; unresolved gross decomposition remains unknown. Both directions have regressions.
- Computing a half-capacity value was unnecessary and could overflow its rational denominator. Burden checks now compare exact BigInteger products; capacity1/long.MaxValue remains testable without constructing its half.
- The new conservative known-content lower-bound check skipped overlapping child aggregates before testing their individual bounds. A probe returned200 documented pounds while fully covering a300-pound child aggregate. Each wholly covered child is now checked against its parent's amount before overlap skipping. The contradictory cases reject, and the consistent30/12/11/1 root/box/child/leaf example remains accepted. A blanket rejection of every crossing extent was considered and removed because an exact whole-root total can resolve that query without decomposition.

The reviewer checked all three changed implementation/test files against `engine/artifacts/run-20261103T210707475Z-bf3393ad/results.json`, which passed328/328 cases, and reported no additional findings in the final changes.

Limits: container lower-bound checks are conservative, not a general equation solver. Cross-unit fallback is atomic only; partially overlapping aggregates that require unknown empty-item decomposition reject. The helper accepts at most256 objects and256 inclusion references per item as technical bounds. No ownership, custody, consent, anatomy, hand availability, item access, action/time permission, catalog, transformation lifecycle, persisted inventory or actual movement execution is granted by numeric success. Estimated hauling mass is explicitly not documented mass. These remain provisional source-bound calculations, not release approval.
