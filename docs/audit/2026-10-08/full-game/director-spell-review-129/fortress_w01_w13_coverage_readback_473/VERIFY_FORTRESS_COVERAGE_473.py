#!/usr/bin/env python3
"""Verify director-corrected W01–W13 coverage and successor evidence bindings."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
BASE = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


report = load(HERE / "FORTRESS_W01_W13_COVERAGE_RECONCILIATION_473.json")
baseline_path = BASE / "fortress_w01_w13_coverage_readback_429/FORTRESS_W01_W13_COVERAGE_READBACK_429_BINDING_RECONCILED.json"
baseline = load(baseline_path)
correction = load(BASE / "fortress_w01_w13_coverage_readback_472/DIRECTOR_CORRECTION_472.json")
rows = {item["id"]: item for item in report["rows"]}

assert report["status"] == "DIRECTOR_CORRECTED_READ_ONLY_COVERAGE_RECONCILIATION_NO_SEAL_NO_ACCEPTANCE"
assert report["supersedes"]["sha256"] == sha(BASE / "fortress_w01_w13_coverage_readback_472/FORTRESS_W01_W13_COVERAGE_RECONCILIATION_472.json")
assert report["directorCorrection"]["sha256"] == sha(BASE / "fortress_w01_w13_coverage_readback_472/DIRECTOR_CORRECTION_472.json")
assert correction["status"] == "COVERAGE_472_REQUIRES_SUCCESSOR_CORRECTION"
assert sha(baseline_path) == report["priorReadback"]["sha256"]
assert report["sourceCommit"] == "6cc400efd00499864671f2377ab7584a1f50f937"

checked_paths = {item["path"] for item in baseline["verifiedRecordBindings"]}
checked_paths.update(item["path"] for row in baseline["rows"] for item in row.get("latestEvidence", []))
changed = []
for path in sorted(checked_paths):
    result = subprocess.run(["git", "diff", "--quiet", baseline["readAtCommit"], report["sourceCommit"], "--", path], cwd=ROOT)
    if result.returncode != 0:
        changed.append(path)
assert len(checked_paths) == report["counts"]["unchangedPriorSourcePathsVerified"] == 29
assert not changed

for row_id in ("PG328-W01", "PG328-W02", "PG328-W03", "PG328-W06", "PG328-W07", "PG328-W08", "PG328-W09"):
    previous = next(item for item in baseline["rows"] if item["id"] == row_id)
    assert rows[row_id]["disposition"] == previous["disposition"]

for row in report["rows"]:
    if isinstance(row.get("evidence"), list):
        for binding in row["evidence"]:
            assert sha(ROOT / binding["path"]) == binding["sha256"], f"hash mismatch: {binding['path']}"

assert rows["PG328-W11"]["disposition"] == "COMPONENT_SUFFICIENT_UNSEALED"
assert "not certified" in rows["PG328-W11"]["limitation"]
assert rows["PG328-W12"]["disposition"] == "COMPONENT_SUFFICIENT_UNSEALED"
assert rows["PG328-W13"]["disposition"] == "COMPONENT_SUFFICIENT_UNSEALED"
assert len(rows) == report["counts"]["rows"] == 13
assert sum(row["disposition"] == "COMPONENT_SUFFICIENT_UNSEALED" for row in rows.values()) == report["counts"]["componentSufficientUnsealed"] == 9
assert sum(row["disposition"] == "SEALED_TEST_ONLY_COMPONENT" for row in rows.values()) == report["counts"]["sealedTestOnlyComponents"] == 4
assert report["counts"]["openIntegrations"] == 0
assert correction["verifiedByDirector"]["openIntegrations"] == 0
assert report["scope"]["heldIds"] == ["conjure-demiplane-fortress"]
assert report["scope"]["identityDecision"].startswith("PENDING_")
assert report["authority"]["reviewedApplied"] == 830
assert report["authority"]["pending"] == 18
assert report["authority"]["acceptedUnapplied"] == 0
assert report["nonEffects"]

print("PASS: director correction 472 incorporated; five prior PASS rows restored")
print("PASS: 29 previous evidence paths unchanged from pinned readback")
print("PASS: all listed successor artifacts match their reviewed hashes")
print("PASS: 13 rows = 9 unsealed-sufficient + 4 sealed + 0 open")
print("PASS: Fortress remains held pending identity-level reconciliation")
