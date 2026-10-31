from __future__ import annotations

import copy
import hashlib
import io
import json
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
PACKET = A / "DD_Rank9_MatterConversion_MF210-B02_Supplement_261.zip"
DELIVERY = A / "DD_Rank9_MatterConversion_MF210-B02_Supplement_261_DELIVERY.json"
WITNESS_DIR = A / "matter_conversion_witnesses_261"
PACKAGE_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/matterconversion_reviewed_262")
PACKAGE = ROOT / PACKAGE_REL
MANUSCRIPT = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/MATTER_CONVERSION_REVIEWED_262.md"

DECISION = A / "MATTER_CONVERSION_DIRECTOR_DECISION_262.json"
ACCEPTANCE = A / "MATTER_CONVERSION_EXACT_ACCEPTANCE_262.json"
RETURN_RECEIPT = A / "MATTER_CONVERSION_RETURN261_RECEIPT.json"
APPLICATION = A / "MATTER_CONVERSION_APPLICATION_262.json"
OPERATIONS = A / "MATTER_CONVERSION_INDEX_OPERATIONS_262.json"
BACKUP = A / "authored_review_index.before_matterconversion_262.json"
PENDING_AUDIT = A / "CURRENT34_PENDING_IDENTITY_AUDIT_262.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_262.json"
HANDOFF = A / "CURRENT_HANDOFF_262.json"
STATE_CORRECTION = A / "CURRENT_REVIEW_STATE_CORRECTION_262.json"
VALIDATION = A / "MATTER_CONVERSION_APPLICATION_VALIDATION_262.json"
SNAPSHOT = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_262.md"
SUBMISSION = A / "RANK9MATERIALFORGING2_PACKET_261_SUBMISSION.json"

ID = "matter-conversion"
GROUP = "rank9-material-forging2"
NEXT_ID = "soul-reflection"
NEXT_GROUP = "rank9-illusion-reality5"
BLOCKER = "MF210-B02"
NEXT_BLOCKER = "IR207-B02"
REVIEW_ID = "RANK9-MATERIALFORGING2-MATTER-CONVERSION-EXACT-AUTHORED-ACCEPTANCE-262"
APPLICATION_ID = "RANK9-MATERIALFORGING2-MATTER-CONVERSION-APPLICATION-262"
GPT_URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"

KERNELS = [
    "MF210-M-mithril-profile",
    "MF210-M-hostile-custody",
    "MF210-M-magical-input",
    "MF210-M-reserved-lot",
    "MF210-M-unknown-material",
    "MF210-M-late-fit",
    "MF210-M-instantaneous",
]
RETAINED_QUALIFICATIONS = [
    "The seven historical conversion kernels remain conditional; Packet261's two integrated witnesses close MF210-B02 only for the expressly authorized bounded fixtures.",
    "The bounded material profiles, station, buyer, quote, reserve and ownership/custody allocations are fixture parameters, not universal material rules or guaranteed campaign markets.",
    "No universal mithril density, AC, durability, recipe equivalence, market price beyond the authorized quote, or automatic assay is established.",
    "The authorizationFrozen cast claim is spell-local and distinct from the custody/work reservation; no global reservation interface is added.",
    "Matter Conversion remains runtime-disabled; no implementation, human-play, balance, cosmology, domain-closure, completion or release approval is implied.",
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


def bind(path: Path, raw: bytes | None = None) -> dict:
    value = path.read_bytes() if raw is None else raw
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(value),
        "sha256": sha(value),
        "crc32": f"{zlib.crc32(value) & 0xFFFFFFFF:08x}",
    }


