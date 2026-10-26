from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUD = FULL / "director-spell-review-129"
IDS = ["cosmic-implosion", "frozen-eternity", "hellstorm", "storm-of-vengeance", "thunder-wrath", "storm-cage"]
CAT10_IDS = ["cataclysmic-conjuration", "elemental-apocalypse", "planar-overload", "armageddon", "cataclysm", "arcane-apocalypse", "meteor-swarm", "starfire-core", "ragnarok", "final-spark"]
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_storm_control_6_source_conference_02_175.json"
ARCHIVE = FULL / "DD_Rank9_Storm_Control_6_Source_Conference_02_175.zip"
OUTPUT = FULL / "rank9-storm-control6-source-conference-02-175"
PREP = FULL / "RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_02_PREPARATION_175.json"
CHECK = FULL / "RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_02_CHECK_175.json"
REQUEST = FULL / "RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_02_REQUEST_175.txt"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUD / "CURRENT_SPELL_QUEUE_175.json"
HANDOFF = AUD / "CURRENT_HANDOFF_175.json"
PENDING = AUD / "CURRENT99_PENDING_IDENTITY_AUDIT_175.json"
AUTH = {"reviewedApplied": 749, "pending": 99, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 473, "scopedInterfaces": 173}
GIT_BYTES_CACHE: dict[str, bytes] = {}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def repository_bytes(path: Path) -> bytes:
    try:
        rel = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.read_bytes()
    if rel not in GIT_BYTES_CACHE:
        try:
            GIT_BYTES_CACHE[rel] = subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{rel}"], cwd=ROOT)
        except subprocess.CalledProcessError:
            GIT_BYTES_CACHE[rel] = path.read_bytes()
    return GIT_BYTES_CACHE[rel]


