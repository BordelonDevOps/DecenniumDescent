import hashlib
import json
import pathlib
import subprocess

REPO = pathlib.Path(r"C:\ep480fix")
BASE_COMMIT = "62876002c4d84b17b7c4a072ccd377ae4bd091cc"
SOURCE_ANCHOR = "38fec0bbf19a4480098eb10ab0d992b055790ada"
AUDIT = "docs/audit/2026-10-08/full-game/director-spell-review-129/"
CAND = "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192/"
CATALOG = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
QUEUE = AUDIT + "CURRENT_SPELL_QUEUE_481.json"
HANDOFF = AUDIT + "CURRENT_HANDOFF_481.json"
PENDING_AUDIT = AUDIT + "CURRENT12_PENDING_IDENTITY_AUDIT_481.json"
RETURN322 = AUDIT + "rank9_collapse_timeline_return322_received/"
RETURN320 = AUDIT + "rank9_fate_rewrite_return320_received/"
FATE_RECON = AUDIT + "fate_rewrite_identity_reconciliation_2026-11-03/"
FATE_WITNESS = AUDIT + "fate_rewrite_ep480_interface_witness_2026-11-03/"
OUT = REPO / pathlib.Path(AUDIT + "collapse_timeline_current_authority_review_2026-11-03")


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args])


def blob(commit, path):
    return git("show", f"{commit}:{path}")


def blob_sha(commit, path):
    return git("rev-parse", f"{commit}:{path}").decode().strip()


