from __future__ import annotations

import hashlib
import json
import os
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "DD_Rank8_Information_Time_4_Director_Return162.zip"
CONFERENCE = ROOT / "docs/audit/2026-10-08/full-game/DD_Rank8_Information_Time_4_Source_Conference_03.zip"
EXPECTED_ARCHIVE_BYTES = 22_993_185
EXPECTED_ARCHIVE_SHA256 = "7f3cf81d8c36ea63d7420d462b532699300c6c5304301224bf78845a7c0a3cd8"
EXPECTED_MEMBER_MANIFEST_BYTES = 24_562
EXPECTED_MEMBER_MANIFEST_SHA256 = "e91c04fec297c26eb39e779cd228c20fd140160fe0c6d27bf121a65e5eb34069"
EXPECTED_CONFERENCE_SHA256 = "bb09971e7a3a83ab85e360b6669d182646a11df607efc11d3904be34207fec50"
EXPECTED_IDS = {
    "alignment-revelation-mass",
    "moment-of-prescience",
    "telepathy",
    "time-echo",
}
EXPECTED_PENDING = 122
EXPECTED_REVIEWED = 726
PACKET_AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129/RANK8_INFORMATION_TIME4_PACKET163_VERIFICATION.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_member(zf: zipfile.ZipFile, name: str):
    return json.loads(zf.read(name).decode("utf-8-sig"))


assert ARCHIVE.is_file()
archive_bytes = ARCHIVE.read_bytes()
assert len(archive_bytes) == EXPECTED_ARCHIVE_BYTES
assert digest(archive_bytes) == EXPECTED_ARCHIVE_SHA256
assert CONFERENCE.is_file()
packet_audit = json.loads(PACKET_AUDIT.read_text(encoding="utf-8-sig"))
assert packet_audit["status"] == "PASS" and packet_audit["checksPassed"] == 13 and packet_audit["checksFailed"] == 0

