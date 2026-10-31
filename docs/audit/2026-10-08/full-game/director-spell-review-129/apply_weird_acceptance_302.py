from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import zipfile
import zlib


ROOT = pathlib.Path.cwd()
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
DELTA_DIR = A / "rank9_weird_conditional_interface_delta_301"
DELTA = DELTA_DIR / "DD_Rank9_Weird_ConditionalInterface_Completion_301.zip"
FRESH_AUDIT = DELTA_DIR / "FRESH_REPLAY_AUDIT_301.json"
INDEPENDENT_AUDIT = A / "WEIRD_COMPLETION_INDEPENDENT_AUDIT_301.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
Q0 = A / "CURRENT_SPELL_QUEUE_299.json"
H0 = A / "CURRENT_HANDOFF_299.json"
P0 = A / "CURRENT27_PENDING_IDENTITY_AUDIT_299.json"
ID = "weird"
NAME = "Weird"
BLOCKER = "PF182-B02"
REVISION = "PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01"
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
EXPECTED_DELTA_SHA = "3e9a9213741d4554132a2b7df6a0c0bbe236e41c59fcaab1b71eed538e67f9b5"
EXPECTED_AUDIT_SHA = "58830abc3616cbe1070d0c5805ea525cb68cd36a2a0ffee8189b827bb1044461"
BEFORE = {"reviewedApplied": 821, "pending": 27, "acceptedUnapplied": 1, "completeStandaloneProcedures": 545, "scopedInterfaces": 173}
AFTER = {"reviewedApplied": 822, "pending": 26, "acceptedUnapplied": 0, "completeStandaloneProcedures": 546, "scopedInterfaces": 173}
INDEX_BEFORE = {"reviewed": 821, "pending": 27}
NEXT = "final-word"
NEXT_BLOCKER = "DR217-B01"
QUALIFICATIONS = [
    "Acceptance is limited to Weird / PF182-B02 authored-procedure review under PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01.",
    "PF181-H05 and every other existing source qualification remain. A real gameplay extra-turn provider, lawful acquisition, consent, and eligible actor remain unestablished.",
    "The conditional provider tests are static authored-review evidence only. They grant no actual provider, turn, gameplay permission, or ability to act while Unconscious.",
    "The historical missing-provider case is preserved byte-exact as history; the authored-review obligation is satisfied only by the accepted WCI-01 through WCI-04 replacement tests.",
    "Native spell catalog stays byte-exact and blocked-pending-operational-review. Runtime selection and all downstream gates remain closed.",
]
DIRECTOR_TEXT = (
    "ACCEPT — weird / PF182-B02, authored-procedure review only. accepted=true, applied=false. No remaining correction within the submitted scope. "
    "WCI-01 through WCI-04 pass under PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01. Independent verification confirmed 35 members / 34 payload bindings with exact hashes and CRCs; 18 preserved cases / 1,054 events / 2,108 forward and 2,108 inverse operations with complete restoration; both Unconscious-policy forks preserve the exact recipient baseline and deny prohibited activation without payment; waking at 14.2, expiry at 60.21, ordinary schedules and attached-phase exposure remain unchanged. "
    "The historical missing-provider case remains preserved as history; its authored-review obligation is satisfied by the authorized replacement tests. PF181-H05 and every other qualification remain. This acceptance establishes no actual provider, acquisition, gameplay turn, consent, or permission to act while Unconscious. All downstream gates remain closed. "
    "Acceptance binds the 13,644,488-byte archive with SHA-256 3e9a9213741d4554132a2b7df6a0c0bbe236e41c59fcaab1b71eed538e67f9b5. Nothing was applied at decision. Canonical snapshot: 821 applied / 27 pending rows, Weird accepted-unapplied, 26 identities held. After application: 822 applied / 26 pending / 0 accepted-unapplied; 546 procedures / 173 interfaces. Next: final-word / DR217-B01. The remaining 26 order is retained in the Director response; no other identity is adjudicated or accepted."
)
PKG_REL = pathlib.Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9weird_reviewed_302")
PKG = ROOT / PKG_REL
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/WEIRD_REVIEWED_302.md"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bind(path: pathlib.Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data), "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"}


