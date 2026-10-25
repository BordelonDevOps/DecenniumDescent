from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
REVIEW = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_environment_3_source_conference_02.json"
OUTPUT = FULL / "rank8-environment3-source-conference-02"
ARCHIVE = FULL / "DD_Rank8_Environment_3_Source_Conference_02.zip"
CHECK = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_CHECK.json"
PREPARATION = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_PREPARATION.json"
REQUEST = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_REQUEST.txt"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_159.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_159.json"
PENDING = AUDIT / "CURRENT125_PENDING_IDENTITY_AUDIT_158.json"
TARGETS = ["absolute-silence", "control-weather", "earthquake"]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def pointer_get(value, pointer: str):
    result = value
    for token in pointer.strip("/").split("/"):
        if not token:
            continue
        token = token.replace("~1", "/").replace("~0", "~")
        result = result[int(token)] if isinstance(result, list) else result[token]
    return result


def spells_by_id(model: dict) -> dict:
    spells = model["spells"]
    return spells if isinstance(spells, dict) else {row["id"]: row for row in spells}


def main() -> None:
    candidate = read(CANDIDATE)
    checks = read(CHECK)
    prep = read(PREPARATION)
    queue = read(QUEUE)
    handoff = read(HANDOFF)
    pending = read(PENDING)
    index = read(INDEX)
    catalog = read(CATALOG)
    entries = {row["id"]: row for row in index["entries"]}
    catalog_spells = {row["id"]: row for row in catalog["spells"]}
    results = []

    def ck(label: str, value: bool) -> None:
        results.append({"check": label, "passed": bool(value)})
        assert value, label

    candidate_binding = binding(CANDIDATE)
    archive_binding = binding(ARCHIVE)
    ck("Preparation and check bind the exact candidate", prep["candidate"] == candidate_binding and checks["candidate"] == candidate_binding)
    ck("Preparation binds exact archive, request, check and current authority", prep["archive"] == archive_binding and prep["check"] == binding(CHECK) and prep["request"] == binding(REQUEST) and prep["sourceAuthority"] == {"reviewedApplied": 723, "pending": 125, "acceptedUnapplied": 0})
    ck("Candidate identifies fresh Conference02 and current 723/125/0 authority", candidate["id"] == "RANK8-ENVIRONMENT3-SOURCE-CONFERENCE02-159" and candidate["currentAuthority"]["reviewedApplied"] == 723 and candidate["currentAuthority"]["pending"] == 125 and candidate["currentAuthority"]["acceptedUnapplied"] == 0)
    ck("Current index/catalog/queue/pending/handoff bindings are exact", candidate["currentAuthority"]["index"] == binding(INDEX) and candidate["currentAuthority"]["catalog"] == binding(CATALOG) and candidate["currentAuthority"]["currentQueue"] == binding(AUDIT / "CURRENT_SPELL_QUEUE_158.json") and candidate["currentAuthority"]["pendingIdentityAudit"] == binding(PENDING) and candidate["currentAuthority"]["priorHandoff"] == binding(AUDIT / "CURRENT_HANDOFF_158.json"))
    ck("Current live pending set is exactly 125 and Environment3 is first", len([e for e in index["entries"] if e["authoredStatus"] == "pending-authored-procedure"]) == 125 and queue["nextGroup"] == "rank8-environment3" and queue["currentPendingGroups"][0]["pendingIds"] == TARGETS)
    ck("Target identities remain pending and current catalog rows match", [r["spellId"] for r in candidate["records"]] == TARGETS and all(entries[sid]["authoredStatus"] == "pending-authored-procedure" and next(r for r in candidate["records"] if r["spellId"] == sid)["completeCurrentCatalogSourceAndAccess"] == catalog_spells[sid] for sid in TARGETS))
    ck("All 15 questions are unique, unselected, and cover only the three targets", len(candidate["questions"]) == 15 and len({q["id"] for q in candidate["questions"]}) == 15 and all(q["decisionSelected"] is False for q in candidate["questions"]) and set().union(*(set(q["spellIds"]) for q in candidate["questions"])) == set(TARGETS))
    ck("Six complete new cases and original future-case requirements remain", len(candidate["futureCaseRequirements"]) >= 4 and len(read(OUTPUT / "CONFERENCE_NOTES.json")["requiredNewCases"]) == 6)
    ck("Fresh authority supersedes Conference01 and labels its 525/323 scope as historical", "Conference01 remains historical 525/323" in candidate["priorConferenceSupersededBy"] and candidate["countsUnchanged"] == {"reviewed": 723, "pending": 125})

    rows = candidate["sourceBindings"]
    frozen = {r["path"]: r for r in read(OUTPUT / "MANIFEST.json")["frozenSources"]}
    ck("All bound current sources have matching manifest rows", len(rows) == len(frozen) == prep["sourceCount"] and set(frozen) == {r["path"] for r in rows})
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        ck("ZIP has unique safe paths and passes CRC verification", len(names) == len(set(names)) and archive.testzip() is None and all(not PurePosixPath(n).is_absolute() and ".." not in PurePosixPath(n).parts for n in names))
        ck("ZIP carries exact candidate/check/request and historical packet", archive.read("CANDIDATE.json") == CANDIDATE.read_bytes() and archive.read("SOURCE_CHECK.json") == CHECK.read_bytes() and archive.read("REQUEST.txt") == REQUEST.read_bytes() and archive.read("historical/Conference01_ARCHIVE.zip") == (FULL / "DD_Rank8_Environment_3_Source_Conference_01.zip").read_bytes())
        for row in rows:
            live = ROOT / Path(*row["path"].split("/"))
            local = OUTPUT / "sources" / Path(*row["path"].split("/"))
            archive_raw = archive.read("sources/" + row["path"])
            ck("Live/frozen/archive source hash matches: " + row["path"], binding(live) == row and local.read_bytes() == live.read_bytes() and len(archive_raw) == row["bytes"] and sha(archive_raw) == row["sha256"])
        historical = [n for n in names if n.startswith("historical/")]
        ck("Historical Conference01 evidence includes local copy explicitly marked not authority", "historical/Conference01_CANDIDATE.json" in historical and "historical/Conference01_CURRENT_LOCAL_WORKING_COPY_NOT_AUTHORITY.json" in historical and "historical/Conference01_PREPARATION.json" in historical)
        ck("ZIP member count matches recorded preparation", len(names) == prep["archiveMemberCount"])

    latest = candidate["recentExactAcceptedAppliedComparisons"]
    perception = next(row for row in latest if row["batch"] == "rank8-perception5-reviewed-156-applied-158")
    expected = ["mass-hallucination", "illusory-dragon", "phantom-execution", "antipathy-sympathy", "glibness"]
    ck("Latest exact comparison is Perception5 and contains only its accepted identities", perception["acceptedIds"] == expected and [r["spellId"] for r in perception["procedures"]] == expected)
    perception_model = read(REVIEW / "rank8perception5_reviewed_156" / "MODEL.json")
    live_perception = spells_by_id(perception_model)
    ck("All Perception5 comparison procedures equal current exact model data", all(perception["procedures"][i]["completeAcceptedProcedure"] == live_perception[sid] for i, sid in enumerate(expected)))
    comparison_scope = perception["scope"].lower()
    ck("Accepted comparison keeps runtime, cosmology, completeness and release boundaries", all(label in comparison_scope for label in ["no runtime", "human-play", "balance", "cosmology", "release"]))
    ck("Preparation records no rule adoption, runtime, human-play, cosmology, or whole-game completion", candidate["newRuleAdoptions"] == 0 and candidate["runtimeTestsExecuted"] == 0 and candidate["humanPlaytests"] == 0 and candidate["cosmologyDecisions"] == 0 and candidate["wholeGameComplete"] is False)
    ck("Updated queue and handoff bind the prepared Environment3 packet", queue["currentPendingGroups"][0]["candidate"] == candidate_binding and queue["currentPendingGroups"][0]["archive"] == archive_binding and handoff["nextPreparedRequest"]["candidate"] == candidate_binding and handoff["nextPreparedRequest"]["archive"] == archive_binding and handoff["currentQueueBinding"] == binding(QUEUE))
    ck("Source check declares zero failures and expected static-only scope", checks["status"] == "PASS" and checks["failures"] == 0 and checks["sourceAuthority"] == {"reviewedApplied": 723, "pending": 125, "acceptedUnapplied": 0})

    report = {
        "id": "RANK8-ENVIRONMENT3-SOURCE-CONFERENCE02-INDEPENDENT-VERIFICATION-159",
        "status": "PASS",
        "candidate": candidate_binding,
        "archive": archive_binding,
        "checks": results,
        "checkCount": len(results),
        "failures": 0,
        "verifiedCurrentSources": len(rows),
        "verifiedArchiveMembers": len(names),
        "authority": {"reviewedApplied": 723, "pending": 125, "acceptedUnapplied": 0},
        "scope": "Packet/source integrity and current identity/authority binding only. No rule adoption or runtime, human-play, balance, cosmology or release approval.",
    }
    out = AUDIT / "RANK8_ENVIRONMENT3_SOURCE_CONFERENCE02_INDEPENDENT_VERIFICATION_159.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "report": str(out), "checkCount": len(results), "sources": len(rows), "archiveMembers": len(names), "failures": 0}, indent=2))


if __name__ == "__main__":
    main()