with zipfile.ZipFile(ARCHIVE) as zf:
    infos = zf.infolist()
    names = [i.filename for i in infos]
    assert zf.testzip() is None
    assert len(names) == 96 and len(set(names)) == 96
    for name in names:
        path = PurePosixPath(name)
        assert not path.is_absolute() and ".." not in path.parts and "\\" not in name, name
        assert name and not name.startswith("/")

    manifest_raw = zf.read("MEMBER_MANIFEST.json")
    assert len(manifest_raw) == EXPECTED_MEMBER_MANIFEST_BYTES
    assert digest(manifest_raw) == EXPECTED_MEMBER_MANIFEST_SHA256
    manifest = json.loads(manifest_raw.decode("utf-8-sig"))
    allowlist = manifest["allowlist"]
    assert manifest["memberCountIncludingManifest"] == 96
    assert len(allowlist) == 96 and len(set(allowlist)) == 96
    assert set(allowlist) == set(names)
    entries = {item["path"]: item for item in manifest["members"]}
    assert set(entries) == set(names) - {"MEMBER_MANIFEST.json"}
    for name, item in entries.items():
        raw = zf.read(name)
        assert len(raw) == item["bytes"], name
        assert digest(raw) == item["sha256"], name
        assert f"{zipfile.crc32(raw) & 0xffffffff:08x}" == item["crc32"].lower(), name

    decision = json_member(zf, "DIRECTOR_DECISION.json")
    validation = json_member(zf, "VALIDATION.json")
    semantic = json_member(zf, "SEMANTIC_FAILURE_CHECK.json")
    questions = json_member(zf, "QUESTION_DISPOSITIONS.json")
    original_questions = json_member(zf, "ORIGINAL_QUESTION_DISPOSITIONS.json")
    future = json_member(zf, "FUTURE_OBLIGATION_DISPOSITIONS.json")
    original_sources = json_member(zf, "ORIGINAL_SOURCE_RECORDS.json")
    procedures = [json_member(zf, f"procedures/{sid}.json") for sid in sorted(EXPECTED_IDS)]
    casebook = json_member(zf, "CASEBOOK.json")
    case_dispositions = json_member(zf, "CASE_DISPOSITIONS.json")
    holds = json_member(zf, "HOLDS.json")
    proposal_operations = json_member(zf, "PROPOSAL_OPERATIONS.json")
    source_verification = json_member(zf, "evidence/SOURCE_VERIFICATION.json")
    provenance = json_member(zf, "evidence/PROVENANCE_SUPERSESSION.json")

    assert decision["accepted"] is True and decision["applied"] is False
    assert set(decision["acceptedIds"]) == EXPECTED_IDS
    assert set(decision["newExactAcceptedUnappliedIds"]) == EXPECTED_IDS
    assert decision["remainingAcceptanceBlockers"] == []
    assert decision["controllingConference"] == "03" and decision["packet02Superseded"] is True
    assert decision["inputAuthority"]["reviewedApplied"] == EXPECTED_REVIEWED
    assert decision["inputAuthority"]["pending"] == EXPECTED_PENDING
    assert decision["inputAuthority"]["acceptedUnapplied"] == 0
    assert decision["canonicalFilesEdited"] is False and decision["applicationPerformed"] is False
    assert all(value is False for value in decision["qualifications"].values())
    assert decision["counts"] == validation["counts"]
    assert decision["counts"]["failedChecks"] == 0
    assert validation["passed"] is True and validation["remainingBlockers"] == []
    assert validation["counts"]["passedChecks"] == validation["counts"]["validationChecks"] == 14_095
    assert semantic["topicCount"] == 16 and semantic["remainingBlockers"] == []
    assert len(semantic["topics"]) == 16 and all(t["remainingBlocker"] is False for t in semantic["topics"])
    assert len(questions) == 17 and len(original_questions) == 4 and len(future) == 7
    assert len(procedures) == 4 and {p.get("id") for p in procedures} == EXPECTED_IDS
    assert isinstance(case_dispositions, list) and len(case_dispositions) == 56
    assert isinstance(holds, list) and len(holds) == 16
    assert len(decision["heldWholeCaseIds"]) == 20
    assert all(q["decisionSelected"] is True and q["answer"] and q["resolutionStatus"] for q in questions)
    assert all(q["originalQuestionUnchanged"] and q["answerUnchanged"] for q in original_questions)
    assert all(o["originalObligationUnchanged"] and o["status"] for o in future)
    assert set(decision["retainedHoldIds"]) == {h["id"] for h in holds} and all(h["retained"] is True for h in holds)
    assert {c["id"] for c in casebook} == {c["id"] for c in case_dispositions}
    assert sum(len(c["events"]) for c in casebook) == 246
    assert sum(len(e["forward"]) + len(e["inverse"]) for c in casebook for e in c["events"]) == 984
    held_cases = {c["id"] for c in casebook if c["status"] == "whole-dependent-branch-held"}
    assert held_cases == set(decision["heldWholeCaseIds"])
    assert all(c["actualCampaignExecution"] is False for c in casebook)
    assert len(proposal_operations) == 4 and {x["id"].removeprefix("IT162-PROPOSAL-") for x in proposal_operations} == EXPECTED_IDS
    assert source_verification["archive"]["sha256"] == EXPECTED_CONFERENCE_SHA256
    assert source_verification["archive"]["members"] == 68 and source_verification["archive"]["CRCVerified"] is True
    assert source_verification["baseSourceBindingsVerified"] is True and source_verification["provenanceBlockers"] == []
    assert all(b["verified"] is True for b in source_verification["outerMemberBindings"])
    assert len(source_verification["outerMemberBindings"]) == 67
    assert provenance["currentPacket"] == "Conference03" and provenance["packet02Superseded"] is True
    assert all(m["nestedMemberByteExact"] is True for m in provenance["nestedMemberVerification"])
    assert decision["sourceArchive"]["bytes"] == CONFERENCE.stat().st_size == 20_242_102
    assert decision["sourceArchive"]["sha256"] == digest(CONFERENCE.read_bytes()) == "bb09971e7a3a83ab85e360b6669d182646a11df607efc11d3904be34207fec50"
    assert zf.read("inputs/DD_Rank8_Information_Time_4_Source_Conference_03.zip") == CONFERENCE.read_bytes()

    catalog_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
    index_path = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    index = json.loads(index_path.read_text(encoding="utf-8-sig"))
    catalog_rows = {x["id"]: x for x in catalog["spells"]}
    index_rows = {x["id"]: x for x in index["entries"]}
    source_rows = {x["spellId"]: x for x in original_sources["sourceRecordsUnchanged"]}
    assert set(source_rows) == EXPECTED_IDS
    assert all(source_rows[sid]["completeCurrentCatalogSourceAndAccess"] == catalog_rows[sid] for sid in EXPECTED_IDS)
    assert all(p["nativeSourceAndAccessUnchanged"] == catalog_rows[p["id"]] for p in procedures)
    assert all(index_rows[sid]["authoredStatus"] == "pending-authored-procedure" for sid in EXPECTED_IDS)
    assert index["authoredCounts"] == {"reviewed": EXPECTED_REVIEWED, "pending": EXPECTED_PENDING}
    assert all(source_rows[sid]["currentIndexEntry"] == index_rows[sid] for sid in EXPECTED_IDS)
    candidate_path = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_information_time_4_source_conference_03.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8-sig"))
    assert [q for q in questions] and len(candidate["inheritedQuestions"]) == 17
    assert [q["originalQuestionUnchanged"] for q in questions] == candidate["inheritedQuestions"]
    assert [o["originalObligationUnchanged"] for o in future] == candidate["futureCaseRequirements"]

    extract_dir = HERE / "extracted"
    if not extract_dir.exists():
        zf.extractall(extract_dir)
    else:
        extracted_files = {p.relative_to(extract_dir).as_posix() for p in extract_dir.rglob("*") if p.is_file()}
        assert extracted_files == set(names)
        assert all((extract_dir / name).read_bytes() == zf.read(name) for name in names)

