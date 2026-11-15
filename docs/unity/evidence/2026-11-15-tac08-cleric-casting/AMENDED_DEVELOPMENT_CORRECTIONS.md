# TAC08 amended development corrections

The earlier `implementation/` and `review-correction/` packets remain historical. Actual GPT response `67a07398-59b8-5af5-8410-ee42b2ce2ca2` approved the bounded paid Club pickup; it did not grant module acceptance.

Four preliminary build attempts under `engine/artifacts/tac08-cleric-casting/amended-club-build/` are failed development evidence:

- `run-20261115T203320840Z-5def1bd6`: compiled, then the genuine pickup rejected. A post-payment structural check ran before the transaction advanced the revision, so its new handling row was considered future history. Full structural validation remains at the transaction boundary; the completion check now verifies actual capacity there without prematurely validating the next revision.
- `run-20261115T203510791Z-cb4849b6`: compiled, then the genuine session pickup rejected. The rule resolver admitted it, but the connected-session target filter still required a PortableEquipmentRecord. The exact amended companion Club is now recognized by that filter, retaining actor and inventory visibility checks.
- `run-20261115T203732765Z-c74bab4e`: compiled, then a detached negative control attempted to construct an unsupported generic held portable item. The control now uses two detached held Club records to exercise occupied hands; it does not claim genuine item acquisition.
- `run-20261115T203902279Z-60ffc1fd`: compilation failed because the test assembly attempted to call internal `ActorLifeRules.Record`. The incapacity control now uses its existing detached Stunned condition helper. Zero executed cases is not a pass.

The separate amended build `run-20261115T204040935Z-8553181f` compiled all C# inputs and passed the complete genuine cadence case, including the paid pickup, negative controls, nonzero Refrain across the actual idle and weapon intervals, the next same-spell cast, and restore/replay. Standalone C# compilation and static checks also passed. The fresh focused/full runs, independent connected paths, compatibility and final actual GPT review remain separate qualification gates.

The preliminary reports retain exact compiled-source hashes. These intermediate uncommitted source states are not advertised as reconstructible source freezes or qualifying binaries. The corrected source commit and its frozen binary identities must be used for final evidence.
