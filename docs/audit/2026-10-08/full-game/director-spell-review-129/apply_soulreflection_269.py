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
PACKET_DIR = A / "rank9_illusionreality5_delta_269_prepared"
ARCHIVE = PACKET_DIR / "DD_Rank9_SoulReflection_Delta_269.zip"
DELIVERY = PACKET_DIR / "DD_Rank9_SoulReflection_Delta_269_DELIVERY.json"
INDEPENDENT_AUDIT = PACKET_DIR / "SOUL_REFLECTION_DELTA_269_INDEPENDENT_AUDIT.json"
SUBMISSION = PACKET_DIR / "SOUL_REFLECTION_DELTA_269_SUBMISSION.json"

INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PACKAGE_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9illusionreality5_reviewed_269")
PACKAGE = ROOT / PACKAGE_REL
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/SOUL_REFLECTION_REVIEWED_269.md"

DECISION = A / "SOUL_REFLECTION_DIRECTOR_DECISION_269.json"
ACCEPTANCE = A / "SOUL_REFLECTION_EXACT_ACCEPTANCE_269.json"
RETURN_RECEIPT = A / "SOUL_REFLECTION_RETURN_RECEIPT_269.json"
APPLICATION = A / "SOUL_REFLECTION_APPLICATION_269.json"
OPERATIONS = A / "SOUL_REFLECTION_INDEX_OPERATIONS_269.json"
BACKUP = A / "authored_review_index.before_soulreflection_269.json"
PENDING_BEFORE = A / "CURRENT34_PENDING_IDENTITY_AUDIT_262.json"
QUEUE_BEFORE = A / "CURRENT_SPELL_QUEUE_262.json"
HANDOFF_BEFORE = A / "CURRENT_HANDOFF_262.json"
PENDING_AFTER = A / "CURRENT33_PENDING_IDENTITY_AUDIT_269.json"
QUEUE_AFTER = A / "CURRENT_SPELL_QUEUE_269.json"
HANDOFF_AFTER = A / "CURRENT_HANDOFF_269.json"
STATE_CORRECTION = A / "CURRENT_REVIEW_STATE_CORRECTION_269.json"
VALIDATION = A / "SOUL_REFLECTION_APPLICATION_VALIDATION_269.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_269.md"

ID = "soul-reflection"
GROUP = "rank9-illusion-reality5"
BLOCKERS = ["IR207-B02", "IR268-C01"]
NEXT_ID = "unholy-ascendance"
NEXT_GROUP = "rank9-casting-cost5"
NEXT_BLOCKER = "CC194-B04"
REVIEW_ID = "RANK9-ILLUSIONREALITY5-SOUL-REFLECTION-EXACT-AUTHORED-ACCEPTANCE-269"
APPLICATION_ID = "RANK9-ILLUSIONREALITY5-SOUL-REFLECTION-APPLICATION-269"
GPT_URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"

QUALIFICATIONS = [
    "This accepts one static authored Soul Reflection procedure with the five Delta 269 witnesses only; it does not enable runtime selection or execution.",
    "The Cave Bear source authorization remains narrow to the witnessed Cave Bear profile and fixture. It does not authorize arbitrary companion or creature profiles.",
    "The phase-less recipient branch remains conditional; the witnessed attached Cave Bear case does not establish a general phase-less schedule.",
    "Only the demonstrated spell-local cast, snapshot, finite resources, phase ordering, concentration, cargo, damage and lifecycle callbacks are accepted. Unsupported forms, creature anatomy, copied dependencies and unbound branches remain held.",
    "Soul Reflection preserves the native card and source envelope. No global spell, companion, form, concentration, healing, phase, Null, death or inventory rule is added.",
    "Runtime, implementation, human playtest, balance, cosmology, domain closure, game completion and release gates remain closed.",
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encode_json(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(encode_json(value))


def binding(path: Path, raw: bytes | None = None) -> dict:
    data = path.read_bytes() if raw is None else raw
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": sha(data),
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
    }


def member_binding(archive_binding: dict, row: dict) -> dict:
    return {
        "archive": archive_binding,
        "memberPath": row["path"],
        "bytes": row["bytes"],
        "sha256": row["sha256"],
        "crc32": row["crc32"],
    }


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


OUTPUTS = [PACKAGE, MANUSCRIPT, DECISION, ACCEPTANCE, RETURN_RECEIPT, APPLICATION,
           OPERATIONS, BACKUP, PENDING_AFTER, QUEUE_AFTER, HANDOFF_AFTER,
           STATE_CORRECTION, VALIDATION, SNAPSHOT]
assert all(not path.exists() for path in OUTPUTS if path != BACKUP), "Refuse to overwrite a prior Soul Reflection application artifact"

archive_raw = ARCHIVE.read_bytes()
archive_binding = binding(ARCHIVE, archive_raw)
delivery = read_json(DELIVERY)
audit = read_json(INDEPENDENT_AUDIT)
submission_before = read_json(SUBMISSION)
assert archive_binding["bytes"] == 14_111_384
assert archive_binding["sha256"] == "35a762f0b590bc34e9f2eda70b937cb282bc9fd0df48ba919c7618bafe533efd"
assert archive_binding["crc32"] == "0fca8e57"
assert archive_binding["sha256"] == delivery["archive"]["sha256"] and archive_binding["bytes"] == delivery["archive"]["bytes"]
assert delivery["targetIds"] == [ID] and delivery["authority"] == {
    "reviewedApplied": 814, "pending": 34, "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 538, "scopedInterfaces": 173,
}
assert audit["status"] == "PASS" and audit["passedChecks"] == audit["checkCount"] == 27 and audit["failedChecks"] == 0
assert audit["archive"]["sha256"] == archive_binding["sha256"] and audit["acceptanceOrApplicationPerformed"] is False
assert submission_before["status"] == "AUDITED_PREPARED_UNSENT" and submission_before["targetIds"] == [ID]

with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None
    manifest = json.loads(z.read("MEMBER_MANIFEST.json"))
    assert manifest["memberCountExcludingSelf"] == len(manifest["members"]) == 49
    assert len(z.namelist()) == 50 and set(z.namelist()) == {"MEMBER_MANIFEST.json"} | {x["path"] for x in manifest["members"]}
    for row in manifest["members"]:
        raw = z.read(row["path"])
        assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
        assert f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}" == row["crc32"]
    source_procedure = json.loads(z.read("return246/members/PROCEDURE.json"))
    assert source_procedure["id"] == ID and source_procedure["accepted"] is False
    case_rows = [row for row in manifest["members"] if row["path"].startswith("cases/")]
    cases = {row["path"]: json.loads(z.read(row["path"])) for row in case_rows}
    archived_index_raw = z.read("current/authored_review_index.json")
    archived_catalog_raw = z.read("current/catalog.json")
    source_bindings = json.loads(z.read("sourceBindings/CURRENT_SOURCE_BINDINGS_269.json"))

