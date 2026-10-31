from __future__ import annotations

import copy
import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PACKAGE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/matterconversion_reviewed_262"
ID = "matter-conversion"
BLOCKER = "MF210-B02"
checks = []


def check(name: str, condition: bool) -> None:
    checks.append({"check": name, "passed": bool(condition)})


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data),
            "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"}


before_raw = (A / "authored_review_index.before_matterconversion_262.json").read_bytes()
before = json.loads(before_raw)
after_raw = INDEX.read_bytes()
after = read(INDEX)
catalog_raw = CATALOG.read_bytes()
catalog = read(CATALOG)
decision = read(A / "MATTER_CONVERSION_DIRECTOR_DECISION_262.json")
acceptance = read(A / "MATTER_CONVERSION_EXACT_ACCEPTANCE_262.json")
application = read(A / "MATTER_CONVERSION_APPLICATION_262.json")
audit = read(A / "matter_conversion_witnesses_261/MATTER_CONVERSION_INDEPENDENT_AUDIT_261.json")
queue = read(A / "CURRENT_SPELL_QUEUE_262.json")
pending_audit = read(A / "CURRENT34_PENDING_IDENTITY_AUDIT_262.json")
entry_before = next(row for row in before["entries"] if row["id"] == ID)
entry_index = next(i for i, row in enumerate(before["entries"]) if row["id"] == ID)
entry_after = next(row for row in after["entries"] if row["id"] == ID)
pending_before = {row["id"] for row in before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
pending_after = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}

check("director decision is explicit exact ACCEPT", decision["decision"] == "EXACT_ACCEPT" and decision["accepted"] is True)
check("GPT acceptance has applied=false at decision time", decision["appliedAtDecision"] is False)
check("only Matter Conversion accepted and applied", acceptance["acceptedIds"] == [ID] and application["appliedIds"] == [ID])
check("MF210-B02 closed", acceptance["closedBlockerIds"] == [BLOCKER] and application["closedBlockerIds"] == [BLOCKER])
check("Packet261 exact archive binding", decision["packet"]["sha256"] == "9d092e47f2d792ba3d1a0222b50d8b41800dd21b2f941d302d5160672a7fc500" and decision["packet"]["bytes"] == 7_626_583)
check("integrated witness independent audit 60/60", audit["status"] == "PASS" and audit["passedChecks"] == audit["checkCount"] == 60 and audit["failedChecks"] == 0)
check("two integrated cases and 60 forward/inverse operations", audit["counts"]["newIntegratedCases"] == 2 and audit["counts"]["newForwardOperations"] == audit["counts"]["newInverseOperations"] == 60)
check("authority is 814/34/0 and procedures 538", after["authoredCounts"] == {"reviewed": 814, "pending": 34} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 538)
check("accepted entry references the applied envelope", entry_after["authoredStatus"] == "reviewed-authored-operational-playtest" and entry_after["accepted"] and entry_after["applied"] and entry_after["procedureFile"] == "../spell_candidates/matterconversion_reviewed_262/MODEL.json")
check("source catalog selection status remains blocked", entry_after["sourceStatus"] == entry_before["sourceStatus"] == "blocked-pending-operational-review")
check("catalog bytes remain exact", catalog_raw == (ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json").read_bytes() and sha(catalog_raw) == queue["currentCatalogBinding"]["sha256"])
check("pre-existing index catalog bindings are preserved and current queue binds untouched catalog", after["sourceCatalogSha256"] == before["sourceCatalogSha256"] and after["currentSourceCatalogBinding"] == before["currentSourceCatalogBinding"] and queue["currentCatalogBinding"]["sha256"] == sha(catalog_raw) and catalog["spells"][768]["id"] == ID)
check("pending set is exactly prior set minus one accepted spell", pending_after == pending_before - {ID} and len(pending_before) == 35 and len(pending_after) == 34)
check("pending audit hash binds current index", pending_audit["indexBinding"]["sha256"] == sha(after_raw) and set(pending_audit["pendingIds"]) == pending_after)
check("pending audit and queue agree on 34 remaining", pending_audit["pendingCount"] == queue["pendingCount"] == 34)
nonempty_groups = [group for group in queue["currentPendingGroups"] if group["pendingIds"]]
check("remaining pending identities span 16 groups", len(nonempty_groups) == 16 and {sid for group in nonempty_groups for sid in group["pendingIds"]} == pending_after)
check("GPT next priority is Soul Reflection IR207-B02", queue["next"]["identity"] == "soul-reflection" and queue["next"]["blocker"] == "IR207-B02")
check("Soul Reflection director witness requirements preserved", set(queue["next"]["requiredWitnessScope"]) == {"changed-form attached/no-phase recipient lifecycle", "original-target zero/death settlement", "copied concentration ending", "actual original cargo entrusted to the reflection"})
check("runtime selection remains disabled", entry_after["runtimeSelectionEnabled"] is False and read(PACKAGE / "MODEL.json")["runtimeSelectionEnabled"] is False)
check("seven historical kernels remain conditional", len(read(PACKAGE / "RETAINED_QUALIFICATIONS.json")["conditionalKernelIds"]) == 7 and decision["retainedConditionalKernels"] == read(PACKAGE / "RETAINED_QUALIFICATIONS.json")["conditionalKernelIds"])
check("application receipt binding matches index entry", entry_after["authoredApplicationReceipt"] == bind(A / "MATTER_CONVERSION_APPLICATION_262.json"))
check("backup binding matches operation ledger", bind(A / "authored_review_index.before_matterconversion_262.json")["sha256"] == sha(before_raw) and read(A / "MATTER_CONVERSION_INDEX_OPERATIONS_262.json")["inverseSemanticExact"] is True)

# Independently reverse exactly the entry, envelope append, and authored-count changes.
inverse = copy.deepcopy(after)
inverse["entries"][entry_index] = copy.deepcopy(entry_before)
inverse["additionalStandaloneEnvelopes"].pop()
inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
check("inverse restores exact pre-application index", inverse == before)
check("candidate package manifest binds all payload files", all(
    (ROOT / row["path"]).stat().st_size == row["bytes"] and sha((ROOT / row["path"]).read_bytes()) == row["sha256"]
    for row in read(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json")["files"]
))

failed = [row["check"] for row in checks if not row["passed"]]
result = {
    "id": "MATTER-CONVERSION-APPLICATION-INDEPENDENT-VERIFICATION-262",
    "status": "PASS" if not failed else "FAIL",
    "checksPassed": sum(row["passed"] for row in checks),
    "checkCount": len(checks),
    "checksFailed": len(failed),
    "checks": checks,
    "acceptedIds": [ID],
    "appliedIds": [ID],
    "indexAfter": bind(INDEX, after_raw),
    "catalogAfter": bind(CATALOG, catalog_raw),
    "authority": queue["currentAuthority"],
    "remainingPending": {"count": len(pending_after), "groups": len(nonempty_groups), "next": queue["next"]},
}
if failed:
    raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
(A / "MATTER_CONVERSION_APPLICATION_INDEPENDENT_VERIFICATION_262.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
