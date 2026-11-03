#!/usr/bin/env python3
"""Build a Fate Rewrite static-review reconciliation without changing identity or queue state."""
import copy, hashlib, json, subprocess
from pathlib import Path

BASE = "2299547210a528b8854253233407160f3899fec1"
IDENTITY = "fate-rewrite"
P05 = "FR-EP480-INTERFACE-PROPOSAL-05"
P05_SHA = "cd492a5bdf9c966f83a2674c31ff1db02a10d2df5f3c92fe8b4680974047386d"
R03_COMMIT = "477fda34de62295995d2fb779656fcbedb081121"
R03_PACKET_SHA = "e575b9ce6738dea5c780c18da95afa8daa8e53602beaf83795d20ca5a47da799"
R03_PASS_READBACK_SHA = "a9fca80d3c8e7bdef0ed799369d5e4cb0fcfd0b751a025dba685fa34d5c78e5e"
R03_PASS_READBACK = "docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03/CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_03.json"
DIRECTOR_STATUS = "docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03/CODEX_TRANSCRIBED_DIRECTOR_STATUS_POST_R03_PASS_01.json"
QUEUE = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_481.json"
HANDOFF = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_481.json"
PENDING_AUDIT = "docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT12_PENDING_IDENTITY_AUDIT_481.json"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
PROCEDURE = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192/procedures/fate-rewrite.json"
R320 = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_fate_rewrite_return320_received/"
R323 = "docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_eternal_prophecy_return323_received/"
EP480 = "docs/audit/2026-10-08/full-game/director-spell-review-129/eternal_prophecy_identity_reconciliation_2026-11-02/"
EP480_WITNESS = "docs/audit/2026-10-08/full-game/director-spell-review-129/eternal_prophecy_ep480_testonly_witness_2026-11-02/"
WITNESS = "docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_witness_2026-11-03/"
P05DIR = "docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_ep480_interface_spec_2026-11-02/"
OUT = Path("docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_identity_reconciliation_2026-11-03")
PACKET = OUT / "FATE_REWRITE_IDENTITY_RECONCILIATION_01.json"
REQUEST = OUT / "DIRECTOR_REVIEW_REQUEST_FATE_REWRITE_IDENTITY_01.md"
MANIFEST = OUT / "PACKET_MANIFEST_FATE_REWRITE_IDENTITY_01.json"
BUILDER = OUT / "tools/build_verify_fate_rewrite_identity_reconciliation_01.py"
STAMP = "2026-11-03T03:43:32Z"
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

