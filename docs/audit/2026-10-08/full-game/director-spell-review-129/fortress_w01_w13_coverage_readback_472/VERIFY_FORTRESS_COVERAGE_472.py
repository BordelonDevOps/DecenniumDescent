#!/usr/bin/env python3
"""Verify the read-only W01–W13 coverage reconciliation and W13 director pass."""

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
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


report = load(HERE / "FORTRESS_W01_W13_COVERAGE_RECONCILIATION_472.json")
baseline_path = BASE / "fortress_w01_w13_coverage_readback_429/FORTRESS_W01_W13_COVERAGE_READBACK_429_BINDING_RECONCILED.json"
baseline = load(baseline_path)
readback = load(BASE / "fortress_w13_nested_space_witness_471/DIRECTOR_READBACK_471.json")
delivery = load(BASE / "fortress_w13_nested_space_witness_471/DELIVERY_471.json")

assert report["status"] == "READ_ONLY_COVERAGE_RECONCILIATION_NO_SEAL_NO_ACCEPTANCE"
assert report["sourceCommit"] == "6cc400efd00499864671f2377ab7584a1f50f937"
assert sha(baseline_path) == report["priorReadback"]["sha256"]
assert baseline["readAtCommit"] == report["priorReadback"]["readAtCommit"]
assert readback["status"] == "PASS_ADOPTED_TEST_ONLY_COMPONENT_SUFFICIENCY"
assert readback["reviewedPacket"]["witnessSha256"] == delivery["witness"]["sha256"]
assert readback["reviewedPacket"]["traceSha256"] == delivery["trace"]["sha256"]
assert readback["reviewedPacket"]["archiveSha256"] == delivery["archive"]["sha256"]

source_commit = report["sourceCommit"]
checked_paths = {item["path"] for item in baseline["verifiedRecordBindings"]}
checked_paths.update(item["path"] for row in baseline["rows"] for item in row.get("latestEvidence", []))
changed = []
for path in sorted(checked_paths):
    result = subprocess.run(["git", "diff", "--quiet", baseline["readAtCommit"], source_commit, "--", path], cwd=ROOT)
    if result.returncode != 0:
        changed.append(path)
assert len(checked_paths) == report["counts"]["unchangedPriorSourcePathsVerified"] == 29
assert not changed

rows = report["rows"]
assert len(rows) == report["counts"]["rows"] == 13
assert sum(row["disposition"] == "COMPONENT_SUFFICIENT_UNSEALED" for row in rows) == report["counts"]["componentSufficientUnsealed"] == 4
assert sum(row["disposition"] == "SEALED_TEST_ONLY_COMPONENT" for row in rows) == report["counts"]["sealedTestOnlyComponents"] == 4
assert sum(row["disposition"].startswith("OPEN_INTEGRATION") for row in rows) == report["counts"]["openIntegrations"] == 5
assert rows[-1]["id"] == "PG328-W13" and rows[-1]["directorDecision"] == readback["status"]
assert report["openIntegrations"] == ["PG328-W04", "PG328-W05", "PG328-W10", "PG328-W11", "PG328-W12"]
assert report["authority"]["reviewedApplied"] == 830
assert report["authority"]["pending"] == 18
assert report["authority"]["acceptedUnapplied"] == 0
assert report["scope"]["identityDecision"] == "NOT_EXECUTED"
assert report["scope"]["heldIds"] == ["conjure-demiplane-fortress"]
assert report["nonEffects"]

print("PASS: 29 prior evidence paths unchanged")
print("PASS: W13-471 director hashes and status cross-bind")
print("PASS: 13 rows = 4 unsealed-sufficient + 4 TEST_ONLY-sealed + 5 open")
print("PASS: Fortress remains held; queue is 830/18/0; no identity decision")
