# FEAT335 acquisition / initial-state audit evidence

Start with FEAT335_ACQUISITION_AUDIT_VERDICT.md. The full row-by-row deliverable is ACQUISITION_ROWS.json and ACQUISITION_ROWS.md. Each of all335 IDs has five obligation sections and exact submitted bindings. FINDINGS_AND_REPLACEMENTS.json and GUARDED_CORRECTIONS.json provide the four finite findings and exact derived operations; they have NOT been applied to the submitted tree.

MENU_AND_SNAPSHOT_ATLAS.json retains the real menus and exact members. SUPPLEMENT_AUDIT.json covers all nine supporting groups and the two outside-catalog proposals. FINITE_REMAINING_WORK.json separates corrections, assembly evidence, and carried preservation-only conditions. ACCEPTANCE_EXPECTATIONS.json contains authored finite expectations, not asserted runtime passes.

EVIDENCE_REPORT_INDEX.json preserves all20 report scopes and current-versus-historical source binding comparisons. REPORT_SNAPSHOT_MISMATCHES.json inventories559 actually observed mutable-report discrepancies. REPRODUCTION_RESULTS.json contains the reviewer’s executed source/reference checks and isolated counterexamples, not a rerun of the20 original suites.

Reproduce in Python3 standard library:

```sh
python -X utf8 reproduce_acquisition_audit.py --archive /path/to/DD_FEAT335_Acquisition_Audit_01.zip --output /path/to/new-audit-output
```

Or use `--submission /path/to/extracted-packet`. The checker writes only to the requested output directory; it imports bounded source models with bytecode writing disabled. It does not run submitted validator main functions, enable gameplay selection, change originals or authenticate a campaign. On Windows use an appropriately short extraction path if historical names approach path-length limits.

All files here are reviewer-generated evidence. The submitted archive remains unchanged. Package manifest hashes every payload except itself. No final-feat, class, spell, runtime, human-balance or whole-game promotion is authorized.

Validate the delivered rows, source links and all14 correction guards without applying them:

```sh
python -X utf8 validate_audit_package.py --submission /path/to/extracted-packet --package /path/to/this-evidence-folder
```

`DELIVERABLE_QA.json` records4917/4917 deliverable/preservation checks. This is separate from the4194 source/reference/model-counterexample checks in `REPRODUCTION_RESULTS.json`; neither count represents335 complete gameplay acquisitions. The QA command writes its report in the evidence folder, not the source tree. Copy the evidence folder before re-running if its delivered report hash must be preserved.
