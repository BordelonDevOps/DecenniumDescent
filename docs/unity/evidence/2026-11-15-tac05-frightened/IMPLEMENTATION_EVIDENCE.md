# TAC-05 implementation evidence

Source checkpoint **`f5800818bfadb7c51865c96a6058f9af2deb75a3`** is committed on `Engine`. This packet is interim while the original exact regression completes. It is not final TAC-05 acceptance; CHR-03 and Unity integration remain held.

`IMPLEMENTATION_BINDINGS.json` binds all41 changed engine files, the exact engine archive, pinned source records, build/static source hashes, executed assemblies, external drivers, inputs, checkpoints and worker identities. `REGRESSION_PROGRESS.json` explicitly distinguishes an incomplete prefix from a full passing run. The launch predates the checkpoint commit; the retained compiled-source hashes and frozen DLLs are verified against that immutable commit without rewriting the original launch record.

## Executed evidence

| Evidence | Observed result |
| --- | --- |
| C#9 headless compile with warnings as errors | PASS; both new connected cases pass;130 additional selected component cases pass (132 focused total). |
| Independent standalone compile | PASS for Core, Persistence and LabModel. |
| Static package check | PASS; this is not Unity compilation. |
| Main connected route |216 committed commands: exploration, first encounter, specimen, research, six-dose recipe4 manufacture, reinforced encounter, actual source uses/recharge, affected attack, repeat ending, normal closure and paid ordinary continuation. |
| Paid check route |186 commands: physical thieves-tool retrieval, real locked-cache Action with disadvantage, failed repeat and exact final expiry. |
| Sight-loss route |181 commands: paid movement behind the authored blocker, unchanged closer-movement denial, ordinary one-die paid Hide while fear remains. |
| Persistence/replay |19 canonical checkpoints match across five execution paths;95 comparisons. Inputs and outputs are retained, including independent typed dispatch and separate receipt replay. |
| Authentic prior saves |19 actual wire95–106 saves round-trip exactly and execute their remaining recorded commands to the expected final bytes; all reject unchanged into the new profile. |
| Source boundaries |11 supplementary controls pass: wrong context, pre-level class, three history capacities, second-target journal capacity, public stale revision, forged DC/source/revision/feared entity. Existing focused cases retain perception, grant, choice, Action/recharge, immunity and ordering controls. |
| Console boundaries |10 parser/constructor/id-conflict/forced-field controls pass, separate from the existing authority/spent-Action/exact-retry probe. The first harness attempt expected `Conflict`; the engine correctly returned `CommandIdConflict`. The failed expectation and corrected run are both retained. |
| Historical causality |Four structurally encodable forged records reject strict restore unchanged: old cache natural, WIS modifier, ended-fear attack modifier, unseen-Hide modifier. |
| Shared components |Independent relationships/advantage cancellation/dead source, qualified all-eligible cure, suppression/immunity, real forced Push producer, actor-only dynamic geometry, exact pending-edge suspension and whole/split clock progression pass with detached labels. |
| Closure intersection |[Reviewed scope exception](GPT_CLOSURE_GUIDANCE.md): **not demonstrated; reviewed scope exception**. Genuine fourth-use closure denial retains identical bytes. Detached actual closure-path control passes failed-repeat retention, final expiry during closure, and final expiry through subsequent ordinary clock advancement. |
| Full regression |Original run `d9620202bba1434aa4885782edb2888d`,1517 cases, six frozen-DLL workers. See the exact current status; incomplete journals are not passes. No replacement run was started. |

The party helper named `ClericGuard` submits Aggressive stance ordinal1. The retained command/snapshot values, not the helper name, define the scenario. The applying defender's ordinary tactic uses its own actual stance and Action. There is no source regrant, edited RNG/HP/position, scenario reset, player fear cure, Radiance producer or earned Warrior build in the genuine connected routes.

[Consumer audit](CONSUMER_AUDIT.md) distinguishes shared hooks, actual witnesses and unavailable combinations. The internal source-qualified cure component has only its explicit detached-test invocation factory here; future lawful gameplay producers must supply their own authority/payment/trigger validation. TEST_ONLY fixture entitlement is not production authorization.

## Retained layout and reproduction

`retained-development/` preserves selected paths from `engine/artifacts/tac05-frightened/development/`. The external scripts were executed from that original workspace location; copy them there in an isolated checkout to preserve their repository-relative tool references. Do not overwrite an active run. Use fresh output paths for any independent rerun. Recorded absolute paths identify the original execution, while hashes identify the retained inputs.

The source build commands are:

```powershell
pwsh -NoProfile -File engine/tools/Test-Foundation.ps1 -ResultsRoot engine/artifacts/tac05-rerun -CaseName tac05_frightened_connected_paid_ability_check
pwsh -NoProfile -File engine/tools/Compile-Foundation.ps1 -ResultsRoot engine/artifacts/tac05-rerun
pwsh -NoProfile -File engine/tools/Validate-Package.ps1 -ResultsRoot engine/artifacts/tac05-rerun/static
```

Point `Run-ConnectedCase.ps1 -AssemblyRoot ... -CaseName tac05_frightened_connected_activation_restore_and_recharge` and `Run-SourceIntegrationControls.ps1 -AssemblyRoot ...` at the newly produced headless assemblies. `Test-FrightenedPaths.ps1 -AssemblyRoot ... -TraceRoot ... -Run ...` accepts each retained `trace-*` directory and executes its five paths; its independent typed constructor does not decode receipts. `Test-Compatibility.ps1 -AssemblyRoot ... -Run ...` uses the authentic predecessor inputs still committed in their own evidence packets.

The specific component/boundary drivers and their named input parameters are retained beside their results. In particular, `Test-FrightenedClosureTransition.ps1` takes the genuine affected-cache, before-final-expiry and fourth-use attack saves. It changes only the source life record in its explicitly detached cases, preserves target relationship/RNG/calendar/endpoints, and calls the actual shared resolver for closure and subsequent ordinary time. It separately restores the untouched fourth-use save into the public session and verifies the rejected closure's bytes. Its JSON summaries are component evidence, not asserted valid connected saves.

The exact regression launcher and original worker are retained. A new independent run must use a fresh directory and retain its own run ID; do not replace the original workers or journals. `Retain-Evidence.py` verifies immutable source/build/input bindings and records an interim prefix. `Retain-Evidence.py --complete` additionally requires all six original completion identities, assignment order, journal hashes, DONE markers and all1517 passing results before producing final-review-ready evidence. It does not execute or imply GPT acceptance.

The historical contract verifier deliberately asserts an unchanged engine at its proposal baseline and must not be used as a post-implementation runtime validator. The new retainer rehashes the pinned authority/source blobs without rerunning that obsolete pre-implementation assertion.
