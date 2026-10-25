from __future__ import annotations

import hashlib
import json
import zlib
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
IDS = ["mass-hallucination", "illusory-dragon", "phantom-execution", "antipathy-sympathy", "glibness"]
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_perception_5_source_conference_02.json"
ARCHIVE = FULL / "DD_Rank8_Perception_5_Source_Conference_02.zip"
PREPARATION = FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_PREPARATION.json"
CHECK = FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_CHECK.json"
REQUEST = FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_REQUEST.txt"
NOTES = AUDIT / "RANK8PERCEPTION5_NEXT_CONFERENCE_NOTES_156.json"
OUT = FULL / "rank8-perception5-source-conference-02"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_156.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_155.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_156.json"
PENDING = AUDIT / "CURRENT130_PENDING_IDENTITY_AUDIT_155.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def verify() -> dict:
    prep = read(PREPARATION)
    check = read(CHECK)
    candidate = read(CANDIDATE)
    notes = read(NOTES)
    index_raw = INDEX.read_bytes()
    catalog_raw = CATALOG.read_bytes()
    index = json.loads(index_raw.decode("utf-8-sig"))
    catalog = read(CATALOG)
    queue = read(QUEUE)
    handoff = read(HANDOFF)
    pending = read(PENDING)
    archive_raw = ARCHIVE.read_bytes()
    assert prep["status"] == "PREPARED_UNSENT"
    assert prep["sourceAuthority"] == {"reviewedApplied": 718, "pending": 130, "acceptedUnapplied": 0}
    assert len(archive_raw) == prep["archive"]["bytes"] and sha(archive_raw) == prep["archive"]["sha256"]
    assert len(archive_raw) < 100_000_000
    assert len(CANDIDATE.read_bytes()) == prep["candidate"]["bytes"] and sha(CANDIDATE.read_bytes()) == prep["candidate"]["sha256"]
    assert check["status"] == "PASS" and check["failures"] == 0
    assert check["sourceAuthority"] == prep["sourceAuthority"]
    assert check["candidate"]["sha256"] == prep["candidate"]["sha256"]
    assert index["authoredCounts"] == {"reviewed": 718, "pending": 130}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 442
    live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == 130 and set(pending["pendingIds"]) == live_pending
    assert pending["indexBinding"]["sha256"] == sha(index_raw)
    assert pending["catalogBinding"]["sha256"] == sha(catalog_raw)
    assert handoff["currentIndexBinding"]["sha256"] == sha(index_raw)
    assert handoff["currentCatalogBinding"]["sha256"] == sha(catalog_raw)
    assert queue["currentAuthority"]["reviewedApplied"] == 718 and queue["currentAuthority"]["pending"] == 130
    first = queue["currentPendingGroups"][0]
    assert first["group"] == "rank8-perception5" and first["pendingIds"] == IDS
    assert candidate["currentAuthority"]["reviewedApplied"] == 718 and candidate["currentAuthority"]["pending"] == 130
    assert candidate["currentAuthority"]["index"]["sha256"] == sha(index_raw)
    assert candidate["currentAuthority"]["catalog"]["sha256"] == sha(catalog_raw)
    assert candidate["currentAuthority"]["currentQueue"]["sha256"] == sha(QUEUE_BEFORE.read_bytes())
    assert candidate["currentAuthority"]["pendingIdentityAudit"]["sha256"] == sha(PENDING.read_bytes())
    assert candidate["currentAuthority"]["priorHandoff"]["sha256"] == sha(AUDIT.joinpath("CURRENT_HANDOFF_155.json").read_bytes())
    candidate_entries = {row["spellId"]: row for row in candidate["records"]}
    catalog_entries = {row["id"]: row for row in catalog["spells"]}
    for sid in IDS:
        assert candidate_entries[sid]["completeCurrentCatalogSourceAndAccess"] == catalog_entries[sid]
        assert candidate_entries[sid]["currentIndexEntry"] == next(row for row in index["entries"] if row["id"] == sid)
        assert candidate_entries[sid]["currentAuthorityStatus"] == "pending-authored-procedure at current 718/130 authority"
    assert len(candidate["conference02Questions"]) == 23
    assert all(question["decisionSelected"] is False for question in candidate["conference02Questions"])
    assert {question["id"] for question in candidate["conference02Questions"]} == {question["id"] for question in notes["allQuestions"]}
    assert notes["currentAppliedCounts"] == {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0}
    assert candidate["newRuleAdoptions"] == 0 and candidate["runtimeTestsExecuted"] == 0
    assert len(candidate["recentExactAcceptedAppliedComparisons"]) == 5
    for batch in candidate["recentExactAcceptedAppliedComparisons"]:
        assert len(batch["procedures"]) == len(batch["acceptedIds"])
        for procedure in batch["procedures"]:
            assert procedure["spellId"] in batch["acceptedIds"]
            assert procedure["currentIndexEntry"]["authoredStatus"] == "reviewed-authored-operational-playtest"

    with ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        assert archive.testzip() is None and len(names) == len(set(names)) == prep["archiveMemberCount"]
        assert all(name and not PurePosixPath(name).is_absolute() and ".." not in PurePosixPath(name).parts and "\\" not in name for name in names)
        assert archive.read("CANDIDATE.json") == CANDIDATE.read_bytes()
        assert archive.read("REQUEST.txt") == REQUEST.read_bytes()
        assert archive.read("SOURCE_CHECK.json") == CHECK.read_bytes()
        assert archive.read("RANK8PERCEPTION5_NEXT_CONFERENCE_NOTES.json") == NOTES.read_bytes()
        assert len(NOTES.read_bytes()) == prep["notes"]["bytes"] and sha(NOTES.read_bytes()) == prep["notes"]["sha256"]
        assert archive.read("historical/Conference01_ARCHIVE.zip") == (OUT / "historical/Conference01_ARCHIVE.zip").read_bytes()
        source_manifest = json.loads(archive.read("MANIFEST.json"))
        assert source_manifest["candidate"]["sha256"] == sha(CANDIDATE.read_bytes())
        frozen = source_manifest["frozenSources"]
        assert len(frozen) == prep["sourceCount"] == len(candidate["sourceBindings"])
        for row in frozen:
            raw = archive.read("sources/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            live = (ROOT / PurePosixPath(row["path"])).read_bytes()
            assert len(live) == row["bytes"] and sha(live) == row["sha256"]
        historical = json.loads(archive.read("historical/Conference01_CANDIDATE.json"))
        assert historical["countsUnchanged"] == {"reviewed": 525, "pending": 323}
        hist_row = candidate["historicalConference01"]["candidate"]
        historical_bytes = archive.read("historical/Conference01_CANDIDATE.json")
        assert len(historical_bytes) == hist_row["bytes"] and sha(historical_bytes) == hist_row["sha256"]
        assert len(frozen) == 96
        assert not any(row["path"].endswith("DIRECTOR_RETURN_ARCHIVE.zip") for row in frozen)

    # The comparison is about applied procedures and their exact receipts; nested full return ZIPs stay in their own records.
    return {
        "id": "RANK8-PERCEPTION5-SOURCE-CONFERENCE02-INDEPENDENT-VERIFICATION-156",
        "status": "PASS",
        "candidateBytes": len(CANDIDATE.read_bytes()),
        "candidateSha256": sha(CANDIDATE.read_bytes()),
        "archiveBytes": len(archive_raw),
        "archiveSha256": sha(archive_raw),
        "archiveMembers": len(names),
        "currentSourceBindings": len(frozen),
        "questions": 23,
        "exactAppliedComparisonBatches": len(candidate["recentExactAcceptedAppliedComparisons"]),
        "historicalConference01Preserved": True,
        "authority": {"reviewedApplied": 718, "pending": 130, "acceptedUnapplied": 0},
        "canonicalIndexAndCatalogUnchanged": True,
        "failures": 0,
    }


if __name__ == "__main__":
    report = verify()
    target = AUDIT / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_INDEPENDENT_VERIFICATION.json"
    target.write_bytes((json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(report, ensure_ascii=False, indent=2))
