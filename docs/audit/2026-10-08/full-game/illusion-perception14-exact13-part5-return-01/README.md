# Illusion/Perception14 Exact13 Part5 integration return

Start with `ACCEPTANCE.json` and `REVIEW.md`. All eight accepted artifacts are copied byte-identically under `accepted/current/`. This is an external exact-artifact acceptance, not a repository-application receipt or runtime implementation.

`IDENTITY_DISPOSITIONS.json` covers all14 complete procedures and exact source/access records. `SHARED_CLAUSE_DISPOSITIONS.json` covers all19 source-routed clauses. `CASE_PRESERVATION.json` retains the full28 current cases,28 original scenarios and3 supplements with their prior dispositions and conditional limits. `HOLD_REGISTER.json` contains all9 exact prior holds and the independent CompanionExact05 boundary. `SOURCE_PRECEDENCE.json` contains the complete current/frozen source-convergence evidence. `POINTER_OPERATIONS.json` is empty: no further repair is required.

`evidence/accepted_part5_semantic_return/` preserves all10 files from the actual earlier semantic return unchanged. Its operations are historical and must not be applied again to Exact13.

Run `python verify_return.py path/to/this_return.zip --input path/to/DD_Illusion_Perception_14_Exact_13.zip` to check the return manifest and the eight unchanged artifacts against the original submission.

For the independent source/integration checks, run:

```text
python verification/verify_exact13.py DD_Illusion_Perception_14_Exact_13.zip --prior-return DD_Illusion_Perception_14_Part5_Return_01.zip --conference12 DD_Illusion_Perception_14_Conference_12.zip --acceptance-context DD_Control_Illusion_Current_Acceptance_Context_01.zip --out verification-rerun.json
```

Use the actual uploaded filenames, including any `(1)` suffix, for those arguments. The three original-archive arguments are optional and produce additional documented full-byte anchor comparisons. All verification is read-only with respect to input archives; the report output is the only requested write. No input project scripts are executed.

The manifest intentionally excludes itself from its own hash list. The enclosing ZIP SHA256 and external sidecar cover the complete manifest and all members. Authoritative applied membership remains525/323/249 until a separate exact application is verified.