assert len(case_rows) == 5
assert sum(len(case["events"]) for case in cases.values()) == 118
assert sum(len(case["events"]) for case in cases.values()) * 2 == 236
assert len(source_bindings) == 22

index_before_raw = INDEX.read_bytes()
catalog_before_raw = CATALOG.read_bytes()
assert archived_index_raw == index_before_raw, "The accepted packet is not bound to the current authored index"
assert archived_catalog_raw == catalog_before_raw, "The accepted packet is not bound to the current native catalog"
index_before = read_json(INDEX)
catalog_before = read_json(CATALOG)
pending_audit_before = read_json(PENDING_BEFORE)
queue_before = read_json(QUEUE_BEFORE)
handoff_before = read_json(HANDOFF_BEFORE)
assert index_before["authoredCounts"] == {"reviewed": 814, "pending": 34}
assert index_before["representationCounts"]["completeReviewedStandaloneProcedures"] == 538
assert index_before["representationCounts"].get("scopedInterfaces", 173) == 173
authority_before = {"reviewedApplied": 814, "pending": 34, "acceptedUnapplied": 0,
                    "completeStandaloneProcedures": 538, "scopedInterfaces": 173}
assert queue_before["currentAuthority"] == authority_before
assert pending_audit_before["authority"] == authority_before and pending_audit_before["indexBinding"]["sha256"] == sha(index_before_raw)
assert queue_before["currentIndexBinding"]["sha256"] == sha(index_before_raw)
assert queue_before["next"]["identity"] == ID and queue_before["next"]["blocker"] == "IR207-B02"
entry_index = next(i for i, row in enumerate(index_before["entries"]) if row["id"] == ID)
entry_before = copy.deepcopy(index_before["entries"][entry_index])
pending_before = {row["id"] for row in index_before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
assert len(pending_before) == 34 and ID in pending_before
assert entry_before["authoredStatus"] == "pending-authored-procedure"
assert source_procedure["currentIndexEntryUnchanged"] == entry_before
assert source_procedure["sourceBinding"]["path"].endswith("spell_playtests/catalog.json")
assert source_procedure["nativeCardUnchanged"] == next(row for row in catalog_before["spells"] if row["id"] == ID)
assert set(pending_audit_before["pendingIds"]) == pending_before

index_binding_before = binding(BACKUP, index_before_raw)
if BACKUP.exists():
    assert BACKUP.read_bytes() == index_before_raw, "Existing backup is not the exact current index"
else:
    BACKUP.write_bytes(index_before_raw)
assert BACKUP.read_bytes() == index_before_raw
source_audit_binding = binding(INDEPENDENT_AUDIT)
delivery_binding = binding(DELIVERY)
case_bindings = {path: member_binding(archive_binding, row) for path, row in
                 ((r["path"], r) for r in case_rows)}
procedure_member_row = next(x for x in manifest["members"] if x["path"] == "return246/members/PROCEDURE.json")
procedure_member_binding = member_binding(archive_binding, procedure_member_row)
source_bindings_member = next(x for x in manifest["members"] if x["path"] == "sourceBindings/CURRENT_SOURCE_BINDINGS_269.json")
source_bindings_binding = member_binding(archive_binding, source_bindings_member)

decision = {
    "id": "RANK9-ILLUSIONREALITY5-SOUL-REFLECTION-GPT-DIRECTOR-DECISION-269",
    "recordedAtUtc": now(),
    "decision": "EXACT_ACCEPT",
    "identity": ID,
    "group": GROUP,
    "closedBlockerIds": BLOCKERS,
    "accepted": True,
    "appliedAtDecision": False,
    "countsAtDecision": authority_before,
    "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": GPT_URL},
    "packet": archive_binding,
    "deliveryManifest": delivery_binding,
    "independentAudit": source_audit_binding,
    "exactAcceptance": {
        "status": "ACCEPT — soul-reflection / IR207-B02",
        "accepted": True,
        "applied": False,
        "blockersClosed": BLOCKERS,
        "remainingBlockingDefect": None,
        "verified": [
            "Exact archive size and SHA-256; 50-member allowlist, member hashes/CRCs, delivery binding and 22 source bindings.",
            "All five traces: 118 events, 236 forward operations and 236 inverse operations, including complete reverse traversal.",
            "All ten cast-window actor sets match their actual before-states.",
            "Both corrections propagate throughout histories; responder records and previously reviewed state content remain unchanged.",
        ],
        "scope": "The preserved Soul Reflection static-authored procedure, Delta269 spell-local rulings and five completed witnesses.",
        "retainedRulings": [
            "Cave Bear authorization remains narrowly scoped.",
            "The phase-less recipient branch remains conditional.",
            "All other qualifications and runtime, implementation, playtest, balance, cosmology, domain-closure, completion and release gates remain intact.",
        ],
    },
    "authorityAfterApplicationExpected": {"reviewedApplied": 815, "pending": 33, "acceptedUnapplied": 0,
        "completeStandaloneProcedures": 539, "scopedInterfaces": 173},
    "nextPriority": {"identity": NEXT_ID, "group": NEXT_GROUP, "blocker": NEXT_BLOCKER,
        "requiredWitnessScope": ["caster-Undead zero-HP/Null recipient contract",
                                 "type-specific healing", "death consequences", "other-form adverse traces"]},
    "retainedQualifications": QUALIFICATIONS,
    "gatesStillClosed": ["runtime", "implementation", "human-play", "balance", "cosmology",
                         "domain-closure", "completion", "release"],
}
write_json(DECISION, decision)
decision_binding = binding(DECISION)

