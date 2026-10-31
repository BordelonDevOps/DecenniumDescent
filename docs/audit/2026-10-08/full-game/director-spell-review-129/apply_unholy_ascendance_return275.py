from __future__ import annotations

import copy
import hashlib
import json
import shutil
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
A = ROOT / "docs/audit/2026-10-08/full-game/director-spell-review-129"
ARCHIVE = A / "DD_Rank9_UnholyAscendance_Director_Return275.zip"
DELIVERY = A / "DD_Rank9_UnholyAscendance_Director_Return275_DELIVERY.json"
AUDIT = A / "RANK9_CASTINGCOST5_RETURN275_INDEPENDENT_AUDIT.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
P0 = A / "CURRENT33_PENDING_IDENTITY_AUDIT_270.json"
Q0 = A / "CURRENT_SPELL_QUEUE_270.json"
H0 = A / "CURRENT_HANDOFF_270.json"

PKG_REL = Path("DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9unholyascendance_reviewed_275")
PKG = ROOT / PKG_REL
MAN = ROOT / "DescentReviewChanges/ReviewBible/docs/spells/candidates/UNHOLY_ASCENDANCE_REVIEWED_275.md"
BACKUP = A / "authored_review_index.before_unholy_ascendance_275.json"
DEC = A / "UNHOLY_ASCENDANCE_DIRECTOR_DECISION_275.json"
ACC = A / "UNHOLY_ASCENDANCE_EXACT_ACCEPTANCE_275.json"
RCPT = A / "UNHOLY_ASCENDANCE_RETURN275_RECEIPT.json"
APP = A / "UNHOLY_ASCENDANCE_APPLICATION_275.json"
OPS = A / "UNHOLY_ASCENDANCE_INDEX_OPERATIONS_275.json"
VALID = A / "UNHOLY_ASCENDANCE_APPLICATION_VALIDATION_275.json"
P1 = A / "CURRENT32_PENDING_IDENTITY_AUDIT_275.json"
Q1 = A / "CURRENT_SPELL_QUEUE_275.json"
H1 = A / "CURRENT_HANDOFF_275.json"
SNAP = A / "CURRENT_SPELL_REVIEW_SNAPSHOT_275.md"

ID = "unholy-ascendance"
NAME = "Unholy Ascendance"
GROUP = "rank9-casting-cost5"
BLOCKER = "CC194-B04"
URL = "https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682"
NEXT = "mind-collapse"
NEXT_GROUP = "rank9-memory-denial6"
NEXT_BLOCKER = "MD196-B01"
ARCHIVE_SHA = "d8a8e33afbd3d8487741c6d3f714dee5c81b3601ed9e37d0459e4ae467798418"
BEFORE = {"reviewedApplied": 815, "pending": 33, "acceptedUnapplied": 0,
          "completeStandaloneProcedures": 539, "scopedInterfaces": 173}
AFTER = {"reviewedApplied": 816, "pending": 32, "acceptedUnapplied": 0,
         "completeStandaloneProcedures": 540, "scopedInterfaces": 173}
DIRECTOR_TEXT = (
    "ACCEPT — unholy-ascendance only. accepted=true, applied=false. CC194-B04 and UA274-I01/I02 are closed. "
    "Acceptance covers the reviewed spell-local procedure, UA270-LIFE/UA270-HEAL contracts, and preserved evidence. "
    "Independent verification passed: 46 archive members with exact allowlist, sizes, SHA-256 and CRCs; 117/117 current-source "
    "bindings including both repaired hashes; 11 cases, 51 events, 102 forward and 102 inverse operations; procedure content "
    "and all replay states/operations unchanged from reviewed Return274. Archive size 3,898,708 bytes; SHA-256 "
    f"{ARCHIVE_SHA}. Canonical index remains 815 applied / 33 pending / 0 accepted-unapplied, with 539 procedures / 173 interfaces. "
    "After application expected authority is 816 applied / 32 pending / 0 accepted-unapplied, with 540 procedures / 173 interfaces. "
    "Next priority: mind-collapse / MD196-B01. It still requires an acquired genuine full-turn grant and a legal actor preserving "
    "the three-regular-END clock, recharge and Ready history. All CC194-H01–H08, unrelated holds and downstream gates remain intact. "
    "No other identity is accepted or applied."
)
QUALIFICATIONS = [
    "Acceptance is limited to the exact static authored Unholy Ascendance procedure, its 11 reviewed cases and the bound UA270-LIFE/UA270-HEAL contracts.",
    "The demi-lich body overlay, acquired spell identity and actor clocks remain limited to the written procedure and witnessed traces; no generic monster abilities or new inventory are granted.",
    "The null, healing, death, suppression/resumption, form lifecycle, recharge, action-budget and ordinary casting branches retain the reviewed source and timing boundaries.",
    "All other qualifications and CC194-H01–H08, unrelated holds, runtime, implementation, playtest, balance, cosmology, domain-closure, completion and release gates remain intact.",
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
    value = path.read_bytes() if raw is None else raw
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(value), "sha256": sha(value),
            "crc32": f"{zlib.crc32(value) & 0xffffffff:08x}"}


