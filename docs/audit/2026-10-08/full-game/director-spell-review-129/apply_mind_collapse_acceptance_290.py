from __future__ import annotations

import copy
import hashlib
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
DELTA_DIR = A / "rank9_mindcollapse_closure_delta_290"
DELTA = DELTA_DIR / "MD196_B01_CLOSURE_DELTA.json"
DELTA_AUDIT = DELTA_DIR / "MD196_B01_CLOSURE_DELTA_INDEPENDENT_AUDIT.json"
SOURCE_ARCHIVE = A / "rank9_memorydenial6_return196_received/DD_Rank9_MemoryDenial6_Director_Return196.zip"
SOURCE_DELIVERY = A / "rank9_memorydenial6_return196_received/DD_Rank9_MemoryDenial6_Director_Return196_DELIVERY.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PENDING0 = A / "CURRENT32_PENDING_IDENTITY_AUDIT_290.json"
QUEUE0 = A / "CURRENT_SPELL_QUEUE_290.json"
HANDOFF0 = A / "CURRENT_HANDOFF_290.json"
PRIORITIES = A / "CURRENT_CLOSURE_PRIORITIES_290.json"

PACKAGE_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_mindcollapse_reviewed_290")
PACKAGE = ROOT / PACKAGE_REL
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/MIND_COLLAPSE_REVIEWED_290.md"
BACKUP = A / "authored_review_index.before_mind_collapse_290.json"
DECISION = A / "MIND_COLLAPSE_DIRECTOR_DECISION_290.json"
ACCEPTANCE = A / "MIND_COLLAPSE_EXACT_ACCEPTANCE_290.json"
RETURN_RECEIPT = A / "MIND_COLLAPSE_RETURN290_RECEIPT.json"
APPLICATION = A / "MIND_COLLAPSE_APPLICATION_290.json"
OPERATIONS = A / "MIND_COLLAPSE_INDEX_OPERATIONS_290.json"
PENDING1 = A / "CURRENT31_PENDING_IDENTITY_AUDIT_291.json"
QUEUE1 = A / "CURRENT_SPELL_QUEUE_291.json"
HANDOFF1 = A / "CURRENT_HANDOFF_291.json"
VALIDATION = A / "MIND_COLLAPSE_APPLICATION_VALIDATION_290.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_291.md"

ID = "mind-collapse"
NAME = "Mind Collapse"
BLOCKER = "MD196-B01"
REVIEW_ID = "RANK9-MEMORYDENIAL6-MIND-COLLAPSE-EXACT-ACCEPTANCE-290"
APPLICATION_ID = "RANK9-MEMORYDENIAL6-MIND-COLLAPSE-APPLICATION-290"
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
EXPECTED_DELTA_SHA = "5c00f2efa2cd9a089c8156056c268dceb58e37a9f56cb921299dd304aa7c27c9"
BEFORE = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
          "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
AFTER = {"reviewedApplied": 817, "pending": 31, "acceptedUnapplied": 0,
         "completeStandaloneProcedures": 541, "scopedInterfaces": 173}
NEXT_ID = "absolute-domination"
NEXT_BLOCKER = "AG190-B01"
NEXT_GROUP = "rank9-agency-control9"
RETAINED_HOLDS = ["MD196-H01", "MD196-H02", "MD196-H03", "MD196-H04", "MD196-H06", "MD196-H08"]
DIRECTOR_TEXT = (
    "ACCEPT — mind-collapse / MD196-B01 only. accepted=true, applied=false. MD196-B01 is closed. "
    "Verified the exact delta SHA-256: 5c00f2efa2cd9a089c8156056c268dceb58e37a9f56cb921299dd304aa7c27c9. "
    "The requested flag corrections pass. Independent replay passes 30 events, 224 forward operations, "
    "224 inverse operations and complete reverse traversal. Admission, regular-END markers, recharge, "
    "Ready termination, resources and conditional interface projections remain consistent. No residual correction remains. "
    "Acceptance covers the preserved Mind Collapse procedure plus MC290-EXTRA-TURN-BOUNDARY and this corrected delta. "
    "Retain MD290-Q-EXTRA-SOURCE and MD196-H01/H02/H03/H04/H06/H08. This establishes no acquired extra-turn provider "
    "and closes no other spell. Canonical index remains 816 applied / 32 pending until application, currently "
    "540 procedures / 173 interfaces. After independently verified application: 817 applied / 31 pending / "
    "0 accepted-unapplied, 541 procedures / 173 interfaces. Next: absolute-domination / AG190-B01, reassessed independently. "
    "All downstream gates remain closed; no canonical changes or application occurred."
)
QUALIFICATIONS = [
    "Acceptance is limited to the preserved static Mind Collapse procedure, MC290-EXTRA-TURN-BOUNDARY, and the exact 30-event closure delta.",
    "The inserted-turn boundary does not advance the three original regular-END markers or create extra repeat saves, duration decrements, recharge, Reaction refresh, Ready reset, or regular recovery.",
    "The A/T/H actors are source-bound conditional fixtures, not authenticated campaign people or events; this acceptance establishes no acquired extra-turn provider.",
    "MD290-Q-EXTRA-SOURCE remains: use of an external inserted-turn provider requires its separately authorized procedure, lawful acquisition, activation, recipient eligibility, and history.",
    "MD196-H01/H02/H03/H04/H06/H08 and all unrelated holds remain. Runtime, implementation, human-play, balance, cosmology, domain-closure, completion, and release gates stay closed.",
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode(value))


