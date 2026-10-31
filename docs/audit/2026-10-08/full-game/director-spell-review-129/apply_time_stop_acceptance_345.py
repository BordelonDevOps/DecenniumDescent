from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import shutil
import subprocess
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ID = "time-stop"
BLOCKER = "TF192-B01"
CONTRACT_ID = "TF318-JOINT-INTERFACE-01"
ARCHIVE_DIR = A / "rank9_time_stop_joint_witness_345_delivery_r6"
ARCHIVE = ARCHIVE_DIR / "DD_Rank9_TimeStop_TF318_Witness345.zip"
DELIVERY = ARCHIVE_DIR / "DD_Rank9_TimeStop_TF318_Witness345_DELIVERY.json"
GENERATOR_AUDIT = ARCHIVE_DIR / "TIME_STOP_TF318_WITNESS345_GENERATOR_REPLAY.json"
INDEPENDENT_REVIEW = ARCHIVE_DIR / "TIME_STOP_TF318_WITNESS345_INDEPENDENT_REVIEW.json"
VERIFIER = A / "verify_time_stop_joint_witness_345.py"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE0 = A / "CURRENT_SPELL_QUEUE_343.json"
HANDOFF0 = A / "CURRENT_HANDOFF_343.json"
PENDING0 = A / "CURRENT25_PENDING_IDENTITY_AUDIT_343.json"
OLD_PROCEDURE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192/procedures/time-stop.json"
PKG_REL = pathlib.Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timestop_reviewed_345")
PKG = ROOT / PKG_REL
STAGING = PKG.with_name(PKG.name + ".staging")
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/TIME_STOP_REVIEWED_345.md"
BACKUP = A / "authored_review_index.before_time_stop_345.json"
DECISION_PATH = A / "TIME_STOP_WITNESS345_DIRECTOR_DECISION.json"
ACCEPTANCE_PATH = A / "TIME_STOP_WITNESS345_ACCEPTANCE.json"
RECEIPT_PATH = A / "TIME_STOP_WITNESS345_RECEIPT.json"
APPLICATION_PATH = A / "TIME_STOP_WITNESS345_APPLICATION.json"
OPERATIONS_PATH = A / "TIME_STOP_WITNESS345_INDEX_OPERATIONS.json"
VALIDATION_PATH = A / "TIME_STOP_WITNESS345_APPLICATION_VALIDATION.json"
PENDING1 = A / "CURRENT24_PENDING_IDENTITY_AUDIT_344.json"
QUEUE1 = A / "CURRENT_SPELL_QUEUE_344.json"
HANDOFF1 = A / "CURRENT_HANDOFF_344.json"
SNAPSHOT1 = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_344.md"
BEFORE = {
    "reviewedApplied": 823,
    "pending": 25,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 547,
    "scopedInterfaces": 173,
}
AFTER = {
    "reviewedApplied": 824,
    "pending": 24,
    "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 548,
    "scopedInterfaces": 173,
}
NEW_CASES = [
    "TF318-345-ACTION-NATURAL",
    "TF318-345-CLERIC-UNIVERSAL-NATURAL",
    "TF318-345-ACTION-FAILED-THEN-INTERRUPTED",
]
EXPECTED_ARCHIVE_SHA = "9af268e9d72a61eb8cf813b119840b74380acd9110e7c7929202cda68286863f"
DIRECTOR_URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750"
DIRECTOR_TEXT = """SEALED ACCEPT — time-stop / TF192-B01, Witness345 r6. The corrected evidence satisfies TF318. R1–R3 are resolved.

acceptedIds=["time-stop"], appliedIds=[], heldIds=[], closedBlockerIds=["TF192-B01"], applicationAuthorized=true. This ruling concerns Time Stop only.

R1: In both Action cases, C’s automaticFeatures[5].resistanceChoice, arcaneWardChoice.damageType and active resistances consistently specify psychic, supported by the prepared Illusory Blade and Wizard card 57.

R2: The saved cursor preserves C’s pending round-one slot at 0 ms. Events 24–27 process P’s resumed END → C’s round-one START → C’s END → P’s round-two START at 6,000 ms. C’s Reaction remains 0 throughout the interval and refreshes 0→1 only at event 25, its actual regular START. Each case records 20 ordered regular slots, each with exactly one START and END; schedule views agree.

R3: Perception, commitment, cast and resource records agree: P targets at 50 feet; C targets the self-origin effect at 0 feet. Both retain the same captured Time Stop application ID.

Prior TF318 requirements remain satisfied: qualified candidate acquisitions/preparation, paid casting and counter-window order, Wizard strain protection, source-bound Arcane Sight, failed-removal costs/recharge, successful interruption and cleanup, independent peer phases, natural completion after the final peer END, preserved shared expenditures/custody, and Timeless Form’s original 60,000-ms expiry.

Integrity: all 33 payload hashes, the 34-member allowlist, 10 embedded source bindings and 14 byte-exact preserved cases pass. All 179 events / 358 forward / 358 inverse operations pass full replay and reversal. No remaining TF192-B01 witness gap was identified. Ruling binds ZIP SHA-256 9af268e9d72a61eb8cf813b119840b74380acd9110e7c7929202cda68286863f.

Queue343 baseline: 823 applied / 25 pending / 0 accepted-unapplied, 0 first-review identities / 25 closure tasks, 547 procedures / 173 interfaces. This accepts one identity awaiting application and applies none; 24 other closure tasks remain. No canonical counters were modified.

Canonical application is explicitly authorized for time-stop only under TF318-JOINT-INTERFACE-01 and this acceptance. Timeless Form remains pending; DF218-B03 stays open. TF192-H-WORLD, all retained qualifications, and every unrelated hold/CLOSED disposition remain unchanged. No runtime, human-play, balance, cosmology or release claim is made."""
QUALIFICATIONS = [
    "Acceptance closes Time Stop / TF192-B01 only, under TF318-JOINT-INTERFACE-01, based on Witness345 r6.",
    "TF192-H-WORLD and every other retained Time Stop qualification remain unchanged.",
    "Timeless Form remains pending; DF218-B03 remains open. This acceptance does not accept or apply Timeless Form.",
    "The witness cases are conditional authored-review evidence, not authenticated campaign events, runtime execution, or human playtests.",
    "The native catalog card and all class access/source rows remain byte-exact and blocked for runtime selection.",
    "No implementation, runtime, balance, cosmology, domain-closure, completion, or release gate is authorized.",
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def bind(path: pathlib.Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def bind_at(relative: pathlib.Path, raw: bytes) -> dict:
    return {"path": relative.as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def main() -> None:
    out_files = [DECISION_PATH, ACCEPTANCE_PATH, RECEIPT_PATH, APPLICATION_PATH, OPERATIONS_PATH,
                 VALIDATION_PATH, PENDING1, QUEUE1, HANDOFF1, SNAPSHOT1, BACKUP, MANUSCRIPT]
    assert not PKG.exists() and not STAGING.exists(), "Refusing to overwrite the Time Stop candidate package."
    assert all(not path.exists() for path in out_files), "Refusing to overwrite an existing Time Stop application output."

    before_raw = INDEX.read_bytes()
    catalog_raw = CATALOG.read_bytes()
    index0, catalog0 = read(INDEX), read(CATALOG)
    queue0, handoff0, pending0 = map(read, (QUEUE0, HANDOFF0, PENDING0))
    previous = read(OLD_PROCEDURE)
    entry0 = copy.deepcopy(next(row for row in index0["entries"] if row["id"] == ID))
    live0 = {row["id"] for row in index0["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    catalog_row = next(row for row in catalog0["spells"] if row["id"] == ID)
    assert index0["authoredCounts"] == {"reviewed": 823, "pending": 25}
    assert index0["representationCounts"]["completeReviewedStandaloneProcedures"] == 547
    assert pending0["authority"] == queue0["currentAuthority"] == handoff0["authority"] == BEFORE
    assert sha(before_raw) == pending0["indexBinding"]["sha256"] == queue0["currentIndexBinding"]["sha256"]
    assert pending0["pendingCount"] == queue0["pendingCount"] == 25 and set(pending0["pendingIds"]) == live0
    assert ID in live0 and entry0["authoredStatus"] == "pending-authored-procedure"
    assert entry0["sourceStatus"] == "blocked-pending-operational-review"
    assert catalog_row["status"] == "blocked-pending-operational-review" and catalog_row["operational"] is None
    assert previous["spellId"] == ID and previous["accepted"] is False and previous["applied"] is False
    assert previous["blockerIds"] == [BLOCKER] and BLOCKER in previous["holdIds"]
    assert not index0.get("additionalStandaloneEnvelopes") is None

    delivery, independent = read(DELIVERY), read(INDEPENDENT_REVIEW)
    generator = read(GENERATOR_AUDIT)
    assert delivery["scopeIds"] == [ID] and delivery["archive"]["sha256"] == EXPECTED_ARCHIVE_SHA
    assert delivery["authority"] == {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0,
                                     "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
    assert delivery["acceptedIds"] == delivery["appliedIds"] == delivery["heldIds"] == []
    assert delivery["applicationAuthorized"] is False and delivery["canonicalFilesChanged"] is False
    assert independent["status"] == "PASS" and all(check["passed"] for check in independent["checks"])
    assert len(independent["checks"]) == 29 and independent["authority"] == {
        "reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0}
    assert generator["status"] == "PASS" and generator["totalNewEvents"] == 179
    assert generator["totalForwardOperations"] == generator["totalInverseOperations"] == 358

    verify_run = subprocess.run(["python", str(VERIFIER)], cwd=ROOT, capture_output=True, text=True, check=True)
    verify_output = json.loads(verify_run.stdout)
    assert verify_output["status"] == "PASS" and verify_output["checks"] == 29 and not verify_output["failedChecks"]

    archive_raw = ARCHIVE.read_bytes()
    assert len(archive_raw) == delivery["archive"]["bytes"] == 16_940_751
    assert sha(archive_raw) == delivery["archive"]["sha256"] == EXPECTED_ARCHIVE_SHA
    archive_ref = bind(ARCHIVE, archive_raw)
    delivery_ref = bind(DELIVERY)
    generator_ref = bind(GENERATOR_AUDIT)
    independent_ref = bind(INDEPENDENT_REVIEW)
    verifier_ref = bind(VERIFIER)
    source_procedure_ref = bind(OLD_PROCEDURE)
    queue0_ref = bind(QUEUE0)
    handoff0_ref = bind(HANDOFF0)
    pending0_ref = bind(PENDING0)
    catalog_ref = bind(CATALOG, catalog_raw)
    index0_ref = bind(INDEX, before_raw)

    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        member_names = archive.namelist()
        assert len(member_names) == len(set(member_names)) == 34
        manifest = read_member(archive, "MEMBER_MANIFEST.json")
        member_rows = {row["path"]: row for row in manifest["members"]}
        assert manifest["memberCount"] == 34 and manifest["payloadMemberCount"] == 33
        for member, row in member_rows.items():
            raw = archive.read(member)
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"]
        new_case_refs = []
        for case_id in NEW_CASES:
            member = f"cases/new/{case_id}.json"
            row = member_rows[member]
            new_case_refs.append({"id": case_id, "archiveMember": member, "archiveMemberBinding": row})

    preserved_case_refs = []
    preserved_case_dir = A / "rank9_time_stop_return318_received/cases"
    for case_id in previous["caseIds"]:
        case_path = preserved_case_dir / f"{case_id}.json"
        assert case_path.exists(), f"Missing byte-exact preserved case: {case_id}"
        preserved_case_refs.append({"id": case_id, "binding": bind(case_path)})
    assert len(preserved_case_refs) == 14 and len(new_case_refs) == 3

    time = stamp()
    decision_id = "TIME-STOP-WITNESS345-DIRECTOR-DECISION"
    acceptance_id = "TIME-STOP-WITNESS345-EXACT-AUTHORED-ACCEPTANCE"
    application_id = "TIME-STOP-WITNESS345-AUTHORED-APPLICATION"
    retained_holds = [hold for hold in previous["holdIds"] if hold != BLOCKER]
    assert "TF192-H-WORLD" in retained_holds

    decision = {
        "id": decision_id,
        "recordedAtUtc": time,
        "status": "SEALED_ACCEPT_TIME_STOP_TF192_B01_WITNESS345_R6",
        "decision": "EXACT_ACCEPT",
        "identity": ID,
        "acceptedIds": [ID],
        "appliedIds": [],
        "heldIds": [],
        "closedBlockerIds": [BLOCKER],
        "accepted": True,
        "appliedAtDecision": False,
        "applicationAuthorized": True,
        "source": {"service": "ChatGPT", "conversationTitle": "Review Time Stop Witness Evidence", "url": DIRECTOR_URL},
        "exactDirectorResponse": DIRECTOR_TEXT,
        "witness345Archive": archive_ref,
        "deliveryManifest": delivery_ref,
        "independentReview": independent_ref,
        "generatorReplay": generator_ref,
        "verifier": verifier_ref,
        "authorityAtDecision": BEFORE,
        "authorityAfterApplicationExpected": AFTER,
        "acceptanceScope": "Time Stop / TF192-B01 only, under TF318-JOINT-INTERFACE-01 and Witness345 r6.",
        "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": retained_holds,
        "linkedPendingIdentity": "timeless-form",
        "linkedPendingBlockerIds": ["DF218-B03"],
        "otherSpellAccepted": False,
        "canonicalFilesChangedByDirector": False,
        "gatesStillClosed": ["runtime", "implementation", "human-play", "balance", "cosmology", "domain-closure", "completion", "release"],
    }
    write(DECISION_PATH, decision)
    decision_ref = bind(DECISION_PATH)

    procedure_record = copy.deepcopy(previous)
    procedure_record.update({
        "accepted": True,
        "applied": True,
        "blockerIds": [],
        "closedBlockerIds": [BLOCKER],
        "resolvedBlockerIds": [BLOCKER],
        "holdIds": retained_holds,
        "caseIds": previous["caseIds"] + NEW_CASES,
        "witnessCaseIds": NEW_CASES,
        "status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
        "directorDecisionBinding": decision_ref,
        "retainedQualifications": QUALIFICATIONS,
        "scope": "Time Stop only; close TF192-B01 using the accepted conditional Witness345 r6 branches. Preserve all other qualifications and keep runtime disabled.",
    })

    case_coverage = {
        "id": "TIME-STOP-WITNESS345-CASE-COVERAGE",
        "spellId": ID,
        "preservedCases": {"count": 14, "byteExact": True, "cases": preserved_case_refs},
        "acceptedConditionalWitnessCases": {
            "count": 3,
            "archive": archive_ref,
            "cases": new_case_refs,
            "newEvents": 179,
            "forwardOperations": 358,
            "inverseOperations": 358,
            "fullReplayAndReversalPassed": True,
        },
        "resolvedBlockerIds": [BLOCKER],
        "reviewedResiduals": {
            "R1": "Arcane Ward psychic selection agrees with the prepared Illusory Blade and Wizard card 57.",
            "R2": "The Universal case processes C's pending R1 slot at 0 ms before P's R2 slot at 6,000 ms; Reaction refreshes only at C's actual R1 START.",
            "R3": "P's Dispel target is 50 feet; C's self-origin target is 0 feet, consistently bound in perception, commitment, cast, resource and clock records.",
        },
        "scope": "Static authored conditional witness evidence; not runtime or authenticated campaign execution.",
    }
    coverage_rel = PKG_REL / "CASE_COVERAGE.json"
    coverage_raw = encode(case_coverage)
    coverage_ref = bind_at(coverage_rel, coverage_raw)

    evidence = {
        "id": "TIME-STOP-WITNESS345-EVIDENCE-BINDINGS",
        "sourceProcedure": source_procedure_ref,
        "directorDecision": decision_ref,
        "witnessArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "generatorReplay": generator_ref,
        "independentReview": independent_ref,
        "independentVerifier": verifier_ref,
        "queueBefore": queue0_ref,
        "handoffBefore": handoff0_ref,
        "pendingAuditBefore": pending0_ref,
        "indexBefore": index0_ref,
        "catalogBefore": catalog_ref,
        "jointInterfaceContract": pending0["timeStopJointInterfaceAuthorization"],
        "caseCoverage": coverage_ref,
        "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": retained_holds,
    }

    procedure_content = json.dumps(previous["procedure"], ensure_ascii=False, indent=2)
    model = {
        "schemaVersion": 1,
        "moduleId": "rank9timestop-reviewed-345",
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_TF192_B01_CLOSED_RUNTIME_DISABLED",
        "scope": "Time Stop / TF192-B01 only. The native catalog and runtime remain unchanged. Timeless Form, its DF218-B03 blocker, all retained Time Stop qualifications, and all unrelated dispositions remain pending or held.",
        "acceptedIds": [ID],
        "unacceptedIds": [],
        "excludedPendingIds": sorted(live0 - {ID}),
        "unresolvedQualifications": {ID: QUALIFICATIONS},
        "sharedRequirements": {"scope": "No global or shared rule changes; preserve all native catalog cards and class access; runtime selection disabled.", "runtimeSelectionEnabled": False},
        "spells": [{
            "id": ID,
            "name": "Time Stop",
            "position": 0,
            "procedure": {
                "id": "TF192-STATIC-TIME-STOP-345",
                "spellId": ID,
                "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                "accepted": True,
                "applied": True,
                "nativeCardUnchanged": copy.deepcopy(previous["currentCatalogSourceAndAccessUnchanged"]),
                "procedureContent": procedure_content,
                "sharedRequirements": copy.deepcopy(previous["sharedRequirements"]),
                "orderedExecution": copy.deepcopy(previous["orderedExecution"]),
                "holdIds": retained_holds,
                "caseIds": procedure_record["caseIds"],
                "questionIds": copy.deepcopy(previous["questionIds"]),
                "procedureRecordFile": "PROCEDURE_RECORD.json",
                "caseCoverageFile": "CASE_COVERAGE.json",
                "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
                "directorDecisionId": decision_id,
                "closedBlockerIds": [BLOCKER],
                "retainedQualifications": QUALIFICATIONS,
                "runtimeSelectionEnabled": False,
            },
            "directorProcedureRecord": procedure_record,
            "previousProcedureRecord": previous,
            "nativeCardUnchanged": copy.deepcopy(previous["currentCatalogSourceAndAccessUnchanged"]),
            "caseIds": procedure_record["caseIds"],
            "questionIds": copy.deepcopy(previous["questionIds"]),
            "retainedHoldIds": retained_holds,
            "retainedQualifications": QUALIFICATIONS,
            "runtimeSelectionEnabled": False,
        }],
        "sourceProcedure": source_procedure_ref,
        "witnessArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "generatorReplay": generator_ref,
        "independentReview": independent_ref,
        "independentVerifier": verifier_ref,
        "directorDecision": decision_ref,
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

    STAGING.mkdir(parents=True)
    write(STAGING / "PROCEDURE_RECORD.json", procedure_record)
    write(STAGING / "PREVIOUS_PROCEDURE_RECORD.json", previous)
    write(STAGING / "CASE_COVERAGE.json", case_coverage)
    write(STAGING / "EVIDENCE_BINDINGS.json", evidence)
    write(STAGING / "MODEL.json", model)
    manuscript = (
        "# Time Stop — accepted static authored procedure 345\n\n"
        "GPT sealed-accepted Time Stop / TF192-B01 after reviewing the corrected Witness345 r6 packet. The application records one accepted identity in the authored review index only. The native catalog, runtime selection, and downstream gates remain unchanged.\n\n"
        "## Accepted witness coverage\n\n"
        "The three conditional branches cover natural Action-mode completion, Universal-mode natural completion, and failed removal followed by a successful legal interruption. All 14 earlier Time Stop cases remain byte-exact. The 179 new events and 358 forward/inverse operations pass full replay and reversal.\n\n"
        "Residuals R1–R3 are closed: Arcane Ward selects psychic consistently; C's Universal round-one regular slot and Reaction refresh are ordered before P's round-two slot; and the Dispel geometries are consistently 50 feet for P and 0 feet for C's self-origin target.\n\n"
        "## Retained qualifications\n\n" + "\n".join(f"- {item}" for item in QUALIFICATIONS) + "\n"
    )
    (STAGING / "STANDALONE_PROCEDURES.md").write_text(manuscript, encoding="utf-8", newline="\n")
    package_manifest = {
        "id": "TIME-STOP-WITNESS345-CANDIDATE-PACKAGE-MANIFEST",
        "directorDecision": decision_ref,
        "sourceProcedure": source_procedure_ref,
        "witnessArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "independentReview": independent_ref,
        "files": [],
    }
    for file in sorted(path for path in STAGING.rglob("*") if path.is_file()):
        raw = file.read_bytes()
        package_manifest["files"].append(bind_at(PKG_REL / file.relative_to(STAGING), raw))
    write(STAGING / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    STAGING.rename(PKG)

    model_ref = bind(PKG / "MODEL.json")
    manifest_ref = bind(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
    coverage_ref = bind(PKG / "CASE_COVERAGE.json")
    evidence_ref = bind(PKG / "EVIDENCE_BINDINGS.json")
    manuscript_ref = bind(MANUSCRIPT, manuscript.encode("utf-8"))
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")

    acceptance = {
        "id": acceptance_id,
        "recordedAtUtc": time,
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AWAITING_APPLICATION",
        "acceptedIds": [ID],
        "appliedIds": [],
        "heldIds": [],
        "closedBlockerIds": [BLOCKER],
        "applicationAuthorized": True,
        "directorDecision": decision_ref,
        "sourceProcedure": source_procedure_ref,
        "witnessArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "generatorReplay": generator_ref,
        "independentReview": independent_ref,
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": manifest_ref,
        "evidenceBindings": evidence_ref,
        "caseCoverage": coverage_ref,
        "countsBefore": BEFORE,
        "countsAfterAcceptanceBeforeApplication": {
            "reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 1,
            "completeStandaloneProcedures": 547, "scopedInterfaces": 173,
        },
        "countsAfterApplicationExpected": AFTER,
        "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": retained_holds,
    }
    write(ACCEPTANCE_PATH, acceptance)
    acceptance_ref = bind(ACCEPTANCE_PATH)
    receipt = {
        "id": "TIME-STOP-WITNESS345-RETURN-RECEIPT",
        "recordedAtUtc": time,
        "status": "SEALED_ACCEPT_TIME_STOP_TF192_B01_ONLY",
        "acceptedIds": [ID],
        "appliedIds": [],
        "heldIds": [],
        "closedBlockerIds": [BLOCKER],
        "applicationAuthorized": True,
        "directorDecision": decision_ref,
        "acceptance": acceptance_ref,
        "witnessArchive": archive_ref,
        "independentReview": independent_ref,
        "retainedHoldIds": retained_holds,
        "sourceResponse": DIRECTOR_TEXT,
    }
    write(RECEIPT_PATH, receipt)
    receipt_ref = bind(RECEIPT_PATH)

    index1 = copy.deepcopy(index0)
    entry1 = copy.deepcopy(entry0)
    entry1.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank9timestop_reviewed_345/MODEL.json",
        "procedurePointer": "/spells/0/procedure",
        "wholeCardPointer": "/spells/0",
        "sourceCatalogWholeCardPointer": entry0.get("sourceCatalogWholeCardPointer") or entry0["wholeCardPointer"],
        "wholeCardIdField": "id",
        "procedureTextPointer": "/spells/0/procedure/procedureContent",
        "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
        "sharedRulesPointer": "/spells/0/procedure/sharedRequirements",
        "spellLocalRequirementsPointer": "/spells/0/procedure",
        "manuscript": "../../../docs/spells/candidates/TIME_STOP_REVIEWED_345.md",
        "reviewId": application_id,
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
        "authoredApplicationReceipt": application_id + ".json",
        "directorReturnReceipt": receipt_ref,
        "accepted": True,
        "applied": True,
        "closedBlockerIds": [BLOCKER],
        "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": retained_holds,
        "sourceStatus": "blocked-pending-operational-review",
        "priorCatalogSelectionStatusUnchanged": True,
    })
    entry_i = next(i for i, row in enumerate(index1["entries"]) if row["id"] == ID)
    index1["entries"][entry_i] = entry1
    excluded_pending = sorted(live0 - {ID})
    envelope = {
        "file": "../spell_candidates/rank9timestop_reviewed_345/MODEL.json",
        "binding": model_ref,
        "reviewId": acceptance_id,
        "acceptedIds": [ID],
        "unacceptedIds": [],
        "excludedPendingIds": excluded_pending,
        "authority": acceptance_ref,
        "applicationReceipt": application_id + ".json",
        "directorDecision": decision_ref,
        "directorReturnReceipt": receipt_ref,
        "sourceArchive": archive_ref,
        "sourceDeliveryManifest": delivery_ref,
        "independentReview": independent_ref,
        "caseCoverage": coverage_ref,
        "procedureSource": source_procedure_ref,
        "candidatePackageManifestBinding": manifest_ref,
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_TF192_B01_CLOSED_RUNTIME_DISABLED",
        "runtimeSelectionEnabled": False,
    }
    index1["additionalStandaloneEnvelopes"].append(envelope)
    index1["authoredCounts"] = {"reviewed": 824, "pending": 24}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"] = 548
    live1 = {row["id"] for row in index1["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert live1 == live0 - {ID} and len(live1) == 24 and "timeless-form" in live1
    BACKUP.write_bytes(before_raw)
    assert BACKUP.read_bytes() == before_raw
    write(INDEX, index1)
    index_core_ref = bind(INDEX)

    application = {
        "id": application_id,
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
        "witnessArchive": archive_ref,
        "deliveryManifest": delivery_ref,
        "generatorReplay": generator_ref,
        "independentReview": independent_ref,
        "candidateEnvelope": model_ref,
        "candidatePackageManifest": manifest_ref,
        "caseCoverage": coverage_ref,
        "evidenceBindings": evidence_ref,
        "manuscript": manuscript_ref,
        "indexBefore": bind(BACKUP, before_raw),
        "indexAfterCoreUpdate": index_core_ref,
        "countsBefore": BEFORE,
        "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": 547, "after": 548},
        "scopedInterfaces": 173,
        "catalogChanged": False,
        "sourceStatusPreservedAsBlocked": True,
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
    index1["entries"][entry_i] = entry1
    index1["additionalStandaloneEnvelopes"][-1]["applicationReceipt"] = application_ref
    write(INDEX, index1)
    index_ref = bind(INDEX)

    operations = {
        "id": "TIME-STOP-WITNESS345-INDEX-OPERATIONS",
        "recordedAtUtc": time,
        "before": bind(BACKUP, before_raw),
        "after": index_ref,
        "operations": [
            {"op": "update-entry", "id": ID, "before": entry0, "after": entry1},
            {"op": "append-standalone-envelope", "acceptedIds": [ID]},
            {"op": "update-authored-counts", "before": {"reviewed": 823, "pending": 25}, "after": {"reviewed": 824, "pending": 24}},
            {"op": "increment-complete-procedure-count", "before": 547, "after": 548},
        ],
        "inverse": [
            {"op": "restore-entry", "id": ID, "value": entry0},
            {"op": "remove-appended-standalone-envelope", "acceptedIds": [ID]},
            {"op": "restore-authored-counts", "value": {"reviewed": 823, "pending": 25}},
            {"op": "restore-complete-procedure-count", "value": 547},
            {"op": "restore-byte-exact-index-from-backup", "backup": bind(BACKUP, before_raw)},
        ],
        "catalogByteExact": CATALOG.read_bytes() == catalog_raw,
        "nativeCardUnchanged": True,
        "sourceStatusPreservedAsBlocked": True,
        "inverseRestoresExactIndex": BACKUP.read_bytes() == before_raw,
    }
    write(OPERATIONS_PATH, operations)
    operations_ref = bind(OPERATIONS_PATH)

    pending_path_ref = PENDING1.relative_to(ROOT).as_posix()
    queue1 = copy.deepcopy(queue0)
    queue1.update({
        "id": "SPELL-REVIEW-QUEUE-344",
        "recordedAtUtc": time,
        "supersedesQueue": bind(QUEUE0),
        "currentAuthority": AFTER,
        "currentIndexBinding": index_ref,
        "currentCatalogBinding": catalog_ref,
        "pendingCount": 24,
        "acceptedUnapplied": 0,
        "nextGroup": None,
        "nextPendingIds": [],
        "nextPendingCount": 0,
        "activeReview": None,
        "next": None,
        "continuingPriorityOrder": [item for item in queue0["continuingPriorityOrder"] if item != ID],
        "closureTasksRemaining": 24,
        "firstReviewTasksRemaining": 0,
        "allPendingGroupsReviewed": True,
        "unreviewedPendingIds": [],
        "lastDirectorReturn": decision_id,
        "currentReturnAcceptedIds": [ID],
        "currentReturnAppliedIds": [ID],
        "currentReturnHeldIds": [],
        "currentReturnBlockers": {k: v for k, v in queue0.get("currentReturnBlockers", {}).items() if k != ID},
        "currentReturnDecision": decision_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": independent_ref,
        "currentSourcePacket": archive_ref,
        "currentPreparation": None,
        "currentPacketStatus": "WITNESS345_SEALED_ACCEPT_TIME_STOP_TF192_B01_APPLIED; 24_CLOSURE_TASKS_REMAIN",
        "pendingIdentityAudit": pending_path_ref,
        "directorConnectionStatus": "GPT sealed-accepted and explicitly authorized application of Time Stop / TF192-B01 only. The 24 other closure tasks and unrelated holds remain unchanged.",
        "githubChanges": False,
        "canonicalFilesChanged": True,
        "applicationPerformed": True,
        "currentReturnReceipt": receipt_ref,
        "currentPendingIdentityAudit": pending_path_ref,
        "currentHandoff": HANDOFF1.relative_to(ROOT).as_posix(),
        "acceptedThisStep": [ID],
        "appliedThisStep": [ID],
        "currentDirectorInstruction": "W345 sealed acceptance authorizes only Time Stop application. Request Director-prioritized changed closure work for the remaining 24 tasks; no other identity was accepted.",
        "heldThisStep": [],
        "currentReview": None,
        "timeStopDisposition": {
            "held": False,
            "blockerIds": [],
            "closedBlockerIds": [BLOCKER],
            "accepted": True,
            "applied": True,
            "applicationAuthorized": True,
            "jointInterfaceAuthorizationId": CONTRACT_ID,
            "jointInterfaceStatus": "WITNESS345_SEALED_ACCEPT_TIME_STOP_ONLY",
            "retainedHoldIds": retained_holds,
            "linkedPendingComparisonId": "timeless-form",
            "linkedPendingBlockerIds": ["DF218-B03"],
        },
    })
    write(QUEUE1, queue1)
    queue1_ref = bind(QUEUE1)

    pending1 = copy.deepcopy(pending0)
    pending1.update({
        "id": "SPELL-REVIEW-CURRENT24-PENDING-IDENTITY-AUDIT-344",
        "recordedAtUtc": time,
        "status": "PASS_CURRENT_824_24_TIME_STOP_TF192_B01_ACCEPTED_AND_APPLIED_WITNESS345",
        "supersedes": PENDING0.name,
        "authority": AFTER,
        "indexBinding": index_ref,
        "catalogBinding": catalog_ref,
        "pendingCount": 24,
        "pendingIds": sorted(live1),
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "unreviewedPendingIds": [],
        "firstReviewTasksRemaining": 0,
        "closureTasksRemaining": 24,
        "nextGroup": None,
        "nextPendingIds": [],
        "nextPendingCount": 0,
        "nextStep": "Time Stop / TF192-B01 was accepted and applied. Consult the Director for a changed closure delta and priority among the 24 remaining closure tasks; do not re-run unchanged holds.",
        "sourceQueue": QUEUE1.relative_to(ROOT).as_posix(),
        "canonicalFilesChanged": True,
        "heldThisStep": [],
        "timeStopBlockers": [],
        "currentQueueBinding": queue1_ref,
        "applicationPerformed": True,
        "currentReturn": decision_ref,
        "currentReturnReceipt": receipt_ref,
        "currentHandoff": HANDOFF1.relative_to(ROOT).as_posix(),
        "closedBlockerIdsThisStep": [BLOCKER],
        "lastDirectorReturn": {
            "decisionId": decision_id,
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
    closed = list(dict.fromkeys(handoff0.get("closedBlockerIds", []) + [BLOCKER]))
    handoff1.update({
        "id": "CURRENT-HANDOFF-344",
        "recordedAtUtc": time,
        "supersedes": handoff0["id"],
        "status": "TIME_STOP_TF192_B01_ACCEPTED_AND_APPLIED_824_24_0",
        "authority": AFTER,
        "currentAuthority": AFTER,
        "continuingPriorityOrder": [item for item in handoff0.get("continuingPriorityOrder", []) if item != ID],
        "scopeIds": [ID],
        "blockerIds": [],
        "indexBinding": index_ref,
        "queue": QUEUE1.relative_to(ROOT).as_posix(),
        "queueBinding": queue1_ref,
        "pendingIdentityAudit": pending1_ref,
        "pendingIdentityAuditBinding": pending1_ref,
        "appliedThisStep": True,
        "acceptedThisStep": [ID],
        "heldThisStep": [],
        "currentBlocker": None,
        "nextPendingGroup": None,
        "nextStep": "Ask GPT to prioritize a changed closure delta among the 24 remaining tasks; preserve all unrelated holds and CLOSED dispositions.",
        "closureTasksRemaining": 24,
        "firstReviewTasksRemaining": 0,
        "directorConnectionStatus": "GPT returned SEALED ACCEPT for Time Stop / TF192-B01 only and explicitly authorized canonical authored-index application.",
        "directorReturnDecision": decision_ref,
        "directorReturnArchive": archive_ref,
        "directorReturnDelivery": delivery_ref,
        "directorReturnAudit": independent_ref,
        "applicationPerformed": True,
        "canonicalFilesChanged": True,
        "closedBlockerIds": closed,
        "acceptedIds": [ID],
        "appliedIds": [ID],
        "currentDirectorInstruction": decision_ref,
        "currentReturnReceipt": receipt_ref,
        "currentDirectorReturn": decision_ref,
        "currentDirectorDelivery": delivery_ref,
        "currentReturnAudit": independent_ref,
        "currentReadbackAudit": independent_ref,
        "currentReturn": decision_ref,
        "currentReturnArchive": archive_ref,
        "currentReturnDelivery": delivery_ref,
        "currentReturnAuditBinding": independent_ref,
        "currentPreparation": None,
        "nextStepText": "Request the Director's next changed closure priority; 24 closure tasks remain, with no first-review identities outstanding.",
    })
    write(HANDOFF1, handoff1)
    handoff1_ref = bind(HANDOFF1)

    checks = [
        ("GPT sealed-accepted only Time Stop and authorized application", decision["acceptedIds"] == [ID] and decision["applicationAuthorized"] and decision["closedBlockerIds"] == [BLOCKER]),
        ("Witness345 r6 archive hash and independent checks pass", archive_ref["sha256"] == EXPECTED_ARCHIVE_SHA and independent["status"] == "PASS" and len(independent["checks"]) == 29 and all(c["passed"] for c in independent["checks"])),
        ("Exact Queue343 baseline was bound", pending0["authority"] == queue0["currentAuthority"] == BEFORE and index0_ref["sha256"] == pending0["indexBinding"]["sha256"]),
        ("Only Time Stop leaves the pending set", live1 == live0 - {ID} and len(live1) == 24),
        ("Authority advances to 824/24/0 and 548/173", index1["authoredCounts"] == {"reviewed": 824, "pending": 24} and index1["representationCounts"]["completeReviewedStandaloneProcedures"] == 548),
        ("Timeless Form and DF218-B03 remain pending", "timeless-form" in live1 and decision["linkedPendingBlockerIds"] == ["DF218-B03"]),
        ("TF192-H-WORLD and all other Time Stop qualifications remain", "TF192-H-WORLD" in retained_holds and set(previous["holdIds"]) - {BLOCKER} == set(retained_holds)),
        ("Native catalog remains byte-exact and blocked", CATALOG.read_bytes() == catalog_raw and catalog_row["status"] == "blocked-pending-operational-review" and entry1["sourceStatus"] == "blocked-pending-operational-review"),
        ("Runtime and downstream gates remain disabled", model["runtimeSelectionEnabled"] is False and model["implementationApproved"] is False and model["releaseApproved"] is False),
        ("Backup restores exact pre-application index bytes", BACKUP.read_bytes() == before_raw),
        ("Pending audit, queue and handoff bind final index and authority", pending1["indexBinding"]["sha256"] == index_ref["sha256"] and queue1["currentIndexBinding"]["sha256"] == index_ref["sha256"] and handoff1["indexBinding"]["sha256"] == index_ref["sha256"] and handoff1["queueBinding"]["sha256"] == queue1_ref["sha256"]),
        ("Handoff closure and first-review counts match Queue344 and its pending audit", handoff1["closureTasksRemaining"] == queue1["closureTasksRemaining"] == pending1["closureTasksRemaining"] == 24 and handoff1["firstReviewTasksRemaining"] == queue1["firstReviewTasksRemaining"] == pending1["firstReviewTasksRemaining"] == 0),
        ("Applied Time Stop is removed from the continuing priority order", ID not in handoff1["continuingPriorityOrder"] and handoff1["continuingPriorityOrder"] == queue1["continuingPriorityOrder"]),
        ("Preserved and new conditional case counts are 14 and 3", len(preserved_case_refs) == 14 and len(new_case_refs) == 3 and case_coverage["acceptedConditionalWitnessCases"]["newEvents"] == 179),
        ("No other spell was accepted or applied", acceptance["acceptedIds"] == acceptance["closedBlockerIds"][:0] + [ID] and application["appliedIds"] == [ID] and len(live1) == 24),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation = {
        "id": "TIME-STOP-WITNESS345-APPLICATION-VALIDATION",
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
        "# Spell review snapshot — Time Stop Witness345 application\n\n"
        "Authority: **824 applied / 24 pending / 0 accepted-unapplied; 548 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "GPT sealed-accepted and explicitly authorized application of `time-stop` / `TF192-B01` only after reviewing Witness345 r6. R1–R3 are closed. Timeless Form / `DF218-B03`, all retained Time Stop qualifications, and every unrelated disposition remain unchanged. The native catalog and runtime remain blocked.\n\n"
        f"Validation: `{validation_ref['path']}` (SHA-256 `{validation_ref['sha256']}`).\n",
        encoding="utf-8", newline="\n")

    assert CATALOG.read_bytes() == catalog_raw and sha(INDEX.read_bytes()) == index_ref["sha256"]
    final_index = read(INDEX)
    assert final_index["authoredCounts"] == {"reviewed": 824, "pending": 24}
    final_row = next(row for row in final_index["entries"] if row["id"] == ID)
    assert final_row["accepted"] is True and final_row["applied"] is True and final_row["closedBlockerIds"] == [BLOCKER]
    print(json.dumps({
        "status": "PASS",
        "acceptedApplied": ID,
        "closedBlockerIds": [BLOCKER],
        "authority": AFTER,
        "archive": archive_ref,
        "index": bind(INDEX),
        "application": application_ref,
        "validation": validation_ref,
        "pendingAudit": pending1_ref,
        "queue": queue1_ref,
        "handoff": handoff1_ref,
    }, ensure_ascii=False, indent=2))


def read_member(archive: zipfile.ZipFile, name: str):
    return json.loads(archive.read(name).decode("utf-8-sig"))


if __name__ == "__main__":
    main()