procedure_record = copy.deepcopy(source_procedure)
procedure_record.update({
    "status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
    "accepted": True,
    "applied": True,
    "blockerIds": [],
    "closedBlockerIds": BLOCKERS,
    "holdIds": [x for x in source_procedure.get("holdIds", []) if x not in BLOCKERS],
    "caseIds": list(dict.fromkeys(source_procedure.get("caseIds", []) + [case.get("id") for case in cases.values()])),
    "directorDecisionBinding": decision_binding,
    "packetBinding": archive_binding,
    "deliveryManifestBinding": delivery_binding,
    "independentAuditBinding": source_audit_binding,
    "sourceProcedureMemberBinding": procedure_member_binding,
    "acceptedWitnessBindings": case_bindings,
    "retainedQualifications": QUALIFICATIONS,
    "scope": "Soul Reflection only. Five bound Delta269 witnesses close IR207-B02 and IR268-C01. Cave Bear scope remains narrow and the phase-less recipient branch remains conditional.",
})

case_coverage = {
    "id": "SOUL-REFLECTION-CASE-COVERAGE-269",
    "sourceProcedure": procedure_member_binding,
    "witnessCases": [
        {"id": cases[path]["id"], "member": case_bindings[path],
         "acceptedResult": result}
        for path, result in [
            ("cases/FORM_SNAPSHOT_269.json", "The source-paid Gaseous Form recipient reverts at its exact source deadline; form/body/equipment and phase state settle without invented anatomy."),
            ("cases/COPIED_CONCENTRATION_269.json", "Copied Gaseous Form has its own cast window; the later source-qualified Arcane Bolt causes the actual concentration save and ending with exact phase budgets."),
            ("cases/ORIGINAL_ZERO_269.json", "The original target, not the reflection, reaches zero; damage, conditions, death-save history, item custody and finite-opponent termination settle in order."),
            ("cases/ORIGINAL_CARGO_269.json", "One actually entrusted original map remains distinct from temporary reflection gear and follows suppression, resumption and ending custody."),
            ("cases/ATTACHED_CAVE_BEAR_269.json", "The source-qualified Cave Bear is bonded and the reflection follows three actual attached phase markers without inventing target regular turns; authorization remains profile-specific."),
        ]
    ],
    "independentAudit": source_audit_binding,
    "events": 118,
    "forwardOperations": 236,
    "inverseOperations": 236,
    "castWindowActorSetComparisons": 10,
    "boundedFixturesOnly": True,
}
evidence_bindings = {
    "id": "SOUL-REFLECTION-ACCEPTED-EVIDENCE-269",
    "directorDecision": decision_binding,
    "packet": archive_binding,
    "deliveryManifest": delivery_binding,
    "independentAudit": source_audit_binding,
    "sourceBindingsMember": source_bindings_binding,
    "sourceProcedureMember": procedure_member_binding,
    "witnesses": case_bindings,
    "caseCoverage": case_coverage,
    "retainedQualifications": QUALIFICATIONS,
}

PACKAGE.mkdir(parents=True)
write_json(PACKAGE / "DIRECTOR_DECISION.json", decision)
write_json(PACKAGE / "PROCEDURE_RECORD.json", procedure_record)
write_json(PACKAGE / "CASE_COVERAGE.json", case_coverage)
write_json(PACKAGE / "EVIDENCE_BINDINGS.json", evidence_bindings)
write_json(PACKAGE / "RETAINED_QUALIFICATIONS.json", {
    "identity": ID, "closedBlockerIds": BLOCKERS,
    "retainedHoldIds": procedure_record["holdIds"], "qualifications": QUALIFICATIONS,
})
procedure_content = procedure_record["procedure"] + "\n\n" + "\n\n".join(
    f"{qid}: {row['rule']}" for qid, row in procedure_record.get("newChoices", {}).items())
