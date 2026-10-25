from __future__ import annotations

import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
IDS = ["summon-greater-water-pet", "summon-archlich-shade", "faction-paragon", "conjure-sky-fortress", "shifting-fortress"]
RECEIVED = AUDIT / "summonstructure5_return153_received"
ARCHIVE = RECEIVED / "DD_Rank8_SummonStructure5_Director_Return153.zip"
DELIVERY = RECEIVED / "DIRECTOR_RETURN_DELIVERY.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
BACKUP = AUDIT / "authored_review_index.before_summon_structure5_153.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8summonstructure5_reviewed_153"
APPLICATION = AUDIT / "SUMMON_STRUCTURE5_APPLICATION_153.json"
RECEIPT = AUDIT / "SUMMON_STRUCTURE5_EXACT_ACCEPTANCE_153.json"
OPERATIONS = AUDIT / "SUMMON_STRUCTURE5_INDEX_OPERATIONS_153.json"
PENDING = AUDIT / "CURRENT130_PENDING_IDENTITY_AUDIT_155.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_155.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_155.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def binding_matches(path: Path, binding: dict) -> bool:
    raw = path.read_bytes()
    return len(raw) == binding["bytes"] and sha(raw) == binding["sha256"]


def verify() -> dict:
    before_bytes = BACKUP.read_bytes()
    before = json.loads(before_bytes.decode("utf-8-sig"))
    after_bytes = INDEX.read_bytes()
    after = json.loads(after_bytes.decode("utf-8-sig"))
    catalog_bytes = CATALOG.read_bytes()
    app = read(APPLICATION)
    receipt = read(RECEIPT)
    ops = read(OPERATIONS)
    pending = read(PENDING)
    queue = read(QUEUE)
    handoff = read(HANDOFF)
    independent = read(AUDIT / "SUMMONSTRUCTURE5_RETURN153_INDEPENDENT_VERIFICATION.json")
    assert independent["status"] == "PASS" and independent["failures"] == 0
    assert app["acceptedIds"] == receipt["acceptedIds"] == ops["onlyIdentityIds"] == IDS
    assert app["counts"] == {"before": {"reviewed": 713, "pending": 135, "acceptedUnapplied": 0}, "after": {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0}}
    assert receipt["countsAfter"] == {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0}
    assert after["authoredCounts"] == {"reviewed": 718, "pending": 130}
    assert after["representationCounts"]["completeReviewedStandaloneProcedures"] == 442
    assert len(ops["operations"]) == 5 and all(row["identity"] in IDS for row in ops["operations"])
    touched = {row["id"] for row in before["entries"] if next(n for n in after["entries"] if n["id"] == row["id"]) != row}
    assert touched == set(IDS)
    reverted = copy.deepcopy(after)
    for operation in ops["operations"]:
        reverted["entries"][operation["index"]] = copy.deepcopy(operation["before"])
    reverted["additionalStandaloneEnvelopes"] = reverted["additionalStandaloneEnvelopes"][:-1]
    reverted["authoredCounts"] = copy.deepcopy(before["authoredCounts"])
    reverted["representationCounts"] = copy.deepcopy(before["representationCounts"])
    assert reverted == before
    assert ops["after"]["bytes"] == len(after_bytes) and ops["after"]["sha256"] == sha(after_bytes)
    assert pending["pendingCount"] == 130 and pending["acceptedUnapplied"] == 0
    pending_ids = {row["id"] for row in after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert pending_ids == set(pending["pendingIds"]) and len(pending_ids) == 130
    assert queue["currentAuthority"]["reviewedApplied"] == 718 and queue["currentAuthority"]["pending"] == 130
    assert queue["currentAuthority"]["acceptedUnapplied"] == 0 and queue["nextGroup"] == "rank8-perception5"
    assert queue["currentPendingGroups"][0]["pendingIds"] == ["mass-hallucination", "illusory-dragon", "phantom-execution", "antipathy-sympathy", "glibness"]
    assert handoff["currentAuthority"]["reviewedApplied"] == 718 and handoff["currentAuthority"]["pending"] == 130
    assert handoff["currentAuthority"]["acceptedUnapplied"] == 0 and handoff["nextGroup"] == "rank8-perception5"
    assert handoff["currentIndexBinding"]["sha256"] == sha(after_bytes)
    assert handoff["currentCatalogBinding"]["sha256"] == sha(catalog_bytes)
    assert handoff["appliedThisStep"]["ids"] == IDS
    assert sha(catalog_bytes) == "773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b"
    assert binding_matches(ARCHIVE, app["directorReturn"])
    assert binding_matches(DELIVERY, app["directorReturnDelivery"])
    assert binding_matches(CANDIDATE / "MODEL.json", app["candidateEnvelope"])
    assert receipt["decision"] == "ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY"
    assert receipt["runtimeSelectionEnabled"] is False and receipt["canonicalApplicationPerformed"] is False
    assert receipt["runtimeTestsExecuted"] is False and receipt["humanPlaytested"] is False
    assert receipt["balanceApproved"] is False and receipt["cosmologyModified"] is False and receipt["releaseApproved"] is False

    model = read(CANDIDATE / "MODEL.json")
    package_manifest = read(CANDIDATE / "CANDIDATE_PACKAGE_MANIFEST.json")
    assert model["acceptedIds"] == IDS and model["independentAcceptanceGranted"] is True
    assert model["canonicalApplicationPerformed"] is False and model["runtimeTestsExecuted"] is False
    for row in package_manifest["files"]:
        path = CANDIDATE / Path(row["path"])
        raw = path.read_bytes()
        assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
    with gzip.open(CANDIDATE / "CASEBOOK.json.gz", "rb") as source:
        casebook_raw = source.read()
    assert len(casebook_raw) == model["casebookSourceArchiveMemberBinding"]["bytes"]
    assert sha(casebook_raw) == model["casebookSourceArchiveMemberBinding"]["sha256"]
    assert CATALOG.read_bytes() == catalog_bytes
    return {
        "id": "SUMMON-STRUCTURE5-APPLICATION153-POST-APPLY-VERIFICATION",
        "status": "PASS",
        "changedIdentityIds": IDS,
        "indexBeforeSha256": sha(before_bytes),
        "indexAfterSha256": sha(after_bytes),
        "catalogSha256Unchanged": sha(catalog_bytes),
        "authority": {"reviewedApplied": 718, "pending": 130, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 442},
        "onlyExactAcceptedEntriesChanged": True,
        "inverseReplayExact": True,
        "candidatePackageBindingsVerified": len(package_manifest["files"]),
        "casebookDecompressionHashVerified": True,
        "nextGroup": queue["nextGroup"],
        "runtimeTests": 0,
        "failures": 0,
    }


if __name__ == "__main__":
    result = verify()
    target = AUDIT / "SUMMON_STRUCTURE5_POST_APPLICATION_VERIFICATION_153.json"
    target.write_bytes((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
