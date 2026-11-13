Actual Unity Rules Engine Development reply `e371a0e0-6313-4c8e-a517-02f2f3ed9a35`, recorded verbatim apart from trailing whitespace.

## MGT-06 evidence corrections — substantive findings resolved; final execution remains pending

**Gameplay source:** `71e6612cbdc07d2e8e2f347f38355e62c493d5c6`
**Evidence correction reviewed:** `3f5c8fdd1b97f149aca805e75188645a442233ba`
**Prior review:** `182c0bfb-11fa-4e80-a965-44039d4b3f00`

**The two substantive evidence findings are addressed. The corrected walkthrough checks are adequate for the retained run, and the new regression machinery provides the missing execution-to-assembly binding.**

There is **one small, nonblocking verifier typo** to correct when preparing the final packet: the work-type redaction predicate reads `Category`, but the public property is `Kind`. The existing Trap-ID predicate remains effective, so this does not invalidate the present redaction evidence or require a gameplay rebuild or regression restart.

**Final bounded acceptance remains pending the completed, bound 1,486-case journals. No gameplay-source correction is requested.**

## 1. Public walkthrough verification — substantive finding closed

I read the complete corrected `Test-TrapWalkthrough.ps1`. Its expected observations now come from the input chronology, rather than from the output’s own `ObservedLocally` claim.

The verifier requires every expected observation checkpoint to occur. At away checkpoints it explicitly requires `ObservedLocally=false` and null physical status, outcome and captured identity. At local-result checkpoints it requires local observation and compares the reported outcome and creature identity with the actual resolved save. It also requires an enabled Player Trap view, rather than allowing a missing or failed view to satisfy nullable-field checks.

The other requested checks are now explicit:

| Previous gap | Corrected check |
|---|---|
| A failed load could leave the same final bytes | Every `save` must return `Saved`; every `load` must return `Restored`. |
| Exact retries were not required to return Duplicate | Both Set and Retrieve retries must return `Duplicate` at revision 240 and clock 60478. |
| Unexpected fresh repeat acceptance | Both fresh claims must return `Unavailable` without advancing that endpoint. |
| Only one console history received the checks | `Assert-Console` runs against both the restored and uninterrupted console transcripts. |
| Rejected restore atomicity checked only revision | Each wrong-profile and altered-history rejection now compares complete canonical live-save hashes before and after. |

The C# branch remains accurately characterized as **committed-action replay**, with automatic defender planning invoked again. It is not being presented as independent replay of every rejected console input.

The updated result records identical before/after hashes for both cross-profile directions and the false-history rejection. All four checkpoint hashes remain unchanged, including the final r242 continuation:

```text
14add8d9963d41cbdec7433254413fc095499f1ad02086065608acdc14dda712
```

The result still records the actual natural **13 + 2**, one RNG word, check at **60174**, retrieval at **60478**, and continuation at **60480**. These are retained execution results I inspected—not executions I performed.

### Minor verifier cleanup: `Kind`, not `Category`

The generic-work assertion currently contains:

```powershell
$_.Id -like 'fishing.trap.*' -or $_.Category -match 'Fishing|Trap'
```

`ExpeditionWorkStatus` exposes **`Kind`**, not `Category`. Replace the second predicate with:

```powershell
$_.Kind -match 'Fishing|Trap'
```

The ID predicate already detects this lifecycle’s actual attempt/retrieval identities, so the selected run has not passed solely because of the incorrect property name. Nevertheless, the intended second predicate should inspect the real public field.

This is an evidence-script correction only. Check it against the retained transcripts when preparing the final evidence; **do not rebuild gameplay or restart the full regression for it**.

## 2. Regression execution provenance — mechanism accepted

The new launcher and worker address the original problem directly. The packager no longer merely attaches whichever DLL identities were supplied with `--headless` to an unrelated set of journals.

### Before execution

The launcher creates a fresh run directory, copies the four DLLs into a dedicated execution directory, and writes a launch manifest containing the assembly digests, complete-inventory digest, six assignment digests and unique run ID before starting the workers.