def gitshow(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def load(path):
    return json.loads(gitshow(path))

def bind(path, role):
    raw = gitshow(path)
    blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()
    return {"path": path, "role": role, "bytes": len(raw), "sha256": sha(raw), "gitBlobSha1": blob}

def find_row(array, key, value):
    matches = [(i, item) for i, item in enumerate(array) if isinstance(item, dict) and item.get(key) == value]
    assert len(matches) == 1, f"expected exactly one {key}={value}, found {len(matches)}"
    return matches[0]

def main():
    queue = load(QUEUE)
    handoff = load(HANDOFF)
    audit = load(PENDING_AUDIT)
    catalog = load(CATALOG)
    index = load(INDEX)
    current_proc = load(PROCEDURE)
    r320_blocker = load(R320 + "BLOCKER_REASSESSMENT.json")
    r320_decision = load(R320 + "DIRECTOR_DECISION.json")
    r320_cases = load(R320 + "CASE_RESULTS.json")
    r320_questions = load(R320 + "QUESTION_DISPOSITIONS.json")
    r320_quals = load(R320 + "QUALIFICATIONS.json")
    r320_proc = load(R320 + "procedures/fate-rewrite.json")
    r323_blocker = load(R323 + "BLOCKER_REASSESSMENT.json")
    r323_decision = load(R323 + "DIRECTOR_DECISION.json")
    ep_reconciliation = load(EP480 + "IDENTITY_RECONCILIATION_EP480_01.json")
    ep_acceptance = load(EP480 + "CODEX_TRANSCRIBED_DIRECTOR_IDENTITY_ACCEPTANCE_EP480_01.json")
    ep_application = load(EP480 + "APPLICATION_EP480_STATIC_01.json")
    r03_packet = load(WITNESS + "FR_EP480_P05_TESTONLY_WITNESS_PACKET_R03.json")
    r03_pass = load(R03_PASS_READBACK)
    director_status = load(DIRECTOR_STATUS)
    p05_manifest = load(P05DIR + "PACKET_MANIFEST_05.json")

    assert queue["id"] == "CURRENT-SPELL-QUEUE-481" and queue["currentAuthority"]["reviewedApplied"] == 836
    assert queue["currentAuthority"]["pending"] == 12 and queue["currentAuthority"]["acceptedUnapplied"] == 0
    assert queue["nextIdentity"] == IDENTITY and queue["nextBlockerIds"] == ["TF192-B04"]
    assert queue["nextDependencyIds"] == ["TF192-B02"]
    assert handoff["nextIdentity"] == IDENTITY and handoff["nextBlockerIds"] == ["TF192-B04"]
    assert audit["firstReviewTasksRemaining"] == 0 and audit["closureTasksRemaining"] == 12
    assert audit["nextDependencyIds"] == ["TF192-B02"]
    catalog_i, catalog_row = find_row(catalog["spells"], "id", IDENTITY)
    index_i, index_row = find_row(index["entries"], "id", IDENTITY)
    assert catalog_row["status"] == "blocked-pending-operational-review" and catalog_row["operational"] is None
    assert index_row["authoredStatus"] == "pending-authored-procedure"
    assert current_proc["accepted"] is False and current_proc["applied"] is False
    assert r320_blocker["id"] == "TF192-B04" and r320_blocker["status"] == "OPEN"
    assert r323_blocker["id"] == "TF192-B02" and r323_blocker["status"] == "OPEN"
    assert r320_decision["heldIds"] == [IDENTITY] and not r320_decision["acceptedIds"] and not r320_decision["appliedIds"]
    assert r323_decision["heldIds"] == ["eternal-prophecy"] and not r323_decision["acceptedIds"]
    assert queue["acceptedIds"] == ["reverse-gravity-field", "eternal-prophecy"]
    assert "eternal-prophecy" in queue["appliedIds"]
    assert ep_acceptance["decision"]["scope"] == "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY"
    assert ep_acceptance["decision"]["disposition"] == "ACCEPT"
    assert ep_acceptance["decision"]["retainedOpenBlockerIds"] == ["TF192-B02"]
    assert ep_application["applicationScope"] == "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY"
    assert ep_application["guaranteeProved"] is False and ep_application["runtimeSelectionEnabled"] is False
    assert r03_packet["reviewedProposal"]["sha256"] == P05_SHA
    assert r03_pass["disposition"].startswith("PASS")
    assert r03_pass["reviewedCommit"] == R03_COMMIT
    assert r03_pass["reviewedPacket"]["sha256"] == R03_PACKET_SHA
    assert sha(gitshow(R03_PASS_READBACK)) == R03_PASS_READBACK_SHA
    assert sha(gitshow(P05DIR + "FATE_REWRITE_EP480_INTERFACE_PROPOSAL_05.json")) == P05_SHA
    assert p05_manifest["adoptionBinding"]["requiredSha256ManifestPointer"] == "/files/1/sha256"

    # Bind every original Fate Rewrite case and ensure result rows are a bijection to those files.
    case_prefix = R320 + "cases/"
    names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE, "--", case_prefix], cwd=ROOT, text=True).splitlines()
    case_paths = sorted(p for p in names if p.endswith(".json"))
    assert len(case_paths) == 17, f"expected 17 historical case files, found {len(case_paths)}"
    case_files = {load(p)["id"]: (p, load(p)) for p in case_paths}
    results = {r["id"]: r for r in r320_cases["results"]}
    assert len(results) == 17 and set(case_files) == set(results), "historical case/result set mismatch"
    history_crosswalk = []
    for case_id in r320_proc["caseIds"]:
        assert case_id in case_files and case_id in results
        case_path, case_obj = case_files[case_id]
        result = results[case_id]
        assert case_obj["status"] in ("DEMONSTRATED", "BLOCKED_EVIDENCE")
        assert case_obj["status"] == result["preservedStatus"]
        history_crosswalk.append({
          "caseId": case_id, "sourcePath": case_path,
          "sourceSha256": sha(gitshow(case_path)),
          "disposition": result["preservedStatus"], "holdIds": result.get("holdIds", []),
          "events": result.get("events"), "forwardOperations": result.get("forwardOperations"),
          "inverseOperations": result.get("inverseOperations"), "replay": result.get("replay"),
          "scope": result.get("scope"), "semanticDisposition": result.get("semanticDisposition")
        })
    assert sum(1 for x in history_crosswalk if x["disposition"] == "DEMONSTRATED") == 16
    assert sum(1 for x in history_crosswalk if x["disposition"] == "BLOCKED_EVIDENCE") == 1

    qualification_ids = list(r320_quals["qualificationIds"])
    expected_quals = ["TF192-H-DEATH", "TF192-H-HISTORY", "TF192-Q-BALANCE", "TF192-Q-COMPLETION",
      "TF192-Q-COSMOLOGY", "TF192-Q-DOMAIN", "TF192-Q-PHYSICAL", "TF192-Q-PLAY",
      "TF192-Q-RELEASE", "TF192-Q-RUNTIME", "TF192-Q-SOURCE"]
    assert qualification_ids == expected_quals
    question_ids = [q["questionId"] for q in r320_questions["dispositions"]]
    assert len(question_ids) == r320_questions["count"] == 10

    # Bind direct evidence and exact lineage. Source bytes all come from BASE.
    source_roles = [
      (QUEUE, "Current authoritative Queue481"), (HANDOFF, "Current handoff 481"),
      (PENDING_AUDIT, "Current pending identity audit 481"),
      (CATALOG, "Current spell catalog"), (INDEX, "Current authored review index"),
      (PROCEDURE, "Current retained Fate Rewrite candidate procedure"),
      (R320 + "BLOCKER_REASSESSMENT.json", "Return320 Fate Rewrite B04 reassessment"),
      (R320 + "DIRECTOR_DECISION.json", "Return320 Fate Rewrite decision"),
      (R320 + "CASE_RESULTS.json", "Return320 17 historical case results"),
      (R320 + "QUESTION_DISPOSITIONS.json", "Return320 question dispositions"),
      (R320 + "QUALIFICATIONS.json", "Return320 H and Q qualifications"),
      (R320 + "SOURCE_BINDING.json", "Return320 source binding inventory"),
      (R320 + "MANIFEST.json", "Return320 received packet manifest"),
      (R320 + "FUTURE_OBLIGATION_DISPOSITIONS.json", "Return320 future obligation limits"),
      (R320 + "PROVENANCE_NOTES.json", "Return320 provenance notes"),
      (R320 + "procedures/fate-rewrite.json", "Return320 retained held procedure"),
      (R323 + "BLOCKER_REASSESSMENT.json", "Return323 Eternal Prophecy B02 reassessment"),
      (R323 + "DIRECTOR_DECISION.json", "Return323 Eternal Prophecy decision"),
      (R323 + "CASE_RESULTS.json", "Return323 linked Eternal Prophecy historical coverage"),
      (R323 + "QUESTION_DISPOSITIONS.json", "Return323 linked question dispositions"),
      (R323 + "QUALIFICATIONS.json", "Return323 retained qualifications"),
      (R323 + "MANIFEST.json", "Return323 received packet manifest"),
      (EP480 + "IDENTITY_RECONCILIATION_EP480_01.json", "EP480 static identity reconciliation"),
      (EP480 + "CODEX_TRANSCRIBED_DIRECTOR_IDENTITY_ACCEPTANCE_EP480_01.json", "EP480 Director static-only acceptance readback"),
      (EP480 + "APPLICATION_EP480_STATIC_01.json", "EP480 static-only authored-index application receipt"),
      (EP480_WITNESS + "EP480_TESTONLY_WITNESS_PACKET_T1_T4.json", "EP480 accepted static-only witness evidence"),
      (EP480 + "PACKET_MANIFEST_EP480_IDENTITY_01.json", "EP480 identity packet manifest"),
      (P05DIR + "FATE_REWRITE_EP480_INTERFACE_PROPOSAL_05.json", "Owner-adopted Proposal05 machine terms"),
      (P05DIR + "FATE_REWRITE_EP480_INTERFACE_SPEC_05.md", "Proposal05 human specification"),
      (P05DIR + "PACKET_MANIFEST_05.json", "Proposal05 readiness and adoption-binding manifest"),
      (WITNESS + "OWNER_ADOPTION_RECEIPT_FR_EP480_P05.json", "Exact owner adoption receipt"),
      (WITNESS + "FR_EP480_P05_TESTONLY_WITNESS_PACKET_R03.json", "Director-passed R03 component witnesses"),
      (WITNESS + "PACKET_MANIFEST_FR_EP480_P05_WITNESSES_R03.json", "R03 component packet manifest"),
      (R03_PASS_READBACK, "Director PASS readback for R03"),
      (DIRECTOR_STATUS, "Director next-step and retained-blocker guidance"),
      (WITNESS + "tools/build_verify_fr_ep480_p05_witnesses_r03.py", "R03 replay and target-hash verifier")
    ]
    roles = dict(source_roles)
    for case_path in case_paths:
        roles[case_path] = "One of the 17 preserved Return320 Fate Rewrite historical cases"
    source_bindings = [bind(path, role) for path, role in roles.items()]
    by_path = {x["path"]: x for x in source_bindings}
    assert len(by_path) == len(roles), "duplicate source binding path"

    queue_obj = {
      "path": QUEUE, "sha256": by_path[QUEUE]["sha256"], "gitBlobSha1": by_path[QUEUE]["gitBlobSha1"],
      "reviewedApplied": 836, "pending": 12, "acceptedUnapplied": 0, "nextIdentity": IDENTITY,
      "nextBlockerIds": ["TF192-B04"], "nextDependencyIds": ["TF192-B02"],
      "priorityOrder": queue["continuingPriorityOrder"], "runtimeSelectionEnabled": False,
      "queueMutationRequested": False
    }
    catalog_snapshot = {"path": CATALOG, "sha256": by_path[CATALOG]["sha256"], "pointer": f"/spells/{catalog_i}", "row": catalog_row}
    index_snapshot = {"path": INDEX, "sha256": by_path[INDEX]["sha256"], "pointer": f"/entries/{index_i}", "row": index_row}

    ep_static_summary = {
      "identity": "eternal-prophecy",
      "acceptedScope": ep_acceptance["decision"]["scope"],
      "disposition": ep_acceptance["decision"]["disposition"],
      "appliedToAuthoredIndexOnly": ep_application["status"] == "APPLIED_TO_AUTHORED_REVIEW_INDEX_ONLY",
      "retainedOpenBlockers": ep_acceptance["decision"]["retainedOpenBlockerIds"],
      "guaranteeProved": ep_application["guaranteeProved"],
      "witnessSealed": ep_application["witnessSealed"],
      "runtimeSelectionEnabled": ep_application["runtimeSelectionEnabled"],
      "doesNotCloseFateRewriteB04": True
    }

    packet = {
      "schemaVersion": 1,
      "id": "FATE-REWRITE-IDENTITY-RECONCILIATION-01",
      "identity": IDENTITY,
      "displayName": "Fate Rewrite",
      "blockerId": "TF192-B04",
      "dependencyIds": ["TF192-B02"],
      "scope": "STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY",
      "classification": "DIRECTOR_STATIC_REVIEW_PACKET_NO_IDENTITY_ACCEPTANCE_OR_APPLICATION",
      "baseCommit": BASE,
      "sourceHashRule": "Every sourceBindings entry is read from its exact Git object at baseCommit and includes byte length, raw-byte SHA-256 and Git blob SHA-1. Catalog/index snapshots below are parsed views of those exact bound files.",
      "queueBefore": queue_obj,
      "currentCatalog": catalog_snapshot,
      "currentAuthoredReviewIndex": index_snapshot,
      "retainedProcedureAndHistoricalCoverage": {
        "currentProcedure": {"path": PROCEDURE, "sha256": by_path[PROCEDURE]["sha256"], "accepted": False,
          "applied": False, "blockerIds": current_proc.get("blockerIds", []), "holdIds": current_proc.get("holdIds", []),
          "caseIds": current_proc.get("caseIds", []), "questionIds": current_proc.get("questionIds", [])},
        "Return320Procedure": {"path": R320 + "procedures/fate-rewrite.json", "sha256": by_path[R320 + "procedures/fate-rewrite.json"]["sha256"],
          "status": r320_proc.get("status"), "accepted": r320_proc.get("accepted"), "applied": r320_proc.get("applied"),
          "blockerIds": r320_proc.get("blockerIds"), "holdIds": r320_proc.get("holdIds")},
        "Return320HistoricalCaseResults": {"path": R320 + "CASE_RESULTS.json", "sha256": by_path[R320 + "CASE_RESULTS.json"]["sha256"],
          "counts": r320_cases["counts"], "results": history_crosswalk},
        "questionDispositions": {"path": R320 + "QUESTION_DISPOSITIONS.json", "sha256": by_path[R320 + "QUESTION_DISPOSITIONS.json"]["sha256"],
          "count": r320_questions["count"], "dispositions": r320_questions["dispositions"]},
        "retainedQualifications": {"path": R320 + "QUALIFICATIONS.json", "sha256": by_path[R320 + "QUALIFICATIONS.json"]["sha256"],
          "qualificationIds": qualification_ids, "text": r320_quals["text"],
          "specialHistoryScopes": r320_blocker["qualificationScope"]},
        "return320BlockerReassessment": {"path": R320 + "BLOCKER_REASSESSMENT.json", "sha256": by_path[R320 + "BLOCKER_REASSESSMENT.json"]["sha256"],
          "status": r320_blocker["status"], "minimumMissingWitness": r320_blocker["minimumMissingWitness"],
          "mechanismGap": r320_blocker["mechanismGap"], "closurePaths": r320_blocker["closurePaths"]},
        "return320DirectorDecision": {"path": R320 + "DIRECTOR_DECISION.json", "sha256": by_path[R320 + "DIRECTOR_DECISION.json"]["sha256"],
          "status": r320_decision["status"], "heldIds": r320_decision["heldIds"], "blockerIds": r320_decision["decisions"][0]["blockerIds"],
          "dependencyIds": r320_decision["decisions"][0]["dependencyIds"]},
        "return323DependencyReassessment": {"path": R323 + "BLOCKER_REASSESSMENT.json", "sha256": by_path[R323 + "BLOCKER_REASSESSMENT.json"]["sha256"],
          "status": r323_blocker["status"], "minimumMissingWitness": r323_blocker.get("minimumMissingWitness"),
          "missingWitnessParts": r323_blocker.get("missingWitnessParts")},
        "return323DirectorDecision": {"path": R323 + "DIRECTOR_DECISION.json", "sha256": by_path[R323 + "DIRECTOR_DECISION.json"]["sha256"],
          "status": r323_decision["status"], "heldIds": r323_decision["heldIds"]},
        "ep480PriorStaticIdentityAcceptance": ep_static_summary
      },
      "adoptedTestOnlyEvidence": {
        "proposal": {"id": P05, "sha256": P05_SHA, "manifestPointer": "/files/1/sha256", "ownerAdopted": True,
          "scope": ["FR-EP480-IFACE-COMPAT-01", "FR-EP480-IFACE-CONFLICT-01"]},
        "componentPacket": {"path": WITNESS + "FR_EP480_P05_TESTONLY_WITNESS_PACKET_R03.json", "sha256": R03_PACKET_SHA,
          "reviewedCommit": R03_COMMIT, "branches": ["FR-EP480-IFACE-COMPAT-01", "FR-EP480-IFACE-CONFLICT-01"],
          "disposition": "PASS_ADOPTED_TEST_ONLY_COMPONENT_SUFFICIENCY_BOTH_BRANCHES", "witnessesSealed": False,
          "spellIdentityAcceptedOrApplied": False, "blockerIdsRemainOpen": ["TF192-B02", "TF192-B04"]},
        "directorPassReadback": {"path": R03_PASS_READBACK, "sha256": by_path[R03_PASS_READBACK]["sha256"]},
        "directorNextStepGuidance": {"path": DIRECTOR_STATUS, "sha256": by_path[DIRECTOR_STATUS]["sha256"]}
      },
      "identityCrosswalk": [
        {"requirement": "TF192-B02 — native Eternal Prophecy dependency", "status": "OPEN_NOT_CLOSED_BY_EP480_STATIC_ACCEPTANCE",
          "requiredBySource": r323_blocker.get("minimumMissingWitness"),
          "reconciledEvidence": "Eternal Prophecy received STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY acceptance and authored-index-only application; its own readback retains TF192-B02 OPEN and guaranteeProved=false.",
          "notEstablished": "No native source-qualified finite guarantee, adversarial closure through the original deadline, or affected external/parent history closure."},
        {"requirement": "TF192-B04 — Fate Rewrite committed guarantee and rewrite interoperability", "status": "OPEN_NOT_CLOSED_BY_R03",
          "requiredBySource": r320_blocker["minimumMissingWitness"],
          "reconciledEvidence": "R03 passes only two bounded TEST_ONLY compatible/conflicting interface branches with local costs, custody, memory, retry and inverse evidence.",
          "notEstablished": r320_blocker["mechanismGap"]},
        {"requirement": "Return320 historical case coverage", "status": "PRESERVED_STATIC_CASE_RESULTS_16_DEMONSTRATED_1_BLOCKED_EVIDENCE",
          "historicalCaseCount": 17, "caseIds": [x["caseId"] for x in history_crosswalk],
          "questionDispositionIds": question_ids, "qualificationIds": qualification_ids,
          "notEstablished": "Static case results and R03 component sufficiency do not prove native unconditional guarantee, actual campaign facts, or closure of any retained qualification."},
        {"requirement": "EP480 static-only result", "status": "PRIOR_ACCEPTANCE_APPLIED_WITH_B02_RETAINED_OPEN",
          "evidence": ep_static_summary,
          "notEstablished": "This prior static-only result is dependency context only and does not accept Fate Rewrite or close TF192-B02/B04."}
      ],
      "factsNotInferred": [
        "The native Fate Rewrite and Eternal Prophecy descriptions, exact sources, and access rows are unchanged.",
        "R03 is TEST_ONLY component evidence; no campaign event, source authority, seal, blocker closure, identity acceptance, or application is inferred.",
        "TF192-B02 and TF192-B04 remain OPEN; TF192-H-HISTORY and TF192-H-DEATH and all nine TF192-Q qualifications remain retained.",
        "The 17 Return320 case dispositions remain historical static results; 16 are DEMONSTRATED and one remains BLOCKED_EVIDENCE.",
        "EP480 static-only acceptance does not prove the native unconditional guarantee; guaranteeProved remains false.",
        "Runtime selection remains disabled; this packet requests no catalog, index, queue, canon, runtime, campaign, seal or blocker change."
      ],
      "requestedDirectorDisposition": {
        "question": "Does this exact reconciliation support a STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY disposition for Fate Rewrite that accurately records R03 component PASS and the retained 17-case/question/qualification evidence while keeping TF192-B02/B04 and all qualifications open? This is review classification only; do not accept or apply the Fate Rewrite identity.",
        "decisionOptions": ["PASS_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY_RECONCILIATION", "REVISE_WITH_EXACT_POINTERS", "HOLD_WITH_PRECISE_SOURCE_OR_EVIDENCE_GAP"],
        "requestedEffects": {"staticProcedureReviewDispositionRequested": True, "identityAcceptanceRequested": False,
          "identityApplication": False, "blockerClosure": False, "witnessSeal": False, "queueMutation": False,
          "catalogOrIndexMutation": False, "canonChange": False, "runtimeSelectionChange": False, "campaignFactAssertion": False}
      },
      "statusBeforeDirectorResponse": {"identity": IDENTITY, "identityStatus": "HELD",
        "blockers": {"TF192-B02": "OPEN", "TF192-B04": "OPEN"},
        "queue": {"reviewedApplied": 836, "pending": 12, "acceptedUnapplied": 0},
        "nextIdentity": IDENTITY, "identityAccepted": False, "identityApplied": False,
        "witnessesSealed": False, "runtimeSelectionEnabled": False},
      "sourceBindings": source_bindings
    }

    assert packet["currentAuthoredReviewIndex"]["row"]["authoredStatus"] == "pending-authored-procedure"
    assert packet["currentCatalog"]["row"]["operational"] is None
    assert packet["adoptedTestOnlyEvidence"]["componentPacket"]["spellIdentityAcceptedOrApplied"] is False
    OUT.mkdir(parents=True, exist_ok=True)
    (ROOT / PACKET).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    packet_sha = sha((ROOT / PACKET).read_bytes())
    request = f"""# Director review — Fate Rewrite static identity reconciliation, packet 01

This packet requests a separate `{packet['scope']}` reconciliation only. It does not request identity acceptance/application, a seal, blocker closure, or any source, catalog, index, queue, canon, runtime, or campaign change.

- Base main commit: `{BASE}`.
- Reconciliation packet: `{PACKET.as_posix()}` — SHA-256 `{packet_sha}`.
- Current Queue481: `{queue_obj['reviewedApplied']}/{queue_obj['pending']}/{queue_obj['acceptedUnapplied']}`; Fate Rewrite remains next, TF192-B04 OPEN with TF192-B02 dependency OPEN.
- Adopted Proposal05 component review: R03 PASS, commit `{R03_COMMIT}`, packet SHA-256 `{R03_PACKET_SHA}`.
- Current catalog row: `/spells/{catalog_i}`; authored-index row: `/entries/{index_i}`; both exact file hashes and blob IDs are in `sourceBindings`.

The reconciliation binds the current Fate Rewrite procedure and Queue481 sources; Return320's 17 historical cases (16 DEMONSTRATED, one BLOCKED_EVIDENCE), ten question dispositions and all 11 retained H/Q qualifications; the exact B02/B04 reassessments; the prior EP480 static-only acceptance/application; and the Proposal05 adoption, R03 PASS, and Director's next-step guidance. It distinguishes component sufficiency from native guarantee authority and preserves the current holds.

Please return `PASS_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY_RECONCILIATION`, `REVISE` with exact pointers, or `HOLD` with the precise source/evidence gap. Please do not accept or apply Fate Rewrite. Keep TF192-B02/B04, TF192-H-HISTORY/H-DEATH, all nine TF192-Q qualifications, unsealed witness status, and disabled runtime selection unchanged.
"""
    (ROOT / REQUEST).write_text(request, encoding="utf-8", newline="\n")
    manifest_files = []
    for path in (PACKET, REQUEST, BUILDER):
        raw = (ROOT / path).read_bytes()
        manifest_files.append({"path": path.as_posix(), "bytes": len(raw), "sha256": sha(raw)})
    manifest = {"schemaVersion": 1, "id": "FATE-REWRITE-IDENTITY-RECONCILIATION-MANIFEST-01",
      "classification": packet["classification"], "baseCommit": BASE,
      "identity": IDENTITY, "scope": packet["scope"], "packetSha256": packet_sha,
      "sourceBindingCount": len(source_bindings), "historicalFateRewriteCases": 17,
      "questionDispositionCount": len(question_ids), "retainedQualificationIds": qualification_ids,
      "files": manifest_files,
      "preservation": {"Queue481": "836/12/0", "TF192-B02": "OPEN", "TF192-B04": "OPEN",
        "allHAndQQualificationsRetained": True, "witnessesSealed": False,
        "identityAcceptedOrApplied": False, "runtimeSelectionEnabled": False,
        "noCatalogIndexQueueCanonRuntimeCampaignOrBlockerChange": True}}
    (ROOT / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    for entry in manifest_files:
        raw = (ROOT / entry["path"]).read_bytes()
        assert len(raw) == entry["bytes"] and sha(raw) == entry["sha256"], entry["path"]
    verify = json.loads((ROOT / PACKET).read_text(encoding="utf-8"))
    assert len(verify["retainedProcedureAndHistoricalCoverage"]["Return320HistoricalCaseResults"]["results"]) == 17
    assert verify["requestedDirectorDisposition"]["requestedEffects"]["identityAcceptanceRequested"] is False
    print("PASS baseCommit=" + BASE)
    print("PASS sourceBindings=" + str(len(source_bindings)) + " cases=17 questions=10 qualifications=11")
    print("PASS identity held; TF192-B02/B04 open; no application, seal, closure, or queue change")
    print("PASS packet SHA-256=" + packet_sha)

if __name__ == "__main__":
    main()
