from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
REVIEW = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates"
IDS = ["absolute-silence", "control-weather", "earthquake"]

OLD_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_environment_3_source_conference_01.json"
OLD_ARCHIVE = FULL / "DD_Rank8_Environment_3_Source_Conference_01.zip"
OLD_CHECK = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_01_CHECK.json"
OLD_PREPARATION = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_01_PREPARATION.json"
OLD_NOTES = AUDIT / "RANK8ENVIRONMENT3_NEXT_CONFERENCE_NOTES_129.json"

INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_158.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_158.json"
PENDING_BEFORE = AUDIT / "CURRENT125_PENDING_IDENTITY_AUDIT_158.json"
REGISTRY = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"

CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_environment_3_source_conference_02.json"
OUTPUT = FULL / "rank8-environment3-source-conference-02"
ARCHIVE = FULL / "DD_Rank8_Environment_3_Source_Conference_02.zip"
CHECK = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_CHECK.json"
PREPARATION = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_PREPARATION.json"
REQUEST = FULL / "RANK8_ENVIRONMENT_3_SOURCE_CONFERENCE_02_REQUEST.txt"
NOTES = AUDIT / "RANK8ENVIRONMENT3_NEXT_CONFERENCE_NOTES_159.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_159.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_159.json"


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def pointer_get(value: Any, pointer: str) -> Any:
    assert pointer.startswith("/")
    result = value
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        result = result[int(token)] if isinstance(result, list) else result[token]
    return result


def spells_by_id(model: dict) -> dict:
    spells = model["spells"]
    return spells if isinstance(spells, dict) else {row["id"]: row for row in spells}


def validate_archive(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)), f"duplicate ZIP member in {path}"
        assert archive.testzip() is None, f"CRC failure in {path}"
        return names


