#!/usr/bin/env python3
"""Apply only the explicitly accepted Gate closure to the authored review index."""
import concurrent.futures
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import zlib

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
REV = "a669773b9f7b8cdea5c250b59aa9ceaa273b6f14"
BASE_REL = BASE.relative_to(REPO).as_posix()
OUT = BASE / "banishment_gate_closure404"
W03 = BASE / "banishment_gate_w03_lich_taxonomy_witness400_repack03"
PKT = W03 / "packet"
INDEX_REL = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CAND_REL = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9banishmentgate_reviewed_404"
CAND = REPO / CAND_REL
SEALS = {
    "W01": "PG327_W01_DIRECTOR_SEAL_365_REPACK04.json",
    "W02": "PG327_W02_DIRECTOR_SEAL_364_REPACK03.json",
    "W04": "PG327_W04_DIRECTOR_SEAL_365_REPACK02.json",
    "W05": "banishment_gate_witness365_w05_separation365_repack03_build01/PG327-W05-365-REPACK03-DIRECTOR-SEAL.json",
    "W06": "PG327_W06_DIRECTOR_SEAL_365_REPACK06.json",
    "W07": "PG327_W07_DIRECTOR_SEAL_363_REPACK01.json",
    "W08": "PG327_W08_DIRECTOR_SEAL_365_REPACK04.json",
}


def h(data):
    return hashlib.sha256(data).hexdigest()


def readgit(path):
    return subprocess.check_output(["git", "show", REV + ":" + path], cwd=REPO)


def binding(path, data=None):
    data = path.read_bytes() if data is None else data
    return {"path": path.relative_to(REPO).as_posix(), "bytes": len(data), "sha256": h(data), "crc32": format(zlib.crc32(data) & 0xffffffff, "08x")}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode())
    return binding(path)


