from __future__ import annotations

import copy
import gzip
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
IDS = ["absolute-silence", "control-weather", "earthquake"]
AUTHORITY = {"reviewedApplied": 726, "pending": 122, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 450, "scopedInterfaces": 173}
RETURN = AUDIT / "environment3_return159_received/DD_Rank8_Environment3_Director_Return159.zip"
PACKAGE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8environment3_reviewed_159"
FRESH_PACKET = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank8_Information_Time_4_Source_Conference_02.zip"
FRESH_IDS = ["alignment-revelation-mass", "moment-of-prescience", "telepathy", "time-echo"]
REPORT = AUDIT / "ENVIRONMENT3_APPLICATION_VERIFICATION_161.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def verify() -> dict:
    checks = []
    failures = []

    def ck(label: str, value: bool):
        row = {"check": label, "passed": bool(value)}
        checks.append(row)
        if not value:
            failures.append(label)

    index_bytes = INDEX.read_bytes()
    before_bytes = (AUDIT / "authored_review_index.before_environment3_161.json").read_bytes()
    index = json.loads(index_bytes.decode("utf-8-sig"))
    before = json.loads(before_bytes.decode("utf-8-sig"))
    catalog_bytes = CATALOG.read_bytes()
    catalog = read(CATALOG)
    app = read(AUDIT / "ENVIRONMENT3_APPLICATION_161.json")
    receipt = read(AUDIT / "ENVIRONMENT3_EXACT_ACCEPTANCE_159.json")
    decision = read(AUDIT / "GPT_DIRECTOR_DECISION_ENVIRONMENT3_159.json")
    ops = read(AUDIT / "ENVIRONMENT3_INDEX_OPERATIONS_161.json")
    validation = read(AUDIT / "ENVIRONMENT3_APPLICATION_VALIDATION_161.json")
    pending = read(AUDIT / "CURRENT122_PENDING_IDENTITY_AUDIT_161.json")
    queue = read(AUDIT / "CURRENT_SPELL_QUEUE_162.json")
    handoff = read(AUDIT / "CURRENT_HANDOFF_162.json")
    stored_return_audit = read(AUDIT / "ENVIRONMENT3_RETURN159_INDEPENDENT_VERIFICATION.json")

    ck("Exact return was independently verified before application", stored_return_audit["status"] == "PASS" and stored_return_audit["failures"] == 0 and stored_return_audit["acceptedIds"] == IDS)
    ck("Director decision and receipt accept only the three exact spell IDs", decision["accepted"] is True and decision["appliedAtDecision"] is False and decision["acceptedIds"] == IDS and receipt["acceptedIds"] == IDS)
    ck("Application references the exact return archive hash", sha(RETURN.read_bytes()) == decision["acceptedArchive"]["sha256"] == receipt["directorReturn"]["sha256"])
    ck("Application status and authority counts advance by exactly three", app["status"] == "APPLIED_THREE_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS" and app["counts"]["before"]["reviewed"] == 723 and app["counts"]["after"]["reviewed"] == 726 and app["counts"]["after"]["pending"] == 122)
    ck("Current index and representation counts match application", index["authoredCounts"] == {"reviewed": 726, "pending": 122} and index["representationCounts"]["completeReviewedStandaloneProcedures"] == 450)
    ck("Current pending audit is exact against live index/catalog", pending["pendingCount"] == 122 and pending["indexBinding"]["sha256"] == sha(index_bytes) and pending["catalogBinding"]["sha256"] == sha(catalog_bytes))
    ck("Queue/handoff both name the exact current authority and next group", queue["currentAuthority"] == handoff["currentAuthority"] == AUTHORITY and queue["nextGroup"] == handoff["nextGroup"] == "rank8-information-time4")
    ck("Handoff binds the current index/catalog and pending audit", handoff["currentIndexBinding"]["sha256"] == sha(index_bytes) and handoff["currentCatalogBinding"]["sha256"] == sha(catalog_bytes) and handoff["pendingIdentityAudit"]["sha256"] == sha((AUDIT / pending["id"].replace("CURRENT122-PENDING-IDENTITY-AUDIT-161", "CURRENT122_PENDING_IDENTITY_AUDIT_161.json")).read_bytes()))

    index_rows = {row["id"]: row for row in index["entries"]}
    before_rows = {row["id"]: row for row in before["entries"]}
    catalog_rows = {row["id"]: row for row in catalog["spells"]}
    changed_ids = sorted(sid for sid in index_rows if index_rows[sid] != before_rows[sid])
    ck("Only the exact accepted identities changed in the authored index", changed_ids == sorted(IDS) and ops["onlyIdentityIds"] == IDS)
    ck("All accepted identities were pending before and are reviewed-authored after", all(before_rows[sid]["authoredStatus"] == "pending-authored-procedure" and index_rows[sid]["authoredStatus"] == "reviewed-authored-operational-playtest" for sid in IDS))
    ck("Native source catalog rows and access remain byte-unchanged and exact", all(index_rows[sid]["sourceStatus"] == "blocked-pending-operational-review" and index_rows[sid]["runtimeSelectionEnabled"] is False and catalog_rows[sid]["status"] == "blocked-pending-operational-review" for sid in IDS))
    ck("Pending set has 122 catalog-backed identities", len(pending["pendingIds"]) == len(set(pending["pendingIds"])) == 122 and all(sid in catalog_rows for sid in pending["pendingIds"]))

    after_from_ops = copy.deepcopy(before)
    ck("Three recorded index operations are exact before/after snapshots", len(ops["operations"]) == 3 and {row["identity"] for row in ops["operations"]} == set(IDS))
    for row in ops["operations"]:
        ck("Operation prior row matches byte-bound prior index " + row["identity"], row["before"] == before_rows[row["identity"]])
        after_from_ops["entries"][row["index"]] = copy.deepcopy(row["after"])
    after_from_ops["additionalStandaloneEnvelopes"] = copy.deepcopy(index["additionalStandaloneEnvelopes"])
    after_from_ops["authoredCounts"] = copy.deepcopy(index["authoredCounts"])
    after_from_ops["representationCounts"] = copy.deepcopy(index["representationCounts"])
    ck("Index operation forward replay yields exact current index", after_from_ops == index)
    inverse = copy.deepcopy(index)
    for row in ops["operations"]:
        inverse["entries"][row["index"]] = copy.deepcopy(row["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    ck("Recorded inverse replay restores prior index exactly", inverse == before)
    ck("Prior index backup is exact original byte sequence", sha(before_bytes) == ops["before"]["sha256"] and len(before_bytes) == ops["before"]["bytes"])
    ck("Native catalog bytes did not change", validation["sourceCatalogBytesUnchanged"] is True and validation["sourceCatalogBytesUnchanged"])

    with zipfile.ZipFile(RETURN) as z:
        member_names = z.namelist()
        ck("Director return archive remains 65-member CRC-valid package", len(member_names) == 65 and len(set(member_names)) == 65 and z.testzip() is None)
        source_model = json.loads(z.read("MODEL.json"))
        return_holds = json.loads(z.read("HOLDS.json"))
        casebook_bytes = z.read("CASEBOOK.json")
        casebook = json.loads(casebook_bytes)
        ck("Return contains exact accepted procedures and 15 retained holds", list(source_model["spells"]) == IDS and len(return_holds) == 15 and all(h["retained"] for h in return_holds))
        ck("All 18 held branches and no actual campaign successes remain held", sum(case["status"] == "held-dependent-case" for case in casebook["cases"]) == 18 and all(case["actualCampaignSuccess"] is False for case in casebook["cases"]))
        ck("All accepted native source/access rows equal the live catalog", all(source_model["spells"][sid]["completeNativeSourceAndAccess"] == catalog_rows[sid] for sid in IDS))

    package_manifest = read(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json")
    package_rows = {row["path"]: row for row in package_manifest["files"]}
    package_ok = True
    for rel, row in package_rows.items():
        raw = (PACKAGE / Path(*Path(rel).parts)).read_bytes()
        package_ok = package_ok and len(raw) == row["bytes"] and sha(raw) == row["sha256"]
    candidate = read(PACKAGE / "MODEL.json")
    ck("Candidate package manifest binds every packaged source/evidence file", package_ok and len(package_rows) == len(package_manifest["files"]))
    ck("Normalized candidate preserves exact full director procedure records", candidate["acceptedIds"] == IDS and [row["id"] for row in candidate["spells"]] == IDS and all(row["directorProcedureRecord"] == source_model["spells"][row["id"]] for row in candidate["spells"]))
    ck("Casebook compression round-trips byte-exactly", gzip.decompress((PACKAGE / "CASEBOOK.json.gz").read_bytes()) == casebook_bytes)
    ck("No runtime, human-play, balance, cosmology or release approval was added", all(candidate[key] is False for key in ["runtimeSelectionEnabled", "runtimeTestsExecuted", "sourceProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyModified", "releaseApproved"]))

    with zipfile.ZipFile(FRESH_PACKET) as z:
        packet_names = z.namelist()
        packet_manifest = json.loads(z.read("MANIFEST.json"))
        packet_update = json.loads(z.read("CURRENT_AUTHORITY_UPDATE.json"))
        packet_index = z.read("CURRENT_AUTHORITY/authored_review_index.json")
        packet_catalog = z.read("CURRENT_AUTHORITY/catalog.json")
        packet_queue = json.loads(z.read("CURRENT_AUTHORITY/CURRENT_SPELL_QUEUE_161.json"))
        ck("Fresh next packet has 67 unique CRC-valid members and hash-bound manifest", len(packet_names) == 67 and len(set(packet_names)) == 67 and z.testzip() is None and packet_manifest["memberCount"] == 67)
        packets_ok = all(len(z.read(row["path"])) == row["bytes"] and sha(z.read(row["path"])) == row["sha256"] for row in packet_manifest["members"])
        ck("All next packet manifest member hashes verify", packets_ok)
        ck("Next packet binds current 726/122 index, catalog, queue and exact four pending identities", packet_update["currentAuthority"] == AUTHORITY and packet_index == index_bytes and packet_catalog == catalog_bytes and packet_queue["currentAuthority"] == AUTHORITY and [row["spellId"] for row in packet_update["records"]] == FRESH_IDS and all(index_rows[sid]["authoredStatus"] == "pending-authored-procedure" for sid in FRESH_IDS))
        nested = z.read("BASE_PACKET/DD_Rank8_Information_Time_4_Source_Conference_01.zip")
        ck("Historical packet01 nested archive exact hash matches fresh-context binding", sha(nested) == packet_update["previousConference"]["archive"]["sha256"])
        request_lower = z.read("DIRECTOR_REQUEST.txt").decode("utf-8").lower()
        ck("Director request excludes just-applied identities and closed feat cohorts", "do not revisit them" in request_lower and "feat335" in request_lower and all(name.lower().encode() in request_lower.encode() for name in ["Alignment Revelation Mass", "Moment of Prescience", "Telepathy", "Time Echo"]) and packet_update["excludedAlreadyAppliedIds"] == ["absolute-silence", "control-weather", "earthquake"])

    result = {"id": "ENVIRONMENT3-APPLICATION-VERIFICATION-161", "status": "PASS" if not failures else "FAIL",
              "checkCount": len(checks), "failures": len(failures), "failedChecks": failures, "checks": checks,
              "acceptedIds": IDS, "authority": AUTHORITY, "nextGroup": "rank8-information-time4",
              "freshPacketArchive": {"bytes": FRESH_PACKET.stat().st_size, "sha256": sha(FRESH_PACKET.read_bytes())}}
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    result = verify()
    print(json.dumps({k: result[k] for k in ["id", "status", "checkCount", "failures", "failedChecks", "acceptedIds", "authority", "nextGroup", "freshPacketArchive"]}, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
