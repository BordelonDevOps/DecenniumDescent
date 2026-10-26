from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUD = FULL / "director-spell-review-129"
IDS = ["cosmic-implosion", "frozen-eternity", "hellstorm", "storm-of-vengeance", "thunder-wrath", "storm-cage"]
OLD_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_storm_control_6_source_conference_01.json"
OLD_ARCHIVE = FULL / "DD_Rank9_Storm_Control_6_Source_Conference_01.zip"
NOTES = AUD / "RANK9STORMCONTROL6_NEXT_CONFERENCE_NOTES_129.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE = AUD / "CURRENT_SPELL_QUEUE_173.json"
HANDOFF = AUD / "CURRENT_HANDOFF_173.json"
PENDING = AUD / "CURRENT99_PENDING_IDENTITY_AUDIT_173.json"
LATEST = [
    AUD / "CATASTROPHE10_APPLICATION_173.json",
    AUD / "CATASTROPHE10_EXACT_ACCEPTANCE_172.json",
    AUD / "CATASTROPHE10_APPLICATION_VALIDATION_173.json",
    AUD / "RANK9_CATASTROPHE10_GPT_RETURN_172.json",
    AUD / "GPT_DIRECTOR_DECISION_CATASTROPHE10_172.json",
    ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9catastrophe10_reviewed_172/MODEL.json",
    AUD / "rank9_catastrophe10_return172_received/DD_Rank9_Catastrophe10_Director_Return172.zip",
]
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank9_storm_control_6_source_conference_02_175.json"
OUTPUT = FULL / "rank9-storm-control6-source-conference-02-175"
ARCHIVE = FULL / "DD_Rank9_Storm_Control_6_Source_Conference_02_175.zip"
CHECK = FULL / "RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_02_CHECK_175.json"
PREP = FULL / "RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_02_PREPARATION_175.json"
REQUEST = FULL / "RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_02_REQUEST_175.txt"
PENDING_AFTER = AUD / "CURRENT99_PENDING_IDENTITY_AUDIT_175.json"
QUEUE_AFTER = AUD / "CURRENT_SPELL_QUEUE_175.json"
HANDOFF_AFTER = AUD / "CURRENT_HANDOFF_175.json"
AUTH = {"reviewedApplied": 749, "pending": 99, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 473, "scopedInterfaces": 173}
GIT_BYTES_CACHE: dict[str, bytes] = {}


