#!/usr/bin/env python3
"""Independent checks for Fortress static acceptance/application 475."""
import hashlib
import json
import subprocess
import zlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
APP = BASE / "fortress_static_acceptance_475"
CAND = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9fortress_static_reviewed_475"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PROCEDURE = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/procedures/conjure-demiplane-fortress.json"
HOLD = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9planargates5_reviewed_200/HOLD_REGISTER.json"
ID = "conjure-demiplane-fortress"
BLOCKER = "PG200-B06"
QUALS = [f"PG200-H{i:02d}" for i in range(1, 11)]
CHECKS = []


def check(label, ok, actual=None):
    CHECKS.append({"check": label, "passed": bool(ok), **({"actual": actual} if actual is not None else {})})
    if not ok:
        raise AssertionError(f"FAIL: {label}: {actual}")


def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def crc(b):
    return f"{zlib.crc32(b) & 0xffffffff:08x}"


def git_blob(path, commit):
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(["git", "show", f"{commit}:{rel}"], cwd=ROOT)


def verify_binding(b, commit):
    p = ROOT / b["path"]
    raw = git_blob(p, commit) if b.get("byteDomain") == "exact committed Git blob" else p.read_bytes()
    check(f"binding: {b['path']}", len(raw) == b["bytes"] and sha(raw) == b["sha256"]
          and ("crc32" not in b or crc(raw) == b["crc32"]), {"bytes": len(raw), "sha256": sha(raw)})