def bind_member(label: str, raw: bytes) -> dict:
    return {"path": label, "bytes": len(raw), "sha256": sha(raw), "crc32": f"{zlib.crc32(raw) & 0xFFFFFFFF:08x}"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


outputs = [PACKAGE, MANUSCRIPT, DECISION, ACCEPTANCE, RETURN_RECEIPT, APPLICATION, OPERATIONS,
           BACKUP, PENDING_AUDIT, QUEUE, HANDOFF, STATE_CORRECTION, VALIDATION, SNAPSHOT]
assert all(not path.exists() for path in outputs), "Refuse to overwrite an existing Matter Conversion application artifact"

packet_raw = PACKET.read_bytes()
packet_sha = sha(packet_raw)
delivery = read_json(DELIVERY)
assert len(packet_raw) == 7_626_583
assert packet_sha == "9d092e47f2d792ba3d1a0222b50d8b41800dd21b2f941d302d5160672a7fc500"
assert packet_sha == delivery["archive"]["sha256"] and len(packet_raw) == delivery["archive"]["bytes"]

audit_path = WITNESS_DIR / "MATTER_CONVERSION_INDEPENDENT_AUDIT_261.json"
replay_path = WITNESS_DIR / "CASE_REPLAY_261.json"
w1_path = WITNESS_DIR / "MF259-M-W1.json"
w2_path = WITNESS_DIR / "MF259-M-W2.json"
audit = read_json(audit_path)
replay = read_json(replay_path)
assert audit["status"] == "PASS" and audit["passedChecks"] == audit["checkCount"] == 60
assert audit["failedChecks"] == 0
assert audit["counts"]["newForwardOperations"] == audit["counts"]["newInverseOperations"] == 60
assert audit["counts"]["newEvents"] == 30 and audit["counts"]["newIntegratedCases"] == 2
assert audit["counts"]["newForwardOperations"] == audit["counts"]["newInverseOperations"] == 60

# The original director-preserved procedure is embedded in Return247, itself nested in corrected Packet260.
with zipfile.ZipFile(PACKET) as packet_zip:
    assert packet_zip.testzip() is None
    corrected_raw = packet_zip.read("payload/DD_Rank9_MatterConversion_MF210-B02_Supplement_260_corrected.zip")
    with zipfile.ZipFile(io.BytesIO(corrected_raw)) as corrected_zip:
        held_raw = corrected_zip.read("payload/prior/Return247_HELD.zip")
        with zipfile.ZipFile(io.BytesIO(held_raw)) as held_zip:
            procedure_raw = held_zip.read("PROCEDURES.json")
            procedures = json.loads(procedure_raw)
            source_procedure = next(row for row in procedures if row.get("id") == ID)
            source_hold_register = json.loads(held_zip.read("HOLD_REGISTER.json"))
assert source_procedure["id"] == ID and source_procedure["accepted"] is False and source_procedure["applied"] is False
assert len(KERNELS) == 7

index_before_raw = INDEX.read_bytes()
catalog_before_raw = CATALOG.read_bytes()
index_before = read_json(INDEX)
catalog_before = read_json(CATALOG)
queue_before = read_json(A / "CURRENT_SPELL_QUEUE_261.json")
pending_audit_before = read_json(A / "CURRENT35_PENDING_IDENTITY_AUDIT_257.json")
submission_before = read_json(SUBMISSION)
assert index_before["authoredCounts"] == {"reviewed": 813, "pending": 35}
assert index_before["representationCounts"]["completeReviewedStandaloneProcedures"] == 537
assert index_before["representationCounts"].get("scopedInterfaces", 173) == 173
assert queue_before["currentAuthority"] == {
    "reviewedApplied": 813, "pending": 35, "acceptedUnapplied": 0,
    "completeStandaloneProcedures": 537, "scopedInterfaces": 173,
}
assert submission_before["status"] == "SUBMITTED_AWAITING_DIRECTOR_RESPONSE"
assert submission_before["archive"]["sha256"] == packet_sha
entry_index = next(i for i, row in enumerate(index_before["entries"]) if row["id"] == ID)
entry_before = copy.deepcopy(index_before["entries"][entry_index])
pending_before = {row["id"] for row in index_before["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
assert len(pending_before) == 35 and ID in pending_before
assert set(pending_audit_before["pendingIds"]) == pending_before
assert pending_audit_before["indexBinding"]["sha256"] == sha(index_before_raw)
assert entry_before["authoredStatus"] == "pending-authored-procedure"
assert entry_before["sourceStatus"] == "blocked-pending-operational-review"
assert entry_before["wholeCardPointer"] == "/spells/768"
assert catalog_before["spells"][768]["id"] == ID

director_acceptance_response = """ACCEPT — matter-conversion: accepted=true, applied=false. MF210-B02 is closed.
Acceptance covers the preserved Matter Conversion procedure, the expressly authorized bounded fixtures, and Supplement261’s two integrated witnesses. It accepts no other pending identity and changes no canonical file.
Verified archive: 7,626,583 bytes, SHA-256 9d092e47f2d792ba3d1a0222b50d8b41800dd21b2f941d302d5160672a7fc500.
My independent checks confirm: 13 archive members / 12 bound payloads, with matching sizes, hashes and CRCs; embedded corrected Packet260 has 28 members / 27 bound payloads, including REQUEST.txt, with preserved non-manifest contents matching Packet259; both actor profiles match Return247; 30 events, 60 forward operations and 60 inverse operations pass hashes, continuity and complete reverse traversal; scheduled starts/ends, Action expenditure, 64→38 RP, prepared-family history and zero Dissonance/Refrain are consistent, with no incidental recovery.
MF247-M-W1: exact 1 lb stone→1 lb mithril conversion; input retired once; finite sale settles before expiry; reserve 300→50 gp, with 250 gp owned by A under B’s recorded custody. Total coins remain unchanged; repeated settlement pays nothing.
MF247-M-W2: active work reservation rejects preflight without payment; B releases it on B’s turn; A commits against the updated revision. Exact 143/32 lb persists, the corner remains absent, and 6/10→4/8 HP preserves the four-point deficit. Body identity, ownership and custody remain intact; the ordinary glass result persists.
For these fixtures, /pendingCasts/*/authorizationFrozen is accepted as the cast’s exclusive target/quantity claim, separate from B’s custody/work reservation. Both traces contain one committed claim and no conflicting active work hold at resolution. This is a representation clarification, not a new global reservation interface.
The seven prior kernels remain conditional. The authored material profiles, buyer, quote and station remain bounded fixtures; this acceptance establishes no universal mithril profile, recipe equivalence or guaranteed market.
Authority remains 813 applied / 35 pending / 0 accepted-unapplied in the unchanged canonical snapshot, with 537 procedures / 173 interfaces. This decision creates one acceptance awaiting independent application. After exact application, the expected snapshot is 814 applied / 34 pending / 0 accepted-unapplied, with 538 procedures / 173 interfaces.
Next priority: soul-reflection / IR207-B02. Eternal Forge and Unravel Identity remain closed. All unrelated holds and runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates remain unchanged."""

remaining_work_response = """ACCEPT — matter-conversion / MF210-B02. accepted=true; applied=false; acceptedIds=[\"matter-conversion\"]. MF210-B02 is closed.
Packet261’s two integrated witnesses pass the source, semantic, clock, conservation, custody, damage and reservation checks, plus 30 events / 60 forward operations / 60 inverse operations. Acceptance includes the bounded director-authored fixtures; the seven historical kernels remain conditional. No other identity is accepted.
Until you independently apply this acceptance, canonical authority remains 813 applied / 35 pending / 0 accepted-unapplied, with 537 procedures / 173 interfaces. After exact application, the expected counts are 814 applied / 34 pending / 0 accepted-unapplied, with 538 procedures / 173 interfaces.
Next pending identity: soul-reflection / IR207-B02. Prepare the missing changed-form, attached/no-phase recipient lifecycle witnesses, including original-target zero/death settlement, copied concentration ending, and actual original cargo entrusted to the reflection.
Remaining work: no identity awaits its first review. The other 34 identities across 16 groups need their specific retained blockers closed, followed by independent acceptance/application checks. After Soul Reflection, prioritize unholy-ascendance / CC194-B04, especially its caster-Undead zero-HP/Null recipient contract and healing/death/form branches.
Eternal Forge and Unravel Identity remain closed. All unrelated holds and runtime, implementation, human-play, balance, cosmology, domain-closure, completion and release gates remain unchanged."""

source_outer = bind(PACKET)
source_delivery = bind(DELIVERY)
source_cases = {
    "w1": bind(w1_path),
    "w2": bind(w2_path),
    "replay": bind(replay_path),
    "audit": bind(audit_path),
    "authorization": bind(A / "MATTER_CONVERSION_DIRECTOR_FIXTURE_AUTHORIZATION_260.json"),
    "preservedReturn247Archive": bind_member(
        "DD_Rank9_MatterConversion_MF210-B02_Supplement_261.zip!payload/DD_Rank9_MatterConversion_MF210-B02_Supplement_260_corrected.zip!payload/prior/Return247_HELD.zip",
        held_raw,
    ),
    "preservedProcedureRecord": bind_member(
        "DD_Rank9_MatterConversion_MF210-B02_Supplement_261.zip!payload/DD_Rank9_MatterConversion_MF210-B02_Supplement_260_corrected.zip!payload/prior/Return247_HELD.zip!PROCEDURES.json#matter-conversion",
        procedure_raw,
    ),
}

write_json(DECISION, {
    "id": "MATTER-CONVERSION-GPT-DIRECTOR-DECISION-262",
    "recordedAtUtc": now(),
    "decision": "EXACT_ACCEPT",
    "identity": ID,
    "group": GROUP,
    "closedBlockerIds": [BLOCKER],
    "accepted": True,
    "appliedAtDecision": False,
    "countsAtDecision": {"reviewedApplied": 813, "pending": 35, "acceptedUnapplied": 0,
                          "completeStandaloneProcedures": 537, "scopedInterfaces": 173},
    "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": GPT_URL},
    "packet": source_outer,
    "deliveryManifest": source_delivery,
    "independentWitnessAudit": source_cases["audit"],
    "exactAcceptanceResponse": director_acceptance_response,
    "followupRemainingWorkResponse": remaining_work_response,
    "acceptedScope": "The preserved Matter Conversion authored procedure and exactly the two bounded integrated witnesses W1/W2 in Packet261; one identity only.",
    "retainedConditionalKernels": KERNELS,
    "retainedQualifications": RETAINED_QUALIFICATIONS,
    "nextPriority": {"identity": NEXT_ID, "group": NEXT_GROUP, "blocker": NEXT_BLOCKER,
                     "requiredWitnessScope": ["changed-form attached/no-phase recipient lifecycle",
                                              "original-target zero/death settlement",
                                              "copied concentration ending",
                                              "actual original cargo entrusted to the reflection"]},
    "remainingQueue": {"pendingIdentityCount": 34, "pendingGroupCount": 16,
                        "allPendingIdentitiesHaveReceivedFirstReview": True,
                        "nextAfterSoulReflection": {"identity": "unholy-ascendance", "blocker": "CC194-B04",
                                                   "focus": "caster-Undead zero-HP/Null recipient contract and healing/death/form branches"}},
    "gatesStillClosed": ["runtime", "implementation", "human-play", "balance", "cosmology", "domain-closure", "completion", "release"],
})
decision_binding = bind(DECISION)

procedure_record = copy.deepcopy(source_procedure)
procedure_record.update({
    "status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
    "accepted": True,
    "applied": False,
    "closedBlockerIds": [BLOCKER],
    "retainedConditionalKernelIds": KERNELS,
    "retainedQualifications": RETAINED_QUALIFICATIONS,
    "currentIndexEntryBeforeApplication": entry_before,
    "directorDecisionBinding": decision_binding,
    "packet261Binding": source_outer,
    "deliveryManifestBinding": source_delivery,
    "witnessBindings": source_cases,
    "sourceProcedureMemberBinding": source_cases["preservedProcedureRecord"],
    "scope": "Matter Conversion only. Accepted evidence proves the two fixture encounters and does not create a universal material profile, recipe interface, market rule or global reservation interface.",
})

case_coverage = {
    "id": "MATTER-CONVERSION-CASE-COVERAGE-262",
    "sourceProcedure": source_cases["preservedProcedureRecord"],
    "witnessCases": [
        {"id": "MF247-M-W1", "source": source_cases["w1"],
         "acceptedResult": "1 lb stone converted to 1 lb mithril; finite sale settles 250 gp from B's 300 gp reserve to A before quote expiry; input retires exactly once; custody and coin totals reconcile."},
        {"id": "MF247-M-W2", "source": source_cases["w2"],
         "acceptedResult": "Active custody/work hold rejects preflight without payment; release on B's turn; A's next legal cast preserves 143/32 lb, missing corner, HP deficit, identity, ownership and custody, then ordinary glass persists."},
    ],
    "replay": source_cases["replay"],
    "independentAudit": source_cases["audit"],
    "events": 30,
    "forwardOperations": 60,
    "inverseOperations": 60,
    "conditionalKernelIds": KERNELS,
    "boundedFixturesOnly": True,
}

evidence_bindings = {
    "id": "MATTER-CONVERSION-ACCEPTED-EVIDENCE-262",
    "directorDecision": decision_binding,
    "packet": source_outer,
    "deliveryManifest": source_delivery,
    "witnesses": source_cases,
    "conditionalKernelIds": KERNELS,
    "retainedQualifications": RETAINED_QUALIFICATIONS,
}

PACKAGE.mkdir(parents=True)
write_json(PACKAGE / "DIRECTOR_DECISION.json", read_json(DECISION))
write_json(PACKAGE / "PROCEDURE_RECORD.json", procedure_record)
write_json(PACKAGE / "CASE_COVERAGE.json", case_coverage)
write_json(PACKAGE / "EVIDENCE_BINDINGS.json", evidence_bindings)
write_json(PACKAGE / "RETAINED_QUALIFICATIONS.json", {
    "identity": ID, "closedBlockerIds": [BLOCKER], "conditionalKernelIds": KERNELS,
    "qualifications": RETAINED_QUALIFICATIONS,
})

procedure_content = "\n\n".join(
    [f"{name}: {value}" for name, value in source_procedure["sharedProcedure"].items()]
    + [f"{name}: {value}" for name, value in source_procedure["spellLocalNEW"].items()]
)
model = {
    "schemaVersion": 1,
    "moduleId": "matterconversion-reviewed-262",
    "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
    "scope": "Matter Conversion only; exactly two bounded authorized integrated fixture witnesses accepted; historical kernels and broader claims remain conditional.",
    "acceptedIds": [ID],
    "unacceptedIds": [],
    "excludedPendingIds": sorted(pending_before - {ID}),
    "unresolvedQualifications": {ID: RETAINED_QUALIFICATIONS},
    "sharedRequirements": {
        "scope": "No global/shared interface changes. The authorizationFrozen target/quantity claim is accepted only as the cast-local representation described by GPT; runtime selection stays disabled.",
        "rules": source_procedure["sharedProcedure"],
        "runtimeSelectionEnabled": False,
    },
    "spells": [{
        "id": ID,
        "name": entry_before["name"],
        "position": 0,
        "procedure": {
            "id": "MF247-STATIC-MATTER-CONVERSION",
            "spellId": ID,
            "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
            "accepted": True,
            "applied": False,
            "nativeCardUnchanged": copy.deepcopy(source_procedure["nativeSourceUnchanged"]["completeCurrentCatalogSourceAndAccess"]),
            "procedureContent": procedure_content,
            "sharedRequirements": copy.deepcopy(source_procedure["sharedProcedure"]),
            "spellLocalRequirements": copy.deepcopy(source_procedure["spellLocalNEW"]),
            "qualifications": RETAINED_QUALIFICATIONS,
            "retainedQualificationIds": ["MF210-KERNELS-CONDITIONAL", "MF210-BOUNDED-FIXTURES"],
            "retainedConditionalKernelIds": KERNELS,
            "closedBlockerIds": [BLOCKER],
            "directorDecisionId": "MATTER-CONVERSION-GPT-DIRECTOR-DECISION-262",
            "directorDecisionBinding": decision_binding,
            "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
            "caseCoverageFile": "CASE_COVERAGE.json",
        },
        "directorProcedureRecord": procedure_record,
        "nativeCardUnchanged": copy.deepcopy(source_procedure["nativeSourceUnchanged"]["completeCurrentCatalogSourceAndAccess"]),
        "caseIds": ["MF247-M-W1", "MF247-M-W2"],
        "holdIds": KERNELS,
        "runtimeSelectionEnabled": False,
    }],
    "caseCoverage": {"caseCount": 2, "caseIds": ["MF247-M-W1", "MF247-M-W2"], "file": "CASE_COVERAGE.json"},
    "evidenceBindings": {"file": "EVIDENCE_BINDINGS.json"},
    "directorDecision": decision_binding,
    "sourcePacket": source_outer,
    "runtimeSelectionEnabled": False,
    "runtimeTestsExecuted": False,
    "implementationApproved": False,
    "humanPlaytested": False,
    "balanceApproved": False,
    "cosmologyModified": False,
    "releaseApproved": False,
    "domainClosure": False,
}
write_json(PACKAGE / "MODEL.json", model)

manuscript = (
    "# Matter Conversion — accepted static authored procedure 262\n\n"
    "GPT explicitly accepted Matter Conversion / MF210-B02 for the preserved procedure and two expressly authorized bounded fixtures. "
    "This index application does not enable runtime use or adopt universal mithril/material/economy rules.\n\n"
    "## Preserved native card and access\n\n"
    + json.dumps(procedure_record["nativeSourceUnchanged"]["completeCurrentCatalogSourceAndAccess"], ensure_ascii=False, indent=2)
    + "\n\n## Shared procedure and spell-local completion\n\n"
    + procedure_content
    + "\n\n## Accepted witness scope\n\n"
    + "MF247-M-W1 and MF247-M-W2 only. Seven earlier conversion kernels remain conditional. The accepted market, materials, station and ownership values are bounded fixture parameters.\n\n"
    + "## Retained qualifications\n\n"
    + "\n".join(f"- {item}" for item in RETAINED_QUALIFICATIONS)
    + "\n"
)
PACKAGE.joinpath("STANDALONE_PROCEDURES.md").write_text(manuscript, encoding="utf-8", newline="\n")
MANUSCRIPT.parent.mkdir(parents=True, exist_ok=True)
MANUSCRIPT.write_text(manuscript, encoding="utf-8", newline="\n")

package_manifest = {"id": "MATTER-CONVERSION-PACKAGE-MANIFEST-262", "decision": decision_binding, "sourcePacket": source_outer, "files": []}
for path in sorted(item for item in PACKAGE.rglob("*") if item.is_file() and item.name != "CANDIDATE_PACKAGE_MANIFEST.json"):
    package_manifest["files"].append({
        "path": (PACKAGE_REL / path.relative_to(PACKAGE)).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha(path.read_bytes()),
    })
write_json(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json", package_manifest)

model_binding = bind(PACKAGE / "MODEL.json")
package_binding = bind(PACKAGE / "CANDIDATE_PACKAGE_MANIFEST.json")
evidence_binding = bind(PACKAGE / "EVIDENCE_BINDINGS.json")
coverage_binding = bind(PACKAGE / "CASE_COVERAGE.json")
manuscript_binding = bind(MANUSCRIPT)

write_json(ACCEPTANCE, {
    "id": REVIEW_ID,
    "recordedAtUtc": now(),
    "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED",
    "acceptedIds": [ID],
    "appliedIds": [],
    "closedBlockerIds": [BLOCKER],
    "retainedQualificationIds": ["MF210-KERNELS-CONDITIONAL", "MF210-BOUNDED-FIXTURES"],
    "retainedConditionalKernelIds": KERNELS,
    "directorDecision": decision_binding,
    "packet": source_outer,
    "delivery": source_delivery,
    "independentAudit": source_cases["audit"],
    "candidateEnvelope": model_binding,
    "candidatePackageManifest": package_binding,
    "evidenceBindings": evidence_binding,
    "caseCoverage": coverage_binding,
    "countsBefore": {"reviewed": 813, "pending": 35, "acceptedUnapplied": 0},
    "countsAfterAcceptanceBeforeApplication": {"reviewed": 813, "pending": 34, "acceptedUnapplied": 1},
    "scope": "Static Matter Conversion procedure only; exactly MF247-M-W1/W2 bounded fixtures; runtime and shared rules unchanged.",
})
acceptance_binding = bind(ACCEPTANCE)
write_json(RETURN_RECEIPT, {
    "id": "MATTER-CONVERSION-RETURN261-RECEIPT",
    "recordedAtUtc": now(),
    "status": "EXACT_ACCEPT_MATTER_CONVERSION",
    "acceptedIds": [ID],
    "appliedIds": [],
    "closedBlockerIds": [BLOCKER],
    "retainedConditionalKernelIds": KERNELS,
    "directorDecision": decision_binding,
    "acceptance": acceptance_binding,
    "packet": source_outer,
    "delivery": source_delivery,
    "nextPriority": {"identity": NEXT_ID, "group": NEXT_GROUP, "blocker": NEXT_BLOCKER},
})
return_binding = bind(RETURN_RECEIPT)

shutil_backup = index_before_raw
BACKUP.write_bytes(shutil_backup)
assert BACKUP.read_bytes() == index_before_raw
index_after = copy.deepcopy(index_before)
entry_after = copy.deepcopy(entry_before)
entry_after.update({
    "authoredStatus": "reviewed-authored-operational-playtest",
    "procedureFile": "../spell_candidates/matterconversion_reviewed_262/MODEL.json",
    "procedurePointer": "/spells/0/procedure",
    "wholeCardPointer": "/spells/0",
    "wholeCardIdField": "id",
    "sourceCatalogWholeCardPointer": entry_before.get("sourceCatalogWholeCardPointer") or entry_before["wholeCardPointer"],
    "procedureTextPointer": "/spells/0/procedure/procedureContent",
    "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
    "sharedRulesPointer": "/spells/0/procedure/sharedRequirements",
    "spellLocalRequirementsPointer": "/spells/0/procedure/spellLocalRequirements",
    "manuscript": "../../../docs/spells/candidates/MATTER_CONVERSION_REVIEWED_262.md",
    "reviewId": APPLICATION_ID,
    "runtimeSelectionEnabled": False,
    "historicalCandidateLabelsPreserved": True,
    "completeEvidenceRoot": PACKAGE_REL.as_posix(),
    "completeEnvelopeBinding": model_binding,
    "caseEvidenceBindings": coverage_binding,
    "sourceArchiveBinding": source_outer,
    "deliveryManifestBinding": source_delivery,
    "candidatePackageManifestBinding": package_binding,
    "procedureSourceBinding": decision_binding,
    "authoredAcceptanceReceipt": acceptance_binding,
    "authoredApplicationReceipt": {"path": APPLICATION.relative_to(ROOT).as_posix()},
    "directorReturnReceipt": return_binding,
    "accepted": True,
    "applied": True,
    "closedBlockerIds": [BLOCKER],
    "retainedQualificationIds": ["MF210-KERNELS-CONDITIONAL", "MF210-BOUNDED-FIXTURES"],
    "retainedConditionalKernelIds": KERNELS,
})
assert entry_after["sourceStatus"] == entry_before["sourceStatus"] == "blocked-pending-operational-review"
index_after["entries"][entry_index] = entry_after
append_record = {
    "file": "../spell_candidates/matterconversion_reviewed_262/MODEL.json",
    "binding": model_binding,
    "reviewId": REVIEW_ID,
    "acceptedIds": [ID],
    "unacceptedIds": [],
    "excludedPendingIds": sorted(pending_before - {ID}),
    "authority": acceptance_binding,
    "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
    "directorDecision": decision_binding,
    "directorReturnReceipt": return_binding,
    "sourcePacket": source_outer,
    "deliveryManifest": source_delivery,
    "evidenceBindings": evidence_binding,
    "caseCoverage": coverage_binding,
    "candidatePackageManifestBinding": package_binding,
    "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
}
assert not any(ID in row.get("acceptedIds", []) for row in index_after["additionalStandaloneEnvelopes"])
index_after["additionalStandaloneEnvelopes"].append(append_record)
index_after["authoredCounts"] = {"reviewed": 814, "pending": 34}
index_after["representationCounts"]["completeReviewedStandaloneProcedures"] = 538
pending_after = {row["id"] for row in index_after["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
assert pending_after == pending_before - {ID} and len(pending_after) == 34

inverse = copy.deepcopy(index_after)
inverse["entries"][entry_index] = copy.deepcopy(entry_before)
inverse["additionalStandaloneEnvelopes"].pop()
inverse["authoredCounts"] = copy.deepcopy(index_before["authoredCounts"])
inverse["representationCounts"] = copy.deepcopy(index_before["representationCounts"])
assert inverse == index_before

write_json(APPLICATION, {
    "id": APPLICATION_ID,
    "recordedAtUtc": now(),
    "status": "APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE",
    "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER],
    "retainedConditionalKernelIds": KERNELS,
    "directorAcceptance": acceptance_binding, "directorDecision": decision_binding,
    "directorReturnReceipt": return_binding, "packet": source_outer,
    "delivery": source_delivery, "independentAudit": source_cases["audit"],
    "candidateEnvelope": model_binding, "candidatePackageManifest": package_binding,
    "evidenceBindings": evidence_binding, "caseCoverage": coverage_binding,
    "manuscript": manuscript_binding,
    "indexBefore": bind(BACKUP, index_before_raw),
    "countsBefore": {"reviewed": 813, "pending": 35, "acceptedUnapplied": 0},
    "countsAfter": {"reviewed": 814, "pending": 34, "acceptedUnapplied": 0},
    "completeReviewedStandaloneProcedures": {"before": 537, "after": 538},
    "scopedInterfaces": 173,
    "catalogChanged": False,
    "sourceStatusPreservedAsBlocked": True,
    "runtimeSelectionEnabled": False,
    "runtimeTestsExecuted": False,
    "independentValidationPath": VALIDATION.relative_to(ROOT).as_posix(),
})
application_binding = bind(APPLICATION)
entry_after["authoredApplicationReceipt"] = application_binding
index_after["entries"][entry_index] = entry_after
inverse = copy.deepcopy(index_after)
inverse["entries"][entry_index] = copy.deepcopy(entry_before)
inverse["additionalStandaloneEnvelopes"].pop()
inverse["authoredCounts"] = copy.deepcopy(index_before["authoredCounts"])
inverse["representationCounts"] = copy.deepcopy(index_before["representationCounts"])
assert inverse == index_before

catalog_binding = bind(CATALOG, catalog_before_raw)
authority_after = {"reviewedApplied": 814, "pending": 34, "acceptedUnapplied": 0,
                   "completeStandaloneProcedures": 538, "scopedInterfaces": 173}
groups = copy.deepcopy(queue_before["currentPendingGroups"])
for group in groups:
    remaining = [spell_id for spell_id in group["pendingIds"] if spell_id in pending_after]
    group["pendingIds"] = remaining
    group["pendingCount"] = len(remaining)
    if group["group"] == GROUP:
        group["status"] = "MATTER_CONVERSION_ACCEPTED_APPLIED_MF210_B02_CLOSED"
        group["currentDisposition"] = {"acceptedAppliedIds": [ID], "remainingPendingIds": [], "closedBlockerIds": [BLOCKER]}
        group["freshPacketRequiredForCurrentAuthority"] = True
    if group["group"] == NEXT_GROUP:
        group["status"] = "GPT_DIRECTED_NEXT_PRIORITY_SOUL_REFLECTION_IR207_B02"
        group["sourceAuthority"] = authority_after
        group["freshPacketRequiredForCurrentAuthority"] = True
assert set(spell_id for group in groups for spell_id in group["pendingIds"]) == pending_after
next_group = next(group for group in groups if group["group"] == NEXT_GROUP)
next_record = {
    "identity": NEXT_ID, "group": NEXT_GROUP, "pendingIds": [NEXT_ID], "pendingCount": 1,
    "blocker": NEXT_BLOCKER, "status": "GPT_DIRECTED_FRESH_CURRENT_AUTHORITY_PACKET_REQUIRED",
    "freshPacketRequiredForCurrentAuthority": True,
    "requiredWitnessScope": ["changed-form attached/no-phase recipient lifecycle",
                             "original-target zero/death settlement", "copied concentration ending",
                             "actual original cargo entrusted to the reflection"],
    "nextAction": "Prepare Soul Reflection at authority 814/34/0. Build the director-named lifecycle witnesses, request explicit GPT acceptance, then independently apply only accepted identities.",
}

write_json(PENDING_AUDIT, {
    **copy.deepcopy(pending_audit_before),
    "id": "CURRENT34-PENDING-IDENTITY-AUDIT-262",
    "recordedAtUtc": now(),
    "status": "PASS_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_MATTER_CONVERSION_APPLICATION",
    "authority": authority_after,
    "indexBinding": bind(INDEX, encode_json(index_after)),
    "catalogBinding": catalog_binding,
    "pendingCount": 34,
    "pendingIds": sorted(pending_after),
    "groups": groups,
    "allPendingIdsExistInNativeCatalog": pending_after <= {row["id"] for row in catalog_before["spells"]},
    "noPendingTargetWasSilentlyAccepted": True,
    "acceptedIds": sorted(set(pending_audit_before.get("acceptedIds", [])) | {ID}),
    "appliedIds": sorted(set(pending_audit_before.get("appliedIds", [])) | {ID}),
    "heldIds": sorted(pending_after),
    "allCurrentPendingIdentitiesReviewed": True,
    "unreviewedPendingIds": [],
    "applicationReceipt": application_binding,
    "directorDecision": decision_binding,
    "nextBlockerPriority": {"identity": NEXT_ID, "group": NEXT_GROUP, "blockerId": NEXT_BLOCKER},
})
pending_audit_binding = bind(PENDING_AUDIT)
write_json(QUEUE, {
    **copy.deepcopy(queue_before),
    "id": "CURRENT-SPELL-QUEUE-262",
    "recordedAtUtc": now(),
    "supersedesQueue": "CURRENT_SPELL_QUEUE_261.json",
    "currentAuthority": authority_after,
    "currentIndexBinding": bind(INDEX, encode_json(index_after)),
    "currentCatalogBinding": catalog_binding,
    "currentPendingGroups": groups,
    "nextSuggestedGroups": [next_group],
    "nextGroup": NEXT_GROUP,
    "next": next_record,
    "nextPreparedRequest": next_record,
    "pendingCount": 34,
    "pendingIdentityAudit": pending_audit_binding,
    "parentQueue": bind(A / "CURRENT_SPELL_QUEUE_261.json"),
    "lastReviewedBatch": {"group": GROUP, "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [], "blockerIdsClosed": [BLOCKER]},
    "justAppliedBatch": {"reviewId": REVIEW_ID, "applicationId": APPLICATION_ID, "ids": [ID], "count": 1,
                         "applicationReceipt": APPLICATION.relative_to(ROOT).as_posix(),
                         "directorDecision": DECISION.relative_to(ROOT).as_posix()},
    "packetStatus": "MATTER_CONVERSION_ACCEPTED_APPLIED_814_34_NEXT_SOUL_REFLECTION_IR207_B02",
    "status": "MATTER_CONVERSION_ACCEPTED_APPLIED_NEXT_GPT_DIRECTED_SOUL_REFLECTION_814_34",
    "recommendedClosurePriority": [NEXT_ID, "unholy-ascendance"],
    "githubChanges": False,
    "currentAcceptedPacket": {"archive": source_outer, "delivery": source_delivery,
                              "decision": decision_binding, "acceptance": acceptance_binding,
                              "application": application_binding},
    "activeReview": {"identity": NEXT_ID, "group": NEXT_GROUP, "blocker": NEXT_BLOCKER,
                     "stage": "GPT named missing lifecycle witnesses; prepare exact current-authority packet"},
    "directorRemainingWorkResponse": {"text": remaining_work_response, "source": {"conversationTitle": "Calibration review part 6", "url": GPT_URL}},
})
queue_binding = bind(QUEUE)
write_json(HANDOFF, {
    "id": "CURRENT-HANDOFF-262",
    "recordedAtUtc": now(),
    "supersedes": "CURRENT_HANDOFF_261.json",
    "status": "MATTER_CONVERSION_APPLIED_NEXT_SOUL_REFLECTION_814_34",
    "authority": authority_after,
    "indexBinding": bind(INDEX, encode_json(index_after)),
    "queueBinding": queue_binding,
    "queue": QUEUE.relative_to(ROOT).as_posix(),
    "pendingIdentityAudit": PENDING_AUDIT.relative_to(ROOT).as_posix(),
    "appliedThisStep": {"identity": ID, "application": APPLICATION.relative_to(ROOT).as_posix(),
                        "acceptance": ACCEPTANCE.relative_to(ROOT).as_posix(), "decision": DECISION.relative_to(ROOT).as_posix()},
    "acceptedThisStep": [ID],
    "retainedConditionalKernelIds": KERNELS,
    "nextStep": next_record["nextAction"],
    "nextGroup": NEXT_GROUP,
    "nextPendingCount": 1,
    "nextPendingIds": [NEXT_ID],
    "currentBlocker": {"identity": NEXT_ID, "group": NEXT_GROUP, "blockerId": NEXT_BLOCKER},
    "directorConnectionStatus": "GPT explicitly accepted Matter Conversion and named Soul Reflection / IR207-B02 as next; after application, 34 pending identities remain across 16 groups.",
    "githubChanges": False,
    "runtimeSelectionEnabled": False,
})
handoff_binding = bind(HANDOFF)
write_json(STATE_CORRECTION, {
    "id": "CURRENT-REVIEW-STATE-CORRECTION-262",
    "recordedAtUtc": now(),
    "status": "PASS_CURRENT_AUTHORITY_UPDATED_AFTER_EXPLICIT_GPT_ACCEPTANCE_AND_APPLICATION",
    "supersedes": "CURRENT_REVIEW_STATE_CORRECTION_257.json",
    "oldRecordsPreservedByteForByte": True,
    "acceptedIdentity": ID,
    "closedBlockerIds": [BLOCKER],
    "directorDecision": decision_binding,
    "acceptance": acceptance_binding,
    "application": application_binding,
    "indexOperations": {"path": OPERATIONS.relative_to(ROOT).as_posix()},
    "authorityAfter": authority_after,
    "pendingAudit": pending_audit_binding,
    "queue": queue_binding,
    "handoff": handoff_binding,
    "nextPriority": next_record,
    "scope": "One static authored procedure only; no runtime/global rule change.",
})
correction_binding = bind(STATE_CORRECTION)

# Apply only after all acceptance and provenance artifacts are written and the inverse is proven.
index_after_raw = encode_json(index_after)
temp_index = INDEX.with_name("authored_review_index.matterconversion262.tmp")
temp_index.write_bytes(index_after_raw)
temp_index.replace(INDEX)
assert CATALOG.read_bytes() == catalog_before_raw

write_json(OPERATIONS, {
    "id": "MATTER-CONVERSION-INDEX-OPERATIONS-262",
    "before": bind(BACKUP, index_before_raw),
    "after": bind(INDEX, index_after_raw),
    "operations": [
        {"op": "replace-entry", "identity": ID, "index": entry_index, "before": entry_before, "after": entry_after},
        {"op": "append-envelope", "identity": ID, "envelope": append_record},
        {"op": "update-counts", "before": index_before["authoredCounts"], "after": index_after["authoredCounts"],
         "standaloneProcedures": {"before": 537, "after": 538}},
    ],
    "onlyIdentityIds": [ID],
    "inverseSemanticExact": True,
    "catalogByteExact": True,
})

# Update the pre-existing submission ledger with the received director decision and application result.
submission_after = copy.deepcopy(submission_before)
submission_after.update({
    "recordedAtUtc": now(),
    "status": "DIRECTOR_ACCEPTED_AND_APPLICATION_INDEPENDENTLY_VERIFIED",
    "authority": {"reviewedApplied": 813, "pending": 35, "acceptedUnapplied": 0,
                  "completeStandaloneProcedures": 537, "scopedInterfaces": 173},
    "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [],
    "closedBlockerIds": [BLOCKER],
    "directorDecision": bind(DECISION),
    "acceptance": bind(ACCEPTANCE),
    "application": bind(APPLICATION),
    "returnReceipt": bind(RETURN_RECEIPT),
    "authorityAfterApplication": authority_after,
    "applicationValidation": VALIDATION.relative_to(ROOT).as_posix(),
    "return": {"explicitAccept": True, "accepted": True, "appliedAtDecision": False,
               "remainingPending": 34, "remainingGroups": 16, "next": next_record},
    "canonicalChanges": True,
    "githubChanges": False,
})
write_json(SUBMISSION, submission_after)

checks = [
    ("GPT explicit acceptance recorded", read_json(DECISION)["decision"] == "EXACT_ACCEPT" and read_json(DECISION)["accepted"] is True),
    ("one identity accepted and applied", read_json(APPLICATION)["acceptedIds"] == [ID] and read_json(APPLICATION)["appliedIds"] == [ID]),
    ("Packet261 exact hash and size", bind(PACKET)["sha256"] == delivery["archive"]["sha256"] and bind(PACKET)["bytes"] == delivery["archive"]["bytes"]),
    ("witness audit 60/60", read_json(audit_path)["passedChecks"] == read_json(audit_path)["checkCount"] == 60 and read_json(audit_path)["failedChecks"] == 0),
    ("index counts 814/34", read_json(INDEX)["authoredCounts"] == {"reviewed": 814, "pending": 34}),
    ("standalone procedures 538", read_json(INDEX)["representationCounts"]["completeReviewedStandaloneProcedures"] == 538),
    ("pending identity set exact", pending_after == {row["id"] for row in read_json(INDEX)["entries"] if row["authoredStatus"] == "pending-authored-procedure"}),
    ("pending identity count 34", len(pending_after) == 34),
    ("Matter Conversion removed from pending", ID not in pending_after),
    ("native catalog byte exact", CATALOG.read_bytes() == catalog_before_raw),
    ("source status preserved blocked", next(row for row in read_json(INDEX)["entries"] if row["id"] == ID)["sourceStatus"] == "blocked-pending-operational-review"),
    ("application inverse restores exact semantic index", inverse == index_before),
    ("before-index backup byte exact", BACKUP.read_bytes() == index_before_raw),
    ("pending groups exactly cover pending set", set(sid for group in groups for sid in group["pendingIds"]) == pending_after),
    ("next priority Soul Reflection IR207-B02", read_json(QUEUE)["next"]["blocker"] == NEXT_BLOCKER and read_json(QUEUE)["nextGroup"] == NEXT_GROUP),
    ("current queue authority matches index", read_json(QUEUE)["currentAuthority"] == authority_after),
    ("runtime remains disabled", read_json(PACKAGE / "MODEL.json")["runtimeSelectionEnabled"] is False),
    ("seven historical kernels retained conditional", len(read_json(PACKAGE / "RETAINED_QUALIFICATIONS.json")["conditionalKernelIds"]) == 7),
    ("all candidate package files pass their manifest", all((ROOT / row["path"]).stat().st_size == row["bytes"] and sha((ROOT / row["path"]).read_bytes()) == row["sha256"] for row in package_manifest["files"])),
]
assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
index_after_binding = bind(INDEX)
write_json(VALIDATION, {
    "id": "MATTER-CONVERSION-APPLICATION-VALIDATION-262",
    "recordedAtUtc": now(), "status": "PASS",
    "checksPassed": len(checks), "checkCount": len(checks), "checksFailed": 0,
    "checks": [{"check": name, "passed": passed} for name, passed in checks],
    "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER],
    "beforeIndex": bind(BACKUP, index_before_raw), "afterIndex": index_after_binding,
    "catalogByteExact": True, "sourceStatusPreservedAsBlocked": True,
    "runtimeSelectionEnabled": False, "witnessAudit": source_cases["audit"],
    "decision": decision_binding, "acceptance": acceptance_binding,
    "application": application_binding, "pendingIdentityAudit": pending_audit_binding,
    "queue": queue_binding, "handoff": handoff_binding,
    "inverseSemanticExact": inverse == index_before,
    "remainingPending": {"count": 34, "groups": 16, "next": next_record},
})
SNAPSHOT.write_text(
    "# Current spell review snapshot 262\n\n"
    "Authority: **814 applied / 34 pending / 0 accepted-unapplied; 538 complete standalone procedures / 173 scoped interfaces.**\n\n"
    "Matter Conversion / MF210-B02 was explicitly accepted by GPT and applied to the authored review index. The decision accepts only the preserved procedure and two bounded fixture witnesses; seven historical kernels remain conditional.\n\n"
    "Next GPT-directed priority: **Soul Reflection / IR207-B02**. GPT identified changed-form attached/no-phase recipient lifecycle witnesses, original-target zero/death settlement, copied concentration ending, and actual original cargo entrusted to the reflection. After Soul Reflection, Unholy Ascendance / CC194-B04 is next priority.\n\n"
    "34 identities across 16 groups remain pending. Runtime and downstream approval gates remain closed.\n",
    encoding="utf-8", newline="\n")
print(json.dumps({"status": "PASS", "identity": ID, "applied": True, "counts": authority_after,
                  "checksPassed": len(checks), "remaining": {"pending": 34, "groups": 16},
                  "next": next_record, "validation": bind(VALIDATION), "index": index_after_binding}, indent=2))
