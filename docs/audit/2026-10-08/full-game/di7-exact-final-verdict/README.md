# DI7 exact reviewer package

Start with **DI7_EXACT_VERDICT.md**. Review ID: `DI7-EXACT-REVIEW-01-FINAL`.

Accepted scope: seven manifest-bound authored operational procedures and their full shared/public/internal presentation. No operative spell replacements. DI7-EV01 is an evidence-only classification to append beside the preserved report. No submitted file was edited.

## Main files

- `DI7_EXACT_CARD_REGISTER.json`: all7 individual decisions, source pointers, findings and14 examples.
- `DI7_EXACT_CASE_DISPOSITIONS.json`: all93 original/supplemental expectation dispositions with exact submitted and fresh evidence references.
- `DI7_EXACT_ISSUE_DISPOSITIONS.json`:13 mechanical decisions and DI7-X14 receipt.
- `DI7_EXACT_ACCEPTANCE_AUTHORITY.json`: finite local recording/index scope, forbidden promotions and remaining particular dependencies.
- `DI7_EVIDENCE_SCOPE_ADDENDUM.json`: exact guarded DI7-EV01 scope clarification.
- `DI7_EXACT_CORRECTIONS.json`: empty operative replacement list.
- `DI7_SUBMISSION_BINDING.json`, `DI7_SOURCE_LOCATIONS.json`, `DI7_READ_SCOPE.json`: exact provenance and inspection limits.
- `SUBMISSION_VERIFICATION.json`, `INDEPENDENT_SUBMISSION_CHECKS.json`, `REPRODUCTION_RESULTS.json`: actually executed checks.
- `reviewer_fresh_results/`:15 new bounded suite reports, not replacements for submitted historical reports.
- `REVIEWER_DIAGNOSTIC_RESOLUTION.json`: reviewer-tool diagnostics and their corrections.
- `OUTPUT_MANIFEST.json`: hashes of this final package's other payloads; does not hash itself.

## Reproduce without modifying the submission

Python standard library only. Supply an extracted original ZIP as `SUBMISSION`, and a separate writable `OUTPUT` directory. Do not use a submitted source directory as the output directory.

```text
python -B verify_exact_submission.py --submission SUBMISSION --out OUTPUT/INDEPENDENT_SUBMISSION_CHECKS.json
python -B reproduce_submitted_checks.py --submission SUBMISSION --out OUTPUT/reviewer_fresh_results
```

Check each script's `--help` for its exact arguments. The second wrapper redirects submitted suite report writes into OUTPUT, retaining input source paths and game predicates. The independently authored checker reconstructs the full manuscript and compares complete envelopes as well as bindings and inverses.

Fresh run timestamps/output-root bindings may differ, so reproduction means matching the explicit checks and scoped results, not necessarily identical report bytes. Historical input-binding differences are retained, not rewritten as current runs.

The bundle is reviewer evidence, not a player publication or application runtime. Conditional actor/world assumptions remain assumptions. No arbitrary future Fate payload, campaign authentication, human balance, class/feat promotion, cosmology or whole-game approval is supplied.