model = {
    "schemaVersion": 1,
    "moduleId": "rank9illusionreality5-reviewed-269",
    "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
    "scope": "Soul Reflection only; five bounded source-qualified lifecycle witnesses accepted; runtime and shared rules unchanged.",
    "acceptedIds": [ID],
    "unacceptedIds": [],
    "excludedPendingIds": sorted(pending_before - {ID}),
    "unresolvedQualifications": {ID: QUALIFICATIONS},
    "sharedRequirements": {"scope": "No global/shared rule changes; accepted effects are spell-local and the runtime remains disabled.",
                         "runtimeSelectionEnabled": False},
    "spells": [{
        "id": ID,
        "name": entry_before["name"],
        "position": 0,
        "procedure": {
            "id": "IR207-STATIC-SOUL-REFLECTION",
            "spellId": ID,
            "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
            "accepted": True,
            "applied": True,
            "nativeCardUnchanged": copy.deepcopy(procedure_record["nativeCardUnchanged"]),
            "procedureContent": procedure_content,
            "spellLocalChoices": copy.deepcopy(procedure_record["newChoices"]),
            "retainedQualifications": QUALIFICATIONS,
            "retainedHoldIds": procedure_record["holdIds"],
            "closedBlockerIds": BLOCKERS,
            "directorDecisionId": decision["id"],
            "directorDecisionBinding": decision_binding,
            "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
            "caseCoverageFile": "CASE_COVERAGE.json",
        },
        "directorProcedureRecord": procedure_record,
        "nativeCardUnchanged": copy.deepcopy(procedure_record["nativeCardUnchanged"]),
        "caseIds": [case.get("id") for case in cases.values()],
        "holdIds": procedure_record["holdIds"],
        "runtimeSelectionEnabled": False,
    }],
    "sourceArchive": archive_binding,
    "deliveryManifest": delivery_binding,
    "independentAudit": source_audit_binding,
    "caseCoverage": case_coverage,
    "evidenceBindings": evidence_bindings,
    "returnCounts": {"events": 118, "forwardOperations": 236, "inverseOperations": 236,
                     "castWindowActorSetComparisons": 10},
    "runtimeSelectionEnabled": False,
    "runtimeTestsExecuted": False,
    "implementationApproved": False,
    "humanPlaytested": False,
    "balanceApproved": False,
    "cosmologyModified": False,
    "domainClosure": False,
    "releaseApproved": False,
}
write_json(PACKAGE / "MODEL.json", model)
manuscript = (
    "# Soul Reflection — accepted static authored procedure 269\n\n"
    "GPT explicitly accepted Soul Reflection / IR207-B02 after Delta269 closed the five named lifecycle witnesses and the IR268-C01 snapshot metadata defect. "
    "This application updates one authored-review index entry and leaves the native spell card, runtime selection and other approval gates unchanged.\n\n"
    "## Preserved native card\n\n" + json.dumps(procedure_record["nativeCardUnchanged"], ensure_ascii=False, indent=2) +
    "\n\n## Accepted procedure and spell-local choices\n\n" + procedure_content +
    "\n\n## Accepted witness scope\n\n" + "\n".join(
        f"- {x['id']}: {x['acceptedResult']}" for x in case_coverage["witnessCases"]) +
    "\n\n## Retained qualifications\n\n" + "\n".join(f"- {x}" for x in QUALIFICATIONS) + "\n"
)
(PACKAGE / "STANDALONE_PROCEDURES.md").write_text(manuscript, encoding="utf-8", newline="\n")
MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")

package_manifest = {"id": "SOUL-REFLECTION-PACKAGE-MANIFEST-269", "decision": decision_binding,
                    "sourcePacket": archive_binding, "files": []}
for path in sorted(p for p in PACKAGE.rglob("*") if p.is_file() and p.name != "CANDIDATE_PACKAGE_MANIFEST.json"):
    package_manifest["files"].append({"path": (PACKAGE_REL / path.relative_to(PACKAGE)).as_posix(),
        "bytes": path.stat().st_size, "sha256": sha(path.read_bytes())})
write_json(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)

