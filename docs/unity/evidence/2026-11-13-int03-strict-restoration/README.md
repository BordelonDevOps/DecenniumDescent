# INT-03/P1 strict restoration

Source `75872e1e01fea9b17fce0c5c6c34d56679848961` on `Engine` follows the [engineering contract](ENGINEERING_CONTRACT.md) and [actual GPT authorization](GPT_ENGINEERING_REVIEW.md). The selected Default and Fishing Trap profiles collect the first qualifying passage while their full uncached validation replay reconstructs the incoming history. The passage remains local to the validation attempt. Core creates the actual origin after validation succeeds, then the factory matches that origin's exact bytes before sealing its checkpoint.

The diagnostic count separates the outer validating pass, the existing nested charter reference search and the prior dedicated sealing replay. The outer pass and nested reference remain. The selected construction no longer runs the dedicated sealing pass. Standalone full replay and the prior sealing path remain executable references. No field, fingerprint or wire encoding changes. [Reference counts](counts/Reference/results.json) · [Candidate counts](counts/Candidate/results.json)

## Public r104 restore timings

| Profile | Baseline p95 | First candidate p95 | Repeat p95 | Repeat max |
| --- | ---: | ---: | ---: | ---: |
| Default | 4427.22 ms | 4330.26 ms | 3851.09 ms | 3939.60 ms |
| Fishing Trap | 4202.97 ms | 3715.55 ms | 3626.77 ms | 3817.53 ms |

Each distribution contains 30 warm observations on the same source and accepted input bytes. The first Default run missed the 3,950 ms criterion and is retained in full. The same exact assemblies met the criterion for both profiles on the repeat. The second profile starts in the same process. The direct reference `Seal` diagnostic remains in the timing reports and measures the old method outside the selected public load path. It does not represent a second replay inside the measured candidate operation. [Baseline](baseline/results.json) · [First run](first-performance/results.json) · [Repeat](performance/results.json)

Both complete accepted public console histories match byte for byte, including pending choices, views and canonical checkpoints. The new focused test restores actual partial movement and compares its continuation with both normal live execution and uncached full reference. The r104 negative witnesses exercise malformed input, cross-profile scope rejection, invalid late history after the qualifying crossing, and final canonical mismatch. They preserve full live bytes and revoked authority. Backup rejection preserves the files, and success retains the accepted backup and displaced primary and keeps the committed receipt idempotent. [Connected evidence](connected/results.json) · [Restore and recovery controls](rejections/results.json) · [Source and assembly bindings](BINDINGS.json)

These results apply to the selected strict restoration increment. Unity gameplay integration remains deferred.
