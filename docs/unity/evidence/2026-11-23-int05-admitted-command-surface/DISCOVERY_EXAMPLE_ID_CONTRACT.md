# Deterministic discovery example identities

**PROPOSED technical contract; no implementation or full HC acceptance.**

An example is a concrete current Command, not a pending choice, reservation, proof, permission token or new game operation. A real decision keeps its actual native pending ID. This algorithm changes neither native command identity nor fingerprint semantics.

For an authorized endpoint and one coherent current observation:
1. Freeze the endpoint's actual internally bound principal and command-specific grant; callers cannot supply a principal or Authority in JSON.
2. Enumerate the public operation catalog by existing numeric CommandKind, then the fixed registered variant ordinal. Enumerate each variant's illustrative examples by its fixed descriptor order; use the operation-specific visible parameter/domain order. The exact variant/example allocation remains part of the parameter registry.
3. For each example, form the ASCII candidate `hc1.r{revision}.k{kind}.v{variant}.e{example}.n{nonce}`. Use exact lowercase base36 (digits0-9 thena-z), without signs or padding; zero is0. Convert integer values directly, never through floating point. Revision is a nonnegative Int64; kind, variant and example are nonnegative Int32; nonce is a nonnegative Int64 initially0.
4. Reject an ID already present in the current receipt set for this exact principal, or already emitted by this endpoint invocation. Increment nonce and use the first unused ID. No other principal's receipt identity/count affects the result.
5. At most the number of same-principal existing IDs plus already-emitted IDs plus1 candidates is required. Use checked arithmetic and the existing bounded collection sizes. This is a read of identifiers, not receipt replay or fingerprint validation. It creates no receipt and reserves nothing.
6. Construct the exact native Command with that ID and current revision, then pass it through the same new pure assessment. Retain supported but currently denied examples only as the applicable descriptor permits, with the safe actual assessment. Never replace a hidden/unavailable target with a guessed positive example.

The maximum textual shape under these declared numeric widths is57 ASCII characters, within existing Validation.ValidId's96-character limit; only permitted letters, digits and periods are used. The57-character bound is only the Command.Id envelope. Each variant must additionally prove every native derived identity and payload constructor bound. For example DivineInvocation may validate command.Id + ".invocation.sync"; the old81-character decimal envelope could exceed96. The revised base36 shape leaves room for that16-character suffix, but is not a blanket proof for all other native derived IDs. Include those exact suffix/prefix constraints in the parameter allocation; no silently omitted valid domain or falsely admitted example.

No hashing, truncation, random UUID, time, object identity or dictionary iteration enters the algorithm. Candidate IDs from another session may match: native idempotency is scoped by actual principal plus ID within its own simulation. The algorithm does not promise global uniqueness.

Exact source boundaries: Simulation.cs:67-71 retains Principal/Id/Fingerprint/Revision; :1032-1037 defines the ID alphabet/limit; :1562 finds prior receipts by principal+ID. Existing receipt capacity differs by schema and execution stage; this algorithm must not change it. A suggested ID can conflict if the state changes after observation; normal stale/conflict behavior remains authoritative.

Prospective checks: repeatability at one revision, native numeric enum ordering, adversarial same-principal collision prefix and high suffix, unrelated-principal receipt independence, multiple emitted example uniqueness, maximum numeric lengths, deterministic strict-restored output, no receipts/state/RNG/checkpoint mutation, and old endpoint equality. Only pure string-length/alphabet arithmetic is checked during this design phase, not engine execution.
