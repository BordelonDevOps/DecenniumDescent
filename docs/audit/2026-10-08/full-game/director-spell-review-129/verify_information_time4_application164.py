from __future__ import annotations

import copy
import gzip
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
PACKAGE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8informationtime4_reviewed_162"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
BEFORE = AUDIT / "authored_review_index.before_information_time4_164.json"
OPS = AUDIT / "INFORMATION_TIME4_INDEX_OPERATIONS_164.json"
APP = AUDIT / "INFORMATION_TIME4_APPLICATION_164.json"
ACCEPTANCE = AUDIT / "INFORMATION_TIME4_EXACT_ACCEPTANCE_162.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_INFORMATION_TIME4_162.json"
RETURN_ZIP = AUDIT / "information-time4_return162_received/DD_Rank8_Information_Time_4_Director_Return162.zip"
PACKET_ZIP = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank8_Information_Time_4_Source_Conference_03.zip"
LOCAL_RETURN_AUDIT = AUDIT / "information-time4_return162_received/INFORMATION_TIME4_RETURN162_LOCAL_AUDIT.json"
PENDING = AUDIT / "CURRENT118_PENDING_IDENTITY_AUDIT_164.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_164.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_164.json"
VALIDATION = AUDIT / "INFORMATION_TIME4_APPLICATION_VALIDATION_164.json"
START = ROOT / "START_HERE.md"
SNAPSHOT = ROOT / "SNAPSHOT_STATUS_2026-10-25_SPELL_REVIEW_164.md"

IDS = ["alignment-revelation-mass", "moment-of-prescience", "telepathy", "time-echo"]
AUTHORITY = {"reviewedApplied": 730, "pending": 118, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 454, "scopedInterfaces": 173}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def pointer(value, pointer: str):
    current = value
    for part in pointer.strip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


checks = []
failures = []


def check(label: str, passed: bool):
    checks.append({"check": label, "passed": bool(passed)})
    if not passed:
        failures.append(label)


index_raw = INDEX.read_bytes()
catalog_raw = CATALOG.read_bytes()
before_raw = BEFORE.read_bytes()
index = json.loads(index_raw.decode("utf-8-sig"))
before = json.loads(before_raw.decode("utf-8-sig"))
catalog = json.loads(catalog_raw.decode("utf-8-sig"))
ops = read(OPS)
app = read(APP)
acceptance = read(ACCEPTANCE)
decision = read(DECISION)
local_return = read(LOCAL_RETURN_AUDIT)
pending = read(PENDING)
queue = read(QUEUE)
handoff = read(HANDOFF)

check("Local exact Return162 audit passed", local_return["status"] == "PASSED_EXACT_ACCEPTED_RETURN_READY_FOR_APPLICATION" and local_return["acceptedIds"] == IDS)
check("Return archive hash and size remain bound", sha(RETURN_ZIP.read_bytes()) == decision["acceptedArchive"]["sha256"] == app["directorReturn"]["sha256"] and RETURN_ZIP.stat().st_size == app["directorReturn"]["bytes"])
check("Director decision accepts only four exact IDs and was unapplied", decision["accepted"] is True and decision["appliedAtDecision"] is False and decision["acceptedIds"] == IDS and decision["remainingBlockingDefects"] == [])
check("Acceptance receipt binds four exact IDs and retains 16 holds", acceptance["acceptedIds"] == IDS and acceptance["directorDecision"]["acceptedIds"] == IDS and acceptance["retainedHolds"] == 16)
check("Application receipt advances exact authority by four", app["status"] == "APPLIED_FOUR_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS" and app["counts"]["before"]["reviewed"] == 726 and app["counts"]["before"]["pending"] == 122 and app["counts"]["after"]["reviewed"] == 730 and app["counts"]["after"]["pending"] == 118 and app["counts"]["after"]["acceptedUnapplied"] == 0)
check("Complete procedure count advances 450 to 454", app["completeReviewedStandaloneProcedures"] == {"before": 450, "after": 454} and index["representationCounts"]["completeReviewedStandaloneProcedures"] == 454)
check("Live authored count is 730 reviewed and 118 pending", index["authoredCounts"] == {"reviewed": 730, "pending": 118})
check("Catalog source/access bytes remain equal to Conference03 current authority", catalog_raw == zipfile.ZipFile(PACKET_ZIP).read("CURRENT_AUTHORITY/catalog.json"))
check("Index before backup matches exact recorded prior hash and bytes", len(before_raw) == ops["before"]["bytes"] and sha(before_raw) == ops["before"]["sha256"])
check("Index after hash and bytes match operation record", len(index_raw) == ops["after"]["bytes"] and sha(index_raw) == ops["after"]["sha256"])

