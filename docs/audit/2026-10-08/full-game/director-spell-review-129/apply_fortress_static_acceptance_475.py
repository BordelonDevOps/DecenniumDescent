#!/usr/bin/env python3
"""Apply GPT Director's exact Fortress static-authored-review decision to the index only."""
import copy
import datetime as dt
import hashlib
import json
import subprocess
import zlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
APP = BASE / "fortress_static_acceptance_475"
CAND_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9fortress_static_reviewed_475")
CAND = ROOT / CAND_REL
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PROCEDURE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/procedures/conjure-demiplane-fortress.json"
HOLD_REGISTER = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/HOLD_REGISTER.json"
QUEUE0 = BASE / "CURRENT_SPELL_QUEUE_465_REPACK01.json"
HANDOFF0 = BASE / "CURRENT_HANDOFF_465_REPACK09.json"
COVERAGE = BASE / "fortress_w01_w13_coverage_readback_473/FORTRESS_W01_W13_COVERAGE_RECONCILIATION_473.json"
COVERAGE_MD = BASE / "fortress_w01_w13_coverage_readback_473/FORTRESS_W01_W13_COVERAGE_RECONCILIATION_473.md"
IDENTITY = BASE / "fortress_identity_level_reconciliation_474/FORTRESS_IDENTITY_LEVEL_RECONCILIATION_474.json"
HISTORIC = BASE / "fortress_w01_w13_coverage_readback_429/FORTRESS_W01_W13_COVERAGE_READBACK_429_BINDING_RECONCILED.json"
W13 = BASE / "fortress_w13_nested_space_witness_471"
W13_PROPOSAL = BASE / "fortress_w13_nested_space_owner_proposal_448"
ID = "conjure-demiplane-fortress"
BLOCKER = "PG200-B06"
QUALS = [f"PG200-H{i:02d}" for i in range(1, 11)]
EXPECTED = {
    "coverage": "d110203b65fb697e8a0574c8a4bccae9b0654423b8662044632c7174526c2306",
    "identity": "be12a0c116737b6624eff2ed0484c3cfdefac7a846d524a10f05a5b876164e13",
    "procedure": "bf8b80fcb3f819ad549b94bef7ef9227cd8a190962a70392dbaa0fb6237b4145",
    "queue": "b6ef81469804a4e196bdbc61a927cb5b53c51c738005082ba41293a6e54f9133",
    "index": "cfd06d3eb2a163a2ae6a92db9cc67171a031393ee789bf308f6a7a5b9a7767cb",
    "catalog": "f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8",
    "holdRegister": "65f4419f329e83c82272a848f324d945d7e5244896f911318e73c2f857ef39c7",
}

DIRECTOR_TEXT = """ACCEPT — conjure-demiplane-fortress for static authored-procedure review only. PG200-B06 is closed within that scope.

Reconciliation 473 correctly establishes 13 covered obligations: nine component-sufficient unsealed records, four preserved TEST_ONLY seals, zero open integrations. The retained procedure matches Return328’s procedure and shared contract. No further component construction or replay is required.

Decision payload: {\"decision\":\"ACCEPT\",\"spellId\":\"conjure-demiplane-fortress\",\"scope\":\"STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY\",\"acceptedIds\":[\"conjure-demiplane-fortress\"],\"appliedIds\":[],\"heldIdsInReviewedScope\":[],\"closedBlockerIds\":[\"PG200-B06\"],\"retainedQualificationIds\":[\"PG200-H01\",\"PG200-H02\",\"PG200-H03\",\"PG200-H04\",\"PG200-H05\",\"PG200-H06\",\"PG200-H07\",\"PG200-H08\",\"PG200-H09\",\"PG200-H10\"],\"applicationAuthorized\":true,\"applicationScope\":\"FORTRESS_AUTHORED_REVIEW_INDEX_ONLY\",\"authorityAfterDecision\":{\"applied\":830,\"stillHeldPending\":17,\"acceptedUnapplied\":1}}.

This decision binds Coverage473 JSON SHA-256 d110203b65fb697e8a0574c8a4bccae9b0654423b8662044632c7174526c2306; Identity reconciliation474 SHA-256 be12a0c116737b6624eff2ed0484c3cfdefac7a846d524a10f05a5b876164e13; and the retained Fortress procedure SHA-256 bf8b80fcb3f819ad549b94bef7ef9227cd8a190962a70392dbaa0fb6237b4145.

Preserve all 14 historical records, exact adopted component scopes, and W11’s limitation: its PASS does not certify an invertible state-patch chain. Existing component seals remain unchanged; unsealed components are not retroactively sealed. Unsupported nested-source relationships and unadopted physical premises receive no general permission.

The existing operational=null and historical unresolved labels do not prevent this static acceptance. They remain preserved source/runtime boundaries.

The separate application step is to record and independently verify this exact acceptance and its evidence bindings, then apply only Fortress’s authored-review index disposition, record the PG200-B06 closure, and refresh the application receipt, pending audit, queue and handoff. Preserve the native catalog bytes, historical evidence, H01–H10 and every unrelated identity.

After verified application: 831 applied / 17 pending / 0 accepted-unapplied; 555 standalone procedures / 173 interfaces. No application occurred in this response.

Next priority: Elemental Shell — DF218-B01/B02. Runtime, implementation, human-play, balance, cosmology, domain/completion and release gates remain closed."""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def crc(b):
    return f"{zlib.crc32(b) & 0xffffffff:08x}"


