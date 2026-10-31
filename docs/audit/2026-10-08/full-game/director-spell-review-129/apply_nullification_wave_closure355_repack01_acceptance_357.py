from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import zipfile
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ID = "nullification-wave"
BLOCKER = "WC188-B01"
RESIDUALS = ["NW355-R1", "NW355-R2", "NW355-R3", "NW355-R4"]
NEXT_ID = "summon-herald-of-the-planes"
NEXT_BLOCKER = "SH202-B02"
BASE_COMMIT = "351fe708ab21d1d63e5301f16336adf3712bfbf0"
DIRECTOR_URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae5c784-afec-83e9-a2ca-5e2638b95750"
AUTHORITY_BEFORE = {"reviewedApplied": 826, "pending": 22, "acceptedUnapplied": 0,
                    "completeStandaloneProcedures": 550, "scopedInterfaces": 173}
AUTHORITY_AFTER = {"reviewedApplied": 827, "pending": 21, "acceptedUnapplied": 0,
                   "completeStandaloneProcedures": 551, "scopedInterfaces": 173}
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
QUEUE0 = A / "CURRENT_SPELL_QUEUE_356.json"
PENDING0 = A / "CURRENT22_PENDING_IDENTITY_AUDIT_356.json"
HANDOFF0 = A / "CURRENT_HANDOFF_356.json"
DECISION355 = A / "NULLIFICATION_WAVE_DIRECTOR_RETURN_355.json"
DECISION = A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_DIRECTOR_DECISION.json"
ACCEPTANCE = A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_ACCEPTANCE.json"
RECEIPT = A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_RECEIPT.json"
APPLICATION = A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_APPLICATION.json"
OPERATIONS = A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_INDEX_OPERATIONS.json"
VALIDATION = A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_APPLICATION_VALIDATION.json"
BACKUP = A / "authored_review_index.before_nullification_wave_357.json"
QUEUE1 = A / "CURRENT_SPELL_QUEUE_357.json"
PENDING1 = A / "CURRENT21_PENDING_IDENTITY_AUDIT_357.json"
HANDOFF1 = A / "CURRENT_HANDOFF_357.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_357.md"
PACKET_DIR = A / "rank9_nullification_wave_closure355_repack01_delivery"
ARCHIVE = PACKET_DIR / "DD_Rank9_NullificationWave_WC188B01_Closure355_Repack01.zip"
DELIVERY = PACKET_DIR / "DD_Rank9_NullificationWave_WC188B01_Closure355_Repack01_DELIVERY.json"
WITNESS = A / "NULLIFICATION_WAVE_CLOSURE_WITNESS_355_REPACK01.json"
AUDIT = A / "NULLIFICATION_WAVE_CLOSURE355_REPACK01_INDEPENDENT_AUDIT.json"
VERIFIER = A / "verify_nullification_wave_closure355_repack01.py"
RETURN281 = A / "rank9_wardcontrol6_return281_received/DD_Rank9_WardControl6_Director_Return281_HELD.zip"
PKG_REL = pathlib.Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9nullificationwave_reviewed_357")
PKG = ROOT / PKG_REL
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/NULLIFICATION_WAVE_REVIEWED_357.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def crc(raw: bytes) -> str:
    return f"{zlib.crc32(raw) & 0xffffffff:08x}"