def binding(path: Path, raw: bytes | None = None) -> dict:
    content = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(content), "sha256": sha(content),
            "crc32": f"{zlib.crc32(content) & 0xffffffff:08x}"}


def in_archive(archive_binding: dict, member: str, content: bytes) -> dict:
    return {"archive": archive_binding, "memberPath": member, "bytes": len(content),
            "sha256": sha(content), "crc32": f"{zlib.crc32(content) & 0xffffffff:08x}"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def remove_identity_from_groups(groups: list[dict]) -> list[dict]:
    out = []
    for original in groups:
        row = copy.deepcopy(original)
        if "pendingIds" in row:
            row["pendingIds"] = [x for x in row["pendingIds"] if x != ID]
            if "pendingCount" in row:
                row["pendingCount"] = len(row["pendingIds"])
        if row.get("pendingCount", 1) == 0:
            continue
        out.append(row)
    return out


def main() -> None:
    package_members = {"DIRECTOR_DECISION.json", "PREVIOUS_PROCEDURE_RECORD.json", "PROCEDURE_RECORD.json",
                       "CASE_COVERAGE.json", "EVIDENCE_BINDINGS.json", "MODEL.json",
                       "MD196_B01_CLOSURE_DELTA.json", "MD196_B01_CLOSURE_DELTA_INDEPENDENT_AUDIT.json",
                       "STANDALONE_PROCEDURES.md", "CANDIDATE_PACKAGE_MANIFEST.json"}
    output_files = [MANUSCRIPT, BACKUP, DECISION, ACCEPTANCE, RETURN_RECEIPT, APPLICATION, OPERATIONS,
                    PENDING1, QUEUE1, HANDOFF1, VALIDATION, SNAPSHOT]
    assert not PACKAGE.exists() and all(not p.exists() for p in output_files), "Refusing to overwrite an existing application artifact."

    delta_raw, audit_raw = DELTA.read_bytes(), DELTA_AUDIT.read_bytes()
    delta_hash = sha(delta_raw)
    audit = json.loads(audit_raw)
    delta = json.loads(delta_raw)
    assert delta_hash == EXPECTED_DELTA_SHA
    assert audit["status"] == "PASS" and audit["checksPassed"] == 194 and audit["checksFailed"] == 0
    assert audit["closureDeltaFileSha256"] == EXPECTED_DELTA_SHA
    assert delta["directorDecision"]["id"] == "MD290-OBLIGATION-REVISION-01"
    assert delta["procedureAmendment"]["id"] == "MC290-EXTRA-TURN-BOUNDARY"
    assert delta["authority"] == {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
                                  "acceptedIds": [], "appliedIds": []}

    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index0, catalog0 = read(INDEX), read(CATALOG)
    p0, q0, h0, priorities = map(read, (PENDING0, QUEUE0, HANDOFF0, PRIORITIES))
    assert sha(index_raw) == p0["indexBinding"]["sha256"] == q0["currentIndexBinding"]["sha256"]
    assert sha(catalog_raw) == p0["catalogBinding"]["sha256"]
    assert index0["authoredCounts"] == {"reviewed": 816, "pending": 32}
    assert index0["representationCounts"]["completeReviewedStandaloneProcedures"] == 540
    assert p0["authority"] == q0["currentAuthority"] == h0["currentAuthority"] == BEFORE
    rows = {row["id"]: row for row in index0["entries"]}
    entry0 = copy.deepcopy(rows[ID])
    live0 = {row["id"] for row in index0["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert ID in live0 and len(live0) == 32 and set(p0["pendingIds"]) == live0
    assert entry0["authoredStatus"] == "pending-authored-procedure" and entry0["sourceStatus"] == "blocked-pending-operational-review"
    assert entry0["wholeCardPointer"] == "/spells/577"
    assert catalog0["spells"][577]["id"] == ID

    source_archive_raw = SOURCE_ARCHIVE.read_bytes()
    source_archive_binding = binding(SOURCE_ARCHIVE, source_archive_raw)
    delivery = read(SOURCE_DELIVERY)
    assert source_archive_binding["sha256"] == delivery["archive"]["sha256"] == "bc00b730c195ae835c560fd06945d04ae58359a5cbf8dccf6f72f7873d078ee4"
    assert source_archive_binding["bytes"] == delivery["archive"]["bytes"]
    with zipfile.ZipFile(SOURCE_ARCHIVE) as archive:
        assert archive.testzip() is None
        procedure_raw = archive.read("procedures/mind-collapse.json")
        source_procedure = json.loads(procedure_raw)
        case_index_raw = archive.read("CASE_INDEX.json")
        case_index = json.loads(case_index_raw)
    assert source_procedure["id"] == ID and source_procedure["accepted"] is False and source_procedure["applied"] is False
    assert source_procedure["blockerIds"] == [BLOCKER] and source_procedure["currentIndexEntryUnchanged"] == entry0
    assert sha(procedure_raw) == delta["sourceBindings"]["procedureSourceSha256"]
    catalog_row = catalog0["spells"][577]
    assert source_procedure["completeSourceAndAccess"]["source"]["catalogKey"] == catalog_row["id"] == ID
    base_cases = [copy.deepcopy(row) for row in case_index["cases"] if row.get("spellId") == ID]
    assert len(base_cases) == 14 and sum(int(row.get("events", 0)) for row in base_cases) == 317
    closure = delta["closureCase"]
    assert closure["id"] not in {row["id"] for row in base_cases}
    forward_count = sum(len(event.get("forward", [])) for event in closure["events"])
    inverse_count = sum(len(event.get("inverse", [])) for event in closure["events"])
    assert len(closure["events"]) == 30 and forward_count == inverse_count == 224
    assert len(closure["conditionalInterfaceTests"]) == 1

    timestamp = now()
    delta_binding = binding(DELTA, delta_raw)
    audit_binding = binding(DELTA_AUDIT, audit_raw)
    delivery_binding = binding(SOURCE_DELIVERY)
    previous_casebook_path = ROOT / closure["forkOf"]["casebookPath"]
    previous_caseindex_path = ROOT / closure["forkOf"]["caseIndexPath"]
    assert previous_casebook_path.exists() and previous_caseindex_path.exists()
    casebook_binding = binding(previous_casebook_path)
    caseindex_binding = binding(previous_caseindex_path)
    assert casebook_binding["sha256"] == closure["forkOf"]["casebookSha256"]
    assert casebook_binding["bytes"] == closure["forkOf"]["casebookBytes"]
    assert caseindex_binding["sha256"] == closure["forkOf"]["caseIndexSha256"]
    source_procedure_binding = in_archive(source_archive_binding, "procedures/mind-collapse.json", procedure_raw)
    source_case_index_binding = in_archive(source_archive_binding, "CASE_INDEX.json", case_index_raw)

    decision = {
        "id": "RANK9-MEMORYDENIAL6-MIND-COLLAPSE-GPT-DIRECTOR-DECISION-290",
        "recordedAtUtc": timestamp, "decision": "EXACT_ACCEPT", "identity": ID,
        "closedBlockerIds": [BLOCKER], "accepted": True, "appliedAtDecision": False,
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": URL},
        "exactDirectorResponse": DIRECTOR_TEXT,
        "directorObligationRevision": copy.deepcopy(delta["directorDecision"]),
        "delta": delta_binding, "independentAudit": audit_binding,
        "originalSourceArchive": source_archive_binding, "sourceDeliveryManifest": delivery_binding,
        "authorityAtDecision": BEFORE,
        "authorityAfterApplicationExpected": AFTER,
        "acceptanceScope": "Preserved Mind Collapse procedure + MC290-EXTRA-TURN-BOUNDARY + corrected MD196-B01 closure delta only.",
        "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": RETAINED_HOLDS,
        "nextPriority": {"identity": NEXT_ID, "blocker": NEXT_BLOCKER,
                         "requirement": "Independently demonstrate the inserted-turn grant in the control/turn branch; Mind Collapse evidence alone does not close this interaction."},
        "otherSpellAccepted": False,
        "canonicalFilesChangedByDirector": False,
        "gatesStillClosed": ["runtime", "implementation", "human-play", "balance", "cosmology", "domain-closure", "completion", "release"],
    }
    write(DECISION, decision)
    decision_binding = binding(DECISION)

    updated_procedure = copy.deepcopy(source_procedure)
    updated_procedure.update({
        "status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
        "accepted": True, "applied": True, "blockerIds": [], "closedBlockerIds": [BLOCKER],
        "resolvedBlockerIds": [BLOCKER], "procedureAmendment": copy.deepcopy(delta["procedureAmendment"]),
        "closureDeltaBinding": delta_binding, "closureDeltaAuditBinding": audit_binding,
        "directorDecisionBinding": decision_binding, "sourceArchiveBinding": source_archive_binding,
        "sourceProcedureMemberBinding": source_procedure_binding,
        "retainedQualifications": QUALIFICATIONS, "holdIds": RETAINED_HOLDS,
        "caseIds": [row["id"] for row in base_cases] + [closure["id"]],
        "scope": "Mind Collapse only; exact preserved procedure, MC290 boundary amendment and 30-event closure delta. Runtime remains disabled.",
    })

    case_coverage = {
        "id": "MIND-COLLAPSE-CASE-COVERAGE-290", "spellId": ID,
        "preservedSourceCases": {"archive": source_archive_binding, "caseIndexMember": source_case_index_binding,
                                 "casebook": casebook_binding, "count": len(base_cases),
                                 "events": sum(int(row.get("events", 0)) for row in base_cases),
                                 "cases": base_cases},
        "acceptedClosureCase": {"id": closure["id"], "delta": delta_binding, "audit": audit_binding,
                                 "forkOf": closure["forkOf"], "events": len(closure["events"]),
                                 "forwardOperations": forward_count, "inverseOperations": inverse_count,
                                 "conditionalInterfaceTests": len(closure["conditionalInterfaceTests"]),
                                 "fixtureQualification": closure["fixtureQualification"],
                                 "noAcquiredExtraTurnProviderEstablished": True},
        "totalsForThisAcceptance": {"preservedCaseCount": len(base_cases), "preservedEvents": 317,
                                    "newClosureEvents": 30, "newForwardOperations": 224,
                                    "newInverseOperations": 224},
    }
    evidence_bindings = {
        "id": "MIND-COLLAPSE-ACCEPTED-EVIDENCE-290", "directorDecision": decision_binding,
        "originalSourceArchive": source_archive_binding, "sourceDeliveryManifest": delivery_binding,
        "sourceProcedureMember": source_procedure_binding, "sourceCaseIndexMember": source_case_index_binding,
        "baseCasebook": casebook_binding, "closureDelta": delta_binding, "independentAudit": audit_binding,
        "sourceBindingsFromDelta": copy.deepcopy(delta["sourceBindings"]),
        "retainedQualifications": QUALIFICATIONS, "retainedHoldIds": RETAINED_HOLDS,
    }
    write(PACKAGE / "DIRECTOR_DECISION.json", decision)
    write(PACKAGE / "PREVIOUS_PROCEDURE_RECORD.json", source_procedure)
    write(PACKAGE / "PROCEDURE_RECORD.json", updated_procedure)
    write(PACKAGE / "CASE_COVERAGE.json", case_coverage)
    write(PACKAGE / "EVIDENCE_BINDINGS.json", evidence_bindings)
    (PACKAGE / "MD196_B01_CLOSURE_DELTA.json").write_bytes(delta_raw)
    (PACKAGE / "MD196_B01_CLOSURE_DELTA_INDEPENDENT_AUDIT.json").write_bytes(audit_raw)
    procedure_content = source_procedure["procedure"] + "\n\n" + delta["procedureAmendment"]["text"]
    model = {
        "schemaVersion": 1, "moduleId": "rank9memorydenial6-mindcollapse-reviewed-290",
        "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
        "scope": "Mind Collapse only; preserved procedure plus MC290-EXTRA-TURN-BOUNDARY and corrected closure delta. Native catalog and runtime remain unchanged.",
        "acceptedIds": [ID], "unacceptedIds": [], "excludedPendingIds": sorted(live0 - {ID}),
        "unresolvedQualifications": {ID: QUALIFICATIONS},
        "sharedRequirements": {"scope": "No global/shared rule changes; native catalog unchanged; runtime selection disabled.",
                              "runtimeSelectionEnabled": False},
        "spells": [{
            "id": ID, "name": NAME, "position": 0,
            "procedure": {"id": "MD196-STATIC-MIND-COLLAPSE-290", "spellId": ID,
                          "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                          "accepted": True, "applied": True,
                          "nativeCardUnchanged": copy.deepcopy(source_procedure["completeSourceAndAccess"]),
                          "procedureContent": procedure_content,
                          "sharedRequirements": source_procedure["commonProcedure"],
                          "spellLocalChoices": copy.deepcopy(source_procedure["newChoices"]),
                          "procedureAmendment": copy.deepcopy(delta["procedureAmendment"]),
                          "retainedQualifications": QUALIFICATIONS, "closedBlockerIds": [BLOCKER],
                          "retainedHoldIds": RETAINED_HOLDS,
                          "questionIds": copy.deepcopy(source_procedure["questionIds"]),
                          "caseIds": updated_procedure["caseIds"],
                          "directorDecisionId": decision["id"], "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
                          "caseCoverageFile": "CASE_COVERAGE.json"},
            "directorProcedureRecord": updated_procedure,
            "previousProcedureRecord": source_procedure,
            "nativeCardUnchanged": copy.deepcopy(source_procedure["completeSourceAndAccess"]),
            "caseIds": updated_procedure["caseIds"], "questionIds": copy.deepcopy(source_procedure["questionIds"]),
            "retainedHoldIds": RETAINED_HOLDS, "runtimeSelectionEnabled": False,
        }],
        "sourceArchive": source_archive_binding, "deliveryManifest": delivery_binding,
        "directorDecision": decision_binding, "closureDelta": delta_binding, "independentAudit": audit_binding,
        "caseCoverage": case_coverage, "evidenceBindings": evidence_bindings,
        "returnCounts": {"preservedCases": 14, "preservedEvents": 317, "newClosureEvents": 30,
                         "newForwardOperations": 224, "newInverseOperations": 224},
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "implementationApproved": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
        "domainClosure": False, "releaseApproved": False,
    }
    write(PACKAGE / "MODEL.json", model)
    manuscript = (
        "# Mind Collapse — accepted static authored procedure 290\n\n"
        "GPT accepted Mind Collapse / MD196-B01 only after independently verifying the corrected closure delta. "
        "This application updates the authored review index; the native spell catalog, runtime selection, and downstream gates remain unchanged.\n\n"
        "## Preserved native card\n\n" + json.dumps(source_procedure["completeSourceAndAccess"], ensure_ascii=False, indent=2) +
        "\n\n## Preserved procedure and accepted boundary amendment\n\n" + procedure_content +
        "\n\n## New closure witness\n\n" + f"- `{closure['id']}`: 30 events, 224 forward operations, 224 inverse operations; the 6.300–6.400 interface injection remains conditional test evidence only.\n" +
        "\n## Retained qualifications and holds\n\n" + "\n".join(f"- {x}" for x in QUALIFICATIONS) +
        "\n\nRetained hold IDs: " + ", ".join(RETAINED_HOLDS) + ".\n"
    )
    (PACKAGE / "STANDALONE_PROCEDURES.md").write_text(manuscript, encoding="utf-8", newline="\n")
    MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")
    package_manifest = {"id": "MIND-COLLAPSE-PACKAGE-MANIFEST-290", "directorDecision": decision_binding,
                        "sourcePacket": source_archive_binding, "closureDelta": delta_binding, "files": []}
    for file in sorted(x for x in PACKAGE.rglob("*") if x.is_file() and x.name != "CANDIDATE_PACKAGE_MANIFEST.json"):
        package_manifest["files"].append({"path": (PACKAGE_REL / file.relative_to(PACKAGE)).as_posix(),
                                           "bytes": file.stat().st_size, "sha256": sha(file.read_bytes())})
    write(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)
    assert {p.name for p in PACKAGE.iterdir()} == package_members

    model_binding = binding(PACKAGE / "MODEL.json")
    package_binding = binding(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json")
    coverage_binding = binding(PACKAGE / "CASE_COVERAGE.json")
    evidence_binding = binding(PACKAGE / "EVIDENCE_BINDINGS.json")
    manuscript_binding = binding(MANUSCRIPT)
    acceptance = {
        "id": REVIEW_ID, "recordedAtUtc": timestamp, "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED",
        "acceptedIds": [ID], "appliedIds": [], "closedBlockerIds": [BLOCKER],
        "directorDecision": decision_binding, "sourcePacket": source_archive_binding,
        "sourceDeliveryManifest": delivery_binding, "closureDelta": delta_binding,
        "independentAudit": audit_binding, "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_binding, "evidenceBindings": evidence_binding,
        "caseCoverage": coverage_binding,
        "countsBefore": {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0},
        "countsAfterAcceptanceBeforeApplication": {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 1},
        "scope": decision["acceptanceScope"], "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": RETAINED_HOLDS,
    }
    write(ACCEPTANCE, acceptance)
    acceptance_binding = binding(ACCEPTANCE)
    return_receipt = {
        "id": "MIND-COLLAPSE-RETURN290-RECEIPT", "recordedAtUtc": timestamp,
        "status": "EXACT_ACCEPT_MIND_COLLAPSE_MD196_B01_ONLY",
        "acceptedIds": [ID], "appliedIds": [], "closedBlockerIds": [BLOCKER],
        "directorDecision": decision_binding, "acceptance": acceptance_binding,
        "sourcePacket": source_archive_binding, "sourceDeliveryManifest": delivery_binding,
        "closureDelta": delta_binding, "independentAudit": audit_binding,
        "nextPriority": decision["nextPriority"], "retainedHoldIds": RETAINED_HOLDS,
        "sourceResponse": DIRECTOR_TEXT,
    }
    write(RETURN_RECEIPT, return_receipt)
    receipt_binding = binding(RETURN_RECEIPT)

    index1 = copy.deepcopy(index0)
    entry1 = copy.deepcopy(entry0)
    entry1.update({
        "authoredStatus": "reviewed-authored-operational-playtest",
        "procedureFile": "../spell_candidates/rank9memorydenial6_mindcollapse_reviewed_290/MODEL.json",
        "procedurePointer": "/spells/0/procedure", "wholeCardPointer": "/spells/0", "wholeCardIdField": "id",
        "sourceCatalogWholeCardPointer": entry0.get("sourceCatalogWholeCardPointer") or entry0["wholeCardPointer"],
        "procedureTextPointer": "/spells/0/procedure/procedureContent",
        "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
        "sharedRulesPointer": "/sharedRequirements", "spellLocalRequirementsPointer": "/spells/0/procedure/spellLocalChoices",
        "manuscript": "../../../docs/spells/candidates/MIND_COLLAPSE_REVIEWED_290.md",
        "reviewId": APPLICATION_ID, "runtimeSelectionEnabled": False, "historicalCandidateLabelsPreserved": True,
        "completeEvidenceRoot": PACKAGE_REL.as_posix(), "completeEnvelopeBinding": model_binding,
        "caseEvidenceBindings": coverage_binding, "sourceArchiveBinding": source_archive_binding,
        "deliveryManifestBinding": delivery_binding, "candidatePackageManifestBinding": package_binding,
        "procedureSourceBinding": decision_binding, "authoredAcceptanceReceipt": acceptance_binding,
        "authoredApplicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        "directorReturnReceipt": receipt_binding, "accepted": True, "applied": True,
        "closedBlockerIds": [BLOCKER], "retainedQualifications": QUALIFICATIONS,
        "retainedHoldIds": RETAINED_HOLDS,
    })
    entry_i = next(i for i, row in enumerate(index1["entries"]) if row["id"] == ID)
    index1["entries"][entry_i] = entry1
    assert not any(ID in row.get("acceptedIds", []) for row in index1["additionalStandaloneEnvelopes"])
    envelope = {
        "file": "../spell_candidates/rank9memorydenial6_mindcollapse_reviewed_290/MODEL.json",
        "binding": model_binding, "reviewId": REVIEW_ID, "acceptedIds": [ID], "unacceptedIds": [],
        "excludedPendingIds": sorted(live0 - {ID}), "authority": acceptance_binding,
        "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorDecision": decision_binding,
        "directorReturnReceipt": receipt_binding, "sourcePacket": source_archive_binding,
        "deliveryManifest": delivery_binding, "evidenceBindings": evidence_binding,
        "caseCoverage": coverage_binding, "candidatePackageManifestBinding": package_binding,
        "closureDelta": delta_binding, "independentAudit": audit_binding,
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
    }
    index1["additionalStandaloneEnvelopes"].append(envelope)
    index1["authoredCounts"] = {"reviewed": 817, "pending": 31}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"] = 541
    live1 = {row["id"] for row in index1["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert live1 == live0 - {ID} and len(live1) == 31 and NEXT_ID in live1
    if BACKUP.exists():
        assert BACKUP.read_bytes() == index_raw
    else:
        BACKUP.write_bytes(index_raw)
    write(INDEX, index1)
    index_core_binding = binding(INDEX)

    application = {
        "id": APPLICATION_ID, "recordedAtUtc": timestamp,
        "status": "APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE",
        "ownerInstruction": "Apply each exact Director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.",
        "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER],
        "directorAcceptance": acceptance_binding, "directorDecision": decision_binding,
        "directorReturnReceipt": receipt_binding, "sourcePacket": source_archive_binding,
        "sourceDeliveryManifest": delivery_binding, "closureDelta": delta_binding,
        "independentAudit": audit_binding, "candidateEnvelope": model_binding,
        "candidatePackageManifest": package_binding, "evidenceBindings": evidence_binding,
        "caseCoverage": coverage_binding, "manuscript": manuscript_binding,
        "indexBefore": binding(BACKUP, index_raw), "indexAfterCoreUpdate": index_core_binding,
        "countsBefore": BEFORE, "countsAfter": AFTER,
        "completeReviewedStandaloneProcedures": {"before": 540, "after": 541},
        "scopedInterfaces": 173, "catalogChanged": False, "sourceStatusPreservedAsBlocked": True,
        "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "implementationApproved": False,
        "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
        "domainClosure": False, "releaseApproved": False,
    }
    write(APPLICATION, application)
    application_binding = binding(APPLICATION)
    entry1["authoredApplicationReceipt"] = application_binding
    index1["entries"][entry_i] = entry1
    envelope["applicationReceipt"] = APPLICATION.relative_to(ROOT).as_posix()
    index1["additionalStandaloneEnvelopes"][-1] = envelope
    write(INDEX, index1)
    index_binding1 = binding(INDEX)

    write(OPERATIONS, {
        "id": "MIND-COLLAPSE-INDEX-OPERATIONS-290", "recordedAtUtc": timestamp,
        "before": binding(BACKUP, index_raw), "after": index_binding1,
        "operations": [
            {"op": "update-entry", "id": ID, "before": entry0, "after": entry1},
            {"op": "append-standalone-envelope", "acceptedIds": [ID]},
            {"op": "update-authored-counts", "before": {"reviewed": 816, "pending": 32}, "after": {"reviewed": 817, "pending": 31}},
            {"op": "increment-complete-procedure-count", "before": 540, "after": 541},
        ],
        "inverse": [
            {"op": "restore-entry", "id": ID, "value": entry0},
            {"op": "remove-appended-standalone-envelope", "acceptedIds": [ID]},
            {"op": "restore-authored-counts", "value": {"reviewed": 816, "pending": 32}},
            {"op": "restore-complete-procedure-count", "value": 540},
            {"op": "restore-byte-exact-index-from-backup", "backup": binding(BACKUP, index_raw)},
        ],
        "catalogByteExact": CATALOG.read_bytes() == catalog_raw,
        "nativeCardUnchanged": True, "sourceStatusPreservedAsBlocked": True,
        "inverseRestoresExactIndex": BACKUP.read_bytes() == index_raw,
        "note": "The rollback receipt preserves the exact pre-application index bytes; restoring that backup reverses the final receipt binding as well as the semantic count and entry updates.",
    })
    operations_binding = binding(OPERATIONS)
    assert CATALOG.read_bytes() == catalog_raw

    authority1 = copy.deepcopy(AFTER)
    p1 = copy.deepcopy(p0)
    groups1 = remove_identity_from_groups(p0["groups"])
    p1.update({
        "id": "CURRENT31-PENDING-IDENTITY-AUDIT-291", "recordedAtUtc": timestamp,
        "status": "PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_MIND_COLLAPSE_APPLICATION_290",
        "authority": authority1, "indexBinding": index_binding1, "catalogBinding": binding(CATALOG, catalog_raw),
        "pendingCount": 31, "pendingIds": sorted(live1), "groups": groups1,
        "heldIds": sorted(set(p0.get("heldIds", [])) - {ID}),
        "acceptedIds": sorted(set(p0.get("acceptedIds", [])) | {ID}),
        "appliedIds": sorted(set(p0.get("appliedIds", [])) | {ID}),
        "pendingGroupCount": sum(1 for group in groups1 if group.get("pendingCount", 0) > 0),
        "nextBlockerPriority": [NEXT_ID, "puppetmaster-s-realm", "psychic-scream", "mass-phantom-killer", "weird",
                                "final-word", "elemental-shell", "timeless-form", "invulnerable-sphere",
                                "nullification-wave", "reality-anchor", "time-stop", "fate-rewrite", "collapse-timeline",
                                "eternal-prophecy", "faction-omniscience-supreme", "banishment-gate",
                                "conjure-demiplane-fortress", "summon-elemental-avatar", "summon-herald-of-the-planes",
                                "summon-avatar-of-decay", "reverse-gravity-field", "alignment-ascension",
                                "alignment-perfection", "faction-incarnate", "faction-perfection",
                                "corruption-purification", "astral-projection", "imprisonment",
                                "divine-intervention-greater", "wish"],
        "applicationReceipt": application_binding, "directorDecision": decision_binding,
        "acceptanceReceipt": acceptance_binding,
        "closedBlockerIdsThisStep": sorted(set(p0.get("closedBlockerIdsThisStep", [])) | {BLOCKER}),
        "lastDirectorReturn": {"decisionId": decision["id"], "acceptedIds": [ID], "appliedIds": [ID],
                               "heldIds": [], "closedBlockerIds": [BLOCKER], "delta": delta_binding,
                               "independentAudit": audit_binding},
        "preparedNextGroup": {"group": NEXT_GROUP, "pendingIds": [NEXT_ID],
                              "freshPacketRequiredForCurrentAuthority": True,
                              "directorRequirement": decision["nextPriority"]["requirement"]},
        "allCurrentPendingIdentitiesReviewed": True, "unreviewedPendingIds": [],
        "noPendingTargetWasSilentlyAccepted": True,
        "allPendingIdsExistInNativeCatalog": live1 <= {row["id"] for row in catalog0["spells"]},
        "pendingIdentityCount": 31, "remainingPendingCount": 31,
    })
    write(PENDING1, p1)
    p1_binding = binding(PENDING1)

    priority_rows = copy.deepcopy(priorities["priorityOrder"])
    priority_rows = [row for row in priority_rows if ID not in row.get("identities", [])]
    next_order = []
    for rank, row in enumerate(priority_rows, 1):
        row = copy.deepcopy(row)
        row["priority"] = rank
        next_order.append(row)
    next_data = {"group": NEXT_GROUP, "pendingIds": [NEXT_ID], "pendingCount": 1,
                 "status": "DIRECTOR_NEXT_IDENTITY_AFTER_MIND_COLLAPSE_290",
                 "freshPacketRequiredForCurrentAuthority": True,
                 "directorRequirement": decision["nextPriority"]["requirement"]}
    q1 = copy.deepcopy(q0)
    q1.update({
        "id": "SPELL-REVIEW-QUEUE-291", "recordedAtUtc": timestamp,
        "supersedesQueue": binding(QUEUE0), "parentQueue": binding(QUEUE0),
        "currentAuthority": authority1, "currentIndexBinding": index_binding1,
        "pendingIdentityAudit": p1_binding, "pendingCount": 31,
        "nextGroup": NEXT_GROUP, "next": next_data, "nextPendingIds": [NEXT_ID],
        "currentPendingGroups": groups1, "nextSuggestedGroups": [next_data],
        "recommendedClosurePriority": [identity for row in next_order for identity in row.get("identities", [])],
        "recommendedClosureOrder": next_order,
        "lastReviewedBatch": {"group": "rank9-memory-denial6", "acceptedIds": [ID], "appliedIds": [ID],
                              "heldIds": [], "closedBlockerIds": [BLOCKER]},
        "justAppliedBatch": {"reviewId": REVIEW_ID, "applicationId": APPLICATION_ID,
                             "ids": [ID], "count": 1, "applicationReceipt": application_binding,
                             "directorDecision": decision_binding, "sourcePacket": source_archive_binding,
                             "closureDelta": delta_binding, "independentAudit": audit_binding},
        "packetStatus": "MIND_COLLAPSE_MD196_B01_ACCEPTED_AND_APPLIED; NEXT_ABSOLUTE_DOMINATION_AG190_B01",
        "currentAcceptedPacket": {"sourceArchive": source_archive_binding, "delivery": delivery_binding,
                                  "decision": decision_binding, "acceptance": acceptance_binding,
                                  "application": application_binding, "closureDelta": delta_binding,
                                  "independentAudit": audit_binding},
        "directorRemainingWorkResponse": {"text": DIRECTOR_TEXT, "source": {"conversationTitle": "Calibration review part 6", "url": URL}},
        "currentDirectorPosition": {"stage": "MIND_COLLAPSE_ACCEPTED_MD196_B01; ABSOLUTE_DOMINATION_NEXT",
                                    "acceptedIds": [ID], "appliedIds": [], "heldIds": sorted(live1),
                                    "blockers": {NEXT_ID: [NEXT_BLOCKER]},
                                    "nextPendingGroup": {"group": NEXT_GROUP, "pendingIds": [NEXT_ID],
                                                         "pendingCount": 1, "reportedByDirector": True}},
        "noFirstReviewTasksRemain": True, "afterNextAcceptedAppliedForecast": {"remainingIdentities": 30},
        "githubChanges": False, "canonicalRuntimeApplicationPerformed": False,
        "nextPriorityContext": decision["nextPriority"],
    })
    write(QUEUE1, q1)
    q1_binding = binding(QUEUE1)

    h1 = copy.deepcopy(h0)
    h1.update({
        "id": "CURRENT-HANDOFF-291", "recordedAtUtc": timestamp, "supersedes": h0["id"],
        "status": "MIND_COLLAPSE_APPLIED_NEXT_ABSOLUTE_DOMINATION_817_31",
        "authority": authority1, "currentAuthority": authority1, "indexBinding": index_binding1,
        "queueBinding": q1_binding, "queue": QUEUE1.relative_to(ROOT).as_posix(),
        "pendingIdentityAudit": p1_binding, "appliedThisStep": True,
        "acceptedThisStep": [ID], "appliedThisStepRecord": {"identity": ID,
            "application": APPLICATION.relative_to(ROOT).as_posix(), "applicationBinding": application_binding,
            "closedBlockerIds": [BLOCKER]},
        "nextStep": next_data, "nextGroup": NEXT_GROUP, "nextPendingCount": 1,
        "nextPendingIds": [NEXT_ID], "currentBlocker": {"identity": NEXT_ID, "group": NEXT_GROUP, "blockerId": NEXT_BLOCKER},
        "directorConnectionStatus": "GPT explicitly accepted Mind Collapse / MD196-B01 only; next priority is absolute-domination / AG190-B01.",
        "githubChanges": False, "latestBatch": {"accepted": [ID], "applied": [ID], "closed": [BLOCKER]},
        "currentPreparation": next_data, "canonicalRuntimeApplicationPerformed": False,
        "nextStepText": "Independently prepare and review the inserted-turn grant in the absolute-domination control/turn branch; Mind Collapse does not close AG190-B01.",
        "currentDirectorPosition": {"stage": "MIND_COLLAPSE_ACCEPTED_MD196_B01; ABSOLUTE_DOMINATION_NEXT",
                                    "acceptedIds": [ID], "appliedIds": [], "heldIds": sorted(live1),
                                    "blockers": {NEXT_ID: [NEXT_BLOCKER]},
                                    "nextPendingGroup": {"group": NEXT_GROUP, "pendingIds": [NEXT_ID],
                                                         "pendingCount": 1, "reportedByDirector": True}},
    })
    write(HANDOFF1, h1)
    h1_binding = binding(HANDOFF1)

    validation_checks = [
        ("Director explicitly accepted only Mind Collapse / MD196-B01", decision["accepted"] is True and decision["appliedAtDecision"] is False and decision["closedBlockerIds"] == [BLOCKER]),
        ("Corrected delta hash and independent audit pass", delta_hash == EXPECTED_DELTA_SHA and audit["checksPassed"] == 194 and audit["checksFailed"] == 0),
        ("Preserved Mind Collapse source procedure and native catalog binding match", sha(procedure_raw) == delta["sourceBindings"]["procedureSourceSha256"] and catalog0["spells"][577]["id"] == ID),
        ("Original cases retained and closure case adds 30 events / 224 reversible operations", len(base_cases) == 14 and len(closure["events"]) == 30 and forward_count == inverse_count == 224),
        ("Only Mind Collapse leaves the exact pending set", live1 == live0 - {ID} and len(live1) == 31),
        ("Authority advances to 817 applied / 31 pending / 541 procedures / 173 interfaces", index1["authoredCounts"] == {"reviewed": 817, "pending": 31} and index1["representationCounts"]["completeReviewedStandaloneProcedures"] == 541 and authority1 == AFTER),
        ("Source status remains blocked and native catalog remains byte-exact", index1["entries"][entry_i]["sourceStatus"] == "blocked-pending-operational-review" and CATALOG.read_bytes() == catalog_raw),
        ("Runtime and downstream gates remain disabled", model["runtimeSelectionEnabled"] is False and model["implementationApproved"] is False and model["releaseApproved"] is False),
        ("Next Director priority is absolute-domination / AG190-B01", q1["next"]["pendingIds"] == [NEXT_ID] and q1["next"]["group"] == NEXT_GROUP and q1["nextPriorityContext"]["blocker"] == NEXT_BLOCKER),
    ]
    assert all(passed for _, passed in validation_checks)
    write(VALIDATION, {
        "id": "MIND-COLLAPSE-APPLICATION-VALIDATION-290", "recordedAtUtc": timestamp,
        "status": "PASS", "checks": [{"check": label, "passed": passed} for label, passed in validation_checks],
        "checkCount": len(validation_checks), "failedChecks": 0, "acceptedIds": [ID], "appliedIds": [ID],
        "authority": authority1, "index": index_binding1, "application": application_binding,
        "pendingIdentityAudit": p1_binding, "queue": q1_binding, "handoff": h1_binding,
        "indexOperations": operations_binding, "catalogByteExact": True,
        "sourceStatusPreservedAsBlocked": True, "runtimeSelectionEnabled": False,
    })
    validation_binding = binding(VALIDATION)
    SNAPSHOT.write_text(
        "# Spell Review Snapshot — Mind Collapse Application 290\n\n"
        "Authority: **817 applied / 31 pending / 0 accepted-unapplied; 541 complete standalone procedures / 173 scoped interfaces.**\n\n"
        "Mind Collapse / MD196-B01 was explicitly accepted by GPT and applied to the authored review index using the corrected 30-event closure delta. "
        "The preserved source procedure and all six retained MD196 holds remain bound. The native spell catalog and runtime selection are unchanged.\n\n"
        "Next priority: **absolute-domination / AG190-B01**. The Director requires an independent inserted-turn demonstration in the control/turn branch.\n\n"
        f"Validation: {validation_binding['path']} ({validation_binding['sha256']}).\n",
        encoding="utf-8", newline="\n")

    final_index = read(INDEX)
    assert final_index["authoredCounts"] == {"reviewed": 817, "pending": 31}
    assert final_index["entries"][entry_i]["sourceStatus"] == "blocked-pending-operational-review"
    assert CATALOG.read_bytes() == catalog_raw
    print(json.dumps({"status": "PASS", "acceptedApplied": ID, "authority": AFTER,
                      "index": binding(INDEX), "pendingAudit": str(PENDING1), "queue": str(QUEUE1),
                      "handoff": str(HANDOFF1), "validation": str(VALIDATION),
                      "next": decision["nextPriority"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
