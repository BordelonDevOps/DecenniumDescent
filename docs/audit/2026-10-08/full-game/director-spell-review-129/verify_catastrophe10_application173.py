from __future__ import annotations

import copy
import gzip
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
RECV = AUDIT / "rank9_catastrophe10_return172_received"
RETURN = RECV / "DD_Rank9_Catastrophe10_Director_Return172.zip"
DELIVERY = RECV / "DD_Rank9_Catastrophe10_Director_Return172_DELIVERY.json"
RETURN_AUDIT = AUDIT / "RANK9_CATASTROPHE10_RETURN172_INDEPENDENT_AUDIT.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_CATASTROPHE10_172.json"
ACCEPTANCE = AUDIT / "CATASTROPHE10_EXACT_ACCEPTANCE_172.json"
APPLICATION = AUDIT / "CATASTROPHE10_APPLICATION_173.json"
OPERATIONS = AUDIT / "CATASTROPHE10_INDEX_OPERATIONS_173.json"
RECEIPT = AUDIT / "RANK9_CATASTROPHE10_GPT_RETURN_172.json"
PENDING = AUDIT / "CURRENT99_PENDING_IDENTITY_AUDIT_173.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_173.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_173.json"
VALIDATION = AUDIT / "CATASTROPHE10_APPLICATION_VALIDATION_173.json"
BACKUP = AUDIT / "authored_review_index.before_catastrophe10_173.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9catastrophe10_reviewed_172"
PACKET = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank9_Catastrophe_10_Source_Conference_02.zip"
IDS = ["cataclysmic-conjuration", "elemental-apocalypse", "planar-overload", "armageddon", "cataclysm", "arcane-apocalypse", "meteor-swarm", "starfire-core", "ragnarok", "final-spark"]
checks: list[dict] = []
failures: list[str] = []


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check(name: str, passed: bool, details=None):
    checks.append({"check": name, "passed": bool(passed), **({"details": details} if details is not None else {})})
    if not passed:
        failures.append(name)


