# Pack 20 Orchestrator

Run **Statistical Integrity Audit** against the frozen V7.2 source.

Audit every numerical conclusion. Verify seed independence, sample size, confidence intervals, training/holdout separation, fixture hashes, duplicate-run detection, and whether the result supports the stated claim. Reject narrative estimates and missing raw evidence.

Write one JSON file per seed or fixture under `results/raw/`; then write `COMPILED_REPORT.md`. Do not edit canon.
