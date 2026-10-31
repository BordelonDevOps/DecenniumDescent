from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ID = "timeless-form"
BLOCKER = "DF218-B03"
DECISION_ID = "TIMELESS-FORM-CLOSURE346-DIRECTOR-DECISION"
ACCEPTANCE_ID = "TIMELESS-FORM-CLOSURE346-EXACT-AUTHORED-ACCEPTANCE"
APPLICATION_ID = "TIMELESS-FORM-CLOSURE346-AUTHORED-APPLICATION"
DIRECTOR_URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750"
EXPECTED_ARCHIVE_SHA = "1883c7791d8638a12fececb889728cf5e9aa94c43f66ddc8feb90e7c98438830"
EXPECTED_W345_SHA = "9af268e9d72a61eb8cf813b119840b74380acd9110e7c7929202cda68286863f"
BEFORE = {
    "reviewedApplied": 824,
    "pending": 24,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 548,
    "scopedInterfaces": 173,
}
AFTER = {
    "reviewedApplied": 825,
    "pending": 23,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 549,
    "scopedInterfaces": 173,
}
QUALIFICATIONS = [
    "Static authored review only; no runtime or supplied/historical program was executed.",
    "No human playtest, balance, cosmology, domain-closure, completion, or release approval is made.",
    "Native catalog card, class access, and source status remain unchanged and blocked for runtime selection.",
    "DF218-Q-AGING remains a conditional external forced-aging qualification; no source or cosmological clock is invented.",
    "Time Stop pauses the global world clock; Timeless Form grants no separate clock pause. Its original 60,000-ms deadline remains unchanged.",
    "W345 fixture acquisition remains candidate-only for Timeless Form; actual acquisition remains contingent on the reviewed spell's own permissions.",
    "Ready, active Haste/Slow, and longer Action-mode duration combinations remain disclosed untested cross-products, not claims of coverage.",
    "Historical Return218 HOLD records and their 11 cases remain byte-exact; this application records the later Closure346 disposition separately.",
]
CLOSURE346_AMENDMENT = (
    "CLOSURE346 CURRENT-DISPOSITION AMENDMENT: The preceding DF9-Q22 text records the historical Return218/Queue344 state. "
    "It is preserved as source history and is superseded for the current authored procedure by the Director's sealed acceptance "
    "of Timeless Form / DF218-B03 after the accepted Time Stop / TF192-B01 procedure. Time Stop pauses the one global world-clock "
    "cursor; Timeless Form grants no separate pause. Its original 60,000-ms deadline remains unchanged and resumes with the original "
    "world cursor. DF218-Q-AGING remains a conditional external forced-aging qualification. Candidate-only acquisition, combined "
    "Ready/Haste/Slow encounters, and longer Action-mode rolls remain disclosed coverage limits; no runtime claim is made."
)
DIRECTOR_EXCERPT = (
    "SEALED ACCEPT — timeless-form / DF218-B03. Bound to commit 3a63152a and Closure346 ZIP SHA-256 "
    + EXPECTED_ARCHIVE_SHA
    + ". acceptedIds=[timeless-form], appliedIds=[], heldIds=[], blockerIds=[], "
    "closedBlockerIds=[DF218-B03], applicationAuthorized=true. Remaining DF218-B03 source/witness gaps: none. "
    "The adopted clock reconciliation is that Time Stop pauses the world clock, Timeless Form grants no separate clock pause, and the original 60,000-ms deadline remains unchanged. "
    "Canonical authored-index application is explicitly authorized for Timeless Form only, using the preserved "
    "Return218 procedure, Closure346 crosswalk, and accepted TF318 interface. After application, Fate Rewrite / "
    "TF192-B04 remains first in the continuing queue, retaining dependency TF192-B02; Closure346 supplies no "
    "qualifying Fate Rewrite change, so review it only upon new evidence."
)

INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
SOURCE_PROCEDURE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9defenseform8_reviewed_218/DIRECTOR_RETURN/procedures/timeless-form.json"
TIME_STOP_DIR = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timestop_reviewed_345"
CLOSURE_DIR = A / "rank9_timeless_form_closure_346_delivery"
CLOSURE_ZIP = CLOSURE_DIR / "DD_Rank9_TimelessForm_DF218B03_Closure346.zip"
DELIVERY = CLOSURE_DIR / "DD_Rank9_TimelessForm_DF218B03_Closure346_DELIVERY.json"
INDEPENDENT = CLOSURE_DIR / "TIMELESS_FORM_CLOSURE346_INDEPENDENT_REVIEW.json"
GENERATOR = CLOSURE_DIR / "TIMELESS_FORM_CLOSURE346_GENERATOR_REPLAY.json"
VERIFIER = A / "verify_timeless_form_closure_346.py"
QUEUE0 = A / "CURRENT_SPELL_QUEUE_344.json"
HANDOFF0 = A / "CURRENT_HANDOFF_344.json"
PENDING0 = A / "CURRENT24_PENDING_IDENTITY_AUDIT_344.json"
W345_DIR = A / "rank9_time_stop_joint_witness_345_delivery_r6"
W345_ZIP = W345_DIR / "DD_Rank9_TimeStop_TF318_Witness345.zip"
W345_DELIVERY = W345_DIR / "DD_Rank9_TimeStop_TF318_Witness345_DELIVERY.json"
W345_REVIEW = W345_DIR / "TIME_STOP_TF318_WITNESS345_INDEPENDENT_REVIEW.json"
W345_GENERATOR = W345_DIR / "TIME_STOP_TF318_WITNESS345_GENERATOR_REPLAY.json"
TIME_STOP_PROCEDURE = TIME_STOP_DIR / "PROCEDURE_RECORD.json"
TIME_STOP_ACCEPTANCE = A / "TIME_STOP_WITNESS345_ACCEPTANCE.json"
TIME_STOP_APPLICATION = A / "TIME_STOP_WITNESS345_APPLICATION.json"
TIME_STOP_DECISION = A / "TIME_STOP_WITNESS345_DIRECTOR_DECISION.json"