def main() -> None:
    outputs = [CANDIDATE, OUTPUT, ARCHIVE, CHECK, PREPARATION, REQUEST, NOTES, QUEUE_AFTER, HANDOFF_AFTER]
    existing = [str(path) for path in outputs if path.exists()]
    assert not existing, f"Conference02 outputs already exist; inspect before retry: {existing}"

    old_check = read(OLD_CHECK)
    old_prep = read(OLD_PREPARATION)
    old_notes = read(OLD_NOTES)
    old_local_candidate_raw = OLD_CANDIDATE.read_bytes()
    index = read(INDEX)
    catalog = read(CATALOG)
    registry = read(REGISTRY)
    queue = read(QUEUE_BEFORE)
    handoff = read(HANDOFF_BEFORE)
    pending = read(PENDING_BEFORE)

    assert old_check["failures"] == 0 and old_prep["status"] == "PREPARED_UNSENT"
    assert index["authoredCounts"] == {"reviewed": 723, "pending": 125}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 447
    assert queue["currentAuthority"] == {
        "reviewedApplied": 723, "pending": 125, "acceptedUnapplied": 0,
        "completeReviewedStandaloneProcedures": 447, "scopedInterfaces": 173,
    }
    assert handoff["currentAuthority"] == queue["currentAuthority"]
    assert pending["pendingCount"] == 125
    assert pending["indexBinding"]["sha256"] == binding(INDEX)["sha256"]
    assert handoff["currentIndexBinding"]["sha256"] == binding(INDEX)["sha256"]
    assert handoff["currentCatalogBinding"]["sha256"] == binding(CATALOG)["sha256"]
    first = queue["currentPendingGroups"][0]
    assert first["group"] == "rank8-environment3" and first["pendingIds"] == IDS
    live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == 125 and set(pending["pendingIds"]) == live_pending
    entries = {row["id"]: row for row in index["entries"]}
    catalog_spells = {row["id"]: row for row in catalog["spells"]}
    assert all(sid in live_pending for sid in IDS)

    old_archive_raw = OLD_ARCHIVE.read_bytes()
    assert len(old_archive_raw) == old_prep["archive"]["bytes"]
    assert sha(old_archive_raw) == old_prep["archive"]["sha256"]
    with zipfile.ZipFile(OLD_ARCHIVE) as archive:
        assert archive.testzip() is None
        old_candidate_raw = archive.read("CANDIDATE.json")
        old_archived_check = archive.read("SOURCE_CHECK.json")
        old_manifest = json.loads(archive.read("MANIFEST.json"))
        assert len(old_candidate_raw) == old_prep["candidate"]["bytes"]
        assert sha(old_candidate_raw) == old_prep["candidate"]["sha256"]
        assert json.loads(old_archived_check)["failures"] == 0
        old = json.loads(old_candidate_raw.decode("utf-8-sig"))
        assert old["status"] == "SOURCE_CONFERENCE_PREPARED_UNSENT"
        for row in old["sourceBindings"]:
            raw = archive.read("sources/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
    assert old_manifest["candidate"]["sha256"] == old_prep["candidate"]["sha256"]

    # The historical 13 questions and two focused additions remain unselected.
    original_questions = copy.deepcopy(old["questions"])
    focused_questions = copy.deepcopy(old_notes["focusedAdditionalQuestions"])
    questions = original_questions + focused_questions
    assert len(original_questions) == 13 and len(focused_questions) == 2
    assert len(questions) == len({row["id"] for row in questions}) == 15
    assert all(row["decisionSelected"] is False for row in questions)
    assert set().union(*(set(row["spellIds"]) for row in questions)) == set(IDS)

    now = datetime.now(timezone.utc).isoformat()
    candidate = copy.deepcopy(old)
    candidate.update({
        "id": "RANK8-ENVIRONMENT3-SOURCE-CONFERENCE02-159",
        "recordedAtUtc": now,
        "status": "SOURCE_CONFERENCE_PREPARED_UNSENT",
        "priorConferenceSupersededBy": "This Conference02 packet is freshly bound to current 723 reviewed / 125 pending / 0 accepted-unapplied authority. Conference01 remains historical 525/323 evidence only and cannot authorize current acceptance or application.",
        "currentAuthority": {
            "reviewedApplied": 723,
            "pending": 125,
            "acceptedUnapplied": 0,
            "completeReviewedStandaloneProcedures": 447,
            "index": binding(INDEX),
            "catalog": binding(CATALOG),
            "currentQueue": binding(QUEUE_BEFORE),
            "pendingIdentityAudit": binding(PENDING_BEFORE),
            "priorHandoff": binding(HANDOFF_BEFORE),
        },
        "countsUnchanged": {"reviewed": 723, "pending": 125},
        "conference01QuestionSetPreserved": {"questions": original_questions, "questionCount": 13, "allStillUnselected": True},
        "conference02Questions": questions,
        "focusedAdditionalQuestions": focused_questions,
        "questions": questions,
        "historicalPendingComparisonsNowReviewed": [],
        "pendingComparisonsNotAuthority": [],
        "recentExactAcceptedAppliedComparisons": [],
        "sourceInformationDeleted": 0,
        "gptCommunication": "Fresh Rank8 Environment3 source conference for current authority 723 applied-reviewed / 125 pending / 0 accepted-unapplied. Review only absolute-silence, control-weather, and earthquake. Preserve 13 original source questions and two focused follow-ups unselected. Do not reopen any completed feat or spell cohort.",
        "nonAcceptanceOfLaterSourceChanges": "Current source files in this packet are bound current context only. A changed backing source or procedure does not promote later edits into a previously accepted scope. Preserve each exact acceptance/application receipt as the boundary; do not reopen accepted identities.",
        "newRuleAdoptions": 0,
        "runtimeTestsExecuted": 0,
        "humanPlaytests": 0,
        "cosmologyDecisions": 0,
        "wholeGameComplete": False,
    })

    for record in candidate["records"]:
        sid = record["spellId"]
        assert sid in IDS
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(catalog_spells[sid])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
        record["currentAuthorityStatus"] = "pending-authored-procedure at current 723/125 authority"

    # Preserve Conference01 comparisons as history while resolving each against the live index.
    for group in old.get("pendingComparisonsNotAuthority", []):
        ids = list(group["identities"])
        reviewed_ids = [sid for sid in ids if entries[sid]["authoredStatus"] == "reviewed-authored-operational-playtest"]
        still_pending = [sid for sid in ids if entries[sid]["authoredStatus"] == "pending-authored-procedure"]
        if reviewed_ids:
            candidate["historicalPendingComparisonsNowReviewed"].append({
                "historicalGroup": copy.deepcopy(group),
                "currentReviewedIds": reviewed_ids,
                "stillPendingIds": still_pending,
                "currentIndexEntries": [copy.deepcopy(entries[sid]) for sid in reviewed_ids + still_pending],
                "qualification": "Historical comparison only; current status comes from exact live 723/125 authority and exact acceptance/application records. This group cannot replace the first pending group.",
            })
        if still_pending:
            candidate["pendingComparisonsNotAuthority"].append({
                **copy.deepcopy(group),
                "currentPendingIds": still_pending,
                "qualification": "Historical source comparison, not a current review packet or acceptance. Use only a fresh packet bound to current authority.",
            })

    # Refresh accepted interface snapshots without reopening or broadening them.
    current_interfaces = []
    for item in old["currentAcceptedInterfaceComparisons"]:
        pointer = item["registryPointer"]
        current_interfaces.append({
            "registryPointer": pointer,
            "completeCurrentEntry": copy.deepcopy(pointer_get(registry, pointer)),
            "historicalConference01Entry": copy.deepcopy(item["completeEntryUnchanged"]),
            "scope": "Current interface reference only. It does not reopen, extend or replace an exact accepted procedure scope.",
        })
    candidate["currentAcceptedInterfaceComparisons"] = current_interfaces

    # Refresh fully accepted counterpart spell procedures from their exact current reviewed models.
    current_counterparts = []
    for item in old["completeAcceptedCounterparts"]:
        sid = item["spellId"]
        entry = entries[sid]
        model_path = (INDEX.parent / entry["procedureFile"]).resolve()
        model = read(model_path)
        procedure_pointer = entry.get("wholeCardPointer", entry.get("procedurePointer", item["pointer"]))
        current_counterparts.append({
            "spellId": sid,
            "model": binding(model_path),
            "pointer": procedure_pointer,
            "completeCurrentCard": copy.deepcopy(pointer_get(model, procedure_pointer)),
            "currentIndexEntry": copy.deepcopy(entry),
            "historicalConference01Card": copy.deepcopy(item["completeCurrentCard"]),
            "scope": "Exact source-specific reviewed comparison only; preserve its accepted and applied boundary, with no automatic adoption for Environment3.",
        })
    candidate["completeAcceptedCounterparts"] = current_counterparts

    # Include complete procedures for previously pending source-comparison groups that are now reviewed.
    for item in candidate["historicalPendingComparisonsNowReviewed"]:
        for sid in item["currentReviewedIds"]:
            entry = entries[sid]
            model_path = (INDEX.parent / entry["procedureFile"]).resolve()
            model = read(model_path)
            pointer = entry.get("wholeCardPointer", entry.get("procedurePointer"))
            item.setdefault("completeCurrentProcedures", []).append({
                "spellId": sid,
                "model": binding(model_path),
                "pointer": pointer,
                "completeProcedure": copy.deepcopy(pointer_get(model, pointer)),
                "currentIndexEntry": copy.deepcopy(entry),
                "scope": "Current exact authored procedure used only as a bounded comparison; its prior cohort is closed.",
            })

    # Bind the most recent exact applied batch, which establishes the current 718 -> 723 transition.
    perception_model_path = REVIEW / "rank8perception5_reviewed_156" / "MODEL.json"
    perception_model = read(perception_model_path)
    perception_spells = spells_by_id(perception_model)
    perception_ids = ["mass-hallucination", "illusory-dragon", "phantom-execution", "antipathy-sympathy", "glibness"]
    perception_receipt = AUDIT / "PERCEPTION5_EXACT_ACCEPTANCE_156.json"
    perception_application = AUDIT / "PERCEPTION5_APPLICATION_158.json"
    perception_decision = AUDIT / "GPT_DIRECTOR_DECISION_PERCEPTION5_156.json"
    perception_delivery = AUDIT / "perception5_return156_received" / "DIRECTOR_RETURN_DELIVERY.json"
    perception_postcheck = AUDIT / "PERCEPTION5_APPLICATION_VERIFICATION_158.json"
    assert read(perception_receipt)["acceptedIds"] == perception_ids
    assert read(perception_application)["acceptedIds"] == perception_ids
    assert read(perception_decision)["acceptedIds"] == perception_ids
    assert read(perception_delivery)["acceptedIds"] == perception_ids
    assert read(perception_delivery)["accepted"] is True and read(perception_delivery)["applied"] is False
    assert all(entries[sid]["authoredStatus"] == "reviewed-authored-operational-playtest" for sid in perception_ids)
    candidate["recentExactAcceptedAppliedComparisons"] = [{
        "batch": "rank8-perception5-reviewed-156-applied-158",
        "acceptedIds": perception_ids,
        "procedures": [
            {
                "spellId": sid,
                "completeAcceptedProcedure": copy.deepcopy(perception_spells[sid]),
                "currentIndexEntry": copy.deepcopy(entries[sid]),
            }
            for sid in perception_ids
        ],
        "bindings": [binding(path) for path in [
            perception_model_path,
            REVIEW / "rank8perception5_reviewed_156" / "CANDIDATE_PACKAGE_MANIFEST.json",
            perception_receipt,
            perception_application,
            perception_decision,
            perception_delivery,
            perception_postcheck,
        ]],
        "scope": "Exact accepted and applied authored comparison only; all recorded holds remain, with no runtime, human-play, balance, cosmology, completeness or release approval.",
    }]

    # Freeze each original source binding again at current bytes and include current authority and exact comparisons.
    source_paths = {row["path"] for row in old["sourceBindings"]}
    required_paths = [INDEX, CATALOG, QUEUE_BEFORE, HANDOFF_BEFORE, PENDING_BEFORE, REGISTRY,
                      CANDIDATE]
    source_paths.update(path.relative_to(ROOT).as_posix() for path in required_paths if path != CANDIDATE)
    comparison_paths = [
        perception_model_path,
        REVIEW / "rank8perception5_reviewed_156" / "CANDIDATE_PACKAGE_MANIFEST.json",
        perception_receipt, perception_application, perception_decision, perception_delivery, perception_postcheck,
    ]
    for item in current_counterparts:
        comparison_paths.append(ROOT / item["model"]["path"])
    for group in candidate["historicalPendingComparisonsNowReviewed"]:
        for procedure in group.get("completeCurrentProcedures", []):
            comparison_paths.append(ROOT / procedure["model"]["path"])
    for path in comparison_paths:
        source_paths.add(path.relative_to(ROOT).as_posix())

    source_rows = []
    historical = {row["path"]: row for row in old["sourceBindings"]}
    source_deltas = []
    for relative in sorted(source_paths):
        path = ROOT / Path(*relative.split("/"))
        assert path.is_file(), f"missing bound source: {relative}"
        row = binding(path)
        source_rows.append(row)
        previous = historical.get(relative)
        if previous and (previous["bytes"], previous["sha256"]) != (row["bytes"], row["sha256"]):
            source_deltas.append({
                "path": relative,
                "conference01Binding": {"bytes": previous["bytes"], "sha256": previous["sha256"]},
                "currentBinding": row,
                "scope": "Current source context only; a changed current file does not alter any prior exact acceptance boundary.",
            })
    candidate["sourceBindings"] = source_rows
    candidate["historicalSourceBindingDeltas"] = source_deltas
    candidate["sourceBindingCounts"] = {
        "currentFiles": len(source_rows),
        "historicalChangedFilesExplicitlyRecorded": len(source_deltas),
    }

    # Build a fresh frozen source set plus explicitly historical conference evidence.
    OUTPUT.mkdir(parents=True)
    frozen = []
    for row in source_rows:
        src = ROOT / Path(*row["path"].split("/"))
        dst = OUTPUT / "sources" / Path(*row["path"].split("/"))
        dst.parent.mkdir(parents=True, exist_ok=True)
        raw = src.read_bytes()
        assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        dst.write_bytes(raw)
        assert dst.read_bytes() == raw
        frozen.append({**row, "frozenCopy": dst.relative_to(ROOT).as_posix()})
    historical_dir = OUTPUT / "historical"
    historical_dir.mkdir()
    historical_files = {
        "Conference01_CANDIDATE.json": old_candidate_raw,
        "Conference01_ARCHIVE.zip": old_archive_raw,
        "Conference01_CHECK.json": OLD_CHECK.read_bytes(),
        "Conference01_PREPARATION.json": OLD_PREPARATION.read_bytes(),
        "Conference01_NEXT_NOTES.json": OLD_NOTES.read_bytes(),
        "Conference01_CURRENT_LOCAL_WORKING_COPY_NOT_AUTHORITY.json": old_local_candidate_raw,
    }
    for name, raw in historical_files.items():
        (historical_dir / name).write_bytes(raw)

    checks: list[dict] = []
    def ck(label: str, passed: bool) -> None:
        checks.append({"check": label, "passed": bool(passed)})
        assert passed, label

    ck("Current authored authority is exactly 723 reviewed and 125 pending", index["authoredCounts"] == {"reviewed": 723, "pending": 125})
    ck("Current complete standalone authored procedures equals 447", index["representationCounts"]["completeReviewedStandaloneProcedures"] == 447)
    ck("Queue and handoff both bind 723/125/0 authority", queue["currentAuthority"] == handoff["currentAuthority"] and queue["currentAuthority"]["acceptedUnapplied"] == 0)
    ck("Current pending identity audit equals exact live pending index set", set(pending["pendingIds"]) == live_pending and len(live_pending) == 125)
    ck("Environment3 is the exact first live pending group", first["group"] == "rank8-environment3" and first["pendingIds"] == IDS)
    ck("Only the three exact target identities are in scope", [row["spellId"] for row in candidate["records"]] == IDS)
    ck("All 13 historical plus two focused questions are retained and unselected", len(questions) == 15 and len({row["id"] for row in questions}) == 15 and all(row["decisionSelected"] is False for row in questions))
    ck("All 15 questions cover the three target identities", set().union(*(set(row["spellIds"]) for row in questions)) == set(IDS))
    ck("Current native source/access rows match the live catalog", all(next(row for row in candidate["records"] if row["spellId"] == sid)["completeCurrentCatalogSourceAndAccess"] == catalog_spells[sid] for sid in IDS))
    ck("All three targets are pending with no prior accepted procedure", all(entries[sid]["authoredStatus"] == "pending-authored-procedure" for sid in IDS))
    ck("Conference01 is retained as historical 525/323 only", old["countsUnchanged"] == {"reviewed": 525, "pending": 323} and len(old_archive_raw) == old_prep["archive"]["bytes"])
    ck("Last completed Perception5 batch is accepted, applied, and exactly five identities", len(candidate["recentExactAcceptedAppliedComparisons"][0]["procedures"]) == 5 and read(perception_application)["acceptedIds"] == perception_ids)
    ck("No feat or completed cohort is in target scope", not set(IDS).intersection({"feat335", "erase-mind", "feeblemind", "mass-dominate", "mind-ravel"}))
    ck("Current authority, live counterparts and exact recent application sources are frozen", all((OUTPUT / "sources" / Path(*row["path"].split("/"))).read_bytes() == (ROOT / Path(*row["path"].split("/"))).read_bytes() for row in source_rows))
    ck("All preserved prior source/case obligations remain", len(old["sourceFindings"]) >= 8 and len(old_notes["requiredNewCases"]) == 6)
    ck("No canonical index/catalog edit is part of packet preparation", binding(INDEX)["sha256"] == handoff["currentIndexBinding"]["sha256"] and binding(CATALOG)["sha256"] == handoff["currentCatalogBinding"]["sha256"])
    ck("Preparation does not adopt rules or claim runtime/playtest/cosmology/release completion", candidate["newRuleAdoptions"] == candidate["runtimeTestsExecuted"] == candidate["humanPlaytests"] == candidate["cosmologyDecisions"] == 0 and candidate["wholeGameComplete"] is False)

    candidate_bytes = encode(candidate)
    CANDIDATE.write_bytes(candidate_bytes)
    candidate_binding = binding(CANDIDATE)
    readme = (
        "Fresh Rank8 Environment3 Conference02, bound to 723 reviewed / 125 pending / 0 accepted-unapplied. "
        "Three exact pending identities, 13 original questions plus two focused follow-ups, current queue/handoff/index/catalog, "
        f"{len(source_rows)} frozen source bindings, closed reviewed comparisons, and Conference01 preserved only as historical 525/323 evidence. "
        "Preparation only; no procedure or rule is adopted.\n"
    ).encode("utf-8")
    (OUTPUT / "README.md").write_bytes(readme)
    check_doc = {
        "id": "RANK8-ENVIRONMENT3-SOURCE-CHECK-159",
        "status": "PASS",
        "candidate": candidate_binding,
        "checks": checks,
        "checkCount": len(checks),
        "failures": 0,
        "sourceCount": len(source_rows),
        "historicalSourceDeltas": len(source_deltas),
        "sourceAuthority": {"reviewedApplied": 723, "pending": 125, "acceptedUnapplied": 0},
        "targetIds": IDS,
        "originalQuestions": 13,
        "focusedQuestions": 2,
        "totalQuestions": 15,
        "historicalConference01Retained": True,
        "newRuleAdoptions": 0,
        "runtimeTestsExecuted": 0,
    }
    write(CHECK, check_doc)
    manifest = {
        "id": "RANK8-ENVIRONMENT3-SOURCE-CONFERENCE02-MANIFEST-159",
        "candidate": candidate_binding,
        "check": binding(CHECK),
        "sourceCount": len(source_rows),
        "frozenSources": frozen,
        "historicalConference01Archive": {"path": "historical/Conference01_ARCHIVE.zip", "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)},
        "sourceAuthority": candidate["currentAuthority"],
        "closedComparisonCohorts": [row["historicalGroup"].get("group") for row in candidate["historicalPendingComparisonsNowReviewed"]],
    }
    write(OUTPUT / "MANIFEST.json", manifest)
    request_text = (
        f"GPT — please review the exact fresh {ARCHIVE.name} source-conference packet against current authority 723 applied-reviewed / 125 pending / 0 accepted-unapplied.\n\n"
        f"Review only {', '.join(IDS)}. Resolve all 15 unselected questions and the six complete case obligations. The packet includes the exact current queue, pending identity audit, handoff, index/catalog/native access rows, {len(source_rows)} frozen source bindings, exact current reviewed comparison procedures, the latest applied Perception5 batch, and Conference01 only as historical 525/323 material.\n\n"
        "Preserve every source, access, content, lifecycle, information, structure, runtime, balance, cosmology, and release hold. Keep the actual class-school access differences, concentration and duration clocks, source-root/provenance rules, actual geometry, matter and support prerequisites, and physical aftermath explicit. Do not infer execution from authored fixtures.\n\n"
        "Return source-faithful complete procedures, all question and case dispositions, a complete hold register, and your independent failure check. If the exact package passes, state accepted=true and applied=false only for the exact accepted IDs. If it fails, keep every identity unaccepted and unapplied and list exact blockers. Do not edit canonical files, reopen feat335, or redo any completed/applied spell cohort. Keep runtime, human-play, balance, cosmology, and release qualifications explicit.\n"
    )
    REQUEST.write_text(request_text, encoding="utf-8", newline="\n")
    (OUTPUT / "CONFERENCE_NOTES.json").write_bytes(encode({
        "id": "RANK8ENVIRONMENT3-INDEPENDENT-CONFERENCE-159",
        "status": "PREPARED_UNSENT_NOT_ACCEPTED",
        "identities": IDS,
        "currentAppliedCounts": {"reviewed": 723, "pending": 125, "acceptedUnapplied": 0},
        "completeOriginalQuestionsUnchanged": original_questions,
        "focusedAdditionalQuestions": focused_questions,
        "allQuestions": questions,
        "requiredNewCases": copy.deepcopy(old_notes["requiredNewCases"]),
        "historicalComparisons": candidate["historicalPendingComparisonsNowReviewed"],
        "sourceChecks": source_rows,
        "scope": "Preparation only. No new procedure or rule adopted; no program execution or runtime, human-play, balance, cosmology or release claim.",
    }))

    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(CANDIDATE, "CANDIDATE.json")
        archive.write(CHECK, "SOURCE_CHECK.json")
        archive.write(OUTPUT / "MANIFEST.json", "MANIFEST.json")
        archive.write(OUTPUT / "README.md", "README.md")
        archive.write(OUTPUT / "CONFERENCE_NOTES.json", "CONFERENCE_NOTES.json")
        archive.write(REQUEST, "REQUEST.txt")
        for name in historical_files:
            archive.write(historical_dir / name, "historical/" + name)
        for row in frozen:
            archive.write(OUTPUT / "sources" / Path(*row["path"].split("/")), "sources/" + row["path"])

    archive_names = validate_archive(ARCHIVE)
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.read("CANDIDATE.json") == candidate_bytes
        assert json.loads(archive.read("SOURCE_CHECK.json"))["failures"] == 0
        assert archive.read("historical/Conference01_ARCHIVE.zip") == old_archive_raw
        for row in frozen:
            raw = archive.read("sources/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]

    prep = {
        "id": "RANK8-ENVIRONMENT3-SOURCE-CONFERENCE02-PREPARATION-159",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "PREPARED_UNSENT",
        "candidate": candidate_binding,
        "archive": binding(ARCHIVE),
        "manifest": binding(OUTPUT / "MANIFEST.json"),
        "check": binding(CHECK),
        "request": binding(REQUEST),
        "sourceCount": len(source_rows),
        "identityCount": len(IDS),
        "questionCount": len(questions),
        "historicalDeltas": len(source_deltas),
        "archiveMemberCount": len(archive_names),
        "allArchiveMembersVerified": True,
        "sourceAuthority": {"reviewedApplied": 723, "pending": 125, "acceptedUnapplied": 0},
        "nextGroup": first["group"],
        "canonicalIndexOrCatalogModified": False,
    }
    write(PREPARATION, prep)

    queue_after = copy.deepcopy(queue)
    queue_after["currentPendingGroups"][0].update({
        "candidate": candidate_binding,
        "archive": binding(ARCHIVE),
        "preparation": binding(PREPARATION),
        "freshPacketRequiredForCurrentAuthority": False,
    })
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-159",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "packetStatus": "RANK8_ENVIRONMENT3_CONFERENCE02_PREPARED_UNSENT_723_125",
        "sourceConferencePrepared": {
            "group": first["group"], "candidate": candidate_binding,
            "archive": binding(ARCHIVE), "preparation": binding(PREPARATION), "status": "PREPARED_UNSENT",
        },
        "directorSubmission": {
            "record": "docs/audit/2026-10-08/full-game/director-spell-review-129/PERCEPTION5_SUBMISSION_157.json",
            "status": "RETURN_RECEIVED_AND_APPLIED",
            "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
            "applicationReceipt": "docs/audit/2026-10-08/full-game/director-spell-review-129/PERCEPTION5_APPLICATION_158.json",
        },
    })
    write(QUEUE_AFTER, queue_after)

    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-159",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "RANK8_ENVIRONMENT3_PACKET02_PREPARED_UNSENT_723_125",
        "currentQueueBinding": binding(QUEUE_AFTER),
        "nextGroup": first["group"],
        "nextPreparedRequest": {
            "group": first["group"],
            "candidate": candidate_binding,
            "archive": binding(ARCHIVE),
            "preparation": binding(PREPARATION),
            "request": binding(REQUEST),
            "freshPacketRequiredForCurrentAuthority": False,
            "status": "prepared-unsent",
        },
        "resumePriority": "Publish and submit the exact Rank8 Environment3 Conference02 packet bound to current 723/125 authority to Calibration review part6; independently audit the exact return, apply only accepted IDs, then continue with the current queue's first pending group until pending reaches zero.",
        "directorSubmission": {
            "priorSubmission": "PERCEPTION5_SUBMISSION_157",
            "priorStatus": "RETURN_RECEIVED_AND_APPLIED",
            "nextStatus": "PREPARED_UNSENT",
            "conversationId": "6adc506d-8770-83ea-b64c-0345d9b9b682",
        },
    })
    write(HANDOFF_AFTER, handoff_after)

    print(json.dumps({
        "status": "PREPARATION_PASS",
        "candidate": candidate_binding,
        "archive": binding(ARCHIVE),
        "request": binding(REQUEST),
        "checkCount": len(checks),
        "sources": len(source_rows),
        "historicalDeltas": len(source_deltas),
        "questions": len(questions),
        "members": len(archive_names),
        "authority": {"reviewed": 723, "pending": 125, "acceptedUnapplied": 0},
        "next": first["group"],
    }, indent=2))


if __name__ == "__main__":
    main()