def jdata(commit, path):
    return json.loads(blob(commit, path).decode("utf-8-sig"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(name, obj):
    path = OUT / name
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return path


OUT.mkdir(parents=True, exist_ok=True)

queue = jdata(BASE_COMMIT, QUEUE)
handoff = jdata(BASE_COMMIT, HANDOFF)
pending_audit = jdata(BASE_COMMIT, PENDING_AUDIT)
catalog = jdata(BASE_COMMIT, CATALOG)
index = jdata(BASE_COMMIT, INDEX)
catrow = next(row for row in catalog["spells"] if row.get("id") == "collapse-timeline")
idxrow = next(row for row in index["entries"] if row.get("id") == "collapse-timeline")
catptr = f"/spells/{catalog['spells'].index(catrow)}"
idxptr = f"/entries/{index['entries'].index(idxrow)}"

anchor_catalog = jdata(SOURCE_ANCHOR, CATALOG)
anchor_index = jdata(SOURCE_ANCHOR, INDEX)
anchor_catrow = next(row for row in anchor_catalog["spells"] if row.get("id") == "collapse-timeline")
anchor_idxrow = next(row for row in anchor_index["entries"] if row.get("id") == "collapse-timeline")
procedure = jdata(BASE_COMMIT, CAND + "procedures/collapse-timeline.json")
candidate_manifest = jdata(BASE_COMMIT, CAND + "CANDIDATE_PACKAGE_MANIFEST.json")
candidate_decision = jdata(BASE_COMMIT, CAND + "DIRECTOR_DECISION.json")

r322_blocker = jdata(BASE_COMMIT, RETURN322 + "BLOCKER_REASSESSMENT.json")
r322_cases = jdata(BASE_COMMIT, RETURN322 + "CASE_RESULTS.json")
r322_quals = jdata(BASE_COMMIT, RETURN322 + "QUALIFICATIONS.json")
r322_questions = jdata(BASE_COMMIT, RETURN322 + "QUESTION_DISPOSITIONS.json")
r322_decision = jdata(BASE_COMMIT, RETURN322 + "DIRECTOR_DECISION.json")
r322_source_binding = jdata(BASE_COMMIT, RETURN322 + "SOURCE_BINDING.json")
r322_queue321 = jdata(BASE_COMMIT, RETURN322 + "authority/CURRENT_SPELL_QUEUE_321.json")
r322_handoff321 = jdata(BASE_COMMIT, RETURN322 + "authority/CURRENT_HANDOFF_321.json")
r320_decision = jdata(BASE_COMMIT, RETURN320 + "DIRECTOR_DECISION.json")
r320_blocker = jdata(BASE_COMMIT, RETURN320 + "BLOCKER_REASSESSMENT.json")
fate_reconciliation = jdata(BASE_COMMIT, FATE_RECON + "FATE_REWRITE_IDENTITY_RECONCILIATION_01.json")
fate_reconciliation_pass = jdata(BASE_COMMIT, FATE_RECON + "CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_FATE_REWRITE_IDENTITY_01.json")
fate_witness_pass = jdata(BASE_COMMIT, FATE_WITNESS + "CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_03.json")

case_ids = procedure["caseIds"]
case_result_ids = [row["id"] for row in r322_cases["results"]]
assert len(case_ids) == 17 and set(case_ids) == set(case_result_ids), "procedure and Return322 case identities differ"
case_file_paths = [RETURN322 + "cases/" + case_id + ".json" for case_id in case_ids]
for path in case_file_paths:
    blob(BASE_COMMIT, path)

# Current-authority assertions: bind to exact main snapshot and preserve the hold.
auth = queue["currentAuthority"]
assert auth == {"reviewedApplied": 836, "pending": 12, "acceptedUnapplied": 0, "completeStandaloneProcedures": 560, "scopedInterfaces": 173}
assert queue["nextIdentity"] == "fate-rewrite"
assert queue["remainingPendingIds"][-1] == "collapse-timeline"
assert queue["continuingPriorityOrder"][0:2] == ["fate-rewrite", "collapse-timeline"]
assert "collapse-timeline" in queue["remainingPendingIds"]
assert queue["runtimeSelectionEnabled"] is False and queue["runtimeExecuted"] is False
assert handoff["nextIdentity"] == "fate-rewrite" and handoff["acceptedUnapplied"] == 0
assert pending_audit["nextIdentity"] == "fate-rewrite" and pending_audit["firstReviewTasksRemaining"] == 0
assert catrow["id"] == "collapse-timeline" and catrow["status"] == "blocked-pending-operational-review"
assert catrow["operational"] is None and catrow["classAccess"]["Wizard"]["baseRpCost"] == 26
assert idxrow["id"] == "collapse-timeline" and idxrow["authoredStatus"] == "pending-authored-procedure"
assert catrow == anchor_catrow and idxrow == anchor_idxrow
assert procedure["currentCatalogSourceAndAccessUnchanged"] == catrow
assert procedure["currentIndexEntryUnchanged"] == idxrow
assert procedure["accepted"] is False and procedure["applied"] is False
assert "TF192-B05" in procedure["blockerIds"] and "TF192-B05" in procedure["holdIds"]
assert r322_blocker["status"] == "OPEN" and r322_blocker["dependencyIds"] == ["TF192-B02"]
assert r322_blocker["newMechanismAuthorized"] is False and r322_blocker["promiseQualified"] is False
assert r322_decision["status"] == "HOLD" and r322_decision["acceptedIds"] == [] and r322_decision["appliedIds"] == []
assert r322_cases["counts"]["targetCases"] == 17 and r322_cases["counts"]["targetEvents"] == 156
assert r322_cases["counts"]["forwardOperations"] == 312 and r322_cases["counts"]["inverseOperations"] == 312
assert sum(1 for row in r322_cases["results"] if row["preservedStatus"] == "DEMONSTRATED") == 16
assert sum(1 for row in r322_cases["results"] if row["preservedStatus"] == "BLOCKED_EVIDENCE") == 1
assert len(r322_questions["dispositions"]) == 8 and len(r322_quals["qualificationIds"]) == 10
next_scope = r320_decision["nextScope"]
assert "Collapse Timeline-only current-authority packet" in next_scope
assert fate_reconciliation_pass["disposition"] == "PASS_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY_RECONCILIATION"
assert fate_reconciliation_pass["scopeLimits"]["identityAccepted"] is False
assert fate_reconciliation_pass["scopeLimits"]["identityApplied"] is False
assert fate_witness_pass["reviewedCommit"] == "477fda34de62295995d2fb779656fcbedb081121"

source_roles = {}
def add(path, role):
    source_roles.setdefault(path, set()).add(role)

for p, role in [
    (QUEUE, "Current Queue481 authority and order"),
    (HANDOFF, "Current Handoff481 consistency"),
    (PENDING_AUDIT, "Current pending identity audit consistency"),
    (CATALOG, "Current public catalog, Collapse Timeline row"),
    (INDEX, "Current authored review index, Collapse Timeline row"),
    (CAND + "CANDIDATE_PACKAGE_MANIFEST.json", "Reviewed candidate package provenance"),
    (CAND + "DIRECTOR_DECISION.json", "Candidate package held decision"),
    (CAND + "SOURCE_BINDINGS.json", "Candidate package source bindings"),
    (CAND + "CASE_DISPOSITIONS.json", "Candidate historical case dispositions"),
    (CAND + "CASE_HASH_BINDINGS.json", "Candidate case byte/hash bindings"),
    (CAND + "COUNTS.json", "Candidate package counts"),
    (CAND + "FUTURE_OBLIGATIONS.json", "Future obligation scope"),
    (CAND + "HOLD_REGISTER.json", "Candidate hold register"),
    (CAND + "ORIGINAL_QUESTIONS.json", "Original review questions"),
    (CAND + "QUESTION_DISPOSITIONS.json", "Candidate question dispositions"),
    (CAND + "QUALIFICATIONS.json", "Candidate qualifications"),
    (CAND + "CURRENT_CONTEXT_191.json", "Historical package context, not current queue authority"),
    (CAND + "procedures/collapse-timeline.json", "Current authored candidate procedure; no acceptance or application"),
    (RETURN322 + "BLOCKER_REASSESSMENT.json", "B05 and B02 retained blocker evidence"),
    (RETURN322 + "CASE_RESULTS.json", "Return322 static case summary"),
    (RETURN322 + "DATA_VALIDATION.json", "Return322 data validation record"),
    (RETURN322 + "DIRECTOR_DECISION.json", "Historical Return322 hold; not current queue authority"),
    (RETURN322 + "FUTURE_OBLIGATION_DISPOSITIONS.json", "Preserved future obligations"),
    (RETURN322 + "INDEPENDENT_SEMANTIC_FAILURE_CHECK.json", "Return322 semantic failure check"),
    (RETURN322 + "INPUT_MEMBER_MANIFEST.json", "Return322 source member manifest"),
    (RETURN322 + "MANIFEST.json", "Return322 manifest"),
    (RETURN322 + "PACKAGE_CHECKS.json", "Return322 package checks"),
    (RETURN322 + "PRIOR_CASE_BINDINGS.json", "Return322 prior case bindings"),
    (RETURN322 + "QUALIFICATIONS.json", "Return322 held qualifications"),
    (RETURN322 + "QUESTION_DISPOSITIONS.json", "Return322 Collapse Timeline questions"),
    (RETURN322 + "SOURCE_BINDING.json", "Return322 source snapshots, historical-only"),
    (RETURN322 + "authority/CURRENT_SPELL_QUEUE_321.json", "Historical Queue321, explicitly superseded"),
    (RETURN322 + "authority/CURRENT_HANDOFF_321.json", "Historical Handoff321, explicitly superseded"),
    (RETURN322 + "procedures/collapse-timeline.json", "Return322 retained Collapse Timeline procedure"),
    (RETURN320 + "DIRECTOR_DECISION.json", "Director-authorized current-authority nextScope"),
    (RETURN320 + "BLOCKER_REASSESSMENT.json", "Fate Rewrite B02/B04 unresolved boundary"),
    (FATE_RECON + "FATE_REWRITE_IDENTITY_RECONCILIATION_01.json", "Completed preceding static reconciliation"),
    (FATE_RECON + "CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_FATE_REWRITE_IDENTITY_01.json", "Director PASS readback; static only"),
    (FATE_WITNESS + "CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_03.json", "Adopted Proposal05 witness component PASS; unsealed"),
]: add(p, role)
for p in case_file_paths: add(p, "One of 17 Return322 Collapse Timeline case records")

bindings = []
for path in sorted(source_roles):
    data = blob(BASE_COMMIT, path)
    bindings.append({
        "path": path,
        "bytes": len(data),
        "sha256": sha(data),
        "gitBlobSha1": blob_sha(BASE_COMMIT, path),
        "roles": sorted(source_roles[path]),
    })

# Historical stale-source note: Return322's whole-file snapshots predate Queue481.
old_catalog_row = next(row for row in r322_source_binding["comparison"]["rows"] if row["path"] == CATALOG)
old_index_row = next(row for row in r322_source_binding["comparison"]["rows"] if row["path"] == INDEX)
assert old_catalog_row["currentSha256"] != sha(blob(BASE_COMMIT, CATALOG))
assert old_index_row["currentSha256"] != sha(blob(BASE_COMMIT, INDEX))

packet = {
    "schemaVersion": 1,
    "id": "COLLAPSE-TIMELINE-CURRENT-AUTHORITY-REVIEW-01",
    "classification": "READ_ONLY_CURRENT_AUTHORITY_STATIC_RECONCILIATION",
    "recordedAtUtc": "2026-11-03",
    "baseCommit": BASE_COMMIT,
    "scope": {
        "spellId": "collapse-timeline",
        "reviewOnly": True,
        "purpose": "Reconcile current Queue481, catalog/index, retained Collapse Timeline procedure and Return322 evidence after the preceding Fate Rewrite reconciliation.",
        "directorAuthorizedNextScope": next_scope,
        "directorAuthorizationSource": {"path": RETURN320 + "DIRECTOR_DECISION.json", "pointer": "/nextScope"},
        "noNewPremisesOrWitnessConstruction": True,
    },
    "requestedDirectorDisposition": "PASS_STATIC_CURRENT_AUTHORITY_RECONCILIATION_ONLY, REVISE with exact path/pointer/hash, or HOLD with the precise unresolved source or authority gap.",
    "currentAuthority": {
        "queuePath": QUEUE,
        "queueSha256": sha(blob(BASE_COMMIT, QUEUE)),
        "handoffPath": HANDOFF,
        "handoffSha256": sha(blob(BASE_COMMIT, HANDOFF)),
        "pendingAuditPath": PENDING_AUDIT,
        "pendingAuditSha256": sha(blob(BASE_COMMIT, PENDING_AUDIT)),
        "counts": auth,
        "remainingPendingIds": queue["remainingPendingIds"],
        "continuingPriorityOrder": queue["continuingPriorityOrder"],
        "nextIdentity": queue["nextIdentity"],
        "acceptedUnapplied": queue["acceptedUnapplied"],
        "runtimeExecuted": queue["runtimeExecuted"],
        "runtimeSelectionEnabled": queue["runtimeSelectionEnabled"],
        "collapseTimelineQueuePosition": queue["continuingPriorityOrder"].index("collapse-timeline") + 1,
        "queueDisposition": "No queue mutation or identity acceptance/application is requested. Queue481 remains authoritative; Return322/Queue321 snapshots are historical only.",
    },
    "currentCatalogAndIndex": {
        "catalog": {"path": CATALOG, "bytes": len(blob(BASE_COMMIT, CATALOG)), "sha256": sha(blob(BASE_COMMIT, CATALOG)), "gitBlobSha1": blob_sha(BASE_COMMIT, CATALOG), "pointer": catptr, "row": catrow},
        "authoredReviewIndex": {"path": INDEX, "bytes": len(blob(BASE_COMMIT, INDEX)), "sha256": sha(blob(BASE_COMMIT, INDEX)), "gitBlobSha1": blob_sha(BASE_COMMIT, INDEX), "pointer": idxptr, "row": idxrow},
        "sourceAnchor": {
            "commit": SOURCE_ANCHOR,
            "catalogFileSha256": sha(blob(SOURCE_ANCHOR, CATALOG)),
            "indexFileSha256": sha(blob(SOURCE_ANCHOR, INDEX)),
            "targetCatalogRowEqual": catrow == anchor_catrow,
            "targetIndexRowEqual": idxrow == anchor_idxrow,
        },
        "candidateProcedureSnapshotsEqualCurrentRows": {
            "catalog": procedure["currentCatalogSourceAndAccessUnchanged"] == catrow,
            "authoredReviewIndex": procedure["currentIndexEntryUnchanged"] == idxrow,
        },
        "interpretation": "The target catalog/index rows match their package anchor, but Return322's whole-file catalog and index hashes are stale. Queue481's bound whole-file snapshots and exact rows at 6287600 are used for current authority.",
    },
    "collapseTimelineCurrentStatus": {
        "catalogStatus": catrow["status"],
        "authoredStatus": idxrow["authoredStatus"],
        "operationalDefinition": catrow["operational"],
        "blockerIds": procedure["blockerIds"],
        "dependencyIds": r322_blocker["dependencyIds"],
        "accepted": procedure["accepted"],
        "applied": procedure["applied"],
        "sourceSummary": catrow["source"]["original"]["description"],
        "access": catrow["classAccess"],
    },
    "retainedReturn322Evidence": {
        "historicalAuthority": {"before": r322_decision["authorityBefore"], "after": r322_decision["authorityAfter"], "nextIdentityThen": r322_decision.get("nextIdentity"), "note": "Historical Return322 dispositions only; superseded by Queue481."},
        "caseCounts": r322_cases["counts"],
        "caseResults": r322_cases["results"],
        "caseFiles": case_file_paths,
        "blockerB05": r322_blocker,
        "questions": {"count": r322_questions["count"], "dispositions": r322_questions["dispositions"]},
        "qualifications": r322_quals,
        "sourceSnapshotDrift": {
            "return322CatalogSnapshotSha256": old_catalog_row["currentSha256"],
            "queue481CatalogSha256": queue["currentCatalogBinding"]["sha256"],
            "return322AuthoredIndexSnapshotSha256": old_index_row["currentSha256"],
            "queue481AuthoredIndexSha256": queue["currentIndexBinding"]["sha256"],
            "return322SnapshotsAreCurrent": False,
        },
    },
    "precedingFateRewriteContext": {
        "identityReconciliationPath": FATE_RECON + "FATE_REWRITE_IDENTITY_RECONCILIATION_01.json",
        "identityReconciliationSha256": sha(blob(BASE_COMMIT, FATE_RECON + "FATE_REWRITE_IDENTITY_RECONCILIATION_01.json")),
        "directorDisposition": fate_reconciliation_pass["disposition"],
        "scopeLimits": fate_reconciliation_pass["scopeLimits"],
        "proposal05WitnessDisposition": fate_witness_pass["disposition"],
        "proposal05WitnessesRemainUnsealed": True,
        "B02AndB04RemainOpen": True,
    },
    "openEvidenceRequirement": {
        "B05Status": r322_blocker["status"],
        "dependencyIds": r322_blocker["dependencyIds"],
        "minimumMissingWitness": r322_blocker["minimumMissingWitness"],
        "actualConditionalRecordMeaning": r322_blocker["actualConditionalRecord"]["meaning"],
        "guaranteeDependency": r322_blocker["guaranteeDependency"],
        "newMechanismAuthorized": r322_blocker["newMechanismAuthorized"],
        "promiseQualified": r322_blocker["promiseQualified"],
        "waiver": r322_blocker["waiver"],
    },
    "nonAuthorization": {
        "identityAcceptance": False,
        "identityApplication": False,
        "blockerClosure": False,
        "witnessConstruction": False,
        "witnessSeal": False,
        "canonOrNativeRuleChange": False,
        "runtimeOrCampaignChange": False,
        "queueChange": False,
        "promiseQualificationOrWaiver": False,
    },
    "sourceBindings": bindings,
}

packet_path = write_json("COLLAPSE_TIMELINE_CURRENT_AUTHORITY_REVIEW_01.json", packet)
packet_bytes = packet_path.read_bytes()
packet_hash = sha(packet_bytes)
packet_rel = AUDIT + "collapse_timeline_current_authority_review_2026-11-03/"
request = f'''# Director review request — Collapse Timeline current authority\n\nPlease review the read-only packet bound to main commit `{BASE_COMMIT}`. Return `PASS_STATIC_CURRENT_AUTHORITY_RECONCILIATION_ONLY`, `REVISE` with exact path/pointer/hash, or `HOLD` with the precise unresolved source or authority gap.\n\n- Packet: https://github.com/BordelonDevOps/DecenniumDescent/blob/main/{packet_rel}COLLAPSE_TIMELINE_CURRENT_AUTHORITY_REVIEW_01.json\n- Packet SHA-256: `{packet_hash}`\n- Manifest: https://github.com/BordelonDevOps/DecenniumDescent/blob/main/{packet_rel}PACKET_MANIFEST_COLLAPSE_TIMELINE_CURRENT_AUTHORITY_01.json\n\nThe packet reconciles Queue481 (836 applied / 12 pending / 0 accepted-unapplied; Fate Rewrite remains first and Collapse Timeline second), current catalog/index bindings at `{BASE_COMMIT}`, the retained Return322 B05 evidence, and the preceding Fate Rewrite static reconciliation. Return322's Queue321 and whole-file catalog/index snapshots are labeled historical; they do not supersede Queue481. The target catalog/index rows are byte-source-derived and match the package anchor, but the spell remains blocked and its operational field remains null.\n\nPlease verify current source/version bindings, the priority/status crosswalk, and whether the packet accurately carries the unresolved B05/B02 evidence and qualifications. Identify any remaining read-only current-authority reconciliation that falls within the authorized scope. Do not construct witnesses or propose new premises. No seal, blocker closure, identity acceptance/application, canon/native-rule, runtime, campaign or queue change is requested.\n'''
req_path = OUT / "DIRECTOR_REVIEW_REQUEST_COLLAPSE_TIMELINE_CURRENT_AUTHORITY_01.md"
req_path.write_text(request, encoding="utf-8")

manifest_entries = []
for p in [packet_path, req_path, pathlib.Path(__file__)]:
    data = p.read_bytes()
    manifest_entries.append({"path": p.name if p.parent == OUT else "tools/" + p.name, "bytes": len(data), "sha256": sha(data)})
manifest = {
    "schemaVersion": 1,
    "id": "PACKET-MANIFEST-COLLAPSE-TIMELINE-CURRENT-AUTHORITY-01",
    "baseCommit": BASE_COMMIT,
    "packetSha256": packet_hash,
    "entries": manifest_entries,
    "sourceBindingCount": len(bindings),
    "caseFileCount": len(case_file_paths),
    "scope": "Read-only current-authority reconciliation only; no new witness premises.",
}
write_json("PACKET_MANIFEST_COLLAPSE_TIMELINE_CURRENT_AUTHORITY_01.json", manifest)

print(json.dumps({
    "packet": str(packet_path),
    "packetSha256": packet_hash,
    "sourceBindings": len(bindings),
    "caseFiles": len(case_file_paths),
    "queue": auth,
    "catalogRowPointer": catptr,
    "indexRowPointer": idxptr,
    "anchorRowsEqual": catrow == anchor_catrow and idxrow == anchor_idxrow,
    "Return322SnapshotsCurrent": False,
    "B05": r322_blocker["status"],
    "newMechanismAuthorized": r322_blocker["newMechanismAuthorized"],
    "request": str(req_path),
}, indent=2))
