# Independent review — action query increment

## Findings and disposition

- `source_review` found that discovery filtered out unseen targets even when their locations were known. Existing ranged rules allow attacks at known unseen locations with disadvantage. Discovery now keeps those targets, and `repeating_crossbow_discovery_retains_known_unseen_attack_targets` covers the behavior.
- `review_fnd05` found no further actionable issue in query authority, revision and idempotency checks, detached read-only assessment, or the shared ranged preflight.
- `source_review` found no further source-integrity or transaction discrepancy after the visibility correction.

## Independent focused execution

`source_review` independently executed **25/25** nondisk cases from the final headless build `run-20261104T185048310Z-e97074a8`: 10 ranged-roll cases, 8 composed-shot cases, and 7 shared crossbow/query/controller cases. The focused run included the known-but-unseen regression. It excluded the initial-equipment save and critical-attack save cases. The reviewer made no file changes.

This does not substitute for the separately recorded full 1,055-case suite, Unity import or runtime validation.