def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def enc(x):
    return (json.dumps(x, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def bind(p, raw=None):
    raw = p.read_bytes() if raw is None else raw
    return {"path": p.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha(raw), "crc32": crc(raw)}


def write(p, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = enc(x)
    p.write_bytes(raw)
    return bind(p, raw)


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def git_blob(path, commit):
    return subprocess.check_output(["git", "show", f"{commit}:{path.as_posix()}"], cwd=ROOT)


def main():
    readback = APP / "DIRECTOR_READBACK_474.json"
    acceptance = APP / "DIRECTOR_ACCEPTANCE_475.json"
    model_path = CAND / "MODEL.json"
    case_path = CAND / "CASE_COVERAGE.json"
    manifest_path = CAND / "CANDIDATE_PACKAGE_MANIFEST.json"
    application_path = APP / "APPLICATION_475.json"
    queue_path = BASE / "CURRENT_SPELL_QUEUE_475.json"
    pending_path = BASE / "CURRENT17_PENDING_IDENTITY_AUDIT_475.json"
    handoff_path = BASE / "CURRENT_HANDOFF_475.json"
    validation_path = APP / "VALIDATION_475.json"
    ops_path = APP / "INDEX_OPERATIONS_475.json"
    snapshot_path = BASE / "CURRENT_SPELL_REVIEW_SNAPSHOT_475.md"
    outputs = [readback, acceptance, model_path, case_path, manifest_path, application_path,
               queue_path, pending_path, handoff_path, validation_path, ops_path, snapshot_path]
    assert not any(p.exists() for p in outputs), "Refusing to overwrite existing application outputs."
    assert not (APP / "authored_review_index.before_fortress_475.json").exists()
    assert not (CAND / ".gitattributes").exists() and not (APP / ".gitattributes").exists()

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    q0, h0, idx0 = read(QUEUE0), read(HANDOFF0), read(INDEX)
    idxraw, catraw, procr = INDEX.read_bytes(), CATALOG.read_bytes(), PROCEDURE.read_bytes()
    holdraw = HOLD_REGISTER.read_bytes()
    source = json.loads(procr)
    cov, identity = read(COVERAGE), read(IDENTITY)
    assert sha(COVERAGE.read_bytes()) == EXPECTED["coverage"]
    assert sha(IDENTITY.read_bytes()) == EXPECTED["identity"]
    assert sha(procr) == EXPECTED["procedure"]
    assert sha(QUEUE0.read_bytes()) == EXPECTED["queue"]
    assert sha(idxraw) == EXPECTED["index"]
    assert sha(holdraw) == EXPECTED["holdRegister"]
    assert q0["currentAuthority"] == h0["authority"] == {
        "reviewedApplied": 830, "pending": 18, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 554, "scopedInterfaces": 173}
    assert q0["currentIndexBinding"]["sha256"] == EXPECTED["index"]
    assert q0["currentCatalogBinding"]["sha256"] == EXPECTED["catalog"]
    assert bind(INDEX, idxraw)["bytes"] == q0["currentIndexBinding"]["bytes"]
    committed_catalog = git_blob(Path("DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"), head)
    assert sha(committed_catalog) == EXPECTED["catalog"]
    assert json.loads(catraw) == json.loads(committed_catalog)
    assert sha(committed_catalog) == q0["currentCatalogBinding"]["sha256"]
    assert idx0["authoredCounts"] == {"reviewed": 830, "pending": 18}
    assert idx0["representationCounts"]["completeReviewedStandaloneProcedures"] == 554
    assert cov["counts"] == {"componentSufficientUnsealed": 9, "sealedTestOnlyComponents": 4,
                              "openIntegrations": 0, "rows": 13,
                              "unchangedPriorSourcePathsVerified": 29, "changedPriorSourcePaths": 0}
    assert {r["id"] for r in cov["rows"]} == {f"PG328-W{i:02d}" for i in range(1, 14)}
    assert "invertible state-patch chain" in json.dumps(next(r["evidence"] for r in cov["rows"] if r["id"] == "PG328-W11"))
    assert identity["coverageReconciliation"]["sha256"] == EXPECTED["coverage"]
    assert identity["retainedProcedure"]["gitBlobSha256"] == EXPECTED["procedure"]
    assert identity["identityQualifications"]["currentHoldRegister"]["gitBlobSha256"] == EXPECTED["holdRegister"]
    assert identity["identityQualifications"]["currentCatalogEntry"]["gitBlobSha256"] == EXPECTED["catalog"]
    assert source["id"] == ID and source["status"] == "UNRESOLVED_PROPOSED_PROCEDURE_REQUIRED_WITNESSES_BLOCKED"
    assert source["nativeCardUnchanged"]["operational"] is None and source["nativeCardUnchanged"]["status"] == "blocked-pending-operational-review"
    assert source["accepted"] is False and source["applied"] is False
    assert set(source["holdIds"]) == set([BLOCKER] + QUALS)
    assert identity["identityQualifications"]["currentHoldRegister"]["PG200-B06"]["status"] == "OPEN"
    assert identity["identityQualifications"]["currentHoldRegister"]["PG200-B06"]["blocking"] is True
    assert identity["identityQualifications"]["currentHoldRegister"]["retainedNonblockingQualifications"]
    row0 = copy.deepcopy(next(e for e in idx0["entries"] if e["id"] == ID))
    pending0 = [e["id"] for e in idx0["entries"] if e["authoredStatus"] == "pending-authored-procedure"]
    assert len(pending0) == 18 and ID in pending0
    assert row0["sourceStatus"] == "blocked-pending-operational-review"
    assert row0["wholeCardPointer"] == "/spells/198"
    assert q0["remainingPendingIds"] == pending0
    catalog = read(CATALOG)
    native = next(e for e in catalog["spells"] if e["id"] == ID)
    assert catalog["spells"].index(native) == 198 and native["operational"] is None
    assert native["status"] == "blocked-pending-operational-review"

    acceptance_obj = {
        "schemaVersion": 1,
        "id": "CONJURE-DEMIPLANE-FORTRESS-STATIC-AUTHORED-ACCEPTANCE-475",
        "classification": "GPT_DIRECTOR_STATIC_AUTHORED_PROCEDURE_ACCEPTANCE_NOT_APPLICATION",
        "status": "ACCEPTED_UNAPPLIED",
        "issuer": "GPT Director",
        "observedAtUtc": stamp(),
        "sourceSnapshotCommit": head,
        "scopeIds": [ID],
        "decision": "ACCEPT",
        "accepted": True,
        "applied": False,
        "acceptedIds": [ID],
        "appliedIds": [],
        "heldIdsInReviewedScope": [],
        "closedBlockerIds": [BLOCKER],
        "retainedQualificationIds": QUALS,
        "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "applicationAuthorized": True,
        "applicationScope": "FORTRESS_AUTHORED_REVIEW_INDEX_ONLY",
        "authorityAfterDecision": {"applied": 830, "stillHeldPending": 17, "acceptedUnapplied": 1},
        "evidenceBindings": {},
        "limitations": {
            "sourceProcedureStatusPreserved": source["status"],
            "nativeOperationalValuePreserved": None,
            "nativeCatalogStatusPreserved": native["status"],
            "originalHoldRegisterB06RemainsHistoricalOpen": True,
            "B06ClosureScope": "Static authored-procedure review only; it does not clear operational or downstream gates.",
            "allHistoricalEvidencePreserved": True,
            "componentSealsPreserved": True,
            "W11InvertibleStatePatchChainCertified": False,
            "unsupportedNestedSourceRelationshipsGranted": False,
            "unadoptedPhysicalPremisesGranted": False,
            "runtimeImplementationHumanPlayBalanceCosmologyDomainAndReleaseApproved": False,
        },
    }
    rb_obj = {
        "schemaVersion": 1,
        "id": "FORTRESS-DIRECTOR-READBACK-474",
        "recordedAtUtc": stamp(),
        "source": {"service": "GPT Director", "conversationTitle": "Calibration review part 6",
                   "conversationUrl": "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"},
        "directorResponseText": DIRECTOR_TEXT,
        "structuredDecision": {
            "decision": "ACCEPT", "spellId": ID, "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
            "acceptedIds": [ID], "appliedIds": [], "heldIdsInReviewedScope": [],
            "closedBlockerIds": [BLOCKER], "retainedQualificationIds": QUALS,
            "applicationAuthorized": True, "applicationScope": "FORTRESS_AUTHORED_REVIEW_INDEX_ONLY",
            "authorityAfterDecision": {"applied": 830, "stillHeldPending": 17, "acceptedUnapplied": 1}},
        "boundEvidence": {"coverage473Sha256": EXPECTED["coverage"],
                          "identity474Sha256": EXPECTED["identity"],
                          "retainedProcedureSha256": EXPECTED["procedure"]},
        "applicationOccurredInDirectorResponse": False,
    }
    rbr = write(readback, rb_obj)
    acceptance_obj["readbackBinding"] = rbr
    acceptance_obj["evidenceBindings"] = {
        "coverageReconciliation473": bind(COVERAGE),
        "coverageMarkdown473": bind(COVERAGE_MD),
        "identityReconciliation474": bind(IDENTITY),
        "retainedProcedure": bind(PROCEDURE, procr),
        "historicalCoverageReadback429": bind(HISTORIC),
        "sourceHoldRegister": bind(HOLD_REGISTER, holdraw),
        "nativeCatalogCommittedGitBlob": {**bind(CATALOG, committed_catalog), "byteDomain": "exact committed Git blob"},
        "nativeCatalogWorkingRepresentationBeforeAfter": bind(CATALOG, catraw),
        "currentQueueBefore": bind(QUEUE0),
        "directorReadback": rbr,
    }
    accept_ref = write(acceptance, acceptance_obj)

    cov_obj = {
        "schemaVersion": 1, "id": "FORTRESS-STATIC-AUTHORED-COVERAGE-475", "spellId": ID,
        "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
        "coverageReconciliation": bind(COVERAGE), "identityDecision": accept_ref,
        "historicalCoverageMap": identity["historicalCoverage"]["initialCoverageMap"],
        "historicalByteReconciliation": bind(HISTORIC),
        "componentCounts": cov["counts"], "componentRows": copy.deepcopy(cov["rows"]),
        "historicalRecordCount": 14,
        "preservedLimits": ["W11 PASS does not certify an invertible state-patch chain.",
                            "Four preexisting TEST_ONLY seals remain unchanged.",
                            "Nine component-sufficient unsealed rows remain unsealed.",
                            "No unsupported nested-source relationship or unadopted physical premise is generally authorized."],
        "closure": {"blockerId": BLOCKER, "status": "CLOSED_FOR_STATIC_AUTHORED_REVIEW_ONLY",
                    "sourceHoldRegisterBytesChanged": False,
                    "originalSourceHoldRegisterStatus": "OPEN_BLOCKING_FOR_OTHER_SCOPES"},
        "effects": {"historyReplayed": False, "componentReconstructed": False, "campaignEventClaimed": False,
                    "runtimeExecuted": False, "nativeCatalogChanged": False},
    }
    case_ref = write(case_path, cov_obj)

    derived = copy.deepcopy(source)
    derived.update({
        "accepted": True, "applied": True,
        "status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
        "holdIds": QUALS, "qualificationHoldIds": QUALS,
        "closedBlockerIds": [BLOCKER], "resolvedBlockerIds": [BLOCKER],
        "sourceProcedureStatusPreserved": source["status"],
        "sourceOperationalValuePreserved": None,
        "reassessment": [{"blockerId": BLOCKER, "decision": "CLOSED_FOR_STATIC_AUTHORED_REVIEW_ONLY",
                          "directorReadback": rbr["path"],
                          "limitation": "The source hold register remains unchanged; operational and downstream scopes remain closed."}],
    })
    model = {
        "schemaVersion": 1,
        "id": "RANK9-CONJURE-DEMIPLANE-FORTRESS-STATIC-REVIEWED-475",
        "reviewId": acceptance_obj["id"],
        "status": "REVIEWED_AUTHORED_STATIC_PROCEDURE",
        "acceptedIds": [ID], "heldIds": [], "closedBlockerIds": [BLOCKER],
        "retainedQualificationIds": QUALS,
        "sourceProcedureBinding": bind(PROCEDURE, procr),
        "directorReadback": rbr,
        "directorAcceptance": accept_ref,
        "caseEvidence": case_ref,
        "spells": [{
            "id": ID, "name": native["name"], "nativeCard": copy.deepcopy(source["nativeCardUnchanged"]),
            "procedure": {"procedureContent": source["procedure"], "sharedContract": copy.deepcopy(source["sharedContract"])},
            "sourceProcedureRecord": copy.deepcopy(source), "directorProcedureRecord": derived,
            "sourceProcedureBinding": bind(PROCEDURE, procr), "qualificationIds": QUALS,
            "closedBlockerIds": [BLOCKER], "caseEvidence": case_ref,
        }],
        "sharedRequirements": copy.deepcopy(source["sharedContract"]),
        "runtimeSelectionEnabled": False, "implementationApproved": False,
        "humanPlayApproved": False, "balanceApproved": False, "cosmologyModified": False,
        "domainClosure": False, "releaseApproved": False,
        "nativeCatalogChanged": False, "historicalEvidenceChanged": False,
    }
    model_ref = write(model_path, model)
    manifest = {"id": "CONJURE-DEMIPLANE-FORTRESS-STATIC-REVIEWED-475-PACKAGE",
                "files": [model_ref, case_ref, bind(PROCEDURE, procr), accept_ref, rbr, bind(COVERAGE), bind(HISTORIC)],
                "scope": "Static authored-review index only; native catalog, source procedure and runtime unchanged."}
    manifest_ref = write(manifest_path, manifest)

    backup = APP / "authored_review_index.before_fortress_475.json"
    APP.mkdir(parents=True, exist_ok=True)
    CAND.mkdir(parents=True, exist_ok=True)
    (APP / ".gitattributes").write_text("** -text !eol\n", encoding="utf-8", newline="\n")
    (CAND / ".gitattributes").write_text("** -text !eol\n", encoding="utf-8", newline="\n")
    backup.write_bytes(idxraw)
    backup_ref = bind(backup, idxraw)

    authority_after = {"reviewedApplied": 831, "pending": 17, "acceptedUnapplied": 0,
                       "completeStandaloneProcedures": 555, "scopedInterfaces": 173}
    pending_after = [x for x in pending0 if x != ID]
    priority = [x for x in q0["continuingPriorityOrder"] if x != ID]
    assert set(pending_after) == set(priority) and len(pending_after) == 17
    assert priority[0] == "elemental-shell"

    app_obj = {
        "id": "CONJURE-DEMIPLANE-FORTRESS-STATIC-APPLICATION-475", "recordedAtUtc": stamp(),
        "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER],
        "directorAcceptance": accept_ref, "directorReadback": rbr,
        "candidateModel": model_ref, "caseCoverage": case_ref, "candidatePackageManifest": manifest_ref,
        "sourceProcedureBeforeAfter": bind(PROCEDURE, procr), "sourceHoldRegisterBeforeAfter": bind(HOLD_REGISTER, holdraw),
        "nativeCatalogWorkingRepresentationBeforeAfter": bind(CATALOG, catraw),
        "nativeCatalogCommittedGitBlobBeforeAfter": {**bind(CATALOG, committed_catalog), "byteDomain": "exact committed Git blob"},
        "indexBefore": bind(INDEX, idxraw), "indexBackup": backup_ref,
        "authorityBefore": q0["currentAuthority"], "authorityAfter": authority_after,
        "retainedQualificationIds": QUALS,
        "applicationScope": "FORTRESS_AUTHORED_REVIEW_INDEX_ONLY",
        "B06ClosureScope": "Static authored-procedure review only; original source hold register remains unchanged.",
        "nativeCatalogChanged": False, "sourceProcedureChanged": False, "sourceHoldRegisterChanged": False,
        "historicalEvidenceChanged": False, "runtimeSelectionEnabled": False, "runtimeExecuted": False,
        "implementationHumanPlayBalanceCosmologyDomainReleaseApproved": False,
        "unrelatedIdentityRowsChanged": False,
    }
    app_ref = write(application_path, app_obj)

    idx1 = copy.deepcopy(idx0)
    row = copy.deepcopy(row0)
    row.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank9fortress_static_reviewed_475/MODEL.json",
        "procedurePointer": "/spells/0/procedure", "wholeCardPointer": "/spells/0",
        "procedureTextPointer": "/spells/0/procedure/procedureContent", "wholeCardIdField": "id",
        "sourceCatalogWholeCardPointer": "/spells/198",
        "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
        "sharedRulesPointer": "/sharedRequirements", "spellLocalRequirementsPointer": "/spells/0/procedure",
        "runtimeSelectionEnabled": False, "completeEvidenceRoot": CAND_REL.as_posix(),
        "completeEnvelopeBinding": model_ref, "caseEvidenceBindings": case_ref,
        "candidatePackageManifestBinding": manifest_ref,
        "authoredAcceptanceReceipt": accept_ref, "authoredApplicationReceipt": app_ref,
        "sourceProcedureBinding": bind(PROCEDURE, procr), "historicalCoverageBinding": bind(HISTORIC),
        "coverageReconciliationBinding": bind(COVERAGE), "directorReadbackBinding": rbr,
        "reviewId": app_obj["id"], "accepted": True, "applied": True,
        "closedBlockerIds": [BLOCKER], "retainedQualificationIds": QUALS,
        "retainedQualifications": ["Static authored-procedure review only. Preserve the original unresolved procedure and blocked native card; runtime, implementation, human-play, balance, cosmology, domain and release gates stay closed."],
        "historicalCandidateLabelsPreserved": True,
        "applicationScope": "Fortress authored-review index only; no native catalog/source procedure or runtime promotion.",
    })
    ri = next(i for i, e in enumerate(idx1["entries"]) if e["id"] == ID)
    idx1["entries"][ri] = row
    idx1["authoredCounts"] = {"reviewed": 831, "pending": 17}
    idx1["representationCounts"]["completeReviewedStandaloneProcedures"] = 555
    idx1.setdefault("additionalStandaloneEnvelopes", []).append({
        "file": row["procedureFile"], "binding": model_ref, "reviewId": acceptance_obj["id"],
        "acceptedIds": [ID], "unacceptedIds": [], "excludedPendingIds": sorted(set(pending0) - {ID}),
        "authority": accept_ref, "applicationReceipt": app_ref, "caseEvidenceBinding": case_ref,
        "candidatePackageManifestBinding": manifest_ref, "sourceProcedureBinding": bind(PROCEDURE, procr),
        "historicalCoverageBinding": bind(HISTORIC), "runtimeSelectionEnabled": False,
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_PG200_B06_CLOSED_FOR_REVIEW_ONLY",
    })
    assert all(idx0["entries"][i] == idx1["entries"][i] for i in range(len(idx0["entries"])) if i != ri)
    assert idx1["sourceCatalogSha256"] == idx0["sourceCatalogSha256"]
    assert idx1["currentSourceCatalogBinding"] == idx0["currentSourceCatalogBinding"]
    assert [e["id"] for e in idx1["entries"] if e["authoredStatus"] == "pending-authored-procedure"] == pending_after
    idxbytes = enc(idx1)
    INDEX.write_bytes(idxbytes)
    index_ref = bind(INDEX, idxbytes)

    queue_obj = {
        "id": "CURRENT-SPELL-QUEUE-475", "supersedesQueue": bind(QUEUE0),
        "currentAuthority": authority_after, "currentIndexBinding": index_ref,
        "currentCatalogBinding": q0["currentCatalogBinding"], "remainingPendingIds": pending_after,
        "continuingPriorityOrder": priority, "continuingPriorityOrderIsPrioritySubset": False,
        "nextIdentity": "elemental-shell", "nextBlockerIds": ["DF218-B01", "DF218-B02"],
        "closureTasksRemaining": 17, "firstReviewTasksRemaining": 0, "acceptedUnapplied": 0,
        "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIdsThisStep": [BLOCKER],
        "application": app_ref,
        "pendingIdentityAuditPath": pending_path.relative_to(ROOT).as_posix(),
        "currentHandoffPath": handoff_path.relative_to(ROOT).as_posix(),
        "runtimeExecuted": False, "runtimeSelectionEnabled": False,
        "retainedHolds": "The 17 unrelated pending identities remain unchanged. PG200-B06 is closed only for Fortress static authored-procedure review; H01-H10 and all operational/downstream gates remain retained.",
        "currentReviewPacket": {"path": "elemental_shell_caster_qualification_472/SHELL_CASTER_QUALIFICATION_472_TESTONLY.json",
                                "classification": "READY_FOR_DIRECTOR_READBACK_TESTONLY_CASTER_QUALIFICATION",
                                "proposal468Sha256": "de4bd28b11d33be17a9185f925fae4c740956a10f7aaf5d89bcddc16a7bb8169",
                                "ownerAdopted": True, "testOnlyCasterQualificationPremisePrepared": True,
                                "casterQualificationDisposition": "READY_FOR_DIRECTOR_READBACK",
                                "castOrWitnessAuthorized": False, "identityAcceptedOrApplied": False},
        "directorReadback": rbr,
    }
    qr = write(queue_path, queue_obj)
    pending_obj = {
        "id": "CURRENT17-PENDING-IDENTITY-AUDIT-475", "recordedAtUtc": stamp(),
        "authority": authority_after, "pendingCount": 17, "pendingIds": pending_after,
        "indexBinding": index_ref, "currentQueueBinding": qr,
        "nextPriorityOrder": priority, "acceptedUnappliedIds": [],
        "appliedIdentityThisStep": ID, "closedBlockerThisStep": BLOCKER,
        "nextStep": "Elemental Shell / DF218-B01 and DF218-B02: submit the Proposal468-bound caster qualification for Director readback; no cast, witness, or identity disposition is authorized by the qualification packet.",
    }
    pr = write(pending_path, pending_obj)
    handoff_obj = {
        "id": "CURRENT-HANDOFF-475", "supersedes": HANDOFF0.relative_to(ROOT).as_posix(),
        "queue": qr, "pendingIdentityAudit": pr, "authority": authority_after,
        "continuingPriorityOrder": priority, "closureTasksRemaining": 17, "firstReviewTasksRemaining": 0,
        "nextStep": pending_obj["nextStep"], "currentApplication": app_ref,
        "nativeCatalogAndDownstreamGatesUnchanged": True,
        "FortressDisposition": {"scope": acceptance_obj["scope"], "accepted": True, "applied": True,
                                 "closedBlockerIds": [BLOCKER], "retainedQualificationIds": QUALS,
                                 "componentCoverage": cov["counts"],
                                 "sourceProcedureStatus": source["status"], "sourceOperational": None,
                                 "sourceHoldRegisterUnchanged": True, "nativeCatalogUnchanged": True,
                                 "runtimeSelectionEnabled": False},
        "DirectorReadback474": rbr,
        "W13Witness471": {"path": bind(W13 / "DIRECTOR_READBACK_471.json")["path"],
                          "sha256": bind(W13 / "DIRECTOR_READBACK_471.json")["sha256"],
                          "status": "PASS_FOR_ADOPTED_TEST_ONLY_COMPONENT_SUFFICIENCY_UNSEALED"},
        "ElementalShell468Next": {"packet": "elemental_shell_caster_qualification_472/SHELL_CASTER_QUALIFICATION_472_TESTONLY.json",
                                  "proposalSha256": "de4bd28b11d33be17a9185f925fae4c740956a10f7aaf5d89bcddc16a7bb8169",
                                  "ownerAdoption": bind(BASE / "elemental_shell_caster_premise_proposal_468/OWNER_DF218_B02_SHELL_CASTER_PREMISE_ADOPTION_468_TESTONLY.json"),
                                  "casterQualificationReadyForDirector": True,
                                  "castOrWitnessAuthorized": False},
    }
    hr = write(handoff_path, handoff_obj)

    ops = {"id": "FORTRESS-STATIC-INDEX-OPERATIONS-475", "beforeBinding": bind(INDEX, idxraw),
           "afterBinding": index_ref, "backup": backup_ref, "acceptedIds": [ID], "appliedIds": [ID],
           "closedBlockerIds": [BLOCKER], "retainedQualificationIds": QUALS,
           "onlyFortressIndexRowChanged": True, "allOtherIndexRowsByteSemanticallyUnchanged": True,
           "authoredCountsBeforeAfter": [{"reviewed": 830, "pending": 18}, {"reviewed": 831, "pending": 17}],
           "catalogByteExact": CATALOG.read_bytes() == catraw,
           "sourceProcedureByteExact": PROCEDURE.read_bytes() == procr,
           "sourceHoldRegisterByteExact": HOLD_REGISTER.read_bytes() == holdraw,
           "historicalEvidenceByteExact": True, "runtimeSelectionEnabled": False,
           "inverseRestoresExactIndex": backup.read_bytes() == idxraw}
    ops_ref = write(ops_path, ops)
    assert CATALOG.read_bytes() == catraw and PROCEDURE.read_bytes() == procr and HOLD_REGISTER.read_bytes() == holdraw
    assert read(INDEX)["authoredCounts"] == {"reviewed": 831, "pending": 17}
    assert read(queue_path)["currentIndexBinding"]["sha256"] == index_ref["sha256"]
    assert read(pending_path)["currentQueueBinding"]["sha256"] == qr["sha256"]
    assert read(handoff_path)["queue"]["sha256"] == qr["sha256"]
    assert read(handoff_path)["pendingIdentityAudit"]["sha256"] == pr["sha256"]
    assert sha(git_blob(Path("DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"), head)) == EXPECTED["catalog"]

    validation = {
        "id": "FORTRESS-STATIC-APPLICATION-VALIDATION-475", "recordedAtUtc": stamp(), "status": "PASS",
        "checks": [
            "GPT Director response binds exact coverage473, identity474, retained procedure and accepts Fortress for static authored-procedure review only.",
            "Director explicitly authorizes the authored-review-index-only application and closes PG200-B06 within that scope.",
            "The 13-row component register is 9 component-sufficient unsealed, 4 existing TEST_ONLY seals, 0 open integrations; W11 limitation preserved.",
            "Only the Fortress authored-review index row and one standalone envelope registration changed.",
            "Authority is 831 applied / 17 pending / 0 accepted-unapplied; 555 standalone procedures / 173 interfaces.",
            "All unrelated pending IDs and all other authored-review index entries are unchanged.",
            "Native catalog, retained procedure, source HOLD_REGISTER, historical evidence, and original operational=null remain byte-exact.",
            "PG200-H01 through PG200-H10 remain retained; PG200-B06 closure is limited to static authored review.",
            "No runtime, implementation, human-play, balance, cosmology, domain, release or campaign claim was enabled.",
            "Queue, pending audit, and handoff cross-bind current index bytes and 831/17/0 authority.",
            "Index backup is byte-exact and restores the prior 830/18/0 index state.",
            "Elemental Shell Proposal468 qualification is the next Director review; it authorizes no cast, witness, acceptance, or application.",
        ],
        "checkCount": 12, "passedChecks": 12, "failedChecks": 0,
        "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER],
        "retainedQualificationIds": QUALS, "authority": authority_after,
        "directorAcceptance": accept_ref, "directorReadback": rbr,
        "application": app_ref, "candidateModel": model_ref, "candidatePackageManifest": manifest_ref,
        "indexOperations": ops_ref, "queue": qr, "pendingIdentityAudit": pr, "handoff": hr,
        "catalogChanged": False, "sourceProcedureChanged": False, "sourceHoldRegisterChanged": False,
        "runtimeSelectionEnabled": False, "nextIdentity": "elemental-shell",
    }
    vr = write(validation_path, validation)
    snapshot_path.write_text(
        "# Spell review snapshot — Fortress 475\n\n"
        "**831 applied / 17 pending / 0 accepted-unapplied; 555 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "GPT Director accepted Conjure Demiplane Fortress for static authored-procedure review only and authorized application to the authored-review index only. PG200-B06 is closed for this scope; H01–H10 remain retained. The source procedure remains unresolved with operational=null, the native catalog and historical evidence are unchanged, and runtime and downstream gates remain closed.\n\n"
        "Coverage473 records 13 obligations: nine component-sufficient unsealed rows, four existing TEST_ONLY seals, and zero open integrations. W11’s limitation remains explicit.\n\n"
        "Next priority: Elemental Shell / DF218-B01 and DF218-B02. Proposal468-bound caster qualification is ready for GPT review; no cast or witness is authorized by that packet.\n\n"
        f"Validation: {validation_path.relative_to(ROOT).as_posix()} (SHA-256 {vr['sha256']}).\n",
        encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "authority": authority_after, "acceptance": accept_ref,
                      "application": app_ref, "validation": vr, "index": index_ref,
                      "queue": qr, "pendingIdentityAudit": pr, "handoff": hr}, indent=2))


if __name__ == "__main__":
    main()