Each worker then:

- Rejects an existing journal instead of silently resuming it.
- Checks the inventory and assignment against the launch.
- Checks each DLL’s digest before loading.
- Confirms the actual loaded assembly location and records its module identity.
- Checks the compiled inventory.
- Writes its PID, group, launch identity and loaded-assembly record **before executing cases**.

### At completion and packaging

The worker rechecks the execution files, hashes its completed journal and writes its completion record before `DONE`.

The packager requires the launch digests to equal the retained focused DLL digests. For every shard it matches the start record to the launch, process PID, assignment and inventory; requires the completion record to preserve the start-record fields; verifies the journal digest and case count; and retains the original ordered-result, uniqueness, passing-result and focused-row checks.

**That is an adequate bounded provenance chain.** It prevents the earlier paths-only journals from being treated as this new run and prevents mismatched run artifacts from being packaged under the focused DLL identity.

### Actual start records inspected

I read the launch manifest, process list and **all six** `shard*.started.json` records. They agree on:

- Run ID **`d7820b43641040f0a1980ecf96b565ae`**.
- The same four reviewed DLL SHA-256 values.
- Matching module IDs across workers.
- The complete-inventory digest.
- Each shard’s recorded PID and assigned digest.

The process counts total the expected 1,486 cases. These are **pre-execution/start records**, not evidence that those cases have finished.

The binding correctly continues to report `regressionCases: null`. **I am accepting the corrected verification mechanism and its retained launch evidence—not prematurely accepting the unfinished regression.**

## 3. Historical standalone provenance — addressed

The historical verifier now records the assemblies actually loaded, including their SHA-256 values and module IDs, for both generation and restoration. It checks loaded locations rather than reporting only the requested assembly directory.

The two reports preserve distinct assembly sets while agreeing on the schema37, revision-2 soaking state and save digest:

```text
827bfaa4398e4aa0a7173c865851ed5c48aca9d87d6de7fd875eb7ab9863e29d
```

The restoration set agrees with the current focused assemblies. The packager checks the generation set against the retained prior build and the restoration set against the current packet, then requires matching save identities. This addresses the earlier distinction between **creating an authentic predecessor under prior assemblies** and merely restoring a newly created save under current assemblies.

**I inspected the records and checking logic; I did not independently load those assemblies or hash the archived binaries.**

## 4. Remaining acceptance gate

The substantive focused evidence holds are resolved. The final return should contain the completed evidence already required by the corrected packager:

**The same launch, all six matching start/completion records, ordered assignments and journals, completion markers, the exact 1,486-name inventory, final results and updated bindings.**

The inventory remains **1,485 accepted predecessors plus the one new MGT-06 control**. Preserve the superseded paths-only launch separately; do not merge its journal results into the fresh bound run.

The small `Kind` correction can accompany that final evidence. **No additional gameplay scenario, source/API proposal, outcome change or redundant full run is requested.**

P1’s timing disposition is unchanged. The updated single-run measurements are not a new latency acceptance, and strict external validation remains required.

## Inspection limits and final disposition

For this follow-up I inspected the evidence correction, README, complete corrected walkthrough verifier, complete launcher/worker/packager, historical verifier and both historical reports, updated connected report and bindings, launch/process manifests, and all six worker start records. I also checked the unchanged public work-status declaration to confirm the property-name discrepancy.

**I did not execute scripts or tests, compile, load DLLs or binary saves, independently rerun either console history, recompute artifact hashes, inspect completed journals that are not yet supplied, or modify repository files.** The prior gameplay-source review remains the basis for the unchanged implementation findings.

**Disposition: substantive evidence corrections accepted; one nonblocking verifier-field cleanup identified. Final MGT-06 acceptance remains pending only the completed exact-bound execution and its final package.**

No gameplay-source correction or regression restart is requested. Prior acceptances stand; broader P1 and INT-03 remain open, no successor is authorized, and Unity gameplay integration remains deferred.