index_rows = {row["id"]: row for row in index["entries"]}
before_rows = {row["id"]: row for row in before["entries"]}
catalog_rows = {row["id"]: row for row in catalog["spells"]}
changed = sorted(sid for sid in index_rows if index_rows[sid] != before_rows[sid])
check("Only the four director-accepted identity entries changed", changed == sorted(IDS) and ops["onlyIdentityIds"] == IDS)
check("Four exact before/after row operations exist", len(ops["operations"]) == 4 and {op["identity"] for op in ops["operations"]} == set(IDS))
for op in ops["operations"]:
    sid = op["identity"]
    check(f"Prior operation row matches backup for {sid}", op["before"] == before_rows[sid])
    check(f"Applied operation row matches live index for {sid}", op["after"] == index_rows[sid])
    check(f"Accepted source remains blocked from runtime for {sid}", index_rows[sid]["sourceStatus"] == "blocked-pending-operational-review" and index_rows[sid]["runtimeSelectionEnabled"] is False and catalog_rows[sid]["status"] == "blocked-pending-operational-review")
    model = read(PACKAGE / "MODEL.json")
    pos = IDS.index(sid)
    check(f"Procedure pointers resolve to accepted native ID for {sid}", pointer(model, index_rows[sid]["wholeCardPointer"])["id"] == sid and pointer(model, index_rows[sid]["procedurePointer"]) == model["spells"][pos]["procedure"])

inverse = copy.deepcopy(index)
for op in ops["operations"]:
    inverse["entries"][op["index"]] = copy.deepcopy(op["before"])
inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
check("Recorded inverse semantic replay restores the complete prior index", inverse == before)
check("Catalog was not altered by application", catalog_raw == zipfile.ZipFile(PACKET_ZIP).read("CURRENT_AUTHORITY/catalog.json"))