def main():
    root = read(APP / "DIRECTOR_READBACK_474.json")
    acceptance = read(APP / "DIRECTOR_ACCEPTANCE_475.json")
    application = read(APP / "APPLICATION_475.json")
    coverage = read(BASE / "fortress_w01_w13_coverage_readback_473/FORTRESS_W01_W13_COVERAGE_RECONCILIATION_473.json")
    identity = read(BASE / "fortress_identity_level_reconciliation_474/FORTRESS_IDENTITY_LEVEL_RECONCILIATION_474.json")
    model = read(CAND / "MODEL.json")
    case = read(CAND / "CASE_COVERAGE.json")
    manifest = read(CAND / "CANDIDATE_PACKAGE_MANIFEST.json")
    idx0 = read(APP / "authored_review_index.before_fortress_475.json")
    idx1 = read(INDEX)
    q0 = read(BASE / "CURRENT_SPELL_QUEUE_465_REPACK01.json")
    queue = read(BASE / "CURRENT_SPELL_QUEUE_475.json")
    pending = read(BASE / "CURRENT17_PENDING_IDENTITY_AUDIT_475.json")
    handoff = read(BASE / "CURRENT_HANDOFF_475.json")
    initial_commit = acceptance["sourceSnapshotCommit"]

    decision = root["structuredDecision"]
    check("exact Director accept and scope recorded", decision["decision"] == "ACCEPT" and decision["spellId"] == ID
          and decision["scope"] == "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY")
    check("Director authorized only authored-review-index application", decision["applicationAuthorized"] is True
          and decision["applicationScope"] == "FORTRESS_AUTHORED_REVIEW_INDEX_ONLY")
    check("Director closed B06 only in this scope and retained H01-H10",
          decision["closedBlockerIds"] == [BLOCKER] and decision["retainedQualificationIds"] == QUALS)
    check("Director said no application had occurred in response", root["applicationOccurredInDirectorResponse"] is False)
    check("acceptance preserves its unapplied state before application",
          acceptance["status"] == "ACCEPTED_UNAPPLIED" and acceptance["acceptedIds"] == [ID]
          and acceptance["appliedIds"] == [] and acceptance["applicationAuthorized"] is True)
    check("all 13 coverage obligations bind 9/4/0 counts", coverage["counts"]["rows"] == 13
          and coverage["counts"]["componentSufficientUnsealed"] == 9
          and coverage["counts"]["sealedTestOnlyComponents"] == 4
          and coverage["counts"]["openIntegrations"] == 0)
    check("W11 limitation remains explicit", "invertible state-patch chain not certified" in json.dumps(coverage["rows"]))
    check("identity reconciliation and decision use the same coverage and procedure hashes",
          acceptance["evidenceBindings"]["coverageReconciliation473"]["sha256"] == identity["coverageReconciliation"]["sha256"]
          and acceptance["evidenceBindings"]["retainedProcedure"]["sha256"] == identity["retainedProcedure"]["gitBlobSha256"])

    old_row = next(r for r in idx0["entries"] if r["id"] == ID)
    new_row = next(r for r in idx1["entries"] if r["id"] == ID)
    check("only Fortress authored-index row changed", all(idx0["entries"][i] == idx1["entries"][i]
          for i in range(len(idx0["entries"])) if idx0["entries"][i]["id"] != ID))
    check("Fortress row is accepted and applied only to authored index", new_row["accepted"] is True
          and new_row["applied"] is True and new_row["applicationScope"].startswith("Fortress authored-review index only"))
    check("native source status remains blocked and runtime disabled", new_row["sourceStatus"] == old_row["sourceStatus"]
          == "blocked-pending-operational-review" and new_row["runtimeSelectionEnabled"] is False)
    check("PG200-B06 closure and H01-H10 retained", new_row["closedBlockerIds"] == [BLOCKER]
          and new_row["retainedQualificationIds"] == QUALS)
    check("index counts and standalone procedure count are 831/17 and 555",
          idx1["authoredCounts"] == {"reviewed": 831, "pending": 17}
          and idx1["representationCounts"]["completeReviewedStandaloneProcedures"] == 555)
    check("source catalog bindings remain unchanged in the index",
          idx1["sourceCatalogSha256"] == idx0["sourceCatalogSha256"]
          and idx1["currentSourceCatalogBinding"] == idx0["currentSourceCatalogBinding"])
    check("exactly one standalone envelope added", len(idx1["additionalStandaloneEnvelopes"])
          == len(idx0["additionalStandaloneEnvelopes"]) + 1)

    current_source = read(PROCEDURE)
    original_source = json.loads(git_blob(PROCEDURE, initial_commit))
    check("retained procedure is byte-exact to pre-application commit", PROCEDURE.read_bytes() == git_blob(PROCEDURE, initial_commit))
    check("retained procedure unresolved and operational=null", current_source == original_source
          and current_source["status"] == "UNRESOLVED_PROPOSED_PROCEDURE_REQUIRED_WITNESSES_BLOCKED"
          and current_source["nativeCardUnchanged"]["operational"] is None)
    check("original hold register is byte-exact and B06 remains open there",
          HOLD.read_bytes() == git_blob(HOLD, initial_commit)
          and identity["identityQualifications"]["currentHoldRegister"]["PG200-B06"]["status"] == "OPEN")
    catalog_work_binding = application["nativeCatalogWorkingRepresentationBeforeAfter"]
    check("native catalog working representation is byte-exact to its pre-application binding",
          len(CATALOG.read_bytes()) == catalog_work_binding["bytes"]
          and sha(CATALOG.read_bytes()) == catalog_work_binding["sha256"])
    check("native catalog committed object remains byte-exact to the pre-application queue binding",
          sha(git_blob(CATALOG, initial_commit)) == q0["currentCatalogBinding"]["sha256"])
    check("candidate envelope preserves source procedure and exact authored text",
          model["spells"][0]["sourceProcedureRecord"] == current_source
          and model["spells"][0]["procedure"]["procedureContent"] == current_source["procedure"])
    check("candidate overlay closes B06 only and carries all ten qualifications",
          model["spells"][0]["directorProcedureRecord"]["holdIds"] == QUALS
          and model["spells"][0]["directorProcedureRecord"]["closedBlockerIds"] == [BLOCKER])
    check("candidate remains runtime and downstream disabled", model["runtimeSelectionEnabled"] is False
          and model["implementationApproved"] is False and model["humanPlayApproved"] is False
          and model["balanceApproved"] is False and model["domainClosure"] is False and model["releaseApproved"] is False)

    pending0 = [e["id"] for e in idx0["entries"] if e["authoredStatus"] == "pending-authored-procedure"]
    pending1 = [e["id"] for e in idx1["entries"] if e["authoredStatus"] == "pending-authored-procedure"]
    check("pending set is the prior set minus Fortress", set(pending1) == set(pending0) - {ID} and len(pending1) == 17)
    authority = {"reviewedApplied": 831, "pending": 17, "acceptedUnapplied": 0,
                 "completeStandaloneProcedures": 555, "scopedInterfaces": 173}
    check("queue authority and pending IDs match the applied index", queue["currentAuthority"] == authority
          and queue["remainingPendingIds"] == pending1 and queue["acceptedUnapplied"] == 0)
    check("next identity is Elemental Shell with both blockers", queue["nextIdentity"] == "elemental-shell"
          and queue["nextBlockerIds"] == ["DF218-B01", "DF218-B02"])
    check("queue source catalog binding retained", queue["currentCatalogBinding"] == q0["currentCatalogBinding"])
    queue_binding = {"path": (BASE / "CURRENT_SPELL_QUEUE_475.json").relative_to(ROOT).as_posix(),
                     "bytes": (BASE / "CURRENT_SPELL_QUEUE_475.json").stat().st_size,
                     "sha256": sha((BASE / "CURRENT_SPELL_QUEUE_475.json").read_bytes()),
                     "crc32": crc((BASE / "CURRENT_SPELL_QUEUE_475.json").read_bytes())}
    check("pending audit and handoff cross-bind queue/index/authority", pending["currentQueueBinding"] == queue_binding
          and handoff["queue"] == queue_binding
          and queue["currentIndexBinding"]["sha256"] == sha(INDEX.read_bytes())
          and handoff["authority"] == authority and pending["authority"] == authority)
    check("Shell Proposal468 test-only qualification packet ready for Director with no cast/witness authority",
          queue["currentReviewPacket"]["ownerAdopted"] is True
          and queue["currentReviewPacket"]["proposal468Sha256"] == "de4bd28b11d33be17a9185f925fae4c740956a10f7aaf5d89bcddc16a7bb8169"
          and queue["currentReviewPacket"]["testOnlyCasterQualificationPremisePrepared"] is True
          and queue["currentReviewPacket"]["casterQualificationDisposition"] == "READY_FOR_DIRECTOR_READBACK"
          and queue["currentReviewPacket"]["castOrWitnessAuthorized"] is False)

    for p in [APP / "DIRECTOR_READBACK_474.json", APP / "DIRECTOR_ACCEPTANCE_475.json",
              APP / "APPLICATION_475.json", APP / "VALIDATION_475.json", CAND / "MODEL.json",
              CAND / "CASE_COVERAGE.json", CAND / "CANDIDATE_PACKAGE_MANIFEST.json",
              BASE / "CURRENT_SPELL_QUEUE_475.json", BASE / "CURRENT17_PENDING_IDENTITY_AUDIT_475.json",
              BASE / "CURRENT_HANDOFF_475.json"]:
        check(f"artifact present: {p.relative_to(ROOT).as_posix()}", p.is_file())
    for b in acceptance["evidenceBindings"].values():
        if isinstance(b, dict) and "path" in b and "bytes" in b and "sha256" in b:
            verify_binding(b, initial_commit)
    check("application receipt records exact one-ID scope", application["acceptedIds"] == [ID]
          and application["appliedIds"] == [ID] and application["applicationScope"] == "FORTRESS_AUTHORED_REVIEW_INDEX_ONLY"
          and application["closedBlockerIds"] == [BLOCKER])
    check("application receipt retains H01-H10 and records no side effects", application["retainedQualificationIds"] == QUALS
          and application["nativeCatalogChanged"] is False and application["sourceProcedureChanged"] is False
          and application["sourceHoldRegisterChanged"] is False and application["runtimeExecuted"] is False)

    validation_path = APP / "VALIDATION_475.json"
    validation = read(validation_path)
    check("builder validation is passing", validation["status"] == "PASS" and validation["failedChecks"] == 0
          and validation["passedChecks"] == validation["checkCount"])
    result = {"id": "FORTRESS-STATIC-APPLICATION-INDEPENDENT-VALIDATION-475",
              "status": "PASS", "checksPassed": len(CHECKS), "checksFailed": 0,
              "authority": authority, "indexSha256": sha(INDEX.read_bytes()),
              "queueSha256": sha((BASE / "CURRENT_SPELL_QUEUE_475.json").read_bytes()),
              "checks": CHECKS}
    result_path = APP / "INDEPENDENT_VALIDATION_475.json"
    result_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    result_path.write_bytes(result_bytes)
    result_binding = {"path": result_path.relative_to(ROOT).as_posix(), "bytes": len(result_bytes),
                      "sha256": sha(result_bytes), "crc32": crc(result_bytes)}
    handoff_path = BASE / "CURRENT_HANDOFF_475.json"
    handoff["independentValidation"] = result_binding
    handoff_bytes = (json.dumps(handoff, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    handoff_path.write_bytes(handoff_bytes)
    print(json.dumps({**result, "validationBinding": result_binding,
                      "handoffSha256": sha(handoff_bytes)}, indent=2))


if __name__ == "__main__":
    main()