def enc(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def repository_bytes(path: Path) -> bytes:
    try:
        rel = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.read_bytes()
    if rel not in GIT_BYTES_CACHE:
        try:
            GIT_BYTES_CACHE[rel] = subprocess.check_output(["git", "cat-file", "blob", f"HEAD:{rel}"], cwd=ROOT, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            GIT_BYTES_CACHE[rel] = path.read_bytes()
    return GIT_BYTES_CACHE[rel]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bind(path: Path, rel: str | None = None):
    raw = repository_bytes(path)
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def resolve_pointer(obj, pointer: str):
    current = obj
    for part in pointer.strip("/").split("/") if pointer else []:
        part = part.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def main():
    outputs = [CANDIDATE, OUTPUT, ARCHIVE, CHECK, PREP, REQUEST, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER]
    assert not any(p.exists() for p in outputs), "Refusing to overwrite an existing packet or checkpoint."
    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index, catalog, queue, handoff, pending, notes = map(read, [INDEX, CATALOG, QUEUE, HANDOFF, PENDING, NOTES])
    old_archive_raw = OLD_ARCHIVE.read_bytes()
    assert sha(old_archive_raw) == "e64c6db2037880b42e0598f190f0060fa224cc621521444e5d91aaac6e477a69"
    with zipfile.ZipFile(OLD_ARCHIVE) as old_zip:
        assert old_zip.testzip() is None
        archive_candidate_raw = old_zip.read("CANDIDATE.json")
        old_manifest_raw = old_zip.read("MANIFEST.json")
        old_check_raw = old_zip.read("SOURCE_CHECK.json")
        old_readme_raw = old_zip.read("README.md")
    old_raw = repository_bytes(OLD_CANDIDATE)
    assert sha(old_raw) == "15c672c40f3ac72f33e7aae274f55e00c20e6ecba4b309b64c64bc0de641797b"
    assert sha(archive_candidate_raw) == "15c672c40f3ac72f33e7aae274f55e00c20e6ecba4b309b64c64bc0de641797b"
    old = json.loads(old_raw.decode("utf-8-sig"))
    assert old == json.loads(archive_candidate_raw.decode("utf-8-sig")), "Conference01 candidate data differs; reconcile before reuse."
    assert queue["currentAuthority"] == handoff["currentAuthority"] == AUTH
    assert pending["authoredCounts"] == {"reviewed": 749, "pending": 99}
    assert queue["nextGroup"] == "rank9-storm-control6"
    group = copy.deepcopy(queue["currentPendingGroups"][0])
    assert group["group"] == "rank9-storm-control6" and group["pendingIds"] == IDS and group["pendingCount"] == 6
    assert pending["pendingCount"] == 99 and len(pending["pendingIds"]) == 99
    live_pending = {r["id"] for r in index["entries"] if r["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == 99 and set(pending["pendingIds"]) == live_pending and set(IDS) <= live_pending
    assert index["authoredCounts"] == {"reviewed": 749, "pending": 99}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 473
    assert len(old["records"]) == 6 and [r["spellId"] for r in old["records"]] == IDS
    assert len(old["questions"]) == 25 and all(not q["decisionSelected"] for q in old["questions"])
    assert len(notes["focusedAdditionalQuestions"]) == 2 and all(not q["decisionSelected"] for q in notes["focusedAdditionalQuestions"])
    assert len(notes["requiredNewCases"]) == 12 and all(x["status"] == "REQUIRED_NEW_CASE_NOT_AUTHORED" for x in notes["requiredNewCases"])
    assert len(old["sourceBindings"]) == 78

    index_by = {r["id"]: r for r in index["entries"]}
    catalog_by = {r["id"]: r for r in catalog["spells"]}
    historical_queue_refs = {k: copy.deepcopy(group[k]) for k in ["candidate", "archive"] if k in group}
    current_group_context = copy.deepcopy(group)
    current_group_context.pop("candidate", None)
    current_group_context.pop("archive", None)
    current_group_context["status"] = "CURRENT_749_99_SCOPE; conference artifacts are recorded separately"
    source_paths = {row["path"] for row in old["sourceBindings"]}
    current_authority_paths = {
        INDEX.relative_to(ROOT).as_posix(), CATALOG.relative_to(ROOT).as_posix(),
        QUEUE.relative_to(ROOT).as_posix(), HANDOFF.relative_to(ROOT).as_posix(),
        PENDING.relative_to(ROOT).as_posix(), NOTES.relative_to(ROOT).as_posix(),
        *[p.relative_to(ROOT).as_posix() for p in LATEST],
    }
    source_paths |= current_authority_paths
    for rel in source_paths:
        assert (ROOT / rel).is_file(), f"Missing current packet source: {rel}"
    source_bindings = [
        {**bind(ROOT / rel, rel), "packetPath": f"sources/{number:03d}.bin"}
        for number, rel in enumerate(sorted(source_paths), 1)
    ]

    candidate = copy.deepcopy(old)
    now = datetime.now(timezone.utc).isoformat()
    extra_questions = copy.deepcopy(notes["focusedAdditionalQuestions"])
    all_questions = copy.deepcopy(old["questions"]) + extra_questions
    historical_candidate_binding = bind(OLD_CANDIDATE)
    candidate.update({
        "id": "RANK9-STORM-CONTROL6-SOURCE-CONFERENCE02-175",
        "recordedAtUtc": now,
        "sourceGitBranch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
        "sourceGitCommit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "status": "FRESH_SOURCE_CONFERENCE_PREPARED_UNSENT",
        "developmentDirection": "Fresh source context bound to the current 749 applied-reviewed / 99 pending / 0 accepted-unapplied authority. Conference01 and its 525/323 baseline are retained as historical evidence only.",
        "supersedes": "This Conference02 packet controls the current review scope for exactly the six Storm Control identities. Current index, catalog, queue, handoff, pending audit, latest accepted batch and all source bindings are refreshed to the live 749/99 authority. Conference01 remains byte-exact historical context only.",
        "currentAuthority": {**AUTH, "index": bind(INDEX), "catalog": bind(CATALOG), "currentQueue": bind(QUEUE), "currentHandoff": bind(HANDOFF), "pendingIdentityAudit": bind(PENDING), "latestApplication": bind(LATEST[0]), "latestExactAcceptance": bind(LATEST[1]), "latestApplicationValidation": bind(LATEST[2]), "latestDirectorReturnReceipt": bind(LATEST[3]), "latestReturnArchive": bind(LATEST[6])},
        "countsUnchanged": {"reviewed": 749, "pending": 99, "acceptedUnapplied": 0},
        "historicalConference01": {"authority": old["countsUnchanged"], "workspaceCandidate": historical_candidate_binding, "archiveMemberCandidate": {"path": "CANDIDATE.json in archive", "bytes": len(archive_candidate_raw), "sha256": sha(archive_candidate_raw)}, "workspaceVsArchiveCandidate": "The exact current Git blob candidate matches the archived CANDIDATE.json byte-for-byte. The checked-out Windows line-ending variant is not used as authority.", "archive": bind(OLD_ARCHIVE), "queueHistoricalReferences": historical_queue_refs, "qualification": "Exact 525/323 source-conference history only. It is superseded by current Conference02 authority and does not determine current acceptance or pending counts."},
        "sourceBindings": source_bindings,
        "currentPendingIds": IDS,
        "currentQueueGroup": current_group_context,
        "currentPendingIdentityAudit": {"id": pending["id"], **bind(PENDING), "pendingCount": 99, "pendingIds": pending["pendingIds"]},
        "currentAcceptedBatchSinceConference01": {"ids": read(LATEST[1])["acceptedIds"], "application": bind(LATEST[0]), "acceptance": bind(LATEST[1]), "validation": bind(LATEST[2]), "decisionReceipt": bind(LATEST[3]), "returnArchive": bind(LATEST[6]), "scope": "The immediately preceding exact Rank9 Catastrophe10 batch is applied. The complete live index/catalog and refreshed accepted-interface contexts remain authoritative for all other intervening completed cohorts."},
        "priorConferenceQuestionSetPreserved": {"questionCount": 25, "allStillUnselected": True},
        "focusedAdditionalQuestions": extra_questions,
        "allQuestions": all_questions,
        "requiredNewCaseObligations": copy.deepcopy(notes["requiredNewCases"]),
        "originalFutureCaseRequirementsUnchanged": copy.deepcopy(notes["originalFutureCaseRequirementsUnchanged"]),
        "focusedAdditionalQuestionSource": bind(NOTES),
        "gptCommunication": "Fresh rank9 Storm Control6 packet for current 749 applied-reviewed / 99 pending / 0 accepted-unapplied authority. Review exactly cosmic-implosion, frozen-eternity, hellstorm, storm-of-vengeance, thunder-wrath, and storm-cage. Preserve and resolve all 25 original source questions plus both focused additional questions (27 total). Author complete source-faithful procedures and required cases/branches, including real chronology, repeated-event, control, containment, damage, displacement, and temporal-clock evidence. Return exact accepted IDs, exact blockers, retained holds, and an independent semantic failure check. Do not change canonical data or reopen any completed/applied spell or feat cohort.",
        "newRuleAdoptions": 0, "runtimeTestsExecuted": 0, "humanPlaytests": 0, "sourceInformationDeleted": 0, "cosmologyDecisions": 0, "wholeGameComplete": False,
    })

    for record in candidate["records"]:
        sid = record["spellId"]
        assert record["completeCurrentCatalogSourceAndAccess"] == catalog_by[sid], f"Native card/access changed for {sid}; resolve source drift before sending."
        assert index_by[sid]["authoredStatus"] == "pending-authored-procedure"
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(catalog_by[sid])
        record["currentIndexEntry"] = copy.deepcopy(index_by[sid])
        record["currentQueueStatus"] = {"identity": sid, "group": "rank9-storm-control6", "pending": True, "reviewedApplied": 749, "pendingCount": 99}
        record["status"] = "Fresh Conference02 source context; all dispositions remain unselected."

    for counterpart in candidate["completeAppliedCounterparts"]:
        sid = counterpart["spellId"]
        entry = index_by[sid]
        env_path = (INDEX.parent / entry["procedureFile"]).resolve()
        envelope = read(env_path)
        pointer = entry.get("wholeCardPointer") or entry["procedurePointer"]
        counterpart["source"] = bind(env_path)
        counterpart["pointer"] = pointer
        counterpart["completeCurrentCard"] = copy.deepcopy(resolve_pointer(envelope, pointer))
        shared = entry.get("sharedRulesPointer")
        counterpart["completeSharedRules"] = copy.deepcopy(resolve_pointer(envelope, shared) if shared else envelope.get("sharedRules", {}))
        counterpart["indexEntry"] = copy.deepcopy(entry)
    registry_path = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
    registry = read(registry_path)
    for interface in candidate["currentAcceptedInterfaceComparisons"]:
        pointer = interface["registryPointer"]
        number = int(pointer.split("/")[-1])
        interface["completeEntryUnchanged"] = copy.deepcopy(registry["entries"][number])
    for row in candidate["completeCosmologySourcesAndAuthority"]:
        old_bind = row.get("source") or row.get("binding")
        if isinstance(old_bind, dict) and old_bind.get("path"):
            live_path = ROOT / old_bind["path"]
            if live_path.is_file():
                row["source"] = bind(live_path)

    assert len(candidate["questions"]) == 25 and all(not q["decisionSelected"] for q in candidate["questions"])
    assert len(candidate["allQuestions"]) == 27 and len({q["id"] for q in candidate["allQuestions"]}) == 27
    assert all(not q["decisionSelected"] for q in candidate["allQuestions"])
    assert set().union(*(set(q["spellIds"]) for q in candidate["allQuestions"])) == set(IDS)
    assert candidate["currentPendingIds"] == IDS and candidate["countsUnchanged"] == {"reviewed": 749, "pending": 99, "acceptedUnapplied": 0}
    candidate_raw = enc(candidate)
    write(CANDIDATE, candidate_raw)

    case_ids = [case["id"] for case in candidate["requiredNewCaseObligations"]]
    request_text = (
        "GPT — review the attached fresh Rank9 Storm Control6 Conference02 packet against the current GitHub branch.\n\n"
        "Authority: 749 applied-reviewed / 99 pending / 0 accepted-unapplied; 473 complete standalone procedures; 173 scoped interfaces.\n"
        f"Exact spell scope: {', '.join(IDS)} only.\n\n"
        "Resolve all 25 preserved source questions and both focused additions (27 total). Return complete source-faithful procedures, every question disposition, at least the 12 specified main cases plus all distinct branches, reversible event/state evidence, explicit exact accepted IDs, exact blockers, complete retained holds, and an independent semantic failure check. Refresh all live source/access, accepted-interface, cosmology, and queue context from this packet. The chronology question requires each spell's own source-relative schedule and opportunity accounting; do not impose a universal pulse rule. The cross-domain question requires separate time-control, containment, damage-resistance, anchoring, displacement, and support-loss scopes.\n\n"
        f"Required case IDs: {', '.join(case_ids)}. Preserve every native route and access record. Keep runtime, human-play, balance, cosmology, domain-closure, and release qualifications explicit. Do not edit canonical files, alter the index/catalog, reopen applied spell cohorts, or reopen the closed feat review. Mark accepted=true and applied=false only for the exact IDs that pass; otherwise leave them unaccepted and unapplied and list exact blockers.\n"
    )
    write(REQUEST, request_text.encode("utf-8"))
    output_files: list[Path] = []
    write(OUTPUT / "CANDIDATE.json", candidate_raw); output_files.append(OUTPUT / "CANDIDATE.json")
    write(OUTPUT / "REQUEST.txt", request_text.encode("utf-8")); output_files.append(OUTPUT / "REQUEST.txt")
    write(OUTPUT / "historical/Conference01_ARCHIVE.zip", old_archive_raw); output_files.append(OUTPUT / "historical/Conference01_ARCHIVE.zip")
    write(OUTPUT / "historical/Conference01_CANDIDATE.json", old_raw); output_files.append(OUTPUT / "historical/Conference01_CANDIDATE.json")
    write(OUTPUT / "historical/Conference01_ARCHIVE_MEMBER_CANDIDATE.json", archive_candidate_raw); output_files.append(OUTPUT / "historical/Conference01_ARCHIVE_MEMBER_CANDIDATE.json")
    write(OUTPUT / "historical/Conference01_MANIFEST.json", old_manifest_raw); output_files.append(OUTPUT / "historical/Conference01_MANIFEST.json")
    write(OUTPUT / "historical/Conference01_SOURCE_CHECK.json", old_check_raw); output_files.append(OUTPUT / "historical/Conference01_SOURCE_CHECK.json")
    write(OUTPUT / "historical/Conference01_README.md", old_readme_raw); output_files.append(OUTPUT / "historical/Conference01_README.md")
    authority_update = {"id": "RANK9-STORM-CONTROL6-CURRENT-AUTHORITY-UPDATE-175", "recordedAtUtc": now, "authority": AUTH, "scopeIds": IDS, "index": bind(INDEX), "catalog": bind(CATALOG), "queue": bind(QUEUE), "handoff": bind(HANDOFF), "pendingIdentityAudit": bind(PENDING), "latestAppliedBatch": {"application": bind(LATEST[0]), "acceptance": bind(LATEST[1]), "validation": bind(LATEST[2]), "returnReceipt": bind(LATEST[3]), "returnArchive": bind(LATEST[6])}, "focusedQuestionSource": bind(NOTES), "qualification": "Fresh static source context only; no new procedure, runtime, cosmology, playtest, balance, or release approval."}
    write(OUTPUT / "CURRENT_AUTHORITY_UPDATE.json", enc(authority_update)); output_files.append(OUTPUT / "CURRENT_AUTHORITY_UPDATE.json")
    source_manifest_rows = []
    for row in source_bindings:
        src = ROOT / row["path"]
        dst = OUTPUT / PurePosixPath(row["packetPath"])
        write(dst, repository_bytes(src))
        source_manifest_rows.append({"repositoryPath": row["path"], "packetPath": row["packetPath"], "bytes": row["bytes"], "sha256": row["sha256"]})
    write(OUTPUT / "SOURCES_MANIFEST.json", enc({"id": "RANK9-STORM-CONTROL6-CONFERENCE02-SOURCES-175", "sources": source_manifest_rows}))
    output_files.append(OUTPUT / "SOURCES_MANIFEST.json")
    readme = ("# Rank9 Storm Control6 Source Conference02\n\n"
              "Freshly bound to 749/99/0 authority. Scope is exactly six pending rank9 identities, 25 preserved questions plus two focused additions, and 12 required main-case obligations. Conference01 is historical context only. All dispositions remain unselected; this packet makes no canonical or runtime changes.\n")
    write(OUTPUT / "README.md", readme.encode("utf-8")); output_files.append(OUTPUT / "README.md")

    checks = []
    def ck(label, ok):
        checks.append({"check": label, "passed": bool(ok)})
        assert ok, label
    ck("Current authority and standalone count match the live index", AUTH == {"reviewedApplied": 749, "pending": 99, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 473, "scopedInterfaces": 173})
    ck("Live pending identity set matches the current pending audit", set(pending["pendingIds"]) == live_pending and pending["pendingCount"] == 99)
    ck("Exact six Storm Control IDs are the next pending group", group["group"] == "rank9-storm-control6" and group["pendingIds"] == IDS and set(IDS) <= live_pending)
    ck("All 25 original questions and two focused additions remain unselected", len(candidate["questions"]) == 25 and len(candidate["focusedAdditionalQuestions"]) == 2 and len(candidate["allQuestions"]) == 27 and all(not q["decisionSelected"] for q in candidate["allQuestions"]))
    ck("All 12 specified case obligations are preserved", len(candidate["requiredNewCaseObligations"]) == 12 and [x["id"] for x in candidate["requiredNewCaseObligations"]] == case_ids)
    ck("All six current catalog cards and index entries bind live data", all(r["completeCurrentCatalogSourceAndAccess"] == catalog_by[r["spellId"]] and r["currentIndexEntry"] == index_by[r["spellId"]] for r in candidate["records"]))
    ck("Refreshed accepted interfaces and applied counterparts are present", len(candidate["currentAcceptedInterfaceComparisons"]) == 43 and len(candidate["completeAppliedCounterparts"]) == 10)
    ck("All current source bindings are exact byte-for-byte Git repository blobs", all(bind(ROOT / r["path"]) == {"path": r["path"], "bytes": r["bytes"], "sha256": r["sha256"]} and sha((OUTPUT / PurePosixPath(r["packetPath"])).read_bytes()) == r["sha256"] for r in source_bindings))
    ck("Latest accepted application, exact acceptance, validation, receipt, and return archive are bound", all(p.is_file() for p in LATEST) and read(LATEST[2])["status"] == "PASS")
    ck("Conference01 archive and exact Git blob candidate remain byte-exact historical evidence", (OUTPUT / "historical/Conference01_ARCHIVE.zip").read_bytes() == old_archive_raw and (OUTPUT / "historical/Conference01_CANDIDATE.json").read_bytes() == old_raw and (OUTPUT / "historical/Conference01_ARCHIVE_MEMBER_CANDIDATE.json").read_bytes() == archive_candidate_raw and old_raw == archive_candidate_raw)
    ck("No rules, runtime, human-play, or cosmology choices are adopted", candidate["newRuleAdoptions"] == candidate["runtimeTestsExecuted"] == candidate["humanPlaytests"] == candidate["cosmologyDecisions"] == 0 and not candidate["wholeGameComplete"])
    ck("Canonical catalog and index bytes remain unchanged", INDEX.read_bytes() == index_raw and CATALOG.read_bytes() == catalog_raw)
    check_doc = {"id": "RANK9-STORM-CONTROL6-CONFERENCE02-CHECK-175", "recordedAtUtc": now, "status": "PASS", "checkCount": len(checks), "checksFailed": 0, "checks": checks, "currentAuthority": AUTH, "scopeIds": IDS, "questionCount": 27, "requiredMainCaseCount": 12, "sourceBindingCount": len(source_bindings)}
    write(CHECK, enc(check_doc)); write(OUTPUT / "SOURCE_CHECK.json", enc(check_doc))
    members = []
    for path in sorted(OUTPUT.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.json":
            raw = path.read_bytes()
            members.append({"path": path.relative_to(OUTPUT).as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    manifest = {"id": "RANK9-STORM-CONTROL6-CONFERENCE02-MANIFEST-175", "candidate": {"path": "CANDIDATE.json", "bytes": len(candidate_raw), "sha256": sha(candidate_raw)}, "currentAuthority": AUTH, "scopeIds": IDS, "memberCount": len(members), "members": members, "historicalConference01Archive": {"path": "historical/Conference01_ARCHIVE.zip", "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)}, "liveCurrentSourceBindings": source_bindings}
    write(OUTPUT / "MANIFEST.json", enc(manifest))
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(OUTPUT.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(OUTPUT).as_posix())
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == len(set(names))
        assert z.read("CANDIDATE.json") == candidate_raw
        assert z.read("historical/Conference01_ARCHIVE.zip") == old_archive_raw
        assert json.loads(z.read("SOURCE_CHECK.json"))["checksFailed"] == 0
        for row in source_bindings:
            assert z.read(row["packetPath"]) == repository_bytes(ROOT / row["path"])
    prep = {"id": "RANK9-STORM-CONTROL6-CONFERENCE02-PREPARATION-175", "recordedAtUtc": now, "status": "PREPARED_UNSENT", "sourceGitBranch": candidate["sourceGitBranch"], "sourceGitCommit": candidate["sourceGitCommit"], "candidate": bind(CANDIDATE), "archive": bind(ARCHIVE), "check": bind(CHECK), "request": bind(REQUEST), "manifest": bind(OUTPUT / "MANIFEST.json"), "memberCount": len(names), "sourceBindingCount": len(source_bindings), "questionCount": 27, "requiredMainCaseCount": 12, "currentAuthority": AUTH, "reviewIds": IDS}
    write(PREP, enc(prep)); write(OUTPUT / "PREPARATION.json", enc(prep))
    pending_after = {"id": "CURRENT99-PENDING-IDENTITY-AUDIT-175", "recordedAtUtc": now, "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET", "indexBinding": bind(INDEX), "catalogBinding": bind(CATALOG), "authoredCounts": index["authoredCounts"], "pendingCount": 99, "pendingIds": sorted(live_pending), "allPendingExistInSourceCatalog": all(sid in catalog_by for sid in live_pending), "closed335AndCompletedCohortsReopened": False, "acceptedUnapplied": 0}
    write(PENDING_AFTER, enc(pending_after))
    q = copy.deepcopy(queue)
    q.update({"id": "SPELL-REVIEW-QUEUE-175", "recordedAtUtc": now, "packetStatus": "RANK9_STORM_CONTROL6_FRESH_PACKET_PREPARED_UNSENT", "currentAuthority": AUTH, "pendingIdentityAudit": {"path": PENDING_AFTER.name, "pending": 99, "sha256": sha(PENDING_AFTER.read_bytes())}})
    q["currentPendingGroups"][0].update({"candidate": prep["candidate"], "archive": prep["archive"], "freshPacketRequiredForCurrentAuthority": False, "status": "FRESH_PACKET_PREPARED_UNSENT"})
    q["nextGroup"] = "rank9-storm-control6"
    q["next"] = {"group": "rank9-storm-control6", "pendingCount": 6, "candidate": prep["candidate"], "archive": prep["archive"], "freshPacketRequiredForCurrentAuthority": False, "status": "FRESH_PACKET_PREPARED_UNSENT"}
    q["sourceConferencePrepared"] = {"candidate": prep["candidate"], "archive": prep["archive"], "check": prep["check"], "preparation": bind(PREP), "request": bind(REQUEST), "status": "prepared-unsent"}
    write(QUEUE_AFTER, enc(q))
    h = copy.deepcopy(handoff)
    h.update({"id": "CURRENT-HANDOFF-175", "recordedAtUtc": now, "status": "RANK9_STORM_CONTROL6_FRESH_PACKET_PREPARED_UNSENT", "currentQueueBinding": bind(QUEUE_AFTER), "pendingIdentityAudit": {"id": pending_after["id"], "path": PENDING_AFTER.name, "pendingCount": 99, "sha256": sha(PENDING_AFTER.read_bytes())}, "nextGroup": "rank9-storm-control6", "resumePriority": "Publish and submit this exact fresh 749/99 Storm Control6 packet to the GPT director; independently audit the exact return, apply only exact accepted IDs, push that batch, and continue until pending reaches zero.", "nextPreparedRequest": {"group": "rank9-storm-control6", "candidate": prep["candidate"], "archive": prep["archive"], "request": bind(REQUEST), "freshPacketRequiredForCurrentAuthority": False}})
    h["currentIndexBinding"] = bind(INDEX)
    h["currentCatalogBinding"] = bind(CATALOG)
    h["sourceConferencePrepared"] = {"candidate": prep["candidate"], "archive": prep["archive"], "check": prep["check"], "preparation": bind(PREP), "request": bind(REQUEST), "status": "prepared-unsent"}
    h["directorSubmission"] = {"status": "prepared-unsent", "group": "rank9-storm-control6", "reviewIds": IDS, "candidate": prep["candidate"], "archive": prep["archive"], "request": bind(REQUEST)}
    write(HANDOFF_AFTER, enc(h))
    print(json.dumps({"status": "PASS_PREPARED_UNSENT", "candidate": prep["candidate"], "archive": prep["archive"], "checks": len(checks), "sourceBindingCount": len(source_bindings), "archiveMemberCount": len(names), "authority": AUTH, "reviewIds": IDS}, indent=2))


if __name__ == "__main__":
    main()