def main():
    validation_path = W03 / "INDEPENDENT_VERIFICATION_400_REPACK03.json"
    verification = json.loads(validation_path.read_bytes())
    archive = W03 / "DD_Rank9_BanishmentGate_PG327W03_LichTaxonomy_Witness400_Repack03_TESTONLY.zip"
    assert verification["result"] == "PASS" and verification["R6"] == "PASS"
    assert verification["archiveSha256"] == h(archive.read_bytes())
    oldbytes = readgit(INDEX_REL)
    old = json.loads(oldbytes)
    queuebytes = readgit(BASE_REL + "/CURRENT_SPELL_QUEUE_361.json")
    queue = json.loads(queuebytes)
    assert old["authoredCounts"] == {"reviewed": 828, "pending": 20}
    assert old["entries"][89]["id"] == "banishment-gate"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ".gitattributes").write_text("** -text !eol\n", encoding="utf-8")
    CAND.mkdir(parents=True, exist_ok=True)
    (CAND / ".gitattributes").write_text("** -text !eol\n", encoding="utf-8")

    witnesses = []
    for witness, source in SEALS.items():
        raw = readgit(BASE_REL + "/" + source)
        record = json.loads(raw)
        assert not record.get("remainingResidualIds", record.get("remaining" + witness + "ResidualIds", []))
        text = json.dumps(record)
        assert "SEALED_TEST_ONLY" in text or "PASSES for this TEST_ONLY witness" in text
        target = OUT / "preserved_seals" / (witness + ".json")
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(raw)
        witnesses.append({"witnessId": "PG327-" + witness, "status": "SEALED_TEST_ONLY", "receipt": binding(target), "sourceCommit": REV, "sourcePath": BASE_REL + "/" + source})
    seal = {
        "id": "PG327-W03-400-REPACK03-DIRECTOR-SEAL", "decision": "SEALED_TEST_ONLY",
        "witnessId": "PG327-W03", "w03Satisfied": True,
        "archive": binding(archive), "independentVerification": binding(validation_path),
        "closedResidualIds": ["W03-400-R" + str(i) for i in range(1, 8)],
        "remainingResidualIds": [], "remainingDefectPaths": [],
        "sourceAcceptance": binding(PKT / "sources/OWNER_SOURCE_ACCEPTANCE_399.json"),
        "proposalSha256": "a0d22b2c54958e12e93df890b169e70b578f4f66e055c5fc75f172f64271fac1",
        "authority": "Owner's current instruction authorizes fixing, approving and applying completed closures; supersedes the earlier review-only/no-seal restriction for this verified closure.",
        "scope": "Conditional TEST_ONLY witness only; same extant body type change without crossing; no campaign event or runtime execution.",
        "counterspell": "Existing automatic Wizard class matrix; B/D source-qualified eligible declines; no new global rule or D&D rule import.",
    }
    seal_binding = write(OUT / "W03_DIRECTOR_SEAL_404.json", seal)
    witnesses.append({"witnessId": "PG327-W03", "status": "SEALED_TEST_ONLY", "receipt": seal_binding})
    witnesses.sort(key=lambda x: x["witnessId"])
    assert [w["witnessId"] for w in witnesses] == ["PG327-W0" + str(i) for i in range(1, 9)]
    qualifications = ["PG200-H" + str(i).zfill(2) for i in range(1, 11)]
    acceptance = {
        "id": "BANISHMENT-GATE-CLOSURE404-DIRECTOR-ACCEPTANCE", "decision": "ACCEPT",
        "acceptedIds": ["banishment-gate"], "appliedIds": [], "heldIds": [],
        "closedBlockerIds": ["PG200-B03", "PG200-B04"], "remainingResidualIds": [],
        "applicationAuthorized": True, "applicationAuthorizedIds": ["banishment-gate"],
        "witnessCoverage": witnesses, "retainedQualificationIds": qualifications,
        "scope": "Authored operational review only. Preserve all historical records, native card/source status and TEST_ONLY limits; runtime and all downstream gates stay closed.",
        "unrelatedDispositionsChanged": False, "queueBefore": queue["currentAuthority"],
        "expectedAfterApplication": {"reviewedApplied": 829, "pending": 19, "acceptedUnapplied": 0, "completeStandaloneProcedures": 553, "scopedInterfaces": 173},
    }
    accept_binding = write(OUT / "DIRECTOR_ACCEPTANCE_404.json", acceptance)

    case_prefix = BASE_REL + "/banishment_gate_return327_received/evidence/packet327/prior/cases/"
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", REV, case_prefix], cwd=REPO).decode().splitlines()
    assert len(paths) == 9
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        historical = [{"sourceCommit": REV, "binding": binding(REPO / path, raw), "status": "PRESERVED_HISTORICAL_NOT_RECLASSIFIED"} for path, raw in zip(paths, pool.map(readgit, paths))]
    coverage_binding = write(CAND / "CASE_COVERAGE.json", {"historicalCases": historical, "witnesses": witnesses, "remainingWitnessIds": [], "originalsUnchanged": True})
    procraw = (PKT / "sources/RETURN327_BANISHMENT_GATE_PROCEDURE.json").read_bytes()
    proc = json.loads(procraw)
    catalog = json.loads((PKT / "sources/W07_BOUND_CATALOG_351fe708.json").read_bytes())
    native = catalog["spells"][89]
    model = {
        "id": "RANK9-BANISHMENT-GATE-REVIEWED-404", "status": "REVIEWED_AUTHORED_OPERATIONAL_PLAYTEST",
        "spells": [{"id": "banishment-gate", "name": "Banishment Gate", "nativeCard": native,
                    "procedure": {"procedureContent": proc["procedure"], "sharedContract": proc["sharedContract"]},
                    "directorProcedureRecord": proc, "sourceProcedureBinding": binding(PKT / "sources/RETURN327_BANISHMENT_GATE_PROCEDURE.json"),
                    "qualificationIds": qualifications}],
        "sharedRequirements": proc["sharedContract"], "caseEvidence": coverage_binding,
        "acceptance": accept_binding, "runtimeSelectionEnabled": False,
        "scope": "Discovery envelope; original procedure and native card preserved. No campaign, canon, implementation, balance, cosmology or release approval.",
    }
    model_binding = write(CAND / "MODEL.json", model)
    manifest_binding = write(CAND / "CANDIDATE_PACKAGE_MANIFEST.json", {"id": "BANISHMENT-GATE-404-CANDIDATE-MANIFEST", "files": [model_binding, coverage_binding]})
    application = {
        "id": "BANISHMENT-GATE-CLOSURE404-APPLICATION", "acceptedIds": ["banishment-gate"], "appliedIds": ["banishment-gate"],
        "acceptance": accept_binding, "applicationScope": "Authored review index only; no native catalog/source procedure or runtime promotion",
        "indexBefore": binding(REPO / INDEX_REL, oldbytes), "model": model_binding,
        "authorityBefore": queue["currentAuthority"], "authorityAfter": acceptance["expectedAfterApplication"],
        "closedBlockerIds": ["PG200-B03", "PG200-B04"], "otherIdentityRowsChanged": False,
        "publication": "Local committed application; remote synchronization must be separately verified",
    }
    app_binding = write(OUT / "APPLICATION_404.json", application)
    new = copy.deepcopy(old)
    row = new["entries"][89]
    row.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank9banishmentgate_reviewed_404/MODEL.json",
        "procedurePointer": "/spells/0/procedure", "procedureTextPointer": "/spells/0/procedure/procedureContent",
        "wholeCardPointer": "/spells/0", "wholeCardIdField": "id", "sourceCatalogWholeCardPointer": "/spells/89",
        "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord", "sharedRulesPointer": "/sharedRequirements",
        "spellLocalRequirementsPointer": "/spells/0/procedure", "runtimeSelectionEnabled": False,
        "completeEvidenceRoot": CAND_REL, "completeEnvelopeBinding": model_binding,
        "caseEvidenceBindings": coverage_binding, "candidatePackageManifestBinding": manifest_binding,
        "authoredAcceptanceReceipt": accept_binding, "authoredApplicationReceipt": app_binding,
        "sourceArchiveBinding": binding(archive), "independentReviewBinding": binding(validation_path),
        "reviewId": acceptance["id"], "accepted": True, "applied": True,
        "closedBlockerIds": ["PG200-B03", "PG200-B04"], "retainedQualificationIds": qualifications,
        "applicationScope": application["applicationScope"], "historicalCandidateLabelsPreserved": True,
        "retainedQualifications": [acceptance["scope"]],
    })
    new["authoredCounts"] = {"reviewed": 829, "pending": 19}
    new["representationCounts"]["completeReviewedStandaloneProcedures"] = 553
    new["additionalStandaloneEnvelopes"].append({"file": row["procedureFile"], "binding": model_binding, "reviewId": acceptance["id"], "acceptedIds": ["banishment-gate"], "authority": accept_binding, "receipt": app_binding})
    for i in range(len(old["entries"])):
        if i != 89:
            assert old["entries"][i] == new["entries"][i]
    assert row["sourceStatus"] == old["entries"][89]["sourceStatus"]
    assert new["sourceCatalogSha256"] == old["sourceCatalogSha256"]
    pending = [r["id"] for r in new["entries"] if r["authoredStatus"] == "pending-authored-procedure"]
    assert len(pending) == 19
    index_binding = write(REPO / INDEX_REL, new)
    order = [i for i in queue["continuingPriorityOrder"] if i != "banishment-gate"]
    assert set(order) == set(pending)
    next_queue = {
        "id": "CURRENT-SPELL-QUEUE-404", "supersedesQueue": binding(REPO / (BASE_REL + "/CURRENT_SPELL_QUEUE_361.json"), queuebytes),
        "currentAuthority": acceptance["expectedAfterApplication"], "currentIndexBinding": index_binding,
        "currentCatalogBinding": queue["currentCatalogBinding"], "remainingPendingIds": pending,
        "continuingPriorityOrder": order, "continuingPriorityOrderIsPrioritySubset": False,
        "nextIdentity": "conjure-demiplane-fortress", "nextBlockerIds": ["PG200-B06"],
        "closureTasksRemaining": 19, "firstReviewTasksRemaining": 0, "acceptedUnapplied": 0,
        "acceptedIds": ["banishment-gate"], "appliedIds": ["banishment-gate"],
        "closedBlockerIdsThisStep": ["PG200-B03", "PG200-B04"], "application": app_binding,
        "currentHandoff": BASE_REL + "/CURRENT_HANDOFF_404.json", "currentHandoffPath": BASE_REL + "/CURRENT_HANDOFF_404.json",
        "runtimeExecuted": False, "runtimeSelectionEnabled": False,
        "retainedHolds": "All other identity holds and qualifications remain unchanged; no blanket approval inferred.",
        "publication": "Local application pending verified remote synchronization",
    }
    queue_binding = write(BASE / "CURRENT_SPELL_QUEUE_404.json", next_queue)
    write(BASE / "CURRENT_HANDOFF_404.json", {
        "id": "CURRENT-HANDOFF-404", "supersedes": BASE_REL + "/CURRENT_HANDOFF_361.json",
        "queue": queue_binding, "authority": acceptance["expectedAfterApplication"], "continuingPriorityOrder": order,
        "closureTasksRemaining": 19, "firstReviewTasksRemaining": 0,
        "nextStep": "Conjure Demiplane Fortress / PG200-B06: continue the source-bound outstanding structural, scribing and remaining witness obligations; preserve its existing seals.",
        "currentApplication": app_binding, "nativeCatalogAndDownstreamGatesUnchanged": True,
        "publication": "Local application pending verified remote synchronization",
    })
    report = {
        "id": "BANISHMENT-GATE-CLOSURE404-APPLICATION-READBACK", "result": "PASS",
        "checks": {"onlyGateIndexRowChanged": True, "allEightWitnessesSealed": True, "nineHistoricalCasesBoundUnchanged": True,
                   "nativeCardEqualsSource": model["spells"][0]["nativeCard"] == native,
                   "procedureEqualsSource": model["spells"][0]["procedure"]["procedureContent"] == proc["procedure"],
                   "allOther847IndexRowsUnchanged": True, "pendingInventoryCount19": True,
                   "priorityOrderCoversEveryPendingIdentity": True, "sourceCatalogBindingUnchanged": True,
                   "runtimeSelectionDisabled": True, "noCanonicalPromotion": True},
        "indexAfter": index_binding, "authorityAfter": acceptance["expectedAfterApplication"], "queue": queue_binding,
    }
    write(OUT / "APPLICATION_READBACK_404.json", report)
    print(json.dumps({"result": "PASS", "acceptedIds": ["banishment-gate"], "locallyAppliedIds": ["banishment-gate"], "authorityAfter": acceptance["expectedAfterApplication"], "nextIdentity": "conjure-demiplane-fortress"}))


if __name__ == "__main__":
    main()