def main() -> None:
    outputs = [MAN, BACKUP, ACC, RCPT, APP, OPS, VALID, P1, Q1, H1, SNAP]
    assert all(not p.exists() for p in outputs), "Refusing to overwrite an application artifact."
    if DEC.exists():
        prior_decision = read(DEC)
        assert prior_decision.get("id") == "RANK9-CASTINGCOST5-UNHOLY-ASCENDANCE-GPT-DIRECTOR-DECISION-275" \
            and prior_decision.get("accepted") is True and prior_decision.get("appliedAtDecision") is False, \
            "Refusing to overwrite a non-matching director decision artifact."
    partial_package_members = {"CASE_COVERAGE.json", "DIRECTOR_DECISION.json", "EVIDENCE_BINDINGS.json", "PROCEDURE_RECORD.json"}
    if PKG.exists():
        assert PKG.is_dir() and {p.name for p in PKG.iterdir()} == partial_package_members, \
            "Refusing to overwrite an unexpected package; only the four known partial files from this script are resumable."

    archive_raw = ARCHIVE.read_bytes()
    archive_binding = binding(ARCHIVE, archive_raw)
    delivery = read(DELIVERY)
    audit = read(AUDIT)
    assert archive_binding["bytes"] == 3_898_708 and archive_binding["sha256"] == ARCHIVE_SHA
    assert archive_binding["sha256"] == delivery["archive"]["sha256"] and archive_binding["bytes"] == delivery["archive"]["bytes"]
    assert delivery["memberCount"] == delivery["payloadMemberCount"] == 46
    assert delivery["spellId"] == ID and delivery["blockerIds"] == [BLOCKER]
    assert delivery["accepted"] is False and delivery["applied"] is False
    assert audit["status"] == "PASS_PACKAGE_BINDING_AND_REPLAY"
    assert all(row["passed"] for row in audit["checks"])
    assert audit["caseCount"] == 11 and audit["eventCount"] == 51 and audit["sourceBindingCount"] == 117

    index_raw, catalog_raw = INDEX.read_bytes(), CATALOG.read_bytes()
    index0, catalog0 = read(INDEX), read(CATALOG)
    pending0, queue0, handoff0 = read(P0), read(Q0), read(H0)
    assert index0["authoredCounts"] == {"reviewed": 815, "pending": 33}
    assert index0["representationCounts"]["completeReviewedStandaloneProcedures"] == 539
    assert pending0["authority"] == queue0["currentAuthority"] == handoff0["currentAuthority"] == BEFORE
    assert pending0["indexBinding"]["sha256"] == sha(index_raw)
    assert pending0["catalogBinding"]["sha256"] == sha(catalog_raw)
    assert queue0["currentIndexBinding"]["sha256"] == sha(index_raw)
    entry_i = next(i for i, row in enumerate(index0["entries"]) if row["id"] == ID)
    entry0 = copy.deepcopy(index0["entries"][entry_i])
    assert entry0["authoredStatus"] == "pending-authored-procedure"
    assert entry0["sourceStatus"] == "blocked-pending-operational-review"
    pending_ids0 = {row["id"] for row in index0["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert len(pending_ids0) == 33 and pending_ids0 == set(pending0["pendingIds"])
    assert pending0["nextBlockerPriority"]["identity"] == ID
    assert any(g["group"] == NEXT_GROUP and NEXT in g["pendingIds"] for g in pending0["groups"])

    delivery_rows = {row["name"]: row for row in delivery["members"]}
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        names = set(z.namelist())
        assert len(names) == 46 and names == set(delivery_rows)
        for name, row in delivery_rows.items():
            raw = z.read(name)
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"]
            assert f"{zlib.crc32(raw) & 0xffffffff:08x}" == row["crc32"]
        procedure_source = json.loads(z.read("procedures/unholy-ascendance.json"))
        source_binding_doc = json.loads(z.read("SOURCE_BINDING.json"))
        case_index = json.loads(z.read("case-index/CC194-B04-RETURN275.json"))
        case_paths = sorted(name for name in names if name.startswith("cases/") and name.endswith(".json"))
        cases = {name: json.loads(z.read(name)) for name in case_paths}
    assert procedure_source["id"] == ID and procedure_source["accepted"] is False and procedure_source["applied"] is False
    assert procedure_source["blockerIds"] == [BLOCKER]
    assert len(case_paths) == 11 and len(procedure_source["caseIds"]) == 11
    assert len(source_binding_doc["current117Bindings"]) == 117
    assert source_binding_doc["current117Bindings"][53]["sha256"] == "1887160f0f5227383d19b8add6c26faec71e501195c1f2cf17d9e5592bdb9a88"
    assert source_binding_doc["current117Bindings"][81]["sha256"] == "2e9612e80f2f907c4b30afddbcb75e611b57632739d264a84e074483bbb356b6"
    event_count = sum(len(case.get("events", [])) for case in cases.values())
    assert event_count == 51 and sum(int(row.get("eventCount", 0)) for row in case_index.get("cases", [])) == 51
    assert set(procedure_source["caseIds"]) == {case.get("id") for case in cases.values()}

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    delivery_binding = binding(DELIVERY)
    audit_binding = binding(AUDIT)
    source_procedure_member = delivery_rows["procedures/unholy-ascendance.json"]
    source_procedure_binding = {"archive": archive_binding, "memberPath": "procedures/unholy-ascendance.json",
                                "bytes": source_procedure_member["bytes"], "sha256": source_procedure_member["sha256"],
                                "crc32": source_procedure_member["crc32"]}
    witness_bindings = {}
    for name in case_paths:
        row = delivery_rows[name]
        witness_bindings[name] = {"archive": archive_binding, "memberPath": name, "bytes": row["bytes"],
                                  "sha256": row["sha256"], "crc32": row["crc32"]}

    decision = {
        "id": "RANK9-CASTINGCOST5-UNHOLY-ASCENDANCE-GPT-DIRECTOR-DECISION-275",
        "recordedAtUtc": now, "decision": "EXACT_ACCEPT", "identity": ID, "group": GROUP,
        "closedBlockerIds": [BLOCKER], "alsoClosedFindings": ["UA274-I01", "UA274-I02"],
        "accepted": True, "appliedAtDecision": False, "countsAtDecision": BEFORE,
        "source": {"service": "ChatGPT", "conversationTitle": "Calibration review part 6", "url": URL},
        "packet": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
        "exactAcceptance": {
            "status": "ACCEPT — unholy-ascendance only; accepted=true; applied=false",
            "accepted": True, "applied": False, "blockersClosed": [BLOCKER],
            "findingsClosed": ["UA274-I01", "UA274-I02"], "remainingBlockingDefect": None,
            "verified": ["46 archive members; exact allowlist, sizes, SHA-256 and CRCs.",
                         "117/117 current source bindings, including both repaired hashes.",
                         "11 cases, 51 events, 102 forward and 102 inverse operations.",
                         "Procedure content and all replay states/operations unchanged from reviewed Return274."],
            "scope": "The reviewed spell-local Unholy Ascendance procedure, UA270-LIFE/UA270-HEAL contracts and preserved evidence.",
            "retainedQualifications": QUALIFICATIONS,
        },
        "authorityAfterApplicationExpected": AFTER,
        "nextPriority": {"identity": NEXT, "group": NEXT_GROUP, "blocker": NEXT_BLOCKER,
                         "requirements": ["An acquired genuine full-turn grant.",
                                          "A legal actor preserving the three-regular-END clock, recharge and Ready history."]},
        "retainedQualifications": QUALIFICATIONS,
        "gatesStillClosed": ["runtime", "implementation", "human-play", "balance", "cosmology", "domain-closure", "completion", "release"],
    }
    write(DEC, decision)
    decision_binding = binding(DEC)

    procedure_record = copy.deepcopy(procedure_source)
    procedure_record.update({"status": "DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_APPLIED_TO_AUTHORED_REVIEW_INDEX_RUNTIME_DISABLED",
                             "accepted": True, "applied": True, "blockerIds": [], "closedBlockerIds": [BLOCKER],
                             "resolvedBlockerIds": [BLOCKER], "directorDecisionBinding": decision_binding,
                             "packetBinding": archive_binding, "deliveryManifestBinding": delivery_binding,
                             "independentAuditBinding": audit_binding, "sourceProcedureMemberBinding": source_procedure_binding,
                             "acceptedWitnessBindings": witness_bindings, "retainedQualifications": QUALIFICATIONS,
                             "scope": "Unholy Ascendance only; exact reviewed procedure and 11 Return275 cases. Runtime remains disabled."})

    case_coverage = {"id": "UNHOLY-ASCENDANCE-CASE-COVERAGE-275", "sourceProcedure": source_procedure_binding,
                     "witnessCases": [{"id": c["id"], "file": name, "member": witness_bindings[name],
                                       "eventCount": len(c.get("events", []))} for name, c in cases.items()],
                     "events": 51, "forwardOperations": 102, "inverseOperations": 102}
    evidence = {"id": "UNHOLY-ASCENDANCE-ACCEPTED-EVIDENCE-275", "directorDecision": decision_binding,
                "packet": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
                "sourceProcedureMember": source_procedure_binding, "witnesses": witness_bindings,
                "caseCoverage": case_coverage, "retainedQualifications": QUALIFICATIONS}

    PKG.mkdir(parents=True, exist_ok=True)
    write(PKG / "DIRECTOR_DECISION.json", decision)
    write(PKG / "PROCEDURE_RECORD.json", procedure_record)
    write(PKG / "CASE_COVERAGE.json", case_coverage)
    write(PKG / "EVIDENCE_BINDINGS.json", evidence)
    new_choices = procedure_record.get("newChoices", "")
    if isinstance(new_choices, str):
        choices_text = new_choices
    else:
        choices_text = "\n\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in new_choices.items())
    procedure_content = procedure_record["procedure"] + ("\n\n" + choices_text if choices_text else "")
    model = {"schemaVersion": 1, "moduleId": "rank9unholyascendance-reviewed-275",
             "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED",
             "scope": "Unholy Ascendance only; exact reviewed procedure and 11 Return275 cases; runtime disabled.",
             "acceptedIds": [ID], "unacceptedIds": [], "excludedPendingIds": sorted(pending_ids0 - {ID}),
             "unresolvedQualifications": {ID: QUALIFICATIONS},
             "sharedRequirements": {"scope": "No global/shared rule changes; native catalog unchanged; runtime selection disabled.",
                                    "runtimeSelectionEnabled": False},
             "spells": [{"id": ID, "name": NAME, "position": 0,
                         "procedure": {"id": "CC194-STATIC-UNHOLY-ASCENDANCE", "spellId": ID,
                                       "status": "director-accepted static authored procedure; applied to authored review index; runtime disabled",
                                       "accepted": True, "applied": True,
                                       "nativeCardUnchanged": copy.deepcopy(procedure_source["completeSourceAndAccess"]),
                                       "procedureContent": procedure_content,
                                       "spellLocalChoices": copy.deepcopy(procedure_record["newChoices"]),
                                       "retainedQualifications": QUALIFICATIONS, "closedBlockerIds": [BLOCKER],
                                       "directorDecisionId": decision["id"], "evidenceBindingsFile": "EVIDENCE_BINDINGS.json",
                                       "caseCoverageFile": "CASE_COVERAGE.json"},
                         "directorProcedureRecord": procedure_record,
                         "nativeCardUnchanged": copy.deepcopy(procedure_source["completeSourceAndAccess"]),
                         "caseIds": copy.deepcopy(procedure_source["caseIds"]), "runtimeSelectionEnabled": False}],
             "sourceArchive": archive_binding, "deliveryManifest": delivery_binding, "independentAudit": audit_binding,
             "caseCoverage": case_coverage, "evidenceBindings": evidence,
             "returnCounts": {"cases": 11, "events": 51, "forwardOperations": 102, "inverseOperations": 102},
             "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False, "implementationApproved": False,
             "humanPlaytested": False, "balanceApproved": False, "cosmologyModified": False,
             "domainClosure": False, "releaseApproved": False}
    write(PKG / "MODEL.json", model)
    manuscript = ("# Unholy Ascendance — accepted static authored procedure 275\n\n"
                  "GPT explicitly accepted Unholy Ascendance / CC194-B04 after Return275 corrected the two current-source hash fields and preserved all reviewed procedure and replay state content. "
                  "This application updates one authored-review index entry; the native catalog, runtime selection and downstream gates remain unchanged.\n\n"
                  "## Preserved native card\n\n" + json.dumps(procedure_source["completeSourceAndAccess"], ensure_ascii=False, indent=2) +
                  "\n\n## Accepted procedure and spell-local choices\n\n" + procedure_content +
                  "\n\n## Accepted witnesses\n\n" + "\n".join(f"- {c['id']}: {len(c.get('events', []))} events; archive member `{name}`."
                                                                    for name, c in cases.items()) +
                  "\n\n## Retained qualifications\n\n" + "\n".join(f"- {x}" for x in QUALIFICATIONS) + "\n")
    MAN.parent.mkdir(parents=True, exist_ok=True)
    MAN.write_text(manuscript, encoding="utf-8", newline="\n")
    (PKG / "STANDALONE_PROCEDURES.md").write_text(manuscript, encoding="utf-8", newline="\n")
    manifest = {"id": "UNHOLY-ASCENDANCE-PACKAGE-MANIFEST-275", "decision": decision_binding,
                "sourcePacket": archive_binding, "files": []}
    for file in sorted(x for x in PKG.rglob("*") if x.is_file() and x.name != "CANDIDATE_PACKAGE_MANIFEST.json"):
        manifest["files"].append({"path": (PKG_REL / file.relative_to(PKG)).as_posix(),
                                  "bytes": file.stat().st_size, "sha256": sha(file.read_bytes())})
    write(PKG / "CANDIDATE_PACKAGE_MANIFEST.json", manifest)
    model_binding = binding(PKG / "MODEL.json")
    package_binding = binding(PKG / "CANDIDATE_PACKAGE_MANIFEST.json")
    manuscript_binding = binding(MAN)
    coverage_binding = binding(PKG / "CASE_COVERAGE.json")
    evidence_binding = binding(PKG / "EVIDENCE_BINDINGS.json")

    acceptance = {"id": "RANK9-CASTINGCOST5-UNHOLY-ASCENDANCE-EXACT-ACCEPTANCE-275", "recordedAtUtc": now,
                  "status": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED", "acceptedIds": [ID], "appliedIds": [],
                  "closedBlockerIds": [BLOCKER], "closedFindings": ["UA274-I01", "UA274-I02"],
                  "directorDecision": decision_binding, "packet": archive_binding, "delivery": delivery_binding,
                  "independentAudit": audit_binding, "candidateEnvelope": model_binding,
                  "candidatePackageManifest": package_binding, "evidenceBindings": evidence_binding,
                  "caseCoverage": coverage_binding,
                  "countsBefore": {"reviewed": 815, "pending": 33, "acceptedUnapplied": 0},
                  "countsAfterAcceptanceBeforeApplication": {"reviewed": 815, "pending": 32, "acceptedUnapplied": 1},
                  "scope": decision["exactAcceptance"]["scope"], "retainedQualifications": QUALIFICATIONS}
    write(ACC, acceptance)
    acceptance_binding = binding(ACC)
    write(RCPT, {"id": "UNHOLY-ASCENDANCE-RETURN275-RECEIPT", "recordedAtUtc": now,
                 "status": "EXACT_ACCEPT_UNHOLY_ASCENDANCE", "acceptedIds": [ID], "appliedIds": [],
                 "closedBlockerIds": [BLOCKER], "closedFindings": ["UA274-I01", "UA274-I02"],
                 "directorDecision": decision_binding, "acceptance": acceptance_binding,
                 "packet": archive_binding, "delivery": delivery_binding, "nextPriority": decision["nextPriority"],
                 "sourceResponse": DIRECTOR_TEXT})
    receipt_binding = binding(RCPT)

    index1 = copy.deepcopy(index0)
    entry1 = copy.deepcopy(entry0)
    entry1.update({"authoredStatus": "reviewed-authored-operational-playtest",
                   "procedureFile": "../spell_candidates/rank9unholyascendance_reviewed_275/MODEL.json",
                   "procedurePointer": "/spells/0/procedure", "wholeCardPointer": "/spells/0", "wholeCardIdField": "id",
                   "sourceCatalogWholeCardPointer": entry0.get("sourceCatalogWholeCardPointer") or entry0["wholeCardPointer"],
                   "procedureTextPointer": "/spells/0/procedure/procedureContent",
                   "directorProcedureRecordPointer": "/spells/0/directorProcedureRecord",
                   "sharedRulesPointer": "/sharedRequirements", "spellLocalRequirementsPointer": "/spells/0/procedure/spellLocalChoices",
                   "manuscript": "../../../docs/spells/candidates/UNHOLY_ASCENDANCE_REVIEWED_275.md",
                   "reviewId": "RANK9-CASTINGCOST5-UNHOLY-ASCENDANCE-APPLICATION-275",
                   "runtimeSelectionEnabled": False, "historicalCandidateLabelsPreserved": True,
                   "completeEvidenceRoot": PKG_REL.as_posix(), "completeEnvelopeBinding": model_binding,
                   "caseEvidenceBindings": coverage_binding, "sourceArchiveBinding": archive_binding,
                   "deliveryManifestBinding": delivery_binding, "candidatePackageManifestBinding": package_binding,
                   "procedureSourceBinding": decision_binding, "authoredAcceptanceReceipt": acceptance_binding,
                   "authoredApplicationReceipt": {"path": APP.relative_to(ROOT).as_posix()},
                   "directorReturnReceipt": receipt_binding, "accepted": True, "applied": True,
                   "closedBlockerIds": [BLOCKER], "closedFindingIds": ["UA274-I01", "UA274-I02"],
                   "retainedQualifications": QUALIFICATIONS})
    index1["entries"][entry_i] = entry1
    assert not any(ID in row.get("acceptedIds", []) for row in index1["additionalStandaloneEnvelopes"])
    index1["additionalStandaloneEnvelopes"].append({"file": "../spell_candidates/rank9unholyascendance_reviewed_275/MODEL.json",
        "binding": model_binding, "reviewId": acceptance["id"], "acceptedIds": [ID], "unacceptedIds": [],
        "excludedPendingIds": sorted(pending_ids0 - {ID}), "authority": acceptance_binding,
        "applicationReceipt": APP.relative_to(ROOT).as_posix(), "directorDecision": decision_binding,
        "directorReturnReceipt": receipt_binding, "sourcePacket": archive_binding,
        "deliveryManifest": delivery_binding, "evidenceBindings": evidence_binding,
        "caseCoverage": coverage_binding, "candidatePackageManifestBinding": package_binding,
        "scope": "ONE_EXACT_STATIC_AUTHORED_PROCEDURE_ACCEPTED_AND_APPLIED_RUNTIME_DISABLED"})
    index1["authoredCounts"] = {"reviewed": 816, "pending": 32}
    index1["representationCounts"]["completeReviewedStandaloneProcedures"] = 540
    pending_ids1 = {row["id"] for row in index1["entries"] if row["authoredStatus"] == "pending-authored-procedure"}
    assert pending_ids1 == pending_ids0 - {ID} and len(pending_ids1) == 32 and NEXT in pending_ids1
    index_binding0 = binding(BACKUP, index_raw)
    if BACKUP.exists():
        assert BACKUP.read_bytes() == index_raw
    else:
        BACKUP.write_bytes(index_raw)
    write(INDEX, index1)
    index_binding1 = binding(INDEX)

    write(APP, {"id": "RANK9-CASTINGCOST5-UNHOLY-ASCENDANCE-APPLICATION-275", "recordedAtUtc": now,
                "status": "APPLIED_ONE_EXACT_DIRECTOR_ACCEPTED_AUTHORED_PROCEDURE",
                "acceptedIds": [ID], "appliedIds": [ID], "closedBlockerIds": [BLOCKER],
                "closedFindings": ["UA274-I01", "UA274-I02"], "directorAcceptance": acceptance_binding,
                "directorDecision": decision_binding, "directorReturnReceipt": receipt_binding,
                "packet": archive_binding, "delivery": delivery_binding, "independentAudit": audit_binding,
                "candidateEnvelope": model_binding, "candidatePackageManifest": package_binding,
                "evidenceBindings": evidence_binding, "caseCoverage": coverage_binding, "manuscript": manuscript_binding,
                "indexBefore": index_binding0, "indexAfter": index_binding1,
                "countsBefore": BEFORE, "countsAfter": AFTER, "completeReviewedStandaloneProcedures": {"before": 539, "after": 540},
                "scopedInterfaces": 173, "catalogChanged": False, "sourceStatusPreservedAsBlocked": True,
                "runtimeSelectionEnabled": False, "runtimeTestsExecuted": False,
                "implementationApproved": False, "humanPlaytested": False, "balanceApproved": False,
                "cosmologyModified": False, "domainClosure": False, "releaseApproved": False})
    app_binding = binding(APP)
    entry1["authoredApplicationReceipt"] = app_binding
    index1["entries"][entry_i] = entry1
    index1["additionalStandaloneEnvelopes"][-1]["applicationReceipt"] = APP.relative_to(ROOT).as_posix()
    index1["additionalStandaloneEnvelopes"][-1]["authority"] = acceptance_binding
    write(INDEX, index1)
    index_binding1 = binding(INDEX)

    write(OPS, {"id": "UNHOLY-ASCENDANCE-INDEX-OPERATIONS-275", "recordedAtUtc": now,
                "before": index_binding0, "after": index_binding1, "operations": [
                    {"op": "update-entry", "id": ID, "before": entry0, "after": entry1},
                    {"op": "append-standalone-envelope", "acceptedIds": [ID]},
                    {"op": "update-counts", "before": {"reviewed": 815, "pending": 33}, "after": {"reviewed": 816, "pending": 32}},
                    {"op": "update-procedure-count", "before": 539, "after": 540}],
                "catalogByteExact": CATALOG.read_bytes() == catalog_raw, "nativeCardUnchanged": True,
                "sourceStatusPreservedAsBlocked": True, "inverseRestoresExactIndex": True})
    ops_binding = binding(OPS)
    assert CATALOG.read_bytes() == catalog_raw

    authority1 = copy.deepcopy(AFTER)
    p1 = copy.deepcopy(pending0)
    groups1 = [g for g in p1["groups"] if g.get("group") != GROUP]
    p1.update({"id": "CURRENT32-PENDING-IDENTITY-AUDIT-275", "recordedAtUtc": now,
               "status": "PASSED_EXACT_CURRENT_INDEX_PENDING_SET_AFTER_UNHOLY_ASCENDANCE_APPLICATION_275",
               "authority": authority1, "indexBinding": index_binding1, "catalogBinding": binding(CATALOG, catalog_raw),
               "pendingCount": 32, "pendingIds": sorted(pending_ids1),
               "groups": groups1,
               "heldIds": sorted(set(pending0.get("heldIds", [])) - {ID}),
               "acceptedIds": sorted(set(pending0.get("acceptedIds", [])) | {ID}),
               "appliedIds": sorted(set(pending0.get("appliedIds", [])) | {ID}),
               "pendingGroupCount": sum(1 for g in groups1 if g.get("pendingCount", 0) > 0),
               "nextBlockerPriority": decision["nextPriority"], "applicationReceipt": app_binding,
               "directorDecision": decision_binding, "acceptanceReceipt": acceptance_binding,
               "closedBlockerIdsThisStep": sorted(set(pending0.get("closedBlockerIdsThisStep", [])) | {BLOCKER}),
               "preparedNextGroup": {"group": NEXT_GROUP, "pendingIds": [NEXT],
                   "freshPacketRequiredForCurrentAuthority": True,
                   "historicalPreparedPacket": next(g for g in pending0["groups"] if g.get("group") == NEXT_GROUP).get("preparedPacket"),
                   "directorRequirement": decision["nextPriority"]["requirements"]}})
    p1["allCurrentPendingIdentitiesReviewed"] = True
    p1["unreviewedPendingIds"] = []
    p1["noPendingTargetWasSilentlyAccepted"] = True
    p1["allPendingIdsExistInNativeCatalog"] = pending_ids1 <= {row["id"] for row in catalog0["spells"]}
    p1["pendingIdentityCount"] = 32
    write(P1, p1)
    p1_binding = binding(P1)

    q1 = copy.deepcopy(queue0)
    old_next_group = next(g for g in pending0["groups"] if g.get("group") == NEXT_GROUP)
    next_data = {"group": NEXT_GROUP, "pendingIds": [NEXT], "pendingCount": 1,
                 "status": "FRESH_CURRENT_SOURCE_PACKET_REQUIRED_FOR_AUTHORITY_816_32",
                 "historicalPreparedPacket": old_next_group.get("preparedPacket"),
                 "historicalDeliveryManifest": old_next_group.get("deliveryManifest"),
                 "freshPacketRequiredForCurrentAuthority": True, "directorRequirement": decision["nextPriority"]["requirements"]}
    q1.update({"id": "SPELL-REVIEW-QUEUE-275", "recordedAtUtc": now, "supersedesQueue": binding(Q0),
               "parentQueue": binding(Q0), "currentAuthority": authority1, "currentIndexBinding": index_binding1,
               "pendingIdentityAudit": p1_binding, "pendingCount": 32, "nextGroup": NEXT_GROUP,
               "next": next_data, "nextPendingIds": sorted(pending_ids1), "currentPendingGroups": copy.deepcopy(p1["groups"]),
               "nextSuggestedGroups": [next_data], "recommendedClosurePriority": [NEXT, "absolute-domination", "puppetmaster-s-realm"],
               "recommendedClosureOrder": [{"rank": 1, "identities": [NEXT], "priority": "; ".join(decision["nextPriority"]["requirements"])}],
               "lastReviewedBatch": {"group": GROUP, "acceptedIds": [ID], "appliedIds": [ID], "heldIds": [],
                                     "closedBlockerIds": [BLOCKER]},
               "justAppliedBatch": {"reviewId": acceptance["id"], "applicationId": APP.stem,
                                    "ids": [ID], "count": 1, "applicationReceipt": APP.relative_to(ROOT).as_posix(),
                                    "directorDecision": decision_binding, "sourceArchive": archive_binding,
                                    "deliveryManifest": delivery_binding, "independentAudit": audit_binding},
               "packetStatus": "UNHOLY_ASCENDANCE_APPLIED; NEXT_MIND_COLLAPSE_REQUIRES_FRESH_PACKET",
               "currentAcceptedPacket": {"archive": archive_binding, "delivery": delivery_binding,
                                          "independentAudit": audit_binding, "decision": decision_binding,
                                          "acceptance": acceptance_binding, "application": app_binding},
               "directorRemainingWorkResponse": {"text": DIRECTOR_TEXT, "source": {"conversationTitle": "Calibration review part 6", "url": URL}},
               "noFirstReviewTasksRemain": True, "afterNextAcceptedAppliedForecast": {"remainingIdentities": 31,
                                                                                     "remainingGroups": p1["pendingGroupCount"] - 1},
               "githubChanges": False, "canonicalRuntimeApplicationPerformed": False,
               "nextPriorityContext": decision["nextPriority"]})
    q1["currentPendingGroups"] = [g for g in p1["groups"]]
    write(Q1, q1)
    q1_binding = binding(Q1)

    handoff1 = copy.deepcopy(handoff0)
    handoff1.update({"id": "CURRENT-HANDOFF-275", "recordedAtUtc": now, "supersedes": handoff0["id"],
                     "status": "UNHOLY_ASCENDANCE_APPLIED_NEXT_MIND_COLLAPSE_816_32",
                     "authority": authority1, "currentAuthority": authority1, "indexBinding": index_binding1,
                     "queueBinding": q1_binding, "queue": Q1.relative_to(ROOT).as_posix(),
                     "pendingIdentityAudit": p1_binding, "appliedThisStep": True,
                     "acceptedThisStep": [ID], "appliedThisStepRecord": {"identity": ID, "application": APP.relative_to(ROOT).as_posix(),
                                                                           "applicationBinding": app_binding},
                     "nextStep": next_data, "nextGroup": NEXT_GROUP, "nextPendingCount": 1, "nextPendingIds": [NEXT],
                     "currentBlocker": {"identity": NEXT, "group": NEXT_GROUP, "blockerId": NEXT_BLOCKER},
                     "directorConnectionStatus": "GPT explicitly accepted and applied Unholy Ascendance; next priority is Mind Collapse / MD196-B01.",
                     "githubChanges": False, "latestBatch": {"accepted": [ID], "applied": [ID], "closed": [BLOCKER]},
                     "currentPreparation": next_data, "currentPacket": old_next_group.get("preparedPacket"),
                     "currentPacketDelivery": old_next_group.get("deliveryManifest"),
                     "canonicalRuntimeApplicationPerformed": False})
    write(H1, handoff1)
    h1_binding = binding(H1)

    validation_checks = [
        ("GPT explicitly accepted only Unholy Ascendance and left application to Codex", decision["accepted"] is True and decision["appliedAtDecision"] is False),
        ("Return275 archive and 46 member hashes/CRCs verify", len(delivery_rows) == 46 and archive_binding["sha256"] == ARCHIVE_SHA),
        ("117 current-source bindings and both repaired hashes verify", len(source_binding_doc["current117Bindings"]) == 117),
        ("11 reviewed cases contain 51 events and reversible operation counts", len(cases) == 11 and event_count == 51),
        ("Only Unholy Ascendance leaves the pending set", pending_ids1 == pending_ids0 - {ID}),
        ("Counts are 816 applied / 32 pending / 0 accepted-unapplied", index1["authoredCounts"] == {"reviewed": 816, "pending": 32}),
        ("Complete standalone procedure count increments to 540", index1["representationCounts"]["completeReviewedStandaloneProcedures"] == 540),
        ("Native spell catalog remains byte-exact and runtime remains disabled", CATALOG.read_bytes() == catalog_raw and model["runtimeSelectionEnabled"] is False),
        ("Next priority is Mind Collapse / MD196-B01 and requires a fresh current-authority packet", q1["next"]["group"] == NEXT_GROUP and q1["next"]["freshPacketRequiredForCurrentAuthority"] is True),
    ]
    assert all(ok for _, ok in validation_checks)
    write(VALID, {"id": "UNHOLY-ASCENDANCE-APPLICATION-VALIDATION-275", "recordedAtUtc": now,
                  "status": "PASS", "checks": [{"check": label, "passed": ok} for label, ok in validation_checks],
                  "checkCount": len(validation_checks), "failedChecks": 0, "acceptedIds": [ID], "appliedIds": [ID],
                  "authority": authority1, "index": index_binding1, "application": app_binding,
                  "pendingIdentityAudit": p1_binding, "queue": q1_binding, "handoff": h1_binding,
                  "catalogByteExact": True, "sourceStatusPreservedAsBlocked": True, "runtimeSelectionEnabled": False})
    valid_binding = binding(VALID)
    SNAP.write_text(("# Spell Review Snapshot — Return275 Application\n\n"
                 "Authority: **816 applied / 32 pending / 0 accepted-unapplied; 540 complete standalone procedures / 173 scoped interfaces.**\n\n"
                 "Unholy Ascendance / CC194-B04 was explicitly accepted by GPT and applied to the authored review index. "
                 "The native spell catalog and runtime selection remain unchanged.\n\n"
                 "Next priority: **Mind Collapse / MD196-B01**. GPT requires an acquired genuine full-turn grant and a legal actor that preserves the three-regular-END clock, recharge and Ready history. A fresh source packet must bind the updated current authority before director review.\n\n"
                 f"Validation: {valid_binding['path']} ({valid_binding['sha256']}).\n"), encoding="utf-8", newline="\n")
    assert read(INDEX)["authoredCounts"] == {"reviewed": 816, "pending": 32}
    print(json.dumps({"status": "PASS", "acceptedApplied": ID, "authority": AFTER,
                      "pendingAudit": str(P1), "queue": str(Q1), "handoff": str(H1),
                      "validation": str(VALID), "next": decision["nextPriority"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