PKG_REL = pathlib.Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timelessform_reviewed_347")
PKG = ROOT / PKG_REL
STAGING = PKG.with_name(PKG.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/TIMELESS_FORM_CLOSURE346_REVIEWED_347.md"
BACKUP = A / "authored_review_index.before_timeless_form_closure346_347.json"
DECISION_PATH = A / "TIMELESS_FORM_CLOSURE346_DIRECTOR_DECISION.json"
ACCEPTANCE_PATH = A / "TIMELESS_FORM_CLOSURE346_ACCEPTANCE.json"
RECEIPT_PATH = A / "TIMELESS_FORM_CLOSURE346_RECEIPT.json"
APPLICATION_PATH = A / "TIMELESS_FORM_CLOSURE346_APPLICATION.json"
OPERATIONS_PATH = A / "TIMELESS_FORM_CLOSURE346_INDEX_OPERATIONS.json"
VALIDATION_PATH = A / "TIMELESS_FORM_CLOSURE346_APPLICATION_VALIDATION.json"
QUEUE1 = A / "CURRENT_SPELL_QUEUE_345.json"
PENDING1 = A / "CURRENT23_PENDING_IDENTITY_AUDIT_345.json"
HANDOFF1 = A / "CURRENT_HANDOFF_345.json"
SNAPSHOT1 = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_345.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def bind(path: pathlib.Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def bind_at(relative: pathlib.Path, raw: bytes) -> dict:
    return {"path": relative.as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def refresh_current_procedure_bindings() -> None:
    """Append the accepted current disposition while preserving Return218 source bytes and all dependent bindings."""
    procedure_path = PKG / "PROCEDURE_RECORD.json"
    previous_path = PKG / "PREVIOUS_PROCEDURE_RECORD_218.json"
    model_path = PKG / "MODEL.json"
    manifest_path = PKG / "CANDIDATE_PACKAGE_MANIFEST.json"
    original = read(previous_path)
    procedure = read(procedure_path)
    current_text = original["procedureText"] + "\n\n" + CLOSURE346_AMENDMENT
    procedure.update({
        "procedureText": current_text,
        "historicalProcedureTextBinding": bind(previous_path),
        "sourceProcedureTextPreserved": True,
        "closure346CurrentDispositionAmendment": CLOSURE346_AMENDMENT,
    })
    write(procedure_path, procedure)

    model = read(model_path)
    model_spell = model["spells"][0]
    model_spell["procedure"]["procedureText"] = current_text
    model_spell["directorProcedureRecord"] = procedure
    model_spell["procedure"]["directorProcedureRecordFile"] = "PROCEDURE_RECORD.json"
    write(model_path, model)

    package_manifest = read(manifest_path)
    package_manifest["files"] = [
        bind_at(pathlib.Path(row["path"]), (ROOT / row["path"]).read_bytes())
        for row in package_manifest["files"]
    ]
    write(manifest_path, package_manifest)
    model_ref = bind(model_path)
    manifest_ref = bind(manifest_path)
    coverage_ref = bind(PKG / "CASE_COVERAGE.json")
    evidence_ref = bind(PKG / "EVIDENCE_BINDINGS.json")
    decision_ref = bind(DECISION_PATH)

    acceptance = read(ACCEPTANCE_PATH)
    acceptance.update({
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": manifest_ref,
        "caseCoverage": coverage_ref,
        "evidenceBindings": evidence_ref,
    })
    write(ACCEPTANCE_PATH, acceptance)
    acceptance_ref = bind(ACCEPTANCE_PATH)

    receipt = read(RECEIPT_PATH)
    receipt["acceptance"] = acceptance_ref
    receipt["directorDecision"] = decision_ref
    write(RECEIPT_PATH, receipt)
    receipt_ref = bind(RECEIPT_PATH)

    index = read(INDEX)
    entry_i = next(i for i, row in enumerate(index["entries"]) if row["id"] == ID)
    entry = index["entries"][entry_i]
    entry.update({
        "completeEnvelopeBinding": model_ref,
        "caseEvidenceBindings": coverage_ref,
        "candidatePackageManifestBinding": manifest_ref,
        "authoredAcceptanceReceipt": acceptance_ref,
        "directorReturnReceipt": receipt_ref,
        "procedureSourceBinding": decision_ref,
        "authoredApplicationReceipt": APPLICATION_ID + ".json",
    })
    envelope = index["additionalStandaloneEnvelopes"][-1]
    envelope.update({
        "binding": model_ref,
        "authority": acceptance_ref,
        "applicationReceipt": APPLICATION_ID + ".json",
        "directorDecision": decision_ref,
        "directorReturnReceipt": receipt_ref,
        "caseCoverage": coverage_ref,
        "candidatePackageManifestBinding": manifest_ref,
    })
    core_raw = encode(index)
    application = read(APPLICATION_PATH)
    application.update({
        "directorAcceptance": acceptance_ref,
        "directorDecision": decision_ref,
        "directorReturnReceipt": receipt_ref,
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": manifest_ref,
        "caseCoverage": coverage_ref,
        "evidenceBindings": evidence_ref,
        "indexAfterCoreUpdate": bind_at(pathlib.Path("DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"), core_raw),
    })
    write(APPLICATION_PATH, application)
    application_ref = bind(APPLICATION_PATH)
    entry["authoredApplicationReceipt"] = application_ref
    envelope["applicationReceipt"] = application_ref
    write(INDEX, index)
    index_ref = bind(INDEX)

    operations = read(OPERATIONS_PATH)
    operations["after"] = index_ref
    operations["operations"][0]["after"] = entry
    write(OPERATIONS_PATH, operations)


def finalize_existing_application() -> None:
    """Validate and finalize a partially written application without rewriting canonical data."""
    refresh_current_procedure_bindings()
    verifier_run = subprocess.run(["python", str(VERIFIER)], cwd=ROOT, capture_output=True, text=True, check=True)
    verifier_result = json.loads(verifier_run.stdout)
    decision, acceptance, application = map(read, (DECISION_PATH, ACCEPTANCE_PATH, APPLICATION_PATH))
    procedure_record = read(PKG / "PROCEDURE_RECORD.json")
    model = read(PKG / "MODEL.json")
    coverage = read(PKG / "CASE_COVERAGE.json")
    manifest = read(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
    index = read(INDEX)
    backup_raw = BACKUP.read_bytes()
    pending, queue, handoff = map(read, (PENDING1, QUEUE1, HANDOFF1))
    catalog_hash = sha(CATALOG.read_bytes())
    decision_ref = bind(DECISION_PATH)
    archive_ref, delivery_ref, independent_ref = bind(CLOSURE_ZIP), bind(DELIVERY), bind(INDEPENDENT)
    receipt_ref = bind(RECEIPT_PATH)
    current_packet_status = "CLOSURE346_SEALED_ACCEPT_TIMELESS_FORM_DF218_B03_APPLIED; 23_CLOSURE_TASKS_REMAIN"
    current_last_blocker = {"identity": ID, "blockerId": BLOCKER, "group": "timeless-form-closure346"}
    current_index_ref = bind(INDEX)
    for row in (queue, pending, handoff):
        if "indexBinding" in row:
            row["indexBinding"] = current_index_ref
        if "currentIndexBinding" in row:
            row["currentIndexBinding"] = current_index_ref
        row.update({
            "currentPacketStatus": current_packet_status,
            "currentPacketSubmission": archive_ref,
            "currentSubmission": archive_ref,
            "submissionReceipt": None,
            "currentPacketReadbackAudit": independent_ref,
            "currentReturn": decision_ref,
            "currentReturnDecision": decision_ref,
            "currentReturnArchive": archive_ref,
            "currentReturnDelivery": delivery_ref,
            "currentReturnAudit": independent_ref,
            "currentReturnReceipt": receipt_ref,
            "currentReturnAcceptedIds": [ID],
            "currentReturnAppliedIds": [ID],
            "currentReturnHeldIds": [],
            "fateRewriteDependencyIds": ["TF192-B02"],
        })
    queue["lastReviewedBlocker"] = current_last_blocker
    write(QUEUE1, queue)
    queue_ref = bind(QUEUE1)
    pending["currentQueueBinding"] = queue_ref
    pending["lastReviewedBlocker"] = current_last_blocker
    write(PENDING1, pending)
    pending_ref = bind(PENDING1)
    handoff.update({
        "queueBinding": queue_ref,
        "pendingIdentityAuditBinding": pending_ref,
        "lastReviewedBlocker": current_last_blocker,
    })
    write(HANDOFF1, handoff)
    entry = next(row for row in index["entries"] if row["id"] == ID)
    live_pending = {row["id"] for row in index["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    application_ref = bind(APPLICATION_PATH)
    index_ref = bind(INDEX)
    queue_ref = bind(QUEUE1)
    pending_ref = bind(PENDING1)
    package_checks = []
    for file_ref in manifest["files"]:
        path = ROOT / file_ref["path"]
        raw = path.read_bytes()
        package_checks.append(len(raw) == file_ref["bytes"] and sha(raw) == file_ref["sha256"] and crc(raw) == file_ref["crc32"])
    index_core = copy.deepcopy(index)
    core_entry = next(row for row in index_core["entries"] if row["id"] == ID)
    core_entry["authoredApplicationReceipt"] = APPLICATION_ID + ".json"
    index_core["additionalStandaloneEnvelopes"][-1]["applicationReceipt"] = APPLICATION_ID + ".json"
    checks = [
        ("Closure346 verifier passes 74/74", verifier_result["status"] == "PASS_WITH_DECLARED_LIMITS" and verifier_result["checks"] == "74/74" and verifier_result["failed"] == 0),
        ("Director accepted only Timeless Form and authorized application", decision["acceptedIds"] == acceptance["acceptedIds"] == application["acceptedIds"] == [ID] and decision["applicationAuthorized"] is True),
        ("Director closed DF218-B03 only", decision["closedBlockerIds"] == acceptance["closedBlockerIds"] == application["closedBlockerIds"] == [BLOCKER]),
        ("Closure346 archive hash matches sealed ruling", sha(CLOSURE_ZIP.read_bytes()) == EXPECTED_ARCHIVE_SHA and decision["closureArchive"]["sha256"] == EXPECTED_ARCHIVE_SHA),
        ("Index backup matches Queue344 input binding", sha(backup_raw) == read(QUEUE0)["currentIndexBinding"]["sha256"]),
        ("Authored index authority is 825/23 and has 549 procedures", index["authoredCounts"] == {"reviewed": 825, "pending": 23} and index["representationCounts"]["completeReviewedStandaloneProcedures"] == 549),
        ("Only Timeless Form left the pending identity set", len(live_pending) == 23 and pending["pendingIds"] == sorted(live_pending) and ID not in live_pending),
        ("Timeless Form entry is applied and source remains blocked", entry["accepted"] is True and entry["applied"] is True and entry["sourceStatus"] == "blocked-pending-operational-review"),
        ("Application receipt is bound by the index", entry["authoredApplicationReceipt"] == application_ref and application["indexBefore"]["sha256"] == sha(backup_raw)),
        ("Current procedure supersedes historical Q22 without altering Return218 source", procedure_record["procedureText"].endswith(CLOSURE346_AMENDMENT) and model["spells"][0]["procedure"]["procedureText"] == procedure_record["procedureText"] and application["indexAfterCoreUpdate"]["sha256"] == sha(encode(index_core))),
        ("All candidate-package members match the manifest", bool(package_checks) and all(package_checks)),
        ("Eleven historical cases and three W345 witnesses are crosswalked", len(coverage["historicalReturn218Cases"]["cases"]) == 11 and len(coverage["acceptedConditionalTimeStopJointWitnesses"]["cases"]) == 3),
        ("Original deadline reconciliation and aging qualification remain", procedure_record["conditionalQualificationIds"] == ["DF218-Q-AGING"] and procedure_record["clockLifecycleReconciliation"]["observedAnchors"]["ACTION-NATURAL"]["deadlineMs"] == 60000),
        ("Native catalog matches Queue344 and application declares it unchanged", catalog_hash == read(QUEUE0)["currentCatalogBinding"]["sha256"] and application["catalogChanged"] is False),
        ("Queue, pending audit and handoff agree on final authority", queue["currentAuthority"] == pending["authority"] == handoff["authority"] == AFTER),
        ("Queue, pending audit and handoff bind final index and each other", queue["currentIndexBinding"]["sha256"] == pending["indexBinding"]["sha256"] == handoff["indexBinding"]["sha256"] == index_ref["sha256"] and pending["currentQueueBinding"] == queue_ref and handoff["queueBinding"] == queue_ref and handoff["pendingIdentityAuditBinding"] == pending_ref),
        ("Fate Rewrite / TF192-B04 retains dependency TF192-B02", queue["continuingPriorityOrder"][0] == handoff["continuingPriorityOrder"][0] == "fate-rewrite" and queue["fateRewriteDependencyIds"] == handoff["fateRewriteDependencyIds"] == ["TF192-B02"]),
        ("Queue and handoff current packet pointers identify Closure346", queue["currentPacketStatus"] == handoff["currentPacketStatus"] == current_packet_status and queue["currentPacketSubmission"]["sha256"] == handoff["currentPacketSubmission"]["sha256"] == EXPECTED_ARCHIVE_SHA and pending["currentReturnDelivery"]["sha256"] == delivery_ref["sha256"]),
        ("Runtime and downstream gates remain closed", model["runtimeSelectionEnabled"] is False and application["runtimeTestsExecuted"] is False and application["implementationApproved"] is False and application["releaseApproved"] is False),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation = {
        "id": "TIMELESS-FORM-CLOSURE346-APPLICATION-VALIDATION",
        "recordedAtUtc": stamp(),
        "status": "PASS",
        "checks": [{"check": name, "passed": bool(ok)} for name, ok in checks],
        "checkCount": len(checks),
        "failedChecks": 0,
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "closedBlockerIds": [BLOCKER],
        "authority": AFTER,
        "index": index_ref,
        "application": application_ref,
        "acceptance": bind(ACCEPTANCE_PATH),
        "pendingIdentityAudit": pending_ref,
        "queue": queue_ref,
        "handoff": bind(HANDOFF1),
        "catalogByteExact": True,
        "sourceStatusPreservedAsBlocked": True,
        "runtimeSelectionEnabled": False,
    }
    write(VALIDATION_PATH, validation)
    validation_ref = bind(VALIDATION_PATH)
    SNAPSHOT1.write_text(
        "# Spell review snapshot — Timeless Form Closure346 application\n\n"
        "Authority: **825 applied / 23 pending / 0 accepted-unapplied; 549 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "GPT sealed-accepted and explicitly authorized application of `timeless-form` / `DF218-B03` only after reviewing Closure346. The 11 historical Return218 cases remain byte-exact; the three accepted W345 joint witnesses are crosswalked to them. DF218-Q-AGING and declared cross-product coverage limits remain. Fate Rewrite / `TF192-B04`, with dependency `TF192-B02`, is next and should be reviewed only upon qualifying new evidence. The native catalog and runtime remain blocked.\n\n"
        f"Validation: `{validation_ref['path']}` (SHA-256 `{validation_ref['sha256']}`).\n",
        encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "checkCount": len(checks), "failedChecks": 0,
                      "authority": AFTER, "index": index_ref, "application": application_ref,
                      "validation": validation_ref}, ensure_ascii=False, indent=2))


def read_member(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8-sig"))


def main() -> None:
    generated = [DECISION_PATH, ACCEPTANCE_PATH, RECEIPT_PATH, APPLICATION_PATH, OPERATIONS_PATH,
                 VALIDATION_PATH, QUEUE1, PENDING1, HANDOFF1, SNAPSHOT1, BACKUP, MANUSCRIPT]
    assert not PKG.exists() and not STAGING.exists(), "Refusing to overwrite the Timeless Form candidate package."
    assert all(not path.exists() for path in generated), "Refusing to overwrite an existing Closure346 application output."

    verifier_run = subprocess.run(["python", str(VERIFIER)], cwd=ROOT, capture_output=True, text=True, check=True)
    verifier_result = json.loads(verifier_run.stdout)
    assert verifier_result["status"] == "PASS_WITH_DECLARED_LIMITS" and verifier_result["checks"] == "74/74" and verifier_result["failed"] == 0

    before_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index0, catalog0 = read(INDEX), read(CATALOG)
    queue0, handoff0, pending0 = map(read, (QUEUE0, HANDOFF0, PENDING0))
    previous = read(SOURCE_PROCEDURE)
    entry0 = copy.deepcopy(next(row for row in index0["entries"] if row["id"] == ID))
    pending_live0 = {row["id"] for row in index0["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    catalog_row = next(row for row in catalog0["spells"] if row["id"] == ID)
    expected_index_binding = pending0["indexBinding"]
    assert sha(before_raw) == expected_index_binding["sha256"] == queue0["currentIndexBinding"]["sha256"]
    assert pending0["authority"] == queue0["currentAuthority"] == handoff0["authority"] == BEFORE
    assert pending0["pendingCount"] == queue0["pendingCount"] == 24 and pending_live0 == set(pending0["pendingIds"])
    assert ID in pending_live0 and entry0["authoredStatus"] == "pending-authored-procedure"
    assert entry0["sourceStatus"] == "blocked-pending-operational-review"
    assert catalog_row["status"] == "blocked-pending-operational-review" and catalog_row["operational"] is None
    assert previous["spellId"] == ID and previous["accepted"] is False and previous["applied"] is False
    assert previous["holds"] == [BLOCKER] and len(previous["caseIds"]) == 11

    with zipfile.ZipFile(CLOSURE_ZIP) as closure:
        assert closure.testzip() is None
        cmanifest = read_member(closure, "MEMBER_MANIFEST.json")
        crows = {row["path"]: row for row in cmanifest["members"]}
        assert len(closure.namelist()) == 51 and cmanifest["memberCountExcludingSelf"] == 50 and len(crows) == 50
        for member, row in crows.items():
            raw = closure.read(member)
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"]
        crosswalk = read_member(closure, "crosswalk/TIMELESS_FORM_DF218_B03_POSITIVE_CROSSWALK.json")
        projection = read_member(closure, "crosswalk/W345_TIMELESS_FORM_EVIDENCE_PROJECTION.json")
        source_procedure_raw = closure.read("evidence/timeless_form/PROCEDURE_RECORD_218.json")
        held_record = json.loads(source_procedure_raw.decode("utf-8-sig"))
        assert sha(source_procedure_raw) == sha(SOURCE_PROCEDURE.read_bytes())
        assert held_record["accepted"] is False and held_record["applied"] is False and held_record["holds"] == [BLOCKER]
        assert crosswalk["identity"] == ID and crosswalk["blockerIds"] == [BLOCKER]
        assert crosswalk["currentAuthority"] == BEFORE and crosswalk["noApplicationAuthorization"] is True
        assert crosswalk["historicalPreservation"]["sourceCaseCount"] == 11
        assert crosswalk["historicalPreservation"]["event4RemainsHeld"] is True
        assert len(crosswalk["jointWitnesses"]) == 3
        assert projection["sourceArchive"]["sha256"] == EXPECTED_W345_SHA

        delivery, independent, generator = read(DELIVERY), read(INDEPENDENT), read(GENERATOR)
        assert sha(CLOSURE_ZIP.read_bytes()) == EXPECTED_ARCHIVE_SHA
        assert delivery["archive"]["sha256"] == EXPECTED_ARCHIVE_SHA
        assert independent["status"] == "PASS_WITH_DECLARED_LIMITS" and independent["checkCount"] == independent["passedChecks"] == 74 and len(independent["checks"]) == 74
        assert all(row["passed"] for row in independent["checks"])
        assert generator["status"] == "PASS_WITH_DECLARED_LIMITS"
        assert len(crosswalk["historicalPreservation"]["caseBindings"]) == 11
        preserved_refs = []
        for row in crosswalk["historicalPreservation"]["caseBindings"]:
            member = "history/Return218/preserved_cases/" + pathlib.PurePosixPath(row["member"]).name
            actual = crows[member]
            assert actual["bytes"] == row["bytes"] and actual["sha256"] == row["sha256"]
            preserved_refs.append({"id": pathlib.PurePosixPath(row["member"]).stem, "archiveMember": member, "binding": actual})
        crosswalk_raw = closure.read("crosswalk/TIMELESS_FORM_DF218_B03_POSITIVE_CROSSWALK.json")
        question_dispositions_raw = closure.read("evidence/timeless_form/QUESTION_DISPOSITIONS_DF9_Q20_Q22.json")
        interface_raw = closure.read("evidence/time_stop/TF318_JOINT_INTERFACE_CONTRACT.md")
        interface_auth = read_member(closure, "evidence/time_stop/JOINT_INTERFACE_AUTHORIZATION.json")
        assert interface_auth["id"] == "TF318-JOINT-INTERFACE-01"
        assert interface_auth["status"] == "AUTHORIZED_FOR_CONDITIONAL_WITNESS_CONSTRUCTION_ONLY"
        assert sha(interface_raw) == interface_auth["contract"]["sha256"]
        accepted_ts_record_raw = closure.read("evidence/time_stop/rank9timestop_reviewed_345/PROCEDURE_RECORD.json")
        assert sha(accepted_ts_record_raw) == sha(TIME_STOP_PROCEDURE.read_bytes())

    archive_ref = bind(CLOSURE_ZIP)
    delivery_ref = bind(DELIVERY)
    independent_ref = bind(INDEPENDENT)
    generator_ref = bind(GENERATOR)
    verifier_ref = bind(VERIFIER)
    source_procedure_ref = bind(SOURCE_PROCEDURE, source_procedure_raw)
    crosswalk_archive_ref = {"archive": archive_ref, "member": crows["crosswalk/TIMELESS_FORM_DF218_B03_POSITIVE_CROSSWALK.json"]}
    crosswalk_source_ref = bind_at(PKG_REL / "CLOSURE_CROSSWALK.json", crosswalk_raw)
    question_ref = {"archive": archive_ref, "member": crows["evidence/timeless_form/QUESTION_DISPOSITIONS_DF9_Q20_Q22.json"]}
    interface_ref = {"archive": archive_ref, "member": crows["evidence/time_stop/TF318_JOINT_INTERFACE_CONTRACT.md"]}
    time_stop_procedure_ref = bind(TIME_STOP_PROCEDURE, accepted_ts_record_raw)
    time_stop_acceptance = read(TIME_STOP_ACCEPTANCE)
    time_stop_application = read(TIME_STOP_APPLICATION)
    time_stop_decision = read(TIME_STOP_DECISION)
    assert time_stop_acceptance["acceptedIds"] == ["time-stop"] and time_stop_acceptance["appliedIds"] == []
    assert time_stop_application["acceptedIds"] == time_stop_application["appliedIds"] == ["time-stop"]
    assert time_stop_decision["applicationAuthorized"] is True and time_stop_decision["closedBlockerIds"] == ["TF192-B01"]
    assert sha(W345_ZIP.read_bytes()) == EXPECTED_W345_SHA
    w345_archive_ref, w345_delivery_ref = bind(W345_ZIP), bind(W345_DELIVERY)
    w345_review_ref, w345_generator_ref = bind(W345_REVIEW), bind(W345_GENERATOR)
    time_stop_acceptance_ref, time_stop_application_ref = bind(TIME_STOP_ACCEPTANCE), bind(TIME_STOP_APPLICATION)
    time_stop_decision_ref = bind(TIME_STOP_DECISION)
    queue0_ref, handoff0_ref, pending0_ref = bind(QUEUE0), bind(HANDOFF0), bind(PENDING0)
    catalog_ref = bind(CATALOG, catalog_raw)
    index0_ref = bind(INDEX, before_raw)

    with zipfile.ZipFile(W345_ZIP) as w345:
        assert w345.testzip() is None
        w345_names = set(w345.namelist())
        projected_case_refs = []
        for case in projection["newJointCases"]:
            raw = w345.read(case["member"])
            assert len(raw) == case["memberBytes"] and sha(raw) == case["memberSha256"]
            assert projection["sourceMemberHashes"][case["member"]]["sha256"] == sha(raw)
            projected_case_refs.append({"id": case["id"], "archiveMember": case["member"],
                                        "binding": {"bytes": len(raw), "sha256": sha(raw)}})
        assert len(projected_case_refs) == 3

    time = stamp()
    decision = {
        "id": DECISION_ID,
        "recordedAtUtc": time,
        "status": "SEALED_ACCEPT_TIMELESS_FORM_DF218_B03_CLOSURE346",
        "decision": "EXACT_ACCEPT",
        "identity": ID,
        "acceptedIds": [ID],
        "appliedIds": [],
        "heldIds": [],
        "blockerIds": [],
        "closedBlockerIds": [BLOCKER],
        "accepted": True,
        "appliedAtDecision": False,
        "applicationAuthorized": True,
        "source": {"service": "ChatGPT", "conversationTitle": "Review Time Stop Witness Evidence", "url": DIRECTOR_URL},
        "exactDirectorResponseExcerpt": DIRECTOR_EXCERPT,
        "bindingCommit": "3a63152aef5083bce93a7d37bd89330d1f45801e",
        "closureArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "independentReview": independent_ref,
        "generatorReplay": generator_ref,
        "verifier": verifier_ref,
        "crosswalk": crosswalk_archive_ref,
        "authorityAtDecision": BEFORE,
        "authorityAfterApplicationExpected": AFTER,
        "acceptanceScope": "Timeless Form / DF218-B03 only, based on Closure346 and the accepted TF318 Time Stop procedure.",
        "retainedQualificationIds": previous["qualificationHoldIds"],
        "retainedConditionalQualificationIds": previous["conditionalQualificationIds"],
        "retainedQualifications": QUALIFICATIONS,
        "historicalReturn218HoldRecordsRewritten": False,
        "otherSpellAccepted": False,
        "canonicalFilesChangedByDirector": False,
        "gatesStillClosed": ["runtime", "implementation", "human-play", "balance", "cosmology", "domain-closure", "completion", "release"],
    }
    write(DECISION_PATH, decision)
    decision_ref = bind(DECISION_PATH)

    procedure_record = copy.deepcopy(previous)
    original_case_ids = list(previous["caseIds"])
    joint_case_ids = [row["id"] for row in projected_case_refs]
    previous_record_ref = bind_at(PKG_REL / "PREVIOUS_PROCEDURE_RECORD_218.json", source_procedure_raw)
    procedure_record.update({
        "accepted": True,
        "applied": True,
        "holds": [],
        "closedBlockerIds": [BLOCKER],
        "resolvedBlockerIds": [BLOCKER],
        "caseIds": original_case_ids + joint_case_ids,
        "historicalCaseIdsPreserved": original_case_ids,
        "procedureText": previous["procedureText"] + "\n\n" + CLOSURE346_AMENDMENT,
        "historicalProcedureTextBinding": previous_record_ref,
        "sourceProcedureTextPreserved": True,
        "closure346CurrentDispositionAmendment": CLOSURE346_AMENDMENT,
        "jointWitnessCaseIds": joint_case_ids,
        "status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
        "directorDecisionBinding": decision_ref,
        "closureCrosswalkBinding": crosswalk_source_ref,
        "historicalCaseArchiveBinding": archive_ref,
        "acceptedTimeStopProcedureBinding": time_stop_procedure_ref,
        "timeStopAcceptanceBinding": time_stop_acceptance_ref,
        "timeStopApplicationBinding": time_stop_application_ref,
        "jointInterfaceContractBinding": interface_ref,
        "questionDispositionsBinding": question_ref,
        "retainedQualifications": QUALIFICATIONS,
        "retainedQualificationHoldIds": list(previous["qualificationHoldIds"]),
        "retainedConditionalQualificationIds": list(previous["conditionalQualificationIds"]),
        "closedHistoricalHoldDisposition": {"blockerId": BLOCKER, "sourceHoldRecordPreserved": True, "closureReview": archive_ref},
        "clockLifecycleReconciliation": crosswalk["clockLifecycleReconciliation"],
        "declaredCoverageLimits": crosswalk["identifiedUncoveredOrConditionalBranches"],
        "scope": "Timeless Form / DF218-B03 only; apply the Director-accepted Closure346 crosswalk under the accepted TF318 interface, preserving all historical records, qualifications, native source, and runtime gates.",
    })
    procedure_raw = encode(procedure_record)
    procedure_ref = bind_at(PKG_REL / "PROCEDURE_RECORD.json", procedure_raw)

    case_coverage = {
        "id": "TIMELESS-FORM-CLOSURE346-CASE-COVERAGE",
        "spellId": ID,
        "historicalReturn218Cases": {
            "count": len(preserved_refs),
            "byteExact": True,
            "holdRecordsRewritten": False,
            "cases": preserved_refs,
        },
        "acceptedConditionalTimeStopJointWitnesses": {
            "count": len(projected_case_refs),
            "sourceArchive": w345_archive_ref,
            "projectedFromClosure346": True,
            "cases": projected_case_refs,
            "sameSourceEventsAsAcceptedW345": True,
        },
        "closedBlockerIds": [BLOCKER],
        "crosswalk": crosswalk_source_ref,
        "clockLifecycleInterpretation": "Time Stop pauses the global world clock; Timeless Form has no separate clock pause. Its deadline remains 60,000 ms and is frozen/resumed with the world cursor, never reset or extended by personal-turn count.",
        "scope": "Static authored evidence only; no runtime or authenticated campaign execution.",
    }
    case_coverage_raw = encode(case_coverage)
    case_coverage_ref = bind_at(PKG_REL / "CASE_COVERAGE.json", case_coverage_raw)
    evidence = {
        "id": "TIMELESS-FORM-CLOSURE346-EVIDENCE-BINDINGS",
        "sourceProcedure218": source_procedure_ref,
        "directorDecision": decision_ref,
        "closureArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "independentReview": independent_ref,
        "generatorReplay": generator_ref,
        "independentVerifier": verifier_ref,
        "positiveCrosswalk": crosswalk_source_ref,
        "questionDispositions": question_ref,
        "historicalCaseArchive": {"archive": archive_ref, "members": [row["binding"] for row in preserved_refs]},
        "acceptedTimeStopProcedure": time_stop_procedure_ref,
        "timeStopAcceptance": time_stop_acceptance_ref,
        "timeStopApplication": time_stop_application_ref,
        "timeStopDirectorDecision": time_stop_decision_ref,
        "timeStopWitnessArchive": w345_archive_ref,
        "timeStopWitnessDelivery": w345_delivery_ref,
        "timeStopIndependentReview": w345_review_ref,
        "timeStopGeneratorReplay": w345_generator_ref,
        "jointInterfaceAuthorization": interface_auth,
        "jointInterfaceContract": interface_ref,
        "queueBefore": queue0_ref,
        "handoffBefore": handoff0_ref,
        "pendingAuditBefore": pending0_ref,
        "indexBefore": index0_ref,
        "catalogBefore": catalog_ref,
        "caseCoverage": case_coverage_ref,
        "retainedQualifications": QUALIFICATIONS,
    }
    evidence_raw = encode(evidence)
    evidence_ref = bind_at(PKG_REL / "EVIDENCE_BINDINGS.json", evidence_raw)
    crosswalk_ref_actual = bind_at(PKG_REL / "CLOSURE_CROSSWALK.json", crosswalk_raw)
    model = {
        "schemaVersion": 1,
        "moduleId": "rank9timelessform-reviewed-closure346-347",
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_DF218_B03_CLOSED_RUNTIME_DISABLED",
        "scope": "Timeless Form / DF218-B03 only. Native catalog, class access, and runtime remain blocked. All qualifications and unrelated dispositions remain unchanged.",
        "acceptedIds": [ID],
        "unacceptedIds": [],
        "excludedPendingIds": sorted(pending_live0 - {ID}),
        "retainedQualifications": QUALIFICATIONS,
        "sharedRequirements": {"scope": "No shared-rule or native catalog changes; preserve all other pending identities and holds.", "runtimeSelectionEnabled": False},
        "spells": [{
            "id": ID,
            "name": "Timeless Form",
            "position": 0,
            "procedure": {
                "id": "DF218-STATIC-TIMELESS-FORM-CLOSURE346-347",
                "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                "accepted": True,
                "applied": True,
                "procedureText": procedure_record["procedureText"],
                "selectedRules": previous["selectedRules"],
                "sharedRules": previous["sharedRules"],
                "nativeCardAndAccessUnchanged": previous["nativeCardAndAccessUnchanged"],
                "closureCrosswalk": crosswalk,
                "historicalCaseIds": original_case_ids,
                "jointWitnessCaseIds": joint_case_ids,
                "procedureRecordFile": "PROCEDURE_RECORD.json",
                "caseCoverageFile": "CASE_COVERAGE.json",
                "closureCrosswalkFile": "CLOSURE_CROSSWALK.json",
                "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
                "directorDecisionId": DECISION_ID,
                "closedBlockerIds": [BLOCKER],
                "retainedQualificationHoldIds": previous["qualificationHoldIds"],
                "retainedConditionalQualificationIds": previous["conditionalQualificationIds"],
                "retainedQualifications": QUALIFICATIONS,
                "runtimeSelectionEnabled": False,
            },
            "directorProcedureRecord": procedure_record,
            "previousProcedureRecordBinding": previous_record_ref,
            "caseCoverage": case_coverage,
            "nativeCardAndAccessUnchanged": previous["nativeCardAndAccessUnchanged"],
            "caseIds": procedure_record["caseIds"],
            "closedBlockerIds": [BLOCKER],
            "retainedQualificationHoldIds": previous["qualificationHoldIds"],
            "retainedConditionalQualificationIds": previous["conditionalQualificationIds"],
            "runtimeSelectionEnabled": False,
        }],
        "sourceProcedure": source_procedure_ref,
        "previousProcedureRecord": previous_record_ref,
        "closureArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "independentReview": independent_ref,
        "generatorReplay": generator_ref,
        "independentVerifier": verifier_ref,
        "directorDecision": decision_ref,
        "closureCrosswalk": crosswalk_ref_actual,
        "caseCoverage": case_coverage,
        "evidenceBindings": evidence,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "implementationApproved": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "domainClosure": False,
        "completionApproved": False,
        "releaseApproved": False,
    }
    model_raw = encode(model)

    STAGING.mkdir(parents=True)
    (STAGING / "PROCEDURE_RECORD.json").write_bytes(procedure_raw)
    (STAGING / "PREVIOUS_PROCEDURE_RECORD_218.json").write_bytes(source_procedure_raw)
    (STAGING / "CASE_COVERAGE.json").write_bytes(case_coverage_raw)
    (STAGING / "CLOSURE_CROSSWALK.json").write_bytes(crosswalk_raw)
    (STAGING / "EVIDENCE_BINDINGS.json").write_bytes(evidence_raw)
    (STAGING / "MODEL.json").write_bytes(model_raw)
    manuscript = (
        "# Timeless Form — accepted static authored procedure 347\n\n"
        "GPT sealed-accepted Timeless Form / DF218-B03 after reviewing Closure346, bound to commit `3a63152a` and the archive SHA-256 above. This application records one accepted identity in the authored review index only. The native catalog, runtime selection, and downstream gates remain unchanged.\n\n"
        "## Closure evidence\n\n"
        "The application joins the 11 byte-exact historical Return218 Timeless Form cases with the three already accepted W345 conditional joint witnesses. The Closure346 crosswalk maps DF9-Q20/Q21/Q22, the held Return308 event, acquisition and paid histories, interruption and resumption, and the original expiry. No new runtime execution is claimed.\n\n"
        "The Director adopts this clock interpretation: Time Stop pauses the global world clock; Timeless Form grants no separate clock pause. Its original 60,000-ms deadline remains unchanged and resumes with that cursor.\n\n"
        "## Retained qualifications\n\n" + "\n".join(f"- {item}" for item in QUALIFICATIONS) + "\n"
    )
    (STAGING / "STANDALONE_PROCEDURES.md").write_text(manuscript, encoding="utf-8", newline="\n")
    package_manifest = {
        "id": "TIMELESS-FORM-CLOSURE346-CANDIDATE-PACKAGE-MANIFEST",
        "directorDecision": decision_ref,
        "sourceProcedure": source_procedure_ref,
        "closureArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "independentReview": independent_ref,
        "files": [],
    }
    for file in sorted(path for path in STAGING.rglob("*") if path.is_file()):
        package_manifest["files"].append(bind_at(PKG_REL / file.relative_to(STAGING), file.read_bytes()))
    write(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    STAGING.rename(PKG)

    model_ref = bind(PKG / "MODEL.json")
    manifest_ref = bind(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
    coverage_ref = bind(PKG / "CASE_COVERAGE.json")
    evidence_pkg_ref = bind(PKG / "EVIDENCE_BINDINGS.json")
    manuscript_ref = bind_at(pathlib.Path("DescentReviewChanges/ReviewBible/docs/spells/candidates/TIMELESS_FORM_CLOSURE346_REVIEWED_347.md"), manuscript.encode("utf-8"))
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")

    acceptance = {
        "id": ACCEPTANCE_ID,
        "recordedAtUtc": time,
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AWAITING_APPLICATION",
        "acceptedIds": [ID],
        "appliedIds": [],
        "heldIds": [],
        "closedBlockerIds": [BLOCKER],
        "applicationAuthorized": True,
        "directorDecision": decision_ref,
        "sourceProcedure": source_procedure_ref,
        "closureArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "generatorReplay": generator_ref,
        "independentReview": independent_ref,
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": manifest_ref,
        "evidenceBindings": evidence_pkg_ref,
        "caseCoverage": coverage_ref,
        "countsBefore": BEFORE,
        "countsAfterAcceptanceBeforeApplication": {**BEFORE, "acceptedUnapplied": 1},
        "countsAfterApplicationExpected": AFTER,
        "retainedQualificationHoldIds": previous["qualificationHoldIds"],
        "retainedConditionalQualificationIds": previous["conditionalQualificationIds"],
        "retainedQualifications": QUALIFICATIONS,
    }
    write(ACCEPTANCE_PATH, acceptance)
    acceptance_ref = bind(ACCEPTANCE_PATH)
    receipt = {
        "id": "TIMELESS-FORM-CLOSURE346-RETURN-RECEIPT",
        "recordedAtUtc": time,
        "status": "SEALED_ACCEPT_TIMELESS_FORM_DF218_B03_ONLY",
        "acceptedIds": [ID],
        "appliedIds": [],
        "heldIds": [],
        "closedBlockerIds": [BLOCKER],
        "applicationAuthorized": True,
        "directorDecision": decision_ref,
        "acceptance": acceptance_ref,
        "closureArchive": archive_ref,
        "independentReview": independent_ref,
        "retainedQualificationHoldIds": previous["qualificationHoldIds"],
        "retainedConditionalQualificationIds": previous["conditionalQualificationIds"],
        "sourceResponseExcerpt": DIRECTOR_EXCERPT,
    }
    write(RECEIPT_PATH, receipt)
    receipt_ref = bind(RECEIPT_PATH)

    index1 = copy.deepcopy(index0)
    entry1 = copy.deepcopy(entry0)
    entry1.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank9timelessform_reviewed_347/MODEL.json",
        "procedurePointer": "/spells/0/procedure",
        "wholeCardPointer": "/spells/0",
        "sourceCatalogWholeCardPointer": entry0.get("sourceCatalogWholeCardPointer") or entry0["wholeCardPointer"],
        "wholeCardIdField": "id",
        "procedureTextPointer": "/spells/0/procedure/procedureText",
        "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
        "sharedRulesPointer": "/spells/0/procedure/sharedRules",
        "spellLocalRequirementsPointer": "/spells/0/procedure",
        "manuscript": "../../../docs/spells/candidates/TIMELESS_FORM_CLOSURE346_REVIEWED_347.md",
        "reviewId": APPLICATION_ID,
        "runtimeSelectionEnabled": False,
        "historicalCandidateLabelsPreserved": True,
        "completeEvidenceRoot": PKG_REL.as_posix(),
        "completeEnvelopeBinding": model_ref,
        "caseEvidenceBindings": coverage_ref,
        "sourceArchiveBinding": archive_ref,
        "deliveryManifestBinding": delivery_ref,
        "independentReviewBinding": independent_ref,
        "candidatePackageManifestBinding": manifest_ref,
        "procedureSourceBinding": decision_ref,
        "authoredAcceptanceReceipt": acceptance_ref,
        "authoredApplicationReceipt": APPLICATION_ID + ".json",
        "directorReturnReceipt": receipt_ref,
        "accepted": True,
        "applied": True,
        "closedBlockerIds": [BLOCKER],
        "retainedQualificationHoldIds": previous["qualificationHoldIds"],
        "retainedConditionalQualificationIds": previous["conditionalQualificationIds"],
        "retainedQualifications": QUALIFICATIONS,
        "sourceStatus": "blocked-pending-operational-review",
        "priorCatalogSelectionStatusUnchanged": True,
    })
    row_i = next(i for i, row in enumerate(index1["entries"]) if row["id"] == ID)
    index1["entries"][row_i] = entry1
    excluded_pending = sorted(pending_live0 - {ID})
    envelope = {
        "file": "../spell_candidates/rank9timelessform_reviewed_347/MODEL.json",
        "binding": model_ref,
        "reviewId": ACCEPTANCE_ID,
        "acceptedIds": [ID],
        "unacceptedIds": [],
        "excludedPendingIds": excluded_pending,
        "authority": acceptance_ref,
        "applicationReceipt": APPLICATION_ID + ".json",
        "directorDecision": decision_ref,
        "directorReturnReceipt": receipt_ref,
        "sourceArchive": archive_ref,
        "sourceDeliveryManifest": delivery_ref,
        "independentReview": independent_ref,
        "caseCoverage": coverage_ref,
        "procedureSource": source_procedure_ref,
        "candidatePackageManifestBinding": manifest_ref,
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_DF218_B03_CLOSED_RUNTIME_DISABLED",
        "runtimeSelectionEnabled": False,
    }
    index1["additionalStandaloneEnvelopes"].append(envelope)
    index1["authoredCounts"] = {"reviewed": 825, "pending": 23}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"] = 549
    pending_live1 = {row["id"] for row in index1["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert pending_live1 == pending_live0 - {ID} and len(pending_live1) == 23
    assert "fate-rewrite" in pending_live1

    BACKUP.write_bytes(before_raw)
    assert BACKUP.read_bytes() == before_raw
    write(INDEX, index1)
    index_core_ref = bind(INDEX)
    application = {
        "id": APPLICATION_ID,
        "recordedAtUtc": time,
        "status": "APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE",
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "heldIds": [],
        "closedBlockerIds": [BLOCKER],
        "directorAcceptance": acceptance_ref,
        "directorDecision": decision_ref,
        "directorReturnReceipt": receipt_ref,
        "sourceProcedure": source_procedure_ref,
        "closureArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "generatorReplay": generator_ref,
        "independentReview": independent_ref,
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": manifest_ref,
        "caseCoverage": coverage_ref,
        "evidenceBindings": evidence_pkg_ref,
        "manuscript": manuscript_ref,
        "indexBefore": bind(BACKUP, before_raw),
        "indexAfterCoreUpdate": index_core_ref,
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": 548, "after": 549},
        "scopedInterfaces": 173,
        "catalogChanged": False,
        "sourceStatusPreservedAsBlocked": True,
        "historicalReturn218RecordsRewritten": False,
        "runtimeSelectionEnabled": False,
        "runtimeTestsExecuted": False,
        "implementationApproved": False,
        "humanPlaytested": False,
        "balanceApproved": False,
        "cosmologyModified": False,
        "domainClosure": False,
        "completionApproved": False,
        "releaseApproved": False,
    }
    write(APPLICATION_PATH, application)
    application_ref = bind(APPLICATION_PATH)
    entry1["authoredApplicationReceipt"] = application_ref
    index1["entries"][row_i] = entry1
    index1["additionalStandaloneEnvelopes"][-1]["applicationReceipt"] = application_ref
    write(INDEX, index1)
    index_ref = bind(INDEX)

    operations = {
        "id": "TIMELESS-FORM-CLOSURE346-INDEX-OPERATIONS",
        "recordedAtUtc": time,
        "before": bind(BACKUP, before_raw),
        "after": index_ref,
        "operations": [
            {"op": "update-entry", "id": ID, "before": entry0, "after": entry1},
            {"op": "append-standalone-envelope", "acceptedIds": [ID]},
            {"op": "update-authored-counts", "before": {"reviewed": 824, "pending": 24}, "after": {"reviewed": 825, "pending": 23}},
            {"op": "increment-complete-procedure-count", "before": 548, "after": 549},
        ],
        "inverse": [
            {"op": "restore-entry", "id": ID, "value": entry0},
            {"op": "remove-appended-standalone-envelope", "acceptedIds": [ID]},
            {"op": "restore-authored-counts", "value": {"reviewed": 824, "pending": 24}},
            {"op": "restore-complete-procedure-count", "value": 548},
            {"op": "restore-byte-exact-index-from-backup", "backup": bind(BACKUP, before_raw)},
        ],
        "catalogByteExact": CATALOG.read_bytes() == catalog_raw,
        "nativeCardUnchanged": True,
        "sourceStatusPreservedAsBlocked": True,
        "historicalReturn218HoldRecordsRewritten": False,
        "inverseRestoresExactIndex": BACKUP.read_bytes() == before_raw,
    }
    write(OPERATIONS_PATH, operations)
    operations_ref = bind(OPERATIONS_PATH)

    decision_ref = bind(DECISION_PATH)
    receipt_ref = bind(RECEIPT_PATH)
    next_priorities = [item for item in queue0["continuingPriorityOrder"] if item != ID]
    assert next_priorities and next_priorities[0] == "fate-rewrite"
    queue1 = copy.deepcopy(queue0)
    queue1.update({
        "id": "SPELL-REVIEW-QUEUE-345",
        "recordedAtUtc": time,
        "supersedesQueue": queue0_ref,
        "currentAuthority": AFTER,
        "currentIndexBinding": index_ref,
        "currentCatalogBinding": catalog_ref,
        "pendingCount": 23,
        "acceptedUnapplied": 0,
        "nextGroup": None,
        "nextPendingIds": [],
        "nextPendingCount": 0,
        "activeReview": None,
        "next": None,
        "continuingPriorityOrder": next_priorities,
        "separatelyRetainedHolds": [item for item in queue0.get("separatelyRetainedHolds", []) if item != ID],
        "closureTasksRemaining": 23,
        "firstReviewTasksRemaining": 0,
        "allPendingGroupsReviewed": True,
        "unreviewedPendingIds": [],
        "lastDirectorReturn": DECISION_ID,
        "currentReturnAcceptedIds": [ID],
        "currentReturnAppliedIds": [ID],
        "currentReturnHeldIds": [],
        "currentReturnBlockers": {k: v for k, v in queue0.get("currentReturnBlockers", {}).items() if k != ID},
        "currentReturnDecision": decision_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": independent_ref,
        "currentReturn": decision_ref,
        "currentSourcePacket": archive_ref,
        "currentPreparation": None,
        "currentPacketStatus": "CLOSURE346_SEALED_ACCEPT_TIMELESS_FORM_DF218_B03_APPLIED; 23_CLOSURE_TASKS_REMAIN",
        "currentPacketSubmission": archive_ref,
        "currentSubmission": archive_ref,
        "submissionReceipt": None,
        "currentPacketReadbackAudit": independent_ref,
        "lastReviewedBlocker": {"identity": ID, "blockerId": BLOCKER, "group": "timeless-form-closure346"},
        "pendingIdentityAudit": PENDING1.relative_to(ROOT).as_posix(),
        "directorConnectionStatus": "GPT sealed-accepted and explicitly authorized Timeless Form / DF218-B03 application only.",
        "githubChanges": True,
        "canonicalFilesChanged": True,
        "applicationPerformed": True,
        "currentReturnReceipt": receipt_ref,
        "currentPendingIdentityAudit": PENDING1.relative_to(ROOT).as_posix(),
        "currentHandoff": HANDOFF1.relative_to(ROOT).as_posix(),
        "acceptedThisStep": [ID],
        "appliedThisStep": [ID],
        "currentDirectorInstruction": "Apply the sealed Timeless Form acceptance only. Thereafter, Fate Rewrite / TF192-B04 remains first and retains dependency TF192-B02; review that hold only upon new qualifying evidence.",
        "fateRewriteDependencyIds": ["TF192-B02"],
        "heldThisStep": [],
        "currentReview": None,
        "timelessFormDisposition": {
            "held": False,
            "blockerIds": [],
            "closedBlockerIds": [BLOCKER],
            "accepted": True,
            "applied": True,
            "applicationAuthorized": True,
            "closureArchive": archive_ref,
            "retainedQualificationHoldIds": previous["qualificationHoldIds"],
            "retainedConditionalQualificationIds": previous["conditionalQualificationIds"],
            "clockLifecycleReconciliation": "Time Stop pauses the global world clock; Timeless Form grants no separate pause; its original 60,000-ms deadline remains unchanged.",
            "declaredCoverageLimits": crosswalk["identifiedUncoveredOrConditionalBranches"],
        },
    })
    write(QUEUE1, queue1)
    queue1_ref = bind(QUEUE1)

    pending1 = copy.deepcopy(pending0)
    pending1.update({
        "id": "SPELL-REVIEW-CURRENT23-PENDING-IDENTITY-AUDIT-345",
        "recordedAtUtc": time,
        "status": "PASS_CURRENT_825_23_TIMELESS_FORM_DF218_B03_ACCEPTED_AND_APPLIED_CLOSURE346",
        "supersedes": PENDING0.name,
        "authority": AFTER,
        "indexBinding": index_ref,
        "catalogBinding": catalog_ref,
        "pendingCount": 23,
        "pendingIds": sorted(pending_live1),
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "separatelyHeldIds": [item for item in pending0.get("separatelyHeldIds", []) if item != ID],
        "unreviewedPendingIds": [],
        "firstReviewTasksRemaining": 0,
        "closureTasksRemaining": 23,
        "nextGroup": None,
        "nextPendingIds": [],
        "nextPendingCount": 0,
        "nextStep": "Timeless Form / DF218-B03 was accepted and applied. Next priority is Fate Rewrite / TF192-B04 with TF192-B02 retained; review it only if qualifying new evidence is available.",
        "sourceQueue": QUEUE1.relative_to(ROOT).as_posix(),
        "canonicalFilesChanged": True,
        "heldThisStep": [],
        "timelessFormBlockers": [],
        "currentQueueBinding": queue1_ref,
        "currentPacketStatus": "CLOSURE346_SEALED_ACCEPT_TIMELESS_FORM_DF218_B03_APPLIED; 23_CLOSURE_TASKS_REMAIN",
        "currentPacketSubmission": archive_ref,
        "currentSubmission": archive_ref,
        "submissionReceipt": None,
        "currentPacketReadbackAudit": independent_ref,
        "currentReturnDecision": decision_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": independent_ref,
        "currentReturnAcceptedIds": [ID],
        "currentReturnAppliedIds": [ID],
        "currentReturnHeldIds": [],
        "fateRewriteDependencyIds": ["TF192-B02"],
        "lastReviewedBlocker": {"identity": ID, "blockerId": BLOCKER, "group": "timeless-form-closure346"},
        "applicationPerformed": True,
        "currentReturn": decision_ref,
        "currentReturnReceipt": receipt_ref,
        "currentHandoff": HANDOFF1.relative_to(ROOT).as_posix(),
        "closedBlockerIdsThisStep": [BLOCKER],
        "lastDirectorReturn": {
            "decisionId": DECISION_ID,
            "acceptedIds": [ID],
            "appliedIds": [ID],
            "heldIds": [],
            "closedBlockerIds": [BLOCKER],
            "archive": archive_ref,
            "independentReview": independent_ref,
        },
    })
    write(PENDING1, pending1)
    pending1_ref = bind(PENDING1)

    handoff1 = copy.deepcopy(handoff0)
    handoff1.update({
        "id": "CURRENT-HANDOFF-345",
        "recordedAtUtc": time,
        "supersedes": handoff0["id"],
        "status": "TIMELESS_FORM_DF218_B03_ACCEPTED_AND_APPLIED_825_23_0",
        "authority": AFTER,
        "currentAuthority": AFTER,
        "continuingPriorityOrder": next_priorities,
        "fateRewriteDependencyIds": ["TF192-B02"],
        "currentPacketStatus": "CLOSURE346_SEALED_ACCEPT_TIMELESS_FORM_DF218_B03_APPLIED; 23_CLOSURE_TASKS_REMAIN",
        "currentPacketSubmission": archive_ref,
        "currentSubmission": archive_ref,
        "submissionReceipt": None,
        "currentPacketReadbackAudit": independent_ref,
        "lastReviewedBlocker": {"identity": ID, "blockerId": BLOCKER, "group": "timeless-form-closure346"},
        "scopeIds": [ID],
        "blockerIds": [],
        "indexBinding": index_ref,
        "queue": QUEUE1.relative_to(ROOT).as_posix(),
        "queueBinding": queue1_ref,
        "pendingIdentityAudit": PENDING1.relative_to(ROOT).as_posix(),
        "pendingIdentityAuditBinding": pending1_ref,
        "appliedThisStep": True,
        "acceptedThisStep": [ID],
        "heldThisStep": [],
        "currentBlocker": None,
        "nextPendingGroup": None,
        "nextStep": "Fate Rewrite / TF192-B04 is next with TF192-B02 retained; obtain qualifying new evidence before reviewing that hold.",
        "closureTasksRemaining": 23,
        "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "GPT returned SEALED ACCEPT for Timeless Form / DF218-B03 only and explicitly authorized canonical authored-index application.",
        "directorReturnDecision": decision_ref,
        "directorReturnArchive": archive_ref,
        "directorReturnDelivery": delivery_ref,
        "directorReturnAudit": independent_ref,
        "applicationPerformed": True,
        "canonicalFilesChanged": True,
        "closedBlockerIds": list(dict.fromkeys(handoff0.get("closedBlockerIds", []) + [BLOCKER])),
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "currentDirectorInstruction": decision_ref,
        "currentReturnReceipt": receipt_ref,
        "currentReturnAcceptedIds": [ID],
        "currentReturnAppliedIds": [ID],
        "currentReturnHeldIds": [],
        "currentDirectorReturn": decision_ref,
        "currentDirectorDelivery": delivery_ref,
        "currentReturnAudit": independent_ref,
        "currentReadbackAudit": independent_ref,
        "currentReturn": decision_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAuditBinding": independent_ref,
        "currentPreparation": None,
        "nextStepText": "Fate Rewrite / TF192-B04 is the next priority with dependency TF192-B02 retained; review only upon new qualifying evidence.",
    })
    write(HANDOFF1, handoff1)
    handoff1_ref = bind(HANDOFF1)

    checks = [
        ("Director sealed-accepted only Timeless Form and authorized application", decision["acceptedIds"] == [ID] and decision["applicationAuthorized"] and decision["closedBlockerIds"] == [BLOCKER]),
        ("Closure346 packet verifier passes 74/74", verifier_result["status"] == "PASS_WITH_DECLARED_LIMITS" and verifier_result["checks"] == "74/74" and verifier_result["failed"] == 0),
        ("Closure346 archive and delivery bindings match", archive_ref["sha256"] == EXPECTED_ARCHIVE_SHA and delivery["archive"]["sha256"] == archive_ref["sha256"]),
        ("Queue344 authority and exact pre-index binding match", pending0["authority"] == BEFORE and index0_ref["sha256"] == pending0["indexBinding"]["sha256"]),
        ("Only Timeless Form leaves the pending set", pending_live1 == pending_live0 - {ID} and len(pending_live1) == 23),
        ("Authority advances to 825/23/0 and 549/173", index1["authoredCounts"] == {"reviewed": 825, "pending": 23} and index1["representationCounts"]["completeReviewedStandaloneProcedures"] == 549),
        ("Fate Rewrite remains pending and first in priority", "fate-rewrite" in pending_live1 and next_priorities[0] == "fate-rewrite"),
        ("TF192-B04 keeps dependency TF192-B02", handoff1["fateRewriteDependencyIds"] == queue1["fateRewriteDependencyIds"] == ["TF192-B02"] and "fate-rewrite" in handoff1["continuingPriorityOrder"]),
        ("Queue and handoff current packet pointers identify Closure346", queue1["currentPacketStatus"] == handoff1["currentPacketStatus"] and queue1["currentPacketSubmission"]["sha256"] == handoff1["currentPacketSubmission"]["sha256"] == EXPECTED_ARCHIVE_SHA and pending1["currentReturnDelivery"]["sha256"] == delivery_ref["sha256"]),
        ("All 11 historical Return218 cases remain byte-exact", len(preserved_refs) == 11 and crosswalk["historicalPreservation"]["event4RemainsHeld"] is True),
        ("Three joint witnesses bind to accepted W345 bytes", len(projected_case_refs) == 3 and all(c["binding"]["sha256"] for c in projected_case_refs)),
        ("Clock interpretation preserves original 60,000-ms deadline", procedure_record["clockLifecycleReconciliation"]["observedAnchors"]["ACTION-NATURAL"]["deadlineMs"] == 60000 and "global world-clock cursor" in procedure_record["clockLifecycleReconciliation"]["proposedInterpretationForDirector"]),
        ("Aging remains conditionally qualified", "DF218-Q-AGING" in procedure_record["conditionalQualificationIds"]),
        ("Native catalog is byte-exact and Timeless Form remains source-blocked", CATALOG.read_bytes() == catalog_raw and catalog_row["status"] == "blocked-pending-operational-review" and entry1["sourceStatus"] == "blocked-pending-operational-review"),
        ("Historical Return218 record bytes are preserved", SOURCE_PROCEDURE.read_bytes() == source_procedure_raw and BACKUP.read_bytes() == before_raw),
        ("Runtime and downstream gates remain disabled", model["runtimeSelectionEnabled"] is False and model["implementationApproved"] is False and model["releaseApproved"] is False),
        ("Queue, pending audit, and handoff bind the final index and authority", pending1["indexBinding"]["sha256"] == index_ref["sha256"] and queue1["currentIndexBinding"]["sha256"] == index_ref["sha256"] and handoff1["indexBinding"]["sha256"] == index_ref["sha256"]),
        ("Queue, pending audit, and handoff agree on 23 closure tasks", queue1["closureTasksRemaining"] == pending1["closureTasksRemaining"] == handoff1["closureTasksRemaining"] == 23),
        ("No other spell was accepted or applied", acceptance["acceptedIds"] == [ID] and application["appliedIds"] == [ID] and len(pending_live1) == 23),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation = {
        "id": "TIMELESS-FORM-CLOSURE346-APPLICATION-VALIDATION",
        "recordedAtUtc": time,
        "status": "PASS",
        "checks": [{"check": name, "passed": bool(ok)} for name, ok in checks],
        "checkCount": len(checks),
        "failedChecks": 0,
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "closedBlockerIds": [BLOCKER],
        "authority": AFTER,
        "index": index_ref,
        "application": application_ref,
        "acceptance": acceptance_ref,
        "pendingIdentityAudit": pending1_ref,
        "queue": queue1_ref,
        "handoff": handoff1_ref,
        "indexOperations": operations_ref,
        "catalogByteExact": True,
        "sourceStatusPreservedAsBlocked": True,
        "runtimeSelectionEnabled": False,
    }
    write(VALIDATION_PATH, validation)
    validation_ref = bind(VALIDATION_PATH)
    SNAPSHOT1.write_text(
        "# Spell review snapshot — Timeless Form Closure346 application\n\n"
        "Authority: **825 applied / 23 pending / 0 accepted-unapplied; 549 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "GPT sealed-accepted and explicitly authorized application of `timeless-form` / `DF218-B03` only after reviewing Closure346. The 11 historical Return218 cases remain byte-exact; the three accepted W345 joint witnesses are crosswalked to them. DF218-Q-AGING and declared cross-product coverage limits remain. Fate Rewrite / `TF192-B04`, with dependency `TF192-B02`, is next and should be reviewed only upon qualifying new evidence. The native catalog and runtime remain blocked.\n\n"
        f"Validation: `{validation_ref['path']}` (SHA-256 `{validation_ref['sha256']}`).\n",
        encoding="utf-8", newline="\n")

    assert CATALOG.read_bytes() == catalog_raw and sha(INDEX.read_bytes()) == index_ref["sha256"]
    final_index = read(INDEX)
    final_entry = next(row for row in final_index["entries"] if row["id"] == ID)
    assert final_index["authoredCounts"] == {"reviewed": 825, "pending": 23}
    assert final_entry["accepted"] is True and final_entry["applied"] is True and final_entry["closedBlockerIds"] == [BLOCKER]
    print(json.dumps({
        "status": "PASS",
        "acceptedApplied": ID,
        "closedBlockerIds": [BLOCKER],
        "authority": AFTER,
        "closureArchive": archive_ref,
        "index": bind(INDEX),
        "application": application_ref,
        "validation": validation_ref,
        "pendingAudit": pending1_ref,
        "queue": queue1_ref,
        "handoff": handoff1_ref,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--finalize-existing":
        finalize_existing_application()
    else:
        main()