package_manifest = read(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json")
manifest_ok = True
for row in package_manifest["files"]:
    path = PACKAGE / Path(*PurePosixPath(row["path"]).parts)
    raw = path.read_bytes()
    manifest_ok = manifest_ok and len(raw) == row["bytes"] and sha(raw) == row["sha256"]
check("Candidate package manifest binds every included file", manifest_ok and len(package_manifest["files"]) > 100)
model = read(PACKAGE / "MODEL.json")
check("Normalized model contains exactly the four accepted IDs", model["acceptedIds"] == IDS and [row["id"] for row in model["spells"]] == IDS)
check("Normalized model preserves each director procedure record", all(model["spells"][IDS.index(sid)]["directorProcedureRecord"] == read(PACKAGE / "DIRECTOR_RETURN" / f"procedures/{sid}.json") for sid in IDS))
check("Each native card/access object is exact current catalog data", all(model["spells"][IDS.index(sid)]["nativeCardAndAccessUnchanged"] == catalog_rows[sid] for sid in IDS))
casebook_raw = (PACKAGE / "DIRECTOR_RETURN/CASEBOOK.json").read_bytes()
check("Compressed casebook round-trips byte-for-byte", gzip.decompress((PACKAGE / "CASEBOOK.json.gz").read_bytes()) == casebook_raw)
check("All sixteen hold rows remain retained", len(read(PACKAGE / "DIRECTOR_RETURN/HOLDS.json")) == 16 and all(h["retained"] is True for h in read(PACKAGE / "DIRECTOR_RETURN/HOLDS.json")))
check("All twenty wholly held cases remain held", len(model["directorReturnDeliveryObservation"]) > 0 and model["returnCounts"]["wholeCaseHeld"] == 20)
check("No runtime, play, balance, cosmology, domain or release approval is added", all(model[k] is False for k in ["runtimeSelectionEnabled", "runtimeTestsExecuted", "sourceProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved", "domainClosure"]))
check("The accepted batch did not reopen feat335 or completed cohorts", app["closedCohortsReopened"] is False and model["directorReturnDeliveryObservation"]["applied"] is False)

pending_ids = set(pending["pendingIds"])
live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
check("Current pending audit is 118 and exactly matches live index", pending["pendingCount"] == 118 and len(pending_ids) == 118 and pending_ids == live_pending and pending["acceptedUnapplied"] == 0)
check("All pending identities remain in the unchanged source catalog", pending["allPendingExistInSourceCatalog"] is True and all(sid in catalog_rows for sid in pending_ids))
check("Queue has exact 730/118 authority and 118 remaining records", queue["currentAuthority"] == AUTHORITY and sum(g["pendingCount"] for g in queue["currentPendingGroups"]) == 118)
check("Rank8 Planar5 is the next fresh packet group", queue["nextGroup"] == "rank8-planar5" and queue["currentPendingGroups"][0]["group"] == "rank8-planar5" and queue["next"]["freshPacketRequiredForCurrentAuthority"] is True)
check("Planar5 has exactly five pending identities", queue["currentPendingGroups"][0]["pendingCount"] == 5 and queue["currentPendingGroups"][0]["pendingIds"] == ["demiplane", "maze", "planar-seal", "seal-of-banishment", "gloom-bind"])
check("Handoff binds live authority, index, catalog, queue and pending audit", handoff["currentAuthority"] == AUTHORITY and handoff["currentIndexBinding"]["sha256"] == sha(index_raw) and handoff["currentCatalogBinding"]["sha256"] == sha(catalog_raw) and handoff["currentQueueBinding"]["sha256"] == sha(QUEUE.read_bytes()) and handoff["pendingIdentityAudit"]["sha256"] == sha(PENDING.read_bytes()))
check("Start and snapshot state the current authority and next group", "730 reviewed / 118 pending / 0 accepted-unapplied" in START.read_text(encoding="utf-8") and "730 reviewed / 118 pending / 0 accepted-unapplied" in SNAPSHOT.read_text(encoding="utf-8") and "rank8-planar5" in START.read_text(encoding="utf-8") and "rank8-planar5" in SNAPSHOT.read_text(encoding="utf-8"))

result = {
    "id": "INFORMATION-TIME4-APPLICATION-VERIFICATION-164",
    "status": "PASS" if not failures else "FAIL",
    "checkCount": len(checks),
    "failures": len(failures),
    "failedChecks": failures,
    "checks": checks,
    "acceptedIds": IDS,
    "authority": AUTHORITY,
    "nextGroup": queue["nextGroup"],
    "index": {"bytes": len(index_raw), "sha256": sha(index_raw)},
    "catalog": {"bytes": len(catalog_raw), "sha256": sha(catalog_raw)},
    "directorReturn": {"bytes": RETURN_ZIP.stat().st_size, "sha256": sha(RETURN_ZIP.read_bytes())},
}
VALIDATION.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: result[k] for k in ["id", "status", "checkCount", "failures", "failedChecks", "acceptedIds", "authority", "nextGroup"]}, ensure_ascii=False, indent=2))
raise SystemExit(0 if result["status"] == "PASS" else 1)