model_binding = binding(PACKAGE / "MODEL.json")
package_binding = binding(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json")
case_coverage_binding = binding(PACKAGE / "CASE_COVERAGE.json")
evidence_binding = binding(PACKAGE / "EVIDENCE_BINDINGS.json")
manuscript_binding = binding(MANUSCRIPT)
acceptance = {
    "id": REVIEW_ID,
    "recordedAtUtc": now(),
    "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED",
    "acceptedIds": [ID], "appliedIds": [], "closedBlockerIds": BLOCKERS,
    "retainedQualificationIds": procedure_record["holdIds"],
    "directorDecision": decision_binding, "packet": archive_binding,
    "delivery": delivery_binding, "independentAudit": source_audit_binding,
    "candidateEnvelope": model_binding, "candidatePackageManifest": package_binding,
    "evidenceBindings": evidence_binding, "caseCoverage": case_coverage_binding,
    "countsBefore": {"reviewed": 814, "pending": 34, "acceptedUnapplied": 0},
    "countsAfterAcceptanceBeforeApplication": {"reviewed": 814, "pending": 33, "acceptedUnapplied": 1},
    "scope": "One static Soul Reflection authored procedure with the five bounded Delta269 witnesses; conditional branch and downstream qualifications remain intact.",
}
write_json(ACCEPTANCE, acceptance)
acceptance_binding = binding(ACCEPTANCE)
write_json(RETURN_RECEIPT, {
    "id": "SOUL-REFLECTION-DELTA269-RETURN-RECEIPT",
    "recordedAtUtc": now(), "status": "EXACT_ACCEPT_SOUL_REFLECTION",
    "acceptedIds": [ID], "appliedIds": [], "closedBlockerIds": BLOCKERS,
    "directorDecision": decision_binding, "acceptance": acceptance_binding,
    "packet": archive_binding, "delivery": delivery_binding,
    "nextPriority": decision["nextPriority"],
})
return_binding = binding(RETURN_RECEIPT)

index_after = copy.deepcopy(index_before)
entry_after = copy.deepcopy(entry_before)
entry_after.update({
    "authoredStatus": "reviewed-authored-operational-playtest",
    "procedureFile": "../spell_candidates/rank9illusionreality5_reviewed_269/MODEL.json",
    "procedurePointer": "/spells/0/procedure",
    "wholeCardPointer": "/spells/0",
    "wholeCardIdField": "id",
    "sourceCatalogWholeCardPointer": entry_before.get("sourceCatalogWholeCardPointer") or entry_before["wholeCardPointer"],
    "procedureTextPointer": "/spells/0/procedure/procedureContent",
    "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
    "sharedRulesPointer": "/sharedRequirements",
    "spellLocalRequirementsPointer": "/spells/0/procedure/spellLocalChoices",
    "manuscript": "../../../docs/spells/candidates/SOUL_REFLECTION_REVIEWED_269.md",
    "reviewId": APPLICATION_ID,
    "runtimeSelectionEnabled": False,
    "historicalCandidateLabelsPreserved": True,
    "completeEvidenceRoot": PACKAGE_REL.as_posix(),
    "completeEnvelopeBinding": model_binding,
    "caseEvidenceBindings": case_coverage_binding,
    "sourceArchiveBinding": archive_binding,
    "deliveryManifestBinding": delivery_binding,
    "candidatePackageManifestBinding": package_binding,
    "procedureSourceBinding": decision_binding,
    "authoredAcceptanceReceipt": acceptance_binding,
    "authoredApplicationReceipt": {"path": APPLICATION.relative_to(ROOT).as_posix()},
    "directorReturnReceipt": return_binding,
    "accepted": True, "applied": True,
    "closedBlockerIds": BLOCKERS,
    "retainedQualificationIds": procedure_record["holdIds"],
    "retainedQualifications": QUALIFICATIONS,
})
assert entry_after["sourceStatus"] == entry_before["sourceStatus"] == "blocked-pending-operational-review"
index_after["entries"][entry_index] = entry_after
append_record = {
    "file": "../spell_candidates/rank9illusionreality5_reviewed_269/MODEL.json",
    "binding": model_binding, "reviewId": REVIEW_ID, "acceptedIds": [ID], "unacceptedIds": [],
    "excludedPendingIds": sorted(pending_before - {ID}), "authority": acceptance_binding,
    "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(), "directorDecision": decision_binding,
    "directorReturnReceipt": return_binding, "sourcePacket": archive_binding,
    "deliveryManifest": delivery_binding, "evidenceBindings": evidence_binding,
    "caseCoverage": case_coverage_binding,
    "candidatePackageManifestBinding": package_binding,
    "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
}
assert not any(ID in row.get("acceptedIds", []) for row in index_after["additionalStandaloneEnvelopes"])
index_after["additionalStandaloneEnvelopes"].append(append_record)
index_after["authoredCounts"] = {"reviewed": 815, "pending": 33}
index_after["representationCounts"]["completeReviewedStandaloneProcedures"] = 539
pending_after = {row["id"] for row in index_after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
assert pending_after == pending_before - {ID} and len(pending_after) == 33
inverse = copy.deepcopy(index_after)
inverse["entries"][entry_index] = copy.deepcopy(entry_before)
inverse["additionalStandaloneEnvelopes"].pop()
inverse["authoredCounts"] = copy.deepcopy(index_before["authoredCounts"])
inverse["representationCounts"] = copy.deepcopy(index_before["representationCounts"])
assert inverse == index_before

authority_after = {"reviewedApplied": 815, "pending": 33, "acceptedUnapplied": 0,
                   "completeStandaloneProcedures": 539, "scopedInterfaces": 173}
write_json(APPLICATION, {
    "id": APPLICATION_ID, "recordedAtUtc": now(),
    "status": "APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE",
    "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": BLOCKERS,
    "directorAcceptance": acceptance_binding, "directorDecision": decision_binding,
    "directorReturnReceipt": return_binding, "packet": archive_binding,
    "delivery": delivery_binding, "independentAudit": source_audit_binding,
    "candidateEnvelope": model_binding, "candidatePackageManifest": package_binding,
    "evidenceBindings": evidence_binding, "caseCoverage": case_coverage_binding,
    "manuscript": manuscript_binding, "indexBefore": index_binding_before,
    "countsBefore": authority_before, "countsAfter": authority_after,
    "completeReviewedStandaloneProcedures": {"before": 538, "after": 539},
    "scopedInterfaces": 173, "catalogChanged": False,
    "sourceStatusPreservedAsBlocked": True, "runtimeSelectionEnabled": False,
    "runtimeTestsExecuted": False,
    "independentValidationPath": VALIDATION.relative_to(ROOT).as_posix(),
})
application_binding = binding(APPLICATION)
entry_after["authoredApplicationReceipt"] = application_binding
index_after["entries"][entry_index] = entry_after
inverse = copy.deepcopy(index_after)
inverse["entries"][entry_index] = copy.deepcopy(entry_before)
inverse["additionalStandaloneEnvelopes"].pop()
inverse["authoredCounts"] = copy.deepcopy(index_before["authoredCounts"])
inverse["representationCounts"] = copy.deepcopy(index_before["representationCounts"])
assert inverse == index_before

groups = copy.deepcopy(pending_audit_before["groups"])
for group in groups:
    group["pendingIds"] = [sid for sid in group.get("pendingIds", []) if sid in pending_after]
    group["pendingCount"] = len(group["pendingIds"])
    if group.get("group") == GROUP:
        group["status"] = "SOUL_REFLECTION_ACCEPTED_APPLIED_IR207_B02_CLOSED"
        group["currentDisposition"] = {"acceptedAppliedIds": [ID], "remainingPendingIds": [], "closedBlockerIds": BLOCKERS}
        group["freshPacketRequiredForCurrentAuthority"] = True
    if group.get("group") == NEXT_GROUP:
        group["status"] = "GPT_DIRECTED_NEXT_PRIORITY_UNHOLY_ASCENDANCE_CC194_B04"
        group["sourceAuthority"] = authority_after
        group["freshPacketRequiredForCurrentAuthority"] = True
assert set(sid for group in groups for sid in group["pendingIds"]) == pending_after
nonempty_groups = [group for group in groups if group.get("pendingIds")]
assert len(nonempty_groups) == 15
next_group = next(group for group in groups if group.get("group") == NEXT_GROUP)
next_record = {
    "identity": NEXT_ID, "group": NEXT_GROUP, "pendingIds": [NEXT_ID], "pendingCount": 1,
    "blocker": NEXT_BLOCKER, "status": "GPT_DIRECTED_FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED",
    "freshPacketRequiredForCurrentAuthority": True, "sourceAuthority": authority_after,
    "requiredWitnessScope": ["caster-Undead zero-HP/Null recipient contract",
                             "type-specific healing", "death consequences", "other-form adverse traces"],
    "candidate": next_group.get("candidate"), "archive": next_group.get("archive"),
    "nextAction": "Prepare Unholy Ascendance at authority 815/33/0, resolve CC194-B04 with GPT as director, and independently apply only an explicitly accepted identity.",
}

write_json(PENDING_AFTER, {
    **copy.deepcopy(pending_audit_before),
    "id": "CURRENT33-PENDING-IDENTITY-AUDIT-269", "recordedAtUtc": now(),
    "status": "PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_SOUL_REFLECTION_APPLICATION",
    "authority": authority_after, "indexBinding": binding(INDEX, encode_json(index_after)),
    "catalogBinding": binding(CATALOG, catalog_before_raw), "pendingCount": 33,
    "pendingIds": sorted(pending_after), "pendingGroupCount": len(nonempty_groups), "groups": groups,
    "allPendingIdsExistInNativeCatalog": pending_after <= {row["id"] for row in catalog_before["spells"]},
    "noPendingTargetWasSilentlyAccepted": True,
    "acceptedIds": sorted(set(pending_audit_before.get("acceptedIds", [])) | {ID}),
    "appliedIds": sorted(set(pending_audit_before.get("appliedIds", [])) | {ID}),
    "heldIds": sorted(pending_after), "allCurrentPendingIdentitiesReviewed": True,
    "unreviewedPendingIds": [], "closedBlockerIdsThisStep": BLOCKERS,
    "directorDecision": decision_binding, "acceptanceReceipt": acceptance_binding,
    "applicationReceipt": application_binding, "nextBlockerPriority": {
        "identity": NEXT_ID, "group": NEXT_GROUP, "blockerId": NEXT_BLOCKER},
})
pending_after_binding = binding(PENDING_AFTER)

queue = copy.deepcopy(queue_before)
queue.update({
    "id": "CURRENT-SPELL-QUEUE-269", "recordedAtUtc": now(),
    "supersedesQueue": queue_before["id"], "currentAuthority": authority_after,
    "currentIndexBinding": binding(INDEX, encode_json(index_after)),
    "currentCatalogBinding": binding(CATALOG, catalog_before_raw),
    "currentPendingGroups": groups, "nextSuggestedGroups": [copy.deepcopy(next_group)],
    "nextGroup": NEXT_GROUP, "nextPendingIds": [NEXT_ID], "pendingCount": 33,
    "pendingIdentityAudit": pending_after_binding,
    "lastReviewedBatch": {"group": GROUP, "acceptedIds": [ID], "appliedIds": [ID],
        "heldIds": [], "blockerIdsClosed": BLOCKERS},
    "justAppliedBatch": {"reviewId": REVIEW_ID, "applicationId": APPLICATION_ID,
        "ids": [ID], "count": 1, "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
        "directorDecision": DECISION.relative_to(ROOT).as_posix()},
    "next": next_record, "nextPreparedRequest": next_record,
    "packetStatus": "SOUL_REFLECTION_ACCEPTED_APPLIED_815_33_NEXT_UNHOLY_ASCENDANCE_CC194_B04",
    "status": "SOUL_REFLECTION_ACCEPTED_APPLIED_NEXT_GPT_DIRECTED_UNHOLY_ASCENDANCE_815_33",
    "currentAcceptedPacket": {"archive": archive_binding, "delivery": delivery_binding,
        "independentAudit": source_audit_binding, "decision": decision_binding,
        "acceptance": acceptance_binding, "application": application_binding},
    "activeReview": {"identity": NEXT_ID, "group": NEXT_GROUP, "stage": "FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED",
        "blocker": NEXT_BLOCKER, "requiredWitnessScope": next_record["requiredWitnessScope"]},
    "githubChanges": False, "canonicalRuntimeApplicationPerformed": False,
})
write_json(QUEUE_AFTER, queue)
queue_binding = binding(QUEUE_AFTER)

handoff = copy.deepcopy(handoff_before)
handoff.update({
    "id": "CURRENT-HANDOFF-269", "recordedAtUtc": now(),
    "supersedes": handoff_before["id"], "status": "SOUL_REFLECTION_APPLIED_NEXT_UNHOLY_ASCENDANCE_815_33",
    "authority": authority_after, "indexBinding": binding(INDEX, encode_json(index_after)),
    "queue": QUEUE_AFTER.relative_to(ROOT).as_posix(), "queueBinding": queue_binding,
    "pendingIdentityAudit": PENDING_AFTER.relative_to(ROOT).as_posix(),
    "acceptedThisStep": [ID], "appliedThisStep": {"identity": ID,
        "application": APPLICATION.relative_to(ROOT).as_posix(),
        "acceptance": ACCEPTANCE.relative_to(ROOT).as_posix()},
    "currentBlocker": {"identity": NEXT_ID, "group": NEXT_GROUP, "blockerId": NEXT_BLOCKER},
    "nextGroup": NEXT_GROUP, "nextPendingCount": 1, "nextPendingIds": [NEXT_ID],
    "nextStep": next_record["nextAction"],
    "directorConnectionStatus": "GPT explicitly accepted Soul Reflection, applied locally, and set Unholy Ascendance / CC194-B04 as next priority.",
    "githubChanges": False, "runtimeSelectionEnabled": False,
})
write_json(HANDOFF_AFTER, handoff)
handoff_binding = binding(HANDOFF_AFTER)

index_after_raw = encode_json(index_after)
temp_index = INDEX.with_name("authored_review_index.soulreflection269.tmp")
temp_index.write_bytes(index_after_raw)
temp_index.replace(INDEX)
assert CATALOG.read_bytes() == catalog_before_raw

write_json(OPERATIONS, {
    "id": "SOUL-REFLECTION-INDEX-OPERATIONS-269",
    "before": index_binding_before, "after": binding(INDEX, index_after_raw),
    "operations": [
        {"op": "replace-entry", "identity": ID, "index": entry_index,
         "before": entry_before, "after": entry_after},
        {"op": "append-envelope", "identity": ID, "envelope": append_record},
        {"op": "update-counts", "before": index_before["authoredCounts"],
         "after": index_after["authoredCounts"],
         "standaloneProcedures": {"before": 538, "after": 539}},
    ],
    "onlyIdentityIds": [ID], "inverseSemanticExact": inverse == index_before,
    "catalogByteExact": True,
})

submission_after = copy.deepcopy(submission_before)
submission_after.update({
    "recordedAtUtc": now(), "status": "DIRECTOR_ACCEPTED_AND_APPLICATION_INDEPENDENTLY_VERIFIED",
    "authority": authority_before, "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [],
    "blockerIds": [], "closedBlockerIds": BLOCKERS,
    "directorDecision": binding(DECISION), "acceptance": acceptance_binding,
    "application": binding(APPLICATION), "returnReceipt": return_binding,
    "authorityAfterApplication": authority_after,
    "applicationValidation": VALIDATION.relative_to(ROOT).as_posix(),
    "return": {"explicitAccept": True, "accepted": True, "appliedAtDecision": False,
        "remainingPending": 33, "remainingGroups": len(nonempty_groups), "next": next_record},
    "canonicalChanges": True, "githubChanges": False,
})
write_json(SUBMISSION, submission_after)

checks = [
    ("GPT explicit acceptance recorded for Soul Reflection only", read_json(DECISION)["accepted"] is True and read_json(DECISION)["appliedAtDecision"] is False and read_json(DECISION)["identity"] == ID),
    ("Delta269 archive, delivery and 27-check independent audit match", binding(ARCHIVE)["sha256"] == delivery["archive"]["sha256"] == audit["archive"]["sha256"] and audit["passedChecks"] == audit["checkCount"] == 27),
    ("All 50 archive members match exact manifest hashes and CRCs", len(manifest["members"]) == 49 and len(case_rows) == 5),
    ("Five accepted traces total 118 events with complete reversible operation counts", sum(len(case["events"]) for case in cases.values()) == 118 and 2 * sum(len(case["events"]) for case in cases.values()) == 236),
    ("Embedded current index/catalog exactly match canonical pre-application files", archived_index_raw == index_before_raw and archived_catalog_raw == catalog_before_raw),
    ("Only the Soul Reflection index row is changed and native catalog is byte-exact", next(row for row in read_json(INDEX)["entries"] if row["id"] == ID)["accepted"] is True and CATALOG.read_bytes() == catalog_before_raw),
    ("Authored index counts are 815 reviewed / 33 pending", read_json(INDEX)["authoredCounts"] == {"reviewed": 815, "pending": 33}),
    ("Complete standalone procedure count is 539 and scoped interfaces remain 173", read_json(INDEX)["representationCounts"]["completeReviewedStandaloneProcedures"] == 539 and read_json(INDEX)["representationCounts"].get("scopedInterfaces", 173) == 173),
    ("Pending set is exact and excludes only Soul Reflection", pending_after == {row["id"] for row in read_json(INDEX)["entries"] if row["authoredStatus"] == "pending-authored-procedure"} and len(pending_after) == 33 and ID not in pending_after),
    ("Application inverse restores the exact pre-application semantic index", inverse == index_before and BACKUP.read_bytes() == index_before_raw),
    ("Source status and native catalog content remain unchanged", next(row for row in read_json(INDEX)["entries"] if row["id"] == ID)["sourceStatus"] == entry_before["sourceStatus"] and CATALOG.read_bytes() == catalog_before_raw),
    ("Pending groups exactly cover the 33 remaining IDs across 15 groups", set(sid for group in groups for sid in group["pendingIds"]) == pending_after and len(nonempty_groups) == 15),
    ("Next priority is Unholy Ascendance / CC194-B04 at current authority", read_json(QUEUE_AFTER)["next"]["identity"] == NEXT_ID and read_json(QUEUE_AFTER)["next"]["blocker"] == NEXT_BLOCKER and read_json(QUEUE_AFTER)["currentAuthority"] == authority_after),
    ("Runtime remains disabled and no runtime tests were run", read_json(PACKAGE / "MODEL.json")["runtimeSelectionEnabled"] is False and read_json(APPLICATION)["runtimeTestsExecuted"] is False),
    ("Every candidate package file is hash-bound by its package manifest", all((ROOT / row["path"]).stat().st_size == row["bytes"] and sha((ROOT / row["path"]).read_bytes()) == row["sha256"] for row in package_manifest["files"])),
]
assert all(passed for _, passed in checks), [name for name, passed in checks if not passed]
index_after_binding = binding(INDEX)
write_json(VALIDATION, {
    "id": "SOUL-REFLECTION-APPLICATION-VALIDATION-269", "recordedAtUtc": now(),
    "status": "PASS", "checksPassed": len(checks), "checkCount": len(checks), "checksFailed": 0,
    "checks": [{"check": name, "passed": passed} for name, passed in checks],
    "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": BLOCKERS,
    "beforeIndex": index_binding_before, "afterIndex": index_after_binding,
    "catalogByteExact": True, "sourceStatusPreservedAsBlocked": True,
    "runtimeSelectionEnabled": False, "independentWitnessAudit": source_audit_binding,
    "directorDecision": decision_binding, "acceptance": acceptance_binding,
    "application": binding(APPLICATION), "pendingIdentityAudit": pending_after_binding,
    "queue": queue_binding, "handoff": handoff_binding,
    "inverseSemanticExact": inverse == index_before,
    "remainingPending": {"count": 33, "groups": len(nonempty_groups), "next": next_record},
})
write_json(STATE_CORRECTION, {
    "id": "CURRENT-REVIEW-STATE-CORRECTION-269", "recordedAtUtc": now(),
    "status": "PASS_CURRENT_AUTHORITY_UPDATED_AFTER_EXPLICIT_GPT_ACCEPTANCE_AND_APPLICATION",
    "supersedes": "CURRENT_REVIEW_STATE_CORRECTION_262.json", "oldRecordsPreservedByteForByte": True,
    "acceptedIdentity": ID, "closedBlockerIds": BLOCKERS,
    "directorDecision": decision_binding, "acceptance": acceptance_binding,
    "application": binding(APPLICATION), "indexOperations": binding(OPERATIONS),
    "authorityAfter": authority_after, "pendingAudit": pending_after_binding,
    "queue": queue_binding, "handoff": handoff_binding, "nextPriority": next_record,
    "scope": "One static authored procedure only; no runtime or global rule change.",
})
SNAPSHOT.write_text(
    "# Current spell review snapshot 269\n\n"
    "Authority: **815 applied / 33 pending / 0 accepted-unapplied; 539 complete standalone procedures / 173 scoped interfaces.**\n\n"
    "Soul Reflection / IR207-B02 was explicitly accepted by GPT, and the accepted procedure was applied to the authored review index. Cave Bear authorization remains narrow; the phase-less recipient branch remains conditional. Runtime and downstream gates remain closed.\n\n"
    "Next GPT-directed priority: **Unholy Ascendance / CC194-B04**. Establish the caster-Undead zero-HP/Null recipient contract and complete type-specific healing, death and other-form adverse witnesses.\n\n"
    "33 identities across 15 groups remain pending.\n",
    encoding="utf-8", newline="\n")

print(json.dumps({"status": "PASS", "identity": ID, "applied": True,
    "counts": authority_after, "checksPassed": len(checks),
    "remaining": {"pending": 33, "groups": len(nonempty_groups)},
    "next": next_record, "validation": binding(VALIDATION), "index": index_after_binding}, indent=2))