report = {
    "id": "IT162-LOCAL-RETURN-AUDIT",
    "status": "PASSED_EXACT_ACCEPTED_RETURN_READY_FOR_APPLICATION",
    "archive": {"path": ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(archive_bytes), "sha256": digest(archive_bytes)},
    "memberCount": 96,
    "allMemberHashesAndCRCsVerified": True,
    "sourceConference03BytesAndHashMatch": True,
    "sourcePacket163IndependentVerification": {"checks": packet_audit["checksPassed"], "status": packet_audit["status"]},
    "acceptedIds": sorted(EXPECTED_IDS),
    "authority": {"reviewedApplied": EXPECTED_REVIEWED, "pendingBefore": EXPECTED_PENDING, "acceptedUnappliedBefore": 0},
    "procedures": 4,
    "conferenceQuestionDispositions": 17,
    "originalQuestionDispositions": 4,
    "futureObligations": 7,
    "caseDispositions": 56,
    "retainedHoldCategories": 16,
    "wholeCaseHeld": 20,
    "directorFailureChecks": 14095,
    "directorSemanticTopics": 16,
    "independentAudit": "Passed outer bytes/hash, ZIP CRC, safe unique exact-allowlist members, each embedded member size/SHA256/CRC, director acceptance and authority fields, exact accepted identity scope, source-card and index bindings, all question/obligation/case/hold counts, case event forward/inverse totals, retained non-runtime qualifications, and byte-exact Conference03 source archive binding.",
    "extractedTo": extract_dir.relative_to(ROOT).as_posix(),
}
(HERE / "INFORMATION_TIME4_RETURN162_LOCAL_AUDIT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
