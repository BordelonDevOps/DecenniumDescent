from pathlib import Path
import hashlib, json, zipfile

G = Path(r"C:\Github\DecenniumDescent")
D = Path(__file__).parent.resolve()
ARCHIVE = G / "docs/audit/2026-10-08/full-game/DD_Ward_7_Source_Conference_01.zip"
DIRECTOR_PACKET = G / "docs/audit/2026-10-08/full-game/DD_Ward7_Director_Conference_128.zip"
DIRECTOR_RECEIPT = G / "docs/audit/2026-10-08/full-game/director-spell-review-128/WARD7_PACKET_128.json"
INDEX = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
sha = lambda b: hashlib.sha256(b).hexdigest()
ward_ids = ["arcane-aegis", "spell-turning", "dimensional-lock", "resonance-fortress", "faction-aegis", "corruption-immunity", "summon-living-armor"]
archive_bytes = ARCHIVE.read_bytes()
with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None
    manifest = json.loads(z.read("MANIFEST.json"))
    candidate = json.loads(z.read("CANDIDATE.json"))
    pref = json.loads(z.read("PREFLIGHT.json"))
    assert len(z.infolist()) == 54 and len(manifest["files"]) == 50
    member_checks = []
    for item in manifest["files"]:
        raw = z.read("sources/" + item["path"])
        assert len(raw) == item["bytes"] and sha(raw) == item["sha256"], item["path"]
        member_checks.append(item["path"])

idx = json.loads(INDEX.read_text(encoding="utf-8-sig"))
catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
current_index = {e["id"]: e for e in idx["entries"]}
current_cards = {s["id"]: s for s in catalog["spells"]}
assert candidate["status"] == "SOURCE_CONFERENCE_PREPARED_UNSENT"
assert [r["spellId"] for r in candidate["records"]] == ward_ids
assert len(candidate["questions"]) == 20
assert pref["failures"] == 0
card_comparisons = {}
index_comparisons = {}
for record in candidate["records"]:
    sid = record["spellId"]
    card_comparisons[sid] = record["completeCurrentCatalogSourceAndAccess"] == current_cards[sid]
    index_comparisons[sid] = record["currentIndexEntry"] == current_index[sid]
assert all(card_comparisons.values()) and all(index_comparisons.values())
assert idx["authoredCounts"] == {"reviewed": 648, "pending": 200}
assert all(current_index[s]["authoredStatus"] == "pending-authored-procedure" for s in ward_ids)
packet_raw = DIRECTOR_PACKET.read_bytes()
packet_receipt = json.loads(DIRECTOR_RECEIPT.read_text(encoding="utf-8-sig"))
assert len(packet_raw) == packet_receipt["archive"]["bytes"] == 58204627
assert sha(packet_raw) == packet_receipt["archive"]["sha256"] == "b2cb6b3f93090bd11f2997f38a22ec2a88e46ca79cf847d4fb19ec4ef3e6a77d"
with zipfile.ZipFile(DIRECTOR_PACKET) as z:
    assert z.testzip() is None and len(z.infolist()) == packet_receipt["members"] == 53
    packet_manifest = json.loads(z.read("MANIFEST.json"))
    question_file = json.loads(z.read("INDEPENDENT_QUESTIONS_128.json"))
    assert len(packet_manifest["files"]) == packet_receipt["bindings"] == 52
    for item in packet_manifest["files"]:
        data = z.read(item["path"])
        assert len(data) == item["bytes"] and sha(data) == item["sha256"], item["path"]
    assert question_file["identities"] == ward_ids
    assert question_file["completeOriginalQuestionsUnchanged"] == candidate["questions"]
    assert len(question_file["completeOriginalQuestionsUnchanged"]) == 20
    assert len(question_file["focusedAdditionalQuestions"]) == 6
    assert len(question_file["allQuestions"]) == packet_receipt["questions"] == 26
    assert [q["id"] for q in question_file["allQuestions"]] == [q["id"] for q in question_file["completeOriginalQuestionsUnchanged"] + question_file["focusedAdditionalQuestions"]]
    assert len(question_file["requiredNewCases"]) == packet_receipt["requiredNewCases"] == 14
    assert len(question_file["separateUnassignedProfileEvidence"]) == packet_receipt["unassignedProfileAnalyses"] == 2
    packet_index = json.loads(z.read("current/authored_review_index.json"))
    packet_entries = {e["id"]: e for e in packet_index["entries"]}
    packet_index_comparisons = {sid: packet_entries[sid] == current_index[sid] for sid in ward_ids}
    assert all(packet_index_comparisons.values())
result = {
    "id": "WARD7-CURRENT-SOURCE-BASELINE-134",
    "status": "PASSED_EXACT_SOURCE_AND_CURRENT_LOCAL_CARD_BASELINE",
    "archive": {"path": ARCHIVE.relative_to(G).as_posix(), "bytes": len(archive_bytes), "sha256": sha(archive_bytes)},
    "archiveMembers": 54,
    "verifiedManifestSourceFiles": len(member_checks),
    "preflightChecks": pref["checkCount"],
    "preflightFailures": pref["failures"],
    "identities": ward_ids,
    "originalQuestions": len(candidate["questions"]),
    "directorPacket": {"path": DIRECTOR_PACKET.relative_to(G).as_posix(), "bytes": len(packet_raw), "sha256": sha(packet_raw), "memberCount": 53, "manifestBoundMembers": 52},
    "followupQuestions": 6,
    "totalQuestionDispositionsRequired": 26,
    "requiredNewCases": 14,
    "separateUnassignedProfileAnalyses": 2,
    "catalogCardsExactCurrent": card_comparisons,
    "indexEntriesExactCurrent": index_comparisons,
    "directorPacketIndexEntriesExactCurrent": packet_index_comparisons,
    "currentCounts": idx["authoredCounts"],
}
(D / "WARD7_CURRENT_BASELINE_134.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