def bind(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def main() -> int:
    before_bytes = BACKUP.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    after_bytes = INDEX.read_bytes()
    after = json.loads(after_bytes.decode("utf-8-sig"))
    catalog_bytes = CATALOG.read_bytes()
    audit = read(RETURN_AUDIT)
    receipt = read(RECEIPT)
    decision = read(DECISION)
    acceptance = read(ACCEPTANCE)
    application = read(APPLICATION)
    operations = read(OPERATIONS)
    pending = read(PENDING)
    queue = read(QUEUE)
    handoff = read(HANDOFF)
    delivery = read(DELIVERY)

    check("Return audit passed independently before application", audit["status"] == "PASS" and audit["checksPassed"] == 40 and audit["checksFailed"] == 0 and audit["acceptedIds"] == IDS)
    check("Director decision, acceptance, receipt, and application agree on exactly ten IDs", decision["accepted"] is True and decision["appliedAtDecision"] is False and decision["acceptedIds"] == IDS and acceptance["acceptedIds"] == IDS and receipt["acceptedIds"] == IDS and receipt["appliedSeparately"] is True and application["acceptedIds"] == IDS)
    check("Index backup is byte-exact to the application’s bound 739/109 input", bind(BACKUP) == application["indexBefore"] and before["authoredCounts"] == {"reviewed": 739, "pending": 109})
    check("Live index reflects exactly 749 reviewed and 99 pending", after["authoredCounts"] == {"reviewed": 749, "pending": 99} and after["representationCounts"]["completeReviewedStandaloneProcedures"] == 473)
    check("Catalog bytes are unchanged from the director-bound 739/109 snapshot", len(catalog_bytes) == 5085187 and sha(catalog_bytes) == "773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b")

    before_rows = {row["id"]: row for row in before["entries"]}
    after_rows = {row["id"]: row for row in after["entries"]}
    changed_ids = {sid for sid in before_rows if before_rows[sid] != after_rows[sid]}
    check("Only the exact ten accepted entry rows changed", changed_ids == set(IDS), sorted(changed_ids - set(IDS)))
    procedure_model = read(CANDIDATE / "MODEL.json")
    procedure_rows = procedure_model["spells"]
    index_entries_ok = True
    for position, sid in enumerate(IDS):
        row = after_rows[sid]
        record = procedure_rows[position]
        index_entries_ok &= row["authoredStatus"] == "reviewed-authored-operational-playtest"
        index_entries_ok &= row["sourceStatus"] == before_rows[sid]["sourceStatus"] == "blocked-pending-operational-review"
        index_entries_ok &= row["runtimeSelectionEnabled"] is False
        index_entries_ok &= record["id"] == sid and record["directorProcedureRecord"]["id"] == sid
        index_entries_ok &= record["directorProcedureRecord"]["accepted"] is True and record["directorProcedureRecord"]["applied"] is False
        index_entries_ok &= row["procedureFile"] == "../spell_candidates/rank9catastrophe10_reviewed_172/MODEL.json"
        index_entries_ok &= row["procedurePointer"] == f"/spells/{position}/procedure"
        index_entries_ok &= row["completeEnvelopeBinding"]["sha256"] == bind(CANDIDATE / "MODEL.json")["sha256"]
    check("Each applied index entry points to its exact procedure and keeps native source blocked/runtime disabled", index_entries_ok)
    check("The application adds one standalone envelope and no duplicate reviewed identities", len(after["additionalStandaloneEnvelopes"]) == len(before["additionalStandaloneEnvelopes"]) + 1 and after["additionalStandaloneEnvelopes"][-1]["acceptedIds"] == IDS and len(after_rows) == len(before_rows))

    op_rows = operations["operations"]
    inverse = copy.deepcopy(after)
    for op in op_rows:
        inverse["entries"][op["index"]] = copy.deepcopy(op["before"])
    inverse["additionalStandaloneEnvelopes"] = inverse["additionalStandaloneEnvelopes"][:-1]
    inverse["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    inverse["representationCounts"] = copy.deepcopy(before["representationCounts"])
    check("Recorded index operations list only the exact ten identities and reverse semantically to the original", operations["onlyIdentityIds"] == IDS and len(op_rows) == 10 and inverse == before)
    check("Current pending audit is exactly the 99 live pending identities with no accepted-unapplied IDs", pending["pendingCount"] == 99 and len(pending["pendingIds"]) == 99 and set(pending["pendingIds"]) == {sid for sid, row in after_rows.items() if row["authoredStatus"] == "pending-authored-procedure"} and pending["acceptedUnapplied"] == 0 and pending["allPendingExistInSourceCatalog"] is True)
    check("Queue and handoff bind the applied 749/99 authority and identify the next group", queue["currentAuthority"]["reviewedApplied"] == 749 and queue["currentAuthority"]["pending"] == 99 and queue["currentAuthority"]["acceptedUnapplied"] == 0 and queue["nextGroup"] == "rank9-storm-control6" and queue["currentPendingGroups"][0]["group"] == "rank9-storm-control6" and queue["currentPendingGroups"][0]["pendingCount"] == 6 and handoff["currentAuthority"] == queue["currentAuthority"] and handoff["nextGroup"] == queue["nextGroup"])
    check("Queue retains the accepted/applied batch receipt and strips the old submission from the next packet scope", queue["justAppliedBatch"]["ids"] == IDS and queue["directorSubmission"]["appliedIds"] == IDS and queue["currentPendingGroups"][0]["freshPacketRequiredForCurrentAuthority"] is True and queue["currentPendingGroups"][0].get("submission") is None)

    with zipfile.ZipFile(RETURN) as archive:
        returned_members = {name: archive.read(name) for name in archive.namelist()}
    check("Applied candidate retains byte-exact director ZIP, delivery, source packet, and source candidate", (CANDIDATE / "DIRECTOR_RETURN_ARCHIVE.zip").read_bytes() == RETURN.read_bytes() and (CANDIDATE / "DIRECTOR_DELIVERY.json").read_bytes() == DELIVERY.read_bytes() and (CANDIDATE / "SOURCE_CONFERENCE_ARCHIVE.zip").read_bytes() == PACKET.read_bytes() and (CANDIDATE / "SOURCE_CONFERENCE_CANDIDATE.json").read_bytes() == (ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_catastrophe_10_source_conference_02.json").read_bytes())
    check("Compressed casebook replays byte-exactly to accepted 59-case source member", gzip.decompress((CANDIDATE / "CASEBOOK.json.gz").read_bytes()) == returned_members["CASEBOOK.json"] and len(json.loads(returned_members["CASEBOOK.json"])) == 59)
    manifest = read(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json")
    listed = {row["path"]: row for row in manifest["files"]}
    actual = {path.relative_to(CANDIDATE).as_posix(): path for path in CANDIDATE.rglob("*") if path.is_file() and path.relative_to(CANDIDATE).as_posix() not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}}
    package_mismatches = [name for name, path in actual.items() if name not in listed or len(path.read_bytes()) != listed[name]["bytes"] or sha(path.read_bytes()) != listed[name]["sha256"]]
    package_mismatches += [name for name in listed if name not in actual]
    check("Candidate package manifest covers every stored evidence file and matches its bytes", not package_mismatches, package_mismatches[:10])
    check("Candidate model and index envelope preserve static-only/no-approval qualifications", procedure_model["accepted"] is True and procedure_model["applied"] is False and procedure_model["runtimeSelectionEnabled"] is False and all(procedure_model[key] is False for key in ["runtimeTestsExecuted", "sourceProgramsExecuted", "humanPlaytested", "balanceApproved", "cosmologyApproved", "domainClosure", "releaseApproved", "canonicalApplicationPerformed"]) and acceptance["canonicalApplicationPerformed"] is False)
    check("All 45 hold records and 13 whole-case-held traces remain in the applied evidence", len(read(CANDIDATE / "DIRECTOR_RETURN/HOLD_REGISTER.json")) == 45 and sum(case["wholeCaseHeld"] for case in read(CANDIDATE / "DIRECTOR_RETURN/CASEBOOK.json")) == 13 and len(delivery["exactAcceptedIds"]) == 10)
    check("Return receipt, application validation, and handoff point to the same verified batch", receipt["applicationBinding"]["sha256"] == bind(APPLICATION)["sha256"] and receipt["independentAudit"]["checksPassed"] == 40 and application["directorReturn"]["sha256"] == sha(RETURN.read_bytes()) and read(VALIDATION)["acceptedIds"] == IDS and handoff["appliedThisStep"]["ids"] == IDS)
    check("Authored counts and no-regression boundaries are recorded consistently", application["counts"]["after"]["reviewed"] == 749 and application["counts"]["after"]["pending"] == 99 and application["catalogChanged"] is False and application["closed335AndCompletedCohortsReopened"] is False)

    result = {
        "id": "RANK9-CATASTROPHE10-APPLICATION-POSTCHECK-173",
        "status": "PASS" if not failures else "FAIL",
        "checkCount": len(checks),
        "checksPassed": len(checks) - len(failures),
        "checksFailed": len(failures),
        "failedChecks": failures,
        "checks": checks,
        "acceptedIds": IDS,
        "authority": queue["currentAuthority"],
        "pendingCount": pending["pendingCount"],
        "nextGroup": queue["nextGroup"],
        "catalogBinding": bind(CATALOG),
        "indexBinding": bind(INDEX),
    }
    VALIDATION.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in ["id", "status", "checkCount", "checksPassed", "checksFailed", "failedChecks", "acceptedIds", "authority", "pendingCount", "nextGroup"]}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