def bind(path: Path):
    raw = repository_bytes(path)
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def resolve_pointer(obj, pointer: str):
    current = obj
    for part in pointer.strip("/").split("/") if pointer else []:
        part = part.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def main():
    checks = []

    def ck(label, ok):
        checks.append((label, bool(ok)))
        assert ok, label

    candidate_raw = CANDIDATE.read_bytes()
    archive_raw = ARCHIVE.read_bytes()
    candidate = json.loads(candidate_raw.decode("utf-8-sig"))
    prep = read(PREP)
    check_doc = read(CHECK)
    index = read(INDEX)
    catalog = read(CATALOG)
    queue = read(QUEUE)
    handoff = read(HANDOFF)
    pending = read(PENDING)
    index_by = {r["id"]: r for r in index["entries"]}
    catalog_by = {r["id"]: r for r in catalog["spells"]}
    live_pending = {r["id"] for r in index["entries"] if r["authoredStatus"] == "pending-authored-procedure"}

    ck("Fresh candidate hash and byte length match preparation record", prep["candidate"]["sha256"] == sha(candidate_raw) and prep["candidate"]["bytes"] == len(candidate_raw))
    ck("Fresh archive hash and byte length match preparation record", prep["archive"]["sha256"] == sha(archive_raw) and prep["archive"]["bytes"] == len(archive_raw))
    ck("Authority matches the live authored index, queue and handoff", candidate["countsUnchanged"] == {"reviewed": 749, "pending": 99, "acceptedUnapplied": 0} and queue["currentAuthority"] == handoff["currentAuthority"] == AUTH and index["authoredCounts"] == {"reviewed": 749, "pending": 99})
    ck("Pending audit exactly matches the index pending identities", pending["pendingCount"] == 99 and len(live_pending) == 99 and set(pending["pendingIds"]) == live_pending)
    ck("The six review IDs exactly match the next live queue group", prep["reviewIds"] == IDS and candidate["currentPendingIds"] == IDS and queue["nextGroup"] == "rank9-storm-control6" and queue["next"]["group"] == "rank9-storm-control6" and queue["next"]["pendingCount"] == 6 and set(IDS) <= live_pending)
    ck("All original questions and focused additions are present and unselected", len(candidate["questions"]) == 25 and len(candidate["focusedAdditionalQuestions"]) == 2 and len(candidate["allQuestions"]) == 27 and len({q["id"] for q in candidate["allQuestions"]}) == 27 and all(not q["decisionSelected"] for q in candidate["allQuestions"]))
    ck("All question spell scopes are contained within the six pending IDs", set().union(*(set(q["spellIds"]) for q in candidate["allQuestions"])) == set(IDS))
    ck("All 12 complete main-case obligations remain present", len(candidate["requiredNewCaseObligations"]) == 12 and len({c["id"] for c in candidate["requiredNewCaseObligations"]}) == 12 and all(c["status"] == "REQUIRED_NEW_CASE_NOT_AUTHORED" for c in candidate["requiredNewCaseObligations"]))
    ck("All six native source/access cards and current index entries equal live records", len(candidate["records"]) == 6 and [r["spellId"] for r in candidate["records"]] == IDS and all(r["completeCurrentCatalogSourceAndAccess"] == catalog_by[r["spellId"]] and r["currentIndexEntry"] == index_by[r["spellId"]] and r["currentQueueStatus"]["pending"] for r in candidate["records"]))
    registry_path = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
    registry = read(registry_path)
    interfaces_ok = all(x["completeEntryUnchanged"] == registry["entries"][int(x["registryPointer"].split("/")[-1])] for x in candidate["currentAcceptedInterfaceComparisons"])
    ck("All 43 accepted-interface comparisons match the live registry", len(candidate["currentAcceptedInterfaceComparisons"]) == 43 and interfaces_ok)
    counterparts_ok = True
    for item in candidate["completeAppliedCounterparts"]:
        entry = index_by[item["spellId"]]
        env = read(INDEX.parent / entry["procedureFile"])
        pointer = entry.get("wholeCardPointer") or entry["procedurePointer"]
        if item["indexEntry"] != entry or item["completeCurrentCard"] != resolve_pointer(env, pointer):
            counterparts_ok = False
    ck("All ten applied counterpart cards resolve from the current index", len(candidate["completeAppliedCounterparts"]) == 10 and counterparts_ok)
    application = read(AUD / "CATASTROPHE10_APPLICATION_173.json")
    acceptance = read(AUD / "CATASTROPHE10_EXACT_ACCEPTANCE_172.json")
    ck("Latest applied batch exact acceptance, application and validation agree", read(AUD / "CATASTROPHE10_APPLICATION_VALIDATION_173.json")["status"] == "PASS" and application["acceptedIds"] == CAT10_IDS and acceptance["directorDecision"]["acceptedIds"] == CAT10_IDS and acceptance["directorDecision"]["accepted"] is True and acceptance["directorDecision"]["appliedAtDecision"] is False)
    ck("Canonical catalog and index remain bound to the current exact sources", candidate["currentAuthority"]["index"] == bind(INDEX) and candidate["currentAuthority"]["catalog"] == bind(CATALOG))
    ck("Independent preparation checks all pass", check_doc["status"] == "PASS" and check_doc["checksFailed"] == 0 and all(x["passed"] for x in check_doc["checks"]))

    with zipfile.ZipFile(ARCHIVE) as z:
        ck("Archive central directory and all CRCs pass", z.testzip() is None)
        names = z.namelist()
        ck("Archive members are unique and include the complete packet controls", len(names) == len(set(names)) and all(n in names for n in ["CANDIDATE.json", "REQUEST.txt", "SOURCE_CHECK.json", "MANIFEST.json", "SOURCES_MANIFEST.json", "CURRENT_AUTHORITY_UPDATE.json"]))
        ck("Archived candidate and request exactly match published files", z.read("CANDIDATE.json") == candidate_raw and z.read("REQUEST.txt") == REQUEST.read_bytes())
        source_manifest = json.loads(z.read("SOURCES_MANIFEST.json"))
        source_rows = source_manifest["sources"]
        ck("All 89 mapped sources exist once with exact byte length and digest", len(source_rows) == len(candidate["sourceBindings"]) == 89 and len({x["repositoryPath"] for x in source_rows}) == 89 and all(len(z.read(x["packetPath"])) == x["bytes"] and sha(z.read(x["packetPath"])) == x["sha256"] for x in source_rows))
        for row in candidate["sourceBindings"]:
            src = ROOT / row["path"]
            packet = z.read(row["packetPath"])
            if bind(src) != {"path": row["path"], "bytes": row["bytes"], "sha256": row["sha256"]} or packet != repository_bytes(src):
                raise AssertionError(f"Current source binding mismatch: {row['path']}")
        ck("Every current source binding matches the local repository byte-for-byte", True)
        historical = z.read("historical/Conference01_ARCHIVE.zip")
        hist_candidate = z.read("historical/Conference01_CANDIDATE.json")
        hist_archive_candidate = z.read("historical/Conference01_ARCHIVE_MEMBER_CANDIDATE.json")
        with zipfile.ZipFile(__import__("io").BytesIO(historical)) as oldz:
            ck("Conference01 archive retains its exact original hash and passes CRC", sha(historical) == "e64c6db2037880b42e0598f190f0060fa224cc621521444e5d91aaac6e477a69" and oldz.testzip() is None)
            ck("Both historical candidate serializations are preserved byte-exactly and parse identically", hist_archive_candidate == oldz.read("CANDIDATE.json") and json.loads(hist_candidate) == json.loads(hist_archive_candidate))
        manifest = json.loads(z.read("MANIFEST.json"))
        manifest_files = {x["path"]: x for x in manifest["members"]}
        ck("Manifest member lengths and hashes match all listed packet files", all(len(z.read(path)) == meta["bytes"] and sha(z.read(path)) == meta["sha256"] for path, meta in manifest_files.items()))
        ck("Manifest covers every archive member except itself", set(manifest_files) | {"MANIFEST.json"} == set(names))
        ck("Embedded source check declares pass with zero failures", json.loads(z.read("SOURCE_CHECK.json"))["status"] == "PASS" and json.loads(z.read("SOURCE_CHECK.json"))["checksFailed"] == 0)

    ck("Request requires exact scope, all 27 questions, 12 cases, retained holds and separate approvals", all(s in REQUEST.read_text(encoding="utf-8") for s in ["749 applied-reviewed / 99 pending / 0 accepted-unapplied", "27 total", "12 specified main cases", "complete retained holds", "runtime, human-play, balance, cosmology, domain-closure, and release", "accepted=true and applied=false"]))
    ck("No dispositions, rules, runtime, human-play, or cosmology choices were preselected", candidate["newRuleAdoptions"] == 0 and candidate["runtimeTestsExecuted"] == 0 and candidate["humanPlaytests"] == 0 and candidate["cosmologyDecisions"] == 0 and not candidate["wholeGameComplete"])

    print(json.dumps({"status": "PASS", "checks": len(checks), "failed": [label for label, ok in checks if not ok], "candidateSha256": sha(candidate_raw), "archiveSha256": sha(archive_raw), "sourceBindings": len(candidate["sourceBindings"]), "questions": len(candidate["allQuestions"]), "requiredMainCases": len(candidate["requiredNewCaseObligations"]), "reviewIds": IDS, "authority": AUTH}, indent=2))


if __name__ == "__main__":
    main()
