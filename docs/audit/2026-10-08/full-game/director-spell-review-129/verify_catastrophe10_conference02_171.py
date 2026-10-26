from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUD = FULL / "director-spell-review-129"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_catastrophe_10_source_conference_02.json"
ARCHIVE = FULL / "DD_Rank9_Catastrophe_10_Source_Conference_02.zip"
OUTPUT = FULL / "rank9-catastrophe10-source-conference-02-171"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
IDS = ["cataclysmic-conjuration", "elemental-apocalypse", "planar-overload", "armageddon", "cataclysm", "arcane-apocalypse", "meteor-swarm", "starfire-core", "ragnarok", "final-spark"]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main():
    results = []

    def ck(label, condition):
        results.append({"check": label, "passed": bool(condition)})

    candidate_bytes = CANDIDATE.read_bytes()
    candidate = json.loads(candidate_bytes.decode("utf-8-sig"))
    archive_bytes = ARCHIVE.read_bytes()
    index_bytes = INDEX.read_bytes()
    catalog_bytes = CATALOG.read_bytes()
    index, catalog = read(INDEX), read(CATALOG)
    queue = read(AUD / "CURRENT_SPELL_QUEUE_171.json")
    handoff = read(AUD / "CURRENT_HANDOFF_171.json")
    pending = read(AUD / "CURRENT109_PENDING_IDENTITY_AUDIT_171.json")
    source_check = read(FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_CHECK_171.json")
    preparation = read(FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_PREPARATION_171.json")
    manifest = read(OUTPUT / "MANIFEST.json")
    rows = {row["id"]: row for row in index["entries"]}
    cards = {row["id"]: row for row in catalog["spells"]}
    pending_ids = sorted(row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure")

    ck("Current live authority is 739 reviewed / 109 pending / 0 accepted-unapplied", index["authoredCounts"] == {"reviewed": 739, "pending": 109} and queue["currentAuthority"]["reviewedApplied"] == 739 and queue["currentAuthority"]["pending"] == 109 and queue["currentAuthority"]["acceptedUnapplied"] == 0)
    ck("Pending audit exactly matches live index and preserves closed feat/spell cohorts", pending["pendingIds"] == pending_ids and pending["pendingCount"] == 109 and pending["closed335AndCompletedCohortsReopened"] is False)
    ck("Exact ten Catastrophe spells are the first pending group", candidate["currentPendingIds"] == IDS and queue["currentPendingGroups"][0]["pendingIds"] == IDS and set(IDS) <= set(pending_ids))
    ck("All ten current native cards/access rows and index entries match live authority", all(rec["completeCurrentCatalogSourceAndAccess"] == cards[rec["spellId"]] and rec["currentIndexEntry"] == rows[rec["spellId"]] for rec in candidate["records"]))
    ck("All 25 source questions remain present and unselected", len(candidate["questions"]) == 25 and all(q["decisionSelected"] is False for q in candidate["questions"]))
    ck("Current source bindings equal live files and the exact frozen archive copies", len(candidate["sourceBindings"]) == 86 and all((ROOT / row["path"]).read_bytes() == (OUTPUT / "sources" / PurePosixPath(row["path"])).read_bytes() and len((ROOT / row["path"]).read_bytes()) == row["bytes"] and sha((ROOT / row["path"]).read_bytes()) == row["sha256"] for row in candidate["sourceBindings"]))
    ck("Current authority bindings in candidate point at this exact index/catalog/queue/handoff/audit", candidate["currentAuthority"]["index"]["sha256"] == sha(index_bytes) and candidate["currentAuthority"]["catalog"]["sha256"] == sha(catalog_bytes) and candidate["currentAuthority"]["currentQueue"]["sha256"] == sha((AUD / "CURRENT_SPELL_QUEUE_170.json").read_bytes()) and candidate["currentAuthority"]["currentHandoff"]["sha256"] == sha((AUD / "CURRENT_HANDOFF_170.json").read_bytes()) and candidate["currentPendingIdentityAudit"]["sha256"] == sha((AUD / "CURRENT109_PENDING_IDENTITY_AUDIT_170.json").read_bytes()))
    ck("Four-identity accepted batch since Conference01 is exact and verified", candidate["currentAcceptedBatchSinceConference01"]["ids"] == ["prismatic-wall", "faction-convergence", "divine-intervention-lesser", "reality-patch"] and candidate["currentAcceptedBatchSinceConference01"]["validation"]["sha256"] == sha((AUD / "REMAINING4_APPLICATION_VALIDATION_170.json").read_bytes()))
    ck("Candidate retains exact historical 525/323 Conference01 source archive and authority label", candidate["historicalConference01"]["authority"] == {"reviewed": 525, "pending": 323} and candidate["historicalConference01"]["archive"]["sha256"] == "c638dd2a85617789d73864346c2a55820e84edb342a2cb7d7c90537dc5f954c4" and (OUTPUT / "historical/Conference01_ARCHIVE.zip").read_bytes() == (FULL / "DD_Rank9_Catastrophe_10_Source_Conference_01.zip").read_bytes())
    ck("No new choices, rules, runtime behavior, human play, or cosmology state were adopted", candidate["newRuleAdoptions"] == candidate["runtimeTestsExecuted"] == candidate["humanPlaytests"] == candidate["cosmologyDecisions"] == 0 and candidate["wholeGameComplete"] is False)
    ck("Source-conference check passed all preparation checks", source_check["status"] == "PASS" and source_check["checksFailed"] == 0 and all(c["passed"] for c in source_check["checks"]))
    ck("Preparation manifest binds exact candidate and archive", preparation["candidate"]["sha256"] == sha(candidate_bytes) and preparation["archive"]["sha256"] == sha(archive_bytes) and preparation["archive"]["bytes"] == len(archive_bytes))
    ck("Handoff and queue bind prepared packet at current authority", handoff["currentQueueBinding"]["sha256"] == sha((AUD / "CURRENT_SPELL_QUEUE_171.json").read_bytes()) and queue["sourceConferencePrepared"]["archive"]["sha256"] == sha(archive_bytes) and handoff["nextPreparedRequest"]["candidate"]["sha256"] == sha(candidate_bytes))
    with zipfile.ZipFile(ARCHIVE) as z:
        names = z.namelist()
        zip_checks = z.testzip() is None and len(names) == len(set(names)) and z.read("CANDIDATE.json") == candidate_bytes and json.loads(z.read("SOURCE_CHECK.json"))["checksFailed"] == 0
        zip_sources = all(z.read("sources/" + row["path"]) == (ROOT / row["path"]).read_bytes() for row in candidate["sourceBindings"])
    ck("Fresh source ZIP is CRC-valid, unique-member, and carries exact candidate and check", zip_checks)
    ck("All 86 current source bindings are byte-exact inside the ZIP", zip_sources)
    check_count = len(results)
    failures = [r["check"] for r in results if not r["passed"]]
    report = {"id": "RANK9-CATASTROPHE10-CONFERENCE02-VERIFICATION-171", "status": "PASS" if not failures else "FAIL", "checkCount": check_count, "checksPassed": check_count - len(failures), "checksFailed": len(failures), "failedChecks": failures, "checks": results, "currentAuthority": queue["currentAuthority"], "scopeIds": IDS, "sourceBindings": len(candidate["sourceBindings"]), "questions": len(candidate["questions"]), "archive": {"bytes": len(archive_bytes), "sha256": sha(archive_bytes)}, "candidate": {"bytes": len(candidate_bytes), "sha256": sha(candidate_bytes)}}
    (FULL / "RANK9_CATASTROPHE_10_SOURCE_CONFERENCE_02_VERIFICATION_171.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["id", "status", "checkCount", "checksPassed", "checksFailed", "failedChecks", "currentAuthority", "sourceBindings", "questions", "archive", "candidate"]}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
