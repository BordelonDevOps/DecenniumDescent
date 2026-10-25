from __future__ import annotations

import copy
import gzip
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from verify_perception5_return156 import IDS, AUDIT, CATALOG, INDEX, ROOT, SOURCE_ARCHIVE

QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_158.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_158.json"
PENDING = AUDIT / "CURRENT125_PENDING_IDENTITY_AUDIT_158.json"

APP = AUDIT / "PERCEPTION5_APPLICATION_158.json"
RECEIPT = AUDIT / "PERCEPTION5_EXACT_ACCEPTANCE_156.json"
DECISION = AUDIT / "GPT_DIRECTOR_DECISION_PERCEPTION5_156.json"
OPERATIONS = AUDIT / "PERCEPTION5_INDEX_OPERATIONS_158.json"
VALIDATION = AUDIT / "PERCEPTION5_APPLICATION_VALIDATION_158.json"
BACKUP = AUDIT / "authored_review_index.before_perception5_158.json"
RETURN_ARCHIVE = AUDIT / "perception5_return156_received/DD_Rank8_Perception5_Director_Return156.zip"
RETURN_DELIVERY = AUDIT / "perception5_return156_received/DIRECTOR_RETURN_DELIVERY.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8perception5_reviewed_156"
MODEL = CANDIDATE / "MODEL.json"
PACKAGE_MANIFEST = CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def verify() -> dict:
    index = read_json(INDEX)
    before_raw = BACKUP.read_bytes()
    before = json.loads(before_raw.decode("utf-8-sig"))
    catalog_raw = CATALOG.read_bytes()
    catalog = read_json(CATALOG)
    app = read_json(APP)
    receipt = read_json(RECEIPT)
    decision = read_json(DECISION)
    ops = read_json(OPERATIONS)
    validation = read_json(VALIDATION)
    queue = read_json(QUEUE)
    handoff = read_json(HANDOFF)
    pending = read_json(PENDING)
    model_raw = MODEL.read_bytes()
    model = json.loads(model_raw.decode("utf-8-sig"))
    package_manifest_raw = PACKAGE_MANIFEST.read_bytes()
    package_manifest = json.loads(package_manifest_raw.decode("utf-8-sig"))

    assert app["status"] == "APPLIED_FIVE_AUTHORED_PROCEDURES_WITH_RETAINED_HOLDS"
    assert app["acceptedIds"] == receipt["acceptedIds"] == decision["acceptedIds"] == IDS
    assert receipt["directorDecision"]["accepted"] is True
    assert receipt["directorDecision"]["appliedAtDecision"] is False
    assert receipt["countsBefore"] == {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0}
    assert receipt["countsAfter"] == {"reviewed": 723, "pending": 125, "acceptedUnapplied": 0}
    assert app["counts"] == {"before": receipt["countsBefore"], "after": receipt["countsAfter"]}
    assert app["completeReviewedStandaloneProcedures"] == {"before": 442, "after": 447}
    assert app["catalogChanged"] is False and app["runtimeSelectionEnabled"] is False
    assert app["closedCohortsReopened"] is False

    assert index["authoredCounts"] == {"reviewed": 723, "pending": 125}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 447
    before_entries = {row["id"]: row for row in before["entries"]}
    after_entries = {row["id"]: row for row in index["entries"]}
    assert set(before_entries) == set(after_entries)
    changed = {sid for sid in before_entries if before_entries[sid] != after_entries[sid]}
    assert changed == set(IDS)
    for sid in IDS:
        assert before_entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert after_entries[sid]["authoredStatus"] == "reviewed-authored-operational-playtest"
        assert after_entries[sid]["reviewId"] == app["id"]
        assert after_entries[sid]["runtimeSelectionEnabled"] is False
    assert ops["onlyIdentityIds"] == IDS
    assert [op["identity"] for op in ops["operations"]] == IDS
    assert ops["before"]["bytes"] == len(before_raw) and ops["before"]["sha256"] == sha(before_raw)
    assert ops["after"]["bytes"] == len(INDEX.read_bytes()) and ops["after"]["sha256"] == sha(INDEX.read_bytes())
    rollback = copy.deepcopy(index)
    for operation in ops["operations"]:
        assert operation["op"] == "replace-entry"
        assert rollback["entries"][operation["index"]] == operation["after"]
        rollback["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    rollback["additionalStandaloneEnvelopes"] = rollback["additionalStandaloneEnvelopes"][:-1]
    rollback["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    rollback["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert rollback == before
    assert ops["inverse"]["semanticExact"] is True

    pending_ids = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(pending_ids) == 125 and set(pending["pendingIds"]) == pending_ids
    assert pending["pendingCount"] == 125 and pending["acceptedUnapplied"] == 0
    assert pending["indexBinding"]["sha256"] == sha(INDEX.read_bytes())
    assert pending["catalogBinding"]["sha256"] == sha(catalog_raw)
    assert queue["currentAuthority"]["reviewedApplied"] == 723 and queue["currentAuthority"]["pending"] == 125
    assert queue["currentAuthority"]["acceptedUnapplied"] == 0
    assert sum(row["pendingCount"] for row in queue["currentPendingGroups"]) == 125
    assert queue["currentPendingGroups"][0]["group"] == "rank8-environment3"
    assert queue["currentPendingGroups"][0]["pendingCount"] == 3
    assert queue["currentPendingGroups"][0]["freshPacketRequiredForCurrentAuthority"] is True
    assert handoff["currentAuthority"] == queue["currentAuthority"]
    assert handoff["currentIndexBinding"]["sha256"] == sha(INDEX.read_bytes())
    assert handoff["currentCatalogBinding"]["sha256"] == sha(catalog_raw)
    assert handoff["currentQueueBinding"]["sha256"] == sha(QUEUE.read_bytes())
    assert handoff["nextGroup"] == "rank8-environment3"

    assert receipt["directorReturn"]["sha256"] == sha(RETURN_ARCHIVE.read_bytes())
    assert receipt["directorReturnDelivery"]["sha256"] == sha(RETURN_DELIVERY.read_bytes())
    assert decision["acceptedArchive"]["sha256"] == sha(RETURN_ARCHIVE.read_bytes())
    assert app["directorAcceptance"]["sha256"] == sha(RECEIPT.read_bytes())
    assert app["candidateEnvelope"]["sha256"] == sha(model_raw)
    assert app["candidatePackageManifest"]["sha256"] == sha(package_manifest_raw)
    assert CATALOG.read_bytes() == catalog_raw

    assert model["acceptedIds"] == IDS and model["moduleId"] == "rank8perception5-reviewed-156"
    assert model["independentAcceptanceGranted"] is True
    assert model["canonicalApplicationPerformed"] is False
    assert model["runtimeTestsExecuted"] is False and model["humanPlaytested"] is False
    assert model["balanceApproved"] is False and model["cosmologyModified"] is False and model["releaseApproved"] is False
    assert model["archiveMemberCount"] == 98 and model["returnCounts"]["wholeCaseHeld"] == 31
    model_spells = {row["id"]: row for row in model["spells"]}
    assert set(model_spells) == set(IDS)
    catalog_spells = {row["id"]: row for row in catalog["spells"]}
    for position, sid in enumerate(IDS):
        entry = after_entries[sid]
        record = model_spells[sid]
        native = catalog_spells[sid]
        assert record["nativeCardAndAccessUnchanged"] == native
        assert record["directorProcedureRecord"]["completeNativeSourceAndAccess"] == native
        assert entry["procedureFile"] == "../spell_candidates/rank8perception5_reviewed_156/MODEL.json"
        assert entry["procedurePointer"] == f"/spells/{position}/procedure"
        assert entry["procedureTextPointer"] == f"/spells/{position}/procedure"
        assert entry["directorProcedureRecordPointer"] == f"/spells/{position}/directorProcedureRecord"
        assert entry["completeEnvelopeBinding"]["sha256"] == sha(model_raw)
        assert entry["retainedHoldsBinding"]["sha256"] == binding(CANDIDATE / "DIRECTOR_RETURN/HOLDS.json")["sha256"]
        assert entry["sourceStatus"] == "blocked-pending-operational-review"

    assert len(package_manifest["files"]) == len({r["path"] for r in package_manifest["files"]})
    listed = {row["path"]: row for row in package_manifest["files"]}
    actual = {path.relative_to(CANDIDATE).as_posix(): path for path in CANDIDATE.rglob("*") if path.is_file() and path.relative_to(CANDIDATE).as_posix() not in {"MODEL.json", "CANDIDATE_PACKAGE_MANIFEST.json"}}
    assert set(listed) == set(actual)
    for rel, path in actual.items():
        raw = path.read_bytes()
        assert len(raw) == listed[rel]["bytes"] and sha(raw) == listed[rel]["sha256"], rel
    with ZipFile(CANDIDATE / "DIRECTOR_RETURN_ARCHIVE.zip") as archive:
        assert archive.testzip() is None and len(archive.namelist()) == 98
        casebook_raw = archive.read("CASEBOOK.json")
    assert gzip.decompress((CANDIDATE / "CASEBOOK.json.gz").read_bytes()) == casebook_raw
    assert (CANDIDATE / "STANDALONE_PROCEDURES.md").read_bytes() == (CANDIDATE / "DIRECTOR_RETURN/STANDALONE_PROCEDURES.md").read_bytes()
    with ZipFile(SOURCE_ARCHIVE) as source_archive:
        catalog_frozen = source_archive.read("sources/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json")
    assert catalog_frozen == catalog_raw

    assert validation["status"] == "PASS" and validation["checksFailed"] == 0
    assert validation["changedIdentityIds"] == IDS and validation["onlyFivePendingEntriesChanged"] is True
    assert validation["inverseSemanticReplayExact"] is True and validation["backupByteExact"] is True
    assert validation["sourceCatalogBytesUnchanged"] is True and validation["all98ReturnMembersVerified"] is True
    return {
        "id": "PERCEPTION5-APPLICATION158-VERIFICATION",
        "status": "PASS",
        "appliedIds": IDS,
        "authority": queue["currentAuthority"],
        "changedIndexIdentityCount": len(changed),
        "inverseSemanticReplayExact": True,
        "sourceCatalogByteExact": True,
        "candidateManifestFilesVerified": len(listed),
        "returnArchiveMembersVerified": 98,
        "nextGroup": queue["currentPendingGroups"][0]["group"],
        "nextPendingCount": 125,
        "runtimeTests": 0,
        "failures": 0,
    }


if __name__ == "__main__":
    report = verify()
    out = AUDIT / "PERCEPTION5_APPLICATION_VERIFICATION_158.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
