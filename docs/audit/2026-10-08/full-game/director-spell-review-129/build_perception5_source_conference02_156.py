from __future__ import annotations

import copy
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/audit/2026-10-08/full-game"
AUDIT = FULL / "director-spell-review-129"
IDS = ["mass-hallucination", "illusory-dragon", "phantom-execution", "antipathy-sympathy", "glibness"]
OLD_CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_perception_5_source_conference_01.json"
OLD_ARCHIVE = FULL / "DD_Rank8_Perception_5_Source_Conference_01.zip"
OLD_CHECK = FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_01_CHECK.json"
OLD_PREPARATION = FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_01_PREPARATION.json"
OLD_NOTES = AUDIT / "RANK8PERCEPTION5_NEXT_CONFERENCE_NOTES_129.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
REGISTRY = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json"
QUEUE_BEFORE = AUDIT / "CURRENT_SPELL_QUEUE_155.json"
HANDOFF_BEFORE = AUDIT / "CURRENT_HANDOFF_155.json"
PENDING_BEFORE = AUDIT / "CURRENT130_PENDING_IDENTITY_AUDIT_155.json"
CANDIDATE = ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_perception_5_source_conference_02.json"
OUT = FULL / "rank8-perception5-source-conference-02"
ARCHIVE = FULL / "DD_Rank8_Perception_5_Source_Conference_02.zip"
CHECK = FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_CHECK.json"
PREPARATION = FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_PREPARATION.json"
REQUEST = FULL / "RANK8_PERCEPTION_5_SOURCE_CONFERENCE_02_REQUEST.txt"
NOTES = AUDIT / "RANK8PERCEPTION5_NEXT_CONFERENCE_NOTES_156.json"
QUEUE_AFTER = AUDIT / "CURRENT_SPELL_QUEUE_156.json"
HANDOFF_AFTER = AUDIT / "CURRENT_HANDOFF_156.json"
REVIEW_DIR = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates"
COMPARISON_BATCHES = [
    {
        "name": "rank8-control5", "folder": "rank8control5_reviewed_148",
        "receipt": "RANK8_CONTROL5_EXACT_ACCEPTANCE_148.json", "application": "RANK8_CONTROL5_APPLICATION_148.json",
        "decision": "GPT_DIRECTOR_DECISION_RANK8_CONTROL5_148.json", "deliveryFolder": "rank8control5_return148_received",
        "ids": ["frozen-time-prism", "paralyzing-presence", "power-word-stun", "mental-collapse", "reality-rewrite"],
    },
    {
        "name": "rank8-ward5", "folder": "rank8ward5_reviewed_149",
        "receipt": "RANK8_WARD5_EXACT_ACCEPTANCE_149.json", "application": "RANK8_WARD5_APPLICATION_149.json",
        "decision": "GPT_DIRECTOR_DECISION_RANK8_WARD5_149.json", "deliveryFolder": "rank8ward5_return149_received",
        "ids": ["alignment-immunity", "antilife-shell", "antimagic-field", "mind-blank", "reputation-fortress"],
    },
    {
        "name": "rank8-memorycontrol4", "folder": "rank8memorycontrol4_reviewed_150",
        "receipt": "MEMORY_CONTROL4_EXACT_ACCEPTANCE_150.json", "application": "MEMORY_CONTROL4_APPLICATION_150.json",
        "decision": "GPT_DIRECTOR_DECISION_MEMORY_CONTROL4_150.json", "deliveryFolder": "rank8memorycontrol4_return150_received",
        "ids": ["erase-mind", "feeblemind", "mass-dominate", "mind-ravel"],
    },
    {
        "name": "rank8lifeform4", "folder": "rank8lifeform4_reviewed_151",
        "receipt": "LIFE_FORM4_EXACT_ACCEPTANCE_151.json", "application": "LIFE_FORM4_APPLICATION_151.json",
        "decision": "GPT_DIRECTOR_DECISION_LIFE_FORM4_151.json", "deliveryFolder": "rank8lifeform4_return151_received",
        "ids": ["animal-shapes", "clone", "flesh-to-grave", "perfect-form"],
    },
    {
        "name": "rank8summonstructure5", "folder": "rank8summonstructure5_reviewed_153",
        "receipt": "SUMMON_STRUCTURE5_EXACT_ACCEPTANCE_153.json", "application": "SUMMON_STRUCTURE5_APPLICATION_153.json",
        "decision": "GPT_DIRECTOR_DECISION_SUMMON_STRUCTURE5_153.json", "deliveryFolder": "summonstructure5_return153_received",
        "ids": ["summon-greater-water-pet", "summon-archlich-shade", "faction-paragon", "conjure-sky-fortress", "shifting-fortress"],
    },
]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def binding(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw)}


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def model_spells_by_id(model: dict) -> dict:
    spells = model["spells"]
    return spells if isinstance(spells, dict) else {row["id"]: row for row in spells}


