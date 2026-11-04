# Independent engineering review

Reviewer: `/root/source_review`. Scope: schema14 sparse calendar and connected-combat changes on the Engine candidate.

The reviewer inspected sparse observation identity, replay and persistence, exact movement/Action/Reaction continuity, tactical continuations, worker separation and the transition dispatcher. No actionable defect was found in the final candidate.

Against `engine/artifacts/run-20261104T033411085Z-9aa998b0`, the reviewer independently executed43 nondisk cases:9 connected-combat,20 shared-world,6 command-history and8 encounter-history cases. All passed. All104 compiled-source hashes matched at that point.

An additional independent command probe exercised an actual off-turn Press: hit, enemy turn, two departure steps, declined OA, accepted Press. The hero moved to(4,1), ordinary movement stayed15feet and its previously spent Action remained spent. Restore rejected a forged reset of that shared ledger.

The parent then added one exact-boundary regression without changing implementation: Blinded expires at6seconds, save/restore at6, tactical entry at6, with unchanged processed journal, life events and interval budgets. The reviewer independently ran that case against final `run-20261104T033931641Z-3641aaaf`; it passed, and all104 final compiled-source hashes matched. The other43 focused cases were run against the preceding DLL with identical implementation files.

The final parent receipt is837/837. The reviewer read that receipt but did not independently rerun the full suite, disk tests, legacy byte comparison or Unity. Parent full-suite/disk and69-file byte-parity receipts supply those separate checks. Mobile stance, off-grid entry, changed rosters and general content remain outside the admitted host. This is bounded engineering review, not whole-engine completion or release qualification.