def read(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def filter_rows(rows: list[dict]) -> list[dict]:
    kept = []
    for old in rows:
        row = copy.deepcopy(old)
        key = next((k for k in ("pendingIds", "identities", "spellIds") if isinstance(row.get(k), list)), None)
        if key:
            row[key] = [item for item in row[key] if item != ID]
            if not row[key]:
                continue
            if "pendingCount" in row:
                row["pendingCount"] = len(row[key])
        if isinstance(row.get("blockersByIdentity"), dict):
            row["blockersByIdentity"].pop(ID, None)
        kept.append(row)
    return kept


def main() -> None:
    assert not PKG.exists() and not MANUSCRIPT.exists(), "Refusing to overwrite Weird application outputs."
    for name in (
        "WEIRD_DIRECTOR_DECISION_302.json", "WEIRD_ACCEPTANCE_302.json", "WEIRD_APPLICATION_302.json",
        "CURRENT26_PENDING_IDENTITY_AUDIT_302.json", "CURRENT_SPELL_QUEUE_302.json", "CURRENT_HANDOFF_302.json",
    ):
        assert not (A / name).exists(), f"Refusing to overwrite {name}"
    assert sha(DELTA.read_bytes()) == EXPECTED_DELTA_SHA and DELTA.stat().st_size == 13_644_488
    assert sha(INDEPENDENT_AUDIT.read_bytes()) == EXPECTED_AUDIT_SHA
    independent = read(INDEPENDENT_AUDIT)
    assert independent["status"] == "PASS" and independent["auditedArchive"]["sha256"] == EXPECTED_DELTA_SHA
    assert all(row["passed"] for row in independent["checks"])
    assert independent["summary"]["wci03Branches"] == 2 and independent["summary"]["wci03ScheduleEvents"] == 83
    assert independent["summary"]["authority"].startswith("821 applied / 27 pending") and independent["summary"]["canonicalIndexChanged"] is False

    with zipfile.ZipFile(DELTA) as z:
        assert z.testzip() is None and len(z.namelist()) == 35
        manifest_raw = z.read("DELIVERY_MANIFEST_301.json")
        manifest = json.loads(manifest_raw)
        files = {row["path"]: row for row in manifest["files"]}
        assert len(files) == 34
        member_raw = {}
        for name, row in files.items():
            raw = z.read(name)
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]
            member_raw[name] = raw
        source_proc_raw = z.read("preserved/procedures/weird.json")
        source_proc = json.loads(source_proc_raw)
        assert source_proc["spellId"] == ID and source_proc["accepted"] is False and source_proc["applied"] is False
        assert source_proc["nativeCardAndAccessUnchanged"]["id"] == ID
        revision = json.loads(z.read("PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01.json"))
        assert revision["id"] == REVISION
        wci1 = json.loads(z.read("WCI-01_PROVIDERLESS_GAMEPLAY_ACTIVATION_DENIAL_301.json"))
        wci2 = json.loads(z.read("WCI-02_CONDITIONAL_START_END_LIFECYCLE_TRACE_301.json"))
        wci3 = json.loads(z.read("WCI-03_UNCONSCIOUS_RECIPIENT_BOUNDARY_TRACE_301.json"))
        wci4 = json.loads(z.read("WCI-04_ATTACHED_PHASE_DEDUPLICATION_TRACE_301.json"))
        fresh = json.loads(z.read("FRESH_REPLAY_AUDIT_301.json"))
        assert fresh["caseCount"] == 18 and fresh["eventCount"] == 1054
        assert fresh["forwardEventCount"] == fresh["inverseEventCount"] == 1054
        assert fresh["allInitialStatesRestored"] and fresh["sourceCasesByteExactToPreservedReturn234"]
        assert len(wci3["branches"]) == 2
        assert "14.2" in json.dumps(wci3) and "60.21" in json.dumps(wci3)
        assert wci1 and wci2 and wci4
        evidence_names = [
            "WCI-01_PROVIDERLESS_GAMEPLAY_ACTIVATION_DENIAL_301.json",
            "WCI-02_CONDITIONAL_START_END_LIFECYCLE_TRACE_301.json",
            "WCI-03_UNCONSCIOUS_RECIPIENT_BOUNDARY_TRACE_301.json",
            "WCI-04_ATTACHED_PHASE_DEDUPLICATION_TRACE_301.json",
            "FRESH_REPLAY_AUDIT_301.json",
            "SOURCE_MAP_301.json",
            "PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01.json",
            "WCI03_PRESERVED_BASELINE_CLARIFICATION_301.json",
        ]
        evidence_raw = {name: z.read(name) for name in evidence_names}
        current_authority = json.loads(z.read("CURRENT_AUTHORITY_301.json"))
        assert current_authority["authority"] == {
            "reviewedApplied": 821, "pending": 27, "acceptedUnapplied": 0,
            "completeStandaloneProcedures": 545, "scopedInterfaces": 173,
        }
        authority_index = z.read("authority/current/authored_review_index.json") if "authority/current/authored_review_index.json" in z.namelist() else None
        # The packet's authority snapshot is nested as an exact prior archive; the live index is also checked below.

    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert branch == "main"
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    index_raw = INDEX.read_bytes()
    catalog_raw = CATALOG.read_bytes()
    index0, catalog0, q0, h0, p0 = read(INDEX), read(CATALOG), read(Q0), read(H0), read(P0)
    assert index0["authoredCounts"] == INDEX_BEFORE
    assert index0["representationCounts"]["completeReviewedStandaloneProcedures"] == 545
    assert q0["currentAuthority"] == h0["currentAuthority"] == p0["authority"] == {
        "reviewedApplied": 821, "pending": 27, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 545, "scopedInterfaces": 173,
    }
    assert p0["pendingCount"] == 27 and p0["indexBinding"]["sha256"] == sha(index_raw)
    entry0 = copy.deepcopy(next(row for row in index0["entries"] if row["id"] == ID))
    assert entry0["authoredStatus"] == "pending-authored-procedure"
    assert entry0["sourceStatus"] == "blocked-pending-operational-review"
    live0 = {row["id"] for row in index0["entries"] if row.get("authoredStatus") == "pending-authored-procedure"}
    assert len(live0) == 27 and ID in live0
    native = next(row for row in catalog0["spells"] if row["id"] == ID)
    assert native["operational"] is None and native["status"] == "blocked-pending-operational-review"

    delta_ref = bind(DELTA)
    source_proc_ref = {"archive": delta_ref, "member": "preserved/procedures/weird.json", "bytes": len(source_proc_raw), "sha256": sha(source_proc_raw)}
    decision_id = "RANK9-WEIRD-PF182-B02-DIRECTOR-DECISION-302"
    acceptance_id = "RANK9-WEIRD-PF182-B02-ACCEPTANCE-302"
    application_id = "RANK9-WEIRD-PF182-B02-APPLICATION-302"
    decision_path = A / "WEIRD_DIRECTOR_DECISION_302.json"
    decision = {
        "id": decision_id, "recordedAtUtc": stamp, "decision": "EXACT_ACCEPT_WEIRD_AUTHORED_PROCEDURE_ONLY",
        "identity": ID, "blocker": BLOCKER, "accepted": True, "appliedAtDecision": False,
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": URL},
        "exactDirectorResponse": DIRECTOR_TEXT,
        "acceptedRevision": {"id": REVISION, "scope": "Weird / PF182-B02 authored-procedure review only", "acceptedArchive": delta_ref, "independentAudit": bind(INDEPENDENT_AUDIT)},
        "acceptedTests": ["WCI-01", "WCI-02", "WCI-03", "WCI-04"],
        "preservedReplay": {"cases": 18, "events": 1054, "forwardOperations": 2108, "inverseOperations": 2108, "allInitialStatesRestored": True},
        "retainedQualifications": QUALIFICATIONS,
        "noOtherIdentityAcceptedOrApplied": True, "nativeCatalogChanged": False, "runtimeSelectionEnabled": False,
        "countsBeforeApplication": BEFORE, "forecastAfterApplication": AFTER,
        "nextPriority": ["final-word / DR217-B01"],
    }
    write(decision_path, decision)
    decision_ref = bind(decision_path)
    acceptance_path = A / "WEIRD_ACCEPTANCE_302.json"
    acceptance = {
        "id": acceptance_id, "recordedAtUtc": stamp, "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED",
        "acceptedIds": [ID], "appliedIds": [], "closedBlockerIds": [BLOCKER], "directorDecision": decision_ref,
        "acceptedRevision": {"id": REVISION, "archive": delta_ref, "independentAudit": bind(INDEPENDENT_AUDIT)},
        "countsBeforeApplication": BEFORE, "retainedQualifications": QUALIFICATIONS,
    }
    write(acceptance_path, acceptance)
    acceptance_ref = bind(acceptance_path)
    return_path = A / "WEIRD_RETURN301_RECEIPT.json"
    return_receipt = {
        "id": "RANK9-WEIRD-DIRECTOR-RETURN301-RECEIPT", "recordedAtUtc": stamp,
        "status": "EXACT_ACCEPT_PF182_B02_WEIRD_ONLY", "acceptedIds": [ID], "appliedIds": [],
        "heldIds": [], "closedBlockerIds": [BLOCKER], "directorDecision": decision_ref,
        "acceptance": acceptance_ref, "acceptedArchive": delta_ref,
        "sourceResponse": DIRECTOR_TEXT, "retainedQualifications": QUALIFICATIONS,
        "nextPriority": ["final-word / DR217-B01"],
    }
    write(return_path, return_receipt)
    return_ref = bind(return_path)

    PKG.mkdir(parents=True)
    (PKG / "evidence").mkdir()
    for member in evidence_names:
        (PKG / "evidence" / member).write_bytes(evidence_raw[member])
    source_procedure = copy.deepcopy(source_proc["localProcedure"])
    procedure_record = {
        "id": "PF182-STATIC-WEIRD-302", "spellId": ID,
        "status": "director-accepted authored-procedure review; applied to authored review index; runtime disabled",
        "accepted": True, "applied": True, "scope": "Weird / PF182-B02 only under PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01",
        "acceptedRevision": REVISION, "directorDecisionId": decision_id,
        "sourceProcedureArchiveMember": source_proc_ref, "sourceProcedureBytesPreserved": True,
        "localProcedure": source_procedure, "sourceProcedureRecord": source_proc,
        "acceptedReviewEvidence": {
            "WCI-01": "Providerless gameplay activation is denied before payment or state mutation; the unrelated lawful Weird cast is not blocked.",
            "WCI-02": "Conditional START/END lifecycle preserves the original schedule, concentration, saves, costs, and 60.21 expiry without granting an extra turn.",
            "WCI-03": "Both external-policy forks preserve the exact Unconscious recipient baseline; denial is precommit, and the permitted branch remains hypothetical with no gameplay grant.",
            "WCI-04": "Attached-phase schedule remains unchanged and family/recipient/round exposure keys deduplicate correctly.",
        },
        "retainedQualificationIds": ["PF181-H05"], "retainedQualifications": QUALIFICATIONS,
        "closedBlockerIds": [BLOCKER], "runtimeSelectionEnabled": False,
    }
    write(PKG / "PROCEDURE_RECORD.json", procedure_record)
    procedure_ref = bind(PKG / "PROCEDURE_RECORD.json")
    fresh_replay = read(PKG / "evidence/FRESH_REPLAY_AUDIT_301.json")
    coverage = {
        "id": "WEIRD-ACCEPTED-CASE-COVERAGE-302", "sourceArchive": delta_ref,
        "sourceProcedure": source_proc_ref, "historicalCaseCount": 18, "historicalEventCount": 1054,
        "historicalForwardOperations": 2108, "historicalInverseOperations": 2108,
        "preservedCases": fresh_replay["results"],
        "conditionalTraceBindings": [bind(PKG / "evidence" / name) for name in evidence_names[:4]],
        "conditionalTraceEvents": {"WCI-02": 83, "WCI-03_shared_schedule": 83, "WCI-04": 17},
        "sourceCaseByteExact": True, "runtimeOrCampaignEvidence": False,
        "scope": "Accepted authored-procedure review under the Weird-only provider-obligation revision; actual provider and gameplay requirements remain.",
    }
    write(PKG / "CASE_COVERAGE.json", coverage)
    coverage_ref = bind(PKG / "CASE_COVERAGE.json")
    evidence_bindings = {
        "id": "WEIRD-ACCEPTED-EVIDENCE-BINDINGS-302", "acceptedArchive": delta_ref,
        "acceptedRevision": {"id": REVISION, "binding": bind(PKG / "evidence/PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01.json")},
        "directorDecision": decision_ref, "acceptance": acceptance_ref, "directorReturnReceipt": return_ref,
        "independentAudit": bind(INDEPENDENT_AUDIT), "sourceProcedure": source_proc_ref,
        "caseCoverage": coverage_ref, "evidenceFiles": [bind(PKG / "evidence" / name) for name in evidence_names],
        "currentAuthorityBeforeApplication": {"index": bind(INDEX, index_raw), "queue": bind(Q0), "handoff": bind(H0), "pendingAudit": bind(P0)},
        "authority": BEFORE, "baseCommit": head, "acceptedReviewRevision": REVISION,
        "retainedQualifications": QUALIFICATIONS, "nativeCatalogChanged": False, "runtimeSelectionEnabled": False,
    }
    write(PKG / "EVIDENCE_BINDINGS.json", evidence_bindings)
    evidence_ref = bind(PKG / "EVIDENCE_BINDINGS.json")
    model = {
        "schemaVersion": 1, "moduleId": "rank9weird-reviewed-302",
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
        "scope": "Weird / PF182-B02 only; accepted authored-procedure review under PF301. Actual gameplay provider obligations remain.",
        "acceptedIds": [ID], "excludedPendingIds": sorted(live0 - {ID}),
        "unresolvedQualifications": {ID: QUALIFICATIONS},
        "sharedRequirements": {"scope": "No shared rule changes; native catalog unchanged; runtime selection disabled.", "runtimeSelectionEnabled": False},
        "spells": [{
            "id": ID, "name": NAME, "position": 0,
            "procedure": {"id": procedure_record["id"], "spellId": ID, "status": procedure_record["status"],
                          "accepted": True, "applied": True, "procedureContent": json.dumps(source_procedure, ensure_ascii=False, sort_keys=True),
                          "procedureRecordFile": "PROCEDURE_RECORD.json", "acceptedRevision": REVISION,
                          "retainedQualifications": QUALIFICATIONS, "closedBlockerIds": [BLOCKER],
                          "retainedHoldIds": ["PF181-H05"], "caseCoverageFile": "CASE_COVERAGE.json",
                          "evidenceBindingsFile": "EVIDENCE_BINDINGS.json", "directorDecisionId": decision_id},
            "directorProcedureRecord": procedure_record, "previousProcedureRecord": source_proc,
            "nativeCardUnchanged": source_proc["nativeCardAndAccessUnchanged"],
            "caseIds": [result["sourceMember"] for result in fresh_replay["results"]],
            "retainedHoldIds": ["PF181-H05"], "runtimeSelectionEnabled": False,
        }],
        "sourceProcedureArchive": delta_ref, "directorDecision": decision_ref,
        "acceptanceReceipt": acceptance_ref, "directorReturnReceipt": return_ref,
        "caseCoverage": coverage_ref, "evidenceBindings": evidence_ref,
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "implementationApproved": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
        "domainClosure": False, "releaseApproved": False,
    }
    write(PKG / "MODEL.json", model)
    model_ref = bind(PKG / "MODEL.json")
    manuscript = (
        "# Weird — accepted static authored procedure 302\n\n"
        "Director accepted Weird / PF182-B02 for authored-procedure review under PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01. The Weird-only obligation is satisfied by WCI-01 through WCI-04; this application does not establish an actual extra-turn provider, lawful acquisition, consent, or permission to act while Unconscious. PF181-H05 and every other qualification remain. The original source procedure and 18 historical cases remain preserved.\n\n"
        "The providerless activation test denies before payment or state mutation. Conditional lifecycle tests preserve the actual schedule, cost, concentration, regular saves, and 60.21 expiry. Both Unconscious-policy forks preserve their exact recipient baseline; one denies prohibited activation, while the other treats external permission solely as a conditional test input. The attached-phase tests preserve family/recipient/round deduplication. These are authored-review traces, not runtime or campaign evidence.\n\n"
        "The native catalog remains byte-exact and blocked-pending-operational-review. Runtime selection and downstream gates remain disabled.\n\n"
        "## Retained qualifications\n\n" + "\n".join("- " + item for item in QUALIFICATIONS) + "\n"
    )
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")
    manuscript_ref = bind(MANUSCRIPT)
    manifest_path = PKG / "CANDIDATE_PACKAGE_MANIFEST.json"
    pkg_manifest = {"id": "WEIRD-PACKAGE-MANIFEST-302", "recordedAtUtc": stamp, "directorDecision": decision_ref, "acceptedArchive": delta_ref, "files": []}
    for path in sorted(item for item in PKG.rglob("*") if item.is_file() and item != manifest_path):
        pkg_manifest["files"].append({"path": (PKG_REL / path.relative_to(PKG)).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path.read_bytes())})
    write(manifest_path, pkg_manifest)
    pkg_manifest_ref = bind(manifest_path)

    index1 = copy.deepcopy(index0)
    entry1 = copy.deepcopy(entry0)
    entry1.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank9weird_reviewed_302/MODEL.json",
        "procedurePointer": "/spells/0/procedure", "wholeCardPointer": "/spells/0",
        "sourceStatus": entry0["sourceStatus"], "wholeCardIdField": "id",
        "sourceCatalogWholeCardPointer": entry0["wholeCardPointer"],
        "procedureTextPointer": "/spells/0/procedure/procedureContent",
        "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
        "sharedRulesPointer": "/sharedRequirements", "spellLocalRequirementsPointer": "/spells/0/procedure",
        "manuscript": "../../../docs/spells/candidates/WEIRD_REVIEWED_302.md",
        "reviewId": acceptance_id, "runtimeSelectionEnabled": False,
        "historicalCandidateLabelsPreserved": True, "completeEvidenceRoot": PKG_REL.as_posix(),
        "completeEnvelopeBinding": model_ref, "caseEvidenceBindings": coverage_ref,
        "sourceArchiveBinding": delta_ref, "candidatePackageManifestBinding": pkg_manifest_ref,
        "procedureSourceBinding": decision_ref, "authoredAcceptanceReceipt": acceptance_ref,
        "authoredApplicationReceipt": (A / "WEIRD_APPLICATION_302.json").relative_to(ROOT).as_posix(),
        "directorReturnReceipt": return_ref, "accepted": True, "applied": True,
        "closedBlockerIds": [BLOCKER], "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": ["PF181-H05"], "acceptedReviewRevision": REVISION,
    })
    target_i = next(i for i, row in enumerate(index1["entries"]) if row["id"] == ID)
    index1["entries"][target_i] = entry1
    assert not any(ID in row.get("acceptedIds", []) for row in index1["additionalStandaloneEnvelopes"])
    envelope = {
        "file": "../spell_candidates/rank9weird_reviewed_302/MODEL.json", "binding": model_ref,
        "reviewId": acceptance_id, "acceptedIds": [ID], "unacceptedIds": [],
        "excludedPendingIds": sorted(live0 - {ID}), "authority": acceptance_ref,
        "applicationReceipt": (A / "WEIRD_APPLICATION_302.json").relative_to(ROOT).as_posix(),
        "directorDecision": decision_ref, "sourceArchive": delta_ref, "caseCoverageBinding": coverage_ref,
        "candidatePackageManifestBinding": pkg_manifest_ref,
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
    }
    index1["additionalStandaloneEnvelopes"].append(envelope)
    index1["authoredCounts"] = {"reviewed": 822, "pending": 26}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"] = 546
    live1 = {row["id"] for row in index1["entries"] if row.get("authoredStatus") == "pending-authored-procedure"}
    assert live1 == live0 - {ID} and len(live1) == 26 and NEXT in live1
    backup = A / "authored_review_index.before_weird_302.json"
    assert not backup.exists()
    backup.write_bytes(index_raw)
    write(INDEX, index1)
    index_core_ref = bind(INDEX)
    application_path = A / "WEIRD_APPLICATION_302.json"
    application = {
        "id": application_id, "recordedAtUtc": stamp, "status": "APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE",
        "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER],
        "directorDecision": decision_ref, "acceptance": acceptance_ref, "directorReturnReceipt": return_ref,
        "acceptedArchive": delta_ref, "candidateEnvelope": model_ref, "candidatePackageManifest": pkg_manifest_ref,
        "caseCoverage": coverage_ref, "evidenceBindings": evidence_ref, "manuscript": manuscript_ref,
        "indexBefore": bind(backup, index_raw), "indexAfterCoreUpdate": index_core_ref,
        "countsBefore": BEFORE, "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": 545, "after": 546}, "scopedInterfaces": 173,
        "catalogByteExact": CATALOG.read_bytes() == catalog_raw, "sourceStatusPreservedAsBlocked": True,
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "implementationApproved": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
        "domainClosure": False, "releaseApproved": False, "retainedQualifications": QUALIFICATIONS,
    }
    write(application_path, application)
    application_ref = bind(application_path)
    entry1["authoredApplicationReceipt"] = application_ref
    index1["entries"][target_i] = entry1
    index1["additionalStandaloneEnvelopes"][-1]["applicationReceipt"] = application_ref
    write(INDEX, index1)
    index_ref = bind(INDEX)

    operations_path = A / "WEIRD_INDEX_OPERATIONS_302.json"
    operations = {
        "id": "WEIRD-INDEX-OPERATIONS-302", "recordedAtUtc": stamp,
        "before": bind(backup, index_raw), "after": index_ref,
        "operations": [
            {"op": "update-entry", "id": ID, "before": entry0, "after": entry1},
            {"op": "append-standalone-envelope", "acceptedIds": [ID]},
            {"op": "update-authored-counts", "before": INDEX_BEFORE, "after": {"reviewed": 822, "pending": 26}},
            {"op": "increment-complete-procedure-count", "before": 545, "after": 546},
        ],
        "inverse": [
            {"op": "restore-entry", "id": ID, "value": entry0},
            {"op": "remove-appended-standalone-envelope", "acceptedIds": [ID]},
            {"op": "restore-authored-counts", "value": INDEX_BEFORE},
            {"op": "restore-complete-procedure-count", "value": 545},
            {"op": "restore-byte-exact-index-from-backup", "backup": bind(backup, index_raw)},
        ],
        "catalogByteExact": CATALOG.read_bytes() == catalog_raw, "sourceStatusPreservedAsBlocked": True,
        "runtimeSelectionEnabled": False, "inverseRestoresExactIndex": backup.read_bytes() == index_raw,
    }
    write(operations_path, operations)

    final_order = [x for x in q0.get("recommendedClosurePriority", []) if x not in {ID}]
    next_row = {
        "group": "rank9-death-recovery7", "pendingIds": [NEXT], "pendingCount": 1,
        "status": "DIRECTOR_NEXT_IDENTITY_AFTER_WEIRD_302", "freshPacketRequiredForCurrentAuthority": True,
        "blockerByIdentity": {NEXT: NEXT_BLOCKER},
        "directorRequirement": "Final Word / DR217-B01 is next. Refresh with Director for its current packet scope, exact actor/victim bindings, and closure tests before submission.",
    }
    pending1 = copy.deepcopy(p0)
    pending1.update({
        "id": "CURRENT26_PENDING_IDENTITY_AUDIT_302", "recordedAtUtc": stamp,
        "status": "PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_WEIRD_APPLICATION_302",
        "authority": AFTER, "indexBinding": index_ref, "catalogBinding": bind(CATALOG, catalog_raw),
        "pendingCount": 26, "pendingIds": sorted(live1), "groups": filter_rows(p0.get("groups", [])),
        "acceptedIds": sorted(set(p0.get("acceptedIds", [])) | {ID}),
        "appliedIds": sorted(set(p0.get("appliedIds", [])) | {ID}),
        "heldIds": sorted(set(p0.get("heldIds", [])) - {ID}),
        "applicationReceipt": application_ref, "acceptanceReceipt": acceptance_ref, "directorDecision": decision_ref,
        "lastDirectorReturn": {"decisionId": decision_id, "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [], "closedBlockerIds": [BLOCKER], "identity": ID, "archive": delta_ref},
        "lastReviewedBatch": {"return": 301, "group": "rank9-psychic-fear7", "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [], "blockerIds": {ID: [BLOCKER]}, "authorityBefore": {k: v for k, v in BEFORE.items()}, "authorityAfter": AFTER},
        "closedBlockerIdsByIdentityThisStep": {ID: [BLOCKER]},
        "nextBlockerPriority": final_order, "preparedNextGroup": next_row,
        "nextGroup": "rank9-death-recovery7", "nextPendingIds": [NEXT], "nextPendingCount": 1,
        "nextPendingGroup": next_row, "remainingPendingCount": 26, "pendingIdentityCount": 26,
        "packetStatus": "WEIRD_ACCEPTED_APPLIED; NEXT_FINAL_WORD_DR217-B01",
    })
    pending_path = A / "CURRENT26_PENDING_IDENTITY_AUDIT_302.json"
    write(pending_path, pending1)
    pending_ref = bind(pending_path)
    q1 = copy.deepcopy(q0)
    order = [row for row in q0.get("recommendedClosureOrder", []) if ID not in row.get("identities", []) and NEXT not in row.get("identities", [])]
    order = [{"priority": 1, "identities": [NEXT], "blockersByIdentity": {NEXT: [NEXT_BLOCKER]}, "remaining": next_row["directorRequirement"]}] + order
    for i, row in enumerate(order, 1):
        row["priority"] = i
    closure = [NEXT] + [x for x in final_order if x != NEXT]
    q1.update({
        "id": "SPELL-REVIEW-QUEUE-302", "recordedAtUtc": stamp,
        "supersedesQueue": bind(Q0), "parentQueue": bind(Q0), "currentAuthority": AFTER,
        "currentIndexBinding": index_ref, "pendingIdentityAudit": pending_ref, "pendingCount": 26,
        "nextGroup": "rank9-death-recovery7", "next": next_row,
        "nextPendingIds": [NEXT], "nextPendingCount": 1, "currentPendingGroups": filter_rows(q0.get("currentPendingGroups", [])),
        "nextSuggestedGroups": [next_row], "recommendedClosurePriority": closure,
        "recommendedClosureOrder": order,
        "lastReviewedBatch": pending1["lastReviewedBatch"],
        "justAppliedBatch": {"reviewId": acceptance_id, "applicationId": application_id, "ids": [ID], "count": 1, "applicationReceipt": application_ref, "directorDecision": decision_ref},
        "packetStatus": "WEIRD_PF182_B02_ACCEPTED_AND_APPLIED; NEXT_FINAL_WORD_DR217_B01",
        "currentAcceptedPacket": {"acceptedArchive": delta_ref, "directorDecision": decision_ref, "acceptance": acceptance_ref, "application": application_ref, "caseCoverage": coverage_ref, "candidatePackageManifest": pkg_manifest_ref},
        "currentDirectorPosition": {"stage": "WEIRD_ACCEPTED_APPLIED_PF182_B02; FINAL_WORD_NEXT", "acceptedIds": [ID], "appliedIds": [ID], "heldIds": sorted(live1), "blockers": {NEXT: [NEXT_BLOCKER]}, "nextPendingGroup": next_row},
        "nextPriorityContext": {"identity": NEXT, "blocker": NEXT_BLOCKER, "requirement": next_row["directorRequirement"]},
        "currentPreparation": next_row, "githubChanges": False, "canonicalRuntimeApplicationPerformed": False,
        "afterNextAcceptedAppliedForecast": {"remainingIdentities": 25},
    })
    queue_path = A / "CURRENT_SPELL_QUEUE_302.json"
    write(queue_path, q1)
    queue_ref = bind(queue_path)
    hand = copy.deepcopy(h0)
    hand.update({
        "id": "CURRENT-HANDOFF-302", "recordedAtUtc": stamp, "supersedes": h0.get("id"),
        "status": "WEIRD_APPLIED_NEXT_FINAL_WORD_822_26", "authority": AFTER, "currentAuthority": AFTER,
        "indexBinding": index_ref, "queueBinding": queue_ref,
        "queue": queue_path.relative_to(ROOT).as_posix(), "pendingIdentityAudit": pending_ref,
        "appliedThisStep": True, "acceptedThisStep": [ID],
        "appliedThisStepRecord": {"identity": ID, "application": application_path.relative_to(ROOT).as_posix(), "applicationBinding": application_ref, "closedBlockerIds": [BLOCKER]},
        "nextStep": next_row, "nextGroup": "rank9-death-recovery7", "nextPendingCount": 1,
        "nextPendingIds": [NEXT], "currentBlocker": {"identity": NEXT, "group": "rank9-death-recovery7", "blockerId": NEXT_BLOCKER},
        "directorConnectionStatus": "GPT explicitly accepted Weird / PF182-B02 authored-procedure review only; Codex independently applied that exact acceptance. Next is Final Word / DR217-B01.",
        "githubChanges": False, "latestBatch": {"accepted": [ID], "applied": [ID], "closed": {ID: [BLOCKER]}},
        "currentPreparation": next_row, "canonicalRuntimeApplicationPerformed": False,
        "nextStepText": next_row["directorRequirement"], "currentDirectorPosition": q1["currentDirectorPosition"],
        "resumePriority": [NEXT] + [x for x in closure if x != NEXT],
    })
    hand_path = A / "CURRENT_HANDOFF_302.json"
    write(hand_path, hand)
    hand_ref = bind(hand_path)

    checks = [
        ("Exact Weird-only Director acceptance and PF301 archive binding", decision["accepted"] and decision["appliedAtDecision"] is False and delta_ref["sha256"] == EXPECTED_DELTA_SHA),
        ("WCI-01 through WCI-04 and independent replay audit pass", independent["status"] == "PASS" and all(row["passed"] for row in independent["checks"]) and independent["summary"]["wci03Branches"] == 2),
        ("All 18 preserved Weird source cases and 1,054 events restore exact initial states", fresh["caseCount"] == 18 and fresh["eventCount"] == 1054 and fresh["allInitialStatesRestored"]),
        ("Only Weird leaves the pending authored-procedure set", live1 == live0 - {ID} and len(live1) == 26 and NEXT in live1),
        ("Authority advances exactly to 822/26/0 and 546/173", index1["authoredCounts"] == {"reviewed": 822, "pending": 26} and index1["representationCounts"]["completeReviewedStandaloneProcedures"] == 546 and AFTER["scopedInterfaces"] == 173),
        ("Native catalog remains byte-exact and Weird source remains blocked", CATALOG.read_bytes() == catalog_raw and entry1["sourceStatus"] == "blocked-pending-operational-review" and native["operational"] is None),
        ("Runtime selection and downstream approval gates remain closed", model["runtimeSelectionEnabled"] is False and model["implementationApproved"] is False and model["releaseApproved"] is False),
        ("Director priority advances to Final Word / DR217-B01", q1["next"]["pendingIds"] == [NEXT] and q1["recommendedClosurePriority"][0] == NEXT),
        ("Queue, pending audit, and handoff bind the same index and authority", pending1["indexBinding"]["sha256"] == index_ref["sha256"] and q1["currentIndexBinding"]["sha256"] == index_ref["sha256"] and hand["indexBinding"]["sha256"] == index_ref["sha256"] and q1["currentAuthority"] == hand["currentAuthority"] == pending1["authority"] == AFTER),
        ("Backup restores exact pre-application index bytes", backup.read_bytes() == index_raw),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    validation_path = A / "WEIRD_APPLICATION_VALIDATION_302.json"
    validation = {
        "id": "WEIRD-APPLICATION-VALIDATION-302", "recordedAtUtc": stamp, "status": "PASS",
        "checks": [{"check": name, "passed": bool(ok)} for name, ok in checks],
        "checkCount": len(checks), "failedChecks": 0, "acceptedIds": [ID], "appliedIds": [ID],
        "closedBlockerIds": [BLOCKER], "authority": AFTER, "index": index_ref,
        "application": application_ref, "acceptance": acceptance_ref, "pendingIdentityAudit": pending_ref,
        "queue": queue_ref, "handoff": hand_ref, "indexOperations": bind(operations_path),
        "candidatePackage": model_ref, "candidatePackageManifest": pkg_manifest_ref,
        "catalogByteExact": True, "sourceStatusPreservedAsBlocked": True, "runtimeSelectionEnabled": False,
    }
    write(validation_path, validation)
    validation_ref = bind(validation_path)
    snapshot_path = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_302.md"
    snapshot_path.write_text(
        "# Spell Review Snapshot — Weird Application 302\n\n"
        "Authority: **822 applied / 26 pending / 0 accepted-unapplied; 546 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "Weird / PF182-B02 was accepted for authored-procedure review under PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01 and applied to the authored review index. PF181-H05 and all other qualifications remain; no actual provider or gameplay turn is established. The native catalog stays blocked and runtime selection remains disabled.\n\n"
        "Next priority: **Final Word / DR217-B01**, followed by the current Director order recorded in CURRENT_SPELL_QUEUE_302.json.\n\n"
        "Validation: " + validation_ref["path"] + " (" + validation_ref["sha256"] + ").\n",
        encoding="utf-8", newline="\n",
    )
    assert CATALOG.read_bytes() == catalog_raw and backup.read_bytes() == index_raw
    print(json.dumps({"status": "PASS", "acceptedAndApplied": ID, "authority": AFTER, "index": index_ref,
                      "candidatePackage": model_ref, "application": application_ref, "validation": validation_ref,
                      "pendingAudit": pending_ref, "queue": queue_ref, "handoff": hand_ref, "next": next_row},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
