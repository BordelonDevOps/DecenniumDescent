#!/usr/bin/env python3
"""Verify the Fortress identity-level source bindings and decision boundary."""

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


def git_blob_sha256(path: str) -> str:
    data = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
    return hashlib.sha256(data).hexdigest()


report = load(HERE / "FORTRESS_IDENTITY_LEVEL_RECONCILIATION_474.json")
coverage = report["coverageReconciliation"]
bindings = [
    (coverage["path"], coverage["sha256"]),
    (report["retainedProcedure"]["path"], report["retainedProcedure"]["gitBlobSha256"]),
    (report["historicalCoverage"]["initialCoverageMap"]["path"], report["historicalCoverage"]["initialCoverageMap"]["gitBlobSha256"]),
    (report["historicalCoverage"]["byteReconciledReadback429"]["path"], report["historicalCoverage"]["byteReconciledReadback429"]["sha256"]),
    (report["historicalCoverage"]["directorCorrection472"]["path"], report["historicalCoverage"]["directorCorrection472"]["sha256"]),
    (report["identityQualifications"]["currentHoldRegister"]["path"], report["identityQualifications"]["currentHoldRegister"]["gitBlobSha256"]),
    (report["identityQualifications"]["historicalDirectorDecision200"]["path"], report["identityQualifications"]["historicalDirectorDecision200"]["gitBlobSha256"]),
    (report["identityQualifications"]["currentCatalogEntry"]["path"], report["identityQualifications"]["currentCatalogEntry"]["gitBlobSha256"]),
    (report["currentAuthority"]["queuePath"], report["currentAuthority"]["queueSha256"]),
]
for path, expected in bindings:
    assert git_blob_sha256(path) == expected, f"Git blob SHA-256 mismatch: {path}"

procedure = load(ROOT / report["retainedProcedure"]["path"])
hold_register = load(ROOT / report["identityQualifications"]["currentHoldRegister"]["path"])
director_decision = load(ROOT / report["identityQualifications"]["historicalDirectorDecision200"]["path"])
queue = load(ROOT / report["currentAuthority"]["queuePath"])
state466 = load(BASE / "CURRENT_REVIEW_STATE_466_REPACK10.json")
catalog = load(ROOT / report["identityQualifications"]["currentCatalogEntry"]["path"])
catalog_entry = next(item for item in catalog["spells"] if item["id"] == "conjure-demiplane-fortress")
b06 = next(item for item in hold_register["newHolds"] if item["id"] == "PG200-B06")
retained = [item for item in hold_register["newHolds"] if item["id"].startswith("PG200-H") and "conjure-demiplane-fortress" in item.get("spellIds", [])]
decision = next(item for item in director_decision["perIdentity"] if item["spellId"] == "conjure-demiplane-fortress")

assert procedure["status"] == report["retainedProcedure"]["status"]
assert procedure.get("operational") is None
assert b06["status"] == "OPEN" and b06["blocking"] is True and len(b06["caseIds"]) == 14
assert len(retained) == 10 and all(item["status"] == "RETAINED" and item["blocking"] is False for item in retained)
assert decision["accepted"] is False and decision["applied"] is False
assert catalog_entry["status"] == "blocked-pending-operational-review" and catalog_entry["operational"] is None
assert queue["currentAuthority"]["reviewedApplied"] == 830
assert queue["currentAuthority"]["pending"] == 18
assert queue["currentAuthority"]["acceptedUnapplied"] == 0
assert "conjure-demiplane-fortress" in queue["remainingPendingIds"]
assert queue["nextIdentity"] == "conjure-demiplane-fortress"
assert state466["componentDispositions"]["W11-456"].startswith("PASS")
assert state466["componentDispositions"]["W12-451"].startswith("PASS")
assert coverage["openIntegrations"] == 0 and coverage["rows"] == 13
assert coverage["qualificationLimitations"]
assert report["scope"]["identityAcceptanceGranted"] is False
assert report["scope"]["identityApplicationGranted"] is False
assert all(value is False for value in report["nonEffects"].values())

print("PASS: corrected coverage 473 and retained/historical source bindings match Git blobs")
print("PASS: all 13 components sufficient or sealed; zero open integrations")
print("PASS: PG200-B06 remains OPEN; H01–H10 remain retained nonblocking qualifications")
print("PASS: procedure/catalog remain unresolved; current queue remains 830/18/0")
print("PASS: identity decision requested; no acceptance, application, or mutation recorded")
