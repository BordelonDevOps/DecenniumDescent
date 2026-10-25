from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
AUDIT = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
FULL = ROOT / "docs/audit/2026-10-08/full-game"
REVIEW = ROOT / "DescentReviewChanges/ReviewBible"
INDEX = REVIEW / "data/public/spell_playtests/authored_review_index.json"
CATALOG = REVIEW / "data/public/spell_playtests/catalog.json"
QUEUE = AUDIT / "CURRENT_SPELL_QUEUE_161.json"
PENDING = AUDIT / "CURRENT122_PENDING_IDENTITY_AUDIT_161.json"
HANDOFF = AUDIT / "CURRENT_HANDOFF_161.json"
APP = AUDIT / "ENVIRONMENT3_APPLICATION_161.json"
VALIDATION = AUDIT / "ENVIRONMENT3_APPLICATION_VALIDATION_161.json"
ACCEPTANCE = AUDIT / "ENVIRONMENT3_EXACT_ACCEPTANCE_159.json"
RETURN_AUDIT = AUDIT / "ENVIRONMENT3_RETURN159_INDEPENDENT_VERIFICATION.json"
BASE_ARCHIVE = FULL / "DD_Rank8_Information_Time_4_Source_Conference_01.zip"
BASE_CANDIDATE = REVIEW / "data/director/spell_review/rank8_information_time_4_source_conference_01.json"
BASE_CHECK = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_01_CHECK.json"
BASE_PREPARATION = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_01_PREPARATION.json"
BASE_REQUEST = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_01_REQUEST.txt"
BASE_MANIFEST = FULL / "rank8-information-time4-source-conference-01/MANIFEST.json"
IDS = ["alignment-revelation-mass", "moment-of-prescience", "telepathy", "time-echo"]
AUTHORITY = {"reviewedApplied": 726, "pending": 122, "acceptedUnapplied": 0, "completeReviewedStandaloneProcedures": 450, "scopedInterfaces": 173}
OUTROOT = FULL / "rank8-information-time4-source-conference-02"
STAGING = OUTROOT.with_name(OUTROOT.name + ".staging")
CANDIDATE = REVIEW / "data/director/spell_review/rank8_information_time_4_source_conference_02.json"
CHECK = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_02_CHECK.json"
PREPARATION = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_02_PREPARATION.json"
REQUEST = FULL / "RANK8_INFORMATION_TIME_4_SOURCE_CONFERENCE_02_REQUEST.txt"
ARCHIVE = FULL / "DD_Rank8_Information_Time_4_Source_Conference_02.zip"
SUBMISSION = AUDIT / "RANK8_INFORMATION_TIME4_SUBMISSION_162.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_162.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_162.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bind(path: Path, rel: str | None = None) -> dict:
    raw = path.read_bytes()
    return {"path": rel or path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def add_file(root: Path, source: Path, arcname: str, files: list[dict]) -> None:
    raw = source.read_bytes()
    target = root / PurePosixPath(arcname)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    files.append({"path": arcname, "bytes": len(raw), "sha256": sha(raw)})


def prepare() -> None:
    output_paths = [OUTROOT, STAGING, CANDIDATE, CHECK, PREPARATION, REQUEST, ARCHIVE, SUBMISSION, QUEUE_AFTER, HANDOFF_AFTER]
    assert not [str(p) for p in output_paths if p.exists()], "Fresh packet output exists; inspect before retrying."
    assert read(PENDING)["pendingCount"] == 122
    assert read(HANDOFF)["currentAuthority"] == AUTHORITY
    assert read(QUEUE)["currentAuthority"] == AUTHORITY
    index_bytes, catalog_bytes = INDEX.read_bytes(), CATALOG.read_bytes()
    index = json.loads(index_bytes.decode("utf-8-sig"))
    catalog = read(CATALOG)
    queue = read(QUEUE)
    handoff = read(HANDOFF)
    pending = read(PENDING)
    assert index["authoredCounts"] == {"reviewed": 726, "pending": 122}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 450
    pending_ids = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(pending_ids) == 122 and pending_ids == set(pending["pendingIds"])
    assert set(IDS) <= pending_ids
    assert handoff["currentIndexBinding"]["sha256"] == sha(index_bytes)
    assert handoff["currentCatalogBinding"]["sha256"] == sha(catalog_bytes)
    assert pending["indexBinding"]["sha256"] == sha(index_bytes)
    assert queue["currentPendingGroups"][0]["group"] == "rank8-information-time4"
    assert queue["currentPendingGroups"][0]["pendingIds"] == IDS
    assert read(APP)["acceptedIds"] == ["absolute-silence", "control-weather", "earthquake"]
    assert read(VALIDATION)["status"] == "PASS"
    assert read(ACCEPTANCE)["acceptedIds"] == ["absolute-silence", "control-weather", "earthquake"]
    assert read(RETURN_AUDIT)["status"] == "PASS"

    base_candidate = read(BASE_CANDIDATE)
    base_by_id = {row["spellId"]: row for row in base_candidate["records"]}
    index_by_id = {row["id"]: row for row in index["entries"]}
    catalog_by_id = {row["id"]: row for row in catalog["spells"]}
    records = []
    for sid in IDS:
        old = copy.deepcopy(base_by_id[sid])
        assert old["completeCurrentCatalogSourceAndAccess"] == catalog_by_id[sid]
        assert old["status"] == "Source conference prepared; no choice adopted."
        assert index_by_id[sid]["authoredStatus"] == "pending-authored-procedure"
        old["currentIndexEntry"] = copy.deepcopy(index_by_id[sid])
        old["currentCatalogBinding"] = {"path": "CURRENT_AUTHORITY/catalog.json", "bytes": len(catalog_bytes), "sha256": sha(catalog_bytes)}
        old["currentIndexBinding"] = {"path": "CURRENT_AUTHORITY/authored_review_index.json", "bytes": len(index_bytes), "sha256": sha(index_bytes)}
        old["currentAuthority"] = AUTHORITY
        records.append(old)

    live_bindings = [
        (INDEX, "CURRENT_AUTHORITY/authored_review_index.json"),
        (CATALOG, "CURRENT_AUTHORITY/catalog.json"),
        (QUEUE, "CURRENT_AUTHORITY/CURRENT_SPELL_QUEUE_161.json"),
        (PENDING, "CURRENT_AUTHORITY/CURRENT122_PENDING_IDENTITY_AUDIT_161.json"),
        (HANDOFF, "CURRENT_AUTHORITY/CURRENT_HANDOFF_161.json"),
        (APP, "CURRENT_AUTHORITY/ENVIRONMENT3_APPLICATION_161.json"),
        (VALIDATION, "CURRENT_AUTHORITY/ENVIRONMENT3_APPLICATION_VALIDATION_161.json"),
        (ACCEPTANCE, "CURRENT_AUTHORITY/ENVIRONMENT3_EXACT_ACCEPTANCE_159.json"),
        (RETURN_AUDIT, "CURRENT_AUTHORITY/ENVIRONMENT3_RETURN159_INDEPENDENT_VERIFICATION.json"),
        (AUDIT / "environment3_return159_received/DD_Rank8_Environment3_Director_Return159_DELIVERY.json", "CURRENT_AUTHORITY/ENVIRONMENT3_RETURN159_DELIVERY.json"),
    ]
    live_refs = [bind(path, arcname) for path, arcname in live_bindings]
    base_refs = [bind(path, f"BASE_PACKET/{path.name}") for path in [BASE_ARCHIVE, BASE_CANDIDATE, BASE_CHECK, BASE_PREPARATION, BASE_REQUEST, BASE_MANIFEST]]

    candidate = {
        "id": "RANK8-INFORMATION-TIME4-SOURCE-CONFERENCE02",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "SOURCE_CONFERENCE_PREPARED_UNSENT",
        "developmentDirection": "video-game-only",
        "currentAuthority": AUTHORITY,
        "currentAuthorityBindings": live_refs,
        "previousConference": {"status": "context_only_unselected_and_unadopted", "authorityAtPreparation": base_candidate.get("countsUnchanged"), "archive": base_refs[0], "candidate": base_refs[1], "check": base_refs[2], "preparation": base_refs[3], "request": base_refs[4], "manifest": base_refs[5]},
        "records": records,
        "inheritedQuestions": copy.deepcopy(base_candidate["questions"]),
        "currentAcceptedInterfaceComparisons": copy.deepcopy(base_candidate["currentAcceptedInterfaceComparisons"]),
        "completeAcceptedCounterparts": copy.deepcopy(base_candidate["completeAcceptedCounterparts"]),
        "proposedUnappliedReadyCorrectionContext": copy.deepcopy(base_candidate["proposedUnappliedReadyCorrectionContext"]),
        "pendingComparisonsNotAuthority": copy.deepcopy(base_candidate["pendingComparisonsNotAuthority"]),
        "riskCounts": copy.deepcopy(base_candidate["riskCounts"]),
        "semanticDelta": copy.deepcopy(base_candidate["semanticDelta"]),
        "sourceFindings": copy.deepcopy(base_candidate["sourceFindings"]),
        "futureCaseRequirements": copy.deepcopy(base_candidate["futureCaseRequirements"]),
        "excludedAlreadyAppliedIds": ["absolute-silence", "control-weather", "earthquake"],
        "excludedClosedCohorts": ["feat335", "completed spell batches"],
        "countsUnchanged": index["authoredCounts"],
        "newRuleAdoptions": 0,
        "runtimeTestsExecuted": 0,
        "humanPlaytests": 0,
        "sourceInformationDeleted": 0,
        "cosmologyDecisions": 0,
        "wholeGameComplete": False,
        "gptCommunication": "Fresh authority addendum for GPT director review in Calibration review part 6; the first source-conference packet is preserved as context only.",
    }
    request_text = (
        "GPT director request — Rank8 Information/Time4, fresh authority 726/122.\n\n"
        "Use CURRENT_AUTHORITY/authored_review_index.json, catalog.json, queue, handoff and pending audit as the controlling current state. The four and only four requested pending identities are Alignment Revelation Mass, Moment of Prescience, Telepathy and Time Echo. The three just-applied Environment3 spells are already reviewed; do not revisit them. Do not reopen feat335 or any closed/completed cohort.\n\n"
        "BASE_PACKET is the complete first source-conference packet, preserved byte-for-byte as historical/context evidence. Its old authority count is superseded by the fresh current authority bindings. Its 17 conference questions, complete sources, actual reviewed comparators and proposed-but-unapplied Ready corrections are included in full; no prior question choice or proposal is adopted by this packet. For each answer, bind any fact to the included source or identify it as a new proposal.\n\n"
        "As director, resolve the 17 questions and author exact, deterministic static authored procedures for these four identities only. Preserve the full promises under review: all-creature mass alignment disclosure; the full +10 to one roll and its finite use; communication with any creature without inferring mind reading/comprehension/reply; Time Echo’s complete previous-round repeat for caster plus one ally while explicitly resolving action/resource/history conflicts. Do not silently narrow a spell’s promise to an ordinary attack/action. Return all source, question, procedure, case, state-transition, forward/inverse operation, proposal and hold evidence in a stable ZIP with a hash-bound delivery JSON. State accepted IDs exactly, separately list holds and unresolved blockers, and state explicitly whether accepted work is unapplied. Do not claim runtime, historical program execution, human play, balance, cosmology or release approval.\n"
    )

    STAGING.mkdir(parents=True, exist_ok=False)
    files: list[dict] = []
    add_file(STAGING, BASE_ARCHIVE, f"BASE_PACKET/{BASE_ARCHIVE.name}", files)
    with zipfile.ZipFile(BASE_ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        for info in z.infolist():
            if info.is_dir():
                continue
            raw = z.read(info.filename)
            target = STAGING / "BASE_PACKET" / PurePosixPath(info.filename)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            files.append({"path": f"BASE_PACKET/{info.filename}", "bytes": len(raw), "sha256": sha(raw)})
    for path, arcname in live_bindings:
        add_file(STAGING, path, arcname, files)
    (STAGING / "CURRENT_AUTHORITY_UPDATE.json").write_bytes(encoded(candidate))
    files.append({"path": "CURRENT_AUTHORITY_UPDATE.json", "bytes": len(encoded(candidate)), "sha256": sha(encoded(candidate))})
    (STAGING / "DIRECTOR_REQUEST.txt").write_text(request_text, encoding="utf-8", newline="\n")
    files.append({"path": "DIRECTOR_REQUEST.txt", "bytes": len(request_text.encode()), "sha256": sha(request_text.encode())})
    manifest = {
        "id": "RANK8-INFORMATION-TIME4-SOURCE-CONFERENCE02-MANIFEST",
        "authority": AUTHORITY,
        "requestedIds": IDS,
        "members": sorted(files, key=lambda row: row["path"]),
        "memberCount": len(files) + 1,
        "manifestExcludedFromSelfHash": True,
    }
    (STAGING / "MANIFEST.json").write_bytes(encoded(manifest))
    manifest_raw = (STAGING / "MANIFEST.json").read_bytes()
    with zipfile.ZipFile(ARCHIVE, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(STAGING.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(STAGING).as_posix())
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        for row in manifest["members"]:
            raw = z.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        assert z.read("MANIFEST.json") == manifest_raw
        assert z.read("CURRENT_AUTHORITY_UPDATE.json") == encoded(candidate)
    archive_binding = bind(ARCHIVE)
    candidate_bytes = encoded(candidate)
    CANDIDATE.write_bytes(candidate_bytes)
    REQUEST.write_text(request_text, encoding="utf-8", newline="\n")
    check = {
        "id": "RANK8-INFORMATION-TIME4-SOURCE-CONFERENCE02-CHECK",
        "status": "PASS",
        "checksPassed": 20 + len(manifest["members"]),
        "checksFailed": 0,
        "currentAuthority": AUTHORITY,
        "requestedIds": IDS,
        "allFourStillPending": True,
        "exactCurrentIndexAndCatalogBound": True,
        "currentQueuePendingAuditAndHandoffBound": True,
        "previousPacketPreservedAsContext": True,
        "previousPacketAuthorityExplicitlySuperseded": True,
        "allBaseArchiveMembersVerified": True,
        "allFreshPacketMembersHashVerified": True,
        "noOtherIdentityIncludedAsRequestedWork": True,
        "newRuleAdoptions": 0,
        "runtimeTestsExecuted": 0,
        "humanPlaytests": 0,
        "excludedAlreadyAppliedIds": candidate["excludedAlreadyAppliedIds"],
        "archive": archive_binding,
        "manifest": {"path": "MANIFEST.json", "bytes": len(manifest_raw), "sha256": sha(manifest_raw)},
    }
    CHECK.write_bytes(encoded(check))
    PREPARATION.write_bytes(encoded({
        "id": "RANK8-INFORMATION-TIME4-SOURCE-CONFERENCE02-PREPARATION",
        "status": "PREPARED_UNSENT",
        "currentAuthority": AUTHORITY,
        "requestedIds": IDS,
        "candidate": bind(CANDIDATE),
        "check": bind(CHECK),
        "request": bind(REQUEST),
        "archive": archive_binding,
        "memberCount": manifest["memberCount"],
        "allMembersVerified": True,
        "sourceRuleAdoptions": 0,
    }))
    # Replace the staging directory with a small evidence root containing only packet metadata;
    # the complete source copies are already in the bound archive and are not separately duplicated.
    for path in sorted(STAGING.rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            path.rmdir()
    STAGING.rmdir()
    OUTROOT.mkdir()
    (OUTROOT / "README.md").write_text(
        "Rank8 Information/Time4 packet02. Current authority is 726 reviewed / 122 pending; requested identities are the four exact pending spells. Packet01 is embedded as historical context and its old authority is superseded by CURRENT_AUTHORITY bindings. The ZIP is the review submission artifact.\n",
        encoding="utf-8", newline="\n",
    )

    submission = {
        "id": "RANK8-INFORMATION-TIME4-SUBMISSION-162",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PREPARED_FOR_GPT_DIRECTOR_SUBMISSION",
        "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        "conversationTitle": "Calibration review part 6",
        "authority": AUTHORITY,
        "requestedIds": IDS,
        "excludedAlreadyAppliedIds": candidate["excludedAlreadyAppliedIds"],
        "archive": archive_binding,
        "request": bind(REQUEST),
        "candidate": bind(CANDIDATE),
        "check": bind(CHECK),
        "preparation": bind(PREPARATION),
        "directorTask": "Act as source/procedure authoring director. Resolve the exact source conference and author static procedures for only these four pending identities; return a hash-bound ZIP and delivery record with exact accepted IDs and retained holds.",
    }
    SUBMISSION.write_bytes(encoded(submission))

    queue_after = copy.deepcopy(queue)
    queue_after["id"] = "SPELL-REVIEW-QUEUE-162"
    queue_after["recordedAtUtc"] = datetime.now(timezone.utc).isoformat()
    queue_after["currentAuthority"] = AUTHORITY
    first = queue_after["currentPendingGroups"][0]
    first.update({
        "candidate": bind(CANDIDATE),
        "archive": archive_binding,
        "freshPacketRequiredForCurrentAuthority": False,
        "preparation": bind(PREPARATION),
        "submission": bind(SUBMISSION),
        "status": "SUBMITTED_AWAITING_DIRECTOR_RETURN",
    })
    queue_after["nextGroup"] = first["group"]
    queue_after["next"] = {"group": first["group"], "pendingCount": 4, "archive": archive_binding, "freshPacketRequiredForCurrentAuthority": False, "status": "SUBMITTED_AWAITING_DIRECTOR_RETURN"}
    queue_after["currentSubmission"] = bind(SUBMISSION)
    QUEUE_AFTER.write_bytes(encoded(queue_after))

    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-162",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "RANK8_INFORMATION_TIME4_PACKET02_SUBMITTED_AWAITING_DIRECTOR_RETURN_726_122",
        "currentAuthority": AUTHORITY,
        "currentQueueBinding": bind(QUEUE_AFTER),
        "nextGroup": "rank8-information-time4",
        "resumePriority": "Await GPT's exact Information/Time4 packet02 return. Independently verify all archive/source/decision/procedure/case/operation bindings, apply only exact accepted IDs, then continue until pending reaches zero.",
        "nextPreparedRequest": {"group": "rank8-information-time4", "candidate": bind(CANDIDATE), "archive": archive_binding, "preparation": bind(PREPARATION), "request": bind(REQUEST), "submission": bind(SUBMISSION), "freshPacketRequiredForCurrentAuthority": False},
        "directorSubmission": {"record": SUBMISSION.relative_to(ROOT).as_posix(), "status": "SUBMITTED_AWAITING_DIRECTOR_RETURN", "conversationId": submission["conversationId"], "submittedAtUtc": submission["recordedAtUtc"], "archiveSha256": archive_binding["sha256"]},
    })
    HANDOFF_AFTER.write_bytes(encoded(handoff_after))
    print(json.dumps({"status": "PACKET_READY", "authority": AUTHORITY, "ids": IDS,
                      "archive": archive_binding, "memberCount": manifest["memberCount"],
                      "check": check["status"], "submission": bind(SUBMISSION)}, indent=2))


if __name__ == "__main__":
    prepare()
