# TAC-10 original frozen regression completion

The original run `9d490d26ac3c4e57931b50ab9a6dd34b` completed **1,583/1,583 cases, zero failures** on engine tree `db91c9ce8711be802674762d458bca9782207833`. All six original workers exited. This qualifies that frozen tree only. The subsequently reviewed public Dash correction changes the host/runtime and requires renewed qualification; TAC-10 remains unaccepted.

The [collector](support/Retain-FerryRegression.py), committed at `b4c2e5d6d`, reconciled:

- The exact 1,576 accepted predecessor names/order and original six shard memberships against the authenticated TAC-03 final archive, plus the seven explicitly named new Ferry cases. An older `tac10_` case remains part of the predecessor set.
- All six ordered result journals, zero errors, complete assignments, terminal `DONE` records, original run IDs/PIDs/start metadata, inventory hashes, journal hashes and matching loaded assembly hashes/module IDs. A fresh CIM observation found none of the original workers present.
- All 468 compilation inputs against the frozen Git tree, the exact executed launcher/runner against their committed bytes, and all four frozen DLLs against the retained seal archive. The original build report's single focused pass is separate from these 1,583 journal results.
- Every generated artifact from all seven new cases: 119 files. Predecessor case artifact trees remain local; the complete result journals and authenticated assignments are retained here without duplicating those older trees.

| Shard | Cases | Original PID | Result |
| --- | ---: | ---: | --- |
| A | 281 | 10888 | PASS |
| B | 267 | 8700 | PASS |
| C | 263 | 4860 | PASS |
| D | 259 | 14676 | PASS |
| E | 257 | 18820 | PASS |
| F | 256 | 9448 | PASS |

[RETENTION.json](regression-checkpoint/RETENTION.json) and [MEMBERS.json](regression-checkpoint/MEMBERS.json) bind the 179-member [archive](regression-checkpoint/full-regression.zip): 973,324 bytes, SHA256 `55797f08290acb27bca1dee3e927ba7d86a7af8a31dfa311198cef8ac83a82ec`. The archive includes actual process observation, all run metadata/journals, the seven new case trees, collector and immutable build references.

The collector explicitly records that seven current engine files differ from the tested tree while the Dash correction is being developed. No result is transferred to that correction. Five paths, authentic95–113 compatibility, remaining source/ability/consumer gates and actual final GPT/Codex agreement remain required. No successor; Unity integration, storage cleanup and GitHub Support remain held.
