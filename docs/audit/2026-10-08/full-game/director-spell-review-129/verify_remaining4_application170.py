from __future__ import annotations

import gzip
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUD = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PACKAGE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8remaining4_reviewed_169"
IDS = ["prismatic-wall", "faction-convergence", "divine-intervention-lesser", "reality-patch"]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def binding(path: Path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": digest(data)}


def main():
    checks = []

    def check(label, condition):
        checks.append({"check": label, "passed": bool(condition)})

    before_path = AUD / "authored_review_index.before_remaining4_170.json"
    before_bytes = before_path.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    index_bytes = INDEX.read_bytes()
    after = json.loads(index_bytes.decode("utf-8-sig"))
    catalog_bytes = CATALOG.read_bytes()
    catalog = json.loads(catalog_bytes.decode("utf-8-sig"))
    operations = read(AUD / "REMAINING4_INDEX_OPERATIONS_170.json")
    acceptance = read(AUD / "REMAINING4_EXACT_ACCEPTANCE_169.json")
    app = read(AUD / "REMAINING4_APPLICATION_170.json")
    local_audit = read(AUD / "REMAINING4_RETURN169_INDEPENDENT_AUDIT.json")
    return_receipt = read(AUD / "REMAINING4_GPT_RETURN_169.json")
    queue = read(AUD / "CURRENT_SPELL_QUEUE_170.json")
    handoff = read(AUD / "CURRENT_HANDOFF_170.json")
    pending_doc = read(AUD / "CURRENT109_PENDING_IDENTITY_AUDIT_170.json")
    model = read(PACKAGE / "MODEL.json")
    manifest = read(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json")

    before_rows = {r["id"]: r for r in before["entries"]}
    after_rows = {r["id"]: r for r in after["entries"]}
    catalog_rows = {r["id"]: r for r in catalog["spells"]}
    pending = sorted(r["id"] for r in after["entries"] if r["authoredStatus"] == "pending-authored-procedure")
    changed = [r["id"] for r in after["entries"] if r != before_rows[r["id"]]]
    inverse = json.loads(index_bytes.decode("utf-8-sig"))
    for op in operations["operations"]:
        inverse["entries"][op["index"]] = op["before"]
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = before["authoredCounts"]
    inverse["representationCounts"] = before["representationCounts"]

    check("Exact four director IDs accepted and application receipt records same batch", acceptance["acceptedIds"] == IDS and app["acceptedIds"] == IDS and operations["onlyIdentityIds"] == IDS)
    check("Director decision was accepted but unapplied; local independent return audit passed", return_receipt["accepted"] and return_receipt["appliedAtDecision"] is False and local_audit["status"] == "PASS" and local_audit["checksFailed"] == 0)
    check("Authority moved from 735/113 to 739/109 with zero accepted-unapplied", before["authoredCounts"] == {"reviewed": 735, "pending": 113} and after["authoredCounts"] == {"reviewed": 739, "pending": 109} and acceptance["countsAfter"]["acceptedUnapplied"] == 0)
    check("Only the exact four accepted entries changed", set(changed) == set(IDS) and len(operations["operations"]) == 4)
    check("Complete inverse index replay restores the original semantic object", inverse == before and operations["inverse"]["semanticExact"] is True)
    check("Exact before-index backup is bound to application operations", operations["before"]["sha256"] == digest(before_bytes) and operations["before"]["bytes"] == len(before_bytes))
    check("Updated index hash and size match operation log", operations["after"]["sha256"] == digest(index_bytes) and operations["after"]["bytes"] == len(index_bytes))
    check("Standalone procedure count advances 459 to 463", before["representationCounts"]["completeReviewedStandaloneProcedures"] == 459 and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 463)
    check("Catalog remains byte-exact and all pending identities still exist there", digest(catalog_bytes) == "773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b" and all(sid in catalog_rows for sid in pending))
    check("All four native cards and source statuses remain unchanged and runtime disabled", all(after_rows[sid]["sourceStatus"] == before_rows[sid]["sourceStatus"] == "blocked-pending-operational-review" and after_rows[sid]["runtimeSelectionEnabled"] is False and after_rows[sid]["sourceCatalogWholeCardPointer"] == before_rows[sid].get("sourceCatalogWholeCardPointer", before_rows[sid]["wholeCardPointer"]) for sid in IDS) and all(model["spells"][i]["nativeCardAndAccessUnchanged"] == catalog_rows[sid] for i, sid in enumerate(IDS)))
    check("Accepted procedure envelope contains exactly four IDs and runtime selection remains disabled", model["acceptedIds"] == IDS and [r["id"] for r in model["spells"]] == IDS and model["runtimeSelectionEnabled"] is False)
    check("All retained holds and whole-case holds remain", len(model["holdIds"]) == 29 and model["applicationCountSummary"]["wholeCaseHeldBranches"] == 4 and acceptance["retainedHolds"] == 29)
    check("Gzipped casebook decompresses byte-exactly to accepted return member", gzip.decompress((PACKAGE / "CASEBOOK.json.gz").read_bytes()) == (PACKAGE / "DIRECTOR_RETURN/CASEBOOK.json").read_bytes())
    check("Candidate package manifest binds every packaged file except its declared exclusions", all((PACKAGE / row["path"]).is_file() and binding(PACKAGE / row["path"]) == {"bytes": row["bytes"], "sha256": row["sha256"]} for row in manifest["files"]) and manifest["sourceArchive"]["sha256"] == return_receipt["receivedArchive"]["sha256"])
    check("Exact director archive is preserved with expected byte length and SHA-256", return_receipt["receivedArchive"]["bytes"] == 29362298 and return_receipt["receivedArchive"]["sha256"] == "081aa49e33c7df0965428db6a63bbcbf656f226e3f496976a68750fb90330b0e")
    with zipfile.ZipFile(PACKAGE / "DIRECTOR_RETURN_ARCHIVE.zip") as archive:
        zip_good = archive.testzip() is None and len(archive.namelist()) == 85 and archive.read("DIRECTOR_ACCEPTANCE.json") == (PACKAGE / "DIRECTOR_RETURN/DIRECTOR_ACCEPTANCE.json").read_bytes()
    check("Full director archive remains CRC-valid with all 85 original members", zip_good)
    check("Pending audit binds exact 109 live pending IDs", pending_doc["pendingCount"] == 109 and pending_doc["pendingIds"] == pending and pending_doc["indexBinding"]["sha256"] == digest(index_bytes))
    check("Queue binds current authority and first fresh group is rank9-catastrophe10", queue["currentAuthority"]["reviewedApplied"] == 739 and queue["currentAuthority"]["pending"] == 109 and queue["currentPendingGroups"][0]["group"] == "rank9-catastrophe10" and queue["currentPendingGroups"][0]["pendingCount"] == 10)
    check("Handoff binds the current index, catalog, queue, accepted IDs, and pending audit", handoff["currentIndexBinding"]["sha256"] == digest(index_bytes) and handoff["currentCatalogBinding"]["sha256"] == digest(catalog_bytes) and handoff["currentQueueBinding"]["sha256"] == digest((AUD / "CURRENT_SPELL_QUEUE_170.json").read_bytes()) and handoff["appliedThisStep"]["ids"] == IDS and handoff["pendingIdentityAudit"]["pendingCount"] == 109)
    check("No runtime, human-play, balance, cosmology, or release approval was granted", all(model[k] is False for k in ["runtimeSelectionEnabled", "runtimeTestsExecuted", "sourceProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"]))
    check("Closed feats and previously completed spell cohorts remain closed", pending_doc["closed335AndCompletedCohortsReopened"] is False and app["closedCohortsReopened"] is False)
    check("Start page reports current checkpoint and next group", "739 reviewed / 109 pending" in (ROOT / "START_HERE.md").read_text(encoding="utf-8") and "rank9-catastrophe10" in (ROOT / "START_HERE.md").read_text(encoding="utf-8"))

    failures = [row["check"] for row in checks if not row["passed"]]
    report = {
        "id": "REMAINING4-APPLICATION-VALIDATION-170", "status": "PASS" if not failures else "FAIL",
        "checkCount": len(checks), "checksPassed": len(checks) - len(failures), "checksFailed": len(failures),
        "failedChecks": failures, "checks": checks, "acceptedIds": IDS,
        "authority": {"reviewedApplied": 739, "pending": 109, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 463, "scopedInterfaces": 173},
        "index": {"bytes": len(index_bytes), "sha256": digest(index_bytes)},
        "catalog": {"bytes": len(catalog_bytes), "sha256": digest(catalog_bytes)},
        "nextGroup": queue["currentPendingGroups"][0]["group"], "nextPendingCount": queue["currentPendingGroups"][0]["pendingCount"],
    }
    (AUD / "REMAINING4_APPLICATION_VALIDATION_170.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["id", "status", "checkCount", "checksPassed", "checksFailed", "failedChecks", "acceptedIds", "authority", "nextGroup", "nextPendingCount"]}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
