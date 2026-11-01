# W12 TEST_ONLY witness 450

Owner adoption of exact proposal 445 is recorded at `OWNER_PG328_W12_ADOPTION_445_TESTONLY.json`. This witness copies the adopted hypothetical W12 inputs without adding branch premises and binds them to unchanged W01-403 S030. The source bindings are verified against the exact pinned Git commit `f1a58b32640d327bb2abbc0372bc80577d212fce`.

- Proposal SHA-256: `93d31941e6a6d4d059cb3a108d0e247d07cc8e6cce395712f1c0ad45523df14c`
- Adoption record SHA-256: `83d25ca677ea8d910575a3bcc87be6a29837553112d3445e1c50cc954a8f4c60`
- Parent W01 replay SHA-256: `2b60ae35d828bd6028d71f202c1dd61c823d6212bb45c7f633ecd8f6b51d44fb`
- S030 snapshot SHA-256: `6270321d6f07a55173f01fb353142d6bfb537d8e044cd313ef8fdd956baeff6c`
- Source bindings: 18/18 exact Git blobs verified
- Timeline: 45 regular START markers, 44 END markers, 12 ordered authored events, endpoint 79.31
- Witness SHA-256: `0cbcd37186973879e01db62096fd2c09cd31a663bf81f3d38503ef16dafc0cae`
- Scope: hypothetical PG328-W12-R1 only. No campaign event, seal, Fortress acceptance/application, canon change, or queue mutation.

See `BUILD_VALIDATION_450.json` for the checks. This event witness does not claim an invertible state-patch chain.

Run `VERIFY_W12_WITNESS_450.py` to recompute the adoption, source-binding, timeline, scope, and artifact-hash checks.
