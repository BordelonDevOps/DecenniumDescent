from pathlib import Path
import hashlib, json, zipfile

G = Path(r"C:\Github\DecenniumDescent")
D = Path(__file__).parent.resolve()
INDEX = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = G / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = D / "CURRENT_SPELL_QUEUE_134.json"
sha = lambda b: hashlib.sha256(b).hexdigest()
idx = json.loads(INDEX.read_text(encoding="utf-8-sig"))
catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
queue = json.loads(QUEUE.read_text(encoding="utf-8-sig"))
idx_entries = {e["id"]: e for e in idx["entries"]}
cards = {s["id"]: s for s in catalog["spells"]}
groups = {g["group"]: g for g in queue["groups"]}
specs = [
    ("manifestation7", "DD_Manifestation_7_Source_Conference_01.zip"),
    ("soul-contact6", "DD_Soul_Contact_6_Source_Conference_01.zip"),
    ("vitality-matter10", "DD_Vitality_Matter_10_Source_Conference_01.zip"),
]
results = []
for group_name, archive_name in specs:
    path = G / "docs/audit/2026-10-08/full-game" / archive_name
    raw_archive = path.read_bytes()
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        manifest = json.loads(z.read("MANIFEST.json"))
        candidate = json.loads(z.read("CANDIDATE.json"))
        preflight = json.loads(z.read("PREFLIGHT.json"))
        assert len(manifest["files"]) == manifest["sourceCount"]
        for item in manifest["files"]:
            data = z.read("sources/" + item["path"])
            assert len(data) == item["bytes"] and sha(data) == item["sha256"], (group_name, item["path"])
        wanted = groups[group_name]["identities"]
        records = {r["spellId"]: r for r in candidate["records"]}
        assert set(records) == set(wanted)
        assert len(candidate["questions"]) > 0 and preflight["failures"] == 0
        card_ok, index_ok = {}, {}
        for sid in wanted:
            card_ok[sid] = records[sid]["completeCurrentCatalogSourceAndAccess"] == cards[sid]
            index_ok[sid] = records[sid]["currentIndexEntry"] == idx_entries[sid]
            assert idx_entries[sid]["authoredStatus"] == "pending-authored-procedure"
        assert all(card_ok.values()) and all(index_ok.values())
        results.append({
            "group": group_name,
            "archive": {"path": path.relative_to(G).as_posix(), "bytes": len(raw_archive), "sha256": sha(raw_archive)},
            "archiveMemberCount": len(z.infolist()),
            "manifestBoundSourceFiles": len(manifest["files"]),
            "candidateStatus": candidate["status"],
            "identityCount": len(wanted),
            "questionCount": len(candidate["questions"]),
            "preflightChecks": preflight["checkCount"],
            "preflightFailures": preflight["failures"],
            "catalogCardsExactCurrent": card_ok,
            "indexEntriesExactCurrent": index_ok,
        })
assert idx["authoredCounts"] == {"reviewed": 648, "pending": 200}
report = {"id": "NEXT-SOURCE-CONFERENCES-BASELINE-134", "status": "PASSED_ALL_THREE_SOURCE_BASELINES", "currentCounts": idx["authoredCounts"], "groups": results}
(D / "NEXT_SOURCE_CONFERENCES_BASELINE_134.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