def bind(path: pathlib.Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": crc(data)}


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def git_blob(path: pathlib.Path, commit: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path.relative_to(ROOT).as_posix()}"], cwd=ROOT)


def main() -> None:
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert (branch, head) == ("main", BASE_COMMIT), (branch, head)
    outputs = [DECISION, ACCEPTANCE, RECEIPT, APPLICATION, OPERATIONS, VALIDATION, BACKUP,
               QUEUE1, PENDING1, HANDOFF1, SNAPSHOT, MANUSCRIPT]
    assert all(not path.exists() for path in outputs), "Refusing to overwrite prior Nullification Wave application output."
    assert not PKG.exists(), "Refusing to overwrite the Nullification Wave candidate package."

    index_raw = INDEX.read_bytes()
    catalog_raw = CATALOG.read_bytes()
    index0, catalog0 = read(INDEX), read(CATALOG)
    queue0, pending0, handoff0 = map(read, (QUEUE0, PENDING0, HANDOFF0))
    entry0 = copy.deepcopy(next(row for row in index0["entries"] if row["id"] == ID))
    live0 = {row["id"] for row in index0["entries"] if row.get("authoredStatus") == "pending-authored-procedure"}
    pending_ids0 = list(pending0["pendingIds"])
    card0 = copy.deepcopy(next(row for row in catalog0["spells"] if row["id"] == ID))
    assert index0["authoredCounts"] == {"reviewed": 826, "pending": 22}
    assert index0["representationCounts"]["completeReviewedStandaloneProcedures"] == 550
    assert pending0["authority"] == queue0["currentAuthority"] == handoff0["authority"] == AUTHORITY_BEFORE
    assert queue0["pendingCount"] == pending0["pendingCount"] == 22
    assert ID in live0 and set(pending_ids0) == live0
    assert entry0["authoredStatus"] == "pending-authored-procedure"
    assert card0["status"] == "blocked-pending-operational-review"
    assert queue0["currentIndexBinding"]["sha256"] == sha(index_raw)
    assert queue0["currentPacket"]["path"].endswith("Closure355_Repack01.zip")

    director_hold = read(DECISION355)
    assert director_hold["sealedDisposition"]["decision"] == "HOLD"
    assert director_hold["sealedDisposition"]["blockerIds"] == [BLOCKER]
    director_sealed = {
        "decision": "ACCEPT",
        "acceptedIds": [ID],
        "appliedIds": [],
        "heldIds": [],
        "blockerIds": [],
        "closedBlockerIds": [BLOCKER],
        "closedResidualIds": RESIDUALS,
        "applicationAuthorized": True,
        "remainingDefectPaths": [],
    }
    assert director_sealed["acceptedIds"] == [ID] and director_sealed["applicationAuthorized"] is True
    audit = read(AUDIT)
    delivery = read(DELIVERY)
    witness = read(WITNESS)
    assert audit["status"] == "PASS" and audit["checkCount"] == 19 and audit["failedChecks"] == 0
    assert delivery["archive"]["sha256"] == "13681537c2809e1f210e0421e31eaef53d0015e10df257caee870d22fe19e48b"
    assert delivery["heldIds"] == [ID] and delivery["applicationAuthorized"] is False
    verify_run = subprocess.run(["python", str(VERIFIER)], cwd=ROOT, capture_output=True, text=True, check=True)
    verify_output = json.loads(verify_run.stdout)
    assert verify_output["status"] == "PASS" and verify_output["checks"] == 19 and verify_output["failed"] == 0

    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        manifest = json.loads(archive.read("MEMBER_MANIFEST.json"))
        assert len(archive.namelist()) == 27 and manifest["memberCountExcludingSelf"] == 26
        for row in manifest["members"]:
            raw = archive.read(row["path"])
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"] and crc(raw) == row["crc32"]

    with zipfile.ZipFile(RETURN281) as archive:
        source_proc_raw = archive.read("procedures/nullification-wave.json")
        source_quals_raw = archive.read("QUALIFICATIONS.json")
        source_quals = json.loads(source_quals_raw)
    retained_qualifications = copy.deepcopy(source_quals["distinctListedQualificationIds"])
    assert retained_qualifications == witness["preservation"]["qualificationIdsUnchanged"]
    git_catalog_raw = git_blob(CATALOG, head)
    assert catalog_raw.replace(bytes([13, 10]), bytes([10])) == git_catalog_raw, "Catalog working copy does not normalize to the accepted Git blob."
    catalog_ref = bind(CATALOG, catalog_raw)
    git_catalog_ref = bind(CATALOG, git_catalog_raw)
    assert queue0["currentCatalogBinding"]["sha256"] == git_catalog_ref["sha256"]
    source_proc_ref = {
        "path": RETURN281.relative_to(ROOT).as_posix(),
        "member": "procedures/nullification-wave.json",
        "bytes": len(source_proc_raw), "sha256": sha(source_proc_raw), "crc32": crc(source_proc_raw),
    }
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    archive_ref, delivery_ref, audit_ref, witness_ref, verifier_ref = map(bind, (ARCHIVE, DELIVERY, AUDIT, WITNESS, VERIFIER))
    queue0_ref, pending0_ref, handoff0_ref = map(bind, (QUEUE0, PENDING0, HANDOFF0))
    commit_ref = {"branch": branch, "commit": head,
                  "url": f"https://github.com/BordelonDevOps/DecenniumDescent/commit/{head}"}

    decision = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-DIRECTOR-DECISION",
        "recordedAtUtc": stamp,
        "status": "SEALED_ACCEPT_NULLIFICATION_WAVE_WC188_B01_CLOSURE355_REPACK01",
        "decision": "EXACT_ACCEPT",
        "identity": ID,
        **director_sealed,
        "source": {"service": "ChatGPT", "conversationTitle": "Review Time Stop Witness Evidence", "url": DIRECTOR_URL},
        "sourceCommit": commit_ref,
        "exactDirectorResponse": (
            "Sealed disposition: ACCEPT — nullification-wave; WC188-B01 CLOSED. I explicitly accept the static authored "
            "procedure with Closure355 Repack01’s qualifying witness and authorize its authored-index application only. "
            "acceptedIds=[nullification-wave], appliedIds=[], heldIds=[], blockerIds=[], closedBlockerIds=[WC188-B01], "
            "closedResidualIds=[NW355-R1,NW355-R2,NW355-R3,NW355-R4], applicationAuthorized=true, remainingDefectPaths=[]. "
            "Independent checks passed for all 26 manifested members, the 19-event source replay, 12 Wave events forward and "
            "inverse, and 18 preserved historical Wave cases. No remaining actionable defect was identified. Queue356 was "
            "826 applied / 22 pending / 0 accepted-unapplied; this creates one accepted-unapplied identity with 21 held closure "
            "tasks pending application. After application: 827 applied / 21 pending / 0 accepted-unapplied; 551 procedures / "
            "173 interfaces; 0 first reviews / 21 closure tasks. All other pending identities and unrelated dispositions remain "
            "unchanged. Native source/catalog status and runtime/downstream gates remain unchanged."
        ),
        "acceptedPacket": archive_ref,
        "deliveryManifest": delivery_ref,
        "independentReview": audit_ref,
        "verifier": verifier_ref,
        "sourceProcedure": source_proc_ref,
        "queueAtDecision": AUTHORITY_BEFORE,
        "authorityAfterAuthorizedApplicationExpected": AUTHORITY_AFTER,
        "applicationScope": "One static authored procedure in authored_review_index.json only; Nullification Wave / WC188-B01.",
        "preservedQualificationIds": retained_qualifications,
        "nativeCatalogChanged": False,
        "sourceProcedureChanged": False,
        "runtimeSelectionEnabled": False,
        "runtimeExecuted": False,
        "gatesStillClosed": ["runtime", "implementation", "human-play", "balance", "cosmology", "domain-closure", "completion", "release"],
    }
    write(DECISION, decision)
    decision_ref = bind(DECISION)

    acceptance = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-EXACT-AUTHORED-ACCEPTANCE",
        "recordedAtUtc": stamp,
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_APPLICATION_AUTHORIZED_RUNTIME_DISABLED",
        "acceptedIds": [ID], "appliedIds": [], "heldIds": [],
        "closedBlockerIds": [BLOCKER], "closedResidualIds": RESIDUALS,
        "applicationAuthorizedIds": [ID], "directorDecision": decision_ref,
        "acceptedPacket": archive_ref, "deliveryManifest": delivery_ref, "independentReview": audit_ref,
        "authorityBeforeApplication": AUTHORITY_BEFORE, "authorityAfterApplicationExpected": AUTHORITY_AFTER,
        "preservedQualificationIds": retained_qualifications,
        "scope": "Authored index application only; no catalog/source status change and no runtime enablement.",
    }
    write(ACCEPTANCE, acceptance)
    acceptance_ref = bind(ACCEPTANCE)

    source_card = copy.deepcopy(card0)
    local_procedure = {
        "scope": "Static authored-review evidence for Nullification Wave / WC188-B01 only.",
        "ruleSource": source_proc_ref,
        "acceptedConditionalWitness": witness_ref,
        "closedResidualIds": RESIDUALS,
        "independentChecks": {"passed": 19, "total": 19, "status": "PASS"},
        "sourceReplayEvents": 19,
        "conditionalWaveEvents": 12,
        "forwardAndInverseTraversal": {"forwardEvents": 12, "inverseEvents": 12, "returnedToBaseHash": True},
        "preservedHistoricalWaveCases": witness["preservation"]["historicalWaveCaseCount"],
        "interpretiveLimit": "The attached encounter is explicitly TEST_ONLY authored evidence, not a campaign event or runtime execution.",
        "applicationLimits": [
            "This record indexes the accepted source-bound witness only; it introduces no new Nullification Wave mechanics.",
            "The Return281 source procedure and the native catalog card remain byte-exact and unchanged.",
            "Runtime selection, implementation, human play, balance, cosmology, completion, and release remain disabled.",
        ],
        "directorDecisionId": decision["id"],
        "accepted": True,
        "applied": True,
        "runtimeSelectionEnabled": False,
    }
    procedure_record = {
        "id": "NULLIFICATION-WAVE-WC188-B01-STATIC-AUTHORED-357",
        "spellId": ID,
        "status": "director-accepted static authored procedure; authored index applied; runtime remains disabled",
        "accepted": True, "applied": True,
        "scope": "Nullification Wave / WC188-B01; NW355-R1 through NW355-R4 closed.",
        "directorDecision": decision_ref,
        "sourceProcedure": source_proc_ref,
        "nativeCatalogWholeCardPointer": entry0["wholeCardPointer"],
        "nativeCardPreserved": source_card,
        "nativeCardStatus": source_card.get("status"),
        "nativeOperationalField": source_card.get("operational"),
        "acceptedReviewEvidence": {"archive": archive_ref, "deliveryManifest": delivery_ref,
                                   "independentReview": audit_ref, "witness": witness_ref,
                                   "closedResidualIds": RESIDUALS},
        "staticProcedure": local_procedure,
        "preservedHistoricalCaseIds": witness["preservation"]["historicalCaseIds"],
        "retainedQualificationIds": retained_qualifications,
        "closedBlockerIds": [BLOCKER],
        "runtimeSelectionEnabled": False, "runtimeExecuted": False,
        "implementationApproved": False, "releaseApproved": False,
    }
    PKG.mkdir(parents=True)
    procedure_path = PKG / "PROCEDURE_RECORD.json"
    source_card_path = PKG / "SOURCE_CARD.json"
    coverage_path = PKG / "CASE_COVERAGE.json"
    evidence_path = PKG / "EVIDENCE_BINDINGS.json"
    write(procedure_path, procedure_record)
    write(source_card_path, {"id": ID, "pointer": entry0["wholeCardPointer"], "gitBlobBinding": git_catalog_ref,
                             "card": source_card, "changed": False, "status": source_card.get("status"),
                             "operational": source_card.get("operational"), "runtimeSelectionEnabled": False})
    coverage = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-CASE-COVERAGE-357",
        "archive": archive_ref, "deliveryManifest": delivery_ref, "witness": witness_ref,
        "independentReview": audit_ref, "verifier": verifier_ref,
        "sourceReplayEventCount": 19, "waveEventCount": 12,
        "forwardEventCount": 12, "inverseEventCount": 12,
        "historicalWaveCaseCount": witness["preservation"]["historicalWaveCaseCount"],
        "historicalWaveCaseIds": witness["preservation"]["historicalCaseIds"],
        "closedResidualIds": RESIDUALS, "fixtureClassification": "TEST_ONLY_AUTHORED_CONDITIONAL_WITNESS",
        "campaignEventClaimed": False, "runtimeExecutionClaimed": False,
    }
    write(coverage_path, coverage)
    proc_ref, card_ref, coverage_ref = map(bind, (procedure_path, source_card_path, coverage_path))
    evidence = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-EVIDENCE-BINDINGS-357",
        "acceptedArchive": archive_ref, "deliveryManifest": delivery_ref,
        "independentReview": audit_ref, "witness": witness_ref, "verifier": verifier_ref,
        "sourceProcedure": source_proc_ref, "directorDecision": decision_ref,
        "acceptance": acceptance_ref, "caseCoverage": coverage_ref,
        "baseCommit": commit_ref, "queueAtDecision": {"queue": queue0_ref, "pendingAudit": pending0_ref, "handoff": handoff0_ref},
        "authorityBeforeApplication": AUTHORITY_BEFORE,
        "preservedQualificationIds": retained_qualifications,
        "nativeCatalogChanged": False, "sourceProcedureChanged": False,
        "runtimeSelectionEnabled": False,
    }
    write(evidence_path, evidence)
    evidence_ref = bind(evidence_path)
    model = {
        "schemaVersion": 1,
        "moduleId": "rank9nullificationwave-reviewed-357",
        "status": "ONE_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
        "scope": "Authored-review index envelope only; no native operational promotion.",
        "acceptedIds": [ID], "excludedPendingIds": sorted(live0 - {ID}),
        "sharedRequirements": {"runtimeSelectionEnabled": False, "catalogSourceStatusChanged": False},
        "spells": [{
            "id": ID, "name": source_card["name"],
            "position": int(entry0["wholeCardPointer"].rsplit("/", 1)[1]),
            "procedure": {
                "id": procedure_record["id"], "spellId": ID, "status": procedure_record["status"],
                "accepted": True, "applied": True,
                "procedureContent": json.dumps(local_procedure, ensure_ascii=False, sort_keys=True),
                "procedureRecordFile": "PROCEDURE_RECORD.json", "sourceCardFile": "SOURCE_CARD.json",
                "caseCoverageFile": "CASE_COVERAGE.json", "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
                "directorDecisionId": decision["id"], "closedBlockerIds": [BLOCKER],
                "closedResidualIds": RESIDUALS, "runtimeSelectionEnabled": False,
            },
            "directorProcedureRecord": procedure_record,
            "nativeCardUnchanged": True, "retainedQualificationIds": retained_qualifications,
            "runtimeSelectionEnabled": False,
        }],
        "sourceProcedure": source_proc_ref, "nativeCatalogGitBlob": git_catalog_ref,
        "directorDecision": decision_ref, "acceptance": acceptance_ref,
        "caseCoverage": coverage_ref, "evidenceBindings": evidence_ref,
        "runtimeSelectionEnabled": False, "runtimeExecuted": False,
        "implementationApproved": False, "humanPlaytested": False,
        "balanceApproved": False, "cosmologyModified": False,
        "completionApproved": False, "releaseApproved": False,
    }
    model_path = PKG / "MODEL.json"
    write(model_path, model)

    manuscript = (
        "# Nullification Wave — accepted static authored review 357\n\n"
        "GPT sealed-accepted Nullification Wave / WC188-B01 after Closure355 Repack01 closed NW355-R1 through NW355-R4. "
        "The independently checked packet binds the exact 19-event Forge source replay, 12 forward and inverse Wave events, "
        "and all 18 preserved historical Wave cases.\n\n"
        "This artifact indexes the accepted conditional witness as static authored-review evidence. It leaves the source procedure, "
        "native catalog card, source status, operational fields, and runtime selection unchanged. All encounter premises remain "
        "TEST_ONLY; no campaign event, runtime execution, or downstream approval is claimed.\n"
    )
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")

    package_files = [procedure_path, source_card_path, coverage_path, evidence_path, model_path]
    package_rows = [bind(path) for path in sorted(package_files, key=lambda p: p.name)]
    package_manifest = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-CANDIDATE-PACKAGE-MANIFEST-357",
        "selfExcluded": True, "memberCountExcludingSelf": len(package_rows), "members": package_rows,
    }
    manifest_path = PKG / "CANDIDATE_PACKAGE_MANIFEST.json"
    write(manifest_path, package_manifest)
    package_manifest_ref = bind(manifest_path)
    model_ref = bind(model_path)

    receipt = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-DIRECTOR-RETURN-RECEIPT",
        "recordedAtUtc": stamp,
        "status": "SEALED_ACCEPT_WC188_B01_APPLICATION_AUTHORIZED_ONLY",
        "acceptedIds": [ID], "appliedIds": [], "heldIds": [],
        "closedBlockerIds": [BLOCKER], "closedResidualIds": RESIDUALS,
        "applicationAuthorizedIds": [ID], "directorDecision": decision_ref,
        "acceptedArchive": archive_ref, "deliveryManifest": delivery_ref, "independentReview": audit_ref,
        "sourceResponseSummary": decision["exactDirectorResponse"],
        "applicationPerformedByDirector": False,
    }
    write(RECEIPT, receipt)
    receipt_ref = bind(RECEIPT)
    application = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-AUTHORED-APPLICATION",
        "recordedAtUtc": stamp,
        "status": "APPLIED_ONE_STATIC_AUTHORED_PROCEDURE_AUTHORED_INDEX_ONLY_RUNTIME_DISABLED",
        "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [],
        "closedBlockerIds": [BLOCKER], "closedResidualIds": RESIDUALS,
        "applicationAuthorizedIds": [ID], "directorDecision": decision_ref,
        "acceptance": acceptance_ref, "directorReturnReceipt": receipt_ref,
        "archive": archive_ref, "deliveryManifest": delivery_ref, "independentReview": audit_ref,
        "candidatePackage": model_ref, "candidatePackageManifest": package_manifest_ref,
        "caseCoverage": coverage_ref, "evidenceBindings": evidence_ref,
        "applicationScope": "One authored_review_index.json entry and one standalone static authored-review envelope only.",
        "indexPath": INDEX.relative_to(ROOT).as_posix(), "indexBindingBefore": bind(INDEX, index_raw),
        "catalogWorkingCopyBinding": catalog_ref, "catalogCommittedBlobBinding": git_catalog_ref,
        "catalogCRLFToLFGitBlobReconciled": True,
        "authorityBefore": AUTHORITY_BEFORE, "authorityAfterExpected": AUTHORITY_AFTER,
        "sourceProcedureChanged": False, "nativeCatalogChanged": False,
        "runtimeSelectionEnabled": False, "runtimeExecuted": False,
        "otherPendingIdentitiesChanged": False, "unrelatedDispositionsChanged": False,
    }
    write(APPLICATION, application)
    application_ref = bind(APPLICATION)

    backup_raw = index_raw
    BACKUP.write_bytes(backup_raw)
    index1 = copy.deepcopy(index0)
    entry1 = next(row for row in index1["entries"] if row["id"] == ID)
    entry1.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank9nullificationwave_reviewed_357/MODEL.json",
        "procedurePointer": "/spells/0/procedure",
        "wholeCardPointer": "/spells/0",
        "sourceStatus": entry0["sourceStatus"],
        "priorCatalogSelectionStatusUnchanged": True,
        "wholeCardIdField": "id",
        "sourceCatalogWholeCardPointer": entry0["wholeCardPointer"],
        "procedureTextPointer": "/spells/0/procedure/procedureContent",
        "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
        "sharedRulesPointer": "/sharedRequirements",
        "spellLocalRequirementsPointer": "/spells/0/procedure",
        "manuscript": "../../../docs/spells/candidates/NULLIFICATION_WAVE_REVIEWED_357.md",
        "reviewId": "NULLIFICATION_WAVE_CLOSURE355_REPACK01_APPLICATION.json",
        "runtimeSelectionEnabled": False,
        "historicalCandidateLabelsPreserved": True,
        "completeEvidenceRoot": PKG_REL.as_posix(),
        "completeEnvelopeBinding": model_ref,
        "caseEvidenceBindings": coverage_ref,
        "sourceArchiveBinding": archive_ref,
        "deliveryManifestBinding": delivery_ref,
        "independentReviewBinding": audit_ref,
        "candidatePackageManifestBinding": package_manifest_ref,
        "procedureSourceBinding": source_proc_ref,
        "authoredAcceptanceReceipt": acceptance_ref,
        "authoredApplicationReceipt": application_ref,
        "directorReturnReceipt": receipt_ref,
        "accepted": True, "applied": True,
        "closedBlockerIds": [BLOCKER], "closedResidualIds": RESIDUALS,
        "retainedQualificationIds": retained_qualifications,
        "retainedQualifications": [
            "All 18 historical Wave cases and retained qualification identifiers remain unchanged.",
            "The Return281 source procedure and native catalog card/source status remain byte-exact and unchanged.",
            "All new encounter premises remain TEST_ONLY; no campaign occurrence or runtime execution is claimed.",
            "Runtime selection, implementation, human play, balance, cosmology, completion, and release remain disabled.",
        ],
        "applicationScope": "Authored-review index application only; no native spell procedure or catalog promotion.",
    })
    index1["additionalStandaloneEnvelopes"].append({
        "file": "../spell_candidates/rank9nullificationwave_reviewed_357/MODEL.json",
        "binding": model_ref,
        "reviewId": "NULLIFICATION_WAVE_CLOSURE355_REPACK01_APPLICATION.json",
        "acceptedIds": [ID], "unacceptedIds": [],
        "excludedPendingIds": sorted(live0 - {ID}),
        "authority": acceptance_ref, "applicationReceipt": application_ref,
        "directorDecision": decision_ref, "sourceArchive": archive_ref,
        "deliveryManifest": delivery_ref, "caseCoverageBinding": coverage_ref,
        "candidatePackageManifestBinding": package_manifest_ref,
        "sourceProcedureBinding": source_proc_ref,
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_WC188_B01_RUNTIME_DISABLED",
        "runtimeSelectionEnabled": False,
    })
    index1["authoredCounts"] = {"reviewed": 827, "pending": 21}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"] = 551
    pending_ids1 = [spell_id for spell_id in pending_ids0 if spell_id != ID]
    assert len(pending_ids1) == 21 and set(pending_ids1) == live0 - {ID}
    assert index1["authoredCounts"] == {"reviewed": 827, "pending": 21}
    INDEX.write_bytes(encode(index1))
    index1_ref = bind(INDEX)

    priority = [spell_id for spell_id in queue0["continuingPriorityOrder"] if spell_id != ID]
    assert priority[0] == NEXT_ID and set(priority) == set(pending_ids1)
    pending_ids_json = pending_ids1
    queue1 = copy.deepcopy(queue0)
    queue1.update({
        "id": "CURRENT-SPELL-QUEUE-357", "recordedAtUtc": stamp,
        "supersedesQueue": QUEUE0.relative_to(ROOT).as_posix(),
        "currentAuthority": AUTHORITY_AFTER, "authority": AUTHORITY_AFTER,
        "pendingCount": 21, "acceptedUnapplied": 0,
        "currentIndexBinding": index1_ref,
        "continuingPriorityOrder": priority,
        "remainingPendingIds": pending_ids_json,
        "nextGroup": "rank9-ward-control6", "nextPendingIds": [NEXT_ID], "nextPendingCount": 1,
        "next": "summon-herald-of-the-planes / SH202-B02 — W01 Director reconciliation first; W02 state remains conditional on approved W01.",
        "activeReview": {"scopeIds": [NEXT_ID], "blockerIds": [NEXT_BLOCKER],
                         "status": "NEXT PRIORITY; W01 CONTENT AUTHORITY RECONCILIATION REQUIRED"},
        "lastDirectorReturn": decision["id"],
        "currentReturnAcceptedIds": [ID], "currentReturnAppliedIds": [ID],
        "currentReturnHeldIds": [], "currentReturnBlockers": [],
        "currentReturnDecision": decision_ref,
        "currentReturnArchive": archive_ref, "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref, "currentReturnReceipt": receipt_ref,
        "currentPacketStatus": "SEALED_ACCEPT_AND_AUTHORIZED_AUTHORED_INDEX_APPLICATION_COMPLETED_FOR_NULLIFICATION_WAVE_ONLY",
        "currentPacket": {"path": archive_ref["path"], "status": "SEALED_ACCEPTED_AND_APPLIED"},
        "currentPreparation": {"scopeIds": [ID], "blockerIds": [BLOCKER], "path": archive_ref["path"],
                               "status": "ACCEPTED_AND_APPLIED"},
        "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [],
        "acceptedThisStep": [ID], "appliedThisStep": [ID], "applicationPerformed": True,
        "closedBlockerIdsThisStep": [BLOCKER], "closedResidualIdsThisStep": RESIDUALS,
        "nextIdentity": NEXT_ID, "nextBlockerIds": [NEXT_BLOCKER],
        "nextActionablePriority": {"identity": NEXT_ID, "blockerIds": [NEXT_BLOCKER]},
        "currentDirectorRulingSupplement": decision_ref["path"],
        "currentDirectorReturn": decision_ref,
        "currentDirectorSourceCheck": decision_ref,
        "currentApplication": {"path": APPLICATION.relative_to(ROOT).as_posix(), **bind(APPLICATION)},
        "applicationPerformed": True, "canonicalFilesChanged": False,
        "runtimeExecuted": False, "githubChanges": False,
        "currentPendingIdentityAudit": PENDING1.relative_to(ROOT).as_posix(),
        "pendingIdentityAudit": PENDING1.relative_to(ROOT).as_posix(),
        "currentHandoff": HANDOFF1.relative_to(ROOT).as_posix(),
        "currentPendingIdentityAuditPath": PENDING1.relative_to(ROOT).as_posix(),
        "currentHandoffPath": HANDOFF1.relative_to(ROOT).as_posix(),
        "separatelyRetainedHolds": [x for x in queue0.get("separatelyRetainedHolds", []) if x != ID],
    })
    queue1["fateRewriteSubmissionStatus"] = "NO_CURRENT_SUBMISSION"
    queue1["currentApplicationValidation"] = VALIDATION.relative_to(ROOT).as_posix()
    write(QUEUE1, queue1)
    queue1_ref = bind(QUEUE1)

    pending1 = copy.deepcopy(pending0)
    pending1["closedBlockerIdsThisStepHistorical"] = copy.deepcopy(pending1.get("closedBlockerIdsThisStep", []))
    pending1.update({
        "id": "CURRENT21-PENDING-IDENTITY-AUDIT-357", "recordedAtUtc": stamp,
        "supersedes": {"path": PENDING0.relative_to(ROOT).as_posix(), **pending0_ref},
        "status": "PASS_CURRENT_827_21_NULLIFICATION_WAVE_APPLIED_NEXT_HERALD_W01",
        "authority": AUTHORITY_AFTER, "pendingCount": 21, "pendingIds": pending_ids1,
        "acceptedIds": [ID], "appliedIds": [ID],
        "indexBinding": index1_ref,
        "currentQueueBinding": queue1_ref,
        "currentHandoff": HANDOFF1.relative_to(ROOT).as_posix(),
        "closureTasksRemaining": 21, "firstReviewTasksRemaining": 0,
        "nextGroup": "rank9-ward-control6", "nextPendingIds": [NEXT_ID], "nextPendingCount": 1,
        "nextIdentity": NEXT_ID, "nextBlockerIds": [NEXT_BLOCKER],
        "nextStep": "Prepare the Summon Herald of the Planes / SH202-B02 W01 Director-integration content reconciliation. W02 remains conditional on W01 approval; do not create the W02 fixture before that approval.",
        "currentBlocker": NEXT_BLOCKER,
        "continuingPriorityOrder": priority, "remainingPendingIds": pending_ids1,
        "heldThisStep": [], "acceptedThisStep": [ID], "appliedThisStep": True,
        "applicationPerformed": True, "canonicalFilesChanged": False,
        "currentReturnAcceptedIds": [ID], "currentReturnAppliedIds": [ID],
        "currentReturnHeldIds": [], "currentReturnBlockers": [],
        "currentReturnDecision": decision_ref,
        "currentReturnArchive": archive_ref, "currentReturnDelivery": delivery_ref,
        "currentReturnAudit": audit_ref, "currentReturnReceipt": receipt_ref,
        "currentPacketStatus": "SEALED_ACCEPTED_AND_AUTHORIZED_APPLICATION_COMPLETED_FOR_NULLIFICATION_WAVE_ONLY",
        "currentPacket": archive_ref["path"],
        "closedBlockerIdsThisStep": [BLOCKER], "closedResidualIdsThisStep": RESIDUALS,
        "lastDirectorReturnHistorical": copy.deepcopy(pending0.get("lastDirectorReturn")),
        "lastDirectorReturn": {"decisionId": decision["id"], "acceptedIds": [ID], "appliedIds": [ID],
                               "heldIds": [], "blockerIds": [], "closedBlockerIds": [BLOCKER],
                               "closedResidualIds": RESIDUALS, "applicationAuthorized": True},
    })
    write(PENDING1, pending1)
    pending1_ref = bind(PENDING1)

    handoff1 = copy.deepcopy(handoff0)
    prior_closed = list(handoff1.get("closedBlockerIds", []))
    if BLOCKER not in prior_closed:
        prior_closed.append(BLOCKER)
    handoff1.update({
        "id": "CURRENT-HANDOFF-357", "recordedAtUtc": stamp,
        "supersedes": handoff0.get("id"),
        "status": "CURRENT DIRECTOR HANDOFF; NULLIFICATION WAVE ACCEPTED/APPLIED; 21 CLOSURE TASKS REMAIN",
        "authority": AUTHORITY_AFTER, "scopeIds": pending_ids1, "pendingIds": pending_ids1,
        "continuingPriorityOrder": priority, "remainingPendingIds": pending_ids1,
        "blockerIds": [NEXT_BLOCKER], "currentBlocker": {"identity": NEXT_ID, "group": "rank9-ward-control6", "blockerIds": [NEXT_BLOCKER]},
        "nextPendingGroup": "rank9-ward-control6", "nextIdentity": NEXT_ID, "nextBlockerIds": [NEXT_BLOCKER],
        "nextStep": "Prepare Herald W01 reconciliation under Director integration authority. W02 synthetic state remains conditional on W01 approval.",
        "currentPacketStatus": "Nullification Wave / WC188-B01 accepted and authored-index application completed; next task is Herald W01.",
        "currentPreparation": None,
        "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [],
        "currentReturnAcceptedIds": [ID], "currentReturnAppliedIds": [ID], "currentReturnHeldIds": [],
        "currentReturnBlockers": [], "currentReturnDecision": decision_ref,
        "currentPacket": archive_ref["path"], "currentDirectorSourceCheck": decision_ref,
        "closedBlockerIds": prior_closed, "closedBlockerIdsThisStep": [BLOCKER],
        "closedResidualIdsThisStep": RESIDUALS, "closureTasksRemaining": 21, "firstReviewTasksRemaining": 0,
        "canonicalFilesChanged": False, "applicationPerformed": True, "runtimeExecuted": False,
        "queueBinding": queue1_ref, "pendingIdentityAuditBinding": pending1_ref,
        "currentPendingIdentityAudit": PENDING1.relative_to(ROOT).as_posix(),
        "pendingIdentityAudit": PENDING1.relative_to(ROOT).as_posix(),
        "currentDirectorReturn": decision_ref,
    })
    write(HANDOFF1, handoff1)
    handoff1_ref = bind(HANDOFF1)

    # Record exact index operations; the full backup permits a byte-exact inverse.
    operations = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-INDEX-OPERATIONS-357",
        "recordedAtUtc": stamp, "targetIndex": INDEX.relative_to(ROOT).as_posix(),
        "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER],
        "closedResidualIds": RESIDUALS,
        "beforeBinding": bind(INDEX, index_raw), "afterBinding": index1_ref,
        "backup": bind(BACKUP, backup_raw),
        "operations": [
            {"op": "replace-authored-entry", "id": ID, "before": entry0, "after": copy.deepcopy(entry1)},
            {"op": "append-standalone-authored-envelope", "acceptedIds": [ID], "model": model_ref},
            {"op": "update-authored-counts", "before": {"reviewed": 826, "pending": 22}, "after": {"reviewed": 827, "pending": 21}},
            {"op": "increment-complete-standalone-procedure-count", "before": 550, "after": 551},
        ],
        "inverse": [
            {"op": "restore-entry", "id": ID, "value": entry0},
            {"op": "remove-appended-envelope", "acceptedIds": [ID]},
            {"op": "restore-authored-counts", "value": {"reviewed": 826, "pending": 22}},
            {"op": "restore-procedure-count", "value": 550},
            {"op": "restore-byte-exact-index-from-backup", "backup": bind(BACKUP, backup_raw)},
        ],
        "catalogByteExact": CATALOG.read_bytes() == catalog_raw,
        "sourceProcedureChanged": False,
        "nativeCardUnchanged": True,
        "inverseRestoresExactIndex": BACKUP.read_bytes() == index_raw,
    }
    write(OPERATIONS, operations)
    operations_ref = bind(OPERATIONS)

    checks = [
        ("sealed Director accepts and authorizes only Nullification Wave", decision["acceptedIds"] == [ID] and decision["applicationAuthorized"] is True and decision["remainingDefectPaths"] == []),
        ("accepted Repack01 archive and 19-check audit pass", archive_ref["sha256"] == delivery["archive"]["sha256"] and audit["status"] == "PASS" and audit["checkCount"] == 19),
        ("single index entry applied; source card and catalog remain byte-exact", entry1["authoredStatus"] == "reviewed-authored-operational-playtest" and CATALOG.read_bytes() == catalog_raw and card0 == next(row for row in read(CATALOG)["spells"] if row["id"] == ID) and catalog_raw.replace(bytes([13, 10]), bytes([10])) == git_catalog_raw),
        ("current authority advances exactly to 827/21/0 and 551/173", index1["authoredCounts"] == {"reviewed": 827, "pending": 21} and index1["representationCounts"]["completeReviewedStandaloneProcedures"] == 551),
        ("pending index identities equal prior identities minus target", pending_ids1 == [spell_id for spell_id in pending_ids0 if spell_id != ID] and set(pending_ids1) == live0 - {ID}),
        ("other 21 entry dispositions remain semantically unchanged", all(next(row for row in index1["entries"] if row["id"] == spell_id) == next(row for row in index0["entries"] if row["id"] == spell_id) for spell_id in pending_ids1)),
        ("queue/pending/handoff cross-bind updated index and each other", queue1["currentIndexBinding"]["sha256"] == pending1["indexBinding"]["sha256"] == index1_ref["sha256"] and pending1["currentQueueBinding"]["sha256"] == queue1_ref["sha256"] and handoff1["queueBinding"]["sha256"] == queue1_ref["sha256"] and handoff1["pendingIdentityAuditBinding"]["sha256"] == pending1_ref["sha256"]),
        ("next review remains Herald W01; Lumen W02 stays conditional", queue1["nextIdentity"] == NEXT_ID and queue1["nextBlockerIds"] == [NEXT_BLOCKER] and "conditional on W01 approval" in pending1["nextStep"]),
        ("static authored package keeps runtime and downstream gates disabled", model["runtimeSelectionEnabled"] is False and procedure_record["runtimeSelectionEnabled"] is False and application["runtimeSelectionEnabled"] is False and application["runtimeExecuted"] is False),
        ("index inverse backup restores byte-exact pre-application file", BACKUP.read_bytes() == index_raw and operations["inverseRestoresExactIndex"] is True),
    ]
    failures = [label for label, passed in checks if not passed]
    assert not failures, failures
    validation = {
        "id": "NULLIFICATION-WAVE-CLOSURE355-REPACK01-APPLICATION-VALIDATION-357",
        "recordedAtUtc": stamp, "status": "PASS",
        "checks": [{"check": label, "passed": bool(passed)} for label, passed in checks],
        "checkCount": len(checks), "passedChecks": len(checks), "failedChecks": 0,
        "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER], "closedResidualIds": RESIDUALS,
        "authority": AUTHORITY_AFTER,
        "index": index1_ref, "application": application_ref,
        "decision": decision_ref, "acceptance": acceptance_ref, "receipt": receipt_ref,
        "archive": archive_ref, "audit": audit_ref, "queue": queue1_ref,
        "pendingIdentityAudit": pending1_ref, "handoff": handoff1_ref,
        "indexOperations": operations_ref,
        "nativeCatalogChanged": False, "sourceProcedureChanged": False,
        "runtimeSelectionEnabled": False, "nextIdentity": NEXT_ID,
    }
    write(VALIDATION, validation)

    validation_ref = bind(VALIDATION)
    # The bounded snapshots point at final binding values; validation names the applied identity and counts.
    SNAPSHOT.write_text(
        "# Spell review snapshot — Nullification Wave Closure355 Repack01 application\n\n"
        "**827 applied / 21 pending / 0 accepted-unapplied; 551 complete standalone procedures / 173 scoped interfaces; 0 first reviews / 21 closure tasks.**\n\n"
        "GPT sealed-accepted and authorized Nullification Wave / WC188-B01 only. NW355-R1–R4 are closed. The source procedure and native catalog remain unchanged; runtime selection remains disabled.\n\n"
        "The next directed priority is Summon Herald of the Planes / SH202-B02. Prepare the W01 content reconciliation first. The user's W02 test-state authorization remains conditional on W01 approval.\n\n"
        f"Application validation: {validation_ref['path']} (SHA-256 {validation_ref['sha256']}).\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"status": "PASS", "acceptedApplied": ID, "closedBlockerIds": [BLOCKER],
                      "closedResidualIds": RESIDUALS, "authority": AUTHORITY_AFTER,
                      "index": bind(INDEX), "application": bind(APPLICATION),
                      "validation": bind(VALIDATION), "queue": bind(QUEUE1),
                      "pendingAudit": bind(PENDING1), "handoff": bind(HANDOFF1),
                      "next": NEXT_ID}, indent=2))


if __name__ == "__main__":
    main()
