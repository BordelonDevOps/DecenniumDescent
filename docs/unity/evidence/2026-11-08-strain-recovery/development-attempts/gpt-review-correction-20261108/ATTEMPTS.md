# GPT review correction attempts (2026-11-08)

This folder preserves every failed focused run from the correction window plus the two temporary compiler diagnostics. The final retained focused and full-suite reports are in the parent evidence folder; the failures below were not suppressed.

## Reproduced findings and fixes

- The first updated fixture still expected the old number of ineligible Strain points after starting from hour 32. The trace confirmed two distinct missed Watch events and one qualifying due event; the scenario's expected facts were corrected to match the clock and event history.
- The first 24-hour regression incorrectly expected recovery at hour 48. The corrected rule records the hour-40 Rest even while provisioning is blocked, so the hour-48 gate opening is too early for another beneficial Rest. The acceptance now expects no offer at hour 48 and offers at the exact hour-64 boundary.
- The first exact-boundary assertion did not include the correct retained clock target. The scenario now requests hour 65, completes the hour-64 Rest, observes the pending offer while the accepted target remains saved, resolves the offer, and asserts a single resume to hour 65. It also compares a split hour-60→64 then 64→65 trace.
- Recovery resolution initially returned `InvalidResult` because it appended a second beneficial-Rest record while the completion record already existed. Resolution now links the offer to and reuses the completion record.
- A restored split-trace candidate was rejected because the test generated duplicate beneficial-Rest records for one Rest interval. The scenario now forks from the persisted pre-offer state and compares the supported split trace without fabricating duplicate history.
- One subsequent replay assertion exposed divergence after the continuation/benefit changes. The resolver now resumes only after the last pending recovery/manufacturing choice and keeps the v2 completion/removal relationship valid. The final two-branch snapshot comparison and restore roundtrip pass.
- Two intermediate test-instrumentation builds failed because diagnostics referenced nonexistent `RestWatchOutcomeRecord.Kind` and `Command.Fingerprint` members. Those temporary diagnostics were removed; they were fixture/compiler errors, not runtime API changes.

## Binding audit attempt

One earlier `Validate-RuleBindings.ps1` invocation used its default 2026-11-05 binding manifest and failed before binding tests because that historical manifest pins `Runtime/Core/ActorConditionRecord.cs` to an older hash. The dedicated schema64 manifest was then run explicitly against the final full-suite report and passes all four pinned sources, 17 profiles, 340 RP cells, and 18 named cases. The failed default-manifest report is retained as `default-bindings-stale-source.json`.

## Final result

After the corrections: focused case **1/1 PASS**, full suite **1,260/1,260 PASS**, explicit Core/Persistence/LabModel compilation **PASS**, static package **18/18 PASS**, and schema64 source-binding audit **PASS**. The final evidence JSONs and compiled assemblies are in the parent folder. Unity checks were not performed.
