# MGT-10 desk restriction correction

[Correction commit](https://github.com/BordelonDevOps/DecenniumDescent/commit/d2085f510d74214e1b1eecefcde5d4ddbf5f3022) addresses GPT's B1 and E1 findings for the bounded Haven appraisal. The source change is a single shared `CraftingRestrictions.StationUseBlocked` check on the exact desk inside the eligibility predicate used by start, reconciliation, resume and finalization. The schema, service terms, work duration and valuation remain those reviewed for the initial candidate. [Initial review](../GPT_REVIEW.md)

## Corrected behavior

- The exact pre-fix assemblies let appraisal progress from 300 to 1,800 seconds and produce 15/2 cp after an occurred result-1 station restriction. The same normal command trace against corrected assemblies records immediate pause at clock 2,114, 300 seconds retained, and 300 seconds after another 1,500 elapsed seconds with the restriction still active. [Reproducer](../Verify-AppraisalDeskRestriction.ps1) · [Pre-fix trace](../baseline-desk-restriction.json) · [Corrected trace](desk-restriction.json)
- The focused tests verify blocked admission and blocked unfinished-work resumption, immediate truncation of worker time, a retained whole-lot claim, and no labor during the existing one-hour cleanup. After cleanup, explicit resumption completes the remaining 1,500 seconds. A separate case retains all 1,800 earned seconds during endpoint incapacity, dispatches the desk restriction, cures the worker, and confirms the desk still blocks explicit finalization until normal cleanup. The final resume spends neither labor nor RNG. [Focused results](focused/run-20261111T071756803Z-b51e6944/results.json)
- A separate case denies appraisal and its query to a principal with worker control and no inventory-owner grant. It books normal crafting remedy labor for the same worker at the desk and verifies appraisal rejects while that worker is busy. After cancellation of that booking, appraisal remains eligible under a result-5 order-specific restriction. A shortened lot and a portable link to the wrong unit fail appraisal admission and snapshot validation. [Exact correction diff](https://github.com/BordelonDevOps/DecenniumDescent/commit/d2085f510d74214e1b1eecefcde5d4ddbf5f3022)

## Retained checks

- **9/9 focused cases**, including the three correction cases and the original connected save/replay trace.
- **168/168 historical cases** cover shared-world activity, mining, portable handling, combat, connected resource management, and existing crafting, research and remedy behavior. Their 287 source hashes agree with the focused report. [Historical results](historical/run-20261111T071756806Z-2b49cb55/results.json) · [Exact evidence bindings](BINDINGS.json)
- Standalone C# 9 warnings-as-errors compilation passed for Core, Persistence and LabModel. Static package validation passed **18/18**, with 313 assets and 313 unique GUIDs. [Compilation](compile/compile-20261111T071757577Z-560f8323/results.json) · [Static package](static/static-20261111T071757698Z-94a4db88/results.json)
- The pre-change schema 43 before/after save verifier passed on the corrected assemblies. The previous save and continuation are byte-identical, with the historical retrieval restriction and wrong-profile rejection preserved. [Legacy verification](legacy-verification.json)

The initial unfiltered run was stopped once the reviewed defect was reproduced. The unfiltered suite is running against this corrected source. Unity gameplay integration remains deferred.