def main() -> None:
    outputs = [CANDIDATE, ARCHIVE, CHECK, PREPARATION, REQUEST, NOTES, QUEUE_AFTER, HANDOFF_AFTER]
    existing = [str(path) for path in outputs if path.exists()]
    assert "--rebuild" in sys.argv or not existing, f"Conference02 output already exists; inspect before retry: {existing}"
    assert not OUT.exists() or (OUT.is_dir() and not OUT.is_symlink()), "Unexpected source staging output; inspect before retry."

    old_prep = read(OLD_PREPARATION)
    old_notes = read(OLD_NOTES)
    index = read(INDEX)
    catalog = read(CATALOG)
    registry = read(REGISTRY)
    queue = read(QUEUE_BEFORE)
    handoff = read(HANDOFF_BEFORE)
    pending = read(PENDING_BEFORE)
    assert old_prep["status"] == "PREPARED_UNSENT"
    assert index["authoredCounts"] == {"reviewed": 718, "pending": 130}
    assert index["representationCounts"]["completeReviewedStandaloneProcedures"] == 442
    assert queue["currentAuthority"]["reviewedApplied"] == 718 and queue["currentAuthority"]["pending"] == 130
    assert pending["pendingCount"] == 130 and pending["indexBinding"]["sha256"] == binding(INDEX)["sha256"]
    assert handoff["currentIndexBinding"]["sha256"] == binding(INDEX)["sha256"]
    assert handoff["currentCatalogBinding"]["sha256"] == binding(CATALOG)["sha256"]
    first = queue["currentPendingGroups"][0]
    assert first["group"] == "rank8-perception5" and first["pendingIds"] == IDS
    live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(live_pending) == 130 and set(pending["pendingIds"]) == live_pending
    entries = {row["id"]: row for row in index["entries"]}
    catalog_spells = {row["id"]: row for row in catalog["spells"]}
    assert all(sid in live_pending for sid in IDS)

    old_archive_raw = OLD_ARCHIVE.read_bytes()
    old_local_candidate_raw = OLD_CANDIDATE.read_bytes()
    assert len(old_archive_raw) == old_prep["archive"]["bytes"]
    assert sha(old_archive_raw) == old_prep["archive"]["sha256"]
    with zipfile.ZipFile(OLD_ARCHIVE) as old_zip:
        old_candidate_raw = old_zip.read("CANDIDATE.json")
        old_check_raw = old_zip.read("SOURCE_CHECK.json")
    assert len(old_candidate_raw) == old_prep["candidate"]["bytes"]
    assert sha(old_candidate_raw) == old_prep["candidate"]["sha256"]
    assert len(old_check_raw) == old_prep["check"]["bytes"]
    assert sha(old_check_raw) == old_prep["check"]["sha256"]
    old = json.loads(old_candidate_raw.decode("utf-8-sig"))
    old_check = json.loads(old_check_raw.decode("utf-8-sig"))
    assert old["countsUnchanged"] == {"reviewed": 525, "pending": 323}
    assert all(next(row for row in old["records"] if row["spellId"] == sid)["completeCurrentCatalogSourceAndAccess"]["id"] == sid for sid in IDS)
    assert old_check["failures"] == 0

    # Preserve the complete 21-question source set and its focused additions; all remain unselected.
    original_questions = copy.deepcopy(old["questions"])
    focused = copy.deepcopy(old_notes["focusedAdditionalQuestions"])
    questions = original_questions + focused
    assert len(original_questions) == 21 and len(questions) == 23
    assert len({row["id"] for row in questions}) == len(questions)
    assert all(row["decisionSelected"] is False for row in questions)
    assert set().union(*(set(row["spellIds"]) for row in questions)) == set(IDS)

    now = datetime.now(timezone.utc).isoformat()
    candidate = copy.deepcopy(old)
    candidate.update({
        "id": "RANK8-PERCEPTION5-SOURCE-CONFERENCE02-156",
        "recordedAtUtc": now,
        "status": "SOURCE_CONFERENCE_PREPARED_UNSENT",
        "priorConferenceSupersededBy": "This Conference02 packet is freshly bound to current authority 718/130. Conference01 remains historical 525/323 evidence only and cannot authorize current acceptance or application.",
        "currentAuthority": {
            "reviewedApplied": 718, "pending": 130, "acceptedUnapplied": 0,
            "completeReviewedStandaloneProcedures": 442,
            "index": binding(INDEX), "catalog": binding(CATALOG),
            "currentQueue": binding(QUEUE_BEFORE), "pendingIdentityAudit": binding(PENDING_BEFORE),
            "priorHandoff": binding(HANDOFF_BEFORE),
        },
        "countsUnchanged": {"reviewed": 718, "pending": 130},
        "gptCommunication": "Fresh Rank8 Perception5 source conference for current authority 718 reviewed / 130 pending / 0 accepted-unapplied. Only mass-hallucination, illusory-dragon, phantom-execution, antipathy-sympathy, and glibness are in scope. Preserve the 21 original source questions and two focused state/factuality questions unselected. Do not reopen any completed feat or spell cohort.",
        "historicalConference01": {
            "status": "HISTORICAL_SOURCE_PACKET_ONLY",
            "authority": copy.deepcopy(old["countsUnchanged"]),
            "candidate": {"path": "historical/Conference01_CANDIDATE.json", "bytes": len(old_candidate_raw), "sha256": sha(old_candidate_raw)},
            "archive": {"path": OLD_ARCHIVE.relative_to(ROOT).as_posix(), "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)},
            "originalSourceBindings": copy.deepcopy(old["sourceBindings"]),
            "originalCheck": {"path": "historical/Conference01_CHECK.json", "bytes": len(old_check_raw), "sha256": sha(old_check_raw)},
            "originalPreparation": binding(OLD_PREPARATION),
            "currentLocalWorkingCopyNotUsedAsHistoricalAuthority": binding(OLD_CANDIDATE),
        },
        "conference01QuestionSetPreserved": {"questions": original_questions, "questionCount": 21, "allStillUnselected": True},
        "conference02Questions": questions,
        "focusedAdditionalQuestions": focused,
        "requiredNewCases": copy.deepcopy(old_notes["requiredNewCases"]),
        "historicalPendingComparisonsNowReviewed": [],
        "pendingComparisonsNotAuthority": [],
        "nonAcceptanceOfLaterSourceChanges": "Current source files in this packet are bound current context only. A changed backing source or procedure does not promote later edits into a previously accepted scope. Preserve each exact acceptance/application receipt as the boundary; do not reopen accepted identities.",
    })
    candidate["questions"] = questions
    candidate["sourceInformationDeleted"] = 0

    for record in candidate["records"]:
        sid = record["spellId"]
        assert sid in IDS
        record["completeCurrentCatalogSourceAndAccess"] = copy.deepcopy(catalog_spells[sid])
        record["currentIndexEntry"] = copy.deepcopy(entries[sid])
        record["currentAuthorityStatus"] = "pending-authored-procedure at current 718/130 authority"

    # Every earlier pending comparison is history only; mark exact current reviewed status where applicable.
    for group in old.get("pendingComparisonsNotAuthority", []):
        ids = list(group["identities"])
        reviewed_ids = [sid for sid in ids if entries[sid]["authoredStatus"] == "reviewed-authored-operational-playtest"]
        still_pending = [sid for sid in ids if entries[sid]["authoredStatus"] == "pending-authored-procedure"]
        if reviewed_ids:
            candidate["historicalPendingComparisonsNowReviewed"].append({
                "historicalGroup": copy.deepcopy(group), "currentReviewedIds": reviewed_ids,
                "stillPendingIds": still_pending, "currentIndexEntries": [copy.deepcopy(entries[sid]) for sid in reviewed_ids + still_pending],
                "qualification": "Historical comparison only. Every identity is resolved against the exact live 718/130 index; this group cannot replace the current first pending group.",
            })
        if still_pending:
            candidate["pendingComparisonsNotAuthority"].append({
                **copy.deepcopy(group), "currentPendingIds": still_pending,
                "qualification": "Historical source comparison, not a current review packet or acceptance. Use only a fresh packet bound to current authority.",
            })

    # Refresh current interface records while preserving Conference01 snapshots.
    current_interfaces = []
    for item in old["currentAcceptedInterfaceComparisons"]:
        tokens = item["registryPointer"].strip("/").split("/")
        value = registry
        for token in tokens:
            value = value[int(token)] if isinstance(value, list) else value[token]
        current_interfaces.append({
            "registryPointer": item["registryPointer"],
            "completeCurrentEntry": copy.deepcopy(value),
            "historicalConference01Entry": copy.deepcopy(item["completeEntryUnchanged"]),
            "scope": "Current interface reference only. It does not reopen, expand or replace any prior exact accepted procedure scope.",
        })
    candidate["currentAcceptedInterfaceComparisons"] = current_interfaces

    # Add exact accepted/current applied authored procedures for the batches most relevant to Perception5.
    comparison_sets = []
    accepted_comparison_paths = set()
    for spec in COMPARISON_BATCHES:
        model_path = REVIEW_DIR / spec["folder"] / "MODEL.json"
        package_manifest = REVIEW_DIR / spec["folder"] / "CANDIDATE_PACKAGE_MANIFEST.json"
        receipt_path = AUDIT / spec["receipt"]
        application_path = AUDIT / spec["application"]
        decision_path = AUDIT / spec["decision"]
        delivery_path = AUDIT / spec["deliveryFolder"] / "DIRECTOR_RETURN_DELIVERY.json"
        model = read(model_path)
        receipt = read(receipt_path)
        application = read(application_path)
        decision = read(decision_path)
        delivery = read(delivery_path)
        spells = model_spells_by_id(model)
        assert receipt["acceptedIds"] == spec["ids"]
        assert application["acceptedIds"] == spec["ids"]
        assert decision["accepted"] is True and decision["acceptedIds"] == spec["ids"]
        assert delivery["accepted"] is True and delivery["applied"] is False and delivery["acceptedIds"] == spec["ids"]
        assert all(entries[sid]["authoredStatus"] == "reviewed-authored-operational-playtest" for sid in spec["ids"])
        model_binding = binding(model_path)
        package_binding = binding(package_manifest)
        receipt_binding = binding(receipt_path)
        application_binding = binding(application_path)
        decision_binding = binding(decision_path)
        delivery_binding = binding(delivery_path)
        procedures = []
        for i, sid in enumerate(spec["ids"]):
            assert sid in spells
            procedures.append({
                "spellId": sid, "model": model_binding,
                "pointer": f"/spells/{i}" if isinstance(model["spells"], list) else f"/spells/{sid}",
                "completeAcceptedProcedure": copy.deepcopy(spells[sid]),
                "currentIndexEntry": copy.deepcopy(entries[sid]),
                "qualification": "Exact accepted and applied authored comparison only; all recorded holds remain. It grants no runtime, human-play, balance, cosmology, domain-closure or release approval.",
            })
        comparison_sets.append({
            "batch": spec["name"], "acceptedIds": spec["ids"], "procedures": procedures,
            "candidateModel": model_binding, "candidatePackageManifest": package_binding,
            "exactAcceptance": receipt_binding, "applicationReceipt": application_binding,
            "directorDecision": decision_binding, "deliveryRecord": delivery_binding,
            "scope": "Closed exact accepted comparison; preserve recorded hashes and qualifications, do not reopen or broaden.",
        })
        accepted_comparison_paths.update({
            model_path, package_manifest, receipt_path, application_path, decision_path, delivery_path,
        })
    candidate["recentExactAcceptedAppliedComparisons"] = comparison_sets

    source_paths = {row["path"] for row in old["sourceBindings"]}
    source_paths.update({
        binding(INDEX)["path"], binding(CATALOG)["path"], binding(QUEUE_BEFORE)["path"],
        binding(PENDING_BEFORE)["path"], binding(HANDOFF_BEFORE)["path"], binding(REGISTRY)["path"],
        binding(SOURCE_CANDIDATE_PATH := ROOT / "DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_summon_structure_5_source_conference_02.json")["path"],
        binding(REVIEW_DIR / "rank8summonstructure5_reviewed_153" / "MODEL.json")["path"],
        binding(REVIEW_DIR / "rank8summonstructure5_reviewed_153" / "CANDIDATE_PACKAGE_MANIFEST.json")["path"],
        binding(AUDIT / "SUMMON_STRUCTURE5_EXACT_ACCEPTANCE_153.json")["path"],
        binding(AUDIT / "SUMMON_STRUCTURE5_APPLICATION_153.json")["path"],
        binding(AUDIT / "GPT_DIRECTOR_DECISION_SUMMON_STRUCTURE5_153.json")["path"],
        binding(AUDIT / "summonstructure5_return153_received" / "DIRECTOR_RETURN_DELIVERY.json")["path"],
        binding(AUDIT / "SUMMON_STRUCTURE5_POST_APPLICATION_VERIFICATION_153.json")["path"],
    })
    source_paths.update(path.relative_to(ROOT).as_posix() for path in accepted_comparison_paths)
    source_rows = []
    historical_bindings = {row["path"]: row for row in old["sourceBindings"]}
    source_deltas = []
    for relative in sorted(source_paths):
        path = ROOT / Path(*relative.split("/"))
        assert path.is_file(), f"Missing bound source: {relative}"
        row = binding(path)
        source_rows.append(row)
        previous = historical_bindings.get(relative)
        if previous and (previous["bytes"], previous["sha256"]) != (row["bytes"], row["sha256"]):
            source_deltas.append({
                "path": relative, "conference01Binding": {"bytes": previous["bytes"], "sha256": previous["sha256"]},
                "currentBinding": row, "scope": "Current source context only; changed current bytes do not alter any prior acceptance boundary.",
            })
    candidate["sourceBindings"] = source_rows
    candidate["historicalSourceBindingDeltas"] = source_deltas
    candidate["sourceBindingCounts"] = {"currentFiles": len(source_rows), "historicalChangedFilesExplicitlyRecorded": len(source_deltas)}

    # Verify Conference01 sources, freeze all current bound files, then build a deterministic manifest.
    with zipfile.ZipFile(OLD_ARCHIVE) as old_zip:
        assert old_zip.testzip() is None
        old_manifest = json.loads(old_zip.read("MANIFEST.json"))
        assert old_manifest["candidate"]["sha256"] == old_prep["candidate"]["sha256"]
        for row in old["sourceBindings"]:
            raw = old_zip.read("sources/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]

    OUT.mkdir(parents=True, exist_ok=True)
    # Omit redundant nested acceptance ZIPs; exact procedures, models and receipts remain bound.
    # Remove only the copies this builder froze under its own source snapshot directory.
    for spec in COMPARISON_BATCHES:
        relative = f"DescentReviewChanges/ReviewBible/data/public/spell_candidates/{spec['folder']}/DIRECTOR_RETURN_ARCHIVE.zip"
        frozen_archive = OUT / "sources" / Path(*relative.split("/"))
        if frozen_archive.exists():
            frozen_archive.unlink()
    frozen = []
    for row in source_rows:
        src = ROOT / Path(*row["path"].split("/"))
        dst = OUT / "sources" / Path(*row["path"].split("/"))
        dst.parent.mkdir(parents=True, exist_ok=True)
        raw = src.read_bytes()
        assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        dst.write_bytes(raw)
        assert dst.read_bytes() == raw
        frozen.append({**row, "frozenCopy": dst.relative_to(ROOT).as_posix()})
    historical_dir = OUT / "historical"
    historical_dir.mkdir(exist_ok=True)
    (historical_dir / "Conference01_CANDIDATE.json").write_bytes(old_candidate_raw)
    (historical_dir / "Conference01_ARCHIVE.zip").write_bytes(old_archive_raw)
    (historical_dir / "Conference01_CHECK.json").write_bytes(old_check_raw)
    (historical_dir / "Conference01_CURRENT_LOCAL_WORKING_COPY_NOT_AUTHORITY.json").write_bytes(old_local_candidate_raw)
    notes_value = {
        "id": "RANK8PERCEPTION5-INDEPENDENT-CONFERENCE-156", "status": "PREPARED_UNSENT_NOT_ACCEPTED",
        "identities": IDS, "currentAppliedCounts": {"reviewed": 718, "pending": 130, "acceptedUnapplied": 0},
        "completeOriginalQuestionsUnchanged": original_questions, "focusedAdditionalQuestions": focused,
        "allQuestions": questions, "requiredNewCases": old_notes["requiredNewCases"],
        "originalFutureCaseRequirementsUnchanged": old_notes["originalFutureCaseRequirementsUnchanged"],
        "historicalComparisons": comparison_sets,
        "sourceChecks": source_rows,
        "scope": "Preparation only. No new procedure or rule adopted; no program execution or runtime, human-play, balance, cosmology or release claim.",
    }
    notes_raw = encode(notes_value)
    (OUT / "CONFERENCE_NOTES.json").write_bytes(notes_raw)
    NOTES.write_bytes(notes_raw)

    checks = []
    def ck(label: str, passed: bool) -> None:
        checks.append({"check": label, "passed": bool(passed)})
        assert passed, label
    ck("Live authored authority is exactly 718 reviewed and 130 pending", index["authoredCounts"] == {"reviewed": 718, "pending": 130})
    ck("Complete standalone procedure count is 442", index["representationCounts"]["completeReviewedStandaloneProcedures"] == 442)
    ck("Pending audit exactly equals current index pending set", set(pending["pendingIds"]) == live_pending)
    ck("Perception5 is the exact first pending group", first["pendingIds"] == IDS)
    ck("All five native catalog/access rows match the current catalog", all(next(r for r in candidate["records"] if r["spellId"] == sid)["completeCurrentCatalogSourceAndAccess"] == catalog_spells[sid] for sid in IDS))
    ck("All 21 original source questions plus two focused questions remain unselected", len(questions) == 23 and len({q["id"] for q in questions}) == 23 and all(q["decisionSelected"] is False for q in questions))
    ck("All five exact target identities are covered by the 23 questions", set().union(*(set(q["spellIds"]) for q in questions)) == set(IDS))
    ck("Conference01 archive remains historical 525/323 evidence", old["countsUnchanged"] == {"reviewed": 525, "pending": 323} and len(old_archive_raw) == old_prep["archive"]["bytes"])
    ck("All five exact recent applied cohorts remain closed comparison-only records", len(comparison_sets) == 5 and all(len(row["procedures"]) == len(row["acceptedIds"]) for row in comparison_sets))
    historical_groups = candidate["historicalPendingComparisonsNowReviewed"] + candidate["pendingComparisonsNotAuthority"]
    ck("Earlier comparison groups do not replace current first-pending authority", all(row.get("group", row.get("historicalGroup", {}).get("group")) != first["group"] for row in historical_groups))
    ck("Current index, catalog, queue, pending audit, and handoff are all byte-bound", len({binding(INDEX)["sha256"], binding(CATALOG)["sha256"], binding(QUEUE_BEFORE)["sha256"], binding(PENDING_BEFORE)["sha256"], binding(HANDOFF_BEFORE)["sha256"]}) == 5)
    ck("Source archive has no new-rule adoption or runtime execution", candidate["newRuleAdoptions"] == 0 and candidate["runtimeTestsExecuted"] == 0 and candidate["humanPlaytests"] == 0)
    ck("Closed feat335 and completed 16/72 cohorts are outside the target scope", not set(IDS).intersection({"feat335", "erase-mind", "feeblemind", "mass-dominate", "mind-ravel"}))
    ck("Current sources and all five exact applied comparison packages are frozen", all((OUT / "sources" / Path(*row["path"].split("/"))).read_bytes() == (ROOT / Path(*row["path"].split("/"))).read_bytes() for row in source_rows))

    candidate_bytes = encode(candidate)
    CANDIDATE.write_bytes(candidate_bytes)
    candidate_binding = binding(CANDIDATE)
    readme = (
        "Fresh Rank8 Perception5 Conference02, bound to 718 reviewed / 130 pending / 0 accepted-unapplied. "
        "Five exact pending identities, 21 original unselected questions plus two focused questions, live queue/handoff/index/catalog, "
        "current source bindings, recent exact accepted comparison cohorts, and historical Conference01 at 525/323 are preserved. "
        "Preparation only; no procedure or rule is adopted.\n"
    ).encode("utf-8")
    (OUT / "README.md").write_bytes(readme)
    check_doc = {
        "id": "RANK8-PERCEPTION5-SOURCE-CHECK-156", "status": "PASS", "candidate": candidate_binding,
        "checks": checks, "checkCount": len(checks), "failures": 0, "sourceCount": len(source_rows),
        "historicalSourceDeltas": len(source_deltas), "sourceAuthority": {"reviewedApplied": 718, "pending": 130, "acceptedUnapplied": 0},
        "targetIds": IDS, "originalQuestions": 21, "focusedQuestions": 2, "totalQuestions": 23,
        "historicalConference01Retained": True, "exactClosedComparisonBatches": 5, "newRuleAdoptions": 0, "runtimeTestsExecuted": 0,
    }
    write(CHECK, check_doc)
    manifest = {
        "id": "RANK8-PERCEPTION5-SOURCE-CONFERENCE02-MANIFEST-156", "candidate": candidate_binding,
        "check": binding(CHECK), "sourceCount": len(source_rows), "frozenSources": frozen,
        "historicalConference01Archive": {"path": "historical/Conference01_ARCHIVE.zip", "bytes": len(old_archive_raw), "sha256": sha(old_archive_raw)},
        "sourceAuthority": candidate["currentAuthority"], "closedComparisonBatches": [row["batch"] for row in comparison_sets],
    }
    write(OUT / "MANIFEST.json", manifest)
    request_text = (
        f"GPT — please review the exact fresh {ARCHIVE.name} source-conference packet against current authority 718 applied-reviewed / 130 pending / 0 accepted-unapplied.\n\n"
        f"Review only {', '.join(IDS)}. Resolve all 23 unselected source questions and the required complete case directions. The packet includes the exact current queue, pending audit, handoff, index/catalog/native rows, {len(source_rows)} frozen current source bindings, five exact recent accepted/applied comparison batches, and Conference01 preserved only as historical 525/323 material.\n\n"
        "Preserve exact prior acceptance boundaries and all source, content, access, runtime, balance, cosmology, and release holds. Keep actual versus perceived state and private information separate, distinguish genuine damage/death/healing and factual evidence from illusion or blocked diagnosis, and preserve actual movement/action wallets and targeting. Do not infer execution from authored fixtures.\n\n"
        "Return complete source-faithful procedures, all dispositions and an independent failure check. If the exact package passes, state accepted=true and applied=false for only the exact accepted IDs. If it fails, leave all identities unaccepted and unapplied and list exact blockers. Do not edit canonical files, reopen feat335, or redo any completed/applied spell cohort.\n"
    )
    REQUEST.write_text(request_text, encoding="utf-8", newline="\n")
    notes_binding = binding(NOTES)
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(CANDIDATE, "CANDIDATE.json")
        archive.write(CHECK, "SOURCE_CHECK.json")
        archive.write(OUT / "MANIFEST.json", "MANIFEST.json")
        archive.write(OUT / "README.md", "README.md")
        archive.write(OUT / "CONFERENCE_NOTES.json", "CONFERENCE_NOTES.json")
        archive.write(NOTES, "RANK8PERCEPTION5_NEXT_CONFERENCE_NOTES.json")
        archive.write(REQUEST, "REQUEST.txt")
        archive.write(historical_dir / "Conference01_CANDIDATE.json", "historical/Conference01_CANDIDATE.json")
        archive.write(historical_dir / "Conference01_ARCHIVE.zip", "historical/Conference01_ARCHIVE.zip")
        archive.write(historical_dir / "Conference01_CHECK.json", "historical/Conference01_CHECK.json")
        archive.write(historical_dir / "Conference01_CURRENT_LOCAL_WORKING_COPY_NOT_AUTHORITY.json", "historical/Conference01_CURRENT_LOCAL_WORKING_COPY_NOT_AUTHORITY.json")
        for row in frozen:
            source = OUT / "sources" / Path(*row["path"].split("/"))
            archive.write(source, "sources/" + row["path"])
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == len(set(archive.namelist()))
        assert archive.read("CANDIDATE.json") == candidate_bytes
        assert json.loads(archive.read("SOURCE_CHECK.json"))["failures"] == 0
        assert archive.read("CONFERENCE_NOTES.json") == (OUT / "CONFERENCE_NOTES.json").read_bytes()
        for row in frozen:
            raw = archive.read("sources/" + row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        assert archive.read("historical/Conference01_ARCHIVE.zip") == old_archive_raw
    archive_binding = binding(ARCHIVE)
    request_binding = binding(REQUEST)
    prep = {
        "id": "RANK8-PERCEPTION5-SOURCE-CONFERENCE02-PREPARATION-156",
        "recordedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "PREPARED_UNSENT",
        "candidate": candidate_binding, "archive": archive_binding, "manifest": binding(OUT / "MANIFEST.json"),
        "check": binding(CHECK), "request": request_binding, "notes": notes_binding,
        "sourceCount": len(source_rows), "identityCount": 5, "questionCount": 23,
        "historicalDeltas": len(source_deltas), "archiveMemberCount": len(zipfile.ZipFile(ARCHIVE).namelist()),
        "allArchiveMembersVerified": True, "sourceAuthority": {"reviewedApplied": 718, "pending": 130, "acceptedUnapplied": 0},
        "nextGroup": first["group"], "canonicalIndexOrCatalogModified": False,
    }
    write(PREPARATION, prep)

    queue_after = copy.deepcopy(queue)
    group = queue_after["currentPendingGroups"][0]
    group.update({"candidate": candidate_binding, "archive": archive_binding, "preparation": binding(PREPARATION), "freshPacketRequiredForCurrentAuthority": False})
    queue_after.update({
        "id": "SPELL-REVIEW-QUEUE-156", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "sourceConferencePrepared": {"group": first["group"], "candidate": candidate_binding, "archive": archive_binding, "preparation": binding(PREPARATION), "status": "PREPARED_UNSENT"},
    })
    write(QUEUE_AFTER, queue_after)
    handoff_after = copy.deepcopy(handoff)
    handoff_after.update({
        "id": "CURRENT-HANDOFF-156", "recordedAtUtc": datetime.now(timezone.utc).isoformat(),
        "status": "RANK8_PERCEPTION5_PACKET02_PREPARED_UNSENT_718_130",
        "currentQueueBinding": binding(QUEUE_AFTER), "nextGroup": first["group"],
        "nextPreparedRequest": {"group": first["group"], "candidate": candidate_binding, "archive": archive_binding, "preparation": binding(PREPARATION), "request": request_binding, "freshPacketRequiredForCurrentAuthority": False, "status": "prepared-unsent"},
        "resumePriority": "Publish and submit exact Rank8 Perception5 Conference02 to Calibration review part6 for independent source question resolution and failure checking. Apply only an exact accepted return, then continue with the new queue's next pending group.",
    })
    write(HANDOFF_AFTER, handoff_after)
    print(json.dumps({"status": "PREPARATION_PASS", "candidate": candidate_binding, "archive": archive_binding, "request": request_binding, "checks": len(checks), "sources": len(source_rows), "historicalDeltas": len(source_deltas), "authority": {"reviewed": 718, "pending": 130}, "acceptedComparisons": [row["batch"] for row in comparison_sets]}, indent=2))


if __name__ == "__main__":
    main()
